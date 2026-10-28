#!/usr/bin/env python3
"""Coleta pistas jornalísticas; NÃO confirma declarações de apoio."""
import json,re,time,urllib.parse,urllib.request,xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path
from datetime import datetime,timezone,timedelta
OUT=Path(__file__).resolve().parents[1]/'data/news.json'
QUERIES=['"Lula" "2026" "empresários" "apoio"','"Lula" "2026" "livrarias" "manifesto"','"Lula" "2026" "empresário" "declarou apoio"','"Lula" "2026" "comerciantes" "lista"']
now=datetime.now(timezone.utc)
found={}
for query in QUERIES:
    url='https://news.google.com/rss/search?'+urllib.parse.urlencode({'q':query+' after:2026-08-01','hl':'pt-BR','gl':'BR','ceid':'BR:pt-419'})
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (Observatorio2026/1.0)'})
        with urllib.request.urlopen(req,timeout=20) as resp: root=ET.fromstring(resp.read(1200000))
        for item in root.findall('./channel/item'):
            title=(item.findtext('title') or '').strip()[:250]
            href=(item.findtext('link') or '').strip()
            raw=(item.findtext('pubDate') or '').strip()
            try:published=parsedate_to_datetime(raw).astimezone(timezone.utc)
            except (ValueError,TypeError):continue
            if published<now-timedelta(days=21) or not href.startswith('https://') or not re.search('lula',title,re.I):continue
            source=item.find('source')
            publisher=source.text if source is not None and source.text else ''
            key=re.sub(r'\W+',' ',title.casefold()).strip()
            found[key]={'title':title,'url':href,'source':publisher,'published':published.strftime('%Y-%m-%d')}
    except Exception as e:print('Busca jornalística falhou:',type(e).__name__,str(e)[:100])
    time.sleep(.4)
if found:
    data={'updatedAt':now.strftime('%Y-%m-%dT%H:%M:%SZ'),'status':'Resultados automáticos em análise: não constituem prova de apoio.','items':sorted(found.values(),key=lambda x:x['published'],reverse=True)[:80]}
    OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Novas notícias capturadas:',len(data['items']))
else:
    print('Sem novas notícias verificáveis no feed; mantidos os dados anteriores.')
