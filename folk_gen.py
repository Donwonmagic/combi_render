"""Flank folk art -- `tex/swirl.png` (show side), `tex/swirl_b.png` (off side)
and `tex/nose.png` (nose front face decal, not yet read by t1_mats.py).

rev 11 -- THE COMPOSITION
=========================
rev 10 hit the coverage and the contrast: cab-door gold 29.09 % against a
measured 29.08 %, gold-to-red luma ratio x2.050 against a measured x2.048.
Held against `ref_side.jpg` it was still visibly wrong, and the failure was
COMPOSITIONAL.  Coverage is a MARGINAL; a generator can match it exactly and
still be wrong, because the same 10 % gold over the same flank can be one
bouquet or five hundred commas.

Measured on `ref_side.jpg` (door rectified into its own plane on
folk_door.md sec.1's four corners; flank in the body plane, painted field
extracted per column, script ink and hardware masked):

    quantity                                 ref_side   rev 10   rev 11
    gold connected components, whole flank       66        95       30
    gold in the LARGEST component               47.8 %    32.4 %   44.9 %
    gold in the largest 3                       84.4 %    67.2 %   92.5 %
    gold in the largest 10                      93.5 %    87.5 %   97.3 %
    components of 300-3000 mm2                   13        47       16
    gold on the open panel X +0.87..-0.62        0.29 %    1.85 %   0.02 %
    gold in the script band, v 0.05-0.75         0.02 %    1.65 %   0.00 %
    gold under the script, v 0.55-1.00           0.04 %    1.93 %   0.00 %
    gold in the top margin, v 0-0.10             0.73 %   16.95 %   0.00 %

Three findings drove the rebuild, and all three are corrections to numbers this
file previously took on trust:

  1. folk_door.md sec.11's mid-flank bins (0.72-3.28 % gold from X +0.74 to
     -0.40) are CONTAMINATED.  That scan swept two fixed body lines and did not
     mask the script.  The counter's BRASS NOSING sits at the top of that band
     (G/R 0.6-0.8, B/R 0.2-0.4) and the script's TARNISHED SILVER LEAF reads
     (85,46,35) = G/R 0.554, B/R 0.419 -- both inside the gold gate
     (G/R >= 0.475, B/R < 0.52), against the folk gold's own B/R of 0.03-0.05.
     Re-measured with the field taken per column below the nosing and the
     script masked on its own B/R signature, the open panel is 0.00-0.14 % gold
     per 0.10 m bin and 0.29 % overall.  SPEC 10.9's original "0.0-0.2 % bare
     red where the script sits" was RIGHT.
  2. The COUNTER hides the top 125 mm of the flank band (t1_detail.CNT_ZB
     1.1470 authored = Z_BELT0 - 0.1250 after the shear; the photograph's
     visible cream->red break sits 124.8 mm below the cab door's belt across
     621 measured columns).  rev 10 authored art into that strip.
  3. The REAR ARCH cuts the band.  rev 10's band ran belt-to-sill everywhere,
     so art placed in band fractions went into the wheel arch.

The generator changed shape as a result.  rev 10 solved 56 independent per-bin
coverage targets by adding small curls from a candidate pool.  That reaches any
coverage profile and cannot reach a composition.  rev 11 places the MEASURED
INVENTORY -- two large connected masses at their measured boxes, four tendrils,
eight rosettes, five dark commas -- and solves SIZES, never counts.

rev 10.  REBUILT against `/home/claude/work/measure/folk_door.md`, which
re-measured the cab door in the DOOR'S OWN PLANE (the door is swung open ~49
deg in `ref_side.jpg`, so every earlier column-scan of "body x" over the door
was sampling the wrong surface).

What that measurement changed
-----------------------------
    quantity                       old generator / SPEC 10.9   folk_door.md
    cab-door gold coverage         0.0 - 0.2 %                 29.08 % +/- 2
    gold / red luma ratio          not controlled              2.048  (core)
    cream rosettes                 "scattered densely", 26     3.90 %, 10 of them
    rosette diameter               random 0.017-0.032 of tile  median 0.072 of
                                                               door width
    dark-brown outline on the door 9 commas scattered over it  0.48 % (<= 2 %)
                                                               -- it is NOT a
                                                               door feature
    dark-brown outline elsewhere   -                           lower nose 2.42 %,
                                                               rear quarter (a
                                                               28 mm stroke
                                                               resolves there)
    gold across the door           flat                        42 % at u < 0.25
                                                               -> 5 % at u > 0.75
    forward flank "bare"           0.0 - 0.2 %                 0.7 - 3.3 %

The old tile was a MOTIF FIELD: motifs at random positions in tile space, with
`t1_mats.body_paint` deciding where they landed on the body via a MapRange
density mask on object X.  That cannot reproduce the measurement, for two
reasons that are structural, not tuning:

  * the mask modulates ALPHA only.  It cannot put dark-brown ink on the lower
    nose and the rear quarter and keep it off the cab door -- that is a
    per-class, per-station statement.
  * the mask is a threshold on a noise field.  It cannot deliver a 42 % -> 5 %
    ramp across a 0.94 m door.

So this generator is now BODY-STATION AWARE.  It knows the object-space -> tile
mapping that `t1_mats.body_paint` applies and paints each motif at the body
station the measurement puts it at.  Density-vs-x and class-vs-x are baked into
the tile.  See MAPPING CONTRACT below -- if those numbers move in t1_mats.py,
this file must be re-run with them.

MAPPING CONTRACT  (t1_mats.body_paint, the `mp` Mapping node + `swirl` BOX)
---------------------------------------------------------------------------
    tile_co   = MAP_LOC + MAP_SCALE * object_position         (Mapping, POINT)
    flank (normal +/-Y) samples (tile_co.x, tile_co.z)        (BOX projection)
    Blender mirrors u on ONE of the two Y faces, which is audit finding
    materials-14 -- the off flank is the show flank mirrored.  See SIDES below.

    u = U0 + SGN * MAP_SCALE * x      v = MAP_LOC[2] + MAP_SCALE * z
    1 texel = 1.878 mm on the body;  the tile period is 3.846 m.

SIDES
-----
`studio.views()` puts hero34f at y = +8.55 (the reference-photo angle, so +Y is
the show flank, the one `ref_side.jpg` shows) and front34 at y = -6.60.  Both
flanks are therefore in the hero set, which is why materials-14 matters.

This file writes TWO tiles with genuinely different compositions, both obeying
the measured statistics:

    tex/swirl.png    show side (+Y), authored for u = 0.815 - 0.26 x
    tex/swirl_b.png  off  side (-Y), authored for u = 0.185 + 0.26 x

`t1_mats.py` must be changed to select between them -- see the block comment at
the bottom of this file.  Until it is, only swirl.png is read and the off side
keeps materials-14.

Verification (run this file; every number is measured with numpy, in BODY
coordinates, by sampling the tile the way the shader samples it):
  * cab door -- class fractions and the 20-bin / 10-bin gold profiles of sec.5
  * lower nose -- sec.10's 11.44 % gold / 2.42 % dark over its own wedge
  * flank -- sec.11's gold/(red+gold) in the report's own X bins
  * contrast -- the tile composited over t1_mats.RED in linear light, Rec.709
    luma on sRGB codes, gold core / cream core / dark core against sec.7;
    and the same tile through the UNPATCHED body_paint, which shows the
    contrast target is blocked there, not here
  * materials-14 -- both tiles sampled onto the same body grid and correlated
    over every shift and both parities, raw and after removing each side's own
    local density (which the two sides are supposed to share)

What is NOT measured, and is flagged as such wherever it is used
----------------------------------------------------------------
  * rear-quarter DARK and CREAM percentages.  folk_door.md gives a dark figure
    for the lower nose (2.42 %) and says a 28 mm dark stroke resolves on the
    rear quarter, but no rear-quarter area fraction.  REAR_DARK / REAR_CREAM
    below are extrapolations from the same painter's hand and are printed with
    the word "extrapolated" against them.
  * the gold density profile DOWN the panel is measured on the door only
    (sec.5).  It is reused as the shape for the rest of the flank.
  * the strip below the cab-door shut line has no measurement of its own; it is
    carried at the near-bare mid-flank rate.
  * rosette internal structure is below the photograph's resolution on the door
    (8-11 px).  sec.4 says to take it from the rear quarter at (890, 545), and
    that is what the rosette() sub-structure is: cream pearl ring, cream
    scalloped ring, gold disc, dark centre.  At 1.878 mm/texel the smallest
    measured rosette (0.031 of door width = 28 mm) resolves to 15 texels, so
    its dark centre is ~2 texels across -- present but at the limit.

Palette
-------
folk_door.md sec.6 is explicit that its sRGB medians are PHOTOGRAPH values, not
albedo.  What is transferable is the CONTRAST, sec.7: gold core reads 2.048x
the adjacent red in luma (Rec.709 weights on sRGB code values), cream 2.348x,
pure dark ink 0.49x.  So the measured chromaticities are kept and their
luminances are solved so that, composited over this project's own measured
livery red (t1_mats.RED), those three ratios come out exactly.
"""
import math
import os
import re
import numpy as np
from PIL import Image, ImageDraw

try:
    from scipy import ndimage
except ImportError:                                   # colour-bleed pass only
    ndimage = None

HERE = os.path.dirname(os.path.abspath(__file__))
TEXDIR = os.path.join(HERE, "tex")

# ===========================================================================
# 1.  MAPPING CONTRACT -- must match t1_mats.body_paint
# ===========================================================================
MAP_LOC = (0.185, 0.410, 0.263)      # Mapping node Location
MAP_SCALE = 0.26                     # Mapping node Scale (uniform)
N = 4096                             # tile size (rev 60b: 2048 -> 4096, SPEC 5 3K floor, F93)
SS = 3                               # supersample factor (0.626 mm sub-texel)
TILE = N * SS
PPM = MAP_SCALE * TILE               # sub-texels per metre = 1597.4

# u = U0 + SGN * MAP_SCALE * x
SIDES = {
    # name        U0                  SGN   file
    "show": (1.0 - MAP_LOC[0], -1.0, "swirl.png"),
    "off":  (MAP_LOC[0],       +1.0, "swirl_b.png"),
}


def check_mapping_contract():
    """Read t1_mats.py (never write it) and warn if the mapping has drifted."""
    p = os.path.join(HERE, "t1_mats.py")
    try:
        src = open(p).read()
    except OSError:
        return
    i = src.find("def body_paint(")
    j = src.find("\ndef ", i + 1) if i >= 0 else -1
    src = src[i:j] if i >= 0 else src
    loc = re.search(r'mp\.inputs\["Location"\]\.default_value\s*=\s*\(([^)]*)\)', src)
    sca = re.search(r'mp\.inputs\["Scale"\]\.default_value\s*=\s*\(([^)]*)\)', src)
    bad = []
    if loc:
        got = tuple(float(t) for t in loc.group(1).split(","))
        if max(abs(a - b) for a, b in zip(got, MAP_LOC)) > 1e-6:
            bad.append("Location %s != MAP_LOC %s" % (got, MAP_LOC))
    if sca:
        got = float(sca.group(1).split(",")[0])
        if abs(got - MAP_SCALE) > 1e-6:
            bad.append("Scale %.4f != MAP_SCALE %.4f" % (got, MAP_SCALE))
    for b in bad:
        print("  !! MAPPING CONTRACT BROKEN: %s -- the baked art will land at "
              "the wrong body station. Update the constants here and re-run."
              % b)


# ===========================================================================
# 2.  BODY GEOMETRY -- read off t1_core.py / t1_shell.py, never imported
#     (importing them needs bpy).  Object-space z == height above ground:
#     step 8b shears the shell by rake_drop(x) = RAKE_Z0 + RAKE_DZDX * x.
# ===========================================================================
# rev 23, SPEC 10.63.  THESE WERE RE-TYPED LITERALS AND ALL FOUR HAD GONE
# STALE -- X_TAIL by 235 mm (rev 16 re-spaced the tail), RAKE_DZDX by
# 15.25 mm/m and RAKE_Z0 / Z_BELT0 by 11.4 mm each (rev 13 re-derived the
# rake).  This is the exact failure family as the dead RIM_R, the dead
# countertan args, _NOSE_SEL and audit.py's hardcoded 4.290: a constant tuned
# against another constant that was not expressed in terms of it (SPEC 10.25).
#
# folk_gen cannot `import t1_core` -- that needs bpy and this is a standalone
# texture generator.  So the values are PARSED OUT with `ast`, which is the
# pattern rev 14 already established for SCR in build.py, and the parse is a
# HARD ERROR rather than a fallback: a silent fallback to a stale literal is
# precisely how this drifted for ten revisions.
def _from_module(fname, names):
    """Read top-level literal assignments out of a sibling module, by AST."""
    import ast as _ast
    src = open(os.path.join(HERE, fname)).read()
    tree = _ast.parse(src)
    found = {}
    for node in tree.body:
        if not isinstance(node, _ast.Assign):
            continue
        tgts = []
        for t in node.targets:
            if isinstance(t, _ast.Name):
                tgts.append((t.id, node.value))
            elif isinstance(t, _ast.Tuple) and isinstance(node.value,
                                                          _ast.Tuple):
                for tt, vv in zip(t.elts, node.value.elts):
                    if isinstance(tt, _ast.Name):
                        tgts.append((tt.id, vv))
        for nm, val in tgts:
            if nm in names:
                try:
                    found[nm] = float(_ast.literal_eval(val))
                except (ValueError, TypeError):
                    pass
    missing = [n for n in names if n not in found]
    if missing:
        raise RuntimeError(
            "folk_gen could not parse %s out of %s. It must NOT fall back to a "
            "re-typed literal -- that is how the bake frame went 235 mm stale "
            "(SPEC 10.63). Fix the parse." % (missing, fname))
    return found


# rev 25, SPEC 10.68.  `_from_module` above can only read a name whose value is
# a bare literal.  The three things this generator STILL re-typed -- the door's
# rear station, the rocker LUT and the arch/tyre radii -- are not bare literals
# in their home modules: `DOOR_GAP`'s rear points are EXPRESSIONS, `BAYS` is a
# comprehension, `B_PILLAR` is an os.environ lookup and `ZB` is wrapped in a
# call.  rev 23 named that as the reason it left them re-typed and said the
# proper parse "is real work and was not done blind at the end of a revision".
#
# This is that work.  `_ceval` is a DELIBERATELY TINY evaluator over the node
# types those definitions actually use -- no attribute access, no imports, no
# arbitrary calls -- so it can read a constant GRAPH without executing the
# module (which would need bpy).  Anything it does not recognise RAISES; a
# silent fallback to a re-typed literal is precisely how this drifted for
# fourteen revisions (SPEC 10.63).
def _ceval(node, ns):
    import ast as _a
    if isinstance(node, _a.Constant):
        return node.value
    if isinstance(node, _a.Name):
        if node.id not in ns:
            raise RuntimeError("folk_gen._ceval: unbound name %r" % node.id)
        return ns[node.id]
    if isinstance(node, _a.Tuple):
        return tuple(_ceval(e, ns) for e in node.elts)
    if isinstance(node, _a.List):
        return [_ceval(e, ns) for e in node.elts]
    if isinstance(node, _a.UnaryOp) and isinstance(node.op, _a.USub):
        return -_ceval(node.operand, ns)
    if isinstance(node, _a.BinOp):
        a, b = _ceval(node.left, ns), _ceval(node.right, ns)
        for op, fn in ((_a.Add, lambda p, q: p + q), (_a.Sub, lambda p, q: p - q),
                       (_a.Mult, lambda p, q: p * q), (_a.Div, lambda p, q: p / q)):
            if isinstance(node.op, op):
                return fn(a, b)
        raise RuntimeError("folk_gen._ceval: unsupported operator")
    if isinstance(node, _a.Subscript):
        return _ceval(node.value, ns)[_ceval(node.slice, ns)]
    if isinstance(node, _a.ListComp):
        if len(node.generators) != 1 or node.generators[0].ifs:
            raise RuntimeError("folk_gen._ceval: only a simple 1-for comp")
        gen = node.generators[0]
        if not isinstance(gen.target, _a.Name):
            raise RuntimeError("folk_gen._ceval: comp target must be a Name")
        out = []
        for v in _ceval(gen.iter, ns):
            sub = dict(ns)
            sub[gen.target.id] = v
            out.append(_ceval(node.elt, sub))
        return out
    if isinstance(node, _a.Call):
        f = node.func
        # float(x) -> x
        if isinstance(f, _a.Name) and f.id == "float":
            return float(_ceval(node.args[0], ns))
        # os.environ.get(VAR, DEFAULT) -> honour the SAME env var t1_shell reads,
        # so a falsification run (T1_BPILLAR=...) moves the art frame with the
        # geometry instead of silently baking against the default.
        if (isinstance(f, _a.Attribute) and f.attr == "get"
                and isinstance(f.value, _a.Attribute) and f.value.attr == "environ"):
            var = _ceval(node.args[0], ns)
            dfl = _ceval(node.args[1], ns)
            return os.environ.get(var, dfl)
        raise RuntimeError("folk_gen._ceval: unsupported call")
    raise RuntimeError("folk_gen._ceval: unsupported node %s"
                       % type(node).__name__)


