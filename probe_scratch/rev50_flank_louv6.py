"""Row-COHERENCE detector: horizontal periodic lines vs isotropic paint texture.
For each column u, correlate its vertically-high-passed profile with the mean of
its neighbours' (sheared by the fitted rake).  Blank paint -> ~0; ruled lines -> high.
KILL CONTROL: the same statistic on bands of blank paint above and below."""
import numpy as np
from PIL import Image
import scipy.ndimage as nd
A,B,C = 641220.4, 11140.0, 55.0322
def fX(u): return A/(np.asarray(u,float)+B)-C
im=np.asarray(Image.open('ref_side.jpg').convert('RGB'),float); lum=im.mean(2)
hp = lum - nd.uniform_filter1d(lum,9,axis=0)
TH=-0.030   # rake fitted earlier
def coh(r0,r1,W=7):
    out=[]
    for u in range(690,910):
        rows=np.arange(r0,r1,0.5)
        me=nd.map_coordinates(hp,[rows,np.full(len(rows),float(u))],order=1,mode='nearest')
        nb=[]
        for d in list(range(-W,0))+list(range(1,W+1)):
            nb.append(nd.map_coordinates(hp,[rows+TH*d,np.full(len(rows),float(u+d))],order=1,mode='nearest'))
        nb=np.mean(nb,0)
        me-=me.mean(); nb-=nb.mean()
        den=np.sqrt((me*me).sum()*(nb*nb).sum())
        out.append(float((me*nb).sum()/den) if den>0 else 0.0)
    return np.array(out)
blk=coh(443,492); bel=coh(500,549); abv=coh(560,609)
us=np.arange(690,910)
print(" col      x(m)    BLOCK   below   lower   bar")
for i,u in enumerate(us):
    if u%2: continue
    print("%4d  %+8.4f  %6.3f  %6.3f  %6.3f  %s"%(u,fX(u),blk[i],bel[i],abv[i],"#"*int(max(0,blk[i])*50)))
print("\nmedians: block %.3f  ctrl-below %.3f  ctrl-lower %.3f"%(np.median(blk[40:150]),np.median(bel),np.median(abv)))
