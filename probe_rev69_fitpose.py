# probe_rev69_fitpose.py -- rev 69.  THE EMBLEM, COMPARED POSE-FREE.  F236.
#
# THE PROBLEM THIS SOLVES, AND IT HAS BLOCKED THE EMBLEM FOR EIGHT REVISIONS.
#
# Every emblem statistic in this tree is measured on an OBLIQUE photograph and
# compared against a HEAD-ON raster.  F184 says so explicitly -- *"their targets
# carry the viewing angle -- a pure shear spans both"* -- and it is why C6's
# count and C8's elongation have targets nobody trusts, and why F138's angles
# were never reproducible.
#
# REV 69 TRIED TO UN-PROJECT THE PHOTOGRAPH AND THAT IS ILL-POSED.  The roundel
# is a circle, so its image ellipse gives an affine that maps it back -- but
# that affine is not unique (an unknown in-plane rotation survives) and, worse,
# a PLANE under a perspective camera maps by a HOMOGRAPHY, which an affine
# cannot undo.  MEASURED, with the mark's own mirror symmetry as the judge:
#
#     BUILT mask, symmetric BY CONSTRUCTION   best mirror IoU 0.9932 at 90.0 deg
#     ref_nolita_front34, affine-corrected                0.6128 at 141.0 deg
#     ref_workshop,       affine-corrected                0.6247 at 138.0 deg
#
# Two different vehicles, cameras and scenes agree on the leftover rotation to
# 3 deg, so the failure is systematic, not noise -- and 0.61 against a control
# of 0.99 says the affine leaves the mark a long way from its own symmetry.
# FITTING ANY ANGLE TARGET TAKEN THROUGH THAT CORRECTION WOULD BAKE THE POSE
# INTO THE GEOMETRY.  That is F184's trap, and rev 69 walked up to it.
#
# SO THE PROBLEM IS INVERTED.  Do not un-project the photograph.  PROJECT THE
# MODEL and fit the pose out as a nuisance parameter: search the homography that
# best maps the built mark onto the photographed one, and the residual that
# SURVIVES the best pose is the SHAPE difference.  Well-posed, needs no camera,
# no focal length and no un-squash, and it is the comparison this project has
# never had.
#
# READ THIS PROBE'S OWN SUMMARY LINE, NEVER ITS EXIT CODE (rule 9).
import os
import sys

import numpy as np
from PIL import Image, ImageDraw
import scipy.ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "probe_scratch")
N = 220                      # working raster for the model side


def unit_mask(rows=N, **over):
    """The built mark -- glyph AND ring -- on a unit disc, head-on."""
    import probe_rev46_vw as P
    return P.built_mask(rows=rows, **over)


def photo_mark(path, box=None, dark=True):
    """The photographed mark as a mask, plus its own bounding box.

    No pose correction of any kind is applied here.  That is the point."""
    a = np.asarray(Image.open(os.path.join(HERE, path)).convert("RGB")).astype(float)
    if box is not None:
        a = a[box[1]:box[3], box[0]:box[2]]
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    thr = 0.5 * (np.percentile(lum, 10) + np.percentile(lum, 90))
    m = lum < thr if dark else lum > thr
    lab, k = ndi.label(m)
    if k == 0:
        return None
    sz = ndi.sum(m, lab, range(1, k + 1))
    m = lab == int(np.argmax(sz)) + 1
    f = ndi.binary_fill_holes(m)
    ys, xs = np.nonzero(f)
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def warp(src, H, shape):
    """Sample `src` through homography H into an output of `shape`.

    H maps OUTPUT (photograph) coordinates back to SOURCE (model) coordinates,
    both normalised to [-1, 1] on the mark's own bounding box, so the search is
    scale-free and the two rasters need not be the same size."""
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w]
    u = (xx - (w - 1) / 2.0) / ((w - 1) / 2.0)
    v = -(yy - (h - 1) / 2.0) / ((h - 1) / 2.0)
    d = H[2, 0] * u + H[2, 1] * v + H[2, 2]
    d = np.where(np.abs(d) < 1e-9, 1e-9, d)
    su = (H[0, 0] * u + H[0, 1] * v + H[0, 2]) / d
    sv = (H[1, 0] * u + H[1, 1] * v + H[1, 2]) / d
    sh, sw = src.shape
    ix = np.round((su * ((sw - 1) / 2.0)) + (sw - 1) / 2.0).astype(int)
    iy = np.round(((-sv) * ((sh - 1) / 2.0)) + (sh - 1) / 2.0).astype(int)
    ok = (ix >= 0) & (ix < sw) & (iy >= 0) & (iy < sh)
    out = np.zeros(shape, bool)
    out[ok] = src[np.clip(iy, 0, sh - 1), np.clip(ix, 0, sw - 1)][ok]
    return out


