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


# rev 14, AUDIT_rev12 item 3 (all glass reads as a mirror): `A()` called
# `shade_smooth()` UNCONDITIONALLY on every mesh routed through it, including
# the glazing. Every pane is a 6 mm SOLID slab (`thick=0.006`), so smooth
# shading averages the flat face normal with the 90 deg normals of the rim
# faces all the way round the perimeter -- bending the mirror inward at every
# edge. Flat glass is flat: its normal is constant by definition.
#
# MEASURED by the audit: forcing flat shading changes 88.7 % of pane pixels at
# mean |delta| 39.18, against a render-to-render null of 4.19 -- 9.4x the
# noise floor. It is not the whole defect (81 % of the pane's brightness is
# the rig: deleting the rig drops pane mean 34.05 -> 6.54, and `gal_ceiling`'s
# visible_glossy was REFUTED as the cause at 1.87 against a 4.19 null), but it
# is the half that is unambiguously wrong and costs nothing.
#
# Named by prefix, not by material, because `A()` runs before materials are
# assigned. Covers glass_ws, glass_dm/dv +-1, glass_bay{0,1,2}_{L,R},
# glass_rear -- 10 objects at the time of writing.
_FLAT_SHADED = ("glass_",)


def A(objs, key):
    if not isinstance(objs, (list, tuple)):
        objs = [objs]
    for o in objs:
        if o.type == 'MESH':
            if o.name.startswith(_FLAT_SHADED):
                o.data.shade_flat()
            else:
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


# --- headlamp hard points, hoisted to step 0 at rev 45 -----------------------
# These were declared in step 7.  Step 3 now cuts the headlamp bowls (finding
# 41) and a cutter cannot read a constant that is defined 300 lines later, so
# they are hoisted VERBATIM rather than duplicated.  The rev-44 derivation of
# HL_DROP is unchanged and lives with the lamp assembly in step 7.
HL_DROP = 0.0970                 # 97.0 +- 25.0 mm, SPEC 10.24 item 3, belt arm
HL_X    = 2.1015
HL_Y    = 0.5450
HL_Z    = 1.0300 - HL_DROP       # == 0.9330 authored.  WAS 1.0300.

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
# rev 48 -- THE LOUVRES BECOME APERTURES.  t1_detail.louvres() has swept 20
# pressed blades since rev 16, but onto an UNBROKEN flank: closed ribs, where a
# T1 louvre is an opening.  One hole per side spans the block and the blades
# span the hole, so the gaps between them are now real slots that self-shadow.
# See t1_detail.louvre_cutters.__doc__ for why it is one hole and not twenty.
cut(body, D.louvre_cutters(), "rear-quarter louvre apertures")
# ... and the dark bay behind them.  Without it the new slots look straight
# into the lit cabin -- rendered, looked at, and the frame came back with
# BRIGHT WHITE BARS among the slots.  See louvre_backing.__doc__.
A(D.louvre_backing(), "dark")
cut(body, S.door_gaps() + S.cargo_door_gaps() + S.engine_lid_gap(), "gaps",
    kind="gap")

# rev 12: THE ROOF HOLE.  Up to rev 11 no roof cutter was ever issued, so the
# lids floated over an unbroken roof skin and the galley was a sealed 2.8 mm
# steel box -- which is why the black serving bays survived six revisions of
# light tuning: the light had nowhere to enter.  ONE opening (SPEC sec.10.28,
# settled with the owner), cut here in step 3 like every other aperture, i.e.
# AFTER solidify.  It changes the roof's manifold state, so verify.py's
# non-manifold count and the shut-line probes must both be re-read at BOTH
# subdivision levels.
cut(body, S.roof_cutters(), "roof hole")

# rev 45 SPIKE, finding 41 / SPEC 10.115 -- the headlamp bowls.  HL_X/Y/Z are
# defined in step 7 (brightwork) which runs AFTER this, so the three constants
# are forward-declared there and read here; they are NOT re-typed.  Cutting in
# step 3 is required: this is an aperture like every other one and must be cut
# while the shell is still a plain solidified skin.
# T1_HL_BOWL=0 skips the cut, so the A/B is one flag and the ablation is
# declared rather than reconstructed by editing the source (SPEC 10.105's rule
# for a presentation device, applied to a geometry spike).
if os.environ.get("T1_HL_BOWL", "1") != "0":
    cut(body, S.headlamp_recess_cutters(HL_X, HL_Y, HL_Z), "headlamp bowls")

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

# -------------------------------------------------------------- 5 roof lids
# rev 8: was S.ragtop() -- a folding CANVAS ragtop with bow sticks and a
# sailcloth sag term, a reading SPEC sec.0.2 retired in rev 4. See t1_shell.
# The roof is cut into rigid hinged steel lids, modelled OPEN.
lid_skins, lid_rails, lid_struts, lid_boards = S.roof_lids()
A(lid_skins, "paint")
A(lid_rails, "paint")
A(lid_struts, "chrome_d")
A(lid_boards[0], "lidmural")           # flower mural + yellow menu strips

# rev 12: the cream panel lettered in red brush script with the red star is a
# SEPARATE SIGNBOARD, not a second cut roof lid -- the owner's reading, SPEC
# sec.10.28.  It therefore gets no opening under it, and roof_cutters() issues
# exactly one cutter.  Its fore-aft STATION is unsettled and deliberately left
# where rev 8 put it; see t1_shell.signboard().
sign_skins, sign_boards, sign_struts = S.signboard()
A(sign_skins, "paint")
A(sign_struts, "chrome_d")
if sign_boards:
    A(sign_boards[0], "lidsign")       # "LA SANTA..." red brush script + star

# --------------------------------------------- 6 counter, galley, interior
A(D.plank_counter(S.SHOW_SIDE), "countercream")
A(D.galley(), "steel")
A(D.interior(), "dark")
# rev 44, SPEC 10.104 -- THE CAB.  Returned as (object, material key) pairs:
# a cab assigned one "dark" key is a cab that reads as a void, and the
# fascia is body-coloured, the instrument chrome and glass, the welts cream.
for _o, _k in D.cab_fitout():
    A(_o, _k)
# rev 38, SPEC 10.96: close each wheel arch from inside.  Without these the arch
# is a cylinder cut clean through the skin with NOTHING behind it, and the cab
# floor is in plain sight from outside -- which is what his report 6, "there
# seems to be a bar obstructing the front wheel?", was looking at.
A(D.wheel_houses(), "dark")
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
            # rev 8: step 8b SKIPS wheel parts, so this is the FINAL height.
            # The wheel is a circle resting on flat ground: centre at exactly
            # TIRE_R, contact patch on z = 0, no tilt. It does not rake.
            D.place(o, loc=(x, s * tr / 2, T.TIRE_R))

