import numpy as np
import r51_photo as PH, r51_pipe as P, r51_seed2 as S2

def run(fn, box, cx, cy, rg, capmode='red', clip_cap='both', cap_frac=0.63,
        ang_excl=None, mode='pct'):
    img, off = PH.load(fn, box)
    cs = PH.sc_cream(img)
    ks = PH.sc_red(img) if capmode == 'red' else PH.sc_chromecap(img)
    ang = np.linspace(-np.pi, np.pi, 720, endpoint=False)
    if ang_excl:
        keep = np.ones(len(ang), bool)
        for (a0, a1) in ang_excl:
            keep &= ~((ang >= np.radians(a0)) & (ang <= np.radians(a1)))
        ang = ang[keep]
    f0, fm, t = S2.seed_ellipse(cs, cx, cy, rg, mode)
    if f0 is None: return None
    r = P.analyze3(cs, ks, f0, angles=ang, clip_cap=clip_cap, cap_frac=cap_frac)
    if r is None: return None
    r['img'] = img; r['cs'] = cs; r['ks'] = ks; r['seed'] = f0; r['t'] = t
    return r


def run_best(fn, box, cx, cy, rg, **kw):
    """try both seed thresholds; keep the fit with the SMALLER cream-ring
    residual.  Selection is on fit quality, never on the answer."""
    best = None
    for m in ('otsu', 'pct'):
        try:
            r = run(fn, box, cx, cy, rg, mode=m, **kw)
        except Exception:
            r = None
        if r is None: continue
        r['seedmode'] = m
        if best is None or r['cream']['rms'] < best['cream']['rms']:
            best = r
    return best
