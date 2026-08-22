"""
probe_rev54_aov.py -- rev 54, brief sec.3 item 2, ARM B.

RENDER THE EDGE VALUE ITSELF AS AN EMISSION AOV AND LOOK AT WHERE IT IS
NON-ZERO.  The brief's instruction, verbatim, because three revisions of
guessing produced two refuted hypotheses and no cause.

Taps the WEATHER group's internal chain by GRAPH WALK, not by node location:
    Bevel -> DotProduct -> EDGE(1-dot) -> pw(MapRange) -> craw -> hard
and drives an Emission with each in turn.  One build, N renders.

EVERY TAP IS PRINTED WITH THE NODE IT CAME FROM before it renders anything --
a tap is a window, and rule 8 applies to a node graph exactly as it applies
to a pixel mask.

Materials that do NOT carry the WEATHER group emit BLUE, so "not measured
here" can never be mistaken for "measured zero".
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

import t1_shell as SH
import t1_mats as MT

# ------------------------------------------------------------------ 1. taps
hdr("LOCATING THE TAPS BY GRAPH WALK (not by node location)")

GRPS = [g for g in bpy.data.node_groups if g.name.startswith("WEATHER")]
P("WEATHER node groups in the file: %s" % [g.name for g in GRPS])
assert len(GRPS) == 1, "expected exactly one shared WEATHER group"
NG = GRPS[0]

def out_links(sock):
    return [l for l in NG.links if l.from_socket == sock]

bev = [n for n in NG.nodes if n.type == 'BEVEL']
assert len(bev) == 1, "expected one Bevel node in WEATHER, got %d" % len(bev)
BEV = bev[0]
P("Bevel node          : %-22s radius %.6f m  samples %d"
  % (BEV.name, BEV.inputs["Radius"].default_value, BEV.samples))

DOT = out_links(BEV.outputs[0])[0].to_node
P("  -> dot product    : %-22s op=%s" % (DOT.name, DOT.operation))
# what is the OTHER input of the dot?
other = [l.from_socket for l in NG.links if l.to_node == DOT and l.from_node != BEV]
P("     other input    : %s . %s"
  % (other[0].node.bl_idname.replace("ShaderNode", ""), other[0].name))

EDGE = out_links(DOT.outputs["Value"])[0].to_node
P("  -> EDGE           : %-22s op=%s  (1 - dot)" % (EDGE.name, EDGE.operation))

pw_cands = [l.to_node for l in out_links(EDGE.outputs[0])]
P("  -> EDGE feeds     : %s" % [(n.name, n.bl_idname) for n in pw_cands])
PW = [n for n in pw_cands if n.bl_idname == 'ShaderNodeMapRange'][0]
P("  -> pw (MapRange)  : %-22s from %.5f..%.5f"
  % (PW.name, PW.inputs["From Min"].default_value, PW.inputs["From Max"].default_value))

# pw -> craw (MULTIPLY with cprod) and -> deep (MapRange)
CRAW = [l.to_node for l in out_links(PW.outputs[0])
        if l.to_node.bl_idname == 'ShaderNodeMath' and l.to_node.operation == 'MULTIPLY'][0]
P("  -> craw           : %-22s op=%s" % (CRAW.name, CRAW.operation))
CPROD = [l.from_node for l in NG.links
         if l.to_node == CRAW and l.from_node != PW][0]
P("  -> cprod          : %-22s op=%s" % (CPROD.name, CPROD.operation))
HARD = [l.to_node for l in out_links(CRAW.outputs[0])
        if l.to_node.bl_idname == 'ShaderNodeMath'][0]
P("  -> hard           : %-22s op=%s  threshold %.3f"
  % (HARD.name, HARD.operation, HARD.inputs[1].default_value))
WEAR = [l.to_node for l in out_links(HARD.outputs[0])
        if l.to_node.bl_idname == 'ShaderNodeMath'][0]
P("  -> wear           : %-22s op=%s" % (WEAR.name, WEAR.operation))

TAPS = [("edge",  EDGE.outputs[0],  "1 - dot(bevel_n, shading_n)"),
        ("pw",    PW.outputs[0],    "smoothstep(EDGE, %.4f..%.4f)"
                                    % (MT.W_EDGE_LO, MT.W_EDGE_HI)),
        ("cprod", CPROD.outputs[0], "cm * clm  (the two object-space noises)"),
        ("craw",  CRAW.outputs[0],  "pw * cprod"),
        ("hard",  HARD.outputs[0],  "craw > %.2f" % MT.W_CHIP_CUT),
        ("wear",  WEAR.outputs[0],  "hard * IN[wear]")]

# ------------------------------------------------- 2. a PROBE output socket
NG.interface.new_socket("PROBE", in_out='OUTPUT', socket_type='NodeSocketFloat')
GO = [n for n in NG.nodes if n.bl_idname == 'NodeGroupOutput'][0]

def set_tap(sock):
    for l in list(NG.links):
        if l.to_node == GO and l.to_socket.name == "PROBE":
            NG.links.remove(l)
    NG.links.new(sock, GO.inputs["PROBE"])

# --------------------------------------- 3. every material becomes emission
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
P("probed (grey = the tapped value) : %d materials" % len(PROBED))
P("NOT probed (BLUE = not measured) : %d materials -> %s"
  % (len(BLUE), ", ".join(sorted(BLUE)[:12])))
P("counter's material 'countercream' probed? %s" % ("countercream" in PROBED))

# world black, so nothing but emission is in the frame
w = bpy.context.scene.world
if w is None:
    w = bpy.data.worlds.new("AOVWORLD"); bpy.context.scene.world = w
w.use_nodes = True
for n in w.node_tree.nodes:
    if n.bl_idname == 'ShaderNodeBackground':
        n.inputs["Color"].default_value = (0, 0, 0, 1)
        n.inputs["Strength"].default_value = 0.0
P("world: %s, background forced to black" % w.name)

# ------------------------------------------------------- 4. the crop camera
hdr("WHERE THE SHOW-SIDE FASCIA ACTUALLY IS -- ASKED OF THE MESH")
ob = bpy.data.objects["counter"]
bm = bmesh.new(); bm.from_mesh(ob.data); bm.transform(ob.matrix_world)
V = [v.co.copy() for v in bm.verts]
bm.free()
P("counter, ALL verts : x %.4f..%.4f  y %.4f..%.4f  z %.4f..%.4f"
  % (min(v.x for v in V), max(v.x for v in V), min(v.y for v in V),
     max(v.y for v in V), min(v.z for v in V), max(v.z for v in V)))
FAS = [v for v in V if v.y > 0.90]
P("the +y FASCIA verts : n=%d  x %.4f..%.4f  y %.4f..%.4f  z %.4f..%.4f"
  % (len(FAS), min(v.x for v in FAS), max(v.x for v in FAS),
     min(v.y for v in FAS), max(v.y for v in FAS),
     min(v.z for v in FAS), max(v.z for v in FAS)))
FX0, FX1 = min(v.x for v in FAS), max(v.x for v in FAS)
FZ0, FZ1 = min(v.z for v in FAS), max(v.z for v in FAS)
P("FASCIA BOTTOM FOLD z = %.4f  (this is the row every profile is measured from)" % FZ0)

sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.use_denoising = False          # a denoiser would SMEAR the answer
sc.cycles.use_adaptive_sampling = False
sc.render.resolution_percentage = 100
sc.render.film_transparent = False
sc.view_settings.view_transform = 'Standard'   # linear: 1.0 emission -> 1.0
sc.view_settings.look = 'None'
sc.view_settings.exposure = 0.0
sc.view_settings.gamma = 1.0
sc.render.image_settings.file_format = 'OPEN_EXR'
sc.render.image_settings.color_depth = '32'
sc.render.image_settings.color_mode = 'RGB'
SAMP = int(os.environ.get("T1_AOVSAMP", "64"))
P("\ndenoising OFF, adaptive OFF, view transform Standard, %d spp" % SAMP)

cam_d = bpy.data.cameras.new("aovcam"); cam_d.type = 'ORTHO'
cam = bpy.data.objects.new("aovcam", cam_d)
bpy.context.scene.collection.objects.link(cam)
# LOOK ALONG -Y.  Euler (90,0,0) points at +Y -- AWAY from the vehicle; that
# cost one render and a zero-pixel mask.  (90,0,180) is -Y.  Asserted below
# by the mask's own pixel count, which is the only thing that proves it.
cam.rotation_euler = (math.radians(90), 0, math.radians(180))
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

# ------------------------------------------------- 5. the mask machinery
mk = bpy.data.materials.new("AOVMASK"); mk.use_nodes = True
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
    """Give ONE object its own white emitter, black everything else, render."""
    o = bpy.data.objects[objname]
    saved = list(o.data.materials)
    o.data.materials.clear(); o.data.materials.append(mk)
    keep = []
    for m, n in emitters():
        keep.append((n, tuple(n.inputs["Color"].default_value)))
        for l in list(m.node_tree.links):
            if l.to_node == n and l.to_socket.name == "Color":
                m.node_tree.links.remove(l)
        n.inputs["Color"].default_value = (0, 0, 0, 1)
    a = render_to(path, 16)
    for n, c in keep:
        n.inputs["Color"].default_value = c
    for m in bpy.data.materials:
        if m == mk or not m.use_nodes:
            continue
        g = [q for q in m.node_tree.nodes if q.type == 'GROUP' and q.node_tree == NG]
        cc = [q for q in m.node_tree.nodes if q.bl_idname == 'ShaderNodeCombineColor']
        e = [q for q in m.node_tree.nodes if q.bl_idname == 'ShaderNodeEmission']
        if g and cc and e:
            m.node_tree.links.new(cc[0].outputs[0], e[0].inputs["Color"])
    o.data.materials.clear()
    for m in saved:
        o.data.materials.append(m)
    return a[:, :, 0] > 0.5

# --------------------------------------------------- 6. run one crop
import json
import scipy.ndimage as ndi

META = {}

def fold_per_column(MK):
    """THE FOLD IS A LINE AND IT SLOPES.  A single min(z) is the wrong row --
    the mask's own last row disagreed with the mesh's global minimum by 134 px
    in the tight crop, which is rule 7: ask the geometry, do not assume a pose.
    Returns fold row per column, -1 where the object is absent."""
    RY, RX = MK.shape
    f = np.full(RX, -1, np.int32)
    any_ = MK.any(axis=0)
    idx = np.where(any_)[0]
    f[idx] = (RY - 1) - np.argmax(MK[::-1, :][:, idx], axis=0)
    return f

def band_mask(MK, fold, lo_mm, hi_mm, MMPX):
    """pixels whose distance ABOVE the per-column fold lies in [lo,hi) mm."""
    RY, RX = MK.shape
    rr = np.arange(RY)[:, None]
    d = (fold[None, :] - rr) * MMPX          # mm above the fold
    return MK & (d >= lo_mm) & (d < hi_mm) & (fold[None, :] >= 0)

def run_crop(tag, x0, x1, z0, z1, RX, taps, samples, radius_mm=None):
    hdr("CROP '%s'%s" % (tag, "" if radius_mm is None else
                         "   BEVEL RADIUS %.2f mm" % radius_mm))
    if radius_mm is not None:
        BEV.inputs["Radius"].default_value = radius_mm / 1000.0
    RAD = BEV.inputs["Radius"].default_value * 1000.0
    ORTHO = x1 - x0
    RY = max(8, int(round(RX * (z1 - z0) / ORTHO)))
    cam_d.ortho_scale = ORTHO
    cam.location = ((x0 + x1) / 2.0, 26.0, (z0 + z1) / 2.0)
    sc.render.resolution_x, sc.render.resolution_y = RX, RY
    MMPX = ORTHO / RX * 1000.0
    P("x %.4f..%.4f  z %.4f..%.4f   %dx%d   %.4f mm/px (%.1f px/m)"
      % (x0, x1, z0, z1, RX, RY, MMPX, RX / ORTHO))
    P("bevel radius %.2f mm = %.2f px here" % (RAD, RAD / MMPX))
    META[tag] = dict(x0=x0, x1=x1, z0=z0, z1=z1, RX=RX, RY=RY, mmpx=MMPX,
                     radius_mm=RAD, samples=samples)

    MK = object_mask("counter", os.path.join(OUTD, "rev54_%s_mask.exr" % tag))
    assert MK.sum() > 0, "the mask is EMPTY -- the camera is not looking at it"
    fold = fold_per_column(MK)
    ok = fold >= 0
    P("counter mask: %d px (%.2f %% of crop); %d of %d columns carry it"
      % (MK.sum(), 100.0 * MK.mean(), ok.sum(), RX))
    P("PER-COLUMN FOLD row: %d..%d  (a single global min(z) would have said %d)"
      % (fold[ok].min(), fold[ok].max(),
         int(round((z1 - FZ0) / (z1 - z0) * RY))))
    P("  the fold DROPS %.2f mm across this crop -- it SLOPES, and that is why"
      % ((fold[ok].max() - fold[ok].min()) * MMPX))
    P("  a fixed row band is the wrong instrument here.")
    np.save(os.path.join(OUTD, "rev54_%s_mk.npy" % tag), MK)
    np.save(os.path.join(OUTD, "rev54_%s_fold.npy" % tag), fold)
    Image.fromarray((MK * 255).astype(np.uint8)).save(
        os.path.join(OUTD, "rev54_%s_mask.png" % tag))

    R = {}
    P("\n%-7s %-30s %9s %9s %9s %9s" %
      ("tap", "what it is", "max", "mean", "frac>0", "frac>.5"))
    for nm, sock, what in taps:
        set_tap(sock)
        a = render_to(os.path.join(OUTD, "rev54_%s_%s.exr" % (tag, nm)),
                      samples)[:, :, 0]
        R[nm] = a
        np.save(os.path.join(OUTD, "rev54_%s_%s.npy" % (tag, nm)), a)
        v = a[MK]
        P("%-7s %-30s %9.5f %9.5f %8.3f%% %8.3f%%"
          % (nm, what, v.max(), v.mean(),
             100.0 * (v > 1e-4).mean(), 100.0 * (v > 0.5).mean()))
        g = a / max(a.max(), 1e-6)
        rgb = np.dstack([g, g, g]); b = np.zeros_like(g)
        rgb[~MK] = np.dstack([b, b, b + 0.30])[~MK]
        Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(
            os.path.join(OUTD, "rev54_%s_%s.png" % (tag, nm)))
    return R, MK, fold, MMPX

def profile(tag, R, MK, fold, MMPX, edges):
    P("\nPROFILE -- bands measured UP FROM THE PER-COLUMN FOLD (mm)")
    P("%-12s %8s %9s %9s %9s %9s %9s"
      % ("band mm", "px", "EDGE mn", "pw mn", "cprod mn", "craw mx", "hard>.5"))
    rows = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        b = band_mask(MK, fold, lo, hi, MMPX)
        if b.sum() == 0:
            continue
        r = dict(lo=lo, hi=hi, px=int(b.sum()),
                 edge=float(R['edge'][b].mean()),
                 pw=float(R['pw'][b].mean()) if 'pw' in R else float('nan'),
                 cprod=float(R['cprod'][b].mean()) if 'cprod' in R else float('nan'),
                 craw=float(R['craw'][b].max()) if 'craw' in R else float('nan'),
                 hard=float(100.0 * (R['hard'][b] > 0.5).mean()) if 'hard' in R else float('nan'))
        rows.append(r)
        P("%-12s %8d %9.5f %9.5f %9.5f %9.5f %8.3f%%"
          % ("%g-%g" % (lo, hi), r['px'], r['edge'], r['pw'], r['cprod'],
             r['craw'], r['hard']))
    META.setdefault(tag, {})['profile'] = rows
    # paint the 0-2 mm band and LOOK at it
    b0 = band_mask(MK, fold, 0, 2, MMPX)
    ov = np.zeros(MK.shape + (3,), np.uint8)
    ov[MK] = (60, 60, 60)
    ov[b0] = (255, 0, 0)
    Image.fromarray(ov).save(os.path.join(OUTD, "rev54_%s_band0_2.png" % tag))
    P("painted the 0-2 mm band -> probe_scratch/rev54_%s_band0_2.png (%d px)"
      % (tag, b0.sum()))
    return rows


def halfwidth(R, MK, fold, MMPX, tag):
    """How far above the fold does EDGE actually reach?  If the Bevel node is
    doing what its radius says, this tracks the radius.  rev 53 could not see
    this at 271 px/m because the whole band was 0.75 px."""
    P("\nEDGE REACH -- mean EDGE in 0.25 mm bands, and where it falls to 10 %%")
    xs, ys = [], []
    mm = 0.0
    while mm < 20.0:
        b = band_mask(MK, fold, mm, mm + 0.25, MMPX)
        if b.sum() >= 20:
            xs.append(mm + 0.125); ys.append(float(R['edge'][b].mean()))
        mm += 0.25
    if not xs:
        P("  (no band pixels)"); return None
    y0 = max(ys)
    thr = 0.10 * y0
    reach = None
    for x, y in zip(xs, ys):
        if y < thr:
            reach = x; break
    P("  peak mean EDGE %.5f at %.2f mm above the fold" % (y0, xs[int(np.argmax(ys))]))
    P("  falls below 10 %% of peak at %s mm"
      % ("%.2f" % reach if reach is not None else ">20"))
    P("  %-8s %s" % ("mm", "mean EDGE"))
    for x, y in list(zip(xs, ys))[:24]:
        P("  %-8.2f %.5f  %s" % (x, y, "#" * int(round(60 * y / max(y0, 1e-9)))))
    META.setdefault(tag, {})['edge_reach_mm'] = reach
    return reach


def blobs(R, MK, MMPX, tag):
    P("\nTHE CHIP POPULATION -- blob statistics of hard > 0.5")
    h = (R['hard'] > 0.5) & MK
    lab, n = ndi.label(h)
    if n == 0:
        P("  NO chip blobs at all."); META.setdefault(tag, {})['chips'] = 0; return
    sizes = np.bincount(lab.ravel())[1:]
    area = sizes * MMPX * MMPX
    dia = 2.0 * np.sqrt(area / math.pi)
    P("  %d blobs, total %d px = %.2f mm^2" % (n, h.sum(), area.sum()))
    P("  blob diameter (equivalent circle): min %.3f  median %.3f  mean %.3f  max %.3f mm"
      % (dia.min(), np.median(dia), dia.mean(), dia.max()))
    P("  area-weighted mean diameter %.3f mm"
      % (float((dia * area).sum() / area.sum())))
    P("  coverage of the counter mask: %.4f %%" % (100.0 * h.sum() / MK.sum()))
    META.setdefault(tag, {}).update(
        chips=int(n), chip_area_mm2=float(area.sum()),
        chip_dia_med_mm=float(np.median(dia)),
        chip_dia_awt_mm=float((dia * area).sum() / area.sum()))


def ladder(R, MK, MMPX, tag, targets):
    """What survives at coarser pixel scales.  Box-averaging a LINEAR AOV is
    exactly what a lower-resolution render integrates to, so this needs no
    extra render -- but it is a MODEL of one, and is labelled as such."""
    P("\nRESOLUTION LADDER -- box-average the linear `wear` AOV to coarser px")
    P("(a model of a coarser render, not a render: stated, not hidden)")
    w = R['wear'] * MK
    P("  %-12s %8s %10s %10s %10s"
      % ("mm/px", "factor", "peak wear", "mean wear", "frac>0.05"))
    for t in targets:
        f = max(1, int(round(t / MMPX)))
        RY, RX = w.shape
        ry, rx = (RY // f) * f, (RX // f) * f
        if ry == 0 or rx == 0:
            continue
        dw = w[:ry, :rx].reshape(ry // f, f, rx // f, f).mean(axis=(1, 3))
        dm = MK[:ry, :rx].reshape(ry // f, f, rx // f, f).mean(axis=(1, 3))
        sel = dm > 0.5
        if sel.sum() == 0:
            continue
        P("  %-12.3f %8d %10.5f %10.5f %9.3f%%"
          % (f * MMPX, f, dw[sel].max(), dw[sel].mean(),
             100.0 * (dw[sel] > 0.05).mean()))

# ------------------------------------------------------------- 7. run it
SAMP = int(os.environ.get("T1_AOVSAMP", "64"))
BANDS = [0, 1, 2, 3, 4, 6, 9, 12, 18, 24, 30, 42]
cx = (FX0 + FX1) / 2.0
TIGHT = (cx - 0.15, cx + 0.15, FZ0 - 0.030, FZ0 + 0.070, 1600)

# ---- the default radius, full chain
R, MK, fold, MMPX = run_crop("tight", *TIGHT, taps=TAPS, samples=SAMP)
profile("tight", R, MK, fold, MMPX, BANDS)
halfwidth(R, MK, fold, MMPX, "tight")
blobs(R, MK, MMPX, "tight")
# 3.687 mm/px is the SHIPPED side render's own scale (271.2 px/m); 4.728 is
# ref_side.jpg's.  Both are derived below from the ledger's px/m, printed.
for lbl, pxm in (("shipped side render", 271.2), ("ref_side.jpg", 211.5)):
    P("  %-22s %.1f px/m -> %.3f mm/px" % (lbl, pxm, 1000.0 / pxm))
ladder(R, MK, MMPX, "tight", [MMPX, 0.5, 1.0, 2.0, 1000.0 / 271.2, 1000.0 / 211.5])

# ---- DOES THE BAND TRACK THE RADIUS?  rev 53 could not see this at 271 px/m.
hdr("RADIUS SWEEP AT 5333 px/m -- the measurement rev 53 could not make")
SWEEP = [t for t in TAPS if t[0] in ("edge", "hard")]
for rad in (1.0, 2.75, 6.0, 12.0):
    tg = "r%s" % str(rad).replace(".", "p")
    Rr, MKr, foldr, MMr = run_crop(tg, *TIGHT, taps=SWEEP, samples=32,
                                   radius_mm=rad)
    reach = halfwidth(Rr, MKr, foldr, MMr, tg)
    h = (Rr['hard'] > 0.5) & MKr
    lab, n = ndi.label(h)
    P("  radius %5.2f mm -> EDGE reach %s mm, %d chip blobs, coverage %.4f %%"
      % (rad, "%.2f" % reach if reach else "n/a", n, 100.0 * h.sum() / MKr.sum()))
    META[tg]['chips'] = int(n)
    META[tg]['coverage_pct'] = float(100.0 * h.sum() / MKr.sum())
BEV.inputs["Radius"].default_value = SH.GAPW / 2.0    # restore the derived one

json.dump(META, open(os.path.join(OUTD, "rev54_aov_meta.json"), "w"), indent=1)
P("\nmetadata -> probe_scratch/rev54_aov_meta.json")
P("DONE -- crop the PNGs in probe_scratch/ and LOOK AT THEM")
