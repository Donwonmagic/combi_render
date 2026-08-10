"""white cyclorama studio, PHYSICAL camera, lighting rig, render driver

rev 7 -- the camera was a pinhole with infinite depth of field and the rig was
six neutral rectangles. Both are loud CGI tells at hero resolution:

  * A pinhole renders the tail as sharp as the near arch. No lens does that.
    The camera now has a real sensor size, a real focal length and a real
    f-number, and focuses on the near front arch. Every view logs its measured
    near/far DoF limits so the depth falloff is a number, not a claim.
  * Six rectangles each draw a short specular blob and the eye reads blobs as
    plastic. One long narrow source draws a CONTINUOUS streak that runs the
    length of the flank and bends where the panel curves -- which is what
    actually says "sheet metal". Still large and soft per SPEC sec.6; it just
    has an aspect ratio now.
  * A render with no lens or film artefacts at all reads as synthetic even when
    everything else is right. Restrained chromatic aberration, vignette, bloom
    on the brightest speculars and fine grain are added in the compositor, in
    the order a real camera imposes them.

Every effect is switchable from the environment so any of it can be A/B'd or
zeroed without editing code. T1_FX=0 disables the whole optics chain.
"""
import bpy, math, os
from mathutils import Vector


def _envf(k, d):
    return float(os.environ.get(k, d))


def _envi(k, d):
    return int(float(os.environ.get(k, d)))


# --------------------------------------------------------------------- clay
def clay_all(rgb=(0.62, 0.62, 0.63)):
    m = bpy.data.materials.get("__clay")
    if not m:
        m = bpy.data.materials.new("__clay")
        m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (*rgb, 1)
        b.inputs["Roughness"].default_value = 0.40
        b.inputs["Specular IOR Level"].default_value = 0.35
    for ob in bpy.data.objects:
        if ob.type == 'MESH':
            ob.data.materials.clear()
            ob.data.materials.append(m)


def cyclorama(size=90.0, **kw):
    """
    Flat shadow-catching ground.  Deliberately NOT a curved cyc wall: a wall
    sits between the subject and any orthographic camera placed outside it,
    which is what blanked the front elevation.  Background comes from the
    compositor (pure white) instead.
    """
    me = bpy.data.meshes.new("cyc")
    h = size / 2
    me.from_pydata([(-h, -h, 0), (h, -h, 0), (h, h, 0), (-h, h, 0)], [],
                   [(0, 1, 2, 3)])
    me.validate()
    ob = bpy.data.objects.new("cyc", me)
    bpy.context.collection.objects.link(ob)
    mat = bpy.data.materials.new("cyc_white")
    mat.use_nodes = True
    b = mat.node_tree.nodes["Principled BSDF"]
    # rev 8: was 0.94 -- near-PTFE. A real studio sweep is 0.70-0.80, and at
    # 0.94 the floor bounced enough NEUTRAL light back up the flank to be the
    # single largest desaturator in the scene. See the saturation experiment in
    # SPEC 10.9.
    b.inputs["Base Color"].default_value = (float(os.environ.get("T1_CYCALB", 0.76)),) * 3 + (1,)
    b.inputs["Roughness"].default_value = 0.68
    b.inputs["Specular IOR Level"].default_value = 0.20
    ob.data.materials.append(mat)
    ob.is_shadow_catcher = True
    return ob


# ----------------------------------------------------------------- lighting
def _softbox(name, loc, aim_at, size, power, colour=(1, 1, 1), spread=None):
    d = bpy.data.lights.new(name, 'AREA')
    d.shape = 'RECTANGLE'
    d.size, d.size_y = size
    d.energy = power
    d.color = colour
    if spread is not None:                     # narrow spread = crisper streak
        d.spread = math.radians(spread)
    o = bpy.data.objects.new(name, d)
    bpy.context.collection.objects.link(o)
    o.location = loc
    v = Vector(aim_at) - Vector(loc)
    o.rotation_euler = v.to_track_quat('-Z', 'Y').to_euler()
    return o


