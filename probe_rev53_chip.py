"""
probe_rev53_chip.py -- HOW BIG IS A CHIP IN A PHOTOGRAPH?

rev 53, brief sec.4 item 2.  LEDGER_rev52 sec.6.4 names the ceiling this probe
exists to close:

    "What is missing is a radius grounded in HOW BIG A REAL CHIP IS IN A
     PHOTOGRAPH -- a measurement nobody in this project has made."

WHAT THE RADIUS ACTUALLY IS, AND IT IS NOT A CHIP DIAMETER.  In `t1_mats.py`
the gate is `edge = 1 - dot(bevel_normal, true_normal)` -- see the line
`_dot.operation = 'DOT_PRODUCT'` -- and that is non-zero ONLY within about one
bevel radius of a fold.  So the Bevel radius is THE HALF-WIDTH OF THE WEAR BAND
ALONG AN EDGE.  Two quantities have to come out of a photograph before it can
be set from one:  (i) the width of the chipped band along a fold, which sets
the radius;  (ii) the size of one chip, which bounds (i) from below.

THE ANSWER THIS PROBE RETURNS IS NEITHER, AND THAT IS THE RESULT.  On every
cream window in the frames we hold that survives being painted and looked at,
the vehicle is NOT CHIPPED -- and the detection floor in arm C shows that is
not a resolution artefact, because the render's OWN chip population sits well
above the floor and would have been seen.

ARMS
  A  the estimator, CALIBRATED on LEDGER_rev52 sec.6.1's own two controls
  B  the frame's scale and PSF
  C  THE DETECTION FLOOR, every size against its OWN null control
  D  the frames, on windows PAINTED to probe_scratch/ before they yield a number
  E  the render, put through the PHOTOGRAPH'S OWN OPTICS so the two are
     comparable, plus the render's chip SIZE distribution against the floor

TWO INSTRUMENT DEFECTS THIS PROBE CAUGHT IN ITSELF, both by a control or a
painted window and NEITHER by reasoning:
  * arm C first used the window's raw high-pass STD (8.57 DN, outlier-driven)
    instead of its MAD (0.99 DN).  Its null control then read 8.117 % on PURE
    NOISE -- every "detection" in that pass was noise.
  * FIVE of the SIX windows first tried in arm D were contaminated: the menu
    card (read 12.0 % -- PRINTED TEXT counted as chips), the bulb-string
    shadow, the window chrome, the tail/wall highlight, and the bumper (on the
    white wall behind it).  Only the counter fascia survived on ref_side.jpg.
    The trap check MISSED the wall one because the check's own box covered the
    LEFT wall only.  A trap check is a window too.
"""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

OUTD = 'probe_scratch'; os.makedirs(OUTD, exist_ok=True)
def hdr(s): print("\n" + "=" * 74 + "\n  " + s + "\n" + "=" * 74)

MED_R, DARK_K = 9, 12.0
def dark_frac(imgL, mask):
    med = ndi.median_filter(imgL, size=2 * MED_R + 1)
    dk = (imgL < med - DARK_K) & mask
    return 100.0 * dk.sum() / max(1, mask.sum()), dk
def robust_noise(imgL, mask):
    hp = (imgL - ndi.median_filter(imgL, size=5))[mask]
    return float(1.4826 * np.median(np.abs(hp - np.median(hp))))

rng = np.random.default_rng(53)
S_PHOT, S_REND = 211.5, 271.2          # px/m; REF_MEASUREMENTS sec.8 / studio
MM_PX = 1000.0 / S_PHOT

# ===========================================================================
hdr("ARM A -- THE ESTIMATOR, ON LEDGER_rev52's OWN TWO CONTROLS")
c1 = np.full((220, 220), 205.0) + rng.normal(0, 0.5, (220, 220))
f1, _ = dark_frac(c1, np.ones_like(c1, bool))
c2 = np.full((220, 220), 205.0) + rng.normal(0, 0.5, (220, 220))
cm = np.zeros_like(c2, bool); yy, xx = np.mgrid[0:220, 0:220]
while cm.mean() < 0.0732:
    cy, cx = rng.integers(6, 214, 2); rr = rng.uniform(2.0, 3.4)
    cm |= ((yy - cy) ** 2 + (xx - cx) ** 2) < rr * rr
