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
    pt, k = fit_pt(s, face, pt, tracking, m)
    if pt < MIN_TIPO_MM:
        k = k * MIN_TIPO_MM / pt
        pt = MIN_TIPO_MM
        w_at_floor, _ = fit_pt(s, face, pt, tracking * k, m)
        if w_at_floor < pt - 1e-9:
            DEMASIADO.append((PIEZA[0], s[:34], round(m, 1)))
    # tracking follows the size it was chosen for -- see fit_pt
    L.text(x, y, s, face, pt, fill, anchor=anchor, tracking=tracking * k)
    FIT.append((PIEZA[0], s[:28], round(k, 4)))
    # the run's own box, in mm, from the FACE'S metrics -- so occlusion can be
    # tested against the geometry rather than guessed at from pixels
    box = None
    fp = lienzo.FACES.get(face)
    if fp and os.path.exists(fp) and s:
        from PIL import ImageFont
        u = 256
        ff = ImageFont.truetype(fp, u)
        adv = sum(ff.getlength(c) for c in s) * pt / u
        wmm = adv + tracking * k * (len(s) - 1)
        asc, desc = ff.getmetrics()
        x0 = (x - wmm / 2.0 if anchor == "middle"
              else x - wmm if anchor == "end" else x)
        box = (x0, y - asc * pt / u, x0 + wmm, y + desc * pt / u)
    TEXTS.append({"piece": PIEZA[0], "s": s, "x": x, "y": y, "pt": pt,
                  "face": face, "fill": fill, "anchor": anchor,
                  "tracking": tracking * k, "box": box,
                  "order": len(L.body) - 1})

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

# ⚠ GROUNDS ARE NOT THE SAME VALUES AS THE INKS, AND THEY USED TO BE.  Seven of
# eleven sheets painted artwork in EXACTLY the page colour -- `body_gold`,
# `mural_gold`, `lidsign` and `countertan` are all ORO, and four sheets used ORO
# as the ground; `body_cream`, `chrome`, `wheelcream`, `capwhite` and four more
# are all CREMA, and three sheets used CREMA.  7.6 % of the A-frame's drawing
# was painted in its own background.  These grounds are chosen to CLEAR the
# palette, and `contrast()` now proves it every build.
F_ORO   = "#F2CC77"     # gold ground, clear of ORO artwork
F_PAPEL = "#E4D6B4"     # paper ground, clear of CREMA artwork
F_AZUL  = "#22406E"     # blue ground, clear of the AZUL_CUERPO body
F_NEGRO = "#141518"

LETRERO = "TAQUERIA y CERVECERIA"
MENU = ("GOURMET TACOS", "TORTAS", "FRESH JUICES",
        "CEVICHE / TOSTADAS", "SHRIMP & FISH")
PROV = "TEXTO: MEDIDO · LETRERO · AUTORADO"


class Rejilla(object):
    """One grid for the whole set.

    ⚠ WHAT IS INVARIANT IS THE USABLE BOX, NOT THE SHEET.  Two earlier
    versions of this docstring claimed more than that: the first said margin
    and column together made every format "the same design at different
    sizes", the second narrowed it to `y(k)/h`.  THE ROW IN `main` REFUTED THE
    SECOND ON ITS FIRST RUN -- `y(k)/h` spreads 2.78e-02 across these eleven
    formats, because the margin is `min(w, h)/12` and so is a different
    fraction of the height on a portrait sheet than on a landscape one.

    The true statement, and the one the layouts actually rely on:

      * `(y(k) - m) / (h - 2m)` is EXACTLY `k / rows` on every format.  Row 6
        is a quarter of the way down the usable box on an 85 mm card and on a
        900 mm panel alike.
      * `(x(i) - m) / (w - 2m)` is `(i / cols) * (1 + gut / (w - 2m))` -- the
        columns are invariant only to within the gutter term, which is small
        and format-dependent.
      * NEITHER is invariant as a fraction of the SHEET, and cannot be: a
        margin that is optically equal on all four sides is a constant
        fraction of the short side and a varying fraction of the long one.

    All three are measured in `main` rather than asserted here."""

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



# Pieces that bleed to the trim by design.  Declared, not tolerated silently.
SANGRA = {"vaso"}

# AUTHORED, and it will be moved to whatever the measurement supports -- see
# the printed table under `type presence`.  It is a PRESENCE bar, not a
# fidelity one: Chromium and PIL hint and kern differently, so an identical
# run does not score 1.000.
# AUTHORED, and both were placed AFTER watching the clean set and the
# occlusion ablation print their numbers -- never the other way round (rule 5).
GAP_EM = 1.20        # a word space is ~0.3 em; the disc ate about 5
EXT_FRAC = 0.80      # inked width against the face's own metric for the run

