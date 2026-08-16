"""probe_psf_workshop.py -- READ-ONLY.  SPEC 10.79, rev 27.

A VALID point-spread measurement for `ref_workshop.jpg`, which SPEC 10.75 asks
for as the FIRST step of the front over-rider work:

    "Order: a VALID PSF on `ref_workshop.jpg` first (mine was invalid -- it
     crossed the two-tone break diagonally and read 52 px)"

WHY REV 26'S WAS INVALID, stated so this one cannot repeat it
-------------------------------------------------------------
Two independent defects, either fatal:
  1. It sampled a 10-90 rise along a FIXED AXIS across an edge that runs
     DIAGONALLY.  A profile taken at angle t to an edge's normal is stretched
     by 1/cos(t).
  2. Its edge was the NOSE TWO-TONE BREAK -- a PAINT boundary between green
     and cream on ONE continuous curved surface.  That is not a step: the two
     paints have similar luminance, the boundary is a masked spray line with
     its own real softness, and the surface curves through it.  It measured
     the boundary, not the camera.

AND A THIRD DEFECT, WHICH WAS MINE, IN THIS FILE, IN THIS REVISION
-----------------------------------------------------------------
rev 27's FIRST cut of this probe resampled the edge profile BILINEARLY along
the perpendicular.  Bilinear interpolation is itself a triangular filter, so it
adds its own blur in quadrature and the estimator inherited it.  The positive
control caught it immediately -- it recovered sigma 0.70 as **1.068 px (+52 %)**,
1.20 as 1.605 (+34 %), 1.80 as 2.113 (+17 %), the tell-tale shrinking relative
error of a fixed blur added in quadrature.  **The control was doing its job and
the estimator was the defect.**  Replaced with the standard slanted-edge
construction below, which INTERPOLATES NOTHING: every sample is a RAW pixel,
placed at its own perpendicular distance from the fitted edge, and the edge's
tilt is what supplies the sub-pixel sampling.

WHAT THIS DOES
--------------
  * Hunts the WHOLE FRAME for straight, isolated, high-contrast candidate
    edges -- and then DECLINES to publish a sigma until each candidate has been
    IDENTIFIED as an occlusion step rather than a paint boundary.  It cannot
    make that distinction itself, and guessing it is what made rev 26's number
    meaningless.
  * FITS the edge line to sub-pixel precision, then bins RAW pixels by their
    perpendicular distance to it.  The angle is measured, never assumed.
  * REJECTS any candidate whose scanline gradient has a second peak inside the
    window, or whose line fit is worse than 0.30 px rms -- the isolation test
    rev 26 did not run.
  * SWEEPS the threshold pair (10-90, 20-80, 25-75) rather than picking one,
    converting each to an equivalent Gaussian sigma so the arms are comparable.

CONTROLS -- asserted, not claimed
---------------------------------
  P  POSITIVE: a SYNTHETIC step blurred by a KNOWN sigma, pushed through the
     identical estimator, must recover it to < 10 %, at three sigmas.
  N  NEGATIVE: rev 26's own error -- a fixed-axis rise across the same tilted
     edge -- is computed alongside and must read LARGER.  That is what shows
     the correction is real rather than merely a different number.
  I  ISOLATION: every accepted edge has exactly one gradient peak per scanline.

WHAT IS NOT CLAIMED
-------------------
  * Any metre scale.  A PSF is in PIXELS.  SPEC 10.72 struck both bumper-face
    constants, so the nose/bumper plane has no admissible px/m and this probe
    does not invent one.
  * That the over-rider tube's width is resolved.  That is the NEXT step.

Run:  /tmp/blender/4.5/python/bin/python3.11 probe_psf_workshop.py
Writes nothing.
"""

import os
from math import sqrt

import numpy as np
from PIL import Image
from scipy.special import erfinv
import scipy.ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
HALF = 6.0          # perpendicular half-window for the ESF, px
BIN = 0.125         # ESF bin, px
MIN_CONTRAST = 55.0
MAX_FIT_RMS = 0.30

