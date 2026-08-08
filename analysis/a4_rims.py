import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
from scipy import ndimage
P='/home/claude/tacombi/ref_side.jpg'
im,a=load(P); H,W,_=a.shape
h,s,v=hsv(a); L=lum(a)

def fit_circle(x,y,w=None):
    A=np.c_[2*x,2*y,np.ones(len(x))]; bb=x**2+y**2
    if w is not None:
        A=A*w[:,None]; bb=bb*w
    sol,*_=np.linalg.lstsq(A,bb,rcond=None); xc,yc,c=sol
    return xc,yc,np.sqrt(max(c+xc**2+yc**2,0))

# ---------- REAR cream ring ----------
reg=np.zeros((H,W),bool); reg[545:670,690:815]=True
# cream = warm, moderate sat, brighter than tyre
cream = reg & (L>0.30) & (s<0.45) & (h>15) & (h<70)
lab,n=ndimage.label(cream)
sz=ndimage.sum(cream,lab,range(1,n+1)); big=np.argmax(sz)+1
ring=(lab==big)
print("rear ring px",ring.sum())
ys,xs=np.nonzero(ring)
print("rear ring bbox x",xs.min(),xs.max(),"y",ys.min(),ys.max())
# outer boundary: for each angle from known hub centre take max radius of ring
hx,hy=749.60,603.98
ang=np.degrees(np.arctan2(ys-hy,xs-hx))%360
rad=np.hypot(xs-hx,ys-hy)
import collections
bins=np.arange(0,360,5)
outer=[];inner=[]
for b in bins:
    m=(ang>=b)&(ang<b+5)
    if m.sum()>3:
        outer.append((b+2.5,np.percentile(rad[m],99)))
        inner.append((b+2.5,np.percentile(rad[m],1)))
oa=np.array(outer); ia=np.array(inner)
print("REAR ring outer radius by angle (deg,r):")
print(" ".join(f"{d:.0f}:{r:.1f}" for d,r in oa))
print("median outer r", np.median(oa[:,1]), "-> D",2*np.median(oa[:,1]))
print("median inner r", np.median(ia[:,1]), "-> D",2*np.median(ia[:,1]))

# ---------- FRONT cream ring ----------
reg2=np.zeros((H,W),bool); reg2[555:670,180:305]=True
cream2 = reg2 & (L>0.22) & (s<0.5) & (h>10) & (h<80)
lab2,n2=ndimage.label(cream2)
sz2=ndimage.sum(cream2,lab2,range(1,n2+1))
order=np.argsort(sz2)[::-1][:6]
pts=[]
for k in order:
    cid=k+1
    if sz2[k]<40: continue
    yy,xx=np.nonzero(lab2==cid)
    print(f"front cream comp {cid} size={sz2[k]:.0f} bbox x[{xx.min()}-{xx.max()}] y[{yy.min()}-{yy.max()}]")
    pts.append((xx,yy))
