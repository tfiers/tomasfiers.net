import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
from PIL import Image
import numpy as np, math
U = SRC

def clusters(ys):
    g=[]
    for y in ys:
        if g and y-g[-1][-1]<=2: g[-1].append(y)
        else: g.append([y])
    return g

# ---- sE V7: red curves; take the lowest red trace per column = solid 60 cm line
im=np.asarray(Image.open(U+'a53d1e0f-image.jpg').convert('RGB')).astype(int)
R,G,B=im[:,:,0],im[:,:,1],im[:,:,2]
red=(R>100)&(R-(G+B)/2>30)
fx=lambda x: 20*10**((x-97)/((929.5-97)/3))
dy=lambda y: (198-y)/((325-135)/30)
v7=[]
for x in range(98,930):
    ys=np.nonzero(red[74:324,x])[0]+74
    if not len(ys): continue
    c=clusters(list(ys))[-1]
    if fx(x)>=27: v7.append((fx(x),dy(np.mean(c))))

# ---- AT: thin black curve over black grid; mask gridline rows/cols
im=np.asarray(Image.open(U+'fa1198f6-image.jpg').convert('L')).astype(int)
dark=im<170
hrows=[143,218,292,366,439,512]
vcols=[613,677,722,758,787,812.5,830,849,867,927,976.5,1040,1085,1120.5,1150,1175,1193,1212,1229.5,1289.5,1339,1402,1448,1483.5,1513,1538,1555.5,1574,1592.5,1652,1701.5,1768]
fa=lambda x: 100*10**((x-867)/362.75)
da=lambda y: (292-y)/((439-143)/40)
at=[]
for x in range(616,1701):
    if min(abs(x-c) for c in vcols)<=3: continue
    ys=[y for y in range(146,510) if dark[y,x] and min(abs(y-h) for h in hrows)>2]
    if ys:
        cs=clusters(ys); c=max(cs,key=len)
        y=np.mean(c)
    else:
        # curve hidden in a horizontal gridline: check which gridline is thickened
        # no curve pixels off the grid: it runs along a gridline; take the one nearest the previous point
        if not at: continue
        prev=292-at[-1][1]*((439-143)/40)
        y=min(hrows,key=lambda h:abs(h-prev))
    at.append((fa(x),da(y)))

def despike(pts, tol=0.6, w=6):
    out=[]
    for i,(f,d) in enumerate(pts):
        nb=[p[1] for p in pts[max(0,i-w):i+w+1]]
        if abs(d-np.median(nb))<=tol: out.append((f,d))
    return out

def resample(pts, step=24):
    pts=despike(pts)
    # median in 1/step-octave bins, to smooth pixel noise
    out=[]
    lo=math.log2(pts[0][0]); hi=math.log2(pts[-1][0])
    k=0
    b=lo
    while b<hi:
        vals=[d for f,d in pts if b<=math.log2(f)<b+1/step]
        if vals: out.append((2**(b+0.5/step), float(np.median(vals))))
        b+=1/step
    return out

for name,pts in [('sE V7',v7),('AT2020',at)]:
    r=resample(pts)
    fn=name.replace(' ','_')+'.csv'
    with open(fn,'w') as f:
        f.write('# %s — traced from manufacturer frequency-response graph\nfreq_hz,db\n'%name)
        for fr,d in r: f.write('%.1f,%.2f\n'%(fr,d))
    print(name,len(pts),'->',len(r), r[0], r[-1])

from PIL import ImageDraw
for img,fn,xf,yf,col in [('a53d1e0f-image.jpg','sE_V7.csv',lambda f:97+277.5*math.log10(f/20),lambda d:198-d*6.333,(0,160,255)),
                         ('fa1198f6-image.jpg','AT2020.csv',lambda f:867+362.75*math.log10(f/100),lambda d:292-d*7.4,(255,0,0))]:
    I=Image.open(U+img).convert('RGB'); D=ImageDraw.Draw(I)
    for l in open(fn):
        if not l[0].isdigit(): continue
        f,d=map(float,l.split(',')); x,y=xf(f),yf(d)
        D.ellipse([x-2,y-2,x+2,y+2],fill=col)
    I.save('check_'+fn.replace('.csv','.png'))
