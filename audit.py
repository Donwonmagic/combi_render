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
# rev 18 -- `H = hi.z` WAS THE RAISED LID STRUT, and it poisoned five numbers.
#
# `hi` is the bound over EVERY mesh in the scene, and the roof lids are modelled
# OPEN, as they serve.  `lid_strut0` spans z 1.8994..3.0169 and `lid_board`
# 1.9381..2.9920, so `hi.z` = 3.0169 -- the top of a strut standing 1.06 m above
# the roof.  STATE.md published that as "overall height ... 3.0169 vs 1.9600 =
# +1056.9 mm OUT" every run, and the four percentages below were percentages of
# a strut, low by a factor 1.9600/3.0169 = 0.6497.
#
# Same class as the `counter_top` phantom this file already carries a comment
# about: a bound taken over a set that quietly contains a prop.  The lid parts
# are all named `lid_*` by t1_shell.roof_lids(), so the exclusion is by
# construction rather than by an enumerated list that can go stale.
_LID_PARTS = tuple(o.name for o in meshes if o.name.startswith("lid_"))
_VEHICLE = [o for o in meshes
            if not o.name.startswith("lid_") and o.name not in
            ("counter", "counter_nosing", "counter_top")]
_vlo, _vhi = vbounds(_VEHICLE)
H = _vhi.z
P("excluded from H: %d open-lid parts %s + the counter"
  % (len(_LID_PARTS), list(_LID_PARTS[:4])))
P("overall  L=%.4f  W(body)=%.4f  H=%.4f  (H over the VEHICLE, lids and counter"
  " excluded; all-mesh max z is %.4f and is the open lid strut)"
  % (hi.x - lo.x, bhi.y - blo.y, H, hi.z))
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
# rev 20, SPEC 10.52.  This row was `ARCH_R - TIRE_R` -- a subtraction of two
# SOURCE CONSTANTS -- so it printed 41.0 mm forever no matter what
# rear_arch_outline built, and it went on printing it for two revisions AFTER
# rev 18 repaired the identical defect in verify.py.  Third instance of the
# shape (`counter_top`'s exclusion, the hardcoded 4.290, this).  Now MEASURED
# on the built mesh with verify's own probe, which returns None rather than an
# endpoint, so "not found" can never be published as a number.
import verify as _VA
_hubz = T.TIRE_R
for _atag, _aax in (("rear", T.X_AXLE_R), ("front", T.X_AXLE_F)):
    _alip = _VA._arch_lip_z(body, _aax, +1, _hubz - 0.02, _hubz + 0.45)
    if _alip is None:
        P("%-5s arch lip     = NOT FOUND at x=%.3f -- this row measured NOTHING"
          % (_atag, _aax))
    else:
        P("%-5s arch lip above hub = %.4f m  -> tyre gap %.1f mm   "
          "[retired constants-only test ARCH_R-TIRE_R would say %.1f]"
          % (_atag, _alip - _hubz, (_alip - _hubz - T.TIRE_R) * 1000,
             (S.ARCH_R - T.TIRE_R) * 1000))
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
# rev 18 -- this row now measures the VEHICLE, not the raised lid strut, and it
# has stopped pretending to be a guard.  Two separate defects were stacked here:
#   (a) H was the max over every mesh, so it read `lid_strut0` at 3.0169 and
#       published `+1056.9 mm OUT` every single run.  Fixed at H's definition.
#   (b) even with the right H, "max over ANY station" is not the quantity
#       H_ROOF = 1.960 named.  1.960 was REF sec.2.3's roof height AT THE REAR
#       AXLE, and on a raked body the max is at a different station entirely.
#       rev 8 spotted this and wrote a prose note under the row -- but left the
#       row emitting OUT.  A prose note is not a guard, and a row that is known
#       to be the wrong test should not carry a target at all.
# rev 22 -- H_ROOF = 1.960 IS NOW RETIRED as an accuracy target (owner's call);
# see the H_ROOF block at the top of verify.py for the chain of withdrawals.
# So there is no longer any roof-height TARGET anywhere in this project, and
# this row's "no target" is now the same kind of statement verify row 1a makes.
# verify row 1a keeps the direct mesh probe as a REGRESSION CATCHER against the
# model's own baseline (1.9835, band +-5 mm) -- it reports that the roof has
# not MOVED, never that it is RIGHT.  The real vehicle's absolute roof height
# is OPEN and UNMEASURED and needs the head-on elevation nobody has.
_hstat = max(((mw @ v.co).z, (mw @ v.co).x)
             for o in _VEHICLE for v in o.data.vertices
             for mw in (o.matrix_world,))
A("| overall height (vehicle max, lids excluded) | %.4f | — *(no target: this "
  "is a max over all stations, and since rev 22 there is no roof-height target "
  "at all — H_ROOF 1.960 is RETIRED, see verify.py. Regression-caught by "
  "verify row 1a and the roof line below)* | at x = %+.3f |"
  % (H, _hstat[1]))
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
A("missing roof-lid curb but a tilt signature — the residual varied by station,")
A("which a scalar cannot express. `Z_BELT` is a line too; see")
A("`t1_mats.z_belt(x)`.")
A("")
A("_rev 18: the three residual figures that used to be quoted in this paragraph")
A("(+12 / −29 / −67 mm) were **hand-authored, and the table below had long since")
A("overtaken them** — this file's own header says nothing in it is typed by")
A("hand. The live numbers are in the table; the mid-wheelbase station has no")
A("roof over it at all because the aperture cuts the crown away there, and this")
A("file used to publish the rocker seen through that hole as the roof height._")
A("")
A("| station | x | roof z | belt z |")
A("|---|---|---|---|")


