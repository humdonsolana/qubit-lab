"""Additional same-moment spectra retaining published low-band lambda fractions.
The paper gives 96.1% /98.2% below its pseudo-gap (near86meV for H7).
Here use a deliberately stricter illustrative split: both low modes <86meV,
third >100meV. Not a digitization of the actual spectrum or an anisotropic fit.
"""
import json,sys
from pathlib import Path
import numpy as np
from spectral_gate import PARENTS,fit_modes,tc_e
out=Path(sys.argv[1]);rows=[]
for name,(l,w,v,_) in PARENTS.items():
 q=.039 if 'H7' in name else .018
 for hi in [120.,150.,180.]:
  wl=np.exp((np.log(w)-q*np.log(hi))/(1-q));v2=np.sqrt((v*v-q*hi*hi)/(1-q))
  for p in [.3,.6,.85]:
   if v2<wl:continue
   m=fit_modes(wl,v2,p);c=l*np.array([(1-q)*p,(1-q)*(1-p),q]);m=np.r_[m,hi]
   if m[1]>86:continue
   assert abs(sum(c)-l)<1e-12
   assert abs(np.exp(sum(c*np.log(m))/l)-w)<1e-8
   assert abs(np.sqrt(sum(c*m*m)/l)-v)<1e-8
   rows.append({'parent':name,'modes_meV':m.tolist(),'lambda_components':c.tolist(),'Tc_iso_mu01_N256_K':tc_e(m,c,.1,256),'Tc_iso_mu01_N512_K':tc_e(m,c,.1,512)})
r={'scope':'Counterexamples to identification from moments and one cumulative weight, not material predictions. No anisotropy, ZPE, BKT or substrate included. mu convention in spectral_gate.py.','rows':rows}
(out/'constrained_spectra.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
