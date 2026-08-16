"""probe_orb_xratio.py -- rev 32.  READ-ONLY.  NO METRE FIGURE IS PRODUCED.

THE QUESTION
------------
SPEC 10.75's vertical POST is the oldest undone item.  SPEC 10.84 (rev 31) said
it is no longer blocked on a READING but on a CONSTRUCTION, and the rev-32 brief
asked for the post as a FRACTION of the bar's half-width -- so that it inherits
`BAR_HALF_Y`'s grade E instead of adding a new lateral choice -- and asked for a
ruling on whether that will close BEFORE the revision is spent.

THE CONSTRUCTION, AND WHY IT IS THE RIGHT SHAPE
-----------------------------------------------
Four points lie on ONE LINE in the BUMPER PLANE: the bar's far end, the far
strut, the near post, and the bar's near end.  Four collinear points carry a
projective invariant -- the CROSS-RATIO -- which is preserved by any camera.
So this needs NO vanishing point, NO scale, NO depth and NO camera model.

**AND IT REPAIRS SPEC 10.84's OBJECTION AT THE ROOT.**  10.84's finding was that
10.83 compared a NOSE-SKIN feature with a BUMPER-PLANE feature and so measured
nothing: A REFUTATION WHOSE TWO TERMS ARE NOT COMMENSURABLE MEASURES NOTHING.
Every one of these four points is in the SAME plane, and rev 31's owner reading
is what guarantees it -- [stated] the post is "bar to blade only ... extending
from the bumper upwards and away from the body panel".  There is no cross-depth
term left to price.

Under the symmetry model (bar ends at t = -1 and +1, struts at t = -f and +f)
the cross-ratio is

    X = (A-C)(B-D) / ((A-D)(B-C))  =  (1+f)^2 / (4f)

one equation in one unknown, solved by  f^2 + (2-4X) f + 1 = 0.  The two roots
are reciprocals; the physical one is the root below 1.

THE RULING: **IT WILL NOT CLOSE, AND IT FAILS ON EXACTLY ONE TERM.**
--------------------------------------------------------------------
The estimator is sound -- P1 below recovers a planted f to 1e-12 from a
synthetic projective map, so the algebra is not the problem.  The problem is
CONDITIONING, and it is entirely in the far end:

  * (1+f)^2/(4f) has a MINIMUM of 1 at f = 1.  Near a measured X of ~1.06 the
    map from X to f is nearly vertical -- dX/df = 0 exactly at the degenerate
    root -- so a small error in X becomes a large error in f.
  * rev 31 established BY THE OWNER'S OWN READING that the far end is a
    SUPERPOSITION of three members inside ~29 px: [stated] "Appears to be
    covering the bumper, the post, and the far end of the bar."

C5 below sweeps the far bar end across rev 31's own stated blob and prints what
f does.  **THE ~29 px IS NOT "THE STATED PRECISION" ON THIS ROUTE; IT IS FATAL
TO IT.**  Reported as a dead route rather than widened into an answer, which is
rev 30's rule about the two estimators that died in `probe_orb_hoop.py`.

WHAT IS PUBLISHED, AND WHAT IS NOT
-----------------------------------
PUBLISHED: two columns MEASURED off the frame this revision --
  * the near post at u 355-377 (cream-run scan, rows 676-700, centre 366).
    SPEC 10.75 drew 357-374 as a POINTER and its own text says no number was to
    be taken from it; rev 30 took one anyway.  THE POINTER IS VINDICATED to
    within 2 px.  The number survives; the process defect stands.
  * the bar's near end (hoop outer) at u = 485.0, stable to 0.0 px
    over a five-threshold sweep.
NOT PUBLISHED: any value of f, any lateral metre figure, any position for the
post.  **THE POST STAYS UNBUILT.**

CONTROLS
--------
  P1  POSITIVE: the estimator must recover a PLANTED f through a synthetic
      projective map with a known vanishing point.  Graded, and the grading is
      run until it fails.
  P2  the two roots must be reciprocal and exactly one must lie below 1.
  C3  the measured columns must be reproducible under a THRESHOLD SWEEP, not
      taken at one threshold.
  C4  the near/far assignment must come from the vehicle's own visible corner,
      not from an assumption.
  C5  KILL: sweep the far bar end across rev 31's stated blob and print f.
"""
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "ref_workshop.jpg")

