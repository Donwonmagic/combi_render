"""
sheet.py -- a minimal drafting-sheet primitive layer, in MILLIMETRES.

WHY THIS EXISTS.  The rev-76 design program's spine is the owner's own recovered
sentence -- "vector line and flat colour, shading and occlusion sampled from the
3D asset" -- and a vector master is what screen positives, flexo plates and
die-cut cutters all want.  Every drawing in this programme therefore has to come
out as SVG.  A PNG is a PROOF, not the artefact.

ONE description, TWO backends: `save_svg()` writes the master, `save_png()`
writes a supersampled proof of the SAME primitive list, so the two cannot drift.
That is the only reason this is a module and not a script.

UNITS ARE MILLIMETRES ON THE SHEET, origin top-left, y down.  Vehicle
coordinates are converted by the caller; this layer knows nothing about buses.

CEILING, STATED (rule 12): the PNG backend is PIL, which has no antialiased
line primitive, so it draws at SS x the final raster and downsamples.  Hairlines
below about 0.10 mm at 300 dpi will therefore land as grey rather than as a
thinner black line.  The SVG has no such limit -- print from the SVG.
"""
import os, math

# ------------------------------------------------------------------ fonts
# Rule 37: an absent input must never read as a measurement.  A missing font
# must REFUSE, not silently substitute a face that changes every metric on the
# sheet.  The chain is system fonts only -- nothing under /mnt or /opt, because
# those are not on a clone.
_FONT_CHAIN = {
    "mono": ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
             "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"],
    "mono-b": ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
               "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"],
    "sans": ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    "sans-b": ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
               "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
}
_SVG_FAMILY = {"mono": "DejaVu Sans Mono, monospace",
               "mono-b": "DejaVu Sans Mono, monospace",
               "sans": "Liberation Sans, Helvetica, Arial, sans-serif",
               "sans-b": "Liberation Sans, Helvetica, Arial, sans-serif"}


def font_path(key):
    for p in _FONT_CHAIN[key]:
        if os.path.exists(p):
            return p
    raise SystemExit("NO FONT: none of %s exists.  sheet.py REFUSES to "
                     "substitute -- every metric on the sheet is set in this "
                     "face (rule 37).  Install fonts-dejavu-core." %
                     _FONT_CHAIN[key])


def mix(ink, stock, tint):
    """tint 1.0 = full ink, 0.0 = bare stock.  Flat-colour halftone stand-in."""
    t = max(0.0, min(1.0, float(tint)))
    return tuple(int(round(s + (i - s) * t)) for i, s in zip(ink, stock))


def _hex(c):
    return "#%02x%02x%02x" % tuple(c)


