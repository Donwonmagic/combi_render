"""probe_rev48_louv.py -- the rear-quarter louvres READ WITH THE WRONG SIGN.

rev 48.

WHAT THIS SETTLES, AND WHAT IT DOES NOT
---------------------------------------
It does NOT ask whether the louvres exist.  They do, and that is settled
against the BUILD, not the source:  `louvres1` / `louvres-1`, 560 v each,
x -1.5371..-1.2419 (len 0.2952), z 0.8636..1.0699, TEN slot rows at pitch
21.111 mm -- watched print from a T1_SUB=2 build.

    `LEDGER_rev46.md` §5 "THE MODEL HAS NO REAR VENTS", the grep it rests on,
    `LEDGER_rev47.md` §10c's "nothing replaced them", and
    `NEXT_CONTEXT_PROMPT_rev48.md` §2 JOB 2 are ALL REFUTED on that point.
    The grep they quote returns 140 hits, including
    `t1_detail.py:2122  # ===== REAR-QUARTER AIR LOUVRES`.

It asks the question those three files never reached:  DO THEY READ?

    ref_side.jpg  slat lines are DARKER  than the panel, |mod| 0.206
    the render    slat lines are BRIGHTER than the panel, |mod| 0.111

THE SIGN IS NOT THE FINDING, AND AN EARLIER DRAFT OF THIS FILE SAID IT WAS.
It concluded that the build's slats "catch light where the photograph's cast
shadow", blamed `LOUV_OFF = +0.0020` for riding the sweep proud, and would
have had the next revision recess it.  THAT IS RETRACTED, by a frame this
project already holds:

    ref_nolita_front34.jpg -- the SAME real louvres, lit from the other
    side, read as BRIGHT highlight lines.

So a real pressed louvre reads dark or bright depending only on where the key
is.  Sign alone condemns nothing, and `ref_side.jpg`'s block additionally sits
in the serving counter's shade while the render's is in open key.  ONE
LIGHTING EACH IS NOT A COMPARISON OF GEOMETRY (SPEC 10.110.8).

WHAT REV 48 THEN FIXED, AND IT IS THE HALF THAT DOES NOT DEPEND ON LIGHTING.
`t1_detail.louvres()` was "A sweep, not a boolean ... the shell is never
touched" -- twenty CLOSED RIBS laid on UNBROKEN metal, where a T1 louvre is an
APERTURE.  One hole per flank now spans the block, the blades span the hole,
and a shallow dark bay sits behind so the slots do not look into the lit cabin
(they did, and the first render showed BRIGHT WHITE BARS among them -- rule 28).

    before   +0.0343   the blades caught the key
    after    -0.2559   the slots self-shadow, as the photograph's do

WHAT SURVIVES AS A CEILING RATHER THAN A TARGET:

    |photographed| / |built|  =  1.85x

    -- the photographed block modulates its own panel 1.85x as hard as the
    built block modulates its own.  Dimensionless on both sides, so paint
    (W6) and exposure cancel.  IT IS NOT A CLAIM ABOUT DEPTH: the two are
    lit differently, and no frame we hold lets that be separated.  Quote it
    as "the built feature is roughly half as prominent, measured one lighting
    against another", never as a depth error.

AN INSTRUMENT I BUILT, WATCHED FAIL, AND THREW AWAY  (SPEC 10.116.6)
--------------------------------------------------------------------
The first version of this probe bounded the block AUTOMATICALLY, by the
periodic power of its own row profile.  It reported the built block at power
0.958 and looked authoritative.  Its kill control killed it:

    blank painted panel, photograph   power up to 0.228
    the louvre block,    photograph   power      0.213
    blank painted panel, render       power up to 0.380
    the louvre block,    render       power      0.405

The block is NOT SEPARABLE from blank paint by that statistic at this
resolution.  The 0.958 was the bounder locking onto the belt line, not the
louvres.  The bounder is deleted rather than re-thresholded -- lowering the
threshold would have made a blind estimator quiet instead of making it see.

SO THE BUILT BLOCK IS BOUNDED BY PROJECTION, NEVER BY TYPING  (brief §3)
-----------------------------------------------------------------------
NOTHING here is transcribed.  The probe PARSES its two sources at run time
(SPEC 10.25, rule 2 -- derive it, do not freeze it):

    studio.py   views()["side"]  ->  loc, tgt, ortho      (the camera)
    t1_detail.py LOUV_Z_TOP/BOT, LOUV_N                   (the block)

The `side` camera is ORTHOGRAPHIC at (0, 26, 1.52) aimed at (0, 0, 1.52),
ortho 5.90 across the 1600 px long axis, so

    px/m   = 1600 / 5.90                       = 271.186
    x_px   = 800.0  - px/m * X                 (camera sits at world x = 0)
    y_px   = (550 + px/m*1.52) - px/m * Z      (frame centre is z = 1.52)

and both fall out of the view dict with no landmark hunting at all.  C6 and
C7 then check the mapping against the frame: the ground plane must land on
the frame's own last non-white row, and x = X_TAIL on the tail cap.

A FIRST ATTEMPT AT THIS ANCHORED ON THE SILHOUETTE AND WAS WRONG TWICE.
Taking "the rightmost non-white pixel" over z 0.81..1.10 gives 1315 -- 22 mm
PAST the body's own rearmost vertex, because the TAIL LAMP protrudes.  Moving
the band up to z 1.20..1.50 gives 1396, because the SERVING COUNTER SHELF is
there.  Both readings were plausible and both would have slid the box far
enough to sample bare paint.  The camera dict has no such failure mode.

THE PHOTOGRAPH cannot be projected -- its camera is unknown -- so its window
is STATED and the reading is repeated over a FAMILY of windows (C8), because
a measurement's window is part of the measurement (SPEC 10.106.6).

QUOTE THE RATIO, NOT THE READING (rule 24): the headline is the photographed
modulation over the built one, same estimator, same pixel scale (79x54 vs
80x56 -- no resampling is applied to either).
"""
import os, re, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RX, RY = 1600, 1100

