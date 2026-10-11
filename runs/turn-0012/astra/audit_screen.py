"""Reproducible audits of published numbers, not new EPC or ML training.
Downloads source arXiv HTML and checks 34-row table automatically. Kagome
inputs are manually transcribed with locations. All extrapolations labelled.
"""
import json,sys,hashlib,csv
from pathlib import Path
import numpy as np
from scipy.constants import R
from scipy.optimize import brentq
from scipy.stats import spearmanr
import requests
from bs4 import BeautifulSoup

def inv_mcmillan(theta,tc,mu=.13):
 L=np.log(theta/(1.45*tc));return (1.04+mu*L)/((1-.62*mu)*L-1.04)
def ad(lam,w,mu=.1):
 # Simplified Allen-Dynes form f1=f2=1, w expressed in K.
 return w/1.2*np.exp(-1.04*(1+lam)/(lam-mu*(1+.62*lam)))
def main(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 kag=[]
 for formula,tc,beta,theta,lambda_tab,lam,tc_body,tc_intro in [('YRu3B2',.81,.16,283.7,.44,.477,1.88,3.37),('LuRu3B2',.95,.48,453.,.41,.561,3.27,1.88)]:
  theta_calc=(12*np.pi**4*R*6/(5*beta*1e-3))**(1/3)
  # omega_log not provided here; invert simplified AD conditional on stated lam,tc.
  weff=tc_body/ad(lam,1.)
  kag.append(dict(formula=formula,tc_exp=tc,beta_mJ_molK4=beta,theta_prose_K=theta,theta_from_beta_K=theta_calc,lambda_exp_table=lambda_tab,lambda_inverse_using_prose_theta=inv_mcmillan(theta,tc),lambda_inverse_using_beta_theta=inv_mcmillan(theta_calc,tc),lambda_DFPT_body=lam,tc_DFPT_body=tc_body,tc_prediction_intro=tc_intro,exp_over_body=tc/tc_body,exp_over_intro=tc/tc_intro,conditional_effective_omega_K=weff,conditional_mu_fit=brentq(lambda mu:ad(lam,weff,mu)-tc,.1,.25)))
 result={'kagome':kag,'source':'arXiv:2512.16945v2 Table1, Sec II.2, Introduction, Sec III.3; PDF checked separately','warning':'Conflicting input labels are not silently corrected. Inverse McMillan lambda uses measured Tc, so is not independent validation of a Tc prediction. Two selected positive hits cannot calibrate general ML or family recall. Effective omega is algebraic, not extracted alpha2F.'}
 url='https://arxiv.org/html/2608.02426v1'; raw=requests.get(url,timeout=60);raw.raise_for_status();html=raw.text
 soup=BeautifulSoup(html,'html.parser');rows=[]
 for tr in soup.select('.ltx_tr'):
  td=tr.select(':scope > .ltx_td');vals=[t.get_text('',strip=True) for t in td]
  if len(vals)!=7 or not vals[0].startswith('mp-'):continue
  press=td[-1].find('sup'); pressure=float(press.get_text()) if press else 0.
  tc_str=td[-1].get_text('',strip=True)
  if press:tc_str=tc_str[:-len(press.get_text('',strip=True))]
  rows.append(dict(mp=vals[0],formula=vals[1],xi_sepr=float(vals[2]),xi_dfpt=float(vals[3]),chi_sepr=float(vals[4]),chi_dfpt=float(vals[5]),tc_table=float(tc_str),pressure_GPa=pressure))
 assert len(rows)==34,len(rows)
 for i,row in enumerate(rows):
  row['status']='experiment' if i<9 else ('predicted_synthesized_structure' if i<24 else 'predicted_unsynthesized_structure')
  row['BC_binary']=row['formula'].startswith('BC') or row['formula']=='B13C2'
  row['xi_dfpt_over_sepr']=row['xi_dfpt']/row['xi_sepr']
 # Table's BaBiO3 31 K is actually doped bismuthate context, not parent Tc.
 results={}
 for flag in [True,False]:
  rr=[r for r in rows if r['BC_binary']==flag];q=[r['xi_dfpt_over_sepr'] for r in rr]
  results[str(flag)]={'n':len(rr),'median_ratio':float(np.median(q)),'range_ratio':[min(q),max(q)]}
 a=next(r for r in rows if r['mp']=='mp-1080030');b=next(r for r in rows if r['mp']=='mp-1079661')
 result['orbital_screen']={'url':url,'html_sha256':hashlib.sha256(raw.content).hexdigest(),'n_rows':len(rows),'family_ratio_DFPT_over_SEPR':results,'max_listed_tc':max(r['tc_table'] for r in rows),'bc7_same_proxy_pair':[a,b],'minimax_constant_tc_error_for_pair_K':abs(a['tc_table']-b['tc_table'])/2,'warning':'34 selected positive rows only: ratios NOT calibrated over all 8833 screened metals. Xi is EPC response proxy, NOT lambda or Tc. Mixed experiment/prediction and pressure; BaBiO3 experimental entry is a doped-parent proxy. Pair bound assumes indistinguishable rounded proxy input; proxies actually differ by 0.1meV so this is illustrative constant-pair error, not mathematical impossibility for all models.'}
 with (out/'orbital_screen.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 (out/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main(sys.argv[1])
