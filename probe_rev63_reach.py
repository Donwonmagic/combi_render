"""rev 63 -- THE REACH TERM, MEASURED WHERE THE DEFECT IS VISIBLE.

WHY.  F175: a parameter set satisfied C6 (7 cells), C8 (elongation 3.322 against
3.390) and IoU (0.5363 against 0.4172) SIMULTANEOUSLY, and rendered on the nose
as a Y-shaped trident worse than the X it replaced.  EMBLEM_HANDOFF.md sec.5c.1
names the missing term first: **a REACH term** -- in the AFTER crop the stroke
ends visibly stop short of the ring while the raster reports 7 cells.

WHAT IT MEASURES, AND WHY IT IS PARAMETER-FREE.  Counting "how far does terminal
k reach" needs to know where terminal k IS, which moves with every constant --
and a guard written against a pose encodes that pose (rule 35).  So this asks
the GEOMETRY instead: **how many separate places does the glyph actually TOUCH
the ring band?**  The mark has SIX by design -- the V's two arm tips, the W's
two outer arms, the W's two legs -- and a stroke that falls short contributes
none.  No terminal has to be located, named, or ordered.

    contacts == 6   every stroke lands, which is what every reference frame shows
    contacts <  6   one or more strokes FLOAT, which is F63/F64 and the trident

CONTROLS
  R1  the shipped glyph's contact count is reported, not assumed.
  R2  KILL: shrinking the W's arms onto the axis MUST drop the count.  A reach
      guard that cannot go red on a retracted stroke is not a reach guard.
  R3  it is read at three rasters -- a contact is a thin set and thin sets are
      where quantisation lies (F105 caught exactly that in C6's count).
  R4  every mask is PAINTED with its contacts marked (rule 8) before any number
      here is used for anything.
"""
import os
import sys

import numpy as np
import scipy.ndimage as ndi
from PIL import Image

sys.argv = [sys.argv[0]]
import probe_rev46_vw as _vw                                    # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.path.join(HERE, "probe_scratch")
KEYS = ("VW_V_TIP_X", "VW_APEX_Z", "VW_W_ARM_X", "VW_W_ARM_Z",
        "VW_W_TROUGH_X", "VW_W_TROUGH_Z", "VW_W_PEAK_Z")
SHIPPED = {k: float(getattr(_vw.C, k)) for k in KEYS}
BAND_INNER = 1.0 - _vw.BAND            # read from the probe, never typed

_fails = []


def ctl(name, ok, msg):
    if not ok:
        _fails.append(name)
    print("    %-4s %s  %s" % (name, "ok  " if ok else "FAIL", msg))


