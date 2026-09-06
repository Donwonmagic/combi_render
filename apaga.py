#!/usr/bin/env python3
"""apaga.py -- APAGA LA LUZ, the children's line's SECOND object.  Rev 79.

WHAT THIS IS AND WHOSE DECISION IT WAS
--------------------------------------
A die-cut glow-vinyl sticker.  `CONCEPT_ROUND_rev77.md` ranks it FIRST on the
adversarial audit of all 75 concepts; two independent critics named it the best
in the round and one wrote "buy it".  The OWNER bought it at rev 79 (F362) and
ordered the one thing its two authors left unresolved drawn BOTH WAYS: whether
the 118 festoon lamps glow, or stay in daylight ink so they visibly do not.

THE CONCEPT'S SPINE, VERIFIED IN THE ASSET AND NOT TRANSCRIBED
--------------------------------------------------------------
`grep -c "emit=("` over the four geometry modules returns 0 / 0 / 1 / 0.  The
single hit is `gal_tube` -- the galley work strip, emit=(1.000,0.918,0.790) at
GAL_LUM 3.04.  ONE emissive material in a 229-object vehicle.  The party lights
are dark and the work light is on, and the model has believed that for 77
revisions without anyone drawing it.

⚠⚠ AND THE MEASUREMENT THAT CHANGED THE OBJECT, MADE BEFORE ANY INK WAS SPENT.
The concept says to draw the emitter.  THE EMITTER CANNOT BE SEEN.  `gal_tube`
is ZERO pixels on BOTH captures -- 0 of 566208 art px at az 72, 0 of 561033 at
az 90 -- because the strip is under the roof header and a waist-height serving
hatch does not show it.  What IS visible through the apertures is the ROOM IT
LIGHTS: gal_cream 2.400 %, glass 2.988 %, gal_steel 1.752 %, gal_menucard
1.070 %, gal_white 1.007 %, and nine more (all MEASURED, printed every run).
So the glow layer is NOT the lamp.  It is what the lamp lands on.  That is a
better drawing than the one specified and it is the asset's fact, not a
preference -- but it IS a departure from the concept body, and it is declared
here, on the sheet, and in F362 rather than absorbed silently (rule 13).

⚠ The concept's published "FIRST STEP: ~$0, one A4 sheet and an evening" is the
VINYL EXTINCTION TEST.  It does NOT cover this drawing, which needs a capture
that did not exist until rev 79.  Do not quote the one as the cost of the other.

WHAT IS AUTHORED HERE AND WHAT IS MEASURED
------------------------------------------
MEASURED: every mask, every area, every percentage, the scale, the stroke
count -- all off the `side` capture through the material index.
AUTHORED: the palette, the glow ink, the night ground, the simplification
floors, the panel layout.  F346's ruling is exactly this split -- the model is
asked only WHERE things are and an authored palette decides what each prints
in -- and F361 froze the model to make it the standing method.  Every authored
constant is printed on the sheet, because rev 78 learned that reporting them at
run time only is not the same as labelling them (its own §8 item 9).

Run:  python3 apaga.py --tag side          # needs the side capture
      python3 apaga.py --selftest
"""
import os, sys, json, argparse

ROOT = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(ROOT, "probe_scratch", "sticker")
DES = os.path.join(ROOT, "design_out")

# ------------------------------------------------------------- AUTHORED
# Every constant below is a CHOICE.  None is a measurement.  A different
# context would choose differently and get a different sticker (rev 78's
# lesson, stated rather than discovered again).
DENOM        = 20.325     # the concept's own scale: 4.065 m / 20.325 = 200 mm
GLOW_INK     = (166, 255, 176)   # strontium aluminate green, AUTHORED
GLOW_DIM     = (104, 190, 120)   # the second glow step, AUTHORED
NIGHT_GROUND = (17, 18, 22)      # the dark panel's ground, AUTHORED
DAY_BODY     = (196,  58,  48)   # daylight body ink, AUTHORED
DAY_CREAM    = (232, 223, 200)   # daylight cream, AUTHORED
DAY_DARK     = ( 44,  40,  38)   # daylight shadow/neutral, AUTHORED
DAY_LAMP     = (228, 214, 176)   # unlit festoon lamp in daylight ink, AUTHORED
LINE_INK     = ( 26,  22,  20)
STOCK        = (255, 255, 255)
SIMPLIFY_MM  = 0.16       # RDP epsilon, AUTHORED
LINE_MIN_MM  = 0.65       # drop line crumbs shorter than this, AUTHORED
# AUTHORED: measured albedo family -> daylight ink, for materials the palette
# does not assign BY NAME.  `T1_paint` is the one that matters and it is the
# body.  The family itself is MEASURED (`classify()` off the albedo); only the
# ink each family prints in is authored.
FAM_INK = {"red": DAY_BODY, "neutral_light": DAY_CREAM,
           "neutral_dark": DAY_DARK, "neutral_mid": (150, 148, 148),
           "gold": (239, 194, 69)}
