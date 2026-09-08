"""
promo.py -- a COLLECTION OF PROMOTIONAL IMAGES built on the combi.

WHY THIS EXISTS.  The owner supplied a photograph of a real Tacombi A-frame
sidewalk sign (`ref_sign_aframe.jpg`) and said: *"I simply want a collection of
promotional images utilizing the combi.  Very similar to this sign, but I want
to make it special, distinguished in a way."*  He then corrected a first reading
of that brief: *"It's not about the palette, it's just an example of a
promotional product."*  So the photograph fixes the CATEGORY -- printed
promotional pieces with the vehicle on them -- and NOT the colours.

WHAT MAKES THESE DIFFERENT FROM THE EXAMPLE, STATED SO IT CAN BE ARGUED WITH.
The example sign carries a stock cartoon panel van in cream and pale blue: it is
not this vehicle, and it is not any vehicle in particular.  Every piece here
carries THE ACTUAL BUS -- the mural lid, the folk-art scrollwork, the Senor
Tacombi script, the 100% Calidad sunburst, the open serving counter -- because
that asset is what this project has and what nobody else has.  The example also
says four things at once (name, offer, QR, app).  Each piece here says ONE.

THE VEHICLE IS AN UNDERLAY (F361).  Nothing here re-poses or re-lights the
model.  The art is drawn from the TRACKED captures in `probe_scratch/sticker/`,
so this module runs on a cold clone with no Blender at all.

CEILINGS, STATED (rule 12):
  * TYPE.  ⚠⚠ **THIS MODULE'S ORIGINAL TYPE CEILING WAS FALSE IN BOTH HALVES
    AND IS RETRACTED HERE, IN THE SOURCE THAT CARRIED IT (rule 13, F371).**  It
    said *"Bitstream Charter is present only as Type1 `.pfb`, WHICH PIL CANNOT
    LOAD, and fonts.google.com is refused by the egress proxy"*.  MEASURED:
    `ImageFont.truetype('/usr/share/fonts/X11/Type1/c0632bt_.pfb', 48)` loads
    and returns `('Bitstream Charter', 'Bold')` on PIL 12.3.0, rendering 7702
    ink px of `Señor Tacombi 100% Calidad` with accents.  And the CDN test was
    aimed at the wrong host: `fonts.google.com` is the marketing site;
    `https://fonts.googleapis.com/css?family=...` returns **200** and hands back
    `fonts.gstatic.com` `.ttf` URLs that PIL opens directly.  NEITHER HALF WAS
    EVER TESTED -- both were asserted from memory and then quoted as
    "(measured: CONNECT 403)", which is rule 10 committed inside a ceiling
    statement.  Real faces now ship in `fonts/`.
  * VIEWPOINT.  Three captures exist -- `side` (az 90), `flank` (az 72),
    `nose`.  Every piece draws one of those three.  A piece wanting any other
    angle needs a new capture, which needs Blender.
  * THESE ARE PROOFS, NOT PRINT MASTERS.  They are RGB PNG at screen scale with
    no bleed, no trim marks and no separation.  `sheet.py` is the module that
    emits print masters; nothing here goes near a press.
  * NOTHING IN THIS TREE CAN GRADE A PROMOTIONAL IMAGE.  There is no check here
    that says a piece is any good.  The owner is the instrument.
"""
import os, sys, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

CAP = "probe_scratch/sticker"
OUT = "design_out"
CHECK = [0]; FAILED = []

def ck(cond, msg):
    CHECK[0] += 1
    if not cond:
        FAILED.append(msg); print("  FAIL  %s" % msg)
    else:
        print("  ok    %s" % msg)

# --------------------------------------------------------------- the palette
# AUTHORED, not sampled.  The owner ruled the example sign is not a colour
# reference, so nothing here is measured off it.  These are chosen to sit in the
# vehicle's own register -- its red, its cream, its ochre scrollwork.
INK   = (38, 30, 28)        # warm near-black, the drawing ink
CREMA = (243, 233, 211)
AMBAR = (219, 160, 44)
ROJO  = (158, 38, 31)
AZUL  = (33, 52, 88)
VERDE = (48, 88, 72)
PAPEL = (238, 228, 206)

