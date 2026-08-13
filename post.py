"""
post.py -- lens and film artefacts applied to a FINISHED frame, in numpy.

These live here rather than in the compositor because the hero is rendered in
horizontal strips (the sandbox reaps long background processes), and a bloom
or a vignette computed per strip bands at the seams. Applied once, to the
stitched image, they cannot.

Order is the order a real camera imposes:
    bloom (on the linear image, before the display transform is inverted --
    approximated here by working in linearised sRGB)
    -> chromatic aberration (a property of the taking lens)
    -> vignette -> grain.

    python3 post.py in.png out.png
        [--bloom 1.0] [--ca 1.0] [--vig 1.0] [--grain 1.0]   # per-stage gains
        [--bloom-thr 0.94] [--bloom-sigma 9.0]               # bloom knee
        [--ca-coef 0.0011]                                   # CA strength
        [--backdrop white|headroom] [--backdrop-peak 252.0]  # backdrop A/B
        [--matte PATH|auto] [--mask-level 250] [--mask-chroma 3]

Every long option is parsed (see `main`); an option this file does not know is
a HARD ERROR, not a silent no-op.  Until rev 14 the `--bloom-thr` override was
documented in a comment and accepted by nothing, so `--bloom-thr 0.8` was
swallowed without a word.  A claim in prose is not a guard.

DEFAULTS ARE THE SHIPPED LOOK.  `--backdrop white` is the SPEC sec.6 lock and
is byte-for-byte what this file did at rev 13; `--backdrop headroom` is the
opt-in other arm of the A/B and changes nothing unless it is asked for.
"""
import sys, numpy as np
from PIL import Image


# ------------------------------------------------------------- constants
# Each of these is the CURRENT SHIPPED VALUE and is overridable from the
# command line, so an A/B is one flag rather than one edit.

BLOOM_THR = 0.94        # see bloom() -- rev 13 locked value
BLOOM_SIGMA = 9.0

# LATERAL CA STRENGTH -- MEASURED, NOT YET CHANGED.
# The image is resampled with R scaled by (1 + CA_COEF) and B by (1 - CA_COEF)
# about the frame centre, so a feature at radius r px separates R from B by
#     sep = 2 * CA_COEF * r
# On the shipped 3000x2000 hero the corner radius is sqrt(1500^2 + 1000^2) =
# 1802.78 px, so 0.0011 puts 3.966 px of R-B separation in the corner.  A good
# 78 mm prime gives 1-2 px there.  Evidence that it is visible rather than
# theoretical: corr(R-B, radial luminance gradient) = -0.885 over 10 422
# outer-field edge pixels of the shipped frame.
# The audit recommends halving this to ~0.0005 (1.80 px at the corner).  THAT
# HAS NOT BEEN APPLIED: it is a look change and it gets its own A/B.  Run it
# with `--ca-coef 0.0005`; when the owner accepts it, this line is the edit.
CA_COEF = 0.0011

# --- backdrop A/B ---------------------------------------------------------
# SPEC sec.6 locks the backdrop to PURE WHITE, and `studio.composite_on_white`
# delivers exactly that: display 253-255, linear 0.982-1.000.  Consequences,
# measured on the shipped hero and NOT bugs under that lock -- they are what
# the lock costs:
#     * bloom's mask at thr=0.94 is m = 0.704 ... 1.000 on the backdrop, which
#       lifts it to 1.09-1.16 linear, so the vignette multiply cannot pull it
#       back below 1.0 and it re-clips;
#     * vignette falloff delivered 0.00 +/- 0.01 of its designed 4.4 code
#       values and all four 40x40 corner boxes came out exactly 255.000;
#     * grain high-pass sd 0.0000 in all three channels, 99.51 % of backdrop
#       pixels exactly (255,255,255) over a 4.9 Mpx field.
# `--backdrop headroom` is the OTHER ARM: it scales the backdrop (and only the
# backdrop) so its peak lands at --backdrop-peak display code values, keeps it
# out of bloom's source, and lets grain run at full weight there, so the
# designed vignette falloff and the designed grain are actually rendered.  It
# is opt-in.  Only the owner retires the pure-white lock.
BACKDROP = "white"
BACKDROP_PEAK = 252.0   # display code values, used only by `headroom`

