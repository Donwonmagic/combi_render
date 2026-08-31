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
import os
import sys

import numpy as np
from PIL import Image

import photometry as PH

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


# The uniformity tolerance, in ENCODED units, relative to the tile's own level.
# 0.13 reproduces the rev-71 window that WAS painted and validated (745 tiles
# against that window's 840) while being independent of the frame's brightest
# pixel.  IT IS NOT A FREE PARAMETER: R1 prints the whole sensitivity band every
# run, because the reading MOVES with it -- see SENS below.
UNIF_ENC = 0.13
# ⚠ AND THIS IS A CEILING ON EVERY RED NUMBER THIS PROJECT HAS EVER PUBLISHED,
# MEASURED AT REV 71's CLOSE AND NOT KNOWN BEFORE.  The photograph's own red
# G/R depends on how strictly "plain paint" is defined, and not weakly:
#     tolerance 0.13 -> 745 tiles, G/R 0.0307      (the validated window)
#     tolerance 0.09 -> 279 tiles, G/R 0.0235
#     tolerance 0.06 ->  68 tiles, G/R 0.0149
# a 2.1x span across three defensible cuts, LARGER than most of the effects this
# project has been chasing on the red.  Quote the band, never a single figure.
SENS = (0.20, 0.13, 0.09, 0.06)


def _load(path, transform):
    """THE FRAME, LINEAR, WITH ITS TRANSFORM DECLARED BY THE CALLER.

    ⚠ THIS USED TO APPLY INVERSE-sRGB UNCONDITIONALLY, WHICH IS A DOUBLE
    DE-GAMMA ON A 'Raw' FRAME -- and every 'Raw' number this probe's own text
    quoted was read that way.  An adversary found it.  `photometry.load_linear`
    REFUSES an AgX frame outright and refuses an 8-bit 'raw' one, and it reads
    16 bits where PIL silently gives 8 (F263)."""
    return PH.load_linear(path, transform)


def flank(path, band, step, tsz, transform):
    """Linear G/R over the red flank.  Returns (n, median, p10, p90) or None."""
    a = _load(path, transform) if transform else (
        np.asarray(Image.open(path).convert('RGB')).astype(float) / 255.0)
    if transform is None:      # a PHOTOGRAPH: sRGB by definition, no choice to make
        a = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    x0, y0, x1, y1 = band
    keep = []
    for y in range(y0, y1 - tsz, step):
        for x in range(x0, x1 - tsz, step):
            t = a[y:y + tsz, x:x + tsz].reshape(-1, 3)
            m = t.mean(0)
            # UNIFORMITY IS JUDGED IN ENCODED SPACE AND RELATIVE TO THE TILE'S
            # OWN LEVEL.  Two decisions, both load-bearing, both watched:
            #   ENCODED, because "plain paint" is a VISUAL predicate and the
            #   window was painted and validated as one.  Judged in LINEAR the
            #   same tolerance admits tiles ON THE FOLK ART and rejects plain
            #   mottled paint -- PAINTED AND LOOKED AT at rev 71's close
            #   (probe_scratch/rev71_red_photowin_v2.png) and visibly wrong.
            #   RELATIVE, because the absolute form scaled by the frame's
            #   brightest pixel: one off-window highlight moved a control
            #   window from 0 tiles to 675 (photometry selftest check 9).
            # The MEASUREMENT is still taken in LINEAR, below.  Selection in
            # display space and measurement in linear is not two rulers for one
            # ratio (rule 38) -- both sides of every ratio here use both.
            te = np.clip(t, 0, 1) ** (1 / 2.2)
            if (te.std(0) > UNIF_ENC * float(te.mean())).any():
                continue                       # not plain paint: art, edge, or shadow line
            if not (m[0] > m[1] > m[2]):
                continue                       # red-dominant ORDERING, not a saturation cut
            if m[1] / m[0] > 0.80:
                continue                       # excludes cream, grey and the background wall
            keep.append(m)
    if len(keep) < 20:
        return None
    K = np.array(keep)
    g = K[:, 1] / K[:, 0]
    return len(g), float(np.median(g)), float(np.percentile(g, 10)), float(np.percentile(g, 90))


