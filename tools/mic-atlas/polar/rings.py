import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
from PIL import Image
import numpy as np, sys
def rings(path, cx, cy, box=None, rmax=None, thr=None):
    im=np.asarray(Image.open(path).convert('RGB')).astype(int)
    if box: im=im[box[1]:box[3], box[0]:box[2]]; cx-=box[0]; cy-=box[1]
    g=im.sum(2)/3; R,G,B=im[...,0],im[...,1],im[...,2]
    gray=(g<215)&(abs(R-G)<22)&(abs(G-B)<22)
    ys,xs=np.nonzero(gray); r=np.hypot(xs-cx,ys-cy)
    rmax=rmax or int(r.max())
    h=np.bincount(np.round(r).astype(int),minlength=rmax+2)[:rmax]
    # normalise by circumference
    hn=h/np.maximum(1,2*np.pi*np.arange(rmax))
    thr=thr or np.percentile(hn[5:],92)
    peaks=[i for i in range(3,rmax-1) if hn[i]>thr and hn[i]>=hn[i-1] and hn[i]>=hn[i+1]]
    out=[]
    for p in peaks:
        if out and p-out[-1]<=4: continue
        out.append(p)
    return out
if __name__=='__main__':
    print(rings(sys.argv[1],float(sys.argv[2]),float(sys.argv[3])))