# fallback backdrop-mask thresholds, in display code values (see backdrop_mask)
MASK_LEVEL = 250.0
MASK_CHROMA = 3.0

_LUMA = np.array([0.2126, 0.7152, 0.0722])


def srgb_to_lin(a):
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)


def lin_to_srgb(a):
    a = np.clip(a, 0.0, 1.0)
    return np.where(a <= 0.0031308, a * 12.92, 1.055 * a ** (1 / 2.4) - 0.055)


def _blur(a, sigma):
    """separable gaussian, no scipy dependency"""
    r = max(1, int(sigma * 3))
    x = np.arange(-r, r + 1, dtype=np.float64)
    k = np.exp(-(x ** 2) / (2 * sigma * sigma)); k /= k.sum()
    out = a
    for ax in (0, 1):
        pad = [(0, 0)] * a.ndim
        pad[ax] = (r, r)
        p = np.pad(out, pad, mode='edge')
        sh = [1] * a.ndim
        sh[ax] = k.size
        acc = np.zeros_like(out)
        for i, w in enumerate(k):
            sl = [slice(None)] * a.ndim
            sl[ax] = slice(i, i + a.shape[ax])
            acc += w * p[tuple(sl)]
        out = acc
    return out


def _erode(b, r):
    """binary erosion by a (2r+1) square. Edge-replicated, so the FRAME BORDER
    does not eat the backdrop -- only real subject boundaries do."""
    out = b
    for ax in (0, 1):
        pad = [(0, 0)] * b.ndim
        pad[ax] = (r, r)
        p = np.pad(out, pad, mode='edge')
        acc = np.ones_like(out)
        for i in range(2 * r + 1):
            sl = [slice(None)] * b.ndim
            sl[ax] = slice(i, i + b.shape[ax])
            acc &= p[tuple(sl)]
        out = acc
    return out


def _border_connected(cand, maxit=None):
    """The subset of `cand` reachable from the frame border under 4-connectivity.

    This is the single guard that stops a 255 SPECULAR being called backdrop:
    a highlight on the chrome or a bulb filament is an island of white
    surrounded by vehicle, so it is not reachable from the border and is
    dropped.  scipy is used when it is importable because it is exact and
    fast; the numpy path is a bounded geodesic dilation and warns rather than
    lying if it does not converge.
    """
    try:
        from scipy import ndimage
        lab, _ = ndimage.label(cand)
        edge = np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])
        keep = np.unique(edge)
        keep = keep[keep > 0]
        return np.isin(lab, keep)
    except Exception as e:
        sys.stderr.write("post: scipy unavailable (%s), using numpy flood\n" % e)
        cur = np.zeros_like(cand)
        cur[0] = cur[-1] = True
        cur[:, 0] = cur[:, -1] = True
        cur &= cand
        n = maxit or (cand.shape[0] + cand.shape[1])
        for _ in range(n):
            nxt = cur.copy()
            nxt[1:] |= cur[:-1]; nxt[:-1] |= cur[1:]
            nxt[:, 1:] |= cur[:, :-1]; nxt[:, :-1] |= cur[:, 1:]
            nxt &= cand
            if nxt.sum() == cur.sum():
                return nxt
            cur = nxt
        sys.stderr.write("post: WARNING flood did not converge in %d steps; "
                         "backdrop mask may be incomplete\n" % n)
        return cur


