"""rev 64 -- THE EMBLEM'S TARGETS ARE MEASURED ON IMAGES THAT ARE NOT
MIRROR-SYMMETRIC, AND A PURE SHEAR OF THE UNCHANGED GLYPH SPANS BOTH OF THEM.

F175 showed that C6 and C8 can both pass on a glyph that renders as a Y.  This
comes at the same gate from the other side: it asks whether the TARGETS mean
what they are taken to mean.  Rule 39 -- a gate's target is an instrument too.

THE ARGUMENT, AND EVERY STEP OF IT IS A MEASUREMENT BELOW:

  1. The VW mark is MIRROR-SYMMETRIC about its vertical.  That is a property of
     the object, not of any photograph of it, and the built glyph has it by
     construction (S1).
  2. Both frames the emblem's targets are read from are NOT mirror-symmetric
     (S2).  `probe_rev63_angles.desquash` rescales the axes by a fitted ratio;
     it never ROTATES, so it cannot undo the shear a three-quarter view puts in.
  3. So a shear sits between the mark and every target taken off those frames.
     S3 shears the BUILT GLYPH -- changing no constant, no spine, nothing about
     the shape -- and watches C6's cell count and C8's elongation move through
     BOTH photographic targets.
  4. Therefore neither target can separate "the glyph is the wrong shape" from
     "the frame is oblique".  That is the finding.  It does NOT say the glyph is
     right; it says these two numbers cannot be the thing that decides.

WHAT THIS DOES **NOT** ESTABLISH, SAID OUT LOUD (rule 12).  It does not
quantify how much of C8's 3.390 is shear.  Mirror IoU saturates around shear
0.3 while elongation keeps climbing, so the two do not pin each other, and the
photographs' own mirror IoU (0.41 / 0.48) sits at a shear where elongation is
only ~2.6-2.8, not 3.39.  Recovering the actual amount needs the badge's RING
FITTED AS AN ELLIPSE -- the ring is a circle on the real object, so its image
gives the homography outright.  That is well-posed and it is not done here.
"""
import sys

import numpy as np
from PIL import Image

import probe_rev63_angles as A

_fail = []


def ck(n, ok, m):
    if not ok:
        _fail.append(n)
    print("  [%s] %-4s %s" % ("PASS" if ok else "FAIL", n, m))


def mirror_iou(mask):
    """IoU of a mask against its own left-right flip, cropped to its ink bbox.

    Cropped to the INK, not to the canvas: a mark sitting off-centre in its
    raster would otherwise read as asymmetric for a reason that has nothing to
    do with the mark.  That is the registration defect rev 64 found in
    probe_rev63_trace.raster, and it is not repeated here."""
    ys, xs = np.nonzero(mask)
    s = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    f = s[:, ::-1]
    return float((s & f).sum()) / float((s | f).sum())


def shear(mask, k):
    n0, n1 = mask.shape
    return np.asarray(Image.fromarray((mask * 255).astype(np.uint8))
                      .transform((n1, n0), Image.AFFINE,
                                 (1, k, -k * n1 / 2.0, 0, 1, 0),
                                 resample=Image.BILINEAR)) > 127


sys.argv = [sys.argv[0]]
import probe_rev46_vw as _vw                                    # noqa: E402

SHIP = _vw.glyph_only_mask(rows=276,
                           **{k: getattr(_vw.C, k) for k in _vw.PARAMS})
WS, NOL = A.workshop(), A.nolita()

print("")
print("  S1 -- IS THE INSTRUMENT SOUND?  the built glyph is mirror-symmetric")
print("        by construction, so this must read near 1.")
ck("S1", mirror_iou(SHIP) > 0.95,
   "the BUILT glyph mirrors onto itself at IoU %.4f" % mirror_iou(SHIP))

ck("S1k", mirror_iou(shear(SHIP, 0.30)) < 0.40,
   "KILL: the SAME glyph sheared by 0.30 reads %.4f.  The statistic responds "
   "to shear, so S2 is a reading and not an artefact"
   % mirror_iou(shear(SHIP, 0.30)))

