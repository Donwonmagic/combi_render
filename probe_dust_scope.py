"""probe_dust_scope.py -- rev 29.  READ-ONLY: builds, measures, prints, exits.

WHAT THIS ASKS
--------------
SPEC 10.81 records the owner's reading that `ref_rear34.jpg` shows the counter
top as CLEAN VARNISHED PLYWOOD.  That contradicts a LIVE ASSERT at
`t1_mats.py:467` which recomputes

    _f_up = W_DUST_UP_W * W_DUST_MOT_MEAN * W_DUST_FAC_UP * 1.4   # counter dust

on every build, and `t1_mats.py:366`'s prose, which reads

    "-> W_DUST_FAC_UP  0.7313, i.e. mean coverage 0.548 on the counter top"

Both describe `W_DUST_FAC_UP` as a COUNTER TOP quantity.  SPEC 10.81 inherits
that framing and reasons about the repair entirely on the counter top.

**THE PROJECT'S OWN RULE IS `CHECK THE LEVER REACHES ONLY WHAT YOU THINK`**
(rev 26, earned on `T1_CTAN_WEAR`, which turned out to be two levers).  It has
never been applied to `W_DUST_FAC_UP` itself.  This probe applies it.

It answers ONE question, BY EXECUTION AND NOT BY READING (rev 24/26's rule):

    WHICH SURFACES OF THE VEHICLE DOES `W_DUST_FAC_UP` ACTUALLY REACH,
    AND HOW MUCH UP-FACING AREA DOES IT FILM?

Nothing here changes a constant, a mesh, a texture or a guard.  The output is
a census.  A census is not a repair and this file does not propose one.

METHOD, AND ITS STATED LIMITS
-----------------------------
* Scene is built by exec'ing `build.py` truncated at its `T1_SAVE` split
  (`build.py:586`), which is `audit.py`'s own idiom.  SPEC 10.78 established
  that this truncation EXCLUDES `ST.cyclorama()` at `build.py:600` -- and also
  the lighting, the camera and `verify`.  **STATED, NOT SILENTLY FIXED.**  It
  excludes NO vehicle geometry and NO material: every `apply_weather()` call
  runs at `t1_mats.py:1826-1864`, far above the split.  Asserted below by mesh
  count against `audit.py`'s published 185.
* Constants are IMPORTED from `t1_mats`, never re-typed (rev 25's rule).
* Areas are measured on the EVALUATED mesh in WORLD space, so modifiers and
  the ride-height shear are included.
* The up-face selector reproduced here is the shipped graph's, read off
  `t1_mats.py:914-916`:  upn = map_range(N.z, W_DUST_NZ_LO, W_DUST_NZ_HI,
  0, 1) ; upw = upn * W_DUST_UP_W.  `motm` is spatial noise whose MEAN is the
  published `W_DUST_MOT_MEAN`; this probe uses that mean exactly as the live
  assert does, so its coverage figures are MEAN coverages and are directly
  comparable with the assert's 0.548.  **A mean is not a station value**
  (rev 26) -- that is why every figure below is labelled `mean`.

CONTROLS -- ALL ASSERTED, so a broken probe cannot print a clean census
----------------------------------------------------------------------
C1  POSITIVE, arithmetic: the coverage this probe computes for `countertan`
    must reproduce the SHIPPED LIVE ASSERT to 1e-12 WHEN FED THE SAME INPUT
    the assert is fed -- the Python literal 1.4.
    **C1 FAILED ON ITS FIRST RUN AT 9.34e-09 AND THE PREMISE WAS MINE**
    (sixth instance in this project of check-the-control's-own-premise).  The
    first cut fed the probe the `dust` value read back off the NODE SOCKET,
    which Blender stores as **float32**: the graph's dust is
    `1.3999999761581421`, not `1.4`.  So the shipped mean coverage the shader
    actually evaluates is `0.54825560066326251` against the assert's
    `0.54825560999999989`.  **THE CAUSE IS FIXED, THE BAND IS NOT WIDENED** --
    C1 now compares like with like at 1e-12, and the float32 round-trip is
    reported separately as C1b, a measured fact rather than a tolerance.
    It is physically irrelevant (1.7e-08 relative).  It is recorded because it
    is a figure nobody has watched.
C1b REPORTED, not asserted: the float32 gap above.
C6  POSITIVE, and it exists because **MY FIRST AREA ESTIMATOR WAS WRONG**.
    The first cut summed `|(v_i - v_0) x (v_{i+1} - v_0)|/2` over a triangle
    fan.  That is correct only for CONVEX polygons.  `counter_top` is a single
    n-gon tracing a U-shaped plan that wraps the tail (`CNT_Y_OUT 1.1660`,
    `CNT_Y_IN 0.8450`, 321 mm plan depth, `t1_detail.py:658-676`), so the fan
    triangles OVERLAP and unsigned magnitudes cannot cancel them.  It reported
    **7.2332 m^2** for a counter top on a 1.750 m wide body, and reported the
    IDENTICAL figure for `counter` -- which is what exposed it, under this
    project's own rule that two rows agreeing exactly are a bug until checked.
    Areas are now Newell (signed, projected on the face normal), which is
    exact for any planar simple polygon, convex or not.  C6 recovers the
    analytic area of a synthetic concave U-gon to 1e-12 **and PRICES the old
    method's error on the same shape** rather than silently dropping it.
C2  POSITIVE, geometric: `counter_top` is a flat up-facing slab, so its
    area-weighted mean up-ramp must be >= 0.95.  If the normal census cannot
    see the one surface everybody agrees faces up, it sees nothing.
C3  NEGATIVE, geometric: the census must DISCRIMINATE -- total up-facing area
    must be a strict minority of total area on a vehicle that is mostly
    flanks.  A census that calls everything up-facing is a constant.
C4  NEGATIVE, structural: at least one material in the scene must carry NO
    WEATHER group, and must be reported as such rather than as coverage 0.
    A probe that cannot answer must say so, not return an endpoint (rev 18).
C5  STRUCTURAL, and it is the finding's backbone: count the DISTINCT WEATHER
    node-trees in the file.  `W_DUST_FAC_UP` is baked into one MULTIPLY node
    inside that group.  If there is exactly ONE tree, every material that
    carries it shares that single node, and the constant is GLOBAL by
    construction -- structure, not inference.

FALSIFICATION ARM (driven from the shell, not from here)
--------------------------------------------------------
    T1_W_DUP=0 blender -b --python probe_dust_scope.py
The override at `t1_mats.py:374` is `T1_W_DUP`.  If the lever were local to the
counter top, only `countertan`'s row would move.  Run both arms and diff.
"""
import bpy, os, sys, math

