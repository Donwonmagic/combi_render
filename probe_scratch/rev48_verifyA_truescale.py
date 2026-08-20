"""Calibrate at the PHOTOGRAPH'S ACTUAL scale (burst 61 px tall, x-squashed to
43.6/61) with a despeckled mask, and invert the photograph's reading."""
import sys, math, importlib.util
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None
spec=importlib.util.spec_from_file_location("cg","/home/user/combi_render/cal_gen.py")
cg=importlib.util.module_from_spec(spec); spec.loader.exec_module(cg)

def type_mask(img,Z):
    big=img.resize((img.width*Z,img.height*Z),Image.LANCZOS)
    a=np.asarray(big.convert("RGB"),np.float32)
    R,G,B=a[...,0],a[...,1],a[...,2]
    mx=a.max(2);sat=(mx-a.min(2))/np.maximum(mx,1)
    red=(R>90)&(R-G>40)&(R-B>25)
    burst=nd.binary_fill_holes(nd.binary_closing(red,np.ones((9,9))))
    lab,n=nd.label(burst)
    if n>1: burst=lab==(int(np.argmax(nd.sum(burst,lab,range(1,n+1))))+1)
    ty=nd.binary_opening(burst&(mx>150)&(sat<0.30),np.ones((5,5)))
    return ty,burst
def despeckle(ty,Z,minpx=3.0):
    lab,n=nd.label(ty); sz=nd.sum(ty,lab,range(1,n+1))
    keep=np.zeros(n+1,bool); keep[1:]=sz>(Z*Z*minpx)
    return keep[lab]
def scan(ty,Z,lo=-46,hi=-16,step=0.5):
    """Return list of (ang,cap,gap) for every angle giving EXACTLY 2 runs, no
    length filter that can span dropped runs."""
    out=[]
    for ang in np.arange(lo,hi,step):
        rot=nd.rotate(ty.astype(float),ang,reshape=True,order=1)>0.5
        prof=rot.sum(1);nz=np.nonzero(prof)[0]
        if len(nz)==0: continue
        seg,run=[],None
        for i in range(nz.min(),nz.max()+2):
            p=prof[i] if i<len(prof) else 0
            if p>0 and run is None: run=i
            if p==0 and run is not None: seg.append((run,i-1));run=None
        if len(seg)!=2: continue
        cap=(seg[0][1]-seg[0][0]+1)/Z; gap=(seg[1][0]-seg[0][1]-1)/Z
        if gap<=0: continue
        out.append((ang,cap,gap,gap/cap))
    return out
def report(tag,ty,Z,bh):
    s=scan(ty,Z)
    if not s: print("  %-24s NO two-run angle"%tag); return None
    best=max(s,key=lambda t:t[2])
    caps=[t[1] for t in s]; rs=[t[3] for t in s]
    print("  %-24s two-run angles %.1f..%.1f (%d)  cap %.2f  gap %.2f  gap/cap max %.4f  median %.4f  cap/burstH %.3f"%(
        tag,s[0][0],s[-1][0],len(s),best[1],best[2],max(rs),float(np.median(rs)),best[1]/bh))
    return max(rs), float(np.median(rs))

TARGET_BURST_H=61.0; SQUASH=43.6/61.0
def photoscale(decal):
    W,H=decal.size
    burst_h=0.87*H
    k=TARGET_BURST_H/burst_h
    return decal.convert("RGB").resize((max(8,int(W*k*SQUASH)),max(8,int(H*k))),Image.LANCZOS)

def build(g):
    cg.LINE_GAP=g; cg.LINE_SEP=cg.LINE_SEP_BASE+g*cg.CAP_100
    w,h,W,H=cg.w,cg.h,cg.W,cg.H
    img=Image.new("RGBA",(w,h),(0,0,0,0)); d=ImageDraw.Draw(img)
    cx,cy,RO=cg.starburst(d); img=cg.gradient(img,cx,cy); d=ImageDraw.Draw(img)
    sx,sy,sr=w*0.075,h*0.60,h*0.085; sp=[]
    for i in range(10):
        a=math.pi*i/5-math.pi/2; r=sr if i%2==0 else sr*0.42
        sp.append((sx+r*math.cos(a),sy+r*math.sin(a)))
    d.polygon(sp,fill=cg.PINK+(255,))
    t=cg.TypeMask(w,h); pre=cg._type_centroid()
    cg._place(t,(cg.BURST_CX-pre[0],cg.BURST_CY-pre[1]))
    lay=Image.merge("RGBA",(Image.new("L",(w,h),cg.WHITE[0]),Image.new("L",(w,h),cg.WHITE[1]),
                            Image.new("L",(w,h),cg.WHITE[2]),t.m))
    lay=lay.rotate(-math.degrees(cg.ANG),resample=Image.BICUBIC,center=(w*cg.BURST_CX,h*cg.BURST_CY))
    img=Image.alpha_composite(img,lay).resize((W,H),Image.LANCZOS)
    return img, 0.9804*g-0.14413

print("=== PHOTOGRAPH, despeckled, no span-the-dropped-run bug ===")
im=Image.open("IMG_2073.jpeg").convert("RGB").crop((1108,360,1210,445))
ty,bu=type_mask(im,8); ys,xs=np.nonzero(bu); bh=(ys.max()-ys.min()+1)/8.
report("PHOTO raw mask",ty,8,bh)
ph=report("PHOTO despeckled",despeckle(ty,8),8,bh)
print()
print("=== BUILD at the PHOTOGRAPH'S TRUE scale (burst %.0f px tall, x*%.3f) ==="%(TARGET_BURST_H,SQUASH))
print("%8s %10s   reading"%("LINE_GAP","truth"))
import os
todo=[float(x) for x in sys.argv[1:]] or [0.15,0.20,0.26,0.32,0.43]
for g in todo:
    img,truth=build(g)
    sm=photoscale(img)
    t2,b2=type_mask(sm,8); ys,xs=np.nonzero(b2); bh2=(ys.max()-ys.min()+1)/8.
    print("%8.3f %10.4f  canvas %s burstH %.1f"%(g,truth,sm.size,bh2))
    report("   raw",t2,8,bh2); report("   despeckled",despeckle(t2,8),8,bh2)
