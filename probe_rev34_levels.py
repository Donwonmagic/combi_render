"""
probe_rev34_levels.py -- rev 34.  READ-ONLY.  NO METRE FIGURE IS PRODUCED.
NO GEOMETRY MOVES.  NOTHING HERE IS A BUILD VALUE.

WHY THIS PROBE EXISTS, BEFORE ANY QUESTION IS ASKED.

rev 34's item 1 is to ask the owner for the FAR STRUT's column and feed it
into `probe_rev33_barend.py`'s A7.  Before spending his attention, grade the
INSTRUMENT the answer would be scored by.  rev 33's own new rule says a
question about to be asked is a probe too, and so is the threshold it will
be scored against.

WHAT GRADING THE INSTRUMENT FINDS.

`probe_rev33_barend.py` gates its controls in TWO DIFFERENT UNITS.

  A3 gates in PIXELS      :  check(... dU <= CLOSE_AT ...)      CLOSE_AT = 4
  A7 gates in PER CENT    :  check(sw4 <= interp_error(4))      -> 6.2 %

and `interp_error` reads `P1B`, whose own comment in that file says:

    # P1b's published conditioning levels, on the SYNTHETIC map (planted
    # f 0.626)

So A7 asks "does 4 px on the STRUT cost no more than 4 px on the FAR END
costs?" -- a fair question -- but prices the far end's 4 px on a SYNTHETIC
map while pricing the strut's 4 px on the LIVE columns.  The comparison is
live against synthetic.  That is SPEC 10.87.3's defect -- rev 32 quoting
P1b's PLANTED 0.626 as though it were a measurement -- recurring one
revision later inside the probe that records the correction.

THIS PROBE DOES NOT ASSUME THAT IS FATAL, AND IT DOES NOT ASSUME A UNIT.
It computes both readings and reports where they disagree.  A defect in a
scoring map changes a verdict only if the corrected number lands on the
other side of the band; K2 and K4 are written so that outcome is reachable
in either direction.

CONTROLS
  N1  the live estimator reproduces C5's four published rows      POSITIVE
  N2  the synthetic map reproduces P1b's published curve exactly  POSITIVE
  N3  the synthetic map's four columns beside the live four       EVIDENCE
  K1  the far end's LIVE sensitivity equals the SYNTHETIC curve
      that was used to score it                                   KILL
  K2  the two UNITS of the published band agree about whether
      rev 33's far-end residual closes                            KILL
  K3  A7's "the strut is the MORE sensitive column" survives when
      BOTH columns are graded live                                KILL
  K4  the px band transfers between columns -- i.e. 4 px on the
      strut costs what 4 px on the far end costs                  KILL
  K5  a candidate-line question on the strut, at the tightest
      spacing such a set can carry, closes the post               KILL

CEILING, STATED.  This probe does not re-measure the photograph.  It
produces no new column, does not touch the superposition, and publishes no
`f` as a build value.  It grades the MAP and the UNITS that four published
percentages were read off.  If every KILL passed, the conclusion would be
that rev 33's arithmetic was sound and the strut question should be asked
exactly as the rev-34 brief writes it.  That outcome is reachable from here,
which is what makes these controls and not decoration.

NOT CLAIMED: that P1b's synthetic map is a bad instrument, that it was wrong
to build one, or that 0.626 is a bad value.  P1b exists to grade the ALGEBRA
where truth is known exactly and for that it is the right instrument -- P1's
3.55e-15 is why the algebra is not in question.  The claim is only about
where its OUTPUT was later spent.
"""
import math
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---- the LIVE columns.  C3-measured except the strut, which is why we are
#      here at all.  Copied from probe_orb_xratio.py / probe_rev33_barend.py.
POST_U = 365.5          # C3 measured, right edge stable to 0.5 px
HOOP_U = 485.0          # C3 measured, 0.0 px over five thresholds
STRUT_U = 228.0         # C5's far strut -- HARD-CODED, its own print: '(blob)'
ANSWER_U = 205.0        # [stated, rev 33] Q1 + Q1b: AT candidate line 1

