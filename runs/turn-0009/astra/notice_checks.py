"""Limited live primary metadata/notice checks; not proof of absence of disputes.
No web page instructions are executed. Store only status/notice metadata, no contacts.
"""
import requests,json,sys
from pathlib import Path
from bs4 import BeautifulSoup
terms=['Mg2IrH6','MgAlFeH6','LaSc2H24'];rows=[]
for term in terms:
 for url in ['https://pubpeer.com/search?q='+term,'https://retractionwatch.com/?s='+term]:
  try:
   r=requests.get(url,timeout=25);s=BeautifulSoup(r.text,'html.parser');text=s.get_text(' ',strip=True)
   rows.append({'query':term,'url':url,'status':r.status_code,'title':s.title.get_text() if s.title else None,'query_term_present':term.lower() in text.lower(),'no_results_text':any(x in text.lower() for x in ['nothing found','no results found','no posts found']),'interpretation':'Status/landing-page check only; no absence claim from blocked or ambiguous results.'})
  except Exception as e:rows.append({'query':term,'url':url,'error':type(e).__name__})
for doi in ['10.1038/s41524-024-01214-9','10.1038/s41524-026-02040-x','10.1103/PhysRevLett.132.166001','10.1021/jacs.6c08889']:
 try:
  r=requests.get('https://api.crossref.org/works/'+doi,timeout=25);d=r.json()['message'];rows.append({'doi':doi,'status':r.status_code,'title':d.get('title'),'update_to':d.get('update-to',[]),'relation':d.get('relation',{}),'interpretation':'Metadata at lookup; lack of listed notice is not independent validation.'})
 except Exception as e:rows.append({'doi':doi,'error':type(e).__name__})
out=Path(sys.argv[1]);out.mkdir(exist_ok=True,parents=True);(out/'notice_checks.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
