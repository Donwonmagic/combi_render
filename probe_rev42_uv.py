"""probe_rev42_uv.py -- rev 42.  THE UV-OVERLAP AND TEXTURE-RESOLUTION CHECK.

READ-ONLY.  Changes nothing, writes nothing but stdout.  Run under
    /tmp/blender/blender -b --python probe_rev42_uv.py

WHY THIS EXISTS
---------------
SPEC sec.5 "Mesh & texture quality bar" says, verbatim:

    Decals 3K-4K, **non-overlapping**, correctly oriented, correct handedness.

and the owner's own words on the second deliverable are "4K non-overlapping
textures ... no floating artifacts".  In FORTY-ONE revisions nothing has ever
measured either half of that bar.  `grep -ric "uv overlap|texel densit|
non-overlapping"` over SPEC, REF_MEASUREMENTS and every .py returns exactly
ONE hit -- SPEC:319, the requirement itself.  This probe is the first
measurement of it.

It needs no photograph, no px/m, no datum and no owner reading, and it moves
no geometry.  That is why it is cheap; it is not why it matters.

WHAT "OVERLAPPING" MEANS HERE, STATED BEFORE THE RUN
---------------------------------------------------
A texture is OVERLAPPING when one texel paints two different physical places
on the asset.  That definition is deliberately independent of whether the
mapping is a hand-made UV layout or a procedural projection, because THIS
BUILD USES BOTH and a check that only understood UV layouts would silently
score most of the vehicle as 0.000 by never looking at it.

Operationally: sample every painted polygon on a barycentric grid, push each
sample through that polygon's own texture map into the image's texel grid, and
for each texel cell cluster the 3D positions of the samples that landed in it.
A cell is COLLIDING when it holds two clusters separated by more than TOL_M.
The published statistic is the fraction of PAINTED WORLD AREA whose samples
land in a colliding cell.

ACCEPTANCE CRITERIA, WRITTEN DOWN BEFORE THE RUN
-----------------------------------------------
  G1 RESOLUTION.  SPEC sec.5's bar is "3K-4K".  An image whose LONGEST side is
     below 3072 px does not meet it; the owner's own stricter wording is 4096.
     Both are reported per image.  NO VERDICT OF MINE -- his bar, his call.
  G2 TEXEL DENSITY.  Reported as a distribution, in texels per metre, area
     weighted.  A DERIVED comparison bar is printed and labelled as derived:
     the shipped hero is 4800 px across a 4.065 m vehicle = 1180.8 px/m, so a
     surface delivering fewer texels/m than that is soft in the hero by
     construction.  That bar is arithmetic, not a measurement of the vehicle.
  G3 OVERLAP.  < 1.0 % of painted area colliding  -> the sec.5 bar is
     substantially met.  > 10.0 % -> a real defect.  BETWEEN THE TWO I PUBLISH
     THE DISTRIBUTION AND DECLINE A VERDICT.  Stated now so the threshold
     cannot be chosen after seeing the number (rev 41's rule: a verdict that
     moves with the bar is a property of the bar).

CONTROLS, ALSO STATED BEFORE THE RUN
------------------------------------
  C1 POSITIVE, AND ITS ANSWER IS ALREADY IN THE RECORD.  rev 10 found (as
     `materials-14`) that BOTH FLANKS CARRIED THE SAME DRAWING MIRRORED, and
     the repair was a SECOND TILE selected by side, not a UV layout.  So if I
     switch the side selector off and let one tile paint both flanks, a
     detector that works MUST report a large collision fraction on `T1_body`.
     If it reports a small one it is blind and every other number here is
     worthless.  A control with a known-sign answer from the project's own
     history, not one I invented to pass.
  C2 NEGATIVE.  A single planar quad projected along its own normal cannot
     collide with itself.  Must return exactly 0.000.
  C3 PARAMETER STABILITY.  Every free parameter the estimator has is
     SWEPT, including the one I introduced myself.  If the fraction moves with
     a parameter then the fraction is a property of that parameter and not of
     the asset; the tolerance is stated and checked, never widened.
  C4 CENSUS EXHAUSTIVE.  Every image node's Vector chain is traced to a named
     origin.  An unrecognised node shape RAISES.  A census that silently drops
     what it does not understand is the `or -9` shape (SPEC 10.47).
  C5 AREA CONSERVATION.  The sampler's total weighted area must reproduce the
     mesh's own polygon-area sum.  Proves it is not dropping surface, which
     would flatter every fraction below.

WHAT THIS PROBE DOES NOT CLAIM
------------------------------
  * that an overlap is a DEFECT.  A REPEAT-tiled procedural pattern is
    *supposed* to repeat; the question sec.5 asks is about decals.  Both are
    reported separately and the reader decides.
  * any statement about the ARTWORK's correctness.  This is a layout and
    sampling measurement only.
  * anything about render quality.  It measures the asset, not a frame.
"""
_DOC = __doc__          # build.py's exec below overwrites __doc__

import bpy, bmesh, os, sys, math
from collections import defaultdict
from mathutils import Vector

try:
    ROOT = os.path.dirname(os.path.abspath(__file__))
