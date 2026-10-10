import urllib.request,urllib.parse,sys,time
import xml.etree.ElementTree as ET
ns={'a':'http://www.w3.org/2005/Atom'}
def q(s,n=200):
    s=s+' AND submittedDate:[202501010000 TO 202612312359]'
    u='http://export.arxiv.org/api/query?'+urllib.parse.urlencode({'search_query':s,'sortBy':'submittedDate','sortOrder':'descending','max_results':n})
    r=urllib.request.urlopen(u,timeout=90).read()
    t=ET.fromstring(r)
    for e in t.findall('a:entry',ns):
        p=e.find('a:published',ns).text[:10]
        i=e.find('a:id',ns).text.split('/abs/')[-1]
        ti=' '.join(e.find('a:title',ns).text.split())
        print(p,i,ti)
for s in sys.argv[1:]:
    print('==',s)
    try: q(s)
    except Exception as ex: print('ERR',ex)
    time.sleep(3)
