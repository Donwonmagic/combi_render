"""probe_ctan_pedestal.py -- READ-ONLY.  What IS the COUNTERTAN pedestal?

rev 26, work item 1.  SPEC 10.70.  Six revisions on the list as "UNIDENTIFIED".

WHAT SPEC 10.56 GOT WRONG, and it is this project's own rule running backwards.
It ablated the dust film, measured the counter top's radiance RISE at
+4.1 / +8.6 / +13.3 %, and concluded "the dust hypothesis is REFUTED -- and it
was HELPING".  That does not follow.  For a mix of coverage `f` and a
base-INDEPENDENT colour `D` over base `A`:

    albedo_eff = (1 - f) * chain(A)  +  f * D
    d(radiance)/d(dust) ~ f * (A - D)      <- what 10.56 measured
    contribution to P   ~ f * D            <- what its conclusion was about

`W_DUST_COL_UP` is (0.5077, 0.3775, 0.2340) and `COUNTERTAN` is
(0.5870, 0.4930, 0.3060) -- the deposit is within 13.5 % of the wood in R.  So
`f*(A-D)` is SMALL *precisely because* the film is nearly the colour of the
base, while `f*D` is LARGE.  Both are true at once.  SPEC 10.68's rule inverted:
A SMALL MAGNITUDE DOES NOT MEAN A SMALL CONTRIBUTION, when the derivative you
measured is not the one your conclusion is about.

THE COVERAGE WAS NEVER HIDDEN.  t1_mats.py:366 says "W_DUST_FAC_UP 0.7313, i.e.
mean coverage 0.548 on the counter top" in plain prose, and a LIVE ASSERT at
t1_mats.py:441 recomputes it on every build.  A base-independent colour at
54.8 % coverage IS a pedestal by construction.

THE LEVER WAS CHECKED BEFORE IT WAS BELIEVED, per 10.56's own rule that a
ray-visibility flag is not an ablation.  The WEATHER group's `Dust` input
reaches dfac -> cdust -> Base Color (t1_mats.py:855, 862, 887) and NOTHING
else; Roughness comes from the fade path (r7), Metallic from the wear path
(steel).  `T1_CTAN_DUST=0` removes the ALBEDO.  `T1_CTAN_WEAR=0` ALSO drops
Metallic, so that arm is TWO levers and is labelled as such below.

HOW THE ARMS WERE PRODUCED.  Each is one full run of `probe_ctan_index.py`
(rev 24's instrument: object-index mask, three controls, null control exact in
every arm).  The env vars must be set per PROCESS because t1_mats reads them at
import, so this file does the FIT and the cross-check, and the arms are
reproduced by re-running the eight commands below.  Every triple here was READ
OFF THE CONSOLE, not typed from memory -- the rule that has caught a violation
in five of the last seven revisions.

    T1_SUB=1 T1_SOLVE_EV=-4 [ARM ENV] blender -b --python probe_ctan_index.py

      ARM ENV per row:
        1  (none)
        2  T1_CTAN=0.02,0.02,0.02
        3  T1_CTAN_WEAR=0
        4  T1_CTAN=0.02,0.02,0.02 T1_CTAN_WEAR=0
        5  T1_CTAN_DUST=0
        6  T1_CTAN=0.02,0.02,0.02 T1_CTAN_DUST=0
        7  T1_CTAN_DUST=0 T1_CTAN_SP=0 T1_CTAN_CT=0
        8  T1_CTAN=0.02,0.02,0.02 T1_CTAN_DUST=0 T1_CTAN_SP=0 T1_CTAN_CT=0

    Read the `top  CLEAN        mask` line from each.

HARNESS CONTROL, and it is what makes the rest readable: the dust-shipped arm
must reproduce SPEC 10.65's published clean pedestal 60.8 / 58.2 / 59.5 %.  It
does, to three significant figures in all three channels, on a tree restored
independently from the bundles.  This file ASSERTS that rather than asserting
it in prose.

Run:  python3 probe_ctan_pedestal.py        (no blender needed -- it is a fit)
Writes nothing.
"""
import sys

A_HI = (0.5870, 0.4930, 0.3060)          # t1_mats.COUNTERTAN
A_LO = (0.02, 0.02, 0.02)                # T1_CTAN near-black arm

# top radiance through rev 24's index-CLEAN mask, one purged rig, EV -4.
# clipped fraction 0.001-0.002 % in every arm; null control exact in every arm.
ARMS = {
    "shipped (dust 1.4, wear .7, spec .32, coat .05)":
        ((0.055051, 0.042708, 0.028070), (0.034200, 0.025571, 0.017433)),
    "wear = 0            (TWO levers: also drops Metallic)":
        ((0.058587, 0.045589, 0.029634), (0.033293, 0.024798, 0.016738)),
    "dust = 0            (pure Base Color ablation)":
        ((0.057265, 0.047109, 0.033222), (0.015820, 0.013219, 0.012062)),
    "dust = 0 AND spec = coat = 0":
        ((0.054738, 0.045416, 0.029736), (0.005333, 0.004718, 0.004308)),
}
SHIPPED = "shipped (dust 1.4, wear .7, spec .32, coat .05)"
DUST_OFF = "dust = 0            (pure Base Color ablation)"

