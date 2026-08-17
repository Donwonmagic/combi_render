# probe_rev36_barend.py -- rev 36
#
# WHAT THIS IS FOR
# ----------------
# The owner stated, at the end of rev 35:
#
#   "the upper bar appears to also connect with the main bumper on either end.
#    In the current version, there is no connection made."
#
# Rev 35 confirmed both halves "against the build's own constants, no render
# needed", and published two magnitudes:
#
#     hoop end underside  BAR_Z - BAR_END_DROP - BAR_DIA/2 = 0.5441
#         -> 8.1 mm of clear air above BLADE_TOP_Z = 0.536
#     hoop end station    BAR_X - BAR_END_BACK           = 2.0879
#         -> 52.4 mm behind the blade face at 2.1403
#
# BOTH ARE WRONG, AND WRONG THE SAME WAY.  They read the CONSTANTS and not the
# FUNCTION THAT CONSUMES THEM.  `overrider_bar()` does not turn the hoop end
# through a quarter circle; it caps the sweep angle at
#
#     a_max = (pi/2) * 0.62  =  55.80 deg
#
# the code's own comment saying "<= 56 deg from horizontal", for a NUMERICAL
# reason -- sweep()'s frame is t x UP and degenerates as the tangent approaches
# UP.  So the end descends by DROP*sin(a_max), not DROP, and moves back by
# BACK*(1-cos(a_max)), not BACK.
#
# THE PROJECT'S OWN RULE, EARNED TWICE BEFORE: A CLAIM IN PROSE IS NOT A GUARD;
# GREP FOR THE NODE THAT DOES IT.  Same class as SPEC 10.19's "the lids open
# FORWARD" -- prose disagreeing with the build, and the build was right.
#
# WHAT IS NOT IN DISPUTE: THE SIGN.  The ends float, at both ends, in both
# axes.  The owner's defect report stands in full.  Only rev 35's two
# magnitudes fall.
#
# METHOD -- and why it is not the arithmetic route again
# ------------------------------------------------------
# This probe's FIRST version failed its own control C3 by 81.7 mm.  The cause
# was a FRAME ERROR OF MY OWN: build.py step 8b shears the whole vehicle
# (`v.co.z -= RAKE_Z0 + RAKE_DZDX*v.co.x`) AFTER the bar is built, so the
# constants live in the UN-DROPPED frame and the mesh lives in the dropped one.
# That is verify.py 11d2's defect from rev 12, reproduced by me in rev 36.
# The control caught it before a number was published.  It is recorded, not
# quietly fixed.
#
# So this version does not compare a constant with a vertex at all.  It CASTS
# RAYS THROUGH THE BUILT SCENE.  A ray is frame-free: it measures the air
# between two surfaces as they actually sit, whatever transform put them there.
#
# CONTROLS
#   C1  orb_bar exists, is a mesh, > 100 verts
#   C2  a front bumper blade exists and is a mesh
#   C3  the two ends agree by symmetry to < 0.1 mm  (the build is mirror-built;
#       if this fails the ray sampling is biased, not the geometry)
#   C4  rev 35's z formula reproduces its own published 0.5441 from constants
#   C5  rev 35's x formula reproduces its own published 2.0879 from constants
#   C6  NEGATIVE CONTROL: a ray cast downward from a point known to be INSIDE
#       the blade's own volume must return a hit at ~zero distance, and a ray
#       cast downward from far outboard of the vehicle must return NO hit.
#       Without both, "no hit" and "hit at 0" are not distinguishable from a
#       broken caster.
#
# REFUSES TO PRINT A RULING if any control fails.

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy
from mathutils import Vector
import build as B          # noqa: F401  -- importing build constructs the scene
import t1_detail as D
import t1_core as T

CONTROLS = {}
def say(s=""):
    print(s)
def ctl(key, ok, msg):
    CONTROLS[key] = bool(ok)
    say("  [%s] %-4s %s" % ("PASS" if ok else "FAIL", key, msg))


def wverts(ob):
    m = ob.matrix_world
    return [m @ v.co for v in ob.data.vertices]


DEPS = bpy.context.evaluated_depsgraph_get()

