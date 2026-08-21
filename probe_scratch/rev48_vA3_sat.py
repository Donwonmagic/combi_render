import numpy as np, math
from PIL import Image
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None
def bands(ty,Z,lo=-55.,hi=15.):
    best=None; allr=[]
    for ang in np.arange(lo,hi,0.5):
        rot=nd.rotate(ty.astype(float),ang,reshape=True,order=1)>0.5
        prof=rot.sum(1); nz=np.nonzero(prof)[0]
        if len(nz)==0: continue
        seg,run=[],None
        for i in range(nz.min(),nz.max()+2):
            p=prof[i] if i<len(prof) else 0
            if p>0 and run is None: run=i
            if p==0 and run is not None: seg.append((run,i-1)); run=None
        seg=[s for s in seg if (s[1]-s[0]+1)>Z*1.5]
        if len(seg)!=2: continue
        cap=(seg[0][1]-seg[0][0]+1)/Z; gap=(seg[1][0]-seg[0][1]-1)/Z
        if gap<=0: continue
        allr.append((ang,gap/cap,cap,gap))
        if best is None or gap>best[3]: best=(gap/cap,ang,cap,gap)
    return best,allr
def go(f,box,Z,tag,satT,save=None,angref=None):
    im=Image.open(f).convert("RGB").crop(box)
    big=im.resize((im.width*Z,im.height*Z),Image.LANCZOS)
    a=np.asarray(big,np.float32); mx=a.max(2); mn=a.min(2)
    sat=(mx-mn)/np.maximum(mx,1)
    R,G,B=a[...,0],a[...,1],a[...,2]
    burst=(sat>satT)&(R>=G)&(R>=B)
    burst=nd.binary_closing(burst,np.ones((2*Z,2*Z)))
    lab,n=nd.label(burst)
    burst=lab==(int(np.argmax(nd.sum(burst,lab,range(1,n+1))))+1)
    fill=nd.binary_fill_holes(burst)
    h=nd.binary_opening(fill&~burst,np.ones((Z//2,Z//2)))
    lab,n=nd.label(h)
    if n:
        sz=nd.sum(h,lab,range(1,n+1))
        h=np.isin(lab,[i+1 for i in range(n) if sz[i]>Z*Z*2])
    ys,xs=np.nonzero(fill)
    print("%-12s burst %.1f x %.1f px  typepx %d  ncomp %d"%(tag,(xs.ptp()+1)/Z,(ys.ptp()+1)/Z,h.sum(),nd.label(h)[1]))
    b,allr=bands(h,Z)
    print("   argmax-gap:",("gap/cap %.3f ang %.1f cap %.2f gap %.2f"%b) if b else "NOT SEPARABLE")
    if angref is not None:
        near=[r for r in allr if abs(r[0]-angref)<3.0]
        if near:
            near.sort(key=lambda r:abs(r[0]-angref))
            print("   at true angle %.1f: gap/cap %.3f  cap %.2f  gap %.2f (ang %.1f)"%(angref,near[0][1],near[0][2],near[0][3],near[0][0]))
        else: print("   at true angle %.1f: no two-band split"%angref)
    # spike count: radial profile of burst boundary
    cy,cx=nd.center_of_mass(fill)
    th=np.linspace(0,2*np.pi,720,endpoint=False); rad=[]
    for t in th:
        rr=np.arange(0,int(max(fill.shape)/2),1.0)
        yy=(cy+rr*np.sin(t)).astype(int); xx=(cx+rr*np.cos(t)).astype(int)
        ok=(yy>=0)&(yy<fill.shape[0])&(xx>=0)&(xx<fill.shape[1])
        v=np.zeros(len(rr),bool); v[ok]=fill[yy[ok],xx[ok]]
        idx=np.nonzero(v)[0]; rad.append(idx.max() if len(idx) else 0)
    rad=np.array(rad,float); rs=nd.uniform_filter1d(rad,5,mode='wrap')
    base=nd.uniform_filter1d(rad,120,mode='wrap')
    d=rs-base
    peaks=[i for i in range(720) if d[i]>0.02*base[i] and d[i]>=d[(i-1)%720] and d[i]>d[(i+1)%720]]
    # merge adjacent
    m=[]; 
    for p in peaks:
        if m and (p-m[-1])<6: continue
        m.append(p)
    amp=np.mean([d[i]/base[i] for i in m]) if m else 0
    print("   burst spikes ~%d   mean spike depth %.3f of radius   aspect %.2f"%(len(m),amp,(xs.ptp()+1)/(ys.ptp()+1)))
    if save:
        o=np.zeros(h.shape+(3,),np.uint8); o[...,0]=fill*70; o[...,1]=h*255; o[...,2]=h*255
        Image.fromarray(o).resize((im.width*4,im.height*4)).save(save)
go("IMG_2073.jpeg",(1108,360,1210,445),8,"2073 GREEN",0.30,"probe_scratch/rev48_vA3_s_2073.png",angref=-19.7)
go("ref_side.jpg",(728,300,845,392),8,"side RED",0.30,"probe_scratch/rev48_vA3_s_side.png",angref=-19.7)
go("ref_rear34.jpg",(748,288,862,378),8,"rear34 RED",0.28,"probe_scratch/rev48_vA3_s_rear.png",angref=-19.7)
