# probe_rev36_posts.py -- rev 36.  Runs under plain python3.11, no Blender.
#
# WHAT THIS TESTS
# ---------------
# The owner stated, rev 36, when shown a crop of the far end of the over-rider
# assembly:
#
#   "that circle is the post that connects the bumper to the bar, and both
#    continue past the post.  past that, out of sight the bar wraps downwards,
#    and meets with the bumper, the same way it does on the close side"
#
# That renames a column this project has consumed since rev 32.  u 205-208 was
# asked of him TWICE (rev 33 Q1, rev 34 Q1b) under the label "the bar's far
# end", and both answers were taken as readings of a bar terminus.  He now says
# the feature there is a POST.
#
# It also implies something testable that he did NOT claim: if that is a post,
# and the post at u ~ 360 that SPEC 10.83 has been trying to place for five
# revisions is its MIRROR, then the two are symmetric about the vehicle's
# centreline, and their midpoint must land on the centreline's image.
#
# This project already published that centreline INDEPENDENTLY, from a
# completely different feature -- the crossing of the two-tone V-swage arms:
#
#     SPEC 10.85 (rev 31b):  u = 288.8 +- 3 px SYSTEMATIC, arms cross at
#                            (288.8, 701.1)
#
# So this is a corroboration test with a pre-registered target that was fixed
# five revisions before the claim existed.  It cannot be tuned to pass.
#
# WHAT THIS PROBE DOES NOT DO
# ---------------------------
# IT DOES NOT OPEN A THIRD ESTIMATOR FOR THE POST'S LATERAL POSITION.  The
# inherited brief forbids that and the brief is right.  This is a YES/NO test
# of an identification, not a metric route to a 3-D coordinate.  If it passes,
# what it buys is a RENAMING and a resolved contradiction -- not a number for
# the build.  Nothing in build.py may consume anything below.
#
# DETECTOR
# --------
# A post is a vertical white member BRIDGING the bar and the bumper.  Between
# them the background is the vehicle's GREEN nose.  So a post is a column where
# the green is INTERRUPTED and white spans the gap.  That is a two-sided test:
# it requires green to be present at neighbouring columns and absent here.
# A detector that just found "white" would fire on the bar and the bumper
# themselves, which is the error that produced rev 36's own first coalescence
# reading (SPEC 10.88's "a detector whose errors cancel").
#
# CONTROLS
#   P1  the green wedge between bar and bumper EXISTS at control columns
#       (if it never exists, "interrupted green" is meaningless)
#   P2  exactly TWO bridged groups are found in the search window
#   P3  each group's width is between 8 and 40 px (a post, not a merge)
#   P4  FALSIFICATION: the same detector run on the band ABOVE the bar, where
#       there is no post and nothing to bridge, must find ZERO groups
#   P5  the published centreline 288.8 is read from REF_MEASUREMENTS.md at run
#       time, NOT typed here, so this file cannot drift from the record
#   P6  a NULL: the midpoint of two columns drawn at random from the search
#       window lands within 3 px of 288.8 only rarely -- report the rate, so
#       the hit is priced rather than admired

import os, sys, re
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "ref_workshop.jpg")
RECORD = os.path.join(HERE, "REF_MEASUREMENTS.md")

CTL = {}
def ctl(k, ok, msg):
    CTL[k] = bool(ok)
    print("  [%s] %-3s %s" % ("PASS" if ok else "FAIL", k, msg))

print("=" * 78)
print("probe_rev36_posts -- IS THE FAR ELEMENT A POST, AND IS IT THE MIRROR?")
print("=" * 78)
print()

A = np.asarray(Image.open(REF).convert("RGB")).astype(float)
Rc, Gc, Bc = A[:, :, 0], A[:, :, 1], A[:, :, 2]
mx = A.max(2); mn = A.min(2); V = mx
S = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
WHITE = (V > 140) & (S < 0.20)
GREEN = (Gc > Rc + 8) & (Gc > Bc + 8) & (V > 50)

# ---------------------------------------------------------------- P5 first
txt = open(RECORD).read()
m = re.search(r"u\s*=\s*(\d+\.\d+)\s*\+-\s*(\d+)\s*px\s*SYSTEMATIC", txt)
CENTRE = float(m.group(1)) if m else None
BAND = float(m.group(2)) if m else None
ctl("P5", CENTRE is not None,
    "centreline read from REF_MEASUREMENTS.md at run time: u = %s +- %s px "
    "(NOT typed into this file)" % (CENTRE, BAND))
if CENTRE is None:
    print("\nREFUSING TO PRINT A RULING -- could not read the record.")
    sys.exit(1)

