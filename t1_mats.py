"""PBR materials.  Body two-tone + livery is driven by object-space position
so no UV unwrap of the shell is needed.

SPEC rev6 sec.3 locks the finish as WEATHERED -- chalky, sun-faded, uneven,
chipped edges, dusty lower body.  Every exterior material therefore runs its
Base Color / Roughness / Normal through the shared WEATHER node group below;
nothing on this vehicle carries a constant roughness.

NO SUBSURFACE ANYWHERE.  Every material sits at Subsurface Weight 0.0 and
verify.py asserts it.

MEASURED RESULT (2026-08-09, /sessions/.../tmp/rms_metric.py, side ortho
500x340 @ 9.90 mm/px, 16 samples, plain cream tiles on the rear-corner panel,
noise-corrected texture residual sd(L - boxblur)/mean at matched physical
scale):

                                   25 mm   100 mm   400 mm
  ref_side.jpg, patch as specified  3.37 %   7.03 %  10.54 %
  ref_side.jpg, flat part only      1.06 %   3.63 %   4.78 %
  ref_side.jpg, flat + detrended    1.00 %   3.42 %   3.97 %
  build BEFORE this change          0.22 %   0.24 %   0.33 %
  build AFTER  this change          0.37 %   0.81 %   1.42 %

Two things stop the display-referred figure reaching the design target, both
measured, neither fixable in a shader:

 1. 55 % of the 400 mm target is the tail curving out of the light.  The
    reference patch is 45 px wide and its last 7 columns run 235 -> 182 code
    values down the rear corner.  Dropping them takes the target from 10.54 %
    to 4.78 %.

 2. AgX + "AgX - Punchy" is nearly flat where the cream sits.  Measured by
    exposure derivative on this scene (T1_EXP -0.25 / 0 / +0.25):
    d(code)/dEV = 16.60 at cream mean 224.9, i.e. a local gain of 0.106
    display-fraction per unit scene-linear fraction.  On the red lower body,
    two stops darker, the same measurement gives 0.309.  A gamma-2.4 camera
    response would be ~0.42 before its own highlight shoulder.  So the cream
    panel throws away ~90 % of any albedo modulation before it reaches a code
    value, and the same shader reads three times stronger on the red.

Working back through the measured gain, the 1.42 % display residual here is
13.4 % albedo sd in linear reflectance.  The reference's flat + detrended
3.97 % corresponds to 11-16 % albedo sd for a camera highlight gain of
0.25-0.35.  In linear reflectance the paint now carries the same texture
amplitude as the real vehicle; it is the view transform that hides it.
"""
import bpy, math, os
import t1_core as T          # rev 8: the rake coefficient has one home

TEXDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tex")

# SPEC r4 sec.3: measured (196,106,36) sRGB in sun -> faded orange-red /
# vermillion, hue ~26deg. NOT a deep crimson.
# rev 9: sRGB(196,49,36). See the note below and SPEC 10.12 -- the previous
# value's hue came off the retired 246x197 thumbnail and matches the reference
# GOLD folk-art hue to 2.9%, which is what contamination looks like on a
# thumbnail where the flank is ~100 px wide. Saturation is UNCHANGED at 0.816:
# SPEC 10.9 settled that and this does not re-open it. Revert with
# T1_RED=196,106,36.
RED = (0.5520, 0.0294, 0.0176)   # = sRGB(196,49,36), hue 5.0, sat 0.816
_RED_THUMB = (0.5520, 0.1441, 0.0176)   # sRGB(196,106,36), hue 26.2 (retired)
                                 # rev-3 shipped (0.5250,0.0395,0.0072) =
                                 # sRGB(192,56,20), hue 12.5 sat 0.894 -- a
                                 # DEEP CRIMSON, which SPEC 0.2 retires by
                                 # name. Its green channel was 3.6x low.


def _srgb_to_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


# rev 9: T1_RED="r,g,b" (sRGB 0-255) overrides the flank albedo, so the hue
# question below can be A/B'd without editing a locked constant.
#
# The locked (196,106,36) comes from the retired 246x197 thumbnail. Measured on
# ref_side.jpg instead, the red flank reads hue 4.0-4.3 deg in its least-lit
# patches and 19-23 deg where warm bounce is strong. The hue-invariant ratio
# (G-B)/(R-B) -- which any NEUTRAL additive term leaves unchanged, so SPEC
# 10.9's specular pedestal cannot move it -- is 0.067 in deep shade against
# 0.438 for the locked value. And 0.438 matches the reference GOLD folk-art
# motif's 0.450 to 2.9%: on a thumbnail where the flank is ~100 px wide and
# the gold covers much of it, that is what contamination looks like.
# Nothing is changed by default. See SPEC 10.12.
if os.environ.get("T1_RED"):
    RED = tuple(_srgb_to_lin(float(v))
                for v in os.environ["T1_RED"].split(","))
# measured (206,208,200) sRGB -> sun-bleached near-neutral off-white
CREAM = (0.6172, 0.6308, 0.5776) # = sRGB(206,208,200). rev-3 had R > G;
                                 # the measurement has G > R, and rev-3 was
                                 # 24 code values bright.
GOLD = (0.8600, 0.5400, 0.0600)

# two-tone break line:  belt line on the flanks, V-swage across the nose
#
# FRAME NOTE (measured 2026-08-09, not assumed).  build.py step 8b subtracts
# T.RIDE_DROP from every vertex AFTER the materials are assigned, but a shader
# reads Geometry->Position at RENDER time, i.e. from the already-dropped mesh.
# The shader therefore sees the DROPPED frame, and Position.Z is the true
# height above the ground plane (the cyclorama sits at z = 0 and the tyres
# bottom out at z = 0.010 +- one 9.9 mm pixel).
# Verified empirically: in the side ortho probe the painted cream/red break on
# the rear quarter (clear of the counter, tblend = 0 so the mix is pure Z_BELT)
# lands between pixel rows 128 and 130 with row 129 the mixed pixel; row 129 is
# z = 1.3859 against Z_BELT = 1.3860.  A shader reading the UN-dropped frame
# would have put it on row 135.6.  So height ramps below are written in
# TRUE ABOVE-GROUND METRES with NO ride-drop offset added.
# CORRECTED 2026-08-09, re-derived off the high-resolution photographs.
# All four are ABOVE-GROUND metres (see the frame note above).  The pressed
# swage in t1_shell.nose_shape.zV() carries the same three numbers + 0.065,
# because THAT is geometry and is cut before the drop.  If you change one,
# change the other in the same commit or the swage and the paint de-register.
# V_APEX <= 0.396 above ground is a HARD BOUND, not an estimate: the cream
# wedge is still 14 px wide where the bumper occludes it in ref_workshop.jpg
# and the bumper top measures 0.331 +- 0.020 above ground.  That bound is
# independent of any px/m conversion.  V_POW < 1 -- the profile is CONCAVE.
# rev 8: THE BELT IS A LINE, NOT A CONSTANT.
# Step 8b no longer subtracts a scalar -- it shears, because the vehicle sits
# nose-down ~1.9 deg (t1_core.rake_drop). A shader reading Position.Z off the
# sheared mesh therefore sees a break whose height FALLS as x rises:
#
#     break_z(x) = Z_BELT0 - RAKE_DZDX * x            (above ground)
#
# Z_BELT0 / V_APEX0 are the above-ground values AT x = 0, i.e.
# authored - RAKE_Z0, where the old constants were authored - RIDE_DROP. The
# rake term is subtracted once, AFTER the flank/nose mix, so it applies equally
# to both branches and V_APEX0 + V_RISE == Z_BELT0 keeps holding at every
# station -- which is what makes the swage arms land on the belt line.
RAKE_DZDX = T.RAKE_DZDX                 # single source of truth
Z_BELT0 = 1.2355                        # = 1.2720 authored - RAKE_Z0 0.0365
V_APEX0 = 0.3685                        # = 0.4050 authored - RAKE_Z0
V_RISE = 0.8670
V_POW = 0.60

