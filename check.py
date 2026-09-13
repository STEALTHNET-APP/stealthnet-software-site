#!/usr/bin/env python3
"""Check shipped pages, counterpart languages, internal links and asset paths."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.lang=None
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='html':self.lang=a.get('lang')
  if 'id' in a:self.ids.add(a['id'])
  for k in ('href','src'):
   if k in a:self.links.append(a[k])
root=Path(__file__).resolve().parent;pages={};errors=[]
for f in [root/'index.html',root/'404.html',*root.glob('docs/**/*.html'),*root.glob('ru/**/*.html')]:
 p=Page();p.feed(f.read_text());pages[f]=p
 if p.lang not in ('en','ru'):errors.append(f'{f}: missing language')
for f,p in pages.items():
 for link in p.links:
  u=urlsplit(link)
  if u.scheme or link.startswith('//'):continue
  dest=(root/u.path.lstrip('/') if u.path.startswith('/') else f.parent/u.path) if u.path else f
  if dest.is_dir():dest=dest/'index.html'
  if not dest.exists():errors.append(f'{f.relative_to(root)}: missing {link}')
  elif u.fragment and dest in pages and unquote(u.fragment) not in pages[dest].ids:errors.append(f'{f.relative_to(root)}: missing anchor {link}')
 for link in p.links:
  if link.startswith('/ru/docs/') or (p.lang=='ru' and link.startswith('/docs/')):
   assert (root/link.lstrip('/')).is_file()
for l in ('en','ru'):
 data=json.loads((root/'assets'/f'search.{l}.json').read_text())
 for row in data:
  if root/row['url'].lstrip('/') not in pages:errors.append('Search target missing: '+row['url'])
assert (root/'CNAME').read_text().strip()=='stealthnet.software'
assert not errors,'\n'.join(errors)
print('PASS',len(pages),'pages: internal links, fragments, language, search destinations and CNAME')