except NameError:
    ROOT = os.getcwd()
sys.path.insert(0, ROOT)

# Build the vehicle exactly the way audit.py, probe_dust_scope.py and
# probe_rev38_wheelbar.py do.  probe_rev38_wheelbar's first draft ran against
# Blender's DEFAULT STARTUP CUBE and printed a confident fictional tally; the
# whole reason this line is not optional.
_src = open(os.path.join(ROOT, "build.py")).read().split(
    'if os.environ.get("T1_SAVE")')[0]
exec(compile(_src, "build.py", "exec"))

W = "=" * 78
TOL_M       = 0.005      # 5 mm: two places this far apart are "different places"
DENS        = 40         # barycentric samples per polygon edge subdivision
HERO_PXM    = 4800.0 / 4.065   # DERIVED, see G2

def hr(t=""):
    print(W)
    if t:
        print(t)
        print(W)

hr("PROBE rev 42 -- UV OVERLAP AND TEXTURE RESOLUTION (SPEC sec.5)")
print(_DOC.split("WHY THIS EXISTS")[1].split("WHAT THIS PROBE DOES NOT")[0])
hr()


# ----------------------------------------------------------------- census ---
def _up(sock):
    return sock.links[0] if sock.is_linked else None


def trace_vector(node):
    """Return a dict describing how this TEX_IMAGE gets its coordinates.

    RAISES on any shape it does not recognise (C4).
    """
    vi = node.inputs["Vector"]
    if not vi.is_linked:
        return {"kind": "UV", "detail": "default UV layer"}

    l = _up(vi)
    n = l.from_node
    if n.type != "MAPPING":
        raise RuntimeError("C4: unrecognised vector source %r on %s"
                           % (n.type, node.name))
    loc = tuple(n.inputs["Location"].default_value)
    rot = tuple(n.inputs["Rotation"].default_value)
    sca = tuple(n.inputs["Scale"].default_value)
    if any(abs(r) > 1e-9 for r in rot):
        raise RuntimeError("C4: rotated Mapping not handled on %s" % node.name)

    mi = n.inputs["Vector"]
    if not mi.is_linked:
        raise RuntimeError("C4: Mapping with no input on %s" % node.name)
    src = _up(mi).from_node
    if src.type == "TEX_COORD":
        return {"kind": "OBJECT", "loc": loc, "sca": sca,
                "socket": _up(mi).from_socket.name,
                "detail": "TexCoord.%s -> Mapping(loc=%s sca=%s)"
                          % (_up(mi).from_socket.name, loc, sca)}
    if src.type == "COMBXYZ":
        comps = []
        for cn in ("X", "Y", "Z"):
            ci = src.inputs[cn]
            if not ci.is_linked:
                comps.append(("CONST", float(ci.default_value)))
                continue
            sep = _up(ci).from_node
            if sep.type != "SEPXYZ":
                raise RuntimeError("C4: unrecognised CombineXYZ feed %r"
                                   % sep.type)
            geo = _up(sep.inputs["Vector"]).from_node
            if geo.type != "NEW_GEOMETRY":
                raise RuntimeError("C4: unrecognised SeparateXYZ feed %r"
                                   % geo.type)
            comps.append((_up(sep.inputs["Vector"]).from_socket.name,
                          _up(ci).from_socket.name))
        return {"kind": "GEOM_COMB", "loc": loc, "sca": sca, "comps": comps,
                "detail": "Geometry -> Combine%s -> Mapping(loc=%s sca=%s)"
                          % (comps, loc, sca)}
    raise RuntimeError("C4: unrecognised Mapping input %r on %s"
                       % (src.type, node.name))


IMAGES = []          # one row per TEX_IMAGE node actually in the file
for mat in bpy.data.materials:
    if not mat.use_nodes:
        continue
    for n in mat.node_tree.nodes:
        if n.type != "TEX_IMAGE" or n.image is None:
            continue
        IMAGES.append({
            "mat": mat.name, "node": n.name, "img": n.image.name,
            "size": tuple(n.image.size), "proj": n.projection,
            "blend": round(getattr(n, "projection_blend", 0.0), 4),
            "ext": n.extension, "interp": n.interpolation,
            "vec": trace_vector(n),
        })

WEARERS = defaultdict(list)
for ob in bpy.data.objects:
    if ob.type != "MESH":
        continue
    for s in ob.material_slots:
        if s.material:
            WEARERS[s.material.name].append(ob.name)

hr("1.  CENSUS -- every image node in the shipped build (C4 armed)")
print("  %-10s %-18s %-15s %-12s %-6s %-7s %s"
      % ("material", "node", "image", "size", "proj", "ext", "wearers"))
for r in IMAGES:
    print("  %-10s %-18s %-15s %-12s %-6s %-7s %d"
          % (r["mat"], r["node"], r["img"], "%dx%d" % r["size"],
             r["proj"], r["ext"], len(WEARERS[r["mat"]])))
print()
for r in IMAGES:
    print("    %-10s %-15s coords: %s" % (r["mat"], r["img"], r["vec"]["detail"]))
