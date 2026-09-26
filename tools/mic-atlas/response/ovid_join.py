import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
from PIL import Image, ImageDraw
import numpy as np, math, json
P = PAGES+'ovid_131.png'
im=np.asarray(Image.open(P).convert('RGB')).astype(int)
R,G,B=im[...,0],im[...,1],im[...,2]
blue=(B>140)&(B-R>60)&(B-G>30)
fx=lambda x: 20*10**(3*(x-42)/(746-42))
xf=lambda f: 42+(746-42)*math.log10(f/20)/3
dy=lambda y: 110-(y-28)*50/(395-28)
yd=lambda d: 28+(110-d)*(395-28)/50
near=[]
for x in range(43,746):
    col=blue[30:394,x]
    if col.sum()>25: continue
    ys=list(np.nonzero(col)[0]+30)
    if not ys: continue
    g=[]
    for y in ys:
        if g and y-g[-1][-1]<=2: g[-1].append(y)
        else: g.append([y])
    c=max(g,key=len)
    if len(c)>=2: near.append((fx(x),dy(np.mean(c))))
far=[(f,d) for f,d in json.load(open('ovid.json')) if f>=58]
print('near',len(near),round(near[0][0]),round(near[-1][0]),' far',len(far),round(far[0][0]),round(far[-1][0]))
def interp(pts,f):
    pts=sorted(pts)
    for (f0,d0),(f1,d1) in zip(pts,pts[1:]):
        if f0<=f<=f1: return d0+(d1-d0)*(math.log(f/f0)/math.log(f1/f0) if f1>f0 else 0)
    return None
# overlap agreement check
for f in (400,500,630,800,1000):
    print(f, round(interp(near,f) or float('nan'),2), round(interp(far,f) or float('nan'),2))
# join: near below 400 Hz, far above 800 Hz, log-frequency crossfade in between
F1,F2=400.0,800.0
grid=[20*2**(i/48) for i in range(0,int(48*math.log2(20000/20))+1)]
out=[]
for f in grid:
    n=interp(near,f); r=interp(far,f)
    if f<=F1: d=n
    elif f>=F2: d=r
    else:
        w=math.log(f/F1)/math.log(F2/F1)
        d=None if n is None or r is None else (1-w)*n+w*r
    if d is not None: out.append((f,d))
json.dump({'near':near,'joined':out},open('ovid_join.json','w'))
print('joined',len(out),[(round(f),round(d,1)) for f,d in out[::40]])
I=Image.open(P).convert('RGB'); D=ImageDraw.Draw(I)
for f,d in out: D.point((xf(f),yd(d)+7),fill=(0,150,0))
I.save('chk_ovid_join.png')
