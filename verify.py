"""Regression guard — asserts the machine-checkable rows of SPEC.md sec.9 (rev 4).

Design note: rev 3's version counted *panes* to decide whether the serving bays
existed. That is not a test of the shell — a boolean that silently rolled back
would leave the panes untouched and the guard green. Row 4 below now tests the
sheet metal itself.
"""
import bpy, bmesh
from mathutils import Vector

TOL = 0.025
import t1_core as _T

# SPEC rev 4 sec.2 — factory-sourced 1963 T1 hard points
#
# FRAME. MEASURED 2026-08-09, and the note that used to sit here was wrong.
# build.py calls run() at line 354, AFTER step 8b has already subtracted
# RIDE_DROP from every vertex, so the mesh run() sees is DROPPED. Two
# consequences, and they pull in opposite directions:
#
#  1. SPEC["H"] = 1.941 is a DROPPED figure and must stay as it is. It is
#     compared against a height measured off the same dropped mesh (1.936).
#     "Correcting" it to 1.941 - RIDE_DROP is what produced a phantom +60 mm
#     failure once. Do not.
#  2. Every probe coordinate taken from AUTHORED geometry -- Z_SILL, Z_HEAD,
#     DOOR_GAP, REAR_Z, WS_MID -- is in the UN-DROPPED frame and MUST have
#     RIDE_DROP subtracted before it is used to aim a ray. Skipping that on a
#     5.5 mm shut line reads 26 % open instead of 100 %.
#
# _frame_dz() below carries (2) so the two never get confused again.
SPEC = dict(L=4.290, W=1.750, H=1.941, WB=2.400,
            TRACK_F=1.369, TRACK_R=1.359, TYRE_D=0.665,
            # rev 8: REF_MEASUREMENTS sec.2.3 measures 1.960 on the fixed roof
            # aft of the lid opening, at the rear-axle station. That is the
            # number the rake was tuned to reproduce.
            H_ROOF=1.960)
RIDE_DROP_SPEC = 0.065        # rev 6: the bus IS lowered. See SPEC sec.2.

BANNED = ("bed", "gate", "canopy", "fascia", "post")   # pickup-era geometry

# Material names this project has ever used for a reading SPEC sec.0.2 retires.
# Only names that are actually MATERIAL keys belong here -- sec.0.2 is prose, so
# the mapping from a retired reading to the datablock that implemented it has to
# be stated once. The guard below reads sec.0.2 and warns about any retired
# reading whose token is NOT in this map, which is what stops the next `canvas`.
_RETIRED_MAT = {
    "whitewall": "whitewall tyres",
    "wheelred": "red rims",
    "timber": "timber plank counter",
    "canvas": "folding canvas ragtop",
}


# Number of bullets in SPEC sec.0.2 that _RETIRED_MAT has been reviewed against.
# Bump this ONLY together with a review of the map above.
_RETIRED_BULLETS_REVIEWED = 16


def _retired_material_tokens():
    """Material names banned because SPEC sec.0.2 retires the reading."""
    return set(_RETIRED_MAT)


def _retired_section_drift():
    """Has SPEC sec.0.2 gained a retired reading nobody mapped to a material?

    The first attempt at this scanned sec.0.2 for material names directly. That
    cannot work: every bullet is "<retired reading> — <correction>", and the
    material names are ordinary English words that appear on BOTH sides.
    'gold side script — it is silver' contains 'script'; 'chrome bumpers — they
    are painted cream' contains 'chrome' and 'cream'. It flagged six correct
    materials as retired.

    So the map stays explicit and reviewed, and this checks only that it has
    been reviewed against the CURRENT sec.0.2. That closes the actual failure --
    'canvas' was retired in the spec in rev 4 and nobody armed the guard, so it
    shipped for three revisions -- without inventing false positives.
    """
    import os as _os
    spec = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "SPEC.md")
    try:
        txt = open(spec, encoding="utf-8").read()
        sec = txt.split("## 0.2")[1].split("\n## ")[0]
    except Exception:
        return None
    n = sum(1 for ln in sec.splitlines() if ln.strip().startswith("- "))
    if n != _RETIRED_BULLETS_REVIEWED:
        return (f"SPEC 0.2 now has {n} retired readings, last reviewed at "
                f"{_RETIRED_BULLETS_REVIEWED}. Check verify._RETIRED_MAT maps "
                "every one that was implemented as a material, then bump "
                "_RETIRED_BULLETS_REVIEWED. This is how 'canvas' shipped for "
                "three revisions after the spec retired it.")
    return None