_HERE = os.path.dirname(os.path.abspath(__file__))
F = {
 "disp":  os.path.join(_HERE, "fonts", "Alfa.ttf"),      # Alfa Slab One, OFL
 "cond":  os.path.join(_HERE, "fonts", "Oswald.ttf"),    # Oswald, OFL
 "serif": "/usr/share/fonts/X11/Type1/c0648bt_.pfb",     # Bitstream Charter
 "sans":  os.path.join(_HERE, "fonts", "Oswald.ttf"),
 "sansb": os.path.join(_HERE, "fonts", "Oswald.ttf"),
}
def font(key, px):
    p = F[key]
    if not os.path.exists(p):
        raise SystemExit("NO FONT: %s absent.  promo.py REFUSES to substitute "
                         "-- every metric here is set in this face (rule 37)." % p)
    return ImageFont.truetype(p, px)

# ------------------------------------------------------------- letterspacing
def ls_width(f, s, ls):
    if not s: return 0
    w = sum(f.getlength(c) for c in s) + ls * (len(s) - 1)
    return w

# Every text run records its own box here.  THIS EXISTS BECAUSE THE FIRST
# DRAFT SHIPPED `02_cartel` WITH THE WORDMARK OVERFLOWING BOTH MARGINS -- it
# read "SEÑOR TACOMB", the I cut off by the page edge -- with ALL FIFTEEN
# CHECKS GREEN ON IT.  Not one of them measured type against the frame.  A
# green check is not evidence about a drawing (rule 2); this is the check that
# would have caught it, and it was WATCHED FAILING on that exact defect before
# the defect was fixed (rule 3).
TEXTBOX = []
OBSTACLE = []          # (piece, label, x0,y0,x1,y1) -- art no text may cross
_CUR = {"piece": None, "safe": None}

def piece_frame(name, safe):
    _CUR["piece"] = name; _CUR["safe"] = safe


def ls_text(d, xy, s, f, fill, ls=0, anchor="lt"):
    """Letterspaced text.  PIL has no tracking, so glyphs are placed one at a
    time.  anchor: first char is l/m/r horizontally, t/m/b vertically."""
    x, y = xy
    w = ls_width(f, s, ls)
    a = f.getbbox("Hxy")
    if anchor[0] == "m": x -= w / 2.0
    elif anchor[0] == "r": x -= w
    if anchor[1] == "m": y -= (a[3] + a[1]) / 2.0
    elif anchor[1] == "b": y -= a[3]
    x0 = x
    top = y + a[1]; bot = y + a[3]
    for c in s:
        d.text((x, y), c, font=f, fill=fill)
        x += f.getlength(c) + ls
    if _CUR["piece"]:
        TEXTBOX.append((_CUR["piece"], s, x0, top, x0 + w, bot, _CUR["safe"]))
    return w

# ------------------------------------------------------------- the vehicle
_CACHE = {}

def load_capture(tag):
    if tag in _CACHE: return _CACHE[tag]
    need = ["%s_alpha_0001.png", "%s_albedo_0001.png"]
    for n in need:
        p = os.path.join(CAP, n % tag)
        if not os.path.exists(p):
            raise SystemExit("ABSENT: %s.  The tracked captures are what this "
                             "module draws from; without them there is no art "
                             "and promo.py REFUSES to invent one." % p)
    al = np.asarray(Image.open(os.path.join(CAP, "%s_alpha_0001.png" % tag)
                               ).convert("L")) > 127
    ab = np.asarray(Image.open(os.path.join(CAP, "%s_albedo_0001.png" % tag)
                               ).convert("RGB"))
    lp = os.path.join(CAP, "%s_lines.json" % tag)
    st = json.load(open(lp))["strokes"] if os.path.exists(lp) else []
    _CACHE[tag] = (al, ab, st)
    return _CACHE[tag]

