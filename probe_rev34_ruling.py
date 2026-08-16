"""
probe_rev34_ruling.py -- rev 34.  READ-ONLY.  NO METRE FIGURE IS PRODUCED.
NO GEOMETRY MOVES.  NO `f` IS PUBLISHED AS A BUILD VALUE.

THE OWNER ANSWERED TWICE.
  [stated, rev 34] Q1  : the far strut is at S1 or S2 -- LEFT of the
                         hard-coded u = 228.
  [stated, rev 34] Q1b : it is at B1 OR LEFT OF IT -- u 205 to 208.

Both answers are the LEFTMOST option of their set.  rev 33's rule says an
endpoint answer is an open interval and must be bounded before it is
consumed.  Q1's left side WAS bounded, and not by a set boundary I chose:
the cross-ratio requires far_end < strut, so with the far end answered at
u = 205 every column at or left of 205 is forbidden by the estimator's own
order.  Q1b's leftmost option is that wall.  THE INTERVAL IS CLOSED ON BOTH
SIDES: u in (205, 208].

WHAT THIS PROBE RULES ON.  Not whether the post closes -- K5 already said it
does not, before the question was asked.  It rules on something the answer
made visible that no prior revision anticipated, because every prior
revision assumed the strut sat ~23 px inboard of the bar's far end.

CONTROLS
  R1  the estimator reproduces C5's four published rows            POSITIVE
  R2  the answered interval is closed on both sides and its `f`
      span is reported, not asserted                               EVIDENCE
  R3  the two far-side columns are separated by more than the far
      end's OWN published uncertainty                              KILL
  R4  the estimator's precondition (far_end < strut) survives the
      far end's own published error bar                            KILL
  R5  the answered regime is no more sensitive than the regime the
      go/no-go levels were graded in                               KILL
  R6  the post closes                                              KILL

CEILING, STATED.  This probe re-measures nothing.  It consumes two owner
readings and the columns already in the tree.  It does not claim the
assembly is asymmetric, it does not claim u 228 was a lie, and it does not
claim the owner's interval is wrong.  It claims only what the arithmetic
shows about four numbers and their stated uncertainties.

NOT CLAIMED: that the symmetry model (struts at t = -f and +f) is refuted.
A large far-side overhang in 3D can project to a very small one in image
space, and the cross-ratio already accounts for that exactly -- that is the
whole reason it was chosen.  The finding below is about SEPARABILITY, which
is a fact about the numbers, not about the model.
"""
import math
import sys

POST_U, HOOP_U = 365.5, 485.0
FAR_U = 205.0            # [stated, rev 33] Q1 + Q1b
FAR_RESID = 3.5          # rev 33's own residual after Q1b: the half-spacing
STRUT_HARD = 228.0       # what C5 assumed, on no support
ANS_LO, ANS_HI = 205.0, 208.0     # [stated, rev 34] Q1b: B1 or left of it
ANS_MID = 206.5

C5_PUBLISHED = {203.0: 0.5780, 209.0: 0.6160, 215.0: 0.6661, 221.0: 0.7390}
CLOSE_PCT = 8.6          # the 4 px band, priced LIVE (probe_rev34_levels K1)

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
    return None if disc < 0.0 else (-b - math.sqrt(disc)) / 2.0


def f_of(far, strut):
    if far >= strut:
        return None
    return f_from_X(xratio(float(far), float(strut), POST_U, HOOP_U))


def swing(vals):
    """Returns None if ANY sample is unreachable.  The first draft filtered
    the Nones out and computed a swing over the survivors, which printed a
    SMALLER number for a regime that had actually broken -- while the prose
    below the table said it returned nothing.  A silently dropped sample is
    not a smaller error, it is a missing one."""
    if any(v is None for v in vals):
        return None
    if len(vals) < 2 or min(vals) <= 0:
        return None
    return 100.0 * (max(vals) - min(vals)) / min(vals)


