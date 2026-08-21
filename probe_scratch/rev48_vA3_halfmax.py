import numpy as np
from PIL import Image
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None

def profile(img, ang, x0, x1, Z=10):
    """img: PIL RGB crop. returns mean-saturation row profile in de-rotated frame,
       sampled at Z subpixels per native px, over native-x window [x0,x1]."""
    a=np.asarray(img,np.float32); mx=a.max(2); mn=a.min(2)
    sat=(mx-mn)/np.maximum(mx,1)
    g=Image.fromarray(np.clip(sat*255,0,255).astype(np.uint8))
    g=g.resize((img.width*Z,img.height*Z),Image.LANCZOS).rotate(-ang,expand=True,resample=Image.BICUBIC)
    A=np.asarray(g,np.float32)/255.
    return A[:,int(x0*Z):int(x1*Z)].mean(1)

def halfmax_bands(p,Z,y0,y1):
    """Between y0,y1 (native), find LOW segments (type) via local half-max crossings."""
    s=nd.uniform_filter1d(p,Z//2)
    i0,i1=int(y0*Z),int(y1*Z)
    seg=s[i0:i1]
    # local extrema
    ext=[]
    for i in range(1,len(seg)-1):
        if seg[i]>=seg[i-1] and seg[i]>seg[i+1]: ext.append((i,'max'))
        if seg[i]<=seg[i-1] and seg[i]<seg[i+1]: ext.append((i,'min'))
    # prune shallow extrema (< 0.05 sat prominence) by alternating merge
    changed=True
    while changed and len(ext)>2:
        changed=False
        for k in range(len(ext)-1):
            if abs(seg[ext[k][0]]-seg[ext[k+1][0]])<0.06:
                del ext[k:k+2]; changed=True; break
    cross=[]
    for k in range(len(ext)-1):
        a,ta=ext[k]; b,tb=ext[k+1]
        if ta==tb: continue
        h=(seg[a]+seg[b])/2
        sub=seg[a:b+1]
        idx=np.nonzero((sub[:-1]-h)*(sub[1:]-h)<=0)[0]
        if len(idx): cross.append(((a+idx[0])/Z+y0, ta))
    return ext,seg,cross

def report(tag,p,Z,y0,y1):
    ext,seg,cross=halfmax_bands(p,Z,y0,y1)
    print("%-22s extrema:"%tag, [(round(i/Z+y0,1),t,round(float(seg[i]),3)) for i,t in ext])
    print("   half-max crossings (native y):", [(round(c,2),t) for c,t in cross])
    ys=[c for c,t in cross]
    if len(ys)>=4:
        cap=ys[1]-ys[0]; gap=ys[2]-ys[1]; cap2=ys[3]-ys[2]
        print("   -> band1(100%%) %.2f px   gap %.2f px   band2(Calidad) %.2f px   gap/cap %.3f"%(cap,gap,cap2,gap/cap))
        return gap/cap
    return None

im=Image.open("ref_side.jpg").convert("RGB").crop((728,300,845,392))
report("side RED",profile(im,19.7,52,94),10,36,96)
im=Image.open("IMG_2073.jpeg").convert("RGB").crop((1108,360,1210,445))
report("2073 GREEN",profile(im,19.7,20,60),10,10,80)
# built raster at both scales
d=Image.open("tex/calidad.png").convert("RGB")
for target,tg in ((44,"BUILT@44"),(101,"BUILT@101")):
    k=target/float(d.width)*3.0
    sm=d.resize((max(8,int(d.width*k)),max(8,int(d.height*k))),Image.LANCZOS)
    print("  (%s canvas %dx%d)"%(tg,sm.width,sm.height))
    report(tg,profile(sm,19.7,0.30*sm.width,0.80*sm.width),10,0,sm.height*1.4)