def _graph_from_module(fname, names, seed=None):
    """Evaluate a module's top-level constant GRAPH for the named values.

    Walks top-level assignments in source order, evaluating each one it can and
    SKIPPING the ones it cannot, so an unrelated definition using bpy or a
    function call never blocks the ones we want.  Raises if any requested name
    is still missing at the end -- never falls back.
    """
    import ast as _a
    src = open(os.path.join(HERE, fname)).read()
    ns = dict(seed or {})
    for node in _a.parse(src).body:
        if not isinstance(node, _a.Assign) or len(node.targets) != 1:
            continue
        tgt = node.targets[0]
        if not isinstance(tgt, _a.Name):
            continue
        try:
            ns[tgt.id] = _ceval(node.value, ns)
        except Exception:
            continue                      # not constant-evaluable; not our concern
    missing = [n for n in names if n not in ns]
    if missing:
        raise RuntimeError(
            "folk_gen could not evaluate %s out of %s. It must NOT fall back to "
            "a re-typed literal -- that is how the door frame went 17.25 mm and "
            "the rocker LUT 76 mm stale (SPEC 10.68). Fix the parse."
            % (missing, fname))
    return {n: ns[n] for n in names}


def _call_arg_from_module(fname, name, fnames):
    """Return the first argument of `name = <fname>( ... )`, literal-evaluated.

    Used for `ZB = aft_lut([...])` in t1_core: the KNOTS are what this generator
    needs, and they are the call's argument, not the name's value.
    """
    import ast as _a
    src = open(os.path.join(HERE, fname)).read()
    for node in _a.parse(src).body:
        if (isinstance(node, _a.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], _a.Name)
                and node.targets[0].id == name
                and isinstance(node.value, _a.Call)
                and isinstance(node.value.func, _a.Name)
                and node.value.func.id in fnames):
            return _a.literal_eval(node.value.args[0]), node.value.func.id
    raise RuntimeError(
        "folk_gen could not find `%s = <%s>(...)` in %s. It must NOT fall back "
        "to a re-typed table (SPEC 10.68)." % (name, "|".join(fnames), fname))


_C = _from_module("t1_core.py", ("RAKE_Z0", "RAKE_DZDX", "X_NOSE",
                                 "X_AXLE_R", "O_NEW", "X_TAIL_OLD",
                                 "TIRE_R"))
RAKE_Z0, RAKE_DZDX = _C["RAKE_Z0"], _C["RAKE_DZDX"]
X_NOSE = _C["X_NOSE"]
# X_TAIL is DERIVED in t1_core (`_aft(X_TAIL_OLD)`) and is not a literal there,
# so it is reconstructed from its DEFINITION -- the rear axle less the measured
# overhang -- rather than re-typed.  Cross-checked against the live mesh at
# -1.8730 when this was written.
X_TAIL = _C["X_AXLE_R"] - _C["O_NEW"]
X_AXLE_R = _C["X_AXLE_R"]
TIRE_R = _C["TIRE_R"]
_O_OLD = _C["X_AXLE_R"] - _C["X_TAIL_OLD"]


def _aft(x):
    """t1_core._aft, re-derived from the SAME parsed constants.

    rev 16 re-spaced every aft LUT knot by its fraction of the rear overhang.
    t1_core applies this inside `aft_lut()`; this generator read the AUTHORED
    knots and never applied it, which is SPEC 10.68's rocker defect.
    """
    if x >= X_AXLE_R:
        return x
    return X_AXLE_R - ((x - X_AXLE_R) / (-_O_OLD)) * _C["O_NEW"]
# Z_BELT0 is the ABOVE-GROUND belt at x = 0: the authored (un-dropped) belt
# less the ride drop at x = 0.  t1_mats derives it exactly this way.
_M = _from_module("t1_mats.py", ("Z_BELT_AUTH",))
Z_BELT0 = _M["Z_BELT_AUTH"] - RAKE_Z0

# cab-door shut line -- PARSED out of t1_shell.DOOR_GAP (authored z, un-sheared)
#
# rev 25, SPEC 10.68.  This was re-typed as `DOOR_X0 = 0.9084` and rev 23
# recorded it as "17.3 mm stale, carried forward".  MEASURED this revision, the
# staleness is 17.250 mm on the rear control point -- but the number that
# matters is the WIDTH: the re-typed DOOR_W was 0.908700 against a true
# 0.891450, i.e. 1.935 % too wide, and DOOR_W is the divisor for every
# u-coordinate of the door art.  That displaced 82.5 % of the door ink by more
# than 2 mm and put 3411 px past the true rear shut line.
#
# The whole outline now comes from t1_shell through `_graph_from_module`, so
# DOOR_X0 is EXPRESSED IN TERMS OF `BAYS[0][1]` exactly as t1_shell expresses
# it, and the B-pillar env override moves the art with the geometry.
_S = _graph_from_module("t1_shell.py",
                        ("BAY_W", "BAY_CX", "BAYS", "B_PILLAR",
                         "_DOOR_REAR_X0", "DOOR_REAR_DX", "DOOR_GAP"))
B_PILLAR = float(_S["B_PILLAR"])
DOOR_REAR_DX = _S["DOOR_REAR_DX"]
_GAP = [(float(x), float(z)) for (x, z) in _S["DOOR_GAP"]]
DOOR_X0 = min(x for x, _ in _GAP)            # latch (aft)
DOOR_X1 = max(x for x, _ in _GAP)            # hinge (fwd)
DOOR_W = DOOR_X1 - DOOR_X0                   # 0.8915 m  (measured 0.94)
# the bottom run is the tail of t1_shell's outline: every point at or below the
# lowest z plus 20 mm, in increasing x.  Read, not re-typed.
_zbot = min(z for _, z in _GAP)
_DOOR_BOT_AUTH = sorted([p for p in _GAP if p[1] <= _zbot + 0.020])
# top rail of the shut line: an AUTHORED scalar, DELIBERATELY NOT PARSED.
#
# rev 25.  I first derived this as the mean z of t1_shell's top run and wrote
# "within 1 mm of the historical 1.8140" in this comment BEFORE watching it
# print.  The print refuted me: the run (1.8020, 1.8130, 1.8150, 1.8130, 1.8060)
# means 1.80980, which is 4.2 mm LOWER, and it would move DOOR_H and with it
# every v-coordinate of the door art.  That is a SECOND lever in the same bake
# and nothing measured says 1.8098 is the better value -- so it is HELD at the
# authored 1.8140, DOOR_H stays bit-identical, and the 4.2 mm discrepancy is
# carried forward as an open item rather than absorbed into an unrelated fix.
# One lever at a time.
#
# rev 26, SPEC 10.73 -- THE 4.2 mm WAS AN ARTEFACT AND THE PRE-PRINT COMMENT WAS
# RIGHT.  1.80980 is the MEAN of a five-knot run whose two end knots are corner
# roll-offs (the rail rises 13 mm off the hinge corner and falls 9 mm into the
# latch corner).  This constant is a HEIGHT AT A STATION, and the DOOR_H line
# below proves it by subtracting rake_drop(1.36) from it.  Compared like for
# like at x = 1.36 on DOOR_GAP_S -- the smoothed outline that actually CUTS the
# geometry -- the outline reads 1.814315 against this 1.8140: 0.315 mm, not 4.2.
# (Raw DOOR_GAP at the same station 1.814333, +0.333 mm; run max 1.814670.)
# The value therefore STAYS, the hold is now for a measured reason rather than a
# cautious one, and NO RE-BAKE IS OWED.  What remains genuinely open is that
# BOTH numbers are authored and the door's true top edge is UNMEASURED -- and
# unmeasurable on the admissible set, since no supplied frame carries both a
# closed cab door and an admissible px/m on the door plane.
_DOOR_TOP_AUTH = 1.8140                      # authored; see SPEC 10.68, 10.73
# rocker / sill bottom -- PARSED from t1_core.ZB's own knots and re-spaced by
# the SAME `_aft()` t1_core applies inside `aft_lut()`.
#
# rev 25, SPEC 10.68.  The re-typed table did two things wrong and only one of
# them mattered.  (a) It never applied `_aft()`, giving 76.222 mm of z error at
# x = X_TAIL -- CONFIRMED exactly, and REFUTED as a defect, because no art is
# painted anywhere aft of x = -1.40: ink-weighted that mechanism is 0.0023 mm.
# (b) It DROPPED FIVE KNOTS (-2.086, -2.050, -1.900, -1.200, +2.085).  The one
# at +2.085 is at the NOSE, where there IS ink: 19.477 mm peak, touching 3.53 %
# of the primary-copy ink, and it is essentially the whole 0.7818 mm
# ink-weighted error.  Parsing the table kills both at once.
_ZB_KNOTS, _ZB_WRAP = _call_arg_from_module("t1_core.py", "ZB",
                                            ("aft_lut", "lut"))
_ZB_AUTH = ([(_aft(x), z) for (x, z) in _ZB_KNOTS] if _ZB_WRAP == "aft_lut"
            else [(x, z) for (x, z) in _ZB_KNOTS])
# the flank proper: outside this the body wraps to the +/-X faces of the box
# projection and a (x, z) authored motif is not what gets sampled.
FLANK_X0, FLANK_X1 = -2.000, 2.030
# no flank op may reach x < XART_LO: at MAP_SCALE 0.26 that wraps onto the
# cab door's hinge edge (x = -2.029 is the same texel as x = +1.817).
XART_LO, XART_HI = -2.026, 2.028


def _lut(tab, x):
    xs = [t[0] for t in tab]
    ys = [t[1] for t in tab]
    return float(np.interp(x, xs, ys))


def rake_drop(x):
    return RAKE_Z0 + RAKE_DZDX * x


def belt_z(x):
    """cream/red break line in object space (t1_mats: Z_BELT0 - RAKE*x)."""
    return Z_BELT0 - RAKE_DZDX * x


def sill_z(x):
    return _lut(_ZB_AUTH, x) - rake_drop(x)


def door_bot_z(x):
    return _lut(_DOOR_BOT_AUTH, x) - rake_drop(x)


DOOR_H = ((_DOOR_TOP_AUTH - rake_drop(1.36)) - door_bot_z(1.36))   # 1.013467 m
# rev 26: this comment read "~1.017 m"; the line computes 1.013467. Another
# figure in a comment that was never watched print.  Corrected, SPEC 10.73.


# --- rev 11: two things the flank band was getting wrong ------------------
#
# (1) THE COUNTER HIDES THE TOP 125 mm OF THE FLANK.  `t1_detail.CNT_ZB` is
#     1.1470 authored; after the shear that is 1.1470 - rake_drop(0) = 1.1105
#     at x = 0, i.e. exactly Z_BELT0 - 0.1250.  And the photograph agrees to
#     the millimetre: the visible cream->red break in `ref_side.jpg` sits at
#     yref 439.45 +/- 0.5 from image x 400 to 920 (measured per column, 621
#     columns), which is 26.35 px = 124.8 mm below the cab door's own belt at
#     yref 413.1.  `build.py:256` puts the counter on `S.SHOW_SIDE` only, so
#     strictly this band is visible on the off flank -- but the composition
#     being replicated was measured UNDER the counter, and inventing art for
#     the strip would breach SPEC 10.10.  Both tiles therefore leave it bare.
#     Whether the body's own two-tone break is at the belt or 125 mm below it
#     is NOT MEASURABLE: the counter covers it in the only photograph that
#     shows this flank.
#
# (2) THE REAR ARCH CUTS THE BAND.  Art authored in band fractions without it
#     goes into the wheel arch, where there is no sheet metal.  Circle taken
#     from the model's own geometry (t1_core.TIRE_R, t1_shell.ARCH_R,
#     t1_core.X_AXLE_R) and cross-checked against the photograph: the arch lip
#     at body X -0.965 measures 0.696 m above ground off `ref_side.jpg`
#     (ground-line datum + the 28.6 mm common-mode correction of RULES 3)
#     against the model's 0.681 m -- 15 mm.  The arch WIDTH does not agree:
#     `analysis/final_numbers.py` reads the opening as 0.952 m off the
#     photograph against the model's 2*ARCH_R = 0.747 m.  That is a
#     pre-existing model/reference discrepancy, not this file's to fix; the
#     model's own circle is used, because the art has to be visible on the
#     body that is actually rendered.
CNT_DROP = 0.1248
# rev 25, SPEC 10.68.  These were three MORE re-typed literals -- the same
# family as the four rev 23 converted, 100 lines below the parse that already
# reads X_AXLE_R into _C and then shadowed it with a bare literal.  All three
# happened to still AGREE when checked, so this is exposure removed, not damage
# repaired, and it is stated that way.  Their provenance comment was also wrong:
# TIRE_R is t1_core.py:80 and ARCH_R is t1_shell.py:254, not :35 / :203.
ARCH_R = _graph_from_module("t1_shell.py", ("ARCH_R",))["ARCH_R"]
# TIRE_R and X_AXLE_R are parsed into _C at the top of section 2.


def arch_top(x):
    """height above ground of the rear wheel-arch lip, or None off the arch."""
    d = x - X_AXLE_R
    if abs(d) >= ARCH_R:
        return None
    return TIRE_R + math.sqrt(ARCH_R * ARCH_R - d * d) - RAKE_DZDX * d


def panel_top(x):
    """top of the VISIBLE painted red field."""
    if x < DOOR_X0:
        return belt_z(x) - CNT_DROP
    return belt_z(x)


def panel_bot(x):
    if DOOR_X0 <= x <= DOOR_X1:
        return door_bot_z(x)
    a = arch_top(x)
    s = sill_z(x)
    return s if a is None else max(s, a)


# ===========================================================================
# 3.  MEASURED TARGETS -- folk_door.md
# ===========================================================================
DOOR_GOLD = 29.08          # sec.3, % of the painted panel
DOOR_CREAM = 3.90
DOOR_DARK = 0.50           # 0.48 measured, bounded <= 2
BELT_MARGIN = 0.052        # sec.5: top tenth of the panel only 4.5 % gold

# sec.5, gold % per bin ACROSS the door, u = 0 (hinge) -> 1 (latch)
DOOR_U_PROFILE = np.array([
    45.4, 53.3, 48.9, 33.2, 29.4, 40.8, 33.4, 46.6, 43.5, 38.6,
    53.1, 36.3, 20.7, 6.4, 20.2, 4.7, 3.1, 8.6, 2.2, 7.0])
# sec.5, gold % per bin DOWN the panel, belt -> bottom
DOOR_V_PROFILE = np.array([
    4.5, 17.7, 20.1, 41.1, 42.0, 37.2, 43.3, 29.2, 34.7, 15.7])

# sec.9 motif map.  u = 0 at the hinge (front) edge, v over the WHOLE door with
# the belt at 0.5058;  d = equivalent-area diameter as a fraction of door width.
BELT_V = 0.5058
# sec.9's `d` is the HORIZONTAL extent as a fraction of door width -- the one
# sec.2 calls exact (vertical mm carry the 5.3 % rectification stretch, which
# is also why the equivalent-area diameters in sec.4 run ~11 % larger).  Their
# median is 0.0718, the figure sec.4 reports.
ROSETTES = [                                     # (u, v, d)
    (0.422, 0.554, 0.0479), (0.585, 0.636, 0.1106), (0.103, 0.780, 0.0766),
    (0.408, 0.824, 0.1138), (0.865, 0.913, 0.0670), (0.196, 0.922, 0.0809),
    (0.552, 0.929, 0.1191), (0.371, 0.935, 0.0628), (0.716, 0.942, 0.0596),
    (0.065, 0.979, 0.0309)]
CURLS = [                                        # (u, v, su, sv)  sec.9
    (0.529, 0.918, 0.172, 0.117), (0.354, 0.925, 0.106, 0.082),
    (0.869, 0.911, 0.096, 0.090), (0.725, 0.944, 0.068, 0.050)]
EDGE_E = (0.988, 0.593, 0.031, 0.095)
DARK_1 = (0.020, 0.591, 0.028, 0.073)

