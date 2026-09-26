"""Builds static/mics-library.js from the extracted data in response/ and polar/ (no PDFs needed)."""
import json, math, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from paths import STATIC
os.chdir(os.path.join(HERE, 'response'))   # the response-curve data files are read by name
vec=json.load(open('vec.json'))

def path_points(d):
    pts=[]
    for it in d['items']:
        seg=[it[1],it[2]] if it[0]=='l' else [it[1],it[4]] if it[0]=='c' else []
        for q in seg: pts.append((q.x,q.y))
    return pts

v7x=[tuple(p) for p in json.load(open('vector_extras.json'))['v7x']]

# V7: raster trace from before (60 cm curve)
v7=[(float(a),float(b)) for a,b in (l.strip().split(',') for l in open('sE_V7.csv') if l[0].isdigit()) if not 850<=float(a)<=1150]
ovid=[(f,d) for f,d in json.load(open('ovid.json')) if f>=58]

def despike(pts, tol=0.4, w=8):
    out=[]
    for i,(f,d) in enumerate(pts):
        nb=[p[1] for p in pts[max(0,i-w):i+w+1]]
        if abs(d-np.median(nb))<=tol: out.append((f,d))
    return out

def resample(pts, step=24, clean=True):
    pts=sorted(pts)
    if len(pts)<60: return pts
    if clean: pts=despike(pts)   # raster traces only; vector data is exact
    out=[]; lo=math.log2(pts[0][0]); hi=math.log2(pts[-1][0]); b=lo
    while b<hi:
        vals=[d for f,d in pts if b<=math.log2(f)<b+1/step]
        if vals: out.append((2**(b+0.5/step), float(np.median(vals))))
        b+=1/step
    return out


se=json.load(open('se_raster.json')); c4=json.load(open('c414.json'))
c4['XLS_fig8']=[tuple(p) for p in json.load(open('vector_extras.json'))['XLS_fig8']]

S4400=dict(type='Condenser, 1″ (large diaphragm)', sens=-32, noise=13, maxspl=137, imp=22, range='20–20k')
SSE8=dict(type='Condenser, small diaphragm', pattern='Cardioid', sens=-32, noise=13, maxspl=139, imp=110, range='20–20k')
SC414=dict(type='Condenser, 1″ (large diaphragm)', sens=-33, noise=6, maxspl=140, imp=200, range='20–20k')
# The Ovid graph is in absolute dB SPL; every other manufacturer's graph has 0 dB at 1 kHz. Shift it to match.
ovid_pts=resample(json.load(open('ovid_join.json'))['joined'])
_o1k=min(ovid_pts,key=lambda p:abs(math.log(p[0]/1000)))[1]
ovid_pts=[(f,d-_o1k) for f,d in ovid_pts]
PAT={'card':'Cardioid','omni':'Omni','hyper':'Hypercardioid','fig8':'Figure-8','wide':'Wide cardioid'}
lib=[
 dict(model='AT2020', points=resample(vec['AT2020'], clean=False), auto=False,
      source='Audio-Technica spec sheet, 12″ or more on axis (vector data from the PDF)',
      specs=dict(type='Condenser, 16 mm', electret=True, pattern='Cardioid', sens=-37, noise=20, maxspl=144, imp=100, range='20–20k')),
 dict(model='Behringer C-2', points=resample(vec['C-2'], clean=False), auto=False,
      source='Behringer C-2 manual (vector data from the PDF)',
      specs=dict(type='Condenser, 16 mm', pattern='Cardioid', sens=-38, noise=19, maxspl=136, imp=75, range='20–20k')),
 dict(model='sE V7', points=resample(v7), auto=True,
      source='sE V7 manual, 60 cm (2 ft) curve (traced from image)',
      specs=dict(type='Dynamic', pattern='Supercardioid', sens=-54, noise=None, maxspl=None, imp=300, range='40–19k')),
 dict(model='sE V7 X', points=resample(v7x, clean=False), auto=True,
      source='sE V7 X manual, 60 cm (2 ft) curve (vector data from the PDF)',
      specs=dict(type='Dynamic', pattern='Supercardioid', sens=-54, noise=None, maxspl=None, imp=300, range='30–19k')),
 dict(model='Ovid CC 100', points=ovid_pts, auto=False,
      source='the t.bone datasheet: ARTA measurement, 1/6-oct smoothed; near-field (blue) below 400 Hz joined to far-field (orange) above 800 Hz (traced from image); shifted from dB SPL so that 1 kHz = 0 dB, like the other graphs',
      specs=dict(type='Condenser clip-on (mini XLR)', electret=True, pattern='Cardioid', sens=-41.3, noise=20.3, maxspl=110, imp=1500, range='')),
 dict(model='sE8', points=resample(se['se8']), auto=False,
      source='sE8 manual, low cut off (traced from image)', specs=SSE8, owned=False),
]
for k,auto in [('card',False),('omni',False),('hyper',False),('fig8',False)]:
    lib.append(dict(model='sE4400', pattern=PAT[k], points=resample(se['se4400_'+k]), auto=auto, owned=False,
        source='sE4400 manual, low cut off (traced from image)', specs=dict(S4400, pattern=PAT[k])))
