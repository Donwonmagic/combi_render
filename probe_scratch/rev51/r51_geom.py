"""REV51 A2 -- analytic wheel renderer + ellipse instrument.  NO BLENDER.

Ray-casts a perspective camera against surfaces of revolution about the Y axis
(the axle), exactly the primitive t1_detail.revolve() builds.  Each profile
segment (y0,r0)->(y1,r1) is a truncated cone; ray/cone is a quadratic.  Nearest
positive root over all segments of all objects gives exact occlusion.
"""
import numpy as np

# ---------------------------------------------------------------- primitives
class Cone:
    """truncated cone about +Y, from (y0,r0) to (y1,r1); mat = material id"""
    def __init__(self, y0, r0, y1, r1, mat):
        self.y0, self.r0, self.y1, self.r1, self.mat = y0, r0, y1, r1, mat

class Disc:
    """flat annulus in plane y=yp, ri<=r<=ro, normal +Y"""
    def __init__(self, yp, ri, ro, mat):
        self.yp, self.ri, self.ro, self.mat = yp, ri, ro, mat


def revolve_profile(prof, mat):
    """closed (y,r) loop -> list of Cone"""
    out = []
    n = len(prof)
    for i in range(n):
        y0, r0 = prof[i]
        y1, r1 = prof[(i + 1) % n]
        if y0 == y1 and r0 == r1:
            continue
        out.append(Cone(y0, r0, y1, r1, mat))
    return out


# ------------------------------------------------------------------- camera
def camera_rays(W, H, f, C, look, up=(0.0, 0.0, 1.0)):
    C = np.asarray(C, float)
    fwd = np.asarray(look, float) - C
    fwd /= np.linalg.norm(fwd)
    up = np.asarray(up, float)
    right = np.cross(fwd, up); right /= np.linalg.norm(right)
    true_up = np.cross(right, fwd)
    j, i = np.mgrid[0:H, 0:W]
    x = (i + 0.5) - W / 2.0
    y = (j + 0.5) - H / 2.0
    d = (fwd[None, None, :] * f
         + right[None, None, :] * x[..., None]
         - true_up[None, None, :] * y[..., None])
    d /= np.linalg.norm(d, axis=-1, keepdims=True)
    return C, d


# ------------------------------------------------------------------- caster
def cast(C, d, prims):
    """returns t (nearest hit, inf if none), mat id (-1 none), normal"""
    sh = d.shape[:-1]
    best_t = np.full(sh, np.inf)
    best_m = np.full(sh, -1, dtype=np.int32)
    best_n = np.zeros(d.shape)
    ox, oy, oz = C
    dx, dy, dz = d[..., 0], d[..., 1], d[..., 2]
    for p in prims:
        if isinstance(p, Disc):
            with np.errstate(divide='ignore', invalid='ignore'):
                t = (p.yp - oy) / dy
            px = ox + t * dx; pz = oz + t * dz
            r2 = px * px + pz * pz
            ok = (t > 1e-6) & np.isfinite(t) & (r2 >= p.ri**2) & (r2 <= p.ro**2)
            upd = ok & (t < best_t)
            best_t = np.where(upd, t, best_t)
            best_m = np.where(upd, p.mat, best_m)
            nrm = np.zeros(d.shape); nrm[..., 1] = 1.0
            best_n = np.where(upd[..., None], nrm, best_n)
            continue
        y0, r0, y1, r1 = p.y0, p.r0, p.y1, p.r1
        if y1 == y0:                       # flat ring -> Disc
            ri, ro = min(r0, r1), max(r0, r1)
            prims_disc = Disc(y0, ri, ro, p.mat)
            with np.errstate(divide='ignore', invalid='ignore'):
                t = (y0 - oy) / dy
            px = ox + t * dx; pz = oz + t * dz
            r2 = px * px + pz * pz
            ok = (t > 1e-6) & np.isfinite(t) & (r2 >= ri**2) & (r2 <= ro**2)
            upd = ok & (t < best_t)
            best_t = np.where(upd, t, best_t)
            best_m = np.where(upd, p.mat, best_m)
            nrm = np.zeros(d.shape); nrm[..., 1] = 1.0
            best_n = np.where(upd[..., None], nrm, best_n)
            continue
        k = (r1 - r0) / (y1 - y0)          # r(y) = r0 + k*(y-y0)
        b0 = r0 - k * y0                   # r(y) = k*y + b0
        # (ox+t dx)^2 + (oz+t dz)^2 = (k(oy+t dy)+b0)^2
        A = dx*dx + dz*dz - (k*dy)**2
        Bq = 2*(ox*dx + oz*dz) - 2*k*dy*(k*oy + b0)
        Cq = ox*ox + oz*oz - (k*oy + b0)**2
        ylo, yhi = min(y0, y1), max(y0, y1)
        disc = Bq*Bq - 4*A*Cq
        with np.errstate(invalid='ignore', divide='ignore'):
            sq = np.sqrt(np.maximum(disc, 0.0))
            for sgn in (-1.0, 1.0):
                t = np.where(np.abs(A) > 1e-14, (-Bq + sgn*sq) / (2*A),
                             np.where(np.abs(Bq) > 1e-14, -Cq/Bq, np.inf))
                yy = oy + t*dy
                rr = k*yy + b0
                ok = ((disc >= 0) & (t > 1e-6) & np.isfinite(t)
                      & (yy >= ylo) & (yy <= yhi) & (rr >= 0))
                upd = ok & (t < best_t)
                if not np.any(upd):
                    continue
                px = ox + t*dx; pz = oz + t*dz
                rho = np.sqrt(np.maximum(px*px + pz*pz, 1e-18))
                # surface normal of cone: (cos,  -k, sin)/sqrt(1+k^2) w/ sign
                nx = px/rho; nz = pz/rho
                nrm = np.stack([nx, -k*np.ones_like(nx), nz], axis=-1)
                nrm = nrm / np.linalg.norm(nrm, axis=-1, keepdims=True)
                best_t = np.where(upd, t, best_t)
                best_m = np.where(upd, p.mat, best_m)
                best_n = np.where(upd[..., None], nrm, best_n)
    return best_t, best_m, best_n


