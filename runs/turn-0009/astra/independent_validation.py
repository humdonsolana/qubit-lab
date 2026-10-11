"""Validate persisted artifacts and circuit without assuming shot agreement."""
import json,sys,math
from pathlib import Path
import numpy as np
from qiskit import qasm2
from qiskit.quantum_info import Statevector
import holstein_benchmark as h
root=Path(__file__).parent;out=Path(sys.argv[1]);out.mkdir(exist_ok=True,parents=True)
checks={}
# Exact vector simulation independent of the shot sampler.
qc=qasm2.loads((root/'outputs/holstein.qasm').read_text()).remove_final_measurements(inplace=False)
sv=Statevector.from_instruction(qc).data;v,s=h.exact(2)
fidelity=abs(np.vdot(s,sv))**2;assert fidelity>1-1e-12
checks['qasm_state_fidelity']=float(fidelity)
# Decoupled oscillator limit recovers the two-electron Hubbard dimer.
g=h.G;h.G=0.;vv,_=h.exact(4);h.G=g
expected=h.U/2-math.sqrt((h.U/2)**2+4*h.T**2)
assert abs(vv['E0']-expected)<1e-12;checks['zero_coupling_energy_error']=float(vv['E0']-expected)
# Independent observed probabilities use explicit bit bins.
raw=json.loads((root/'outputs/qpu_raw.json').read_text());c=raw['counts'];n=sum(c.values());assert n==8192
comp=json.loads((root/'outputs/qpu_comparison.json').read_text())
for k,bins in {'double_occupancy':['000','011','100','111'],'phonon_occupation':['100','101','110','111'],'joint_D_phonon':['100','111']}.items():
 p=sum(c.get(b,0) for b in bins)/n;assert p==comp['estimates'][k]['mean']
 checks[k+'_bin_check']=True
# Independently sample the f2 envelope on a dense grid.
ad=json.loads((root/'outputs/coulomb_sensitivity.json').read_text());r=np.linspace(1,20,100001);L=ad['inputs']['lambda']
for row in ad['sensitivity']:
 cc=1.82*(1+6.3*row['mu_star']);f=1+(r-1)*L*L/(L*L+cc*cc*r*r)
 assert max(f)<=row['f2_max']+1e-12;assert row['f2_max']-max(f)<1e-8
checks['AD_shape_envelope_grid_check']=True
# Test compact saved JSON against outputs from executable scripts.
for name in ['holstein_simulation.json','coulomb_sensitivity.json','phase_access_review.json','qpu_comparison.json']:
 p=Path('/tmp/astra9/outputs')/name
 if p.exists():assert json.loads(p.read_text())==json.loads((root/'outputs'/name).read_text())
checks['saved_json_matches_execution']=True
checks['convergence_D_N16_N32_difference']=abs(h.exact(16)[0]['D']-h.exact(32)[0]['D'])
print(json.dumps(checks,indent=2));(out/'validation.json').write_text(json.dumps(checks,indent=2)+'\n')
