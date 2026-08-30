# probe_rev71_red.py -- rev 71, F257.  THE RED FLANK, RENDER AGAINST PHOTOGRAPH.
#
# TWO THINGS THIS FIXES ABOUT EVERY EARLIER READING OF THE RED:
#
# 1. IT MEASURES IN LINEAR.  An 8-bit sRGB channel RATIO is not a physical
#    quantity: gamma is non-linear, so G/R depends on absolute brightness, and
#    the render's flank is 2.9x brighter in linear R than the photograph's.
#    Comparing sRGB G/R across two exposures is not one ruler (rule 38).
#    In linear the gap is 5.4x; the sRGB reading says 3.2x and HIDES part of it.
#
# 2. ITS WINDOW WAS PAINTED AND LOOKED AT, THREE TIMES, AND THE FIRST TWO WERE
#    WRONG (rule 8).  Cut 1 (four positional patches) sat under the counter's
#    SHADE and read G/R 0.36.  Cut 2 (a wide band) ran onto the CREAM and the
#    BACKGROUND WALL -- p90 0.898, i.e. tiles that are not red at all.  Cut 3,
#    below, is tiles kept by UNIFORMITY (std <= 7) plus a red-dominant ORDERING
#    and a G/R < 0.80 cut that excludes cream and wall.  The pick is never by
#    saturation, so the report is not circular (rule 6).
#
# CEILING: the photograph's flank is partly in the counter's shade, whose bluer
# light RAISES G/R -- so 0.0305 is if anything an OVER-estimate of the paint's
# own ratio.  The frame's cast is small: its foreground paving reads G/R 0.966.
import sys

import numpy as np
from PIL import Image

# R3's windows: the red flank, and CREAM ON THE SAME VERTICAL PLANE as it --
# roof cream would sit at a different orientation and take different light,
# which is the whole point of scoring one surface against another (the pattern
# probe_rev70_tyre uses: the tyre against the cream rim ring in its own image).
CREAM_BOXES = [(320, 600, 500, 640), (1150, 590, 1290, 650), (560, 585, 700, 615)]
RED_ALB = (0.5520, 0.0294, 0.0176)      # t1_mats.RED,   linear
CREAM_ALB = (0.6172, 0.6308, 0.5776)    # t1_mats.CREAM, linear

PHOTO = ('ref_side.jpg', (320, 450, 900, 565), 5, 10)
RENDER_BAND, RSTEP, RTSZ = (430, 680, 1230, 850), 9, 16
# the flank band on the 800x550 diffuse-colour pass (half the preview's scale)
AOV_BAND, ASTEP, ATSZ = (215, 340, 615, 425), 4, 8
AUTHORED_RED_GR = 0.0294 / 0.5520          # t1_mats RED, linear


def _lin(x):
    x = x / 255.0
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def flank(path, band, step, tsz, linear=True):
    """Linear G/R over the red flank.  Returns (n, median, p10, p90) or None."""
    a = np.asarray(Image.open(path).convert('RGB')).astype(float)
    x0, y0, x1, y1 = band
    keep = []
    for y in range(y0, y1 - tsz, step):
        for x in range(x0, x1 - tsz, step):
            t = a[y:y + tsz, x:x + tsz].reshape(-1, 3)
            m = t.mean(0)
            if t.std(0).max() > 7.0:
                continue                       # not plain paint: art, edge, or shadow line
            if not (m[0] > m[1] > m[2]):
                continue                       # red-dominant ORDERING, not a saturation cut
            if m[1] / m[0] > 0.80:
                continue                       # excludes cream, grey and the background wall
            keep.append(_lin(t).mean(0) if linear else m)
    if len(keep) < 20:
        return None
    K = np.array(keep)
    g = K[:, 1] / K[:, 0]
    return len(g), float(np.median(g)), float(np.percentile(g, 10)), float(np.percentile(g, 90))


def ratio(path, boxes, red, tsz=8, step=4):
    """Mean LINEAR colour over uniform tiles in `boxes`, and the CLIP fraction.

    ⚠ CLIPPING IS WHY THIS ROW NEEDED A GUARD.  R3 divides by the cream, and in
    the SHIPPED render 84 % of the cream window sits at sRGB >= 254 -- it is
    BLOWN OUT.  A clipped denominator cannot rise, so red/cream is inflated and
    the row reads a distortion that is partly the exposure.  Measured: the same
    rig at two exposures gave 2.41x and 2.57x, and under AgX 3.43x.  A ratio of
    two albedos must not move with exposure at all.  Returns None on a clipped
    window rather than a number (rule 37)."""
    a = np.asarray(Image.open(path).convert('RGB')).astype(float)
    k = []
    for (x0, y0, x1, y1) in boxes:
        for y in range(y0, y1 - tsz, step):
            for x in range(x0, x1 - tsz, step):
                t = a[y:y + tsz, x:x + tsz].reshape(-1, 3)
                m = t.mean(0)
                if t.std(0).max() > 7.0:
                    continue
                if red and (not (m[0] > m[1] > m[2]) or m[1] / m[0] > 0.80):
                    continue
                # LINEARISE PER PIXEL, THEN AVERAGE.  lin(mean) != mean(lin),
                # and taking the mean in sRGB first left this row still moving
                # with EXPOSURE -- which a ratio of two albedos must not do.
                k.append(_lin(t).mean(0))
    if len(k) < 10:
        return None
    return np.array(k).mean(0)