NEED_MATS = ("T1_paint", "cream", "chrome", "glass", "wheelcream",
             "bumpercream", "roundelred", "countercream", "script", "calidad")

# SPEC rev 4 sec.1.1 — three apertures, then SOLID sheet metal
N_BAYS_OPEN = 3
# rev 6 corrected: the window band is Z_SILL 1.372 / Z_HEAD 1.775 UN-DROPPED
# (1.307 / 1.710 above ground).  Derive the probe height instead of hard-
# coding it — the old literal 1.600 was keyed to the retired 1.402/1.798 band
# and would have silently drifted toward the head rail.
def _bay_probe_z(S):
    return (S.Z_SILL + S.Z_HEAD) / 2.0


# rear corner panel must be metal.  Bay 2's rear edge is at x = -0.960.
SOLID_PROBE_X = (-1.05, -1.30, -1.55, -1.80)

# MEASURED serving-bay edges, (rear, front) to match t1_shell.BAYS
BAYS_SPEC = ((0.3130, 0.8200), (-0.3210, 0.1950), (-0.9600, -0.4350))
BAND_SPEC = (1.3720, 1.7750)           # Z_SILL, Z_HEAD, UN-DROPPED
# a shut line is a 5.5 mm slot; allow a few samples to be occluded by a seal
SLOT_FRAC_MIN = 0.90


def _bounds():
    lo = Vector((1e9, 1e9, 1e9)); hi = -lo
    for ob in bpy.data.objects:
        if ob.type != 'MESH' or ob.name in ("cyc", "counter", "counter_nosing"):
            continue
        for c in ob.bound_box:
            v = ob.matrix_world @ Vector(c)
            lo = Vector((min(lo[i], v[i]) for i in range(3)))
            hi = Vector((max(hi[i], v[i]) for i in range(3)))
    return lo, hi


def _frame_dz(x=None):
    """z offset from the AUTHORED frame to the frame the mesh is actually in.

    build.py sets RIDE_DROP_APPLIED just after step 8b. Default to "applied"
    if the flag is missing, because that is what build.py has always done and
    an un-offset probe silently under-reports rather than failing loudly.

    rev 8: step 8b SHEARS rather than dropping, so this offset depends on the
    station. `x` is REQUIRED for any probe that aims a ray at a specific place;
    calling it bare returns the offset at t1_core.X_DROP_REF, which is only
    correct at that one station. A probe 5.5 mm wide aimed one station off is
    exactly how rev 6 read a shut line as 26 % open instead of 100 %.
    """
    try:
        import __main__
        applied = getattr(__main__, "RIDE_DROP_APPLIED", True)
    except Exception:
        applied = True
    if not applied:
        return 0.0
    return -_T.rake_drop(_T.X_DROP_REF if x is None else x)


def _roof_z_at(xq, tol=0.05):
    """Highest point of the FIXED roof at station xq (excludes the raised lids)."""
    body = bpy.data.objects.get("T1_body")
    if body is None:
        return float('nan')
    mw = body.matrix_world
    zs = [(mw @ v.co).z for v in body.data.vertices
          if abs((mw @ v.co).x - xq) < tol and abs((mw @ v.co).y) < 0.35]
    return max(zs) if zs else float('nan')


def _has_metal(body, x, z, side=1):
    """True if the shell has sheet metal at (x, z) on the given flank.

    Cast a ray inboard along -Y from well outside the body. A serving aperture
    is a hole: the first hit is then the FAR flank (loc.y on the opposite
    side) or nothing at all. Testing abs(loc.y) alone cannot tell those apart
    — it reports 0.87 either way — so the sign against `side` is what makes
    this a test rather than a coin flip.
    """
    y_start = side * 3.0
    direction = Vector((0.0, -side, 0.0))
    ok, loc, _, _ = body.ray_cast(Vector((x, y_start, z)), direction)
    if not ok:
        return False
    return loc.y * side > 0.5        # near flank sits at |y| ~ 0.86


def _flank_open(body, x, z, side):
    """True if a ray inboard at (x, z) gets past the near skin: hole or slot"""
    return not _has_metal(body, x, z, side)