# ===========================================================================
# 3b.  THE FLANK COMPOSITION -- re-measured 2026-08-10 from `ref_side.jpg`
#
# WHY folk_door.md sec.11's scan HAD TO BE RE-DONE.  That scan swept the
# project's two FIXED body lines (`y = 439.45 - 0.0385(x-749.6)` down to
# `y = 594.4 - ...`) and classified everything inside them.  Two things that
# are not folk art fall inside those lines and pass the gold gate
# (G/R >= 0.475, B/R < 0.52):
#
#   * THE COUNTER'S BRASS NOSING.  `t1_detail.counter_nosing` is real brass
#     and `analysis/final_numbers.py` puts it at yref 416.8; the fixed band's
#     top edge at yref 439.45 sits within a few px of it and the JPEG's
#     4:2:2 chroma smears it down across the boundary.  Measured on the strip
#     itself: G/R 0.6-0.8, B/R 0.2-0.4.
#   * THE SCRIPT'S TARNISHED SILVER LEAF.  SPEC 10.21 measures `Senor` at
#     median (85, 46, 35).  That is G/R 0.554, B/R 0.419 -- inside the gold
#     gate.  Re-measured here over the word's own pixels: G/R 0.554,
#     B/R 0.419 (n = 392) against the folk gold's B/R 0.03-0.05 (n = 3640 on
#     the rear-quarter mass).
#
# Re-measured with the painted field extracted PER COLUMN (top = the measured
# cream->red break, which is below the nosing; bottom = the rocker or the arch
# lip), the script masked on its own B/R signature, the hatch man's hand
# masked, the louvre block masked and the field eroded 2 px so its own
# boundary cannot be counted as ink:
#
#   quantity                          sec.11 scan     re-measured
#   gold, X +0.74 .. -0.40            0.72 - 3.28 %   0.00 - 0.14 %
#   gold, whole open panel +0.87..-0.62  ~2 %         0.29 %
#   gold under the script (v .55-1)      ~1.5 %       0.04 %
#
# i.e. SPEC 10.9's original "0.0-0.2 % bare red where the script sits" was
# RIGHT, and sec.11's correction of it was the artefact.  This matters far
# more than 2 percentage points of coverage: a generator told the open panel
# carries 1-3 % gold fills it with small marks, and small marks scattered over
# open red is exactly the failure this rev exists to remove.
# ===========================================================================
FLANK_SCAN = [   # (X centre, gold % of the local visible band, reliable?)
    (+0.850, 3.17, True), (+0.750, 0.00, True), (+0.550, 0.00, True),
    (+0.350, 0.00, True), (+0.150, 0.00, True), (-0.050, 0.00, True),
    (-0.250, 0.00, True), (-0.450, 0.00, True), (-0.550, 0.23, True),
    (-0.650, 6.28, True), (-0.750, 6.06, True), (-0.850, 10.51, True),
    (-0.950, 19.48, True), (-1.050, 26.19, True), (-1.150, 26.81, True),
    (-1.250, 11.08, False), (-1.350, 8.48, False), (-1.450, 12.24, False),
    (-1.550, 13.39, True), (-1.650, 16.28, True), (-1.750, 19.79, True),
    (-1.850, 36.99, True), (-1.950, 37.83, True)]

# Forward of the door the lower nose (sec.10) is 11.44 % gold / 2.42 % dark.
NOSE_GOLD, NOSE_DARK = 11.44, 2.42
FLANK_DENSITY = [           # (x, gold % of the local VISIBLE band)
    (2.108, 11.4), (1.900, 11.4), (1.840, 7.0),
    (1.8171, 29.1),                              # <- the door, sec.3
    (0.9084, 29.1),
    (0.880, 3.2), (0.800, 0.1), (0.550, 0.0), (0.350, 0.0), (0.150, 0.0),
    (-0.050, 0.0), (-0.250, 0.0), (-0.450, 0.0), (-0.550, 0.2),
    (-0.620, 2.0), (-0.650, 6.3), (-0.750, 6.1), (-0.850, 10.5),
    (-0.950, 19.5), (-1.050, 26.2), (-1.150, 26.8), (-1.250, 11.1),
    (-1.350, 8.5), (-1.450, 12.2), (-1.550, 13.4), (-1.650, 16.3),
    (-1.750, 19.8), (-1.850, 37.0), (-1.950, 37.8), (-2.108, 38.0)]

# --- the flank's own v-profile.  folk_door.md sec.5 measures a v-profile on
#     the DOOR only and rev 10 reused it everywhere.  Measured here on the
#     flank itself, in 10 bins of the visible band, v = 0 at the field top:
FLANK_V_REAR = np.array([                        # X -1.45 .. -2.01
    2.84, 3.50, 24.00, 66.11, 54.19, 35.37, 30.26, 31.05, 26.14, 11.13])
FLANK_V_ARCH = np.array([                        # X -0.83 .. -1.45
    0.86, 0.00, 0.00, 0.00, 24.78, 43.59, 39.65, 23.19, 26.29, 25.50])

# --- CLEAR ZONES.  (name, X hi, X lo, v0, v1, measured gold %, tolerance)
CLEAR_ZONES = [
    ("script band  X +0.87..-0.55 v .05-.75", 0.872, -0.55, 0.05, 0.75, 0.02),
    ("under script X +0.60..-0.30 v .55-1.0", 0.600, -0.30, 0.55, 1.00, 0.04),
    ("open panel   X +0.87..-0.62 all v",     0.872, -0.62, 0.00, 1.00, 0.29),
    ("top margin   X +0.87..-2.01 v 0-.10",   0.872, -2.007, 0.00, 0.10, 0.73),
]

# --- COMPOSITION.  Connected components of the gold, `ref_side.jpg`, closed at
#     ~15 mm, door in its own plane and flank in the body plane, on one list.
#     66 components carry 0.2826 m2 of gold.
COMP_TOP = {1: 47.8, 2: 73.7, 3: 84.4, 5: 87.8, 10: 93.5}
COMP_HIST = [                # (bin, n, % of all gold)
    ("<100", 24, 0.42), ("100-300", 21, 1.32), ("300-1k", 3, 0.55),
    ("1k-3k", 10, 5.96), ("3k-10k", 5, 7.32), ("10k-30k", 0, 0.00),
    (">30k", 3, 84.43)]

# --- the measured inventory.  v is a fraction of the VISIBLE band.
#     (id, X0, X1, v0, v1, area mm2, elongation)   X0 = aft end.
FLANK_MASSES = [
    ("MASS-R1  rear-most quarter", -2.007, -1.557, 0.18, 0.96, 73213, 1.35),
    ("MASS-R2  over the rear arch", -1.216, -0.828, 0.40, 0.95, 30285, 1.50)]
FLANK_TENDRILS = [           # (X0, X1, v0, v1, area mm2, elong)
    (-0.861, -0.747, 0.51, 0.91, 5290, 2.08),
    (-1.391, -1.268, 0.72, 0.95, 2578, 3.40),
    (-1.538, -1.476, 0.63, 0.91, 1726, 2.73),
    (-2.007, -1.978, 0.01, 0.17, 1211, 4.02)]
FLANK_ROSETTES = [           # (X centre, v centre, gold-blob area mm2)
    (-0.687, 0.45, 3632), (-1.688, 0.75, 3564), (-1.744, 0.87, 1838),
    (-1.254, 0.75, 1816), (-0.671, 0.91, 1524), (+0.845, 0.81, 1435),
    (-1.444, 0.71, 1076), (-1.848, 0.90, 740)]
# dark-brown ink.  The 0.62 x red gate of sec.3 resolves only the ink's core
# (0.12 % of the flank field); at 0.78 x red -- still well below the red
# ground -- the marks resolve as objects and 5 of them carry 83 % of the dark.
# Both numbers are reported; neither is "the" area, exactly as sec.8 says.
FLANK_DARKS = [              # (X0, X1, v0, v1, area mm2)
    (-0.781, -0.511, 0.60, 0.92, 11881), (-1.429, -1.263, 0.71, 0.93, 8384),
    (-1.784, -1.723, 0.06, 0.26, 4439), (-1.652, -1.538, 0.62, 0.92, 2376),
    (-1.836, -1.794, 0.18, 0.25, 1098)]
# measured zone fractions (visible band, script ink and hardware excluded)
FLANK_GOLD = 10.03           # whole field X +0.872 .. -2.007
OPEN_GOLD = 0.29             # X +0.872 .. -0.62
BOUQ_GOLD = 13.93            # X -0.62 .. -1.45
REAR_GOLD = 27.86            # X -1.45 .. -2.007
# rev 10 carried REAR_DARK 3.0 / REAR_CREAM 4.0 as EXTRAPOLATIONS because
# folk_door.md measures neither.  Both are now measured on the flank itself.
REAR_DARK = 4.21             # X -1.45..-2.01 at the 50 %-ink gate (0.14 at 0.62)
FLANK_DARK = 3.83            # whole field, same gate (0.12 at 0.62)
REAR_CREAM = 1.10            # X -1.45..-2.01


def flank_density(x):
    xs = [t[0] for t in FLANK_DENSITY][::-1]
    ys = [t[1] for t in FLANK_DENSITY][::-1]
    return float(np.interp(x, xs, ys))


def v_profile(pv):
    """gold density multiplier down the panel, pv = 0 at the belt, 1 at the
    bottom.  Measured on the door (sec.5); used as the shape everywhere,
    which is an assumption -- the report measures it on the door only."""
    c = (np.arange(10) + 0.5) / 10.0
    return float(np.interp(pv, c, DOOR_V_PROFILE / DOOR_V_PROFILE.mean()))


def u_profile(ud):
    c = (np.arange(20) + 0.5) / 20.0
    return float(np.interp(ud, c, DOOR_U_PROFILE / DOOR_U_PROFILE.mean()))


# ===========================================================================
# 4.  PALETTE -- chromaticity measured (sec.6), luminance solved for the
#     contrast ratios of sec.7 against this project's own livery red.
# ===========================================================================
RED_LIN = np.array([0.5520, 0.0294, 0.0176])      # t1_mats.RED
LUMA_W = np.array([0.2126, 0.7152, 0.0722])       # Rec.709 on sRGB CODE values


def lin_to_srgb(a):
    a = np.clip(a, 0.0, 1.0)
    return np.where(a <= 0.0031308, a * 12.92, 1.055 * a ** (1 / 2.4) - 0.055)


def srgb_to_lin(a):
    a = np.clip(np.asarray(a, float), 0.0, 1.0)
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)


def code_luma(lin):
    return float(np.dot(lin_to_srgb(np.asarray(lin, float)) * 255.0, LUMA_W))


RED_LUMA = code_luma(RED_LIN)                     # 78.3


def _solve_luma(srgb255, target):
    """scale a measured chromaticity in LINEAR light until its sRGB-code luma
    equals `target`."""
    base = srgb_to_lin(np.asarray(srgb255, float) / 255.0)
    lo, hi = 1e-4, 40.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if code_luma(base * mid) < target:
            lo = mid
        else:
            hi = mid
    return base * (0.5 * (lo + hi))


# class ids used in the label raster
NONE, GOLD, GOLDS, CREAM, DARK = 0, 1, 2, 3, 4
GOLD_CLASSES = (GOLD, GOLDS)

PAL = {
    GOLD:  _solve_luma((194, 146, 6), 2.048 * RED_LUMA),    # sec.7 gold core
    GOLDS: _solve_luma((194, 146, 6), 2.048 * RED_LUMA * 0.88),  # shaded side
    CREAM: _solve_luma((198, 164, 105), 2.348 * RED_LUMA),  # sec.7 rosette
    DARK:  _solve_luma((75, 17, 13), 0.490 * RED_LUMA),     # sec.7 pure ink
}


# ===========================================================================
# 5.  RASTERISER.  Ops are authored in BODY metres (x, z) and drawn through the
#     mapping contract, three times (u-1, u, u+1) so the tile wraps.
# ===========================================================================
class Pen:
    def __init__(self, side, view=None):
        self.U0, self.SGN, _ = SIDES[side]
        # view = (col0, row0, w, h) in sub-texels; None = the whole tile
        self.view = view or (0, 0, TILE, TILE)

    def px(self, x, z):
        u = self.U0 + self.SGN * MAP_SCALE * x
        v = MAP_LOC[2] + MAP_SCALE * z
        return u * TILE - self.view[0], (1.0 - v) * TILE - self.view[1]

    def m(self, d):
        return d * PPM


def _tangents(pts):
    n = len(pts)
    t = []
    for i in range(n):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        t.append((dx / L, dy / L))
    return t


def _stroke_poly(pts, w0, w1, bias=0.0):
    """offset polygon for a tapered stroke through `pts` (already in px)."""
    n = len(pts)
    tg = _tangents(pts)
    left, right = [], []
    for i, (px, py) in enumerate(pts):
        f = i / (n - 1) if n > 1 else 0.0
        w = (w0 + (w1 - w0) * f) * 0.5
        tx, ty = tg[i]
        nx, ny = -ty, tx
        left.append((px + nx * w, py + ny * w))
        right.append((px - nx * w * (1.0 - bias), py - ny * w * (1.0 - bias)))
    return left + right[::-1]


class Raster:
    """label image + the op list that produced it."""

    def __init__(self, pen):
        self.pen = pen
        self.ops = []

    # -- authoring (body metres) -------------------------------------------
    def stroke(self, cls, pts_xz, w0, w1=None, bias=0.0, cap=True):
        self.ops.append(("stroke", cls, list(pts_xz), w0,
                         w0 if w1 is None else w1, bias, cap))

    def disc(self, cls, x, z, r):
        self.ops.append(("disc", cls, x, z, r))

    def poly(self, cls, pts_xz):
        self.ops.append(("poly", cls, list(pts_xz)))

    # -- rasterising --------------------------------------------------------
    def render(self, ops=None):
        pen = self.pen
        w, h = pen.view[2], pen.view[3]
        im = Image.new("L", (w, h), NONE)
        d = ImageDraw.Draw(im)
        for shift in (-TILE, 0, TILE):
            for op in (self.ops if ops is None else ops):
                self._draw(d, op, shift)
        return im

    def _draw(self, d, op, shift):
        pen = self.pen
        kind = op[0]
        if kind == "stroke":
            _, cls, pts, w0, w1, bias, cap = op
            P = [pen.px(x, z) for (x, z) in pts]
            P = [(p[0] + shift, p[1]) for p in P]
            if len(P) < 2:
                return
            a, b = pen.m(w0), pen.m(w1)
            if max(a, b) < 0.7:
                return
            d.polygon(_stroke_poly(P, a, b, bias), fill=cls)
            if cap:
                for (px, py), r in ((P[0], a / 2), (P[-1], b / 2)):
                    if r > 0.4:
                        d.ellipse([px - r, py - r, px + r, py + r], fill=cls)
        elif kind == "disc":
            _, cls, x, z, r = op
            px, py = pen.px(x, z)
            px += shift
            R = pen.m(r)
            if R < 0.35:
                return
            d.ellipse([px - R, py - R, px + R, py + R], fill=cls)
        elif kind == "poly":
            _, cls, pts = op
            P = [pen.px(x, z) for (x, z) in pts]
            d.polygon([(p[0] + shift, p[1]) for p in P], fill=cls)


# ===========================================================================
# 6.  MOTIF VOCABULARY.  Everything is authored in body metres.
# ===========================================================================
def spiral(cx, cz, r0, r1, turns, phase, chir=1, n=64, squash=1.0):
    """logarithmic-ish scroll centreline, body metres."""
    pts = []
    for i in range(n):
        f = i / (n - 1)
        t = phase + chir * turns * 2 * math.pi * f
        r = r0 * (r1 / r0) ** f
        pts.append((cx + r * math.cos(t), cz + r * math.sin(t) * squash))
    return pts


def arc(x0, z0, x1, z1, bow, n=32):
    """a bowed line from (x0,z0) to (x1,z1); bow is the sagitta in metres."""
    dx, dz = x1 - x0, z1 - z0
    L = math.hypot(dx, dz) or 1.0
    nx, nz = -dz / L, dx / L
    pts = []
    for i in range(n):
        f = i / (n - 1)
        s = math.sin(math.pi * f) * bow
        pts.append((x0 + dx * f + nx * s, z0 + dz * f + nz * s))
    return pts


