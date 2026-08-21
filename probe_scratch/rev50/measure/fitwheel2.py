"""Adaptive per-ray 50%-level edge extraction + robust ellipse fits.
Returns outer (flange lip) ellipse and inner (cap edge) constrained fit."""
import sys; sys.path.insert(0,'/home/user/combi_render/probe_scratch/rev50/measure')
import numpy as np, rays, ellip, wheelfit as W

def ell_r(d, a):
    """radius of ellipse d along ray angle a from its centre"""
    c,s=np.cos(d['ang']),np.sin(d['ang'])
    ca,sa=np.cos(a),np.sin(a)
    u=(c*ca+s*sa)/d['a']; v=(-s*ca+c*sa)/d['b']
    return 1.0/np.hypot(u,v)

def extract(V, d_out, d_in_c, angs, frac=0.5, rmax=None, step=0.15,
            excl=None, plateau=0.30):
    """d_out: dict outer ellipse; d_in_c: (x0,y0,s) inner constrained.
       For each ray, adaptive level = dark + frac*(bright-dark)."""
    OP=[]; IP=[]; info=[]
    a_ref,b_ref,ang = d_out['a'], d_out['b'], d_out['ang']
    xi,yi,si = d_in_c
    d_in = dict(a=a_ref*si, b=b_ref*si, ang=ang, x0=xi, y0=yi)
    for a in angs:
        Ro = ell_r(d_out,a); Ri = ell_r(d_in,a)
        # ray from OUTER centre for the outer edge
        r,v = rays.ray_profile(V, d_out['x0'], d_out['y0'], a, Ro*1.6, step)
        cream = v[(r>Ri*1.12+2)&(r<Ro*0.92)]
        if cream.size<4: continue
        Pc = np.median(cream)
        tyre = v[(r>Ro*1.15)&(r<Ro*1.45)]
        if tyre.size<4: continue
        Pt = np.percentile(tyre,30)
        lev = Pt + frac*(Pc-Pt)
        ro = rays.subpix_cross(r,v,lev, Ro*0.90, Ro*1.20, rising=False)
        if ro is not None and Pc-Pt>40: OP.append((d_out['x0']+ro*np.cos(a), d_out['y0']+ro*np.sin(a), a, ro, Pc, Pt, lev))
        # inner edge: ray from INNER centre
        r2,v2 = rays.ray_profile(V, xi, yi, a, Ro*1.3, step)
        Ri2 = ell_r(d_in,a)
        chrome = v2[(r2>Ri2*0.45)&(r2<Ri2*0.86)]
        cream2 = v2[(r2>Ri2*1.14+2)&(r2<Ro*0.90)]
        if chrome.size<4 or cream2.size<4: continue
        Pch = np.median(chrome); Pcr = np.median(cream2)
        lev2 = Pch + frac*(Pcr-Pch)
        ri = rays.subpix_cross(r2,v2,lev2, Ri2*0.82, Ri2*1.22, rising=True)
        if ri is not None and Pcr-Pch>40:
            IP.append((xi+ri*np.cos(a), yi+ri*np.sin(a), a, ri, Pcr, Pch, lev2))
    return np.array(OP), np.array(IP)

def robust_ell(P, niter=8, kap=2.5, floor=1.0):
    pts=P[:,:2]; keep=np.ones(len(pts),bool)
    for _ in range(niter):
        d=ellip.decode(ellip.fit_ellipse(pts[keep,0],pts[keep,1]))
        r=W.ell_pt_dist(pts,d['x0'],d['y0'],d['a'],d['b'],d['ang'])*d['a']
        s=np.std(r[keep]); keep=np.abs(r)<max(floor,kap*s)
    return d,keep,r

def robust_con(P, d_out, niter=8, kap=2.5, floor=1.0):
    pts=P[:,:2]; keep=np.ones(len(pts),bool)
    p=[d_out['x0'],d_out['y0'],0.65]
    for _ in range(niter):
        p,f=W.constrained_fit(pts[keep], d_out['a'],d_out['b'],d_out['ang'], p[0],p[1])
        r=W.ell_pt_dist(pts,p[0],p[1],p[2]*d_out['a'],p[2]*d_out['b'],d_out['ang'])*p[2]*d_out['a']
        s=np.std(r[keep]); keep=np.abs(r)<max(floor,kap*s)
    return p,keep,r
