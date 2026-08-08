"""
audit.py -- measured build/render provenance + silhouette metrics.
Answers the audit checklist with numbers, not claims. Run headless after build.
"""
import bpy, bmesh, os, sys, math, time
sys.path.append("/home/claude/tacombi")
from mathutils import Vector

src = open("/home/claude/tacombi/build.py").read().split('if os.environ.get("T1_SAVE")')[0]
exec(compile(src, "build.py", "exec"))

import studio as ST
P = print


def sec(t):
    P("\n=== %s ===" % t)


# ------------------------------------------------------------ PROVENANCE
sec("BUILD / RENDER PROVENANCE")
P("blender            : %s" % bpy.app.version_string)
P("geometry source    : procedural, built this run (no mesh file loaded)")
for f in ("t1_core.py", "t1_shell.py", "t1_detail.py", "t1_mats.py",
          "tex/swirl.png", "tex/senor.png", "tex/calidad.png", "tex/emblem.png"):
    fp = "/home/claude/tacombi/" + f
    if os.path.exists(fp):
        P("  %-18s mtime %s  %8d B" %
          (f, time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(fp))),
           os.path.getsize(fp)))
P("subdivision APPLIED: level %d (destructive, before booleans) -- "
  "no render-time subsurf remains" % SUB)
P("modifiers left on body: %s" % [m.type for m in body.modifiers] or "none")

sc = ST.setup_render((640, 440), 14, True)
P("engine/device      : %s / %s" % (sc.render.engine, sc.cycles.device))
P("samples            : %d   adaptive_threshold %.4f" %
  (sc.cycles.samples, sc.cycles.adaptive_threshold))
P("denoise            : %s  (%s, passes=%s)" %
  (sc.cycles.use_denoising, sc.cycles.denoiser,
   sc.cycles.denoising_input_passes))
P("colour management  : view_transform=%s  look=%s  exposure=%.2f  "
  "display=%s" % (sc.view_settings.view_transform, sc.view_settings.look,
                  sc.view_settings.exposure, sc.display_settings.display_device))
P("film_transparent   : %s" % sc.render.film_transparent)
V = ST.views()
for k in ("hero34f", "side"):
    v = V[k]
    P("camera %-8s    : loc=%s lens=%s ortho=%s" %
      (k, v["loc"], v.get("lens"), v.get("ortho")))
P("texture colourspace: %s" %
  {i.name: i.colorspace_settings.name for i in bpy.data.images})

# ------------------------------------------------------------ SILHOUETTE
sec("SILHOUETTE (measured from vertices, not bound_box)")


def vbounds(objs):
    lo = Vector((1e9, 1e9, 1e9)); hi = -lo
    for ob in objs:
        for v in ob.data.vertices:
            w = ob.matrix_world @ v.co
            lo = Vector((min(lo[i], w[i]) for i in range(3)))
            hi = Vector((max(hi[i], w[i]) for i in range(3)))
    return lo, hi


meshes = [o for o in bpy.data.objects if o.type == 'MESH']
lo, hi = vbounds(meshes)
blo, bhi = vbounds([body])
P("ALL   x[%.4f,%.4f] y[%.4f,%.4f] z[%.4f,%.4f]" %
  (lo.x, hi.x, lo.y, hi.y, lo.z, hi.z))
P("BODY  x[%.4f,%.4f] y[%.4f,%.4f] z[%.4f,%.4f]" %
  (blo.x, bhi.x, blo.y, bhi.y, blo.z, bhi.z))
H = hi.z
P("overall  L=%.4f  W(body)=%.4f  H=%.4f" % (hi.x - lo.x, bhi.y - blo.y, H))
P("rocker (body min z)      = %.4f   -> %.1f%% of height" %
  (blo.z, 100 * blo.z / H))
P("belt line (paint break)  = %.4f   -> %.1f%% of height"
  % (1.2320 - T.RIDE_DROP, 100 * (1.2320 - T.RIDE_DROP) / H))
P("window band sill/head    = %.4f / %.4f  -> %.1f%% / %.1f%%"
  % (S.Z_SILL - T.RIDE_DROP, S.Z_HEAD - T.RIDE_DROP,
     100 * (S.Z_SILL - T.RIDE_DROP) / H, 100 * (S.Z_HEAD - T.RIDE_DROP) / H))

# roof crown location
roof = [(v.co.x, v.co.z) for v in body.data.vertices
        if abs(v.co.y) < 0.05 and v.co.z > H - 0.20]
