"""Precomputed q(dome_depth, phi) for the authored cap SHAPE, seated."""
import numpy as np, os, r51_scene as SC, r51_fwd as F

DOMES = np.concatenate([np.linspace(0.002, 0.030, 12),
                        np.linspace(0.034, 0.150, 18)])
PHIS  = np.arange(4.0, 84.0, 4.0)
CACHE = 'r51_qtab.npz'

def build(shape_fn=None, tag='auth'):
    fn = shape_fn or (lambda d: SC.cap_profile_seated(d))
    Q = np.zeros((len(DOMES), len(PHIS)))
    for i, d in enumerate(DOMES):
        for j, p in enumerate(PHIS):
            Q[i, j] = F.q_model(d, p, fn)[0]
    return Q

def get(tag='auth'):
    if os.path.exists(CACHE):
        z = np.load(CACHE)
        if tag in z: return z[tag]
    return None

def q_of(Q, dome, phi):
    from scipy.interpolate import RegularGridInterpolator
    g = RegularGridInterpolator((DOMES, PHIS), Q, bounds_error=False,
                               fill_value=None)
    return g(np.array([[dome, phi]]))[0]

def invert(Q, q_obs, phi):
    """monotone in dome at fixed phi"""
    j = np.interp(phi, PHIS, np.arange(len(PHIS)))
    j0 = int(np.clip(np.floor(j), 0, len(PHIS)-2)); w = j - j0
    col = Q[:, j0]*(1-w) + Q[:, j0+1]*w
    if not np.all(np.diff(col) > -1e-9):
        col = np.maximum.accumulate(col)
    if q_obs <= col[0]:  return DOMES[0] if q_obs > col[0]-1e-9 else np.nan
    if q_obs >= col[-1]: return np.nan
    return float(np.interp(q_obs, col, DOMES))

if __name__ == '__main__':
    import sys
    d = {}
    d['auth'] = build()
    # SHAPE VARIANTS -- how much of the error bar is shape, not measurement?
    def sph(dd):
        """spherical cap of the same lip radius and depth"""
        R = SC.LIP_R; y0 = SC.disc_y_at(R)
        ys = np.linspace(0, dd, 24)
        rr = R*np.sqrt(np.maximum(1-(ys/dd)**2, 0))**0.5*0 + R*np.sqrt(
            np.maximum(1 - (ys/dd)**2, 0))
        prof = [(y0+y, r) for y, r in zip(ys, rr)]
        prof = prof[::-1] + [(y0-0.004, R), (y0-0.004, 0.0)]
        return prof
    def con(dd):
        """straight cone -- the flattest plausible shape"""
        R = SC.LIP_R; y0 = SC.disc_y_at(R)
        prof = [(y0+dd, 0.0), (y0, R), (y0-0.004, R), (y0-0.004, 0.0)]
        return prof
    def par(dd):
        """paraboloid -- fuller than the authored ogive"""
        R = SC.LIP_R; y0 = SC.disc_y_at(R)
        rr = np.linspace(0, R, 24)
        return ([(y0+dd*(1-(r/R)**2), r) for r in rr][::-1]
                + [(y0-0.004, R), (y0-0.004, 0.0)])
    d['sph'] = build(sph); d['con'] = build(con); d['par'] = build(par)
    np.savez(CACHE, DOMES=DOMES, PHIS=PHIS, **d)
    print('built', {k: v.shape for k, v in d.items()})
    for tag in ('auth','sph','par','con'):
        print(tag, ' '.join('%.4f' % q_of(d[tag], h+0.0123, 55)
                            for h in (0.005,0.010,0.022,0.035,0.058)))
