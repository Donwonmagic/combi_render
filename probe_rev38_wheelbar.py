"""rev 38 -- NAME the object his report 6 calls 'a bar obstructing the front wheel'.

METHOD: cast a ray from the hero34f camera through a grid of PIXELS covering the
member visible above the front tyre, and report which object each ray hits FIRST.
This is an IDENTIFICATION BY CONSTRUCTION, not a pixel inference: no colour, no
threshold and no segmentation enters.  The brief's candidate (doorback1) was
ablated and the member did not move, so the candidate is refuted and this
restarts the search.

CONTROLS (a ray-caster that hits nothing tells you nothing):
  C1  a ray aimed at the tyre's centre must hit a wheel object
  C2  a ray aimed at the red flank above the arch must hit the body
  C3  a ray aimed at empty background must hit NOTHING
  C4  the camera must resolve to hero34f's published loc/tgt
"""
import bpy, os, sys, math, importlib
from mathutils import Vector

try:
    ROOT = os.path.dirname(os.path.abspath(__file__))
except NameError:
    ROOT = os.getcwd()
sys.path.insert(0, ROOT)

# Build the vehicle the way audit.py and probe_dust_scope.py do: exec build.py
# truncated at its T1_SAVE split.  THE FIRST DRAFT OF THIS PROBE DID NOT DO
# THIS and ran against Blender's default startup cube -- every ray hit "Cube"
# and the tally printed a confident, well-formatted, entirely fictional result.
# C1-C3 caught it.  That is the whole reason they are here: a ray-caster that
# hits SOMETHING always produces a plausible answer.
_src = open(os.path.join(ROOT, "build.py")).read().split(
    'if os.environ.get("T1_SAVE")')[0]
exec(compile(_src, "build.py", "exec"))

import studio as ST

sc = bpy.context.scene
RX, RY = 1600, 1067
sc.render.resolution_x, sc.render.resolution_y = RX, RY
sc.render.resolution_percentage = 100
cam = ST.camera()
sc.camera = cam
V = ST.views()["hero34f"]
# render_set() aims the camera per view; standalone we must do the same or the
# camera sits at the origin and EVERY ray misses -- which reads as "the member
# is not an object", a false negative dressed as a finding.  C4 is the control.
ST.aim(cam, V["loc"], V["tgt"], V.get("lens"), V.get("ortho"),
       V.get("focus"), V.get("fstop"))
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
print("\n" + "=" * 78)
print("  camera hero34f  loc=%s  published=%s" % (
    tuple(round(v, 4) for v in cam.location), V["loc"]))
ok4 = all(abs(a - b) < 1e-3 for a, b in zip(cam.location, V["loc"]))
print("  [%s] C4 camera resolves to hero34f's published loc" % ("PASS" if ok4 else "FAIL"))

def ray(px, py):
    """px,py in PIXELS, origin top-left."""
    ndc_x = (px + 0.5) / RX
    ndc_y = 1.0 - (py + 0.5) / RY
    # camera frame at unit distance
    fr = cam.data.view_frame(scene=sc)          # 4 corners, camera space
    tr, br, bl, tl = fr
    p = tl.lerp(tr, ndc_x).lerp(bl.lerp(br, ndc_x), 1.0 - ndc_y)
    M = cam.matrix_world
    if cam.data.type == 'ORTHO':
        # rev 59.  An ORTHOGRAPHIC camera has no eye point: every ray shares a
        # direction and each pixel has its OWN origin.  The perspective form
        # below aimed every ray from the camera's origin, which for the side
        # ortho is one point 26 m out on +y -- a fan, not a projection, and it
        # lands nowhere near the pixel it claims.  Kept separate so the
        # perspective path is untouched bit for bit.
        o = M @ Vector((p.x, p.y, 0.0))
        d = (M.to_3x3() @ Vector((0.0, 0.0, -1.0))).normalized()
    else:
        o = M.translation
        d = (M.to_3x3() @ p).normalized()
    hit, loc, nor, idx, obj, mat = sc.ray_cast(dg, o, d)
    if not hit:
        return None, None, None, d
    return obj.name, loc, nor, d