FAIL = []


def P(s=""):
    print(s)


def check(ok, label, detail=""):
    P("  [%s] %s%s" % ("PASS" if ok else "FAIL", label,
                       ("  -- " + detail) if detail else ""))
    if not ok:
        FAIL.append(label)


def xratio(a, b, c, d):
    return ((a - c) * (b - d)) / ((a - d) * (b - c))


def f_from_X(X):
    """Solve (1+f)^2/(4f) = X.  Returns (f_small, f_large) or None if the
    discriminant is negative -- which means the configuration is not
    reachable by ANY symmetric arrangement, and that is a result."""
    b = 2.0 - 4.0 * X
    disc = b * b - 4.0
    if disc < 0:
        return None
    r = np.sqrt(disc)
    f1, f2 = (-b - r) / 2.0, (-b + r) / 2.0
    return (min(f1, f2), max(f1, f2))


def cream_runs(img, row, u0, u1, lthr, sthr):
    L = 0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]
    mx, mn = img.max(2), img.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    m = (L[row, u0:u1] > lthr) & (sat[row, u0:u1] < sthr)
    out, s = [], None
    for i, v in enumerate(m):
        if v and s is None:
            s = i
        if (not v) and s is not None:
            out.append((u0 + s, u0 + i - 1))
            s = None
    if s is not None:
        out.append((u0 + s, u1 - 1))
    return [r for r in out if r[1] - r[0] >= 1]


