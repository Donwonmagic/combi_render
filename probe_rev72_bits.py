#!/usr/bin/env python3
# probe_rev72_bits.py -- rev 72.  DOES THE 16-BIT RE-READ MOVE THE GATES?
#
# WHY.  F263 (rev 71) found that every frame this project renders is 16-bit on
# disk and every measurement ever taken off one was read at 8, because PIL has
# no 16-bit RGB path and truncates silently.  `photometry.read_png` is a real
# decoder.  The rev-72 brief calls re-reading the gates through it "the cheapest
# re-measurement available" and warns it "may move the numbers before you tune
# anything".  THIS PROBE ASKS THAT QUESTION AND ANSWERS IT WITH A NUMBER.
#
# WHAT IT DOES NOT DO.  It does not re-tune anything and it does not touch the
# gates' shipped code.  It re-computes each gate's OWN statistic, by its OWN
# rule, off the SAME window, changing exactly one thing: the reader.
#
# ⚠ THE CEILING, AND IT IS STRUCTURAL (rule 38).  `gloss_compare`'s verdict is a
# RATIO of the render's spread to the PHOTOGRAPH's.  The photographs are JPEG
# and are 8-bit; there is no 16-bit version of them and there never will be.  So
# the re-read can only ever move the NUMERATOR.  A gate whose two sides are read
# at different depths is not thereby wrong, but the ratio's precision is floored
# by the 8-bit side, and no re-read can lift that.  Stated, not hidden.
import os
import sys

import numpy as np
import scipy.ndimage as ndi
from PIL import Image

import photometry

ROOT = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(ROOT, "probe_scratch")
checks, fails = [], []


def ck(name, ok, detail=""):
    checks.append(name)
    if not ok:
        fails.append(name)
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name,
                           ("  --  " + detail) if detail else ""))
    return ok


# --------------------------------------------------------------- the readers
def read8(path):
    """EXACTLY what every gate in this tree does today."""
    return np.asarray(Image.open(path).convert("RGB")).astype(float)


def read16(path):
    """The same frame, all of it, rescaled to the SAME 0..255 footing.

    Rescaled rather than left at 0..65535 so every threshold in the gates'
    own masks (`L > 25`, and the ratio tests) keeps its meaning.  The ONLY
    difference from read8() is that the low byte survives.
    """
    a, mx = photometry.read_png(path)
    return a[..., :3].astype(float) * (255.0 / mx)


# ------------------------------------------------- gloss_compare's OWN statistic
def gloss_spread(a, box, loose=False):
    """`gloss_compare.spread()`, byte-for-byte in its arithmetic, on an ARRAY.

    Copied rather than imported because the shipped function takes a PATH and
    opens it with PIL -- the very thing under test.  Every constant below is
    read off gloss_compare.py at this commit; if that file moves, this
    stops being a comparison and B0 is what says so.
    """
    sub = a[box[1]:box[3], box[0]:box[2]]
    R, G, B = sub[..., 0], sub[..., 1], sub[..., 2]
    L = 0.2126 * R + 0.7152 * G + 0.0722 * B
    m = (R > G * 1.35) & (R > B * 1.35) & (L > 25)
    if not loose:
        m = m & (G < 0.55 * R) & (B < 0.50 * R)
    m = ndi.binary_erosion(ndi.binary_opening(m, np.ones((5, 5))), np.ones((5, 5)))
    if m.sum() < 2000:
        return None
    p5, p50, p95, p99 = np.percentile(L[m], [5, 50, 95, 99])
    return dict(n=int(m.sum()), spread=(p95 - p5) / p50, head=p99 / p50 - 1.0,
                p5=p5, med=p50, p95=p95, p99=p99)


def paint_mask(a, box, path, loose=False):
    """Rule 8: PAINT the selection this probe reports from, and LOOK at it."""
    sub = a[box[1]:box[3], box[0]:box[2]]
    R, G, B = sub[..., 0], sub[..., 1], sub[..., 2]
    L = 0.2126 * R + 0.7152 * G + 0.0722 * B
    m = (R > G * 1.35) & (R > B * 1.35) & (L > 25)
    if not loose:
        m = m & (G < 0.55 * R) & (B < 0.50 * R)
    m = ndi.binary_erosion(ndi.binary_opening(m, np.ones((5, 5))), np.ones((5, 5)))
    ov = np.clip(a, 0, 255).astype(np.uint8).copy()
    o = ov[box[1]:box[3], box[0]:box[2]]
    o[m] = (o[m] * 0.5 + np.array([0, 255, 255]) * 0.5).astype(np.uint8)
    ov[box[1]:box[3], box[0]:box[2]] = o
    Image.fromarray(ov).save(path)
    return int(m.sum())


