from pathlib import Path
import math, html
OUT=Path('dist/assets/graphs')
INK='#294c3d';GREEN='#3d8061';ORANGE='#c57958';BLUE='#4e7e9e';PURPLE='#8271a3';GRID='#e5eadf'
def txt(x,y,s,color=INK,anchor='start',size=17):
 return f'<text x="{x:.2f}" y="{y:.2f}" fill="{color}" text-anchor="{anchor}" font-size="{size}">{html.escape(s)}</text>'
def line(x1,y1,x2,y2,c=INK,dash=False,w=2):
 return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="{w}"'+(' stroke-dasharray="6 5"' if dash else '')+'/>'
def path(d,c=GREEN,w=3,fill='none'):
 return f'<path d="{d}" stroke="{c}" stroke-width="{w}" fill="{fill}" stroke-linejoin="round" stroke-linecap="round"/>'
def dot(x,y,c=INK):return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" fill="{c}"/>'
def save(name,title,parts,desc='',height=465):
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 {height}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc or title)}</desc><rect width="700" height="{height}" fill="#fffefb"/><g font-family="Arial, PingFang TC, sans-serif">{parts}</g></svg>'
 (OUT/(name+'.svg')).write_text(svg)
class Plot:
 def __init__(self,xlabel='Quantity / 數量 Q',ylabel='Price / 價格 P',xmax=10,ymax=10):
  self.x=lambda q:90+510*q/xmax
  self.y=lambda p:370-300*p/ymax
  self.s=''
  for a in [2,4,6,8,10]:
   self.s+=line(self.x(a*xmax/10),70,self.x(a*xmax/10),370,GRID,w=1)+line(90,self.y(a*ymax/10),600,self.y(a*ymax/10),GRID,w=1)
  self.s+=line(90,370,625,370)+line(90,370,90,48)+path('M619 365L625 370L619 375',INK,2)+path('M85 54L90 48L95 54',INK,2)
  self.s+=txt(80,394,'0',anchor='end')+txt(90,30,ylabel,size=18)+txt(600,435,xlabel,anchor='end',size=18)
 def curve(self,fn,start=0,end=10,c=GREEN):
  pts=[]
  for i in range(241):
   q=start+(end-start)*i/240;p=fn(q)
   if not -0.05<=p<=10.1 and self.y(p)<48:continue
   pts.append((self.x(q),self.y(p)))
  if pts:self.s+=path(' '.join(('M' if i==0 else 'L')+f'{a:.2f} {b:.2f}' for i,(a,b) in enumerate(pts)),c)
  return self
 def label(self,q,p,t,c=INK,dx=10,dy=0,anchor='start'):
  self.s+=txt(self.x(q)+dx,self.y(p)+dy,t,c,anchor);return self
 def point(self,q,p,t='',c=INK):
  self.s+=dot(self.x(q),self.y(p),c)
  if t:self.label(q,p,t,c,10,-12)
  return self
 def guides(self,q,p,ql='Q*',pl='P*'):
  self.s+=line(90,self.y(p),self.x(q),self.y(p),INK,True,1.3)+line(self.x(q),self.y(p),self.x(q),370,INK,True,1.3)
  if ql:self.s+=txt(self.x(q),399,ql,anchor='middle')
  if pl:self.s+=txt(78,self.y(p)+5,pl,anchor='end')
  return self
 def poly(self,pts,col):
  self.s+=f'<polygon points="{" ".join(f"{self.x(q):.2f},{self.y(p):.2f}" for q,p in pts)}" fill="{col}" opacity=".8"/>'
  return self
def base():
 p=Plot();p.curve(lambda q:10-q,.3,9.7,ORANGE).curve(lambda q:q,0,9.7,GREEN).label(9.5,9.5,'S',GREEN).label(9.5,.5,'D',ORANGE)
 return p
