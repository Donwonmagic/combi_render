"""rev 15 -- the three-point solves for work-list items 1, 2 and 3.

Run headless, one mode per invocation:

    T1_SOLVE=mural  T1_MURAL_SPEC=0.16  blender -b --python shader_solve.py
    T1_SOLVE=cream  T1_W_ALB=0.260      blender -b --python shader_solve.py
    T1_SOLVE=ctan   T1_CTAN=r,g,b       blender -b --python shader_solve.py

WHY THIS FILE EXISTS RATHER THAN A BEAUTY-PIXEL EYEBALL.  Every one of these
three numbers has already been got wrong once by comparing a texture-file mean
to a tonemapped render mean, which crosses AgX + Punchy AND an sRGB decode.
So every render here is taken with

    view_transform = 'Standard',  look = 'None',  exposure = 0,  gamma = 1

i.e. plain sRGB, and decoded back to linear in numpy.  That is the only way a
"linear ratio" in this file means the same thing as a "linear ratio" measured
off `ref_side.jpg` with PIL.

The mural mode reads the DENOISING ALBEDO pass, not the beauty pass, because the
quantity under solve -- `img_paint`'s Specular IOR Level -- is an achromatic
pedestal on the material's own reflectance, and the albedo pass is the only
output that carries it without also carrying the light rig.

MASKS ARE RENDERED, NEVER GUESSED.  Each region is isolated by re-rendering the
same camera with everything except the target object hidden and reading alpha.
A bounding box on a tilted object catches its neighbours -- that is exactly how
rev 14's "rear pane CV 1.22" came about, and it is not repeated here.
"""
import bpy, os, sys, math
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

MODE = os.environ.get("T1_SOLVE", "mural")
OUT = os.path.join(ROOT, "out")
os.makedirs(OUT, exist_ok=True)

# ---- build the scene exactly as build.py does, minus the save tail ---------
src = open(os.path.join(ROOT, "build.py")).read().split('if os.environ.get("T1_SAVE")')[0]
exec(compile(src, "build.py", "exec"))
import studio as ST


# ---------------------------------------------------------------- helpers --
def srgb_to_lin(a):
    a = np.asarray(a, dtype=np.float64)
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)


def lin_to_srgb(a):
    a = np.clip(np.asarray(a, dtype=np.float64), 0.0, None)
    return np.where(a <= 0.0031308, a * 12.92, 1.055 * a ** (1 / 2.4) - 0.055)


def _gauss1d(sig):
    r = max(1, int(3.0 * sig + 0.5))
    x = np.arange(-r, r + 1, dtype=np.float64)
    k = np.exp(-0.5 * (x / sig) ** 2)
    return k / k.sum()


def gblur(a, sig):
    """Separable Gaussian in pure numpy -- Blender's bundled python has no scipy."""
    k = _gauss1d(sig)
    r = (len(k) - 1) // 2
    p = np.pad(a, ((r, r), (0, 0)), mode='reflect')
    o = np.zeros_like(a)
    for i, w in enumerate(k):
        o += w * p[i:i + a.shape[0], :]
    p = np.pad(o, ((0, 0), (r, r)), mode='reflect')
    o2 = np.zeros_like(a)
    for i, w in enumerate(k):
        o2 += w * p[:, i:i + a.shape[1]]
    return o2


def erode(m, n):
    r = n // 2
    p = np.pad(m, ((r, r), (r, r)), mode='constant', constant_values=False)
    o = np.ones_like(m)
    for i in range(n):
        for j in range(n):
            o = o & p[i:i + m.shape[0], j:j + m.shape[1]]
    return o


def _plain_view(sc):
    """No AgX, no Punchy, no exposure. The file becomes invertible."""
    sc.view_settings.view_transform = 'Standard'
    sc.view_settings.look = 'None'
    # rev 15: the first ctan run clipped 60.9 % of the frame at >= 0.995 -- BOTH
    # the plywood top and the cream fascia sat pinned near 1.0, so the probe
    # could not see the quantity it was measuring.  Exposure divides out of a
    # ratio exactly, so pulling it down costs nothing and restores the dynamic
    # range.  Caught by the clipped-fraction line this file prints, not by eye.
    sc.view_settings.exposure = float(os.environ.get("T1_SOLVE_EV", 0.0))
    sc.view_settings.gamma = 1.0


