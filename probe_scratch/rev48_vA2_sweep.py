#!/usr/bin/env python3.11
"""Is the estimator's bias additive, multiplicative, or neither?
Generate the decal at several LINE_GAP values (never touching tex/), measure the
TRUE gap/cap off the full-res raster, then run probe_rev47_gap's own estimator on
the same decal downsampled to the photograph's scale."""
import sys, math, importlib.util, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None
sys.path.insert(0,"/home/user/combi_render")
import os; os.chdir("/home/user/combi_render")

spec = importlib.util.spec_from_file_location("cg","/home/user/combi_render/cal_gen.py")
cg = importlib.util.module_from_spec(spec); spec.loader.exec_module(cg)

# ---- the probe's estimator, verbatim ----
def bands(ty, Z, lo=-45.0, hi=10.0):
    best=None
    for ang in np.arange(lo,hi,0.5):
        rot = nd.rotate(ty.astype(float),ang,reshape=True,order=1)>0.5
        prof = rot.sum(1); nz=np.nonzero(prof)[0]
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

def type_mask(img,Z):
    big=img.resize((img.width*Z,img.height*Z),Image.LANCZOS)
    a=np.asarray(big.convert("RGB"),np.float32)
    R,G,B=a[...,0],a[...,1],a[...,2]
    mx=a.max(2); sat=(mx-a.min(2))/np.maximum(mx,1)
    red=(R>90)&(R-G>40)&(R-B>25)
    burst=nd.binary_fill_holes(nd.binary_closing(red,np.ones((9,9))))
    lab,n=nd.label(burst)
    if n>1:
        burst=lab==(int(np.argmax(nd.sum(burst,lab,range(1,n+1))))+1)
    ty=nd.binary_opening(burst&(mx>150)&(sat<0.30),np.ones((5,5)))
    return ty,burst

def build(line_gap):
    cg.LINE_GAP = line_gap
    cg.LINE_SEP = cg.LINE_SEP_BASE + line_gap*cg.CAP_100
    w,h = cg.w, cg.h
    img=Image.new("RGBA",(w,h),(0,0,0,0)); d=ImageDraw.Draw(img)
    cx,cy,RO=cg.starburst(d)
    img=cg.gradient(img,cx,cy); d=ImageDraw.Draw(img)
    sx,sy,sr=w*0.075,h*0.60,h*0.085
    sp=[]
    for i in range(10):
        a=math.pi*i/5-math.pi/2; r=sr if i%2==0 else sr*0.42
        sp.append((sx+r*math.cos(a),sy+r*math.sin(a)))
    d.polygon(sp,fill=cg.PINK+(255,))
    t=cg.TypeMask(w,h); _pre=cg._type_centroid()
    SH=(cg.BURST_CX-_pre[0],cg.BURST_CY-_pre[1]); cg._place(t,SH)
    lay=Image.merge("RGBA",(Image.new("L",(w,h),cg.WHITE[0]),Image.new("L",(w,h),cg.WHITE[1]),
                            Image.new("L",(w,h),cg.WHITE[2]),t.m))
    lay=lay.rotate(-math.degrees(cg.ANG),resample=Image.BICUBIC,center=(w*cg.BURST_CX,h*cg.BURST_CY))
    img=Image.alpha_composite(img,lay)
    return img.resize((cg.W,cg.H),Image.LANCZOS)

def truth_from_raster(im):
    H=im.height
    a=np.asarray(im).astype(float); al=a[:,:,3]/255.0
    wm=(al>0.5)&(a[:,:,0]>200)&(a[:,:,1]>195)&(a[:,:,2]>190)
    rot=nd.rotate(wm.astype(float),-19.7,reshape=True,order=1)>0.5
    prof=rot.sum(1); nz=np.nonzero(prof)[0]
    seg,run=[],None
    for i in range(nz.min(),nz.max()+2):
        p=prof[i] if i<len(prof) else 0
        if p>0 and run is None: run=i
        if p==0 and run is not None: seg.append((run,i-1)); run=None
    seg=[s for s in seg if s[1]-s[0]+1>3]
    if len(seg)<2: return None
    cap=seg[0][1]-seg[0][0]+1; gap=seg[1][0]-seg[0][1]-1
    return gap/cap, cap/H, gap/H

print("%-9s %-10s %-9s %-9s %-9s %-9s %-8s" % ("LINE_GAP","true g/c","capC","gapC","read g/c","read-true","read/true"))
for lg in (0.24,0.28,0.32,0.36,0.43,0.50,0.57,0.64):
    im=build(lg)
    tr=truth_from_raster(im)
    k=44.0/float(im.width)*3.0
    small=im.convert("RGB").resize((max(8,int(im.width*k)),max(8,int(im.height*k))),Image.LANCZOS)
    ty,_=type_mask(small,8); rb=bands(ty,8)
    if tr is None: print("%-9.2f  NO TWO BANDS in full-res raster"%lg); continue
    if rb is None: print("%-9.2f %-10.4f %-9.4f %-9.4f  estimator: NO TWO BANDS"%(lg,tr[0],tr[1],tr[2])); continue
    print("%-9.2f %-10.4f %-9.4f %-9.4f %-9.4f %+-9.4f %-8.3f"
          % (lg,tr[0],tr[1],tr[2],rb[0],rb[0]-tr[0],rb[0]/tr[0]))
