"""probe_rev58_gloss.py -- rev 57b.  ITEM A's ablation, ready to run.

RULE 36: before tuning a constant against a gate, ABLATE IT AND CHECK THE GATE
MOVES.  Rev 57 lost item B to skipping that.  So this probe does not tune
anything -- it renders the SAME scene with the paint's finish overridden, so
`gloss_compare.py` can be run on each frame and the lever's authority measured
before anyone argues about a value.

IT CHANGES NO SOURCE.  The overrides are applied to the BUILT `T1_paint`
material after build.py has run, so the shipped constants are untouched and
nothing can be left behind in the tree by accident.

    T1_SUB=1 T1_GL_COATW=1.0 T1_GL_COATR=0.03 T1_GL_RGH=0.25 T1_GL_PFX=g1 \
      /tmp/blender/blender -b -P probe_rev58_gloss.py
    python3 gloss_compare.py out/g1_hero.png

WHAT TO REPORT, BOTH OF THEM, EVERY RUN.  `gloss_compare.py` for the gloss and
`flank_compare.py`'s own G/R block for the chroma -- because `t1_mats.py` says
in its own words that the chalky finish is what restores the red's saturation,
so the two may trade.  GLOSS is fair game; COLOUR is the owner's call (W6).
If they trade, that is a question for him, not a number to split.

CEILING: the rig's `top` softbox is 13.0 x 8.5 m, so even a mirror-smooth
paint gives a BROAD highlight here.  This cannot reach the photograph and is
not meant to -- find where the ceiling is and report it.
"""
import os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.environ.setdefault("T1_SUB", "1")
# build the scene exactly as shipped, WITHOUT its own preview render
_prev = os.environ.pop("T1_PREVIEW", None)
exec(compile(open(os.path.join(ROOT, "build.py")).read(), "build.py", "exec"))

import bpy
import studio as ST
P = print


# ----------------------------------------------------------------- rev 57b
# BUILD THE RIG.  F51: `build.py` constructs the cyclorama, the lighting, the
# cabin fill and the camera INSIDE its `if os.environ.get("T1_PREVIEW"):`
# block, so anything that execs build.py to MEASURE something -- rather than
# to ask for a preview -- gets a scene with no lights in it.
#
# That is not a hypothetical.  This script's first delivery render came back
# with a BLACK BUS lit only by its own emissive bulb string, and every
# automated check passed it: stitch.py exited 0, the seam detector read a
# clean z = 3.63, and the job ran 2.94x FASTER than the lit one -- because an
# unlit scene is cheap.  Only LOOKING at the frame found it.  It is also the
# same root cause as F05, `mottle_measure.py`'s dead beauty arm, whose note
# says "shader_solve._render() builds no studio rig".
#
# rev 58 DID factor them into one function.  This calls studio.rig(), the
# single definition, so there is no longer a copy here to drift.  The unlit
# case is now refused by studio.assert_lit() inside render_set().
_KEY = float(os.environ.get("T1_KEY", "1.0"))
if os.environ.get("T1_SCENE", "studio") != "studio":
    raise SystemExit("FATAL: this script mirrors build.py's STUDIO rig only")
# rev 58, F51: ONE definition, in studio.rig().  This used to be four calls
# copied out of build.py, with a verify_clone row comparing the copies so they
# could not rot -- a workaround for the absence of this function.
ST.rig(key=_KEY, scene="studio", log=P)

def _f(v, d):
    """v is the RAW value already read from the environment by name below.
    The read is written out literally at each call site, not folded into a
    helper: `verify_clone.sh` asserts every T1_ switch a brief names appears
    as `os.environ.get("NAME")` in source, and a helper that takes the name
    as a variable hides it from that row.  Rev 57b found this the hard way --
    the helper form passed a loosened copy of the check and FAILED the
    repository's own verifier, i.e. two instruments disagreeing because one
    of them had been relaxed.  Match the convention instead of relaxing it."""
    return d if v is None else float(v)