dpa=json.load(open('dpa.json'))
SDPA=dict(type='Condenser clip-on, 5.4 mm', electret=True, pattern='Supercardioid', sens=-44.5, noise=23, maxspl=142, imp=50, range='80–15k')
# Other distances: the 20 cm curve plus the bass change from DPA's proximity-effect graph (10 and 100 cm vs 20 cm).
prox=json.load(open('dpa_prox.json'))
def at_dist(pts, d):
    fs=[math.log(f) for f,_ in prox[d]]; ds=[v for _,v in prox[d]]
    return [(f, v+float(np.interp(math.log(f),fs,ds))) for f,v in pts]
on20=resample(dpa['on20cm'], clean=False)
for label,pts,src in [('10 cm',at_dist(on20,'10'),'at 10 cm: the 20 cm curve plus the proximity-effect graph\'s bass boost'),
                      ('20 cm',on20,'on axis at 20 cm'),
                      ('1 m',at_dist(on20,'100'),'at 1 m: the 20 cm curve plus the proximity-effect graph\'s bass loss'),
                      ('with XLR adapter',resample(dpa['dad'], clean=False),'with DAD4099 XLR adapter (80 Hz low cut), 20 cm')]:
    lib.append(dict(model='DPA 4099', pattern=label, points=pts, auto=False, owned=False,
        source='DPA 4099 manual, '+src+' (vector data from the PDF)', specs=SDPA))
u87=json.load(open('u87.json'))
for k,pat,sens,noise in [('card','Cardioid',-31.1,12),('omni','Omni',-34.0,15),('fig8','Figure-8',-33.2,14)]:
    lib.append(dict(model='Neumann U 87 Ai', pattern=pat, points=resample(u87[k], clean=False), auto=False, owned=False,
        source='Neumann U 87 Ai manual, free field (vector data from the PDF)',
        specs=dict(type='Condenser, large diaphragm', pattern=pat, sens=sens, noise=noise, maxspl=117, imp=200, range='20–20k')))
mk5=json.load(open('mk5.json'))
for k,pat,sens,noise,maxspl,rng in [('omni','Omni',-38,12,132,'20–28k'),('card','Cardioid',-37,13,131,'40–26k')]:
    lib.insert(6 if k=='omni' else 7, dict(model='Schoeps MK 5', pattern=pat, points=resample(mk5[k]), auto=False, owned=False,
        source='schoeps.de graphs and specs, MK 5 with CMC 6 (traced from image)',
        specs=dict(type='Condenser, small diaphragm (switchable)', pattern=pat, sens=sens, noise=noise, maxspl=maxspl, imp=42, range=rng)))
sh=json.load(open('shure.json'))
for m,sens,rng in [('SM57',-56.0,'40–15k'),('SM58',-54.5,'50–15k')]:
    lib.append(dict(model='Shure '+m, points=resample(sh[m], clean=False), auto=False, owned=False,
        source='Shure '+m+' spec sheet (vector data from the PDF)',
        specs=dict(type='Dynamic', pattern='Cardioid', sens=sens, noise=None, maxspl=None, imp=150, range=rng)))
lib.append(dict(model='Schoeps MK 4', points=resample(json.load(open('mk4.json'))), auto=False, owned=False,
    source='schoeps.de graph and specs, MK 4 + CMC 6 (traced from image)',
    specs=dict(type='Condenser, small diaphragm', pattern='Cardioid', sens=-36.5, noise=14, maxspl=131, imp=42, range='40–26k')))