def combi(tag, height, lift=1.14, ring=2, ss=3, ink=INK):
    """The vehicle as flat colour with a drawn contour, at `height` px tall.

    WHY FLAT ALBEDO AND NOT THE SHADED PASS, WATCHED RATHER THAN ASSUMED.  Four
    treatments were built and looked at side by side (`flat`, two posterised
    quantisations at K=6 and K=10, and the shaded pass).  Quantising MUDDIED the
    mural lid -- its red flowers went to brown at K=6 -- and overlaying the full
    line pass laid grime across the cream upper body and blunted the 100%
    Calidad sunburst.  Flat albedo plus an outer contour only was the cleanest
    and is what ships.  The contour is grown from the ALPHA, not drawn from the
    line pass, so it is the silhouette and nothing else.
    """
    al, ab, st = load_capture(tag)
    H, W = al.shape
    img = Image.fromarray(ab).convert("RGB")
    if lift != 1.0:
        img = ImageEnhance.Color(img).enhance(lift)
    img = img.convert("RGBA")
    A = Image.fromarray((al * 255).astype(np.uint8))
    img.putalpha(A)
    big = img.resize((W * ss, H * ss), Image.LANCZOS)
    if ring > 0:
        m = A.resize((W * ss, H * ss), Image.LANCZOS).point(lambda v: 255 if v > 127 else 0)
        grown = m.filter(ImageFilter.MaxFilter(ring * 2 + 1))
        canvas = Image.new("RGBA", big.size, (0, 0, 0, 0))
        canvas.paste(Image.new("RGBA", big.size, tuple(ink) + (255,)), (0, 0), grown)
        big = Image.alpha_composite(canvas, big)
    bb = big.getbbox(); big = big.crop(bb)
    w = max(1, int(round(big.width * height / float(big.height))))
    return big.resize((w, height), Image.LANCZOS)