m = bpy.data.materials.get("T1_paint")
if m is None:
    raise SystemExit("FATAL: no T1_paint in the built scene -- refusing")
b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')

BEFORE = {k: b.inputs[k].default_value
          for k in ("Roughness", "Specular IOR Level", "Coat Weight", "Coat Roughness")}
OVER = {
    "Roughness":          _f(os.environ.get("T1_GL_RGH"),   BEFORE["Roughness"]),
    "Specular IOR Level": _f(os.environ.get("T1_GL_SPEC"),  BEFORE["Specular IOR Level"]),
    "Coat Weight":        _f(os.environ.get("T1_GL_COATW"), BEFORE["Coat Weight"]),
    "Coat Roughness":     _f(os.environ.get("T1_GL_COATR"), BEFORE["Coat Roughness"]),
}

P("=" * 74)
P("  T1_paint finish -- the material that carries the WHOLE two-tone body")
P("=" * 74)
P("  %-22s %10s %10s %s" % ("input", "shipped", "this run", ""))
moved = 0
for k in OVER:
    ch = abs(OVER[k] - BEFORE[k]) > 1e-9
    moved += ch
    P("  %-22s %10.3f %10.3f %s" % (k, BEFORE[k], OVER[k], "<-- CHANGED" if ch else ""))
    b.inputs[k].default_value = OVER[k]
# The Roughness socket may be DRIVEN by the WEATHER group, in which case the
# default_value above is inert.  Say so rather than letting a dead lever pass
# for a null result -- that is exactly how rev 57 lost item B.
drv = [k for k in OVER if b.inputs[k].is_linked]
if drv:
    P("")
    P("  !! LINKED, so setting default_value is INERT for: %s" % ", ".join(drv))
    P("     For those, the live value comes from the WEATHER group and this")
    P("     probe CANNOT move it.  Do not read a flat gate as 'no effect'.")
P("  %d of 4 inputs changed this run" % moved)
if not moved:
    P("  BASELINE RUN -- nothing overridden.")

# ------------------------------------------------------------- rev 58, F53
# THE ROUGHNESS ARM -- THE ONE MODEL-SIDE LEVER ITEM A HAS LEFT.
#
# `T1_GL_RGH` above sets the BSDF's Roughness socket, and F53 established that
# socket is LINKED: `apply_weather()` re-routes it through the WEATHER group,
# so writing default_value on it is INERT.  Setting it there and reading a flat
# gate is exactly how rev 57 lost item B -- a lever that was not connected to
# the thing it was being read against (rule 36).
#
# The live path, traced through t1_mats.py rather than assumed:
#   body_paint()    sets bsdf["Roughness"].default_value = 0.420 (unlinked yet)
#   apply_weather() finds it unlinked, so copies it into the GROUP's own
#                   Roughness input, then links group.outputs[1] -> bsdf
#   weather_group() rlo = rgh - W_ROUGH_SWING (0.09), rhi = rgh + 0.09, and the
#                   noise field is mapped between them; then peel, steel, dust,
#                   a 0.85 ceiling, a 0.030 floor and the FadeRough term
# So the GROUP's Roughness input is what shifts the whole band, and that is
# what T1_GL_WRGH writes.  It REFUSES rather than silently doing nothing if the
# node or the socket is not where the trace says.
_WRGH = os.environ.get("T1_GL_WRGH")
if _WRGH is not None:
    _grp = [n for n in m.node_tree.nodes
            if n.type == 'GROUP' and n.node_tree
            and "Roughness" in n.inputs and "FadeVert" in n.inputs]
    if len(_grp) != 1:
        raise SystemExit(
            "T1_GL_WRGH: expected exactly one WEATHER group in T1_paint, found "
            "%d -- REFUSING to set a lever I cannot locate" % len(_grp))
    _g = _grp[0]
    if _g.inputs["Roughness"].is_linked:
        raise SystemExit(
            "T1_GL_WRGH: the GROUP's own Roughness input is itself LINKED, so "
            "writing default_value here is inert too -- REFUSING (this is F53 "
            "one level up, and it must not pass for a null result)")
    _was = float(_g.inputs["Roughness"].default_value)
    _g.inputs["Roughness"].default_value = float(_WRGH)
    P("")
    P("  ROUGHNESS ARM: WEATHER group %r Roughness %.3f -> %.3f"
      % (_g.node_tree.name, _was, float(_WRGH)))
    P("    (the BSDF socket is LINKED and inert -- F53.  This is the live path.)")
    P("    band becomes %.3f .. %.3f before peel/dust/fade"
      % (float(_WRGH) - 0.09, float(_WRGH) + 0.09))