for m in ['XLS','XLII']:
    for k in ['card','omni','wide','hyper','fig8']:
        lib.append(dict(model='AKG C414 '+m, pattern=PAT[k], points=resample(c4[m+'_'+k], clean=(m,k)!=('XLS','fig8')), auto=False, owned=False,
            source='AKG C414 XLS/XLII manual, no bass cut ('+('vector data from the PDF' if (m,k)==('XLS','fig8') else 'traced from image')+')',
            specs=dict(SC414, pattern=PAT[k])))
DESC={
 'AT2020':'Affordable side-address cardioid condenser (electret, 16 mm), the classic first home-studio mic. Fairly flat, with a gentle lift in the highs; for vocals, voice-over, and acoustic instruments.',
 'Behringer C-2':'Budget small-diaphragm “pencil” condenser, sold as a matched stereo pair with a stereo bar. For acoustic guitar, overheads, and simple stereo recordings.',
 'sE V7':'Supercardioid dynamic vocal mic for the stage. The tight pattern keeps out spill and feedback; rolled-off lows and a presence lift for clear, forward vocals.',
 'sE V7 X':'Instrument version of the V7: same supercardioid dynamic design, but with fuller, flatter lows. For guitar cabs, snare, toms, brass, and more.',
 'Ovid CC 100':'Miniature clip-on condenser (cardioid, mini-XLR) on a gooseneck, part of the t.bone Ovid system for acoustic instruments (violin, guitar, wind) on stage.',
 'Neumann U 87 Ai':'The classic studio large-diaphragm condenser (3 patterns). Flat mids with a gentle lift around 8–10 kHz; the reference “big studio” vocal sound.',
 'Schoeps MK 5':'Switchable Colette capsule: a slider on the side sets omni or cardioid, each close to the dedicated MK 2S / MK 4. Unlike most dual-diaphragm mics, the cardioid stays directional down to the lowest frequencies. Schoeps\' recommended all-purpose first capsule.',
 'Shure SM57':'The workhorse instrument dynamic: cardioid, nearly indestructible, with a bass roll-off and a presence peak around 5–6 kHz. On snare drums and guitar cabinets everywhere, and on plenty of vocals too.',
 'Shure SM58':'The standard stage vocal mic: essentially the SM57 behind a ball grille with a built-in pop filter. Bass roll-off and a presence lift around 4–5 kHz for clear vocals; famously rugged.',
 'Schoeps MK 4':'Reference small-diaphragm cardioid (MK 4 capsule on a CMC 6 amplifier): very flat and natural, also off-axis. A favourite for acoustic and classical recording, often as a pair.',
 'DPA 4099':'Tiny clip-on instrument mic on a gooseneck (violin, guitar, sax clips). Natural sound and strong off-axis rejection, so lots of gain before feedback on stage. Curves: at 20 cm from the source (DPA\'s reference distance), and at 10 cm and 1 m, where only the bass changes (the closer, the more bass: proximity effect). XLR: with the DAD4099 XLR adapter, whose low cut removes the lowest bass.',
 'sE8':'Small-diaphragm “pencil” condenser. Even, detailed, and very quiet; for acoustic guitar, piano, drum overheads, and as a stereo pair.',
 'sE4400':'Large-diaphragm condenser with 4 patterns and a smooth, classic sound. A studio all-rounder: vocals, acoustic instruments, piano, overheads.',
 'AKG C414 XLS':'The neutral C414: flat, smooth, very low noise (6 dB(A)), 9 patterns. The industry-standard all-rounder for instruments, ensembles, and rooms.',
 'AKG C414 XLII':'Same mic as the XLS but voiced brighter: a presence lift of about +3 to +5 dB from 3–10 kHz, so lead vocals and solo instruments stand out.',
}
GRAPH={'AT2020':'at2020','Behringer C-2':'behringer-c2','sE V7':'se-v7','sE V7 X':'se-v7x','Ovid CC 100':'ovid-cc100','sE8':'se8',
 'sE4400':'se4400','AKG C414 XLS':'akg-c414','AKG C414 XLII':'akg-c414','DPA 4099':'dpa-4099','Neumann U 87 Ai':'neumann-u87ai','Schoeps MK 4':'schoeps-mk4','Schoeps MK 5':'schoeps-mk5','Shure SM57':'shure-sm57','Shure SM58':'shure-sm58'}