def backdrop_mask(srgb, level=MASK_LEVEL, chroma=MASK_CHROMA,
                  erode=2, feather=1.5):
    """FALLBACK backdrop matte, for when no real matte is supplied.

    THE HONEST SEPARATION IS THE RENDER'S OWN ALPHA, AND IT IS NOT AVAILABLE.
    Measured, not assumed: `studio.setup_render` leaves image_settings.
    color_mode at Blender's default RGBA, so the strips and hero.py's stitched
    `*_raw.png` DO carry an alpha channel -- but `studio.composite_on_white`
    ends in an AlphaOver over an opaque RGB node, so that alpha is 255
    everywhere.  A 64x48 probe render through the real `composite_on_white`
    gave alpha min 255, max 255, unique [255].  So the file has an alpha
    channel and it carries no information.  Getting a real matte means adding
    a File Output node tapping the Render Layers `Alpha` (or a Cryptomatte /
    object-index pass) in studio.py, which this file does not own; until then
    pass one with `--matte PATH` (white = subject) or accept this heuristic.

    The heuristic: a backdrop pixel is (a) at or above `level` in EVERY
    channel, (b) achromatic to within `chroma`, and (c) connected to the frame
    border.  Thresholds are in display code values.

    FAILURE MODES, explicitly, and measured on a 3000x2000 synthetic that
    carries both cases (out/ab/synth_raw.png, built to have a known matte):
      * (c) is what protects the speculars.  Chrome trim, the bulb string and
        the glass hits also reach 255 and are achromatic, and without the
        connectivity test they would be classified as backdrop and pushed down
        with it -- exactly the pixels a lens flares.  It works: of 1878 px of
        255-white specular sitting INSIDE the body, 0 were called backdrop.
      * it does NOT protect a clipped specular sitting ON the sweep -- a bulb
        against the white, a rim light that blows through to the backdrop.  In
        a display-referred frame that pixel is 255 white touching 255 white and
        is connected to the border THROUGH the backdrop, so nothing here can
        separate them: of 791 px of bulb specular lying on the sweep, 791 were
        called backdrop, and in `headroom` they are scaled down with it and
        stop blooming.  ONLY A REAL MATTE FIXES THIS.
      * a white subject region that reaches the frame border (a lid edge blown
        to 255 against the sweep, a white sign face bled off frame) is
        misclassified for the same reason.
      * backdrop seen THROUGH the vehicle -- a serving hatch, a window -- is an
        island and is dropped.  That is the safe direction: it stays pure white,
        i.e. it keeps rev-13 behaviour.
      * the mask is eroded by `erode` px before it is feathered, so the
        anti-aliased silhouette pixels (part subject, part sweep) are NOT
        scaled; the feather then ramps the scale over ~3 px instead of
        stepping it, which would draw a hard outline around the vehicle.
    """
    d = srgb * 255.0
    cand = (d.min(axis=2) >= level) & ((d.max(axis=2) - d.min(axis=2)) <= chroma)
    cand = _border_connected(cand)
    cand = _erode(cand, erode)
    return np.clip(_blur(cand.astype(np.float64), feather), 0.0, 1.0)


def backdrop_headroom(lin, m, peak=BACKDROP_PEAK):
    """Scale the masked backdrop so its peak lands `peak` display code values
    below clipping, leaving room for the vignette and the grain to be SEEN.

    Never brightens (k is clamped to <= 1), and the scale is lerped by the
    feathered mask so the silhouette does not gain an edge.  Returns
    (lin, k, measured_p999_linear).
    """
    lum = lin @ _LUMA
    sel = m > 0.5
    if not sel.any():
        sys.exit("post: --backdrop headroom selected no pixels -- supply "
                 "--matte, or loosen --mask-level / --mask-chroma")
    now = float(np.percentile(lum[sel], 99.9))
    tgt = float(srgb_to_lin(np.array(peak / 255.0)))
    k = min(1.0, tgt / max(now, 1e-9))
    return lin * (1.0 - m + m * k)[..., None], k, now


# rev 13, audit-2 dimension `optics`, severity 5 and it damages the WHOLE frame.
# `main()` reads a DISPLAY-REFERRED PNG in which paper white is 1.0, not the
# scene-linear 21-25 the studio actually renders at -- so a threshold of 0.72
# fires on 70.3 % of the hero and adds ~+0.16 linear EVERYWHERE.  Measured
# consequences on the shipped frame: the vignette delivered 0.00 of its designed
# 4.4 code values and all four corners came out exactly 255.000; the grain's
# high-pass sd was 0.0000 in all three channels and 99.51 % of the backdrop was
# exactly (255,255,255); every specular above 240 was flattened; and the
# silhouette wore a one-sided inward glow.  91 % of the "bloom on the speculars"
# was the subject's own diffuse energy.
#
# In a display-referred frame the only pixels that should bloom are the ones at
# or near clipping.  0.94 puts the knee above the cream (0.78-0.82 typical) and
# above the backdrop's own texture, leaving the speculars and the bulb string --
# which is what a real lens flares.  `--bloom-thr` overrides it for A/B, and as
# of rev 14 the parser actually accepts it.
#
# 0.94 fixed the PAINT (cream at display 224 -> 0.7454 linear -> m = 0.000) but
# NOT the backdrop: pure white at display 253-255 is 0.982-1.000 linear, so
# m = 0.704 ... 1.000 there and the sweep is still lifted to 1.09-1.16 and still
# re-clips.  `exclude` is the other half of that fix and is only ever passed in
# `--backdrop headroom`: a lifted diffuse sweep is not a specular, and if it is
# left in the blur source it re-lifts itself no matter how far it was scaled.
def bloom(lin, amount=1.0, thr=BLOOM_THR, sigma=BLOOM_SIGMA, exclude=None):
    """veiling glare off the brightest speculars only"""
    if amount <= 0:
        return lin
    lum = lin @ _LUMA
    m = np.clip((lum - thr) / max(1e-6, 1.0 - thr), 0, 1)
    if exclude is not None:
        m = m * (1.0 - exclude)      # backdrop cannot be its own glare source
    m = m[..., None]
    return lin + amount * 0.16 * _blur(lin * m, sigma)


