"""REV51 A2 -- THE INSTRUMENT.  Same code path for synthetic and photograph.

Estimator (first principles, no fitted constants):
  cosphi = b/a of the CREAM-RING outer ellipse   (a true circle in the wheel plane)
  s      = a_cream / R_CREAM      px per metre, derived ON the frame
  Delta  = (C_feature - C_cream) . that   px, that = outboard unit vector
  dy     = Delta / (sin(phi) * s)          metres of AXIAL offset
  h_apex = dy + DOME_H + (Y_CREAM - Y_FLANGE)          [cap-silhouette route]
  h_apex = dy + (Y_CREAM - Y_FLANGE) - EMB_PROUD       [emblem route]
"""
import numpy as np
from r51_geom import fit_ellipse, ellipse_resid

R_CREAM   = 0.2198        # flange OD/2 = t1_core RIM_R -- radius of the visible
                          # cream outer boundary (tyre bead sits on it)
Y_CREAM   = 0.0620        # axial plane of that boundary (barrel prof 0.0600 at
                          # r=0.1905*S ... 0.0640 at 0.1885*S)  +/- 0.0020
Y_FLANGE  = 0.0640        # rim() barrel prof max y  -- THE DATUM
DOME_H    = 0.0705        # cap apex 0.0745 - cap max-r plane 0.0040
EMB_PROUD = 0.0060        # CAP_EMBLEM_PLANE 0.0805 - apex 0.0745
R_TYRE    = 0.3325


def bilinear(img, x, y):
    h, w = img.shape[:2]
    x = np.clip(x, 0, w - 1.001); y = np.clip(y, 0, h - 1.001)
    x0 = np.floor(x).astype(int); y0 = np.floor(y).astype(int)
    fx = x - x0; fy = y - y0
    return (img[y0, x0]*(1-fx)*(1-fy) + img[y0, x0+1]*fx*(1-fy)
            + img[y0+1, x0]*(1-fx)*fy + img[y0+1, x0+1]*fx*fy)


def outer_edge(score, cx, cy, rmin, rmax, angles, thresh, step=0.25):
    """last inside->outside crossing of `thresh` along each ray; subpixel."""
    rs = np.arange(rmin, rmax, step)
    pts = []
    for a in angles:
        x = cx + rs*np.cos(a); y = cy + rs*np.sin(a)
        v = bilinear(score, x, y)
        inside = v > thresh
        idx = np.where(inside[:-1] & ~inside[1:])[0]
        if len(idx) == 0:
            continue
        k = idx[-1]
        v0, v1 = v[k], v[k+1]
        f = (v0 - thresh)/(v0 - v1) if v0 != v1 else 0.5
        r = rs[k] + f*step
        pts.append((cx + r*np.cos(a), cy + r*np.sin(a), a, r))
    return np.array(pts) if pts else np.zeros((0, 4))


def fit_boundary(score, c0, rmin, rmax, angles, thresh, iters=4):
    cx, cy = c0
    fit = None; pts = None
    for _ in range(iters):
        pts = outer_edge(score, cx, cy, rmin, rmax, angles, thresh)
        if len(pts) < 12:
            return None, pts
        f = fit_ellipse(pts[:, 0], pts[:, 1])
        if f is None:
            return None, pts
        fit = f; cx, cy = f['cx'], f['cy']
    fit['rms'] = ellipse_resid(fit, pts[:, 0], pts[:, 1])
    fit['n'] = len(pts)
    return fit, pts


def outboard_unit(fit, hint):
    """unit vector along the ellipse MINOR axis, signed to agree with `hint`
    (a rough (dx,dy) pointing outboard in image coords)."""
    th = fit['theta']                      # major-axis angle
    t = np.array([-np.sin(th), np.cos(th)])   # minor axis
    if np.dot(t, np.asarray(hint, float)) < 0:
        t = -t
    return t


def measure(cream_fit, feat_fit, outboard_hint, route='cap',
            feat_centre=None):
    """returns dict with phi, s, delta_px, dy, h"""
    a, b = cream_fit['a'], cream_fit['b']
    ratio = b/a
    phi = np.arccos(np.clip(ratio, -1, 1))
    s = a / R_CREAM
    t = outboard_unit(cream_fit, outboard_hint)
    if feat_centre is None:
        feat_centre = (feat_fit['cx'], feat_fit['cy'])
    d = np.array([feat_centre[0]-cream_fit['cx'], feat_centre[1]-cream_fit['cy']])
    delta_px = float(np.dot(d, t))
    perp_px = float(np.dot(d, np.array([np.cos(cream_fit['theta']),
                                        np.sin(cream_fit['theta'])])))
    sp = np.sin(phi)
    dy = delta_px/(sp*s) if sp > 1e-6 else np.nan
    if route == 'cap':
        h = dy + DOME_H + (Y_CREAM - Y_FLANGE)
    else:
        h = dy + (Y_CREAM - Y_FLANGE) - EMB_PROUD
    return dict(ratio=ratio, phi_deg=float(np.degrees(phi)), s=float(s),
                delta_px=delta_px, perp_px=perp_px, dy=float(dy), h=float(h))


def sigma_h(res, sig_centre_px=0.5, sig_ratio=0.010, sig_a_frac=0.005):
    """1-sigma on h from: centre localisation, axis-ratio, scale."""
    phi = np.radians(res['phi_deg']); sp = np.sin(phi); s = res['s']
    if sp < 1e-6:
        return np.inf
    t1 = (np.sqrt(2)*sig_centre_px)/(sp*s)                 # two centres
    dphi = sig_ratio/max(sp, 1e-6)                          # d phi from d(b/a)
    t2 = abs(res['dy'])*abs(np.cos(phi)/max(sp, 1e-6))*dphi
    t3 = abs(res['dy'])*sig_a_frac
    return float(np.sqrt(t1*t1 + t2*t2 + t3*t3))