# SPEC r4 8.2: bumpers are PAINTED CREAM, not chrome
A(D.bumper(True, name="bumper_f"), "bumpercream")
# SPEC rev6 sec.2.4: the rear bumper was REMOVED after the conversion. It is
# absent from both in-service photographs. Do not re-add it.
# A(D.bumper(False, name="bumper_r"), "bumpercream")
A(D.bumper_irons(True), "bumpercream")
# rev 44, SPEC 10.104 -- the cab door hangs on two external butt hinges and
# the scene had ZERO hinges in it.
A(D.door_hinges(), "chrome_d")
# SPEC 10.83, rev 30: the front over-rider bar.  WORKSHOP-STAGE -- it appears
# in ref_workshop.jpg, which is the CONVERSION stage, and SPEC 10.75's scope
# ruling (the owner's) is MODEL IT, TAGGED.  The rear bumper was removed
# between that stage and service, so front hardware present in the workshop is
# not automatically present in service; if an in-service frame ever shows the
# nose and contradicts this, delete this one line.
# WITHDRAWN BY THE OWNER, rev 37 -- SPEC 10.93.  He asked for the front to go
# back to "the original bumper": a plain cream blade plus its two irons, with no
# over-rider assembly at all.  THIS IS CONSISTENT WITH SPEC 2.4's OWN PRECEDENT
# a few lines above, not contrary to it -- `ref_workshop.jpg` is the CONVERSION
# stage, 10.75 already records that the REAR bumper was removed between that
# stage and service, and NO IN-SERVICE FRAME SHOWS THE NOSE.  Workshop-stage
# hardware is not automatically in-service hardware, which is precisely what the
# WORKSHOP-STAGE tag existed to allow.
# COMMENTED, NOT DELETED; overrider_bar() stays defined.  Re-enabling is this one
# line, and verify.py's 10.83 / 10.90 / 10.91 guards are ALL KEPT ARMED for the
# built case -- proven by two arms in rev 37, one re-enabling the bar (both rows
# came back alive) and one re-enabling it with a broken hoop end (10.90 failed at
# 12.36 mm).  So re-enabling restores full coverage with no edit to verify.py.
# A(D.overrider_bar(), "bumpercream")
# SPEC 10.91, rev 37: the two over-rider POSTS -- BUILT, THEN WITHDRAWN BY THE
# OWNER IN THE SAME REVISION.  SPEC 10.91.8 has his decision.  He asked for them
# ("build the post -- the half of 'model them' still unbuilt"), the build and its
# guard were completed and falsified in seven arms, and he then said: "I want to
# change my decision back... I want to stick to the original bumper."
#
# THE LINE IS COMMENTED, NOT DELETED, and `overrider_posts()` stays defined --
# the same treatment SPEC 2.4 gives the rear bumper eight lines above.  The
# measurement work, the guard and the four detector defects it caught are all
# still of value and are recorded in SPEC 10.91; only the GEOMETRY is withdrawn.
# Re-enabling is this one line.  DO NOT re-add it without his say-so.
# A(D.overrider_posts(), "bumpercream")
A(D.gutter(), "paint")
A(D.mirrors(), "chrome")
# *** rev 50 -- THE WIPERS ARE WITHDRAWN BY THE OWNER, ARMS, BLADES AND
# SPINDLES.  Asked with the evidence and the alternatives; he ruled "Remove all
# of it including the spindles." ***
#
# WHY IT WAS PUT TO HIM.  `wipers()` built two 300 mm blades plus arms standing
# 24 mm proud of the glass in light chrome -- among the most conspicuous objects
# on the face in every front and front-3/4 frame -- and its ONLY warrant was
# SPEC sec.4's inventory line, which sits under the heading "Stock 1963 T1".
# That is what the model left the factory with, INFERRED, not measured on this
# bus.  Three in-service photographs of this vehicle show the near pane legible
# from top rail to sill with no arm and no blade: ref_playa_34.png (TARGET
# artwork), ref_nolita_front34.jpg and ref_nolita_front34b.jpg.  At those
# frames' 140-215 px/m a 300 mm arm is 42-65 px and a 13 mm blade is 1.8-2.8 px,
# both well above the resolving floor -- the bobble-fringe balls in the same
# frames are ~2 px and are unambiguous.  Same evidence class as the over-rider
# bar he withdrew at rev 37 (three lines above) and the rear bumper SPEC 2.4
# removed.
#
# THE SPINDLES GO TOO, AND THAT IS HIS CALL, NOT AN INFERENCE.  The survey
# proposed keeping `wiper_pivot`/`wiper_boss` and deleting only the arm and
# blade.  He overruled it: the two dark cowl stubs are ~3 px objects that could
# equally be washer jets, so nothing is kept on that evidence.
#
# COMMENTED, NOT DELETED, exactly as the over-rider is, so the geometry and its
# VISIBILITY_WATCH registration survive if he ever reverses this.  Re-enabling
# is this one line.  DO NOT re-add it without his say-so.
# A(D.wipers(), "chrome_d")
A(D.handles(), "chrome")

# ===================================================================== rev 44
# SPEC 10.24 ITEM 3 -- APPLIED, after thirty-four revisions OPEN.
#
# The owner filed it himself: "the paint job and the headlights are not
# alligned".  It has been OPEN since rev 10 with one stated blocker -- "it is a
# single-chain claim that moves the face of the vehicle, and it deserves a
# SECOND DERIVATION first".
#
# THE BLOCKER WAS DISCHARGED AT REV 37 AND SEC.10.24 NEVER LEARNED OF IT
# (SPEC:6999, the same carrier failure sec.10.91.1 names).  Rev 44 re-checked
# both arms of that discharge before acting, and they are NOT equally sound:
#
#   ARM A -- ORDINAL, SCALE-FREE, and it is what settles that the defect is
#   REAL.  Three independent routes, none needing a px/m conversion:
#     * rev 11: in the photograph the INDICATOR aperture lies BELOW the
#       two-tone break; in the build it lies ABOVE it.
#     * rev 44 (probe_rev44_report3): in the build the break CUTS A 131.9 mm
#       CHORD ACROSS THE HEADLAMP APERTURE; in ref_source.jpeg the lamp sits
#       entirely in the red with 12 px of clear red above it.
#     * the owner's own report, which is the same statement in his words.
#
#   ARM B -- the roundel-ratio MAGNITUDE, "83 +- 19 mm at 4.4 sigma" from a
#   roundel-to-lamp separation of 0.628 +- 0.066 roundel diameters.  REV 44
#   COULD NOT REPRODUCE IT: the same arithmetic on today's constants returns
#   103.4 mm, not 83.  The 20.4 mm gap is a STALE COUPLING in the roundel's own
#   placement, not in this finding -- see the note above ROUNDEL_Z_AG below.
#   ARM B IS THEREFORE SET ASIDE AS CONTAMINATED and is NOT used here.
#
# SO THE MAGNITUDE COMES FROM THE BELT-RELATIVE ARM ALONE, which touches no
# stale constant: headlamp centre photographed at belt - 0.339 +- 0.025 m
# against the build's belt - 0.242, i.e. 97.0 mm too high at ~3.9 sigma.  The
# belt is independently anchored -- photographed window-sill-to-body-break
# 102.7 +- 6.6 mm against a built 100.0 (SPEC 10.98), -2.7 mm.
# rev 45: HL_DROP/X/Y/Z are DECLARED IN STEP 0 (search "HL_DROP =") because
# step 3 cuts the headlamp bowls and needs them.  They are read here, not
# re-typed -- re-typing them is exactly SPEC 10.25's defect class.
# THE INDICATOR IS MEASURED RELATIVE TO THE LAMP AND MUST MOVE WITH IT.
# Its Z was written as the LITERAL 1.2360 while the comment below claimed "Z is
# set RELATIVE to the lamp, which is robust to the open question about the
# lamp's own absolute height".  IT WAS NOT -- 1.2360 is 1.0300 + 0.206 re-typed,
# and the lamp moving would have left the indicator behind.  Y was the same
# defect (0.6750 == 0.5450 + 0.130).  Both now expressed, which is SPEC 10.25's
# own rule: "a constant tuned against another constant must be expressed in
# terms of it, or correcting one silently breaks the other."
IND_DZ  = 0.2060                 # measured above the lamp, ref_workshop.jpg
IND_DY  = 0.1300                 # measured outboard of the lamp
IND_Y   = HL_Y + IND_DY          # == 0.6750, unchanged
IND_Z   = HL_Z + IND_DZ          # == 1.1390.  WAS the literal 1.2360.
#
# WHAT IS DELIBERATELY NOT TOUCHED: THE ROUNDEL.  SPEC:7005 names this trap
# explicitly -- "DO NOT MOVE THE ROUNDEL WITH THE LAMPS" -- because 10.24's
# three findings were applied together once and reverted together once, and the
# lesson from that revert is that they are NOT one change.  ROUNDEL_Z is
# derived from its own chain and is untouched here.  Its separate defect is
# recorded, NOT fixed in this revision.
#
# TO REVERT: set HL_DROP = 0.0.  That restores the lamp AND the indicator.

