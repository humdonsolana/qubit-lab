"""Reproduce literature thermodynamic gates, not new DFT or pressure phase diagrams.
MgAlFeH6: Xu et al. npj Comput Mater12,183(2026), DOI10.1038/s41524-026-02040-x.
Use reported approximate decomposition energy 0.11eV/atom (do not reconstruct
it by subtracting formation energies normalized to different atom totals).
C0001: reread original Dolui numerical blocks already extracted in Turn4.
"""
import json,sys,math
from pathlib import Path
from decimal import Decimal as D
from pymatgen.core import Composition
KB=8.617333262145e-5
reaction={'MgAlFeH6':-6,'AlH3':5,'Mg2FeH6':3,'AlFe3H':1,'H2':1}
balance={e:sum(c*Composition(f)[e] for f,c in reaction.items()) for e in ['Mg','Al','Fe','H']}
assert all(abs(v)<1e-12 for v in balance.values())
natoms=6*Composition('MgAlFeH6').num_atoms;assert natoms==54
above=.11;deltaE=-above*natoms
# DeltaG_rxn ~= DeltaE + delta_mu_H2 with all solid contributions fixed.
rows=[]
for temp in [300,600,1000]:
 for decades in [1,3,6]:
  dm=KB*temp*math.log(10)*decades
  rows.append({'temperature_K':temp,'fugacity_ratio_decades':decades,'increment_delta_mu_H2_eV':dm,'increase_reaction_free_energy_meV_per_atom':dm/natoms*1000})
source=Path(__file__).resolve().parent/'../../turn-0004/astra/outputs/dft_gate_compact.json'
x=json.loads(source.read_text(),parse_float=D)['records']
def energy(k):return x[k]['reported_energy_eV_per_formula']
e5=energy('MgIrH-2-Mg2IrH5-Cmcm');e6=energy('MgIrH-1-Mg2IrH6-Fm-3m')
c1=[]
for comp in ['MgIrH-1-Mg2IrH7-Fm-3m','MgIrH-1-Mg2IrH7-R-3m']:
 w=e5+energy(comp)-2*e6
 c1.append({'H7_competitor':comp,'D_E5_plus_E7_minus_2E6_eV':str(w),'H6_above_equal_mixture_meV_per_atom':str(-w/D(18)*1000),'mu_H_coefficient':0,'static_mu_window_exists':bool(w>=0)})
r={'not_new_DFT':True,'MgAlFeH6':{'balanced_decomposition':reaction,'balance_residual':balance,'atoms_in_reaction':natoms,'input_above_hull_eV_per_atom_approximate':above,'reaction_energy_eV_approximate':deltaE,'required_H2_mu_increment_over_static_reference_eV_approximate':-deltaE,'ideal_fugacity_differential_scenarios':rows,'limitations':['No zero-point, finite-temperature solid free energies, actual gas standard chemical potential, compressibility or solid P-deltaV included.','Ideal fugacity response is differential, not pressure inferred from a static H2 DFT reference.','High-pressure synthesis is not ruled out: solid enthalpies/structures vary with pressure.','Reported 130K is an unmade literature prediction below the 133K bar; no candidate proposed.']},'C0001':{'verdict':'challenge maintained; no new support for phase access or above133K route','results':c1,'latest_primary_source':'Sinha et al., arXiv:2602.23675: H7 reverts to H5 below ~20GPa during room-temperature unloading; no spontaneous superconducting H6 intermediate.'}}
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True);(out/'phase_access_review.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
