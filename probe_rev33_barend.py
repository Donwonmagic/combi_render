"""
probe_rev33_barend.py -- rev 33.  READ-ONLY.

THE OWNER ANSWERED Q1: the over-rider bar's far termination is at CANDIDATE
LINE 1, u = 205.  This probe feeds that column into C5's machinery and rules
on whether the post can be built, against a go/no-go that was PUBLISHED IN
REV 32 AND RESTATED ON THE FIGURE BEFORE HE ANSWERED.

THE PRE-COMMITMENT, ON THE RECORD BEFORE THE ANSWER ARRIVED (rev33_q1
figure, "WHAT I EXPECT"):
    "the three usable lines are 7 px apart and span 20.6 % in f ... naming
     ONE line still leaves ~7 px of residual and the route does NOT close."
This probe is scored against that sentence, not against a fresh opinion.

CONTROLS
  A1  the estimator reproduces C5's published rows                POSITIVE
  A2  u = 205 is inside C5's swept range and order is intact      SANITY
  A3  the residual implied by the LINE SPACING lands the error
      between the two published levels                            GRADED
  A4  the answer is the EXTREME of the offered set, so the
      interval is ONE-SIDED -- test whether the set bracketed it  KILL
  A5  a left-unbounded interval is not a measurement: grade how
      far f moves for plausible columns LEFT of the offered set   KILL
  A6  did the grading ever cover every column the estimator
      consumes?  The FAR STRUT was never measured or graded       KILL
  A7  grade the FAR STRUT with the far end held at the answer     KILL

A4 AND A5 STILL FAIL BY DESIGN.  They record what the Q1 answer ALONE
established.  Q1b then BOUNDED that side -- [stated] the end is AT line 1,
not left of it -- and the ruling scores both answers together.  The failures
are kept rather than silenced because they are the reason Q1b was asked.

WHY A4 AND A5 EXIST.  He picked LINE 1, the leftmost option.  When a
respondent selects the endpoint of an offered range, the range may simply not
have reached far enough: the true value can lie beyond it, and nothing in the
answer excludes that.  rev 31 twice returned an answer OUTSIDE the offered
set and both times it was better than the set.  Choosing the extreme member
is the weakest evidence the set can produce that the set was wide enough --
and this project's own rule says the option set is a probe too.

CEILING, STATED.  This probe cannot tell whether the true edge is at 205 or
left of it.  It can only price that ambiguity.  It does not re-measure the
photograph, it does not revisit the superposition, and it publishes NO f as
a build value.
"""
import math
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---- C5's constants, copied from probe_orb_xratio.py --------------------
POST_U = 365.5          # C3 measured, right edge stable to 0.5 px
HOOP_U = 485.0          # C3 measured, 0.0 px over five thresholds
STRUT_U = 228.0         # C5's far strut

# C5's published rows, the positive control
C5_PUBLISHED = {203.0: 0.5780, 209.0: 0.6160, 215.0: 0.6661, 221.0: 0.7390}

# P1b's published conditioning levels, on the SYNTHETIC map (planted f 0.626)
P1B = {0: 0.0, 1: 1.4, 2: 2.9, 4: 6.2, 8: 14.3, 15: 44.0}
CLOSE_AT, FAIL_AT = 4, 8

ANSWER_U = 205.0        # [stated] the owner's Q1 answer, rev 33
# [stated, rev 33] Q1b: the end is AT line 1, NOT left of it.  This CLOSES the
# left side that A4/A5 opened.  Recorded here so the ruling below is scored
# against BOTH answers, not just the first.
Q1B_LEFT_BOUNDED = True
CAND = [205, 212, 219, 228, 240]
SPACING = 7.0           # the offered lines' spacing, in original-frame px

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


def f_at(u):
    if u >= STRUT_U:
        return None
    return f_from_X(xratio(float(u), STRUT_U, POST_U, HOOP_U))


