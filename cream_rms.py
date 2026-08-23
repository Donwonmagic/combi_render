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
import os
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
    """rev 17 -- KEPT ONLY SO THE OLD, WRONG RESULT STAYS REPRODUCIBLE.

    `sat < 0.30 & lum > 0.20` is not a test for "cream paint".  It is a test for
    "pale", and a lit galley seen through an open serving bay, a cream jacket
    and a whitewashed background wall all pass it.  Use `body_cream_mask`.
    """
    return (sat < 0.30) & (lum > 0.20)


# ---------------------------------------------------------------- rev 17
# THE GEOMETRY GATE, and why this file needed one.
#
# `run()` below searched v 240-320, u 380-780 of ref_side.jpg for the best
# 100 %-cream window and reported 8.890 % as "the cream".  It is not the cream.
# Against the two LOCKED image lines -- rev 16's drip-rail fit and SPEC 10.34's
# 27.7 mm drip-to-aperture -- the guarded serving-aperture band at those columns
# is v 305.6-399.0, and the chosen patch (u 592-742, v 319-345) lies ENTIRELY
# inside it.  The number is the GALLEY INTERIOR seen through bay 3, at 99.8 %
# "class purity", because the galley is pale and the gate only tests pale.
#
# The search band cannot avoid it: v 240-320 overlaps the aperture band from
# v 304 down, and the galley is the most uniform pale thing in the frame, so it
# wins the scan.  Every "the cream is 26x too uniform" statement on this project
# compares the render's paint against an open hole.
#
# This file's own docstring already warned that a high-pass estimator measures
# whatever edges you hand it.  rev 15 fixed the FILL and left the SEARCH BAND.
# The rule that generalises, and it is new: A CLASS GATE IS A PROBE TOO. Gate on
# GEOMETRY -- which surface of the vehicle -- before gating on colour.
#
# Constants below are the locked ones, not re-typed metres:
#   drip rail   v = -0.04409 u + 332.301   rev 16 fit, rms 0.067 px, n = 83
#   drip -> aperture top  27.7 +- 0.5 mm   SPEC 10.34, 228 columns, 3 bays
#   aperture band height  1.775 - 1.372    verify.py's guarded band
#   k_t = 215.5 px/m                       validated by belt->aperture to 0.4 %
_DRIP  = lambda u: -0.04409 * u + 332.301
_K_T   = 215.5
_ATOP  = lambda u: _DRIP(u) + 0.0277 * _K_T
_ABOT  = lambda u: _ATOP(u) + (1.775 - 1.372) * _K_T
_BELT  = lambda u: _ABOT(u) + (1.372 - 1.2070) * _K_T


def aperture_band(shape, pad=4.0):
    """Boolean mask of the guarded serving-aperture band in ref_side.jpg."""
    h, w = shape
    uu = np.arange(w)[None, :] * np.ones((h, 1))
    vv = np.arange(h)[:, None] * np.ones((1, w))
    return (vv >= _ATOP(uu) - pad) & (vv <= _ABOT(uu) + pad)


def body_cream_mask(lum, sat, rgb255=None):
    """Cream that is actually the BODY's paint in ref_side.jpg.

    Colour gate tightened (a jacket and a wall both pass sat<0.30), plus four
    geometric exclusions, each anchored to something already locked:
      * below the drip rail            (above it is roof / lid / sky)
      * above the two-tone belt line   (below it is red paint and the counter)
      * outside the aperture band      (inside it is the galley, not paint)
      * forward of the tail column     u < 916  (X(922.2) = -1.873, the tail)
    Returns the mask; the CALLER must check how much survives.
    """
    h, w = lum.shape
    uu = np.arange(w)[None, :] * np.ones((h, 1))
    vv = np.arange(h)[:, None] * np.ones((1, w))
    m = (sat < 0.16) & (lum > 0.45)
    if rgb255 is not None:
        m &= (rgb255.max(2) < 254)                       # unclipped only
    m &= (vv > _DRIP(uu) + 3) & (vv < _BELT(uu) - 2)
    m &= ~aperture_band(lum.shape)
    m &= (uu > 200) & (uu < 916)
    return m


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