PHOTO={'AT2020':'at2020','Behringer C-2':'behringer-c2','sE V7':'se-v7','sE V7 X':'se-v7x','Ovid CC 100':'ovid-cc100','sE8':'se8','sE4400':'se4400',
 'AKG C414 XLS':'akg-c414xls','AKG C414 XLII':'akg-c414xlii','DPA 4099':'dpa-4099','Neumann U 87 Ai':'neumann-u87ai','Schoeps MK 4':'schoeps-mk4-capsule','Schoeps MK 5':'schoeps-mk5','Shure SM57':'shure-sm57','Shure SM58':'shure-sm58'}
# Extra photos shown as thumbnails under the main one in the info card.
# Both Schoeps: the capsule first; then the pair of pencils and the wooden box (from the MK 4 set).
PHOTO_EXTRA={'Schoeps MK 4':['schoeps-mk4','schoeps-mk4-box'],'Schoeps MK 5':['schoeps-mk4','schoeps-mk4-box']}
# How the manufacturer markets / positions the mic (verbatim quotes from the manuals and data sheets).
QUOTE={}  # (marketing quotes replaced by own descriptions)
# Official product/manual pages; filled in once known.
URL={
 'AT2020':('https://www.audio-technica.com/en-us/at2020','https://docs.audio-technica.com/us/at2020_english.pdf'),
 'Behringer C-2':('https://www.behringer.com/en/products/0504-AAG','https://mediadl.musictribe.com/media/PLM/data/docs/P0263/C-2%20(OEM)_P0263_M_FR.pdf'),
 'sE V7':('https://seelectronics.com/products/v7/','https://seelectronics.com/wp-content/uploads/2021/11/V7V3UserManualv1.0-2.pdf'),
 'sE V7 X':('https://seelectronics.com/products/v7-x/','https://seelectronics.com/wp-content/uploads/2021/11/V7XUserManualv1-1.pdf'),
 'Ovid CC 100':('https://www.thomannmusic.com/the_tbone_ovid_system_cc_100.htm',None),
 'sE8':('https://seelectronics.com/products/se8/','https://seelectronics.com/wp-content/uploads/2021/11/sE8UserManualv1-9-2.pdf'),
 'sE4400':('https://seelectronics.com/products/se4400/','https://seelectronics.com/wp-content/uploads/2022/09/sE4400-T2-user-manual.pdf'),
 'AKG C414 XLS':('https://www.akg.com/C414XLS.html','https://www.akg.com/on/demandware.static/-/Sites-masterCatalog_Harman/default/dwaabcd3f2/pdfs/AKG_C414XLS_C414XLII_Manual.pdf'),
 'AKG C414 XLII':('https://www.akg.com/microphones/condenser-microphones/C414+XLII.html','https://www.akg.com/on/demandware.static/-/Sites-masterCatalog_Harman/default/dwaabcd3f2/pdfs/AKG_C414XLS_C414XLII_Manual.pdf'),
 'DPA 4099':('https://www.dpamicrophones.com/microphones/instrument/4099?variant=29','https://dpa.cloud14.structpim.com/media/4bknjkkj/4099-manual.pdf'),
 'Neumann U 87 Ai':('https://www.neumann.com/en-us/products/microphones/u-87-ai','https://www.neumann.com/globalassets/digizuite/16474-en-opin0134_u87ai_06-10.pdf'),
 'Shure SM57':('https://www.shure.com/en-US/products/microphones/sm57',None),
 'Shure SM58':('https://www.shure.com/en-US/products/microphones/sm58',None),
 'Schoeps MK 5':(None,'https://schoeps.de/fileadmin/user_upload/user_upload/Downloads/Bedienungsanleitungen/SCHOEPS_Manual_CMC_MK_E_2015-10-03_1444311033__1_.pdf'),
 'Schoeps MK 4':('https://schoeps.de/en/products/colette/capsules/cardioids/mk-4.html','https://schoeps.de/fileadmin/user_upload/user_upload/Downloads/Bedienungsanleitungen/SCHOEPS_Manual_CMC_MK_E_2015-10-03_1444311033__1_.pdf'),
}
# Manufacturer, and an indicative new price (euro street price, 2025; rounded). Schoeps capsules: with a CMC 6 amplifier.
MAKER={'AT2020':('Audio-Technica','~€100'),'Behringer C-2':('Behringer','~€60 a pair'),'sE V7':('sE Electronics','~€90'),
 'sE V7 X':('sE Electronics','~€90'),'Ovid CC 100':('the t.bone (Thomann)','~€50'),'sE8':('sE Electronics','~€220'),
 'Schoeps MK 5':('Schoeps','~€2,100 with CMC 6'),'sE4400':('sE Electronics','~€400'),'DPA 4099':('DPA Microphones','~€500'),
 'Neumann U 87 Ai':('Neumann','~€2,900'),'Shure SM57':('Shure','~€100'),'Shure SM58':('Shure','~€100'),
 'Schoeps MK 4':('Schoeps','~€1,700 with CMC 6'),'AKG C414 XLS':('AKG','~€850'),'AKG C414 XLII':('AKG','~€900')}