C5_PUBLISHED = {203.0: 0.5780, 209.0: 0.6160, 215.0: 0.6661, 221.0: 0.7390}

# ---- P1b's SYNTHETIC map, copied verbatim from probe_orb_xratio.py -------
SYN_VP, SYN_P, SYN_Q = 111.0, -453.8, -1.7036
SYN_F = 0.626

# ---- P1b's published conditioning levels, as rev 33 copied them ----------
P1B = {0: 0.0, 1: 1.4, 2: 2.9, 4: 6.2, 8: 14.3, 15: 44.0}
CLOSE_AT_PX, FAIL_AT_PX = 4, 8          # the band as A3 gates it
SPACING = 7.0                            # rev 32/33's candidate-line spacing

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
    b = 2.0 - 4.0 * X
    disc = b * b - 4.0
    if disc < 0.0:
        return None
    return (-b - math.sqrt(disc)) / 2.0


def U_syn(t):
    return (SYN_VP * t + SYN_P) / (t + SYN_Q)


def f_live(far, strut=None, post=None, hoop=None):
    strut = STRUT_U if strut is None else strut
    post = POST_U if post is None else post
    hoop = HOOP_U if hoop is None else hoop
    if far >= strut:
        return None
    return f_from_X(xratio(float(far), strut, post, hoop))


def interp(curve, dU):
    ks = sorted(curve)
    if dU <= ks[0]:
        return curve[ks[0]]
    for a, b in zip(ks, ks[1:]):
        if a <= dU <= b:
            t = (dU - a) / float(b - a)
            return curve[a] + t * (curve[b] - curve[a])
    return curve[ks[-1]]


def swing_pct(vals):
    """A7's own low-anchored convention, kept identical so every number
    below is directly comparable to A7's published 11.1 %."""
    vals = [v for v in vals if v is not None]
    if len(vals) < 2 or min(vals) <= 0:
        return None
    return 100.0 * (max(vals) - min(vals)) / min(vals)


def far_err(dpx):
    return swing_pct([f_live(ANSWER_U - dpx), f_live(ANSWER_U),
                      f_live(ANSWER_U + dpx)])


def strut_err(dpx):
    return swing_pct([f_live(ANSWER_U, strut=STRUT_U - dpx),
                      f_live(ANSWER_U, strut=STRUT_U),
                      f_live(ANSWER_U, strut=STRUT_U + dpx)])


