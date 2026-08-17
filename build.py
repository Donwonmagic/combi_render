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

# rev 12: THE ROOF HOLE.  Up to rev 11 no roof cutter was ever issued, so the
# lids floated over an unbroken roof skin and the galley was a sealed 2.8 mm
# steel box -- which is why the black serving bays survived six revisions of
# light tuning: the light had nowhere to enter.  ONE opening (SPEC sec.10.28,
# settled with the owner), cut here in step 3 like every other aperture, i.e.
# AFTER solidify.  It changes the roof's manifold state, so verify.py's
# non-manifold count and the shut-line probes must both be re-read at BOTH
# subdivision levels.
cut(body, S.roof_cutters(), "roof hole")

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
A(D.wipers(), "chrome_d")
A(D.handles(), "chrome")

for s in (1, -1):
    ring, lens, bowl = D.headlamp()
    # rev 10 (audit materials-6): the bezel is BRASS, not chrome.  Measured in
    # ref_side.jpg the bezel reads a* +2.1 / b* +31.6 at L* 65.6, against five
    # neutral references in the same frame at b* -2.4...+1.6 (cab door handle,
    # wing mirror, counter stainless, lamppost, pavement).  It is not a warm
    # bounce: every genuinely warm surface in that frame carries a* with its
    # b* (red 49/40, wall 11/11) and the bezel's ratio is 0.07.  R-B = +68.
    for o, k in ((ring, "brass"), (lens, "lens"), (bowl, "reflector")):
        D.place(o, loc=(2.1015, s * 0.5450, 1.0300)); A(o, k)
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
    D.place(ibase, loc=(2.0960, s * 0.6750, 1.2360)); A(ibase, "chrome")
    D.place(ilens, loc=(2.0960, s * 0.6750, 1.2360)); A(ilens, "amber")
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
    D.place(tl, loc=(T.X_TAIL + 0.0040, s * 0.6200, 0.8250)); A(tl, "amber")

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
ROUNDEL_Z_AG = 1.0170
ROUNDEL_Z = ROUNDEL_Z_AG + T.rake_drop(2.1155)
vr, vd = D.roundel(R=ROUNDEL_D / 2)
for o, k in ((vr, "roundelred"), (vd, "cream")):
    D.place(o, loc=(2.1155, 0.0, ROUNDEL_Z)); A(o, k)
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
for b in D.vw_logo_fit(ROUNDEL_D / 2, x=2.1210):   # V over W, never inverted
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
