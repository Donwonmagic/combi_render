import numpy as np, math
from PIL import Image

def load(p): return np.asarray(Image.open(p).convert('RGB')).astype(float)

def dome_radius_profile(im, cx, cy, rmax, redfn):
    """for 720 rays, the last radius (px) at which the pixel is still 'red'."""
    out=[]
    lum=im[...,:3]
    for k in range(720):
        th=2*math.pi*k/720
        last=0.0
        r=2.0
        while r<rmax:
            x=int(round(cx+r*math.cos(th))); y=int(round(cy+r*math.sin(th)))
            if 0<=y<im.shape[0] and 0<=x<im.shape[1]:
                p=im[y,x]
                if redfn(p): last=r
            r+=0.25
        out.append(last)
    return np.array(out)

# ---------------- RENDER ----------------
im=load('out/r49base_side.png')
PPM=271.1864
cx,cy=1099.25,873.95     # refined red-dome centroid, rear wheel
redfn=lambda p:(p[0]>85)and(p[1]<0.70*p[0])and(p[2]<0.70*p[0])
rp=dome_radius_profile(im,cx,cy,60,redfn)
rp_s=np.sort(rp)
print("RENDER rear hubcap red-boundary radius px: median %.2f  p10 %.2f  p25 %.2f  p75 %.2f  p90 %.2f  max %.2f"
      %(np.median(rp),rp_s[71],rp_s[179],rp_s[539],rp_s[647],rp.max()))
print("   -> median r = %.4f m ; max r = %.4f m ; built CAP_R = 0.1345 (+lip 0.1370)"
      %(np.median(rp)/PPM, rp.max()/PPM))
# how much of the circumference is 'lobe' (r > median + 2px)
lobe=(rp>np.median(rp)+2.0)
print("   fraction of rays on a lobe: %.3f"%lobe.mean())

# tyre outer radius in the same frame: dark ring, scan down from centre
lum=im[...,:3].mean(axis=2)
col=lum[int(cy):int(cy)+150,int(cx)]
dark=np.nonzero(col<110)[0]
print("   tyre bottom (dark run ends) at dy=%d px -> R_tyre=%.1f px = %.4f m (built 0.3325)"
      %(dark.max(),dark.max(),dark.max()/PPM))
Rt=dark.max()
print("   RENDER visible dome R / tyre R = %.4f   (built CAP_R/TIRE_R = %.4f)"
      %(np.median(rp)/Rt, 0.1345/0.3325))

# ---------------- PHOTOGRAPH ref_side.jpg rear wheel ----------------
ph=load('ref_side.jpg')
# rear wheel red dome: crop box quoted in source (736,591,764,619) is the EMBLEM.
# hubcap disc quoted 58.370 px diameter; find the dome centroid near (748,606)
sub=ph[575:640,715:785]
R,G,B=sub[...,0],sub[...,1],sub[...,2]
red=(R>70)&(G<0.62*R)&(B<0.70*R)
ys,xs=np.nonzero(red)
pcx,pcy=xs.mean()+715, ys.mean()+575
print("\nPHOTO ref_side rear dome centroid px",round(pcx,2),round(pcy,2),"n",red.sum())
pf=lambda p:(p[0]>70)and(p[1]<0.62*p[0])and(p[2]<0.70*p[0])
rp2=dome_radius_profile(ph,pcx,pcy,45,pf)
rp2_s=np.sort(rp2)
print("PHOTO dome radius px: median %.2f p25 %.2f p75 %.2f max %.2f  frac lobe %.3f"
      %(np.median(rp2),rp2_s[179],rp2_s[539],rp2.max(),(rp2>np.median(rp2)+2.0).mean()))
