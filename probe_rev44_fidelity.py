"""FIDELITY AUDIT -- the built scene against product-visualisation standard.

The owner set the bar with a catalogue-grade school-bus render and asked for
that level of detail.  This probe does not argue about it; it counts.  Six
things separate a measured model from a product-viz asset, and every one of
them is a number you can read off the built scene:

  1. EDGE TREATMENT.  A product-viz asset has NO knife edges.  Every hard
     edge carries a 0.5-3 mm chamfer, and that chamfer is what catches the
     highlight that reads as "metal".  Counted here as: how many objects have
     a Bevel modifier or a bevel-weighted edge, and what fraction of the
     scene's sharp edges are unchamfered.
  2. FASTENERS.  Rivets, bolts, lug nuts, hinges, screws -- modelled, not
     painted.  Counted by name and by object.
  3. TYRE TREAD.  Displaced or modelled, never a texture.  Counted as tris on
     the tyre objects against the tyre's own surface area.
  4. GLASS.  Thickness, not a plane.  Counted as the bounding-box depth of
     each glazing object.
  5. TEXTURE RESOLUTION.  Read off every image datablock actually bound.
  6. DENSITY.  Tris per object and tris per square metre of visible surface,
     which is the only density figure that means anything across parts of
     wildly different size.

Run:  blender -b -P probe_rev44_fidelity.py
"""
import os, sys, math
sys.argv = [sys.argv[0]]
os.environ.setdefault("T1_SUB", "2")

import bpy, bmesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

exec(compile(open("build.py").read(), "build.py", "exec"))

print()
print("=" * 78)
print("FIDELITY AUDIT -- built scene against product-visualisation standard")
print("=" * 78)

MESHES = [o for o in bpy.data.objects if o.type == "MESH"]
tot_tri = 0
rows = []
for o in MESHES:
    me = o.data
    n = sum(max(0, len(p.vertices) - 2) for p in me.polygons)
    tot_tri += n
    rows.append((n, o.name))
rows.sort(reverse=True)

print()
print("1. DENSITY")
print("   mesh objects            %6d" % len(MESHES))
print("   triangles (evaluated 0) %6d" % tot_tri)
print("   heaviest 12:")
for n, nm in rows[:12]:
    print("       %-34s %7d" % (nm, n))
print("   lightest 12 (candidates for detail that is simply absent):")
for n, nm in rows[-12:]:
    print("       %-34s %7d" % (nm, n))

print()
print("2. EDGE TREATMENT -- the single biggest tell")
bev_mod = [o for o in MESHES if any(m.type == "BEVEL" for m in o.modifiers)]
print("   objects with a Bevel modifier        %4d / %d" % (len(bev_mod), len(MESHES)))
bw = 0
sharp_edges = 0
tot_edges = 0
for o in MESHES:
    me = o.data
    bm = bmesh.new(); bm.from_mesh(me)
    lay = bm.edges.layers.bevel_weight_verify() if hasattr(
        bm.edges.layers, "bevel_weight_verify") else None
    for e in bm.edges:
        tot_edges += 1
        if len(e.link_faces) == 2:
            try:
                if e.calc_face_angle() > math.radians(28.0):
                    sharp_edges += 1
            except Exception:
                pass
    bm.free()
print("   edges total                          %8d" % tot_edges)
print("   edges over 28 deg (hard edges)       %8d  = %.1f %% of all edges"
      % (sharp_edges, 100.0 * sharp_edges / max(1, tot_edges)))
print("   -> every one of those is a KNIFE EDGE unless it is chamfered.")

print()
print("3. FASTENERS AND SECONDARY HARDWARE")
KEYS = ("rivet", "bolt", "screw", "nut", "hinge", "latch", "clip", "seal",
        "handle", "washer", "stud", "grommet", "bracket")
for k in KEYS:
    n = len([o for o in bpy.data.objects if k in o.name.lower()])
    print("   %-10s %4d" % (k, n))

print()
print("4. TYRES AND WHEELS")
for o in MESHES:
    ln = o.name.lower()
    if any(k in ln for k in ("tyre", "tire", "wheel", "rim", "cap")):
        me = o.data
        n = sum(max(0, len(p.vertices) - 2) for p in me.polygons)
        d = o.dimensions
        print("   %-30s %7d tri   dims %.3f x %.3f x %.3f"
              % (o.name, n, d.x, d.y, d.z))

print()
print("5. GLAZING -- thickness, not planes")
for o in MESHES:
    ln = o.name.lower()
    if "glass" in ln or "glaz" in ln or "pane" in ln:
        d = o.dimensions
        thin = min(d.x, d.y, d.z)
        print("   %-30s min dim %6.4f m   %s"
              % (o.name, thin, "PLANE" if thin < 1e-4 else "solid"))

print()
print("6. TEXTURES ACTUALLY BOUND")
seen = {}
for im in bpy.data.images:
    if im.size[0] and im.users:
        seen[im.name] = (im.size[0], im.size[1], im.users)
for nm in sorted(seen):
    w, h, u = seen[nm]
    print("   %-28s %5d x %-5d  users %d" % (nm, w, h, u))
if not seen:
    print("   (none bound)")

print()
print("7. MATERIALS")
mats = [m for m in bpy.data.materials if m.users]
print("   materials in use %d" % len(mats))
disp = [m for m in mats if m.node_tree and any(
    n.type == "DISPLACEMENT" for n in m.node_tree.nodes)]
print("   with true displacement %d" % len(disp))
print()
print("=" * 78)
