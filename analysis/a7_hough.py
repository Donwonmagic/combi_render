import numpy as np, sys, math
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
from scipy import ndimage
im,a=load('/home/claude/tacombi/ref_side.jpg'); H,W,_=a.shape
L=lum(a)
def bl(x,y):
    x0=np.clip(np.floor(x).astype(int),0,W-2); y0=np.clip(np.floor(y).astype(int),0,H-2)
    fx=x-x0; fy=y-y0
    return (L[y0,x0]*(1-fx)*(1-fy)+L[y0,x0+1]*fx*(1-fy)+L[y0+1,x0]*(1-fx)*fy+L[y0+1,x0+1]*fx*fy)

RS=np.arange(20,52,0.5)
ANG=np.concatenate([np.arange(-38,39,2.0), np.arange(142,219,2.0)])
def prof(cx,cy):
    out=np.zeros(len(RS))
    for i,r in enumerate(RS):
        xs=cx+r*np.cos(np.radians(ANG)); ys=cy+r*np.sin(np.radians(ANG))
        out[i]=np.median(bl(xs,ys))
    return out
tmpl=prof(749.60,603.98)
tmpl_n=(tmpl-tmpl.mean())/tmpl.std()
print("template (r,L):", " ".join(f"{r:.0f}:{t:.2f}" for r,t in zip(RS,tmpl) if r%2==0))

best=None
for cx in np.arange(228,262,0.5):
    for cy in np.arange(592,618,0.5):
        p=prof(cx,cy)
        if p.std()<1e-4: continue
        pn=(p-p.mean())/p.std()
        sc=float((tmpl_n*pn).mean())
        if best is None or sc>best[0]: best=(sc,cx,cy)
print("BEST front centre (NCC):",best)
sc,fx,fy=best
p=prof(fx,fy)
print("front profile:"," ".join(f"{r:.0f}:{t:.2f}" for r,t in zip(RS,p) if r%2==0))

# scan score map along cx at best cy
print("score vs cx at cy=%.1f"%fy)
for cx in np.arange(232,258,1.0):
    p=prof(cx,fy); pn=(p-p.mean())/p.std()
    print(f"  cx={cx:.1f} ncc={(tmpl_n*pn).mean():.4f}")
print("score vs cy at cx=%.1f"%fx)
for cy in np.arange(594,616,1.0):
    p=prof(fx,cy); pn=(p-p.mean())/p.std()
    print(f"  cy={cy:.1f} ncc={(tmpl_n*pn).mean():.4f}")
