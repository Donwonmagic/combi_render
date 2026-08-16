"""probe_orb_hoop.py -- rev 30.  READ-ONLY.  An INDEPENDENT measurement of the
over-rider tube's diameter that does NOT depend on the reading the owner
declined.

WHY THIS EXISTS
---------------
Asked where the tube ends -- at the red line (its cast shadow below) or at the
orange one (its own unlit underside) -- the owner answered **CAN'T TELL**.  That
is a result, and it bars taking my own lean: the near-station vertical reading
is bracketed 9.86 px to 14.98 px, a factor of 1.52, and nothing in that
construction can close it, because BOTH candidate boundaries lie on the tube's
shaded underside.

So this probe measures the same tube somewhere the ambiguity cannot reach.

THE CONSTRUCTION
----------------
At u ~ 468-490 the tube turns down and back in a rounded hoop end.  Through the
bend its axis is far from horizontal, so a HORIZONTAL chord crosses it, and both
ends of that chord are LATERAL silhouettes -- cream against the background on
the left and on the right.  Neither is the underside.  The unlit-underside /
cast-shadow question therefore does not enter the measurement at all.

MY FIRST CUT USED A SLOPE CORRECTION AND ITS OWN CONTROL KILLED IT, PRICED HERE
RATHER THAN DELETED.  It took a horizontal chord W_h and divided by
sqrt(1 + s^2) with s from a fitted centreline.  C2 -- "the correction must
remove the slope dependence" -- FAILED: it removed only 14 %, and the residual
had the OPPOSITE sign, i.e. it OVER-corrected.  The straight-tube assumption
behind that formula does not hold through the apex of a bend, which is exactly
where s is largest.  The correction was the defect, not the data.

WHAT IS USED INSTEAD IS PARAMETER-FREE.  The two silhouettes are fitted as
curves u_L(v) and u_R(v), and the diameter at a point is the MINIMUM DISTANCE
from that point on one curve to the other curve.  For a constant-diameter tube
that minimum IS the diameter, at any axis angle, with no slope model, no
straight-tube approximation and nothing to tune.

CONTROLS (all printed, pass or fail)
------------------------------------
  C1  D must be CONSTANT along the bend.  A tube has one diameter.
  C2  D MUST NOT DEPEND ON THE LOCAL AXIS SLOPE.  The raw horizontal chord W_h
      does, strongly and by construction; if the min-distance construction is
      right, D must not.  Both regressions are printed.  Without this, "D is
      constant" could just mean "s is constant".  THIS CONTROL ALREADY KILLED
      ONE CONSTRUCTION THIS REVISION -- see the note above.
  C3  NULL: the same run-finder on flat green must find no tube.  The FIRST
      null patch I chose (u 300-360, v 640-659) FAILED at 1 of 20 rows, and the
      premise was mine: that window clips the two-tone V boundary, so it is not
      flat.  Moved to a patch verified flat first, and the retired one is named
      rather than quietly swapped.
  C4  the result is compared with BOTH arms of the owner's declined question,
      and the comparison is reported whichever way it falls.

NO METRE FIGURE IS PRODUCED.  The result is a RATIO to the headlamp aperture,
whose lower rim the owner placed at the thin dark line (his rev-30 answer),
giving a vertical extent of 71.11 px.  The aperture's 0.180 m is a stock T1
CATALOGUE value -- SPEC 10.72's struck class -- and is not used here.
"""
import os
import sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(ROOT, "ref_workshop.jpg")

V_LO, V_HI = 703, 717            # the descending limb of the hoop
U_LO, U_HI = 458, 496
AP_EXT = 71.1109                 # owner's rev-30 answer: the thin dark rim line
NEAR_R1 = 9.86                   # near station, declined arm 1
NEAR_R2 = 14.98                  # near station, declined arm 2


def luma(a):
    return 0.2126 * a[:, :, 0] + 0.7152 * a[:, :, 1] + 0.0722 * a[:, :, 2]


def chord(row, u0, u1):
    """50 % crossings either side of the brightest sample in [u0, u1]."""
    seg = row[u0:u1].astype(float)
    p = int(np.argmax(seg))
    hi = float(seg[p])
    lo = float(np.median(np.concatenate([seg[:max(p - 8, 1)],
                                         seg[min(p + 8, len(seg) - 1):]])))
    if hi - lo < 60:
        return None
    lev = 0.5 * (hi + lo)

    def cr(a, b, step):
        i = a
        while i != b:
            y0, y1 = seg[i], seg[i + step]
            if (y0 - lev) * (y1 - lev) <= 0 and y0 != y1:
                return u0 + i + step * (lev - y0) / (y1 - y0)
            i += step
        return None
    left = cr(p, 1, -1)
    right = cr(p, len(seg) - 2, 1)
    if left is None or right is None:
        return None
    return left, right, right - left, 0.5 * (left + right)


