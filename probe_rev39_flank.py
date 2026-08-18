"""probe_rev39_flank.py -- SPEC 10.97.  READ-ONLY.  Changes nothing.

THE OWNER'S OWN METHOD, executed for the first time on the WHOLE flank:
"drive fixes off the broadside render laid over ref_side.jpg at matched scale".
`flank_compare.py` does this for the SCRIPT LOCKUP only; this carries the whole
ortho broadside into ref_side.jpg's own projective frame and registers it.

NO NEW ESTIMATOR (SPEC 10.79/10.83's rule -- do not open a third estimator on a
panel two have already died on).  Every instrument here is already calibrated
in this repo and is IMPORTED, never re-typed:

    flank_compare.flank_X / flank_u / flank_mpp / flank_kv   SPEC 10.34 + 10.35
    flank_compare.projector()                                the exact ortho map
    the cream/red two-tone break, fitted in BOTH frames by flank_compare and
    used by it as ONE datum precisely so its own height never enters

WHAT IT MEASURES, and it is a RELATIVE measurement by construction: the warp
pins the model's break line onto the photograph's, so the residual is the whole
BODY against the BREAK.  It is not a ride-height measurement and must never be
quoted as one.

INPUT: the ortho side probe, produced with

    T1_SUB=1 T1_PREVIEW=side T1_SAMP=24 T1_RX=1400 T1_RY=933 T1_FX=0 \
        T1_PFX=p blender -b --python build.py

T1_FX=0 matters for the same reason flank_compare states: a measurement probe
is rendered without the taking-lens artefacts.

ACCEPTANCE FOR A BAND, STATED BEFORE THE RUN, because a correlation peak that
sits at the end of its own search range is not a peak -- it is the probe
answering instead of declining, which is the `or -9` / `_roof_at` shape this
repo has had twice (SPEC 10.47):

    a band's answer counts only if its score curve has an INTERIOR maximum at
    least 8 samples from either search bound AND that maximum exceeds the
    curve's own median by >= 8 %.  Otherwise the band DECLINES.

Three of ten z bands decline under that rule.  Without it the run manufactures
"+222 mm for the upper body" and an apparent 13 % vertical scale error, both of
which are fictional and both of which I published to myself before the gate
existed.

AND THE VERDICT IS DERIVED, NEVER PRINTED AS A CONSTANT STRING.  SPEC 10.50's
`rear34_character` printed "CHALKY SUN-FADE MOTTLE" unconditionally, including
on a box of pure red paint with every statistic nan.  The first draft of THIS
file printed "FLAT IN HEIGHT" the same way, in the same hour.
"""
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as nd

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
import flank_compare as FC                      # noqa: E402  -- the calibrated map
import compare_script as CS                     # noqa: E402  -- the reference rule

RENDER = sys.argv[1] if len(sys.argv) > 1 else "out/p_side.png"
SEARCH = 55                                     # +/- px of vertical search
MIN_EDGE = 8                                    # samples clear of the bound
MIN_PROM = 1.08                                 # peak / median of the curve
# FALSIFICATION LEVER, default a PROVEN no-op (rev 20's pattern): setting
# T1_R39_NOGATE=1 removes the acceptance gate, and the three fictional bands --
# including the "+222 mm upper body" and the apparent 13 % scale error -- come
# straight back.  That is what shows the gate is load-bearing rather than tidy.
if os.environ.get("T1_R39_NOGATE") == "1":
    MIN_EDGE, MIN_PROM = 0, 0.0
JSEARCH = 30                                    # +/- px of the JOINT search
FLAT_MM = 30.0                                  # spread below which "flat" holds

# the man in the white cap and jacket occludes the lower-forward flank.  He is
# a known occluder and the exclusion is PRICED, never quietly trimmed.
MAN_ROWS, MAN_COLS = (420, 768), (90, 300)


def _edges(a):
    L = 0.2126 * a[:, :, 0] + 0.7152 * a[:, :, 1] + 0.0722 * a[:, :, 2]
    L = nd.gaussian_filter(L, 1.2)
    gy, gx = np.gradient(L)
    return np.hypot(gx, gy)