def _legacy_ref_side(render_png, pxm_r=211.5, ortho_px=1248, ortho_m=5.90):
    """THE DEAD PATH, KEPT SO THE RETRACTION STAYS WATCHABLE (rule 15).

    This was `run()` from rev 13 to rev 55.  It measures ref_side.jpg, hits
    the rev-17 hard guard, prints LEGACY PATH, RESULT IS NOT CREAM and returns
    {} -- it has produced no number for eight revisions.  It is NOT deleted:
    it is the thing that demonstrates WHY the re-base was necessary, and a
    reader who wants to see ref_side.jpg fail to supply a body-cream patch
    runs `T1_CR_LEGACY=1 python3 cream_rms.py`.
    """
    print("=" * 72)
    print("25 mm CREAM BREAKUP -- one estimator, both frames")
    print("=" * 72)
    out = {}

    # ---- photograph ------------------------------------------------------
    a, lum, sat = load("ref_side.jpg")
    # rev 17 HARD GUARD.  The old path measured the galley through bay 3 and
    # called it cream.  Refuse to report that number again: assert the chosen
    # patch is not inside the guarded aperture band, and say so in the console.
    m = cream_mask(lum, sat)
    sig = 0.025 * 211.5 / 2.0
    H, W = 26, 150
    f, v, u = best_patch(m, H, W, 240, 320, 380, 780)
    _ap = aperture_band(lum.shape)[v:v + H, u:u + W].mean()
    if _ap > 0.05:
        print("PHOTOGRAPH ref_side.jpg -- LEGACY PATH, RESULT IS NOT CREAM")
        print("  patch (u %d-%d, v %d-%d) is %.0f %% inside the guarded serving-"
              "aperture\n  band (v %.1f-%.1f at these columns).  It is the GALLEY "
              "INTERIOR seen\n  through bay 3, not the body's paint.  See the rev-17 "
              "note above."
              % (u, u + W, v, v + H, 100 * _ap, _ATOP(u + W), _ABOT(u)))
        _bm = body_cream_mask(lum, sat, a * 255.0)
        print("  body-cream pixels that survive the geometry gate in this frame: "
              "%d (%.2f %% of frame)" % (int(_bm.sum()), 100 * _bm.mean()))
        _bf, _bv, _bu = best_patch(_bm, 20, 60, 200, 470, 200, 856)
        print("  best 60x20 body-cream window: %.1f %% pure  ->  ref_side.jpg "
              "CANNOT\n  supply a clean body-cream patch.  Re-base on ref_rear34.jpg "
              "(rev 17)." % (100 * _bf))
        print("=" * 72)
        return {}
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


def run(render_png=None):
    """WHAT A READER RUNS.  rev 56 pointed it at the LIVE measurement.

    From rev 13 to rev 55 this name was bound to the ref_side.jpg path, which
    hits the rev-17 hard guard and returns {}.  So three consecutive briefs
    carried "re-base cream_rms.py onto ref_rear34.jpg, open since rev 17" as
    an open item WHILE THE RE-BASED MEASUREMENT WAS ALREADY WRITTEN, in this
    same file, a hundred lines below -- and nothing called it.  The open item
    was never the measurement.  It was the entry point.

    WHY THERE IS NO RENDER ARM HERE, AND WHY THAT IS NOT AN OMISSION.  The
    render side needs a mask, and a COLOUR gate on a render of the very
    surface whose colour is under test is circular -- mottle_measure.py's own
    docstring says so and chooses the patch in MODEL space instead.  This
    function will not run a colour-gated render arm and call it a second
    opinion.  It names the render arm and the command that runs it.
    """
    print("=" * 74)
    print("cream_rms.run() -- the LIVE re-based path (rev 17 re-base, rev 56 wired up)")
    print("=" * 74)
    if os.environ.get("T1_CR_LEGACY") == "1":
        print("T1_CR_LEGACY=1 -- running the DEAD ref_side.jpg path instead, so\n"
              "the reason for the re-base can be watched rather than believed.\n")
        return _legacy_ref_side(render_png or "out/_solve_cream.png")
    got = spectrum()
    if got is None:
        print("\n  spectrum() REFUSED -- no usable patch.  No number is reported,")
        print("  and none may be quoted from this run.")
        print("=" * 74)
        return {}
    spec, mask, Y = got
    character()
    print("=" * 74)
    print("THE RENDER ARM IS mottle_measure.py, AND IT NEEDS BLENDER:")
    print("    T1_SUB=1 /tmp/blender/blender -b -P mottle_measure.py")
    print("  It projects a MODEL-SPACE patch through an ORTHO render, so its")
    print("  px/m is exact by construction, and it compares at matched")
    print("  PHYSICAL scale against exactly the spectrum printed above.")
    print("  As of rev 56 it DERIVES that target by calling spectrum() rather")
    print("  than carrying it as five typed literals.")
    print("=" * 74)
    return spec



