"""Primary-source metadata searches; archive results, don't equate no hits to no disputes."""
from pathlib import Path
import requests,json,time,xml.etree.ElementTree as ET
p=Path('sources');p.mkdir(exist_ok=True)
queries={
'latest_fese':'all:FeSe AND submittedDate:[202401010000 TO 202610132359]',
'nernst':'all:FeSe AND all:Nernst',
'double_interface':'all:FeSe AND (all:sandwich OR all:superlattice OR all:bilayer)',
'fe_disputes':'all:FeSe AND (all:retraction OR all:Comment OR all:replication OR all:reproducibility)',
'strain_disputes':'all:"2602209123" OR (all:FeSe AND all:"Jia" AND all:Comment)',
'100k':'all:FeSe AND (all:"100 K" OR all:"100K")'}
report={}
for name,q in queries.items():
 try:
  r=requests.get('https://export.arxiv.org/api/query',params={'search_query':q,'start':0,'max_results':60,'sortBy':'submittedDate','sortOrder':'descending'},timeout=70)
  (p/(name+'_arxiv.xml')).write_text(r.text)
  root=ET.fromstring(r.text); ns={'a':'http://www.w3.org/2005/Atom','arxiv':'http://arxiv.org/schemas/atom'}
  entries=[]
  for e in root.findall('a:entry',ns):
   d={k:e.findtext('a:'+k,default='',namespaces=ns).strip() for k in ['id','title','published','updated','summary']}; d['doi']=e.findtext('arxiv:doi',default='',namespaces=ns);entries.append(d)
  report[name]={'status':r.status_code,'query':q,'entries':entries};print(name,len(entries))
 except Exception as e:report[name]={'error':str(e)};print(name,str(e))
 time.sleep(3)
for name,doi in [('strain_crossref','10.1073/pnas.2602209123'),('nernst_crossref','10.1103/1yxb-1pl5'),('100k_crossref','10.1038/nmat4153')]:
 try:
  r=requests.get('https://api.crossref.org/works/'+doi,timeout=45);(p/(name+'.json')).write_text(r.text);d=r.json().get('message',{});report[name]={'doi':doi,'status':r.status_code,'title':d.get('title'),'published':d.get('published'),'relation':d.get('relation'),'update_to':d.get('update-to')};print(name,report[name])
 except Exception as e: report[name]={'error':str(e)}
Path('outputs/source_audit.json').write_text(json.dumps(report,indent=2))
