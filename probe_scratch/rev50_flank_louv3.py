"""rev50 -- ref_side.jpg louvre block: rake, pitch, phase, extent.
Instruments: SPEC 10.35 flank map (horizontal), SPEC 10.34 k_t carried (vertical),
hub datum z = TIRE_R = 0.3325 by construction.
"""
import numpy as np
from PIL import Image
import scipy.ndimage as nd

A,B,C = 641220.4, 11140.0, 55.0322
KT=215.5; U_RHUB=749.38
def fX(u): return A/(np.asarray(u,float)+B)-C
def fu(x): return A/(np.asarray(x,float)+C)-B
def mpp(u): return A/(np.asarray(u,float)+B)**2
def kv(u): return KT*mpp(U_RHUB)/mpp(u)
def vhub(u): return 604.0 - 0.0087*(np.asarray(u,float)-749.6)
def zref(u,v): return 0.3325 + (vhub(u)-v)/kv(u)

im=np.asarray(Image.open('ref_side.jpg').convert('RGB'),float)
lum=im.mean(2)
# high-pass along rows only (vertical detail), window 9 px kills nothing at p=4.6/9
hp = lum - nd.uniform_filter1d(lum, 9, axis=0)

def sheared_profile(u0,u1,r0,r1,theta):
    """mean profile along rows, shearing each column by theta (px row per px col)."""
    us=np.arange(u0,u1)
    acc=np.zeros(r1-r0)
    for u in us:
        sh = theta*(u-(u0+u1)/2.0)
        rows=np.arange(r0,r1)+sh
        acc += nd.map_coordinates(hp,[rows,np.full(len(rows),float(u))],order=1,mode='nearest')
    return acc/len(us)

def power(p, prof):
    n=len(prof); t=np.arange(n)
    c=(prof*np.cos(2*np.pi*t/p)).sum(); s=(prof*np.sin(2*np.pi*t/p)).sum()
    return np.hypot(c,s)*2/n, np.arctan2(-s,c)

U0,U1,R0,R1 = 775, 830, 439, 496
best=None
for theta in np.arange(-0.20,0.201,0.005):
    prof=sheared_profile(U0,U1,R0,R1,theta)
    for p in np.arange(3.6,12.0,0.02):
        a,ph=power(p,prof)
        if best is None or a>best[0]: best=(a,p,theta,ph)
print("REF best: amp %.3f  pitch %.3f px  rake %.4f px/px (%.2f deg)  phase %.3f"%(
    best[0],best[1],best[2],np.degrees(np.arctan(best[2])),best[3]))
# top-5 pitches at best theta
prof=sheared_profile(U0,U1,R0,R1,best[2])
res=[(power(p,prof)[0],p) for p in np.arange(3.6,12.0,0.02)]
res.sort(reverse=True)
print("  pitch peaks:", [("%.2f px amp %.3f"%(p,a)) for a,p in res[:1]])
# local maxima list
arr=np.array([a for a,p in [(power(p,prof)[0],p) for p in np.arange(3.6,12.0,0.02)]])
ps=np.arange(3.6,12.0,0.02)
for i in range(1,len(arr)-1):
    if arr[i]>arr[i-1] and arr[i]>arr[i+1] and arr[i]>0.3*arr.max():
        print("     local peak pitch %.2f px amp %.3f  -> %.2f mm at kv %.1f"%(ps[i],arr[i],1000*ps[i]/kv(802),kv(802)))
print()
print("profile at best rake (rows %d-%d):"%(R0,R1))
for i,v in enumerate(prof):
    print("   row %d %+7.2f %s"%(R0+i,v,("-"*int(-v*3) if v<0 else " "*0)))
