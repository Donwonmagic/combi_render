"""rev 19 -- measure the rendered cream mottle against the re-grounded target.

WHY AN ORTHOGRAPHIC RENDER.  The target spectrum is scale-indexed in PIXELS on
a photograph whose px/m is only bracketed.  On an ORTHO render px/m is exact by
construction (ortho_scale metres across the long axis), so the render side of
the comparison carries no scale uncertainty at all.  All the uncertainty is
then in one stated place: the photograph's px/m on the flank plane.

THE MASK IS GEOMETRY, NOT COLOUR.  A colour gate on a render of the very
surface whose colour is under test would be circular.  The patch is chosen in
MODEL space and projected through the ortho transform, and the transform is
VERIFIED against the rendered alpha extent before it is used.

    T1_SUB=1 T1_MOT_AMP=0.55 blender -b --python mottle_measure.py
"""
import bpy, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
src = open(os.path.join(ROOT, "build.py")).read().split('if os.environ.get("T1_SAVE")')[0]
exec(compile(src, "build.py", "exec"))
import studio as ST
import shader_solve as SS
import t1_core as T
import t1_mats as MT

RES = (int(os.environ.get("T1_MM_W", 2400)), int(os.environ.get("T1_MM_H", 1600)))
SAMP = int(os.environ.get("T1_MM_SAMP", 64))
ORTHO = ST.views()["side"]["ortho"]                     # metres across long axis
PXM = RES[0] / ORTHO                                    # EXACT
AMP = MT.MOTTLE_AMP

# ---- the model-space patch: rear-quarter flank cream ----------------------
# Between the belt line and the drip rail, over the rear quarter, clear of the
# serving apertures (which stop at the aft-most bay) and clear of the tail
# corner roll.  Quoted in model x/z so it cannot drift with a texture.
PX0, PX1 = -1.72, -1.34                                  # model x, metres
def band(x):
    zb = MT.z_belt(x)                                    # above ground
    return zb + 0.035, zb + 0.150                        # clear of the break

def cam():
    v = ST.views()["side"]
    c = bpy.data.objects.get("cam_side") or bpy.context.scene.camera
    ST.aim(c, v["loc"], v["tgt"], v.get("lens"), v.get("ortho"))
    bpy.context.scene.camera = c