def _render(path, res, samples, transparent=False, albedo=False):
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.cycles.samples = samples
    sc.render.film_transparent = transparent
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'
    sc.render.image_settings.color_depth = '16'
    _plain_view(sc)

    vl = sc.view_layers[0]
    sc.use_nodes = True
    nt = sc.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    rl = nt.nodes.new("CompositorNodeRLayers")
    cp = nt.nodes.new("CompositorNodeComposite")
    if albedo:
        vl.cycles.denoising_store_passes = True
        sc.cycles.use_denoising = True
        # re-evaluate so the socket exists
        bpy.context.view_layer.update()
        sock = rl.outputs.get("Denoising Albedo")
        if sock is None:
            raise SystemExit("FATAL: no Denoising Albedo socket -- cannot solve")
        nt.links.new(sock, cp.inputs["Image"])
    else:
        nt.links.new(rl.outputs["Image"], cp.inputs["Image"])
        if "Alpha" in rl.outputs and "Alpha" in cp.inputs:
            nt.links.new(rl.outputs["Alpha"], cp.inputs["Alpha"])
    if os.environ.get("T1_SOLVE_NODENOISE") == "1":
        sc.cycles.use_denoising = False        # control: is OIDN eating the breakup?
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    real = path + ".png"
    if not os.path.exists(real):
        real = sc.render.frame_path(frame=sc.frame_current)
    from PIL import Image
    # ------------------------------------------------------------- rev 57
    # THE 16-BIT BRANCH BELOW CAN NEVER BE TAKEN, AND IT LOOKS LIKE IT CAN.
    # F42.  color_depth is set to '16' above and Blender DELIVERS -- the
    # written PNG's own IHDR reads bit depth 16, colour type 6, checked byte
    # by byte.  But PIL's convert("RGBA") returns uint8, so by the time
    # a.max() is tested the low byte is already gone and the test is on the
    # WRONG SIDE OF THE CONVERSION.  Every measurement that comes through
    # this function -- both arms of mottle_measure.py, and the mural solve --
    # is therefore 8-bit.
    #
    # MEASURED rather than argued, with a stdlib 16-bit decoder CONTROLLED
    # against PIL (its top byte is bit-identical to PIL's read for 100.0000 %
    # of pixels, max difference 0):
    #     cream patch sd   3.9999 at 16 bits   vs  4.0200 here   (+0.50 %)
    # SO THE AGGREGATE COST IS SMALL AND IS STATED AS SMALL.  What it destroys
    # is a small signal on a large one: the cream mottle's entire contribution
    # to this patch is sd 0.2594 DN against an 8-bit quantisation noise floor
    # of 1/sqrt(12) = 0.289 DN -- the mottle is quantised to 0.9 of one step
    # by the reader, in the file named mottle_measure.py.
    #
    # NOT FIXED HERE, deliberately.  This is a SHARED path; every consumer's
    # numbers move if it changes, and changing it without re-running each of
    # them is the failure this project's own record warns about.  The line
    # stays as it is so the defect stays watchable, and the fix is a whole
    # revision's item with the decoder already written and controlled.
    a = np.asarray(Image.open(real).convert("RGBA"), dtype=np.float64)
    a /= 65535.0 if a.max() > 255.0 else 255.0
    return a


def _only(objs):
    """Hide everything except `objs` from the render. Returns a restore fn."""
    keep = set(o.name for o in objs)
    was = {}
    for o in bpy.data.objects:
        was[o.name] = o.hide_render
        if o.type == 'MESH':
            o.hide_render = o.name not in keep
    def restore():
        for o in bpy.data.objects:
            if o.name in was:
                o.hide_render = was[o.name]
    return restore


def _objs_with_material(name):
    out = []
    for o in bpy.data.objects:
        if o.type != 'MESH':
            continue
        for s in o.material_slots:
            if s.material and s.material.name == name:
                out.append(o)
                break
    return out


def _mask_for(objs, path, res, cam_setup):
    """Render alpha with only `objs` visible. A rendered mask, not a box."""
    restore = _only(objs)
    cam_setup()
    a = _render(path, res, 1, transparent=True)
    restore()
    return a[..., 3] > 0.5


def _report(tag, rows):
    print("\n" + "=" * 68)
    print("SOLVE %s" % tag)
    print("=" * 68)
    for r in rows:
        print(r)
    print("=" * 68 + "\n")


