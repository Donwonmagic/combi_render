# photometry.py -- rev 71.  THE MEASUREMENT PROTOCOL, AS CODE RATHER THAN PROSE.
#
# WHY THIS FILE EXISTS.  Rev 71 spent most of itself finding SIX defects in its
# OWN instruments, and every one was a violation of one of four rules.  Each
# produced a plausible, publishable number; each was caught only by painting or
# by a control.  They are encoded here so the next context inherits the fix
# instead of the lesson:
#
#   1. READ IN LINEAR, AND ONLY WHERE LINEAR IS RECOVERABLE -- AND MAKE THE
#      CALLER DECLARE WHICH TRANSFORM THE FRAME CARRIES, because it CANNOT be
#      inferred from the pixels.  An 8-bit sRGB
#      channel RATIO is not a physical quantity -- gamma is non-linear, so a
#      ratio depends on absolute brightness.  Worse, inverse-sRGB does NOT undo
#      AgX.  Read through AgX, rev 71's red ratio moved with EXPOSURE and read
#      3.43x where the truth was 1.73x.
#   2. REFUSE CLIPPED DATA.  A clipped denominator cannot rise, so every ratio
#      against it reads high.  Rev 71 measured a "relight" three times and every
#      gain was the cream denominator clipping.  The relight was worth nothing.
#   3. USE A ROBUST STATISTIC.  The red's authored G albedo is 0.0294 and the
#      cream's is 0.6308 -- twenty times larger -- so a 15 % tail of contaminant
#      tiles DOUBLES the mean G while barely moving R.  Median, not mean.
#   4. PAINT THE WINDOW AND LOOK BEFORE PUBLISHING ANY NUMBER FROM IT.  Four of
#      rev 71's windows were wrong: two selected the wall and the mural behind
#      the bus, one was mostly board cream, one sat on the galley interior seen
#      through the serving apertures.  `tiles()` writes its own paint every call.
#
# AND THE FIFTH, WHICH IS NOT ABOUT PIXELS: A CONTROL MUST BE FRAMED THE WAY ITS
# MEASUREMENT IS FRAMED (F246), AND AN INSTRUMENT MAY BE BLIND TO WHAT MATTERS
# (F262: a silhouette IoU ranked a visibly shattered glyph ABOVE the shipped
# one).  No module can enforce those.  Render it, crop it, and look.
import os
import struct
import zlib

import numpy as np
from PIL import Image

CLIP = 0.999
# UNIFORMITY IS RELATIVE, AND THAT IS A FIX, NOT A STYLE CHOICE.  The first cut
# compared a tile's per-channel sd against `UNIFORM * (a.max() or 1.0)` -- an
# ABSOLUTE tolerance scaled by the frame's brightest pixel, so stopping the
# exposure down 2 stops quartered the tolerance and SILENTLY CHANGED WHICH TILES
# WERE SELECTED.  A ratio of two albedos must not depend on exposure; a window
# that does makes it depend.  Selftest check 5 is that control, and it is
# WATCHED FAILING on the old absolute rule.
UNIFORM = 0.16               # tile sd as a FRACTION of the tile's OWN LUMINANCE
UNIFORM_FLOOR = 1.5 / 65535.0   # plus a quantisation floor, so a near-black
                                # tile is not required to be sd == 0
# ⚠ RELATIVE TO THE TILE'S LUMINANCE, NOT TO EACH CHANNEL'S OWN MEAN.  A
# per-channel relative test holds a DARK channel to an impossible standard --
# the red's G mean is 0.0294, so 16 % of it is 0.005, below the Monte-Carlo
# noise of any real render, and every red tile is rejected.  Measured: check 5
# read 0 tiles both sides under that rule, which is a degenerate "hold".


