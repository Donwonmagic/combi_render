"""
estilo_vec.py -- the six styles AS VECTOR, for `lienzo.py`.

`estilos.py` draws the styles as RASTER, by compositing upscaled pixel masks.
This module produces the SAME styles as ordered lists of (svg path data, fill),
traced by `trazo.py` from the underlay, so a piece can be drawn at any size and
printed from the master.  ⚠ IT DOES NOT REPLACE `estilos.py`: that module still
owns the underlay recovery and the raster proofs, and its ablation
(`T1_EST_NOKEY`) still guards the colour key both modules depend on.

⚠ CEILINGS.
  * A style is an ARRANGEMENT OF INKS, and the arrangement is AUTHORED.  Nothing
    here measures whether it is any good.
  * `linea`, `riso` and `sello` depend on raster screens -- hatching, halftone
    dots, a broken edge -- which are not naturally vector.  They are NOT ported
    here; only the four styles that are genuinely shape-based are.  Asking this
    module for one of the other three REFUSES rather than returning a silently
    different drawing (rule 37).
"""
import os
import math
import numpy as np
import trazo, estilos

CREMA = "#F0E7D1"; ROJO = "#AC2921"; GRANA = "#601A16"
ORO   = "#DE9E2E"; TINTA = "#241E1E"; PIZ  = "#38424A"
AZUL  = "#1A2E54"; CIELO = "#96BED6"; HUESO = "#FAF6EC"

# z-order matters: later layers paint over earlier ones
PLANO = [("_rest", PIZ), ("interior_dark", TINTA), ("glass", PIZ),
         ("countertan", ORO), ("countercream", CREMA), ("gal_menucard", CREMA),
         ("steel", PIZ), ("chrome_dull", PIZ), ("chrome", CREMA),
         ("underseal", TINTA), ("rubber", TINTA),
         ("body_cream", CREMA), ("body_red", ROJO), ("T1_paint_rest", ROJO),
         ("lidmural_rest", GRANA), ("mural_ground", GRANA), ("mural_gold", ORO),
         ("lidsign", ORO), ("body_gold", ORO),
         ("calidad_field", CREMA), ("calidad_ink", ROJO), ("roundelred", ROJO),
         ("bumpercream", CREMA), ("tyre", TINTA), ("wheelcream", CREMA),
         ("capred", ROJO), ("capwhite", CREMA), ("script", TINTA),
         ("bulb", HUESO)]

PAPEL_HOLES = ("glass", "body_gold", "script", "mural_gold", "bulb",
               "calidad_ink", "wheelcream", "capwhite", "gal_menucard")

AZULEJO_EDGE = ("body_gold", "mural_gold", "script", "calidad_ink", "glass",
                "body_cream", "body_red", "mural_ground", "tyre", "wheelcream")

VECTOR_STYLES = ("plano", "papel", "azulejo", "silueta")

# ⚠ THE BLUEPRINT BODY WAS THE GROUND COLOUR EXACTLY.  `azulejo` filled the
# silhouette with AZUL on sheets whose ground is also AZUL -- contrast 1.00:1,
# a full-body path written, rasterised and printed at zero contrast.  The body
# is now a step darker than the ground, so the form reads as a form.
AZUL_CUERPO = "#0E1B2E"