# ------------------------------------------------------- ellipse (Fitzgibbon)
def fit_ellipse(x, y):
    """Halir & Flusser (1998) numerically-stable direct ellipse fit."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    mx, my = x.mean(), y.mean()
    s = max(0.5*(x.std() + y.std()), 1e-9)
    u = (x - mx)/s; v = (y - my)/s
    D1 = np.stack([u*u, u*v, v*v], 1)
    D2 = np.stack([u, v, np.ones_like(u)], 1)
    S1 = D1.T @ D1; S2 = D1.T @ D2; S3 = D2.T @ D2
    try:
        T = -np.linalg.solve(S3, S2.T)
    except np.linalg.LinAlgError:
        return None
    M = S1 + S2 @ T
    Cinv = np.array([[0.0, 0.0, 0.5], [0.0, -1.0, 0.0], [0.5, 0.0, 0.0]])
    M = Cinv @ M
    w, V = np.linalg.eig(M)
    cond = 4*V[0]*V[2] - V[1]**2
    k = np.where(np.isreal(w) & (cond > 0))[0]
    if len(k) == 0:
        return None
    a1 = np.real(V[:, k[0]])
    a2 = T @ a1
    A, B, Cc, Dd, E, F = np.concatenate([a1, a2])
    den = B*B - 4*A*Cc
    if abs(den) < 1e-18:
        return None
    x0 = (2*Cc*Dd - B*E)/den
    y0 = (2*A*E - B*Dd)/den
    Fp = F + 0.5*(Dd*x0 + E*y0)          # conic value after translating to centre
    Q = np.array([[A, B/2.0], [B/2.0, Cc]])
    lam, W = np.linalg.eigh(Q)
    if np.any(lam == 0) or np.any(-Fp/lam <= 0):
        return None
    L = np.sqrt(-Fp/lam)                  # semi-axis along eigenvector W[:,i]
    i_major = int(np.argmax(L))
    aa = float(L[i_major]); bb = float(L[1 - i_major])
    th = float(np.arctan2(W[1, i_major], W[0, i_major]))
    return dict(cx=x0*s + mx, cy=y0*s + my, a=aa*s, b=bb*s, theta=th)


def ellipse_resid(fit, x, y):
    """rms radial residual in px"""
    ct, st = np.cos(-fit['theta']), np.sin(-fit['theta'])
    dx = np.asarray(x)-fit['cx']; dy = np.asarray(y)-fit['cy']
    u = ct*dx - st*dy; v = st*dx + ct*dy
    rr = np.sqrt((u/fit['a'])**2 + (v/fit['b'])**2)
    # radial distance error, scaled by local radius
    loc = np.sqrt(u*u+v*v)
    return float(np.sqrt(np.mean((loc*(1-1/np.maximum(rr, 1e-9)))**2)))
