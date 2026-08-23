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
REND = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "out", "r57_hero.png")
PHOT = os.path.join(ROOT, "ref_nolita_front34.jpg")
OUTD = os.path.join(ROOT, "probe_scratch")
BAR = 0.60          # the render must reach 60 % of the photograph's spread
P = print

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
P("  painted -> probe_scratch/rev57_gloss_render.png / _photo.png")
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
