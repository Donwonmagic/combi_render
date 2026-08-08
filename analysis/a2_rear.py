import numpy as np
from PIL import Image
from scipy import ndimage

im = Image.open('/home/claude/tacombi/ref_side.jpg').convert('RGB')
a = np.asarray(im).astype(np.float32)/255.0
H,W,_ = a.shape
mx=a.max(2); mn=a.min(2); v=mx
s=np.where(mx>0,(mx-mn)/np.maximum(mx,1e-6),0)
r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
d=mx-mn; h=np.zeros_like(mx); m=(d>1e-6)
i=m&(mx==r); h[i]=((g-b)[i]/d[i])%6
i=m&(mx==g); h[i]=((b-r)[i]/d[i])+2
i=m&(mx==b); h[i]=((r-g)[i]/d[i])+4
h*=60.0
red=((h<18)|(h>350))&(s>0.55)&(v>0.28)
lab,n=ndimage.label(red)
# component containing (750,604)
cid = lab[604,750]
mask = (lab==cid)
ys,xs=np.nonzero(mask)
print("hubcap bbox", xs.min(),xs.max(),ys.min(),ys.max())
cy,cx = ndimage.center_of_mass(mask)
print("centroid", cx, cy)

# refine centre: for the binary disc, best-fit circle centre = centre minimising variance of boundary radius
# Use edge points of the mask
er = mask ^ ndimage.binary_erosion(mask)
ey,ex = np.nonzero(er)
def fit_circle(x,y):
    A=np.c_[2*x,2*y,np.ones(len(x))]
    bb=x**2+y**2
    sol,*_=np.linalg.lstsq(A,bb,rcond=None)
    xc,yc,c=sol
    R=np.sqrt(c+xc**2+yc**2)
    return xc,yc,R
xc,yc,R = fit_circle(ex.astype(float),ey.astype(float))
print(f"hubcap circle fit: centre=({xc:.2f},{yc:.2f}) R={R:.2f}  D={2*R:.2f}")
resid = np.sqrt((ex-xc)**2+(ey-yc)**2)-R
print("edge radius resid std", resid.std())

# Now radial profile from that centre to find tyre outer edge.
# grayscale luminance
L = (0.299*a[:,:,0]+0.587*a[:,:,1]+0.114*a[:,:,2])
import math
def radial_profile(xc,yc,angles,rmax=90,step=0.25):
    rs=np.arange(0,rmax,step)
    out=[]
    for ang in angles:
        ca,sa=math.cos(math.radians(ang)),math.sin(math.radians(ang))
        px=xc+rs*ca; py=yc+rs*sa
        pxi=np.clip(px.astype(int),0,W-1); pyi=np.clip(py.astype(int),0,H-1)
        out.append(L[pyi,pxi])
    return rs, np.array(out)

# sample angles that avoid the ground (below) and avoid arch (above) -> use forward/back horizontal +-35deg
angs = list(range(-30,31,5)) + list(range(150,211,5))
rs,prof = radial_profile(xc,yc,angs,rmax=100)
mean=prof.mean(0)
for k in range(0,len(rs),4):
    print(f"r={rs[k]:5.1f} L={mean[k]:.3f}")
