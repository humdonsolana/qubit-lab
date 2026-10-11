"""Regenerate actual strict-QASM submitted jobs; compare estimator with ED/Aer.
The first sampler transport returned only top64: insufficient for a mean.
Second estimator job measured the full Hamiltonian, not truncated counts.
No hardware settings beyond tool-returned fields are available.
"""
import sys,json
from pathlib import Path
import numpy as np
from qiskit import QuantumCircuit,transpile,qasm2
from qiskit.circuit.library import StatePreparation
from qiskit.quantum_info import Statevector,SparsePauliOp
from bilayer_spin_benchmark import exact,BONDS
root=Path(__file__).resolve().parent
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
target,s=exact(2)
q=QuantumCircuit(4);q.append(StatePreparation(s),range(4));q=transpile(q,basis_gates=['u','cx'],optimization_level=3,seed_transpiler=10)
obs=[(''.join(p if k in (i,j) else 'I' for k in reversed(range(4))),.5 if n<2 else .25) for n,(i,j) in enumerate(BONDS) for p in 'XYZ']
text=qasm2.dumps(q).replace('include "qelib1.inc";','include "qelib1.inc";\ngate u(theta,phi,lambda) a { U(theta,phi,lambda) a; }')
q2=qasm2.loads(text);ex=float(Statevector(q2).expectation_value(SparsePauliOp.from_list(obs)).real)
assert abs(ex-target['energy'])<1e-12
(out/'spin_estimator.qasm').write_text(text+'\n')
# Regenerate strict sampler from Aer-tested generated qasm.
sampler=(out/'spin.qasm').read_text().replace('include "qelib1.inc";','include "qelib1.inc";\ngate u(theta,phi,lambda) a { U(theta,phi,lambda) a; }')
assert qasm2.loads(sampler).num_qubits==12
(out/'spin_sampler_submitted.qasm').write_text(sampler)
raw=json.loads((root/'outputs/qpu_estimator_raw.json').read_text());top=json.loads((root/'outputs/qpu_sampler_top64.json').read_text());sim=json.loads((root/'outputs/spin_simulation.json').read_text())
d=raw['expectation']-ex;n=sum(top['counts'].values())
aer=sim['aer']['estimates']['energy']
r={'exact_energy_Jleg':ex,'aer_energy':aer,'hardware':raw,'hardware_minus_exact':d,'difference_over_returned_std':d/raw['std'],'relative_energy_error':abs(d/ex),'sampler_returned_count':n,'sampler_missing_count':4096-n,'sampler_missing_fraction':(4096-n)/4096,'total_quantum_seconds':17,'sampler_first_attempt':'rejected QASM undefined u; no hardware job. Added gate definition, same unitary.','interpretation':'Hardware systematic disagreement far exceeds reported std. Do not use energy as calibrated material/pairing prediction. Sampler top64 cannot yield unbiased correlation. Estimator uncertainty is tool reported, not full systematic uncertainty.','observables':[{'pauli':p,'coefficient':c} for p,c in obs]}
(out/'qpu_comparison.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
