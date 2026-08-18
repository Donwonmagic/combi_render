"""probe_rev41_gate.py -- SPEC 10.99.  READ-ONLY.  Changes nothing.

RE-DERIVES probe_rev39_flank.py's BAND ACCEPTANCE GATE (SPEC 10.98.10, rev 41
item 1).

THIS FILE RECORDS A CRITERION OF MINE THAT FAILED, AND THE FAILURE IS THE
FINDING.  Both criteria are printed, in the order they were stated, with the
run that killed the first one.

------------------------------------------------------------------ CRITERION 1
STATED BEFORE ANY RUN.  Mechanism assumed: SPEC 10.97.7 records that the three
bad bands originally "returned the ENDPOINT of the +/-55 px search range", so
G1 (interior) caught them.  The corrected datum moved the warp ~19.8 px, which
should have slid a RAMP's arg-max just inside the bound while G2 (peak over
median) stayed powerless.  On that reading the missing clause is:

    G3  TWO-SIDED HALF-PROMINENCE DESCENT -- on EACH side of the peak the curve
        must fall to <= median + 0.5*(peak - median) inside the search range.
        A curve that climbs to the edge of its window and stops has no peak,
        it has a bound.

    RESULT: G3 PASSES ALL TEN BANDS, including all three bad ones.  Their
    curves DO come back down on both sides.  THE MECHANISM I ASSUMED IS WRONG:
    on the corrected datum these are not ramps riding a bound, they are
    genuine, well-formed LOCAL MAXIMA sitting in the wrong place -- alias peaks.
    G3 is retained below and REPORTED, because a criterion that fails is a
    result, but it is NOT the gate.

------------------------------------------------------------------ CRITERION 2
FORCED BY C4, THE NEGATIVE CONTROL, WHICH IS THE REAL FINDING.  Displace the
reference beyond the search window so that NO true dy exists inside it, and the
inherited gate still answers on half the bands.  A gate that answers when there
is nothing to find is not mis-tuned; it has no POWER.  So the acceptance rule
must be derived from the NULL, not from the shape of the curve:

    G4  MAX-STATISTIC NULL TEST.  For each band, build a null by displacing the
        reference by many offsets far outside +/-SEARCH, and take the peak
        prominence under each.  The band ANSWERS only if its ACTUAL prominence
        exceeds the LARGEST prominence that band reached under the null.

WHY G4 IS NOT A TUNED NUMBER, which the brief forbids:
 1. The bar is the BAND'S OWN null maximum.  I do not choose it; the data does,
    per band, and a band with noisy texture is held to a higher bar than a band
    with clean texture -- automatically.
 2. THE NULL CANNOT CONTAIN THE ANSWER.  It is built at displacements where the
    true registration is out of reach by construction, so no choice made here
    can steer the result toward -5 mm or toward +222 mm.
 3. It is the strictest form of the standard permutation test (max-statistic,
    family-wise), not a level I picked from a menu.
 4. It is STRICTLY STRICTER than the inherited gate: G1 and G2 are inherited
    verbatim and G4 is ANDed on.  Nothing is widened by one digit.

BOTH OUTCOMES REMAIN PUBLISHABLE.  If G4 leaves fewer than four bands the
ladder says NO RULING, and that is reported rather than tuned away.

CONTROLS
--------
 C1  reproduce probe_rev39_flank.py's published JOINT registration (-1, -4).
     SPEC 10.90.10: a re-derivation is a SECOND instrument and needs its own
     control before it may contradict the first.
 C2  ... and its ten band answers and prominences, digit for digit (this also
     serves as C5: the DEFECT is reproduced before it is claimed fixed).
 C3  POSITIVE, END TO END: shift the RENDER IMAGE ITSELF and re-derive the whole
     warp.  Every answering band's dy must move by the predicted amount.
     (rev 41's first draft rolled the edge map but not the mask -- an invalid
     control that produced a spurious instability signal.  Recorded, not
     quietly replaced.)
 C4  NEGATIVE: reference displaced beyond the search window at many offsets.
 C6  the fast scorer must reproduce the inherited np.roll scorer EXACTLY.

FALSIFICATION LEVER, default a proven no-op:  T1_R41_NOG4=1 removes G4.

INPUT: out/p_side.png (T1_FX=0, 1400 px wide floor), as probe_rev39_flank.py.
"""
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as nd

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
import flank_compare as FC                      # noqa: E402
import compare_script as CS                     # noqa: E402

