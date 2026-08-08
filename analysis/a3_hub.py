import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
from scipy import ndimage
P='/home/claude/tacombi/ref_side.jpg'
im,a=load(P); H,W,_=a.shape
h,s,v=hsv(a)
red=((h<25)|(h>340))&(s>0.45)&(v>0.20)
lab,n=ndimage.label(red)
cid=None
best=0
for c in range(1,n+1):
    pass
# find comp overlapping the rear hub area
sub = lab[560:660, 700:800]
ids,cnts = np.unique(sub[sub>0], return_counts=True)
o=np.argsort(cnts)[::-1]
for k in o[:4]:
    print("id",ids[k],"count",cnts[k])
cid=ids[o[0]]
mask=(lab==cid)
mask=ndimage.binary_fill_holes(mask)
# restrict to the local region
box=np.zeros_like(mask); box[540:680,690:820]=True
mask=mask&box
ys,xs=np.nonzero(mask)
print("bbox x",xs.min(),xs.max(),"y",ys.min(),ys.max(),"w",xs.max()-xs.min()+1,"h",ys.max()-ys.min()+1)
cy,cx=ndimage.center_of_mass(mask); print("centroid",cx,cy, "area",mask.sum(), "equiv D", 2*np.sqrt(mask.sum()/np.pi))
er=mask^ndimage.binary_erosion(mask)
ey,ex=np.nonzero(er)
def fit_circle(x,y):
    A=np.c_[2*x,2*y,np.ones(len(x))]; bb=x**2+y**2
    sol,*_=np.linalg.lstsq(A,bb,rcond=None); xc,yc,c=sol
    return xc,yc,np.sqrt(c+xc**2+yc**2)
xc,yc,R=fit_circle(ex.astype(float),ey.astype(float))
print(f"REAR HUB circle: ({xc:.2f},{yc:.2f}) R={R:.2f} D={2*R:.2f}")
res=np.sqrt((ex-xc)**2+(ey-yc)**2)-R; print("resid std",res.std(),"n",len(ex))