# rev 18 -- `_roof_at` READ THE ROCKER THROUGH THE ROOF HOLE.
#
# The window is |y| < 0.30, and the roof aperture spans y[-0.5450, +0.5650] over
# x[-1.0700, 0.9640].  At mid-wheelbase the ENTIRE window is inside the hole, so
# there is no roof over it -- and `max()` fell through to whatever else was in
# the x-slab: the rocker.  STATE.md published `roof z at mid wheelbase = 0.3497`,
# an error of -1612.8 mm, with n = 18 selected vertices so the `if zs else nan`
# guard never fired.  A non-empty selection of the WRONG surface.
#
# That is precisely the failure this file's own rev-7 comment describes for
# `reach()` -- "`or -9` hid the empty selection behind a plausible number" --
# reproduced inside the function written to replace it.  A floor is not enough
# on its own either: the fix is to require the selected vertices to be ROOF,
# and to report honestly when there are none rather than returning a number.
#
# _ROOF_FLOOR is the window head in the dropped frame.  Anything above it at
# |y| < 0.30 is roof by construction; the rocker at 0.3497 is 1.36 m below it.
_ROOF_FLOOR = S.Z_HEAD - T.rake_drop(T.X_DROP_REF)


def _roof_at(xq, tol=0.045, count=False):
    zs = [(mw @ v.co).z
          for o in meshes if o.name == "T1_body"
          for v in o.data.vertices
          for mw in (o.matrix_world,)
          if abs((mw @ v.co).x - xq) < tol and abs((mw @ v.co).y) < 0.30
          and (mw @ v.co).z > _ROOF_FLOOR]
    if count:
        return (max(zs) if zs else float('nan')), len(zs)
    return max(zs) if zs else float('nan')


for _lbl, _xq in (("front axle", T.X_AXLE_F),
                  ("mid wheelbase", 0.5 * (T.X_AXLE_F + T.X_AXLE_R)),
                  ("rear axle", T.X_AXLE_R)):
    _rz, _rn = _roof_at(_xq, count=True)
    if _rn == 0:
        # rev 18: say so, do not publish a number.  At mid-wheelbase the crown
        # does not exist -- the roof opening has cut it away -- and the honest
        # report is that the station is inside the aperture, not 0.3497 m.
        A("| %s | %+.3f | — *(inside the roof aperture: no roof above "
          "%.3f m at \\|y\\|<0.30)* | %.4f |" % (_lbl, _xq, _ROOF_FLOOR,
                                                MT.z_belt(_xq)))
    else:
        A("| %s | %+.3f | %.4f *(n=%d)* | %.4f |"
          % (_lbl, _xq, _rz, _rn, MT.z_belt(_xq)))
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
# rev 20, SPEC 10.52.  This row read `| arch radius - tyre radius | 41.0 mm
# (measured 41) |` -- two source constants, plus a HAND-TYPED "(measured 41)"
# asserting a measurement that never happened, in a file whose own header says
# nothing in it is typed by hand.  It sat 68 lines below the real, mesh-measured
# 39.7 mm.  Sourced now from the SAME verify line that publishes that number,
# exactly as `_bayline` is, so there is no second implementation to go stale.
def _arch_gap_mm(tag):
    _l = next((l for l in _glines if ("%s arch lip above hub" % tag) in l), "")
    if "tyre gap" in _l:
        try:
            return float(_l.split("tyre gap")[1].split("mm")[0])
        except ValueError:
            return None
    return None
_rgap, _fgap = _arch_gap_mm("rear"), _arch_gap_mm("front")
A("| rear arch lip → tyre gap (MEASURED on the mesh) | %s |"
  % ("%.1f mm — SPEC §2 locks 41 ± 8" % _rgap if _rgap is not None
     else "**NOT MEASURED — verify's probe returned None**"))
A("| front arch → tyre gap (untouched circular control) | %s |"
  % ("%.1f mm" % _fgap if _fgap is not None
     else "**NOT MEASURED — verify's probe returned None**"))
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
# rev 18 -- THIS SENTENCE CONTRADICTED THE LINE PRINTED FOUR ROWS ABOVE IT.
# It asserted 0.507 / 0.516 / 0.526 and "they are **not** equal" while the live
# bay-width line printed 0.516 0.515 0.516.  rev 13 found the 100 mm origin
# error that produced the apparent taper and settled the bays as EQUAL at
# 0.5155; t1_shell.py:131 says in as many words that STATE.md's taper claim is
# "therefore retired".  It was retired everywhere except in the file this repo
# declares authoritative over all prose, where it was hand-typed.
A("SPEC §1.1's taper (0.507 / 0.516 / 0.526) is **RETIRED** — it was the 100 mm")
A("origin error of rev 13, not a real taper. The bays are EQUAL at 0.5155 m;")
A("the measured widths are printed live in the block above, not typed here.")
A("rev-3's three equal 0.600s are retired too, for a different reason.")
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
