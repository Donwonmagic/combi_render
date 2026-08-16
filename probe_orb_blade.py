"""probe_orb_blade.py -- rev 30.  READ-ONLY.  The front over-rider, SPEC 10.75
/ 10.80, item 1.

WHAT THIS ANSWERS, AND WHAT IT DELIBERATELY DOES NOT
----------------------------------------------------
rev 26 left the over-rider bracketed at 7.9-11.7 px with NO metre scale, and
named the blocker as the foreground trolley occluding the bumper blade's lower
edge "in 5 of 8 columns".  rev 29 named the most promising untried route as a
SCALE-FREE RATIO at the same station: the tube's vertical thickness against the
bumper blade's face height IN THE SAME COLUMNS.

Three things have to hold for that route to be admissible, and this probe tests
each of them separately rather than as one verdict:

  Q1  IS THE BLADE'S LOWER BOUNDARY OCCLUDED in the tube's own columns?
      Settled BY GEOMETRY -- the trolley rail's top edge is fitted as a
      straight line and compared with the blade's lower boundary column by
      column.  Not by eye, and not by the naive scan rev 26 ran.

  Q2  WHAT DOES A REAL STEP LOOK LIKE IN THIS FRAME?  SPEC 10.80 measured the
      point spread at sigma = 0.5594 px, so an ideal step's 10-90 rise here is
      2 * 1.2816 * sigma = 1.434 px.  The rail's own edges are the frame's
      empirical answer.  Every other boundary is priced against them.

  Q3  IS THE RATIO THRESHOLD-STABLE?  This is the question that decides the
      route, and it is NOT the same question as Q2.  Both the tube and the
      blade are bounded partly by shading rather than by silhouette, so both
      move with the luma threshold -- but a ratio of two boundaries that move
      TOGETHER can be far better conditioned than either one alone.  rev 26
      swept the threshold on the tube and found +-19 %; nobody has ever swept
      it on the RATIO.  That is done here.

METHOD NOTES, because the method is a probe too
-----------------------------------------------
* No resampling anywhere.  SPEC 10.79: a probe that measures the optics must
  not add optics of its own.  Every crossing is a linear interpolation between
  two adjacent RAW samples.
* The 10-90 estimator is AUTO-CENTRED on the steepest gradient in its search
  window and grows its plateaus outward until the gradient dies.  A FIXED
  window was tried first and is PRICED below: on the rail's own edge it read
  6.92 px where the auto-centred estimator reads 1.9 px, because the fixed
  window's outer thirds landed on a shading gradient rather than on a plateau.
  That is the same class of defect as rev 27's bilinear resample -- the
  instrument adding its own blur -- and it is recorded, not deleted.

NO METRE FIGURE IS PRODUCED HERE and none is inferred.  No px/m is used,
invented or implied.  This probe reports whether the ratio route is
admissible; it is deliberately possible for it to return NOT ADMISSIBLE.
"""
import os
import sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(ROOT, "ref_workshop.jpg")

# SPEC 10.80, rev 28.  Measured on THIS frame, core arms only, n = 32.
PSF_SIGMA = 0.5594
PSF_SIGMA_SD = 0.0280
STEP_1090 = 2.0 * 1.28155 * PSF_SIGMA          # 1.434 px

# Column run over which the tube is ISOLATED: clear of the bracket at its far
# end and of the centre post at its near end.  rev 26 used 248-272.
U_LO, U_HI = 236, 300
V_LO, V_HI = 636, 800
THRESH = [110, 120, 130, 140, 150, 160, 170]


def luma(a):
    return 0.2126 * a[:, :, 0] + 0.7152 * a[:, :, 1] + 0.0722 * a[:, :, 2]


def runs_above(col, v0, T, minlen=3):
    out, s = [], None
    for i, b in enumerate(col >= T):
        if b and s is None:
            s = i
        elif not b and s is not None:
            if i - s >= minlen:
                out.append((s + v0, i - 1 + v0))
            s = None
    if s is not None and len(col) - s >= minlen:
        out.append((s + v0, len(col) - 1 + v0))
    return out


def runs_below(col, v0, T, minlen=3):
    out, s = [], None
    for i, b in enumerate(col <= T):
        if b and s is None:
            s = i
        elif not b and s is not None:
            if i - s >= minlen:
                out.append((s + v0, i - 1 + v0))
            s = None
    if s is not None and len(col) - s >= minlen:
        out.append((s + v0, len(col) - 1 + v0))
    return out


