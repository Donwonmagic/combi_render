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


def dom_edge_peaks(lum, magmin=16.0, ntop=3, nbin=720, smooth=3.0):
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
        if any(abs(c - u) < 8 or abs(c - u) > 172 for u in used):
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
    Measured on out/r73_side.png: board L/W 16.1, roof dome L/W 1.5. ***"""
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


def paint(win, marks, out):
    ov = np.clip(win.copy(), 0, 255)
    for sel, col in marks:
        ov[sel] = col
    os.makedirs(SCRATCH, exist_ok=True)
    Image.fromarray(ov.astype("uint8")).save(os.path.join(SCRATCH, out))


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
    ren = None
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
    rot = 7.0
    rr = np.asarray(Image.fromarray(np.clip(rwin, 0, 255).astype("uint8"))
                    .rotate(rot, resample=Image.BICUBIC, expand=True,
                            fillcolor=(255, 255, 255))).astype(float)
    tr, _, _, _ = dom_edge_peaks(rr.mean(axis=2))
    moved = (tr[0][0] - tops[0][0]) if (tr and tops) else float("nan")
    ck("T3 KILL -- rotating the SAME frame by a known 7.00 deg moves the "
       "gradient detector by 7.00 deg",
       tr is not None and abs(moved - rot) < 1.0,
       "detector moved %+.2f deg for a %+.2f deg rotation (residual %+.2f).  "
       "WATCHED: without this row the detector could be reporting a constant."
       % (moved, rot, moved - rot))

    paint(rwin, [(rlum < 246, [0, 120, 255])], "rev73_tb_render.png")

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
        paint(pwin, marks, "rev73_tb_photo.png")
        print("  photograph peaks (IMAGE angles): "
              + ", ".join("%.2f deg (w %.0f)" % t for t in ptops[:2]))
        print("     the drip rail is %.3f deg in this image and %.3f deg on the "
              "vehicle (rake), so the frame exaggerates rise-toward-the-tail by "
              "%.3f deg" % (dimg, dworld, off))
        print("     PAINTED -> probe_scratch/rev73_tb_photo.png -- LOOK AT IT "
              "(rule 8).  Both peaks run the WHOLE length of the board, "
              "interleaved; they are NOT a base half and a tip half.")
        ck("T4 the shipped TB_TILT_DEG lies INSIDE the bracket the photograph "
           "supports, on the CONSTANT's own ruler",
           world[0] <= truth <= world[1],
           "the photograph brackets the world angle at %.2f..%.2f deg "
           "(midpoint %.2f, span %.2f); the shipped constant is %.2f.  "
           "*** THIS IS A NON-EXCLUSION, NOT A CONFIRMATION (rule 12): a "
           "bracket 8 deg wide cannot distinguish 38 from 35 or 41. ***"
           % (world[0], world[1], 0.5 * (world[0] + world[1]),
              world[1] - world[0], truth))
        ck("T5 F165's photographed 28.0 deg lies OUTSIDE that bracket -- the "
           "three-ruler mismatch resolves AGAINST the 28.0, not against the "
           "model",
           not (world[0] <= 28.0 <= world[1]),
           "28.0 against %.2f..%.2f -- %.2f deg outside.  F165 read it on "
           "IMG_3840.jpeg ALONG THE PANEL'S TOP EDGE, a third ruler, on a "
           "480x320 frame in which the board spans ~90 px.  ⚠ CEILING: this "
           "row does not prove 28.0 was misread; it proves it is not "
           "reproduced by THIS frame on THIS ruler."
           % (world[0], world[1], world[0] - 28.0))

    print("-" * 78)
    print("  CEILINGS, STATED (rule 12).")
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
    print("  * IT LICENSES NO GEOMETRY CHANGE.  38.0 is not excluded and")
    print("    nothing here says where inside the bracket the truth is.")
    print("-" * 78)
    print("  %d checked, %d FAILED%s%s"
          % (len(checks), len(fails),
             (", %d ABSENT" % len(absent)) if absent else "",
             ("  --  " + "; ".join(fails + absent)) if (fails or absent) else ""))
    print("=" * 78)
    return 1 if fails else (2 if absent else 0)


if __name__ == "__main__":
    sys.exit(main())
