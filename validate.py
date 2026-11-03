from pathlib import Path
import re,json
from html.parser import HTMLParser
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
root=Path(__file__).parent
expected=re.findall(r'^- \[ \] (.+)$',(root/'content/checklist.md').read_text(),re.M)
data=json.loads((root/'content/curriculum.json').read_text());items=[x for g in data for x in g['items']]
assert [x['objective'] for x in items]==expected
assert len(items)==117
for group in data:
 key=group['key']
 rows=(root/'content'/('cross.txt' if key=='cross' else 'ch'+key+'.txt')).read_text().splitlines()
 rows=[r for r in rows if r.strip()]
 for row,item in zip(rows,group['items']):
  fields=row.split('~')
  expected_answer=fields[5].split('^')[int(fields[6])]
  assert item['options'][item['answer']]==expected_answer,(item['id'],'answer changed')

class Page(HTMLParser):
 def __init__(self,p):super().__init__();self.p=p;self.links=[];self.classes=[];self.objective=False;self.objective_depth=0;self.objective_text=''
 def handle_starttag(self,t,attrs):
  a=dict(attrs);self.classes.extend(a.get('class','').split())
  if a.get('class')=='objective':self.objective=True
  if self.objective and t=='p':self.objective_depth=1
  for name in ('href','src'):
   v=a.get(name,'')
   if v and not v.startswith(('http:','https:','#','mailto:','data:')):self.links.append(self.p.parent/urlsplit(v).path)
 def handle_endtag(self,t):
  if t=='p':self.objective_depth=0
  if t=='section':self.objective=False
 def handle_data(self,d):
  if self.objective and self.objective_depth:self.objective_text+=d
for item_index,it in enumerate(items):
 p=root/'dist/lessons'/it['file'];s=p.read_text();page=Page(p);page.feed(s)
 for cl in ('explain','worked-example','question'):assert page.classes.count(cl)==1,(p,cl)
 assert len(it['options'])==4 and 0<=it['answer']<4
 assert all(it[x].strip() for x in ('en','zh','example','question','why'))
 normalized=re.sub(r'\*\*|'+chr(96),'',it['objective'])
 assert page.objective_text==normalized,(p,page.objective_text,normalized)
 if item_index+1<len(items):assert f'href="{items[item_index+1]["file"]}">Next' in s,(p,'next order')
 if item_index:assert f'href="{items[item_index-1]["file"]}">← Previous' in s,(p,'previous order')
 if it['graph']:assert (root/'dist/assets/graphs'/(it['graph']+'.svg')).exists()
pages=list((root/'dist').rglob('*.html'))
for p in pages:
 s=p.read_text();assert '<pre' not in s and not re.search('[│╲└─]{2}',s),p
 page=Page(p);page.feed(s)
 for link in page.links:assert link.exists(),(p,link)
for p in (root/'dist/assets/graphs').glob('*.svg'):ET.parse(p)
print('PASS:',len(items),'objectives in exact checklist order;',len(pages),'pages; one explanation/example/question each; all links and SVGs valid; zero text diagrams.')