# --------------------------------------------------------------- rev 71, F246
# TRANSLATION IS SEARCHED NOW, AND THE START SET COVERS THE WHOLE CIRCLE.
#
# THE PREMISE THE OLD DOCSTRING ASSERTED WAS FALSE.  It said "translation is
# not searched -- both masks are already centred on their own bounding boxes".
# `photo_mark` DOES bbox-crop every real target, but a projected disc's bbox
# centre is NOT its centre, so the two masks are NOT co-centred and the search
# could not reach the offset.  P1's control hid this because `synth` is the raw
# `warp` output, centred on the OUTPUT FRAME -- so the CONTROL was framed one
# way and every MEASUREMENT another (rule 42, and it is the whole of F246).
#
# WATCHED, on the SAME model against the SAME known view, bbox-framed as
# photo_mark frames it:
#     6-param, 6 rotation starts (the old search)      0.4988
#     8-param, 6 rotation starts                       0.5403
#     8-param, FULL CIRCLE every 20 deg                0.9703   <- PASSES
#     analytic H = inv(Hk) @ the crop's own affine     1.000000
# So the collapse was TWO defects compounding: no translation, AND a start set
# covering only half the circle.  Rev 71's first cut called translation
# "necessary and not sufficient" and shipped the probe REFUSING; a dispatched
# adversary measured the full-circle start set and refuted that.  It is
# necessary AND sufficient, and the repair is here rather than deferred.
#
# T1_FITPOSE_LEGACY=1 restores the rev-69 search EXACTLY (6 params, 6 starts)
# so the two can be scored from one tree and this is ablatable (rule 36).
_LEGACY = os.environ.get("T1_FITPOSE_LEGACY") == "1"


def make_H(p):
    """Homography from 8 parameters: rotation, two scales, shear, two
    perspective terms, and TWO TRANSLATIONS.  Six under T1_FITPOSE_LEGACY=1."""
    if len(p) == 6:
        rot, sx, sy, sh, px, py = p
        tx = ty = 0.0
    else:
        rot, sx, sy, sh, px, py, tx, ty = p
    c, s = np.cos(rot), np.sin(rot)
    R = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])
    S = np.array([[sx, sh, tx], [0.0, sy, ty], [0.0, 0.0, 1.0]])
    P = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [px, py, 1.0]])
    return R @ S @ P


def iou(a, b):
    u = (a | b).sum()
    return float((a & b).sum()) / u if u else 0.0