def lighting(key=1.0):
    """
    One long raking strip carries the image; everything else is support.

    The strip is 16 m long and 0.55 m deep, sitting high on the show side and
    raking down the flank. Its reflection is a single unbroken highlight that
    tracks the body's shoulder line from nose to tail and pinches where the
    panel turns -- the read that says "this is a curved metal surface" rather
    than "this is a shaded polygon". Its spread is narrowed so the streak has
    an edge; a full 180 deg area light washes and the streak dissolves.
    """
    c = Vector((0, 0, 1.0))

    # --- the hero source ------------------------------------------------
    _softbox("strip", (0.85, 8.30, 5.90), (0.00, 0.55, 1.28),
             (16.0, 0.55), 511.5 * key, (1.0, 0.998, 0.992), spread=78)
    # a second, much shorter and lower strip picks out the counter lip and the
    # louvre block, which the high strip rakes straight over
    _softbox("strip_lo", (1.60, 7.40, 1.95), (-0.80, 0.60, 1.05),
             (7.5, 0.34), 77.5 * key, (1.0, 0.995, 0.985), spread=92)

    # --- support --------------------------------------------------------
    _softbox("top",   (0.6, 1.2, 8.6), (0, 0, 1.3), (13.0, 8.5), 305.3 * key)
    _softbox("fillR", (2.4, -9.0, 2.4), (0, 0, 1.1), (9.0, 3.6), 92.4 * key,
             (0.975, 0.985, 1.0))
    _softbox("rim",   (-9.2, 3.4, 4.2), c, (5.0, 4.0), 145.2 * key)
    _softbox("nose",  (10.6, 1.6, 1.5), (1.6, 0.0, 1.05), (3.2, 2.6),
             39.6 * key)
    # SPEC r4 sec.6 (old D4): the galley is a closed 2.8 mm box lit only by
    # EXTERIOR sources, so the three serving hatches rendered as flat black
    # holes. This sits just outboard of the show flank and rakes into the bays
    # so the openings read as depth. Small and dim: it must not spill onto the
    # paint or wash the contact shadow.
    _softbox("fill_galley", (-0.35, 2.35, 1.58), (-0.35, 0.0, 1.47),
             (1.7, 0.55), 10.2 * key, (1.0, 0.965, 0.915))

    w = bpy.data.worlds.new("w")
    bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
    # cut from 0.30: a bright white world dumps achromatic fill into every
    # shadow and desaturates the paint (SPEC rev4 sec.3)
    # rev 8: 0.17 -> 0.05. Pure achromatic fill landing on saturated paint.
    w.node_tree.nodes["Background"].inputs[1].default_value = float(
        os.environ.get("T1_WORLD", 0.05))