true2 = 100.0 * cm.mean(); c2[cm] -= 45.0
f2, _ = dark_frac(c2, np.ones_like(c2, bool))
print("  flat cream + 0.5 DN noise  -> %6.3f %%   record 0.00 %%" % f1)
print("  flat cream + known chips   -> %6.3f %%   true %5.2f %%   record 7.316 %%" % (f2, true2))
if not ((f1 < 0.05) and abs(f2 - true2) < 1.2):
    print("  ARM A: FAIL -- STOP"); sys.exit(1)
print("  ARM A: PASS")

# ===========================================================================
hdr("ARM B -- ref_side.jpg's SCALE AND PSF")
im = np.asarray(Image.open('ref_side.jpg').convert('RGB')).astype(np.float64)
H, W, _ = im.shape
L = im.mean(2); Rc, Gc, Bc = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (Rc > 110) & (Rc - Gc > 55) & (Rc - Bc > 45)
lab, n = ndi.label(red); hub = None
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 300: continue
    h, w = ys.max() - ys.min() + 1, xs.max() - xs.min() + 1
    if not (0.70 < w / float(h) < 1.45): continue
    if len(ys) / float(h * w) < 0.62 or ys.mean() < H * 0.60: continue
    if hub is None or len(ys) > hub[2]: hub = (xs.mean(), ys.mean(), len(ys))
print("  rear hubcap disc x=%.1f y=%.1f (n=%d)." % hub)
print("  THE FRONT HUB IS BEHIND THE LEANING MAN, so the wheelbase span is a")
print("  CONSISTENCY CHECK here, not an independent re-derivation.  Scale is the")
print("  record's %.1f px/m, which puts the front hub at x=%.1f.  STATED."
      % (S_PHOT, hub[0] - 2.400 * S_PHOT))
print("  => %.3f mm/px" % MM_PX)
sig = []
for x in range(690, 800):
    prof = L[432:448, x]
    if prof.max() - prof.min() < 60: continue
    t = ((prof - prof.min()) / (prof.max() - prof.min()))[::-1]
    if not (t[0] < 0.2 and t[-1] > 0.8): continue
    u = np.interp([0.10, 0.90], t, np.arange(len(t))); d = u[1] - u[0]
    if 0 < d < 10: sig.append(d / 2.563)
PSF = float(np.median(sig))
print("  PSF sigma %.3f px (n=%d cols, on the fascia bottom edge arm D paints)"
      % (PSF, len(sig)))
print("     FWHM %.2f px = %.1f mm" % (2.355 * PSF, 2.355 * PSF * MM_PX))

# ===========================================================================
hdr("ARM D-1 -- THE COUNTER FASCIA, TRACKED PER COLUMN AND PAINTED")
# NOT a fixed row band.  The fascia SLOPES; a fixed band crossed the gold
# nosing at both ends, and painting it is what showed that.  Each column is cut
# between the nosing's bottom and the red's top, inset 2 px each way.
gold = (Rc - Bc > 90); redb = (Rc - Gc > 45) & (Rc > 60) & (Gc < 90)
fascia = np.zeros(L.shape, bool); hts = []
for x in range(640, 905):
    cg = np.where(gold[400:432, x])[0]; cr = np.where(redb[425:460, x])[0]
    if len(cg) == 0 or len(cr) == 0: continue
    t, b = 400 + cg.max() + 2, 425 + cr.min() - 2
    if b - t < 6: continue
    fascia[t:b, x] = True; hts.append(b - t)
NOISE = robust_noise(L, fascia)
f_fascia, dk_f = dark_frac(L, fascia)
print("  %d columns, %d px, height %.1f px = %.0f mm (record ~94 mm -> the"
      % (len(hts), fascia.sum(), np.mean(hts), np.mean(hts) * MM_PX))
print("     window is on the right object), robust noise %.2f DN" % NOISE)
print("  DARK COVERAGE = %.3f %%  -- %d px, in %d blobs, of which %d are SINGLE"
      % (f_fascia, dk_f.sum(), ndi.label(dk_f)[1],
         sum(1 for i in range(1, ndi.label(dk_f)[1] + 1)
             if (ndi.label(dk_f)[0] == i).sum() == 1)))
print("     pixels, i.e. JPEG noise.  The record's figure is 0.00 %.")
ov = im.copy(); ov[fascia] = 0.45 * ov[fascia] + 0.55 * np.array([255, 0, 0])
Image.fromarray(ov.astype(np.uint8)).crop((600, 390, 960, 470)).resize(
    (360 * 4, 80 * 4), Image.NEAREST).save(OUTD + '/rev53_fascia_window.png')
