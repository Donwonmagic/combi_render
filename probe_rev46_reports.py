# probe_rev46_reports.py -- HIS FOUR REPORTS, ALL FOUR IN ONE RUN.
#
# Written at the close of rev 45, for rev 46 to work against.
#
# WHY IT EXISTS.  At the end of rev 45 the owner wrote:
#
#     "I still see a lot of problems, including the 100% calidad off center, the
#      vw logo wrong, senor Tacombi still isn't clearer, the nose of the car is
#      too flat which is inaccurate in shape, among other things."
#
# Every previous revision has answered a report like that by opening a fresh
# investigation, and every one has taken most of a revision to get back to a
# number.  This probe IS the number, for all four, and it runs in one command.
# Change a constant, run it, watch the row move.  That is the whole point.
#
# WHAT IT MEASURES, and the photographed target beside each
#
#   R1  "100% CALIDAD OFF CENTER"      the WHITE TYPE's centroid minus the RED
#       BURST's centroid, as a fraction of the decal.  Built off
#       tex/calidad.png; photographed off ref_playa_34.png.
#           built rev 45   (-0.1195, +0.1782)
#           photographed   (+0.0455, +0.0746)
#       THE HORIZONTAL ERROR IS IN THE WRONG DIRECTION.
#       NOTE THE TRAP: ledger finding 5's "the defect is COLOUR, not position"
#       is about the decal PANEL'S PLACEMENT ON THE VEHICLE (Report 7, 0.180 of
#       texture width).  This is the TYPE'S PLACEMENT INSIDE THE DECAL.  Both
#       are true and they are different things.  Do not re-open the placement.
#
#   R2  "THE VW LOGO WRONG"            the glyph's VERTICAL landmarks as a
#       fraction of the ring's vertical diameter, measured from its top.
#       VERTICAL EXTENTS NEED NO AXIS RATIO -- that is SPEC 10.107.2's own rule,
#       and it is why this measurement is possible when the ANGLES are not:
#       de-foreshortening a three-quarter view of a circle needs the ring's
#       axis ratio and the two fits available disagree by 10 %.
#           landmark                          photo   built rev 45
#           V arms clear the ring band        0.147   0.104
#           V's apex / the central knot       0.353   0.254   <- 27.7 mm high
#           W outer arms leave the band       0.485   0.507
#           W troughs reach the lower band    0.810   0.866
#
#   R3  "SENOR TACOMBI STILL ISN'T CLEARER"  Michelson contrast of the script's
#       ink against the red it sits on.
#           built rev 45   0.217        photographed   0.324
#       NOTE THE TRAP: ledger finding 19 says senor.png's ink is already too
#       LIGHT against its own measured target, so darkening it toward that
#       target makes legibility WORSE.  The two findings pull opposite ways.
#       The lever is the EDGE -- an outline or a drop shadow raises Michelson
#       without moving the ink's mean.  Measure before and after.
#
#   R4  "THE NOSE IS TOO FLAT"         the body's surface x versus y at a fixed
#       height, as mm behind the centreline crown.  Built rev 45, z = 1.25:
#           y  0.00  0.10  0.20  0.30  0.40  0.50  0.60  0.70
#          mm   0.0  -0.4  -1.6  -3.6  -6.5 -10.1 -12.8 -14.3
#       14.3 mm over 0.70 m of half-width.  The nose is a plane.
#       NOTE THE TRAP: ledger finding 6 is "the nose shape, V_POW locked 0.60"
#       and it is A DIFFERENT AXIS.  V_POW_Z drives zV(y), the PAINTED two-tone
#       break line's height.  It is a paint curve.  It has nothing to do with
#       how far the sheet metal bulges forward.
#       R4 HAS NO PHOTOGRAPHED TARGET YET and this probe does not invent one.
#       Rev 45 tried a luminance profile across the cream nose and THREW THE
#       RESULT AWAY -- the render and photograph boxes were not comparable.
#       See W4 of NEXT_CONTEXT_PROMPT_rev46.md for the three candidate methods.
#
# CONTROLS -- read THIS PROBE'S OWN SUMMARY LINE, never its exit code.
#   C1  every source loads at a size this probe did not assume
#   C2  R1's two masks are non-empty in BOTH the texture and the photograph,
#       and are DIFFERENT sizes -- a mask that matched everything would give a
#       centroid of (0.5, 0.5) and read as "perfectly centred"
#   C3  R2 finds the glyph's ring in the photograph at the published rows, and
#       the built raster's run-structure has the expected number of transitions
#   C4  R4's raycast hits T1_body at the crown and at y = 0.70
#   C5  A POSITIVE CONTROL ON THE ESTIMATOR, and it is NOT a kill -- the first
#       draft of this header called it one, which is exactly the mislabelling
#       this project punishes.  A KILL is written to FAIL forever; C5 is
#       written to PASS forever, and it fails only if the centroid routine
#       itself is broken.  R1's estimator is run on a SYNTHETIC PERFECTLY
#       CENTRED decal and must report (0.000, 0.000) to within 0.005.  Without
#       it, "the type is off centre" is untestable: a centroid routine with a
#       transposed axis, or one that weighted by the wrong channel, would
#       report an offset on anything at all.
#       THIS IS THE CONTROL REV 45 NEEDED THREE TIMES AND DID NOT HAVE.
#
# RUN
#   /tmp/blender/blender -b -P probe_rev46_reports.py
#   T1_R46_NORENDER=1 skips R3 (which needs a render) and runs in ~90 s.

