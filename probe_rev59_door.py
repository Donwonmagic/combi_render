# probe_rev59_door.py -- rev 59.  THE CAB DOOR'S FORWARD LOBE, AND WHETHER THE
# FRONT ARCH IS A CIRCLE.  Both measured off ref_nolita_doorshut.jpg, and BOTH
# CONTROLLED by running the identical pixel code on a render whose answer the
# source already knows.
#
# WHY IT EXISTS.  The rev-59 brief section 3.10 carries two claims:
#   (a) the door's step must move aft ~95 mm, because DOOR_LOBE_A/B were built
#       off the WHEEL HUB column while the model's datum is the ARCH centre,
#       and off a px/m obtained by assuming the radius it then measures;
#   (b) the front arch "is up to 0.13 A ~ 48 mm inboard of a circle", from a
#       radius-versus-angle sweep about (crown column, hub row).
# (a) REPRODUCES, at a smaller magnitude.  (b) DOES NOT SURVIVE ITS OWN CONTROL:
# run the same sweep on the side render -- whose front arch IS a circle of
# ARCH_R about X_AXLE_F, by construction -- and it invents swings of +-0.07 R
# on a shape that is exactly circular.  Section 3.10's 1.0241 -> 0.8723 fall
# sits inside that artefact band.  A CIRCLE FIT, which is what this probe uses
# instead, recovers the render's own centre to 0.3 px and its radius to 0.5 %.
#
# WHICH AXES THIS GATE DOES NOT SEE (rule 36).  It sees the door line and the
# arch lip in ONE frame, in the flank plane, in COLUMNS and ROWS.  It does not
# see: the arch below the door line (deep shade and the white bumper cut in --
# not recoverable from what we hold); the off side; or absolute millimetres
# independently of ARCH_R, because ARCH_R is the ruler.  Every figure it
# publishes is DIMENSIONLESS -- a ratio of two flank-plane lengths in one
# frame -- so it carries no px/m and no parallax term.  That is deliberate:
# section 3.10's own +-4 % parallax floor came from mixing the flank plane
# (the arch crown) with the wheel plane (the hub), and this probe does not.
#
# READ THIS PROBE'S OWN SUMMARY LINE, NEVER ITS EXIT CODE (rule 9).
import sys, os
import numpy as np
from PIL import Image

REF   = "ref_nolita_doorshut.jpg"
PHOTO = os.path.join(os.path.dirname(os.path.abspath(__file__)), REF)

# ---- the model's own constants, so the control has something to miss -------
#
# READ LIVE, NEVER RE-TYPED.  The first cut of this probe pasted rev 44b's two
# constants as literals, and the moment the source moved -- in the same
# revision, by this probe's own finding -- the controls started grading the new
# build against the old numbers and reported the FIX as a 20 % miss.  A probe
# that re-types the thing it is checking is checking its own typing.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import t1_core as _T
import t1_shell as _S
X_AXLE_F, TIRE_R, ARCH_R = _T.X_AXLE_F, _T.TIRE_R, _S.ARCH_R
DOOR_LOBE_A_BUILT, DOOR_LOBE_B_BUILT = _S.DOOR_LOBE_A, _S.DOOR_LOBE_B
ORTHO, RX, RY, CAM_Z = 5.90, 1600, 1100, 1.52     # studio.py "side"


