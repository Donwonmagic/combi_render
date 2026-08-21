import numpy as np
from PIL import Image
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None
im = Image.open("tex/calidad.png")
a = np.asarray(im.convert("RGBA"), np.float32)
al=a[...,3]/255.0
wm=(al>0.5)&(a[...,0]>200)&(a[...,1]>195)&(a[...,2]>190)
def band(mask, ang, minh=3):
    rot = nd.rotate(mask.astype(float), ang, reshape=True, order=1) > 0.5
    prof=rot.sum(1); nz=np.nonzero(prof)[0]
    if len(nz)==0: return None
    seg,run=[],None
    for i in range(nz.min(), nz.max()+2):
        p=prof[i] if i<len(prof) else 0
        if p>0 and run is None: run=i
        if p==0 and run is not None: seg.append((run,i-1)); run=None
    seg=[s for s in seg if s[1]-s[0]+1>minh]
    return seg
for ang in (-19.7,-19.0,-20.0,19.7):
    seg=band(wm,ang)
    out=""
    if seg and len(seg)==2:
        cap=seg[0][1]-seg[0][0]+1; gap=seg[1][0]-seg[0][1]-1
        out=" cap %d gap %d gap/cap %.4f"%(cap,gap,gap/cap)
    print("%+6.1f : %d bands %s%s"%(ang,len(seg) if seg else 0,seg,out))
best=None
for ang in np.arange(-30,-8,0.25):
    seg=band(wm,ang)
    if not seg or len(seg)!=2: continue
    cap=seg[0][1]-seg[0][0]+1; gap=seg[1][0]-seg[0][1]-1
    if gap<=0: continue
    if best is None or gap>best[3]: best=(gap/cap,ang,cap,gap)
print("full-res max-gap sweep:",best)
