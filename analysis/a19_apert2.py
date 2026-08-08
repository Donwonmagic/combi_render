import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
from scipy import ndimage
im,a=load('/home/claude/tacombi/ref_side.jpg'); H,W,_=a.shape
h,s,v=hsv(a); L=lum(a)
cream=(v>0.66)&(s<0.32)
# use a band that follows the body slope: at x, band centre = 358 - 0.0385*(x-500)
cnt=np.zeros(W)
for x in range(250,1000):
    yc=358-0.0385*(x-500)
    y0=int(yc-32); y1=int(yc+32)
    cnt[x]=(~cream[y0:y1,x]).sum()
print("non-cream count in window band per column:")
for x in range(250,1000,5):
    bar='#'*int(cnt[x])
    print(f" {x:4d} {int(cnt[x]):3d} {bar}")
