# adversary rev 68 -- three mesh questions, one build.
#   (b) the BUILT bumper_f crown: max-x as a function of y over |y| <= 0.70
#   (7) does the SHIPPED nose_shape() fold?  and where would the reverted form?
#   (8) fixture-to-skin registration AT THE SHIPPED BULGE (not a moved one)
# Run with:  T1_SUB=1 /tmp/blender/blender -b -P probe_scratch/adv68_mesh.py
import os, sys, numpy as np
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
os.chdir(HERE)
os.environ.pop("T1_PREVIEW", None)
import bpy  # noqa
src = open(os.path.join(HERE, "build.py")).read()
import __main__
exec(compile(src, "build.py", "exec"),
     {"__name__": "__main__", "__file__": "build.py"})

def verts(name):
    ob = bpy.data.objects.get(name)
    if ob is None:
        return None
    mw = ob.matrix_world
    return np.array([tuple(mw @ v.co) for v in ob.data.vertices])

print("=" * 78)
print("(b) BUILT bumper_f -- crown plan profile, WORLD frame")
bf = verts("bumper_f")
if bf is None:
    print("    NO bumper_f")
else:
    print("    n verts %d   x %.5f..%.5f   y %.4f..%.4f   z %.4f..%.4f"
          % (len(bf), bf[:,0].min(), bf[:,0].max(), bf[:,1].min(),
             bf[:,1].max(), bf[:,2].min(), bf[:,2].max()))
    xs = []
    for t in np.arange(-0.70, 0.7001, 0.05):
        m = np.abs(bf[:,1] - t) < 0.025
        if m.sum():
            xs.append((t, bf[m][:,0].max()))
    print("    y -> max x :")
    for t, x in xs:
        print("       y=%+.3f  x=%.5f" % (t, x))
    v = np.array([x for _, x in xs])
    print("    PLAN BULGE of the BUILT FRONT BUMPER over |y|<=0.70 : %.4f mm"
          % (1000 * (v.max() - v.min())))

print("=" * 78)
print("(7) SHIPPED nose_shape(): is the plan section x(y) monotone?  T1_NOSE_BULGE=%s"
      % os.environ.get("T1_NOSE_BULGE", "shipped 0.019"))
body = verts("T1_body")
nose = body[body[:,0] > 1.80]
for z0 in (0.65, 0.80, 0.915, 0.95, 1.10):
    m = np.abs(nose[:,2] - z0) < 0.02
    s = nose[m]
    if len(s) < 20:
        continue
    prof = []
    for t in np.arange(0.0, 0.9001, 0.03):
        k = np.abs(s[:,1] - t) < 0.02
        if k.sum():
            prof.append((t, s[k][:,0].max()))
    if len(prof) < 4:
        continue
    y = np.array([p[0] for p in prof]); x = np.array([p[1] for p in prof])
    d = np.diff(x)
    rises = [(y[i+1], 1000*d[i]) for i in range(len(d)) if d[i] > 1e-5]
    print("  z=%.3f  n=%3d  x(0)=%.5f x(0.70)=%.5f  bulge %+.1f mm | "
          "outward RISES: %s"
          % (z0, len(s), x[0], np.interp(0.70, y, x),
             1000*(x[0] - np.interp(0.70, y, x)),
             ("NONE -- monotone" if not rises else
              "; ".join("y=%.2f +%.2f mm" % r for r in rises))))

print("=" * 78)
print("(8) FIXTURE-TO-SKIN REGISTRATION AT THE SHIPPED BULGE")
ob = bpy.data.objects.get("T1_body")
import mathutils
dg = bpy.context.evaluated_depsgraph_get()
for nm in ("ind1_base", "ind-1_base", "hl_lens", "hl_ring", "hl_bowl1"):
    v = verts(nm)
    if v is None:
        continue
    # cast from well forward of the fixture, straight back along -x, at the
    # fixture's own centroid (y,z), and report where the BODY skin is
    c = v.mean(axis=0)
    org = mathutils.Vector((3.0, c[1], c[2]))
    hit, loc, nor, idx = ob.ray_cast(ob.matrix_world.inverted() @ org,
                                     mathutils.Vector((-1, 0, 0)))
    skin = (ob.matrix_world @ loc).x if hit else float("nan")
    print("  %-12s centroid (%.4f, %+.4f, %.4f)  rear-most x %.4f  front-most x %.4f"
          "  |  skin x %.4f  ->  fixture rear face is %+.1f mm from skin"
          % (nm, c[0], c[1], c[2], v[:,0].min(), v[:,0].max(), skin,
             1000*(v[:,0].min() - skin)))
print("=" * 78)
