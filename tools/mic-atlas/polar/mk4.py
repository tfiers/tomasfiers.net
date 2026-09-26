import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
from common import *
P=U+'99afab08-image.jpg'; cx,cy=537.5,462
r2db=lambda r: r/342*30-30
left={250:[146,155,200],500:[44,72,148],1000:[22,163,136],2000:[156,202,187]}
right={4000:[163,17,55],8000:[193,112,117],16000:[214,191,185]}
res=trace_raster(P,[('left',(cx,cy),left),('right',(cx,cy),right)],r2db,rmax=360,tol=40)
res={f:despike(fill_ends(v,-30)) for f,v in res.items()}
for f,v in sorted(res.items()): print(f,[v[i] for i in (0,6,12,18,24,30,36)], 'missing',sum(x is None for x in v))
json.dump({'Schoeps MK 4':res},open('mk4.json','w'))