# ---- controls
ctl = [("C1 wheel centre",     (747, 843), "WHEEL"),
       ("C2 red flank",        (700, 640), "body"),
       ("C3 empty background", (120, 120), None)]
print()
for nm, (px, py), want in ctl:
    o, L, N, D = ray(px, py)
    if want is None:
        good = o is None
    elif want == "WHEEL":
        # The pixel lands on the HUB CAP, which is a wheel part.  The first
        # draft asked for "tyre" in the name and read cap1.31 as a failure --
        # the CONTROL's scope was wrong, not the result.  Repair the scope;
        # never re-aim the ray until it hits the name you first wrote down.
        good = o is not None and any(k in o.lower()
                                     for k in ("tyre", "rim", "cap"))
    else:
        good = o is not None and want in o.lower()
    print("  [%s] %s -> %s" % ("PASS" if good else "FAIL", nm, o))

# ---- the member itself, and the WHOLE front arch aperture
print("\n  --- rays through the member above the front tyre ---")
from collections import Counter
tally = Counter()
for py in range(756, 790, 2):
    row = []
    for px in range(725, 830, 5):
        o, L, N, D = ray(px, py)
        row.append(o or ".")
        if o: tally[o] += 1
    print("  row %4d : %s" % (py, " ".join(s0[:11] for s0 in row)))

print("\n  --- hit tally, member window ---")
def report(t):
    for n, c in t.most_common():
        ob = bpy.data.objects.get(n)
        if ob:
            bb = [ob.matrix_world @ Vector(cc) for cc in ob.bound_box]
            xs = [v.x for v in bb]; ys = [v.y for v in bb]; zs = [v.z for v in bb]
            print("   %-16s %5d hits   x[%.3f,%.3f] y[%.3f,%.3f] z[%.3f,%.3f]"
                  % (n, c, min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))
        else:
            print("   %-16s %5d hits" % (n, c))
report(tally)

# ---- SCOPE: what is visible through EACH arch aperture?
# The question a notch answers and a liner answers are different.  If only the
# cab floor shows, notching it is enough; if several interior objects show, the
# aperture itself is unclosed and the repair is an inner wing.  Decide from the
# census, not from the first object found.
print("\n  --- CENSUS: everything seen through the FRONT arch (px 700-860 x 740-830) ---")
front = Counter()
for py in range(740, 832, 2):
    for px in range(700, 862, 2):
        o, L, N, D = ray(px, py)
        if o: front[o] += 1
report(front)

print("\n  --- CONTROL: the REAR arch, same treatment (px 980-1120 x 690-790) ---")
rear = Counter()
for py in range(690, 792, 2):
    for px in range(980, 1122, 2):
        o, L, N, D = ray(px, py)
        if o: rear[o] += 1
report(rear)

ok5 = any("tyre" in n or "rim" in n for n in rear)
print("\n  [%s] C5 the rear-arch window actually lands on the rear wheel"
      % ("PASS" if ok5 else "FAIL"))

# rev 59.  "gal_floor" WAS NOT AN OBJECT IN THIS BUILD and never had been --
# `grep -rn "gal_floor" *.py` hit this line and nothing else, so the one
# interior object the REAR arch can actually show, the steel floor pan, was
# spelled wrong and counted as zero.  It is `van_floor` (t1_detail.galley,
# grep `name="van_floor"`).  A member of a set that names no object is a
# silent zero, which is why the rear census read clean while the render showed
# van_floor's 40 mm edge through the arch as a bar at hub height.
INTERIOR = {"cab_floor", "seat_base", "seat_back", "dash", "van_floor"}
if os.environ.get("T1_WB_OLDNAME") == "1":       # ABLATION: restore the typo
    INTERIOR = (INTERIOR - {"van_floor"}) | {"gal_floor"}
_missing = sorted(n for n in INTERIOR if n not in bpy.data.objects)
print("\n  [%s] C0 every INTERIOR name is an object in this build: %s"
      % ("PASS" if not _missing else "FAIL", _missing or "all present"))