print("  painted -> %s/rev53_fascia_window.png -- LOOKED AT: on cream, clear of" % OUTD)
print("     the nosing above and the red below.")

# ===========================================================================
hdr("ARM C -- THE DETECTION FLOOR, EACH SIZE AGAINST ITS OWN NULL")
print("  noise %.2f DN = the MAD of the painted window above.\n" % NOISE)
print("   chip dia   true cov    NULL      with chips   detected?")
SUP, N = 6, 160; floor_mm = None
for d_mm in (4, 6, 8, 10, 15, 20, 30, 40):
    d_hi = (d_mm / MM_PX) * SUP
    hi = np.full((N * SUP, N * SUP), 205.0); m = np.zeros_like(hi, bool)
    yy, xx = np.mgrid[0:N * SUP, 0:N * SUP]; tries = 0
    while m.mean() < 0.05 and tries < 6000:
        cy, cx = rng.integers(0, N * SUP, 2)
        m |= ((yy - cy) ** 2 + (xx - cx) ** 2) < (d_hi / 2.0) ** 2; tries += 1
    cov = 100.0 * m.mean(); hi[m] -= 45.0
    lo = ndi.gaussian_filter(hi, PSF * SUP)[SUP // 2::SUP, SUP // 2::SUP]
    lo = lo + rng.normal(0, NOISE, lo.shape)
    nul = np.full_like(lo, 205.0) + rng.normal(0, NOISE, lo.shape)
    fN, _ = dark_frac(nul, np.ones_like(nul, bool))
    fC, _ = dark_frac(lo, np.ones_like(lo, bool))
    det = fC > max(0.30, 5.0 * max(fN, 0.02))
    if det and floor_mm is None: floor_mm = d_mm
    print("   %4d mm    %5.2f %%   %7.3f %%    %7.3f %%      %s"
          % (d_mm, cov, fN, fC, "yes" if det else "NO"))
print("\n  DETECTION FLOOR = %d mm at 5 %% coverage." % floor_mm)
print("  Below the PSF FWHM (%.1f mm) because this estimator counts COVERAGE,"
      % (2.355 * PSF * MM_PX))
print("  not shape: blur spreads a chip but conserves its darkness.  SIZE is")
print("  resolved only above the FWHM; PRESENCE well below it.")

# ===========================================================================
hdr("ARM D-2 -- A SECOND FRAME, ref_rear34.jpg, INDEPENDENT OF THE FIRST")
im2 = np.asarray(Image.open('ref_rear34.jpg').convert('RGB')).astype(np.float64)
L2 = im2.mean(2); R2, G2, B2 = im2[:, :, 0], im2[:, :, 1], im2[:, :, 2]
cream2 = (L2 > 150) & (L2 < 250) & (R2 - B2 > 18) & (R2 - B2 < 75) \
         & (R2 - G2 > 4) & (R2 - G2 < 38)
cream2 = ndi.binary_opening(cream2, np.ones((3, 3)))
ov2 = im2.copy(); rows2 = []
for nm, (x0, x1, y0, y1) in {
        'tail cream below the nosing': (960, 1180, 495, 520),
        'counter fascia, mid':         (700, 900, 470, 500)}.items():
    m = np.zeros(L2.shape, bool); m[y0:y1, x0:x1] = True; m &= cream2
    m = ndi.binary_erosion(m, np.ones((3, 3)))
    f, _ = dark_frac(L2, m); rows2.append((nm, m.sum(), robust_noise(L2, m), f))
    ov2[m] = 0.45 * ov2[m] + 0.55 * np.array([0, 190, 255])
Image.fromarray(ov2.astype(np.uint8)).crop((650, 410, 1200, 540)).resize(
    (550 * 3, 130 * 3), Image.NEAREST).save(OUTD + '/rev53_rear34_windows.png')
print("  painted -> %s/rev53_rear34_windows.png\n" % OUTD)
print("   %-30s %7s %9s %9s" % ("window", "px", "noise", "dark %"))
for nm, px, nz, f in rows2: print("   %-30s %7d %9.2f %9.3f" % (nm, px, nz, f))
print("\n  NO SCALE IS PUBLISHED FOR THIS FRAME, so these are COVERAGE ONLY.")
print("  A size in mm would need a scale this probe has not established here.")

# ===========================================================================
hdr("ARM E -- THE RENDER, THROUGH THE PHOTOGRAPH'S OWN OPTICS")
CAND = [('r53base', 'Pointiness gate (the DEFAULT)'),
        ('r53bev',  'T1_EDGEBEVEL=1, radius GAPW/2 = 2.75 mm'),
        ('r53bev12','T1_EDGEBEVEL=1, T1_EDGERAD=12 mm')]
print("  The render is 271.2 px/m and the photograph 211.5, so a fixed 9 px")
print("  median radius is a DIFFERENT PHYSICAL SIZE in each.  Comparing the two")
print("  raw is an instrument mismatch.  Each render below is therefore blurred")
print("  by the MEASURED PSF, decimated to the photograph's mm/px and given the")
print("  photograph's noise BEFORE the same estimator reads it.\n")
print("   %-42s %9s %9s %11s" % ("render", "own px/m", "thru opt", "blob dia mm"))
for pfx, desc in CAND:
    p = 'out/%s_side.png' % pfx
    if not os.path.exists(p):
        print("   %-42s   -- not rendered --" % desc); continue
    r = np.asarray(Image.open(p).convert('RGB')).astype(np.float64)
    Lr = r.mean(2); Rr, Gr, Br = r[:, :, 0], r[:, :, 1], r[:, :, 2]
    gd = (Rr - Br > 40) & (Rr > 140); rd = (Rr - Gr > 45) & (Gr < 95)
    # A 2 px inset is NOT enough here, and PAINTING THE DARK PIXELS is what
    # showed it: on the Bevel render all 294 of them were the gold nosing's
    # soft shadow line at the left end and the tops of the four COUNTER
    # BRACKETS -- structural boundaries, not chips on the cream face.  So:
    # 4 px inset, and any column whose fascia is shorter than the median (a
    # bracket intruding from below) is dropped entirely.
    cand = {}
    for x in range(700, 1330):
        cg = np.where(gd[620:640, x])[0]; cr = np.where(rd[640:690, x])[0]
        if len(cg) == 0 or len(cr) == 0: continue
        t, b = 620 + cg.max() + 4, 640 + cr.min() - 4
        if b - t < 6: continue
        cand[x] = (t, b)
    hmed = np.median([b - t for t, b in cand.values()])
    # A ONE-SIDED height test dropped nothing, and the machine says why: a
    # bracket is CREAM, so the red detector finds red only BELOW it and the
    # column comes out TALLER (28-30 px) not shorter (17 px).  My test had the
    # SIGN BACKWARDS -- rule 35's shape exactly, a guard written against an
    # assumed geometry instead of the measured one.  Two-sided now.
    mr = np.zeros(Lr.shape, bool)
    for x, (t, b) in cand.items():
        if abs((b - t) - hmed) > 1.5: continue     # bracket / end column
        mr[t:b, x] = True
    f_own, dk = dark_frac(Lr, mr)
    lb, nb = ndi.label(dk)
    if nb:
        szs = np.array(ndi.sum(dk, lb, range(1, nb + 1)))
        eq = 2 * np.sqrt(szs / np.pi) * (1000.0 / S_REND)
        aw = float(np.sum(szs / szs.sum() * eq))
    else: aw = 0.0
    k = S_PHOT / S_REND
    Lb = ndi.gaussian_filter(Lr, PSF / k)
    nz = (int(Lr.shape[1] * k), int(Lr.shape[0] * k))
    Ld = np.asarray(Image.fromarray(Lb.astype(np.uint8)).resize(nz, Image.BILINEAR)).astype(float)
    md = np.asarray(Image.fromarray((mr * 255).astype(np.uint8)).resize(nz, Image.NEAREST)) > 127
    md = ndi.binary_erosion(md, np.ones((3, 3)))
    Ld = Ld + rng.normal(0, NOISE, Ld.shape)
    f_opt, _ = dark_frac(Ld, md)
    print("   %-42s %8.3f%% %8.3f%% %10.1f" % (desc, f_own, f_opt, aw))
print("   %-42s %8s  %8.3f%% %10s" % ("ref_side.jpg  THE PHOTOGRAPH", "--", f_fascia, "--"))

# ===========================================================================
hdr("ARM F -- THE WEAR-BAND PROFILE: DARKNESS vs DISTANCE FROM THE FOLD")
# ARM E's window insets 4 px from the fascia's folds, which at the render's
# 271.2 px/m is ~15 mm.  It therefore CANNOT SEE the edge band, and a 0.000 %
# there means "no chips more than 15 mm from a fold", NOT "no chips".  This arm
# measures the thing the Bevel radius actually sets: how dark the cream is as a
# function of DISTANCE FROM THE FOLD, in millimetres, on both sides.
def band_profile(Lx, gdx, rdx, xr, ytop, ymid, ybot, mmpx, nb=7, bw_mm=6.0):
    xr = list(xr)
    """Dark coverage in successive bands measured UP from the bottom fold."""
    bw = max(1, int(round(bw_mm / mmpx)))
    cand = {}
    for x in xr:
        cg = np.where(gdx[ytop:ymid, x])[0]; cr = np.where(rdx[ymid:ybot, x])[0]
        if len(cg) == 0 or len(cr) == 0: continue
        t, b = ytop + cg.max() + 2, ymid + cr.min()
        if b - t < 8: continue
        cand[x] = (t, b)
    if not cand: return None, 0
    hmed = np.median([b - t for t, b in cand.values()])
    # Drop bracket columns AND THEIR NEIGHBOURS.  Painting the 2 px edge band
    # showed the surviving dark pixels sitting on the BRACKET SHOULDERS -- the
    # ambient-occlusion shadow where the tab meets the fascia -- in the columns
    # immediately beside an excluded one.  Excluding a feature is not enough;
    # its shadow reaches further than it does.
    bad = np.zeros(max(xr) + 40, bool)
    for x, v in cand.items():
        if abs((v[1] - v[0]) - hmed) > 1.5: bad[x] = True
    bad = ndi.binary_dilation(bad, np.ones(17))
    cand = {x: v for x, v in cand.items()
            if abs((v[1] - v[0]) - hmed) <= 1.5 and not bad[x]}
    med = ndi.median_filter(Lx, size=2 * MED_R + 1)
    out = []
    for k in range(nb):
        m = np.zeros(Lx.shape, bool)
        for x, (t, b) in cand.items():
            lo, hi = b - (k + 1) * bw, b - k * bw
            if lo <= t: continue
            m[lo:hi, x] = True
        if m.sum() < 60: out.append((k * bw_mm, (k + 1) * bw_mm, m.sum(), float('nan'))); continue
        d = (Lx < med - DARK_K) & m
        out.append((k * bw_mm, (k + 1) * bw_mm, int(m.sum()),
                    100.0 * d.sum() / m.sum()))
    return out, len(cand)

print("  Bands are %g mm wide, measured UP from the fascia's BOTTOM fold (the"
      % 6.0)
print("  cream/red edge).  Same estimator, each frame at its OWN scale.\n")
print("   %-40s %s" % ("", "  ".join("%4.0f-%2.0f" % (a, b)
      for a, b, _, _ in band_profile(L, gold, redb, range(640, 905), 400, 425, 460, MM_PX)[0])))
prof_p, npc = band_profile(L, gold, redb, range(640, 905), 400, 425, 460, MM_PX)
print("   %-40s %s" % ("ref_side.jpg  THE PHOTOGRAPH (n=%d col)" % npc,
      "  ".join("%7.2f" % f for _, _, _, f in prof_p)))
for pfx, desc in CAND:
    p = 'out/%s_side.png' % pfx
    if not os.path.exists(p): continue
    r = np.asarray(Image.open(p).convert('RGB')).astype(np.float64)
    Lr = r.mean(2); Rr, Gr, Br = r[:, :, 0], r[:, :, 1], r[:, :, 2]
    gd = (Rr - Br > 40) & (Rr > 140); rd = (Rr - Gr > 45) & (Gr < 95)
    pr, nc = band_profile(Lr, gd, rd, range(700, 1330), 620, 640, 690, 1000.0 / S_REND)
    print("   %-40s %s" % (desc[:40], "  ".join("%7.2f" % f for _, _, _, f in pr)))
print("\n  READ THIS COLUMN-WISE.  If a gate puts wear AT THE EDGE, its leftmost")
print("  band is the hottest and the profile falls away.  A gate that saturates")
print("  a flat face is FLAT across the bands.  The photograph is the target.")
