import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
def satprof(f,box,ang,x0,x1,tag,Z=10,thr=None):
    im=Image.open(f).convert("RGB").crop(box)
    a=np.asarray(im,np.float32); mx=a.max(2); mn=a.min(2); sat=(mx-mn)/np.maximum(mx,1)
    g=Image.fromarray(np.clip(sat*255,0,255).astype(np.uint8)).resize((im.width*Z,im.height*Z),Image.LANCZOS)
    g=g.rotate(-ang,expand=True,resample=Image.BICUBIC)
    A=np.asarray(g,np.float32)/255.
    col=A[:,int(x0*Z):int(x1*Z)].mean(1)
    print("=== %s  window native x %.0f-%.0f  (derotated frame, %dx)"%(tag,x0,x1,Z))
    nz=np.nonzero(col>0.02)[0]
    lo,hi=nz.min(),nz.max()
    for i in range(lo,hi+1,Z//2):
        v=col[i]
        print("  y=%6.2f  sat %.3f  %s"%(i/Z,v,"#"*int(v*70)))
satprof("ref_side.jpg",(728,300,845,392),19.7,52,94,"side RED 100%/idad")