def main():
    P("=" * 74)
    P("probe_rev34_ruling.py -- the owner's two answers, fed into C5.")
    P("=" * 74)

    P("\n--- R1  POSITIVE: the estimator reproduces C5's published rows ----")
    worst = 0.0
    for u in sorted(C5_PUBLISHED):
        got = f_of(u, STRUT_HARD)
        worst = max(worst, abs(got - C5_PUBLISHED[u]))
        P("    far end %6.1f -> f %.6f   published %.4f" % (u, got,
                                                            C5_PUBLISHED[u]))
    check(worst < 1e-3, "R1 the estimator reproduces C5's four rows",
          "worst deviation %.2e" % worst)

    P("\n--- R2  EVIDENCE: the answered interval, closed on both sides -----")
    P("    LEFT  bound: the ORDERING WALL at u %.0f -- the estimator's own"
      % FAR_U)
    P("                 precondition, not a set boundary I chose.")
    P("    RIGHT bound: [stated] B1, u %.0f." % ANS_HI)
    P("    %10s %10s" % ("strut u", "f"))
    for s in (205.25, 205.5, 206.0, 206.5, 207.0, 207.5, 208.0):
        P("    %10.2f %10.4f" % (s, f_of(FAR_U, s)))
    f_lo, f_hi = f_of(FAR_U, ANS_HI), f_of(FAR_U, 205.25)
    P("    the answered interval spans f %.4f .. %.4f  = %.1f %%"
      % (f_lo, f_hi, 100.0 * (f_hi - f_lo) / f_lo))
    P("    the HARD-CODED %.0f gives f %.4f -- OUTSIDE the answered interval"
      % (STRUT_HARD, f_of(FAR_U, STRUT_HARD)))
    P("    by %.1f %%.  Three revisions of C5 ran on a column the owner"
      % (100.0 * (f_lo - f_of(FAR_U, STRUT_HARD)) / f_of(FAR_U, STRUT_HARD)))
    P("    places %.0f-%.0f px away." % (STRUT_HARD - ANS_HI,
                                         STRUT_HARD - ANS_LO))

    P("\n--- R3  KILL: are the two far-side columns SEPARABLE? -------------")
    gap = ANS_MID - FAR_U
    P("    bar far end        u %.1f   [stated, rev 33]" % FAR_U)
    P("    far strut, centre  u %.1f   [stated, rev 34]" % ANS_MID)
    P("    GAP                  %.1f px" % gap)
    P("    the far end's OWN published residual after Q1b is +-%.1f px."
      % FAR_RESID)
    P("    -> its uncertainty is %.1f x the gap it has to stay left of."
      % (FAR_RESID / gap))
    check(gap > FAR_RESID,
          "R3 the two far-side columns are separated by more than the far "
          "end's own uncertainty",
          "gap %.1f px against a +-%.1f px residual -- the two points are "
          "NOT SEPARABLE at the precision of the readings that define them"
          % (gap, FAR_RESID))

    P("\n--- R4  KILL: does the PRECONDITION survive the far end's bar? ----")
    P("    the far end's stated interval is %.1f .. %.1f px."
      % (FAR_U - FAR_RESID, FAR_U + FAR_RESID))
    P("    %10s %16s" % ("far end u", "strut 206.5"))
    broken = 0
    tested = []
    for far in (201.5, 203.0, 205.0, 206.0, 206.5, 207.5, 208.5):
        v = f_of(far, ANS_MID)
        tested.append(far)
        if v is None:
            broken += 1
            P("    %10.1f %16s" % (far, "ORDER BROKEN"))
        else:
            P("    %10.1f %16.4f" % (far, v))
    frac = 100.0 * (FAR_U + FAR_RESID - ANS_MID) / (2.0 * FAR_RESID)
    P("    %.0f %% of the far end's own error bar puts it AT OR RIGHT OF the"
      % frac)
    P("    strut, which the four-point construction forbids outright.")
    check(broken == 0,
          "R4 the estimator's precondition survives the far end's own error "
          "bar",
          "%d of %d sampled positions inside the far end's stated interval "
          "give ORDER BROKEN -- the four-point construction has degenerated "
          "to three" % (broken, len(tested)))

    P("\n--- R5  KILL: how sensitive is the ANSWERED regime? ---------------")
    P("    %14s %10s %10s %10s" % ("strut centre", "+-0.5 px", "+-1.0 px",
                                   "+-1.5 px"))
    for c in (ANS_MID, 212.0, STRUT_HARD):
        cells = []
        for dd in (0.5, 1.0, 1.5):
            s = swing([f_of(FAR_U, c - dd), f_of(FAR_U, c),
                       f_of(FAR_U, c + dd)])
            cells.append("ORDER BRK" if s is None else "%.1f %%" % s)
        P("    %14.1f %10s %10s %10s" % (c, cells[0], cells[1], cells[2]))
    s_ans = swing([f_of(FAR_U, ANS_MID - 1.0), f_of(FAR_U, ANS_MID),
                   f_of(FAR_U, ANS_MID + 1.0)])
    s_hard = swing([f_of(FAR_U, STRUT_HARD - 1.0), f_of(FAR_U, STRUT_HARD),
                    f_of(FAR_U, STRUT_HARD + 1.0)])
    s15 = swing([f_of(FAR_U, ANS_MID - 1.5), f_of(FAR_U, ANS_MID),
                 f_of(FAR_U, ANS_MID + 1.5)])
    P("    at +-1 px the answered regime costs %.1f %% against %.1f %% where"
      % (s_ans, s_hard))
    P("    the levels were graded -- %.1f x worse." % (s_ans / s_hard))
    P("    at +-1.5 px it %s"
      % ("returns %.1f %%." % s15 if s15 is not None else
         "DOES NOT RETURN A NUMBER AT ALL -- the low sample is at or "
         "left of the\n    ordering wall.  This sentence is computed "
         "from the table above it."))
    check(s_ans <= s_hard * 1.1,
          "R5 the answered regime is no more sensitive than the graded one",
          "%.1f %% vs %.1f %% at +-1 px -- %.1f x worse, and +-1.5 px breaks "
          "the order" % (s_ans, s_hard, s_ans / s_hard))

    P("\n--- R6  KILL: does the post close? --------------------------------")
    best = swing([f_of(FAR_U, ANS_LO + 0.25), f_of(FAR_U, ANS_MID),
                  f_of(FAR_U, ANS_HI)])
    assert best is not None, "R6's span must be reachable or it is not a span"
    tot = math.sqrt(7.5 ** 2 + best ** 2)
    P("    strut, across the WHOLE answered interval : %.1f %%" % best)
    P("    far end, at its published +-3.5 px, live  : 7.5 %")
    P("    total in quadrature                       : %.1f %%" % tot)
    P("    against the %.1f %% the 4 px band buys live." % CLOSE_PCT)
    check(tot <= CLOSE_PCT, "R6 the post closes",
          "%.1f %% against a %.1f %% tolerance" % (tot, CLOSE_PCT))

    P("\n" + "=" * 74)
    P("RULING -- THE CROSS-RATIO ROUTE IS RETIRED, AND NOT ON PRECISION")
    P("=" * 74)
    P("  WHAT THE TWO ANSWERS BOUGHT, said first because it is the point:")
    P("    THE LAST UNGRADED COLUMN IS NOW MEASURED.  The far strut was")
    P("    hard-coded at u %.0f on no support of any kind, its own print" % STRUT_HARD)
    P("    calling it '(blob)'.  It now has an owner reading CLOSED ON BOTH")
    P("    SIDES: u in (%.0f, %.0f].  That is what was asked for and that is"
      % (ANS_LO, ANS_HI))
    P("    what arrived.")
    P("")
    P("    AND THE HARD-CODED VALUE WAS WRONG BY %.0f-%.0f px, which puts it"
      % (STRUT_HARD - ANS_HI, STRUT_HARD - ANS_LO))
    P("    OUTSIDE the answered interval entirely.  Every C5 row published")
    P("    since rev 32 was computed at a column the owner does not put the")
    P("    feature anywhere near.  NOT A REFINEMENT -- A REPLACEMENT.")
    P("")
    P("  WHY THE ROUTE IS RETIRED, and this is NEW:")
    P("    R3 and R4.  The answered strut sits %.1f px from the bar's far"
      % gap)
    P("    end.  The far end's OWN published residual is +-%.1f px -- %.1f x"
      % (FAR_RESID, FAR_RESID / gap))
    P("    the gap.  The two points are NOT SEPARABLE at the precision of")
    P("    the readings that define them, and %.0f %% of the far end's error"
      % frac)
    P("    bar puts it at or right of the strut, which the construction")
    P("    forbids outright.")
    P("")
    P("    THE FOUR-POINT CONSTRUCTION HAS DEGENERATED TO THREE.  That is a")
    P("    failure of its PRECONDITION, not of its precision.  No amount of")
    P("    further measurement on these two columns repairs it, because the")
    P("    thing that broke is that they are the same place to within their")
    P("    own error bars.")
    P("")
    P("    EVERY PRIOR REVISION ASSUMED OTHERWISE.  C5, P1b, A6, A7 and both")
    P("    of rev 34's own probes were written on a %.0f px separation."
      % (STRUT_HARD - FAR_U))
    P("    The owner's reading makes it %.1f px.  Nobody could have found" % gap)
    P("    this by measuring harder; it took asking.")
    P("")
    P("  WHAT IS NOT CLAIMED:")
    P("    - NOT that the assembly is asymmetric.  A large far-side overhang")
    P("      in 3D can project to a small one, and the cross-ratio accounts")
    P("      for that exactly.  The finding is about SEPARABILITY.")
    P("    - NOT that the owner's interval is wrong, or that u %.0f was a lie."
      % STRUT_HARD)
    P("      u %.0f was never a measurement; that is the whole complaint."
      % STRUT_HARD)
    P("    - NOT that the algebra failed.  R1 passes; P1's 3.55e-15 stands.")
    P("")
    P("  THE POST STAYS UNBUILT.  NO `f` IS PUBLISHED AS A BUILD VALUE.")
    P("  What closes it is unchanged and is now the ONLY route: a square-on")
    P("  frame of the FRONT.  Everything else on this panel has been spent.")
    P("")
    P("=" * 74)
    P("CONTROLS: 6 checked, %d FAILED" % len(FAIL))
    for f in FAIL:
        P("   FAILED: %s" % f)
    if FAIL:
        P("")
        P("EXIT CODE 1 IS THE INTENDED RESULT.  R3, R4, R5 and R6 are KILL")
        P("controls.  R3 and R4 are the ruling; R5 and R6 were already")
        P("expected to fail and are kept so the record shows both reasons.")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
