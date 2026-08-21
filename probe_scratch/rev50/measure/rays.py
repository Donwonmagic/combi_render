import numpy as np
from PIL import Image

def load(path):
    return np.asarray(Image.open(path).convert('RGB')).astype(np.float64)

def bilin(img, x, y):
    h,w = img.shape[:2]
    x=np.clip(x,0,w-1.001); y=np.clip(y,0,h-1.001)
    x0=np.floor(x).astype(int); y0=np.floor(y).astype(int)
    fx=(x-x0)[...,None]; fy=(y-y0)[...,None]
    if img.ndim==2: fx=fx[...,0]; fy=fy[...,0]
    a=img[y0,x0]; b=img[y0,x0+1]; c=img[y0+1,x0]; d=img[y0+1,x0+1]
    return (a*(1-fx)+b*fx)*(1-fy) + (c*(1-fx)+d*fx)*fy

def ray_profile(chan, cx, cy, ang, rmax, step=0.25):
    r = np.arange(0, rmax, step)
    return r, bilin(chan, cx+r*np.cos(ang), cy+r*np.sin(ang))

def subpix_cross(r, v, level, r_lo, r_hi, rising):
    """last/first crossing of `level` within [r_lo,r_hi]; returns radius or None"""
    m = (r>=r_lo)&(r<=r_hi)
    rr=r[m]; vv=v[m]
    if rr.size<3: return None
    s = np.sign(vv-level)
    idx = np.where(np.diff(s)!=0)[0]
    if idx.size==0: return None
    # pick crossing with correct direction, outermost for falling-outward edges
    good=[i for i in idx if (vv[i+1]>vv[i])==rising]
    if not good: return None
    i = good[-1] if not rising else good[0]
    v0,v1=vv[i],vv[i+1]
    t=(level-v0)/(v1-v0+1e-12)
    return rr[i]+t*(rr[i+1]-rr[i])
