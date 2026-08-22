"""Robust wheel-face seed: largest bright-desaturated blob near a clicked point."""
import numpy as np
from scipy import ndimage as ndi
import r51_inst as IN

def otsu(v):
    hs, be = np.histogram(v, 128)
    p = hs/max(hs.sum(), 1); om = np.cumsum(p)
    ctr = (be[:-1]+be[1:])/2
    mu = np.cumsum(p*ctr); mt = mu[-1]
    with np.errstate(invalid='ignore', divide='ignore'):
        sb = (mt*om - mu)**2/(om*(1-om))
    return float(ctr[np.nanargmax(sb)])

def face_seed(cs, cx, cy, rg, mode='pct'):
    H, W = cs.shape
    x0, x1 = int(max(0, cx-1.6*rg)), int(min(W, cx+1.6*rg))
    y0, y1 = int(max(0, cy-1.6*rg)), int(min(H, cy+1.6*rg))
    win = np.clip(cs[y0:y1, x0:x1], 0.0, None)
    t = otsu(win.ravel()) if mode == 'otsu' else \
        0.5*(np.percentile(win, 55) + np.percentile(win, 98))
    m = np.zeros_like(cs, bool)
    m[y0:y1, x0:x1] = win > t
    m = ndi.binary_closing(m, np.ones((3, 3)))
    lab, n = ndi.label(m)
    if n == 0: return None, t
    yy, xx = np.mgrid[0:H, 0:W]
    near = (xx-cx)**2 + (yy-cy)**2 < (0.92*rg)**2
    best, bs = 0, 0
    for L in range(1, n+1):
        c = (lab == L)
        if not np.any(c & near): continue
        s = c.sum()
        if s > bs: bs, best = s, L
    if best == 0: return None, t
    return ndi.binary_fill_holes(lab == best), t

def seed_ellipse(cs, cx, cy, rg, mode='pct'):
    f, t = face_seed(cs, cx, cy, rg, mode)
    if f is None: return None, None, t
    return IN.init_from_mask(f), f, t