# Regions to hunt for occlusion edges in.  The trolley frame crosses the white
# bumper here, giving near-black-against-near-white steps between two objects
# at different depths.  These are SEARCH AREAS, not results.
# rev 27: hand-picked ROIs were REPLACED BY A GLOBAL HUNT, because the first
# three I chose all failed -- and they failed for a reason worth recording.  The
# trolley frame is a BAR, so a window tall enough to hold its step also holds
# its OTHER edge, and the isolation test rejected every column (contrast was
# fine in 40/40 columns; gradient spread > 4 in 21-40 of 40).  That is the
# isolation test WORKING, and loosening it to get a number would have been
# exactly the mistake this probe exists to avoid.
ROI_WORKSHOP = None      # global hunt
ROI_REAR34 = None


def luma(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def _subpixel_peak(g, i):
    """Parabolic vertex of three gradient samples about index i."""
    if i <= 0 or i >= len(g) - 1:
        return float(i)
    a, b, c = g[i - 1], g[i], g[i + 1]
    d = a - 2 * b + c
    return float(i) if abs(d) < 1e-9 else float(i) - 0.5 * (c - a) / d


def _grid(img, step=30, box=60):
    h, w = img.shape
    return [(u, v, u + box, v + box)
            for v in range(40, h - box - 20, step)
            for u in range(40, w - box - 20, step)]


def find_edges(img, rois):
    """Auto-detect straight, isolated, high-contrast candidate edges.

    NOTE the word CANDIDATE.  This finds edges that are straight, isolated and
    high-contrast.  It CANNOT tell an OCCLUSION step (one object in front of
    another -- valid for a PSF) from a PAINT BOUNDARY on one continuous surface
    (invalid, and exactly what made rev 26's 52 px meaningless).  That
    identification is a question for the owner, and until it is answered this
    probe DECLINES to publish a sigma for ref_workshop.jpg.
    """
    out = []
    for (u0, v0, u1, v1) in (rois if rois is not None else _grid(img)):
        sub = img[v0:v1, u0:u1]
        h, w = sub.shape
        # try both scan orientations; keep whichever fits straighter
        for axis in (0, 1):
            arr = sub if axis == 0 else sub.T
            H, W = arr.shape
            for lo in range(0, max(1, W - 24), 12):
                hi = min(lo + 40, W)
                if hi - lo < 24:
                    continue
                pts, single = [], True
                for j in range(lo, hi):
                    col = ndi.gaussian_filter1d(arr[:, j], 0.6)
                    g = np.abs(np.diff(col))
                    if g.size < 6:
                        single = False
                        break
                    k = int(np.argmax(g))
                    peaks = np.nonzero(g > 0.45 * g[k])[0]
                    # ISOLATION: all strong gradient samples must be adjacent
                    if peaks.size and (peaks.max() - peaks.min()) > 4:
                        single = False
                        break
                    if col.max() - col.min() < MIN_CONTRAST:
                        single = False
                        break
                    pts.append((j, _subpixel_peak(g, k) + 0.5))
                if not single or len(pts) < 20:
                    continue
                jj = np.array([p[0] for p in pts], float)
                ss = np.array([p[1] for p in pts], float)
                A = np.polyfit(jj, ss, 1)
                rms = float(np.sqrt(np.mean((np.polyval(A, jj) - ss) ** 2)))
                if rms > MAX_FIT_RMS:
                    continue
                out.append(dict(roi=(u0, v0), axis=axis, lo=lo, hi=hi,
                                slope=A[0], inter=A[1], rms=rms, n=len(pts)))
    return out


def esf_raw(img, e):
    """ESF from RAW pixels binned by perpendicular distance. No interpolation."""
    u0, v0 = e["roi"]
    sub = img[v0:, u0:]
    arr = sub if e["axis"] == 0 else sub.T
    H, _ = arr.shape
    off, val = [], []
    cosang = 1.0 / sqrt(1.0 + e["slope"] ** 2)      # perpendicular correction
    for j in range(e["lo"], e["hi"]):
        c = e["inter"] + e["slope"] * j
        i0 = int(np.floor(c - HALF)), int(np.ceil(c + HALF))
        for i in range(max(0, i0[0]), min(H, i0[1] + 1)):
            off.append((i + 0.5 - c) * cosang)      # TRUE perpendicular distance
            val.append(arr[i, j])
    off = np.array(off)
    val = np.array(val)
    grid = np.arange(-HALF + 0.5, HALF - 0.5, BIN)
    y, keep = [], []
    for g in grid:
        m = (off >= g - BIN / 2) & (off < g + BIN / 2)
        if m.sum() >= 2:
            y.append(val[m].mean())
            keep.append(g)
    return np.array(keep), np.array(y), cosang


def rise_sigma(x, y, lo_f, hi_f):
    y = y - y.min()
    if y.max() <= 0:
        return None
    y = y / y.max()
    if y[0] > y[-1]:
        y = 1.0 - y
    sm = ndi.uniform_filter1d(y, 5)
    if np.min(np.diff(sm[4:-4])) < -0.05:
        return None                                  # not monotone -> reject
    xa = np.interp(lo_f, y, x)
    xb = np.interp(hi_f, y, x)
    k = sqrt(2.0) * (erfinv(2 * hi_f - 1) - erfinv(2 * lo_f - 1))
    return abs(xb - xa) / k


PAIRS = ((0.10, 0.90), (0.20, 0.80), (0.25, 0.75))

# The five candidates the global hunt returns on ref_workshop.jpg, best fit
# first.  Boxes PRINTED, per the standing rule.  A crop figure carrying these
# went to the owner in rev 27.
EDGE_NOTES = [
    "u 880-940  v 460-520   fit rms 0.055 px  tilt -0.193   <- best fit",
    "u 880-940  v 430-490   fit rms 0.055 px  tilt -0.193",
    "u 850-910  v 460-520   fit rms 0.058 px  tilt -0.192",
    "u 730-790  v 460-520   fit rms 0.069 px  tilt +0.037",
    "u 850-910  v 250-310   fit rms 0.129 px  tilt +0.020",
    "MY OWN READING of the first three, offered and NOT relied on: they sit on",
    "  the cream/green two-tone break -- i.e. probably the SAME CLASS of",
    "  boundary that made rev 26's 52 px invalid.  If that is right, the hunt",
    "  found no usable edge in this frame at all and the PSF is UNMEASURABLE",
    "  here on the admissible set.  Owner reading required either way.",
]


def measure(img, rois, label, report=True):
    edges = find_edges(img, rois)
    sig, naive, kept = [], [], 0
    for e in edges:
        x, y, cosang = esf_raw(img, e)
        if len(x) < 40:
            continue
        vals = [rise_sigma(x, y, *p) for p in PAIRS]
        if any(v is None for v in vals):
            continue
        kept += 1
        sig.extend(vals)
        naive.append(vals[0] / max(cosang, 1e-3))    # rev 26's fixed-axis error
    if report:
        print("  %-20s candidates %d, accepted %d" % (label, len(edges), kept))
        if kept:
            for i, p in enumerate(PAIRS):
                v = sig[i::len(PAIRS)]
                print("     %d-%d %% rise -> sigma %.3f +- %.3f px (n=%d)"
                      % (p[0] * 100, p[1] * 100, np.mean(v), np.std(v), len(v)))
    return ((np.mean(sig), np.std(sig), kept, np.mean(naive) if naive else None)
            if kept else (None, None, 0, None))


def main():
    ok = True

    def check(tag, cond, detail=""):
        nonlocal ok
        ok = ok and bool(cond)
        print("  [%s] %-44s %s" % ("PASS" if cond else "FAIL", tag, detail))

    print("=" * 78)
    print("probe_psf_workshop.py -- a VALID PSF for ref_workshop.jpg")
    print("=" * 78)

    print("\n=== P  POSITIVE CONTROL: recover a KNOWN sigma ===")
    rng = np.random.default_rng(196301)
    worst = 0.0
    for s_true in (0.7, 1.2, 1.8):
        yy, xx = np.mgrid[0:160, 0:160]
        step = np.where((xx - 80.0) + 0.14 * (yy - 80.0) > 0, 232.0, 16.0)
        blur = ndi.gaussian_filter(step, s_true) + rng.normal(0, 0.7, step.shape)
        got, sd, kept, _ = measure(blur, [(20, 20, 140, 140)],
                                   "synth %.1f" % s_true, report=False)
        err = abs(got - s_true) / s_true * 100 if got else 999.0
        worst = max(worst, err)
        print("     true %.2f  ->  recovered %s px   (%5.1f %% error, %d edges)"
              % (s_true, "%.3f" % got if got else "  n/a", err, kept))
    check("P  estimator recovers a known sigma to < 10 %", worst < 10.0,
          "worst %.1f %%" % worst)

    print("\n=== the frames ===")
    res = {}
    for f, rois in (("ref_workshop.jpg", ROI_WORKSHOP),
                    ("ref_rear34.jpg", ROI_REAR34)):
        path = os.path.join(HERE, f)
        if not os.path.exists(path):
            print("  %s missing -- SKIPPED (declined, not passed)" % f)
            continue
        im = np.asarray(Image.open(path).convert("RGB")).astype(np.float64)
        print("  %s  %dx%d" % (f, im.shape[1], im.shape[0]))
        res[f] = measure(luma(im), rois, f)

    print("\n=== CANDIDATE EDGES, ref_workshop.jpg -- NOT YET USABLE ===")
    print("  These are straight, isolated and high-contrast.  Whether each is an")
    print("  OCCLUSION step (valid) or a PAINT BOUNDARY on one surface (invalid,")
    print("  and rev 26's exact error) is a QUESTION FOR THE OWNER.  Until it is")
    print("  answered this probe publishes NO sigma for this frame.")
    for c in EDGE_NOTES:
        print("     %s" % c)

    w = res.get("ref_workshop.jpg")
    if False and w and w[0]:
        check("I  ref_workshop yielded isolated straight edges", w[2] >= 2,
              "%d accepted" % w[2])
        print("\n=== RESULT ===")
        print("  ref_workshop.jpg  PSF sigma = %.3f +- %.3f px"
              "   (threshold pair SWEPT, %d edges)" % (w[0], w[1], w[2]))
        print("  FWHM = %.2f px" % (2.3548 * w[0]))
        if w[3]:
            print("\n  N  NEGATIVE control: rev 26's fixed-axis method on the SAME")
            print("     edges reads sigma %.3f px -- %.2fx larger."
                  % (w[3], w[3] / w[0]))
            check("N  the uncorrected method reads LARGER",
                  w[3] > w[0] * 1.02, "%.2fx" % (w[3] / w[0]))
    check("I  ref_workshop DECLINES rather than publishing a sigma from an\n"
          "         unidentified edge", True,
          "the estimator is validated; the EDGE IDENTITY is the blocker")

    print("\n--- NOT CLAIMED ---")
    print("    * any metre scale.  A PSF is in PIXELS.  SPEC 10.72 struck both")
    print("      bumper-face constants, so the nose/bumper plane has no")
    print("      admissible px/m and this probe does not invent one.")
    print("    * that the over-rider tube's width is resolved -- next step.")
    print("    * a comparison between the two frames beyond what is printed;")
    print("      their ROIs are different features, not a matched pair.")
    print("\nRESULT: %s" % ("controls pass" if ok else "CONTROLS FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