for s in (1, -1):
    ring, lens, bowl = D.headlamp()
    # rev 10 (audit materials-6): the bezel is BRASS, not chrome.  Measured in
    # ref_side.jpg the bezel reads a* +2.1 / b* +31.6 at L* 65.6, against five
    # neutral references in the same frame at b* -2.4...+1.6 (cab door handle,
    # wing mirror, counter stainless, lamppost, pavement).  It is not a warm
    # bounce: every genuinely warm surface in that frame carries a* with its
    # b* (red 49/40, wall 11/11) and the bezel's ratio is 0.07.  R-B = +68.
    #
    # ------------------------------------------------- rev 45, SPEC 10.111
    # RETIRED TO CHROME, AND THE REV-10 READING IS NOT CALLED WRONG -- IT IS
    # CALLED UNCONTROLLED.  ref_nolita_front34.jpg (recovered this revision;
    # the rev-44 brief listed it as tracked and it was NOT in the tree) shows
    # the same bezel at about four times the scale, front three-quarter,
    # resolved over ~15 px of arc, under cool indoor light:
    #
    #     bezel top arc                 b* + 2.7      a* +23.1
    #     bezel bottom arc              b* + 6.7      a* +16.1
    #     white wall, SAME frame        b* + 6.9      <- the frame's neutral
    #     red nose, 10 px outboard      b* +61.8      <- the frame's warm
    #
    # The bezel's b* is INDISTINGUISHABLE FROM THE FRAME'S OWN NEUTRAL and
    # nowhere near its warm surfaces.  ref_playa_34.png shows the same part in
    # low direct sun reading gold on its sunward arc and dark on the other --
    # which is what CHROME does and what brass does not: brass is warm from
    # every direction.
    #
    # WHY THE REV-10 CONTROL SET DOES NOT CONTROL.  Its five neutrals are a
    # door handle, a wing mirror, counter stainless, a lamppost and pavement.
    # Not one of them is a SMALL MIRROR-FINISH TORUS RINGED BY A LARGE WARM
    # PANEL, which is the confound here, and on ref_side.jpg -- a flat side
    # view -- the bezel is seen at grazing incidence and is a few pixels wide.
    # A chrome ring surrounded by cream and red bodywork reading b* +31.6 in
    # that frame is exactly what the bounce predicts.  The 1963 T1's headlamp
    # rim is a chrome-plated pressing; two frames and the part agree.
    #
    # THE RETIRED ARM STILL RENDERS: T1_HL_BEZEL=brass restores it.  This is
    # the same pattern as SPEC 10.82's T1_W_DUP.
    _BEZEL = os.environ.get("T1_HL_BEZEL", "chrome")
    for o, k in ((ring, _BEZEL), (lens, "lens"), (bowl, "reflector")):
        D.place(o, loc=(HL_X, s * HL_Y, HL_Z)); A(o, k)
    # rev 10 (audit inventory-9, re-derived).  The finding said "20 mm
    # inboard"; it understated by 7x.  Measured off ref_workshop.jpg the
    # indicator sits 0.130 +/- 0.035 m OUTBOARD of the headlamp centre and
    # 0.206 +/- 0.010 m above it.  Y goes 0.5250 -> 0.6750 (= 0.5450 + 0.130)
    # and Z is set RELATIVE to the lamp, which is robust to the open question
    # about the lamp's own absolute height (SPEC 10.22).
    #
    # The finding also proposed replacing the bullet with a flat oval standing
    # 15 mm proud.  That is REFUTED: ref_side shows the lens standing ~65 mm
    # proud and ~69 mm tall, depth/height 0.94.  The bullet is the right type;
    # it was only too shallow (41.5 mm proud of its plinth).  Deepened in
    # t1_detail.bullet_indicator, height untouched.
    ibase, ilens = D.bullet_indicator(f"ind{s}")
    D.place(ibase, loc=(2.0960, s * IND_Y, IND_Z)); A(ibase, "chrome")
    D.place(ilens, loc=(2.0960, s * IND_Y, IND_Z)); A(ilens, "amber")
    # rev 15 -- TAIL LAMP DIAMETER.  It is ROUND (locked) and it was half size.
    # ref_rear34.jpg, probe box (918,636,975,730).  50 %-crossings of the
    # paint/lens step down each column; columns x 925-941 are thrown out
    # because the yellow flower above the lamp is a separate dark blob there.
    # Over the clean columns x 943-961 the vertical extent peaks at 69.06 px
    # (top 6 columns mean 68.57, sd 0.35).  The vertical is the unforeshortened
    # axis for a round lamp on a panel turned about a vertical axis, and the
    # plate frame beside it is the only VERTICAL ruler at the tail:
    #
    #   lamp vertical D / plate outer H = 1.1627 +/- 0.0271     photograph
    #                                     0.4619                built (rev 14)
    #   -> lamp OD 0.1956 m against 0.1030 built = 1.90x too small
    #
    # 1.90x is the low end of the work list's 1.9-2.2x, and it only reads that
    # way once the plate itself is corrected (t1_detail.plate_1963); against
    # the rev-14 plate the same pixels give 2.52x.  Tied to PLATE_OUTER_H on
    # purpose -- that IS the ruler the ratio was measured against.
    #
    # DEPTH NOT CHANGED, deliberately.  Nothing in any frame we hold resolves
    # how proud the lens stands, and scaling 0.0270 with the radius would push
    # the lamp's tip to x -2.159, past the T-handle, making it the rear-most
    # object on the vehicle and adding ~24 mm to verify.py row 1's overall
    # length -- through a guard, on an unmeasured number.
    TAIL_LAMP_OD = 1.1627 * D.PLATE_OUTER_H
    tl = D.small_lamp(TAIL_LAMP_OD / 2 - 0.006, 0.0270, f"tail{s}")
    for v in tl.data.vertices:
        v.co.x = -v.co.x
    T.fix_normals(tl)
    # rev 13, tail dimension: the lens is AMBER, not ruby.  Measured in
    # ref_rear34.jpg against the paint it is mounted on -- lens hue 21.4 deg,
    # G/R 0.456; adjacent tail red hue 12.2 deg, G/R 0.275.  The lens is
    # YELLOWER and LESS red-dominant than the body it sits on, and `ruby` is
    # redder than that body.  Same-frame, same-light, same class (both are
    # coloured transmissive/painted surfaces under one source), so the
    # comparison is admissible under SPEC 10.21.
    # rev 16: the lamp mounts ON the tail skin, so it moves with it.  It was
    # authored at -2.1040 = X_TAIL_OLD + 0.0040; the tail re-space carries that
    # 4.0 mm standoff forward rather than re-typing the station.  Left where it
    # was, this pair became the rear-most objects on the vehicle by 258 mm and
    # verify row 1's "length 4.291 vs spec 4.290" would have kept PASSING on a
    # phantom -- the same failure shape as the counter_top length row the
    # rev-12 audit found at audit.py:308.
    # *** rev 50, A10 -- THE 4.0 mm STANDOFF WAS BURYING THE LENS'S CENTRE. ***
    #
    # `small_lamp`'s profile STARTS ON THE AXIS -- its first point is
    # (0.000, 0.0000) -- so the lamp's mounting plane and the deepest point of
    # its dish are the SAME plane.  Inserting the lamp 4.0 mm into the skin
    # therefore does not bed a flange, it buries the middle of the lens: the
    # skin cuts the dish where its radius is
    #     0.55 * r * (0.0040 / (0.45 * 0.0270)) = 0.1811 r
    # so the innermost 18.1 % of each lamp is BEHIND the bodywork and the camera
    # sees a Ø33.2 mm disc of BODY RED at the exact centre of each lens.
    # Confirmed photometrically rather than by eye alone: the core reads
    # G/R 0.299 / B/R 0.191 against the body paint 90 px above at 0.277 / 0.174
    # and the amber lens itself at 0.584 / 0.287 -- the core IS the paint.
    # A specular would move toward the source's white and RAISE B/R; it is lower.
    #
    # THE MAXIMUM ADMISSIBLE INSERTION IS ZERO, and that is not a choice -- it
    # follows from the profile starting on the axis.  The mounting face goes ON
    # the skin.  Expressed as X_TAIL so it still rides the tail re-space, which
    # is what the rev-16 note below was protecting.
    #
    # NOT CHANGED, deliberately: the lamp's DEPTH (0.0270, unmeasured, see
    # above), its lateral station (y 0.6200, correct to 2 px in ref_rear34.jpg)
    # and its DIAMETER (1.1627 x PLATE_OUTER_H, confirmed against the rev-15
    # measurement).  This edit moves one number, 4.0 mm, in one axis.
    # ALSO NOT CHANGED, and it is a separate open item: SURVEY_rev49 finding 47
    # measures the lens centre ~46 +- 12 mm too HIGH (photograph puts it BELOW
    # the plate's centre, z 0.8250 sits 37.5 mm ABOVE PLATE_OUTER_CZ 0.787545).
    # That is a photograph measurement coupled to the engine lid's own z station
    # (finding 3), and moving one without the other would trade one internal
    # contradiction for another.  Left, measured, and reported.
    D.place(tl, loc=(T.X_TAIL, s * 0.6200, 0.8250)); A(tl, "amber")
    # GUARD, SAME EDIT AS THE CHANGE (rule 12).  Rev 49 wrote rule 30 -- "a
    # fixture's foot must be clear of the body it stands on, and something must
    # check it" -- and wrote guards for the tail board's foot and the trunk
    # bay's lining.  The tail lamps were not in scope, and they had the same
    # defect.  This reads the BUILT lamp's own rearmost-forward vertex against
    # X_TAIL, not the loc= that positioned it (rule 32).
    # WATCHED FAIL on T1_LAMPSINK=1, which restores the 4.0 mm insertion.
    if os.environ.get("T1_LAMPSINK"):
        for _v in tl.data.vertices:
            _v.co.x += 0.0040
        tl.data.update()
    _nose_most = max((tl.matrix_world @ _v.co).x for _v in tl.data.vertices)
    if _nose_most > T.X_TAIL + 1e-6:
        raise AssertionError(
            "tail lamp %s reaches x %.4f, %.1f mm FORWARD of the tail skin at "
            "%.4f -- small_lamp()'s profile starts ON THE AXIS, so any "
            "insertion buries the CENTRE of the lens and the skin renders as a "
            "disc of body red at the middle of the lamp."
            % (tl.name, _nose_most, (_nose_most - T.X_TAIL) * 1000, T.X_TAIL))