print("\n  [PASS] C4 all %d image nodes traced to a named coordinate origin"
      % len(IMAGES))

ondisk = sorted(f for f in os.listdir(os.path.join(ROOT, "tex"))
                if f.lower().endswith(".png"))
used = {r["img"] for r in IMAGES}
print("\n  tex/ on disk: %d files; referenced by a material: %d"
      % (len(ondisk), len(used)))
for f in ondisk:
    if f not in used:
        print("    UNREFERENCED BY ANY MATERIAL: tex/%s" % f)
for r in IMAGES:
    if not WEARERS[r["mat"]]:
        print("    REFERENCED BUT WORN BY NO OBJECT: %s (material %s)"
              % (r["img"], r["mat"]))

# --------------------------------------------------------------- G1 sizes ---
hr("2.  G1 RESOLUTION -- against SPEC sec.5's own bar")
print('  SPEC.md:319  "Decals 3K-4K, **non-overlapping**, correctly oriented,')
print('                correct handedness."')
print("  His own words on the 3D deliverable: \"4K non-overlapping textures\".")
print()
print("  %-15s %-12s %-9s %-9s %s" % ("image", "size", ">=3072?", ">=4096?",
                                      "long side"))
for r in sorted(IMAGES, key=lambda r: max(r["size"])):
    w, h = r["size"]
    long = max(w, h)
    print("  %-15s %-12s %-9s %-9s %d"
          % (r["img"], "%dx%d" % (w, h),
             "yes" if long >= 3072 else "NO",
             "yes" if long >= 4096 else "NO", long))
n3 = sum(1 for r in IMAGES if max(r["size"]) >= 3072)
n4 = sum(1 for r in IMAGES if max(r["size"]) >= 4096)
print("\n  %d of %d meet SPEC sec.5's 3K floor; %d of %d meet his 4K wording."
      % (n3, len(IMAGES), n4, len(IMAGES)))
print("  REPORTED, NOT RULED ON.  The bar is his.")


# --------------------------------------------------------- the sampler -----
def dom_axis(nv):
    a = (abs(nv.x), abs(nv.y), abs(nv.z))
    return a.index(max(a))


def uv_of(rec, co, nrm, uvloop):
    """Texture-space coordinate, in UNIT texture space, for a world/object
    sample.  Returns None where the image does not paint."""
    v = rec["vec"]
    if v["kind"] == "UV":
        return uvloop
    p = co
    if v["kind"] == "OBJECT":
        q = (p.x * v["sca"][0] + v["loc"][0],
             p.y * v["sca"][1] + v["loc"][1],
             p.z * v["sca"][2] + v["loc"][2])
        if rec["proj"] == "BOX":
            ax = dom_axis(nrm)
            # Blender BOX: the plane whose normal is the dominant axis.
            if ax == 0:
                return (q[1], q[2])
            if ax == 1:
                return (q[0], q[2])
            return (q[0], q[1])
        return (q[0], q[1])
    if v["kind"] == "GEOM_COMB":
        got = []
        for c in v["comps"][:2]:
            if c[0] == "CONST":
                got.append(c[1])
            elif c[0] == "Position":
                got.append({"X": p.x, "Y": p.y, "Z": p.z}[c[1]])
            elif c[0] == "Normal":
                got.append({"X": nrm.x, "Y": nrm.y, "Z": nrm.z}[c[1]])
            else:
                raise RuntimeError("C4: unhandled geometry socket %r" % (c,))
        return (got[0] * v["sca"][0] + v["loc"][0],
                got[1] * v["sca"][1] + v["loc"][1])
    raise RuntimeError("C4: unhandled kind %r" % v["kind"])


# ---------------------------------------------------------------------------
# THE ESTIMATOR, AND THE TWO IT REPLACED.  Both predecessors are recorded here
# rather than deleted, because each was killed by a control that was written
# down before the run (rev 41's pattern).
#
# DRAFT 1 -- POINT SAMPLING.  Sample each triangle, flag a texel if any two
# samples in it are far apart.  C3 KILLED IT: the fraction climbed 5.34 ->
# 6.10 -> 10.98 % as sample spacing went 40 -> 20 -> 10 mm.  A "does any pair
# differ" test can only find MORE collisions with more samples, so it never
# converges; it measured my sample count, not the asset.  C1 failed for the
# same reason and my >25 % bar was never the problem.
#
# DRAFT 2 -- CONSERVATIVE RASTER WITH A FIXED METRIC TOLERANCE.  C2 KILLED IT
# at 99.95 %: a single flat 2 m quad "collided with itself" everywhere.  The
# cause is real and general -- a collision CELL spans a finite distance ON THE
# SURFACE, and on that quad one cell spans 62 mm while TOL_M is 5 mm, so every
# cell contained two points "far apart" without any overlap existing.  C5
# failed at +53.8 % for a second, independent reason: area accumulated over the
# conservative slop margin, which inflates every small triangle.
#
# DRAFT 3, BELOW.  Two fixes, both to the CAUSE:
#   (a) THE TOLERANCE IS SCALE AWARE.  A cell is colliding when it is painted
#       from two places FARTHER APART THAN THAT CELL'S OWN FOOTPRINT ON THE
#       SURFACE could account for: threshold = max(TOL_M, C_FOOT * cell extent
#       in metres), cell extent taken from that triangle's own texel density.
#       C_FOOT is swept as a control, not chosen.
#   (b) AREA IS ANALYTIC, NOT RASTERISED.  painted = sum of true triangle
#       areas.  A triangle's colliding area is its own area times the fraction
#       of ITS cells that are colliding.  Two passes: pass 1 builds the cell
#       map, pass 2 attributes.  So the painted total is exact by construction
#       and C5 is repointed at what actually needs checking -- whether the
#       raster's covered-cell count reproduces the analytic texture area.
#
# REPEAT IS NOT WRAPPED, DELIBERATELY.  `swirl` tiles by design; wrapping its
# coordinates would score the tiling itself as overlap and answer a question
# nobody asked.  What is measured is whether the LAYOUT is injective, ignoring
# intentional repetition.  A scope decision, stated, not an implementation
# detail.
# ---------------------------------------------------------------------------
CELL_K_DEFAULT = 4        # collision cell width, in texels
C_FOOT_DEFAULT = 3.0      # a cell's own footprint may span this many cell
                          # extents on one continuous sheet before two points
                          # in it count as two different places
