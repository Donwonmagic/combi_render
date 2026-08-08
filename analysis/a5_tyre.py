import numpy as np, sys, math
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
P='/home/claude/tacombi/ref_side.jpg'
im,a=load(P); H,W,_=a.shape
L=lum(a)
hx,hy=749.60,603.98

def bilin(x,y):
    x0=np.floor(x).astype(int); y0=np.floor(y).astype(int)
    fx=x-x0; fy=y-y0
    x0=np.clip(x0,0,W-2); y0=np.clip(y0,0,H-2)
    return (L[y0,x0]*(1-fx)*(1-fy)+L[y0,x0+1]*fx*(1-fy)+L[y0+1,x0]*(1-fx)*fy+L[y0+1,x0+1]*fx*fy)

print("=== vertical profile at x=749.6 (rear wheel) ===")
for y in np.arange(520,690,2.0):
    print(f"y={y:6.1f} L={bilin(np.array([hx]),np.array([y]))[0]:.3f}")
