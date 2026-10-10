"""Number-conserving HVA for 2x2 open Hubbard plaquette, U/t=8, sectors N=2,3,4.
Qubit order: ring sites r=[0,1,3,2]; up spins on qubits 0..3 (ring order), down on 4..7.
Optimised with statevector; writes hva.json with QASM for estimator and expected energies.
Result (seed 1): N=2 converges, N=3/N=4 do not (see outputs/hva_summary.json) -> no QPU job."""
import numpy as np, json
from scipy.optimize import minimize
from qiskit import QuantumCircuit, qasm2
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.circuit.library import XXPlusYYGate

NQ=8; t=1.0; U=8.0
ring=[0,1,3,2]; pos={s:k for k,s in enumerate(ring)}
bonds=[(0,1),(1,3),(3,2),(2,0)]
qb=[(pos[i],pos[j]) for i,j in bonds]
def label(ops):
    s=['I']*NQ
    for q,o in ops.items(): s[NQ-1-q]=o
    return ''.join(s)
terms=[]
for (a,b) in qb:
    for s in (0,4):
        lo,hi=sorted((a+s,b+s)); zs={q:'Z' for q in range(lo+1,hi)}
        for p in 'XY':
            d=dict(zs); d[lo]=p; d[hi]=p; terms.append((label(d),-t/2))
for k in range(4):
    terms+=[(label({}),U/4),(label({k:'Z'}),-U/4),(label({4+k:'Z'}),-U/4),(label({k:'Z',4+k:'Z'}),U/4)]
H=SparsePauliOp.from_list(terms).simplify()
Hm=H.to_matrix()
def exact(N):
    idx=[k for k in range(256) if bin(k).count('1')==N]
    return float(np.linalg.eigvalsh(Hm[np.ix_(idx,idx)])[0])
E_ex={N:exact(N) for N in (2,3,4)}

def ansatz(N, params, L):
    qc=QuantumCircuit(NQ)
    occ={2:[0,5],3:[0,5,2],4:[0,5,2,7]}[N]
    for q in occ: qc.x(q)
    p=iter(params)
    for l in range(L):
        for (a,b) in qb:
            th=next(p)
            for s in (0,4):
                lo,hi=sorted((a+s,b+s))
                if hi-lo==1: qc.append(XXPlusYYGate(2*th),[lo,hi])
                else:  # ring-closing bond (qubits lo, lo+3): CX parity chain then XX+YY
                    qc.cx(lo,lo+1); qc.cx(lo+1,lo+2)
                    qc.append(XXPlusYYGate(2*th),[lo+2,hi])
                    qc.cx(lo+1,lo+2); qc.cx(lo,lo+1)
        for k in range(4):
            ph=next(p); qc.rzz(2*ph,k,4+k)
        for q in range(NQ): qc.rz(next(p),q)
    return qc
NP=lambda L: L*(4+4+8)
def energy(N,params,L):
    sv=Statevector(ansatz(N,params,L)); return float(np.real(sv.expectation_value(H)))
out={}
rng=np.random.default_rng(1)
for N in (2,3,4):
    best=None
    for L in (1,2):
        for trial in range(2):
            x0=rng.normal(0,0.3,NP(L))
            r=minimize(lambda x:energy(N,x,L),x0,method='L-BFGS-B',options=dict(maxiter=150))
            if best is None or r.fun<best[0]: best=(r.fun,L,r.x)
        print(N,L,"best so far",best[0],"exact",E_ex[N])
    E,L,x=best
    qc=ansatz(N,x,L)
    sv=Statevector(qc); probs=sv.probabilities_dict()
    bad=sum(p for b,p in probs.items() if b.count('1')!=N)
    out[N]=dict(E_var=E,E_exact=E_ex[N],L=L,params=x.tolist(),leak=bad,depth=qc.depth(),qasm=qasm2.dumps(qc))
    print(f"N={N}: Evar={E:.4f} Eexact={E_ex[N]:.4f} L={L} depth={qc.depth()} leak={bad:.1e}")
Dvar=out[4]['E_var']+out[2]['E_var']-2*out[3]['E_var']
Dex=E_ex[4]+E_ex[2]-2*E_ex[3]
print("Delta_pb variational",Dvar,"exact",Dex)
json.dump(dict(sectors=out,Dpb_var=Dvar,Dpb_exact=Dex,H_terms=[(l,float(c.real)) for l,c in zip(H.paulis.to_labels(),H.coeffs)]),open('hva.json','w'),indent=1)
