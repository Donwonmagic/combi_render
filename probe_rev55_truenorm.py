"""
probe_rev55_truenorm.py -- rev 55, brief sec.3 item 2.

DOES THE CHIP GATE'S EDGE DETECTOR COLLAPSE ON THE SMOOTH RED SHELL?

t1_mats.py builds the detector as

    EDGE = 1 - dot(bevel_normal, geo.outputs["Normal"])

while its own design note two hundred lines above says, verbatim,
"edge = 1 - dot(bevel_normal, true_normal)" and "On a flat face the two
normals are identical and edge == 0 BY CONSTRUCTION".  `Normal` is the
SHADING normal.  On a FLAT-shaded mesh the two are the same thing, which is
why rev 54's counter-fascia result is untouched by this.  `T1_body` is
SMOOTH-shaded, and there the shading normal is already interpolated across
every fold -- which is very nearly what the Bevel node computes -- so the
dot product may sit near 1 and EDGE near 0 over the whole red shell.

THE EXPERIMENT IS ONE VARIABLE.  The same build, the same camera, the same
sample count, the same emission AOV; the ONLY difference between the two
arms is which socket feeds input 1 of that dot product.

    arm S   geo "Normal"        -- WHAT SHIPS
    arm T   geo "True Normal"   -- what the design note says it is

THE CONTROL IS THE COUNTER, AND IT IS THE WHOLE REASON THIS CAN BE BELIEVED.
`counter` is FLAT-shaded, so on it the two sockets are the SAME VECTOR and
the two arms MUST agree to the sampler's own noise.  If the counter moves,
the switch is doing something other than what it claims and no number here
means anything.  Rule 29.3: no finding is attributed to a cause until a
control separates it.

    T1_SUB=1 T1_TNSAMP=64 /tmp/blender/blender -b -P probe_rev55_truenorm.py
"""
import bpy, bmesh, os, sys, math
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
OUTD = os.path.join(ROOT, "probe_scratch")
os.makedirs(OUTD, exist_ok=True)

src = open(os.path.join(ROOT, "build.py")).read().split('if os.environ.get("T1_SAVE")')[0]
exec(compile(src, "build.py", "exec"))

P = print
def hdr(t): P("\n=== %s ===" % t)

import t1_mats as MT
import t1_core as T

# ------------------------------------------------- 1. ASK THE MESH FIRST
# Rule 10: grepping for a name is not a test.  The whole hypothesis rests on
# T1_body being smooth and counter being flat, so both are COUNTED.
hdr("ASK THE MESH -- which objects are smooth-shaded?")
SHADE = {}
for nm in ("T1_body", "counter"):
    o = bpy.data.objects.get(nm)
    if o is None or o.type != 'MESH':
        P("%-10s MISSING -- cannot run" % nm); raise SystemExit(1)
    polys = o.data.polygons
    sm = sum(1 for p in polys if p.use_smooth)
    SHADE[nm] = (len(polys), sm)
    P("%-10s %7d polys, %7d smooth (%.1f %%)  -> %s"
      % (nm, len(polys), sm, 100.0 * sm / max(len(polys), 1),
         "SMOOTH: shading normal is interpolated, the two sockets DIFFER"
         if sm else "FLAT: the two sockets are the SAME vector"))
assert SHADE["counter"][1] == 0, "the control is not flat -- it cannot control"
assert SHADE["T1_body"][1] > 0, "T1_body is not smooth -- there is nothing to test"

# ------------------------------------------------- 2. the taps, by graph walk
hdr("LOCATING THE DOT PRODUCT BY GRAPH WALK (not by node location)")
GRPS = [g for g in bpy.data.node_groups if g.name.startswith("WEATHER")]
assert len(GRPS) == 1, "expected exactly one shared WEATHER group"
NG = GRPS[0]
def out_links(sock): return [l for l in NG.links if l.from_socket == sock]

BEV = [n for n in NG.nodes if n.type == 'BEVEL'][0]
P("Bevel      : radius %.6f m  samples %d"
  % (BEV.inputs["Radius"].default_value, BEV.samples))
