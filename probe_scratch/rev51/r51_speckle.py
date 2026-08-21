"""rev 51 -- A6 baseline. Chip/speckle coverage on cream surfaces, render vs photograph.

Statistic: fraction of pixels more than 6 % below their own LOCAL median (box 25 px
at the render's scale, scaled to px/m on each image so the physical box matches).
Local median, not a global tone, so a lighting gradient cannot manufacture coverage.

CONTROLS, run first:
  (1) a synthetic FLAT cream patch + gaussian noise at the render's own MC noise
      level -> must return ~0 %.  If it does not, the threshold is inside the noise.
  (2) a synthetic cream patch WITH known 5 % dark-chip coverage -> must return ~5 %.
  (3) the shell's own nose cream in the SAME render, SAME material family -- the
      survey's internal control, which must come back near zero if the mechanism is
      pointiness-on-unsubdivided-meshes and not a global paint setting.
"""
import numpy as np
from PIL import Image
from scipy.ndimage import median_filter

def cov(a, box, frac=0.06):
    L = a.astype(float)
    m = median_filter(L, size=box)
    r = (L - m) / np.maximum(m, 1e-6)
    return (r < -frac).mean()*100.0, (r > frac).mean()*100.0, np.percentile(r,2), np.percentile(r,98)

def lum(im):
    a = np.asarray(im.convert('RGB'), float)
    return 0.2126*a[:,:,0] + 0.7152*a[:,:,1] + 0.0722*a[:,:,2]

rng = np.random.default_rng(7)
print("CONTROLS")
flat = np.full((300,600), 190.0) + rng.normal(0, 0.5, (300,600))   # MC noise ~0.5 DN
d,b,p2,p98 = cov(flat, 25); print("  flat cream + 0.5 DN noise      dark %5.2f %%  bright %5.2f %%  (expect ~0)" % (d,b))
chip = np.full((300,600), 190.0) + rng.normal(0, 0.5, (300,600))
mask = rng.random((300,600)) < 0.0
# 5 % coverage as ~40 blobs
yy,xx = np.mgrid[0:300,0:600]
for _ in range(60):
    cy,cx = rng.integers(0,300), rng.integers(0,600)
    mask |= ((yy-cy)**2 + (xx-cx)**2) < 9.0**2
chip[mask] *= 0.85
d,b,p2,p98 = cov(chip, 25); print("  flat cream + %.1f %% dark chips  dark %5.2f %%  bright %5.2f %%  (expect ~%.1f)" % (mask.mean()*100, d,b, mask.mean()*100))

REN = 'out/r51b_side.png'
ren = Image.open(REN)
PPM_REN = 271.1864
PPM_REF = 211.5
box_ren = 25
box_ref = max(3, int(round(25*PPM_REF/PPM_REN)))
print("\nlocal-median box: render %d px, photograph %d px  (same %.0f mm on the vehicle)"
      % (box_ren, box_ref, 25/PPM_REN*1000))

print("\nRENDER  %s" % REN)
wins_ren = {
  "counter fascia (countercream)": (1000, 639, 1270, 656),
  "cab roof cream (shell paint)" : ( 430, 300,  700, 340),
  "flank cream above the bays"   : ( 500, 470,  900, 500),
}
for k,(x0,y0,x1,y1) in wins_ren.items():
    a = lum(ren.crop((x0,y0,x1,y1)))
    d,b,p2,p98 = cov(a, box_ren)
    print("  %-32s dark %6.2f %%  bright %5.2f %%  p2 %+.3f p98 %+.3f  mean L %.1f  win (%d,%d)-(%d,%d)"
          % (k, d, b, p2, p98, a.mean(), x0,y0,x1,y1))

print("\nPHOTOGRAPH  ref_side.jpg  (RED target, current artwork)")
ref = Image.open('ref_side.jpg')
wins_ref = {
  "counter fascia, same feature": (660, 423, 900, 433),
}
for k,(x0,y0,x1,y1) in wins_ref.items():
    a = lum(ref.crop((x0,y0,x1,y1)))
    d,b,p2,p98 = cov(a, box_ref)
    print("  %-32s dark %6.2f %%  bright %5.2f %%  p2 %+.3f p98 %+.3f  mean L %.1f  win (%d,%d)-(%d,%d)"
          % (k, d, b, p2, p98, a.mean(), x0,y0,x1,y1))
