"""Photo gap/cap as a function of the assumed reading angle, and an independent
reading-angle estimate from the words' own axes."""
import numpy as np
from PIL import Image
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None
def type_mask(img,Z):
    big=img.resize((img.width*Z,img.height*Z),Image.LANCZOS)
    a=np.asarray(big.convert("RGB"),np.float32)
    R,G,B=a[...,0],a[...,1],a[...,2]
    mx=a.max(2);sat=(mx-a.min(2))/np.maximum(mx,1)
    red=(R>90)&(R-G>40)&(R-B>25)
    burst=nd.binary_fill_holes(nd.binary_closing(red,np.ones((9,9))))
    lab,n=nd.label(burst)
    if n>1: burst=lab==(int(np.argmax(nd.sum(burst,lab,range(1,n+1))))+1)
    ty=nd.binary_opening(burst&(mx>150)&(sat<0.30),np.ones((5,5)))
    return ty,burst
def segs_at(ty,Z,ang):
    rot=nd.rotate(ty.astype(float),ang,reshape=True,order=1)>0.5
    prof=rot.sum(1);nz=np.nonzero(prof)[0]
    if len(nz)==0: return []
    seg,run=[],None
    for i in range(nz.min(),nz.max()+2):
        p=prof[i] if i<len(prof) else 0
        if p>0 and run is None: run=i
        if p==0 and run is not None: seg.append((run,i-1));run=None
    return [s for s in seg if (s[1]-s[0]+1)>Z*1.5]
im=Image.open("IMG_2073.jpeg").convert("RGB").crop((1108,360,1210,445))
ty,bu=type_mask(im,8)
# despeckle: drop components smaller than 1 native px^2 * 8^2 * 3
lab,n=nd.label(ty)
sz=nd.sum(ty,lab,range(1,n+1))
keep=np.zeros(n+1,bool); keep[1:]=sz> (8*8*3)
tyc=keep[lab]
print("components %d -> kept %d (dropped %d specks)"%(n,int(keep.sum()),n-int(keep.sum())))
print("%7s %6s %8s %8s %8s   (despeckled)"%("angle","bands","cap","gap","gap/cap"))
for ang in np.arange(-46,-20,1.0):
    s=segs_at(tyc,8,ang)
    if len(s)!=2: print("%7.1f %6d"%(ang,len(s))); continue
    cap=(s[0][1]-s[0][0]+1)/8.; gap=(s[1][0]-s[0][1]-1)/8.
    print("%7.1f %6d %8.2f %8.2f %8.3f"%(ang,len(s),cap,gap,gap/cap))
# independent reading angle: principal axis of the LOWER word only.
# split the mask at the trough found at -35 deg, map components to words by their
# projection onto the -35 deg normal.
th=np.radians(-35.0)
ys,xs=np.nonzero(tyc)
proj = xs*np.sin(th)+ys*np.cos(th)      # coordinate along the stacking direction
hist,edges=np.histogram(proj,bins=60)
lo=np.argmin(hist[len(hist)//3:2*len(hist)//3])+len(hist)//3
cut=edges[lo]
print("split at proj %.1f (trough bin %d, count %d)"%(cut,lo,hist[lo]))
for name,sel in (("100%",proj<cut),("Calidad",proj>=cut)):
    X=xs[sel]-xs[sel].mean(); Y=ys[sel]-ys[sel].mean()
    C=np.cov(np.vstack([X,Y])); ev,evec=np.linalg.eigh(C)
    v=evec[:,np.argmax(ev)]
    print("  %-8s px %6d  principal axis %+6.1f deg  extent-ratio %.2f"%(
        name,sel.sum(),np.degrees(np.arctan2(v[1],v[0])),np.sqrt(ev.max()/max(ev.min(),1e-9))))

print()
print("=== what the PROBE's own (speckled) mask does at its winning angle -37.5 ===")
for ang in (-37.5,-35.0,-32.0):
    rot=nd.rotate(ty.astype(float),ang,reshape=True,order=1)>0.5
    prof=rot.sum(1);nz=np.nonzero(prof)[0]
    seg,run=[],None
    for i in range(nz.min(),nz.max()+2):
        p=prof[i] if i<len(prof) else 0
        if p>0 and run is None: run=i
        if p==0 and run is not None: seg.append((run,i-1));run=None
    print(" ang %+.1f  ALL runs (len in native px): %s"%(ang,
        [(a,b,round((b-a+1)/8.,2)) for a,b in seg]))
    kept=[s for s in seg if (s[1]-s[0]+1)>8*1.5]
    print("            KEPT (>1.5 native px): %s"%[(a,b,round((b-a+1)/8.,2)) for a,b in kept])
    if len(kept)==2:
        cap=(kept[0][1]-kept[0][0]+1)/8.;gap=(kept[1][0]-kept[0][1]-1)/8.
        print("            -> cap %.2f gap %.2f gap/cap %.3f   <-- gap SPANS the dropped runs"%(cap,gap,gap/cap))
