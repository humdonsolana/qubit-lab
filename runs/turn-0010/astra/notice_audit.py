"""Bounded public metadata/notice audit, not proof of no disputes.
Successful Retraction Watch zero-result searches are site-search only.
PubPeer403 and search-engine JS shells do not count as negative results.
"""
import json,sys
from pathlib import Path
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
DOIS=['10.1038/s41563-026-02750-z','10.1021/acs.nanolett.6c03024','10.1093/nsr/nwag151','10.1002/adma.202510394']
r={'audit_date':'2026-10-11','crossref':{},'retraction_watch':{},'pubpeer':{}}
for d in DOIS:
 try:
  x=requests.get('https://api.crossref.org/works/'+quote(d,safe=''),timeout=30);j=x.json()['message']
  r['crossref'][d]={'status':x.status_code,'title':j.get('title'),'published':j.get('published'),'update_to':j.get('update-to'),'relation':j.get('relation')}
 except Exception as e:r['crossref'][d]={'error':str(e)}
for query in ['bilayer nickelate','Interlayer hybridization','Mg2IrH6']:
 try:
  x=requests.get('https://retractionwatch.com/',params={'s':query},timeout=30);s=BeautifulSoup(x.text,'html.parser');m=s.find('main') or s;r['retraction_watch'][query]={'status':x.status_code,'excerpt':m.get_text(' ',strip=True)[:220]}
 except Exception as e:r['retraction_watch'][query]={'error':str(e)}
for d in DOIS[:2]:
 try:x=requests.get('https://pubpeer.com/search',params={'q':d},timeout=30);r['pubpeer'][d]={'status':x.status_code,'usable':x.status_code==200}
 except Exception as e:r['pubpeer'][d]={'error':str(e)}
r['limits']='No update field does not mean no correction. PubPeer unavailable; general Google queries returned JS shells. No comprehensive failed replication clearance. See independent_film_audit.md for formal peer review criticisms and controls.'
Path(sys.argv[1]).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
