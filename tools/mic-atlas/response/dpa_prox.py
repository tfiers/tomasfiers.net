import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
import pymupdf, json, math, numpy as np
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dpa.py')).read().split("s=subpaths(D[320])")[0])   # U, p, D, fx, subpaths
# Proximity-effect graph (manual p.12): 973 = solid parts of the 5 distance curves, 972 = their dotted low ends.
subs=subpaths(D[973])+subpaths(D[972])
def lowy(sp): return min(sp,key=lambda q:q[0])[1]
# Join each dotted low end to the solid curve it continues (nearest endpoint).
solid=subpaths(D[973]); dotted=subpaths(D[972])
print('solid',len(solid),[ (len(s),round(min(q[0] for q in s),1),round(max(q[0] for q in s),1)) for s in solid])
print('dotted',len(dotted),[ (len(s),round(min(q[0] for q in s),1),round(max(q[0] for q in s),1)) for s in dotted])
curves=[]
for s in solid:
    lo=min(s,key=lambda q:q[0])
    best=min(dotted,key=lambda d:min(math.hypot(e[0]-lo[0],e[1]-lo[1]) for e in (d[0],d[-1])))
    curves.append(sorted(s+best))
curves.sort(key=lambda c:c[0][1])     # top (most bass) first: 10, 15, 20, 30, 100 cm
names=['10','15','20','30','100']
grid=[20*2**(k/12) for k in range(12*10)]
def at(c,f):
    xs=[fx(x) for x,y in c]; ys=[-(y)/1.872 for x,y in c]
    return float(np.interp(math.log(f),[math.log(v) for v in xs],ys))
ref=curves[2]
out={}
for n,c in zip(names,curves):
    fmax=fx(max(q[0] for q in c))
    out[n]=[(f,at(c,f)-at(ref,f)) for f in grid if f<=min(fmax,2000)]
    print(n,'cm',[(round(f),round(d,1)) for f,d in out[n][::12]])
json.dump(out,open('dpa_prox.json','w'))
