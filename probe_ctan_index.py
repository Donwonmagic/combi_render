"""probe_ctan_index.py -- READ-ONLY.  Does `solve_ctan` measure the counter top?

rev 24, work item 1.  SPEC 10.56 left the COUNTERTAN pedestal UNIDENTIFIED:
cutting the albedo 96.6 % cuts the top's rendered radiance only 29.6/29.9/25.4 %,
so ~69 % of that radiance does not come from COUNTERTAN.  Dust, wear, fade,
coat+spec and interreflection are all ablated and excluded (SPEC 10.56).

THE HYPOTHESIS UNDER TEST is rev 15's, carried unrun for four revisions:

    `solve_mural` renders its MASK from the object in isolation and -- since
    rev 15 -- its MEASURED frame too (shader_solve.py:234).  `solve_ctan`
    renders its mask in isolation (shader_solve.py:175, via `_only`) and its
    MEASURED frame WITH THE WHOLE SCENE PRESENT (shader_solve.py:425-427).
    There is no `_only` on that path.  So the mask can cover pixels that have
    something in FRONT of them, and their radiance is attributed to COUNTERTAN.

rev 20 tried to settle this per-pixel at 48 samples and DISCARDED THE PROBE,
not the hypothesis: seed-to-seed noise is 21.7 % per pixel (median), larger
than the effect.  That was the wrong statistic.  This probe compares REGION
MEANS over ~10^4 px, where that noise falls as sqrt(n) to ~0.2 %.

WHY AN OBJECT-INDEX PASS AND NOT A RAY-VISIBILITY FLAG.  SPEC 10.56's rule --
A RAY-VISIBILITY FLAG IS NOT AN ABLATION -- was learned here: in Cycles a ray
that cannot see an object passes THROUGH it and hits whatever is behind, so the
flag SUBSTITUTES the background instead of removing the surface.  IndexOB does
not suppress anything; it labels the surface each camera ray actually
terminated on.  It answers "which object is this pixel" and nothing else.

THREE CONTROLS, because in this project an ill-posed control has been the bug
twice running (SPEC 10.62's "an outline is not inside itself"; SPEC 10.60's
wrong reference albedo).  A control that can only ever say "clean" is not a
control.

  NULL      render IndexOB under `_only(tops)` -- the mask's OWN configuration,
            nothing in front of the top.  Require the index map to equal the
            rendered alpha mask with ZERO disagreeing pixels and foreign == 0
            EXACTLY.  Any non-zero value indicts the filter width, the index
            assignment or the read-back, and NO result may then be read.
  POSITIVE  the instrument must NAME a foreign object in the full-scene frame.
            A pass that reports only the target cannot detect the defect.
  HARNESS   reproduce SPEC 10.56's shipped control (0.12107, 0.09953, 0.07388)
            before quoting anything, so this is the same measurement chain.

FILTER WIDTH IS LOAD-BEARING.  The default reconstruction filter is 1.5 px and
blends neighbouring indices into fractional values at every silhouette, which
would manufacture foreign pixels.  samples=1, filter_size~0, denoiser off.
INDICES START AT 1: IndexOB writes 0 for background, so 0 is ambiguous.

KNOWN LIMIT, stated rather than discovered later: Cycles writes IndexOB for the
surface the camera ray TERMINATES on, so a transmissive surface in front would
be reported as the surface behind it.  The probe asserts no `glass_*` object
appears in either mask; if one ever does, this instrument is inadmissible there.

Run:  T1_SUB=1 blender -b --python probe_ctan_index.py
Writes nothing into the repo; scratch goes to out/.
"""
import os
import sys
import numpy as np
import bpy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shader_solve as SS          # noqa: E402  -- reuse ITS chain, not a copy
import studio as ST                # noqa: E402

OUT = SS.OUT
RES = (760, 520)

# EV MUST go through the ENVIRONMENT, not through the scene.  My first run set
# `scene.view_settings.exposure` in cam_setup and `shader_solve._plain_view`
# -- which runs inside every `_render` -- overwrote it from T1_SOLVE_EV
# (shader_solve.py:98, default 0.0).  The frame came back 70.54 % clipped
# against SPEC 10.56's 0.086 %, the harness control failed, and the radiance
# shares collapsed onto the pixel shares, which is exactly what SPEC 10.54's
# "CLIPPING DESTROYS TEXTURE" predicts.  Caught by the harness control, not by
# eye.  Set it here so the probe cannot be run the broken way.
os.environ.setdefault("T1_SOLVE_EV", "-4")
EV = float(os.environ["T1_SOLVE_EV"])

