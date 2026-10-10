"""Independent Fock-space/sign and Matsubara folding checks (numpy/scipy)."""
import sys,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh
OUT=Path(sys.argv[1] if len(sys.argv)>1 else 'outputs');OUT.mkdir(parents=True,exist_ok=True)
# Four canonical orbitals [site0up,site1up,site0down,site1down].
c=[]
for k in range(4):
    a=np.zeros((16,16))
    for b in range(16):
        if b>>k&1:a[b^(1<<k),b]=(-1)**((b&((1<<k)-1)).bit_count())
    c.append(a)
n=[a.T@a for a in c];H=np.zeros((16,16))
for i,j in [(0,1),(2,3)]:H-=c[i].T@c[j]+c[j].T@c[i]
D=n[0]@n[2]+n[1]@n[3];H+=4*D
b0=c[2]@c[0];b1=c[3]@c[1];P=b0.T@b1+b1.T@b0
energies={}
for N in [0,1,2]:
    inds=[b for b in range(16) if b.bit_count()==N]
    es,vs=np.linalg.eigh(H[np.ix_(inds,inds)]);energies[str(N)]=float(es[0])
    if N==2:
        v=np.zeros(16);v[inds]=vs[:,0];d=float(v@D@v);p=float(v@P@v)
assert abs(d-(1-1/np.sqrt(2))/2)<1e-13 and abs(p-d)<1e-13
assert abs(energies['2']-(2-np.sqrt(8)))<1e-13
# Validate positive-frequency folding without importing interface_gate.
N=64;lam=.35;tau=.12;wp=(2*np.arange(N)+1)*np.pi*tau
wf=np.concatenate((-wp[::-1],wp))
full=2*lam*tau/(1+(wf[:,None]-wf[None,:])**2)/np.abs(wf[:,None]*wf[None,:])
fold=2*lam*tau*(1/(1+(wp[:,None]-wp[None,:])**2)+1/(1+(wp[:,None]+wp[None,:])**2))/(wp[:,None]*wp[None,:])
e=float(abs(eigvalsh(full)[-1]-eigvalsh(fold)[-1]));assert e<1e-12
r={'full_Fock_energies_t':energies,'full_Fock_double_occupancy':d,'full_Fock_pair_hopping':p,'pair_binding_E2_plus_E0_minus_2E1_t':energies['2']+energies['0']-2*energies['1'],'pair_binding_interpretation':'positive: no energetic binding by this vacuum two-electron diagnostic; not a thermodynamic limit conclusion','folded_vs_full_Matsubara_eigenvalue_abs_error':e,'status':'all assertions passed'}
(OUT/'independent_checks.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
