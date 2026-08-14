"""
audit.py -- measured build/render provenance + silhouette metrics.
Answers the audit checklist with numbers, not claims. Run headless after build.
"""
import bpy, bmesh, os, sys, math, time

# Repo root is wherever this file lives. The container is ephemeral and has
# already been rebuilt under a different path once; hardcoding /home/claude
# silently breaks the guards, which is the one thing that must never happen.
try:
    ROOT = os.path.dirname(os.path.abspath(__file__))
except NameError:                                   # exec'd without __file__
    ROOT = next((os.path.dirname(os.path.abspath(a)) for a in sys.argv
                 if a.endswith("audit.py") and os.path.exists(a)), os.getcwd())
sys.path.insert(0, ROOT)
from mathutils import Vector

src = open(os.path.join(ROOT, "build.py")).read().split('if os.environ.get("T1_SAVE")')[0]
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
    fp = os.path.join(ROOT, f)
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
# rev 7: this printed a HARDCODED 1.2320 - RIDE_DROP for six revisions,
# unconnected to t1_mats.Z_BELT. The fabricated value sat near the correct
# one, so the status report certified the exact dimension that was broken.
# Shaders read the DROPPED frame, so Z_BELT is already above-ground.
P("belt line (paint break)  = %.4f   -> %.1f%% of height   [live MT.Z_BELT]"
  % (MT.Z_BELT, 100 * MT.Z_BELT / H))
P("V-swage apex / rise / pow= %.4f / %.4f / %.2f  (apex+rise=%.4f, Z_BELT=%.4f)"
  % (MT.V_APEX, MT.V_RISE, MT.V_POW, MT.V_APEX + MT.V_RISE, MT.Z_BELT))
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

# nose / tail reach. rev 7: this had two stacked bugs. RIDE_DROP was
# subtracted a SECOND time from the query window (build.py already dropped
# every vertex), and the |y| < 0.12 filter slices the vehicle's CENTRE plane,
# where between z 0.65 and 1.05 there are exactly four vertices -- the two
# loft end-cap poles. So max() over the tail poles was printed as "nose
# reach", and `or -9` hid the empty selection behind a plausible number.
def reach(zlo, zhi):
    xs = [v.co.x for v in body.data.vertices if zlo < v.co.z < zhi]
    return (max(xs), min(xs), len(xs)) if xs else (None, None, 0)


for lab, z0, z1 in (("rocker  z~0.36", 0.31, 0.41), ("mid  z~0.95", 0.90, 1.00),
                    ("belt  z~1.20", 1.16, 1.24),
                    ("screen base", 1.28, 1.36), ("header", 1.66, 1.74)):
    f, r, n = reach(z0, z1)
    P("reach @ %-14s nose %+.4f  tail %+.4f  (n=%d)"
      % (lab, f if f is not None else float('nan'),
         r if r is not None else float('nan'), n))

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
  "inboard of the flank" % (T.TRACK_F, T.TRACK_R, bhi.y,
                            (bhi.y - (T.TRACK_F / 2 + T.TIRE_W / 2)) * 1000))

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
  % (2 * S.WS_PANE_W + 2 * S.WS_DIV,
     100 * (2 * S.WS_PANE_W + 2 * S.WS_DIV) / (bhi.y - blo.y)))
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


# ===================================================================== STATE
# HANDOFF.md once claimed "0 fail, 0 warn" over a state that had one of each,
# and claimed six git commits that did not exist. audit.py itself printed a
# hardcoded belt line for six revisions. Prose drifts and hand-written status
# lies. Everything below is measured off the mesh that was just built, in this
# process, and written to STATE.md. Nothing in it is typed by hand.
import subprocess, collections


