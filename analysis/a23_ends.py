import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
from scipy import ndimage
im,a=load('/home/claude/tacombi/ref_side.jpg'); H,W,_=a.shape
h,s,v=hsv(a); L=lum(a)
gold=((h>=28)&(h<58))&(s>0.30)&(v>0.45)
print("=== gold nosing line: per column the y of gold pixels near the expected line ===")
for x in list(range(280,340,5))+list(range(940,1024,4)):
    yc=416.8-0.0385*(749.6-x)
    ys=np.nonzero(gold[int(yc)-8:int(yc)+9,x])[0]
    print(f" x={x} expected y~{yc:.0f} gold rows: {(ys+int(yc)-8).tolist()}")
print()
print("=== red lower body: max x per row 440..600 ===")
red=((h<28)|(h>335))&(s>0.42)&(v>0.18)
red=ndimage.binary_opening(red,np.ones((3,3)))
for y in range(440,605,10):
    xs=np.nonzero(red[y,700:1024])[0]
    print(f" y={y} red_max_x={700+xs.max() if len(xs) else None}")
print()
print("=== cream body: max x per row 250..460 (excluding background wall) ===")
cream=(v>0.72)&(s<0.26)
for y in range(250,470,10):
    xs=np.nonzero(cream[y,820:1024])[0]
    # find the first big gap => body edge
    if len(xs)==0: print(f" y={y} none"); continue
    arr=820+xs
    brk=arr[0]
    for i in range(1,len(arr)):
        if arr[i]-arr[i-1]>3: brk=arr[i-1]; break
        brk=arr[i]
    print(f" y={y} cream run to x={brk}")
