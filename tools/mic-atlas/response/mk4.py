import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
# Schoeps MK 4 (+ CMC 6) on-axis response, traced from the clean graph on schoeps.de (a58ba6db-image.jpg).
from PIL import Image, ImageDraw
import numpy as np, json, math
P = SRC + 'a58ba6db-image.jpg'
im=np.asarray(Image.open(P).convert('RGB')).astype(int)
R,G,B=im[...,0],im[...,1],im[...,2]
A=[(50,163.5),(100,256.0),(200,348.0),(500,470.5),(1000,562.5),(2000,655.5),(5000,777.0),(10000,869.0),(20000,961.0)]
def fx(x):
    for (f0,x0),(f1,x1) in zip(A,A[1:]):
        if x<=x1 or f1==20000: return f0*(f1/f0)**((x-x0)/(x1-x0))
dy=lambda y:(86.5-y)/7.05
red=(R>100)&(R-G>50)&(R-B>20)
pts=[]
for x in range(164,961):
    ys=np.nonzero(red[20:250,x])[0]+20
    if len(ys)>=2: pts.append((fx(x),dy(np.mean(ys))))
json.dump(pts,open('mk4.json','w'))
# overlay check
I=Image.open(P).convert('RGB'); D=ImageDraw.Draw(I)
for f,d in pts[::3]:
    for (f0,x0),(f1,x1) in zip(A,A[1:]):
        if f<=f1 or f1==20000: x=x0+(x1-x0)*math.log(f/f0)/math.log(f1/f0); break
    D.point((x,86.5-d*7.05+8),fill=(0,150,0))
I.save('chk_mk4.png')