def main():
    print("=" * 78)
    print("  probe_rev72_bits -- DOES READING ALL 16 BITS MOVE THE GATES?  (F263)")
    print("=" * 78)

    # ---------------------------------------------------------------- B0
    # THE STATISTIC I AM COMPARING MUST BE THE GATE'S OWN.  If gloss_compare's
    # mask or percentiles are edited, this probe silently stops comparing what
    # it says it compares.  Anchor on the ARITHMETIC, not on a grep (rule 50):
    # run the shipped file's own selftest path and require the numbers this
    # probe's copy produces on the SAME synthetic patch to agree exactly.
    # ANCHOR ON BEHAVIOUR, NOT A GREP (rule 50): write the shipped selftest's
    # own synthetic patch to an 8-bit PNG, run the SHIPPED gloss_compare.spread()
    # on it, and require this probe's copy to return the IDENTICAL spread.  If
    # gloss_compare's mask or percentiles are ever edited, this row goes red and
    # says so, instead of the probe quietly comparing the wrong statistic.
    rng = np.random.default_rng(58)
    n = 220
    base = np.zeros((n, n, 3), float)
    base[..., 0] = 150 + 60 * np.linspace(0, 1, n)[None, :]
    base[..., 1] = 55 + 10 * np.linspace(0, 1, n)[:, None]
    base[..., 2] = 40 + 8 * np.linspace(0, 1, n)[:, None]
    img = np.clip(base + rng.normal(0, 1.5, base.shape), 0, 255)
    tmp = os.path.join(SCRATCH, "_r72_b0.png")
    Image.fromarray(img.astype(np.uint8)).save(tmp)
    # RULE 42: the control must be framed the way the measurement is.  The first
    # cut fed my copy the un-quantised float patch while the shipped function
    # re-read the uint8 PNG, and the row went red at 0.170992 vs 0.172118 -- a
    # 0.7 % disagreement that was entirely MY input, not its arithmetic.  Feed
    # both the same bytes off the same file.
    mine = gloss_spread(read8(tmp), (0, 0, n, n))
    theirs, why0 = None, ""
    try:
        # gloss_compare.py is a SCRIPT: importing it runs the whole gate and it
        # SystemExits when out/ has no hero frame.  So take the shipped SOURCE
        # TEXT of `spread` itself, exec it, and call that.  This anchors on the
        # arithmetic actually in the file (rule 50) and goes red if it changes,
        # without depending on the module being importable -- which it is not.
        import ast
        gsrc = open(os.path.join(ROOT, "gloss_compare.py")).read()
        fn = next(nd for nd in ast.parse(gsrc).body
                  if isinstance(nd, ast.FunctionDef) and nd.name == "spread")
        ns = {"np": np, "ndi": ndi, "Image": Image, "os": os,
              "OUTD": SCRATCH, "SystemExit": SystemExit}
        exec(compile(ast.Module([fn], []), "<gloss_compare.spread>", "exec"), ns)
        theirs = ns["spread"](tmp, (0, 0, n, n), "r72b0")
    except SystemExit as e:                 # its own REFUSING path
        why0 = "gloss_compare.spread refused: %s" % str(e)[:60]
    except Exception as e:
        why0 = "%s: %s" % (type(e).__name__, str(e)[:60])
    agree = (theirs is not None and mine is not None
             and abs(theirs["spread"] - mine["spread"]) < 1e-12)
    ck("B0 this probe's copy IS gloss_compare.spread()'s arithmetic -- the "
       "shipped function's own source, exec'd, agrees to 1e-12",
       agree,
       ("mine %.9f  shipped %.9f" % (mine["spread"], theirs["spread"]))
       if theirs is not None else ("could not run the shipped function -- %s" % why0))

    # ---------------------------------------------------------------- B1
    # THE WATCHED KILL (rule 3).  A frame whose signal lives ENTIRELY in the low
    # byte: every pixel's TOP byte is the same constant, so an 8-bit reader sees
    # a FLAT patch (spread 0) while a 16-bit reader sees the gradient that is
    # really there.  If this control does not fire, the re-read below is
    # measuring nothing and the whole probe is void.
    h = w = 200
    hi = 180                                    # constant top byte -> flat at 8 bit
    lo_r = np.linspace(0, 255, w)[None, :].repeat(h, 0)
    a16 = np.zeros((h, w, 3), np.uint16)
    a16[..., 0] = (hi << 8) + lo_r.astype(np.uint16)
    a16[..., 1] = (60 << 8)
    a16[..., 2] = (40 << 8)
    kill = os.path.join(SCRATCH, "_r72_bits_kill.png")
    photometry._write_png16(kill, a16)
    s8 = gloss_spread(read8(kill), (0, 0, w, h))
    s16 = gloss_spread(read16(kill), (0, 0, w, h))
    fired = (s8 is not None and s16 is not None
             and abs(s16["spread"] - s8["spread"]) > 1e-9)
    ck("B1 KILL: on a frame whose signal is ONLY in the low byte, the 8-bit read "
       "reports a FLAT patch and the 16-bit read does not",
       fired,
       "8-bit spread %.6f   16-bit spread %.6f" %
       (s8["spread"] if s8 else float('nan'),
        s16["spread"] if s16 else float('nan')))

    # ---------------------------------------------------------------- B2
    frame = sys.argv[1] if len(sys.argv) > 1 else None
    if frame is None:
        print()
        print("  NO FRAME GIVEN -- B2/B3 (the LIVE gate re-read) DID NOT RUN.")
        print("  Pass a hero frame, e.g. `python3 probe_rev72_bits.py "
              "out/r72_hero34f.png`.")
        print("  out/ is untracked and starts EMPTY on a clone.  The controls")
        print("  above stand; the live rows are ABSENT, not passed.")
        print("-" * 78)
        print("  %d checked, %d FAILED, 2 ABSENT (no frame)"
              % (len(checks), len(fails)))
        print("=" * 78)
        return 2 if not fails else 1
    if not os.path.exists(frame):
        print("  NO RENDER -- %s does not exist.  Nothing was measured." % frame)
        return 2

    dep = photometry.read_png(frame)[1]
    box = (520, 610, 1060, 790)                 # gloss_compare WIN["render"]
    a8, a16f = read8(frame), read16(frame)
    g8, g16 = gloss_spread(a8, box), gloss_spread(a16f, box)
    npx = paint_mask(a8, box, os.path.join(SCRATCH, "rev72_bits_glosswin.png"))
    print()
    print("  FRAME %s   on-disk depth %s-bit   window %s   mask %d px"
          % (os.path.basename(frame), 16 if dep == 65535 else 8, box, npx))
    print("  PAINTED: probe_scratch/rev72_bits_glosswin.png -- LOOK AT IT.")
    if g8 is None or g16 is None:
        print("  REFUSING: the window holds fewer than 2000 red px on this "
              "frame -- it is not the gloss window's frame.")
        print("-" * 78)
        print("  %d checked, %d FAILED, 2 ABSENT (wrong frame)"
              % (len(checks), len(fails)))
        return 2
    print()
    print("      statistic      8-bit (PIL)   16-bit (read_png)      delta")
    for k in ("p5", "med", "p95", "p99", "spread", "head"):
        print("      %-9s   %11.5f   %14.5f   %+10.5f"
              % (k, g8[k], g16[k], g16[k] - g8[k]))
    print("      mask px     %11d   %14d   %+10d"
          % (g8["n"], g16["n"], g16["n"] - g8["n"]))

    rel = abs(g16["spread"] / g8["spread"] - 1.0)
    # *** rev 72b -- THIS ROW WAS `ck(..., True, ...)`: AN UNCONDITIONAL PASS. ***
    # A rule-17 adversary counted two of this probe's five rows as rows that
    # CANNOT FAIL, while the brief quoted "5 checked, 0 FAILED" as if all five
    # were tests.  A control that cannot fail is not a control (rule 42's
    # neighbour).  What is actually falsifiable here, and load-bearing for every
    # number above, is that the two readers agree on the eight bits they SHARE --
    # if they did not, the difference could not be attributed to the low byte at
    # all and this whole probe would be measuring a decoder bug.
    a16, mx16 = photometry.read_png(frame)
    top8 = (a16[..., :3] >> 8).astype(np.uint8) if mx16 == 65535 else a16[..., :3]
    pil8 = np.asarray(Image.open(frame).convert("RGB"))
    same = bool(np.array_equal(top8, pil8))
    ck("B2 the 16-bit reader agrees with PIL on the eight bits they SHARE, so "
       "the move below is the LOW BYTE and not a decoder bug",
       same,
       "max top-8 difference %d over %d px; spread moves %+.5f = %.3f %% of the "
       "8-bit value" % (int(np.abs(top8.astype(int) - pil8.astype(int)).max()),
                        top8.shape[0] * top8.shape[1], g16["spread"] - g8["spread"],
                        100 * rel))

    # ---------------------------------------------------------------- B3
    # THE CEILING, MEASURED RATHER THAN ASSERTED.  gloss_compare's verdict
    # divides the render's spread by the PHOTOGRAPH's.  Show that the
    # photograph cannot be re-read, by asking read_png for its depth.
    phot = os.path.join(ROOT, "ref_nolita_front34.jpg")
    photo_16 = False
    why = ""
    try:
        photometry.read_png(phot)
        photo_16 = True
    except Exception as e:
        why = str(e).split("--")[0].strip()[:60]
    ck("B3 the PHOTOGRAPH side of this ratio CANNOT be re-read at 16 bits, so "
       "the gate's precision is floored by it (rule 38)",
       not photo_16,
       "ref_nolita_front34.jpg is JPEG: %s" % (why or "no 16-bit form exists"))

    # ---------------------------------------------------------------- B4
    # WHEN DOES F263 ACTUALLY MATTER?  B2's null is measured on a window whose
    # median sits near 106/255 -- WELL EXPOSED.  F263's bite was on a DARK
    # channel (the red's G near 5 of 255), and F266 showed the 8-bit read of
    # that quantity failing its exposure-invariance test outright.  So the null
    # above must NOT be generalised to "the re-read never matters".
    #
    # MEASURE THE CROSSOVER INSTEAD OF ARGUING IT.  Take the real 16-bit window,
    # stop it DOWN by k (which is what rendering at a lower exposure does),
    # then read it two ways: quantised to 8 bits (what every gate does today)
    # and at full depth.  The divergence is the cost of the 8-bit reader at that
    # exposure.  Same pixels, same statistic, one variable.
    print()
    print("  B4 WHEN THE RE-READ MATTERS -- the SAME window stopped down:")
    print("      stop-down   median/255   spread  8-bit   spread 16-bit    apart")
    raw16, mxv = photometry.read_png(frame)
    sub16 = raw16[..., :3].astype(float) * (255.0 / mxv)
    worst, rungs = 0.0, 0
    for k in (1.0, 1 / 4.0, 1 / 16.0, 1 / 64.0):
        scaled = sub16 * k
        q8 = np.floor(scaled)                      # what an 8-bit file holds
        s_q = gloss_spread(q8, box)
        s_f = gloss_spread(scaled, box)
        if s_q is None or s_f is None:
            print("      x%-9.4f  --  window falls below the mask's L>25 floor; "
                  "REFUSING rather than reporting" % k)
            continue
        apart = abs(s_f["spread"] / s_q["spread"] - 1.0)
        worst = max(worst, apart); rungs += 1
        print("      x%-9.4f  %10.2f   %12.5f   %13.5f   %6.2f %%"
              % (k, s_f["med"], s_q["spread"], s_f["spread"], 100 * apart))
    # *** rev 72b -- ALSO AN UNCONDITIONAL PASS, AND ITS CONCLUSION WAS INVERTED.
    # The first cut asserted True and the rev-73 brief drew from it that this is
    # "why F266's dark-channel ratio was decisively wrong at 8 bits".  IT SHOWS
    # THE OPPOSITE TREND -- divergence FALLS as the window is stopped down
    # (0.46 % -> 0.07 %) -- and it only ever produced TWO points before the
    # mask's own L>25 floor refused.  A ladder that refuses at the third rung
    # has not characterised the dark regime and must not be quoted as if it had.
    # The row now REFUSES unless the ladder actually reached enough rungs to
    # support a trend, which on this window it does not.
    ck("B4 the stop-down ladder reached at least THREE rungs, without which it "
       "has not characterised the dark regime and must not be quoted for one",
       rungs >= 3,
       "%d of %d rungs usable (the rest fall under the mask's own L>25 floor and "
       "REFUSE); worst divergence over the rungs that ran: %.2f %%.  ⚠ THE TREND "
       "IS FALLING, NOT RISING -- this does NOT show 8 bits getting worse in the "
       "dark, and F266 is the evidence for that, not this row"
       % (rungs, 4, 100 * worst))

    print("-" * 78)
    print("  %d checked, %d FAILED%s"
          % (len(checks), len(fails),
             ("  --  " + "; ".join(fails)) if fails else ""))
    print("=" * 78)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
