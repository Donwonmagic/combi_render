"""probe_rev59_mural.py -- rev 59.  THE ROOF MURAL BOARD: size, border, finish.

The owner reported the mural board "not true to size/scale/material".  This
probe measures the three things the fix touches and renders the frames the
numbers are read off, in ONE build per configuration.

IT CHANGES NO SOURCE.  The specular sweep is applied to the BUILT `lidmural`
material after build.py has run, so the shipped constant is untouched and
nothing can be left behind in the tree.  (`Specular IOR Level` is an UNLINKED
default on this material -- apply_weather() re-routes Base Color, Roughness
and Normal but never touches Specular -- so writing default_value here is the
live path, not an inert one.  It REFUSES if it finds the socket linked, rather
than reporting a flat sweep as "no effect": that is F53 / rule 36.)

    T1_SUB=1 T1_MU_PFX=m59 T1_MU_SPEC=0.16,0.30,0.50 \
      /tmp/blender/blender -b -P probe_rev59_mural.py

    T1_SUB=1 T1_LIDINSET=0.030 ...   # the item-1 ABLATION: the border returns
    T1_SUB=1 T1_LIDWEATHER=0    ...   # the item-2 ABLATION: the boards go bare

WHAT IT PRINTS, all WATCHED, none transcribed:
  * the decal quad's own edge lengths and aspect, off the MESH;
  * tex/lidmural.png's authored pixel aspect, off the file's IHDR;
  * the cream border in mm and in projected pixels, per side;
  * the projected pixel window of the board and of the panel it sits on, so
    the crop that every number is read from is DECLARED before it is taken;
  * whether the WEATHER group actually reaches each board's BSDF.
"""
import os, sys, math, struct
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.environ.setdefault("T1_SUB", "1")
_prev = os.environ.pop("T1_PREVIEW", None)
exec(compile(open(os.path.join(ROOT, "build.py")).read(), "build.py", "exec"))

import bpy
from bpy_extras.object_utils import world_to_camera_view
import studio as ST
P = print

ST.rig(key=float(os.environ.get("T1_KEY", "1.0")), scene="studio", log=P)

VIEW = os.environ.get("T1_MU_VIEW", "side")
RX = int(os.environ.get("T1_RX", "1600"))
RY = int(os.environ.get("T1_RY", "1100"))
SAMP = int(os.environ.get("T1_SAMP", "48"))
PFX = os.environ.get("T1_MU_PFX", "m59")
OUT = os.path.join(ROOT, "out")

P("=" * 74)
P("  rev 59 -- the roof mural board")
P("=" * 74)

# ---------------------------------------------------------------- geometry
bd = bpy.data.objects.get("lid_board")
mn = bpy.data.objects.get("lid_main")
if bd is None or mn is None:
    raise SystemExit("NO BOARD: lid_board=%r lid_main=%r -- refusing to "
                     "report a measurement off a scene that has no board"
                     % (bd, mn))


def _wco(ob):
    return [ob.matrix_world @ v.co for v in ob.data.vertices]


BW = _wco(bd)
MW = _wco(mn)
# The lid is hinged about a FORE-AFT axis, so X is untouched by the pose and
# the board's other edge lies in the (y,z) plane.  Ask the geometry for both
# rather than assuming the pose (rule 35): the long edge is the X span, the
# short edge is the largest (y,z) separation among the quad's own corners.
bl = max(c.x for c in BW) - min(c.x for c in BW)
ml = max(c.x for c in MW) - min(c.x for c in MW)


def _yz_span(W):
    """The panel's SHORT edge, in world space.

    RETRACTED AND CORRECTED IN THE SAME REVISION IT WAS WRITTEN.  The first
    version took the lowest-z and the highest-z vertex and measured between
    them.  On this quad those two are a DIAGONAL, not an edge -- build.py's
    step-8b rake shear drops z as a function of x, so the extreme-z corners
    are at opposite ends of the board.  It printed 1.2588 m for a 1.2237 m
    edge, i.e. +2.9 %, and it printed it with a straight face: the derived
    "STRETCH along the vehicle" came out -2.33 % when the correct figure is
    +0.47 %, THE WRONG SIGN.  `_decal_aspect_guard()` in t1_shell.py, which
    measures in the un-hinged frame, is what disagreed with it.
    Ask for an EDGE: take the corners that share the extreme x, so the span
    cannot run diagonally across the panel.
    """
    xs = [c.x for c in W]
    end = [c for c in W if abs(c.x - min(xs)) < 1e-6]
    lo = min(end, key=lambda c: c.z)
    hi = max(end, key=lambda c: c.z)
    return math.hypot(hi.y - lo.y, hi.z - lo.z)


bw_ = _yz_span(BW)
mw_ = _yz_span(MW)

tp = os.path.join(ROOT, "tex", "lidmural.png")
if os.path.exists(tp):
    h = open(tp, "rb").read(24)
    iw, ih = struct.unpack(">II", h[16:24])
    authored = iw / float(ih)
    tex = "%d x %d = %.4f" % (iw, ih, authored)
else:
    authored, tex = None, "NO TEXTURE ON DISK"

