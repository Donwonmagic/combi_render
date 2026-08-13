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
    # rev 12, audit `optics-6` -- logged for four revisions, never applied.
    # MEASURED, not asserted: on a 1400x933 side probe the ground read 255.00
    # at EVERY row from 3 px below the contact patch outward, and with the
    # backdrop forced to linear 1.0 (T1_BGW=1.0) the ground under the tyre read
    # 177.00 against open ground at 177.00 -- identical to two decimal places.
    # The catcher was contributing exactly nothing, so the vehicle floated.
    #
    # A shadow catcher writes its shadow into ALPHA and composite_on_white()
    # then lays the frame over linear 24.87. A real photograph on a real white
    # sweep still has a contact shadow: the sweep is a LIT SURFACE, not a matte.
    # TESTED, and the obvious fix is REFUTED: rendering the sweep as a real lit
    # surface (T1_CATCH=0) does put a shadow under the body -- 175.2 mean /
    # 161.2 min on the row below the contact against 255 -- but it also brings
    # back defect D3 in full. The sweep falls off to a 166 grey with a hard
    # horizon line across the frame, and SPEC 6 locks the backdrop to PURE
    # WHITE. Trading the studio's whole look for a contact shadow is not a fix.
    #
    # So the catcher stays ON and `optics-6` stays OPEN, but it is now open with
    # a number instead of an impression: the previous note said the shadow
    # "dies within 11 mm of the tyre", which implies a shadow that decays. It
    # does not decay -- it is not there at all, alpha is identically zero. The
    # next attempt should look at why the catcher writes no alpha under a
    # vehicle that plainly occludes the rig, NOT at softening or lengthening a
    # shadow that does not exist. T1_CATCH=0 reproduces the A/B in one render.
    ob.is_shadow_catcher = bool(int(os.environ.get("T1_CATCH", "1")))
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
    # rev 13: `gal_ceiling`, the emissive stand-in for the roof opening, is
    # DELETED -- the rig now lights the galley through the hole that has been
    # real geometry since rev 12.  Measured on a 1400x933 side ortho, matched
    # windows, against the photograph's 154 / 169 / 181 mean and 38.0 / 32.3 /
    # 17.7 sd:
    #     rev 12 (stand-in)  132 / 158 / 172   sd 17.1 / 18.5 / 17.4
    #     rev 13 (real hole) 141 / 164 / 175   sd 27.6 / 21.8 / 26.9
    # Every mean moved toward the photograph and the two FLAT bays gained real
    # internal contrast -- from the physics, not from dressing.  The remaining
    # deficit was a LEVEL, so this is the one constant that retunes; swept 10.2
    # / 15.0 / 21.0 and measured, not guessed:
    #     10.2 -> 141.8 / 164.0 / 175.0
    #     15.0 -> 140.4 / 164.8 / 177.9
    #     21.0 -> 142.8 / 167.2 / 180.8    <- bays 2 and 3 land within 2 DN
    # Bay 1 stays 11 DN low and that is a DISTRIBUTION problem, not a level one:
    # cranking the global further over-lights the other two.  Logged, not
    # cranked.
    #
    # SPILL, measured rather than asserted, because the rev-11 docstring's whole
    # justification for keeping this source small was "it must not spill onto
    # the paint": 15.0 -> 21.0 moves the aft cream 195.83 -> 198.83 (+1.5 %) and
    # the aft red 128.16 -> 131.04 (+2.2 %).  Accepted on SPEC 10.9's finding
    # that the beauty-pass flank value is an OUTCOME of the rig and not a
    # target; the albedo, which is the guarded quantity, does not move at all.
    _softbox("fill_galley", (-0.35, 2.35, 1.58), (-0.35, 0.0, 1.47),
             (1.7, 0.55), _envf("T1_FILLG", 21.0) * key, (1.0, 0.965, 0.915))

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
    """Playa del Carmen, as the reference photograph actually measures.

    rev 10.  This rig was rebuilt against measurement and four of its previous
    elements were REMOVED because the photograph refutes them.  The rev-8/9
    docstring described "a low warm sun", "broken palm shadow", "a cool sky
    fill" and a haze band.  None of those are in ref_rear34.jpg:

      * NO SUN.  The brightest ground patches sit only +5 L* over their
        surround with 7.4 px edges -- softer than the softest painted edge in
        the frame is sharp.  And the bright/dark ground split measures
        db* +2.4: the SHADOWS ARE WARMER.  A sun/skylight pair has the
        opposite sign by construction, so there is no sun/skylight pair.
      * NO DAPPLE GOBO, for the same reason.  rev 9 added one to honour a
        docstring; the docstring was wrong.
      * NO SKY.  The world ramp topped out at (0.286, 0.452, 0.720) -- a blue
        sky -- at strength 1.30.  There is no sky in frame; the set is under a
        closed canopy with one lateral opening.
      * NO HAZE.  Aerial perspective measures ZERO: the canopy shadow floor
        holds at Y p5 = 0.014-0.019 across the whole depth range and the
        airlight bound is dY < 0.004.

    What IS there is one large, low, LATERAL source -- a palapa opening -- and
    an absorbing ceiling.  The signature that identifies it: the same red paint
    reads 3.95 : 1 between the flank facing the opening and the tail face 72
    deg away, the palm trunk runs 12.5 : 1 across its own diameter with the
    peak 33 deg off the view ray, and an up-facing cream surface is DARKER than
    a vertical one facing the opening (0.93 : 1) while being brighter than one
    turned away (1.87 : 1).  Only a near-horizontal key under a dark ceiling
    does all three.

    Calibrated against those three numbers before any albedo was touched:
    this rig renders flank:f72 = 4.00 (measured 3.95), roof:f72 = 1.91
    (measured 1.87), and up-facing cream 0.787 (measured 0.772 -- a surface
    that was never fitted to).  SPEC 10.23.
    """
    import math as _m
    # rev 10.  The rig geometry and the RATIOS below were solved against the
    # photograph in scene-linear (flank:f72 4.00 against a measured 3.95).
    # The absolute level is a separate question and it is set by the FILM, not
    # by the photograph: this pipeline runs AgX + Punchy, under which the
    # studio's paper white sits at linear 21.0 to reach display 253 (SPEC 10.8).
    # A rig solved at cream = 0.787 linear therefore lands ~5.6 stops down.
    # T1_KEY_PLAYA carries the whole rig -- key, world and galley fill together
    # -- so the solved ratios are untouched by it.
    # Solved by sweep against the film, 2026-08-10.  The reference's cream
    # bodywork sits at display code ~205, i.e. linear 0.593.  Sweep of the
    # up-facing cream roof, in linear: key 30 -> 0.566, 150 -> 0.865,
    # 600 -> clipped.  35 lands it at 0.593.
    key = key * float(os.environ.get("T1_KEY_PLAYA", 35.0))
    KEY_AZ, KEY_EL, KEY_D = 89.0, 10.0, 9.5
    AZ, EL = _m.radians(KEY_AZ), _m.radians(KEY_EL)

    kd = bpy.data.lights.new("key_playa", 'AREA')
    kd.shape = 'RECTANGLE'
    kd.size, kd.size_y = 8.5, 5.0
    kd.energy = 306.4 * key
    kd.color = (1.0, 0.972, 0.936)
    ko = bpy.data.objects.new("key_playa", kd)
    bpy.context.collection.objects.link(ko)
    ko.location = (KEY_D * _m.cos(EL) * _m.cos(AZ),
                   KEY_D * _m.cos(EL) * _m.sin(AZ),
                   KEY_D * _m.sin(EL) + 1.0)
    ko.rotation_euler = (Vector((0, 0, 1.15)) - Vector(ko.location)) \
        .to_track_quat('-Z', 'Y').to_euler()

    # rev 11: this was `12.5 * key`, and `key` is multiplied by T1_KEY_PLAYA
    # (35.0) six lines above -- so it ran at 437, forty-three times the studio
    # rig's 10.2.  It was calibrated when the galley was a black box with no
    # source of its own.  The galley now carries measured practicals whose
    # output is ABSOLUTE, so a softbox scaling with the environment key drowns
    # them.  Held at the studio value, where the galley is solved to within
    # 2.3 % of the photograph on all three bays.
    _softbox("fill_galley", (-0.35, 2.35, 1.58), (-0.35, 0.0, 1.47),
             (1.7, 0.55), 10.2, (1.0, 0.940, 0.860))

    # --- the absorbing canopy.  It is what makes an up-facing surface darker
    #     than a vertical one facing the opening, which is the measured
    #     signature.  Camera-invisible: it shades, it is never in frame.
    ceil = bpy.data.materials.new("absorb_playa")
    ceil.use_nodes = True
    _cb = ceil.node_tree.nodes["Principled BSDF"]
    _cb.inputs["Base Color"].default_value = (0.115, 0.102, 0.086, 1)
    _cb.inputs["Roughness"].default_value = 0.95
    _cb.inputs["Specular IOR Level"].default_value = 0.02

    def _plate(name, verts, faces):
        me = bpy.data.meshes.new(name)
        me.from_pydata(verts, [], faces)
        me.validate()
        ob = bpy.data.objects.new(name, me)
        bpy.context.collection.objects.link(ob)
        ob.data.materials.append(ceil)
        ob.visible_camera = False
        return ob

    _plate("palapa_roof", [(-15.0, -3.0, 3.55), (-1.20, -3.0, 3.55),
                           (-1.20, 7.20, 3.55), (-15.0, 7.20, 3.55)],
           [(0, 1, 2, 3)])
    _R = 11.56          # the one free parameter, solved against roof:f72
    _plate("canopy",
           [(_m.cos(t) * _R - 2.0, _m.sin(t) * _R + 2.0, 7.5)
            for t in [i * 2 * _m.pi / 48 for i in range(48)]],
           [tuple(range(48))])
    _plate("backwall", [(-34.0, -20.0, 0), (34.0, -20.0, 0),
                        (34.0, -20.0, 7.5), (-34.0, -20.0, 7.5)],
           [(0, 1, 2, 3)])

    # --- a uniform dark ambient, NOT a sky gradient.  Open shade.
    w = bpy.data.worlds.new("w_playa")
    bpy.context.scene.world = w
    w.use_nodes = True
    bgn = w.node_tree.nodes["Background"]
    bgn.inputs[0].default_value = (0.92, 0.95, 1.0, 1)
    # The 0.30 : 306 W ratio was solved in an open test cell.  In the built
    # scene the world is a UNIFORM ambient that also lights 90 m of ground the
    # canopy does not cover, so at the solved ratio the terrace blew out and
    # dragged the whole frame flat and pink.  Swept against the reference's own
    # display codes (cream 152, red 167, foliage 81): key 35 / world 0.25 gives
    # cream 160, red 195, foliage 75.
    bgn.inputs[1].default_value = 0.30 * key * float(
        os.environ.get("T1_WORLD_PLAYA", 0.10))

    # --- the place itself ---------------------------------------------------
    # Procedural vegetation and set dressing, placed by inverting the reference
    # photograph's recovered camera: every mass sits at the (image column,
    # depth) the measurement puts it at.  This is the single biggest gap
    # between the rev-9 hero and the memory -- that render had no vegetation in
    # it at all and read as an empty pale plain.  No lamps, no fog, no gobo,
    # and no bunting: the band across the top of the reference is a continuous
    # flowering mass (55.1 % foliage / 13.4 % crimson heads / 5.5 % cream
    # florets), not papel picado.
    import playa_env
    env = playa_env.build(seed=int(os.environ.get("T1_ENV_SEED", 0)))
    print("  playa_env: %d objects, %d instanced polys, band %s"
          % (env["_objects"], env["_instanced_polygons"],
             env["_band_fractions"]))



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
    # rev 10: halved.  Measured against ref_rear34.jpg the terrace sits at
    # display 108 against the cream bodywork's 241 -- a ratio of 0.45.  At the
    # rev-9 albedo the render put it at 209/243 = 0.86, i.e. the paving was
    # nearly as bright as the paint.  That is not only wrong in itself: a
    # terrace that bright throws a large bounce up onto the red flank, and the
    # red below the counter came out at display 198 against the reference's
    # 118.  This is limestone in deep open shade, not a lit apron.
    cr.color_ramp.elements[0].color = (0.245, 0.216, 0.176, 1)
    cr.color_ramp.elements[1].position = 0.68
    cr.color_ramp.elements[1].color = (0.367, 0.339, 0.285, 1)
    nt.links.new(slow.outputs["Fac"], cr.inputs[0])
    # rev 9: 90 m of paving meeting the sky at full contrast gives a hard
    # cut-out horizon. Fade the ground into the haze band beyond ~14 m so the
    # join reads as distance rather than as the edge of a plane.
    tc2 = nt.nodes.new("ShaderNodeTexCoord")
    vlen = nt.nodes.new("ShaderNodeVectorMath")
    vlen.operation = 'LENGTH'
    nt.links.new(tc2.outputs["Object"], vlen.inputs[0])
    far = nt.nodes.new("ShaderNodeMapRange")
    far.inputs["From Min"].default_value = 14.0
    far.inputs["From Max"].default_value = 52.0
    far.inputs["To Min"].default_value = 0.0
    # rev 10: was 0.88.  Aerial perspective in the reference measures ZERO --
    # the canopy shadow floor holds at Y p5 = 0.014-0.019 across the whole
    # depth range and the airlight bound is dY < 0.004.  There is nothing for
    # a haze band to reproduce, and beyond ~6 m the frame is now filled with
    # measured vegetation rather than with empty ground.  Left wired at 0 so
    # the node graph still shows what was there.
    far.inputs["To Max"].default_value = 0.00
    nt.links.new(vlen.outputs["Value"], far.inputs["Value"])
    hazemix = nt.nodes.new("ShaderNodeMix")
    hazemix.data_type = 'RGBA'
    hazemix.inputs[7].default_value = (0.930, 0.882, 0.790, 1)   # the haze band
    nt.links.new(far.outputs["Result"], hazemix.inputs[0])
    nt.links.new(cr.outputs["Color"], hazemix.inputs[6])
    nt.links.new(hazemix.outputs[2], b.inputs["Base Color"])
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
        # rev 10.  The reference photograph's own camera, recovered from the
        # rear rim flange (139.1 px conic fit = 0.440 m -> 316 px/m), the
        # horizon row (230 +/- 30) and the wheel-ellipse axis ratio: it sits at
        # (-4.83, +2.22, 1.90) -- level with the bus's roof line -- with a
        # 53.1 deg horizontal field, i.e. a 36 mm lens.  Confirmed by a feature
        # the solve never saw: it predicts the bus's far top corner at image
        # column 554.6 and the cream lid panel is read at 555.
        #
        # This is the frame Donald wants the owner to remember standing in.
        # Everything playa_env places is placed by inverting THIS camera, so it
        # is also the one view where every plant is exactly where it was
        # measured to be.
        "playa_ref": dict(loc=(-4.829, 2.222, 1.900), tgt=(-0.55, -0.10, 1.28),
                          lens=36, focus=(-1.20, 0.55, 1.20), fstop=4.5),
        "playa_w":  dict(loc=(6.40, 6.90, 1.70), tgt=(-0.30, 0.20, 1.42),
                         lens=50, focus=(0.90, 0.95, 1.25), fstop=4.5),
        # serving counter three-quarter, close -- the shot that says taqueria
        "counter":  dict(loc=(3.40, 5.20, 1.98), tgt=(-0.55, 0.75, 1.26),
                         lens=90, focus=(0.20, 1.05, 1.22), fstop=6.3),
    }


