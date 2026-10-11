"""Fixed electronic deformation potential softening audit; toy model, no material Tc.
One electron/spin on 2 sites. Relative oscillator only; constant center mode omitted.
H=-t(X0+X1)+U(1+Z0Z1)/2+w a†a+g/sqrt(2)(Z0+Z1)(a+a†).
Hold g^2*w=2 (fixed mass and displacement-force derivative), not g fixed.
Exact state preparation tests measurement, not a quantum eigensolver.
"""
import json,sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from qiskit import QuantumCircuit,transpile,qasm2
from qiskit.circuit.library import StatePreparation
from qiskit_aer import AerSimulator
I=np.eye(2); X=np.array([[0.,1],[1,0]]); Z=np.diag([1.,-1]); D=np.diag([1.,0,0,1.]); Q=np.kron(I,Z)+np.kron(Z,I)
KE=-(np.kron(I,X)+np.kron(X,I)); HE=KE+2*D

def exact(n,w):
 g=np.sqrt(2/w); a=np.diag(np.sqrt(np.arange(1,n)),1); N=a.T@a
 H=np.kron(np.eye(n),HE)+w*np.kron(N,np.eye(4))+g/np.sqrt(2)*np.kron(a+a.T,Q)
 es,vs=eigh(H); v=vs[:,0]; p=v*v
 return {'nph':n,'omega':w,'g':float(g),'E':float(es[0]),'D':float(v@np.kron(np.eye(n),D)@v),'kinetic':float(v@np.kron(np.eye(n),KE)@v),'nphonon':float(v@np.kron(N,np.eye(4))@v),'top_level_probability':float(p[-4:].sum())},v

def analyze(counts):
 N=sum(counts.values()); vals=[]; weights=[]
 for s,k in counts.items():
  ix=int(s.replace(' ',''),2); d=float((ix&1)==((ix>>1)&1)); n=ix>>2
  vals.append([d,n,d*n]); weights.append(k)
 vals=np.array(vals); weights=np.array(weights); mu=np.average(vals,axis=0,weights=weights); se=np.sqrt(np.sum(weights[:,None]*(vals-mu)**2,axis=0)/(N*(N-1)))
 return {'shots':N,'measurements':{k:{'mean':float(m),'shot_se':float(s)} for k,m,s in zip(['D','nphonon','D_nphonon'],mu,se)}}

def main(out):
 out=Path(out);out.mkdir(exist_ok=True,parents=True)
 conv=[exact(n,w)[0] for w in [2.,1.5,1.] for n in [2,4,8,16,32]]
 # Select moderate softening w=1.5; retain 4 oscillator states and document residual bias.
 val,v=exact(4,1.5); qc=QuantumCircuit(4,4);qc.append(StatePreparation(v),range(4));qc=transpile(qc,basis_gates=['u','cx'],optimization_level=3,seed_transpiler=12);qc.measure(range(4),range(4))
 sim=AerSimulator();cts=sim.run(transpile(qc,sim),shots=8192,seed_simulator=1212).result().get_counts()
 p=v*v; joint=sum(p[i]*float((i&1)==((i>>1)&1))*(i>>2) for i in range(16))
 result={'convergence':conv,'target':{**val,'D_nphonon':joint},'aer_counts':cts,'aer':analyze(cts),'circuit_depth':qc.depth(),'ops':dict(qc.count_ops()),'warning':'Exact classically prepared toy state. No material mapping, pairing temperature, quantum advantage, or discovery. Shot uncertainty omits device and truncation bias.'}
 (out/'simulation.json').write_text(json.dumps(result,indent=2)+'\n');(out/'circuit.qasm').write_text(qasm2.dumps(qc)+'\n');print(json.dumps(result,indent=2));print(qasm2.dumps(qc))
if __name__=='__main__':main(sys.argv[1])
