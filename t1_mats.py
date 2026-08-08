"""PBR materials.  Body two-tone + livery is driven by object-space position
so no UV unwrap of the shell is needed."""
import bpy, math, os

TEXDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tex")

# SPEC r4 sec.3: measured (196,106,36) sRGB in sun -> faded orange-red /
# vermillion, hue ~26deg. NOT a deep crimson.
RED = (0.4800, 0.0750, 0.0300)
# measured (206,208,200) sRGB -> sun-bleached near-neutral off-white
CREAM = (0.7900, 0.7700, 0.7150)
GOLD = (0.8600, 0.5400, 0.0600)

# two-tone break line:  belt line on the flanks, V-swage across the nose
Z_BELT = 1.2320
V_APEX = 0.8180
V_RISE = 0.4140
V_POW = 1.16


def _nt(mat):
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (900, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (560, 0)
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    return nt, bsdf


def simple(name, base, rough=0.35, metal=0.0, spec=0.5, coat=0.0,
           ior=1.45, emit=None, transmit=0.0, alpha=1.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    nt, b = _nt(m)
    b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Specular IOR Level"].default_value = spec
    b.inputs["IOR"].default_value = ior
    if coat:
        b.inputs["Coat Weight"].default_value = coat
        b.inputs["Coat Roughness"].default_value = 0.030
    if transmit:
        b.inputs["Transmission Weight"].default_value = transmit
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
        m.blend_method = 'BLEND'
    if emit:
        b.inputs["Emission Color"].default_value = (*emit[0], 1)
        b.inputs["Emission Strength"].default_value = emit[1]
    return m


# ---------------------------------------------------------------------------
def _img(nt, filename, x, y, projection='FLAT', blend=0.0,
         interp='Cubic', ext='CLIP'):
    node = nt.nodes.new("ShaderNodeTexImage")
    node.location = (x, y)
    path = os.path.join(TEXDIR, filename)
    if os.path.exists(path):
        node.image = bpy.data.images.load(path, check_existing=True)
        node.image.colorspace_settings.name = 'sRGB'
    node.projection = projection
    node.projection_blend = blend
    node.interpolation = interp
    node.extension = ext
    return node


def _feed(nt, src, socket):
    """src may be a node, an output socket, or a plain number"""
    if src is None:
        return
    if hasattr(src, 'outputs'):                 # a node
        nt.links.new(src.outputs[0], socket)
    elif hasattr(src, 'node'):                  # an output socket
        nt.links.new(src, socket)
    else:
        socket.default_value = src


def _math(nt, op, a=None, b=None, x=0, y=0, clamp=False):
    n = nt.nodes.new("ShaderNodeMath")
    n.operation = op
    n.location = (x, y)
    n.use_clamp = clamp
    _feed(nt, a, n.inputs[0])
    _feed(nt, b, n.inputs[1])
    return n


def body_paint(name="T1_paint"):
    """
    Cream above the break line, Tacombi red below, gold folk-art swirls
    box-projected over the red, gloss clearcoat over everything.
    """
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    nt, bsdf = _nt(m)

    geo = nt.nodes.new("ShaderNodeNewGeometry"); geo.location = (-1600, 300)
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); sep.location = (-1420, 300)
    nt.links.new(geo.outputs["Position"], sep.inputs[0])

    # u = |y| / 0.86
    absy = _math(nt, 'ABSOLUTE', sep.outputs["Y"], None, -1240, 240)
    u = _math(nt, 'DIVIDE', absy, 0.860, -1080, 240, clamp=True)
    up = _math(nt, 'POWER', u, V_POW, -920, 240)
    zv = _math(nt, 'MULTIPLY_ADD', up, V_RISE, -760, 240)
    zv.inputs[2].default_value = V_APEX

    # blend factor: 0 on the flanks, 1 across the nose panel
    tblend = nt.nodes.new("ShaderNodeMapRange")
    tblend.location = (-1000, 60)
    tblend.interpolation_type = 'SMOOTHSTEP'
    tblend.clamp = True
    tblend.inputs[1].default_value = 1.858
    tblend.inputs[2].default_value = 2.012
    tblend.inputs[3].default_value = 0.0
    tblend.inputs[4].default_value = 1.0
    nt.links.new(sep.outputs["X"], tblend.inputs[0])

    mixz = nt.nodes.new("ShaderNodeMix"); mixz.location = (-180, 200)
    mixz.data_type = 'FLOAT'
    mixz.inputs[2].default_value = Z_BELT
    nt.links.new(tblend.outputs[0], mixz.inputs[0])
    nt.links.new(zv.outputs[0], mixz.inputs[3])

    # hard-ish edge:  cream = 1 when z > break
    dz = _math(nt, 'SUBTRACT', sep.outputs["Z"], mixz.outputs[0], -20, 340)
    edge = _math(nt, 'DIVIDE', dz, 0.0045, 140, 340)
    edge = _math(nt, 'ADD', edge, 0.5, 300, 340, clamp=True)

    # gold swirl decal, box-projected in object space
    texco = nt.nodes.new("ShaderNodeTexCoord"); texco.location = (-1600, -420)
    mp = nt.nodes.new("ShaderNodeMapping"); mp.location = (-1420, -420)
    mp.inputs["Location"].default_value = (0.185, 0.410, 0.263)
    mp.inputs["Scale"].default_value = (0.6300, 0.6300, 0.6300)
    nt.links.new(texco.outputs["Object"], mp.inputs["Vector"])
    swirl = _img(nt, "swirl.png", -1180, -420, projection='BOX',
                 blend=0.32, ext='REPEAT')
    nt.links.new(mp.outputs[0], swirl.inputs["Vector"])

    # --- density mask (SPEC sec.3): heaviest on the nose, trailing along the
    #     belt, sparse at the tail. Applied as a spatially varying cutoff on a
    #     low-frequency noise so whole motifs drop out rather than fading.
    fx = nt.nodes.new("ShaderNodeMapRange"); fx.location = (-1180, -900)
    fx.interpolation_type = 'SMOOTHSTEP'; fx.clamp = True
    fx.inputs[1].default_value = -2.05
    fx.inputs[2].default_value = 1.65
    fx.inputs[3].default_value = 0.34
    fx.inputs[4].default_value = 1.00
    nt.links.new(sep.outputs["X"], fx.inputs[0])

    bz = _math(nt, 'SUBTRACT', sep.outputs["Z"], 1.045, -1180, -1060)
    bz = _math(nt, 'DIVIDE', bz, 0.300, -1020, -1060)
    bz = _math(nt, 'MULTIPLY', bz, bz, -880, -1060)
    bz = _math(nt, 'MULTIPLY', bz, -1.0, -740, -1060)
    belt = _math(nt, 'EXPONENT', bz, None, -600, -1060)
    beltw = _math(nt, 'MULTIPLY_ADD', belt, 0.62, -460, -1060)
    beltw.inputs[2].default_value = 0.52
    dens = _math(nt, 'MULTIPLY', fx, beltw, -320, -960, clamp=True)

    clut = nt.nodes.new("ShaderNodeTexNoise"); clut.location = (-1180, -1240)
    clut.inputs["Scale"].default_value = 1.15
    clut.inputs["Detail"].default_value = 1.0
    nt.links.new(texco.outputs["Object"], clut.inputs["Vector"])
    thr = _math(nt, 'SUBTRACT', 0.92, dens, -180, -1240)
    keep = _math(nt, 'GREATER_THAN', clut.outputs["Fac"], thr, -40, -1240)
    amask = _math(nt, 'MULTIPLY', swirl.outputs["Alpha"], keep, 100, -1240)

    # red + gold
    mix_g = nt.nodes.new("ShaderNodeMix"); mix_g.location = (-820, -420)
    mix_g.data_type = 'RGBA'
    mix_g.inputs[6].default_value = (*RED, 1)
    if swirl.image:
        hs = nt.nodes.new("ShaderNodeHueSaturation"); hs.location = (-980, -560)
        hs.inputs["Saturation"].default_value = 1.22
        hs.inputs["Value"].default_value = 1.06
        nt.links.new(swirl.outputs["Color"], hs.inputs["Color"])
        nt.links.new(amask.outputs[0], mix_g.inputs[0])
        nt.links.new(hs.outputs[0], mix_g.inputs[7])
    else:
        mix_g.inputs[0].default_value = 0.0
        mix_g.inputs[7].default_value = (*GOLD, 1)

    mix_c = nt.nodes.new("ShaderNodeMix"); mix_c.location = (380, 0)
    mix_c.data_type = 'RGBA'
    nt.links.new(edge.outputs[0], mix_c.inputs[0])
    nt.links.new(mix_g.outputs[2], mix_c.inputs[6])
    mix_c.inputs[7].default_value = (*CREAM, 1)
    nt.links.new(mix_c.outputs[2], bsdf.inputs["Base Color"])

    bsdf.inputs["Roughness"].default_value = 0.105
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Specular IOR Level"].default_value = 0.58
    bsdf.inputs["Coat Weight"].default_value = 0.75
    bsdf.inputs["Coat Roughness"].default_value = 0.025

    # very fine orange-peel so the highlights are not mirror perfect
    noise = nt.nodes.new("ShaderNodeTexNoise"); noise.location = (0, -640)
    noise.inputs["Scale"].default_value = 240.0
    noise.inputs["Detail"].default_value = 2.0
    bump = nt.nodes.new("ShaderNodeBump"); bump.location = (300, -640)
    bump.inputs["Strength"].default_value = 0.045
    bump.inputs["Distance"].default_value = 0.004
    nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs[0], bsdf.inputs["Normal"])
    return m


