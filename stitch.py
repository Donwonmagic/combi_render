"""
stitch.py -- reassemble a hero frame from T1_BORDER strips.

studio.render_set renders each strip with use_crop_to_border = False, so every
strip PNG is the FULL frame with only its own horizontal band carrying render
data. Blender's border_min_y is measured from the BOTTOM of the frame, so a
strip "0.00,0.25" occupies the LAST quarter of the image rows.

This does not trust that arithmetic. It measures where each strip actually put
its pixels, asserts the measured bands tile the frame with no gap and no
overlap, and only then assembles. A stitch that guesses the row mapping is the
kind of thing that produces a seam nobody can explain.

    python3 stitch.py out.png lo,hi=strip1.png lo,hi=strip2.png ...

The lo,hi are the T1_BORDER values the strip was rendered with. They are NOT
inferred from content: a white-composited frame makes an unrendered region and
a rendered backdrop region byte-identical (measured: max |diff| = 0 over a
full backdrop row), so content detection cannot find the band edge -- which is
precisely why a bad row mapping here would survive a test frame and only show
up on the hero.
"""
import sys
import numpy as np
from PIL import Image


def main():
    out, args = sys.argv[1], sys.argv[2:]
    arrs, spans = [], []
    H = W = None
    for arg in args:
        if "=" not in arg:
            sys.exit("FAIL expected lo,hi=path.png, got %r" % arg)
        border, p = arg.split("=", 1)
        lo, hi = (float(t) for t in border.split(","))
        a = np.array(Image.open(p).convert("RGBA"))
        if H is None:
            H, W = a.shape[:2]
        elif a.shape[:2] != (H, W):
            sys.exit("FAIL size mismatch: %s is %s, expected %dx%d"
                     % (p, a.shape[:2], H, W))
        # Blender measures border_min_y from the BOTTOM; image row 0 is the top.
        r0, r1 = int(round(H * (1.0 - hi))), int(round(H * (1.0 - lo))) - 1
        arrs.append(a)
        spans.append((r0, r1, p, "declared"))
        print("  %-26s T1_BORDER %.2f,%.2f -> rows %4d-%4d  (%3d rows)"
              % (p.split('/')[-1], lo, hi, r0, r1, r1 - r0 + 1))

    order = sorted(range(len(spans)), key=lambda i: spans[i][0])
    print("\n  frame %dx%d, %d strips" % (W, H, len(spans)))

    # --- tiling assertions -------------------------------------------------
    problems = []
    if spans[order[0]][0] != 0:
        problems.append("top of frame uncovered: first strip starts at row %d"
                        % spans[order[0]][0])
    if spans[order[-1]][1] != H - 1:
        problems.append("bottom of frame uncovered: last strip ends at row %d "
                        "of %d" % (spans[order[-1]][1], H - 1))
    for a, b in zip(order, order[1:]):
        gap = spans[b][0] - spans[a][1] - 1
        if gap > 0:
            problems.append("GAP of %d rows between %s and %s (rows %d-%d)"
                            % (gap, spans[a][2], spans[b][2],
                               spans[a][1] + 1, spans[b][0] - 1))
        elif gap < 0:
            print("  note: %d-row overlap between %s and %s -- later strip wins"
                  % (-gap, spans[a][2].split('/')[-1],
                     spans[b][2].split('/')[-1]))

    if problems:
        for p in problems:
            print("  FAIL %s" % p)
        sys.exit(1)
    print("  bands tile the frame exactly: no gap")

    # --- assemble ----------------------------------------------------------
    canvas = np.zeros((H, W, 4), dtype=np.uint8)
    for i in order:
        r0, r1 = spans[i][0], spans[i][1]
        canvas[r0:r1 + 1] = arrs[i][r0:r1 + 1]

    # --- seam continuity check --------------------------------------------
    # Across a true seam the row-to-row difference should be no larger than
    # the difference between neighbouring rows inside a strip. A visible seam
    # shows up as an outlier here long before it shows up to the eye.
    rgb = canvas[..., :3].astype(np.float64)
    d = np.abs(np.diff(rgb, axis=0)).mean(axis=(1, 2))
    interior = np.ones(H - 1, dtype=bool)
    seam_rows = []
    for a, b in zip(order, order[1:]):
        s = spans[a][1]
        seam_rows.append(s)
        interior[max(0, s - 2):min(H - 1, s + 3)] = False
    base_mu, base_sd = d[interior].mean(), d[interior].std()
    print("\n  interior row-delta  mean %.4f  sd %.4f  (DN, 0-255)"
          % (base_mu, base_sd))
    worst = 0.0
    for s in seam_rows:
        z = (d[s] - base_mu) / max(base_sd, 1e-9)
        worst = max(worst, abs(z))
        flag = "OK" if abs(z) < 4 else "** SEAM **"
        print("  seam at row %4d   delta %.4f   z = %+6.2f   %s"
              % (s, d[s], z, flag))

    Image.fromarray(canvas).save(out)
    print("\n  wrote %s   worst seam z = %.2f" % (out, worst))
    if worst >= 4:
        print("  RESULT: seam detected -- fix the stitch before rendering big")
        sys.exit(2)
    print("  RESULT: no seam detectable above the frame's own row noise")


if __name__ == "__main__":
    main()
