"""probe_updust_pointer.py -- rev 29.  READ-ONLY.  Validates the pointer for
the rev-29 owner question BEFORE it is sent, and prints its crop box.

WHY THIS FILE EXISTS
--------------------
`probe_dust_scope.py` established BY EXECUTION that `W_DUST_FAC_UP` is a GLOBAL
up-face lever reaching ELEVEN materials, not the counter-top constant that
`t1_mats.py:366`/`:467` and SPEC 10.81 describe.  The owner's rev-28 reading --
"the counter top is CLEAN VARNISHED PLYWOOD" -- is therefore LOCAL to one of the
surfaces the lever films.  Whether the contradiction is local or global is a
PHOTOGRAPH question, not a vehicle question.

The largest filmed surface in the build is `T1_body` under `T1_paint`:
**12.3697 m^2 of up-facing area at mean coverage 0.3916** -- the ROOF.
`ref_rear34.jpg` is the only supplied frame with elevation on it (`ref_side.jpg`
puts the camera at roof height, so the roof plane is edge-on -- rev 12's method
note).  So the roof crown in `ref_rear34.jpg` is the surface to ask about.

THE RULE BEING OBEYED
---------------------
rev 28: **A QUESTION THAT CANNOT BE ANSWERED UNAMBIGUOUSLY IS THE ASKER'S
DEFECT.**  rev 20's boxes A/B straddled; rev 21's redrawn N1 still did; rev 22
found SPEC's OWN founding crop straddling; rev 27 proved `W_DUST_FAC_UP`'s
founding patch NECESSARILY straddled.  So the pointer is validated first.

THE INDICATOR, AND TWO CORRECTIONS TO MY OWN FIRST CUT
------------------------------------------------------
A curved painted panel under one dominant source carries a smooth ILLUMINATION
GRADIENT.  Raw spread cannot tell that from a material step.  Fitting and
removing a low-order surface absorbs a gradient and does NOT absorb a step.

**CORRECTION 1 -- MY FIRST CUT FITTED A PLANE, AND THE ROOF IS A CROWN.**
A crown's shading is curved, so a PLANE leaves curvature in the residual and
charges it to "straddle".  The fit is now QUADRATIC, and the positive control
is re-run under the quadratic too: a known straddler must still read large
(it does -- 55.1 % planar, 53.2 % quadratic).  **The model of "gradient" was
changed; the acceptance band was NOT widened to let the box through.**

**CORRECTION 2 -- MY FIRST THRESHOLD WOULD HAVE REJECTED REV 28'S OWN
ACCEPTED POINTER.**  I set 6.0 % by eye.  Recomputed with THIS file's
statistic, rev 28's validated counter-top pointer `(640,680,420,435)` reads
**7.4 %** -- it would have FAILED.  rev 28 published 0.0 % / 0.6 % for those
boxes, which is a DIFFERENT spread statistic; comparing across the two is the
carried-forward-figure trap (rev 23).  **A number computed one way is not a
number computed another way, and a threshold calibrated against the wrong one
is a threshold calibrated against nothing.**

So the band is no longer chosen.  It is DERIVED, per box, from two controls
printed on every run:
  * FLOOR -- a synthetic quadratic ramp of the SAME BOX SHAPE carrying noise at
    the box's own measured high-frequency sigma.  This is what a perfectly
    clean single material of that size reads on this JPEG.
  * CEILING -- SPEC 10.76's founding patch, PROVEN box-independently in rev 27
    to straddle tan / cream / brass nosing / a tin can.
**CORRECTION 3 -- MY SECOND THRESHOLD WAS ALSO WRONG, AND THE ANCHOR CAUGHT
IT.**  "Residual < 2 x its own floor" REJECTED rev 28's accepted pointer at
3.08 x.  A box the owner demonstrably answered cannot be ruled unanswerable by
a later instrument.  Third self-correction on this one probe, recorded rather
than smoothed.

The band now has **NO FREE PARAMETER**.  Both calibration points are measured
in the same run with the same statistic, and one of them is a box the owner
HAS ALREADY SUCCESSFULLY ANSWERED.  A box is accepted when its ratio-to-floor
is **closer, in log distance, to the ANSWERED ANCHOR than to the KNOWN
STRADDLER**.  Both distances are printed, so the verdict is auditable rather
than trusted.

CONTROLS -- asserted
--------------------
P1  the KNOWN STRADDLER must read LARGE under the quadratic fit.  If a proven
    straddle is absorbed, the indicator is dead.
N1  a SYNTHETIC pure quadratic gradient must read at the floor.  If a pure
    gradient reads as a straddle, the indicator is a curvature detector.
N2  the indicator's DYNAMIC RANGE (ceiling / floor) must exceed 5x, or it
    cannot discriminate at all.
A1  the ROOF pointer must be closer in log-ratio to the ANSWERED ANCHOR than
    to the KNOWN STRADDLER.
A2  the ROOF pointer must contain NO CLIPPED pixel.  Every cream in
    `ref_rear34.jpg` clips at 249-254 somewhere, and clipping destroys the
    very texture the question is about.
A3  the two calibration anchors must be separated by more than 3x, or they
    cannot calibrate anything.  (rev 28's accepted pointer reads 3.08 x its
    floor; the proven straddler reads 14.14 x -- a 4.6x separation.)

NOTHING IS MEASURED FROM THESE BOXES.  They are POINTERS -- they say "this
surface", not "these pixels".  Stated, because rev 20 and rev 21 took numbers
from boxes that straddled and both readings were fatal.
"""
import os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
FRAME = os.path.join(ROOT, "ref_rear34.jpg")
IM = np.asarray(Image.open(FRAME).convert("RGB"), dtype=float)
H, W, _ = IM.shape
P = print
FAIL = []
SEED = 196301                       # the project's own bake seed, not a fresh one


