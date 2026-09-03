"""gloss_compare.py -- rev 57b.  THE THIRD FIDELITY GATE, and the first one
that measures the surface the eye actually lands on.

WHAT IT MEASURES.  Not colour -- W6 settles colour and a G/R shortfall is the
owner's call, not a paint error.  This measures GLOSS: how widely the luminance
of ONE paint region spreads about ITS OWN median.  A glossy panel carries a
specular highlight and a dark reflected horizon, so its own spread is wide; a
matte one is narrow.  Every number is divided by the region's own median, so
the statistic is free of exposure, of white balance, and of any px/m bracket --
none of the three open scale unknowns can reach it.

WHY IT IS NEEDED.  `flank_compare` measures a decal's outline.  `mottle_measure`
measures a cream patch's band-passed rms -- and rev 57 showed it is not even
measuring the mottle.  Between them they cover a few per cent of the frame.
The paint's gloss covers roughly 3.4 m^2 of it, which `visibility_budget.py`
puts at ~3.4e6 px^2 of a 3840 px hero -- the largest single thing in the image,
and nothing in this repository has ever measured it.

CEILING, STATED UP FRONT.  (1) The reference is a JPEG of a bus in a market
hall with its own reflections; the render is a bus in a white cyclorama.  The
owner has RULED that the rig stays ("keep studio, fix the model"), so a gap
here is NOT automatically a shader defect -- part of it is the surround having
nothing to reflect, which is his call and not this gate's business.  What the
gate can say is HOW BIG the gap is and whether a change moved it.  (2) Compare
a POSTED frame when you have one: post.py's bloom widens the spread, and an
un-posted render is therefore measured at a disadvantage.

    python3 gloss_compare.py [render.png]
"""
import os, sys
import numpy as np
from PIL import Image
import scipy.ndimage as ndi

ROOT = os.path.dirname(os.path.abspath(__file__))
PHOT = os.path.join(ROOT, "ref_nolita_front34.jpg")
# rev 60, F85.  THIS USED TO WRITE INTO probe_scratch/, WHICH IS TRACKED, so
# merely RUNNING the gate dirtied the working tree and verify_clone.sh's
# "modified tracked files" row then fired.  It cost rev 59 a wasted hunt.
# The painted tiles are a LOOK-AT-IT aid, not a record (the numbers live in the
# ledger), so they belong in out/, which is untracked.  T1_GL_TILES=track
# restores the old destination for the one case that wants it: deliberately
# refreshing the committed reference tiles.
OUTD = os.path.join(ROOT, "probe_scratch"
                    if os.environ.get("T1_GL_TILES") == "track" else "out")
os.makedirs(OUTD, exist_ok=True)
BAR = 0.60          # the render must reach 60 % of the photograph's spread
P = print
# rev 58, F58: THE DEFAULT USED TO BE A HARD-CODED `out/r57_hero.png`.
# `out/` is untracked and starts EMPTY on every clone, so that default resolved
# only in the working tree of the revision that wrote it -- the one place it is
# guaranteed to work and the one place nobody re-runs it from cold.  A
# verify_clone row called this script with no argument and reported the missing
# file as `MOVED: []`, i.e. as "the gate is no longer exposure-free": an ABSENT
# INPUT reading as a MEASUREMENT RESULT, pointing the reader at the statistic
# instead of at the path.  Take the newest hero actually present, and if there
# is none say so in those words rather than raising a stack trace.
def _newest_hero():
    import glob
    c = sorted(glob.glob(os.path.join(ROOT, "out", "*_hero.png")),
               key=os.path.getmtime, reverse=True)
    return c[0] if c else None


_ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
if _ARGS:
    REND = _ARGS[0]
    # *** rev 72, rule 37 -- A NAMED FRAME THAT IS NOT THERE MUST REFUSE. ***
    # The no-argument branch below has refused since rev 58, but a frame named
    # on the command line went straight into spread() and died with a raw
    # FileNotFoundError out of Image.open -- no "NO RENDER" line, no summary
    # line, so a reader obeying rule 9 (read the summary, never the exit code)
    # had NOTHING to read.  `out/` is untracked and starts EMPTY on a clone, and
    # every brief prints this gate with an explicit `out/rNN_hero34f.png`, so
    # this is the branch that actually gets typed.  Found by an adversary
    # dispatched at the rev-72 brief, which ranks this gate #2 while flagging
    # the same defect only in probe_rev67_nose.py.
    if not os.path.exists(REND):
        P("NO RENDER -- %s does not exist.  out/ is untracked and starts EMPTY "
          "on a clone." % REND)
        P("  Nothing was measured.  Render it first:")
        # rev 75, F327: this named T1_PFX=r72, which went stale the revision
        # after it was written -- F321's defect in a second file.  Name the
        # SOURCE of the prefix, never a value.
        P("  T1_SUB=1 T1_PREVIEW=hero34f T1_PFX=<the prefix the brief's sec.0 "
          "renders> ... build.py")
        sys.exit(3)
