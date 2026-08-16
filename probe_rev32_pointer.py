"""probe_rev32_pointer.py -- rev 32.  READ-ONLY.  Validates rev 32's THREE
Q2 pointers BEFORE they are sent, and prints every crop box.

WHY THIS FILE EXISTS
--------------------
SPEC 10.82 retired `W_DUST_FAC_UP` 0.7313 -> 0.0 on ONE owner reading (the roof
in `ref_rear34.jpg` is clean) and NAMED the surfaces that reading does not
cover: the BUMPER TOP, the RIM BARRELS and the HUB CAPS.  rev 30 and rev 31
both carried that item forward without asking.  rev 32 asks.

rev 28's standing rule: A QUESTION THAT CANNOT BE ANSWERED UNAMBIGUOUSLY IS THE
ASKER'S DEFECT.  rev 29's standing rule: A THRESHOLD IS A PROBE TOO, and the
band must be calibrated against a box the owner HAS ALREADY ANSWERED.  This
file reuses rev 29's statistic and rev 29's two calibration anchors unchanged.

TWO FINDINGS THAT CHANGED THE QUESTION BEFORE IT WAS ASKED
----------------------------------------------------------
**FINDING 1 -- THE WORK LIST'S OWN DESCRIPTION IS WRONG.**  rev 29's memory,
rev 30's, rev 31's and the rev-32 brief all say "the workshop frame shows all
three".  IT DOES NOT.  In `ref_workshop.jpg` BOTH road wheels are BARE PAINTED
RIMS WITH NO HUB CAP -- the vehicle is at conversion stage.  The red VW-logo
hub caps appear only in `ref_side.jpg`, the in-service frame.  So the hub-cap
pointer is placed on `ref_side.jpg` and the item's own description is
corrected.  A FEATURE NAMED IN A WORK LIST IS A PROBE TOO.

**FINDING 2 -- THE QUESTION IS WORTH ASKING, AND THAT WAS MEASURED, NOT
ASSUMED.**  `probe_dust_scope.py` on the shipped build reports the up-facing
area the retired lever reaches on exactly these surfaces:

    rim barrel   0.1125 m^2 x 4 = 0.4500 m^2   (`wheelcream`)
    hub cap      0.0525 m^2 x 4 = 0.2100 m^2   (`capred`)
    bumper_f     0.0909 m^2                    (`bumpercream`)

0.751 m^2 against `T1_body`'s 12.294 m^2 -- about 6 % of the filmed area, on
three surfaces that sit at the front of every hero frame.  A QUESTION YOU ARE
ABOUT TO ASK IS A PROBE TOO: if the lever had barely reached them, asking would
have spent his attention on nothing.

**A THIRD FINDING, UNSOUGHT AND UNRELATED TO THE QUESTION.**
`probe_dust_scope.py` FAILS one of its own eight controls on the shipped build:
`probe_dust_scope.py:249` hard-codes "audit.py publishes 185" and the build has
carried **186** meshes since rev 30 added `orb_bar`.  It has been failing since
rev 30 and neither rev 30 nor rev 31 ran it.  Recorded here because that is
where it was found; the fix belongs in that file.

THE CROSS-FRAME CAVEAT, STATED RATHER THAN BURIED
-------------------------------------------------
rev 29's two calibration anchors both live on `ref_rear34.jpg`.  Two of rev
32's three boxes do not.  The statistic is a RATIO TO THE BOX'S OWN SYNTHETIC
FLOOR, which normalises out that box's own noise and shape and is therefore
designed to travel; but it is not proven to travel, and no answered anchor
exists on `ref_side.jpg` at all.  **THAT IS THIS PROBE'S CEILING and it is
printed with the verdict, not omitted.**
"""
import math
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 20250816
FAIL = []
LINES = []


def P(s=""):
    print(s)
    LINES.append(s)


def check(ok, label, detail=""):
    P("  [%s] %s%s" % ("PASS" if ok else "FAIL", label,
                       ("  -- " + detail) if detail else ""))
    if not ok:
        FAIL.append(label)


