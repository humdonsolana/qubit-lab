"""Analyze real counts, including joint-shot covariance; no mitigation/postselection."""
import sys,json
from pathlib import Path
# Import runs the deterministic Aer setup into the chosen writable output dir.
from hubbard_dimer_qpu import analyze_counts,exact,counts,OUT
raw=json.loads((Path(__file__).parent/'outputs/qpu_raw.json').read_text())
a=analyze_counts(counts);h=analyze_counts(raw['counts'])
for key,r in h['estimates'].items():
    r['exact']=exact[key];r['bias']=r['mean']-exact[key]
    r['bias_in_shot_se']=r['bias']/r['shot_se'] if r['shot_se'] else None
summary={'job_id':raw['job_id'],'backend':raw['backend'],'quantum_seconds':raw['quantum_seconds'],'exact':exact,'aer':a,'hardware':h,'limitations':['Finite repulsive Hubbard dimer, not FeSe parameterization, phonon calculation, Tc, or superconductivity evidence.','Shot standard errors do not include device drift, readout bias, or calibration uncertainty.','Three independent preparation replicas in one six-qubit circuit; no mitigation or postselection.','P is pair hopping, not pair binding. Positive P in a repulsive dimer does not imply attraction.']}
(OUT/'qpu_comparison.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
