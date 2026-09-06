"""
sticker_pass.py -- the 3D CAPTURE half of F18, the die-cut sticker.

WHY THIS EXISTS.  F18 is the project's original deliverable and the register's
oldest live row.  Its trigger fired at rev 77 (F330: *"Yes -- start it now"*),
and its STYLE IS LOCKED to the owner's own recovered sentence:

    "cartoon with rendered depth -- vector line and flat colour,
     shading and occlusion sampled from the 3D asset"

That sentence names THREE things and rev 77 built ONE of them.  `line_pass.py`
is the vector line.  This module is the other two: FLAT COLOUR and SHADING /
OCCLUSION, and the word that matters in both is SAMPLED -- from the asset, not
invented by a draughtsman.  Nothing here draws.  It captures, and `sticker.py`
draws from what it captured.

WHAT IT CAPTURES, AND WHY EACH IS AN EXACT INSTRUMENT RATHER THAN A GUESS
------------------------------------------------------------------------
1. THE INK MASKS.  One binary matte per INK FAMILY, via Cycles' Material Index
   pass through an ID Mask node.  This is an INTEGER pass: a pixel either
   carries material index k or it does not.  The obvious alternative -- render
   the beauty frame and threshold it by colour -- is exactly the defect rule 8
   is about, because a shaded red panel and a lit gold letter overlap in RGB
   and the window would select the wrong pixels while printing a plausible
   number.  A material index cannot do that.

2. THE ALBEDO, BECAUSE THE NODE TREE CANNOT BE ASKED.  ⚠ AN EARLIER DRAFT OF
   THIS LIST SAID the families were read off each material's Principled Base
   Color.  THAT METHOD IS RETRACTED -- see `base_colour_survey()` below and
   F351: the socket is LINKED on 22 of this asset's 45 materials, `T1_paint`
   among them, so the read returned the UNCONNECTED DEFAULT and `ink_red` came
   out empty on a bus that is mostly red.  What this module captures is the
   RENDERED ALBEDO plus the material-index map; classification happens
   downstream in `sticker.py`, off an AUTHORED palette keyed on material
   identity, under the owner's rev-78 ruling (F346).  `base_colour_survey()`
   survives only as the DIAGNOSTIC that counts how many materials could never
   have been classified that way.

3. THE SILHOUETTE.  The alpha of a transparent-film render -- the die-cut path.
   F161 established `deliver.py`'s trimmed output is this geometry; here it is
   captured at the sticker's own camera rather than a delivery camera.

4. THE SHADING TERM.  Combined / DiffuseColor, per pixel, in LINEAR light.
   Dividing the beauty pass by the albedo pass removes the paint and leaves the
   LIGHT -- which is what "shading sampled from the 3D asset" means.  Reading
   the beauty pass alone would confound shading with the paint it falls on: a
   cream panel in shadow and a red panel in sun can carry the same luminance,
   and a drawing banded off that would put a shadow where a colour change is.
   `photometry.py`'s rules apply and are imported, not re-derived: READ LINEAR,
   REFUSE CLIPPED, MEDIAN NOT MEAN.

5. THE OCCLUSION TERM.  Cycles' Ambient Occlusion pass, which is contact
   darkening only and is INDEPENDENT of the light rig -- so a contact shadow
   under the arch survives a change of key light.  If the pass is unavailable
   this module REFUSES rather than substituting the shading term for it
   (rule 37: an absent input must never read as a measurement).

CEILINGS, STATED (rule 12)
--------------------------
  * THE VIEW IS A POSE, NOT A MEASUREMENT -- BUT LESS OF ONE THAN REV 78's
    FIRST DRAFT CLAIMED, AND THAT CLAIM IS RETRACTED HERE (rule 13).
    `AUDIT_rev43.md`'s row reads *"VIEWPOINT -- 18 deg front three-quarter
    from the serving side, eye height 1.55 m.  The face and the flank are
    provably exclusive; choose the flank."*  I wrote that this row was one of
    the eight hard-cut at 120 characters and that the disambiguating sentence
    did not survive.  **THAT IS FALSE.**  MEASURED: the DESIGN cell is 142
    characters and ends in a FULL STOP.  What is hard-cut at 120 is a
    DIFFERENT COLUMN -- the trailing symbol list -- on all eight rows, and
    only rows 2 (the cab door) and 8 (colour separation) end mid-thought, at
    149 and 150 characters.
    So the record DOES answer the face/flank question: *choose the flank*.
    The only genuine residual is WHICH AXIS the 18 deg is measured from, and
    the flank reading (azimuth 72 deg) is the one consistent with the
    surviving sentence.  This module defaults to it for that reason, not
    because the question is open.  `--az 18` renders the nose reading, which
    the record EXCLUDES; it is kept only as the painted evidence for that.
    Nothing may quote 18 deg itself as measured.
  * `T1_SUB` matters.  The masks and the line pass MUST be baked at the same
    subdivision or the line will not sit on its own colour.
  * Cycles is not run-to-run deterministic (the brief's ~2.04 % floor), but an
    ID MASK is: it is an integer comparison, not a light transport estimate.
    The SHADING and OCCLUSION terms are NOT exempt and are sampled accordingly.
"""
import os, sys, json, math, time

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "probe_scratch", "sticker")

