# probe_rev73_tailboard.py -- rev 73.  THE TAIL BOARD'S TILT, ON ONE RULER.
#
# WHY THIS EXISTS.  HANDOFF_CARRIERS.md sec 0.05 item 3 has asked since rev 62 for
# "the angle and chord re-measured ON ONE RULER and moved together", because
# F165's table mixes THREE:
#     the CONSTANT      TB_TILT_DEG = 38.0, the principal axis in XZ
#     F165's "BUILT"    38.40 deg, the BOUNDING-BOX DIAGONAL, which carries the
#                       board's own thickness TB_T and its rounded corners
#     F165's "PHOTO"    28.0 deg, read along the panel's TOP EDGE
# Rule 38: two sides of a ratio must share a ruler.  Nothing in this tree had
# ever measured the photographed angle against the ruler the CONSTANT uses.
#
# HOW THE RULER IS MADE HONEST, AND IT IS THE WHOLE POINT OF THE FILE.
# `studio.views()["side"]` is ORTHOGRAPHIC -- `loc=(0,26,1.52) tgt=(0,0,1.52)
# ortho=5.90` -- and its pixels are square (5.90 m over 1600 px across, and the
# same metres per pixel down).  So in `out/*_side.png` an angle in the vehicle's
# XZ plane PROJECTS TRUE.  That makes the render a KNOWN ANSWER: `STATE.md`
# publishes `tail board pose ... angle 38.0 deg -- ruler = PRINCIPAL AXIS in XZ`,
# and any image detector worth using must recover it FROM THE PIXELS.
# Both detectors below are calibrated that way BEFORE either is pointed at a
# photograph (rule 3, rule 42).
#
# READ THIS PROBE'S OWN SUMMARY LINE, NEVER ITS EXIT CODE (rule 9).
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "probe_scratch")

# ---- the model's own answer, on the ruler audit.py uses.  NOT typed as a
# target: it is re-read off STATE.md so it cannot drift from the mesh silently.
def state_angle():
    p = os.path.join(HERE, "STATE.md")
    if not os.path.exists(p):
        return None
    for ln in open(p):
        if "tail board pose" in ln and "angle" in ln:
            for tok in ln.replace(",", " ").split():
                pass
            import re
            m = re.search(r"angle\s+([0-9.]+)\s*deg", ln)
            if m:
                return float(m.group(1))
    return None

# ---- ref_side.jpg's own datum.  cream_rms.py carries a rev-16 fit of the DRIP
# RAIL, rms 0.067 px over n = 83:   v = -0.04409 u + 332.301
# That line is the vehicle's own near-horizontal in this frame, so it is what
# converts an IMAGE angle to a WORLD one without a camera model.
DRIP_SLOPE = -0.04409          # dv/du, from cream_rms.py -- NOT re-typed metres
RAKE_MM_PER_M = 17.75          # STATE.md: "rake 17.75 mm/m (locked 17.75)"

def camera_offset_deg():
    """how much this frame EXAGGERATES rise-toward-the-tail, in degrees.

    The drip rail is not horizontal on the vehicle either -- the body is raked
    NOSE-DOWN, so walking from the nose to the tail it RISES.  Nose is at frame
    left in ref_side.jpg and in the `side` render alike, so both senses agree
    and the difference is what the camera adds."""
    img = np.degrees(np.arctan(abs(DRIP_SLOPE)))
    world = np.degrees(np.arctan(RAKE_MM_PER_M / 1000.0))
    return img - world, img, world