p=base().point(5,5,'E').guides(5,5);save('market','Market equilibrium / 市場均衡',p.s)
p=Plot('Good X / 商品 X','Good Y / 商品 Y')
p.curve(lambda q:math.sqrt(max(0,100-q*q)),0,10)
for q,v,t,c in [(3,math.sqrt(91),'A',GREEN),(8,6,'B',GREEN),(3,4,'I',BLUE),(8,9,'X',ORANGE)]:p.point(q,v,t,c)
p.s+=txt(120,460,'A, B: efficient   I: inefficient   X: infeasible',size=16)
save('ppf','PPF: efficient and infeasible points / 生產可能性邊界',p.s,height=490)
p=Plot('Good X / 商品 X','Good Y / 商品 Y')
p.curve(lambda q:8*math.sqrt(max(0,1-(q/7)**2)),0,7,BLUE).curve(lambda q:10*math.sqrt(max(0,1-(q/9.2)**2)),0,9.2,GREEN).point(3,8*math.sqrt(1-(3/7)**2),'A',BLUE).point(5.8,8*math.sqrt(1-(5.8/7)**2),'B',BLUE)
p.label(7.1,1.3,'PPF₀',BLUE).label(9.1,2.7,'PPF₁',GREEN)
save('ppfshift','Movement along PPF versus outward shift',p.s)
p=Plot('Good X / 商品 X','Good Y / 商品 Y')
p.curve(lambda q:8-.8*q,0,10,BLUE).curve(lambda q:8-.5*q,0,10,GREEN).point(6,3.2,'Production',BLUE).point(6,5,'Consumption',GREEN)
p.label(8,1.6,'PPF',BLUE,dy=18).label(8,4,'Trade line',GREEN,dy=-12)
save('trade','Trade permits consumption beyond own PPF',p.s)
for name,curve0,curve1,c in [('demandshift',lambda q:10-q,lambda q:12-q,ORANGE),('supplyshift',lambda q:q,lambda q:q-2,GREEN)]:
 p=Plot()
 p.curve(lambda q:q,0,9.6,GREEN).curve(lambda q:10-q,.3,9.7,ORANGE)
 if name=='demandshift':p.curve(curve1,2,10,PURPLE).point(5,5,'E₀').point(6,6,'E₁',PURPLE).guides(6,6,'Q₁','P₁').label(9.3,2.7,'D₁',PURPLE).label(9.3,.7,'D₀',ORANGE).label(9.4,9.4,'S',GREEN)
 else:p.curve(curve1,2,10,PURPLE).point(5,5,'E₀').point(6,4,'E₁',PURPLE).guides(6,4,'Q₁','P₁').label(9.4,7.4,'S₁',PURPLE).label(9.4,9.4,'S₀',GREEN).label(9.4,.6,'D',ORANGE)
 save(name,'Demand increase / 需求增加' if name=='demandshift' else 'Supply increase / 供給增加',p.s)
for name,price in [('ceiling',3),('floor',7),('shortage',3)]:
 p=base().point(5,5,'E')
 p.s+=line(90,p.y(price),600,p.y(price),PURPLE,w=2.5)
 p.guides(price,price,'Qs','Pc' if price<5 else 'Pf').guides(10-price,price,'Qd','')
 a,b=sorted([price,10-price]);yy=p.y(price)-22
 p.s+=line(p.x(a),yy,p.x(b),yy,PURPLE)+line(p.x(a),yy-6,p.x(a),yy+6,PURPLE)+line(p.x(b),yy-6,p.x(b),yy+6,PURPLE)
 p.s+=txt(p.x(5),yy-12,'Shortage / 短缺' if price<5 else 'Surplus / 過剩',PURPLE,'middle')
 save(name,'Binding ceiling / 價格上限' if price<5 else 'Binding floor / 價格下限',p.s)
