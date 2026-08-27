# adversary rev 68 -- the FOLD ONSET, measured, and the headlamp registration
# re-done against the RECESS rather than the outer skin.
#
# METHOD.  Build ONCE with T1_NOSE_BULGE ~ 0 to recover the base section
# x_b(y,z).  nose_shape() applies  x = x_b + B * w(x) * G(y,z)  where G is the
# only y-dependent factor, so BOTH forms can then be evaluated ANALYTICALLY on
# the recovered base section for any B -- no tree edit, no second build, and
# the reverted form can be tested without restoring it.
import os, sys, numpy as np
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE); os.chdir(HERE)
os.environ["T1_NOSE_BULGE"] = "1e-12"
os.environ.pop("T1_PREVIEW", None)
import bpy, mathutils  # noqa
exec(compile(open("build.py").read(), "build.py", "exec"),
     {"__name__": "__main__", "__file__": "build.py"})

ob = bpy.data.objects["T1_body"]
mw = ob.matrix_world
co = np.array([tuple(mw @ v.co) for v in ob.data.vertices])
nose = co[co[:, 0] > 1.80]
DROP = 0.0855          # ride drop at the nose station, world = undropped - DROP

def section(zw, tol=0.012):
    s = nose[np.abs(nose[:, 2] - zw) < tol]
    prof = []
    for t in np.arange(0.0, 0.9001, 0.02):
        k = np.abs(s[:, 1] - t) < 0.015
        if k.sum():
            prof.append((t, s[k][:, 0].max()))
    return np.array(prof)

def w_of(x):
    u = np.clip((x - 1.86) / 0.17, 0.0, 1.0)
    return u * u * (3 - 2 * u)

print("=" * 78)
print("FOLD ONSET -- x(y) must be NON-INCREASING in |y|.  Base section from a")
print("T1_NOSE_BULGE=0 build; both forms evaluated analytically on it.")
print("=" * 78)
print("%-9s %-9s | %-22s | %s" % ("z world", "z undrop", "SHIPPED  max(0,1-r)",
                                  "REVERTED  max(0,1-r)-max(0,1-r0)"))
for zw in (0.65, 0.75, 0.85, 0.915, 0.95, 1.05, 1.10):
    P = section(zw)
    if len(P) < 12:
        continue
    y, xb = P[:, 0], P[:, 1]
    zu = zw + DROP
    r0 = ((zu - 1.00) / 0.46) ** 2
    r = (y / 0.80) ** 2 + r0
    g = np.maximum(0.0, 1.0 - r)
    g0 = max(0.0, 1.0 - r0)
    w = w_of(xb)
    out = []
    for form, disp in (("SHIPPED", w * g), ("REVERTED", w * (g - g0))):
        onset = None
        for B in np.arange(0.005, 0.401, 0.0025):
            x = xb + B * disp
            if np.any(np.diff(x) > 2e-5):          # 0.02 mm, above tessellation
                onset = B; break
        out.append("no fold to B=0.40" if onset is None else "FOLDS at B=%.4f" % onset)
    print("%-9.3f %-9.3f | %-22s | %s" % (zw, zu, out[0], out[1]))

print()
print("predicted onset for the REVERTED form = 1/[(1-r0)*max w'] , max w' = %.4f/m"
      % (1.5 / 0.17))
print("=" * 78)
print("HEADLAMP REGISTRATION -- against the RECESS, not the outer skin.")
print("(the earlier cast at the lamp's own (y,z) went straight THROUGH the cut")
print(" bore and hit the TAIL at x -1.8702.  REFUSED, not published.)")
ring = np.array([tuple(mw @ v.co) for v in bpy.data.objects["hl_ring"].data.vertices])
cy, cz = ring[:, 1].mean(), ring[:, 2].mean()
rad = np.hypot(ring[:, 1] - cy, ring[:, 2] - cz).max()
print("  hl_ring centre (y %.4f z %.4f) outer radius %.4f  rear-most x %.5f"
      % (cy, cz, rad, ring[:, 0].min()))
mwi = ob.matrix_world.inverted()
for k in (1.05, 1.15, 1.30):
    hits = []
    for a in np.arange(0, 2 * np.pi, np.pi / 12):
        o = mwi @ mathutils.Vector((3.0, cy + rad * k * np.cos(a),
                                    cz + rad * k * np.sin(a)))
        h, loc, _, _ = ob.ray_cast(o, mathutils.Vector((-1, 0, 0)))
        if h:
            hits.append((ob.matrix_world @ loc).x)
    if hits:
        print("  skin at %.2f x ring radius: %d/24 rays hit, x %.5f..%.5f (mean %.5f)"
              "  -> ring rear face %+.1f mm vs mean skin"
              % (k, len(hits), min(hits), max(hits), np.mean(hits),
                 1000 * (ring[:, 0].min() - np.mean(hits))))
print("=" * 78)
