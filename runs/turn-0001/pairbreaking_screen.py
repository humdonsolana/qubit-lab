"""Conditional heavy-fermion pair-breaking screen; NOT a material Tc prediction.
Run: python pairbreaking_screen.py
Conventions: kB in meV/K, Gamma an effective pair-breaking ENERGY in meV.
ln(T0/T) = psi(1/2+Gamma/(2*pi*kB*T)) - psi(1/2).
No transport lifetime or residual-resistivity conversion is assumed.
Model sources and scope: README.md and heavy_fermion_literature.md.
"""
from pathlib import Path
import csv, json, platform
import numpy as np
import scipy
from scipy.constants import Boltzmann, electron_volt
from scipy.special import digamma
from scipy.optimize import brentq

OUT = Path('outputs'); OUT.mkdir(exist_ok=True)
KB = Boltzmann / electron_volt * 1000
PSI_HALF = digamma(0.5)
TREF = 2.3  # experimental reference, IDEALIZED as clean for the main scenarios

def critical_gamma(t0):
    return np.pi * np.exp(-np.euler_gamma) * KB * t0 / 2

def residual(t, t0, gamma):
    return np.log(t0/t) - (digamma(0.5 + gamma/(2*np.pi*KB*t)) - PSI_HALF)

def tc(t0, gamma):
    if gamma < 0 or t0 <= 0:
        raise ValueError('Require Gamma >= 0 and T0 > 0')
    if gamma == 0:
        return float(t0)
    if gamma >= critical_gamma(t0):
        return 0.0
    return brentq(lambda t: residual(t,t0,gamma), t0*1e-7, t0, xtol=1e-12)

def gamma_at_target(t0, target):
    if target > t0 or target <= 0:
        raise ValueError('Require 0 < target <= T0')
    if target == t0:
        return 0.0
    return brentq(lambda g: residual(target,t0,g), 0, critical_gamma(t0), xtol=1e-14)

def save_csv(name, rows):
    with (OUT/name).open('w', newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)

# Forward sweep of hypothetical intrinsic gains. These gains are not measured.
gains=[0,0.05,0.1,0.2,0.5]
rows=[]
for gain in gains:
    t0=TREF*(1+gain)
    for g in np.linspace(0,0.32,321):
        t=tc(t0,g)
        rows.append(dict(clean_gain_fraction=gain,clean_tc_k=t0,gamma_mev=g,tc_k=t,beats_reference=bool(t>TREF)))
save_csv('ag_grid.csv',rows)

thresholds=[]
for gain in gains[1:]:
    t0=TREF*(1+gain)
    g=gamma_at_target(t0,TREF)
    thresholds.append(dict(clean_gain_fraction=gain,clean_tc_k=t0,gamma_erasing_gain_mev=g,
                           gamma_critical_mev=critical_gamma(t0),roundtrip_tc_k=tc(t0,g)))
save_csv('ag_thresholds.csv',thresholds)

# Identifiability check: the observed 2.3 K need not be the clean Tc.
# Infer clean reference from ASSUMED existing Gamma, then give it 10% gain.
baselines=[]
for g0 in [0,0.025,0.05,0.1]:
    clean_ref=TREF*np.exp(digamma(0.5+g0/(2*np.pi*KB*TREF))-PSI_HALF)
    total_g=gamma_at_target(1.1*clean_ref,TREF)
    baselines.append(dict(assumed_baseline_gamma_mev=g0,inferred_clean_reference_k=clean_ref,
                          hypothetical_clean_gain_fraction=0.1,additional_gamma_erasing_gain_mev=total_g-g0))
save_csv('baseline_sensitivity.csv',baselines)

# Independent LOCAL linear arithmetic from Gofryk et al. PRL 109,186402 (2012).
# Their x or y counts dopant atoms PER FORMULA UNIT, not fraction of all atoms.
# Slopes isolated through pressure/codoping, not ambient-pressure alloy forecasts.
slopes=[('Cd','In',5,5.0),('Pt','Co',1,11.2),('Sn','In',5,13.3)]
empirical=[]
for gain in [0.05,0.1,0.2]:
    for dopant,site,multiplicity,slope in slopes:
        amount=TREF*gain/slope
        empirical.append(dict(hypothetical_gain_k=TREF*gain,dopant=dopant,host_site=site,
                              loss_slope_k_per_dopant_per_formula=slope,
                              dopants_per_formula_erasing_gain=amount,
                              host_site_percent_erasing_gain=100*amount/multiplicity))
save_csv('empirical_local_budgets.csv',empirical)

# Tests independent of table presentation.
assert tc(TREF,0)==TREF
assert tc(TREF,critical_gamma(TREF))==0
assert tc(TREF,1.01*critical_gamma(TREF))==0
small_g=KB*TREF*1e-5
slope=(tc(TREF,small_g)-TREF)/small_g
expected=-np.pi/(4*KB)
assert np.isclose(slope,expected,rtol=1e-4)
for gain in gains:
    ts=[r['tc_k'] for r in rows if r['clean_gain_fraction']==gain]
    assert np.all(np.diff(ts)<=1e-10)
positive=[r for r in rows if r['gamma_mev']>0 and r['tc_k']>0]
max_residual=max(abs(residual(r['tc_k'],r['clean_tc_k'],r['gamma_mev'])) for r in positive)
assert max_residual < 1e-9
assert all(abs(r['roundtrip_tc_k']-TREF)<1e-9 for r in thresholds)
for row in baselines:
    assert abs(tc(row['inferred_clean_reference_k'],row['assumed_baseline_gamma_mev'])-TREF)<1e-9
summary=dict(model='conditional homogeneous AG, no material fit',reference_tc_k=TREF,kb_mev_per_k=KB,
             grid_rows=len(rows),max_equation_residual=max_residual,
             numerical_initial_slope_k_per_mev=slope,analytic_initial_slope_k_per_mev=expected,
             all_tests_passed=True,thresholds=thresholds,baseline_sensitivity=baselines,
             versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__))
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
print('\nIndependent empirical LOCAL budgets for hypothetical 0.23 K gain:')
for r in empirical:
    if np.isclose(r['hypothetical_gain_k'],0.23): print(r)

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(7,4.5))
    for gain in gains:
        subset=[r for r in rows if r['clean_gain_fraction']==gain]
        ax.plot([r['gamma_mev']*1000 for r in subset],[r['tc_k'] for r in subset],label=f'{gain:.0%} assumed clean gain')
    ax.axhline(TREF,color='black',ls='--',lw=1,label='2.3 K reference')
    ax.set(xlabel='Effective pair-breaking energy Gamma (micro-eV)',ylabel='Conditional Tc (K)',title='Sensitivity benchmark only; not a CeCoIn5 fit')
    ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(OUT/'ag_sensitivity.png',dpi=160); plt.close(fig)
except ImportError:
    print('matplotlib unavailable; CSV and JSON results retained')