# ⚠ TYPE HAS A PHYSICAL FLOOR AND THE GRID DID NOT KNOW IT.  The type scale is
# anchored on the baseline unit, and the baseline unit on an 85 x 55 mm card is
# 1.91 mm, so `pt(-2.4)` asked for 0.90 mm -- about two and a half points.  The
# card's provenance line rendered FOUR PIXELS of an expected 345 at 200 dpi:
# set, checked, exported and invisible.  1.8 mm is roughly 5 pt, the smallest
# size a colophon is set at in print.  A run that cannot fit its measure AT the
# floor is a design problem, so it is reported rather than shrunk past it.
MIN_TIPO_MM = 1.8
DEMASIADO = []


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
    """-> (size_mm, factor).  Shrink a size until the run fits its measure.

    ⚠ IT USED TO SUM PER-GLYPH ADVANCES -- `sum(getlength(c) for c in s)` --
    which is the UN-KERNED width, the exact quantity its own next sentence
    called Chromium's estimate wrong for.  It now measures the STRING, so the
    pairs kern, and it keeps the per-glyph sum as an upper bound so the
    pre-flight still errs wide rather than narrow.

    ⚠ It returns the FACTOR as well as the size, because the caller's tracking
    was computed for the size BEFORE this shrink: applying an unchanged
    absolute tracking at 60 % of the size doubles the spacing relative to the
    letterforms, which is what the foot lines on the small formats were doing.
    """
    from PIL import ImageFont
    path = lienzo.FACES.get(face)
    if not path or not os.path.exists(path) or not s:
        return pt, 1.0
    pt0 = pt
    for _ in range(24):
        f = ImageFont.truetype(path, max(4, int(round(pt * 96 / 25.4))))
        kerned = f.getlength(s)
        loose = sum(f.getlength(c) for c in s)
        w_px = max(kerned, loose) + tracking * (len(s) - 1) * 96 / 25.4
        if w_px * 25.4 / 96.0 <= max_mm:
            return pt, pt / pt0
        pt *= 0.94
    return pt, pt / pt0


def tapado(box, opaque, order):
    """-> fraction of a text run's box covered by a slab drawn AFTER it.

    ⚠ THE DEFECT: the A-frame's vignette disc was drawn over
    `TAQUERIA y CERVECERIA` and ate its middle -- the sign read
    "TAQUE...CERIA" -- with every check on the piece green, and THREE
    successive pixel instruments failed to see it.  The last of them was
    defeated by the disc's own outline, which is this run's ink colour and
    crosses the whole band, so every column reads inked.

    Pixels cannot isolate one element from another.  Draw order and geometry
    can, and both are exactly known here."""
    if box is None:
        return 0.0
    x0, y0, x1, y1 = box
    A = max(1e-9, (x1 - x0) * (y1 - y0))
    hit = 0.0
    for kind, geom, o in opaque:
        if o <= order:
            continue
        if kind == "rect":
            gx0, gy0, gx1, gy1 = geom
            w = max(0.0, min(x1, gx1) - max(x0, gx0))
            h = max(0.0, min(y1, gy1) - max(y0, gy0))
            hit = max(hit, w * h / A)
        elif kind == "circle":
            cx, cy, r = geom
            # sampled, not solved: a disc against a box has no one-line area,
            # and a 40 x 12 lattice resolves a covered word without pretending
            # to a precision this does not need
            n = 0; tot = 40 * 12
            for i in range(40):
                px_ = x0 + (i + 0.5) * (x1 - x0) / 40.0
                for j in range(12):
                    py_ = y0 + (j + 0.5) * (y1 - y0) / 12.0
                    if (px_ - cx) ** 2 + (py_ - cy) ** 2 <= r * r:
                        n += 1
            hit = max(hit, n / float(tot))
    return hit


