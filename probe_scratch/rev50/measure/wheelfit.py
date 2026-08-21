import sys, numpy as np
sys.path.insert(0,'/home/user/combi_render/probe_scratch/rev50/measure')
import rays, ellip
from scipy.optimize import least_squares

def edges(V, cx, cy, rmax, level_out, level_in, angs, r_in_lo, r_in_hi,
          r_out_lo, r_out_hi, step=0.2):
    """returns outer edge pts (bright->dark, falling outward) and inner edge pts
       (dark->bright, rising outward)"""
    OP=[]; IP=[]
    for a in angs:
        r,v = rays.ray_profile(V,cx,cy,a,rmax,step)
        ro = rays.subpix_cross(r,v,level_out,r_out_lo,r_out_hi,rising=False)
        ri = rays.subpix_cross(r,v,level_in ,r_in_lo ,r_in_hi ,rising=True)
        if ro is not None: OP.append((cx+ro*np.cos(a), cy+ro*np.sin(a), a, ro))
        if ri is not None: IP.append((cx+ri*np.cos(a), cy+ri*np.sin(a), a, ri))
    return np.array(OP), np.array(IP)

def ell_pt_dist(pts, x0,y0,a,b,ang):
    """approx signed radial distance of pts from ellipse (in 'unit-circle' metric * a)"""
    c,s = np.cos(ang), np.sin(ang)
    dx = pts[:,0]-x0; dy = pts[:,1]-y0
    u = ( c*dx + s*dy)/a
    v = (-s*dx + c*dy)/b
    return (np.hypot(u,v)-1.0)

def constrained_fit(pts, a_ref, b_ref, ang, x0g, y0g):
    """fit centre + uniform scale, holding axis-ratio and orientation."""
    def res(p):
        x0,y0,s = p
        return ell_pt_dist(pts, x0,y0, s*a_ref, s*b_ref, ang)
    s0 = 1.0
    r = least_squares(res, [x0g,y0g,s0], method='lm')
    return r.x, r.fun
