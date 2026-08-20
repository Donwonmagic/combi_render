#!/usr/bin/env python3.11
"""
probe_rev47_sharp.py -- rev 47.  THE SHARPNESS INSTRUMENT, AND ITS CALIBRATION.

WHY IT EXISTS.  Three revisions chased a CONTRAST number for a SHARPNESS fault
(LEDGER_rev46 sec.3).  The metric this item should have used all along is the
10-90% alpha edge width divided by the mean stroke width: dimensionless, so a
4096-px texture and a 1024-px photograph are directly comparable.

THE ESTIMATOR, and why it needs no contour tracer.
  By the co-area formula, sum|grad a| over the image equals the integral of the
  level-set perimeter over levels, so for an image whose level sets are near
  parallel it IS the edge length P.  For a 1-D ramp of full width W the band
  0.1<a<0.9 has area 0.8*W per unit length, and sum|grad a| per unit length is
  1.  Hence

      edge_width_10_90 = count(0.1 < a < 0.9) / sum(|grad a|)

  and the mean stroke width comes from the Euclidean distance transform: for a
  slab of width w the mean interior EDT is w/4, so w = 4*mean(EDT).

SPEC 10.116.6 / rule 20: AN INSTRUMENT THAT HAS NEVER BEEN WRONG HAS NEVER BEEN
TESTED.  Rule 22: CALIBRATE AGAINST A KNOWN DISPLACEMENT AT THE REAL DATA'S
RESOLUTION.  So this file does not merely measure -- it first blurs a synthetic
by a KNOWN sigma at 4096 px, the real texture's own width, and checks that the
number tracks the truth.  A Gaussian edge has a 10-90 width of 2*1.2816*sigma
= 2.5631*sigma; if the estimator does not reproduce that it is not measuring
sharpness and nothing it says about senor.png is worth reading.

C4 is the KILL CONTROL and it is the one that matters: a sharp raster and a
blurred one MUST give different numbers.  An estimator that returns the same
answer for the defect and its absence is blind and will look healthy forever.
"""
import sys, numpy as np
from PIL import Image
from scipy import ndimage as nd

Image.MAX_IMAGE_PIXELS = None
FAIL = 0; CHECKED = 0

def ck(label, ok, got):
    global FAIL, CHECKED
    CHECKED += 1
    if not ok: FAIL += 1
    print("  %-4s %-52s %s" % ("ok" if ok else "FAIL", label, got))

# ----------------------------------------------------------------- estimator
def edge_width_10_90(a):
    """a in [0,1] float. Returns the mean 10-90% ramp width in pixels."""
    gy, gx = np.gradient(a)
    g = np.hypot(gx, gy)
    P = g.sum()
    if P <= 0: return float('nan')
    band = np.count_nonzero((a > 0.1) & (a < 0.9))
    return band / P

def stroke_width(a):
    """Mean stroke width in px: 4 * mean interior EDT of the a>0.5 core."""
    core = a > 0.5
    if core.sum() == 0: return float('nan')
    d = nd.distance_transform_edt(core)
    return 4.0 * d[core].mean()

def softness_frac(a):
    """LEDGER rev46 sec.3's figure: fraction of ink px in the 0.1-0.9 band."""
    ink = a > 0.1
    if ink.sum() == 0: return float('nan')
    return np.count_nonzero((a > 0.1) & (a < 0.9)) / ink.sum()

def report(a, name):
    ew, sw = edge_width_10_90(a), stroke_width(a)
    print("    %-22s edge10-90 %8.3f px   stroke %8.2f px   RATIO %.4f   soft %.4f"
          % (name, ew, sw, ew / sw, softness_frac(a)))
    return ew, sw, ew / sw

