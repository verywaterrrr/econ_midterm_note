from pathlib import Path
import re,json,html
root=Path(__file__).parent;dist=root/'dist';groups=[]
for part in re.split(r'^## ',(root/'content/checklist.md').read_text(),flags=re.M)[1:]:
 lines=part.splitlines();heading=lines[0];m=re.match(r'Chapter (\d+)',heading)
 if not (m or heading.startswith('Cross-chapter')):continue
 key=m.group(1) if m else 'cross';section='';items=[];sources=''
 for line in lines[1:]:
  if line.startswith('### '):section=line[4:]
  if line.startswith('**Sources:**'):sources=line.replace('**Sources:**','').strip()
  if line.startswith('- [ ] '):items.append({'objective':line[6:],'section':section})
 rows=[r for r in (root/'content'/('cross.txt' if key=='cross' else 'ch'+key+'.txt')).read_text().splitlines() if r.strip()]
 assert len(rows)==len(items),(key,len(rows),len(items))
 for i,(it,row) in enumerate(zip(items,rows),1):
  f=row.split('~');assert len(f)==9
  title,en,zh,example,q,opts,ans,why,graph=f
  it.update(id=f'{key}-{i:02d}',position=i,title=title,en=en,zh=zh,example=example,question=q,options=opts.split('^'),answer=int(ans),why=why,graph=graph,file=f'ch{key}-{i:02d}.html')
 groups.append(dict(key=key,title=heading,items=items,sources=sources))
flat=[(g,it) for g in groups for it in g['items']]
assert len(flat)==117
for global_index,(_,item) in enumerate(flat):
 target=global_index%4
 shift=(item['answer']-target)%4
 item['options']=item['options'][shift:]+item['options'][:shift]
 item['answer']=target
def esc(s):return html.escape(str(s),quote=True)
def inline(s):
 s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',esc(s));tick=chr(96)
 return re.sub(tick+'([^'+tick+']+)'+tick,r'<code>\1</code>',s)
names={'1':'Choice & incentives','2':'Thinking like an economist','3':'Gains from trade','4':'Supply & demand','5':'Elasticity','6':'Government policies','7':'Market efficiency','8':'Costs of taxation','14':'Costs of production','15':'Competitive firms','cross':'Final MCQ checks'}
cn={'1':'選擇與激勵','2':'經濟學思考','3':'貿易收益','4':'供給與需求','5':'彈性','6':'政府政策','7':'市場效率','8':'稅收成本','14':'生產成本','15':'完全競爭企業','cross':'跨章節 MCQ 檢查'}
def shell(title,body,prefix=''):
 return f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f8f8f3"><meta name="description" content="Bilingual ECON2103 study: one checklist item, example and practice question at a time."><title>{esc(title)} · ECON2103</title><link rel="stylesheet" href="{prefix}assets/style.css?v=checklist2"><script defer src="{prefix}assets/app.js?v=checklist2"></script></head><body><header class="top"><a class="brand" href="{prefix}index.html"><span class="mark">e</span><span>econ / study notes</span></a><small>ECON2103 · CHECKLIST EDITION</small><a class="back" href="{prefix}index.html">All chapters ↗</a></header>{body}<footer class="foot"><span>ECON2103 · 117 checklist items</span><span>Fall 2026 · 中英對照 · 非官方教材</span></footer></body></html>'
captions={
'market':'E 是供需交點；虛線標示均衡價格與數量。Market equilibrium.',
'ppf':'A、B 有效率；I 在邊界內，X 在邊界外。Efficient, inefficient and infeasible points.',
'ppfshift':'A 到 B 是沿線移動；PPF₀ 到 PPF₁ 是邊界外移。Movement versus shift.',
'trade':'交易線上的消費組合可在個人 PPF 外。Trade expands consumption possibilities.',
'demandshift':'D₀ 右移到 D₁：均衡價格和數量上升。Demand increases.',
'supplyshift':'S₀ 右移到 S₁：均衡價格下降、數量上升。Supply increases.',
'ceiling':'Pc 低於均衡價，Qd 大於 Qs，差額為短缺。A binding ceiling.',
'floor':'Pf 高於均衡價，Qs 大於 Qd，差額為過剩。A binding floor.',
'shortage':'紫色價格線上 Qd 與 Qs 的差是短缺。Shortage creates upward price pressure.',
'welfare':'綠色是 CS，橙色是 PS，合計為總剩餘。Consumer and producer surplus.',
'tax':'Qt 上 Pb−Ps=t；綠色長方形為稅收，橙色三角形為 DWL。Revenue and lost gains from trade.',
'taxwelfare':'藍色 CS、紫色 PS、綠色政府收入相加為稅後總剩餘；橙色為 DWL。',
'subsidy':'Ps−Pb=s；綠色長方形是政府支出，橙色三角形是過量交易的 DWL。',
'elasticity':'A → B：P 5→6，Q 5→3，TR 25→18。有彈性需求區加價令收入下降。',
'inelastic':'A → B：P 5→6，Q 5→4.5，TR 25→27。缺乏彈性需求區加價令收入上升。',
'extremes':'垂直 Ed=0；水平 Ed=∞。Two separate extreme demand cases.',
'laffer':'收入為 t×Q(t)；稅太高時收入可下降。Revenue need not increase with the tax.',
'cost':'同一組成本函數：MC 通過 AVC 及 ATC 各自最低點；AFC 下降。',
'firm':'在上升 MC 與價格線交點選 q*；綠色利潤面積=(P−ATC)×q*。',
'shutdown':'最低 AVC 是短期停產門檻；價格更低時供給為零。Shutdown threshold.',
'production':'曲線漸平代表邊際產量下降。Diminishing marginal product.',
'scale':'長期 ATC 下降是規模經濟，上升是規模不經濟。Scale economies.',
'longrun':'固定成本行業需求右移：長期總量上升，價格維持最低 ATC。',
'circular':'綠線為商品或要素，橙線為相應貨幣付款。Real flows and money flows.'
}
def chart(name):
 assert (dist/'assets/graphs'/f'{name}.svg').exists()
 return f'<figure class="econ-figure"><div class="figure-label">DRAWN DIAGRAM · 概念圖</div><div class="graph-scroll"><img src="../assets/graphs/{name}.svg?v=2" alt="{esc(captions[name])}" width="700" height="465"></div><figcaption>{esc(captions[name])}<span class="scrollhint">小螢幕可左右滑動圖表 · Swipe to view</span></figcaption></figure>'