DOT = out_links(BEV.outputs[0])[0].to_node
P("dot product: %s  op=%s" % (DOT.name, DOT.operation))
_other = [l for l in NG.links if l.to_node == DOT and l.from_node != BEV]
assert len(_other) == 1
GEO = _other[0].from_node
P("its OTHER input AS SHIPPED: %s . %r"
  % (GEO.bl_idname.replace("ShaderNode", ""), _other[0].from_socket.name))
P("the sockets this node offers : %s" % [s.name for s in GEO.outputs])
assert "True Normal" in [s.name for s in GEO.outputs]
EDGE = out_links(DOT.outputs["Value"])[0].to_node
P("EDGE       : %s  op=%s   (1 - dot)" % (EDGE.name, EDGE.operation))

def set_arm(sockname):
    """Relink input 1 of the dot product.  THE ONLY VARIABLE IN THIS PROBE."""
    for l in list(NG.links):
        if l.to_node == DOT and l.from_node == GEO:
            NG.links.remove(l)
    NG.links.new(GEO.outputs[sockname], DOT.inputs[1])

# ------------------------------------------------- 3. PROBE socket = EDGE
NG.interface.new_socket("PROBE", in_out='OUTPUT', socket_type='NodeSocketFloat')
GO = [n for n in NG.nodes if n.bl_idname == 'NodeGroupOutput'][0]
NG.links.new(EDGE.outputs[0], GO.inputs["PROBE"])

hdr("REWIRING MATERIALS TO EMISSION")
PROBED, BLUE = [], []
for m in bpy.data.materials:
    if not m.use_nodes:
        continue
    nt = m.node_tree
    outs = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeOutputMaterial']
    if not outs:
        continue
    grp = [n for n in nt.nodes if n.type == 'GROUP' and n.node_tree == NG]
    em = nt.nodes.new("ShaderNodeEmission"); em.location = (600, 600)
    em.inputs["Strength"].default_value = 1.0
    if grp:
        cr = nt.nodes.new("ShaderNodeCombineColor"); cr.location = (400, 600)
        for ch in ("Red", "Green", "Blue"):
            nt.links.new(grp[0].outputs["PROBE"], cr.inputs[ch])
        nt.links.new(cr.outputs[0], em.inputs["Color"])
        PROBED.append(m.name)
    else:
        em.inputs["Color"].default_value = (0.0, 0.0, 0.35, 1.0)
        BLUE.append(m.name)
    for o in outs:
        for l in list(nt.links):
            if l.to_node == o:
                nt.links.remove(l)
        nt.links.new(em.outputs[0], o.inputs["Surface"])
P("probed %d materials; NOT probed (emit BLUE, never 'measured zero') %d"
  % (len(PROBED), len(BLUE)))

# ------------------------------------------------- 4. scene
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.use_denoising = False
sc.cycles.use_adaptive_sampling = False
sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.view_settings.view_transform = 'Standard'
sc.view_settings.look = 'None'
sc.view_settings.exposure = 0.0
sc.view_settings.gamma = 1.0
sc.render.image_settings.file_format = 'OPEN_EXR'
sc.render.image_settings.color_depth = '32'
sc.render.image_settings.color_mode = 'RGB'
SAMP = int(os.environ.get("T1_TNSAMP", "64"))
P("denoising OFF, adaptive OFF, Standard view transform, %d spp" % SAMP)

cam_d = bpy.data.cameras.new("tncam"); cam_d.type = 'ORTHO'
cam = bpy.data.objects.new("tncam", cam_d)
bpy.context.scene.collection.objects.link(cam)
cam.rotation_euler = (math.radians(90), 0, math.radians(180))   # look along -Y
bpy.context.scene.camera = cam

from PIL import Image

def load_exr(p):
    img = bpy.data.images.load(p)
    w, h = img.size
    a = np.array(img.pixels[:], dtype=np.float32).reshape(h, w, 4)[::-1]
    bpy.data.images.remove(img)
    return a

def render_to(path, samples):
    sc.cycles.samples = samples
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    return load_exr(path)

