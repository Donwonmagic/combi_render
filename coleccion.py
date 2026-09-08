"""
coleccion.py -- THE COLLECTION.  Six drawn styles across four categories.

THE OWNER'S BRIEF, ASSEMBLED FROM THREE MESSAGES:
  1  *"I simply want a collection of promotional images utilizing the combi.
      Very similar to this sign, but I want to make it special, distinguished
      in a way."*
  2  *"It's not about the palette, it's just an example of a promotional
      product."*   -- so `ref_sign_aframe.jpg` fixes the CATEGORY, not colour.
  3  *"Remember that the model is simply an underlay for the hero of each
      piece.  It should be done in different styles too."*
  and then, asked which of six styles and which of four categories: **ALL.**

He had already rejected `promo.py`'s seven pieces -- *"None of them yet"* --
which is the THIRD revision running that he has rejected an artefact every check
in this tree passed (rev 78 *"Oh god that looks terrible"*, rev 79 *"that's not
a product"*, F366).  `promo.py`'s defect was named by message 3: it PASTED THE
RENDER as the artwork.  Nothing here does.  Every hero is DRAWN by `estilos.py`
over the model as underlay, and the model is asked only where things are (F361).

THE TYPE IS THE VEHICLE'S OWN.  `promo.py` set every wordmark in DejaVu Serif
Bold because this container has no display face and the font CDNs are refused by
the egress proxy.  That ceiling is GONE for display use: the bus carries the
hand-lettered `Señor Tacombi` wordmark, the `100% Calidad` seal, the folk-art
scrollwork and the mural's menu header AS ARTWORK, and F369's within-material
colour key recovers all four.  ⚠ **IT IS NOT GONE FOR BODY COPY**, which is
still DejaVu and Liberation, and that is stated on every sheet.

WHERE EVERY WORD ON THESE PIECES COMES FROM (F372).  The first build of this
module printed a menu with sub-lines -- *"al pastor · carnitas · pollo"*,
*"del día"*, *"a la plancha"* -- under a docstring in `promo.py` claiming the
list was *"read off the vehicle rather than invented"*.  IT WAS INVENTED.  The
sub-lines appear nowhere in the record, the list DROPPED `GOURMET` and REORDERED
`JUICES`, and the claim was a rule-10 violation sitting in a docstring.  Worse,
these are assertions about a REAL BUSINESS'S MENU, and `CONCEPT_BENCH_rev77.md`
already warns *"WE MAY BE SELLING FOOD HE NO LONGER SERVES ... only he can"*.
Every string is now sourced, and the source is PRINTED ON THE PIECE:

  MEDIDO      off the vehicle's own mural lid, `lid_gen.py`'s measured v-fractions:
              GOURMET 0.001-0.041, TACOS 0.105-0.145, TORTAS 0.204-0.244,
              JUICES 0.523-0.555, CEVICHE/TOSTADAS 0.590-0.637, SHRIMP 0.731-0.755;
              top strip FRESH · JUICES · GOURMET TACOS · & · TORTAS
  LETRERO     `TAQUERÍA Y CERVECERÍA` -- read off the owner's OWN photograph,
              `ref_sign_aframe.jpg`.  It is in no other file in this repository.
  AUTORADO    ABIERTO · HECHO A MANO · SE SIRVE DESDE LA COMBI · HORARIO ·
              LA CARTA · TARJETA DE CLIENTE · the loyalty offer.  MINE, not his.

⚠ **NO PIECE HERE STATES A PRICE, AN OPENING TIME, A DATE OR A DISCOUNT AS
FACT.**  The hours card is deliberately BLANK RULES and the menu is marked
`MENÚ DE MUESTRA` on its face.

CEILINGS (rule 12):
  * Screen-scale RGB proofs.  No bleed, no trim, no separation, no spot plates.
    `sheet.py` is the module that emits print masters; nothing here is one.
  * The merch pieces are FLAT ARTWORK, not garment or vessel mock-ups.  There
    is no cloth simulation here and none is implied.
  * One viewpoint per drawing -- `side` (az 90) unless a piece names another.
  * NOTHING IN THIS TREE CAN GRADE ANY OF THESE.  The owner is the instrument,
    and he has now rejected one full round.
"""
import os, sys, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

