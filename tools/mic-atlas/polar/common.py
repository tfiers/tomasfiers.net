import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
import math, json, numpy as np, pymupdf
U = SRC
ANG=list(range(0,181,5))
def path_pts(d, n=10):
    pts=[]
    for it in d['items']:
        if it[0]=='l': pts += [(it[1].x,it[1].y),(it[2].x,it[2].y)]
        elif it[0]=='c':
            a,b,c,e=it[1:5]
            for t in np.linspace(0,1,n):
                pts.append(((1-t)**3*a.x+3*(1-t)**2*t*b.x+3*(1-t)*t**2*c.x+t**3*e.x,(1-t)**3*a.y+3*(1-t)**2*t*b.y+3*(1-t)*t**2*c.y+t**3*e.y))
    return pts
def to_polar(pts, cx, cy, r2db):
    """(x,y) -> (angle 0..180 from front, dB); left/right halves folded."""
    out=[]
    for x,y in pts:
        dx,dy=x-cx,y-cy; r=math.hypot(dx,dy)
        if r<1e-6: continue
        a=math.degrees(math.atan2(abs(dx),-dy))
        out.append((a,r2db(r)))
    return out
def resample(ad, lo=-40):
    """angle/dB samples -> dB at ANG (median per 5° bin, then interpolate gaps)."""
    ad=sorted(ad); vals=[]
    for a in ANG:
        v=[d for aa,d in ad if abs(aa-a)<=2.5]
        vals.append(float(np.median(v)) if v else None)
    known=[(a,v) for a,v in zip(ANG,vals) if v is not None]
    res=[]
    for a,v in zip(ANG,vals):
        if v is None:
            if a<known[0][0] or a>known[-1][0]: res.append(None); continue
            (a0,v0),(a1,v1)=max([k for k in known if k[0]<a]),min([k for k in known if k[0]>a])
            v=v0+(v1-v0)*(a-a0)/(a1-a0)
        res.append(round(max(v,lo),1))
    return res
def resample_raw(ad, lo=-40):
    """like resample but leaves unseen angles as None (no interpolation)."""
    out=[]
    for a in ANG:
        v=[d for aa,d in ad if abs(aa-a)<=2.5]
        out.append(round(max(float(np.median(v)),lo),1) if len(v)>=2 else None)
    return out
def resample_track(ad, start=0.0, maxstep=6, lo=-40):
    """per 5° bin, follow the pixel cluster nearest the previous value (robust to stray gridline/label pixels)."""
    out=[]; prev=start
    for a in ANG:
        v=np.array([d for aa,d in ad if abs(aa-a)<=2.5])
        if len(v)<2: out.append(None); continue
        near=v[np.abs(v-prev)<=maxstep]
        if len(near)<2: out.append(None); continue
        # centre of the cluster nearest prev
        c=near[np.abs(near-prev)<=np.abs(near-prev).min()+1.5]
        x=round(max(float(np.median(c)),lo),1); out.append(x); prev=x
    return out
def interp_inner(v):
    known=[(i,x) for i,x in enumerate(v) if x is not None]
    v=list(v)
    for i in range(len(v)):
        if v[i] is None and known and known[0][0]<i<known[-1][0]:
            (i0,x0)=max(k for k in known if k[0]<i); (i1,x1)=min(k for k in known if k[0]>i)
            v[i]=round(x0+(x1-x0)*(i-i0)/(i1-i0),1)
    return v