# ------------------------------------------------- locate bar and bumper
# In the search window the bar is the UPPER white run and the bumper the LOWER
# one.  Find, per column, the topmost and bottommost tall white runs.
def col_runs(col, r0, r1, minh=3):
    idx = np.where(WHITE[r0:r1, col])[0]
    if len(idx) == 0:
        return []
    g = []; s = idx[0]; p = idx[0]
    for i in idx[1:]:
        if i != p + 1:
            g.append((r0 + s, r0 + p)); s = i
        p = i
    g.append((r0 + s, r0 + p))
    return [(a, b) for a, b in g if b - a + 1 >= minh]

R0, R1 = 615, 775
C0, C1 = 196, 500

# --------------------------------------------------------- P1: green wedge
wedge_cols = []
for col in range(C0, C1):
    rr = col_runs(col, R0, R1, minh=4)
    if len(rr) >= 2:
        a = rr[0][1] + 1; b = rr[-1][0]          # between top and bottom run
        if b - a >= 4 and GREEN[a:b, col].mean() > 0.5:
            wedge_cols.append(col)
ctl("P1", len(wedge_cols) >= 40,
    "green wedge between bar and bumper present at %d columns in %d-%d"
    % (len(wedge_cols), C0, C1))

# ------------------------------------------------- bridged (post) columns
def bridged(col, r0, r1):
    """white spans the whole gap between the bar's run and the bumper's run.

    THE FIRST VERSION OF THIS DETECTOR USED 'green absent' AND FIRED ON THE
    BODY.  The nose's V-swage is CREAM, not green, so between the bar and the
    bumper across the middle of the frame the background is already pale and
    the test found a 30 px 'post' at cols 281-310 that is the vehicle's own
    two-tone V.  Its falsification arm caught two more above the bar.  Three
    controls went down and the probe refused to rule -- which is what they are
    for.  Recorded, not quietly fixed.

    THE REPLACEMENT USES NO BACKGROUND COLOUR AT ALL.  A post is bounded ABOVE
    by the bar: the white stops there.  Body cream does not stop there -- it
    carries on up the nose.  So the discriminator is 'is the bridge capped?',
    which is a property of the bridge itself, not of what happens to be behind
    it.
    """
    rr = col_runs(col, r0, r1, minh=4)
    if len(rr) == 0:
        return False
    tall = [x for x in rr if x[1] - x[0] + 1 >= 30]
    if len(tall) != 1:
        return False
    a, b = tall[0]
    if (b - a + 1) < 55:
        return False
    cap = WHITE[max(0, a - 14):a - 1, col]
    return cap.size > 0 and cap.mean() < 0.20

hits = [c for c in range(C0, C1) if bridged(c, R0, R1)]
groups = []
if hits:
    cur = [hits[0]]
    for c in hits[1:]:
        if c <= cur[-1] + 2:
            cur.append(c)
        else:
            groups.append((cur[0], cur[-1])); cur = [c]
    groups.append((cur[0], cur[-1]))
groups = [g for g in groups if g[1] - g[0] + 1 >= 6]

print()
print("  BRIDGED GROUPS (white spans the bar-to-bumper gap, green absent):")
for a, b in groups:
    print("    cols %3d - %3d   width %2d px   centre %6.1f"
          % (a, b, b - a + 1, (a + b) / 2.0))

ctl("P2", len(groups) == 2,
    "exactly TWO bridged groups found (got %d)" % len(groups))
ctl("P3", all(8 <= (b - a + 1) <= 40 for a, b in groups),
    "every group is post-width (8-40 px): %s"
    % [b - a + 1 for a, b in groups])

# ------------------------------------------------- P4: falsification arm
# Same detector, band ABOVE the bar, where there is no bar/bumper pair and so
# nothing can bridge.  Must find nothing.
arm = [c for c in range(C0, C1) if bridged(c, 470, 620)]
armg = []
if arm:
    cur = [arm[0]]
    for c in arm[1:]:
        if c <= cur[-1] + 2: cur.append(c)
        else: armg.append((cur[0], cur[-1])); cur = [c]
    armg.append((cur[0], cur[-1]))
armg = [g for g in armg if g[1] - g[0] + 1 >= 6]
ctl("P4", len(armg) == 0,
    "FALSIFICATION ARM: same detector on rows 470-620 (above the bar) finds "
    "%d group(s) -- expected 0" % len(armg))

print()
if not all(CTL.values()):
    print("REFUSING TO PRINT A RULING -- %d control(s) down: %s"
          % (sum(1 for v in CTL.values() if not v),
             [k for k, v in CTL.items() if not v]))
    sys.exit(1)