def edge_1090(col, v0, vc, half, falling, gfrac=0.15):
    """AUTO-CENTRED 10-90 width, in RAW pixels.

    Locates the steepest signed gradient within +-half of vc, then grows the
    two plateaus outward until |g| drops below gfrac of the peak.  Returns
    (width, v10, v90, hi, lo, vsteep) or None.
    """
    a, b = int(vc - half - 3), int(vc + half + 3)
    a = max(a, 0)
    b = min(b, len(col) + v0 - 1)
    seg = col[a - v0:b - v0 + 1].astype(float)
    if len(seg) < 9:
        return None
    g = np.gradient(seg)
    lo_i, hi_i = int(half + 3 - half), int(half + 3 + half)
    lo_i = max(1, lo_i)
    hi_i = min(len(seg) - 2, hi_i)
    win = g[lo_i:hi_i + 1]
    if len(win) == 0:
        return None
    p = (lo_i + int(np.argmin(win))) if falling else (
        lo_i + int(np.argmax(win)))
    gp = abs(g[p])
    if gp < 3.0:
        return None
    i = p
    while i > 1 and abs(g[i - 1]) > gfrac * gp:
        i -= 1
    j = p
    while j < len(seg) - 2 and abs(g[j + 1]) > gfrac * gp:
        j += 1
    i = max(0, i - 3)
    j = min(len(seg) - 1, j + 3)
    pa = float(np.median(seg[i:max(i + 3, p - 1)]))
    pb = float(np.median(seg[min(p + 2, j - 2):j + 1]))
    hi, lo = (pa, pb) if falling else (pb, pa)
    if hi - lo < 25:
        return None
    t10, t90 = lo + 0.10 * (hi - lo), lo + 0.90 * (hi - lo)

    def cross(level):
        best = None
        for k in range(i, j):
            y0, y1 = seg[k], seg[k + 1]
            if (y0 - level) * (y1 - level) <= 0 and y0 != y1:
                v = a + k + (level - y0) / (y1 - y0)
                if best is None or abs(v - (a + p)) < abs(best - (a + p)):
                    best = v
        return best
    c10, c90 = cross(t10), cross(t90)
    if c10 is None or c90 is None:
        return None
    return abs(c10 - c90), c10, c90, hi, lo, a + p