fi = sum(c for n, c in front.items() if n in INTERIOR)
ri = sum(c for n, c in rear.items() if n in INTERIOR)
print("\n  interior-object rays through FRONT arch: %d" % fi)
print("  interior-object rays through REAR  arch: %d" % ri)
# ON ARRIVAL IN REV 38 there was NO arch liner anywhere in the build (grep: no
# liner, inner_wing, wheelwell, wheel_well, splash) and this line said so.  That
# sentence is now FALSE and is REPLACED rather than left standing -- a probe
# that keeps asserting a fact its own subject has moved past is exactly the
# defect this revision found in probe_dust_scope's mesh-count literal.
# rev 59, rule 8: PAINT THE WINDOW AND LOOK AT IT.  A census is a number from
# a window, and this window is a hard-coded pixel box that nobody had ever
# seen.  One glyph per object class, laid out where the rays actually landed.
def _glyph(n):
    if n is None:
        return "."
    if n in INTERIOR:
        return "#"                                   # interior -- the defect
    if n.startswith("wheelhouse"):
        return "L"                                   # liner
    if any(k in n for k in ("tyre", "rim", "cap")):
        return "o"                                   # wheel
    if "body" in n:
        return "="                                   # sheet metal
    return "?"
print("\n  --- the REAR census window, PAINTED  "
      "( . miss  = body  o wheel  L liner  # interior  ? other ) ---")
for py in range(690, 792, 4):
    line = "".join(_glyph(ray(px, py)[0]) for px in range(980, 1122, 2))
    print("  %4d %s" % (py, line))

# --------------------------------------------------------------------------
# rev 59 -- THE REAR ARM OF THIS PROBE WAS BLIND TWICE OVER, AND BOTH ARE HERE.
#
#   1. Its window was a HARD-CODED PIXEL BOX in the hero34f camera.  Painted
#      above, it is mostly background and flank decal and it does not cover the
#      ends of the rear arch, which is where rev 59's defect lives.  The window
#      is now DERIVED from the aperture's own geometry -- the front's circle of
#      ARCH_R, the rear's `rear_arch_outline` -- projected through whichever
#      camera is being asked.  A window that is computed from the thing it is
#      meant to frame cannot drift off it.
#   2. It only ever asked hero34f, a 3/4 FRONT view, about the REAR arch, where
#      the arch is small, oblique and half self-occluded.  The side ortho is
#      the view the defect was reported in, and it is asked here too.
#
# AND THE CENSUS COUNTED THE WRONG THING.  Looking through an unlined aperture
# you mostly see the body's OWN INNER SURFACE -- still object `T1_body`, so a
# census keyed on object NAMES scores it as sheet metal, which is what it says
# when you are looking at the outside of the bus.  Back-facing hits are
# separated by the face normal instead: dot(normal, ray) > 0 is a surface whose
# outside points away from the camera, i.e. the inside of the shell.
def _arch_ring(xa):
    """The aperture rim in WORLD space at axle xa, on the near (+y) flank."""
    import t1_shell as S
    zc = S.arch_z(xa)
    if xa == T.X_AXLE_R:
        ring = S.rear_arch_outline(xa)[:-2]           # drop the FLOOR points
    else:
        ring = [(S.ARCH_R * math.cos(math.pi * i / 64),
                 S.ARCH_R * math.sin(math.pi * i / 64)) for i in range(65)]
    out = []
    for dx, dz in ring:
        x = xa + dx
        z_auth = zc + dz
        out.append(Vector((x, T.flank_y(x, z_auth),
                           z_auth - T.rake_drop(x))))
    return out


def _px_of(P):
    from bpy_extras.object_utils import world_to_camera_view
    u = world_to_camera_view(sc, cam, P)
    return u.x * RX, (1.0 - u.y) * RY


