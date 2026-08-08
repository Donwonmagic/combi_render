import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
from scipy import ndimage
im,a=load('/home/claude/tacombi/ref_side.jpg'); H,W,_=a.shape
h,s,v=hsv(a); L=lum(a)
# classes
red  = ((h<28)|(h>335)) & (s>0.42) & (v>0.15)
yellow=(h>=28)&(h<70)&(s>0.45)&(v>0.35)
cream=(v>0.60)&(s<0.35)
print("=== belt line (lowest cream / highest red) per column ===")
for x in range(280,960,20):
    col_c=np.nonzero(cream[250:520,x])[0]+250
    col_r=np.nonzero(red[250:560,x])[0]+250
    cb = col_c.max() if len(col_c) else -1
    rt = col_r.min() if len(col_r) else -1
    print(f"x={x:4d} cream_bottom={cb} red_top={rt}")
