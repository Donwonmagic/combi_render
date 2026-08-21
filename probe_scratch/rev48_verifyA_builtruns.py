import numpy as np
from PIL import Image
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None
def type_mask(img,Z):
    big=img.resize((img.width*Z,img.height*Z),Image.LANCZOS)
    a=np.asarray(big.convert("RGB"),np.float32)
    R,G,B=a[...,0],a[...,1],a[...,2]
    mx=a.max(2);sat=(mx-a.min(2))/np.maximum(mx,1)
    red=(R>90)&(R-G>40)&(R-B>25)
    burst=nd.binary_fill_holes(nd.binary_closing(red,np.ones((9,9))))
    lab,n=nd.label(burst)
    if n>1: burst=lab==(int(np.argmax(nd.sum(burst,lab,range(1,n+1))))+1)
    return nd.binary_opening(burst&(mx>150)&(sat<0.30),np.ones((5,5))),burst
def runs(ty,Z,ang):
    rot=nd.rotate(ty.astype(float),ang,reshape=True,order=1)>0.5
    prof=rot.sum(1);nz=np.nonzero(prof)[0]
    seg,run=[],None
    for i in range(nz.min(),nz.max()+2):
        p=prof[i] if i<len(prof) else 0
        if p>0 and run is None: run=i
        if p==0 and run is not None: seg.append((run,i-1));run=None
    return seg
for tag,path,ang in (("LG 0.26 (pre-1bfc97a)","probe_scratch/rev48_verifyA_calidad_LG026.png",-45.0),
                     ("LG 0.43 (shipped)","tex/calidad.png",-20.0)):
    d=Image.open(path).convert("RGB")
    k=44/float(d.width)*3.0
    sm=d.resize((int(d.width*k),int(d.height*k)),Image.LANCZOS)
    ty,bu=type_mask(sm,8)
    s=runs(ty,8,ang)
    print("%s  @ probe's winning angle %+.1f"%(tag,ang))
    print("   ALL runs (native px): %s"%[(a,b,round((b-a+1)/8.,2)) for a,b in s])
    kept=[x for x in s if (x[1]-x[0]+1)>12]
    print("   KEPT: %s"%[(a,b,round((b-a+1)/8.,2)) for a,b in kept])
    if len(kept)==2:
        cap=(kept[0][1]-kept[0][0]+1)/8.;gap=(kept[1][0]-kept[0][1]-1)/8.
        print("   -> cap %.2f gap %.2f gap/cap %.4f  (dropped runs inside the gap: %d)"%(
            cap,gap,gap/cap,sum(1 for x in s if kept[0][1]<x[0]<kept[1][0] and x not in kept)))
