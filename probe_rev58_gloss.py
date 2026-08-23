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

PFX = os.environ.get("T1_GL_PFX", "gl")
ST.render_set([os.environ.get("T1_GL_VIEW", "hero")],
              os.path.join(ROOT, "out"), prefix=PFX,
              res=(int(_f(os.environ.get("T1_RX"), 1600)),
                   int(_f(os.environ.get("T1_RY"), 1100))),
              samples=int(_f(os.environ.get("T1_SAMP"), 96)), log=P)
P("")
P("  now:  python3 gloss_compare.py out/%s_hero.png" % PFX)
P("  and:  python3 flank_compare.py <a side render> /tmp/fc.png   # the CHROMA half")