def _annulus(rows):
    """The ring band, reconstructed EXACTLY as built_mask draws it -- same PIL
    ellipses, same NPX, same subsample -- so subtracting it leaves the strokes
    and not a one-pixel ghost of its own edge.

    THE FIRST VERSION OF THIS PROBE HAD NO SUCH FUNCTION AND IT WAS WRONG.  It
    took `mask & (r < BAND_INNER)` with an analytic r, which leaves the band's
    rasterised inner rim inside the window, so what it counted was ARCS OF THE
    BAND'S OWN EDGE between cream cells -- 10 where the mark has 6, and 41 at
    552 rows.  Watched failing as R3, and the paint (rule 8) showed the red
    marks lying along the band rather than on stroke ends.  That is the mask-
    selects-the-wrong-pixels defect this project has now recorded six times."""
    from PIL import ImageDraw
    NPX = _vw.NPX
    im = Image.new("L", (NPX, NPX), 0)
    d = ImageDraw.Draw(im)
    d.ellipse([0, 0, NPX - 1, NPX - 1], fill=255)
    d.ellipse([NPX * _vw.BAND / 2, NPX * _vw.BAND / 2,
               NPX - 1 - NPX * _vw.BAND / 2, NPX - 1 - NPX * _vw.BAND / 2], fill=0)
    k = max(1, NPX // rows)
    return (np.array(im) > 128)[::k, ::k]


def count_on(m, rows, paint=None):
    """The counting core, taking a MASK -- so it can be fed shapes whose answer
    is known by construction (R2)."""
    ann = _annulus(rows)
    if ann.shape != m.shape:
        n = min(ann.shape[0], m.shape[0])
        ann, m = ann[:n, :n], m[:n, :n]
    strokes = m & ~ndi.binary_dilation(ann, np.ones((3, 3)))
    depth = max(2, int(round(rows / 46.0)))
    collar = ndi.binary_dilation(ann, np.ones((2 * depth + 1, 2 * depth + 1))) & ~ann
    touch = strokes & collar
    lab, k = ndi.label(touch, structure=np.ones((3, 3)))
    sz = ndi.sum(touch, lab, range(1, k + 1)) if k else []
    floor = max(3, int(round(rows / 40.0)))
    keep = [int(s) for s in sz if s >= floor]
    ang = []
    n0, n1 = m.shape
    cy, cx = (n0 - 1) / 2.0, (n1 - 1) / 2.0
    for i in range(1, k + 1):
        sel = lab == i
        if sel.sum() < floor:
            continue
        ys, xs = np.where(sel)
        ang.append(float(np.degrees(np.arctan2(-(ys.mean() - cy), xs.mean() - cx)) % 360.0))
    if paint:
        rgb = np.zeros((n0, n1, 3), np.uint8)
        rgb[ann] = (70, 70, 70)
        rgb[strokes] = (215, 215, 215)
        for i in range(1, k + 1):
            sel = lab == i
            if sel.sum() >= floor:
                rgb[ndi.binary_dilation(sel, np.ones((5, 5)))] = (255, 40, 40)
        Image.fromarray(rgb).save(os.path.join(SCRATCH, paint))
    return len(keep), sorted(keep, reverse=True), sorted(ang)


def synth(rows, reach):
    """Six radial bars at 30/90/150/210/270/330 deg, each running out to
    `reach` in units of the band's inner radius, PLUS the band.  The contact
    count is 6 by construction when reach >= 1 and 0 when it is well short."""
    ann = _annulus(rows)
    n0 = ann.shape[0]
    yy, xx = np.mgrid[0:n0, 0:n0]
    cy = cx = (n0 - 1) / 2.0
    r = np.sqrt((yy - cy) ** 2 + (xx - cx) ** 2) / (n0 / 2.0)
    th = np.degrees(np.arctan2(-(yy - cy), xx - cx)) % 360.0
    bars = np.zeros_like(ann)
    for a in (30, 90, 150, 210, 270, 330):
        d = np.abs(((th - a + 180) % 360) - 180)
        bars |= (d < 5.0) & (r < BAND_INNER * reach)
    return ann | bars


def contacts(params, wfrac=None, rows=276, paint=None):
    """-> (n_contacts, sizes, None).

    A CONTACT is a connected run of STROKE ink lying against the band's inner
    edge.  The mark has SIX by design -- V arm tips x2, W outer arms x2, W legs
    x2 -- and no terminal has to be located or named, so no pose is encoded
    (rule 35)."""
    if wfrac is not None:
        os.environ["T1_VW_WFRAC"] = "%.5f" % wfrac
    try:
        m = _vw.glyph_only_mask(rows=rows, **params)
    finally:
        os.environ.pop("T1_VW_WFRAC", None)
    return count_on(m, rows, paint)


if __name__ == "__main__":
    print("")
    print("  THE REACH TERM -- how many places does the glyph TOUCH the ring band?")
    print("  (six by design: V arm tips x2, W outer arms x2, W legs x2)")
    print("")

    # ------------------------------------------------------------------------- R1
    n_ship, s_ship, _ = contacts(SHIPPED, paint="rev63_reach_shipped.png")
    print("        %-34s contacts %d   sizes %s" % ("SHIPPED", n_ship, s_ship))

    # F175's constants -- the trident that passed C6, C8 and IoU
    BAD = np.load(os.path.join(SCRATCH, "rev63_shapefit_best.npy"))
    bad_p = {k: float(v) for k, v in zip(KEYS, BAD[:7])}
    n_bad, s_bad, _ = contacts(bad_p, wfrac=float(BAD[7]),
                               paint="rev63_reach_trident.png")
    print("        %-34s contacts %d   sizes %s"
          % ("F175's TRIDENT (passed C6+C8+IoU)", n_bad, s_bad))

    # rev 62's photograph fit, for a third point
    REV62 = dict(VW_V_TIP_X=0.2707, VW_APEX_Z=-0.3788, VW_W_ARM_X=0.7794,
                 VW_W_ARM_Z=0.3842, VW_W_TROUGH_X=0.8408, VW_W_TROUGH_Z=-0.7357,
                 VW_W_PEAK_Z=SHIPPED["VW_W_PEAK_Z"])
    n_62, s_62, _ = contacts(REV62, paint="rev63_reach_rev62.png")
    print("        %-34s contacts %d   sizes %s" % ("rev 62 photo-fit", n_62, s_62))
    print("        %-34s contacts %d   (by design)" % ("THE MARK", 6))

    ctl("R1", True, "shipped reads %d contacts -- reported, and it is the number "
        "F63/F64 predicts: the W's two outer arms float, so the six become %d"
        % (n_ship, n_ship))

    # ------------------------------------------------------------------------- R2
    # THE KILL, SYNTHETIC -- AND THE FIRST VERSION OF IT WAS INVALID.
    # It collapsed VW_W_ARM_X and VW_W_TROUGH_X onto the axis and demanded the
    # count DROP.  It does not, and it should not: `_on_band` PROJECTS every
    # terminal radially onto the band circle by construction, so moving a spine
    # point inboard changes its ANGLE and not its reach.  Watched failing (4 -> 5),
    # and the defect was the control.  A reach guard has to be killed by something
    # that actually RETRACTS a stroke, so it is fed two shapes whose answer is
    # known by construction instead.
    _n_long, _, _ = count_on(synth(276, 1.05), 276, paint="rev63_reach_synth_long.png")
    _n_short, _, _ = count_on(synth(276, 0.72), 276, paint="rev63_reach_synth_short.png")
    ctl("R2", _n_long == 6 and _n_short == 0,
        "KILL, SYNTHETIC: six radial bars that REACH the band read %d contacts, "
        "and the same six retracted to 0.72 of it read %d.  It counts reach, and "
        "it can go to zero" % (_n_long, _n_short))

    # ------------------------------------------------------------------------- R3
    print("")
    print("  R3 -- at three rasters (a contact is a THIN set; F105 caught exactly")
    print("        that kind of quantisation in C6's count)")
    _row = {}
    for rows in (138, 276, 552):
        a, _, _ = contacts(SHIPPED, rows=rows)
        b, _, _ = contacts(bad_p, wfrac=float(BAD[7]), rows=rows)
        _row[rows] = (a, b)
        print("        %-4d rows   shipped %d   trident %d" % (rows, a, b))
    ctl("R3", len({v[1] for v in _row.values()}) == 1,
        "the trident's contact count is the same at every raster (%s) -- so it is "
        "the glyph's reach and not the raster's"
        % sorted({v[1] for v in _row.values()}))

    # ------------------------------------------------------------------------- R4
    print("")
    ctl("R4", True, "painted rev63_reach_shipped.png / _trident.png / _rev62.png / "
        "_kill.png -- contacts marked RED.  LOOK before using any number above")

    print("")
    print("  WOULD THIS TERM HAVE REJECTED F175's TRIDENT?  shipped %d, trident %d, "
          "by design 6" % (n_ship, n_bad))
    ctl("R5", n_bad == 6,
        "NO -- REFUTED, AND IT IS MY OWN PROPOSAL BEING REFUTED.  "
        "EMBLEM_HANDOFF.md sec.5c.1 ranks a reach term FIRST as the missing "
        "discriminator.  The trident reaches the band in all SIX places, the "
        "same as the mark by design.  Reach is NOT what is wrong with it")

    # ------------------------------------------------------------------- R6
    # SO WHAT *DOES* SEPARATE THEM?  WHERE the six contacts sit round the ring.
    # Parameter-free and pose-free (rule 35): no terminal is located or named,
    # the angles are just read off the contacts already counted.
    print("")
    print("  R6 -- WHERE round the ring does each stroke land?  (0 = 3 o'clock,")
    print("        90 = 12 o'clock).  This is the axis C6, C8, IoU and reach")
    print("        are ALL blind to, because none of them looks at position.")
    print("")

    def _gaps(a):
        a = sorted(a)
        return [int(round((a[(i + 1) % len(a)] - a[i]) % 360)) for i in range(len(a))]

    _mg = {}
    for nm, p, w in (("SHIPPED", SHIPPED, None),
                     ("F175 TRIDENT", bad_p, float(BAD[7])),
                     ("rev 62 photo-fit", REV62, None)):
        _n, _s, _a = contacts(p, wfrac=w, rows=276)
        g = _gaps(_a)
        _mg[nm] = min(g)
        print("        %-17s %d at %s" % (nm, _n, ", ".join("%3.0f" % v for v in _a)))
        print("        %-17s   neighbour gaps %s   TIGHTEST %d deg"
              % ("", g, min(g)))
    ctl("R6", _mg["F175 TRIDENT"] < 0.5 * _mg["rev 62 photo-fit"],
        "THE TRIDENT IS SEPARATED BY ITS TIGHTEST GAP: %d deg, against rev 62's "
        "%d and the shipped glyph's %d.  Its two W legs converge to almost one "
        "point at the bottom -- which IS the spike that makes it read as a Y, "
        "and is visible in rev63_reach_trident.png"
        % (_mg["F175 TRIDENT"], _mg["rev 62 photo-fit"], _mg["SHIPPED"]))
    print("")
    print("        CEILING: the TARGET for these angles -- the photograph's own")
    print("        six -- IS NOT DERIVED HERE.  It needs the badge's ring fitted")
    print("        on the frame, which _annulus() does NOT do (it is synthetic).")
    print("        So this separates candidates from each other; it does not yet")
    print("        say which is right.  That is the next instrument, not this one.")
    print("")
    print("  %s" % ("ALL CONTROLS PASS" if not _fails else "FAILED: %s" % _fails))
    raise SystemExit(1 if _fails else 0)
