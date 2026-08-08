import numpy as np, sys, math
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
im,a=load('/home/claude/tacombi/ref_side.jpg'); H,W,_=a.shape
L=lum(a)
def bl(x,y):
    x0=np.clip(np.floor(x).astype(int),0,W-2); y0=np.clip(np.floor(y).astype(int),0,H-2)
    fx=x-x0; fy=y-y0
    return (L[y0,x0]*(1-fx)*(1-fy)+L[y0,x0+1]*fx*(1-fy)+L[y0+1,x0]*(1-fx)*fy+L[y0+1,x0+1]*fx*fy)
cx,cy=749.60,603.98
rs=np.arange(50,100,0.5)
print("radius profiles by angle (deg from +x, y down):")
for ang in range(-70,100,10):
    xs=cx+rs*math.cos(math.radians(ang)); ys=cy+rs*math.sin(math.radians(ang))
    p=bl(xs,ys)
    # find where gradient max
    g=np.gradient(p)
    k=int(np.argmax(g))
    print(f"ang={ang:4d} maxgrad at r={rs[k]:.1f} (g={g[k]:.3f})  ", " ".join(f"{p[i]:.2f}" for i in range(0,len(rs),4)))
