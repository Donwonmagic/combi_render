"""
Master build - Tacombi Playa combi, per SPEC.md rev 3.

  loft -> subsurf -> nose swage -> arches -> solidify -> apertures -> gaps
       -> glass/seals -> ragtop -> counter -> galley -> brightwork -> mats
"""
import bpy, bmesh, math, os, sys, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from mathutils import Vector

bpy.ops.wm.read_factory_settings(use_empty=True)

import importlib
import t1_core as T;   importlib.reload(T)
import t1_shell as S;  importlib.reload(S)
import t1_detail as D; importlib.reload(D)
import t1_mats as MT;  importlib.reload(MT)

t0 = time.time()
def log(m):
    print(f"[{time.time()-t0:7.1f}s] {m}", flush=True)

SUB = int(os.environ.get("T1_SUB", "2"))
ASSIGN = []
FAILED_CUTS = []


def A(objs, key):
    if not isinstance(objs, (list, tuple)):
        objs = [objs]
    for o in objs:
        if o.type == 'MESH':
            o.data.shade_smooth()
        ASSIGN.append((o, key))
    return objs


# --------------------------------------------------------------- boolean guard
# The old guard was `after < before * 0.6`.  Measured, the worst LEGITIMATE
# vertex ratio is 0.9902 (SUB=1) / 0.9862 (SUB=2), so a cutter could delete
# 39 % of the shell and pass.  Worse, a NO-OP boolean passed silently: a cutter
# entirely outside the shell gives dv = 0 and the guard never fired.
#
# The obvious digest does NOT work.  EXACT re-tessellates n-gons even on a true
# no-op, giving df = +9 and a spurious dVolume of -3.38e-06 m^3.  Vertex-count
# equality is the only clean count test, and there must be no dVolume floor
# below 1e-5 m^3.  Connected-component count is also useless here -- it
# legitimately goes 1 -> 6 as each gap cutter frees a panel.
#
# Thresholds below were checked against all 44 measured (cutter, level) rows:
# 2 true positives, 0 false positives.
#
#   test                        threshold   worst legitimate   margin
#   pre: cutter volume          >= 1.0e-4   0.004838 (cargo_mid)   48x
#   pre: cutter bbox n body     overlap     all 22 overlap          -
#   vertex ratio                >= 0.95     0.9862                3.6x
#   face ratio                  >= 0.95     0.9849                3.3x
#   dv != 0 (no-op)             strict      min |dv| = 64          64 v
#   non-manifold edges          no increase 0 -> 0 on all 22   unbounded
#   loose verts / zero-area f   no increase 0 after all 22    unbounded
#   kind="aperture": df < 0     strict      -33                    33 f
#   kind="gap":      dv > 0     strict      +240                  240 v
V_RATIO_MIN = 0.95
F_RATIO_MIN = 0.95
CUTTER_VOL_MIN = 1.0e-4
# 1e-12 m2 = a 1 um square: TRULY degenerate, the kind that breaks normals.
# NOT 1e-9.  Measured: the corrected bay 1 has its front edge at x = 0.1950,
# which is EXACTLY the level-1 subsurf midpoint of stations 0.120 and 0.270,
# so the cutter plane is coincident with a mesh edge loop and EXACT emits 9
# slivers of 2.53e-11 ... 4.68e-10 m2 (5-20 um across) on the aperture rim,
# deterministically, at both subdivision levels.  That is a coincidence
# artefact on 9 of 53 000 faces, not a shred -- a shred is caught by the
# vertex ratio with four orders of magnitude to spare.  1e-12 clears the
# worst observed sliver by 25x and still fires on an exactly-zero face.
ZERO_AREA = 1e-12


def _digest(me):
    """cheap numpy health digest of a mesh: (nonmanifold_e, loose_v, zeroA_f)"""
    import numpy as np
    nv, ne, nf = len(me.vertices), len(me.edges), len(me.polygons)
    if ne == 0:
        return (0, nv, 0)
    # faces per edge, via the loop -> edge map.  != 2 is non-manifold for a
    # closed surface (wire, boundary or bowtie all land here).
    nl = len(me.loops)
    li = np.empty(nl, dtype=np.int32)
    me.loops.foreach_get("edge_index", li)
    fpe = np.bincount(li, minlength=ne)
    nonman = int((fpe != 2).sum())
    # loose verts: not referenced by any edge
    ev = np.empty(ne * 2, dtype=np.int32)
    me.edges.foreach_get("vertices", ev)
    used = np.bincount(ev, minlength=nv)
    loose = int((used == 0).sum())
    # zero-area faces
    ar = np.empty(nf, dtype=np.float64)
    me.polygons.foreach_get("area", ar)
    zero = int((ar < ZERO_AREA).sum())
    return (nonman, loose, zero)


