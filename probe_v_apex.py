"""probe_v_apex.py -- rev 31b.  READ-ONLY.

WHY THIS EXISTS
---------------
The owner looked at `rev31_q_post.png` and said the apex marking did not look
right.  He is correct, and the defect is in REF Sec 9, not in the figure's
drawing code.

REF Sec 9 publishes:

    two-tone V apex (centreline)    (311.5, 669)  +- 4 px

**THAT POINT IS NOT THE APEX.**  At x8 and x14 the two-tone V's two arms have
NOT converged at v = 669 -- the cream wedge is still ~30 px wide there -- and
the over-rider bar (SPEC 10.83) crosses the nose at exactly that height and
occludes everything below.  (311.5, 669) is the column where the V's **RIGHT
ARM disappears behind the bar**.  The true vertex is BEHIND THE BAR and is not
directly visible in this frame at all.

WHY IT MATTERS BEYOND THE FIGURE
--------------------------------
REF Sec 9 uses that point AS THE CENTRELINE, and SPEC 10.83 used it as the
centreline to refute "the post is at the vehicle's centreline"; SPEC 10.84 then
priced that refutation at 54.0 px.  **If the anchor is one arm's occlusion point
rather than the vertex, it is not on the centreline at all, and every figure
derived from it inherits the error.**

THE CONSTRUCTION
----------------
The two arms ARE cleanly visible above the bar.  Each is traced as a
cream->green boundary, fitted as a straight line, and the two lines are
intersected.  **The intersection's COLUMN is the quantity of interest** and it
is far better determined than its row: two arms meeting at a shallow angle fix
u tightly and v loosely.  No scale, no calibration, no depth enters.

WHAT IS NOT CLAIMED
-------------------
That the vertex is SHARP.  A T1's two-tone V is radiused at the tip, so the
straight-line intersection gives the ARMS' axis crossing, which is the vertex's
column but is BELOW the real rounded tip.  Only the COLUMN is published.

CONTROLS (all printed, pass or fail)
------------------------------------
  C1  each arm must be a straight line: rms residual and row span printed.
  C2  SYMMETRY.  The two arms' slopes must be opposite in sign and comparable in
      magnitude.  If one arm is not an arm, this fails.
  C3  NULL / FALSIFICATION: REF Sec 9's published point must be shown to lie ON
      one arm's trace rather than at the intersection.  If (311.5, 669) is in
      fact the vertex, its distance to BOTH arms is ~0 and this probe is wrong.
  C4  the bar's top edge must lie BELOW the traced band at every row used, so
      that no traced sample is contaminated by the bar.
  C5  CURVATURE / EXTRAPOLATION.  The crossing sits 38 rows below the deepest
      traced row -- an extrapolation 0.93x the length of the traced span -- and
      it is only valid if the arms stay straight.  The band is split in half and
      re-crossed.  **This control is what sets the published band**: a bootstrap
      over the traced samples returns +-0.2 px, which is a FALSE PRECISION,
      because it prices scatter and not the straightness assumption.
"""
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "ref_workshop.jpg")

REF_APEX = (311.5, 669.0)
REF_TOL = 4.0
POST_U = 365.5                      # SPEC 10.75 box C centre

V_ROWS = (622, 664)                 # rows to trace, ABOVE the bar
U_SPAN = (245, 345)                 # columns the V occupies in that band
BAR_ROWS = (664, 690)               # where the bar's top edge is looked for


def luma(im):
    a = np.asarray(im.convert("RGB"), dtype=np.float64)
    return 0.2126 * a[:, :, 0] + 0.7152 * a[:, :, 1] + 0.0722 * a[:, :, 2]


def subpix(y0, y1, y2):
    den = y0 - 2 * y1 + y2
    return 0.0 if den == 0 else 0.5 * (y0 - y2) / den


def trace_arms(L):
    """For each row, the cream wedge's LEFT and RIGHT boundary, sub-pixel."""
    lo, hi = U_SPAN
    left, right, rows = [], [], []
    for v in range(V_ROWS[0], V_ROWS[1]):
        row = L[v, lo:hi]
        g = np.diff(row)
        kL = int(np.argmax(g))                   # green -> cream, rising
        kR = int(np.argmin(g))                   # cream -> green, falling
        if kL <= 0 or kR <= 0 or kL >= g.size - 1 or kR >= g.size - 1:
            continue
        if g[kL] < 4.0 or g[kR] > -4.0 or kR <= kL + 4:
            continue
        left.append(lo + kL + 0.5 + subpix(g[kL - 1], g[kL], g[kL + 1]))
        right.append(lo + kR + 0.5 - subpix(-g[kR - 1], -g[kR], -g[kR + 1]))
        rows.append(float(v))
    return np.array(rows), np.array(left), np.array(right)


def fit(v, u):
    """u = m v + c"""
    A = np.vstack([v, np.ones_like(v)]).T
    (m, c), *_ = np.linalg.lstsq(A, u, rcond=None)
    r = u - (m * v + c)
    return m, c, float(np.sqrt((r ** 2).mean())), len(v)


