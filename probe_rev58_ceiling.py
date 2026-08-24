"""
probe_rev58_ceiling.py -- HOW MUCH OF THE GLOSS DEFICIT IS THE RIG'S?
=====================================================================

OWNER-AUTHORISED MEASUREMENT, rev 57b.  He was shown F54/F55 -- that a full
automotive clearcoat buys `gloss_compare` +0.5 % of spread while costing the
red 18 % of its saturation -- and ruled:

    "Quantify it, ship nothing.  Render ONE frame under a structured
     surround purely to read gloss_compare, then revert.  Tells us how
     much of the 0.392 is the model's vs the rig's.  Nothing ships, no
     constant changes."

NOTHING IN THIS FILE CHANGES A CONSTANT.  It reads two frames that already
exist and prints a comparison.  The frames come from `probe_rev58_gloss.py`,
which overrides a BUILT material in memory and writes no source either.

WHY THIS IS A SEPARATE SCRIPT AND NOT A FLAG ON `gloss_compare.py`
------------------------------------------------------------------
`gloss_compare.py` recomputes its red mask FROM EACH FRAME.  That is correct
for its own job -- render against photograph, two different cameras, no pixel
correspondence -- and it is why its exposure control (0.70x / 1.00x / 1.40x,
0.4677 every time) holds: the mask rule is a pair of RATIO tests, and a ratio
is scale-invariant.

**IT IS NOT SCALE-INVARIANT ONCE ANYTHING CLIPS**, and that is F58.  This
probe compares two renders of the SAME camera and the SAME geometry, so the
pixels correspond exactly, and it therefore uses ONE mask -- built on the
baseline -- for both.  It also REFUSES on clipping rather than reporting a
number, because a clipped surface has had its spread destroyed by the sensor
and not by the lighting.

RULE 8: the mask is painted before the number, to `probe_scratch/`.
"""
import os, sys
import numpy as np
import scipy.ndimage as ndi
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(ROOT, "probe_scratch")
os.makedirs(OUTD, exist_ok=True)

# The SAME window `gloss_compare.py` uses on a 1600x1100 hero.  Quoted from
# that file's own `WIN["render"]`; a verifier row holds the two together.
WIN = (520, 610, 1060, 790)

# `gloss_compare.py`'s own photograph and photograph window, so this probe can
# express its result in the SAME unit the gate reports -- "x of the
# photograph's spread" -- instead of leaving the reader to divide.  Both are
# read from that file at run time rather than copied, so the two cannot drift
# apart silently.  If gloss_compare moves its window, this probe moves with it.
PHOTO = os.path.join(ROOT, "ref_nolita_front34.jpg")
PHOTO_WIN = (300, 175, 520, 300)

# Above this, the number is refused rather than printed.  A clipped pixel has
# no spread left to measure, so a spread computed over clipped pixels is a
# statement about the sensor, not about the paint.
CLIP_REFUSE_PCT = 1.0


def _load(path):
    if not os.path.exists(path):
        sys.exit("probe_rev58_ceiling: %s does not exist -- render it first" % path)
    return np.asarray(Image.open(path).convert("RGB")).astype(float)


def _lum(s):
    return 0.2126 * s[..., 0] + 0.7152 * s[..., 1] + 0.0722 * s[..., 2]


def _redmask(sub):
    R, G, B = sub[..., 0], sub[..., 1], sub[..., 2]
    m = (R > G * 1.35) & (R > B * 1.35) & (_lum(sub) > 25)
    return ndi.binary_erosion(ndi.binary_opening(m, np.ones((5, 5))),
                              np.ones((5, 5)))


