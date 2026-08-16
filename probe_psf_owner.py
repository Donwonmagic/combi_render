"""probe_psf_owner.py -- rev 28, READ-ONLY.  SPEC 10.80.

Publishes a PSF sigma for `ref_workshop.jpg` -- the first this project has been
entitled to publish for that frame -- and, on the way, REFUTES rev 27's
diagnosis of its own threshold-pair spread.

THE OWNER READING THAT UNBLOCKED IT
-----------------------------------
SPEC 10.79 built a VALIDATED slanted-edge estimator and then correctly DECLINED,
because an estimator cannot tell an OCCLUSION STEP from a PAINT BOUNDARY and
that is an owner reading.  rev 27 offered its own reading -- "the first three
sit on the cream/green two-tone break", i.e. the frame is probably unmeasurable
-- and explicitly did NOT rely on it.  **That reading is now REFUTED.**

Shown the fourteen CLUSTERED edges with the estimator's ACTUAL fitted line
drawn on each (rev 27 sent boxes; every box held more than one edge):

  [stated] D1, D2, D3, D4, D6, D7, D8, D9 are PHYSICAL STEPS.
  [stated] D5 is NOT.

D2 is rev 27's E1+E2+E3, which probe_psf_lines.py shows are ONE edge, colinear
to ~0.1 px.  He calls it a step.

THREE FINDINGS, IN THE ORDER THEY WERE FORCED
---------------------------------------------
1. **THE SPREAD IS NOT MIXED EDGE CLASSES.**  rev 27 read its 76 % pooled
   threshold-pair spread as evidence the candidate pool mixed classes.  With
   the classes settled by the owner the spread went UP, to 86 %.  Refuted.
2. **IT IS THE 10-90 ARM'S TAIL SENSITIVITY, and this is reproducible on ONE
   edge.**  On D2's NINE independent member windows -- the identical data --
   the 20-80 arm reads 0.569-0.595 px (4.5 % spread) while the 10-90 arm reads
   0.584-2.203 px (3.8x).  The 10-90 rise reaches into the ESF tails, where
   the profile is contaminated by whatever else lies in the window.  The
   threshold SWEEP is doing its job: it is reporting that one arm is
   unreliable here, not that the measurement is bad.
3. **THE NEGATIVE CONTROL PASSES ONCE THE UNRELIABLE ARM IS DROPPED.**  On the
   pooled figure D5 read SHARPER than the steps and the control FAILED.  On
   the core arms it reads 18.0 % SOFTER -- the direction his identification
   predicts -- with an internal scatter of +-0.017 px, so the 18 % is far
   outside noise.  **The control's premise was contaminated, not his reading.**

D9 IS EXCLUDED AND THE EXCLUSION IS PRICED
------------------------------------------
D9 reads sigma ~3.5 px, 6x every other confirmed step.  It is excluded for a
STATED reason that is not "it disagrees": it is the only candidate whose edge
CARRIES PERIODIC HARDWARE -- the bulb string, three red domes visible sitting
on the rail in the figure -- so the far side of its step is not a uniform
surface, which is the one thing an ESF requires.  It is also n=1.
**Cost of the exclusion, printed every run: +0.176 px, 32 %.**  D1, D4 and D8
could not be measured at all (too few ESF bins, or the monotone test rejected
them) and are named rather than silently dropped.

WHAT IS NOT CLAIMED
-------------------
  * Any metre scale.  A PSF is in PIXELS.  SPEC 10.72 struck both bumper-face
    constants, so the nose/bumper plane has no admissible px/m.
  * That the over-rider tube's 7.9-11.7 px bracket is closed.
  * That D5 IS a paint boundary.  That is the owner's identification; this
    file tests CONSISTENCY with it and finds it, which is weaker.
  * A depth-resolved PSF.  Four edges agree to 12.4 % and that is reported as
    the spread, not explained.

Run:  /tmp/blender/4.5/python/bin/python3.11 probe_psf_owner.py
Writes nothing.
"""
import sys

import numpy as np
import scipy.ndimage as ndi
from PIL import Image

import probe_psf_workshop as P
import probe_psf_lines as L

SRC = "ref_workshop.jpg"