def acanthus_scroll(R, cx, cz, size, chir=1, phase=0.0, w=0.055,
                    eyes=(0.30, 0.62), shade=True, dark=0.0):
    """A fat gold C-scroll with rolled end and two inner eye curls -- the
    dominant element of the vocabulary.  `dark` > 0 lays a dark keyline under
    it (rear quarter / lower nose only)."""
    # 0.60 turns from full radius down to a third of it, with the stroke
    # tapering to a fifth: a C-scroll with a rolled end, not a filled disc.
    main = spiral(cx, cz, size, size * 0.34, 0.60, phase, chir)
    if dark > 0:
        R.stroke(DARK, main, w + 2 * dark, w * 0.22 + 2 * dark)
    if shade:
        sh = [(x, z - w * 0.26) for (x, z) in main]
        R.stroke(GOLDS, sh, w * 1.06, w * 0.26)
    R.stroke(GOLD, main, w, w * 0.22)
    # the rolled tip: a short tight coil carrying on from the scroll's end
    tipx, tipz = main[-1]
    roll = spiral(tipx + chir * size * 0.10 * math.cos(phase + 3.4),
                  tipz + size * 0.10 * math.sin(phase + 3.4),
                  size * 0.12, size * 0.03, 0.70, phase + 3.4, chir)
    R.stroke(GOLD, roll, w * 0.30, w * 0.10)
    for f in eyes:
        i = int(f * (len(main) - 1))
        ex, ez = main[i]
        e = spiral(ex, ez, size * 0.34, size * 0.07, 0.66, phase + 2.2, -chir)
        R.stroke(GOLD, e, w * 0.38, w * 0.11)
    return main


def leaf(R, x0, z0, x1, z1, bow, w, cls=GOLD, dark=0.0):
    """a tapered acanthus leaf / tendril."""
    p = arc(x0, z0, x1, z1, bow)
    if dark > 0:
        R.stroke(DARK, p, w + 2 * dark, 2 * dark)
    R.stroke(cls, p, w, w * 0.10)
    return p


def curl(R, cx, cz, size, chir=1, phase=0.0, w=0.030, dark=0.0):
    p = spiral(cx, cz, size * 0.92, size * 0.12, 0.85, phase, chir)
    if dark > 0:
        R.stroke(DARK, p, w + 2 * dark, w * 0.25 + 2 * dark)
    R.stroke(GOLD, p, w, w * 0.25)
    return p


def _seg(R, cls, run, w0, w1, n):
    """draw one surviving run of a clipped stroke, keeping its own taper."""
    f0 = run[0][0] / max(n - 1, 1)
    f1 = run[-1][0] / max(n - 1, 1)
    R.stroke(cls, [q for _, q in run],
             w0 + (w1 - w0) * f0, w0 + (w1 - w0) * f1)


def bouquet(R, x0, x1, z0, z1, w, chir=1, phase=0.0, head=-1, keep=None,
            rich=1.0, nvol=5, ncurl=4, leaves=3, tail=True, lat=0.0,
            jit=None, bow=0.50, wf=1.15):
    """ONE CONNECTED MASS filling the box (x0..x1, z0..z1).

    This is the element the photograph is built from and rev 10 did not have.
    Every stroke starts ON the spine, so the whole thing rasterises as a SINGLE
    connected component -- which is what makes "the largest component carries
    48 % of all the gold" reachable at all.

    Shape read off `ref_rear34.jpg`'s rear quarter, which resolves this mass at
    roughly twice `ref_side.jpg`'s sampling: a broad tapering paisley body
    sweeping corner to corner, a rolled C-scroll HEAD, C-scroll volutes budding
    off the head half of the spine, small curls, two leaves and a thin tail.

    Two proportions decide whether this reads as signwriting or as a worm, and
    rev 11 got both wrong before getting them right:

      * a spiral needs RADIUS >= ~2.8x its own stroke width or it rasterises as
        a filled disc.  `w` is therefore clamped to 0.22 R0 and the AREA is
        bought with stroke LENGTH -- more elements -- not with width.
      * the measured mass is not centred in its own box: component 1 of
        `ref_side.jpg` has its centroid 0.675 of the way from the forward edge
        to the aft edge.  The head sits deep in the head-end quarter and the
        volutes hang off the head half of the spine.

    `keep(x, z) -> bool` vetoes a point; strokes are CLIPPED to the allowed
    region, never dropped whole (section 8, the lower nose's shared texels).
    """
    cx, cz = 0.5 * (x0 + x1), 0.5 * (z0 + z1)
    hx, hz = 0.5 * (x1 - x0), 0.5 * (z1 - z0)
    # R0 sets every scroll's radius.  min(hx, hz) starves a wide flat box (the
    # mass over the rear arch is 388 x 244 mm), so use the geometric mean and
    # cap each scroll against the box height instead.
    # per-side phase / placement jitter.  The two flanks must carry the SAME
    # measured composition (same boxes, same areas, same aft-weighted
    # centroid), so the only room left for decorrelation is INSIDE each mass:
    # every scroll's phase and every volute's seat are re-drawn per side.
    def J(a=1.0):
        return 0.0 if jit is None else float(jit.uniform(-a, a))

    R0 = math.sqrt(hx * hz)
    w = min(w * (0.72 + 0.28 * min(rich, 1.8)), R0 * 0.22)

    def put(cls, p, aa, bb):
        if keep is None:
            R.stroke(cls, p, aa, bb)
            return
        run, n = [], len(p)
        for i, (px, pz) in enumerate(p):
            if keep(px, pz):
                run.append((i, (px, pz)))
                continue
            if len(run) > 3:
                _seg(R, cls, run, aa, bb, n)
            run = []
        if len(run) > 3:
            _seg(R, cls, run, aa, bb, n)

    def scroll(px, pz, size, ch, ph, ww):
        """`acanthus_scroll`'s geometry, routed through the clipper."""
        main = spiral(px, pz, size, size * 0.34, 0.60, ph, ch)
        put(GOLDS, [(q, r - ww * 0.26) for (q, r) in main], ww * 1.06, ww * 0.26)
        put(GOLD, main, ww, ww * 0.22)
        tipx, tipz = main[-1]
        put(GOLD, spiral(tipx + ch * size * 0.10 * math.cos(ph + 3.4),
                         tipz + size * 0.10 * math.sin(ph + 3.4),
                         size * 0.12, size * 0.03, 0.70, ph + 3.4, ch),
            ww * 0.30, ww * 0.10)
        for f in (0.30, 0.62):
            i = int(f * (len(main) - 1))
            put(GOLD, spiral(main[i][0], main[i][1], size * 0.34, size * 0.07,
                             0.66, ph + 2.2, -ch), ww * 0.38, ww * 0.11)
        return main

    # --- body: a broad tapering sweep from the tail corner to the head corner
    tx = cx - head * hx * 0.92
    tz = cz - hz * 0.66 * chir
    hxx = cx + head * hx * 0.78
    hzz = cz + hz * 0.52 * chir
    # the spine's BELLY must fall on the head side, or the mass's centroid
    # lands in the wrong half of its own box (measured 0.675 of the way aft).
    spine = arc(tx, tz, hxx, hzz, -hz * bow * chir * head, n=56)
    # The BODY is the widest stroke in the mass -- it is a paisley body, not a
    # tendril -- and it is also the stroke that carries the mass's ORIENTATION.
    # Buying area here instead of with more volutes keeps the two flanks
    # distinguishable: at high volute counts a mass degenerates into a filled
    # box and the two sides correlate no matter how they were drawn.
    put(GOLDS, [(x, z - w * 0.28) for (x, z) in spine], w * 1.62, w * 0.34)
    put(GOLD, spine, w * 1.50, w * 0.30)

    def at(f):
        return spine[int(np.clip(f, 0.0, 1.0) * (len(spine) - 1))]

    # --- head scroll, deep in the head end
    scroll(hxx, hzz, R0 * 0.62, chir, phase + J(2.2), w * 1.25)

    # --- volutes budding off the spine ALONG ITS WHOLE LENGTH, biggest at the
    #     head end so the mass's centroid lands where the measurement puts it.
    #     `rich` is the solver's area knob: it adds ATTACHED elements, which
    #     grows the mass's area without growing the component COUNT.  Width is
    #     not the knob -- width past 0.22 R0 turns every scroll into a disc.
    nv = int(np.clip(round(nvol * rich), 2, 26))
    for k in range(nv):
        # Volutes are placed on a 2-D low-discrepancy lattice inside the box,
        # each STEMMED back to its nearest spine point.  Strung along the spine
        # instead (rev 11's third attempt) they leave the box corners bare and
        # the mass cannot reach the measured fill of 0.30 no matter how rich it
        # gets: a 1-D chain of scrolls has no way to fill a 2-D box.
        u1 = (lat + (k + 1) * 0.6180339887) % 1.0       # golden-ratio sequence
        u2 = (0.37 * lat + (k + 1) * 0.7548776662) % 1.0
        f = 0.96 - 0.80 * u1 ** wf                      # weighted to the head
        sx, sz = at(f)
        rr = 0.34 + 0.60 * u2
        ang = phase + 2.399963 * k                      # golden angle
        vxc = sx + head * hx * (0.52 * rr * math.cos(ang) + J(0.10))
        vzc = sz + hz * (0.60 * rr * math.sin(ang) * chir + J(0.10))
        size = min(R0 * (0.18 + 0.26 * f), hz * 0.60, hx * 0.60)
        ww = w * (0.40 + 0.26 * f)
        if keep is not None and not keep(vxc, vzc):
            # the volute's centre landed in a forbidden slice (the lower nose's
            # shared texels).  Slide it OUT of the slice rather than let the
            # clipper eat it -- same inventory, nudged, which is what a painter
            # working round an obstruction does.
            for dz in np.arange(0.02, 0.40, 0.02):
                if keep(vxc, vzc + dz):
                    vzc += dz
                    break
                if keep(vxc, vzc - dz):
                    vzc -= dz
                    break
        put(GOLD, arc(sx, sz, vxc, vzc, 0.0, n=10), ww * 0.85, ww * 0.85)
        scroll(vxc, vzc, size, chir * (1 if k % 2 == 0 else -1),
               phase + 1.7 + 1.35 * k + J(3.14), ww)

    # --- small curls between the volutes
    nc = int(np.clip(round(ncurl * rich), 2, 18))
    for k in range(nc):
        f = 0.88 - 0.78 * ((k + 0.5) / nc)
        ex, ez = at(f)
        s = R0 * (0.14 + 0.13 * f)
        put(GOLD, spiral(ex, ez, s * 0.92, s * 0.12, 0.85,
                         phase + 2.6 + 1.9 * k + J(3.14), -chir),
            w * 0.44, w * 0.12)

    # --- leaves reaching for the box corners
    nl = int(np.clip(round(leaves * rich), 1, 9))
    for k in range(nl):
        f = 0.86 - 0.62 * ((k + 0.5) / nl)
        ex, ez = at(f)
        ang = phase + 1.1 + 2.3 * k + J(1.2)
        put(GOLD, arc(ex, ez, ex + head * hx * 0.52 * math.cos(ang),
                      ez - hz * 0.72 * math.sin(ang) * chir,
                      hz * 0.16 * chir, n=22), w * 0.62, w * 0.08)

    # --- tail: a long thin sweep with its own coil
    if tail:
        t = arc(tx, tz, cx - head * hx * 1.00, cz + hz * 0.22 * chir,
                -hz * 0.24 * chir * head, n=28)
        put(GOLDS, [(x, z - w * 0.12) for (x, z) in t], w * 0.60, w * 0.09)
        put(GOLD, t, w * 0.52, w * 0.07)
        put(GOLD, spiral(t[-1][0], t[-1][1], R0 * 0.22, w * 0.30, 0.80,
                         phase + 4.6, -chir), w * 0.34, w * 0.09)
    return spine


# rosette: outer ring of cream pearls, cream scalloped mid-ring, gold disc,
# DARK CENTRE.  folk_door.md sec.4 -- the door rosettes are 8-11 px in the
# photograph so this sub-structure is taken from the same painter's rosettes on
# the rear quarter at (890, 545), as the report instructs.  CONFIRMED at 12x on
# `ref_rear34.jpg` (855,565)-(915,625), where the same flower resolves at ~2x
# `ref_side.jpg`'s sampling: twelve pale pearls on an outer ring, a scalloped
# mid-ring, a pale disc with a small dark dot.  It is a PALE motif, not a gold
# one -- the reason it classifies as gold in `ref_side.jpg` is that at
# 4.7 mm/px the whole 40 mm flower blurs into one warm blob whose B/R lands at
# 0.16-0.31, inside the gold gate.
# geometry solved so cream / (pi R^2) = ROS_CREAM_FRAC, which is what turns the
# measured 10-rosette disc area into the measured 3.90 % cream.
ROS_PEARLS = 12
ROS_PEARL_R = 0.152        # x R
ROS_PEARL_AT = 0.845       # x R
ROS_MID_IN, ROS_MID_OUT = 0.442, 0.5218
ROS_GOLD_R = 0.400
ROS_DARK_R = 0.155


def rosette(R, cx, cz, d, phase=0.0):
    r = d * 0.5
    for k in range(ROS_PEARLS):
        a = phase + 2 * math.pi * k / ROS_PEARLS
        R.disc(CREAM, cx + r * ROS_PEARL_AT * math.cos(a),
               cz + r * ROS_PEARL_AT * math.sin(a), r * ROS_PEARL_R)
    R.disc(CREAM, cx, cz, r * ROS_MID_OUT)
    R.disc(NONE, cx, cz, r * ROS_MID_IN)
    R.disc(GOLD, cx, cz, r * ROS_GOLD_R)
    R.disc(DARK, cx, cz, r * ROS_DARK_R)


# ===========================================================================
# 7.  CAB DOOR.  Authored in door-local metres:  a = across from the HINGE
#     (front, +x) edge, b = down from the belt.
# ===========================================================================
def door_xz(a, b):
    x = DOOR_X1 - a
    return x, belt_z(x) - b


def door_pv(u, v):
    """motif-map (u, v) from folk_door.md sec.9 -> door-local metres."""
    a = u * DOOR_W
    pv = (v - BELT_V) / (1.0 - BELT_V)
    x = DOOR_X1 - a
    return a, (belt_z(x) - panel_bot(x)) * pv


def build_door(R, rng, variant=0, ws=1.0):
    """G1 / ACANTHUS-MAIN -- one continuous stroke system spanning u 0.000-0.813
    and the full panel height, 86 % of the component gold area -- plus the four
    detached bottom-row curls G2-G5 and the latch-edge sliver G6.
    `variant` re-composes the same inventory for the other flank; `ws` is the
    global stroke-width scale the door solver sets."""
    A = DOOR_W

    def S(a, b):
        return door_xz(a, b)

    if variant == 0:
        acanthus_scroll(R, *S(0.115 * A, 0.300), 0.150, chir=+1, phase=1.05,
                        w=0.064 * ws)
        acanthus_scroll(R, *S(0.070 * A, 0.372), 0.098, chir=-1, phase=3.6,
                        w=0.048 * ws)
        stem = arc(*S(0.055 * A, 0.395), *S(0.395 * A, 0.125), -0.055)
        R.stroke(GOLDS, [(x, z - 0.010) for (x, z) in stem], 0.052 * ws,
                 0.020 * ws)
        R.stroke(GOLD, stem, 0.045 * ws, 0.017 * ws)
        curl(R, *S(0.325 * A, 0.185), 0.070, chir=-1, phase=0.4, w=0.034 * ws)
        curl(R, *S(0.395 * A, 0.310), 0.074, chir=+1, phase=2.5, w=0.036 * ws)
        acanthus_scroll(R, *S(0.520 * A, 0.250), 0.118, chir=-1, phase=2.0,
                        w=0.052 * ws)
        leaf(R, *S(0.470 * A, 0.390), *S(0.610 * A, 0.110), 0.045, 0.034 * ws)
        tail = arc(*S(0.600 * A, 0.235), *S(0.800 * A, 0.412), 0.052)
        R.stroke(GOLDS, [(x, z - 0.006) for (x, z) in tail], 0.030 * ws,
                 0.008 * ws)
        R.stroke(GOLD, tail, 0.025 * ws, 0.007 * ws)
        curl(R, *S(0.788 * A, 0.398), 0.036, chir=+1, phase=1.4, w=0.014 * ws)
        leaf(R, *S(0.360 * A, 0.230), *S(0.455 * A, 0.360), 0.026, 0.030 * ws)
        leaf(R, *S(0.240 * A, 0.155), *S(0.062 * A, 0.140), -0.030, 0.028 * ws)
        leaf(R, *S(0.150 * A, 0.410), *S(0.330 * A, 0.425), 0.028, 0.030 * ws)
        leaf(R, *S(0.430 * A, 0.410), *S(0.560 * A, 0.395), 0.024, 0.024 * ws)
    else:
        acanthus_scroll(R, *S(0.118 * A, 0.325), 0.152, chir=-1, phase=2.3,
                        w=0.064 * ws)
        acanthus_scroll(R, *S(0.196 * A, 0.170), 0.094, chir=+1, phase=0.6,
                        w=0.046 * ws)
        stem = arc(*S(0.070 * A, 0.140), *S(0.380 * A, 0.390), 0.058)
        R.stroke(GOLDS, [(x, z - 0.010) for (x, z) in stem], 0.052 * ws,
                 0.020 * ws)
        R.stroke(GOLD, stem, 0.045 * ws, 0.017 * ws)
        curl(R, *S(0.350 * A, 0.145), 0.072, chir=+1, phase=2.9, w=0.036 * ws)
        curl(R, *S(0.300 * A, 0.395), 0.068, chir=-1, phase=1.1, w=0.032 * ws)
        acanthus_scroll(R, *S(0.545 * A, 0.300), 0.122, chir=+1, phase=4.1,
                        w=0.052 * ws)
        leaf(R, *S(0.480 * A, 0.115), *S(0.625 * A, 0.395), -0.048, 0.034 * ws)
        tail = arc(*S(0.615 * A, 0.355), *S(0.802 * A, 0.155), -0.048)
        R.stroke(GOLDS, [(x, z - 0.006) for (x, z) in tail], 0.030 * ws,
                 0.008 * ws)
        R.stroke(GOLD, tail, 0.025 * ws, 0.007 * ws)
        curl(R, *S(0.792 * A, 0.168), 0.034, chir=-1, phase=3.3, w=0.014 * ws)
        leaf(R, *S(0.365 * A, 0.340), *S(0.458 * A, 0.215), -0.026, 0.030 * ws)
        leaf(R, *S(0.230 * A, 0.415), *S(0.058 * A, 0.398), 0.030, 0.028 * ws)
        leaf(R, *S(0.170 * A, 0.135), *S(0.340 * A, 0.120), -0.026, 0.030 * ws)
        leaf(R, *S(0.440 * A, 0.130), *S(0.570 * A, 0.145), -0.022, 0.024 * ws)

    for i, (u, v, su, sv) in enumerate(CURLS):          # G2..G5, bottom row
        uu = u if variant == 0 else min(0.94, 1.04 - u)
        a, b = door_pv(uu, v)
        curl(R, *S(a, b), 0.42 * su * A, chir=(1 if (i + variant) % 2 else -1),
             phase=1.7 * i + 0.6 * variant, w=0.26 * su * A * ws)
    u, v, su, sv = EDGE_E                                # G6, latch-edge sliver
    uu = u if variant == 0 else 0.012
    a, b = door_pv(uu, v)
    h = sv * DOOR_H
    R.stroke(GOLD, arc(*S(a, b - 0.5 * h), *S(a, b + 0.5 * h), 0.006),
             0.024 * ws, 0.018 * ws)


