import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
im,a=load('/home/claude/tacombi/ref_side.jpg'); H,W,_=a.shape
h,s,v=hsv(a); L=lum(a)
body = (v>0.16)  # not deep shadow
print("=== REAR ARCH: lowest non-shadow (body) pixel per column, x 600..930 ===")
for x in range(600,935,10):
    col=np.nonzero(L[430:640,x]>0.155)[0]+430
    # find first long dark run from below
    prof=L[430:660,x]
    # walk up from y=655 to find where it becomes bright (arch lip)
    y=655; 
    while y>430 and prof[y-430]<0.155: y-=1
    print(f" x={x} arch_lip_y={y}  L@{y}={prof[y-430]:.3f}")
print()
print("=== FRONT ARCH: x 140..330 ===")
for x in range(140,335,10):
    prof=L[430:670,x]
    y=660
    while y>430 and prof[y-430]<0.155: y-=1
    print(f" x={x} arch_lip_y={y} L={prof[y-430]:.3f}")