def check(ok, label, detail=""):
    P("  [%s] %s%s" % ("PASS" if ok else "FAIL", label,
                       ("  -- " + detail) if detail else ""))
    if not ok:
        FAIL.append(label)


def luma(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def _resid(l):
    """Quadratic fit in normalised box coordinates; return residual spread as
    a percentage of the box mean, using a robust 5-95 percentile range."""
    h, w = l.shape
    yy, xx = np.mgrid[0:h, 0:w]
    x = xx.ravel() / max(1, w - 1)
    y = yy.ravel() / max(1, h - 1)
    A = np.column_stack([np.ones_like(x), x, y, x * x, x * y, y * y])
    c, *_ = np.linalg.lstsq(A, l.ravel(), rcond=None)
    r = l.ravel() - A @ c
    lo, hi = np.percentile(r, [5, 95])
    return 100.0 * (hi - lo) / l.mean()


def hf_sigma(l):
    """High-frequency noise sigma from horizontal first differences.  A single
    material step contributes to only ONE column of differences, so this is a
    noise estimate a step barely moves -- which is what makes it usable as the
    floor's input on a box that might straddle."""
    d = np.diff(l, axis=1)
    return 1.4826 * np.median(np.abs(d - np.median(d))) / np.sqrt(2.0)


def floor_for(l):
    """What a PERFECTLY CLEAN single material of this box's shape and this
    box's own noise reads on this frame.  Synthetic, quadratic, seeded."""
    h, w = l.shape
    yy, xx = np.mgrid[0:h, 0:w]
    x, y = xx / max(1, w - 1), yy / max(1, h - 1)
    rng = np.random.default_rng(SEED)
    span = np.percentile(l, 95) - np.percentile(l, 5)
    ramp = l.mean() + span * (0.6 * x - 0.35 * x * x + 0.25 * y)
    return _resid(ramp + rng.normal(0.0, max(hf_sigma(l), 0.3), (h, w)))


def report(box, name):
    u0, u1, v0, v1 = box
    sub = IM[v0:v1, u0:u1]
    l = luma(sub)
    res, flr = _resid(l), floor_for(l)
    clip = 100.0 * (sub.max(axis=2) >= 254).mean()
    med = tuple(np.median(sub.reshape(-1, 3), axis=0).round(0).astype(int))
    P("  %s" % name)
    P("    CROP BOX  u %d-%d  v %d-%d   (%d x %d px, n=%d)"
      % (u0, u1, v0, v1, u1 - u0, v1 - v0, l.size))
    P("    median sRGB %s   hf sigma %.2f   clipped %.2f %%"
      % (med, hf_sigma(l), clip))
    P("    quadratic residual %5.1f %%   own floor %5.1f %%   ratio %.2f x"
      % (res, flr, res / flr if flr else float("inf")))
    return res, flr, clip


STRADDLER = (556, 656, 397, 424)          # SPEC 10.76 founding patch, PROVEN
REV28_ANCHOR = (640, 680, 420, 435)       # rev 28's own accepted Q1 pointer
ROOF = (860, 930, 234, 246)               # rev 29, this file

P("\n" + "=" * 74)
P("probe_updust_pointer.py -- validating rev 29's pointer before sending")
P("=" * 74)
P("frame %s  %d x %d ; quadratic straddle indicator, seeded %d"
  % (os.path.basename(FRAME), W, H, SEED))

P("\n--- P1  POSITIVE CEILING: a PROVEN straddler ---")
c_res, c_flr, _ = report(STRADDLER, "SPEC 10.76 founding patch for _UP_MEASURED")
check(c_res > 8.0 * c_flr, "P1 the known straddler is NOT absorbed",
      "%.1f %% at %.1f x its own floor -- a material step survives a "
      "quadratic" % (c_res, c_res / c_flr))

P("\n--- N1  NEGATIVE FLOOR: a synthetic pure gradient at the roof's shape ---")
_rl = luma(IM[ROOF[2]:ROOF[3], ROOF[0]:ROOF[1]])
_f = floor_for(_rl)
P("  synthetic quadratic ramp, roof box shape, sigma %.2f : %.1f %%"
  % (hf_sigma(_rl), _f))
check(_f < 0.25 * c_res, "N1 a pure gradient reads far below the straddler",
      "%.1f %% against %.1f %%" % (_f, c_res))

P("\n--- N2  DYNAMIC RANGE ---")
P("  ceiling / floor = %.1f / %.1f = %.1f x" % (c_res, _f, c_res / _f))
check(c_res / _f > 5.0, "N2 the indicator discriminates",
      "%.1f x between a proven straddle and a proven clean surface"
      % (c_res / _f))

P("\n--- A3  rev 28's OWN accepted pointer, re-measured with THIS statistic ---")
a_res, a_flr, a_clip = report(REV28_ANCHOR,
                              "rev 28 Q1 'P1' counter top, mid-run [ANSWERED]")
_anchor_r, _strad_r = a_res / a_flr, c_res / c_flr
check(_strad_r / _anchor_r > 3.0,
      "A3 the two calibration anchors are separated",
      "answered anchor %.2f x vs proven straddler %.2f x = %.1f x apart"
      % (_anchor_r, _strad_r, _strad_r / _anchor_r))
P("    [stated, rev 28] he reads this surface as CLEAN VARNISHED PLYWOOD.")
P("    It is in the figure as an ANSWERED ANCHOR, not as a new question.")

P("\n--- A1/A2  THE ROOF POINTER, the rev-29 question ---")
r_res, r_flr, r_clip = report(ROOF,
                              "ROOF CROWN, aft of the opening, above the "
                              "drip rail")
import math as _m
_roof_r = r_res / r_flr
_d_anchor = abs(_m.log(_roof_r) - _m.log(_anchor_r))
_d_strad = abs(_m.log(_roof_r) - _m.log(_strad_r))
P("    log-distance to the ANSWERED anchor (%.2f x) : %.3f" % (_anchor_r,
                                                              _d_anchor))
P("    log-distance to the PROVEN straddler (%.2f x): %.3f" % (_strad_r,
                                                               _d_strad))
check(_d_anchor < _d_strad, "A1 the roof pointer does NOT straddle",
      "it sits %.1fx closer to a box he answered than to a proven straddle"
      % (_d_strad / _d_anchor if _d_anchor else float("inf")))
check(r_clip == 0.0, "A2 the roof pointer contains no clipped pixel")

P("\n" + "=" * 74)
P("CONTROLS: 6 checked, %d FAILED  %s"
  % (len(FAIL), ("-> " + "; ".join(FAIL)) if FAIL else ""))
P("=" * 74)
P("These are POINTERS, not sampling windows.  No number in rev 29 is taken")
P("from them.  They mark WHICH SURFACE the question is about.")
if FAIL:
    raise SystemExit("probe_updust_pointer: %d control(s) FAILED" % len(FAIL))
