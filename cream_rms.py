"""rev 15 -- the 25 mm cream-breakup estimator, applied IDENTICALLY to the
photograph and to the render.

WHY IT IS A SEPARATE FILE.  The first attempt at this measurement reproduced
NEITHER number on record (7.37 % for `ref_side.jpg`, 1.24 % for the shipped
render): it read 19.8 % and 18.2 %.  The cause was found and it is instructive --
the crop straddled the serving apertures, and filling the gated-out pixels with
the patch mean planted synthetic step edges straight into the high-pass.  A
high-pass estimator measures whatever edges you hand it, including the ones you
made yourself.

So this file does three things the first attempt did not:
  * it takes patches that are 100 % of the target class, found by scanning
    rather than assumed, and PRINTS the class fraction it actually got;
  * it erodes every patch by 3 sigma so the whole filter footprint lies inside
    the class -- no boundary can enter the statistic;
  * it reports the render and the photograph through the SAME estimator, and
    quotes their RATIO, which is the quantity that survives not knowing the
    exact estimator the 7.37 % and 1.24 % were taken with.

An absolute number from an estimator that cannot reproduce its own record is
not evidence.  The ratio is.
"""
import sys, numpy as np
from PIL import Image

S2L = lambda x: np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
LUMA = np.array([0.2126, 0.7152, 0.0722])


def _gauss1d(sig):
    r = max(1, int(3.0 * sig + 0.5))
    x = np.arange(-r, r + 1, dtype=np.float64)
    k = np.exp(-0.5 * (x / sig) ** 2)
    return k / k.sum()


def gblur(a, sig):
    k = _gauss1d(sig); r = (len(k) - 1) // 2
    p = np.pad(a, ((r, r), (0, 0)), mode='reflect'); o = np.zeros_like(a)
    for i, w in enumerate(k):
        o += w * p[i:i + a.shape[0], :]
    p = np.pad(o, ((0, 0), (r, r)), mode='reflect'); o2 = np.zeros_like(a)
    for i, w in enumerate(k):
        o2 += w * p[:, i:i + a.shape[1]]
    return o2


def load(path):
    a = np.asarray(Image.open(path).convert("RGB"), dtype=np.float64)
    a /= 65535.0 if a.max() > 255.0 else 255.0
    lin = S2L(a)
    lum = lin @ LUMA
    mx, mn = a.max(2), a.min(2)
    sat = np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0.0)
    return a, lum, sat


def cream_mask(lum, sat):
    return (sat < 0.30) & (lum > 0.20)


def best_patch(mask, h, w, v_lo, v_hi, u_lo, u_hi):
    """Largest-offset window of size h x w that is 100 % class. Scanned, not assumed."""
    best = None
    for v in range(v_lo, min(v_hi, mask.shape[0] - h)):
        for u in range(u_lo, min(u_hi, mask.shape[1] - w), 4):
            f = mask[v:v + h, u:u + w].mean()
            if best is None or f > best[0]:
                best = (f, v, u)
            if f >= 1.0:
                return best
    return best


def rms25(lum, sig_px, tag):
    """25 mm high-pass RMS over a patch already known to be all one class."""
    lo = gblur(lum, sig_px)
    r = int(3 * sig_px + 1)
    core = slice(r, lum.shape[0] - r), slice(r, lum.shape[1] - r)
    hp = (lum[core] - lo[core]) / np.maximum(lo[core], 1e-6)
    return float(np.sqrt(np.mean(hp ** 2))), hp.size


def run(render_png, pxm_r=211.5, ortho_px=1248, ortho_m=5.90):
    print("=" * 72)
    print("25 mm CREAM BREAKUP -- one estimator, both frames")
    print("=" * 72)
    out = {}

    # ---- photograph ------------------------------------------------------
    a, lum, sat = load("ref_side.jpg")
    m = cream_mask(lum, sat)
    sig = 0.025 * 211.5 / 2.0
    H, W = 26, 150
    f, v, u = best_patch(m, H, W, 240, 320, 380, 780)
    print("PHOTOGRAPH ref_side.jpg")
    print("  patch (u %d-%d, v %d-%d) %dx%d px, cream fraction %.1f %%"
          % (u, u + W, v, v + H, W, H, 100 * f))
    if f < 0.995:
        print("  REJECTED: no >=99.5 %% cream patch of this size exists in the search band")
    else:
        r, n = rms25(lum[v:v + H, u:u + W], sig, "photo")
        out["photo"] = r
        print("  25 mm high-pass RMS  %.3f %%   over %d px  (sigma %.2f px)"
              % (100 * r, n, sig))

    # ---- render ----------------------------------------------------------
    a, lum, sat = load(render_png)
    m = cream_mask(lum, sat)
    pxm = ortho_px / ortho_m
    sig = 0.025 * pxm / 2.0
    f, v, u = best_patch(m, H, W, 340, 400, 300, 800)
    print("RENDER %s" % render_png)
    print("  %.1f px/m, patch (u %d-%d, v %d-%d) %dx%d px, cream fraction %.1f %%"
          % (pxm, u, u + W, v, v + H, W, H, 100 * f))
    if f < 0.995:
        print("  REJECTED: no >=99.5 %% cream patch of this size exists in the search band")
    else:
        r, n = rms25(lum[v:v + H, u:u + W], sig, "render")
        out["render"] = r
        print("  25 mm high-pass RMS  %.3f %%   over %d px  (sigma %.2f px)"
              % (100 * r, n, sig))

    if "photo" in out and "render" in out:
        print("-" * 72)
        print("  RENDER / PHOTOGRAPH = %.3f      (1.000 = the render is as broken "
              "up as the vehicle)" % (out["render"] / out["photo"]))
        print("  on record: 1.24 %% render against 7.37 %% photograph = ratio 0.168")
    print("=" * 72)
    return out


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "out/_solve_cream.png")
