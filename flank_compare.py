"""
flank_compare.py -- the acceptance test for the flank script, against the RENDER.

Donald's terms, verbatim: "render the flank, crop the script to the same
framing as the reference, and show me the two side by side at matched scale."

WHAT THIS TEST USED TO BE, AND WHY IT COULD NOT FAIL
Up to rev 13 this file computed no number at all.  It printed three provenance
lines and stacked two JPEG crops.  It had three framing decisions and two of
them cancelled, so the pair looked MORE alike than they were:

  1. It cropped the reference with `REF_INK = (5, 4, 276, 103)` inside
     `REF_CROP = (325, 486, ...)`, i.e. it threw away four rows off the top of
     the ink -- and SPEC 10.20 had already established that the missing rows
     are at the TOP and that they are the top of `Senor`.  `compare_script.py`
     was fixed in rev 10; this file was not.
  2. It projected the panel from a COPY of build.py's SCR, and the copy went
     stale: it still carried z1 = 0.9154 after build.py moved to 0.9896 in
     rev 11.  It also projected the AUTHORED z, but build.py step 8b shears
     every non-wheel vertex down by `RAKE_Z0 + RAKE_DZDX * x` AFTER the decal
     is placed, so the RENDERED panel is 61.8 mm lower at x0 and 39.2 mm lower
     at x1 than the authored one.  This file had no rake term at all.
  3. It resampled both panels to the same WIDTH and let each height follow its
     own aspect.  That is the one operation guaranteed to hide an aspect-ratio
     error -- and an aspect-ratio error is exactly what rev 11 found (the
     panel had been squashed 15.8 % vertically for three revisions).

All three are fixed below, and the file now prints measurements with their
ceiling instead of an impression.

    python3 flank_compare.py [out/p_side.png] [out/flank_compare.png]

The render it compares against is the ortho side probe, produced with:

    T1_SUB=1 T1_PREVIEW=side T1_SAMP=32 T1_RX=1600 T1_RY=1100 T1_FX=0 \
        T1_PFX=p /tmp/blender/blender -b --python build.py

T1_FX=0 matters: chromatic aberration displaces R against B by a fraction of a
pixel across the frame, and every mask here is a CHROMATICITY rule.  A
measurement probe is rendered without the taking-lens artefacts; post.py puts
them back on the pictures that are meant to be looked at.
"""
import ast
import os
import sys
import time

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)                 # compare_script.ref_mask() opens ref_side.jpg by
                               # relative path, so this test is cwd-independent
                               # and both argv paths resolve against the repo
import compare_script as CS    # noqa: E402  -- the ESTABLISHED reference rule

# ===========================================================================
# THRESHOLDS.  Every one of them carries where it came from.  None of them is
# a score out of 100: each is a measurement against the reference, and the IoU
# is quoted against a ceiling measured in the same run.
# ===========================================================================

# Ink-area ratio, render / reference.  SPEC 10.20 puts the reference footprint
# itself at 9 129 +/- 300 px, i.e. +/- 3.3 %, and the mask edge is a
# half-covered-pixel locus whose threshold sensitivity is measured and printed
# below.  0.10 is three times the reference's own uncertainty, so it cannot
# fire on measurement noise, and it sits inside the 11-13 % deficit AUDIT_rev11
# recorded ("Ink 12.5 % light"), so it does fire on that.  It is the weakest of
# the four checks: the render mask's own 25-75 % coverage band is about the
# same size, and that band is printed next to the ratio for exactly that reason.
AREA_TOL = 0.10

# Aspect ratio, ink bbox w/h.  This is the metric the old test could not see.
# It is DIMENSIONLESS, so it does not depend on px/m on either side and no
# scale error can cancel it.  The reference's own aspect uncertainty is the
# projection isotropy (h/v 0.9989 +/- 0.010, AUDIT_rev11) plus a pixel of bbox
# edge on 270 x 115 px, about 1.5 % combined.  0.05 is three sigma of that,
# and one third of the 15.8 % squash that went unnoticed for three revisions.
ASPECT_TOL = 0.05

# IoU is quoted as a FRACTION OF THE CEILING measured this run, never as a
# bare number -- a bare IoU means nothing without knowing what a perfect
# redraw would score.  AUDIT_rev11: `Tacombi` passes at 0.873 against a 0.899
# ceiling (0.971 of ceiling); the broken `Senor` scored 0.454 against the same
# 0.90 (0.505 of ceiling).  0.85 sits between them.
IOU_FRAC_OF_CEILING = 0.85

# Same idea per glyph region, and looser, because a small region loses more of
# itself to the same pixel of slop and because the region boxes are generous.
# 0.75 still sits between AUDIT_rev11's `Tacombi` (0.971 of ceiling) and its
# `Senor` (0.505).  This check exists because a whole-lockup IoU is dominated
# by the biggest glyph: rev 11 recorded 0.942 whole-lockup with `Senor` at
# 0.454 inside it.
REGION_IOU_FRAC = 0.75