def door_dark(R, variant=0):
    """DARK-1, and nothing else.  folk_door.md sec.8: vertical luma transects
    across gold->red boundaries ON THE DOOR show NO undershoot below the red --
    the gold falls to red and stops.  There is no dark keyline on this panel;
    the heavy dark curlwork is a rear-quarter and lower-nose feature."""
    u, v, su, sv = DARK_1
    uu = u if variant == 0 else 0.975
    a, b = door_pv(uu, v)
    h = sv * DOOR_H
    R.stroke(DARK, arc(*door_xz(a, b - 0.5 * h), *door_xz(a, b + 0.5 * h),
                       0.004), su * DOOR_W * 0.90, su * DOOR_W * 0.70)


def door_rosettes(R, rng, variant=0):
    """10 rosettes at the measured diameters, six of them in the bottom row at
    v 0.91-0.98 (sec.4).  Cream ring, gold sub-disc, DARK CENTRE."""
    out = []
    for (u, v, d) in ROSETTES:
        if variant == 0:
            uu, vv = u, v
        else:
            # same inventory, different hand: reverse the u order and jitter
            # inside the measured band, so the two flanks do not rhyme
            uu = float(np.clip(1.0 - u + rng.normal(0, 0.030), 0.03, 0.97))
            vv = float(np.clip(v + rng.normal(0, 0.010), BELT_V + 0.03, 0.992))
        a, b = door_pv(uu, vv)
        rosette(R, *door_xz(a, b), d * DOOR_W, phase=rng.random() * 0.5)
        out.append((uu, vv, d))
    return out


# ===========================================================================
# 8.  REST OF THE FLANK
#
#     TEXTURE-WRAP COLLISION.  The tile period is 1/MAP_SCALE = 3.846 m and the
#     flank is 4.01 m long, so body station x and station x - 3.846 SHARE
#     TEXELS.  Concretely x >= +1.866 is the same paint as x <= -1.980: the
#     lower nose and the rear-most quarter cannot be authored independently
#     under a single object-space box projection.  They are therefore authored
#     ONCE, with the nose's own band (z 0.470-0.700, sec.10) carrying the nose
#     composition and the rear bouquet kept above and below it.  The fix is a
#     MAP_SCALE change in t1_mats.py -- see the note at the bottom of this file.
# ===========================================================================
SHARE_X = FLANK_X0 + 1.0 / MAP_SCALE          # +1.866
NOSE_Z0, NOSE_Z1 = 0.470, 0.700               # sec.10 wedge, above the bumper


def full_band(x):
    """the whole painted red field -- the band sec.11's scan measures over."""
    return panel_top(x), panel_bot(x)


def band(x):
    """where art may be PLACED: the same field less the measured 52 mm bare
    margin the painter left under the belt (sec.5)."""
    return panel_top(x) - BELT_MARGIN, panel_bot(x)


def rocker_band(x):
    """strip below the cab-door shut line.  folk_door.md gives no separate
    figure for it; carried at the near-bare mid-flank rate."""
    return door_bot_z(x) - 0.010, sill_z(x)


def nose_band(x):
    return NOSE_Z1, NOSE_Z0


def build_nose(R, rng, variant=0, gs=1.0, ds=1.0):
    """Lower nose, sec.10: ONE bold yellow hook and ONE bold dark-brown
    comma/leaf on plain red -- sparser and larger-stroked than the door, and
    unlike the door it carries resolved heavy dark curlwork.  The wedge sec.10
    measures is only ~0.039 m2, so 11.44 % gold is ~4500 mm2 of stroke and
    2.42 % dark is ~940 mm2: two motifs, not a field."""
    zc = 0.5 * (NOSE_Z0 + NOSE_Z1)
    sgn = 1 if variant == 0 else -1
    R.stroke(DARK, spiral(1.906, zc + 0.045, 0.040, 0.012, 0.46,
                          2.4 + variant, -sgn), 0.026 * ds, 0.008 * ds)
    acanthus_scroll(R, 1.948, zc - 0.008, 0.062, chir=sgn, phase=0.7 + variant,
                    w=0.030 * gs, eyes=(0.45,), shade=False)


def vz(x, v):
    """body z at fraction `v` down the VISIBLE band at station x."""
    t, b = panel_top(x), panel_bot(x)
    return t - v * (t - b)


def nose_free(x, z):
    """False where a flank motif would land on the lower nose's own texels.

    The tile period is 1/MAP_SCALE = 3.846 m, so x and x - 3.846 are the same
    texel.  The lower-nose composition occupies x 1.87-2.02 at z 0.470-0.700,
    which is the same paint as x -1.976..-1.826 at the same z -- i.e. a 150 mm
    window inside the rear-quarter mass.  The two cannot both be authored:
    sec.10 puts 11.4 % gold on the nose and the flank scan puts 37 % there.
    The rear mass yields, and the residual is reported, not hidden.  The fix is
    in section 12(e)/(f) and it is a t1_mats.py change, not a tile change.
    """
    # `build_nose` puts its two motifs at x 1.866-2.010, so the shared window
    # is exactly x - 3.846 = -1.980 .. -1.836, plus a 5 mm margin.
    if not (-2.020 <= x <= -1.796):
        return True
    return not (NOSE_Z0 - 0.035 <= z <= NOSE_Z1 + 0.035)


def build_rear(R, rng, variant=0, ws=1.0, aw=1.0):
    """THE FLANK COMPOSITION.  Two large connected masses where the photograph
    puts them, plus the four measured tendrils.  Nothing else.

    rev 10 built this as six `acanthus_scroll`s at hand-picked stations and
    then let a 56-bin density controller add small curls until the coverage
    profile matched.  The coverage profile did match; the composition did not.
    Measured on `ref_side.jpg`, the gold aft of the door is TWO components
    carrying 78 % of it (0.0732 and 0.0303 m2), four tendrils carrying 8 %,
    eight rosette blobs carrying 12 %, and a tail of chroma fringes.
    """
    sgn = 1 if variant == 0 else -1

    def guard(x, z):
        # no flank stroke may reach x < XART_LO: that texel is the cab door's
        # hinge edge (x = -2.029 and x = +1.817 are the same paint).
        # + 12 mm.  Anything aft of XART_LO wraps onto the cab door's hinge
        # edge (x = -2.029 and x = +1.817 are the same texel); the margin is
        # kept small because the last 40 mm of the tail is where the measured
        # rear mass is densest -- at +40 mm the X -1.95 bin lost 13 points.
        return x >= XART_LO + 0.012 and nose_free(x, z)

    for i, (nm, xa, xb, v0, v1, area, el) in enumerate(FLANK_MASSES):
        # variant 1 flips the sweep of each mass inside its own box and
        # re-phases it: same box, same area, a different drawing.
        ch = sgn if i == 0 else -sgn
        xm = 0.5 * (xa + xb)
        bouquet(R, xa, xb, vz(xm, v1), vz(xm, v0),
                w=0.060, rich=(ws if i == 0 else aw),
                chir=ch, phase=(1.15 if i == 0 else 3.9) + 2.77 * variant,
                # head stays AFT on both flanks: it is the measured centroid,
                # not a stylistic choice.  The two sides are decorrelated by
                # chirality, phase and the volute lattice's offset instead.
                head=-1, keep=guard, lat=0.0 if variant == 0 else 0.41,
                jit=rng,
                # the off flank is a DIFFERENT DRAWING of the same composition:
                # same box, same area, same aft-weighted centroid, but the body
                # sweeps the other way through the box and the volutes seat on
                # a different lattice with the opposite weighting.
                bow=0.50 if variant == 0 else 0.86,
                wf=1.15 if variant == 0 else 0.62,
                nvol=5 if variant == 0 else 6,
                ncurl=4 if variant == 0 else 3,
                leaves=3 if variant == 0 else 2)
    for k, (xa, xb, v0, v1, area, el) in enumerate(FLANK_TENDRILS):
        xm, zm0, zm1 = 0.5 * (xa + xb), vz(0.5 * (xa + xb), v0), \
            vz(0.5 * (xa + xb), v1)
        # a tendril is a single tapered sweep; its measured elongation sets
        # which way round it runs
        if el > 2.6:                     # tall and thin -> runs down the panel
            p0, p1 = (xb, zm0), (xa, zm1)
        else:
            p0, p1 = (xb, zm1), (xa, zm0)
        if variant:
            p0, p1 = p1, p0
        L = max(math.hypot(p1[0] - p0[0], p1[1] - p0[1]), 1e-4)
        wid = (area * 1e-6) / L          # mm2 -> m2, over the stroke length
        pts = arc(p0[0], p0[1], p1[0], p1[1],
                  (0.030 if k % 2 else -0.030) * sgn, n=24)
        # the tendrils' areas are MEASURED, so they carry no solver scale --
        # rev 11 briefly multiplied them by the mass richness and put 16 % gold
        # into a bin the photograph holds at 6 %.
        if all(guard(px, pz) for (px, pz) in pts):
            R.stroke(GOLD, pts, wid * 1.35, wid * 0.35)
            c = spiral(p1[0], p1[1], 0.030, 0.008, 0.72,
                       1.1 + 1.7 * k + variant, sgn * (1 if k % 2 else -1))
            R.stroke(GOLD, c, wid * 0.90, wid * 0.25)


def rear_rosettes(R, rng, variant=0, scale=1.0):
    """The eight rosettes measured on the flank, at their measured stations.

    rev 10 scattered these on a density-weighted Poisson walk from x -1.985 to
    -0.86 at a 30 mm step, which put 20-30 of them on the panel.  The
    photograph has EIGHT aft of the shut line, and one of those (X +0.845) is
    the only piece of folk art on the whole open panel between the cab door and
    the bouquet.  Diameters are the measured blob diameters: at the
    photograph's 4.7 mm/px a rosette reads as one warm blob, so
    d_eq = 2 sqrt(area / pi) is the rosette's own diameter to within the PSF.
    """
    out = []
    for k, (x, v, area) in enumerate(FLANK_ROSETTES):
        d = 2.0 * math.sqrt(area * 1e-6 / math.pi) * scale
        if variant:
            # same inventory, mirrored within its own zone and jittered, so the
            # two flanks do not rhyme.  The lone open-panel rosette keeps its
            # station: it is a composition anchor, not a texture.
            if x > 0.0:
                xx, vv = x, v          # the open-panel anchor does not move
            else:
                xx = float(np.clip(-2.0 - (x + 2.0) * 0.86 - 0.28, -1.99, -0.64))
                vv = float(np.clip(1.02 - v + rng.normal(0, 0.02), 0.08, 0.94))
        else:
            xx, vv = x, v
        xx = float(np.clip(xx, XART_LO + 0.6 * d, XART_HI - 0.6 * d))
        z = vz(xx, vv)
        if not nose_free(xx, z):
            z = vz(xx, min(0.94, vv + 0.22))
        rosette(R, xx, z, d, phase=rng.random())
        out.append((xx, vv, d))
    return out


def flank_dark(R, rng, variant=0, ds=1.0):
    """The five dark-brown marks that carry 83 % of the flank's dark ink.

    folk_door.md sec.8 says the heavy dark curlwork is a rear-quarter and
    lower-nose feature and gives no rear area fraction; rev 10 therefore laid a
    26 mm dark KEYLINE under every rear gold stroke and called it 3 %
    extrapolated.  Measured, the dark is not a keyline at all -- it is a small
    number of free-standing paisley commas, and the largest of them
    (0.0119 m2, 275 x 204 mm at X -0.51..-0.78) sits on OPEN RED just forward
    of the gold bouquet, which is a composition element in its own right.
    """
    sgn = 1 if variant == 0 else -1
    for k, (xa, xb, v0, v1, area) in enumerate(FLANK_DARKS):
        xm = 0.5 * (xa + xb)
        zt, zb = vz(xm, v0), vz(xm, v1)
        w = xb - xa
        if variant:
            xm = float(np.clip(xm - 0.085 * (1 if k % 2 else -1),
                               XART_LO + 0.10, 0.80))
            xa, xb = xm - 0.5 * w, xm + 0.5 * w
        if min(xa, xb) < XART_LO + 0.05 or not (nose_free(xa, zb)
                                                and nose_free(xb, zt)):
            continue
        # a comma: a fat tapering hook with a rolled head, area-matched
        L = math.hypot(xb - xa, zt - zb)
        wid = (area * 1e-6) / max(L * 0.78, 1e-4) * ds
        ch = sgn * (1 if k % 2 else -1)
        p = arc(xb, zt, xa, zb, 0.34 * L * ch, n=28)
        R.stroke(DARK, p, wid * 1.05, wid * 0.14)
        R.stroke(DARK, spiral(xa, zb, 0.34 * L, 0.05 * L, 0.80,
                              1.2 + 1.9 * k, ch), wid * 0.62, wid * 0.12)
        for j in range(2):                        # the comma's dot pair
            f = 0.34 + 0.24 * j
            i = int(f * (len(p) - 1))
            R.disc(DARK, p[i][0] + 0.030 * ch, p[i][1] - 0.012,
                   0.30 * wid)


# ------------------------------------------------------- filler candidates
def _cands(seed, key, x0, x1, zf, n=34, smin=0.024, smax=0.060, big=1.0):
    """A fixed pool of small curls / tendrils for one cell.  Drawn once, so a
    budget that goes up or down changes only HOW MANY are used, which is what
    makes the density solvers converge."""
    rng = np.random.default_rng([seed] + list(key))
    out = []
    for _ in range(n):
        f = float(rng.random())
        s = float(rng.uniform(smin, smax)) * big
        out.append(dict(x=x0 + (x1 - x0) * float(rng.random()),
                        f=f, s=s, w=s * float(rng.uniform(0.34, 0.54)),
                        ch=1 if rng.random() < 0.5 else -1,
                        ph=float(rng.random()) * 6.283,
                        kind=float(rng.random()), ang=float(rng.random()) * 6.283))
    return out, zf