# ----------------------------------------------------------- the calibration
# THE FIRST HARNESS THIS PROBE HAD WAS WRONG, AND ITS OWN CONTROLS SAID SO.
# It drew 60-px bars and blurred them by sigma up to 40.  At sigma 20 the alpha
# at a bar's CENTRE is 0.866 -- it never reaches 0.9 -- so the whole bar counts
# as "band" and the estimator over-reported by 26%, then 44% at sigma 40.  That
# is not the estimator failing; it is the SYNTHETIC violating the estimator's
# validity regime, which is edge width << stroke width.  The harness is fixed
# rather than the threshold loosened (rule 19), and C6 below now WATCHES the
# estimator break when the regime is violated, so the limit is guarded, stated,
# and demonstrated instead of merely believed.
def synth(n=4096, sigma=0.0, bar=400, pitch=1000, aa=4):
    """A synthetic at THE REAL DATA'S RESOLUTION: 4096 px across.  Edges are
    ANTIALIASED (drawn at aa x and box-downsampled), because real 'sharp' data
    is antialiased and an ideal binary step has a 10-90 band of exactly zero
    pixels -- which is why C1's first form was measuring a degenerate case."""
    N, H = n * aa, (n // 4) * aa
    a = np.zeros((H, N), np.float32)
    # +aa//2 puts every bar edge HALF A SOURCE PIXEL off the output grid.  On
    # the exact grid the box-downsample returns a perfectly binary edge and the
    # 0.1-0.9 band is empty -- which is what made C1 read 0.000 and is a
    # degenerate case, not sharp data.
    for cx in range(pitch * aa // 2, N - pitch * aa // 2, pitch * aa):
        a[:, cx - bar * aa // 2 + aa // 2: cx + bar * aa // 2 + aa // 2] = 1.0
    a = a.reshape(n // 4, aa, n, aa).mean(axis=(1, 3))
    if sigma > 0:
        a = nd.gaussian_filter(a, sigma)
    return np.clip(a, 0, 1)

print("=" * 66)
print("  probe_rev47_sharp -- calibration first, measurement second")
print("=" * 66)
print("-- CALIBRATION at 4096 px, the real texture's own width --")

sharp = synth(sigma=0.0)
ew0, sw0, r0 = report(sharp, "synthetic sharp")

# C1  a sharp edge must read about one pixel, not zero and not ten.
ck("C1 sharp synthetic edge width in [0.5, 2.0] px",
   0.5 <= ew0 <= 2.0, "%.3f px" % ew0)

# C2  the known stroke width is 60 px by construction.
ck("C2 stroke width recovers the built 400 px (+/-5%%)",
   abs(sw0 - 400.0) / 400.0 < 0.05, "%.2f px (truth 400.00)" % sw0)

# C3  THE TRACKING TEST.  Blur by a KNOWN sigma; a Gaussian edge's 10-90 width
#     is 2*1.2816*sigma.  The estimator must reproduce it across a decade.
print("-- C3 does it TRACK a known blur? --")
# THE FLOOR IS REAL AND IT IS STATED RATHER THAN HIDDEN.  The band is an
# INTEGER pixel count, so at a ramp of only a few px the quantisation alone is
# worth double figures.  C3 asserts tracking where the ramp is resolved
# (edge >= 10 px, sigma >= 4); C3b records the floor below it so that a future
# revision reads the limit instead of rediscovering it.  The rev-46 built
# texture measures a 14.08 px ramp -- inside C3's asserted band.
worst = 0.0; floor_err = 0.0
for s in (2.0, 5.0, 10.0, 20.0, 40.0):   # bar is 400 px, so all stay in regime
    a = synth(sigma=s)
    ew = edge_width_10_90(a)
    truth = 2.5631 * s
    err = abs(ew - truth) / truth
    if s >= 4.0: worst = max(worst, err)
    else:        floor_err = max(floor_err, err)
    print("    sigma %5.1f   truth %8.3f   measured %8.3f   err %5.1f%%%s"
          % (s, truth, ew, 100 * err, "   <- below the resolved floor" if s < 4 else ""))
ck("C3 tracks known blur to within 8%% where ramp >= 10 px", worst < 0.08,
   "worst %.1f%%" % (100 * worst))
ck("C3b floor is recorded: sub-10-px ramps are good to ~20%% only",
   floor_err < 0.20, "%.1f%% at sigma 2 (ramp 5 px)" % (100 * floor_err))

# C4  THE KILL CONTROL.  Sharp and blurred MUST differ.  Rule 19/22.
blur = synth(sigma=15.0)
ewb = edge_width_10_90(blur)
ck("C4 KILL: sharp vs blurred give DIFFERENT numbers",
   ewb > 5.0 * ew0, "sharp %.3f vs blurred %.3f  (%.1fx)" % (ew0, ewb, ewb / ew0))

# C6  WATCH IT FAIL.  Rule 19: a control is finished when you have seen it go
#     red on the defect.  Re-run C3's worst case on the ORIGINAL 60-px bars --
#     edge width comparable to stroke width -- and require that the estimator
#     DOES break there.  If this ever passes quietly, the regime limit has moved
#     and every ratio in this file needs re-deriving.
narrow = synth(sigma=40.0, bar=60, pitch=400)
ew_bad = edge_width_10_90(narrow)
truth_bad = 2.5631 * 40.0
err_bad = abs(ew_bad - truth_bad) / truth_bad
ck("C6 WATCHED-FAIL: estimator DOES break when edge ~ stroke",
   err_bad > 0.25, "err %.1f%% on 60-px bars (must be >25%%)" % (100 * err_bad))

# C5  BLINDNESS TEST ON THE RATIO.  The ratio must be scale-invariant: the same
#     shape rendered at half the pixels must give the same RATIO.  If it does
#     not, the ratio cannot compare a texture to a photograph and the whole
#     dimensionless argument collapses.
_s10 = synth(sigma=10.0)
half = np.asarray(Image.fromarray((_s10 * 255).astype(np.uint8))
                  .resize((2048, 512), Image.LANCZOS), np.float32) / 255.0
rf = edge_width_10_90(_s10) / stroke_width(_s10)
rh = edge_width_10_90(half) / stroke_width(half)
ck("C5 ratio is scale-invariant (4096 vs 2048, within 10%%)",
   abs(rf - rh) / rf < 0.10, "%.4f vs %.4f" % (rf, rh))

# ------------------------------------------------------------ measurement
print()
print("-- MEASUREMENT: tex/senor.png --")
im = Image.open("tex/senor.png")
if im.mode != "RGBA":
    print("    NOTE senor.png mode is %s" % im.mode)
a = np.asarray(im.split()[-1], np.float32) / 255.0
print("    senor.png %dx%d" % (im.size[0], im.size[1]))
ew, sw, ratio = report(a, "BUILT tex/senor.png")

# ------------------------------------------------- stroke weight, and a trap
# THE EYE SAYS THE BUILT STROKES ARE TOO FAT.  Beside the photograph they look
# bloated and the counters look choked.  Rev 46 had exactly this impression
# about the VW glyph and it evaporated on measurement.  So measure it -- and
# CONTROL IT FIRST, because the obvious comparison is the wrong one.
#
# C7 is the control and IT FAILS BY DESIGN AT MISMATCHED SCALE: the EDT stroke
# estimator is NOT scale-invariant across a 15x resolution gap (4096 px built
# against 271 px photographed differ by 16.6% on the SAME texture).  Comparing
# the 4096-px build to the 271-px photograph therefore measures the estimator's
# resolution bias, not the artwork.  Downsample the build to the photograph's
# own ink width first.  SPEC 10.110.8: a part measured in isolation from what
# it is fitted to is not measured -- here, from the RESOLUTION it is compared at.
print()
print("-- stroke weight, dimensionless (stroke / ink bbox width) --")
_ys, _xs = np.nonzero(a > 0.1)
_bw = _xs.max() - _xs.min() + 1
r_hi = stroke_width(a) / _bw
_sm = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).resize(
    (int(a.shape[1] * 271 / _bw), int(a.shape[0] * 271 / _bw)), Image.LANCZOS),
    np.float32) / 255.0
_y2, _x2 = np.nonzero(_sm > 0.1)
_bw2 = _x2.max() - _x2.min() + 1
r_lo = stroke_width(_sm) / _bw2
print("    built @4096  %.5f      built @271  %.5f" % (r_hi, r_lo))
ck("C7 WATCHED-FAIL: stroke ratio is NOT scale-invariant",
   abs(r_hi - r_lo) / r_hi > 0.05,
   "%.1f%% apart -- so compare at MATCHED resolution only"
   % (100 * abs(r_hi - r_lo) / r_hi))

ref = np.asarray(Image.open("ref_side.jpg").convert("RGB").crop((318, 462, 614, 598)),
                 np.float32)
_mx, _mn = ref.max(2), ref.min(2)
_sat = (_mx - _mn) / np.maximum(_mx, 1)
vals = []
for st in (0.25, 0.30, 0.35, 0.40):
    for bt in (60, 70, 80, 90):
        ink = nd.binary_opening((_sat < st) & (_mx > bt), np.ones((2, 2)))
        if ink.sum() < 500: continue
        yy, xx = np.nonzero(ink); w = xx.max() - xx.min() + 1
        if not (250 < w < 290): continue
        vals.append(stroke_width(ink) / w)
v = np.array(vals)
sig = abs(r_lo - v.mean()) / max(v.std(), 1e-9)
print("    photo @271   %.5f +/- %.5f over %d threshold pairs" % (v.mean(), v.std(), len(v)))
ck("C8 built stroke weight matches the photograph within 3 sigma",
   sig < 3.0, "built %.5f vs photo %.5f -- %.1f sigma" % (r_lo, v.mean(), sig))

print()
print("CONTROLS: %d checked, %d FAILED" % (CHECKED, FAIL))
print("RESULT: built edge10-90 %.3f px, stroke %.2f px, RATIO %.4f, soft %.4f"
      % (ew, sw, ratio, softness_frac(a)))
