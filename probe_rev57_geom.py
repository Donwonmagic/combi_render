"""rev 57 -- pull the BUILT nose roundel out of the scene as 2-D polygons.

Ask the MESH, not the constants (rule 10).  vw_ring and the two vwbar prisms
are revolved/extruded about X, so the badge lies in the Y-Z plane.  Writes
probe_scratch/rev57_glyph.npz for the pure-numpy measurement to consume, so
the estimator can be iterated without re-running Blender.
"""
import bpy, os, sys, math
import numpy as np
ROOT = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, ROOT)
os.environ.setdefault("T1_SUB", "1")
exec(compile(open(os.path.join(ROOT, "build.py")).read(), "build.py", "exec"))
P = print

def polys2d(ob):
    """world-space (y,z) polygons of every face whose normal is +-X-ish, i.e.
    the FACE of the pressing -- the silhouette the photograph sees."""
    M = ob.matrix_world
    out = []
    for p in ob.data.polygons:
        n = (M.to_3x3() @ p.normal)
        if abs(n.x) < 0.5 * max(1e-9, n.length):
            continue
        out.append(np.array([[(M @ ob.data.vertices[i].co).y,
                              (M @ ob.data.vertices[i].co).z]
                             for i in p.vertices]))
    return out

def allpts(ob):
    M = ob.matrix_world
    return np.array([[(M @ v.co).y, (M @ v.co).z] for v in ob.data.vertices])

ring = bpy.data.objects.get("vw_ring")
bars = [o for o in bpy.data.objects if o.name.startswith("vwbar")]
disc = bpy.data.objects.get("vw_disc")
P("objects: vw_ring=%s  vw_disc=%s  bars=%s"
  % (ring and ring.name, disc and disc.name, [b.name for b in bars]))

rp = allpts(ring)
cy, cz = rp[:, 0].mean(), rp[:, 1].mean()
r = np.hypot(rp[:, 0] - cy, rp[:, 1] - cz)
P("ring centre (y,z) = %.6f %.6f" % (cy, cz))
P("ring radius: min %.6f  max %.6f  (outer R = max)" % (r.min(), r.max()))
R_OUT = r.max()
P("RING OUTER D (built, off the mesh) = %.6f m" % (2 * R_OUT))
P("ROUNDEL_D constant                 = %.6f m" % ROUNDEL_D)
P("  agree to %.3e m" % abs(2 * R_OUT - ROUNDEL_D))

bpol = []
for b in bars:
    bpol.extend(polys2d(b))
P("bar face-polygons captured: %d" % len(bpol))
bp = np.vstack([allpts(b) for b in bars])
rb = np.hypot(bp[:, 0] - cy, bp[:, 1] - cz)
P("glyph extreme radius / ring outer R = %.6f  (vw_logo_fit targets 0.84)"
  % (rb.max() / R_OUT))

np.savez(os.path.join(ROOT, "probe_scratch", "rev57_glyph.npz"),
         cy=cy, cz=cz, R_OUT=R_OUT, ROUNDEL_D=ROUNDEL_D,
         polys=np.array([p for p in bpol], dtype=object),
         nring=len(rp))
P("wrote probe_scratch/rev57_glyph.npz")
