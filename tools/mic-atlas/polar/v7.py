import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
from common import *
P=U+'a53d1e0f-image.jpg'
r2db=lambda r: (r-216)/7.24
left={250:[212,178,136],500:[168,234,226],1000:[135,199,174]}
right={2000:[78,75,140],4000:[168,100,110],8000:[139,208,138],16000:'dark'}
res=trace_raster(P,[('left',(593,681),left),('right',(624,681),right)],r2db,rmax=262,rmin=36,tol=40,satmin=35,axis_gap=6)
res={f:despike(fill_ends(v,-25)) for f,v in res.items()}
for f,v in sorted(res.items()): print(f,[v[i] for i in (0,6,9,12,18,24,30,36)])
json.dump({'sE V7':res},open('v7.json','w'))