def _load(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(float)
    return a, a[..., 0] - 0.5 * (a[..., 1] + a[..., 2]), a.mean(axis=2)


def kasa(u, v):
    A = np.c_[u, v, np.ones(len(u))]
    c, *_ = np.linalg.lstsq(A, u * u + v * v, rcond=None)
    cu, cv = c[0] / 2, c[1] / 2
    return cu, cv, np.sqrt(c[2] + cu * cu + cv * cv)


def trace_lip(red, u_lo, u_hi, v_lo, v_hi, hold, minc=25):
    """Sub-pixel arch lip: the first SUSTAINED fall of redness in a column.
    'Sustained' -- redness must STAY below the half level for `hold` more rows.
    That is the clause that rejects the folk art, whose motifs fall and recover
    within a few rows and which poisoned the crown before it was added."""
    cols, rows = [], []
    for u in range(u_lo, u_hi):
        col = red[v_lo:v_hi + 1, u]
        if len(col) < hold + 8:
            continue
        hi, lo = np.percentile(col[:6], 75), np.percentile(col[-6:], 25)
        if hi - lo < minc:
            continue
        half = 0.5 * (hi + lo)
        for i in range(len(col) - hold - 1):
            if col[i] >= half > col[i + 1] and (col[i + 1:i + 1 + hold] < half).all():
                cols.append(float(u))
                rows.append(v_lo + i + (col[i] - half) / (col[i] - col[i + 1]))
                break
    return np.array(cols), np.array(rows)


def despike(u, v, tol=2.0):
    o = np.argsort(u); u, v = u[o], v[o]
    med = np.array([np.median(v[max(0, i - 2):i + 3]) for i in range(len(v))])
    k = np.abs(v - med) < tol
    return u[k], v[k]


def arch_fit(u, v, hw_frac=0.78, iters=6):
    """Circle fit over a window scaled to the fitted radius, so the ANGULAR
    span is the same at both image scales and the two are comparable."""
    cu = u[np.argmin(v)]; r = 0.35 * (u.max() - u.min())
    for _ in range(iters):
        k = np.abs(u - cu) <= hw_frac * r
        if k.sum() < 8:
            break
        cu, cv, r = kasa(u[k], v[k])
    k = np.abs(u - cu) <= hw_frac * r
    res = np.hypot(u[k] - cu, v[k] - cv) - r
    return cu, cv, r, np.sqrt((res ** 2).mean()), int(k.sum())


def walk(lum, u_start, v_start, u_end, half, mind):
    """Follow the shut line column by column.  A tracked walk, not a per-column
    search: the groove and the arch lip's own shadow are both dark, and a
    per-column minimum swaps between them (it did, for four columns)."""
    v, pts = v_start, []
    step = -1 if u_end < u_start else 1
    for u in range(u_start, u_end, step):
        lo, hi = int(round(v - half)), int(round(v + half))
        col = lum[lo:hi + 1, u]
        i = int(np.argmin(col))
        if i == 0 or i == len(col) - 1:
            break
        sh = 0.5 * (col[max(0, i - 3)] + col[min(len(col) - 1, i + 3)])
        if sh - col[i] < mind:
            break
        y0, y1, y2 = col[i - 1], col[i], col[i + 1]
        den = y0 - 2 * y1 + y2
        v = lo + i + (0.5 * (y0 - y2) / den if abs(den) > 1e-9 else 0.0)
        pts.append((float(u), v))
    return np.array(pts)


def feet(pts, frac=0.18):
    """The two flats and the ramp between them, segmented BY THE FLAT LEVELS
    THEMSELVES rather than by a slope threshold -- the same code then works at
    both image scales.  A slope threshold did not (rms 9.9 px on the render).

    rev 60c-ii -- THE RAMP IS FITTED u-ON-v, NOT v-ON-u, AND THAT IS THE WHOLE
    POINT.  The shut line steps down about 78 px over roughly 25 px of u, so
    |dv/du| ~ 3: fitting v as a function of u across it is ILL-CONDITIONED,
    and the returned feet -- (zl - p1)/p0 -- divide by that badly-determined
    slope.  Measured consequence: the rev-60c underbody let the tracked walk
    run THREE COLUMNS further before its `mind` break (116 points against
    113), and on walks otherwise IDENTICAL to under 1.1 px the old fit flipped
    from (b 347.96, a 376.19, rms 1.13) to (b 289.84, a 425.79, rms 12.47).
    C4 and C5 both went red on a door that had not moved, and NOTHING in the
    tree reported it -- verify.py, verify_clone.sh and both audits were green
    throughout.  An independent adversary found it by rendering the live tree
    and re-running this probe.

    v spans the full step while u spans only the ramp's width, so u-on-v is
    the conditioned regression and the feet come straight out of it with no
    division by a slope at all."""
    u, v = pts[:, 0], pts[:, 1]
    o = np.argsort(u); u, v = u[o], v[o]
    k = max(3, int(frac * len(u)))
    zl, zr = np.median(v[:k]), np.median(v[-k:])
    D = zl - zr
    band = (v > zr + 0.18 * D) & (v < zl - 0.18 * D)
    # rev 60c-ii -- AND THE BAND MUST BE THE CONTIGUOUS RUN, NOT EVERY POINT
    # WHOSE v HAPPENS TO LIE IN THE RANGE.  The shut line does not stop at the
    # lower flat: past it the tracked feature RISES again at the door's
    # forward end, and that rise re-enters the same v range 48 columns away
    # from the ramp.  Measured: on the live tree the band held u 305 (v 820.2)
    # and u 306 (v 824.0) alongside the ramp at u 353-372, and the fit's rms
    # went to 13.7 px.  Whether those two columns exist at all depends on
    # where the walk's `mind` break happens to land -- the rev-60c underbody
    # moved it by three columns, which is how a door that had not moved took
    # C4 and C5 red.  The ramp is ONE connected segment between the flats;
    # anything disconnected from it is a different feature.
    if band.any():
        idx = np.nonzero(band)[0]
        cut = np.nonzero(np.diff(idx) > 1)[0]
        runs = np.split(idx, cut + 1)
        keep = max(runs, key=len)
        band = np.zeros_like(band); band[keep] = True
    q = np.polyfit(v[band], u[band], 1)          # u = q0*v + q1  -- CONDITIONED
    res = u[band] - np.polyval(q, v[band])
    return (np.polyval(q, zl), np.polyval(q, zr), zl, zr,
            np.sqrt((res ** 2).mean()), int(band.sum()))


def selftest():
    """RUN THE INSTRUMENT ON A CASE WHOSE ANSWER YOU KNOW.

    rev 60c-ii.  `feet()` had two defects that took C4 and C5 red on a door
    that had not moved (F131), and neither could be watched through an
    ablation: T1_DOOR_STALE refuses at BUILD time, so it never produces a
    frame this probe could read.  This is the control instead -- a synthetic
    flat/ramp/flat whose feet are known BY CONSTRUCTION, with and without the
    contaminant that caused the failure (the door's forward-end rise
    re-entering the ramp's v band 40-odd columns away).

    Watched, and this is what makes the fix a fix rather than an opinion:

        clean step                OLD  b -0.00   a +0.00     NEW  b -0.00  a -0.00
        with the forward-end RISE OLD  b -50.37  a +47.59    NEW  b -0.00  a -0.00
    """
    us, vs = [], []
    for u in range(372, 421):
        us.append(u); vs.append(765.0)                       # upper flat
    for u in range(348, 372):
        us.append(u); vs.append(765.0 + (372 - u) * (78.0 / 24.0))   # the ramp
    for u in range(310, 348):
        us.append(u); vs.append(843.0)                       # lower flat
    clean = np.array(list(zip(us, vs)), dtype=float)
    for u in (307, 306, 305):
        us.append(u); vs.append(843.0 - (308 - u) * 6.0)     # the CONTAMINANT
    dirty = np.array(list(zip(us, vs)), dtype=float)

    bad = 0
    for tag, pts in (("clean step", clean), ("with the forward-end rise", dirty)):
        b, a, zl, zr, rms, n = feet(pts)
        ok = abs(b - 348.0) < 0.5 and abs(a - 372.0) < 0.5
        bad += 0 if ok else 1
        print("  %-4s %-26s b %7.2f (%+6.2f)  a %7.2f (%+6.2f)  rms %.3f"
              % ("PASS" if ok else "FAIL", tag, b, b - 348.0, a, a - 372.0, rms))
    print("  feet() selftest: %d checked, %d FAILED  -- the feet are known BY "
          "CONSTRUCTION, so a failure here is the INSTRUMENT" % (2, bad))
    return 1 if bad else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    frame = sys.argv[1] if len(sys.argv) > 1 else None
    if not frame or not os.path.exists(frame):
        print("NO RENDER -- pass a side-elevation render as argv[1]; out/ is "
              "untracked and starts empty on a clone.  Nothing was measured.")
        return 2

    fails, checks = [], []

    def ck(name, ok, detail):
        checks.append((name, ok, detail))
        if not ok:
            fails.append(name)

    # ------------------------------------------------- the render, as control
    a_r, red_r, lum_r = _load(frame)
    if a_r.shape[0] != RY or a_r.shape[1] != RX:
        print("NO RENDER -- %s is %dx%d, not the %dx%d side elevation this "
              "probe's ortho scale is written for." % (frame, a_r.shape[1],
                                                       a_r.shape[0], RX, RY))
        return 2
    pxm = RX / ORTHO
    u_ax = RX / 2.0 - X_AXLE_F * pxm
    v_ax = RY / 2.0 + (CAM_Z - TIRE_R) * pxm

    sat = a_r.max(axis=2) - a_r.min(axis=2)
    bg = (lum_r > 225) & (sat < 25)              # the cyclorama, EXCLUDED
    v0, v1, u0, u1 = 790, 960, 370, 530
    w = lum_r[v0:v1, u0:u1].copy()
    w[bg[v0:v1, u0:u1]] = -1e9
    m = w >= np.percentile(w[w > -1e8], 88)
    vv, uu = np.nonzero(m); uu, vv = uu + u0, vv + v0
    cu, cv = uu.mean(), vv.mean()
    k = np.hypot(uu - cu, vv - cv) > 25; uu, vv = uu[k], vv[k]
    for _ in range(6):
        cu, cv, rr = kasa(uu, vv)
        d = np.abs(np.hypot(uu - cu, vv - cv) - rr)
        k = d < max(2.0, 2 * d.std()); uu, vv = uu[k], vv[k]
    ck("C1 hub finder recovers the model's own front axle",
       abs(cu - u_ax) < 4 and abs(cv - v_ax) < 4,
       "du %+.2f px  dv %+.2f px  (%+.1f mm, %+.1f mm)"
       % (cu - u_ax, cv - v_ax, 1000 * (cu - u_ax) / pxm, 1000 * (cv - v_ax) / pxm))

    lu, lv = despike(*trace_lip(red_r, 298, 604, 752, int(cv), hold=8))
    rcu, rcv, rR, rrms, rn = arch_fit(lu, lv)
    ck("C2 circle fit recovers the render's own ARCH_R",
       abs(rR - ARCH_R * pxm) / (ARCH_R * pxm) < 0.03,
       "R %.2f px against ARCH_R*pxm %.2f  (%+.2f %%), centre du %+.2f dv %+.2f, n=%d"
       % (rR, ARCH_R * pxm, 100 * (rR - ARCH_R * pxm) / (ARCH_R * pxm),
          rcu - u_ax, rcv - v_ax, rn))
    ck("C3 the render's arch fits a circle to the instrument's noise floor",
       rrms < 0.6, "rms %.3f px = %.3f %% of R  -- THIS IS THE FLOOR every "
       "non-circularity claim must clear" % (rrms, 100 * rrms / rR))

    rb, ra, rzl, rzr, rramp, rnb = feet(walk(lum_r, 420, 765.0, 300, 6, 2.0))
    tA = RX / 2.0 - (X_AXLE_F + DOOR_LOBE_A_BUILT * ARCH_R) * pxm
    tB = RX / 2.0 - (X_AXLE_F + DOOR_LOBE_B_BUILT * ARCH_R) * pxm
    ck("C4 lobe feet recover the model's own DOOR_LOBE_A / DOOR_LOBE_B",
       abs(ra - tA) < 3 and abs(rb - tB) < 3,
       "aft %+.2f px (%+.1f mm)  fwd %+.2f px (%+.1f mm), ramp rms %.3f px"
       % (ra - tA, 1000 * (ra - tA) / pxm, rb - tB, 1000 * (rb - tB) / pxm, rramp))
    mA_r, mB_r = (rcu - ra) / rR, (rcu - rb) / rR
    ck("C5 the WHOLE chain reproduces the built constants end to end",
       abs(mA_r - DOOR_LOBE_A_BUILT) < 0.03 and abs(mB_r - DOOR_LOBE_B_BUILT) < 0.05,
       "A %.4f vs built %.4f (%+.2f %%)   B %.4f vs built %.4f (%+.2f %%)"
       % (mA_r, DOOR_LOBE_A_BUILT, 100 * (mA_r / DOOR_LOBE_A_BUILT - 1),
          mB_r, DOOR_LOBE_B_BUILT, 100 * (mB_r / DOOR_LOBE_B_BUILT - 1)))

    # ------------------------------------------------------- the photograph
    a_p, red_p, lum_p = _load(PHOTO)
    pu, pv = despike(*trace_lip(red_p, 58, 132, 236, 300, hold=4))
    pcu, pcv, pR, prms, pn = arch_fit(pu, pv)
    pb, pa, pzl, pzr, pramp, pnb = feet(walk(lum_p, 60, 239.4, 36, 4, 4.0))
    mA, mB = (pcu - pa) / pR, (pcu - pb) / pR

    ck("M1 the ramp's WIDTH agrees with the built width",
       abs((mB - mA) / (DOOR_LOBE_B_BUILT - DOOR_LOBE_A_BUILT) - 1) < 0.08,
       "photograph %.4f of R against built %.4f  (%+.2f %%) -- the step is the "
       "right SIZE, only in the wrong PLACE"
       % (mB - mA, DOOR_LOBE_B_BUILT - DOOR_LOBE_A_BUILT,
          100 * ((mB - mA) / (DOOR_LOBE_B_BUILT - DOOR_LOBE_A_BUILT) - 1)))
    ck("M2 the built lobes sit where the photograph puts them",
       abs(mA - DOOR_LOBE_A_BUILT) < 0.03 and abs(mB - DOOR_LOBE_B_BUILT) < 0.03,
       "photograph A %.4f B %.4f against built %.4f %.4f -- built stands "
       "%+.1f / %+.1f mm FORWARD of the photograph (+ = too far forward)"
       % (mA, mB, DOOR_LOBE_A_BUILT, DOOR_LOBE_B_BUILT,
          1000 * (DOOR_LOBE_A_BUILT - mA) * ARCH_R,
          1000 * (DOOR_LOBE_B_BUILT - mB) * ARCH_R))
    ck("M3 the photographed front arch is a circle to the render's own floor",
       prms / pR <= rrms / rR * 2.0,
       "photograph rms %.3f px = %.3f %% of R (n=%d) against the render's %.3f %% "
       "on a KNOWN circle -- ratio %.1fx.  Departure %.1f mm rms on ARCH_R, NOT "
       "the 48 mm section 3.10 claims"
       % (prms, 100 * prms / pR, pn, 100 * rrms / rR, (prms / pR) / (rrms / rR),
          1000 * (prms / pR) * ARCH_R))

    print("=" * 78)
    print("  probe_rev59_door -- the cab door's forward lobe and the front arch")
    print("  render %s" % frame)
    print("=" * 78)
    for name, ok, detail in checks:
        print("  %-4s %s" % ("PASS" if ok else "FAIL", name))
        print("       %s" % detail)
    print("-" * 78)
    print("  PHOTOGRAPH  arch centre col %.2f  R %.2f px  rms %.3f px  n=%d"
          % (pcu, pR, prms, pn))
    print("  PHOTOGRAPH  lobe feet: aft col %.3f  fwd col %.3f  ramp rms %.3f px"
          % (pa, pb, pramp))
    print("  PHOTOGRAPH  DOOR_LOBE_A %.4f   DOOR_LOBE_B %.4f   (units of ARCH_R)"
          % (mA, mB))
    print("  BUILT       DOOR_LOBE_A %.4f   DOOR_LOBE_B %.4f"
          % (DOOR_LOBE_A_BUILT, DOOR_LOBE_B_BUILT))
    print("-" * 78)
    print("  %d checked, %d FAILED%s"
          % (len(checks), len(fails), ("  --  " + "; ".join(fails)) if fails else ""))
    print("=" * 78)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
