"""Recheck the existing target from saved primary-source energies, not new DFT."""
import json,sys
from pathlib import Path
from decimal import Decimal as D
p=Path(__file__).parent/'../../turn-0004/astra/outputs/dft_gate_compact.json'
x=json.loads(p.read_text(),parse_float=D)['records']
def e(name):return x[name]['reported_energy_eV_per_formula']
e6=e('MgIrH-1-Mg2IrH6-Fm-3m');e5=e('MgIrH-2-Mg2IrH5-Cmcm')
r=[]
for name in ['MgIrH-1-Mg2IrH7-Fm-3m','MgIrH-1-Mg2IrH7-R-3m']:
    W=e5+e(name)-2*e6
    r.append({'competitor':name,'reaction_energy_eV':str(W),'H6_above_mixture_meV_per_atom':str(-W/D(18)*1000),'static_mu_window_exists':W>=0})
res={'candidate':'C0001','verdict':'existing challenge upheld; no new synthesis or Tc evidence','not_new_DFT':True,'results':r,'bar_review':'105 K conditional prediction is below 133 K; older 160-175 K computations are not a demonstrated upward route after dense-grid 90-120 K estimates. Retention alone would not establish an above-bar material.'}
out=Path(sys.argv[1] if len(sys.argv)>1 else 'outputs');out.mkdir(exist_ok=True,parents=True);(out/'c0001_review.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