body = [bpy.data.objects["T1_body"]]
restore = SS._only(body)
cam()
# ---------------------------------------------------------------- rev 57
# THIS FILE IS NOT MEASURING THE MOTTLE.  F03/F04 ARE NOT MOTTLE FINDINGS.
#
# Rev 56 woke this gate and reported its spectrum as a live fidelity
# comparison of the cream mottle.  It is live.  It is not about the mottle.
# ABLATED, not argued -- five runs, every mottle constant this file's own
# header names, render % of the band-passed patch:
#
#     run                          3.0mm   5.9    11.9   23.7   35.6
#     base  M .024 RGH .62 AMP .55  0.538  1.048  1.861  2.971  3.614
#     T1_MOT_M   = 0.016            0.544  1.055  1.869  2.978  3.616
#     T1_MOT_M   = 0.004  (6x fine) 0.562  1.057  1.857  2.950  3.586
#     T1_MOT_RGH = 0.90             0.544  1.048  1.853  2.956  3.596
#     T1_MOT_AMP = 1.10  (double)   0.573  1.109  1.932  3.045  3.693
#     T1_MOT_AMP = 0.0   (MOTTLE
#                          ENTIRELY OFF) 0.527 1.027 1.837 2.937 3.574
#     the photograph                0.804  1.135  1.455  2.201  3.183
#
# TURNING THE MOTTLE COMPLETELY OFF MOVES THIS GATE BY 1.1-2.0 %.  The gap it
# reports against the photograph is 7.7-35.0 %.  Sweeping MOTTLE_M over a
# factor of six closes 3 points of the 33 at 3 mm; DOUBLING the amplitude
# moves the 23.7 mm row the WRONG WAY, 1.35 -> 1.38.
#
# AT PIXEL LEVEL: out/mottle_alb0.550.png and out/mottle_alb0.000.png differ
# only in the mottle, so their difference IS the mottle.  Render breakup
# sd 4.000 DN; the mottle alone sd 0.2594, peak-to-peak 1.603 -- 6.5 %.
#
# AND THE DIAGNOSIS IN THE REV-57 BRIEF WAS INVERTED.  Painted and looked at:
# probe_scratch/rev57_alb_off.png (mottle removed) is a COARSE CLOUD;
# probe_scratch/rev57_alb_diff.png (the mottle alone) is a FINE SPECKLE.  The
# mottle IS the fine-scale term.  Shrinking MOTTLE_M would have shrunk the
# only fine-scale thing the cream has -- the opposite of what the 3 mm ratio
# asks -- and could not touch the coarse excess, which is not the mottle's.
# DO NOT TUNE MOTTLE_M AGAINST THIS GATE.
#
# WHY, from t1_mats.py: the mottle reaches BASE COLOUR by one path only --
# FADEV_MOTTLE -> WEATHER's FadeVert -> ffac -> the Fac of a HueSaturation
# whose whole authority is W_FADE_SAT 0.88 and W_FADE_VAL 1.04, capped at
# MOTTLE_AMP 0.55.  On a near-white cream that is ~2 % of value; measured,
# 1.603 DN.  Its OTHER half -- ffac * MOTTLE_RGH_K 0.18 added to ROUGHNESS,
# up to 0.099 -- AN ALBEDO PASS CANNOT SEE AT ALL.  This arm is blind to the
# larger half of the mottle by construction, which is why the ablation above
# is so nearly flat.  t1_mats.py asked for exactly this check beside
# FADEV_CREAM -- "its authority over the rendered cream has to be
# demonstrated, not assumed" -- and it had never been run.  It is 6.5 %.
#
# WHAT IS STILL TRUE: something in the render's cream albedo disagrees with
# the photograph by 7.7-35.0 %.  The measurement is real; only its NAME and
# its diagnosis were wrong.  What the other 93.5 % is, is OPEN.
# ---------------------------------------------------------------------------
ALB = os.environ.get("T1_MM_ALBEDO") == "1"
# rev 19: the ALBEDO pass, because a beauty high-pass on a CURVED lit panel
# measures the form shading and the sampler as well as the material.  SPEC
# 10.31's rule for the mural was "solve on the albedo pass, never the beauty
# pixel"; the same applies here.  The beauty arm is kept (T1_MM_ALBEDO unset)
# because the target is a photograph, which is a beauty frame -- both are
# reported rather than one being chosen.
a = SS._render(os.path.join(ROOT, "out", "mottle_%s%0.3f" % ("alb" if ALB else "", AMP)),
               RES, SAMP, transparent=not ALB, albedo=ALB)
if ALB:
    a = np.dstack([a[..., :3], np.ones(a.shape[:2])])
restore()
al = a[..., 3]
if ALB:
    restore2 = SS._only(body); cam()
    _m = SS._render(os.path.join(ROOT, "out", "mottle_mask"), RES, 1, transparent=True)
    restore2()
    al = _m[..., 3]
ys, xs = np.where(al > 0.5)
print("rendered body alpha extent: u %d..%d   v %d..%d" % (xs.min(), xs.max(), ys.min(), ys.max()))

# ---- the ortho transform, DERIVED then VERIFIED --------------------------
# ortho: model x -> u linearly, model z -> v linearly, centred on the camera
# target.  Solve the sign and offset from the body's own known extremes rather
# than trusting a convention.
tgt = ST.views()["side"]["tgt"]
u0 = RES[0] / 2.0; v0 = RES[1] / 2.0
cand = {}
for sgn in (+1, -1):
    ux = lambda x, s=sgn: u0 + s * (x - tgt[0]) * PXM
    cand[sgn] = (ux(T.X_TAIL), ux(2.127))
