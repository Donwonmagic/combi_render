#!/usr/bin/env python3
"""rev48_verifyA_sweep -- adversarial check of probe_rev47_gap's C1 / ratio rule.
Writes NOTHING into the project. Builds decals at several LINE_GAP values in
memory and runs the SAME estimator on them."""
import sys, math, importlib.util
import numpy as np
from PIL import Image
from scipy import ndimage as nd
sys.path.insert(0, "/home/user/combi_render")
Image.MAX_IMAGE_PIXELS = None

spec = importlib.util.spec_from_file_location("cg", "/home/user/combi_render/cal_gen.py")
cg = importlib.util.module_from_spec(spec); spec.loader.exec_module(cg)

# ---- the probe's own estimator, copied verbatim ------------------------------
def bands(ty, Z, lo=-45.0, hi=10.0):
    best = None
    for ang in np.arange(lo, hi, 0.5):
        rot = nd.rotate(ty.astype(float), ang, reshape=True, order=1) > 0.5
        prof = rot.sum(1)
        nz = np.nonzero(prof)[0]
        if len(nz) == 0: continue
        seg, run = [], None
        for i in range(nz.min(), nz.max() + 2):
            p = prof[i] if i < len(prof) else 0
            if p > 0 and run is None: run = i
            if p == 0 and run is not None:
                seg.append((run, i - 1)); run = None
        seg = [s for s in seg if (s[1] - s[0] + 1) > Z * 1.5]
        if len(seg) != 2: continue
        cap = (seg[0][1] - seg[0][0] + 1) / Z
        gap = (seg[1][0] - seg[0][1] - 1) / Z
        if gap <= 0: continue
        if best is None or gap > best[3]:
            best = (gap / cap, ang, cap, gap)
    return best

def type_mask(img, Z):
    big = img.resize((img.width * Z, img.height * Z), Image.LANCZOS)
    a = np.asarray(big.convert("RGB"), np.float32)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(2); sat = (mx - a.min(2)) / np.maximum(mx, 1)
    red = (R > 90) & (R - G > 40) & (R - B > 25)
    burst = nd.binary_fill_holes(nd.binary_closing(red, np.ones((9, 9))))
    lab, n = nd.label(burst)
    if n > 1:
        burst = lab == (int(np.argmax(nd.sum(burst, lab, range(1, n + 1)))) + 1)
    ty = nd.binary_opening(burst & (mx > 150) & (sat < 0.30), np.ones((5, 5)))
    return ty, burst

# ---- build a decal at an arbitrary LINE_GAP, entirely in memory ---------------
def build(line_gap):
    cg.LINE_GAP = line_gap
    cg.LINE_SEP = cg.LINE_SEP_BASE + line_gap * cg.CAP_100
    w, h, W, H = cg.w, cg.h, cg.W, cg.H
    from PIL import ImageDraw
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy, RO = cg.starburst(d)
    img = cg.gradient(img, cx, cy)
    d = ImageDraw.Draw(img)
    sx, sy, sr = w * 0.075, h * 0.60, h * 0.085
    sp = []
    for i in range(10):
        a = math.pi * i / 5 - math.pi / 2
        r = sr if i % 2 == 0 else sr * 0.42
        sp.append((sx + r * math.cos(a), sy + r * math.sin(a)))
    d.polygon(sp, fill=cg.PINK + (255,))
    t = cg.TypeMask(w, h)
    pre = cg._type_centroid()
    shift = (cg.BURST_CX - pre[0], cg.BURST_CY - pre[1])
    cg._place(t, shift)
    # construction truth: pre-rotation row bands of the type mask, full res
    m = np.array(t.m) > 127
    prof = m.sum(1); nz = np.nonzero(prof)[0]
    seg, run = [], None
    for i in range(nz.min(), nz.max() + 2):
        p = prof[i] if i < len(prof) else 0
        if p > 0 and run is None: run = i
        if p == 0 and run is not None:
            seg.append((run, i - 1)); run = None
    if len(seg) != 2:
        cap_px = gap_px = 0; truth = float("nan")
    else:
        cap_px = seg[0][1] - seg[0][0] + 1
        gap_px = seg[1][0] - seg[0][1] - 1
        truth = gap_px / cap_px
    lay = Image.merge("RGBA", (Image.new("L", (w, h), cg.WHITE[0]),
                               Image.new("L", (w, h), cg.WHITE[1]),
                               Image.new("L", (w, h), cg.WHITE[2]), t.m))
    lay = lay.rotate(-math.degrees(cg.ANG), resample=Image.BICUBIC,
                     center=(w * cg.BURST_CX, h * cg.BURST_CY))
    img = Image.alpha_composite(img, lay)
    img = img.resize((W, H), Image.LANCZOS)
    return img, truth, cap_px, gap_px

def photoscale_read(decal_rgba, target=44):
    d = decal_rgba.convert("RGB")
    k = target / float(d.width) * 3.0
    small = d.resize((max(8, int(d.width * k)), max(8, int(d.height * k))), Image.LANCZOS)
    ty, _ = type_mask(small, 8)
    return bands(ty, 8)

if __name__ == "__main__":
    gaps = [float(x) for x in sys.argv[1:]] or [0.10,0.18,0.26,0.34,0.43,0.52,0.60]
    print("%8s %10s %10s %10s %8s %8s" % ("LINE_GAP","truth","reading","read/truth","read-truth","angle"))
    for g in gaps:
        img, truth, cp, gp = build(g)
        r = photoscale_read(img)
        ana = (cg.LINE_SEP - 0.28352) / 0.23256
        if r is None:
            print("%8.3f %10.4f %10s  (analytic %.4f)" % (g, truth, "NO BANDS", ana)); continue
        print("%8.3f %10.4f %10.4f %10.3f %8.4f %8.1f  (fullres cap %d gap %d)"
              % (g, truth, r[0], r[0]/truth, r[0]-truth, r[1], cp, gp), " analytic %.4f"%ana)
