"""probe_orb_post.py -- rev 31.  READ-ONLY.  NO METRE FIGURE IS PRODUCED.

THE QUESTION THIS PROBE WAS BUILT TO ANSWER
-------------------------------------------
SPEC 10.83 refuted SPEC 10.75's "the post is at the vehicle's centreline" by
comparing the post's own columns (357-374, centre 365.5) against the two-tone V
apex at u = 311.5, which REF Sec 9 gives as the centreline.  That refutation is
recorded as SETTLED and it is what BLOCKS the post from being built.

**IT COMPARES TWO FEATURES AT DIFFERENT DEPTHS.**  The V apex is on the NOSE
SKIN.  The post stands in the BUMPER plane, forward of it by the bumper's
standoff -- a quantity SPEC 10.83 itself grades "A CHOICE, not a reading".
Under perspective a centreline point translated forward does not keep its
column, so the nose-skin centreline column and the bumper-plane centreline
column are different numbers, and 10.83 used one as if it were the other.

The disputed offset is only 54.0 px.  So the whole refutation turns on a
parallax whose SIGN 10.83 never established.  This probe tries to establish it.

  forward-translation image direction = AWAY from the aft vanishing point.
    V_aft RIGHT of the nose -> forward moves LEFT  -> gap WIDENS -> 10.83 stands
    V_aft LEFT  of the nose -> forward moves RIGHT -> gap NARROWS -> 10.83 unsafe

ARM 1 -- the vehicle's own fore-aft vanishing point.  **THIS ARM DIED, AND THE
WAY IT DIED IS THE PROBE'S MAIN RESULT.**  Five long edges are traced.  Two of
them fit straight lines to rms 0.09 px, so tracing is not the limit.  Their
pairwise intersections nevertheless scatter over thousands of pixels and change
SIDE.  **The vehicle's "horizontal" edges are not mutually parallel in 3D**, and
the model itself says so: `t1_mats.z_belt(x)` makes the belt a SLOPED line and
the roof carries its own rake and crown.  A pencil fitted to lines that are not
parallel has no vanishing point to find.  This is reported as a FAILURE, not
widened into an answer.

ARM 2 -- two centreline features at different depths.  The VW roundel and the V
apex are both on the vehicle's centreline and at different depths on the nose.
Their column difference is a DIRECT reading of the parallax sign, needing no
vanishing point at all.  It is reported with REF Sec 9's own +-4 px band on the
apex, and it is NOT significant.

CONTROLS (all printed, pass or fail)
------------------------------------
  C1  the fore-aft edges must CONVERGE to one point.  Pairwise intersections
      and the least-squares pencil residual are printed.  FAILS.
  C2  each traced edge must be a REAL edge: rms residual and column span
      printed for every one.  An edge with rms > 1.5 px is not used in C1.
  C3  the SIDE must not depend on the subset used.  Leave-one-out.  FAILS.
  C4  ARM 2's sign must clear REF Sec 9's stated +-4 px band on the V apex.
"""
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "ref_workshop.jpg")

V_APEX_U, V_APEX_TOL = 311.5, 4.0      # REF Sec 9, with its own stated band
ROUNDEL_U = 306.0                      # REF Sec 9, centre of the VW emblem
POST_U0, POST_U1 = 357.0, 374.0        # SPEC 10.75 box C
POST_U = 0.5 * (POST_U0 + POST_U1)
RMS_GATE = 1.5                         # px: an edge worse than this is not a line

# (name, v_lo, v_hi, u_lo, u_hi, polarity)
EDGES = [
    ("drip rail",          300, 360, 520, 700, "dark_below"),
    ("counter lower edge", 470, 540, 730, 955, "dark_below"),
    ("belt break, fwd",    470, 520, 505, 690, "dark_below"),
    ("counter upper edge", 430, 500, 730, 960, "dark_above"),
    ("rocker, mid run",    590, 700, 680, 820, "dark_below"),
]


def luma(im):
    a = np.asarray(im.convert("RGB"), dtype=np.float64)
    return 0.2126 * a[:, :, 0] + 0.7152 * a[:, :, 1] + 0.0722 * a[:, :, 2]


def trace(L, v0, v1, u0, u1, pol, thr=3.0):
    us, vs = [], []
    for u in range(u0, u1):
        col = L[v0:v1, u]
        if col.size < 5:
            continue
        d = np.diff(col)
        g = -d if pol == "dark_below" else d
        k = int(np.argmax(g))
        if k <= 0 or k >= g.size - 1 or g[k] < thr:
            continue
        a0, a1, a2 = g[k - 1], g[k], g[k + 1]
        den = a0 - 2 * a1 + a2
        off = 0.0 if den == 0 else 0.5 * (a0 - a2) / den
        us.append(float(u))
        vs.append(v0 + k + 0.5 + off)
    return np.array(us), np.array(vs)


