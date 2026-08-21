import numpy as np
from PIL import Image
A,B,C = 641220.4, 11140.0, 55.0322
KT=215.5; U_RHUB=749.38
def fX(u): return A/(np.asarray(u,float)+B)-C
def mpp(u): return A/(np.asarray(u,float)+B)**2
def kv(u): return KT*mpp(U_RHUB)/mpp(u)
im=np.asarray(Image.open('ref_side.jpg').convert('RGB'),float)
lum=im.mean(2)
# narrow windows, detrended, print
def prof(c0,c1,r0=436,r1=496):
    p=lum[r0:r1,c0:c1].mean(1)
    t=np.convolve(p,np.ones(9)/9,'same')
    d=p-t
    return p,d
for c0 in range(768,836,8):
    p,d=prof(c0,c0+6)
    s="".join("%+ .0f "%v for v in d)
    print("cols %d-%d"%(c0,c0+6))
    print("  ", " ".join("%d:%+.1f"%(436+i,v) for i,v in enumerate(d)))