# Inherited, NOT measured by this script: AUDIT_rev11's ceiling for this
# comparison.  Printed alongside the ceiling this run measures, so the two can
# be checked against each other.
CEILING_INHERITED = 0.90            # AUDIT_rev11, "THE SCRIPT AND THE CALIDAD DECAL"
CEILING_INHERITED_1PX = 0.87        # ... "or 0.87 with 1 px of registration slop"

# Reference scale.  AUDIT_rev11, same section: "scale 211.2 +/- 1.0 px/m from
# the locked wheelbase and independently from the bay frame lines", with
# projection isotropy h/v 0.9989 +/- 0.010 (subpixel conic fit to the rear
# hubcap ring, 180 rays) -- so one scalar is enough for both axes.
REF_PPM = 211.2
REF_PPM_SD = 1.0

SEARCH = 14                    # +/- px of registration search, at REF_PPM this
                               # is +/- 66 mm.  Reported, and flagged if the
                               # optimum lands on the boundary.
PROJ_TOL_PX = 3.0              # projection self-check.  The tyre is TANGENT to
                               # z = 0, so its coverage falls off quadratically
                               # and the last fully dark row sits 1-2 px inside
                               # the geometric ground line at a 1.50 px filter
                               # width (studio.setup_render).  Past 3 px the
                               # projection is wrong and every number below it
                               # is meaningless, so this aborts.
MARGIN_PX = 10                 # slack around the projected panel, used only to
                               # measure the ground endmember and to detect a
                               # crop that clips the ink
MIN_BLOB = 12                  # compare_script.ref_mask()'s own speckle filter


# ===========================================================================
# CONSTANTS READ FROM THE SOURCE OF TRUTH, NOT COPIED FROM IT
# ===========================================================================
# I could not `import build` / `import t1_core` / `import studio`: all three
# `import bpy` at module scope, and importing build.py would build the entire
# vehicle as a side effect.  So the constants are PARSED out of the source with
# ast instead of being copied into this file.  That is the whole point -- the
# copy is what failed: this file carried SCR z1 = 0.9154 for three revisions
# after build.py moved to 0.9896, and nothing could ever have noticed.  A
# renamed or deleted constant is now a hard error, not a silently wrong number.

def _lit(node):
    if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "dict":
        return {kw.arg: _lit(kw.value) for kw in node.keywords}
    return ast.literal_eval(node)


def _const(path, name):
    """Module-level constant out of a .py file, without importing it."""
    with open(path) as fh:
        tree = ast.parse(fh.read(), path)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return _lit(node.value)
    sys.exit("FAIL %s no longer defines %s -- this test reads it from there "
             "on purpose; fix the reader, do not re-copy the value" % (path, name))


def _view(path, want):
    """One entry of studio.views(), out of the source, without importing it."""
    with open(path) as fh:
        tree = ast.parse(fh.read(), path)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "views":
            for sub in ast.walk(node):
                if isinstance(sub, ast.Return) and isinstance(sub.value, ast.Dict):
                    for k, v in zip(sub.value.keys, sub.value.values):
                        if isinstance(k, ast.Constant) and k.value == want:
                            return _lit(v)
    sys.exit("FAIL %s: views()[%r] is gone" % (path, want))


SCR = _const(os.path.join(HERE, "build.py"), "SCR")
RAKE_Z0 = _const(os.path.join(HERE, "t1_core.py"), "RAKE_Z0")
RAKE_DZDX = _const(os.path.join(HERE, "t1_core.py"), "RAKE_DZDX")
VIEW = _view(os.path.join(HERE, "studio.py"), "side")


def rake_drop(x):
    """t1_core.rake_drop(): authored z minus this == rendered z."""
    return RAKE_Z0 + RAKE_DZDX * x


# ===========================================================================
# PROJECTION
# ===========================================================================

def projector(img_w, img_h):
    """Model (x, z) -> pixel, for the ortho side view.  Linear, so exact.

    studio.aim() sets sensor_fit='HORIZONTAL' unconditionally (studio.py:434),
    so ortho_scale spans the image WIDTH whatever the aspect ratio is.
    The camera sits on +Y looking at -Y with world +Z up, so its local +X --
    image right -- is world -X: model +X runs to image LEFT.
    """
    loc, tgt, ortho = VIEW["loc"], VIEW["tgt"], VIEW["ortho"]
    if not (ortho and abs(loc[0] - tgt[0]) < 1e-9 and abs(loc[2] - tgt[2]) < 1e-9
            and loc[1] > tgt[1]):
        sys.exit("FAIL studio.views()['side'] is no longer a level +Y ortho "
                 "view (%r); the projection below would be wrong" % (VIEW,))
    ppm = img_w / float(ortho)

    def f(x, z):
        return (img_w * 0.5 - (x - tgt[0]) * ppm,
                img_h * 0.5 - (z - tgt[2]) * ppm)
    return f, ppm


