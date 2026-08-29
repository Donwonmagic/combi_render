# probe_rev70_tyre.py -- rev 70.  THE TYRE IS TWICE AS LIGHT AS THE PHOTOGRAPH'S.
#
# THE RECORD HAS CARRIED "the tyres are 35 % too light" FOR EIGHT REVISIONS WITH
# NO INSTRUMENT UNDER IT.  This is that instrument, and it says 2.05x, not 35 %.
#
# WHY IT IS EXPOSURE-FREE (rule 38).  The tyre is scored against THE CREAM RIM
# RING IN THE SAME IMAGE, a bright near-neutral annulus a few pixels away from
# it.  A ratio of two luminances read off one frame cancels the exposure, the
# film curve and the illuminant's level.  Neither side is scored against a
# number typed into this file.
#
# WHY IT DOES NOT ENCODE A POSE (rule 35).  Nothing here is a typed radius.
# The wheel centre is found from the hubcap's own colour, and the two bands are
# then read OFF THE RADIAL PROFILE -- the rim is the brightest annulus outside
# the hubcap, the tyre the darkest annulus outside the rim.  Give it a frame at
# a different scale or distance and it finds different pixels for the same two
# physical surfaces.
#
# CEILING, AND IT IS REAL.  Both tyres sit under a wheel arch and neither rim
# does, so the ratio cancels exposure but NOT the difference in how much each
# surface is shadowed.  Treat the ratio as good to about +-20 %, which is far
# inside the 2x it is reporting.
#
# AND ONE STATED ASSUMPTION, WHICH THE CONTROL WAS BUILT WRONG WITHOUT AND
# CAUGHT: the tyre is found as the DARKEST annulus beyond the rim, so the
# surround must not be darker than the rubber.  The render (white cyclorama)
# and every reference frame (paving, workshop floor) satisfy this; a night
# shot would not, and the finder would silently return the background.  The
# control is built with a BRIGHT surround because that is the case this
# instrument claims -- it is not a claim about darker ones.
#
# READ THIS PROBE'S OWN SUMMARY LINE, NEVER ITS EXIT CODE (rule 9).
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "probe_scratch")


def _lum(a):
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]


def _sat(a):
    return (a.max(2) - a.min(2)) / np.maximum(a.max(2), 1.0)


def find_wheel(a, box):
    """Centre AND RADIUS of the painted hubcap inside `box`, from its own
    colour.  The radius is what makes everything below scale-free: every other
    radius in this file is a multiple of it, so a wheel imaged at 60 px and one
    at 200 px are measured on the same physical surfaces."""
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1]
    red = (sub[..., 0] - sub[..., 1]) > 40
    ys, xs = np.nonzero(red)
    if len(xs) < 50:
        return None
    return (x0 + xs.mean(), y0 + ys.mean(), np.sqrt(len(xs) / np.pi))


def bands(a, cx, cy, rhub):
    """Read the rim and tyre annuli OFF THE PROFILE, in units of the hubcap's
    own radius.  Nothing here is a typed pixel radius (rule 35).

    Returns (rim_lo, rim_hi, tyre_lo, tyre_hi) or None."""
    h, w, _ = a.shape
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.hypot(xx - cx, yy - cy)
    L = _lum(a)
    step = max(2.0, rhub / 8.0)

    def ring(r0):
        m = (r >= r0) & (r < r0 + step)
        return L[m].mean() if m.sum() >= 20 else None

    # the RIM is the brightest ring in (1.0 .. 2.0) hubcap radii -- the painted
    # steel between the cap and the rubber.  The TYRE is the darkest ring in
    # (2.0 .. 3.4), which is the sidewall and tread.
    def scan(a0, a1, pick):
        best = None
        r0 = a0 * rhub
        while r0 < a1 * rhub:
            v = ring(r0)
            if v is not None and (best is None or pick(v, best[1])):
                best = (r0, v)
            r0 += step
        return best
    rim = scan(1.0, 2.0, lambda v, b: v > b)
    tyr = scan(2.0, 3.4, lambda v, b: v < b)
    if rim is None or tyr is None:
        return None
    return (rim[0], rim[0] + step, tyr[0], tyr[0] + step)