def dom_edge_peaks(lum, magmin=16.0, ntop=3, nbin=720, smooth=3.0, sep=8.0):
    """the dominant EDGE directions in a window, weighted by gradient strength.

    Segmentation-free ON PURPOSE.  The board and the wall behind it in
    ref_side.jpg have the SAME brightness -- measured, window u870..975
    v195..300: wall and board both sit in lum 170..220 -- so a silhouette
    threshold cannot separate them and a principal-axis fit has nothing to fit.
    What IS separable is that the board's edges are long and straight and the
    wall's texture is not."""
    gy = ndimage.sobel(lum, axis=0); gx = ndimage.sobel(lum, axis=1)
    mag = np.hypot(gx, gy); k = mag > magmin
    if k.sum() < 200:
        return None, None, None, 0
    ang = (np.degrees(np.arctan2(-gy, gx)) + 90.0) % 180.0
    h, e = np.histogram(ang[k], bins=nbin, range=(0, 180), weights=mag[k])
    h = ndimage.gaussian_filter1d(h, smooth, mode="wrap")
    tops, used = [], []
    for i in np.argsort(h)[::-1]:
        c = 0.5 * (e[i] + e[i + 1])
        if any(abs(c - u) < sep or abs(c - u) > 180.0 - sep for u in used):
            continue
        used.append(c); tops.append((float(c), float(h[i])))
        if len(tops) >= ntop:
            break
    return tops, ang, mag, int(k.sum())


def silhouette_angle(sel, opens=3, minpx=200):
    """principal axis of the most ELONGATED blob, after an opening that removes
    the STAY.  Watched: the stay is ~2 px wide and the board ~10, so an opening
    of 3 drops the stay and keeps the board.

    *** ELONGATION, NOT AREA, AND THE FIRST CUT OF THIS FUNCTION USED AREA AND
    WAS WRONG.  In the `side` render's tail window the ROOF DOME is the larger
    blob -- 4016 px against the board's 2556 -- so "largest" selected the roof
    and T1 reported 123.17 deg against a known 38.0.  The control caught it
    before any photograph was touched, which is what the control is for.
    Elongation is also the POSE-FREE choice (rule 35): a blade is a blade at
    any angle, whereas "the big one" encodes what else happens to be in frame.
    Measured on out/r73_side.png, BEFORE the opening: roof dome 4016 px,
    board 2556 px -- which is the stage the wrong selection compared.
    AFTER it, T1's own live row prints the board at 2305 px, L/W 16.3;
    the dome's L/W is 1.5.  Say which stage a px figure is from. ***"""
    st = ndimage.generate_binary_structure(2, 1)
    op = ndimage.binary_opening(sel, structure=st, iterations=opens)
    if op.sum() < minpx:
        return None
    lab, n = ndimage.label(op)
    best = None
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < minpx:
            continue
        P = np.stack([xs, ys]).astype(float); P -= P.mean(axis=1, keepdims=True)
        ev, evec = np.linalg.eigh(np.cov(P))
        if ev.min() <= 0:
            continue
        el = float(np.sqrt(ev.max() / ev.min()))
        v = evec[:, np.argmax(ev)]
        ang = float(np.degrees(np.arctan2(-v[1], v[0])) % 180.0)
        if best is None or el > best[0]:
            best = (el, ang, int(len(xs)))
    if best is None:
        return None
    return best[1], best[2], best[0]


def paint(win, marks, out, committed=True):
    """RULE 8's paint.  `committed=False` writes to /tmp instead of the tracked
    probe_scratch/.

    *** F297, THIRD OCCURRENCE, AND THIS FILE CAUSED IT.  F297 fixed exactly
    this in probe_rev67_nose.py and its own ceiling said THIS probe had not
    been audited for the same shape -- and it had it.  The render paint was
    written unconditionally to a TRACKED file while the frame is chosen as the
    alphabetically-last out/*_side.png, so the moment rev 74 renders
    `T1_PFX=r74` the artefact changes, `verify_clone.sh` runs this probe, and
    the NEXT run fails `modified tracked files` naming an innocent file.
    The committed artefact is now written ONLY when the frame is the one it was
    committed from; any other frame paints to /tmp and the print says so. ***"""
    ov = np.clip(win.copy(), 0, 255)
    for sel, col in marks:
        ov[sel] = col
    d = SCRATCH if committed else "/tmp"
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, out)
    Image.fromarray(ov.astype("uint8")).save(path)
    return path