# ===========================================================================
# MASKS
# ===========================================================================
# The reference mask is NOT re-derived here.  compare_script.ref_mask() is the
# rule SPEC 10.20 established and measured: `T` is the redness of a 50 %-area
# optical mix of the ink and ground endmembers, mixed in linear light and
# re-encoded -- the locus where a pixel is half covered by paint -- with four
# separately measured tarnish zones, each with its own threshold, because
# tarnished ink is a different endmember.  The rev-9 rule `sat < 0.36` found
# untarnished silver only and dropped 14 % of the ink.
#
# The RENDER needs its own thresholds and cannot borrow the reference's: the
# photograph is open shade under an absorbing canopy over a ground at
# B = 6.0 +/- 3.6 DN, the render is a white softbox over a ground at B = 92,
# and SPEC 10.21's rule is explicit that a rendered ratio is not an albedo
# ratio.  So the render gets the SAME CONSTRUCTION with its OWN endmembers,
# measured from the render, and both the endmembers and the resulting
# threshold are printed.

def _srgb_to_linear(v):
    v = np.asarray(v, float) / 255.0
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def _linear_to_srgb(v):
    v = np.asarray(v, float)
    return 255.0 * np.where(v <= 0.0031308, v * 12.92,
                            1.055 * v ** (1 / 2.4) - 0.055)


def mix_threshold(ink, ground, cover=0.5):
    """Redness of a `cover`-area optical mix of the two endmembers.

    Same construction as compare_script's T_SILVER.  Note it is reproduced
    here to 0.0057 in redness rather than exactly (0.1352 against the recorded
    0.1409 for the reference's own endmembers): the recorded constant behaves
    like a pure gamma-2.0 encode, this uses the sRGB EOTF.  It is applied only
    to the RENDER, whose own threshold is derived the same way throughout, so
    the two sides are never mixed.  The render is also AgX-tonemapped, which
    is not the renderer's linear space -- the cost of that approximation is
    the 25 %/75 % coverage band printed with the result.
    """
    mix = _linear_to_srgb(cover * _srgb_to_linear(ink)
                          + (1.0 - cover) * _srgb_to_linear(ground))
    return float((mix[0] - 0.5 * (mix[1] + mix[2])) / mix.sum())


def endmembers(rgb, redness):
    """Ink and ground endmembers, from the valley of the redness histogram.

    The valley is used ONLY to decide which pixels are which population; the
    endmembers are the medians of each side, which sit far from the split, so
    the answer is insensitive to where exactly the valley is put.
    """
    h, e = np.histogram(redness, bins=180, range=(-0.05, 0.40))
    hs = nd.uniform_filter1d(h.astype(float), 5)
    ctr = 0.5 * (e[:-1] + e[1:])
    i1 = int(np.argmax(hs))
    i2 = int(np.argmax(np.where(np.abs(ctr - ctr[i1]) > 0.06, hs, -1.0)))
    lo, hi = sorted((i1, i2))
    v = lo + int(np.argmin(hs[lo:hi + 1]))
    split = float(ctr[v])
    ink = redness < split
    E_i = np.array([np.median(rgb[..., k][ink]) for k in range(3)])
    E_g = np.array([np.median(rgb[..., k][~ink]) for k in range(3)])
    return split, float(ctr[i1]), float(ctr[i2]), E_i, E_g, ink


def clean(mask):
    """compare_script.ref_mask()'s own morphology, applied to the render too."""
    m = nd.binary_closing(mask, np.ones((2, 2)))
    m = nd.binary_opening(m, nd.generate_binary_structure(2, 1))
    lab, n = nd.label(m)
    if n:
        sz = nd.sum(m, lab, range(1, n + 1))
        m = np.isin(lab, 1 + np.nonzero(sz >= MIN_BLOB)[0])
    return m


def bbox(mask):
    ys, xs = np.nonzero(mask)
    return xs.min(), ys.min(), xs.max(), ys.max()


def iou(a, b):
    u = (a | b).sum()
    return float((a & b).sum() / u) if u else 1.0


def best_shift(ref, gen, rad=SEARCH):
    """Integer-shift registration.  TRANSLATION ONLY -- no scaling, no
    rotation, so a size or aspect error cannot be absorbed by the fit."""
    best = (-1.0, 0, 0)
    for dy in range(-rad, rad + 1):
        for dx in range(-rad, rad + 1):
            v = iou(ref, np.roll(np.roll(gen, dy, 0), dx, 1))
            if v > best[0]:
                best = (v, dy, dx)
    return best


def box_resample(a, size):
    """Area-average resample of a float array to `size` = (w, h).

    PIL's BOX filter is an exact area average on a downscale, so a binary mask
    resamples to per-pixel COVERAGE, and thresholding that at 0.5 is the same
    half-covered-pixel convention the mask rules themselves use.
    """
    return np.asarray(Image.fromarray(a.astype(np.float32), mode="F")
                      .resize(size, Image.BOX), dtype=float)


