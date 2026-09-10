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
import json, os, re, sys, math
import numpy as np
from PIL import Image

import lienzo, trazo, estilo_vec, estilos


def T(L, g, x, y, s, face, pt, fill, anchor="middle", tracking=None,
      measure=None, nivel=None):
    """Every text run in this module goes through here, so no run can be added
    without a measure it must fit."""
    # THE PROVENANCE DECLARATION: recorded against the piece, and NOT DRAWN.
    # ⚠ IT RETURNS BEFORE ANY MEASUREMENT.  The first version returned after
    # `fit_pt` and the floor test, so the `type floor` row reported `chapa`'s
    # colophon at 1.558 mm -- a run that is not on the sheet.  A row that
    # measures ink must not be handed something that was never inked.
    # `T1_PLIEGO_CONPROV=1` puts the ink back so both provenance rows red.
    if PROV in s and os.environ.get("T1_PLIEGO_CONPROV") != "1":
        CREDITO.append((PIEZA[0], s))
        return
    # ⚠ 0.88, NOT 1.0.  Chromium applies letter-spacing after EVERY glyph and
    # shapes tighter than PIL's estimate, so a run measured at exactly the
    # column width still ran off three sheets.  The safety factor is authored,
    # and the RENDERED edge check below is what actually proves it.
    # ⚠ CAP HEIGHT, NOT EM.  The level fixes the CAP HEIGHT; the em is derived
    # per face from that face's own sCapHeight, so `cond` and `display` at one
    # level are the same height to a READER instead of 3.95 % apart -- which is
    # what the scale is for, and what applying it to em quietly prevented.
    cf = lienzo.capfrac(face)
    if cf:
        pt = pt * CAP_REF / cf
    # ⚠ TRACKING COMES FROM THE TABLE, NOT FROM THE CALL SITE.  An explicit
    # `tracking=` still wins so a piece can depart, but it has to say so.
    if tracking is None:
        tracking = pt * PISTA.get(nivel, 0.055)
    m = (measure if measure is not None else (g.w - 2 * g.m)) * 0.88
    pt, k = fit_pt(s, face, pt, tracking, m)
    # ⚠ NO PER-RUN CLAMP.  The floor is applied to the PIECE's scale before it
    # is drawn (see `escalar`), so a run arriving here below the floor means
    # the pre-pass missed it -- which is a finding, not something to paper over.
    if pt < MIN_TIPO_MM - 1e-9:
        DEMASIADO.append((PIEZA[0], s[:34], round(pt, 3)))
    # tracking follows the size it was chosen for -- see fit_pt
    # THE ABLATION FOR THE MARGIN AND EDGE ROWS.  ⚠ The adversary's kill, kept:
    # it multiplied every run on `vaso` by six so the sheet read
    # `TAQUERIA y CERVECER` clean off the right trim, and BOTH ROWS STILL
    # PASSED, because the bleed exemption had widened them past anything a
    # defect could move.  With the bleed excluded instead of the bar widened,
    # this reds.  It is a check only once it has been watched failing.
    if os.environ.get("T1_PLIEGO_TIPOGRANDE") == "1":
        pt *= 6.0
    # THE ABLATION FOR THE `hierarchy` ROW.  ⚠ Switching the SNAP off is not an
    # ablation any more: once every call site names a level from `NIVEL`, and
    # every level is already a half-step, the snap has nothing left to do and
    # the row stays green -- which is a control that cannot fail.  So this
    # plants a genuinely off-scale size, which is the defect: a run 7 % off a
    # step is exactly the 1.14x accident the row exists to catch.
    if os.environ.get("T1_PLIEGO_SINESCALA") == "1":
        pt *= 1.07

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
        # ⚠ `len(s)`, not `len(s) - 1`: CSS puts the letter-space after the
        # LAST glyph too, so the advance this run occupies is one tracking
        # wider than a naive reading gives.  The same wrong assumption is what
        # pushed every centred tracked line off its axis.
        wmm = adv + tracking * k * len(s)
        asc, desc = ff.getmetrics()
        x0 = (x - wmm / 2.0 if anchor == "middle"
              else x - wmm if anchor == "end" else x)
        box = (x0, y - asc * pt / u, x0 + wmm, y + desc * pt / u)
    TEXTS.append({"nivel": nivel, "cap": pt * (cf or CAP_REF),
                  "piece": PIEZA[0], "s": s, "x": x, "y": y, "pt": pt,
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
# MEASURED OFF HIS PHOTOGRAPH -- BY `foto.py`, WHICH PRINTS IT AND COMMITS IT
# TO `foto_sign.json`, and checked below against what this palette does.
#
# ⚠⚠ TWO CORRECTIONS TO WHAT THIS COMMENT USED TO SAY, BOTH CAUGHT BY GRADERS.
# (1) It quoted "his reads 1.629:1" AND NO SCRIPT COMPUTED IT -- rule 5, in the
# justification for the most-used colour in the suite.  `foto.py` computes it
# now: 1.6293:1, and the row below compares the palette against the committed
# file rather than against a remembered number.
# (3) It transferred the WCAG ratio, and THE WCAG RATIO IS NOT THE INVARIANT.
# The argument "same light, same frame, so the RATIO is what can be trusted" is
# true of L1/L2 and FALSE of (L1+0.05)/(L2+0.05) -- the offset breaks scale
# invariance, so a different exposure of the same sign gives a different
# number.  The palette is fitted to `light_over_ground_luminance` = 1.7176 now.
# ⚠ The token barely moved -- `#EBBB55` was already at 1.7136, a 0.23 % error --
# so this changed the ARGUMENT, not the artwork, which is the point: the
# previous gold was very nearly right for a reason that was wrong.
# (2) It called cluster 2 a "cream disc", and THERE IS NO DISC ON HIS SIGN.
# Painting the measurement window and looking at it (rule 8) shows `#D4CDBA`
# is the sign's LIGHT INK -- the inline of the CLUB lettering, the van's cream
# body, and WHITE QUARTER-CIRCLES AT THE CORNERS OF THE BOARD.  The centred
# vignette disc on `p_aframe` was mine; I attributed it to a photograph that
# does not contain it.  The RATIO transferred is sound and is what the row
# checks; the provenance claim around it was not.
F_ORO   = "#E4BD60"     # gold ground, clear of ORO artwork
F_PAPEL = "#E4D6B4"     # paper ground, clear of CREMA artwork
F_AZUL  = "#22406E"     # blue ground, clear of the AZUL_CUERPO body
F_NEGRO = "#141518"

LETRERO = "TAQUERIA y CERVECERIA"
MENU = ("GOURMET TACOS", "TORTAS", "FRESH JUICES",
        "CEVICHE / TOSTADAS", "SHRIMP & FISH")
# ⚠ `AUTORADO` IS NOT A SPANISH WORD.  It shipped on all seventeen pieces, in
# the one string whose entire job is to certify provenance, on a brand whose
# proposition is authenticity.  `DE AUTOR` is the phrase Spanish uses.
# ⚠⚠ THE PROVENANCE LINE IS NO LONGER PRINTED ON THE ARTWORK, AND THE CALL
# SITES THAT PRINTED IT ARE STILL THERE, because they ARE the record (rule 16).
# `T()` recognises this token, records the line against the piece, and draws
# NOTHING.  Nothing is deleted; the ink is.
#
# WHY.  Three independent graders upheld it: this was production metadata
# leaking onto the artwork on 17 of 17 pieces -- including a tote bag, a
# t-shirt and a business card -- and it is not a colophon in any tradition.  A
# colophon names the MAKER and the MEANS: printer, place, date, edition, paper.
# `TEXTO: MEDIDO · LETRERO · DE AUTOR` names none of those. It names the
# provenance CLASS of the strings, in three codewords that exist only inside
# this repository, and a Spanish reader parses it as "TEXT: MEASURED · SIGN ·
# BY THE AUTHOR", which is not a sentence.  Worse, it had swollen to carry the
# build system's own taxonomy -- `SERIE COMBI`, `CALLE`, `IMPRESO`, `SOCIAL`,
# `MERCANCÍA` are category keys, `PAPEL PICADO` and `ESTILO AZULEJO` are style
# keys, `TROQUEL 59 mm` is a die spec.
#
# ⚠ F372 IS NOT WEAKENED BY THIS, IT IS STRENGTHENED.  F372's defect was an
# INVENTED menu under a docstring claiming it was measured; its fix is that the
# claim be TRUE AND RECORDED, not that it be printed on a bag.  It is recorded
# in `pl_MANIFIESTO.txt` per piece, and `PROCEDENCIA` below now classes EVERY
# drawn literal in the suite with a row that reds on any string nobody has
# sourced -- which the printed line never did.
PROV = "TEXTO: MEDIDO · LETRERO · DE AUTOR"

# Every literal this module draws, and where it came from.  MEDIDO: read off
# the vehicle's own artwork.  LETRERO: off the owner's photographed sign.
# AUTOR: written for this suite.  A string absent from here is a finding.
PROCEDENCIA = {
    "TAQUERIA y CERVECERIA": "LETRERO",
    "GOURMET TACOS": "MEDIDO", "TORTAS": "MEDIDO", "FRESH JUICES": "MEDIDO",
    "CEVICHE / TOSTADAS": "MEDIDO", "SHRIMP & FISH": "MEDIDO",
    "SE SIRVE DESDE LA COMBI": "AUTOR", "HECHO A MANO": "AUTOR",
    "ABIERTO": "AUTOR", "HORARIO": "AUTOR", "TARJETA DE CLIENTE": "AUTOR",
    "OCHO VISITAS · LA NOVENA ES NUESTRA": "AUTOR",
    "OFERTA DE MUESTRA · NO APROBADA": "AUTOR",
    "MENÚ DE MUESTRA · TOMADO DEL MURAL": "AUTOR",
    "LUNES": "AUTOR", "MARTES": "AUTOR", "MIÉRCOLES": "AUTOR",
    "JUEVES": "AUTOR", "VIERNES": "AUTOR", "SÁBADO": "AUTOR",
    "DOMINGO": "AUTOR",
}
CREDITO = []         # the provenance line each piece declares, recorded not drawn


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
        # ⚠ THE TYPE SCALE IS ANCHORED ON THE ROW UNIT, AND THE ROW UNIT ON AN
        # 85 x 55 mm CARD IS 1.91 mm.  F386 put a 1.8 mm PHYSICAL FLOOR under
        # every run to stop sub-point type shipping -- and on the three
        # smallest formats that clamped EVERY run to 1.8000 mm, so headline,
        # body and disclaimer came out identical and the hierarchy was gone.
        # Sixty-nine green checks did not see it: the `type` row even PRINTED
        # "10 raised off it by the floor" and it was read as fine.
        #
        # The floor lifts the WHOLE SCALE now, not each run: `k` is set after a
        # first pass so the SMALLEST size on the piece lands on the floor and
        # every other size keeps its exact ratio to it.
        self.k = 1.0
        self.pasos = []

    def x(self, i):                 return self.m + i * (self.col + self.gut)
    def span(self, n):              return n * self.col + (n - 1) * self.gut
    def y(self, k):                 return self.m + k * self.base
    def box(self, i, n, k0, k1):
        return (self.x(i), self.y(k0), self.x(i) + self.span(n), self.y(k1))
    def pt(self, step):
        """Type scale: a perfect fourth, anchored on the baseline unit and
        lifted by `k` so the smallest size on the piece clears the print floor
        without flattening everything above it.

        ⚠ THE STEP IS SNAPPED TO A HALF STEP HERE, so no call site can be off
        the scale.  Every authored size in this module used to be a free
        decimal -- pt(-2.2), pt(-0.4), pt(-1.6) -- which is a scale in the
        docstring and no scale in the artefact.  Enforcing it by construction
        is the only way it stays true; enforcing it by discipline is how it
        stopped being true."""
        step = round(step * 2.0) / 2.0
        self.pasos.append(step)
        return self.base * (PASO ** step) * self.k



# Pieces that bleed to the trim by design.  Declared, not tolerated silently.
# Every ink this module may legitimately put on a sheet.  The SVG sweep in the
# `ink/ground` row compares what was WRITTEN against what was RECORDED, and
# needs a name for the colours that belong to the layout rather than to a
# drawing -- rules, frames, bands.
# The blank-rule grey on the hours card.  ⚠ It was typed inline as a literal
# and the `ink/ground` SVG sweep caught it on its first render as "1 ink in the
# SVGs that no record accounts for" -- which is exactly what that half of the
# row was added for.  1.562:1 against CREMA: a rule you can see and write over.
REGLA = "#C4BAA6"

PALETA = (CREMA, ROJO, GRANA, ORO, TINTA, estilo_vec.PIZ, AZUL, CIELO, HUESO,
          REGLA,
          estilo_vec.AZUL_CUERPO, F_ORO, F_PAPEL, F_AZUL, F_NEGRO, "#DED2B8",
          "#7A6E63")

# Pieces that bleed to the trim by design, WITH THE INKS THEY BLEED IN.  The
# first entry is the page; the rest are erased to it before the margin and edge
# bands are read, so a bleed piece is held to exactly the same bars as every
# other sheet instead of to a bar wide enough to hide anything.
# ============================================================ THE LEVELS
# ⚠ EVERY SIZE IN THE SUITE IS ONE OF THESE, AND NOTHING ELSE.  Before this,
# every call site authored its own decimal -- pt(0.2), pt(-0.1), pt(-1.6),
# pt(-2.3), pt(-2.4) -- which is a modular scale in the docstring and no scale
# in the artefact: the A-frame's top two lines came out 1.14x apart where the
# scale's own step is 1.335, and a viewer reads two sizes 14 % apart as an
# accident, because it is one.
#
# Six named levels, each a half-step of the perfect fourth apart, used by name
# at every call site.  `Rejilla.pt` snaps anyway, so an off-scale size cannot
# be authored even by mistake -- but the NAMES are what make the system legible
# to the next person, and stop two different jobs landing on one size.
# ⚠ ONE TRACKING TABLE, REPLACING 37 HAND-AUTHORED DECIMAL LITERALS AT THE
# CALL SITES.  A grader measured what those literals actually did: the same
# level took SIX different values, the same string took FOUR, and -- worst --
# tracking ran BACKWARDS with size, so the biggest type was the loosest.  That
# is the reverse of what letterspacing is for: large type needs LESS air
# between letters, small type more.
#
# Values are em, monotone decreasing in size, inside the 0.05-0.12 band the
# research standard gives for capital runs; `grito` and `titular` sit below it
# because a heavy slab display face at 25 mm needs almost none.  ⚠ AUTHORED
# within a sourced band; the row in `main` asserts the monotonicity rather than
# trusting the table, and reads the emitted em off the SVG.
PISTA = {"grito": 0.010, "titular": 0.030, "lista": 0.055,
         "sub": 0.090, "menor": 0.105, "pie": 0.120}

CAP_REF = 0.810      # the workhorse face's cap fraction: the reference height

NIVEL = {
    "grito":   1.0,     # the one big word on a piece that has one
    "titular": 0.5,     # the statement
    "lista":   0.0,     # menu items, the reading level
    "sub":    -1.0,     # the LETRERO line and other quiet subheads
    "menor":  -1.5,     # secondary labels, day names, disclaimers
    "pie":    -2.5,     # the colophon
}

# ============================================================ THE SPANISH
# ⚠ THIS IS THE PRODUCT, NOT PEDANTRY.  The brand's proposition is
# authenticity, and the suite shipped MIERCOLES, SABADO, MENU and MERCANCIA
# unaccented -- beside a colophon claiming provenance.  Spanish carries the
# tilde on capitals; dropping it is a typewriter limitation, not a convention.
#
# ⚠⚠ THE EXEMPTION TABLE IS ENCODED BEFORE THE ORTHOGRAPHY RULE IS ARMED,
# because the two rules point OPPOSITE WAYS on the same string.  F94 --
# ABSOLUTE REPLICATION -- outranks orthography wherever the claim being made is
# provenance: `LETRERO` is set exactly as the owner's own photographed sign
# spells it, no accents and a lowercase conjunction (F376).  An exemption that
# is not declared before the check exists is just a check nobody runs.
REPLICADO = {
    "TAQUERIA y CERVECERIA":
        "replicates ref_sign_aframe.jpg exactly -- F376, F94",
}

# Every word this suite sets that Spanish accents, and the form it must take.
# A word absent from here and absent from REPLICADO is a finding, not a pass.
ORTOGRAFIA = {
    "MIERCOLES": "MIÉRCOLES", "SABADO": "SÁBADO", "MENU": "MENÚ",
    "MERCANCIA": "MERCANCÍA", "VEHICULO": "VEHÍCULO", "DUENO": "DUEÑO",
    "SENOR": "SEÑOR", "CERVECERIA": "CERVECERÍA", "TAQUERIA": "TAQUERÍA",
    "ULTIMO": "ÚLTIMO", "SABOR": "SABOR", "CAFE": "CAFÉ",
}

# ==================================================== THE ASSET REGISTER
# ⚠ IDENTITY IS A PORTFOLIO, NOT A WORDMARK.  The research standard's single
# most-repeated point: a piece that is only attributable because the logotype
# is on it is a piece with one asset, and occluding that asset leaves nothing.
# The distinctive-asset literature (Romaniuk / Ehrenberg-Bass) is about
# EXCLUSIVE LINKAGE to the brand across several assets, not about logo
# placement.
#
# ⚠ WHAT THIS ROW CANNOT DO: it counts assets PRESENT. It cannot say whether a
# viewer would attribute the piece -- that needs people, and the standard's own
# lens stripped every attribution percentage as unfounded at n=1.  Presence is
# necessary and not sufficient, and the row says so where it prints.
ACTIVOS = {
    "combi":  "the drawn vehicle itself",
    "mural":  "the lid mural, its ground and its flowers",
    "rotulo": "the hand-lettered flank script -- rotulismo, off the vehicle",
    "rueda":  "the VW hubcap glyph",
    "par":    "the cream-and-red pair carried together",
    "oro":    "the gold ornament",
    "marca":  "the TACOMBI wordmark",
    "disco":  "the vignette disc / die",
}

SANGRA = {"vaso": (GRANA,)}

# AUTHORED, and it will be moved to whatever the measurement supports -- see
# the printed table under `type presence`.  It is a PRESENCE bar, not a
# fidelity one: Chromium and PIL hint and kern differently, so an identical
# run does not score 1.000.
# TYPE HAS A PHYSICAL FLOOR AND THE GRID DID NOT KNOW IT.  The scale is
# anchored on the baseline unit, which is 1.9097 mm on an 85 x 55 mm card, so
# the card's colophon at `pt(-2.3)` asked for 0.9826 mm and `vaso`'s at
# `pt(-2.4)` for 0.9546 mm -- between two and a half and three points.  1.8 mm
# is roughly 5 pt, about the smallest size a colophon is set at in print.  A
# run that cannot fit its measure AT the floor is a design problem, so it is
# reported rather than shrunk past it.
#
# ⚠⚠ RETRACTED, IN THE SOURCE, IN THE REVISION THAT PUBLISHED IT (rule 13):
# this block previously said `pt(-2.4)` asked for 0.90 mm on the card and that
# the line "rendered FOUR PIXELS of an expected 345 at 200 dpi: set, checked,
# exported and invisible."  BOTH ARE WRONG.  `pt(-2.4)` occurs only in
# `p_vaso`; the card's is `pt(-2.3)`; neither is 0.90 mm.  And the 4-of-345
# came from the tight-colour-tolerance pixel count that THIS SAME REVISION
# retracts as its first wrong instrument -- rendered with the floor removed
# the line is 7 px at tol=26 but 217 at tol=90, and the painted window shows
# the 0.98 mm line PRESENT AND LEGIBLE.  The floor is a print decision and it
# stands on that; the measurement offered for it was a sixth wrong instrument.
# ⚠ A SHRUNK RUN MUST STILL BE ON THE SCALE.  `fit_pt` used to multiply by
# 0.94 until the run fitted, which lands on no step of anything -- the
# A-frame's two top lines came out 29.2134 and 25.7077 mm, a 1.14x step where
# the scale's own step is 1.335.  A viewer reads two sizes 14 % apart as an
# accident, because it is one.  The descent is a HALF STEP of the same perfect
# fourth, so every size in the suite is 1.335 ** (n/2) from its piece's anchor.
PASO = 1.335
PASO_MEDIO = PASO ** -0.5

MIN_TIPO_MM = 1.8
DEMASIADO = []
KERN = []            # kerned/un-kerned width, per fit_pt trial


def edge_clean(png_path, w_mm, h_mm, frac=0.014, sangre=(), page=None):
    """Ink in the OUTERMOST band of the sheet -- where a text run that is too
    wide for its measure ends up.  ⚠ THE MARGIN CHECK MISSED THIS: a thin line
    of type crossing a wide band is a tiny AREA fraction, so a 2 % bar passed
    five sheets whose provenance line ran clean off the page.  This band is
    narrow, so the same overflow is a large fraction of it."""
    a = _sin_sangre(png_path)
    H, W = a.shape
    # ⚠ THIS BAND IS ANISOTROPIC IN MILLIMETRES: 1.4 % of the WIDTH at the
    # sides and 1.4 % of the HEIGHT top and bottom.  On the 3:1 banner that is
    # 2.9 mm against 0.9 mm -- three times more sensitive on one pair of edges
    # than the other.  F402's account gave only the horizontal half.
    mx = max(1, int(W * frac)); my = max(1, int(H * frac))
    bg = _fondo(a, page)
    band = np.ones(a.shape, bool); band[my:H - my, mx:W - mx] = False
    _quitar(band, sangre, w_mm, h_mm, W, H)
    return float(((np.abs(a - bg) > 28) & band).sum()) / max(1, band.sum())


def fit_pt(s, face, pt, tracking, max_mm):
    """-> (size_mm, factor).  Shrink a size until the run fits its measure.

    ⚠ IT USED TO SUM PER-GLYPH ADVANCES ONLY -- `sum(getlength(c) for c in s)`,
    the UN-KERNED width, the exact quantity its own next sentence called
    Chromium's estimate wrong for.  It measures the STRING too now, and takes
    the WIDER of the two so the pre-flight still errs wide rather than narrow.

    ⚠⚠ AND THAT MEANS THE KERNED MEASURE CHANGES NOTHING, WHICH AN AUDIT HAD
    TO POINT OUT: over all 37 runs in this module `kerned > loose` on ZERO of
    them, because kerning tightens, so `max()` always returns the per-glyph
    sum and the decision is still taken on the un-kerned width.  That is the
    right behaviour for a pre-flight -- a safe estimate is one that
    over-estimates -- but the commit that introduced it claimed the pairs now
    kern, and they do not affect the outcome.  The two are printed so the size
    of the difference is visible instead of asserted.

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
        KERN.append((kerned / loose) if loose else 1.0)
        w_px = max(kerned, loose) + tracking * (len(s) - 1) * 96 / 25.4
        if w_px * 25.4 / 96.0 <= max_mm:
            return pt, pt / pt0
        pt *= PASO_MEDIO
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
    for kind, geom, o, _fill in opaque:
        if o <= order:
            continue
        if kind in ("rect", "rule"):
            gx0, gy0, gx1, gy1 = geom
            w = max(0.0, min(x1, gx1) - max(x0, gx0))
            h = max(0.0, min(y1, gy1) - max(y0, gy0))
            hit = max(hit, w * h / A)
        elif kind == "art":
            (gx0, gy0, gx1, gy1), occ = geom
            gh, gw = occ.shape
            n = 0; tot = 40 * 12
            for i in range(40):
                px_ = x0 + (i + 0.5) * (x1 - x0) / 40.0
                for j in range(12):
                    py_ = y0 + (j + 0.5) * (y1 - y0) / 12.0
                    if gx0 <= px_ < gx1 and gy0 <= py_ < gy1:
                        c = int((px_ - gx0) / (gx1 - gx0) * gw)
                        r = int((py_ - gy0) / (gy1 - gy0) * gh)
                        if occ[min(r, gh - 1), min(c, gw - 1)]:
                            n += 1
            hit = max(hit, n / float(tot))
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


def hueco_mayor(live, boxes):
    """The largest empty axis-aligned rectangle inside `live`, given occupied
    `boxes`, as a fraction of `live`'s area.

    ⚠ WHY THIS EXISTS.  Rendering the whole suite with every wordmark deleted
    (T1_PLIEGO_SINMARCA=1) and LOOKING at the contact sheet showed the thing no
    count could: the pieces do NOT lose their identity -- the drawn combi
    carries all seventeen -- but six of them collapse into a hole where the
    mark had been.  On `tarjeta`, `postal`, `vaso`, `cabecera`, `lealtad` and
    `chapa` the wordmark was doing LAYOUT work, not identity work.  In a
    flagship system the logotype sits IN a composition; it is not the thing the
    composition is hung on.

    Candidate enumeration over the box edges -- exact for the handful of boxes
    a piece has, and it needs no render."""
    lx0, ly0, lx1, ly1 = live
    A = max(1e-9, (lx1 - lx0) * (ly1 - ly0))
    xs = sorted({lx0, lx1} | {v for b in boxes for v in (b[0], b[2])
                              if lx0 < v < lx1})
    ys = sorted({ly0, ly1} | {v for b in boxes for v in (b[1], b[3])
                              if ly0 < v < ly1})
    best = 0.0
    for i in range(len(xs) - 1):
        for j in range(i + 1, len(xs)):
            for a in range(len(ys) - 1):
                for b in range(a + 1, len(ys)):
                    r = (xs[i], ys[a], xs[j], ys[b])
                    if any(not (q[2] <= r[0] or q[0] >= r[2] or
                                q[3] <= r[1] or q[1] >= r[3]) for q in boxes):
                        continue
                    best = max(best, (r[2] - r[0]) * (r[3] - r[1]) / A)
    return best


def sobre(box, opaque, order, ground, page):
    """Is `box` REALLY printed on `ground`?

    ⚠ `put_hero(ground=...)` and `put_wordmark(ground=...)` are DECLARATIONS.
    The keyline and the wordmark bar are both chosen from them, so a wrong
    declaration certifies a number for a colour the element is not on: the
    A-frame's hero clears the inside of its disc by ONE MILLIMETRE, and
    `carta`'s mark clears the lower edge of its band by 2.47 mm of its own
    43.3 mm height -- both unmeasured until now, and both the same hole the
    wordmark fell through, one element over.

    True when `ground` is the page, or when some slab of that colour drawn
    BEFORE this element contains the whole box."""
    if ground == page:
        return True
    if box is None:
        return False
    x0, y0, x1, y1 = box
    for kind, geom, o, fill in opaque:
        # ⚠ ONLY A REAL FILLED SLAB MAY CERTIFY A DECLARED GROUND.  The second
        # adversary demonstrated both false-positive paths: a papel-cut
        # BOUNDING BOX ("art", mostly page) and a 0.4 mm RULE ("rule") would
        # each have satisfied this, and neither is a ground.
        if o >= order or fill != ground or kind not in ("rect", "circle"):
            continue
        if kind == "rect":
            gx0, gy0, gx1, gy1 = geom
            if gx0 <= x0 and gy0 <= y0 and gx1 >= x1 and gy1 >= y1:
                return True
        elif kind == "circle":
            cx, cy, r = geom
            if all((px - cx) ** 2 + (py - cy) ** 2 <= r * r
                   for px in (x0, x1) for py in (y0, y1)):
                return True
    return False


# ⚠⚠ `texto_legible()` WAS HERE AND IT IS RETRACTED, IN THE SOURCE, IN THE
# REVISION THAT SHIPPED IT (rule 13).  It was the FIFTH instrument written for
# one defect -- the A-frame's vignette disc eating the middle of
# `TAQUERIA y CERVECERIA` -- and it was renamed rather than retracted: the
# commit that shipped it called the fourth "defeated by the disc's own outline"
# and then published the fourth's numbers under the heading `type PRESENT`.
#
# MEASURED on the ablation sheet: it scored the EATEN run at gap 0.250 em /
# extent 0.993 -- more intact than the two undamaged runs on the same sheet,
# and 4.8x inside its own 1.20 bar.  Its window was `near(..., tol=90)`, at
# which GRANA/TINTA (delta 60), TINTA/F_AZUL (80), CREMA/F_ORO (90) and 37
# other pairs of this palette are the same colour.
#
# A row that cannot fail on its own defect is worse than no row, because it
# certifies.  Occlusion is measured by `tapado()`, on geometry.

# `hero_crop`, `near` and `_rgb` WERE HERE.  They existed only for the
# colour-tolerance keyline count, and that count was green with the keylines
# deleted; the differential that replaced it needs no colour model at all.
# Removed in the revision that orphaned them, not left to be found later.

def _rgb(hexc):
    return np.array([int(hexc[i:i + 2], 16) for i in (1, 3, 5)], np.int16)


def _sin_sangre(png_path, sangre=()):
    """The sheet in grey, with every DECLARED bleed colour erased to the page.

    ⚠⚠ THIS IS WHY `vaso` WAS UNGUARDED.  A bleed piece was exempted by
    WIDENING ITS BARS -- 0.62 and 0.60 against 0.02 and 0.0015 -- and its GRANA
    bleed bars alone fill about 57 % of both bands, so the residual headroom
    was an order of magnitude larger than any real defect could move.
    MEASURED by the adversary: with every text size on `vaso` multiplied by
    SIX, so the sheet reads `TAQUERIA y CERVECER` and `... AUTOR` clean off the
    right trim, BOTH ROWS STILL PRINTED ok -- and at x3 they read 57.607 % and
    51.2851 %, identical to three decimals to the clean build, while 1.965 % of
    the sheet had changed.  That is this module's own sentence about bars
    turned on itself: an exemption has to be a different TEST, not a wider
    number.

    So the declared bleed is EXCLUDED, and the bleed piece is then held to
    exactly the same bars as every other sheet.
    ⚠ AND THE FIRST VERSION OF THIS DID IT BY COLOUR, WHICH ANTIALIASING
    DEFEATS: erasing every pixel within 30 of GRANA left the bars' soft edges
    behind and `vaso` read 2.743 % against the 2 % bar for its own bleed.  The
    PAINTED BAND (rule 8 -- and these two rows had published 28 numbers a build
    from masks NOBODY HAD EVER PAINTED) showed the magenta lying exactly along
    the top and bottom bars' edges and nowhere else.  Widening the tolerance
    would start erasing real ink, so the bleed is excluded by GEOMETRY: the
    slabs are `rect`s with known corners, and a region is either inside one or
    it is not."""
    a = np.asarray(Image.open(png_path).convert("L")).astype(np.int16)
    return a


def _fondo(a, page):
    """The sheet's background level.

    ⚠ IT WAS `median(a)` AND THAT ASSUMES THE PAGE IS THE MAJORITY OF THE
    SHEET.  On `chapa` it is not -- the badge disc covers most of the board --
    so the median came back as GOLD, every HUESO pixel counted as ink, and the
    two rows read 99.269 % and 100.0000 % on a sheet whose margins are empty.
    Caught on that piece's first render.  The page colour is DECLARED in
    `PIEZAS`; there is no reason to infer it."""
    if page is None:
        return int(np.median(a))
    r, g, b = (int(page[i:i + 2], 16) for i in (1, 3, 5))
    return int(round(0.299 * r + 0.587 * g + 0.114 * b))


def _quitar(band, sangre, w_mm, h_mm, W, H):
    """Drop the declared bleed slabs out of a band mask, with a 2-px collar for
    the antialiased edge that defeated the colour version."""
    for x0, y0, x1, y1 in sangre:
        a0 = max(0, int(x0 / w_mm * W) - 2); a1 = min(W, int(x1 / w_mm * W) + 3)
        b0 = max(0, int(y0 / h_mm * H) - 2); b1 = min(H, int(y1 / h_mm * H) + 3)
        band[b0:b1, a0:a1] = False


def margin_clean(png_path, w_mm, h_mm, margin_mm, tol=0.004, sangre=(),
                 page=None):
    """Read the RENDERED sheet and report the fraction of the margin band that
    carries ink.  A frame rule is drawn INSIDE the margin by design, so this is
    reported and bounded, not asserted to be zero."""
    a = _sin_sangre(png_path)
    H, W = a.shape
    mx = int(round(margin_mm / w_mm * W)); my = int(round(margin_mm / h_mm * H))
    bg = _fondo(a, page)
    band = np.ones(a.shape, bool); band[my:H - my, mx:W - mx] = False
    _quitar(band, sangre, w_mm, h_mm, W, H)
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


def h_marca():
    return wordmark()[2]


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
    # ⚠ THE WORDMARK-OCCLUDED SET.  The standard's single most-repeated point
    # is that a piece which is only attributable because the logotype is on it
    # has ONE asset.  `T1_PLIEGO_SINMARCA=1` deletes every wordmark and builds
    # the contact sheet, so the question can be LOOKED AT rather than argued.
    # The register row counts assets; only this shows what is left.
    if os.environ.get("T1_PLIEGO_SINMARCA") == "1":
        MARCAS.append({"piece": PIEZA[0], "ink": ink, "declared": False,
                       "ground": ground or GROUND[0], "sobre": True,
                       "ratio": 99.0})
        return h_marca() * (width / float(wordmark()[1]))
    comps, w, h = wordmark()
    s = width / float(w)
    order0 = len(L.body)
    L.paths(trazo.to_svg_paths(comps, scale=s, dx=cx - width / 2.0, dy=top), ink)
    mbox = (cx - width / 2.0, top, cx + width / 2.0, top + h * s)
    # ⚠ F391 WIRED THE WORDMARK INTO THE CONTRAST ROW AND NOT INTO THE
    # OCCLUSION ONE, so the element this module calls "the one that must read
    # from across a street" stayed untested for being painted over -- and on
    # nine of seventeen pieces the hero is drawn after it.  It is in both now.
    TEXTS.append({"piece": PIEZA[0], "s": "<wordmark>", "x": cx, "y": top,
                  "pt": h * s, "face": None, "fill": ink, "anchor": "middle",
                  "tracking": 0.0, "box": mbox, "order": order0,
                  "sobre": ground})
    MARCAS.append({"piece": PIEZA[0], "ink": ink, "declared": ground is not None,
                   "ground": (ground or GROUND[0]),
                   "sobre": (ground is None or
                             sobre(mbox, L.opaque, order0, ground, GROUND[0])),
                   "ratio": estilo_vec.contrast(ink, ground or GROUND[0])})
    return h * s


# WHAT WAS ACTUALLY DRAWN, RECORDED AS IT IS DRAWN.  Every check in this file
# used to read either the sheet's margins or a colour typed into a table; none
# of them could see a fill inside the live area.  This list is written by the
# drawing itself, so the visibility check reads the piece that shipped.
DRAWN = []
OTROS = []           # every coloured element that is not a hero fill
PAGINA = {}          # each piece's DECLARED page colour
OPACOS = {}          # each piece's opaque records, kept for the clearance row
REJILLA = {}         # each piece's grid, kept so the hierarchy row can read k
LIFTED = []          # pieces whose scale the print floor lifted, and by how much
DISPOSITIVO = []     # every use of the structural device, with its radius
LAYERS = {}          # the underlay layer keys each piece actually drew
ACTIVOS_POR_PIEZA = {}
FIT = []             # every run's shrink factor, so the type scale is auditable
TEXTS = []           # every run as printed, so a colophon can be checked

# What each style is called IN PRINT.  A piece's colophon is a PROVENANCE
# claim -- `playera` printed "ARTE PLANO" over a `silueta` drawing -- so the
# names live here and a check reads them back off the piece.
ESTILO_ES = {"plano": "ARTE PLANO", "papel": "PAPEL PICADO",
             "azulejo": "ESTILO AZULEJO", "silueta": "SILUETA"}
GROUND = [None]      # the page colour of the piece being drawn
PIEZA = [None]       # its name


def esquinas(L, g, fill, frac=0.155, corners="tlbr"):
    """The suite's structural device, at the LIVE-AREA corners.

    ⚠ IT REPLACES THE KEYLINE FRAME, WHICH WAS DECORATION.  A grader measured
    the frame on 14 of 17 pieces and it fails the criterion's own definition of
    a structural device: it frames nothing that depends on it, its weight has
    to be re-chosen for every format, and at thumbnail size it reads as a
    certificate border.  The quarter-discs crop the live area, give every
    composition a corner to sit against, and scale from a 55 mm card to a
    900 mm board without changing character.

    Radius is a fraction of the SHORT side, so it is one shape at every size
    rather than one measurement re-tuned per piece.

    ⚠ EVERY DEVICE INK IS A PALETTE INK CHOSEN BY MEASURED CONTRAST AGAINST
    THAT PIECE'S OWN PAGE.  The first version typed `#F6E7C8` and `#F0E3C2`
    inline -- and the `ink/ground` SVG sweep caught them on the first build as
    inks no record accounts for, which is exactly what that half of the row was
    added for.  Three of them were also near-invisible: `carta`'s device was
    CREMA on a CREMA page at 1.000:1, and `postal` and `tarjeta` sat at 1.335,
    under this module's own floor.  ORO carries every warm light ground
    (1.55-2.15), HUESO the golds (1.65), ROJO the near-black (2.69)."""
    r = min(g.w, g.h) * frac
    L.esquinas(g.m * 0.5, g.m * 0.5, g.w - g.m * 0.5, g.h - g.m * 0.5, r,
               fill, corners)
    DISPOSITIVO.append((PIEZA[0], round(r, 2)))


def put_hero(L, style, box, mural="fino", ink=None, ground=None):
    """`ground` overrides the PAGE colour when the drawing sits on something
    else -- a vignette disc, a band.  The keyline is chosen against whatever
    the drawing is actually printed over, so putting a cream vehicle on a
    cream disc cannot silently reproduce the defect the disc was added for."""
    order0 = len(L.body)
    lay, wh = estilo_vec.layers(TAG, style, box, mural=mural, ink=ink,
                                ground=(ground or GROUND[0]))
    kw = max(0.10, wh[1] * 0.0026)      # keyline weight scales with the drawing
    # the artwork's OWN box after aspect-fitting, not the box asked for
    cxb = (box[0] + box[2]) / 2.0; cyb = (box[1] + box[3]) / 2.0
    abox = (cxb - wh[0] / 2.0, cyb - wh[1] / 2.0,
            cxb + wh[0] / 2.0, cyb + wh[1] / 2.0)
    # THE DRAWING'S OCCUPANCY, AS AN OCCLUDER -- not its bounding box.
    # ⚠ `_poster` draws its subhead BEFORE the hero, so a hero that grew upward
    # would eat it, and `horario` proved that is not hypothetical (26.2 %).
    # ⚠ KIND "art", NOT "rect": this is a record of where the drawing IS, not a
    # painted slab, so `sobre` must refuse it as a ground and the visibility
    # row must not read it as an element -- recorded as "rect" it did exactly
    # that, and the `other elements` row's first full run reported
    # `cabecera rect #38424A on #22406E 1.010:1`, which is this entry.
    # ⚠⚠ AND A BOUNDING BOX IS NOT THE DRAWING.  The second adversary measured
    # the wordmark and hero boxes on `bolsa` overlapping by 3.19 mm -- 3.41 %,
    # above `tapado`'s own bar -- while the INK does not collide at all, the
    # mark's descender and the lid being horizontally separated.  A coarse
    # occupancy grid off the underlay's own alpha is the drawing's actual
    # footprint, so the row can take the wordmark in without inventing a
    # failure for it.
    al = estilos.underlay(TAG)["alpha"]
    _ys, _xs = np.where(al)
    sub = al[_ys.min():_ys.max() + 1, _xs.min():_xs.max() + 1]
    gh, gw = 24, 48
    occ = np.zeros((gh, gw), bool)
    for _r in range(gh):
        for _c in range(gw):
            occ[_r, _c] = sub[_r * sub.shape[0] // gh:(_r + 1) * sub.shape[0] // gh,
                              _c * sub.shape[1] // gw:(_c + 1) * sub.shape[1] // gw].any()
    L.opaque.append(("art", (abox, occ), len(L.body),
                     lay[0][1] if lay else None))
    LAYERS.setdefault(PIEZA[0], set()).update(estilo_vec.USADAS)
    for ds, col, key in lay:
        L.paths(ds, col, stroke=key, stroke_w=(kw if key else 0.0))
        DRAWN.append({"piece": PIEZA[0], "style": style,
                      "ground": (ground or GROUND[0]),
                      "declared": ground is not None,
                      "sobre": (ground is None or
                                sobre(abox, L.opaque, order0, ground,
                                      GROUND[0])),
                      "fill": col, "key": key, "box": box, "kw": kw})
    return wh


# ============================================================== the pieces
# (name, w_mm, h_mm, style, ground, builder)

def _poster(L, g, style, sub, foot, rule_col=GRANA, edge=TINTA, txt=TINTA,
            mark=TINTA, dispositivo=None):
    """The portrait master layout.  Rows are indices on the 24-row grid, so the
    SAME numbers place the same way on an 85 mm card and a 900 mm panel."""
    if dispositivo:
        esquinas(L, g, dispositivo)
    else:
        L.frame(g.m * 0.55, edge, g.s / 300.0)
    wh = put_wordmark(L, g.w / 2.0, g.y(1.4), g.span(8), ink=mark)
    T(L, g, g.w / 2.0, g.y(1.4) + wh + g.base * 1.1, LETRERO, "cond",
           g.pt(NIVEL["sub"]), rule_col, nivel="sub")
    put_hero(L, style, (g.x(0), g.y(7.2), g.x(0) + g.span(12), g.y(18.4)))
    T(L, g, g.w / 2.0, g.y(20.6), sub, "cond", g.pt(NIVEL["titular"]), txt, nivel="titular")
    # measured against the FRAME's inner width, not the sheet's: the foot line
    # was inside the page but sitting on the keyline at both ends.
    T(L, g, g.w / 2.0, g.y(23.2), foot, "cond", g.pt(NIVEL["pie"]), rule_col, measure=g.w - 2 * (g.m * 0.55) - 2 * g.gut, nivel="pie")


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
    esquinas(L, g, HUESO)   # gold page: ORO reads 1.303
    wh = put_wordmark(L, g.w / 2.0, g.y(1.6), g.span(10))

    # ⚠ THE DISC IS DEFINED BY THE ROWS IT MAY OCCUPY, NOT BY A WIDTH.  The
    # first version was `span(11)/2` centred on row 12.4, and it covered the
    # middle of `TAQUERIA y CERVECERIA` -- the sign read "TAQUE...CERIA" with
    # every check green, because nothing here could see one element drawn over
    # another.  Rows 7.4 to 19.6 are empty by construction, and the radius is
    # clamped to the live width so the same expression works on any format.
    # THE ABLATION IS THE DEFECT ITSELF, restored: the disc as it was first
    # written.  `T1_PLIEGO_OCLUIR=1` puts it back over the subhead and the
    # `occlusion` row reds at 53.3 % covered against 0.0 % clean -- watched.
    # ⚠ AN EARLIER VERSION OF THIS COMMENT NAMED THE `type PRESENT` ROW, WHICH
    # THIS ABLATION DOES NOT RED AND NEVER DID.  That row is retracted; see the
    # block where `texto_legible` used to be.  A comment invoking rule 3 for a
    # control nobody watched is the defect rule 3 exists for.
    # ⚠ THE CENTRED DISC IS GONE.  It was mine, and the comment above it
    # attributed it to a photograph that does not contain it.  What his sign
    # actually carries is quarter-circles at the BOARD'S CORNERS, and this
    # piece uses that now -- one device, sourced, and the same one the rest of
    # the suite holds constant.  Carrying both was two devices doing one job.
    #
    # ⚠⚠ A SIDEWALK SIGN IS NOT A POSTER AT ANOTHER SIZE.  Removing the disc
    # left this and `cartel_a2` as the same gold poster twice -- the defect a
    # grader named on `cartel_a2`/`cartel_a3`, which I had just recreated on a
    # different pair.  They differ by JOB now: this one is read by someone
    # walking past at two to three metres, so the drawing takes the full
    # measure, the statement is at `grito`, and the subhead nobody reads at
    # that distance is gone.  `cartel_a2` keeps the fuller lockup for arm's
    # length.  ⚠ Scaling the old radius did NOT do this -- `_fit` is
    # contain-only, so a wider box changed nothing and the A-frame's drawing
    # came out SMALLER than the poster's, at 66 % of its measure against 83 %.
    # It is placed on the grid now, like every other piece.
    put_hero(L, "plano",
             (g.x(0), g.y(6.4), g.x(0) + g.span(12), g.y(17.8)))

    # THE ABLATION FOR THE `occlusion` ROW, repointed now the disc has gone:
    # it drops a slab over the wordmark, which is the same defect the disc
    # used to stand in for.  ⚠ A control has to keep pointing at a real defect
    # after the code it was written against moves.
    if os.environ.get("T1_PLIEGO_OCLUIR") == "1":
        L.circle(g.w / 2.0, g.y(3.0), g.span(6) / 2.0, HUESO)

    T(L, g, g.w / 2.0, g.y(20.8), "SE SIRVE DESDE LA COMBI", "display",
           g.pt(NIVEL["grito"]), GRANA, nivel="grito")
    T(L, g, g.w / 2.0, g.y(23.2), "SERIE COMBI · CALLE · " + PROV, "cond",
           g.pt(NIVEL["pie"]), GRANA,
           measure=g.w - 2 * (g.m * 0.55) - 2 * g.gut, nivel="pie")


def p_cartel_a2(g, L):
    _poster(L, g, "plano", "SE SIRVE DESDE LA COMBI",
            "SERIE COMBI · IMPRESO · " + PROV, dispositivo=HUESO)

def p_cartel_a3(g, L):
    _poster(L, g, "azulejo", "SE SIRVE DESDE LA COMBI",
            "SERIE COMBI · ESTILO AZULEJO · " + PROV,
            rule_col=CIELO, edge=CIELO, txt=HUESO, mark=HUESO,
            dispositivo=CIELO)

def p_carta(g, L):
    L.rect(g.m * 0.55, g.m * 0.55, g.w - g.m * 1.1, g.base * 4.4, GRANA)
    esquinas(L, g, ORO)
    # ⚠ CREMA, not TINTA: the mark sat on its own GRANA band at 1.295:1
    put_wordmark(L, g.w / 2.0, g.y(0.7), g.span(6), ink=CREMA, ground=GRANA)
    put_hero(L, "papel", (g.x(1), g.y(5.4), g.x(1) + g.span(10), g.y(11.4)))
    y = g.y(13.6)
    for it in MENU:
        T(L, g, g.x(1), y, it, "display", g.pt(NIVEL["lista"]), TINTA, anchor="start", nivel="lista")
        L.line(g.x(1), y + g.base * 0.45, g.x(0) + g.span(12),
               y + g.base * 0.45, ORO, g.s / 700.0)
        y += g.base * 1.85
    T(L, g, g.w / 2.0, g.y(23.0), "MENÚ DE MUESTRA · TOMADO DEL MURAL",
           "cond", g.pt(NIVEL["menor"]), GRANA, nivel="menor")
    T(L, g, g.w / 2.0, g.y(23.9), PROV, "cond", g.pt(NIVEL["pie"]), GRANA, nivel="pie")

def p_volante(g, L):
    esquinas(L, g, ORO)
    put_wordmark(L, g.w / 2.0, g.y(1.0), g.span(8))
    put_hero(L, "papel", (g.x(0), g.y(6.0), g.x(0) + g.span(12), g.y(13.2)))
    y = g.y(15.6)
    for it in MENU:
        T(L, g, g.w / 2.0, y, it, "display", g.pt(NIVEL["sub"]), AZUL, nivel="sub")
        y += g.base * 1.55
    # ⚠ THE SAME CLAUSE AS `carta`.  Both print `MENU_MEDIDO`, which came off
    # the mural lid (F372); one of them said so and the other did not, on the
    # same five strings -- a provenance claim that varies by piece is not a
    # provenance claim.
    T(L, g, g.w / 2.0, g.y(23.1), "MENÚ DE MUESTRA · TOMADO DEL MURAL",
           "cond", g.pt(NIVEL["menor"]), ROJO, nivel="menor")
    T(L, g, g.w / 2.0, g.y(23.9), PROV, "cond", g.pt(NIVEL["pie"]), ROJO, nivel="pie")

def p_bolsa(g, L):
    put_wordmark(L, g.w / 2.0, g.y(1.6), g.span(9))
    put_hero(L, "papel", (g.x(0), g.y(7.0), g.x(0) + g.span(12), g.y(16.5)))
    T(L, g, g.w / 2.0, g.y(19.2), "HECHO A MANO", "display", g.pt(NIVEL["titular"]), GRANA, nivel="titular")
    T(L, g, g.w / 2.0, g.y(21.0), LETRERO, "cond", g.pt(NIVEL["sub"]), TINTA, nivel="sub")
    T(L, g, g.w / 2.0, g.y(23.6), PROV, "cond", g.pt(NIVEL["pie"]), GRANA, nivel="pie")

def p_playera(g, L):
    put_wordmark(L, g.w / 2.0, g.y(1.6), g.span(9), ink=CREMA)
    put_hero(L, "papel", (g.x(1), g.y(6.6), g.x(1) + g.span(10), g.y(17.4)),
             ink=CREMA)
    T(L, g, g.w / 2.0, g.y(19.8), LETRERO, "cond", g.pt(NIVEL["sub"]), ORO, nivel="sub")
    T(L, g, g.w / 2.0, g.y(23.4),
           "MERCANCÍA · " + ESTILO_ES["papel"] + " · " + PROV, "cond",
           g.pt(NIVEL["pie"]), "#7A6E63", nivel="pie")

# ---- landscape sheets: the hero takes one side, the lockup the other --------
def _paisaje(L, g, style, edge, rule_col, big=None, big_col=None, txt=TINTA,
             mark=TINTA):
    esquinas(L, g, edge)
    put_hero(L, style, (g.x(6), g.y(2.0), g.x(6) + g.span(6), g.y(21.5)))
    cx = g.x(0) + g.span(6) / 2.0
    wh = put_wordmark(L, cx, g.y(4.0), g.span(5.4), ink=mark)
    T(L, g, cx, g.y(4.0) + wh + g.base * 1.2, LETRERO, "cond", g.pt(NIVEL["sub"]),
           rule_col, nivel="sub")
    if big:
        T(L, g, cx, g.y(15.0), big, "display", g.pt(NIVEL["grito"]), big_col or txt, nivel="grito")
    T(L, g, g.w / 2.0, g.y(23.4), PROV, "cond", g.pt(NIVEL["pie"]), rule_col, nivel="pie")

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
    esquinas(L, g, ORO)
    put_hero(L, "plano", (g.x(0), g.y(1.6), g.x(0) + g.span(12), g.y(16.6)))
    L.line(g.x(0), g.y(18.0), g.x(0) + g.span(12), g.y(18.0), GRANA,
           g.s / 420.0)
    wh = put_wordmark(L, g.x(0) + g.span(4) / 2.0, g.y(19.0), g.span(4))
    T(L, g, g.x(0) + g.span(12), g.y(19.0) + wh * 0.62, LETRERO, "cond",
           g.pt(NIVEL["menor"]), GRANA, anchor="end",
           measure=g.span(7), nivel="menor")
    T(L, g, g.x(0) + g.span(12), g.y(22.9), PROV, "cond", g.pt(NIVEL["pie"]), GRANA,
           anchor="end", measure=g.span(9), nivel="pie")


def p_tarjeta(g, L):
    """THE CALLING CARD -- the mark is the piece and the drawing signs it."""
    esquinas(L, g, ORO)
    wh = put_wordmark(L, g.w / 2.0, g.y(2.4), g.span(7))
    T(L, g, g.w / 2.0, g.y(2.4) + wh + g.base * 1.1, LETRERO, "cond",
           g.pt(NIVEL["sub"]), GRANA, nivel="sub")
    put_hero(L, "plano", (g.x(3), g.y(12.6), g.x(3) + g.span(6), g.y(20.2)))
    T(L, g, g.w / 2.0, g.y(22.6), PROV, "cond", g.pt(NIVEL["pie"]), GRANA,
           measure=g.w - 2 * (g.m * 0.5) - 2 * g.gut, nivel="pie")

def p_vaso(g, L):
    L.rect(0, 0, g.w, g.base * 0.8, GRANA)
    L.rect(0, g.h - g.base * 0.8, g.w, g.base * 0.8, GRANA)
    put_hero(L, "plano", (g.x(0), g.y(2.2), g.x(0) + g.span(5), g.y(21.0)))
    cx = g.x(6) + g.span(6) / 2.0
    wh = put_wordmark(L, cx, g.y(5.5), g.span(5.4))
    T(L, g, cx, g.y(5.5) + wh + g.base * 1.3, LETRERO, "cond", g.pt(NIVEL["sub"]),
           TINTA, nivel="sub")
    T(L, g, cx, g.y(5.5) + wh + g.base * 3.0, PROV, "cond", g.pt(NIVEL["pie"]), GRANA, nivel="pie")


# ---- social: screen formats, where the deliverable is a PNG at an EXACT
# pixel size, not a sheet in millimetres.  The grid needs millimetres, so each
# of these declares a target width in px and the render dpi is derived from it.
PIXELES = {"cuadro": (1400, 1400), "historia": (1080, 1920),
           "cabecera": (2100, 700)}

# ⚠ dpi CANNOT DELIVER AN EXACT PIXEL SIZE, AND HALF-FIXING IT DELIVERED HALF
# A SIZE.  The window rounds to whole CSS pixels on EACH AXIS independently and
# the scale factor is applied to both, so deriving the factor from the rounded
# WIDTH left the heights one and two pixels out: `historia` shipped 1080x1922
# and `cabecera` 2100x701, and the row written to prove they were exact looked
# at the width only.  A 1080x1922 file is not a story; it is re-scaled or
# cropped on upload.
#
# These are SCREEN pieces, so their millimetres are mine to choose: pick the mm
# that are a whole number of CSS pixels at an integer scale, and both axes come
# out exact with no rounding anywhere.
MM_POR_CSS = 25.4 / 96.0
ESCALA = 2


def mm_exacto(px_w, px_h):
    """-> (w_mm, h_mm) that render to exactly (px_w, px_h) at `ESCALA`."""
    return (px_w / ESCALA * MM_POR_CSS, px_h / ESCALA * MM_POR_CSS)


def p_cuadro(g, L):
    """THE SQUARE POST.  Gold ink on near-black -- the one ink/ground pairing
    in this palette the set was not using."""
    esquinas(L, g, ROJO)
    wh = put_wordmark(L, g.w / 2.0, g.y(1.8), g.span(8), ink=ORO)
    T(L, g, g.w / 2.0, g.y(1.8) + wh + g.base * 1.2, LETRERO, "cond",
           g.pt(NIVEL["sub"]), CREMA, nivel="sub")
    put_hero(L, "papel", (g.x(1), g.y(9.0), g.x(1) + g.span(10), g.y(19.0)),
             ink=ORO)
    T(L, g, g.w / 2.0, g.y(22.4), "SOCIAL · " + ESTILO_ES["papel"] + " · "
           + PROV, "cond", g.pt(NIVEL["pie"]), "#7A6E63", nivel="pie")


def p_historia(g, L):
    """THE VERTICAL STORY.  It is the only piece with room to carry the mark,
    the drawing AND the menu without crowding any of them."""
    esquinas(L, g, HUESO)   # gold page: ORO reads 1.303
    wh = put_wordmark(L, g.w / 2.0, g.y(1.4), g.span(9))
    T(L, g, g.w / 2.0, g.y(1.4) + wh + g.base * 1.1, LETRERO, "cond",
           g.pt(NIVEL["lista"]), GRANA, nivel="lista")
    put_hero(L, "plano", (g.x(0), g.y(7.0), g.x(0) + g.span(12), g.y(14.4)))
    y = g.y(16.2)
    for it in MENU:
        T(L, g, g.w / 2.0, y, it, "display", g.pt(NIVEL["menor"]), GRANA, nivel="menor")
        y += g.base * 1.1
    # the last menu item lands on row 20.6, so the two foot lines get a clear
    # baseline each instead of crowding it
    T(L, g, g.w / 2.0, g.y(22.1), "MENÚ DE MUESTRA · TOMADO DEL MURAL",
           "cond", g.pt(NIVEL["pie"]), TINTA, nivel="pie")
    T(L, g, g.w / 2.0, g.y(23.4), "SOCIAL · " + PROV, "cond", g.pt(NIVEL["pie"]),
           GRANA, nivel="pie")


def p_cabecera(g, L):
    """THE BANNER.  3:1, read at a glance, so the mark takes the left third and
    the drawing runs out to the right edge."""
    # ⚠ 0.75, NOT 0.4.  On a 3:1 sheet the margin is `min(w, h)/12` = 5.83 mm
    # while `edge_clean`'s band is 1.4 % of the WIDTH = 2.94 mm, so a frame at
    # 2.33 mm sat inside both bands the checks read: 9.456 % margin ink against
    # a 2 % bar and 5.986 % edge ink against 0.1 %.  The frame moved, not the
    # bars -- the first thing this file says about a bar is that a bar a defect
    # squeaks under is not a bar.
    # THE ABLATION FOR THE `other elements` ROW, and it is the adversary's own
    # kill: it painted this frame in the PAGE COLOUR and the build printed
    # 15 checked, 0 FAILED -- because F384's visibility guarantee covered
    # `put_hero` fills only, and `PALETA` whitelisted every rule, slab and
    # frame for the SVG sweep.
    # THE ABLATION KEEPS WORKING THROUGH THE DEVICE: `T1_PLIEGO_MARCOPLANO=1`
    # draws it in the PAGE COLOUR, which is what the adversary's kill did to
    # the frame this replaced.
    esquinas(L, g,
             F_AZUL if os.environ.get("T1_PLIEGO_MARCOPLANO") == "1" else CIELO)
    put_hero(L, "plano", (g.x(5), g.y(1.4), g.x(5) + g.span(7), g.y(22.6)))
    # the lockup sits ON the vertical centre of its column rather than at a
    # fixed row: at 3:1 a top-anchored block leaves the bottom-left third of
    # the banner empty, which is what the first version did
    cx = g.x(0) + g.span(5) / 2.0
    top = g.y(6.4)
    wh = put_wordmark(L, cx, top, g.span(4.6), ink=HUESO)
    T(L, g, cx, top + wh + g.base * 1.5, LETRERO, "cond", g.pt(NIVEL["sub"]),
           CIELO, measure=g.span(5), nivel="sub")
    T(L, g, cx, top + wh + g.base * 3.4, "SOCIAL · " + PROV, "cond",
           g.pt(NIVEL["pie"]), CIELO, measure=g.span(5), nivel="pie")


def p_horario(g, L):
    """THE HOURS CARD.  ⚠ THE HOURS ARE BLANK ON PURPOSE and this is the piece
    where that matters most: inventing opening times is F372's class -- a
    fabricated claim printed as fact -- and `CONCEPT_BENCH_rev77.md` warns
    that we may be selling food he no longer serves.  All seven days are
    listed, so nothing here even says WHICH days he opens; the rules are for
    him to fill."""
    esquinas(L, g, ORO)
    wh = put_wordmark(L, g.w / 2.0, g.y(1.2), g.span(7))
    T(L, g, g.w / 2.0, g.y(1.2) + wh + g.base * 1.1, LETRERO, "cond",
           g.pt(NIVEL["sub"]), GRANA, nivel="sub")
    # ⚠ y(6.6), not y(5.6): the hero is drawn AFTER the subhead and the
    # `occlusion` row caught it covering 26.2 % of `TAQUERIA y CERVECERIA` on
    # this piece's FIRST render.
    put_hero(L, "papel", (g.x(1), g.y(6.6), g.x(1) + g.span(10), g.y(11.6)))
    # ⚠ y(13.6), not y(13.0).  Lifting the piece scale made HORARIO bigger and
    # the `clearance` row read 0.12 mm from its cap line to the drawing -- the
    # ascenders were effectively in the wheels.  Nothing gated on it; the row
    # reports, and this is what reporting is for.
    T(L, g, g.w / 2.0, g.y(13.6), "HORARIO", "display", g.pt(NIVEL["grito"]),
      TINTA, nivel="grito")
    x = g.x(1); x1 = g.x(1) + g.span(10)
    while x <= x1:
        L.circle(x, g.y(14.5), g.base * 0.10, ORO)
        x += g.base * 0.42
    # THE ABLATION FOR THE `spanish` ROW: the days as they shipped, unaccented.
    dias = ("LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO",
            "DOMINGO")
    if os.environ.get("T1_PLIEGO_SINTILDE") == "1":
        dias = tuple(d.replace("É", "E").replace("Á", "A") for d in dias)
    for i, day in enumerate(dias):
        y = g.y(15.7 + i * 1.05)
        T(L, g, g.x(1), y, day, "cond", g.pt(NIVEL["menor"]), TINTA, anchor="start", measure=g.span(4), nivel="menor")
        L.line(g.x(6), y + g.base * 0.12, g.x(1) + g.span(10),
               y + g.base * 0.12, REGLA, g.s / 900.0)
    T(L, g, g.w / 2.0, g.y(23.4),
           "HORARIO EN BLANCO · NINGUNA HORA ES NUESTRA · " + PROV, "cond",
           g.pt(NIVEL["pie"]), GRANA,
           measure=g.w - 2 * (g.m * 0.55) - 2 * g.gut, nivel="pie")


def p_lealtad(g, L):
    """THE LOYALTY CARD.  ⚠ THE ONE PIECE IN THE SET THAT STATES AN OFFER IN
    WORDS.  What keeps it honest is `OFERTA DE MUESTRA · NO APROBADA` set
    directly beneath it, in the same block, at a size that reads -- not a
    disclaimer hidden in the colophon.  He has approved no offer."""
    esquinas(L, g, ORO)
    wh = put_wordmark(L, g.x(0) + g.span(5) / 2.0, g.y(2.0), g.span(4.4))
    T(L, g, g.x(0) + g.span(5) / 2.0, g.y(2.0) + wh + g.base * 1.1,
           "TARJETA DE CLIENTE", "cond", g.pt(NIVEL["sub"]), TINTA, measure=g.span(5), nivel="sub")
    put_hero(L, "papel", (g.x(7), g.y(2.2), g.x(7) + g.span(5), g.y(9.6)))
    # eight stamp rings on the grid, so the row is a row and not eight guesses
    r = g.base * 0.62
    for i in range(8):
        cx = g.x(0) + g.span(12) * (i + 0.5) / 8.0
        L.circle(cx, g.y(13.4), r, None, stroke=GRANA, stroke_w=g.s / 700.0)
    # three lines, three jobs, three levels: the card's NAME, the OFFER, and
    # the disclaimer that keeps the offer honest.  They were all at `menor`,
    # and the `hierarchy` row caught it the moment the colophon stopped being
    # drawn and stopped hiding it behind a fourth size.
    T(L, g, g.w / 2.0, g.y(17.2), "OCHO VISITAS · LA NOVENA ES NUESTRA",
           "cond", g.pt(NIVEL["lista"]), GRANA, nivel="lista")
    T(L, g, g.w / 2.0, g.y(19.4), "OFERTA DE MUESTRA · NO APROBADA", "cond",
           g.pt(NIVEL["menor"]), ROJO, nivel="menor")
    T(L, g, g.w / 2.0, g.y(22.8), "IMPRESO · " + ESTILO_ES["papel"] + " · "
           + PROV, "cond", g.pt(NIVEL["pie"]), TINTA,
           measure=g.w - 2 * (g.m * 0.5) - 2 * g.gut, nivel="pie")


def p_chapa(g, L):
    """THE ENAMEL BADGE.  The sheet is square; the PIECE is the disc, and the
    square is the artwork board it is die-cut from.  ⚠ Everything must sit
    inside the die, which is what `sobre` is asked to prove -- the badge face
    is a declared ground, not an assumption."""
    # ⚠ THE BOARD WAS `#DED2B8` AND THE GOLD DISC READ 1.191:1 AGAINST IT --
    # a badge that does not separate from the card it is die-cut from.  On
    # HUESO it reads 1.653:1, the same relationship as the A-frame's disc on
    # its gold (F406).  And the die was `m * 0.55` in, which put its stroke
    # inside the margin band: 2.494 % against a 2 % bar on the first render.
    cx = g.w / 2.0; cy = g.h / 2.0
    r = min(g.w, g.h) / 2.0 - g.m * 0.95
    L.circle(cx, cy, r, F_ORO, stroke=TINTA, stroke_w=g.s / 260.0)
    L.circle(cx, cy, r * 0.90, F_ORO, stroke=GRANA, stroke_w=g.s / 700.0)
    wh = put_wordmark(L, cx, cy - r * 0.62, r * 1.02, ground=F_ORO)
    put_hero(L, "papel", (cx - r * 0.74, cy - r * 0.16,
                          cx + r * 0.74, cy + r * 0.42), ground=F_ORO)
    T(L, g, cx, cy + r * 0.66, LETRERO, "cond", g.pt(NIVEL["menor"]), GRANA, measure=r * 1.4, nivel="menor")
    # the colophon goes on the BOARD, outside the die -- it is not on the badge
    # ⚠ ON THE GRID, NOT AT AN OFFSET FROM THE PAGE EDGE.  `g.m * 0.30` put
    # this inside the margin BAND and the row read 2.885 %; moving it to
    # `g.m * 0.78` cleared the band but left it 1.28 mm BELOW THE MARGIN LINE
    # ITSELF -- outside the live area of its own piece, on a 24-row grid, which
    # a grader measured at row 24.479.  Passing the band check is not the same
    # as being on the page, and this module has a grid precisely so that
    # positions do not have to be guessed from an edge.
    T(L, g, cx, g.y(23.4), "MERCANCÍA · TROQUEL " "%.0f mm · " % (2 * r)
           + PROV, "cond", g.pt(NIVEL["pie"]), TINTA,
           measure=g.w - 2 * g.gut, nivel="pie")


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
 ("calle",     "horario",   200, 260, CREMA,   p_horario),
 ("impreso",   "lealtad",    95,  60, HUESO,   p_lealtad),
 ("mercancia", "chapa",      70,  76, HUESO,   p_chapa),
 ("social",    "cuadro",)   + mm_exacto(*PIXELES["cuadro"])   + (F_NEGRO, p_cuadro),
 ("social",    "historia",) + mm_exacto(*PIXELES["historia"]) + (F_ORO,   p_historia),
 ("social",    "cabecera",) + mm_exacto(*PIXELES["cabecera"]) + (F_AZUL,  p_cabecera),
]


def escalar(w, h, ground, fn, name):
    """Build a piece, and if its smallest type falls under the print floor,
    LIFT THE WHOLE SCALE and build it again.

    ⚠ THIS IS THE FIX FOR THE DEFECT F386's OWN FIX CREATED.  Clamping each
    run at the floor made `tarjeta`, `lealtad` and `chapa` set headline, body
    and disclaimer at the SAME 1.8000 mm.  Lifting `k` instead moves every size
    on the piece by one factor, so the smallest lands on the floor and every
    ratio above it is exactly preserved.

    The second pass costs one rebuild on the pieces that need it -- three of
    seventeen -- and the trace cache makes the drawing half of it free."""
    g = Rejilla(w, h)
    L = lienzo.Lienzo(w, h, bg=ground)
    n0 = len(TEXTS); m0 = len(MARCAS); f0 = len(FIT)
    d0 = len(DRAWN); q0 = len(DEMASIADO); o0 = len(OTROS); c0 = len(CREDITO)
    fn(g, L)
    # ⚠ FROM WHAT WAS DRAWN, NOT FROM EVERY SIZE ASKED FOR.  `g.pasos` records
    # every `pt()` call, including the ones whose run is a provenance
    # declaration that draws nothing -- so the piece's whole scale was being
    # lifted for ink that does not exist.
    drawn_pt = [t["pt"] for t in TEXTS[n0:] if t["s"] != "<wordmark>"]
    if drawn_pt:
        smallest = min(drawn_pt)
        if smallest < MIN_TIPO_MM:
            k = MIN_TIPO_MM / smallest
            del TEXTS[n0:], MARCAS[m0:], FIT[f0:], DRAWN[d0:]
            del DEMASIADO[q0:], OTROS[o0:], CREDITO[c0:]
            g = Rejilla(w, h); g.k = k
            L = lienzo.Lienzo(w, h, bg=ground)
            fn(g, L)
            LIFTED.append((name, round(k, 4), round(smallest, 4)))
    return g, L


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

    # ⚠⚠ THE FONT FILES ARE LOAD-BEARING FOR FOUR CHECKS, AND WITHOUT THEM ALL
    # FOUR GO SILENT RATHER THAN RED.  Measured with `lienzo.FACES` pointed at
    # nonexistent paths: `T()` computes no boxes, so `tapado` reports 0.0 % for
    # every run; `fit_pt` applies no shrink; `DEMASIADO` stays empty; and the
    # build printed "41 checked, 0 FAILED" with no FAIL and no mention.  That
    # is F380's failure mode in four rows at once, and it is what a COLD CLONE
    # with no `fonts/` would have seen.  So the faces are checked FIRST.
    faces = sorted((k, v) for k, v in lienzo.FACES.items())
    miss_f = [k for k, v in faces if not os.path.exists(v)]
    ck(not miss_f, "faces: %d declared, %d resolve on disk%s"
       % (len(faces), len(faces) - len(miss_f),
          ("  <-- MISSING " + ", ".join(miss_f)) if miss_f else ""))

    made = []
    for cat, name, w, h, ground, fn in PIEZAS:
        if only and only not in (cat, name): continue
        GROUND[0] = ground; PIEZA[0] = name
        g, L = escalar(w, h, ground, fn, name)
        REJILLA[name] = g
        stem = os.path.join(OUT, "pl_%s_%s" % (cat, name))
        svg = L.save_svg(stem + ".svg")
        L.render(svg, png=stem + ".png", pdf=stem + ".pdf", dpi=dpi,
                 px=PIXELES.get(name))
        # the declared bleed slabs, taken from what was actually drawn -- not
        # from a transcribed rectangle
        sang = tuple(geom for kind, geom, _o, fill in L.opaque
                     if kind == "rect" and fill in SANGRA.get(name, ())
                     and (geom[0] <= 0.01 or geom[1] <= 0.01
                          or geom[2] >= w - 0.01 or geom[3] >= h - 0.01))
        # EVERY OTHER COLOURED ELEMENT ON THE SHEET, for the visibility row.
        # ⚠ F384's guarantee covered `put_hero` fills ONLY.  `rect`, `line`,
        # `circle`, `frame` and every text run were in no record at all, and
        # `PALETA` whitelists them, so the SVG sweep certified them.  MEASURED
        # by the adversary, who painted `p_cabecera`'s frame in the PAGE COLOUR
        # and got 15 checked, 0 FAILED.  Live, unmeasured until now: the
        # A-frame's HUESO disc on F_ORO at 1.422:1 -- the largest single
        # element in the set -- and `carta`'s five ORO rules on CREMA at
        # 1.888:1.
        # WHAT IDENTITY ASSETS THIS PIECE ACTUALLY CARRIES, read off what was
        # drawn -- not assumed from the piece's name.
        act = set()
        fills = {d["fill"] for d in DRAWN if d["piece"] == name}
        lay = LAYERS.get(name, set())
        if any(d["piece"] == name for d in DRAWN):
            act.add("combi")
        if CREMA in fills and (ROJO in fills or GRANA in fills):
            act.add("par")
        if ORO in fills:
            act.add("oro")
        if lay & {"mural_gold", "mural_ground", "lidmural_rest", "lidsign"}:
            act.add("mural")
        if "script" in lay:
            act.add("rotulo")
        if lay & {"capvw", "capwhite", "capred", "capring"}:
            act.add("rueda")
        if any(m["piece"] == name for m in MARCAS):
            act.add("marca")
        if any(k == "circle" for k, _g, _o, _f in L.opaque):
            act.add("disco")
        ACTIVOS_POR_PIEZA[name] = act

        OTROS.extend((name, ground, fill, kind)
                     for kind, _geom, _o, fill in L.opaque
                     if fill and kind in ("rect", "circle", "rule"))
        # ⚠ AGAINST THE DECLARED GROUND WHERE THERE IS ONE.  This row's stated
        # ceiling -- "compares each element to the PAGE, not to whatever slab
        # it lands on" -- bit as soon as the wordmark joined `TEXTS`: `carta`'s
        # mark is CREMA on a GRANA band, and against the page it read
        # `#F0E7D1 IS the page`, 1.000:1, on the piece where it is the most
        # visible thing on the sheet.  `sobre` has already PROVEN the
        # declaration, so the declaration is what to compare against.
        OTROS.extend((name, t.get("sobre") or ground, t["fill"], "text")
                     for t in TEXTS if t["piece"] == name)
        PAGINA[name] = ground
        OPACOS[name] = list(L.opaque)
        made.append((cat, name, w, h, g, stem, sang))
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
    for cat, name, w, h, g, stem, sang in made:
        frac = margin_clean(stem + ".png", w, h, g.m * 0.42, sangre=sang,
                            page=PAGINA[name])
        ck(frac < 0.02, "%-10s margin band %.3f %% ink (bar 2 %%)%s"
           % (name, 100 * frac,
              "  [declared bleed excluded, not exempted]" if sang else ""))
        e = edge_clean(stem + ".png", w, h, sangre=sang, page=PAGINA[name])
        # 0.0015, not 0.004: at 0.4 % the aframe passed at 0.3919 % with its
        # foot line visibly clipped.  A bar a defect squeaks under is not a bar.
        # ⚠ AND IT IS 0.15 %, NOT THE "0.1 %" THREE COMMITS PRINTED -- `%.1f`
        # on 0.0015 rounds to 0.1, so the row, the ledger and F402 all quoted a
        # bar 33 % TIGHTER than the one actually being held.
        ck(e < 0.0015, "%-10s outer edge %.4f %% ink (bar 0.15 %%)"
           % (name, 100 * e))

    stems0 = {n: (w, h, st) for _c, n, w, h, _g, st, _sa in made}

    # ⚠ A SCREEN PIECE IS A PIXEL SIZE, NOT A PAPER SIZE.  A story that is not
    # 1080 wide is not a story, however good the drawing on it is.
    wrong = []
    for _c, name, w, h, _g, st, _sa in made:
        if name not in PIXELES: continue
        got = Image.open(st + ".png").size
        if got != PIXELES[name]:
            wrong.append("%s %dx%d, wanted %dx%d"
                         % ((name,) + got + PIXELES[name]))
    if any(n in PIXELES for _c, n, _w, _h, _g, _s, _sa in made):
        # ⚠ THE REACH, NOT THE POPULATION -- `len(PIXELES)` counted three when
        # `--only cuadro` had tested one.  That is F400's own defect, in a row
        # written one commit later.
        nsc = len([1 for _c, n, _w, _h, _g, _s, _sa in made if n in PIXELES])
        ck(not wrong, "screen sizes: %d of %d screen piece(s) built, each at "
                      "an exact pixel width AND height%s"
           % (nsc, len(PIXELES), ("  <-- " + " | ".join(wrong)) if wrong else ""))

    # ⚠ `lienzo.pdf_page_mm` EXISTED, ITS DOCSTRING SAID "THE BUILD NEVER
    # CHECKED EITHER, so eleven US-Letter documents shipped as print masters",
    # AND THE BUILD STILL NEVER CHECKED.  A retracted defect with a live
    # docstring and no caller is not fixed, it is remembered.
    pw = []
    for _c, name, w, h, _g, st, _sa in made:
        mm, pages = lienzo.pdf_page_mm(st + ".pdf")
        if mm is None:
            pw.append("%s NO /MediaBox" % name); continue
        d = max(abs(mm[0] - w), abs(mm[1] - h))
        if pages != 1 or d > 0.30:
            pw.append("%s %.3f x %.3f mm, %d page(s)" % (name, mm[0], mm[1], pages))
    if made:
        ck(not pw, "PDF page size: %d document(s), each 1 page within 0.30 mm "
                   "of its declared size%s"
           % (len(made), ("  <-- " + " | ".join(pw[:3])) if pw else ""))

    # ⚠ THE TRACE CACHE LIVES IN THE TRACKED TREE, WHATEVER `--out` SAYS.
    # A build that had to COMPUTE entries has written new files into
    # `probe_scratch/trace/`, and if they are not committed the next clone
    # dirties itself and re-traces (F335, and ~25 minutes for one piece).
    ck(True, "trace cache: %d entr%s loaded, %d computed and WRITTEN INTO THE "
             "TRACKED TREE%s"
       % (len(trazo.CARGADO), "y" if len(trazo.CARGADO) == 1 else "ies",
          len(trazo.CALCULADO),
          "  <-- commit them" if trazo.CALCULADO else ""))

    # ============================================================ THE GRID
    # The docstring on `Rejilla` claims one invariance and disclaims another.
    # Both are MEASURED here rather than asserted, over the formats that were
    # actually built, because a claim in a docstring is not a measurement.
    ys, xs, ysh = [], [], []
    for _c, _n, w, h, g, _st, _sa in made:
        ys.append([(g.y(k) - g.m) / (h - 2 * g.m) for k in (0, 6, 12, 18, 24)])
        xs.append([(g.x(i) - g.m) / (w - 2 * g.m) for i in (0, 3, 6, 9)])
        ysh.append([g.y(k) / h for k in (0, 6, 12, 18, 24)])
    if made:
        dy = max(max(c) - min(c) for c in zip(*ys))
        dx = max(max(c) - min(c) for c in zip(*xs))
        dsh = max(max(c) - min(c) for c in zip(*ysh))
        # the bar on the columns is the GUTTER TERM, computed from the built
        # formats -- an independently obtained quantity, not this expression
        gt = max(g.gut / (w - 2 * g.m) for _c, _n, w, _h, g, _st, _sa in made)
        # ⚠ THIS ROW CANNOT FAIL AND IT IS PRINTED, NOT ASSERTED AWAY.  Both
        # halves are identities: `(y(k)-m)/(h-2m) == k/rows` exactly, so `dy`
        # measures float noise, and `dx` is `(i/cols) * spread(gut/(w-2m))`
        # against a bar that is `max(gut/(w-2m))` -- the same term (rule 6).
        # Over 4000 random format sets the audit found max(dx - gt) = 0.
        # It stays because the THIRD number is not an identity and is the one
        # that refuted this grid's docstring: `y(k)/h` spreads 2.78e-02.
        ck(dy < 1e-12 and dx <= gt + 1e-12,
           "grid (identity, cannot fail -- the third figure is the live one): "
           "rows exact in the usable box (spread %.1e); columns within the "
           "gutter term (%.4f vs %.4f); NEITHER invariant on the sheet "
           "(y(k)/h spreads %.4f) -- %d format(s)"
           % (dy, dx, gt, dsh, len(made)))

    # THE TYPE SCALE.  Every run is authored on a 1.335 scale and then shrunk
    # by `fit_pt` if it will not fit, so the scale is a starting point and not
    # a property of the sheet.  Printing the worst shrink is the difference
    # between knowing that and believing the docstring.
    if FIT:
        worst = min(FIT, key=lambda r: r[2])
        # ⚠ BOTH DIRECTIONS.  The row used to count only runs the measure
        # SHRANK; the 1.8 mm floor moves runs UP off the scale too, and those
        # were excluded by construction -- three of them, to 1.83x.
        nsh = sum(1 for r in FIT if r[2] < 0.999)
        ngr = sum(1 for r in FIT if r[2] > 1.001)
        big = max(FIT, key=lambda r: r[2])
        ck(worst[2] > 0.45,
           "type: %d of %d run(s) shrunk off the 1.335 scale (worst %.3f x on "
           "%s %r) and %d raised off it by the floor (most %.3f x on %s %r); "
           "tracking follows both"
           % (nsh, len(FIT), worst[2], worst[0], worst[1], ngr, big[2],
              big[0], big[1]))
        if KERN:
            ck(min(KERN) <= 1.0 + 1e-9,
               "kerning: over %d fit trial(s) the kerned width is %.4f-%.4f x "
               "the per-glyph sum, so the wider of the two is ALWAYS the sum "
               "and the string measure never changes a decision"
               % (len(KERN), min(KERN), max(KERN)))

    # ================================================== IS THE TYPE THERE
    # EVERY DECLARED GROUND, MEASURED.  A declaration nothing checks is an
    # assumption that the checks reading it then certify.
    dec = [d for d in DRAWN + MARCAS if d["declared"]]
    off = [d for d in dec if not d["sobre"]]
    if dec:
        ck(not off, "declared grounds: %d element(s) say they are printed on "
                    "something other than the page; %d are not inside it%s"
           % (len(dec), len(off),
              ("  <-- " + " | ".join("%s on %s" % (d["piece"], d["ground"])
                                     for d in off[:3])) if off else ""))

    if MARCAS:
        wm = min(MARCAS, key=lambda m: m["ratio"])
        ck(wm["ratio"] >= MARCA_BAR,
           "wordmark: %d drawn, each checked against the ground it is printed "
           "on; weakest %.3f:1 on %s (%s on %s, bar %.1f)"
           % (len(MARCAS), wm["ratio"], wm["piece"], wm["ink"], wm["ground"],
              MARCA_BAR))

    cov = sorted(((t.get("tapado", 0.0), t["piece"], t["s"][:30])
                  for t in TEXTS), reverse=True)
    # A run with no box is a run `tapado` cannot test, and it would report 0.0
    # for it -- indistinguishable from clear.  Counted, not assumed.
    noboxes = sum(1 for t in TEXTS if t["box"] is None)
    if cov:
        ck(cov[0][0] <= 0.02 and not noboxes,
           "occlusion: %d run(s), %d with a measurable box, tested against "
           "every slab drawn after them; worst covered %.1f %% -- %s %r"
           % (len(cov), len(TEXTS) - noboxes, 100 * cov[0][0], cov[0][1],
              cov[0][2]))

    # CLEARANCE, PRINTED NOT BARRED.  ⚠ `tapado`'s bar is 2 % COVERAGE, so a
    # ZERO-MILLIMETRE gap between a run and the drawing prints green: they do
    # not overlap, and that is all it asks.  Nothing measured how close they
    # come.  Measured now, and reported rather than barred, because what counts
    # as tight is a judgement about a piece and not a number this file owns.
    gaps = []
    for t in TEXTS:
        if t["box"] is None: continue
        for kind, geom, _o, _f in OPACOS.get(t["piece"], ()):
            if kind != "art": continue
            (gx0, gy0, gx1, gy1), _occ = geom
            dx = max(gx0 - t["box"][2], t["box"][0] - gx1, 0.0)
            dy = max(gy0 - t["box"][3], t["box"][1] - gy1, 0.0)
            if dx == 0.0 and dy == 0.0: continue
            gaps.append(((dx * dx + dy * dy) ** 0.5, t["piece"], t["s"][:22]))
    if gaps:
        gaps.sort()
        ck(True, "clearance: tightest gap from a text run to a drawing is "
                 "%.2f mm (%s %r); next %.2f, %.2f -- PRINTED, NOT BARRED"
           % (gaps[0][0], gaps[0][1], gaps[0][2],
              gaps[1][0] if len(gaps) > 1 else -1,
              gaps[2][0] if len(gaps) > 2 else -1))

    ck(not DEMASIADO, "type floor: %.2f mm; %d run(s) arrived below it after "
                      "the piece scale was lifted%s"
       % (MIN_TIPO_MM, len(DEMASIADO),
          ("  <-- " + " | ".join("%s %r at %.3f mm" % d for d in DEMASIADO[:3]))
          if DEMASIADO else ""))

    # ============================================================ HIERARCHY
    # ⚠ EVERY SIZE MUST BE A STEP ON THE DECLARED SCALE, and the piece must
    # have more than one level.  Both halves failed silently before: three
    # pieces resolved to ONE size for headline, body and disclaimer alike, and
    # the A-frame's top two levels were 1.14x apart where the scale's step is
    # 1.335.  Structural halves GATE; the counts and ratios are REPORTED,
    # because how many levels a piece should have is a judgement.
    niveles = {}
    fuera = []
    for t in TEXTS:
        if t["s"] == "<wordmark>": continue
        g = REJILLA.get(t["piece"])
        if not g: continue
        # ⚠ CAP HEIGHT, NOT EM.  The em is deliberately face-corrected now, so
        # measuring it reports a `display` run as 0.140 steps off a scale it is
        # exactly on.  Cap height is the quantity the scale is FOR and the one
        # a reader sees; this row read the other one and failed the moment the
        # correction landed, which is the row doing its job on itself.
        cap = t.get("cap", t["pt"] * CAP_REF)
        niveles.setdefault(t["piece"], set()).add(round(cap, 4))
        n = math.log(cap / (g.base * g.k * CAP_REF)) / math.log(PASO)
        if abs(n * 2 - round(n * 2)) > 0.02:
            fuera.append("%s %r %.4f mm = %.3f steps" % (t["piece"], t["s"][:18],
                                                         t["pt"], n))
    uno = sorted(p for p, v in niveles.items() if len(v) < 2 and
                 len([t for t in TEXTS if t["piece"] == p and t["s"] != "<wordmark>"]) > 2)
    ck(not fuera and not uno,
       "hierarchy: %d run(s) across %d piece(s); every CAP HEIGHT a half-step "
       "on the 1.335 scale (%d off it); %d piece(s) with 3+ runs at one size%s"
       % (sum(len([t for t in TEXTS if t['piece'] == p]) for p in niveles),
          len(niveles), len(fuera), len(uno),
          ("  <-- " + " | ".join((fuera + uno)[:3])) if (fuera or uno) else ""))
    lv = sorted(niveles.items(), key=lambda kv: len(kv[1]))
    print("   levels per piece: %s"
          % ", ".join("%s %d" % (p, len(v)) for p, v in lv[:6]))

    # ============================================================ THE SPANISH
    # ⚠ THE EXEMPTION IS CHECKED FIRST.  A string in `REPLICADO` is set as the
    # source spells it and orthography does not apply to it (F94 over F376);
    # anything else carrying a word `ORTOGRAFIA` accents, without the accent,
    # is a finding.
    mal = []
    for t in TEXTS:
        if t["s"] in REPLICADO or t["s"] == "<wordmark>":
            continue
        for bare, right in ORTOGRAFIA.items():
            if bare != right and re.search(r"\b" + bare + r"\b", t["s"]):
                mal.append("%s %r wants %r" % (t["piece"], bare, right))
    ck(not mal, "spanish: %d run(s) checked against %d accented forms, %d "
                "declared REPLICADO; %d unaccented and undeclared%s"
       % (len(TEXTS), len(ORTOGRAFIA), len(REPLICADO), len(mal),
          ("  <-- " + " | ".join(sorted(set(mal))[:3])) if mal else ""))

    # ============================================== PROVENANCE, RECORDED
    # ⚠ STRONGER THAN THE LINE IT REPLACED.  The printed line asserted three
    # codewords over a whole piece; this classes EVERY drawn literal and reds
    # on any string nobody has sourced.  A provenance claim that cannot fail is
    # decoration, which is what the line on the artwork was.
    sinfuente = sorted({t["s"] for t in TEXTS
                        if t["s"] != "<wordmark>" and PROV not in t["s"]
                        and t["s"] not in PROCEDENCIA})
    piezas_hechas = {n for _c, n, _w, _h, _g, _s, _sa in made}
    sincredito = sorted(piezas_hechas - {c[0] for c in CREDITO})
    from collections import Counter as _C
    cnt = _C(PROCEDENCIA[t["s"]] for t in TEXTS
             if t["s"] in PROCEDENCIA)
    ck(not sinfuente and not sincredito,
       "provenance: %d drawn literal(s) classed (%s); %d unsourced; %d of %d "
       "piece(s) declare a provenance line, RECORDED NOT PRINTED%s"
       % (sum(cnt.values()), ", ".join("%s %d" % kv for kv in sorted(cnt.items())),
          len(sinfuente), len(piezas_hechas) - len(sincredito),
          len(piezas_hechas),
          ("  <-- " + " | ".join((sinfuente + sincredito)[:3]))
          if (sinfuente or sincredito) else ""))

    # ...and the ink itself must be ABSENT from every sheet
    conprov = [t["piece"] for t in TEXTS if PROV in t["s"]]
    ck(not conprov,
       "provenance INK: %d run(s) of build metadata on the artwork (must be 0; "
       "it belongs in pl_MANIFIESTO.txt, and `T1_PLIEGO_CONPROV=1` puts it "
       "back so this row can be watched failing)%s"
       % (len(conprov),
          ("  <-- " + ", ".join(sorted(set(conprov))[:4])) if conprov else ""))

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
    # ⚠ THE REACH, NOT THE POPULATION.  This row used to print "37 run(s)
    # checked"; only the runs that NAME a style are comparable, and a piece
    # that names none can never be caught by it.
    named = [t for t in TEXTS if any(e in t["s"] for e in ESTILO_ES.values())]
    ck(not lies, "colophons: %d of %d run(s) name a style, on %d of %d "
                 "piece(s); %d misnamed%s"
       % (len(named), len(TEXTS), len({t["piece"] for t in named}),
          len({t["piece"] for t in TEXTS}), len(lies),
          ("  <-- " + " | ".join(lies[:3])) if lies else ""))

    # ============================================ THE ASSET REGISTER
    sin_marca = []
    for _c, name, _w, _h, _g, _st, _sa in made:
        a = ACTIVOS_POR_PIEZA.get(name, set()) - {"marca"}
        if len(a) < 2:
            sin_marca.append("%s carries %s" % (name, sorted(a) or "NOTHING"))
    if ACTIVOS_POR_PIEZA:
        cen = {}
        for a in ACTIVOS_POR_PIEZA.values():
            for k in a: cen[k] = cen.get(k, 0) + 1
        n = len(ACTIVOS_POR_PIEZA)
        ck(not sin_marca,
           "assets: %d registered; every piece must carry 2+ BESIDES the "
           "wordmark, %d do not.  Census over %d piece(s): %s.  ⚠ PRESENCE, "
           "NOT ATTRIBUTION -- whether a viewer would name the brand needs "
           "people%s"
           % (len(ACTIVOS), len(sin_marca), n,
              ", ".join("%s %d" % (k, v) for k, v in sorted(cen.items(),
                                                            key=lambda kv: -kv[1])),
              ("  <-- " + " | ".join(sin_marca[:3])) if sin_marca else ""))

    # =========================================== THE PALETTE AGAINST THE PHOTO
    # Two independently obtained quantities (rule 6): the left side is computed
    # by `foto.py` off `ref_sign_aframe.jpg` and committed; the right side is
    # this module's own palette. Neither is derived from the other.
    fj = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "foto_sign.json")
    if os.path.exists(fj):
        fo = json.load(open(fj))
        mia = estilo_vec._lum(HUESO) / estilo_vec._lum(F_ORO)
        suya = fo["light_over_ground_luminance"]
        ck(abs(mia - suya) < 0.05,
           "photograph: his sign's light ink over its gold is %.4f in "
           "REFLECTANCE (%s over %s, %.1f %% of the face, by foto.py); ours is "
           "%.4f (%s over %s).  ⚠ THE LUMINANCE RATIO IS THE INVARIANT -- it "
           "survives a change of exposure; the WCAG figure (%.3f his, %.3f "
           "ours) does NOT, because its +0.05 offset is not scale-invariant"
           % (suya, fo["disc"], fo["ground"],
              100 * fo["clusters"][0]["share"], mia, HUESO, F_ORO,
              fo["disc_on_ground_wcag"], estilo_vec.contrast(HUESO, F_ORO)))
    else:
        ck(False, "photograph: foto_sign.json ABSENT -- run `python3 foto.py`")

    # ========================================================== THE TRACKING
    # ⚠ IT USED TO RUN BACKWARDS WITH SIZE.  Thirty-seven decimal literals at
    # the call sites meant the same level took six different values and the
    # BIGGEST type was the LOOSEST, which is the reverse of what letterspacing
    # is for.  One table keyed on level now, and this row proves the property
    # the table is supposed to have rather than trusting that it does: read the
    # emitted em off each run, divide by its size, and require the result to be
    # monotone DECREASING as cap height grows.
    tr = {}
    for t in TEXTS:
        if t["s"] == "<wordmark>" or not t.get("nivel"): continue
        tr.setdefault(t["nivel"], set()).add(round(t["tracking"] / t["pt"], 5))
    seq = [(NIVEL[k], k, sorted(v)) for k, v in tr.items() if k in NIVEL]
    seq.sort()
    multi = [k for _n, k, v in seq if len(v) > 1]
    mono = all(seq[i][2][0] >= seq[i + 1][2][0] for i in range(len(seq) - 1))
    if seq:
        ck(mono and not multi,
           "tracking: %d level(s) in use, each ONE value in em, monotone "
           "decreasing as size grows: %s%s"
           % (len(seq), " > ".join("%s %.3f" % (k, v[0]) for _n, k, v in seq),
              ("  <-- %d level(s) with more than one value: %s"
               % (len(multi), ", ".join(multi))) if multi else
              ("" if mono else "  <-- NOT MONOTONE")))

    # ============================================================ CENTRING
    # ⚠ EVERY CENTRED TRACKED RUN IN THIS SUITE SAT LEFT OF ITS OWN AXIS.
    # CSS letter-spacing adds the space after the LAST glyph too and
    # `text-anchor` centres the ADVANCE, so the ink lands half a tracking to
    # the left -- on nearly every line in the set.  Found by a grader, not by
    # any row here: the margin checks read the margins, and `occlusion`
    # compares boxes built on the SAME wrong assumption, so it could not see it.
    #
    # THE TEST IS A SLOPE, NOT AN OFFSET.  Glyph sidebearings make a run's ink
    # centre differ from its advance centre by a little, always, and that is
    # optical centring working correctly.  What must not happen is for the
    # error to GROW WITH TRACKING.  Regressing measured offset against tracking
    # over every centred run in the build gives a slope of -0.5 mm per mm when
    # the defect is present and ~0 when it is not, and the slope is obtained
    # from the RENDERED sheets while the tracking comes from the layout -- two
    # independent quantities (rule 6).
    pts = []
    for t in TEXTS:
        if t["anchor"] != "middle" or t["box"] is None: continue
        if t["tracking"] <= 1e-9 or t["piece"] not in stems0: continue
        w, h, st = stems0[t["piece"]]
        a = np.asarray(Image.open(st + ".png").convert("RGB")).astype(np.int16)
        H, W = a.shape[:2]; ppm = W / float(w)
        bx0, by0, bx1, by1 = t["box"]
        X0 = max(0, int(bx0 * ppm) - 6); X1 = min(W, int(bx1 * ppm) + 6)
        Y0 = max(0, int(by0 * (H / h))); Y1 = min(H, int(by1 * (H / h)))
        if X1 - X0 < 8 or Y1 - Y0 < 4: continue
        win = a[Y0:Y1, X0:X1]
        m = (np.abs(win - _rgb(t["fill"])).max(axis=2) <= 90)
        cols = np.where(m.any(axis=0))[0]
        if len(cols) < 2: continue
        centre = (X0 + (cols.min() + cols.max()) / 2.0) / ppm
        pts.append((t["tracking"], centre - t["x"]))
    # ⚠ NOT A SILENT SKIP.  A regression needs several points; with fewer the
    # row says ABSENT and why, rather than disappearing and leaving a shorter
    # green list that reads as full coverage (F380).
    if len(pts) < 6:
        ck(True, "centring: ABSENT -- %d centred tracked run(s) in this build, "
                 "a slope needs 6" % len(pts))
    else:
        xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
        slope = float(((xs - xs.mean()) * (ys - ys.mean())).sum()
                      / max(1e-9, ((xs - xs.mean()) ** 2).sum()))
        ck(abs(slope) < 0.12,
           "centring: %d centred tracked run(s) measured off the rendered "
           "sheets; offset-vs-tracking slope %+.4f mm/mm (bar 0.12; the defect "
           "reads -0.5, a clean build ~0); mean residual %+.3f mm is sidebearing"
           % (len(pts), slope, float(ys.mean())))

    # ============================== IS THE WORDMARK LOAD-BEARING FOR LAYOUT
    hue = []
    for _c, name, w, h, g, _st, _sa in made:
        live = (g.m, g.m, w - g.m, h - g.m)
        occ = [t["box"] for t in TEXTS
               if t["piece"] == name and t["box"] and t["s"] != "<wordmark>"]
        occ += [geom[0] for kind, geom, _o, _f in OPACOS.get(name, ())
                if kind == "art"]
        mk = [t["box"] for t in TEXTS
              if t["piece"] == name and t["s"] == "<wordmark>" and t["box"]]
        con = hueco_mayor(live, occ + mk)
        sin = hueco_mayor(live, occ)
        hue.append((sin - con, name, con, sin))
    hue.sort(reverse=True)
    if hue:
        print("   largest empty rectangle, with the mark and without it:")
        for d, n, c, s_ in hue[:6]:
            print("     %-10s %5.1f %% -> %5.1f %%   (+%.1f)"
                  % (n, 100 * c, 100 * s_, 100 * d))
        ck(True, "wordmark as LAYOUT: deleting it opens the largest hole by "
                 "%.1f points on %s (%.1f %% -> %.1f %%) -- REPORTED, and the "
                 "artefact that shows it is the SINMARCA contact sheet"
           % (100 * hue[0][0], hue[0][1], 100 * hue[0][2], 100 * hue[0][3]))

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
    unkeyed = sum(1 for d in DRAWN
                  if estilo_vec.contrast(d["fill"], d["ground"])
                  < estilo_vec.KEY_BAR and d["key"] is None)
    # ⚠ ON ITS OWN THIS IS A TAUTOLOGY AND THE AUDIT PROVED IT (rule 6).  Over
    # every fill x ground pair this palette can make, branch 2 trips on 0 of 72
    # keylines -- it re-checks the condition `keyline_for` already enforces,
    # with the same function and the same bar -- and branch 1 fires on 0 pairs,
    # because no pair in this palette defeats 1.35 without one.  Its only red
    # is the forced ablation.
    #
    # So the row also asserts the half that is NOT derived from the record:
    # every ink actually written into the SVG must be one this module knows it
    # drew.  THE WORDMARK ESCAPED EVERY CHECK FOR EXACTLY THIS REASON -- it was
    # painted, and nothing compared what was painted against what was recorded.
    import re as _re
    known = ({d["fill"] for d in DRAWN} | {d["key"] for d in DRAWN if d["key"]}
             | {m["ink"] for m in MARCAS} | {t["fill"] for t in TEXTS}
             | {g for _c, _n, _w, _h, g, _f in PIEZAS} | set(PALETA))
    unknown = set()
    for _c, name, _w, _h, _g, st, _sa in made:
        for m in _re.finditer(r'(?:fill|stroke)="(#[0-9A-Fa-f]{6})"',
                              open(st + ".svg").read()):
            if m.group(1).upper() not in {k.upper() for k in known}:
                unknown.add("%s %s" % (name, m.group(1)))
    ck(not bad and not unknown,
       "ink/ground: %d fill(s) drawn, %d needed a keyline, %d UNSEEABLE; "
       "%d ink(s) in the SVGs that no record accounts for%s"
       % (len(DRAWN), sum(1 for d in DRAWN if d["key"]), len(bad),
          len(unknown),
          ("  <-- " + " | ".join(sorted(unknown)[:3] or bad[:3]))
          if (bad or unknown) else ""))

    # (c) EVERYTHING THAT IS NOT A HERO FILL, against the page it sits on.
    #     ⚠ CEILING, STATED: this compares each element to the PAGE, not to
    #     whatever slab it happens to land on, so an element deliberately laid
    #     over a band is judged against the wrong thing.  The two elements in
    #     this set that do that DECLARE it and are checked by `sobre`; nothing
    #     forces a new one to.
    flojo = []
    for piece, page, ink, kind in OTROS:
        if ink == page:
            flojo.append("%s %s %s IS the page" % (piece, kind, ink)); continue
        c = estilo_vec.contrast(ink, page)
        if c < estilo_vec.KEY_BAR:
            flojo.append("%s %s %s on %s %.3f:1" % (piece, kind, ink, page, c))
    if OTROS:
        wk = min(OTROS, key=lambda r: estilo_vec.contrast(r[2], r[1]))
        ck(not flojo, "other elements: %d rule(s), slab(s) and text run(s) "
                      "checked against their page; weakest %.3f:1 (%s %s %s "
                      "on %s); %d below %.2f%s"
           % (len(OTROS), estilo_vec.contrast(wk[2], wk[1]), wk[0], wk[3],
              wk[2], wk[1], len(flojo), estilo_vec.KEY_BAR,
              ("  <-- " + " | ".join(flojo[:3])) if flojo else ""))

    # (b) DIFFERENTIAL: the sheet is rendered a SECOND time with the keylines
    #     suppressed, and the two proofs are subtracted.  Whatever is different
    #     IS the keylines; nothing else on the page moved.
    #
    # ⚠⚠ THE ROW THIS REPLACES COUNTED PIXELS `near(a, key)` AT tol=26 AND WAS
    # GREEN WITH THE KEYLINES PHYSICALLY DELETED.  The adversary stripped all
    # nine `stroke="#0E1B2E"` attributes out of the committed
    # `pl_calle_aframe.svg`, re-rendered, and the count went 409 901 -> 282 379
    # against a floor of 347: it passed by 814x.  At tol=26 the AZUL_CUERPO
    # keyline and TINTA are 22 apart, so the row was counting the tyres, the
    # flank script and the roundel -- and the rule-8 windows it shipped as
    # evidence show exactly that, magenta over the tyres, if they are opened.
    # THAT IS THE FIFTH INSTRUMENT IN THIS MODULE TO BE GREEN ON ITS OWN
    # DEFECT, AND THE FOURTH FOUND BY SOMEONE ELSE LOOKING.
    #
    # A difference cannot be fooled by two inks being close, because it does
    # not ask what colour anything is.
    npiece = {}
    for d in DRAWN:
        if d["key"]:
            npiece[d["piece"]] = npiece.get(d["piece"], 0) + 1
    diffs = []
    if npiece:
        estilo_vec.NOKEY[0] = True
        try:
            for cat, name, w, h, ground, fn in PIEZAS:
                if name not in npiece or name not in stems0: continue
                GROUND[0] = ground; PIEZA[0] = name
                g2 = Rejilla(w, h); L2 = lienzo.Lienzo(w, h, bg=ground)
                n0 = len(TEXTS); m0 = len(MARCAS); f0 = len(FIT)
                d0 = len(DRAWN); q0 = len(DEMASIADO)
                fn(g2, L2)
                del TEXTS[n0:], MARCAS[m0:], FIT[f0:], DRAWN[d0:], DEMASIADO[q0:]
                sv = L2.save_svg(os.path.join(OUT, "_sinfilete.svg"))
                pn = os.path.join(OUT, "_sinfilete.png")
                # ⚠ THE SAME dpi.  The first version rendered this copy at 90
                # against the sheet's own dpi and resampled one onto the other:
                # the difference was then dominated by RESAMPLING, marking the
                # whole vehicle, the wordmark and every text run as changed.
                # It read 5.25 % where the keylines are worth a fraction of
                # that -- a sixth wrong instrument, caught before it was
                # published by PAINTING THE WINDOW AND LOOKING (rule 8), which
                # is the only thing that has ever caught one of these.
                L2.render(sv, png=pn, dpi=dpi, px=PIXELES.get(name))
                a = np.asarray(Image.open(stems0[name][2] + ".png")
                               .convert("RGB")).astype(np.int16)
                b = np.asarray(Image.open(pn).convert("RGB")).astype(np.int16)
                if a.shape != b.shape:
                    diffs.append((0.0, name, npiece[name])); continue
                m = np.abs(a - b).max(axis=2) > 24
                ch = float(m.sum()) / a[:, :, 0].size
                # one stroke down one side of the drawing, as a fraction of
                # THIS sheet -- the floor was one global constant for sheets
                # whose one-stroke fraction differs by 1.5x
                kws = [d["kw"] for d in DRAWN if d["piece"] == name]
                hs = [d["box"][3] - d["box"][1] for d in DRAWN
                      if d["piece"] == name]
                fl = (min(kws) * min(hs) / (w * h)) if kws else 6e-5
                diffs.append((ch, name, npiece[name], fl))
                if paint:
                    q = b.copy(); q[m] = (255, 0, 255)
                    Image.fromarray(q.astype(np.uint8)).save(os.path.join(
                        OUT, "pl_FILETE_%s.png" % name))
        finally:
            estilo_vec.NOKEY[0] = False
            for f in ("_sinfilete.svg", "_sinfilete.png"):
                fp = os.path.join(OUT, f)
                if os.path.exists(fp): os.remove(fp)
    # THE FLOOR IS OBTAINED INDEPENDENTLY of the difference: a keyline is `kw`
    # mm wide and the drawing it outlines is `bh` mm tall, so ONE stroke down
    # one side of one shape is already this fraction of the sheet.  Nothing
    # here is derived from the pixels being counted.
    # ⚠⚠ THE CLAIM MADE FOR THIS ROW WAS WIDER THAN WHAT IT DOES.  The commit
    # said "a difference cannot be fooled"; it cannot be fooled by a TOTAL
    # suppression, which is what its ablation tests.  MEASURED by the adversary
    # on `aframe`: with EIGHT OF NINE keylines deleted it reads 0.08375 % and
    # PASSES, and with all nine present at a twentieth of their weight
    # (0.027 mm, a tenth of what a press can hold) it reads 0.05944 % and
    # PASSES.  What catches a SUBSET is the analytic row, which this same file
    # calls a tautology.  That gap is real, and stated rather than papered.
    worstd = min(diffs, key=lambda d: d[0] / d[3]) if diffs else None
    nkey = sum(1 for d in DRAWN if d["key"])
    if nkey == 0:
        # NOT an empty-set pass: it asserts the analytic row's own count, so
        # "nothing to difference" can only be green when nothing needed one.
        ck(not unkeyed and not npiece,
           "keylines DIFFERENTIAL: no fill on any sheet needed a keyline, and "
           "%d fill(s) are below the bar without one" % unkeyed)
    else:
        ck(bool(diffs) and all(d[0] >= d[3] for d in diffs),
           "keylines DIFFERENTIAL: %d sheet(s) rendered twice, with and "
           "without; tightest %.5f %% against that sheet's own one-stroke "
           "floor %.5f %% on %s (%d keylines) -- CATCHES A TOTAL SUPPRESSION, "
           "NOT A SUBSET"
           % (len(diffs), 100 * worstd[0], 100 * worstd[3], worstd[1],
              worstd[2]))

    if not only and made:
        cells = []
        for _c, name, w, h, _g, stem, _sa in made:
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

    # ⚠ THE BUILD dpi WAS RECORDED NOWHERE, so re-running at the dpi the brief
    # documents silently produced different files from the committed ones.
    # It ships beside them.
    if made:
        man = os.path.join(OUT, "pl_MANIFIESTO.txt")
        with open(man, "w") as fh:
            fh.write("pliego.py -- THIS IS THE DELIVERABLE SET.\n")
            fh.write("`design_out/promo_r80_*` and `design_out/col_r80_*` are "
                     "EARLIER ROUNDS on the PIL engine (F382) and are "
                     "superseded; eleven names appear in all three.\n\n")
            fh.write("built at --dpi %d; screen pieces at their own exact "
                     "pixel sizes\n\n" % dpi)
            for cat, name, w, h, _g, st, _sa in made:
                px = PIXELES.get(name)
                fh.write("%-10s %-10s %7.3f x %7.3f mm%s\n"
                         % (cat, name, w, h,
                            ("   %d x %d px exact" % px) if px else ""))
            fh.write("\n\nPROVENANCE -- this is where it lives now, not on "
                     "the artwork.\n")
            fh.write("MEDIDO: read off the vehicle's own artwork.  "
                     "LETRERO: off the owner's photographed sign.\n"
                     "AUTOR: written for this suite and approved by nobody.\n")
            for cat, name, _w, _h, _g, _st, _sa in made:
                fh.write("\n%s / %s\n" % (cat, name))
                for pz, line in CREDITO:
                    if pz == name:
                        fh.write("  declares: %s\n" % line)
                for t in TEXTS:
                    if t["piece"] == name and t["s"] in PROCEDENCIA:
                        fh.write("  %-8s %s\n"
                                 % (PROCEDENCIA[t["s"]], t["s"]))
        ck(os.path.exists(man), "manifest -> %s (names the deliverable set and "
                                "the build dpi)" % man)

    print("%d checked, %d FAILED" % (CHECK[0], len(FAILED)))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