def playa(key=1.0):
    """Late-afternoon Playa del Carmen, in place of the white studio.

    rev 8b. Donald: he wants a viewer to feel they were there, and the owner to
    remember standing in this vehicle. A white cyclorama cannot do that -- by
    construction it removes the place. This rig reproduces what the reference
    photograph actually has:

      * a low, warm, partly-diffused sun from the show side and slightly aft,
        the colour of late tropical afternoon through palm
      * broken palm shadow rather than an even key -- the reference is dappled
      * warm bounce off pale limestone paving under the vehicle
      * a cool sky fill from above, which is what keeps the cream from going
        orange and stops the shadows going dead
      * the festoon bulbs doing real work: they are emissive in the model and at
        this light level they read as lit rather than as white plastic

    Deliberately NOT a sunset postcard. The reference is shaded, mid-warm and
    fairly soft; an orange-graded hero would be a different lie from a white one.
    """
    c = Vector((0, 0, 1.0))

    # --- low warm sun, show side and slightly aft, raking down the flank
    sun = bpy.data.lights.new("sun", 'SUN')
    sun.energy = 4.70 * key           # rev 9: 3.05 read as overcast once
    sun.color = (1.0, 0.842, 0.664)   # the world was actually visible
    sun.angle = math.radians(2.6)          # softened by haze and palm
    so = bpy.data.objects.new("sun", sun)
    bpy.context.collection.objects.link(so)
    so.location = (-6.0, 9.0, 6.4)
    v = Vector((0.2, 0.0, 1.15)) - Vector(so.location)
    so.rotation_euler = v.to_track_quat('-Z', 'Y').to_euler()

    # --- warm bounce off pale limestone paving
    _softbox("bounce", (1.10, 4.60, 0.30), (0.0, 0.30, 1.05), (7.0, 2.2),
             26.0 * key, (1.0, 0.884, 0.742), spread=120)
    # --- soft warm wrap on the counter side, standing in for the palapa
    _softbox("wrap", (2.60, 7.20, 2.55), (-0.40, 0.60, 1.30), (5.5, 3.0),
             41.0 * key, (1.0, 0.918, 0.816), spread=118)
    # --- cool sky from above: keeps the cream from going orange
    _softbox("sky", (0.4, 0.8, 8.2), (0, 0, 1.3), (12.0, 8.0), 62.0 * key,
             (0.858, 0.918, 1.0))
    # --- the galley still needs its own small source or the bays go black
    _softbox("fill_galley", (-0.35, 2.35, 1.58), (-0.35, 0.0, 1.47),
             (1.7, 0.55), 12.5 * key, (1.0, 0.940, 0.860))
    # --- a little rim off the tail so the rear quarter separates
    _softbox("rim", (-8.4, 2.6, 3.4), c, (4.0, 3.2), 33.0 * key,
             (1.0, 0.930, 0.860))

    w = bpy.data.worlds.new("w_playa")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    # warm-below / cool-above gradient rather than a flat white world. A flat
    # world is the other half of what desaturated the paint (SPEC 10.9).
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    # rev 9: three stops, not two. Until now the film was rendered transparent
    # and composited on white, so this gradient never reached a pixel and the
    # sky read as blown paper with a hard horizon. With the alpha-over path off
    # for T1_SCENE=playa it is the background, and it has to do the work:
    #   below the horizon  warm limestone bounce
    #   at the horizon     the haze band -- this is what reads as "outside"
    #   above              a deeper tropical sky, cool enough to keep the cream
    #                      cream (SPEC 10.9: a flat world was half of what
    #                      desaturated the paint)
    # Still not a sunset postcard. The horizon band is warm-pale, not orange;
    # SKEPTIC B5 is explicit that neither in-service photograph is in direct
    # sun, so an orange grade would be a different lie from a white one.
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.280
    ramp.color_ramp.elements[0].color = (0.520, 0.436, 0.328, 1)
    e_h = ramp.color_ramp.elements.new(0.495)
    e_h.color = (0.930, 0.882, 0.790, 1)
    ramp.color_ramp.elements[1].position = 0.640
    ramp.color_ramp.elements[1].color = (0.286, 0.452, 0.720, 1)
    # rev 9: a world shader's Generated coordinate is the VIEW VECTOR, so Z
    # runs -1..1, not 0..1. The ramp was keyed in 0..1, so every direction at
    # or below the horizon clamped to the bottom stop and the whole background
    # rendered as one flat colour. That, plus the alpha-over path above, is why
    # the sky never existed. Remap -1..1 -> 0..1 so 0.5 IS the horizon.
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = -1.0
    mr.inputs["From Max"].default_value = 1.0
    nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], ramp.inputs[0])
    nt.links.new(ramp.outputs["Color"], bg.inputs[0])
    bg.inputs[1].default_value = float(os.environ.get("T1_WORLD_PLAYA", 1.30))


