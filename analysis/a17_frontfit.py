import numpy as np, sys, math
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
from scipy import ndimage, optimize
im,a=load('/home/claude/tacombi/ref_side.jpg'); H,W,_=a.shape
L=lum(a)
lo=ndimage.uniform_filter(L,31); n=(L-lo)

# extract outer edge of the bright rim arcs: for each row, find the leftmost/rightmost strong-positive run
ptsL=[];ptsR=[]
for y in range(580,656):
    rowL=n[y,185:245]; rowR=n[y,245:305]
    iL=np.nonzero(rowL>0.055)[0]
    iR=np.nonzero(rowR>0.055)[0]
    if len(iL)>2:
        x0=185+iL.min()
        # subpixel: linear interp of n across threshold
        if x0>0:
            v1,v2=n[y,x0-1],n[y,x0]
            if v2!=v1: x0=x0-1+(0.055-v1)/(v2-v1)
        ptsL.append((x0,y))
    if len(iR)>2:
        x1=245+iR.max()
        if x1<W-1:
            v1,v2=n[y,x1],n[y,x1+1]
            if v1!=v2: x1=x1+(v1-0.055)/(v1-v2)
        ptsR.append((x1,y))
P=np.array(ptsL+ptsR,float)
print("nL",len(ptsL),"nR",len(ptsR))
print("L pts:", " ".join(f"({x:.1f},{y})" for x,y in ptsL[::4]))
print("R pts:", " ".join(f"({x:.1f},{y})" for x,y in ptsR[::4]))

def resid(p):
    cx,cy,r=p
    return np.hypot(P[:,0]-cx,P[:,1]-cy)-r
sol=optimize.least_squares(resid,[242,610,45],loss='soft_l1',f_scale=1.5)
print("free fit centre/R:",sol.x, "rms",np.sqrt((resid(sol.x)**2).mean()))

# fixed radius variants
for R in [44.0,46.2,48.0]:
    def r2(p):
        cx,cy=p
        return np.hypot(P[:,0]-cx,P[:,1]-cy)-R
    s2=optimize.least_squares(r2,[242,610],loss='soft_l1',f_scale=1.5)
    print(f"  R fixed {R}: centre {s2.x}, rms {np.sqrt((r2(s2.x)**2).mean()):.2f}")

print()
print("=== constrained tests: fix cy, fit cx and R ===")
for cyf in [600,604,608,612,616,620,624,628]:
    def r3(p):
        cx,R=p
        return np.hypot(P[:,0]-cx,P[:,1]-cyf)-R
    s3=optimize.least_squares(r3,[242,45])
    print(f" cy={cyf}: cx={s3.x[0]:.2f} R={s3.x[1]:.2f} rms={np.sqrt((r3(s3.x)**2).mean()):.3f}")
print()
print("=== same, R fixed to rear value 46.16 ===")
for cyf in [600,604,608,612,616,620,624,628]:
    def r4(p):
        cx=p[0]
        return np.hypot(P[:,0]-cx,P[:,1]-cyf)-46.16
    s4=optimize.least_squares(r4,[242.])
    print(f" cy={cyf}: cx={s4.x[0]:.2f} rms={np.sqrt((r4(s4.x)**2).mean()):.3f}")