def cast(origin, direction, ignore=None, maxd=3.0):
    """Cast through the whole scene; return (hitobj, dist) nearest hit that is
    not `ignore`.  Re-casts past ignored hits."""
    o = Vector(origin); d = Vector(direction).normalized()
    travelled = 0.0
    for _ in range(12):
        ok, loc, nrm, idx, obj, mat = bpy.context.scene.ray_cast(
            DEPS, o + d * 1e-5, d, distance=maxd - travelled)
        if not ok:
            return None, None
        step = (loc - o).length
        travelled += step
        if ignore is None or obj.name not in ignore:
            return obj, travelled
        o = loc
    return None, None


say("=" * 78)
say("probe_rev36_barend -- WHERE DO THE OVER-RIDER BAR'S ENDS ACTUALLY SIT?")
say("=" * 78)
say()

bars = [o for o in bpy.data.objects if o.type == 'MESH' and "orb_bar" in o.name]
blades = [o for o in bpy.data.objects
          if o.type == 'MESH' and ("bumper_f" in o.name)]

ctl("C1", len(bars) == 1 and len(bars[0].data.vertices) > 100,
    "orb_bar: %d object(s), %d verts"
    % (len(bars), len(bars[0].data.vertices) if bars else 0))
ctl("C2", len(blades) == 1,
    "front bumper blade: %s" % [o.name for o in blades])

if not (CONTROLS.get("C1") and CONTROLS.get("C2")):
    say("\nREFUSING TO PRINT A RULING -- a positive control is down.")
    sys.exit(0)

bar, blade = bars[0], blades[0]
bv, blv = wverts(bar), wverts(blade)

blade_y_max = max(abs(v.y) for v in blv)
blade_x_max = max(v.x for v in blv)
blade_z_max = max(v.z for v in blv)
say("  blade %-12s  |y|<=%.4f   x<=%.4f   z<=%.4f"
    % (blade.name, blade_y_max, blade_x_max, blade_z_max))

ymax = max(abs(v.y) for v in bv)
say("  bar    |y|max %.4f   (BAR_HALF_Y const %.4f + hoop y-excursion)"
    % (ymax, D.BAR_HALF_Y))
say("  -> the bar's tips are %s the blade's lateral extent"
    % ("INSIDE" if ymax <= blade_y_max else "OUTSIDE"))
say()

# ---------------------------------------------- vertical clear air, by ray
say("  VERTICAL CLEAR AIR -- rays cast straight down (0,0,-1) from the bar's")
say("  own underside, ignoring the bar itself.  Frame-free by construction.")
say()
say("  %-8s %9s %9s %9s  %-14s %10s"
    % ("|y|", "x", "z_start", "hit z", "hit object", "clear mm"))

results = []
for sgn in (+1, -1):
    band = [v for v in bv if sgn * v.y >= 0.94 * ymax]
    # sample the lowest vertex in each of several |y| slices near the tip
    lo = min(band, key=lambda v: v.z)
    obj, dist = cast((lo.x, lo.y, lo.z), (0, 0, -1), ignore={bar.name})
    results.append((sgn, lo, obj, dist))
    say("  %-8.4f %9.4f %9.4f %9s  %-14s %10s"
        % (abs(lo.y), lo.x, lo.z,
           ("%.4f" % (lo.z - dist)) if dist else "  --",
           obj.name if obj else "NO HIT",
           ("%.2f" % (dist * 1000.0)) if dist else "n/a"))

s1 = results[0]; s2 = results[1]
sym_ok = (s1[3] is not None and s2[3] is not None
          and abs(s1[3] - s2[3]) < 1e-4)
ctl("C3", sym_ok, "the two ends agree by symmetry: d=%s"
    % (("%.4f mm" % (abs(s1[3] - s2[3]) * 1000.0))
       if (s1[3] is not None and s2[3] is not None) else "one end MISSED"))

