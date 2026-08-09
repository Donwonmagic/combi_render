#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
texgen.py -- procedural texture maps for the 1962 VW Type 2 "Tacombi" taqueria truck.

Writes into ./tex :
    swirl.png    2048 x 2048  RGBA  seamless Mexican folk-art scrollwork, transparent bg
    fascia.png   4096 x  640  RGBA  hand-painted "Tacombi" canopy signboard
    emblem.png   1024 x 1024  RGBA  round taqueria badge

Everything is original artwork built from primitives.  The single drawing
primitive is a "circle chain": a path sampled densely and stamped with filled
discs whose radius varies along the parameter, which is what produces the
calligraphic thick-to-hairline tapers of sign-writer brushwork.

Deterministic: every random draw comes from a seeded numpy Generator.
Pure PIL + numpy (the morphology is hand rolled, no scipy).
"""

import math
import os
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# --------------------------------------------------------------------------- #
# configuration
# --------------------------------------------------------------------------- #

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tex")
SEED = 20620801

SWIRL_SIZE = 2048
SWIRL_SS = 2                      # supersample factor -> 4096 render
SWIRL_TARGET_INK = 0.305          # aim mid-band of the 25-38% requirement
SWIRL_INK_RANGE = (0.25, 0.38)

FASCIA_W, FASCIA_H = 4096, 640
FASCIA_SS = 2
EMBLEM_SIZE = 1024
EMBLEM_SS = 2

# warm gold / amber palette + near-white highlight
GOLD_A = (242, 194, 74)           # #F2C24A
GOLD_B = (232, 161, 26)           # #E8A11A
GOLD_C = (217, 132, 16)           # #D98410
HILITE = (251, 230, 168)          # #FBE6A8
GOLDS = (GOLD_A, GOLD_B, GOLD_C)
BRICK = (142, 27, 18)             # #8E1B12
CREAM = (239, 228, 204)           # #EFE4CC

SCRIPT_FONT = "/root/.claude/skills/canvas-design/canvas-fonts/NothingYouCouldDo-Regular.ttf"
SCRIPT_FALLBACKS = [
    "/root/.claude/skills/canvas-design/canvas-fonts/Lora-Italic.ttf",
    "/root/.claude/skills/canvas-design/canvas-fonts/IBMPlexSerif-Italic.ttf",
]
SANS_CANDIDATES = [
    "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf",
    "/usr/share/fonts/truetype/google-fonts/WorkSans-Bold.ttf",
    "/root/.claude/skills/canvas-design/canvas-fonts/Outfit-Bold.ttf",
    "/root/.claude/skills/canvas-design/canvas-fonts/InstrumentSans-Bold.ttf",
]

TAU = 2.0 * math.pi


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #

def load_font(paths, size):
    """Return (ImageFont, path) for the first path that loads."""
    if isinstance(paths, str):
        paths = [paths]
    for p in paths:
        try:
            return ImageFont.truetype(p, size), p
        except Exception:
            continue
    raise RuntimeError("no usable font among %r" % (paths,))


def jitter_rgb(rng, col, amt=12):
    """
    Per-stroke colour variation.  Varies value/tint along the warm axis rather
    than jittering channels independently, which would swing the golds green.
    """
    f = 1.0 + (amt / 110.0) * rng.uniform(-1.0, 1.0)
    d = rng.uniform(-0.22 * amt, 0.22 * amt)
    return tuple(int(np.clip(c * f + d * (1.0 - 0.25 * i), 0, 255))
                 for i, c in enumerate(col))


def pick_gold(rng, hi_chance=0.10):
    """A gold with slight per-stroke variation; occasionally a highlight tint."""
    if rng.random() < hi_chance:
        return jitter_rgb(rng, HILITE, 8)
    base = GOLDS[int(rng.integers(0, 3))]
    return jitter_rgb(rng, base, 14)


# --------------------------------------------------------------------------- #
# path geometry  (units are arbitrary: the swirl builds in [0,1) tile space,
# the fascia and emblem build directly in supersampled pixels)
# --------------------------------------------------------------------------- #

def _nsamp(length, ds, lo=32, hi=6000):
    """Sample count for a path of the given length at spacing `ds`."""
    return int(np.clip(int(abs(length) / max(ds, 1e-9)) + 2, lo, hi))


def flow_points(rng, p0, ang0, length, curviness, ds=6e-4, n=None):
    """
    A wandering, sine-perturbed path.  Heading is the sum of two sinusoids in
    arclength, so the curve naturally forms long graceful S-bends rather than
    random noise.  Returns (pts[N,2], heading[N]).
    """
    if n is None:
        n = _nsamp(length, ds, lo=48)
    s = np.linspace(0.0, 1.0, n)
    f1 = rng.uniform(0.55, 1.05)
    f2 = rng.uniform(1.7, 3.2)
    a1 = curviness * rng.uniform(0.75, 1.35) * (1.0 if rng.random() < 0.5 else -1.0)
    a2 = curviness * rng.uniform(0.12, 0.38) * (1.0 if rng.random() < 0.5 else -1.0)
    ph1 = rng.uniform(0.0, TAU)
    ph2 = rng.uniform(0.0, TAU)
    hdg = ang0 + a1 * np.sin(TAU * f1 * s + ph1) + a2 * np.sin(TAU * f2 * s + ph2)
    ds = length / (n - 1)
    dx = np.cos(hdg) * ds
    dy = np.sin(hdg) * ds
    x = p0[0] + np.concatenate([[0.0], np.cumsum(dx[:-1])])
    y = p0[1] + np.concatenate([[0.0], np.cumsum(dy[:-1])])
    return np.stack([x, y], axis=1), hdg


def spiral_points(center, r0, r1, a0, sweep, ds=6e-4, n=None):
    """Logarithmic-ish spiral, r0 -> r1 over `sweep` radians from angle a0."""
    if n is None:
        n = _nsamp(abs(sweep) * 0.5 * (r0 + r1), ds, lo=48)
    t = np.linspace(0.0, 1.0, n)
    ang = a0 + sweep * t
    r = r0 * (r1 / max(r0, 1e-9)) ** t
    x = center[0] + r * np.cos(ang)
    y = center[1] + r * np.sin(ang)
    return np.stack([x, y], axis=1)


def curl_points(anchor, ang, size, sign, tightness=None, ds=6e-4, n=None):
    """
    A tendril that leaves `anchor` heading `ang` then coils inward.
    Built as a spiral whose outer end is placed at the anchor.
    """
    sweep = sign * (TAU * (1.05 if tightness is None else tightness))
    r0 = size
    r1 = size * 0.07
    # centre chosen so the spiral's outer point sits on the anchor and the
    # initial tangent runs along `ang`
    a0 = ang - sign * math.pi / 2.0
    cx = anchor[0] - r0 * math.cos(a0)
    cy = anchor[1] - r0 * math.sin(a0)
    return spiral_points((cx, cy), r0, r1, a0, sweep, ds=ds, n=n)


def arc_points(p0, a0, turn, length, ds):
    """Circular arc: heading sweeps `turn` radians over the run. Returns (pts, hdg)."""
    n = _nsamp(length, ds, lo=32)
    t = np.linspace(0.0, 1.0, n)
    ang = a0 + turn * t
    step = length / (n - 1)
    x = p0[0] + np.concatenate([[0.0], np.cumsum(np.cos(ang)[:-1] * step)])
    y = p0[1] + np.concatenate([[0.0], np.cumsum(np.sin(ang)[:-1] * step)])
    return np.stack([x, y], axis=1), ang


def petal_points(center, ang, length, bend, base_frac=0.08, ds=6e-4, n=None):
    """A single petal / leaf spine: straight-ish out from centre with a lateral bow."""
    if n is None:
        n = _nsamp(length * 1.15, ds, lo=28, hi=1200)
    t = np.linspace(0.0, 1.0, n)
    u = np.array([math.cos(ang), math.sin(ang)])
    v = np.array([-u[1], u[0]])
    along = length * (base_frac + (1.0 - base_frac) * t)
    lat = bend * length * np.sin(math.pi * t) * 0.40
    pts = center + np.outer(along, u) + np.outer(lat, v)
    return pts


def teardrop_profile(n, peak=0.42, sharp_tip=0.62, sharp_base=0.45):
    """
    Radius profile: narrow at the base, fat in the body, tapering to the tip.
    Low `sharp_tip` gives the blunt rounded end of a painted folk petal, high
    values give the needle point of a leaf or tendril.
    """
    t = np.linspace(0.0, 1.0, n)
    p = (t + 0.035) ** sharp_base * (1.0 - t + 1e-6) ** sharp_tip
    tp = (peak + 0.035) ** sharp_base * (1.0 - peak) ** sharp_tip
    return p / tp


# blunt, plump petal for flowers; pointed for leaves and buds
def petal_profile(n):
    return teardrop_profile(n, peak=0.60, sharp_tip=0.28, sharp_base=0.55)


def leaf_profile(n):
    return teardrop_profile(n, peak=0.40, sharp_tip=0.70, sharp_base=0.50)


def vine_profile(hdg, taper=0.26, belly=0.55):
    """
    Radius profile for a vine: full weight through the middle, tapering to a
    hairline at both tips, and swelling through the belly of each bend
    (curvature-weighted) the way a loaded brush does.
    """
    n = len(hdg)
    t = np.linspace(0.0, 1.0, n)
    ends = np.clip(np.minimum(t, 1.0 - t) / taper, 0.0, 1.0) ** 0.85
    k = np.abs(np.gradient(hdg))
    kn = k / (k.max() + 1e-9)
    kn = np.convolve(kn, np.ones(15) / 15.0, mode="same")
    kn = kn / (kn.max() + 1e-9)
    return ends * (1.0 - belly + belly * kn)


def decimate(pts, radii, k=0.45, min_step=2.5e-4):
    """Keep points spaced ~0.45*radius apart so stamped discs overlap smoothly."""
    keep = [0]
    last = pts[0]
    for i in range(1, len(pts) - 1):
        step = max(min_step, k * radii[i])
        if np.hypot(*(pts[i] - last)) >= step:
            keep.append(i)
            last = pts[i]
    keep.append(len(pts) - 1)
    idx = np.array(keep, dtype=np.int32)
    return pts[idx].astype(np.float64), radii[idx].astype(np.float64)


def draw_chain(drw, pts, radii, color, min_px=0.42):
    """The one drawing primitive: stamp overlapping filled discs along a path."""
    for (x, y), r in zip(pts, radii):
        if r < min_px:
            r = min_px
        drw.ellipse((x - r, y - r, x + r, y + r), fill=color)


# --------------------------------------------------------------------------- #
# numpy morphology (no scipy)
# --------------------------------------------------------------------------- #

def _shift(a, k, axis):
    if k == 0:
        return a
    out = np.zeros_like(a)
    if axis == 0:
        if k > 0:
            out[k:, :] = a[:-k, :]
        else:
            out[:k, :] = a[-k:, :]
    else:
        if k > 0:
            out[:, k:] = a[:, :-k]
        else:
            out[:, :k] = a[:, -k:]
    return out


def _dilate_line(a, w, axis):
    """Centred dilation by a line of half-width w, via log-doubling shifts."""
    if w <= 0:
        return a
    out = a
    total = 0
    step = 1
    while total < 2 * w:
        s = min(step, 2 * w - total)
        out = np.maximum(out, _shift(out, s, axis))
        total += s
        step *= 2
    return _shift(out, -w, axis)


def dilate_disc(mask, radius):
    """
    Binary dilation with a circular structuring element, numpy only.
    Decomposed into per-row horizontal line dilations unioned over vertical
    shifts; each distinct half-width is computed once.
    """
    r = int(round(radius))
    if r <= 0:
        return mask.copy()
    ys, xs = np.nonzero(mask)
    if len(ys) == 0:
        return mask.copy()
    pad = r + 2
    y0 = max(0, ys.min() - pad)
    y1 = min(mask.shape[0], ys.max() + pad + 1)
    x0 = max(0, xs.min() - pad)
    x1 = min(mask.shape[1], xs.max() + pad + 1)
    sub = mask[y0:y1, x0:x1]
    widths = [int(math.floor(math.sqrt(max(0.0, r * r - dy * dy)))) for dy in range(-r, r + 1)]
    cache = {}
    out = np.zeros_like(sub)
    for dy, w in zip(range(-r, r + 1), widths):
        if w not in cache:
            cache[w] = _dilate_line(sub, w, axis=1)
        out = np.maximum(out, _shift(cache[w], dy, axis=0))
    res = mask.copy()
    res[y0:y1, x0:x1] = out
    return res


def erode1(mask):
    """Erosion by a 3x3 plus-shaped element."""
    out = mask.copy()
    for ax, k in ((0, 1), (0, -1), (1, 1), (1, -1)):
        out = np.minimum(out, _shift(mask, k, ax))
    return out


def stroke_width(mask):
    """Estimate mean stroke width: w = 2*area / boundary_count."""
    area = float(mask.sum())
    if area <= 0:
        return 0.0
    bnd = area - float(erode1(mask).sum())
    if bnd <= 0:
        return 0.0
    return 2.0 * area / bnd


# --------------------------------------------------------------------------- #
# downsample with correct (premultiplied) alpha handling
# --------------------------------------------------------------------------- #

def resolve_rgba(img, out_size, wrap=False, bg_rgb=(232, 161, 26)):
    """
    Downsample an RGBA render.  The source is drawn with hard opaque pixels on a
    zero background, i.e. it is already premultiplied, so LANCZOS is applied
    directly and the result un-premultiplied.  That kills the dark fringe you
    would otherwise get around every stroke.

    wrap=True pads the source by wrapping before resizing and crops afterwards,
    so the filter sees true toroidal neighbours and the output stays exactly
    periodic.
    """
    src = np.asarray(img).astype(np.float64)
    ss = img.size[0] // out_size[0]
    pad = 0
    if wrap:
        pad = 8 * ss
        src = np.pad(src, ((pad, pad), (pad, pad), (0, 0)), mode="wrap")
    tmp = Image.fromarray(np.clip(src, 0, 255).astype(np.uint8), "RGBA")
    tw = src.shape[1] // ss
    th = src.shape[0] // ss
    small = tmp.resize((tw, th), Image.LANCZOS)
    arr = np.asarray(small).astype(np.float64)
    if wrap:
        p = pad // ss
        arr = arr[p:p + out_size[1], p:p + out_size[0]]
    a = arr[..., 3:4]
    rgb = np.where(a > 0.5, arr[..., :3] * (255.0 / np.maximum(a, 1e-6)), 0.0)
    rgb = np.clip(rgb, 0, 255)
    # transparent pixels get a neutral warm colour so GPU filtering never
    # drags black into the edges
    flat = (a[..., 0] <= 0.5)
    for c in range(3):
        rgb[..., c][flat] = bg_rgb[c]
    out = np.concatenate([rgb, np.clip(a, 0, 255)], axis=2).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


# --------------------------------------------------------------------------- #
# 1. swirl.png -- seamless folk-art scrollwork
# --------------------------------------------------------------------------- #
# Commands live in [0,1) tile space:
#     ("chain", pts[N,2], radii[N], rgb)
#     ("disc",  (x, y), r, rgb)
# Everything is stamped nine times at offsets (-1,0,+1)^2, which is exactly
# equivalent to drawing on a 3x3 tiled canvas and cropping the centre.

STROKE_W = 1.0       # global brush-weight trim; motif weights below are set so
DISC_W = 1.0         # the ink calibration lands near 1.0


def _add_chain(cmds, pts, radii, col):
    pts, radii = decimate(pts, np.asarray(radii) * STROKE_W)
    cmds.append(("chain", pts, radii, col))


def _add_disc(cmds, c, r, col):
    cmds.append(("disc", (float(c[0]), float(c[1])), float(r) * DISC_W, col))


def add_flower(cmds, rng, c, R, hi=True):
    """Stylised 5-8 petal folk flower."""
    n = int(rng.integers(5, 9))
    phase = rng.uniform(0, TAU)
    bend = rng.uniform(-0.45, 0.45)
    col = pick_gold(rng, hi_chance=0.02)
    wf = rng.uniform(0.21, 0.27)
    for k in range(n):
        a = phase + TAU * k / n + rng.normal(0, 0.055)
        L = R * rng.uniform(0.86, 1.14)
        pts = petal_points(c, a, L, bend + rng.normal(0, 0.13), base_frac=0.16)
        radii = petal_profile(len(pts)) * (wf * L)
        _add_chain(cmds, pts, radii, jitter_rgb(rng, col, 9))
    _add_disc(cmds, c, R * rng.uniform(0.24, 0.31), pick_gold(rng, 0.35))
    if hi and rng.random() < 0.55:
        off = rng.uniform(0, TAU)
        d = R * 0.13
        _add_disc(cmds, (c[0] + d * math.cos(off), c[1] + d * math.sin(off)),
                  R * 0.085, jitter_rgb(rng, HILITE, 6))


def add_leaf(cmds, rng, base, ang, L, col=None):
    pts = petal_points(base, ang, L, rng.uniform(-0.55, 0.55), base_frac=0.02)
    radii = leaf_profile(len(pts)) * (L * rng.uniform(0.14, 0.20))
    _add_chain(cmds, pts, radii, col if col else pick_gold(rng, 0.05))


def add_bud(cmds, rng, base, ang, L):
    """A teardrop petal on a short stem."""
    stem = petal_points(base, ang, L * 0.55, rng.uniform(-0.3, 0.3), base_frac=0.0)
    sr = np.linspace(1.0, 0.35, len(stem)) * (L * 0.045)
    _add_chain(cmds, stem, sr, pick_gold(rng, 0.05))
    tip = stem[-1]
    pts = petal_points(tip, ang + rng.normal(0, 0.2), L * 0.55, rng.uniform(-0.35, 0.35),
                       base_frac=0.0)
    radii = teardrop_profile(len(pts), peak=0.45) * (L * rng.uniform(0.13, 0.19))
    _add_chain(cmds, pts, radii, pick_gold(rng, 0.08))


def add_curl(cmds, rng, anchor, ang, size, sign=None, w=0.0035):
    """
    A tendril flourish.  `w` is the stroke radius where it leaves the anchor;
    it coils inward tapering to a fine point.
    """
    if sign is None:
        sign = 1 if rng.random() < 0.5 else -1
    pts = curl_points(anchor, ang, size, sign, tightness=rng.uniform(0.85, 1.5))
    t = np.linspace(0, 1, len(pts))
    radii = np.clip(t / 0.05, 0, 1) * ((1.0 - t) ** 0.85) * w
    _add_chain(cmds, pts, radii, pick_gold(rng, 0.09))


def add_dots(cmds, rng, c, R):
    n = int(rng.integers(3, 6))
    a0 = rng.uniform(0, TAU)
    arc = rng.uniform(0.7, 2.1)
    col = pick_gold(rng, 0.20)
    for k in range(n):
        a = a0 + arc * (k / max(1, n - 1) - 0.5)
        d = R * (0.55 + 0.45 * k / max(1, n - 1))
        r = R * rng.uniform(0.10, 0.19)
        _add_disc(cmds, (c[0] + d * math.cos(a), c[1] + d * math.sin(a)), r,
                  jitter_rgb(rng, col, 10))


def add_vine(cmds, rng, p0, ang, length, weight):
    pts, hdg = flow_points(rng, p0, ang, length, curviness=rng.uniform(0.9, 1.9))
    # keep the whole element inside [-1,2] so the 3x3 stamping fully covers it
    ctr = pts.mean(axis=0)
    pts = pts - ctr + np.mod(ctr, 1.0)
    radii = vine_profile(hdg) * weight
    col = pick_gold(rng, 0.0)
    _add_chain(cmds, pts, radii, col)

    # a fine highlight stroke riding the inside of the vine
    if rng.random() < 0.55:
        nrm = np.stack([-np.sin(hdg), np.cos(hdg)], axis=1)
        side = 1.0 if rng.random() < 0.5 else -1.0
        a, b = sorted(rng.uniform(0.15, 0.9, 2))
        if b - a > 0.16:
            i0, i1 = int(a * len(pts)), int(b * len(pts))
            hp = pts[i0:i1] + nrm[i0:i1] * (radii[i0:i1, None] * 0.42 * side)
            t = np.linspace(0, 1, len(hp))
            hr = np.sin(math.pi * t) ** 0.6 * radii[i0:i1] * 0.26
            if len(hp) > 6:
                _add_chain(cmds, hp, hr, jitter_rgb(rng, HILITE, 6))

    # coils at both tips
    for end, tang in ((pts[-1], hdg[-1]), (pts[0], hdg[0] + math.pi)):
        if rng.random() < 0.85:
            add_curl(cmds, rng, end, tang, length * rng.uniform(0.07, 0.13),
                     w=weight * rng.uniform(0.5, 0.8))

    # ornaments budding off the vine
    nrm = np.stack([-np.sin(hdg), np.cos(hdg)], axis=1)
    ts = np.sort(rng.uniform(0.06, 0.94, int(rng.integers(4, 7))))
    for t in ts:
        i = int(t * (len(pts) - 1))
        side = 1.0 if rng.random() < 0.5 else -1.0
        n_ = nrm[i] * side
        base = pts[i] + n_ * radii[i] * 0.8
        ang_out = math.atan2(n_[1], n_[0]) + rng.normal(0, 0.45)
        roll = rng.random()
        if roll < 0.42:
            stem_l = length * rng.uniform(0.035, 0.075)
            stem = petal_points(base, ang_out, stem_l, rng.uniform(-0.4, 0.4),
                                base_frac=0.0)
            _add_chain(cmds, stem, np.linspace(1.0, 0.45, len(stem)) * weight * 0.55,
                       pick_gold(rng, 0.05))
            add_flower(cmds, rng, stem[-1], length * rng.uniform(0.022, 0.036))
        elif roll < 0.62:
            add_leaf(cmds, rng, base, ang_out, length * rng.uniform(0.055, 0.095))
        elif roll < 0.78:
            add_curl(cmds, rng, base, ang_out, length * rng.uniform(0.04, 0.085),
                     w=weight * rng.uniform(0.40, 0.65))
        elif roll < 0.90:
            add_bud(cmds, rng, base, ang_out, length * rng.uniform(0.055, 0.095))
        else:
            add_dots(cmds, rng, base + n_ * length * 0.04, length * 0.042)


def occupancy(cmds, G=28):
    """Coarse toroidal ink map, used to find bald patches."""
    occ = np.zeros((G, G))
    for cmd in cmds:
        if cmd[0] == "chain":
            pts, radii = cmd[1], cmd[2]
            p = pts[::3]
            r = radii[::3]
            gi = np.mod((p[:, 1] * G).astype(int), G)
            gj = np.mod((p[:, 0] * G).astype(int), G)
            np.add.at(occ, (gi, gj), r * r * 40.0 + 1e-4)
        else:
            (x, y), r = cmd[1], cmd[2]
            occ[int(y * G) % G, int(x * G) % G] += r * r * 40.0
    return occ


def build_swirl(rng):
    cmds = []
    # --- main wandering vines, starts on a jittered 3x3 lattice -------------
    starts = []
    for i in range(3):
        for j in range(3):
            starts.append(((j + rng.uniform(0.15, 0.85)) / 3.0,
                           (i + rng.uniform(0.15, 0.85)) / 3.0))
    rng.shuffle(starts)
    starts = starts[:7]
    base_ang = rng.uniform(0, TAU)
    for k, s in enumerate(starts):
        ang = base_ang + k * (TAU / len(starts)) + rng.normal(0, 0.5)
        add_vine(cmds, rng, np.array(s), ang,
                 length=rng.uniform(1.05, 1.5),
                 weight=rng.uniform(0.0058, 0.0082))

    # --- secondary short scrolls -------------------------------------------
    for _ in range(5):
        s = np.array([rng.random(), rng.random()])
        add_vine(cmds, rng, s, rng.uniform(0, TAU),
                 length=rng.uniform(0.42, 0.72),
                 weight=rng.uniform(0.0034, 0.0050))

    # --- fill the bald patches so the coverage reads evenly ----------------
    for _round in range(2):
        G = 28
        occ = occupancy(cmds, G)
        blur = occ.copy()
        for ax in (0, 1):
            blur = (blur + np.roll(blur, 1, ax) + np.roll(blur, -1, ax)) / 3.0
        order = np.argsort(blur, axis=None)
        placed = []
        for flat in order:
            gi, gj = divmod(int(flat), G)
            c = np.array([(gj + rng.uniform(0.25, 0.75)) / G,
                          (gi + rng.uniform(0.25, 0.75)) / G])
            if any(np.hypot(*np.minimum(np.abs(c - q), 1 - np.abs(c - q))) < 0.16
                   for q in placed):
                continue
            placed.append(c)
            roll = rng.random()
            if roll < 0.45:
                add_flower(cmds, rng, c, rng.uniform(0.027, 0.042))
                a = rng.uniform(0, TAU)
                add_curl(cmds, rng, c + 0.065 * np.array([math.cos(a), math.sin(a)]),
                         a, rng.uniform(0.04, 0.070), w=rng.uniform(0.0022, 0.0034))
            elif roll < 0.72:
                a = rng.uniform(0, TAU)
                add_vine(cmds, rng, c, a, length=rng.uniform(0.26, 0.44),
                         weight=rng.uniform(0.0026, 0.0040))
            elif roll < 0.90:
                a = rng.uniform(0, TAU)
                add_leaf(cmds, rng, c, a, rng.uniform(0.055, 0.090))
                add_leaf(cmds, rng, c, a + rng.uniform(2.2, 3.9), rng.uniform(0.045, 0.075))
                add_dots(cmds, rng, c, 0.042)
            else:
                add_dots(cmds, rng, c, rng.uniform(0.035, 0.060))
            if len(placed) >= 6:
                break

    # scattered dot triads to break up the remaining flat red
    for _ in range(10):
        add_dots(cmds, rng, np.array([rng.random(), rng.random()]), rng.uniform(0.028, 0.05))

    # sanity: the 3x3 stamping only covers support inside [-1, 2]
    cmds = wrap_cmds(cmds)
    for cmd in cmds:
        if cmd[0] == "chain":
            p, r = cmd[1], cmd[2]
            lo = (p - r[:, None]).min()
            hi = (p + r[:, None]).max()
        else:
            lo = min(cmd[1]) - cmd[2]
            hi = max(cmd[1]) + cmd[2]
        assert -1.0 <= lo and hi <= 2.0, "element escapes the 3x3 stamp window"
    return cmds


def render_swirl(cmds, N, ink=1.0):
    img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    drw = ImageDraw.Draw(img)
    offs = (-1, 0, 1)
    for cmd in cmds:
        if cmd[0] == "chain":
            pts, radii, col = cmd[1], cmd[2], cmd[3]
            rmax = radii.max() * ink
            bx0, by0 = pts[:, 0].min() - rmax, pts[:, 1].min() - rmax
            bx1, by1 = pts[:, 0].max() + rmax, pts[:, 1].max() + rmax
            rgba = col + (255,)
            for ox in offs:
                if bx1 + ox < 0.0 or bx0 + ox > 1.0:
                    continue
                for oy in offs:
                    if by1 + oy < 0.0 or by0 + oy > 1.0:
                        continue
                    X = (pts[:, 0] + ox) * N
                    Y = (pts[:, 1] + oy) * N
                    R = radii * (N * ink)
                    m = (X + R >= 0) & (X - R < N) & (Y + R >= 0) & (Y - R < N)
                    draw_chain(drw, np.stack([X[m], Y[m]], axis=1), R[m], rgba)
        else:
            (x, y), r, col = cmd[1], cmd[2], cmd[3]
            rgba = col + (255,)
            for ox in offs:
                for oy in offs:
                    px = (x + ox) * N
                    py = (y + oy) * N
                    pr = max(0.42, r * N * ink)
                    if px + pr < 0 or px - pr > N or py + pr < 0 or py - pr > N:
                        continue
                    drw.ellipse((px - pr, py - pr, px + pr, py + pr), fill=rgba)
    return img


def wrap_cmds(cmds):
    """
    Re-anchor every element so its centroid sits in [0,1).  Because the drawing
    is stamped over the 3x3 neighbourhood, shifting an element by a whole tile
    cannot change the rendered result - it only guarantees that the element's
    support stays inside the stamped window.
    """
    out = []
    for cmd in cmds:
        if cmd[0] == "chain":
            p = cmd[1]
            sh = np.floor(p.mean(axis=0))
            out.append(("chain", p - sh, cmd[2], cmd[3]))
        else:
            x, y = cmd[1]
            out.append(("disc", (x - math.floor(x), y - math.floor(y)), cmd[2], cmd[3]))
    return out


def translate_cmds(cmds, dx, dy):
    out = []
    for cmd in cmds:
        if cmd[0] == "chain":
            p = cmd[1].copy()
            p[:, 0] += dx
            p[:, 1] += dy
            out.append(("chain", p, cmd[2], cmd[3]))
        else:
            out.append(("disc", (cmd[1][0] + dx, cmd[1][1] + dy), cmd[2], cmd[3]))
    return wrap_cmds(out)


def ink_fraction(img):
    a = np.asarray(img)[..., 3]
    return float((a > 127).mean())


def make_swirl(path):
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    cmds = build_swirl(rng)
    npts = sum(len(c[1]) for c in cmds if c[0] == "chain")
    print("[swirl] %d elements, %d stamps" % (len(cmds), npts))

    # ---- calibrate stroke weight to land inside the 25-38% ink window -----
    def probe(ink, n=768):
        return ink_fraction(render_swirl(cmds, n, ink=ink))

    lo, hi = 0.30, 2.4
    f_lo, f_hi = probe(lo), probe(hi)
    print("[swirl] calibration bracket: ink %.2f -> %.3f, ink %.2f -> %.3f"
          % (lo, f_lo, hi, f_hi))
    assert f_lo < SWIRL_TARGET_INK < f_hi, "target ink not bracketed - retune density"
    ink = 1.0
    for _ in range(7):
        ink = 0.5 * (lo + hi)
        f = probe(ink)
        if f < SWIRL_TARGET_INK:
            lo = ink
        else:
            hi = ink
        if abs(f - SWIRL_TARGET_INK) < 0.004:
            break
    print("[swirl] calibrated ink scale = %.4f (probe %.4f)  [%.1fs]"
          % (ink, f, time.time() - t0))

    # ---- periodicity proof --------------------------------------------------
    # Translating every element by (0.25, 0.375) of a tile must reproduce the
    # same raster as np.roll-ing the untranslated render by the same amount.
    # Individual boundary pixels can flip on floating-point ties, so the strict
    # test is done on 8x8 block means, where any real structural break (a motif
    # not stamped into a neighbouring tile) shows up immediately.
    Nv = 512
    base = np.asarray(render_swirl(cmds, Nv, ink=ink))[..., 3].astype(np.float64)
    shifted = np.asarray(render_swirl(translate_cmds(cmds, 0.25, 0.375), Nv,
                                      ink=ink))[..., 3].astype(np.float64)
    rolled = np.roll(base, (int(0.375 * Nv), int(0.25 * Nv)), axis=(0, 1))
    mism = float((shifted != rolled).mean())
    B = 8
    blk = lambda a: a.reshape(Nv // B, B, Nv // B, B).mean(axis=(1, 3))
    bdiff = float(np.abs(blk(shifted) - blk(rolled)).max()) / 255.0
    print("[swirl] toroidal check: per-pixel mismatch %.2e, max 8x8 block diff %.4f"
          % (mism, bdiff))
    assert mism < 1e-3 and bdiff < 0.25, "drawing is not periodic"

    # ---- final render -----------------------------------------------------
    # The low-res probe runs slightly heavy against the supersampled render, so
    # close the loop on the real thing.
    N = SWIRL_SIZE * SWIRL_SS
    best = None
    for attempt in range(4):
        big = render_swirl(cmds, N, ink=ink)
        img = resolve_rgba(big, (SWIRL_SIZE, SWIRL_SIZE), wrap=True)
        frac = ink_fraction(img)
        print("[swirl] full render ink=%.4f -> coverage %.4f  [%.1fs]"
              % (ink, frac, time.time() - t0))
        if best is None or abs(frac - SWIRL_TARGET_INK) < abs(best[1] - SWIRL_TARGET_INK):
            best = (img, frac)
        if abs(frac - SWIRL_TARGET_INK) <= 0.015:
            break
        ink *= (SWIRL_TARGET_INK / max(frac, 1e-6)) ** 0.9
    img, frac = best
    img.save(path)
    return img


def verify_swirl(path):
    img = Image.open(path)
    a = np.asarray(img)[..., 3].astype(np.float64)
    frac = float((a > 127.5).mean())

    # seam continuity: the wrap-around difference must look like any interior
    # neighbouring-column difference, i.e. no discontinuity at the tile edge
    seam_x = np.abs(a - np.roll(a, 1, axis=1))[:, 0].mean()
    inner_x = np.abs(a[:, 1:] - a[:, :-1]).mean()
    seam_y = np.abs(a - np.roll(a, 1, axis=0))[0, :].mean()
    inner_y = np.abs(a[1:, :] - a[:-1, :]).mean()
    print("[swirl] seam L/R diff %.3f vs interior %.3f   T/B diff %.3f vs interior %.3f"
          % (seam_x, inner_x, seam_y, inner_y))
    assert seam_x <= 1.5 * inner_x + 0.5, "left/right edges do not tile"
    assert seam_y <= 1.5 * inner_y + 0.5, "top/bottom edges do not tile"
    return img.size, img.mode, frac


# --------------------------------------------------------------------------- #
# 2. fascia.png -- the canopy signboard
# --------------------------------------------------------------------------- #

def text_mask(font, text, size, pos, anchor="mm"):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).text(pos, text, font=font, fill=255, anchor=anchor)
    return np.asarray(m) > 127


def flourish(drw, rng, x, y, size, flip=1.0):
    """
    A gold sign-writer's scroll, built in local coordinates (+x runs outward,
    away from the word) and then mirrored, so the two sides match.  Same
    tapered circle-chain routine as the swirl tile.
    """
    def place(pts):
        out = np.empty_like(pts)
        out[:, 0] = x + flip * pts[:, 0]
        out[:, 1] = y + pts[:, 1]
        return out

    def stroke(pts, radii, col):
        draw_chain(drw, *decimate(place(pts), radii, min_step=1.0), color=col + (255,))

    # main sweep: leaves the word thick, arcs up and tapers to a hairline
    for lane, (a0, turn, ln, wt, drop) in enumerate((
            (-0.30, 1.55, 2.05, 0.105, 0.0),
            (0.34, -1.35, 1.30, 0.055, 0.10))):
        pts, hdg = arc_points(np.array([0.10 * size, drop * size]), a0, turn,
                              ln * size, ds=1.5)
        t = np.linspace(0, 1, len(pts))
        radii = (np.clip(t / 0.10, 0, 1) ** 0.55) * ((1.0 - t) ** 0.80) * (wt * size)
        stroke(pts, radii, pick_gold(rng, 0.0))
        # coil the tip
        cp = curl_points(pts[-1], hdg[-1], size * (0.30 if lane == 0 else 0.20),
                         1 if turn > 0 else -1, tightness=1.15, ds=1.5)
        tc = np.linspace(0, 1, len(cp))
        cr = np.clip(tc / 0.06, 0, 1) * ((1 - tc) ** 0.85) * (wt * size * 0.42)
        stroke(cp, cr, pick_gold(rng, 0.0))

    # a pair of teardrop leaves and a trail of dots
    for ang, ln in ((-1.15, 0.62), (0.95, 0.50)):
        pp = petal_points(np.array([0.30 * size, 0.04 * size]), ang, ln * size,
                          0.30, base_frac=0.05, ds=1.5)
        pr = petal_profile(len(pp)) * (size * 0.115)
        stroke(pp, pr, pick_gold(rng, 0.10))
    for k in range(3):
        d = size * (0.95 + 0.30 * k)
        r = size * (0.075 - 0.017 * k)
        px, py = x + flip * d, y + size * (0.30 + 0.12 * k)
        drw.ellipse((px - r, py - r, px + r, py + r), fill=pick_gold(rng, 0.2) + (255,))


def make_fascia(path, word="Tacombi", fill=None, key=(232, 172, 60),
                box=(0.55, 0.70), flour=True, out_size=None):
    fill = BRICK if fill is None else fill
    rng = np.random.default_rng(SEED + 11)
    W, H = FASCIA_W * FASCIA_SS, FASCIA_H * FASCIA_SS
    try:
        _f, used = load_font(SCRIPT_FONT, 200)
        font_path = SCRIPT_FONT
    except Exception:
        _f, font_path = load_font(SCRIPT_FALLBACKS, 200)
    print("[fascia] script font: %s" % os.path.basename(font_path))

    # --- linear metrics at a reference size, so one solve gives the size ----
    REF = 200
    fref = ImageFont.truetype(font_path, REF)
    probe = Image.new("L", (REF * 8, REF * 5), 0)
    ImageDraw.Draw(probe).text((REF * 4, REF * 2.5), word, font=fref, fill=255, anchor="mm")
    pm = np.asarray(probe) > 127
    ys, xs = np.nonzero(pm)
    w1 = (xs.max() - xs.min() + 1) / REF
    h1 = (ys.max() - ys.min() + 1) / REF
    capm = text_mask(fref, "T", (REF * 8, REF * 5), (REF * 4, REF * 2.5))
    cys, _cxs = np.nonzero(capm)
    c1 = (cys.max() - cys.min() + 1) / REF          # cap height per font unit
    s1 = stroke_width(pm) / REF                      # native stroke per font unit
    target_ratio = 0.175                             # stroke width / cap height
    k = max(0.0, (target_ratio * c1 - s1) / 2.0)     # dilation radius per font unit
    box_w, box_h = box[0] * W, box[1] * H
    size = int(min(box_w / (w1 + 2 * k), box_h / (h1 + 2 * k)))
    dil = int(round(k * size))
    print("[fascia] font size %d, native stroke %.1fpx, dilation radius %dpx, "
          "target stroke %.1fpx (%.1f%% of %.0fpx cap)"
          % (size, s1 * size, dil, target_ratio * c1 * size,
             100 * target_ratio, c1 * size))

    font = ImageFont.truetype(font_path, size)
    mask = text_mask(font, word, (W, H), (W // 2, int(H * 0.52)))
    # centre on the ink bounding box, not the font metrics box: a script face
    # has large asymmetric side bearings and the "mm" anchor leaves the word
    # visibly high and off to one side
    iy, ix = np.nonzero(mask)
    mask = _shift(mask, int(W / 2 - (ix.min() + ix.max()) / 2), 1)
    mask = _shift(mask, int(H / 2 - (iy.min() + iy.max()) / 2), 0)
    letters = dilate_disc(mask, dil)
    got = stroke_width(letters)
    print("[fascia] thickened stroke %.1fpx = %.1f%% of cap height"
          % (got, 100.0 * got / (c1 * size)))
    outline = dilate_disc(letters, 4 * FASCIA_SS)

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    arr = np.zeros((H, W, 4), np.uint8)
    arr[outline] = key + (255,)                      # keyline
    arr[letters] = fill + (255,)
    # subtle hand-mixed variation in the brick red
    ys, xs = np.nonzero(letters)
    if len(ys):
        n = np.sin(xs / 90.0) * 6 + np.cos(ys / 55.0) * 5
        for c, base in enumerate(fill):
            arr[ys, xs, c] = np.clip(base + n * (1.0 - 0.3 * c), 0, 255).astype(np.uint8)
    img = Image.fromarray(arr, "RGBA")
    drw = ImageDraw.Draw(img)

    ink_x0 = xs.min() if len(xs) else W // 4
    ink_x1 = xs.max() if len(xs) else 3 * W // 4
    fs = H * 0.25
    if flour:
        flourish(drw, rng, ink_x0 - fs * 1.85, H * 0.44, fs, flip=-1.0)
        flourish(drw, rng, ink_x1 + fs * 1.85, H * 0.44, fs, flip=1.0)

    out = resolve_rgba(img, out_size or (FASCIA_W, FASCIA_H))
    out.save(path)
    return out


# --------------------------------------------------------------------------- #
# 3. emblem.png -- round taqueria badge
# --------------------------------------------------------------------------- #

def ring(drw, c, r_out, r_in, col):
    drw.ellipse((c - r_out, c - r_out, c + r_out, c + r_out), fill=col + (255,))
    drw.ellipse((c - r_in, c - r_in, c + r_in, c + r_in), fill=CREAM + (255,))


def arched_text(img, font, text, center, radius, deg_per_extra=0.0, color=(0, 0, 0),
                spacing=1.0, up=True):
    """Set text along a circular arc, one rotated glyph at a time."""
    d = ImageDraw.Draw(img)
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    total_ang = total / radius
    a = -math.pi / 2.0 - total_ang / 2.0 if up else math.pi / 2.0 + total_ang / 2.0
    S = int(font.size * 4)
    cum = 0.0
    for ch, w in zip(text, widths):
        mid = cum + w / 2.0
        th = (a + mid / radius) if up else (a - mid / radius)
        tile = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        ImageDraw.Draw(tile).text((S // 2, S // 2), ch, font=font,
                                  fill=color + (255,), anchor="ms")
        rot = tile.rotate(-math.degrees(th + math.pi / 2.0), resample=Image.BICUBIC,
                          expand=False, center=(S / 2, S / 2))
        px = center[0] + radius * math.cos(th)
        py = center[1] + radius * math.sin(th)
        img.alpha_composite(rot, (int(round(px - S / 2)), int(round(py - S / 2))))
        cum += w + spacing


def make_emblem(path):
    rng = np.random.default_rng(SEED + 23)
    S = EMBLEM_SIZE * EMBLEM_SS
    c = S / 2.0
    u = S / 1024.0                                    # px per final pixel
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    drw = ImageDraw.Draw(img)

    R = 496 * u
    drw.ellipse((c - R, c - R, c + R, c + R), fill=CREAM + (255,))
    ring(drw, c, R, R - 19 * u, GOLD_B)               # gold outer ring
    ring(drw, c, R - 33 * u, R - 41 * u, BRICK)       # thin red ring
    ring(drw, c, R - 55 * u, R - 65 * u, GOLD_B)      # gold inner ring

    font, fp = load_font(SANS_CANDIDATES, int(96 * u))
    print("[emblem] sans font: %s" % os.path.basename(fp))
    # baseline radius chosen so the cap height clears the inner gold ring
    arched_text(img, font, "TACOMBI", (c, c), 346 * u, color=BRICK, spacing=12 * u, up=True)

    bfont, _ = load_font(SANS_CANDIDATES, int(74 * u))
    bw = drw.textlength("TAQUERIA", font=bfont) + 10 * u * 7
    x = c - bw / 2.0
    for ch in "TAQUERIA":                              # letterspaced, straight
        drw.text((x, c + 300 * u), ch, font=bfont, fill=BRICK + (255,), anchor="lt")
        x += drw.textlength(ch, font=bfont) + 10 * u

    # small red diamonds separating the two texts
    for sgn in (-1, 1):
        px, py = c + sgn * 372 * u, c + 34 * u
        s = 15 * u
        drw.polygon([(px, py - s), (px + s, py), (px, py + s), (px - s, py)],
                    fill=BRICK + (255,))
        drw.ellipse((px - s * 0.34, py - s * 0.34, px + s * 0.34, py + s * 0.34),
                    fill=GOLD_B + (255,))

    # gold folk-art rosette in the middle
    cen = np.array([c, c - 6 * u])
    for L, wf, n, ph, col in ((150 * u, 0.34, 8, 0.0, GOLD_C),
                              (104 * u, 0.36, 8, math.pi / 8, GOLD_A)):
        for k in range(n):
            a = ph + TAU * k / n + rng.normal(0, 0.03)
            pp = petal_points(cen, a, L * rng.uniform(0.94, 1.06),
                              rng.uniform(-0.16, 0.16), ds=1.5)
            pr = teardrop_profile(len(pp)) * (wf * L)
            draw_chain(drw, *decimate(pp, pr, min_step=1.0),
                       color=jitter_rgb(rng, col, 8) + (255,))
    for r, col in ((40 * u, BRICK), (26 * u, GOLD_A), (10 * u, BRICK)):
        drw.ellipse((cen[0] - r, cen[1] - r, cen[0] + r, cen[1] + r), fill=col + (255,))
    for k in range(8):
        a = TAU * k / 8 + math.pi / 8
        d = 196 * u
        r = 9 * u
        px, py = cen[0] + d * math.cos(a), cen[1] + d * math.sin(a)
        drw.ellipse((px - r, py - r, px + r, py + r), fill=GOLD_C + (255,))

    # tiny leaf sprigs left and right of the rosette
    for sgn in (-1, 1):
        base = np.array([c + sgn * 222 * u, c - 6 * u])
        out = 0.0 if sgn > 0 else math.pi
        pp = petal_points(base, out, 78 * u, 0.22 * sgn, base_frac=0.06, ds=1.5)
        pr = leaf_profile(len(pp)) * 17 * u
        draw_chain(drw, *decimate(pp, pr, min_step=1.0), color=GOLD_C + (255,))
        r = 9 * u
        px = c + sgn * 296 * u
        drw.ellipse((px - r, c - 6 * u - r, px + r, c - 6 * u + r), fill=GOLD_C + (255,))

    out = resolve_rgba(img, (EMBLEM_SIZE, EMBLEM_SIZE), bg_rgb=CREAM)
    out.save(path)
    return out


# --------------------------------------------------------------------------- #

def report(path):
    im = Image.open(path)
    a = np.asarray(im)[..., 3]
    frac = float((a > 127.5).mean())
    print("  %-34s %s %s  alpha>0.5 = %.4f"
          % (os.path.basename(path), "x".join(map(str, im.size)), im.mode, frac))
    return frac


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    t0 = time.time()
    sw = os.path.join(OUT_DIR, "swirl.png")
    fa = os.path.join(OUT_DIR, "fascia.png")
    em = os.path.join(OUT_DIR, "emblem.png")

    make_swirl(sw)
    make_fascia(fa)
    make_emblem(em)

    print("\n=== verification ===")
    size, mode, frac = verify_swirl(sw)
    print("  swirl.png                          %dx%d %s  alpha>0.5 = %.4f"
          % (size[0], size[1], mode, frac))
    assert size == (SWIRL_SIZE, SWIRL_SIZE) and mode == "RGBA"
    assert SWIRL_INK_RANGE[0] <= frac <= SWIRL_INK_RANGE[1], \
        "swirl ink coverage %.3f outside 25-38%%" % frac
    f2 = report(fa)
    f3 = report(em)
    im = Image.open(fa)
    assert im.size == (FASCIA_W, FASCIA_H) and im.mode == "RGBA"
    im = Image.open(em)
    assert im.size == (EMBLEM_SIZE, EMBLEM_SIZE) and im.mode == "RGBA"
    print("\nall textures written to %s in %.1fs" % (OUT_DIR, time.time() - t0))
    return frac, f2, f3


if __name__ == "__main__":
    main()
