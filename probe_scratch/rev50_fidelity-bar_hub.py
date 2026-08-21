import numpy as np
from PIL import Image

def load(p):
    return np.asarray(Image.open(p).convert('RGB')).astype(float)

# ---- render, side view, exact ortho.  ppm and origin parsed by the rev49 survey
PPM = 271.1864
def px(X, Z): return (800.0 - PPM*X, 962.203 - PPM*Z)

im = load('out/r49base_side.png')
H,W,_ = im.shape
# rear wheel: X_AXLE_R = -1.100, hub z = TIRE_R = 0.3325
cx, cy = px(-1.100, 0.3325)
print("predicted rear hub centre px", cx, cy)

# refine: find the red dome centroid (high R, low G) in a 90px box
y0,y1,x0,x1 = int(cy-70), int(cy+70), int(cx-70), int(cx+70)
sub = im[y0:y1, x0:x1]
R,G,B = sub[...,0], sub[...,1], sub[...,2]
red = (R>90)&(G<0.62*R)
ys,xs = np.nonzero(red)
print("red dome pixels", red.sum(), "centroid", xs.mean()+x0, ys.mean()+y0)
ccx, ccy = xs.mean()+x0, ys.mean()+y0
# equivalent radius
Rdome = np.sqrt(red.sum()/np.pi)
print("dome equiv radius px", Rdome, "-> m", Rdome/PPM)

# angular profile of luminance at a set of radii around the dome edge
lum = im[...,:3].mean(axis=2)
for rr_m in (0.128, 0.134, 0.138, 0.142, 0.147, 0.152, 0.160):
    r = rr_m*PPM
    th = np.linspace(0, 2*np.pi, 720, endpoint=False)
    xs2 = ccx + r*np.cos(th); ys2 = ccy + r*np.sin(th)
    v = lum[np.round(ys2).astype(int), np.round(xs2).astype(int)]
    # count dark runs (below cream level)
    print("r=%.3f m (%.1f px)  lum min %.0f  med %.0f  max %.0f  frac<80 %.3f"
          % (rr_m, r, v.min(), np.median(v), v.max(), (v<80).mean()))