# ------------------------------------------------- 5. object masks
mk = bpy.data.materials.new("TNMASK"); mk.use_nodes = True
mnt = mk.node_tree
for n in list(mnt.nodes):
    if n.bl_idname != "ShaderNodeOutputMaterial":
        mnt.nodes.remove(n)
mo = [n for n in mnt.nodes][0]
mem = mnt.nodes.new("ShaderNodeEmission")
mem.inputs["Color"].default_value = (1, 1, 1, 1)
mnt.links.new(mem.outputs[0], mo.inputs["Surface"])

def emitters():
    for m in bpy.data.materials:
        if m == mk or not m.use_nodes:
            continue
        for n in m.node_tree.nodes:
            if n.bl_idname == 'ShaderNodeEmission':
                yield m, n

def object_mask(objname, path):
    o = bpy.data.objects[objname]
    saved = list(o.data.materials)
    o.data.materials.clear(); o.data.materials.append(mk)
    keep = []
    for m, n in emitters():
        keep.append((n, tuple(n.inputs["Color"].default_value)))
        n.inputs["Color"].default_value = (0, 0, 0, 1)
    A = render_to(path, 1)
    for n, c in keep:
        n.inputs["Color"].default_value = c
    o.data.materials.clear()
    for s in saved:
        o.data.materials.append(s)
    return A[..., 0] > 0.5

# ------------------------------------------------- 6. the crops
def view(x0, x1, z0, z1, RX):
    ORTHO = x1 - x0
    RY = max(8, int(round(RX * (z1 - z0) / ORTHO)))
    cam_d.ortho_scale = ORTHO
    cam.location = ((x0 + x1) / 2.0, 26.0, (z0 + z1) / 2.0)
    sc.render.resolution_x, sc.render.resolution_y = RX, RY
    return ORTHO / RX * 1000.0, RY

LO, HI = MT.W_EDGE_LO, MT.W_EDGE_HI
def stats(E, M):
    v = E[M]
    return dict(n=int(M.sum()), mean=float(v.mean()), p99=float(np.percentile(v, 99)),
                mx=float(v.max()),
                fLO=float((v > LO).mean()), fHI=float((v > HI).mean()))

def report(tag, obj, mmpx, S, Tn, M):
    a, b = stats(S, M), stats(Tn, M)
    P("\n  %s -- masked to %s   %d px   %.4f mm/px" % (tag, obj, a["n"], mmpx))
    P("    %-26s %10s %10s %10s" % ("", "arm S", "arm T", "T / S"))
    for k, lab in (("mean", "mean EDGE"), ("p99", "p99 EDGE"),
                   ("mx", "max EDGE"),
                   ("fLO", "frac > W_EDGE_LO %.4f" % LO),
                   ("fHI", "frac > W_EDGE_HI %.4f" % HI)):
        r = b[k] / a[k] if a[k] > 1e-12 else float('inf')
        P("    %-26s %10.6f %10.6f %10s"
          % (lab, a[k], b[k], ("%.2fx" % r) if np.isfinite(r) else "inf"))
    return a, b

def paint(path, S, Tn, M):
    """PAINT IT.  Rule 8 -- the window is part of the measurement."""
    def lay(E):
        v = np.clip(E / max(MT.W_EDGE_90, 1e-9), 0, 1)
        img = np.zeros(E.shape + (3,), np.uint8)
        img[..., 0] = (v * 255).astype(np.uint8)
        img[..., 1] = (v * 255).astype(np.uint8)
        img[..., 2] = (v * 255).astype(np.uint8)
        img[~M] = (0, 0, 60)
        return img
    a, b = lay(S), lay(Tn)
    can = np.zeros((a.shape[0] + 4, a.shape[1] * 2 + 12, 3), np.uint8)
    can[:, :] = 30
    can[2:2 + a.shape[0], 4:4 + a.shape[1]] = a
    can[2:2 + b.shape[0], 8 + a.shape[1]:8 + a.shape[1] + b.shape[1]] = b
    Image.fromarray(can).save(path)
    P("    painted -> %s   (LEFT arm S = what ships, RIGHT arm T = True Normal;"
      " white = EDGE at W_EDGE_90, dark blue = outside the mask)" % path)

