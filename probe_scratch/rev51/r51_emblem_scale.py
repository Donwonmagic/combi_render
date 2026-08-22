"""rev 51 -- emblem diameter / hubcap diameter, render vs photographs.
MASKS ARE PAINTED AND SAVED BEFORE ANY NUMBER IS QUOTED (rule, this revision)."""
import numpy as np, math
from scipy import ndimage
from PIL import Image

def cap_and_emblem(path, cx, cy, rmax_px, tag):
    im = np.asarray(Image.open(path).convert('RGB'), float)
    H, W, _ = im.shape
    R, G, B = im[:,:,0], im[:,:,1], im[:,:,2]
    mx, mn = im.max(2), im.min(2)
    sat = np.where(mx > 0, (mx-mn)/np.maximum(mx,1), 0)
    L = 0.2126*R + 0.7152*G + 0.0722*B
    yy, xx = np.mgrid[0:H, 0:W]
    rr = np.hypot(xx-cx, yy-cy)

    # CAP: red, within rmax
    cap = (rr < rmax_px) & (R > 90) & (G < 0.72*R)
    # EMBLEM: pale / low-sat, INSIDE the cap's own radius (a CIRCLE, not a bbox --
    # the rev-51 defect was using a rectangle and catching the rim ring)
    cap_r = np.percentile(rr[cap], 98) if cap.sum() > 50 else 0
    raw = (rr < 0.55*cap_r) & (sat < 0.45) & (L > 0.9*np.median(L[cap]))
    # THE EMBLEM IS ONE COMPACT BLOB ON THE CAP AXIS.  A specular streak is a
    # SEPARATE, elongated blob and my first version merged the two -- visible in
    # PAINT_emblem_masks.png as a lump reaching up-left out of the badge.  Take the
    # connected component whose centroid is nearest the cap centre, nothing else.
    lab, n = ndimage.label(raw)
    if n == 0: return cap, raw, cap_r, rr, im
    best, bestd = None, 1e18
    for i in range(1, n+1):
        m = lab == i
        if m.sum() < 8: continue
        d = math.hypot(xx[m].mean()-cx, yy[m].mean()-cy)
        if d < bestd: bestd, best = d, m
    emb = raw if best is None else best
    return cap, emb, cap_r, rr, im

FRAMES = [
    ("RENDER r51c side, rear", 'out/r51c_side.png', 1098.3, 872.0, 42.0),
    ("RENDER r51c side, front",'out/r51c_side.png',  447.5, 872.0, 42.0),
    ("PHOTO ref_side, rear",   'ref_side.jpg',       749.4, 604.3, 34.0),
]
print("%-26s cap_D_px  emb_D_px   emb/cap" % "frame")
paint = []
for tag, path, cx, cy, rmax in FRAMES:
    cap, emb, cap_r, rr, im = cap_and_emblem(path, cx, cy, rmax, tag)
    if emb.sum() < 8:
        print("%-26s  emblem mask empty (%d px) -- NOT QUOTED" % (tag, emb.sum())); continue
    emb_r = np.percentile(rr[emb], 98)
    print("%-26s %7.2f  %8.2f   %.4f" % (tag, 2*cap_r, 2*emb_r, emb_r/cap_r))
    vis = im.copy(); vis[cap] = 0.45*vis[cap] + 0.55*np.array([255,60,60])
    vis[emb] = np.array([0,255,0])
    x0,x1 = int(cx-rmax-8), int(cx+rmax+8); y0,y1 = int(cy-rmax-8), int(cy+rmax+8)
    paint.append((Image.fromarray(vis[y0:y1, x0:x1].astype('uint8')).resize((300,300), Image.NEAREST), tag))

c = Image.new('RGB', (300*len(paint)+20*(len(paint)+1), 340), (255,255,255))
for i,(p,t) in enumerate(paint): c.paste(p, (20+i*320, 10))
c.save('probe_scratch/rev51/PAINT_emblem_masks.png')
print("\nPAINTED: probe_scratch/rev51/PAINT_emblem_masks.png  (red = cap mask, GREEN = emblem mask)")
print("built constant: CAP_EMBLEM_D / CAP_D = 0.3170  (declared measured 0.317 +- 0.017)")
