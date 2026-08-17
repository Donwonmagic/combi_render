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
    o = cam.matrix_world.translation
    d = (cam.matrix_world.to_3x3() @ p).normalized()
    hit, loc, nor, idx, obj, mat = sc.ray_cast(dg, o, d)
    return (obj.name if hit else None), (loc if hit else None)

# ---- controls
ctl = [("C1 wheel centre",     (747, 843), "WHEEL"),
       ("C2 red flank",        (700, 640), "body"),
       ("C3 empty background", (120, 120), None)]
print()
for nm, (px, py), want in ctl:
    o, L = ray(px, py)
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
        o, L = ray(px, py)
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
        o, L = ray(px, py)
        if o: front[o] += 1
report(front)

print("\n  --- CONTROL: the REAR arch, same treatment (px 980-1120 x 690-790) ---")
rear = Counter()
for py in range(690, 792, 2):
    for px in range(980, 1122, 2):
        o, L = ray(px, py)
        if o: rear[o] += 1
report(rear)

ok5 = any("tyre" in n or "rim" in n for n in rear)
print("\n  [%s] C5 the rear-arch window actually lands on the rear wheel"
      % ("PASS" if ok5 else "FAIL"))

INTERIOR = {"cab_floor", "seat_base", "seat_back", "dash", "gal_floor"}
fi = sum(c for n, c in front.items() if n in INTERIOR)
ri = sum(c for n, c in rear.items() if n in INTERIOR)
print("\n  interior-object rays through FRONT arch: %d" % fi)
print("  interior-object rays through REAR  arch: %d" % ri)
# ON ARRIVAL IN REV 38 there was NO arch liner anywhere in the build (grep: no
# liner, inner_wing, wheelwell, wheel_well, splash) and this line said so.  That
# sentence is now FALSE and is REPLACED rather than left standing -- a probe
# that keeps asserting a fact its own subject has moved past is exactly the
# defect this revision found in probe_dust_scope's mesh-count literal.
_wh = [n for n in list(front) + list(rear) if n.startswith("wheelhouse")]
print("\n  [%s] C6 an arch liner exists and is what the arch rays now land on: %s"
      % ("PASS" if _wh else "FAIL", sorted(set(_wh))))
print("      pre-repair: 308 interior rays through the front arch, 0 liner objects")
print("=" * 78)