# THE CONTROL WINDOW IS DERIVED FROM THE COUNTER'S OWN MESH, NOT TYPED.
# Rule 7: ask the geometry, never the pose.  A typed window put 418 px of
# counter in frame on the first run and the probe REFUSED rather than report
# a control it did not have -- which is the behaviour, but the window was
# still the defect.  Its OUTBOARD fascia (the +y face) is what the side
# camera sees, so the crop is that face's own extent, padded 15 mm.
def _obj_window(name, ysel=None, pad=0.015):
    o = bpy.data.objects[name]
    M = o.matrix_world
    V = [M @ v.co for v in o.data.vertices]
    if ysel is not None:
        ym = max(v.y for v in V)
        V = [v for v in V if v.y > ym - ysel]
    x0, x1 = min(v.x for v in V), max(v.x for v in V)
    z0, z1 = min(v.z for v in V), max(v.z for v in V)
    P("%-8s window DERIVED from %d verts: x %.4f..%.4f  z %.4f..%.4f"
      % (name, len(V), x0, x1, z0, z1))
    return x0 - pad, x1 + pad, z0 - pad, z1 + pad

_cx0, _cx1, _cz0, _cz1 = _obj_window("counter", ysel=0.05)
# The counter runs the whole vehicle length, so its own window is 3.1 m wide
# and 0.8 px of bevel radius -- too coarse to control anything.  Take a
# 0.30 m section about its middle instead, which puts the same fold at the
# same kind of mm/px as the T1_body crops.
_cmid = 0.5 * (_cx0 + _cx1)
_cx0, _cx1 = _cmid - 0.15, _cmid + 0.15
P("counter control narrowed to a 0.30 m section about x %.4f" % _cmid)

CROPS = [
    # tag,      obj,        x0,      x1,      z0,     z1,    RX
    ("flank",   "T1_body",  -1.60,  -0.40,   0.25,   1.25,   900),
    ("arch",    "T1_body",  T.X_AXLE_R - 0.10, T.X_AXLE_R + 0.10, 0.62, 0.76, 700),
    ("counter", "counter",  _cx0, _cx1, _cz0, _cz1, 900),
]

RESULT, NULLS = {}, {}
for tag, obj, x0, x1, z0, z1, RX in CROPS:
    hdr("CROP '%s'  (%s)" % (tag, obj))
    mmpx, RY = view(x0, x1, z0, z1, RX)
    P("x %.4f..%.4f  z %.4f..%.4f   %dx%d   %.4f mm/px   bevel radius %.2f mm "
      "= %.2f px here"
      % (x0, x1, z0, z1, RX, RY, mmpx,
         BEV.inputs["Radius"].default_value * 1000.0,
         BEV.inputs["Radius"].default_value * 1000.0 / mmpx))
    M = object_mask(obj, os.path.join(OUTD, "rev55_tn_%s_mask.exr" % tag))
    P("mask: %d px (%.2f %% of crop)" % (M.sum(), 100.0 * M.mean()))
    if M.sum() < 500:
        P("  *** REFUSING: fewer than 500 px of %s in this crop." % obj)
        continue
    set_arm("Normal")
    sc.cycles.seed = 0
    S = render_to(os.path.join(OUTD, "rev55_tn_%s_S.exr" % tag), SAMP)[..., 0]
    # THE NULL ARM.  The Bevel node RAY-TRACES, so EDGE is a noisy quantity and
    # a percentage difference means nothing without the sampler's own spread.
    # This is arm S again, same socket, same samples, DIFFERENT SEED -- so any
    # difference it shows is the floor, not the switch.  Rev 54 established the
    # same floor the same way on the fascia.
    sc.cycles.seed = 12345
    S2 = render_to(os.path.join(OUTD, "rev55_tn_%s_S2.exr" % tag), SAMP)[..., 0]
    sc.cycles.seed = 0
    set_arm("True Normal")
    Tn = render_to(os.path.join(OUTD, "rev55_tn_%s_T.exr" % tag), SAMP)[..., 0]
    a, b = report(tag, obj, mmpx, S, Tn, M)
    n_ = stats(S2, M)
    P("    %-26s %10.6f  <- NULL ARM (arm S, different seed): the floor"
      % ("mean EDGE", n_["mean"]))
    P("    %-26s %10.6f" % ("frac > W_EDGE_LO", n_["fLO"]))
    NULLS[tag] = n_
    paint(os.path.join(OUTD, "rev55_tn_%s.png" % tag), S, Tn, M)
    RESULT[tag] = (obj, a, b)

