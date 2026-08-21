import numpy as np
from PIL import Image
import scipy.ndimage as nd
A,B,C = 641220.4, 11140.0, 55.0322
KT=215.5; U_RHUB=749.38
def mpp(u): return A/(np.asarray(u,float)+B)**2
def kv(u): return KT*mpp(U_RHUB)/mpp(u)
im=np.asarray(Image.open('ref_side.jpg').convert('RGB'),float); lum=im.mean(2)
hp = lum - nd.uniform_filter1d(lum,9,axis=0)

def sheared(u0,u1,r0,r1,theta,step=0.25):
    us=np.arange(u0,u1); rows=np.arange(r0,r1,step)
    acc=np.zeros(len(rows))
    for u in us:
        sh=theta*(u-(u0+u1)/2.0)
        acc+=nd.map_coordinates(hp,[rows+sh,np.full(len(rows),float(u))],order=1,mode='nearest')
    return rows, acc/len(us)

def scan(u0,u1,r0,r1,label):
    best=None
    for theta in np.arange(-0.15,0.1501,0.0025):
        rows,prof=sheared(u0,u1,r0,r1,theta)
        n=len(prof); t=np.arange(n)*0.25
        for p in np.arange(3.5,13.0,0.02):
            c=(prof*np.cos(2*np.pi*t/p)).sum(); s=(prof*np.sin(2*np.pi*t/p)).sum()
            a=np.hypot(c,s)*2/n
            if best is None or a>best[0]: best=(a,p,theta)
    a,p,th=best
    print("%-14s rows %d-%d cols %d-%d : pitch %.2f px = %.1f mm  rake %.4f (%.2f deg) amp %.2f"
          %(label,r0,r1,u0,u1,p,1000*p/kv((u0+u1)/2),th,np.degrees(np.arctan(th)),a))
    return best

scan(775,830,442,470,"UPPER")
scan(775,830,468,494,"LOWER")
scan(775,830,442,494,"WHOLE")
scan(790,815,442,494,"WHOLE-narrow")
# control: blank painted panel below the block, same size window
scan(775,830,500,552,"CONTROL below")
scan(700,755,442,494,"CONTROL fwd")
