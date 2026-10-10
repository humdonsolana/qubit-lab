"""Two-site, one-up/one-down Hubbard benchmark, NOT a FeSe Tc model.
Run: python hubbard_dimer_qpu.py /tmp/astra7
Encoding |q1 q0>: each bit locates one spin species. Species-ordered
fermionic basis gives H=-t(XI+IX)+U/2(II+ZZ). N_up=N_down=1 exactly.
P=(XX-YY)/2 is intersite on-site-pair hopping. D=(1+ZZ)/2 is total
on-site double occupancy. Finite P is not superconductivity or binding.
Six physical qubits are three independent replicas measured in Z/X/Y.
All parameters dimensionless, U/t=4, not fitted to FeSe. No error mitigation.
"""
import sys,json,platform
from pathlib import Path
import numpy as np
import qiskit,qiskit_aer
from qiskit import QuantumCircuit,transpile,qasm2
from qiskit.quantum_info import Statevector,SparsePauliOp
from qiskit_aer import AerSimulator

OUT=Path(sys.argv[1] if len(sys.argv)>1 else 'outputs');OUT.mkdir(parents=True,exist_ok=True)
u=4.;t=1.;shots=4096
# symmetric ground: c_D Phi+ + c_S Psi+, beta=2 atan(c_S/c_D)
D=(1-u/np.sqrt(u*u+16*t*t))/2
beta=2*np.arctan2(np.sqrt(1-D),np.sqrt(D))
prep=QuantumCircuit(2);prep.h(0);prep.ry(beta,1);prep.cx(0,1)
sv=Statevector.from_instruction(prep)
ops={s:SparsePauliOp.from_list([(s,1.)]) for s in ['ZZ','XI','IX','XX','YY']}
exact={s:float(sv.expectation_value(op).real) for s,op in ops.items()}
H=SparsePauliOp.from_list([('XI',-t),('IX',-t),('II',u/2),('ZZ',u/2)])
eval0,vec=np.linalg.eigh(H.to_matrix());E=float(sv.expectation_value(H).real)
assert abs(E-eval0[0])<1e-12
assert abs(abs(np.vdot(vec[:,0],sv.data))**2-1)<1e-12
exact.update(E_over_t=E,D=D,P=(exact['XX']-exact['YY'])/2)
qc=QuantumCircuit(6,6)
for k,basis in enumerate(['Z','X','Y']):
    a,b=2*k,2*k+1
    qc.compose(prep,[a,b],inplace=True)
    if basis=='X':qc.h(a);qc.h(b)
    if basis=='Y':qc.sdg(a);qc.sdg(b);qc.h(a);qc.h(b)
qc.measure(range(6),range(6))
qasm=qasm2.dumps(qc);(OUT/'dimer.qasm').write_text(qasm+'\n')
sim=AerSimulator(); counts=sim.run(transpile(qc,sim),shots=shots,seed_simulator=7007).result().get_counts()

def analyze_counts(counts):
    N=sum(counts.values()); rows=[]; weights=[]
    for bits,n in counts.items():
        bits=bits.replace(' ','')
        if bits.startswith('0x'):bits=format(int(bits,16),'06b')
        bits=bits.zfill(6)
        z=[1-2*int(c) for c in bits[::-1]]
        zz=z[0]*z[1];xx=z[2]*z[3];yy=z[4]*z[5]
        rows.append([(1+zz)/2,(xx-yy)/2,-z[2]-z[3]+u*(1+zz)/2,zz,xx,yy])
        weights.append(n)
    rows=np.array(rows);w=np.array(weights);mean=np.average(rows,axis=0,weights=w)
    # Unbiased sample variance / N; includes correlations within each shot.
    se=np.sqrt(np.sum(w[:,None]*(rows-mean)**2,axis=0)/(N*(N-1)))
    return {'shots':N,'estimates':{key:{'mean':float(m),'shot_se':float(s)} for key,m,s in zip(['D','P','E_over_t','ZZ','XX','YY'],mean,se)}}
if __name__=='__main__':
    res={'purpose':'Finite Hubbard-dimer estimator calibration; no material Tc forecast','U_over_t':u,'beta':beta,'exact':exact,'aer':analyze_counts(counts),'aer_counts':counts,'versions':{'python':platform.python_version(),'qiskit':qiskit.__version__,'qiskit_aer':qiskit_aer.__version__},'seed':7007,'qasm_logical_qubits':6,'logical_cx_count':3}
    (OUT/'qpu_simulation.json').write_text(json.dumps(res,indent=2)+'\n')
    print(json.dumps(res,indent=2));print('\nQASM\n'+qasm)
