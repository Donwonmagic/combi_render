# rev 68 -- ONE BUILD, THREE MEASUREMENTS.  Scratch, not a guard.
#
#   A. the BUMPER's own plan profile  max-x(y)  over |y| <= 0.75
#   B. the SHELL's plan profile at the same and at nose heights
#   C. every nose fixture's back face against the skin at its own (y, z)
#
# WHY A AND B TOGETHER.  F221 measured a sagitta on the PHOTOGRAPHED BUMPER's
# top edge and the register compares it against the SHELL's 19.6 mm plan bulge.
# They are different objects.  This prints both, off one mesh, so the comparison
# is made on like against like or not at all (rule 38).
#
# THE WINDOW IS PART OF THE MEASUREMENT (rule 8).  My first cut of C ray-cast
# from x = +3.5 down -x and accepted the first hit.  At the headlamp station the
# ray goes STRAIGHT THROUGH the headlamp aperture -- the recess is cut through,
# not blind -- and hit the REAR of the bus at x = -1.8702, so the "gap" printed
# +3967 mm.  A hit forward of x = 1.5 is required, and a ray that finds none is
# reported as a MISS and not as a number.
import os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

import bpy  # noqa
from mathutils import Vector

os.environ.pop("T1_PREVIEW", None)
_cwd = os.getcwd(); os.chdir(HERE)
try:
    exec(compile(open(os.path.join(HERE, "build.py")).read(), "build.py", "exec"),
         {"__name__": "__main__", "__file__": "build.py"})
finally:
    os.chdir(_cwd)

TAG = os.environ.get("T1_NOSE_BULGE", "(shipped 0.019)")
print("\n" + "=" * 78)
print("  rev68 NOSE MEASUREMENT   T1_NOSE_BULGE=%s" % TAG)
print("=" * 78)

body = bpy.data.objects["T1_body"]
bmw = body.matrix_world
inv = bmw.inverted()
DIR = (inv.to_3x3() @ Vector((-1.0, 0.0, 0.0))).normalized()


def skin_x(y, z, x_min=1.5):
    """outer skin x at (y, z) FORWARD OF x_min, world frame, or None.

    Walks the ray forward past any hit that is behind x_min -- an aperture the
    ray fell through -- so an opening never reads as a surface."""
    ox = 3.5
    for _ in range(8):
        hit, loc, _n, _i = body.ray_cast(inv @ Vector((ox, y, z)), DIR)
        if not hit:
            return None
        wx = (bmw @ loc).x
        if wx > x_min:
            return wx
        return None
    return None


def profile(ob_names, zlo, zhi, label):
    """max world x as a function of |y|, over the objects named, z in [zlo,zhi]."""
    pts = []
    for nm in ob_names:
        for ob in bpy.data.objects:
            if ob.type != 'MESH':
                continue
            if not (ob.name == nm or ob.name.startswith(nm + ".")):
                continue
            mw = ob.matrix_world
            for v in ob.data.vertices:
                c = mw @ v.co
                if zlo <= c.z <= zhi:
                    pts.append((abs(c.y), c.x, c.z))
    if not pts:
        print("  %s: NO VERTICES in z [%.3f, %.3f] -- nothing measured" % (label, zlo, zhi))
        return None
    print("  %s   (z in [%.3f, %.3f], %d verts)" % (label, zlo, zhi, len(pts)))
    out = {}
    for y0 in (0.00, 0.15, 0.30, 0.45, 0.60, 0.70, 0.75):
        s = [p for p in pts if abs(p[0] - y0) < 0.025]
        if not s:
            continue
        out[y0] = max(p[1] for p in s)
    if 0.0 in out:
        print("    " + "  ".join("|y|=%.2f x=%.4f (%+.1f mm)"
                                 % (y, x, 1000 * (x - out[0.0]))
                                 for y, x in sorted(out.items())))
    return out


# ---------------------------------------------------------------- A. bumper
zs = [(bpy.data.objects["bumper_f"].matrix_world @ v.co).z
      for v in bpy.data.objects["bumper_f"].data.vertices]
print("\nA. THE FRONT BUMPER  bumper_f: z %.4f .. %.4f (AG, after step-8b drop)"
      % (min(zs), max(zs)))
ztop = max(zs)
pb = profile(["bumper_f"], ztop - 0.012, ztop + 0.001, "bumper TOP EDGE, max-x(|y|)")
if pb and 0.0 in pb and 0.70 in pb:
    print("    ==> BUMPER plan bulge  x(0) - x(0.70) = %+.2f mm"
          % (1000 * (pb[0.0] - pb[0.70])))

# ---------------------------------------------------------------- B. shell
print("\nB. THE SHELL  T1_body")
for z0 in (0.65, 0.80, 0.95, 1.10):
    ps = profile(["T1_body"], z0 - 0.02, z0 + 0.02, "shell at z=%.2f" % z0)
    if ps and 0.0 in ps and 0.70 in ps:
        print("    ==> SHELL plan bulge at z=%.2f  x(0) - x(0.70) = %+.2f mm"
              % (z0, 1000 * (ps[0.0] - ps[0.70])))
# and at the bumper's own height, so like is compared with like
ps = profile(["T1_body"], ztop - 0.02, ztop + 0.02, "shell at the BUMPER's top-edge height")
if ps and 0.0 in ps and 0.70 in ps:
    print("    ==> SHELL plan bulge at z=%.4f  x(0) - x(0.70) = %+.2f mm"
          % (ztop, 1000 * (ps[0.0] - ps[0.70])))

# ---------------------------------------------------------------- C. fixtures
print("\nC. NOSE FIXTURE BACK FACE vs SKIN AT ITS OWN (y, z)")
print("  %-14s %5s %5s  %8s %8s %8s   %s"
      % ("fixture", "n", "miss", "min mm", "mean mm", "max mm", "back x"))
for nm in ("hl_ring", "hl_lens", "hl_bowl", "ind1_base", "ind1_lens",
           "ind-1_base", "ind-1_lens"):
    for ob in [o for o in bpy.data.objects if o.type == 'MESH'
               and (o.name == nm or o.name.startswith(nm + "."))]:
        mw = ob.matrix_world
        co = [mw @ v.co for v in ob.data.vertices]
        if not co:
            continue
        xmin = min(c.x for c in co)
        back = [c for c in co if c.x - xmin < 0.001]
        gaps, miss = [], 0
        for c in back:
            sx = skin_x(c.y, c.z)
            if sx is None:
                miss += 1
            else:
                gaps.append(c.x - sx)
        if not gaps:
            print("  %-14s %5d %5d   ALL RAYS MISSED -- nothing measured"
                  % (ob.name, len(back), miss))
            continue
        print("  %-14s %5d %5d  %+8.2f %+8.2f %+8.2f   %.4f"
              % (ob.name, len(gaps), miss, 1000 * min(gaps),
                 1000 * sum(gaps) / len(gaps), 1000 * max(gaps), xmin))

print("\n  --- skin stations (forward hits only) ---")
for (y, z, tag) in ((0.000, 0.933, "centreline @ HL_Z"),
                    (0.545, 0.933, "HL station"),
                    (0.675, 1.139, "IND station"),
                    (0.700, 0.950, "|y|=0.70 @ z=0.95")):
    sx = skin_x(y, z)
    print("  %-22s (y %.3f z %.3f)  skin x = %s"
          % (tag, y, z, "%.4f" % sx if sx is not None else "MISS (aperture)"))

print("\n  nose tip (max x over T1_body) = %.5f"
      % max((bmw @ v.co).x for v in body.data.vertices))
