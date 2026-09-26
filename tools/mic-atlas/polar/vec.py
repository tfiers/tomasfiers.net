import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
from common import *
res={}
# --- sE V7 X (vector). Rings every 5 dB from +5 (outer) to -25; per half its own centre.
p=pymupdf.open(U+'68ef680f-V7XUserManualv1-1.pdf')[3]; D=p.get_drawings()
r2db_v7x=lambda r: (r-8.5)/1.86-25
LEFT,RIGHT=(457.4,159.1),(465.4,159.1)
spec={250:([247],LEFT),500:([248],LEFT),1000:([250],LEFT),2000:([249,254],RIGHT),4000:([251,255],RIGHT),8000:([252],RIGHT),16000:([253],RIGHT)}
res['sE V7 X']={}
for f,(ks,(cx,cy)) in spec.items():
    pts=sum((path_pts(D[k]) for k in ks),[])
    res['sE V7 X'][f]=resample(to_polar(pts,cx,cy,r2db_v7x))
# sanity: grid ring radii
for k in (119,121,131): r=D[k]['rect']; print('v7x ring',k,round(r.y1-159.1,1))
# --- DPA 4099 (vector, full circle, rings every 5 dB, 0 dB at outer circle, centre = -25 dB)
p=pymupdf.open(U+'c2844ec7-19-1-4099_manual.pdf')[12]; D=p.get_drawings()
o=D[16]['rect']; cx,cy=(o.x0+o.x1)/2,(o.y0+o.y1)/2; R=(o.x1-o.x0)/2
print('dpa centre',round(cx,1),round(cy,1),'R',round(R,1))
r2db_dpa=lambda r: r/R*25-25
colors={250:21,500:22,1000:23,2000:24,4000:25,8000:26,16000:27}
res['DPA 4099']={f:resample(to_polar(path_pts(D[k]),cx,cy,r2db_dpa)) for f,k in colors.items()}
for m,d in res.items():
    for f,v in d.items(): print(m,f,[v[i] for i in (0,6,12,18,24,30,36)])
json.dump(res,open('vec.json','w'))
