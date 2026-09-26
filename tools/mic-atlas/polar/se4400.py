import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
from common import *
S=4.23; r2db=lambda r:(r-21)/S-25; db2r=lambda d:21+(d+25)*S
B,R,G,O=[20,20,220],[210,20,20],[20,240,20],[235,130,30]
cfg={ # n: pattern, cx_left, cx_right, cy, left cols, right cols, {alias: source}
 199:('cardioid',344,361,196,{250:'gray',500:O},{2000:B,4000:R,8000:G,16000:'dark'},{1000:500}),
 201:('omni',338,356,194,{250:'gray'},{2000:B,8000:R,16000:G},{500:250,1000:250,4000:2000}),
 203:('hypercardioid',341,360,198,{250:'gray'},{2000:B,8000:R,16000:G},{500:250,1000:250,4000:2000}),
 205:('figure-8',343,361,196,{250:'gray'},{2000:B,8000:R,16000:G},{500:250,1000:250,4000:2000}),
}
out={}
for n,(pat,xl,xr,cy,L,Rt,alias) in cfg.items():
    P=PAGES+f'se4400_{n}.png'
    res=trace_raster(P,[('left',(xl,cy),L),('right',(xr,cy),Rt)],r2db,rmax=150,rmin=15,tol=90,satmin=60,axis_gap=3,dark_thick=True)
    res={f:despike(fill_ends(v,-25)) for f,v in res.items()}
    C={f:('left',(xl,cy)) if f in L else ('right',(xr,cy)) for f in res}
    overlay(P,res,C,db2r,f'chk_se4400_{n}.png',box=(180,0,585,389))
    for a,s in alias.items(): res[a]=list(res[s])
    out[pat]=res
    print(pat); [print(' ',f,[v[i] for i in (0,6,9,12,18,24,30,33,36)]) for f,v in sorted(res.items())]
json.dump({'sE4400':out},open('se4400.json','w'))
