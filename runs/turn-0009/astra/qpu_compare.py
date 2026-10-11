import json,sys
from pathlib import Path
from holstein_benchmark import analyze,exact
root=Path(__file__).parent
raw=json.loads((root/'outputs/qpu_raw.json').read_text());a=analyze(raw['counts']);val,s=exact(2);p=abs(s)**2
truth={'double_occupancy':val['D'],'phonon_occupation':val['nphonon'],'joint_D_phonon':float(p[4]+p[7])}
for key,r in a['estimates'].items():
 r['exact_truncated_model']=truth[key];r['bias']=r['mean']-truth[key];r['bias_in_shot_se']=r['bias']/r['shot_se']
assert a['shots']==raw['requested_shots']
a.update({'job_id':raw['job_id'],'backend':raw['backend'],'quantum_seconds':raw['quantum_seconds'],'postselection':False,'readout_mitigation':False,'error_note':'Shot SE excludes device drift/gate/readout errors and phonon truncation error. Exact preparation is not a quantum solver or Tc calculation.'})
out=Path(sys.argv[1]);out.mkdir(exist_ok=True,parents=True);(out/'qpu_comparison.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps(a,indent=2))
