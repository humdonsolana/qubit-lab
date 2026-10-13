"""Turn 15: add finite-T phase-stiffness gate to turn7's ideal-forward pair scale.
NOT material Tc predictions or bounds on all iron superconductors.
Single effectively isolated parabolic 2D sheet, electron density n=2x/a^2;
J_s=hbar^2*n_s/(4 m); T_BKT=pi J_s(T_BKT)/(2 k_B).
L_k=m/(n_s e^2); universal-jump L_k=pi hbar^2/(8 e^2 k_B T).
Finite-T depletion is phenomenological clean isotropic Yosida with prescribed
Delta(T)=Delta0*tanh(1.74*sqrt(Tpair/T-1)); R=2Delta0/(kB*Tpair).
Bare quasiparticle stiffness used, NO vortex fugacity/RG, disorder, anisotropy,
multiband geometric stiffness, Pearl-length cutoff or interlayer coupling.
Thus optimistic conditional screening only, not a rigorously renormalized Tc.
"""
from pathlib import Path
import csv,json
import numpy as np
from scipy.constants import hbar,k,e,m_e
# Shared SciPy spatial binary is invalid in this sandbox; no global package changes.
# NumPy Gauss-Legendre quadrature and scalar bisection avoid that dependency.
GX,GW=np.polynomial.legendre.leggauss(256)
GX=(GX+1)*30; GW=GW*30
def brentq(func,a,b,xtol=1e-11):
 fa=func(a); fb=func(b)
 assert fa*fb<0
 for _ in range(100):
  c=(a+b)/2; fc=func(c)
  if b-a<xtol:return c
  if fa*fc>0:a=c;fa=fc
  else:b=c
 return (a+b)/2
P=Path('outputs');P.mkdir(exist_ok=True)
KB=k/e*1000; A=3.905e-10 # analyst substrate-clamped in-plane reference

def sfrac(t,R):
 if t<=0:return 1.
 if t>=1:return 0.
 d=(R/2)*np.tanh(1.74*np.sqrt(1/t-1))/t
 val=1-.5*np.sum(GW/np.cosh(np.sqrt(GX*GX+d*d)/2)**2) if d<100 else 1.
 return float(max(0,min(1,val)))
def T0(x,m,f=1):return np.pi*hbar*hbar*(2*x/A**2)*f/(8*m*m_e*k)
def tbkt(tp,t0,R):
 return tp*brentq(lambda t:t-t0/tp*sfrac(t,R),1e-8,1-1e-9,xtol=1e-11)
def pairT(lam,w):return w/KB*lam/(2+3*lam)
def inductance(T):return np.pi*hbar*hbar/(8*e*e*k*T)
rows=[]
for x in [.08,.10,.12,.14,.16]:
 for mass in [1.,2.,3.,4.,5.,6.]:
  for f in [.5,.75,1.]:
   for R in [3.53,5.,6.35,8.]:
    for retain in [0.,.5,1.]:
     for w in [80.,100.]:
      lam=.2*(1+retain);tp=pairT(lam,w); t0=T0(x,mass,f);bkt=tbkt(tp,t0,R)
      rows.append(dict(x_e_per_Fe=x,mass_over_me=mass,condensate_fraction_zero=f,gap_ratio_R=R,second_interface_retention=retain,omega_meV=w,lambda_total=lam,pair_scale_K=tp,bare_BKT_ceiling_K=t0,conditional_clean_BKT_K=bkt,passes133=bkt>133))
with (P/'interface_stiffness_sweep.csv').open('w') as fh:
 dw=csv.DictWriter(fh,fieldnames=rows[0]);dw.writeheader();dw.writerows(rows)
# Reference table: deliberately optimistic retention=1, lambda=.4, omega=100meV.
tp=pairT(.4,100)
refs=[dict(mass_over_me=m,gap_ratio_R=R,T0_K=T0(.12,m),conditional_BKT_K=tbkt(tp,T0(.12,m),R)) for m in [1,2,3,4,6] for R in [3.53,6.35]]
thresholds=[]
for R in [3.53,5,6.35,8]:
 sf=sfrac(133/tp,R)
 thresholds.append(dict(R=R,pair_scale_K=tp,s_fraction_at133=sf,T0_required_K=133/sf,max_mass_over_me_if_x0p12_f1=T0(.12,1)*sf/133, max_Lk_zero_pH=inductance(133)*sf*1e12))
strain={
 'source':'Jia et al PNAS123 e2602209123, arXiv2607.27104; gaps measured, not Tc',
 'outer_gap_meV':[17.8,23.6],'inner_gap_meV':[11.5,16.0],
 'assumed_reference_pair_scale_K':65.,
 'outer_constant_gap_ratio_extrapolation_K':65*23.6/17.8,
 'inner_constant_gap_ratio_extrapolation_K':65*16/11.5,
 'outer_gap_needed_for133_same_ratio_meV':17.8*133/65,
 'ratio_required_for133_at23p6':2*23.6/(KB*133),
 'warning':'65K is from other FeSe/STO reports, not measured Tc of the strained STM spot. Scaling is sensitivity, not prediction.'}
summary={'scope':__doc__,'rows':len(rows),'passing_rows':sum(r['passes133'] for r in rows),'grid_not_probability_distribution':True,'best_case':max(rows,key=lambda r:r['conditional_clean_BKT_K']),'reference_x0p12_f1':refs,'necessary_thresholds_at133':thresholds,'universal_jump_inductance_pH_at133':inductance(133)*1e12,'universal_jump_inductance_pH_at300':inductance(300)*1e12,'strain_check':strain}
(P/'interface_stiffness_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
# Independent units and invariants.
assert abs(np.pi*hbar*hbar/(8*e*e*k*(m_e/((2*.12/A**2)*e**2)))-T0(.12,1))<1e-10
assert all(0<r['conditional_clean_BKT_K']<min(r['pair_scale_K'],r['bare_BKT_ceiling_K']) for r in rows)
assert sfrac(.001,3.53)>.999999 and sfrac(.99999,3.53)<.001
