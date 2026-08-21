"""FLAT-NOSE FEASIBILITY, done algebraically instead of by blind optimisation.

If the nose is a plane, plane->image is a homography H.  Every homography that
carries the ROUNDEL circle onto the MEASURED roundel conic is
        H = A^-1 . M . S
where S scales the model roundel to the unit circle, M is any element of
PO(2,1) (the 3-parameter group of projective maps that preserve the unit
circle) and A rectifies the measured roundel conic to diag(1,1,-1).
So the search is only FOUR numbers -- three for M, one for the unknown lamp
aperture radius -- and it is exhaustive rather than hopeful.

The test: with the roundel matched EXACTLY by construction, how close can the
lamp circle be brought to the measured lamp conic?  That residual is the
flat-nose hypothesis's best case over ALL camera poses and ALL focal lengths.

A CONTROL is run alongside on the SHIPPED RENDER out/r49s_hero34f.png, where
the nose really is flat by construction: the same procedure there must give a
small residual, or the instrument -- not the bus -- is what is being measured.
"""
import numpy as np, math
from scipy.optimize import least_squares
from scipy import ndimage
from PIL import Image


def fit_conic(px, py):
    """algebraic ellipse fit -> (cx,cy,semimaj,semimin,ang) and the 3x3 conic"""
    mx, my = px.mean(), py.mean()
    x, y = px - mx, py - my
    D = np.stack([x * x, x * y, y * y, x, y, np.ones_like(x)], 1)
    _, _, V = np.linalg.svd(D, full_matrices=False)
    a, b, c, d, e, f = V[-1]
    M = np.array([[a, b / 2], [b / 2, c]])
    cen = np.linalg.solve(2 * M, [-d, -e])
    k = a * cen[0] ** 2 + b * cen[0] * cen[1] + c * cen[1] ** 2 + d * cen[0] + e * cen[1] + f
    ev, evec = np.linalg.eigh(M)
    ax = np.sqrt(np.maximum(-k / ev, 1e-12))
    o = np.argsort(ax)[::-1]
    ang = math.atan2(evec[1, o[0]], evec[0, o[0]]) % math.pi
    # conic in ABSOLUTE image coords
    cx, cy = cen[0] + mx, cen[1] + my
    A_, B_, C_ = a, b, c
    D_ = d - 2 * a * mx - b * my
    E_ = e - 2 * c * my - b * mx
    F_ = f - d * mx - e * my + a * mx * mx + b * mx * my + c * my * my
    Cm = np.array([[A_, B_ / 2, D_ / 2], [B_ / 2, C_, E_ / 2], [D_ / 2, E_ / 2, F_]])
    return np.array([cx, cy, ax[o[0]], ax[o[1]], ang]), Cm


def blob_conic(img, box, chan, thr, sense):
    x0, y0, x1, y1 = box
    sub = chan[y0:y1, x0:x1]
    m = (sub < thr) if sense == 'lt' else (sub > thr)
    lab, _ = ndimage.label(m)
    sy, sx = (y1 - y0) // 2, (x1 - x0) // 2
    if not m[sy, sx]:                       # centre is in a bright gap: reseed
        ys_, xs_ = np.nonzero(m)
        k = ((ys_ - sy) ** 2 + (xs_ - sx) ** 2).argmin()
        sy, sx = ys_[k], xs_[k]
    i = lab[sy, sx]
    assert i != 0, "seed landed on background"
    bl = ndimage.binary_fill_holes(lab == i)
    assert not (bl[0].any() or bl[-1].any() or bl[:, 0].any() or bl[:, -1].any()), \
        "blob touches the window edge -- the window is part of the measurement"
    ys, xs = np.nonzero(bl)
    er = ndimage.binary_erosion(bl)
    by, bx = np.nonzero(bl & ~er)
    p, C = fit_conic(bx.astype(float) + x0, by.astype(float) + y0)
    return p, C, (xs.max() - xs.min() + 1, ys.max() - ys.min() + 1), bl.sum()


def rectifier(C):
    """A with A^-T C A^-1 ~ diag(1,1,-1); returns A_inv (circle frame -> image)"""
    C = C / np.abs(C).max()
    ev, U = np.linalg.eigh(C)
    if np.sum(ev > 0) == 1:                      # flip overall sign
        C = -C
        ev, U = np.linalg.eigh(C)
    o = np.concatenate([np.where(ev > 0)[0], np.where(ev < 0)[0]])
    ev, U = ev[o], U[:, o]
    Ainv = U @ np.diag(1.0 / np.sqrt(np.abs(ev)))
    return Ainv                                   # x_img = Ainv @ x_circleframe


def po21(th1, t, th2):
    def R(a):
        return np.array([[math.cos(a), -math.sin(a), 0],
                         [math.sin(a), math.cos(a), 0], [0, 0, 1.]])
    B = np.array([[math.cosh(t), 0, math.sinh(t)], [0, 1., 0],
                  [math.sinh(t), 0, math.cosh(t)]])
    return R(th1) @ B @ R(th2)


