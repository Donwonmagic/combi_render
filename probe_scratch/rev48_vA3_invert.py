"""Regenerate the decal at several LINE_GAP values INTO SCRATCH ONLY and run the
probe's own estimator on each.  Gives reading-vs-LINE_GAP for the real glyphs."""
import os, sys, importlib.util, numpy as np, shutil
from PIL import Image
from scipy import ndimage as nd
sys.path.insert(0,"/home/user/combi_render")
os.chdir("/home/user/combi_render")
SCR="/home/user/combi_render/probe_scratch/rev48_vA3_tex"
os.makedirs(SCR,exist_ok=True)

def bands(ty,Z,lo=-45.0,hi=10.0):
    best=None
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
        if best is None or gap>best[3]: best=(gap/cap,ang,cap,gap)
    return best
def type_mask(img,Z):
    big=img.resize((img.width*Z,img.height*Z),Image.LANCZOS)
    a=np.asarray(big.convert("RGB"),np.float32)
    R,G,B=a[...,0],a[...,1],a[...,2]
    mx=a.max(2); sat=(mx-a.min(2))/np.maximum(mx,1)
    red=(R>90)&(R-G>40)&(R-B>25)
    burst=nd.binary_fill_holes(nd.binary_closing(red,np.ones((9,9))))
    lab,n=nd.label(burst)
    if n>1: burst=lab==(int(np.argmax(nd.sum(burst,lab,range(1,n+1))))+1)
    return nd.binary_opening(burst&(mx>150)&(sat<0.30),np.ones((5,5))),burst

def truthgap(img):
    """construction truth from the full-res raster: clear gap / cap along -19.7"""
    a=np.asarray(img.convert("RGB"),np.float32); H=a.shape[0]
    R,G,B=a[...,0],a[...,1],a[...,2]; mx=a.max(2); sat=(mx-a.min(2))/np.maximum(mx,1)
    red=(R>90)&(R-G>40)&(R-B>25)
    burst=nd.binary_fill_holes(nd.binary_closing(red,np.ones((9,9))))
    lab,n=nd.label(burst); burst=lab==(int(np.argmax(nd.sum(burst,lab,range(1,n+1))))+1)
    ty=nd.binary_opening(burst&(mx>150)&(sat<0.30),np.ones((5,5)))
    rot=nd.rotate(ty.astype(float),19.7,reshape=True,order=1)>0.5
    prof=rot.sum(1); nz=np.nonzero(prof)[0]
    seg,run=[],None
    for i in range(nz.min(),nz.max()+2):
        p=prof[i] if i<len(prof) else 0
        if p>0 and run is None: run=i
        if p==0 and run is not None: seg.append((run,i-1)); run=None
    seg=[s for s in seg if (s[1]-s[0]+1)>10]
    if len(seg)!=2: return None
    cap=seg[0][1]-seg[0][0]+1; gap=seg[1][0]-seg[0][1]-1
    return gap/cap, cap, gap

print("LINE_GAP  construction(true, -19.7)   estimator@44px    read/true")
for lg in [0.20,0.26,0.32,0.38,0.43,0.50]:
    spec=importlib.util.spec_from_file_location("cg%d"%int(lg*100),"cal_gen.py")
    cg=importlib.util.module_from_spec(spec); spec.loader.exec_module(cg)
    cg.TEX=SCR
    cg.LINE_GAP=lg; cg.LINE_SEP=cg.LINE_SEP_BASE+lg*cg.CAP_100
    import io,contextlib
    buf=io.StringIO()
    try:
        with contextlib.redirect_stdout(buf): cg.main()
    except SystemExit as e:
        print("  %.2f  GUARD: %s"%(lg,str(e)[:60])); continue
    d=Image.open(os.path.join(SCR,"calidad.png")).convert("RGB")
    t=truthgap(d)
    k=44.0/float(d.width)*3.0
    sm=d.resize((max(8,int(d.width*k)),max(8,int(d.height*k))),Image.LANCZOS)
    r=bands(type_mask(sm,8)[0],8)
    tt = ("%.4f (cap %d gap %d)"%t) if t else "TOUCHING (no 2 bands)"
    rr = ("%.4f"%r[0]) if r else "none"
    ra = ("%.3f"%(r[0]/t[0])) if (r and t) else "-"
    print("  %.2f      %-26s   %-8s   %s"%(lg,tt,rr,ra))
    os.rename(os.path.join(SCR,"calidad.png"), os.path.join(SCR,"calidad_%03d.png"%int(lg*100)))
