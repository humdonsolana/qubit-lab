"""Four-spin bilayer exchange readout benchmark; NOT a Tc/pairing calculation.
Sites 0,1 upper layer and 2,3 lower; rungs (0,2),(1,3), legs (0,1),(2,3).
Jleg=1; illustrative Jperp=2 (not fitted to any material).
Exact state prepared three times for XX,YY,ZZ readout. No mitigation/postselection.
"""
import json,sys
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from qiskit import QuantumCircuit,transpile,qasm2
from qiskit.circuit.library import StatePreparation
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
I=np.eye(2); P=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1.,-1.])]
BONDS=[(0,2),(1,3),(0,1),(2,3)]
def op(i,j,p):
 a=np.array([[1.]])
 for k in reversed(range(4)):a=np.kron(a,p if k in (i,j) else I)
 return a
B=[sum(op(i,j,p) for p in P)/4 for i,j in BONDS]
def exact(r):
 h=r*(B[0]+B[1])+B[2]+B[3];e,v=eigh(h);s=v[:,0];cs=[float(np.vdot(s,b@s).real) for b in B]
 return {'Jperp_over_Jleg':r,'energy':float(e[0]),'gap':float(e[1]-e[0]),'bond_correlations':cs,'rung_singlet':.25-(cs[0]+cs[1])/2,'leg_singlet':.25-(cs[2]+cs[3])/2},s

def analyze(counts):
 n=sum(counts.values());vs=[];ws=[]
 for bit,k in counts.items():
  z=[1-2*int(x) for x in bit.replace(' ','').zfill(12)[::-1]]
  c=[sum(z[4*b+i]*z[4*b+j] for b in range(3))/4 for i,j in BONDS]
  # Per-shot estimators combine independent basis blocks; include covariance.
  vs.append(c+[.25-(c[0]+c[1])/2,.25-(c[2]+c[3])/2,2*(c[0]+c[1])+c[2]+c[3]])
  ws.append(k)
 v=np.array(vs);w=np.array(ws);m=np.average(v,axis=0,weights=w);se=np.sqrt(np.sum(w[:,None]*(v-m)**2,axis=0)/(n*(n-1)))
 return {'shots':n,'estimates':{name:{'mean':float(a),'shot_se':float(b)} for name,a,b in zip(['rung02','rung13','leg01','leg23','rung_singlet','leg_singlet','energy'],m,se)}}
def main():
 out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
 target,s=exact(2);prep=QuantumCircuit(4);prep.append(StatePreparation(s),range(4));prep=transpile(prep,basis_gates=['u','cx'],optimization_level=3,seed_transpiler=10)
 fidelity=abs(np.vdot(s,Statevector.from_instruction(prep).data))**2
 qc=QuantumCircuit(12,12)
 for b in range(3):
  qc.compose(prep,qubits=range(4*b,4*b+4),inplace=True)
  for i in range(4*b,4*b+4):
   if b==0:qc.h(i)
   elif b==1:qc.sdg(i);qc.h(i)
 qc=transpile(qc,basis_gates=['u','cx'],optimization_level=3,seed_transpiler=10);qc.measure(range(12),range(12))
 counts=AerSimulator().run(qc,shots=4096,seed_simulator=1010).result().get_counts()
 result={'model':'four-spin Heisenberg bilayer, no charge or itinerant orbitals','target':target,'fidelity':float(fidelity),'scan':[exact(r)[0] for r in [0,.25,.5,1,2,4,8]],'aer':analyze(counts),'ops':dict(qc.count_ops()),'depth':qc.depth(),'warning':'Prepared exact small model. No quantum advantage, finite-T transition, electronic pairing amplitude or material calibration.'}
 (out/'spin_simulation.json').write_text(json.dumps(result,indent=2)+'\n');(out/'spin.qasm').write_text(qasm2.dumps(qc)+'\n');print(json.dumps(result,indent=2));print(qasm2.dumps(qc))
if __name__=='__main__':main()
