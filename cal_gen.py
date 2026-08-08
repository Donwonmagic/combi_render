"""
"100% Calidad" rear-corner decal.

SPEC rev4 sec.3 / 8.4: this sits on SOLID cream sheet metal aft of bay 3, not
on glass. Reference reads a red-to-orange spiky sunburst carrying white
slanted type, with a small pink five-point star to its left.

Drawn at 4x and downsampled, so the spike edges stay clean on a curved flank.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os

W, H, SS = 2048, 1400, 4
w, h = W * SS, H * SS
img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- sunburst
cx, cy = int(w * 0.585), int(h * 0.50)
R_OUT, R_IN = int(h * 0.455), int(h * 0.320)
N = 24
pts = []
for i in range(N * 2):
    a = math.pi * i / N - math.pi / 2 + math.pi / N
    r = R_OUT if i % 2 == 0 else R_IN
    pts.append((cx + r * math.cos(a), cy + r * math.sin(a) * 0.92))
d.polygon(pts, fill=(214, 58, 26, 255))                    # outer red spikes

pts2 = [(cx + (p[0] - cx) * 0.90, cy + (p[1] - cy) * 0.90) for p in pts]
d.polygon(pts2, fill=(232, 104, 24, 255))                  # orange inner burst
d.ellipse([cx - R_IN * 0.94, cy - R_IN * 0.86,
           cx + R_IN * 0.94, cy + R_IN * 0.86], fill=(206, 40, 22, 255))

def font(px):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, px)
    return ImageFont.load_default()

# ------------------------------------------------------------------- type
txt = Image.new("RGBA", (w, h), (0, 0, 0, 0))
td = ImageDraw.Draw(txt)
f1, f2 = font(int(h * 0.175)), font(int(h * 0.115))
for s, fo, dy in (("100%", f1, -int(h * 0.082)), ("Calidad", f2, int(h * 0.088))):
    bb = td.textbbox((0, 0), s, font=fo)
    tx, ty = cx - (bb[2] - bb[0]) / 2 - bb[0], cy + dy - (bb[3] - bb[1]) / 2 - bb[1]
    td.text((tx + SS * 3, ty + SS * 3), s, font=fo, fill=(120, 16, 8, 190))
    td.text((tx, ty), s, font=fo, fill=(255, 252, 246, 255))
txt = txt.rotate(-8.5, resample=Image.BICUBIC, center=(cx, cy))
img = Image.alpha_composite(img, txt)

# --------------------------------------------------------- five-point star
d = ImageDraw.Draw(img)
sx, sy, sr = int(w * 0.115), int(h * 0.50), int(h * 0.135)
sp = []
for i in range(10):
    a = math.pi * i / 5 - math.pi / 2
    r = sr if i % 2 == 0 else sr * 0.42
    sp.append((sx + r * math.cos(a), sy + r * math.sin(a)))
d.polygon(sp, fill=(226, 74, 96, 255))

img = img.resize((W, H), Image.LANCZOS)
img.save("tex/calidad.png")
Image.alpha_composite(Image.new("RGBA", (W, H), (238, 232, 220, 255)),
                      img).convert("RGB").save("tex/prev_calidad.png")
print("wrote tex/calidad.png", img.size)
