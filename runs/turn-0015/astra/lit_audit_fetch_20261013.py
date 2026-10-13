import requests, pathlib, json, hashlib, time
root=pathlib.Path('.')
urls={
'pnas2026_arxiv':'https://arxiv.org/pdf/2607.27104',
'nernst2025_arxiv':'https://arxiv.org/pdf/2508.11018',
'100k2015_arxiv':'https://arxiv.org/pdf/1406.3435',
'pnas2026_pmc':'https://pmc.ncbi.nlm.nih.gov/articles/PMC13273281/',
'pnas2026_pubmed':'https://pubmed.ncbi.nlm.nih.gov/42263135/',
'nernst2025_aps':'https://journals.aps.org/prb/abstract/10.1103/1yxb-1pl5',
'growth2026_aps':'https://journals.aps.org/prmaterials/abstract/10.1103/3mjl-8p88',
'dome2026_pmc':'https://pmc.ncbi.nlm.nih.gov/articles/PMC13506021/',
}
manifest=[]
for tag,url in urls.items():
 try:
  r=requests.get(url,timeout=65); ext='pdf' if r.content.startswith(b'%PDF') else 'html'; p=root/f'lit_audit_snapshot_{tag}_20261013.{ext}'; p.write_bytes(r.content)
  manifest.append(dict(file=str(p),url=url,status=r.status_code,bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest(),retrieved_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())))
  print(tag,r.status_code,len(r.content),ext,flush=True)
 except Exception as e: manifest.append(dict(url=url,error=str(e)))
(root/'lit_audit_manifest_20261013.json').write_text(json.dumps(manifest,indent=2))