def main():
    checks, fails, absent = [], [], []

    def ck(name, ok, detail):
        checks.append(name)
        if not ok:
            fails.append(name)
        print("  %s %s\n       %s" % ("PASS" if ok else "FAIL", name, detail))

    truth = state_angle()
    if truth is None:
        print("NO STATE.md -- the model's own angle is unavailable; nothing "
              "may be calibrated against it (rule 37).")
        return 2
    print("  the MODEL's angle, re-read off STATE.md (ruler = principal axis "
          "in XZ): %.2f deg" % truth)

    # ---------------------------------------------------- the render controls
    #
    # *** REV 77: THIS PROBE NOW TAKES AN OPTIONAL FRAME, AND THAT IS A REPAIR
    # OF A NAMED FINDING. *** F324 recorded that `verify_clone.sh`'s verdict
    # depends on which `out/*_side.png` happens to be alphabetically last,
    # "because the probe takes no argument and reads that frame", and F316's
    # rule is NAME THE FRAME.  A probe that cannot be pointed at a frame cannot
    # be used to measure a distribution ACROSS frames, which is exactly what
    # F324 left outstanding.  The bare behaviour is UNCHANGED -- `verify_clone`
    # calls it with no argument and gets the same frame it always got -- so
    # this adds an address without moving any verdict.
    ren = None
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        ren = sys.argv[1]
        if not os.path.exists(ren):
            print("NO SUCH FRAME: %s -- out/ is untracked and does not exist "
                  "on a clone, so nothing was measured (rule 37)." % ren)
            print("-" * 78)
            print("  0 checked, 0 FAILED, 2 ABSENT  --  named frame absent")
            return 2
    else:
        for cand in sorted(os.listdir(os.path.join(HERE, "out"))
                           if os.path.isdir(os.path.join(HERE, "out")) else []):
            if cand.endswith("_side.png") and "raw" not in cand:
                ren = os.path.join(HERE, "out", cand)
    if ren is None:
        print("NO SIDE RENDER in out/ -- out/ is untracked and starts EMPTY. "
              "Both controls are ABSENT and the photograph row below CANNOT be "
              "calibrated, so it does not run either (rule 37).")
        print("-" * 78)
        print("  0 checked, 0 FAILED, 2 ABSENT  --  no side render")
        return 2
    print("  the render being used as the KNOWN ANSWER: %s"
          % os.path.basename(ren))

    a = np.asarray(Image.open(ren).convert("RGB")).astype(float)
    RW = (1230, 1520, 330, 500)
    rwin = a[RW[2]:RW[3], RW[0]:RW[1]]
    rlum = rwin.mean(axis=2)

    sil = silhouette_angle(rlum < 246)
    ck("T1 the SILHOUETTE detector recovers the mesh's own angle from the "
       "render's pixels (the ruler is calibrated, not assumed)",
       sil is not None and abs(sil[0] - truth) < 0.5,
       "reads %.3f deg against STATE.md's %.2f (%+.3f), %d px, elongation "
       "%.1f, after an opening of 3 that drops the stay.  Window u%d..%d "
       "v%d..%d, PAINTED."
       % (sil[0], truth, sil[0] - truth, sil[1], sil[2],
          RW[0], RW[1], RW[2], RW[3])
       if sil else "no blade-like blob found")

    tops, rang, rmag, rn = dom_edge_peaks(rlum)
    bias = tops[0][0] - truth if tops else float("nan")
    ck("T2 the GRADIENT detector recovers it too, and its bias is MEASURED "
       "rather than assumed zero",
       tops is not None and abs(bias) < 1.5,
       "dominant edge %.2f deg against %.2f -> bias %+.2f deg.  %d px over "
       "threshold.  This bias is SUBTRACTED from the photograph below; it is "
       "not a fudge, it is the same detector reading a known answer."
       % (tops[0][0], truth, bias, rn) if tops else "no edges found")

    # THE KILL (rule 3).  Rotate the render by a KNOWN angle and require the
    # detector to follow it.  A detector that reports the same number whatever
    # the input is not measuring anything.
    # THE KILL IS A LADDER, NOT ONE RUNG -- rev 73, F300.  One rung passed a
    # bar of |moved-rot| < 1.0 and was quoted as validating the +0.62 bias
    # SUBTRACTION two rows later.  A rule-17 adversary swept it and the
    # detector turns out to have a GAIN below 1, not a constant offset, which
    # is a different error model and invalidates subtracting a constant.
    lad = []
    for rot in (-7.0, 3.0, 5.0, 7.0, 10.0):
        rr = np.asarray(Image.fromarray(np.clip(rwin, 0, 255).astype("uint8"))
                        .rotate(rot, resample=Image.BICUBIC, expand=True,
                                fillcolor=(255, 255, 255))).astype(float)
        tr, _, _, _ = dom_edge_peaks(rr.mean(axis=2))
        if tr and tops:
            lad.append((rot, tr[0][0] - tops[0][0]))
    gains = [m / r for r, m in lad if r]
    gain = float(np.mean(gains)) if gains else float("nan")
    # ------------------------------------------------------------- F334, rev 77
    # THE -7.0 RUNG IS BELOW ITS OWN MEASURED FLOOR AND NO LONGER GATES.
    # MEASURED on FIVE renders of ONE tree at rev 77, no source change between
    # any of them, each read BY NAME (the probe took no argument until rev 77,
    # which is why this could not be measured before).  Per-rung residual sd:
    #     rung  -7.0   sd 1.282   range 2.500   <- 4x to 11x every other rung
    #     rung  +3.0   sd 0.326   range 0.750
    #     rung  +5.0   sd 0.112   range 0.250
    #     rung  +7.0   sd 0.224   range 0.500
    #     rung +10.0   sd 0.285   range 0.750
    # A 1.5 deg bar on a rung whose own render-to-render sd is 1.282 deg is a
    # coin flip and cannot report anything about the tree -- and it was the
    # reason `verify_clone.sh`'s TOTAL depended on which side frame happened to
    # be alphabetically last (F311's disease one level deeper).  The four rungs
    # that ARE above their floor keep the bar unchanged, and MONOTONICITY --
    # which held in 5 renders of 5 -- is now required as well, so the row still
    # fails a detector that has stopped moving, which is what it exists for.
    # NOT A WIDENING: no bar was relaxed.  One rung was found to be below its
    # own noise and is now REPORTED WITHOUT GATING, labelled as such.
    T3_UNGATED = (-7.0,)
    _gated = [(r, m) for r, m in lad if r not in T3_UNGATED]
    _mono = all(lad[i][1] < lad[i + 1][1] for i in range(len(lad) - 1))
    ck("T3 KILL -- rotating the SAME frame by known angles moves the gradient "
       "detector, AND the ladder measures HOW it moves (not just that it does)",
       len(lad) >= 4 and _mono and all(abs(m - r) < 1.5 for r, m in _gated),
       "; ".join("%+.1f -> %+.2f%s" % (t[0], t[1],
                 "  [UNGATED -- BELOW ITS OWN FLOOR, sd 1.282 deg over n=5]"
                 if t[0] in T3_UNGATED else "") for t in lad)
       + ".  MEAN GAIN %.3f, NOT 1.000.  *** THIS REFUTES THE ERROR MODEL THE "
         "PHOTOGRAPH ROWS USE: a detector with a gain below 1 is pulled back "
         "toward its unrotated reading, so its +%.2f deg offset measured AT "
         "38 deg is NOT the offset at 43 deg. Subtracting it as a CONSTANT is "
         "wrong, and T5's world figure inherits that error. One rung passed a "
         "|moved-rot| < 1.0 bar and hid this (F300). ***"
         "\n       *** THIS ROW'S FLOOR, MEASURED AT REV 77 ON n=5 (F334), "
         "WITHOUT WHICH NEITHER ITS VERDICT NOR ITS GAIN IS QUOTABLE. FIVE "
         "renders of ONE tree, no source change between any of them, read the "
         "-7.0 rung at -8.75, -8.75, -6.50, -9.00, -6.50: a RANGE of 2.50 deg "
         "and sd 1.282 deg on a rung whose bar is 1.5, 2 PASS / 3 FAIL. "
         "THE INSTABILITY IS CONFINED TO THAT ONE RUNG: the other four read sd "
         "0.326 / 0.112 / 0.224 / 0.285 over the same five frames, 4x to 11x "
         "tighter, and the ladder was MONOTONIC in 5 of 5. So the honest "
         "verdict is NOT 'T3 is noise' -- it is that ONE RUNG of five is below "
         "its own floor, and it is now UNGATED rather than the bar being "
         "widened. *** AND THIS REFUTES F324's OWN 'TWO DISJOINT CLUSTERS' "
         "(retracted here, rule 13): F324 attributed -9.00/-9.00/-8.75 to rev "
         "74's tree and -7.00/-8.50/-6.50 to rev 75's, and called the "
         "difference a BUILD-dependence. ONE TREE -- this one, unchanged -- "
         "produced -9.00 AND -8.75 AND -6.50. The clusters are not disjoint "
         "and there is no evidence of build-dependence; it is one wide "
         "distribution. *** THE GAIN CLAIM IS ESTABLISHED AFTER ALL, AND REV "
         "77's FIRST DRAFT WITHDREW IT ON THE WRONG STATISTIC (retracted here, "
         "rule 13, caught by the rule-17 adversary). The gains read 0.967 / "
         "0.979 / 0.936 / 0.935 / 0.893, mean 0.942, sd 0.033, departure from "
         "1.000 = 0.0579. The first draft divided that departure by the sd of "
         "INDIVIDUALS, got 1.73, published it as '1.8 sigma' and called it 'not "
         "a result'. THE SCALE FOR A MEAN IS THE SEM, sd/sqrt(5) = 0.0150, "
         "giving 3.86 SIGMA. And excluding the -7.0 rung THIS ROW ITSELF "
         "declares unusable, the gains read mean 0.8955, departure 0.1045 -- "
         "3.13 sigma on the sd, 7.00 on the SEM. So the sub-unity gain IS "
         "established on this tree, and 'not established' was an artefact of the "
         "wrong denominator plus contamination by the ungated rung. CEILING: "
         "n = 5, ONE tree, normality unexamined. *** A "
         "HYPOTHESIS, NAMED SO IT IS NOT MISTAKEN FOR A FINDING: -7.0 is the "
         "ONLY NEGATIVE rotation in the ladder, so the instability may be about "
         "the direction of the resample -- but that is n=1 negative rung, "
         "confounded with being the largest-magnitude and the first, and it is "
         "UNTESTED. Add a -3.0 and a -10.0 rung to test it. ***" % (gain, bias)
       if lad else "no rotated reading")

    _pr = paint(rwin, [(rlum < 246, [0, 120, 255])], "rev73_tb_render.png",
                committed=os.path.basename(ren) == "r73_side.png")
    print("     render window PAINTED -> %s" % _pr)

    # ---------------------------------------------------- the photograph
    ph = os.path.join(HERE, "ref_side.jpg")
    PW = (870, 975, 195, 300)
    b = np.asarray(Image.open(ph).convert("RGB")).astype(float)
    pwin = b[PW[2]:PW[3], PW[0]:PW[1]]
    plum = pwin.mean(axis=2)
    ptops, pang, pmag, pn = dom_edge_peaks(plum)
    off, dimg, dworld = camera_offset_deg()

    if not ptops:
        print("NO EDGES in the photograph window -- nothing measured.")
        absent.append("T4 the photograph")
    else:
        world = sorted((t[0] - off - bias) for t in ptops[:2])
        marks = []
        for (c, _), col in zip(ptops[:2], ([0, 120, 255], [255, 40, 40])):
            d = np.abs(((pang - c + 90) % 180) - 90)
            marks.append(((d < 3.0) & (pmag > 16), col))
        _pp = paint(pwin, marks, "rev73_tb_photo.png")
        print("  photograph peaks (IMAGE angles): "
              + ", ".join("%.2f deg (w %.0f)" % t for t in ptops[:2]))
        print("     the drip rail is %.3f deg in this image and %.3f deg on the "
              "vehicle (rake), so the frame exaggerates rise-toward-the-tail by "
              "%.3f deg" % (dimg, dworld, off))
        print("     PAINTED -> probe_scratch/rev73_tb_photo.png -- LOOK AT IT "
              "(rule 8).  Both peaks run the WHOLE length of the board, "
              "interleaved; they are NOT a base half and a tip half.")
        # ================================================== rev 73, F300
        # T4 AND T5 USED TO REPORT A BRACKET AND TWO CONCLUSIONS FROM IT.  BOTH
        # WERE ARTEFACTS OF THIS DETECTOR'S OWN TUNING CONSTANT, AND A RULE-17
        # ADVERSARY FOUND IT AFTER THEY HAD BEEN PUBLISHED.
        #
        # `dom_edge_peaks` refuses a second peak within 8 degrees of the first.
        # The published bracket's span was EXACTLY 8.00 -- because the second
        # peak was placed at the first bin the exclusion allowed.  Swept:
        #     sep= 2  43.12 45.12 -> 41.00..43.00   38.0 inside: False
        #     sep= 4  43.12 47.62 -> 41.00..45.50   38.0 inside: False
        #     sep= 6  43.12 49.12 -> 41.00..47.00   38.0 inside: False
        #     sep= 8  43.12 35.12 -> 33.00..41.00   38.0 inside: TRUE  <- shipped
        #     sep=10  43.12 92.38 -> 41.00..90.25   38.0 inside: False
        # The histogram's TRUE ranked local maxima are 43.12 (4555), 40.12
        # (3447), 47.62 (3282), 35.12 (2201): the reported "second peak" is the
        # FOURTH strongest, and the two stronger ones were suppressed by the
        # same rule.  So this is NOT "two peaks"; it is ONE BROAD RIDGE from
        # about 35 to 48 degrees with its mode at 43.12.
        #
        # RULE 39: a gate's target is an instrument too and must be SWEPT like
        # one.  RULE 6: an interval derived from the instrument's own parameter
        # is not evidence.  The row below does the sweep and REFUSES.
        seps = (2.0, 4.0, 6.0, 8.0, 10.0, 12.0)
        verdicts, lines = [], []
        for sp in seps:
            tp, _, _, _ = dom_edge_peaks(plum, ntop=2, sep=sp)
            if not tp or len(tp) < 2:
                continue
            wl = sorted(t[0] - off - bias for t in tp[:2])
            inside = wl[0] <= truth <= wl[1]
            verdicts.append(inside)
            lines.append("sep=%4.1f -> %6.2f..%6.2f (span %5.2f)  %s inside: %s"
                         % (sp, wl[0], wl[1], wl[1] - wl[0], truth,
                            "YES" if inside else "no"))
        stable = len(set(verdicts)) == 1 and len(verdicts) > 1
        ck("T4 the photograph's BRACKET survives a sweep of the detector's own "
           "minimum-peak-separation constant (rule 39)",
           stable,
           "IT DOES NOT.  " + " | ".join(lines) + ".  *** THE PUBLISHED "
           "BRACKET 32.99..40.99 HAD A SPAN OF EXACTLY 8.00 BECAUSE 8.0 IS THE "
           "SEPARATION CONSTANT, and 38.0 falls inside at that ONE value and "
           "outside at every other.  The histogram's true ranked maxima are "
           "43.12 / 40.12 / 47.62 / 35.12 -- the reported second peak is the "
           "FOURTH strongest.  THIS IS ONE BROAD RIDGE, ~35..48 deg, mode "
           "43.12, NOT two peaks.  F296's 'the shipped 38.0 is NOT EXCLUDED' "
           "and 'F165's 28.0 is OUTSIDE' are BOTH WITHDRAWN (F300). ***")

        ck("T5 the RIDGE is reported instead, as a description rather than a "
           "bracket -- and the shipped constant sits BELOW its mode",
           True,
           "mode %.2f deg in-image -> %.2f deg world after the drip-rail "
           "correction (%.3f) and the detector bias (%.2f); the shipped "
           "TB_TILT_DEG is %.2f, i.e. %.2f deg BELOW the mode.  *** THIS IS A "
           "DESCRIPTION, NOT A MEASUREMENT, AND IT LICENSES NOTHING.  The bias "
           "subtraction is itself refuted by T3 (see the ceiling below), and a "
           "ridge mode is not an angle of a board. ***"
           % (ptops[0][0], ptops[0][0] - off - bias, off, bias, truth,
              (ptops[0][0] - off - bias) - truth))

    print("-" * 78)
    print("  CEILINGS, STATED (rule 12).")
    print("  * THE PHOTOGRAPH ROWS DO NOT MEASURE THE BOARD'S ANGLE, AND THE")
    print("    FIRST VERSION OF THIS FILE SAID THEY DID (F300).  T4's sweep and")
    print("    T3's ladder are both refutations of THIS PROBE's own earlier")
    print("    output: the bracket was its separation constant, and the bias")
    print("    it subtracts has a GAIN, not a constant offset.")
    print("  * WHAT SURVIVES IS THE RENDER-SIDE CALIBRATION (T1/T2), which is")
    print("    real and reusable: an XZ angle projects TRUE in the ortho `side`")
    print("    view, and two independent detectors recover the mesh's own")
    print("    figure from the pixels.")
    print("  * ONE FRAME.  The board spans ~100 px in ref_side.jpg; this is a")
    print("    TWO-SIGNIFICANT-FIGURE measurement and is quoted as a bracket.")
    print("  * THE TWO PEAKS ARE NOT ASSIGNED.  They are 8 deg apart and both")
    print("    run the board's whole length.  The likeliest reading is the")
    print("    board's NEAR and FAR long edges projecting differently -- the")
    print("    same depth-plane ambiguity t1_shell.tail_board's own comment")
    print("    already carries for the width and the stay -- but rev 73 could")
    print("    NOT assign them, and did not pick one.")
    print("  * THE CAMERA CORRECTION IS A ROLL, APPLIED AS A CONSTANT.  A")
    print("    perspective camera does not add a constant angular offset, and")
    print("    the drip-rail fit's own u-range is the body, not the board.")
    print("  * IT LICENSES NO GEOMETRY CHANGE -- and now for a STRONGER")
    print("    reason than the first version gave: not `38.0 is inside a wide")
    print("    bracket`, but `this frame and this detector do not constrain the")
    print("    angle at all`.  F165's 28.0 is NOT shown to be outside anything.")
    print("-" * 78)
    print("  %d checked, %d FAILED%s%s"
          % (len(checks), len(fails),
             (", %d ABSENT" % len(absent)) if absent else "",
             ("  --  " + "; ".join(fails + absent)) if (fails or absent) else ""))
    print("=" * 78)
    return 1 if fails else (2 if absent else 0)


if __name__ == "__main__":
    sys.exit(main())
