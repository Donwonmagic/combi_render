import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
im,a=load('/home/claude/tacombi/ref_side.jpg'); H,W,_=a.shape
h,s,v=hsv(a); L=lum(a)
def cls(x,y):
    hh,ss,vv=h[y,x],s[y,x],v[y,x]
    if vv<0.18: return 'K'      # black
    if ss<0.28 and vv>0.62: return 'C'  # cream/white
    if ss<0.30: return 'g'      # grey
    if (hh<26 or hh>335) and ss>0.45: return 'R'
    if 26<=hh<50 and ss>0.45: return 'Y'
    if 50<=hh<200: return 'G'
    return '.'
for x in [300,360,420,500,560,620,680,760,820,860,900,930]:
    s2=''.join(cls(x,y) for y in range(250,700))
    # compress runs
    out=[];cur=s2[0];st=0
    for i in range(1,len(s2)):
        if s2[i]!=cur:
            if i-st>=3: out.append(f"{cur}{250+st}-{250+i-1}")
            cur=s2[i];st=i
    if len(s2)-st>=3: out.append(f"{cur}{250+st}-{250+len(s2)-1}")
    print(f"x={x}: "+" ".join(out))