p=Plot()
p.poly([(0,5),(0,10),(5,5)],'#c9dfb9').poly([(0,0),(0,5),(5,5)],'#f1ceb5')
p.curve(lambda q:10-q,.3,9.7,ORANGE).curve(lambda q:q,0,9.7,GREEN).point(5,5,'E').guides(5,5)
p.label(1.4,6.7,'CS',GREEN).label(1.4,2.8,'PS',ORANGE).label(9.5,9.5,'S',GREEN).label(9.5,.5,'D',ORANGE)
save('welfare','Consumer and producer surplus / 消費者與生產者剩餘',p.s)
for name in ['tax','taxwelfare','subsidy']:
 p=Plot();sub=name=='subsidy';qt=6.5 if sub else 3.5;pb=10-qt;ps=qt
 if sub:p.poly([(0,pb),(qt,pb),(qt,ps),(0,ps)],'#c9dfb9').poly([(5,5),(qt,pb),(qt,ps)],'#f0c9b5')
 else:
  if name=='taxwelfare':p.poly([(0,pb),(0,10),(qt,pb)],'#d4e3f0').poly([(0,0),(0,ps),(qt,ps)],'#e5dcf0')
  p.poly([(0,ps),(qt,ps),(qt,pb),(0,pb)],'#c9dfb9').poly([(qt,ps),(qt,pb),(5,5)],'#f0c9b5')
 p.curve(lambda q:10-q,.3,9.7,ORANGE).curve(lambda q:q,0,9.7,GREEN).guides(qt,pb,'Qsub' if sub else 'Qt','Pb').guides(qt,ps,'','Ps').guides(5,5,'Q0','')
 p.s+=line(p.x(qt),p.y(pb),p.x(qt),p.y(ps),PURPLE,w=3)
 p.point(qt,pb).point(qt,ps).point(5,5)
 p.label(1,5,'Spending' if sub else 'Tax revenue',GREEN).label(qt+.2,7.3,'s = Ps − Pb' if sub else 't = Pb − Ps',PURPLE)
 target=(5.8,5) if sub else (4,5);p.label(6.9 if sub else 5.1,8,'DWL',ORANGE)
 p.s+=line(p.x(7 if sub else 5.5),p.y(7.6),p.x(target[0]),p.y(target[1]),ORANGE,False,1.5)
 p.label(9.5,9.5,'S',GREEN).label(9.5,.5,'D',ORANGE)
 save(name,'Subsidy wedge and government spending / 補貼' if sub else 'Tax wedge, revenue and deadweight loss / 稅與無謂損失',p.s)
for name,fn in [('elasticity',lambda q:7.5-.5*q),('inelastic',lambda q:15-2*q)]:
 p=Plot();q2=3 if name=='elasticity' else 4.5
 p.poly([(0,0),(5,0),(5,5),(0,5)],'#d9e8ca').poly([(0,0),(q2,0),(q2,6),(0,6)],'#f1cbb4')
 p.curve(fn,2.6 if name=='inelastic' else 0,7.4 if name=='inelastic' else 10,ORANGE).point(5,5,'A').point(q2,6,'B')
 p.guides(5,5,'5','5').guides(q2,6,str(q2),'6')
 save(name,'Elastic demand: revenue falls when price rises' if name=='elasticity' else 'Inelastic demand: revenue rises when price rises',p.s)
p=Plot();p.s+=line(p.x(5),p.y(0),p.x(5),p.y(10),ORANGE,w=3)+line(90,p.y(6),600,p.y(6),GREEN,w=3)
p.label(5,9,'Ed = 0',ORANGE).label(7,6.5,'Ed = ∞',GREEN)
save('extremes','Vertical: perfectly inelastic; horizontal: perfectly elastic',p.s)
p=Plot('Tax per unit / 單位稅 t','Revenue / 稅收')
p.curve(lambda q:.32*q*(10-q),0,10).point(5,8,'Maximum').guides(5,8,'t*','')
save('laffer','Tax revenue rises and then falls / 拉弗曲線',p.s)
FC=4
avc=lambda q:4-q+q*q/6
mc=lambda q:4-2*q+q*q/2
atc=lambda q:4/q+avc(q)
lo,hi=3,5
for _ in range(80):
 m=(lo+hi)/2
 if mc(m)>atc(m):hi=m
 else:lo=m
