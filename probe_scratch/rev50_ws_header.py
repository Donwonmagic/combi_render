"""rev50 nose/front -- IS THE WINDSCREEN APERTURE'S TOP EDGE STRAIGHT?

ref_workshop.jpg, GREEN bus, GEOMETRY ONLY.  The glass is out, so the top of
each screen aperture is a hard cream->dark step.  A straight 3-D line projects
to a straight image line under ANY perspective camera.  So: trace the step
down each column, fit ONE straight line to the whole run, and report the
residual; then fit two lines, one per pane, and report the included angle.

CEILING: the trace is the 50 % crossing between the cream header and the dark
cab interior.  Where something pale is parked behind the screen (the wall, the
extinguisher) the step weakens; columns whose contrast is under CMIN are
dropped and the count is printed.  A curved header would also break the
one-line fit -- this test separates STRAIGHT from NOT-STRAIGHT, not vee from
arc.
"""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('ref_workshop.jpg').convert('RGB')).astype(float)
L = im @ np.array([0.299, 0.587, 0.114])

# search window: above = cream header, below = dark interior
Y0, Y1 = 330, 400
CMIN = 45.0

rows = []
for x in range(255, 545):
    col = L[Y0:Y1, x]
    hi = col[:6].mean()          # header
    lo = col[-10:].mean()        # interior
    if hi - lo < CMIN:
        continue
    thr = 0.5 * (hi + lo)
    idx = np.nonzero(col < thr)[0]
    if len(idx) == 0:
        continue
    i = idx[0]
    if i == 0:
        continue
    # linear subpixel
    a, b = col[i-1], col[i]
    t = (a - thr) / (a - b)
    rows.append((x, Y0 + i - 1 + t))

rows = np.array(rows)
print("columns used: %d of %d  (x %d..%d)" % (len(rows), 545-255, rows[:,0].min(), rows[:,0].max()))

def fit(r):
    A = np.vstack([r[:,0], np.ones(len(r))]).T
    c, res, *_ = np.linalg.lstsq(A, r[:,1], rcond=None)
    pred = A @ c
    return c, r[:,1]-pred

c, resid = fit(rows)
print("ONE LINE   slope %+.5f  rms resid %.3f px  max |resid| %.2f px" %
      (c[0], resid.std(), np.abs(resid).max()))

# where is the divider?  scan for the split in the trace: the divider is a
# bright vertical member, so those columns were dropped by CMIN.  print gaps.
xs = rows[:,0]
gaps = np.nonzero(np.diff(xs) > 1)[0]
for g in gaps:
    print("   gap in trace: x %d .. %d" % (xs[g], xs[g+1]))

for split in range(300, 430, 5):
    lft = rows[rows[:,0] < split]
    rgt = rows[rows[:,0] > split]
    if len(lft) < 15 or len(rgt) < 15:
        continue
    cl, rl = fit(lft); cr, rr = fit(rgt)
    tot = np.sqrt((rl.var()*len(rl) + rr.var()*len(rr))/(len(rl)+len(rr)))
    print("split %3d  L slope %+.5f (n=%3d rms %.3f)  R slope %+.5f (n=%3d rms %.3f)  joint rms %.3f"
          % (split, cl[0], len(rl), rl.std(), cr[0], len(rr), rr.std(), tot))
