import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
import pymupdf, math, json
U = SRC
def path_points(d):
    pts=[]
    for it in d['items']:
        if it[0]=='l': seg=[it[1],it[2]]
        elif it[0]=='c': seg=[it[1],it[4]]
        else: continue
        for q in seg:
            if not pts or (abs(pts[-1][0]-q.x)>1e-3 or abs(pts[-1][1]-q.y)>1e-3): pts.append((q.x,q.y))
    return pts
out={}
# AT2020
p=pymupdf.open(U+'2009385d-at2020_english.pdf')[0]
d=p.get_drawings()[74]
pts=path_points(d)
out['AT2020']=[(100*10**((x-431.9)/52.0),(404.3-y)/1.06) for x,y in pts]
# C-2
p=pymupdf.open(U+'c982d482-8849953521694.pdf')[5]
d=p.get_drawings()[44]
pts=path_points(d)
out['C-2']=[(20*10**(3*(x-70.6)/(237.2-70.6)),(300.1-y)/1.11) for x,y in pts]
for k,v in out.items():
    v.sort()
    print(k,len(v),[ (round(f),round(db,1)) for f,db in v[::max(1,len(v)//12)]])
json.dump(out,open('vec.json','w'))