import estilos
import promo
from promo import (ls_text, ls_width, piece_frame, font, keyline, rule,
                   dotrule, TEXTBOX, OBSTACLE)

OUT = "design_out"
CHECK = [0]; FAILED = []

def ck(cond, msg):
    CHECK[0] += 1
    print(("  ok    " if cond else "  FAIL  ") + msg)
    if not cond: FAILED.append(msg)

# ------------------------------------------------------------------ palette
CREMA = estilos.CREMA; PAPEL = estilos.PAPEL; ROJO = estilos.ROJO
GRANA = estilos.GRANA; ORO = estilos.ORO;     TINTA = estilos.TINTA
AZUL  = estilos.AZUL;  CIELO = estilos.CIELO; HUESO = estilos.HUESO
VERDE = (44, 82, 66)

# MEDIDO off the vehicle's mural lid -- lid_gen.py's own strings, its own order.
MENU_MEDIDO = ("GOURMET TACOS", "TORTAS", "FRESH JUICES",
               "CEVICHE / TOSTADAS", "SHRIMP & FISH")
# LETRERO -- the owner's photograph, ref_sign_aframe.jpg.  Nowhere else in the tree.
LETRERO = "TAQUERÍA Y CERVECERÍA"

# ---------------------------------------------------- the art, computed once
_ART = {}; _MARKS = {}
USED = []      # (piece, style) -- so a style cannot silently drop out

def art(style, tag="side"):
    """A style's hero, rendered ONCE per (style, tag) and reused.

    WHY A CACHE IS NOT AN OPTIMISATION HERE.  Each style costs 8-12 s at ss=3;
    sixteen pieces re-rendering their own would be minutes of identical work and
    would make the sheet's build time scale with the number of pieces rather
    than the number of styles.
    """
    k = (style, tag)
    if k not in _ART:
        fn = dict(estilos.ESTILOS)[style]
        _ART[k] = fn(estilos.underlay(tag), 3)
    return _ART[k]

def marks(tag="side"):
    if tag not in _MARKS: _MARKS[tag] = estilos.marks(tag)
    return _MARKS[tag]

def place(im, style, box, tag="side", anchor="mm"):
    """Drop a style's hero into `box` (x0,y0,x1,y1), preserving aspect."""
    a, _g = art(style, tag)
    USED.append(style)
    x0, y0, x1, y1 = box
    s = min((x1 - x0) / a.width, (y1 - y0) / a.height)
    t = a.resize((max(1, int(a.width * s)), max(1, int(a.height * s))),
                 Image.LANCZOS)
    x = x0 + ((x1 - x0) - t.width) // 2
    y = y0 + ((y1 - y0) - t.height) // 2 if anchor[1] == "m" else y0
    im.paste(t, (x, y), t)
    return (x, y, x + t.width, y + t.height)

_SEAL = {}

def seal(im, height, xy, field_ink, burst_ink, anchor="mt", tag="side"):
    """The seal drawn on BOTH its plates so the knocked-out lettering reads."""
    if tag not in _SEAL: _SEAL[tag] = estilos.seal_pair(tag)
    if _SEAL[tag] is None: return None
    f, b = _SEAL[tag]
    gf = estilos.mark_img(f, height, field_ink)
    gb = estilos.mark_img(b, height, burst_ink)
    g = Image.new("RGBA", gf.size, (0, 0, 0, 0))
    g = Image.alpha_composite(g, gf)
    g = Image.alpha_composite(g, gb.resize(gf.size, Image.LANCZOS))
    x, y = xy
    if anchor[0] == "m": x -= g.width // 2
    elif anchor[0] == "r": x -= g.width
    if anchor[1] == "m": y -= g.height // 2
    elif anchor[1] == "b": y -= g.height
    im.paste(g, (int(x), int(y)), g)
    return (int(x), int(y), int(x) + g.width, int(y) + g.height)


def mark(im, name, height, xy, ink, anchor="mt", tag="side"):
    M = marks(tag)
    if name not in M: return None
    g = estilos.mark_img(M[name], height, ink)
    x, y = xy
    if anchor[0] == "m": x -= g.width // 2
    elif anchor[0] == "r": x -= g.width
    if anchor[1] == "m": y -= g.height // 2
    elif anchor[1] == "b": y -= g.height
    im.paste(g, (int(x), int(y)), g)
    return (int(x), int(y), int(x) + g.width, int(y) + g.height)