# ====================================================================== rev 17
# THE RE-BASED MEASUREMENT.  ref_side.jpg cannot supply a body-cream patch
# (33.8 % pure at 60x20, 1799 gated pixels in the whole frame), and it is also
# the worst frame this project owns:
#
#   ref_side.jpg      1024x768   2.32 bits/px   JPEG DC quantiser 4
#   ref_rear34.jpg    1200x824   9.28 bits/px   JPEG DC quantiser 1
#   ref_workshop.jpg  1200x824   8.87 bits/px   JPEG DC quantiser 1
#
# DC quantiser 1 is essentially lossless.  The owner chose to re-base on
# ref_rear34.jpg, which is one of his own three photographs.
#
# The largest clean cream in ANY frame is the LID UNDERSIDE -- the panel
# lettered "La Santa" -- at u 588-760, v 40-190: 25 800 px, 80.8 % class-pure
# after a 3 px erosion, 0.2 % clipped.  State the caveat with every number taken
# from it: it is an INWARD-FACING panel, so its weathering is a LOWER BOUND on
# the sun-exposed flank's.
#
# THE CODEC FLOOR ESTIMATOR IS NOT THE OBVIOUS ONE, and the obvious one is
# wrong.  Blurring at sigma and then high-passing at sigma does NOT leave zero
# -- a difference of two Gaussians passes plenty -- so "smooth, re-encode,
# measure" charges the codec for the blur's own leak.  Measured: that mistake
# overstated the floor by about 4x (it read 1.7-2.7 % where the true codec
# contribution is 0.31-0.66 %).  `codec_floor` below blurs by 4*sigma, measures
# the LEAK with no codec at all, and subtracts it in quadrature.  The leak is
# printed so it can never go unchecked again.

_LID = (588, 760, 40, 190)          # u0, u1, v0, v1 -- the "La Santa" panel


def codec_floor(path, box, mask, sig, prefactor=4.0):
    """Codec-only RMS at scale `sig`, with the blur's own leak subtracted."""
    import io
    from PIL import Image as _I
    im0 = _I.open(path); qt = im0.quantization
    raw = np.asarray(im0.convert("RGB"), dtype=np.float64)
    u0, u1, v0, v1 = box
    sm = np.empty_like(raw)
    for c in range(3):
        sm[:, :, c] = gblur(raw[:, :, c], sig * prefactor)

    def _rms(arr):
        z = S2L(np.clip(arr, 0, 255) / 255.0) @ LUMA
        zz = z[v0:v1, u0:u1]; lo = gblur(zz, sig)
        return float(np.sqrt((((zz - lo) / np.maximum(lo, 1e-6))[mask] ** 2).mean()))

    leak = _rms(sm)                                   # no codec at all
    b = io.BytesIO()
    _I.fromarray(np.clip(sm, 0, 255).astype(np.uint8)).save(
        b, "JPEG", qtables=qt, subsampling="4:2:2"); b.seek(0)
    both = _rms(np.asarray(_I.open(b).convert("RGB"), dtype=np.float64))
    return leak, float(np.sqrt(max(both ** 2 - leak ** 2, 0.0)))