def main():
    P("=" * 74)
    P("probe_rev34_levels.py -- grade the INSTRUMENT before spending a")
    P("question on the far strut.  READ-ONLY.  NO GEOMETRY MOVES.")
    P("=" * 74)

    # ---------------- N1 -------------------------------------------------
    P("\n--- N1  POSITIVE: the live estimator reproduces C5's rows ---------")
    worst = 0.0
    for u in sorted(C5_PUBLISHED):
        got = f_live(u)
        d = abs(got - C5_PUBLISHED[u])
        worst = max(worst, d)
        P("    far end %6.1f -> f %.6f   published %.4f   delta %.2e"
          % (u, got, C5_PUBLISHED[u], d))
    check(worst < 1e-3,
          "N1 the live estimator reproduces C5's four published rows",
          "worst deviation %.2e over 4 rows" % worst)
    f0 = f_live(ANSWER_U)
    P("    f at the ANSWERED column %.1f is %.4f  (rev 33 published 0.5897)"
      % (ANSWER_U, f0))

    # ---------------- N2 -------------------------------------------------
    P("\n--- N2  POSITIVE: the synthetic map reproduces P1b's curve --------")
    P("    %6s  %10s  %12s  %10s" % ("dU px", "f", "err % now", "published"))
    worst2 = 0.0
    for dU in sorted(P1B):
        A = U_syn(-1.0) + dU
        got = f_from_X(xratio(A, U_syn(-SYN_F), U_syn(+SYN_F), U_syn(+1.0)))
        if got is None:
            P("    %6d  %10s" % (dU, "NO REAL ROOT"))
            continue
        e = 100.0 * abs(got - SYN_F) / SYN_F
        worst2 = max(worst2, abs(e - P1B[dU]))
        P("    %6d  %10.4f  %12.1f  %10.1f" % (dU, got, e, P1B[dU]))
    check(worst2 < 0.1,
          "N2 the synthetic map reproduces P1b's published curve",
          "worst deviation %.2f percentage points over %d rows"
          % (worst2, len(P1B)))

    # ---------------- N3 -------------------------------------------------
    P("\n--- N3  EVIDENCE: the synthetic map's columns vs the LIVE ones ----")
    P("    %-16s %11s %11s %10s" % ("point", "synthetic", "live", "diff px"))
    rows = [("far end   (t=-1)", U_syn(-1.0), ANSWER_U),
            ("far strut (t=-f)", U_syn(-SYN_F), STRUT_U),
            ("near post (t=+f)", U_syn(+SYN_F), POST_U),
            ("near end  (t=+1)", U_syn(+1.0), HOOP_U)]
    worst_col = 0.0
    for name, s, l in rows:
        worst_col = max(worst_col, abs(s - l))
        P("    %-16s %11.1f %11.1f %10.1f" % (name, s, l, l - s))
    P("    worst column disagreement %.1f px -- LARGER than the %d px"
      % (worst_col, CLOSE_AT_PX))
    P("    perturbation this very curve is used to price.")
    P("    planted f %.3f  vs  live f at the answer %.4f" % (SYN_F, f0))

    # ---------------- K1 -------------------------------------------------
    P("\n--- K1  KILL: grade the FAR END *LIVE*, by A7's own method --------")
    P("    %8s %10s" % ("far u", "f"))
    for a in (197.0, 201.0, 205.0, 209.0, 213.0):
        P("    %8.1f %10.4f" % (a, f_live(a)))
    live4, live8 = far_err(4.0), far_err(8.0)
    syn4, syn8 = interp(P1B, 4), interp(P1B, 8)
    P("    +-4 px on the FAR END   LIVE %.1f %%   SYNTHETIC %.1f %%  (%.2f x)"
      % (live4, syn4, live4 / syn4))
    P("    +-8 px on the FAR END   LIVE %.1f %%   SYNTHETIC %.1f %%  (%.2f x)"
      % (live8, syn8, live8 / syn8))
    P("    -> P1b's curve UNDER-PRICES the live configuration throughout.")
    check(abs(live4 - syn4) <= 1.0,
          "K1 the far end's LIVE sensitivity matches the curve used to "
          "score it",
          "live %.1f %% vs synthetic %.1f %% at +-4 px -- the curve is "
          "optimistic by %.2f x" % (live4, syn4, live4 / syn4))

    # ---------------- K2 -------------------------------------------------
    P("\n--- K2  KILL: do the band's TWO UNITS agree about the far end? ----")
    half = SPACING / 2.0
    e_syn_half = interp(P1B, half)
    e_live_half = far_err(half)
    px_says = "CLOSES" if half <= CLOSE_AT_PX else "DOES NOT CLOSE"
    pct_says = "CLOSES" if e_live_half <= syn4 else "DOES NOT CLOSE"
    P("    rev 33's residual after Q1b is the HALF-SPACING, %.1f px." % half)
    P("    PIXEL reading   : %.1f px vs a %d px band          -> %s"
      % (half, CLOSE_AT_PX, px_says))
    P("    PER-CENT reading: %.1f %% live vs the %.1f %% that the %d px band"
      % (e_live_half, syn4, CLOSE_AT_PX))
    P("                      was licensed by                  -> %s"
      % pct_says)
    P("    rev 33 wrote: '%.1f px on the stronger reading -> %.1f %%, INSIDE"
      % (half, e_syn_half))
    P("    the published closing level of dU <= %d px'.  That sentence"
      % CLOSE_AT_PX)
    P("    CONVERTS px to %% and then compares against a px band.  The")
    P("    conversion is unnecessary under the px reading and WRONG under")
    P("    the %% one: live it is %.1f %%, not %.1f %%." % (e_live_half, e_syn_half))
    # The verdict text is COMPUTED, never asserted.  A detail string that
    # narrates "the two readings disagree" while the control PASSES is the
    # degenerate-narration defect SPEC 10.87.2 named -- caught here by an
    # arm that made this control pass and left the sentence standing.
    check(px_says == pct_says,
          "K2 the band's two units agree about rev 33's far-end residual",
          "px reading says %s, per-cent reading says %s -- the two readings "
          "%s" % (px_says, pct_says,
                  "AGREE" if px_says == pct_says else
                  "DISAGREE ACROSS THE DECISION BOUNDARY"))

    # ---------------- K3 -------------------------------------------------
    P("\n--- K3  KILL: A7's comparison, with BOTH columns graded LIVE ------")
    st4, st8 = strut_err(4.0), strut_err(8.0)
    P("    STRUT   +-4 px live : %.1f %%   (A7 published %.1f %%)" % (st4, 11.1))
    P("    FAR END +-4 px live : %.1f %%" % live4)
    P("    FAR END +-4 px syn  : %.1f %%   <- A7's ACTUAL comparator" % syn4)
    P("    A7 published the ratio as %.2f x (%.1f / %.1f)."
      % (11.1 / syn4, 11.1, syn4))
    P("    LIKE FOR LIKE it is  %.2f x (%.1f / %.1f) -- the finding stands,"
      % (st4 / live4, st4, live4))
    P("    the published MARGIN was inflated by %.0f %%."
      % (100.0 * ((11.1 / syn4) / (st4 / live4) - 1.0)))
    check(st4 > live4,
          "K3 the strut is still the more sensitive column, like for like",
          "strut %.1f %% vs far end %.1f %% at +-4 px = %.2f x, against the "
          "%.2f x A7 published" % (st4, live4, st4 / live4, 11.1 / syn4))

    # ---------------- K4 -------------------------------------------------
    P("\n--- K4  KILL: does the PIXEL band transfer between columns? -------")
    P("    A3 gates in px.  If a px band is to mean anything on a NEW")
    P("    column, the same px must buy the same error in f.")
    P("    %10s %14s %14s %8s" % ("+- px", "far end err %", "strut err %",
                                  "ratio"))
    worst_ratio = 0.0
    for d in (1.0, 2.0, 4.0, 8.0):
        a, b = far_err(d), strut_err(d)
        worst_ratio = max(worst_ratio, b / a)
        P("    %10.1f %14.1f %14.1f %8.2f x" % (d, a, b, b / a))
    P("    The SAME %d px costs %.1f %% on the far end and %.1f %% on the"
      % (CLOSE_AT_PX, live4, st4))
    P("    strut.  A tolerance stated in the units of the MEASUREMENT does")
    P("    not transfer to a column with a different px -> f map.")
    check(worst_ratio <= 1.10,
          "K4 the px band buys the same error in f on both columns",
          "the same px costs up to %.2f x more on the strut -- the band is "
          "a PER-COLUMN proxy, licensed on ONE column by a synthetic map"
          % worst_ratio)

    # ---------------- K5 -------------------------------------------------
    P("\n--- K5  KILL: CAN A CANDIDATE-LINE QUESTION ON THE STRUT CLOSE? ---")
    P("    THE PRE-COMMITMENT FOR REV 34's QUESTION.  Per rev 33's rule it")
    P("    names the quantity it binds: the TOTAL error in f, in per cent,")
    P("    against the tolerance the project ACTUALLY ACCEPTED -- %d px on"
      % CLOSE_AT_PX)
    P("    the far end, which LIVE is %.1f %%.  (Using the synthetic %.1f %%"
      % (live4, syn4))
    P("    instead would only make this verdict harsher, so the generous")
    P("    reading is the one taken.)")
    P("")
    P("    Far end already spends %.1f %% at its answered +-%.1f px."
      % (e_live_half, half))
    budget = live4 ** 2 - e_live_half ** 2
    budget = math.sqrt(budget) if budget > 0 else None
    P("    Budget left for the strut, in quadrature: %s"
      % ("%.2f %%" % budget if budget else "NONE"))
    P("")
    P("    %10s %14s %16s %10s" % ("strut +-px", "strut err %", "total (quad)",
                                   "verdict"))
    need_px = None
    for d in (0.5, 1.0, 1.5, 2.0, 3.0, 3.5, 4.0):
        e = strut_err(d)
        tot = math.sqrt(e_live_half ** 2 + e ** 2)
        ok = tot <= live4
        if ok:
            need_px = d
        P("    %10.1f %14.1f %16.1f %10s"
          % (d, e, tot, "closes" if ok else "NO"))
    P("")
    if need_px is not None:
        P("    -> THE STRUT MUST BE PINNED TO ABOUT +-%.1f px FOR THE POST"
          % need_px)
        P("       TO CLOSE.  That is the number this question would have to")
        P("       deliver.")
    best_px = SPACING / 2.0
    e_best = strut_err(best_px)
    tot_best = math.sqrt(e_live_half ** 2 + e_best ** 2)
    P("    A candidate set at rev 32/33's %.0f px spacing returns at best"
      % SPACING)
    P("    +-%.1f px -> %.1f %% on the strut alone, %.1f %% total."
      % (best_px, e_best, tot_best))
    P("    Halving the spacing to %.0f px returns +-%.1f px -> %.1f %% alone,"
      % (SPACING / 2.0, SPACING / 4.0, strut_err(SPACING / 4.0)))
    P("    %.1f %% total."
      % math.sqrt(e_live_half ** 2 + strut_err(SPACING / 4.0) ** 2))
    P("    The strut's own print calls it '(blob)'; rev 31 measured the far")
    P("    end's blob at ~29 px.  A %.1f px reading is not available from a"
      % (need_px if need_px else 1.5))
    P("    blob on this frame.")
    check(tot_best <= live4,
          "K5 a candidate-line question on the strut closes the post",
          "best-case total %.1f %% against a %.1f %% tolerance; closing "
          "needs about +-%.1f px on a feature its own print calls '(blob)'"
          % (tot_best, live4, need_px if need_px else 0.0))

    # ---------------- ruling ---------------------------------------------
    # REFUSE TO PRINT THE RULING IF A POSITIVE CONTROL FAILED.  The ruling
    # below states its own controls' outcomes in prose.  Arms 4 and 5 showed
    # that prose surviving a failed positive control -- SPEC 10.87.2's
    # degenerate narration, in a probe written the same day.  A ruling whose
    # foundation did not hold is not a ruling.
    _pos = ["N1 the live estimator reproduces", "N2 the synthetic map reproduces"]
    if any(p in " | ".join(FAIL) for p in _pos):
        P("\n" + "=" * 74)
        P("REFUSING TO PRINT A RULING -- a POSITIVE control FAILED.")
        P("=" * 74)
        P("  The ruling below narrates its own controls' outcomes.  With a")
        P("  positive control down, that narration would assert a result the")
        P("  run did not produce.  Nothing is ruled.")
        P("")
        P("CONTROLS: %d FAILED" % len(FAIL))
        for _f in FAIL:
            P("   FAILED: %s" % _f)
        return 1

    P("\n" + "=" * 74)
    P("RULING")
    P("=" * 74)
    P("  WHAT SURVIVES, SAID FIRST AND WITHOUT HEDGING:")
    P("    - THE ALGEBRA IS UNTOUCHED.  N1 and N2 both pass.  P1's 3.55e-15")
    P("      stands.  DO NOT REBUILD THE CROSS-RATIO.")
    P("    - K3 PASSES.  The strut IS the more sensitive column even when")
    P("      both are graded live.  A6/A7's CONCLUSION SURVIVES -- rev 33's")
    P("      verdict was right.  Only its published margin was inflated,")
    P("      %.2f x reported against %.2f x like-for-like."
      % (11.1 / syn4, st4 / live4))
    P("    - rev 33's far-end verdict CLOSES on the unit A3 actually gates")
    P("      in (px).  It is not overturned.")
    P("    - THE POST WAS ALREADY UNBUILT AND STAYS UNBUILT.  Nothing here")
    P("      moves a verdict in the permissive direction.")
    P("")
    P("  WHAT DOES NOT SURVIVE:")
    P("    - K1.  P1b's curve under-prices the live configuration by %.2f x"
      % (live4 / syn4))
    P("      at 4 px and %.2f x at 8 px.  EVERY per-cent figure ever read"
      % (live8 / syn8))
    P("      off that curve and applied to the live columns is that much")
    P("      too small.  The published %.1f %% closing level is %.1f %% live;"
      % (syn4, live4))
    P("      the published %.1f %% failing level is %.1f %% live."
      % (syn8, live8))
    P("    - K2.  The band exists in TWO UNITS inside ONE probe, and on")
    P("      rev 33's own residual they DISAGREE ACROSS THE BOUNDARY.")
    P("      rev 33's justifying sentence converts px to %% unnecessarily")
    P("      and lands on the synthetic value.  THE VERDICT IS RIGHT AND")
    P("      THE REASON PRINTED UNDER IT IS NOT -- which is exactly what")
    P("      rev 33 said about its OWN pre-commitment, one quantity over.")
    P("    - K4.  The px band DOES NOT TRANSFER.  4 px buys %.1f %% on the"
      % live4)
    P("      far end and %.1f %% on the strut.  Every use of 'dU <= %d px'"
      % (st4, CLOSE_AT_PX))
    P("      on a new column silently assumes a shared px -> f map.")
    P("")
    P("  WHAT THIS DOES TO REV 34's ITEM 1 -- SAID BEFORE ASKING:")
    P("    K5 FAILS.  A candidate-line question on the strut CANNOT CLOSE")
    P("    THE POST at any spacing such a set can carry on this feature.")
    P("    Closing needs about +-%.1f px on a column whose own print calls"
      % (need_px if need_px else 0.0))
    P("    it '(blob)'.  The rev-34 brief's instruction to bracket on both")
    P("    sides is right and necessary -- and still not sufficient.")
    P("")
    P("    THE QUESTION IS STILL WORTH ASKING, FOR A DIFFERENT REASON, AND")
    P("    THE FIGURE MUST SAY SO: the strut is the last ungraded column in")
    P("    the estimator, it is hard-coded on no support at all, and a")
    P("    bounded owner reading converts it from '(blob)' into a measured")
    P("    value with a stated interval.  THAT is what the answer buys.")
    P("    IT DOES NOT BUY THE POST.")
    P("")
    P("  NOT CLAIMED: that %.1f is wrong, that the strut should never be" % STRUT_U)
    P("  measured, or that P1b was a mistake.  Only that the number it")
    P("  published was spent on columns it was never measured on.")
    P("")
    P("=" * 74)
    P("CONTROLS: 8 checked, %d FAILED" % len(FAIL))
    for f in FAIL:
        P("   FAILED: %s" % f)
    if FAIL:
        P("")
        P("EXIT CODE 1 IS THE INTENDED RESULT.  K1, K2, K4 and K5 are KILL")
        P("controls, written to fire if the substitution and the unit")
        P("ambiguity matter.  K3 is written to fire if A6/A7's conclusion")
        P("does NOT survive -- K3 PASSING is a real result, reported as one.")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