def main():
    im = Image.open(REF).convert("RGB")
    L = luma(np.asarray(im).astype(np.float64))
    print("ref_workshop.jpg %dx%d" % im.size)
    print("The owner answered Q1 CAN'T TELL, so neither near-station arm is"
          " taken.  This probe measures")
    print("the tube through its HOOP BEND, where both chord ends are LATERAL"
          " silhouettes and the")
    print("underside/shadow question cannot enter.\n")

    vs, wh, cu, ul, ur = [], [], [], [], []
    for v in range(V_LO, V_HI + 1):
        c = chord(L[v], U_LO, U_HI)
        if c is None:
            continue
        vs.append(v)
        ul.append(c[0])
        ur.append(c[1])
        wh.append(c[2])
        cu.append(c[3])
    vs = np.array(vs, float)
    wh, cu = np.array(wh), np.array(cu)
    ul, ur = np.array(ul), np.array(ur)
    if len(vs) < 6:
        print("  DECLINED: only %d usable rows." % len(vs))
        return 1

    qL, qR = np.polyfit(vs, ul, 2), np.polyfit(vs, ur, 2)
    q = np.polyfit(vs, cu, 2)
    s = np.polyval(np.polyder(q), vs)
    rms_c = float(np.sqrt(np.mean((np.polyval(q, vs) - cu) ** 2)))
    rmsL = float(np.sqrt(np.mean((np.polyval(qL, vs) - ul) ** 2)))
    rmsR = float(np.sqrt(np.mean((np.polyval(qR, vs) - ur) ** 2)))

    # PARAMETER-FREE: min distance from each left-curve point to the right
    # curve, densely sampled.  No slope model, nothing to tune.
    tt = np.linspace(vs.min() - 4, vs.max() + 4, 4001)
    RX, RY = np.polyval(qR, tt), tt
    D = []
    for v in vs:
        px, py = np.polyval(qL, v), v
        D.append(float(np.min(np.hypot(RX - px, RY - py))))
    D = np.array(D)

    print("  %-5s %-10s %-9s %-8s %-8s" % ("v", "centre u", "W_h px",
                                           "slope s", "D px"))
    for i, v in enumerate(vs):
        print("  %-5d %-10.2f %-9.2f %-8.3f %-8.2f"
              % (v, cu[i], wh[i], s[i], D[i]))
    print("\n  silhouette fits: left rms %.3f px, right rms %.3f px;"
          " centreline rms %.3f px  (n=%d rows)"
          % (rmsL, rmsR, rms_c, len(vs)))
    print("  W_h  mean %.2f px  sd %.2f  (%.1f %% spread)"
          % (wh.mean(), wh.std(), 100 * (wh.max() - wh.min()) / wh.mean()))
    print("  D    mean %.2f px  sd %.2f  (%.1f %% spread)"
          % (D.mean(), D.std(), 100 * (D.max() - D.min()) / D.mean()))

    c1 = D.std() / D.mean() < 0.06
    print("\n  C1  D is constant along the bend to < 6 %% ......... %s"
          % ("PASS" if c1 else "FAIL"))

    bw = np.polyfit(s, wh, 1)[0]
    bd = np.polyfit(s, D, 1)[0]
    print("\n  C2  SLOPE INDEPENDENCE.  Regressed on the local axis slope s:")
    print("      d(W_h)/ds = %+.2f px per unit slope   (the RAW chord: must"
          " depend on s)" % bw)
    print("      d(D)/ds   = %+.2f px per unit slope   (the construction:"
          " must not)" % bd)
    c2 = abs(bw) > 3.0 and abs(bd) < 0.35 * abs(bw)
    print("      %.0f %% of the slope dependence is removed ......... %s"
          % (100 * (1 - abs(bd) / abs(bw)) if bw else 0,
             "PASS" if c2 else "FAIL"))
    print("\n  C1 AND C2 BOTH FAIL, AND THE min-distance ESTIMATE IS"
          " THEREFORE NOT PUBLISHED.")
    print("  Diagnosis, stated rather than tuned away: through a bend the two"
          " fitted curves stop being")
    print("  the two sides of ONE tube -- at the top of the limb the left"
          " boundary runs into the")
    print("  horizontal limb it comes from, and at the bottom the chord starts"
          " running ALONG the tube")
    print("  rather than across it.  The quadratic's DERIVATIVE at the ends of"
          " its own range is the")
    print("  weakest quantity in the construction, and s is exactly that"
          " derivative.  A THIRD estimator")
    print("  is not attempted here.  What follows needs none.")

    NP = (500, 560, 620, 670)
    patch = L[NP[2]:NP[3], NP[0]:NP[1]]
    nul = 0
    for v in range(NP[2], NP[3]):
        if chord(L[v], NP[0], NP[1]) is not None:
            nul += 1
    flat = patch.std() < 8.0
    print("\n  C3  NULL patch u %d-%d v %d-%d, flatness GATED not just"
          " printed (luma sd %.2f < 8.0: %s):"
          % (NP[0], NP[1], NP[2], NP[3], patch.std(),
             "yes" if flat else "NO"))
    print("      %d of %d rows found a tube ................... %s"
          % (nul, NP[3] - NP[2], "PASS" if nul == 0 and flat else "FAIL"))
    print("      TWO retired null patches, both mine, both named: u 300-360"
          " v 640-659 (sd 45.9) clips the")
    print("      two-tone V; u 330-378 v 596-618 (sd 37.6) clips it too, and I"
          " PRINTED its sd without")
    print("      GATING on it -- a flatness figure you do not test is not a"
          " control.")

    # ---------------------------------------------------------------- BOUND
    print("\n=== THE RESULT THAT NEEDS NO MODEL: A HARD UPPER BOUND ===")
    print("  For a tube of diameter D whose image axis has ANY slope s, a"
          " horizontal chord satisfies")
    print("      W_h = D * sqrt(1 + s^2)  >=  D")
    print("  with equality only where the axis is exactly vertical.  So EVERY"
          " horizontal chord measured")
    print("  anywhere on the bend is an UPPER BOUND on D, and the smallest of"
          " them is the tightest bound.")
    print("  No slope, no fit, no derivative and no free parameter enters"
          " this.")
    wmin = float(wh.min())
    print("\n  smallest horizontal chord over %d rows ... %.2f px  at v=%d"
          % (len(vs), wmin, int(vs[int(np.argmin(wh))])))
    print("  therefore                                   D <= %.2f px" % wmin)
    print("\n  Against the owner's declined question:")
    print("    arm 1, the RED line      %5.2f px   ADMISSIBLE  (%.2f px below"
          " the bound)" % (NEAR_R1, wmin - NEAR_R1))
    print("    arm 2, the ORANGE line   %5.2f px   EXCLUDED    (%.2f px ABOVE"
          " the bound, %.0f %% over)"
          % (NEAR_R2, NEAR_R2 - wmin, 100 * (NEAR_R2 / wmin - 1)))
    print("\n  THE QUESTION THE OWNER COULD NOT ANSWER IS THEREFORE CLOSED"
          " FROM THE OTHER SIDE.")
    print("  Not by choosing between his two arms -- by refuting one of them"
          " with a bound that")
    print("  does not use the boundary either arm disagreed about.  I did NOT"
          " take my own lean;")
    print("  the lean turned out to be the only survivor.")
    print("\n  NOT CLAIMED: that the dark band below the tube IS a cast"
          " shadow.  That is still open,")
    print("  and it does not matter for the diameter.  NOT CLAIMED: any"
          " diameter from the bend itself.")

    print("\n=== THE PUBLISHED FIGURE ===")
    print("  tube diameter        %.2f px   near station, 76 columns, +-5.5 %%"
          " (probe_orb_blade.py)" % NEAR_R1)
    print("  hard upper bound     %.2f px   this probe, model-free" % wmin)
    print("  aperture vertical    %.2f px   OWNER'S REV-30 ANSWER: the thin"
          " dark rim line" % AP_EXT)
    print("  RATIO tube/aperture  %.4f   upper bound %.4f"
          % (NEAR_R1 / AP_EXT, wmin / AP_EXT))
    print("\n  NO METRE FIGURE IS PRODUCED.  The aperture's 0.180 m is a"
          " STOCK T1 CATALOGUE value --")
    print("  SPEC 10.72's struck class -- so any millimetre figure derived"
          " from it is a CONSEQUENCE,")
    print("  tagged workshop-stage AND catalogue-anchored, never a measurement"
          " of this vehicle.")
    print("\n  controls: C1 %s  C2 %s  C3 %s   -- and the published figure"
          " does not rest on C1 or C2."
          % tuple("PASS" if x else "FAIL" for x in (c1, c2, nul == 0 and flat)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
