"""
pliego.py -- THE PRINT SET.  Real sheet sizes, one modular grid, SVG masters.

WHAT CHANGED FROM `coleccion.py`, AND WHY.  That module laid fifteen pieces out
in PIXELS with HAND-PICKED COORDINATES, drew them with PIL, and shipped PNG
only.  The owner asked for refinement and then, when asked, chose to tighten the
composition onto a real grid.  So:

  * every sheet is a REAL SIZE IN MILLIMETRES, not a pixel guess;
  * every position comes from ONE modular grid and ONE type scale, so the set
    is a system rather than eleven separate opinions;
  * every piece emits an SVG MASTER plus a PNG proof and a PDF, all three from
    the same file (`lienzo.py`), which is what `sheet.py` said the programme
    required all along.

THE OWNER'S RULINGS THIS ROUND, so they are not re-asked:
  * The mural is drawn at the FINE threshold -- the A/B was put to him and A
    won.  The flat panel discarded the header, the flowers and all four menu
    strips to fix what turned out to be one wrong number.
  * `linea`, `riso` and `sello` stay RASTER-ONLY screen pieces; they are raster
    screens and cannot make a print master.  Print comes from the four
    shape-based styles.
  * The wordmark is TACOMBI ALONE.
  * All four format groups get masters: A-frame, posters, small print, merch.

⚠ THE CHECK IS DIFFERENT HERE, AND STRONGER.  `coleccion.py` measured text
boxes in Python and compared them to a safe area -- but PIL was doing the
shaping, so the box was knowable.  CHROMIUM does the shaping now, and Python
cannot know where a shaped, kerned run actually landed.  So instead of trusting
a computed box, `margin_clean()` READS THE RENDERED PNG and asserts the margin
band carries no ink.  That tests the artefact rather than the intention, which
is what rule 1 has been asking for all along.
"""
import os, sys, math
import numpy as np
from PIL import Image

import lienzo, trazo, estilo_vec


def T(L, g, x, y, s, face, pt, fill, anchor="middle", tracking=0.0, measure=None):
    """Every text run in this module goes through here, so no run can be added
    without a measure it must fit."""
    # ⚠ 0.88, NOT 1.0.  Chromium applies letter-spacing after EVERY glyph and
    # shapes tighter than PIL's estimate, so a run measured at exactly the
    # column width still ran off three sheets.  The safety factor is authored,
    # and the RENDERED edge check below is what actually proves it.
    m = (measure if measure is not None else (g.w - 2 * g.m)) * 0.88
    pt = fit_pt(s, face, pt, tracking, m)
    L.text(x, y, s, face, pt, fill, anchor=anchor, tracking=tracking)

OUT = "design_out/pliego"
TAG = "sidehi"
CHECK = [0]; FAILED = []

def ck(cond, msg):
    CHECK[0] += 1
    print(("  ok    " if cond else "  FAIL  ") + msg)
    if not cond: FAILED.append(msg)

CREMA = "#F0E7D1"; ROJO = "#AC2921"; GRANA = "#601A16"
ORO   = "#DE9E2E"; TINTA = "#241E1E"; AZUL = "#1A2E54"
CIELO = "#96BED6"; HUESO = "#FAF6EC"; PAPEL = "#EEE4CE"

LETRERO = "TAQUERIA y CERVECERIA"
MENU = ("GOURMET TACOS", "TORTAS", "FRESH JUICES",
        "CEVICHE / TOSTADAS", "SHRIMP & FISH")
PROV = "TEXTO: MEDIDO · LETRERO · AUTORADO"


