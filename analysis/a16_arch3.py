import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
from scipy import ndimage
im,a=load('/home/claude/tacombi/ref_side.jpg'); H,W,_=a.shape
h,s,v=hsv(a); L=lum(a)
paint = (((h<32)|(h>330))&(s>0.40)&(v>0.20)) | ((h>=32)&(h<62)&(s>0.45)&(v>0.35))
paint = ndimage.binary_closing(paint, np.ones((3,3)))
def lip(x, y0, y1):
    run=0
    for y in range(y0,y1):
        if not paint[y,x]:
            run+=1
            if run>=6: return y-run+1
        else: run=0
    return None
print("=== REAR ARCH lip (first sustained non-livery scanning down from y=470) ===")
r=[]
for x in range(600,940,5):
    y=lip(x,470,665)
    r.append((x,y)); print(f" x={x} lip={y}")
print()
print("=== FRONT ARCH lip (scan from y=470) ===")
for x in range(120,345,5):
    print(f" x={x} lip={lip(x,470,665)}")
