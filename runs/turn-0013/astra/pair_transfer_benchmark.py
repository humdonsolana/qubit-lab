"""Exactly prepared one-pair/two-band plus relative-phonon toy benchmark.
H = delta Z - J X + omega a†a + g Z(a+a†).
The electronic basis is one pair in band sigma or pi; X measures coherent pair
transfer, NOT superconducting order or Tc. No material-specific fit. Frequencies
and couplings are in arbitrary units. Exact classical state prep, no advantage.
"""
import json,sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from qiskit import QuantumCircuit,transpile,qasm2
from qiskit.circuit.library import StatePreparation
from qiskit_aer import AerSimulator
X=np.array([[0.,1.],[1.,0.]]);Z=np.diag([1.,-1.]);I=np.eye(2)
def solve(n,g):
 a=np.diag(np.sqrt(np.arange(1,n)),1);N=a.T@a
 H=np.kron(np.eye(n),.3*Z-X)+np.kron(N,I)+g*np.kron(a+a.T,Z)
 e,v=eigh(H);v=v[:,0]
 return {'nph':n,'g':g,'energy':float(e[0]),'transfer_X':float(v@np.kron(np.eye(n),X)@v),'nphonon':float(v@np.kron(N,I)@v),'X_nphonon':float(v@np.kron(N,X)@v),'top_probability':float(sum(v[-2:]**2))},v
def analyze(counts):
 n=sum(counts.values());vals=[];w=[]
 for bits,k in counts.items():
  ix=int(bits.replace(' ',''),2);x=1-2*(ix&1);p=ix>>1
  vals.append([x,p,x*p]);w.append(k)
 vals=np.array(vals);w=np.array(w);m=np.average(vals,weights=w,axis=0)
 se=np.sqrt(np.sum(w[:,None]*(vals-m)**2,axis=0)/(n*(n-1)))
 return {'shots':n,'moments':{key:{'mean':float(a),'shot_se':float(b)} for key,a,b in zip(['transfer_X','nphonon','X_nphonon'],m,se)}}
def main(out):
 out=Path(out);out.mkdir(exist_ok=True,parents=True)
 conv=[solve(n,g)[0] for g in [0.,.6,1.] for n in [2,4,8,16,32]]
 target,v=solve(4,.6);q=QuantumCircuit(3,3);q.append(StatePreparation(v),range(3));q.h(0)
 q=transpile(q,basis_gates=['u','cx'],optimization_level=3,seed_transpiler=13);q.measure(range(3),range(3))
 sim=AerSimulator();counts=sim.run(transpile(q,sim),shots=8192,seed_simulator=13).result().get_counts()
 data={'hamiltonian':'0.3 Z - X + n + 0.6 Z(a+a†)','target':target,'convergence':conv,'aer_counts':counts,'aer':analyze(counts),'depth':q.depth(),'ops':dict(q.count_ops()),'warning':'One-pair finite toy: X is transfer coherence, not order or Tc. Shot SE excludes state-prep device bias and phonon truncation.'}
 (out/'pair_transfer_simulation.json').write_text(json.dumps(data,indent=2)+'\n');(out/'pair_transfer.qasm').write_text(qasm2.dumps(q)+'\n');print(json.dumps(data,indent=2));print(qasm2.dumps(q))
if __name__=='__main__':main(sys.argv[1])