# ------------------------------------------------------------------ mural --
def solve_mural():
    spec = float(os.environ.get("T1_MURAL_SPEC", 0.16))
    boards = _objs_with_material("lidmural")
    if not boards:
        raise SystemExit("FATAL: no object carries `lidmural`")
    ob = boards[0]

    # aim an ortho camera down the board's own largest-face normal, so the
    # measured patch is the painted face and not a rim or the reverse.
    dg = bpy.context.evaluated_depsgraph_get()
    me = ob.evaluated_get(dg).to_mesh()
    M = ob.matrix_world
    best, bn, bc = -1.0, None, None
    for p in me.polygons:
        if p.area > best:
            best = p.area
            bn = (M.to_3x3() @ p.normal).normalized()
            bc = M @ p.center
    ob.evaluated_get(dg).to_mesh_clear()
    dim = max(ob.dimensions)

    def cam_setup():
        ST.lighting(1.0)
        cam = ST.camera()
        loc = bc + bn * 6.0
        ST.aim(cam, tuple(loc), tuple(bc), ortho=dim * 1.05)
        ST.setup_render(res=(360, 360), samples=8)
        bpy.context.scene.camera = cam

    res = (360, 360)
    m = _mask_for([ob], os.path.join(OUT, "_solve_mural_mask"), res, cam_setup)
    # erode hard: the target is the board INTERIOR, never its lit rim
    m = erode(m, 13)
    n = int(m.sum())
    if n < 500:
        raise SystemExit("FATAL: mural mask only %d px -- probe cannot see it" % n)

    # THE BOARD ONLY.  The first run of this probe rendered the albedo with the
    # whole scene visible while the MASK was board-only, so the cream lid skin
    # sat between an ortho camera 6 m along -Y and the board and was measured
    # instead of it: albedo read (208, 210, 203).  Exactly the failure mode this
    # file's header warns about, caught by a control rather than by eye.
    restore = _only([ob])
    cam_setup()
    a = _render(os.path.join(OUT, "_solve_mural_alb"), res, 8, albedo=True)
    # the reverse face, as a control: only one side carries the painted image
    def cam_back():
        ST.lighting(1.0)
        cam = ST.camera()
        ST.aim(cam, tuple(bc - bn * 6.0), tuple(bc), ortho=dim * 1.05)
        ST.setup_render(res=res, samples=8)
        bpy.context.scene.camera = cam
    cam_back()
    b = _render(os.path.join(OUT, "_solve_mural_alb_back"), res, 8, albedo=True)
    restore()
    lin = srgb_to_lin(a[..., :3])
    back = srgb_to_lin(b[..., :3])[m].mean(0)
    mean_lin = lin[m].mean(0)
    mean_srgb = lin_to_srgb(mean_lin) * 255.0

    TEX = np.array([127, 59, 23]) / 255.0
    PHOTO = np.array([126, 60, 24]) / 255.0
    tex_lin, photo_lin = srgb_to_lin(TEX), srgb_to_lin(PHOTO)
    bch = lambda v: v[2] / max(1e-9, v.sum())

    _report("mural  T1_MURAL_SPEC=%.4f" % spec, [
        "mask            rendered from the board's own alpha, eroded; %d px" % n,
        "board normal    (%+.4f, %+.4f, %+.4f)" % tuple(bn),
        "ALBEDO PASS     linear (%.5f, %.5f, %.5f)" % tuple(mean_lin),
        "                sRGB   (%.1f, %.1f, %.1f)" % tuple(mean_srgb),
        "                b-chrom %.4f" % bch(mean_lin),
        "TEXTURE target  linear (%.5f, %.5f, %.5f)  sRGB (127, 59, 23)  b-chrom %.4f"
        % (*tex_lin, bch(tex_lin)),
        "PHOTO   target  linear (%.5f, %.5f, %.5f)  sRGB (126, 60, 24)  b-chrom %.4f"
        % (*photo_lin, bch(photo_lin)),
        "REVERSE face (control)  linear (%.5f, %.5f, %.5f)  sRGB (%.1f, %.1f, %.1f)"
        % (*back, *(lin_to_srgb(back) * 255.0)),
        "residual vs texture, linear  (%+.5f, %+.5f, %+.5f)"
        % tuple(mean_lin - tex_lin),
        "residual vs texture, sRGB    (%+.1f, %+.1f, %+.1f)"
        % tuple(mean_srgb - TEX * 255.0),
        "CSV %.4f,%.6f,%.6f,%.6f,%.6f" % (spec, *mean_lin, bch(mean_lin)),
    ])