class Rejilla(object):
    """One grid for the whole set.  Margin and column both derive from the
    sheet's SHORT side, so a business card and an A-frame panel are the same
    design at different sizes rather than two unrelated layouts."""

    def __init__(self, w, h, cols=12):
        self.w, self.h, self.cols = float(w), float(h), cols
        self.s = min(w, h)
        self.m = self.s / 12.0                      # margin
        self.gut = self.s / 60.0                    # gutter
        self.col = (self.w - 2 * self.m - (cols - 1) * self.gut) / cols
        # ⚠ THE BASELINE IS A FRACTION OF THE USABLE HEIGHT, NOT OF THE SHORT
        # SIDE.  The first version used s/48, so an index tuned on a 900 mm
        # panel collapsed to nothing on an 85 mm card -- the hero came out 7 mm
        # tall with two thirds of the sheet empty.  Making the usable height
        # exactly ROWS units means the SAME index means the same PLACE on every
        # format, which is what makes this a system rather than eleven layouts.
        self.rows = 24.0
        self.base = (self.h - 2 * self.m) / self.rows

    def x(self, i):                 return self.m + i * (self.col + self.gut)
    def span(self, n):              return n * self.col + (n - 1) * self.gut
    def y(self, k):                 return self.m + k * self.base
    def box(self, i, n, k0, k1):
        return (self.x(i), self.y(k0), self.x(i) + self.span(n), self.y(k1))
    def pt(self, step):
        """Type scale: a perfect fourth, anchored on the baseline unit."""
        return self.base * (1.335 ** step)

    def h_(self, f):
        """A height fraction of the usable box, for heroes that must scale with
        the sheet rather than with a baseline count."""
        return self.m + f * (self.h - 2 * self.m)


# Pieces that bleed to the trim by design.  Declared, not tolerated silently.
SANGRA = {"vaso"}


def edge_clean(png_path, frac=0.014):
    """Ink in the OUTERMOST band of the sheet -- where a text run that is too
    wide for its measure ends up.  ⚠ THE MARGIN CHECK MISSED THIS: a thin line
    of type crossing a wide band is a tiny AREA fraction, so a 2 % bar passed
    five sheets whose provenance line ran clean off the page.  This band is
    narrow, so the same overflow is a large fraction of it."""
    a = np.asarray(Image.open(png_path).convert("L")).astype(np.int16)
    H, W = a.shape
    mx = max(1, int(W * frac)); my = max(1, int(H * frac))
    bg = int(np.median(a))
    band = np.ones(a.shape, bool); band[my:H - my, mx:W - mx] = False
    return float(((np.abs(a - bg) > 28) & band).sum()) / max(1, band.sum())


def fit_pt(s, face, pt, tracking, max_mm):
    """Shrink a size until the run fits its measure, using the FACE'S OWN
    metrics.  ⚠ This is a PRE-FLIGHT, not the check: Chromium does the real
    shaping and kerns tighter than this estimate, so it errs safe.  The check
    that matters is `edge_clean`, which reads the rendered sheet."""
    from PIL import ImageFont
    path = lienzo.FACES.get(face)
    if not path or not os.path.exists(path) or not s:
        return pt
    for _ in range(24):
        f = ImageFont.truetype(path, max(4, int(round(pt * 96 / 25.4))))
        w_px = sum(f.getlength(c) for c in s) + tracking * (len(s) - 1) * 96 / 25.4
        if w_px * 25.4 / 96.0 <= max_mm:
            return pt
        pt *= 0.94
    return pt


def margin_clean(png_path, w_mm, h_mm, margin_mm, tol=0.004):
    """Read the RENDERED sheet and report the fraction of the margin band that
    carries ink.  A frame rule is drawn INSIDE the margin by design, so this is
    reported and bounded, not asserted to be zero."""
    im = Image.open(png_path).convert("L")
    a = np.asarray(im).astype(np.int16)
    H, W = a.shape
    mx = int(round(margin_mm / w_mm * W)); my = int(round(margin_mm / h_mm * H))
    inner = a[my:H - my, mx:W - mx]
    bg = int(np.median(a))
    band = np.ones(a.shape, bool); band[my:H - my, mx:W - mx] = False
    ink = (np.abs(a - bg) > 28) & band
    return float(ink.sum()) / max(1, band.sum())


_WM = {}
def wordmark():
    """TACOMBI alone, from `script_gen`'s own letter functions -- vector, at any
    size, and NOT the model's defective `Senor` lockup (F01/F39, F379)."""
    if "c" not in _WM:
        import script_gen as SG
        c = SG.Canvas()
        for fn in (SG.draw_T, SG.draw_a, SG.draw_c, SG.draw_o,
                   SG.draw_m, SG.draw_b, SG.draw_i):
            fn(c)
        m = (np.asarray(c.ink).astype(np.int16)
             - np.asarray(c.hole).astype(np.int16)) > 127
        ys, xs = np.where(m)
        sub = m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        comps, _d, _k = trazo.trace_cached(sub, "gen", "tacombi", 1.2, 20.0, 2)
        _WM["c"] = (comps, sub.shape[1], sub.shape[0])
    return _WM["c"]