def _draw_cands(R, pool, zf, k, dark=0.0):
    for c in pool[:int(max(0, round(k)))]:
        x = float(np.clip(c["x"], XART_LO + c["s"], XART_HI - c["s"]))
        c = dict(c, x=x)
        z = zf(c["x"], c["f"])
        if c["kind"] < 0.55:
            curl(R, c["x"], z, c["s"], chir=c["ch"], phase=c["ph"], w=c["w"],
                 dark=dark)
        else:
            s, a = c["s"], c["ang"]
            leaf(R, c["x"] - s * math.cos(a), z - s * 0.75 * math.sin(a),
                 c["x"] + s * math.cos(a), z + s * 0.75 * math.sin(a),
                 s * 0.45 * c["ch"], c["w"], dark=dark)


# ===========================================================================
# 9.  BODY-SPACE SAMPLING.  Every number reported below is read off the tile
#     the way the shader reads it: through the mapping contract, on a grid in
#     BODY coordinates -- not by looking at texels in tile space.
# ===========================================================================
def look(lab, pen, X, Z, wrap=True):
    px, py = pen.px(X, Z)
    c = px.astype(np.int64)
    r = py.astype(np.int64)
    if wrap:
        c = np.mod(c, TILE)
        r = np.mod(r, TILE)
    else:
        c = np.clip(c, 0, lab.shape[1] - 1)
        r = np.clip(r, 0, lab.shape[0] - 1)
    return lab[r, c]


def door_grid(nu=440, nv=240):
    ud = (np.arange(nu) + 0.5) / nu                 # 0 = hinge
    pv = (np.arange(nv) + 0.5) / nv                 # 0 = belt
    UD, PV = np.meshgrid(ud, pv)
    X = DOOR_X1 - UD * DOOR_W
    ZT = Z_BELT0 - RAKE_DZDX * X
    ZB = np.interp(X, [t[0] for t in _DOOR_BOT_AUTH],
                   [t[1] for t in _DOOR_BOT_AUTH]) - RAKE_Z0 - RAKE_DZDX * X
    return X, ZT - PV * (ZT - ZB), UD, PV


def band_grid(x0, x1, nx, nz, bandfn):
    xs = x0 + (x1 - x0) * (np.arange(nx) + 0.5) / nx
    fz = (np.arange(nz) + 0.5) / nz
    X, F = np.meshgrid(xs, fz)
    T = np.array([bandfn(x)[0] for x in xs])[None, :]
    B = np.array([bandfn(x)[1] for x in xs])[None, :]
    return X, B + (T - B) * F


def classify(v):
    return (((v == GOLD) | (v == GOLDS)), v == CREAM, v == DARK)


def frac(lab, pen, X, Z, wrap=True):
    g, c, d = classify(look(lab, pen, X, Z, wrap))
    n = float(X.size)
    return 100 * g.sum() / n, 100 * c.sum() / n, 100 * d.sum() / n


# ===========================================================================
# 10.  SOLVERS.  Closed loop: render, measure in body space, adjust, repeat.
# ===========================================================================
def solve_door(side, seed, variant, verbose=True):
    view = door_view(side)
    pen = Pen(side, view)
    X, Z, UD, PV = door_grid()
    ub = np.clip((UD * 20).astype(int), 0, 19)
    vb = np.clip((PV * 10).astype(int), 0, 9)
    cell = [[(ub == i) & (vb == j) for j in range(10)] for i in range(20)]
    T2 = np.clip(np.outer(DOOR_U_PROFILE, DOOR_V_PROFILE) / DOOR_GOLD, 0, 92.0)

    over = Raster(Pen(side))
    door_dark(over, variant)
    door_rosettes(over, np.random.default_rng(seed + 7), variant)

    def base(ws):
        R = Raster(Pen(side))
        build_door(R, np.random.default_rng(seed), variant, ws)
        return R.ops

    def gold_of(ops):
        R = Raster(pen)
        R.ops = ops
        lab = np.asarray(R.render(), dtype=np.uint8)
        g, c, d = classify(look(lab, pen, X, Z, wrap=False))
        return g, lab

    # 1) global stroke-width scale so the ACANTHUS MASS alone lands at ~68 % of
    #    the measured coverage, leaving the rest for the curl filler
    lo, hi = 0.45, 1.35
    for _ in range(7):
        ws = 0.5 * (lo + hi)
        g, _ = gold_of(base(ws) + over.ops)
        if 100.0 * g.mean() < 0.68 * DOOR_GOLD:
            lo = ws
        else:
            hi = ws
    ws = 0.5 * (lo + hi)
    if verbose:
        print("      acanthus width scale %.3f" % ws)
    under = base(ws)

    # 2) per-cell filler against the max-entropy 2-D target
    pools = {}
    for i in range(20):
        for j in range(10):
            a0, a1 = DOOR_W * i / 20.0, DOOR_W * (i + 1) / 20.0
            j0, j1 = j / 10.0, (j + 1) / 10.0

            def zf(x, f, j0=j0, j1=j1):
                zt, zb = belt_z(x), panel_bot(x)
                return zt - (j0 + (j1 - j0) * f) * (zt - zb)
            pools[(i, j)] = _cands(seed, [i, j], DOOR_X1 - a1, DOOR_X1 - a0,
                                   zf, n=64, smin=0.013, smax=0.040)
    # Controller.  The SHAPE is set by a per-cell residual against the
    # max-entropy 2-D target; the LEVEL is then set by bisecting one global
    # scalar on the whole budget, which is monotone and therefore cannot
    # ratchet the way a clipped per-cell integrator does.
    def draw(nb):
        Rf = Raster(Pen(side))
        for i in range(20):
            for j in range(10):
                p, zf = pools[(i, j)]
                _draw_cands(Rf, p, zf, nb[i, j])
        return under + Rf.ops + over.ops

    def stats(ops):
        g, _ = gold_of(ops)
        A2 = np.array([[100.0 * g[cell[i][j]].mean() for j in range(10)]
                       for i in range(20)])
        uu = np.array([100.0 * g[ub == i].mean() for i in range(20)])
        vv = np.array([100.0 * g[vb == j].mean() for j in range(10)])
        return 100.0 * g.mean(), A2, uu, vv

    Tn = T2 * (DOOR_GOLD / T2.mean())
    K = 0.030                            # motifs per percentage-point of gap
    nbud = np.zeros((20, 10))
    ops = draw(nbud)
    tot, A2, uu, vv = stats(ops)
    best, bops = None, ops
    for rnd in range(7):
        raw = np.maximum(0.0, nbud + K * (Tn - A2))
        if raw.sum() <= 0:
            break
        lo, hi = 0.0, 4.0                                  # global level solve
        for _ in range(9):
            lam = 0.5 * (lo + hi)
            t2_, _a, _u, _v = stats(draw(raw * lam))
            if t2_ < DOOR_GOLD:
                lo = lam
            else:
                hi = lam
        nbud = raw * (0.5 * (lo + hi))
        ops = draw(nbud)
        tot, A2, uu, vv = stats(ops)
        urms = float(np.sqrt(((uu - DOOR_U_PROFILE) ** 2).mean()))
        vrms = float(np.sqrt(((vv - DOOR_V_PROFILE) ** 2).mean()))
        cost = abs(tot - DOOR_GOLD) * 3.0 + urms + vrms
        if best is None or cost < best:
            best, bops = cost, ops
        if verbose:
            print("      round %d  gold %6.2f %%  u-rms %5.2f  v-rms %5.2f"
                  % (rnd, tot, urms, vrms))
    return bops


def solve_flank(side, seed, variant, door_ops, verbose=True):
    """The flank is now COMPOSED, not filled.

    rev 10 solved 56 independent per-bin coverage targets by adding small
    curls from a candidate pool until each bin matched.  That reaches any
    coverage profile and cannot reach a composition: coverage is a marginal.
    Held against `ref_side.jpg` it produced 55 free marks of 300-3000 mm2
    against the photograph's 13, and 1.7 % gold on the open panel the
    photograph keeps at 0.29 %.

    What is solved here is five scalars, and every one of them is a SIZE, not a
    count:
        wsR  element richness of MASS-R1, the rear-most quarter's paisley
        wsA  element richness of MASS-R2, the mass over the rear arch
        rs   rosette diameter scale (count and stations are measured)
        dks  dark-comma stroke width
        gs, dsn   the two lower-nose motifs, sec.10's 11.44 % / 2.42 %
    Solving sizes cannot invent marks, so the component statistics are a
    property of the inventory and not of the controller.
    """
    pen = Pen(side)
    NB = 56
    edges = np.linspace(FLANK_X0, FLANK_X1, NB + 1)
    Xs, Zs, tgt, live = [], [], [], []
    for i in range(NB):
        x0, x1 = edges[i], edges[i + 1]
        xc = 0.5 * (x0 + x1)
        indoor = DOOR_X0 - 0.02 < xc < DOOR_X1 + 0.02
        bf = rocker_band if indoor else full_band
        X, Z = band_grid(x0, x1, 12, 110, bf)
        Xs.append(X)
        Zs.append(Z)
        tgt.append(0.0 if indoor else flank_density(xc))
        live.append(xc < 1.83)
    tgt = np.array(tgt)
    live = np.array(live)

    def build(wsR, wsA, rs, dks, gs, dsn):
        R = Raster(Pen(side))
        rng = np.random.default_rng(seed + 31)
        build_rear(R, rng, variant, wsR, wsA)
        flank_dark(R, np.random.default_rng(seed + 53), variant, dks)
        rear_rosettes(R, np.random.default_rng(seed + 91), variant, rs)
        build_nose(R, rng, variant, gs, dsn)      # LAST: it owns its texels
        return R.ops

    def render(ops):
        R = Raster(pen)
        R.ops = ops
        return np.asarray(R.render(), dtype=np.uint8)

    def zone(lab, xa, xb, n=64):
        X, Z = band_grid(xa, xb, n, 200, full_band)
        return frac(lab, pen, X, Z)

    Xn, Zn = band_grid(1.870, 2.020, 60, 170, nose_band)

    def bisect(f, lo, hi, n=8):
        for _ in range(n):
            m = 0.5 * (lo + hi)
            if f(m):
                lo = m
            else:
                hi = m
        return 0.5 * (lo + hi)

    def dens_target(xa, xb, n=96):
        """the FLANK_DENSITY profile averaged over a zone, weighted by the
        MODEL's own band height -- which is what the tile can actually fill."""
        q = np.linspace(min(xa, xb), max(xa, xb), n)
        h = np.array([max(panel_top(x) - panel_bot(x), 0.0) for x in q])
        d = np.array([flank_density(x) for x in q])
        return float((d * h).sum() / max(h.sum(), 1e-9))

    T_R1 = dens_target(-1.53, -2.007)
    T_R2 = dens_target(-0.80, -1.30)
    P = dict(wsR=1.0, wsA=1.0, rs=1.0, dks=1.0, gs=1.0, dsn=1.0)

    def lab_of(**kw):
        q = dict(P)
        q.update(kw)
        return render(door_ops + build(**q))

    # 1) MASS-R1 against the measured 27.86 % over X -1.45..-2.007
    P["wsR"] = bisect(lambda m: zone(lab_of(wsR=m), -1.53, -2.007)[0]
                      < T_R1, 0.40, 8.00)
    # 2) MASS-R2 against the measured 13.93 % over X -0.62..-1.45
    P["wsA"] = bisect(lambda m: zone(lab_of(wsA=m), -0.80, -1.30)[0]
                      < T_R2, 0.40, 8.00)
    # 3) rosette diameters are MEASURED (d_eq of the blob each one makes in
    #    `ref_side.jpg`), so they are NOT solved -- the achieved cream is
    #    reported as an outcome.  sec.3's cream gate (B/R >= 0.42 against a
    #    red ground at 0.193 and a cream ink at 0.53) sits ABOVE the 50 %-ink
    #    crossing, so the measured 1.10 % rear cream is itself a floor.
    P["rs"] = 1.0
    # 4) dark commas against the rear quarter's measured dark.  The gate used
    #    is the 50 %-ink crossing (0.78 x the local red ground), which is the
    #    unbiased area estimator for a blurred edge -- sec.3's 0.62 x gate is
    #    ~88 % pure and reads only the marks' cores (0.14 % against 4.21 %).
    #    The same argument says sec.3's gold gate IS unbiased: G/R 0.475 sits
    #    at the midpoint of red 0.249 and gold ink 0.75.
    P["dks"] = bisect(lambda m: zone(lab_of(dks=m), -1.45, -2.007)[2]
                      < REAR_DARK, 0.30, 2.40)
    # 5) the two lower-nose motifs, sec.10
    P["gs"] = bisect(lambda m: frac(lab_of(gs=m), pen, Xn, Zn)[0]
                     < NOSE_GOLD, 0.20, 2.2)
    P["dsn"] = bisect(lambda m: frac(lab_of(dsn=m), pen, Xn, Zn)[2]
                      < NOSE_DARK, 0.05, 2.0)
    # 6) re-close R1/R2 once, because 3-5 add ink inside their zones
    for _ in range(2):
        P["wsR"] = bisect(lambda m: zone(lab_of(wsR=m), -1.53, -2.007)[0]
                          < T_R1, 0.40, 8.00, 7)
        P["wsA"] = bisect(lambda m: zone(lab_of(wsA=m), -0.80, -1.30)[0]
                          < T_R2, 0.40, 8.00, 7)

    ops = door_ops + build(**P)
    lab = render(ops)
    if verbose:
        print("      sizes: R1 %.3f  R2 %.3f  rosette %.3f  dark %.3f  "
              "nose gold %.3f  nose dark %.3f"
              % (P["wsR"], P["wsA"], P["rs"], P["dks"], P["gs"], P["dsn"]))
        got = np.array([frac(lab, pen, Xs[i], Zs[i])[0] for i in range(NB)])
        e = (got - tgt)[live]
        print("      flank density rms %.2f %%, max %.2f %% (%d bins); "
              "open panel %.2f %% against a measured %.2f %%\n"
              "      zone targets: R1 %.2f got %.2f   R2 %.2f got %.2f"
              % (float(np.sqrt((e ** 2).mean())), float(np.abs(e).max()),
                 int(live.sum()), zone(lab, 0.872, -0.62)[0], OPEN_GOLD,
                 T_R1, zone(lab, -1.53, -2.007)[0],
                 T_R2, zone(lab, -0.80, -1.30)[0]))
    return ops, lab


# ---------------------------------------------------------------- nose decal
# `tex/nose.png`.  NOT read by t1_mats.py yet -- see section 12(f) for the four
# nodes that wire it in.  It exists because the nose FRONT face is box-projected
# and therefore samples (y, z), which lands in the same u-band as the cab door's
# flank footprint: the door's lower art appears on the nose.
#
# Content is deliberately almost empty.  folk_door.md sec.10 measures the lower
# nose WEDGE (the red below the open door, above the bumper, source x 93-124,
# y 545-601) at 11.44 % gold / 2.42 % dark, and says of the front face itself
# that the bullet indicator and the headlamp bezel occupy essentially all of it
# and that the strip between the lamps and the door's leading edge is 4-9 px
# wide at grazing incidence -- NOT MEASURABLE.  So this decal carries the
# measured wedge composition around BOTH front corners at the measured band
# height and asserts nothing about the middle of the face, which is left bare.
# Inventing scrollwork for the centre would breach SPEC 10.10.
NOSE_TEX = 3072
NOSE_Y0, NOSE_Y1 = -0.780, 0.780       # decal window in object space
NOSE_ZA, NOSE_ZB = 0.020, 1.580        # square, so the art is undistorted


class NosePen:
    """maps (y, z) to the nose decal, the way a FLAT projection on
    CombineXYZ(Y, 0, Z) would.  `x` in every motif call is the body Y."""

    def __init__(self):
        self.view = (0, 0, NOSE_TEX * SS, NOSE_TEX * SS)

    def px(self, y, z):
        u = (y - NOSE_Y0) / (NOSE_Y1 - NOSE_Y0)
        v = (z - NOSE_ZA) / (NOSE_ZB - NOSE_ZA)
        return u * NOSE_TEX * SS, (1.0 - v) * NOSE_TEX * SS

    def m(self, d):
        return d * NOSE_TEX * SS / (NOSE_Y1 - NOSE_Y0)


