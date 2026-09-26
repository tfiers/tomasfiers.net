import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
from common import *
P=PAGES+'se8_35.png'
r2db=lambda r:(r-27)/5.533-25
left={500:[255,127,0],1000:[0,255,255]}
right={2000:[0,0,255],4000:[255,0,0],8000:'dark'}
res=trace_raster(P,[('left',(1156,240),left),('right',(1179,240),right)],r2db,rmax=200,rmin=20,tol=60,satmin=60,axis_gap=4)
res={f:despike(fill_ends(v,-25)) for f,v in res.items()}
res[16000]=list(res[8000])
for f,v in sorted(res.items()): print(f,[None if x is None else round(x,1) for x in (v[i] for i in (0,6,9,12,18,24,30,33,36))])
json.dump({'sE8':res},open('se8.json','w'))
C={500:('left',(1156,240)),1000:('left',(1156,240)),2000:('right',(1179,240)),4000:('right',(1179,240)),8000:('right',(1179,240)),16000:('right',(1179,240))}
overlay(P,{f:v for f,v in res.items() if f!=16000},C,lambda d:27+(d+25)*5.533,'chk_se8.png',box=(900,0,1440,493))
