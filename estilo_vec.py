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


def _fit(comps, box, art_wh):
    """Scale traced contours (in capture px) into a mm box, preserving aspect."""
    x0, y0, x1, y1 = box
    aw, ah = art_wh
    s = min((x1 - x0) / float(aw), (y1 - y0) / float(ah))
    dx = x0 + ((x1 - x0) - aw * s) / 2.0
    dy = y0 + ((y1 - y0) - ah * s) / 2.0
    return s, dx, dy


def layers(tag, style, box, eps=0.9, min_area=6.0, smooth=2, cache={}):
    """-> [(svg_d_strings, fill_colour)] fitted into `box` (mm)."""
    if style not in VECTOR_STYLES:
        raise SystemExit(
            "estilo_vec REFUSES style %r: only %s are shape-based and can be "
            "vectorised.  `linea`, `riso` and `sello` are RASTER SCREENS "
            "(hatching, halftone, a broken edge); returning a silently "
            "different drawing would be worse than refusing (rule 37)."
            % (style, ", ".join(VECTOR_STYLES)))
    key = (tag, style, eps, min_area, smooth)
    if key not in cache:
        u = estilos.underlay(tag)
        L, al = u["layers"], u["alpha"]
        ys, xs = np.where(al)
        oy, ox = ys.min(), xs.min()
        aw = xs.max() - ox + 1; ah = ys.max() - oy + 1

        def tr(mask):
            c, _d, _k = trazo.trace_layer(mask, eps, min_area, smooth)
            return [([(x - ox, y - oy) for x, y in o],
                     [[(x - ox, y - oy) for x, y in h] for h in hs])
                    for o, hs in c]

        out = []
        if style == "plano":
            for k, col in PLANO:
                m = L.get(k)
                if m is not None and m.any():
                    out.append((tr(m), col))
        elif style == "papel":
            holes = np.zeros_like(al)
            for k in PAPEL_HOLES:
                if k in L: holes |= L[k]
            out.append((tr(al & ~holes), GRANA))
        elif style == "silueta":
            out.append((tr(al), TINTA))
        elif style == "azulejo":
            out.append((tr(al), AZUL))
            edge = np.zeros_like(al)
            from scipy import ndimage
            for k in AZULEJO_EDGE:
                m = L.get(k)
                if m is not None and m.any():
                    edge |= m & ~ndimage.binary_erosion(m, np.ones((3, 3)))
            out.append((tr(edge), CIELO))
        cache[key] = (out, (aw, ah))
    out, art_wh = cache[key]
    s, dx, dy = _fit(None, box, art_wh)
    return [(trazo.to_svg_paths(c, scale=s, dx=dx, dy=dy), col)
            for c, col in out], (art_wh[0] * s, art_wh[1] * s)
