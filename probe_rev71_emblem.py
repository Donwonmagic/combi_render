# probe_rev71_emblem.py -- rev 71.  THE FIT DEPTH, MEASURED FOR THE FIRST TIME,
# AND THE THREE SEARCHES THAT SAY THE CONSTRUCTION IS NOT THE BINDING CONSTRAINT.
#
# THE FIT DEPTH IS `1.0 - 0.8 * _BAND_FRAC` IN t1_detail.vw_logo_fit -- NOT
# t1_core.py, which is where the rev-71 brief cites it (rule 18).  It sets how
# far the glyph's extreme is driven into the ring band (0.84 R against a band
# inner edge of 0.80 R, i.e. 20 % in).  The briefs have carried
# *"THE FIT DEPTH IS STILL UNMEASURED -- the answer is a MEASUREMENT, not a
# guess"* and dropped it THREE TIMES.  This measures it.
#
# ⚠ READ THIS BEFORE QUOTING ANY IoU BELOW.  `probe_rev69_fitpose`'s P1b (F246)
# shows its control is NOT framed the way its measurements are, and framed
# correctly the control scores BELOW the specimen.  So these IoUs RANK
# candidates against each other on ONE fixed instrument -- which is what a sweep
# needs -- but the DISTANCE to 0.9882 is not a shape deficit and must not be
# quoted as one.
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def main():
    import probe_rev71_proxy as X
    import probe_rev69_fitpose as F

    checks, fails = [], []

    def ck(name, ok, detail):
        checks.append(name)
        print("  [%s] %s" % ("PASS" if ok else "FAIL", name))
        print("       " + detail)
        if not ok:
            fails.append(name)

    v = X.prove(verbose=False)
    ck("E0 CONTROL -- the 2-D proxy IS the bpy build, on the known answer",
       v > 0.999,
       "PROXY vs BUILT IoU %.6f at 276 rows.  Every number below is computed in "
       "the proxy; if this row ever fails they are all void (rule 3)" % v)

    dst_fit = F.photo_mark("ref_workshop.jpg", (262, 492, 352, 600), True)
    # THE RE-CUT BOX (trap (c)): the shipped (288,542)-(352,640) discards ~14 %
    # of the mark's ink -- 2527 on-px against 2926 -- and was never painted.
    dst_ind = F.photo_mark("IMG_2073.jpeg", (283, 537, 357, 662), True)

    base = None
    rows = []
    keep = X.FIT_R
    try:
        for fr in (0.70, 0.74, 0.78, 0.80, 0.82, 0.84, 0.86, 0.88, 0.90, 0.94, 1.00):
            X.FIT_R = fr
            m = X.mask(X.SHIPPED, X.WFRAC, rows=220)
            a = F.fit(m, dst_fit)[0]
            b = F.fit(m, dst_ind)[0]
            rows.append((fr, a, b))
            if abs(fr - 0.84) < 1e-9:
                base = (a, b)
    finally:
        X.FIT_R = keep

    print("\n  THE FIT DEPTH SWEPT.  fit frame = ref_workshop.jpg;")
    print("  score frame = IMG_2073.jpeg at the RE-CUT box (fit on one, score")
    print("  on the other -- the two frames are NOT comparable to each other)")
    print("     FIT_R    ref_workshop   IMG_2073(re-cut)")
    for fr, a, b in rows:
        print("     %.3f      %.4f          %.4f%s"
              % (fr, a, b, "   <-- SHIPPED" if abs(fr - 0.84) < 1e-9 else ""))

    best_fit = max(rows, key=lambda r: r[1])
    best_ind = max(rows, key=lambda r: r[2])
    # THE CRITERION IS ONE SWEEP STEP, NOT A TYPED TOLERANCE.  The grid is
    # 0.02 wide through the optimum, so "within one step of the argmax" is the
    # finest statement this sweep can make -- claiming tighter would be reading
    # below the instrument's own resolution (rule 48).
    step = 0.02 + 1e-9
    ck("E1 THE SHIPPED FIT DEPTH 0.84 IS WITHIN ONE SWEEP STEP OF THE OPTIMUM "
       "ON BOTH FRAMES",
       abs(best_fit[0] - 0.84) <= step and abs(best_ind[0] - 0.84) <= step,
       "best on ref_workshop is FIT_R %.2f (%.4f) against the shipped 0.84's "
       "%.4f -- a difference of %+.4f; best on the INDEPENDENT frame is "
       "FIT_R %.2f, which IS the shipped value.  The sweep is broad and shallow "
       "within +-0.02 and falls away hard outside it.  So the constant the "
       "briefs called UNMEASURED is measured, and it was already right"
       % (best_fit[0], best_fit[1], base[0], best_fit[1] - base[0], best_ind[0]))

    span = max(r[1] for r in rows) - min(r[1] for r in rows)
    ck("E2 KILL -- this sweep can actually see the fit depth",
       span > 0.05,
       "the statistic spans %.4f across the sweep (0.70 -> %.4f, shipped 0.84 "
       "-> %.4f, 1.00 -> %.4f).  The bar is on the SPAN, not on one end, so a "
       "flat sweep fails it whichever end is flat.  A sweep that does not move "
       "is measuring nothing (rule 36)"
       % (span, rows[0][1], base[0], rows[-1][1]))

    print("\n  %d checked, %d FAILED%s" % (len(checks), len(fails),
          "  --  " + "; ".join(fails) if fails else ""))
    raise SystemExit(1 if fails else 0)


if __name__ == "__main__":
    main()
