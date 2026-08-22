"""REV51 A2 -- one pipeline, used on synthetics AND photographs."""
import numpy as np
import r51_inst as IN
from r51_geom import fit_ellipse

def analyze(cream_sc, cap_sc, seed_face, seed_cap, angles=None,
            rho=(0.80, 1.22), rho_cap=(0.78, 1.25)):
    if angles is None:
        angles = np.linspace(-np.pi, np.pi, 720, endpoint=False)
    f0 = IN.init_from_mask(seed_face)
    if f0 is None: return None
    cf, cp = IN.refine(cream_sc, f0, angles, *rho)
    if cf is None: return None
    k0 = IN.init_from_mask(seed_cap)
    if k0 is None: return None
    kf, kp = IN.refine(cap_sc, k0, angles, *rho_cap)
    if kf is None: return None
    return dict(cream=cf, cap=kf, cpts=cp, kpts=kp,
                q=kf['ratio'] - cf['ratio'],
                rad_ratio=kf['a']/cf['a'])