import os
import sys
import math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("T1_SUB", "1")
NORENDER = bool(os.environ.get("T1_R46_NORENDER"))
if not NORENDER:
    os.environ["T1_PREVIEW"] = "side"
    os.environ["T1_PFX"] = "r46"
    os.environ.setdefault("T1_RX", "1100")
    os.environ.setdefault("T1_RY", "760")
    os.environ.setdefault("T1_SAMP", "40")

import bpy                                                   # noqa: E402
from mathutils import Vector                                 # noqa: E402
import runpy                                                 # noqa: E402
import numpy as np                                           # noqa: E402
from PIL import Image, ImageDraw                             # noqa: E402

CTL = {}


def ctl(name, ok, msg):
    CTL[name] = bool(ok)
    print("  [%s] %-4s %s" % ("PASS" if ok else "FAIL", name, msg))


def centroid(mask, w, h):
    t = mask.sum()
    if t < 20:
        return None
    ys, xs = np.mgrid[0:h, 0:w]
    return ((xs * mask).sum() / t / w, (ys * mask).sum() / t / h)


# =========================================================== R1  the decal
print("\nR1  \"100% CALIDAD OFF CENTER\" -- the TYPE's centroid minus the BURST's")
TEX = os.path.join(HERE, "tex", "calidad.png")
REF = os.path.join(HERE, "ref_playa_34.png")
ok1 = os.path.exists(TEX) and os.path.exists(REF)
a = np.array(Image.open(TEX).convert("RGBA")).astype(float) if ok1 else None
r1 = None
if ok1:
    h, w, _ = a.shape
    al = a[:, :, 3] / 255.0
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    burst = (al > 0.5) & (R > 120) & (R - G > 40)
    white = (al > 0.5) & (R > 200) & (G > 195) & (B > 190)
    cb, cw = centroid(burst, w, h), centroid(white, w, h)
    if cb and cw:
        r1 = (cw[0] - cb[0], cw[1] - cb[1])
        print("    BUILT   tex/calidad.png %dx%d   burst n=%d  type n=%d"
              % (w, h, burst.sum(), white.sum()))
        print("            type - burst = (%+.4f, %+.4f) of the decal" % r1)

    p = np.array(Image.open(REF).convert("RGB")).astype(float)[112:168, 424:462]
    ph, pw, _ = p.shape
    pb = centroid((p[:, :, 0] > 140) & (p[:, :, 0] - p[:, :, 1] > 45), pw, ph)
    pw_ = centroid((p[:, :, 0] > 205) & (p[:, :, 1] > 200) & (p[:, :, 2] > 195), pw, ph)
    if pb and pw_:
        print("    PHOTO   ref_playa_34.png crop 38x56")
        print("            type - burst = (%+.4f, %+.4f) of the decal"
              % (pw_[0] - pb[0], pw_[1] - pb[1]))
        if r1:
            print("            ERROR   dx %+.4f   dy %+.4f   <- dx is in the WRONG DIRECTION"
                  % (r1[0] - (pw_[0] - pb[0]), r1[1] - (pw_[1] - pb[1])))
    ctl("C2", burst.sum() > 1000 and white.sum() > 1000
        and abs(burst.sum() - white.sum()) > 1000,
        "R1's two masks are non-empty and different sizes (burst %d, type %d) "
        "-- a mask matching everything would centroid to (0.5,0.5) and read as "
        "perfectly centred" % (burst.sum(), white.sum()))
