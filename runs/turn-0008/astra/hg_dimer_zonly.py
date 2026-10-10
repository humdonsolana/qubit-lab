"""4q follow-up avoids sampler tool's top64-count truncation. Z basis only.
12q original analysis retained as censored data, never postselected.
"""
import json,sys
from pathlib import Path
import numpy as np
from qiskit import QuantumCircuit,transpile,qasm2
from qiskit_aer import AerSimulator
from hg_dimer_benchmark import PARAMS,EXACT,exact_prep

def analyze(counts):
 n=sum(counts.values());rows=[];w=[]
 for bits,k in counts.items():
  b=bits.replace(' ','').zfill(4)[::-1];d0=float(b[0]==b[1]);d30=float(b[2]==b[3]);rows.append([d0,d30,d30-d0]);w.append(k)
 rows=np.array(rows);w=np.array(w);mean=np.average(rows,axis=0,weights=w)
 se=np.sqrt(np.sum(w[:,None]*(rows-mean)**2,axis=0)/(n*(n-1)))
 true=[EXACT[0]['D'],EXACT[1]['D'],EXACT[1]['D']-EXACT[0]['D']]
 return dict(shots=n,estimates={key:dict(mean=float(m),shot_se=float(s),exact=float(t),bias=float(m-t)) for key,m,s,t in zip(['D_0','D_30','delta_D'],mean,se,true)})

def main():
 out=Path(sys.argv[1]);out.mkdir(exist_ok=True,parents=True)
 qc=QuantumCircuit(4,4)
 for j,p in enumerate(PARAMS):qc.compose(exact_prep(p)[0],[2*j,2*j+1],inplace=True)
 qc.measure(range(4),range(4));qasm=qasm2.dumps(qc)
 sim=AerSimulator();c=sim.run(transpile(qc,sim),shots=8192,seed_simulator=8009).result().get_counts()
 r=dict(parameters=PARAMS,counts=c,aer=analyze(c),seed=8009,reason='At most16outcome bins so quantum_result top64 limit cannot censor counts.')
 (out/'zonly_simulation.json').write_text(json.dumps(r,indent=2)+'\n');(out/'hg_dimer_zonly.qasm').write_text(qasm+'\n');print(json.dumps(r,indent=2));print(qasm)
if __name__=='__main__':main()
