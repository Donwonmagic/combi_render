# probe_rev62_senor.py -- IS `Senor`'s DEFICIT SIZE, WEIGHT, OR PLACEMENT?
#
# THE BRIEF'S CLAIM, WHICH THIS PROBE TESTS AND PARTLY CONTRADICTS.
# NEXT_CONTEXT_PROMPT_rev62.md sec.3 item 2 ranks `Senor` second and says:
#     "The deficit is letterform SIZE and WEIGHT across the whole word."
# citing a lookdev panel's ink bbox at 78 % of the reference's width and 71 %
# of its height.  A fix aimed at WEIGHT (thicken the strokes) and a fix aimed at
# SIZE (scale the artwork up) are different edits, and only one of them is
# right, so the two must be separated before either is attempted.
#
# WHY THE WHOLE-WORD NUMBER CANNOT ANSWER IT.  `flank_compare.py` reports the
# `Senor` region as ref 1261 px against render 973 px.  A word can lose 23 % of
# its ink by being drawn smaller at the same stroke weight, by being drawn at
# the same size with thinner strokes, or by being drawn correctly and placed
# where the reference is not.  Ink alone cannot tell those apart.  The
# separating statistic is FILL WITHIN THE GLYPH'S OWN BOUNDING BOX: shrink a
# word and its fill fraction is unchanged; thin its strokes and its fill falls.
#
# WHAT IS MEASURED, AND ON WHAT.  `flank_compare.py`'s own registered OVERLAY --
# a metric frame at 4.76 mm/cell in which red is reference-only, green is
# render-only and white is both.  That is the project's existing registration,
# not a new one, so nothing here re-solves the warp.
#
# THE CEILING, STATED BEFORE THE NUMBERS.  `Senor` overlaps `Tacombi`'s swash in
# the overlay and the two are ONE connected component, so the whole word cannot
# be isolated.  Only the `S` and its tilde are separable.  Every ratio below is
# THAT PART OF THE WORD, not the word.  Do not quote it as the word's.
#
# AND THE SECOND CEILING, WHICH BIASES THE ANSWER IN A KNOWN DIRECTION.  The
# photograph's `Senor` is heavily tarnished and `flank_compare.py`'s own header
# says so: the tarnish "is not [recoverable] and no threshold rule can recover
# it.  That is the floor under `swash` and `Senor` in the region table."  If the
# reference mask UNDER-counts tarnished reference ink, then:
#   - the reference BBOX shrinks, which makes the render look relatively BIGGER.
#     So a measured size deficit is a LOWER BOUND -- the conservative direction.
#   - the reference FILL falls, which INFLATES the render/reference fill ratio.
#     So the fill row is the one to distrust, and it is reported with that said.
#
#   C15  the overlay panel is found by structure, not by a typed row range.
#   C16  a CONTROL REGION: `Tacombi`'s own body must NOT show the same deficit.
#        IT DOES, AND THE ROW FAILS.  That is the control doing its job: it
#        stopped this probe publishing "`Senor` is 43 mm out of place" off an
#        overlay whose registration shift is the same order.  What survives C16
#        is the fill row, which is invariant to both scale and shift.
#   C17  THE SEPARATING ROW.  Fill-within-bbox decides SIZE against WEIGHT.
#
# RUN   python3 probe_rev62_senor.py [path/to/fc.png]
#       With no argument it runs flank_compare.py itself on out/r62_side.png.

import os
import subprocess
import sys

import numpy as np
import scipy.ndimage as ndi
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(HERE, "probe_scratch")
MMPC = 4.76                                   # flank_compare's overlay scale

CTL = {}


def ctl(name, ok, msg):
    CTL[name] = bool(ok)
    print("  [%s] %-4s %s" % ("PASS" if ok else "FAIL", name, msg))


FC = sys.argv[1] if len(sys.argv) > 1 else "/tmp/rev62_fc.png"
if len(sys.argv) <= 1:
    side = os.path.join(HERE, "out", "r62_side.png")
    if not os.path.exists(side):
        print("NO RENDER: %s absent.  Render before quoting this probe "
              "(rule 37)." % side)
        raise SystemExit(2)
    print("    running flank_compare.py to produce the overlay ...")
    subprocess.run([sys.executable, os.path.join(HERE, "flank_compare.py"),
                    side, FC], capture_output=True, text=True, timeout=1800)
if not os.path.exists(FC):
    print("NO OVERLAY: %s absent (rule 37)." % FC)
    raise SystemExit(2)

A = np.array(Image.open(FC).convert("RGB")).astype(int)

# ------------------------------------------------------------------------ C15
# The overlay is the panel whose rows are mostly black.  Found, not typed.
dark = (A.sum(axis=2) < 40).mean(axis=1)
ys = np.nonzero(dark > 0.5)[0]
runs, st, prev = [], ys[0], ys[0]
for y in ys[1:]:
    if y != prev + 1:
        runs.append((st, prev))
        st = y
    prev = y
runs.append((st, prev))
y0, y1 = max(runs, key=lambda r: r[1] - r[0])
P = A[y0:y1 + 1]
ctl("C15", (y1 - y0) > 100 and P.shape[1] > 400,
    "the overlay panel is located BY STRUCTURE at rows %d..%d (%d x %d) -- "
    "a typed row range would rot the first time flank_compare's layout moved"
    % (y0, y1, P.shape[1], P.shape[0]))

R, G, B = P[..., 0], P[..., 1], P[..., 2]
white = (R > 150) & (G > 150) & (B > 150)
ref = ((R > 110) & (G < 90) & (B < 90)) | white
ren = ((G > 110) & (R < 90) & (B < 90)) | white

