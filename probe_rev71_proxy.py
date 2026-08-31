# probe_rev71_proxy.py -- rev 71.  A 2-D REPLICA OF THE EMBLEM RASTER, PROVEN
# BIT-IDENTICAL TO THE bpy BUILD ON THE KNOWN ANSWER FIRST.
#
# WHY.  Every emblem search in this project has gone through `vw_logo_fit`,
# which builds meshes.  Rev 66 proved the method that makes emblem work
# affordable -- *"the emblem's whole search was done in a PURE-2-D replica with
# no bpy, validated on a KNOWN ANSWER first, while Blender had all four cores"*
# -- and then no later revision had a replica to use.  This is that replica,
# kept, so the next context does not rebuild it.
#
# IT IS NOT AN APPROXIMATION.  It calls `t1_core._mitre_outline` -- the SAME
# function the build calls -- and reproduces `vw_bars`' terminal fixed point and
# `vw_logo_fit`'s `_fit_glyph` scaling.  `prove()` scores it against
# `probe_rev69_fitpose.unit_mask()`, i.e. against the real bpy build:
#     PROXY-vs-BUILT IoU 1.000000, 41255 on-pixels each, at 276 rows.
# RUN `prove()` BEFORE TRUSTING ANY NUMBER FROM IT (rule 3): if it ever drifts
# from the build, the proxy is wrong and its searches are void.
#
# ONE EVALUATION IS ~0.01 s AGAINST ~2 s THROUGH bpy.
import os, sys, math
import numpy as np
sys.path.insert(0, '/home/user/combi_render')
from PIL import Image, ImageDraw
import bpy
from mathutils import Vector
import t1_core as C

NPX = 69 * 8
BAND = 0.20
RING_INNER_FRAC = 1.0 - 2.0 * 0.093
BAND_FRAC = 0.028 / 0.140
import t1_detail as _D
FIT_R = 1.0 - _D.VW_FIT_COEF * BAND_FRAC   # READ LIVE from t1_detail, never typed:
#   the proxy must track the build or its searches are void (F251/F256)

def spines(p):
    """p: dict of the free parameters.  Returns V and W spines in R=1 units."""
    on = p.get('on_band', True)
    def ob(q):
        if not on: return q
        r = math.hypot(*q); k = RING_INNER_FRAC / r
        return (q[0]*k, q[1]*k)
    ty = (RING_INNER_FRAC**2 - p['V_TIP_X']**2) ** 0.5 if on else p['V_TIP_Z']
    V = [ob((-p['V_TIP_X'], ty)), (0.0, p['APEX_Z']), ob((p['V_TIP_X'], ty))]
    W = [ob((-p['W_ARM_X'], p['W_ARM_Z'])), ob((-p['W_TR_X'], p['W_TR_Z'])),
         (0.0, p['W_PEAK_Z']),
         ob((p['W_TR_X'], p['W_TR_Z'])), ob((p['W_ARM_X'], p['W_ARM_Z']))]
    return V, W

def outlines(p, w):
    """The two mitred outlines, terminals driven onto the band, then fit-scaled."""
    V0, W0 = spines(p)
    arc_r = RING_INNER_FRAC
    term = [('V',0),('V',2),('W',0),('W',1),('W',4),('W',3)]
    ENDS = {('V',0),('V',2),('W',0),('W',4)}
    drive = [t for t in term if t not in ENDS]     # arc cut ON -> only the troughs
    rad = {t: RING_INNER_FRAC for t in term}
    for _ in range(40):
        V = list(V0); W = list(W0)
        for (wh, i) in term:
            base = V0[i] if wh=='V' else W0[i]
            k = rad[(wh,i)] / RING_INNER_FRAC
            if wh=='V': V[i] = (base[0]*k, base[1]*k)
            else:       W[i] = (base[0]*k, base[1]*k)
        reach, worst = {}, 0.0
        for wh, sp in (('V',V),('W',W)):
            ol = C._mitre_outline([(x,y) for (x,y) in sp], w, arc_r=arc_r)
            for (px,py) in ol:
                j = min(range(len(sp)), key=lambda k:(px-sp[k][0])**2+(py-sp[k][1])**2)
                if (wh,j) in rad:
                    reach.setdefault((wh,j), []).append(math.hypot(px,py))
        for t in drive:
            rs = sorted(reach.get(t,[]), reverse=True)
            if not rs or rs[0] <= 1e-9: continue
            e = RING_INNER_FRAC / rs[0]
            worst = max(worst, abs(e-1.0)); rad[t] *= e
        if worst < 1e-9: break
    V = list(V0); W = list(W0)
    for (wh,i) in term:
        base = V0[i] if wh=='V' else W0[i]
        k = rad[(wh,i)] / RING_INNER_FRAC
        if wh=='V': V[i] = (base[0]*k, base[1]*k)
        else:       W[i] = (base[0]*k, base[1]*k)
    outs = [C._mitre_outline(list(sp), w, arc_r=arc_r) for sp in (V, W)]
    ex = max(math.hypot(x,y) for o in outs for (x,y) in o)
    s = FIT_R / ex
    return [[(x*s, y*s) for (x,y) in o] for o in outs]

def mask(p, w, rows=220, npx=NPX):
    im = Image.new("L",(npx,npx),0); d = ImageDraw.Draw(im)
    d.ellipse([0,0,npx-1,npx-1], fill=255)
    d.ellipse([npx*BAND/2, npx*BAND/2, npx-1-npx*BAND/2, npx-1-npx*BAND/2], fill=0)
    def P(y,z): return (npx/2 + y*(npx/2), npx/2 - z*(npx/2))
    for o in outlines(p, w):
        d.polygon([P(x,y) for (x,y) in o], fill=255)
    k = max(1, npx//rows)
    return (np.array(im) > 128)[::k,::k]

SHIPPED = dict(V_TIP_X=C.VW_V_TIP_X, APEX_Z=C.VW_APEX_Z, W_ARM_X=C.VW_W_ARM_X,
               W_ARM_Z=C.VW_W_ARM_Z, W_TR_X=C.VW_W_TROUGH_X, W_TR_Z=C.VW_W_TROUGH_Z,
               W_PEAK_Z=C.VW_W_PEAK_Z, on_band=True)
WFRAC = 0.2283


def prove(rows=276, verbose=True):
    """The KNOWN ANSWER: this proxy against the real bpy build.  Returns IoU."""
    import probe_rev69_fitpose as F
    built = F.unit_mask(rows=rows)
    prox = mask(SHIPPED, WFRAC, rows=rows)
    inter = (built & prox).sum()
    union = (built | prox).sum()
    v = float(inter) / union if union else 0.0
    if verbose:
        print("  PROXY vs BUILT (bpy) at %d rows: IoU %.6f   on-px %d / %d"
              % (rows, v, built.sum(), prox.sum()))
        print("  %s" % ("[PASS] the proxy IS the build" if v > 0.999 else
                        "[FAIL] THE PROXY HAS DRIFTED FROM THE BUILD -- its "
                        "searches are VOID until this is fixed"))
    return v


if __name__ == "__main__":
    prove()
