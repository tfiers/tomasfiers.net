"""V7 X response and C414 XLS figure-8 response, from the vector paths in the PDFs."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
import pymupdf, json, numpy as np
U = SRC

def path_points(d):
    pts=[]
    for it in d['items']:
        seg=[it[1],it[2]] if it[0]=='l' else [it[1],it[4]] if it[0]=='c' else []
        for q in seg: pts.append((q.x,q.y))
    return pts

# V7 X: solid 60 cm curve = drawings 68 + 69; hand-drawn log axis -> piecewise between labelled gridlines
p=pymupdf.open(U+'68ef680f-V7XUserManualv1-1.pdf')[3]
D=p.get_drawings()
anch=[(20,90.7),(50,112.5),(100,133.7),(200,154.9),(500,182.9),(1000,203.8),(2000,225.0),(5000,253.1),(10000,274.3),(20000,296.2)]
def fx(x):
    for (f0,x0),(f1,x1) in zip(anch,anch[1:]):
        if x<=x1 or f1==20000:
            return f0*(f1/f0)**((x-x0)/(x1-x0))
v7x=[(fx(x),(155.7-y)/1.605) for x,y in path_points(D[68])+path_points(D[69])]

# XLS figure 8: resample the vector path with proper Bezier sampling
p=pymupdf.open(U+'8bb1a74e-AKG_C414XLS_C414XLII_Manual.pdf')[46]
d=p.get_drawings()[304]; pts=[]
for it in d['items']:
    if it[0]=='l': qs=[it[1],it[2]]
    elif it[0]=='c':
        a,b,c,e=it[1],it[2],it[3],it[4]
        qs=[]
        for t in np.linspace(0,1,12):
            x=(1-t)**3*a.x+3*(1-t)**2*t*b.x+3*(1-t)*t**2*c.x+t**3*e.x
            y=(1-t)**3*a.y+3*(1-t)**2*t*b.y+3*(1-t)*t**2*c.y+t**3*e.y
            qs.append(pymupdf.Point(x,y))
    else: continue
    for q in qs: pts.append((20*10**(3*(q.x-49.53)/(172.86-49.53)),(489.15-q.y)/0.7956))
fig8=pts

json.dump({'v7x': v7x, 'XLS_fig8': fig8}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vector_extras.json'), 'w'))