print("X_TAIL=%.4f -> u %.1f (sgn+) / %.1f (sgn-)" % (T.X_TAIL, cand[1][0], cand[-1][0]))
# the body's aft skin is X_TAIL; pick the sign whose predicted X_TAIL column
# lands on the observed alpha edge
err = {s: min(abs(cand[s][0] - xs.min()), abs(cand[s][0] - xs.max())) for s in cand}
SGN = min(err, key=err.get)
print("chosen sign %+d  (residual %.1f px vs the other %.1f px)"
      % (SGN, err[SGN], err[-SGN]))
if err[SGN] > 12.0:
    raise SystemExit("FATAL: ortho transform does not reproduce the alpha edge "
                     "to 12 px (got %.1f). Refusing to measure." % err[SGN])

U = lambda x: u0 + SGN * (x - tgt[0]) * PXM
V = lambda z: v0 - (z - tgt[2]) * PXM            # v grows downward

ua, ub = sorted([U(PX0), U(PX1)])
zl0, zh0 = band(PX0); zl1, zh1 = band(PX1)
va, vb = sorted([V(max(zh0, zh1)), V(min(zl0, zl1))])
box = (int(ua) + 2, int(ub) - 2, int(va) + 2, int(vb) - 2)
print("patch model x %.3f..%.3f  z %.3f..%.3f -> image u %d-%d v %d-%d"
      % (PX0, PX1, min(zl0, zl1), max(zh0, zh1), *box))

bu0, bu1, bv0, bv1 = box
sub = a[bv0:bv1, bu0:bu1, :3]; sal = al[bv0:bv1, bu0:bu1]
m = sal > 0.99
for _ in range(3):
    q = m.copy()
    q[1:, :] &= m[:-1, :]; q[:-1, :] &= m[1:, :]
    q[:, 1:] &= m[:, :-1]; q[:, :-1] &= m[:, 1:]
    m = q
n = int(m.sum())
lin = SS.srgb_to_lin(sub)
Y = lin @ np.array([0.2126, 0.7152, 0.0722])
clip = float((sub.max(2) >= 0.995)[m].mean()) if n else float("nan")

# rev 56 -- THE REFUSALS ARE HOISTED TO HERE, BEFORE ANYTHING IS PRINTED.
# They used to sit at the very END of the file, after the BASE LEVEL block and
# the character table had already printed their numbers.  So the dead beauty
# arm printed "mean L* 100.00  mean C* 0.00" and a character table of nan and
# 0.000 -- five lines of measurement-shaped output -- and only then refused.
# A refusal that arrives after the numbers is not a refusal.
if n < 2000:
    print("  *** too few px -- refusing to report."); raise SystemExit(0)
# rev 56 -- THE BEAUTY ARM IS DEAD, AND IT REPORTED 0.000 RATHER THAN SAYING SO.
# The first time this file was ever RUN end to end (rev 56; nothing invoked it
# for the 37 revisions it has existed) the beauty arm came back with the patch
# 100.00 % CLIPPED -- mean L* exactly 100.00, mean C* exactly 0.00, every
# high-pass RMS 0.000 and every ratio 0.00 against the target.  The cream band
# renders PURE WHITE: shader_solve._render() never builds a studio rig, and
# mottle_measure execs build.py without T1_PREVIEW, so nothing sets the
# exposure the cream was balanced for.  LOOKED AT, not inferred --
# probe_scratch/rev56_mottle_frame.png is the frame with the patch marked on
# it, and the whole cream band is blown flat.
#
# A run that prints "ratio 0.00" five times looks like a MEASUREMENT of a
# model with no mottle at all.  It is not: it is a measurement of nothing.
# This guard makes it refuse, which is the same rule spectrum() already obeys.
# WATCHED FAILING: the beauty arm (T1_MM_ALBEDO unset) trips it; the ALBEDO
# arm passes it at 0.00 % clipped.
#
# NOT FIXED HERE, AND SAID SO: making the beauty arm live means building the
# studio rig inside this file, which changes what it measures and is rev 57's
# job.  The ALBEDO arm is the better instrument anyway -- this file's own
# docstring says a beauty high-pass on a curved lit panel measures the form
# shading and the sampler as well as the material.
if clip > 0.02:
    print("  *** %.2f %% of the patch is CLIPPED -- REFUSING TO REPORT."
          % (100 * clip))
    print("      A high-pass on a saturated patch is identically zero, and a")
    print("      printed 0.000 would read as 'the model has no mottle'.")
    print("      Cause: shader_solve._render() builds no studio rig, so the")
    print("      cream blows out.  Run the ALBEDO arm instead:")
    print("        T1_SUB=1 T1_MM_ALBEDO=1 blender -b -P mottle_measure.py")
    raise SystemExit(0)