# ------------------------------------------------------------- rev 57b
# THE RIG-CEILING ARM.  OWNER-AUTHORISED MEASUREMENT, SHIPS NOTHING.
#
# F55: a smooth coat under a 13.0 x 8.5 m softbox reflects a nearly uniform
# field, so it gives a uniform LIFT and not a highlight -- which is why the
# clearcoat bought +0.5 % of spread (F54).  The open question is how much of
# `gloss_compare`'s 0.392 is therefore the RIG's rather than the model's, and
# the owner ruled "quantify it, ship nothing".
#
# T1_GL_SPOT=n adds n SMALL, BRIGHT area lights -- a market-hall-lamp
# analogue, which is what the reference photograph actually has -- to the
# EXISTING studio rig, changes nothing else, and reverts when the process
# exits.  Nothing here is written to the shipped rig, and studio.py is not
# touched: the lights are created with bpy directly so verify_clone's
# "the duplicated studio rig still matches build.py" row stays exact.
#
# READ THE RESULT AS A CEILING, NOT A PROPOSAL.  It says how much spread a
# structured surround would buy.  It does NOT say the rig should change --
# that is the owner's ruling and "keep studio, fix the model" stands.
_SPOT = int(os.environ.get("T1_GL_SPOT", "0"))
if _SPOT:
    import mathutils
    for _i in range(_SPOT):
        _d = bpy.data.lights.new("ceil_spot%d" % _i, type='AREA')
        _d.shape = 'SQUARE'
        _d.size = float(os.environ.get("T1_GL_SPOTSIZE", "0.35"))   # SMALL
        _d.energy = float(os.environ.get("T1_GL_SPOTPOW", "4000"))
        _o = bpy.data.objects.new("ceil_spot%d" % _i, _d)
        bpy.context.collection.objects.link(_o)
        _o.location = (2.0 + 2.2 * _i, 7.0 - 1.4 * _i, 5.2 + 0.6 * _i)
        _v = mathutils.Vector((0.0, 0.0, 1.2)) - mathutils.Vector(_o.location)
        _o.rotation_euler = _v.to_track_quat('-Z', 'Y').to_euler()
    P("RIG-CEILING ARM: %d small bright source(s) added, size %.2f m, %.0f W each"
      % (_SPOT, _d.size, _d.energy))
    P("  MEASUREMENT ONLY -- nothing here ships, and the studio ruling stands.")

