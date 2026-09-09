"""
lienzo.py -- SVG MASTER, CHROMIUM RENDER.  The engine the collection should
have been built on.

WHY THIS REPLACES THE PIL PATH, AND WHO SAID SO FIRST.  The owner asked
*"maybe there are better ways to render this than the current py engine?  Maybe
we've been going about this the wrong way?"*  The answer is yes, and this
repository already knew it -- `sheet.py`'s own docstring, written revisions
before any of this:

    "Every drawing in this programme therefore has to come out as SVG.
     A PNG is a PROOF, not the artefact."

MEASURED against that standard, the round shipped at rev 80 was wrong:
  * `apaga.py`, `calendario.py`, `la_rueda.py`, `sticker.py` and
    `sheet3_notissued.py` all import `sheet.py`.  `promo.py`, `coleccion.py`
    and `estilos.py` import it **ZERO** times.
  * `design_out/` held **42 PNG against 6 SVG**, and all six SVGs came from the
    other modules.  Fifteen promotional pieces shipped with NO MASTER.
  * PIL has no text shaping, so `promo.ls_text` places glyphs ONE AT A TIME.
    That is not "letterspacing with a caveat" -- it means **NO KERNING AT ALL**.

WHAT THIS GIVES INSTEAD, each verified on this machine before being claimed:
  * ONE description in millimetres -> SVG master, PNG proof, PDF for print.
    All three come from THE SAME FILE, so they cannot drift.  That is a
    stronger guarantee than `sheet.py`'s two backends, which are two code paths
    that must be kept in step by hand.
  * Real text shaping through Chromium: kerning, ligatures, small caps,
    OpenType features.  Verified: `VA`/`WAV` kern, `fi fl ffi` ligate.
  * Vector output at any size, so the print ceiling is gone permanently rather
    than for one round.

⚠ CEILINGS, STATED (rule 12).
  * Chromium is the renderer, so the PROOF depends on a browser's rasteriser.
    The MASTER does not -- it is the SVG, and any RIP can take it.
  * `headless_shell` lives at a pinned path under /opt/pw-browsers.  On a clone
    without it the SVG still writes and only the raster steps REFUSE (rule 37);
    they do not silently substitute PIL.
  * Fonts are referenced by `@font-face` with `file://` URLs.  That resolves
    for a LOCAL render.  An SVG handed to a third party must have its type
    converted to outlines first, and nothing here does that yet.
  * `sheet.py` remains the right tool for millimetre die-cut work -- the
    stickers.  This is not a replacement for it; it is the typographic half
    the programme never had.
"""
import os, re, subprocess, xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.abspath(__file__))
FONTDIR = os.path.join(ROOT, "fonts")
SHELL = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
MM = 25.4

FACES = {
    "display": os.path.join(FONTDIR, "Alfa.ttf"),
    "cond":    os.path.join(FONTDIR, "Oswald.ttf"),
    "serif":   "/usr/share/fonts/X11/Type1/c0648bt_.pfb",
}


def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