def _ray_clear(body, origin, direction, dist):
    """True if the body has no surface within `dist` of `origin` along `direction`"""
    return not body.ray_cast(Vector(origin), Vector(direction).normalized(),
                             distance=dist)[0]


def _slot_frac(body, outline, side, dzf):
    """rev 8: dzf is a CALLABLE of x, not a scalar -- the shear moves the frame
    33 mm for every metre forward, and a 5.5 mm shut line probed one station off
    reads closed."""
    """fraction of samples along a flank (x, z) outline that are open slots"""
    n = sum(1 for (x, z) in outline if _flank_open(body, x, z + dzf(x), side))
    return n / max(len(outline), 1)


def _englid_frac(body, outline, dz):
    # engine lid is at a fixed tail station, so a scalar dz is correct here
    """fraction of samples along the tail (y, z) outline that are open slots.

    Cast forward along +X from well behind the tail. The tail skin sits at
    x ~ -2.09; anything the ray reaches forward of -1.95 means it got through.
    """
    ok_n = 0
    for (y, z) in outline:
        hit, loc, _, _ = body.ray_cast(Vector((-3.0, y, z + dz)),
                                       Vector((1, 0, 0)))
        if (not hit) or loc.x > -1.95:
            ok_n += 1
    return ok_n / max(len(outline), 1)