def texto_legible(png_path, w_mm, h_mm, t, pad=1.9):
    """-> (gap_em, extent_frac) for one text run, read off the RENDERED sheet.

    ⚠ THE DEFECT THIS EXISTS FOR: the A-frame's vignette disc was drawn after
    `TAQUERIA y CERVECERIA` and covered its middle -- the sign read
    "TAQUE...CERIA" -- with every check on the piece green.  Nothing in this
    module compared one element against another, and neither margin check can
    see anything between the margins.

    ⚠⚠ TWO EARLIER INSTRUMENTS FOR THIS WERE BOTH WRONG, AND BOTH PRINTED A
    PLAUSIBLE NUMBER.  The first counted pixels within 26 of the ink colour
    against PIL's own glyph pixels: it scored `postal`'s provenance line 0.207
    and `tarjeta`'s 0.324, and the PAINTED WINDOW showed both fully set and
    perfectly legible -- at 15 px most of a condensed face is partial coverage,
    so that ratio measured TYPE SIZE, not presence.  The second weighted by ink
    mass against a per-window background, and the window straddles a gold page
    and a cream disc, so the second background counted as ink: it scored the
    plainly-eaten subhead at 1.015.  A third, per-pixel median background,
    scored a fully-visible display line at 0.307, because a median wider than
    the stems of a heavy slab face returns the STEM, not the page.

    So this one has no background model and no reference raster to align:

      * `gap_em`   -- the widest run of consecutive columns carrying NO ink of
                      this run's colour, between its first and last inked
                      column, in multiples of the type size.  A word space is
                      about 0.3 em; the disc ate about 5 em.
      * `extent`   -- inked width over the width the face's own metrics say the
                      run should occupy.  Catches an end being cut off, which a
                      middle-gap measure cannot see.

    Both are invariant to size, to antialiasing and to Chromium kerning
    tighter than PIL, which is what defeated the three before it."""
    path = lienzo.FACES.get(t["face"])
    if not path or not os.path.exists(path) or not t["s"]:
        return None, None
    from PIL import ImageFont
    im = Image.open(png_path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    H, W = a.shape[:2]
    ppm = W / float(w_mm)
    px = max(4, int(round(t["pt"] * ppm)))
    f = ImageFont.truetype(path, px)
    trk = t["tracking"] * ppm
    wid = sum(f.getlength(c) for c in t["s"]) + trk * (len(t["s"]) - 1)
    asc, desc = f.getmetrics()
    bx = t["x"] * ppm
    if t["anchor"] == "middle": x0 = bx - wid / 2.0
    elif t["anchor"] == "end":  x0 = bx - wid
    else:                       x0 = bx
    by = t["y"] * (H / float(h_mm))
    p = pad * px * 0.5
    X0 = max(0, int(x0 - p)); X1 = min(W, int(x0 + wid + p))
    Y0 = max(0, int(by - asc - p)); Y1 = min(H, int(by + desc + p))
    if X1 <= X0 or Y1 <= Y0 or wid <= 0:
        return 99.0, 0.0
    # generous tolerance: an antialiased edge is still this run's ink
    col = near(a[Y0:Y1, X0:X1], t["fill"], tol=90).any(axis=0)
    if not col.any():
        return 99.0, 0.0
    lo = int(np.argmax(col)); hi = len(col) - 1 - int(np.argmax(col[::-1]))
    inner = col[lo:hi + 1]
    gap = run = 0
    for v in inner:
        run = 0 if v else run + 1
        gap = max(gap, run)
    return gap / float(px), (hi - lo + 1) / float(wid)


def _rgb(hexc):
    return np.array([int(hexc[i:i + 2], 16) for i in (1, 3, 5)], np.int16)


def hero_crop(png_path, w_mm, h_mm, box):
    """The RENDERED pixels inside a hero box, in the box's own frame."""
    im = Image.open(png_path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    H, W = a.shape[:2]
    x0 = int(round(box[0] / w_mm * W)); x1 = int(round(box[2] / w_mm * W))
    y0 = int(round(box[1] / h_mm * H)); y1 = int(round(box[3] / h_mm * H))
    x0 = max(0, x0); y0 = max(0, y0); x1 = min(W, x1); y1 = min(H, y1)
    return a[y0:y1, x0:x1]


def near(a, hexc, tol=26):
    """Pixels within `tol` of a colour, per channel, in the CROP.  This is the
    window every count below is taken through, and `--paint` writes it out."""
    return (np.abs(a - _rgb(hexc)).max(axis=2) <= tol)


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


# The wordmark is not a fill among fills.  It is the identity, it is the one
# element on every sheet that must read from across a street, and it is held to
# a higher bar than the drawing is.  4.5:1 is WCAG's own level for large text;
# a decorative fill may sit quietly against its page, a logotype may not.
MARCA_BAR = 4.5
MARCAS = []


def put_wordmark(L, cx, top, width, ink=TINTA, ground=None):
    """⚠ THIS WAS THE ONE ELEMENT NO CHECK COULD SEE.  It draws through
    `L.paths`, so the ink/ground row -- which reads `DRAWN`, written by
    `put_hero` -- never saw it, and a sweep of the SVG's `fill=` attributes
    skips paths as "heroes, already checked".  It fell through both.

    MEASURED, once it was looked for: `carta` set the wordmark in TINTA on its
    GRANA header band at 1.295:1, BELOW THIS MODULE'S OWN FLOOR for a
    decorative fill, and `vidriera` and `cartel_a3` set it in TINTA on F_AZUL
    at 1.584:1 -- a dark blob where the mark should be, on a window sign whose
    entire job is to be read from the pavement.  Every call now declares the
    ground it is printed on and is checked against it."""
    # THE ABLATION IS THE DEFECT: every mark back to the module default, which
    # is what put `carta`'s at 1.295:1 on its own header band.
    if os.environ.get("T1_PLIEGO_MARCAPLANA") == "1":
        ink = TINTA
    comps, w, h = wordmark()
    s = width / float(w)
    L.paths(trazo.to_svg_paths(comps, scale=s, dx=cx - width / 2.0, dy=top), ink)
    MARCAS.append({"piece": PIEZA[0], "ink": ink,
                   "ground": (ground or GROUND[0]),
                   "ratio": estilo_vec.contrast(ink, ground or GROUND[0])})
    return h * s


# WHAT WAS ACTUALLY DRAWN, RECORDED AS IT IS DRAWN.  Every check in this file
# used to read either the sheet's margins or a colour typed into a table; none
# of them could see a fill inside the live area.  This list is written by the
# drawing itself, so the visibility check reads the piece that shipped.
DRAWN = []
FIT = []             # every run's shrink factor, so the type scale is auditable
TEXTS = []           # every run as printed, so a colophon can be checked

# What each style is called IN PRINT.  A piece's colophon is a PROVENANCE
# claim -- `playera` printed "ARTE PLANO" over a `silueta` drawing -- so the
# names live here and a check reads them back off the piece.
ESTILO_ES = {"plano": "ARTE PLANO", "papel": "PAPEL PICADO",
             "azulejo": "ESTILO AZULEJO", "silueta": "SILUETA"}
GROUND = [None]      # the page colour of the piece being drawn
PIEZA = [None]       # its name


def put_hero(L, style, box, mural="fino", ink=None, ground=None):
    """`ground` overrides the PAGE colour when the drawing sits on something
    else -- a vignette disc, a band.  The keyline is chosen against whatever
    the drawing is actually printed over, so putting a cream vehicle on a
    cream disc cannot silently reproduce the defect the disc was added for."""
    lay, wh = estilo_vec.layers(TAG, style, box, mural=mural, ink=ink,
                                ground=(ground or GROUND[0]))
    kw = max(0.10, wh[1] * 0.0026)      # keyline weight scales with the drawing
    for ds, col, key in lay:
        L.paths(ds, col, stroke=key, stroke_w=(kw if key else 0.0))
        DRAWN.append({"piece": PIEZA[0], "style": style,
                      "ground": (ground or GROUND[0]),
                      "fill": col, "key": key, "box": box, "kw": kw})
    return wh


# ============================================================== the pieces
# (name, w_mm, h_mm, style, ground, builder)

def _poster(L, g, style, sub, foot, rule_col=GRANA, edge=TINTA, txt=TINTA,
            mark=TINTA):
    """The portrait master layout.  Rows are indices on the 24-row grid, so the
    SAME numbers place the same way on an 85 mm card and a 900 mm panel."""
    L.frame(g.m * 0.55, edge, g.s / 300.0)
    wh = put_wordmark(L, g.w / 2.0, g.y(1.4), g.span(8), ink=mark)
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
    """THE SIDEWALK SIGN.  It had been `_poster` with a different subhead, so
    it and `cartel_a2` were the same piece at two sizes -- in a set whose whole
    purpose is range.

    The format cues are taken from HIS PHOTOGRAPH, `ref_sign_aframe.jpg`, and
    only the format: a gold ground, and the vehicle standing in a LIGHT DISC
    that lifts it off that ground.  ⚠ NOT the palette -- he said the sign was
    "just an example of a promotional product" -- and NOT the offer, the app
    callout or the QR code, which are his to approve, not mine to invent.

    The disc is also the reason this piece can carry the vehicle at size: a
    cream body on gold needs a keyline, a cream body on a cream disc needs a
    keyline against THAT, and `put_hero(ground=...)` is told which."""
    L.frame(g.m * 0.55, GRANA, g.s / 300.0)
    wh = put_wordmark(L, g.w / 2.0, g.y(1.5), g.span(9))
    T(L, g, g.w / 2.0, g.y(1.5) + wh + g.base * 1.15, LETRERO, "cond",
           g.pt(0.6), GRANA, tracking=g.pt(0.6) * 0.26)

    # ⚠ THE DISC IS DEFINED BY THE ROWS IT MAY OCCUPY, NOT BY A WIDTH.  The
    # first version was `span(11)/2` centred on row 12.4, and it covered the
    # middle of `TAQUERIA y CERVECERIA` -- the sign read "TAQUE...CERIA" with
    # every check green, because nothing here could see one element drawn over
    # another.  Rows 7.4 to 19.6 are empty by construction, and the radius is
    # clamped to the live width so the same expression works on any format.
    # THE ABLATION IS THE DEFECT ITSELF, restored: the disc as it was first
    # written.  `T1_PLIEGO_OCLUIR=1` puts it back over the subhead, and the
    # `type PRESENT` row must go red -- a check that has only ever been watched
    # passing is not a check (rule 3).
    if os.environ.get("T1_PLIEGO_OCLUIR") == "1":
        r = g.span(11) / 2.0; cy = g.y(12.4)
    else:
        r = min((g.y(19.6) - g.y(7.4)) / 2.0, (g.w - 2 * g.m) / 2.0)
        cy = (g.y(19.6) + g.y(7.4)) / 2.0
    L.circle(g.w / 2.0, cy, r, HUESO, stroke=GRANA, stroke_w=g.s / 420.0)
    bw = r * 1.72; bh = r * 1.02
    put_hero(L, "plano",
             (g.w / 2.0 - bw / 2.0, cy - bh / 2.0,
              g.w / 2.0 + bw / 2.0, cy + bh / 2.0), ground=HUESO)

    T(L, g, g.w / 2.0, g.y(21.0), "SE SIRVE DESDE LA COMBI", "display",
           g.pt(0.4), GRANA)
    T(L, g, g.w / 2.0, g.y(23.2), "SERIE COMBI · CALLE · " + PROV, "cond",
           g.pt(-2.0), GRANA, tracking=g.pt(-2.0) * 0.12,
           measure=g.w - 2 * (g.m * 0.55) - 2 * g.gut)

def p_cartel_a2(g, L):
    _poster(L, g, "plano", "SE SIRVE DESDE LA COMBI",
            "SERIE COMBI · IMPRESO · " + PROV)

def p_cartel_a3(g, L):
    _poster(L, g, "azulejo", "SE SIRVE DESDE LA COMBI",
            "SERIE COMBI · ESTILO AZULEJO · " + PROV,
            rule_col=CIELO, edge=CIELO, txt=HUESO, mark=HUESO)

def p_carta(g, L):
    L.rect(g.m * 0.55, g.m * 0.55, g.w - g.m * 1.1, g.base * 4.4, GRANA)
    L.frame(g.m * 0.55, TINTA, g.s / 320.0)
    # ⚠ CREMA, not TINTA: the mark sat on its own GRANA band at 1.295:1
    put_wordmark(L, g.w / 2.0, g.y(0.7), g.span(6), ink=CREMA, ground=GRANA)
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
    put_hero(L, "papel", (g.x(1), g.y(6.6), g.x(1) + g.span(10), g.y(17.4)),
             ink=CREMA)
    T(L, g, g.w / 2.0, g.y(19.8), LETRERO, "cond", g.pt(-0.3), ORO,
           tracking=g.pt(-0.3) * 0.26)
    T(L, g, g.w / 2.0, g.y(23.4),
           "MERCANCIA · " + ESTILO_ES["papel"] + " · " + PROV, "cond",
           g.pt(-2.3), "#7A6E63", tracking=g.pt(-2.3) * 0.1)

# ---- landscape sheets: the hero takes one side, the lockup the other --------
def _paisaje(L, g, style, edge, rule_col, big=None, big_col=None, txt=TINTA,
             mark=TINTA):
    L.frame(g.m * 0.5, edge, g.s / 260.0)
    put_hero(L, style, (g.x(6), g.y(2.0), g.x(6) + g.span(6), g.y(21.5)))
    cx = g.x(0) + g.span(6) / 2.0
    wh = put_wordmark(L, cx, g.y(4.0), g.span(5.4), ink=mark)
    T(L, g, cx, g.y(4.0) + wh + g.base * 1.2, LETRERO, "cond", g.pt(-0.7),
           rule_col, tracking=g.pt(-0.7) * 0.22)
    if big:
        T(L, g, cx, g.y(15.0), big, "display", g.pt(1.0), big_col or txt)
    T(L, g, g.w / 2.0, g.y(23.4), PROV, "cond", g.pt(-2.3), rule_col,
           tracking=g.pt(-2.3) * 0.1)

def p_vidriera(g, L):
    _paisaje(L, g, "azulejo", CIELO, CIELO, big="ABIERTO", big_col=HUESO,
             mark=HUESO)

def p_postal(g, L):
    """THE PICTURE SIDE OF A POSTCARD -- the drawing is the piece.

    ⚠ It and `tarjeta` were the SAME CALL, `_paisaje(..., "plano", ...)`, at
    two sizes: two of eleven pieces in a set whose whole purpose is range.  A
    postcard leads with the picture and signs it small; a calling card leads
    with the mark.  They are two layouts now, and `silueta` stays out of both
    -- at 148 mm it read as an unrecognisable black lump."""
    L.frame(g.m * 0.5, GRANA, g.s / 260.0)
    put_hero(L, "plano", (g.x(0), g.y(1.6), g.x(0) + g.span(12), g.y(16.6)))
    L.line(g.x(0), g.y(18.0), g.x(0) + g.span(12), g.y(18.0), GRANA,
           g.s / 420.0)
    wh = put_wordmark(L, g.x(0) + g.span(4) / 2.0, g.y(19.0), g.span(4))
    T(L, g, g.x(0) + g.span(12), g.y(19.0) + wh * 0.62, LETRERO, "cond",
           g.pt(-1.2), GRANA, anchor="end", tracking=g.pt(-1.2) * 0.22,
           measure=g.span(7))
    T(L, g, g.x(0) + g.span(12), g.y(22.9), PROV, "cond", g.pt(-2.2), GRANA,
           anchor="end", tracking=g.pt(-2.2) * 0.08, measure=g.span(9))


def p_tarjeta(g, L):
    """THE CALLING CARD -- the mark is the piece and the drawing signs it."""
    L.frame(g.m * 0.5, GRANA, g.s / 240.0)
    wh = put_wordmark(L, g.w / 2.0, g.y(2.4), g.span(7))
    T(L, g, g.w / 2.0, g.y(2.4) + wh + g.base * 1.1, LETRERO, "cond",
           g.pt(-0.4), GRANA, tracking=g.pt(-0.4) * 0.26)
    put_hero(L, "plano", (g.x(3), g.y(12.6), g.x(3) + g.span(6), g.y(20.2)))
    T(L, g, g.w / 2.0, g.y(22.6), PROV, "cond", g.pt(-2.2), GRANA,
           tracking=g.pt(-2.2) * 0.08,
           measure=g.w - 2 * (g.m * 0.5) - 2 * g.gut)

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
 ("calle",     "aframe",    600, 900, F_ORO,   p_aframe),
 ("impreso",   "cartel_a2", 420, 594, F_ORO,   p_cartel_a2),
 ("impreso",   "cartel_a3", 297, 420, F_AZUL,  p_cartel_a3),
 ("calle",     "carta",     300, 420, CREMA, p_carta),
 ("calle",     "vidriera",  500, 350, F_AZUL,  p_vidriera),
 ("impreso",   "postal",    148, 105, F_PAPEL, p_postal),
 ("impreso",   "tarjeta",    85,  55, F_PAPEL, p_tarjeta),
 ("impreso",   "volante",   148, 210, HUESO, p_volante),
 ("mercancia", "bolsa",     380, 420, "#DED2B8", p_bolsa),
 ("mercancia", "playera",   300, 360, F_NEGRO, p_playera),
 ("mercancia", "vaso",      220,  95, F_PAPEL, p_vaso),
]


def main(argv):
    global OUT
    only = None; dpi = 150
    for i, a in enumerate(argv):
        if a == "--only": only = argv[i + 1]
        if a == "--out":  OUT = argv[i + 1]
        if a == "--dpi":  dpi = int(argv[i + 1])
    paint = "--paint" in argv
    os.makedirs(OUT, exist_ok=True)
    print("pliego.py -- print set, SVG masters, %d mm sheets" % len(PIEZAS))

    made = []
    for cat, name, w, h, ground, fn in PIEZAS:
        if only and only not in (cat, name): continue
        GROUND[0] = ground; PIEZA[0] = name
        g = Rejilla(w, h)
        L = lienzo.Lienzo(w, h, bg=ground)
        fn(g, L)
        stem = os.path.join(OUT, "pl_%s_%s" % (cat, name))
        svg = L.save_svg(stem + ".svg")
        L.render(svg, png=stem + ".png", pdf=stem + ".pdf", dpi=dpi)
        made.append((cat, name, w, h, g, stem))
        for t in TEXTS:
            if t["piece"] == name and "tapado" not in t:
                t["tapado"] = tapado(t["box"], L.opaque, t["order"])
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

    stems0 = {n: (w, h, st) for _c, n, w, h, _g, st in made}

    # ============================================================ THE GRID
    # The docstring on `Rejilla` claims one invariance and disclaims another.
    # Both are MEASURED here rather than asserted, over the formats that were
    # actually built, because a claim in a docstring is not a measurement.
    ys, xs, ysh = [], [], []
    for _c, _n, w, h, g, _st in made:
        ys.append([(g.y(k) - g.m) / (h - 2 * g.m) for k in (0, 6, 12, 18, 24)])
        xs.append([(g.x(i) - g.m) / (w - 2 * g.m) for i in (0, 3, 6, 9)])
        ysh.append([g.y(k) / h for k in (0, 6, 12, 18, 24)])
    if made:
        dy = max(max(c) - min(c) for c in zip(*ys))
        dx = max(max(c) - min(c) for c in zip(*xs))
        dsh = max(max(c) - min(c) for c in zip(*ysh))
        # the bar on the columns is the GUTTER TERM, computed from the built
        # formats -- an independently obtained quantity, not this expression
        gt = max(g.gut / (w - 2 * g.m) for _c, _n, w, _h, g, _st in made)
        ck(dy < 1e-12 and dx <= gt + 1e-12,
           "grid: rows exact in the usable box (spread %.1e); columns within "
           "the gutter term (%.4f vs %.4f); NEITHER invariant on the sheet "
           "(y(k)/h spreads %.4f) -- %d formats"
           % (dy, dx, gt, dsh, len(made)))

    # THE TYPE SCALE.  Every run is authored on a 1.335 scale and then shrunk
    # by `fit_pt` if it will not fit, so the scale is a starting point and not
    # a property of the sheet.  Printing the worst shrink is the difference
    # between knowing that and believing the docstring.
    if FIT:
        worst = min(FIT, key=lambda r: r[2])
        nsh = sum(1 for r in FIT if r[2] < 0.999)
        ck(worst[2] > 0.45,
           "type: %d of %d run(s) shrunk off the 1.335 scale; worst %.3f x on "
           "%s %r (tracking follows the shrink)"
           % (nsh, len(FIT), worst[2], worst[0], worst[1]))

    # ================================================== IS THE TYPE THERE
    if MARCAS:
        wm = min(MARCAS, key=lambda m: m["ratio"])
        ck(wm["ratio"] >= MARCA_BAR,
           "wordmark: %d drawn, each checked against the ground it is printed "
           "on; weakest %.3f:1 on %s (%s on %s, bar %.1f)"
           % (len(MARCAS), wm["ratio"], wm["piece"], wm["ink"], wm["ground"],
              MARCA_BAR))

    cov = sorted(((t.get("tapado", 0.0), t["piece"], t["s"][:30])
                  for t in TEXTS), reverse=True)
    if cov:
        ck(cov[0][0] <= 0.02,
           "occlusion: %d run(s) tested against every slab drawn after them; "
           "worst covered %.1f %% -- %s %r"
           % (len(cov), 100 * cov[0][0], cov[0][1], cov[0][2]))

    rat = []
    for t in TEXTS:
        if t["piece"] not in stems0: continue
        w, h, st = stems0[t["piece"]]
        gap, ext = texto_legible(st + ".png", w, h, t)
        if gap is None: continue
        rat.append((gap, ext, t["piece"], t["s"][:26]))
    rat.sort(reverse=True)
    if rat:
        print("   type read back off the sheet, widest 8 gaps of %d run(s):"
              % len(rat))
        for r in rat[:8]:
            print("     gap %5.2f em   extent %.3f   %-10s %s"
                  % (r[0], r[1], r[2], r[3]))
        worst_g = rat[0]
        worst_e = min(rat, key=lambda r: r[1])
        ck(worst_g[0] <= GAP_EM and worst_e[1] >= EXT_FRAC,
           "type PRESENT: %d run(s); widest hole %.2f em on %s %r (bar %.2f); "
           "narrowest extent %.3f on %s %r (bar %.2f)"
           % (len(rat), worst_g[0], worst_g[2], worst_g[3], GAP_EM,
              worst_e[1], worst_e[2], worst_e[3], EXT_FRAC))

    ck(not DEMASIADO, "type floor: %.2f mm; %d run(s) could not fit their "
                      "measure at it%s"
       % (MIN_TIPO_MM, len(DEMASIADO),
          ("  <-- " + " | ".join("%s %r in %.0f mm" % d for d in DEMASIADO[:3]))
          if DEMASIADO else ""))

    # ================================================== PROVENANCE OF STYLE
    # ⚠ `playera` PRINTED "ARTE PLANO" ACROSS THE FOOT OF A `silueta` DRAWING.
    # That is F372's class exactly -- a provenance line stating something the
    # artefact does not do -- and thirty-six green checks did not see it,
    # because the string and the drawing were never compared to each other.
    drew = {}
    for d in DRAWN:
        drew.setdefault(d["piece"], set()).add(d["style"])
    lies = []
    for t in TEXTS:
        for st, es in ESTILO_ES.items():
            if es in t["s"] and st not in drew.get(t["piece"], ()):
                lies.append("%s says %r, drew %s"
                            % (t["piece"], es,
                               "/".join(sorted(drew.get(t["piece"], ()))) or "nothing"))
    ck(not lies, "colophons: %d run(s) checked against the styles actually "
                 "drawn, %d misnamed%s"
       % (len(TEXTS), len(lies), ("  <-- " + " | ".join(lies[:3])) if lies else ""))

    # ============================================================ VISIBILITY
    # ⚠ THIS IS THE CLASS THAT HAS SHIPPED MOST OFTEN IN THIS PROJECT: a shape
    # that is traced, rasterised and printed IN THE PAGE COLOUR.  F378 (a sixth
    # of the vehicle painted white on white), `playera` (TINTA on near-black),
    # `azulejo` (the body filled AZUL on an AZUL page, 1.00:1) and six of these
    # eleven sheets.  Neither `margin_clean` nor `edge_clean` can see it -- they
    # only read the margins, and a fill at zero contrast has no luminance step
    # for either to find.  These two rows read INSIDE the live area.
    #
    # (a) ANALYTIC: every fill either clears the bar against its own page, or
    #     carries a keyline that clears the bar against BOTH page and fill.
    bad = []
    for d in DRAWN:
        c = estilo_vec.contrast(d["fill"], d["ground"])
        if c >= estilo_vec.KEY_BAR:
            continue
        if d["key"] is None:
            bad.append("%s %s on %s %.3f:1 NO KEYLINE"
                       % (d["piece"], d["fill"], d["ground"], c))
            continue
        kg = estilo_vec.contrast(d["key"], d["ground"])
        kf = estilo_vec.contrast(d["key"], d["fill"])
        if min(kg, kf) < estilo_vec.KEY_BAR:
            bad.append("%s keyline %s only %.3f/%.3f"
                       % (d["piece"], d["key"], kg, kf))
    ck(not bad, "ink/ground: %d fill(s) drawn, %d needed a keyline, %d "
                "UNSEEABLE%s"
       % (len(DRAWN), sum(1 for d in DRAWN if d["key"]), len(bad),
          ("  <-- " + " | ".join(bad[:3])) if bad else ""))

    # (b) PIXEL: the keyline is asserted to be PRINTED, counted in the rendered
    #     sheet through a window that is written to disk and looked at.  An
    #     analytic table alone would only prove the intention (rule 10).
    stems = stems0
    seen = set(); shown = 0; miss = []
    for d in DRAWN:
        if d["key"] is None or d["piece"] not in stems: continue
        k = (d["piece"], d["fill"], d["key"])
        if k in seen: continue
        seen.add(k)
        w, h, st = stems[d["piece"]]
        a = hero_crop(st + ".png", w, h, d["box"])
        m = near(a, d["key"])
        n = int(m.sum())
        # INDEPENDENT SCALE, not a typed constant: the keyline is `kw` mm wide
        # and the drawing is `box` wide, so one stroke crossing the box once is
        # already this many pixels.  Anything less than that is not a line.
        px_mm = a.shape[1] / max(1e-6, (d["box"][2] - d["box"][0]))
        floor = max(8.0, d["kw"] * px_mm * a.shape[0] * 0.05)
        if n < floor: miss.append("%s %s %d px < %.0f" % (d["piece"], d["key"], n, floor))
        else: shown += 1
        if paint:
            im = Image.fromarray(a.astype(np.uint8)).copy()
            q = np.asarray(im).copy(); q[m] = (255, 0, 255)
            Image.fromarray(q).save(os.path.join(
                OUT, "pl_VENTANA_%s_%s_sobre_%s.png"
                % (d["piece"], d["fill"].lstrip("#"), d["key"].lstrip("#"))))
    # ⚠ AN EMPTY MATCH SET IS NOT A PASS.  F380 is exactly this row's failure
    # mode one file over: with keylines switched off there is nothing to count,
    # and "0 of 0 found" would print green over the defect the row exists for.
    # So the row also asserts that every sub-bar fill HAS a keyline to look for.
    unkeyed = sum(1 for d in DRAWN
                  if estilo_vec.contrast(d["fill"], d["ground"]) < estilo_vec.KEY_BAR
                  and d["key"] is None)
    ck(not miss and not unkeyed,
       "keylines PRINTED: %d of %d found in the rendered sheet; %d sub-bar "
       "fill(s) with no keyline to look for%s"
       % (shown, shown + len(miss), unkeyed,
          ("  <-- " + " | ".join(miss[:3])) if miss else ""))

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
