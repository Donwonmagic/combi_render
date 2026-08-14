"""rev 19 -- ABLATE THE FADE PATH BEFORE BUILDING A MAP ON IT.

The standing rule (SPEC 10.31): before scheduling a solve on a constant,
ablate it to zero and re-measure.  `W_ALBEDO` was solved for three revisions
before one render showed the shipped arm and the zero arm were the same number.

The cream mottle map is going to modulate `FadeVert` SPATIALLY.  That is only
worth doing if `FadeVert` has authority over the rendered cream's L* and C* in
the first place.  This file swings it 0.00 / 0.50 / 1.00 and measures.

Everything is rendered plain-sRGB (Standard, look None, gamma 1) and decoded
back to linear in numpy, exactly as shader_solve.py does, so a "linear ratio"
here means the same as one measured off the photograph.

THE MASK IS RENDERED, NOT BOXED -- only the objects carrying the `cream`
material are visible in the measured render, so no neighbour can leak in.
That is the rev-15 lesson: the first mural probe read the cream lid skin
THROUGH the board because only the mask was isolated, not the render.

    T1_FADEV=0.0 blender -b --python fadev_ablate.py
"""
import bpy, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
src = open(os.path.join(ROOT, "build.py")).read().split('if os.environ.get("T1_SAVE")')[0]
exec(compile(src, "build.py", "exec"))
import studio as ST
import shader_solve as SS          # reuse _render/_only/_objs_with_material

FADEV = float(os.environ.get("T1_FADEV", 0.50))
RES = (900, 620)
SAMP = int(os.environ.get("T1_ABL_SAMP", 48))


def _lab(rgb_lin):
    M = np.array([[0.4124, 0.3576, 0.1805],
                  [0.2126, 0.7152, 0.0722],
                  [0.0193, 0.1192, 0.9505]])
    XYZ = rgb_lin @ M.T
    t = XYZ / np.array([0.9505, 1.0, 1.089]); d = 6 / 29
    f = np.where(t > d ** 3, np.cbrt(np.clip(t, 1e-9, None)), t / (3 * d * d) + 4 / 29)
    L = 116 * f[..., 1] - 16
    A = 500 * (f[..., 0] - f[..., 1]); B = 200 * (f[..., 1] - f[..., 2])
    return L, np.sqrt(A * A + B * B)


def cam():
    v = ST.views()["side"]
    c = bpy.data.objects.get("cam_side") or bpy.context.scene.camera
    ST.aim(c, v["loc"], v["tgt"], v.get("lens"), v.get("ortho"))
    bpy.context.scene.camera = c


objs = SS._objs_with_material("cream")
if not objs:
    raise SystemExit("FATAL: no objects carry the 'cream' material")
print("cream objects: %d  (%s)" % (len(objs), ", ".join(o.name for o in objs[:6])))

restore = SS._only(objs)
cam()
a = SS._render(os.path.join(ROOT, "out", "fadev_%0.2f" % FADEV), RES, SAMP,
               transparent=True)
restore()

rgb = a[..., :3]; al = a[..., 3]
m = al > 0.98                                   # fully covered pixels only
for _ in range(3):                              # erode 3 px: no edge pixels
    q = m.copy()
    q[1:, :] &= m[:-1, :]; q[:-1, :] &= m[1:, :]
    q[:, 1:] &= m[:, :-1]; q[:, :-1] &= m[:, 1:]
    m = q
n = int(m.sum())
lin = SS.srgb_to_lin(rgb)
clip = float((rgb.max(2) >= 0.995)[m].mean()) if n else float("nan")
L, C = _lab(lin)
Y = lin @ np.array([0.2126, 0.7152, 0.0722])

print("=" * 70)
print("FADEV ABLATION   T1_FADEV = %.2f   samples %d" % (FADEV, SAMP))
print("  rendered mask: %d px fully covered after a 3 px erosion" % n)
print("  clipped fraction inside the mask: %.2f %%" % (100 * clip))
if n < 2000:
    print("  *** too few px -- refusing to report.  Returns nothing.")
    raise SystemExit(0)
print("  mean L* %8.4f     mean C* %8.4f" % (L[m].mean(), C[m].mean()))
print("  sd   L* %8.4f     sd   C* %8.4f" % (L[m].std(), C[m].std()))
for sg in (2.0, 4.0, 8.0):
    lo = SS.gblur(Y, sg)
    r = float(np.sqrt((((Y - lo) / np.maximum(lo, 1e-9))[m] ** 2).mean()))
    print("  high-pass RMS sigma %4.1f px : %8.4f %%" % (sg, 100 * r))
print("=" * 70)
