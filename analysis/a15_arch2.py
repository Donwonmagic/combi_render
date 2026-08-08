import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
from scipy import ndimage
im,a=load('/home/claude/tacombi/ref_side.jpg'); H,W,_=a.shape
h,s,v=hsv(a); L=lum(a)
paint = (((h<32)|(h>330))&(s>0.40)&(v>0.20)) | ((h>=32)&(h<62)&(s>0.45)&(v>0.35))  # red or yellow livery
paint = ndimage.binary_closing(paint, np.ones((3,3)))
print("=== REAR ARCH lip: lowest livery pixel per column ===")
for x in range(590,940,10):
    idx=np.nonzero(paint[430:640,x])[0]
    print(f" x={x} lowest_paint={430+idx.max() if len(idx) else None}")
print()
print("=== FRONT ARCH lip ===")
for x in range(130,340,10):
    idx=np.nonzero(paint[430:660,x])[0]
    print(f" x={x} lowest_paint={430+idx.max() if len(idx) else None}")
