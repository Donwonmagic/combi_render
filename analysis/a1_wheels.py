import numpy as np
from PIL import Image
import colorsys

im = Image.open('/home/claude/tacombi/ref_side.jpg').convert('RGB')
a = np.asarray(im).astype(np.float32)/255.0
H,W,_ = a.shape
print("side", W, H)

# HSV
mx = a.max(2); mn = a.min(2)
v = mx
s = np.where(mx>0,(mx-mn)/np.maximum(mx,1e-6),0)
r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
d = mx-mn
h = np.zeros_like(mx)
m = (d>1e-6)
idx = m & (mx==r); h[idx] = ((g-b)[idx]/d[idx])%6
idx = m & (mx==g); h[idx] = ((b-r)[idx]/d[idx])+2
idx = m & (mx==b); h[idx] = ((r-g)[idx]/d[idx])+4
h = h*60.0

# strongly saturated red mask
red = ((h<18)|(h>350)) & (s>0.55) & (v>0.28)
print("red px total", red.sum())

# look only in lower-right region where the rear hubcap is
ys,xs = np.nonzero(red)
# Print a coarse density map to find blobs in the lower half
from scipy import ndimage
lab,n = ndimage.label(red)
print("n components", n)
sizes = ndimage.sum(red, lab, range(1,n+1))
order = np.argsort(sizes)[::-1][:12]
for i in order:
    cid = i+1
    cy,cx = ndimage.center_of_mass(red, lab, cid)
    ys2,xs2 = np.nonzero(lab==cid)
    print(f"comp {cid}: size={sizes[i]:.0f} centroid=({cx:.1f},{cy:.1f}) bbox x[{xs2.min()}-{xs2.max()}] y[{ys2.min()}-{ys2.max()}] w={xs2.max()-xs2.min()+1} h={ys2.max()-ys2.min()+1}")