def rear34_cream(box=_LID):
    """The cream's spectrum and CHARACTER off ref_rear34.jpg.  Scale-free."""
    from PIL import Image as _I
    f = "ref_rear34.jpg"
    a, lum, sat = load(f)
    raw = np.asarray(_I.open(f).convert("RGB"), dtype=np.float64)
    u0, u1, v0, v1 = box
    sub = raw[v0:v1, u0:u1]; S = sat[v0:v1, u0:u1]
    mask = (S < 0.20) & (sub.max(2) < 254)            # drop the red script + star
    for _ in range(3):                                # 3 px erosion
        m = mask.copy()
        m[1:, :] &= mask[:-1, :]; m[:-1, :] &= mask[1:, :]
        m[:, 1:] &= mask[:, :-1]; m[:, :-1] &= mask[:, 1:]
        mask = m
    Y = S2L(sub / 255.0) @ LUMA
    print("=" * 74)
    print("rev 17 -- CREAM off ref_rear34.jpg, lid underside u %d-%d v %d-%d"
          % (u0, u1, v0, v1))
    print("  class-pure after 3 px erosion: %.1f %%   (inward-facing panel: this"
          " is a LOWER BOUND\n  on the sun-exposed flank)" % (100 * mask.mean()))
    print("  sigma_px   total %    leak %    codec %    REAL %")
    out = {}
    for sg in (1.0, 2.0, 4.0, 8.0, 12.0):
        lo = gblur(Y, sg)
        t = float(np.sqrt((((Y - lo) / np.maximum(lo, 1e-6))[mask] ** 2).mean()))
        lk, cf = codec_floor(f, box, mask, sg)
        real = np.sqrt(max(t * t - cf * cf, 0.0))
        out[sg] = real
        print("   %5.1f    %8.3f  %8.3f  %8.3f  %8.3f"
              % (sg, 100 * t, 100 * lk, 100 * cf, 100 * real))
    print("  SCALE IS OPEN: three routes to px/m on this frame all failed --")
    print("    aperture band  truncated by the counter   (>= 320 px/m)")
    print("    tyre OD        truncated by the frame     (>= 397 px/m)")
    print("    bulb string    NOT DETECTED, peak/mean 3.6, candidates 225-629")
    print("  So the mm axis is NOT established.  Do not convert these to mm yet.")
    return out, mask, Y


def rear34_character(box=_LID):
    """Which KIND of texture it is.  None of these needs an absolute scale."""
    _, mask, Y = rear34_cream(box)
    from PIL import Image as _I
    a, lum, sat = load("ref_rear34.jpg")
    u0, u1, v0, v1 = box
    lin = S2L(np.asarray(_I.open("ref_rear34.jpg").convert("RGB"),
                         dtype=np.float64)[v0:v1, u0:u1] / 255.0)
    M = np.array([[0.4124, 0.3576, 0.1805],
                  [0.2126, 0.7152, 0.0722],
                  [0.0193, 0.1192, 0.9505]])
    XYZ = lin @ M.T; t = XYZ / np.array([0.9505, 1.0, 1.089]); d = 6 / 29
    fx = np.where(t > d ** 3, np.cbrt(np.clip(t, 1e-9, None)), t / (3 * d * d) + 4 / 29)
    Ls = 116 * fx[..., 1] - 16
    A_ = 500 * (fx[..., 0] - fx[..., 1]); B_ = 200 * (fx[..., 1] - fx[..., 2])
    Cs = np.sqrt(A_ * A_ + B_ * B_)
    print("-" * 74)
    print("CHARACTER -- fade vs dirt vs brush vs dents")
    print("  sigma   corr(dL*,dC*)   dL* rms   dC* rms   anisotropy v/u   skew")
    for sg in (2.0, 4.0, 8.0):
        hl = Ls - gblur(Ls, sg); hc = Cs - gblur(Cs, sg)
        r = np.corrcoef(hl[mask], hc[mask])[0, 1]
        b = Y - gblur(Y, sg); k = int(3 * sg + 1)
        bb = b[k:-k, k:-k]; mm = mask[k:-k, k:-k]
        gx = np.diff(bb, axis=1); gy = np.diff(bb, axis=0)
        an = (np.sqrt((gy[mm[:-1, :]] ** 2).mean())
              / np.sqrt((gx[mm[:, :-1]] ** 2).mean()))
        x = (Y - gblur(Y, sg))[mask]
        sk = ((x - x.mean()) ** 3).mean() / max(x.std() ** 3, 1e-12)
        print("  %5.1f      %+7.3f       %6.3f    %6.3f        %.3f       %+6.2f"
              % (sg, r, hl[mask].std(), hc[mask].std(), an, sk))
    print("  READING:  corr(dL*,dC*) NEGATIVE and growing with scale, chroma")
    print("  structure of the same order as luminance, anisotropy ~0.9 (isotropic).")
    print("  -> CHALKY SUN-FADE MOTTLE: patches oxidised LIGHTER and LESS")
    print("     chromatic.  NOT dirt (both would fall together, corr positive),")
    print("     NOT brush/roller (chroma would be flat), NOT dents (chroma flat")
    print("     and structure smooth at large scale only).")
    print("  CONSEQUENCE FOR THE FIX, and it explains why W_ALBEDO could never")
    print("  work: a SCALAR MULTIPLY ON ALBEDO CANNOT CHANGE CHROMA.  The map")
    print("  must modulate the EXISTING fade path (rev 14's FadeVert, which")
    print("  fades toward white and is currently spatially constant), and drive")
    print("  roughness with it.  It is not an albedo-breakup map.")
    print("=" * 74)


