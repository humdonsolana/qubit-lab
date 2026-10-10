#!/usr/bin/env python3
"""Independent local-workbook audit; never imports or executes audited routines.
Run python independent_validation.py --source /tmp/astra5/results --out /tmp/astra5/validation
"""
import argparse, hashlib, json
from pathlib import Path
import numpy as np
import pandas as pd

def interp(points, target):
    x,y=points[:,0],points[:,1]
    if target<x[0] or target>x[-1]: return None
    k=int(np.searchsorted(x,target,side='right'))
    if k==len(x): return float(y[-1])
    j=k-1
    return float(y[j]+(target-x[j])*(y[k]-y[j])/(x[k]-x[j]))

def thresholds(points, p):
    ref=interp(points,50.)
    if ref is None or ref<=0: return None,0
    below=points[points[:,0]<50.]
    seq=np.vstack([below,[50.,ref]])
    roots=[]
    for (t0,r0),(t1,r1) in zip(seq[:-1],seq[1:]):
        if r0<=p*ref and r1>p*ref:
            roots.append(float(t0+(p*ref-r0)*(t1-t0)/(r1-r0)))
    return (roots[-1] if roots else None),len(roots)

def fit(x,y):
    xc=x-x.mean(); yc=y-y.mean()
    slope=float(np.dot(xc,yc)/np.dot(xc,xc)); intercept=float(y.mean()-slope*x.mean())
    predicted=intercept+slope*x
    loo=[]
    for i in range(len(x)):
        keep=np.arange(len(x))!=i
        design=np.column_stack([np.ones(keep.sum()),x[keep]])
        beta=np.linalg.lstsq(design,y[keep],rcond=None)[0]
        loo.append(float(np.array([1.,x[i]])@beta-y[i]))
    return {'n':len(x),'slope_K_per_A':slope,'intercept_K':intercept,'R2':float(1-np.sum((y-predicted)**2)/np.dot(yc,yc)),'LOO_RMSE_K':float(np.sqrt(np.mean(np.square(loo))))}

def main(source,out):
    source=Path(source);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    summary=json.loads((source/'summary.json').read_text())
    raw=(source/'publisher_source.xlsx').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==summary['source_sha256'] and len(raw)==summary['source_bytes']
    wb=pd.ExcelFile(source/'publisher_source.xlsx')
    for sheet,name in [('Figure 5a','figure5a.csv'),('Figure 5b','figure5b.csv')]:
        data=pd.read_excel(wb,sheet_name=sheet,header=None).iloc[2:].to_numpy(dtype=float)
        archived=pd.read_csv(source/name).to_numpy()
        np.testing.assert_array_equal(data,archived)
    c=pd.read_excel(wb,sheet_name='Figure 5b',header=None).iloc[2:].to_numpy(dtype=float)
    duplicates=[];sse=0.
    for x in np.unique(c[:,0]):
        y=c[c[:,0]==x,1]
        if len(y)>1:
            term=float(np.sum((y-y.mean())**2));sse+=term
            duplicates.append({'c_A':float(x),'onsets_K':y.tolist(),'minimax_residual_K':float((max(y)-min(y))/2),'irreducible_SSE_K2':term})
    positive=c[c[:,1]>0]; regression=fit(positive[:,0],positive[:,1]); bound=float(np.sqrt(sse/len(c)))
    for key in ['slope_K_per_A','R2','LOO_RMSE_K']:
        assert abs(regression[key]-summary['c_positive_only_descriptive_linear_fit'][key])<1e-9
    assert abs(bound-summary['any_deterministic_c_only_fit_RMSE_lower_bound_all_rows_K'])<1e-12
    d=pd.read_excel(wb,sheet_name='Figure 1c',header=None)
    missing=[]
    for col in range(0,d.shape[1],3):
        if str(d.iloc[0,col+1])=='A11':
            temperature=pd.to_numeric(d.iloc[3:,col],errors='coerce')
            resistivity=pd.to_numeric(d.iloc[3:,col+1],errors='coerce')
            missing.append({'sample':'A11','numeric_temperature_cells':int(temperature.notna().sum()),'numeric_resistivity_cells':int(resistivity.notna().sum()),'paired_rows':int((temperature.notna() & resistivity.notna()).sum())})
    assert len(missing)==1 and missing[0]['numeric_resistivity_cells']==0
    op=pd.read_csv(source/'operational_thresholds.csv')
    assert not ((op.sheet=='Figure 1c') & (op['sample']=='A11')).any()
    d=pd.read_excel(wb,sheet_name='Figure 2b',header=None)
    rows=[]; maxdiff=0.;allthreshold_maxdiff=0.; checks=0
    for col in range(0,d.shape[1],3):
        label=str(d.iloc[0,col+1]); pair=d.iloc[3:,[col,col+1]].apply(pd.to_numeric,errors='coerce').dropna()
        pair.columns=['T','rho'];points=pair.to_numpy();points=points[np.argsort(points[:,0],kind='stable')]
        rawhalf,count=thresholds(points,.5)
        record={'sample':label,'raw_n':len(points),'duplicate_temperature_rows':int(len(points)-len(np.unique(points[:,0]))),'raw_rho50':interp(points,50.),'raw_half_K':rawhalf,'raw_half_upcrossings':count}
        for width in [.1,.25,.5]:
            # Independent Python group construction, medians of T and rho separately.
            groups={}
            for t,r in points: groups.setdefault(int(round(float(t/width))),[]).append((t,r))
            b=np.array([np.median(v,axis=0) for v in groups.values()]);b=b[np.argsort(b[:,0],kind='stable')]
            archived=op[(op.sheet=='Figure 2b') & (op['sample']==label) & (op.bin_K==width)].iloc[0]
            half,ncross=thresholds(b,.5);diff=abs(half-float(archived['T_fraction_0.5_K']));maxdiff=max(maxdiff,diff)
            assert diff<1e-10
            record[f'bin_{width}_half_K']=half;record[f'bin_{width}_minus_raw_K']=half-rawhalf
            for p in [.9,.5,.1,.01]:
                value,_=thresholds(b,p);expected=archived[f'T_fraction_{p}_K'];checks+=1
                if value is None: assert pd.isna(expected)
                else:
                    delta=abs(value-expected);allthreshold_maxdiff=max(allthreshold_maxdiff,delta);assert delta<1e-10
        rows.append(record)
    pd.DataFrame(rows).to_csv(out/'aging_independent.csv',index=False)
    result={'source_sha256':hashlib.sha256(raw).hexdigest(),'source_bytes':len(raw),'duplicates':duplicates,'duplicate_SSE_K2':sse,'all_rows_RMSE_lower_bound_K':bound,'positive_only_RMSE_duplicate_bound_K':float(np.sqrt(sse/len(positive))),'positive_only_descriptive_fit':regression,'missing_Figure1c':missing,'aging':rows,'aging_binned_half_max_abs_difference_K':maxdiff,'aging_all_fraction_checks':checks,'aging_all_fraction_max_abs_difference_K':allthreshold_maxdiff,'figure5_csvs_exact_numeric_match':True}
    (out/'independent_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    for name in ['summary.json','figure5a.csv','figure5b.csv','operational_thresholds.csv','publisher_source.xlsx','extracted_raw_curves.csv']:
        data=(source/name).read_bytes();print('FILE',name,len(data),hashlib.sha256(data).hexdigest())
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',required=True);parser.add_argument('--out',required=True);a=parser.parse_args();main(a.source,a.out)
