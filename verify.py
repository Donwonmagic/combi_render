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
# SPEC rev 6 sec.2. NOTE: run() is called from build.py BEFORE the global
# ride-height drop is applied, so H here is the UN-DROPPED body height. Do not
# subtract RIDE_DROP from it -- doing so is what produced a phantom +60 mm fail.
# audit.py measures post-drop and will report H = 1.941 - RIDE_DROP.
SPEC = dict(L=4.290, W=1.750, H=1.941, WB=2.400,
            TRACK_F=1.369, TRACK_R=1.359, TYRE_D=0.665)
RIDE_DROP_SPEC = 0.065        # rev 6: the bus IS lowered. See SPEC sec.2.

BANNED = ("bed", "gate", "canopy", "fascia", "post")   # pickup-era geometry
NEED_MATS = ("T1_paint", "cream", "chrome", "glass", "wheelcream",
             "bumpercream", "roundelred", "countercream", "script", "calidad")

# SPEC rev 4 sec.1.1 — three apertures, then SOLID sheet metal
N_BAYS_OPEN = 3
BAY_PROBE_Z = 1.600                    # mid-band height
SOLID_PROBE_X = (-1.30, -1.55, -1.80)  # rear corner panel must be metal


def _bounds():
    lo = Vector((1e9, 1e9, 1e9)); hi = -lo
    for ob in bpy.data.objects:
        if ob.type != 'MESH' or ob.name in ("cyc",):
            continue
        for c in ob.bound_box:
            v = ob.matrix_world @ Vector(c)
            lo = Vector((min(lo[i], v[i]) for i in range(3)))
            hi = Vector((max(hi[i], v[i]) for i in range(3)))
    return lo, hi


def _has_metal(body, x, z, side=1):
    """True if the shell has sheet metal at (x, z) on the given flank.

    Cast a ray inboard along -Y from well outside the body. A serving aperture
    is a hole: the first hit is then the far flank or nothing at all, so the
    hit lands beyond the near flank's y. Tolerant of the 2.8 mm skin.
    """
    y_start = side * 3.0
    direction = Vector((0.0, -side, 0.0))
    ok, loc, _, _ = body.ray_cast(Vector((x, y_start, z)), direction)
    if not ok:
        return False
    return abs(loc.y) > 0.5          # near flank sits at |y| ~ 0.86


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
    for nm, got, want in (("length", L, SPEC["L"]), ("width", W, SPEC["W"]),
                          ("height", H, SPEC["H"])):
        d = got - want
        (fails if abs(d) > TOL else warns if abs(d) > TOL * 0.5
         else []).append(f"{nm} {got:.3f} vs spec {want:.3f} ({d*1000:+.0f} mm)")
    log(f"  dims  L={L:.3f} W={W:.3f} H={H:.3f}")

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
    opened = 0
    for i, (xr, xf) in enumerate(_S.BAYS):
        xm = (xr + xf) / 2.0
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
        if not _has_metal(body, xp, BAY_PROBE_Z, _S.SHOW_SIDE):
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
    for banned_mat in ("whitewall", "wheelred", "timber"):
        if banned_mat in bpy.data.materials:
            uses = [o.name for o in bpy.data.objects if o.type == 'MESH'
                    and any(s.material and s.material.name == banned_mat
                            for s in o.material_slots)]
            if uses:
                fails.append(f"retired material '{banned_mat}' is assigned to "
                             f"{len(uses)} objects e.g. {uses[0]} (SPEC 0.2)")

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

    log("  VERIFY: %d fail, %d warn" % (len(fails), len(warns)))
    for f in fails:
        log("    FAIL  " + f)
    for w in warns:
        log("    warn  " + w)
    return not fails
