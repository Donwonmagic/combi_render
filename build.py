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


def cut(target, cutters, tag):
    """one cutter at a time, with a sanity guard -- a failed EXACT boolean
    silently shreds the mesh, which is how the pickup-era build lost its roof"""
    for c in cutters:
        keep = target.data.copy()
        before = len(target.data.vertices)
        T.boolean(target, c)
        T.apply_mods(target)
        after = len(target.data.vertices)
        if after < before * 0.6:
            log(f"  !! BOOLEAN COLLAPSE on {c.name}: {before} -> {after}v"
                "  -- ROLLED BACK")
            old = target.data
            target.data = keep
            bpy.data.meshes.remove(old)
            FAILED_CUTS.append(c.name)
        else:
            bpy.data.meshes.remove(keep)
        bpy.data.objects.remove(c, do_unlink=True)
    log(f"cut {tag}: {len(target.data.vertices)}v")


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
cut(body, S.door_gaps() + S.cargo_door_gaps() + S.engine_lid_gap(), "gaps")

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
A(D.bumper(False, name="bumper_r"), "bumpercream")
A(D.bumper_irons(True) + D.bumper_irons(False), "bumpercream")
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
vr, vd = D.roundel()
for o, k in ((vr, "roundelred"), (vd, "cream")):
    D.place(o, loc=(2.1155, 0.0, 1.1620)); A(o, k)
for b in D.vw_logo(x=2.1210):                 # V over W, never inverted
    D.place(b, loc=(0.0, 0.0, 1.1620)); A(b, "roundelred")
log("brightwork + lamps")

# --------------------------------------------------------------- 8 decals
SCR = dict(x0=-0.300, x1=-1.900, z0=0.8250, z1=1.1725)   # 4.60:1, matches tex
A(T.conform_panel(SCR["x0"], SCR["x1"], SCR["z0"], SCR["z1"], S.SHOW_SIDE,
                  name="script_L"), "script")
A(T.conform_panel(SCR["x0"], SCR["x1"], SCR["z0"], SCR["z1"], -S.SHOW_SIDE,
                  name="script_R"), "script")
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
                  os.environ.get("T1_OUT", "/home/claude/tacombi/out"),
                  prefix=os.environ.get("T1_PFX", "c"),
                  res=(int(os.environ.get("T1_RX", "900")),
                       int(os.environ.get("T1_RY", "600"))),
                  samples=int(os.environ.get("T1_SAMP", "24")), log=log)
