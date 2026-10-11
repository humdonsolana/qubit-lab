"""Exact two-electron Holstein relative-mode dimer; not a material or Tc model.
Electronic bits q0,q1 give up/down electron site; q2 is truncated phonon.
H=-t(X0+X1)+U(1+Z0Z1)/2 + omega a†a + g/sqrt(2)(Z0+Z1)(a+a†).
Center-of-mass oscillator is removed at fixed N=2 (constant shift omitted).
We prepare exact ground state at nph=2; convergence checked against nph=4..32.
No claim that two phonon levels suffice for a real hydride.
"""
import json,sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from qiskit import QuantumCircuit,transpile,qasm2
from qiskit.circuit.library import StatePreparation
from qiskit_aer import AerSimulator
T,U,W,G=1.,2.,2.,1.
I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1.,-1.])
D=np.diag([1.,0,0,1.]);Q=np.kron(I,Z)+np.kron(Z,I)
HE=-T*(np.kron(I,X)+np.kron(X,I))+U*D

def exact(n):
 a=np.diag(np.sqrt(np.arange(1,n)),1);N=a.T@a
 h=np.kron(np.eye(n),HE)+W*np.kron(N,np.eye(4))+G/np.sqrt(2)*np.kron(a+a.T,Q)
 ev,v=eigh(h);s=v[:,0];prob=abs(s)**2
 vals={'nph':n,'E0':float(ev[0]),'gap':float(ev[1]-ev[0]),'D':float(s@np.kron(np.eye(n),D)@s),'nphonon':float(s@np.kron(N,np.eye(4))@s),'top_phonon_probability':float(prob[-4:].sum())}
 return vals,s

def analyze(counts):
 n=sum(counts.values());v=[];w=[]
 for b,k in counts.items():
  b=b.replace(' ','').zfill(3)[::-1]
  d=float(b[0]==b[1]);p=float(b[2]=='1');v.append([d,p,d*p]);w.append(k)
 v=np.array(v);w=np.array(w);m=np.average(v,axis=0,weights=w);se=np.sqrt(np.sum(w[:,None]*(v-m)**2,axis=0)/(n*(n-1)))
 return {'shots':n,'estimates':{k:{'mean':float(x),'shot_se':float(s)} for k,x,s in zip(['double_occupancy','phonon_occupation','joint_D_phonon'],m,se)}}

def main():
 out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
 rows=[exact(n)[0] for n in [2,4,8,16,32]];val,s=exact(2)
 qc=QuantumCircuit(3,3);qc.append(StatePreparation(s),range(3));qc=transpile(qc,basis_gates=['u','cx'],optimization_level=3,seed_transpiler=9);qc.measure(range(3),range(3))
 sim=AerSimulator();counts=sim.run(transpile(qc,sim),shots=8192,seed_simulator=9009).result().get_counts()
 p=abs(s)**2;joint=sum(p[k] for k in [4,7])
 result={'model':'relative-mode Holstein dimer, fixed one electron of each spin','parameters':{'t':T,'U':U,'omega':W,'g':G},'convergence':rows,'exact_hardware_targets':{'double_occupancy':val['D'],'phonon_occupation':val['nphonon'],'joint_D_phonon':float(joint)},'aer_counts':counts,'aer_analysis':analyze(counts),'circuit_depth':qc.depth(),'circuit_ops':dict(qc.count_ops()),'warning':'Nph=2 state preparation benchmark only. Compare against convergence before any physical inference. No hydride mapping or Tc prediction.'}
 (out/'holstein_simulation.json').write_text(json.dumps(result,indent=2)+'\n');(out/'holstein.qasm').write_text(qasm2.dumps(qc)+'\n');print(json.dumps(result,indent=2));print(qasm2.dumps(qc))
if __name__=='__main__':main()
