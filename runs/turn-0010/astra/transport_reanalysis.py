"""Reanalyse measured Fig1b/c transport from Zhang et al. 2026.
No author-fit curves; operational normalized thresholds, NOT author Tc or zero.
Downloads are hashed, binned to 0.5K medians, interpolated versus R(50K).
Instrumental near-zero thresholds are sensitivity scenarios, not measured floor.
"""
import hashlib,json,sys,io
from pathlib import Path
import requests,numpy as np,pandas as pd
SOURCES={'SC1_before':67351044,'SC1_after':67351038,'SC2_before':67351053,'SC2_after':67351047}
def crossing(t,r,threshold):
 # Follow cooling from normal state: first downward crossing, no monotonic fit.
 for i in range(len(t)-1,0,-1):
  if r[i]>=threshold and r[i-1]<threshold:
   return float(t[i-1]+(threshold-r[i-1])*(t[i]-t[i-1])/(r[i]-r[i-1]))
 return None

def process(df,bw,ref=50.):
 df=df.dropna();df=df[(df.x>0)&(df.x<80)].copy();df['bin']=np.round(df.x/bw)
 b=df.groupby('bin')[['x','y']].median().sort_values('x');t=b.x.to_numpy();r=b.y.to_numpy();rref=float(np.interp(ref,t,r))
 c={str(f):crossing(t[t<=ref],r[t<=ref],f*rref) for f in [.9,.5,.1,.01]}
 z={str(v):crossing(t[t<=ref],r[t<=ref],v) for v in [.01,.1,1.]}
 return {'Rref_ohm_sq':rref,'reference_T_K':ref,'crossing_K':c,'width90_10_K':c['0.9']-c['0.1'] if c['0.9'] and c['0.1'] else None,'near_zero_threshold_ohm_sq_crossing_K':z,'binned_points':len(b),'minT_K':float(t.min()),'R_at_5K_ohm_sq':float(np.interp(5,t,r))},b

def main():
 out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True);res={};meta={};table=[]
 for name,id in SOURCES.items():
  url=f'https://ndownloader.figshare.com/files/{id}';rr=requests.get(url,timeout=60);rr.raise_for_status();raw=rr.content
  (out/(name+'.csv')).write_bytes(raw);df=pd.read_csv(io.BytesIO(raw))
  meta[name]={'url':url,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'nraw':len(df)}
  a,b=process(df,.5);res[name]={'main':a,'bin_sensitivity':{str(w):process(df,w)[0] for w in [.25,1.]},'reference_sensitivity':{str(ref):process(df,.5,ref)[0] for ref in [40,60]}}
  b['sample']=name;table.append(b)
 for name in ['SC1','SC2']:
  a=res[name+'_before']['main'];b=res[name+'_after']['main'];res[name+'_change']={'delta_T50_K':b['crossing_K']['0.5']-a['crossing_K']['0.5'],'delta_T10_K':b['crossing_K']['0.1']-a['crossing_K']['0.1'],'R50_after_over_before':b['Rref_ohm_sq']/a['Rref_ohm_sq']}
 pd.concat(table).to_csv(out/'binned_transport.csv',index=False)
 (out/'transport_manifest.json').write_text(json.dumps(meta,indent=2)+'\n');(out/'transport_results.json').write_text(json.dumps(res,indent=2)+'\n')
 print(json.dumps({'manifest':meta,'main':{k:(v['main'] if 'main' in v else v) for k,v in res.items()}},indent=2))
if __name__=='__main__':main()
