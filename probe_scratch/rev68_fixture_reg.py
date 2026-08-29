# rev 68 -- MEASURE the nose fixtures' registration against the skin.
#
# F217 says the indicator pods and headlamps sit at hard-coded x literals and
# do not follow the skin.  This script MEASURES that, at whatever T1_NOSE_BULGE
# is set to, so the claim is a number and not a sentence.  It is a scratch
# measurement, not a guard: the guard goes in verify.py in the same edit as the
# change (rule 13).
#
# WHAT IT ASKS THE GEOMETRY (rule 7 -- never the pose).  For each nose fixture:
# take the fixture's REARMOST vertex ring -- the vertices within 1 mm of its own
# minimum x -- and for each, ray-cast the body from x = +3.5 back along -x at
# that vertex's own (y, z).  The signed gap is  v.x - skin.x:
#     gap > 0  the fixture's back face stands OFF the skin  -> open air
#     gap < 0  the fixture's back face is BURIED in the skin
# Report min/mean/max per fixture.
#
# NOTE ON THE HEADLAMP BOWL.  build.py cuts a recess at HL_X, so the skin behind
# the lamp is NOT the outer skin.  We therefore ALSO report a reference station
# taken off the untouched skin OUTBOARD and BELOW each fixture, so a recess does
# not read as a fixture defect.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa
from mathutils import Vector

os.environ.pop("T1_PREVIEW", None)
_cwd = os.getcwd(); os.chdir(HERE)
try:
    exec(compile(open(os.path.join(HERE, "build.py")).read(), "build.py", "exec"),
         {"__name__": "__main__", "__file__": "build.py"})
finally:
    os.chdir(_cwd)

body = bpy.data.objects["T1_body"]
bmw = body.matrix_world
inv = bmw.inverted()


def skin_x(y, z):
    """outer skin x at (y, z), world frame, or None."""
    o = inv @ Vector((3.5, y, z))
    d = (inv.to_3x3() @ Vector((-1.0, 0.0, 0.0))).normalized()
    hit, loc, _n, _i = body.ray_cast(o, d)
    return (bmw @ loc).x if hit else None


NAMES = ["hl_ring", "hl_lens", "hl_bowl", "ind1_base", "ind1_lens",
         "ind-1_base", "ind-1_lens"]

print("=" * 78)
print("  rev68 fixture-to-skin registration   T1_NOSE_BULGE=%s"
      % os.environ.get("T1_NOSE_BULGE", "(shipped)"))
print("=" * 78)
print("  %-14s %5s  %8s %8s %8s   %s"
      % ("fixture", "n", "min mm", "mean mm", "max mm", "back-face x"))
for nm in NAMES:
    obs = [o for o in bpy.data.objects if o.type == 'MESH' and
           (o.name == nm or o.name.startswith(nm + "."))]
    if not obs:
        print("  %-14s  MISSING" % nm)
        continue
    for ob in obs:
        mw = ob.matrix_world
        co = [mw @ v.co for v in ob.data.vertices]
        if not co:
            continue
        xmin = min(c.x for c in co)
        back = [c for c in co if c.x - xmin < 0.001]
        gaps = []
        for c in back:
            sx = skin_x(c.y, c.z)
            if sx is not None:
                gaps.append(c.x - sx)
        if not gaps:
            print("  %-14s  NO SKIN HIT behind %d back-face verts" % (ob.name, len(back)))
            continue
        print("  %-14s %5d  %+8.2f %+8.2f %+8.2f   %.4f"
              % (ob.name, len(gaps), 1000 * min(gaps),
                 1000 * sum(gaps) / len(gaps), 1000 * max(gaps), xmin))

# the untouched-skin reference stations, so a recess cannot read as a defect
print("  --- untouched skin, for reference ---")
for (y, z, tag) in ((0.0, 0.933, "centreline @ HL_Z"),
                    (0.545, 0.933, "HL station"),
                    (0.675, 1.139, "IND station"),
                    (0.700, 0.950, "|y|=0.70 @ z=0.95")):
    sx = skin_x(y, z)
    print("  %-22s (y %.3f z %.3f)  skin x = %s"
          % (tag, y, z, "%.4f" % sx if sx is not None else "MISS"))
