"""Allen-Dynes sensitivity, NOT an independent Mg2IrH6 Tc prediction.
Sanna et al DOI10.1038/s41524-024-01214-9 table1: lambda2.1, wlog50meV.
We don't know w2: maximize the AD shape factor over r=sqrt(<w²>)/wlog>=1.
f2=1+(r-1)lambda²/(lambda²+c²r²), c=1.82(1+6.3mu*).
Derivative gives r_max=1+sqrt(1+(lambda/c)^2). Thus Tc_AD in[T0,T0*f2max].
This bounds an approximate FORMULA, not the actual Tc. Energy-dependent DOS
and Coulomb kernels in the primary work cannot be reproduced by this formula.
"""
import json,sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar,brentq
KB=8.617333262145e-5
L=2.1;WK=.05/KB

def bounds(mu):
 c=1.82*(1+6.3*mu);r=1+np.sqrt(1+(L/c)**2)
 f2=lambda r:1+(r-1)*L**2/(L**2+c*c*r*r)
 f1=(1+(L/(2.46*(1+3.8*mu)))**1.5)**(1/3)
 t0=WK/1.2*np.exp(-1.04*(1+L)/(L-mu*(1+.62*L)))*f1
 opt=minimize_scalar(lambda x:-f2(x),bounds=(1,20),method='bounded')
 assert abs(f2(r)+opt.fun)<1e-10
 return {'mu_star':mu,'shape_ratio_at_maximum':float(r),'Tc_AD_min_K':float(t0),'Tc_AD_max_K':float(t0*f2(r)),'f2_max':float(f2(r))}
rows=[bounds(m) for m in [0.1,.16,.25,.3,.4]]
r={'inputs':{'lambda':L,'omega_log_meV':50,'omega_log_K':WK},'sensitivity':rows,'mu_star_at_upper_formula_bound_105K':brentq(lambda m:bounds(m)['Tc_AD_max_K']-105,.001,.3),'primary_methods_Tc_K':{'Sanna_isotropic_SCDFT':65.9,'Sanna_anisotropic_SCDFT':71,'Sanna_isotropic_Eliashberg':77,'Hansen_dense_grid_range':[90,120],'existing_C0001_single_number':105},'verdict':'105K is a selected-method conditional forecast, not a consensus. Include material-dependent Coulomb/DOS uncertainty in addition to phase-access challenge. Do not average methods or equate bare mu=0.58 to mu_star.','limitation':'AD formula envelope only, not a rigorous superconducting Tc bound.'}
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True);(out/'coulomb_sensitivity.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
