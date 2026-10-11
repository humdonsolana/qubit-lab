"""Independent local audit. No import/execution of transport_reanalysis.py.
Stdlib CSV/median/bisect implementation; writes temporary JSON only when run.
Usage: python independent_transport_audit.py > /tmp/astra10_independent.json
"""
import bisect, csv, hashlib, json, math, statistics
from collections import defaultdict
from pathlib import Path
ROOT=Path('/tmp/astra10')
NAMES=['SC1_before','SC1_after','SC2_before','SC2_after']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    with p.open(newline='') as f: return list(csv.DictReader(f))
def interp(x, xs, ys):
    if x<=xs[0]: return ys[0]
    if x>=xs[-1]: return ys[-1]
    j=bisect.bisect_right(xs,x); i=j-1
    return ys[i]+(ys[j]-ys[i])/(xs[j]-xs[i])*(x-xs[i])
def cross(xs,ys,h,ref):
    candidates=[i for i in range(len(xs)-1) if xs[i+1]<=ref and ys[i]<h<=ys[i+1]]
    if not candidates: return None
    i=candidates[-1]
    return xs[i]+(h-ys[i])*(xs[i+1]-xs[i])/(ys[i+1]-ys[i])
def bins(rows,w):
    g=defaultdict(list)
    for x,y in rows:g[round(x/w)].append((x,y))
    return sorted([(statistics.median([v[0] for v in a]),statistics.median([v[1] for v in a])) for a in g.values()])
def calculate(b,ref):
    xs,ys=map(list,zip(*b)); rr=interp(ref,xs,ys)
    c={str(f):cross(xs,ys,f*rr,ref) for f in [.9,.5,.1,.01]}
    z={str(f):cross(xs,ys,f,ref) for f in [.01,.1,1.]}
    return dict(Rref_ohm_sq=rr,reference_T_K=ref,crossing_K=c,width90_10_K=c['0.9']-c['0.1'] if c['0.9'] is not None and c['0.1'] is not None else None,near_zero_threshold_ohm_sq_crossing_K=z,binned_points=len(b),minT_K=xs[0],R_at_5K_ohm_sq=interp(5,xs,ys))
def flatten(d,p=''):
    if isinstance(d,dict):
        for k,v in d.items():yield from flatten(v,p+'/'+k)
    else:yield p,d