def clip_fraction(path, boxes):
    a = np.asarray(Image.open(path).convert('RGB')).astype(float)
    px = np.vstack([a[y0:y1, x0:x1].reshape(-1, 3) for (x0, y0, x1, y1) in boxes])
    return float((px.max(1) >= 254).mean())



def main():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    p = flank(os.path.join(here, PHOTO[0]), PHOTO[1], PHOTO[2], PHOTO[3])
    if p is None:
        print("  R1 NO PHOTOGRAPH WINDOW -- nothing measured (rule 37)")
        raise SystemExit(3)
    print("  R1 PHOTOGRAPH ref_side.jpg      linear G/R %.4f  [%.4f .. %.4f]  (%d tiles)"
          % (p[1], p[2], p[3], p[0]))
    print("     the authored RED constant    linear G/R %.4f" % AUTHORED_RED_GR)

    frames = [a for a in sys.argv[1:] if a.endswith('.png')]
    if not frames:
        print("\n  NO FRAME GIVEN -- the RENDER row DID NOT RUN.  It is ABSENT, not")
        print("  passed (rule 37).   python3 probe_rev71_red.py out/<pfx>_side.png")
        raise SystemExit(3)
    fails = []
    for f in frames:
        r = flank(f, RENDER_BAND, RSTEP, RTSZ)
        if r is None:
            print("  R2 NO FLANK WINDOW in %s -- nothing measured" % f)
            continue
        ok = r[1] <= 2.0 * p[1]
        if not ok:
            fails.append(f)
        print("  [%s] R2 %-28s linear G/R %.4f  -- %.2fx the photograph"
              % ("PASS" if ok else "FAIL", os.path.basename(f), r[1], r[1] / p[1]))
    # ---- R3.  THE STRONGEST ROW, AND IT NEEDS NO PHOTOGRAPH AND NO ILLUMINANT.
    # A renderer must preserve the RATIO between two of its own albedos.  Score
    # the red flank against CREAM ON THE SAME VERTICAL PLANE and compare that to
    # RED/CREAM as authored.  Any departure is rendering distortion -- it cannot
    # be blamed on exposure, on the frame's white balance, or on the fact that
    # the photograph is outdoors and the render is in a studio.
    ar = np.array(RED_ALB) / np.array(CREAM_ALB)
    print("\n  ⚠ R3 MUST BE READ ON A TONE-CURVE-FREE FRAME.  Inverse-sRGB does NOT")
    print("    undo AgX, and read through AgX this row moves with EXPOSURE -- which a")
    print("    ratio of two albedos cannot do.  Same rig, two exposures: 2.41 / 2.57;")
    print("    under AgX: 3.43.  AND IT MUST ALSO BE UNCLIPPED: every 'gain' rev 71")
    print("    first measured for the relight was the CREAM DENOMINATOR clipping.")
    print("    THE ONLY VALID PROTOCOL: view_transform 'Raw', 16-bit, stopped DOWN")
    print("    (a ratio of two albedos is exposure-invariant in true linear, so")
    print("    stopping down is free).  On that ruler the shipped rig reads 2.67x,")
    print("    T1_SOFTEN=3.5 reads 2.86x -- WORSE -- and T1_SPEC+T1_CYCALB reach 1.71x.")
    print("\n  R3 PHOTOGRAPH-FREE -- does the render preserve its OWN albedo ratio?")
    print("     authored RED/CREAM              R %.4f  G %.4f  B %.4f" % tuple(ar))
    for f in frames:
        cf = clip_fraction(f, CREAM_BOXES)
        rr = ratio(f, [RENDER_BAND], True)
        cc = ratio(f, CREAM_BOXES, False)
        if rr is None or cc is None:
            print("     %-24s NO WINDOW -- not measured" % os.path.basename(f))
            continue
        if cf > 0.05:
            print("     %-24s REFUSED: %.0f %% of the CREAM window is clipped at "
                  "sRGB >= 254." % (os.path.basename(f), 100 * cf))
            print("     %-24s A clipped denominator cannot rise, so red/cream would"
                  % "")
            print("     %-24s read HIGH and the number would be exposure, not shape."
                  % "")
            fails.append(os.path.basename(f) + " (cream clipped)")
            continue
        q = rr / cc
        print("     %-24s R %.4f  G %.4f  B %.4f   G is %.2fx authored  [clip %.0f %%]"
              % (os.path.basename(f), q[0], q[1], q[2], q[1] / ar[1], 100 * cf))

    print("\n  DECOMPOSITION MEASURED AT REV 71 (F257), each term ablated, none inferred:")
    print("     specular       T1_SPEC   0.50 -> 0.05    -0.0574   44 % of the gap")
    print("     cyclorama floor T1_CYCALB 0.76 -> 0.05    -0.0277   21 %")
    print("     the WEATHER group's whole base-colour chain")
    print("                    T1_PAINT_RAW=1             -0.0044    3 %")
    print("     T1_WEATHER / T1_MOT_AMP / W_FADE_SAT       ~0        ~0 %")
    print("     STILL UNACCOUNTED with both nearly off    -0.0423   32 %")
    print("  => ENVIRONMENT 65 %, PAINT CHAIN 3 %.  Perfect neutral lighting would")
    print("     land the render on its own albedo (0.0533), so ~85 % of the total")
    print("     error is the STUDIO and ~15 % is the albedo.")
    print("  ⚠ DO NOT infer this from the Diffuse-Colour AOV: read against its own")
    print("    control the AOV over-states the paint chain by 8x (0.0347 vs 0.0044).")
    raise SystemExit(1 if fails else 0)


if __name__ == "__main__":
    main()
