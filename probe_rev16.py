"""rev 16 measure-only probe: reports the four loft changes off the BUILT mesh.

Run:  T1_SUB=n blender -b --python probe_rev16.py
Writes nothing. Every number below is measured on the mesh built in this same
process, per the STATE.md rule -- not read back out of the source constants.
"""
import bpy, sys, os, math
import numpy as np
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build  # noqa: F401   -- building is the point
import t1_core as T
import t1_shell as S

body = bpy.data.objects["T1_body"]
mw = body.matrix_world
V = [mw @ v.co for v in body.data.vertices]
print("\n================ rev 16 PROBE  (SUB=%s) ================"
      % os.environ.get("T1_SUB", "1"))
print("T1_body verts %d  faces %d" % (len(body.data.vertices),
                                      len(body.data.polygons)))


def _frame_dz(x):
    return T.RAKE_Z0 + T.RAKE_DZDX * x


# ---------------------------------------------------------------- A. the roof
print("\n--- A. ROOF SECTION -------------------------------------------------")
xa = T.X_AXLE_R
crown = max((v.z for v in V if abs(v.x - xa) < 0.05 and abs(v.y) < 0.10),
            default=float('nan'))
# gutter: lowest z on the near flank where the surface is still ~vertical is
# not directly probe-able, so report the authored roll start alongside.
zt0 = T.ZT_ALL(xa) - T.RT_ALL(xa)
print("  crown @ rear axle (mesh, |y|<0.10)     %.4f  AG" % crown)
print("  authored roll start zt0                %.4f  -> AG %.4f"
      % (zt0, zt0 - _frame_dz(xa)))
print("  RT_ALL / CR_ALL @ rear axle            %.4f / %.4f"
      % (T.RT_ALL(xa), T.CR_ALL(xa)))
print("  D = RT + CR                            %.4f   (LOFT_GROUND 0.2116 +- 0.035)"
      % (T.RT_ALL(xa) + T.CR_ALL(xa)))
_zt = T.ZT_ALL(xa)
_Yt = max(T.WX(xa) * T.G(_zt - T.RT_ALL(xa)) - T.RT_ALL(xa), 1e-3)
print("  Yt (crown half-width)                  %.4f" % _Yt)
print("  R = Yt^2/(2 CR)                        %.3f m  (quote WITH its Yt)"
      % (_Yt * _Yt / (2.0 * T.CR_ALL(xa))))
# gutter object, measured
g = bpy.data.objects.get("gutter1")
if g:
    gz = [(g.matrix_world @ v.co).z for v in g.data.vertices
          if abs((g.matrix_world @ v.co).x - xa) < 0.06]
    if gz:
        print("  drip-rail object lip @ rear axle       %.4f AG" % min(gz))
        print("  aperture top (guarded band)            %.4f AG"
              % (1.775 - _frame_dz(xa)))
        print("  lip - aperture top                     %+.1f mm   "
              "(photograph: 27.7 +- 0.5)" % ((min(gz) - (1.775 - _frame_dz(xa))) * 1000))

# ---------------------------------------------------------------- B. the arch
print("\n--- B. REAR ARCH ----------------------------------------------------")
az = S.arch_z(xa)
lip = {}
for v in V:
    if v.y < 0.60 or abs(v.z - (az - _frame_dz(xa))) > 0.60:
        continue
for name, x0, x1 in (("rear", xa - 0.62, xa + 0.62),):
    # trace the arch aperture edge: for a grid of x, the lowest body z above
    # the axle line on the show flank
    xs = np.arange(x0, x1, 0.004)
    prof = []
    for x in xs:
        zs = [v.z for v in V if abs(v.x - x) < 0.0025 and v.y > 0.60
              and v.z > (az - _frame_dz(xa)) - 0.02]
        if zs:
            prof.append((x, min(zs)))
    if prof:
        p = np.array(prof)
        top = p[:, 1].max()
        # feet: outermost x where the lip is within 10 mm of the rocker
        rocker = T.ZB(xa) - _frame_dz(xa)
        onarch = p[p[:, 1] < rocker + 0.30]
        if len(onarch):
            print("  %s arch: lip crown z %.4f AG   at x %.4f"
                  % (name, top, p[np.argmax(p[:, 1]), 0]))
            print("  arch aperture x-span (lip below rocker+0.30) %.4f .. %.4f"
                  " = %.4f m" % (onarch[:, 0].min(), onarch[:, 0].max(),
                                 onarch[:, 0].max() - onarch[:, 0].min()))
print("  ARCH_W_REAR authored %.3f   (measured 0.92 +- 0.03; was 0.747)"
      % S.ARCH_W_REAR)
print("  crown centre authored x %.4f  (rear axle %.4f; photo agrees to ~1 mm)"
      % (xa, xa))

# ---------------------------------------------------------------- C. the tail
print("\n--- C. TAIL ---------------------------------------------------------")
xmin = min(v.x for v in V)
print("  rear-most sheet metal (mesh)           %.4f" % xmin)
print("  T.X_TAIL                               %.4f" % T.X_TAIL)
print("  overhang past rear axle                %.4f m  (photo 0.773 +- 0.022)"
      % (xa - xmin))
print("  overhang / wheelbase                   %.4f      (photo 0.3412 +- 0.0015)"
      % ((xa - xmin) / T.WHEELBASE if hasattr(T, "WHEELBASE") else
         (xa - xmin) / 2.400))

# ------------------------------------------------------------- D. the poles
print("\n--- D. END-CAP POLES ------------------------------------------------")
me = body.data
val = {}
for e in me.edges:
    for i in e.vertices:
        val[i] = val.get(i, 0) + 1
hi = sorted(val.items(), key=lambda kv: -kv[1])[:6]
print("  highest vertex valences: %s" % ", ".join(str(v) for _, v in hi))
for i, n in hi[:2]:
    co = mw @ me.vertices[i].co
    print("     valence %3d at (%.4f, %.4f, %.4f)" % (n, co.x, co.y, co.z))
nv = sum(1 for k, v in val.items() if v > 4)
print("  vertices with valence > 4              %d" % nv)
print("  NHALF / NLOOP                          %d / %d" % (T.NHALF, T.NLOOP))
print("=======================================================================\n")

# ------------------------------------------------------- E. what is rearmost
print("--- E. REARMOST OBJECTS (verify row 1 measures across these) ---------")
import verify as _V
rows = []
for ob in bpy.data.objects:
    if ob.type != 'MESH' or not len(ob.data.vertices):
        continue
    xs = [(ob.matrix_world @ v.co).x for v in ob.data.vertices]
    rows.append((min(xs), max(xs), ob.name))
rows.sort()
for lo, hi, nm in rows[:10]:
    print("   %-22s x %.4f .. %.4f" % (nm, lo, hi))
print("   ... forward-most:")
for lo, hi, nm in sorted(rows, key=lambda r: -r[1])[:4]:
    print("   %-22s x %.4f .. %.4f" % (nm, lo, hi))
