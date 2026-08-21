"""rev50 nose/front -- DOES THE V SWAGE READ AS A PRESSED CREASE?

Sample luminance along short segments perpendicular to the cream/red V break,
on the RED side only, and report L(d) / L(d=12..20 px) for d = 1..20 px out.
A pure paint edge gives a flat profile (~1.00 everywhere past the edge blur).
A pressed crease gives a bright or dark band in the first few px.

Frames: ref_nolita_front34.jpg (RED bus, different artwork state -- the V
break and the swage under it are GEOMETRY, the colours are paint) and
out/r49s_hero34f.png (the shipped render).  The two are NOT the same lighting,
so the SIGN of the band is not comparable; its AMPLITUDE is what is compared,
and a render with no band at all cannot be explained by lighting.

CEILING: the break's position per scanline is found by a 50 % crossing on
(R-G).  JPEG ringing on a high-contrast diagonal can manufacture a 1-2 px
overshoot; that is why d=1 and d=2 are printed separately from d>=3, and why
the render (PNG, no JPEG) is the arm that must show the band if it is real.
"""
import numpy as np
from PIL import Image

def profile(path, box, sgn, label):
    im = np.asarray(Image.open(path).convert('RGB')).astype(float)
    L = im @ np.array([0.299, 0.587, 0.114])
    RG = im[..., 0] - im[..., 1]
    x0, y0, x1, y1 = box
    prof = np.zeros(24); n = np.zeros(24)
    used = 0
    for y in range(y0, y1):
        row = RG[y, x0:x1]
        lo = row[:4].mean(); hi = row[-4:].mean()      # cream -> red along +x
        if hi - lo < 30:
            continue
        thr = 0.5*(lo+hi)
        idx = np.nonzero(row > thr)[0]
        if len(idx) == 0 or idx[0] == 0:
            continue
        e = x0 + idx[0]
        used += 1
        for d in range(1, 24):
            xx = e + sgn*d
            if 0 <= xx < im.shape[1]:
                prof[d] += L[y, xx]; n[d] += 1
    p = prof/np.maximum(n,1)
    base = p[14:22].mean()
    print("%-28s rows=%d  base L=%.1f" % (label, used, base))
    print("   d :  " + " ".join("%5d" % d for d in range(1,14)))
    print("  L/b:  " + " ".join("%5.3f" % (p[d]/base) for d in range(1,14)))
    print("   peak deviation d=3..10 : %+.1f %%" %
          (100*(max(p[3:11]/base, key=lambda v: abs(v-1))-1)))

# ref_nolita_front34: the V's NEAR arm.  Scan rows y 250..300, x 185..225,
# cream on the left, red on the right.
profile('ref_nolita_front34.jpg', (183, 250, 226, 300), +1, 'PHOTO nolita_front34 near arm')
# the render: same arm.  hero34f nose, cream left / red right, rows 760..840
profile('out/r49s_hero34f.png',   (470, 760, 545, 845), +1, 'RENDER r49s_hero34f near arm')

# --- second frame, GREEN bus (geometry only): cream -> green, use (G-R)
def profile2(path, box, label):
    im = np.asarray(Image.open(path).convert('RGB')).astype(float)
    L = im @ np.array([0.299, 0.587, 0.114])
    GR = im[..., 1] - im[..., 0]
    x0, y0, x1, y1 = box
    prof = np.zeros(24); n = np.zeros(24); used=0
    for y in range(y0, y1):
        row = GR[y, x0:x1]
        lo = row[:4].mean(); hi = row[-4:].mean()
        if hi - lo < 15: continue
        thr = 0.5*(lo+hi)
        idx = np.nonzero(row > thr)[0]
        if len(idx)==0 or idx[0]==0: continue
        e = x0+idx[0]; used+=1
        for d in range(1,24):
            prof[d]+=L[y,e+d]; n[d]+=1
    p=prof/np.maximum(n,1); base=p[14:22].mean()
    print("%-28s rows=%d base L=%.1f"%(label,used,base))
    print("   d :  "+" ".join("%5d"%d for d in range(1,14)))
    print("  L/b:  "+" ".join("%5.3f"%(p[d]/base) for d in range(1,14)))
profile2('ref_workshop.jpg', (325, 570, 400, 640), 'PHOTO workshop GREEN near arm')
