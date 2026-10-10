"""Pair-binding Delta_pb(U) for the open 2x2 Hubbard square and for the periodic 2x2 cluster
(doubled bonds => t_eff = 2t), exact diagonalisation. Output is in outputs/scan_pbc.txt."""
import numpy as np
from qiskit.quantum_info import SparsePauliOp
NQ=8;NS=4
def label(ops):
    s=['I']*NQ
    for q,o in ops.items(): s[NQ-1-q]=o
    return ''.join(s)
def H(t,U,bonds):
    terms=[]
    for (i,j) in bonds:
        for s in (0,4):
            a,b=sorted((i+s,j+s)); zs={q:'Z' for q in range(a+1,b)}
            for p in 'XY':
                d=dict(zs); d[a]=p; d[b]=p; terms.append((label(d),-t/2))
    for i in range(NS):
        terms+= [(label({}),U/4),(label({i:'Z'}),-U/4),(label({4+i:'Z'}),-U/4),(label({i:'Z',4+i:'Z'}),U/4)]
    return SparsePauliOp.from_list(terms).simplify().to_matrix()
def E0s(Hm):
    out={}
    for N in (2,3,4):
        idx=[k for k in range(256) if bin(k).count('1')==N]
        out[N]=float(np.linalg.eigvalsh(Hm[np.ix_(idx,idx)])[0])
    return out
sq=[(0,1),(1,3),(3,2),(2,0)]
for name,bonds in [('open square t',sq),('PBC 2x2 (doubled bonds, t_eff=2t)',sq+sq)]:
    print(name)
    for U in [1,2,3,4,5,6,8,10,12,16,20]:
        e=E0s(H(1.0,U,bonds)); print(f"  U={U:>3} E2={e[2]:.4f} E3={e[3]:.4f} E4={e[4]:.4f} Dpb={e[4]+e[2]-2*e[3]:+.4f}")
