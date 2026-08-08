import numpy as np, sys, math
sys.path.insert(0,'/home/claude/tacombi/analysis')
from util import *
from scipy import ndimage, optimize
im,a=load('/home/claude/tacombi/ref_side.jpg'); H,W,_=a.shape
L=lum(a); h,s,v=hsv(a)

# Local contrast normalise the front wheel region
sub=L[540:690,170:320].copy()
lo=ndimage.uniform_filter(sub,25)
nrm=(sub-lo)
nrm=(nrm-nrm.min())/(nrm.max()-nrm.min())
from PIL import Image as I
I.fromarray((np.clip(nrm,0,1)*255).astype(np.uint8)).resize((150*8,150*8),I.LANCZOS).save('front_norm.png')

# cream arcs: relative brightness
cream = (nrm>0.62)
lab,n=ndimage.label(cream)
sz=ndimage.sum(cream,lab,range(1,n+1))
keep=[i+1 for i in range(n) if sz[i]>=25]
print("components kept",[(k,int(sz[k-1])) for k in keep])
pts=[]
for k in keep:
    yy,xx=np.nonzero(lab==k)
    print(f"  comp{k} bbox x[{xx.min()+170}-{xx.max()+170}] y[{yy.min()+540}-{yy.max()+540}] n={len(xx)}")
