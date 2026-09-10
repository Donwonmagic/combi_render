"""
foto.py -- MEASURE THE OWNER'S PHOTOGRAPH, AND COMMIT WHAT IT SAYS.

⚠ WHY THIS EXISTS.  `pliego.py` set its gold ground by a figure written into a
comment -- "his disc reads 1.629:1 against his ground" -- and NO SCRIPT
COMPUTED IT.  That is this project's rule 5 exactly: never put a figure in an
acceptance test unless you watched it print.  A grader attacked the number and
was right to: the justification for the most-used colour in the suite was a
sentence.

What can honestly be taken from a photograph is the RATIO BETWEEN TWO AREAS OF
THE SAME FRAME under the same light.  Absolute values cannot -- they carry the
exposure, the white balance and the time of day.  So this measures the sign
face, writes the clusters and the ratios to `foto_sign.json`, and `pliego.py`
checks its own palette against THAT rather than against a remembered number.

Run:  python3 foto.py            # measures and rewrites foto_sign.json
      python3 foto.py --check    # re-measures and compares, prints, changes nothing
"""
import json, os, sys
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTO = os.path.join(AQUI, "ref_sign_aframe.jpg")
SALIDA = os.path.join(AQUI, "foto_sign.json")

# The sign face inside the frame, as fractions of the image.  ⚠ AUTHORED, by
# looking: the photograph is a rotated A-frame on a pavement and the board does
# not fill it.  This window is PAINTED by --paint so it can be checked by eye
# rather than trusted (rule 8).
VENTANA = (0.052, 0.093, 0.560, 0.910)     # x0, y0, x1, y1


def _lum(rgb):
    v = [c / 255.0 for c in rgb]
    v = [(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4) for c in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


def contrast(a, b):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def medir(k=6, paint=None):
    im = Image.open(FOTO).convert("RGB")
    W, H = im.size
    a = np.asarray(im).astype(np.float64)
    x0, y0, x1, y1 = VENTANA
    reg = a[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)]
    flat = reg[::9, ::9].reshape(-1, 3)
    from scipy.cluster.vq import kmeans2
    cen, lab = kmeans2(flat, k, minit="++", seed=3)
    cnt = np.bincount(lab, minlength=k)
    order = np.argsort(-cnt)
    clusters = [{"hex": "#%02X%02X%02X" % tuple(int(round(v)) for v in cen[i]),
                 "rgb": [int(round(v)) for v in cen[i]],
                 "share": round(float(cnt[i]) / cnt.sum(), 4)}
                for i in order]
    if paint:
        q = np.asarray(im).copy()
        q[int(y0 * H):int(y0 * H) + 24, int(x0 * W):int(x1 * W)] = (255, 0, 255)
        q[int(y1 * H) - 24:int(y1 * H), int(x0 * W):int(x1 * W)] = (255, 0, 255)
        q[int(y0 * H):int(y1 * H), int(x0 * W):int(x0 * W) + 24] = (255, 0, 255)
        q[int(y0 * H):int(y1 * H), int(x1 * W) - 24:int(x1 * W)] = (255, 0, 255)
        Image.fromarray(q).resize((W // 6, H // 6), Image.LANCZOS).save(paint)
    return clusters


def main(argv):
    paint = None
    for i, v in enumerate(argv):
        if v == "--paint":
            paint = argv[i + 1]
    cl = medir(paint=paint)
    # the two largest are the GROUND and the LIGHT DISC; both are wanted
    ground, disc = cl[0], cl[1]
    # ⚠⚠ THE INVARIANT IS THE REFLECTANCE RATIO, NOT THE WCAG RATIO, AND THE
    # FIRST VERSION OF THIS TRANSFERRED THE WRONG ONE.  A grader caught it: the
    # argument "both under the same light in the same frame, so the RATIO
    # between them is what can be trusted" is TRUE of L1/L2 and FALSE of
    # (L1+0.05)/(L2+0.05), because the +0.05 offset is not scale-invariant.
    # Double the exposure and the reflectance ratio is unchanged while the WCAG
    # figure moves.  So the quantity carried across is L_light/L_gold; the WCAG
    # number is recorded beside it as a reading convenience and is NOT what the
    # palette is fitted to.
    lr = _lum(disc["rgb"]) / max(1e-9, _lum(ground["rgb"]))
    out = {
        "source": "ref_sign_aframe.jpg",
        "window": list(VENTANA),
        "clusters": cl,
        "ground": ground["hex"],
        "disc": disc["hex"],
        "light_over_ground_luminance": round(lr, 4),
        "disc_on_ground_wcag": round(contrast(disc["rgb"], ground["rgb"]), 4),
        "note": ("REFLECTANCE RATIO ONLY. L_light/L_gold survives a change of "
                 "exposure; absolute values do not, and neither does the WCAG "
                 "ratio, whose +0.05 offset breaks scale invariance."),
    }
    print("sign face, %d clusters:" % len(cl))
    for c in cl:
        print("  %6.2f %%  %s" % (100 * c["share"], c["hex"]))
    print()
    print("ground %s   light ink %s" % (out["ground"], out["disc"]))
    print("  L_light / L_gold = %.4f   <- THE INVARIANT, transferred"
          % out["light_over_ground_luminance"])
    print("  WCAG            = %.4f   <- recorded, NOT fitted to"
          % out["disc_on_ground_wcag"])
    if "--check" in argv:
        old = json.load(open(SALIDA))
        d = abs(old["light_over_ground_luminance"]
                - out["light_over_ground_luminance"])
        print("committed %.4f, re-measured %.4f, delta %.4f"
              % (old["light_over_ground_luminance"],
                 out["light_over_ground_luminance"], d))
        return 0 if d < 0.02 else 1
    json.dump(out, open(SALIDA, "w"), indent=1)
    print("-> %s" % SALIDA)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