P("  decal quad (mesh)   %.4f x %.4f m   aspect %.4f" % (bl, bw_, bl / bw_))
P("  lid panel  (mesh)   %.4f x %.4f m   aspect %.4f" % (ml, mw_, ml / mw_))
P("  tex/lidmural.png    %s" % tex)
if authored:
    P("  STRETCH along the vehicle: %+.3f %%"
      % ((bl / bw_) / authored * 100.0 - 100.0))
P("  bare border, per side:  long axis %.1f mm   short axis %.1f mm"
  % ((ml - bl) * 500.0, (mw_ - bw_) * 500.0))
P("  bare border as a fraction of the panel: %.2f %% of length, %.2f %% of "
  "width" % ((ml - bl) / ml * 100.0, (mw_ - bw_) / mw_ * 100.0))

# ------------------------------------------------- the material, and its state
M = bpy.data.materials
for k in ("lidmural", "lidsign"):
    m = M.get(k)
    if m is None:
        P("  %-9s NO MATERIAL" % k)
        continue
    b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    # WALK THE CHAIN, do not read the immediate upstream node.  The first
    # version of this reported "WEATHER spliced: NO" on `lidmural` while the
    # splice was in fact present: `round_edges()` runs AFTER build_all() and
    # inserts a Bevel into every Principled Normal, FEEDING THE EXISTING LINK
    # INTO IT rather than discarding it.  So a weathered material's Normal
    # legitimately reads BEVEL, with the group one hop further back.  A
    # one-hop test called the shipped state a defect.
    def _chain(sock, depth=0):
        if not sock.links or depth > 6:
            return "-"
        n = sock.links[0].from_node
        if n.type == 'GROUP':
            return "GROUP"
        for i in n.inputs:
            r = _chain(i, depth + 1)
            if r == "GROUP":
                return "GROUP via %s" % n.type
        return n.type
    drv = {s: _chain(b.inputs[s]) for s in
           ("Base Color", "Roughness", "Normal")}
    P("  %-9s spec %.4f (F0 %.4f)  users %d" %
      (k, b.inputs["Specular IOR Level"].default_value,
       0.08 * b.inputs["Specular IOR Level"].default_value, m.users))
    P("             BaseColor<-%s  Roughness<-%s  Normal<-%s"
      % (drv["Base Color"], drv["Roughness"], drv["Normal"]))
    P("             WEATHER spliced: %s"
      % ("YES" if all(v.startswith('GROUP') for v in drv.values()) else "NO"))

# ----------------------------------------------- the crop window, DECLARED
sc = bpy.context.scene
V = ST.views()[VIEW]
cam = sc.camera or ST.camera()
ST.aim(cam, V["loc"], V["tgt"], V.get("lens"), V.get("ortho"),
       V.get("focus"), V.get("fstop"))
sc.render.resolution_x, sc.render.resolution_y = RX, RY
bpy.context.view_layer.update()


def _px(W):
    xs, ys = [], []
    for c in W:
        u = world_to_camera_view(sc, cam, c)
        xs.append(u.x * RX)
        ys.append((1.0 - u.y) * RY)
    return min(xs), max(xs), min(ys), max(ys)


for nm, W in (("lid_board", BW), ("lid_main", MW)):
    x0, x1, y0, y1 = _px(W)
    P("  %-9s in %-6s px x %.1f..%.1f  y %.1f..%.1f   (%.1f x %.1f px)"
      % (nm, VIEW, x0, x1, y0, y1, x1 - x0, y1 - y0))
P("  WINDOW=%s %d %d" % (VIEW, RX, RY))
bx0, bx1, by0, by1 = _px(BW)
mx0, mx1, my0, my1 = _px(MW)
P("  BOARDPX %.2f %.2f %.2f %.2f" % (bx0, bx1, by0, by1))
P("  PANELPX %.2f %.2f %.2f %.2f" % (mx0, mx1, my0, my1))

# ------------------------------------------------------- the specular sweep
mm = M.get("lidmural")
bb = next(n for n in mm.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
if bb.inputs["Specular IOR Level"].is_linked:
    raise SystemExit(
        "T1_MU_SPEC: lidmural's Specular IOR Level is LINKED, so writing "
        "default_value here would be INERT -- REFUSING rather than reporting "
        "a flat sweep as 'the lever has no authority' (F53 / rule 36).")
shipped = float(bb.inputs["Specular IOR Level"].default_value)
sweep = os.environ.get("T1_MU_SPEC")
vals = [float(v) for v in sweep.split(",")] if sweep else [shipped]

for v in vals:
    bb.inputs["Specular IOR Level"].default_value = v
    tag = "%s_s%03d" % (PFX, round(v * 100))
    P("")
    P("  RENDER  spec %.3f (F0 %.4f)  -> %s_%s.png" % (v, 0.08 * v, tag, VIEW))
    ST.render_set([VIEW], OUT, prefix=tag, res=(RX, RY), samples=SAMP,
                  transparent=True, log=P)
bb.inputs["Specular IOR Level"].default_value = shipped
P("")
P("  done.  shipped spec restored to %.3f in this session's datablock." % shipped)