# ---------------------------------------------------------------- keylines
# WCAG relative luminance.  Lives HERE and not in `pliego.py` because the
# decision it drives -- whether a fill needs an outline -- is part of drawing
# the piece, not part of laying it out.  `pliego` imports these.
def _lum(hexc):
    v = [int(hexc[i:i + 2], 16) / 255.0 for i in (1, 3, 5)]
    v = [(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4) for c in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


def contrast(a, b):
    """WCAG relative-luminance ratio, 1.0 = identical."""
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# The bar is a VISIBILITY bar, not a legibility bar.  WCAG's own floor for
# non-text graphics is 3.0:1; this is deliberately far below it, because a
# drawing may legitimately sit close to its page.  What it forbids is the
# thing that actually shipped: a shape at 1.00-1.25:1, which is not a quiet
# passage, it is an absent one.
KEY_BAR = 1.35
KEY_INKS = (TINTA, GRANA, AZUL_CUERPO, PIZ, AZUL, ROJO, ORO, CREMA, HUESO)


# In-process switch for the SAME suppression the environment variable does, so
# a build can draw a piece twice -- with and without keylines -- and DIFFERENCE
# the two renders.  See `pliego`'s `keylines PRINTED` row: a colour-tolerance
# count of the shipped sheet passed with all nine strokes physically deleted.
NOKEY = [False]


def keyline_for(fill, ground, bar=KEY_BAR):
    """The ink that outlines `fill` when `fill` cannot be seen on `ground`.

    Returns None when the fill already clears the bar.  Otherwise picks the
    palette ink that maximises the WEAKER of its two separations -- from the
    page and from the fill it outlines -- so the keyline is neither lost in
    the ground nor lost in the shape it is drawing round."""
    if contrast(fill, ground) >= bar:
        return None
    best, score = None, 0.0
    for ink in KEY_INKS:
        sc = min(contrast(ink, ground), contrast(ink, fill))
        if sc > score:
            best, score = ink, sc
    return best if score >= bar else None


def inks_used(style):
    """Every fill a style can emit.  Exists so a piece can be CHECKED against
    its ground before it is drawn -- six of eleven sheets shipped with artwork
    painted in exactly the page colour."""
    if style == "plano":   return sorted({c for _k, c in PLANO})
    if style == "papel":   return [GRANA]
    if style == "silueta": return [TINTA]
    if style == "azulejo": return [AZUL_CUERPO, CIELO]
    return []


# PER-LAYER TRACE THRESHOLDS.  One threshold for every layer is what shredded
# the mural: the eps/min_area that suits the SCROLLWORK (bold, open curls)
# destroys the LACE (fine, dense flower field).  Coarse for big flats, fine for
# the mural.  ⚠ AUTHORED, and tuned by looking -- see the A/B this produced.
THRESH = {
    "mural_gold":    (0.45, 1.5),
    "mural_ground":  (0.45, 1.5),
    "lidsign":       (0.45, 1.5),
    "body_gold":     (0.90, 6.0),
    "script":        (0.60, 3.0),
    "calidad_ink":   (0.50, 2.0),
    "calidad_field": (0.50, 2.0),
    "bulb":          (0.50, 1.5),
}
DEFAULT_THRESH = (1.10, 14.0)


def _fit(comps, box, art_wh):
    """Scale traced contours (in capture px) into a mm box, preserving aspect."""
    x0, y0, x1, y1 = box
    aw, ah = art_wh
    s = min((x1 - x0) / float(aw), (y1 - y0) / float(ah))
    dx = x0 + ((x1 - x0) - aw * s) / 2.0
    dy = y0 + ((y1 - y0) - ah * s) / 2.0
    return s, dx, dy


# CONTOUR PRECISION IS FIXED IN MILLIMETRES ON THE SHEET, NOT IN CAPTURE PIXELS.
# ⚠ MEASURED: `pl_impreso_tarjeta.svg` was 1.4 MB for an 85 x 55 mm card, because
# the same contour density that suits a 600 mm panel was being written for a
# 35 mm drawing.  At 300 dpi one millimetre is 11.8 px, so precision finer than
# about 0.12 mm cannot be printed and is pure file weight.  `eps` is therefore
# derived from the OUTPUT SCALE and only ever COARSENS the per-layer value --
# a fine layer stays fine on a poster and simplifies on a card.
PRECISION_MM = 0.12


def _eps_for(scale_mm_per_px, layer_eps):
    """The larger of the layer's own eps and the eps that lands on
    PRECISION_MM at this output scale."""
    if scale_mm_per_px <= 0:
        return layer_eps
    return max(layer_eps, min(24.0, PRECISION_MM / scale_mm_per_px))


def layers(tag, style, box, smooth=2, mural="fino", ink=None, ground=None,
           cache={}):
    """-> ([(svg_d_strings, fill_colour, keyline_or_None)], (w_mm, h_mm)).

    `ground` is the PAGE COLOUR the drawing will be printed on.  Pass it and
    every fill that cannot be seen against it comes back with a keyline."""
    if style not in VECTOR_STYLES:
        raise SystemExit(
            "estilo_vec REFUSES style %r: only %s are shape-based and can be "
            "vectorised.  `linea`, `riso` and `sello` are RASTER SCREENS "
            "(hatching, halftone, a broken edge); returning a silently "
            "different drawing would be worse than refusing (rule 37)."
            % (style, ", ".join(VECTOR_STYLES)))
    # the output scale decides contour precision, so it is part of the key --
    # quantised so nearby sizes share a cache entry instead of re-tracing
    _probe = estilos.underlay(tag)
    _ys, _xs = np.where(_probe["alpha"])
    _aw = _xs.max() - _xs.min() + 1; _ah = _ys.max() - _ys.min() + 1
    _s = min((box[2] - box[0]) / float(_aw), (box[3] - box[1]) / float(_ah))
    tier = round(math.log(max(_s, 1e-6)) * 2.0) / 2.0      # half-log steps
    key = (tag, style, smooth, mural, tier)
    if key not in cache:
        u = estilos.underlay(tag)
        L, al = u["layers"], u["alpha"]
        ys, xs = np.where(al)
        oy, ox = ys.min(), xs.min()
        aw = xs.max() - ox + 1; ah = ys.max() - oy + 1

        def tr(mask, name):
            e, a = THRESH.get(name, DEFAULT_THRESH)
            e2 = _eps_for(_s, e)
            a2 = a * max(1.0, (e2 / e) ** 2)      # area floor follows precision
            c, _d, _k = trazo.trace_cached(mask, tag, name, round(e2, 2),
                                           round(a2, 1), smooth)
            return [([(x - ox, y - oy) for x, y in o],
                     [[(x - ox, y - oy) for x, y in h] for h in hs])
                    for o, hs in c]

        MURAL = ("lidmural_rest", "mural_ground", "mural_gold", "lidsign")
        out = []
        if style == "plano":
            for k, col in PLANO:
                if mural == "llano" and k in MURAL:
                    continue          # the lid is drawn as one flat panel below
                m = L.get(k)
                if m is not None and m.any():
                    out.append((tr(m, k), col))
            if mural == "llano":
                slab = np.zeros_like(al)
                for k in MURAL:
                    if k in L: slab |= L[k]
                if slab.any():
                    out.insert(0, (tr(slab, "mural_slab"), GRANA))
        elif style == "papel":
            holes = np.zeros_like(al)
            for k in PAPEL_HOLES:
                if k in L: holes |= L[k]
            out.append((tr(al & ~holes, "papel"), GRANA))
        elif style == "silueta":
            out.append((tr(al, "silueta"), TINTA))
        elif style == "azulejo":
            out.append((tr(al, "silueta"), AZUL_CUERPO))
            edge = np.zeros_like(al)
            from scipy import ndimage
            for k in AZULEJO_EDGE:
                m = L.get(k)
                if m is not None and m.any():
                    edge |= m & ~ndimage.binary_erosion(m, np.ones((3, 3)))
            out.append((tr(edge, "azulejo_edge"), CIELO))
        cache[key] = (out, (aw, ah))
    out, art_wh = cache[key]
    s, dx, dy = _fit(None, box, art_wh)
    # ⚠ THE INK OVERRIDE IS APPLIED AFTER THE CACHE, not baked into it.  A
    # single-ink style drawn in its default TINTA on a near-black ground is
    # INVISIBLE -- which is exactly what `playera` shipped.  Only the FIRST
    # (body) layer is recoloured; a style's own second ink, like azulejo's
    # keyline, keeps its contrast.
    nokey = os.environ.get("T1_VEC_NOKEYLINE") == "1" or NOKEY[0]
    res = []
    for i, (c, col) in enumerate(out):
        use = ink if (ink and i == 0 and style in ("papel", "silueta")) else col
        key = None if (ground is None or nokey) else keyline_for(use, ground)
        res.append((trazo.to_svg_paths(c, scale=s, dx=dx, dy=dy), use, key))
    return res, (art_wh[0] * s, art_wh[1] * s)