for e in lib:
    if e['model'] in MAKER: e['manufacturer'],e['price']=MAKER[e['model']]
    if e['model'] in DESC: e['desc']=DESC[e['model']]
    e['graph']='mics-sources/'+GRAPH[e['model']]+'.webp'
    if e['model'] in PHOTO: e['photo']='mics-photos/'+PHOTO[e['model']]+'.webp'
    # Image sizes, so the info card can reserve space before the images load (no layout jump).
    from PIL import Image as _I
    for k in ('graph','photo'):
        if k in e: e[k+'Size']=list(_I.open(STATIC+e[k]).size)
    POLAR={'AT2020':'at2020','Behringer C-2':'behringer-c2','sE V7':'se-v7','sE V7 X':'se-v7x','Ovid CC 100':'ovid-cc100',
           'sE8':'se8','sE4400':'se4400','DPA 4099':'dpa-4099','Neumann U 87 Ai':'neumann-u87ai','Schoeps MK 4':'schoeps-mk4','Schoeps MK 5':'schoeps-mk5','Shure SM57':'shure-sm57','Shure SM58':'shure-sm58'}
    if e['model'] in POLAR:
        e['polar']='mics-polar/'+POLAR[e['model']]+'.webp'
        e['polarSize']=list(_I.open(STATIC+e['polar']).size)
    if e['model'] in PHOTO_EXTRA:
        e['photosExtra']=[{'src':'mics-photos/'+n+'.webp','size':list(_I.open(STATIC+'mics-photos/'+n+'.webp').size)} for n in PHOTO_EXTRA[e['model']]]
    if e['model'] in QUOTE: e['quote'],e['quoteBy']=QUOTE[e['model']]
    if e['model'] in URL:
        page,pdf=URL[e['model']]
        if page: e['url']=page
        if pdf: e['pdf']=pdf
# Off-axis (polar) data, traced from the manufacturers' polar plots (scratchpad/polar/*.py).
# offaxis = {f: [freqs], db: [[dB at 0°, 5°, …, 180°] per freq]}, relative to on-axis (0 dB at 0°).
PD=os.path.join(HERE, 'polar')+'/'
POL={}
for fn in ['vec','mk4','mk5','v7','se8','se4400','c414','bw','shure']: POL.update(json.load(open(PD+fn+'.json')))
# The C414 manual has one polar diagram per pattern, shared by the XLS and XLII.
POL['AKG C414 XLS']=POL['AKG C414 XLII']=POL.pop('AKG C414')
S44={'cardioid':'Cardioid','omni':'Omni','hypercardioid':'Hypercardioid','figure-8':'Figure-8'}
POL['sE4400']={S44[k]:v for k,v in POL['sE4400'].items()}
def offaxis(d):
    fs=sorted(d,key=float); rows=[]
    for f in fs:
        v=list(d[f]); last=None
        for i in range(len(v)):
            if v[i] is None: v[i]=last if last is not None and last>-22 else -25
            last=v[i]
        # lone spikes (a point far off both neighbours, which agree): replace with their mean
        for i in range(1,len(v)-1):
            if abs(v[i-1]-v[i+1])<3 and abs(v[i]-v[i-1])>6 and abs(v[i]-v[i+1])>6: v[i]=(v[i-1]+v[i+1])/2
        rows.append([round(x-v[0],1) for x in v])
    return {'f':[int(float(f)) for f in fs],'db':rows}