# Above-ground value at any station, for probes and reports.
def z_belt(x):
    return Z_BELT0 - RAKE_DZDX * x


def v_apex(x):
    return V_APEX0 - RAKE_DZDX * x


# Back-compat scalars, evaluated at the station where the old uniform drop and
# the rake agree (t1_core.X_DROP_REF). Anything that wants a height at a
# specific x must call z_belt(x)/v_apex(x) -- a bare Z_BELT is now only correct
# at one station.
Z_BELT = z_belt(T.X_DROP_REF)           # == 1.2070, the rev-7 value
V_APEX = v_apex(T.X_DROP_REF)           # == 0.3400

assert abs((V_APEX0 + V_RISE) - Z_BELT0) < 1e-9, (
    "V_APEX0 + V_RISE must equal Z_BELT0: the V-swage arms have to land on the "
    "flank belt line at |y| = 0.86, at every station")
assert abs((V_APEX + V_RISE) - Z_BELT) < 1e-9
# The bumper-occlusion bound is a statement about the NOSE, so it is tested at
# the nose station, not at x = 0.
assert v_apex(2.108) <= 0.3960, "V_APEX at the nose above the bumper-occlusion bound"

# ---------------------------------------------------------------- WEATHER
# Tunables for the shared weathering field.  W_ALBEDO is the one that is
# actually measured against the reference: see the residual table in the
# handover.  Roughness modulation alone is nearly invisible at Specular IOR
# Level 0.21 / Roughness 0.42 because the body is diffuse-dominated.
W_N1_SCALE, W_N1_DETAIL, W_N1_ROUGH = 3.5, 6.0, 0.55
W_N2_SCALE, W_N2_DETAIL = 22.0, 4.0
W_N1_W, W_N2_W = 0.65, 0.35
W_ROUGH_SWING = 0.09           # +- about the material's base roughness
W_ALBEDO = float(os.environ.get("T1_W_ALB", 0.130))
                               # +- albedo half-range over the 0.30-0.70 map
                               # window.  The design entered 0.06; measured,
                               # that realises only 1.2 % albedo sd and 0.13 %
                               # display residual (see the report).  0.70
                               # realises 14.2 % albedo sd.
W_MAP_LO, W_MAP_HI = 0.30, 0.70
# rev 10.  This was 0.30 -- a 30 % opacity ceiling on hand-painted signwriting,
# put there in rev 8 to stop the folk art dragging the flank saturation down.
# It is the arithmetic cause of Donald's "far too faint and sparse": measured
# through the shader the gold read x1.455 against the adjacent red where the
# photograph reads x2.048, and at 0.30 even a PURE WHITE ink only reaches
# x2.15, so the measured contrast was unreachable by construction. The tile is
# now authored at measured coverage (29.1 % on the cab door, not the 0.0-0.2 %
# a scan of the OPEN door produced) and measured colour, so the ceiling has
# nothing left to protect against. SPEC 10.21.
W_ART = float(os.environ.get("T1_W_ART", 1.00))   # folk-art opacity ceiling

# curvature edge wear.  Pointiness RE-MEASURED off the built mesh 2026-08-09
# by rendering Geometry->Pointiness to a 32-bit EXR through the side ortho,
# at BOTH subdivision levels (mean / p95 / max over the sampled window):
#                          T1_SUB=1                T1_SUB=2
#   flat flank        0.5002 / .5004 / .5005   0.5001 / .5003 / .5005
#   front arch lip    0.5326 / .5926 / .6084   0.5324 / .5926 / .6084
#   rear arch lip     0.5031 / .5096 / .5099        (never reaches 0.52)
#   bumper front      0.5101 / .5463 / .5950   0.5085 / .5463 / .5950
#   counter lip       0.5794 / .6150 / .6690   0.5764 / .6150 / .6690
#   above 0.520          27.9 % of frame          24.2 % of frame
#   above 0.600           3.99 %                   3.94 %
# The design's figures (flank 0.503, arch lip 0.552, bumper crown 0.571, drip
# rail 0.591, counter lip 0.617) are close for the bumper and the counter, but
# the flank is 0.500 not 0.503 and the REAR arch lip never crosses 0.520 at
# all, so it gets no chips.  SUB=1 and SUB=2 agree to <0.003 everywhere --
# pointiness here is NOT mesh-density sensitive, because the subsurf runs
# before solidify and the arches / bumper / counter are unsubdivided detail
# geometry.  The 0.520 / 0.600 window is kept: it clears the flank by 20 sigma.
W_PT_LO, W_PT_HI = 0.520, 0.600
W_CHIP_SCALE, W_CHIP_DETAIL = 60.0, 3.0
W_CHIP_LO, W_CHIP_HI = 0.42, 0.58
W_CHIP_CUT = 0.35
# Pointiness is a PER-VERTEX quantity. On the subdivided shell it does what
# the design assumes, but on unsubdivided detail geometry every vertex is a
# corner, so the ramp saturates over the whole face: measured, the counter
# slab reads pw = 1.0 across its entire top (55 % of the top-down frame at
# pw > 0.5), which turned Wear 0.7 into 29 % chip coverage on a flat slab
# instead of a chipped lip. A second, low-frequency cluster gate breaks the
# chipping into runs -- which is also what the design asks for ("not a uniform
# pen line") -- and brings the slab back to a believable coverage without
# touching the per-material Wear weights.
W_CLUST_SCALE, W_CLUST_DETAIL = 7.0, 2.0
W_CLUST_LO, W_CLUST_HI = 0.44, 0.60
W_PRIMER = (0.1290, 0.1070, 0.0920)     # linear oxide grey
W_STEEL = (0.5600, 0.5620, 0.5680)      # bare steel
W_STEEL_LO, W_STEEL_HI = 0.80, 1.00     # deepest ~20 % of the wear ramp
W_STEEL_ROUGH = 0.55
# The pointiness histogram on this mesh is BIMODAL -- 49 % of the visible
# surface sits at 0.500-0.505 (flat panel) and the edges jump straight to
# 0.58-0.61.  "the deepest 20 % of the ramp" therefore selects ~100 % of the
# chips, not 20 % of them: measured 4.20 % steel against 4.42 % primer on the
# lower flank.  A second, finer mask cuts the bare-metal core back to a fifth
# of the chip, which is also what a real chip looks like: primer ring, small
# bright core.
W_CORE_SCALE, W_CORE_DETAIL, W_CORE_CUT = 110.0, 2.0, 0.573

