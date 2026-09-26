import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'polar'))   # common.py
import pymupdf, json, math
U = SRC
import sys; sys.path.insert(0,'../polar'); from common import path_pts
out={}
# SM57: gridlines 20 Hz at x=372.1, 53.2 pt/decade (1 kHz at 462.5); 0 dB at y=560.2, 5 dB per 8.9 pt.
# SM58: labels: 1 kHz at x=455.3, 51.9 pt/decade; 0 dB at y=573.65, 10 dB per 19.75 pt.
for name,fn,idx,x1k,dec,y0,ppd in [('SM57','bea4129c-us_pro_sm57_specsheet.pdf',243,462.5,53.2,560.2,1.78),
                                   ('SM58','9402a691-us_pro_sm58_specsheet.pdf',84,455.3,51.9,573.65,1.975)]:
    D=pymupdf.open(U+fn)[0].get_drawings()
    pts=sorted((1000*10**((x-x1k)/dec),(y0-y)/ppd) for x,y in path_pts(D[idx],20))
    out[name]=pts
    print(name,len(pts),[(round(f),round(d,1)) for f,d in pts[::max(1,len(pts)//12)]])
json.dump(out,open('shure.json','w'))