# rev 19: CHROMA structure as well as luminance.  The target character is
# corr(dL*,dC*) NEGATIVE with dC* of the same order as dL* -- so a LUMINANCE
# high-pass alone cannot tell whether the map is working.  The fade path is a
# HueSaturation: it moves chroma far more than it moves luminance, which is
# exactly why the luminance statistic barely responds to it.
def _lab_img(rgb_lin):
    M2 = np.array([[0.4124, 0.3576, 0.1805],
                   [0.2126, 0.7152, 0.0722],
                   [0.0193, 0.1192, 0.9505]])
    XYZ = rgb_lin @ M2.T
    t = XYZ / np.array([0.9505, 1.0, 1.089]); dd = 6 / 29
    f = np.where(t > dd ** 3, np.cbrt(np.clip(t, 1e-9, None)), t / (3 * dd * dd) + 4 / 29)
    L = 116 * f[..., 1] - 16
    A = 500 * (f[..., 0] - f[..., 1]); B = 200 * (f[..., 1] - f[..., 2])
    return L, np.sqrt(A * A + B * B)
Ls, Cs = _lab_img(lin)
# rev 20: the BASE LEVEL, not just the structure.  dC* rms is an ABSOLUTE Lab
# statistic, so it scales with the patch's mean C*.  Comparing a render's dC*
# against a photograph's without also comparing mean C* silently charges a
# base-chroma error to the mottle map.  10.49 measured the photograph's region
# 2 at C* 19.91; this is the same quantity on the render's own patch.
# Photograph side re-measured this revision on `cream_rms._BODY` itself, in
# these same Lab units and with the same D65 white, rather than quoted from a
# comment: n = 7968 px, 0.00 % clipped, mean L* 80.89, mean C* 21.44.
REF_L, REF_C = 80.89, 21.44
print("  --- BASE LEVEL (photograph _BODY, measured: L* %.2f  C* %.2f) ---"
      % (REF_L, REF_C))
print("  render patch mean L* %6.2f   mean C* %6.2f   -> C* ratio %.3f"
      % (Ls[m].mean(), Cs[m].mean(), Cs[m].mean() / REF_C))
print("  --- character on the render, same statistics as the photograph ---")
print("  sigma_mm   corr(dL*,dC*)   dL* rms   dC* rms      [photograph]")
# rev 55 -- THIS NAME WAS ASSIGNED TWICE, TWO LINES APART, AND THE FIRST DICT
# WAS DEAD CODE.  The file therefore carried TWO different sets of "the
# photograph's" figures and silently discarded one, with nothing to say which
# had been measured on what.  NEITHER IS DELETED (rule 16: a figure that lives
# in only one place is not mine to drop) -- the dead one is carried below as
# data, plainly labelled, and only the live one is bound to the name.
#
# WHICH IS WHICH IS NOT ESTABLISHED HERE.  Both were typed into this file by
# an earlier revision without provenance; the LIVE row is simply the one
# Python was using, which is the second.  Re-deriving them is a job for
# whoever next re-runs the photograph side -- see LEDGER_rev55 SS4.
_PHOT_SUPERSEDED = {5.9: (-0.159, 0.377, 0.756), 11.9: (-0.497, 0.531, 1.162),
                    23.7: (-0.698, 0.659, 1.721)}      # DEAD since it was written
