import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
from PIL import Image, ImageDraw
import numpy as np, math, json
P = PAGES
A4400=[(20,94),(30,127),(40,155),(50,176),(100,241),(150,264),(200,292),(300,330),(500,395),(1000,467),(1500,503),(2000,532),(5000,606),(10000,669),(15000,703),(20000,730)]
ASE8=[(20,67),(50,132),(100,195),(200,259),(300,295),(500,343),(2000,469),(5000,553),(10000,617),(20000,683)]
def mk(anch):
    def fx(x):
        for (f0,x0),(f1,x1) in zip(anch,anch[1:]):
            if x<=x1 or f1==anch[-1][0]: return f0*(f1/f0)**((x-x0)/(x1-x0))
    def xf(f):
        for (f0,x0),(f1,x1) in zip(anch,anch[1:]):
            if f<=f1 or f1==anch[-1][0]: return x0+(x1-x0)*math.log(f/f0)/math.log(f1/f0)
    return fx,xf
def trace(fn,anch,top,bot,out):
    fx,xf=mk(anch)
    im=np.asarray(Image.open(P+fn).convert('RGB')).astype(int)
    R,G,B=im[...,0],im[...,1],im[...,2]
    red=(R>150)&(R-G>80)&(R-B>80)
    dy=lambda y:20-40*(y-top)/(bot-top)
    pts=[]
    for x in range(anch[0][1]+1,anch[-1][1]):
        ys=np.nonzero(red[int(top)-2:int(bot)+3,x])[0]+int(top)-2
        if not len(ys): continue
        g=[]
        for y in ys:
            if g and y-g[-1][-1]<=2: g[-1].append(y)
            else: g.append([y])
        pts.append((fx(x),dy(np.mean(g[0]))))
    I=Image.open(P+fn).convert('RGB'); D=ImageDraw.Draw(I)
    for f,d in pts:
        x=xf(f); y=top+(20-d)*(bot-top)/40
        D.point((x,y+5),fill=(0,150,0))
    I.save(out)
    return pts
res={}
for key,fn,top,bot in [('se4400_card','se4400_198.png',49,322),('se4400_omni','se4400_200.png',49,322),('se4400_hyper','se4400_202.png',47,321),('se4400_fig8','se4400_204.png',50,324)]:
    res[key]=trace(fn,A4400,top,bot,'chk_'+key+'.png')
res['se8']=trace('se8_35.png',ASE8,131,324,'chk_se8.png')
for k,v in res.items():
    s=sorted(v); print(k,len(v),[(round(f),round(d,1)) for f,d in s[::max(1,len(s)//14)]])
json.dump(res,open('se_raster.json','w'))
