"""Regression guard — asserts the machine-checkable rows of SPEC.md sec.6."""
import bpy, bmesh
from mathutils import Vector

TOL = 0.025
import t1_core as _T
SPEC = dict(L=4.280, W=1.720, H=1.940 - _T.RIDE_DROP, WB=2.400,
            TRACK_F=1.375, TRACK_R=1.360, TYRE_D=0.665)

BANNED = ("bed", "gate", "canopy", "fascia", "post")   # pickup-era geometry
NEED_MATS = ("T1_paint", "cream", "chrome", "glass", "wheelred",
             "script", "calidad")


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


def run(body, log=print):
    fails, warns = [], []

    lo, hi = _bounds()                      # everything: L over bumpers, H
    bb = [body.matrix_world @ Vector(c) for c in body.bound_box]
    bw = max(v.y for v in bb) - min(v.y for v in bb)   # body width only
    L, W, H = hi.x - lo.x, bw, hi.z
    log(f"  x range [{lo.x:.3f}, {hi.x:.3f}]   full-Y [{lo.y:.3f}, {hi.y:.3f}]")
    for nm, got, want in (("length", L, SPEC["L"]), ("width", W, SPEC["W"]),
                          ("height", H, SPEC["H"])):
        d = got - want
        (fails if abs(d) > TOL else warns if abs(d) > TOL * 0.5
         else []).append(f"{nm} {got:.3f} vs spec {want:.3f} ({d*1000:+.0f} mm)")
    log(f"  dims  L={L:.3f} W={W:.3f} H={H:.3f}")

    # 3. pickup-era geometry must be gone
    for ob in bpy.data.objects:
        n = ob.name.lower()
        for b in BANNED:
            if b in n:
                fails.append(f"banned object '{ob.name}' (matches '{b}')")

    # 4. serving bays: 3 open on the show side, bay 4 glazed
    glass_bays = [o.name for o in bpy.data.objects
                  if o.name.startswith("glass_bay")]
    show = [n for n in glass_bays if n.endswith("_L")]
    if len(show) != 1:
        fails.append(f"show side should have exactly 1 glazed bay, has "
                     f"{len(show)} ({show})")
    if not bpy.data.objects.get("glass_calidad"):
        fails.append("missing 100% CALIDAD frosted pane")

    # 5. materials
    for m in NEED_MATS:
        if m not in bpy.data.materials:
            fails.append(f"missing material '{m}'")

    # 6. roof must run to the tail
    zmax_tail = max((body.matrix_world @ v.co).z for v in body.data.vertices
                    if (body.matrix_world @ v.co).x < -1.60)
    if zmax_tail < 1.90 - _T.RIDE_DROP:
        fails.append(f"roof drops to {zmax_tail:.3f} aft of x=-1.60 "
                     "(bed-rail regression)")
    log(f"  roof at tail = {zmax_tail:.3f}")

    # 7. manifold body shell
    bm = bmesh.new(); bm.from_mesh(body.data)
    nm_e = sum(1 for e in bm.edges if not e.is_manifold)
    nm_v = sum(1 for v in bm.verts if not v.is_manifold)
    bm.free()
    if nm_e:
        warns.append(f"{nm_e} non-manifold edges / {nm_v} verts on the shell")

    log("  VERIFY: %d fail, %d warn" % (len(fails), len(warns)))
    for f in fails:
        log("    FAIL  " + f)
    for w in warns:
        log("    warn  " + w)
    return not fails