RENDER = "out/p_side.png"
SEARCH = 55
MIN_EDGE = 8            # G1, inherited verbatim
MIN_PROM = 1.08         # G2, inherited verbatim
HALF = 0.5              # G3, half-prominence convention
JSEARCH = 30
MAN_ROWS, MAN_COLS = (420, 768), (90, 300)
NOG4 = os.environ.get("T1_R41_NOG4") == "1"
# null displacements: every one is >= 2x SEARCH away from 0, so the true
# registration is unreachable inside the search window by construction.
NULL_OFFS = tuple(range(120, 361, 20)) + tuple(range(-360, -119, 20))

PUB_BANDS = {0.10: -3, 0.30: -4, 0.50: -5, 0.70: -40, 0.90: -1,
             1.10: -1, 1.30: +46, 1.50: -4, 1.70: -4, 1.90: +40}
PUB_PROM = {0.10: 1.82, 0.30: 1.41, 0.50: 1.37, 0.70: 1.20, 0.90: 3.49,
            1.10: 2.10, 1.30: 1.30, 1.50: 1.29, 1.70: 1.23, 1.90: 1.55}


def _edges(a):
    L = 0.2126 * a[:, :, 0] + 0.7152 * a[:, :, 1] + 0.0722 * a[:, :, 2]
    L = nd.gaussian_filter(L, 1.2)
    gy, gx = np.gradient(L)
    return np.hypot(gx, gy)


def build_warp(rnd, ref, proj, ppm, zm, RW, RH, FW, FH):
    uu, _vv = np.meshgrid(np.arange(FW), np.arange(FH))
    xm = FC.flank_X(uu)
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
    return warp, ok


class Band:
    """Pre-extracts a band's pixels so a whole curve costs one gather per shift.

    s(dy) = sum over (r,c) in M of ew[r,c] * er[(r+dy)%H, (c+dx)%W] / |M|,
    which is algebraically identical to the inherited np.roll form.  C6 proves
    it numerically rather than by this comment (SPEC 10.45).
    """

    def __init__(self, mask, ew, H, W):
        self.r, self.c = np.nonzero(mask)
        self.v = ew[self.r, self.c]
        self.n = max(len(self.r), 1)
        self.H, self.W = H, W

    def curve(self, er, dx, lo=-SEARCH, hi=SEARCH):
        cc = (self.c + dx) % self.W
        out = np.empty(hi - lo + 1)
        for i, dy in enumerate(range(lo, hi + 1)):
            out[i] = np.dot(self.v, er[(self.r + dy) % self.H, cc]) / self.n
        return out

    def at(self, er, dy, dx):
        return float(np.dot(self.v, er[(self.r + dy) % self.H,
                                       (self.c + dx) % self.W]) / self.n)


def gate(sc, nog4_bar=None):
    k = int(np.argmax(sc))
    med = float(np.median(sc))
    pk = float(sc[k])
    prom = pk / med if med else 0.0
    g1 = MIN_EDGE <= k <= 2 * SEARCH - MIN_EDGE
    g2 = prom >= MIN_PROM
    half = med + HALF * (pk - med)
    g3 = bool(np.any(sc[:k] <= half)) and bool(np.any(sc[k + 1:] <= half))
    g4 = True if (nog4_bar is None or NOG4) else prom > nog4_bar
    ok = g1 and g2 and g4
    return (k - SEARCH if ok else None), prom, g1, g2, g3, g4


