import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
import pymupdf, io, os
from PIL import Image, ImageDraw, ImageFont
U = SRC
P = PAGES
OUT=STATIC+'mics-polar/'
def pdfcrop(fn,page,rect,dpi=250):
    pix=pymupdf.open(U+fn)[page].get_pixmap(dpi=dpi,clip=pymupdf.Rect(*rect))
    return Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
def img(path,box=None):
    im=Image.open(path).convert('RGB'); return im.crop(box) if box else im
def stack(parts, W=520):
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
    except Exception: font=ImageFont.load_default()
    ims=[]
    for lab,im in parts:
        im=im.copy(); im.thumbnail((W,W)); ims.append((lab,im))
    H=sum(i.height+30 for _,i in ims); c=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(c); y=0
    for lab,i in ims:
        d.text((6,y+4),lab,fill=(0,0,0),font=font); c.paste(i,((W-i.width)//2,y+30)); y+=i.height+30
    return c
from PIL import ImageChops
def trim(im, pad=10):
    bg=Image.new('RGB', im.size, (255,255,255))
    diff=ImageChops.difference(im, bg).convert('L').point(lambda v: 255 if v>30 else 0)
    bb=diff.getbbox()
    if not bb: return im
    return im.crop((max(0,bb[0]-pad),max(0,bb[1]-pad),min(im.width,bb[2]+pad),min(im.height,bb[3]+pad)))
def save(im,name,maxw=700):
    im=trim(im)
    if im.width>maxw: im=im.resize((maxw,round(im.height*maxw/im.width)),Image.LANCZOS)
    im.quantize(colors=64).save(OUT+name+'.png',optimize=True)
    print(name,im.size,os.path.getsize(OUT+name+'.png')//1024,'KB')
save(pdfcrop('2009385d-at2020_english.pdf',0,(296,366,392,478),400),'at2020')
save(pdfcrop('c982d482-8849953521694.pdf',5,(38,27,245,240),300),'behringer-c2')
save(img(U+'a53d1e0f-image.jpg',(40,372,960,1000)),'se-v7')
save(pdfcrop('68ef680f-V7XUserManualv1-1.pdf',3,(315,60,580,240),300),'se-v7x')
save(img(P+'ovid_134.png'),'ovid-cc100')
save(img(P+'se8_35.png',(740,0,1440,493)),'se8')
se=[('Cardioid','se4400_199.png'),('Omnidirectional','se4400_201.png'),('Hypercardioid','se4400_203.png'),('Figure-8','se4400_205.png')]
save(stack([(l,trim(img(P+f))) for l,f in se]),'se4400',maxw=520)
save(pdfcrop('c2844ec7-19-1-4099_manual.pdf',12,(25,235,225,400),350),'dpa-4099')
save(pdfcrop('5bd4da93-462001-01U.pdf',5,(410,95,815,560),220),'neumann-u87ai')