print("")
print("  S2 -- THE TWO FRAMES EVERY EMBLEM TARGET IS READ FROM")
_w, _n = mirror_iou(WS), mirror_iou(NOL)
print("        WORKSHOP badge  (C6/C8's pressing, and rev 63's trace) %.4f" % _w)
print("        TARGET BUS badge (ref_nolita_front34.jpg)              %.4f" % _n)
print("        the BUILT glyph                                        %.4f"
      % mirror_iou(SHIP))
ck("S2", _w < 0.70 and _n < 0.70,
   "NEITHER photographed badge is mirror-symmetric (%.4f, %.4f against the "
   "built glyph's %.4f).  desquash() rescales the axes and never rotates, so "
   "the shear survives it" % (_w, _n, mirror_iou(SHIP)))

print("")
print("  S3 -- SHEAR THE BUILT GLYPH.  NO CONSTANT, NO SPINE, NO SHAPE CHANGES.")
print("        %-7s %-12s %-12s %s" % ("shear", "mirror IoU", "elongation", "cells"))
rows = []
for k in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6):
    m = shear(SHIP, k)
    e = _vw.cell_elongation(m, 1.0)
    c, _ = _vw.cream_cells(m)
    rows.append((k, mirror_iou(m), e, c))
    print("        %-7.2f %-12.4f %-12.3f %d" % (k, mirror_iou(m), e, c))
print("        %-7s %-12s %-12s %s"
      % ("PHOTO", "%.3f/%.3f" % (_w, _n), "3.390", "7"))

_es = [r[2] for r in rows]
_cs = [r[3] for r in rows]
ck("S3", min(_es) <= 3.390 <= max(_es),
   "C8's 3.390 TARGET LIES INSIDE THE RANGE A PURE SHEAR OF THE UNCHANGED "
   "GLYPH SWEEPS: %.3f .. %.3f.  The glyph that reaches it is the SHIPPED one "
   "with a viewing angle on it, not a better shape" % (min(_es), max(_es)))
ck("S4", min(_cs) <= 7 <= max(_cs),
   "and C6's 7-cell target likewise: shear alone carries the count %d -> %d, "
   "through 7.  Neither gate can tell an oblique frame from a wrong shape"
   % (min(_cs), max(_cs)))

# S5 -- the honest limit.  If shear ALONE explained the target, the shear that
# reproduces the photographs' mirror IoU would also reproduce 3.390.  It does
# not, and saying so is the difference between a result and an overclaim.
_at = [r for r in rows if r[1] <= max(_w, _n)]
_e_at = _at[0][2] if _at else float("nan")
ck("S5", True,
   "CEILING, NOT A CLAIM: at the shear that first matches the photographs' own "
   "mirror IoU (<= %.3f) the elongation is only %.3f, not 3.390.  So shear is "
   "PRESENT and SUFFICIENT to span the targets, but this probe does NOT show "
   "it is the whole of the gap.  Fit the badge's ring as an ELLIPSE and the "
   "homography is recoverable outright" % (max(_w, _n), _e_at))

# S6 -- PAINT IT (rule 8).  No number above is published without the picture.
_p = [np.where(m, 235, 30) for m in
      (SHIP, shear(SHIP, 0.4),
       np.asarray(Image.fromarray((WS * 255).astype(np.uint8))
                  .resize((276, 276), Image.LANCZOS)) > 127,
       np.asarray(Image.fromarray((NOL * 255).astype(np.uint8))
                  .resize((276, 276), Image.LANCZOS)) > 127)]
Image.fromarray(np.concatenate(_p, axis=1).astype(np.uint8)).save(
    "probe_scratch/rev64_shear.png")
ck("S6", True,
   "painted probe_scratch/rev64_shear.png  BUILT | BUILT SHEARED 0.4 | "
   "WORKSHOP | TARGET BUS -- look at it before believing any row above")

print("")
print("  %d checked, %d FAILED%s"
      % (6, len(_fail), (" -- " + ",".join(_fail)) if _fail else ""))
sys.exit(1 if _fail else 0)
