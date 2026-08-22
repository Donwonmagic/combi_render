"""
probe_rev54_badge.py -- rev 54, brief sec.3 item 1, THE UNBLOCKED HALF.

The brief's top job is the two VW badges and it is blocked on a photograph.
This is the part that is NOT blocked: what the BUILT MESH actually realises,
and whether the two independently-authored glyphs agree with each other.

  hubcap  t1_detail.CAP_EMBLEM_WFRAC = 0.2087   (0.0072 / 0.0345, and 0.0345
                                                 was the OLD rev-14 radius)
  nose    t1_detail.vw_logo(R=0.1385, w=0.0275) -> 0.19856

Those are the SOURCE's numbers.  Nothing has ever asked the MESH whether the
built glyphs realise them, and no row in either verifier names a cap, rim,
hub, spoke or either badge constant -- measured at rev 54, see the ledger.

Rule 6: compare two INDEPENDENTLY obtained quantities.  Rule 8: the raster is
a window, so it is painted and looked at before it produces a number.
"""
import bpy, bmesh, os, sys, math
import numpy as np
import scipy.ndimage as ndi
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
OUTD = os.path.join(ROOT, "probe_scratch")
os.makedirs(OUTD, exist_ok=True)

src = open(os.path.join(ROOT, "build.py")).read().split('if os.environ.get("T1_SAVE")')[0]
exec(compile(src, "build.py", "exec"))

P = print
def hdr(t): P("\n=== %s ===" % t)

import t1_detail as D

hdr("WHAT THE SOURCE SAYS")
P("CAP_EMBLEM_D    = %.6f * CAP_D" % 0.3170)
P("CAP_EMBLEM_WFRAC= %.5f    <- hubcap glyph, w/R" % D.CAP_EMBLEM_WFRAC)
import inspect
sg = inspect.signature(D.vw_logo)
NR = sg.parameters['R'].default; NW = sg.parameters['w'].default
P("vw_logo default R=%.5f w=%.5f -> w/R = %.5f   <- nose glyph"
  % (NR, NW, NW / NR))
P("the two DISAGREE by %.2f %%" % (100.0 * (D.CAP_EMBLEM_WFRAC / (NW / NR) - 1)))


# ---------------------------------------------------------------------------
# THE FIRST VERSION OF THIS PROBE TOOK EVERY OBJECT WHOSE NAME STARTS `capring`
# AND CALLED THE RESULT "the ring".  There are FOUR hubcaps, so the "ring" came
# out as a 2.486 m circle spanning the wheelbase with two 20 mm glyphs at the
# axle stations, and w/R read 0.01136.  It was caught in one second by LOOKING
# at probe_scratch/rev54_badge_hubcap.png -- the red circle is the whole
# vehicle.  Rule 8, and the project's most-repeated defect, live again.
# The instances are separated by CLUSTERING on the ring centroids below, and
# all four are reported so they act as controls on each other.
# ---------------------------------------------------------------------------

def obj_verts(objs):
    polys, allv = [], []
    for ob in objs:
        M = ob.matrix_world
        vs = [M @ v.co for v in ob.data.vertices]
        allv.extend(vs)
        for p in ob.data.polygons:
            polys.append([vs[i] for i in p.vertices])
    return allv, polys


def centroid(ob):
    M = ob.matrix_world
    vs = [M @ v.co for v in ob.data.vertices]
    return sum(vs, mathutils.Vector((0, 0, 0))) / len(vs)


import mathutils


def measure_glyph(tag, glyph_objs, ring_objs, uax, vax, PX=1400, paint=True):
    U = mathutils.Vector(uax).normalized(); V = mathutils.Vector(vax).normalized()
    gv, gp = obj_verts(glyph_objs)
    rv, rp = obj_verts(ring_objs)
    if not gv or not rv:
        P("  %s: missing objects" % tag); return None
    ru = np.array([U.dot(p) for p in rv]); rvv = np.array([V.dot(p) for p in rv])
    cu, cv = 0.5 * (ru.min() + ru.max()), 0.5 * (rvv.min() + rvv.max())
    R_out = 0.5 * max(ru.max() - ru.min(), rvv.max() - rvv.min())

    half = R_out * 1.10
    S = PX / (2 * half)
    img = Image.new("L", (PX, PX), 0); dr = ImageDraw.Draw(img)
    for poly in gp:
        dr.polygon([((U.dot(p) - cu + half) * S, (half - (V.dot(p) - cv)) * S)
                    for p in poly], fill=255)
    A = np.asarray(img) > 127
    dt = ndi.distance_transform_edt(A) / S
    mx = ndi.maximum_filter(dt, size=3)
    ridge = A & (dt > 0) & (dt >= mx - 1e-12) & (dt > 0.25 * dt.max())
    if ridge.sum() < 10:
        P("  %s: ridge too small (%d px)" % (tag, ridge.sum())); return None
    w_ridge = 2.0 * dt[ridge]
    hist, edges = np.histogram(w_ridge, bins=60)
    mode = 0.5 * (edges[np.argmax(hist)] + edges[np.argmax(hist) + 1])
    if paint:
        ov = np.zeros(A.shape + (3,), np.uint8); ov[A] = (235, 235, 235)
        yy, xx = np.mgrid[0:PX, 0:PX]
        rr = np.hypot(xx - PX / 2.0, yy - PX / 2.0)
        ov[np.abs(rr - R_out * S) < 1.5] = (255, 0, 0)
        ov[ridge] = (0, 200, 255)
        Image.fromarray(ov).save(os.path.join(OUTD, "rev54_badge_%s.png" % tag))
    return dict(tag=tag, R_out=R_out, glyph_px=int(A.sum()), ridge_px=int(ridge.sum()),
                w_med=float(np.median(w_ridge)), w_mode=float(mode),
                ratio_med=float(np.median(w_ridge)) / R_out,
                ratio_mode=float(mode) / R_out)


