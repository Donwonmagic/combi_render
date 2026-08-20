#!/usr/bin/env python3.11
"""Measure clear gap + cap height straight off the shipped tex/calidad.png."""
import math, numpy as np
from PIL import Image
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None

im = Image.open("/home/user/combi_render/tex/calidad.png").convert("RGBA")
W,H = im.size
a = np.asarray(im).astype(float)
al = a[:,:,3]/255.0
wm = (al>0.5)&(a[:,:,0]>200)&(a[:,:,1]>195)&(a[:,:,2]>190)
print("canvas %dx%d  white-type px %d" % (W,H,wm.sum()))

for ang in (19.7,):
    # cal_gen rotated the type layer by -degrees(ANG) = +19.7 (PIL CCW).
    # Undo with -19.7 in PIL terms.
    rot = nd.rotate(wm.astype(float), -ang, reshape=True, order=1) > 0.5
    prof = rot.sum(1)
    nz = np.nonzero(prof)[0]
    seg=[];run=None
    for i in range(nz.min(), nz.max()+2):
        p = prof[i] if i < len(prof) else 0
        if p>0 and run is None: run=i
        if p==0 and run is not None: seg.append((run,i-1)); run=None
    seg=[s for s in seg if s[1]-s[0]+1 > 3]
    print("de-rot %+.1f deg: %d segments: %s" % (-ang, len(seg), seg))
    if len(seg)>=2:
        cap_px = seg[0][1]-seg[0][0]+1
        gap_px = seg[1][0]-seg[0][1]-1
        cal_px = seg[1][1]-seg[1][0]+1
        print("   '100%%' cap %d px = %.4f canvas-H ; clear gap %d px = %.4f canvas-H ; 'Calidad' %d px"
              % (cap_px, cap_px/H, gap_px, gap_px/H, cal_px))
        print("   RASTER gap/cap = %.4f" % (gap_px/cap_px))