# ------------------------------------------------------------- rev 58, F55
# THE DARK-CARD ARM -- and it exists because the SPOT arm answered the wrong
# question.  MEASUREMENT ONLY, ships nothing, same standing as the spot arm.
#
# T1_GL_SPOT adds small BRIGHT sources on the theory that the photograph's
# market-hall lamps are what the studio lacks.  Measured at rev 58, that theory
# is REFUTED: 3 x 250 W moved the gate BACKWARDS, spread ratio 0.4261 -> 0.3435,
# median L 104.7 -> 124.2, G/R 0.4364 -> 0.4860.  At the arm's own default
# 3 x 4000 W the panel washed out entirely and the gate REFUSED it (0 red px).
# Adding sources adds FILL: it lifts p5 and compresses the relative spread.
#
# Spread needs the reflected field to be NON-UNIFORM, and a featureless white
# cyclorama has no DARK in it at all.  So the thing the surround is missing is
# not brightness, it is DARKNESS -- and that is a testable claim rather than an
# argument.  T1_GL_DARK=1 puts one large low-albedo card in the flank's
# reflected field, low and outboard so it does NOT occlude the key strip at
# y 8.30 z 5.90 or strip_lo at y 7.40 z 1.95, and changes nothing else.
#
# READ IT AS A CEILING, NOT A PROPOSAL.  "Keep studio, fix the model" stands.
if os.environ.get("T1_GL_DARK"):
    _dm = bpy.data.materials.new("ceil_darkcard")
    _dm.use_nodes = True
    _db = next(n for n in _dm.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    _db.inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1.0)
    _db.inputs["Roughness"].default_value = 0.9
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0.0, 10.0, 1.25))
    _dc = bpy.context.active_object
    _dc.name = "ceil_darkcard"
    _dc.rotation_euler = (1.5707963, 0.0, 0.0)      # stand it up, facing -Y
    _dc.scale = (20.0, 4.5, 1.0)
    _dc.data.materials.append(_dm)
    P("")
    P("RIG-CEILING ARM (DARK): one 20.0 x 4.5 m card, albedo 0.02, at y +10.0,")
    P("  centred z 1.25 -- BELOW the key strip (z 5.90), so it adds dark to the")
    P("  reflected field without removing any light from the scene.")
    P("  MEASUREMENT ONLY -- nothing here ships, and the studio ruling stands.")

