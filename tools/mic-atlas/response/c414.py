import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
import pymupdf, json, math, numpy as np
from PIL import Image, ImageDraw
P = PAGES
U = SRC
MAP={'XLS':{'omni':654,'wide':645,'card':652,'hyper':644},'XLII':{'omni':648,'wide':650,'card':653,'hyper':655,'fig8':643}}
fx=lambda x:20*10**((x-50)/172)
xf=lambda f:50+172*math.log10(f/20)
dy=lambda y:(80.2-y)/3.333
res={}
sheets=[]
for model,d in MAP.items():
    for pat,x in d.items():
        im=np.asarray(Image.open(P+'c414_%d.png'%x).convert('RGB')).astype(int)[:190]
        R,G,B=im[...,0],im[...,1],im[...,2]
        red=(R>170)&(G<110)&(B<110)
        pts=[]
        for c in range(51,566):
            ys=np.nonzero(red[5:185,c])[0]+5
            if not len(ys): continue
            g=[]
            for y in ys:
                if g and y-g[-1][-1]<=2: g[-1].append(y)
                else: g.append([y])
            gg=max(g,key=len)
            if len(gg)<2: continue
            pts.append((fx(c),dy(np.mean(gg))))
        res[f'{model}_{pat}']=pts
        I=Image.open(P+'c414_%d.png'%x).convert('RGB').crop((0,0,591,190)); D=ImageDraw.Draw(I)
        for f,db in pts: D.point((xf(f),80.2-db*3.333+5),fill=(0,140,0))
        D.text((300,150),f'{model} {pat}',fill=(0,0,0)); sheets.append(I)
# vector XLS figure 8
p=pymupdf.open(U+'8bb1a74e-AKG_C414XLS_C414XLII_Manual.pdf')[46]
d=p.get_drawings()[304]
pts=[]
for it in d['items']:
    seg=[it[1],it[2]] if it[0]=='l' else [it[1],it[4]] if it[0]=='c' else []
    for q in seg: pts.append((20*10**(3*(q.x-49.53)/(172.86-49.53)),(489.15-q.y)/0.7956))
res['XLS_fig8']=sorted(pts)
for k,v in res.items():
    s=sorted(v); print(k,len(v),[(round(f),round(db,1)) for f,db in s[::max(1,len(s)//10)]])
json.dump(res,open('c414.json','w'))
c=Image.new('RGB',(591,190*len(sheets)),'white')
for i,s in enumerate(sheets): c.paste(s,(0,190*i))
c.save('chk_c414.png')
