import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
from scipy import ndimage
im,a=load('/home/claude/tacombi/ref_side.jpg'); H,W,_=a.shape
h,s,v=hsv(a); L=lum(a)
SLOPE=-0.0385; XR=749.6; GY=668.0; PX=211.21
def yref(x,y): return y - SLOPE*(x-XR)
def hgt(x,y): return (GY - yref(x,y))/PX
def mx(x): return (496.15-x)/PX

print("--- cream/red break line, refined per column ---")
vals=[]
for x in range(340,940,10):
    yc=440.4+SLOPE*(x-XR)
    col=None
    for y in range(int(yc)-9,int(yc)+10):
        cr=(v[y,x]>0.62 and s[y,x]<0.34); rd=((h[y,x]<28 or h[y,x]>335) and s[y,x]>0.42)
        if cr and ((h[y+1,x]<28 or h[y+1,x]>335) and s[y+1,x]>0.42):
            col=y+0.5; break
    if col: vals.append((x,yref(x,col)))
arr=np.array(vals)
print(f" n={len(arr)} mean yref={arr[:,1].mean():.2f} sd={arr[:,1].std():.2f}")
print(f" -> height above ground at rear-axle station = {(GY-arr[:,1].mean())/PX:.4f} m")

print()
print("--- counter gold nosing: front end search x 280..360 ---")
gold=((h>=25)&(h<62))&(s>0.28)&(v>0.42)
for x in range(280,370,4):
    yc=416.8+SLOPE*(x-XR)
    rows=[y for y in range(int(yc)-7,int(yc)+8) if gold[y,x]]
    print(f"  x={x} yc={yc:.0f} gold rows {rows}")
print()
print("--- counter gold nosing: rear end search x 950..1024 (row window) ---")
for x in range(940,1024,4):
    yc=416.8+SLOPE*(x-XR)
    rows=[y for y in range(int(yc)-9,int(yc)+10) if gold[y,x]]
    print(f"  x={x} yc={yc:.0f} gold rows {rows}")
