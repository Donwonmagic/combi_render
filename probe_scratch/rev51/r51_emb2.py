"""REV51 A2 -- SHAPE-FREE crown measurement, emblem located inside a GENEROUS
hand-given box (the box is stated; the centroid inside it is computed)."""
import numpy as np
import r51_seedfit as SF, r51_photo as PH, r51_inst as IN
from PIL import Image, ImageDraw
R = '/home/user/combi_render/'
Y_CREAM, Y_FLANGE, EMB_PROUD = 0.0585, 0.0640, 0.0060

CASES = [
 # tag        file                     crop box            cx cy  rg  capmode  emb box (crop coords)  outboard  mode
 ('CTRL_low34','out/r51b_low34.png',   (700,745,830,890),  55,60, 61,'red',   (48,68,70,90), (1,0), 'bright'),
 ('IMG_2073',  'IMG_2073.jpeg',        (670,720,810,890),  73,90, 70,'chrome',(74,80,95,105),(1,0), 'dark'),
 ('rear34_rear','ref_rear34.jpg',      (690,630,840,825),  57,100,68,'red',   (18,84,42,112),(-1,0),'bright'),
 ('nolita_f34','ref_nolita_front34.jpg',(370,270,475,385), 44,66, 36,'red',   (40,56,58,76), (1,0),'bright'),
 ('refside_rear','ref_side.jpg',       (690,540,820,680),  61,71, 54,'red',   (48,48,74,74), (-1,0),'bright'),
 ('playa_front','ref_playa_34.png',    (195,275,290,365),  45,47, 33,'red',   (44,40,60,56), (1,0),'bright'),
]

def centroid(img, box, mode):
    x0, y0, x1, y1 = box
    sub = img[y0:y1, x0:x1]
    V = sub.mean(-1)
    med = np.median(V)
    d = np.clip(V-med, 0, None) if mode == 'bright' else np.clip(med-V, 0, None)
    thr = np.percentile(d, 82)
    m = d > thr
    if m.sum() < 6: return None
    yy, xx = np.mgrid[y0:y1, x0:x1]
    w = d*m
    return float((xx*w).sum()/w.sum()), float((yy*w).sum()/w.sum())

print('%-14s %6s %7s %8s %8s %9s %9s %9s'
      % ('frame','phi','px/m','delta_px','perp_px','y_crown','h(mm)','dome(mm)'))
for tag, fn, box, cx, cy, rg, cm, ebox, hint, mode in CASES:
    r = SF.run_best(R+fn, box, cx, cy, rg, capmode=cm)
    if r is None: print(tag, 'FAIL'); continue
    c = r['cream']
    ec = centroid(r['img'], ebox, mode)
    if ec is None: print(tag, 'no emblem'); continue
    ph = np.arccos(np.clip(c['ratio'], -1, 1))
    s = c['a']/IN.R_CREAM
    th = c['theta']
    t = np.array([-np.sin(th), np.cos(th)])
    if np.dot(t, np.asarray(hint, float)) < 0: t = -t
    d = np.array([ec[0]-c['cx'], ec[1]-c['cy']])
    delta = float(np.dot(d, t)); perp = float(np.dot(d, [np.cos(th), np.sin(th)]))
    dy = delta/(np.sin(ph)*s) if np.sin(ph) > 0.1 else np.nan
    h = dy + (Y_CREAM-Y_FLANGE) - EMB_PROUD
    print('%-14s %6.2f %7.1f %8.2f %8.2f %9.4f %9.1f %9.1f'
          % (tag, np.degrees(ph), s, delta, perp, dy+Y_CREAM, h*1000, h*1000+12.3))
    im = Image.fromarray((np.clip(r['img'],0,1)*255).astype('uint8'))
    im = im.resize((im.width*6, im.height*6), Image.LANCZOS)
    dd = ImageDraw.Draw(im)
    dd.rectangle([ebox[0]*6, ebox[1]*6, ebox[2]*6, ebox[3]*6], outline=(0,255,0))
    dd.ellipse([ec[0]*6-4, ec[1]*6-4, ec[0]*6+4, ec[1]*6+4], fill=(0,255,0))
    dd.ellipse([c['cx']*6-4, c['cy']*6-4, c['cx']*6+4, c['cy']*6+4], fill=(255,255,0))
    a = np.linspace(0,2*np.pi,400); rr = IN.ell_radius(c,a)
    dd.line(list(zip((c['cx']+rr*np.cos(a))*6,(c['cy']+rr*np.sin(a))*6)), fill=(255,255,0))
    im.save('EMB_%s.png' % tag)
