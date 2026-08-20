#!/usr/bin/env python3.11
"""
probe_rev47_gap.py -- rev 47.  THE WORD GAP, MEASURED FROM IMG_2073.jpeg.

WHY.  The owner reported the two words of the "100% Calidad" decal colliding.
rev 47 opened the gap to zero shared pixels and he looked at it and said IT
STILL DOES NOT READ AS TWO SEPARATE WORDS.  Zero shared pixels is CLEARANCE;
he is reporting LEGIBILITY, and they are different quantities.  Until
IMG_2073.jpeg arrived there was no frame that could settle it -- ref_playa_34
shows the burst at 23x39 px.  IMG_2073 shows it at ~44x61 px, and the two
words separate cleanly under a mask.

THE ESTIMATOR.  Mask the type (bright, low-saturation, inside the filled burst),
then find the reading angle BY SWEEPING IT -- rotate the mask over a range and
keep the angle whose row profile splits into exactly two bands with the deepest
trough.  The reading angle is NOT the mask's principal axis: two stacked words
make a roughly square block whose principal axis is meaningless, which is the
bug that made a first attempt report a 0.75 px cap height at 102 degrees.

CALIBRATION -- rule 22, and it is the whole point.  The same estimator is run
first on the BUILT decal, downsampled to the PHOTOGRAPH'S OWN SIZE, where the
answer is known by construction (LINE_GAP is set in cal_gen).  If it does not
recover the built gap at the photograph's resolution it cannot be trusted on
the photograph.  C3 is the KILL: a decal with the words far apart and one with
them touching must give different answers.
"""
import numpy as np
from PIL import Image
from scipy import ndimage as nd

Image.MAX_IMAGE_PIXELS = None
FAIL = 0; CHECKED = 0
def ck(label, ok, got):
    global FAIL, CHECKED
    CHECKED += 1
    if not ok: FAIL += 1
    print("  %-4s %-50s %s" % ("ok" if ok else "FAIL", label, got))

def bands(ty, Z, lo=-45.0, hi=10.0):
    """Sweep the reading angle; return (gap/cap, angle, cap_px, gap_px)."""
    best = None
    for ang in np.arange(lo, hi, 0.5):
        rot = nd.rotate(ty.astype(float), ang, reshape=True, order=1) > 0.5
        prof = rot.sum(1)
        nz = np.nonzero(prof)[0]
        if len(nz) == 0: continue
        seg, run = [], None
        for i in range(nz.min(), nz.max() + 2):
            p = prof[i] if i < len(prof) else 0
            if p > 0 and run is None: run = i
            if p == 0 and run is not None:
                seg.append((run, i - 1)); run = None
        seg = [s for s in seg if (s[1] - s[0] + 1) > Z * 1.5]
        if len(seg) != 2: continue
        cap = (seg[0][1] - seg[0][0] + 1) / Z
        gap = (seg[1][0] - seg[0][1] - 1) / Z
        if gap <= 0: continue
        if best is None or gap > best[3]:
            best = (gap / cap, ang, cap, gap)
    return best

def type_mask(img, Z):
    big = img.resize((img.width * Z, img.height * Z), Image.LANCZOS)
    a = np.asarray(big.convert("RGB"), np.float32)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(2); sat = (mx - a.min(2)) / np.maximum(mx, 1)
    red = (R > 90) & (R - G > 40) & (R - B > 25)
    burst = nd.binary_fill_holes(nd.binary_closing(red, np.ones((9, 9))))
    lab, n = nd.label(burst)
    if n > 1:
        burst = lab == (int(np.argmax(nd.sum(burst, lab, range(1, n + 1)))) + 1)
    ty = nd.binary_opening(burst & (mx > 150) & (sat < 0.30), np.ones((5, 5)))
    return ty, burst

print("=" * 64)
print("  probe_rev47_gap -- calibrate on the BUILD, then read the PHOTOGRAPH")
print("=" * 64)

# ---------------------------------------------------------- CALIBRATION
import importlib.util
spec = importlib.util.spec_from_file_location("cg", "cal_gen.py")
cg = importlib.util.module_from_spec(spec); spec.loader.exec_module(cg)
TRUTH = None
d = Image.open("tex/calidad.png").convert("RGB")
# the built decal, shrunk to the photograph's own burst size (~44 px across)
for target in (44,):
    k = target / float(d.width) * 3.0     # decal canvas is wider than the burst
    small = d.resize((max(8, int(d.width * k)), max(8, int(d.height * k))), Image.LANCZOS)
    tyb, _ = type_mask(small, 8)
    rb = bands(tyb, 8)
    if rb:
        print("  BUILT at photo scale: gap/cap %.3f  angle %.1f  cap %.2f px  gap %.2f px"
              % rb)
        TRUTH = rb[0]