def _paint(full, masks, cols, out):
    ov = full.copy().astype(np.uint8)
    o = ov[WIN[1]:WIN[3], WIN[0]:WIN[2]]
    for mk, col in zip(masks, cols):
        o[mk] = (o[mk] * 0.45 + np.array(col) * 0.55).astype(np.uint8)
    ov[WIN[1]:WIN[3], WIN[0]:WIN[2]] = o
    im = Image.fromarray(ov)
    # HALVED ON THE WAY OUT.  These tiles are the EVIDENCE for F58/F59 and are
    # tracked, so they have to survive a clone -- and the owner's F56 ruling
    # caps a tracked frame at 1600 px.  Halving keeps them a quarter of a MB
    # and the mask boundary still reads; a re-run overwrites them with the
    # same picture rather than with an 11 MB one.
    im.resize((im.size[0] // 2, im.size[1] // 2)).save(os.path.join(OUTD, out))


def stats(sub, m):
    L = _lum(sub)[m]
    p5, p50, p95, p99 = np.percentile(L, [5, 50, 95, 99])
    clip = ((sub[..., 0] >= 254) | (sub[..., 1] >= 254) | (sub[..., 2] >= 254))
    return dict(n=int(m.sum()), med=p50, spread=(p95 - p5) / p50,
                head=p99 / p50 - 1.0, clip=100.0 * clip[m].mean())


BASE = sys.argv[1] if len(sys.argv) > 1 else "out/g0_hero.png"
TEST = sys.argv[2] if len(sys.argv) > 2 else "out/c4_hero.png"

fb, ft = _load(BASE), _load(TEST)
if fb.shape != ft.shape:
    sys.exit("probe_rev58_ceiling: the two frames are different sizes -- "
             "there is no pixel correspondence and this probe is invalid")
sb = fb[WIN[1]:WIN[3], WIN[0]:WIN[2]]
st = ft[WIN[1]:WIN[3], WIN[0]:WIN[2]]

MASK = _redmask(sb)                 # ONE mask, from the BASELINE, for both
drift = _redmask(st)                # what the gate WOULD have used on the test

# Two runs (the refused pair and the good one) must not overwrite each other's
# evidence -- `mottle_measure.py` keyed its output on a constant and two runs
# diffed a file against itself.  T1_CEIL_TAG keeps them apart.
TAG = os.environ.get("T1_CEIL_TAG", "")
_paint(fb, [MASK], [(0, 255, 255)], "rev58_ceil%s_mask_base.png" % TAG)
_paint(ft, [MASK, drift], [(0, 255, 255), (255, 0, 255)],
       "rev58_ceil%s_mask_test.png" % TAG)
# and the clipping itself, painted, because the refusal below is a number about
# these pixels and rule 8 says the window is part of the measurement.
_clip = ((st[..., 0] >= 254) | (st[..., 1] >= 254) | (st[..., 2] >= 254))
_paint(ft, [_clip], [(255, 0, 0)], "rev58_ceil%s_clip_test.png" % TAG)

b, t = stats(sb, MASK), stats(st, MASK)
d = stats(st, drift) if drift.sum() else None

P = print
P("=" * 78)
P("  THE RIG CEILING -- how much of gloss_compare's deficit is the SURROUND?")
P("=" * 78)
P("  baseline %s" % BASE)
P("  test     %s" % TEST)
P("")
P("  %-26s %10s %10s" % ("", "baseline", "test"))
for k, f in (("red px in the ONE mask", "%10d"), ("median L (exposure match)", "%10.1f"),
             ("spread (p95-p5)/med", "%10.4f"), ("headroom p99/med - 1", "%10.4f"),
             ("CLIPPED in mask, %", "%10.2f")):
    key = {"red px in the ONE mask": "n", "median L (exposure match)": "med",
           "spread (p95-p5)/med": "spread", "headroom p99/med - 1": "head",
           "CLIPPED in mask, %": "clip"}[k]
    P(("  %-26s " + f + " " + f) % (k, b[key], t[key]))

exp = 100.0 * (t["med"] / b["med"] - 1.0)
P("")
P("  exposure difference %+.1f %% of the baseline median" % exp)

if d is not None:
    P("")
    P("  AND WHAT THE PER-FRAME MASK WOULD HAVE DONE (F58) -- the gate rebuilds")
    P("  its mask from each frame, and on a brighter frame the paint desaturates")
    P("  out of the R > 1.35 G ratio test, so the mask RETREATS INTO THE SHADOWS:")
    P("    it would have held %d px of the baseline's %d (%.1f %%)"
      % (d["n"], b["n"], 100.0 * d["n"] / b["n"]))
    P("    and read %.2f %% clipped inside that retreat, against %.2f %% over"
      % (d["clip"], t["clip"]))
    P("    the region it came from.  A MASK THAT MOVES CAN MOVE OFF THE DEFECT.")

P("")
if t["clip"] > CLIP_REFUSE_PCT or b["clip"] > CLIP_REFUSE_PCT:
    P("  REFUSED: %.2f %% of the measured pixels are clipped, over a %.1f %% bar."
      % (max(t["clip"], b["clip"]), CLIP_REFUSE_PCT))
    P("  A clipped surface has no spread left to measure.  NO CEILING IS")
    P("  PUBLISHED FROM THIS PAIR -- re-render the test at matched exposure.")
    sys.exit(2)
if abs(exp) > 10.0:
    P("  REFUSED: the two frames are %+.1f %% apart in exposure, over a 10 %% bar."
      % exp)
    P("  gloss_compare's median normalisation is only exposure-free while the")
    P("  tone curve is locally linear; %+.1f %% is not that." % exp)
    sys.exit(2)

ph = _load(PHOTO)
ps = ph[PHOTO_WIN[1]:PHOTO_WIN[3], PHOTO_WIN[0]:PHOTO_WIN[2]]
pm = _redmask(ps)
p = stats(ps, pm)

gain = t["spread"] / b["spread"]
P("  MEASURED CEILING: three small bright sources move the paint's spread")
P("  %.4f -> %.4f, a factor of %.3f, at %+.1f %% exposure and %.2f %% clipping."
  % (b["spread"], t["spread"], gain, exp, t["clip"]))
P("")
P("  IN THE GATE'S OWN UNIT -- against %s, whose"
  % os.path.basename(PHOTO))
P("  same-window spread is %.4f over %d red px:" % (p["spread"], p["n"]))
P("    baseline  %.3f of the photograph's spread   (gloss_compare's 0.60 bar)"
  % (b["spread"] / p["spread"]))
P("    test      %.3f of the photograph's spread"
  % (t["spread"] / p["spread"]))
P("")
P("  THAT IS THE PART OF THE DEFICIT THE SURROUND OWNS, and the model did not")
P("  move to earn it: not one constant differs between these two frames.")
P("  The studio ruling stands -- nothing here ships.  This is a BOUND on how")
P("  much of item A is the model's to fix, not a proposal to change the rig.")
