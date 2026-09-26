import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
import json, math, numpy as np
from PIL import Image, ImageDraw
U = SRC
# schoeps.de graphs: 200 Hz gridline at x=348, 307 px/decade; 0 dB at y=86.5, 7.05 px/dB.
fx=lambda x:200*10**((x-348)/307); xf=lambda f:348+307*math.log10(f/200)
dy=lambda y:(86.5-y)/7.05
res={}; sheets=[]
for pat,img in [('omni','0d42ac95'),('card','3768500a')]:
    I=Image.open(U+img+'-image.jpg').convert('RGB'); a=np.asarray(I).astype(int)
    s=a.max(2)-a.min(2); red=(a[...,0]>120)&(a[...,1]<110)&(s>60)
    pts=[]
    for x in range(50,980):
        ys=np.nonzero(red[5:250,x])[0]+5
        if len(ys)>=2: pts.append((fx(x),dy(float(np.median(ys)))))
    res[pat]=pts
    D=ImageDraw.Draw(I)
    for f,d in pts[::6]: D.ellipse([xf(f)-2,86.5-d*7.05-2,xf(f)+2,86.5-d*7.05+2],outline=(0,160,0))
    sheets.append(I)
    print(pat,len(pts),[(round(f),round(d,1)) for f,d in pts[::90]])
json.dump(res,open('mk5.json','w'))
c=Image.new('RGB',(1000,614),'white'); c.paste(sheets[0],(0,0)); c.paste(sheets[1],(0,307)); c.save('chk_mk5_fr.png')
