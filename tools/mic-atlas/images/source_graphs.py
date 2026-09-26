import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from paths import SRC, PAGES, STATIC
import pymupdf, io
from PIL import Image
U = SRC
P = PAGES
OUT=STATIC+'mics-sources/'
def pdfcrop(fn,page,rect,dpi=200):
    p=pymupdf.open(U+fn)[page]
    pix=p.get_pixmap(dpi=dpi,clip=pymupdf.Rect(*rect))
    return Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
def img(fn,box=None,base=U):
    im=Image.open(base+fn).convert('RGB')
    return im.crop(box) if box else im
def save(im,name,maxw=1100):
    if im.width>maxw: im=im.resize((maxw,round(im.height*maxw/im.width)),Image.LANCZOS)
    q=im.quantize(colors=64,method=Image.Quantize.MEDIANCUT)
    q.save(OUT+name+'.png',optimize=True)
    import os; print(name,im.size,os.path.getsize(OUT+name+'.png')//1024,'KB')
save(pdfcrop('2009385d-at2020_english.pdf',0,(385,370,592,462),300),'at2020')
save(pdfcrop('c982d482-8849953521694.pdf',5,(25,255,262,340),400),'behringer-c2')
save(img('a53d1e0f-image.jpg',(0,0,960,350)),'se-v7')
save(pdfcrop('68ef680f-V7XUserManualv1-1.pdf',3,(62,112,308,200),350),'se-v7x')
save(img('ovid_131.png',None,P),'ovid-cc100')
save(img('se8_35.png',(0,100,720,360),P),'se8')
save(pdfcrop('8ac76b35-sE4400-sE4100-T2-T1-user-manual-v1-2.pdf',39,(40,95,340,785),170),'se4400',maxw=700)
save(pdfcrop('8bb1a74e-AKG_C414XLS_C414XLII_Manual.pdf',46,(28,95,395,555),250),'akg-c414')
save(pdfcrop('c2844ec7-19-1-4099_manual.pdf',13,(20,35,240,335),300),'dpa-4099',maxw=800)
save(pdfcrop('5bd4da93-462001-01U.pdf',5,(20,130,400,500),220),'neumann-u87ai',maxw=900)
save(img('556bd71e-image.png',(360,820,2400,1400)),'schoeps-mk4')