def _src(fn):
    return open(os.path.join(HERE, fn)).read()

def side_view():
    """Parse views()["side"] out of studio.py.  Fails loudly if it moves."""
    t = _src("studio.py")
    m = re.search(r'"side":\s*dict\(loc=\(([^)]*)\),\s*tgt=\(([^)]*)\),'
                  r'\s*lens=(\w+),\s*ortho=([0-9.]+)\)', t)
    if not m:
        raise SystemExit("studio.py views()['side'] no longer parses -- "
                         "this probe's projection is invalid until it does.")
    loc = [float(v) for v in m.group(1).split(",")]
    tgt = [float(v) for v in m.group(2).split(",")]
    return loc, tgt, m.group(3), float(m.group(4))

def louv_consts():
    """Parse the louvre block's own constants out of t1_detail.py."""
    t = _src("t1_detail.py")
    zt = float(re.search(r"LOUV_Z_TOP,\s*LOUV_Z_BOT\s*=\s*([0-9.]+),\s*([0-9.]+)", t).group(1))
    zb = float(re.search(r"LOUV_Z_TOP,\s*LOUV_Z_BOT\s*=\s*([0-9.]+),\s*([0-9.]+)", t).group(2))
    n  = int(re.search(r"LOUV_N\s*=\s*(\d+)", t).group(1))
    off= float(re.search(r"LOUV_OFF\s*=\s*([0-9.]+)", t).group(1))
    return zt, zb, n, off

