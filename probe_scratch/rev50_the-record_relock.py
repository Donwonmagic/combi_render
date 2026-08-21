"""rev 50, THE RECORD.  Re-derive SPEC section 8.1-8.5's five M-graded locks on
ref_playa_34.png -- WHICH IS THE SAME PHOTOGRAPH AS ref_source.jpeg, at 2.03x
the linear resolution.  Nothing but the pixel grid changes: same pose, same
light, same artwork state.

CEILING.  Every coordinate below is SPEC's own ref_source pixel scaled by
s = 500/246 = 2.0325 (x) and 400/197 = 2.0305 (y).  Scaling a coordinate is not
a re-measurement of the feature; the hub is RE-CENTRED by a local search before
the radial profile is taken, and the search window is printed.  If the search
moves the centre more than ~2 playa px the scaling, not the frame, is the
suspect.
"""
import numpy as np
from PIL import Image
import colorsys

def load(p):
    a = np.asarray(Image.open(p).convert('RGB'), float)
    return a

def hsv_sat(rgb):
    r, g, b = rgb[...,0]/255., rgb[...,1]/255., rgb[...,2]/255.
    mx = np.maximum(np.maximum(r,g),b); mn = np.minimum(np.minimum(r,g),b)
    s = np.where(mx > 0, (mx-mn)/np.maximum(mx,1e-9), 0.0)
    return s

SRC = load('ref_source.jpeg'); PLA = load('ref_playa_34.png')
SS = hsv_sat(SRC); PS = hsv_sat(PLA)
SL = SRC.mean(2); PL = PLA.mean(2)

sx, sy = 500/246., 400/197.
print("scale x %.5f  y %.5f" % (sx, sy))

# ---- 8.1 radial profile about the front hub -------------------------------
def radial(img_l, img_s, cx, cy, rmax, sect=(185,265)):
    out = []
    for r in range(0, rmax+1):
        ls, ss_, n = [], [], 0
        for adeg in np.arange(sect[0], sect[1]+0.001, 1.0):
            a = np.radians(adeg)
            x = cx + r*np.cos(a); y = cy + r*np.sin(a)
            xi, yi = int(round(x)), int(round(y))
            if 0 <= yi < img_l.shape[0] and 0 <= xi < img_l.shape[1]:
                ls.append(img_l[yi, xi]); ss_.append(img_s[yi, xi]); n += 1
        out.append((r, np.mean(ls) if n else np.nan, np.mean(ss_) if n else np.nan, n))
    return out

print("\n=== 8.1  ref_source.jpeg, SPEC's own hub (114.5, 160.5) ===")
for r, l, s, n in radial(SL, SS, 114.5, 160.5, 20):
    print("  r %2d  lum %6.1f  sat %.3f" % (r, l, s))

cx0, cy0 = 114.5*sx, 160.5*sy
print("\n=== 8.1  ref_playa_34.png, scaled hub (%.1f, %.1f) ===" % (cx0, cy0))
# re-centre: the hubcap is the strongly red disc.  Maximise mean sat in r<=10.
best = None
for dx in np.arange(-6, 6.01, 0.5):
    for dy in np.arange(-6, 6.01, 0.5):
        cx, cy = cx0+dx, cy0+dy
        v = np.mean([s for r, l, s, n in radial(PL, PS, cx, cy, 10) if r <= 10])
        if best is None or v > best[0]:
            best = (v, cx, cy, dx, dy)
print("  re-centre search +-6.0 px, step 0.5:  moved (%+.1f, %+.1f) -> (%.1f, %.1f), mean sat %.3f"
      % (best[3], best[4], best[1], best[2], best[0]))
for r, l, s, n in radial(PL, PS, best[1], best[2], 40):
    tag = ""
    if r <= 14: tag = "  [SPEC r0-7  -> hubcap, sat 0.70-0.83]"
    elif r <= 20: tag = "  [SPEC r7-10 -> pale annulus, lum ~169, sat ~0.27]"
    elif 24 <= r <= 35: tag = "  [SPEC r12-17-> tyre, lum 34-93, sat <0.08]"
    print("  r %2d  lum %6.1f  sat %.3f%s" % (r, l, s, tag))