elif "--selftest" not in sys.argv:
    REND = _newest_hero()
    if REND is None:
        P("NO RENDER: out/ holds no *_hero.png.  This is not a measurement --")
        # rev 75, F327: this named T1_PFX=r58 AND T1_PREVIEW=hero -- and there
        # is no plain `hero` view in the brief's preview list, so the command
        # as written produced nothing.  The views are front,side,hero34f,hero34r.
        P("  render one first: T1_PREVIEW=hero34f T1_PFX=<the prefix the "
          "brief's sec.0 renders> ... build.py")
        sys.exit(3)
    P("no frame named; taking the newest hero in out/: %s" % os.path.basename(REND))
else:
    REND = None

# Windows are FIXED and PAINTED.  Both sit on flat red bodywork with no lamp,
# no badge and no chrome in them; rev 57's first attempt included the lit
# headlamp and inflated the photograph's p99 -- caught by painting it.
WIN = {"render": (520, 610, 1060, 790), "photo": (300, 175, 520, 300)}


def spread(path, box, tag):
    a = np.asarray(Image.open(path).convert("RGB")).astype(float)
    sub = a[box[1]:box[3], box[0]:box[2]]
    R, G, B = sub[..., 0], sub[..., 1], sub[..., 2]
    L = 0.2126 * R + 0.7152 * G + 0.0722 * B
    m = (R > G * 1.35) & (R > B * 1.35) & (L > 25)
    # rev 58, F59: THE SHIPPED MASK LET THE GOLD FLANK INK THROUGH, AND THE
    # HEADROOM STATISTIC IS DEFINED ON EXACTLY THE PIXELS IT CONTAMINATED.
    #
    # `R > G*1.35` excludes cream, chrome, the silver script and the teal, so
    # the kept set is 95.0 % body red -- the mask does most of its job and the
    # rectangle's raw 42.9 % red fraction OVERSTATES the problem.  But 3.4 %
    # of the kept pixels are the gold artwork, and they are the BRIGHT ones:
    # measured on out/r58_hero.png the p99 pixels average RGB (194.8, 119.0,
    # 78.7), G/R 0.61 -- gold ink, not paint.  Excluding it moves
    #     SPREAD   render +0.6 %, photo +0.8 %   (the headline is ROBUST)
    #     HEADROOM render -31.6 %, photo +0.1 %  (the headline is NOT)
    # RECOMPUTED THROUGH THIS SHIPPED PATH, and it CORRECTED two figures I had
    # published from an exploratory script that applied the tighter test in a
    # different order relative to the erosion: I had -0.2 % and -29.4 %.  The
    # conclusion is unchanged and the direction of the important one is not:
    # the spread ratio reads 0.3918 loose against 0.3911 tight, so the headline
    # really is robust, and the headroom really does fall by about a third.
    # so the render's headroom was inflated by a third by ink.  A paint
    # measurement may not include the signwriting.  T1_GC_LOOSEMASK=1 restores
    # the old mask so the change is testable in both directions.
    if not os.environ.get("T1_GC_LOOSEMASK"):
        m = m & (G < 0.55 * R) & (B < 0.50 * R)
    m = ndi.binary_erosion(ndi.binary_opening(m, np.ones((5, 5))), np.ones((5, 5)))
    if m.sum() < 2000:
        raise SystemExit("gloss_compare: %s window holds only %d red px -- REFUSING"
                         % (tag, m.sum()))
    v = L[m]
    p5, p50, p95, p99 = np.percentile(v, [5, 50, 95, 99])
    ov = np.asarray(Image.open(path).convert("RGB")).copy()
    o = ov[box[1]:box[3], box[0]:box[2]]
    o[m] = (o[m] * 0.5 + np.array([0, 255, 255]) * 0.5).astype(np.uint8)
    ov[box[1]:box[3], box[0]:box[2]] = o
    Image.fromarray(ov).save(os.path.join(OUTD, "rev57_gloss_%s.png" % tag))
    return dict(n=int(m.sum()), p5=p5, med=p50, p95=p95, p99=p99,
                spread=(p95 - p5) / p50, head=p99 / p50 - 1.0, L=L, m=m)