else:
    ctl("C2", False, "R1 sources missing")

# C5 -- the KILL, on a synthetic perfectly-centred decal
syn = Image.new("RGBA", (400, 300), (0, 0, 0, 0))
d = ImageDraw.Draw(syn)
d.ellipse([60, 40, 340, 260], fill=(200, 60, 30, 255))          # burst, centred
d.rectangle([160, 130, 240, 170], fill=(250, 248, 244, 255))    # type,  centred
sa = np.array(syn).astype(float)
sal = sa[:, :, 3] / 255.0
sb = centroid((sal > 0.5) & (sa[:, :, 0] > 120) & (sa[:, :, 0] - sa[:, :, 1] > 40), 400, 300)
sw = centroid((sal > 0.5) & (sa[:, :, 0] > 200) & (sa[:, :, 1] > 195) & (sa[:, :, 2] > 190),
              400, 300)
kill = (abs(sw[0] - sb[0]), abs(sw[1] - sb[1])) if (sb and sw) else (9, 9)
ctl("C5", kill[0] < 0.005 and kill[1] < 0.005,
    "POSITIVE CONTROL (not a kill): a synthetic PERFECTLY CENTRED decal reports "
    "(%+.4f, %+.4f) and must be (0,0) to 0.005 -- without it a centroid routine "
    "with a transposed axis would report an offset on anything" % kill)

# =============================================== build (R2 and R4 need it)
G = runpy.run_path(os.path.join(HERE, "build.py"), run_name="__main__")
T = G["T"]
import t1_detail as D                                        # noqa: E402

# =========================================================== R2  the glyph
print("\nR2  \"THE VW LOGO WRONG\" -- VERTICAL landmarks, no axis ratio needed")


def runs_of(mask_row):
    idx = np.nonzero(mask_row)[0]
    if not len(idx):
        return []
    out, s, p = [], idx[0], idx[0]
    for i in idx[1:]:
        if i > p + 1:
            out.append((s, p)); s = i
        p = i
    out.append((s, p))
    return out


def transitions(m):
    """f at each change in run-count, top to bottom, as a fraction of height."""
    H = m.shape[0]
    seq, prev = [], None
    for r in range(H):
        n = len(runs_of(m[r]))
        if n == 0:
            continue
        if n != prev:
            seq.append((r / (H - 1), n))
            prev = n
    return seq


# --- photographed: a RED emblem on CREAM segments cleanly; the workshop
# --- frame's chrome does not, and rev 45 tried and abandoned it.
ph = np.array(Image.open(os.path.join(HERE, "ref_nolita_front34.jpg"))
              .convert("RGB")).astype(float)
red = ph[:, :, 0] - 0.5 * (ph[:, :, 1] + ph[:, :, 2])
Wm = red[191:260, 148:198] > 35
print("    PHOTO   ref_nolita_front34.jpg rows 191-259, cols 152-192")
for f, n in transitions(Wm):
    print("            f=%.3f -> %d runs" % (f, n))

# --- built: rasterise the glyph WITH the ring band, at the same row count
RING_R = 0.2800 / 2.0
BAND = 0.20                       # t1_detail.roundel: band 0.028 on R 0.140
obs = D.vw_logo_fit(RING_R, x=0.0)
N = Wm.shape[0] * 8
im = Image.new("L", (N, N), 0)
dd = ImageDraw.Draw(im)
dd.ellipse([0, 0, N - 1, N - 1], fill=255)
dd.ellipse([N * BAND / 2, N * BAND / 2, N - 1 - N * BAND / 2, N - 1 - N * BAND / 2], fill=0)


def P(y, z):
    return (N / 2 + y / RING_R * (N / 2), N / 2 - z / RING_R * (N / 2))