def chromatic(lin, amount=1.0, coef=CA_COEF):
    """lateral CA: scale R out and B in about the frame centre"""
    if amount <= 0:
        return lin
    h, w, _ = lin.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    cy, cx = (h - 1) / 2.0, (w - 1) / 2.0
    out = lin.copy()
    for ch, k in ((0, 1.0 + coef * amount), (2, 1.0 - coef * amount)):
        sy = np.clip((yy - cy) / k + cy, 0, h - 1)
        sx = np.clip((xx - cx) / k + cx, 0, w - 1)
        y0 = np.floor(sy).astype(int); x0 = np.floor(sx).astype(int)
        y1 = np.minimum(y0 + 1, h - 1); x1 = np.minimum(x0 + 1, w - 1)
        fy = (sy - y0)[..., None][..., 0]; fx = (sx - x0)[..., None][..., 0]
        c = lin[..., ch]
        out[..., ch] = ((c[y0, x0] * (1 - fx) + c[y0, x1] * fx) * (1 - fy) +
                        (c[y1, x0] * (1 - fx) + c[y1, x1] * fx) * fy)
    return out


def vignette(lin, amount=1.0, strength=0.055):
    """cos^4-ish falloff. Deliberately tiny: SPEC sec.6 wants a PURE white
    backdrop, so this must be felt and not seen."""
    if amount <= 0:
        return lin
    h, w, _ = lin.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    cy, cx = (h - 1) / 2.0, (w - 1) / 2.0
    r = np.sqrt(((xx - cx) / cx) ** 2 + ((yy - cy) / cy) ** 2) / np.sqrt(2)
    return lin * (1.0 - amount * strength * (r ** 2.2))[..., None]


def grain(srgb, amount=1.0, sigma=0.0042, seed=7, full_weight=None):
    """fine, achromatic-dominant film grain, scaled with luminance so it does
    not crawl in the pure-white backdrop.

    That highlight rolloff exists ONLY because SPEC sec.6 pins the backdrop at
    clipping: at display 252 the weight is 1 - (0.988 - 0.86)/0.14 = 0.086, so
    even a backdrop given headroom would still show only 0.09 of the designed
    1.07 code values.  `full_weight` (the backdrop mask, passed only by
    `--backdrop headroom`) lifts the weight back to 1 exactly where the
    backdrop is no longer at clipping, so there is nothing left to suppress.
    """
    if amount <= 0:
        return srgb
    rng = np.random.default_rng(seed)
    h, w, _ = srgb.shape
    lum = srgb @ _LUMA
    w8 = (1.0 - np.clip((lum - 0.86) / 0.14, 0, 1))[..., None]
    if full_weight is not None:
        w8 = np.maximum(w8, full_weight[..., None])
    n = rng.normal(0, sigma, (h, w, 1)) * 0.8 + rng.normal(0, sigma, (h, w, 3)) * 0.2
    return srgb + amount * n * w8


USAGE = __doc__.split("    python3 ")[1].split("\n\nEvery")[0]

# name -> default. Floats are parsed with float(), strings taken verbatim.
_FLOATS = {"bloom": 1.0, "ca": 1.0, "vig": 1.0, "grain": 1.0,
           "bloom-thr": BLOOM_THR, "bloom-sigma": BLOOM_SIGMA,
           "ca-coef": CA_COEF, "backdrop-peak": BACKDROP_PEAK,
           "mask-level": MASK_LEVEL, "mask-chroma": MASK_CHROMA}
