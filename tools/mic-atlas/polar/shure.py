import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
from common import *
# Shure SM57 spec sheet: two full-circle polar plots (front at the bottom), vector paths.
# 0 dB on the outer ring (r = 50.4 pt), 5 dB per 10.35 pt. Each dashed curve is drawn as dash pieces
# followed by its full path; these indices are the full paths (identified by overlaying them on a render).
# The SM58 sheet has the identical polar diagram.
fn='bea4129c-us_pro_sm57_specsheet.pdf'
D=pymupdf.open(U+fn)[0].get_drawings()
r2db=lambda r:(r-50.4)/2.07
res={}
for f,i,cx in [(125,212,105.9),(500,226,105.9),(1000,219,105.9),(2000,227,248.5),(4000,241,248.5),(8000,234,248.5)]:
    cy=555.1; pts=[(x,2*cy-y) for x,y in path_pts(D[i],20)]
    res[f]=fill_ends(interp_inner(resample(to_polar(pts,cx,cy,r2db))),-25)
    print(f,[res[f][k] for k in (0,6,12,18,24,30,36)])
json.dump({'Shure SM57':res,'Shure SM58':res},open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'shure.json'),'w'))
