"""Discovery-only metadata retrieval. Emits JSON to stdout; indexes are not experimental evidence.
The lab run_shell identity cannot create files in this astra folder; use write_file to persist outputs.
"""
import json
from datetime import datetime, timezone
import requests
out={'retrieved_utc':datetime.now(timezone.utc).isoformat(),'cutoff':'2026-10-10','requests':[]}
def get(url,params=None):
 r=requests.get(url,params=params,timeout=60)
 row={'url':r.url,'status':r.status_code}
 try:row['data']=r.json()
 except ValueError:row['error']=r.text[:200]
 out['requests'].append(row)
base='https://www.ebi.ac.uk/europepmc/webservices/rest/'
for q in ['DOI:10.1073/pnas.2536178123','(Hg1223 OR "Hg-1223" OR "HgBa2Ca2Cu3O8") AND (quench OR quenched OR replication OR reproduction) AND FIRST_PDATE:[2026-01-01 TO 2026-10-10]','("pressure quench" OR "pressure-quench" OR "pressure quenching") AND (Bi2212 OR "Bi-2212" OR Hg1223 OR "Hg-1223") AND FIRST_PDATE:[2022-01-01 TO 2023-12-31]']:
 get(base+'search',{'query':q,'format':'json','pageSize':100,'resultType':'core'})
get(base+'MED/41802058/citations',{'format':'json','pageSize':100})
for wid in ['W7134283102','W3167352516']:
 get('https://api.openalex.org/works',{'filter':'cites:'+wid+',to_publication_date:2026-10-10','per-page':100})
for doi in ['10.1007/s10948-021-06117-0','10.1007/s10948-022-06162-3','10.1021/jacs.6c10866','10.1063/5.0338010','10.1016/j.physrep.2026.06.003','10.1088/1361-6633/ae9aae','10.1088/1361-648x/ae8fac','10.1103/qqvw-ltth','10.1088/1757-899X/1302/1/012010']:
 get('https://api.crossref.org/works/'+doi)
print(json.dumps(out,indent=2))