qm=(lo+hi)/2
for name in ['cost','firm','shutdown']:
 p=Plot('Output / 產量 q','Cost and revenue / 每單位成本與收益',7,12)
 qstar=2+math.sqrt(8);price=6
 if name=='firm':p.poly([(0,atc(qstar)),(qstar,atc(qstar)),(qstar,price),(0,price)],'#c9dfb9')
 p.curve(atc,.5,7,BLUE).curve(avc,0,7,ORANGE).curve(mc,0,6.8,GREEN)
 if name=='cost':
  p.curve(lambda q:4/q,.5,7,PURPLE).point(3,avc(3),'min AVC',ORANGE).point(qm,atc(qm),'',BLUE).guides(qm,atc(qm),'Efficient scale','')
  p.label(6.4,4/6.4,'AFC',PURPLE,dy=-8)
 elif name=='firm':
  p.s+=line(90,p.y(price),600,p.y(price),PURPLE,w=2.5)
  p.point(qstar,price,'P = MC').guides(qstar,price,'q*','P')
  p.label(.5,4.8,'Profit / 利潤',GREEN)
 else:
  p.s+=line(90,p.y(2.5),600,p.y(2.5),PURPLE,w=2)
  p.point(3,2.5,'Shutdown threshold',PURPLE).guides(3,2.5,'q at min AVC','')
 for fn,col,label,q in [(mc,GREEN,'MC',6.3),(atc,BLUE,'ATC',6.5),(avc,ORANGE,'AVC',6.5)]:p.label(q,fn(q),label,col,dy=-8 if label!='AVC' else 15)
 save(name,{'cost':'Cost curves: MC crosses AVC and ATC at their minima','firm':'Profit-maximizing firm: price equals rising MC','shutdown':'Short-run supply begins at minimum AVC'}[name],p.s)
p=Plot('Labor / 勞工 L','Output / 產量 Q')
p.curve(lambda q:9*(1-math.exp(-q/3)),0,10).point(2,9*(1-math.exp(-2/3)),'A').point(7,9*(1-math.exp(-7/3)),'B')
save('production','Production function with diminishing marginal product',p.s)
p=Plot('Output / 產量 q','Long-run ATC / 長期平均總成本')
p.curve(lambda q:2+(q-5)**2/4,0,10).label(.7,7,'Economies',GREEN).label(5.8,7,'Diseconomies',GREEN).point(5,2)
save('scale','Economies and diseconomies of scale',p.s)
p=Plot('Industry output / 市場產量 Q','Price / 價格 P')
p.curve(lambda q:9-q,0,9,ORANGE).curve(lambda q:11-q,1,10,PURPLE)
p.s+=line(90,p.y(4),600,p.y(4),GREEN,w=3)
p.point(5,4,'E₀').point(7,4,'E₁').guides(5,4,'Q₀','min ATC').guides(7,4,'Q₁','')
p.label(8,4.4,'LR supply',GREEN).label(8.8,.2,'D₀',ORANGE).label(9.2,1.8,'D₁',PURPLE)
save('longrun','Constant-cost industry: demand growth and long-run entry',p.s)
# Circular-flow diagram: routes are arrows, not text characters.
parts=''
for x,y,w,h,en,zh in [(15,170,160,80,'Households','家庭'),(525,170,160,80,'Firms','企業'),(240,30,220,75,'Goods market','商品市場'),(240,325,220,75,'Factor market','要素市場')]:
 parts+=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#e5eedf" stroke="#cbdac4"/>'+txt(x+w/2,y+31,en,anchor='middle')+txt(x+w/2,y+57,zh,anchor='middle')
parts+='<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#617e6d"/></marker></defs>'
for d,c in [('M545 170L435 110',GREEN),('M240 65L95 65L95 170',GREEN),('M175 188L260 112',ORANGE),('M460 65L605 65L605 170',ORANGE),('M95 250L95 362L240 362',GREEN),('M460 362L605 362L605 250',GREEN),('M525 235L445 318',ORANGE),('M260 318L175 245',ORANGE)]:
 parts+=f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2.5" marker-end="url(#arrow)"/>'
parts+=txt(85,47,'Goods / 商品',GREEN)+txt(492,47,'Spending / 支出',ORANGE)+txt(90,435,'Inputs / 要素',GREEN)+txt(492,435,'Income / 收入',ORANGE)
save('circular','Circular flow / 家庭與企業的經濟循環',parts,height=465)
print('Generated',len(list(OUT.glob('*.svg'))),'SVG diagrams')