def overviewfile(k):return f'{int(k):04d}-chapter-{k}.html' if k!='cross' else 'cross-chapter.html'
for p in (dist/'lessons').glob('*.html'):p.unlink()
for idx,(g,it) in enumerate(flat):
 k=g['key'];n=it['position'];count=len(g['items'])
 side=f'<aside class="side item-side"><a class="chapter-back" href="{overviewfile(k)}">← {esc(cn[k])}</a><span class="eyebrow">{count} CHECKLIST ITEMS</span><nav aria-label="Chapter checklist">'
 for other in g['items']:
  active=other['id']==it['id']
  side+=f'<a href="{other["file"]}" class="item-link {"active" if active else ""}" data-item-link="{other["id"]}"'+(' aria-current="page"' if active else '')+f'><span>{other["position"]:02d}</span><span>{esc(other["title"].split(" / ")[0])}</span><i aria-hidden="true"></i></a>'
 side+='</nav></aside>'
 quiz=f'<section class="quiz item-quiz"><span class="eyebrow">03 · TRY IT / 例題練習</span><h2>One question. Your turn.</h2><fieldset class="question" data-key="{it["id"]}" data-answer="{it["answer"]}" data-explanation="{esc(it["why"])}"><legend>{esc(it["question"])}</legend>'
 for j,opt in enumerate(it['options']):quiz+=f'<label class="option"><input type="radio" name="answer" value="{j}"><span class="option-letter">{chr(65+j)}</span><span>{esc(opt)}</span></label>'
 quiz+='<div class="feedback" role="status" hidden></div></fieldset></section>'
 prev=flat[idx-1][1] if idx else None;nxt=flat[idx+1][1] if idx+1<len(flat) else None
 nav=('<a href="'+prev['file']+'">← Previous 上一項</a>' if prev else '<a href="../index.html">← All chapters</a>')
 nav+=('<a class="btn" href="'+nxt['file']+'">Next 下一項 →</a>' if nxt else '<a class="btn" href="../index.html">Back to chapters 完成 →</a>')
 ts=it['title'].split(' / ')
 main=f'<main class="item-main" data-current-item="{it["id"]}" data-current-path="lessons/{it["file"]}"><div class="lessonhead"><span class="eyebrow">{"CHAPTER "+k if k!="cross" else "FINAL CHECKS"} · ITEM {n:02d} / {count:02d}</span><p class="section-label">{esc(it["section"])}</p><h1>{esc(ts[0])}<span>{esc(ts[1]) if len(ts)>1 else ""}</span></h1><div class="step-track" aria-hidden="true"><span style="width:{100*n/count:.3f}%"></span></div></div><article class="article"><section class="objective"><span class="eyebrow">YOUR CHECKBOX · 原始清單項目</span><p>{inline(it["objective"])}</p></section><section class="explain"><span class="eyebrow">01 · UNDERSTAND / 概念解釋</span><p class="zh-explanation" lang="zh-Hant">{esc(it["zh"])}</p><p class="en-explanation" lang="en">{esc(it["en"])}</p></section>'
 if it['graph']:main+=chart(it['graph'])
 main+=f'<section class="worked-example"><span class="eyebrow">02 · WORKED EXAMPLE / 一個示範</span><h2>See it in action.</h2><p>{esc(it["example"])}</p></section>{quiz}<section class="review-control"><label><input type="checkbox" data-reviewed="{it["id"]}"> I have reviewed this item / 我已複習這項</label><p>這是複習紀錄；答過一題不代表完全掌握。Saved in this browser.</p></section><nav class="navbottom">{nav}</nav><p class="source">{inline(g["sources"] or "Cross-chapter checks from the original checklist.")} <a href="../reference/sources.html">Source notes ↗</a></p></article></main>'
 (dist/'lessons'/it['file']).write_text(shell(it['title'],f'<div class="wrap lesson-layout">{side}{main}</div>','../'))
