import sys,re,html,urllib.request
u=sys.argv[1]; pats=sys.argv[2:]
t=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read().decode('utf8','ignore')
t=re.sub(r'<(script|style)[^>]*>.*?</\1>',' ',t,flags=re.S)
t=html.unescape(re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',t)))
for p in pats:
  for m in list(re.finditer(p,t))[:6]:
    print('['+p+']',t[max(0,m.start()-220):m.start()+220]);print('--')