try:
    ROOT = os.path.dirname(os.path.abspath(__file__))
except NameError:
    ROOT = os.getcwd()
sys.path.insert(0, ROOT)

_src = open(os.path.join(ROOT, "build.py")).read().split(
    'if os.environ.get("T1_SAVE")')[0]
exec(compile(_src, "build.py", "exec"))

import t1_mats as MT

P = print
FAIL = []


def check(ok, label, detail=""):
    P("  [%s] %s%s" % ("PASS" if ok else "FAIL", label,
                       ("  -- " + detail) if detail else ""))
    if not ok:
        FAIL.append(label)


P("\n" + "=" * 74)
P("probe_dust_scope.py -- what does W_DUST_FAC_UP reach?")
P("=" * 74)
P("blender %s" % bpy.app.version_string)
P("build.py exec'd truncated at its T1_SAVE split (build.py:586).")
P("  EXCLUDED by that truncation, stated per SPEC 10.78: ST.cyclorama()")
P("  (build.py:600), ST.lighting(), ST.camera(), verify.run().")
P("  EXCLUDED vehicle geometry: none.  EXCLUDED materials: none.")

# ------------------------------------------------------------ constants
NZ_LO, NZ_HI = MT.W_DUST_NZ_LO, MT.W_DUST_NZ_HI
UP_W, MOT_MEAN = MT.W_DUST_UP_W, MT.W_DUST_MOT_MEAN
FAC_UP = MT.W_DUST_FAC_UP
P("\n--- constants, IMPORTED from t1_mats (never re-typed) ---")
P("  W_DUST_NZ_LO/HI  %.4f / %.4f      (up-normal ramp)" % (NZ_LO, NZ_HI))
P("  W_DUST_UP_W      %.4f" % UP_W)
P("  W_DUST_MOT_MEAN  %.4f" % MOT_MEAN)
P("  W_DUST_FAC_UP    %.4f   <-- the lever under test" % FAC_UP)


def up_ramp(nz):
    """The shipped graph's up-face selector, t1_mats.py:914-916 -> upw."""
    t = (nz - NZ_LO) / (NZ_HI - NZ_LO)
    t = 0.0 if t < 0.0 else (1.0 if t > 1.0 else t)
    return t * UP_W


