#!/usr/bin/env python3
"""
hero.py -- render one view as overlapping strips, stitch, post once.

WHY THIS EXISTS
The sandbox reaps background processes (nohup/setsid/disown all fail; three
hero attempts were killed 25-30 s in), so a 20-minute frame has to be broken
into synchronous pieces. studio.render_set already supports T1_BORDER="lo,hi".
What it does NOT do is make the pieces join invisibly.

Measured on a 1200x800 hero34f test, four abutting strips vs a single-pass
reference of the same frame: the frame-wide per-row error was 0.090 DN, but at
the three seam rows it was 0.657 / 2.254 / 0.991 DN -- z = +5.2 / +19.4 / +8.2
above the frame's own Monte-Carlo floor, with 42 pixels over 20 DN on the worst
seam against 18 in the entire rest of the frame. The seams were real.

Two causes, and the second is the big one:
  * the pixel reconstruction filter (filter_width 1.50 px) loses support at the
    border edge, so edge pixels are integrated over a clipped kernel;
  * OpenImageDenoise runs per render and its receptive field is tens of pixels
    wide, so a denoised band edge is denoised against missing neighbours.

A 1.5 px filter margin would fix the first and leave the second. So each strip
is rendered with PAD rows of overlap on each side and only its own rows are
copied into the canvas -- the contaminated edge rows are thrown away. PAD
defaults to 48 px, which is 32x the filter width and comfortably past the
denoiser's practical support.

    python3 hero.py VIEW [--res WxH] [--samples N] [--strips N] [--pad PX]
                         [--scene studio|playa] [--out DIR] [--tag NAME]
                         [--sub N] [--no-post] [--extra K=V,K=V]

Optics (bloom/CA/vignette/grain) are forced OFF during the strip renders with
T1_FX=0 and applied once by post.py to the stitched frame. Per-strip optics
band at the seams -- that is what post.py's own docstring warns about.
"""
import argparse
import os
import subprocess
import sys
import time

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BLENDER = os.environ.get("T1_BLENDER", "/tmp/blender/blender")


def sh(cmd, env, label):
    t0 = time.time()
    p = subprocess.run(cmd, env=env, cwd=HERE, capture_output=True, text=True)
    dt = time.time() - t0
    if p.returncode != 0:
        sys.stderr.write(p.stdout[-4000:] + p.stderr[-4000:])
        sys.exit("FAIL %s exited %d" % (label, p.returncode))
    return dt, p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("view")
    ap.add_argument("--res", default="2400x1600")
    ap.add_argument("--samples", type=int, default=64)
    ap.add_argument("--strips", type=int, default=4)
    ap.add_argument("--pad", type=int, default=48)
    ap.add_argument("--scene", default="studio")
    ap.add_argument("--out", default="out")
    ap.add_argument("--tag", default=None)
    ap.add_argument("--sub", default="1")
    ap.add_argument("--no-post", action="store_true")
    ap.add_argument("--post-args", default="")
    ap.add_argument("--extra", default="")
    a = ap.parse_args()

    W, H = (int(t) for t in a.res.lower().split("x"))
    tag = a.tag or ("%s_%s" % (a.scene, a.view))
    tmp = os.path.join(a.out, "strip_%s" % tag)
    os.makedirs(tmp, exist_ok=True)
    os.makedirs(a.out, exist_ok=True)

    # Strip boundaries in ROW space first, so the bands tile H exactly even
    # when H is not divisible by the strip count.
    edges = [int(round(H * i / a.strips)) for i in range(a.strips + 1)]
    print("hero.py  view=%s  %dx%d  %d samples  %d strips  pad=%d px  scene=%s"
          % (a.view, W, H, a.samples, a.strips, a.pad, a.scene))

    total = 0.0
    parts = []
    for i in range(a.strips):
        r0, r1 = edges[i], edges[i + 1] - 1          # rows this strip OWNS
        p0 = max(0, r0 - a.pad)                      # rows it RENDERS
        p1 = min(H - 1, r1 + a.pad)
        # rows -> Blender border, which measures y from the BOTTOM of the frame
        lo, hi = (H - 1 - p1) / H, (H - p0) / H
        env = dict(os.environ)
        env.update({
            "T1_SUB": a.sub, "T1_PREVIEW": a.view, "T1_FX": "0",
            "T1_SCENE": a.scene, "T1_BORDER": "%.6f,%.6f" % (lo, hi),
            "T1_RX": str(W), "T1_RY": str(H), "T1_SAMP": str(a.samples),
            "T1_OUT": tmp, "T1_PFX": "p%d" % i,
        })
        for kv in filter(None, a.extra.split(",")):
            k, v = kv.split("=", 1)
            env[k] = v
        dt, _ = sh([BLENDER, "-b", "--python", "build.py"], env, "strip %d" % i)
        total += dt
        f = os.path.join(tmp, "p%d_%s.png" % (i, a.view))
        if not os.path.exists(f):
            sys.exit("FAIL strip %d produced no file at %s" % (i, f))
        parts.append((r0, r1, f))
        print("  strip %d/%d  owns rows %4d-%4d  rendered %4d-%4d  %5.1f s"
              % (i + 1, a.strips, r0, r1, p0, p1, dt))

    # --- stitch: copy ONLY the owned rows out of each strip -----------------
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    for r0, r1, f in parts:
        im = np.array(Image.open(f).convert("RGBA"))
        if im.shape[:2] != (H, W):
            sys.exit("FAIL %s is %s, expected %dx%d" % (f, im.shape[:2], H, W))
        canvas[r0:r1 + 1] = im[r0:r1 + 1]
    raw = os.path.join(a.out, "%s_raw.png" % tag)
    Image.fromarray(canvas).save(raw)

    # --- seam report --------------------------------------------------------
    rgb = canvas[..., :3].astype(np.float64)
    d = np.abs(np.diff(rgb, axis=0)).mean(axis=(1, 2))
    seams = [e - 1 for e in edges[1:-1]]
    keep = np.ones(H - 1, dtype=bool)
    for s in seams:
        keep[max(0, s - 2):min(H - 1, s + 3)] = False
    mu, sd = d[keep].mean(), d[keep].std()
    worst = 0.0
    print("  interior row-delta mean %.4f sd %.4f DN" % (mu, sd))
    for s in seams:
        z = (d[s] - mu) / max(sd, 1e-9)
        worst = max(worst, abs(z))
        print("  seam row %4d  delta %.4f  z=%+6.2f  %s"
              % (s, d[s], z, "OK" if abs(z) < 4 else "** SEAM **"))
    print("  render %.1f s total, worst seam z=%.2f -> %s" % (total, worst, raw))

    if a.no_post:
        return
    final = os.path.join(a.out, "%s.png" % tag)
    cmd = ["python3", "post.py", raw, final] + a.post_args.split()
    dt, out = sh([c for c in cmd if c], dict(os.environ), "post")
    print(out.strip())
    print("  post %.1f s -> %s" % (dt, final))


if __name__ == "__main__":
    main()