# ===========================================================================

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "out/p_side.png"
    out = sys.argv[2] if len(sys.argv) > 2 else "out/flank_compare.png"
    if not os.path.exists(src):
        sys.exit("FAIL no render at %s.  Produce one with:\n"
                 "  T1_SUB=1 T1_PREVIEW=side T1_SAMP=32 T1_RX=1600 T1_RY=1100 "
                 "T1_FX=0 T1_PFX=p /tmp/blender/blender -b --python build.py"
                 % src)

    print("=" * 78)
    print("FLANK SCRIPT ACCEPTANCE TEST -- render against photograph")
    print("=" * 78)

    # ---------------------------------------------------------- provenance
    im = Image.open(src).convert("RGB")
    W, H = im.size
    A = np.asarray(im, dtype=float)
    print("render     %s  %dx%d  %s" % (
        src, W, H, time.strftime("%Y-%m-%d %H:%M:%S",
                                 time.localtime(os.path.getmtime(src)))))
    print("reference  ref_side.jpg  %s  scale %.1f +/- %.1f px/m (AUDIT_rev11)"
          % (Image.open("ref_side.jpg").size, REF_PPM, REF_PPM_SD))
    print("SCR        read from build.py  x0=%.4f x1=%.4f z0=%.4f z1=%.4f"
          % (SCR["x0"], SCR["x1"], SCR["z0"], SCR["z1"]))
    print("rake       read from t1_core.py  RAKE_Z0=%.6f  RAKE_DZDX=%.6f"
          % (RAKE_Z0, RAKE_DZDX))
    print("camera     read from studio.py views()['side']  ortho %.3f m  "
          "target z %.3f" % (VIEW["ortho"], VIEW["tgt"][2]))

    # ---------------------------------------------------------- projection
    proj, ppm = projector(W, H)
    print("scale      render %.4f px/m   reference %.4f px/m   "
          "ratio %.5f" % (ppm, REF_PPM, REF_PPM / ppm))
    print("           (the panel's own extents give the same: %.3f m of SCR "
          "spans %.1f px = %.4f px/m)"
          % (SCR["x0"] - SCR["x1"], (SCR["x0"] - SCR["x1"]) * ppm, ppm))

    # All FOUR corners, each with its own rake drop: step 8b is a SHEAR, so
    # the panel's two ends do not drop by the same amount and the rendered
    # panel is not a rectangle in the image.
    d0, d1 = rake_drop(SCR["x0"]), rake_drop(SCR["x1"])
    corners = {}
    for xk in ("x0", "x1"):
        for zk in ("z0", "z1"):
            corners[(xk, zk)] = proj(SCR[xk], SCR[zk] - rake_drop(SCR[xk]))
    cx = [c[0] for c in corners.values()]
    cy = [c[1] for c in corners.values()]
    print("rake drop  %.1f mm at x0=%+.3f   %.1f mm at x1=%+.3f   "
          "shear residual %.1f mm = %.2f px"
          % (d0 * 1000, SCR["x0"], d1 * 1000, SCR["x1"],
             abs(d0 - d1) * 1000, abs(d0 - d1) * ppm))
    print("panel      authored z %.4f-%.4f -> rendered z %.4f-%.4f "
          "(bbox over the shear)"
          % (SCR["z0"], SCR["z1"], SCR["z0"] - max(d0, d1), SCR["z1"] - min(d0, d1)))
    px0, px1 = int(np.floor(min(cx))), int(np.ceil(max(cx)))
    py0, py1 = int(np.floor(min(cy))), int(np.ceil(max(cy)))
    print("           projects to render px x %d-%d  y %d-%d  (%dx%d)"
          % (px0, px1, py0, py1, px1 - px0, py1 - py0))

    # Projection self-check that uses nothing from the decal: the wheels are
    # placed so that they land at z = 0 after step 8b skips them, so the
    # bottom of the tyre IS the ground plane.
    lum = A @ [0.2126, 0.7152, 0.0722]
    ground_meas = int(np.nonzero((lum < 100).any(1))[0].max())
    ground_pred = proj(0.0, 0.0)[1]
    print("projection self-check: z=0 predicted at row %.1f, lowest dark row "
          "%d  (delta %+.1f px = %+.1f mm)  %s"
          % (ground_pred, ground_meas, ground_meas - ground_pred,
             (ground_meas - ground_pred) / ppm * 1000,
             "ok" if abs(ground_meas - ground_pred) <= PROJ_TOL_PX else "OUT"))
    if abs(ground_meas - ground_pred) > PROJ_TOL_PX:
        sys.exit("FAIL the projection does not land on the render: the ground "
                 "plane is %.1f px out.  Nothing below this would mean "
                 "anything." % (ground_meas - ground_pred))

    # ------------------------------------------------- reference ink mask
    # FULL ink extent.  The old REF_INK dropped 4 rows off the top and SPEC
    # 10.20 established that the missing rows are the top of `Senor`.
    R = CS.ref_mask()
    rx0, ry0, rx1, ry1 = bbox(R)
    ref_rgb = np.asarray(Image.open("ref_side.jpg").convert("RGB"),
                         dtype=float)[CS.CY0:CS.CY0 + CS.CMH,
                                      CS.X0:CS.X0 + CS.MW]
    print("\nreference mask: compare_script.ref_mask(), SPEC 10.20 rule "
          "(imported, not re-derived)")
    print("           window %dx%d at ref_side.jpg (%d,%d); ink bbox "
          "(%d,%d)-(%d,%d) = %dx%d px"
          % (CS.MW, CS.CMH, CS.X0, CS.CY0, CS.X0 + rx0, CS.CY0 + ry0,
             CS.X0 + rx1, CS.CY0 + ry1, rx1 - rx0 + 1, ry1 - ry0 + 1))
    if ry0 == 0 or rx0 == 0 or ry1 == CS.CMH - 1 or rx1 == CS.MW - 1:
        print("           !! the ink touches the window edge -- the window is "
              "clipping the reference")
    # Said out loud because it is easy to read the bbox as an independent
    # measurement made here, and it is not: ref_mask() clips to LOCKUP, the
    # whole-lockup extent measured in SPEC 10.20 / AUDIT_rev11.
    lk = CS.LOCKUP
    binds = sum(int(a == b) for a, b in
                ((CS.X0 + rx0, lk[0]), (CS.CY0 + ry0, lk[1]),
                 (CS.X0 + rx1, lk[2]), (CS.CY0 + ry1, lk[3])))
    print("           the mask is clipped to compare_script.LOCKUP %s, the "
          "MEASURED lockup extent, and the ink reaches %d of its 4 edges -- so "
          "the bbox above is that measurement, not a re-derivation" % (lk, binds))

    # ---------------------------------------------------- render ink mask
    mx0, mx1 = px0 - MARGIN_PX, px1 + MARGIN_PX
    my0, my1 = py0 - MARGIN_PX, py1 + MARGIN_PX
    crop = A[my0:my1, mx0:mx1]
    r = CS._redness(crop)                       # the SAME chromaticity metric
    split, m1, m2, E_ink, E_gnd, _ = endmembers(crop, r)
    T50 = mix_threshold(E_ink, E_gnd, 0.50)
    T25 = mix_threshold(E_ink, E_gnd, 0.25)
    T75 = mix_threshold(E_ink, E_gnd, 0.75)
    print("\nrender mask: same construction, endmembers measured IN THE RENDER")
    print("           redness modes %.4f (ink) and %.4f (ground), valley %.4f"
          % (min(m1, m2), max(m1, m2), split))
    print("           endmembers  ink (%.0f,%.0f,%.0f)  ground (%.0f,%.0f,%.0f)"
          % (tuple(E_ink) + tuple(E_gnd)))
    print("           T(50%% cover) %.4f   band T(25%%) %.4f  T(75%%) %.4f"
          % (T50, T25, T75))

    # Confine to the rendered panel QUAD, not its bbox: the decal cannot be
    # outside the panel, and the panel is sheared, so each column has its own
    # top and bottom row.  Anything the rule calls ink outside the quad is a
    # misclassification and is reported rather than quietly kept.
    cols = np.arange(crop.shape[1]) + mx0 + 0.5
    xs_m = VIEW["tgt"][0] - (cols - W * 0.5) / ppm
    top = np.array([proj(x, SCR["z1"] - rake_drop(x))[1] for x in xs_m])
    bot = np.array([proj(x, SCR["z0"] - rake_drop(x))[1] for x in xs_m])
    rows = (np.arange(crop.shape[0]) + my0 + 0.5)[:, None]
    in_panel = ((rows >= top[None, :]) & (rows <= bot[None, :])
                & (xs_m <= SCR["x0"])[None, :] & (xs_m >= SCR["x1"])[None, :])

    raw = r < T50
    outside = int((raw & ~in_panel).sum())
    G_native = clean(raw & in_panel)
    print("           ink px in the render at T(50%%): %d inside the panel, "
          "%d outside it (rejected)" % (int((raw & in_panel).sum()), outside))
    sens = [100.0 * ((r < T) & in_panel).sum() / (raw & in_panel).sum() - 100
            for T in (T25, T75)]
    print("           threshold sensitivity: %d px at T(25%%), %d at T(75%%) "
          "= %+.1f%% / %+.1f%% on the area"
          % (int(((r < T25) & in_panel).sum()),
             int(((r < T75) & in_panel).sum()), sens[0], sens[1]))
    gx0, gy0, gx1, gy1 = bbox(G_native)
    touch = (gx0 <= MARGIN_PX - 1 or gy0 <= MARGIN_PX - 1
             or gx1 >= crop.shape[1] - MARGIN_PX or gy1 >= crop.shape[0] - MARGIN_PX)
    print("           ink bbox %dx%d px inside a %dx%d panel; ink reaches the "
          "panel edge: %s" % (gx1 - gx0 + 1, gy1 - gy0 + 1, px1 - px0, py1 - py0,
                              "yes" if touch else "no"))
    # How much of the panel the ink actually uses.  tex/senor.png's alpha runs
    # to within 13 of its 1738 rows and to within 12 of its 4096 columns, so a
    # gap here is the LOCKUP not reaching the panel, not padding in the file.
    print("           ink sits %+.0f mm below the panel top and %+.0f mm above "
          "the panel bottom (panel is %.0f mm tall)"
          % ((gy0 + my0 - top.min()) / ppm * 1000,
             (bot.max() - (gy1 + my0)) / ppm * 1000,
             (SCR["z1"] - SCR["z0"]) * 1000))

    # =================================================== THE MEASUREMENTS
    print("\n" + "-" * 78)
    print("MEASUREMENTS   (mm from each frame's own scale; the render's is "
          "exact from")
    print("                the ortho camera, the reference's is %.1f +/- %.1f "
          "px/m)" % (REF_PPM, REF_PPM_SD))
    print("-" * 78)

    ref_px = int(R.sum())
    gen_px = int(G_native.sum())
    ref_mm2 = ref_px / REF_PPM ** 2 * 1e6
    gen_mm2 = gen_px / ppm ** 2 * 1e6
    ref_mm2_sd = 2.0 * REF_PPM_SD / REF_PPM * ref_mm2      # area ~ 1/ppm^2
    ratio = gen_mm2 / ref_mm2
    ratio_sd = ratio * 2.0 * REF_PPM_SD / REF_PPM
    print("ink area        reference %6d px = %8.0f +/- %.0f mm^2" %
          (ref_px, ref_mm2, ref_mm2_sd))
    print("                render    %6d px = %8.0f mm^2" % (gen_px, gen_mm2))
    print("                ratio render/reference  %.4f +/- %.4f   (%+.1f %%)"
          % (ratio, ratio_sd, 100 * (ratio - 1)))
    print("                read against the render mask's own coverage band, "
          "%+.1f %% / %+.1f %%" % (sens[0], sens[1]))

    rw_mm = (rx1 - rx0 + 1) / REF_PPM * 1000
    rh_mm = (ry1 - ry0 + 1) / REF_PPM * 1000
    gw_mm = (gx1 - gx0 + 1) / ppm * 1000
    gh_mm = (gy1 - gy0 + 1) / ppm * 1000
    ra, ga = (rx1 - rx0 + 1) / (ry1 - ry0 + 1), (gx1 - gx0 + 1) / (gy1 - gy0 + 1)
    print("ink bbox        reference %7.1f x %6.1f mm   aspect %.4f"
          % (rw_mm, rh_mm, ra))
    print("                render    %7.1f x %6.1f mm   aspect %.4f"
          % (gw_mm, gh_mm, ga))
    print("                width  %+.1f mm (%+.1f %%)   height %+.1f mm (%+.1f %%)"
          % (gw_mm - rw_mm, 100 * (gw_mm / rw_mm - 1),
             gh_mm - rh_mm, 100 * (gh_mm / rh_mm - 1)))
    print("                ASPECT DIFFERENCE %+.4f = %+.2f %%   "
          "(dimensionless: no px/m enters it)"
          % (ga - ra, 100 * (ga / ra - 1)))

    # ------------------------------------------------------- common frame
    # Both masks are put in ONE frame with ONE mm-per-pixel, so a size or an
    # aspect error shows up as a mismatch instead of being normalised away.
    # The common scale is the REFERENCE's, so the reference is not resampled
    # at all and the render is area-averaged DOWN to it -- no detail is
    # invented, and the ceiling below is measured at exactly this scale.
    tw = int(round(G_native.shape[1] * REF_PPM / ppm))
    th = int(round(G_native.shape[0] * REF_PPM / ppm))
    Gc = box_resample(G_native.astype(float), (tw, th)) >= 0.5
    Gc = clean(Gc)
    crop_c = np.dstack([box_resample(crop[..., k], (tw, th)) for k in range(3)])
    print("\ncommon frame    %.4f mm/px for both  (reference native, render "
          "%dx%d -> %dx%d)" % (1000.0 / REF_PPM, G_native.shape[1],
                               G_native.shape[0], tw, th))

    # place both on one canvas, ink-bbox centres coincident, then search
    gx0c, gy0c, gx1c, gy1c = bbox(Gc)
    ch = max(R.shape[0], th) + 4 * SEARCH
    cw = max(R.shape[1], tw) + 4 * SEARCH
    Rc = np.zeros((ch, cw), bool)
    Gk = np.zeros((ch, cw), bool)
    Ck = np.zeros((ch, cw, 3), float)
    Rk = np.zeros((ch, cw, 3), float)
    ay = 2 * SEARCH
    ax = 2 * SEARCH
    Rc[ay:ay + R.shape[0], ax:ax + R.shape[1]] = R
    Rk[ay:ay + R.shape[0], ax:ax + R.shape[1]] = ref_rgb
    # offset that makes the two ink-bbox centres coincide
    oy = int(round((ry0 + ry1) / 2 - (gy0c + gy1c) / 2))
    ox = int(round((rx0 + rx1) / 2 - (gx0c + gx1c) / 2))
    Gk[ay + oy:ay + oy + th, ax + ox:ax + ox + tw] = Gc
    Ck[ay + oy:ay + oy + th, ax + ox:ax + ox + tw] = crop_c

    v0 = iou(Rc, Gk)
    v, dy, dx = best_shift(Rc, Gk)
    Gs = np.roll(np.roll(Gk, dy, 0), dx, 1)
    Cs = np.roll(np.roll(Ck, dy, 0), dx, 1)
    print("registration    bbox-centre align gives IoU %.4f; best integer "
          "shift (%+d, %+d) px = (%+.1f, %+.1f) mm" %
          (v0, dx, dy, dx * 1000 / REF_PPM, dy * 1000 / REF_PPM))
    if abs(dx) == SEARCH or abs(dy) == SEARCH:
        print("                !! the optimum is ON the search boundary "
              "(+/-%d px) -- widen SEARCH" % SEARCH)

    # ----------------------------------------------------------- ceiling
    # Measured, not asserted: what one pixel of registration slop costs the
    # reference mask against ITSELF.  Nothing can score above this.
    slop = [iou(Rc, np.roll(np.roll(Rc, sy, 0), sx, 1))
            for sy, sx in ((0, 1), (0, -1), (1, 0), (-1, 0))]
    ceiling = float(np.mean(slop))
    print("ceiling         reference against itself at 1 px: "
          "%.4f %.4f %.4f %.4f -> mean %.4f  (MEASURED this run)"
          % tuple(slop + [ceiling]))
    print("                inherited, AUDIT_rev11: %.2f, or %.2f with 1 px of "
          "registration slop" % (CEILING_INHERITED, CEILING_INHERITED_1PX))
    print("IoU             %.4f  =  %.3f of the measured ceiling  "
          "(%.3f of the inherited %.2f)"
          % (v, v / ceiling, v / CEILING_INHERITED_1PX, CEILING_INHERITED_1PX))

    # --------------------------------------------------------- per region
    # A whole-lockup IoU is dominated by the largest glyph -- which is exactly
    # how this comparison went blind before (AUDIT_rev11: whole-lockup 0.942
    # while `Senor` was at 0.454).  The regions are compare_script.BOXES, the
    # established set, and each one gets its OWN measured ceiling because a
    # small region loses more of itself to 1 px of slop than a large one.
    print("\n  %-14s %6s %8s %8s %8s %8s" %
          ("region", "IoU", "ceiling", "of ceil", "ref px", "render px"))
    print("  " + "-" * 56)
    worst = (1e9, "")
    for name, bx0, by0, bx1, by1 in CS.BOXES:
        sl = (slice(ay + by0 + CS.YPAD, ay + by1 + CS.YPAD),
              slice(ax + bx0, ax + bx1))
        a, b = Rc[sl], Gs[sl]
        if a.sum() == 0:
            continue
        cl = float(np.mean([iou(a, np.roll(np.roll(Rc, sy, 0), sx, 1)[sl])
                            for sy, sx in ((0, 1), (0, -1), (1, 0), (-1, 0))]))
        f = iou(a, b) / cl
        print("  %-14s %6.3f %8.3f %8.3f %8d %8d"
              % (name, iou(a, b), cl, f, a.sum(), b.sum()))
        if f < worst[0]:
            worst = (f, name)
    print("  " + "-" * 56)
    print("  worst region: %s at %.3f of its own ceiling" % (worst[1], worst[0]))

    # --------------------------------------------- what the misses are made of
    # A false negative can mean two different things and they are not the same
    # defect: nothing is there, or something is there and it does not read as
    # ink.  This says which, in the render's own pixels.
    fn = Rc & ~Gs
    fp = Gs & ~Rc
    both = Rc & Gs
    inpanel_c = Cs.sum(2) > 0
    gnd_c = inpanel_c & ~Rc & ~Gs
    def _stat(m):
        if m.sum() < 10:
            return "n<10"
        px = Cs[m]
        rn = (px[:, 0] - 0.5 * (px[:, 1] + px[:, 2])) / np.maximum(px.sum(1), 1e-6)
        return ("(%5.1f,%5.1f,%5.1f) redness %.4f  n=%d"
                % (px[:, 0].mean(), px[:, 1].mean(), px[:, 2].mean(),
                   rn.mean(), m.sum()))
    print("\nwhat the render has where the two masks disagree "
          "(render pixels, common frame):")
    print("   both agree ink   %s" % _stat(both))
    print("   ref only (miss)  %s" % _stat(fn & inpanel_c))
    print("   render only      %s" % _stat(fp))
    print("   bare ground      %s" % _stat(gnd_c))
    # ... and the same three inside the region that failed hardest, because a
    # miss means two different things -- nothing is there, or something is
    # there and it does not read as ink -- and they are not the same defect.
    for name, bx0, by0, bx1, by1 in CS.BOXES:
        if name != worst[1]:
            continue
        wm = np.zeros_like(Rc)
        wm[ay + by0 + CS.YPAD:ay + by1 + CS.YPAD, ax + bx0:ax + bx1] = True
        print("   in `%s`:  missed %s" % (name, _stat(fn & wm & inpanel_c)))
        print("   %s   ground %s" % (" " * len(name), _stat(gnd_c & wm)))

    # ------------------------------------------------------- ink colour
    # The reference silver is NOT flat, and the four measured tarnish zones are
    # a different endmember, so the whole-mask spread and the untarnished
    # spread are both quoted -- the published "per-channel sd 16-19, luma
    # p5-p95 85-135" (SPEC 10.21) is the UNTARNISHED figure and would not be
    # comparable with a whole-mask number.
    untar = R.copy()
    for tx0, ty0, tx1, ty1, _ in CS.TARNISH:
        untar[max(0, ty0 - CS.CY0):max(0, ty1 - CS.CY0),
              max(0, tx0 - CS.X0):max(0, tx1 - CS.X0)] = False
    print("\nink pixel colour (native resolution, each in its own image):")
    for lab_, px_ in (("reference all ink", ref_rgb[R]),
                      ("reference untarnished", ref_rgb[untar]),
                      ("render all ink", crop[G_native])):
        lm = px_ @ [0.2126, 0.7152, 0.0722]
        print("   %-22s mean (%5.1f,%5.1f,%5.1f)  sd (%4.1f,%4.1f,%4.1f)  "
              "luma p5-p95 %3.0f-%3.0f  n=%d"
              % (lab_, px_[:, 0].mean(), px_[:, 1].mean(), px_[:, 2].mean(),
                 px_[:, 0].std(), px_[:, 1].std(), px_[:, 2].std(),
                 np.percentile(lm, 5), np.percentile(lm, 95), len(px_)))

    # ============================================================= verdict
    print("\n" + "=" * 78)
    ok_area = abs(ratio - 1) <= AREA_TOL
    ok_asp = abs(ga / ra - 1) <= ASPECT_TOL
    iou_min = IOU_FRAC_OF_CEILING * ceiling
    ok_iou = v >= iou_min
    ok_reg = worst[0] >= REGION_IOU_FRAC
    for name, ok, got, want in (
            ("ink area ratio", ok_area, "%.4f" % ratio,
             "1.000 +/- %.2f  (SPEC 10.20: the reference footprint itself is "
             "+/- 3.3 %%)" % AREA_TOL),
            ("ink aspect", ok_asp, "%.4f vs %.4f" % (ga, ra),
             "within %.0f %% (3 sigma of the reference's own isotropy)"
             % (100 * ASPECT_TOL)),
            ("IoU vs ceiling", ok_iou, "%.4f" % v,
             ">= %.4f = %.2f x the %.4f ceiling measured this run"
             % (iou_min, IOU_FRAC_OF_CEILING, ceiling)),
            ("worst region", ok_reg, "%.3f (%s)" % (worst[0], worst[1]),
             ">= %.2f of that region's own measured ceiling"
             % REGION_IOU_FRAC)):
        print("  %-4s %-16s %-22s  target %s"
              % ("PASS" if ok else "FAIL", name, got, want))
    verdict = ok_area and ok_asp and ok_iou and ok_reg
    print("\n%s  -- flank script, render against ref_side.jpg"
          % ("PASS" if verdict else "FAIL"))
    print("=" * 78)

    # ================================================== the picture, honestly
    # Both panels at ONE mm/px, one canvas, registered by the shift printed
    # above.  Neither is stretched to the other's box.
    S = 3
    y0k, y1k = ay - SEARCH, ay + max(R.shape[0], th) + SEARCH
    x0k, x1k = ax - SEARCH, ax + max(R.shape[1], tw) + SEARCH

    def band(rgbimg):
        a = rgbimg[y0k:y1k, x0k:x1k]
        return np.kron(np.clip(a, 0, 255).astype(np.uint8),
                       np.ones((S, S, 1), np.uint8))

    ov = np.zeros((y1k - y0k, x1k - x0k, 3), np.uint8)
    ov[..., 0] = Rc[y0k:y1k, x0k:x1k] * 255
    ov[..., 1] = Gs[y0k:y1k, x0k:x1k] * 255
    ov[..., 2] = (Rc & Gs)[y0k:y1k, x0k:x1k] * 255
    ov = np.kron(ov, np.ones((S, S, 1), np.uint8))

    panels = [("REFERENCE  ref_side.jpg, full measured ink extent, "
               "%.3f mm/px" % (1000 / REF_PPM), band(Rk)),
              ("RENDER  %s, panel projected with the rake, area-averaged to "
               "the same mm/px" % os.path.basename(src), band(Cs)),
              ("OVERLAY  red = reference only, green = render only, "
               "white = both.  IoU %.4f / ceiling %.4f" % (v, ceiling), ov)]
    lab = 20
    Wc = panels[0][1].shape[1]
    Hc = sum(p[1].shape[0] + lab for p in panels) + 8
    canvas = Image.new("RGB", (Wc, Hc), (26, 26, 28))
    d = ImageDraw.Draw(canvas)
    y = 0
    for text, arr in panels:
        d.text((6, y + 5), text, fill=(235, 235, 235))
        canvas.paste(Image.fromarray(arr), (0, y + lab))
        y += lab + arr.shape[0]
    canvas.save(out)
    print("wrote %s" % out)
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