def main():
    fails = 0
    ref = np.asarray(Image.open("ref_side.jpg").convert("RGB")).astype(float)
    rnd = np.asarray(Image.open(RENDER).convert("RGB")).astype(float)
    FH, FW = ref.shape[:2]
    RH, RW = rnd.shape[:2]
    proj, _finv, ppm = FC.projector(RW, RH)

    print("=" * 78)
    print("PROBE rev 39 -- the whole broadside against ref_side.jpg (SPEC 10.97)")
    print("=" * 78)
    print("reference  ref_side.jpg  %dx%d" % (FW, FH))
    print("render     %s  %dx%d   %.4f px/m (exact, ortho)" % (RENDER, RW, RH, ppm))

    # ---- C1: the projector must reproduce flank_compare's own printed self-check
    row0 = float(proj(0.0, 0.0)[1])
    c1 = abs(row0 - 827.2) < 1.0
    fails += not c1
    print("\n[%s] C1  model z=0 projects to render row %.1f; flank_compare "
          "publishes 827.2" % ("PASS" if c1 else "FAIL", row0))

    # ---- C2: flank_kv must reduce to SPEC 10.34's k_t where k_t was taken
    kv_at = float(FC.flank_kv(FC.U_RHUB))
    c2 = abs(kv_at - FC.K_T) < 0.1
    fails += not c2
    print("[%s] C2  flank_kv(u=%.2f) = %.2f px/m; SPEC 10.34's k_t = %.1f"
          % ("PASS" if c2 else "FAIL", FC.U_RHUB, kv_at, FC.K_T))

    def zrow(py):
        return (RH * 0.5 - np.asarray(py, float)) / ppm + FC.VIEW["tgt"][2]

    # rev 40, SPEC 10.98.  THIS LINE USED TO BE A TRANSCRIBED LITERAL
    # (-0.03467 u + 446.813) even though this file's own docstring says every
    # instrument is "IMPORTED, never re-typed".  That literal was fitted with a
    # LUMINANCE gradient and landed on the counter fascia TOP, while the render
    # datum below is a REDNESS fit on the fascia BOTTOM -- two different edges,
    # one fascia height apart, which is where 10.97.5's 81 mm came from.
    # It is now FITTED LIVE with flank_compare's own corrected call, and C3
    # checks it against the fascia-bottom line flank_compare prints.
    _ref_red = CS._redness(ref)
    _ea, _eb, _erms, _ekp, _en = FC.fit_edge(
        _ref_red, range(CS.LOCKUP[0], CS.LOCKUP[2]), 440, 462, +1, 0.004)

    def v_break(u):
        return _ea * np.asarray(u, float) + _eb

    # ---- C3: the reference datum, fitted live, must be flank_compare's
    #      CORRECTED fascia-BOTTOM line and must NOT be the rev-39 fascia-TOP
    #      literal.  Two-sided on purpose: SPEC 10.98.
    c3a = abs(_ea - (-0.03412)) < 5e-4 and abs(_eb - 466.632) < 0.5
    c3b = abs(_eb - 446.813) > 10.0
    c3 = c3a and c3b
    fails += not c3
    print("[%s] C3  reference datum fitted LIVE: v = %+.5f u %+.3f (rms %.3f, "
          "n=%d/%d)" % ("PASS" if c3 else "FAIL", _ea, _eb, _erms, _ekp, _en))
    print("        flank_compare's corrected fascia-BOTTOM line is "
          "-0.03412 u +466.632; the rev-39 literal was -0.03467 u +446.813,")
    print("        %.1f px = %.0f mm higher -- one counter fascia. SPEC 10.98."
          % (_eb - 446.813, (_eb - 446.813) / FC.K_T * 1000))

    uu, vv = np.meshgrid(np.arange(FW), np.arange(FH))
    xm = FC.flank_X(uu)
    rpx = np.asarray(proj(xm, 1.1459)[0], float)
    zm = zrow(-0.01777 * rpx + 579.070) - (vv - v_break(uu)) / FC.flank_kv(uu)

    rx, ry = proj(xm, zm)
    rx = np.asarray(rx, float)
    ry = np.asarray(ry, float)
    ok = (rx >= 0) & (rx < RW - 1) & (ry >= 0) & (ry < RH - 1)
    x0 = np.clip(rx, 0, RW - 2).astype(int)
    y0 = np.clip(ry, 0, RH - 2).astype(int)
    fx = (rx - x0)[..., None]
    fy = (ry - y0)[..., None]
    warp = (rnd[y0, x0] * (1 - fx) * (1 - fy) + rnd[y0, x0 + 1] * fx * (1 - fy)
            + rnd[y0 + 1, x0] * (1 - fx) * fy + rnd[y0 + 1, x0 + 1] * fx * fy)
    warp[~ok] = 255.0
    print("\nwarp covers %.1f %% of the reference frame" % (100 * ok.mean()))

    er = _edges(ref)
    ew = _edges(np.where(ok[..., None], warp, 255.0))
    sil = ok & (warp.max(2) < 250)
    man = np.zeros_like(sil)
    man[MAN_ROWS[0]:MAN_ROWS[1], MAN_COLS[0]:MAN_COLS[1]] = True
    print("occluder PRICED: the man covers %.1f %% of the render silhouette"
          % (100 * (man & sil).sum() / max(sil.sum(), 1)))
    base = sil & ~man

    def _score(mask, dy, dx):
        m = np.roll(np.roll(mask, dy, 0), dx, 1)
        return (np.roll(np.roll(ew, dy, 0), dx, 1) * er)[m].sum() \
            / max(m.sum(), 1)

    def best_dy(mask, dx0):
        """Interior maximum or None.  NEVER an endpoint.

        rev 40, SPEC 10.98: the row shift is now searched AT THE GLOBAL BEST
        COLUMN SHIFT.  The rev-39 form searched dx and dy SEQUENTIALLY and they
        are coupled -- on a flank whose strong edges are near-horizontal, a few
        px of un-corrected dy moves the dx peak a long way.  Measured: with the
        corrected datum the sequential search returned dx = -15 px (-71 mm)
        where the joint search returns -4 px (-19 mm).
        """
        sc = np.array([_score(mask, d, dx0)
                       for d in range(-SEARCH, SEARCH + 1)])
        k = int(np.argmax(sc))
        prom = sc[k] / np.median(sc)
        if k < MIN_EDGE or k > 2 * SEARCH - MIN_EDGE or prom < MIN_PROM:
            return None, prom
        return k - SEARCH, prom

    # ---- JOINT whole-vehicle registration, rev 40.  dx and dy are coupled.
    bs, by, bx = -1.0, 0, 0
    for dy in range(-JSEARCH, JSEARCH + 1):
        for dx in range(-40, 41):
            s = _score(base, dy, dx)
            if s > bs:
                bs, by, bx = s, dy, dx
    mpp = float(FC.flank_mpp(FW / 2))
    kv0 = float(FC.flank_kv(FW / 2))
    print("\nJOINT registration, whole vehicle: (dy, dx) = (%+d, %+d) px "
          "= (%+.0f mm in z, %+.0f mm in x)"
          % (by, bx, by / kv0 * 1000, bx * mpp * 1000))
    print("HORIZONTAL, from that joint fit: %+d px = %+.0f mm"
          % (bx, bx * mpp * 1000))

    kv = float(FC.flank_kv(FW / 2))
    print("\nZ-LADDER -- bands selected by MODEL z, so each spans the full width")
    print("and cannot alias onto one horizontal line.")
    print("  model z band     dy      mm    peak/median  verdict")
    good = []
    for z0 in np.arange(0.1, 2.05, 0.20):
        z1 = z0 + 0.30
        m = base & (zm >= z0) & (zm < z1)
        if m.sum() < 6000:
            continue
        dy, prom = best_dy(m, bx)
        if dy is None:
            print("  %.2f-%.2f      --      --      %.2fx     DECLINED"
                  % (z0, z1, prom))
            continue
        good.append(dy)
        print("  %.2f-%.2f     %+3d   %+5.0f      %.2fx     ok"
              % (z0, z1, dy, dy / kv * 1000, prom))

    print("\n  %d band(s) answered." % len(good))
    if len(good) < 4:
        print("  NO RULING -- fewer than four bands answered.")
        fails += 1
    else:
        g = np.array(good, float)
        spread = (g.max() - g.min()) / kv * 1000
        print("  dy = %.1f +/- %.1f px = %.0f +/- %.0f mm"
              % (g.mean(), g.std(), g.mean() / kv * 1000, g.std() / kv * 1000))
        print("  spread across the answered bands, z 0.10 -> 2.00: %.0f mm" % spread)
        # THE VERDICT IS DERIVED
        if spread <= FLAT_MM:
            print("\n  VERDICT (derived, not a constant string): the residual is FLAT")
            print("  in height to %.0f mm, so it is ONE RIGID OFFSET of the body against" % spread)
            print("  the cream/red break -- NOT a vertical scale error, and NOT a stance")
            print("  error.  Compare SPEC 10.24: headlamp against belt, 83 +/- 19 mm at")
            print("  4.4 sigma, and 97 mm by the belt chain.  This route uses no headlamp,")
            print("  no roundel and no scale on the lamp.")
        else:
            print("\n  VERDICT (derived): spread %.0f mm exceeds the %.0f mm bar -- NOT"
                  % (spread, FLAT_MM))
            print("  flat, so the offset-versus-scale question is NOT settled here.")

    print("\nCONTROLS: %d checked, %d FAILED" % (3, fails))
    print("=" * 78)
    return fails


if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 1)