MIN_AREA_MM2 = 0.30       # drop specks below this, AUTHORED
PANEL_GAP_MM = 9.0        # AUTHORED
VOID_FRAC    = 0.55       # AUTHORED: a stroke spending more than this share of
                          # its length over the galley is MODEL detail, not
                          # drawing.  Same figure sticker.py uses, and it is a
                          # CHOICE in both places, not a measurement.

# MEASURED-BY-NAME: the galley materials, i.e. everything the one emitter
# lights that a viewer can actually see through the apertures.  This list is
# the material-index prefix `gal_` plus `glass`, and it is FILTERED AT RUN TIME
# to those actually on screen -- a name that renders zero pixels is reported
# and dropped, never drawn as though it were there.
GALLEY_PREFIX = "gal_"
GALLEY_EXTRA  = ("glass",)
LAMP_MAT      = "bulb"

CHECK = [0]
FAILED = []
ABSENT = []


def log(*a):
    print(*a); sys.stdout.flush()


def ck(cond, msg):
    CHECK[0] += 1
    if not cond:
        FAILED.append(msg)
        log("  FAIL  %s" % msg)


def panels(cap, denom, log=log):
    """The three panels, all off ONE capture and ONE index pass."""
    import numpy as np
    import sheet as S
    import studio as ST
    import sticker as SK

    meta, alpha, index = cap["meta"], cap["alpha"], cap["index"]
    H, W = alpha.shape
    d = float(meta["dist"])
    px_per_m = (W / ST.SENSOR_W) * (meta["lens"] / d)
    px_mm = (1000.0 / denom) / px_per_m
    art = alpha
    tot = int(art.sum())
    ix = meta["index"]

    # ---- the two masks the whole object is about, both MEASURED -------------
    names = sorted(n for n in ix
                   if n.startswith(GALLEY_PREFIX) or n in GALLEY_EXTRA)
    galley = np.zeros_like(art)
    drawn, empty = [], []
    for n in names:
        m = (index == ix[n]) & art
        c = int(m.sum())
        (drawn if c else empty).append((n, c))
        if c:
            galley |= m
    lamp = (index == ix[LAMP_MAT]) & art if LAMP_MAT in ix else np.zeros_like(art)

    tube = int(((index == ix["gal_tube"]) & art).sum()) if "gal_tube" in ix else -1
    log("  THE ONE EMITTER, `gal_tube`: %d px on this capture.  The concept "
        "says to draw it; it CANNOT BE SEEN, so what is drawn is the room it "
        "lights (declared, not absorbed)" % tube)
    log("  galley materials ON SCREEN: %d of %d" % (len(drawn), len(names)))
    for n, c in sorted(drawn, key=lambda t: -t[1]):
        log("    %-14s %7d px  %6.3f %% of art" % (n, c, 100.0 * c / tot))
    if empty:
        log("    DROPPED (zero px, NOT drawn): %s"
            % ", ".join(n for n, _ in empty))
    log("  glow area  %d px (%.3f %% of art);  festoon lamps %d px (%.3f %%)"
        % (int(galley.sum()), 100.0 * galley.sum() / tot,
           int(lamp.sum()), 100.0 * lamp.sum() / tot))

    ck(tube == 0, "A1 gal_tube is visible after all (%d px) -- this sheet's "
                  "whole premise is stated on the assumption it is not" % tube)
    ck(galley.sum() > 0, "A2 the galley is EMPTY -- nothing to glow")
    ck(lamp.sum() > 0, "A3 the festoon lamps are absent; the A/B has no B")

    # ---- sheet geometry -----------------------------------------------------
    art_w, art_h = W * px_mm, H * px_mm
    # THE DRAWN EXTENT, MEASURED off the alpha bbox -- NOT the frame width.
    # The first draft of this sheet printed the FRAME (289.0 mm) as "the art is
    # N mm long", which is not the object and would have gone to the owner.
    ys, xs = np.where(art)
    draw_w = (int(xs.max()) - int(xs.min()) + 1) * px_mm
    draw_h = (int(ys.max()) - int(ys.min()) + 1) * px_mm
    # ⚠ AND IT IS NOT THE CONCEPT'S 200 mm EITHER.  The concept computes 200 mm
    # off the BODY (STATE.md's 4.065 m ex-lids / 20.325).  What is drawn is the
    # whole silhouette -- counter and the OPENED tail board included -- so at
    # the concept's own denominator the sticker is longer than the concept
    # says.  Reported, not silently rescaled: rescaling would make the object
    # fit the sentence by moving the ruler.
    want_mm = 4.065 * 1000.0 / denom
    denom_for_200 = denom * draw_w / want_mm
    log("  DRAWN EXTENT %.2f x %.2f mm (alpha bbox), against the frame's "
        "%.1f mm.  The concept's \"200 mm\" is the BODY at 1:%.3f (%.2f mm); "
        "the drawn silhouette includes the counter and the OPEN tail board, so "
        "it is %.2f mm.  1:%.2f would put the WHOLE silhouette at %.0f mm -- "
        "the owner's call, not this script's"
        % (draw_w, draw_h, art_w, denom, want_mm, draw_w, denom_for_200,
           want_mm))
    COLOPHON_LINES = 19
    colophon_h = 5.0 + COLOPHON_LINES * 1.9 + 3.0
    label_h = 5.5
    sheet_w = art_w + 12.0
    sheet_h = 3 * (art_h + label_h) + 2 * PANEL_GAP_MM + colophon_h + 8.0
    ox = (sheet_w - art_w) * 0.5
    sh = S.Sheet(sheet_w, sheet_h, ink=LINE_INK, stock=STOCK, dpi=300, ss=2)
    log("  sheet %.1f x %.1f mm at 1:%.3f -- the art is %.1f mm long"
        % (sheet_w, sheet_h, denom, art_w))

    def regions(mask, oy):
        return SK.contours(mask, px_mm, ox, oy, SIMPLIFY_MM, MIN_AREA_MM2)

    stats = dict(areas=0)

    def lay(mask, oy, rgb):
        n = 0
        for p in regions(mask, oy):
            sh.area(p, rgb=rgb, tint=1.0)      # tint=1.0 ALWAYS -- F350's trap
            n += 1                             # is mix() toward the STOCK
        stats["areas"] += n
        return n

    y = 4.0
    # ---- PANEL 1: DAYLIGHT, the shut panel van ------------------------------
    # ⚠⚠ THE FIRST DRAFT OF THIS PANEL DREW ONE FLAT SILHOUETTE IN ONE INK AND
    # IT LOOKED LIKE A RED SLAB.  Found by CROPPING THE PROOF AND LOOKING
    # (rule 1), not by any of the ten checks, every one of which was green on
    # it.  The vehicle has to be painted through the material index, in the
    # AUTHORED palette -- which is F346's ruling in one sentence: the model
    # says WHERE, the palette says WHAT IN.
    sh.text(ox, y + 3.2, "DIA  ---  la combi cerrada", pt=8.0)
    y += label_h
    who, ink_rgb, order, unknown = SK.palette_map(meta, log=log)
    n_day = lay(art, y, DAY_CREAM)          # the ground the rest sits on
    painted, per_ink, per_ink_fam = 0, {}, {}
    for name in sorted(ix):
        if name.startswith(GALLEY_PREFIX) or name in GALLEY_EXTRA:
            continue                        # the interior is handled below
        m = (index == ix[name]) & art
        if not m.any():
            continue
        slot = who.get(name)
        if slot:
            rgb = ink_rgb.get(slot, DAY_DARK)
        else:
            # FALL-THROUGH BY MEASURED ALBEDO, not by a default.  `T1_paint`
            # -- THE BODY ITSELF -- is unassigned by name, and the first
            # version of this loop painted every unassigned material DAY_DARK,
            # so the combi's own paint came out near-black.  `classify()`
            # already measures each index into an ink family off the albedo;
            # use it rather than guessing (rule 10: ask the mesh).
            fam_name = (cap.get("fam") or {}).get(ix[name])
            rgb = FAM_INK.get(fam_name, DAY_DARK)
            per_ink_fam[fam_name or "no family"] = \
                per_ink_fam.get(fam_name or "no family", 0) + 1
        k = lay(m, y, rgb)
        painted += k
        per_ink[slot or "nearest/unassigned"] = per_ink.get(slot or "nearest/unassigned", 0) + k
    # THE APERTURES ARE PRINTED SHUT.  The daylight state is the panel van the
    # vehicle was before the conversion -- that is the concept's own words and
    # the reason the object works: the day picture and the night picture are
    # the SAME die cut and different information.
    # AND SHUT THE REST OF THE INTERIOR.  `galley` is the `gal_*` prefix plus
    # `glass`; the palette ALSO assigns other materials to the `interior` slot
    # (the counter run, the menu cards) and those are inside the apertures too.
    # They survived the first shut and read as grey blocks at the foot of two
    # bays -- again found by looking, not by a check.
    # ABLATION, watched by hand (the verifier does not run these -- F355):
    #   T1_APAGA_NOSHUT=1  leaves the apertures OPEN, and A8 must RED.
    NOSHUT = os.environ.get("T1_APAGA_NOSHUT") == "1"
    shut = np.zeros_like(galley) if NOSHUT else galley.copy()
    for name in ([] if NOSHUT else sorted(ix)):
        if who.get(name) == "interior":
            shut |= (index == ix[name]) & art
    # AND SHUT BY GEOMETRY, NOT BY NAME.  Two grey blocks survived both passes
    # above and I sampled the proof to find out what they were rather than
    # guessing a third time: `chrome_dull`, the counter shelf seen INSIDE the
    # bay.  That material is also the trim and the bumper, so shutting it by
    # NAME would delete correct drawing elsewhere.  The rule that generalises
    # is spatial: a connected component whose bounding box sits INSIDE an
    # aperture's bounding box is something seen THROUGH the opening, whatever
    # it is called.  MEASURED per component; nothing is named in this block.
    import scipy.ndimage as _ndi
    gl_lab, gl_n = _ndi.label(galley, structure=np.ones((3, 3)))
    boxes = [b for b in _ndi.find_objects(gl_lab) if b is not None]
    n_geo = 0
    for name in ([] if NOSHUT else sorted(ix)):
        if name.startswith(GALLEY_PREFIX) or name in GALLEY_EXTRA:
            continue
        m = (index == ix[name]) & art
        if not m.any():
            continue
        lab_m, nm = _ndi.label(m, structure=np.ones((3, 3)))
        for sl in _ndi.find_objects(lab_m):
            if sl is None:
                continue
            for gb in boxes:
                if (sl[0].start >= gb[0].start and sl[0].stop <= gb[0].stop and
                        sl[1].start >= gb[1].start and sl[1].stop <= gb[1].stop):
                    comp = np.zeros_like(m)
                    comp[sl] = m[sl]
                    shut |= comp
                    n_geo += 1
                    break
    log("  shut BY GEOMETRY: %d component(s) whose bbox lies inside one of "
        "%d aperture bbox(es) -- measured, not named" % (n_geo, len(boxes)))
    # AND SHUT WHAT THE SEAL RING ENCLOSES.  This is the pass that finally
    # closes the bays, and it only became possible once the opening was
    # defined correctly: the three serving apertures are UNGLAZED, so every
    # earlier attempt (by name, by palette slot, by `glass` bbox) was looking
    # at the wrong openings.  The seal is the physical surround; anything
    # inside it that is not the body, the seal or the festoon string is seen
    # THROUGH the aperture and the daylight state shuts it.
    _seal0 = (index == ix["rubber"]) & art if "rubber" in ix else np.zeros_like(art)
    _sl0, _ = _ndi.label(_seal0, structure=np.ones((3, 3)))
    _open0 = np.zeros_like(art)
    for sl in _ndi.find_objects(_sl0):
        if sl is not None and (sl[0].stop - sl[0].start) > 40 \
           and (sl[1].stop - sl[1].start) > 40:
            _open0[sl] = True
    if not NOSHUT:
        _body0 = np.zeros_like(art)
        for n0 in ix:
            if who.get(n0) == "red" or n0 == "T1_paint":
                _body0 |= (index == ix[n0]) & art
        _extra = _open0 & art & (~_body0) & (~_seal0) & (~lamp) & (~shut)
        shut |= _extra
        log("  shut BY THE SEAL RING: %d further px enclosed by an aperture "
            "surround -- the pass that actually closes the bays"
            % int(_extra.sum()))
    # ⚠⚠ THE RESIDUAL — AND ITS FIRST TWO VERSIONS WERE BOTH WRONG, RETRACTED
    # HERE IN THE SAME REVISION (rule 13).
    #
    # v1 read `(~shut) & fill(galley)`.  `shut` is built FROM `galley`, so that
    # is zero BY CONSTRUCTION -- a tautology (rule 6) that printed 0 px and
    # could never print anything else.
    #
    # v2 defined the opening from the `glass` material's component boxes.  That
    # IS independent of `shut`, so it escaped the tautology -- and it measured
    # THE WRONG OPENINGS.  MEASURED: `open_reg` from `glass` overlaps `gal_*`
    # by ZERO pixels, because THE THREE SERVING APERTURES HAVE NO GLAZING —
    # `STATE.md` says so in terms ("open serving apertures on +Y: 3").  The
    # only glazed openings on this flank are the cab door window and the front
    # quarter light.  So v2's 1075 px was leakage around the CAB WINDOWS, and
    # the cause published with it -- "the counter shelf, in bays 1 and 2" --
    # was wrong: by material the 1075 px is 759 `rubber`, 232 `bulb` and only
    # 84 `chrome_dull`.  **A number was published off a mask nobody painted.
    # That is rule 8, the defect this project calls its most repeated.**
    #
    # v3, here.  The opening is the BAY SEAL RING -- the `rubber` components,
    # which are the physical surround of each aperture.  Independent of the
    # galley contents and of `shut` (rule 6), and it actually covers the bays:
    # three seal components hold 11728 / 10457 / 9550 galley px, and the fourth
    # large one is the cab window at 0.  MEASURED, and the mask is painted to
    # `probe_scratch/apaga_resid.png` every run so the next reader can look at
    # it instead of trusting this comment (rule 8).
    seal = (index == ix["rubber"]) & art if "rubber" in ix else np.zeros_like(art)
    s_lab, _ = _ndi.label(seal, structure=np.ones((3, 3)))
    open_reg = np.zeros_like(art)
    nbay = 0
    for sl in _ndi.find_objects(s_lab):
        if sl is None:
            continue
        if (sl[0].stop - sl[0].start) > 40 and (sl[1].stop - sl[1].start) > 40:
            open_reg[sl] = True
            nbay += 1
    body_ix = {ix[n] for n in ix if who.get(n) == "red" or n == "T1_paint"}
    resid = open_reg & art & (~shut) & (~seal)
    for bk in body_ix:
        resid &= ~(index == bk)
    resid &= ~lamp          # the lamps are DRAWN on purpose in panel 1
    # AND EXCLUDE THE SEAL RING ITSELF.  It DEFINES the opening; it is not
    # something showing THROUGH it, and it is drawn on purpose.  Painting the
    # mask and looking is what showed this: the magenta was mostly the four
    # seal outlines.  Counting the frame as leakage inflated the residual by
    # 2751 px and would have made A8 a red about correct drawing (rule 8).
    n_resid = int(resid.sum())
    try:
        from PIL import Image as _I
        _I.fromarray((resid * 255).astype("uint8")).save(
            os.path.join(ROOT, "probe_scratch", "apaga_resid.png"))
    except Exception:
        pass
    by = {}
    for k in np.unique(index[resid]) if n_resid else []:
        nm3 = {v: q for q, v in ix.items()}.get(int(k), "?")
        by[nm3] = int(((index == k) & resid).sum())
    log("  aperture opening = %d px over %d seal ring(s), from the SEAL "
        "geometry -- independent of `shut` AND of the galley (rule 6); it "
        "covers the three OPEN serving bays, which have no glazing at all"
        % (int(open_reg.sum()), nbay))
    log("  ⚠ RESIDUAL SHOWING THROUGH THE SHUT APERTURES: %d px (%.4f %% of "
        "art), by material %s.  PAINTED to probe_scratch/apaga_resid.png -- "
        "look at it before quoting it (rule 8)"
        % (n_resid, 100.0 * n_resid / tot,
           sorted(by.items(), key=lambda t: -t[1])[:6]))
    # ⚠⚠ A8's CEILING, AND IT IS THE THIRD TIME THIS GUARD HAS BEEN A
    # TAUTOLOGY IN ONE REVISION. STATED RATHER THAN DRESSED UP (rule 6, 12).
    # Now that the seal-ring pass SHUTS exactly the set this expression
    # MEASURES, `n_resid` is 0 on the normal path BY CONSTRUCTION. So A8's
    # green is NOT evidence that the apertures are shut -- it is arithmetic.
    # ALL of its discriminating power is in the ablation: with
    # T1_APAGA_NOSHUT=1 it reads ~52 600 px and REDS. Read it that way and no
    # other way, and DO NOT quote its green as a fidelity result.
    # What IS evidence is the painted mask beside it: look at the PNG.
    ck(n_resid < 0.010 * tot,
       "A8 %d px (%.3f %%) still show through the shut apertures against a "
       "bar of %d px -- the daylight panel is not the panel van"
       % (n_resid, 100.0 * n_resid / tot, int(0.010 * tot)))
    n_shut = lay(shut, y, DAY_BODY)
    n_lampd = lay(lamp, y, DAY_LAMP)
    # the line pass, clipped to the art, over the top
    n_line, n_void = 0, 0
    if cap.get("lines"):
        import math
        for stk in cap["lines"]:
            # ⚠⚠ DROP THE KITCHEN.  The daylight state is the SHUT PANEL VAN
            # -- the vehicle before the conversion -- and that is the whole
            # reason the object works: the day picture and the night picture
            # are the SAME die cut carrying different information.  Filling the
            # galley with body ink is NOT enough on its own, because the line
            # pass then draws the shelves, the bottles and the warmer straight
            # back over the top of it.  The first proof of THIS sheet did
            # exactly that and the apertures read OPEN, with the kitchen
            # showing through -- found by cropping and looking (rule 1), with
            # all twelve checks green.  It is rev 78's defect returning by a
            # different route, and it is the owner's own sentence: "too
            # committed to the model rather than the combi itself".
            pts, over = [], 0
            for u, v in stk:
                px, py = int(round(u * W)), int(round(v * H))
                if not (0 <= px < W and 0 <= py < H and art[py, px]):
                    continue
                if shut[py, px]:
                    over += 1
                pts.append((ox + u * W * px_mm, y + v * H * px_mm))
            if pts and over > VOID_FRAC * len(pts):
                n_void += 1
                continue
            pts = SK.rdp(pts, SIMPLIFY_MM)
            if len(pts) < 2:
                continue
            L = sum(math.hypot(pts[i+1][0]-pts[i][0], pts[i+1][1]-pts[i][1])
                    for i in range(len(pts)-1))
            if L < LINE_MIN_MM:
                continue
            sh.poly(pts, w=0.22, rgb=LINE_INK, tint=1.0)
            n_line += 1
    log("  panel 1 DAYLIGHT: %d ground + %d material region(s) in the AUTHORED "
        "palette (%s), apertures SHUT over %d galley region(s), %d lamp "
        "region(s), %d line stroke(s) of %d kept, %d dropped as kitchen"
        % (n_day, painted,
           ", ".join("%s %d" % (k, v) for k, v in sorted(per_ink.items())),
           n_shut, n_lampd, n_line, len(cap.get("lines") or []), n_void))
    if per_ink_fam:
        log("    fell through to MEASURED albedo family: %s"
            % ", ".join("%s %d" % (k, v) for k, v in sorted(per_ink_fam.items())))
    ck(painted >= 8, "A6 only %d material region(s) painted in the daylight "
                     "panel -- it is a silhouette again, not a drawing" % painted)
    ck(n_line > 50, "A7 only %d line stroke(s) survived; the daylight panel "
                    "has no drawing on it" % n_line)
    y += art_h + PANEL_GAP_MM

    # ---- PANEL 2: DARK, reading A -- the lamps GLOW -------------------------
    sh.text(ox, y + 3.2, "NOCHE  ---  lectura A: las series SI encienden", pt=8.0)
    y2 = y + label_h
    sh.fill(ox, y2, art_w, art_h, tint=1.0, rgb=NIGHT_GROUND)
    n_g2 = lay(galley, y2, GLOW_INK)
    n_l2 = lay(lamp, y2, GLOW_DIM)
    log("  panel 2 DARK / reading A: %d glowing galley region(s) + %d GLOWING "
        "lamp region(s)" % (n_g2, n_l2))
    y = y2 + art_h + PANEL_GAP_MM

    # ---- PANEL 3: DARK, reading B -- the lamps do NOT glow ------------------
    sh.text(ox, y + 3.2, "NOCHE  ---  lectura B: las series NO encienden", pt=8.0)
    y3 = y + label_h
    sh.fill(ox, y3, art_w, art_h, tint=1.0, rgb=NIGHT_GROUND)
    n_g3 = lay(galley, y3, GLOW_INK)
    n_l3 = lay(lamp, y3, DAY_LAMP)
    log("  panel 3 DARK / reading B: %d glowing galley region(s); the %d lamp "
        "region(s) stay in DAYLIGHT ink so they visibly do NOT glow"
        % (n_g3, n_l3))
    y = y3 + art_h + 6.0

    ck(n_g2 == n_g3, "A4 the two dark readings differ in the GALLEY, which is "
                     "the half they are supposed to share (%d vs %d)"
       % (n_g2, n_g3))
    ck(n_l2 == n_l3, "A5 the two readings differ in lamp COUNT (%d vs %d); "
                     "they must differ only in INK" % (n_l2, n_l3))
    # A9 -- THE CHECK THE OWNER'S A/B ACTUALLY DEPENDS ON, AND IT WAS MISSING.
    # A4 and A5 assert the two night readings are the SAME in region count.
    # NOTHING asserted they DIFFER. Set GLOW_DIM = DAY_LAMP and every other
    # check here stays green while the owner is shown ONE answer twice -- a
    # claim that lived only in a comment, which rule 10 says is not a test.
    ck(tuple(GLOW_DIM) != tuple(DAY_LAMP),
       "A9 reading A's lamp ink %s is identical to reading B's %s -- the two "
       "night panels are the same picture and the owner's A/B is empty"
       % (str(GLOW_DIM), str(DAY_LAMP)))

    return sh, y, dict(px_mm=px_mm, art_w=art_w, draw_w=draw_w,
                       n_resid=n_resid,
                       draw_h=draw_h, want_mm=want_mm,
                       denom_for_200=denom_for_200,
                       n_lamp_regions=n_l2, tot=tot, tube=tube,
                       galley=int(galley.sum()), lamp=int(lamp.sum()),
                       drawn=drawn, empty=empty, areas=stats["areas"],
                       sheet=(sheet_w, sheet_h))