for e in lib:
    d=POL.get(e['model'])
    if d and e.get('pattern') and not any(k[:1].isdigit() for k in d): d=d.get(e['pattern'])
    if d: e['offaxis']=offaxis(d)
# 'Other mics' in the library are grouped by manufacturer, in this order (my own mics keep their order).
MAKER_ORDER=['sE Electronics','DPA Microphones','Neumann','Shure','Schoeps','AKG']
lib.sort(key=lambda e: (e.get('owned') is False, MAKER_ORDER.index(e['manufacturer']) if e.get('owned') is False else 0,
                        e['model'] if e['manufacturer']=='Schoeps' else ''))   # MK 4 before MK 5
for e in lib:
    e['name']=e['model']+(' ('+e['pattern'][0].lower()+e['pattern'][1:]+')' if e.get('pattern') else '')
    e['points']=[[round(f,1),round(d,2)] for f,d in e['points']]
    print(e['name'],len(e['points']))

# Short lines (at most ~110 characters), so the file can be read and diffed on GitHub: one field per line,
# and long lists (curves, polar data) packed several values per line.
WIDTH = 110
def fmt(v, ind):
    one = json.dumps(v, separators=(',', ':'), ensure_ascii=False)
    if ind + len(one) <= WIDTH or not isinstance(v, (list, dict)) or not v:
        return ' ' * ind + one
    pad = ' ' * (ind + 2)
    if isinstance(v, dict):
        items = []
        for k, x in v.items():
            key = json.dumps(k, ensure_ascii=False) + ':'
            sub = fmt(x, ind + 2).lstrip()
            items.append(pad + key + sub)
        return ' ' * ind + '{\n' + ',\n'.join(items) + '\n' + ' ' * ind + '}'
    parts = [fmt(x, ind + 2).lstrip() for x in v]
    if any('\n' in p for p in parts):
        return ' ' * ind + '[\n' + ',\n'.join(pad + p for p in parts) + '\n' + ' ' * ind + ']'
    lines, cur = [], ''
    for p in parts:
        if cur and len(pad) + len(cur) + 1 + len(p) > WIDTH:
            lines.append(cur); cur = p
        else:
            cur = cur + ',' + p if cur else p
    lines.append(cur)
    return ' ' * ind + '[\n' + ',\n'.join(pad + l for l in lines) + '\n' + ' ' * ind + ']'

js="""// Mic Atlas (mics.html): the built-in microphones. One entry per curve (a mic with several patterns
// or variants has one entry per pattern, sharing `model`). To add a mic, append an entry; only
// model, name and points are required, everything else is optional.
//
//   model         mic name; entries with the same model are grouped (one library chip, one details card)
//   pattern       the variant's name, e.g. "Cardioid", "Omni", "20 cm" (omit for single-curve mics)
//   name          model + pattern, e.g. "sE4400 (cardioid)": the name on the chart
//   owned         false = listed under 'Other mics' (default: 'My mics')
//   auto          true = shown on a first visit
//   points        on-axis frequency response: [[freq_hz, dB], ...], any number of points, any dB offset
//   offaxis       polar data: {f: [freqs], db: [[dB at 0°, 5°, 10°, ..., 180°] per freq]}, 0 dB at 0°
//   specs         {type, pattern, sens (dBV/Pa), noise (dB(A)), maxspl (dB SPL), imp (ohm), range ("20–20k"),
//                 electret (true for electret condensers; shown in the mic's details)}; null = not published
//   manufacturer, price (approximate, text), desc (short description), source (where the curve comes from)
//   url, pdf      product page and manual / data sheet
//   photo, photosExtra, graph, polar (+ …Size = [w, h] in px): images in mics-photos/, mics-sources/, mics-polar/
//
// The curves here were read from the vector paths in the manufacturers' PDFs where possible,
// otherwise traced from the images (roughly ±0.5 dB; polar data ±1 dB).
window.MIC_LIBRARY = [
""" + ",\n".join(fmt(e, 2) for e in lib) + "\n];\n"
open(STATIC+'mics-library.js','w').write(js)
print(len(js))