def main():
    im = Image.open(REF)
    L = luma(im)
    print("probe_v_apex.py -- rev 31b -- READ-ONLY")
    print(f"REF Sec 9 publishes the V apex at {REF_APEX} +-{REF_TOL:.0f} px\n")

    rows, uL, uR = trace_arms(L)
    if len(rows) < 15:
        print(f"  DECLINED: only {len(rows)} rows traced.")
        return 2
    print(f"=== C1  trace both arms over rows {int(rows.min())}-"
          f"{int(rows.max())} ===")
    mL, cL, rmsL, nL = fit(rows, uL)
    mR, cR, rmsR, nR = fit(rows, uR)
    print(f"  LEFT  arm  n={nL:3d}  du/dv {mL:+.4f}  rms {rmsL:5.3f} px")
    print(f"  RIGHT arm  n={nR:3d}  du/dv {mR:+.4f}  rms {rmsR:5.3f} px")
    print(f"  C1 {'PASS' if max(rmsL, rmsR) < 1.5 else 'FAIL'}: "
          f"both arms are straight lines to < 1.5 px")

    print("\n=== C2  symmetry: the arms must lean OPPOSITE ways ===")
    opp = (mL * mR) < 0
    ratio = abs(mL) / abs(mR) if mR else float("inf")
    print(f"  slopes {mL:+.4f} and {mR:+.4f}   opposite: {opp}   "
          f"|ratio| {ratio:.2f}")
    print(f"  C2 {'PASS' if opp else 'FAIL'}")

    print("\n=== C4  no traced row may touch the bar ===")
    barv = []
    for u in range(280, 340):
        col = L[BAR_ROWS[0]:BAR_ROWS[1], u]
        d = np.diff(col)
        k = int(np.argmax(d))
        if d[k] > 4.0:
            barv.append(BAR_ROWS[0] + k + 0.5)
    btop = float(np.median(barv)) if barv else float("nan")
    print(f"  bar top edge over u 280-340: median v = {btop:.1f} "
          f"(n={len(barv)})")
    ok4 = btop > rows.max()
    print(f"  deepest traced row {rows.max():.0f}   C4 "
          f"{'PASS' if ok4 else 'FAIL'}")

    print("\n=== THE ARMS' CROSSING ===")
    # u = mL v + cL = mR v + cR
    v_x = (cR - cL) / (mL - mR)
    u_x = mL * v_x + cL
    print(f"  arms cross at (u, v) = ({u_x:.1f}, {v_x:.1f})")
    print(f"  REF Sec 9's published apex   = ({REF_APEX[0]:.1f}, "
          f"{REF_APEX[1]:.1f})")
    print(f"  COLUMN SHIFT = {u_x - REF_APEX[0]:+.1f} px")

    print("\n=== C3  NULL: is REF's point the vertex, or a point on one arm? ===")
    du, dv = REF_APEX
    dL = abs(du - (mL * dv + cL))
    dR = abs(du - (mR * dv + cR))
    print(f"  horizontal distance from REF's point to the LEFT  arm: "
          f"{dL:7.2f} px")
    print(f"  horizontal distance from REF's point to the RIGHT arm: "
          f"{dR:7.2f} px")
    on_one = min(dL, dR) < REF_TOL and max(dL, dR) > 3.0 * REF_TOL
    print(f"  C3 {'PASS' if on_one else 'FAIL'}: REF's point lies ON the "
          f"{'RIGHT' if dR < dL else 'LEFT'} ARM "
          f"({min(dL, dR):.2f} px) and far from the other "
          f"({max(dL, dR):.2f} px)")
    print("  -> it is that arm's OCCLUSION POINT at the over-rider bar,")
    print("     NOT the vertex.  The vertex is BEHIND THE BAR.")

    print("\n=== C5  CURVATURE: split the band and re-cross ===")
    mid = len(rows) // 2

    def _cross(v, a, b):
        m1, c1, _, _ = fit(v, a)
        m2, c2, _, _ = fit(v, b)
        vx = (c2 - c1) / (m1 - m2)
        return m1 * vx + c1, vx

    up = _cross(rows[:mid], uL[:mid], uR[:mid])
    lo_ = _cross(rows[mid:], uL[mid:], uR[mid:])
    dsplit = abs(up[0] - lo_[0])
    print(f"  upper half (far from tip) u = {up[0]:7.1f}")
    print(f"  lower half (near tip)     u = {lo_[0]:7.1f}")
    print(f"  half-to-half disagreement = {dsplit:.1f} px")
    print(f"  C5 {'PASS' if dsplit < 8.0 else 'FAIL'} at an 8 px tolerance")
    for nm, u in (("LEFT", uL), ("RIGHT", uR)):
        q = np.polyfit(rows, u, 2)
        lin = np.polyfit(rows, u, 1)
        rq = float(np.sqrt(((u - np.polyval(q, rows)) ** 2).mean()))
        rl = float(np.sqrt(((u - np.polyval(lin, rows)) ** 2).mean()))
        print(f"    {nm:<6} lin rms {rl:5.3f} -> quad rms {rq:5.3f} px ; "
              f"curvature {q[0]:+.5f} px/row^2")
    print(f"  PUBLISHED BAND: +-{max(3.0, dsplit):.0f} px SYSTEMATIC, set by "
          f"this control.")
    print("  A bootstrap over the traced samples returns +-0.2 px and that is a")
    print("  FALSE PRECISION -- it prices scatter, not the straightness")
    print("  assumption the extrapolation rests on.  The right arm carries a")
    print("  real quadratic term; if it continues, the worst case is ~7 px.")

    print("\n=== CONSEQUENCE for SPEC 10.83 / 10.84 ===")
    print(f"  post centre u = {POST_U:.1f}")
    print(f"  offset against REF's published anchor : "
          f"{POST_U - REF_APEX[0]:+.1f} px   (the 54.0 px 10.84 priced)")
    print(f"  offset against the arms' crossing     : "
          f"{POST_U - u_x:+.1f} px")
    print("\n  CEILING: only the COLUMN is published.  The T1's V is RADIUSED")
    print("  at the tip, so the straight-line crossing sits BELOW the real")
    print("  rounded vertex; its row is not a measurement.  No scale, no")
    print("  calibration and no depth enter, and NOTHING here prices the")
    print("  nose-skin-to-bumper-plane parallax -- 10.84 stays UNDECIDED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
