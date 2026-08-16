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

    # ---- ruling ---------------------------------------------------------
    P("\n" + "=" * 74)
    P("RULING")
    P("=" * 74)
    P("  f at the answered column is %.4f of the bar's half-width." % f0)
    P("  THE ROUTE DOES NOT CLOSE, and it does not close for TWO independent")
    P("  reasons, either of which is sufficient:")
    P("    (1) the residual the answer carries -- %.0f px on the weaker" % SPACING)
    P("        reading, %.1f px on the stronger -- straddles the published"
      % (SPACING / 2.0))
    P("        closing level of dU <= %d px.  This is what was PRE-COMMITTED."
      % CLOSE_AT)
    P("    (2) the answer is the SET'S ENDPOINT, so the interval is open to")
    P("        the left, and 20 px of reach there moves f by %.1f %%."
      % swing_left)
    P("  (2) IS THE STRONGER FINDING AND IT WAS NOT ANTICIPATED.  A tighter")
    P("  answer among the SAME five lines could have satisfied (1); nothing")
    P("  inside that set can satisfy (2).")
    P("")
    P("  AND THE PRE-COMMITMENT WAS ONLY HALF RIGHT -- SAID PLAINLY.")
    P("  It asserted ~7 px of residual and no close.  On the HALF-spacing")
    P("  reading the residual is %.1f px -> %.1f %%, which is INSIDE the"
      % (SPACING / 2.0, e_half))
    P("  closing level, so criterion (1) alone would have closed the route.")
    P("  The pre-commitment named a residual without naming which reading of")
    P("  it applied, and the two disagree.  The route survives on A4/A5, NOT")
    P("  on the reason that was pre-committed.  A PRE-COMMITMENT IS A PROBE")
    P("  TOO, and this one was under-specified.")
    P("")
    P("  THE POST STAYS UNBUILT.  No f is published as a build value.")
    P("  NOT CLAIMED: that the end is left of 205.  He may mean exactly 205.")
    P("  The finding is that THE QUESTION CANNOT DISTINGUISH THE TWO, and")
    P("  that is a defect of the option set, which rev 33 built.")
    P("")
    P("  WHAT WOULD CLOSE IT, unchanged and now sharper: a square-on frame of")
    P("  the FRONT of the vehicle.  Failing that, ONE bounded question --")
    P("  'is the end AT line 1, or LEFT of it?' -- converts the open interval")
    P("  into a closed one and is the only cheap move left.")

    P("\nCONTROLS: %d checked, %d FAILED" % (5, len(FAIL)))
    for f_ in FAIL:
        P("   FAILED: %s" % f_)
    if FAIL:
        P("")
        P("EXIT CODE 1 IS THE INTENDED RESULT.  A4 and A5 are KILL controls:")
        P("they ask whether the answer CLOSES the route.  It does not.  A")
        P("green run would have meant the post could be built this revision.")
        P("Do not 'fix' them by widening a tolerance.")
        sys.exit(1)


if __name__ == "__main__":
    main()
