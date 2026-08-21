"""THE STRONGEST POSSIBLE TEST OF THE FLAT-NOSE HYPOTHESIS.

If the nose is a PLANE and both circles lie in it, then plane->image is a
HOMOGRAPHY.  A homography is the PERMISSIVE LIMIT of "any camera pose and any
focal length" (every plane homography is realisable by some K,R,t), so if no
homography carries the two known coplanar circles onto the two MEASURED
conics, no camera can, and the flat nose is dead for every f -- the window
argument stops mattering.  If it fits well, the flat nose survives at some f
and the whole finding reduces to whether that f is credible.

Model plane coords (u,v) = (y, z) metres, from build.py:
  roundel  centre (0.000,  0.00000)  radius 0.1400
  near HL  centre (0.545, -0.16948)  radius r (free 0.055..0.135)

CEILING: assumes the roundel is a circle and the lamp aperture is a circle in
the SAME plane; assumes my conic fits are the outlines of those two circles;
assumes the 0.545 / 0.16948 offsets (which are the BUILD's, not measured on
the green bus).  r is free so absolute scale is not assumed.
"""
import numpy as np, math
from scipy.optimize import least_squares
from PIL import Image
from scipy import ndimage

im = np.asarray(Image.open('ref_workshop.jpg').convert('RGB')).astype(float)
GR = im[..., 1] - im[..., 0]
L = im.mean(-1)


def conic_of(box, chan, thr, sense):
    x0, y0, x1, y1 = box
    sub = chan[y0:y1, x0:x1]
    m = (sub < thr) if sense == 'lt' else (sub > thr)
    lab, _ = ndimage.label(m)
    i = lab[(y1 - y0) // 2, (x1 - x0) // 2]
    bl = ndimage.binary_fill_holes(lab == i)
    er = ndimage.binary_erosion(bl)
    by, bx = np.nonzero(bl & ~er)
    return fit(bx.astype(float) + x0, by.astype(float) + y0)


def fit(px, py):
    x = px - px.mean(); y = py - py.mean()
    D = np.stack([x * x, x * y, y * y, x, y, np.ones_like(x)], 1)
    _, _, V = np.linalg.svd(D, full_matrices=False)
    a, b, c, d, e, f = V[-1]
    M = np.array([[a, b / 2], [b / 2, c]])
    try:
        cen = np.linalg.solve(2 * M, [-d, -e])
    except Exception:
        return None
    k = a * cen[0] ** 2 + b * cen[0] * cen[1] + c * cen[1] ** 2 + d * cen[0] + e * cen[1] + f
    ev, evec = np.linalg.eigh(M)
    if np.any(-k / ev <= 0):
        return None
    ax = np.sqrt(-k / ev); o = np.argsort(ax)[::-1]
    ang = math.atan2(evec[1, o[0]], evec[0, o[0]])
    return np.array([cen[0] + px.mean(), cen[1] + py.mean(),
                     ax[o[0]], ax[o[1]], ang % math.pi])


RO = conic_of((270, 494, 346, 600), L, 170, 'lt')
HL = conic_of((372, 584, 466, 676), GR, 16, 'lt')
for n, c in (("roundel", RO), ("near HL", HL)):
    print("measured %-8s cx %.1f cy %.1f semi-maj %.2f semi-min %.2f ratio %.3f ang %.1f deg"
          % (n, c[0], c[1], c[2], c[3], c[3] / c[2], math.degrees(c[4])))

t = np.linspace(0, 2 * math.pi, 360, endpoint=False)


def resid(p):
    H = np.append(p[:8], 1.0).reshape(3, 3)
    r = p[8]
    out = []
    for (cx, cy, rad), meas in ((( 0.0, 0.0, 0.140), RO),
                                ((0.545, -0.16948, r), HL)):
        P = np.stack([cx + rad * np.cos(t), cy + rad * np.sin(t), np.ones_like(t)], 1)
        Q = P @ H.T
        w = Q[:, 2]
        if np.any(np.abs(w) < 1e-6) or (w.min() * w.max() <= 0):
            return np.full(10, 1e4)
        uv = Q[:, :2] / w[:, None]
        ep = fit(uv[:, 0], uv[:, 1])
        if ep is None:
            return np.full(10, 1e4)
        da = (ep[4] - meas[4] + math.pi / 2) % math.pi - math.pi / 2
        out += [ep[0] - meas[0], ep[1] - meas[1], ep[2] - meas[2],
                ep[3] - meas[3], da * meas[2]]
    return np.array(out)


best = None
rng = np.random.default_rng(0)
for trial in range(150):
    H0 = np.array([[300., 0., 306.], [0., -300., 547.], [0., 0., 1.]])
    H0[0, :2] += rng.normal(0, 200, 2)
    H0[1, :2] += rng.normal(0, 200, 2)
    H0[2, :2] += rng.normal(0, 1.0, 2)
    p0 = np.append(H0.reshape(-1)[:8], rng.uniform(0.07, 0.12))
    try:
        s = least_squares(resid, p0, xtol=1e-14, ftol=1e-14, max_nfev=3000,
                          bounds=(np.append(np.full(8, -1e5), 0.055),
                                  np.append(np.full(8, 1e5), 0.135)))
    except Exception:
        continue
    c = float(np.sum(s.fun ** 2))
    if best is None or c < best[0]:
        best = (c, s.x, s.fun)

c, x, fun = best
print("\nBEST HOMOGRAPHY (flat nose, ANY camera, ANY focal length):")
print("  rms residual %.3f px over 10 observations" % math.sqrt(c / 10))
print("  lamp aperture radius solved to %.4f m (dia %.3f m)" % (x[8], 2 * x[8]))
print("  residuals [roCx roCy roMaj roMin roAng | hlCx hlCy hlMaj hlMin hlAng] px")
print("  ", np.round(fun, 2))
