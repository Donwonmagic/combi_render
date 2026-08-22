"""REV51 A2 -- one pipeline, used on synthetics AND photographs."""
import numpy as np
import r51_inst as IN
from r51_geom import fit_ellipse

def analyze(cream_sc, cap_sc, seed_face, seed_cap, angles=None,
            rho=(0.80, 1.22), rho_cap=(0.78, 1.25), clip_cap='both'):
    if angles is None:
        angles = np.linspace(-np.pi, np.pi, 720, endpoint=False)
    f0 = IN.init_from_mask(seed_face)
    if f0 is None: return None
    cf, cp = IN.refine(cream_sc, f0, angles, *rho)
    if cf is None: return None
    k0 = IN.init_from_mask(seed_cap)
    if k0 is None: return None
    kf, kp = IN.refine(cap_sc, k0, angles, *rho_cap, clip=clip_cap)
    if kf is None: return None
    sc_ = IN.bootstrap_ratio(cream_sc, cf, angles, *rho)
    sk_ = IN.bootstrap_ratio(cap_sc, kf, angles, *rho_cap, clip=clip_cap)
    return dict(cream=cf, cap=kf, cpts=cp, kpts=kp,
                q=kf['ratio'] - cf['ratio'],
                sig_q=float(np.hypot(sc_, sk_)),
                sig_rc=sc_, sig_rk=sk_,
                rad_ratio=kf['a']/cf['a'])


def analyze2(cream_sc, cap_sc, f0, k0, angles=None, rho=(0.80, 1.22),
             rho_cap=(0.78, 1.25), clip_cap='both'):
    """same as analyze() but takes explicit seed ELLIPSES."""
    if angles is None:
        angles = np.linspace(-np.pi, np.pi, 720, endpoint=False)
    cf, cp = IN.refine(cream_sc, f0, angles, *rho)
    if cf is None: return None
    kf, kp = IN.refine(cap_sc, k0, angles, *rho_cap, clip=clip_cap)
    if kf is None: return None
    sc_ = IN.bootstrap_ratio(cream_sc, cf, angles, *rho)
    sk_ = IN.bootstrap_ratio(cap_sc, kf, angles, *rho_cap, clip=clip_cap)
    return dict(cream=cf, cap=kf, cpts=cp, kpts=kp,
                q=kf['ratio'] - cf['ratio'],
                sig_q=float(np.hypot(sc_, sk_)), sig_rc=sc_, sig_rk=sk_,
                rad_ratio=kf['a']/cf['a'])


def analyze3(cream_sc, cap_sc, f0, angles=None, rho=(0.84, 1.18),
             rho_cap=(0.72, 1.30), clip_cap='both', cap_frac=0.63):
    """fit the CREAM ring first, then seed the CAP from the fitted cream
    ellipse scaled by cap_frac.  Far more robust than an independent guess."""
    if angles is None:
        angles = np.linspace(-np.pi, np.pi, 720, endpoint=False)
    cf, cp = IN.refine(cream_sc, f0, angles, *rho)
    if cf is None: return None
    k0 = dict(cf); k0['a'] = cf['a']*cap_frac; k0['b'] = cf['b']*cap_frac
    kf, kp = IN.refine(cap_sc, k0, angles, *rho_cap, clip=clip_cap)
    if kf is None: return None
    sc_ = IN.bootstrap_ratio(cream_sc, cf, angles, *rho)
    sk_ = IN.bootstrap_ratio(cap_sc, kf, angles, *rho_cap, clip=clip_cap)
    return dict(cream=cf, cap=kf, cpts=cp, kpts=kp,
                q=kf['ratio'] - cf['ratio'],
                sig_q=float(np.hypot(sc_, sk_)), sig_rc=sc_, sig_rk=sk_,
                rad_ratio=kf['a']/cf['a'])
