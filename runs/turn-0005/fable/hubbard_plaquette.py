"""2x2 Hubbard plaquette (open square, 4 bonds), U/t=8: exact pair-binding energy
Delta_pb = E0(N=4) + E0(N=2) - 2 E0(N=3) by exact diagonalisation of the Jordan-Wigner
qubit Hamiltonian (8 qubits; site i spin-up -> qubit i, spin-down -> qubit 4+i), plus a U/t scan.
Run in /tmp/f5 (turn folder not shell-writable); output exact.json copied verbatim to outputs/."""
import numpy as np, json
from qiskit.quantum_info import SparsePauliOp

NS=4; NQ=8; t=1.0; U=8.0
bonds=[(0,1),(1,3),(3,2),(2,0)]  # square 0-1 / 2-3
def label(ops):  # qiskit label is little-endian (q0 rightmost)
    s=['I']*NQ
    for q,o in ops.items(): s[NQ-1-q]=o
    return ''.join(s)
terms=[]
for (i,j) in bonds:
    for s in (0,4):
        a,b=sorted((i+s,j+s))
        zs={q:'Z' for q in range(a+1,b)}
        for p in 'XY':
            d=dict(zs); d[a]=p; d[b]=p
            terms.append((label(d),-t/2))
for i in range(NS):
    # U n_up n_dn = U/4 (1 - Z_up)(1 - Z_dn)
    terms.append((label({}),U/4)); terms.append((label({i:'Z'}),-U/4)); terms.append((label({4+i:'Z'}),-U/4)); terms.append((label({i:'Z',4+i:'Z'}),U/4))
H=SparsePauliOp.from_list(terms).simplify()
Hm=H.to_matrix()
def n_of(idx): return bin(idx).count('1')
E0={}
for N in (2,3,4):
    idx=[k for k in range(2**NQ) if n_of(k)==N]
    E0[N]=float(np.linalg.eigvalsh(Hm[np.ix_(idx,idx)])[0])
D=E0[4]+E0[2]-2*E0[3]
print("exact E0:",E0," pair binding Delta_pb =",D)
scan=[]
for Uu in [2,4,6,8,10,12,16,20]:
    Hs=SparsePauliOp.from_list([(l,c) for (l,c) in terms if abs(c)==t/2]+[(l,c*Uu/U) for (l,c) in terms if abs(c)==U/4]).simplify().to_matrix()
    e={}
    for N in (2,3,4):
        idx=[k for k in range(2**NQ) if n_of(k)==N]
        e[N]=float(np.linalg.eigvalsh(Hs[np.ix_(idx,idx)])[0])
    scan.append(dict(U=Uu,E2=e[2],E3=e[3],E4=e[4],Dpb=e[4]+e[2]-2*e[3]))
    print(scan[-1])
json.dump(dict(exact=E0,Dpb=D,scan=scan,bonds=bonds,U=U,t=t),open('exact.json','w'),indent=1)