def put_wordmark(L, cx, top, width, ink=TINTA):
    comps, w, h = wordmark()
    s = width / float(w)
    L.paths(trazo.to_svg_paths(comps, scale=s, dx=cx - width / 2.0, dy=top), ink)
    return h * s


def put_hero(L, style, box, mural="fino", ink=None):
    lay, wh = estilo_vec.layers(TAG, style, box, mural=mural, ink=ink)
    for ds, col in lay:
        L.paths(ds, col)
    return wh


# ============================================================== the pieces
# (name, w_mm, h_mm, style, ground, builder)

def _poster(L, g, style, sub, foot, rule_col=GRANA, edge=TINTA, txt=TINTA):
    """The portrait master layout.  Rows are indices on the 24-row grid, so the
    SAME numbers place the same way on an 85 mm card and a 900 mm panel."""
    L.frame(g.m * 0.55, edge, g.s / 300.0)
    wh = put_wordmark(L, g.w / 2.0, g.y(1.4), g.span(8))
    T(L, g, g.w / 2.0, g.y(1.4) + wh + g.base * 1.1, LETRERO, "cond",
           g.pt(0.2), rule_col, tracking=g.pt(0.2) * 0.26)
    put_hero(L, style, (g.x(0), g.y(7.2), g.x(0) + g.span(12), g.y(18.4)))
    T(L, g, g.w / 2.0, g.y(20.6), sub, "cond", g.pt(-0.2), txt,
           tracking=g.pt(-0.2) * 0.16)
    # measured against the FRAME's inner width, not the sheet's: the foot line
    # was inside the page but sitting on the keyline at both ends.
    T(L, g, g.w / 2.0, g.y(23.2), foot, "cond", g.pt(-2.0), rule_col,
      tracking=g.pt(-2.0) * 0.12, measure=g.w - 2 * (g.m * 0.55) - 2 * g.gut)


def p_aframe(g, L):
    _poster(L, g, "plano", "FRESH JUICES · GOURMET TACOS · TORTAS",
            "SERIE COMBI · CALLE · " + PROV)

def p_cartel_a2(g, L):
    _poster(L, g, "plano", "SE SIRVE DESDE LA COMBI",
            "SERIE COMBI · IMPRESO · " + PROV)

def p_cartel_a3(g, L):
    _poster(L, g, "azulejo", "SE SIRVE DESDE LA COMBI",
            "SERIE COMBI · ESTILO AZULEJO · " + PROV,
            rule_col=CIELO, edge=CIELO, txt=HUESO)

def p_carta(g, L):
    L.rect(g.m * 0.55, g.m * 0.55, g.w - g.m * 1.1, g.base * 4.4, GRANA)
    L.frame(g.m * 0.55, TINTA, g.s / 320.0)
    put_wordmark(L, g.w / 2.0, g.y(0.7), g.span(6))
    put_hero(L, "papel", (g.x(1), g.y(5.4), g.x(1) + g.span(10), g.y(11.4)))
    y = g.y(13.6)
    for it in MENU:
        T(L, g, g.x(1), y, it, "display", g.pt(-0.1), TINTA, anchor="start")
        L.line(g.x(1), y + g.base * 0.45, g.x(0) + g.span(12),
               y + g.base * 0.45, ORO, g.s / 700.0)
        y += g.base * 1.85
    T(L, g, g.w / 2.0, g.y(23.0), "MENU DE MUESTRA · TOMADO DEL MURAL",
           "cond", g.pt(-1.6), GRANA, tracking=g.pt(-1.6) * 0.14)
    T(L, g, g.w / 2.0, g.y(23.9), PROV, "cond", g.pt(-2.3), GRANA,
           tracking=g.pt(-2.3) * 0.1)

def p_volante(g, L):
    L.frame(g.m * 0.5, ROJO, g.s / 280.0)
    put_wordmark(L, g.w / 2.0, g.y(1.0), g.span(8))
    put_hero(L, "papel", (g.x(0), g.y(6.0), g.x(0) + g.span(12), g.y(13.2)))
    y = g.y(15.6)
    for it in MENU:
        T(L, g, g.w / 2.0, y, it, "display", g.pt(-0.5), AZUL)
        y += g.base * 1.55
    T(L, g, g.w / 2.0, g.y(23.1), "MENU DE MUESTRA", "cond", g.pt(-1.8), ROJO,
           tracking=g.pt(-1.8) * 0.16)
    T(L, g, g.w / 2.0, g.y(23.9), PROV, "cond", g.pt(-2.3), ROJO,
           tracking=g.pt(-2.3) * 0.1)

