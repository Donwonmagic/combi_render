"""Window / convention sensitivity of the photographed 0.244."""
import sys, numpy as np
from PIL import Image
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None
def bands(ty,Z,lo=-45.0,hi=10.0):
    best=None
    for ang in np.arange(lo,hi,0.5):
        rot=nd.rotate(ty.astype(float),ang,reshape=True,order=1)>0.5
        prof=rot.sum(1); nz=np.nonzero(prof)[0]
        if len(nz)==0: continue
        seg,run=[],None
        for i in range(nz.min(),nz.max()+2):
            p=prof[i] if i<len(prof) else 0
            if p>0 and run is None: run=i
            if p==0 and run is not None: seg.append((run,i-1)); run=None
        seg=[s for s in seg if (s[1]-s[0]+1)>Z*1.5]
        if len(seg)!=2: continue
        cap=(seg[0][1]-seg[0][0]+1)/Z; gap=(seg[1][0]-seg[0][1]-1)/Z
        if gap<=0: continue
        if best is None or gap>best[3]: best=(gap/cap,ang,cap,gap)
    return best
def type_mask(img,Z,thr=150,satmax=0.30):
    big=img.resize((img.width*Z,img.height*Z),Image.LANCZOS)
    a=np.asarray(big.convert("RGB"),np.float32)
    R,G,B=a[...,0],a[...,1],a[...,2]
    mx=a.max(2); sat=(mx-a.min(2))/np.maximum(mx,1)
    red=(R>90)&(R-G>40)&(R-B>25)
    burst=nd.binary_fill_holes(nd.binary_closing(red,np.ones((9,9))))
    lab,n=nd.label(burst)
    if n>1: burst=lab==(int(np.argmax(nd.sum(burst,lab,range(1,n+1))))+1)
    ty=nd.binary_opening(burst&(mx>thr)&(sat<satmax),np.ones((5,5)))
    return ty,burst
src=Image.open("IMG_2073.jpeg").convert("RGB")
print("IMG_2073 size", src.size)
base=(1108,360,1210,445)
print("--- crop window jitter (probe convention: Z=8, thr150, sat0.30) ---")
for d in (0,-8,-4,4,8,12):
    box=(base[0]-d,base[1]-d,base[2]+d,base[3]+d)
    ty,bu=type_mask(src.crop(box),8)
    r=bands(ty,8)
    ys,xs=np.nonzero(bu)
    print("  pad %+3d %s burst %.1fx%.1f -> %s"%(d,box,(xs.max()-xs.min()+1)/8,(ys.max()-ys.min()+1)/8,
        ("gap/cap %.3f ang %.1f cap %.2f gap %.2f"%r) if r else "NO BANDS"))
print("--- brightness threshold jitter (window fixed) ---")
for thr in (130,140,150,160,170,180):
    ty,_=type_mask(src.crop(base),8,thr=thr)
    r=bands(ty,8)
    print("  thr %d -> %s"%(thr,("gap/cap %.3f ang %.1f cap %.2f gap %.2f"%r) if r else "NO BANDS"))
print("--- saturation cut jitter ---")
for s in (0.20,0.25,0.30,0.35,0.40):
    ty,_=type_mask(src.crop(base),8,satmax=s)
    r=bands(ty,8)
    print("  sat<%.2f -> %s"%(s,("gap/cap %.3f ang %.1f cap %.2f gap %.2f"%r) if r else "NO BANDS"))
print("--- Z (upsample factor) jitter ---")
for Z in (4,6,8,10,12):
    ty,_=type_mask(src.crop(base),Z)
    r=bands(ty,Z)
    print("  Z=%d -> %s"%(Z,("gap/cap %.3f ang %.1f cap %.2f gap %.2f"%r) if r else "NO BANDS"))
print("--- angle sweep window jitter (default -45..10) ---")
for lo,hi in ((-45,10),(-30,-10),(-45,45),(-25,-15)):
    ty,_=type_mask(src.crop(base),8)
    r=bands(ty,8,lo,hi)
    print("  sweep %+d..%+d -> %s"%(lo,hi,("gap/cap %.3f ang %.1f cap %.2f gap %.2f"%r) if r else "NO BANDS"))