def arch_census(view, xa, tag, pad=10, want=64):
    """Census + PAINTED map of one arch aperture through one named view."""
    global RX, RY
    V = ST.views()[view]
    RX, RY = (1600, 1100) if V.get("ortho") else (1600, 1067)
    sc.render.resolution_x, sc.render.resolution_y = RX, RY
    ST.aim(cam, V["loc"], V["tgt"], V.get("lens"), V.get("ortho"),
           V.get("focus"), V.get("fstop"))
    bpy.context.view_layer.update()
    pts = [_px_of(P) for P in _arch_ring(xa)]
    x0 = max(0, int(min(a for a, _ in pts)) - pad)
    x1 = min(RX - 1, int(max(a for a, _ in pts)) + pad)
    y0 = max(0, int(min(b for _, b in pts)) - pad)
    y1 = min(RY - 1, int(max(b for _, b in pts)) + pad)
    sx = max(1, (x1 - x0) // want)
    sy = max(1, (y1 - y0) // want)
    tal, inner, rows = Counter(), Counter(), []
    for py in range(y0, y1 + 1, sy):
        line = []
        for px in range(x0, x1 + 1, sx):
            o, L, N, D = ray(px, py)
            if o is None:
                line.append(".")
                continue
            back = N is not None and N.dot(D) > 0.0
            tal[o] += 1
            if o in INTERIOR:
                line.append("#")
            elif back and "body" in o:
                inner[o] += 1
                line.append("X")                       # the shell, from inside
            elif o.startswith("wheelhouse"):
                line.append("L")
            elif any(k in o for k in ("tyre", "rim", "cap")):
                line.append("o")
            elif "body" in o:
                line.append("=")
            else:
                line.append("?")
        rows.append("  %4d %s" % (py, "".join(line)))
    n_int = sum(c for n, c in tal.items() if n in INTERIOR)
    n_in = sum(inner.values())
    print("\n  --- %s: the %s arch through '%s', window DERIVED from the "
          "aperture  px[%d,%d] x [%d,%d] ---" % (tag, tag, view, x0, x1, y0, y1))
    print("      ( . miss  = body outside  X body INSIDE  o wheel  L liner  "
          "# interior  ? other )")
    for r in rows:
        print(r)
    print("      interior-object rays %d   back-facing body rays %d" % (n_int, n_in))
    report(tal)
    return tal, n_int, n_in


ARCH_ARMS = [("side", T.X_AXLE_R, "REAR"), ("side", T.X_AXLE_F, "FRONT"),
             ("hero34f", T.X_AXLE_R, "REAR")]
_arm = []
for _v, _xa, _tg in ARCH_ARMS:
    _arm.append((("%s/%s" % (_tg, _v)),) + arch_census(_v, _xa, _tg))
_leak = [(k, i, b) for k, _t, i, b in _arm if i or b]

_wh = [n for n in list(front) + list(rear) if n.startswith("wheelhouse")]
# rev 59 -- C6 WAS A TAUTOLOGY AND IS RETIRED AS ONE.  It read
#     "PASS" if _wh else "FAIL"
# i.e. it passed the moment ANY liner object appeared in either census, at ANY
# size.  It reported PASS for four revisions while the REAR liner was a 0.747 m
# circle inside a 0.920 m aperture and the body interior showed through the
# crescent at both ends of it.  A guard that cannot fail is not a guard
# (CLAUDE.md rule 3), and this one could not: the liners are built
# unconditionally by t1_detail.wheel_houses().
#
# It is SPLIT.  The existence half is kept but demoted to a PRECONDITION -- it
# is a statement about the build, not a result -- and C6 now asserts the thing
# the liner is FOR: that no interior object is visible through either arch.
# WATCHED FAILING under T1_WHCIRC=1, which restores the circular rear liner.
print("\n  precondition: liner objects seen in the two censuses: %s"
      % (sorted(set(_wh)) or "NONE -- C6 below cannot mean anything"))
ok6 = bool(_wh) and fi == 0 and ri == 0 and not _leak
print("  [%s] C6 nothing behind the skin is visible through any arch aperture "
      "-- hero34f name census front %d / rear %d, derived windows %s"
      % ("PASS" if ok6 else "FAIL", fi, ri,
         "clean" if not _leak else _leak))
if not ok6 and _wh:
    for tag, cen in (("FRONT", front), ("REAR", rear)):
        seen = {n: c for n, c in cen.items() if n in INTERIOR}
        if seen:
            print("      through the %s arch (hero34f): %s" % (tag, seen))
print("      pre-repair: 308 interior rays through the front arch, 0 liner objects")
print("=" * 78)
