import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
im,a=load('/home/claude/tacombi/ref_side.jpg'); H,W,_=a.shape
h,s,v=hsv(a); L=lum(a)

def subpix_edge(x, y0, y1, rising=True, thresh=None):
    col=L[y0:y1+1,x].astype(float)
    if thresh is None: thresh=(col.min()+col.max())/2
    for i in range(len(col)-1):
        if rising and col[i]<thresh<=col[i+1]:
            return y0+i+(thresh-col[i])/(col[i+1]-col[i])
        if (not rising) and col[i]>thresh>=col[i+1]:
            return y0+i+(col[i]-thresh)/(col[i]-col[i+1])
    return None

print("=== ROOF TOP EDGE (bright roof vs beige wall), x 770..890 ===")
for x in range(770,895,10):
    col=L[230:300,x]
    g=np.gradient(col)
    k=int(np.argmax(g))
    print(f" x={x} roof_top~{230+k} (grad {g[k]:.3f})  vals@240,245,250,255,260,265,270: "+" ".join(f"{L[y,x]:.2f}" for y in [240,245,250,255,260,265,270]))
print()
print("=== ROOF TOP EDGE front section x 150..330 ===")
for x in range(150,340,10):
    col=L[250:360,x]; g=np.gradient(col); k=int(np.argmax(g))
    print(f" x={x} maxgrad@{250+k} g={g[k]:.3f}")