# ---------------------------------------------------------------- furniture
def ground_shadow(im, v, x, y, colour=(0, 0, 0), op=52, squash=0.052, grow=1.02):
    """A soft ellipse under the wheels.  AUTHORED, not sampled -- the vehicle's
    real contact shadow is F67 and is open.  This exists only so the cream upper
    body does not disappear into the cream grounds, which it did in the first
    draft of 02, 05 and 06."""
    w = int(v.width * grow); h = max(6, int(v.width * squash))
    sh = Image.new("L", (w + 40, h + 40), 0)
    ImageDraw.Draw(sh).ellipse([20, 20, w + 20, h + 20], fill=op)
    sh = sh.filter(ImageFilter.GaussianBlur(h * 0.30))
    im.paste(Image.new("RGB", sh.size, colour),
             (x + (v.width - w) // 2 - 20, y + v.height - h // 2 - 20), sh)


def keyline(d, box, colour, w=3, inset=0):
    x0, y0, x1, y1 = box
    d.rectangle([x0 + inset, y0 + inset, x1 - inset, y1 - inset], outline=colour, width=w)

def rule(d, x0, x1, y, colour, w=3):
    d.line([(x0, y), (x1, y)], fill=colour, width=w)

def dotrule(d, x0, x1, y, colour, r=4, gap=18):
    x = x0
    while x <= x1:
        d.ellipse([x - r, y - r, x + r, y + r], fill=colour); x += gap

def corner_discs(im, colour, r):
    """The quarter-round corners on the owner's example, kept because they are
    the one piece of its furniture that is structural rather than shouted."""
    W, H = im.size
    d = ImageDraw.Draw(im)
    d.pieslice([-r, H - 2 * r, r, H], 270, 360, fill=colour)
    d.pieslice([W - r, H - 2 * r, W + r, H], 180, 270, fill=colour)
    return im

def serie(d, xy, n, colour, px=26, anchor="lt"):
    ls_text(d, xy, "SERIE   COMBI   ·   Nº %s" % n, font("sansb", px),
            colour, ls=px * 0.28, anchor=anchor)

# ================================================================ the pieces
# Every piece says ONE thing.  The copy is drawn from strings the VEHICLE
# ITSELF carries -- the mural lid's header and side panels, the flank script,
# the sunburst -- plus "taqueria y cerveceria" off the owner's own photograph.
# NOTHING here invents an offer, a price, a date or a claim.

def p01_aframe(path):
    """The A-frame, answering the owner's example head on: same object, same
    job, one message instead of four, and THIS bus instead of a stock one."""
    W, H = 1200, 1800
    piece_frame("01_aframe", (56, 56, W - 56, H - 56))
    im = Image.new("RGB", (W, H), AMBAR); d = ImageDraw.Draw(im)
    # The example sign's quarter-round corners were tried here and DROPPED:
    # inside the keyline they read as accidental white notches, not furniture.
    keyline(d, (0, 0, W - 1, H - 1), INK, w=7, inset=34)

    f1 = font("disp", 132)
    ls_text(d, (W // 2, 150), "SEÑOR", f1, CREMA, ls=14, anchor="mt")
    ls_text(d, (W // 2, 292), "TACOMBI", f1, CREMA, ls=14, anchor="mt")
    rule(d, 190, W - 190, 470, ROJO, 8)
    ls_text(d, (W // 2, 500), "TAQUERÍA   Y   CERVECERÍA", font("sansb", 34),
            AZUL, ls=13, anchor="mt")

    v = combi("side", 640)
    ground_shadow(im, v, (W - v.width) // 2, 700, (120, 78, 10), 70)
    im.paste(v, ((W - v.width) // 2, 700), v)

    ls_text(d, (W // 2, 1460), "FRESH JUICES · GOURMET TACOS · TORTAS",
            font("sansb", 33), INK, ls=8, anchor="mt")
    rule(d, 190, W - 190, 1540, ROJO, 8)
    ls_text(d, (W // 2, 1580), "100%  CALIDAD", font("disp", 60), ROJO,
            ls=10, anchor="mt")
    im.save(path); return im


def p02_cartel(path):
    """The poster.  Paper ground, the vehicle given the room the example sign
    could not give it, and the name set once."""
    W, H = 1400, 2000
    piece_frame("02_cartel", (68, 68, W - 68, H - 68))
    im = Image.new("RGB", (W, H), PAPEL); d = ImageDraw.Draw(im)
    keyline(d, (0, 0, W - 1, H - 1), INK, w=5, inset=46)
    rule(d, 120, W - 120, 232, INK, 4)
    ls_text(d, (W // 2, 130), "TAQUERÍA   Y   CERVECERÍA", font("sansb", 38),
            INK, ls=17, anchor="mt")

    v = combi("flank", 900)
    ground_shadow(im, v, (W - v.width) // 2, 470, (70, 55, 35), 46)
    im.paste(v, ((W - v.width) // 2, 470), v)

    # 118, NOT 150.  At 150 this ran -78..1478 on a 1400 pt page -- it printed
    # "SEÑOR TACOMB" with the I off the edge.  The size is authored so the
    # text-fit check stays an independent test rather than a tautology.
    f = font("disp", 118)
    ls_text(d, (W // 2, 1520), "SEÑOR TACOMBI", f, ROJO, ls=4, anchor="mt")
    rule(d, 120, W - 120, 1720, INK, 4)
    ls_text(d, (W // 2, 1770), "SE   SIRVE   DESDE   LA   COMBI",
            font("sansb", 36), AZUL, ls=15, anchor="mt")
    serie(d, (W // 2, 1860), "II", INK, 26, anchor="mt")
    im.save(path); return im


def p03_banner(path):
    """The wide one -- awning, web header, van-side.  Deep ground so the
    vehicle's cream upper body carries the contrast."""
    W, H = 2100, 700
    piece_frame("03_banner", (46, 46, W - 46, H - 46))
    im = Image.new("RGB", (W, H), AZUL); d = ImageDraw.Draw(im)
    keyline(d, (0, 0, W - 1, H - 1), CREMA, w=4, inset=24)
    v = combi("side", 560)
    ground_shadow(im, v, W - v.width - 60, (H - 560) // 2 + 40, (8, 14, 30), 90)
    im.paste(v, (W - v.width - 60, (H - 560) // 2 + 40), v)
    ls_text(d, (110, 210), "SEÑOR", font("disp", 104), CREMA, ls=6)
    ls_text(d, (110, 330), "TACOMBI", font("disp", 104), AMBAR, ls=6)
    rule(d, 112, 700, 470, ROJO, 6)
    ls_text(d, (112, 500), "TAQUERÍA  ·  CERVECERÍA", font("sansb", 30),
            CREMA, ls=11)
    im.save(path); return im


def p04_cuadro(path):
    """The square.  One word, the serving side, nothing else."""
    W = H = 1400
    piece_frame("04_cuadro", (62, 62, W - 62, H - 62))
    im = Image.new("RGB", (W, H), ROJO); d = ImageDraw.Draw(im)
    keyline(d, (0, 0, W - 1, H - 1), CREMA, w=5, inset=40)
    v = combi("side", 560)
    ground_shadow(im, v, (W - v.width) // 2, 300, (70, 10, 8), 80)
    im.paste(v, ((W - v.width) // 2, 300), v)
    ls_text(d, (W // 2, 120), "ABIERTO", font("disp", 172), CREMA, ls=22,
            anchor="mt")
    dotrule(d, 240, W - 240, 960, AMBAR, r=5, gap=26)
    ls_text(d, (W // 2, 1020), "SEÑOR  TACOMBI", font("disp", 74), AMBAR,
            ls=10, anchor="mt")
    ls_text(d, (W // 2, 1140), "TAQUERÍA   Y   CERVECERÍA", font("sansb", 32),
            CREMA, ls=14, anchor="mt")
    serie(d, (W // 2, 1250), "IV", CREMA, 24, anchor="mt")
    im.save(path); return im


def p05_tarjeta(path):
    """The card -- loyalty, business, or the thing that goes in the bag."""
    W, H = 1050, 650
    piece_frame("05_tarjeta", (48, 48, W - 48, H - 48))
    im = Image.new("RGB", (W, H), CREMA); d = ImageDraw.Draw(im)
    keyline(d, (0, 0, W - 1, H - 1), ROJO, w=4, inset=26)
    v = combi("side", 250)
    ground_shadow(im, v, (W - v.width) // 2, 90, (70, 55, 35), 44)
    im.paste(v, ((W - v.width) // 2, 90), v)
    dotrule(d, 150, W - 150, 400, AMBAR, r=4, gap=20)
    ls_text(d, (W // 2, 440), "SEÑOR  TACOMBI", font("disp", 56), ROJO, ls=6,
            anchor="mt")
    ls_text(d, (W // 2, 530), "TAQUERÍA   Y   CERVECERÍA", font("sansb", 24),
            AZUL, ls=11, anchor="mt")
    im.save(path); return im


def p06_menu(path):
    """The menu board.  The list is the mural lid's own five panels, read off
    the vehicle rather than invented."""
    W, H = 1200, 1700
    piece_frame("06_menu", (52, 52, W - 52, H - 52))
    im = Image.new("RGB", (W, H), CREMA); d = ImageDraw.Draw(im)
    d.rectangle([30, 30, W - 30, 320], fill=VERDE)   # inside the keyline, not across it
    keyline(d, (0, 0, W - 1, H - 1), INK, w=5, inset=30)
    v = combi("side", 300)
    ground_shadow(im, v, (W - v.width) // 2, 360, (70, 55, 35), 46)
    im.paste(v, ((W - v.width) // 2, 360), v)
    ls_text(d, (W // 2, 118), "LA   CARTA", font("disp", 96), CREMA, ls=16,
            anchor="mt")
    items = [("TACOS", "al pastor · carnitas · pollo"),
             ("TORTAS", "hecho a mano"),
             ("CEVICHE  &  TOSTADAS", "del día"),
             ("SHRIMP  &  FISH", "a la plancha"),
             ("FRESH  JUICES", "naranja · sandía · jamaica")]
    y = 720
    for name, sub in items:
        ls_text(d, (110, y), name, font("disp", 52), INK, ls=5)
        ls_text(d, (110, y + 66), sub.upper(), font("sansb", 24), AZUL, ls=6)
        dotrule(d, 110, W - 110, y + 122, AMBAR, r=3, gap=17)
        y += 168
    ls_text(d, (W // 2, 1600), "SEÑOR  TACOMBI  ·  100%  CALIDAD",
            font("sansb", 28), ROJO, ls=10, anchor="mt")
    im.save(path); return im

PIECES = [("01_aframe", p01_aframe), ("02_cartel", p02_cartel),
          ("03_banner", p03_banner), ("04_cuadro", p04_cuadro),
          ("05_tarjeta", p05_tarjeta), ("06_menu", p06_menu)]

# --------------------------------------------------- the photoreal variant
def plate(path, aspect=1.30, pad=0.075, white=238):
    """A rendered frame cropped to a PHOTOGRAPHIC PLATE.

    ⚠ THIS REPLACES A KEY THAT WAS WRONG AND WAS GREEN ON BEING WRONG.  The
    first version flood-filled the near-white background from the frame edge and
    dropped the vehicle onto the poster ground.  `hero34f` is NOT rendered on
    plain white -- it has a WHITE STUDIO FLOOR with a soft cast shadow on it --
    so the shadowed floor fell below the near-white threshold, survived the
    flood as "subject", and printed as a ragged white slab behind the bus.
    THREE CHECKS PASSED ON IT, including one that compared background pixels to
    subject pixels and read 978342 > 781658 while the subject silently contained
    the floor.  Caught by looking at the piece, not by any check (rule 1).

    Keeping the frame whole is also the better answer: the floor carries the
    render's own cast shadow, which is the one thing F67 says the vehicle is
    missing, and a photographic plate is a stronger poster device than a
    cut-out.  The crop is measured off the frame's own content -- the bbox of
    everything that is not paper-white -- not authored.
    """
    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    content = (a < white).any(axis=2)
    ys, xs = np.where(content)
    if not len(ys):
        raise SystemExit("plate(): %s is blank" % path)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    w, h = x1 - x0, y1 - y0
    px, py = int(w * pad), int(h * pad)
    x0, x1, y0, y1 = x0 - px, x1 + px, y0 - py, y1 + py
    # grow the short side to the plate's aspect, then clamp into the frame
    cw, ch = x1 - x0, y1 - y0
    if cw / float(ch) < aspect:
        need = int(aspect * ch) - cw
        x0 -= need // 2; x1 += need - need // 2
    else:
        need = int(cw / aspect) - ch
        y0 -= need // 2; y1 += need - need // 2
    x0 = max(0, x0); y0 = max(0, y0)
    x1 = min(im.width, x1); y1 = min(im.height, y1)
    return im.crop((x0, y0, x1, y1)), (int(x0), int(y0), int(x1), int(y1)), \
           int(content.sum())


def p07_hero(path, src="out/r80_hero34f.png"):
    """The photoreal register, for the same collection.  This is the ONLY piece
    that uses a rendered frame rather than a tracked capture, so it is the only
    one that needs Blender to have run."""
    if not os.path.exists(src):
        return None
    W, H = 1400, 1800
    piece_frame("07_hero", (68, 68, W - 68, H - 68))
    im = Image.new("RGB", (W, H), AZUL); d = ImageDraw.Draw(im)
    keyline(d, (0, 0, W - 1, H - 1), CREMA, w=4, inset=44)

    pl, box, npx = plate(src)
    pw = W - 2 * 210
    pl = pl.resize((pw, int(pl.height * pw / float(pl.width))), Image.LANCZOS)
    px, py = 210, 560
    im.paste(pl, (px, py))
    d.rectangle([px - 1, py - 1, px + pl.width, py + pl.height],
                outline=CREMA, width=3)
    OBSTACLE.append(("07_hero", "photographic plate", px, py,
                     px + pl.width, py + pl.height))

    ls_text(d, (W // 2, 150), "SEÑOR", font("disp", 128), CREMA, ls=12, anchor="mt")
    ls_text(d, (W // 2, 300), "TACOMBI", font("disp", 128), AMBAR, ls=12, anchor="mt")
    rule(d, 230, W - 230, 470, ROJO, 7)
    # ABLATION.  T1_PROMO_COLLIDE=1 restores the first layout, which printed the
    # strapline in CREAM ON THE WHITE PLATE.  It exists so the collision check
    # can be WATCHED FAILING on the real defect rather than asserted to work
    # (rule 3).  verify_clone.sh does not run it; watch it by hand:
    #     T1_PROMO_COLLIDE=1 python3 promo.py --only 07_hero
    if os.environ.get("T1_PROMO_COLLIDE") == "1":
        # The defect as it actually shipped: the strapline inside the plate,
        # cream on white.  Expressed RELATIVE to the plate, not as the literal
        # y=1380 of the first draft -- that number stopped colliding the moment
        # the plate was resized, and an ablation that silently stops ablating is
        # worse than none.  Watched: this reds the collision row.
        ty = py + pl.height - 120
    else:
        ty = py + pl.height + 60
    ls_text(d, (W // 2, ty), "TAQUERÍA   Y   CERVECERÍA", font("sansb", 36),
            CREMA, ls=16, anchor="mt")
    ls_text(d, (W // 2, ty + 88), "100%  CALIDAD", font("disp", 62), AMBAR,
            ls=10, anchor="mt")
    serie(d, (W // 2, ty + 218), "VII", CREMA, 25, anchor="mt")
    im.save(path)
    return im, box, npx

# ------------------------------------------------------------ contact sheet
def contact(paths, path, cols=3, cell=560, pad=34):
    ims = [Image.open(p) for p in paths]
    rows = (len(ims) + cols - 1) // cols
    W = cols * cell + pad * (cols + 1)
    H = rows * cell + pad * (rows + 1) + 40
    sh = Image.new("RGB", (W, H), (252, 251, 248)); d = ImageDraw.Draw(sh)
    for i, (im, p) in enumerate(zip(ims, paths)):
        r, c = divmod(i, cols)
        x = pad + c * (cell + pad); y = pad + r * (cell + pad)
        s = min(cell / im.width, cell / im.height)
        t = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        sh.paste(t, (x + (cell - t.width) // 2, y + (cell - t.height) // 2))
        d.text((x, y + cell + 4), os.path.basename(p), fill=(60, 55, 50),
               font=font("sans", 20))
    sh.save(path); return sh

# ------------------------------------------------------------------- checks
def main(argv):
    global OUT
    only = None
    for i, a in enumerate(argv):
        if a == "--only": only = argv[i + 1]
        if a == "--out":  OUT = argv[i + 1]
    # F358: the ablation must not overwrite the tracked artwork the owner was
    # shown, and `git checkout -- probe_scratch/` does NOT reach design_out/.
    if os.environ.get("T1_PROMO_COLLIDE") == "1" and OUT == "design_out":
        raise SystemExit("REFUSING: T1_PROMO_COLLIDE=1 would overwrite the "
                         "tracked artwork in design_out/.  Pass --out /tmp/ab.")
    os.makedirs(OUT, exist_ok=True)
    print("promo.py -- a collection of promotional images on the combi")

    for tag in ("side", "flank"):
        al, ab, st = load_capture(tag)
        ck(al.sum() > 100000, "capture %s: silhouette is %d px, not empty"
           % (tag, int(al.sum())))

    paths = []
    for name, fn in PIECES:
        if only and only != name: continue
        p = os.path.join(OUT, "promo_r80_%s.png" % name)
        im = fn(p)
        paths.append(p)
        ck(os.path.exists(p) and os.path.getsize(p) > 20000,
           "%s written, %d x %d, %d KB" % (name, im.width, im.height,
                                           os.path.getsize(p) // 1024))
        a = np.asarray(im.convert("RGB")).reshape(-1, 3)
        ck(len(np.unique(a[::37], axis=0)) > 200,
           "%s is not a flat slab (%d distinct colours sampled)"
           % (name, len(np.unique(a[::37], axis=0))))

    # the photoreal piece, only if a frame exists (out/ is empty on a clone)
    src = "out/r80_hero34f.png"
    if os.path.exists(src) and only in (None, "07_hero"):
        p = os.path.join(OUT, "promo_r80_07_hero.png")
        r = p07_hero(p, src)
        im, box, npx = r
        paths.append(p)
        ck(npx > 100000, "07_hero: plate crop measured off %d px of non-paper "
           "content, box=%s" % (npx, box))
        # The plate must not be a slab of floor: check the CROP still contains
        # the vehicle's red, which no amount of studio floor can supply.
        pa = np.asarray(Image.open(src).convert("RGB").crop(box)).astype(int)
        red = ((pa[..., 0] > 110) & (pa[..., 0] - pa[..., 1] > 45) &
               (pa[..., 0] - pa[..., 2] > 45))
        ck(red.sum() > 20000, "07_hero: the crop holds %d px of body red -- it "
           "is the vehicle, not a panel of studio floor" % int(red.sum()))
        ck(os.path.exists(p), "07_hero written, %d x %d" % (im.width, im.height))
    else:
        print("       SKIP 07_hero: %s absent -- render first, or this piece "
              "is simply not in the set" % src)

    # THE TEXT-FIT CHECK.  Compares two independently obtained quantities
    # (rule 6): the run's measured box from the FACE's own metrics, against the
    # piece's safe area declared from its page size.  Neither is derived from
    # the other.
    bad = []
    for piece, txt, x0, y0, x1, y1, safe in TEXTBOX:
        sx0, sy0, sx1, sy1 = safe
        if x0 < sx0 or y0 < sy0 or x1 > sx1 or y1 > sy1:
            bad.append((piece, txt, int(x0), int(y0), int(x1), int(y1), safe))
    for b in bad:
        print("       OVERFLOW %s: %r box=(%d,%d,%d,%d) safe=%s"
              % (b[0], b[1][:34], b[2], b[3], b[4], b[5], b[6]))
    ck(not bad, "every text run (%d) lies inside its piece's safe area; %d "
       "overflow" % (len(TEXTBOX), len(bad)))

    # THE COLLISION CHECK.  A run can sit inside the safe area and still be
    # illegible: the first plate treatment printed "TAQUERÍA Y CERVECERÍA" in
    # CREAM ON THE WHITE PLATE, and the safe-area check passed on it because the
    # run WAS inside the margins.  Bounds and collision are different questions.
    # WATCHED FAILING on that exact defect before the layout was changed.
    hit = []
    for piece, txt, x0, y0, x1, y1, safe in TEXTBOX:
        for op, lab, ox0, oy0, ox1, oy1 in OBSTACLE:
            if op != piece: continue
            if x0 < ox1 and x1 > ox0 and y0 < oy1 and y1 > oy0:
                hit.append((piece, txt, lab))
    for h in hit:
        print("       COLLISION %s: %r crosses the %s" % (h[0], h[1][:34], h[2]))
    ck(not hit, "no text run crosses a piece's artwork (%d obstacle(s) "
       "declared); %d collision" % (len(OBSTACLE), len(hit)))

    if not only:
        cp = os.path.join(OUT, "promo_r80_contact.png")
        contact(paths, cp)
        ck(os.path.exists(cp), "contact sheet written")

    print("%d checked, %d FAILED" % (CHECK[0], len(FAILED)))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