def fit(src, dst, rounds=7):
    """Best IoU of `src` warped onto `dst`, over the homography.  Greedy
    coordinate descent from an identity-ish start, multi-start on rotation
    because the mark has a near-180-deg ambiguity and a wrong basin is a real
    risk (the affine route landed in one at 141 deg)."""
    best = (-1.0, None)
    # THE START SET COVERS THE FULL CIRCLE (rev 71, F246).  The old set stopped
    # at 150 deg, which is why the bbox-framed control landed in a bad basin at
    # 0.5403 and was misread as "translation is not sufficient".
    _starts = [0, 30, 60, 90, 120, 150] if _LEGACY else list(range(0, 360, 20))
    # AND THE Y-SCALE IS SEEDED TOO (rev 71, second cut).  With one y-seed the
    # bbox-framed control passed at FIT_R 0.84 (0.9703) and COLLAPSED to 0.7004
    # at 0.86 -- a 2.4 % geometry change flipping the control, which is basin
    # fragility and not shape.  P1b caught it on rev 71's own shipped change
    # (rule 44).  Three y-seeds: 0.7004 -> 0.9146, and 36 rotations -> 0.9314.
    _ys = [1.0] if _LEGACY else [0.6, 1.0, 1.5]
    _n = 6 if _LEGACY else 8
    _seeds = [(r, y) for r in np.radians(_starts) for y in _ys]
    for rot0, ys0 in _seeds:
        p = [rot0, 1.0, ys0, 0.0, 0.0, 0.0] + ([] if _LEGACY else [0.0, 0.0])
        cur = iou(warp(src, make_H(p), dst.shape), dst)
        step = [0.20, 0.20, 0.20, 0.15, 0.15, 0.15, 0.15, 0.15][:_n]
        for _ in range(rounds):
            for i in range(_n):
                moved = True
                while moved:
                    moved = False
                    for d in (+step[i], -step[i]):
                        q = list(p)
                        q[i] += d
                        v = iou(warp(src, make_H(q), dst.shape), dst)
                        if v > cur + 1e-5:
                            cur, p = v, q
                            moved = True
                            break
            step = [t * 0.55 for t in step]
        if cur > best[0]:
            best = (cur, list(p))
    return best


# THE FRAMES.  `ref_workshop.jpg` IS THE TRACE'S OWN SOURCE -- vw_pressing.py's
# outline was traced off it -- so it CANNOT adjudicate between the constant
# spine and the trace (rule 6: two sides of a comparison must be independently
# obtained).  `IMG_2073.jpeg` is the GREEN vehicle, a different camera and a
# different pose, and rule 11 permits it: the roundel is the factory chrome
# PRESSING, which is geometry and transfers; only its colour is artwork (F141).
# It is the emblem's SECOND frame and this project had never used it.
FRAMES = (
    ("ref_nolita_front34.jpg", "ref_nolita_front34.jpg", (153, 192, 194, 261), False),
    ("ref_workshop.jpg  TRACE SOURCE", "ref_workshop.jpg", (262, 492, 352, 600), True),
    # RE-CUT AT REV 71.  The old (288,542)-(352,640) discards ~14 % of the
    # mark's ink (2527 on-px against 2926) and was never painted.  Re-cutting
    # probe_rev71_emblem.py ALONE and leaving this clipped is exactly the trap
    # the brief warns about, and rev 71's first cut committed it.
    ("IMG_2073.jpeg  INDEPENDENT", "IMG_2073.jpeg", (283, 537, 357, 662), True),
)


def regions(src):
    """The mark's own band and interior, as GEOMETRY on the unit disc -- not a
    threshold on either image.  Returns (band, interior)."""
    import probe_rev46_vw as P
    h, w = src.shape
    yy, xx = np.mgrid[0:h, 0:w]
    u = (xx - (w - 1) / 2.0) / ((w - 1) / 2.0)
    v = -(yy - (h - 1) / 2.0) / ((h - 1) / 2.0)
    r = np.hypot(u, v)
    return (r <= 1.0) & (r >= 1.0 - P.BAND), r < 1.0 - P.BAND


def _traced_scores():
    """Score the FACTORY-TRACE construction on every frame, in a FRESH process.

    T1_VW_TRACED is read at t1_core import time, so it cannot be toggled in
    this one.  Returns {tag: IoU} or None if the child said nothing."""
    import subprocess
    code = ("import sys; sys.path.insert(0, __HERE__)\n"
            "import os; os.environ['T1_VW_TRACED'] = '1'\n"
            "import probe_rev69_fitpose as F\n"
            "src = F.unit_mask()\n"
            "for tag, path, box, dark in F.FRAMES:\n"
            "    d = F.photo_mark(path, box, dark)\n"
            "    if d is None: continue\n"
            "    v, p = F.fit(src, d)\n"
            "    if not (0.3 < p[1] < 3.0 and 0.3 < p[2] < 3.0): continue\n"
            "    print('TRACED\\t' + tag + '\\t%.6f' % v)\n"
            ).replace("__HERE__", repr(HERE))
    try:
        out = subprocess.run([sys.executable, "-c", code], capture_output=True,
                             text=True, timeout=900).stdout
    except Exception:
        return None
    got = {}
    for ln in out.splitlines():
        if ln.startswith("TRACED\t"):
            _, t, v = ln.split("\t")
            got[t] = float(v)
    return got or None


