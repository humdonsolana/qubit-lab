"""Hg1223-source-parameter EXTENDED Hubbard dimer benchmark, not a Tc model.
Sources: Kaneko & Imada arXiv:2606.08181v2 Table I (IP, 0/30 GPa).
Retain one nearest-neighbor bond, one up and one down electron; OMIT all
other bonds, doping, planes, lattice, defects, phonons and metastability.
Species-position encoding |q1 q0> gives:
H=-t(XI+IX)+(U+V)/2 II+(U-V)/2 ZZ, D=(II+ZZ)/2,
P_pairhop=(XX-YY)/2. Positive P is NOT pair binding/superconductivity.
Prepare exact real ground states for both endpoints; 3 independent replicas
per endpoint to measure Z/X/Y. All qubits measured in one sampler circuit.
"""
import sys,json,platform
from pathlib import Path
import numpy as np
import qiskit,qiskit_aer
from qiskit import QuantumCircuit,transpile,qasm2
from qiskit.quantum_info import Statevector,SparsePauliOp
from qiskit_aer import AerSimulator
OUT=Path(sys.argv[1] if len(sys.argv)>1 else 'outputs');OUT.mkdir(exist_ok=True,parents=True)
PARAMS=[dict(P_GPa=0,t_eV=.4857,U_eV=4.5184,V_eV=.9878),dict(P_GPa=30,t_eV=.5833,U_eV=4.3615,V_eV=.8752)]
SHOTS=8192

def exact_prep(p):
 t,u,v=p['t_eV'],p['U_eV'],p['V_eV'];w=u-v
 D=(1-w/np.sqrt(w*w+16*t*t))/2
 beta=2*np.arctan2(np.sqrt(1-D),np.sqrt(D))
 prep=QuantumCircuit(2);prep.h(0);prep.ry(beta,1);prep.cx(0,1)
 sv=Statevector.from_instruction(prep)
 ops={s:SparsePauliOp.from_list([(s,1.)]) for s in ['ZZ','XI','IX','XX','YY']}
 exact={s:float(sv.expectation_value(op).real) for s,op in ops.items()}
 H=SparsePauliOp.from_list([('XI',-t),('IX',-t),('II',(u+v)/2),('ZZ',w/2)])
 E,vec=np.linalg.eigh(H.to_matrix());energy=float(sv.expectation_value(H).real)
 assert abs(E[0]-energy)<1e-12
 assert abs(abs(np.vdot(vec[:,0],sv.data))**2-1)<1e-12
 exact.update(D=D,P_pairhop=(exact['XX']-exact['YY'])/2,E_eV=energy,U_over_t=u/t,V_over_t=v/t)
 return prep,exact

EXACT=[exact_prep(p)[1] for p in PARAMS]

def analyze_counts(counts):
 N=sum(counts.values());rows=[];weights=[]
 for bits,n in counts.items():
  bits=bits.replace(' ','')
  if bits.startswith('0x'):bits=format(int(bits,16),'012b')
  z=[1-2*int(c) for c in bits.zfill(12)[::-1]];row=[]
  for j,p in enumerate(PARAMS):
   a=6*j;zz=z[a]*z[a+1];xx=z[a+2]*z[a+3];yy=z[a+4]*z[a+5]
   D=(1+zz)/2;P=(xx-yy)/2
   E=-p['t_eV']*(z[a+2]+z[a+3])+p['V_eV']+(p['U_eV']-p['V_eV'])*D
   row.extend([D,P,E])
  row.extend([row[3]-row[0],row[4]-row[1]])
  rows.append(row);weights.append(n)
 rows=np.array(rows);w=np.array(weights);mean=np.average(rows,axis=0,weights=w)
 se=np.sqrt(np.sum(w[:,None]*(rows-mean)**2,axis=0)/(N*(N-1)))
 keys=['D_0','P_0','E_0_eV','D_30','P_30','E_30_eV','delta_D','delta_P']
 true=[EXACT[0]['D'],EXACT[0]['P_pairhop'],EXACT[0]['E_eV'],EXACT[1]['D'],EXACT[1]['P_pairhop'],EXACT[1]['E_eV'],EXACT[1]['D']-EXACT[0]['D'],EXACT[1]['P_pairhop']-EXACT[0]['P_pairhop']]
 return dict(shots=N,estimates={k:dict(mean=float(m),shot_se=float(s),exact=float(e),bias=float(m-e)) for k,m,s,e in zip(keys,mean,se,true)})

def main():
 qc=QuantumCircuit(12,12)
 for j,p in enumerate(PARAMS):
  prep,_=exact_prep(p)
  for k,basis in enumerate(['Z','X','Y']):
   a,b=6*j+2*k,6*j+2*k+1;qc.compose(prep,[a,b],inplace=True)
   if basis=='X':qc.h(a);qc.h(b)
   if basis=='Y':qc.sdg(a);qc.sdg(b);qc.h(a);qc.h(b)
 qc.measure(range(12),range(12))
 (OUT/'hg_dimer.qasm').write_text(qasm2.dumps(qc)+'\n')
 sim=AerSimulator();counts=sim.run(transpile(qc,sim),shots=SHOTS,seed_simulator=8008).result().get_counts()
 result=dict(source='arXiv:2606.08181v2 Table I IP, already LRFB-corrected U; do not multiply U by0.95 again',parameters=PARAMS,exact=EXACT,aer=analyze_counts(counts),aer_counts=counts,seed=8008,logical_qubits=12,logical_cx_count=6,versions=dict(python=platform.python_version(),qiskit=qiskit.__version__,qiskit_aer=qiskit_aer.__version__),limitations=['Half-filled two-site bond truncation; not multilayer/doped cuprate calculation.','Neither state is a pressure-quenched metastable sample.','No Tc, barrier, lifetime, or superconductivity inference.','Hardware error bar is sampling only, not calibration/drift error.'])
 (OUT/'dimer_simulation.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='aer_counts'},indent=2));print(qasm2.dumps(qc))
if __name__=='__main__':main()