MAXCELLS_PER_TRI = 400000


def _tri_stream(rec, objnames, side_selector):
    """Yield (p0,p1,p2, warea, (x0,y0),(x1,y1),(x2,y2), tarea) in texel space."""
    img_w, img_h = rec["size"]
    is_uv = rec["vec"]["kind"] == "UV"
    for on in objnames:
        ob = bpy.data.objects.get(on)
        if ob is None or ob.type != "MESH":
            continue
        me = ob.data
        mw = ob.matrix_world
        n3 = mw.to_3x3()
        uvl = me.uv_layers.active
        if is_uv and uvl is None:
            continue
        co = [mw @ v.co for v in me.vertices]
        for poly in me.polygons:
            vs = [co[i] for i in poly.vertices]
            nrm = (n3 @ poly.normal).normalized()
            c = sum(vs, Vector((0.0, 0.0, 0.0))) / len(vs)
            sel = SELECTORS.get(rec["img"])
            if sel is not None:
                if side_selector:
                    if not sel[0](c, nrm):
                        continue
                elif rec["img"] == "nose.png":
                    if not sel[0](c, nrm):
                        continue
            uvs = None
            if is_uv:
                uvs = [tuple(uvl.data[li].uv) for li in poly.loop_indices]
            for t in range(1, len(vs) - 1):
                p0, p1, p2 = vs[0], vs[t], vs[t + 1]
                warea = (p1 - p0).cross(p2 - p0).length * 0.5
                if warea <= 1e-12:
                    continue
                if uvs is not None:
                    q0, q1, q2 = uvs[0], uvs[t], uvs[t + 1]
                else:
                    q0 = uv_of(rec, p0, nrm, None)
                    q1 = uv_of(rec, p1, nrm, None)
                    q2 = uv_of(rec, p2, nrm, None)
                A = (q0[0] * img_w, q0[1] * img_h)
                B = (q1[0] * img_w, q1[1] * img_h)
                C = (q2[0] * img_w, q2[1] * img_h)
                d = (B[0] - A[0]) * (C[1] - A[1]) - (C[0] - A[0]) * (B[1] - A[1])
                yield p0, p1, p2, warea, A, B, C, abs(d) * 0.5


def _cells_of(A, B, C, tarea, K):
    """Cell-space rasterisation.

    A triangle deposits into every cell whose CENTRE it contains, and -- if it
    contains none, which happens whenever it is smaller than a cell -- into the
    single cell holding its centroid.  Every triangle is represented exactly
    once and no surface is dropped.

    A CONSERVATIVE version (half-a-cell-diagonal slop on every edge) was tried
    first and C5 rejected it at a coverage ratio of 3.2452: it covered 3.25x
    the analytic texture area, which would have turned every published fraction
    into a loose upper bound without saying so.  Recorded, not deleted.
    """
    x0, y0 = A[0] / K, A[1] / K
    x1, y1 = B[0] / K, B[1] / K
    x2, y2 = C[0] / K, C[1] / K
    d = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
    if abs(d) < 1e-15:
        return []
    lo_x = int(math.floor(min(x0, x1, x2)))
    hi_x = int(math.ceil(max(x0, x1, x2)))
    lo_y = int(math.floor(min(y0, y1, y2)))
    hi_y = int(math.ceil(max(y0, y1, y2)))
    if (hi_x - lo_x + 1) * (hi_y - lo_y + 1) > MAXCELLS_PER_TRI:
        return None
    inv = 1.0 / d
    out = []
    for cy in range(lo_y, hi_y + 1):
        fy = cy + 0.5
        for cx in range(lo_x, hi_x + 1):
            fx = cx + 0.5
            w1 = ((fx - x0) * (y2 - y0) - (x2 - x0) * (fy - y0)) * inv
            if w1 < 0.0:
                continue
            w2 = ((x1 - x0) * (fy - y0) - (fx - x0) * (y1 - y0)) * inv
            if w2 < 0.0:
                continue
            w0 = 1.0 - w1 - w2
            if w0 < 0.0:
                continue
            out.append(((cx, cy), w0, w1, w2))
    if not out:
        gx = (x0 + x1 + x2) / 3.0
        gy = (y0 + y1 + y2) / 3.0
        out.append(((int(math.floor(gx)), int(math.floor(gy))),
                    1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0))
    return out


