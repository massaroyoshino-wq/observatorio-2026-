#!/usr/bin/env python3
"""Busca URLs públicas indexadas de Instagram, Facebook e X; NÃO infere apoio."""
import json,re,time,urllib.parse,urllib.request,xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime,timezone
OUT=Path(__file__).resolve().parents[1]/'data/social.json'
now=datetime.now(timezone.utc)
queries={'instagram':['site:instagram.com/p/ Lula 2026 empresários apoio','site:instagram.com/reel/ Lula 2026 livraria'],
'facebook':['site:facebook.com Lula 2026 empresários apoio','site:facebook.com Lula 2026 livrarias'],
'x':['site:x.com Lula 2026 empresários apoio','site:x.com Lula 2026 livrarias']}
def platform(href):
    try:p=urllib.parse.urlparse(href)
    except ValueError:return None
    host=(p.hostname or '').lower();path=p.path
    if p.scheme!='https':return None
    if host in ('instagram.com','www.instagram.com') and re.match(r'^/(p|reel|tv)/[\w-]+/?$',path):return 'instagram'
    if host in ('facebook.com','www.facebook.com','m.facebook.com'):
        if re.search(r'/posts/|/videos/|/share/p/|/share/v/',path):return 'facebook'
        if path in ('/permalink.php','/story.php') and 'story_fbid' in urllib.parse.parse_qs(p.query):return 'facebook'
    if host in ('x.com','www.x.com','twitter.com','www.twitter.com') and re.match(r'^/[\w]{1,15}/status/\d+',path):return 'x'
    return None
try:old=json.loads(OUT.read_text(encoding='utf-8'))
except (OSError,ValueError):old={}
found={x['url']:x for x in old.get('items',[]) if x.get('url') and platform(x['url'])}
errors=0
for network,qs in queries.items():
    for query in qs:
        url='https://www.bing.com/search?'+urllib.parse.urlencode({'q':query,'format':'rss','setlang':'pt-br'})
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (Observatorio2026/1.0)'})
            with urllib.request.urlopen(req,timeout=18) as resp:root=ET.fromstring(resp.read(1000000))
            for item in root.findall('./channel/item'):
                title=' '.join((item.findtext('title') or '').split())[:240]
                href=(item.findtext('link') or '').strip()
                if platform(href)==network and title:
                    found.setdefault(href,{'title':title,'url':href,'platform':network,'discoveredAt':now.date().isoformat()})
        except Exception as e:
            errors+=1;print('Busca social indisponível:',network,type(e).__name__,str(e)[:80])
        time.sleep(.4)
items=sorted(found.values(),key=lambda x:x.get('discoveredAt',''),reverse=True)[:150]
data={'schemaVersion':1,'checkedAt':now.strftime('%Y-%m-%dT%H:%M:%SZ'),'updatedAt':now.strftime('%Y-%m-%dT%H:%M:%SZ') if items else old.get('updatedAt'),
'status':f'URLs indexadas não verificadas; revisão humana obrigatória. Falhas de consulta: {errors}.','items':items}
OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('URLs em análise:',len(items))