def ellipse_pts(p, n=360):
    cx, cy, A, B, an = p
    t = np.linspace(0, 2 * math.pi, n, endpoint=False)
    ca, sa = math.cos(an), math.sin(an)
    x = cx + A * np.cos(t) * ca - B * np.sin(t) * sa
    y = cy + A * np.cos(t) * sa + B * np.sin(t) * ca
    return np.stack([x, y], 1)


def run(tag, imgpath, ro_box, ro_chan, ro_thr, ro_sense,
        hl_box, hl_chan, hl_thr, hl_sense, ro_R, dy, dz):
    im = np.asarray(Image.open(imgpath).convert('RGB')).astype(float)
    ch = {'L': im.mean(-1), 'GR': im[..., 1] - im[..., 0],
          'RG': im[..., 0] - im[..., 1]}
    pro, Cro, bbro, nro = blob_conic(im, ro_box, ch[ro_chan], ro_thr, ro_sense)
    phl, Chl, bbhl, nhl = blob_conic(im, hl_box, ch[hl_chan], hl_thr, hl_sense)
    print(f"\n===== {tag}  ({imgpath})")
    print("  roundel  bbox %dx%d = %.3f   conic semi %.2f/%.2f ratio %.3f ang %.1f  n=%d"
          % (bbro[0], bbro[1], bbro[0] / bbro[1], pro[2], pro[3], pro[3] / pro[2],
             math.degrees(pro[4]), nro))
    print("  lamp     bbox %dx%d = %.3f   conic semi %.2f/%.2f ratio %.3f ang %.1f  n=%d"
          % (bbhl[0], bbhl[1], bbhl[0] / bbhl[1], phl[2], phl[3], phl[3] / phl[2],
             math.degrees(phl[4]), nhl))

    Ainv = rectifier(Cro)
    S = np.diag([1.0 / ro_R, 1.0 / ro_R, 1.0])
    target = ellipse_pts(phl, 240)
    t = np.linspace(0, 2 * math.pi, 240, endpoint=False)

    def res(p):
        th1, tt, th2, r = p
        H = Ainv @ po21(th1, tt, th2) @ S
        P = np.stack([dy + r * np.cos(t), dz + r * np.sin(t), np.ones_like(t)], 1)
        Q = P @ H.T
        w = Q[:, 2]
        if np.any(np.abs(w) < 1e-9) or w.min() * w.max() <= 0:
            return np.full(5, 1e4)
        uv = Q[:, :2] / w[:, None]
        try:
            q, _ = fit_conic(uv[:, 0], uv[:, 1])
        except Exception:
            return np.full(5, 1e4)
        da = (q[4] - phl[4] + math.pi / 2) % math.pi - math.pi / 2
        return np.array([q[0] - phl[0], q[1] - phl[1], q[2] - phl[2],
                         q[3] - phl[3], da * phl[2]])

    best = None
    rng = np.random.default_rng(1)
    for _ in range(600):
        p0 = np.array([rng.uniform(0, math.pi), rng.uniform(-2.5, 2.5),
                       rng.uniform(0, math.pi), rng.uniform(0.5, 0.95) * ro_R])
        try:
            s = least_squares(res, p0, xtol=1e-14, ftol=1e-14, max_nfev=1200,
                              bounds=([-10, -6, -10, 0.25 * ro_R],
                                      [10, 6, 10, 1.10 * ro_R]))
        except Exception:
            continue
        c = float(np.sum(s.fun ** 2))
        if best is None or c < best[0]:
            best = (c, s.x, s.fun)
    c, x, fun = best
    print("  BEST FLAT-PLANE FIT over ALL cameras/f:  rms %.2f px on 5 obs" % math.sqrt(c / 5))
    print("     lamp radius solved %.4f (x roundel R) -> %.1f mm if roundel is 280 mm"
          % (x[3] / ro_R, x[3] / ro_R * 140.0))
    print("     residuals [cx cy semimaj semimin ang]:", np.round(fun, 2))
    return math.sqrt(c / 5)


# ---- ref_workshop.jpg : GREEN bus, GEOMETRY ONLY, lamp removed --------------
run("PHOTOGRAPH ref_workshop (GREEN, geometry)", 'ref_workshop.jpg',
    (270, 494, 346, 600), 'L', 170, 'lt',
    (372, 584, 466, 676), 'GR', 16, 'lt',
    0.140, 0.545, -0.16948)

# ---- CONTROL: the SHIPPED RENDER, where the nose IS flat by construction ----
# If the same procedure cannot fit a flat plane HERE, the instrument is broken
# and the photograph reading means nothing.
run("CONTROL: RENDER r49s_hero34f (nose flat by construction)",
    'out/r49s_hero34f.png',
    (426, 662, 494, 742), 'RG', 12, 'gt',        # red roundel ring on cream
    (551, 730, 604, 790), 'RG', 40, 'lt',        # bezel/lens: NOT red
    0.140, 0.545, -0.16948)
