"""Diagnostic pair-island toy model, NOT a microscopic FeSe or Tc calculation.
One preformed hard-core pair on two islands: H=-J(XX+YY)/2+delta(Z0-Z1)/2.
Pair binding omitted/fixed. Contrast coherence at delta/J=0 and 3.
Two identical copies per case measure X correlations and Z number conservation.
"""
import json
from pathlib import Path
import numpy as np
from qiskit import QuantumCircuit, transpile, qasm2
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
out=Path('outputs'); out.mkdir(exist_ok=True)
qc=QuantumCircuit(8,8)
expected=[]
for k,delta in enumerate([0.,3.]):
    theta=.5*np.arctan2(1.,delta)
    for base in [2*k,4+2*k]:
        qc.x(base); qc.ry(2*theta,base+1); qc.cx(base+1,base)
    qc.h(2*k); qc.h(2*k+1)
    expected.append({'delta_over_J':delta,'ground_energy_over_J':-float(np.sqrt(1+delta**2)), 'XX':float(1/np.sqrt(1+delta**2)), 'ZZ':-1.})
qc.measure(range(8),range(8))
backend=AerSimulator(); compiled=transpile(qc,backend,seed_transpiler=15)
counts=backend.run(compiled,shots=4096,seed_simulator=15).result().get_counts()
qasm=qasm2.dumps(qc); (out/'pair_coherence.qasm').write_text(qasm)
def summarize(counts):
    n=sum(counts.values()); result={}
    for k,delta in enumerate([0.,3.]):
        means=[]
        for base in [2*k,4+2*k]:
            val=sum(c*(1 if ((int(s.replace(' ',''),2)>>base)&1)==((int(s.replace(' ',''),2)>>(base+1))&1) else -1) for s,c in counts.items())/n
            means.append(val)
        result[str(delta)]={'XX':means[0], 'XX_stderr':float(np.sqrt(max(0,1-means[0]**2)/n)), 'ZZ':means[1], 'odd_parity_probability':(1-means[1])/2}
    return result
report={'model':'two preformed pair islands, J=1; arbitrary dimensionless delta/J, not measured material parameters','expected':expected,'shots':4096,'circuit_depth':qc.depth(),'operations':dict(qc.count_ops()),'counts':counts,'simulation':summarize(counts),'limitations':'Not Fe orbital model; no finite-T transition; no gap prediction; XX=YY only for ideal real number-conserving state. Hardware reports XX, not assumed YY.'}
(out/'pair_coherence_simulation.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='counts'},indent=2)); print(qasm)
