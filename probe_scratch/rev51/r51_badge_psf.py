"""rev 51 -- IS THE HUBCAP EMBLEM UNDERSIZED, OR DOES MY ESTIMATOR OVER-READ?

The open question: my threshold estimator reads emblem/cap = 0.3660 on ref_side.jpg
where the record's hand-read gives 0.3170.  The emblem is ~19 px in a frame whose own
declared PSF sigma is 1.625 px (t1_detail.py: "the frame's own quoted PSF sigma").
A threshold estimator broadens a small bright object by roughly the PSF, so the two
hypotheses are NOT separated by the reading alone.

CALIBRATE FIRST, ON A SYNTHETIC AT KNOWN SIZE AND KNOWN BLUR, exactly as the dome
measurement was calibrated before it was trusted.  Only then invert the real reading.
"""
import numpy as np
from scipy.ndimage import gaussian_filter, label
import math

CAP_PX = 59.97 / 2.0          # cap RADIUS in ref_side px, measured this revision
BAND   = 0.093                # CAP_RING_BANDFRAC -- ring band / ring outer D

def synth(ratio, sigma, S=8, size=140):
    """red cap + white emblem ring at a KNOWN ratio, supersampled then blurred."""
    n = size*S
    yy, xx = np.mgrid[0:n, 0:n]
    cx = cy = n/2.0
    r = np.hypot(xx-cx, yy-cy) / S
    img = np.zeros((n, n, 3))
    img[...] = [235, 232, 225]                       # cream surround
    cap = r <= CAP_PX
    img[cap] = [150, 40, 32]                          # red dome
    r_emb = ratio * CAP_PX                            # emblem OUTER radius
    ring = (r <= r_emb) & (r >= r_emb*(1 - 2*BAND))
    img[ring] = [238, 236, 232]                       # white ring
    # a crude V/W: two chords across the middle, same white
    bar = (np.abs((yy-cy)/S) < 0.16*r_emb) & (r < r_emb*(1-2*BAND))
    img[bar] = [238, 236, 232]
    small = img.reshape(size, S, size, S, 3).mean(axis=(1, 3))
    return gaussian_filter(small, (sigma, sigma, 0))

def estimate(im):
    """THE SAME estimator I ran on the photograph: cap = red, emblem = the
    low-sat bright blob nearest the centre; extent = 2 x 98th-pct radius."""
    R, G = im[:,:,0], im[:,:,1]
    mx, mn = im.max(2), im.min(2)
    sat = np.where(mx > 0, (mx-mn)/np.maximum(mx, 1), 0)
    L = 0.2126*im[:,:,0] + 0.7152*im[:,:,1] + 0.0722*im[:,:,2]
    H, W = L.shape; yy, xx = np.mgrid[0:H, 0:W]
    cx = cy = H/2.0
    rr = np.hypot(xx-cx, yy-cy)
    cap = (rr < 1.3*CAP_PX) & (R > 90) & (G < 0.72*R)
    if cap.sum() < 50: return None
    cap_r = np.percentile(rr[cap], 98)
    raw = (rr < 0.55*cap_r) & (sat < 0.45) & (L > 0.9*np.median(L[cap]))
    if raw.sum() < 8: return None
    return np.percentile(rr[raw], 98) / cap_r

print("CALIBRATION -- recovered ratio against KNOWN true ratio, at ref_side's own scale")
print("cap radius %.2f px; sweep the frame's declared PSF sigma 1.625\n" % CAP_PX)
print("%-8s" % "true", "".join("  s=%.2f" % s for s in (0.8, 1.2, 1.625, 2.0)))
rows = {}
for true in (0.280, 0.3170, 0.340, 0.3660, 0.400):
    line = "%-8.4f" % true; rec = {}
    for s in (0.8, 1.2, 1.625, 2.0):
        e = estimate(synth(true, s))
        rec[s] = e
        line += "  %6.4f" % (e if e else float('nan'))
    rows[true] = rec
    print(line)

print("\nINVERT: my real reading on ref_side.jpg was 0.3660 at the declared sigma 1.625")
xs = sorted(rows); ys = [rows[t][1.625] for t in xs]
if all(y is not None for y in ys):
    true_implied = np.interp(0.3660, ys, xs)
    print("  -> implied TRUE emblem/cap = %.4f" % true_implied)
    print("  -> the built constant is    = 0.3170")
    print("  -> record's hand-read       = 0.3170")
    err = (true_implied - 0.3170) / 0.3170 * 100
    print("  -> built is %+.1f %% relative to the implied truth" % (-err))
