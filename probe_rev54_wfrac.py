"""
probe_rev54_wfrac.py -- rev 54.  What CAP_EMBLEM_WFRAC actually denominates.

The constant says `w/R as authored (0.0072 / 0.0345)` and 0.0345 was a real
OUTER RADIUS, so the authored intent is w / R_outer.  But `vw_bars` is called
with R=1.0 and the finished glyph is then scaled by `_fit_glyph`, which reads
the outline's own rmax.  If rmax != 1.0 the built ratio is NOT the constant.

Calibrated FIRST on glyphs of KNOWN width, so the estimator's bias is measured
before it is used -- rev 53's lesson about giving a statistic a control.
No scene build: t1_core.vw_bars is called directly in an empty file.
"""
import bpy, os, sys, math
import numpy as np, scipy.ndimage as ndi
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
OUTD = os.path.join(ROOT, "probe_scratch"); os.makedirs(OUTD, exist_ok=True)
import t1_core as T
import t1_detail as D
P = print

def strokes(objs, PX=2000, pad=1.06, paint=None):
    """rmax and stroke width of a glyph lying in the Y-Z plane."""
    vs, polys = [], []
    for ob in objs:
        M = ob.matrix_world
        w = [M @ v.co for v in ob.data.vertices]
        vs.extend(w)
        for p in ob.data.polygons:
            polys.append([w[i] for i in p.vertices])
    rmax = max(math.hypot(v.y, v.z) for v in vs)
    half = rmax * pad; S = PX / (2 * half)
    img = Image.new("L", (PX, PX), 0); dr = ImageDraw.Draw(img)
    for poly in polys:
        dr.polygon([((p.y + half) * S, (half - p.z) * S) for p in poly], fill=255)
    A = np.asarray(img) > 127
    dt = ndi.distance_transform_edt(A) / S
    mx = ndi.maximum_filter(dt, size=3)
    ridge = A & (dt > 0) & (dt >= mx - 1e-12) & (dt > 0.25 * dt.max())
    wr = 2.0 * dt[ridge]
    h, e = np.histogram(wr, bins=80)
    mode = 0.5 * (e[np.argmax(h)] + e[np.argmax(h) + 1])
    if paint:
        ov = np.zeros(A.shape + (3,), np.uint8); ov[A] = (230, 230, 230)
        ov[ridge] = (0, 200, 255)
        Image.fromarray(ov).save(os.path.join(OUTD, paint))
    return rmax, float(np.median(wr)), float(mode), int(ridge.sum())

def fresh():
    bpy.ops.wm.read_factory_settings(use_empty=True)

P("\n=== CALIBRATION -- recover a KNOWN stroke width before trusting the tool ===")
P("%8s %10s %10s %10s %10s %9s" % ("w given", "rmax", "w median", "w MODE", "MODE/given", "ridge px"))
CAL = {}
for w in (0.12, 0.1986, 0.2087, 0.28):
    fresh()
    obs = T.vw_bars(1.0, w, (0, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 0), 0.01,
                    tag="cal")
    rmax, med, mode, npx = strokes(obs, paint="rev54_wfrac_cal_%s.png" % w)
    CAL[w] = (rmax, mode)
    P("%8.4f %10.5f %10.5f %10.5f %10.4f %9d" % (w, rmax, med, mode, mode / w, npx))
P("painted -> probe_scratch/rev54_wfrac_cal_*.png (cyan = the ridge the width")
P("          is read from).  LOOK: the ridge must lie ALONG the strokes.")

P("\n=== rmax OF THE UNIT GLYPH -- the factor _fit_glyph divides by ===")
P("(built w/R_outer = wfrac / rmax, because _fit_glyph scales the whole glyph")
P(" so its extreme corner lands on the target radius)")
for w in sorted(CAL):
    rmax, mode = CAL[w]
    P("  wfrac %.4f -> rmax %.5f -> built w/R_outer would be %.5f" % (w, rmax, w / rmax))

P("\n=== THE TWO BADGES, ON A COMMON DENOMINATOR ===")
CW = D.CAP_EMBLEM_WFRAC
import inspect
NWF = inspect.signature(D.vw_logo_fit).parameters['wfrac'].default
P("hubcap  t1_detail.CAP_EMBLEM_WFRAC          = %.5f" % CW)
P("nose    t1_detail.vw_logo_fit(wfrac=...)    = %.5f   <- the REAL call site;" % NWF)
P("        vw_logo's own signature default w/R = %.5f   (0.0275/0.1385) -- these"
  % (0.0275 / 0.1385))
P("        two agree to %.1e, so the signature is not a second source of truth."
  % abs(NWF - 0.0275 / 0.1385))
rc = CAL[0.2087][0]; rn = CAL[0.1986][0]
P("\nbuilt stroke / OWN OUTER RADIUS:")
P("  hubcap %.5f / %.5f = %.5f" % (CW, rc, CW / rc))
P("  nose   %.5f / %.5f = %.5f" % (NWF, rn, NWF / rn))
P("  the two badge DESIGNS differ by %+.2f %%" % (100.0 * ((CW / rc) / (NWF / rn) - 1)))
P("\nAND THE TRAP FOR THE NEXT REVISION:")
P("  CAP_EMBLEM_WFRAC reads %.5f but the BUILT stroke/outer-radius is %.5f."
  % (CW, CW / rc))
P("  A photograph measures the SECOND.  Comparing a frame against the constant")
P("  itself would be wrong by %+.2f %%." % (100.0 * (CW / (CW / rc) - 1)))
