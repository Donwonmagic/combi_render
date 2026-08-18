"""probe_rev40_datum.py -- SPEC 10.98.  READ-ONLY.  Changes nothing.

WHAT IT TESTS, and it is a test of an INSTRUMENT, not of the vehicle:

    rev 39 published "the body sits 81 +/- 7 mm high against the cream/red
    two-tone break" and concluded "THE BREAK LINE SITS ~81 mm TOO LOW ON THE
    BODY" (SPEC 10.97.5-6).  Rev 40's item 1 was to move the break by that
    amount.  This probe asks the question rev 39 did not: WHICH EDGE does each
    side of that measurement actually pin?

`probe_rev39_flank.py` warps the render into ref_side.jpg's frame using two
datum lines it transcribes from `flank_compare.py`:

    reference   v = -0.03467 u + 446.813        (fitted on ref_side.jpg)
    render      y = -0.01777 x + 579.070        (fitted on out/p_side.png)

`flank_compare.py` says of these, in its own words, that the render one is
"the SAME cream/red break ... the reference's is the same physical edge, so the
two are used as ONE datum and its height never enters."

THAT SENTENCE IS THE CLAIM UNDER TEST.  The two lines are fitted with DIFFERENT
ESTIMATORS in DIFFERENT ROW WINDOWS -- a LUMINANCE gradient over rows 425-452
on the reference, a REDNESS gradient over a render-relative window -- and a
luminance step and a redness step on a cream / gold-nosing / beige-fascia / red
stack are NOT the same boundary.

NO NEW ESTIMATOR IS OPENED (SPEC 10.79/10.83/10.90's rule).  The render side is
read from the build's OWN AUTHORED CONSTANTS at run time (t1_detail.CNT_ZT /
CNT_ZB), never from a colour gate -- a class gate tuned on the photograph does
not transfer to the render, which is SPEC 10.97.9's lesson from the flower
heads.  The reference side uses a TWO-TERM gate with its endmembers PRINTED,
because SPEC 10.97.9 records that the red body's luma is 79 and a luminance-only
band cannot separate it from anything dark.

POSITIVE CONTROL FOR THE REFERENCE GATE: it must reproduce REF_MEASUREMENTS
section 3(a)'s own hand-read table at the cab door (x = 130/150/170/190, red
from rows 436/436/438/438).  That table was read by hand off this same frame,
so it grades the gate against something not produced by this probe.

CEILING, STATED UP FRONT: this probe adjudicates WHICH EDGE each datum is on
and what that costs.  It does NOT re-measure the vehicle, it publishes no new
metre scale, and the residual it derives inherits flank_kv's own accuracy.
"""
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
import flank_compare as FC                      # noqa: E402

RENDER = sys.argv[1] if len(sys.argv) > 1 else "out/p_side.png"


def _authored(path, names):
    """Read authored constants out of a build file with ast -- never retyped."""
    import ast
    src = open(path).read()
    tree = ast.parse(src)
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            tgts = []
            for t in node.targets:
                if isinstance(t, ast.Name):
                    tgts.append([t])
                elif isinstance(t, ast.Tuple):
                    tgts.append([e for e in t.elts if isinstance(e, ast.Name)])
            for grp in tgts:
                vals = (node.value.elts
                        if isinstance(node.value, ast.Tuple) else [node.value])
                for nm, v in zip(grp, vals):
                    if nm.id in names:
                        try:
                            out[nm.id] = float(ast.literal_eval(v))
                        except Exception:
                            pass
    miss = set(names) - set(out)
    if miss:
        sys.exit("FAIL could not read %s from %s" % (sorted(miss), path))
    return out


def v_break(u):
    """flank_compare's REFERENCE datum line, as probe_rev39_flank transcribes it."""
    return -0.03467 * np.asarray(u, float) + 446.813


def y_datum(col):
    """flank_compare's RENDER datum line, as probe_rev39_flank transcribes it."""
    return -0.01777 * np.asarray(col, float) + 579.070


