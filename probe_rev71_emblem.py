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
       "FIT_R %.2f (%.4f against the shipped %.4f, %+.4f).  ON THE REPAIRED "
       "RULER (F246) BOTH FRAMES PREFER A DEEPER FIT THAN THE SHIPPED 0.84, "
       "and the independent frame's argmax is TWO steps away -- which is why "
       "this row refuses.  On the BROKEN ruler it passed, and rev 71's first "
       "draft graded the fit depth CLOSED on that reading"
       % (best_fit[0], best_fit[1], base[0], best_fit[1] - base[0],
          best_ind[0], best_ind[2], base[1], best_ind[2] - base[1]))

    span = max(r[1] for r in rows) - min(r[1] for r in rows)
    ck("E2 KILL -- this sweep can actually see the fit depth",
       span > 0.05,
       "the statistic spans %.4f across the sweep (0.70 -> %.4f, shipped 0.84 "
       "-> %.4f, 1.00 -> %.4f).  The bar is on the SPAN, not on one end, so a "
       "flat sweep fails it whichever end is flat.  A sweep that does not move "
       "is measuring nothing (rule 36)"
       % (span, rows[0][1], base[0], rows[-1][1]))

    # ---- THE THREE SEARCHES BEHIND F252.  OPT-IN, because (C) is ~9 minutes.
    # They are HERE rather than in a scratch script so the next context can
    # REPRODUCE the figures the brief and the register publish, instead of
    # taking them from prose (rule 5, rule 16).
    #    T1_REV71_SEARCH=AB  runs (A) and (B), ~40 s
    #    T1_REV71_SEARCH=ABC also runs (C), the 1400-start global search
    #
    # ⚠ EVERY IoU THEY PRINT IS ON THE INSTRUMENT F246 REFUTES.  They RANK
    # constructions against each other on ONE fixed ruler, which is what a
    # search needs; their DISTANCE from 0.9882 is NOT a shape deficit.
    want = os.environ.get("T1_REV71_SEARCH", "")
    if want:
        import math
        import random
        import time

        def sc6(vec):
            p = dict(zip(("V_TIP_X", "APEX_Z", "W_ARM_X", "W_ARM_Z",
                          "W_TR_X", "W_TR_Z", "W_PEAK_Z"), vec[:7]))
            p["on_band"] = True
            return X.mask(p, vec[7], rows=220)

        def sc9(vec):
            p = dict(zip(("V_TIP_X", "V_TIP_Z", "APEX_Z", "W_ARM_X", "W_ARM_Z",
                          "W_TR_X", "W_TR_Z", "W_PEAK_Z"), vec[:8]))
            p["on_band"] = False
            return X.mask(p, vec[8], rows=220)

        def descend(vec, build, steps, rounds, dst):
            cur = F.fit(build(vec), dst)[0]
            for _ in range(rounds):
                for i in range(len(vec)):
                    moved = True
                    while moved:
                        moved = False
                        for d in (+steps[i], -steps[i]):
                            q = list(vec)
                            q[i] += d
                            if q[0] <= 0.02 or not (0.05 < q[-1] < 0.60):
                                continue
                            try:
                                val = F.fit(build(q), dst)[0]
                            except Exception:
                                continue
                            if val > cur + 2e-5:
                                cur, vec, moved = val, q, True
                                break
                steps = [t * 0.55 for t in steps]
            return vec, cur

        P = X.SHIPPED
        print("\n  F252 -- THE SEARCHES.  fit on ref_workshop, score on IMG_2073 (re-cut).")
        print("  shipped: fit %.4f  indep %.4f"
              % (F.fit(X.mask(P, X.WFRAC, rows=220), dst_fit)[0],
                 F.fit(X.mask(P, X.WFRAC, rows=220), dst_ind)[0]))
        vA = [P["V_TIP_X"], P["APEX_Z"], P["W_ARM_X"], P["W_ARM_Z"],
              P["W_TR_X"], P["W_TR_Z"], P["W_PEAK_Z"], X.WFRAC]
        vA, cA = descend(vA, sc6, [.06, .06, .12, .06, .06, .06, .06, .04], 6, dst_fit)
        print("  (A) CURRENT parameterisation re-searched   fit %.4f  indep %.4f"
              % (cA, F.fit(sc6(vA), dst_ind)[0]))
        R = X.RING_INNER_FRAC
        ty = (R ** 2 - P["V_TIP_X"] ** 2) ** 0.5
        k = R / math.hypot(P["W_ARM_X"], P["W_ARM_Z"])
        vB = [P["V_TIP_X"], ty, P["APEX_Z"], P["W_ARM_X"] * k, P["W_ARM_Z"] * k,
              P["W_TR_X"], P["W_TR_Z"], P["W_PEAK_Z"], X.WFRAC]
        vB, cB = descend(vB, sc9, [.06] * 8 + [.04], 7, dst_fit)
        print("  (B) THE BRIEF'S PRESCRIPTION, free endpoints   fit %.4f  indep %.4f"
              % (cB, F.fit(sc9(vB), dst_ind)[0]))
        if "C" in want:
            t0 = time.time()
            BND = [(.10, .70), (.20, .82), (-.50, .60), (.20, .82), (-.60, .60),
                   (.10, .70), (-.82, -.10), (-.60, .55), (.10, .40)]
            random.seed(71)
            pool = []
            for _ in range(1400):
                q = [random.uniform(a, b) for a, b in BND]
                if math.hypot(q[0], q[1]) < .30 or math.hypot(q[3], q[4]) < .30:
                    continue
                try:
                    pool.append((F.fit(sc9(q), dst_fit)[0], q))
                except Exception:
                    pass
            pool.sort(key=lambda t: -t[0])
            bc, bv = -1.0, None
            for _s, q in pool[:12]:
                q2, c2 = descend(q, sc9, [.10] * 9, 8, dst_fit)
                if c2 > bc:
                    bc, bv = c2, q2
            print("  (C) 1400-start GLOBAL search + polish     fit %.4f  indep %.4f  (%.0fs)"
                  % (bc, F.fit(sc9(bv), dst_ind)[0], time.time() - t0))

    print("\n  %d checked, %d FAILED%s" % (len(checks), len(fails),
          "  --  " + "; ".join(fails) if fails else ""))
    raise SystemExit(1 if fails else 0)


if __name__ == "__main__":
    main()