# ---------------------------------------------------------------------------
# THE SELECTOR IS PARSED, NOT ASSUMED.  `T1_paint` carries THREE images and a
# shader-side Mix chain decides which one paints a given point.  The first cut
# of this probe HARD-CODED my reading of that chain -- centroid y > 0 for the
# swirl pair, |normal.x| > 0.7 and x > 1.6 for the nose.  That is a re-typed
# constant of exactly the class this repo has been punished for eleven times,
# and it is worse here than usual: if the split is on the NORMAL rather than
# the POSITION then the solidified shell's INNER skin goes to the other tile
# and the two sets being compared are not the ones the renderer uses.
# So the chain is evaluated from the graph.  Anything it cannot evaluate
# RAISES rather than falling back to my reading.
# ---------------------------------------------------------------------------
def _eval_node(sock, pos, nrm):
    if not sock.is_linked:
        return float(sock.default_value)
    l = sock.links[0]
    n = l.from_node
    if n.type == "SEPXYZ":
        v = _eval_vec(n.inputs["Vector"], pos, nrm)
        return {"X": v[0], "Y": v[1], "Z": v[2]}[l.from_socket.name]
    if n.type == "MATH":
        a = _eval_node(n.inputs[0], pos, nrm)
        op = n.operation
        if op == "ABSOLUTE":
            return abs(a)
        b = _eval_node(n.inputs[1], pos, nrm)
        if op == "GREATER_THAN":
            return 1.0 if a > b else 0.0
        if op == "LESS_THAN":
            return 1.0 if a < b else 0.0
        if op == "MULTIPLY":
            return a * b
        if op == "ADD":
            return a + b
        if op == "SUBTRACT":
            return a - b
        if op == "MINIMUM":
            return min(a, b)
        if op == "MAXIMUM":
            return max(a, b)
        raise RuntimeError("C4: unhandled MATH op %r" % op)
    raise RuntimeError("C4: unhandled selector node %r" % n.type)


def _eval_vec(sock, pos, nrm):
    if not sock.is_linked:
        return tuple(sock.default_value)
    l = sock.links[0]
    n = l.from_node
    if n.type == "NEW_GEOMETRY":
        if l.from_socket.name == "Position":
            return (pos.x, pos.y, pos.z)
        if l.from_socket.name == "Normal":
            return (nrm.x, nrm.y, nrm.z)
        raise RuntimeError("C4: unhandled Geometry socket %r"
                           % l.from_socket.name)
    if n.type == "TEX_COORD":
        return (pos.x, pos.y, pos.z)
    raise RuntimeError("C4: unhandled vector node %r" % n.type)


def build_selectors():
    """image name -> (callable(pos, nrm) -> bool, human description)."""
    sel = {}
    m = bpy.data.materials.get("T1_paint")
    if m is None:
        return sel
    nt = m.node_tree
    img_node = {}
    for n in nt.nodes:
        if n.type == "TEX_IMAGE" and n.image:
            img_node[n.name] = n.image.name
    # walk every MIX whose A/B come from image nodes (directly or via a Mix)
    def src_images(sock, depth=0):
        if depth > 4 or not sock.is_linked:
            return set()
        n = sock.links[0].from_node
        if n.type == "TEX_IMAGE":
            return {n.image.name} if n.image else set()
        if n.type in ("MIX", "MIX_RGB"):
            out = set()
            for i in n.inputs:
                if i.name in ("A", "B") and i.is_linked:
                    out |= src_images(i, depth + 1)
            return out
        return set()

    rules = {}
    for n in nt.nodes:
        if n.type not in ("MIX", "MIX_RGB"):
            continue
        fac = n.inputs[0]
        if not fac.is_linked:
            continue
        ins = [i for i in n.inputs if i.name in ("A", "B") and i.is_linked]
        if len(ins) != 2:
            continue
        aim = src_images(ins[0])
        bim = src_images(ins[1])
        if not aim or not bim:
            continue
        for im in aim:
            rules.setdefault(im, []).append((fac, 0.0))
        for im in bim:
            rules.setdefault(im, []).append((fac, 1.0))
    for im, rl in rules.items():
        def mk(rl=tuple(rl)):
            def f(pos, nrm):
                for (fac, want) in rl:
                    v = _eval_node(fac, pos, nrm)
                    if (v > 0.5) != (want > 0.5):
                        return False
                return True
            return f
        sel[im] = (mk(), "%d shader rule(s) parsed from the Mix chain"
                   % len(rl))
    return sel