def _check_opaque(obname):
    """The decal panels sit on SOLID sheet metal. Assert the material bound to
    the object is opaque: Transmission Weight must be UNLINKED and 0.0 on
    every Principled BSDF in it."""
    out = []
    ob = bpy.data.objects.get(obname)
    if not ob:
        return out
    mats = [s.material for s in ob.material_slots if s.material]
    if not mats:
        out.append(f"'{obname}' has no material bound")
        return out
    for m in mats:
        if not m.use_nodes or not m.node_tree:
            continue
        pr = [n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED']
        if not pr:
            out.append(f"'{obname}' material '{m.name}' has no Principled BSDF")
        for n in pr:
            s = n.inputs["Transmission Weight"]
            if s.is_linked:
                out.append(f"'{obname}' material '{m.name}' has Transmission "
                           "Weight LINKED -- it is painted sheet metal, not "
                           "a frosted pane (SPEC 0.2)")
            elif abs(s.default_value) > 1e-6:
                out.append(f"'{obname}' material '{m.name}' has Transmission "
                           f"Weight {s.default_value:.3f}, must be 0.0 -- it "
                           "is painted sheet metal (SPEC 0.2)")
    return out


def _measure_wheels():
    """Track and tyre diameter measured from geometry, not read from constants."""
    out = {}
    for tag, xa in (("F", _T.X_AXLE_F), ("R", _T.X_AXLE_R)):
        ys, zs = [], []
        for ob in bpy.data.objects:
            if not ob.name.startswith("tyre"):
                continue
            vs = [ob.matrix_world @ v.co for v in ob.data.vertices]
            if abs(sum(v.x for v in vs) / len(vs) - xa) > 0.30:
                continue
            ys.append(sum(v.y for v in vs) / len(vs))
            zs += [v.z for v in vs]
        if len(ys) == 2:
            out["TRACK_" + tag] = abs(ys[0] - ys[1])
        if zs:
            out["TYRE_D"] = max(zs) - min(zs)
    return out


def run(body, log=print):
    fails, warns = [], []

    # 1. overall dimensions
    lo, hi = _bounds()
    bb = [body.matrix_world @ Vector(c) for c in body.bound_box]
    bw = max(v.y for v in bb) - min(v.y for v in bb)
    L, W, H = hi.x - lo.x, bw, hi.z
    log(f"  x range [{lo.x:.3f}, {hi.x:.3f}]   full-Y [{lo.y:.3f}, {hi.y:.3f}]")
    # rev 8: HEIGHT IS NOT A SCALAR ANY MORE, twice over. The vehicle is raked,
    # so the roof is a sloping line; and the roof lids are modelled OPEN, so the
    # bbox top is the raised signboard at ~3.0 m, not the vehicle. Measure the
    # ROOF at the rear-axle station -- the highest point of the fixed roof, and
    # the station REF_MEASUREMENTS sec.2.3 took its 1.960 at.
    Hroof = _roof_z_at(_T.X_AXLE_R)
    # The roof row carries REF_MEASUREMENTS sec.2.3's own +/- 0.030 stated band
    # on top of the model tolerance -- it is a photograph measurement, not a
    # factory figure. rev 8 residual: -37 mm (was -89 mm before the rake).
    for nm, got, want, tol in (("length", L, SPEC["L"], TOL),
                               ("width", W, SPEC["W"], TOL),
                               ("roof @ rear axle", Hroof, SPEC["H_ROOF"], 0.040)):
        d = got - want
        (fails if abs(d) > tol else warns if abs(d) > tol * 0.5
         else []).append(f"{nm} {got:.3f} vs spec {want:.3f} ({d*1000:+.0f} mm)")
    log(f"  dims  L={L:.3f} W={W:.3f} roof@rear-axle={Hroof:.3f} (bbox top {H:.3f})")

    # 2. wheelbase / track / tyre diameter, MEASURED
    m = _measure_wheels()
    for k in ("TRACK_F", "TRACK_R", "TYRE_D"):
        if k not in m:
            fails.append(f"could not measure {k} from geometry")
            continue
        d = m[k] - SPEC[k]
        if abs(d) > TOL:
            fails.append(f"{k} {m[k]:.4f} vs spec {SPEC[k]:.4f} ({d*1000:+.0f} mm)")
    if m:
        log("  measured " + "  ".join(f"{k}={v:.4f}" for k, v in sorted(m.items())))

    # 3. pickup-era geometry must be gone
    for ob in bpy.data.objects:
        n = ob.name.lower()
        for b in BANNED:
            if b in n:
                fails.append(f"banned object '{ob.name}' (matches '{b}')")

    # 4. exactly three OPEN apertures on the show side — tested on the shell
    import t1_shell as _S
    # rev 8: the probe height is now per-bay, because the shear moves the
    # window band down by 33 mm for every metre forward. One scalar probe z
    # across bays 0.82 m apart would miss by 27 mm.
    _bpz = _bay_probe_z(_S)
    opened = 0
    for i, (xr, xf) in enumerate(_S.BAYS):
        xm = (xr + xf) / 2.0
        BAY_PROBE_Z = _bpz + _frame_dz(xm)       # authored -> mesh frame, at xm
        if not _has_metal(body, xm, BAY_PROBE_Z, _S.SHOW_SIDE):
            opened += 1
        else:
            fails.append(f"serving bay {i} at x={xm:.3f} is NOT open "
                         "(boolean rolled back, or bay never cut)")
    if opened != N_BAYS_OPEN:
        fails.append(f"show side has {opened} open apertures, spec says "
                     f"{N_BAYS_OPEN}")
    log(f"  open serving apertures on +Y: {opened}")

    # 5. no fourth bay — the rear corner panel must be solid sheet metal
    if len(_S.BAYS) != N_BAYS_OPEN:
        fails.append(f"t1_shell.BAYS has {len(_S.BAYS)} entries, spec says "
                     f"{N_BAYS_OPEN} (a fourth bay is a rev-3 regression)")
    for xp in SOLID_PROBE_X:
        if not _has_metal(body, xp, _bpz + _frame_dz(xp), _S.SHOW_SIDE):
            fails.append(f"rear corner panel is open at x={xp:.2f} — it must be "
                         "solid metal carrying the 100% Calidad decal")
    if bpy.data.objects.get("glass_calidad"):
        fails.append("'glass_calidad' exists — the decal goes on sheet metal, "
                     "not a frosted pane (SPEC 0.2)")
    if bpy.data.objects.get("glass_bay3_L"):
        fails.append("'glass_bay3_L' exists — there is no fourth bay")
    if not bpy.data.objects.get("calidad_L"):
        fails.append("missing 'calidad_L' decal panel")
    # 5b. and the material actually ON it must be PAINT, not glass. rev 3's
    # frosted_calidad() set Transmission Weight 0.88 and rendered the panel
    # 51.9 sRGB code values darker than the surrounding cream (55.0 % of its
    # linear reflectance) inside a hard rectangular border. Testing only that
    # the object and a material of that name exist passes with that defect
    # present, which is how it came back.
    fails += _check_opaque("calidad_L")

    # 6b. SPEC: nothing on this vehicle is translucent. No subsurface, ever.
    for mt in bpy.data.materials:
        if not mt.use_nodes or not mt.node_tree:
            continue
        for n in mt.node_tree.nodes:
            if n.type != 'BSDF_PRINCIPLED':
                continue
            s = n.inputs.get("Subsurface Weight")
            if s is None:
                continue
            if s.is_linked or s.default_value > 1e-6:
                fails.append(f"material '{mt.name}' has Subsurface Weight "
                             f"{'linked' if s.is_linked else s.default_value}"
                             " -- SPEC allows none anywhere")

    # 6. materials
    for mt in NEED_MATS:
        if mt not in bpy.data.materials:
            fails.append(f"missing material '{mt}'")
    # rev 8: this used to be the hand-written list ("whitewall", "wheelred",
    # "timber") -- the retired materials somebody remembered to type. `canvas`
    # was never added, so a folding CANVAS ragtop that SPEC sec.0.2 retired in
    # rev 4 shipped green through three revisions and every guard passed over
    # it. The list is now DERIVED from sec.0.2 itself, so retiring a reading in
    # the spec arms the guard automatically and this class of miss is closed.
    for banned_mat in _retired_material_tokens():
        if banned_mat in bpy.data.materials:
            uses = [o.name for o in bpy.data.objects if o.type == 'MESH'
                    and any(s.material and s.material.name == banned_mat
                            for s in o.material_slots)]
            if uses:
                fails.append(f"retired material '{banned_mat}' is assigned to "
                             f"{len(uses)} objects e.g. {uses[0]} (SPEC 0.2)")
    _drift = _retired_section_drift()
    if _drift:
        warns.append(_drift)
    # ...and the geometry that carried them
    for ob in bpy.data.objects:
        if ob.type == 'MESH' and ob.name.split('.')[0] in ("rag", "ragframe"):
            fails.append(f"'{ob.name}' is folding-ragtop geometry; the roof is "
                         "cut into rigid hinged steel lids (SPEC 0.2)")

    # 7. roof must run to the tail
    zmax_tail = max((body.matrix_world @ v.co).z for v in body.data.vertices
                    if (body.matrix_world @ v.co).x < -1.60)
    if zmax_tail < 1.90 - _T.RIDE_DROP:
        fails.append(f"roof drops to {zmax_tail:.3f} aft of x=-1.60 "
                     "(bed-rail regression)")
    log(f"  roof at tail = {zmax_tail:.3f}")

    # 8. manifold body shell — SPEC has always said FAIL, rev 3 only warned
    bm = bmesh.new(); bm.from_mesh(body.data)
    nm_e = sum(1 for e in bm.edges if not e.is_manifold)
    nm_v = sum(1 for v in bm.verts if not v.is_manifold)
    bm.free()
    if nm_e:
        fails.append(f"{nm_e} non-manifold edges / {nm_v} verts on the shell")

    # 9. no boolean may have rolled back
    try:
        import __main__
        fc = getattr(__main__, "FAILED_CUTS", [])
    except Exception:
        fc = []
    if fc:
        fails.append(f"{len(fc)} boolean(s) rolled back: {', '.join(fc)}")

    # 10. ride height. rev 4 asserted stock and was WRONG; the measured rear
    # arch-to-tyre gap is 41 mm against a stock 90-120. Guard the real value in
    # BOTH directions so neither a reset-to-stock nor a drift reappears.
    if abs(_T.RIDE_DROP - RIDE_DROP_SPEC) > 0.005:
        fails.append(f"RIDE_DROP={_T.RIDE_DROP:.4f}; SPEC rev 6 says "
                     f"{RIDE_DROP_SPEC:.3f} (the bus is lowered)")
    gap = _S.ARCH_R - _T.TIRE_R
    if abs(gap - 0.041) > 0.008:
        fails.append(f"arch-to-tyre gap {gap*1000:.0f} mm; measured 41 mm")

    # ---------------------------------------------------------------------
    # 11. POSITIVE feature assertions.
    #
    # Row 9 only reports FAILED_CUTS. That is a report of the build's own
    # bookkeeping, not a test of the mesh: a boolean that was rolled back
    # leaves a perfectly VALID, manifold, correctly-sized shell with the
    # feature silently missing, and a cut that was never issued at all leaves
    # nothing for row 9 to report. That is exactly how the shipped model went
    # out with no cab-door shut line. Assert instead that every expected
    # aperture and every expected shut line is actually THERE, measured off
    # the geometry.
    #
    # Frame: run() executes BEFORE build.py step 8b, so every z here is
    # UN-DROPPED.
    ss = _S.SHOW_SIDE
    # 11a. cab door glazing — main + vent, both flanks
    for outline, tag in ((_S.DOOR_MAIN_S, "cab door glass"),
                         (_S.DOOR_VENT_S, "cab door vent")):
        cx = sum(p[0] for p in outline) / len(outline)
        cz = sum(p[1] for p in outline) / len(outline) + _frame_dz(cx)
        for s in (1, -1):
            if not _flank_open(body, cx, cz, s):
                fails.append(f"{tag} aperture on {'+' if s > 0 else '-'}Y is "
                             f"NOT cut at ({cx:.3f}, {cz:.3f})")

    # 11b. serving bays — the off side is glazed but still an aperture in the
    # sheet metal, and row 4 only ever tested the show side
    for i, (xr, xf) in enumerate(_S.BAYS):
        xm = (xr + xf) / 2.0
        if not _flank_open(body, xm, _bpz + _frame_dz(xm), -ss):
            fails.append(f"serving bay {i} at x={xm:.3f} is NOT cut on the "
                         "off side")

    # 11c. windscreen — probe along the screen normal, 60 mm each way
    for s in (1, -1):
        yc = s * (_S.WS_DIV + _S.WS_PANE_W / 2)
        o = (_S.WS_MID + Vector((0.0, yc, _frame_dz(_S.WS_MID.x)))
             + _S.WS_N * 0.060)
        if not _ray_clear(body, o, -_S.WS_N, 0.120):
            fails.append(f"windscreen pane {'L' if s > 0 else 'R'} is NOT cut")

    # 11d. rear window
    if not _ray_clear(body, (-2.40, 0.0, _S.REAR_Z + _frame_dz(_T.X_TAIL)),
                      (1, 0, 0), 0.35):
        fails.append("rear window is NOT cut")

    # 11e. shut lines. A gap cutter makes a 5.5 mm through-slot; sample the
    # outline and require most samples to pass the near skin.
    for s in (1, -1):
        fr = _slot_frac(body, _S.DOOR_GAP_S, s, _frame_dz)
        if fr < SLOT_FRAC_MIN:
            fails.append(f"cab door shut line on {'+' if s > 0 else '-'}Y is "
                         f"missing: only {fr*100:.0f} % of {len(_S.DOOR_GAP_S)}"
                         f" outline samples are open slots")
        log(f"  shut line door{s:+d}: {fr*100:.0f} % open")
    fr = _slot_frac(body, _S.CARGO_GAP, -ss, _frame_dz)
    if fr < SLOT_FRAC_MIN:
        fails.append(f"cargo door shut line is missing: only {fr*100:.0f} % of "
                     f"{len(_S.CARGO_GAP)} outline samples are open slots")
    log(f"  shut line cargo: {fr*100:.0f} % open")
    fr = _englid_frac(body, _S.ENGLID_GAP, _frame_dz(_T.X_TAIL))
    if fr < SLOT_FRAC_MIN:
        fails.append(f"engine lid shut line is missing: only {fr*100:.0f} % of "
                     f"{len(_S.ENGLID_GAP)} outline samples are open slots")
    log(f"  shut line englid: {fr*100:.0f} % open")

    # 11f. the shut lines and the bays must not be see-through. SPEC sec.6:
    # the hatches read as depth, not as holes. Both door gaps are collinear
    # slots and the bays are cut on both flanks, so without an inner skin a
    # ray straight through crosses nothing at all.
    dg = bpy.context.evaluated_depsgraph_get()
    sc = bpy.context.scene
    for name, samples, side in (("cab door +Y", _S.DOOR_GAP_S, 1),
                                ("cab door -Y", _S.DOOR_GAP_S, -1)):
        thru = 0
        for (x, z) in samples:
            r = sc.ray_cast(dg, Vector((x, side * 3.0, z + _frame_dz(x))),
                            Vector((0.0, -side, 0.0)))
            if (not r[0]) or r[1].y * side < 0.0:
                thru += 1
        if thru:
            fails.append(f"{name} shut line is SEE-THROUGH: {thru} of "
                         f"{len(samples)} rays cross no surface (SPEC 6 wants "
                         "an inner skin behind the slot)")
    for i, (xr, xf) in enumerate(_S.BAYS):
        xm = (xr + xf) / 2.0
        r = sc.ray_cast(dg, Vector((xm, ss * 3.0, _bpz + _frame_dz(xm))),
                        Vector((0.0, -ss, 0.0)))
        if (not r[0]) or abs(r[1].y) > 0.80:
            fails.append(f"serving bay {i} has nothing behind it — a "
                         "600 x 400 mm hole, not a hatch (SPEC 6)")

    # 12. the corrected measured constants, both frames.
    #
    # Z_SILL / Z_HEAD / BAYS / DOOR_GAP live in t1_shell and are UN-DROPPED:
    # they build cutter geometry before step 8b. Z_BELT / V_APEX / V_RISE /
    # V_POW live in t1_mats and are ABOVE-GROUND, because a shader reads
    # Geometry->Position at RENDER time off the already-dropped mesh. Getting
    # that backwards puts the paint 65 mm out. The pressed swage in
    # t1_shell.zV() therefore carries the same numbers PLUS RIDE_DROP; if the
    # two drift the crease and the two-tone line separate.
    import t1_mats as _MT
    if abs((_MT.V_APEX + _MT.V_RISE) - _MT.Z_BELT) > 1e-9:
        fails.append(f"V_APEX {_MT.V_APEX} + V_RISE {_MT.V_RISE} != Z_BELT "
                     f"{_MT.Z_BELT}: the V arms miss the flank belt line")
    if _MT.V_APEX > 0.3960 + 1e-9:
        fails.append(f"V_APEX {_MT.V_APEX:.4f} above ground exceeds the hard "
                     "bound 0.396 set by the bumper occlusion in "
                     "ref_workshop.jpg")
    if _MT.V_POW >= 1.0:
        fails.append(f"V_POW {_MT.V_POW} >= 1: the measured V profile is "
                     "CONCAVE, not convex")
    for nm, geo, sha in (("V_APEX", _S.V_APEX_Z - _T.RIDE_DROP, _MT.V_APEX),
                         ("V_RISE", _S.V_RISE_Z, _MT.V_RISE),
                         ("V_POW", _S.V_POW_Z, _MT.V_POW)):
        if abs(geo - sha) > 1e-6:
            fails.append(f"{nm} de-registered: pressed swage says {geo:.4f} "
                         f"above ground, painted break says {sha:.4f}")
    if abs(_S.zV(_S.V_HALF_W) - (_MT.Z_BELT + _T.RIDE_DROP)) > 1e-6:
        fails.append("the V-swage arms do not land on the belt line at "
                     f"|y| = {_S.V_HALF_W}")
    for nm, got, want in (("Z_SILL", _S.Z_SILL, BAND_SPEC[0]),
                          ("Z_HEAD", _S.Z_HEAD, BAND_SPEC[1])):
        if abs(got - want) > 1e-6:
            fails.append(f"{nm} {got:.4f} un-dropped; measured {want:.4f} "
                         f"({want - _T.RIDE_DROP:.4f} above ground)")
    if len(_S.BAYS) == len(BAYS_SPEC):
        for i, (got, want) in enumerate(zip(_S.BAYS, BAYS_SPEC)):
            if abs(got[0] - want[0]) > 1e-6 or abs(got[1] - want[1]) > 1e-6:
                fails.append(f"serving bay {i} edges {got} vs measured {want} "
                             "(rev-3's evenly-spaced bays are retired)")
    log("  band %.3f-%.3f un-dropped (%.3f-%.3f AG)  bay widths %s"
        % (_S.Z_SILL, _S.Z_HEAD, _S.Z_SILL - _T.RIDE_DROP,
           _S.Z_HEAD - _T.RIDE_DROP,
           " ".join("%.3f" % (b[1] - b[0]) for b in _S.BAYS)))

    # Buried detail must never pass again: both wipers shipped for six
    # revisions fully enclosed in the nose skin. Casts camera -> object, not
    # object -> camera; the outward cast scores a buried part 100 % visible.
    try:
        fails += __import__("t1_detail").visibility_fails()
    except Exception as e:                       # never let the guard vanish
        fails.append("visibility assertion could not run: %s" % e)
    log("  VERIFY: %d fail, %d warn" % (len(fails), len(warns)))
    for f in fails:
        log("    FAIL  " + f)
    for w in warns:
        log("    warn  " + w)
    return not fails
