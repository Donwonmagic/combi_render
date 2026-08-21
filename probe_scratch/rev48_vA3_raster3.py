import numpy as np, math
from PIL import Image
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None
d=Image.open("tex/calidad.png").convert("RGB")
a=np.asarray(d,np.float32); H,W=a.shape[:2]
R,G,B=a[...,0],a[...,1],a[...,2]
mx=a.max(2); sat=(mx-a.min(2))/np.maximum(mx,1)
red=(R>90)&(R-G>40)&(R-B>25)
burst=nd.binary_fill_holes(nd.binary_closing(red,np.ones((9,9))))
lab,n=nd.label(burst)
burst=lab==(int(np.argmax(nd.sum(burst,lab,range(1,n+1))))+1)
ty=nd.binary_opening(burst&(mx>150)&(sat<0.30),np.ones((5,5)))
print("canvas %dx%d  burst bbox w %d h %d  type px %d"%(W,H,np.nonzero(burst)[1].ptp()+1,np.nonzero(burst)[0].ptp()+1,ty.sum()))
# de-rotate: sweep, require exactly two bands
best=None
for ang in np.arange(-40,10,0.25):
    rot=nd.rotate(ty.astype(float),ang,reshape=True,order=1)>0.5
    prof=rot.sum(1); nz=np.nonzero(prof)[0]
    if len(nz)==0: continue
    seg,run=[],None
    for i in range(nz.min(),nz.max()+2):
        p=prof[i] if i<len(prof) else 0
        if p>0 and run is None: run=i
        if p==0 and run is not None: seg.append((run,i-1)); run=None
    seg=[s for s in seg if (s[1]-s[0]+1)>10]
    if len(seg)!=2: continue
    cap=seg[0][1]-seg[0][0]+1; gap=seg[1][0]-seg[0][1]-1
    if gap<=0: continue
    if best is None or gap>best[1]: best=(ang,gap,cap,seg)
if best:
    ang,gap,cap,seg=best
    print("FULL RES: ang %.2f  cap %d px = %.4f canvasH  clear gap %d px = %.4f canvasH  gap/cap %.4f"
          %(ang,cap,cap/H,gap,gap/H,gap/cap))
    print("   bands:",seg)
else: print("FULL RES: no two-band split")