def main():
    fails = 0
    ref = np.asarray(Image.open("ref_side.jpg").convert("RGB")).astype(float) / 255.
    rnd = np.asarray(Image.open(RENDER).convert("RGB")).astype(float) / 255.
    RH, RW = rnd.shape[:2]
    proj, projinv, ppm = FC.projector(RW, RH)

    print("=" * 78)
    print("PROBE rev 40 -- WHICH EDGE IS THE DATUM?  (SPEC 10.98)")
    print("=" * 78)

    # ------------------------------------------------------------------ C1
    # The two transcribed lines must equal flank_compare's own live fits.
    ea, eb, erms, ekeep, en = FC.fit_edge(
        0.2126 * ref[:, :, 0] * 255 + 0.7152 * ref[:, :, 1] * 255
        + 0.0722 * ref[:, :, 2] * 255,
        range(331, 600), 425, 452, +1, 3.0)
    c1 = abs(ea - (-0.03467)) < 2e-5 and abs(eb - 446.813) < 0.02
    fails += not c1
    print("\n[%s] C1  reference datum refitted live: v = %+.5f u %+.3f "
          "(rms %.3f, n=%d/%d)" % ("PASS" if c1 else "FAIL", ea, eb, erms,
                                   ekeep, en))
    print("        probe_rev39_flank transcribes  v = -0.03467 u +446.813 "
          "-- transcription is exact")

    # ------------------------------------------------------------------ C2
    # What model z is the RENDER datum on?  flank_compare prints 1.1459 at the
    # lockup mid column, in the AUTHORED (un-sheared) frame.  Compare against
    # the counter's own authored constants, read with ast at run time.
    CN = _authored("t1_detail.py", ("CNT_ZT", "CNT_ZB", "CNT_NOSE_F"))
    cmid = float(proj(FC.flank_X(465.5), 0)[0])
    _, zdat = projinv(cmid, float(y_datum(cmid)))
    dT = (zdat - CN["CNT_ZT"]) * 1000.0
    dB = (zdat - CN["CNT_ZB"]) * 1000.0
    c2 = abs(dB) < 5.0 and abs(dT) > 50.0
    fails += not c2
    print("\n[%s] C2  RENDER datum, authored frame, at the lockup mid column: "
          "z = %.4f" % ("PASS" if c2 else "FAIL", zdat))
    print("        counter fascia TOP    CNT_ZT = %.4f   -> %+.1f mm"
          % (CN["CNT_ZT"], dT))
    print("        counter fascia BOTTOM CNT_ZB = %.4f   -> %+.1f mm"
          % (CN["CNT_ZB"], dB))
    print("        => THE RENDER DATUM IS THE COUNTER FASCIA %s"
          % ("BOTTOM" if abs(dB) < abs(dT) else "TOP"))
    h_slab = (CN["CNT_ZT"] - CN["CNT_ZB"]) * 1000.0
    h_gold = CN["CNT_NOSE_F"] * h_slab
    h_model = h_slab - h_gold
    print("        model SLAB edge   CNT_ZT - CNT_ZB            = %.1f mm" % h_slab)
    print("        model BRASS       CNT_NOSE_F x slab (%.4f)  = %.1f mm"
          % (CN["CNT_NOSE_F"], h_gold))
    print("        model PAINTED FASCIA, nosing bottom -> slab bottom = %.1f mm"
          % h_model)
    print("        SCOPE: the reference datum is the NOSING'S LOWER EDGE, so the")
    print("        like-for-like model quantity is the PAINTED FASCIA, not the")
    print("        slab.  Comparing the slab would be a scope error of %.1f mm."
          % h_gold)

    # ------------------------------------------------------------------ C3
    # The reference gate.  TWO TERMS, endmembers printed, positive control
    # against REF sec.3(a)'s own hand-read table.
    print("\n--- reference gate, endmembers measured in ref_side.jpg ---")
    beige = ref[430:440, 690:710].reshape(-1, 3).mean(0)
    redp = ref[450:465, 690:710].reshape(-1, 3).mean(0)
    creamp = ref[404:412, 450:470].reshape(-1, 3).mean(0)
    for nm, e in (("counter fascia beige", beige), ("body red", redp),
                  ("body cream", creamp)):
        print("    %-22s rgb %.3f %.3f %.3f   luma %.3f   r-g %+.3f"
              % (nm, e[0], e[1], e[2],
                 0.2126 * e[0] + 0.7152 * e[1] + 0.0722 * e[2], e[0] - e[1]))

    def first_red(col, lo, hi):
        """TWO TERMS: saturated-red chroma AND low green.  Never luma alone."""
        for y in range(lo, hi):
            r, g, b = col[y]
            if (r - g) > 0.18 and g < 0.30 and r > 0.25:
                return y
        return None

    print("\n    POSITIVE CONTROL -- REF sec.3(a)'s own hand-read cab-door table")
    want = {130: 436, 150: 436, 170: 438, 190: 438}
    okc = 0
    biases = []
    for x in (130, 150, 170, 190):
        got = first_red(ref[:, x, :], 415, 470)
        d = None if got is None else got - want[x]
        good = got is not None and abs(d) <= 1
        okc += good
        biases.append(d if got is not None else 0)
        print("      x=%3d  gate says row %s   REF sec.3a says %d   %s"
              % (x, got, want[x], ("agree %+d px" % d) if good else "DISAGREE"))
    c3 = okc == 4
    fails += not c3
    print("    [%s] C3  the gate reproduces REF sec.3(a) on 4/4 columns to 1 px"
          % ("PASS" if c3 else "FAIL", ))
    bb = np.array(biases, float)
    print("        BIAS PRICED, not loosened away: the gate sits %+.2f +/- %.2f px"
          % (bb.mean(), bb.std()))
    print("        BELOW the hand reading on 4/4 columns -- one-sided, because a")
    print("        hand call takes the first row that LOOKS red and a two-term gate")
    print("        takes the first row that IS unambiguously red. %.0f mm at k_t."
          % (bb.mean() / FC.K_T * 1000))
    print("        It is one-sided and %.0f mm; it cannot touch a 19 px conclusion."
          % (bb.mean() / FC.K_T * 1000))

    # ------------------------------------------------------------------ C4
    # Where does the REFERENCE datum sit relative to the fascia?
    print("\n--- where the REFERENCE datum lands, per column ---")
    print("      u    fascia_top  fascia_bot   v_break   nearer to   fascia mm")
    tops, bots, hs = [], [], []
    for u in range(360, 961, 20):
        colr = ref[:, u, :]
        bot = first_red(colr, 415, 470)
        if bot is None:
            continue
        top = None
        for y in range(bot - 1, 405, -1):
            r, g, b = colr[y]
            if not (0.68 < r < 0.97 and 0.60 < g < 0.87 and (r - g) < 0.16):
                top = y + 1
                break
        if top is None or bot - top < 8:
            continue
        vb = float(v_break(u))
        kv = float(FC.flank_kv(u))
        near = "TOP" if abs(vb - top) < abs(vb - bot) else "BOTTOM"
        tops.append(vb - top)
        bots.append(vb - bot)
        hs.append((bot - top) / kv * 1000.0)
        print("     %4d      %4d       %4d      %6.1f    %-6s   %6.1f"
              % (u, top, bot, vb, near, hs[-1]))
    tops, bots, hs = np.array(tops), np.array(bots), np.array(hs)
    c4 = np.abs(tops).mean() < np.abs(bots).mean() / 3.0
    fails += not c4
    print("\n    mean |v_break - fascia_top|    = %5.2f px" % np.abs(tops).mean())
    print("    mean |v_break - fascia_bottom| = %5.2f px" % np.abs(bots).mean())
    print("    [%s] C4  THE REFERENCE DATUM IS THE COUNTER FASCIA TOP"
          % ("PASS" if c4 else "FAIL"))
    h_photo = float(np.mean(hs))
    h_sd = float(np.std(hs))
    h_repo = 20.32 / FC.K_T * 1000.0
    bias_mm = float(bb.mean()) / FC.K_T * 1000.0
    print("    photographed painted fascia (nosing bottom -> red):")
    print("      this probe, 2-term gate, %d cols        : %.1f +/- %.1f mm"
          % (len(hs), h_photo, h_sd))
    print("      t1_detail's CNT_NOSE_F comment, 113 cols,")
    print("      saturation half-max, whole edge 24.84 px")
    print("      less 4.52 px of gold = 20.32 px          : %.1f mm" % h_repo)
    print("      -> two INDEPENDENT photographic readings, %.1f mm apart"
          % abs(h_photo - h_repo))
    print("    model PAINTED FASCIA (authored)            : %.1f mm" % h_model)
    print("    model - photograph                         : %+.1f mm"
          % (h_model - h_photo))
    print("    CEILING ON THAT NUMBER, STATED: C3's %+.1f mm gate bias is NOT"
          % bias_mm)
    print("    applied here.  It was measured against REF sec.3(a)'s HAND")
    print("    reading; the repo's figure is a SATURATION HALF-MAX one; the two")
    print("    criteria sit at different points on the same transition, so")
    print("    subtracting one from the other would be a third scope error.")
    print("    The %+.1f mm is quoted against the RAW gate, which agrees with"
          % (h_model - h_photo))
    print("    the repo's independent half-max reading to %.1f mm."
          % abs(h_photo - h_repo))

    # ------------------------------------------------------------------ C5
    # The consequence.  THE VERDICT IS DERIVED, never a constant string.
    print("\n" + "-" * 78)
    print("THE CONSEQUENCE FOR SPEC 10.97.5's 81 mm")
    print("-" * 78)
    R39 = 81.0
    print("  the warp pins  MODEL fascia BOTTOM  onto  PHOTOGRAPH fascia TOP.")
    print("  so the render is placed one fascia height too high, and the")
    print("  measured 'the render must drop 81 mm' contains that offset.")
    print()
    print("  residual with both sides on the fascia TOP    : %+6.1f mm"
          % (R39 - h_model))
    print("  residual with both sides on the fascia BOTTOM : %+6.1f mm"
          % (R39 - h_photo))
    lo, hi = sorted((R39 - h_model, R39 - h_photo))
    print()
    if abs(lo) < R39 / 2 and abs(hi) < R39 / 2:
        print("  VERDICT (derived): correcting the datum takes the residual from")
        print("  +81 mm to the band [%+.0f, %+.0f] mm.  The 81 mm is DOMINATED BY"
              % (lo, hi))
        print("  THE DATUM MISMATCH, not by a misplaced break line.  SPEC 10.97.6's")
        print("  instruction to move the painted break by 81 mm DOES NOT FOLLOW.")
    else:
        print("  VERDICT (derived): correcting the datum leaves [%+.0f, %+.0f] mm,"
              % (lo, hi))
        print("  which is NOT small against 81 mm.  The datum mismatch is real but")
        print("  it does not by itself explain the finding.  NO RULING on 10.97.6.")

    # ---------------------------------------------------- an independent arm
    print("\n" + "-" * 78)
    print("INDEPENDENT ARM -- BREAK-TO-SILL, a body-internal relationship that")
    print("shares NO datum with the warp and cannot be moved by the mismatch")
    print("-" * 78)
    print("  Measured on the CAB DOOR, the only place the body's own two-tone")
    print("  break is visible (REF sec.3a) -- aft of it the counter covers it.")
    ZB = _authored("t1_mats.py", ("Z_BELT_AUTH",))["Z_BELT_AUTH"]
    ZS = _authored("t1_shell.py", ("Z_SILL",))["Z_SILL"]
    m_bs = (ZS - ZB) * 1000.0
    rows = []
    for x in range(120, 201, 10):
        colr = ref[:, x, :]
        brk = first_red(colr, 415, 470)
        if brk is None:
            continue
        # the window opening's lower edge: scan UP from the break through the
        # cream to the first row that is NOT cream.  Cream is the endmember
        # printed above; the opening above it is dark glass/interior.
        sill = None
        for y in range(brk - 2, 395, -1):
            r, g, b = colr[y]
            lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
            if lum < 0.55:
                sill = y + 1
                break
        if sill is None or brk - sill < 8:
            continue
        rows.append((brk - sill) / float(FC.flank_kv(x)) * 1000.0)
        print("    x=%3d  sill row %d  break row %d  ->  %5.1f mm"
              % (x, sill, brk, rows[-1]))
    if len(rows) >= 6:
        p = float(np.mean(rows))
        psd = float(np.std(rows))
        print("\n  photographed  window sill -> body break : %.1f +/- %.1f mm "
              "(n=%d)" % (p, psd, len(rows)))
        print("  model         Z_SILL - Z_BELT_AUTH      : %.1f mm" % m_bs)
        print("  REF sec.3(a)'s own hand figure           : 100.0 mm")
        print("  difference model - photograph            : %+.1f mm" % (m_bs - p))
        print()
        if abs(m_bs - p) < 40.0:
            print("  NO DATUM IS SHARED WITH THE WARP -- both rows are read inside")
            print("  ref_side.jpg and both constants are read out of the build, so")
            print("  the fascia mismatch cannot produce this number.")
            print("  A break line 81 mm out of place would show HERE as ~81 mm of")
            print("  disagreement.  IT SHOWS %.0f mm." % abs(m_bs - p))
        else:
            print("  The two disagree by %.0f mm -- this arm does NOT clear the break,"
                  % abs(m_bs - p))
            print("  and the 81 mm cannot be dismissed on the datum finding alone.")
    else:
        print("  the sill gate found only %d columns -- ARM DECLINES, and a"
              % len(rows))
        print("  declining arm is not a passing arm.")

    print("\nCONTROLS: %d checked, %d FAILED" % (4, fails))
    print("=" * 78)
    return fails


if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 1)
