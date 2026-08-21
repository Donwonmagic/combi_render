"""rev50 A2 instrument: m=5 angular harmonic of the hubcap's red-dome radius profile.

CALIBRATION FIRST (rule 22 / section 8): the instrument is run on two synthetics
where the answer is known BEFORE it is run on any real image.
  control 1  perfect circle           expect m5 ~ 0
  control 2  synthetic 5-petal +8%    expect m5 ~ 0.04
Only then on the render and on ref_side.jpg.
"""
import numpy as np, sys
from PIL import Image

def radial_profile(arr, cx, cy, is_red, rmax, n=720):
    """last radius along each ray that still satisfies is_red()"""
    th = np.linspace(0, 2*np.pi, n, endpoint=False)
    rr = np.arange(1.0, rmax, 0.25)
    out = np.zeros(n)
    H, W = arr.shape[:2]
    for i, t in enumerate(th):
        xs = cx + rr*np.cos(t); ys = cy + rr*np.sin(t)
        ok = (xs >= 0) & (xs < W-1) & (ys >= 0) & (ys < H-1)
        xi = np.clip(xs.astype(int), 0, W-1); yi = np.clip(ys.astype(int), 0, H-1)
        px = arr[yi, xi].astype(float)
        good = ok & is_red(px)
        idx = np.where(good)[0]
        if len(idx) == 0: out[i] = np.nan; continue
        # last contiguous run from the centre outward
        brk = np.where(np.diff(idx) > 1)[0]
        end = idx[brk[0]] if len(brk) else idx[-1]
        out[i] = rr[end]
    return out

def harmonics(prof, ms=(1,2,3,4,5,6,7)):
    p = prof[~np.isnan(prof)]
    if len(p) < 100: return None
    n = len(p); th = np.linspace(0, 2*np.pi, n, endpoint=False)
    mean = p.mean()
    return {m: 2*abs(np.sum(p*np.exp(-1j*m*th)))/n/mean for m in ms}

def synth(petals, amp, R=32.0, size=200):
    """render a synthetic red disc on cream, optionally with `petals` lobes at +amp"""
    a = np.zeros((size,size,3), np.uint8); a[:,:] = (210,205,190)
    yy,xx = np.mgrid[0:size,0:size]; cx=cy=size/2
    t = np.arctan2(yy-cy, xx-cx); r = np.hypot(xx-cx, yy-cy)
    Rl = R*(1.0 + (amp*np.cos(petals*t) if petals else 0.0))
    a[r<=Rl] = (190,55,40)
    return a

RED = lambda px: (px[:,0] > 85) & (px[:,1] < 0.70*px[:,0])

print("=== CONTROLS (run before any real image) ===")
for name, petals, amp in (("perfect circle",0,0.0), ("synthetic 5-petal +8%",5,0.08),
                          ("synthetic 3-petal +8%",3,0.08)):
    a = synth(petals, amp)
    h = harmonics(radial_profile(a, 100.0, 100.0, RED, 60))
    print(f"  {name:24s} " + "  ".join(f"m{m}={h[m]:.4f}" for m in sorted(h)))

def find_hub(arr, box, red=RED):
    """centroid of the red dome inside box=(x0,y0,x1,y1) -- derived, not typed"""
    x0,y0,x1,y1 = box
    sub = arr[y0:y1, x0:x1].astype(float).reshape(-1,3)
    m = red(sub).reshape(y1-y0, x1-x0)
    ys,xs = np.nonzero(m)
    if len(xs)==0: return None
    return x0+xs.mean(), y0+ys.mean(), m.sum()

print()
print("=== REAL IMAGES (instrument unchanged from the controls above) ===")
targets = [
  ("out/r50a_side.png  REAR wheel", "out/r50a_side.png", (1030,800,1170,940), 60),
  ("out/r50a_side.png  FRONT wheel","out/r50a_side.png", (380,800,520,940), 60),
  ("ref_side.jpg       REAR wheel", "ref_side.jpg",      (715,570,785,640), 34),
]
for label, f, box, rmax in targets:
    arr = np.array(Image.open(f).convert("RGB"))
    hb = find_hub(arr, box)
    if hb is None: print(f"  {label}: NO RED FOUND in box {box}"); continue
    cx, cy, npx = hb
    prof = radial_profile(arr, cx, cy, RED, rmax)
    h = harmonics(prof)
    good = prof[~np.isnan(prof)]
    print(f"  {label}")
    print(f"     centre ({cx:.1f},{cy:.1f}) from {int(npx)} red px | "
          f"r median {np.median(good):.2f} p25 {np.percentile(good,25):.2f} max {good.max():.2f} px")
    print("     " + "  ".join(f"m{m}={h[m]:.4f}" for m in sorted(h)))