def poly_area(vs):
    """Newell area of a planar simple polygon in world space.  Signed vector
    sum, magnitude taken ONCE at the end, so a concave loop cancels correctly.
    Exact for convex and concave alike; the fan-of-|cross| it replaces is not
    (see C6)."""
    ax = ay = az = 0.0
    n = len(vs)
    for i in range(n):
        a, b = vs[i], vs[(i + 1) % n]
        ax += a.y * b.z - a.z * b.y
        ay += a.z * b.x - a.x * b.z
        az += a.x * b.y - a.y * b.x
    return 0.5 * math.sqrt(ax * ax + ay * ay + az * az)


def poly_area_fan_abs(vs):
    """The WRONG estimator this probe shipped first, kept so C6 can price it."""
    return sum((vs[i] - vs[0]).cross(vs[i + 1] - vs[0]).length * 0.5
               for i in range(1, len(vs) - 1))


def mean_coverage(dust):
    """Reproduces the live assert's arithmetic with the material's own `dust`.
    t1_mats.py:936-939:  up1 = upw*motm ; fup = up1*FAC_UP ; dfac = fup*dust,
    clamped.  The assert hardcodes dust = 1.4 because that is `countertan`'s."""
    return min(1.0, UP_W * MOT_MEAN * FAC_UP * dust)


# ------------------------------------------------- C5, structural: one group?
trees = sorted(t.name for t in bpy.data.node_groups
               if t.name.startswith("WEATHER"))
P("\n--- C5  STRUCTURAL: distinct WEATHER node-trees in the file ---")
P("  %d: %s" % (len(trees), trees))
check(len(trees) == 1, "C5 exactly ONE shared WEATHER node-tree",
      "so the MULTIPLY node holding W_DUST_FAC_UP is ONE node, shared by "
      "every material spliced with it -- the lever is global BY STRUCTURE")

# ------------------------------------------------ per-material WEATHER census
wmats = {}          # material name -> dust input default
nowx = []           # materials carrying no WEATHER group
for m in bpy.data.materials:
    if not m.use_nodes or m.node_tree is None:
        continue
    g = next((n for n in m.node_tree.nodes
              if n.type == 'GROUP' and n.node_tree is not None
              and n.node_tree.name.startswith("WEATHER")), None)
    if g is None:
        nowx.append(m.name)
        continue
    sock = next((s for s in g.inputs if s.name.lower() == "dust"), None)
    wmats[m.name] = None if sock is None else float(sock.default_value)

P("\n--- C4  NEGATIVE: materials carrying NO WEATHER group ---")
P("  %d of %d node-materials: %s" %
  (len(nowx), len(nowx) + len(wmats), ", ".join(sorted(nowx)[:14]) +
   (" ..." if len(nowx) > 14 else "")))
check(len(nowx) > 0, "C4 at least one material carries no WEATHER group",
      "reported as ABSENT, not as coverage 0")

# ------------------------------------------------- geometry: up-facing area
deps = bpy.context.evaluated_depsgraph_get()
area_tot, area_up, ramp_wsum = {}, {}, {}
obj_up = []                       # (up_area, obj, mat) for the per-object list
for ob in bpy.data.objects:
    if ob.type != 'MESH':
        continue
    ev = ob.evaluated_get(deps)
    me = ev.to_mesh()
    if me is None:
        continue
    M = ob.matrix_world
    N3 = M.to_3x3().inverted_safe().transposed()
    slots = [s.material.name if s.material else None for s in ob.material_slots]
    per_ob = {}
    for poly in me.polygons:
        mat = slots[poly.material_index] if poly.material_index < len(slots) \
            else None
        if mat is None:
            continue
        # world area: |det| is not uniform for sheared objects, so measure the
        # transformed corners directly rather than scaling the local area
        vs = [M @ me.vertices[i].co for i in poly.vertices]
        a = poly_area(vs)
        nz = (N3 @ poly.normal).normalized().z
        r = up_ramp(nz)
        area_tot[mat] = area_tot.get(mat, 0.0) + a
        if r > 0.0:
            area_up[mat] = area_up.get(mat, 0.0) + a
            ramp_wsum[mat] = ramp_wsum.get(mat, 0.0) + a * r
            per_ob[mat] = per_ob.get(mat, 0.0) + a
    for mat, a in per_ob.items():
        obj_up.append((a, ob.name, mat))
    ev.to_mesh_clear()