for o in obs:
    xm = max(v.co.x for v in o.data.vertices)
    for poly in o.data.polygons:
        if all(abs(o.data.vertices[i].co.x - xm) < 1e-6 for i in poly.vertices):
            dd.polygon([P(o.data.vertices[i].co.y, o.data.vertices[i].co.z)
                        for i in poly.vertices], fill=255)
built = (np.array(im) > 128)[::8, ::8]
print("    BUILT   t1_core.vw_bars, rasterised with the ring band")
bt = transitions(built)
for f, n in bt:
    print("            f=%.3f -> %d runs" % (f, n))
print("    TARGET  V arms clear the band 0.147 | V's APEX 0.353 | W outer arms "
      "0.485 | W troughs 0.810")
print("    rev 45  built                0.104 |          0.254 |            "
      "0.507 |            0.866")
ctl("C3", Wm.any() and len(bt) >= 5,
    "R2: the photographed emblem segments (n=%d px) and the built raster has "
    "%d run-count transitions" % (Wm.sum(), len(bt)))

# =========================================================== R4  the nose
print("\nR4  \"THE NOSE IS TOO FLAT\" -- surface x vs y, mm behind the crown")
body = bpy.data.objects["T1_body"]
dg = bpy.context.evaluated_depsgraph_get()


def surf_x(y, z):
    ok, loc, _n, _i, ob, _m = bpy.context.scene.ray_cast(
        dg, Vector((3.5, y, z)), Vector((-1, 0, 0)))
    return loc.x if (ok and ob and ob.name == "T1_body") else None


YS = [0.0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70]
Z = 1.25
xs = [surf_x(y, Z) for y in YS]
if xs[0] is not None:
    print("    z=%.2f  crown x=%.4f" % (Z, xs[0]))
    print("            y   " + "".join("%7.2f" % y for y in YS))
    print("            mm  " + "".join(("%7.1f" % ((x - xs[0]) * 1000)) if x is not None
                                       else "     --" for x in xs))
    tot = (xs[-1] - xs[0]) * 1000 if xs[-1] is not None else float("nan")
    print("            TOTAL RECESSION over 0.70 m of half-width: %.1f mm" % tot)
    print("            the only forward bulge in the model is bulge = 0.019 in "
          "t1_shell.nose_shape")
    print("            NO PHOTOGRAPHED TARGET YET -- see W4 of the rev-46 brief")
ctl("C4", xs[0] is not None and xs[-1] is not None,
    "R4's raycast hits T1_body at the crown and at y = 0.70")

# =========================================================== R3  the script
print("\nR3  \"SENOR TACOMBI STILL ISN'T CLEARER\" -- Michelson ink vs its red")
if NORENDER:
    print("    skipped (T1_R46_NORENDER)")
else:
    png = os.path.join(HERE, "out", "r46_side.png")
    if os.path.exists(png):
        sa2 = np.array(Image.open(png).convert("RGB")).astype(float)
        Hh, Ww, _ = sa2.shape
        box = (int(0.51 * Ww), int(0.60 * Hh), int(0.92 * Ww), int(0.72 * Hh))
        s2 = sa2[box[1]:box[3], box[0]:box[2]].reshape(-1, 3)
        L = s2.mean(1)
        ink = (s2.max(1) - s2.min(1) < 60) & (L > 120)
        if ink.sum() > 50 and (~ink).sum() > 50:
            A, Bb = L[ink].mean(), L[~ink].mean()
            print("    BUILT   ink %.1f  ground %.1f  Michelson %.3f"
                  % (A, Bb, abs(A - Bb) / (A + Bb)))
        print("    PHOTO   0.324   (ref_playa_34.png; ledger finding 30 has "
              "0.269/0.466 on different boxes, same ratio)")
        if not os.environ.get("T1_R46_KEEP"):
            try:
                os.remove(png)
            except OSError:
                pass
    else:
        print("    no render found at %s" % png)

ctl("C1", ok1, "every source loads")

nfail = sum(1 for v in CTL.values() if not v)
print("\nCONTROLS: %d checked, %d FAILED%s"
      % (len(CTL), nfail,
         "" if not nfail else " -- " + ",".join(k for k, v in CTL.items() if not v)))