# dust: measured tide line.  In CIELAB C*/(L*+16) on the real vehicle is flat
# to +-7 % from h = 0.40 m to h = 0.92 m and only collapses at 0.36 (-21 %).
# The 35 % luminance fall toward the rocker is ILLUMINATION, not pigment.
# So there is no dust on the flank above 0.48 m at all.
W_DUST_Z_HI, W_DUST_Z_LO = 0.480, 0.220      # true above-ground metres
W_DUST_RAG_SCALE, W_DUST_RAG_DETAIL, W_DUST_RAG_AMP = 6.0, 2.0, 0.045
W_DUST_NZ_LO, W_DUST_NZ_HI = 0.25, 0.85      # upward-normal ramp
W_DUST_UP_W = 0.85
W_DUST_MOT_SCALE, W_DUST_MOT_DETAIL = 14.0, 4.0
W_DUST_MOT_LO, W_DUST_MOT_HI = 0.35, 0.70
W_DUST_MOT_MIN, W_DUST_MOT_MAX = 0.35, 1.00
W_DUST_COL = (0.4400, 0.3900, 0.3100)        # pale limestone ochre
W_DUST_FAC_UP = float(os.environ.get("T1_W_DUP", 0.35))
W_DUST_FAC_LOW = float(os.environ.get("T1_W_DLO", 0.50))
W_DUST_ROUGH = 0.28                          # ADDITIVE, clamped at 0.85
W_ROUGH_CEIL = 0.85

# sun fade -- a DESIGN VALUE, not a measurement.  Neither in-service photo is
# in direct sun (ref_side.jpg open shade, ref_rear34.jpg under a palapa), so
# fade cannot be separated from exposure.  Kept well under the dust term.
W_FADE_SAT = float(os.environ.get("T1_W_FADESAT", 0.88))
W_FADE_VAL = float(os.environ.get("T1_W_FADEVAL", 1.04))

# orange peel.  rev-3 had Scale 190 with the noise Vector UNLINKED, so it fell
# back to Generated (bounding-box) coordinates: 22.3 / 9.2 / 8.1 mm on T1_body
# at 2.75:1, and the SAME material on gutter+-1 where it is 140:1.  Object
# coordinates fix the anisotropy.  Resolvable peel goes in the Bump; the
# 0.3-1.5 mm microstructure does NOT -- an A/B put a 0.5 mm bump at Strength
# 0.35 on the Monte-Carlo noise floor, where it only aliases.  Fold it into
# Roughness instead.
W_PEEL_SCALE, W_PEEL_DETAIL = 220.0, 2.0
W_PEEL_STRENGTH, W_PEEL_DIST = 0.12, 0.0006
W_MICRO_SCALE, W_MICRO_DETAIL = 1400.0, 1.0
W_MICRO_LO, W_MICRO_HI, W_MICRO_AMP = 0.35, 0.65, 0.035

# per-material wear weights (SPEC rev6 sec.3)
WEAR = dict(bumpercream=1.0, wheelcream=0.8, countercream=0.7, capred=0.6,
            capwhite=0.6, T1_paint=0.55, calidad=0.55, cream=0.3,
            roundelred=0.25)