def make_nose(path=None, verbose=True):
    pen = NosePen()
    R = Raster(pen)
    zc = 0.5 * (NOSE_Z0 + NOSE_Z1)
    for s in (-1, +1):
        y = s * 0.615
        R.stroke(DARK, spiral(y - s * 0.042, zc + 0.045, 0.040, 0.012, 0.46,
                              2.4, -s), 0.0152, 0.0047)
        acanthus_scroll(R, y, zc - 0.008, 0.062, chir=s, phase=0.7,
                        w=0.030, eyes=(0.45,), shade=False)
    lab = np.asarray(R.render(), dtype=np.uint8)
    W = {}
    for c in (GOLD, GOLDS, CREAM, DARK):
        W[c] = ((lab == c).reshape(NOSE_TEX, SS, NOSE_TEX, SS)
                .sum(axis=(1, 3), dtype=np.int32) / float(SS * SS))
    alpha = sum(W.values())
    acc = np.zeros((NOSE_TEX, NOSE_TEX, 3), np.float32)
    for c, col in PAL.items():
        acc += W[c][..., None] * col.astype(np.float32)
    rgb = np.where(alpha[..., None] > 1e-6,
                   acc / np.maximum(alpha, 1e-6)[..., None], 0.0)
    if ndimage is not None:
        m = (alpha > 1e-6).astype(np.float32)
        for _ in range(5):
            w = ndimage.uniform_filter(m, 9)
            for k in range(3):
                sm = ndimage.uniform_filter(rgb[..., k] * m, 9)
                rgb[..., k] = np.where(m > 0.5, rgb[..., k],
                                       sm / np.maximum(w, 1e-6))
            m = (w > 1e-6).astype(np.float32)
    out = np.zeros((NOSE_TEX, NOSE_TEX, 4), np.uint8)
    out[..., :3] = np.clip(lin_to_srgb(rgb) * 255.0 + 0.5, 0, 255).astype(np.uint8)
    out[..., 3] = np.clip(alpha * 255.0 + 0.5, 0, 255).astype(np.uint8)
    p = path or os.path.join(TEXDIR, "nose.png")
    Image.fromarray(out, "RGBA").save(p)
    # measure it in the same wedge folk_door.md sec.10 measured
    g = ((lab == GOLD) | (lab == GOLDS))
    d = (lab == DARK)
    ys = np.linspace(0.545, 0.690, 60)
    zs = np.linspace(NOSE_Z0, NOSE_Z1, 170)
    Y, Z = np.meshgrid(ys, zs)
    px, py = pen.px(Y, Z)
    c = np.clip(px.astype(int), 0, NOSE_TEX * SS - 1)
    r = np.clip(py.astype(int), 0, NOSE_TEX * SS - 1)
    if verbose:
        print("  [nose] %s  %dx%d, window y %.3f..%.3f z %.3f..%.3f "
              "(%.3f m square)"
              % (p, NOSE_TEX, NOSE_TEX, NOSE_Y0, NOSE_Y1, NOSE_ZA, NOSE_ZB,
                 NOSE_Y1 - NOSE_Y0))
        print("        corner wedge: gold %.2f %% (sec.10 %.2f), "
              "dark %.2f %% (sec.10 %.2f); rest of the face bare by design"
              % (100 * g[r, c].mean(), NOSE_GOLD,
                 100 * d[r, c].mean(), NOSE_DARK))
        print("        whole face alpha %.2f %%" % (100 * (alpha > 0.5).mean()))
    return p


def make(path=None, side="show", seed=196301, variant=0, verbose=True):
    check_mapping_contract()
    if verbose:
        print("  [%s] cab door -- folk_door.md sec.3/sec.5" % side)
    dops = solve_door(side, seed, variant, verbose)
    if verbose:
        print("  [%s] flank -- the MEASURED inventory (sec.3b)" % side)
    ops, lab = solve_flank(side, seed, variant, dops, verbose)
    rgba, alpha, W = resolve(lab)
    p = path or os.path.join(TEXDIR, SIDES[side][2])
    Image.fromarray(rgba, "RGBA").save(p)
    if verbose:
        print("  [%s] %d ops -> %s" % (side, len(ops), p))
    return dict(path=p, ops=ops, lab=lab, alpha=alpha, W=W, side=side)


def class_weights(lab):
    """area-exact per-class coverage of every output texel (SS x SS block)."""
    out = {}
    a = np.asarray(lab, dtype=np.uint8)
    for c in (GOLD, GOLDS, CREAM, DARK):
        out[c] = ((a == c).reshape(N, SS, N, SS)
                  .sum(axis=(1, 3), dtype=np.int32) / float(SS * SS))
    return out


def resolve(lab):
    """label raster -> (sRGB uint8, alpha, per-class texel weights)."""
    W = class_weights(lab)
    alpha = sum(W.values())
    acc = np.zeros((N, N, 3), np.float32)
    for c, col in PAL.items():
        acc += W[c][..., None] * col.astype(np.float32)
    rgb = np.where(alpha[..., None] > 1e-6,
                   acc / np.maximum(alpha, 1e-6)[..., None], 0.0)
    # bleed ink colour into the transparent ground so bilinear filtering in the
    # shader cannot pull a dark fringe out of empty texels
    if ndimage is not None:
        m = (alpha > 1e-6).astype(np.float32)
        for _ in range(5):
            w = ndimage.uniform_filter(m, 9)
            for k in range(3):
                sm = ndimage.uniform_filter(rgb[..., k] * m, 9)
                rgb[..., k] = np.where(m > 0.5, rgb[..., k],
                                       sm / np.maximum(w, 1e-6))
            m = (w > 1e-6).astype(np.float32)
    else:
        rgb = np.where(alpha[..., None] > 1e-6, rgb,
                       PAL[GOLD].astype(np.float32))
    out = np.zeros((N, N, 4), np.uint8)
    out[..., :3] = np.clip(lin_to_srgb(rgb) * 255.0 + 0.5, 0, 255).astype(np.uint8)
    out[..., 3] = np.clip(alpha * 255.0 + 0.5, 0, 255).astype(np.uint8)
    return out, alpha, W


def door_view(side):
    """sub-texel bbox of the cab-door painted panel for this side."""
    pen = Pen(side)
    xs = np.linspace(DOOR_X0, DOOR_X1, 9)
    pts = [pen.px(x, panel_top(x)) for x in xs] + \
          [pen.px(x, panel_bot(x)) for x in xs]
    c0 = int(math.floor(min(p[0] for p in pts))) - 2
    c1 = int(math.ceil(max(p[0] for p in pts))) + 2
    r0 = int(math.floor(min(p[1] for p in pts))) - 2
    r1 = int(math.ceil(max(p[1] for p in pts))) + 2
    return c0, r0, c1 - c0, r1 - r0


# ===========================================================================
# 11.  REPORT
# ===========================================================================
def contrast(res):
    """Composite the tile over t1_mats.RED in LINEAR light -- exactly what the
    Mix node in body_paint does -- and measure Rec.709 luma on sRGB codes."""
    a = np.asarray(Image.open(res["path"])).astype(np.float64) / 255.0
    lin = srgb_to_lin(a[..., :3])
    al = a[..., 3:4]
    comp = lin * al + RED_LIN[None, None, :] * (1.0 - al)
    luma = (lin_to_srgb(comp) * 255.0) @ LUMA_W
    W, alpha = res["W"], res["alpha"]
    out = {}
    for nm, sel in (("gold core", W[GOLD] >= 0.995),
                    ("gold whole class", (W[GOLD] + W[GOLDS]) > 0.5),
                    ("cream core", W[CREAM] >= 0.995),
                    ("dark core", W[DARK] >= 0.995)):
        out[nm] = (float(np.median(luma[sel])) if sel.sum() else float("nan"),
                   int(sel.sum()))
    out["red"] = (RED_LUMA, int((alpha < 0.002).sum()))
    return out


def contrast_through_shader(res, w_art=0.30, sat=2.45, val=0.94):
    """What the tile would read as THROUGH THE CURRENT UNPATCHED body_paint:
    Hue/Saturation(Sat 2.45, Val 0.94) on the colour, then Mix over RED at
    alpha * W_ART.  This is the measurement that shows the contrast target is
    unreachable without the t1_mats.py changes listed at the bottom of this
    file -- reported next to the corrected path, not instead of it."""
    a = np.asarray(Image.open(res["path"])).astype(np.float64) / 255.0
    lin = srgb_to_lin(a[..., :3])
    mx = lin.max(axis=2)
    mn = lin.min(axis=2)
    v = mx
    sv = np.where(mx > 1e-9, (mx - mn) / np.maximum(mx, 1e-9), 0.0)
    # hue, then rebuild with S' = clip(S*sat), V' = V*val   (Blender HSV node)
    with np.errstate(invalid="ignore", divide="ignore"):
        d = np.maximum(mx - mn, 1e-12)
        r, g, b = lin[..., 0], lin[..., 1], lin[..., 2]
        h = np.where(mx == r, (g - b) / d % 6,
                     np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) / 6.0
    h = np.where(sv < 1e-9, 0.0, h)
    S = np.clip(sv * sat, 0, 1)
    V = np.clip(v * val, 0, 1)
    i = np.floor(h * 6.0) % 6
    f = h * 6.0 - np.floor(h * 6.0)
    pp, qq, tt = V * (1 - S), V * (1 - S * f), V * (1 - S * (1 - f))
    out = np.zeros_like(lin)
    for k, (rr, gg, bb) in enumerate(((V, tt, pp), (qq, V, pp), (pp, V, tt),
                                      (pp, qq, V), (tt, pp, V), (V, pp, qq))):
        m = (i == k)
        out[..., 0] = np.where(m, rr, out[..., 0])
        out[..., 1] = np.where(m, gg, out[..., 1])
        out[..., 2] = np.where(m, bb, out[..., 2])
    al = a[..., 3:4] * w_art
    comp = out * al + RED_LIN[None, None, :] * (1 - al)
    luma = (lin_to_srgb(comp) * 255.0) @ LUMA_W
    W = res["W"]
    res2 = {}
    for nm, sel in (("gold core", W[GOLD] >= 0.995),
                    ("cream core", W[CREAM] >= 0.995),
                    ("dark core", W[DARK] >= 0.995)):
        res2[nm] = float(np.median(luma[sel])) if sel.sum() else float("nan")
    return res2


def demirror_check(res_show, res_off):
    """Audit materials-14 asks one specific question: is the off flank the show
    flank mirrored?  Sample BOTH tiles the way the body samples them, on the
    same body grid, and correlate over every shift and both parities.

    Two correlations are reported.  The RAW one is dominated by the density
    envelope, which the two sides are *supposed* to share -- both flanks must
    obey the same measured coverage-vs-x.  The WHITENED one subtracts each
    map's own local density (a 0.30 m boxcar along the body) and so answers the
    question that actually matters: is it the same DRAWING?"""
    xs = np.linspace(FLANK_X0, FLANK_X1, 1024)
    fs = np.linspace(0.01, 0.99, 192)
    X, F = np.meshgrid(xs, fs)
    T = np.array([full_band(x)[0] for x in xs])[None, :]
    B = np.array([full_band(x)[1] for x in xs])[None, :]
    Z = B + (T - B) * F

    def bodymap(lab, side):
        return (look(lab, Pen(side), X, Z) != NONE).astype(np.float32)

    def whiten(M):
        k = max(3, int(0.30 / (xs[1] - xs[0])) | 1)          # 0.30 m boxcar
        if ndimage is None:
            return M - M.mean()
        return M - ndimage.uniform_filter1d(M, k, axis=1, mode="wrap")

    A = bodymap(res_show["lab"], "show")
    Bo = bodymap(res_off["lab"], "off")
    C = bodymap(res_show["lab"], "off")      # what the UNPATCHED shader does

    def ncc(P, Q):
        p, q = P - P.mean(), Q - Q.mean()
        n = float(np.sqrt((p * p).sum() * (q * q).sum()))
        if not n:
            return 0.0
        r = np.fft.irfft2(np.fft.rfft2(p) * np.conj(np.fft.rfft2(q)), p.shape)
        return float(r.max() / n)

    wA, wB, wC = whiten(A), whiten(Bo), whiten(C)
    return {
        "TWO tiles  raw   unflipped / mirrored":
            (round(ncc(A, Bo), 4), round(ncc(A, Bo[:, ::-1]), 4)),
        "TWO tiles  whitened  unflipped / mirrored":
            (round(ncc(wA, wB), 4), round(ncc(wA, wB[:, ::-1]), 4)),
        "ONE tile   raw   unflipped / mirrored":
            (round(ncc(A, C), 4), round(ncc(A, C[:, ::-1]), 4)),
        "ONE tile   whitened  unflipped / mirrored":
            (round(ncc(wA, wC), 4), round(ncc(wA, wC[:, ::-1]), 4)),
        "ink coverage over the flank, show / off (%)":
            (round(float(100 * A.mean()), 2), round(float(100 * Bo.mean()), 2)),
    }


def composition(res, x0=0.872, x1=-2.007):
    """The measurement this rev exists for: CONNECTED COMPONENTS of the gold,
    sampled in body coordinates at `ref_side.jpg`'s own 4.735 mm/px so the
    component census is comparable with the photograph's.

    Coverage is a marginal.  Two tiles can carry the same 10 % gold over the
    same flank and read as signwriting or as confetti, and only this
    measurement tells them apart.
    """
    if ndimage is None:
        return None
    lab, pen = res["lab"], Pen(res["side"])
    # rev 23, SPEC 10.63.  `mm = 1000.0 / 211.21` stood here: the BANNED flat
    # px/m.  SPEC 10.43 RETIRED `REF_PPM = 211.2` (4.7 % wrong across the
    # lockup) and 10.29/10.36 established the flank map is PROJECTIVE --
    # X(u) = 641220.4/(u + 11140) - 55.0322, 211.2 px/m mid-body against 226.9
    # at the tail.  A single linear px->metre scale does not hold along this
    # flank; that is one of this project's oldest hard-won rules.
    #
    # WHAT IT IS USED FOR, which is why it is a STEP and not a SCALE: this
    # function walks body stations to count gold coverage, so 211.21 only sets
    # the SAMPLING INTERVAL, never a position -- every x below is a body-frame
    # metre already.  The value is therefore harmless HERE and lethal if copied.
    # It is renamed to say so, and the banned name is not reintroduced.
    STEP_M = 1.0 / 211.21   # SAMPLING STEP ONLY -- never a px<->m conversion
    xs = np.arange(x0, x1, -STEP_M)
    nz = 40
    fz = (np.arange(nz) + 0.5) / nz
    X, F = np.meshgrid(xs, fz)
    T = np.array([panel_top(x) for x in xs])[None, :]
    B = np.array([panel_bot(x) for x in xs])[None, :]
    Z = T - F * (T - B)
    v = look(lab, pen, X, Z)
    gold = (v == GOLD) | (v == GOLDS)
    dark = v == DARK
    cream = v == CREAM
    # rev 24, SPEC 10.66 -- REGRESSION INTRODUCED BY REV 23, caught by AST.
    # rev 23 renamed the definition `mm = 1000.0/211.21` to `STEP_M = 1.0/211.21`
    # (above) and did not update this use site.  `mm` then had ZERO Store sites
    # and ONE Load site in the whole module, so `composition()` -- the function
    # whose own docstring calls it "the measurement this rev exists for" -- could
    # not complete, and the connected-component census it produces (COMP_TOP,
    # COMP_HIST, FLANK_MASSES) could not run at all.  Line 1976 is a top-level
    # statement of the function body, so it is reached unconditionally.
    # STEP_M is in metres, so the mm conversion moves to the use site.
    cell = STEP_M * 1000.0 * 1000.0 * float((T - B).mean()) / nz
    M = ndimage.binary_closing(gold, np.ones((3, 3)))
    L, n = ndimage.label(M, structure=np.ones((3, 3)))
    fa = ndimage.sum(M, L, range(1, n + 1)) * cell if n else np.zeros(0)

    # the door in its own plane at 1 mm/px, sec.5's own recipe
    nu, nv = 940, 524
    UD, PV = np.meshgrid((np.arange(nu) + 0.5) / nu, (np.arange(nv) + 0.5) / nv)
    Xd = DOOR_X1 - UD * DOOR_W
    ZT = np.array([panel_top(x) for x in Xd[0]])[None, :]
    ZB = np.array([panel_bot(x) for x in Xd[0]])[None, :]
    vd = look(lab, pen, Xd, ZT - PV * (ZT - ZB))
    gd = (vd == GOLD) | (vd == GOLDS)
    Md = ndimage.binary_closing(gd, np.ones((15, 15)))
    Ld, nd = ndimage.label(Md, structure=np.ones((3, 3)))
    da = ndimage.sum(Md, Ld, range(1, nd + 1)) * 1.0 if nd else np.zeros(0)

    allar = np.concatenate([da, fa])
    o = np.argsort(allar)[::-1]
    tot = allar.sum()
    cum = np.cumsum(allar[o]) / max(tot, 1e-9)
    zones = {}
    for nm, xa, xb, v0, v1, tgt in CLEAR_ZONES:
        m = (X <= xa) & (X >= xb) & (F >= v0) & (F <= v1)
        if m.sum() > 20:
            zones[nm] = (100 * gold[m].mean(), tgt)
    return dict(areas=allar, n=allar.size, m2=tot * 1e-6,
                top={k: 100 * cum[min(k, allar.size) - 1] for k in
                     (1, 2, 3, 5, 10)},
                zones=zones, gold=100 * gold.mean(), dark=100 * dark.mean(),
                cream=100 * cream.mean())