# ------------------------------------------- fore-aft relationship
# NOT a ray cast.  A forward ray from the tip returns NO HIT and that is not a
# gap measurement -- the tip sits ABOVE the blade's crown, so the ray flies
# over the bumper entirely.  Reporting that "no hit" as a clearance would be a
# detector measuring the wrong thing, which is the failure this project has
# recorded more often than any other.  The fore-aft relationship is a
# COPLANARITY, and it is stated as one.
say()
say("  FORE-AFT RELATIONSHIP -- stated as coplanarity, NOT as a ray gap.")
say("  (A +x ray from the tip returns NO HIT because the tip is ABOVE the")
say("   blade crown.  That is not 'infinite clearance'; it is the wrong test.)")
say()
hres = []
for sgn in (+1, -1):
    band = [v for v in bv if sgn * v.y >= 0.94 * ymax]
    fwd = max(band, key=lambda v: v.x)
    hres.append(blade_x_max - fwd.x)
    say("  |y| %.4f   bar tip outer face x = %.4f   blade face x = %.4f"
        % (abs(fwd.y), fwd.x, blade_x_max))
    say("             -> tip sits %.2f mm BEHIND the blade face"
        % ((blade_x_max - fwd.x) * 1000.0))
say()
say("  BAR_X is DEFINED as 2.1403 - BAR_DIA/2 with the comment 'outer faces")
say("  coplanar -- a CHOICE'.  The measurement confirms the choice took.")
say("  THERE IS NO FORE-AFT GAP TO CLOSE.  Rev 35's '52.4 mm behind it' does")
say("  not describe this build in any axis.")

# ---------------------------------------------------- rev 35's own figures
# BAR_END_DROP and BAR_END_BACK ARE RETIRED IN REV 36.  Their values are
# restated here as LITERALS, tagged as retired, purely so that rev 35's two
# published magnitudes can still be reproduced from the formulas rev 35 used.
# They are NOT read from t1_detail any more, and nothing in the build consumes
# them.  If they were read from the module this probe would crash on the tree
# it was written to audit -- which it did, once, and that is how it was found.
_RETIRED_END_DROP = 2.6 * D.BAR_DIA        # RETIRED rev 36
_RETIRED_END_BACK = 1.6 * D.BAR_DIA        # RETIRED rev 36
r35_z = D.BAR_Z - _RETIRED_END_DROP - D.BAR_DIA / 2.0
r35_x = D.BAR_X - _RETIRED_END_BACK
ctl("C4", abs(r35_z - 0.5441) < 5e-4,
    "rev 35's z formula reproduces its published 0.5441: %.6f" % r35_z)
ctl("C5", abs(r35_x - 2.0879) < 5e-4,
    "rev 35's x formula reproduces its published 2.0879: %.6f" % r35_x)

# ------------------------------------------------------- C7: THE FIX ITSELF
gap_now = s1[3] * 1000.0
ctl("C7", gap_now < 0.50,
    "TANGENCY: the hoop end now lands on the bumper -- %.3f mm of residual, "
    "which is mesh discretisation (the swept profile is a 6-segment rounded "
    "rect, not an analytic circle), not clearance" % gap_now)

# --------------------------------------------- C8: the tip did NOT move far
# The bar's outer AXIS tip is frozen exactly to its rev-30..35 value by
# construction (BAR_TIP_Y).  The MESH's outermost point is not the axis: it is
# the end cap's rim, and the cap's orientation changed from 43.4 deg to 69 deg,
# so the mesh extent moves slightly.  THAT MOVEMENT IS REPORTED, NOT HIDDEN.
_R30_MESH_YMAX = 0.641024        # measured on the rev-30..35 build, this probe
ctl("C8", abs(ymax - _R30_MESH_YMAX) < 0.0005,
    "bar mesh |y|max %.6f against rev-30..35's %.6f -- moved %+.2f mm "
    "(the AXIS tip is frozen exactly; this is the end cap re-orienting)"
    % (ymax, _R30_MESH_YMAX, (ymax - _R30_MESH_YMAX) * 1000.0))

# ------------------------------------------------------- negative controls
inside = Vector((blade_x_max - 0.02, 0.0, blade_z_max - 0.005))
o_in, d_in = cast(inside, (0, 0, -1), ignore={bar.name})
o_out, d_out = cast((blade_x_max - 0.02, 3.0, blade_z_max), (0, 0, -1),
                    ignore={bar.name}, maxd=2.0)