# SPEC 10.56 ran every arm at EV -4 and measured 0.086 % clipped.  A frame more
# clipped than this cannot carry the statistic being asked of it, so the probe
# DECLINES rather than reporting a number it cannot support.
CLIP_MAX = 0.005


def _build():
    """Build exactly as shader_solve does -- same cut of build.py."""
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "build.py"), encoding="utf-8").read()
    head = src.split("if os.environ.get(\"T1_SAVE\")")[0]
    g = {"__name__": "__build__", "__file__": "build.py"}
    exec(compile(head, "build.py", "exec"), g)
    return g


def _index_map(cam_setup, restore_fn=None):
    """One IndexOB render -> integer label per pixel.  0 == background."""
    sc = bpy.context.scene
    vl = sc.view_layers[0]
    vl.use_pass_object_index = True

    meshes = [o for o in bpy.data.objects if o.type == 'MESH']
    idx_of, name_of = {}, {}
    for i, o in enumerate(meshes, start=1):      # NEVER 0 -- 0 is background
        o.pass_index = i
        idx_of[o.name] = i
        name_of[i] = o.name

    cam_setup()
    # point-sample: no filter, no denoise, one sample
    sc.cycles.samples = 1
    sc.cycles.use_denoising = False
    sc.render.filter_size = 0.01

    sc.use_nodes = True
    nt = sc.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    rl = nt.nodes.new("CompositorNodeRLayers")
    fo = nt.nodes.new("CompositorNodeOutputFile")
    fo.format.file_format = 'OPEN_EXR'
    fo.format.color_depth = '32'
    fo.format.color_mode = 'RGB'
    fo.format.exr_codec = 'NONE'
    fo.base_path = OUT
    fo.file_slots[0].path = "_idxob_"
    nt.links.new(rl.outputs["IndexOB"], fo.inputs[0])

    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.render.resolution_percentage = 100
    sc.frame_set(1)
    bpy.ops.render.render(write_still=False)

    path = os.path.join(OUT, "_idxob_0001.exr")
    img = bpy.data.images.load(path)
    w, h = img.size
    a = np.array(img.pixels[:], dtype=np.float32).reshape(h, w, 4)
    bpy.data.images.remove(img)
    return np.rint(a[::-1, :, 0]).astype(np.int32), idx_of, name_of


