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
        self.w, self.h, self.bg = float(w_mm), float(h_mm), bg
        self.body = []
        self.defs = []
        self._fonts = set()

    # ------------------------------------------------------------ primitives
    def rect(self, x, y, w, h, fill, rx=0):
        self.body.append(
            '<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" rx="%.3f" '
            'fill="%s"/>' % (x, y, w, h, rx, fill))

    def line(self, x1, y1, x2, y2, stroke, w=0.4, dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.body.append('<line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" '
                         'stroke="%s" stroke-width="%.3f"%s/>'
                         % (x1, y1, x2, y2, stroke, w, d))

    def frame(self, inset, stroke, w=0.6):
        self.body.append(
            '<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" fill="none" '
            'stroke="%s" stroke-width="%.3f"/>'
            % (inset, inset, self.w - 2 * inset, self.h - 2 * inset, stroke, w))

    def paths(self, ds, fill, opacity=1.0):
        """Traced contours as ONE path element with even-odd fill, so holes are
        holes rather than a second shape painted in the ground colour."""
        if not ds:
            return
        self.body.append('<path fill="%s" fill-rule="evenodd" opacity="%.3f" '
                         'd="%s"/>' % (fill, opacity, " ".join(ds)))

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

    def render(self, svg_path, png=None, pdf=None, dpi=300):
        """PNG proof and/or PDF, BOTH rendered from the SVG file itself."""
        outs = []
        base = ["--headless", "--disable-gpu", "--no-sandbox",
                "--hide-scrollbars", "--force-device-scale-factor=1",
                "--default-background-color=00000000"]
        url = "file://" + os.path.abspath(svg_path)
        if png:
            wpx = int(round(self.w / MM * dpi)); hpx = int(round(self.h / MM * dpi))
            html = svg_path + ".render.html"
            open(html, "w").write(
                "<html><head><style>html,body{margin:0;padding:0}"
                "img{display:block;width:%dpx;height:%dpx}</style></head>"
                "<body><img src='%s'></body></html>"
                % (wpx, hpx, os.path.basename(svg_path)))
            subprocess.run([self._shell()] + base +
                           ["--screenshot=" + os.path.abspath(png),
                            "--window-size=%d,%d" % (wpx, hpx),
                            "file://" + os.path.abspath(html)],
                           capture_output=True, timeout=180)
            os.remove(html)
            outs.append(png)
        if pdf:
            subprocess.run([self._shell()] + base +
                           ["--no-pdf-header-footer",
                            "--print-to-pdf=" + os.path.abspath(pdf), url],
                           capture_output=True, timeout=180)
            outs.append(pdf)
        return outs