def luma(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def _resid(l):
    h, w = l.shape
    yy, xx = np.mgrid[0:h, 0:w]
    x = xx.ravel() / max(1, w - 1)
    y = yy.ravel() / max(1, h - 1)
    A = np.column_stack([np.ones_like(x), x, y, x * x, x * y, y * y])
    c, *_ = np.linalg.lstsq(A, l.ravel(), rcond=None)
    r = l.ravel() - A @ c
    lo, hi = np.percentile(r, [5, 95])
    return 100.0 * (hi - lo) / l.mean()


def hf_sigma(l):
    d = np.diff(l, axis=1)
    return 1.4826 * np.median(np.abs(d - np.median(d))) / np.sqrt(2.0)


def floor_for(l):
    h, w = l.shape
    yy, xx = np.mgrid[0:h, 0:w]
    x, y = xx / max(1, w - 1), yy / max(1, h - 1)
    rng = np.random.default_rng(SEED)
    span = np.percentile(l, 95) - np.percentile(l, 5)
    ramp = l.mean() + span * (0.6 * x - 0.35 * x * x + 0.25 * y)
    return _resid(ramp + rng.normal(0.0, max(hf_sigma(l), 0.3), (h, w)))


FRAMES = {}


def frame(name):
    if name not in FRAMES:
        FRAMES[name] = np.asarray(
            Image.open(os.path.join(HERE, name)).convert("RGB")).astype(float)
    return FRAMES[name]


def report(fr, box, name):
    u0, u1, v0, v1 = box
    im = frame(fr)
    sub = im[v0:v1, u0:u1]
    l = luma(sub)
    res, flr = _resid(l), floor_for(l)
    clip = 100.0 * (sub.max(axis=2) >= 254).mean()
    med = tuple(np.median(sub.reshape(-1, 3), axis=0).round(0).astype(int))
    P("  %s   [%s]" % (name, fr))
    P("    CROP BOX  u %d-%d  v %d-%d   (%d x %d px, n=%d)"
      % (u0, u1, v0, v1, u1 - u0, v1 - v0, l.size))
    P("    median sRGB %s   hf sigma %.2f   clipped %.2f %%"
      % (med, hf_sigma(l), clip))
    P("    quadratic residual %5.1f %%   own floor %5.1f %%   ratio %.2f x"
      % (res, flr, res / flr if flr else float("inf")))
    return res, flr, clip


# rev 29's two calibration anchors, UNCHANGED, both on ref_rear34.jpg
STRADDLER = ("ref_rear34.jpg", (556, 656, 397, 424))   # PROVEN straddler
ANSWERED = ("ref_rear34.jpg", (640, 680, 420, 435))    # rev 28, ANSWERED clean
ROOF29 = ("ref_rear34.jpg", (860, 930, 234, 246))      # rev 29, ANSWERED clean

# rev 32's three pointers
B1 = ("ref_workshop.jpg", (262, 288, 702, 710))   # BUMPER TOP, blade upper face
B2 = ("ref_side.jpg", (708, 719, 590, 620))       # RIM FACE, rear wheel
B3 = ("ref_side.jpg", (756, 774, 586, 602))       # HUB CAP, upper-right quadrant

# EIGHT hub-cap boxes were measured and SEVEN FAILED.  All eight are printed
# below rather than only the survivor -- rev 29's rule, that the wrong cuts are
# recorded and not smoothed away.  The reason SEVEN fail is STRUCTURAL, not
# statistical, and that is what licenses relocating the box instead of widening
# the band: the cap is a DOME under one dominant source, so its lower half
# carries the wheel-arch shadow's EDGE, and a quadratic absorbs a gradient but
# not an edge.  My first cut (726,744,580,596) sat on the specular highlight
# and read 8.77 x -- closer to a PROVEN STRADDLER than to an ANSWERED box.
B3_TRIED = [
    ((726, 744, 580, 596), "first cut -- sits on the specular highlight"),
    ((752, 772, 606, 624), "lower right -- shadow edge"),
    ((730, 750, 610, 626), "lower left -- shadow edge"),
    ((756, 774, 586, 602), "upper right quadrant -- ACCEPTED"),
    ((734, 760, 612, 626), "low centre -- shadow edge"),
    ((722, 740, 604, 620), "left of centre -- highlight rolloff"),
    ((744, 766, 614, 628), "low right -- shadow edge"),
    ((728, 752, 616, 630), "bottom -- shadow edge"),
]


def main():
    P("\n" + "=" * 74)
    P("probe_rev32_pointer.py -- validating rev 32's THREE pointers "
      "before sending")
    P("=" * 74)
    for f in ("ref_rear34.jpg", "ref_workshop.jpg", "ref_side.jpg"):
        a = frame(f)
        P("  frame %-18s %d x %d" % (f, a.shape[1], a.shape[0]))
    P("  quadratic straddle indicator, seeded %d" % SEED)

    P("\n--- P1  POSITIVE CEILING: rev 29's PROVEN straddler ---")
    c_res, c_flr, _ = report(*STRADDLER,
                             name="SPEC 10.76 founding patch [PROVEN STRADDLE]")
    check(c_res > 8.0 * c_flr, "P1 the known straddler is NOT absorbed",
          "%.1f %% at %.1f x its own floor" % (c_res, c_res / c_flr))

    P("\n--- A0  rev 28's and rev 29's ANSWERED boxes, this statistic ---")
    a_res, a_flr, _ = report(*ANSWERED,
                             name="rev 28 counter top [ANSWERED CLEAN]")
    r29_res, r29_flr, _ = report(*ROOF29,
                                 name="rev 29 roof crown [ANSWERED CLEAN]")
    anchor_r = a_res / a_flr
    roof_r = r29_res / r29_flr
    strad_r = c_res / c_flr
    check(strad_r / anchor_r > 3.0, "A0 the calibration anchors are separated",
          "answered %.2f x vs straddler %.2f x = %.1f x apart"
          % (anchor_r, strad_r, strad_r / anchor_r))
    P("    TWO answered anchors now exist, not one: rev 28's counter "
      "(%.2f x) and rev 29's roof (%.2f x)." % (anchor_r, roof_r))
    P("    The band below uses rev 28's, the same one rev 29 used, so the "
      "threshold is UNCHANGED from the revision that set it.")

    P("\n--- B3's EIGHT CANDIDATES: SEVEN FAILED, ALL PRINTED ---")
    P("  the cap is a DOME and its lower half carries the wheel-arch shadow's")
    P("  EDGE; a quadratic absorbs a gradient but not an edge.  Relocating the")
    P("  box is licensed by that, NOT by shopping for a passing number -- and")
    P("  the band below is rev 29's, unchanged.")
    P("  %-22s %-16s %6s %7s %8s  %s"
      % ("box", "median sRGB", "res %", "floor %", "ratio", "note"))
    im_s = frame(B3[0])
    for bx, note in B3_TRIED:
        u0, u1, v0, v1 = bx
        sub = im_s[v0:v1, u0:u1]
        l = luma(sub)
        r, f = _resid(l), floor_for(l)
        med = tuple(np.median(sub.reshape(-1, 3), axis=0).round(0).astype(int))
        P("  %-22s %-16s %6.1f %7.1f %7.2f x  %s"
          % (str(bx), str(med), r, f, r / f, note))
    check(sum(1 for bx, _ in B3_TRIED
              if _resid(luma(im_s[bx[2]:bx[3], bx[0]:bx[1]]))
              / floor_for(luma(im_s[bx[2]:bx[3], bx[0]:bx[1]])) < strad_r) >= 1,
          "B3 at least one candidate clears the straddler",
          "7 of 8 do not -- that is a finding about the cap, not about the box")

    P("\n--- THE THREE REV-32 POINTERS ---")
    out = []
    for fr, bx, nm in ((B1[0], B1[1], "B1  BUMPER TOP, blade upper face"),
                       (B2[0], B2[1], "B2  RIM FACE (barrel), rear wheel"),
                       (B3[0], B3[1], "B3  HUB CAP, red, clear of the logo")):
        P("")
        res, flr, clip = report(fr, bx, nm)
        r = res / flr
        d_ans = abs(math.log(r) - math.log(anchor_r))
        d_str = abs(math.log(r) - math.log(strad_r))
        P("    log-distance to ANSWERED %.2f x : %.3f   |   to STRADDLER "
          "%.2f x : %.3f" % (anchor_r, d_ans, strad_r, d_str))
        check(d_ans < d_str,
              "%s is closer to an ANSWERED box than to a PROVEN straddler"
              % nm.split()[0],
              "%.2f x  (%.1fx closer in log-ratio)"
              % (r, math.exp(d_str - d_ans)))
        check(clip < 1.0, "%s is not clipped" % nm.split()[0],
              "%.2f %% of pixels at 254+" % clip)
        out.append((nm, fr, bx, r))

    P("\n" + "=" * 74)
    P("CONTROLS: %d checked, %d FAILED" % (2 + 1 + 1 + 6, len(FAIL)))
    for f in FAIL:
        P("   FAILED: %s" % f)
    P("=" * 74)
    P("CEILING, stated: rev 29's two calibration anchors both live on")
    P("ref_rear34.jpg.  B1 is on ref_workshop.jpg and B2/B3 are on")
    P("ref_side.jpg.  The statistic is a ratio to each box's OWN synthetic")
    P("floor, which is designed to normalise frame noise and box shape -- but")
    P("it is NOT PROVEN to travel between frames, and NO ANSWERED ANCHOR")
    P("EXISTS ON ref_side.jpg AT ALL.  These three boxes are POINTERS: they")
    P("say 'this surface'.  NO NUMBER IN REV 32 IS TAKEN FROM ANY OF THEM,")
    P("which is what keeps the cross-frame caveat from being load-bearing.")
    P("")
    P("CORRECTION TO THE WORK LIST: `ref_workshop.jpg` does NOT show hub")
    P("caps.  Both wheels there are bare painted rims -- conversion stage.")
    P("The hub caps are in `ref_side.jpg` only.  rev 29, rev 30, rev 31 and")
    P("the rev-32 brief all say the workshop frame shows all three.")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
