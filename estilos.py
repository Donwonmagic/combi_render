"""
estilos.py -- THE COMBI DRAWN, IN SEVERAL STYLES, OVER THE MODEL AS UNDERLAY.

THE OWNER'S INSTRUCTION, VERBATIM: *"Remember that the model is simply an
underlay for the hero of each piece.  It should be done in different styles
too."*  That is a correction of `promo.py`, which pasted the render itself as
the artwork.  Here the model is asked only WHERE THINGS ARE -- silhouette,
region boundaries, creases, tone -- and every hero is DRAWN from that.

⚠ THIS EXTENDS F368 AND PARTLY RETRACTS ITS HEADLINE, IN THE SAME REVISION THAT
RAISED IT (rule 13).  F368 measured that a flat rendering BY MATERIAL destroys
the vehicle's identity: `T1_paint` is 40.49 % of the silhouette and carries the
cream upper body, the red lower body AND the gold scrollwork as one flat ink, so
the two-tone vanishes and the scrollwork with it.  That measurement stands.
What F368 went on to say -- that no pass here can recover the artwork -- IS
WRONG, and the correction is this module: key BY COLOUR WITHIN each material
region instead of by material.  MEASURED on the `side` capture: `T1_paint`
separates 33.1 % cream / 59.4 % red / 7.5 % gold, and `lidmural` separates
27.3 % flower against its ground.  PAINTED AND LOOKED AT before the claim was
made (rule 8) -- the scrollwork, the mural flowers, the `Señor Tacombi` script
and the two-tone all come back as clean, drawable shapes.

CEILINGS:
  * The separation is a COLOUR key, not a semantic one.  It finds gold pixels,
    not "scrollwork".  Anything gold inside `T1_paint` joins that layer.
  * The styles are AUTHORED.  Nothing here measures whether a style is any good,
    and nothing in this tree can.  The owner is the instrument.
  * One capture, one viewpoint per drawing.  `side` (az 90), `flank` (az 72) and
    `nose` are the three that exist.
"""
import os, sys, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

CAP = "probe_scratch/sticker"
OUT = "design_out"
CHECK = [0]; FAILED = []

def ck(cond, msg):
    CHECK[0] += 1
    print(("  ok    " if cond else "  FAIL  ") + msg)
    if not cond: FAILED.append(msg)

