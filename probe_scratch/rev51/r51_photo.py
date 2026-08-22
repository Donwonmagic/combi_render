"""REV51 A2 -- the same pipeline, pointed at photographs."""
import numpy as np
from PIL import Image
import r51_inst as IN, r51_pipe as P

def load(fn, box=None):
    im = Image.open(fn).convert('RGB')
    if box: im = im.crop(box)
    return np.asarray(im, float)/255.0, (box[0] if box else 0, box[1] if box else 0)

def sc_cream(img):
    V = img.max(-1); ch = V - img.min(-1)
    return V - 1.6*ch

def sc_red(img):
    return img[..., 0] - np.maximum(img[..., 1], img[..., 2])

def sc_chromecap(img):
    """cap = NOT cream:  the mirror dome is darker/structured, the rim is a
    bright desaturated plateau."""
    return -sc_cream(img)

def auto_seed(cs, pt, t_cream=None, close=3):
    """connected bright-desaturated blob containing `pt`, holes filled ->
    the WHEEL FACE.  Then face AND NOT cream -> the CAP."""
    from scipy import ndimage as ndi
    if t_cream is None:
        # Otsu on the cream score inside a generous window round pt
        x0, y0 = int(pt[0]), int(pt[1])
        w = cs[max(0, y0-90):y0+90, max(0, x0-90):x0+90].ravel()
        hs, be = np.histogram(w, 128)
        p = hs/hs.sum(); om = np.cumsum(p); mu = np.cumsum(p*(be[:-1]+be[1:])/2)
        mt = mu[-1]
        with np.errstate(invalid='ignore', divide='ignore'):
            sb = (mt*om - mu)**2/(om*(1-om))
        t_cream = float(((be[:-1]+be[1:])/2)[np.nanargmax(sb)])
    m = cs > t_cream
    m = ndi.binary_closing(m, np.ones((close, close)))
    lab, n = ndi.label(m)
    L = lab[int(pt[1]), int(pt[0])]
    if L == 0:
        d = ndi.distance_transform_edt(~m, return_distances=False,
                                       return_indices=True)
        L = lab[d[0][int(pt[1]), int(pt[0])], d[1][int(pt[1]), int(pt[0])]]
    face = ndi.binary_fill_holes(lab == L)
    cap = face & ~(lab == L)
    cap = ndi.binary_opening(cap, np.ones((2, 2)))
    lab2, n2 = ndi.label(cap)
    if n2 > 0:
        sizes = ndi.sum(cap, lab2, range(1, n2+1))
        cap = lab2 == (1 + int(np.argmax(sizes)))
    return face, cap, t_cream


def seed_disc(shape, cx, cy, a, b, th=0.0):
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]]
    c, s = np.cos(-th), np.sin(-th)
    u = c*(xx-cx) - s*(yy-cy); v = s*(xx-cx) + c*(yy-cy)
    return (u/a)**2 + (v/b)**2 <= 1.0

def run(fn, box, pt, capmode='red', ang_excl=None, t_cream=None, clip_cap='both',
        rho=(0.86, 1.16), rho_cap=(0.80, 1.22), seed=None):
    img, off = load(fn, box)
    cs = sc_cream(img)
    ks = sc_red(img) if capmode == 'red' else sc_chromecap(img)
    ang = np.linspace(-np.pi, np.pi, 720, endpoint=False)
    if ang_excl:
        keep = np.ones(len(ang), bool)
        for (a0, a1) in ang_excl:
            keep &= ~((ang >= np.radians(a0)) & (ang <= np.radians(a1)))
        ang = ang[keep]
    if seed is None:
        fseed, kseed, tc = auto_seed(cs, pt, t_cream)
        f0 = IN.init_from_mask(fseed); k0 = IN.init_from_mask(kseed)
    else:
        cx, cy, aa, bb, th = seed
        f0 = dict(cx=cx, cy=cy, a=max(aa, bb), b=min(aa, bb),
                  theta=(th if aa >= bb else th+np.pi/2))
        k0 = dict(f0); k0['a'] = f0['a']*0.62; k0['b'] = f0['b']*0.62
        tc = np.nan; fseed = kseed = None
    r = P.analyze2(cs, ks, f0, k0, angles=ang, rho=rho, rho_cap=rho_cap,
                   clip_cap=clip_cap)
    if r is None: return None
    
    r['img'] = img; r['off'] = off; r['cs'] = cs; r['ks'] = ks
    r['fseed'] = fseed; r['kseed'] = kseed; r['t_cream'] = tc
    return r

def overlay(r, out, sc=6):
    from PIL import ImageDraw
    im = Image.fromarray((np.clip(r['img'], 0, 1)*255).astype('uint8'))
    im = im.resize((im.width*sc, im.height*sc), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    for pts, col in ((r['cpts'], (0, 255, 0)), (r['kpts'], (0, 200, 255))):
        for p in pts:
            d.ellipse([p[0]*sc-1, p[1]*sc-1, p[0]*sc+1, p[1]*sc+1], fill=col)
    for f, col in ((r['cream'], (255, 255, 0)), (r['cap'], (255, 0, 255))):
        a = np.linspace(0, 2*np.pi, 400)
        rr = IN.ell_radius(f, a)
        xs = (f['cx']+rr*np.cos(a))*sc; ys = (f['cy']+rr*np.sin(a))*sc
        d.line(list(zip(xs, ys)), fill=col, width=1)
        d.ellipse([f['cx']*sc-3, f['cy']*sc-3, f['cx']*sc+3, f['cy']*sc+3], fill=col)
    im.save(out)
    return out