def _volume(ob):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    v = bm.calc_volume(signed=False)
    bm.free()
    return v


def _bbox_overlap(a, b, eps=1e-6):
    A = [a.matrix_world @ Vector(c) for c in a.bound_box]
    B = [b.matrix_world @ Vector(c) for c in b.bound_box]
    for i in range(3):
        if min(v[i] for v in A) > max(v[i] for v in B) + eps:
            return False
        if min(v[i] for v in B) > max(v[i] for v in A) + eps:
            return False
    return True


def cut(target, cutters, tag, kind="aperture"):
    """one cutter at a time, with a sanity guard -- a failed EXACT boolean
    silently shreds the mesh, which is how the pickup-era build lost its roof.

    kind="aperture"  a hole: the face count must go DOWN
    kind="gap"       a panel-gap slot: it frees a panel, vert count goes UP
    """
    wv, wf, wvol = 1e9, 1e9, 1e9
    for c in cutters:
        bad = []
        # ---------------------------------------------------------- pre
        vol = _volume(c)
        wvol = min(wvol, vol)
        if vol < CUTTER_VOL_MIN:
            bad.append(f"cutter volume {vol:.3e} m3 < {CUTTER_VOL_MIN:.1e}")
        if not _bbox_overlap(target, c):
            bad.append("cutter bbox does not overlap the body bbox")
        if bad:
            log(f"  !! CUTTER REJECTED {c.name}: " + "; ".join(bad))
            FAILED_CUTS.append(c.name)
            bpy.data.objects.remove(c, do_unlink=True)
            continue

        keep = target.data.copy()
        bv, bf = len(target.data.vertices), len(target.data.polygons)
        bnm, blo, bza = _digest(target.data)

        T.boolean(target, c)
        T.apply_mods(target)

        av, af = len(target.data.vertices), len(target.data.polygons)
        anm, alo, aza = _digest(target.data)

        # --------------------------------------------------------- post
        if bv:
            wv = min(wv, av / bv)
        if bf:
            wf = min(wf, af / bf)
        if bv and av < bv * V_RATIO_MIN:
            bad.append(f"vertex ratio {av/bv:.4f} < {V_RATIO_MIN}"
                       f" ({bv} -> {av}v)")
        if bf and af < bf * F_RATIO_MIN:
            bad.append(f"face ratio {af/bf:.4f} < {F_RATIO_MIN}"
                       f" ({bf} -> {af}f)")
        if av == bv:
            bad.append(f"NO-OP: dv = 0 at {bv}v -- the cutter removed nothing")
        if anm > bnm:
            bad.append(f"non-manifold edges {bnm} -> {anm}")
        if alo > blo:
            bad.append(f"loose verts {blo} -> {alo}")
        if aza > bza:
            bad.append(f"zero-area faces {bza} -> {aza}")
        if kind == "aperture" and af >= bf:
            bad.append(f"aperture did not open a hole: df = {af-bf:+d}")
        if kind == "gap" and av <= bv:
            bad.append(f"gap did not free a panel: dv = {av-bv:+d}")

        if bad:
            log(f"  !! BOOLEAN REJECTED {c.name} ({kind}): " + "; ".join(bad)
                + "  -- ROLLED BACK")
            old = target.data
            target.data = keep
            bpy.data.meshes.remove(old)
            FAILED_CUTS.append(c.name)
        else:
            bpy.data.meshes.remove(keep)
        bpy.data.objects.remove(c, do_unlink=True)
    log(f"cut {tag}: {len(target.data.vertices)}v"
        f"   worst v-ratio {wv:.4f} f-ratio {wf:.4f} vol {wvol:.3e}")


# ------------------------------------------------------------------- 1 shell
log("lofting Kombi shell")
body = T.build_kombi()
m = body.modifiers.new("sub", 'SUBSURF')
m.levels = m.render_levels = SUB
m.use_limit_surface = False
T.apply_mods(body)
log(f"shell {len(body.data.vertices)}v")

S.nose_shape(body)
log("nose bulge + V swage")

# arches cut while the shell is still a closed solid -> real wheel tubs
cut(body, S.arch_cutters(), "wheel arches")

# ---------------------------------------------------------------- 2 thickness
sol = body.modifiers.new("sol", 'SOLIDIFY')
sol.thickness = 0.0028
sol.offset = -1.0
sol.use_even_offset = False
sol.use_rim = True
T.apply_mods(body)
log(f"solidified {len(body.data.vertices)}v")

# ------------------------------------------------------------- 3 apertures
cut(body, S.windscreen_cutters(), "windscreen")
cut(body, S.side_cutters(), "side glazing + serving bays")
cut(body, [S.rear_cutter()], "rear window")
cut(body, S.door_gaps() + S.cargo_door_gaps() + S.engine_lid_gap(), "gaps",
    kind="gap")

