import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
from PIL import Image, ImageDraw
import numpy as np, math, json
P = PAGES+'ovid_131.png'
im=np.asarray(Image.open(P).convert('RGB')).astype(int)
R,G,B=im[...,0],im[...,1],im[...,2]
o=(R>190)&(R-G>60)&(R-B>90)&(G>60)
fx=lambda x: 20*10**(3*(x-42)/(746-42))
dy=lambda y: 110-(y-28)*50/(395-28)
pts=[]
for x in range(43,746):
    col=o[30:394,x]
    if col.sum()>25: continue   # dotted vertical gridline
    ys=list(np.nonzero(col)[0]+30)
    g=[]
    for y in ys:
        if g and y-g[-1][-1]<=2: g[-1].append(y)
        else: g.append([y])
    g=[c for c in g if len(c)>=2]
    if not g: continue
    c=max(g,key=len)
    pts.append((fx(x),dy(np.mean(c))))
json.dump(pts,open('ovid.json','w'))
I=Image.open(P).convert('RGB'); D=ImageDraw.Draw(I)
for f,d in pts:
    x=42+(746-42)*math.log10(f/20)/3; y=28+(110-d)*(395-28)/50
    D.point((x,y+6),fill=(0,160,0))
I.save('check_ovid.png')
print(len(pts), pts[0], pts[-1])