# SPEC r4 8.3: roundel ring + strokes are painted RED on the cream nose
# MEASURED: ring outer diameter 0.370 (was 0.336), centre 1.130 above ground.
# Geometry is authored UN-DROPPED, so the centre goes in at 1.130 + RIDE_DROP.
# rev 10.  This was 0.3700 and it is a live regression, applied in the wrong
# direction.  Audit finding livery-9 said "9 % undersized, centre 32 mm high";
# somebody applied it and the roundel went UP to 0.370.  Re-derived
# independently (SPEC 10.22) the outer diameter is 0.28 +/- 0.03 m and the
# centre sits 0.149 +/- 0.030 m BELOW the belt line, not above it.  The 9 %
# figure was a code-vs-SPEC bookkeeping claim whose only photographic support
# came from ref_source.jpeg -- the 246x197 thumbnail retired in SPEC 0.2.
# Method: D_roundel / D_aperture = (m_ro/2)(1/m_near + 1/m_far) = 1.384 off
# ref_workshop.jpg.  It needs no camera pose, because 1/s is affine in Y and
# the roundel sits at the headlamps' Y-midpoint.
ROUNDEL_D = 0.2800
# rev 10.  Was 1.1300 AG.  Measured belt-relative (the safe framing: a ground
# line carries ~70 mm of common-mode error, SPEC 10.11): roundel centre sits
# 0.149 +/- 0.030 m BELOW the belt, and break_z(2.1155) = 1.166 AG, so the
# centre belongs at 1.017 AG.  The build had it 113 mm high.
#
# Second defect on the same line, and a violation of a stated hard constraint:
# this used the RIDE_DROP SCALAR.  Since rev 8 the drop is a function of x.
# At x = 2.1155 rake_drop is 0.1063 against the scalar's 0.0650 -- the roundel
# was being placed with a 41 mm bookkeeping error internal to the build.
# ---------------------------------------------------------------- rev 44
# FINDING, RECORDED AND **NOT** FIXED IN THIS REVISION.  BOTH FIGURES IN THE
# COMMENT ABOVE ARE STALE, and 1.0170 was tuned against one of them:
#     "rake_drop(2.1155) is 0.1063"  -> the code computes 0.0855  (-20.8 mm)
#     "break_z(2.1155) = 1.166 AG"   -> the code computes 1.1865  (+20.5 mm)
# 0.1063 reproduces under neither the current RAKE_Z0 (0.047925) nor the one
# its comment says it replaced (0.0365); it predates the rev-13 rake.  The
# derivation that produced 1.0170 is "roundel centre sits 0.149 +- 0.030 m
# BELOW the belt, and break_z(2.1155) = 1.166 AG, so the centre belongs at
# 1.017 AG".  Run on today's break_z that gives 1.1865 - 0.149 = 1.0375.
#
# THIS IS SPEC 10.25's OWN DEFECT CLASS -- a constant tuned against another
# constant and not expressed in terms of it -- sitting nine lines above the
# block where 10.25's lesson is written down.  THAT PART STANDS.
#
# BUT THE MAGNITUDE WAS OVER-CLAIMED WHEN THIS NOTE WAS FIRST WRITTEN, AND THE
# CORRECTION IS MINE.  It said "THE ROUNDEL IS ~20.5 mm TOO LOW", which is one
# chain's POINT ESTIMATE quoted as a defect without its error bar and without
# the second chain.  Both chains, run at rev 44:
#     A  belt-relative   break_z(2.1155) - 0.149 +- 0.030  = 1.0375 +- 0.0300
#     B  roundel/lamp    lamp + 0.628 +- 0.066 diameters   = 1.0236 +- 0.0185
#     JOINT                                                = 1.0274 +- 0.0157
# Against the built 1.0170 those are 0.68, 0.36 and 0.66 sigma.  ALL THREE ARE
# INSIDE ONE SIGMA: THE ROUNDEL IS NOT SIGNIFICANTLY MIS-PLACED, and moving
# geometry on a 0.7-sigma difference is what this project calls laundering.
#
# SO IT IS NOT MOVED, AND THE REAL DEFECT -- THAT NOTHING WAS WATCHING -- IS
# FIXED INSTEAD.  probe_rev44_lampmove C5/C6 now hold 1.0170 against BOTH
# chains and fire if either drifts out of band, which is what would have caught
# the datum moving under it in the first place.  SPEC:7005 also forbids moving
# the roundel in the same change as the lamps, and that stands independently.
ROUNDEL_Z_AG = 1.0170
ROUNDEL_Z = ROUNDEL_Z_AG + T.rake_drop(2.1155)
# rev 44 -- THE MOUNTING PLANE, moved forward 13.5 mm.  See the block below the
# glyph placement for the measurement: the nose reaches x 2.1270 between
# z 0.86 and 1.01 while the emblem's front face sat at 2.1265, so the roundel's
# lower half -- the whole W -- was buried inside the bodywork.
ROUNDEL_X = 2.1290                  # was 2.1155
GLYPH_X   = ROUNDEL_X + 0.0055      # the emblem plate stands on the disc face
vr, vd = D.roundel(R=ROUNDEL_D / 2)
for o, k in ((vr, "roundelred"), (vd, "cream")):
    D.place(o, loc=(ROUNDEL_X, 0.0, ROUNDEL_Z)); A(o, k)