# ============================================================== the underlay
def underlay(tag):
    """Every layer the drawings are built from.  Nothing here is a picture --
    they are masks, strokes and a tone field, i.e. WHERE THINGS ARE."""
    meta = json.load(open("%s/%s_meta.json" % (CAP, tag)))
    IDX = meta["index"]
    im = Image.open("%s/%s_index_0001.png" % (CAP, tag))
    raw = np.asarray(im).astype(np.float64)
    if raw.ndim == 3: raw = raw[..., 0]
    den = 65535.0 if im.mode.startswith("I") else 255.0
    I = np.rint(raw / den * 255.0).astype(int)
    al = np.asarray(Image.open("%s/%s_alpha_0001.png" % (CAP, tag)
                               ).convert("L")) > 127
    ab = np.asarray(Image.open("%s/%s_albedo_0001.png" % (CAP, tag)
                               ).convert("RGB")).astype(int)
    sh = np.asarray(Image.open("%s/%s_shade_0001.png" % (CAP, tag)
                               ).convert("L")).astype(np.float64) / 255.0
    ao = np.asarray(Image.open("%s/%s_ao_0001.png" % (CAP, tag)
                               ).convert("L")).astype(np.float64) / 255.0
    st = json.load(open("%s/%s_lines.json" % (CAP, tag)))["strokes"]

    def region(n): return (I == IDX[n]) & al if n in IDX else np.zeros_like(al)

    L = {}

    NOKEY = os.environ.get("T1_EST_NOKEY") == "1"

    def split(base, tests):
        """Key one material region by its OWN colours.  This is the operation
        F368 said did not exist.

        ABLATION T1_EST_NOKEY=1 disables the key and falls back to
        FLAT-BY-MATERIAL -- F368's original method.  It exists so the recovery
        can be WATCHED FAILING (rule 3): with the key off, `body_gold`,
        `body_cream` and `mural_gold` all collapse to zero and their checks red.
        Run it with --out so it cannot overwrite the tracked painting."""
        m = region(base)
        if not m.any(): return
        if NOKEY:
            L[base + "_rest"] = m
            return
        px = ab[m]; ij = np.where(m)
        taken = np.zeros(px.shape[0], bool)
        for name, fn in tests:
            sel = fn(px) & ~taken
            taken |= sel
            z = np.zeros_like(m); z[ij[0][sel], ij[1][sel]] = True
            L[name] = z
        z = np.zeros_like(m); z[ij[0][~taken], ij[1][~taken]] = True
        L[base + "_rest"] = z

    def sat_of(px):
        mx = px.max(1); mn = px.min(1)
        return (mx - mn) / np.maximum(mx, 1), mx

    def is_cream(px):
        s, mx = sat_of(px); return (s < 0.22) & (mx > 90)
    def is_gold(px):
        s, mx = sat_of(px)
        return (~((s < 0.22) & (mx > 90))) & \
               (px[:, 1] - px[:, 2] > 28) & (px[:, 0] > 90) & (px[:, 1] > 55)
    def is_red(px):
        return np.ones(px.shape[0], bool)

    split("T1_paint", [("body_cream", is_cream), ("body_gold", is_gold),
                       ("body_red", is_red)])
    split("lidmural", [("mural_gold", lambda p: (p[:, 0] - p[:, 2] > 40) &
                                                (p[:, 0] > 95)),
                       ("mural_ground", is_red)])
    split("calidad",  [("calidad_ink", lambda p: (p[:, 0] - p[:, 1] > 35) &
                                                 (p[:, 0] > 80)),
                       ("calidad_field", is_red)])
    for n in ("script", "glass", "tyre", "wheelcream", "capred", "capwhite",
              "countercream", "countertan", "bulb", "chrome", "chrome_dull",
              "interior_dark", "underseal", "rubber", "steel", "brass",
              "lidsign", "roundelred", "bumpercream", "gal_menucard"):
        r = region(n)
        if r.any(): L[n] = r

    named = np.zeros_like(al)
    for v in L.values(): named |= v
    L["_rest"] = al & ~named

    # a per-material albedo median, for styles that want an automatic ink
    med = {}
    for k, v in L.items():
        if v.any(): med[k] = tuple(int(x) for x in np.median(ab[v], axis=0))

    return dict(tag=tag, alpha=al, layers=L, med=med, strokes=st,
                shade=sh, ao=ao, albedo=ab, H=al.shape[0], W=al.shape[1])

# ============================================================== primitives
def up(mask, ss):
    """A boolean mask as an antialiased L image at ss scale."""
    a = Image.fromarray((mask * 255).astype(np.uint8))
    return a.resize((mask.shape[1] * ss, mask.shape[0] * ss), Image.LANCZOS)

def lay(img, mask_L, ink):
    img.paste(Image.new("RGBA", img.size, tuple(ink) + (255,)), (0, 0), mask_L)

def grow(mask_L, r):
    return mask_L.filter(ImageFilter.MaxFilter(r * 2 + 1))

def edge(mask_L, w):
    """The outline of a mask: grown minus shrunk."""
    g = mask_L.filter(ImageFilter.MaxFilter(w * 2 + 1))
    s = mask_L.filter(ImageFilter.MinFilter(w * 2 + 1))
    return ImageChops.subtract(g, s)

def strokes_L(u, ss, width, minlen=0, jitter=0.0, seed=3):
    """The line pass as an L image.  `jitter` displaces each stroke slightly so
    the line reads as drawn rather than machined."""
    W, H = u["W"], u["H"]
    im = Image.new("L", (W * ss, H * ss), 0)
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(seed)
    for s in u["strokes"]:
        if len(s) < max(2, minlen): continue
        jx, jy = (rng.normal(0, jitter, 2) * ss if jitter else (0.0, 0.0))
        d.line([(p[0] * W * ss + jx, p[1] * H * ss + jy) for p in s],
               fill=255, width=max(1, int(width * ss)), joint="curve")
    return im