# [stated] by the owner, rev 28, against the fitted lines in
# /tmp/rev28_q2_psf_lines.png.  D-numbering is probe_psf_lines' clustering.
OWNER_STEP = ("D1", "D2", "D3", "D4", "D6", "D7", "D8", "D9")
OWNER_NOT_STEP = ("D5",)
EXCLUDE = ("D9",)                       # reason in the docstring, cost printed
CORE = P.PAIRS[1:]                      # (20-80, 25-75)
TAIL = P.PAIRS[0]                       # 10-90


def arms(img, members):
    out = {p: [] for p in P.PAIRS}
    for c in members:
        x, y, _cos = P.esf_raw(img, c["e"])
        if len(x) < 40:
            continue
        v = [P.rise_sigma(x, y, *p) for p in P.PAIRS]
        if any(t is None for t in v):
            continue
        for p, t in zip(P.PAIRS, v):
            out[p].append(t)
    return out


def pool(a, pairs):
    return [v for p in pairs for v in a[p]]


def main():
    ok = True

    def check(tag, cond, detail=""):
        nonlocal ok
        ok = ok and bool(cond)
        print("  [%s] %-52s %s" % ("PASS" if cond else "FAIL", tag, detail))

    print("=" * 78)
    print("probe_psf_owner.py -- PSF for %s on OWNER-IDENTIFIED edges" % SRC)
    print("=" * 78)

    # ---- P: positive control, AND it must hold on the CORE arms ----------
    # The whole result rests on the core arms, so validating only the pooled
    # estimator would be validating something else.  Both are reported.
    print("\n=== P  POSITIVE CONTROL: recover a KNOWN sigma ===")
    rng = np.random.default_rng(196301)
    worst_core = worst_tail = 0.0
    for s_true in (0.7, 1.2, 1.8):
        yy, xx = np.mgrid[0:160, 0:160]
        step = np.where((xx - 80.0) + 0.14 * (yy - 80.0) > 0, 232.0, 16.0)
        blur = ndi.gaussian_filter(step, s_true) + rng.normal(0, 0.7,
                                                              step.shape)
        edges = [dict(e=e) for e in P.find_edges(blur, [(20, 20, 140, 140)])]
        a = arms(blur, edges)
        gc = float(np.mean(pool(a, CORE))) if pool(a, CORE) else float("nan")
        gt = float(np.mean(a[TAIL])) if a[TAIL] else float("nan")
        ec = abs(gc - s_true) / s_true * 100.0
        et = abs(gt - s_true) / s_true * 100.0
        worst_core = max(worst_core, ec)
        worst_tail = max(worst_tail, et)
        print("     true %.2f  ->  core arms %.3f px (%4.1f %%)   "
              "10-90 arm %.3f px (%4.1f %%)" % (s_true, gc, ec, gt, et))
    check("P  CORE arms recover a known sigma to < 10 %", worst_core < 10.0,
          "worst %.1f %%" % worst_core)
    check("P2 the 10-90 arm also recovers it on a CLEAN synthetic",
          worst_tail < 15.0,
          "worst %.1f %% -- so the 10-90 arm is not broken, it is "
          "TAIL-CONTAMINATED on real windows" % worst_tail)

    # ---- cluster ---------------------------------------------------------
    im = Image.open(SRC).convert("RGB")
    img = P.luma(np.asarray(im, dtype=float))
    raw = P.find_edges(img, None)
    cands = []
    for e in raw:
        a2, b2 = L.endpoints(e)
        cands.append(dict(e=e, a=a2, b=b2, rms=e["rms"], slope=e["slope"],
                          roi=e["roi"], axis=e["axis"]))
    groups = L.cluster(sorted(cands, key=lambda c: c["rms"]))
    order = sorted(range(len(groups)),
                   key=lambda k: min(c["rms"] for c in groups[k]))
    named = {"D%d" % (i + 1): groups[k] for i, k in enumerate(order)}
    print("\n%d candidates -> %d distinct edges (clustering controls live in"
          " probe_psf_lines.py)" % (len(cands), len(groups)))
    check("O  every owner-identified label exists in the clustering",
          set(OWNER_STEP + OWNER_NOT_STEP) <= set(named),
          "%d identified" % len(OWNER_STEP + OWNER_NOT_STEP))

    # ---- finding 2: the arm comparison, on ONE edge ----------------------
    print("\n=== THE 10-90 ARM IS THE UNRELIABLE ONE -- shown on D2 alone ===")
    a2 = arms(img, named["D2"])
    t, c1, c2 = a2[TAIL], a2[CORE[0]], a2[CORE[1]]
    print("     D2, %d independent member windows, IDENTICAL data:" % len(t))
    print("       10-90  %.3f - %.3f px   (ratio %.2fx)"
          % (min(t), max(t), max(t) / min(t)))
    print("       20-80  %.3f - %.3f px   (spread %.1f %%)"
          % (min(c1), max(c1), 100 * (max(c1) - min(c1)) / np.mean(c1)))
    print("       25-75  %.3f - %.3f px   (spread %.1f %%)"
          % (min(c2), max(c2), 100 * (max(c2) - min(c2)) / np.mean(c2)))
    check("T  on one edge, the 10-90 arm scatters far more than the core",
          (max(t) / min(t)) > 3.0 * (max(c1) / min(c1)),
          "%.2fx vs %.2fx" % (max(t) / min(t), max(c1) / min(c1)))

    # ---- the measurement -------------------------------------------------
    keep = [d for d in OWNER_STEP if d not in EXCLUDE]
    per, usable = {}, []
    for d in keep:
        a3 = arms(img, named[d])
        v = pool(a3, CORE)
        if v:
            per[d] = (float(np.mean(v)), float(np.std(v)), len(v))
            usable.append(d)
    core_all = [v for d in usable for v in pool(arms(img, named[d]), CORE)]
    with_d9 = core_all + pool(arms(img, named["D9"]), CORE)

    print("\n=== THE MEASUREMENT -- owner-confirmed steps, CORE arms ===")
    for d in OWNER_STEP:
        if d in per:
            m, s, n = per[d]
            print("     %-3s n=%2d   sigma %.4f +- %.4f px" % (d, n, m, s))
        elif d in EXCLUDE:
            v = pool(arms(img, named[d]), CORE)
            print("     %-3s EXCLUDED  sigma %.3f px -- carries the bulb "
                  "string, n=1 (reason stated, cost priced below)"
                  % (d, np.mean(v)))
        else:
            print("     %-3s NOT MEASURABLE -- too few ESF bins, or the "
                  "monotone test rejected it" % d)
    ms = [per[d][0] for d in usable]
    between = 100.0 * (max(ms) - min(ms)) / float(np.mean(ms))
    print("\n     between-edge spread over %d INDEPENDENT edges: %.1f %%"
          % (len(usable), between))
    check("A  the confirmed steps agree across independent edges",
          between < 20.0, "%.1f %%" % between)

    sig, sd = float(np.mean(core_all)), float(np.std(core_all))
    print("     cost of excluding D9: %+.3f px (%.0f %%)  -- with it, "
          "sigma %.4f +- %.4f"
          % (float(np.mean(with_d9)) - sig,
             100.0 * (float(np.mean(with_d9)) - sig) / sig,
             float(np.mean(with_d9)), float(np.std(with_d9))))

    # ---- N: the owner's own negative control -----------------------------
    print("\n=== N  NEGATIVE CONTROL -- D5, the one edge he did NOT call a"
          " step ===")
    d5 = pool(arms(img, named["D5"]), CORE)
    print("     D5   sigma %.4f +- %.4f px (n=%d)"
          % (np.mean(d5), np.std(d5), len(d5)))
    print("     steps sigma %.4f +- %.4f px (n=%d)" % (sig, sd, len(core_all)))
    check("N  the NON-step edge reads SOFTER than the confirmed steps",
          np.mean(d5) > sig,
          "%.1f %% softer, D5's own scatter only +-%.3f px"
          % (100.0 * (np.mean(d5) - sig) / sig, np.std(d5)))
    print("     NOTE: on the POOLED arms this control FAILED (D5 0.660 vs "
          "0.736).\n           The 10-90 contamination was in the control "
          "too.  Premise fixed,\n           band not widened.")

    print("\n=== RESULT ===")
    print("  ref_workshop.jpg   PSF sigma = %.4f +- %.4f px   FWHM %.3f px"
          % (sig, sd, 2.3548 * sig))
    print("  Basis: %d owner-confirmed occlusion steps (%s), CORE threshold"
          % (len(usable), ", ".join(usable)))
    print("  arms only, n=%d.  D9 excluded and priced.  D1/D4/D8 unmeasurable."
          % len(core_all))
    print("\n--- STILL NOT CLAIMED ---")
    print("  * any metre scale on the nose/bumper plane (SPEC 10.72)")
    print("  * that the over-rider tube's 7.9-11.7 px bracket is closed")
    print("\nRESULT: controls %s" % ("pass" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
