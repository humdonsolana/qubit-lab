import requests,pathlib,concurrent.futures,json,hashlib,time
urls={
'growth2026_pdf':'https://harvest.aps.org/v2/journals/articles/10.1103/3mjl-8p88/fulltext',
'nernst2025_vor_pdf':'https://harvest.aps.org/v2/journals/articles/10.1103/1yxb-1pl5/fulltext',
'dome2026_pdf':'https://arxiv.org/pdf/2605.31459',
'coherence2024_nature':'https://www.nature.com/articles/s41467-024-477 superconductivity',
'phonons2024_nature':'https://www.nature.com/articles/s41586-024-08118-0',
'83k2021_nature':'https://www.nature.com/articles/s41467-021-23106-y',
'interface2014_nature':'https://www.nature.com/articles/ncomms6044',
'100k2020_pdf':'https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.124.227002/fulltext',
'pnas_idconv':'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=10.1073/pnas.2602209123&format=json',
'dome2026_crossref':'https://api.crossref.org/works/10.1073/pnas.2608091123',
}
def f(kv):
 tag,url=kv
 if '477 ' in url:return
 try:
  r=requests.get(url,timeout=80);ext='pdf' if r.content.startswith(b'%PDF') else ('json' if 'json' in r.headers.get('content-type','') else 'html');p=pathlib.Path(f'lit_audit_snapshot_{tag}_20261013.{ext}');p.write_bytes(r.content)
  print(tag,r.status_code,len(r.content),ext,flush=True)
  return dict(file=str(p),url=url,status=r.status_code,bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest(),retrieved_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
 except Exception as e:print(tag,e)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: rows=list(ex.map(f,urls.items()))
p=pathlib.Path('lit_audit_manifest_20261013.json');p.write_text(json.dumps(json.loads(p.read_text())+[x for x in rows if x],indent=2))
from pypdf import PdfReader
for p in pathlib.Path('.').glob('lit_audit_snapshot_*.pdf'):
 if not p.with_suffix('.txt').exists():
  r=PdfReader(p);p.with_suffix('.txt').write_text('\n\n'.join(f'--- PAGE {i+1} ---\n'+q.extract_text() for i,q in enumerate(r.pages)))