P("\n--- meshes measured ---")
nm = sum(1 for o in bpy.data.objects if o.type == 'MESH')
# rev 32, SPEC 10.86: 185 -> 186.  THIS CONTROL HAD BEEN FAILING SINCE REV 30.
# rev 30 added `orb_bar` (SPEC 10.83), taking audit.py's published mesh count
# 185 -> 186, and this literal was not swept.  Neither rev 30 nor rev 31 ran
# this file, so nothing reported it; rev 32 found it while validating an owner
# question.  The literal is corrected rather than the check loosened -- the
# check's whole job is to prove the truncated exec built the WHOLE vehicle, and
# a count that is allowed to drift cannot do that job.
# A CONTROL NOBODY RUNS IS NOT A CONTROL.
# rev 38: 186 -> 190.  THIS LITERAL HAS NOW DRIFTED TWICE, IN BOTH DIRECTIONS.
# rev 30 added `orb_bar` (185 -> 186) and did not sweep it; rev 32 found it.
# rev 37 WITHDREW the bar (186 -> 185) and did not sweep it either, so this
# control was firing spuriously on arrival in rev 38 while the brief published
# it as 8/0.  rev 38 adds four wheel houses and a second lid strut (185 -> 190).
# Corrected, not loosened, for the reason the rev-32 comment above already
# gives.  THE RULE THE TWO MISSES SHARE: a revision that MOVES GEOMETRY must
# re-run the probes, exactly as it must re-shoot the hero -- the hero rule was
# written down in rev 37 and this sibling was not.
P("  %d mesh objects (audit.py publishes 190)" % nm)
check(nm == 190, "mesh count matches audit.py's published 190",
      "the truncated exec built the whole vehicle")

AT = sum(area_tot.values())
AU = sum(area_up.values())
P("\n--- C3  NEGATIVE: does the normal census DISCRIMINATE? ---")
P("  total area %.4f m^2 ; up-facing (ramp > 0) %.4f m^2 = %.1f %%"
  % (AT, AU, 100.0 * AU / AT))
check(0.02 < AU / AT < 0.60, "C3 up-facing area is a strict minority",
      "a census that called everything up-facing would be a constant")

# --------------------------------------------------------------- the table
P("\n" + "=" * 74)
P("WHAT W_DUST_FAC_UP FILMS -- every material carrying the shared group")
P("=" * 74)
P("  %-14s %5s %10s %10s %6s %8s %10s" %
  ("material", "dust", "area m2", "up m2", "up %", "mean f", "filmed m2"))
rows = []
for mat in sorted(wmats):
    d = wmats[mat]
    if d is None:
        continue
    at, au = area_tot.get(mat, 0.0), area_up.get(mat, 0.0)
    ws = ramp_wsum.get(mat, 0.0)
    rmean = (ws / au) if au > 0 else 0.0
    f = mean_coverage(d)
    # area actually filmed at the mean = up area x its mean ramp share x f,
    # normalised so a perfectly up-facing surface reports its own area x f
    filmed = au * (rmean / UP_W if UP_W else 0.0) * f
    rows.append((filmed, mat, d, at, au, rmean, f))
    P("  %-14s %5.2f %10.4f %10.4f %5.1f%% %8.4f %10.4f" %
      (mat, d, at, au, (100.0 * au / at if at else 0.0), f, filmed))
rows.sort(reverse=True)

# --------------------------------------------------------------- C1, C2
P("\n--- C6  POSITIVE: the AREA ESTIMATOR, on a known CONCAVE polygon ---")
# A U-gon: outer 4 x 2 rectangle with a 2 x 1 notch cut into its top edge.
# Analytic area = 4*2 - 2*1 = 6.  Convex-fan-of-|cross| cannot cancel the
# notch and must over-report.  Vertices CCW in the z = 0 plane.
from mathutils import Vector as _V
_ugon = [_V(v) for v in ((0, 0, 0), (4, 0, 0), (4, 2, 0), (3, 2, 0),
                         (3, 1, 0), (1, 1, 0), (1, 2, 0), (0, 2, 0))]
_true, _newell, _fan = 6.0, poly_area(_ugon), poly_area_fan_abs(_ugon)
P("  synthetic U-gon, analytic area           : %.12f" % _true)
P("  Newell (this probe now)                  : %.12f" % _newell)
P("  fan-of-|cross| (this probe's FIRST cut)  : %.12f   -> +%.1f %% ERROR"
  % (_fan, 100.0 * (_fan - _true) / _true))
check(abs(_newell - _true) < 1e-12, "C6 Newell area exact on a concave n-gon")
check(abs(_fan - _true) > 1e-6,
      "C6b the retired estimator is DEMONSTRABLY wrong on this shape",
      "priced at +%.1f %%, not silently dropped" % (100.0 * (_fan - _true)
                                                   / _true))

P("\n--- C1  POSITIVE, arithmetic: reproduce the SHIPPED live assert ---")
ct = wmats.get("countertan")
_k = MT.W_DUST_UP_W * MT.W_DUST_MOT_MEAN * MT.W_DUST_FAC_UP
_assert = _k * 1.4                       # exactly what t1_mats.py:467 evaluates
P("  t1_mats.py:467 live assert  0.85*0.630*0.7313*1.4 : %.17f" % _assert)
P("  probe, fed the SAME literal 1.4                   : %.17f"
  % mean_coverage(1.4))