published=json.loads((ROOT/'transport_results.json').read_text());manifest=json.loads((ROOT/'transport_manifest.json').read_text())
inputs={p.name:dict(bytes=p.stat().st_size,sha256=sha(p)) for p in [Path('transport_reanalysis.py'),Path('bilayer_spin_benchmark.py'),ROOT/'transport_results.json',ROOT/'transport_manifest.json',ROOT/'binned_transport.csv',ROOT/'spin_simulation.json',*[ROOT/(n+'.csv') for n in NAMES]]}
summary=dict(schema='astra-turn10-independent-v1',audit_date='2026-10-11',input_hashes=inputs,method=dict(mask='drop rows with missing x or y; strict 0<x<80 K',binning='round(x/bin_width) ties to even; independent medians of x and y; sort median x',interpolation='piecewise linear with endpoint clamp',crossing='largest-T adjacent pair below reference, low R < threshold <= high R; linear crossing; no monotonic fit',main_bin_K=.5,main_reference_K=50,fractions=[.9,.5,.1,.01],absolute_thresholds_ohm_sq=[.01,.1,1.],sensitivity='full 3x3 grid: bin widths 0.25/0.5/1 K, references 40/50/60 K',null='no qualifying crossing; not evidence of an instrument floor'),samples={},checks={})
all_errors=[];struct_errors=[];binned_errors=[]
existing_bins=read(ROOT/'binned_transport.csv')
for n in NAMES:
    raw=read(ROOT/(n+'.csv'));finite=[];missing=0
    for a in raw:
        if not a['x'].strip() or not a['y'].strip():missing+=1;continue
        x,y=float(a['x']),float(a['y'])
        if math.isnan(x) or math.isnan(y):missing+=1;continue
        if not math.isfinite(x) or not math.isfinite(y):raise ValueError('Nonfinite value')
        finite.append((x,y))
    rows=[(x,y) for x,y in finite if 0<x<80]
    grid={f'{w:g}K/{ref:g}K':calculate(bins(rows,w),ref) for w in [.25,.5,1.] for ref in [40,50,60]}
    main=grid['0.5K/50K']; b=bins(rows,.5)
    stored=[(float(r['x']),float(r['y'])) for r in existing_bins if r['sample']==n]
    if len(stored)!=len(b):struct_errors.append(n+' bin length mismatch')
    else:binned_errors.extend(abs(x-y) for a,z in zip(b,stored) for x,y in zip(a,z))
    for key,old in [('main',published[n]['main']),('bin_sensitivity/0.25',published[n]['bin_sensitivity']['0.25']),('bin_sensitivity/1.0',published[n]['bin_sensitivity']['1.0']),('reference_sensitivity/40',published[n]['reference_sensitivity']['40']),('reference_sensitivity/60',published[n]['reference_sensitivity']['60'])]:
        w=.25 if key.endswith('0.25') else 1. if key.endswith('1.0') else .5
        ref=40 if key.endswith('/40') else 60 if key.endswith('/60') else 50
        new=dict(flatten(calculate(bins(rows,w),ref)))
        for p,v in flatten(old):
            t=new[p]
            if v is None or t is None:
                if v!=t:struct_errors.append(n+key+p+' null mismatch')
            else:all_errors.append(abs(v-t))
    def ranges(keys):
        columns=defaultdict(list)
        for key in keys:
            for p,v in flatten(grid[key]):columns[p].append(v)
        return {p:dict(min=min(v for v in vs if v is not None) if any(v is not None for v in vs) else None,max=max(v for v in vs if v is not None) if any(v is not None for v in vs) else None,nulls=sum(v is None for v in vs)) for p,vs in columns.items() if p not in ['/reference_T_K']}
    low=[(x,y) for x,y in rows if x<=5];floor=[y for x,y in rows if x<=2.5]
    low_info=dict(raw_T_le_5_count=len(low),raw_T_le_5_R_min=min(y for x,y in low),raw_T_le_5_R_max=max(y for x,y in low),raw_T_le_5_R_median=statistics.median(y for x,y in low),raw_T_le_2_5_count=len(floor),raw_T_le_2_5_R_median=statistics.median(floor),raw_T_min=min(x for x,y in rows),lowest_bin_R=b[0][1],lowest_bin_T=b[0][0])
    floor_m=statistics.median(floor)
    xs,ys=map(list,zip(*b)); sub=[y-floor_m for y in ys]; corrected_rr=interp(50,xs,sub)
    low_info['diagnostic_only_constant_offset_subtraction']=dict(offset_ohm_sq=floor_m,R50_corrected=corrected_rr,T50_corrected_K=cross(xs,sub,.5*corrected_rr,50),T10_corrected_K=cross(xs,sub,.1*corrected_rr,50),absolute_crossings_K={str(h):cross(xs,sub,h,50) for h in [.01,.1,1.]},warning='Arbitrary raw T<=2.5K median subtraction; not calibrated or physical zero.')
    meta=manifest[n]
    summary['samples'][n]=dict(source_url=meta['url'],source_manifest_match=(meta['sha256']==inputs[n+'.csv']['sha256'] and meta['bytes']==inputs[n+'.csv']['bytes'] and meta['nraw']==len(raw)),raw_rows=len(raw),missing_rows=missing,mask_rows=len(rows),excluded_temperature_rows=len(finite)-len(rows),main=main,sensitivity_ranges=dict(bins_at_50K=ranges([f'{w:g}K/50K' for w in [.25,.5,1.]]),refs_at_half_K=ranges([f'0.5K/{r:g}K' for r in [40,50,60]]),joint_9=ranges(list(grid))),low_temperature=low_info)
