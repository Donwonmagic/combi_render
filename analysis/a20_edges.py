import numpy as np, sys
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
from scipy import ndimage
im,a=load('/home/claude/tacombi/ref_side.jpg'); H,W,_=a.shape
L=lum(a); h,s,v=hsv(a)
gx=np.abs(ndimage.sobel(ndimage.gaussian_filter(L,0.8),axis=1))
score=np.zeros(W)
for x in range(280,900):
    yc=358-0.0385*(x-500)
    y0=int(yc-25); y1=int(yc+25)
    score[x]=gx[y0:y1,x].mean()
# peaks
from scipy.signal import find_peaks
pk,_=find_peaks(score,height=np.percentile(score[280:900],70),distance=5)
print("vertical-edge peaks (x, strength):")
print(" ".join(f"{p}:{score[p]:.3f}" for p in pk if 280<=p<900))
print()
print("profile:")
for x in range(285,900,3):
    print(f" {x} {'*'*int(score[x]*200)}")
