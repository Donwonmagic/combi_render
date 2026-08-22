"""REV51 A2 -- THE INSTRUMENT (v2).

Two estimators, both fed by the same sub-pixel elliptical-ray edge finder:

  E1  AXIS-RATIO DIFFERENCE (primary).  A flat circle on the wheel plane
      projects with axis ratio cos(phi).  A dome standing h proud silhouettes
      on its own girth, so its outline is pushed out along the MINOR axis and
      reads rounder.  q = ratio(cap) - ratio(cream ring) is then a monotone
      function of h that needs no px/m, no centre and no obliquity estimate.

  E2  CENTRE OFFSET (cross-check).  The emblem sits on the crown; its image
      offset from the cream-ring ellipse centre along the minor axis is
      (y_emblem - y_cream)*sin(phi)*(px/m).

  R   RADIUS RATIO (scale-free, no depth model at all):  a_cap / a_cream.
"""
import numpy as np

R_CREAM   = 0.2198        # t1_core RIM_R -- flange OD/2
Y_FLANGE  = 0.0640        # rim() barrel prof max y  -- THE DATUM
EMB_PROUD = 0.0060        # CAP_EMBLEM_PLANE 0.0805 - apex 0.0745
LIP_R     = 0.1370        # hubcap() max r
R_TYRE    = 0.3325


def bilinear(img, x, y):
    h, w = img.shape[:2]
    x = np.clip(x, 0, w - 1.001); y = np.clip(y, 0, h - 1.001)
    x0 = np.floor(x).astype(int); y0 = np.floor(y).astype(int)
    fx = x - x0; fy = y - y0
    return (img[y0, x0]*(1-fx)*(1-fy) + img[y0, x0+1]*fx*(1-fy)
            + img[y0+1, x0]*(1-fx)*fy + img[y0+1, x0+1]*fx*fy)


def ell_radius(fit, ang):
    """radius of the ellipse at image-plane angle ang"""
    c = np.cos(ang - fit['theta']); s = np.sin(ang - fit['theta'])
    return 1.0/np.sqrt((c/fit['a'])**2 + (s/fit['b'])**2)


def ell_point(fit, ang):
    r = ell_radius(fit, ang)
    return fit['cx'] + r*np.cos(ang), fit['cy'] + r*np.sin(ang)


def init_from_mask(mask):
    """second moments of a filled ellipse -> ellipse estimate (blind)"""
    ys, xs = np.nonzero(mask)
    if len(xs) < 60:
        return None
    cx, cy = xs.mean(), ys.mean()
    cov = np.cov(np.stack([xs - cx, ys - cy]))
    lam, V = np.linalg.eigh(cov)
    lam = np.maximum(lam, 1e-9)
    L = 2.0*np.sqrt(lam)
    i = int(np.argmax(L))
    return dict(cx=cx, cy=cy, a=float(L[i]), b=float(L[1-i]),
                theta=float(np.arctan2(V[1, i], V[0, i])))


