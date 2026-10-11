"""Reference-balanced decomposition using ONLY one published DFT table.
Source: Seeyangnok, Pinsook & Ackland, npj 2D Mater Appl 9,70 (2025),
DOI 10.1038/s41699-025-00590-0 Table2. Table values: E_form eV/atom
relative to elemental metals, alpha-B and molecular H2. Formula M2B2Hn
contains 4+n atoms. Negative elemental formation is NOT a convex-hull test.
No new DFT, ZPE, finite-T, kinetic barrier, substrate energy or Tc calculation.
"""
from decimal import Decimal as D
import json,sys
from pathlib import Path
TABLE={'Sc':['-.2015','-.3458','-.2470','-.1674'],'Y':['-.4746','-.5812','-.5119','-.4597'],'V':['-.1780','-.3191','-.2158','-.1332'],'Nb':['-.3233','-.4353','-.4015','-.3728']}
def main(out):
 data={}
 for metal,es in TABLE.items():
  E={n:D(s)*D(4+n) for n,s in enumerate(es,1)}
  reactions=[];thresholds=[]
  for n in [1,2,3]:
   delta=E[n]-E[4];thresh=-delta/D(4-n)
   # Last printed digit rounded within +/- .00005 eV/atom in each phase.
   err=D('.00005')*D(8+4+n)
   reactions.append({'reaction':f'{metal}2B2H4 -> {metal}2B2H{n} + {(4-n)/2:g} H2','delta_E_eV_per_M2B2':float(delta),'rounding_bound_eV':float(err),'excess_parent_meV_per_initial_atom':max(0,float(-delta/D(8)*1000))})
   thresholds.append(thresh)
  threshold=max(thresholds)
  data[metal]={'formation_eV_per_atom':{str(n):float(D(s)) for n,s in enumerate(es,1)},'formation_eV_per_M2B2':{str(n):float(v) for n,v in E.items()},'dehydrogenation_reactions':reactions,'necessary_muH_min_eV_relative_halfH2_for_H4':float(threshold),'active_competitor_n':1+thresholds.index(threshold),'H4_lowest_at_muH0_within_n1to4':threshold<=0,'largest_tested_decomposition_lower_bound_meV_per_atom':max(r['excess_parent_meV_per_initial_atom'] for r in reactions)}
 # Hypothetical ideal mixing is only an algebraic target, not an alloy energy.
 # At V fraction x, each dehydrogenation delta is interpolated between Nb and V.
 xr=[]
 for i,n in enumerate([1,2,3]):
  dv=data['V']['dehydrogenation_reactions'][i]['delta_E_eV_per_M2B2'];dn=data['Nb']['dehydrogenation_reactions'][i]['delta_E_eV_per_M2B2']
  xr.append({'competitor_n':n,'maximum_V_fraction_at_muH0_if_linear_energies':dn/(dn-dv)})
 result={'source':'https://www.nature.com/articles/s41699-025-00590-0/tables/2','scope':'Static electronic energies, partial competing set (same 2D M2B2 skeleton). An exothermic listed decomposition suffices for instability within this dataset; no such decomposition is NOT proof of stability. Different Hn relaxation geometries included by authors. ZPE, entropy, substrate and barriers absent.','metals':data,'unvalidated_ideal_V_Nb_alloy_interpolation':xr,'alloy_warning':'No alloy has been computed or proposed as a candidate. Positive mixing energy, segregation, magnetism, phonons and competing bulk borides/hydrides remain unknown.'}
 out=Path(out);out.mkdir(exist_ok=True,parents=True);(out/'hydrogen_retention.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main(sys.argv[1])
