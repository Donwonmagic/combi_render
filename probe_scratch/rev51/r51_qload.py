"""Load the precomputed q(dome, phi) tables; the grid comes from the file."""
import numpy as np, os
_z = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'r51_qtab.npz'))
DOMES = _z['DOMES']; PHIS = _z['PHIS']
TAB = {k: _z[k] for k in ('auth', 'sph', 'con', 'par') if k in _z}

def q_of(tag, dome, phi):
    Q = TAB[tag]
    i = np.interp(dome, DOMES, np.arange(len(DOMES)))
    j = np.interp(phi, PHIS, np.arange(len(PHIS)))
    i0 = int(np.clip(np.floor(i), 0, len(DOMES)-2)); u = i-i0
    j0 = int(np.clip(np.floor(j), 0, len(PHIS)-2)); v = j-j0
    return float(Q[i0, j0]*(1-u)*(1-v) + Q[i0+1, j0]*u*(1-v)
                 + Q[i0, j0+1]*(1-u)*v + Q[i0+1, j0+1]*u*v)

def invert(tag, q_obs, phi):
    Q = TAB[tag]
    j = np.interp(phi, PHIS, np.arange(len(PHIS)))
    j0 = int(np.clip(np.floor(j), 0, len(PHIS)-2)); v = j-j0
    col = Q[:, j0]*(1-v) + Q[:, j0+1]*v
    col = np.maximum.accumulate(col)
    if q_obs <= col[0]:
        return 0.0 if q_obs > col[0]-0.05 else np.nan
    if q_obs >= col[-1]:
        return np.nan
    return float(np.interp(q_obs, col, DOMES))

def h_from_q(q_obs, phi, tag='auth'):
    d = invert(tag, q_obs, phi)
    return (d - 0.0123) if np.isfinite(d) else np.nan
