"""ATTACK on the W4-headlamp finding.

QUESTION: on a PERFECTLY FLAT nose (normal +X, both circles in the plane,
lamp axis +X -- i.e. exactly what build.py builds), does there exist ANY
camera pose + focal length that reproduces, simultaneously, the ellipses
measured on ref_workshop.jpg?

3-D (undropped body frame, from build.py):
  roundel  (2.1290, 0.000, 1.10248)  R = 0.140    normal +X
  near HL  (2.1116, 0.545, 0.93300)  R = free     normal +X
  offsets in the nose plane: dy = +0.545, dz = -0.16948

IMAGE (ref_workshop.jpg 1200x824, my own windows, re-read at 8-10x):
  roundel centre (306.5, 547.5)  bbox 61 x 91   aspect 0.670
  near HL centre (416.8, 630.5)  bbox 74 x 70   aspect 1.057 (moment 0.908)

Free: camera position (D along a bearing), yaw theta, pitch eps, roll, f, r_lamp.
Full pinhole, no small-angle approximation; circle sampled at 720 points and
BOUNDING BOX taken, exactly as the pixel measurement does.

CEILING: assumes the roundel really is a circle of 0.280 m and that both
circles are concentric with what the pixel window enclosed.  Principal point
assumed at the image centre (600,412) -- a cropped/uncentred original would
move the answer; that is tested by a sweep.
"""
import numpy as np, itertools, math
from scipy.optimize import least_squares

W,H = 1200.,824.
PPX,PPY = 600.,412.

RO_C = np.array([2.1290, 0.000, 1.10248]); RO_R = 0.140
HL_C = np.array([2.1116, 0.545, 0.93300])

OBS = dict(ro_c=(306.5,547.5), ro_wh=(61.,91.),
           hl_c=(416.8,630.5), hl_wh=(74.,70.))

def cam_matrix(yaw,pitch,roll):
    cy,sy=math.cos(yaw),math.sin(yaw); cp,sp=math.cos(pitch),math.sin(pitch)
    cr,sr=math.cos(roll),math.sin(roll)
    Rz=np.array([[cy,-sy,0],[sy,cy,0],[0,0,1]])
    Ry=np.array([[cp,0,sp],[0,1,0],[-sp,0,cp]])
    Rx=np.array([[1,0,0],[0,cr,-sr],[0,sr,cr]])
    return Rz@Ry@Rx

def project(P, C, Rm, f):
    # world -> camera.  camera looks along its +Z after Rm
    v = (P - C) @ Rm            # rows of P are points
    z = v[...,2]
    return np.stack([PPX + f*v[...,0]/z, PPY + f*v[...,1]/z], -1), z

def circle_bbox(centre, R, normal, C, Rm, f, n=720):
    n_ = normal/np.linalg.norm(normal)
    a = np.cross(n_,[0,0,1.]); a/=np.linalg.norm(a)
    b = np.cross(n_,a)
    t = np.linspace(0,2*math.pi,n,endpoint=False)
    P = centre + R*(np.outer(np.cos(t),a)+np.outer(np.sin(t),b))
    uv,z = project(P,C,Rm,f)
    if (z<=0).any(): return None
    return uv[:,0].min(),uv[:,0].max(),uv[:,1].min(),uv[:,1].max()

def resid(p):
    D,theta,eps,roll,f,rl = p
    # camera placed at distance D from the roundel, bearing theta (azimuth from
    # +X, toward +Y = the near side) and elevation eps
    C = RO_C + D*np.array([math.cos(theta)*math.cos(eps),
                           math.sin(theta)*math.cos(eps),
                           math.sin(eps)])
    # camera looks back at a point between the two features
    look = 0.5*(RO_C+HL_C) - C; look/=np.linalg.norm(look)
    zc = look
    up = np.array([0,0,1.])
    xc = np.cross(up,zc); xc/=np.linalg.norm(xc)
    yc = np.cross(zc,xc)
    cr,sr = math.cos(roll),math.sin(roll)
    xc2 =  cr*xc + sr*yc
    yc2 = -sr*xc + cr*yc
    Rm = np.stack([xc2,-yc2,zc],1)     # image y down
    n = np.array([1.,0.,0.])
    r = circle_bbox(RO_C,RO_R,n,C,Rm,f)
    h = circle_bbox(HL_C,rl,n,C,Rm,f)
    if r is None or h is None: return np.ones(6)*1e3
    rc = ((r[0]+r[1])/2,(r[2]+r[3])/2); rw,rh = r[1]-r[0], r[3]-r[2]
    hc = ((h[0]+h[1])/2,(h[2]+h[3])/2); hw,hh = h[1]-h[0], h[3]-h[2]
    return np.array([rc[0]-OBS['ro_c'][0], rc[1]-OBS['ro_c'][1],
                     rw-OBS['ro_wh'][0], rh-OBS['ro_wh'][1],
                     hc[0]-OBS['hl_c'][0], hc[1]-OBS['hl_c'][1],
                     hw-OBS['hl_wh'][0], hh-OBS['hl_wh'][1]])

best=None
for D in (1.2,1.8,2.5,3.5,5.0):
 for th in (0.3,0.5,0.7,0.9,1.1):
  for ep in (0.05,0.2,0.35):
   for f in (300.,600.,1000.,1800.):
    for rl in (0.086,0.095):
     p0=np.array([D,th,ep,0.0,f,rl])
     try:
       s=least_squares(resid,p0,bounds=([0.5,0.05,-0.6,-0.6,150.,0.060],
                                        [12.,1.45,0.9,0.6,6000.,0.130]),
                       xtol=1e-12,ftol=1e-12,max_nfev=4000)
     except Exception: continue
     c=np.sum(s.fun**2)
     if best is None or c<best[0]: best=(c,s.x,s.fun)
c,x,fun=best
D,th,ep,roll,f,rl = x
print("FLAT-NOSE BEST FIT")
print(f"  cost {c:.4f}  rms {math.sqrt(c/8):.3f} px")
print(f"  D={D:.3f} m  azimuth={math.degrees(th):.1f} deg  elev={math.degrees(ep):.1f} deg")
print(f"  roll={math.degrees(roll):.1f} deg  f={f:.0f} px (HFOV {2*math.degrees(math.atan(600/f)):.1f} deg)")
print(f"  lamp aperture radius {rl:.4f} m (dia {2*rl:.3f})")
print("  residuals [roCx roCy roW roH hlCx hlCy hlW hlH] =", np.round(fun,2))