def obstacle(piece, label, box):
    OBSTACLE.append((piece, label, box[0], box[1], box[2], box[3]))

PROV = "TEXTO: MEDIDO DEL VEHÍCULO · LETRERO DEL DUEÑO · RESTO AUTORADO"

def colophon(d, cx, y, txt, ink, px=19, anchor="mt", prov=True):
    """⚠ THIS TOOK A PAGE WIDTH AND HALVED IT.  Two call sites passed the
    CENTRE they wanted instead, so their colophon printed at half that x --
    `merch_vaso`'s landed on top of the hero.  The collision check caught it.
    It now takes the centre, which is what every call site was trying to say."""
    ls_text(d, (cx, y), txt, font("cond", px), ink, ls=px * 0.16, anchor=anchor)
    if prov:
        # ⚠ ON THE ARTEFACT, NOT IN THE LOG.  "It is printed on the artefact"
        # was FALSE for two revisions running (rev 78 §8 item 9, rev 79 §8
        # item 2) and these 20 PNGs shipped with no provenance mark at all.
        ls_text(d, (cx, y + px + 7), PROV, font("cond", int(px * 0.74)), ink,
                ls=px * 0.10, anchor=anchor)

# ================================================================= CALLE
# Street and in-store: what a person sees standing in front of the place.