_EMBLEM_PLATE = [vr, vd]
_EMBLEM_FRONT = {}                     # object -> indices of its FRONT face
# rev 10.  The V and the W had merged into an X again -- the same failure
# SKEPTIC_PASS sec.D fixed in rev 8, returning by a different route.
#
# vw_logo's R and w were ABSOLUTE (0.1385 / 0.0275), tuned against the then
# locked ring diameter of 0.370, while the ring itself is driven by
# ROUNDEL_D.  Correcting ROUNDEL_D to the measured 0.280 shrank the ring by
# 24 % and left the glyph at its old size, so the bars became proportionally
# fat, the designed 12.7 mm air gap between the V's apex and the W's peak
# closed, and the two prisms touched.  Nothing about the glyph code was
# wrong; the coupling was missing.
#
# Tie them.  The rev-8 proportions are preserved exactly: glyph R was 0.7486
# of the ring's outer radius and the bar width 0.1986 of that R, which is what
# holds the arms 12.29 deg apart with clear air between them at ANY diameter.
#
# rev 15.  The coupling above is right and stays; the FRACTION was wrong.
# 0.7486 leaves the glyph floating in the middle of the ring with 11 mm of
# clear air all round; the emblem in ref_workshop.jpg has every stroke end
# running into the ring band.  Measured there (crop box (258,494,352,604)):
# glyph height / ring outer D = 0.746 +/- 0.028 against 0.5639 built, 5.1
# sigma.  D.vw_logo_fit sizes the glyph off its OWN built outline so the
# extreme corner lands on the ring's outer radius -- no fraction is written
# down at all, so there is nothing left here to go stale a third time.
# ------------------------------------------------------------------ rev 44
# THE ROUNDEL WAS MOUNTED ELEVEN MILLIMETRES INSIDE THE NOSE.
#
# The owner reported the logo off the rev-44 hero.  Rendered face-on it showed
# a V, a centre peak and two stubs; the W's four descending strokes and both
# legs were absent.  Isolated in an empty scene the SAME objects -- glyph, ring
# and disc together -- render a clean V over W, so the outline (rasterised and
# checked), the cap fill (area 0.012193 m2 against 0.01232 hand-computed), the
# material (a flat `simple`, no mask) and the renderer were all cleared.
#
# MEASURED on the built body, forward-most x within |y| < 0.06:
#     z 0.86-1.01 : nose reaches x 2.1266 .. 2.1270   <-- IN FRONT of the glyph
#     z 1.01-1.16 : nose falls back to 2.1262 .. 2.1194
# The glyph's front face sat at 2.1265.  So BELOW z = 1.01 the nose stood
# PROUD of the emblem and buried it, and above that the emblem stood proud and
# rendered.  The crossover is the exact height where the render stops drawing.
# The V lives above it; the W's arms and legs live below it.  Nothing was wrong
# with the emblem at all -- it was sunk into the bodywork.
#
# The mounting plane is moved forward 13.5 mm so the glyph's REAR face clears
# the nose's own maximum by 2 mm.  It does not become the forward-most object:
# the bullet indicator already reaches x 2.1600.
for b in D.vw_logo_fit(ROUNDEL_D / 2, x=GLYPH_X):   # V over W, never inverted
    D.place(b, loc=(0.0, 0.0, ROUNDEL_Z)); A(b, "roundelred")
    _EMBLEM_PLATE.append(b)

# The front face of each piece, identified BEFORE the drape moves anything:
# these are the vertices the camera actually sees, and they are the only ones
# that have to stand proud.  The ring's profile and the disc's back plate both
# carry material BEHIND the skin on purpose, so a guard over every vertex is
# the wrong guard -- it fired on this very change (rule 12 working), at
# -15.11 mm, on the ring's back rim.  Stated, not quietly widened.
for _o in _EMBLEM_PLATE:
    _xm = max(_v.co.x for _v in _o.data.vertices)
    _EMBLEM_FRONT[_o.name] = [_v.index for _v in _o.data.vertices
                              if _v.co.x > _xm - 1e-6]