body.name = "T1_body"
body.data.shade_smooth()
A(body, "paint")

bb = [Vector(c) for c in body.bound_box]
log("BBOX L=%.3f W=%.3f Hmax=%.3f" %
    (max(v.x for v in bb) - min(v.x for v in bb),
     max(v.y for v in bb) - min(v.y for v in bb),
     max(v.z for v in bb)))

# ------------------------------------------------------------------ 4 glass
A(S.windscreen_glass(), "glass")
A(S.windscreen_seals(), "rubber")
A(S.side_glass(), "glass")
# SPEC r4: "100% Calidad" is a decal on SOLID sheet metal aft of bay 3,
# not a frosted pane. Placed with the decals in step 8.
A(S.rear_glass(), "glass")
A(S.bay_seals(), "rubber")
log("glazing + seals")

# ----------------------------------------------------------------- 5 ragtop
canvas, frame = S.ragtop()
A(canvas, "canvas")
A(frame, "chrome_d")

# --------------------------------------------- 6 counter, galley, interior
A(D.plank_counter(S.SHOW_SIDE), "countercream")
A(D.galley(), "steel")
A(D.interior(), "dark")
log("conversion fit-out")

# ------------------------------------------------------------- 7 brightwork
for (x, tr) in ((T.X_AXLE_F, T.TRACK_F), (T.X_AXLE_R, T.TRACK_R)):
    for s in (1, -1):
        t = D.tyre(f"tyre{x:.1f}{s}");     A(t, "tyre")          # blackwall
        br, dc = D.rim(f"rim{x:.1f}{s}");  A([br, dc], "wheelcream")
        hc = D.hubcap(f"cap{x:.1f}{s}");   A(hc, "capred")
        emb = D.cap_emblem(0.0, 1);        A(emb, "capwhite")
        for o in [t, br, dc, hc] + emb:
            if s < 0:
                for v in o.data.vertices:
                    v.co.y = -v.co.y
                T.fix_normals(o)
            D.place(o, loc=(x, s * tr / 2, T.TIRE_R + T.RIDE_DROP))

# SPEC r4 8.2: bumpers are PAINTED CREAM, not chrome
A(D.bumper(True, name="bumper_f"), "bumpercream")
# SPEC rev6 sec.2.4: the rear bumper was REMOVED after the conversion. It is
# absent from both in-service photographs. Do not re-add it.
# A(D.bumper(False, name="bumper_r"), "bumpercream")
A(D.bumper_irons(True), "bumpercream")
A(D.gutter(), "paint")
A(D.mirrors(), "chrome")
A(D.wipers(), "chrome_d")
A(D.handles(), "chrome")

for s in (1, -1):
    ring, lens, bowl = D.headlamp()
    for o, k in ((ring, "chrome"), (lens, "lens"), (bowl, "reflector")):
        D.place(o, loc=(2.1015, s * 0.5450, 1.0300)); A(o, k)
    ibase, ilens = D.bullet_indicator(f"ind{s}")
    D.place(ibase, loc=(2.0960, s * 0.5250, 1.1980)); A(ibase, "chrome")
    D.place(ilens, loc=(2.0960, s * 0.5250, 1.1980)); A(ilens, "amber")
    tl = D.small_lamp(0.0455, 0.0270, f"tail{s}")
    for v in tl.data.vertices:
        v.co.x = -v.co.x
    T.fix_normals(tl)
    D.place(tl, loc=(-2.1040, s * 0.6200, 0.8250)); A(tl, "ruby")

# SPEC r4 8.3: roundel ring + strokes are painted RED on the cream nose
# MEASURED: ring outer diameter 0.370 (was 0.336), centre 1.130 above ground.
# Geometry is authored UN-DROPPED, so the centre goes in at 1.130 + RIDE_DROP.
ROUNDEL_D = 0.3700
ROUNDEL_Z_AG = 1.1300
ROUNDEL_Z = ROUNDEL_Z_AG + T.RIDE_DROP        # 1.1950 un-dropped
vr, vd = D.roundel(R=ROUNDEL_D / 2)
for o, k in ((vr, "roundelred"), (vd, "cream")):
    D.place(o, loc=(2.1155, 0.0, ROUNDEL_Z)); A(o, k)
for b in D.vw_logo(x=2.1210):                 # V over W, never inverted
    D.place(b, loc=(0.0, 0.0, ROUNDEL_Z)); A(b, "roundelred")