# ------------------------------------------------- 7. the control, judged
hdr("THE CONTROL, AND THE VERDICT -- DERIVED, NOT PRINTED")
if "counter" in RESULT:
    _, a, b = RESULT["counter"]
    n_ = NULLS.get("counter", a)
    dm = abs(b["mean"] - a["mean"]) / max(a["mean"], 1e-9)
    fl = abs(n_["mean"] - a["mean"]) / max(a["mean"], 1e-9)
    P("counter is FLAT, so the two sockets are the same vector there.")
    P("  arm S  mean %.6f" % a["mean"])
    P("  arm T  mean %.6f   -> S-to-T  %.2f %%" % (b["mean"], 100 * dm))
    P("  NULL   mean %.6f   -> S-to-S  %.2f %%   (the sampler's own floor)"
      % (n_["mean"], 100 * fl))
    # THE BAR IS THE MEASURED FLOOR, NOT A NUMBER I LIKED.  3x the null arm's
    # own spread: a real effect has to clear the noise by a clear margin.
    ctrl_ok = dm <= max(3.0 * fl, 0.02)
    P("  CONTROL %s"
      % ("HOLDS: S-to-T is inside 3x the S-to-S floor, so the switch changes "
         "nothing where nothing should change."
         if ctrl_ok else
         "FAILED: S-to-T is OUTSIDE 3x the S-to-S floor. The switch is doing "
         "something other than what it claims. NOTHING BELOW STANDS."))
else:
    ctrl_ok = False
    P("  counter crop did not run -- there is no control, so nothing stands.")

for tag in ("flank", "arch"):
    if tag not in RESULT or not ctrl_ok:
        continue
    _, a, b = RESULT[tag]
    r = b["fLO"] / a["fLO"] if a["fLO"] > 1e-12 else float('inf')
    P("\n%s (T1_body, SMOOTH):" % tag)
    P("  fraction over W_EDGE_LO   arm S %.6f   arm T %.6f" % (a["fLO"], b["fLO"]))
    if a["fLO"] < 1e-9 and b["fLO"] > 1e-6:
        P("  -> the gate is DEAD here as shipped and non-zero on the true "
          "normal.")
        P("     BUT THE TRUE NORMAL IS NOT THE FIX, AND THIS RUN CANNOT SAY "
          "SO ON ITS OWN.  On a SMOOTH mesh the true normal is piecewise")
        P("     constant, so 1-dot(bevel_n, true_n) fires on every FACET "
          "boundary -- tessellation, not folds.  Run this probe at")
        P("     T1_SUB=1 AND T1_SUB=2 and compare arm T: at rev 55 it fell "
          "0.208417 -> 0.100381 here and 0.134578 -> 0.112530 on the")
        P("     flank, i.e. it LOSES up to half its coverage when the mesh is "
          "refined.  See the retraction in t1_mats.py.")
    elif np.isfinite(r) and r > 1.5:
        P("  -> the gate is SUPPRESSED as shipped: %.2fx more of this surface "
          "clears W_EDGE_LO on the true normal." % r)
    elif np.isfinite(r) and r < 0.67:
        P("  -> the true normal gives LESS, which is not what the hypothesis "
          "predicted.  Report it and do not act on it.")
    else:
        P("  -> NO MATERIAL DIFFERENCE (%.2fx).  The hypothesis is REFUTED "
          "here: the shading normal is not collapsing this detector." % r)
P("\n(EXR files in probe_scratch/ are large -- delete before committing.)")