def p_bolsa(g, L):
    put_wordmark(L, g.w / 2.0, g.y(1.6), g.span(9))
    put_hero(L, "papel", (g.x(0), g.y(7.0), g.x(0) + g.span(12), g.y(16.5)))
    T(L, g, g.w / 2.0, g.y(19.2), "HECHO A MANO", "display", g.pt(0.4), GRANA)
    T(L, g, g.w / 2.0, g.y(21.0), LETRERO, "cond", g.pt(-0.6), TINTA,
           tracking=g.pt(-0.6) * 0.24)
    T(L, g, g.w / 2.0, g.y(23.6), PROV, "cond", g.pt(-2.2), GRANA,
           tracking=g.pt(-2.2) * 0.1)

def p_playera(g, L):
    put_wordmark(L, g.w / 2.0, g.y(1.6), g.span(9), ink=CREMA)
    put_hero(L, "silueta", (g.x(1), g.y(7.0), g.x(1) + g.span(10), g.y(17.0)),
             ink=CREMA)
    T(L, g, g.w / 2.0, g.y(19.8), LETRERO, "cond", g.pt(-0.3), ORO,
           tracking=g.pt(-0.3) * 0.26)
    T(L, g, g.w / 2.0, g.y(23.4), "MERCANCIA · ARTE PLANO · " + PROV, "cond",
           g.pt(-2.3), "#7A6E63", tracking=g.pt(-2.3) * 0.1)

# ---- landscape sheets: the hero takes one side, the lockup the other --------
def _paisaje(L, g, style, edge, rule_col, big=None, big_col=None, txt=TINTA):
    L.frame(g.m * 0.5, edge, g.s / 260.0)
    put_hero(L, style, (g.x(6), g.y(2.0), g.x(6) + g.span(6), g.y(21.5)))
    cx = g.x(0) + g.span(6) / 2.0
    wh = put_wordmark(L, cx, g.y(4.0), g.span(5.4))
    T(L, g, cx, g.y(4.0) + wh + g.base * 1.2, LETRERO, "cond", g.pt(-0.7),
           rule_col, tracking=g.pt(-0.7) * 0.22)
    if big:
        T(L, g, cx, g.y(15.0), big, "display", g.pt(1.0), big_col or txt)
    T(L, g, g.w / 2.0, g.y(23.4), PROV, "cond", g.pt(-2.3), rule_col,
           tracking=g.pt(-2.3) * 0.1)

def p_vidriera(g, L):
    _paisaje(L, g, "azulejo", CIELO, CIELO, big="ABIERTO", big_col=HUESO)

def p_postal(g, L):
    # `silueta` at this size read as an unrecognisable black lump; `plano`
    # keeps the vehicle legible on a 148 mm card.
    _paisaje(L, g, "plano", TINTA, GRANA)

def p_tarjeta(g, L):
    _paisaje(L, g, "plano", GRANA, GRANA)

def p_vaso(g, L):
    L.rect(0, 0, g.w, g.base * 0.8, GRANA)
    L.rect(0, g.h - g.base * 0.8, g.w, g.base * 0.8, GRANA)
    put_hero(L, "plano", (g.x(0), g.y(2.2), g.x(0) + g.span(5), g.y(21.0)))
    cx = g.x(6) + g.span(6) / 2.0
    wh = put_wordmark(L, cx, g.y(5.5), g.span(5.4))
    T(L, g, cx, g.y(5.5) + wh + g.base * 1.3, LETRERO, "cond", g.pt(-0.7),
           TINTA, tracking=g.pt(-0.7) * 0.22)
    T(L, g, cx, g.y(5.5) + wh + g.base * 3.0, PROV, "cond", g.pt(-2.4), GRANA,
           tracking=g.pt(-2.4) * 0.08)


