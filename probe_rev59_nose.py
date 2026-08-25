# probe_rev59_nose.py -- rev 59.  THE TWO-TONE BREAK ABOVE THE HEADLAMP,
# MEASURED ON AN ORTHOGRAPHIC FRONT ELEVATION.
#
# WHY THIS EXISTS.  F75 says the nose two-tone break passes far too close above
# the headlamp.  Every figure behind it was read off a THREE-QUARTER frame, so
# every one of them carries a pose term, and rev 55's "X" dissolved twice off
# un-pose-matched crops.  `studio.py` has carried
#     "front": dict(loc=(26.0, 0.0, 1.52), tgt=(0.0, 0.0, 1.52), ortho=3.55)
# reachable as T1_PREVIEW=front, and as the rev-59 brief sec.3.11 says, nothing
# in this tree had ever pointed it at the nose.  Being ORTHOGRAPHIC it removes
# perspective and plan-curvature bias entirely: no camera to recover, no
# flank_kv, and F26's camera ambiguity never arises.
#
# THE RULER is the headlamp's OWN vertical radius, measured in the same frame,
# so the figure is dimensionless and carries no px/m.
#
# WHICH AXES IT DOES NOT SEE (rule 36).  It sees the nose in ELEVATION only.
# It cannot see anything about depth or plan curvature; it cannot see the
# indicator (whose pod is not separable from the red field by this segmentation);
# and its ruler is the DARK LENS INTERIOR, not the chrome rim and not the bore.
# That choice matters -- sec.3.11 records that the model's rim stands 16.5 mm
# outside its own bore and that no frame we hold shows a rim and its aperture
# together, so a rim-based figure cannot be converted to a bore-based one.  The
# lens interior is used because it is the one feature this segmentation isolates
# cleanly in the render.  Comparisons to the photographed figures inherit that.
#
# READ THIS PROBE'S OWN SUMMARY LINE, NEVER ITS EXIT CODE (rule 9).
import sys, os
import numpy as np
from PIL import Image
from scipy import ndimage

ORTHO, RX, RY = 3.55, 1600, 1100          # studio.py "front"
# What the photographs read, from OPEN_FINDINGS F75.  Carried here so the
# comparison is in the probe rather than in a paragraph.
# rev 60b -- `ref_workshop` IS THE GREEN VEHICLE AND THIS IS A PAINT BOUNDARY.
#
# The two-tone break is where the CREAM meets the RED.  `ref_workshop.jpg` is a
# different bus in a different livery -- §0.1 of every brief since rev 54 says
# so, and CLAUDE.md rule 11 says paint and artwork do not transfer between
# vehicles while geometry does.  Its 2.127 was nevertheless the number M1
# printed as the target to reach, and rev 60 carried "74-76 mm" forward from it
# into the owner's own item B.
#
# It is KEPT, because it is the only BARE-APERTURE reading -- no chrome rim, no
# bloom -- and F75's register row calls it "the unambiguous ruler".  But it is
# now labelled, and the bar below is taken from the RED BUS frames only.
PHOTO = {"ref_nolita_front34": 2.121, "ref_nolita_front34b": 2.100,
         "ref_playa_34": 1.951}
PHOTO_GEOMETRY_ONLY = {"ref_workshop": 2.127}   # GREEN vehicle -- see above


