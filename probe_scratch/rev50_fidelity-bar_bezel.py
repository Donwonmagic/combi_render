import numpy as np
from PIL import Image

def stats(im,y,x0,x1):
    row=im[y,x0:x1]
    lum=row.mean(axis=1); mx=row.max(axis=1); mn=row.min(axis=1)
    sat=(mx-mn)/np.maximum(mx,1)
    return lum,sat

def runs(mask):
    out=[];s=None
    for i,v in enumerate(mask):
        if v and s is None: s=i
        if (not v) and s is not None: out.append((s,i-1)); s=None
    if s is not None: out.append((s,len(mask)-1))
    return out

P=np.asarray(Image.open('ref_rear34.jpg').convert('RGB')).astype(float)
print("=== ref_rear34.jpg  tail lamp, horizontal scans; metal = sat<0.66 AND lum>70 ===")
for y in range(655,706,5):
    lum,sat=stats(P,y,910,985)
    m=(sat<0.66)&(lum>70)
    r=[(a+910,b+910,b-a+1) for (a,b) in runs(m)]
    print(" y=%d metal runs %s"%(y,r))
print("\n=== NEGATIVE CONTROL: plain red paint, same rows, x 1000..1075 (aft of the lamp, on the lid) ===")
for y in range(655,706,5):
    lum,sat=stats(P,y,1000,1075)
    m=(sat<0.66)&(lum>70)
    print(" y=%d metal runs %s"%(y,[(a+1000,b+1000,b-a+1) for (a,b) in runs(m)]))
print("\n=== POSITIVE CONTROL: the chrome plate frame, y 640..700, x 1070..1190 ===")
for y in (645,660,690):
    lum,sat=stats(P,y,1065,1195)
    m=(sat<0.66)&(lum>70)
    print(" y=%d metal runs %s"%(y,[(a+1065,b+1065,b-a+1) for (a,b) in runs(m)]))

# ---- RENDER: near tail lamp in r49s_rear.png ----
R=np.asarray(Image.open('out/r49s_rear.png').convert('RGB')).astype(float)
print("\n=== RENDER out/r49s_rear.png : locate the amber tail lamps ===")
r,g,b=R[...,0],R[...,1],R[...,2]
amb=(r>110)&(g>40)&(g<0.72*r)&(b<0.45*r)
ys,xs=np.nonzero(amb)
print("amber-ish px",amb.sum())
# cluster by x
if amb.sum():
    for xlo,xhi in ((0,800),(800,1600)):
        s=(xs>=xlo)&(xs<xhi)
        if s.sum()>50:
            print("  cluster x %d..%d  n=%d  bbox x %d..%d y %d..%d"
                  %(xlo,xhi,s.sum(),xs[s].min(),xs[s].max(),ys[s].min(),ys[s].max()))