# ------------------------------------------------------- rev 45, SPEC 10.110
# DRAPE THE BADGE ONTO THE NOSE.  Everything above builds the roundel in the
# Y-Z plane and extrudes it along +X, so ring, disc and glyph together are one
# FLAT PLATE -- and the nose is not flat.  Raycast against this very body,
# before the drape, at the badge's own centre height:
#
#     straight UP    at the ring radius   the nose is  -31.6 mm  (falls away)
#     up-left/right                                    -19.0 mm
#     sideways                                          -0.6 mm
#     straight DOWN                                     +3.0 mm  (comes forward)
#
# so the plate's upper half floated up to 32 mm proud of the sheet metal and
# its LOWER half was flush with it or 0.3 mm BEHIND it.  Rendered, the V stood
# out and THE ENTIRE W VANISHED INTO THE BODY except its two outer arm tips --
# which is why the badge reads as a CLOCK FACE at every resolution, and is what
# the owner has been reporting as "the logo is off" for three revisions.
#
# It was never found because every check ever run on this emblem was run on the
# GLYPH'S OWN OUTLINE, IN ITS OWN PLANE: SPEC 10.25's air gap, 10.107's six
# stroke ends, probe_rev44_lampmove's height.  Not one of them involved the
# body.  A detail you cannot see is not a detail (rule 10) -- and a detail
# measured in isolation from what it sits on is not measured.
#
# NOTHING IN THE GLYPH MOVES IN ITS OWN PLANE.  drape_x translates each vertex
# in X ONLY.  The spine, the stroke width, the fit radius, ROUNDEL_D and
# ROUNDEL_Z_AG are all untouched, so probe_rev44_lampmove's two chains and
# SPEC:7005's trap are unaffected by construction, not by inspection.
def _nose_x(y, z):
    hit, loc, _n, _i = body.ray_cast(Vector((3.5, y, z)), Vector((-1, 0, 0)))
    return loc.x if hit else None


# Two plates, two mounting planes, and BOTH ARE READ OFF THE CONSTANTS ABOVE
# rather than typed -- rule 2.  The ring and its backing disc are authored with
# the mounting plane at local x = 0 and placed at ROUNDEL_X; the glyph is
# authored with its BACK FACE as the mounting plane, at GLYPH_X.
#
# NOTE ON REV 44's 13.5 mm.  The block above moves ROUNDEL_X 2.1155 -> 2.1290
# because the nose stood proud of the emblem below z = 1.01.  That measurement
# is right and rev 45 reproduced it from the other direction (a radial raycast
# at eight angles and three radii, rather than a forward-most-x scan of a
# |y| < 0.06 strip).  THE DRAPE SUBSUMES THE SHIFT: dx = surf - mount +
# standoff, so the badge lands on the surface whatever ROUNDEL_X is, and a
# uniform shift can only ever be right at one height on a curved panel -- at
# 13.5 mm the badge still floated ~18 mm proud at its top.  ROUNDEL_X is kept
# because it is the record and because the drape reads it.
_n_dr = _n_miss = 0
_dx_lo, _dx_hi = 9e9, -9e9
for _plate, _mount in (([vr, vd], ROUNDEL_X),
                       ([o for o in _EMBLEM_PLATE if o not in (vr, vd)], GLYPH_X)):
    _n, _lo, _hi, _ms = T.drape_x(_plate, _nose_x, _mount, standoff=0.0016)
    _n_dr += _n; _n_miss += _ms
    _dx_lo = min(_dx_lo, _lo); _dx_hi = max(_dx_hi, _hi)
log("roundel draped onto the nose: %d verts, dx %+.1f..%+.1f mm, %d lattice misses"
    % (_n_dr, _dx_lo * 1000, _dx_hi * 1000, _n_miss))
# GUARD, ADDED IN THE SAME EDIT AS THE CHANGE (rule 12).  Every emblem vertex
# must now stand PROUD of the nose, and by a bounded amount -- a plate that is
# flush anywhere is a plate that will be swallowed by the shader bevel and the
# 2.8 mm skin, and a plate standing 30 mm off is the defect this fixes.
_pr = []
for _o in _EMBLEM_PLATE:
    for _i in _EMBLEM_FRONT[_o.name]:
        _v = _o.data.vertices[_i]
        _sx = _nose_x(_v.co.y, _v.co.z)
        if _sx is not None:
            _pr.append(_v.co.x - _sx)
assert _pr, "emblem drape guard: no front-face vertex resolved against the nose"
assert min(_pr) > 0.0005, (
    "SPEC 10.110: an emblem FRONT-FACE vertex is only %.2f mm proud of the "
    "nose (the flat plate reached -0.3 mm); the badge is being swallowed again"
    % (min(_pr) * 1000))
assert max(_pr) < 0.030, (
    "SPEC 10.110: an emblem FRONT-FACE vertex stands %.1f mm proud of the "
    "nose (the flat plate reached 32 mm); the badge is a flat plate on a "
    "curved panel again" % (max(_pr) * 1000))
log("  emblem front faces proud of nose: %.2f .. %.2f mm over %d verts"
    % (min(_pr) * 1000, max(_pr) * 1000, len(_pr)))

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
# rev 9: script rebuilt as explicit letterforms (script_gen.py); the panel
# follows the new texture AR. x extents unchanged -- SKEPTIC C3 measured
# them and they still hold. z centre unchanged, height from the AR.
# rev 11 AUDIT.  z1 was 0.9177, giving 1.278 x 0.4724 = 2.705:1, and the
# comment said "= tex AR".  That was true of the rev-9 texture (2702x1000).
# rev 10 rebuilt the script and tex/senor.png is now 4096x1738 = 2.3567:1.
# The constant was never updated, so the lockup has been squashed 15.8 %
# vertically ever since -- and the whole-lockup IoU of 0.942 could not see it,
# because compare_script.py scores the TEXTURE against the reference mask and
# never looks at the panel the texture lands on.
#
# Two independent derivations agree on the height:
#   texture aspect      1.2784 / 2.3567 = 0.5424
#   measured off photo  0.5440 +/- 0.008 m   (ink height, 211.2 px/m)
# Width is already right: photo 1.2784 +/- 0.012 against 1.278 built (-0.4 mm),
# and the x extents are independently confirmed at +3 / -1 mm.
#
# GROWN UPWARD, not recentred.  z0 = 0.4453 is measured and carries the warning
# above it (the analytic half width is 4.5 mm inboard of the real skin there).
# And the missing height belongs at the TOP: SPEC 10.20 found the reference ink
# runs 16 rows higher than the frame allowed, and those rows are the top of
# 'Senor'.  A panel too short at the top is exactly what clips them.
SCR = dict(x0=0.784, x1=-0.494, z0=0.4453, z1=0.9896)    # 2.357:1 = tex AR
A(D.conform_panel_true(body, SCR["x0"], SCR["x1"], SCR["z0"], SCR["z1"],
                       S.SHOW_SIDE, name="script_L"), "script")