PHOT = {5.9: (0.042, 0.385, 0.744), 11.9: (-0.106, 0.493, 1.015),
        23.7: (-0.294, 0.735, 1.295)}                  # the one that was LIVE
for mm, (pc, pl, pcm) in PHOT.items():
    sg = mm * PXM / 1000.0
    hl = Ls - SS.gblur(Ls, sg); hc = Cs - SS.gblur(Cs, sg)
    r = float(np.corrcoef(hl[m], hc[m])[0, 1])
    print("  %6.1f      %+7.3f       %6.3f    %6.3f      [%+.3f  %.3f  %.3f]"
          % (mm, r, hl[m].std(), hc[m].std(), pc, pl, pcm))
print("=" * 74)
print("RENDER MOTTLE  [%s]  MOTTLE_AMP %.3f  RGHK %.3f  M %.4f m  px/m %.2f (EXACT)"
      % ("ALBEDO" if ALB else "beauty", AMP, MT.MOTTLE_RGH_K, MT.MOTTLE_M, PXM))
print("  patch %d x %d, %d px after a 3 px erosion, clipped %.2f %%"
      % (bu1 - bu0, bv1 - bv0, n, 100 * clip))

# target: photograph, region 2, converted at the STATED flank px/m bracket
PXM_REF = float(os.environ.get("T1_PXM_REF", 337.0))
# rev 56 -- TARGET IS DERIVED NOW, NOT TRANSCRIBED.  These five numbers were
# typed literals here and are the output of cream_rms.spectrum(_BODY) on
# ref_rear34.jpg.  Rev 55 verified they still matched BY RUNNING spectrum()
# and reading them off -- which is exactly the check a machine should be doing
# every run, because a literal that agrees today is a literal that goes stale
# silently.  The literals are KEPT as a WATCHED regression baseline (rule 16:
# a figure that lives in one place is not mine to drop) and the delta against
# the live call is PRINTED, so a divergence names itself instead of hiding.
_TARGET_REGRESSION = {1.0: 0.804, 2.0: 1.135, 4.0: 1.455, 8.0: 2.201, 12.0: 3.183}
import cream_rms as _CR
_got = _CR.spectrum(quiet=True)
if _got is None:
    raise SystemExit("mottle_measure: cream_rms.spectrum() REFUSED to report a "
                     "target.  There is no photograph side, so there is no "
                     "comparison.  Refusing to print a ratio against a literal.")
TARGET = {k: 100.0 * v for k, v in _got[0].items()}
_worst = max(abs(TARGET[k] - _TARGET_REGRESSION[k]) for k in _TARGET_REGRESSION)
print("  target DERIVED from cream_rms.spectrum(_BODY) on ref_rear34.jpg: "
      "%s" % ", ".join("%.3f" % TARGET[k] for k in sorted(TARGET)))
print("  worst drift against the rev-19 literals carried here: %.4f pp %s"
      % (_worst, "(they still agree)" if _worst < 0.005 else
         "*** THE LITERALS ARE STALE -- the live call is what is used ***"))
print("  photograph px/m used for the mm axis: %.1f  (flank plane, bracketed"
      " 330-344; NOT the plate's 344.1)" % PXM_REF)
print("   mm      target %    render %   ratio")
for sg_ref, tgt_pct in TARGET.items():
    mm = 1000.0 * sg_ref / PXM_REF
    sg = mm * PXM / 1000.0
    if sg < 0.8:
        print("  %5.1f    %8.3f    (sigma %.2f px too small to measure)" % (mm, tgt_pct, sg))
        continue
    lo = SS.gblur(Y, sg)
    r = 100 * float(np.sqrt((((Y - lo) / np.maximum(lo, 1e-9))[m] ** 2).mean()))
    print("  %5.1f    %8.3f    %8.3f    %5.2f" % (mm, tgt_pct, r, r / max(tgt_pct, 1e-9)))
print("=" * 74)