def _nt(mat):
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (900, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (560, 0)
    bsdf.inputs["Subsurface Weight"].default_value = 0.0
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


def img_paint(name, filename, rough=0.50, spec=0.42):
    """Painted board carrying an image albedo, UV-mapped. rev 8: the lid boards.

    Roughness is driven off the image luminance rather than left constant --
    the dark ground on a hand-painted board is thicker, matter paint than the
    pale motifs, and a constant roughness is the physical definition of the
    plastic look SPEC sec.3 locks out.
    """
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    nt, b = _nt(m)
    tex = _img(nt, filename, -620, 60, ext='EXTEND')
    nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
    lum = nt.nodes.new("ShaderNodeRGBToBW"); lum.location = (-420, -180)
    nt.links.new(tex.outputs["Color"], lum.inputs[0])
    rr = _mr(nt, lum.outputs[0], 0.0, 1.0, rough + 0.10, rough - 0.10, -240, -180)
    nt.links.new(rr.outputs[0], b.inputs["Roughness"])
    b.inputs["Specular IOR Level"].default_value = spec
    return m


def emissive(name, colour, strength=8.0, base=(0.85, 0.84, 0.82)):
    """A lit festoon bulb: warm emission over a pearl-white envelope."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    nt, b = _nt(m)
    b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Roughness"].default_value = 0.22
    b.inputs["Specular IOR Level"].default_value = 0.45
    b.inputs["Emission Color"].default_value = (*colour, 1)
    b.inputs["Emission Strength"].default_value = strength
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


def _mr(nt, val, fmin, fmax, tmin, tmax, x=0, y=0, smooth=False, clamp=True):
    """MapRange (float).  smooth -> SMOOTHSTEP interpolation."""
    n = nt.nodes.new("ShaderNodeMapRange")
    n.location = (x, y)
    n.clamp = clamp
    if smooth:
        n.interpolation_type = 'SMOOTHSTEP'
    for src, sock in ((val, 0), (fmin, 1), (fmax, 2), (tmin, 3), (tmax, 4)):
        _feed(nt, src, n.inputs[sock])
    return n


def _noise(nt, vec, scale, detail, x, y, rough=None):
    """noise texture.  vec MUST be supplied -- an unlinked Vector silently
    falls back to Generated (bounding-box) coordinates, which is anisotropic
    and object-size dependent."""
    n = nt.nodes.new("ShaderNodeTexNoise")
    n.location = (x, y)
    n.inputs["Scale"].default_value = scale
    n.inputs["Detail"].default_value = detail
    if rough is not None:
        n.inputs["Roughness"].default_value = rough
    nt.links.new(vec, n.inputs["Vector"])
    return n


def _mixf(nt, fac, a, b, x=0, y=0):
    n = nt.nodes.new("ShaderNodeMix")
    n.data_type = 'FLOAT'
    n.location = (x, y)
    _feed(nt, fac, n.inputs[0])
    _feed(nt, a, n.inputs[2])
    _feed(nt, b, n.inputs[3])
    return n


def _mixc(nt, fac, a, b, x=0, y=0, blend='MIX'):
    n = nt.nodes.new("ShaderNodeMix")
    n.data_type = 'RGBA'
    n.blend_type = blend
    n.location = (x, y)
    n.inputs[0].default_value = 1.0
    _feed(nt, fac, n.inputs[0])
    if isinstance(a, tuple):
        n.inputs[6].default_value = (*a, 1)
    else:
        _feed(nt, a, n.inputs[6])
    if isinstance(b, tuple):
        n.inputs[7].default_value = (*b, 1)
    else:
        _feed(nt, b, n.inputs[7])
    return n


# =========================================================== WEATHER group
def weather_group(name="WEATHER"):
    """Shared weathering field.

    in : Base Color, Roughness, Dust, Wear, Fade, Peel
    out: Base Color, Roughness, Normal, Metallic

    Metallic is not in the original interface list but 2b requires the bare
    steel stage to read as metal rather than grey paint, and a node group
    cannot write a socket it does not expose.  It is 0 everywhere the steel
    mask is 0, so linking it is a no-op on every non-chipped material.
    """
    ng = bpy.data.node_groups.get(name)
    if ng:
        return ng
    ng = bpy.data.node_groups.new(name, "ShaderNodeTree")
    I = ng.interface
    s = I.new_socket("Base Color", in_out='INPUT', socket_type='NodeSocketColor')
    s.default_value = (*CREAM, 1)
    for nm, dv in (("Roughness", 0.42), ("Dust", 0.0), ("Wear", 0.0),
                   ("Fade", 0.0), ("Peel", 0.0)):
        s = I.new_socket(nm, in_out='INPUT', socket_type='NodeSocketFloat')
        s.default_value = dv
        s.min_value, s.max_value = 0.0, 2.0
    I.new_socket("Base Color", in_out='OUTPUT', socket_type='NodeSocketColor')
    I.new_socket("Roughness", in_out='OUTPUT', socket_type='NodeSocketFloat')
    I.new_socket("Normal", in_out='OUTPUT', socket_type='NodeSocketVector')
    I.new_socket("Metallic", in_out='OUTPUT', socket_type='NodeSocketFloat')

    nt = ng
    gi = ng.nodes.new("NodeGroupInput"); gi.location = (-2600, 0)
    go = ng.nodes.new("NodeGroupOutput"); go.location = (1800, 0)
    IN = dict(col=gi.outputs["Base Color"], rgh=gi.outputs["Roughness"],
              dust=gi.outputs["Dust"], wear=gi.outputs["Wear"],
              fade=gi.outputs["Fade"], peel=gi.outputs["Peel"])

    # ---- front end.  Object coordinates, never Generated.
    texco = ng.nodes.new("ShaderNodeTexCoord"); texco.location = (-2600, -600)
    OBJ = texco.outputs["Object"]
    geo = ng.nodes.new("ShaderNodeNewGeometry"); geo.location = (-2600, -900)
    psep = ng.nodes.new("ShaderNodeSeparateXYZ"); psep.location = (-2420, -860)
    ng.links.new(geo.outputs["Position"], psep.inputs[0])
    nsep = ng.nodes.new("ShaderNodeSeparateXYZ"); nsep.location = (-2420, -1040)
    ng.links.new(geo.outputs["Normal"], nsep.inputs[0])
    PT = geo.outputs["Pointiness"]

    # ---- 2a multi-octave roughness + albedo breakup ---------------------
    n1 = _noise(nt, OBJ, W_N1_SCALE, W_N1_DETAIL, -2200, 400, W_N1_ROUGH)
    n2 = _noise(nt, OBJ, W_N2_SCALE, W_N2_DETAIL, -2200, 120)
    a1 = _math(nt, 'MULTIPLY', n1.outputs["Fac"], W_N1_W, -1980, 400)
    a2 = _math(nt, 'MULTIPLY', n2.outputs["Fac"], W_N2_W, -1980, 240)
    mix = _math(nt, 'ADD', a1, a2, -1820, 320)

    rlo = _math(nt, 'SUBTRACT', IN['rgh'], W_ROUGH_SWING, -1820, 640)
    rhi = _math(nt, 'ADD', IN['rgh'], W_ROUGH_SWING, -1820, 780)
    rough = _mr(nt, mix, W_MAP_LO, W_MAP_HI, rlo, rhi, -1600, 700)

    alb = _mr(nt, mix, W_MAP_LO, W_MAP_HI, 1.0 - W_ALBEDO, 1.0 + W_ALBEDO,
              -1600, 320)
    col = _mixc(nt, 1.0, IN['col'], alb.outputs[0], -1380, 320, blend='MULTIPLY')

    # ---- 2d sun fade (UNDER the dust film) ------------------------------
    fz = _mr(nt, nsep.outputs["Z"], 0.0, 1.0, 0.0, 1.0, -1380, -180)
    ffac = _math(nt, 'MULTIPLY', fz, IN['fade'], -1200, -180, clamp=True)
    hs = ng.nodes.new("ShaderNodeHueSaturation"); hs.location = (-1020, 200)
    hs.inputs["Saturation"].default_value = W_FADE_SAT
    hs.inputs["Value"].default_value = W_FADE_VAL
    ng.links.new(ffac.outputs[0], hs.inputs["Fac"])
    ng.links.new(col.outputs[2], hs.inputs["Color"])

    # ---- 2b curvature edge wear -----------------------------------------
    pw = _mr(nt, PT, W_PT_LO, W_PT_HI, 0.0, 1.0, -2200, -420, smooth=True)
    cn = _noise(nt, OBJ, W_CHIP_SCALE, W_CHIP_DETAIL, -2200, -700)
    cm = _mr(nt, cn.outputs["Fac"], W_CHIP_LO, W_CHIP_HI, 0.0, 1.0,
             -2000, -700)
    cl = _noise(nt, OBJ, W_CLUST_SCALE, W_CLUST_DETAIL, -2200, -900)
    clm = _mr(nt, cl.outputs["Fac"], W_CLUST_LO, W_CLUST_HI, 0.0, 1.0,
              -2000, -900)
    cprod = _math(nt, 'MULTIPLY', cm, clm, -1820, -700)
    craw = _math(nt, 'MULTIPLY', pw, cprod, -1820, -560)
    # real chips have hard edges, not a fade
    hard = _math(nt, 'GREATER_THAN', craw, W_CHIP_CUT, -1640, -560)
    wear = _math(nt, 'MULTIPLY', hard, IN['wear'], -1460, -560, clamp=True)
    deep = _mr(nt, pw, W_STEEL_LO, W_STEEL_HI, 0.0, 1.0, -1640, -760,
               smooth=True)
    sn = _noise(nt, OBJ, W_CORE_SCALE, W_CORE_DETAIL, -1820, -920)
    core = _math(nt, 'GREATER_THAN', sn.outputs["Fac"], W_CORE_CUT,
                 -1640, -920)
    dcore = _math(nt, 'MULTIPLY', deep, core, -1460, -860)
    steel = _math(nt, 'MULTIPLY', wear, dcore, -1280, -760, clamp=True)

    cprim = _mixc(nt, wear, hs.outputs[0], W_PRIMER, -820, 200)
    csteel = _mixc(nt, steel, cprim.outputs[2], W_STEEL, -620, 200)

    # ---- 2e orange peel --------------------------------------------------
    pn = _noise(nt, OBJ, W_PEEL_SCALE, W_PEEL_DETAIL, -1200, -1100)
    pstr = _math(nt, 'MULTIPLY', IN['peel'], W_PEEL_STRENGTH, -1200, -1300)
    bump = ng.nodes.new("ShaderNodeBump"); bump.location = (-900, -1150)
    bump.inputs["Distance"].default_value = W_PEEL_DIST
    ng.links.new(pstr.outputs[0], bump.inputs["Strength"])
    ng.links.new(pn.outputs["Fac"], bump.inputs["Height"])

    mn = _noise(nt, OBJ, W_MICRO_SCALE, W_MICRO_DETAIL, -1200, -1500)
    mmr = _mr(nt, mn.outputs["Fac"], W_MICRO_LO, W_MICRO_HI,
              -W_MICRO_AMP, W_MICRO_AMP, -1000, -1500)
    mamt = _math(nt, 'MULTIPLY', mmr, IN['peel'], -820, -1500)
    r2 = _math(nt, 'ADD', rough.outputs[0], mamt, -640, 700)
    # bare steel is not chalky paint
    r3 = _mixf(nt, steel, r2, W_STEEL_ROUGH, -460, 700)

    # ---- 2c dust with a tide line ---------------------------------------
    rag = _noise(nt, OBJ, W_DUST_RAG_SCALE, W_DUST_RAG_DETAIL, -2200, -1300)
    ragc = _math(nt, 'SUBTRACT', rag.outputs["Fac"], 0.5, -2000, -1300)
    ragz = _math(nt, 'MULTIPLY_ADD', ragc, W_DUST_RAG_AMP, -1820, -1300)
    ng.links.new(psep.outputs["Z"], ragz.inputs[2])
    hgt = _mr(nt, ragz, W_DUST_Z_HI, W_DUST_Z_LO, 0.0, 1.0, -1640, -1300,
              smooth=True)
    upn = _mr(nt, nsep.outputs["Z"], W_DUST_NZ_LO, W_DUST_NZ_HI, 0.0, 1.0,
              -1640, -1480)
    upw = _math(nt, 'MULTIPLY', upn, W_DUST_UP_W, -1460, -1480)
    # independent loading paths -> MAXIMUM, not multiply
    dmax = _math(nt, 'MAXIMUM', hgt, upw, -1280, -1380, clamp=True)
    mot = _noise(nt, OBJ, W_DUST_MOT_SCALE, W_DUST_MOT_DETAIL, -1640, -1660)
    motm = _mr(nt, mot.outputs["Fac"], W_DUST_MOT_LO, W_DUST_MOT_HI,
               W_DUST_MOT_MIN, W_DUST_MOT_MAX, -1460, -1660)
    d1 = _math(nt, 'MULTIPLY', dmax, motm, -1100, -1380)
    dust = _math(nt, 'MULTIPLY', d1, IN['dust'], -920, -1380, clamp=True)
    # heavier film at the rocker than on the upward faces
    dfac0 = _mr(nt, hgt, 0.0, 1.0, W_DUST_FAC_UP, W_DUST_FAC_LOW, -740, -1560)
    dfac = _math(nt, 'MULTIPLY', dust, dfac0, -560, -1480, clamp=True)
    cdust = _mixc(nt, dfac, csteel.outputs[2], W_DUST_COL, -380, 200)

    # dust roughness is ADDITIVE so it stacks on the breakup
    dr = _math(nt, 'MULTIPLY', dust, W_DUST_ROUGH, -380, 700)
    r4 = _math(nt, 'ADD', r3, dr, -220, 700)
    r5 = _math(nt, 'MINIMUM', r4, W_ROUGH_CEIL, -60, 700)
    r6 = _math(nt, 'MAXIMUM', r5, 0.030, 100, 700)

    # index, not name: an output socket may share its name with an input and
    # Blender is free to disambiguate one of them
    ng.links.new(cdust.outputs[2], go.inputs[0])       # Base Color
    ng.links.new(r6.outputs[0], go.inputs[1])          # Roughness
    ng.links.new(bump.outputs[0], go.inputs[2])        # Normal
    ng.links.new(steel.outputs[0], go.inputs[3])       # Metallic
    return ng


def _bsdf(m):
    return next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')


def apply_weather(m, dust=0.0, wear=0.0, fade=0.0, peel=0.0, normal=True):
    """Splice the WEATHER group between the material's colour/roughness
    sources and its Principled BSDF."""
    nt = m.node_tree
    b = _bsdf(m)
    g = nt.nodes.new("ShaderNodeGroup")
    g.node_tree = weather_group()
    g.location = (200, 260)

    cs = b.inputs["Base Color"]
    if cs.links:
        src = cs.links[0].from_socket
        nt.links.remove(cs.links[0])
        nt.links.new(src, g.inputs["Base Color"])
    else:
        g.inputs["Base Color"].default_value = cs.default_value[:]
    g.inputs["Roughness"].default_value = b.inputs["Roughness"].default_value
    g.inputs["Dust"].default_value = dust
    g.inputs["Wear"].default_value = wear
    g.inputs["Fade"].default_value = fade
    g.inputs["Peel"].default_value = peel

    nt.links.new(g.outputs[0], b.inputs["Base Color"])
    nt.links.new(g.outputs[1], b.inputs["Roughness"])
    if normal:
        nt.links.new(g.outputs[2], b.inputs["Normal"])
    if wear > 0.0:
        nt.links.new(g.outputs[3], b.inputs["Metallic"])
    return m


# ===================================================== non-group variants
def _frontend(nt, x=-1900):
    texco = nt.nodes.new("ShaderNodeTexCoord"); texco.location = (x, -400)
    geo = nt.nodes.new("ShaderNodeNewGeometry"); geo.location = (x, -700)
    psep = nt.nodes.new("ShaderNodeSeparateXYZ"); psep.location = (x + 180, -660)
    nt.links.new(geo.outputs["Position"], psep.inputs[0])
    nsep = nt.nodes.new("ShaderNodeSeparateXYZ"); nsep.location = (x + 180, -840)
    nt.links.new(geo.outputs["Normal"], nsep.inputs[0])
    return texco.outputs["Object"], psep, nsep, geo


def _breakup(nt, obj, base_rough, swing=W_ROUGH_SWING, x=-1600):
    """the 2a field, reused by the non-group variants"""
    n1 = _noise(nt, obj, W_N1_SCALE, W_N1_DETAIL, x, 300, W_N1_ROUGH)
    n2 = _noise(nt, obj, W_N2_SCALE, W_N2_DETAIL, x, 60)
    a1 = _math(nt, 'MULTIPLY', n1.outputs["Fac"], W_N1_W, x + 200, 300)
    a2 = _math(nt, 'MULTIPLY', n2.outputs["Fac"], W_N2_W, x + 200, 140)
    mix = _math(nt, 'ADD', a1, a2, x + 380, 220)
    rough = _mr(nt, mix, W_MAP_LO, W_MAP_HI, base_rough - swing,
                base_rough + swing, x + 560, 220)
    return mix, rough


def tarnished(name, base, rough_lo, rough_hi, spec=0.5):
    """chrome / nickel tarnish.  Chrome wears to NICKEL: it dulls and pits,
    it does not chip to primer grey, so the WEATHER group is wrong here."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = simple(name, base, rough=rough_lo, metal=1.0, spec=spec)
    nt = m.node_tree
    b = _bsdf(m)
    obj, psep, nsep, geo = _frontend(nt)
    n1 = _noise(nt, obj, W_N1_SCALE, W_N1_DETAIL, -1600, 300, W_N1_ROUGH)
    n2 = _noise(nt, obj, W_N2_SCALE, W_N2_DETAIL, -1600, 60)
    a1 = _math(nt, 'MULTIPLY', n1.outputs["Fac"], W_N1_W, -1400, 300)
    a2 = _math(nt, 'MULTIPLY', n2.outputs["Fac"], W_N2_W, -1400, 140)
    mix = _math(nt, 'ADD', a1, a2, -1220, 220)
    rgh = _mr(nt, mix, W_MAP_LO, W_MAP_HI, rough_lo, rough_hi, -1040, 220)
    # dark pit speckle
    pit = _noise(nt, obj, 130.0, 2.0, -1600, -160)
    pm = _math(nt, 'GREATER_THAN', pit.outputs["Fac"], 0.615, -1400, -160)
    pmf = _math(nt, 'MULTIPLY', pm, 0.55, -1220, -160)
    col = _mixc(nt, pmf, base, (0.0900, 0.0870, 0.0820), -860, 220)
    rgh2 = _mixf(nt, pmf, rgh, 0.42, -860, 0)
    nt.links.new(col.outputs[2], b.inputs["Base Color"])
    nt.links.new(rgh2.outputs[0], b.inputs["Roughness"])
    b.inputs["Metallic"].default_value = 1.0
    return m


def dust_film(name, base, rough, spec=0.25, fac_up=0.22, fac_low=0.34,
              drough=0.10):
    """tyre / rubber: a sidewall dust film only.  Z ramp + upward term, no
    wear, no peel, no fade.  Blackwall per SPEC 0.2."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = simple(name, base, rough=rough, spec=spec)
    nt = m.node_tree
    b = _bsdf(m)
    obj, psep, nsep, geo = _frontend(nt)
    mix, rgh = _breakup(nt, obj, rough, swing=0.06)
    rag = _noise(nt, obj, W_DUST_RAG_SCALE, W_DUST_RAG_DETAIL, -1600, -1100)
    ragc = _math(nt, 'SUBTRACT', rag.outputs["Fac"], 0.5, -1420, -1100)
    ragz = _math(nt, 'MULTIPLY_ADD', ragc, W_DUST_RAG_AMP, -1240, -1100)
    nt.links.new(psep.outputs["Z"], ragz.inputs[2])
    hgt = _mr(nt, ragz, W_DUST_Z_HI, W_DUST_Z_LO, 0.0, 1.0, -1060, -1100,
              smooth=True)
    upn = _mr(nt, nsep.outputs["Z"], W_DUST_NZ_LO, W_DUST_NZ_HI, 0.0, 1.0,
              -1060, -1280)
    upw = _math(nt, 'MULTIPLY', upn, W_DUST_UP_W, -880, -1280)
    dmax = _math(nt, 'MAXIMUM', hgt, upw, -700, -1180, clamp=True)
    mot = _noise(nt, obj, W_DUST_MOT_SCALE, W_DUST_MOT_DETAIL, -1060, -1460)
    motm = _mr(nt, mot.outputs["Fac"], W_DUST_MOT_LO, W_DUST_MOT_HI,
               W_DUST_MOT_MIN, W_DUST_MOT_MAX, -880, -1460)
    dust = _math(nt, 'MULTIPLY', dmax, motm, -520, -1180, clamp=True)
    dfac0 = _mr(nt, hgt, 0.0, 1.0, fac_up, fac_low, -520, -1360)
    dfac = _math(nt, 'MULTIPLY', dust, dfac0, -340, -1280, clamp=True)
    col = _mixc(nt, dfac, base, W_DUST_COL, -180, 200)
    dr = _math(nt, 'MULTIPLY', dust, drough, -180, 0)
    r2 = _math(nt, 'ADD', rgh, dr, 0, 0)
    r3 = _math(nt, 'MINIMUM', r2, W_ROUGH_CEIL, 160, 0)
    nt.links.new(col.outputs[2], b.inputs["Base Color"])
    nt.links.new(r3.outputs[0], b.inputs["Roughness"])
    return m


def canvas_mat(name="canvas", base=(0.6600, 0.6420, 0.5900)):
    """ragtop duck: woven fibre + water staining, no chips, no peel"""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = simple(name, base, rough=0.86, spec=0.22)
    nt = m.node_tree
    b = _bsdf(m)
    obj, psep, nsep, geo = _frontend(nt)
    # anisotropic weave: stretch the coordinates so warp and weft differ
    mp = nt.nodes.new("ShaderNodeMapping"); mp.location = (-1720, -400)
    mp.inputs["Scale"].default_value = (1.0, 1.0, 0.28)
    nt.links.new(obj, mp.inputs["Vector"])
    weave = _noise(nt, mp.outputs[0], 150.0, 2.0, -1520, -400)
    wm = _mr(nt, weave.outputs["Fac"], 0.30, 0.70, 0.90, 1.08, -1320, -400)
    # water staining: low-frequency blotches that run downward
    stain = _noise(nt, obj, 4.5, 5.0, -1520, -700, 0.62)
    sm = _mr(nt, stain.outputs["Fac"], 0.44, 0.66, 0.0, 1.0, -1320, -700,
             smooth=True)
    scol = _mixc(nt, sm, base, (0.4150, 0.3860, 0.3300), -1000, 200)
    tex = _mixc(nt, 1.0, scol.outputs[2], wm.outputs[0], -800, 200,
                blend='MULTIPLY')
    mix, rgh = _breakup(nt, obj, 0.86, swing=0.05)
    sr = _math(nt, 'MULTIPLY_ADD', sm, 0.06, -600, 0)
    nt.links.new(rgh.outputs[0], sr.inputs[2])
    r2 = _math(nt, 'MINIMUM', sr, 0.94, -420, 0)
    nt.links.new(tex.outputs[2], b.inputs["Base Color"])
    nt.links.new(r2.outputs[0], b.inputs["Roughness"])
    return m


def interior_wear(name, base, rough, metal=0.0, spec=0.5):
    """galley stainless / dark interior: USE wear, not weather.  Scuff and
    handling polish, no dust tide line, no sun fade, no chips to primer."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = simple(name, base, rough=rough, metal=metal, spec=spec)
    nt = m.node_tree
    b = _bsdf(m)
    obj, psep, nsep, geo = _frontend(nt)
    mix, rgh = _breakup(nt, obj, rough, swing=0.07)
    # directional scuff: squash the coordinates along X so it streaks
    mp = nt.nodes.new("ShaderNodeMapping"); mp.location = (-1720, -1100)
    mp.inputs["Scale"].default_value = (1.0, 34.0, 34.0)
    nt.links.new(obj, mp.inputs["Vector"])
    scuff = _noise(nt, mp.outputs[0], 9.0, 3.0, -1520, -1100)
    sm = _mr(nt, scuff.outputs["Fac"], 0.38, 0.62, -0.055, 0.055, -1320, -1100)
    r2 = _math(nt, 'ADD', rgh, sm, -1000, 0)
    r3 = _math(nt, 'MAXIMUM', r2, 0.05, -840, 0)
    alb = _mr(nt, mix, W_MAP_LO, W_MAP_HI, 0.93, 1.07, -1000, 200)
    col = _mixc(nt, 1.0, base, alb.outputs[0], -820, 200, blend='MULTIPLY')
    nt.links.new(col.outputs[2], b.inputs["Base Color"])
    nt.links.new(r3.outputs[0], b.inputs["Roughness"])
    return m


# ============================================================ body paint
def body_paint(name="T1_paint"):
    """
    Cream above the break line, Tacombi red below, gold folk-art swirls
    box-projected over the red.  Weathering (breakup, chips, dust, fade,
    orange peel) comes from the shared WEATHER group.
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
    zv.inputs[2].default_value = V_APEX0          # value at x = 0; rake applied below

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
    mixz.inputs[2].default_value = Z_BELT0        # value at x = 0
    nt.links.new(tblend.outputs[0], mixz.inputs[0])
    nt.links.new(zv.outputs[0], mixz.inputs[3])

    # rev 8: apply the rake ONCE, after the mix, so it lands on both the flank
    # belt and the nose V-swage and V_APEX0 + V_RISE == Z_BELT0 keeps holding
    # at every station. break_z(x) = mix - RAKE_DZDX * x.
    rake = _math(nt, 'MULTIPLY_ADD', sep.outputs["X"], -RAKE_DZDX, -60, 90)
    nt.links.new(mixz.outputs[0], rake.inputs[2])

    # hard-ish edge:  cream = 1 when z > break
    dz = _math(nt, 'SUBTRACT', sep.outputs["Z"], rake.outputs[0], -20, 340)
    edge = _math(nt, 'DIVIDE', dz, 0.0045, 140, 340)
    edge = _math(nt, 'ADD', edge, 0.5, 300, 340, clamp=True)

    # gold swirl decal, box-projected in object space
    texco = nt.nodes.new("ShaderNodeTexCoord"); texco.location = (-1600, -420)
    mp = nt.nodes.new("ShaderNodeMapping"); mp.location = (-1420, -420)
    mp.inputs["Location"].default_value = (0.185, 0.410, 0.263)
    # rev 8 (audit livery-7): 0.63 => a 1.587 m period, ~2.7 visible repeats
    # across the flank -- wallpaper, not signwriting. 0.42 => 2.38 m, 1.8
    # repeats, and the non-monotonic density mask below breaks the rest.
    # rev 8b: swirl.png is now PLACED signwriting (one dominant paisley per
    # quarter + rosettes + dark commas), not a seamless field. 0.42 repeated it
    # 1.8x across the flank and distinct motifs repeat visibly. 0.26 => a
    # 3.85 m period, i.e. essentially one pass over the 4.22 m flank.
    mp.inputs["Scale"].default_value = (0.2600, 0.2600, 0.2600)
    nt.links.new(texco.outputs["Object"], mp.inputs["Vector"])
    # rev 10 (audit materials-14): both flanks carried the SAME art, mirrored.
    # On a two-angle hero set that is fatal -- the studio view sees +Y and the
    # front three-quarter sees -Y, and a viewer comparing them sees the same
    # drawing twice. folk_gen.py now writes two tiles with different
    # compositions obeying identical measured statistics; they are selected on
    # the SIGN OF POSITION Y, which is unambiguous (the surface normal is not,
    # on a crowned flank). Whitened peak cross-correlation between the two
    # drawings sampled onto the same body grid falls 0.175 -> 0.064, and the
    # mirrored pairing no longer wins.
    swirl = _img(nt, "swirl.png", -1180, -420, projection='BOX',
                 blend=0.10, ext='REPEAT')
    nt.links.new(mp.outputs[0], swirl.inputs["Vector"])
    swirl_b = _img(nt, "swirl_b.png", -1180, -640, projection='BOX',
                   blend=0.10, ext='REPEAT')
    nt.links.new(mp.outputs[0], swirl_b.inputs["Vector"])
    sideY = _math(nt, 'GREATER_THAN', sep.outputs["Y"], 0.0, -1180, -760)

    # --- density mask (SPEC sec.3): heaviest on the nose, trailing along the
    #     belt, sparse at the tail. Applied as a spatially varying cutoff on a
    #     low-frequency noise so whole motifs drop out rather than fading.
    # rev 8: MEASURED off ref_side.jpg, gold coverage as a fraction of the
    # red+gold flank, sampled in 40 px columns:
    #
    #   X +1.47 .. -0.40   0.0-0.2 %      <- bare red, the script sits here
    #   X -0.59            4.7 %
    #   X -0.96           13.8 %
    #   X -1.71           25.9 %
    #   X -1.90           36.9 %          <- the rear-quarter bouquet
    #
    # plus a separate scroll on the cab door, forward of X +0.9 (missed by the
    # scan above -- the door is swung open in that photograph and sits outside
    # the band). rev 7 ran a SINGLE MapRange, 0.34 at the tail rising to 1.00 at
    # the nose: monotonic and exactly backwards, densest where the reference is
    # bare and sparsest where the bouquet is. Two lobes, combined with MAXIMUM.
    fx = nt.nodes.new("ShaderNodeMapRange"); fx.location = (-1180, -900)
    fx.interpolation_type = 'SMOOTHSTEP'; fx.clamp = True
    fx.inputs[1].default_value = -0.30
    fx.inputs[2].default_value = -2.05
    fx.inputs[3].default_value = 0.05
    fx.inputs[4].default_value = 1.00
    nt.links.new(sep.outputs["X"], fx.inputs[0])

    # second lobe: the cab-door scroll, forward of X +0.55
    fx2 = nt.nodes.new("ShaderNodeMapRange"); fx2.location = (-1180, -1060)
    fx2.interpolation_type = 'SMOOTHSTEP'; fx2.clamp = True
    fx2.inputs[1].default_value = 0.55
    fx2.inputs[2].default_value = 1.75
    fx2.inputs[3].default_value = 0.05
    fx2.inputs[4].default_value = 0.60
    nt.links.new(sep.outputs["X"], fx2.inputs[0])
    fx = _math(nt, 'MAXIMUM', fx.outputs[0], fx2.outputs[0], -1020, -960)

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
    # rev 10: `keep` is RETIRED, not deleted -- the nodes above are left in
    # place and unlinked so the next reader can see what was there. The mask
    # was a second density profile multiplied on top of the tile's own, and
    # after rev 10 the tile IS the measurement: 29.1 % gold on the cab door
    # with the measured 42 %->5 % gradient across it, 11.44 % on the lower
    # nose, and the rear-quarter bouquet. Multiplying by `keep` applied a
    # wrong profile to a right one. Worse, `fx2`'s door lobe topped out at
    # 0.60 over a window starting at X +0.55 -- its maximum sat on the flank
    # BEHIND the door, not on the door.
    mixA = nt.nodes.new("ShaderNodeMix"); mixA.location = (40, -1240)
    mixA.data_type = 'FLOAT'
    nt.links.new(sideY.outputs[0], mixA.inputs[0])
    nt.links.new(swirl_b.outputs["Alpha"], mixA.inputs[2])
    nt.links.new(swirl.outputs["Alpha"], mixA.inputs[3])
    amask = _math(nt, 'MULTIPLY', mixA.outputs[0], 1.0, 100, -1240)
    # SPEC sec.3 asks for a graded BOUQUET, not wallpaper. Without a ceiling
    # the dense regions run at the tile's own alpha, which covers the red
    # almost completely and drags the flank from sat 0.82 to 0.27.
    amask = _math(nt, 'MULTIPLY', amask.outputs[0], W_ART, 240, -1240)

    # red + gold
    mix_g = nt.nodes.new("ShaderNodeMix"); mix_g.location = (-820, -420)
    mix_g.data_type = 'RGBA'
    mix_g.inputs[6].default_value = (*RED, 1)
    if swirl.image:
        hs = nt.nodes.new("ShaderNodeHueSaturation"); hs.location = (-980, -560)
        # SPEC rev4 sec.3: gold + yellow, not pale cream wallpaper. The
        # source tile is light; 1.22 left it reading as beige on the red.
        # rev 10: was 2.45 / 0.94. Saturation 2.45 clamps S to 1.0 for EVERY
        # ink class, not just the gold -- the cream rosettes (218,181,116)
        # came out fully saturated orange and the dark brown lost its blue
        # channel entirely. The tile is now authored at the measured
        # chromaticities (gold 213,161,7; cream 218,181,116; dark 94,24,19),
        # so it must pass through untouched.
        hs.inputs["Saturation"].default_value = 1.00
        hs.inputs["Value"].default_value = 1.00
        mixC = nt.nodes.new("ShaderNodeMix"); mixC.location = (-1120, -560)
        mixC.data_type = 'RGBA'
        nt.links.new(sideY.outputs[0], mixC.inputs[0])
        nt.links.new(swirl_b.outputs["Color"], mixC.inputs[6])
        nt.links.new(swirl.outputs["Color"], mixC.inputs[7])
        nt.links.new(mixC.outputs[2], hs.inputs["Color"])
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

    # SPEC rev4 sec.3: WEATHERED, not show gloss. The rev-3 values
    # (rough .105, coat .75 @ .025) put a mirror clearcoat on the body, which
    # in a white studio laid an achromatic white veil over the paint -- that,
    # not the base colour, is why the red measured sat 0.37 against the
    # reference's 0.82 and read salmon. Chalky finish restores the chroma.
    bsdf.inputs["Roughness"].default_value = 0.420
    bsdf.inputs["Metallic"].default_value = 0.0
    # rev 8 (audit materials-7): was 0.21, i.e. F0 = 0.0168 / IOR 1.29. Every
    # dielectric paint is F0 ~ 0.04. Fixing an environment problem inside the
    # BSDF cost the panels all their specular structure.
    bsdf.inputs["Specular IOR Level"].default_value = float(
        os.environ.get("T1_SPEC", 0.50))
    bsdf.inputs["Coat Weight"].default_value = 0.02
    bsdf.inputs["Coat Roughness"].default_value = 0.300
    # orange peel now lives in the WEATHER group (Object coordinates, split
    # into a resolvable Bump term and a sub-pixel Roughness term)
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


def paint_calidad(name="calidad"):
    """'100% Calidad' on SOLID cream sheet metal aft of bay 3 (SPEC 0.2 and
    sec.3).  rev-3 made this frosted glass with Transmission 0.88; that is a
    retired reading and it rendered the panel 51.9 sRGB code values darker
    than the surrounding cream (55.0 % of its linear reflectance) inside a
    hard rectangular border.  It is paint, matched to T1_paint so it ages
    with the sheet metal it is painted on."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    nt, b = _nt(m)
    tex = _img(nt, "calidad.png", -420, -140)
    mix = _mixc(nt, 0.0, CREAM, CREAM, 60, 60)
    if tex.image:
        nt.links.new(tex.outputs["Alpha"], mix.inputs[0])
        nt.links.new(tex.outputs["Color"], mix.inputs[7])
    nt.links.new(mix.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.420
    b.inputs["Metallic"].default_value = 0.0
    b.inputs["Transmission Weight"].default_value = 0.0
    b.inputs["Specular IOR Level"].default_value = 0.50   # rev 8, see above
    b.inputs["Coat Weight"].default_value = 0.02
    b.inputs["Coat Roughness"].default_value = 0.300
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
    # chrome wears to NICKEL, so a primer-grey chip is wrong: tarnish instead
    M["chrome"] = tarnished("chrome", (0.860, 0.868, 0.880), 0.14, 0.30)
    M["chrome_d"] = tarnished("chrome_dull", (0.760, 0.768, 0.780), 0.20, 0.38)
    # rev 8 (audit materials-10): 0.004 is the Blender default and renders a
    # black mirror -- the windscreen was bimodal void+blob.
    M["glass"] = simple("glass", (0.780, 0.845, 0.815), rough=0.022,
                        transmit=1.0, ior=1.47, spec=0.35)
    M["rubber"] = dust_film("rubber", (0.0175, 0.0175, 0.0185), 0.78,
                            spec=0.22)
    M["tyre"] = dust_film("tyre", (0.0225, 0.0225, 0.0240), 0.70, spec=0.25)
    # rev 8 (audit materials-11): 0.085 / coat 0.85 was the lowest-roughness
    # non-metal in the file, on a vehicle SPEC sec.3 locks as WEATHERED. The
    # hubcaps ARE the glossiest thing on it, so this stays above the body's
    # 0.420 -- but show-gloss is retired.
    M["capred"] = simple("capred", (0.4750, 0.0290, 0.0225), rough=0.165,
                         coat=0.50, spec=0.55)
    M["capwhite"] = simple("capwhite", (0.8900, 0.8880, 0.8720), rough=0.115,
                           coat=0.7, spec=0.55)
    # rev 8: `canvas` RETIRED. It skinned a folding ragtop that SPEC sec.0.2
    # retired in rev 4; the roof is cut into rigid hinged steel lids. Removing
    # the material as well as the geometry is what stops it coming back.

    # rev 8: the lid boards. Painted board, matte, NOT emissive -- the warm
    # read in the reference is the scene light, not the paint.
    M["lidmural"] = img_paint("lidmural", "lidmural.png", rough=0.52)
    M["lidsign"] = img_paint("lidsign", "lidsign.png", rough=0.48)

    # rev 8: brass was defined locally in t1_detail._brass() because this
    # function had no brass key, which made it the last illegitimate
    # constant-roughness material in the scene. Folded in, and given a
    # roughness field like every other real surface.
    M["brass"] = tarnished("brass", (0.6600, 0.4750, 0.1750), 0.255, 0.34)

    # rev 8: the drip-rail bulb string renders unlit pearl white. In both
    # in-service photographs the bulbs are LIT and read warm -- they are the
    # brightest thing on the vehicle after the cream. Emissive, low power: they
    # are festoon bulbs in daylight, not a key light.
    M["bulb"] = emissive("bulb", (1.000, 0.760, 0.442), strength=9.0,
                         base=(0.900, 0.880, 0.840))
    M["script"] = silver_script()
    M["calidad"] = paint_calidad()
    # old D4: at 0.03 albedo the galley was a black void behind the hatches.
    # Lifted so the openings read as depth once fill_galley is on.
    M["dark"] = interior_wear("interior_dark", (0.1150, 0.1080, 0.1000), 0.78)
    M["amber"] = simple("amber", (0.9200, 0.3400, 0.0250), rough=0.09,
                        transmit=0.75, ior=1.49)
    M["ruby"] = simple("ruby", (0.7000, 0.0350, 0.0250), rough=0.09,
                       transmit=0.72, ior=1.49)
    M["lens"] = simple("lens", (0.900, 0.918, 0.930), rough=0.018,
                       transmit=0.96, ior=1.52, spec=0.42)
    # sealed inside the lamp bowl -- nothing weathers it
    M["reflector"] = simple("reflector", (0.960, 0.962, 0.968), rough=0.055,
                            metal=1.0)
    # brushed galley stainless, not a mirror: at rough 0.28 in an unlit box
    # the hatches filled with specular blobs instead of reading as an interior
    M["steel"] = interior_wear("steel", (0.560, 0.562, 0.568), 0.46, metal=1.0)

    # ------------------------------------------------------- weathering
    # full group: colour breakup + edge wear + dust + fade + orange peel
    for k in ("paint", "bumpercream", "cream", "roundelred", "calidad"):
        apply_weather(M[k], dust=1.0, wear=WEAR[M[k].name], fade=1.0, peel=1.0)
    # group minus peel (not sprayed sheet metal), dust weighted up
    for k in ("countercream", "wheelcream", "capred", "capwhite"):
        apply_weather(M[k], dust=1.4, wear=WEAR[M[k].name], fade=1.0, peel=0.0)
    # hand-painted silver: inherit the panel's dust and roughness field so it
    # does not float, but chip the paint UNDER it, not the silver
    apply_weather(M["script"], dust=1.0, wear=0.0, fade=0.5, peel=0.0)
    return M


def assign(ob, mat):
    ob.data.materials.clear()
    ob.data.materials.append(mat)
