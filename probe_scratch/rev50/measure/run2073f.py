import sys; sys.path.insert(0,'/home/user/combi_render/probe_scratch/rev50/measure')
import numpy as np, rays, ellip, wheelfit as W
img=rays.load('/home/user/combi_render/IMG_2073.jpeg'); V=img.max(2)
cx,cy=744.,811.
angs=np.deg2rad(np.arange(0,360,0.5))
OP,IP=W.edges(V,cx,cy,85,155.,215.,angs,18,55,30,80)

def robust(P, niter=6):
    pts=P[:,:2].copy(); keep=np.ones(len(pts),bool)
    for _ in range(niter):
        d=ellip.decode(ellip.fit_ellipse(pts[keep,0],pts[keep,1]))
        r=W.ell_pt_dist(pts,d['x0'],d['y0'],d['a'],d['b'],d['ang'])*d['a']
        s=np.std(r[keep]); keep=np.abs(r)<max(2.0,2.5*s)
    return d, keep, r
d,keepO,rO = robust(OP)
print('OUTER robust: c=(%.3f,%.3f) a=%.3f b=%.3f b/a=%.5f ang=%.2f  kept %d/%d rms %.2f'%(
  d['x0'],d['y0'],d['a'],d['b'],d['b']/d['a'],np.rad2deg(d['ang']),keepO.sum(),len(keepO),np.std(rO[keepO])))

# inner: use only angles where interior is genuinely dark.  Report which.
ang_deg=np.rad2deg(IP[:,2])
# distance of inner pts from a constrained family
def cfit(mask,label):
    p,f=W.constrained_fit(IP[mask,:2], d['a'],d['b'],d['ang'], d['x0'],d['y0'])
    rr=f*d['a']*p[2]
    # signed offset along minor-axis dir (image), and along major
    off=np.array([p[0]-d['x0'],p[1]-d['y0']])
    mind=d['mindir']; majd=d['majdir']
    print('%-22s n=%3d  s=%.4f  c=(%.3f,%.3f)  d_minor=%+.3f px  d_major=%+.3f px  rms=%.2f'%(
      label,mask.sum(),p[2],p[0],p[1],off@mind,off@majd,np.std(rr)))
    return p,off@mind
allm=np.ones(len(IP),bool)
cfit(allm,'inner ALL angles')
clean=~(((ang_deg>=200)&(ang_deg<=285)))
cfit(clean,'inner excl 200-285')