# The sticker's own view.  Kept HERE and not in `studio.views()` on purpose:
# it is a POSE recovered from a TRUNCATED spec row, and `studio.views()` is
# where MEASURED cameras live (the reference-photo solve, the delivery frame).
# Mixing the two is how a pose becomes a measurement by adjacency.
EYE_Z = 1.55            # the spec row's own figure, and the only one it gives
AZ_FLANK = 72.0         # 18 deg off the FLANK -- the default reading
AZ_NOSE = 18.0          # 18 deg off the NOSE  -- the alternative, for the owner
LENS = 78               # SPEC 10.8 locks the lens; the distance is what moves
SHADE_HEADROOM = 4.0    # see capture(): keeps the light term off the ceiling


def log(*a):
    print(*a); sys.stdout.flush()


# --------------------------------------------------------------- ink families
def srgb(lin):
    """Linear -> 8-bit sRGB.  DERIVED, never transcribed: t1_mats' comments
    carry sRGB triples beside the linear constants and a comment is not a
    measurement (rule 10)."""
    def f(c):
        c = max(0.0, min(1.0, float(c)))
        return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
    return tuple(int(round(f(c) * 255)) for c in lin[:3])


def hue_chroma(lin):
    r, g, b = (max(0.0, float(c)) for c in lin[:3])
    mx, mn = max(r, g, b), min(r, g, b)
    c = mx - mn
    if c <= 1e-9 or mx <= 1e-9:
        return 0.0, 0.0
    if mx == r:
        h = 60.0 * (((g - b) / c) % 6)
    elif mx == g:
        h = 60.0 * ((b - r) / c + 2)
    else:
        h = 60.0 * ((r - g) / c + 4)
    return h, c / mx                       # hue in degrees, chroma as saturation


def base_colour(mat):
    """The material's own Base Color, read off its node tree.  Returns None for
    a material with no Principled surface -- glass, the lens, the reflector --
    which is a REFUSAL, not a zero."""
    if not mat or not mat.use_nodes:
        return None
    for n in mat.node_tree.nodes:
        if n.type == "BSDF_PRINCIPLED":
            return tuple(n.inputs["Base Color"].default_value)[:3]
    for n in mat.node_tree.nodes:
        if n.type == "EMISSION":
            return tuple(n.inputs["Color"].default_value)[:3]
    return None