# SPEC 10.65's published clean pedestal -- the harness control.
PUBLISHED_CLEAN = (60.8, 58.2, 59.5)

# t1_mats' own constants, so the cross-check moves if they do.
W_DUST_UP_W, W_DUST_MOT_MEAN, W_DUST_FAC_UP, CTAN_DUST = 0.85, 0.630, 0.7313, 1.4


def fit(r_hi, r_lo):
    """R = k*A + P, per channel, from two albedo points."""
    k = [(h - l) / (ah - al) for h, l, ah, al in zip(r_hi, r_lo, A_HI, A_LO)]
    p = [h - kk * ah for h, kk, ah in zip(r_hi, k, A_HI)]
    frac = [100.0 * pp / h for pp, h in zip(p, r_hi)]
    return k, p, frac


def main():
    print("=" * 78)
    print("COUNTERTAN pedestal -- SPEC 10.70.  R = k*A + P through the clean mask")
    print("=" * 78)
    out = {}
    for tag, (hi, lo) in ARMS.items():
        k, p, frac = fit(hi, lo)
        out[tag] = (k, p, frac)
        print(f"\n{tag}")
        print(f"    k        {tuple(round(v, 6) for v in k)}")
        print(f"    P        {tuple(round(v, 6) for v in p)}")
        print(f"    PEDESTAL {tuple(round(v, 1) for v in frac)} %")

    # ---- HARNESS CONTROL -------------------------------------------------
    got = out[SHIPPED][2]
    print("\n--- HARNESS CONTROL vs SPEC 10.65's published clean pedestal ---")
    print(f"    published {PUBLISHED_CLEAN}")
    print(f"    this fit  {tuple(round(v, 1) for v in got)}")
    bad = [i for i, (g, w) in enumerate(zip(got, PUBLISHED_CLEAN))
           if abs(g - w) > 0.05]
    if bad:
        print("    HARNESS CONTROL FAILED -- this is not 10.65's chain. "
              "NO RESULT BELOW MAY BE READ.")
        return 1
    print("    PASS -- reproduces to three significant figures in all three "
          "channels.")

    # ---- the decomposition ----------------------------------------------
    p_ship = out[SHIPPED][1]
    print("\n--- share of the SHIPPED pedestal removed by each lever ---")
    for tag in ARMS:
        if tag == SHIPPED:
            continue
        p = out[tag][1]
        share = [100.0 * (a - b) / a for a, b in zip(p_ship, p)]
        print(f"    {tag:<54} {tuple(round(v, 1) for v in share)} %")

    # ---- INDEPENDENT CROSS-CHECK, from an unrelated route ----------------
    # A base-independent mix at coverage f dilutes the base by (1-f), so
    # removing it must raise k by 1/(1-f).  f comes from t1_mats' own live
    # assert, NOT from the render.
    f = W_DUST_UP_W * W_DUST_MOT_MEAN * W_DUST_FAC_UP * CTAN_DUST
    k_on, k_off = out[SHIPPED][0], out[DUST_OFF][0]
    ratio = [b / a for a, b in zip(k_on, k_off)]
    print("\n--- INDEPENDENT CROSS-CHECK (t1_mats' constants, not the render) ---")
    print(f"    dust coverage f            = {f:.6f}   "
          "(t1_mats.py:366 prose and its live assert both say 0.548)")
    print(f"    predicted k_off/k_on = 1/(1-f) = {1.0 / (1.0 - f):.3f}")
    print(f"    MEASURED  k_off/k_on           = "
          f"{tuple(round(v, 3) for v in ratio)}")
    print("    Right direction, right magnitude, ~10 % apart. The residual is")
    print("    chain non-linearity (the fade HueSaturation is not linear in")
    print("    saturation) plus interreflection across a 29x albedo secant.")
    print("    AGREEMENT IS CLAIMED TO ~10 %, NOT BETTER.")

    # ---- what is NOT claimed --------------------------------------------
    resid = out["dust = 0 AND spec = coat = 0"][2]
    print("\n--- WHAT IS NOT CLAIMED ---")
    print(f"    A pedestal of {tuple(round(v, 1) for v in resid)} % SURVIVES "
          "dust + spec + coat and is")
    print("    NOT identified. It is small enough to be the ordinary")
    print("    interreflection floor, and that is a hypothesis, not a result.")
    print("    NEVER-ABLATED paths that could carry it, each one render:")
    print("      T1_WORLD=0     the white environment at strength 0.05")
    print("      T1_CYCALB=0    the 0.76 cyclorama the outboard overhang sees")
    print("      T1_GAL_LUM=0   gal_tube, a 2.08 m warm emitter above the run")
    print("      scene->top bounce: gal_warmer and the caddies sit ON the top")
    print("        (hide the object; a visibility flag is barred by 10.56)")
    print("    And the grazing lobe: the counter camera sits ~83 deg off the")
    print("    top's normal, where Schlick on F0 = 0.0256 gives F ~ 0.53. If")
    print("    'Specular IOR Level' = 0 leaves F90 = 1, `T1_CTAN_SP=0` is not")
    print("    a complete specular ablation. UNVERIFIED -- test it before use.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