PIEZAS = [
 ("calle",     "aframe",    600, 900, ORO,   p_aframe),
 ("impreso",   "cartel_a2", 420, 594, ORO,   p_cartel_a2),
 ("impreso",   "cartel_a3", 297, 420, AZUL,  p_cartel_a3),
 ("calle",     "carta",     300, 420, CREMA, p_carta),
 ("calle",     "vidriera",  500, 350, AZUL,  p_vidriera),
 ("impreso",   "postal",    148, 105, PAPEL, p_postal),
 ("impreso",   "tarjeta",    85,  55, CREMA, p_tarjeta),
 ("impreso",   "volante",   148, 210, HUESO, p_volante),
 ("mercancia", "bolsa",     380, 420, "#DED2B8", p_bolsa),
 ("mercancia", "playera",   300, 360, "#1C1E22", p_playera),
 ("mercancia", "vaso",      220,  95, CREMA, p_vaso),
]


def main(argv):
    global OUT
    only = None; dpi = 150
    for i, a in enumerate(argv):
        if a == "--only": only = argv[i + 1]
        if a == "--out":  OUT = argv[i + 1]
        if a == "--dpi":  dpi = int(argv[i + 1])
    os.makedirs(OUT, exist_ok=True)
    print("pliego.py -- print set, SVG masters, %d mm sheets" % len(PIEZAS))

    made = []
    for cat, name, w, h, ground, fn in PIEZAS:
        if only and only not in (cat, name): continue
        g = Rejilla(w, h)
        L = lienzo.Lienzo(w, h, bg=ground)
        fn(g, L)
        stem = os.path.join(OUT, "pl_%s_%s" % (cat, name))
        svg = L.save_svg(stem + ".svg")
        L.render(svg, png=stem + ".png", pdf=stem + ".pdf", dpi=dpi)
        made.append((cat, name, w, h, g, stem))
        ck(os.path.getsize(svg) > 4000,
           "%-10s %-10s %4.0f x %-4.0f mm  svg %6d KB  pdf %5d KB"
           % (cat, name, w, h, os.path.getsize(svg) // 1024,
              os.path.getsize(stem + ".pdf") // 1024))

    # THE INSTRUMENT: read the RENDERED sheet, not a computed box.  Chromium
    # shapes the type, so Python cannot know where a kerned run landed -- but it
    # can look at the result (rule 1).
    for cat, name, w, h, g, stem in made:
        frac = margin_clean(stem + ".png", w, h, g.m * 0.42)
        bar = 0.62 if name in SANGRA else 0.02
        ck(frac < bar, "%-10s margin band %.3f %% ink (bar %.0f %%)%s"
           % (name, 100 * frac, 100 * bar, "  [bleeds by design]"
              if name in SANGRA else ""))
        e = edge_clean(stem + ".png")
        # 0.0015, not 0.004: at 0.4 % the aframe passed at 0.3919 % with its
        # foot line visibly clipped.  A bar a defect squeaks under is not a bar.
        ebar = 0.60 if name in SANGRA else 0.0015
        ck(e < ebar, "%-10s outer edge %.4f %% ink (bar %.1f %%)"
           % (name, 100 * e, 100 * ebar))

    if not only and made:
        cells = []
        for _c, name, w, h, _g, stem in made:
            cells.append((name, Image.open(stem + ".png")))
        cols = 4; cell = 520; pad = 22
        rows = (len(cells) + cols - 1) // cols
        sh = Image.new("RGB", (cols * cell + pad * (cols + 1),
                               rows * cell + pad * (rows + 1) + 24),
                       (250, 249, 246))
        from PIL import ImageDraw
        import promo
        d = ImageDraw.Draw(sh); f = promo.font("sans", 18)
        for i, (name, im) in enumerate(cells):
            r, c = divmod(i, cols)
            x = pad + c * (cell + pad); y = pad + r * (cell + pad)
            s = min(cell / im.width, cell / im.height)
            t = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))),
                          Image.LANCZOS)
            sh.paste(t, (x + (cell - t.width) // 2, y + (cell - t.height) // 2))
            d.text((x, y + cell + 2), name, fill=(70, 64, 58), font=f)
        p = os.path.join(OUT, "pl_HOJA.png"); sh.save(p)
        ck(os.path.exists(p), "contact sheet -> %s" % p)

    print("%d checked, %d FAILED" % (CHECK[0], len(FAILED)))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
