"""Independent occupation-basis check of reduced dimer and audit arithmetic."""
import json,sys,math
from pathlib import Path
import numpy as np
from scipy.constants import Boltzmann,electron_volt
from hg_dimer_benchmark import PARAMS,EXACT
out=Path(sys.argv[1]);out.mkdir(exist_ok=True,parents=True)
# Four fermionic spin orbitals ordered up0,up1,down0,down1.
a=[]
for mode in range(4):
 A=np.zeros((16,16))
 for n in range(16):
  if (n>>mode)&1:A[n^(1<<mode),n]=(-1)**((n&((1<<mode)-1)).bit_count())
 a.append(A)
n=[A.T@A for A in a];nsite=[n[0]+n[2],n[1]+n[3]]
D=n[0]@n[2]+n[1]@n[3]
Pair=a[0].T@a[2].T@a[3]@a[1];Pair=Pair+Pair.T
# positions encode q0=up site and q1=down site; computational order00,01,10,11
basis=[(1<<(b&1))+(1<<(2+(b>>1))) for b in range(4)]
reports=[]
for p,ex in zip(PARAMS,EXACT):
 H=p['U_eV']*D+p['V_eV']*nsite[0]@nsite[1]
 for i,j in [(0,1),(2,3)]:H-=p['t_eV']*(a[i].T@a[j]+a[j].T@a[i])
 h=H[np.ix_(basis,basis)];e,v=np.linalg.eigh(h);psi=v[:,0]
 d=psi@D[np.ix_(basis,basis)]@psi;pair=psi@Pair[np.ix_(basis,basis)]@psi
 assert abs(e[0]-ex['E_eV'])<1e-12 and abs(d-ex['D'])<1e-12 and abs(pair-ex['P_pairhop'])<1e-12
 reports.append(dict(P_GPa=p['P_GPa'],full_fock_sector_E_eV=float(e[0]),D=float(d),P_pairhop=float(pair)))
# Independent unit conversion and threshold equality.
f=math.pi*1.9e-8/(42.5/1e4)**3
E=(Boltzmann/electron_volt)*math.log(3*24*60)/(1/77-1/170)
assert abs(f-.7775649637217968)<1e-14
assert abs(E-.10153306184365464)<1e-14
result=dict(full_fermion_basis_checks=reports,demagnetization_fraction=f,one_minute170_vs_three_days77_equal_dose_barrier_eV=E,all_pass=True)
(out/'independent_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
