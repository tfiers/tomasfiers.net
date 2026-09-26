import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
from common import *
def vec_polar(fn, page, groups, cx, cy, r2db, flip=False, floor=-25):
    """groups: {freq: [drawing indices]}; halves folded together (median per 5° bin)."""
    p=pymupdf.open(U+fn)[page]; D=p.get_drawings(); out={}
    for f,idx in groups.items():
        pts=[]
        for i in idx: pts+=path_pts(D[i],20)
        if flip: pts=[(x,2*cy-y) for x,y in pts]
        v=resample(to_polar(pts,cx,cy,r2db))
        out[f]=fill_ends(interp_inner(v),floor)
    return out
res={}
# AT2020 spec sheet: rings 5 dB apart (5.2476 pt), 0 dB on the 2nd ring from outside.
at=vec_polar('2009385d-at2020_english.pdf',0,{200:[114,115],1000:[116,117],5000:[118,119],8000:[120,121]},353.27,414.165,lambda r:(r-26.24)/5.2476*5)
res['AT2020']=at
# Behringer C-2 manual p.6: split halves (left 250 Hz-2 kHz, right 4-16 kHz); gray rings every 5 dB, 0 dB outside.
RINGS=[(8.5,-30),(16.36,-25),(24.5,-20),(32.9,-15),(41.36,-10),(49.02,-5),(57.3,0)]
def c2db(r):
    for (r0,d0),(r1,d1) in zip(RINGS,RINGS[1:]):
        if r<=r1 or r1==RINGS[-1][0]: return d0+(r-r0)/(r1-r0)*(d1-d0)
C2='c982d482-8849953521694.pdf'
c2=vec_polar(C2,5,{250:[7],500:[6],1000:[5],2000:[1]},134.13,111.27,c2db,floor=-30)
c2.update(vec_polar(C2,5,{4000:[4],8000:[3],16000:[2]},148.14,111.27,c2db,floor=-30))
res['Behringer C-2']=c2
# Neumann U 87 Ai manual p.6: one centre per plot, 0 dB on the 2nd ring from outside, rings 5 dB (12.22 pt) apart.
U87='5bd4da93-462001-01U.pdf'; u=lambda r:(r-61.1)/12.22*5
card=vec_polar(U87,5,{125:[927],250:[930],500:[933],1000:[929],2000:[931],4000:[934],8000:[928],16000:[932]},546.965,312.255,u)
omni=vec_polar(U87,5,{250:[815],2000:[816],4000:[818],16000:[817]},712.815,174.455,u)
for a,b in {125:250,500:250,1000:250,8000:2000}.items(): omni[a]=list(omni[b])
fig8=vec_polar(U87,5,{250:[1038],2000:[1040],16000:[1037]},712.815,446.905,u)
for a,b in {125:250,500:250,1000:250,4000:2000,8000:2000}.items(): fig8[a]=list(fig8[b])
res['Neumann U 87 Ai']={'Cardioid':card,'Omni':omni,'Figure-8':fig8}
# Ovid CC 100 (t.bone datasheet): raster, 1 kHz only, full circle; rings every 3 dB (16.6 px).
ov=trace_raster(PAGES+'ovid_134.png',[('both',(190.5,201),{1000:'dark'})],lambda r:(r-168.5)/5.533,rmax=185,rmin=8,axis_gap=2,dark_thick=True)
res['Ovid CC 100']={1000:despike(fill_ends(ov[1000],-30))}
overlay(PAGES+'ovid_134.png',res['Ovid CC 100'],{1000:('right',(190.5,201))},lambda d:168.5+d*5.533,'chk_ovid.png')
def show(m,d):
    print(m); [print(' ',f,[v[i] for i in (0,6,12,18,24,30,36)]) for f,v in sorted(d.items())]
for m,d in res.items():
    if m=='Neumann U 87 Ai': [show(m+' '+k,v) for k,v in d.items()]
    else: show(m,d)
json.dump(res,open('bw.json','w'))
