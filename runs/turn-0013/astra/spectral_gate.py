"""Reproduce Chen et al arXiv:2603.00648v1 Table1, then stress-test spectral inference.
Inputs are published prior work, not materials invented here. Tc estimates below are
isotropic surrogate spectra, NOT reproductions of anisotropic EPW Tc (87 K).
Einstein spectra exactly match lambda, wlog and sqrt<w²>; their free low-mode
lambda weight demonstrates that moments do not identify the full a²F spectrum.
Fixed-Hopfield rescaling assumes all w -> s*w and all lambda -> lambda/s².
No stability statement follows from this rescaling; s -> 0 is not a material.
"""
import json,sys
from pathlib import Path
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.linalg import eigh
from labphys.tc import allen_dynes
KB_MEV=.08617333262;MEV_K=1/KB_MEV
PARENTS={'H7_B2C6':(3.33,13.88,41.16,47.9),'H8_B2C6':(2.44,25.28,43.12,63.5)}
def ad(l,w,v,mu):return allen_dynes(l,w*MEV_K,v*MEV_K,mu)
def fit_modes(wlog,w2,p):
 ratio=w2/wlog
 fun=lambda x:p*x*x+(1-p)*x**(-2*p/(1-p))-ratio*ratio
 x=brentq(fun,1e-5,1.)
 return np.array([wlog*x,wlog*x**(-p/(1-p))])
def eliashberg_eigen(T,modes,couplings,mu,N=256):
 # Standard positive-frequency linearized isotropic imaginary-axis kernel.
 # Infinite-sum normal-state Z evaluated analytically for Einstein spectra.
 # Coulomb window 10*max phonon frequency, symmetric external/internal cutoff.
 d=np.arange(2*N);nu=2*np.pi*KB_MEV*T*d
 L=np.sum(couplings[:,None]*modes[:,None]**2/(modes[:,None]**2+nu[None,:]**2),axis=0)
 n=np.arange(N);omega=np.pi*KB_MEV*T*(2*n+1)
 Z=1+(2*np.cumsum(L[:N])-L[0])/(2*n+1)
 theta=(omega<10*max(modes)).astype(float)
 A=L[np.abs(n[:,None]-n[None,:])]+L[n[:,None]+n[None,:]+1]-2*mu*theta[:,None]*theta[None,:]
 den=np.sqrt(omega*Z);A*=np.pi*KB_MEV*T/np.outer(den,den)
 return eigh(A,subset_by_index=[N-1,N-1],eigvals_only=True,check_finite=False)[0]
def tc_e(m,c,mu,N=256):
 return brentq(lambda T:eliashberg_eigen(T,m,c,mu,N)-1,5,250,xtol=.02)
def main(out):
 rows=[];surrogates=[]
 for name,(l,w,v,tpub) in PARENTS.items():
  for mu in [.1,.13]:
   opt=minimize_scalar(lambda logs:-ad(l/np.exp(logs)**2,w*np.exp(logs),v*np.exp(logs),mu),bounds=(np.log(.03),np.log(3)),method='bounded')
   s=np.exp(opt.x)
   factor=brentq(lambda f:ad(l*f,w,v,mu)-133,1,50)
   rows.append({'parent':name,'mu':mu,'lambda':l,'wlog_meV':w,'w2_meV':v,'lambda_w2_squared_meV2':l*v*v,'published_MAD_mu01_K':tpub,'recomputed_AD_K':ad(l,w,v,mu),'fixed_hopfield_scan_s_range':[.03,3],'best_scale':s,'best_AD_K':-opt.fun,'lambda_at_best':l/s**2,'coupling_multiplier_for_133_at_fixed_frequencies':factor,'lambda_required':l*factor})
  for p in [.3,.6,.85]:
   modes=fit_modes(w,v,p);c=l*np.array([p,1-p])
   tc=tc_e(modes,c,.1,256)
   surrogates.append({'parent':name,'low_mode_lambda_fraction':p,'mode_meV':modes.tolist(),'lambda_components':c.tolist(),'moments_verified':{'lambda':sum(c),'wlog':float(np.exp(sum(c*np.log(modes))/sum(c))),'w2':float(np.sqrt(sum(c*modes**2)/sum(c)))},'Tc_iso_mu01_N256_K':tc,'Tc_iso_mu01_N512_K':tc_e(modes,c,.1,512)})
 result={'input_source':'https://arxiv.org/html/2603.00648v1 Table1 (preprint values; final CPL43 060709 reports H7 91K instead of87)','warning':'Parametric isotropic spectral audit, not a new DFT/material Tc; no calibrated anisotropic uplift factor; cutoff mu convention explicit in code. Uniform softening optimum far beyond stable/controlled Migdal regime is diagnostic only.','moment_and_hopfield_gate':rows,'same_moment_two_Einstein_surrogates':surrogates}
 out=Path(out);out.mkdir(exist_ok=True,parents=True);(out/'spectral_gate.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main(sys.argv[1])
