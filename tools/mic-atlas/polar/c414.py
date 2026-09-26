import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
from common import *
import pymupdf
R,G,B=[225,50,55],[20,170,95],[20,130,180]
S=2.15; R0=71; CY=711-364.3
r2db=lambda r:(r-R0)/S; db2r=lambda d:R0+d*S
cfg={649:('Omni',{250:R},{2000:R,8000:B,16000:G},{500:250,1000:250,4000:2000}),
     651:('Wide cardioid',{250:G,500:R},{2000:R,8000:B,16000:G},{1000:500,4000:2000}),
     646:('Cardioid',{250:G,500:R},{2000:R,16000:G},{1000:500,4000:2000,8000:2000}),
     647:('Hypercardioid',{250:G,500:R},{2000:R,16000:G},{1000:500,4000:2000,8000:2000})}
# The diagrams have the front at the bottom: flip them so the front is up, as trace_raster expects.
from PIL import Image
for n in cfg: Image.open(PAGES+f'c414_{n}.png').convert('RGB').transpose(Image.FLIP_TOP_BOTTOM).save(f'c414f_{n}.png')
import sys
XL=float(sys.argv[1]) if len(sys.argv)>1 else 107.3; XR=float(sys.argv[2]) if len(sys.argv)>2 else 130.7
out={}
for n,(pat,L,Rt,alias) in cfg.items():
    P=f'c414f_{n}.png'
    res=trace_raster(P,[('left',(XL,CY),L),('right',(XR,CY),Rt)],r2db,rmax=R0+12,rmin=6,tol=80,satmin=70,axis_gap=2)
    res={f:despike(fill_ends(v,-30)) for f,v in res.items()}
    C={f:('left',(XL,CY)) if f in L else ('right',(XR,CY)) for f in res}
    overlay(P,res,C,db2r,f'chk_c414_{n}.png',box=(20,250,240,450))
    for a,s in alias.items(): res[a]=list(res[s])
    out[pat]=res
    print(pat); [print(' ',f,[v[i] for i in (0,6,12,18,24,30,36)]) for f,v in sorted(res.items())]
# Figure-8: vector paths on page 47 (front at the bottom).
p=pymupdf.open(U+'8bb1a74e-AKG_C414XLS_C414XLII_Manual.pdf')[46]
cy=490.595; R0v=17.03; Sv=R0v*S/R0
fig={}
for d in p.get_drawings():
    r=d['rect']; col=d.get('color')
    if not col or not (186<r.x0<214 and 470<r.y0<476) or max(col)-min(col)<0.3: continue
    left=r.x1<208
    cx=207.46 if left else 212.83
    pts=[(x,2*cy-y) for x,y in path_pts(d,20)]   # flip: front up
    ad=to_polar(pts,cx,cy,lambda rr:(rr-R0v)/Sv)
    key=250 if left else (16000 if col[1]>0.6 else 2000)
    fig[key]=fill_ends(interp_inner(resample(ad)),-30)
for a,s in {500:250,1000:250,4000:2000,8000:2000}.items(): fig[a]=list(fig[s])
out['Figure-8']=fig
print('Figure-8'); [print(' ',f,[v[i] for i in (0,6,12,18,24,30,36)]) for f,v in sorted(fig.items())]
json.dump({'AKG C414':out},open('c414.json','w'))
