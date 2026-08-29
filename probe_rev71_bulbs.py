# probe_rev71_bulbs.py -- rev 71.  THE FESTOON BULBS, RENDER AGAINST PHOTOGRAPH.
#
# THE DEFECT THIS EXISTS FOR HAS BEEN IN t1_mats.py's OWN COMMENT SINCE REV 8:
# *"the drip-rail bulb string renders unlit pearl white.  In both in-service
# photographs the bulbs are LIT and read warm"*.  Rev 61 answered it with TWO
# ABLATION SWITCHES (T1_BULB_STR, T1_BULB_BASEV -- F134) and a NULL HYPOTHESIS:
# *"the emission contributes nothing at studio exposure and we are seeing the
# base lit by the cyclorama"*.  TEN REVISIONS AND NEITHER SWITCH WAS EVER RUN.
#
# REV 71 RAN THEM, AND THE NULL IS REFUTED.  Ablating the emission moves the
# bead: sat 0.0417 -> 0.0251 and V 0.9487 -> 0.8516.  The emission ARRIVES.
# What it cannot do is COLOUR the bead: at strength 9 the bead sits at V 0.95,
# the top of the tone curve, where the view transform's path-to-white takes the
# chroma out.  And the envelope is not the swamp either -- driving it 20x darker
# (T1_BULB_BASEV 1.0 -> 0.05) moves saturation only 0.0417 -> 0.0494.
#
# WHY THE WINDOW IS CUT THE WAY IT IS, AND IT COST TWO WRONG ONES (rule 8).
#   FIRST CUT, DISCARDED: bright-and-warm pixels in the crop.  PAINTED, and it
#     selected THE WALL AND THE MURAL BEHIND THE BUS -- rev 70's exact defect.
#   SECOND CUT, DISCARDED: an 8 px corridor along the board's edge.  PAINTED,
#     and it is mostly BOARD CREAM: the ablation moved its mean by 0.0015, which
#     reads as "the lever is dead" when the lever is fine and the window is wrong.
#   THIS CUT: inside the corridor, the BRIGHTEST 25 % -- the bead cores.  The
#     pick is by BRIGHTNESS and the report is SATURATION, so it is not circular
#     (rule 6), and the SAME rule runs on both sides (rule 38).
#
# CEILING, AND IT IS BINDING.  Painted and looked at, BOTH windows still contain
# some of the board's own cream face, which DILUTES both sides toward neutral.
# The photographed 0.1839 is therefore a LOWER BOUND on the real bead
# saturation, and the deficit below is a LOWER BOUND on the real deficit.  The
# photograph's brightest beads are additionally R-CLIPPED (t1_shell.
# tail_board_edge's own note: they read (255,251,99)), which desaturates them
# further.  This row says the render's beads are TOO NEUTRAL.  It does NOT say
# by how much, and it is NOT a claim that any particular constant is right.
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "probe_scratch")

# The board's bulb edge, in each frame's own crop coordinates.  These are PICKS,
# not derived numbers, and the painted PNGs below are how they were checked.
PHOTO = ("ref_side.jpg", (855, 180, 1010, 320), (30., 114., 146., 8.), +1)
RENDER_BOX, RENDER_LINE, RENDER_SIDE = (1240, 330, 1560, 520), (60., 150., 217., 30.), -1
FRAC = 0.25


def beads(path, box, line, side, tag, frac=FRAC):
    """The bead cores in one frame.  PAINTS its window BEFORE it returns a
    number (rule 8) and returns None if the window is empty (rule 37)."""
    a = np.asarray(Image.open(path).convert("RGB")).astype(float)
    a = a[box[1]:box[3], box[0]:box[2]]
    h, w, _ = a.shape
    yy, xx = np.mgrid[0:h, 0:w]
    ax, ay, bx, by = line
    dx, dy = bx - ax, by - ay
    L = np.hypot(dx, dy)
    t = ((xx - ax) * dx + (yy - ay) * dy) / L ** 2
    d = ((xx - ax) * dy - (yy - ay) * dx) / L
    cor = (t > 0.05) & (t < 0.98) & (d * side > 1.0) & (d * side < 8.0)
    if cor.sum() < 50:
        return None
    V = a.max(2)
    m = cor & (V >= np.percentile(V[cor], 100 * (1 - frac)))
    if m.sum() < 10:
        return None
    px = a[m]
    sat = float(((px.max(1) - px.min(1)) / np.maximum(px.max(1), 1e-6)).mean())
    os.makedirs(SCRATCH, exist_ok=True)
    o = a.copy()
    o[cor] = o[cor] * 0.55 + np.array([0, 0, 150]) * 0.45
    o[m] = [0, 255, 0]
    Image.fromarray(o.astype("uint8")).resize((w * 5, h * 5), Image.NEAREST).save(
        os.path.join(SCRATCH, "rev71_beads_%s.png" % tag))
    return sat, float((px.max(1) / 255).mean()), int(m.sum())