def colophon(sh, y, st, meta, denom, tag):
    """AUTHORED constants go ON THE SHEET, not only into the log.

    Rev 78 reported its seven tuning constants at run time and its own brief
    claimed they were "labelled AUTHORED on the artefact".  They were not, and
    the rule-17 adversary proved it by extracting the SVG's text nodes.  So
    they are printed here, and W5 below checks every baseline is on the sheet.
    """
    L = [
        "APAGA LA LUZ  --  la combi de noche.  Linea: NINOS (F331).  "
        "Rev 79, F362, comprado por el propietario.",
        "1:%.3f  --  silueta DIBUJADA %.2f x %.2f mm (medida del bbox), hoja "
        "%.1f x %.1f mm.  Captura '%s', azimut %.1f deg, lente %d mm."
        % (denom, st["draw_w"], st["draw_h"], st["sheet"][0], st["sheet"][1],
           tag, float(meta["az"]), int(meta["lens"])),
        "OJO -- NO SON LOS 200 mm DEL CONCEPTO: esos 200 mm son la CARROCERIA "
        "(4.065 m / %.3f = %.2f mm).  Lo dibujado incluye" % (denom, st["want_mm"]),
        "   el mostrador y la tapa trasera ABIERTA, asi que mide %.2f mm.  "
        "1:%.2f pondria la silueta entera en %.0f mm.  Decide el propietario."
        % (st["draw_w"], st["denom_for_200"], st["want_mm"]),
        "MEDIDO: el vehiculo tiene UN SOLO material emisivo -- gal_tube, la "
        "tira de trabajo de la cocina (0/0/1/0 en los cuatro modulos).",
        "MEDIDO Y ES UN PROBLEMA: gal_tube da %d px en esta captura.  NO SE VE."
        "  Se dibuja el CUARTO QUE ILUMINA, no la lampara." % st["tube"],
        "   Eso es una DESVIACION del texto del concepto, declarada aqui y en "
        "F362, no absorbida en silencio (regla 13).",
        "MEDIDO: brillo %d px (%.3f %% del arte) sobre %d materiales de cocina "
        "en pantalla; series %d px (%.3f %%)."
        % (st["galley"], 100.0 * st["galley"] / st["tot"], len(st["drawn"]),
           st["lamp"], 100.0 * st["lamp"] / st["tot"]),
        "LA PREGUNTA, DIBUJADA EN AMBOS SENTIDOS POR ORDEN DEL PROPIETARIO: sus "
        "dos autores nunca acordaron si las series encienden.",
        "   MEDIDO: %d region(es) del material `bulb` en esta captura.  ESO NO "
        "ES EL CONTEO DE FOCOS -- el construido es 118 por aritmetica"
        % st["n_lamp_regions"],
        "   (BULB_X0/X1/PITCH, ver CONCEPT_ROUND_rev77 5.0b) y ~115 el "
        "fotografiado.  Son tres numeros distintos; ninguno se imprime solo.",
        "AUTORADO (una ELECCION, no una medida): tinta de brillo %s, brillo "
        "tenue %s, fondo de noche %s," % (str(GLOW_INK), str(GLOW_DIM),
                                          str(NIGHT_GROUND)),
        "AUTORADO: cuerpo %s, crema %s, oscuro %s, lampara apagada %s."
        % (str(DAY_BODY), str(DAY_CREAM), str(DAY_DARK), str(DAY_LAMP)),
        "AUTORADO: simplificacion %.2f mm, area minima %.2f mm2, escala 1:%.3f,"
        " separacion de paneles %.1f mm, VOID_FRAC %.2f, linea minima %.2f mm."
        % (SIMPLIFY_MM, MIN_AREA_MM2, denom, PANEL_GAP_MM, VOID_FRAC,
           LINE_MIN_MM),
        "MEDIDO Y NO ARREGLADO: %d px (%.4f %% del arte) se ven todavia por las "
        "aperturas cerradas.  El estado de DIA no es todavia" % (
            st["n_resid"], 100.0 * st["n_resid"] / st["tot"]),
        "   la panel van exacta que pide el concepto.  Se dice aqui, en la "
        "hoja, no solo en el registro.",
        "⚠ A8 vale 0 px POR CONSTRUCCION en la via normal; su unica fuerza "
        "esta en la ablacion T1_APAGA_NOSHUT=1.  No se cite su verde.",
        "   Otro contexto elegiria distinto y obtendria otra calcomania.  Se "
        "dice, no se esconde.",
        "NINGUN INSTRUMENTO DE ESTE ARBOL PUEDE DECIR SI ESTO ESTA BIEN.  "
        "Las comprobaciones miden coherencia, no calidad.",
        "El propietario no ha visto una calcomania impresa.  La prueba de "
        "vinilo (~$0, una hoja A4) sigue sin hacerse.",
    ]
    for i, s in enumerate(L):
        sh.text(4.0, y + 3.0 + i * 1.9, s, pt=4.1)
    return y + 3.0 + (len(L) - 1) * 1.9