# ------------------------------------------------------------------ cream --
def solve_cream():
    """Local luminance RMS at 25 mm on the flank cream, render vs photograph.

    The instrument is validated on the PHOTOGRAPH first.  If it cannot
    reproduce the 7.37 % that `ref_side.jpg` is on record for, nothing
    downstream of it is worth quoting, and it says so.
    """
    from PIL import Image
    W_ALB = float(os.environ.get("T1_W_ALB", 0.260))
    LO = float(os.environ.get("T1_W_MAPLO", 0.30))
    HI = float(os.environ.get("T1_W_MAPHI", 0.70))

    def hp_rms(lum, sig_px):
        """RMS of the 25 mm high-pass, as a fraction of the local mean."""
        lo = gblur(lum, sig_px)
        return float(np.sqrt(np.mean(((lum - lo) / np.maximum(lo, 1e-6)) ** 2)))

    rows = []

    # ---- 1. the photograph, as the instrument's calibration -----------------
    ref = np.asarray(Image.open(os.path.join(ROOT, "ref_side.jpg")).convert("RGB"),
                     dtype=np.float64) / 255.0
    PXM_REF = 211.5                      # mid-body, SPEC 10.29
    sig_ref = 0.025 * PXM_REF / 2.0
    # a cream window on the flank ABOVE the belt, aft of the script, forward of
    # the tail -- printed so it can be checked against the frame.
    box = (470, 300, 700, 322)           # (u0, v0, u1, v1)
    crop = ref[box[1]:box[3], box[0]:box[2]]
    lin = srgb_to_lin(crop)
    lum = lin @ np.array([0.2126, 0.7152, 0.0722])
    mx, mn = crop.max(2), crop.min(2)
    sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0.0)
    keep = (sat < 0.30) & (lum > 0.20)
    rows.append("PHOTOGRAPH ref_side.jpg  crop box (u %d-%d, v %d-%d) = %d px, "
                "cream-gated %d px (%.1f %%)"
                % (box[0], box[2], box[1], box[3], crop[..., 0].size,
                   int(keep.sum()), 100.0 * keep.mean()))
    if keep.sum() > 200:
        lum_m = np.where(keep, lum, np.nan)
        filled = np.where(keep, lum, np.nanmean(lum_m))
        rows.append("PHOTOGRAPH 25 mm high-pass RMS  %.3f %%   (on record: 7.37 %%)"
                    % (100.0 * hp_rms(filled, sig_ref)))
    else:
        rows.append("PHOTOGRAPH gate kept too few px -- instrument NOT validated")

    # ---- 2. the render ------------------------------------------------------
    ST.lighting(1.0)
    cam = ST.camera()
    ORTHO = 5.90
    RES = (1248, 858)
    ST.aim(cam, (0.0, 26.0, 1.52), (0.0, 0.0, 1.52), ortho=ORTHO)
    ST.setup_render(res=RES, samples=int(os.environ.get("T1_SOLVE_SAMPLES", 96)))
    bpy.context.scene.camera = cam
    pxm = RES[0] / ORTHO
    sig_r = 0.025 * pxm / 2.0
    a = _render(os.path.join(OUT, "_solve_cream"), RES,
                int(os.environ.get("T1_SOLVE_SAMPLES", 96)))
    lin = srgb_to_lin(a[..., :3])
    lum = lin @ np.array([0.2126, 0.7152, 0.0722])
    mx, mn = a[..., :3].max(2), a[..., :3].min(2)
    sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0.0)
    # cream band on the flank, model frame -> pixels
    v0 = int(RES[1] * 0.5 - (1.62 - 1.52) * pxm)
    v1 = int(RES[1] * 0.5 - (1.30 - 1.52) * pxm)
    u0, u1 = int(RES[0] * 0.5 - 1.15 * pxm), int(RES[0] * 0.5 - 0.30 * pxm)
    sub = slice(v0, v1), slice(u0, u1)
    keep = (sat[sub] < 0.30) & (lum[sub] > 0.20)
    rows.append("RENDER ortho side  %d x %d at %.1f px/m, sigma %.2f px"
                % (*RES, pxm, sig_r))
    rows.append("RENDER crop box (u %d-%d, v %d-%d) = %d px, cream-gated %d px (%.1f %%)"
                % (u0, u1, v0, v1, lum[sub].size, int(keep.sum()), 100.0 * keep.mean()))
    if keep.sum() < 200:
        rows.append("RENDER gate kept too few px -- probe cannot see the cream")
    else:
        L = lum[sub]
        filled = np.where(keep, L, L[keep].mean())
        rms = hp_rms(filled, sig_r)
        rows.append("RENDER 25 mm high-pass RMS   %.3f %%   "
                    "(shipped on record: 1.24 %%; targets 4.22 %% / 7.37 %%)"
                    % (100.0 * rms))
        rows.append("CSV %.4f,%.4f,%.4f,%.6f" % (W_ALB, LO, HI, 100.0 * rms))
    _report("cream  T1_W_ALB=%.3f  window %.2f-%.2f" % (W_ALB, LO, HI), rows)


