"""hq_render.py -- rev 57b.  The delivery frame, in ONE Blender session, with
OVERLAP MARGIN on every strip.

TWO DEFECTS IN THE OLD RECIPE, BOTH MEASURED ON THE FIRST DELIVERY RENDER:

1. SEAMS.  Blender's border rounds INWARD, so a strip declared 0.30..0.40 of
   the frame does not actually render every row the stitcher then reads from
   it.  Measured on hq2/hq3 at the 1847/1848 boundary: strip 3 carries real
   pixels through row 1848, strip 2's first real row is 1850, and row 1849 is
   rendered by NEITHER.  stitch.py took row 1848 from strip 2, where it is
   (255,255,255).  Result: a one-pixel WHITE LINE across the frame at 8 of 9
   seams, worst z = 89.26 on stitch.py's own detector.
   FIX: render each band with MARGIN and declare it without.  Every declared
   row is then genuinely rendered and the shipped stitcher needs no change.

2. TEN REBUILDS.  The old loop invoked Blender once per strip and paid the
   ~65 s scene build every time -- 10.8 min of a 116 min job spent rebuilding
   something that had not changed.  This builds once.

    T1_SUB=2 T1_HQ_RX=3840 T1_HQ_RY=2640 T1_HQ_SAMP=256 T1_HQ_N=10 \
      /tmp/blender/blender -b -P hq_render.py
    python3 stitch.py out/hq_hero_raw.png 0.0000,0.1000=out/hq0_hero.png ...
    python3 post.py out/hq_hero_raw.png out/hq_hero.png
"""
import os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.environ.setdefault("T1_SUB", "2")
_p = os.environ.pop("T1_PREVIEW", None)          # build only; we drive the renders
exec(compile(open(os.path.join(ROOT, "build.py")).read(), "build.py", "exec"))

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

RX = int(os.environ.get("T1_HQ_RX", 3840))
RY = int(os.environ.get("T1_HQ_RY", 2640))
SAMP = int(os.environ.get("T1_HQ_SAMP", 256))
N = int(os.environ.get("T1_HQ_N", 10))
VIEW = os.environ.get("T1_HQ_VIEW", "hero")
# MARGIN, in frame fractions.  Needs to beat Blender's inward rounding, which
# measured at ~2 rows; 0.005 of 2640 is 13 rows, so it is not a close call.
MARGIN = float(os.environ.get("T1_HQ_MARGIN", 0.005))

P("=" * 72)
P("  DELIVERY FRAME  %dx%d  %d spp  %d strips  margin %.4f (%.1f rows)"
  % (RX, RY, SAMP, N, MARGIN, MARGIN * RY))
P("  ONE session: the scene is built once, not %d times." % N)
P("=" * 72)
ONLY = os.environ.get("T1_HQ_ONLY")          # render ONE band, for timing controls
for i in range(N):
    if ONLY is not None and i != int(ONLY):
        continue
    lo, hi = i / N, (i + 1) / N
    mlo, mhi = max(0.0, lo - MARGIN), min(1.0, hi + MARGIN)
    os.environ["T1_BORDER"] = "%.6f,%.6f" % (mlo, mhi)
    P("\n--- strip %d   declare %.4f,%.4f   RENDER %.6f,%.6f" % (i, lo, hi, mlo, mhi))
    ST.render_set([VIEW], os.path.join(ROOT, "out"), prefix="hq%d" % i,
                  res=(RX, RY), samples=SAMP, log=P)
P("\nSTRIPS DONE.  Stitch with the DECLARED spans, not the rendered ones:")
P("  python3 stitch.py out/hq_hero_raw.png " +
  " ".join("%.4f,%.4f=out/hq%d_%s.png" % (i / N, (i + 1) / N, i, VIEW)
           for i in range(N)))