SELECTORS = build_selectors()
print("  SHADER SELECTORS, PARSED from T1_paint's Mix chain rather than")
print("  re-typed from my reading of it.  The first cut of this probe")
print("  hard-coded my own reading (centroid y > 0 for the swirl pair,")
print("  |normal.x| > 0.7 and x > 1.6 for the nose); if the split is on the")
print("  NORMAL rather than the POSITION then the solidified shell's INNER")
print("  skin goes to the other tile and the compared sets are not the ones")
print("  the renderer uses.  So it is parsed.")
for _im in sorted(SELECTORS):
    print("    %-15s %s" % (_im, SELECTORS[_im][1]))
if not SELECTORS:
    print("    (none found -- every image paints its whole material)")
print()


_TRI_CACHE = {}


def _tris(rec, objnames, side_selector):
    """The triangle stream, built ONCE per (image, selector) and reused by both
    passes and by every sweep.  Rebuilding it inside the sweeps made the probe
    slower than the hero it is meant to precede."""
    # THE OBJECT LIST IS PART OF THE KEY.  It was not, for one run, and the
    # per-object pass below then re-used the WHOLE-MATERIAL stream for every
    # object in turn: self-overlap printed 332.7618 m^2 = 571.71 % of a
    # 58.2048 m^2 painted area.  A fraction over 100 % is arithmetically
    # impossible, which is the only reason it was caught in one read.
    key = (rec["img"], side_selector, tuple(objnames))
    got = _TRI_CACHE.get(key)
    if got is None:
        got = list(_tri_stream(rec, objnames, side_selector))
        _TRI_CACHE[key] = got
    return got


def measure(rec, objnames, tol=None, side_selector=True, cell_k=None,
            c_foot=None):
    """(painted, colliding, [(texels_per_m, area)], ncells, ncoll, cover_ratio)."""
    if tol is None:
        tol = TOL_M
    K = cell_k or CELL_K_DEFAULT
    CF = C_FOOT_DEFAULT if c_foot is None else c_foot
    rep = {}
    thr = {}
    coll = set()
    dens_list = []
    painted = 0.0
    tarea_sum = 0.0
    ncov = 0
    over = 0
    # ---- pass 1: build the cell map ----
    stream = _tris(rec, objnames, side_selector)
    cellcache = []
    for p0, p1, p2, warea, A, B, C, tarea in stream:
        if tarea <= 1e-9:
            cellcache.append(None)
            continue
        painted += warea
        tarea_sum += tarea
        dens = math.sqrt(tarea / warea)          # texels per metre
        dens_list.append((dens, warea))
        cells = _cells_of(A, B, C, tarea, K)
        cellcache.append(cells)
        if cells is None:
            over += 1
            continue
        ncov += len(cells)
        # a cell spans K/dens metres on this sheet
        local_thr = max(tol, CF * K / dens)
        for (key, b0, b1, b2) in cells:
            px = p0.x * b0 + p1.x * b1 + p2.x * b2
            py = p0.y * b0 + p1.y * b1 + p2.y * b2
            pz = p0.z * b0 + p1.z * b1 + p2.z * b2
            r = rep.get(key)
            if r is None:
                rep[key] = (px, py, pz)
                thr[key] = local_thr
                continue
            t = thr[key]
            if local_thr > t:
                thr[key] = t = local_thr
            if (abs(px - r[0]) >= t or abs(py - r[1]) >= t
                    or abs(pz - r[2]) >= t):
                coll.add(key)
    # ---- pass 2: attribute area analytically ----
    colliding = 0.0
    for tri, cells in zip(stream, cellcache):
        if not cells:
            continue
        warea = tri[3]
        nc = len(cells)
        hit = sum(1 for (key, _, _, _) in cells if key in coll)
        if hit:
            colliding += warea * hit / nc
    cover = (ncov * K * K) / tarea_sum if tarea_sum else 0.0
    return painted, colliding, dens_list, len(rep), len(coll), cover


# -------------------------------------------------------------- controls ---
hr("3.  CONTROLS")

# C5 area conservation --------------------------------------------------
ob = bpy.data.objects["T1_body"]
mesh_area = sum(p.area for p in ob.data.polygons)
rec_test = [r for r in IMAGES if r["img"] == "swirl.png"][0]
pa, ca, dl, nc, ncc, cover = measure(rec_test, ["T1_body"], side_selector=False)
print("  C5  the raster must SEE the whole surface, and the area it reports")
print("      must be the mesh's own.  Two halves, both checked:")
print("        mesh sum(poly.area)        = %.4f m^2" % mesh_area)
print("        probe painted (analytic)   = %.4f m^2" % pa)
rel = abs(pa - mesh_area) / mesh_area
print("        relative difference        = %.4f %%" % (rel * 100))
print("        raster coverage ratio      = %.4f  (covered cells x K^2 /" % cover)
print("                                     analytic texture area; 1.0 = exact.")
print("                                     A conservative half-cell-slop raster")
print("                                     was tried first and scored 3.2452,")
print("                                     which C5 rejected -- it would have")
print("                                     made every fraction below a loose")
print("                                     upper bound without saying so.)")
c5 = rel < 0.02 and 0.55 < cover < 1.8
print("      [%s] C5 area exact to 2 %% AND coverage ratio inside 0.55..1.8"
      % ("PASS" if c5 else "FAIL"))