def edge_points(score, fit, angles, rho_lo, rho_hi, step=0.2, min_step=0.05):
    """OUTERMOST half-level step edge on each elliptical ray.  Vectorised.

    Sampling is normalised to the current ellipse: each ray runs from
    rho_lo*R(a) to rho_hi*R(a), so the window follows the foreshortening
    instead of fighting it.  The level is set PER RAY, half way between the
    inner plateau and the outer floor -- a fixed threshold is defeated by
    shading, a half-level is not.
    """
    angles = np.asarray(angles, float)
    R = ell_radius(fit, angles)
    nsamp = max(int(np.ceil((rho_hi - rho_lo)*float(np.median(R))/step)), 24)
    frac = np.linspace(rho_lo, rho_hi, nsamp)[None, :]
    rs = R[:, None]*frac
    xs = fit['cx'] + rs*np.cos(angles)[:, None]
    ys = fit['cy'] + rs*np.sin(angles)[:, None]
    v = bilinear(score, xs, ys)
    n = nsamp
    hi = np.percentile(v[:, :max(int(0.35*n), 3)], 80, axis=1)
    lo = np.percentile(v[:, int(0.75*n):], 20, axis=1)
    contrast = hi - lo
    lvl = 0.5*(hi + lo)
    inside = v > lvl[:, None]
    cross = inside[:, :-1] & ~inside[:, 1:]
    idx = np.where(cross.any(axis=1),
                   n - 2 - np.argmax(cross[:, ::-1], axis=1), -1)
    good = (idx >= 0) & (contrast >= min_step)
    if not np.any(good):
        return np.zeros((0, 5))
    gi = np.nonzero(good)[0]; k = idx[gi]
    v0 = v[gi, k]; v1 = v[gi, k+1]; lv = lvl[gi]
    f = np.where(v0 != v1, (v0 - lv)/(v0 - v1 + 1e-12), 0.5)
    r = rs[gi, k] + f*(rs[gi, k+1] - rs[gi, k])
    a = angles[gi]
    return np.stack([fit['cx'] + r*np.cos(a), fit['cy'] + r*np.sin(a),
                     a, r, contrast[gi]], axis=1)


def _radial_res(fit, x, y):
    ct, st = np.cos(-fit['theta']), np.sin(-fit['theta'])
    dx = np.asarray(x) - fit['cx']; dy = np.asarray(y) - fit['cy']
    u = ct*dx - st*dy; v = st*dx + ct*dy
    rr = np.sqrt((u/fit['a'])**2 + (v/fit['b'])**2)
    loc = np.sqrt(u*u + v*v)
    return loc*(1 - 1/np.maximum(rr, 1e-9))


def refine(score, fit0, angles, rho_lo=0.80, rho_hi=1.22, iters=6, trim=2.5,
           clip='both'):
    from r51_geom import fit_ellipse
    fit = dict(fit0); pts = None
    for it in range(iters):
        pts = edge_points(score, fit, angles, rho_lo, rho_hi)
        if len(pts) < 15:
            return None, pts
        if it >= 2:
            res = _radial_res(fit, pts[:, 0], pts[:, 1])
            sd = max(np.std(res), 1e-6)
            if clip == 'low':          # reject only INWARD outliers (vent notches)
                keep = res > -trim*sd
            elif clip == 'high':
                keep = res < trim*sd
            else:
                keep = np.abs(res) < trim*sd
            if keep.sum() >= 15:
                pts = pts[keep]
        f = fit_ellipse(pts[:, 0], pts[:, 1])
        if f is None:
            return None, pts
        fit = f
    res = _radial_res(fit, pts[:, 0], pts[:, 1])
    fit['rms'] = float(np.sqrt(np.mean(res**2)))
    fit['n'] = int(len(pts))
    fit['ratio'] = fit['b']/fit['a']
    fit['sig_ratio'] = fit['ratio']*fit['rms']/max(fit['a'], 1)/np.sqrt(max(fit['n'], 1))*np.sqrt(2)
    return fit, pts


def bootstrap_ratio(score, fit, angles, rho_lo, rho_hi, nboot=40, frac=0.6,
                    clip='both', seed=0):
    """1-sigma on the axis ratio, from resampling the boundary rays."""
    from r51_geom import fit_ellipse
    pts = edge_points(score, fit, angles, rho_lo, rho_hi)
    if len(pts) < 20:
        return np.nan
    res = _radial_res(fit, pts[:, 0], pts[:, 1])
    sd = max(np.std(res), 1e-6)
    keep = (res > -2.5*sd) if clip == 'low' else (np.abs(res) < 2.5*sd)
    pts = pts[keep]
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(nboot):
        i = rng.choice(len(pts), int(frac*len(pts)), replace=False)
        f = fit_ellipse(pts[i, 0], pts[i, 1])
        if f is not None:
            out.append(f['b']/f['a'])
    return float(np.std(out)*np.sqrt(frac)) if len(out) > 5 else np.nan
