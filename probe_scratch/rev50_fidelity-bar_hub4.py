import numpy as np, math
from PIL import Image
def load(p): return np.asarray(Image.open(p).convert('RGB')).astype(float)

def radprof(im,cx,cy,rmax,kR,kG,kB,n=720,step=0.20):
    out=[]
    for k in range(n):
        th=2*math.pi*k/n; last=0.0; r=2.0
        while r<rmax:
            x=int(round(cx+r*math.cos(th))); y=int(round(cy+r*math.sin(th)))
            if 0<=y<im.shape[0] and 0<=x<im.shape[1]:
                p=im[y,x]
                if p[0]>kR and p[1]<kG*p[0] and p[2]<kB*p[0]: last=r
            r+=step
        out.append(last)
    return np.array(out)

def centroid(im,box,kR,kG,kB):
    y0,y1,x0,x1=box; sub=im[y0:y1,x0:x1]
    m=(sub[...,0]>kR)&(sub[...,1]<kG*sub[...,0])&(sub[...,2]<kB*sub[...,0])
    ys,xs=np.nonzero(m); return xs.mean()+x0, ys.mean()+y0, m.sum()

def report(tag,im,box,rmax,ths):
    for (kR,kG,kB) in ths:
        cx,cy,n=centroid(im,box,kR,kG,kB)
        rp=radprof(im,cx,cy,rmax,kR,kG,kB)
        s=np.sort(rp); med=np.median(rp)
        print("%-28s th(%3d,%.2f,%.2f) c=(%.1f,%.1f) n=%5d  med %.2f p25 %.2f p75 %.2f max %.2f  lobefrac %.3f  (max-med)/med %.3f"
              %(tag,kR,kG,kB,cx,cy,n,med,s[179],s[539],rp.max(),(rp>med+2).mean(),(rp.max()-med)/med))
    return med

R=load('out/r49base_side.png'); PPM=271.1864
P=load('ref_side.jpg')
ths=[(85,0.70,0.70),(95,0.62,0.70),(75,0.75,0.80)]
print("== RENDER side, REAR wheel ==")
report("render rear",R,(805,945,1030,1170),60,ths)
print("== RENDER side, FRONT wheel ==")
# front axle X ~ +0.900?  find red dome near px for X_AXLE_F
print("   (locate) ")
# scan a box around expected front hub
for XA in (0.90,0.94,0.98):
    cx0=800.0-PPM*XA; cy0=962.203-PPM*0.3325
    print("   X=%.2f -> px %.0f,%.0f"%(XA,cx0,cy0))
report("render front",R,(805,945,470,610),60,ths)
print("== PHOTO ref_side, REAR wheel ==")
report("photo rear",P,(575,640,715,785),45,ths)

# tyre radii, same frames: dark ring below the hub centre
def tyreR(im,cx,cy,thr=110,maxd=200):
    lum=im[...,:3].mean(axis=2); col=lum[int(cy):int(cy)+maxd,int(cx)]
    d=np.nonzero(col<thr)[0]
    # longest run containing small dy
    return d.max()
cxr,cyr,_=centroid(R,(805,945,1030,1170),95,0.62,0.70)
cxp,cyp,_=centroid(P,(575,640,715,785),95,0.62,0.70)
print("\nrender rear tyre R px", tyreR(R,cxr,cyr), " photo rear tyre R px", tyreR(P,cxp,cyp,thr=95,maxd=90))