# ------------------------------------------------------------- rev 57b
# THE MIRROR ARM -- T1_GL_MIRROR=n.
#
# The first ceiling run (T1_GL_SPOT=3, above) put its sources on an arbitrary
# ring and measured spread 0.4437 against the baseline's 0.4675 -- a 5 % LOSS,
# not a gain.  Looking at the frame said why: there was no highlight on the
# show flank at all.  A specular highlight appears at exactly the points whose
# MIRROR DIRECTION from the camera reaches a source, so a source placed
# anywhere else is not a test of gloss -- it is just more ambient.
#
# This arm asks the GEOMETRY instead of guessing a pose (rule 7).  It fires n
# rays from the scene camera through n sample points inside gloss_compare's
# OWN window, takes the surface each one hits, reflects the view direction
# about that surface's normal, and puts one small source out along the
# reflected ray.  If the paint has any specular response at all, THOSE
# sources are the ones it can show.
#
# STILL A MEASUREMENT, STILL SHIPS NOTHING.  Same reversion, same ruling.
_MIRROR = int(os.environ.get("T1_GL_MIRROR", "0"))
if _MIRROR:
    import mathutils
    from mathutils import Vector
    _scn = bpy.context.scene
    _cam = _scn.camera
    if _cam is None:
        raise SystemExit("FATAL: no scene camera -- the mirror arm cannot aim")
    # `ST.camera()` only CREATES the camera; `ST.render_set` aims it per view,
    # which has not happened yet.  Reading matrix_world here without aiming
    # first gave three rays from the ORIGIN that all hit the cyclorama at
    # (0,0,0) -- a plausible-looking null result from a camera that was never
    # pointed at the bus.  Aim it exactly the way render_set will, then force
    # the depsgraph to evaluate the new matrix before any ray is cast.
    _V = ST.views()
    _vv = _V[os.environ.get("T1_GL_VIEW", "hero")]
    ST.aim(_cam, _vv["loc"], _vv["tgt"], _vv.get("lens"), _vv.get("ortho"),
           _vv.get("focus"), _vv.get("fstop"))
    bpy.context.view_layer.update()
    _dg = bpy.context.evaluated_depsgraph_get()
    # gloss_compare.py's WIN["render"] on a 1600x1100 hero, as fractions of
    # the frame, so the arm follows the gate's window rather than a literal.
    _WX0, _WY0, _WX1, _WY1 = 520 / 1600.0, 610 / 1100.0, 1060 / 1600.0, 790 / 1100.0
    _fr = [_cam.matrix_world @ v for v in _cam.data.view_frame(scene=_scn)]
    _tr, _br, _bl, _tl = _fr                     # Blender's order
    _org = _cam.matrix_world.translation
    _hit = 0
    _dist = float(os.environ.get("T1_GL_MIRRORD", "6.0"))
    for _i in range(_MIRROR):
        _u = _WX0 + (_WX1 - _WX0) * (_i + 0.5) / _MIRROR
        _v = _WY0 + (_WY1 - _WY0) * 0.5
        _top = _tl.lerp(_tr, _u)
        _bot = _bl.lerp(_br, _u)
        _pt = _top.lerp(_bot, _v)
        _dir = (_pt - _org).normalized()
        _ok, _loc, _nrm, _idx, _obj, _m = _scn.ray_cast(_dg, _org, _dir)
        P("            [ray] org (%.2f %.2f %.2f) dir (%.3f %.3f %.3f) ok=%s"
          % (_org.x, _org.y, _org.z, _dir.x, _dir.y, _dir.z, _ok))
        if not _ok:
            P("  mirror ray %d MISSED the model -- no source placed" % _i)
            continue
        if _obj is None or _obj.name in ("cyc", "floor") or "cyc" in _obj.name:
            P("  mirror ray %d hit the SURROUND (%s), not the vehicle -- skipped"
              % (_i, _obj.name if _obj else "?"))
            continue
        _refl = (_dir - 2.0 * _dir.dot(_nrm) * _nrm).normalized()
        _d = bpy.data.lights.new("mir_spot%d" % _i, type='AREA')
        _d.shape = 'SQUARE'
        _d.size = float(os.environ.get("T1_GL_SPOTSIZE", "0.35"))
        _d.energy = float(os.environ.get("T1_GL_SPOTPOW", "4000"))
        _o = bpy.data.objects.new("mir_spot%d" % _i, _d)
        bpy.context.collection.objects.link(_o)
        _o.location = _loc + _refl * _dist
        _o.rotation_euler = (_loc - _o.location).to_track_quat('-Z', 'Y').to_euler()
        _hit += 1
        P("  mirror %d: hits %-14s at (%.3f %.3f %.3f) n=(%.2f %.2f %.2f)"
          % (_i, _obj.name if _obj else "?", _loc.x, _loc.y, _loc.z,
             _nrm.x, _nrm.y, _nrm.z))
        P("            source at (%.2f %.2f %.2f), %.1f m out along the mirror"
          % (_o.location.x, _o.location.y, _o.location.z, _dist))
    P("MIRROR ARM: %d of %d source(s) placed ON THE MIRROR DIRECTION, size %.2f m,"
      % (_hit, _MIRROR, float(os.environ.get("T1_GL_SPOTSIZE", "0.35"))))
    P("  %.0f W each.  MEASUREMENT ONLY -- the studio ruling stands."
      % float(os.environ.get("T1_GL_SPOTPOW", "4000")))
    if not _hit:
        raise SystemExit("FATAL: every mirror ray missed -- refusing to render "
                         "a frame that would look like a null result")

if os.environ.get("T1_GL_NORENDER") == "1":
    P("T1_GL_NORENDER=1 -- stopping before the render (placement check only)")
    raise SystemExit(0)

PFX = os.environ.get("T1_GL_PFX", "gl")
ST.render_set([os.environ.get("T1_GL_VIEW", "hero")],
              os.path.join(ROOT, "out"), prefix=PFX,
              res=(int(_f(os.environ.get("T1_RX"), 1600)),
                   int(_f(os.environ.get("T1_RY"), 1100))),
              samples=int(_f(os.environ.get("T1_SAMP"), 96)), log=P)
P("")
P("  now:  python3 gloss_compare.py out/%s_hero.png" % PFX)
P("  and:  python3 flank_compare.py <a side render> /tmp/fc.png   # the CHROMA half")
