import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
from scipy import ndimage
im,a=load('/home/claude/tacombi/ref_side.jpg')
L=lum(a)
sub=L[430:505,750:850]
prof=sub.mean(1)
base=ndimage.uniform_filter1d(prof,11)
d=prof-base
print("row-mean deviation (dark=negative) y:val")
for i,y in enumerate(range(430,505)):
    print(f" {y}: {d[i]:+.4f} {'#'*max(0,int(-d[i]*600))}")
