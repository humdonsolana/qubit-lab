#!/usr/bin/env python3
"""Conditional phase-access gates, NOT material kinetics or a Tc prediction.
Run from this directory: python phase_access_gates.py
Inputs and derivations: README.md, source_inputs.json.
"""
from pathlib import Path
import json, math, platform
import numpy as np
import pandas as pd
import scipy
from scipy.optimize import brentq
from scipy.integrate import solve_ivp

OUT = Path(__file__).resolve().parent / 'outputs'
OUT.mkdir(exist_ok=True)
KB = 8.617333262145e-5  # eV/K, CODATA exact constants ratio

def peak_fraction(r):
    """Initial all H7; k76=1 time units, k65=r, irreversible first order."""
    if abs(r-1.) < 1e-10:
        return math.exp(-1.)
    return math.exp(r * math.log(r) / (1-r))

def peak_time(r):
    return 1. if abs(r-1.) < 1e-10 else math.log(r)/(r-1.)

def fractions(tau, r):
    a = np.exp(-tau)
    if abs(r-1.) < 1e-10:
        b = tau * a
    else:
        b = (np.exp(-r*tau)-a)/(1-r)
    return a, b, 1-a-b

# Yield gate: bracket log r, not r, for precision at high target yields.
rows = []
for target in [0.5, 0.8, 0.9, 0.95, 0.99, 0.999]:
    log_r = brentq(lambda z: peak_fraction(math.exp(z))-target, -30, 5, xtol=1e-13)
    r = math.exp(log_r)
    assert abs(peak_fraction(r)-target) < 1e-11
    tau = peak_time(r)
    a,b,c = fractions(tau,r)
    assert abs(b-target)<1e-11 and abs(a+b+c-1)<1e-14
    for T in [100, 200, 300, 500, 800]:
        # r=(A65/A76)*exp(-(E65-E76)/kT)
        for prefactor_ratio in [0.01, 1., 100.]:
            rows.append(dict(target_peak_H6=target, max_k65_over_k76=r,
                min_k76_over_k65=1/r, optimum_k76_t=tau, T_K=T,
                A65_over_A76=prefactor_ratio,
                min_E65_minus_E76_eV=KB*T*(math.log(prefactor_ratio)-log_r)))
pd.DataFrame(rows).to_csv(OUT/'sequential_yield_thresholds.csv', index=False)

# Numerical independent ODE checks, including equal-rate removable singularity.
errors = []
for r in [1e-4, .001, .03, .1, 1., 3., 100.]:
    t = peak_time(r)
    sol = solve_ivp(lambda tt,y: [-y[0],y[0]-r*y[1],r*y[1]], (0,t),
                    [1.,0.,0.], rtol=1e-10,atol=1e-12)
    exact = np.array(fractions(t,r))
    errors.append(float(np.max(np.abs(sol.y[:,-1]-exact))))
assert max(errors)<1e-8

# Dimensionless time traces for illustration, not actual seconds.
traces=[]
for r in [.001,.01,.03,.1,1.,10.]:
    for tau in np.concatenate(([0.],np.geomspace(.001,100,400))):
        a,b,c=fractions(tau,r)
        assert min(a,b,c)>-1e-12
        traces.append(dict(k65_over_k76=r,k76_t=tau,H7_fraction=a,H6_fraction=b,H5_fraction=c))
pd.DataFrame(traces).to_csv(OUT/'dimensionless_time_traces.csv',index=False)

# Storage after isolation in a *separate* condition: survival exp(-k_loss*t).
# One effective first-order channel and Arrhenius prefactor are ASSUMPTIONS.
ret=[]
for T in [100,200,300,500]:
    for duration_s in [3600.,86400.,31557600.]:
        for survival in [.9,.99,.999]:
            kmax=-math.log(survival)/duration_s
            for attempt_s in [1e9,1e12,1e13]:
                ret.append(dict(T_K=T,duration_s=duration_s,survival=survival,
                    prefactor_per_s=attempt_s,max_effective_loss_per_s=kmax,
                    min_effective_loss_barrier_eV=KB*T*math.log(attempt_s/kmax)))
pd.DataFrame(ret).to_csv(OUT/'conditional_storage_barriers.csv',index=False)

# Phi_x = G_x - x*mu_H. Per formula (one Ir), not per atom!
# H6 wins against x=5,7 iff G6-G5 <= mu_H <= G7-G6.
# W=G5+G7-2G6. H5 entropy alone changes W by -kT log(6).
# No material E supplied here: sweep *assumed* W0, not inferred phase energies.
entropy=[]
for T in [0,100,200,300,500,800]:
    for W0 in [-.3,-.1,0.,.025,.05,.1,.2,.3]:
        shift=KB*T*math.log(6)
        W=W0-shift
        # A convenient artificial energy gauge: G6=0, G5=G7=W0/2.
        G5=W0/2-shift; G6=0.; G7=W0/2
        lower=G6-G5; upper=G7-G6
        assert abs(upper-lower-W)<1e-14
        if W>0:
            mu=(lower+upper)/2
            phi=np.array([G5-5*mu,G6-6*mu,G7-7*mu])
            assert np.argmin(phi)==1
        entropy.append(dict(T_K=T,assumed_W0_eV_per_formula=W0,
            H5_ideal_TS_eV_per_formula=shift,window_width_eV_per_H=W,
            H6_strict_window_exists_among_567=bool(W>0),
            H6_energy_above_equal_5_7_mixture_eV_per_formula=-W/2))
pd.DataFrame(entropy).to_csv(OUT/'hypothetical_grand_potential_windows.csv',index=False)

# Gauge invariance: an arbitrary per-H energy reference cancels in W.
rng=np.random.default_rng(42)
for _ in range(100):
    G=rng.normal(size=3); c=float(rng.normal())
    shifted=G+np.array([5,6,7])*c
    assert abs((G[0]+G[2]-2*G[1])-(shifted[0]+shifted[2]-2*shifted[1]))<1e-13

# Worst-case bounded per-atom errors: 8eps + 10eps + 2*9eps = 36eps.
# This is NOT a calibrated CHGNet uncertainty.
unc=[dict(assumed_bound_meV_per_atom=e,
          worst_case_W_error_meV_per_formula=36*e,
          independence_RSS_W_error_meV_per_formula=math.sqrt(8**2+10**2+18**2)*e)
     for e in [1.,5.,10.,25.,50.]]
pd.DataFrame(unc).to_csv(OUT/'illustrative_energy_error_budget.csv',index=False)

sel=[x for x in rows if x['target_peak_H6'] in [.9,.99] and x['T_K']==300 and x['A65_over_A76']==1]
store=[x for x in ret if x['T_K']==300 and x['duration_s']==86400 and x['survival']==.99 and x['prefactor_per_s']==1e13]
summary=dict(scope='Conditional phase-access review of C0001, not material-specific rates or new Tc',
             kb_eV_K=KB,sequential_targets_at_300K_equal_prefactors=sel,
             storage_example=store[0],H5_entropy_window_reduction_eV_at_300K=KB*300*math.log(6),
             max_ODE_absolute_error=max(errors),all_checks_passed=True,
             gauge_invariance_tests=100,
             versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,pandas=pd.__version__))
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