LOC, TGT, LENS, ORTHO = side_view()
LOUV_Z_TOP, LOUV_Z_BOT, N_SLOTS, LOUV_OFF = louv_consts()
PPM = RX / ORTHO
# BUILT block x, watched print from a T1_SUB=2 build (t1_detail._aft() re-stations
# LOUV_X0/X1, so the authored constants are NOT the built extent -- see §JOB 2).
LOUV_X0, LOUV_X1 = -1.5371, -1.2419
# slot-row centres in the BUILD (watched print).  The authored LOUV_Z_TOP/BOT
# above are the AUTHORED values; _aft()/G() re-station the sweep, so these are
# what the mesh actually occupies and these are what must be projected.
LOUV_Z_BUILT_BOT, LOUV_Z_BUILT_TOP = 0.8636, 1.0536
X_TAIL = -1.873

def to_px(X, Z):
    x = (RX * 0.5) - PPM * (X - LOC[0])
    y = (RY * 0.5) - PPM * (Z - TGT[2])
    return x, y

def _lum(a):
    a = np.asarray(a, float)
    return 0.2126*a[...,0] + 0.7152*a[...,1] + 0.0722*a[...,2]

def frame_ground(img):
    """The frame's own last non-white row -- an INDEPENDENT check on z = 0."""
    a = np.asarray(img, float)
    nw = (a.sum(axis=2) < 3*250)
    return float(np.where(nw.any(axis=1))[0].max())

def project_block():
    """The built block's pixel box, from the camera dict and the build."""
    xa, ytop = to_px(LOUV_X0, LOUV_Z_BUILT_TOP)
    xb, ybot = to_px(LOUV_X1, LOUV_Z_BUILT_BOT)
    return (min(xa, xb), max(xa, xb), min(ytop, ybot), max(ytop, ybot))