def main():
    checks, fails = [], []

    def ck(name, ok, detail):
        checks.append(name)
        print("  [%s] %s" % ("PASS" if ok else "FAIL", name))
        print("       " + detail)
        if not ok:
            fails.append(name)

    frame = None
    for a in sys.argv[1:]:
        if a.endswith(".png"):
            frame = a
    abl = os.environ.get("T1_BULB_ABLATED_FRAME")

    p = beads(os.path.join(HERE, PHOTO[0]), PHOTO[1], PHOTO[2], PHOTO[3], "photo")
    if p is None:
        print("  B1 NO PHOTOGRAPH WINDOW -- nothing measured")
        raise SystemExit(3)
    ck("B1 the PHOTOGRAPHED bead string has real chroma  [PAINTED to "
       "probe_scratch/rev71_beads_photo.png BEFORE the number was read]",
       p[0] > 0.10,
       "ref_side.jpg, brightest %d %% of a corridor on the board's bulb edge: "
       "n=%d  saturation %.4f  V %.4f.  A LOWER BOUND -- the window still holds "
       "some board cream and the brightest beads are R-clipped"
       % (int(FRAC * 100), p[2], p[0], p[1]))

    if frame is None:
        print("\n  NO FRAME GIVEN -- B2 and B3 (the RENDER rows) DID NOT RUN.")
        print("  They are ABSENT, not passed.  Pass a side frame:")
        print("      python3 probe_rev71_bulbs.py out/r71_side.png")
        print("\n  1 checked, 0 FAILED -- AND THE RENDER ROWS DID NOT RUN")
        raise SystemExit(3)

    r = beads(os.path.join(HERE, frame) if not os.path.isabs(frame) else frame,
              RENDER_BOX, RENDER_LINE, RENDER_SIDE, "render")
    if r is None:
        print("  B2 NO BEAD WINDOW IN %s -- nothing measured (rule 37)" % frame)
        raise SystemExit(3)
    ck("B2 the RENDER's bead string is as chromatic as the photograph's",
       r[0] >= 0.60 * p[0],
       "%s: n=%d  saturation %.4f  V %.4f, against the photograph's %.4f -- "
       "%.1fx too neutral.  Both sides read by ONE rule in their own image, so "
       "exposure does not enter (rule 38).  The bar is 60 %% of a LOWER BOUND, "
       "so passing it would still not mean the beads are right"
       % (os.path.basename(frame), r[2], r[0], r[1], p[0], p[0] / max(r[0], 1e-6)))

    if abl and os.path.exists(abl):
        q = beads(abl, RENDER_BOX, RENDER_LINE, RENDER_SIDE, "ablated")
        if q is not None:
            ck("B3 KILL -- this window reads THE BULBS, not the board.  With "
               "T1_BULB_STR=0 the same statistic must MOVE",
               abs(q[0] - r[0]) > 0.005 or abs(q[1] - r[1]) > 0.02,
               "emission ablated: saturation %.4f (was %.4f), V %.4f (was %.4f). "
               "A window on the board's cream moves by ~0.0015 under this "
               "ablation and that is how the second cut of this window was "
               "caught (rule 8, rule 36)" % (q[0], r[0], q[1], r[1]))
    else:
        print("  [ -- ] B3 KILL DID NOT RUN: set T1_BULB_ABLATED_FRAME to a side")
        print("       frame rendered with T1_BULB_STR=0.  ABSENT, not passed.")

    print("\n  %d checked, %d FAILED%s" % (len(checks), len(fails),
          "  --  " + "; ".join(fails) if fails else ""))
    raise SystemExit(1 if fails else 0)


if __name__ == "__main__":
    main()