def calle_aframe(p):
    W, H = 1200, 1800; piece_frame(p, (60, 60, W - 60, H - 60))
    im = Image.new("RGB", (W, H), ORO); d = ImageDraw.Draw(im)
    keyline(d, (0, 0, W - 1, H - 1), TINTA, w=7, inset=36)
    mark(im, "wordmark", 190, (W // 2, 130), TINTA, "mt")
    rule(d, 170, W - 170, 380, GRANA, 7)
    ls_text(d, (W // 2, 408), "TAQUERÍA   Y   CERVECERÍA", font("sansb", 34),
            GRANA, ls=13, anchor="mt")
    obstacle(p, "hero", place(im, "plano", (90, 560, W - 90, 1240)))
    rule(d, 170, W - 170, 1330, GRANA, 7)
    ls_text(d, (W // 2, 1370), "FRESH JUICES · GOURMET TACOS · TORTAS",
            font("sansb", 31), TINTA, ls=7, anchor="mt")
    seal(im, 210, (W // 2, 1450), CREMA, GRANA, "mt")
    colophon(d, W // 2, 1670, "SERIE COMBI · CALLE I · ESTILO PLANO", TINTA)
    return im

def calle_carta(p):
    W, H = 1200, 1700; piece_frame(p, (56, 56, W - 56, H - 56))
    im = Image.new("RGB", (W, H), CREMA); d = ImageDraw.Draw(im)
    d.rectangle([32, 32, W - 32, 330], fill=GRANA)
    keyline(d, (0, 0, W - 1, H - 1), TINTA, w=5, inset=32)
    obstacle(p, "mural", mark(im, "mural", 250, (W // 2, 56), ORO, "mt") or
             (0, 0, 0, 0))
    obstacle(p, "hero", place(im, "papel", (150, 360, W - 150, 700)))
    # MEDIDO.  These are the mural lid's OWN strings at lid_gen.py's measured
    # v-fractions, in its own order.  The first build invented a second line
    # under each and dropped GOURMET; both are gone (F372).
    y = 800
    for name in MENU_MEDIDO:
        ls_text(d, (110, y), name, font("disp", 44), TINTA, ls=3)
        dotrule(d, 110, W - 110, y + 78, ORO, r=3, gap=16)
        y += 128
    ls_text(d, (W // 2, 1512), "MENÚ DE MUESTRA · TOMADO DEL MURAL DEL VEHÍCULO",
            font("cond", 21), GRANA, ls=4, anchor="mt")
    colophon(d, W // 2, 1574, "SERIE COMBI · CALLE II · ESTILO PAPEL PICADO", TINTA)
    return im

def calle_vidriera(p):
    W, H = 1500, 950; piece_frame(p, (54, 54, W - 54, H - 54))
    im = Image.new("RGB", (W, H), AZUL); d = ImageDraw.Draw(im)
    keyline(d, (0, 0, W - 1, H - 1), CIELO, w=4, inset=30)
    obstacle(p, "hero", place(im, "azulejo", (560, 80, W - 60, H - 130)))
    mark(im, "wordmark", 120, (80, 200), HUESO, "lt")
    rule(d, 82, 400, 370, ROJO, 6)
    ls_text(d, (82, 405), "TAQUERÍA", font("sansb", 30), CIELO, ls=11)
    ls_text(d, (82, 452), "CERVECERÍA", font("sansb", 30), CIELO, ls=11)
    ls_text(d, (82, 560), "ABIERTO", font("disp", 62), HUESO, ls=6)
    colophon(d, W // 2, 816, "SERIE COMBI · CALLE III · ESTILO AZULEJO", CIELO)
    return im

def calle_horario(p):
    W, H = 950, 1250; piece_frame(p, (52, 52, W - 52, H - 52))
    im = Image.new("RGB", (W, H), CREMA); d = ImageDraw.Draw(im)
    keyline(d, (0, 0, W - 1, H - 1), GRANA, w=5, inset=30)
    mark(im, "wordmark", 108, (W // 2, 92), GRANA, "mt")
    obstacle(p, "hero", place(im, "sello", (80, 230, W - 80, 560)))
    ls_text(d, (W // 2, 620), "HORARIO", font("disp", 62), TINTA, ls=14,
            anchor="mt")
    dotrule(d, 130, W - 130, 720, ORO, r=4, gap=20)
    # ⚠ THE HOURS ARE BLANK ON PURPOSE.  Inventing opening times would be a
    # fabricated claim on a promotional piece; the rules are for him to fill.
    for i, day in enumerate(("LUNES A JUEVES", "VIERNES", "SÁBADO", "DOMINGO")):
        y = 770 + i * 92
        ls_text(d, (120, y), day, font("sansb", 27), TINTA, ls=6)
        rule(d, 560, W - 120, y + 26, (196, 186, 166), 3)
    colophon(d, W // 2, 1126, "SERIE COMBI · CALLE IV · ESTILO SELLO", TINTA)
    return im

# ================================================================ SOCIAL
def social_cuadro(p):
    W = H = 1400; piece_frame(p, (60, 60, W - 60, H - 60))
    im = Image.new("RGB", (W, H), HUESO); d = ImageDraw.Draw(im)
    keyline(d, (0, 0, W - 1, H - 1), AZUL, w=5, inset=38)
    obstacle(p, "hero", place(im, "riso", (100, 330, W - 100, 1010)))
    mark(im, "wordmark", 165, (W // 2, 130), ROJO, "mt")
    ls_text(d, (W // 2, 1090), "TAQUERÍA   Y   CERVECERÍA",
            font("sansb", 33), AZUL, ls=14, anchor="mt")
    seal(im, 150, (W // 2, 1150), HUESO, ROJO, "mt")
    colophon(d, W // 2, 1276, "SERIE COMBI · SOCIAL I · ESTILO RISO", AZUL)
    return im

def social_historia(p):
    W, H = 1080, 1920; piece_frame(p, (56, 56, W - 56, H - 56))
    im = Image.new("RGB", (W, H), ORO); d = ImageDraw.Draw(im)
    keyline(d, (0, 0, W - 1, H - 1), GRANA, w=5, inset=34)
    mark(im, "wordmark", 175, (W // 2, 210), GRANA, "mt")
    obstacle(p, "hero", place(im, "papel", (70, 640, W - 70, 1180)))
    ls_text(d, (W // 2, 1290), "ABIERTO", font("disp", 122), GRANA, ls=18,
            anchor="mt")
    dotrule(d, 190, W - 190, 1470, GRANA, r=5, gap=26)
    ls_text(d, (W // 2, 1520), "TAQUERÍA   Y   CERVECERÍA",
            font("sansb", 32), TINTA, ls=13, anchor="mt")
    obstacle(p, "scroll", mark(im, "scroll", 168, (W // 2, 1596), GRANA, "mt")
             or (0, 0, 0, 0))
    colophon(d, W // 2, 1794, "SERIE COMBI · SOCIAL II · ESTILO PAPEL PICADO", TINTA)
    return im

def social_cabecera(p):
    W, H = 2100, 700; piece_frame(p, (48, 48, W - 48, H - 48))
    im = Image.new("RGB", (W, H), AZUL); d = ImageDraw.Draw(im)
    keyline(d, (0, 0, W - 1, H - 1), CREMA, w=4, inset=26)
    obstacle(p, "hero", place(im, "plano", (1010, 60, W - 70, H - 60)))
    mark(im, "wordmark", 150, (110, 200), CREMA, "lt")
    rule(d, 112, 860, 400, ROJO, 6)
    ls_text(d, (112, 432), "TAQUERÍA  ·  CERVECERÍA", font("sansb", 31),
            CREMA, ls=12)
    ls_text(d, (112, 494), "FRESH JUICES · GOURMET TACOS · TORTAS",
            font("sans", 25), CIELO, ls=5)
    colophon(d, 112, 562, "SERIE COMBI · SOCIAL III · ESTILO PLANO",
             CIELO, 18, anchor="lt")
    return im

# =============================================================== IMPRESO
def impreso_cartel(p):
    W, H = 1400, 2000; piece_frame(p, (66, 66, W - 66, H - 66))
    im = Image.new("RGB", (W, H), AZUL); d = ImageDraw.Draw(im)
    keyline(d, (0, 0, W - 1, H - 1), CIELO, w=4, inset=44)
    mark(im, "wordmark", 200, (W // 2, 150), HUESO, "mt")
    rule(d, 210, W - 210, 420, ROJO, 7)
    obstacle(p, "hero", place(im, "azulejo", (90, 540, W - 90, 1400)))
    ls_text(d, (W // 2, 1500), "TAQUERÍA   Y   CERVECERÍA",
            font("sansb", 37), HUESO, ls=16, anchor="mt")
    ls_text(d, (W // 2, 1580), "SE  SIRVE  DESDE  LA  COMBI",
            font("sans", 29), CIELO, ls=10, anchor="mt")
    obstacle(p, "seal", seal(im, 190, (W // 2, 1660), HUESO, ROJO, "mt")
             or (0, 0, 0, 0))
    colophon(d, W // 2, 1858, "SERIE COMBI · IMPRESO I · ESTILO AZULEJO", CIELO)
    return im

def impreso_postal(p):
    W, H = 1500, 1000; piece_frame(p, (52, 52, W - 52, H - 52))
    im = Image.new("RGB", (W, H), PAPEL); d = ImageDraw.Draw(im)
    keyline(d, (0, 0, W - 1, H - 1), TINTA, w=4, inset=30)
    obstacle(p, "hero", place(im, "linea", (90, 130, W - 90, 660)))
    dotrule(d, 150, W - 150, 720, ORO, r=4, gap=20)
    mark(im, "wordmark", 95, (W // 2, 748), TINTA, "mt")
    ls_text(d, (W // 2, 858), LETRERO, font("sansb", 25), GRANA, ls=11,
            anchor="mt")
    colophon(d, W // 2, 898, "IMPRESO II · ESTILO LÍNEA", TINTA, 15)
    return im

def impreso_lealtad(p):
    W, H = 1100, 680; piece_frame(p, (44, 44, W - 44, H - 44))
    im = Image.new("RGB", (W, H), CREMA); d = ImageDraw.Draw(im)
    keyline(d, (0, 0, W - 1, H - 1), GRANA, w=4, inset=26)
    obstacle(p, "hero", place(im, "sello", (60, 70, 640, 400)))
    mark(im, "wordmark", 78, (700, 110), GRANA, "lt")
    ls_text(d, (700, 220), "TARJETA", font("sansb", 26), TINTA, ls=9)
    ls_text(d, (700, 262), "DE  CLIENTE", font("sansb", 26), TINTA, ls=9)
    for i in range(8):
        cx = 108 + (i % 8) * 118
        d.ellipse([cx - 32, 446, cx + 32, 510], outline=GRANA, width=4)
    ls_text(d, (W // 2, 530), "OCHO  VISITAS  ·  LA  NOVENA  ES  NUESTRA",
            font("sansb", 20), GRANA, ls=6, anchor="mt")
    ls_text(d, (W // 2, 560), "OFERTA DE MUESTRA · NO APROBADA", font("cond", 16),
            (150, 128, 120), ls=3, anchor="mt")
    colophon(d, W // 2, 594, "IMPRESO III · ESTILO SELLO", TINTA, 14)
    return im

def impreso_volante(p):
    W, H = 1240, 1750; piece_frame(p, (56, 56, W - 56, H - 56))
    im = Image.new("RGB", (W, H), HUESO); d = ImageDraw.Draw(im)
    keyline(d, (0, 0, W - 1, H - 1), ROJO, w=5, inset=34)
    mark(im, "wordmark", 160, (W // 2, 120), ROJO, "mt")
    obstacle(p, "hero", place(im, "riso", (80, 400, W - 80, 1000)))
    rule(d, 160, W - 160, 1080, AZUL, 5)
    for i, it in enumerate(MENU_MEDIDO):
        ls_text(d, (W // 2, 1128 + i * 68), it, font("disp", 34), AZUL,
                ls=4, anchor="mt")
    ls_text(d, (W // 2, 1490), "MENÚ DE MUESTRA", font("cond", 21), ROJO,
            ls=5, anchor="mt")
    colophon(d, W // 2, 1618, "SERIE COMBI · IMPRESO IV · ESTILO RISO", AZUL)
    return im

# ============================================================= MERCANCIA
# ⚠ FLAT ARTWORK, NOT MOCK-UPS.  There is no cloth or vessel simulation here.

def merch_playera(p):
    W = H = 1250; piece_frame(p, (58, 58, W - 58, H - 58))
    im = Image.new("RGB", (W, H), (28, 30, 34)); d = ImageDraw.Draw(im)
    obstacle(p, "hero", place(im, "sello", (110, 300, W - 110, 780)))
    mark(im, "wordmark", 150, (W // 2, 120), CREMA, "mt")
    ls_text(d, (W // 2, 850), "TAQUERÍA   Y   CERVECERÍA",
            font("sansb", 30), ORO, ls=14, anchor="mt")
    # The scroll ornament was tried here and DROPPED: it is a FRAGMENT of a
    # flank-length design, and on a dark ground at any size that fits the piece
    # it reads as a smudge rather than as ornament.  It stays on `bolsa` and
    # `historia`, where the ground is light and it holds together.
    obstacle(p, "seal", seal(im, 150, (W // 2, 930), (44, 46, 50), ORO, "mt")
             or (0, 0, 0, 0))
    colophon(d, W // 2, 1118, "MERCANCÍA I · ARTE PLANO PARA PLAYERA · ESTILO SELLO",
             (150, 150, 150), 17)
    return im

def merch_bolsa(p):
    W, H = 1250, 1450; piece_frame(p, (58, 58, W - 58, H - 58))
    im = Image.new("RGB", (W, H), (222, 210, 184)); d = ImageDraw.Draw(im)
    obstacle(p, "hero", place(im, "papel", (90, 380, W - 90, 900)))
    mark(im, "wordmark", 165, (W // 2, 150), GRANA, "mt")
    dotrule(d, 200, W - 200, 340, GRANA, r=5, gap=24)
    ls_text(d, (W // 2, 960), "HECHO   A   MANO", font("disp", 52), GRANA,
            ls=12, anchor="mt")
    ls_text(d, (W // 2, 1050), "TAQUERÍA   Y   CERVECERÍA",
            font("sansb", 28), TINTA, ls=12, anchor="mt")
    colophon(d, W // 2, 1318, "MERCANCÍA II · ARTE PARA BOLSA · ESTILO PAPEL PICADO",
             TINTA, 17)
    return im

def merch_vaso(p):
    W, H = 1900, 720; piece_frame(p, (44, 44, W - 44, H - 44))
    im = Image.new("RGB", (W, H), CREMA); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 60], fill=GRANA); d.rectangle([0, H - 60, W, H],
                                                        fill=GRANA)
    obstacle(p, "hero", place(im, "linea", (60, 110, 900, 610)))
    mark(im, "wordmark", 120, (1030, 210), GRANA, "lt")
    ls_text(d, (1030, 360), "TAQUERÍA · CERVECERÍA", font("sansb", 24),
            TINTA, ls=6)
    obstacle(p, "seal", seal(im, 160, (1745, 260), CREMA, GRANA, "mm")
             or (0, 0, 0, 0))
    ls_text(d, (1030, 430), "FRESH JUICES · GOURMET TACOS · TORTAS",
            font("sans", 22), GRANA, ls=4)
    colophon(d, 1420, 570, "MERCANCÍA III · DESARROLLO DE VASO · ESTILO LÍNEA",
             TINTA, 16)
    return im

def merch_chapa(p):
    W = H = 980; piece_frame(p, (60, 60, W - 60, H - 60))
    im = Image.new("RGB", (W, H), PAPEL); d = ImageDraw.Draw(im)
    d.ellipse([40, 30, W - 40, H - 170], fill=ORO, outline=TINTA, width=6)
    d.ellipse([72, 62, W - 72, H - 202], outline=GRANA, width=3)
    # ⚠ THE OBSTACLE IS THE RIM, NOT THE DISC.  Declaring the whole disc redded
    # the strapline, which BELONGS on the badge face -- an over-broad guard that
    # forbids the correct layout is a false positive, and a check nobody can
    # satisfy gets deleted.  The defect that actually shipped was the colophon
    # printing ACROSS the bottom rim, so that band is what is guarded.
    obstacle(p, "badge rim", (40, H - 170 - 22, W - 40, H - 170 + 22))
    obstacle(p, "hero", place(im, "plano", (150, 300, W - 150, 545)))
    mark(im, "wordmark", 98, (W // 2, 150), GRANA, "mt")
    ls_text(d, (W // 2, 596), LETRERO, font("sansb", 22),
            GRANA, ls=8, anchor="mt")
    # ABLATION: T1_COL_BADGE=1 puts the colophon back on the rim, so the rim
    # guard can be WATCHED FAILING on the defect it was written for (rule 3).
    cy = (H - 170) if os.environ.get("T1_COL_BADGE") == "1" else 858
    colophon(d, W // 2, cy, "MERCANCÍA IV · CHAPA · ESTILO PLANO", TINTA, 16)
    return im

PIEZAS = [
 ("calle",     "aframe",     calle_aframe),
 ("calle",     "carta",      calle_carta),
 ("calle",     "vidriera",   calle_vidriera),
 ("calle",     "horario",    calle_horario),
 ("social",    "cuadro",     social_cuadro),
 ("social",    "historia",   social_historia),
 ("social",    "cabecera",   social_cabecera),
 ("impreso",   "cartel",     impreso_cartel),
 ("impreso",   "postal",     impreso_postal),
 ("impreso",   "lealtad",    impreso_lealtad),
 ("impreso",   "volante",    impreso_volante),
 ("mercancia", "playera",    merch_playera),
 ("mercancia", "bolsa",      merch_bolsa),
 ("mercancia", "vaso",       merch_vaso),
 ("mercancia", "chapa",      merch_chapa),
]

# ============================================================== the sheets
def contact(items, path, cols, cell, bg=(250, 249, 246)):
    rows = (len(items) + cols - 1) // cols
    pad = 26
    W = cols * cell + pad * (cols + 1)
    H = rows * cell + pad * (rows + 1) + 26
    sh = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(sh)
    for i, (name, im) in enumerate(items):
        r, c = divmod(i, cols)
        x = pad + c * (cell + pad); y = pad + r * (cell + pad)
        s = min(cell / im.width, cell / im.height)
        t = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))),
                      Image.LANCZOS)
        sh.paste(t, (x + (cell - t.width) // 2, y + (cell - t.height) // 2))
        d.text((x, y + cell + 3), name, fill=(70, 64, 58), font=font("sans", 18))
    sh.save(path); return sh

def main(argv):
    global OUT
    only = None
    for i, a in enumerate(argv):
        if a == "--only": only = argv[i + 1]
        if a == "--out":  OUT = argv[i + 1]
    os.makedirs(OUT, exist_ok=True)
    print("coleccion.py -- six drawn styles across four categories")

    M = marks()
    for k in ("wordmark", "seal", "scroll", "mural"):
        ck(k in M and M[k].any(),
           "mark %-10s recovered from the vehicle, %s"
           % (k, M[k].shape if k in M else "ABSENT"))

    made = {}
    for cat, name, fn in PIEZAS:
        if only and only not in (cat, "%s_%s" % (cat, name)): continue
        p = os.path.join(OUT, "col_r80_%s_%s.png" % (cat, name))
        im = fn("%s_%s" % (cat, name))
        im.save(p)
        made.setdefault(cat, []).append((name, im))
        a = np.asarray(im.convert("RGB")).reshape(-1, 3)
        ck(len(np.unique(a[::53], axis=0)) > 150,
           "%-20s %4dx%-4d written, %d distinct colours sampled"
           % ("%s/%s" % (cat, name), im.width, im.height,
              len(np.unique(a[::53], axis=0))))

    # --- the two layout instruments, inherited from promo.py ---------------
    bad = [(pc, t, int(x0), int(y0), int(x1), int(y1), sf)
           for pc, t, x0, y0, x1, y1, sf in TEXTBOX
           if x0 < sf[0] or y0 < sf[1] or x1 > sf[2] or y1 > sf[3]]
    for b in bad:
        print("       OVERFLOW %s: %r box=(%d,%d,%d,%d) safe=%s"
              % (b[0], b[1][:32], b[2], b[3], b[4], b[5], b[6]))
    ck(not bad, "every text run (%d) inside its piece's safe area; %d overflow"
       % (len(TEXTBOX), len(bad)))

    hit = []
    for pc, t, x0, y0, x1, y1, sf in TEXTBOX:
        for op, lab, ox0, oy0, ox1, oy1 in OBSTACLE:
            if op != pc: continue
            if x0 < ox1 and x1 > ox0 and y0 < oy1 and y1 > oy0:
                hit.append((pc, t, lab))
    for h in hit:
        print("       COLLISION %s: %r crosses the %s" % (h[0], h[1][:32], h[2]))
    ck(not hit, "no text run crosses artwork (%d obstacles); %d collision"
       % (len(OBSTACLE), len(hit)))

    # THE TEXT-vs-TEXT CHECK.  The first two instruments compare type to the
    # FRAME and to the ARTWORK; neither compares type to OTHER TYPE.  Switching
    # to real faces changed every metric at once and two pieces -- impreso/postal
    # and impreso/lealtad -- shipped their colophon printed THROUGH another line,
    # illegibly, with all twenty-seven checks green.  Watched failing on exactly
    # those two before either layout was touched.
    over = []
    for i in range(len(TEXTBOX)):
        pc, t1, a0, b0, a1, b1, _ = TEXTBOX[i]
        for j in range(i + 1, len(TEXTBOX)):
            qc, t2, c0, d0, c1, d1, _ = TEXTBOX[j]
            if qc != pc: continue
            ox = min(a1, c1) - max(a0, c0)
            oy = min(b1, d1) - max(b0, d0)
            if ox > 2 and oy > 2:
                over.append((pc, t1, t2, int(ox), int(oy)))
    for o in over:
        print("       TEXT-ON-TEXT %s: %r over %r (%dx%d px)"
              % (o[0], o[1][:24], o[2][:24], o[3], o[4]))
    ck(not over, "no two text runs overlap (%d runs); %d overlap"
       % (len(TEXTBOX), len(over)))

    if not only:
        want = set(n for n, _ in estilos.ESTILOS)
        got = set(USED)
        ck(want == got, "all six styles appear in the collection; missing %s"
           % (sorted(want - got) or "none"))
        for cat, items in made.items():
            cp = os.path.join(OUT, "col_r80_HOJA_%s.png" % cat)
            contact(items, cp, cols=min(4, len(items)), cell=620)
            ck(os.path.exists(cp), "contact sheet %-10s -> %s" % (cat, cp))
        allit = [(("%s/%s" % (c, n)), im) for c, its in made.items()
                 for n, im in its]
        ap = os.path.join(OUT, "col_r80_HOJA_TODO.png")
        contact(allit, ap, cols=5, cell=480)
        ck(os.path.exists(ap), "master sheet -> %s" % ap)

    print("%d checked, %d FAILED" % (CHECK[0], len(FAILED)))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