_STRS = {"backdrop": BACKDROP, "matte": None}


def _parse(a):
    if len(a) < 2 or a[0].startswith("--") or a[1].startswith("--"):
        sys.exit("post: usage: python3 " + USAGE)
    o = dict(_FLOATS); o.update(_STRS)
    i = 2
    while i < len(a):
        t = a[i]
        k = t[2:] if t.startswith("--") else None
        if k not in o:
            sys.exit("post: unknown option %r. Known: %s"
                     % (t, " ".join("--" + n for n in sorted(o))))
        if i + 1 >= len(a):
            sys.exit("post: %s needs a value" % t)
        o[k] = float(a[i + 1]) if k in _FLOATS else a[i + 1]
        i += 2
    if o["backdrop"] not in ("white", "headroom"):
        sys.exit("post: --backdrop must be white|headroom, got %r" % o["backdrop"])
    if o["matte"] and o["backdrop"] == "white":
        sys.exit("post: --matte has no effect with --backdrop white. Add "
                 "--backdrop headroom, or drop --matte.")
    return a[0], a[1], o


def _mask(o, rgba, srgb):
    """backdrop mask in [0,1]: 1 = backdrop, 0 = subject."""
    if o["matte"] == "auto":
        al = rgba[..., 3].astype(np.float64) / 255.0
        if al.min() == al.max():
            sys.exit("post: --matte auto: %s carries a CONSTANT alpha (%.3f), "
                     "so it is not a matte. studio.composite_on_white ends in "
                     "an AlphaOver over an opaque colour, which is why. Supply "
                     "--matte PATH, or drop --matte for the heuristic."
                     % (o["src"], al.min()))
        return 1.0 - al, "alpha of source"
    if o["matte"]:
        mi = np.asarray(Image.open(o["matte"]).convert("L")).astype(np.float64)
        if mi.shape != srgb.shape[:2]:
            sys.exit("post: --matte is %s, frame is %s"
                     % (mi.shape, srgb.shape[:2]))
        return 1.0 - mi / 255.0, "matte %s (white=subject)" % o["matte"]
    sys.stderr.write("post: WARNING --backdrop headroom without --matte: using "
                     "the heuristic mask (level>=%.0f, chroma<=%.0f, "
                     "border-connected). Speculars that touch the frame border "
                     "will be misclassified as backdrop.\n"
                     % (o["mask-level"], o["mask-chroma"]))
    return (backdrop_mask(srgb, o["mask-level"], o["mask-chroma"]),
            "heuristic level>=%.0f chroma<=%.0f" % (o["mask-level"],
                                                    o["mask-chroma"]))


def main(a):
    src, dst, o = _parse(a)
    o["src"] = src
    rgba = np.asarray(Image.open(src).convert("RGBA"))
    im = rgba[..., :3].astype(np.float64) / 255.0
    lin = srgb_to_lin(im)

    bm = None
    if o["backdrop"] == "headroom":
        bm, how = _mask(o, rgba, im)
        lin, k, now = backdrop_headroom(lin, bm, o["backdrop-peak"])
        print("post: backdrop=headroom mask=%s cover=%.2f%% p99.9=%.4f lin "
              "-> x%.4f (peak %.1f DN)"
              % (how, 100.0 * float((bm > 0.5).mean()), now, k,
                 o["backdrop-peak"]))

    lin = bloom(lin, o["bloom"], o["bloom-thr"], o["bloom-sigma"], exclude=bm)
    lin = chromatic(lin, o["ca"], o["ca-coef"])
    lin = vignette(lin, o["vig"])
    out = grain(lin_to_srgb(lin), o["grain"], full_weight=bm)
    Image.fromarray(np.clip(out * 255 + 0.5, 0, 255).astype(np.uint8)).save(dst)
    print("post: %s -> %s  bloom=%.2f ca=%.2f vig=%.2f grain=%.2f"
          % (src, dst, o["bloom"], o["ca"], o["vig"], o["grain"]))
    print("post: bloom-thr=%.3f bloom-sigma=%.2f ca-coef=%.5f backdrop=%s"
          % (o["bloom-thr"], o["bloom-sigma"], o["ca-coef"], o["backdrop"]))


if __name__ == "__main__":
    main(sys.argv[1:])
