import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
from scipy import ndimage
im,a=load('/home/claude/tacombi/ref_side.jpg'); H,W,_=a.shape
h,s,v=hsv(a); L=lum(a)
# opening = not cream (cream = v>0.68 & s<0.30)
cream=(v>0.66)&(s<0.32)
for y in [330,345,360,375,390]:
    row=cream[y,250:1000]
    runs=[];cur=row[0];st=0
    for i in range(1,len(row)):
        if row[i]!=cur:
            if i-st>=4: runs.append(('C' if cur else 'o',250+st,250+i-1))
            cur=row[i];st=i
    runs.append(('C' if cur else 'o',250+st,250+len(row)-1))
    print(f"y={y}: "+" ".join(f"{t}{s0}-{s1}" for t,s0,s1 in runs))
