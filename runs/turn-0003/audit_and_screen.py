"""Turn 0003: empirical-ceiling audit and fixed-geometry XRD screen.
Run: python audit_and_screen.py. No DFT, EPC or synthesis performed.
"""
from pathlib import Path
import json, shutil, platform
from importlib.metadata import version
import numpy as np
import pandas as pd
from scipy.constants import physical_constants
from scipy.stats import linregress, t
from pymatgen.core import Lattice, Structure
from pymatgen.analysis.diffraction.xrd import XRDCalculator

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)
p = json.loads((ROOT / 'source_inputs.json').read_text())
prior = ROOT / p['prior_data']
shutil.copyfile(prior, OUT / 'prior_hf_table.csv')
df = pd.read_csv(prior)
# Match Turn 2's rounded constant exactly, not scipy's higher precision R.
R = 8.314

def hf_stats(d):
    fit = linregress(np.log(d.gamma_mJ), np.log(d.Tc_K))
    bound = float((d.gamma_mJ*d.Tc_K).max())
    half = float(t.ppf(.975,len(d)-2)*fit.stderr)
    return dict(n=len(d), slope=float(fit.slope), r2=float(fit.rvalue**2),
                slope_OLS_95_interval=[float(fit.slope-half),float(fit.slope+half)],
                max_Tc_gamma=bound, conditional_gamma50_K=bound/50)

hf = {'all':hf_stats(df), 'without_PuCoGa5':hf_stats(df[df.compound!='PuCoGa5']),
      'without_Pu':hf_stats(df[~df.compound.str.startswith('Pu')])}
prod = float((df.gamma_mJ*df.Tc_K).max())
proxy = np.pi**2 * R / (2*df.gamma_mJ.values/1000)
assert np.allclose(proxy, df.Tstar_K.values)
assert np.isclose(prod/50,28.49)
hf['conditional_gamma50_alternate_Pu_gamma95_K'] = 18.5*95/50
hf['300K_gamma50_extrapolation_factor'] = 300*50/prod
hf['warning'] = 'Sample maximum is not a universal upper bound. OLS interval ignores selection and measurement errors.'
(OUT/'hf_audit.json').write_text(json.dumps(hf,indent=2)+'\n')

# N independent IrH5 units have 6**N orientations. Comparing unconstrained
# Bernoulli disorder does NOT supply a thermodynamic phase boundary.
kB = physical_constants['Boltzmann constant in eV/K'][0]
ent=[]
for temp in p['entropy_model']['temperatures_K']:
    constrained = kB*temp*np.log(6)*1000
    unconstrained = -6*kB*temp*((5/6)*np.log(5/6)+(1/6)*np.log(1/6))*1000
    ent.append(dict(T_K=temp, TS_one_vacancy_meV_per_H5_formula=constrained,
                    TS_one_vacancy_meV_per_H5_atom=constrained/8,
                    TS_independent_sites_meV_per_H5_formula=unconstrained))
pd.DataFrame(ent).to_csv(OUT/'vacancy_entropy.csv',index=False)

# Same cell/coordinates; occupancy alone changes. Geometry is NOT optimized.
g = p['diffraction_model']
calc = XRDCalculator(wavelength=g['wavelength'])
patterns=[]
for name,occ in [('H6',1.0),('H5_average',5/6)]:
    s = Structure.from_spacegroup('Fm-3m',Lattice.cubic(g['a_angstrom']),
           ['Mg','Ir',{'H':occ}], [g['Mg_8c'],g['Ir_4a'],g['H_24e']])
    assert np.isclose(s.composition['Mg'],8) and np.isclose(s.composition['Ir'],4)
    assert np.isclose(s.composition['H'],24*occ)
    s.to(filename=str(OUT/f'Mg2Ir{name}_fixed_geometry.cif'))
    pat=calc.get_pattern(s,scaled=False,two_theta_range=tuple(g['two_theta_degrees']))
    patterns.append(pat)
    pd.DataFrame({'two_theta_degree':pat.x,'intensity_unscaled':pat.y,
                   'hkl':list(map(str,pat.hkls))}).to_csv(OUT/f'xrd_{name}.csv',index=False)

p6,p5=patterns
assert len(p6.x)==len(p5.x) and np.allclose(p6.x,p5.x,atol=1e-9)
a,b=p6.y,p5.y
scale=float(np.dot(a,b)/np.dot(b,b))
rel=float(np.linalg.norm(a-scale*b)/np.linalg.norm(a))
cos=float(np.dot(a,b)/np.linalg.norm(a)/np.linalg.norm(b))
strong=a/a.max()>.01
contrast=np.abs(a-scale*b)/a
pd.DataFrame({'two_theta_degree':p6.x,'H6_normalized':100*a/a.max(),
              'H5_rescaled_to_H6':100*scale*b/a.max(),
              'fractional_difference':contrast,'strong_gt_1pct':strong}).to_csv(OUT/'xrd_comparison.csv',index=False)
xrd=dict(n_peaks=len(a),scale_H5_to_H6=scale,scale_fitted_relative_L2=rel,
         intensity_vector_cosine=cos, max_relative_difference_strong_peaks=float(contrast[strong].max()),
         same_positions_by_construction=True,
         warning='Illustrative kinematic fixed-geometry CuKa calculation, not real phase fingerprints or experimental detection limit.')
(OUT/'xrd_metrics.json').write_text(json.dumps(xrd,indent=2)+'\n')
summary=dict(hf=hf,xrd=xrd,entropy=ent,
             forecast=p['candidate'],versions={k:version(k) for k in ['numpy','pandas','scipy','pymatgen']},python=platform.python_version())
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
print('ALL NUMERICAL CHECKS PASSED')
