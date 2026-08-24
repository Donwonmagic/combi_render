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
PHOTO = {"ref_nolita_front34": 2.121, "ref_nolita_front34b": 2.100,
         "ref_playa_34": 1.951, "ref_workshop": 2.127}


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
        while v > 500 and not cream[v, ucol]:
            v -= 1
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
    ck("M1 the break sits as high above the lamp as the photographs put it",
       lo_p <= built <= hi_p,
       "elevation %.3f lamp radii against the photographs' %.3f .. %.3f "
       "(%s).  To reach %.3f the break must rise %.1f px = %.0f mm"
       % (built, lo_p, hi_p, ", ".join("%s %.3f" % kv for kv in PHOTO.items()),
          PHOTO["ref_workshop"],
          PHOTO["ref_workshop"] * out[0][2] - (out[0][1] - out[0][3]),
          1000 * (PHOTO["ref_workshop"] * out[0][2] - (out[0][1] - out[0][3])) / pxm))

    print("=" * 78)
    print("  probe_rev59_nose -- the two-tone break, on an ORTHOGRAPHIC elevation")
    print("  frame %s   (%.2f px/m)" % (frame, pxm))
    print("=" * 78)
    for name, ok, detail in checks:
        print("  %-4s %s" % ("PASS" if ok else "FAIL", name))
        print("       %s" % detail)
    print("-" * 78)
    for cu, cv, rad, vb, r, mm in out:
        print("  lamp u %7.1f  centre row %7.1f  vertical radius %5.2f px" % (cu, cv, rad))
        print("       break row %7.2f  ->  %.1f mm above centre  =  %.3f lamp radii"
              % (vb, mm, r))
    print("-" * 78)
    print("  %d checked, %d FAILED%s"
          % (len(checks), len(fails), ("  --  " + "; ".join(fails)) if fails else ""))
    print("=" * 78)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
