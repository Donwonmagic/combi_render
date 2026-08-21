"""The ROCKER TRIM RIDGE: present, bright and sub-pixel-fittable in ref_side.jpg;
absent from the render.  Ridge detector = local vertical LAPLACIAN maximum (a bright
line 1-2 px wide on a darker field), searched in a band around the model's own ZB.
Both frames get the identical detector and the identical band in METRES."""
import numpy as np, ast
from PIL import Image
import scipy.ndimage as nd
A,B,C=641220.4,11140.0,55.0322; KT=215.5; U_RHUB=749.38
fX=lambda u: A/(np.asarray(u,float)+B)-C
fu=lambda x: A/(np.asarray(x,float)+C)-B
mpp=lambda u: A/(np.asarray(u,float)+B)**2
kv=lambda u: KT*mpp(U_RHUB)/mpp(u)
vhub=lambda u: 604.0-0.0087*(np.asarray(u,float)-749.6)
def ridge(a,c,r0,r1):
    s=nd.gaussian_filter1d(a[r0:r1,c],0.8)
    l=-nd.laplace(s)           # positive on a bright line
    i=int(np.argmax(l))
    return r0+i, float(l[i]), float(s[i])
ref=np.asarray(Image.open('ref_side.jpg').convert('RGB'),float).mean(2)
gen=np.asarray(Image.open('out/r49board_side.png').convert('RGB'),float).mean(2)
ppm=1600/5.90
print("REF ridge search, band z 0.28..0.46 above ground")
vals=[]
for X in np.arange(0.9,-1.15,-0.10):
    u=int(round(float(fu(X))))
    r0=int(vhub(u)-(0.46-0.3325)*kv(u)); r1=int(vhub(u)-(0.28-0.3325)*kv(u))
    v,st,br=ridge(ref,u,r0,r1)
    z=0.3325+(vhub(u)-v)/kv(u); vals.append((X,z,st,br))
    print("  X %+5.2f u %3d  row %d  z %.4f  ridge strength %6.2f  peak lum %5.1f"%(X,u,v,z,st,br))
zs=np.array([v[1] for v in vals]); st=np.array([v[2] for v in vals])
print("  ridge z above hub: front-half %+.4f  rear-half %+.4f   (t1_core METHOD 4: -0.0004 / +0.0422)"
      %(zs[:5].mean()-0.3325, zs[-5:].mean()-0.3325))
print("  median ridge strength REF %.2f"%np.median(st))
print()
print("RENDER same band, same detector")
st2=[]
for X in np.arange(0.9,-1.15,-0.10):
    c=int(round(800-ppm*X))
    r0=int(550+ppm*1.52-ppm*0.46); r1=int(550+ppm*1.52-ppm*0.28)
    v,s2,br=ridge(gen,c,r0,r1)
    z=(550+ppm*1.52-v)/ppm; st2.append(s2)
    print("  X %+5.2f col %4d row %d  z %.4f  ridge strength %6.2f  peak lum %5.1f"%(X,c,v,z,s2,br))
print("  median ridge strength GEN %.2f"%np.median(st2))