def _cull_foreground(loc, tgt, margin=2.20, log=print):
    """Hide environment geometry that stands between the camera and the vehicle.

    playa_env places its masses by inverting the REFERENCE photograph's camera,
    which is the right thing to do -- every plant is at the depth and bearing
    the measurement puts it at.  But the hero cameras are not the reference
    camera, and a plant that is correctly 6 m behind the vehicle from one
    bearing is correctly in front of it from another.  The rev-10 probe from
    `playa_w` was a wall of fronds with the bus behind it.

    So this hides from the LENS ONLY (visible_camera) anything named pl_* whose
    origin lies closer to the camera than the vehicle's near side.  It still
    shades, still casts, still bounces light -- the scene is unchanged
    radiometrically, and only the occluders are taken out of the shot.  That is
    a framing decision, not a lighting one.
    """
    import mathutils
    C = mathutils.Vector(loc)
    T = mathutils.Vector(tgt)
    fwd = (T - C)
    L = fwd.length
    if L < 1e-6:
        return
    fwd = fwd / L
    hid = 0
    for ob in bpy.data.objects:
        if ob.type != 'MESH' or not ob.name.startswith("pl_"):
            continue
        was = ob.visible_camera
        rel = ob.matrix_world.translation - C
        t = rel.dot(fwd)                       # depth along the view ray
        perp = (rel - fwd * t).length          # lateral offset from the ray
        # in front of the vehicle, and close enough to the axis to occlude it
        front = (t < L - margin) and (perp < max(3.0, 0.55 * t))
        ob.visible_camera = not front
        if front and was:
            hid += 1
    if hid:
        log("  culled %d pl_* objects from the lens (they still shade)" % hid)


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
        _cull_foreground(v["loc"], v["tgt"], log=log)
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