def ground_playa(size=90.0):
    """Pale limestone paving instead of the white sweep, and it RECEIVES."""
    me = bpy.data.meshes.new("cyc")
    h = size / 2
    me.from_pydata([(-h, -h, 0), (h, -h, 0), (h, h, 0), (-h, h, 0)], [],
                   [(0, 1, 2, 3)])
    me.validate()
    ob = bpy.data.objects.new("cyc", me)
    bpy.context.collection.objects.link(ob)
    mat = bpy.data.materials.new("paving")
    mat.use_nodes = True
    nt = mat.node_tree
    b = nt.nodes["Principled BSDF"]
    # rev 9: at eye height the ground occupies the whole lower third of the
    # frame, so one noise octave at scale 5.5 read as flat grey mud. Two scales
    # now: a slow one that varies the colour of the paving in patches, and a
    # fast one for the surface itself. Base is warmer -- pale limestone in warm
    # light, not neutral aggregate.
    b.inputs["Roughness"].default_value = 0.84
    b.inputs["Specular IOR Level"].default_value = 0.30
    slow = nt.nodes.new("ShaderNodeTexNoise")
    slow.inputs["Scale"].default_value = 0.55
    slow.inputs["Detail"].default_value = 4.0
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].position = 0.36
    cr.color_ramp.elements[0].color = (0.472, 0.418, 0.340, 1)
    cr.color_ramp.elements[1].position = 0.68
    cr.color_ramp.elements[1].color = (0.706, 0.652, 0.548, 1)
    nt.links.new(slow.outputs["Fac"], cr.inputs[0])
    nt.links.new(cr.outputs["Color"], b.inputs["Base Color"])
    n = nt.nodes.new("ShaderNodeTexNoise")
    n.inputs["Scale"].default_value = 26.0
    n.inputs["Detail"].default_value = 10.0
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.16
    nt.links.new(n.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    ob.data.materials.append(mat)
    return ob                               # NOT a shadow catcher: it renders


# ------------------------------------------------------------------- camera
SENSOR_W = 36.0            # full-frame 35 mm, the reference most people read
COC = 0.030                # circle of confusion, mm, for a full-frame sensor


def camera():
    d = bpy.data.cameras.new("cam")
    d.sensor_fit = 'HORIZONTAL'
    d.sensor_width = SENSOR_W
    o = bpy.data.objects.new("cam", d)
    bpy.context.collection.objects.link(o)
    bpy.context.scene.camera = o
    return o


def dof_limits(lens_mm, fstop, dist_m):
    """near / far sharp limits and hyperfocal, metres -- reported, not claimed"""
    f = float(lens_mm)
    H = (f * f) / (fstop * COC) + f                       # mm
    s = dist_m * 1000.0
    near = (H * s) / (H + (s - f))
    far = (H * s) / (H - (s - f)) if H > (s - f) else float('inf')
    return near / 1000.0, far / 1000.0, H / 1000.0


def aim(cam, loc, target, lens=None, ortho=None, focus=None, fstop=None):
    cam.location = loc
    v = Vector(target) - Vector(loc)
    cam.rotation_euler = v.to_track_quat('-Z', 'Y').to_euler()
    d = cam.data
    d.sensor_fit = 'HORIZONTAL'
    d.sensor_width = SENSOR_W
    if ortho:
        d.type = 'ORTHO'
        d.ortho_scale = ortho
        d.dof.use_dof = False
        return None
    d.type = 'PERSP'
    d.lens = lens or 85
    fs = _envf("T1_FSTOP", fstop or 0)
    if fs <= 0:
        d.dof.use_dof = False
        return None
    # focus on the near front arch by default -- the nearest thing on the
    # vehicle that the eye checks for sharpness
    fp = Vector(focus if focus is not None else target)
    dist = (fp - Vector(loc)).length
    d.dof.use_dof = True
    d.dof.focus_object = None
    d.dof.focus_distance = dist
    d.dof.aperture_fstop = fs
    d.dof.aperture_blades = 9          # a real iris, so out-of-focus speculars
    d.dof.aperture_rotation = math.radians(11)   # are 9-sided, not perfect discs
    return (dist, fs) + dof_limits(d.lens, fs, dist)


# ------------------------------------------------------------- white backdrop
def bg_white_level(scene):
    """
    Linear value that the ACTIVE view transform maps to display white.

    The compositor works in LINEAR, upstream of the view transform. Laying the
    render over linear 1.0 and then pushing it through AgX gives a 0.69 GREY
    backdrop -- that was defect D3, and the shadow catcher / film_transparent /
    compositor were all innocent. Drive the backdrop to the transform's white
    point instead.
    """
    # rev 8 (audit optics-7): this keyed on view_transform ALONE, but
    # setup_render then selects the look "AgX - Punchy", under which linear 21.0
    # maps to display 253, not 255 -- the "white" studio backdrop was two code
    # values grey and the vehicle sat on a faintly dirty card. Keyed on the
    # (transform, look) pair.
    vt = scene.view_settings.view_transform
    look = getattr(scene.view_settings, "look", "") or ""
    lvl = {'Standard': 1.0, 'Khronos PBR Neutral': 1.0,
           'AgX': 21.0, 'Filmic': 16.0, 'Filmic Log': 16.0}.get(vt, 21.0)
    if vt == 'AgX' and 'Punchy' in look:
        lvl = 24.87
    return float(os.environ.get("T1_BGW", lvl))


# ------------------------------------------------------------------- optics
def _grain_texture():
    t = bpy.data.textures.get("__grain")
    if not t:
        t = bpy.data.textures.new("__grain", type='NOISE')
    return t


def composite_on_white(scene, rgb=None, optics=True):
    """
    Render with alpha, then lay it over pure white -- and impose the artefacts
    a real lens and a real film stock impose, in the order they impose them.

      bloom   BEFORE the white, on the linear render. After the white it would
              bloom a linear-21.0 background and flare the whole frame.
      CA      after, because dispersion is a property of the taking lens and
              applies to the whole projected image including the backdrop.
      vignette / grain last, for the same reason.

    Vignette is deliberately tiny. SPEC sec.6 says the backdrop composites to
    PURE WHITE, and a visible corner falloff contradicts that; the value here
    is set so the extreme corner sits about one code value below white -- felt,
    not seen. T1_VIG=0 removes it entirely.
    """
    if rgb is None:
        w = bg_white_level(scene)
        rgb = (w, w, w)
    scene.use_nodes = True
    nt = scene.node_tree
    nt.nodes.clear()

    rl = nt.nodes.new("CompositorNodeRLayers"); rl.location = (-900, 0)
    src = rl.outputs["Image"]
    x = -650
    log = []

    on = optics and _envi("T1_FX", 1)

    # --- bloom, on the transparent linear render -------------------------
    if on and _envf("T1_BLOOM", 1.0) > 0:
        try:
            gl = nt.nodes.new("CompositorNodeGlare"); gl.location = (x, 120)
            gl.glare_type = 'FOG_GLOW'
            gl.quality = 'MEDIUM'
            thr = _envf("T1_BLOOM_THR", 3.2)      # linear: speculars only
            sz = _envi("T1_BLOOM_SIZE", 7)
            for holder, key, val in ((gl, "threshold", thr), (gl, "size", sz)):
                if hasattr(holder, key):
                    setattr(holder, key, val)
                elif key.capitalize() in [i.name for i in gl.inputs]:
                    gl.inputs[key.capitalize()].default_value = val
            gl.threshold = getattr(gl, "threshold", thr)
            # -1 = untouched, +1 = glare only. Restrained.
            gl.mix = -1.0 + 2.0 * (0.075 * _envf("T1_BLOOM", 1.0))
            nt.links.new(src, gl.inputs[0]); src = gl.outputs[0]
            log.append("bloom thr=%.2f size=%d mix=%.3f" % (thr, sz, gl.mix))
            x += 250
        except Exception as e:
            log.append("bloom SKIPPED (%s)" % e)

    # --- lay over pure white --------------------------------------------
    bg = nt.nodes.new("CompositorNodeRGB"); bg.location = (x - 200, -300)
    bg.outputs[0].default_value = (*rgb, 1)
    over = nt.nodes.new("CompositorNodeAlphaOver"); over.location = (x, -60)
    nt.links.new(bg.outputs[0], over.inputs[1])
    nt.links.new(src, over.inputs[2])
    src = over.outputs[0]
    x += 250

    # --- chromatic aberration -------------------------------------------
    if on and _envf("T1_CA", 1.0) > 0:
        try:
            ld = nt.nodes.new("CompositorNodeLensdist"); ld.location = (x, -60)
            ld.use_projector = False
            ld.use_jitter = False
            ld.use_fit = True
            # socket names moved between versions; address by index and fall
            # back to name, so this never silently no-ops again
            disp = _envf("T1_CA", 1.0) * 0.0045
            try:
                ld.inputs[1].default_value = 0.0        # Distort
                ld.inputs[2].default_value = disp       # Dispersion
            except Exception:
                ld.inputs["Distortion"].default_value = 0.0
                ld.inputs["Dispersion"].default_value = disp
            nt.links.new(src, ld.inputs[0]); src = ld.outputs[0]
            log.append("CA disp=%.4f" % disp)
            x += 250
        except Exception as e:
            log.append("CA SKIPPED (%s)" % e)

    # --- vignette --------------------------------------------------------
    if on and _envf("T1_VIG", 1.0) > 0:
        try:
            em = nt.nodes.new("CompositorNodeEllipseMask")
            em.location = (x - 200, -420)
            em.width, em.height = 1.36, 1.36
            em.x, em.y = 0.5, 0.5
            em.mask_type = 'ADD'
            bl = nt.nodes.new("CompositorNodeBlur"); bl.location = (x, -420)
            bl.filter_type = 'FAST_GAUSS'
            bl.use_relative = True
            bl.factor_x = bl.factor_y = 28.0
            nt.links.new(em.outputs[0], bl.inputs[0])
            # remap the blurred mask into [1-amt, 1] so it only ever darkens
            amt = _envf("T1_VIG", 1.0) * 0.055
            mr = nt.nodes.new("CompositorNodeMapRange"); mr.location = (x, -560)
            mr.inputs[1].default_value = 0.0
            mr.inputs[2].default_value = 1.0
            mr.inputs[3].default_value = 1.0 - amt
            mr.inputs[4].default_value = 1.0
            nt.links.new(bl.outputs[0], mr.inputs[0])
            mx = nt.nodes.new("CompositorNodeMixRGB"); mx.location = (x + 240, -60)
            mx.blend_type = 'MULTIPLY'
            mx.inputs[0].default_value = 1.0
            nt.links.new(src, mx.inputs[1])
            nt.links.new(mr.outputs[0], mx.inputs[2])
            src = mx.outputs[0]
            log.append("vignette %.1f%% at corner" % (amt * 100))
            x += 480
        except Exception as e:
            log.append("vignette SKIPPED (%s)" % e)

    # --- fine grain ------------------------------------------------------
    if on and _envf("T1_GRAIN", 1.0) > 0:
        try:
            tx = nt.nodes.new("CompositorNodeTexture"); tx.location = (x, -380)
            tx.texture = _grain_texture()
            amt = _envf("T1_GRAIN", 1.0) * 0.016
            sub = nt.nodes.new("CompositorNodeMixRGB"); sub.location = (x + 200, -380)
            sub.blend_type = 'SUBTRACT'
            sub.inputs[0].default_value = 1.0
            sub.inputs[1].default_value = (0.5, 0.5, 0.5, 1)
            nt.links.new(tx.outputs["Color"], sub.inputs[2])
            add = nt.nodes.new("CompositorNodeMixRGB"); add.location = (x + 420, -60)
            add.blend_type = 'ADD'
            add.inputs[0].default_value = amt * 2.0
            nt.links.new(src, add.inputs[1])
            nt.links.new(sub.outputs[0], add.inputs[2])
            src = add.outputs[0]
            log.append("grain %.3f" % amt)
            x += 660
        except Exception as e:
            log.append("grain SKIPPED (%s)" % e)

    out = nt.nodes.new("CompositorNodeComposite"); out.location = (x + 240, -60)
    nt.links.new(src, out.inputs[0])
    return log


# ------------------------------------------------------------------- render
def setup_render(res=(1600, 1100), samples=64, transparent=False):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = samples
    sc.cycles.adaptive_threshold = _envf("T1_ADAPT", 0.008)
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    sc.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
    sc.cycles.max_bounces = 12
    sc.cycles.transmission_bounces = 12
    sc.cycles.transparent_max_bounces = 12
    # rev 8 (audit optics-10): the clamps were never touched, so
    # sample_clamp_indirect sat at the factory 10.0 against a paper white of
    # 21-25 -- every reflected highlight was ceilinged about a stop BELOW the
    # backdrop and then blurred. Nothing in frame could read as polished metal.
    sc.cycles.sample_clamp_direct = 0.0
    sc.cycles.sample_clamp_indirect = 0.0
    sc.cycles.caustics_reflective = True
    sc.cycles.caustics_refractive = False        # no lensing through the glass
    sc.cycles.blur_glossy = 0.2
    sc.render.image_settings.color_depth = '16'  # audit optics-16
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = transparent
    sc.render.use_compositing = True
    sc.render.dither_intensity = 1.0
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.compression = 15
    # a real lens is not a box filter. 1.5 px is close to a photographic MTF
    # and stops the render looking laser-etched at hero resolution.
    # (Cycles owns this in 4.x; RenderSettings.filter_width is BI-era.)
    for holder in (sc.cycles, sc.render):
        if hasattr(holder, "filter_width"):
            holder.filter_width = _envf("T1_FILTER", 1.50)
            break
    vt = os.environ.get("T1_VT", "AgX")
    sc.view_settings.view_transform = vt
    lk = os.environ.get("T1_LOOK", "AgX - Punchy" if vt == 'AgX' else 'None')
    try:
        sc.view_settings.look = lk
    except TypeError:
        sc.view_settings.look = 'None'
    sc.view_settings.exposure = float(os.environ.get("T1_EXP", "0.0"))
    return sc


# ------------------------------------------------------------------ presets
# focus points are on the NEAR FRONT ARCH unless a view has no such thing --
# it is the nearest part of the vehicle and the first place an eye checks.
ARCH_F = (1.30, 0.875, 0.36)
ARCH_F_R = (1.30, -0.875, 0.36)


def views(dist=1.0):
    return {
        # 3/4 front-left, the reference-photo angle
        # rev 8: the lids are OPEN, so the subject is ~3.0 m tall, not 1.94.
        # SPEC 10.8 locks the 78 mm lens and f/8, so the frame is opened by
        # moving the camera BACK and raising the target rather than by going
        # wider -- the lens is what carries the perspective character.
        "hero34f":  dict(loc=(12.20, 8.55, 3.55), tgt=(-0.15, 0.00, 1.34),
                         lens=78, focus=ARCH_F, fstop=8.0),
        # 3/4 rear-left, shows the counter wrap and the louvre block
        "hero34r":  dict(loc=(-11.30, 9.05, 3.80), tgt=(0.10, 0.00, 1.38),
                         lens=76, focus=(-1.50, 0.95, 1.10), fstop=8.0),
        # 3/4 front-right
        "front34":  dict(loc=(13.30, -6.60, 3.10), tgt=(0.25, 0.00, 1.32),
                         lens=76, focus=ARCH_F_R, fstop=8.0),
        "side":     dict(loc=(0.0, 26.0, 1.52), tgt=(0.0, 0.0, 1.52),
                         lens=None, ortho=5.90),
        "front":    dict(loc=(26.0, 0.0, 1.52), tgt=(0.0, 0.0, 1.52),
                         lens=None, ortho=3.55),
        "rear":     dict(loc=(-26.0, 0.0, 1.52), tgt=(0.0, 0.0, 1.52),
                         lens=None, ortho=3.55),
        # nose detail -- longer lens, wider aperture, shallower field
        "detail_f": dict(loc=(4.90, 2.15, 1.85), tgt=(1.95, 0.05, 1.16),
                         lens=100, focus=(2.10, 0.00, 1.14), fstop=6.3),
        "low34":    dict(loc=(11.60, 7.90, 1.55), tgt=(-0.10, 0.0, 1.30),
                         lens=78, focus=ARCH_F, fstop=8.0),
        "topdown":  dict(loc=(2.60, 4.60, 6.40), tgt=(-0.30, 0.0, 1.20),
                         lens=62, focus=(0.60, 0.60, 1.60), fstop=11.0),
        # rev 8b: standing AT the counter, eye height. This is the shot that
        # carries the place rather than the specification -- a person's view,
        # looking slightly up at the mural board with the counter lip in the
        # near field. Wider aperture than the studio heroes: at f/3.5 the tail
        # and the background go soft the way an eye does.
        "playa":    dict(loc=(3.15, 5.75, 1.60), tgt=(-0.30, 0.45, 1.40),
                         lens=42, focus=(0.10, 1.05, 1.30), fstop=3.5),
        "playa_w":  dict(loc=(6.40, 6.90, 1.70), tgt=(-0.30, 0.20, 1.42),
                         lens=50, focus=(0.90, 0.95, 1.25), fstop=4.5),
        # serving counter three-quarter, close -- the shot that says taqueria
        "counter":  dict(loc=(3.40, 5.20, 1.98), tgt=(-0.55, 0.75, 1.26),
                         lens=90, focus=(0.20, 1.05, 1.22), fstop=6.3),
    }


def render_set(names, outdir, prefix="r", res=(1600, 1100), samples=64,
               transparent=True, log=print):
    sc = setup_render(res, samples, transparent)
    fx = []
    if transparent:
        fx = composite_on_white(sc)
    cam = bpy.context.scene.camera or camera()
    V = views()
    os.makedirs(outdir, exist_ok=True)
    log("optics: %s" % ("; ".join(fx) if fx else "NONE"))
    log("film: filter_width=%.2f px  samples=%d  adaptive=%.4f"
        % (getattr(sc.cycles, "filter_width", 0.0), sc.cycles.samples,
           sc.cycles.adaptive_threshold))
    # Strip rendering. The sandbox reaps background processes, so a 20-minute
    # hero cannot run to completion in one go; T1_BORDER="lo,hi" renders a
    # horizontal band of the SAME full-size frame (crop_to_border stays off so
    # the framing is identical in every strip) and the bands are stitched
    # afterwards. Optics are applied to the stitched image in post.py, never
    # per strip, or bloom and vignette would band at the seams.
    bd = os.environ.get("T1_BORDER")
    if bd:
        y0, y1 = (float(t) for t in bd.split(","))
        sc.render.use_border = True
        sc.render.use_crop_to_border = False
        sc.render.border_min_x, sc.render.border_max_x = 0.0, 1.0
        sc.render.border_min_y, sc.render.border_max_y = y0, y1
        log("border render: y %.3f-%.3f of the full %dx%d frame"
            % (y0, y1, res[0], res[1]))
    else:
        sc.render.use_border = False

    for n in names:
        v = V[n]
        d = aim(cam, v["loc"], v["tgt"], v.get("lens"), v.get("ortho"),
                v.get("focus"), v.get("fstop"))
        if d:
            dist, fs, near, far, H = d
            log("cam %-9s %.0f mm  f/%.1f  focus %.2f m  "
                "sharp %.2f-%s m  (hyperfocal %.1f m)"
                % (n, cam.data.lens, fs, dist, near,
                   "inf" if far == float('inf') else "%.2f" % far, H))
        else:
            log("cam %-9s ortho %.3f  (no DoF)" % (n, v.get("ortho") or 0))
        sc.render.resolution_x, sc.render.resolution_y = res
        sc.render.filepath = os.path.join(outdir, f"{prefix}_{n}.png")
        bpy.ops.render.render(write_still=True)
        log(f"rendered {n} -> {sc.render.filepath}")
