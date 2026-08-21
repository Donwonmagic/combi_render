"""REV51 A2 -- the wheel scene, built from the SAME literals as t1_detail.py."""
import numpy as np
from r51_geom import Cone, Disc, revolve_profile, camera_rays, cast

TIRE_R = 0.3325
RIM_R  = 0.2198
CAP_R  = 0.1345
CAP_D  = 2*(CAP_R + 0.0025)
FLANGE_AUTHORED = 0.1905
S = RIM_R / FLANGE_AUTHORED

M_TYRE, M_RIM, M_CAP, M_EMB, M_BODY = 0, 1, 2, 3, 4

def tyre_profile():
    up = [(0.0530,0.1905),(0.0625,0.2020),(0.0705,0.2220),(0.0728,0.2340),
          (0.0745,0.2500),(0.0752,0.2760),(0.0744,0.2905),(0.0735,0.2980),
          (0.0690,0.3110),(0.0640,0.3195),(0.0578,0.3262)]
    def crown(y): return TIRE_R - 0.0042*(abs(y)/0.0522)**2
    tread=[]
    for (y,d) in [(-0.0522,0),(-0.0400,0),(-0.0378,1),(-0.0300,1),(-0.0278,0),
                  (-0.0150,0),(-0.0128,1),(-0.0022,1),(0.0000,0),(0.0128,0),
                  (0.0150,1),(0.0256,1),(0.0278,0),(0.0400,0),(0.0422,1),
                  (0.0500,1),(0.0522,0)]:
        tread.append((y, crown(y)-(0.0080 if d else 0.0)))
    BEAD_AUTHORED=0.1905; SHOULDER=up[-1][1]
    k=(SHOULDER-RIM_R)/(SHOULDER-BEAD_AUTHORED)
    bead=lambda r: SHOULDER-(SHOULDER-r)*k
    up=[(y,bead(r)) for (y,r) in up]
    prof=list(up)+tread[::-1]+[(-y,r) for (y,r) in up[::-1]]
    ib=bead(0.1880)
    prof+= [(-0.0500,ib),(0.0500,ib)]
    return prof

def barrel_profile():
    prof=[(0.0600,0.1905),(0.0640,0.1885),(0.0625,0.1820),(0.0560,0.1795),
          (0.0520,0.1720),(0.0480,0.1660),(0.0300,0.1640),(0.0080,0.1650),
          (-0.0080,0.1700),(-0.0200,0.1790),(-0.0230,0.1860),(-0.0190,0.1900),
          (-0.0250,0.1905),(-0.0300,0.1880),(-0.0290,0.1800),(-0.0180,0.1690),
          (-0.0060,0.1600),(0.0120,0.1560),(0.0330,0.1560),(0.0480,0.1590),
          (0.0540,0.1660),(0.0570,0.1760),(0.0560,0.1840)]
    return [(y,r*S) for (y,r) in prof]

def disc_profile(dish=0.0):
    """dish = extra INBOARD sink applied to the outer part of the disc face,
    ramped 0 at r=0 to full at the flange -- mechanism (b)'s cure."""
    dp=[(0.0500,0.1600),(0.0560,0.1560),(0.0570,0.1400),(0.0520,0.1200),
        (0.0450,0.0900),(0.0430,0.0620),(0.0450,0.0400),(0.0470,0.0000)]
    dp=[(y,r*S) for (y,r) in dp]
    out=[]
    for (y,r) in dp:
        out.append((y - dish*(r/(RIM_R)), r))
    front=out
    back=[(y-0.010,r) for (y,r) in reversed(out)]
    return front+back

def cap_profile(dy=0.0):
    R=CAP_R
    prof=[(0.0745,0.0000),(0.0736,0.0300),(0.0710,0.0560),(0.0664,0.0800),
          (0.0596,0.1010),(0.0502,0.1180),(0.0378,0.1288),(0.0236,0.1342),
          (0.0120,R),(0.0040,R+0.0025),(-0.0035,R+0.0010),(-0.0020,R-0.0060),
          (0.0080,R-0.0090),(0.0220,0.1315),(0.0362,0.1262),(0.0484,0.1155),
          (0.0576,0.0988),(0.0644,0.0780),(0.0690,0.0545),(0.0716,0.0292),
          (0.0725,0.0000)]
    return [(y+dy,r) for (y,r) in prof]

CAP_APEX_AUTHORED   = 0.0745
CAP_SILH_R          = 0.1370          # max r of cap profile
CAP_SILH_Y_AUTHORED = 0.0040          # y at that max r
FLANGE_FACE_Y       = 0.0640          # max y of barrel prof (r=0.2175)
FLANGE_FACE_R       = 0.1885*S
DOME_H              = CAP_APEX_AUTHORED - CAP_SILH_Y_AUTHORED   # 0.0705

def scene(cap_dy=0.0, dish=0.0, emblem=True):
    prims=[]
    prims += revolve_profile(tyre_profile(), M_TYRE)
    prims += revolve_profile(barrel_profile(), M_RIM)
    prims += revolve_profile(disc_profile(dish), M_RIM)
    prims += revolve_profile(cap_profile(cap_dy), M_CAP)
    if emblem:
        ro = 0.3170*CAP_D/2
        prims.append(Disc(CAP_APEX_AUTHORED+cap_dy+0.0060, 0.0, ro, M_EMB))
    return prims

def true_proud(cap_dy):
    """apex proudness above the rim flange FACE, metres"""
    return (CAP_APEX_AUTHORED + cap_dy) - FLANGE_FACE_Y


# ------------------------------------------------------------------ render
ALB = np.array([[0.045,0.045,0.048],     # tyre
                [0.88,0.86,0.80],        # cream rim
                [0.72,0.11,0.09],        # red cap
                [0.95,0.95,0.95],        # emblem
                [0.60,0.10,0.09]])       # body

def render(prims, phi_deg, eps_deg=0.0, dist=4.0, f_px=1800.0, W=520, H=520,
           bg=0.35, seed=0, noise=0.010, blur=0.9, roll_deg=0.0):
    phi=np.radians(phi_deg); eps=np.radians(eps_deg)
    v=np.array([np.sin(phi)*np.cos(eps), np.cos(phi), np.sin(phi)*np.sin(eps)])
    C=v*dist
    up=(0.0,0.0,1.0)
    if roll_deg:
        rr=np.radians(roll_deg); up=(0.0,np.sin(rr),np.cos(rr))
    Cc,d=camera_rays(W,H,f_px,C,(0,0,0),up=up)
    t,m,n=cast(Cc,d,prims)
    L=np.array([0.4,0.75,0.55]); L=L/np.linalg.norm(L)
    lam=np.clip((n*L).sum(-1),0,1)
    img=np.full((H,W,3),bg,float)
    hit=m>=0
    alb=ALB[np.clip(m,0,4)]
    shade=(0.42+0.58*lam)[...,None]
    spec=np.clip((n*L).sum(-1),0,1)**28
    col=alb*shade+0.35*spec[...,None]
    img=np.where(hit[...,None],col,img)
    rng=np.random.default_rng(seed)
    if blur>0:
        from scipy.ndimage import gaussian_filter
        img=gaussian_filter(img,(blur,blur,0))
    img=img+rng.normal(0,noise,img.shape)
    return np.clip(img,0,1), m, t