# ------------------------------------------------------------------- ctan --
def solve_ctan():
    """top/fascia LINEAR ratio in the render, against the photograph's
    (0.796, 0.810, 0.633) +/- 0.02 -- SPEC 10.29.  Both surfaces are in one
    frame under one light, so the light divides out; that is what makes this
    admissible where a same-class albedo ratio was not available."""
    import t1_mats as TM
    tops = _objs_with_material("countertan")
    fasc = _objs_with_material("countercream")
    if not tops or not fasc:
        raise SystemExit("FATAL: countertan %d objs, countercream %d objs"
                         % (len(tops), len(fasc)))
    RES = (760, 520)
    V = ST.views()["counter"]

    def cam_setup():
        # rev 24, SPEC 10.65 -- `studio._softbox` calls bpy.data.lights.new on
        # every invocation and studio.py never removes a light, so ST.lighting()
        # STACKS.  Measured live: 8 / 16 / 24 lights over three calls.  This
        # function is called THREE times (two masks + the measured frame), so
        # every absolute linear figure in SPEC 10.56 -- 0.12107 included -- was
        # read under THREE stacked rigs.  The ratio survives a near-uniform
        # multiplier; the LEVEL and the clipped fraction do not.  Purge first.
        for _l in [o for o in bpy.data.objects if o.type == 'LIGHT']:
            bpy.data.objects.remove(_l, do_unlink=True)
        ST.lighting(1.0)
        cam = ST.camera()
        ST.aim(cam, V["loc"], V["tgt"], lens=V.get("lens"))
        ST.setup_render(res=RES, samples=48)
        bpy.context.scene.camera = cam

    mt = _mask_for(tops, os.path.join(OUT, "_solve_ctan_mt"), RES, cam_setup)
    mf = _mask_for(fasc, os.path.join(OUT, "_solve_ctan_mf"), RES, cam_setup)
    mt, mf = erode(mt, 5), erode(mf, 5)

    # rev 20 -- THE INTERREFLECTION ARM (SPEC 10.31c, five revisions on the
    # list).  10.31c's remaining hypothesis: the top bounces onto the fascia
    # directly below it, so lowering the top's albedo lowers the DENOMINATOR
    # too and the ratio barely moves -- which would explain a secant gain of
    # only 0.33/0.48/0.49.  It is testable in ONE render by taking the top out
    # of the diffuse bounce and re-reading the FASCIA.
    #
    #   T1_CTAN_NOBOUNCE=top     top invisible to diffuse rays
    #   T1_CTAN_NOBOUNCE=fascia  fascia invisible to diffuse rays  (the reverse
    #                            coupling, as its own control)
    #
    # Unset is the shipped arm and touches nothing, so the default render is
    # byte-comparable with every previous ctan run.  `visible_diffuse` removes
    # the object only as a SOURCE of indirect diffuse light; it still renders
    # and still masks, which is exactly the isolation this test needs.
    # rev 20: `top` and `fascia` kill the DIFFUSE path only.  `top_all` /
    # `fascia_all` kill diffuse AND glossy AND transmission, because the
    # counter top carries a coat and a varnished top can light the fascia by a
    # GLOSSY bounce that `visible_diffuse` does not touch.  The two are kept
    # separate on purpose: if they disagree, the difference IS the non-diffuse
    # path, and that is a measurement rather than a preference.
    _nb = os.environ.get("T1_CTAN_NOBOUNCE", "")
    _hidden = []
    if _nb:
        _grp = {"top": tops, "fascia": fasc,
                "top_all": tops, "fascia_all": fasc}.get(_nb, [])
        for _o in _grp:
            _o.visible_diffuse = False
            if _nb.endswith("_all"):
                _o.visible_glossy = False
                _o.visible_transmission = False
                _o.visible_volume_scatter = False
            _hidden.append(_o.name)
        if not _hidden:
            raise SystemExit("FATAL: T1_CTAN_NOBOUNCE=%r matched no object -- "
                             "refusing to report an arm that changed nothing" % _nb)

    # rev 24, SPEC 10.65 -- ISOLATE THE MEASURED FRAME, not only the mask.
    # This is rev 15's own rule (see solve_mural above, and this file's header),
    # never applied here, and it cost four revisions of COUNTERTAN work.  The
    # masks are rendered with `_only` (:175); this frame was rendered with the
    # WHOLE SCENE, so the mask covered pixels with something in FRONT of them
    # and their radiance was attributed to COUNTERTAN.
    #
    # MEASURED with an object-index pass (probe_ctan_index.py, null control
    # IoU 1.0000 / 0 disagreeing px): 33.06 % of the eroded TOP mask and
    # 57.31 % of the FASCIA mask are foreign surfaces -- the largest is
    # `gal_warmer`, and 21.76 % of the fascia mask is `counter_top` itself.
    # 97.84 % of the top mask lies INSIDE the fascia mask, so the un-isolated
    # solve divided a region by a superset of itself.  Correcting it raises the
    # albedo sensitivity k by 40 % in all three channels.
    #
    # T1_CTAN_NOISOLATE=1 reproduces the old contaminated arm, because every
    # figure in SPEC 10.56 was measured that way and must stay reproducible.
    _iso = None
    if os.environ.get("T1_CTAN_NOISOLATE") != "1":
        _iso = _only(list(tops) + list(fasc))
    cam_setup()
    a = _render(os.path.join(OUT, "_solve_ctan" + ("_nb_" + _nb if _nb else "")),
                RES, 48)
    if _iso:
        _iso()
    lin = srgb_to_lin(a[..., :3])
    clipped = float((a[..., :3].max(2) > 0.995).mean())

    t = lin[mt].mean(0)
    f = lin[mf].mean(0)
    ratio = t / np.maximum(f, 1e-9)
    TARGET = np.array([0.796, 0.810, 0.633])
    rg = lambda v: v[0] / max(1e-9, v[1])
    bg = lambda v: v[2] / max(1e-9, v[1])

    _report("ctan  T1_CTAN=%s" % os.environ.get("T1_CTAN", "(built-in %.4f,%.4f,%.4f)"
                                                % TM.COUNTERTAN), [
        "BOUNCE ARM      %s" % ("SHIPPED (nothing hidden)" if not _nb else
                                "%s removed from diffuse bounce: %s"
                                % (_nb, ", ".join(_hidden))),
        "masks           RENDERED from alpha: top %d px, fascia %d px" % (int(mt.sum()), int(mf.sum())),
        "clipped px      %.3f %% of frame at >= 0.995 -- a clipped fascia would "
        "bias the ratio UP" % (100.0 * clipped),
        "top    linear   (%.5f, %.5f, %.5f)" % tuple(t),
        "fascia linear   (%.5f, %.5f, %.5f)" % tuple(f),
        "RATIO  top/fascia  (%.4f, %.4f, %.4f)" % tuple(ratio),
        "TARGET             (%.4f, %.4f, %.4f) +/- 0.02" % tuple(TARGET),
        "residual           (%+.4f, %+.4f, %+.4f)" % tuple(ratio - TARGET),
        "ratio r/g %.4f  (want 1.01-1.03)   b/g %.4f  (want 0.781)"
        % (rg(ratio), bg(ratio)),
        "CSV %.6f,%.6f,%.6f,%.6f,%.6f,%.6f"
        % (*TM.COUNTERTAN, *ratio),
    ])


if MODE == "mural":
    solve_mural()
elif MODE == "cream":
    solve_cream()
elif MODE == "ctan":
    solve_ctan()
else:
    raise SystemExit("T1_SOLVE must be mural | cream | ctan")