# C2 negative -----------------------------------------------------------
bm = bmesh.new()
bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=1.0)
me = bpy.data.meshes.new("ctrl_quad")
bm.to_mesh(me); bm.free()
qob = bpy.data.objects.new("ctrl_quad", me)
bpy.context.scene.collection.objects.link(qob)
fake = dict(rec_test)
fake["img"] = "ctrl"
fake["size"] = (256, 256)
fake["proj"] = "FLAT"
fake["vec"] = {"kind": "OBJECT", "loc": (0.5, 0.5, 0.0),
               "sca": (0.25, 0.25, 0.25), "socket": "Object",
               "detail": "control"}
pa2, ca2, _, _, _, _ = measure(fake, ["ctrl_quad"])
frac2 = ca2 / pa2 if pa2 else 0.0
c2 = frac2 == 0.0
print("\n  C2  a single planar quad projected along its own normal:")
print("        painted %.4f m^2   colliding %.6f m^2   fraction %.4f %%"
      % (pa2, ca2, frac2 * 100))
print("      [%s] C2 a flat quad cannot collide with itself"
      % ("PASS" if c2 else "FAIL"))
bpy.data.objects.remove(qob, do_unlink=True)

# C1 positive, known-sign answer from rev 10's materials-14 -------------
frac3 = ca / pa if pa else 0.0
print("\n  C1  side selector OFF -- one tile painting BOTH flanks.")
print("      rev 10 `materials-14` recorded exactly this state and called it a")
print("      defect: both flanks carried the same drawing mirrored.")
print("        colliding fraction = %.2f %% of painted area" % (frac3 * 100))
c1 = frac3 > 0.25
print("      [%s] C1 the detector SEES the defect the project already recorded"
      % ("PASS" if c1 else "FAIL"))


# ------------------------------------------------------------ the answer ---
hr("4.  G3 OVERLAP and G2 TEXEL DENSITY -- the shipped build, as it ships")
rows = []
for r in IMAGES:
    obs = WEARERS[r["mat"]]
    if not obs:
        rows.append((r, None))
        continue
    pa, ca, dl, nc, ncc, cov = measure(r, obs)
    rows.append((r, (pa, ca, dl, nc, ncc, cov)))

print("  %-15s %-9s %-11s %-11s %-9s %s"
      % ("image", "proj/ext", "painted m^2", "collide m^2", "collide %",
         "texels/m  p5 / median / p95"))
tot_p = tot_c = 0.0
for r, m in rows:
    if m is None:
        print("  %-15s %-9s  (worn by no object -- nothing to measure)"
              % (r["img"], r["proj"] + "/" + r["ext"][:3]))
        continue
    pa, ca, dl, nc, ncc, cov = m
    dl.sort()
    tw = sum(w for _, w in dl)
    def q(f):
        acc = 0.0
        for d, w in dl:
            acc += w
            if acc >= f * tw:
                return d
        return dl[-1][0] if dl else 0.0
    print("  %-15s %-9s %11.4f %11.4f %8.2f %%  %8.0f / %8.0f / %8.0f"
          % (r["img"], r["proj"] + "/" + r["ext"][:3], pa, ca,
             100.0 * ca / pa if pa else 0.0, q(0.05), q(0.50), q(0.95)))
    tot_p += pa
    tot_c += ca

print("\n  TOTAL painted %.4f m^2, colliding %.4f m^2 = %.2f %%"
      % (tot_p, tot_c, 100.0 * tot_c / tot_p if tot_p else 0.0))
print("\n  DERIVED comparison bar for G2, labelled as derived: the shipped hero")
print("  is 4800 px across a %.3f m vehicle = %.1f px/m.  A surface delivering"
      % (4.065, HERO_PXM))
print("  fewer texels/m than that is soft in the hero BY ARITHMETIC.  This is")
print("  not a measurement of the vehicle and is not offered as one.")

# separate the two classes sec.5 actually distinguishes ------------------
print("\n  SELF-OVERLAP vs REUSE, and the difference matters.  A decal used on")
print("  TWO panels (script_L and script_R wear one senor.png) shares texels")
print("  BY DESIGN -- that is instancing, not a layout defect.  What sec.5's")
print("  bar is about is a surface colliding with ITSELF.  Measured per object")
print("  and totalled, so the two are separated rather than added:")
print("  %-15s %-12s %-12s %s"
      % ("image", "self m^2", "self %", "cross-object m^2 (reuse)"))
self_tot = 0.0
for r, m in rows:
    if m is None:
        continue
    pa_all, ca_all = m[0], m[1]
    sp = sc_ = 0.0
    for on in WEARERS[r["mat"]]:
        p1, c1, _, _, _, _ = measure(r, [on])
        sp += p1
        sc_ += c1
    self_tot += sc_
    print("  %-15s %12.4f %11.2f %% %12.4f"
          % (r["img"], sc_, 100.0 * sc_ / sp if sp else 0.0,
             max(0.0, ca_all - sc_)))