A(D.conform_panel_true(body, SCR["x0"], SCR["x1"], SCR["z0"], SCR["z1"],
                       -S.SHOW_SIDE, name="script_R"), "script")
# "100% Calidad" on the solid rear-corner panel, show side (SPEC r4 sec.3)
# rev 9: moved 198 mm forward and enlarged. Checked by a datum that needs no
# pixel-to-metre mapping -- the decal's FRACTION of the solid rear-corner
# panel. In ref_side.jpg the panel runs x 698 (aft edge of bay 3) to x 902
# (tail) and the decal occupies 18.6%-67.2% of it; the old placement sat at
# 37.3%-84.7%. Width 0.513 and height 0.380 both come from the local scale
# there, 194.8 px/m, NOT the 211.5 px/m that holds at mid-body -- the flank is
# foreshortened toward the tail. Vertical CENTRE is unchanged on purpose: see
# SPEC 10.11, the ground-line datum carries a ~70 mm common-mode error.
CAL = dict(x0=-1.155, x1=-1.668, z0=1.4200, z1=1.8000)   # 1.350:1 = tex AR
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
# ------------------------------------------- 8b lower the whole bus, WITH RAKE
# rev 8: this was a scalar `v.co.z -= T.RIDE_DROP`, which left the vehicle 89 mm
# short overall and reading flat and stretched. The real stance is nose-down
# ~1.9 deg, so the drop is a shear in x. See t1_core.rake_drop().
#
# Safe to read v.co.x as WORLD x: verified that all 147 meshes carry an identity
# transform at this point (D.place() bakes into mesh data), so local == world.
# If that ever stops being true this loop silently shears by the wrong station,
# so it is asserted rather than assumed.
_bad = [ob.name for ob in bpy.data.objects
        if ob.type == 'MESH' and (
            max(abs(c) for c in ob.location) > 1e-9
            or max(abs(c) for c in ob.rotation_euler) > 1e-9
            or max(abs(ob.scale[i] - 1.0) for i in range(3)) > 1e-9)]
assert not _bad, ("step 8b shears on v.co.x, which is only world x while every "
                  "mesh has an identity transform. These do not: " + ", ".join(_bad[:8]))

# The WHEELS do not rake. They are circles resting on flat ground: contact patch
# at z = 0, centre at exactly TIRE_R, no tilt. Shearing them would swing the
# hubcap VW glyph 1.9 deg off vertical. They are placed in step 7 at
# TIRE_R + rake_drop(x_axle) so that skipping the shear lands them at TIRE_R.
_WHEEL_PREFIX = ("tyre", "rim", "cap", "capvw")


def _is_wheel(name):
    n = name.split('.')[0]
    return any(n.startswith(p) for p in _WHEEL_PREFIX)


_n_shear = _n_wheel = 0
for ob in bpy.data.objects:
    if ob.type != 'MESH':
        continue
    if _is_wheel(ob.name):
        _n_wheel += 1
        continue
    for v in ob.data.vertices:
        v.co.z -= (T.RAKE_Z0 + T.RAKE_DZDX * v.co.x)
    ob.data.update()
    _n_shear += 1
RIDE_DROP_APPLIED = True          # verify.py reads this to pick its frame
log(f"lowered {T.RAKE_Z0*1000:.1f} mm at x=0, rake {T.RAKE_DZDX*1000:.1f} mm/m "
    f"nose-down ({math.degrees(math.atan(T.RAKE_DZDX)):.2f} deg); "
    f"{_n_shear} sheared, {_n_wheel} wheel parts held level")

# ------------------------------------------------- 8c THE TRUNK LID, OPENED
# rev 48, JOB 1.  "we're going to need the trunk open like it's in service."
#
# AFTER the shear, deliberately.  See t1_shell.split_trunk_lid.__doc__ and the
# block above it: a tail lid hinges about a LATERAL axis, so the swing moves
# v.co.x, and step 8b shears on v.co.x.  Swinging first would shear the open
# lid at the wrong station and tilt it by the rake angle for nothing.  A ROOF
# lid can be swung first only because _hinge() leaves x untouched.
#
# The T-handle and the 1963 plate are mounted ON the lid panel, so they travel
# with it through the identical transform -- not a copy of the angle, the same
# call with the same hinge, so the two can never drift apart (rule 2).
_lid_trunk, _thx, _thz, _tdeg = S.split_trunk_lid(body, log=log)
# rev 49, THE OWNER'S RULING: "leave the lower bay shut, just have the back
# trunk window open for service."  With the lid SHUT the T-handle and the 1963
# plate must NOT be carried and must NOT join SWUNG -- they have not moved, so
# registering them would exclude two parts that ARE inside the closed envelope
# from the vehicle's own length and height, which is rule 18 exactly: a control
# that is right for the wrong reason.  Rev 48's stale-bound_box defect was the
# mirror image of this one.
if _lid_trunk is not None and abs(_tdeg) > 1e-6:
    for _nm in ("englid_handle", "plate_1963"):
        _o = bpy.data.objects.get(_nm)
        if _o is None:
            log("!! trunk lid: %s absent, nothing to carry" % _nm)
            continue
        S._hinge_y(_o, _thx, _thz, _tdeg)
        S.SWUNG.add(_nm)          # it now lives outside the closed envelope
        log("  carried %s through the lid's own swing" % _nm)
    # WHAT IS BEHIND IT IS NOT DECIDED HERE.  The aperture now shows the
    # shell's own inner skin -- the body is solidified with use_rim=True, so
    # the slot has a 2.8 mm returned edge and the cavity is closed.  Whether
    # that reads correctly is a LOOK-AT-IT question and is answered from the
    # render, not from here.  Nothing is invented to fill the bay:
    # PHOTOS_WANTED_rev44 records that "the engine was scrapped and the
    # transmission sold", so its contents are unknown.