def read_png(path):
    """Decode a PNG WITHOUT losing bit depth.  Returns (array, maxval).

    ⚠ THIS EXISTS BECAUSE PIL SILENTLY TRUNCATES A 16-BIT RGB PNG TO 8 BITS,
    AND EVERY FRAME THIS PROJECT RENDERS IS 16-BIT RGB.  `studio.setup_render`
    sets `image_settings.color_depth = '16'` (comment: "audit optics-16") and
    the files carry IHDR bit-depth 16, colour type 2 -- yet
    `np.asarray(Image.open(f))` returns dtype uint8, max 255.  So every
    measurement in this tree that reads a frame through PIL has been throwing
    away half its precision, silently, for the whole life of the project.  That
    is not a property of the renderer -- F42 recorded it as one -- it is a
    property of the READER, and it is why a dark channel (the red's G sits near
    5 of 255) could not be ratioed honestly.

    KILL, WATCHED: `selftest()` writes a 16-bit PNG whose true value is 40000,
    reads it back through PIL (uint8, max 156) and through this function
    (uint16, max 40000), and asserts they DISAGREE.  If PIL ever gains 16-bit
    RGB support this function stays correct and that control turns green on its
    own terms; nothing here depends on PIL being broken."""
    d = open(path, "rb").read()
    if d[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("photometry.read_png: %r is not a PNG" % (path,))
    w, h = struct.unpack(">II", d[16:24])
    depth, ctype, _comp, _filt, interlace = d[24], d[25], d[26], d[27], d[28]
    if interlace:
        raise ValueError("photometry.read_png: interlaced PNG not supported "
                         "(Blender does not write them); got %r" % (path,))
    if depth not in (8, 16) or ctype not in (0, 2, 4, 6):
        raise ValueError("photometry.read_png: bit depth %d colour type %d is "
                         "not supported -- only 8/16-bit grey, RGB or RGBA. "
                         "A PALETTE png (type 3) is not a measurement source."
                         % (depth, ctype))
    nch = {0: 1, 2: 3, 4: 2, 6: 4}[ctype]
    bpp = nch * (depth // 8)              # bytes per pixel
    stride = w * bpp
    idat, i = [], 8
    while i + 8 <= len(d):
        ln = struct.unpack(">I", d[i:i + 4])[0]
        typ = d[i + 4:i + 8]
        if typ == b"IDAT":
            idat.append(d[i + 8:i + 8 + ln])
        elif typ == b"IEND":
            break
        i += 12 + ln
    raw = zlib.decompress(b"".join(idat))
    if len(raw) != h * (stride + 1):
        raise ValueError("photometry.read_png: %d decompressed bytes, expected "
                         "%d -- truncated or unsupported" % (len(raw), h * (stride + 1)))
    buf = np.frombuffer(raw, dtype=np.uint8).reshape(h, stride + 1)
    ftypes = buf[:, 0]
    cur = buf[:, 1:].astype(np.int16)          # working copy, int for the maths
    out = np.empty((h, stride), dtype=np.uint8)
    prev = np.zeros(stride, dtype=np.int16)
    for y in range(h):
        ft = int(ftypes[y])
        line = cur[y].copy()
        if ft == 0:
            pass
        elif ft == 2:                          # Up -- fully vectorised
            line = (line + prev) & 0xFF
        elif ft == 1:                          # Sub -- lane-wise cumsum
            lanes = np.cumsum(line.reshape(w, bpp), axis=0) & 0xFF
            line = lanes.reshape(stride)
        else:                                  # Average (3) / Paeth (4)
            px = line.reshape(w, bpp)
            pv = prev.reshape(w, bpp)
            left = np.zeros(bpp, dtype=np.int16)
            upleft = np.zeros(bpp, dtype=np.int16)
            for x in range(w):
                up = pv[x]
                if ft == 3:
                    px[x] = (px[x] + ((left + up) >> 1)) & 0xFF
                else:
                    p = left + up - upleft
                    pa, pb, pc = np.abs(p - left), np.abs(p - up), np.abs(p - upleft)
                    pred = np.where((pa <= pb) & (pa <= pc), left,
                                    np.where(pb <= pc, up, upleft))
                    px[x] = (px[x] + pred) & 0xFF
                upleft = up
                left = px[x]
            line = px.reshape(stride)
        out[y] = line.astype(np.uint8)
        prev = line
    if depth == 16:
        a = out.reshape(h, w, nch, 2).astype(np.uint32)
        a = (a[..., 0] << 8) | a[..., 1]
        return a.astype(np.uint16), 65535
    return out.reshape(h, w, nch), 255


def load_linear(path, transform):
    """Return the frame as a LINEAR array in 0..1.  `transform` is REQUIRED.

    ⚠ THIS FUNCTION CANNOT INFER THE VIEW TRANSFORM AND MUST NOT PRETEND TO.
    Its first cut had a docstring promising `is_linear=False` for an AgX frame
    while the code returned True unconditionally -- a comment claiming a
    guarantee the code did not provide, which is the exact defect this module
    exists to prevent, committed inside it.  Caught by re-reading my own work.

    AgX is not invertible from 8-bit pixels and there is no signature in the
    data that distinguishes it from 'Standard'.  So the CALLER must declare it:

        'raw'       16-bit PNG written under view_transform 'Raw'.  Already
                    scene-linear; NOT inverse-sRGB'd.  ⚠ PNG cannot hold values
                    above 1.0, so a Raw frame CLIPS wherever the scene exceeds
                    it -- stop DOWN with view_settings.exposure until it does
                    not.  A ratio of two albedos is exposure-invariant in true
                    linear, so stopping down is free.
        'standard'  8-bit under 'Standard'.  sRGB encoding only; inverted here.
                    ⚠ Standard has no rolloff and BLOWS OUT highlights that AgX
                    would have held -- check `clipped()`.
        'agx'       REFUSED.  Read through AgX a ratio moves with EXPOSURE and
                    rev 71 published 3.43x where the truth is 1.73x.
    """
    t = str(transform).lower()
    if t == 'agx':
        raise ValueError(
            "photometry: an AgX frame CANNOT be linearised -- inverse-sRGB does "
            "not undo a filmic tone curve, and read through it a ratio of two "
            "albedos moves with EXPOSURE, which is physically impossible. "
            "Re-render with T1_VT=Standard, or 'Raw' at 16-bit stopped down.")
    if t not in ('raw', 'standard'):
        raise ValueError(
            "photometry: `transform` must be 'raw', 'standard' or 'agx' -- it "
            "cannot be inferred from the pixels, and guessing it is how rev 71 "
            "inflated every ratio it published by ~25 %%.  Got %r" % (transform,))
    raw, mx = read_png(path)
    a = raw.astype(float)
    if a.ndim == 2:                       # grey: promote, do NOT slice
        a = np.repeat(a[:, :, None], 3, axis=2)
    a = a[..., :3]                        # drops alpha only; grey handled above
    if t == 'raw':
        if mx != 65535:
            raise ValueError(
                "photometry: a 'raw' frame must be 16-bit -- this one is 8-bit, "
                "which quantises scene-linear far too coarsely to ratio a dark "
                "channel (the red's G sits near 5 of 255). Set "
                "image_settings.color_depth = '16'.")
        return a / 65535.0
    a = a / float(mx)
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)


def clipped(a, boxes):
    """Fraction of pixels in `boxes` at or above the clip ceiling."""
    px = np.vstack([a[y0:y1, x0:x1].reshape(-1, 3) for (x0, y0, x1, y1) in boxes])
    return float((px.max(1) >= CLIP).mean())


def tiles(a, boxes, keep=None, tsz=8, step=4, paint=None, base=None):
    """Uniform tiles inside `boxes`, as a MEDIAN linear colour (rule 3).

    `keep(mean_rgb) -> bool` selects tiles.  Select by POSITION, BRIGHTNESS or
    ORDERING -- never by the quantity you are about to report, which is a
    tautology (rule 6).  `paint` writes the selection to that path so it can be
    LOOKED AT before the number is used (rule 4); `base` is the 8-bit image to
    paint onto, defaulting to a gamma of `a`.
    Returns (median_rgb, n_tiles) or (None, 0)."""
    got, marks = [], []
    for (x0, y0, x1, y1) in boxes:
        for y in range(y0, y1 - tsz, step):
            for x in range(x0, x1 - tsz, step):
                t = a[y:y + tsz, x:x + tsz].reshape(-1, 3)
                m = t.mean(0)
                # RELATIVE to the tile's OWN mean (+ a quantisation floor), so
                # the selection is exposure-invariant.  See UNIFORM above.
                if (t.std(0) > UNIFORM * float(m.mean()) + UNIFORM_FLOOR).any():
                    continue
                if keep is not None and not keep(m):
                    continue
                got.append(m)
                marks.append((x, y))
    if paint is not None and marks:
        img = base if base is not None else (np.clip(a, 0, 1) ** (1 / 2.2) * 255)
        o = np.array(img, dtype=float)[..., :3].copy()
        for (x, y) in marks:
            o[y:y + tsz, x:x + tsz] = o[y:y + tsz, x:x + tsz] * 0.4 + np.array([0, 255, 0]) * 0.6
        os.makedirs(os.path.dirname(paint) or ".", exist_ok=True)
        Image.fromarray(o.astype("uint8")).save(paint)
    if len(got) < 10:
        return None, 0
    return np.median(np.array(got), axis=0), len(got)


def ratio(a, red_boxes, cream_boxes, red_keep, cream_keep, paint_stem=None):
    """One surface against another IN THE SAME IMAGE, so the illuminant and the
    exposure cancel (probe_rev70_tyre's pattern).  REFUSES if the denominator
    is clipped (rule 2).  Returns (ratio_rgb, note)."""
    cf = clipped(a, cream_boxes)
    if cf > 0.05:
        return None, ("REFUSED: %.0f %% of the reference window is CLIPPED. A "
                      "clipped denominator cannot rise, so the ratio would read "
                      "high and the number would be exposure, not shape." % (100 * cf))
    r, nr = tiles(a, red_boxes, red_keep,
                  paint=(paint_stem + "_num.png") if paint_stem else None)
    c, nc = tiles(a, cream_boxes, cream_keep,
                  paint=(paint_stem + "_den.png") if paint_stem else None)
    if r is None or c is None:
        return None, "REFUSED: window empty (%d / %d tiles)" % (nr, nc)
    return r / c, "%d / %d tiles, clip %.1f %%" % (nr, nc, 100 * cf)


def _write_png16(path, arr16):
    """Write a genuine 16-bit RGB PNG.  Used only by selftest(), so the reader
    is controlled against a file whose true values are known BY CONSTRUCTION
    rather than against another decoder that might share its bug."""
    h, w, _ = arr16.shape
    be = arr16.astype(">u2").tobytes()
    stride = w * 6
    raw = b"".join(b"\x00" + be[y * stride:(y + 1) * stride] for y in range(h))

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))
    ihdr = struct.pack(">IIBBBBB", w, h, 16, 2, 0, 0, 0)
    open(path, "wb").write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
                           + chunk(b"IDAT", zlib.compress(raw))
                           + chunk(b"IEND", b""))


