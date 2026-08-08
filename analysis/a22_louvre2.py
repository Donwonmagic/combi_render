import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
from scipy import ndimage
im,a=load('/home/claude/tacombi/ref_side.jpg')
L=lum(a)
# rows: high-pass along y only, average over x band avoiding graphics
for xr in [(770,800),(800,840),(775,845)]:
    sub=L[440:505,xr[0]:xr[1]]
    prof=sub.mean(1)
    hp=prof-ndimage.uniform_filter1d(prof,7)
    print(f"--- x {xr} ---")
    for i,y in enumerate(range(440,505)):
        print(f" {y}: {hp[i]:+.4f} {'#'*max(0,int(-hp[i]*1500))}")
    print()
# horizontal extent: for the strongest louvre rows, find where the modulation dies out
sub2=L[452:495,:]
hp2=sub2-ndimage.uniform_filter(sub2,(7,1))
energy=(hp2**2).mean(0)
print("louvre modulation energy per column x=730..880:")
for x in range(730,885,3):
    print(f" {x} {'*'*int(energy[x]*40000)}")
