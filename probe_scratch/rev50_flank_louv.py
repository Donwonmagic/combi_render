import numpy as np
from PIL import Image
A,B,C = 641220.4, 11140.0, 55.0322
KT=215.5; U_RHUB=749.38
def fX(u): return A/(np.asarray(u,float)+B)-C
def fu(x): return A/(np.asarray(x,float)+C)-B
def mpp(u): return A/(np.asarray(u,float)+B)**2
def kv(u): return KT*mpp(U_RHUB)/mpp(u)

im=np.asarray(Image.open('ref_side.jpg').convert('RGB'),float)
lum=im.mean(2)
# vertical profile over the block columns; slots are DARK lines on red
for c0,c1 in [(775,825),(770,830),(785,815)]:
    p=lum[425:505,c0:c1].mean(1)
    print("cols %d-%d"%(c0,c1))
    for i,v in enumerate(p):
        r=425+i
        print("   row %d  %6.2f %s"%(r,v,"#"*int(max(0,v-40)/2)))
    break
