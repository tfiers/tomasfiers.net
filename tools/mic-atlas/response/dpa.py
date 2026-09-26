import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
import pymupdf, json, math, numpy as np
U = SRC
p=pymupdf.open(U+'c2844ec7-19-1-4099_manual.pdf')[13]
D=p.get_drawings()
fx=lambda x:100*10**((x-81.39)/50.07)
def subpaths(d):
    subs=[]; cur=[]; last=None
    for it in d['items']:
        if it[0]=='l': a,b=it[1],it[2]; seg=[a,b]
        elif it[0]=='c':
            a,b1,b2,e=it[1],it[2],it[3],it[4]
            seg=[pymupdf.Point((1-t)**3*a.x+3*(1-t)**2*t*b1.x+3*(1-t)*t**2*b2.x+t**3*e.x,(1-t)**3*a.y+3*(1-t)**2*t*b1.y+3*(1-t)*t**2*b2.y+t**3*e.y) for t in np.linspace(0,1,6)]
        else: continue
        if last is None or abs(seg[0].x-last.x)>0.01 or abs(seg[0].y-last.y)>0.01:
            if cur: subs.append(cur)
            cur=[]
        cur+= [(q.x,q.y) for q in seg]; last=seg[-1]
    if cur: subs.append(cur)
    return subs
s=subpaths(D[320])
for i,sp in enumerate(s):
    xs=[q[0] for q in sp]; ys=[q[1] for q in sp]
    print(i,len(sp),round(min(xs),1),round(max(xs),1),'y@~1k',round(min(ys),1),round(max(ys),1))
# 0 deg = subpath with the smallest mean y
on=min(s,key=lambda sp:np.mean([q[1] for q in sp]))
on_pts=sorted((fx(x),(71.7-y)/1.872) for x,y in on)
subs647=subpaths(D[647])
for sp in subs647: print('647 sub',len(sp),round(min(q[0] for q in sp),1),round(max(q[0] for q in sp),1),'y at low x',round(min(sp,key=lambda q:q[0])[1],1))
# the DAD4099 curve is the one lowest (largest y) at its low-frequency end
dad=max(subs647,key=lambda sp:min(sp,key=lambda q:q[0])[1])
dad_pts=sorted((fx(x),(266.36-y)/1.872) for x,y in dad)
for n,v in [('on',on_pts),('dad',dad_pts)]:
    print(n,len(v),[(round(f),round(d,1)) for f,d in v[::max(1,len(v)//12)]])
json.dump({'on20cm':on_pts,'dad':dad_pts},open('dpa.json','w'))

def attach(main, dotted_idx, y0):
    # add the dotted subpath that connects to this curve's end (low or high side)
    pts=list(main)
    xs=[q[0] for q in main]
    lo=min(main,key=lambda q:q[0]); hi=max(main,key=lambda q:q[0])
    for k in dotted_idx:
        subs=subpaths(D[k])
        def gap(sp):
            ends=[sp[0],sp[-1]]
            return min(math.hypot(e[0]-t[0],e[1]-t[1]) for e in ends for t in (lo,hi))
        best=min(subs,key=gap)
        if gap(best)<1.0: pts+=best
    return sorted((fx(x),(y0-y)/1.872) for x,y in pts)
on_full=attach(on,[319,323],71.7)
flat=min(subs647,key=lambda sp:min(sp,key=lambda q:q[0])[1])
xmax=max(q[0] for q in dad)
dad_full=attach(dad+[q for q in flat if q[0]>xmax],[646,648],266.36)
for n,v in [('on',on_full),('dad',dad_full)]:
    print(n,len(v),[(round(f),round(d,1)) for f,d in v[::max(1,len(v)//14)]])
json.dump({'on20cm':on_full,'dad':dad_full},open('dpa.json','w'))