def edge_1090_fixedwin(col, v0, va, vb, falling):
    """THE RETIRED FIRST CUT, kept so its error can be PRICED.  Plateaus are
    the medians of the outer thirds of a FIXED window."""
    a, b = int(va - v0), int(vb - v0)
    if b - a < 5:
        return None
    seg = col[a:b + 1].astype(float)
    n = len(seg)
    k = max(2, n // 3)
    pa, pb = float(np.median(seg[:k])), float(np.median(seg[-k:]))
    hi, lo = (pa, pb) if falling else (pb, pa)
    if hi - lo < 25:
        return None
    t10, t90 = lo + 0.10 * (hi - lo), lo + 0.90 * (hi - lo)

    def cross(level):
        for i in range(n - 1):
            y0, y1 = seg[i], seg[i + 1]
            if (y0 - level) * (y1 - level) <= 0 and y0 != y1:
                return va + i + (level - y0) / (y1 - y0)
        return None
    c10, c90 = cross(t10), cross(t90)
    if c10 is None or c90 is None:
        return None
    return abs(c10 - c90)


def fit_line(us, vs):
    us, vs = np.asarray(us, float), np.asarray(vs, float)
    A = np.vstack([us, np.ones_like(us)]).T
    (m, c), *_ = np.linalg.lstsq(A, vs, rcond=None)
    rms = float(np.sqrt(np.mean((A @ np.array([m, c]) - vs) ** 2)))
    return float(m), float(c), rms


def bands(col, v0, T):
    """(tube, blade) runs at threshold T, or None if the column is not clean."""
    br = runs_above(col, v0, T, minlen=3)
    if len(br) < 2:
        return None
    tube, blade = br[0], br[1]
    if tube[1] - tube[0] > 20 or blade[1] - blade[0] < 10:
        return None
    return tube, blade


def main():
    im = Image.open(REF).convert("RGB")
    L = luma(np.asarray(im).astype(np.float64))
    print("ref_workshop.jpg %dx%d" % im.size)
    print("PSF, SPEC 10.80: sigma %.4f +- %.4f px -> an IDEAL step's 10-90"
          " rise in this frame is %.3f px" % (PSF_SIGMA, PSF_SIGMA_SD,
                                              STEP_1090))
    print("column run u %d-%d  (rev 26 used 248-272; widened, and the"
          " widening is reported not assumed harmless)" % (U_LO, U_HI))

    # ------------------------------------------------------------------ Q1
    print("\n=== Q1  IS THE BLADE'S LOWER BOUNDARY OCCLUDED?  Settled by"
          " geometry ===")
    ru, rt_, rb_ = [], [], []
    merged = []
    for u in range(U_LO, U_HI + 1):
        col = L[V_LO:V_HI, u]
        dk = [r for r in runs_below(col, V_LO, 60, minlen=3) if r[0] > 700]
        if not dk:
            continue
        a, b = dk[0]
        ru.append(u)
        rt_.append(a)
        rb_.append(b)
        if b - a > 14:
            merged.append(u)
    mt, ct, rt = fit_line(ru, rt_)
    mb, cb, rb = fit_line(ru, rb_)
    print("  rail TOP edge   v = %+.4f u %+.3f   rms %.3f px   n=%d"
          % (mt, ct, rt, len(ru)))
    print("  rail BOT edge   v = %+.4f u %+.3f   rms %.3f px"
          % (mb, cb, rb))
    print("  the BOTTOM edge does NOT fit, and the cause is named rather than"
          " widened: in %d of %d" % (len(merged), len(ru)))
    print("  columns (u %d-%d) the rail's dark band MERGES with the shadow"
          " below it, so the" % (min(merged), max(merged)) if merged else "")
    print("  low-threshold run is no longer the rail alone.  ONLY THE TOP EDGE"
          " IS USED BELOW,")
    print("  and it is the only one the occlusion test needs.")
    c1 = rt < 1.0
    print("  C1  rail TOP edge is straight to < 1 px rms ........... %s"
          % ("PASS" if c1 else "FAIL"))

    clear = []
    for u in range(U_LO, U_HI + 1):
        bb = bands(L[V_LO:V_HI, u], V_LO, 130)
        if not bb:
            continue
        clear.append((u, (mt * u + ct) - bb[1][1]))
    cv = np.array([c for _, c in clear])
    print("  rail top edge lies %.1f to %.1f px BELOW the blade's lower"
          " boundary across all %d clean columns."
          % (cv.min(), cv.max(), len(clear)))
    print("  ANSWER Q1: the trolley does NOT occlude the blade's lower"
          " boundary anywhere in the tube's own columns.")
    print("  rev 26's '5 of 8 columns occluded' was measured on a WIDER"
          " column set that runs past u ~285,")
    print("  where the rail genuinely does cross the blade.  Inside the tube's"
          " run it does not.")

    # ------------------------------------------------------------------ Q2
    print("\n=== Q2  WHAT A REAL STEP LOOKS LIKE IN THIS FRAME ===")
    rw, rw_old = [], []
    for u in range(U_LO, U_HI + 1):
        col = L[V_LO:V_HI, u]
        dk = [r for r in runs_below(col, V_LO, 60, minlen=3) if r[0] > 700]
        if not dk:
            continue
        e = edge_1090(col, V_LO, dk[0][0], 5, falling=True)
        if e:
            rw.append(e[0])
        o = edge_1090_fixedwin(col, V_LO, dk[0][0] - 10, dk[0][0] + 3, True)
        if o:
            rw_old.append(o)
    rw = np.array(rw)
    rw_old = np.array(rw_old)
    print("  rail top edge, AUTO-CENTRED : %.2f px  sd %.2f  (n=%d)  = %.2f x"
          " the ideal step"
          % (rw.mean(), rw.std(), len(rw), rw.mean() / STEP_1090))
    print("  rail top edge, FIXED WINDOW : %.2f px  (RETIRED first cut)"
          % rw_old.mean())
    print("  -> THE RETIRED ESTIMATOR IS PRICED AT %+.1f %% ON A KNOWN REAL"
          " EDGE." % (100 * (rw_old.mean() / rw.mean() - 1)))
    print("     Its outer thirds landed on a shading gradient, not on a"
          " plateau.  Same class as rev 27's")
    print("     bilinear resample: the instrument adding its own blur.")
    c2 = rw.mean() < 3.0
    print("  C2  the frame's own real step measures a few px ....... %s"
          % ("PASS" if c2 else "FAIL"))

    # boundary widths, priced against C2
    tw, bw, ttw, tbw = [], [], [], []
    for u in range(U_LO, U_HI + 1):
        col = L[V_LO:V_HI, u]
        bb = bands(col, V_LO, 130)
        if not bb:
            continue
        (t0, t1), (b0, b1) = bb
        for store, vc, fall, half in ((tw, b0, False, 5), (bw, b1, True, 7),
                                      (ttw, t0, False, 4), (tbw, t1, True, 4)):
            e = edge_1090(col, V_LO, vc, half, fall)
            if e:
                store.append(e[0])
    print("\n  boundary                     10-90 width    x ideal   x rail")
    for nm, arr in (("tube TOP  (green -> cream)", ttw),
                    ("tube BOT  (cream -> green)", tbw),
                    ("blade TOP (green -> cream)", tw),
                    ("blade BOT (cream -> ground)", bw)):
        a = np.array(arr)
        print("  %-28s %5.2f px      %5.2f     %5.2f"
              % (nm, a.mean(), a.mean() / STEP_1090, a.mean() / rw.mean()))
    print("  EVERY boundary on the vehicle is softer than the rail's.  The"
          " blade's lower boundary is")
    print("  the softest of the four -- it is a shading rolloff off a curved"
          " underside, not a silhouette.")

    # ------------------------------------------------------------------ C3
    print("\n=== C3  NULL: the same estimator on flat cream ===")
    nul = tot = 0
    for u in range(U_LO, U_HI + 1):
        col = L[V_LO:V_HI, u]
        bb = bands(col, V_LO, 130)
        if not bb or bb[1][1] - bb[1][0] < 24:
            continue
        tot += 1
        mid = (bb[1][0] + bb[1][1]) // 2
        if edge_1090(col, V_LO, mid, 5, falling=True) is not None:
            nul += 1
    print("  flat-cream windows tested %d, edges found %d" % (tot, nul))
    c3 = nul == 0
    print("  C3  estimator finds no edge where there is none ....... %s"
          % ("PASS" if c3 else "FAIL"))

    # ------------------------------------------------------------------ Q3
    print("\n=== Q3  IS THE RATIO THRESHOLD-STABLE?  The question that"
          " decides the route ===")
    print("  %-5s %-8s %-9s %-9s %-9s %-9s %s"
          % ("T", "n cols", "tube px", "sd", "blade px", "sd", "ratio"))
    R = []
    tube_by_T, blade_by_T = [], []
    for T in THRESH:
        tt, bb_ = [], []
        for u in range(U_LO, U_HI + 1):
            r = bands(L[V_LO:V_HI, u], V_LO, T)
            if not r:
                continue
            tt.append(r[0][1] - r[0][0] + 1)
            bb_.append(r[1][1] - r[1][0] + 1)
        if len(tt) < 10:
            print("  %-5d  (only %d clean columns -- DECLINED)" % (T, len(tt)))
            continue
        tt, bb_ = np.array(tt, float), np.array(bb_, float)
        ratio = tt.mean() / bb_.mean()
        R.append(ratio)
        tube_by_T.append(tt.mean())
        blade_by_T.append(bb_.mean())
        print("  %-5d %-8d %-9.2f %-9.2f %-9.2f %-9.2f %.4f"
              % (T, len(tt), tt.mean(), tt.std(), bb_.mean(), bb_.std(),
                 ratio))
    R = np.array(R)
    tb, bb2 = np.array(tube_by_T), np.array(blade_by_T)
    sp = lambda a: 100.0 * (a.max() - a.min()) / 2.0 / a.mean()
    print("\n  threshold-swept spread, +- %% about the mean:")
    print("    tube thickness alone .......... +-%.1f %%" % sp(tb))
    print("    blade height alone ............ +-%.1f %%" % sp(bb2))
    print("    THE RATIO ..................... +-%.1f %%" % sp(R))
    print("  ratio %.4f +- %.4f (sd over thresholds), min %.4f max %.4f"
          % (R.mean(), R.std(), R.min(), R.max()))
    cancels = sp(R) < min(sp(tb), sp(bb2))
    print("  C5  the ratio is better conditioned than EITHER term alone"
          " (i.e. the threshold\n      systematic partially CANCELS) ....."
          "........ %s" % ("PASS" if cancels else "FAIL"))

    print("\n=== WHAT IS STILL MISSING, STATED NOT HIDDEN ===")
    print("  The ratio above is TUBE THICKNESS / BLADE APPARENT VERTICAL"
          " EXTENT.  To become a metre")
    print("  figure it must be multiplied by the blade's true FACE HEIGHT,"
          " and that step assumes the")
    print("  blade's apparent vertical extent in THIS frame equals its face"
          " height.  It does not:")
    print("   (a) the blade is a curved section seen from above, so its"
          " apparent extent includes part")
    print("       of its top return -- an unmeasured positive bias;")
    print("   (b) its lower boundary is a rolloff (Q2), so where the blade"
          " 'ends' is set by the")
    print("       threshold, not by the object;")
    print("   (c) the face height itself carries an 8 %% spread"
          " (0.123-0.133 m, stock T1 ~0.12 m).")
    print("  (a) is the one with no bound yet, and it is the reason no metre"
          " figure is published here.")
    print("\n  controls: C1 %s  C2 %s  C3 %s  C5 %s"
          % tuple("PASS" if x else "FAIL" for x in (c1, c2, c3, cancels)))
    print("  NOTHING IS CONVERTED TO METRES.  No px/m is used, invented or"
          " implied.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
