"""Independent controls for data extraction, balanced chemistry and solver folding."""
import sys,json,hashlib
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
import requests
from bs4 import BeautifulSoup
from pymatgen.core import Composition
from spectral_gate import fit_modes,eliashberg_eigen,tc_e,KB_MEV
from pair_transfer_benchmark import analyze

def main(out):
 out=Path(out);out.mkdir(exist_ok=True,parents=True)
 raw=requests.get('https://www.nature.com/articles/s41699-025-00590-0/tables/2').content
 soup=BeautifulSoup(raw,'html.parser');table={}
 for tr in soup.select('tr'):
  cells=[c.get_text(' ',strip=True) for c in tr.find_all(['td','th'])]
  if cells and cells[0] in ['Sc','Y','V','Nb']:
   table[cells[0]]=[float(c.split()[0].replace('−','-')) for c in cells[1:]]
 stored=json.loads((out/'hydrogen_retention.json').read_text());checks=[]
 for M,values in table.items():
  for n,ef in enumerate(values,1):
   assert ef==stored['metals'][M]['formation_eV_per_atom'][str(n)]
  for n in [1,2,3]:
   p=Composition(f'{M}2B2H4');a=Composition(f'{M}2B2H{n}');h=Composition('H2')*((4-n)/2)
   assert p==a+h
   d=values[n-1]*a.num_atoms-values[3]*p.num_atoms
   assert abs(d-stored['metals'][M]['dehydrogenation_reactions'][n-1]['delta_E_eV_per_M2B2'])<1e-12
   checks.append([M,n,d])
 # Rebuild signed Matsubara matrix independently; positive-frequency folding
 # must give the same maximum even-frequency eigenvalue.
 N=80;T=90.;l=3.33;modes=fit_modes(13.88,41.16,.6);cs=l*np.array([.6,.4])
 ix=np.arange(-N,N);omega=(2*ix+1)*np.pi*KB_MEV*T
 diff=omega[:,None]-omega[None,:]
 lam=sum(c*w*w/(w*w+diff*diff) for w,c in zip(modes,cs))
 # Analytic normal Z independently checked by long signed-frequency sum.
 m=np.arange(-100000,100000);wm=(2*m+1)*np.pi*KB_MEV*T
 zs=[]
 for w in omega:
  z=1+np.pi*KB_MEV*T/w*sum(c*v*v*np.sum(np.sign(wm)/(v*v+(w-wm)**2)) for v,c in zip(modes,cs))
  zs.append(z)
 theta=(abs(omega)<10*max(modes));den=np.sqrt(abs(omega)*np.array(zs))
 mat=np.pi*KB_MEV*T*(lam- mu_outer(theta,.1))/np.outer(den,den)
 ev=eigh(mat,subset_by_index=[2*N-1,2*N-1],eigvals_only=True)[0]
 folded=eliashberg_eigen(T,modes,cs,.1,N)
 assert abs(ev-folded)<1e-8
 # Rerun exact submitted QASM dialect (u3 vs exported u); verify Aer counts
 # algorithmically, not assume the dialect replacement changes no unitary.
 from qiskit import qasm2,transpile
 from qiskit_aer import AerSimulator
 qasm=(out/'pair_transfer.qasm').read_text().replace('u(','u3(')
 (out/'submitted.qasm').write_text(qasm)
 qc=qasm2.loads(qasm);sim=AerSimulator();cts=sim.run(transpile(qc,sim),shots=8192,seed_simulator=13).result().get_counts()
 orig=json.loads((out/'pair_transfer_simulation.json').read_text());assert cts==orig['aer_counts']
 result={'table_html_sha256':hashlib.sha256(raw).hexdigest(),'table16_values_match':True,'balanced12_reactions_match':True,'reaction_checks':checks,'signed_eigenvalue':ev,'folded_eigenvalue':folded,'folding_error':abs(ev-folded),'submitted_u3_qasm_aer_identical_counts':True}
 (out/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
def mu_outer(theta,mu):return mu*np.outer(theta,theta)
if __name__=='__main__':main(sys.argv[1])