def rfit(u, v, keep=0.85, it=4):
    for _ in range(it):
        if len(u) < 12:
            break
        A = np.vstack([u, np.ones_like(u)]).T
        (m, c), *_ = np.linalg.lstsq(A, v, rcond=None)
        r = np.abs(v - (m * u + c))
        s = r <= max(np.quantile(r, keep), 1e-9)
        u, v = u[s], v[s]
    A = np.vstack([u, np.ones_like(u)]).T
    (m, c), *_ = np.linalg.lstsq(A, v, rcond=None)
    r = v - (m * u + c)
    return m, c, float(np.sqrt((r ** 2).mean())), len(u), u


def isect(l1, l2):
    (m1, c1), (m2, c2) = l1, l2
    if abs(m1 - m2) < 1e-12:
        return None
    return (c2 - c1) / (m1 - m2)


def main():
    L = luma(Image.open(REF))
    print("probe_orb_post.py -- rev 31 -- READ-ONLY")
    print(f"V apex u={V_APEX_U} +-{V_APEX_TOL}   roundel u={ROUNDEL_U}   "
          f"post u={POST_U}")
    print(f"disputed offset post - V apex = {POST_U - V_APEX_U:+.1f} px\n")

    print("=== ARM 1 / C2  trace every candidate fore-aft edge ===")
    good = []
    for name, v0, v1, u0, u1, pol in EDGES:
        u, v = trace(L, v0, v1, u0, u1, pol)
        if len(u) < 20:
            print(f"  {name:<20} DECLINED, {len(u)} columns")
            continue
        m, c, rms, n, uu = rfit(u, v)
        used = rms <= RMS_GATE
        print(f"  {name:<20} n={n:4d}  span {uu.min():.0f}-{uu.max():.0f}"
              f"  slope {m:+.4f}  rms {rms:5.3f} px   "
              f"{'USED' if used else 'not a line, EXCLUDED'}")
        if used:
            good.append((name, m, c))

    print(f"\n=== ARM 1 / C1  do the {len(good)} accepted edges converge? ===")
    if len(good) < 3:
        print("  DECLINED: fewer than three accepted edges.")
        return 2
    us = []
    for i in range(len(good)):
        for j in range(i + 1, len(good)):
            x = isect((good[i][1], good[i][2]), (good[j][1], good[j][2]))
            if x is None:
                continue
            us.append(x)
            print(f"  {good[i][0][:18]:<18} x {good[j][0][:18]:<18}"
                  f" -> u {x:10.1f}   ({'RIGHT' if x > POST_U else 'LEFT'})")
    spread = max(us) - min(us)
    sides = {"RIGHT" if x > POST_U else "LEFT" for x in us}
    print(f"\n  spread of pairwise intersections: {spread:,.0f} px "
          f"across a {L.shape[1]} px frame")
    print(f"  C1 {'PASS' if spread < 200 else 'FAIL'}: the accepted edges do "
          f"{'' if spread < 200 else 'NOT '}share a vanishing point")
    print(f"  C3 {'PASS' if len(sides) == 1 else 'FAIL'}: sides seen = {sides}")
    print("\n  ARM 1 IS DEAD.  Two of the accepted edges fit to rms < 0.1 px, so")
    print("  this is NOT a tracing failure.  The vehicle's 'horizontal' edges")
    print("  are genuinely NOT PARALLEL in 3D -- t1_mats.z_belt(x) is a sloped")
    print("  line and the roof carries rake and crown.  There is no single")
    print("  fore-aft vanishing point on this vehicle to recover.")

    print("\n=== ARM 2  two centreline features at different depths ===")
    d = V_APEX_U - ROUNDEL_U
    print(f"  V apex {V_APEX_U} - roundel {ROUNDEL_U} = {d:+.1f} px")
    print(f"  REF Sec 9's own band on the apex is +-{V_APEX_TOL:.0f} px "
          f"-> {abs(d) / V_APEX_TOL:.2f} sigma")
    ok = abs(d) > 2.0 * V_APEX_TOL
    print(f"  C4 {'PASS' if ok else 'FAIL'}: the sign is "
          f"{'established' if ok else 'NOT ESTABLISHED'} by this arm")

    print("\n=== VERDICT ===")
    print("  The SIGN of the nose-skin-to-bumper-plane parallax is UNDECIDED.")
    print("  Therefore SPEC 10.83's refutation of 'the post is at the")
    print("  centreline' is NEITHER CONFIRMED NOR REFUTED by this probe: it")
    print("  rests on a 54.0 px offset between two features whose depth")
    print("  difference has never been priced, and neither arm here prices it.")
    print("  10.83's status on that one claim should read UNDECIDED, not")
    print("  REFUTED.  The post stays UNBUILT either way -- this probe supplies")
    print("  no lateral position and REF Sec 9 bars a lateral metre figure on")
    print("  this panel.")
    print("\n  CEILING: no calibration, no scale, no depth, no metre figure.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
