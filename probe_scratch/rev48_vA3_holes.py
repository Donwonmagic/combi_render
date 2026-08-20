import numpy as np
from PIL import Image
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None
def bands(ty,Z,lo=-55.,hi=15.):
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
def holes(f,box,Z,tag,rg=30,R0=75,save=None):
    im=Image.open(f).convert("RGB").crop(box)
    big=im.resize((im.width*Z,im.height*Z),Image.LANCZOS)
    a=np.asarray(big,np.float32); R,G,B=a[...,0],a[...,1],a[...,2]
    red=(R>R0)&(R-G>rg)&(R-B>rg*0.5)
    red=nd.binary_closing(red,np.ones((3*Z//2,3*Z//2)))
    lab,n=nd.label(red)
    red=lab==(int(np.argmax(nd.sum(red,lab,range(1,n+1))))+1)
    fill=nd.binary_fill_holes(red)
    h=fill&~red
    h=nd.binary_opening(h,np.ones((Z//2,Z//2)))
    lab,n=nd.label(h)
    if n:
        sz=nd.sum(h,lab,range(1,n+1))
        h=np.isin(lab,[i+1 for i in range(n) if sz[i]>Z*Z*3])
    ys,xs=np.nonzero(fill)
    print("%-12s burst %.1f x %.1f   holepx %d  ncomp %d"%(tag,(xs.ptp()+1)/Z,(ys.ptp()+1)/Z,h.sum(),nd.label(h)[1]))
    r=bands(h,Z)
    print("            ",("gap/cap %.3f  ang %.1f  cap %.2f  gap %.2f"%r) if r else "NOT SEPARABLE")
    if save:
        o=np.zeros(h.shape+(3,),np.uint8); o[...,0]=fill*80; o[...,1]=h*255; o[...,2]=h*255
        Image.fromarray(o).resize((im.width*4,im.height*4)).save(save)
    return r
holes("ref_side.jpg",(728,300,845,392),8,"side RED",save="probe_scratch/rev48_vA3_h_side.png")
holes("ref_rear34.jpg",(748,288,862,378),8,"rear34 RED",save="probe_scratch/rev48_vA3_h_rear.png")
holes("IMG_2073.jpeg",(1108,360,1210,445),8,"2073 GREEN",save="probe_scratch/rev48_vA3_h_2073.png")