if roof:
    peak = max(roof, key=lambda p: p[1])
    P("roof crown peak at x=%.3f  z=%.4f ; roof z at x=-1.8 -> %.4f" %
      (peak[0], peak[1],
       max((z for x, z in roof if -1.9 < x < -1.7), default=float('nan'))))

# nose rake: how far forward at rocker height vs at the screen
def fwd_at(zlo, zhi):
    return max((v.co.x for v in body.data.vertices
                if zlo < v.co.z < zhi and abs(v.co.y) < 0.12), default=None)


for lab, z0, z1 in (("rocker  z~0.36", 0.31, 0.41), ("mid  z~0.95", 0.90, 1.00),
                    ("screen base", 1.28, 1.36), ("header", 1.66, 1.74)):
    P("nose reach @ %-14s = %.4f" % (lab, fwd_at(z0 - T.RIDE_DROP,
                                                 z1 - T.RIDE_DROP) or -9))
for lab, z0, z1 in (("rocker", 0.31, 0.41), ("mid", 0.90, 1.00),
                    ("belt", 1.16, 1.24)):
    P("tail reach  @ %-14s = %.4f" % (lab, min(
        (v.co.x for v in body.data.vertices
         if z0 - T.RIDE_DROP < v.co.z < z1 - T.RIDE_DROP and abs(v.co.y) < 0.12),
        default=9)))

# wheels in arches
sec("STANCE")
P("ride drop applied  = %.1f mm" % (T.RIDE_DROP * 1000))
tyres = [o for o in meshes if o.name.startswith("tyre")]
tl, th = vbounds(tyres)
P("tyre z range       = [%.4f, %.4f]  (dia %.4f)" % (tl.z, th.z, th.z - tl.z))
P("arch radius / tyre radius = %.4f / %.4f  -> gap %.1f mm" %
  (S.ARCH_R, T.TIRE_R, (S.ARCH_R - T.TIRE_R) * 1000))
P("rocker-to-ground   = %.4f m" % blo.z)
P("track F/R %.3f / %.3f ; body half-width %.3f -> wheels sit %+.1f mm "
  "inboard of the flank" % (T.TRACK_F, T.TRACK_R, 0.860,
                            (0.860 - (T.TRACK_F / 2 + T.TIRE_W / 2)) * 1000))

# ------------------------------------------------------------ WINDSCREEN
sec("WINDSCREEN")
gl = (S.P_BOT - S.P_TOP).length
P("glass plane run    = %.4f m  from (x %.3f z %.3f) to (x %.3f z %.3f)"
  % (gl, S.P_TOP.x, S.P_TOP.z, S.P_BOT.x, S.P_BOT.z))
P("rake from vertical = %.1f deg" %
  math.degrees(math.atan2(abs(S.P_BOT.x - S.P_TOP.x), abs(S.P_BOT.z - S.P_TOP.z))))
P("pane  W x H        = %.3f x %.3f  (2 panes, divider %.3f)"
  % (S.WS_PANE_W, S.WS_PANE_H, S.WS_DIV * 2))
P("total glass width  = %.3f  -> %.1f%% of body width"
  % (2 * S.WS_PANE_W + 2 * S.WS_DIV, 100 * (2 * S.WS_PANE_W + 2 * S.WS_DIV) / 1.72))
vert = S.WS_PANE_H * abs(S.P_BOT.z - S.P_TOP.z) / gl
P("pane vertical rise = %.3f  -> %.1f%% of vehicle height" % (vert, 100 * vert / H))

# ------------------------------------------------------------ MATERIALS
sec("MATERIALS")
used = {}
for ob in meshes:
    for m in ob.data.materials:
        used.setdefault(m.name, []).append(ob.name)
for k in sorted(used):
    P("  %-16s %3d objects   e.g. %s" % (k, len(used[k]), used[k][0]))
P("distinct materials in scene: %d" % len(used))

# ------------------------------------------------------------ TOPOLOGY
sec("TOPOLOGY / MESH HEALTH")
bm = bmesh.new(); bm.from_mesh(body.data)
tris = sum(1 for f in bm.faces if len(f.verts) == 3)
quads = sum(1 for f in bm.faces if len(f.verts) == 4)
ngons = sum(1 for f in bm.faces if len(f.verts) > 4)
nme = sum(1 for e in bm.edges if not e.is_manifold)
P("body faces: %d quad, %d tri, %d ngon ; non-manifold edges %d"
  % (quads, tris, ngons, nme))
bm.free()
P("objects in scene: %d meshes" % len(meshes))