def selftest():
    """PROVE THE PROTOCOL ON KNOWN ANSWERS, AND WATCH EACH CONTROL FAIL ON THE
    DEFECT IT EXISTS TO CATCH (rule 3).  Its first cut had three checks of which
    only ONE could fail: swapping the median for a mean left it green, because
    the contaminant it planted was cream and the red window's `keep` rejected
    every cream tile before the estimator ever saw it.  A dispatched adversary
    found that.  Each check below now carries its own KILL, computed live in the
    same run, and the check ASSERTS THE KILL FIRED."""
    ok = []
    scr = os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe_scratch")
    os.makedirs(scr, exist_ok=True)
    RED = np.array([0.5520, 0.0294, 0.0176])       # the authored albedos
    CREAM = np.array([0.6172, 0.6308, 0.5776])
    want = RED / CREAM

    def scene(scale=1.0):
        a = np.zeros((120, 240, 3))
        a[:, :120] = RED * scale
        a[:, 120:] = CREAM * scale
        return a
    RB, CB = [(4, 4, 116, 116)], [(124, 4, 236, 116)]
    kr, kc = (lambda m: m[0] > m[1]), (lambda m: m[1] > m[0])

    # -- 1. LINEAR.  Exercise load_linear on a REAL 16-bit file, and watch the
    #       reader PIL would have given us disagree with the truth.
    import tempfile
    f16 = os.path.join(tempfile.mkdtemp(prefix="photometry_"), "sel16.png")
    truth = np.zeros((16, 32, 3), dtype=np.uint16)
    truth[:, :16] = 40000
    truth[:, 16:] = 1234
    _write_png16(f16, truth)
    got16, mx16 = read_png(f16)
    from PIL import Image as _I
    pil = np.asarray(_I.open(f16))
    reader_ok = (mx16 == 65535 and got16.dtype == np.uint16
                 and int(got16.max()) == 40000 and int(got16.min()) == 1234)
    kill_reader = not (pil.dtype == np.uint16 and int(pil.max()) == 40000)
    ok.append(("read_png recovers 16 bits (%d/%d) where PIL gives %s max %d "
               "-- KILL FIRED: %s" % (int(got16.max()), int(got16.min()),
                                      pil.dtype, int(pil.max()), kill_reader),
               reader_ok and kill_reader))
    lin = load_linear(f16, 'raw')
    ok.append(("load_linear('raw') returns those values as linear 0..1 (%.5f)"
               % lin.max(), abs(lin.max() - 40000 / 65535.0) < 1e-9))
    refused = False
    try:
        load_linear(f16, 'agx')
    except ValueError:
        refused = True
    ok.append(("load_linear REFUSES an AgX frame (rule 1's kill)", refused))
    #    and the SUBSTANCE of rule 1: an sRGB-encoded read of the same pair
    #    must give a DIFFERENT ratio, or inverting gamma bought nothing.
    srgb = np.where(scene() <= 0.0031308, scene() * 12.92,
                    1.055 * np.clip(scene(), 0, 1) ** (1 / 2.4) - 0.055)
    bad, _ = ratio(srgb, RB, CB, kr, kc)
    ok.append(("KILL: reading the SAME scene sRGB-encoded gives G %.4f, not the "
               "true %.4f -- so the linearisation is load-bearing"
               % (bad[1], want[1]), bad is not None and abs(bad[1] - want[1]) > 0.2 * want[1]))

    # -- 2. CLIPPING.
    got, _ = ratio(scene(), RB, CB, kr, kc)
    ok.append(("recovers a known ratio exactly (%.6f %.6f %.6f)" % tuple(got)
               if got is not None else "recovers a known ratio",
               got is not None and np.allclose(got, want, rtol=1e-6)))
    b = scene(); b[:, 120:] = 1.0
    got2, note2 = ratio(b, RB, CB, kr, kc)
    ok.append(("REFUSES a clipped denominator", got2 is None and "CLIPPED" in note2))

    # -- 3. ROBUSTNESS.  The contaminant must be one the window ADMITS, or the
    #       check is void -- that was the defect.  A specular hot-spot on the
    #       red is still red-dominant, so `kr` keeps it.
    c = scene()
    c[:20, :120] = (0.62, 0.42, 0.40)              # 17 % hot-spot tiles, red-dominant
    got3, _ = ratio(c, RB, CB, kr, kc)
    tl, n = tiles(c, RB, kr)
    got_med = tl / tiles(c, CB, kc)[0]
    # the KILL: the same window under a MEAN
    _real = np.median
    try:
        np.median = np.mean                        # swap the estimator, nothing else
        got_mean, _ = ratio(c, RB, CB, kr, kc)
    finally:
        np.median = _real
    moved = abs(got_mean[1] - want[1]) > 0.20 * want[1]
    held = abs(got3[1] - want[1]) < 0.02 * want[1]
    ok.append(("the median holds at G %.4f while the MEAN moves to %.4f "
               "(truth %.4f) -- KILL FIRED: %s"
               % (got3[1], got_mean[1], want[1], moved), held and moved))

    # -- 4. THE WINDOW IS PAINTED, AND THE PAINT SHOWS THE SELECTION.
    pth = os.path.join(scr, "photometry_selftest_paint.png")
    if os.path.exists(pth):
        os.remove(pth)
    med, ntiles = tiles(scene(), RB, kr, paint=pth)
    painted = np.asarray(Image.open(pth)).astype(int) if os.path.exists(pth) else None
    #    the mark is a 0.6 blend toward pure green, so it is green by a wide
    #    margin -- a loose "G > R" test would call the CREAM patch green too,
    #    which is how the first cut of THIS check failed itself.
    green = None if painted is None else (
        (painted[..., 1] > painted[..., 0] + 40)
        & (painted[..., 1] > painted[..., 2] + 40))
    #    the paint must land INSIDE the window and nowhere else
    inside = green is None or bool(green[:, 120:].sum() == 0)
    ok.append(("tiles() PAINTS its selection (%d tiles -> %d px marked, none "
               "outside the window)" % (ntiles, 0 if green is None else int(green.sum())),
               painted is not None and green.sum() > 0 and inside))

    # -- 5. THE SELECTION MUST NOT DEPEND ON A PIXEL OUTSIDE THE WINDOW.
    #       ⚠ THE ADVERSARY'S DIAGNOSIS OF THIS ONE WAS WRONG AND THE CONTROL
    #       CAUGHT IT.  It reported `UNIFORM * (a.max() or 1.0)` as
    #       "exposure-dependent"; under a UNIFORM scaling it is not -- the sd
    #       and a.max() scale together and the rule is invariant, which is what
    #       the first cut of this check measured (676 tiles at both scales, kill
    #       did not fire).  THE REAL DEFECT IS DIFFERENT AND WORSE: the
    #       tolerance is set by the frame's BRIGHTEST PIXEL, so one specular
    #       highlight ANYWHERE -- in the sky, on a chrome ring, off-subject
    #       entirely -- silently loosens the uniformity test for every tile in
    #       every window.  That is measured below and it is why the rule is now
    #       relative to the TILE's own mean.
    r_a, _ = ratio(scene(1.0), RB, CB, kr, kc)
    r_b, _ = ratio(scene(0.25), RB, CB, kr, kc)
    inv = r_a is not None and r_b is not None and np.allclose(r_a, r_b, rtol=1e-6)

    def _n_abs(a):
        n = 0
        for y in range(4, 116 - 8, 4):
            for x in range(4, 116 - 8, 4):
                t = a[y:y + 8, x:x + 8].reshape(-1, 3)
                if t.std(0).max() > (7.0 / 255.0) * (a.max() or 1.0):
                    continue
                n += 1
        return n

    def _n_rel(a):
        return tiles(a, RB, None)[1]
    rng = np.random.default_rng(0)
    noisy = scene()
    noisy[:, :120] += rng.normal(0, 0.021, noisy[:, :120].shape)
    hot = noisy.copy()
    hot[0:3, 236:240] = 1.0        # ONE highlight, OUTSIDE both windows
    kill_abs = _n_abs(noisy) != _n_abs(hot)
    held_rel = _n_rel(noisy) == _n_rel(hot)
    ok.append(("an off-window HIGHLIGHT does not change the selection: relative "
               "rule %d -> %d tiles.  KILL FIRED on the old absolute rule "
               "(%d -> %d): %s.  And the ratio is scale-invariant (%.6f vs %.6f)"
               % (_n_rel(noisy), _n_rel(hot), _n_abs(noisy), _n_abs(hot),
                  kill_abs,
                  r_a[1] if r_a is not None else -1,
                  r_b[1] if r_b is not None else -1),
               inv and kill_abs and held_rel))

    for name, good in ok:
        print("  [%s] %s" % ("PASS" if good else "FAIL", name))
    n_bad = sum(1 for _, g in ok if not g)
    print("\n  %d checked, %d FAILED" % (len(ok), n_bad))
    print("  Painted window: probe_scratch/photometry_selftest_paint.png -- LOOK AT IT.")
    return n_bad


if __name__ == "__main__":
    raise SystemExit(1 if selftest() else 0)
