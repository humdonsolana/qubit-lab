#!/usr/bin/env python3
"""Read-only independent arithmetic checks of committed numerical artifacts."""
from pathlib import Path
import json,math
from decimal import Decimal
p=Path(__file__).resolve().parent/'outputs'
d=json.loads((p/'dft_gate_compact.json').read_text())
E={}
for label,r in d['records'].items():
    h=r['header'].split(); c=r['counts']; nf=c['Ir']
    assert sum(c.values())==int(h[7]) and c['Mg']==2*nf and nf==r['formula_units']
    E[label]=Decimal(h[4])/Decimal(nf)
    assert abs(float(E[label])-r['reported_energy_eV_per_formula'])<1e-10
E5=E['MgIrH-2-Mg2IrH5-Cmcm'];E6=E['MgIrH-1-Mg2IrH6-Fm-3m']
for r in d['balanced_tests']:
    W=E5+E[r['H7_competitor']]-2*E6
    assert abs(float(W)-r['W_eV_per_balanced_reaction'])<1e-9
    assert W<0 and not r['strict_H6_window_exists_among_selected_567']
    assert abs(-float(W)*1000/18-r['H6_above_equal_mixture_meV_per_H6_atom'])<1e-7
    print('DFT balanced W:',r['H7_competitor'],str(W),'eV/reaction')
s=json.loads((p/'summary.json').read_text())
for row in s['sequential_targets_at_300K_equal_prefactors']:
    r=row['max_k65_over_k76'];target=row['target_peak_H6']
    assert abs(math.exp(r*math.log(r)/(1-r))-target)<1e-12
    assert abs(1/r-row['min_k76_over_k65'])<1e-8
    assert abs(s['kb_eV_K']*300*math.log(1/r)-row['min_E65_minus_E76_eV'])<1e-12
    print('Kinetic gate:',target,'max rate ratio',r)
a=s['storage_example'];k=a['prefactor_per_s']*math.exp(-a['min_effective_loss_barrier_eV']/(s['kb_eV_K']*a['T_K']))
assert abs(math.exp(-k*a['duration_s'])-a['survival'])<1e-12
assert s['all_checks_passed'] and d['all_composition_and_settings_checks_passed']
print('All committed-result checks passed; no network or writes required.')
