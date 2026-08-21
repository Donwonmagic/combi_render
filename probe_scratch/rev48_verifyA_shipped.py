"""Measure the SHIPPED tex/calidad.png raster at full resolution.
De-rotate by the known build angle, band the white type, report gap/cap."""
import numpy as np, math
from PIL import Image
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None
im = Image.open("tex/calidad.png")
a = np.asarray(im.convert("RGBA"), np.float32)
al = a[...,3]/255.0
wm = (al>0.5)&(a[...,0]>200)&(a[...,1]>195)&(a[...,2]>190)
print("shipped raster", im.size, "white type px", int(wm.sum()))
for ang in (19.7,):
    rot = nd.rotate(wm.astype(float), ang, reshape=True, order=1) > 0.5
    prof = rot.sum(1); nz=np.nonzero(prof)[0]
    seg,run=[],None
    for i in range(nz.min(), nz.max()+2):
        p = prof[i] if i<len(prof) else 0
        if p>0 and run is None: run=i
        if p==0 and run is not None: seg.append((run,i-1)); run=None
    segs=[s for s in seg if s[1]-s[0]+1>3]
    print(" de-rot %+.1f deg -> %d bands (>3px): %s" % (ang, len(segs), segs))
    if len(segs)==2:
        cap=segs[0][1]-segs[0][0]+1; gap=segs[1][0]-segs[0][1]-1
        print("   cap %d px  gap %d px  gap/cap %.4f" % (cap,gap,gap/cap))
# also sweep to find max-gap angle at full res (what the estimator would do)
best=None
for ang in np.arange(15.0,25.0,0.25):
    rot = nd.rotate(wm.astype(float), ang, reshape=True, order=1) > 0.5
    prof=rot.sum(1); nz=np.nonzero(prof)[0]
    seg,run=[],None
    for i in range(nz.min(), nz.max()+2):
        p=prof[i] if i<len(prof) else 0
        if p>0 and run is None: run=i
        if p==0 and run is not None: seg.append((run,i-1)); run=None
    seg=[s for s in seg if s[1]-s[0]+1>3]
    if len(seg)!=2: continue
    cap=seg[0][1]-seg[0][0]+1; gap=seg[1][0]-seg[0][1]-1
    if gap<=0: continue
    if best is None or gap>best[3]: best=(gap/cap,ang,cap,gap)
print(" full-res angle sweep best:", best)
