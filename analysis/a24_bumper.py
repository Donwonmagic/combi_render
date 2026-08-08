import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
im,a=load('/home/claude/tacombi/ref_side.jpg')
h,s,v=hsv(a); L=lum(a)
print("rows across the front bumper region: x=40..120, showing R,G,B and hue")
for y in [575,585,595,605,615,625,635]:
    print(f"--- y={y}")
    out=[]
    for x in range(40,125,3):
        r,g,b=a[y,x]
        out.append(f"{x}:[{r:.2f},{g:.2f},{b:.2f}]h{h[y,x]:.0f}")
    print("  "+"  ".join(out))
