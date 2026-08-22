"""REV51 A2 -- FORWARD MODEL: orthographic silhouette of a surface of
revolution, sampled and fitted EXACTLY as the instrument samples and fits."""
import numpy as np
from r51_geom import fit_ellipse
import r51_inst as IN

def silhouette_ellipse(prof, phi, nang=360, npsi=721, nprof=200, iters=4):
    """prof = [(y,r)] closed loop.  Orthographic tilt phi about the image u
    axis.  Returns the ellipse the instrument would fit to its outline."""
    P = np.asarray(prof, float)
    # densify the profile
    t = np.linspace(0, len(P), nprof, endpoint=False)
    i0 = np.floor(t).astype(int) % len(P); f = t - np.floor(t)
    yy = P[i0, 0]*(1-f) + P[(i0+1) % len(P), 0]*f
    rr = P[i0, 1]*(1-f) + P[(i0+1) % len(P), 1]*f
    psi = np.linspace(0, 2*np.pi, npsi)
    cp, sp = np.cos(phi), np.sin(phi)
    u = (rr[:, None]*np.cos(psi)[None, :]).ravel()
    v = (rr[:, None]*np.sin(psi)[None, :]*cp + (yy*sp)[:, None]).ravel()
    cx, cy = 0.0, float(v.mean())
    edges = np.linspace(-np.pi, np.pi, nang+1)
    for _ in range(iters):
        du = u - cx; dv = v - cy
        ang = np.arctan2(dv, du); rad = np.hypot(du, dv)
        k = np.clip(np.digitize(ang, edges) - 1, 0, nang-1)
        order = np.lexsort((rad, k))
        ks = k[order]; rsort = rad[order]
        last = np.nonzero(np.diff(ks) > 0)[0]
        last = np.concatenate([last, [len(ks)-1]])
        best = np.zeros(nang)
        best[ks[last]] = rsort[last]
        ok = best > 0
        ac = 0.5*(edges[:-1] + edges[1:])[ok]
        px = cx + best[ok]*np.cos(ac); py = cy + best[ok]*np.sin(ac)
        f2 = fit_ellipse(px, py)
        if f2 is None:
            return None
        cx, cy = f2['cx'], f2['cy']
    f2['ratio'] = f2['b']/f2['a']
    return f2

def q_model(dome_depth, phi_deg, cap_profile_fn):
    """axis_ratio(cap silhouette) - cos(phi)"""
    phi = np.radians(phi_deg)
    f = silhouette_ellipse(cap_profile_fn(dome_depth), phi)
    if f is None:
        return np.nan, None
    return f['ratio'] - np.cos(phi), f

def invert_q(q_obs, phi_deg, cap_profile_fn, lo=0.002, hi=0.140):
    """monotone solve for dome depth"""
    import scipy.optimize as so
    def g(d):
        return q_model(d, phi_deg, cap_profile_fn)[0] - q_obs
    a, b = lo, hi
    ga, gb = g(a), g(b)
    if not np.isfinite(ga) or not np.isfinite(gb) or ga*gb > 0:
        return np.nan
    return float(so.brentq(g, a, b, xtol=1e-5))