def interp_error(dU):
    """Interpolate P1b's published error curve.  Levels are the record."""
    ks = sorted(P1B)
    if dU <= ks[0]:
        return P1B[ks[0]]
    for a, b in zip(ks, ks[1:]):
        if a <= dU <= b:
            t = (dU - a) / float(b - a)
            return P1B[a] + t * (P1B[b] - P1B[a])
    return P1B[ks[-1]]


def main():
    P("=" * 74)
    P("probe_rev33_barend.py -- the owner's Q1 answer, fed into C5.")
    P("=" * 74)
    P("[stated, rev 33] the bar's far end is at CANDIDATE LINE 1, u = 205.")
    P("")
    P("PRE-COMMITMENT MADE BEFORE THE ANSWER: naming one line leaves ~7 px")
    P("of residual and THE ROUTE DOES NOT CLOSE.  Scored against that.")

    # ---- A1 positive control ------------------------------------------
    P("\n--- A1  POSITIVE: reproduce C5's published rows ------------------")
    worst = 0.0
    for u, want in sorted(C5_PUBLISHED.items()):
        got = f_at(u)
        worst = max(worst, abs(got - want))
        P("    u %6.1f   published %.4f   recomputed %.4f" % (u, want, got))
    check(worst < 5e-4, "A1 the estimator reproduces C5",
          "worst deviation %.2e over %d rows" % (worst, len(C5_PUBLISHED)))

    # ---- A2 sanity ------------------------------------------------------
    P("\n--- A2  SANITY: is the answered column usable at all? ------------")
    f0 = f_at(ANSWER_U)
    P("    u = %.1f   ->   f = %.4f  of the bar's half-width" % (ANSWER_U, f0))
    check(f0 is not None and ANSWER_U < STRUT_U,
          "A2 the answered column is inside C5's order",
          "u %.0f < strut %.0f" % (ANSWER_U, STRUT_U))

    # ---- A3 graded: the line-spacing residual ---------------------------
    P("\n--- A3  GRADED: price the residual the ANSWER ITSELF carries -----")
    P("    The five lines were offered at %.0f px spacing.  Reading the answer"
      % SPACING)
    P("    as 'nearest line' gives a half-spacing residual; reading it as 'that")
    P("    line' gives the full spacing.  BOTH are priced -- the weaker reading")
    P("    is not quietly discarded.")
    P("    %-26s %8s %10s %10s" % ("residual interpretation", "dU px",
                                   "err % on f", "verdict"))
    for name, dU in (("half the line spacing", SPACING / 2.0),
                     ("the full line spacing", SPACING)):
        e = interp_error(dU)
        verdict = ("CLOSES" if dU <= CLOSE_AT else
                   ("DOES NOT CLOSE" if dU >= FAIL_AT else "BETWEEN LEVELS"))
        P("    %-26s %8.1f %10.1f %10s" % (name, dU, e, verdict))
    e_half = interp_error(SPACING / 2.0)
    e_full = interp_error(SPACING)
    check(not (SPACING / 2.0 <= CLOSE_AT and SPACING <= CLOSE_AT),
          "A3 the answer does NOT land inside the closing level on both "
          "readings",
          "half-spacing %.1f px -> %.1f %%, full spacing %.1f px -> %.1f %%; "
          "the closing level is dU <= %d px"
          % (SPACING / 2.0, e_half, SPACING, e_full, CLOSE_AT))

    # ---- A4 KILL: the extreme-option problem ----------------------------
    P("\n--- A4  KILL: he chose the EXTREME member of the offered set -----")
    P("    offered columns: %s" % ", ".join(str(c) for c in CAND))
    P("    answered:        %d   <-- the LEFTMOST offered column" % ANSWER_U)
    P("    Nothing in 'line 1' excludes a true edge LEFT of 205.  The set's")
    P("    left boundary was chosen by rev 32, not by the photograph, and")
    P("    C5's own sweep started at 203 for the same arbitrary reason.")
    interior = ANSWER_U not in (min(CAND), max(CAND))
    check(interior,
          "A4 the answer is INTERIOR to the offered set, so the set "
          "bracketed it",
          "answered %d; set spans %d-%d -- an endpoint answer leaves the "
          "interval OPEN on that side" % (ANSWER_U, min(CAND), max(CAND)))

    # ---- A5 KILL: price the unbounded side ------------------------------
    P("\n--- A5  KILL: how much does f move for columns LEFT of the set? --")
    P("    %8s %10s %12s" % ("far end u", "f", "vs u = 205"))
    span = []
    for u in (185.0, 190.0, 195.0, 200.0, 205.0):
        f = f_at(u)
        span.append(f)
        P("    %8.1f %10.4f %11.1f %%" % (u, f, 100.0 * (f - f0) / f0))
    swing_left = 100.0 * (max(span) - min(span)) / min(span)
    P("    a 20 px reach to the LEFT -- the same order as rev 31's own ~29 px")
    P("    blob -- moves f by %.1f %%." % swing_left)
    check(swing_left < 10.0,
          "A5 f is stable against an unbounded left side",
          "f swings %.1f %% over 20 px of reach that the answer does not "
          "exclude" % swing_left)

    # ---- A6/A7: THE THIRD COLUMN, added after the owner answered Q1b ----
    P("\n--- A6  KILL: WHAT DID THE GRADING ACTUALLY COVER? ---------------")
    P("    P1b perturbs THE FAR END ONLY.  The cross-ratio needs FOUR")
    P("    collinear points and C3 measured only TWO of them (post 365.5,")
    P("    hoop 485.0).  The third, the FAR STRUT, is carried in C5 as a")
    P("    hard-coded strut_u = %.1f whose own print labels it '(blob)'."
      % STRUT_U)
    P("    u %.0f is ALSO rev 32's candidate line 4 -- the strut column sits"
      % STRUT_U)
    P("    INSIDE the same u 203-232 superposition as the far end.  No")
    P("    revision has asked about it and no revision has graded it.")
    strut_is_measured = False       # C3 measured two columns; this is not one
    check(strut_is_measured,
          "A6 every column the estimator consumes has been graded",
          "the far strut at u %.0f is hard-coded, self-labelled '(blob)', "
          "and lies inside the same superposition as the far end" % STRUT_U)

    P("\n--- A7  KILL: grade the FAR STRUT, far end held at the answer ----")
    P("    %8s %10s %12s" % ("strut u", "f", "err % vs base"))
    for s in (220.0, 224.0, 228.0, 232.0, 236.0):
        X = xratio(ANSWER_U, s, POST_U, HOOP_U)
        fs = f_from_X(X)
        P("    %8.1f %10.4f %11.1f %%" % (s, fs, 100.0 * (fs - f0) / f0))

    def f_strut(s):
        return f_from_X(xratio(ANSWER_U, s, POST_U, HOOP_U))

    v4 = [f_strut(s) for s in (224.0, 228.0, 232.0)]
    v8 = [f_strut(s) for s in (220.0, 228.0, 236.0)]
    sw4 = 100.0 * (max(v4) - min(v4)) / min(v4)
    sw8 = 100.0 * (max(v8) - min(v8)) / min(v8)
    P("    +-4 px on the STRUT ALONE swings f by %.1f %%" % sw4)
    P("    +-8 px on the STRUT ALONE swings f by %.1f %%" % sw8)
    P("    the FAR END's published levels are %.1f %% at 4 px, %.1f %% at 8 px"
      % (interp_error(4), interp_error(8)))
    P("    -- SO THE UNGRADED COLUMN IS THE MORE SENSITIVE OF THE TWO.")
    check(sw4 <= interp_error(4),
          "A7 the strut is no more sensitive than the graded far end",
          "strut +-4 px -> %.1f %% vs far end +-4 px -> %.1f %%"
          % (sw4, interp_error(4)))

    # ---- ruling ---------------------------------------------------------
    P("\n" + "=" * 74)
    P("RULING -- ON BOTH ANSWERS")
    P("=" * 74)
    P("  f at the answered column is %.4f of the bar's half-width." % f0)
    P("")
    P("  WHAT THE TWO ANSWERS DID CLOSE, said first because it is real:")
    P("    A4 and A5 FAILED on the Q1 answer alone -- he chose the SET'S")
    P("    ENDPOINT, leaving the interval open to the left, where 20 px of")
    P("    reach moves f by %.1f %%.  Q1b BOUNDED THAT SIDE: [stated] the end"
      % swing_left)
    P("    is AT line 1, not left of it.  With the left side closed the")
    P("    residual is the line spacing alone -- %.1f px on the stronger"
      % (SPACING / 2.0))
    P("    reading -> %.1f %%, INSIDE the published closing level of dU <= %d"
      % (e_half, CLOSE_AT))
    P("    px.  ON THE FAR END, THE OWNER CLOSED IT.  That is not hedged.")
    P("")
    P("  WHY THE ROUTE STILL DOES NOT CLOSE -- A6 AND A7, and this was NOT")
    P("  anticipated by me or by any prior revision:")
    P("    THE GRADING ONLY EVER COVERED ONE OF THE FOUR COLUMNS.  P1b")
    P("    perturbs the far end.  C3 measured the post and the hoop.  The")
    P("    FAR STRUT at u %.0f was never measured and never graded -- it is"
      % STRUT_U)
    P("    hard-coded, its own print calls it '(blob)', and u %.0f is rev"
      % STRUT_U)
    P("    32's candidate line 4, INSIDE the same superposition as the far")
    P("    end.  Graded now: +-4 px on the strut swings f by %.1f %% against"
      % sw4)
    P("    the far end's %.1f %% for the same move.  THE UNGRADED COLUMN IS"
      % interp_error(4))
    P("    THE MORE SENSITIVE OF THE TWO, so bounding the far end -- which")
    P("    cost two revisions and two questions -- does not control the")
    P("    answer.")
    P("")
    P("  THIS IS REV 32'S OWN RULE FIRING AGAIN: a control that fails can")
    P("  hide the defects downstream of it.  C5 failed on the far end for")
    P("  two revisions, so nobody looked at what else it consumed.")
    P("")
    P("  AND THE PRE-COMMITMENT WAS ONLY HALF RIGHT -- SAID PLAINLY.")
    P("  It asserted ~%.0f px of residual and no close, on the far end." % SPACING)
    P("  On the HALF-spacing reading that residual is %.1f px -> %.1f %%,"
      % (SPACING / 2.0, e_half))
    P("  INSIDE the closing level -- so the reason given was wrong even")
    P("  where the verdict was right.  The verdict survives on A6/A7, which")
    P("  are about a DIFFERENT COLUMN ENTIRELY.  A PRE-COMMITMENT IS A PROBE")
    P("  TOO, and this one was both under-specified AND aimed at the wrong")
    P("  term.")
    P("")
    P("  THE POST STAYS UNBUILT.  No f is published as a build value.")
    P("  NOT CLAIMED: that the strut is wrong, or that %.1f is a bad value."
      % STRUT_U)
    P("  The claim is only that NOTHING HAS EVER MEASURED IT, and the")
    P("  estimator is more sensitive to it than to the column two")
    P("  revisions were spent on.")
    P("")
    P("  WHAT WOULD CLOSE IT NOW, in order of value:")
    P("    1. a square-on frame of the FRONT -- collapses the whole problem")
    P("    2. the FAR STRUT's column, to the same standard the far end now")
    P("       has: an owner reading plus a bound.  It is the only remaining")
    P("       ungraded term, and it is the sensitive one.")
    P("    3. nothing else.  Do not rebuild the cross-ratio algebra; P1")
    P("       shows it is exact to 3.55e-15 and that was never the problem.")

    P("\nCONTROLS: %d checked, %d FAILED" % (7, len(FAIL)))
    for f_ in FAIL:
        P("   FAILED: %s" % f_)
    if FAIL:
        P("")
        P("EXIT CODE 1 IS THE INTENDED RESULT.  A4-A7 are KILL controls:")
        P("they ask whether the answer CLOSES the route.  It does not.  A")
        P("green run would have meant the post could be built this revision.")
        P("Do not 'fix' them by widening a tolerance.")
        sys.exit(1)


if __name__ == "__main__":
    main()
