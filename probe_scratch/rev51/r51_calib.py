"""REV51 A2 -- CALIBRATION.  Full pipeline, blind, on synthetics at known h."""
import numpy as np, sys
import r51_scene as SC, r51_inst as IN
from PIL import Image

def scores(img):
    V = img.max(-1); mn = img.min(-1); chroma = V - mn
    cream = V - 1.6*chroma
    red   = img[..., 0] - np.maximum(img[..., 1], img[..., 2])
    return cream, red, V, chroma

def blind_init(cream, red):
    """crude centre/radius from the image alone -- no ground truth"""
    m = (cream > 0.30) | (red > 0.10)
    ys, xs = np.nonzero(m)
    if len(xs) < 50: return None
    cx, cy = xs.mean(), ys.mean()
    r = np.sqrt(len(xs)/np.pi)
    return cx, cy, r

def run_pipeline(img, outboard_hint, ang_skip=None, verbose=False):
    cream, red, V, chroma = scores(img)
    ini = blind_init(cream, red)
    if ini is None: return None
    cx, cy, r = ini
    ang = np.linspace(0, 2*np.pi, 360, endpoint=False)
    if ang_skip is not None:
        ang = ang[~ang_skip(ang)]
    cf, cpts = IN.fit_boundary(cream, (cx, cy), 0.15*r, 1.35*r, ang, 0.30)
    if cf is None: return None
    rcap = 0.62*cf['a']
    kf, kpts = IN.fit_boundary(red, (cf['cx'], cf['cy']), 0.05*rcap, 1.30*rcap,
                               ang, 0.10)
    if kf is None: return None
    # emblem: bright + neutral, inside the cap
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]]
    d2 = (xx-kf['cx'])**2 + (yy-kf['cy'])**2
    em = (V > 0.62) & (chroma < 0.12) & (d2 < (0.6*kf['b'])**2)
    ec = None
    if em.sum() > 8:
        w = (V*em)
        ec = ((xx*w).sum()/w.sum(), (yy*w).sum()/w.sum())
    rc = IN.measure(cf, kf, outboard_hint, 'cap')
    re = IN.measure(cf, kf, outboard_hint, 'emb', feat_centre=ec) if ec else None
    return dict(cream=cf, cap=kf, emb=ec, cap_res=rc, emb_res=re,
                cpts=cpts, kpts=kpts)

def outboard_hint_from_geom(phi_deg, eps_deg, dist, f_px, W, H):
    """project +Y (outboard) at the origin -- geometry the analyst KNOWS from
    which side of the vehicle the wheel is on; not from the answer."""
    from r51_geom import camera_rays
    phi = np.radians(phi_deg); eps = np.radians(eps_deg)
    v = np.array([np.sin(phi)*np.cos(eps), np.cos(phi), np.sin(phi)*np.sin(eps)])
    C = v*dist
    fwd = -v; up = np.array([0., 0., 1.])
    right = np.cross(fwd, up); right /= np.linalg.norm(right)
    tup = np.cross(right, fwd)
    def proj(P):
        rel = P - C
        z = np.dot(rel, fwd)
        return (W/2 + f_px*np.dot(rel, right)/z, H/2 - f_px*np.dot(rel, tup)/z)
    p0 = proj(np.array([0., 0., 0.])); p1 = proj(np.array([0., 0.05, 0.]))
    return (p1[0]-p0[0], p1[1]-p0[1])


if __name__ == '__main__':
    H_TRUE = [0.005, 0.015, 0.0105, 0.040, 0.060]
    PHIS   = [3, 8, 20, 35, 50, 65]
    dist, f_px, W, H = 4.0, 1800.0, 520, 520
    rows = []
    print('%7s %6s %8s %8s %8s %8s %8s %8s %8s %8s' %
          ('h_true', 'phi', 'ratio', 'phi_hat', 'px/m', 'D_px',
           'h_cap', 'err_cap', 'h_emb', 'err_emb'))
    for ht in H_TRUE:
        for phi in PHIS:
            dy = ht - SC.true_proud(0.0)
            prims = SC.scene(cap_dy=dy)
            img, m, t = SC.render(prims, phi, eps_deg=-12.0, dist=dist,
                                  f_px=f_px, W=W, H=H, bg=0.16, seed=int(ht*1e4)+phi,
                                  noise=0.010, blur=0.9)
            hint = outboard_hint_from_geom(phi, -12.0, dist, f_px, W, H)
            r = run_pipeline(img, hint)
            if r is None:
                print('%7.1f %6.1f   PIPELINE FAILED' % (ht*1000, phi)); continue
            rc, re = r['cap_res'], r['emb_res']
            sc = IN.sigma_h(rc)
            print('%7.1f %6.1f %8.4f %8.2f %8.1f %8.2f %8.1f %+8.1f %8.1f %+8.1f'
                  % (ht*1000, phi, rc['ratio'], rc['phi_deg'], rc['s'],
                     rc['delta_px'], rc['h']*1000, (rc['h']-ht)*1000,
                     re['h']*1000 if re else np.nan,
                     (re['h']-ht)*1000 if re else np.nan))
            rows.append((ht, phi, rc, re, sc))
    np.save('r51_calib_rows.npy', np.array([(a, b, c['h'], c['phi_deg'], c['s'],
             c['delta_px'], (d['h'] if d else np.nan), e)
            for (a, b, c, d, e) in rows]))