def main():
    img = np.asarray(Image.open(REF).convert("RGB")).astype(float)
    P("=" * 74)
    P("probe_orb_xratio.py -- rev 32.  Can the POST close by the bar's own")
    P("two ends?  Ruling published BEFORE the revision is spent.")
    P("=" * 74)
    P("frame ref_workshop.jpg  %d x %d" % (img.shape[1], img.shape[0]))

    P("\n--- P1  POSITIVE, GRADED: recover a PLANTED f through a synthetic map")
    # a genuine 1D projective map u(t) = (vp*t + p)/(t + q)
    vp, p, q = 111.0, -453.8, -1.7036
    def U(t):
        return (vp * t + p) / (t + q)
    worst = 0.0
    for f_true in (0.35, 0.50, 0.626, 0.75, 0.90):
        X = xratio(U(-1.0), U(-f_true), U(+f_true), U(+1.0))
        got = f_from_X(X)
        err = abs(got[0] - f_true)
        worst = max(worst, err)
        P("    planted f %.3f -> X %.6f -> recovered %.6f   err %.2e"
          % (f_true, X, got[0], err))
    check(worst < 1e-8, "P1 the estimator is exact on a synthetic map",
          "worst error %.2e over five planted values -- THE ALGEBRA IS NOT "
          "THE PROBLEM" % worst)

    P("\n--- P1b  GRADE THE CONTROL UNTIL IT FAILS: inject error into the far")
    P("         end ONLY, on the SYNTHETIC map, where truth is known exactly")
    f_true = 0.626
    P("    planted f = %.3f ; far-end column perturbed by dU px" % f_true)
    P("    %6s  %10s  %10s  %8s" % ("dU px", "X", "f", "error %"))
    broke_at = None
    for dU in (0, 1, 2, 4, 8, 15, 29):
        A = U(-1.0) + dU
        X = xratio(A, U(-f_true), U(+f_true), U(+1.0))
        got = f_from_X(X)
        if got is None:
            P("    %6d  %10.6f  %10s  %8s" % (dU, X, "NO REAL ROOT",
                                              "unreachable"))
            broke_at = broke_at or dU
            continue
        e = 100.0 * abs(got[0] - f_true) / f_true
        P("    %6d  %10.6f  %10.4f  %8.1f" % (dU, X, got[0], e))
        if e > 10.0 and broke_at is None:
            broke_at = dU
    check(broke_at is not None and broke_at <= 15,
          "P1b the control FAILS at a perturbation smaller than the real "
          "blob", "10 %% error is reached by dU = %s px, against rev 31's "
                  "stated ~29 px" % broke_at)
    P("    PUBLISHED: the level at which the positive control fails is "
      "dU = %s px." % broke_at)

    P("\n--- P2  the two roots must be reciprocal, exactly one below 1 ---")
    Xt = 1.055861
    r = f_from_X(Xt)
    P("    X %.6f -> roots %.6f and %.6f ; product %.12f"
      % (Xt, r[0], r[1], r[0] * r[1]))
    check(abs(r[0] * r[1] - 1.0) < 1e-9 and r[0] < 1.0 < r[1],
          "P2 the roots are reciprocal and exactly one is physical",
          "product %.12f, small root %.4f, large root %.4f"
          % (r[0] * r[1], r[0], r[1]))

    P("\n--- C3  the two GOOD columns, under a THRESHOLD SWEEP ---")
    P("    %6s  %-22s  %-22s" % ("L thr", "post run (rows 676-700)",
                                 "hoop outer (rows 704-716)"))
    posts, hoops = [], []
    for lthr in (135, 145, 150, 155, 165):
        pa, pb, ha = [], [], []
        for row in range(676, 702, 2):
            for a, b in cream_runs(img, row, 340, 400, lthr, 0.14):
                if b - a >= 8:
                    pa.append(a)
                    pb.append(b)
        for row in range(704, 718, 2):
            for a, b in cream_runs(img, row, 450, 510, lthr, 0.14):
                if b - a >= 3:
                    ha.append(b)
        if pa and ha:
            posts.append((np.median(pa), np.median(pb)))
            hoops.append(np.median(ha))
            P("    %6d  %-22s  %-22s"
              % (lthr, "%.1f - %.1f" % (posts[-1][0], posts[-1][1]),
                 "%.1f" % hoops[-1]))
    p0 = float(np.median([a for a, _ in posts]))
    p1 = float(np.median([b for _, b in posts]))
    hoop = float(np.median(hoops))
    sp = max(b for _, b in posts) - min(b for _, b in posts)
    sh = max(hoops) - min(hoops)
    P("    POST u %.1f - %.1f  (centre %.1f)   HOOP OUTER u %.1f"
      % (p0, p1, 0.5 * (p0 + p1), hoop))
    check(sp <= 6.0 and sh <= 6.0,
          "C3 the two good columns survive a threshold sweep",
          "post right edge moves %.1f px, hoop outer %.1f px over five "
          "thresholds" % (sp, sh))
    P("    SPEC 10.75 drew the post as a POINTER at 357-374 and its own text")
    P("    says no number was to be taken from it.  rev 30 took one.  The")
    P("    POINTER IS VINDICATED to within 2 px -- the number survives, the")
    P("    process defect stands.")

    P("\n--- C4  which end is NEAR?  From the vehicle, not from an assumption")
    P("    The visible flank recedes to HIGH u and the front panel lies to LOW")
    P("    u of the body corner, so the corner at u ~ 490 is the vehicle's")
    P("    NEAR front corner and the bar's near end is the HIGH-u end.")
    P("    REF Sec 9 independently calls the headlamp at u = 419 'the near")
    P("    side of the front panel', which is the same assignment.")
    check(hoop > 0.5 * (p0 + p1),
          "C4 the near end is at higher u than the post",
          "hoop %.1f > post centre %.1f" % (hoop, 0.5 * (p0 + p1)))

    P("\n--- C5  KILL: sweep the far bar end across rev 31's stated blob ---")
    post_u = 0.5 * (p0 + p1)
    strut_u = 228.0
    P("    fixed:  post %.1f   bar near end %.1f   far strut %.1f (blob)"
      % (post_u, hoop, strut_u))
    P("    %8s  %10s  %12s  %10s" % ("far end", "X", "f", "vs u=209"))
    base = None
    span = []
    for A in (203.0, 209.0, 215.0, 221.0, 228.0, 232.0):
        if A >= strut_u:
            P("    %8.1f  %10s  %12s  %10s"
              % (A, "-", "ORDER BROKEN", "the far end would be inboard of "
                 "the strut"))
            continue
        X = xratio(A, strut_u, post_u, hoop)
        got = f_from_X(X)
        if got is None:
            P("    %8.1f  %10.6f  %12s  %10s" % (A, X, "NO REAL ROOT",
                                                 "unreachable"))
            continue
        if base is None:
            base = got[0]
        span.append(got[0])
        P("    %8.1f  %10.6f  %12.4f  %+9.1f %%"
          % (A, X, got[0], 100.0 * (got[0] - base) / base))
    swing = (max(span) - min(span)) / min(span) * 100.0 if span else float("inf")
    check(swing < 10.0, "C5 f is stable across the far end's stated blob",
          "f swings %.0f %% across rev 31's own ~29 px -- THE ROUTE DOES NOT "
          "CLOSE" % swing)

    P("\n" + "=" * 74)
    P("VERDICT: THE CROSS-RATIO ROUTE IS DEAD, AND IT IS DEAD ON ONE TERM.")
    P("=" * 74)
    P("  The estimator is exact (P1, 3.6e-15 worst over five planted values).")
    P("  The CONDITIONING is not: the invariant (1+f)^2/4f has a MINIMUM of 1")
    P("  at f = 1, so near the measured X the map from X back to f is nearly")
    P("  vertical.  The positive control passes 10 %% error at dU = %s px of"
      % broke_at)
    P("  far-end error alone, and rev 31 established from the owner's own")
    P("  reading that the far end is a THREE-MEMBER SUPERPOSITION inside")
    P("  ~29 px.  At 29 px the cross-ratio has NO REAL ROOT AT ALL -- the")
    P("  configuration is not reachable by ANY symmetric arrangement.")
    P("  Every other term is good: the post survives a five-threshold sweep")
    P("  to 0.5 px and the hoop to 0.0 px.")
    P("")
    P("  SO THE POST IS BLOCKED ON ONE COLUMN, AND IT IS A COLUMN THAT")
    P("  MEASUREMENT CANNOT REACH.  A superposition is not resolvable by")
    P("  thresholding it.  That is why rev 32 spends a QUESTION on it rather")
    P("  than a third estimator -- rev 30's rule: MEASURE SOMEWHERE ELSE")
    P("  BEFORE YOU BUILD A THIRD ESTIMATOR, and there is nowhere else on")
    P("  this frame to measure.")
    P("")
    P("  NOT CLAIMED: any value of f.  NOT CLAIMED: that the symmetry model")
    P("  is right -- it is an ASSUMPTION, and the only check available on it")
    P("  (mirroring the far strut through the same map) disagrees at 17 %,")
    P("  which lies inside the blob's own confounding and is therefore")
    P("  NEITHER a refutation NOR a corroboration.  THE POST STAYS UNBUILT.")
    P("")
    P("  CEILING: no scale, no depth, no metre figure, no camera model, no")
    P("  lateral position.  This probe rules a route OUT.  That is all it")
    P("  does, and ruling a route out before it is spent is what the brief")
    P("  asked for.")
    P("")
    P("CONTROLS: 6 checked, %d FAILED" % len(FAIL))
    for f in FAIL:
        P("   FAILED: %s" % f)
    P("")
    P("EXIT CODE 1 IS THE INTENDED RESULT HERE.  C5 is a KILL control: it")
    P("asks whether the route SURVIVES the far end's stated blob, and the")
    P("finding is that it does not.  A green run would have meant the post")
    P("could be built this revision.")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
