"""Run the probe's BUILT-side estimator on the pre-1bfc97a (LINE_GAP=0.26) raster
and on the shipped (LINE_GAP=0.43) raster.  No project file is written."""
import numpy as np
from PIL import Image
from scipy import ndimage as nd
Image.MAX_IMAGE_PIXELS=None
exec(open("probe_scratch/rev48_verifyA_photo.py").read().split('src=Image.open')[0].split('"""')[2])
def read(path,target=44):
    d=Image.open(path).convert("RGB")
    k=target/float(d.width)*3.0
    s=d.resize((max(8,int(d.width*k)),max(8,int(d.height*k))),Image.LANCZOS)
    ty,_=type_mask(s,8)
    return bands(ty,8)
def truth_fullres(path,lo=-30,hi=-8):
    a=np.asarray(Image.open(path).convert("RGBA"),np.float32)
    wm=(a[...,3]/255.>0.5)&(a[...,0]>200)&(a[...,1]>195)&(a[...,2]>190)
    rot=nd.rotate(wm.astype(float),-19.7,reshape=True,order=1)>0.5
    prof=rot.sum(1);nz=np.nonzero(prof)[0]
    seg,run=[],None
    for i in range(nz.min(),nz.max()+2):
        p=prof[i] if i<len(prof) else 0
        if p>0 and run is None: run=i
        if p==0 and run is not None: seg.append((run,i-1));run=None
    seg=[s for s in seg if s[1]-s[0]+1>3]
    if len(seg)!=2: return None
    cap=seg[0][1]-seg[0][0]+1;gap=seg[1][0]-seg[0][1]-1
    return gap/cap,cap,gap
for name,path in (("LINE_GAP 0.26 (pre-1bfc97a)","probe_scratch/rev48_verifyA_calidad_LG026.png"),
                  ("LINE_GAP 0.43 (shipped)","tex/calidad.png")):
    t=truth_fullres(path); r=read(path)
    print("%-28s full-res truth %s | photo-scale reading %s"%(
        name, ("%.4f (cap %d gap %d)"%t) if t else "NONE",
        ("%.4f ang %.1f cap %.2f gap %.2f"%r) if r else "NO BANDS"))
    if t and r: print("%-28s  bias reading/truth = %.3f   reading-truth = %+.4f"%("",r[0]/t[0],r[0]-t[0]))
