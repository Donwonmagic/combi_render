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

PFX = os.environ.get("T1_GL_PFX", "gl")
ST.render_set([os.environ.get("T1_GL_VIEW", "hero")],
              os.path.join(ROOT, "out"), prefix=PFX,
              res=(int(_f(os.environ.get("T1_RX"), 1600)),
                   int(_f(os.environ.get("T1_RY"), 1100))),
              samples=int(_f(os.environ.get("T1_SAMP"), 96)), log=P)
P("")
P("  now:  python3 gloss_compare.py out/%s_hero.png" % PFX)
P("  and:  python3 flank_compare.py <a side render> /tmp/fc.png   # the CHROMA half")