from PIL import Image
def trace_raster(path, halves, r2db, rmax, tol=45, satmin=18, rmin=4, box=None, axis_gap=3, dark_skip=(), dark_track=False, dark_thick=False):
    """halves: list of (side, (cx,cy), {freq: rgb}); side in 'left','right','both'."""
    im=np.asarray(Image.open(path).convert('RGB')).astype(int)
    H,W,_=im.shape
    yy,xx=np.mgrid[0:H,0:W]
    sat=im.max(2)-im.min(2)
    out={}
    for side,(cx,cy),cols in halves:
        freqs=list(cols)
        darkf=[f for f in freqs if cols[f]=='dark']
        grayf=[f for f in freqs if cols[f]=='gray']
        colf=[f for f in freqs if cols[f] not in ('dark','gray')]
        C=np.array([cols[f] for f in colf]) if colf else np.zeros((0,3))
        r=np.hypot(xx-cx,yy-cy)
        isdark=(im.max(2)<95)&(sat<30)&(np.abs(xx-cx)>axis_gap)
        if dark_thick:  # keep only pixels in a 2x2 dark block (drops 1-px dashed gridlines)
            d=isdark; b=d[:-1,:-1]&d[1:,:-1]&d[:-1,1:]&d[1:,1:]; t=np.zeros_like(d)
            t[:-1,:-1]|=b; t[1:,:-1]|=b; t[:-1,1:]|=b; t[1:,1:]|=b; isdark=t
        isgray=(sat<12)&(np.abs(im.mean(2)-185)<9)&(np.abs(xx-cx)>axis_gap)
        mask=((sat>=satmin)|isdark|(isgray if grayf else False))&(r<=rmax)&(r>=rmin)
        if side=='left': mask&=(xx<cx-axis_gap)
        if side=='right': mask&=(xx>cx+axis_gap)
        if box: mask&=(xx>=box[0])&(xx<box[2])&(yy>=box[1])&(yy<box[3])
        ys,xs=np.nonzero(mask); px=im[ys,xs]; dk=isdark[ys,xs]; gy=isgray[ys,xs]
        raw={}
        if len(colf):
            d=np.linalg.norm(px[:,None,:]-C[None,:,:],axis=2)
            best=d.argmin(1); ok=(d.min(1)<tol)&~dk&~gy
            for i,f in enumerate(colf):
                sel=ok&(best==i)
                raw[f]=resample_raw(to_polar(list(zip(xs[sel].tolist(),ys[sel].tolist())),cx,cy,r2db))
        for f in grayf:
            raw[f]=resample_raw(to_polar(list(zip(xs[gy].tolist(),ys[gy].tolist())),cx,cy,r2db))
        for f in darkf:
            ad=to_polar(list(zip(xs[dk].tolist(),ys[dk].tolist())),cx,cy,r2db)
            ad=[(a,d) for a,d in ad if all(abs(a-k)>4 for k in dark_skip)]
            raw[f]=resample_track(ad) if dark_track else resample_raw(ad)
        # A curve that's hidden at some angle lies under the others drawn there: borrow their mean.
        for f in freqs:
            for j,a in enumerate(ANG):
                if raw[f][j] is None:
                    sib=[raw[g][j] for g in freqs if g!=f and raw[g][j] is not None]
                    prev=next((raw[f][k] for k in range(j-1,-1,-1) if raw[f][k] is not None), 0.0 if j<3 else None)
                    if sib and prev is not None:
                        best=min(sib,key=lambda x:abs(x-prev))
                        if abs(best-prev)<4: raw[f][j]=best
            out[f]=interp_inner(raw[f])
    return out
def fill_ends(v, floor=-25):
    """None at the ends: extend the last known value, or the floor if the curve was heading into the centre."""
    v=list(v); known=[i for i,x in enumerate(v) if x is not None]
    if not known: return v
    for i in range(known[0]): v[i]=v[known[0]]
    last=v[known[-1]]
    for i in range(known[-1]+1,len(v)): v[i]=floor if last<=floor+3 else last
    return v

from PIL import ImageDraw
def overlay(path, res, centers, db2r, out, box=None, colors=None):
    """Draw traced points (both halves, mirrored) on the source image for checking."""
    I=Image.open(path).convert('RGB'); D=ImageDraw.Draw(I)
    pal=[(255,0,255),(0,200,0),(0,0,255),(255,140,0),(0,200,200),(200,0,0),(120,60,200),(0,0,0)]
    for k,(f,v) in enumerate(sorted(res.items())):
        side,(cx,cy)=centers[f]
        for a,d in zip(ANG,v):
            if d is None: continue
            r=db2r(d); sgn=-1 if side=='left' else 1
            x=cx+sgn*r*math.sin(math.radians(a)); y=cy-r*math.cos(math.radians(a))
            D.ellipse([x-2.5,y-2.5,x+2.5,y+2.5],outline=pal[k%len(pal)],width=2)
            if a%30==0: D.text((x+4,y-4),str(f//1000 or f) if f>=1000 else str(f),fill=pal[k%len(pal)])
    if box: I=I.crop(box)
    I.save(out)

def despike(v, jump=6):
    """Replace isolated jumps (a point far from both neighbours that agree), incl. the last point."""
    v=list(v)
    for i in range(1,len(v)-1):
        a,b,c=v[i-1],v[i],v[i+1]
        if None in (a,b,c): continue
        if abs(a-c)<3 and abs(b-(a+c)/2)>jump: v[i]=round((a+c)/2,1)
    # tail: last few points that jump away from the curve (labels/axis) -> hold the last good value
    for i in range(len(v)-3,len(v)):
        if v[i] is not None and v[i-1] is not None and v[i]-v[i-1]>8: v[i]=v[i-1]
    return v
