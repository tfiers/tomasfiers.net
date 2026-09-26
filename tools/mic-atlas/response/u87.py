import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
import pymupdf, json, math, numpy as np
U = SRC
p=pymupdf.open(U+'5bd4da93-462001-01U.pdf')[5]
D=p.get_drawings()
fx=lambda x:100*10**((x-158.5)/91.9)
def pts_of(d):
    out=[]
    for it in d['items']:
        if it[0]=='l': seg=[it[1],it[2]]
        elif it[0]=='c':
            a,b1,b2,e=it[1],it[2],it[3],it[4]
            seg=[pymupdf.Point((1-t)**3*a.x+3*(1-t)**2*t*b1.x+3*(1-t)*t**2*b2.x+t**3*e.x,(1-t)**3*a.y+3*(1-t)**2*t*b1.y+3*(1-t)*t**2*b2.y+t**3*e.y) for t in np.linspace(0,1,40)]
        else: continue
        out+=[(q.x,q.y) for q in seg]
    return out
res={}
for key,k,y0 in [('omni',247,174.1),('card',478,311.9),('fig8',709,446.55)]:
    v=sorted((fx(x),(y0-y)/1.6905) for x,y in pts_of(D[k]))
    res[key]=v
    print(key,len(v),[(round(f),round(d,1)) for f,d in v[::max(1,len(v)//12)]])
json.dump(res,open('u87.json','w'))