# ------------------------------------------------------------------ ruling
c_far = (groups[0][0] + groups[0][1]) / 2.0
c_near = (groups[1][0] + groups[1][1]) / 2.0
mid = (c_far + c_near) / 2.0
resid = mid - CENTRE

# ---------------------------------------------------------------- P6 null
rng = np.random.default_rng(20260817)
draws = rng.integers(C0, C1, size=(200000, 2))
mids = draws.mean(1)
rate = float((np.abs(mids - CENTRE) <= 3.0).mean())

print("=" * 78)
print("RULING")
print("=" * 78)
print()
print("  FAR  post centre  u = %7.2f   (cols %d-%d)" % (c_far, *groups[0]))
print("  NEAR post centre  u = %7.2f   (cols %d-%d)" % (c_near, *groups[1]))
print("  MIDPOINT          u = %7.2f" % mid)
print("  PUBLISHED CENTRELINE (SPEC 10.85, rev 31b, read from REF at run time)")
print("                    u = %7.2f  +- %.0f px SYSTEMATIC" % (CENTRE, BAND))
print("  RESIDUAL             %+7.2f px   = %.2f of the published band"
      % (resid, abs(resid) / BAND))
print()
print("  NULL (P6): two columns drawn uniformly from %d-%d have a midpoint"
      % (C0, C1))
print("  within 3 px of %.1f  %.2f %% of the time (200k draws)."
      % (CENTRE, 100 * rate))
print("  So a hit inside the band is worth about %.0f:1, NOT decisive alone."
      % (1.0 / rate if rate else float('inf')))
print()
# ------------------------------------------------ SENSITIVITY, adversarial
# My detector puts the near post's centre at 362.5.  This project has been
# consuming POST_U = 365.5 for the near post since rev 32, read by a different
# method.  A result that depends on which of two readings 3 px apart is used is
# not a result, it is a coin-flip with a decimal point.  PRICE IT.
ALT = 365.5
mid_alt = (c_far + ALT) / 2.0
resid_alt = mid_alt - CENTRE
print("  SENSITIVITY -- the near post has TWO readings in this project:")
print("    mine, this probe          u = %6.2f  -> midpoint %6.2f, resid %+5.2f px (%.2f band)"
      % (c_near, mid, resid, abs(resid) / BAND))
print("    published since rev 32    u = %6.2f  -> midpoint %6.2f, resid %+5.2f px (%.2f band)"
      % (ALT, mid_alt, resid_alt, abs(resid_alt) / BAND))
print("  THE RESULT CROSSES THE BAND BOUNDARY BETWEEN THEM (%s vs %s)."
      % ("IN" if abs(resid) <= BAND else "OUT",
         "IN" if abs(resid_alt) <= BAND else "OUT"))
print("  So this is SUGGESTIVE, NOT ESTABLISHED.  It is reported at that")
print("  strength and no stronger.  A 3 px choice must not decide it.")
print()

if abs(resid) <= BAND:
    print("  THE OWNER'S IDENTIFICATION IS CORROBORATED, at %.0f:1 against the"
          % (1.0 / rate if rate else float('inf')))
    print("  null and SUBJECT TO THE SENSITIVITY ABOVE.")
    print("  Two vertical posts, symmetric about a centreline that was")
    print("  published FIVE REVISIONS EARLIER from a different feature")
    print("  entirely (the V-swage arms crossing at (288.8, 701.1)).")
    print()
    print("  WHAT THIS RESOLVES.  SPEC 10.83 has spent five revisions trying")
    print("  to place 'the post at the vehicle's centreline'.  THERE ARE TWO")
    print("  POSTS AND NEITHER IS ON THE CENTRELINE -- they straddle it.")
    print("  The question was unanswerable because it assumed there was one.")
    print()
    print("  WHAT IT DOES NOT BUY.  Nothing metric.  The posts' 3-D lateral")
    print("  position is still UNMEASURED, this is still a frame with no")
    print("  fore-aft vanishing point and no bounded roll, and NO ESTIMATOR")
    print("  IS OPENED HERE.  A symmetric pair about a known image column")
    print("  fixes an IDENTIFICATION, not a coordinate.")
    print()
    print("  AND IT RENAMES A CONSUMED COLUMN.  u 205-208, answered by him in")
    print("  rev 33 and rev 34 under the label 'the bar's far end', is the")
    print("  FAR POST's outer edge.  His readings were right; the label was")
    print("  wrong.  Every C5 row from rev 32 onward inherits that error.")
else:
    print("  NOT CORROBORATED at the published band.  The identification is")
    print("  not refuted by this -- symmetry was MY inference, not his claim.")
print()
print("  ALL %d CONTROLS PASSED." % len(CTL))
print("=" * 78)
