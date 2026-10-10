"""Conditional ideal-forward phonon feasibility gate; NOT a material Tc predictor.
Reproduce Rademaker et al arXiv1507.03967v2 analytic approximation and
its finite-temperature Matsubara sum. Check the full frequency-dependent
LINEARIZED perfect-forward kernel with Z=1, chi=0, mu*=0. This is not a
self-consistent finite-q Eliashberg calculation. lambda here follows the
paper's weak-coupling g0^2/Omega^2 convention, not arbitrary EPC lambda.
Independent-interface additivity and 80-meV sensitivity are ASSUMPTIONS.
"""
from pathlib import Path
import sys,json,csv
import numpy as np
from scipy.optimize import brentq
from scipy.linalg import eigh
KB=0.08617333262145 # meV/K, exact SI kB/e converted
OUT=Path(sys.argv[1] if len(sys.argv)>1 else 'outputs');OUT.mkdir(exist_ok=True,parents=True)

def tc_approx(lam,omega):return omega/KB*lam/(2+3*lam)
def required_lam(T,omega):
    x=KB*T
    return 2*x/(omega-3*x) if omega>3*x else None

def scalar_rhs(tau,lam):
    r=np.exp(-1/tau)
    return lam/(2*tau)*((1+4*r+r*r)/(1+2*r+r*r)-3*tau*(1-r)/(1+r))
def scalar_root(lam):return brentq(lambda tau:scalar_rhs(tau,lam)-1,1e-5,1.,xtol=1e-13)
def direct_sum(tau,lam,n=10000):
    w=(2*np.arange(n)+1)*np.pi*tau
    return 4*lam*tau*np.sum(1/(w*w*(1+w*w)**2))
def eigenvalue(tau,lam,n):
    w=(2*np.arange(n)+1)*np.pi*tau
    K=2*lam*tau*(1/(1+(w[:,None]-w[None,:])**2)+1/(1+(w[:,None]+w[None,:])**2))/(w[:,None]*w[None,:])
    return eigh(K,eigvals_only=True,subset_by_index=[n-1,n-1])[0]
def kernel_root(lam,n=128):return brentq(lambda tau:eigenvalue(tau,lam,n)-1,1e-4,1.,xtol=1e-12)

rows=[];diagnostics=[]
for lam in [.15,.175,.20,.30,.35,.40]:
    a=scalar_root(lam); b=kernel_root(lam,128);c=kernel_root(lam,256)
    diagnostics.append({'lambda_total':lam,'scalar_tau':a,'kernel_tau_N128':b,'kernel_tau_N256':c,'kernel_convergence_K_at100meV':abs(b-c)*100/KB,'scalar_vs_direct_sum_error':abs(direct_sum(a,lam)-1)})
    for omega in [80.,100.]:
        rows.append({'lambda_total':lam,'omega_meV':omega,'analytic_K':tc_approx(lam,omega),'finite_scalar_ansatz_K':a*omega/KB,'linear_kernel_Z1_K':c*omega/KB})
with (OUT/'forward_gate.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
thresholds=[{'target_K':T,'omega_meV':w,'lambda_required_analytic':required_lam(T,w)} for T in [133.,151.,300.] for w in [80.,100.]]
need=required_lam(133,100);best=tc_approx(.4,100)
summary={'kind':'Feasibility scenarios only; not a Tc forecast or universal bound','kb_meV_per_K':KB,'source_lambda_per_interface_range':[.15,.2],'source_omega_meV':100.,'omega80_status':'analyst sensitivity, not a fitted measurement','thresholds':thresholds,'two_identical_interfaces':{'assumed_total_lambda':[.3,.4],'analytic_T_K_100meV':[tc_approx(.3,100),best],'additional_interface_retention_needed_if_base_lambda_0p2':need/.2-1,'max_fractional_T_reduction_before_falling_below133_at_best_case':1-133/best,'min_omega_meV_to_reach133_at_lambda0p4':133*KB*(2+3*.4)/.4},'diagnostics':diagnostics,'checks':{'inverse_roundtrip_max_error_K':max(abs(tc_approx(d['lambda_required_analytic'],d['omega_meV'])-d['target_K']) for d in thresholds if d['lambda_required_analytic'] is not None),'matsubara_sum_max_error':max(d['scalar_vs_direct_sum_error'] for d in diagnostics),'frequency_convergence_max_K':max(d['kernel_convergence_K_at100meV'] for d in diagnostics)}}
assert summary['checks']['inverse_roundtrip_max_error_K']<1e-10
assert summary['checks']['matsubara_sum_max_error']<1e-9
assert summary['checks']['frequency_convergence_max_K']<1e-5
(OUT/'forward_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print((OUT/'forward_gate.csv').read_text());print(json.dumps(summary,indent=2))