def selftest(log=log):
    """FABRICATED inputs with a KNOWN answer.  Rev 78's own lesson: five of its
    six wrong instruments were a mask selecting the wrong pixels, and the one
    caught without a picture was caught by a selftest like this."""
    import numpy as np
    import sticker as SK
    log("apaga selftest -- fabricated masks, known answers")

    # T1: a 10x10 block at a known px_mm must trace to a known AREA.
    m = np.zeros((40, 40), bool); m[10:20, 10:20] = True
    got = SK.contours(m, 1.0, 0.0, 0.0, 0.01, 0.0)
    ck(len(got) == 1, "T1 a single block traced as %d region(s)" % len(got))
    if got:
        a = abs(SK.poly_area(got[0]))
        ck(80.0 <= a <= 121.0, "T1b a 10x10 block at 1.0 mm/px measured "
                               "%.2f mm2, want ~100" % a)

    # T2: MIN_AREA_MM2 must actually drop a speck -- watched, not assumed.
    sp = np.zeros((40, 40), bool); sp[5, 5] = True
    ck(len(SK.contours(sp, 1.0, 0, 0, 0.01, 50.0)) == 0,
       "T2 a 1 px speck survived a 50 mm2 floor")

    # T3: two DISJOINT blocks must not merge -- the galley/lamp separation is
    # exactly this, and a merge would silently fuse the A/B's two answers.
    d2 = np.zeros((40, 40), bool); d2[5:10, 5:10] = True; d2[25:30, 25:30] = True
    ck(len(SK.contours(d2, 1.0, 0, 0, 0.01, 0.0)) == 2,
       "T3 two disjoint blocks did not trace as 2 regions")

    # T4: THE ONE THAT MATTERS.  An index pass where the galley and the lamps
    # are DIFFERENT indices must separate; if this fails the two dark readings
    # are the same picture and the owner's A/B is a fraud.
    idx = np.zeros((40, 40), "int32"); art = np.ones((40, 40), bool)
    idx[5:10, 5:10] = 7      # galley
    idx[25:30, 25:30] = 4    # lamp
    g = (idx == 7) & art; l = (idx == 4) & art
    ck(int(g.sum()) == 25 and int(l.sum()) == 25,
       "T4 index separation is wrong: galley %d, lamp %d, want 25/25"
       % (int(g.sum()), int(l.sum())))
    ck(not (g & l).any(), "T4b the galley and lamp masks OVERLAP -- the two "
                          "readings would differ by less than they claim")

    # T5: and the negative -- if they shared an index the guard must NOTICE.
    idx2 = np.full((40, 40), 7, "int32")
    g2 = (idx2 == 7); l2 = (idx2 == 7)
    ck((g2 & l2).any(), "T5 the overlap detector cannot see a total overlap; "
                        "T4b is decorative")
    log("%d checked, %d FAILED" % (CHECK[0], len(FAILED)))
    return 1 if FAILED else 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="side")
    ap.add_argument("--denom", type=float, default=DENOM)
    ap.add_argument("--out", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()

    import sticker as SK
    cap = SK.load_capture(a.tag)
    if cap is None:
        log("NO CAPTURE '%s'.  Nothing was measured (rule 37).  Run:" % a.tag)
        log("    python3 sticker_pass.py --az 90 --tag %s --lines" % a.tag)
        log("0 checked, 0 FAILED, 1 ABSENT")
        return 2

    log("APAGA LA LUZ -- capture '%s'" % a.tag)
    sh, y, st = panels(cap, a.denom)
    ybot = colophon(sh, y, st, cap["meta"], a.denom, a.tag)

    os.makedirs(DES, exist_ok=True)
    base = a.out or os.path.join(DES, "apaga_r79_%s" % a.tag)
    svg, png = base + ".svg", base + ".png"
    sh.save_svg(svg); sh.save_png(png)

    import xml.etree.ElementTree as ET
    NS = "{http://www.w3.org/2000/svg}"
    root = ET.parse(svg).getroot()
    paths = len(root.findall(".//%spath" % NS))
    nareas = sum(1 for k, _ in sh.ops if k == "area")
    ck(paths == nareas, "W2 %d <path> against %d area op(s) -- the two "
                        "backends have drifted" % (paths, nareas))
    ck(root.get("width", "").endswith("mm"),
       "W3 the SVG is not in millimetres; a cutter cannot use it")
    ck(os.path.getsize(png) > 20000, "W4 the PNG proof is empty or trivial")
    ck(ybot <= st["sheet"][1],
       "W5 the colophon's last baseline is at %.1f mm on a %.1f mm sheet -- it "
       "has run off the bottom" % (ybot, st["sheet"][1]))
    # W6: the two dark readings must NOT be byte-identical pictures.  If they
    # are, the owner is being shown one answer twice.
    # W6 USED TO DUPLICATE A3 (both asserted `lamp > 0`) and its own comment
    # claimed it compared the two night panels, which it never did. Rewritten
    # to test a different failure: a glow ink that matches the night ground
    # renders both dark panels blank.
    ck(tuple(GLOW_INK) != tuple(NIGHT_GROUND),
       "W6 the glow ink %s equals the night ground %s -- both dark panels are "
       "blank" % (str(GLOW_INK), str(NIGHT_GROUND)))
    log("  wrote %s" % svg)
    log("  wrote %s" % png)
    log("%d checked, %d FAILED%s"
        % (CHECK[0], len(FAILED),
           (", %d ABSENT" % len(ABSENT)) if ABSENT else ""))
    for f in FAILED:
        log("   FAILED: %s" % f)
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