def ratio(path, boxes, red, transform, tsz=8, step=4):
    """Mean LINEAR colour over uniform tiles in `boxes`, and the CLIP fraction.

    ⚠ CLIPPING IS WHY THIS ROW NEEDED A GUARD.  R3 divides by the cream, and in
    the SHIPPED render 84 % of the cream window sits at sRGB >= 254 -- it is
    BLOWN OUT.  A clipped denominator cannot rise, so red/cream is inflated and
    the row reads a distortion that is partly the exposure.  Measured: the same
    rig at two exposures gave 2.41x and 2.57x, and under AgX 3.43x.  A ratio of
    two albedos must not move with exposure at all.  Returns None on a clipped
    window rather than a number (rule 37)."""
    a = _load(path, transform)
    k = []
    for (x0, y0, x1, y1) in boxes:
        for y in range(y0, y1 - tsz, step):
            for x in range(x0, x1 - tsz, step):
                t = a[y:y + tsz, x:x + tsz].reshape(-1, 3)
                m = t.mean(0)
                if (t.std(0) > PH.UNIFORM * float(m.mean()) + PH.UNIFORM_FLOOR).any():
                    continue
                if red and (not (m[0] > m[1] > m[2]) or m[1] / m[0] > 0.80):
                    continue
                # ALREADY LINEAR: _load did the transform, ONCE, with the caller
                # declaring which one.  The old code de-gamma'd here as well.
                k.append(m)
    if len(k) < 10:
        return None
    # MEDIAN, NOT MEAN.  The red's authored G albedo is 0.0294 and the cream's
    # is 0.6308 -- twenty times larger -- so a few contaminant tiles (folk-art
    # edges, the silver script, a shading transition) that survive the
    # uniformity filter DOUBLE the mean G while barely moving R.  Measured on
    # a physically clean render: per-tile G/R median 0.0653 against an authored
    # 0.0533, but the MEAN 0.1174.  Reading the mean is what made rev 71
    # publish a 2.67x distortion that was mostly its own statistic.
    return np.median(np.array(k), axis=0)


def clip_fraction(path, boxes, transform):
    return PH.clipped(_load(path, transform), boxes)



# THE DECOMPOSITION SET.  Each row is (prefix, what it turns off, the env that
# renders it).  R4 computes the deltas LIVE from whichever of these frames are
# present and REFUSES for the ones that are not (rule 37).
#
# ⚠ THIS BLOCK REPLACES A LIST OF HARD-CODED print() LITERALS.  Until rev 71's
# close this probe PRINTED a five-row decomposition -- "specular 44 %, cyclorama
# 21 %, paint chain 3 %, unaccounted 32 %" -- as string constants that no run
# could contradict.  That is F198's defect exactly, the one probe_rev46_vw's C12
# exists to prevent, committed in a file written to prevent it.  An adversary
# found it.  Nothing below is typed: if the frame is absent the row says so.
DECOMP = [
    ("f1shipped", "the shipped rig", ""),
    ("f2nodiffb", "diffuse inter-reflection OFF", "T1_DIFFB=0"),
    ("f3nospec", "+ the specular lobe at F0 0.0025", "T1_DIFFB=0 T1_SPEC=0.05"),
    ("f4flat", "+ the cyclorama and the coat",
     "T1_DIFFB=0 T1_SPEC=0.05 T1_CYCALB=0.05 T1_BODY_COAT=0.0"),
]
RENDER_ENV = ("T1_SUB=1 T1_PREVIEW=side T1_RX=1600 T1_RY=1100 T1_SAMP=96 "
              "T1_VT=Raw T1_LOOK=None T1_EXP=-2.5")