def main():
    frame = sys.argv[1] if len(sys.argv) > 1 else None
    if not frame or not os.path.exists(frame):
        print("NO RENDER -- pass an orthographic front elevation as argv[1] "
              "(T1_PREVIEW=front).  out/ is untracked and starts empty on a "
              "clone.  Nothing was measured.")
        return 2
    a = np.asarray(Image.open(frame).convert("RGB")).astype(float)
    if a.shape[0] != RY or a.shape[1] != RX:
        print("NO RENDER -- %s is %dx%d, not the %dx%d front elevation this "
              "probe's ortho scale is written for." % (frame, a.shape[1],
                                                       a.shape[0], RX, RY))
        return 2
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    red = R - 0.5 * (G + B)
    lum = a.mean(axis=2)
    sat = a.max(axis=2) - a.min(axis=2)
    cream = (sat < 45) & (lum > 110)
    redm = red > 35
    pxm = RX / ORTHO

    lab, n = ndimage.label((~cream) & (~redm))
    cand = []
    for i in range(1, n + 1):
        m = lab == i
        if m.sum() < 800:
            continue
        vv, uu = np.nonzero(m)
        cv, cu = vv.mean(), uu.mean()
        if not (700 < cv < 1000 and 400 < cu < 1200):
            continue
        cand.append((m.sum(), cu, cv, vv.min(), vv.max()))
    cand.sort(reverse=True)

    fails, checks = [], []

    def ck(name, ok, detail):
        checks.append((name, ok, detail))
        if not ok:
            fails.append(name)

    ck("C1 exactly two headlamp blobs are found in the red field",
       len(cand) >= 2, "found %d" % len(cand))
    if len(cand) < 2:
        print("  C1 FAILED -- nothing further can be measured."); return 1
    lamps = sorted(cand[:2], key=lambda c: c[1])

    mid = 0.5 * (lamps[0][1] + lamps[1][1])
    ck("C2 the two lamps are symmetric about the frame's own centre column",
       abs(mid - RX / 2.0) < 0.004 * RX,
       "midpoint %.2f against %.1f -- %+.2f px.  A stub segmentation returning "
       "the frame centre would give exactly 0.00 and is excluded by C3"
       % (mid, RX / 2.0, mid - RX / 2.0))

    out = []
    for _, cu, cv, v0, v1 in lamps:
        ucol = int(round(cu))
        v = int(v0) - 2
        # ------------------------------------------------------- rev 61, F135
        # THIS WALK USED TO STOP ON THE HEADLAMP'S OWN CHROME BEZEL.
        #
        # `v0` is the top row of the LENS blob, which is segmented as
        # (~cream) & (~redm) -- i.e. dark AND unsaturated.  The chrome bezel
        # around the lens is BRIGHT and unsaturated, so `cream` is TRUE on it,
        # and a walk that starts at v0-2 and stops at the first cream pixel
        # stopped on the bezel, two pixels up, every single time.
        #
        # The bezel's top sits at a FIXED offset from the lamp centre -- its
        # own outer radius -- so M1 returned ~1.18 lamp radii NO MATTER WHAT
        # THE PAINT DID.  That is why V_POW, V_POW_Z, V_RISE and the 0.860
        # divisor all read "inert" (F106/F107): they are not inert, this
        # instrument was blind to them.  MEASURED on three renders by walking
        # the same column by hand -- M1 said 1.183 / 1.186 / 1.184 where the
        # true break is 1.730 / 3.701 / 3.788 lamp radii.
        #
        # THE FIX: cross the lamp assembly FIRST.  Walk up until the column is
        # on RED PAINT, and only then look for cream.  A bezel pixel is
        # neither, so it can no longer terminate the walk.  Rule 8: the
        # window is part of the measurement.
        while v > 500 and not redm[v, ucol]:
            v -= 1                      # cross the bezel, onto the paint
        while v > 500 and not cream[v, ucol]:
            v -= 1                      # then up to the true cream/red break
        hi = np.median(red[v + 3:v + 9, ucol])
        lo = np.median(red[max(v - 8, 0):v - 2, ucol])
        half = 0.5 * (hi + lo)
        vb = float(v)
        for k in range(v - 6, v + 7):
            if red[k, ucol] < half <= red[k + 1, ucol]:
                vb = k + (half - red[k, ucol]) / (red[k + 1, ucol] - red[k, ucol])
                break
        rad = (v1 - v0 + 1) / 2.0
        out.append((cu, cv, rad, vb, (cv - vb) / rad, 1000 * (cv - vb) / pxm))

    ck("C3 the two lamps are the same size and sit at the same height",
       abs(out[0][2] - out[1][2]) < 0.06 * out[0][2]
       and abs(out[0][1] - out[1][1]) < 3,
       "vertical radii %.2f and %.2f px; centre rows %.1f and %.1f"
       % (out[0][2], out[1][2], out[0][1], out[1][1]))

    ratios = [o[4] for o in out]
    ck("C4 the two independent lamps agree on the break height",
       abs(ratios[0] - ratios[1]) < 0.10 * np.mean(ratios),
       "%.3f and %.3f lamp radii  (%.1f %% apart)"
       % (ratios[0], ratios[1], 100 * abs(ratios[0] - ratios[1]) / np.mean(ratios)))

    built = float(np.mean(ratios))
    lo_p, hi_p = min(PHOTO.values()), max(PHOTO.values())
    # ----------------------------------------------------------- rev 61, F136
    # M1'S TWO SIDES ARE MEASURED WITH DIFFERENT RULERS, AND THAT IS NOT A
    # DETAIL -- IT IS WHY A "PASS" HERE MUST NOT BE READ AS ITEM B CLOSED.
    #
    # This probe's ruler is the DARK LENS INTERIOR (see the header).  The bar
    # below is F75's RED-BUS readings, and F75 says in terms what ruler those
    # used: "73-80 mm on the red-bus frames WHOSE RULER IS THE CHROME RIM --
    # the model's rim stands 16.5 mm outside its own bore and NO FRAME WE HOLD
    # SHOWS A RIM AND ITS APERTURE TOGETHER, so that 1.19 conversion CANNOT BE
    # CHECKED."  A lens-ruled figure and a rim-ruled bar differ by roughly that
    # unverifiable 1.19, so M1 comparing them is apples to oranges by ~19 %.
    #
    # IT IS LEFT AS THE LIVE ROW because it is the only nose gate that runs,
    # and because the BEZEL-ruled figure is printed beside it below so the
    # reader can see both.  What must never happen again is this line's PASS
    # being quoted as "the nose is right": rev 61 did exactly that for one
    # commit before the register was re-read.  F75's own verdict stands --
    # HONEST RANGE 50-80 mm, BEST SINGLE ESTIMATE 52 mm.
    ck("M1 the break sits as high above the lamp as the photographs put it"
       "  [RULER MISMATCH -- see F136 above; a PASS here is NOT item B closed]",
       lo_p <= built <= hi_p,
       "elevation %.3f lamp radii against the photographs' %.3f .. %.3f "
       "(%s; ref_workshop 2.127 is the GREEN vehicle and is EXCLUDED -- "
       "paint does not transfer, rule 11).  To reach %.3f, the highest RED-BUS "
       "reading, the break must rise %.1f px = %.0f mm"
       % (built, lo_p, hi_p, ", ".join("%s %.3f" % kv for kv in PHOTO.items()),
          max(PHOTO.values()),
          max(PHOTO.values()) * out[0][2] - (out[0][1] - out[0][3]),
          1000 * (max(PHOTO.values()) * out[0][2] - (out[0][1] - out[0][3])) / pxm))

    print("=" * 78)
    print("  probe_rev59_nose -- the two-tone break, on an ORTHOGRAPHIC elevation")
    print("  frame %s   (%.2f px/m)" % (frame, pxm))
    print("=" * 78)
    for name, ok, detail in checks:
        print("  %-4s %s" % ("PASS" if ok else "FAIL", name))
        print("       %s" % detail)
    print("-" * 78)
    for cu, cv, rad, vb, r, mm in out:
        # the BEZEL-ruled figure, on the SAME ruler as F75's red-bus bar.  The
        # bezel's outer top is where the upward walk first met RED PAINT, so
        # it costs nothing to report and it is the like-for-like number.
        ucol = int(round(cu))
        vv = int(cv)
        while vv > 500 and not redm[vv, ucol]:
            vv -= 1
        bez = cv - vv
        print("  lamp u %7.1f  centre row %7.1f  LENS radius %5.2f px  "
              "BEZEL radius %5.2f px" % (cu, cv, rad, bez))
        print("       BEZEL-RULED elevation %.3f  <- compare THIS with F75's "
              "red-bus 1.951..2.121, which is rim-ruled" % ((cv - vb) / bez))
        print("       break row %7.2f  ->  %.1f mm above centre  =  %.3f lamp radii"
              % (vb, mm, r))
    print("-" * 78)
    print("  %d checked, %d FAILED%s"
          % (len(checks), len(fails), ("  --  " + "; ".join(fails)) if fails else ""))
    print("=" * 78)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