for g in groups:
 k=g['key'];items='';section=None
 for it in g['items']:
  if it['section']!=section:
   section=it['section'];items+=f'<h2 class="outline-section">{esc(section or "Final checks")}</h2>'
  items+=f'<a class="outline-item" href="{it["file"]}" data-item-link="{it["id"]}"><span class="outline-num">{it["position"]:02d}</span><div><h3>{esc(it["title"])}</h3><p>{inline(it["objective"])}</p></div><i aria-hidden="true">↗</i></a>'
 body=f'<main class="chapter-outline wrap"><div class="lessonhead"><span class="eyebrow">{"CHAPTER "+k if k!="cross" else "FINAL CHECKS"} · {len(g["items"])} ITEMS</span><h1>{esc(names[k])}<span>{esc(cn[k])}</span></h1><p>依原始 checklist 順序逐項學習。One explanation, one example and one question per item.</p><a class="btn" href="{g["items"][0]["file"]}">Start item 01 開始 →</a></div>{items}</main>'
 (dist/'lessons'/overviewfile(k)).write_text(shell(names[k],body,'../'))
cards=''
for g in groups:
 k=g['key'];cards+=f'<a class="card" href="lessons/{overviewfile(k)}"><span class="num">{"CHAPTER "+k if k!="cross" else "FINAL CHECKS"} · {len(g["items"])} ITEMS</span><h3>{esc(names[k])}</h3><p>{esc(cn[k])}</p><span class="chapter-progress" data-chapter-progress="{k}">0 / {len(g["items"])} reviewed</span><span class="arrow">Open checklist ↗</span></a>'
home=f'<main><div class="wrap"><section class="hero"><div><span class="eyebrow">CHECKLIST EDITION · 中英對照</span><h1>One idea.<br><em>Then the next.</em></h1><p>嚴格跟隨你的 midterm checklist，一次學一項。每項都有概念解釋、一個示範和一道 MCQ，逐步建立理解。</p><a class="btn" href="lessons/ch1-01.html" data-resume>Start item 01 開始學習 ↗</a></div><div class="hero-art"><div class="chartbox"><div class="chart-label"><span>UNDERSTAND THE GRAPH</span><span>理解 · 應用</span></div><img src="assets/graphs/market.svg?v=2" alt="Supply and demand graph with equilibrium E, P* and Q*" width="700" height="465"><div class="chart-label"><span>117 CHECKLIST ITEMS</span><span>10 CHAPTERS + FINAL CHECKS</span></div></div></div></section><section><div class="sectionhead"><div><span class="eyebrow">YOUR EXACT CHECKLIST · 按原清單排序</span><h2>Choose a chapter.</h2></div><p data-total-progress>0 / 117 items reviewed · 本機紀錄</p></div><div class="grid">{cards}</div></section></div><section class="band"><div><span class="eyebrow">THE LEARNING RHYTHM · 學習節奏</span><h2>Understand. Apply. Retrieve.</h2><p>讀解釋 → 看示範 → 自己答題 → 下一項。</p></div><a class="btn" href="lessons/cross-chapter.html">Final MCQ checks ↗</a></section></main>'
(dist/'index.html').write_text(shell('Checklist study',home))
sources='<main class="wrap chapter-outline"><h1>Sources & scope / 資料與範圍</h1><p>Each item follows the exact order and wording of the original ECON2103 Midterm Topic and Skills Checklist. The explanations, examples and questions are independently written study materials.</p><p>課程來源：Fall 2026 Chapters 1–8, 14, 15 slides，以及各章問題集；各頁保留清單的對應資料索引。原始教師 PPTX 及 PDF 沒有公開。</p><p>Ch 1 slides 35–39 mark economy-as-a-whole principles “Not required*”. The Ch 8 slide-24 elasticity/Laffer extension is optional. Final coverage and weighting depend on the instructor.</p><p>圖表為繪製的 SVG 概念圖；除明確標示數字的圖外，不代表示範題的精確數值。Review flags and quiz attempts remain in this browser and do not establish mastery.</p><a class="btn" href="../index.html">All chapters ↗</a></main>'
(dist/'reference/sources.html').write_text(shell('Sources',sources,'../'))
(dist/'reference/review.html').write_text(shell('Final checks','<main class="wrap chapter-outline"><h1>Final MCQ checks</h1><p>跨章節檢查已分成五個獨立學習項目。</p><a class="btn" href="../lessons/cross-chapter.html">Open final checks →</a></main>','../'))
index=[dict(id=it['id'],chapter=g['key'],file='lessons/'+it['file'],objective=it['objective']) for g,it in flat]
(dist/'assets/checklist.json').write_text(json.dumps(index,ensure_ascii=False,indent=2))
(root/'content/curriculum.json').write_text(json.dumps(groups,ensure_ascii=False,indent=2))
print(f'Built {len(flat)} item lessons, {len(groups)} overviews and home.')
