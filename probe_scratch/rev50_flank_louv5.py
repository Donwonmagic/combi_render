import numpy as np
from PIL import Image
import scipy.ndimage as nd
A,B,C = 641220.4, 11140.0, 55.0322
def fX(u): return A/(np.asarray(u,float)+B)-C
im=np.asarray(Image.open('ref_side.jpg').convert('RGB'),float); lum=im.mean(2)
hp = lum - nd.uniform_filter1d(lum,9,axis=0)
def energy(r0,r1):
    return np.array([hp[r0:r1,u].std() for u in range(700,900)])
e_blk = energy(443,492)
e_ctl = energy(500,549)   # blank red below
e_ctl2= energy(390,439)   # cream above  (counter/body cream)
print(" col      x(m)   block   below   above")
for i,u in enumerate(range(700,900)):
    if u%2: continue
    print("%4d  %+8.4f  %6.2f  %6.2f  %6.2f  %s"%(u,fX(u),e_blk[i],e_ctl[i],e_ctl2[i],"#"*int(e_blk[i]*3)))

print("\n=== NORMALISED (std of highpass / local mean luminance) ===")
def nrg(r0,r1):
    out=[]
    for u in range(700,900):
        seg=lum[r0:r1,u]; out.append(hp[r0:r1,u].std()/max(seg.mean(),1e-6))
    return np.array(out)
b=nrg(443,492); c1=nrg(500,549); 
for i,u in enumerate(range(700,900)):
    if u%2: continue
    print("%4d %+8.4f  blk %.4f  below %.4f  %s"%(u,fX(u),b[i],c1[i],"#"*int(b[i]*300)))
