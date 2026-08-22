"""
probe_rev54_edge.py -- rev 54, brief sec.3 item 2.

WHY THE COUNTER FASCIA'S BOTTOM FOLD PRODUCES NO EDGE SIGNAL.

Arm A asks the MESH (no render): shading flags, material, wear weight, and the
dihedral angle of every edge along the fascia's bottom fold.  Arm B (separate
script) renders the EDGE value itself as an emission AOV.

Nothing here is transcribed: every number is measured off the mesh built in
this process.
"""
import bpy, bmesh, os, sys, math

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from mathutils import Vector

src = open(os.path.join(ROOT, "build.py")).read().split('if os.environ.get("T1_SAVE")')[0]
exec(compile(src, "build.py", "exec"))

P = print
def hdr(t): P("\n=== %s ===" % t)

import t1_shell as SH
import t1_mats as MT

hdr("ARM A -- ASK THE MESH")

P("Bevel radius actually used : %.6f m (GAPW/2 = %.6f)"
  % (float(os.environ.get("T1_EDGERAD", 0))/1000.0 if os.environ.get("T1_EDGERAD")
     else SH.GAPW/2.0, SH.GAPW/2.0))
P("W_EDGE_90 %.5f   window LO %.5f  HI %.5f" % (MT.W_EDGE_90, MT.W_EDGE_LO, MT.W_EDGE_HI))
P("W_CHIP_CUT %.3f" % MT.W_CHIP_CUT)

# ---- which objects, and how are they shaded ----------------------------
NAMES = ["counter", "counter_nosing", "counter_top", "T1_body",
         "gutter", "gutter.001", "lid_main"]
P("\n%-18s %7s %7s %7s  %-14s %s" %
  ("object", "polys", "smooth", "flat", "material", "shade"))
for nm in NAMES:
    ob = bpy.data.objects.get(nm)
    if not ob or ob.type != 'MESH':
        P("%-18s  (absent)" % nm); continue
    ps = ob.data.polygons
    ns = sum(1 for p in ps if p.use_smooth)
    mat = ob.data.materials[0].name if ob.data.materials else "(none)"
    P("%-18s %7d %7d %7d  %-14s %s"
      % (nm, len(ps), ns, len(ps)-ns, mat,
         "SMOOTH" if ns == len(ps) else ("FLAT" if ns == 0 else "MIXED")))

# ---- does the material carry the WEATHER group, and at what wear? -------
hdr("THE CHIP GATE'S PER-MATERIAL WEAR WEIGHT")
P("(the gate is  wear = (pw*cm*clm > %.2f) * IN['wear'] -- a zero here would\n"
  " starve the gate no matter what EDGE does)" % MT.W_CHIP_CUT)
for nm in NAMES:
    ob = bpy.data.objects.get(nm)
    if not ob or ob.type != 'MESH' or not ob.data.materials:
        continue
    m = ob.data.materials[0]
    if not m.use_nodes:
        P("%-18s %-14s  (no nodes)" % (nm, m.name)); continue
    grp = [n for n in m.node_tree.nodes
           if n.type == 'GROUP' and n.node_tree and n.node_tree.name == "WEATHER"]
    if not grp:
        P("%-18s %-14s  NO WEATHER GROUP" % (nm, m.name)); continue
    g = grp[0]
    w = g.inputs["Wear"].default_value if "Wear" in g.inputs else None
    lk = [l for l in m.node_tree.links if l.to_node == g and l.to_socket.name == "Wear"]
    P("%-18s %-14s  Wear = %s%s"
      % (nm, m.name, ("%.4f" % w) if w is not None else "?",
         "  (DRIVEN by a link)" if lk else ""))

# ---- the fold itself.  Ask the geometry which edge is the bottom fold ---
# rule 35: do NOT name the fold by a pose.  A fascia's bottom fold is the
# sharp edge lowest on the OUTWARD-facing side, found by asking every edge.
hdr("THE FASCIA'S BOTTOM FOLD -- MEASURED, NOT ASSUMED")

def fold_report(name, want=None):
    ob = bpy.data.objects.get(name)
    if not ob or ob.type != 'MESH':
        P("%s absent" % name); return
    bm = bmesh.new(); bm.from_mesh(ob.data)
    bm.transform(ob.matrix_world)
    bm.normal_update()
    zs = [v.co.z for v in bm.verts]
    ys = [v.co.y for v in bm.verts]
    P("\n%s: %d verts %d edges %d faces   z %.4f..%.4f  y %.4f..%.4f"
      % (name, len(bm.verts), len(bm.edges), len(bm.faces),
         min(zs), max(zs), min(ys), max(ys)))
    P("  boundary edges: %d" % sum(1 for e in bm.edges if len(e.link_faces) != 2))
    # dihedral histogram
    import collections
    hist = collections.Counter()
    sharp = []
    for e in bm.edges:
        if len(e.link_faces) != 2:
            continue
        a = math.degrees(e.calc_face_angle(0.0))
        hist[int(a // 10) * 10] += 1
        if a > 30.0:
            mid = (e.verts[0].co + e.verts[1].co) / 2.0
            sharp.append((a, mid, e))
    P("  dihedral histogram (deg, only 2-face edges):")
    for k in sorted(hist):
        P("      %3d-%3d : %5d" % (k, k + 9, hist[k]))
    if not sharp:
        P("  NO edge sharper than 30 deg -- there is no fold to detect."); bm.free(); return
    # the bottom fold: sharp edges on the outward (+y) half, lowest z
    outw = [s for s in sharp if s[1].y > 0.0]
    pool = outw or sharp
    zmin = min(s[1].co.z if hasattr(s[1], 'co') else s[1].z for s in pool)
    bot = [s for s in pool if (s[1].z - zmin) < 0.003]
    P("  sharp edges (>30 deg): %d total, %d on the +y (outward) half" % (len(sharp), len(outw)))
    P("  BOTTOM FOLD: %d edges within 3 mm of z=%.4f" % (len(bot), zmin))
    if bot:
        angs = [b[0] for b in bot]
        L = sum(b[2].calc_length() for b in bot)
        P("     dihedral %.2f..%.2f deg (mean %.2f), total length %.4f m"
          % (min(angs), max(angs), sum(angs)/len(angs), L))
        P("     y span %.4f..%.4f" % (min(b[1].y for b in bot), max(b[1].y for b in bot)))
        # how much material is there within one bevel radius, either side?
        R = SH.GAPW / 2.0
        P("     bevel radius %.4f m = %.2f mm" % (R, R * 1000))
    bm.free()

for nm in ("counter", "counter_top", "counter_nosing"):
    fold_report(nm)