class Lienzo(object):
    """A sheet in MILLIMETRES, origin top-left, y down -- the same convention
    as `sheet.py`, deliberately, so the two describe space the same way."""

    def __init__(self, w_mm, h_mm, bg="#ffffff"):
        self.opaque = []
        self.w, self.h, self.bg = float(w_mm), float(h_mm), bg
        self.body = []
        self.defs = []
        self._fonts = set()

    # ------------------------------------------------------------ primitives
    # WHAT IS PAINTED OVER WHAT.  Every opaque slab records its geometry and
    # its position in draw order, so an element drawn earlier can be tested for
    # being covered.
    #
    # ⚠ THE CEILING THIS COMMENT USED TO CLAIM WAS WRONG IN THREE WAYS, AND AN
    # AUDIT FOUND ALL THREE.  It said "slabs only -- `rect`, `circle` and the
    # page": the page rect is written in `_svg()` and was never recorded
    # (harmless -- it is under everything), `line()` was not recorded at all
    # (`p_carta` draws its rules AFTER each menu run, 6.94 mm below a baseline
    # whose descenders reach 5.03 mm), and it justified leaving traced `paths`
    # out with "on every layout the drawing is laid down before the type",
    # which is FALSE: `_poster` runs frame -> wordmark -> LETRERO -> hero, and
    # the measured clearance from that subhead to the hero is 10.60 mm on
    # `cartel_a3`.
    #
    # So `line()` records its stroke box, and `pliego`'s `put_hero` records the
    # drawing's bounding box.  ⚠ A DRAWING'S BOUNDING BOX IS NOT THE DRAWING --
    # that OVER-reports coverage, which is the safe direction for a check and
    # the wrong one for a claim.  The page is still not recorded and need not be.
    def rect(self, x, y, w, h, fill, rx=0):
        self.opaque.append(("rect", (x, y, x + w, y + h), len(self.body), fill))
        return self._rect(x, y, w, h, fill, rx)

    def _rect(self, x, y, w, h, fill, rx=0):
        self.body.append(
            '<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" rx="%.3f" '
            'fill="%s"/>' % (x, y, w, h, rx, fill))

    def circle(self, cx, cy, r, fill, stroke=None, stroke_w=0.0):
        self.opaque.append(("circle", (cx, cy, r), len(self.body), fill))
        sk = ('' if not stroke else
              ' stroke="%s" stroke-width="%.4f"' % (stroke, stroke_w))
        self.body.append('<circle cx="%.3f" cy="%.3f" r="%.3f" fill="%s"%s/>'
                         % (cx, cy, r, fill, sk))

    def line(self, x1, y1, x2, y2, stroke, w=0.4, dash=None):
        # kind "rule", not "rect": a stroke can OCCLUDE but it is not a ground
        self.opaque.append(("rule", (min(x1, x2), min(y1, y2) - w / 2.0,
                                     max(x1, x2), max(y1, y2) + w / 2.0),
                            len(self.body), stroke))
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.body.append('<line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" '
                         'stroke="%s" stroke-width="%.3f"%s/>'
                         % (x1, y1, x2, y2, stroke, w, d))

    def frame(self, inset, stroke, w=0.6):
        self.opaque.append(("rule", (inset, inset, self.w - inset,
                                     self.h - inset), len(self.body), stroke))
        self.body.append(
            '<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" fill="none" '
            'stroke="%s" stroke-width="%.3f"/>'
            % (inset, inset, self.w - 2 * inset, self.h - 2 * inset, stroke, w))

    def paths(self, ds, fill, opacity=1.0, stroke=None, stroke_w=0.0):
        """Traced contours as ONE path element with even-odd fill, so holes are
        holes rather than a second shape painted in the ground colour.

        `stroke` is the KEYLINE.  A flat fill whose colour is close to the page
        cannot be seen at all -- the cream upper body on a cream card was a
        traced, rasterised, printed shape at 1.17:1.  Stroking that same path
        is what a screen-printer does, and it keeps the drawing's own colour
        instead of moving it."""
        if not ds:
            return
        sk = ""
        if stroke and stroke_w > 0:
            sk = (' stroke="%s" stroke-width="%.4f" stroke-linejoin="round"'
                  % (stroke, stroke_w))
        self.body.append('<path fill="%s" fill-rule="evenodd" opacity="%.3f"%s '
                         'd="%s"/>' % (fill, opacity, sk, " ".join(ds)))

    def text(self, x, y, s, face, size_mm, fill, anchor="middle",
             tracking=0.0, weight=None, caps=False):
        self._fonts.add(face)
        extra = ""
        if tracking:
            extra += ' letter-spacing="%.4f"' % tracking
        if weight:
            extra += ' font-weight="%s"' % weight
        if caps:
            extra += ' style="font-variant-caps:small-caps"'
        self.body.append(
            '<text x="%.3f" y="%.3f" font-family="%s" font-size="%.4f" '
            'fill="%s" text-anchor="%s"%s>%s</text>'
            % (x, y, face, size_mm, fill, anchor, extra, _esc(s)))

    # ----------------------------------------------------------------- output
    def _svg(self):
        ff = "".join(
            "@font-face{font-family:%s;src:url('file://%s');}" % (k, FACES[k])
            for k in sorted(self._fonts) if k in FACES)
        style = "<style>%s text{font-kerning:normal;}</style>" % ff
        return ('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<svg xmlns="http://www.w3.org/2000/svg" '
                'width="%.3fmm" height="%.3fmm" viewBox="0 0 %.3f %.3f">'
                '%s<rect width="%.3f" height="%.3f" fill="%s"/>%s</svg>'
                % (self.w, self.h, self.w, self.h, style,
                   self.w, self.h, self.bg, "".join(self.body)))

    def save_svg(self, path):
        open(path, "w").write(self._svg())
        ET.parse(path)                       # a master that is not valid XML is not a master
        return path

    def _shell(self):
        if not os.path.exists(SHELL):
            raise SystemExit(
                "NO RENDERER: %s absent.  lienzo REFUSES to fall back to PIL "
                "-- the proof must come from the master, and a different "
                "rasteriser is a different drawing (rule 37)." % SHELL)
        return SHELL

    def _wrap(self, svg_path):
        """An HTML document with the SVG INLINE and the page sized to the sheet.

        ⚠⚠ TWO DECISIVE DEFECTS ARE FIXED BY THIS ONE CHANGE, AND BOTH SHIPPED.
        The first version wrote `<img src=...svg>` and screenshotted it, and
        called `--print-to-pdf` on the SVG directly.

        1  **EVERY PNG PROOF WAS SET IN A FALLBACK SERIF.**  An SVG loaded
           through `<img>` renders in a RESTRICTED RESOURCE MODE where
           `@font-face` `file://` URLs do not load -- so Oswald and Alfa Slab
           One never reached any proof, while the PDF (loaded as a document)
           embedded them correctly.  The module claimed *"all three come from
           THE SAME FILE, so they cannot drift"*; they drifted in TYPEFACE.
           It also caused the colophon overrun on three posters: `fit_pt`
           measured Oswald, Chromium drew a ~26 % wider serif.
        2  **EVERY PDF WAS US LETTER.**  `--print-to-pdf` with no page size
           gives 612 x 792 pt for sheets of 600 x 900 mm, so five of eleven
           paginated and the A-frame's RIGHT HALF WAS NOT IN ITS OWN PDF.

        Inlining the SVG in a document with `@page {size: W H; margin:0}` fixes
        both: fonts load, and the page is the sheet.
        """
        svg = open(svg_path).read()
        svg = svg[svg.index("<svg"):]
        html = svg_path + ".doc.html"
        open(html, "w").write(
            "<!doctype html><html><head><meta charset='utf-8'><style>"
            "@page{size:%.4fmm %.4fmm;margin:0}"
            "html,body{margin:0;padding:0;background:%s}"
            "svg{display:block;width:%.4fmm;height:%.4fmm}"
            "</style></head><body>%s</body></html>"
            % (self.w, self.h, self.bg, self.w, self.h, svg))
        return html

    def render(self, svg_path, png=None, pdf=None, dpi=300, px=None):
        """PNG proof and PDF, BOTH from the same inlined document.

        `px` is an EXACT output size `(w, h)` in pixels, for screen formats where
        the deliverable is a pixel size and not a paper size.  ⚠ dpi alone
        cannot deliver one: the window is rounded to whole CSS pixels and the
        device scale factor is applied to that, so a story asked for at 1080
        came out 1079 and a banner at 2101.  Given `px`, the scale factor is
        derived FROM the rounded window so the product is exact."""
        outs = []
        # ⚠ `--disable-lcd-text`: Chromium's default subpixel antialiasing bakes
        # RGB COLOUR FRINGES into every glyph edge.  On screen that is a feature;
        # in a one- or two-colour print master it is contamination -- the
        # painted window on `postal`'s provenance line showed blue and orange
        # edges on type specified as a single GRANA.  `--font-render-hinting=none`
        # keeps outlines at their designed shapes instead of snapping stems to
        # the raster grid, which is what you want when the raster is a proof of
        # a vector master.
        base = ["--headless", "--disable-gpu", "--no-sandbox",
                "--hide-scrollbars", "--disable-lcd-text",
                "--font-render-hinting=none"]
        html = self._wrap(svg_path)
        url = "file://" + os.path.abspath(html)
        try:
            if png:
                # ⚠ CSS MILLIMETRES ARE 96 dpi, NOT THE OUTPUT dpi.  Sizing the
                # window in output pixels while the document lays out at 96 dpi
                # left the sheet occupying only part of the frame and the rest
                # showing body background -- which moved both margin readings.
                # The window is CSS px; the DEVICE SCALE FACTOR carries the dpi.
                cw = self.w / MM * 96.0; chh = self.h / MM * 96.0
                ww = int(round(cw)); wh = int(round(chh))
                # ⚠ ONE SCALE FOR BOTH AXES, DERIVED FROM THE WIDTH, LEFT THE
                # HEIGHTS OUT BY ONE AND TWO PIXELS (1922 for 1920, 701 for
                # 700).  `pliego` picks screen millimetres that are a whole
                # number of CSS pixels at an integer scale, so `cw` and `chh`
                # are already integral and nothing rounds.
                scale = (px[0] / float(ww)) if px else (dpi / 96.0)
                r = subprocess.run(
                    [self._shell()] + base +
                    ["--force-device-scale-factor=%.9f" % scale,
                     "--screenshot=" + os.path.abspath(png),
                     "--window-size=%d,%d" % (ww, wh),
                     url],
                    capture_output=True, timeout=300)
                if not os.path.exists(png) or os.path.getsize(png) < 1000:
                    raise SystemExit("RENDER FAILED (png) rc=%d: %s"
                                     % (r.returncode, r.stderr[-400:]))
                outs.append(png)
            if pdf:
                r = subprocess.run(
                    [self._shell()] + base + ["--no-pdf-header-footer",
                     "--print-to-pdf=" + os.path.abspath(pdf), url],
                    capture_output=True, timeout=300)
                if not os.path.exists(pdf) or os.path.getsize(pdf) < 1000:
                    raise SystemExit("RENDER FAILED (pdf) rc=%d: %s"
                                     % (r.returncode, r.stderr[-400:]))
                outs.append(pdf)
        finally:
            if os.path.exists(html): os.remove(html)
        return outs


def pdf_page_mm(path):
    """The PDF's own /MediaBox in mm, and its page count.  ⚠ THE BUILD NEVER
    CHECKED EITHER, so eleven US-Letter documents shipped as print masters."""
    raw = open(path, "rb").read()
    import re as _re
    boxes = _re.findall(rb"/MediaBox\s*\[\s*([\d.\-]+)\s+([\d.\-]+)\s+"
                        rb"([\d.\-]+)\s+([\d.\-]+)", raw)
    pages = len(_re.findall(rb"/Type\s*/Page[^s]", raw))
    if not boxes:
        return None, pages
    x0, y0, x1, y1 = [float(v) for v in boxes[0]]
    return ((x1 - x0) * MM / 72.0, (y1 - y0) * MM / 72.0), pages