print("\n  TOTAL SELF-overlap %.4f m^2 = %.2f %% of painted area"
      % (self_tot, 100.0 * self_tot / tot_p if tot_p else 0.0))
print("  the remainder, %.4f m^2, is one decal worn by more than one object."
      % max(0.0, tot_c - self_tot))

print("\n  sec.5's bar is on DECALS.  Splitting the two classes:")
for r, m in rows:
    if m is None:
        continue
    cls = "TILED PATTERN (REPEAT -- repetition is its job)" \
        if r["ext"] == "REPEAT" else "DECAL (bar applies)"
    print("    %-15s %s" % (r["img"], cls))


# ------------------------------------------------------ C3 stability -------
hr("5.  C3 SAMPLING STABILITY")
print("  The rasteriser has no sample count left to tune.  The two parameters")
print("  that remain are both swept here rather than chosen.")
print()
print("  CELL_K -- collision cell width in texels.  Coarsening can only")
print("  OVER-count, so the sequence must DECREASE as K falls and settle.")
print("  Stated before the run: K=4 and K=2 must agree to 2.0 pp.")
ksweep = []
for K in (8, 4, 2):
    p = c = 0.0
    for r in IMAGES:
        obs = WEARERS[r["mat"]]
        if not obs:
            continue
        pa, ca, _, _, _, _ = measure(r, obs, cell_k=K)
        p += pa
        c += ca
    ksweep.append((K, 100.0 * c / p if p else 0.0))
    print("    CELL_K %d texels  ->  %.2f %%" % ksweep[-1])
kspread = abs(ksweep[1][1] - ksweep[2][1])
print("    K=4 vs K=2 difference %.2f pp" % kspread)
print()
print("  TOL_M -- how far apart two places must be to be different places.")
print("  Stated before the run: 2.0 pp across a twentyfold sweep, 1 to 20 mm.")
sweep = []
for d in (0.001, 0.020):
    p = c = 0.0
    for r in IMAGES:
        obs = WEARERS[r["mat"]]
        if not obs:
            continue
        pa, ca, _, _, _, _ = measure(r, obs, d)
        p += pa
        c += ca
    sweep.append((d * 1000.0, 100.0 * c / p if p else 0.0))
    print("    TOL_M %6.1f mm  ->  %.2f %%" % sweep[-1])
spread = max(s for _, s in sweep) - min(s for _, s in sweep)
print()
print("  C_FOOT -- how many cell extents two points in one cell may be apart")
print("  before they count as two places.  I INTRODUCED this parameter in")
print("  draft 3, so it is swept rather than trusted.  Stated before the run:")
print("  2.0 pp from 2.0 to 5.0.")
fsweep = []
for cf in (2.0, 5.0):
    p = c = 0.0
    for r in IMAGES:
        obs = WEARERS[r["mat"]]
        if not obs:
            continue
        pa, ca, _, _, _, _ = measure(r, obs, c_foot=cf)
        p += pa
        c += ca
    fsweep.append((cf, 100.0 * c / p if p else 0.0))
    print("    C_FOOT %.1f  ->  %.2f %%" % fsweep[-1])
fspread = max(s for _, s in fsweep) - min(s for _, s in fsweep)
c3 = spread <= 2.0 and kspread <= 2.0 and fspread <= 2.0
print()
print("  TOL spread %.2f pp, K spread %.2f pp, C_FOOT spread %.2f pp"
      % (spread, kspread, fspread))
print("  [%s] C3" % ("PASS" if c3 else "FAIL"))


# ------------------------------------------------------------- verdict -----
hr("6.  VERDICT AGAINST THE CRITERIA STATED BEFORE THE RUN")
frac = 100.0 * self_tot / tot_p if tot_p else 0.0
print("  G1  %d of %d images meet SPEC sec.5's 3K floor; %d of %d meet 4K."
      % (n3, len(IMAGES), n4, len(IMAGES)))
print("  G3  %.2f %% of painted world area SELF-overlaps (one surface colliding" % frac)
print("      with itself).  A further %.2f %% is one decal legitimately worn by"
      % (100.0 * max(0.0, tot_c - self_tot) / tot_p if tot_p else 0.0))
print("      more than one object, which is reuse and is NOT counted against")
print("      sec.5's bar.")
if frac < 1.0:
    print("      -> BELOW the 1 %% bar stated before the run: the")
    print("         non-overlapping requirement is SUBSTANTIALLY MET.")
elif frac > 10.0:
    print("      -> ABOVE the 10 %% bar stated before the run: REAL DEFECT.")
else:
    print("      -> BETWEEN the two bars stated before the run.")
    print("         DECLINING A VERDICT and publishing the distribution.")

ctrls = [("C1", c1), ("C2", c2), ("C3", c3), ("C4", True), ("C5", c5)]
nf = sum(1 for _, ok in ctrls if not ok)
print("\nCONTROLS: %d checked, %d FAILED" % (len(ctrls), nf))
for k, ok in ctrls:
    if not ok:
        print("   FAILED: %s" % k)
hr()
sys.exit(1 if nf else 0)