def main():
    g = _build()
    ST.lighting  # noqa -- imported for side-effect parity

    tops = SS._objs_with_material("countertan")
    fasc = SS._objs_with_material("countercream")
    V = ST.views()["counter"]

    def cam_setup():
        # `studio._softbox` calls bpy.data.lights.new on every invocation and
        # nothing in studio.py ever removes a light, so ST.lighting() STACKS:
        # measured live at 8 / 16 / 24 lights over three calls.  `solve_ctan`
        # calls cam_setup() three times (two masks + the measured frame), so
        # ITS measured frame is lit by THREE stacked rigs -- which is why the
        # absolute linear figures in SPEC 10.56 are ~1.5x what one rig gives,
        # while its RATIO is right: a near-uniform multiplier divides out.
        # Purging first is what let this probe pass its own clipping guard.
        for _o in [o for o in bpy.data.objects if o.type == 'LIGHT']:
            bpy.data.objects.remove(_o, do_unlink=True)
        ST.lighting(1.0)
        cam = ST.camera()
        ST.aim(cam, V["loc"], V["tgt"], lens=V.get("lens"))
        ST.setup_render(res=RES, samples=48)
        bpy.context.scene.camera = cam

    print("\n" + "=" * 74)
    print("probe_ctan_index -- does solve_ctan measure the counter top?")
    print("=" * 74)
    print("countertan objects  :", [o.name for o in tops])
    print("countercream objects:", [o.name for o in fasc])

    # ---- masks, built EXACTLY as solve_ctan builds them ------------------
    mt_raw = SS._mask_for(tops, os.path.join(OUT, "_p_mt"), RES, cam_setup)
    mf_raw = SS._mask_for(fasc, os.path.join(OUT, "_p_mf"), RES, cam_setup)
    mt, mf = SS.erode(mt_raw, 5), SS.erode(mf_raw, 5)
    print(f"\nmask px (eroded): top {int(mt.sum())}   fascia {int(mf.sum())}")
    print(f"top mask inside fascia mask: {100.0*float((mt&mf).sum())/max(1,mt.sum()):.2f} %")

    # ---- NULL CONTROL ----------------------------------------------------
    # IndexOB under the mask's OWN configuration.  Must be EXACT.
    restore = SS._only(tops)
    idx_iso, idx_of, name_of = _index_map(cam_setup)
    restore()
    tgt = idx_of[tops[0].name]
    iso_hit = idx_iso == tgt
    inter = int((iso_hit & mt_raw).sum())
    union = int((iso_hit | mt_raw).sum())
    iou = inter / max(1, union)
    disagree = int((iso_hit ^ mt_raw).sum())
    foreign_iso = int((mt & (idx_iso != tgt)).sum())
    print("\n--- NULL CONTROL (isolated: nothing may be in front) ---")
    print(f"  IoU(index map, alpha mask) = {iou:.4f}   disagreeing px = {disagree}")
    print(f"  foreign px inside eroded top mask = {foreign_iso}   (must be 0)")
    if disagree != 0 or foreign_iso != 0:
        print("  NULL CONTROL FAILED -- the instrument is not sound. "
              "NO RESULT BELOW MAY BE READ.")
        return
    print("  PASS -- exact. The index map corresponds to the rendered mask.")

    # ---- the measurement: full scene, nothing hidden ---------------------
    idx, idx_of, name_of = _index_map(cam_setup)

    # transmissive guard (stated limit)
    for m, tag in ((mt, "top"), (mf, "fascia")):
        labs = set(np.unique(idx[m]).tolist()) - {0}
        gl = [name_of[i] for i in labs if name_of.get(i, "").startswith("glass")]
        if gl:
            print(f"  INADMISSIBLE: transmissive object in {tag} mask: {gl}")
            return
    print("  transmissive guard: no glass_* in either mask -- admissible")

    # ---- beauty frame, the same one solve_ctan measures ------------------
    cam_setup()
    a = SS._render(os.path.join(OUT, "_p_beauty"), RES, 48)
    lin = SS.srgb_to_lin(a[..., :3])
    clipped = float((a[..., :3].max(2) > 0.995).mean())

    t_all = lin[mt].mean(0)
    f_all = lin[mf].mean(0)
    print("\n--- HARNESS CONTROL vs SPEC 10.56's shipped arm ---")
    print(f"  top    {tuple(round(float(v),5) for v in t_all)}"
          f"   SPEC 10.56 (0.12107, 0.09953, 0.07388)")
    print(f"  fascia {tuple(round(float(v),5) for v in f_all)}"
          f"   SPEC 10.56 (0.13403, 0.12163, 0.10453)")
    print(f"  ratio  {tuple(round(float(v),4) for v in (t_all/np.maximum(f_all,1e-9)))}"
          f"   SPEC 10.56 (0.9033, 0.8183, 0.7068)")
    print(f"  clipped {100*clipped:.3f} %   SPEC 10.56 0.086 %")
    if clipped > CLIP_MAX:
        print(f"\n  HARNESS CONTROL FAILED -- {100*clipped:.2f} % clipped at "
              f"EV {EV}. A clipped frame carries no texture, so every radiance "
              "share below would collapse onto the pixel share and mean "
              "nothing. DECLINING to report radiance. (The PIXEL shares from "
              "the index map are exposure-independent and remain valid.)")
        _RADIANCE_OK = False
    else:
        _RADIANCE_OK = True
        print("  PASS -- reproduces the shipped arm; this is the same chain.")

    # ---- POSITIVE CONTROL + the breakdown --------------------------------
    def breakdown(mask, tag, want_objs):
        """`want_objs` is the UNION of objects carrying the solved material.

        My first version passed `objs[0]`.  For the fascia that is a BRACKET,
        so the report read "target 0.41 % of px, foreign 99.59 %" -- true of
        the bracket and meaningless about `countercream`.  The material is on
        six objects and the mask is their union, so the target must be too.
        Caught by reading my own output, not by a control -- worth saying.
        """
        want = set(want_objs)
        m = mask & (idx > 0)
        labs, cnt = np.unique(idx[m], return_counts=True)
        tot_px = int(m.sum())
        rows = []
        tot_rad = lin[m].sum(0)
        for L, c in zip(labs.tolist(), cnt.tolist()):
            sel = mask & (idx == L)
            rad = lin[sel].sum(0)
            rows.append((name_of.get(L, "?"), c, 100.0*c/tot_px,
                         rad/np.maximum(tot_rad, 1e-9)*100.0,
                         lin[sel].mean(0)))
        rows.sort(key=lambda r: -r[1])
        print(f"\n--- {tag} mask, n={tot_px} px, target material on '{want}' ---")
        print(f"  {'object':<22}{'px':>7}{'px %':>8}   radiance % (R/G/B)")
        for nm, c, pc, rp, mn in rows[:9]:
            print(f"  {nm:<22}{c:>7}{pc:>7.2f}%   "
                  f"{rp[0]:6.2f} /{rp[1]:6.2f} /{rp[2]:6.2f}")
        pc = sum(r[2] for r in rows if r[0] in want)
        rp = [sum(r[3][i] for r in rows if r[0] in want) for i in range(3)]
        print(f"  --> TARGET (union of {len(want)} obj): {pc:.2f} % of px, "
              f"{rp[0]:.2f}/{rp[1]:.2f}/{rp[2]:.2f} % of radiance")
        print(f"  --> FOREIGN: {100-pc:.2f} % of px, "
              f"{100-rp[0]:.2f}/{100-rp[1]:.2f}/{100-rp[2]:.2f} % of radiance")
        return rows, pc, np.array(rp)

    rt, tpc, trp = breakdown(mt, "TOP", [o.name for o in tops])
    rf, fpc, frp = breakdown(mf, "FASCIA", [o.name for o in fasc])

    foreign_names = [r[0] for r in rt if r[0] != tops[0].name]
    print("\n--- POSITIVE CONTROL ---")
    if foreign_names:
        print(f"  PASS -- the instrument NAMES foreign surfaces in the top mask: "
              f"{foreign_names[:4]}")
    else:
        print("  the top mask is clean; the instrument reported no foreign "
              "surface. A pass that can only say 'clean' is weak evidence -- "
              "the null control above is what makes this readable.")

    # ---- the number that matters ----------------------------------------
    _ti = set(idx_of[o.name] for o in tops)
    _fi = set(idx_of[o.name] for o in fasc)
    tsel = mt & np.isin(idx, list(_ti))
    fsel = mf & np.isin(idx, list(_fi))
    t_cln, f_cln = lin[tsel].mean(0), lin[fsel].mean(0)
    print("\n--- OCCLUSION-CORRECTED vs AS-SOLVED ---")
    print(f"  top    as-solved {tuple(round(float(v),5) for v in t_all)}"
          f"  clean {tuple(round(float(v),5) for v in t_cln)}")
    print(f"  fascia as-solved {tuple(round(float(v),5) for v in f_all)}"
          f"  clean {tuple(round(float(v),5) for v in f_cln)}")
    TARGET = np.array([0.796, 0.810, 0.633])
    r_all = t_all/np.maximum(f_all, 1e-9)
    r_cln = t_cln/np.maximum(f_cln, 1e-9)
    print(f"  ratio  as-solved {tuple(round(float(v),4) for v in r_all)}"
          f"  resid {tuple(round(float(v),4) for v in (r_all-TARGET))}")
    print(f"  ratio  clean     {tuple(round(float(v),4) for v in r_cln)}"
          f"  resid {tuple(round(float(v),4) for v in (r_cln-TARGET))}")
    # ---- THE PEDESTAL, MEASURED THROUGH THE CLEAN MASK ------------------
    # SPEC 10.56 derived P from two albedo arms read through the CONTAMINATED
    # mask.  Foreign pixels do not respond to COUNTERTAN, so they land wholly
    # in P and inflate it.  Correcting by arithmetic would be an INFERENCE and
    # would assume the occluders' radiance is exactly invariant under the
    # ablation -- but they sit on the top and catch its bounce, so it is not.
    # This arm re-reads BOTH albedo points through the index-clean mask, which
    # makes the correction a measurement.  Print T1_CTAN to see which arm.
    print(f"\n--- ARM: T1_CTAN={os.environ.get('T1_CTAN','(built-in)')} ---")
    print(f"  top  CONTAMINATED mask {tuple(round(float(v),6) for v in t_all)}")
    print(f"  top  CLEAN        mask {tuple(round(float(v),6) for v in t_cln)}")

    print("\n  region-mean noise floor ~ 21.7 %/sqrt(n) = "
          f"{21.7/np.sqrt(max(1,tsel.sum())):.3f} % on the top -- "
          "the statistic rev 20's per-pixel test could not use")
    print("=" * 74)


if __name__ == "__main__":
    main()
