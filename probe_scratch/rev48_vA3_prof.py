import numpy as np
from PIL import Image
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None
def prof(f,box,ang,satT,typeT,tag,Z=8):
    im=Image.open(f).convert("RGB").crop(box)
    big=im.resize((im.width*Z,im.height*Z),Image.LANCZOS)
    a=np.asarray(big,np.float32); mx=a.max(2); mn=a.min(2)
    sat=(mx-mn)/np.maximum(mx,1); R,G,B=a[...,0],a[...,1],a[...,2]
    burst=(sat>satT)&(R>=G)&(R>=B)
    burst=nd.binary_closing(burst,np.ones((2*Z,2*Z)))
    lab,n=nd.label(burst); burst=lab==(int(np.argmax(nd.sum(burst,lab,range(1,n+1))))+1)
    fill=nd.binary_fill_holes(burst)
    typ=(sat<typeT)&(mx>140)
    rf=nd.rotate(fill.astype(float),ang,reshape=True,order=1)>0.5
    rt=nd.rotate(typ.astype(float),ang,reshape=True,order=1)>0.5
    m=rt&rf
    ys,xs=np.nonzero(rf)
    print("=== %s  derotated fill bbox x %d-%d y %d-%d (px at %dx)"%(tag,xs.min(),xs.max(),ys.min(),ys.max(),Z))
    return m,rf,Z
def report(m,rf,Z,x0f,x1f,tag):
    ys,xs=np.nonzero(rf); W=xs.max()-xs.min()+1
    x0=int(xs.min()+x0f*W); x1=int(xs.min()+x1f*W)
    sub=m[:,x0:x1]
    p=sub.sum(1); nz=np.nonzero(p)[0]
    thr=0.12*p.max()
    print(" window x %d-%d (%.2f-%.2f of burst width), rowmax %d"%(x0,x1,x0f,x1f,p.max()))
    seg,run=[],None
    for i in range(len(p)):
        if p[i]>thr and run is None: run=i
        if p[i]<=thr and run is not None:
            if i-run>Z: seg.append((run,i-1))
            run=None
    if run is not None: seg.append((run,len(p)-1))
    print(" bands (native px):", [( (s[1]-s[0]+1)/Z, s) for s in seg])
    for i in range(len(seg)-1):
        gap=(seg[i+1][0]-seg[i][1]-1)/Z; cap=(seg[i][1]-seg[i][0]+1)/Z
        print("   band%d cap %.2f px, gap to next %.2f px -> gap/cap %.3f"%(i,cap,gap,gap/cap))
m,rf,Z=prof("ref_side.jpg",(728,300,845,392),19.7,0.30,0.22,"side RED")
for w in [(0.35,0.75),(0.40,0.90),(0.45,0.80)]: report(m,rf,Z,w[0],w[1],"side")
m,rf,Z=prof("IMG_2073.jpeg",(1108,360,1210,445),19.7,0.30,0.22,"2073 GREEN")
for w in [(0.20,0.85),(0.30,0.80)]: report(m,rf,Z,w[0],w[1],"2073")

def dump(f,box,ang,tag,x0f,x1f):
    m,rf,Z=prof(f,box,ang,0.30,0.22,tag)
    ys,xs=np.nonzero(rf); W=xs.max()-xs.min()+1
    x0=int(xs.min()+x0f*W); x1=int(xs.min()+x1f*W)
    p=m[:,x0:x1].sum(1)
    nz=np.nonzero(p)[0]
    print(" profile %s (row: count) native-row = /8"%tag)
    for i in range(nz.min(),nz.max()+1,4):
        print("   %6.2f  %4d  %s"%(i/8.0,p[i],"#"*(p[i]//4)))
dump("ref_side.jpg",(728,300,845,392),19.7,"side RED",0.40,0.85)
