#!/usr/bin/env python3
"""Reanalyse publisher's source data, NOT a new-composition Tc model.
Run: python analyze_nickelate_data.py --out /tmp/astra5/results
Requires numpy scipy pandas openpyxl requests. Source XLSX is fetched and hashed.
"""
import argparse, hashlib, io, json
from pathlib import Path
import numpy as np
import pandas as pd
import requests
from scipy.stats import linregress
URL='https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-024-08525-3/MediaObjects/41586_2024_8525_MOESM1_ESM.xlsx'

def curve(sheet,col):
    d=sheet.iloc[3:,[col,col+1]].apply(pd.to_numeric,errors='coerce').dropna()
    d.columns=['T','rho']; return d.sort_values('T')

def binned(d,width):
    x=d.copy(); x['bin']=np.round(x.T.values[0]/width).astype(int) if False else np.round(x['T']/width).astype(int)
    return x.groupby('bin')[['T','rho']].median().sort_values('T')

def interp(d,t):
    if t<d['T'].min() or t>d['T'].max(): return None
    return float(np.interp(t,d['T'],d['rho']))

def crossing(d,p,refT=50.):
    # Operational resistivity fraction, not author onset or measured zero.
    ref=interp(d,refT)
    if ref is None or ref<=0:return None
    z=d[d['T']<refT]; t=np.r_[z['T'].to_numpy(),refT]; y=np.r_[z['rho'].to_numpy()/ref,1.]
    ids=np.where((y[:-1]<=p)&(y[1:]>p))[0]
    if len(ids)==0:return None
    i=ids[-1]
    return float(t[i]+(p-y[i])*(t[i+1]-t[i])/(y[i+1]-y[i]))

def fit(d):
    x=d.iloc[:,0].to_numpy();y=d.iloc[:,1].to_numpy();r=linregress(x,y)
    preds=[]
    for i in range(len(x)):
        keep=np.arange(len(x))!=i;f=linregress(x[keep],y[keep]);preds.append(f.intercept+f.slope*x[i])
    return dict(n=len(x),slope_K_per_A=float(r.slope),R2=float(r.rvalue**2),LOO_RMSE_K=float(np.sqrt(np.mean((np.array(preds)-y)**2))))

def main(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    raw=requests.get(URL,timeout=120);raw.raise_for_status();data=raw.content
    (out/'publisher_source.xlsx').write_bytes(data)
    wb=pd.ExcelFile(io.BytesIO(data))
    a=pd.read_excel(wb,sheet_name='Figure 5a',header=None).iloc[2:].astype(float);a.columns=['a_A','reported_onset_K_or_zero_code']
    c=pd.read_excel(wb,sheet_name='Figure 5b',header=None).iloc[2:].astype(float);c.columns=['c_A','reported_onset_K_or_zero_code']
    a.to_csv(out/'figure5a.csv',index=False);c.to_csv(out/'figure5b.csv',index=False)
    rows=[];curves=[];observations=[]
    for sheet in ['Figure 1b','Figure 1c','Figure 2b']:
        d=pd.read_excel(wb,sheet_name=sheet,header=None)
        for col in range(0,d.shape[1],3):
            label=str(d.iloc[0,col+1]); rawcurve=curve(d,col)
            cc=rawcurve.copy();cc.insert(0,'sample',label);cc.insert(0,'sheet',sheet);curves.append(cc)
            for w in [0.1,0.25,0.5]:
                b=binned(rawcurve,w);r50=interp(b,50)
                r={'sheet':sheet,'sample':label,'bin_K':w,'raw_n':len(rawcurve),'Tmin_K':float(rawcurve['T'].min()),'rho50_mOhm_cm':r50}
                for p in [0.9,0.5,0.1,0.01]:r['T_fraction_'+str(p)+'_K']=crossing(b,p)
                for t in [5,10,20,100,200]:r['rho'+str(t)+'_mOhm_cm']=interp(b,t)
                r['rho5_over_rho50']=None if r['rho5_mOhm_cm'] is None else r['rho5_mOhm_cm']/r50
                rows.append(r)
            if sheet=='Figure 2b':
                observations.append(rows[-2])
    pd.DataFrame(rows).to_csv(out/'operational_thresholds.csv',index=False)
    pd.concat(curves).to_csv(out/'extracted_raw_curves.csv',index=False)
    positive=c[c.iloc[:,1]>0]
    duplicate=[];sse=0
    for x,g in c.groupby('c_A'):
        if len(g)>1:
            y=g.iloc[:,1].to_numpy();sse+=float(np.sum((y-y.mean())**2))
            duplicate.append(dict(c_A=x,onsets_K=y.tolist(),minimum_worst_residual_K=float(np.ptp(y)/2)))
    summary={'source_url':URL,'source_sha256':hashlib.sha256(data).hexdigest(),'source_bytes':len(data),
      'criterion':'Source Fig5 Tc values are author onset; zero entries encode no observed transition, not proven physical Tc=0.',
      'a_rows':a.to_dict('records'),'c_duplicate_rows':duplicate,
      'c_positive_only_descriptive_linear_fit':fit(positive),
      'c_zero_coded_naive_fit_NOT_valid_Tc_regression':fit(c),
      'any_deterministic_c_only_fit_RMSE_lower_bound_all_rows_K':float(np.sqrt(sse/len(c))),
      'aging_025K_bins':observations,
      'threshold_definition':'Highest warming crossing rho(T)/rho(50K)=p after median temperature binning. Linear interpolation; these are not author onsets or measured zeros. Null means no observed crossing within data, not Tc=0.',
      'limitations':['Repeated c values are equal at published precision; not proof of microscopically identical strain.','No uncertainties/covariates or held-out composition validation. LOO rows are not independent experiments.','No causal strain coefficient, oxygen diffusion constant, vacancy density, new Tc, or bulk Meissner fraction inferred.','Binning repeated-temperature data may combine warming/cooling sweeps; no instrument detection limit available.']}
    assert len(a)==5 and len(c)==18 and len(positive)==11
    assert abs(duplicate[-1]['minimum_worst_residual_K']-8.12)<1e-9
    for r in rows:
        vals=[r['T_fraction_'+str(p)+'_K'] for p in [0.9,0.5,0.1,0.01]]
        vals=[v for v in vals if v is not None]
        assert all(vals[i]>=vals[i+1] for i in range(len(vals)-1))
    (out/'summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
    print(json.dumps(summary,indent=2,allow_nan=False))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',default='outputs');args=p.parse_args();main(args.out)