hdr("HUBCAP GLYPHS -- ONE PER WHEEL, clustered on the ring centroids")
rings = [o for o in bpy.data.objects
         if o.type == 'MESH' and o.name.startswith("capring")]
glyphs = [o for o in bpy.data.objects
          if o.type == 'MESH' and o.name.startswith("capvw")]
P("found %d capring and %d capvw objects" % (len(rings), len(glyphs)))
CAPS = []
for r in rings:
    rc = centroid(r)
    mine = [g for g in glyphs if (centroid(g) - rc).length < 0.15]
    res = measure_glyph("cap_%s" % r.name, mine, [r], (1, 0, 0), (0, 0, 1))
    if res:
        res['centre'] = tuple(round(v, 4) for v in rc)
        CAPS.append(res)
        P("  %-16s centre %-28s R %.6f  glyph objs %d  w/R med %.5f mode %.5f"
          % (r.name, res['centre'], res['R_out'], len(mine),
             res['ratio_med'], res['ratio_mode']))

hdr("NOSE GLYPH")
nring = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith("vw_ring")]
nbar = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith("vwbar")]
P("found %d vw_ring and %d vwbar objects" % (len(nring), len(nbar)))
NOSE = measure_glyph("nose", nbar, nring, (0, 1, 0), (0, 0, 1))
if NOSE:
    P("  R %.6f  w med %.6f mode %.6f  ->  w/R med %.5f mode %.5f"
      % (NOSE['R_out'], NOSE['w_med'], NOSE['w_mode'],
         NOSE['ratio_med'], NOSE['ratio_mode']))

hdr("THE COMPARISON -- source against mesh, and glyph against glyph")
P("%-14s %11s %10s %10s %11s" % ("glyph", "source w/R", "mesh med", "mesh mode", "outer R m"))
for c in CAPS:
    P("%-14s %11.5f %10.5f %10.5f %11.6f"
      % (c['tag'], D.CAP_EMBLEM_WFRAC, c['ratio_med'], c['ratio_mode'], c['R_out']))
if NOSE:
    P("%-14s %11.5f %10.5f %10.5f %11.6f"
      % ("nose", NW / NR, NOSE['ratio_med'], NOSE['ratio_mode'], NOSE['R_out']))
if CAPS:
    rs = [c['ratio_mode'] for c in CAPS]
    P("\nthe four hubcaps agree with each other to %.4f (spread %.2e) -- a control"
      % (max(rs) - min(rs), max(rs) - min(rs)))
    P("hubcap mesh mode %.5f vs its own constant %.5f -> %+.2f %%"
      % (rs[0], D.CAP_EMBLEM_WFRAC, 100.0 * (rs[0] / D.CAP_EMBLEM_WFRAC - 1)))
if CAPS and NOSE:
    P("nose   mesh mode %.5f vs its own constant %.5f -> %+.2f %%"
      % (NOSE['ratio_mode'], NW / NR, 100.0 * (NOSE['ratio_mode'] / (NW / NR) - 1)))
    P("\nHUBCAP vs NOSE, as BUILT: %.5f vs %.5f -> the two glyphs differ by %+.2f %%"
      % (rs[0], NOSE['ratio_mode'], 100.0 * (rs[0] / NOSE['ratio_mode'] - 1)))
    P("HUBCAP vs NOSE, in SOURCE: %.5f vs %.5f -> %+.2f %%"
      % (D.CAP_EMBLEM_WFRAC, NW / NR, 100.0 * (D.CAP_EMBLEM_WFRAC / (NW / NR) - 1)))
P("\npainted -> probe_scratch/rev54_badge_*.png  (red = ring R, cyan = the ridge)")