# ---------------------------------------------------------------------------
# rev 19 -- THE CREAM SOURCE MOVES OFF THE SIGN AND ONTO THE VEHICLE.
#
# `_LID` above is the panel lettered "La Santa".  Every cream number in rev 17
# and rev 18 came off it, under the comment "the LID UNDERSIDE ... an
# INWARD-FACING panel, so its weathering is a LOWER BOUND on the sun-exposed
# flank's".  Shown the marked crop, the owner identified it as **A DETACHED
# SIGN, SEPARATE FROM THE BUS** -- which is also his own earlier settled
# reading.  So it is not the lid, it is not inward-facing bodywork, and its
# paint history is not the vehicle's.  Both halves of that comment are void and
# `_LID` is RETIRED as a cream reference.  It is kept only so the retired
# numbers can be reproduced.
#
# `_BODY` is the surface he identified as the bus's own painted cream: the
# solid sheet metal aft of the serving apertures.  His box was
# (860,270)-(970,390); it is trimmed here for a measured reason, not a taste
# one -- 10.17 % of that box is CLIPPED (max channel >= 254), all of it in
# columns 860-882, a blown specular sheen on the left edge, plus a brass strip
# across rows 270-287.  A clipped pixel carries NO texture, so leaving it in
# drags a high-pass RMS toward zero.  The trim removes every clipped pixel:
#
#     (885, 968, 292, 388)   83 x 96 = 7968 px   clipped 0.00 %
#
# THE GATE IS GEOMETRY ONLY, and that is deliberate.  rev 17's rule is that a
# class gate is a probe too.  Inside a box the owner has identified by eye, a
# COLOUR gate cannot add information -- it can only remove pixels for looking
# unlike whatever surface the gate was tuned on.  The old `sat < 0.20` gate is
# tuned to the sign (C* 11.2) and rejects the bus's own cream (C* 19.9): it
# returns 2.9 % purity on this very panel.  So the only rejection here is
# CLIPPING, which is a sensor fact, not a class judgement.
_BODY = (885, 968, 292, 388)        # u0, u1, v0, v1 -- bus cream, aft of bays