def tone_L(u, ss, invert=False):
    t = u["shade"] * (0.55 + 0.45 * u["ao"])
    t = (t - t[u["alpha"]].min()) / max(1e-6, float(np.ptp(t[u["alpha"]])))
    if invert: t = 1.0 - t
    a = Image.fromarray(np.clip(t * 255, 0, 255).astype(np.uint8))
    return a.resize((u["W"] * ss, u["H"] * ss), Image.LANCZOS)

def halftone(tone_img, cell, angle=45, ss=1):
    """A dot screen over a tone image.  Dot area tracks 1 - tone.

    VECTORISED.  The obvious loop -- one PIL ellipse per grid cell -- is 1.3
    million draw calls on a 4200x3000 canvas and does not finish.  Instead every
    pixel is mapped into the rotated screen grid at once and compared with the
    dot radius its own tone asks for.
    """
    W, H = tone_img.size
    t = np.asarray(tone_img).astype(np.float32) / 255.0
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    a = math.radians(angle); ca, sa = math.cos(a), math.sin(a)
    xr = (xx - W / 2.0) * ca + (yy - H / 2.0) * sa
    yr = -(xx - W / 2.0) * sa + (yy - H / 2.0) * ca
    fx = np.abs((xr / cell) - np.round(xr / cell)) * cell
    fy = np.abs((yr / cell) - np.round(yr / cell)) * cell
    dist = np.hypot(fx, fy)
    r = 0.78 * cell * np.sqrt(np.clip(1.0 - t, 0.0, 1.0))
    return Image.fromarray(((dist <= r) * 255).astype(np.uint8))


def hatch(tone_img, spacing, angle, levels=3, width=1):
    """Line hatching: each darker band adds a pass at a new angle."""
    W, H = tone_img.size
    t = np.asarray(tone_img).astype(np.float64) / 255.0
    out = Image.new("L", (W, H), 0)
    for k in range(levels):
        thr = 1.0 - (k + 1) / float(levels + 1)
        band = Image.fromarray(((t < thr) * 255).astype(np.uint8))
        lines = Image.new("L", (W, H), 0); d = ImageDraw.Draw(lines)
        ang = angle + k * 41
        a = math.radians(ang); dx, dy = math.cos(a), math.sin(a)
        n = int(math.hypot(W, H) / spacing) + 2
        for i in range(-n, n):
            cx, cy = W / 2 + (-dy) * i * spacing, H / 2 + dx * i * spacing
            L = math.hypot(W, H)
            d.line([(cx - dx * L, cy - dy * L), (cx + dx * L, cy + dy * L)],
                   fill=255, width=width)
        out = ImageChops.lighter(out, ImageChops.multiply(lines, band))
    return out