class Sheet(object):
    def __init__(self, w_mm, h_mm, ink=(0, 0, 0), stock=(255, 255, 255),
                 dpi=300, ss=2):
        self.w, self.h = float(w_mm), float(h_mm)
        self.ink, self.stock, self.dpi, self.ss = tuple(ink), tuple(stock), dpi, ss
        self.ops = []                       # (kind, payload) -- the ONE record

    # ------------------------------------------------------------- primitives
    def line(self, x1, y1, x2, y2, w=0.25, tint=1.0, dash=None):
        self.ops.append(("line", (x1, y1, x2, y2, w, tint, dash)))

    def poly(self, pts, w=0.25, tint=1.0, close=False, dash=None):
        pts = list(pts)
        for i in range(len(pts) - 1):
            self.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], w, tint, dash)
        if close and len(pts) > 2:
            self.line(pts[-1][0], pts[-1][1], pts[0][0], pts[0][1], w, tint, dash)

    def rect(self, x, y, w, h, lw=0.25, tint=1.0, dash=None):
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)],
                  w=lw, tint=tint, close=True, dash=dash)

    def fill(self, x, y, w, h, tint=1.0):
        self.ops.append(("fill", (x, y, w, h, tint)))

    def arc(self, cx, cy, r, a0, a1, w=0.25, tint=1.0, seg=None, dash=None):
        """angles in DEGREES, 0 = +x, counter-clockwise in sheet space (y down
        means it reads clockwise on the page -- callers pass what they mean)."""
        a0, a1 = math.radians(a0), math.radians(a1)
        n = seg or max(8, int(abs(a1 - a0) * r / 0.35))
        pts = [(cx + r * math.cos(a0 + (a1 - a0) * i / n),
                cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
        self.poly(pts, w=w, tint=tint, dash=dash)

    def circle(self, cx, cy, r, w=0.25, tint=1.0, dash=None):
        self.arc(cx, cy, r, 0, 360, w=w, tint=tint, dash=dash)

    def text(self, x, y, s, pt=7.0, font="mono", tint=1.0, align="l",
             track=0.0, rot=0):
        """y is the BASELINE.  pt is a real typographic point (1/72 in)."""
        self.ops.append(("text", (x, y, s, pt, font, tint, align, track, rot)))

    # --------------------------------------------------------------- backends
    def save_svg(self, path):
        mm = lambda v: ("%.4f" % v).rstrip("0").rstrip(".")
        out = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<svg xmlns="http://www.w3.org/2000/svg" width="%smm" height="%smm" '
               'viewBox="0 0 %s %s" version="1.1">' % (mm(self.w), mm(self.h),
                                                       mm(self.w), mm(self.h)),
               '<rect x="0" y="0" width="%s" height="%s" fill="%s"/>'
               % (mm(self.w), mm(self.h), _hex(self.stock))]
        for kind, p in self.ops:
            if kind == "line":
                x1, y1, x2, y2, w, tint, dash = p
                d = ' stroke-dasharray="%s"' % ",".join(mm(v) for v in dash) if dash else ""
                out.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" '
                           'stroke-width="%s" stroke-linecap="butt"%s/>'
                           % (mm(x1), mm(y1), mm(x2), mm(y2),
                              _hex(mix(self.ink, self.stock, tint)), mm(w), d))
            elif kind == "fill":
                x, y, w, h, tint = p
                out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>'
                           % (mm(x), mm(y), mm(w), mm(h),
                              _hex(mix(self.ink, self.stock, tint))))
            elif kind == "text":
                x, y, s, pt, font, tint, align, track, rot = p
                anchor = {"l": "start", "c": "middle", "r": "end"}[align]
                esc = (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
                tr = ' transform="rotate(%s %s %s)"' % (rot, mm(x), mm(y)) if rot else ""
                out.append('<text x="%s" y="%s" font-family="%s" font-size="%s" '
                           'fill="%s" text-anchor="%s" letter-spacing="%s"'
                           '%s%s>%s</text>'
                           % (mm(x), mm(y), _SVG_FAMILY[font], mm(pt * 25.4 / 72.0),
                              _hex(mix(self.ink, self.stock, tint)), anchor, mm(track),
                              ' font-weight="bold"' if font.endswith("-b") else "",
                              tr, esc))
        out.append("</svg>")
        open(path, "w").write("\n".join(out))
        return path

    def save_png(self, path):
        from PIL import Image, ImageDraw, ImageFont
        k = self.dpi / 25.4 * self.ss                     # mm -> supersampled px
        W, H = int(round(self.w * k)), int(round(self.h * k))
        img = Image.new("RGB", (W, H), self.stock)
        d = ImageDraw.Draw(img)
        cache = {}

        def face(fkey, pt):
            px = max(1, int(round(pt / 72.0 * self.dpi * self.ss)))
            if (fkey, px) not in cache:
                cache[(fkey, px)] = ImageFont.truetype(font_path(fkey), px)
            return cache[(fkey, px)]

        for kind, p in self.ops:
            if kind == "line":
                x1, y1, x2, y2, w, tint, dash = p
                col = mix(self.ink, self.stock, tint)
                lw = max(1, int(round(w * k)))
                if dash:
                    L = math.hypot(x2 - x1, y2 - y1)
                    if L <= 0:
                        continue
                    ux, uy, t, on = (x2 - x1) / L, (y2 - y1) / L, 0.0, True
                    i = 0
                    while t < L:
                        seg = min(dash[i % len(dash)], L - t)
                        if on:
                            d.line([(x1 + ux * t) * k, (y1 + uy * t) * k,
                                    (x1 + ux * (t + seg)) * k, (y1 + uy * (t + seg)) * k],
                                   fill=col, width=lw)
                        t += seg; on = not on; i += 1
                else:
                    d.line([x1 * k, y1 * k, x2 * k, y2 * k], fill=col, width=lw)
            elif kind == "fill":
                x, y, w, h, tint = p
                d.rectangle([x * k, y * k, (x + w) * k, (y + h) * k],
                            fill=mix(self.ink, self.stock, tint))
            elif kind == "text":
                x, y, s, pt, font, tint, align, track, rot = p
                f = face(font, pt)
                col = mix(self.ink, self.stock, tint)
                trk = track * k
                widths = [d.textlength(ch, font=f) for ch in s]
                total = sum(widths) + trk * max(0, len(s) - 1)
                ox = {"l": 0.0, "c": -total / 2.0, "r": -total}[align]
                if rot:
                    # Render into a layer whose CENTRE is the anchor point the
                    # caller gave, rotate about that centre with the size held,
                    # then paste centre-on-anchor.  Doing it any other way means
                    # tracking where expand=True moved the origin, which is how
                    # the first draft lost the rotated label entirely.
                    # PIL rotates the IMAGE counter-clockwise; SVG's rotate()
                    # is clockwise on screen.  Hence the sign flip -- without it
                    # the two backends disagree by 180 degrees.
                    half = int(max(total, f.size * 2.5)) + 12
                    lay = Image.new("RGBA", (2 * half, 2 * half), (0, 0, 0, 0))
                    ld = ImageDraw.Draw(lay)
                    cx = half + ox
                    for ch, wch in zip(s, widths):
                        ld.text((cx, half), ch, font=f, fill=col + (255,), anchor="ls")
                        cx += wch + trk
                    lay = lay.rotate(-rot, expand=False, resample=Image.BICUBIC,
                                     center=(half, half))
                    img.paste(lay, (int(round(x * k)) - half,
                                    int(round(y * k)) - half), lay)
                else:
                    cx = x * k + ox
                    for ch, wch in zip(s, widths):
                        d.text((cx, y * k), ch, font=f, fill=col, anchor="ls")
                        cx += wch + trk

        if self.ss > 1:
            img = img.resize((int(round(self.w * self.dpi / 25.4)),
                              int(round(self.h * self.dpi / 25.4))),
                             Image.LANCZOS)
        img.save(path)
        return path
