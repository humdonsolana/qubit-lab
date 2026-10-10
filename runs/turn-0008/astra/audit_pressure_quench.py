"""Reproduce source arithmetic and show measurement-induced aging confound.
No Tc prediction fit, no phase-fraction conversion, no extracted lifetime.
python audit_pressure_quench.py /tmp/astra8/outputs
"""
import json,sys,math,csv
from pathlib import Path
import numpy as np
from scipy.constants import Boltzmann, electron_volt
ROOT=Path(__file__).resolve().parent
OUT=Path(sys.argv[1] if len(sys.argv)>1 else ROOT/'outputs');OUT.mkdir(exist_ok=True,parents=True)
x=json.loads((ROOT/'source_inputs.json').read_text());kb=Boltzmann/electron_volt

def save_csv(name,rows):
 with (OUT/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

protocols=[]
for p in x['protocols']:
 r=p.copy();r['lost_onset_K']=p['target_onset_K']-p['first_retained_onset_K']
 r['retained_excess_onset_ratio_NOT_phase_fraction']=(p['first_retained_onset_K']-x['baseline_tc_k'])/(p['target_onset_K']-x['baseline_tc_k'])
 protocols.append(r)
save_csv('protocols.csv',protocols)
m=x['magnetism'];chi=m['abs_moment_over_field_emu_per_Oe'];r0=m['effective_disk_radius_cm'];f0=math.pi*chi/r0**3
radius=[]
for rel in [-.1,-.05,0,.05,.1]:
 r=r0*(1+rel);radius.append(dict(assumed_relative_radius_error=rel,radius_um=r*1e4,shielding_fraction_thin_disk=math.pi*chi/r**3))
save_csv('shielding_sensitivity.csv',radius)
# Equal integrated hazard k(T)*time boundary, attempt frequency cancels.
s=x['thermal_dose_scenario'];tc=s['cold_temperature_K'];ts=s['cold_duration_s'];tw=s['illustrative_warm_duration_s']
dose=[];boundaries=[]
for T in s['warm_temperatures_K']:
 Ecrit=kb*math.log(ts/tw)/(1/tc-1/T)
 boundaries.append(dict(warm_K=T,assumed_warm_duration_s=tw,cold_duration_s=ts,equal_hazard_barrier_eV=Ecrit))
 for E in s['assumed_barriers_eV']:
  logratio=math.log(tw/ts)+E/kb*(1/tc-1/T)
  dose.append(dict(assumed_E_eV=E,warm_K=T,warm_to_cold_integrated_hazard_ratio=math.exp(logratio),log10_ratio=logratio/math.log(10)))
save_csv('warm_readout_dose_scenarios.csv',dose);save_csv('equal_hazard_boundaries.csv',boundaries)
# Elementary independent checks: zero barrier ratio only duration; direct rates
# agree with analytical log ratio for every scenario and underflow-free domain.
for row in dose:
 E,T=row['assumed_E_eV'],row['warm_K']
 direct=(tw*np.exp(-E/kb/T))/(ts*np.exp(-E/kb/tc))
 assert np.isclose(direct,row['warm_to_cold_integrated_hazard_ratio'],rtol=1e-12)
for b in boundaries:
 ratio=tw/ts*math.exp(b['equal_hazard_barrier_eV']/kb*(1/tc-1/b['warm_K']))
 assert abs(ratio-1)<1e-12
assert .77<f0<.79
assert len(protocols)==5 and all(r['lost_onset_K']>0 for r in protocols)
summary=dict(shielding_reproduced=f0,shielding_temperature_K=70,shielding_is_not_high_tc_component_fraction=True,xrd_width_ratio=x['xrd']['quenched_200_fwhm_deg']/x['xrd']['pristine_200_fwhm_deg'],equal_hazard_boundaries=boundaries,protocols=protocols,checks_passed=True,limitations=['No calibrated phase fraction versus Tc-onset relation exists here.','S5 repeatedly warms to160/170K; nominal77K storage is not isothermal observation.','60s plateau used for sensitivity only, NOT a source-reported dwell time.','No activation barrier, attempt rate, room-temperature lifetime or residual pressure extracted.','Demagnetization sensitivity assumes source thin-disk model, no experimental uncertainty claimed.'])
(OUT/'audit_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
