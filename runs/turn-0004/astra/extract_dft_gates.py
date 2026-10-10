#!/usr/bin/env python3
"""Recover primary-source numerical .res data and reference-free stability tests.
Source: Dolui et al., PRL132166001, arXiv2310.07562v2, Appendix XI.
No new DFT calculation. Network required unless --html supplies a cached copy.
AIRSS TITL reported scalar is called reported_energy_eV below, without assuming
that printed residual pressure means a nonzero target pressure. See README.
"""
import argparse,base64,hashlib,json,math,re
from pathlib import Path
from collections import Counter
import requests
from bs4 import BeautifulSoup

URL='https://arxiv.org/html/2310.07562v2'
parser=argparse.ArgumentParser(); parser.add_argument('--html'); args=parser.parse_args()
html=Path(args.html).read_text() if args.html else requests.get(URL,timeout=60).text
soup=BeautifulSoup(html,'html.parser')
out=Path(__file__).resolve().parent/'outputs';out.mkdir(exist_ok=True)
rawdir=out/'source_res';rawdir.mkdir(exist_ok=True)
wanted={'MgIrH-2-Mg2IrH5-Cmcm','MgIrH-1-Mg2IrH6-Fm-3m','MgIrH-1-Mg2IrH7-Fm-3m','MgIrH-1-Mg2IrH7-R-3m','MgIrH-2-Mg2IrH6-Amm2'}
records={}
for div in soup.select('.ltx_listing'):
    a=div.select_one('a[href^="data:text/plain;base64,"]')
    if a is None: continue
    raw=base64.b64decode(a['href'].split(',',1)[1]); text=raw.decode()
    lines=text.splitlines();header=lines[0].split();label=header[1]
    if label not in wanted: continue
    count=Counter()
    for line in lines:
        tok=line.split()
        if len(tok)>=6 and tok[0] in ['Mg','Ir','H']:
            count[tok[0]]+=1
    nfu=count['Ir']; nat=sum(count.values())
    assert count['Mg']==2*nfu and nat==int(header[7])
    x=count['H']/nfu; assert x in [5,6,7]
    metadata=[line for line in lines if line.startswith('REM')]
    assert any('PBE for solids (2008)' in v for v in metadata)
    assert any('Cut-off 600.0000 eV' in v for v in metadata)
    assert any('Spacing 0.03' in v for v in metadata)
    pp=[v for v in metadata if re.match(r'REM (Mg|Ir|H) ',v)]
    (rawdir/(label+'.res')).write_bytes(raw)
    records[label]=dict(appendix_html_id=div.get('id'),header=lines[0],
      raw_sha256=hashlib.sha256(raw).hexdigest(),counts=dict(count),formula_units=nfu,
      hydrogen_per_formula=int(x),printed_pressure_GPa=float(header[2]),
      volume_A3_cell=float(header[3]),reported_energy_eV_cell=float(header[4]),
      reported_energy_eV_per_formula=float(header[4])/nfu,
      reported_volume_A3_per_formula=float(header[3])/nfu,
      metadata=metadata,pseudopotentials=pp)
assert set(records)==wanted
assert len({tuple(r['pseudopotentials']) for r in records.values()})==1
E=lambda s:records[s]['reported_energy_eV_per_formula']
H5='MgIrH-2-Mg2IrH5-Cmcm';H6='MgIrH-1-Mg2IrH6-Fm-3m'
results=[]
for H7 in ['MgIrH-1-Mg2IrH7-Fm-3m','MgIrH-1-Mg2IrH7-R-3m']:
    W=E(H5)+E(H7)-2*E(H6)
    lower=E(H6)-E(H5);upper=E(H7)-E(H6)
    assert abs((upper-lower)-W)<1e-9
    # Deliberately overconservative sensitivity if all printed residual PV
    # magnitudes were treated as uncertainty; not a physical correction.
    pv_bound=sum(weight*abs(records[k]['printed_pressure_GPa'])*records[k]['reported_volume_A3_per_formula']/160.2176634
                 for k,weight in [(H5,1),(H7,1),(H6,2)])
    results.append(dict(H7_competitor=H7,W_eV_per_balanced_reaction=W,
        lower_muH_eV_same_DFT_reference=lower,upper_muH_eV_same_DFT_reference=upper,
        strict_H6_window_exists_among_selected_567=bool(W>0),
        H6_above_equal_mixture_meV_per_H6_atom=-1000*W/18,
        sum_absolute_printed_PV_eV_per_reaction=pv_bound,
        sign_negative_even_under_printed_PV_bound=bool(W+pv_bound<0)))
amm=E('MgIrH-2-Mg2IrH6-Amm2')-E(H6)
summary=dict(source=URL,source_doi='10.1103/PhysRevLett.132.166001',
 scope='Re-analysis of reported near-zero-pressure static DFT numerical data; not new DFT or finite-temperature free energy',
 records=records,balanced_tests=results,
 Amm2_minus_cubic_H6_eV_per_formula=amm,
 Amm2_minus_cubic_H6_meV_per_atom=1000*amm/9,
 all_composition_and_settings_checks_passed=True)
(out/'dft_gate_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