def _lab(rgb01):
    M = np.array([[0.4124, 0.3576, 0.1805],
                  [0.2126, 0.7152, 0.0722],
                  [0.0193, 0.1192, 0.9505]])
    XYZ = rgb01 @ M.T
    t = XYZ / np.array([0.9505, 1.0, 1.089]); d = 6 / 29
    f = np.where(t > d ** 3, np.cbrt(np.clip(t, 1e-9, None)), t / (3 * d * d) + 4 / 29)
    L = 116 * f[..., 1] - 16
    A = 500 * (f[..., 0] - f[..., 1]); B = 200 * (f[..., 1] - f[..., 2])
    return L, np.sqrt(A * A + B * B)


def spectrum(box=_BODY, path="ref_rear34.jpg", label="bus cream", quiet=False):
    """Scale-indexed REAL high-pass RMS on a geometry-gated patch.

    Returns (dict sigma->real%, mask, Y) or **None** if the patch cannot
    support the measurement.  It returns None rather than a number on purpose:
    two phantoms in this repo came from a probe answering when it could not
    (`audit.py`'s `or -9`, `_roof_at`'s fall-through), and rev 18 wrote the
    rule.  `rear34_character` below obeys the same rule for its VERDICT.
    """
    from PIL import Image as _I
    u0, u1, v0, v1 = box
    raw = np.asarray(_I.open(path).convert("RGB"), dtype=np.float64)
    sub = raw[v0:v1, u0:u1]
    if sub.size == 0:
        return None
    mask = sub.max(2) < 254                      # clipping only -- see note
    frac = float(mask.mean())
    for _ in range(3):                           # 3 px erosion
        m = mask.copy()
        m[1:, :] &= mask[:-1, :]; m[:-1, :] &= mask[1:, :]
        m[:, 1:] &= mask[:, :-1]; m[:, :-1] &= mask[:, 1:]
        mask = m
    Y = S2L(sub / 255.0) @ LUMA
    n = int(mask.sum())
    if not quiet:
        print("=" * 74)
        print("rev 19 -- %s off %s, u %d-%d v %d-%d  (%d x %d px)"
              % (label.upper(), path, u0, u1, v0, v1, u1 - u0, v1 - v0))
        print("  gate: GEOMETRY (owner-identified) + unclipped only.  No colour gate.")
        print("  unclipped %.1f %% -> %d px survive a 3 px erosion" % (100 * frac, n))
    if n < 500:
        if not quiet:
            print("  *** REFUSING TO REPORT: %d usable px is too few. Returns None." % n)
        return None
    out = {}
    if not quiet:
        print("  sigma_px   total %    leak %    codec %    REAL %")
    for sg in (1.0, 2.0, 4.0, 8.0, 12.0):
        lo = gblur(Y, sg)
        t = float(np.sqrt((((Y - lo) / np.maximum(lo, 1e-6))[mask] ** 2).mean()))
        lk, cf = codec_floor(path, box, mask, sg)
        real = float(np.sqrt(max(t * t - cf * cf, 0.0)))
        out[sg] = real
        if not quiet:
            print("   %5.1f    %8.3f  %8.3f  %8.3f  %8.3f"
                  % (sg, 100 * t, 100 * lk, 100 * cf, 100 * real))
    if not quiet:
        print("  SCALE: px/m on THIS plane is not 344.1.  344.1 +- 6.7 is the")
        # rev 55: `depth_correct()` IS NOT DEFINED ANYWHERE IN THIS REPO.
        # It was cited here as if it were the remedy for the scale caveat and
        # a reader following it finds nothing.  The citation is corrected
        # rather than removed, because the CAVEAT is real and still stands.
        # What actually carries the mm axis today is mottle_measure.py's
        # PXM_REF (337.0 px/m, "flank plane, bracketed 330-344; NOT the
        # plate's 344.1") -- a bracket, not a measurement.
        print("    PLATE plane (SPEC 10.48).  The mm axis on THIS plane is "
              "NOT established:")
        print("    mottle_measure.py uses PXM_REF = 337.0 px/m, itself only "
              "bracketed 330-344.")
    return out, mask, Y


