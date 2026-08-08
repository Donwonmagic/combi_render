"""white cyclorama studio, lighting rig, camera set, render driver"""
import bpy, math, os
from mathutils import Vector


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
    b.inputs["Base Color"].default_value = (0.94, 0.94, 0.945, 1)
    b.inputs["Roughness"].default_value = 0.68
    b.inputs["Specular IOR Level"].default_value = 0.20
    ob.data.materials.append(mat)
    ob.is_shadow_catcher = True
    return ob


def _softbox(name, loc, aim, size, power, colour=(1, 1, 1)):
    d = bpy.data.lights.new(name, 'AREA')
    d.shape = 'RECTANGLE'
    d.size, d.size_y = size
    d.energy = power
    d.color = colour
    o = bpy.data.objects.new(name, d)
    bpy.context.collection.objects.link(o)
    o.location = loc
    v = Vector(aim) - Vector(loc)
    o.rotation_euler = v.to_track_quat('-Z', 'Y').to_euler()
    return o


def lighting(key=1.0):
    """large, few, soft — a real product studio, not a wall of highlights"""
    c = Vector((0, 0, 1.0))
    _softbox("top",   (0.6, 1.2, 8.6), (0, 0, 1.3), (13.0, 8.5), 3400 * key)
    _softbox("key",   (6.4, 8.2, 5.4), c, (6.0, 4.2), 1750 * key)
    _softbox("fillL", (2.0, 9.0, 2.2), (0, 0, 1.1), (9.0, 3.6), 460 * key,
             (0.985, 0.99, 1.0))
    _softbox("fillR", (2.4, -9.0, 2.4), (0, 0, 1.1), (9.0, 3.6), 620 * key,
             (0.975, 0.985, 1.0))
    _softbox("rim",   (-9.2, 3.4, 4.2), c, (5.0, 4.0), 1050 * key)
    _softbox("nose",  (10.6, 1.6, 1.5), (1.6, 0.0, 1.05), (3.2, 2.6),
             260 * key)
    w = bpy.data.worlds.new("w")
    bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.30


def camera():
    d = bpy.data.cameras.new("cam")
    o = bpy.data.objects.new("cam", d)
    bpy.context.collection.objects.link(o)
    bpy.context.scene.camera = o
    return o


def aim(cam, loc, target, lens=None, ortho=None):
    cam.location = loc
    v = Vector(target) - Vector(loc)
    cam.rotation_euler = v.to_track_quat('-Z', 'Y').to_euler()
    if ortho:
        cam.data.type = 'ORTHO'; cam.data.ortho_scale = ortho
    else:
        cam.data.type = 'PERSP'; cam.data.lens = lens or 85


def composite_on_white(scene, rgb=(1.0, 1.0, 1.0)):
    """render with alpha, then lay it over pure white in the compositor"""
    scene.use_nodes = True
    nt = scene.node_tree
    nt.nodes.clear()
    rl = nt.nodes.new("CompositorNodeRLayers"); rl.location = (-400, 0)
    bg = nt.nodes.new("CompositorNodeRGB"); bg.location = (-400, -260)
    bg.outputs[0].default_value = (*rgb, 1)
    over = nt.nodes.new("CompositorNodeAlphaOver"); over.location = (-60, -60)
    nt.links.new(bg.outputs[0], over.inputs[1])
    nt.links.new(rl.outputs["Image"], over.inputs[2])
    out = nt.nodes.new("CompositorNodeComposite"); out.location = (240, -60)
    nt.links.new(over.outputs[0], out.inputs[0])


def setup_render(res=(1600, 1100), samples=64, transparent=False):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = samples
    sc.cycles.adaptive_threshold = 0.008
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    sc.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
    sc.cycles.max_bounces = 12
    sc.cycles.transmission_bounces = 12
    sc.cycles.transparent_max_bounces = 12
    sc.cycles.caustics_reflective = False
    sc.cycles.caustics_refractive = False
    sc.cycles.blur_glossy = 0.6
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.film_transparent = transparent
    sc.render.use_compositing = True
    sc.render.dither_intensity = 1.0
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_depth = '8'
    sc.render.image_settings.compression = 15
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
def views(dist=1.0):
    return {
        # 3/4 front-left, the reference-photo angle
        "hero34f":  dict(loc=(9.30, 6.52, 2.90), tgt=(-0.15, 0.00, 0.92),
                         lens=78),
        # 3/4 rear-left, shows the bed + canopy
        "hero34r":  dict(loc=(-8.60, 6.90, 3.10), tgt=(0.10, 0.00, 0.98),
                         lens=76),
        # 3/4 front-right
        "front34":  dict(loc=(10.10, -5.00, 2.35), tgt=(0.25, 0.00, 0.92),
                         lens=76),
        "side":     dict(loc=(0.0, 26.0, 0.98), tgt=(0.0, 0.0, 0.98),
                         lens=None, ortho=4.95),
        "front":    dict(loc=(26.0, 0.0, 0.98), tgt=(0.0, 0.0, 0.98),
                         lens=None, ortho=3.10),
        "rear":     dict(loc=(-26.0, 0.0, 0.98), tgt=(0.0, 0.0, 0.98),
                         lens=None, ortho=3.10),
        "detail_f": dict(loc=(4.90, 2.15, 1.85), tgt=(1.95, 0.05, 1.16),
                         lens=100),
        "low34":    dict(loc=(9.00, 6.10, 1.30), tgt=(-0.10, 0.0, 0.98),
                         lens=78),
        "topdown":  dict(loc=(2.60, 4.60, 6.40), tgt=(-0.30, 0.0, 1.20),
                         lens=62),
    }


def render_set(names, outdir, prefix="r", res=(1600, 1100), samples=64,
               transparent=True, log=print):
    sc = setup_render(res, samples, transparent)
    if transparent:
        composite_on_white(sc)
    cam = bpy.context.scene.camera or camera()
    V = views()
    os.makedirs(outdir, exist_ok=True)
    for n in names:
        v = V[n]
        aim(cam, v["loc"], v["tgt"], v.get("lens"), v.get("ortho"))
        sc.render.resolution_x, sc.render.resolution_y = res
        sc.render.filepath = os.path.join(outdir, f"{prefix}_{n}.png")
        bpy.ops.render.render(write_still=True)
        img = bpy.data.images.get('Render Result')
        corner = ""
        try:
            fp = bpy.data.images.load(sc.render.filepath + ".png"
                                      if not sc.render.filepath.endswith(".png")
                                      else sc.render.filepath, check_existing=False)
            px = list(fp.pixels[:4])
            corner = "  corner px=%.3f,%.3f,%.3f" % tuple(px[:3])
            bpy.data.images.remove(fp)
        except Exception:
            pass
        log(f"rendered {n}{corner}")
