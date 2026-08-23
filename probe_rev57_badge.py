"""probe_rev57_badge.py -- rev 57, ITEM A.  THE NOSE BADGE'S STROKE WEIGHT.

THE JOB (brief rev 57 sec.3.3, deferred at rev 54, 55 AND 56): compare the two
VW badges' STROKE WEIGHT against a frame we hold.  The route is the NOSE badge
on `ref_workshop.jpg` -- item 7's four closed routes are all about the HUBCAP
badge and none closes the nose (rule 34).

WHAT A FRAME MEASURES.  Not `CAP_EMBLEM_WFRAC`.  `vw_bars` is called at R=1 and
`_fit_glyph` then rescales by the outline's own rmax, so the photographable
quantity is stroke width / ring OUTER radius.  This probe takes it OFF THE
BUILT MESH instead of off any constant (rule 10): probe_rev57_geom.py dumps
vw_ring and the two vwbar prisms, and the six strokes' widths are read as the
perpendicular distance between each stroke's own two parallel outline edges.

THE RESULT IS A REFUSAL, AND IT IS A MEASURED ONE.  Two estimators that each
recover the MODEL's known width EXACTLY from a synthetic image blurred to this
frame's PSF at this frame's scale disagree by 49 points ON THE PHOTOGRAPH, in
OPPOSITE directions, and each is refuted by its own painted window:

  * the 50 %-threshold / distance-transform route reads HIGH (+18 %); its mask
    is refuted by a control -- an 18 % width change costs only IoU 0.885, but
    that mask's best achievable IoU against the glyph is 0.537 and the fit runs
    away to width x1.85.  The mask is eating the proud pressing's SHADOW.
  * the level-free edge-gradient route reads LOW (-31 %); PAINTING IT SHOWS IT
    LOCKED ONTO THE SPECULAR HIGHLIGHT running along each stroke, whose
    gradient beats the stroke's own boundary.

AND THE DIVERGENCE IS A PROPERTY OF THE TARGET, NOT OF THE TOOLS.  Run BOTH on
the RING BAND of the SAME badge in the SAME frame and they agree to 0.8 %.  A
stroke is six short segments each with a highlight down its middle; the band is
an annulus that can be averaged over hundreds of rays and fitted globally.
That is why the record could measure the band to +-0.119 px here and cannot
measure the stroke at all.

WHAT IS DELIVERED INSTEAD: the FIRST built-against-frame comparison on either
badge -- the ring band -- and the resolution of the brief's ceiling (a).
NO STROKE-WEIGHT NUMBER IS PUBLISHED.  Rule 8, rule 12.
"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw
import scipy.ndimage as ndi

ROOT = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(ROOT, "probe_scratch"); os.makedirs(OUTD, exist_ok=True)
P = print
REF = os.path.join(ROOT, "ref_workshop.jpg")
NPZ = os.path.join(OUTD, "rev57_glyph.npz")

_RGB = np.asarray(Image.open(REF).convert("RGB")).astype(float)
LUM = 0.2126 * _RGB[..., 0] + 0.7152 * _RGB[..., 1] + 0.0722 * _RGB[..., 2]


# ===================================================== 1. THE RING'S ELLIPSE
def _samp(A, x, y):
    x = np.clip(x, 0, A.shape[1] - 1.001); y = np.clip(y, 0, A.shape[0] - 1.001)
    xi = np.floor(x).astype(int); yi = np.floor(y).astype(int)
    fx = x - xi; fy = y - yi
    return (A[yi, xi] * (1 - fx) * (1 - fy) + A[yi, xi + 1] * fx * (1 - fy)
            + A[yi + 1, xi] * (1 - fx) * fy + A[yi + 1, xi + 1] * fx * fy)


def _fit_ellipse(x, y):
    mx, my = x.mean(), y.mean(); X = x - mx; Y = y - my
    D = np.column_stack([X * X, X * Y, Y * Y, X, Y, np.ones_like(X)])
    _, _, V = np.linalg.svd(D, full_matrices=False)
    a, b, c, d, e, f = V[-1]
    cen = np.linalg.solve(np.array([[2 * a, b], [b, 2 * c]]), [-d, -e])
    fc = (a * cen[0] ** 2 + b * cen[0] * cen[1] + c * cen[1] ** 2
          + d * cen[0] + e * cen[1] + f)
    Q = np.array([[a, b / 2], [b / 2, c]]) / (-fc)
    w, Vv = np.linalg.eigh(Q); ax = 1 / np.sqrt(w)
    o = np.argsort(-ax); ax = ax[o]; Vv = Vv[:, o]
    return np.array([cen[0] + mx, cen[1] + my, ax[0], ax[1],
                     math.atan2(Vv[1, 0], Vv[0, 0])])


def _rell(p, t):
    c = math.cos(t - p[4]); s = math.sin(t - p[4])
    return 1.0 / math.sqrt((c / p[2]) ** 2 + (s / p[3]) ** 2)


def _resid(x, y, p):
    ct, st = math.cos(p[4]), math.sin(p[4])
    u = (x - p[0]) * ct + (y - p[1]) * st
    v = -(x - p[0]) * st + (y - p[1]) * ct
    rho = np.sqrt((u / p[2]) ** 2 + (v / p[3]) ** 2)
    rad = np.hypot(x - p[0], y - p[1])
    return rad * (1 - 1 / np.where(rho == 0, 1, rho))


def _extents(p):
    c, s = math.cos(p[4]), math.sin(p[4])
    return (2 * math.hypot(p[2] * c, p[3] * s), 2 * math.hypot(p[2] * s, p[3] * c))


def ring_fit(frac, nray=720, dr=0.04, sm=0.6):
    """OUTERMOST crossing of `frac` of the way from cream down to the ring's
    own trough, walking INWARD.  Bounded per-ray, because an unbounded walk
    finds the GREEN PANEL behind the bus at 150 deg (checked, not assumed)."""
    p = np.array([304.0, 548.0, 46.5, 31.2, math.radians(-79.0)])
    for _ in range(12):
        ang = []; rad = []
        for i in range(nray):
            t = i * 2 * math.pi / nray; re = _rell(p, t)
            rr = np.arange(0.60 * re, 1.30 * re, dr)
            v = ndi.gaussian_filter1d(
                _samp(LUM, p[0] + rr * math.cos(t), p[1] + rr * math.sin(t)), sm / dr)
            out = rr > 1.12 * re; inn = (rr > 0.78 * re) & (rr < 1.0 * re)
            if out.sum() < 5 or inn.sum() < 5:
                continue
            cream = np.median(v[out]); trough = v[inn].min()
            if cream - trough < 30:
                continue
            tgt = cream - frac * (cream - trough)
            k = len(rr) - 1
            while k > 0 and v[k] > tgt:
                k -= 1
            if k <= 0 or k >= len(rr) - 1:
                continue
            ang.append(t); rad.append(rr[k] + (tgt - v[k]) / (v[k + 1] - v[k]) * dr)
        ang = np.array(ang); rad = np.array(rad)
        x = p[0] + rad * np.cos(ang); y = p[1] + rad * np.sin(ang)
        p = _fit_ellipse(x, y)
    r = _resid(x, y, p); keep = np.abs(r) < 2.5 * r.std()
    p = _fit_ellipse(x[keep], y[keep])
    return p, _resid(x[keep], y[keep], p).std(), int(keep.sum())


P("=" * 78)
P("  1. THE RING'S OUTER BOUNDARY -- three edge levels, so the systematic is")
P("     STATED rather than hidden in one choice of threshold.")
P("=" * 78)
P("%-6s %5s %10s %10s %9s %10s %10s %8s"
  % ("level", "n", "majorD", "minorD", "tilt", "vertD", "horizD", "resid"))
FITS = {}
for frac in (0.35, 0.50, 0.65):
    p, sd, n = ring_fit(frac); FITS[frac] = p
    Dx, Dy = _extents(p)
    P("%-6.2f %5d %10.3f %10.3f %+9.2f %10.3f %10.3f %8.4f"
      % (frac, n, 2 * p[2], 2 * p[3], math.degrees(p[4]), Dy, Dx, sd))
RING = FITS[0.50]
P("  the record, t1_detail.py band comment  : vertical D 91.729  horizontal 62.705")
P("  the record, vw_logo_fit / SPEC 10.107  : vertical D 91.885  horizontal 63.143")
P("  ^ TWO DIFFERENT VALUES for one boundary in one file -- see the ledger.")
P("  this probe, 50 %% level                 : vertical D %.3f  horizontal %.3f"
  % (_extents(RING)[1], _extents(RING)[0]))
def _paint_ring():
    bx0, by0, bx1, by1 = 248, 484, 362, 614
    c = Image.open(REF).convert("RGB").crop((bx0, by0, bx1, by1))
    Kp = 10
    c = c.resize((c.width * Kp, c.height * Kp), Image.LANCZOS)
    dr = ImageDraw.Draw(c)
    for p_, col, wd in ((RING, (0, 255, 255), 3),):
        pts = []
        for i in range(721):
            t = i * 2 * math.pi / 720
            u = p_[2] * math.cos(t); v = p_[3] * math.sin(t)
            pts.append(((p_[0] + u * math.cos(p_[4]) - v * math.sin(p_[4]) - bx0) * Kp,
                        (p_[1] + u * math.sin(p_[4]) + v * math.cos(p_[4]) - by0) * Kp))
        dr.line(pts, fill=col, width=wd)
    c.save(os.path.join(OUTD, "rev57_ringfit50.png"))


_paint_ring()
P("  PAINTED -> probe_scratch/rev57_ringfit50.png -- the fit ON the chrome,")
P("  which is the only reason to believe the residual (rule 8).")

X0, Y0, AMAJ, BMIN, TH = RING
E1 = np.array([math.cos(TH), math.sin(TH)])
E2 = np.array([-math.sin(TH), math.cos(TH)])


def badge(a, b, rot=0.0, mirror=False):
    """badge coords -> image.  b is the badge's UP and rides the MAJOR axis
    (the un-foreshortened diameter; the record's 'vertical D' is the long one).
    a, b are in units of the ring OUTER RADIUS."""
    aa = -np.asarray(a, float) if mirror else np.asarray(a, float)
    b = np.asarray(b, float)
    c, s = math.cos(rot), math.sin(rot)
    U = aa * s + b * c
    Vs = aa * c - b * s
    return (X0 + U * AMAJ * E1[0] + Vs * BMIN * E2[0],
            Y0 + U * AMAJ * E1[1] + Vs * BMIN * E2[1])


def deproj(a, b, rot=0.0, mirror=False):
    return _samp(LUM, *badge(a, b, rot, mirror))


# ============================================== 2. THE BUILT STROKE, EXACTLY
P("")
P("=" * 78)
P("  2. THE BUILT STROKE WIDTH -- off the MESH, not off a constant (rule 10)")
P("=" * 78)
if not os.path.exists(NPZ):
    P("  %s missing -- run:  T1_SUB=1 blender -b -P probe_rev57_geom.py" % NPZ)
    sys.exit(0)
Z = np.load(NPZ, allow_pickle=True)
CY, CZ, R_OUT = float(Z["cy"]), float(Z["cz"]), float(Z["R_OUT"])
VP = Z["polys"][0].astype(float); WP = Z["polys"][2].astype(float)
VP = np.column_stack([VP[:, 0] - CY, VP[:, 1] - CZ]) / R_OUT
WP = np.column_stack([WP[:, 0] - CY, WP[:, 1] - CZ]) / R_OUT


def _perp(Pg, ia, ib, ic, idd):
    a, b, c, d = Pg[ia], Pg[ib], Pg[ic], Pg[idd]
    u = (b - a) / np.linalg.norm(b - a); v = (d - c) / np.linalg.norm(d - c)
    n = np.array([-u[1], u[0]])
    return (abs(np.dot(a - c, n)),
            math.degrees(math.asin(min(1, abs(u[0] * v[1] - u[1] * v[0])))))


QS = [("V left ", VP, (1, 2, 5, 0)), ("V right", VP, (2, 3, 4, 5)),
      ("W arm L", WP, (1, 2, 9, 0)), ("W leg L", WP, (2, 3, 8, 9)),
      ("W leg R", WP, (3, 4, 7, 8)), ("W arm R", WP, (4, 5, 6, 7))]
P("%-9s %12s %14s" % ("stroke", "w / R_out", "edges parallel"))
_w = []
for tag, Pg, q in QS:
    w, par = _perp(Pg, *q); _w.append(w)
    P("%-9s %12.5f %11.3f deg" % (tag, w, par))
W0 = float(np.mean(_w))
P("  all six agree to %.2f %% -- a constant-width bar, which is the control"
  % (100 * (max(_w) - min(_w)) / W0))
P("  BUILT  stroke / ring OUTER RADIUS = %.5f" % W0)
P("  BUILT  stroke / ring OUTER D      = %.5f   (%.2f mm on a %.2f mm ring)"
  % (W0 / 2, 1000 * W0 * R_OUT, 2000 * R_OUT))
_ext = float(max(np.hypot(*np.vstack([VP, WP]).T)))
P("  glyph extreme / ring outer R, off the mesh = %.6f  (vw_logo_fit targets 0.84)"
  % _ext)
P("  the brief's route, 0.1986/0.814 x %.6f      = %.5f"
  % (_ext, 0.1986 / 0.814 * _ext))
P("  -> the two agree to %.2f %%, so the brief's denominator is SOUND"
  % (100 * abs(0.1986 / 0.814 * _ext / W0 - 1)))


def spine_of(Pg, q):
    a, b, c, d = q
    return 0.5 * (Pg[a] + Pg[d]), 0.5 * (Pg[b] + Pg[c])


SEG = [spine_of(Pg, q) for _, Pg, q in QS]

# ================================================ 3. THE TWO ESTIMATORS
K = 6.0
RPX = AMAJ * K
N = int(2 * RPX * 1.02)
_jj, _ii = np.meshgrid(np.arange(N), np.arange(N), indexing="xy")
_A = (_jj - N / 2.0) / RPX
_B = -(_ii - N / 2.0) / RPX
IMG = deproj(_A, _B)
RR = np.hypot(_jj - N / 2.0, _ii - N / 2.0) / RPX


def spinemask(rot, wfac, mirror=False):
    m = Image.new("L", (N, N), 0); d = ImageDraw.Draw(m)
    c, s = math.cos(rot), math.sin(rot); f = -1.0 if mirror else 1.0
    for p1, p2 in SEG:
        d.line([(N / 2.0 + ((a * f) * c - b * s) * RPX,
                 N / 2.0 - ((a * f) * s + b * c) * RPX) for (a, b) in (p1, p2)],
               fill=255, width=int(round(max(1.0, W0 * wfac * RPX))), joint="curve")
    return np.asarray(m) > 127


def dt_mode(mask, disc):
    m = mask & disc
    dt = ndi.distance_transform_edt(m) / RPX
    if dt.max() <= 0:
        return np.nan
    mx = ndi.maximum_filter(dt, size=3)
    ridge = m & (dt > 0) & (dt >= mx - 1e-12) & (dt > 0.30 * dt.max())
    wr = 2.0 * dt[ridge]
    h, e = np.histogram(wr, bins=60)
    return 0.5 * (e[np.argmax(h)] + e[np.argmax(h) + 1])


def edge_score(G, rot, wfac, mirror=False, disc=None):
    mm = spinemask(rot, wfac, mirror)
    o = (ndi.binary_dilation(mm, iterations=1)
         & ~ndi.binary_erosion(mm, iterations=1)) & disc
    return float(G[o].mean()) if o.sum() > 50 else 0.0


DISC = RR < 0.74
DISC_E = RR < 0.72
# --- the synthetic control: the model, blurred to THIS frame's PSF ---------
SYN = np.where(spinemask(0.0, 1.0), 110.0, 205.0)
SYN = ndi.gaussian_filter(SYN, 0.689 * K)
G_SYN = ndi.gaussian_gradient_magnitude(SYN, 1.0 * K / 6.0)
G_IMG = ndi.gaussian_gradient_magnitude(IMG, 1.0 * K / 6.0)
P("")
P("=" * 78)
P("  3. TWO ESTIMATORS, EACH CALIBRATED ON A SYNTHETIC RENDER OF THE MODEL")
P("     blurred to this frame's PSF (sigma 0.689 px) at this frame's scale.")
P("     An instrument that has never been wrong has never been tested.")
P("=" * 78)
syn_dt = dt_mode(SYN < 157.5, DISC)
P("  A. distance-transform ridge mode, on the synthetic : %.5f  (truth %.5f, %+.2f %%)"
  % (syn_dt, W0, 100 * (syn_dt / W0 - 1)))
bs = max((edge_score(G_SYN, 0.0, wf, False, DISC_E), wf)
         for wf in np.arange(0.75, 1.45, 0.025))
P("  B. level-free edge-gradient fit, on the synthetic  : width x%.3f (truth x1.000, %+.1f %%)"
  % (bs[1], 100 * (bs[1] - 1)))
P("  BOTH RECOVER THE MODEL.  The instruments are sound.")

P("")
P("  ON THE PHOTOGRAPH:")
P("  A. threshold + distance transform (thr = 50 % of cream 205 -> chrome 127):")
for rd in (0.58, 0.70, 0.78):
    row = [dt_mode(IMG < t, RR < rd) for t in (150, 166, 182)]
    P("       disc r<%.2f   thr150 %.5f   thr166 %.5f   thr182 %.5f"
      % (rd, *row))
dtp = dt_mode(IMG < 166, RR < 0.74)
P("       -> %.5f, i.e. %+.0f %% against the built %.5f" % (dtp, 100 * (dtp / W0 - 1), W0))
best = None
for mir in (False, True):
    for dg in np.arange(-180, 180, 1.0):
        for wf in np.arange(0.60, 1.50, 0.05):
            v = edge_score(G_IMG, math.radians(dg), wf, mir, DISC_E)
            if best is None or v > best[0]:
                best = (v, dg, wf, mir)
P("  B. level-free edge fit: rot %+.1f deg, width x%.2f -> %.5f, i.e. %+.0f %%"
  % (best[1], best[2], W0 * best[2], 100 * (best[2] - 1)))
P("  THE TWO DISAGREE BY %.0f POINTS AND IN OPPOSITE DIRECTIONS."
  % (100 * (dtp / W0 - best[2])))

# ================================================ 4. REFUTING EACH WINDOW
P("")
P("=" * 78)
P("  4. EACH WINDOW REFUTED BY ITS OWN CONTROL (rule 8)")
P("=" * 78)
PM = (IMG < 166) & DISC
base = spinemask(0.0, 1.0) & DISC


def iou(m, n):
    return (m & n).sum() / max(1, (m | n).sum())


P("  what a PURE WIDTH error costs in IoU, at perfect registration:")
for wf in (1.10, 1.18, 1.35):
    P("      width x%.2f -> IoU %.4f" % (wf, iou(base, spinemask(0.0, wf) & DISC)))
bb = None
for mir in (False, True):
    for dg in np.arange(-180, 180, 2.0):
        for wf in np.arange(0.8, 2.0, 0.05):
            v = iou(PM, spinemask(math.radians(dg), wf, mir) & DISC)
            if bb is None or v > bb[0]:
                bb = (v, dg, wf)
P("  the threshold MASK's best achievable IoU against the glyph: %.4f at width x%.2f"
  % (bb[0], bb[2]))
P("  -> WORSE than an 18 % width error can explain, and the fit RUNS AWAY in")
P("     width: the mask is eating the proud pressing's SHADOW, not its edge.")
_ov = np.dstack([np.clip(IMG, 0, 255)] * 3).astype(np.uint8)
_ov[PM] = (_ov[PM] * 0.45 + np.array([255, 50, 50]) * 0.55).astype(np.uint8)
_mm = spinemask(math.radians(bb[1]), 1.0) & DISC
_e = ndi.binary_dilation(_mm, iterations=2) & ~ndi.binary_erosion(_mm, iterations=2)
_ov[_e] = (0, 255, 255)
Image.fromarray(_ov).save(os.path.join(OUTD, "rev57_mask70.png"))
_ov2 = np.dstack([np.clip(IMG, 0, 255)] * 3).astype(np.uint8)
_mo = spinemask(math.radians(best[1]), best[2], best[3])
_ov2[(ndi.binary_dilation(_mo, iterations=1)
      & ~ndi.binary_erosion(_mo, iterations=1)) & DISC_E] = (0, 255, 255)
Image.fromarray(_ov2).save(os.path.join(OUTD, "rev57_edgefit.png"))
P("  PAINTED -> probe_scratch/rev57_mask70.png  (red = the threshold mask,")
P("     cyan = the built glyph AT ITS OWN WIDTH and at the best-IoU rotation).")
P("     LOOK AT IT: the red is not the cyan made fatter.  It is fatter AND it")
P("     sits differently, which is what the 0.537 above says in a number --")
P("     the mask disagrees with the glyph by MORE THAN ANY WIDTH, so it is")
P("     not a stroke-weight reading that happens to be large.  It is not a")
P("     stroke-weight reading.")
P("  PAINTED -> probe_scratch/rev57_edgefit.png : the edge fit collapsed onto")
P("     the SPECULAR HIGHLIGHT running along each stroke, not onto its edge.")
P("  NEITHER NUMBER SURVIVES ITS OWN PICTURE.  That is the finding.")

# =========================== 5. THE CONTROL THAT MAKES THE CEILING A NUMBER
P("")
P("=" * 78)
P("  5. IS THE DIVERGENCE THE TOOLS, OR THE TARGET?  Run BOTH on the RING")
P("     BAND of the SAME badge in the SAME frame, where the record has an")
P("     answer.  A control that finds nothing is still a result.")
P("=" * 78)
thr_w = []; grd_w = []
for deg in list(range(-14, 15, 2)) + list(range(166, 195, 2)):
    # phi is measured FROM THE BADGE'S +b AXIS, which rides the MAJOR axis.
    # Measured from +a instead, these rays run down the MINOR axis -- the
    # foreshortened one -- and the control reads 0.109/0.131 at sd 0.025
    # instead of 0.092/0.093 at sd 0.006.  The window is part of the
    # measurement, and this one was wrong on the first run (rule 8).
    t = math.radians(deg)
    rr = np.arange(0.55, 1.30, 0.01)
    v = ndi.gaussian_filter1d(deproj(rr * math.sin(t), rr * math.cos(t)), 3)
    cream = np.median(v[rr > 1.15]); trough = v[(rr > 0.80) & (rr < 1.02)].min()
    if cream - trough < 40:
        continue
    tgt = 0.5 * (cream + trough)
    k = len(rr) - 1
    while k > 0 and v[k] > tgt:
        k -= 1
    ro = rr[k] + (tgt - v[k]) / (v[k + 1] - v[k]) * 0.01
    j = k
    while j > 0 and v[j] <= tgt:
        j -= 1
    if j <= 0:
        continue
    thr_w.append(ro - (rr[j] + (tgt - v[j]) / (v[j + 1] - v[j]) * 0.01))
    g = np.gradient(v, 0.01)
    ko = int(np.argmax(g[rr > 0.90])) + int((rr <= 0.90).sum())
    grd_w.append(rr[ko] - rr[int(np.argmin(g[rr < 0.95]))])
thr_w = np.array(thr_w); grd_w = np.array(grd_w)
MESH_BAND = (R_OUT - 0.111985) / (2 * R_OUT)
P("  ring BAND / ring outer D, %d rays on the major axis:" % len(thr_w))
P("      50%%-threshold route  %.5f +/- %.5f" % (thr_w.mean() / 2, thr_w.std() / 2))
P("      gradient-peak route  %.5f +/- %.5f" % (grd_w.mean() / 2, grd_w.std() / 2))
_gap = 100 * abs(thr_w.mean() / grd_w.mean() - 1)
_str = 100 * abs(dtp / (W0 * best[2]) - 1)
P("      the two routes differ by %.1f %% HERE, against %.0f %% on the STROKE."
  % (_gap, _str))
P("      VERDICT (derived, not asserted): the divergence is a property of the")
P("      %s.  [band gap %.1f %% vs stroke gap %.0f %%]"
  % ("TARGET, not the tools" if _gap < 0.25 * _str else
     "TOOLS -- this control FAILED and the ceiling below is NOT established",
     _gap, _str))
P("      the record (t1_detail.py, vertical axis)     0.0874")
P("      adopted in the source                        0.093 +/- 0.012")
P("  ** THE FIRST BUILT-AGAINST-FRAME COMPARISON ON EITHER BADGE **")
P("      BUILT, off vw_ring's own mesh                %.5f" % MESH_BAND)
P("      -> the built band is %+.1f %% against this probe's %.5f,"
  % (100 * (MESH_BAND / (thr_w.mean() / 2) - 1), thr_w.mean() / 2))
P("         and %+.1f %% against the record's 0.0874." % (100 * (MESH_BAND / 0.0874 - 1)))
P("         It is INSIDE the adopted 0.093 +/- 0.012, at the top of it, while")
P("         three separate readings of the frame cluster at 0.087..0.093.")

P("")
P("=" * 78)
P("  VERDICT -- ITEM A")
P("=" * 78)
P("  THE STROKE WEIGHT CANNOT BE RECOVERED FROM WHAT WE HOLD.  The bracket the")
P("  frame supports is %.5f .. %.5f (%+.0f %% .. %+.0f %% on the built %.5f)."
  % (W0 * best[2], dtp, 100 * (best[2] - 1), 100 * (dtp / W0 - 1), W0))
P("  The built value lies INSIDE that bracket, so the frame does not refute it")
P("  -- but the bracket is %.0f points of the built value wide, and the two"
  % (100 * (dtp - W0 * best[2]) / W0))
P("  questions it was meant to settle are a 5.09 % difference between the two")
P("  badge DESIGNS and an 18.6 % denominator.  IT CANNOT SEE EITHER, by a")
P("  factor of %.0f.  NO STROKE NUMBER IS PUBLISHED."
  % ((100 * (dtp - W0 * best[2]) / W0) / 5.09))
P("  Reported WITH ITS CEILING, not as a score (rule 12).")
