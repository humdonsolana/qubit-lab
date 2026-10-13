import requests,json,pathlib,concurrent.futures
queries={
'latest2026':'FeSe SrTiO3 superconductivity 2026',
'latest2025':'FeSe interface superconductivity 2025',
'latest2024':'FeSe interface superconductivity 2024',
'sandwich':'FeSe SrTiO3 sandwich superconductivity',
'doubleinterface':'FeSe double interface superconductivity',
'100kcomment':'Comment superconductivity single-layer films FeSe transition temperature above 100 K',
'100kreplication':'FeSe 109 K reproducibility four probe',
}
def f(item):
 k,q=item; u='https://api.crossref.org/works'; par={'query':q,'rows':15,'select':'DOI,title,published,author,type','filter':'from-pub-date:2014-01-01'}
 r=requests.get(u,params=par,timeout=90); pathlib.Path(f'lit_audit_search_{k}_crossref_20261013.json').write_text(r.text)
 try:
  print('\nQUERY',k,q)
  for x in r.json()['message']['items']:print(x['DOI'],x.get('published'),x.get('title'))
 except: print(r.status_code,r.text[:100])
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(f,queries.items()))