# rev 48, JOB 1b -- "the main bay that should be open is the upper one".
# Asked with both rear apertures marked by projection on a straight rear view;
# he chose A, the rear window.  B (the engine lid, above) stays open: he called
# the upper one the MAIN bay, not the only one, and his earlier request for the
# trunk open is not withdrawn.
S.open_rear_hatch(log=log)
# The bay behind the engine lid, so the opening reads as a compartment and
# not a hole.  A LINING only -- see t1_shell.trunk_bay.__doc__ and the block
# above it for what is deliberately not in there.
#
# *** rev 49 -- THIS LINE SHIPPED THE BAY WITH NO MATERIAL AT ALL. ***
#
# `A()` only APPENDS to ASSIGN.  The loop that CONSUMES ASSIGN and actually
# calls MT.assign() is step 9, at line 846 -- NINETY-ONE LINES ABOVE THIS ONE.
# Step 8c has to run after step 9 because a lid hinged laterally moves v.co.x
# and step 8b shears on v.co.x; so this is the one A() call in the whole file
# that lands after its own consumer.  `trunk_bay` therefore rendered with
# Blender's default ~0.8-albedo grey, and the bay came back as the BRIGHTEST
# THING ON THE TAIL -- 1.28x the body red, 1.11x the cream -- where a T1's
# engine bay is a dark cavity.
#
# NOTHING SAID SO.  VERIFY printed 0 fail / 0 warn, verify_clone was ALL 110
# PASS, and the log line below printed "materials: 165 objects" WITH THIS
# OBJECT COUNTED IN THE 165 -- len(ASSIGN) counts appends, not assignments,
# so the one line that could have reported the gap asserted coverage instead.
# Rule 27, inverted: a cap nobody logs reads as coverage; a COUNT THAT LOGS
# THE WRONG QUANTITY reads as coverage too.  Rule 28 found it: one rear-3/4
# render, one crop.  This is the same defect rev 48 fixed for the louvre
# apertures (light where a dark bay belongs) IN THE SAME REVISION -- it was
# missed here only because no frame in rev 48 showed the tail.
# rev 49 -- THE TAIL BOARD.  The owner settled its identity this revision:
# "That was referring to a different sign. This one is part of the vehicle."
# The retirement he is being distinguished from is signboard()'s "La Santa"
# board, which stands on the GROUND BEHIND the bus in the same frame.  See
# t1_shell.tail_board.__doc__ for the three pieces of physical evidence that
# this one is attached, and for every measurement with its ceiling.
# T1_NOTAILBOARD=1 stands it down for an ablation.
if not os.environ.get("T1_NOTAILBOARD"):
    _tb, _tb_base, _tb_tip = S.tail_board(log=log)
    A(_tb, "countercream")
    MT.assign(_tb, M["countercream"])
    for _o, _tag in S.tail_board_edge(_tb_base, log=log):
        _k = "capred" if "RED" in _tag else "dark"
        A(_o, _k)
        MT.assign(_o, M[_k])
    _tb_stay = S.tail_board_stay(_tb_base, log=log)
    A(_tb_stay, "chrome")
    MT.assign(_tb_stay, M["chrome"])
    for _o in S.tail_board_bulbs(_tb_base, _tb_tip, log=log):
        A(_o, "bulb")
        MT.assign(_o, M["bulb"])

_trunk_bay = S.trunk_bay(log=log)
A(_trunk_bay, "dark")                 # keep it in ASSIGN, for the guard below
if not os.environ.get("T1_BAREMAT"):  # T1_BAREMAT=1 reproduces the rev-48 defect
    MT.assign(_trunk_bay, M["dark"])  # ...AND apply it, because step 9 is behind us

# THE GUARD, IN THE SAME EDIT (rule 12), AND WATCHED FAIL (rule 19).
# Written against the CAUSE, not the instance: any future A() call that lands
# after step 9 fires this, whatever object it is.  T1_BAREMAT=1 skips the
# repair above so the guard can be watched failing on the real defect.
_bare = [o.name for o, _k in ASSIGN
         if o.type == 'MESH' and not [m for m in o.data.materials if m]]
if _bare:
    raise AssertionError(
        "objects were given a material key but never assigned one: %s"
        "  -- an A() call landed AFTER step 9's ASSIGN loop (build.py:846)"
        % ", ".join(sorted(_bare)))
log(f"materials: {len(ASSIGN)} objects assigned, 0 bare (checked, not assumed)")

# rev 44, SPEC 10.103 -- ROUNDED EDGES.  Runs LAST, after every material
# datablock exists (t1_detail builds some of them at step 7, five steps
# before build_all()), and after the shear, so it can never interact with
# geometry: it only rewrites shading normals.  T1_NOBEVEL=1 stands it down.
MT.round_edges(log=log)
if FAILED_CUTS:
    log("!! cuts that failed and were rolled back: " + ", ".join(FAILED_CUTS))

if os.environ.get("T1_SAVE"):
    bpy.ops.wm.save_as_mainfile(filepath=os.environ["T1_SAVE"])
    log("saved " + os.environ["T1_SAVE"])

if os.environ.get("T1_VERIFY"):
    import verify; importlib.reload(verify)
    verify.run(body, log)

# ---------------------------------------------------------------------------
# T1_ABLATE -- rev 38.  Remove named objects from the built scene BEFORE the
# preview renders, so an ablation A/B can be shot in one process.
#
# WHY IT LIVES HERE AND NOT IN A WRAPPER: rev 37's ablation was attempted by
# APPENDING the removal to build.py, which executes AFTER the T1_PREVIEW block
# has already rendered -- so it removed the object from a scene nobody looked
# at and the test never ran.  SPEC's rule that a test you did not get to run is
# not a result.  The hook has to be upstream of the render, and this is it.
#
# THE POSITIVE CONTROL IS THE POINT.  A name that matches nothing RAISES.  An
# ablation that silently removes zero objects renders a frame identical to the
# baseline, and "identical" is exactly the reading that would be interpreted as
# "the object was not the bar" -- a false negative that looks like a finding.
# Default OFF: unset T1_ABLATE leaves the shipped path bit-identical.
_abl = os.environ.get("T1_ABLATE")
if _abl:
    _want = [n.strip() for n in _abl.split(",") if n.strip()]
    _gone = []
    for _n in _want:
        _hit = [o for o in bpy.data.objects if o.name == _n]
        if not _hit:
            raise SystemExit(
                "T1_ABLATE: no object named %r in the built scene -- REFUSING "
                "to render an ablation that removes nothing.  Present names "
                "matching a prefix: %s" % (
                    _n, sorted(o.name for o in bpy.data.objects
                               if o.name.startswith(_n[:5]))[:12]))
        for _o in _hit:
            _gone.append("%s (%dv)" % (_o.name, len(_o.data.vertices)
                                       if getattr(_o, "data", None)
                                       and hasattr(_o.data, "vertices") else -1))
            bpy.data.objects.remove(_o, do_unlink=True)
    log("T1_ABLATE removed %d object(s): %s" % (len(_gone), ", ".join(_gone)))

if os.environ.get("T1_PREVIEW"):
    import studio as ST; importlib.reload(ST)
    _scene = os.environ.get("T1_SCENE", "studio")
    if _scene == "playa":
        ST.ground_playa()
    else:
        ST.cyclorama()
    if os.environ.get("T1_CLAY"):
        ST.clay_all()
    if _scene == "playa":
        ST.playa(float(os.environ.get("T1_KEY", "1.0")))
    else:
        ST.lighting(float(os.environ.get("T1_KEY", "1.0")))
    # rev 44, SPEC 10.105 -- the cab was built and then rendered invisible.
    ST.cabin_fill(float(os.environ.get("T1_KEY", "1.0")))
    ST.camera()
    # rev 9: the Playa scene must NOT go through the studio's alpha-over path.
    # With transparent=True the film is keyed and composite_on_white() lays the
    # frame over pure white -- so ground_playa() renders but the WORLD does
    # not, and every Playa probe came back with a blown white sky and a hard
    # horizon line. That is the whole reason the rig "had not been
    # art-directed": it was never actually showing its environment.
    ST.render_set(os.environ["T1_PREVIEW"].split(","),
                  os.environ.get("T1_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")),
                  prefix=os.environ.get("T1_PFX", "c"),
                  res=(int(os.environ.get("T1_RX", "900")),
                       int(os.environ.get("T1_RY", "600"))),
                  samples=int(os.environ.get("T1_SAMP", "24")),
                  transparent=(_scene != "playa"), log=log)
