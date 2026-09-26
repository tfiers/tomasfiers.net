import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
from PIL import Image, ImageOps
import os
PH = PAGES
U = SRC
OUT=STATIC+'mics-photos/'
jobs=[
 ('at2020', PH+'2009385d_p0_x1.png', None),
 ('se-v7', PH+'364a6e63_p0_x13.png', (0,0,499,1368)),
 ('se-v7x', PH+'68ef680f_p0_x13.png', None),
 ('ovid-cc100', PH+'5e265249_p0_x138.png', None),
 ('se8', PH+'440f0c59_p0_x13.png', None),
 ('se4400', PH+'8ac76b35_p0_x11.png', (60,20,405,938)),
 ('akg-c414xls', PH+'8bb1a74e_p0_x765.png', None),
 ('akg-c414xlii', PH+'8bb1a74e_p0_x767.png', None),
 ('dpa-4099', PH+'dpa_p8_76.png', None),
 ('neumann-u87ai', PH+'5bd4da93_p0_x85.png', None),
 ('schoeps-mk4', U+'ff7026b8-image.png', (430,820,940,1460)),
]
for name,src,box in jobs:
    im=Image.open(src).convert('RGB')
    if box: im=im.crop(box)
    im.thumbnail((360,360), Image.LANCZOS)
    im.save(OUT+name+'.jpg', quality=82, optimize=True, progressive=True)
    print(name, im.size, os.path.getsize(OUT+name+'.jpg')//1024,'KB')