# SPEC sec.4 detail inventory: rear-quarter louvres (10 per side), fuel filler
# flap, aperture bobble fringe, drip-rail bulb string, pillar menu cards,
# "1963" plate surround, roof peak vent, engine-lid T-handle.  All swept or
# stamped ON TOP of the finished shell -- step 7 is after solidify and after
# every cut, so no boolean and no ordering constraint is involved.
for _obs, _key in D.spec4_details(body):
    if _key:
        A(_obs, _key)
# A() force-smooths everything it touches, which rounds off every pressed
# edge. Undo it on the hard-surface details, once, after the last A().
D.shade_fix()
log("brightwork + lamps")

# --------------------------------------------------------------- 8 decals
# MEASURED in ref_side.jpg: the lockup occupies X +0.784 ... -0.494.  The
# shipped -0.300 ... -1.900 put it ~1.25 m too far aft (centre -1.100 against
# a measured +0.145) and landed it on the louvre block.  x0 is the FORWARD
# edge -- conform_panel runs u from x0 to x1 and the show side is +Y, where
# aft is screen-right, so swapping them mirrors the script.
# The shipped senor.png was 4096 x 890 (4.602:1) with an alpha bbox of only
# 1838 x 716: the ink filled 44.9 % of the panel width and 80.4 % of its
# height, so a panel sized to the measured lockup rendered a script 0.574 m
# wide at 0.816-1.039 AG against a photographed 1.278 m at 0.380-0.853 AG --
# less than half size and 0.4 m too high.  Fixed at the TEXTURE (sign_gen.py
# now crops tight to its own ink and emits at exactly 2.702:1), so the panel
# extent and the ink extent are now the same rectangle:
#     X  +0.784 ... -0.494   width  1.278
#     Z   0.445 ...  0.918   height 0.473   un-dropped (0.380-0.853 AG)
#     AR  1.278 / 0.473 = 2.7019, matching senor.png's 2702 x 1000
# conform_panel_true rides the MEASURED body surface, not T.flank_y(): at
# z = 0.445 the analytic half width is 4.5 mm inboard of the real skin, which
# would bury the foot of the lockup.
SCR = dict(x0=0.784, x1=-0.494, z0=0.4450, z1=0.9180)    # 2.702:1 = tex AR
A(D.conform_panel_true(body, SCR["x0"], SCR["x1"], SCR["z0"], SCR["z1"],
                       S.SHOW_SIDE, name="script_L"), "script")
A(D.conform_panel_true(body, SCR["x0"], SCR["x1"], SCR["z0"], SCR["z1"],
                       -S.SHOW_SIDE, name="script_R"), "script")
# "100% Calidad" on the solid rear-corner panel, show side (SPEC r4 sec.3)
CAL = dict(x0=-1.350, x1=-1.847, z0=1.4400, z1=1.7800)   # 1.463:1 = tex AR
A(T.conform_panel(CAL["x0"], CAL["x1"], CAL["z0"], CAL["z1"], S.SHOW_SIDE,
                  name="calidad_L"), "calidad")
log("signwriting")

# ------------------------------------------------------------ 9 materials
M = MT.build_all()
for ob, key in ASSIGN:
    if isinstance(key, tuple):
        ob.data.materials.clear()
        for k in key:
            ob.data.materials.append(M[k])
    else:
        MT.assign(ob, M[key])
# ------------------------------------------------ 8b lower the whole bus
for ob in bpy.data.objects:
    if ob.type == 'MESH':
        for v in ob.data.vertices:
            v.co.z -= T.RIDE_DROP
        ob.data.update()
RIDE_DROP_APPLIED = True          # verify.py reads this to pick its frame
log(f"lowered {T.RIDE_DROP*1000:.0f} mm")

log(f"materials: {len(ASSIGN)} objects")
if FAILED_CUTS:
    log("!! cuts that failed and were rolled back: " + ", ".join(FAILED_CUTS))

if os.environ.get("T1_SAVE"):
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["T1_SAVE"])
    log("saved " + os.environ["T1_SAVE"])

if os.environ.get("T1_VERIFY"):
    import verify; importlib.reload(verify)
    verify.run(body, log)

if os.environ.get("T1_PREVIEW"):
    import studio as ST; importlib.reload(ST)
    ST.cyclorama()
    if os.environ.get("T1_CLAY"):
        ST.clay_all()
    ST.lighting(float(os.environ.get("T1_KEY", "1.0")))
    ST.camera()
    ST.render_set(os.environ["T1_PREVIEW"].split(","),
                  os.environ.get("T1_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")),
                  prefix=os.environ.get("T1_PFX", "c"),
                  res=(int(os.environ.get("T1_RX", "900")),
                       int(os.environ.get("T1_RY", "600"))),
                  samples=int(os.environ.get("T1_SAMP", "24")), log=log)