# ------------------------------------------------------------- rev 58, F58
# --selftest: EXPOSURE INVARIANCE WITHOUT A FRAME.
#
# Exposure invariance is a property of the ESTIMATOR, not of any particular
# render, so the row that checks it must not need `out/` to be populated.  It
# used to: verify_clone called this script with no argument, the hard-coded
# `out/r57_hero.png` was absent on every clone, and the missing file was
# reported as `MOVED: []` -- an absent input dressed up as a moved statistic.
#
# This runs the REAL `spread()` on a synthetic red patch, so it exercises the
# shipped mask, the shipped erosion and the shipped percentiles, and prints the
# same three lines the live control prints.
if "--selftest" in sys.argv:
    rng = np.random.default_rng(58)
    n = 220
    base = np.zeros((n, n, 3), float)
    # a red panel with a gradient and a bright streak, so the spread is nonzero
    base[..., 0] = 150 + 60 * np.linspace(0, 1, n)[None, :]
    base[..., 1] = 55 + 10 * np.linspace(0, 1, n)[:, None]
    base[..., 2] = 48 + 8 * rng.random((n, n))
    base[90:110, :, :] += 45.0                     # a highlight band
    img = np.clip(base + rng.normal(0, 1.5, base.shape), 0, 255).astype(np.uint8)
    Image.fromarray(img).save("/tmp/_gloss_selftest.png")
    d = spread("/tmp/_gloss_selftest.png", (0, 0, n, n), "selftest")
    P("SELFTEST -- exposure invariance of the shipped estimator, no frame needed")
    P("  synthetic red patch %dx%d, %d px pass the shipped red mask" % (n, n, d["n"]))
    got = []
    for k in (0.70, 1.00, 1.40):
        v = d["L"][d["m"]] * k
        p5, p50, p95 = np.percentile(v, [5, 50, 95])
        # T1_GC_ABSSPREAD=1 drops the /p50 that MAKES the statistic scale-free.
        # That is the ABLATION: it turns the estimator into an exposure-
        # dependent one, and the selftest must then FAIL.  WATCHED FAILING at
        # rev 58 -- x0.70 35.8691, x1.00 51.2416, x1.40 71.7382, SELFTEST FAIL,
        # rc=1.  (These three were TYPED AS A PREDICTION first and were wrong by
        # two orders of magnitude; they are the numbers that printed.  Rule 5.)
        # A control that has only ever passed has not been tested (rule 3).
        _s = (p95 - p5) if os.environ.get("T1_GC_ABSSPREAD") else (p95 - p5) / p50
        got.append("%.4f" % _s)
        P("      x%.2f  spread %s" % (k, got[-1]))
    ok = len(set(got)) == 1
    P("  SELFTEST %s -- exposure-free" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)

P("=" * 78)
P("  GLOSS -- one red panel, render against photograph.  Not colour.")
P("=" * 78)
r = spread(REND, WIN["render"], "render")
q = spread(PHOT, WIN["photo"], "photo")
P("%-8s %8s %9s %9s %9s   %10s %10s"
  % ("", "n", "p5/med", "median", "p95/med", "SPREAD", "HEADROOM"))
for tag, d in (("render", r), ("photo", q)):
    P("%-8s %8d %9.3f %9.1f %9.3f   %10.3f %10.3f"
      % (tag, d["n"], d["p5"] / d["med"], d["med"], d["p95"] / d["med"],
         d["spread"], d["head"]))
P("  painted -> %s/rev57_gloss_render.png / _photo.png"
  % os.path.relpath(OUTD, ROOT))
P("  (those two tiles are OVERWRITTEN by whichever render you last measured --")
P("   this run: %s.  They illustrate the WINDOW, which is fixed; they are not"
  % os.path.basename(REND))
P("   a record of one frame's numbers.  Those live in the ledger.)")
P("  LOOK AT THEM.  A window that catches a lamp or a chrome ring is not a")
P("  paint measurement, and that is how rev 57's first attempt went wrong.")

# ---------------------------------------------------------------- controls
P("")
P("  CONTROL 1 -- is the statistic really exposure-free?  Re-measure the")
P("  render's own window at 0.70x and 1.40x brightness; a scale-free")
P("  statistic must not move.")
base = r["L"][r["m"]]
for k in (0.70, 1.00, 1.40):
    v = base * k
    p5, p50, p95 = np.percentile(v, [5, 50, 95])
    P("      x%.2f  spread %.4f" % (k, (p95 - p5) / p50))
P("  CONTROL 2 -- is it resolution-free?  Halve the photograph and re-measure.")
h = Image.open(PHOT).convert("RGB")
h = h.resize((h.width // 2, h.height // 2), Image.LANCZOS)
h.save("/tmp/_gloss_half.png")
q2 = spread("/tmp/_gloss_half.png", tuple(v // 2 for v in WIN["photo"]), "photohalf")
P("      full %.4f   half %.4f   (%.1f %% apart)"
  % (q["spread"], q2["spread"], 100 * abs(q2["spread"] / q["spread"] - 1)))

# ----------------------------------------------------------------- verdict
ratio = r["spread"] / q["spread"]
hratio = r["head"] / q["head"]
P("")
P("=" * 78)
P("  the render's paint spreads %.3f of the photograph's  (bar %.2f)"
  % (ratio, BAR))
P("  its brightest 1 %% sits %.3f as far above its own median" % hratio)
P("  %s  gloss vs %s" % ("PASS" if ratio >= BAR else "FAIL",
                         os.path.basename(PHOT)))
P("  READ IT THIS WAY: this gate does NOT say the shader is wrong.  Part of")
P("  the gap is the white cyclorama having nothing to reflect, which the owner")
P("  has ruled stays.  What it says is how far apart they are and whether")
P("  anything you change moves it.  It is a RULER, not a verdict on cause.")
P("=" * 78)