def character(box=_BODY, path="ref_rear34.jpg", label="bus cream"):
    """WHICH KIND of texture -- with a DERIVED verdict, not a printed one.

    rev 19: `rear34_character` printed 'CHALKY SUN-FADE MOTTLE' as a constant
    string.  Handed a box of pure RED body paint it reported class purity
    0.0 %, every statistic nan, and still printed that verdict.  A conclusion
    that cannot fail is not a measurement.  This one is computed from the
    statistics and returns None when they do not support any verdict.
    """
    s = spectrum(box, path, label)
    if s is None:
        print("  VERDICT: None -- the patch could not support a measurement.")
        return None
    _, mask, Y = s
    from PIL import Image as _I
    u0, u1, v0, v1 = box
    lin = S2L(np.asarray(_I.open(path).convert("RGB"),
                         dtype=np.float64)[v0:v1, u0:u1] / 255.0)
    Ls, Cs = _lab(lin)
    print("-" * 74)
    print("CHARACTER -- fade vs dirt vs brush vs dents   (verdict is DERIVED)")
    print("  sigma   corr(dL*,dC*)   dL* rms   dC* rms   anisotropy v/u   skew")
    rows = []
    for sg in (2.0, 4.0, 8.0):
        hl = Ls - gblur(Ls, sg); hc = Cs - gblur(Cs, sg)
        if mask.sum() < 8:
            return None
        r = float(np.corrcoef(hl[mask], hc[mask])[0, 1])
        b = Y - gblur(Y, sg); k = int(3 * sg + 1)
        bb = b[k:-k, k:-k]; mm = mask[k:-k, k:-k]
        if mm.sum() < 8:
            print("  %5.1f      insufficient interior after %d px trim" % (sg, k))
            continue
        gx = np.diff(bb, axis=1); gy = np.diff(bb, axis=0)
        an = float(np.sqrt((gy[mm[:-1, :]] ** 2).mean())
                   / max(np.sqrt((gx[mm[:, :-1]] ** 2).mean()), 1e-12))
        x = (Y - gblur(Y, sg))[mask]
        sk = float(((x - x.mean()) ** 3).mean() / max(x.std() ** 3, 1e-12))
        dl, dc = float(hl[mask].std()), float(hc[mask].std())
        rows.append((sg, r, dl, dc, an, sk))
        print("  %5.1f      %+7.3f       %6.3f    %6.3f        %.3f       %+6.2f"
              % (sg, r, dl, dc, an, sk))
    if len(rows) < 2 or any(not np.isfinite(v) for row in rows for v in row):
        print("  VERDICT: None -- statistics are not finite. NOT a texture claim.")
        return None
    corr8 = rows[-1][1]; corr2 = rows[0][1]
    dl8, dc8, an8 = rows[-1][2], rows[-1][3], rows[-1][4]
    chroma_live = dc8 > 0.30 * dl8
    anti = corr8 < -0.20
    deepens = corr8 < corr2
    iso = 0.70 <= an8 <= 1.43
    print("  tests:  anti-correlated(<-0.20) %-5s  deepens-with-scale %-5s"
          % (anti, deepens))
    print("          chroma-structure-live(dC*>0.3 dL*) %-5s  isotropic(0.70-1.43) %-5s"
          % (chroma_live, iso))
    if anti and deepens and chroma_live:
        v = "CHALKY SUN-FADE MOTTLE (patches oxidised lighter AND less chromatic)"
    elif (not anti) and corr8 > 0.20 and chroma_live:
        v = "DIRT / SOILING (L* and C* fall together)"
    elif not chroma_live:
        v = "ACHROMATIC STRUCTURE -- brush, roller, dents or noise, NOT fade"
    else:
        v = None
    if v is None:
        print("  VERDICT: None -- the tests do not agree on any single mechanism.")
    else:
        print("  VERDICT: %s" % v)
        if not iso:
            print("  CAVEAT: anisotropy %.3f is OUTSIDE 0.70-1.43 -- directional." % an8)
    return v


# The entry point lives at the BOTTOM because `run()` calls `spectrum()` and
# `character()`, which are defined below it.  It sat above them from rev 56's
# first draft and raised NameError on the first invocation -- caught by
# running the file, which is the only way this class of defect is ever caught.
if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else None)