def report_composition(res):
    c = composition(res)
    if c is None:
        print("  (composition report needs scipy)")
        return
    print("  COMPOSITION -- gold connected components, whole flank")
    print("    %-26s %10s %10s" % ("", "ref_side", "achieved"))
    print("    %-26s %10d %10d" % ("components", 66, c["n"]))
    print("    %-26s %10.4f %10.4f" % ("gold area (m2)", 0.2826, c["m2"]))
    for k in (1, 2, 3, 5, 10):
        print("    %-26s %10.1f %10.1f"
              % ("gold in the largest %-2d (%%)" % k, COMP_TOP[k], c["top"][k]))
    print("    size histogram (mm2)      %10s %10s   %10s %10s"
          % ("ref n", "got n", "ref % gold", "got %"))
    edges = [0, 100, 300, 1000, 3000, 10000, 30000, 1e12]
    a = c["areas"]
    T = max(a.sum(), 1e-9)
    for i, (nm, rn, rp) in enumerate(COMP_HIST):
        sel = (a >= edges[i]) & (a < edges[i + 1])
        print("      %-24s %10d %10d   %10.2f %10.2f"
              % (nm, rn, int(sel.sum()), rp, 100 * a[sel].sum() / T))
    print("  CLEAR ZONES (gold %, ref_side -> achieved)")
    for nm, (got, tgt) in c["zones"].items():
        print("    %-42s %6.2f -> %6.2f" % (nm, tgt, got))


def report(out):
    for side in ("show", "off"):
        r = out[side]
        lab, pen = r["lab"], Pen(side)
        X, Z, UD, PV = door_grid()
        g, c, d = classify(look(lab, pen, X, Z))
        ub = np.clip((UD * 20).astype(int), 0, 19)
        vb = np.clip((PV * 10).astype(int), 0, 9)
        uu = np.array([100.0 * g[ub == i].mean() for i in range(20)])
        vv = np.array([100.0 * g[vb == j].mean() for j in range(10)])
        gg, cc, dd = 100 * g.mean(), 100 * c.mean(), 100 * d.mean()

        print("\n  =================== %s FLANK ===================" % side.upper())
        print("  CAB DOOR PANEL                     target   achieved")
        for nm, t, a in (("gold / painted panel   %", DOOR_GOLD, gg),
                         ("cream rosettes         %", DOOR_CREAM, cc),
                         ("dark-brown ink         %", DOOR_DARK, dd),
                         ("red ground             %", 66.54,
                          100 - gg - cc - dd)):
            print("    %-30s %8.2f %10.2f" % (nm, t, a))
        print("    gold across the door, 20 bins, hinge -> latch")
        print("      target " + " ".join("%4.1f" % v for v in DOOR_U_PROFILE))
        print("      got    " + " ".join("%4.1f" % v for v in uu))
        print("      u<0.25  target 42.1  got %5.1f      "
              "u>0.75  target  5.1  got %5.1f       "
              "rms %.1f, r = %.2f"
              % (uu[:5].mean(), uu[15:].mean(),
                 float(np.sqrt(((uu - DOOR_U_PROFILE) ** 2).mean())),
                 float(np.corrcoef(uu, DOOR_U_PROFILE)[0, 1])))
        print("    gold down the panel, 10 bins, belt -> bottom")
        print("      target " + " ".join("%4.1f" % v for v in DOOR_V_PROFILE))
        print("      got    " + " ".join("%4.1f" % v for v in vv))
        print("      rms %.1f, r = %.2f"
              % (float(np.sqrt(((vv - DOOR_V_PROFILE) ** 2).mean())),
                 float(np.corrcoef(vv, DOOR_V_PROFILE)[0, 1])))

        Xn, Zn = band_grid(1.870, 2.020, 60, 160, nose_band)
        gn, cn, dn = frac(lab, pen, Xn, Zn)
        print("  LOWER NOSE (sec.10)                target   achieved")
        print("    %-30s %8.2f %10.2f" % ("gold                   %",
                                          NOSE_GOLD, gn))
        print("    %-30s %8.2f %10.2f" % ("dark-brown ink         %",
                                          NOSE_DARK, dn))

        print("  FLANK SCAN, sec.11 quantity gold / (red + gold)")
        print("    %8s %8s %8s   %s" % ("X", "target", "got", "status"))
        for xc, tv, rel in FLANK_SCAN:
            Xb, Zb = band_grid(xc - 0.095, xc + 0.095, 40, 200, full_band)
            gb, cb, db = frac(lab, pen, Xb, Zb)
            note = {True: "measured", False: "arch-affected: lower bound",
                    None: "arch artefact -- discarded"}[rel]
            print("    %8.3f %8.2f %8.2f   %s"
                  % (xc, tv, 100.0 * gb / max(100.0 - cb - db, 1e-6), note))
        Xr, Zr = band_grid(-2.000, -1.700, 60, 200, full_band)
        gr, cr, dr = frac(lab, pen, Xr, Zr)
        print("    rear quarter: dark %.2f %% (extrapolated target %.1f), "
              "cream %.2f %% (extrapolated target %.1f)"
              % (dr, REAR_DARK, cr, REAR_CREAM))

        print("  CONTRAST over t1_mats.RED (adjacent-red luma %.2f)" % RED_LUMA)
        ct = contrast(r)
        for nm, t in (("gold core", 2.048), ("gold whole class", 1.840),
                      ("cream core", 2.348), ("dark core", 0.490)):
            lu, n = ct[nm]
            print("    %-20s target x%.3f    got %6.2f = x%.3f   (n = %d)"
                  % (nm, t, lu, lu / RED_LUMA, n))
        cs2 = contrast_through_shader(r)
        print("  the same tile THROUGH THE UNPATCHED t1_mats.body_paint "
              "(W_ART 0.30, HueSat 2.45/0.94):")
        for nm, t in (("gold core", 2.048), ("cream core", 2.348),
                      ("dark core", 0.490)):
            print("    %-20s target x%.3f    got %6.2f = x%.3f   <- BLOCKED"
                  % (nm, t, cs2[nm], cs2[nm] / RED_LUMA))

        report_composition(r)

    print("\n  ============ materials-14: are the flanks the same art? ========")
    for k, v in demirror_check(out["show"], out["off"]).items():
        print("    %-42s %s" % (k, v if isinstance(v, tuple) else "%.4f" % v))


def main():
    print("folk_gen rev 11  --  composition re-measured from ref_side.jpg;\n"
          "  coverage and contrast held at folk_door.md's values")
    print("  tile %d px, ss %d, 1 texel = %.3f mm on the body, period %.3f m"
          % (N, SS, 1000.0 / (N * MAP_SCALE), 1.0 / MAP_SCALE))
    print("  palette solved for the sec.7 contrast ratios against t1_mats.RED "
          "(luma %.2f):" % RED_LUMA)
    for k, nm in ((GOLD, "gold"), (GOLDS, "gold shade"), (CREAM, "cream"),
                  (DARK, "dark")):
        s = tuple(int(v) for v in np.round(lin_to_srgb(PAL[k]) * 255))
        print("      %-11s sRGB %-16s luma %6.2f   x red = %.3f"
              % (nm, s, code_luma(PAL[k]), code_luma(PAL[k]) / RED_LUMA))
    out = {}
    for side, seed, variant in (("show", 196301, 0), ("off", 771963, 1)):
        out[side] = make(side=side, seed=seed, variant=variant)
    make_nose()
    report(out)
    return out


# ===========================================================================
# 12.  WHAT MUST CHANGE IN t1_mats.py  (not edited here -- other work is live
#      in that file).  Every line number is against the tree this was written
#      on.  Without (a) and (b) the art CANNOT reach the measured contrast: at
#      W_ART 0.30 the densest possible gold composites to x2.15 the red only if
#      the ink is pure white, and the Hue/Saturation node clamps every class to
#      full saturation, which turns the cream rosettes orange.
#
#   (a) t1_mats.py:175   W_ART = float(os.environ.get("T1_W_ART", 0.30))
#                     -> W_ART = float(os.environ.get("T1_W_ART", 1.00))
#       The folk art is painted, not glazed.  0.30 is a 30 % opacity ceiling.
#
#   (b) t1_mats.py:893 and :894  the Hue/Saturation node on the swirl colour
#           hs.inputs["Saturation"].default_value = 2.45   -> 1.0
#           hs.inputs["Value"].default_value      = 0.94   -> 1.0
#       2.45 clamps S to 1.0 for gold, cream AND dark: the cream rosettes
#       (198,164,105) come out fully saturated orange and the dark brown loses
#       its blue channel.  The tile is now authored at the correct colours.
#
#   (c) t1_mats.py:846-878  the density mask (fx, fx2, bz/belt/beltw, clut,
#       thr, keep) is now REDUNDANT and must be bypassed: at line 879 replace
#           amask = _math(nt, 'MULTIPLY', swirl.outputs["Alpha"], keep, ...)
#       with a direct link from swirl.outputs["Alpha"].  Density-vs-x, the
#       42 %->5 % ramp across the door, the 52 mm bare belt margin and the
#       per-class split are all baked into the tile now, measured in body
#       coordinates.  Leaving the mask in place multiplies the measured
#       profile by a second, wrong one.
#       If the mask is kept instead, its corrected numbers are:
#           fx  (rear lobe)   0.05 at X -0.30  ->  1.00 at X -2.05 stays, but
#                             the plateau is 20 % from X -0.97 to -1.72 and the
#                             rise to 40 % happens only aft of -1.75;
#           fx2 (door lobe)   inputs[1] 0.55 -> 0.90, inputs[2] 1.75 -> 1.83,
#                             inputs[3] 0.05 -> 0.03, inputs[4] 0.60 -> 1.00.
#           The old fx2 topped out at 0.60 of the tile alpha over a lobe that
#           began at X +0.55 -- i.e. it put its maximum on the flank BEHIND the
#           door and never reached the door's own coverage.
#
#   (d) materials-14, the de-mirroring.  Blender's BOX projection samples the
#       two Y faces at u and 1-u, so one tile can only ever give two mirrored
#       flanks.  Add a per-side selector (sign of Position.Y is unambiguous;
#       the normal is not, on a crowned flank):
#           sep.Y -> Math GREATER_THAN 0.0            -> `sideY`
#           swirl_b = _img(nt, "swirl_b.png", ...)     same Vector as swirl
#           MixRGB(sideY, swirl_b.Color, swirl.Color) -> hs.Color
#           Math MIX / Mix float(sideY, swirl_b.Alpha, swirl.Alpha) -> amask
#       and make the vector explicit rather than relying on the box flip:
#           u = 0.815 - 0.26*X on +Y, u = 0.185 + 0.26*X on -Y, v = 0.263+0.26*Z
#       (SeparateXYZ -> Math -> CombineXYZ -> projection='FLAT').  That is the
#       convention the two tiles here are authored for.  Also drop
#       projection_blend 0.32 -> 0.10 (t1_mats.py:826): at 0.32 the nose corner
#       cross-fades two unrelated regions of the tile.
#
#   (f) THE NOSE FRONT FACE -- a KNOWN OPEN DEFECT, and the reason this file
#       now also writes `tex/nose.png`.  The swirl image is BOX-projected in
#       object space, so Blender picks the sampling axes from the largest
#       normal component.  On the nose front face that is |Nx|, and the face is
#       therefore sampled on (tile_co.y, tile_co.z):
#           u = 0.410 + 0.26 y   ->  u 0.192 .. 0.628  over y -0.84 .. +0.84
#           v = 0.263 + 0.26 z   ->  v 0.380 .. 0.575  over z  0.45 .. 1.20
#       The cab door's own flank footprint is
#           u = 0.815 - 0.26 x   ->  u 0.379 .. 0.579  over x +0.908 .. +1.817
#           v = 0.263 + 0.26 z   ->  v 0.471 .. 0.572  over the painted panel
#       The two windows overlap over almost the whole of the door's band, so
#       WHATEVER IS IN THE DOOR'S LOWER BAND IS ALSO ON THE NOSE.  That is why
#       the rev-10 render shows the door's scattered comma marks across the
#       nose.  It is not a tile defect and no change to this file can fix it:
#       one image cannot hold two different drawings for one (u, v).
#
#       PER-FACE UVs ALONE DO NOT FIX IT EITHER.  The flank already uses
#       u 0.28 .. 1.34 (mod 1) of a 3.846 m period -- the tile has no unused
#       band to move the nose into.  The fix is A SECOND IMAGE.  `tex/nose.png`
#       is written by `make_nose()` above: 1024 px square covering the object-
#       space window y -0.780 .. +0.780, z 0.020 .. 1.580 (1.560 m square, so
#       the art is undistorted), carrying folk_door.md sec.10's measured wedge
#       composition round both front corners and NOTHING in the middle of the
#       face, which sec.10 records as NOT MEASURABLE.
#
#       Node changes in `body_paint`, against the tree this was written on
#       (`sideY`, `mixA`, `mixC`, `hs`, `sep`, `mp` all already exist):
#
#         geo   = nt.nodes.new("ShaderNodeNewGeometry")
#         sepN  = nt.nodes.new("ShaderNodeSeparateXYZ")            # geo.Normal
#         nt.links.new(geo.outputs["Normal"], sepN.inputs[0])
#         absx  = _math(nt, 'ABSOLUTE', sepN.outputs["X"], None, ...)
#         facex = _math(nt, 'GREATER_THAN', absx, 0.70, ...)       # front face
#         fwd   = _math(nt, 'GREATER_THAN', sep.outputs["X"], 1.60, ...)
#         isNose= _math(nt, 'MULTIPLY', facex, fwd, ...)
#         # decal vector: FLAT on (y, z), mapped into the window above
#         cmb   = nt.nodes.new("ShaderNodeCombineXYZ")
#         nt.links.new(sep.outputs["Y"], cmb.inputs[0])            # -> u axis
#         nt.links.new(sep.outputs["Z"], cmb.inputs[1])            # -> v axis
#         nmp   = nt.nodes.new("ShaderNodeMapping")                # POINT
#         nmp.inputs["Scale"].default_value    = (0.6410, 0.6410, 1.0)
#         nmp.inputs["Location"].default_value = (0.5000, -0.0128, 0.0)
#         nt.links.new(cmb.outputs[0], nmp.inputs["Vector"])
#         nose  = _img(nt, "nose.png", ..., projection='FLAT', ext='CLIP')
#         nt.links.new(nmp.outputs[0], nose.inputs["Vector"])
#         # select: the nose decal WINS on the front face, the flank tile
#         # everywhere else.  Insert between mixC/mixA and hs/amask:
#         mixNC = Mix RGBA (Factor isNose, A mixC.Result, B nose.Color)
#         mixNA = Mix FLOAT(Factor isNose, A mixA.Result, B nose.Alpha)
#         nt.links.new(mixNC.outputs[2], hs.inputs["Color"])
#         nt.links.new(mixNA.outputs[0], amask.inputs[0])
#
#       Scale check: 0.6410 = 1 / 1.560, and 0.5 - 0.6410 * 0.0200 = 0.4872,
#       so z = 0.020 maps to v = 0 and z = 1.580 to v = 1; y = 0 maps to
#       u = 0.5.  `ext='CLIP'` keeps the decal off the rest of the body if the
#       selector is ever mis-wired -- outside the window it returns alpha 0.
#
#       Once (f) is in, the shared-texel collision of section 8 also goes away
#       for the nose motifs and `nose_free()` here can be retired: the rear
#       quarter currently gives up a 154 x 266 mm slice of MASS-R1 to the lower
#       nose's texels, which costs the X -1.85 bin about 6 points of gold.
#
#   (e) OPTIONAL, removes the nose/tail texture-wrap collision documented in
#       section 8: t1_mats.py:823 Scale 0.2600 -> 0.2280 and :815 Location
#       0.185 -> 0.500 (x only).  Period becomes 4.386 m > the 4.01 m flank, so
#       the lower nose and the rear-most quarter stop sharing texels.  MAP_LOC
#       and MAP_SCALE at the top of this file must be changed to match and the
#       generator re-run -- it self-checks and warns if they diverge.
# ===========================================================================

if __name__ == "__main__":
    main()