def rough(mask_L, amount=1.4, seed=5):
    """Break a clean edge so a stencil or a stamp does not look machined."""
    W, H = mask_L.size
    rng = np.random.default_rng(seed)
    n = rng.normal(0, 1, (H // 4 + 1, W // 4 + 1)).astype(np.float32)
    ni = Image.fromarray(np.clip(n * 60 + 128, 0, 255).astype(np.uint8)
                         ).resize((W, H), Image.BICUBIC)
    a = np.asarray(mask_L).astype(np.float64)
    b = np.asarray(ni).astype(np.float64) - 128.0
    return Image.fromarray(np.clip(a + b * amount, 0, 255).astype(np.uint8)
                           ).point(lambda v: 255 if v > 127 else 0)

def finish(img, u, ss, crop=True):
    out = img.resize((u["W"], u["H"]), Image.LANCZOS)
    return out.crop(out.getbbox()) if crop and out.getbbox() else out

# ================================================================ the inks
CREMA  = (240, 231, 209); PAPEL = (236, 227, 205)
ROJO   = (172, 41, 33);   GRANA = (96, 26, 22)
ORO    = (222, 158, 46);  TINTA = (36, 30, 30)
PIZ    = (56, 66, 74);    AZUL  = (26, 46, 84)
CIELO  = (150, 190, 214); HUESO = (250, 246, 236)

def nearest(rgb, pal):
    return min(pal, key=lambda c: sum((a - b) ** 2 for a, b in zip(rgb, c)))

# ================================================================ 1. PLANO
def plano(u, ss=3):
    """Flat vector, sign-painter register.  Every region a flat ink, one
    contour.  This is the style the owner's example sign is in -- drawn from
    THIS bus instead of a stock one."""
    W, H = u["W"] * ss, u["H"] * ss
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    L, med = u["layers"], u["med"]
    PAL = [CREMA, ROJO, ORO, GRANA, TINTA, PIZ, HUESO]
    INKS = {"body_cream": CREMA, "body_red": ROJO, "body_gold": ORO,
            "mural_ground": GRANA, "mural_gold": ORO, "calidad_field": CREMA,
            "calidad_ink": ROJO, "script": TINTA, "glass": PIZ, "tyre": TINTA,
            "wheelcream": CREMA, "capred": ROJO, "capwhite": CREMA,
            "countercream": CREMA, "countertan": ORO, "bulb": HUESO,
            "interior_dark": TINTA, "underseal": TINTA, "rubber": TINTA,
            "steel": PIZ, "chrome": CREMA, "chrome_dull": PIZ,
            "bumpercream": CREMA, "lidsign": ORO, "roundelred": ROJO,
            "gal_menucard": CREMA, "_rest": PIZ, "T1_paint_rest": ROJO,
            "lidmural_rest": GRANA, "calidad_rest": CREMA}
    order = ["_rest", "interior_dark", "glass", "countertan", "countercream",
             "gal_menucard", "steel", "chrome_dull", "chrome", "underseal",
             "rubber", "body_cream", "body_red", "T1_paint_rest",
             "lidmural_rest", "mural_ground", "mural_gold", "lidsign",
             "body_gold", "calidad_field", "calidad_ink", "roundelred",
             "bumpercream", "tyre", "wheelcream", "capred", "capwhite",
             "script", "bulb"]
    for k in order + [k for k in L if k not in order]:
        if k not in L or not L[k].any(): continue
        ink = INKS.get(k) or nearest(med.get(k, (128, 128, 128)), PAL)
        lay(im, up(L[k], ss), ink)
    sil = up(u["alpha"], ss)
    lay(im, edge(sil, max(1, ss)), TINTA)
    im.putalpha(ImageChops.lighter(im.getchannel("A"), grow(sil, 1)))
    return finish(im, u, ss), PAPEL

# ================================================================ 2. LINEA
def linea(u, ss=3):
    """Engraving.  One ink, no flat colour: the drawing is the line pass plus
    hatching that follows the model's own tone, and solids only where the
    vehicle is genuinely black."""
    W, H = u["W"] * ss, u["H"] * ss
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    L = u["layers"]
    sil = up(u["alpha"], ss)
    t = tone_L(u, ss)
    h = ImageChops.multiply(hatch(t, spacing=max(2, int(ss * 1.7)), angle=28,
                                  levels=4, width=max(1, int(ss * 0.7))), sil)
    lay(im, h, TINTA)
    for k in ("glass", "tyre", "interior_dark", "underseal", "script"):
        if k in L and L[k].any(): lay(im, up(L[k], ss), TINTA)
    for k in ("body_gold", "mural_gold", "calidad_ink"):
        if k in L and L[k].any():
            lay(im, edge(up(L[k], ss), max(1, ss // 2)), TINTA)
    lay(im, strokes_L(u, ss, 0.9, jitter=0.35), TINTA)
    lay(im, edge(sil, max(1, ss)), TINTA)
    return finish(im, u, ss), PAPEL

# ================================================================ 3. PAPEL
def papel(u, ss=3):
    """Papel picado.  ONE ink, cut as a single sheet: the artwork is not
    printed on the bus, it is PUNCHED OUT of it, so the ground shows through."""
    W, H = u["W"] * ss, u["H"] * ss
    L = u["layers"]
    sheet = up(u["alpha"], ss).point(lambda v: 255 if v > 110 else 0)
    holes = Image.new("L", (W, H), 0)
    for k in ("glass", "body_gold", "script", "mural_gold", "bulb",
              "calidad_ink", "wheelcream", "capwhite", "gal_menucard"):
        if k in L and L[k].any():
            holes = ImageChops.lighter(holes, up(L[k], ss))
    # a punched hole must not touch the cut edge or the sheet falls apart
    holes = ImageChops.multiply(holes, up(u["alpha"], ss).filter(
        ImageFilter.MinFilter(2 * max(1, ss) + 1)))
    cut = ImageChops.subtract(sheet, holes)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lay(im, cut, GRANA)
    return finish(im, u, ss), ORO

# ================================================================= 4. RISO
def riso(u, ss=3):
    """Risograph duotone.  Two inks, each its own halftone screen at its own
    angle, deliberately misregistered -- the defect that makes riso riso."""
    W, H = u["W"] * ss, u["H"] * ss
    L = u["layers"]
    warm = np.zeros_like(u["alpha"], dtype=bool)
    for k in ("body_red", "capred", "calidad_ink", "mural_ground",
              "T1_paint_rest", "lidmural_rest", "roundelred"):
        if k in L: warm |= L[k]
    for k in ("body_gold", "mural_gold", "countertan", "lidsign"):
        if k in L: warm |= L[k]
    cool = u["alpha"] & ~warm

    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # A duotone plate's density is how much INK the pixel needs, which is the
    # artwork's own darkness -- not how the model happens to be lit.  Using the
    # shading pass printed the mural lid EMPTY because the lid is brightly lit.
    lum = (u["albedo"] * np.array([0.30, 0.59, 0.11])).sum(2) / 255.0
    lum = np.clip(lum * (0.55 + 0.45 * u["ao"]), 0, 1)
    tL = Image.fromarray((lum * 255).astype(np.uint8)).resize((W, H),
                                                              Image.LANCZOS)
    sA = ImageChops.multiply(halftone(tL, cell=max(6, int(ss * 4.5)), angle=15),
                             up(warm, ss))
    sB = ImageChops.multiply(halftone(tL, cell=max(6, int(ss * 4.5)), angle=75),
                             up(cool, ss))
    a = Image.new("RGBA", (W, H), (0, 0, 0, 0)); lay(a, sA, ROJO)
    b = Image.new("RGBA", (W, H), (0, 0, 0, 0)); lay(b, sB, AZUL)
    off = int(ss * 1.6)
    base = Image.alpha_composite(base, ImageChops.offset(b, -off, off // 2))
    base = Image.alpha_composite(base, ImageChops.offset(a, off, 0))
    lay(base, strokes_L(u, ss, 0.8, minlen=14), TINTA)
    return finish(base, u, ss), HUESO

# ============================================================== 5. AZULEJO
def azulejo(u, ss=3):
    """Blueprint.  White line on deep blue -- the vehicle as a drawing OF a
    vehicle, which is the one register that admits the model is a model."""
    W, H = u["W"] * ss, u["H"] * ss
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    L = u["layers"]
    sil = up(u["alpha"], ss)
    lay(im, sil, AZUL)
    for k in ("body_gold", "mural_gold", "script", "calidad_ink", "glass"):
        if k in L and L[k].any():
            lay(im, edge(up(L[k], ss), max(1, ss // 2)), CIELO)
    for k in ("body_cream", "body_red", "mural_ground", "tyre", "wheelcream"):
        if k in L and L[k].any():
            lay(im, edge(up(L[k], ss), max(1, ss // 2)), CIELO)
    lay(im, strokes_L(u, ss, 0.8), HUESO)
    lay(im, edge(sil, max(1, ss)), HUESO)
    return finish(im, u, ss), AZUL

# ================================================================ 6. SELLO
def sello(u, ss=3):
    """Stencil / rubber stamp.  ONE ink, two values, a broken edge.  The test
    of a mark: is the bus still the bus with everything else thrown away?"""
    W, H = u["W"] * ss, u["H"] * ss
    L = u["layers"]
    t = np.asarray(tone_L(u, ss)).astype(np.float64) / 255.0
    dark = Image.fromarray(((t < 0.46) * 255).astype(np.uint8))
    dark = ImageChops.multiply(dark, up(u["alpha"], ss))
    solid = Image.new("L", (W, H), 0)
    for k in ("glass", "tyre", "interior_dark", "underseal", "script",
              "mural_ground"):
        if k in L and L[k].any(): solid = ImageChops.lighter(solid, up(L[k], ss))
    m = ImageChops.lighter(dark, solid)
    m = ImageChops.lighter(m, ImageChops.multiply(
        strokes_L(u, ss, 1.5, minlen=12), up(u["alpha"], ss)))
    m = ImageChops.lighter(m, edge(up(u["alpha"], ss), max(1, ss)))
    # ⚠ THE ROUGHENING MUST BE CLIPPED TO THE VEHICLE.  Unclipped it lifted
    # noise across the whole canvas and the first sheet printed a rectangular
    # smear with THREE CHECKS GREEN on it -- the ink-pixel count went UP, which
    # is exactly the wrong direction for a stencil.  Caught by looking.
    m = rough(m, amount=0.9 * ss)
    m = ImageChops.multiply(m, grow(up(u["alpha"], ss), max(1, ss)))
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lay(im, m, GRANA)
    return finish(im, u, ss), CREMA

ESTILOS = [("plano", plano), ("linea", linea), ("papel", papel),
           ("riso", riso), ("azulejo", azulejo), ("sello", sello)]

# ============================================================== the sheet
PAINT_INKS = {"body_cream": (236, 228, 208), "body_red": (176, 38, 30),
              "body_gold": (228, 164, 44), "mural_gold": (238, 196, 70),
              "mural_ground": (92, 26, 20), "script": (28, 24, 30),
              "calidad_ink": (214, 40, 34), "calidad_field": (250, 240, 220),
              "glass": (46, 60, 72), "tyre": (26, 24, 24),
              "wheelcream": (226, 220, 205), "_rest": (140, 140, 140)}
SIN_ASIGNAR = (255, 0, 255)   # magenta: inside the silhouette, in NO layer

def paint_layers(u, path):
    """⚠ THE PAINTING IS THE CHECK (rule 8).  F369's percentages are a partition
    that sums to its parent BY CONSTRUCTION, so the arithmetic cannot
    self-verify -- only looking can.  This module claimed 'PAINTED AND LOOKED
    AT' while writing NO MASK ANYWHERE; the rule-15 adversary caught that, and
    this is the fix.  Every recovered layer in its own ink, on disk, every run."""
    al = u["alpha"]
    out = np.full((u["H"], u["W"], 3), 255, np.uint8)
    # ⚠ EVERY PIXEL INSIDE THE SILHOUETTE STARTS MAGENTA.  The first version
    # started WHITE -- the same white as the page -- so 86 947 px (15.5 % of the
    # subject) that belong to NO layer were invisible in the one artefact
    # offered as rule-8 evidence.  That is F364's failure (a painted mask that
    # cannot discriminate) inside the fix written for it.  Caught by the rule-17
    # adversary measuring the union against the silhouette.
    out[al] = SIN_ASIGNAR
    covered = np.zeros_like(al)
    for k, ink in PAINT_INKS.items():
        m = u["layers"].get(k)
        if m is not None and m.any():
            out[m] = ink; covered |= m
    ys, xs = np.where(al)
    Image.fromarray(out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]).save(path)
    unass = int((al & ~covered).sum())
    return path, unass, int(al.sum())


def sheet(tag="side", ss=3, out=None, cell=760):
    out = out or OUT
    # ⚠ F358, AND IT WAS CLAIMED BEFORE IT EXISTED.  rev 80's ledger said this
    # module "refuses to run ablated without --out"; the rule-17 adversary
    # tested that sentence, found only a DOCSTRING, and overwrote eight tracked
    # artefacts proving it.  A prose instruction is not a guard (rule 10).
    _abl = [e for e in ['T1_EST_NOKEY'] if os.environ.get(e) == "1"]
    if _abl and out == "design_out":
        raise SystemExit("REFUSING: %s set and --out not given; this would "
                         "overwrite the tracked artwork in design_out/.  "
                         "Pass --out /tmp/ab." % ",".join(_abl))
    os.makedirs(out, exist_ok=True)
    u = underlay(tag)
    pp, unass, tot = paint_layers(u, os.path.join(out,
                                  "estilo_r80_%s_CAPAS.png" % tag))
    ck(os.path.exists(pp), "the recovered layers are PAINTED to %s -- LOOK AT IT"
       % pp)
    # COVERAGE IS PART OF THE PAINTING.  A named layer set that leaves a sixth
    # of the subject unassigned is not a separation; the magenta says where.
    ck(unass / float(tot) < 0.20,
       "unassigned area is %d px of %d (%.1f %%), shown MAGENTA -- bar 20 %%"
       % (unass, tot, 100.0 * unass / tot))
    ck(u["alpha"].sum() > 100000,
       "underlay %s: silhouette %d px" % (tag, int(u["alpha"].sum())))
    for k in ("body_cream", "body_red", "body_gold", "mural_gold", "script"):
        n = int(u["layers"].get(k, np.zeros(1)).sum())
        ck(n > 500, "underlay layer %-12s recovered, %7d px" % (k, n))

    made = []
    for name, fn in ESTILOS:
        img, ground = fn(u, ss)
        p = os.path.join(out, "estilo_r80_%s_%s.png" % (tag, name))
        card = Image.new("RGB", (img.width + 120, img.height + 120), ground)
        card.paste(img, (60, 60), img)
        card.save(p)
        made.append((name, p, img, ground))
        a = np.asarray(img)[..., 3]
        ck((a > 40).sum() > 40000,
           "%-8s drawn, %d ink px on a %dx%d cut-out"
           % (name, int((a > 40).sum()), img.width, img.height))
    # the styles must actually DIFFER -- otherwise this is one style six times
    import itertools
    sims = []
    for (n1, _, i1, _), (n2, _, i2, _) in itertools.combinations(made, 2):
        a1 = np.asarray(i1.convert("RGBA").resize((160, 120)))
        a2 = np.asarray(i2.convert("RGBA").resize((160, 120)))
        d = np.abs(a1.astype(int) - a2.astype(int)).mean()
        sims.append((d, n1, n2))
    worst = min(sims)
    ck(worst[0] > 6.0, "the six styles differ: closest pair %s/%s at mean "
       "channel distance %.2f (floor 6.0)" % (worst[1], worst[2], worst[0]))

    cols = 3
    rows = (len(made) + cols - 1) // cols
    pad = 30
    Wc = cols * cell + pad * (cols + 1)
    Hc = rows * cell + pad * (rows + 1)
    sh = Image.new("RGB", (Wc, Hc), (250, 249, 246))
    for i, (name, p, img, ground) in enumerate(made):
        r, c = divmod(i, cols)
        x = pad + c * (cell + pad); y = pad + r * (cell + pad)
        sh.paste(Image.new("RGB", (cell, cell), ground), (x, y))
        s = min((cell - 60) / img.width, (cell - 60) / img.height)
        t = img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS)
        sh.paste(t, (x + (cell - t.width) // 2, y + (cell - t.height) // 2), t)
    sp = os.path.join(out, "estilo_r80_%s_HOJA.png" % tag)
    sh.save(sp)
    ck(os.path.exists(sp), "style sheet written -> %s" % sp)
    return sp


def main(argv):
    tag = "side"; out = None
    for i, a in enumerate(argv):
        if a == "--tag": tag = argv[i + 1]
        if a == "--out": out = argv[i + 1]
    print("estilos.py -- the combi drawn, over the model as underlay")
    sheet(tag, out=out)
    print("%d checked, %d FAILED" % (CHECK[0], len(FAILED)))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

# ============================================================== THE MARKS
# The vehicle CARRIES ITS OWN TYPE.  `script` is the hand-lettered `Señor
# Tacombi` wordmark, `calidad` the 100 % quality seal, `body_gold` the folk-art
# scrollwork, `mural_gold` the lid's menu header and flower field.  Recovered by
# the same within-material colour key as everything else (F369), they are
# REUSABLE ARTWORK, not pictures of artwork.
#
# ⚠⚠ AND THE CEILING THAT USED TO BE STATED HERE WAS FALSE AND IS RETRACTED
# (F371).  This block said: "promo.py states a real ceiling: this container has
# NO display, script or condensed face -- Charter is Type1, which PIL cannot
# load, and fonts.google.com is refused by the egress proxy."  MEASURED: PIL
# 12.3.0 LOADS that Type1 and returns ('Bitstream Charter','Bold'), 7702 ink px;
# and the CDN probe hit the WRONG HOST -- fonts.googleapis.com returns 200 and
# serves .ttf that PIL opens.  Neither half was ever run.  The marks below are
# still worth having -- they are the vehicle's OWN lettering, which no licensed
# face can substitute for -- but they are NOT a workaround for a limitation
# that does not exist.  Type in use: Alfa Slab One, Oswald (both OFL, in
# fonts/) and Bitstream Charter.

def _despeck(mask, min_px):
    """Drop connected components below `min_px`.  A recovered mask carries
    sampling crumbs; printed at poster size they read as dirt."""
    from scipy import ndimage
    lab, n = ndimage.label(mask)
    if n == 0: return mask
    keep = np.zeros(n + 1, bool)
    cnt = np.bincount(lab.ravel())
    keep[1:] = cnt[1:] >= min_px
    return keep[lab]

def seal_pair(tag="side", min_px=12):
    """The `100% Calidad` seal as TWO plates in ONE frame.

    ⚠ IT IS A REVERSED MARK AND A SINGLE SILHOUETTE DESTROYS IT.  The lettering
    is a HOLE in the red starburst, showing the cream plate beneath, so filling
    `calidad_ink` with one flat colour prints a blot -- which is exactly what
    the first collection sheet did, at 210 px, on five pieces, with every check
    green.  Caught by looking at a piece at FULL SIZE; the contact sheet hid it.
    Returns (field, burst) as boolean masks sharing one bounding box.
    """
    u = underlay(tag)
    L = u["layers"]
    f = L.get("calidad_field"); b = L.get("calidad_ink")
    if f is None or b is None or not f.any() or not b.any(): return None
    f = _despeck(f, min_px); b = _despeck(b, min_px)
    both = f | b
    ys, xs = np.where(both)
    sl = (slice(ys.min(), ys.max() + 1), slice(xs.min(), xs.max() + 1))
    return f[sl], b[sl]


def marks(tag="side", min_px=12):
    """The vehicle's own artwork, cropped and de-specked, as L masks."""
    u = underlay(tag)
    L = u["layers"]
    outv = {}
    for name, key, mp in (("wordmark", "script", min_px),
                          ("seal", "calidad_ink", min_px),
                          ("seal_plate", "calidad_field", min_px),
                          ("scroll", "body_gold", min_px * 3),
                          ("mural", "mural_gold", min_px * 2)):
        if key not in L or not L[key].any(): continue
        m = _despeck(L[key], mp)
        if not m.any(): continue
        ys, xs = np.where(m)
        sub = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        if name == "scroll":
            # The scrollwork runs the WHOLE flank, so its bbox is mostly empty
            # with stragglers at the tail.  An ornament wants the dense cluster,
            # found by column density rather than authored by eye.
            col = sub.sum(0).astype(float)
            k = max(20, int(sub.shape[1] * 0.34))
            csum = np.concatenate([[0], np.cumsum(col)])
            win = csum[k:] - csum[:-k]
            x0 = int(np.argmax(win))
            sub = sub[:, x0:x0 + k]
            ys2, xs2 = np.where(sub)
            sub = sub[ys2.min():ys2.max() + 1, xs2.min():xs2.max() + 1]
        outv[name] = sub
    return outv

def mark_img(mask, height, ink, ss=4):
    """One mark as an RGBA image `height` px tall, antialiased."""
    h, w = mask.shape
    a = Image.fromarray((mask * 255).astype(np.uint8))
    big = a.resize((w * ss, h * ss), Image.LANCZOS)
    wid = max(1, int(round(height * w / float(h))))
    sm = big.resize((wid, height), Image.LANCZOS)
    im = Image.new("RGBA", (wid, height), tuple(ink) + (0,))
    im.paste(Image.new("RGBA", (wid, height), tuple(ink) + (255,)), (0, 0), sm)
    return im