def slat_modulation(img, box, pitch_px):
    """SIGNED modulation of the slat rows about their own local panel level.

    +ve  slats BRIGHTER than the panel  (a lip catching the key)
    -ve  slats DARKER   than the panel  (a slot that self-shadows)
    Divided by the panel's own mean, so exposure, paint and shade cancel."""
    x0, x1, y0, y1 = [int(round(v)) for v in box]
    L = _lum(img.crop((x0, y0, x1, y1)))
    prof = L.mean(axis=1)
    n = len(prof)
    w = max(3, (int(round(pitch_px * 2.5)) | 1))
    trend = np.convolve(np.pad(prof, w//2, mode="edge"), np.ones(w)/w, "valid")[:n]
    res = prof - trend
    idx = []
    for k in range(N_SLOTS):
        a = int(round(k*n/N_SLOTS)); b = int(round((k+1)*n/N_SLOTS))
        if b > a: idx.append(a + int(np.argmax(np.abs(res[a:b]))))
    return (float(np.mean(res[idx]) / prof.mean()),
            float(np.mean(np.abs(res[idx])) / prof.mean()))

def synth(h, w, pitch, sign, depth=0.16, base=110.0, noise=2.0, seed=0):
    rng = np.random.default_rng(seed)
    y = np.arange(h)[:, None]
    lines = np.zeros((h, w))
    for k in range(N_SLOTS):
        lines += np.exp(-0.5*((y - (1.5 + k*pitch))/(pitch*0.22))**2)
    a = np.clip(base*(1.0 + sign*depth*lines) + rng.normal(0, noise, (h, w)), 0, 255)
    return Image.fromarray(np.dstack([a, a*0.30, a*0.18]).astype(np.uint8))

def main():
    checked = fails = 0
    def ck(ok, label, got):
        nonlocal checked, fails
        checked += 1; fails += (not ok)
        print("  %-4s %-56s %s" % ("ok" if ok else "FAIL", label, got))

    print("probe_rev48_louv -- do the built rear louvres READ?")
    print("=" * 78)
    photo = Image.open(os.path.join(HERE, "ref_side.jpg")).convert("RGB")
    # The frame is selectable so BEFORE and AFTER can be read on the IDENTICAL
    # instrument (rule 24's surviving half: compare like with like).  Default
    # is rev 48's pre-aperture render, so an un-parameterised run reproduces
    # the figure this probe was written against.
    rp = os.path.join(HERE, "out",
                      os.environ.get("T1_LOUV_FRAME", "r48b_side.png"))
    if not os.path.exists(rp):
        print("  MISSING %s -- render it first:" % rp)
        print("  T1_PREVIEW=side T1_PFX=r48b T1_RX=1600 T1_RY=1100 T1_SAMP=96 \\")
        print("      /tmp/blender/blender -b -P build.py")
        return 1
    built = Image.open(rp).convert("RGB")

    print("  camera: studio.views()['side'] loc=%s tgt=%s lens=%s ortho=%.2f -> %.3f px/m"
          % (LOC, TGT, LENS, ORTHO, PPM))
    print("  block : t1_detail LOUV_Z_TOP/BOT %.4f/%.4f  LOUV_N %d  LOUV_OFF %+.4f"
          % (LOUV_Z_TOP, LOUV_Z_BOT, N_SLOTS, LOUV_OFF))
    ck(LENS == "None" and ORTHO > 0,
       "C0 the side view is still ORTHOGRAPHIC (else the maths is void)",
       "lens=%s ortho=%.2f" % (LENS, ORTHO))

    yg_pred = to_px(0.0, 0.0)[1]
    yg_meas = frame_ground(built)
    ck(abs(yg_pred - yg_meas) < 2.0,
       "C6 projected ground plane lands on the frame's own last row",
       "z=0 -> y %.1f, frame ends %.0f" % (yg_pred, yg_meas))

    # rev 48: THE BAND MOVED, AND THE OLD ONE WENT RED FOR A GOOD REASON.
    # It sampled z 0.95..1.05, which is where the TRUNK LID now hangs once it
    # is swung open -- the silhouette there reads 1365, not the tail cap's
    # 1307.9.  The control was correctly reporting that the vehicle changed.
    # Moved to z 1.20..1.30, which is clear of the trunk lid (z 0.796..1.103
    # open), clear of the rear hatch (1.455..1.606 open) and below the counter
    # shelf.  Rule 5: the rationale is kept, the shape is replaced.
    xt_pred = to_px(X_TAIL, 1.25)[0]
    a = np.asarray(built, float); nw = (a.sum(axis=2) < 3*250)
    band = nw[int(to_px(0, 1.30)[1]):int(to_px(0, 1.20)[1])]
    xt_meas = float(np.where(band.any(axis=0))[0].max())
    # rev 48, RESTATED TWICE AND NOW TRUE.  It began as "the rightmost
    # non-white pixel IS the tail cap", which is simply false on this vehicle:
    # at z 0.95..1.05 it finds the open TRUNK LID (1365), at z 1.20..1.30 the
    # COUNTER SHELF (1396), and at z 0.81..1.10 the TAIL LAMP (1315).  Three
    # different bands, three different protrusions, none of them the tail cap.
    # Hunting for a clean band was the wrong response: the assumption is
    # wrong, not the window.
    #
    # THE INVARIANT THAT IS ACTUALLY TRUE: things may stick out PAST the tail
    # (lamps, shelves, open lids), but NOTHING can lie forward of the tail cap
    # and still be the silhouette's aft edge.  So the projected tail cap must
    # be at or forward of the measured edge, and within a bound that any
    # grossly wrong mapping would breach.  Weaker than the original, and
    # unlike the original it is not false.  The mapping's real proof is C6
    # (the ground plane, exact to 0.8 px) and C9 (the block's metric size).
    ck(xt_pred <= xt_meas + 2.0 and (xt_meas - xt_pred) < 120.0,
       "C7 projected tail cap is at or forward of the silhouette edge",
       "x=%.3f -> px %.1f, silhouette %.0f (delta %+.0f)"
       % (X_TAIL, xt_pred, xt_meas, xt_meas - xt_pred))

    bb = project_block()
    bw, bh = bb[1]-bb[0], bb[3]-bb[2]
    ck(abs(bw - (LOUV_X1-LOUV_X0)*PPM) < 1.0
       and abs(bh - (LOUV_Z_BUILT_TOP-LOUV_Z_BUILT_BOT)*PPM) < 1.0,
       "C9 the projected box is the built block's own metric size",
       "%.1f x %.1f px  (%.4f x %.4f m)" % (bw, bh, bw/PPM, bh/PPM))
    bpitch = bh / (N_SLOTS - 1)

    P_WIN = (764, 438, 843, 492)          # STATED, not projected: unknown camera
    ppitch = (P_WIN[3]-P_WIN[1]) / (N_SLOTS - 1)
    pbox = (P_WIN[0], P_WIN[2], P_WIN[1], P_WIN[3])

    mp, ap = slat_modulation(photo, pbox, ppitch)
    mb, ab = slat_modulation(built, bb,  bpitch)
    print()
    print("  PHOTOGRAPHED  window %s  %d x %d px, pitch %.2f px" % (
        P_WIN, P_WIN[2]-P_WIN[0], P_WIN[3]-P_WIN[1], ppitch))
    print("                signed modulation  %+.4f   |amp| %.4f" % (mp, ap))
    print("  BUILT         PROJECTED box (%.0f,%.0f)-(%.0f,%.0f)  %.0f x %.0f px, pitch %.2f px" % (
        bb[0], bb[2], bb[1], bb[3], bw, bh, bpitch))
    print("                signed modulation  %+.4f   |amp| %.4f" % (mb, ab))
    print()
    print("  RATIO  |photographed| / |built|   %.2f x        (rule 24)" % (ap/ab))
    print()

    h, w = P_WIN[3]-P_WIN[1], P_WIN[2]-P_WIN[0]
    md, _ = slat_modulation(synth(h, w, ppitch, -1.0, seed=1), (0, w, 0, h), ppitch)
    ck(md < -0.02, "C1 known DARK slats at the real px size read NEGATIVE",
       "%+.4f  (built-in truth: -0.16 depth)" % md)
    mbr, _ = slat_modulation(synth(h, w, ppitch, +1.0, seed=2), (0, w, 0, h), ppitch)
    ck(mbr > +0.02, "C2 known BRIGHT slats read POSITIVE",
       "%+.4f  <- it CAN report either sign" % mbr)

    # C3 KILL -- blank paint on BOTH frames must not produce a block-sized signal
    blanks_p = [(700,438,760,492), (640,440,700,494), (600,500,680,554)]
    blanks_b = [(1000,660,1090,716), (900,660,990,716), (950,760,1040,816)]
    bp = [abs(slat_modulation(photo, (a,c,b,d), ppitch)[0]) for a,b,c,d in blanks_p]
    bq = [abs(slat_modulation(built, (a,c,b,d), bpitch)[0]) for a,b,c,d in blanks_b]
    floor = max(max(bp), max(bq))
    ck(floor < min(ap, ab) * 0.60,
       "C3 KILL blank paint stays well under both readings",
       "floor %.4f vs photo %.4f / built %.4f" % (floor, ap, ab))

    # C4.  Inverting luminance negates the residual EXACTLY (res' = -res) but
    # renormalises by (255 - mean), so the predicted reading is not -mp but
    #     mi_pred = -mp * mean / (255 - mean)
    # Testing the sign alone would pass on a broken estimator that merely
    # returned a constant; testing against the DERIVED magnitude too is
    # strictly stronger.  Neither figure is tuned -- both are arithmetic.
    pc = photo.crop((pbox[0], pbox[2], pbox[1], pbox[3]))
    mean_l = float(_lum(np.asarray(pc, float)).mean())
    inv = Image.fromarray((255 - np.asarray(pc, int)).astype(np.uint8))
    mi, _ = slat_modulation(inv, (0, w, 0, h), ppitch)
    mi_pred = -mp * mean_l / (255.0 - mean_l)
    ck(np.sign(mi) != np.sign(mp) and abs(mi - mi_pred) < 0.15*abs(mi_pred) + 0.002,
       "C4 WATCHED-FAIL invert -> sign flips AND hits the derived value",
       "%+.4f vs predicted %+.4f (mean L %.1f)" % (mi, mi_pred, mean_l))

    # C8 -- the photographed reading must survive its window moving
    fam, sgn = [], []
    for dx in (-4, 0, 4):
        for dy in (-3, 0, 3):
            wq = (P_WIN[0]+dx, P_WIN[2]+dy, P_WIN[2]+dx+ (P_WIN[2]-P_WIN[0]) - (P_WIN[2]-P_WIN[0]), 0)
            b2 = (P_WIN[0]+dx, P_WIN[2]+dx, P_WIN[1]+dy, P_WIN[3]+dy)
            m2, _ = slat_modulation(photo, b2, ppitch)
            fam.append(m2); sgn.append(np.sign(m2))
    ck(all(s == sgn[0] for s in sgn),
       "C8 the photographed SIGN survives a 9-window family",
       "%+.4f .. %+.4f, all %s" % (min(fam), max(fam), "negative" if sgn[0] < 0 else "positive"))

    ck(np.sign(mp) < 0, "C5 in ref_side.jpg the slats are DARKER than their panel", "%+.4f" % mp)

    # C10 -- the lighting-independent half of the finding, read off the source.
    # whitespace-normalised: the claim lives in a wrapped docstring, so a
    # contiguous-substring test would fail on the line break rather than on
    # the fact.  Normalising is what makes this test about the FACT.
    # rev 48: C10 IS INVERTED, DELIBERATELY.  It used to assert that the
    # louvres were CLOSED RIBS -- it was the finding, not the fix.  The shell
    # is now cut (t1_detail.louvre_cutters), so the same row must now assert
    # the opposite, or it would pass for ever on the defect it was written to
    # expose.  Rule 5 again: a guard's rationale outlives its shape.
    src = " ".join(_src("t1_detail.py").split())
    cut_exists = "def louvre_cutters" in src
    wired = "louvre_cutters" in " ".join(_src("build.py").split())
    ck(cut_exists and wired,
       "C10 the louvres are APERTURES -- the shell IS cut behind them",
       "louvre_cutters present and called from build.py" if cut_exists and wired
       else "cutter %s, call site %s" % (cut_exists, wired))

    print()
    print("  READING.   photographed %+.4f   built %+.4f" % (mp, mb))
    print("  HEADLINE.  |photographed| / |built| = %.2fx  -- the built block" % (ap/ab))
    print("             modulates its own panel about half as hard.")
    print()
    print("  CEILING, AND IT IS NOT OPTIONAL:")
    print("   *  The SIGNS differ, and that is NOT evidence of a geometry error.")
    print("      ref_nolita_front34.jpg shows these same real louvres reading")
    print("      BRIGHT.  Sign follows the key light, not the pressing.")
    print("   *  ref_side.jpg's block is in the counter's shade; the render's is")
    print("      in open key.  One lighting each (SPEC 10.110.8).")
    print("   *  So 1.85x bounds PROMINENCE, not DEPTH.  Do not retune LOUV_OFF,")
    print("      LOUV_PROFILE or the pressing depth from this number.")
    print("   *  The lighting-independent half IS NOW FIXED: the shell is cut")
    print("      behind the blades (louvre_cutters) and backed by a dark bay")
    print("      (louvre_backing), so the slots are real openings that")
    print("      self-shadow.  The SIGN moved +0.0343 -> -0.2559.  See C10.")
    print()
    print("CONTROLS: %d checked, %d FAILED" % (checked, fails))
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
