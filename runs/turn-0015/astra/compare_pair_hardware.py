"""Rigorous finite-count intervals for truncated top64 hardware output.
Never renormalize known counts. Unknown shots may contribute +/-1 to each
Pauli product. Intervals enclose the full-sample mean, NOT confidence intervals
for the quantum expectation. Worst-case sampling scale separately provided.
"""
import json,math
from pathlib import Path
p=Path('outputs');h=json.loads((p/'pair_coherence_hardware.json').read_text());s=json.loads((p/'pair_coherence_simulation.json').read_text())
c=h['counts'];N=h['shots'];known=sum(c.values());missing=N-known
assert missing>=0
rows=[]
for k,d in enumerate([0.,3.]):
 r={'delta_over_J':d,'ideal_XX':s['expected'][k]['XX'],'aer':s['simulation'][str(d)]}
 for label,b in [('XX',2*k),('ZZ',4+2*k)]:
  total=sum(v*(1 if ((int(key,2)>>b)&1)==((int(key,2)>>(b+1))&1) else -1) for key,v in c.items())
  r['hardware_'+label+'_full_sample_interval']=[(total-missing)/N,(total+missing)/N]
 rows.append(r)
out={'job_id':h['job_id'],'backend':h['backend'],'quantum_seconds':h['quantum_seconds'],'shots':N,'returned_counts_total':known,'missing_counts':missing,'missing_fraction':missing/N,'worst_case_sampling_SE':1/math.sqrt(N),'rows':rows,'verdict':'Hardware XX=1 preparation is strongly biased; neither error mitigation nor material inference justified. Raw output truncated; all intervals account for missing shots. XX contrasts test toy phase coherence only, not FeSe Tc.'}
(p/'pair_coherence_comparison.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
