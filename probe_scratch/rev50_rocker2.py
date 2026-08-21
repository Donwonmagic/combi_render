"""The rocker trim strip in ref_side.jpg: a NEUTRAL bright line at the foot of the
red flank.  Detector: within the band z 0.28..0.46 above ground, the row of maximum
luminance whose G/R > 0.45 (i.e. NOT body red).  Reported in metres above ground via
SPEC 10.34 k_t carried off the rear hub, datum z = TIRE_R by construction."""
import numpy as np
from PIL import Image
A,B,C=641220.4,11140.0,55.0322; KT=215.5; U_RHUB=749.38
fX=lambda u: A/(np.asarray(u,float)+B)-C
mpp=lambda u: A/(np.asarray(u,float)+B)**2
kv=lambda u: KT*mpp(U_RHUB)/mpp(u)
vhub=lambda u: 604.0-0.0087*(u-749.6)
im=np.asarray(Image.open('ref_side.jpg').convert('RGB'),float)
zs=[];lums=[];grs=[];reds=[]
for u in range(340,665,5):
    r0=int(vhub(u)-(0.46-0.3325)*kv(u)); r1=int(vhub(u)-(0.28-0.3325)*kv(u))
    seg=im[r0:r1,u]; lum=seg.mean(1); gr=seg[:,1]/np.maximum(seg[:,0],1)
    ok=gr>0.45
    if not ok.any(): continue
    i=int(np.argmax(np.where(ok,lum,-1)))
    z=0.3325+(vhub(u)-(r0+i))/kv(u)
    # red paint reference 6 px above
    rp=im[r0+i-6,u]
    zs.append(z); lums.append(lum[i]); grs.append(gr[i]); reds.append(rp.mean())
zs=np.array(zs);lums=np.array(lums);grs=np.array(grs);reds=np.array(reds)
print("n=%d cols (X +0.82 .. -0.66)"%len(zs))
print("strip z above ground: mean %.4f  sd %.4f  min %.4f max %.4f"%(zs.mean(),zs.std(),zs.min(),zs.max()))
print("strip luminance      : mean %.1f   red paint 6 px above: mean %.1f   ratio %.2fx"%(lums.mean(),reds.mean(),lums.mean()/reds.mean()))
print("strip G/R            : mean %.3f  (body red G/R measured 0.08-0.18 in the same columns)"%grs.mean())
print()
print("MODEL: T.ZB above ground at the same stations (authored ZB minus rake_drop):")
ZB=[(-2.108,0.468),(-2.086,0.432),(-2.050,0.408),(-2.000,0.394),(-1.900,0.393),
    (-1.600,0.387),(-1.200,0.386),(-0.400,0.385),(0.400,0.385),(1.000,0.387),
    (1.500,0.391),(1.800,0.397),(1.960,0.408),(2.040,0.430),(2.085,0.470),(2.108,0.520)]
import bisect
def zb(x):
    xs=[p[0] for p in ZB]; ys=[p[1] for p in ZB]
    return float(np.interp(x,xs,ys))
for X in (0.80,0.40,0.00,-0.40,-0.66):
    print("   X %+5.2f  ZB_AG %.4f"%(X,zb(X)-(0.047925+0.017750*X)))