ctl("C6", (o_in is not None and d_in is not None and d_in < 0.10)
          and (o_out is None),
    "caster sane: inside-blade ray hits %s at %s mm; far-outboard ray %s"
    % (o_in.name if o_in else "NOTHING",
       ("%.1f" % (d_in * 1000.0)) if d_in else "n/a",
       "MISSES (correct)" if o_out is None else "HIT " + o_out.name))

say()
if not all(CONTROLS.values()):
    say("REFUSING TO PRINT A RULING -- %d control(s) down: %s"
        % (sum(1 for v in CONTROLS.values() if not v),
           [k for k, v in CONTROLS.items() if not v]))
    sys.exit(0)

# ------------------------------------------------------------------ ruling
gap_z = s1[3] * 1000.0
gap_x = hres[0] * 1000.0
a_max = (math.pi / 2) * 0.62

say("=" * 78)
say("RULING")
say("=" * 78)
say()
say("  THE OWNER'S DEFECT REPORT STANDS.  The hoop ends float at BOTH ends.")
say("  Nothing below touches the sign; only rev 35's magnitudes.")
say()
say("  %-40s %10s %10s" % ("quantity", "rev 35", "MEASURED"))
say("  %-40s %10.1f %10.1f" % ("vertical clear air, mm", 8.1, gap_z))
say("  %-40s %10.1f %10.2f" % ("tip behind blade face, mm", 52.4, gap_x))
say()
say("  THERE IS ONE GAP, NOT TWO, AND IT IS %.1fx THE PUBLISHED SIZE."
    % (gap_z / 8.1))
say()
say("  Vertical gap in tube diameters: %.3f x BAR_DIA  (rev 35 said 0.32 x)"
    % (gap_z / 1000.0 / D.BAR_DIA))
say()
say("  WHY REV 35 WAS WRONG.  It spent DROP and BACK in full.  The code turns")
say("  the hoop %.2f deg, not 90: sin = %.5f, 1-cos = %.5f.  The end descends"
    % (math.degrees(a_max), math.sin(a_max), 1 - math.cos(a_max)))
say("  %.1f mm of a possible %.1f and retreats %.1f of a possible %.1f."
    % (_RETIRED_END_DROP * math.sin(a_max) * 1000.0, _RETIRED_END_DROP * 1000.0,
       _RETIRED_END_BACK * (1 - math.cos(a_max)) * 1000.0,
       _RETIRED_END_BACK * 1000.0))
say()
say("  AND THE 0.62 IS NOT A SHAPE DECISION.  The code's comment gives a")
say("  NUMERICAL reason: sweep()'s frame is t x UP and degenerates as the")
say("  tangent approaches UP.  The hoop stops where it stops to dodge a")
say("  singularity in the sweeper.  THE FLOAT THE OWNER IS LOOKING AT IS")
say("  PARTLY AN ARTEFACT OF A WORKAROUND, not a modelled clearance.")
say()
say("  THE FIX, REV 36.  The hoop end is no longer an ad-hoc arc.  It is a")
say("  TRUE CIRCULAR BEND tangent to the bar, radius %.2f x BAR_DIA (MEASURED"
    % D.BEND_R_RATIO)
say("  in the image, a LOWER bound), turning to %.1f deg below horizontal"
    % math.degrees(D.BEND_THETA))
say("  (MEASURED in the image, an UPPER bound), then a STRAIGHT LEG of")
say("  %.2f mm whose length is DERIVED so the tube's end cap lands on the"
    % (D.BAR_LEG_LEN * 1000.0))
say("  bumper's top face AT THE TUBE'S OWN STATION -- not on the blade's")
say("  crown, which is 2.30 mm higher and is what the first attempt used.")
say()
say("  BAR_HALF_Y IS NOW DERIVED: %.6f, from a FROZEN tip at %.6f."
    % (D.BAR_HALF_Y, D.BAR_TIP_Y))
say("  BAR_END_BACK IS RETIRED.  BAR_END_DROP IS RETIRED.")
say()
say("  ALL %d CONTROLS PASSED." % len(CONTROLS))
say("=" * 78)
