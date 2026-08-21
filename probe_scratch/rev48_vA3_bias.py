"""C-B: is the estimator's bias additive, multiplicative, or neither?
Synthesise the SAME layout the build uses (two staggered words, -19.7 deg, on a
red burst), sweep the TRUE gap/cap, downsample to the photograph's burst size,
and run the probe's own estimator verbatim."""
import numpy as np, math
from PIL import Image, ImageDraw
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None

def bands(ty, Z, lo=-45.0, hi=10.0):          # verbatim from probe_rev47_gap.py
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

def type_mask(img,Z):                          # verbatim
    big=img.resize((img.width*Z,img.height*Z),Image.LANCZOS)
    a=np.asarray(big.convert("RGB"),np.float32)
    R,G,B=a[...,0],a[...,1],a[...,2]
    mx=a.max(2); sat=(mx-a.min(2))/np.maximum(mx,1)
    red=(R>90)&(R-G>40)&(R-B>25)
    burst=nd.binary_fill_holes(nd.binary_closing(red,np.ones((9,9))))
    lab,n=nd.label(burst)
    if n>1: burst=lab==(int(np.argmax(nd.sum(burst,lab,range(1,n+1))))+1)
    ty=nd.binary_opening(burst&(mx>150)&(sat<0.30),np.ones((5,5)))
    return ty,burst

CAP=200; W=1400; H=1100; ANG=-19.7
def make(gapfrac, stagger=0.075):
    """two word bars, cap CAP, true clear gap = gapfrac*CAP, rotated ANG, on a red disc"""
    im=Image.new("RGB",(W,H),(250,246,235)); d=ImageDraw.Draw(im)
    d.ellipse([W*0.09,H*0.09,W*0.91,H*0.91],fill=(200,40,40))
    t=Image.new("L",(W,H),0); td=ImageDraw.Draw(t)
    x0=W*0.24; y0=H*0.34
    td.rectangle([x0,y0,x0+W*0.50,y0+CAP],fill=255)                    # "100%"
    y1=y0+CAP+gapfrac*CAP
    td.rectangle([x0+W*stagger,y1,x0+W*stagger+W*0.50,y1+CAP],fill=255) # "Calidad"
    t=t.rotate(-ANG,resample=Image.BICUBIC,center=(W/2,H/2))
    im=Image.composite(Image.new("RGB",(W,H),(255,255,255)),im,t.point(lambda v:255 if v>127 else 0))
    return im

print(" true    read44  read101   read/true   read-true")
rows=[]
for g in [0.05,0.10,0.111,0.15,0.20,0.25,0.2776,0.30,0.35]:
    im=make(g)
    out=[]
    for target in (44,101):
        k=target/float(W)*(W/ (W*0.82))   # burst is 0.82 of canvas width
        sm=im.resize((max(8,int(W*k)),max(8,int(H*k))),Image.LANCZOS)
        r=bands(type_mask(sm,8)[0],8)
        out.append(r[0] if r else float('nan'))
    print("  %.4f  %.4f  %.4f   %.3f      %+.4f"%(g,out[0],out[1],out[0]/g,out[0]-g))
    rows.append((g,out[0]))