def base_colour_survey(log=log):
    """HOW MANY MATERIALS CANNOT BE CLASSIFIED FROM THEIR NODE TREE AT ALL.

    ⚠ THIS IS A DIAGNOSTIC, NOT THE CLASSIFIER, AND rev 78's FIRST DRAFT USED
    IT AS THE CLASSIFIER AND WAS WRONG.  Reading `Base Color.default_value`
    returns the UNCONNECTED default whenever the socket is LINKED -- and 22 of
    this asset's 45 materials link it, `T1_paint` (the body red) and `cream`
    among them.  The result was an `ink_red` mask that was nearly EMPTY on a
    bus that is mostly red, while every count it fed printed a plausible
    number.  It was caught by PAINTING THE MASK AND LOOKING AT IT (rule 8),
    never by reasoning about the code.

    The real classification is done downstream from the RENDERED ALBEDO
    (`DiffCol`), per material index -- see `sticker.py :: classify`.  A
    texture, a mix, a ramp and a flat value all reduce to the same thing
    there, because it is the colour the renderer actually put on the pixel.
    """
    import bpy
    linked, flat, none_ = [], [], []
    for mat in bpy.data.materials:
        if not mat.use_nodes:
            none_.append(mat.name); continue
        pr = [n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"]
        if not pr:
            none_.append(mat.name); continue
        (linked if pr[0].inputs["Base Color"].is_linked else flat).append(mat.name)
    log("  base-colour survey: %d material(s) LINK Base Color (a node read "
        "would be wrong on every one), %d are flat, %d have no Principled"
        % (len(linked), len(flat), len(none_)))
    return sorted(linked), sorted(flat), sorted(none_)


# ------------------------------------------------------------------ the camera
def fit_camera(az_deg, log=log):
    """Frame the whole vehicle at `az_deg` from the nose axis, eye height 1.55.

    The DISTANCE is solved from the built mesh's own bounding sphere and the
    locked 78 mm lens, so it cannot go stale when the vehicle changes.  It is
    not a spec figure and is not published as one.
    """
    import bpy
    from mathutils import Vector
    import studio as ST
    pts = []
    for o in bpy.data.objects:
        if o.type != "MESH" or not o.visible_get():
            continue
        for c in o.bound_box:
            pts.append(o.matrix_world @ Vector(c))
    if not pts:
        raise SystemExit("REFUSE: no visible mesh to frame")
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    ctr = (lo + hi) * 0.5
    rad = max((p - ctr).length for p in pts)
    half = math.atan(ST.SENSOR_W * 0.5 / LENS)          # horizontal half-angle
    dist = rad / math.sin(half) * 1.06                  # 6 % air, both axes
    a = math.radians(az_deg)
    loc = (ctr.x + dist * math.cos(a), ctr.y + dist * math.sin(a), EYE_Z)
    tgt = (ctr.x, ctr.y, ctr.z)
    log("  bbox centre (%.3f, %.3f, %.3f) radius %.3f m -> distance %.3f m at "
        "%.1f deg azimuth, eye z %.2f (POSE, not a measurement)"
        % (ctr.x, ctr.y, ctr.z, rad, dist, az_deg, EYE_Z))
    return loc, tgt, dist, rad


# ------------------------------------------------------------------- the bake
def capture(az_deg, res, samples, tag, log=log):
    import bpy
    import studio as ST
    os.makedirs(OUT, exist_ok=True)

    sc = ST.setup_render(res, samples, True)            # transparent film

    # ⚠ RAW VIEW TRANSFORM, AND THIS IS NOT COSMETIC.  Blender 4.x defaults to
    # AgX, a DISPLAY transform, and a File Output node applies it on the way
    # out.  Every pass here is DATA, not a picture: an albedo bent by AgX is
    # not the paint, and rev 78's first proof came out with an ORANGE bus and
    # a tan mural because of exactly this -- while all 32 checks passed, since
    # the numbers stayed self-consistent.  Caught by LOOKING at the proof.
    # It also crushed the light term: the shading banding found NOTHING.
    sc.view_settings.view_transform = "Raw"
    sc.view_settings.look = "None"
    sc.display_settings.display_device = "sRGB"
    log("  view transform forced to Raw -- these passes are DATA, and AgX is "
        "a display transform (it turned the red paint orange on the first "
        "proof while every check still passed)")
    cam = ST.camera()
    loc, tgt, dist, rad = fit_camera(az_deg, log=log)
    ST.aim(cam, loc, tgt, lens=LENS, fstop=0.0)         # no DOF: a sticker is flat
    sc.camera = cam
    sc.frame_start = sc.frame_end = sc.frame_current = 1

    linked, flat, nonp = base_colour_survey(log=log)
    # ONE INDEX PER MATERIAL.  Grouping into families HERE would bake a
    # classification into the capture; done downstream it can be recomputed,
    # argued with, and ablated without re-rendering.
    names = sorted(m.name for m in bpy.data.materials)
    idx = {n: i + 1 for i, n in enumerate(names)}       # 0 = no material
    if len(names) > 250:
        raise SystemExit("REFUSE: %d materials will not survive an 8-bit "
                         "index round-trip" % len(names))
    for mat in bpy.data.materials:
        mat.pass_index = idx[mat.name]

    vl = sc.view_layers[0]
    vl.use_pass_material_index = True
    vl.use_pass_diffuse_color = True
    ao_ok = True
    try:
        vl.use_pass_ambient_occlusion = True
    except (AttributeError, TypeError):
        ao_ok = False
    if ao_ok:
        # Cycles computes the AO pass only when it is allowed bounces.
        try:
            sc.cycles.ao_bounces_render = max(1, int(sc.cycles.ao_bounces_render or 1))
        except AttributeError:
            pass
    log("  AO pass %s" % ("ENABLED" if ao_ok else
                          "UNAVAILABLE -- this build REFUSES rather than "
                          "substituting the shading term (rule 37)"))

    sc.use_nodes = True
    nt = sc.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    rl = nt.nodes.new("CompositorNodeRLayers")
    rl.scene = sc
    rl.layer = vl.name

    def out_node(name, sockname, fmt="PNG", depth="16"):
        fo = nt.nodes.new("CompositorNodeOutputFile")
        fo.base_path = OUT
        fo.format.file_format = fmt
        fo.format.color_mode = "BW" if fmt == "PNG" else "RGBA"
        fo.format.color_depth = depth
        fo.file_slots[0].path = "%s_%s_" % (tag, name)
        try:
            nt.links.new(rl.outputs[sockname], fo.inputs[0])
        except KeyError:
            nt.nodes.remove(fo)
            return None
        return fo

    made = {}
    # -- THE INDEX MAP.  IndexMA carries small integers; scaled by 1/255 into a
    #    16-bit container it round-trips EXACTLY (index k -> round(v*65535)
    #    = k*257), so `sticker.py` recovers the material of every pixel with no
    #    threshold and no antialiasing to blur two materials into one.
    sc16 = nt.nodes.new("CompositorNodeMixRGB")
    sc16.blend_type = "MULTIPLY"
    sc16.inputs[0].default_value = 1.0
    sc16.inputs[2].default_value = (1.0 / 255.0,) * 3 + (1.0,)
    nt.links.new(rl.outputs["IndexMA"], sc16.inputs[1])
    fo = nt.nodes.new("CompositorNodeOutputFile")
    fo.base_path = OUT
    fo.format.file_format = "PNG"
    fo.format.color_mode = "BW"
    fo.format.color_depth = "16"
    fo.file_slots[0].path = "%s_index_" % tag
    nt.links.new(sc16.outputs[0], fo.inputs[0])
    made["index"] = True

    # -- THE ALBEDO.  The paint the renderer actually laid down, texture and
    #    all -- which is what makes the ink classification immune to how a
    #    material happens to be wired.
    fo = nt.nodes.new("CompositorNodeOutputFile")
    fo.base_path = OUT
    fo.format.file_format = "PNG"
    fo.format.color_mode = "RGB"
    fo.format.color_depth = "16"
    fo.file_slots[0].path = "%s_albedo_" % tag
    nt.links.new(rl.outputs["DiffCol"], fo.inputs[0])
    made["albedo"] = True

    # -- the silhouette: the film's own alpha
    fo = nt.nodes.new("CompositorNodeOutputFile")
    fo.base_path = OUT
    fo.format.file_format = "PNG"
    fo.format.color_mode = "BW"
    fo.format.color_depth = "8"
    fo.file_slots[0].path = "%s_alpha_" % tag
    nt.links.new(rl.outputs["Alpha"], fo.inputs[0])
    made["alpha"] = True

    # -- shading = Combined / DiffCol, in LINEAR light.
    #
    #    WHY 16-BIT PNG AND NOT EXR.  Neither PIL nor numpy reads OpenEXR on a
    #    bootstrapped clone, so an EXR here would be a file nothing downstream
    #    could open -- an absent input wearing the costume of a present one
    #    (rule 37).  A 16-bit PNG is readable everywhere and carries 65536
    #    levels, which is far finer than the handful of flat bands a cartoon
    #    quantises to.
    #
    #    WHY THE HEADROOM DIVISOR.  Combined/DiffCol is a LIGHT term and is not
    #    bounded by 1 -- a specular hit runs past it -- so writing it straight
    #    into a [0,1] container would CLIP, and photometry.py's standing rule
    #    is REFUSE CLIPPED.  Dividing by SHADE_HEADROOM first makes the write
    #    lossless up to that value and exactly invertible downstream; the
    #    fraction that still pins at the top is COUNTED and reported by
    #    sticker.py rather than silently absorbed.
    div = nt.nodes.new("CompositorNodeMixRGB")
    div.blend_type = "DIVIDE"
    div.inputs[0].default_value = 1.0
    nt.links.new(rl.outputs["Image"], div.inputs[1])
    nt.links.new(rl.outputs["DiffCol"], div.inputs[2])
    hr = nt.nodes.new("CompositorNodeMixRGB")
    hr.blend_type = "MULTIPLY"
    hr.inputs[0].default_value = 1.0
    hr.inputs[2].default_value = (1.0 / SHADE_HEADROOM,) * 3 + (1.0,)
    nt.links.new(div.outputs[0], hr.inputs[1])
    fo = nt.nodes.new("CompositorNodeOutputFile")
    fo.base_path = OUT
    fo.format.file_format = "PNG"
    fo.format.color_mode = "BW"
    fo.format.color_depth = "16"
    fo.file_slots[0].path = "%s_shade_" % tag
    nt.links.new(hr.outputs[0], fo.inputs[0])
    made["shade"] = True

    # -- occlusion.  AO is natively bounded [0,1], so it needs no headroom and
    #    is written straight.  If Cycles will not give the pass, NOTHING is
    #    written and `ao` is recorded False -- sticker.py then refuses to draw
    #    an occlusion layer rather than passing the shading term off as one.
    if ao_ok and "AO" in [x.name for x in rl.outputs]:
        fo = nt.nodes.new("CompositorNodeOutputFile")
        fo.base_path = OUT
        fo.format.file_format = "PNG"
        fo.format.color_mode = "BW"
        fo.format.color_depth = "16"
        fo.file_slots[0].path = "%s_ao_" % tag
        nt.links.new(rl.outputs["AO"], fo.inputs[0])
        made["ao"] = True
    else:
        made["ao"] = False
        log("  NO AO PASS WRITTEN -- the occlusion half of the owner's style "
            "sentence is UNBUILT for this capture, and sticker.py will say so "
            "on the artefact rather than substituting shading for it")

    t0 = time.time()
    bpy.ops.render.render(write_still=False)
    log("  rendered %dx%d at %d spp in %.1f s" % (res[0], res[1], samples,
                                                  time.time() - t0))

    meta = dict(tag=tag, az=az_deg, eye_z=EYE_Z, lens=LENS, res=list(res),
                samples=samples, dist=dist, radius=rad, loc=list(loc), tgt=list(tgt),
                index={n: idx[n] for n in names}, ao=made.get("ao", False),
                shade_headroom=SHADE_HEADROOM,
                base_colour_linked=linked, base_colour_flat=flat,
                base_colour_none=nonp,
                sub=os.environ.get("T1_SUB", ""),
                note=("the 18 deg viewpoint is a POSE recovered from a "
                      "TRUNCATED spec row and admits two readings; see the "
                      "module docstring"))
    open(os.path.join(OUT, "%s_meta.json" % tag), "w").write(
        json.dumps(meta, indent=1, sort_keys=True))
    log("  wrote %s" % os.path.join(OUT, "%s_meta.json" % tag))
    return meta


def main(argv):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--az", type=float, default=AZ_FLANK,
                    help="camera azimuth in degrees off the NOSE axis. "
                         "%.0f = the flank reading of the spec's 18 deg "
                         "(default); %.0f = the nose reading." % (AZ_FLANK, AZ_NOSE))
    ap.add_argument("--tag", default=None)
    ap.add_argument("--rx", type=int, default=1400)
    ap.add_argument("--ry", type=int, default=1000)
    ap.add_argument("--samples", type=int, default=48)
    ap.add_argument("--sub", type=int, default=None)
    ap.add_argument("--lines", action="store_true",
                    help="also bake the line pass at THIS camera")
    a = ap.parse_args(argv)
    tag = a.tag or ("flank" if abs(a.az - AZ_FLANK) < 1e-6 else
                    "nose" if abs(a.az - AZ_NOSE) < 1e-6 else "az%g" % a.az)

    import line_pass as LP
    log("sticker_pass -- F18 capture, tag %r, azimuth %.1f deg" % (tag, a.az))
    LP.build_scene(a.sub)
    meta = capture(a.az, (a.rx, a.ry), a.samples, tag)

    if a.lines:
        log("  line pass at the SAME camera -- baked THROUGH it, not re-aimed "
            "afterwards: CONTOUR strokes are the silhouette and are "
            "view-dependent")
        gp, cam2, sc = LP.bake(res=(a.rx, a.ry), log=log,
                               cam_override=(meta["loc"], meta["tgt"], LENS))
        strokes = LP.project(gp, cam2, sc, log=log)
        p = os.path.join(OUT, "%s_lines.json" % tag)
        open(p, "w").write(json.dumps(
            dict(meta=meta, strokes=strokes), separators=(",", ":")))
        log("  wrote %s (%d stroke(s))" % (p, len(strokes)))
    log("DONE %s" % tag)


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:])