def signage(name, filename, base=CREAM):
    """flat board carrying a decal image (canopy fascia, side emblem)"""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    nt, b = _nt(m)
    tex = _img(nt, filename, -400, 0)
    if tex.image:
        mix = nt.nodes.new("ShaderNodeMix"); mix.location = (100, 0)
        mix.data_type = 'RGBA'
        mix.inputs[6].default_value = (*base, 1)
        nt.links.new(tex.outputs["Alpha"], mix.inputs[0])
        nt.links.new(tex.outputs["Color"], mix.inputs[7])
        nt.links.new(mix.outputs[2], b.inputs["Base Color"])
    else:
        b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Roughness"].default_value = 0.16
    b.inputs["Coat Weight"].default_value = 0.5
    b.inputs["Specular IOR Level"].default_value = 0.5
    return m


def fascia_sign(name="fascia_sign"):
    """canopy valance: object-space X -> u, Z -> v, cream board + script"""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    nt, b = _nt(m)
    X0, X1 = 0.4180, -2.1550
    Z0, Z1 = 1.6280, 1.8380
    geo = nt.nodes.new("ShaderNodeNewGeometry"); geo.location = (-1200, 0)
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); sep.location = (-1020, 0)
    nt.links.new(geo.outputs["Position"], sep.inputs[0])
    u = _math(nt, 'SUBTRACT', sep.outputs["X"], X1, -840, 200)
    u = _math(nt, 'DIVIDE', u, (X0 - X1), -680, 200)
    ui = _math(nt, 'SUBTRACT', 1.0, u, -680, 330)
    nrm = nt.nodes.new("ShaderNodeNewGeometry"); nrm.location = (-1200, 420)
    nsep = nt.nodes.new("ShaderNodeSeparateXYZ"); nsep.location = (-1020, 420)
    nt.links.new(nrm.outputs["Normal"], nsep.inputs[0])
    side = _math(nt, 'GREATER_THAN', nsep.outputs["Y"], 0.0, -840, 420)
    usel = nt.nodes.new("ShaderNodeMix"); usel.location = (-560, 260)
    usel.data_type = 'FLOAT'
    nt.links.new(side.outputs[0], usel.inputs[0])
    nt.links.new(u.outputs[0], usel.inputs[2])
    nt.links.new(ui.outputs[0], usel.inputs[3])
    u = usel
    v = _math(nt, 'SUBTRACT', sep.outputs["Z"], Z0, -840, -120)
    v = _math(nt, 'DIVIDE', v, (Z1 - Z0), -680, -120)
    comb = nt.nodes.new("ShaderNodeCombineXYZ"); comb.location = (-500, 0)
    nt.links.new(u.outputs[0], comb.inputs[0])
    nt.links.new(v.outputs[0], comb.inputs[1])
    tex = _img(nt, "fascia.png", -320, 0)
    nt.links.new(comb.outputs[0], tex.inputs["Vector"])
    mix = nt.nodes.new("ShaderNodeMix"); mix.location = (120, 0)
    mix.data_type = 'RGBA'
    mix.inputs[6].default_value = (*CREAM, 1)
    if tex.image:
        nt.links.new(tex.outputs["Alpha"], mix.inputs[0])
        nt.links.new(tex.outputs["Color"], mix.inputs[7])
    else:
        mix.inputs[0].default_value = 0.0
    nt.links.new(mix.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.170
    b.inputs["Coat Weight"].default_value = 0.45
    return m


def decal_uv(name, filename, base=RED):
    """UV-mapped decal plate (side emblem)"""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    nt, b = _nt(m)
    tex = _img(nt, filename, -320, 0)
    mix = nt.nodes.new("ShaderNodeMix"); mix.location = (120, 0)
    mix.data_type = 'RGBA'
    mix.inputs[6].default_value = (*base, 1)
    if tex.image:
        nt.links.new(tex.outputs["Alpha"], mix.inputs[0])
        nt.links.new(tex.outputs["Color"], mix.inputs[7])
    else:
        mix.inputs[0].default_value = 0.0
    nt.links.new(mix.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.105
    b.inputs["Coat Weight"].default_value = 0.75
    b.inputs["Coat Roughness"].default_value = 0.025
    b.inputs["Specular IOR Level"].default_value = 0.58
    return m


def silver_script(name="script"):
    """Senor Tacombi -- silver signwriting, UV-mapped decal panel"""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    nt, b = _nt(m)
    tex = _img(nt, "senor.png", -420, 0)
    alpha = nt.nodes.new("ShaderNodeMath"); alpha.location = (-120, -260)
    alpha.operation = 'MULTIPLY'
    alpha.inputs[1].default_value = 1.0
    trans = nt.nodes.new("ShaderNodeBsdfTransparent"); trans.location = (200, 240)
    mixs = nt.nodes.new("ShaderNodeMixShader"); mixs.location = (740, 120)
    out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]
    if tex.image:
        nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
        nt.links.new(tex.outputs["Alpha"], alpha.inputs[0])
        nt.links.new(alpha.outputs[0], mixs.inputs[0])
    else:
        mixs.inputs[0].default_value = 0.0
    nt.links.new(trans.outputs[0], mixs.inputs[1])
    nt.links.new(b.outputs[0], mixs.inputs[2])
    nt.links.new(mixs.outputs[0], out.inputs[0])
    b.inputs["Roughness"].default_value = 0.185
    b.inputs["Metallic"].default_value = 0.55
    b.inputs["Coat Weight"].default_value = 0.70
    b.inputs["Coat Roughness"].default_value = 0.025
    m.blend_method = 'BLEND'
    m.show_transparent_back = False
    return m


def frosted_calidad(name="calidad"):
    """bay 4: frosted glass carrying the 100% CALIDAD decal"""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    nt, b = _nt(m)
    tex = _img(nt, "calidad.png", -420, -140)
    b.inputs["Base Color"].default_value = (0.760, 0.790, 0.782, 1)
    b.inputs["Roughness"].default_value = 0.300
    b.inputs["Transmission Weight"].default_value = 0.88
    b.inputs["IOR"].default_value = 1.50
    if tex.image:
        mix = nt.nodes.new("ShaderNodeMix"); mix.location = (60, 60)
        mix.data_type = 'RGBA'
        mix.inputs[6].default_value = (0.760, 0.790, 0.782, 1)
        nt.links.new(tex.outputs["Alpha"], mix.inputs[0])
        nt.links.new(tex.outputs["Color"], mix.inputs[7])
        nt.links.new(mix.outputs[2], b.inputs["Base Color"])
        tr = nt.nodes.new("ShaderNodeMath"); tr.location = (60, -220)
        tr.operation = 'SUBTRACT'
        tr.inputs[0].default_value = 0.88
        tr.use_clamp = True
        nt.links.new(tex.outputs["Alpha"], tr.inputs[1])
        nt.links.new(tr.outputs[0], b.inputs["Transmission Weight"])
    return m


def build_all():
    M = {}
    M["paint"] = body_paint()
    M["cream"] = simple("cream", CREAM, rough=0.13, coat=0.6, spec=0.55)
    # ---- SPEC rev4 painted-not-plated / painted-not-timber additions ----
    M["wheelcream"] = simple("wheelcream", (0.7100, 0.6900, 0.6350),
                             rough=0.34, coat=0.10, spec=0.40)
    M["bumpercream"] = simple("bumpercream", (0.7550, 0.7350, 0.6800),
                              rough=0.22, coat=0.30, spec=0.50)
    M["roundelred"] = simple("roundelred", (0.4550, 0.0720, 0.0300),
                             rough=0.26, coat=0.25, spec=0.45)
    M["countercream"] = simple("countercream", (0.7350, 0.7150, 0.6600),
                               rough=0.38, coat=0.06, spec=0.35)
    M["red"] = simple("red", RED, rough=0.12, coat=0.65, spec=0.58)
    M["chrome"] = simple("chrome", (0.860, 0.868, 0.880), rough=0.045,
                         metal=1.0)
    M["chrome_d"] = simple("chrome_dull", (0.760, 0.768, 0.780), rough=0.16,
                           metal=1.0)
    M["glass"] = simple("glass", (0.780, 0.845, 0.815), rough=0.004,
                        transmit=1.0, ior=1.47, spec=0.35)
    M["rubber"] = simple("rubber", (0.0175, 0.0175, 0.0185), rough=0.78,
                         spec=0.22)
    M["tyre"] = simple("tyre", (0.0225, 0.0225, 0.0240), rough=0.70,
                       spec=0.25)
    M["wheelred"] = simple("wheelred", (0.3600, 0.0230, 0.0180), rough=0.24,
                           coat=0.35, spec=0.50)
    M["capred"] = simple("capred", (0.4750, 0.0290, 0.0225), rough=0.085,
                         coat=0.85, spec=0.60)
    M["capwhite"] = simple("capwhite", (0.8900, 0.8880, 0.8720), rough=0.115,
                           coat=0.7, spec=0.55)
    M["whitewall"] = simple("whitewall", (0.7450, 0.7380, 0.7120), rough=0.46,
                            spec=0.28)
    M["canvas"] = simple("canvas", (0.6600, 0.6420, 0.5900), rough=0.86,
                         spec=0.22)
    M["script"] = silver_script()
    M["calidad"] = frosted_calidad()
    M["dark"] = simple("interior_dark", (0.0300, 0.0290, 0.0280), rough=0.72)
    M["seat"] = simple("seat", (0.1250, 0.1000, 0.0760), rough=0.55)
    M["timber"] = simple("timber", (0.3200, 0.2050, 0.1050), rough=0.48)
    M["amber"] = simple("amber", (0.9200, 0.3400, 0.0250), rough=0.09,
                        transmit=0.75, ior=1.49)
    M["ruby"] = simple("ruby", (0.7000, 0.0350, 0.0250), rough=0.09,
                       transmit=0.72, ior=1.49)
    M["lens"] = simple("lens", (0.900, 0.918, 0.930), rough=0.018,
                       transmit=0.96, ior=1.52, spec=0.42)
    M["reflector"] = simple("reflector", (0.960, 0.962, 0.968), rough=0.055,
                            metal=1.0)
    M["steel"] = simple("steel", (0.520, 0.525, 0.535), rough=0.28, metal=1.0)
    M["white"] = simple("white_gloss", (0.8700, 0.8720, 0.8600), rough=0.11,
                        coat=0.6)
    return M


def assign(ob, mat):
    ob.data.materials.clear()
    ob.data.materials.append(mat)