check(abs(mean_coverage(1.4) - _assert) < 1e-12,
      "C1 probe reproduces the live assert like-for-like", "delta < 1e-12")
P("\n--- C1b REPORTED, not asserted: the float32 socket round-trip ---")
P("  `dust` read back off the live node socket         : %.17f" % ct)
P("  the Python literal the assert uses                : %.17f" % 1.4)
P("  coverage the SHADER actually evaluates            : %.17f"
  % mean_coverage(ct))
P("  coverage the ASSERT publishes                     : %.17f" % _assert)
# rev 29: this line divided by `_assert`, which is EXACTLY ZERO in the shipped
# build now that SPEC 10.82 retired the film -- so the probe crashed on the
# very tree it ships with.  Caught on the FRESH-CLONE run, which is the run
# that matters.  A probe that cannot describe the shipped build is not a probe.
# The relative figure is REPORTED WHEN IT EXISTS and DECLINED when it does not
# (SPEC 10.47: a probe that cannot answer must not answer).
_d = mean_coverage(ct) - _assert
if _assert != 0.0:
    P("  delta %.3e  (%.2e relative) -- physically irrelevant, but it is a"
      % (_d, abs(_d) / _assert))
    P("  figure nobody has watched, and the band was NOT widened to hide it.")
else:
    P("  delta %.3e  (relative: N/A -- the assert is exactly 0 since SPEC"
      % _d)
    P("  10.82 retired the film; declined rather than divided by zero).")
    P("  The float32 gap above is retained because it is the figure that")
    P("  WOULD apply if T1_W_DUP restored the retired arm.")

P("\n--- C2  POSITIVE, geometric: counter_top must read as up-facing ---")
ct_up = [(a, o) for a, o, m in obj_up if o == "counter_top"]
ct_a = area_tot.get("countertan", 0.0)
ct_r = (ramp_wsum.get("countertan", 0.0) / area_up["countertan"]) \
    if area_up.get("countertan") else 0.0
P("  countertan up-area %.4f of %.4f m2 ; area-weighted mean ramp %.4f "
  "(ceiling %.4f)" % (area_up.get("countertan", 0.0), ct_a, ct_r, UP_W))
check(ct_r >= 0.95 * UP_W, "C2 counter_top reads as up-facing",
      "the normal census can see the surface everyone agrees faces up")

# --------------------------------------------------------------- the answer
P("\n" + "=" * 74)
P("THE CENSUS")
P("=" * 74)
tot_filmed = sum(r[0] for r in rows)
ct_filmed = next((r[0] for r in rows if r[1] == "countertan"), 0.0)
P("  materials reached by W_DUST_FAC_UP : %d" % len(rows))
P("  total filmed area at the mean      : %.4f m^2" % tot_filmed)
P("  of which `countertan`              : %.4f m^2 = %.1f %%"
  % (ct_filmed, 100.0 * ct_filmed / tot_filmed if tot_filmed else 0.0))
P("  of which EVERYTHING ELSE           : %.4f m^2 = %.1f %%"
  % (tot_filmed - ct_filmed,
     100.0 * (tot_filmed - ct_filmed) / tot_filmed if tot_filmed else 0.0))
P("\n  largest filmed surfaces that are NOT the counter top:")
for a, o, m in sorted((x for x in obj_up if x[2] in wmats),
                      reverse=True)[:14]:
    if o == "counter_top":
        continue
    P("    %-22s %-14s up-area %.4f m^2  (mean f %.4f)"
      % (o, m, a, mean_coverage(wmats[m])))

P("\n" + "=" * 74)
P("CONTROLS: %d checked, %d FAILED  %s"
  % (8, len(FAIL), ("-> " + "; ".join(FAIL)) if FAIL else ""))
P("=" * 74)
P("This probe states a SCOPE.  It does not propose a repair, and it does not")
P("license setting W_DUST_FAC_UP to 0: SPEC 10.81 already bars that on")
P("separate grounds (clean COUNTERTAN is still 34.0 %% short in B).  What it")
P("adds is that the owner's reading is LOCAL to one surface while the lever")
P("is GLOBAL -- which is a second, independent reason a blind f = 0 is wrong,")
P("and it names the surfaces whose dust nobody has ever been asked about.")
if FAIL:
    raise SystemExit("probe_dust_scope: %d control(s) FAILED" % len(FAIL))