summary['changes']={}
for s in ['SC1','SC2']:
    a=summary['samples'][s+'_before']['main'];b=summary['samples'][s+'_after']['main']
    c=dict(delta_T50_K=b['crossing_K']['0.5']-a['crossing_K']['0.5'],delta_T10_K=b['crossing_K']['0.1']-a['crossing_K']['0.1'],R50_after_over_before=b['Rref_ohm_sq']/a['Rref_ohm_sq'])
    for k,v in c.items():all_errors.append(abs(v-published[s+'_change'][k]))
    gs=[]
    for w in [.25,.5,1.]:
        for r in [40,50,60]:
            aa=calculate(bins([(float(v['x']),float(v['y'])) for v in read(ROOT/(s+'_before.csv')) if 0<float(v['x'])<80],w),r)
            bb=calculate(bins([(float(v['x']),float(v['y'])) for v in read(ROOT/(s+'_after.csv')) if 0<float(v['x'])<80],w),r)
            gs.append(dict(delta_T50_K=bb['crossing_K']['0.5']-aa['crossing_K']['0.5'],delta_T10_K=bb['crossing_K']['0.1']-aa['crossing_K']['0.1'],Rref_after_over_before=bb['Rref_ohm_sq']/aa['Rref_ohm_sq']))
    summary['changes'][s]=dict(main=c,joint_sensitivity_ranges={k:[min(v[k] for v in gs),max(v[k] for v in gs)] for k in gs[0]})
spin=json.loads((ROOT/'spin_simulation.json').read_text())
scan=[]
# Independent spin-1/2 Hamiltonian using bit flips, not supplied Pauli construction.
import numpy as np
for point in spin['scan']:
    j=point['Jperp_over_Jleg'];analytic=-(j+1)/2-math.sqrt(j*j-j+1)
    H=np.zeros((16,16))
    for state in range(16):
        for a,b,c in [(0,2,j),(1,3,j),(0,1,1),(2,3,1)]:
            same=((state>>a)&1)==((state>>b)&1)
            H[state,state]+=c*(.25 if same else -.25)
            if not same:H[state^(1<<a)^(1<<b),state]+=c/2
    eig=np.linalg.eigvalsh(H)
    scan.append(dict(Jp=j,analytic_E=analytic,stored_E=point['energy'],independent_E=float(eig[0]),analytic_minus_stored=analytic-point['energy'],gap_independent=float(eig[1]-eig[0])))
summary['spin_check']=dict(formula='E=-(Jp+1)/2-sqrt(Jp^2-Jp+1); Jleg=1; four spin-1/2 sites, bonds 02/13 rungs and 01/23 legs',scan=scan,max_abs_analytic_vs_stored=max(abs(p['analytic_minus_stored']) for p in scan),max_abs_analytic_vs_independent=max(abs(p['analytic_E']-p['independent_E']) for p in scan),target=spin['target'],aer_energy=spin['aer']['estimates']['energy'],warning='No charge, pairing or finite-T physics; does not establish superconductivity. Aer shots not rerun.')
summary['checks']=dict(max_abs_published_numeric_error=max(all_errors),compared_numeric_fields=len(all_errors),max_abs_binned_cell_error=max(binned_errors),compared_binned_cells=len(binned_errors),structural_errors=struct_errors,pass_at_1e_10=not struct_errors and max(all_errors+binned_errors)<1e-10)
summary['scope_status']=dict(fig1c_assignment='Taken from supplied CSV labels/manifest; original publisher caption not present in these transport files, so independently unverified.',replication='Numerical internal reproduction only, not new experimental replication.',retraction_refutation='Local prior independent_film_audit.md reports no verified retraction encountered, but incomplete external searches; no new literature search. Current status not cleared.',provenance_warning='october_paper.txt is Han et al. 2610.01757, whose Fig1c is an X-ray energy profile, not these curves; weak_links.txt is unrelated graph theory. Neither supports transport attribution.',interpretation='Normalized R(Tref) crossings are operational definitions, not onset or author zero-resistance Tc; absolute thresholds are scenarios, not measured instrument floors.')
print(json.dumps(summary,separators=(',',':'),allow_nan=False))