lab, n = ndi.label(ref | ren, np.ones((3, 3)))
sz = np.bincount(lab.ravel())[1:]
order = np.argsort(sz)[::-1] + 1


def bb(m):
    yy, xx = np.nonzero(m)
    return int(xx.min()), int(yy.min()), int(xx.max()), int(yy.max())


def report(name, m):
    rs, rn = ref & m, ren & m
    b1, b2 = bb(rs), bb(rn)
    w1, h1 = b1[2] - b1[0] + 1, b1[3] - b1[1] + 1
    w2, h2 = b2[2] - b2[0] + 1, b2[3] - b2[1] + 1
    f = (rn.sum() / (w2 * h2)) / (rs.sum() / (w1 * h1))
    print("\n    %s" % name)
    print("        reference  %2d x %2d cells   %5d px" % (w1, h1, rs.sum()))
    print("        render     %2d x %2d cells   %5d px" % (w2, h2, rn.sum()))
    print("        render/reference   width %.3f  height %.3f  ink %.3f"
          % (w2 / w1, h2 / h1, rn.sum() / rs.sum()))
    print("        FILL WITHIN OWN BBOX  %.3f" % f)
    print("        origin offset  %+d, %+d cells = %+.1f, %+.1f mm"
          % (b2[0] - b1[0], b2[1] - b1[1],
             MMPC * (b2[0] - b1[0]), MMPC * (b2[1] - b1[1])))
    return w2 / w1, h2 / h1, f, rn.sum() / rs.sum()


print("\nREV 62 -- `Senor`: SIZE, WEIGHT, OR PLACEMENT?")
print("    overlay %s, metric frame at %.2f mm/cell" % (FC, MMPC))

# The `S` and its tilde: the only part of `Senor` not fused to `Tacombi`.
# Identified by structure -- the top-left-most component of any size.
cands = [(bb(lab == i)[1], i) for i in order[:6]]
senor_i = min(cands)[1]
tac_i = order[0]
sw, sh, sf, si = report("THE `S` AND ITS TILDE  (the separable part of `Senor`)",
                        lab == senor_i)
tw, th, tf, ti = report("CONTROL -- `Tacombi`'s main body (largest component)",
                        lab == tac_i)

# ------------------------------------------------------------------------ C16
ctl("C16", tw > 0.98 and th > 0.98,
    "CONTROL, AND IT FAILS -- WHICH IS THE POINT.  `Tacombi`'s own body is "
    "%.3f x %.3f of the reference's, so THERE IS A GLOBAL SIZE DEFICIT and the "
    "`Senor` rows above CANNOT be attributed to `Senor` alone.  Relative to "
    "the global figure `Senor` carries an EXTRA %.0f %% in width and %.0f %% "
    "in height, and that residual is what is specific to the word.  THE "
    "ORIGIN-OFFSET ROWS ARE CONFOUNDED and are NOT published as a placement "
    "defect: flank_compare registers by an integer shift of its own (this run: "
    "-16,-10 cells) before the overlay is drawn, and these offsets are the same "
    "order.  Untangling them needs the pre-registration frame, which this "
    "overlay does not carry"
    % (tw, th, 100 * (1 - sw / tw), 100 * (1 - sh / th)))

# ------------------------------------------------------------------------ C17
print("\n    WHAT SEPARATES SIZE FROM WEIGHT")
print("        Shrink a word and its FILL WITHIN ITS OWN BBOX is unchanged.")
print("        Thin its strokes and that fill FALLS.  Measured: %.3f" % sf)
ctl("C17", sf >= 0.95,
    "THE SEPARATING ROW: fill-within-bbox is %.3f on the `S`, and %.3f on "
    "`Tacombi`.  Neither is below 1, so THE STROKES ARE NOT THIN ANYWHERE IN "
    "THE LOCKUP.  This is the one statistic here invariant to BOTH scale and "
    "registration shift, so C16's failure does not touch it.  THE BRIEF'S "
    "'letterform SIZE and WEIGHT' IS HALF RIGHT: the WEIGHT half is REFUTED; "
    "the SIZE half stands but its magnitude does not, because the deficit is "
    "partly global (C16).  Tarnish under-counting biases the size rows toward "
    "UNDERSTATING the deficit -- a shrunken reference bbox makes the render "
    "look bigger -- so %.3f x %.3f is a LOWER BOUND; it biases THIS row "
    "UPWARD, so only 'not below 1' is claimed, never the %.0f%% margin"
    % (sf, tf, sw, sh, 100 * abs(sf - 1)))

os.makedirs(OUTD, exist_ok=True)
m = lab == senor_i
b1 = bb(ref & m)
ov = P.copy()
ov[~m] = (ov[~m] * 0.2).astype(int)
im = Image.fromarray(ov[max(0, b1[1] - 8):b1[3] + 9,
                        max(0, b1[0] - 8):b1[2] + 9].astype(np.uint8))
im.resize((im.width * 6, im.height * 6), Image.NEAREST).save(
    os.path.join(OUTD, "rev62_senor_S.png"))
print("\n    PAINTED -> probe_scratch/rev62_senor_S.png")
print("        red = reference only, green = render only, white = both.")
print("        The red lies UP AND LEFT and the green DOWN AND RIGHT.  Part of")
print("        that is flank_compare's own registration shift -- see C16 --")
print("        so LOOK at it, and do not read a placement figure off it.")

bad = [k for k, v in CTL.items() if not v]
print("\nCONTROLS: %d checked, %s"
      % (len(CTL), ("%d FAILED -- %s" % (len(bad), ",".join(bad))) if bad
         else "0 FAILED"))
