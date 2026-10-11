import json,sys
from pathlib import Path
from holstein_softening import analyze,exact
root=Path(__file__).parent
raw=json.loads((root/'outputs/qpu_raw.json').read_text());result=analyze(raw['counts']);val,v=exact(4,1.5);p=v*v
truth={'D':val['D'],'nphonon':val['nphonon'],'D_nphonon':sum(p[i]*float((i&1)==((i>>1)&1))*(i>>2) for i in range(16))}
assert result['shots']==raw['requested_shots']
for k,m in result['measurements'].items():m.update(exact_truncated=truth[k],bias=m['mean']-truth[k],bias_over_shot_se=(m['mean']-truth[k])/m['shot_se'])
result.update(job_id=raw['job_id'],backend=raw['backend'],quantum_seconds=raw['quantum_seconds'],readout_mitigation=False,postselection=False,warning='Shot SE only; systematic gate/readout and phonon truncation errors are separate. Hardware state preparation, not quantum solution or Tc.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