def main():
    checks, fails = [], []

    def ck(name, ok, detail):
        checks.append((name, ok, detail))
        if not ok:
            fails.append(name)

    src = unit_mask()

    # ---- CONTROL: the model against ITSELF through a known homography.  If the
    # search cannot recover a mark it was given exactly, no number below means
    # anything (prove the proxy on a known answer first).
    Hk = make_H([np.radians(37.0), 1.0, 0.62, 0.18, 0.10, -0.06])
    synth = warp(src, np.linalg.inv(Hk), (N, N))
    v_ctl, _p = fit(src, synth)
    ck("P1 CONTROL -- the search recovers the model from a KNOWN oblique view of "
       "itself", v_ctl > 0.90,
       "best IoU %.4f against a synthetic view at 37 deg rotation, 0.62 "
       "foreshortening, shear 0.18 and real perspective. Below ~0.90 the search "
       "is the limit, not the shape.  *** QUOTE P1b's CEILING, NOT THIS ONE: this "
       "control is framed UNCROPPED and every real measurement below is "
       "bbox-cropped, so P1b -- 0.9703 -- is the ceiling the residuals should "
       "be read against (F246) ***" % v_ctl)

    # ---- P1b, NEW AT REV 71.  THE CONTROL MUST BE FRAMED THE WAY THE
    # MEASUREMENT IS FRAMED, AND P1 IS NOT.  F246.
    #
    # `photo_mark` ends every real target with
    #     ys, xs = np.nonzero(f);  return m[ys.min():ys.max()+1, xs.min():xs.max()+1]
    # i.e. EVERY PHOTOGRAPH IS CROPPED TO ITS OWN BOUNDING BOX.  P1's `synth` is
    # not: it is the raw output of `warp`, centred on the OUTPUT FRAME.  And
    # `fit` searches NO TRANSLATION -- its own docstring asserts "both masks are
    # already centred on their own bounding boxes", which is true of `synth`'s
    # frame and FALSE of a bbox crop, because a projected disc's bbox centre is
    # not its centre.
    #
    # SO THE CONTROL IS EASIER THAN THE MEASUREMENT IT CERTIFIES, AND THE GAP
    # BETWEEN THEM IS NOT ALL SHAPE.  Cropped exactly as photo_mark crops,
    # the SAME search on the SAME model against a KNOWN view of ITSELF falls
    # from 0.9882 to 0.4988 -- BELOW the 0.7345 the real mark scores.  A control
    # that scores worse than its specimen is not a ceiling (rule 42).
    ys_, xs_ = np.nonzero(synth)
    synth_bb = synth[ys_.min():ys_.max() + 1, xs_.min():xs_.max() + 1]
    v_ctl_bb, _pbb = fit(src, synth_bb)
    ck("P1b CONTROL, FRAMED THE WAY EVERY REAL TARGET IS FRAMED -- photo_mark "
       "bbox-crops the photograph, so the control must be bbox-cropped too",
       v_ctl_bb > 0.90,
       "the SAME search, the SAME model, the SAME known view -- cropped to its "
       "own bounding box as photo_mark crops every frame: IoU %.4f, against "
       "%.4f uncropped.  THIS ROW READ 0.4988 BEFORE REV 71's REPAIR, BELOW the "
       "0.7345 the specimen scored -- a control losing to its own specimen "
       "(rule 42).  TWO defects compounded: `make_H` had no translation terms, "
       "and the start set covered only half the circle.  Both are fixed; "
       "T1_FITPOSE_LEGACY=1 restores the rev-69 search exactly and drives this "
       "row back to 0.4988, which is its KILL (F246)"
       % (v_ctl_bb, v_ctl))

    # ---- THE LEGACY KILL.  rev 71: the repair above must be WATCHED being the
    # thing that fixed P1b, not asserted.  T1_FITPOSE_LEGACY=1 restores the
    # rev-69 search and this row's own number collapses.
    if not _LEGACY:
        print("  P1b's KILL: run `T1_FITPOSE_LEGACY=1 python3 probe_rev69_fitpose.py`")
        print("      -- the rev-69 search, 6 params and half the circle, drives")
        print("      the same control to 0.4988 and P1b RED (F246).")

    rows = []
    for tag, path, box, dark in FRAMES:
        dst = photo_mark(path, box, dark)
        if dst is None:
            print("  %-24s NO MARK FOUND -- nothing measured" % tag)
            continue
        v, p = fit(src, dst)
        # A NEGATIVE OR ABSURD SCALE MEANS THE SEARCH FELL INTO A BAD BASIN AND
        # THE NUMBER IS NOT A SHAPE RESIDUAL.  Refuse it rather than report it
        # (rule 37).  ref_nolita_front34 does this: 41 x 69 px, and its mark is
        # BRIGHT-on-dark where the workshop's is dark-on-bright, so its polarity
        # and its resolution both work against the fit.
        if not (0.3 < abs(p[1]) < 3.0 and 0.3 < abs(p[2]) < 3.0
                and p[1] > 0 and p[2] > 0):
            print("  %-24s REFUSED -- the pose search landed at scales "
                  "%.2f/%.2f, which is not a view of this mark. NOT a shape "
                  "residual, not scored." % (tag, p[1], p[2]))
            continue
        rows.append((tag, v, p, dst))
        print("  %-24s best pose IoU %.4f   (rot %+6.1f deg, scales %.2f/%.2f, "
              "shear %+.2f, persp %+.2f/%+.2f)"
              % (tag, v, np.degrees(p[0]), p[1], p[2], p[3], p[4], p[5]))

    if rows:
        best = max(r[1] for r in rows)
        ck("P2 THE BUILT MARK MATCHES THE PHOTOGRAPHED ONE UNDER ITS OWN BEST "
           "POSE", best >= 0.85,
           "best IoU over the frames is %.4f, against the control's %.4f. This "
           "is the SHAPE residual with the viewing angle FITTED OUT -- the "
           "comparison F184 says the count and the elongation cannot make"
           % (best, v_ctl))
        # paint the best one
        tag, v, p, dst = max(rows, key=lambda r: r[1])
        w = warp(src, make_H(p), dst.shape)
        ov = np.zeros(dst.shape + (3,), np.uint8)
        ov[..., 0] = np.where(dst, 235, 250)
        ov[..., 1] = np.where(w, 60, 250) * np.where(dst, 1, 1)
        ov[..., 2] = np.where(w, 60, 250)
        ov[dst & w] = [70, 70, 70]
        ov[dst & ~w] = [235, 60, 60]
        ov[~dst & w] = [60, 120, 235]
        im = Image.fromarray(ov)
        S = max(1, 460 // max(im.width, im.height))
        im = im.resize((im.width * S, im.height * S), Image.NEAREST)
        ImageDraw.Draw(im).text((5, 4), "%s  IoU %.3f  grey=agree red=photo-only "
                                "blue=model-only" % (tag, v), fill=(0, 0, 0))
        im.save(os.path.join(SCRATCH, "rev69_fitpose.png"))
        print("  painted -> probe_scratch/rev69_fitpose.png")

        # ---- P3: WHERE THE MISS LIVES.  The band and the interior are the
        # mark's own geometry, warped through the SAME best pose, so this is a
        # partition of the residual, not a second measurement.  PAINTED to
        # probe_scratch/rev69_fitpose_regions.png before any number is read
        # off it (rule 8).
        band, inner = regions(src)
        Rb, Ri = warp(band, make_H(p), dst.shape), warp(inner, make_H(p), dst.shape)

        def part(R):
            ag = (dst & w & R).sum()
            po = (dst & ~w & R).sum()
            mo = (~dst & w & R).sum()
            un = ag + po + mo
            return (float(ag) / un if un else 0.0), int(po), int(mo)

        vb, pob, mob = part(Rb)
        vi, poi, moi = part(Ri)
        rp = np.full(dst.shape + (3,), 250, np.uint8)
        rp[dst & w] = [70, 70, 70]
        rp[dst & ~w] = [235, 60, 60]
        rp[~dst & w] = [60, 120, 235]
        rp[Rb & ~(dst | w)] = [250, 235, 180]
        ri = Image.fromarray(rp)
        S2 = max(1, 520 // max(ri.size))
        ri = ri.resize((ri.width * S2, ri.height * S2), Image.NEAREST)
        ImageDraw.Draw(ri).text((5, 4), "band IoU %.3f  interior IoU %.3f  "
                                "red=photo blue=model" % (vb, vi), fill=(0, 0, 0))
        ri.save(os.path.join(SCRATCH, "rev69_fitpose_regions.png"))
        ck("P3 THE MISS IS IN THE GLYPH, NOT THE RING", vb > vi,
           "band IoU %.4f against interior IoU %.4f on %s. photo-only/model-only "
           "inside the ring is %d/%d -- NEAR BALANCED, so the ink AMOUNT is right "
           "and the ARRANGEMENT is wrong (F235, now pose-free). Painted to "
           "probe_scratch/rev69_fitpose_regions.png" % (vb, vi, tag, poi, moi))

        # ---- P4: THE TRACE, SCORED ON A FRAME IT WAS NOT TRACED FROM.
        # vw_pressing.py's outline was traced off ref_workshop.jpg, so scoring
        # it there compares a thing with its own source (rule 6).  F183 refuted
        # the trace by RENDERING it; that refutation inherits its instrument
        # (rule 46), and F184 says the count and the elongation cannot make this
        # comparison at all -- so it is re-scored here, pose-free, on BOTH
        # frames.  THE ROW GOES RED IF THE TRACE EVER WINS INDEPENDENTLY, which
        # is the finding that would put it back on the table.
        tr = _traced_scores()
        if tr is None:
            print("  P4 NOT RUN -- the traced subprocess did not report. NOT a "
                  "result either way (rule 37)")
        else:
            here = {t: vv for t, vv, _pp, _dd in
                    [(r[0], r[1], r[2], r[3]) for r in rows]}
            src_f, ind_f = "ref_workshop.jpg  TRACE SOURCE", "IMG_2073.jpeg  INDEPENDENT"
            if src_f in here and ind_f in here and src_f in tr and ind_f in tr:
                d_src = tr[src_f] - here[src_f]
                d_ind = tr[ind_f] - here[ind_f]
                ck("P4 THE TRACE'S ADVANTAGE DOES NOT SURVIVE OFF ITS OWN SOURCE "
                   "FRAME -- T1_VW_TRACED STAYS OFF (F183, F237)", d_ind <= 0.0,
                   "traced minus shipped is %+.4f on ref_workshop (the frame it "
                   "was TRACED FROM: %.4f vs %.4f) and %+.4f on IMG_2073, a "
                   "different vehicle, camera and pose (%.4f vs %.4f). An "
                   "improvement that lives only on its own source is OVERFIT. "
                   "If this row goes RED the trace has become the better "
                   "construction and F183 needs re-opening"
                   % (d_src, tr[src_f], here[src_f], d_ind, tr[ind_f], here[ind_f]))
            else:
                print("  P4 NOT RUN -- a frame was refused on one side or the "
                      "other, so there is nothing to compare (rule 37)")

    print("=" * 78)
    print("  probe_rev69_fitpose -- THE EMBLEM, POSE FITTED OUT (F236)")
    print("=" * 78)
    for name, ok, detail in checks:
        print("  [%s] %s\n        %s" % ("PASS" if ok else "FAIL", name, detail))
    print()
    print("  CEILING.  A homography is exact for a PLANE.  The mark is not quite "
          "planar --\n  it stands proud of the nose and the nose is curved -- so "
          "a few percent of any\n  residual is relief, not shape.  And the search "
          "is greedy from six rotation\n  starts; P1 bounds what it can recover. "
          " This says HOW FAR the built mark is\n  from the photographed one with "
          "pose removed. It does not say WHICH stroke.")
    print()
    print("  %d checked, %d FAILED%s"
          % (len(checks), len(fails), ("  --  " + fails[0][:56]) if fails else ""))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
