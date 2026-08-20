import numpy as np
from PIL import Image
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None

def bands(ty, Z, lo=-50.0, hi=10.0):
    best=None
    for ang in np.arange(lo,hi,0.5):
        rot = nd.rotate(ty.astype(float), ang, reshape=True, order=1) > 0.5
        prof = rot.sum(1); nz=np.nonzero(prof)[0]
        if len(nz)==0: continue
        seg,run=[],None
        for i in range(nz.min(), nz.max()+2):
            p = prof[i] if i < len(prof) else 0
            if p>0 and run is None: run=i
            if p==0 and run is not None: seg.append((run,i-1)); run=None
        seg=[s for s in seg if (s[1]-s[0]+1) > Z*1.5]
        if len(seg)!=2: continue
        cap=(seg[0][1]-seg[0][0]+1)/Z; gap=(seg[1][0]-seg[0][1]-1)/Z
        if gap<=0: continue
        if best is None or gap>best[3]: best=(gap/cap,ang,cap,gap)
    return best

def run(f, box, Z=8, tag="", rg=35, R0=80, mxT=150, satT=0.30, save=None):
    im = Image.open(f).convert("RGB").crop(box)
    big = im.resize((im.width*Z, im.height*Z), Image.LANCZOS)
    a = np.asarray(big.convert("RGB"), np.float32)
    R,G,B = a[...,0],a[...,1],a[...,2]
    mx=a.max(2); sat=(mx-a.min(2))/np.maximum(mx,1)
    red = (R>R0)&(R-G>rg)&(R-B>rg*0.6)
    burst = nd.binary_fill_holes(nd.binary_closing(red, np.ones((9,9))))
    lab,n = nd.label(burst)
    if n>1:
        burst = lab==(int(np.argmax(nd.sum(burst,lab,range(1,n+1))))+1)
    ty = nd.binary_opening(burst & (mx>mxT)&(sat<satT), np.ones((5,5)))
    ys,xs=np.nonzero(burst)
    print("%-12s burst %.1f x %.1f native px  typepx %d" % (tag,(xs.max()-xs.min()+1)/Z,(ys.max()-ys.min()+1)/Z, ty.sum()))
    r = bands(ty,Z)
    print("             ", ("gap/cap %.3f  ang %.1f  cap %.2f px  gap %.2f px"%r) if r else "NOT SEPARABLE")
    if save:
        out = np.zeros(burst.shape+(3,),np.uint8)
        out[...,0]=burst*120; out[...,1]=ty*255; out[...,2]=ty*255
        Image.fromarray(out).resize((im.width*3,im.height*3)).save(save)
    return r

run("IMG_2073.jpeg",(1108,360,1210,445),tag="2073 GREEN",save="probe_scratch/rev48_vA3_mask_2073.png")
run("ref_side.jpg",(725,295,850,395),tag="side RED",save="probe_scratch/rev48_vA3_mask_side.png")
run("ref_rear34.jpg",(745,285,865,380),tag="rear34 RED",save="probe_scratch/rev48_vA3_mask_rear34.png")