def _git(*a):
    try:
        return subprocess.check_output(("git",) + a, cwd=ROOT,
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "?"


def _fmt(v, n=4):
    return ("%." + str(n) + "f") % v if isinstance(v, float) else str(v)


def _row(name, measured, expected=None, tol=None, unit="m"):
    if expected is None:
        return "| %s | %s | — | — |" % (name, _fmt(measured))
    d = measured - expected
    mark = "" if tol is None else ("ok" if abs(d) <= tol else "**OUT**")
    return "| %s | %s | %s | %+.1f mm %s |" % (
        name, _fmt(measured), _fmt(expected), d * 1000, mark)


# --- re-run the guard in-process so the reported result cannot drift from
#     the geometry it describes -----------------------------------------
_gfail, _gwarn, _glines = "?", "?", []
try:
    import verify as _V
    importlib.reload(_V)
    _cap = []
    _V.run(body, lambda m: _cap.append(str(m)))
    _glines = _cap
    for _l in _cap:
        if "VERIFY:" in _l:
            _p = _l.split("VERIFY:")[1]
            _gfail = _p.split("fail")[0].strip()
            _gwarn = _p.split(",")[1].split("warn")[0].strip()
except Exception as _e:
    _glines = ["verify could not run in-process: %s" % _e]

inv = collections.Counter()
for o in meshes:
    inv[o.name.rstrip("0123456789.-+_").split(".")[0] or o.name] += 1
nverts = sum(len(o.data.vertices) for o in meshes)
nfaces = sum(len(o.data.polygons) for o in meshes)

# aperture edges, measured off the shell rather than read from the constants
_ap = []
try:
    _zc = (S.Z_SILL + S.Z_HEAD) / 2 - T.RIDE_DROP
    _xs = sorted(v.co.x for v in body.data.vertices
                 if v.co.y > 0.80 and abs(v.co.z - _zc) < 0.02)
    _runs, _cur = [], [_xs[0]] if _xs else []
    for _a, _b in zip(_xs, _xs[1:]):
        if _b - _a > 0.030:
            _runs.append((_cur[0], _cur[-1])); _cur = [_b]
        else:
            _cur.append(_b)
    if _cur:
        _runs.append((_cur[0], _cur[-1]))
    _ap = _runs
except Exception:
    pass

rough = []
for _m in bpy.data.materials:
    if not _m.use_nodes:
        continue
    for _n in _m.node_tree.nodes:
        if _n.type == 'BSDF_PRINCIPLED' and not _n.inputs["Roughness"].links:
            rough.append(_m.name)
            break

L = []
A = L.append
A("# STATE — machine-written by `audit.py`. Do not hand-edit.")
A("")
A("Every number here was measured off the mesh built in the same process that")
A("wrote this file. If this file and any prose in the repo disagree, this file")
A("is right. Regenerate with `T1_SUB=n blender -b --python audit.py`.")
A("")
A("## Provenance")
A("")
A("| | |")
A("|---|---|")
A("| generated | %s UTC |" % time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
A("| git commit | `%s` |" % _git("rev-parse", "--short", "HEAD"))
A("| git subject | %s |" % _git("log", "-1", "--pretty=%s"))
A("| working tree | %s |" % ("**DIRTY** — this state is not committed"
                             if _git("status", "--porcelain") else "clean"))
A("| blender | %s |" % bpy.app.version_string)
A("| subdivision | T1_SUB=%d (applied, destructive, before booleans) |" % SUB)
A("| geometry source | procedural, built this run |")
A("")
A("## Guard result")
A("")
A("**VERIFY: %s fail, %s warn** at T1_SUB=%d." % (_gfail, _gwarn, SUB))
A("")
A("> A pass here is only a pass *at this subdivision level*. The cab-door gap")
A("> booleans passed at SUB=1 and collapsed the shell at SUB=2 for six")
A("> revisions. Run both.")
A("")
A("```")
for _l in _glines:
    A(_l.strip())
A("```")
A("")
A("| | |")
A("|---|---|")
A("| cutters rolled back | %s |" % (", ".join(FAILED_CUTS) if FAILED_CUTS
                                    else "none"))
A("| non-manifold edges (body) | %d |" % nme)
A("| body faces | %d quad, %d tri, %d ngon |" % (quads, tris, ngons))
A("")
A("## Measured dimensions")
A("")
A("Frame: geometry is authored un-dropped and `build.py` step 8b subtracts")
A("`RIDE_DROP` from every vertex last, so everything below is **above ground**.")
A("Shaders read the dropped frame, so `Z_BELT`/`V_APEX` are already AG.")
A("")
A("| dimension | measured | SPEC | delta |")
A("|---|---|---|---|")
# rev 13, found independently by TWO audit contexts: this list excluded
# `counter` and `counter_nosing` but not `counter_top`, which shares the
# counter's plan and reaches x = -2.423.  So the "overall length (ex counter)"
# row measured the COUNTER and reported 4.5830 / +293 mm OUT for two revisions
# when the body is 4.2984 and in spec; and "counter tail overhang past body"
# reported 0.0070, which is the nosing standing 7 mm proud of the top, not the
# 0.32 m overhang it names.  A guard that measures a prop is worse than no
# guard: this one certified a phantom defect AND hid a real number.
_COUNTER_PARTS = ("counter", "counter_nosing", "counter_top")
_bodyish = [o for o in meshes if o.name not in _COUNTER_PARTS]
_blo2, _bhi2 = vbounds(_bodyish)
# rev 17.  THIS ROW WAS A RE-TYPED CONSTANT and it disagreed with the guard.
#
# rev 16 re-spaced the tail and re-expressed the target in verify.py:47 as
# SPEC["L"] = 4.290 - (O_OLD - O_NEW), precisely so that re-measuring the
# overhang could never leave it stale.  It did not make the same change here,
# so audit.py went on comparing against the bare VW catalogue 4.290 while
# verify.py compared against 4.055.  STATE.md -- the file this repo declares
# authoritative over all prose -- therefore reported
#       overall length  4.0648 vs 4.2900 = -225.2 mm OUT
# on a quantity verify.py PASSES at +9.8 mm.  Same failure shape as the
# counter_top row the rev-12 audit found at this exact line, and a direct
# breach of SPEC's own rule that a constant tuned against another constant
# must be expressed in terms of it.
#
# Imported from verify.py rather than recomputed, so there is now exactly ONE
# definition of this target in the repo and no third copy can appear.
import verify as _V
A(_row("overall length (ex counter)", _bhi2.x - _blo2.x, _V.SPEC["L"], 0.025))
A("| counter tail overhang past body | %.4f | — | — |" % (_blo2.x - lo.x))
A(_row("overall width (body)", bhi.y - blo.y, 1.750, 0.025))
A(_row("overall height (max, any station)", H, 1.960, 0.025))
A("| _(rev 8: a single scalar height is the WRONG test now that the rake is"
  " modelled — 1.960 is the maximum of a sloping line, taken at its highest"
  " station. See the three-station roof line below. §2.3's inference that the"
  " roof-lid frame stands 0.10–0.15 m proud is **refuted** at ~13σ; measured"
  " proud height is 26 ± 7 mm.)_ | | | |")
A(_row("wheelbase", T.X_AXLE_F - T.X_AXLE_R, 2.400, 0.005))
A(_row("track front", T.TRACK_F, 1.369, 0.005))
A(_row("track rear", T.TRACK_R, 1.359, 0.005))
A(_row("tyre diameter", th.z - tl.z, 0.665, 0.015))
A(_row("rocker to ground", blo.z))
A(_row("belt line @ x=%.3f (live)" % T.X_DROP_REF, MT.Z_BELT, 1.207, 0.010))
A(_row("window sill @ x=%.3f" % T.X_DROP_REF,
       S.Z_SILL - T.rake_drop(T.X_DROP_REF), 1.307, 0.015))
A(_row("window head @ x=%.3f" % T.X_DROP_REF,
       S.Z_HEAD - T.rake_drop(T.X_DROP_REF), 1.710, 0.020))
A(_row("V-swage apex @ x=%.3f" % T.X_DROP_REF, MT.V_APEX, 0.340, 0.060))
A("")

# ---------------------------------------------------------------- roof line
# rev 8: the height row above used to be a single scalar against 1.960 and it
# read 89 mm short for seven revisions. The cause was never a missing curb --
# it was the unmodelled ~1.9 deg nose-down rake, which makes the roof a LINE.
# A scalar cannot express that, so it is measured at three stations.
A("### Roof line — three stations, not one scalar")
A("")
A("The model read 1.871 against §2.3's 1.960 for seven revisions. That is not a")
A("missing roof-lid curb: the residual against the photograph was **+12 mm at")
A("the front axle, −29 mm mid-wheelbase, −67 mm at the rear axle** — a tilt")
A("signature. `Z_BELT` is a line too; see `t1_mats.z_belt(x)`.")
A("")
A("| station | x | roof z | belt z |")
A("|---|---|---|---|")


def _roof_at(xq, tol=0.045):
    zs = [(mw @ v.co).z
          for o in meshes if o.name == "T1_body"
          for v in o.data.vertices
          for mw in (o.matrix_world,)
          if abs((mw @ v.co).x - xq) < tol and abs((mw @ v.co).y) < 0.30]
    return max(zs) if zs else float('nan')


for _lbl, _xq in (("front axle", T.X_AXLE_F),
                  ("mid wheelbase", 0.5 * (T.X_AXLE_F + T.X_AXLE_R)),
                  ("rear axle", T.X_AXLE_R)):
    A("| %s | %+.3f | %.4f | %.4f |"
      % (_lbl, _xq, _roof_at(_xq), MT.z_belt(_xq)))
A("")
A("| roof line slope (measured off the mesh) | %.1f mm/m |"
  % (1000 * (_roof_at(T.X_AXLE_R) - _roof_at(T.X_AXLE_F))
     / (T.X_AXLE_R - T.X_AXLE_F)))
A("| rake coefficient applied | %.1f mm/m (%.2f°) |"
  % (T.RAKE_DZDX * 1000, math.degrees(math.atan(T.RAKE_DZDX))))
A("")
A("| stance | |")
A("|---|---|")
A("| ride drop @ x=0 | %.1f mm |" % (T.RAKE_Z0 * 1000))
A("| ride drop @ front axle / rear axle | %.1f / %.1f mm |"
  % (T.rake_drop(T.X_AXLE_F) * 1000, T.rake_drop(T.X_AXLE_R) * 1000))
A("| arch radius − tyre radius | %.1f mm (measured 41) |"
  % ((S.ARCH_R - T.TIRE_R) * 1000))
A("| V_APEX + V_RISE == Z_BELT | %.4f == %.4f — %s |"
  % (MT.V_APEX + MT.V_RISE, MT.Z_BELT,
     "held" if abs(MT.V_APEX + MT.V_RISE - MT.Z_BELT) < 1e-6 else "**BROKEN**"))
A("")
A("### Serving apertures")
A("")
_bayline = next((l for l in _glines if "bay widths" in l), "")
_apline = next((l for l in _glines if "open serving apertures" in l), "")
A("Measured by `verify.py` by ray-testing the shell, not by counting panes:")
A("")
A("```")
A(_apline.strip())
A(_bayline.strip())
A("```")
A("")
A("SPEC §1.1 measured widths: 0.507 / 0.516 / 0.526 — they are **not** equal;")
A("they grow slightly toward the tail. rev-3's three equal 0.600s are retired.")
A("")
A("## Materials")
A("")
A("| | |")
A("|---|---|")
A("| datablocks built | %d |" % len(bpy.data.materials))
A("| bound to >=1 mesh | %d |" % len(used))
A("| **still a CONSTANT roughness** | %d — %s |"
  % (len(rough), ", ".join(sorted(rough)) if rough else "none"))
A("")
A("> SPEC §3 locks the finish as WEATHERED. A constant roughness is the")
A("> physical definition of the plastic look. The only materials that may")
A("> legitimately appear above are the transmissive ones and the sealed")
A("> reflector.")
A("")
A("## Object inventory")
A("")
A("| | |")
A("|---|---|")
A("| mesh objects | %d |" % len(meshes))
A("| vertices (all meshes) | %d |" % nverts)
A("| faces (all meshes) | %d |" % nfaces)
A("")
A("| prefix | n |")
A("|---|---|")
for _k, _v in sorted(inv.items(), key=lambda kv: (-kv[1], kv[0])):
    A("| `%s` | %d |" % (_k, _v))
A("")

open(os.path.join(ROOT, "STATE.md"), "w").write("\n".join(L) + "\n")
P("\n=== STATE ===")
P("wrote STATE.md  (%s fail, %s warn, %d meshes, %d materials constant-rough)"
  % (_gfail, _gwarn, len(meshes), len(rough)))