def measure(path, box, tag, paint):
    a = np.asarray(Image.open(os.path.join(HERE, path)).convert("RGB")).astype(float)
    c = find_wheel(a, box)
    if c is None:
        print("  %-28s NO HUBCAP FOUND in the search box -- nothing measured "
              "(rule 37)" % tag)
        return None
    cx, cy, rhub = c
    b = bands(a, cx, cy, rhub)
    if b is None:
        print("  %-28s NO PROFILE -- the wheel does not present a rim and a "
              "tyre here. Nothing measured (rule 37)" % tag)
        return None
    m0, m1, t0, t1 = b
    h, w, _ = a.shape
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.hypot(xx - cx, yy - cy)
    mr, mt = (r >= m0) & (r < m1), (r >= t0) & (r < t1)
    L = _lum(a)
    Lr, Lt = L[mr].mean(), L[mt].mean()
    ov = a.copy()
    ov[mt] = [255, 40, 40]
    ov[mr] = [40, 235, 80]
    R = int(t1 * 1.25)
    sl = ov[max(0, int(cy - R)):int(cy + R), max(0, int(cx - R)):int(cx + R)]
    Image.fromarray(np.clip(sl, 0, 255).astype(np.uint8)).resize(
        (420, 420), Image.NEAREST).save(os.path.join(SCRATCH, paint))
    print("  %-28s tyre %6.1f  rim %6.1f   TYRE/RIM %.4f   bands rim %d-%d "
          "tyre %d-%d px (hubcap r %.1f) -> probe_scratch/%s"
          % (tag, Lt, Lr, Lt / Lr, m0, m1, t0, t1, rhub, paint))
    return Lt / Lr


def main():
    frame = sys.argv[1] if len(sys.argv) > 1 else None
    checks, fails = [], []

    def ck(name, ok, detail):
        checks.append((name, ok, detail))
        if not ok:
            fails.append(name)

    # ---- CONTROL: a synthetic wheel with a KNOWN ratio.  If the band finder
    # cannot recover a ratio it was handed, no number below means anything.
    n = 400
    yy, xx = np.mgrid[0:n, 0:n]
    r = np.hypot(xx - n / 2, yy - n / 2)
    syn = np.full((n, n, 3), 205.0)    # surround: cyclorama / paving, BRIGHT
    syn[r < 185] = [30, 30, 30]        # tyre   L = 30, out to 3.7 hubcap radii
    syn[r < 95] = [150, 150, 150]      # rim    L = 150
    syn[r < 50] = [180, 40, 40]        # hubcap, saturated
    Image.fromarray(syn.astype(np.uint8)).save(os.path.join(SCRATCH,
                                                            "rev70_tyre_synth.png"))
    got = measure("probe_scratch/rev70_tyre_synth.png", (140, 140, 260, 260),
                  "CONTROL synthetic 30/150", "rev70_tyre_ctl.png")
    want = 30.0 / 150.0
    ck("T1 CONTROL -- the band finder recovers a KNOWN tyre/rim ratio",
       got is not None and abs(got - want) < 0.02,
       "synthetic wheel built at tyre 30 / rim 150 = %.4f, recovered %s. The "
       "bands are read off the profile, so this tests the FINDER, not a typed "
       "radius" % (want, "%.4f" % got if got else "NOTHING"))

    ph = measure("ref_side.jpg", (700, 560, 800, 650), "PHOTOGRAPH ref_side.jpg",
                 "rev70_tyre_photo.png")
    if frame is None:
        print("  NO RENDER -- pass a frame: python3 probe_rev70_tyre.py "
              "out/rNN_side.png. The render rows did NOT run (rule 37)")
    else:
        rn = measure(frame, (1040, 820, 1150, 920), "RENDER %s" % os.path.basename(frame),
                     "rev70_tyre_render.png")
        if ph and rn:
            ck("T2 THE TYRE IS AS DARK AS THE PHOTOGRAPH'S, against the cream "
               "rim ring in its own image", rn <= ph * 1.25,
               "render tyre/rim %.4f against the photograph's %.4f -- %.2fx. "
               "The lever is `dust_film`'s road film on M[\"tyre\"], which mixes "
               "the rubber toward W_DUST_COL (pale limestone) at up to fac_low. "
               "CEILING: both tyres sit under an arch and neither rim does, so "
               "shadowing is not cancelled; good to about +-20 %%"
               % (rn, ph, rn / ph))

    print("=" * 78)
    print("  probe_rev70_tyre -- THE TYRE AGAINST ITS OWN RIM RING")
    print("=" * 78)
    for name, ok, detail in checks:
        print("  [%s] %s\n        %s" % ("PASS" if ok else "FAIL", name, detail))
    print()
    print("  %d checked, %d FAILED%s"
          % (len(checks), len(fails), ("  --  " + fails[0][:56]) if fails else ""))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
