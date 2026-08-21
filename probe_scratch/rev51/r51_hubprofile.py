"""rev 51 -- the hubcap's visible red silhouette on the CURRENT tip, with controls.

Instrument: for each of N rays from the hub centre, walk outward and record the
LARGEST radius that is still "red".  NOT the last contiguous run from the centre
-- rev 50 recorded that its first version did exactly that and every ray
terminated on the white VW emblem (median radius 8.25 px on a 33 px dome).  The
control that catches it is a synthetic disc WITH A CENTRAL HOLE.

Controls run BEFORE the real frame, and their expected answers are known by
construction, not by inspection.
"""
import numpy as np, math
from PIL import Image

def redmax(img, cx, cy, rmax_px, nray=720, red=None):
    """largest radius still satisfying red(); returns per-ray radii in px"""
    H, W, _ = img.shape
    out = np.zeros(nray)
    rr = np.arange(0.5, rmax_px, 0.25)
    for k in range(nray):
        a = 2*math.pi*k/nray
        xs = cx + rr*math.cos(a); ys = cy - rr*math.sin(a)
        ok = (xs >= 0) & (xs < W-1) & (ys >= 0) & (ys < H-1)
        xi = np.clip(xs.astype(int), 0, W-1); yi = np.clip(ys.astype(int), 0, H-1)
        px = img[yi, xi].astype(float)
        m = red(px) & ok
        out[k] = rr[np.where(m)[0][-1]] if m.any() else 0.0
    return out

def harm(r, m):
    """normalised amplitude of the m-th angular harmonic. 2|F_m|/n/mean --
    rev 50's convention, TWICE the survey's; do not compare to its 0.0399."""
    n = len(r); F = np.fft.rfft(r - r.mean())
    return 2*abs(F[m])/n/r.mean()

REDGATE = lambda px: (px[:,0] > 95) & (px[:,1] < 0.62*px[:,0])

# ---------------------------------------------------------------- CONTROLS
def synth(shape, R, petal=0.0, hole=0.0, size=220):
    im = np.full((size, size, 3), 235, np.uint8)   # cream ground
    c = size/2.0
    yy, xx = np.mgrid[0:size, 0:size]
    dx = xx - c; dy = c - yy
    r = np.hypot(dx, dy); th = np.arctan2(dy, dx)
    rad = R*(1.0 + petal*np.cos(5*th))
    m = r <= rad
    im[m] = (200, 60, 50)                          # red
    if hole > 0:
        im[r <= hole] = (250, 250, 250)            # WHITE central emblem
    return im, c, c

print("CONTROL                              median r   max r   m5      m2")
cases = [("perfect circle R=33",            33.0, 0.00, 0.0),
         ("circle + WHITE central hole r=9", 33.0, 0.00, 9.0),
         ("5-petal +8%, no hole",           33.0, 0.08, 0.0),
         ("5-petal +8% + WHITE hole r=9",   33.0, 0.08, 9.0)]
for name, R, p, h in cases:
    im, cx, cy = synth(None, R, p, h)
    r = redmax(im, cx, cy, 70, 720, REDGATE)
    # MEDIAN of R*(1+p*cos5th) over uniform theta is R for ANY p, because the
    # median of cos5th is 0.  The petal shows up in the MAX (R*(1+p)) and in m5,
    # never in the median.  Print both so the expectation is not mis-stated.
    print("%-36s %7.2f  %7.2f  %.4f  %.4f  | expect median ~%.1f, max ~%.1f, m5 %s"
          % (name, np.median(r), r.max(), harm(r,5), harm(r,2), R, R*(1+p),
             "0" if p == 0 else "> 0"))

# ---------------------------------------------------------------- THE FRAME
img = np.asarray(Image.open('out/r51b_side.png').convert('RGB'))
PPM = 271.1864
print("\nrev-51 tip, out/r51b_side.png, side ORTHO, %.4f px/m" % PPM)
print("wheel     median_r_px  ->  m       p25     max     m5      m2      m3      m4      m6      m7")
for tag, X in (("rear", -1.100), ("front", 1.300)):
    cx = 800 - PPM*X; cy = 962.203 - PPM*0.3325
    r = redmax(img, cx, cy, 60, 720, REDGATE)
    med = np.median(r)
    print("%-9s %8.2f  %9.5f  %6.2f  %6.2f  %.4f  %.4f  %.4f  %.4f  %.4f  %.4f"
          % (tag, med, med/PPM, np.percentile(r,25), r.max(),
             harm(r,5), harm(r,2), harm(r,3), harm(r,4), harm(r,6), harm(r,7)))
print("\nANALYTIC crossover from the two authored profiles: 0.11973 m = %.2f px" % (0.11973*PPM))
print("CAP_R + lip                                       : 0.13700 m = %.2f px" % (0.137*PPM))