# ------------------------------------------------------------ rev 48 FIX
# THIS WAS A FROZEN LITERAL AND IT MADE C1 LIE IN BOTH DIRECTIONS.
#
# It read `built_truth = 0.111`, commented "the build's own construction
# value, from cal_gen".  It was not from cal_gen; it was typed, and it was the
# construction gap for LINE_GAP = 0.26.  Commit 1bfc97a changed LINE_GAP
# 0.26 -> 0.43, regenerated tex/calidad.png AND created this probe, all in one
# commit -- and the probe was never re-run against the new raster.  Both
# NEXT_CONTEXT_PROMPT_rev48.md sec.12 and LEDGER_rev47.md sec.8 report
# "3 checked, 0 FAILED"; the machine says 3 checked, 1 FAILED.
#
# AND THE FAILURE POINTED THE WRONG WAY.  At LINE_GAP = 0.43 the estimator
# reads 0.281 against a construction 0.2776 -- 1.2 % error, its most accurate
# operating point.  C1 was failing BECAUSE the instrument had become right.
# It passed when the estimator was 34 % wrong and failed when it was 1 % right:
# a control ANTI-CORRELATED with the health of the thing it measures.  SPEC
# 10.116.6, and rule 2 -- expressed is not enough if it is expressed against a
# frozen measurement; derive it at run time.
#
# Derived now, from cal_gen's own constants, so it tracks LINE_GAP for ever.
# The 0.0258 canvas / 0.2326 cap pair is rev 47's watched-print measurement of
# the clear gap AT LINE_GAP = 0.26, and the LINE_GAP term is the delta from it.
import cal_gen as _CG
_GAP_026_CANVAS = 0.0258          # watched print, rev 47, at LINE_GAP = 0.26
_CAP_100_CANVAS = 0.2326          # watched print, rev 47, the "100%" cap
built_truth = (_GAP_026_CANVAS
               + (_CG.LINE_GAP - 0.26) * _CG.CAP_100) / _CAP_100_CANVAS
print("  built_truth DERIVED from cal_gen: LINE_GAP %.3f -> construction "
      "gap/cap %.4f  (frozen literal was 0.111, valid only at LINE_GAP 0.26)"
      % (_CG.LINE_GAP, built_truth))
ck("C1 estimator recovers the BUILT gap at photo scale (+/-35%)",
   TRUTH is not None and abs(TRUTH - built_truth) / built_truth < 0.35,
   ("%.3f vs construction %.3f" % (TRUTH, built_truth)) if TRUTH else "no two bands")

# C2/C3 KILL: a wide gap and a touching pair must differ
print("-- C2/C3 kill controls, synthetic at the photograph's scale --")
def synth(gap_frac, Z=8, cap=14):
    h = int(cap * (2 + gap_frac) + 12); w = 60
    a = np.zeros((h, w), np.uint8)
    a[6:6 + cap, 6:44] = 1
    y2 = int(6 + cap + gap_frac * cap)
    a[y2:y2 + cap, 10:52] = 1
    return a.astype(bool)
r_wide = bands(synth(0.60), 1); r_touch = bands(synth(0.0), 1)
ck("C2 a WIDE synthetic gap is recovered",
   r_wide is not None and abs(r_wide[0] - 0.60) < 0.15,
   "%.3f (truth 0.600)" % r_wide[0] if r_wide else "no two bands")
ck("C3 KILL: touching words give NO two-band split",
   r_touch is None, "two bands found -- estimator is blind" if r_touch else "correctly refused")

# ---------------------------------------------------------- MEASUREMENT
print()
print("-- PHOTOGRAPH IMG_2073.jpeg --")
im = Image.open("IMG_2073.jpeg").convert("RGB").crop((1108, 360, 1210, 445))
ty, burst = type_mask(im, 8)
ys, xs = np.nonzero(burst)
print("    burst %.1f x %.1f native px   type px %d"
      % ((xs.max() - xs.min() + 1) / 8, (ys.max() - ys.min() + 1) / 8, ty.sum()))
r = bands(ty, 8)
if r:
    print("    PHOTO: gap/cap %.3f   reading angle %.1f deg   cap %.2f px   gap %.2f px"
          % r)
    print()
    print("RESULT: photographed gap = %.1f%% of cap height;  built = %.1f%%"
          % (100 * r[0], 100 * built_truth))
else:
    print("    NOT SEPARABLE -- refusing to publish a number")
print()
print("CONTROLS: %d checked, %d FAILED" % (CHECKED, FAIL))