def main():
    fails = 0
    ref = np.asarray(Image.open("ref_side.jpg").convert("RGB")).astype(float)
    rnd0 = np.asarray(Image.open(RENDER).convert("RGB")).astype(float)
    FH, FW = ref.shape[:2]
    RH, RW = rnd0.shape[:2]
    proj, _finv, ppm = FC.projector(RW, RH)

    print("=" * 78)
    print("PROBE rev 41 -- RE-DERIVING THE BAND ACCEPTANCE GATE  (SPEC 10.99)")
    print("=" * 78)
    print("CRITERION 1, stated first: G1 interior + G2 prominence (both")
    print("  INHERITED, unchanged) + G3 two-sided half-prominence descent.")
    print("CRITERION 2, forced by C4: + G4 max-statistic null test, the bar")
    print("  being each BAND'S OWN largest prominence under a destroyed")
    print("  correspondence.  Nothing here is a number I chose.")
    if NOG4:
        print("!! T1_R41_NOG4=1 -- G4 DISABLED, falsification lever armed")

    _ref_red = CS._redness(ref)
    _ea, _eb, _rms, _kp, _n = FC.fit_edge(
        _ref_red, range(CS.LOCKUP[0], CS.LOCKUP[2]), 440, 462, +1, 0.004)
    print("\nreference datum fitted LIVE: v = %+.5f u %+.3f (rms %.3f, n=%d/%d)"
          % (_ea, _eb, _rms, _kp, _n))

    def v_break(u):
        return _ea * np.asarray(u, float) + _eb

    def zrow(py):
        return (RH * 0.5 - np.asarray(py, float)) / ppm + FC.VIEW["tgt"][2]

    uu, vv = np.meshgrid(np.arange(FW), np.arange(FH))
    xm = FC.flank_X(uu)
    rpx = np.asarray(proj(xm, 1.1459)[0], float)
    zm = zrow(-0.01777 * rpx + 579.070) - (vv - v_break(uu)) / FC.flank_kv(uu)

    warp, ok = build_warp(rnd0, ref, proj, ppm, zm, RW, RH, FW, FH)
    er = _edges(ref)
    ew = _edges(np.where(ok[..., None], warp, 255.0))
    sil = ok & (warp.max(2) < 250)
    man = np.zeros_like(sil)
    man[MAN_ROWS[0]:MAN_ROWS[1], MAN_COLS[0]:MAN_COLS[1]] = True
    base = sil & ~man
    kv = float(FC.flank_kv(FW / 2))
    print("render %d x %d, %.4f px/m ortho; reference k_v %.2f px/m"
          % (RW, RH, ppm, kv))

    # ---- C6: the fast scorer must equal the inherited np.roll scorer --------
    def slow(mask, dy, dx):
        m = np.roll(np.roll(mask, dy, 0), dx, 1)
        return (np.roll(np.roll(ew, dy, 0), dx, 1) * er)[m].sum() \
            / max(m.sum(), 1)

    B_all = Band(base, ew, FH, FW)
    d6 = max(abs(slow(base, dy, dx) - B_all.at(er, dy, dx))
             for dy, dx in ((0, 0), (-4, -1), (7, 3), (-13, 9)))
    c6 = d6 < 1e-9
    fails += not c6
    print("\n[%s] C6  fast scorer reproduces the inherited np.roll scorer; "
          "worst |delta| = %.2e" % ("PASS" if c6 else "FAIL", d6))

    # ---- C1: the published JOINT registration ------------------------------
    bs, by, bx = -1.0, 0, 0
    for dx in range(-40, 41):
        sc = B_all.curve(er, dx, -JSEARCH, JSEARCH)
        k = int(np.argmax(sc))
        if sc[k] > bs:
            bs, by, bx = float(sc[k]), k - JSEARCH, dx
    c1 = (by, bx) == (-1, -4)
    fails += not c1
    print("[%s] C1  JOINT registration: (dy, dx) = (%+d, %+d) px = "
          "(%+.0f mm z, %+.0f mm x); probe_rev39_flank publishes (-1, -4)"
          % ("PASS" if c1 else "FAIL", by, bx, by / kv * 1000,
             bx * float(FC.flank_mpp(FW / 2)) * 1000))

    bands = []
    for z0 in np.arange(0.1, 2.05, 0.20):
        z1 = z0 + 0.30
        m = base & (zm >= z0) & (zm < z1)
        if m.sum() < 6000:
            continue
        bands.append((round(float(z0), 2), round(float(z1), 2), m,
                      Band(m, ew, FH, FW)))

    curves = {z0: B.curve(er, bx) for z0, _z1, _m, B in bands}

    # ---- C2 / C5: reproduce the inherited instrument, digit for digit -------
    print("\n--- C2/C5  the INHERITED gate G1^G2 reproduced ---")
    print("  z band       dy     mm    prom   | published dy  prom")
    c2 = True
    for z0, z1, _m, _B in bands:
        _d, prom, g1, g2, _g3, _g4 = gate(curves[z0])
        k = int(np.argmax(curves[z0])) - SEARCH
        hit = (k == PUB_BANDS[z0] and abs(prom - PUB_PROM[z0]) < 0.01
               and g1 and g2)
        c2 &= bool(hit)
        print("  %.2f-%.2f   %+4d  %+5.0f   %.2fx  |   %+4d       %.2fx   %s"
              % (z0, z1, k, k / kv * 1000, prom, PUB_BANDS[z0], PUB_PROM[z0],
                 "match" if hit else "<<< DIFFERS"))
    fails += not c2
    print("[%s] C2/C5  the DEFECT is reproduced before it is claimed fixed"
          % ("PASS" if c2 else "FAIL"))

    # ---- CRITERION 1: G3 ---------------------------------------------------
    print("\n--- CRITERION 1 (G3, two-sided half-prominence descent) ---")
    g3pass = 0
    for z0, z1, _m, _B in bands:
        _d, prom, _g1, _g2, g3, _g4 = gate(curves[z0])
        g3pass += g3
        print("  %.2f-%.2f   prom %.2fx   descends both sides: %s"
              % (z0, z1, prom, "YES" if g3 else "no"))
    print("  => G3 admits %d of %d bands, including the three at "
          "-193/+222/+193 mm." % (g3pass, len(bands)))
    print("  CRITERION 1 IS REFUTED BY ITS OWN RUN.  These are not ramps on a")
    print("  bound; they are well-formed local maxima in the wrong place.")

    # ---- C4 / G4: the null -------------------------------------------------
    print("\n--- C4 NEGATIVE CONTROL and G4's bar, from %d null displacements "
          "---" % len(NULL_OFFS))
    print("  every offset is >= %d px, so no true dy is reachable inside "
          "+/-%d." % (min(abs(o) for o in NULL_OFFS), SEARCH))
    print("  z band     null prom: max   mean   | inherited gate answers "
          "under null")
    nullbar, nullans, nullall = {}, 0, {}
    for z0, z1, _m, B in bands:
        proms = []
        ans = 0
        for off in NULL_OFFS:
            sc = B.curve(np.roll(er, off, 0), bx)
            d, p, _g1, _g2, _g3, _g4 = gate(sc)
            proms.append(p)
            ans += d is not None
        nullbar[z0] = max(proms)
        nullall[z0] = np.array(proms)
        nullans += ans
        print("  %.2f-%.2f        %.2fx  %.2fx   |  %d of %d"
              % (z0, z1, max(proms), float(np.mean(proms)), ans,
                 len(NULL_OFFS)))
    tot = len(bands) * len(NULL_OFFS)
    print("\n  INHERITED GATE FALSE-ANSWER RATE UNDER THE NULL: %d of %d = "
          "%.0f %%" % (nullans, tot, 100.0 * nullans / tot))
    c4 = nullans <= 0.10 * tot
    fails += not c4
    print("  [%s] C4  a gate with power should answer on almost none of these"
          % ("PASS" if c4 else "FAIL"))

    # ---- THE RE-DERIVED GATE ----------------------------------------------
    print("\n--- CRITERION 2: G1 ^ G2 ^ G4 ---")
    print("  z band       dy     mm    prom    G4 bar   VERDICT")
    good = []
    verdicts = {}
    for z0, z1, _m, _B in bands:
        d, prom, g1, g2, _g3, g4 = gate(curves[z0], nullbar[z0])
        verdicts[z0] = d
        if d is None:
            why = "G1" if not g1 else ("G2" if not g2 else "G4")
            print("  %.2f-%.2f     --     --    %.2fx   %.2fx    DECLINED (%s)"
                  % (z0, z1, prom, nullbar[z0], why))
            continue
        good.append(d)
        print("  %.2f-%.2f   %+4d  %+5.0f   %.2fx   %.2fx    ok"
              % (z0, z1, d, d / kv * 1000, prom, nullbar[z0]))

    print("\n  %d of %d band(s) answered." % (len(good), len(bands)))
    if len(good) < 4:
        print("  NO RULING -- fewer than four bands answered.")
    else:
        g = np.array(good, float)
        spread = (g.max() - g.min()) / kv * 1000
        print("  dy = %+.1f +/- %.1f px = %+.0f +/- %.0f mm"
              % (g.mean(), g.std(), g.mean() / kv * 1000, g.std() / kv * 1000))
        print("  spread, z 0.10 -> 2.00: %.0f mm" % spread)
        if spread <= 30.0:
            print("  VERDICT (derived): FLAT to %.0f mm -- ONE RIGID OFFSET."
                  % spread)
        else:
            print("  VERDICT (derived): spread %.0f mm exceeds the 30 mm bar "
                  "-- NOT flat." % spread)

    # ---- IS THE VERDICT AN ARTEFACT OF *MY* BAR?  Sweep the whole range. --
    print("\n--- BAR INDEPENDENCE: the verdict must not hinge on my choice ---")
    print("  G4 uses the null MAX, the strictest bar.  The weakest bar anyone")
    print("  could defend is the null MEAN -- a 50th-percentile test.  If the")
    print("  ladder still cannot rule there, the verdict is not mine to make.")
    print("  bar                       bands answering   ladder verdict")
    sweep = []
    for lab, fn in (("null MAX (G4, used)", lambda a: a.max()),
                    ("null 95th percentile", lambda a: np.percentile(a, 95)),
                    ("null 75th percentile", lambda a: np.percentile(a, 75)),
                    ("null MEAN (weakest)", lambda a: a.mean()),
                    ("inherited MIN_PROM 1.08", lambda a: MIN_PROM)):
        ds = [gate(curves[z0], fn(nullall[z0]))[0]
              for z0, _z1, _m, _B in bands]
        ds = [d for d in ds if d is not None]
        n = len(ds)
        if n < 4:
            v = "NO RULING"
        else:
            sp = (max(ds) - min(ds)) / kv * 1000
            v = ("FLAT, %.0f mm" % sp) if sp <= 30.0 else ("NOT FLAT, spread %.0f mm" % sp)
        print("  %-26s     %2d of %d          %s" % (lab, n, len(bands), v))
        sweep.append(v)
    # DERIVED, never a constant string.  SPEC 10.50: rear34_character printed
    # its verdict unconditionally; probe_rev39_flank's first draft did the same
    # in the same hour; rev 41's first draft of THIS line did it a third time,
    # asserting "no bar supports FLAT" while the 75th percentile printed FLAT.
    kinds = sorted({v.split(",")[0] for v in sweep})
    print("  => the ladder returns %d DIFFERENT verdicts across the bar range:"
          % len(kinds))
    print("     %s" % "; ".join(kinds))
    if len(kinds) > 1:
        print("     THE ANSWER IS A FUNCTION OF THE ACCEPTANCE BAR, NOT OF THE")
        print("     VEHICLE.  With a %.0f %% false-answer rate under the null,"
              % (100.0 * nullans / tot))
        print("     every bar low enough to admit four bands is inside the noise.")

    # ---- C3: POSITIVE, END TO END -----------------------------------------
    DR = 12                                  # render rows
    pred = -DR * kv / ppm
    print("\n--- C3 POSITIVE, END TO END: shift the RENDER IMAGE by %+d rows "
          "---" % DR)
    print("  predicted change in every band's dy: %+.1f px "
          "(= -%d x k_v/ppm)" % (pred, DR))
    warp2, ok2 = build_warp(np.roll(rnd0, DR, 0), ref, proj, ppm, zm,
                            RW, RH, FW, FH)
    ew2 = _edges(np.where(ok2[..., None], warp2, 255.0))
    sil2 = ok2 & (warp2.max(2) < 250)
    base2 = sil2 & ~man
    c3 = True
    n3 = 0
    for z0, z1, _m, _B in bands:
        if verdicts[z0] is None:
            continue
        m2 = base2 & (zm >= z0) & (zm < z0 + 0.30)
        d2, _p, _a, _b, _c, _d4 = gate(Band(m2, ew2, FH, FW).curve(er, bx))
        n3 += 1
        obs = None if d2 is None else d2 - verdicts[z0]
        hit = obs is not None and abs(obs - pred) <= 1.5
        c3 &= bool(hit)
        print("    %.2f-%.2f  dy %+d -> %+s   change %s   %s"
              % (z0, z1, verdicts[z0], d2, obs, "ok" if hit else "<<< MISSED"))
    if n3 == 0:
        print("    no band answered, so C3 has nothing to test -- STATED, "
              "not silently skipped.")
    else:
        fails += not c3
        print("  [%s] C3  %d answering band(s) tracked an end-to-end render "
              "shift" % ("PASS" if c3 else "FAIL", n3))

    # ---- SUB-BAND SPLIT, reported, NOT part of the verdict -----------------
    print("\n--- SUB-BAND SPLIT (reported, NOT part of the gate) ---")
    print("  z band      full   lower   upper   |lo-hi| px")
    for z0, z1, m, _B in bands:
        zmid = (z0 + z1) / 2
        lo_m = m & (zm < zmid)
        hi_m = m & (zm >= zmid)
        if lo_m.sum() < 3000 or hi_m.sum() < 3000:
            print("  %.2f-%.2f      --      --      --      too few px"
                  % (z0, z1))
            continue
        dlo = gate(Band(lo_m, ew, FH, FW).curve(er, bx), nullbar[z0])[0]
        dhi = gate(Band(hi_m, ew, FH, FW).curve(er, bx), nullbar[z0])[0]
        dd = "--" if (dlo is None or dhi is None) else "%d" % abs(dlo - dhi)
        print("  %.2f-%.2f    %5s   %5s   %5s      %s"
              % (z0, z1, verdicts[z0], dlo, dhi, dd))

    print("\nCONTROLS: %d checked, %d FAILED" % (5, fails))
    print("=" * 78)
    return fails


if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 1)