def main():
    here = os.path.dirname(os.path.abspath(__file__))

    # ---- THE TRANSFORM IS DECLARED, NEVER INFERRED (rule 57a).
    tf = None
    for a in sys.argv[1:]:
        if a.startswith("--transform="):
            tf = a.split("=", 1)[1]
        elif a in ("--raw", "--standard", "--agx"):
            tf = a[2:]
    frames = [a for a in sys.argv[1:] if a.endswith('.png')]

    p = flank(os.path.join(here, PHOTO[0]), PHOTO[1], PHOTO[2], PHOTO[3], None)
    if p is None:
        print("  R1 NO PHOTOGRAPH WINDOW -- nothing measured (rule 37)")
        raise SystemExit(3)
    print("  R1 PHOTOGRAPH ref_side.jpg      linear G/R %.4f  [%.4f .. %.4f]  (%d tiles)"
          % (p[1], p[2], p[3], p[0]))
    print("     the authored RED constant    linear G/R %.4f" % AUTHORED_RED_GR)
    print("     (a photograph is sRGB by definition -- there is no transform to")
    print("      declare for it, and that is the ONLY read here that assumes one.)")
    print("     R1b THE WINDOW'S OWN SENSITIVITY -- this is a CEILING, not a knob:")
    _g = globals()
    _save = _g['UNIF_ENC']
    try:
        band = []
        for tol in SENS:
            _g['UNIF_ENC'] = tol
            q = flank(os.path.join(here, PHOTO[0]), PHOTO[1], PHOTO[2], PHOTO[3], None)
            band.append((tol, 0 if q is None else q[0], 0.0 if q is None else q[1]))
            print("         uniformity %.2f -> %4d tiles, linear G/R %.4f"
                  % (tol, band[-1][1], band[-1][2]))
    finally:
        _g['UNIF_ENC'] = _save
    _v = [b[2] for b in band if b[1]]
    if len(_v) > 1:
        print("         => the photograph's red G/R is %.4f .. %.4f, a %.1fx span."
              % (min(_v), max(_v), max(_v) / max(min(_v), 1e-9)))
        print("         DO NOT QUOTE A SINGLE FIGURE FOR IT.  This span is larger")
        print("         than most of the effects the red has been tuned against.")

    if not frames:
        print("\n  NO FRAME GIVEN -- EVERY RENDER ROW DID NOT RUN.  They are ABSENT,")
        print("  not passed (rule 37).")
        print("    python3 probe_rev71_red.py out/<pfx>_side.png --transform=raw")
        raise SystemExit(3)
    if tf is None:
        print("\n  REFUSED: NO TRANSFORM DECLARED, AND IT CANNOT BE INFERRED FROM THE")
        print("  PIXELS.  Read through AgX a ratio of two albedos MOVES WITH EXPOSURE")
        print("  (3.43x against ~1.7x), which is physically impossible -- rev 71")
        print("  published that number before it knew.  Say which one the frame carries:")
        print("    --transform=raw        16-bit PNG under view_transform 'Raw'")
        print("    --transform=standard   8-bit under 'Standard'")
        print("    --transform=agx        will be REFUSED by photometry, by design")
        raise SystemExit(3)

    fails = []
    for f in frames:
        r = flank(f, RENDER_BAND, RSTEP, RTSZ, tf)
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
    print("\n  R3 PHOTOGRAPH-FREE -- does the render preserve its OWN albedo ratio?")
    print("     transform declared: %r      window: RED flank vs CREAM on the SAME"
          " vertical plane" % tf)
    print("     authored RED/CREAM              R %.4f  G %.4f  B %.4f" % tuple(ar))
    got = {}
    for f in frames:
        cf = clip_fraction(f, CREAM_BOXES, tf)
        rr = ratio(f, [RENDER_BAND], True, tf)
        cc = ratio(f, CREAM_BOXES, False, tf)
        if rr is None or cc is None:
            print("     %-24s NO WINDOW -- not measured" % os.path.basename(f))
            continue
        if cf > 0.05:
            print("     %-24s REFUSED: %.0f %% of the CREAM window is CLIPPED."
                  % (os.path.basename(f), 100 * cf))
            print("     %-24s A clipped denominator cannot rise, so red/cream would"
                  % "")
            print("     %-24s read HIGH and the number would be exposure, not shape."
                  % "")
            fails.append(os.path.basename(f) + " (cream clipped)")
            continue
        q = rr / cc
        got[os.path.basename(f)] = q
        print("     %-24s R %.4f  G %.4f  B %.4f   G is %.2fx authored  [clip %.1f %%]"
              % (os.path.basename(f), q[0], q[1], q[2], q[1] / ar[1], 100 * cf))

    # ---- R4.  THE DECOMPOSITION, COMPUTED, NOT TYPED.
    print("\n  R4 THE DECOMPOSITION -- every figure below is computed from the")
    print("     frames present in out/ this run.  A missing frame is a MISSING ROW.")
    have, prev = [], None
    for pfx, what, envs in DECOMP:
        f = os.path.join(here, "out", pfx + "_side.png")
        if not os.path.exists(f):
            print("     %-12s NOT RENDERED -- row ABSENT, not passed (rule 37)" % pfx)
            print("                  env %s T1_PFX=%s %s" % (RENDER_ENV, pfx, envs))
            continue
        cf = clip_fraction(f, CREAM_BOXES, tf)
        rr = ratio(f, [RENDER_BAND], True, tf)
        cc = ratio(f, CREAM_BOXES, False, tf)
        if rr is None or cc is None or cf > 0.05:
            print("     %-12s window empty or CLIPPED (%.1f %%) -- not measured"
                  % (pfx, 100 * cf))
            continue
        g = float((rr / cc)[1])
        d = "" if prev is None else "   delta %+.4f" % (g - prev)
        print("     %-12s G %.4f  = %.2fx authored%s   [%s]"
              % (pfx, g, g / ar[1], d, what))
        have.append((pfx, g))
        prev = g
    if len(have) < 2:
        print("     FEWER THAN TWO FRAMES -- THERE IS NO DECOMPOSITION, only a")
        print("     reading.  Render the set above before quoting any share.")
    else:
        span = have[0][1] - have[-1][1]
        print("     total swing over the terms present: %+.4f G, i.e. %.0f %% of the"
              % (-span, 100 * span / max(have[0][1] - ar[1], 1e-9)))
        print("     departure from the authored ratio is accounted for by them.")
    print("\n  ⚠ ACCEPTANCE CONDITION ON ANY OF THE ABOVE (F261/F263): re-render one")
    print("    configuration at T1_EXP=-1.5 and -3.5 and check the ratio AGREES.  A")
    print("    ratio of two albedos is exposure-invariant in true linear.  Rev 71's")
    print("    published decomposition read 1.60 / 1.53 / 1.39 across those three")
    print("    exposures -- an 8-bit read of a 16-bit file (PIL truncates silently),")
    print("    and that drift is what withdrew its magnitudes.  PUBLISH THE")
    print("    INVARIANCE FIGURE BESIDE THE DECOMPOSITION OR DO NOT PUBLISH IT.")
    print("\n  ⚠ AND DO NOT infer any of this from the Diffuse-Colour AOV: read")
    print("    against its own control the AOV over-states the paint chain by 8x")
    print("    (0.0347 vs 0.0044) -- rev 71 published that and retracted it.")
    raise SystemExit(1 if fails else 0)


if __name__ == "__main__":
    main()
