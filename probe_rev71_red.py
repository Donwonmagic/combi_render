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
            keep.append(_lin(m) if linear else m)
    if len(keep) < 20:
        return None
    K = np.array(keep)
    g = K[:, 1] / K[:, 0]
    return len(g), float(np.median(g)), float(np.percentile(g, 10)), float(np.percentile(g, 90))


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
    print("\n  DECOMPOSITION MEASURED AT REV 71 (F257), each term ablated, none inferred:")
    print("     specular  T1_SPEC 0.50 -> 0.05          -0.0597   44 % of the gap")
    print("     the WEATHER group's base-colour chain   -0.0347   26 %")
    print("     T1_WEATHER / T1_MOT_AMP / W_FADE_SAT     ~0        ~1 %  (all three NULL)")
    print("     ~30 % of the gap is still UNACCOUNTED.")
    print("  ⚠ THE DIFFUSE-COLOUR AOV NEEDS ITS CONTROL RUN FIRST: forcing Base Color")
    print("    to the authored RED and re-reading the SAME pass gives 0.0987, not")
    print("    0.0533, so the pass is BIASED and only its DIFFERENCES are usable.")
    raise SystemExit(1 if fails else 0)


if __name__ == "__main__":
    main()
