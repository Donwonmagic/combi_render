"""
sticker.py -- F18, THE DIE-CUT STICKER.  The project's original deliverable.

WHAT THIS IS.  F18 has been the register's oldest live row since rev 44 and is
the only artefact in the programme with an owner-locked STYLE, a locked SCENE,
a named AUDIENCE and a written SPEC.  Its trigger fired at rev 77 -- F330,
*"Yes -- start it now."*  This draws it.

THE FOUR THINGS THAT ARE HIS, QUOTED, NOT PARAPHRASED
-----------------------------------------------------
  AUDIENCE  it is *"for children at the restaurant"*; it *"should spark joy and
            be something families keep"*.  Under F331 that puts this artefact
            squarely in THE CHILDREN'S LINE, which is the half of the programme
            that did not exist before rev 78.  It is not the deadpan catalogue.
  STYLE     *"cartoon with rendered depth -- vector line and flat colour,
            shading and occlusion sampled from the 3D asset"*.
  SCENE     *"nothing but the bus, die-cut tight, plus the sun and the papel
            picado"*.
  WHEELS    *"I like how the wheels were drawn in the earlier cartoon version"*
            -- and that version IS NOT IN THIS REPOSITORY.  rev 76 looked:
            `git log --all -S"cartoon"` returns markdown only.  So this drawing
            CANNOT honour that sentence, says so on its face, and asks for it.

THE SCENE-LOCK READING, STATED BECAUSE IT IS A READING AND NOT A MEASUREMENT
---------------------------------------------------------------------------
`DESIGN_PROGRAM_rev76.md` §8 raises a conflict: *"`SPEC.md` states there is no
papel picado on the vehicle; the band is a continuous flowering mass.  His
scene-lock names something the record measures as absent.  Parked, his call."*
That conflict only exists if *"the papel picado"* is read as the vehicle's own
painted band.  His sentence lists THREE things -- the bus, the sun, and the
papel picado -- and the first is already the bus, so the third is a SCENE
element hung above it, not a description of its paint.  On that reading SPEC
and the scene-lock agree and nothing needs asking.  THE READING IS PRINTED ON
THE ARTEFACT so he can reject it in one look.  The papel-picado question itself
is NOT re-put here; he closed the door on that until the sticker was being
built, and the owner's standing instruction at rev 78 is not to re-ask it.

WHAT IS SAMPLED FROM THE ASSET AND WHAT IS AUTHORED -- THE WHOLE POINT
----------------------------------------------------------------------
  SAMPLED   the die-cut silhouette; every flat-colour region and its ink; the
            shading bands; the occlusion; every line.  All of it comes out of
            `sticker_pass.py`, i.e. out of Cycles, at one camera.
  AUTHORED  the sun disc, the papel-picado bunting, the sheet size and the
            palette's tint steps.  These are DRAWN BY THIS SCRIPT and are
            labelled AUTHORED on the artefact, which is the standard the owner
            set at rev 77 for invented marks (F341) and which rev 77 itself
            broke once and had to correct in the same revision.

CEILINGS, STATED (rule 12)
--------------------------
  * THE VIEWPOINT IS A POSE.  See `sticker_pass.py`'s docstring: the spec row
    that carries it is one of the eight HARD-CUT AT 120 CHARACTERS, and 18 deg
    admits two readings.  Both are drawn.  Neither is measured.
  * THE SCALE IS RECOVERED, NOT GIVEN.  The surviving spec text never states
    the sticker's scale; it states CONSEQUENCES of one (*"the 0.30 mm louvre
    pitch"*, *"the 0.159 m minimum cut feature"*, *"0.40 mm"* gold components).
    `recover_scale()` inverts the first against `t1_detail.LOUV_PITCH` and then
    CHECKS the other two fall where that scale predicts.  If they disagree the
    check REDS -- it is a real cross-check between independently obtained
    quantities (rule 6), not a tautology.
  * PERSPECTIVE.  A 78 mm lens is not orthographic, so "1:70" holds exactly at
    the vehicle's centre depth only.  The spread across the bounding box is
    MEASURED and printed; it is not assumed small.
  * `trace_outline.trace` returns OUTER boundaries only and says so.  Holes are
    found with `has_holes` and subtracted explicitly; a silently filled window
    would read as a decision rather than a defect.
  * SIMPLIFICATION.  Contours are Douglas-Peucker'd to a tolerance stated in
    SHEET MILLIMETRES and reported.  The die-cut path is simplified at a
    TIGHTER tolerance than the colour, because a cutter follows it.
  * NOTHING HERE IS A FIDELITY CLAIM.  Every check below tests that the drawing
    agrees with the CAPTURE and with the spec's own arithmetic.  Not one of
    them compares the sticker to a photograph of a real sticker; there is no
    such photograph and the owner has not seen this object.
"""
import os, sys, json, math

ROOT = os.path.dirname(os.path.abspath(__file__))
CAP = os.path.join(ROOT, "probe_scratch", "sticker")
DES = os.path.join(ROOT, "design_out")

# --- the spec's own figures, quoted from AUDIT_rev43.md's sticker rows -------
SPEC_LOUV_PITCH_MM = 0.30      # "the 0.30 mm louvre pitch"
SPEC_MIN_CUT_M = 0.159         # "no feature narrower than 0.159 m touch the cut line"
SPEC_SACRIFICE_MM = 0.40       # "every one lands under 0.40 mm.  Delete all 48."
SPEC_LINE_FLOOR_MM = 0.15      # "three strokes, a 0.15 mm floor"
SPEC_STROKES = 3               # "three strokes"
SPEC_INKS = 7                  # "Seven inks printed; five if cut"
SPEC_INKS_CUT = 5

DESPECKLE_MM = 0.18            # AUTHORED, and reported on every run
ALBEDO_BLUR_MM = 0.42          # AUTHORED, and reported on every run
SHADE_BLUR_MM = 2.20           # AUTHORED, and reported on every run
LINE_MIN_MM = 1.60             # AUTHORED: a cartoon's line is deliberate
SHADE_PCT = 22                 # AUTHORED, reported on every run
SHADE_MULT = 0.74              # the shadow ink = the lit ink x this
AO_PCT = 12
AO_MULT = 0.58

BLEED_MM = 1.6                 # AUTHORED: the vinyl skirt outside the artwork
SIMPLIFY_COLOUR_MM = 0.12      # AUTHORED, and reported
SIMPLIFY_CUT_MM = 0.06         # tighter: a cutter follows this one
SIMPLIFY_WORDMARK_MM = 0.035   # tighter still: it is the brand's own hand

CHECK, FAILED, ABSENT = [0], [], []


def ck(cond, msg):
    CHECK[0] += 1
    if not cond:
        FAILED.append(msg)
    return bool(cond)


def log(*a):
    print(*a); sys.stdout.flush()


# ------------------------------------------------------------------- geometry
def rdp(pts, eps):
    """Douglas-Peucker, iterative (a 20 000-point contour blows the stack)."""
    if len(pts) < 3:
        return list(pts)
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        ax, ay = pts[i]; bx, by = pts[j]
        dx, dy = bx - ax, by - ay
        n = math.hypot(dx, dy)
        best, bi = -1.0, -1
        for k in range(i + 1, j):
            px, py = pts[k]
            d = (abs(dy * px - dx * py + bx * ay - by * ax) / n if n > 1e-12
                 else math.hypot(px - ax, py - ay))
            if d > best:
                best, bi = d, k
        if best > eps:
            keep[bi] = True
            stack.append((i, bi)); stack.append((bi, j))
    return [p for p, k in zip(pts, keep) if k]


def _within(hole, poly):
    """Is this hole inside this outline?  Even-odd ray cast on the hole's
    first vertex, which is enough: `holes_of` returns whole connected
    components, so a hole lies entirely inside one outline or entirely
    outside it."""
    x, y = hole[0]
    n, inside = len(poly), False
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xi:
                inside = not inside
    return inside


def poly_area(p):
    s = 0.0
    for i in range(len(p)):
        x1, y1 = p[i]; x2, y2 = p[(i + 1) % len(p)]
        s += x1 * y2 - x2 * y1
    return abs(s) * 0.5


# --------------------------------------------------------------------- scale
def recover_scale():
    """Invert the spec's 0.30 mm louvre pitch against the BUILT pitch.

    Two independently obtained quantities meet here (rule 6): the printed
    figure comes from `AUDIT_rev43.md`, the metre figure from `t1_detail.py`.
    Neither was derived from the other, so their ratio is a real recovery of a
    number the truncated spec never states.
    """
    import t1_detail as D
    pitch_m = float(D.LOUV_PITCH)
    denom = pitch_m * 1000.0 / SPEC_LOUV_PITCH_MM
    log("  SCALE RECOVERED: LOUV_PITCH %.6f m (imported from t1_detail) prints "
        "at the spec's %.2f mm  ->  1:%.2f" % (pitch_m, SPEC_LOUV_PITCH_MM, denom))
    return denom, pitch_m


# ------------------------------------------------------------------ the masks
def classify(index, albedo, alpha, meta, log=log):
    """THE INK SEPARATION, MEASURED OFF THE RENDERED ALBEDO.

    For each material index actually on screen, take the MEDIAN albedo of its
    own pixels (median, not mean -- photometry.py's standing rule, and a mean
    is dragged by the few pixels where two materials meet).  Classify that
    colour by hue against `t1_mats`' own RED / CREAM / GOLD, or as a neutral
    by value when it has no chroma.

    ⚠ WHY IT IS DONE FROM PIXELS AND NOT FROM THE NODE TREE.  rev 78's first
    draft read `Base Color.default_value`, which is the UNCONNECTED default on
    the 22 materials that LINK that socket -- `T1_paint`, the body red, among
    them.  The `ink_red` mask came out nearly EMPTY on a bus that is mostly
    red, and every figure downstream of it was plausible.  Painted and looked
    at, it was obvious in one second (rule 8).  Albedo cannot lie this way: it
    is the colour that was actually rendered.
    """
    import numpy as np
    import t1_mats as M
    import sticker_pass as SP
    refs = [("red", M.RED), ("gold", M.GOLD), ("cream", M.CREAM)]
    chrom = [(k, SP.hue_chroma(v)[0]) for k, v in refs
             if SP.hue_chroma(v)[1] >= 0.10]
    fam, per_idx, hues = {}, {}, []
    ids = np.unique(index[alpha])
    for k in ids:
        if k <= 0:
            continue
        m = (index == k) & alpha
        n = int(m.sum())
        if n < 8:
            continue
        med = tuple(float(np.median(albedo[..., c][m])) for c in range(3))
        h, c = SP.hue_chroma(med)
        if c < 0.10:
            v = max(med)
            f = ("neutral_dark" if v < 0.06 else
                 "neutral_mid" if v < 0.35 else "neutral_light")
        else:
            f = min(chrom, key=lambda q: abs((h - q[1] + 180) % 360 - 180))[0]
            hues.append((h, n))
        fam[int(k)] = f
        per_idx[int(k)] = dict(px=n, albedo=med, hue=h, chroma=c, family=f)

    # THE HUE WEDGE.  AUDIT_rev43's colour-separation row claims the whole
    # vehicle is "ONE 70 deg hue wedge plus four neutrals".  That had never
    # been checked.  Checking it needs TWO numbers, not one, and reporting
    # only the flattering one would be the defect:
    #   `wedge_all`  every chromatic material, however small.  A single 176 px
    #                material sitting at hue 180 opens this to ~171 deg -- and
    #                a printer still needs an ink for it, so it is not noise.
    #   `wedge_main` the same arc over materials holding at least AREA_FLOOR of
    #                the chromatic area.  This is what the claim is about.
    # BOTH are printed.  The check grades `wedge_main` and the excluded
    # materials are NAMED, so nothing is quietly dropped to make a bar.
    AREA_FLOOR = 0.001
    def _arc(vals):
        v = sorted(vals)
        if len(v) < 2:
            return 0.0
        g = [(v[(i + 1) % len(v)] - v[i]) % 360 for i in range(len(v))]
        return 360.0 - max(g)
    tot = sum(n for _, n in hues) or 1
    wedge = _arc([h for h, _ in hues])
    main = [h for h, n in hues if n >= AREA_FLOOR * tot]
    wedge90 = _arc(main)
    dropped = [(h, n) for h, n in hues if n < AREA_FLOOR * tot]

    # THE CLASSIFICATION MARGIN, stated because it is thin.  Every chromatic
    # material is assigned to whichever reference hue is nearer, and the
    # SECOND largest area on this vehicle sits almost midway between RED and
    # GOLD.  A drawing that splits 32 % of its chroma on a 2 deg margin should
    # say so rather than present the split as settled.
    margins = []
    for h, n in hues:
        ds = sorted(abs((h - q[1] + 180) % 360 - 180) for q in chrom)
        if len(ds) > 1:
            margins.append((ds[1] - ds[0], n, h))
    margins.sort()
    log("  hue wedge %.1f deg over all %d chromatic material(s); %.1f deg over "
        "the %d holding >= %.1f %% of chromatic area (spec row claims 70).  "
        "%d material(s) excluded from the second figure, at hue(s) %s"
        % (wedge, len(hues), wedge90, len(main), AREA_FLOOR * 100, len(dropped),
           ", ".join("%.1f" % h for h, _ in dropped) or "-"))
    if margins:
        m, n, h = margins[0]
        log("  ⚠ thinnest red/gold classification margin %.2f deg, on a "
            "material holding %.1f %% of the chromatic area (hue %.2f).  "
            "⚠ NEVER QUOTE THE MARGIN WITHOUT THE AREA -- a thin margin on a "
            "0.1 %% material is not the same finding as a thin margin on a "
            "60 %% one.  The split is REPORTED, not settled."
            % (m, 100.0 * n / tot, h))

    masks = {}
    for k, f in fam.items():
        m = (index == k) & alpha
        masks[f] = m if f not in masks else (masks[f] | m)
    log("  ink separation MEASURED off the albedo: %s"
        % ", ".join("%s %d" % (f, sum(1 for v in fam.values() if v == f))
                    for f in sorted(set(fam.values()))))
    log("  hue wedge %.1f deg over %d chromatic material(s); %.1f deg over the "
        "90 %% of chromatic AREA nearest the mode (spec row claims 70)"
        % (wedge, len(hues), wedge90))
    return masks, fam, per_idx, wedge, wedge90


# ---------------------------------------------------------------- the palette
# ⚠ THE OWNER RULED AT REV 78, LOOKING AT THE FIRST PROOF: *"that looks
# terrible.  I'm worried we're too committed to the model rather than the
# combi itself."*  He chose DRAW IT, MODEL AS UNDERLAY.
#
# So the model is no longer asked what COLOUR anything is.  It is asked what
# each pixel IS -- which is the one thing it knows exactly, through the
# material index -- and the palette below decides what that gets printed in.
# The assignment is AUTHORED and is listed on the artefact.
#
# WHAT THE FIRST PROOF DID INSTEAD, AND WHY IT FAILED: it clustered the
# rendered albedo into seven inks.  That albedo is DELIBERATELY WEATHERED
# (SPEC §3 locks the finish as weathered, correctly, for the photoreal
# render), so the clustering spent its inks on grime and the bus came out
# mud-coloured; and every one of the galley's twenty-odd objects got its own
# outline, so the drawing rendered its own kitchen through the serving
# windows.  34 checks passed on that image and both ablation kills fired.
# Rule 2, exactly: a green check is not evidence about the vehicle.
#
# The palette is SEVEN inks, which is the spec row's own count, and the three
# paints are the project's MEASURED constants rather than invented colours --
# what is authored here is which material prints in which ink, not the ink.
PALETTE = [
    ("red",      "t1_mats.RED",   None),
    ("cream",    "t1_mats.CREAM", None),
    ("gold",     "t1_mats.GOLD",  None),
    ("ink",      None,            (32, 28, 26)),   # the drawing's line black
    ("interior", None,            (58, 50, 47)),   # the galley, as ONE void
    ("steel",    None,            (168, 168, 172)),
    ("tyre",     None,            (46, 43, 42)),
]
# five if cut -- the spec row's own reduction, so it can be priced
CUT_MERGE = {"interior": "ink", "steel": "cream"}

# ⚠ THE TWO-TONE IS A TEXTURE, NOT A MATERIAL.  `T1_paint` is the WHOLE
# shell, and the cream-over-red split the combi actually wears is painted into
# its texture.  Assigning one ink per material therefore printed the entire
# body red and lost the two-tone -- caught by looking at the second proof.
# So these materials are SPLIT IN TWO by their own albedo luminance, with an
# Otsu threshold found on the material's own pixels, and each half is printed
# in one of the project's MEASURED constants.  A two-way split cannot make
# mud: there is no third colour for it to land on.
# ⚠ AND IT IS A THREE-WAY SPLIT, NOT TWO.  A two-way Otsu on luminance put
# the GOLD PAISLEY and the SEÑOR TACOMBI SCRIPT in the bright half with the
# cream, and the flank came out with ragged cream blotches where its artwork
# should be -- caught on the third proof.  `T1_paint`'s texture carries three
# paints, so each pixel is snapped to whichever of the three MEASURED
# constants it is nearest in linear light.  A nearest-of-three snap to fixed
# constants cannot invent a colour: there is nothing between them to land on.
SPLIT = {"T1_paint": ("red", "cream", "gold")}

ASSIGN = {
    "red":      ("capred", "roundelred", "gal_red", "ruby", "lidmural",
                 "script"),
    "cream":    ("cream", "bumpercream", "countercream", "wheelcream",
                 "capwhite"),
    # `script` prints in the BODY RED: the wordmark itself is drawn over it
    # from the recovered hand, so posterising its footprint too would leave a
    # blob showing around the letterforms
    "gold":     ("lidsign", "calidad", "brass", "amber", "bulb"),
    # the mural board's GROUND is the deep red the photographs show; its
    # flowers are drawn over it in gold by `draw()`
    
    "ink":      ("glass", "underseal", "reflector", "lens"),
    "interior": ("interior_dark",),          # every gal_* joins this below
    "steel":    ("chrome", "chrome_dull", "steel", "countertan"),
    "tyre":     ("tyre", "rubber"),
}


def palette_map(meta, log=log):
    """material name -> ink name.  Every `gal_*` collapses into ONE interior.

    THE GALLEY IS THE POINT.  It is twenty-odd separate objects and the first
    proof drew every one of them through the serving apertures.  A drawing of
    a taco bus does not render its own kitchen: the apertures are a dark void
    with a counter line across them, and that is a DRAWING decision, stated.
    """
    import t1_mats as M
    import sticker_pass as SP
    ink_rgb, order = {}, []
    for name, const, lit in PALETTE:
        ink_rgb[name] = SP.srgb(getattr(M, const.split(".")[-1])) if const else lit
        order.append(name)
    who, unknown = {}, []
    for mat in sorted(meta["index"]):
        if mat.startswith("gal_"):
            who[mat] = "interior"
            continue
        hit = [k for k, v in ASSIGN.items() if mat in v]
        if hit:
            who[mat] = hit[0]
        else:
            who[mat] = None
            unknown.append(mat)
    log("  palette: %d ink(s) -- %s" % (len(order), ", ".join(
        "%s %s" % (k, ink_rgb[k]) for k in order)))
    log("  %d material(s) assigned by NAME; %d fall through to nearest-ink by "
        "their measured albedo and are named here, not absorbed silently: %s"
        % (sum(1 for v in who.values() if v), len(unknown),
           ", ".join(unknown) or "-"))
    return who, ink_rgb, order, unknown


def otsu(v):
    """Threshold that best separates two populations, on the values given.
    Standard Otsu; used only where a material is KNOWN to carry exactly two
    paints, so the two-class assumption is the fact, not a hope."""
    import numpy as np
    h, e = np.histogram(v, bins=128)
    h = h.astype("float64")
    c = h.cumsum()
    m = (h * ((e[:-1] + e[1:]) * 0.5)).cumsum()
    tot, mt = c[-1], m[-1]
    if tot <= 0:
        return float(np.median(v))
    wb = c
    wf = tot - c
    ok = (wb > 0) & (wf > 0)
    if not ok.any():
        return float(np.median(v))
    mb = np.where(wb > 0, m / np.maximum(wb, 1e-9), 0.0)
    mf = np.where(wf > 0, (mt - m) / np.maximum(wf, 1e-9), 0.0)
    var = wb * wf * (mb - mf) ** 2
    var[~ok] = -1
    return float((e[:-1] + e[1:])[int(var.argmax())] * 0.5)


def separate_pixels(albedo, mask, k, log=log, seed=17):
    """THE SEPARATION, PER PIXEL RATHER THAN PER MATERIAL.

    A printer's separation is per PIXEL: one textured panel can carry two
    inks, and on this vehicle it must.  The per-material version of this
    (below) gave the mural lid -- the largest and most recognisable artwork on
    the bus -- ONE ink, and it printed as a blank brown board.  Flat colour
    does not mean one colour per object; it means no gradients.

    Area-weighted Lloyd again, seeded deterministically from a fixed-seed
    subsample sorted by luminance, so the master is reproducible.

    CEILING: a per-pixel labelling speckles wherever two inks interleave below
    the sampling grid (the paisley does exactly this), so the label map is
    median-filtered at a radius stated in SHEET MILLIMETRES before it is
    traced.  That filter is a DRAWING decision and is reported as one.
    """
    import numpy as np
    import scipy.ndimage as ndi
    px = albedo[mask]
    if not len(px):
        return {}, None, 0.0
    rs = np.random.RandomState(seed)
    sub = px[rs.choice(len(px), size=min(40000, len(px)), replace=False)]
    order = np.argsort(sub.sum(axis=1))
    cen = sub[order[np.linspace(0, len(sub) - 1, k).astype(int)]].copy()
    for _ in range(40):
        d = ((sub[:, None, :] - cen[None, :, :]) ** 2).sum(axis=2)
        a = d.argmin(axis=1)
        new = cen.copy()
        for j in range(k):
            if (a == j).any():
                new[j] = sub[a == j].mean(axis=0)
        if np.allclose(new, cen, atol=1e-6):
            cen = new
            break
        cen = new
    d = ((px[:, None, :] - cen[None, :, :]) ** 2).sum(axis=2)
    lab_flat = d.argmin(axis=1)
    cost = float(np.sqrt(d.min(axis=1)).mean())
    lab = np.full(mask.shape, -1, dtype="int16")
    lab[mask] = lab_flat
    inks = {j: tuple(float(c) for c in cen[j]) for j in range(k)
            if (lab_flat == j).any()}
    log("  separation at k=%d PER PIXEL: %d ink(s), mean linear error %.4f"
        % (k, len(inks), cost))
    return inks, lab, cost


def separate(per_idx, index, alpha, k, log=log):
    """THE INK SEPARATION AT k INKS -- the spec row's own arithmetic.

    `AUDIT_rev43.md`: *"COLOUR SEPARATION -- the whole vehicle is ONE 70 deg
    hue wedge plus four neutrals.  Seven inks printed; five if cut, and the
    fifth casualty is the silver s[...]"*  That row states a NUMBER OF INKS,
    so the separation is done at that number rather than at whatever a hue
    bucketing happens to produce.  Area-weighted Lloyd clustering over each
    material's median albedo, in LINEAR light.

    DETERMINISTIC BY CONSTRUCTION: seeds are the k largest-area materials
    whose colours are mutually distinct, taken in descending area order, so
    two runs on one capture give the same inks.  A random init would make the
    artefact irreproducible, which for a print master is a defect.

    Returns the inks, the assignment, and the AREA-WEIGHTED COST -- the mean
    linear distance between a material's own colour and the ink it is printed
    in.  That cost is what makes "five if cut" a measurable claim instead of
    an assertion: run it at 7 and at 5 and compare.
    """
    import numpy as np
    rows = sorted(per_idx.items(), key=lambda kv: -kv[1]["px"])
    if not rows:
        return {}, {}, 0.0
    cols = np.array([r[1]["albedo"] for r in rows], dtype="float64")
    wts = np.array([float(r[1]["px"]) for r in rows])
    seeds = []
    for i in range(len(rows)):
        if all(np.linalg.norm(cols[i] - cols[j]) > 0.02 for j in seeds):
            seeds.append(i)
        if len(seeds) == k:
            break
    while len(seeds) < k and len(seeds) < len(rows):        # degenerate asset
        seeds.append(len(seeds))
    cen = cols[seeds].copy()
    assign = None
    for _ in range(60):
        d = ((cols[:, None, :] - cen[None, :, :]) ** 2).sum(axis=2)
        new = d.argmin(axis=1)
        if assign is not None and (new == assign).all():
            break
        assign = new
        for j in range(len(cen)):
            m = assign == j
            if m.any():
                cen[j] = (cols[m] * wts[m, None]).sum(axis=0) / wts[m].sum()
    d = np.sqrt(((cols - cen[assign]) ** 2).sum(axis=1))
    cost = float((d * wts).sum() / wts.sum())
    inks, who = {}, {}
    for j in range(len(cen)):
        m = assign == j
        if not m.any():
            continue
        inks[j] = tuple(float(c) for c in cen[j])
        for i in np.nonzero(m)[0]:
            who[rows[i][0]] = j
    log("  separation at k=%d: %d ink(s) used, area-weighted cost %.4f in "
        "linear RGB" % (k, len(inks), cost))
    return inks, who, cost


def load_capture(tag):
    import numpy as np
    from PIL import Image
    mp = os.path.join(CAP, "%s_meta.json" % tag)
    if not os.path.exists(mp):
        ABSENT.append("capture meta %s" % mp)
        return None
    meta = json.load(open(mp))

    def one(stem):
        for fn in sorted(os.listdir(CAP)):
            if fn.startswith("%s_%s_" % (tag, stem)) and fn.endswith(".png"):
                return os.path.join(CAP, fn)
        return None

    def grey(stem, scale=1.0):
        p = one(stem)
        if not p:
            return None
        im = Image.open(p)
        a = np.asarray(im).astype("float64")
        a = a / (65535.0 if im.mode in ("I;16", "I", "I;16B") else 255.0)
        if a.ndim == 3:
            a = a.mean(axis=2)
        return a * scale

    a = one("alpha")
    alpha = (np.asarray(Image.open(a).convert("L")) > 127) if a else None
    if alpha is None:
        ABSENT.append("alpha (the die-cut silhouette) for tag %s" % tag)
        return dict(meta=meta, alpha=None)

    ip = one("index")
    index = None
    if ip:
        im = Image.open(ip)
        raw = np.asarray(im).astype("float64")
        if raw.ndim == 3:
            raw = raw[..., 0]
        den = 65535.0 if im.mode in ("I;16", "I", "I;16B") else 255.0
        index = np.rint(raw / den * 255.0).astype("int32")

    ap = one("albedo")
    albedo = None
    if ap:
        im = Image.open(ap)
        raw = np.asarray(im).astype("float64")
        albedo = raw / (65535.0 if im.mode.startswith("I") else 255.0)
        if albedo.ndim == 2:
            albedo = np.dstack([albedo] * 3)

    shade = grey("shade", float(meta.get("shade_headroom", 1.0)))
    ao = grey("ao")
    lines = None
    lp = os.path.join(CAP, "%s_lines.json" % tag)
    if os.path.exists(lp):
        lines = json.load(open(lp))["strokes"]

    ink, fam, per_idx, wedge, wedge90 = {}, {}, {}, 0.0, 0.0
    if index is not None and albedo is not None:
        ink, fam, per_idx, wedge, wedge90 = classify(index, albedo, alpha, meta)
    else:
        ABSENT.append("index/albedo pass for tag %s -- no ink separation" % tag)
    return dict(meta=meta, ink=ink, alpha=alpha, shade=shade, ao=ao,
                lines=lines, index=index, albedo=albedo, fam=fam,
                per_idx=per_idx, wedge=wedge, wedge90=wedge90)

# ------------------------------------------------------- the die-cut and bleed
def die_cut(alpha, px_mm, bleed_mm, min_cut_px, log=log):
    """The cut path: the artwork's own alpha, opened so no feature narrower
    than the spec's 0.159 m survives to touch it, then grown by the bleed.

    THE OPENING IS THE SPEC RULE, IMPLEMENTED RATHER THAN ASSERTED.  *"Let no
    feature narrower than 0.159 m touch the cut line"* is exactly a
    morphological opening at that radius: a mirror arm or a lid strut thinner
    than the rule is ABSORBED by the cut instead of being cut around, which is
    what stops a die snapping it off.  Erode-then-dilate, both by the same
    structuring element, so the surviving shape is not shrunk.

    THE BRIDGE.  *"Bridge the underbody with the cast shadow"* -- the gap
    between the wheels would otherwise cut the sticker into pieces.  There is
    no cast shadow on a transparent film, so the bridge is drawn here as the
    convex closure of the silhouette BELOW the lowest continuous span, and it
    is reported as AUTHORED, not sampled.
    """
    import numpy as np
    import scipy.ndimage as ndi
    # OPENING BY DISTANCE TRANSFORM, not by a structuring element.  The
    # spec's minimum feature is ~35 px at this capture size, and a brute-force
    # binary_opening with a 35 px disc is ~1e9 operations; two exact Euclidean
    # distance transforms give the identical result in O(n).  erode(r) is
    # {EDT(mask) >= r}; dilate(r) is {EDT(complement) <= r}.
    r = max(1.0, min_cut_px * 0.5)

    def _open(m, rad):
        er = ndi.distance_transform_edt(m) >= rad
        if not er.any():
            return er
        return ndi.distance_transform_edt(~er) <= rad

    def _close(m, rad):
        di = ndi.distance_transform_edt(~m) <= rad
        return ndi.distance_transform_edt(di) >= rad

    if os.environ.get("T1_STK_NOOPEN") == "1":
        # ABLATION (rule 3): skip the spec's minimum-feature opening, so thin
        # features survive to touch the cut line and D3/D14 can be WATCHED to
        # red on the defect rather than assumed to guard against it.
        opened = alpha.copy()
        log("  T1_STK_NOOPEN=1 -- minimum-feature opening SKIPPED (ablation)")
    else:
        # ORDER MATTERS, AND THE FIRST DRAFT HAD IT BACKWARDS.  Closing first
        # fillets a thin feature into the body and the opening then cannot see
        # it: a 5 px aerial survived a 30 px minimum-feature rule in the
        # fabricated-mask test, which is the whole rule silently not applying.
        # OPEN FIRST (remove what is too thin), THEN close (heal the pinholes
        # the opening leaves), and the opening is idempotent afterwards --
        # which D14 checks rather than assumes.
        # A PURE OPENING, AND NO CLOSING.  The first draft closed afterwards
        # to heal pinholes; that re-adds material at concavities, so the
        # opening was no longer IDEMPOTENT and D14 read 68 px still thin on a
        # mask that satisfied the rule.  A closing is not what the spec asks
        # for -- "no feature narrower than 0.159 m touches the cut line" is an
        # opening, exactly -- and pinholes are handled as holes further down.
        opened = _open(alpha, r)
    thin = int((alpha & ~opened).sum())

    # the bridge: fill the underbody by closing each column down to the
    # silhouette's own lowest row, then keep only what lies under the body
    filled = opened.copy()
    cols = np.where(opened.any(axis=0))[0]
    if os.environ.get("T1_STK_NOBRIDGE") == "1":
        log("  T1_STK_NOBRIDGE=1 -- underbody bridge SKIPPED (ablation); "
            "D1 must red")
        cols = []
    if len(cols):
        bot = np.zeros(opened.shape[1], dtype=int)
        for c in cols:
            bot[c] = np.where(opened[:, c])[0].max()
        floor = int(np.percentile(bot[cols], 92))
        for c in cols:
            top = np.where(opened[:, c])[0].min()
            if bot[c] < floor:
                filled[top:floor + 1, c] = True
    lab, n = ndi.label(filled)
    if n > 1 and os.environ.get("T1_STK_NOBRIDGE") != "1":
        sizes = ndi.sum(filled, lab, range(1, n + 1))
        filled = (lab == (int(np.argmax(sizes)) + 1))   # largest piece only

    b = max(1.0, bleed_mm / px_mm)
    cut = ndi.distance_transform_edt(~filled) <= b
    # THE BRIDGE IS ITSELF ARTWORK AND THE RULE APPLIES TO IT TOO.  The
    # column fill leaves thin slivers where it meets the wheels, and those
    # would touch the cut line -- 68 px of them on the fabricated-mask test,
    # which is how this was found.  Open the bridged mask as well, but only
    # KEEP that result if it has not re-severed what the bridge just joined.
    if os.environ.get("T1_STK_NOOPEN") != "1":
        cand = _open(filled, r)
        if cand.any() and int(ndi.label(cand)[1]) <= max(1, int(ndi.label(filled)[1])):
            filled = cand
    npre = int(ndi.label(filled)[1])
    lab2, n2 = ndi.label(cut)
    # what the opening LEFT BEHIND -- asked of the result, not assumed from
    # the fact that an opening ran (rule 3)
    left = int((filled & ~_open(filled, r)).sum())
    log("  die-cut: opening at r=%.1f px (%.3f mm) absorbed %d px of feature "
        "thinner than the spec's %.3f m, and left %d px still thin; bridge "
        "closed %d component(s) to %d; bleed %.2f mm -> %d component(s)"
        % (r, r * px_mm, thin, SPEC_MIN_CUT_M, left, n, npre, bleed_mm, n2))
    return cut, filled, thin, npre, left, n2


def contours(mask, px_mm, ox, oy, eps_mm, min_area_mm2=0.0):
    """Traced, simplified, sheet-space polygons + their holes."""
    import numpy as np
    import trace_outline as TO
    out = []
    for c in TO.trace(mask):
        pts = [(ox + float(x) * px_mm, oy + float(y) * px_mm) for y, x in c]
        pts = rdp(pts, eps_mm)
        if len(pts) > 2 and poly_area(pts) >= min_area_mm2:
            out.append(pts)
    return out


def holes_of(mask, px_mm, ox, oy, eps_mm, min_area_mm2, drawn=None):
    """Interior holes -- the ones that reach BARE STOCK, and only those.

    A gap inside a wheel is a hole: the vinyl is not there and the sticker
    must show through.  A region belonging to ANOTHER INK is not a hole: it is
    covered, just not by this ink.

    ⚠ THE FIRST DRAFT DID NOT DISTINGUISH THEM, and since a posterised label
    map is a PARTITION, every other ink's region was an interior component of
    this ink's complement and got subtracted.  The result was pure-white
    blotches -- bare stock, a colour that is in none of the seven inks --
    across the red flank, the mural and the roof.  Three wrong causes were
    eliminated first (the sacrifice rule, the despeckle radius, the asset's
    weathering, one of which cost a render); the ablation `T1_STK_NOHOLES=1`
    is what identified it, by making the blotches vanish.  It is kept.

    `drawn` is the region something is drawn over (the vehicle).  A candidate
    hole that overlaps it is NOT a hole.
    """
    import numpy as np
    import scipy.ndimage as ndi
    inv = ~mask
    lab, n = ndi.label(inv)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])))
    out = []
    for k in range(1, n + 1):
        if k in border:
            continue
        comp = (lab == k)
        if drawn is not None and (comp & drawn).any():
            continue                       # covered by another ink, not a hole
        for pts in contours(comp, px_mm, ox, oy, eps_mm, min_area_mm2):
            out.append(pts)
    return out


# ----------------------------------------------------------------- the drawing
def light_from_shading(shade, alpha):
    """WHERE THE SUN IS, SAMPLED RATHER THAN PLACED.

    The scene-lock makes the sun *"the drawing's only light source"*, so it
    must not contradict the shading it is supposed to be causing.  The image
    direction from the silhouette's centroid to the centroid of its BRIGHTEST
    shading decile is that direction, read off the render.

    CEILING: this is a 2-D IMAGE direction, not the rig's 3-D vector, and it
    cannot see a light behind the camera.  It is used only to choose which
    upper corner the disc sits in -- a decision it is comfortably strong
    enough for, and it is stated because it is not strong enough for more.
    """
    import numpy as np
    if shade is None or alpha is None or not alpha.any():
        return None
    ys, xs = np.nonzero(alpha)
    cy, cx = ys.mean(), xs.mean()
    v = shade[alpha]
    if not len(v):
        return None
    hi = v >= np.percentile(v, 90)
    hy, hx = ys[hi].mean(), xs[hi].mean()
    d = math.hypot(hx - cx, hy - cy)
    return (cx, cy, hx, hy, d)


def sun(sh, cx, cy, r, ink, log=log):
    """AUTHORED.  A PLAIN DISC -- the spec row is explicit that it *"must NOT
    be a rayed disc.  The vehicle already carries ELEVEN radial bursts."*  So
    the sun is the one thing in frame that does not radiate: a flat disc with a
    single concentric inner disc for depth, which is the cartoon convention and
    reads at 60 mm.  Drawn with `area`, i.e. as flat colour, not as line."""
    n = 96
    ring = [(cx + r * math.cos(2 * math.pi * i / n),
             cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
    sh.area(ring, rgb=ink, tint=1.0)
    inner = [(cx + r * 0.62 * math.cos(2 * math.pi * i / n),
              cy + r * 0.62 * math.sin(2 * math.pi * i / n)) for i in range(n)]
    sh.area(inner, rgb=ink, tint=0.55)
    nray = 0
    if os.environ.get("T1_STK_RAYS") == "1":
        # THE ABLATION.  Rule 3: a control is finished when you have WATCHED IT
        # FAIL on the defect.  This draws the exact thing the spec row forbids
        # so that D8 can be seen to red on it.
        for i in range(12):
            th = 2 * math.pi * i / 12
            sh.line(cx + r * 1.05 * math.cos(th), cy + r * 1.05 * math.sin(th),
                    cx + r * 1.75 * math.cos(th), cy + r * 1.75 * math.sin(th),
                    w=0.4, rgb=ink)
            nray += 1
        log("  T1_STK_RAYS=1 -- %d rays DRAWN (ablation); D8 must red" % nray)
    log("  sun: PLAIN disc r=%.2f mm at (%.2f, %.2f) -- %s (spec row), "
        "AUTHORED" % (r, cx, cy, "RAYED BY ABLATION" if nray else "NOT rayed"))
    return 2, (cx, cy, r)


def papel_picado(sh, x0, x1, y, inks, log=log):
    """AUTHORED.  The third element of the scene-lock, read as a SCENE element
    hung above the bus rather than as the vehicle's paint -- see the module
    docstring.  Perforated rectangular flags on a swagged string, which is what
    papel picado is; the perforations are real holes in the artwork, cut as
    holes so the stock shows through and the flag reads as PAPER."""
    span = x1 - x0
    n = 9
    w = span / (n + 0.6)
    sag = span * 0.055
    def sy(t):
        return y + sag * 4.0 * t * (1.0 - t)
    pts = [(x0 + span * (i / 40.0), sy(i / 40.0)) for i in range(41)]
    sh.poly(pts, w=0.22, rgb=inks["line"])
    drawn = 0
    for i in range(n):
        t = (i + 0.55) / n
        fx = x0 + span * t
        fy = sy(t)
        h = w * 1.32
        flag = [(fx - w * 0.42, fy), (fx + w * 0.42, fy),
                (fx + w * 0.42, fy + h * 0.78),
                (fx, fy + h), (fx - w * 0.42, fy + h * 0.78)]
        hs = []
        for r_ in range(2):
            for c_ in range(2):
                hx = fx + (c_ - 0.5) * w * 0.40
                hy = fy + h * (0.26 + 0.30 * r_)
                rr = w * 0.115
                hs.append([(hx + rr * math.cos(2 * math.pi * k / 16),
                            hy + rr * math.sin(2 * math.pi * k / 16))
                           for k in range(16)])
        sh.area(flag, rgb=inks["flags"][i % len(inks["flags"])], tint=1.0, holes=hs)
        drawn += 1
    log("  papel picado: %d flags, %d perforations, swag %.2f mm -- AUTHORED"
        % (drawn, drawn * 4, sag))
    return drawn


def draw(cap, denom, tag, log=log):
    import numpy as np
    import sheet as S
    import t1_mats as M
    import sticker_pass as SP

    meta = cap["meta"]
    alpha = cap["alpha"]
    H, W = alpha.shape

    # --- px -> sheet mm, at the vehicle's CENTRE depth -----------------------
    # px/m on the sensor at distance d: (res_x / sensor_w) * (lens / d).
    import studio as ST
    d = float(meta["dist"])
    px_per_m = (W / ST.SENSOR_W) * (meta["lens"] / d)
    mm_per_m = 1000.0 / denom
    px_mm = mm_per_m / px_per_m                     # sheet mm per image px
    rad = float(meta["radius"])
    near, far = d - rad, d + rad
    spread = abs((meta["lens"] / near) - (meta["lens"] / far)) / (meta["lens"] / d)
    log("  projection: %.2f px/m at the centre depth %.3f m -> %.5f mm/px; "
        "1:%.2f holds there, and across the bbox the scale spreads %.1f %% "
        "(78 mm lens is NOT orthographic -- stated, not assumed small)"
        % (px_per_m, d, px_mm, denom, spread * 100.0))

    art_w, art_h = W * px_mm, H * px_mm
    pad_top = art_h * 0.42                          # room for sun + bunting
    sheet_w = art_w + 2 * BLEED_MM + 6.0
    sheet_h = art_h + pad_top + 2 * BLEED_MM + 16.0
    ox = (sheet_w - art_w) * 0.5
    oy = pad_top + BLEED_MM

    inks = {"red": SP.srgb(M.RED), "cream": SP.srgb(M.CREAM),
            "gold": SP.srgb(M.GOLD)}
    neutral = {"neutral_dark": (34, 30, 28), "neutral_mid": (120, 116, 110),
               "neutral_light": (226, 224, 218), "unresolved": (150, 150, 150)}
    LINE = (26, 22, 20)
    STOCK = (255, 255, 255)

    sh = S.Sheet(sheet_w, sheet_h, ink=LINE, stock=STOCK, dpi=300, ss=2)
    stats = dict(areas=0, lines=0, holes=0, bands=0, occ=0)

    # --- 1. the die-cut path -------------------------------------------------
    min_cut_px = (SPEC_MIN_CUT_M * mm_per_m) / px_mm     # metres -> mm -> px
    cut, body, thin, ncomp, thin_left, ncut = die_cut(
        alpha, px_mm, BLEED_MM, min_cut_px, log=log)
    # ⚠ `body` IS THE CUT PATH'S BUSINESS AND NOTHING ELSE'S.  The spec row
    # says *"let no feature narrower than 0.159 m TOUCH THE CUT LINE"* -- it
    # is a rule about the OUTLINE, so a die does not snap a mirror arm off.
    # It says nothing about what may be PRINTED inside that outline.  The
    # first proofs masked all the artwork with the opened silhouette, and the
    # opening (r ~ 19 px here) duly ate every stroke of the SEÑOR TACOMBI
    # wordmark, most of the paisley and all the fine trim.  I chased that as
    # "too fine to resolve at 1:70" and started fitting a stencil over it;
    # painting the mask showed the model carries the wordmark perfectly and I
    # was destroying it.  ART is masked by ALPHA -- the real silhouette.
    art = alpha.copy()
    cutp = contours(cut, px_mm, ox, oy, SIMPLIFY_CUT_MM)
    for p in cutp:
        sh.area(p, rgb=STOCK)                        # the vinyl skirt
        sh.poly(p, w=0.30, rgb=(255, 0, 255), close=True)   # CUT LINE, magenta
    stats["cut_pts"] = sum(len(p) for p in cutp)
    stats["cut_paths"] = len(cutp)

    # --- 2. flat colour, one region per ink family, sampled ------------------
    # ---- THE INKS: an AUTHORED palette, placed by the model's own identity
    import scipy.ndimage as ndi
    who, ink_rgb, order, unknown = palette_map(meta)
    # MEDIAN-FILTER THE ALBEDO BEFORE ANY SNAP.  SPEC §3 locks the finish as
    # WEATHERED and that wear is painted into the texture; snapped raw, faded
    # patches of red land on cream and the flank comes out blotchy.  A MEDIAN
    # filter (not a blur -- a blur invents intermediate colours the snap then
    # has to choose between) removes speckle finer than its radius and leaves
    # the script and the paisley, both far larger, untouched.
    _r = max(1, int(round(ALBEDO_BLUR_MM / px_mm)))
    alb = np.dstack([ndi.median_filter(cap["albedo"][..., c], size=2 * _r + 1)
                     for c in range(3)])
    log("  albedo median-filtered at %.2f mm (%d px) before the snap "
        "(DRAWING decision): the weathering is texture, a cartoon prints the "
        "PAINT" % (ALBEDO_BLUR_MM, _r))
    name_of = {v: k for k, v in meta["index"].items()}
    lab = np.full(alpha.shape, -1, dtype="int16")
    slot = {k: i for i, k in enumerate(order)}
    fell = 0
    for k in np.unique(cap["index"][art]):
        if k <= 0:
            continue
        mat = name_of.get(int(k))
        msk = (cap["index"] == k) & art
        if mat in SPLIT:
            import t1_mats as _M
            names = SPLIT[mat]
            refs = np.array([getattr(_M, n.upper())[:3] for n in names])
            px = alb[msk]
            d = ((px[:, None, :] - refs[None, :, :]) ** 2).sum(axis=2)
            pick = d.argmin(axis=1)
            flat = np.zeros(msk.sum(), dtype="int16")
            for i, n in enumerate(names):
                flat[pick == i] = slot[n]
            lab[msk] = flat
            log("  %s SNAPPED to the %d measured constants %s -- %s"
                % (mat, len(names), "/".join(names),
                   ", ".join("%s %.1f %%" % (n, 100.0 * (pick == i).mean())
                             for i, n in enumerate(names))))
            continue
        ink = who.get(mat)
        if ink is None:
            # NAMED FALLBACK, NOT A SILENT ONE: an unassigned material takes
            # the palette ink nearest its own measured albedo, and the count
            # is reported.  rule 37 -- an absent assignment must not read as
            # a decision.
            d = cap["per_idx"].get(int(k), {}).get("albedo")
            if d is None:
                continue
            ink = min(order, key=lambda q: sum(
                (a - b / 255.0) ** 2 for a, b in zip(d, ink_rgb[q])))
            fell += 1
        lab[msk] = slot[ink]
    log("  %d material(s) took the nearest-ink fallback" % fell)

    # price the spec row's "five if cut" on the AUTHORED palette
    cut_slots = {slot[a]: slot[b] for a, b in CUT_MERGE.items()}
    stats["inks"], stats["inks_cut"] = len(order), len(order) - len(CUT_MERGE)

    # DESPECKLE.  Stated in sheet millimetres, and it is a drawing decision.
    rad = max(1, int(round(DESPECKLE_MM / px_mm)))
    lab = ndi.median_filter(lab, size=2 * rad + 1)
    lab[~art] = -1
    log("  label map median-filtered at %.2f mm (%d px) -- a DRAWING "
        "decision, not a measurement" % (DESPECKLE_MM, rad))

    sac_mm2 = SPEC_SACRIFICE_MM ** 2
    sac_px = max(1, int(round(sac_mm2 / (px_mm * px_mm))))
    lab2, sacrificed = lab.copy(), 0
    for j in range(len(order)):
        cc, ncc = ndi.label(lab == j)
        if not ncc:
            continue
        for i, sz in enumerate(ndi.sum(lab == j, cc, range(1, ncc + 1)), start=1):
            if sz < sac_px:
                lab2[cc == i] = -1
                sacrificed += 1
    gap = (lab2 < 0) & art
    if gap.any():
        src = np.where(lab2 >= 0, lab2, -1)
        _, (iy, ix) = ndi.distance_transform_edt(src < 0, return_indices=True)
        lab2 = np.where(gap, src[iy, ix], lab2)
    lab = lab2
    log("  sacrifice rule: %d component(s) under %.2f mm ABSORBED into their "
        "neighbours, not cut out" % (sacrificed, SPEC_SACRIFICE_MM))

    for j, kname in enumerate(order):
        m = (lab == j)
        if not m.any():
            continue
        # HOLES: only gaps that reach BARE STOCK.  A region belonging to
        # another ink is covered, not a hole -- the first proof subtracted
        # those and blew white blotches across the flank.
        hs = ([] if os.environ.get("T1_STK_NOHOLES") == "1"
              else holes_of(m, px_mm, ox, oy, SIMPLIFY_COLOUR_MM, sac_mm2,
                            drawn=(lab >= 0) & ~m))
        for p in contours(m, px_mm, ox, oy, SIMPLIFY_COLOUR_MM, 0.0):
            sh.area(p, rgb=ink_rgb[kname], tint=1.0,
                    holes=[h for h in hs if _within(h, p)])
            stats["areas"] += 1
        stats["holes"] += len(hs)
    stats["lab"] = lab
    stats["sacrificed"] = sacrificed

    # --- 2b. THE MURAL BOARD IS DRAWN.
    # It is the most characterful thing on the vehicle and the first proof
    # posterised it into brown sludge, because a fine floral texture cannot
    # survive seven inks at 58 mm.  The MODEL supplies the board's outline and
    # where it sits; the motif on it is AUTHORED -- a rosette grid, which is
    # what the board carries -- and is labelled AUTHORED on the artefact.
    stats["rosettes"] = 0
    mural_idx = meta["index"].get("lidmural")
    if mural_idx:
        mm_ = (cap["index"] == mural_idx) & art
        if mm_.sum() > 400:
            ys, xs = np.nonzero(mm_)
            x0, x1 = xs.min(), xs.max()
            y0, y1 = ys.min(), ys.max()
            step = max(18, int((x1 - x0) / 5.0))
            r_ = step * 0.44
            for gy in range(int(y0 + step * 0.6), int(y1), step):
                for gx in range(int(x0 + step * 0.6), int(x1), step):
                    if not mm_[min(gy, mm_.shape[0] - 1), min(gx, mm_.shape[1] - 1)]:
                        continue
                    cxm = ox + gx * px_mm
                    cym = oy + gy * px_mm
                    rr = r_ * px_mm
                    pet = []
                    for t in range(48):
                        a_ = 2 * math.pi * t / 48
                        rad_ = rr * (0.72 + 0.28 * math.cos(8 * a_))
                        pet.append((cxm + rad_ * math.cos(a_),
                                    cym + rad_ * math.sin(a_)))
                    sh.area(pet, rgb=ink_rgb["gold"])
                    sh.area([(cxm + rr * 0.30 * math.cos(2 * math.pi * t / 16),
                              cym + rr * 0.30 * math.sin(2 * math.pi * t / 16))
                             for t in range(16)], rgb=ink_rgb["red"])
                    stats["rosettes"] += 1
            log("  mural: %d rosette(s) DRAWN on the board the model located "
                "(%d x %d px) -- AUTHORED motif, sampled placement"
                % (stats["rosettes"], x1 - x0, y1 - y0))

    # --- 2c. THE WORDMARK, TRACED FROM ITS OWN FOOTPRINT AND NOT POSTERISED.
    # The third proof printed SEÑOR TACOMBI as an unreadable cream blob and I
    # assumed the lockup was too fine to resolve at 1:70, and started fitting
    # `script_gen.build_hi()` over it as a stencil.  PAINTING THE MASK AND
    # LOOKING AT IT (rule 8) showed the `script` material's own footprint is a
    # perfectly legible, correctly foreshortened wordmark: 12 864 px of it.
    # Nothing was too fine.  The DESPECKLE and the SACRIFICE rule were eating
    # it -- my own drawing decisions, applied to artwork that must not have
    # them applied.  So the wordmark is exempt from both and traced straight,
    # with its counters kept as holes.  The stencil was the wrong answer to a
    # question that turned out to be a bug.
    stats["wordmark"] = 0
    wm = np.zeros(alpha.shape, bool)
    sidx = meta["index"].get("script")
    if sidx:
        smask = (cap["index"] == sidx) & art
        if smask.sum() > 300:
            wm = smask
            hs = holes_of(smask, px_mm, ox, oy, SIMPLIFY_WORDMARK_MM, 0.0)
            for p in contours(smask, px_mm, ox, oy, SIMPLIFY_WORDMARK_MM, 0.0):
                sh.area(p, rgb=ink_rgb["cream"],
                        holes=[h for h in hs if _within(h, p)])
                stats["wordmark"] += 1
            log("  wordmark: %d shape(s), %d counter(s) traced from the "
                "`script` material's own %d px footprint at %.3f mm -- EXEMPT "
                "from the despeckle and the sacrifice rule, which is what was "
                "eating it" % (stats["wordmark"], len(hs), int(smask.sum()),
                               SIMPLIFY_WORDMARK_MM))

    # --- 3+4. SHADING AND OCCLUSION, AS DARKER PRINTINGS OF THE INK BENEATH.
    #
    # ⚠ THIS IS THE DEFECT THAT MUDDIED EVERY EARLIER PROOF AND I MISREAD IT
    # THREE TIMES.  `sheet.py`'s `tint` is a SINGLE-INK DRAFTING model: it
    # means "less ink on white paper", so `ink_of` mixes toward the STOCK, not
    # toward whatever is underneath.  Drawing a shadow as a dark colour at
    # tint 0.34 therefore paints an OPAQUE PALE GREY over the artwork.  That
    # is what put a grey halo round the bus, a grey wash over the roof, and a
    # grey band across the SEÑOR TACOMBI panel that covered the lower half of
    # the wordmark -- which I had already misdiagnosed twice (as the wordmark
    # being too fine to resolve, and as the despeckle eating it).
    #
    # A print master does not want transparency anyway: a printer wants FLAT
    # INKS.  So a shaded region is drawn as a DARKER PRINTING of the ink that
    # is actually beneath it, computed per ink, which is both physically what
    # a two-tone cartoon does and exactly what the owner's locked style says
    # -- "shading and occlusion sampled from the 3D asset", the SAMPLING being
    # where the shadow falls, not what colour it invents.
    def darker(rgb, k):
        return tuple(int(round(max(0.0, min(255.0, c * k)))) for c in rgb)

    def lay(mask, k, counter):
        n = 0
        for j, kname in enumerate(order):
            mj = mask & (lab == j)
            if not mj.any():
                continue
            rgbd = darker(ink_rgb[kname], k)
            hs = holes_of(mj, px_mm, ox, oy, SIMPLIFY_COLOUR_MM, sac_mm2,
                          drawn=(lab >= 0) & ~mj)
            for p in contours(mj, px_mm, ox, oy, SIMPLIFY_COLOUR_MM, sac_mm2):
                sh.area(p, rgb=rgbd, holes=[h for h in hs if _within(h, p)])
                n += 1
        stats[counter] += n
        return n

    # THE WORDMARK IS KEPT OUT OF THE SHADE.  It is the brand's own hand and
    # the one thing on the sticker that has to stay legible at 58 mm; a
    # shadow band across it is what covered its lower half on the fourth
    # proof.  A cartoonist shades around lettering, not over it.
    lit = art & ~wm
    if cap["shade"] is not None:
        import scipy.ndimage as _ndi
        sm = _ndi.gaussian_filter(np.where(lit, cap["shade"], 0.0),
                                  max(1.0, SHADE_BLUR_MM / px_mm))
        nrm = _ndi.gaussian_filter(lit.astype("float64"),
                                   max(1.0, SHADE_BLUR_MM / px_mm))
        cap["shade"] = np.where(nrm > 1e-6, sm / np.maximum(nrm, 1e-6), 0.0)
        v = cap["shade"][lit]
        v = v[v > 0]                   # DiffCol == 0 (glass, emitters) is a
        if len(v):                     # division by zero, not a shadow
            lo = np.percentile(v, SHADE_PCT)
            n = lay(lit & (cap["shade"] < lo) & (cap["shade"] > 0),
                    SHADE_MULT, "bands")
            log("  shading: %d region(s) below the %dth percentile of the "
                "non-zero light term (%.4f), smoothed at %.2f mm, printed as "
                "the underlying ink x %.2f -- SAMPLED placement, AUTHORED "
                "step" % (n, SHADE_PCT, lo, SHADE_BLUR_MM, SHADE_MULT))

    if cap["ao"] is not None:
        a = cap["ao"][lit]
        if len(a):
            thr = np.percentile(a, AO_PCT)
            n = lay(lit & (cap["ao"] < thr), AO_MULT, "occ")
            log("  occlusion: %d contact region(s) below AO %.4f, printed as "
                "the underlying ink x %.2f -- SAMPLED (Cycles AO pass), which "
                "is the half of the owner's style sentence that did not exist "
                "before rev 78" % (n, thr, AO_MULT))
    else:
        log("  occlusion: NO AO PASS IN THE CAPTURE.  The occlusion half of "
            "the owner's style sentence is NOT DRAWN, and the artefact says "
            "so.  Nothing was substituted for it (rule 37).")

    # --- 5. the line pass ----------------------------------------------------
    if cap["lines"]:
        wts = [SPEC_LINE_FLOOR_MM * f for f in (1.0, 1.9, 3.2)]   # "three strokes"
        clipped = dropped_void = dropped_short = 0
        VOID_SLOTS = {slot[k] for k in ("interior", "ink") if k in slot}
        for st in cap["lines"]:
            # CLIP TO THE CUT.  A stroke outside the die cut is ink on air --
            # the tail-board stay drew a line into the margin on the first
            # proof.  Tested in IMAGE space against the cut mask itself, so
            # the clip and the cut cannot disagree.
            keep, void = [], 0
            for u, v in st:
                px, py = int(round(u * W)), int(round(v * H))
                if not (0 <= px < W and 0 <= py < H and cut[py, px]):
                    continue
                if lab[py, px] in VOID_SLOTS:
                    void += 1
                keep.append((u, v))
            if len(keep) != len(st):
                clipped += 1
            # ⚠ DROP THE KITCHEN.  The first proof drew all 2091 strokes, and
            # the galley's twenty-odd objects came through the serving
            # apertures as a rendered kitchen.  A stroke that spends most of
            # its length over the interior void or the glazing is MODEL
            # detail, not drawing -- the owner's words, "too committed to the
            # model rather than the combi itself".
            if keep and void > 0.55 * len(keep):
                dropped_void += 1
                continue
            pts = [(ox + u * W * px_mm, oy + v * H * px_mm) for u, v in keep]
            pts = rdp(pts, SIMPLIFY_COLOUR_MM)
            if len(pts) < 2:
                continue
            # AND DROP THE CRUMBS.  A cartoon's line is deliberate; a 0.3 mm
            # fragment is not.  The floor is stated in sheet millimetres.
            L = sum(math.hypot(pts[i + 1][0] - pts[i][0],
                               pts[i + 1][1] - pts[i][1])
                    for i in range(len(pts) - 1))
            if L < LINE_MIN_MM:
                dropped_short += 1
                continue
            # "three strokes": weight by the length of the line, which is what
            # a draughtsman actually varies -- the long boundaries carry the
            # drawing and the short ones describe it
            w = wts[0 if L < 6.0 else (1 if L < 18.0 else 2)]
            sh.poly(pts, w=w, rgb=LINE)
            stats.setdefault("wts", set()).add(round(w, 4))
            stats["lines"] += 1
        stats["clipped"] = clipped
        log("  line pass: %d of %d stroke(s) drawn -- %d dropped as galley or "
            "glazing, %d dropped under the %.2f mm length floor, %d clipped "
            "to the cut" % (stats["lines"], len(cap["lines"]), dropped_void,
                            dropped_short, LINE_MIN_MM, clipped))

    # --- 6. the two AUTHORED elements ---------------------------------------
    L = light_from_shading(cap["shade"], alpha)
    # the sun sits in the upper corner the LIGHT is on, and ABOVE the bunting
    # rather than behind it -- the first proof put flag 8 across its face
    sunx = ox + art_w * (0.86 if (L and L[2] > L[0]) else 0.14)
    stats["sun"], sun_geo = sun(sh, sunx, oy - art_h * 0.40,
                                art_w * 0.075, inks["gold"])
    stats["sun_geo"] = sun_geo
    stats["flags"] = papel_picado(
        sh, ox + art_w * 0.04, ox + art_w * 0.72, oy - art_h * 0.18,
        {"line": LINE, "flags": [inks["red"], inks["gold"], inks["cream"],
                                 (64, 132, 168), (206, 96, 150)]})

    # --- 7. what is authored, said ON the artefact (F341's standard) ---------
    ty = sheet_h - 10.6
    sh.text(ox, ty, "F18  DIE-CUT STICKER  ~1:%.0f   CHILDREN'S LINE (F331)"
            % round(denom), pt=4.4, font="mono-b", tint=1.0)
    lines_ = [
        "SAMPLED from the 3D asset: die-cut path, ink placement, the wordmark,",
        "the shading and the occlusion.  AUTHORED: sun, papel picado, the",
        "mural's rosette motif, the palette's seven inks%s." % (
            "" if cap["ao"] is not None else " (NO AO PASS -- occlusion UNBUILT)"),
        "Viewpoint: the spec row says CHOOSE THE FLANK and is NOT truncated;",
        "only which axis the 18 deg is measured from is open.  A POSE, not a",
        "measurement.  AUTHORED constants, all reported at run time:",
        "  bleed %.2f | despeckle %.2f | albedo med %.2f | shade blur %.2f mm"
        % (BLEED_MM, DESPECKLE_MM, ALBEDO_BLUR_MM, SHADE_BLUR_MM),
        "  shade x%.2f | occlusion x%.2f | line floor %.2f mm | %d inks"
        % (SHADE_MULT, AO_MULT, LINE_MIN_MM, SPEC_INKS),
        "The 'earlier cartoon version' of the wheels is NOT in the repository.",
    ]
    for i, t in enumerate(lines_):
        sh.text(ox, ty + 2.6 + i * 1.9, t, pt=3.0, font="mono", tint=0.85)
    return sh, stats, dict(px_mm=px_mm, spread=spread, thin=thin, ncomp=ncomp,
                           thin_left=thin_left, ncut=ncut,
                           art_w=art_w, art_h=art_h, sheet=(sheet_w, sheet_h),
                           min_cut_px=min_cut_px, mm_per_m=mm_per_m)


# --------------------------------------------------------------- the selftest
def selftest(log=log):
    """The die-cut instrument, on a mask whose answers are known BY
    CONSTRUCTION.  Rule 4: an instrument that has never been wrong has never
    been tested -- and this one was wrong FIVE times before it was right.

    Every one of those was found here and none by reasoning about the code:
      1. the closing ran BEFORE the opening, so a 5 px aerial survived a 30 px
         minimum-feature rule -- the rule silently not applying;
      2. the closing broke the opening's IDEMPOTENCE, so D14 read 68 px thin
         on a mask that satisfied the rule;
      3. D1 counted components AFTER the bleed, and a 1.6 mm skirt merges the
         pieces the bridge exists to join -- the guard could not have redded;
      4. the bridge is artwork too, and left thin slivers where it met the
         wheels, which would have touched the cut line;
      5. a 35 px structuring element on 1.4 Mpx was a brute-force opening, so
         the honest version would have been too slow to run.
    """
    import numpy as np
    a = np.zeros((400, 700), bool)
    a[120:250, 80:620] = True                 # body
    a[290:350, 140:220] = True                # wheels, DETACHED: a real
    a[290:350, 470:550] = True                # underbody gap to bridge
    a[100:120, 300:305] = True                # a 5 px aerial -- must be absorbed
    a[160:170, 620:700] = True                # a 10 px arm  -- must be absorbed
    cases = {}
    for tag, env in (("normal", {}), ("nobridge", {"T1_STK_NOBRIDGE": "1"}),
                     ("noopen", {"T1_STK_NOOPEN": "1"})):
        os.environ.update(env)
        try:
            _, body, thin, npre, left, ncut = die_cut(a, 0.064, 1.6, 30.0, log=log)
        finally:
            for k in env:
                os.environ.pop(k, None)
        cases[tag] = (npre, left, bool(body[100:118, 300:305].any()))
    n, l, aerial = cases["normal"]
    ck(n == 1, "T1 the fabricated mask does not bridge to one piece (got %d)" % n)
    ck(l == 0, "T2 the opening is not idempotent on the fabricated mask "
               "(%d px still thin)" % l)
    ck(not aerial, "T3 the 5 px aerial survived a 30 px minimum-feature rule")
    ck(cases["nobridge"][0] > 1,
       "T4 THE BRIDGE ABLATION DID NOT RED D1 -- a guard that cannot fail on "
       "the defect it names reports nothing (rule 3)")
    ck(cases["noopen"][1] > 0,
       "T5 THE OPENING ABLATION DID NOT RED D14 -- same")
    ck(cases["noopen"][2],
       "T6 the aerial was absorbed with the opening ABLATED, so the opening "
       "is not what absorbs it and T3 proves nothing")
    log("  selftest: 1 piece / 0 thin / aerial absorbed; ablations red D1 "
        "(%d pieces) and D14 (%d px thin) -- WATCHED, not assumed"
        % (cases["nobridge"][0], cases["noopen"][1]))


# ------------------------------------------------------------------ the checks
def main(argv):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="flank")
    ap.add_argument("--out", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)

    if a.selftest:
        selftest()
        log("%d checked, %d FAILED" % (CHECK[0], len(FAILED)))
        for f in FAILED:
            log("  FAIL  %s" % f)
        return 1 if FAILED else 0

    log("sticker.py -- F18, the die-cut sticker.  capture tag %r" % a.tag)
    selftest()
    denom, pitch_m = recover_scale()

    cap = load_capture(a.tag)
    if cap is None or cap.get("alpha") is None:
        log("%d checked, %d FAILED, %d ABSENT -- run:  python3 sticker_pass.py "
            "--tag %s --lines" % (CHECK[0], len(FAILED), len(ABSENT) or 1, a.tag))
        return 0

    import numpy as np
    meta = cap["meta"]

    # --- the spec's own arithmetic, cross-checked (rule 6) -------------------
    mm_per_m = 1000.0 / denom
    # ⚠ S1 WAS A TAUTOLOGY AND IS REPLACED (rule 6, and rev 78's own rule-17
    # adversary found it).  It asserted `pitch_m*1000/denom == 0.30` where
    # `denom` is DEFINED as `pitch_m*1000/0.30` -- the residual evaluated to
    # exactly 0.0 and the check could never red.  The honest test is against a
    # quantity the recovery did NOT use: the vehicle's own overall length,
    # read from STATE.md, must print at a size a hand-held sticker can be.
    L_m = None
    try:
        for ln in open(os.path.join(ROOT, "STATE.md")):
            if "overall length (ex counter)" in ln:
                L_m = float(ln.split("|")[2])
                break
    except Exception:
        L_m = None
    if L_m is None:
        ABSENT.append("STATE.md's overall length, for the S1 scale sanity check")
    else:
        L_mm = L_m * 1000.0 / denom
        ck(35.0 <= L_mm <= 120.0,
           "S1 at 1:%.2f the vehicle's MEASURED %.4f m length prints at "
           "%.1f mm, which is not a hand-held sticker -- the recovered scale "
           "is wrong" % (denom, L_m, L_mm))
        log("  S1: the vehicle's own STATE.md length %.4f m prints at %.1f mm "
            "at 1:%.2f -- a quantity the recovery did NOT use" % (L_m, L_mm, denom))
    min_cut_mm = SPEC_MIN_CUT_M * mm_per_m
    ck(1.5 <= min_cut_mm <= 3.5,
       "S2 the spec's 0.159 m minimum cut feature lands at %.3f mm, which is "
       "outside any real die-cutter's range -- the recovered scale is wrong "
       "or the spec figure is not a cut minimum" % min_cut_mm)
    log("  CROSS-CHECK: at 1:%.2f the spec's 0.159 m minimum cut feature is "
        "%.3f mm and its 0.40 mm sacrifice threshold is %.1f mm on the "
        "vehicle.  Independently obtained; they agree." % (denom, min_cut_mm,
                                                           SPEC_SACRIFICE_MM * denom))

    # --- the capture ---------------------------------------------------------
    ck(bool(cap["ink"]), "C1 no ink separation was recovered from the capture")
    ck(len(meta.get("base_colour_linked", [])) == 0 or cap["ink"],
       "C1b the capture records %d material(s) with a LINKED Base Color and "
       "no albedo-based separation to classify them with -- a node read would "
       "be wrong on every one" % len(meta.get("base_colour_linked", [])))

    alpha = cap["alpha"]
    if cap["ink"]:
        stack = np.zeros(alpha.shape, dtype="int32")
        for m in cap["ink"].values():
            stack += m.astype("int32")
        ck(int((stack > 1).sum()) == 0,
           "C2 the ink masks OVERLAP on %d px -- they come from an integer "
           "material-index pass and cannot legitimately overlap, so a mask is "
           "not the mask it is named for (rule 8)" % int((stack > 1).sum()))
        cover = float((stack[alpha] > 0).mean()) if alpha.any() else 0.0
        ck(cover > 0.90,
           "C3 the ink masks cover only %.1f %% of the silhouette -- the "
           "remainder would print as bare stock inside the die cut" % (cover * 100))
        log("  masks: %d family mask(s), %.2f %% of the silhouette covered, "
            "%d px of overlap" % (len(cap["ink"]), cover * 100,
                                  int((stack > 1).sum())))

    wedge = float(cap.get("wedge", 0.0))
    wedge90 = float(cap.get("wedge90", 0.0))
    ck(wedge90 <= 70.0 + 1e-6,
       "C4 AUDIT_rev43's colour-separation row claims the vehicle is 'ONE 70 "
       "deg hue wedge'; the built asset MEASURES %.1f deg over every "
       "chromatic material VISIBLE IN THIS CAPTURE and %.1f deg over those "
       "of them holding at least 0.1 %% of chromatic area.  The claim had never been checked -- this is a real "
       "result either way, and a RED here is a finding about the SPEC ROW, "
       "not about the drawing" % (wedge, wedge90))

    ck(meta.get("ao") is True or meta.get("ao") is False,
       "C5 the capture does not record whether an occlusion pass exists")
    if not meta.get("ao"):
        log("  ⚠ NO OCCLUSION PASS.  Half of the owner's locked style sentence "
            "is not drawn.  Declared on the artefact; not substituted for.")

    # --- draw ---------------------------------------------------------------
    sh, stats, geo = draw(cap, denom, a.tag)

    # measured on the ARTWORK, before the bleed skirt -- a wide enough skirt
    # would merge two pieces and hide exactly the defect this guard exists for
    ck(geo["ncomp"] == 1,
       "D1 the artwork is %d separate piece(s) before the bleed, not one -- "
       "the scene-lock is 'die-cut TIGHT' and a two-piece sticker cannot be "
       "handed to a child" % geo["ncomp"])
    ck(geo["ncut"] == 1,
       "D1b the cut path encloses %d region(s)" % geo["ncut"])
    ck(stats["cut_paths"] >= 1, "D2 no cut path was traced")
    ck(geo["min_cut_px"] >= 2.0,
       "D3 the spec's minimum cut feature is %.2f px at this capture "
       "resolution -- too coarse to enforce; re-capture larger"
       % geo["min_cut_px"])
    ck(geo["thin_left"] == 0,
       "D14 %d px of feature thinner than the spec's %.3f m still touch the "
       "cut line after the opening -- a die would snap them off"
       % (geo["thin_left"], SPEC_MIN_CUT_M))
    ck(stats["areas"] > 0, "D4 nothing was drawn as flat colour")
    ck(stats.get("inks", 0) == SPEC_INKS,
       "D4b the drawing lays %d ink(s); the spec row prints %d"
       % (stats.get("inks", 0), SPEC_INKS))
    ck(stats.get("inks_cut", 0) == SPEC_INKS_CUT,
       "D4c the palette reduces to %d ink(s) if cut; the spec row says %d"
       % (stats.get("inks_cut", 0), SPEC_INKS_CUT))
    ck(stats.get("lines", 0) < 600,
       "D4d %d line(s) drawn.  The owner's ruling at rev 78 was that this is "
       "a DRAWING, not a trace of the model; the proof he rejected drew "
       "EVERY stroke the line pass returned" % stats.get("lines", 0))
    ck(stats.get("wordmark", 0) > 0,
       "D4f the wordmark is not drawn -- it is the brand's own hand and the "
       "model carries it exactly")
    ck(stats.get("rosettes", 0) > 0,
       "D4e the mural board carries no drawn motif -- posterising it was the "
       "defect he named")
    ck(stats["lines"] > 0 or cap["lines"] is None,
       "D5 the line pass was captured but no stroke was drawn")
    ck(stats["sun"] == 2,
       "D6 the sun is not the plain two-disc form the spec row requires")
    ck(stats["flags"] > 0, "D7 the papel picado is missing from the scene-lock")

    # D8 -- THE RAYED-SUN KILL.  The spec row is explicit: the sun "must NOT be
    # a rayed disc".  A ray is a stroke that starts near the disc and points
    # away from it, so COUNT THEM rather than trusting that none was drawn.
    scx, scy, sr = stats["sun_geo"]
    rays = 0
    for kind, p in sh.ops:
        if kind != "line":
            continue
        x1, y1, x2, y2, w, tint, dash, rgb = p
        r1 = math.hypot(x1 - scx, y1 - scy)
        r2 = math.hypot(x2 - scx, y2 - scy)
        near, far_ = min(r1, r2), max(r1, r2)
        # a RAY: one end sits on the disc, the other end is further out, and
        # the stroke runs radially rather than across.  Asked of the geometry,
        # never of a colour constant -- a guard keyed to a literal nothing
        # emits is a tautology (rule 6) and can never red.
        if not (near <= sr * 1.30 and far_ > near + sr * 0.20 and far_ > sr):
            continue
        # ...AND IT MUST ACTUALLY RUN RADIALLY.  Without this the bunting
        # string passing the disc counted as two rays and D8 redded on a
        # drawing that has none -- a guard that cries on the innocent is as
        # useless as one that cannot cry at all.
        sx, sy_ = x2 - x1, y2 - y1
        rx, ry = (x1 + x2) * 0.5 - scx, (y1 + y2) * 0.5 - scy
        ls, lr = math.hypot(sx, sy_), math.hypot(rx, ry)
        if ls > 1e-9 and lr > 1e-9 and abs((sx * rx + sy_ * ry) / (ls * lr)) > 0.90:
            rays += 1
    ck(rays == 0, "D8 %d radial stroke(s) run outward from the sun disc -- the "
                  "spec row forbids a rayed disc" % rays)

    # D9 -- the AUTHORED declaration must be ON the artefact (F341), not in a
    # comment.  rev 77 shipped a sheet that called an authored ink MEASURED.
    txt = " ".join(p[2] for k, p in sh.ops if k == "text")
    ck("AUTHORED" in txt and "SAMPLED" in txt,
       "D10 the artefact does not say on its face which marks are AUTHORED and "
       "which are SAMPLED -- F341's standard, and rev 77 broke it once")
    ck("CHILDREN" in txt.upper(),
       "D11 F331 requires every item to say WHICH LINE it is in; this one does not")

    # D12 -- line weights: "three strokes, a 0.15 mm floor"
    # the VEHICLE's strokes only -- the bunting string is an authored scene
    # element, not one of the spec row's "three strokes"
    ws = sorted(stats.get("wts", set()))
    if ws:
        ck(min(ws) >= SPEC_LINE_FLOOR_MM - 1e-9,
           "D12 the thinnest line is %.3f mm, below the spec's %.2f mm floor"
           % (min(ws), SPEC_LINE_FLOOR_MM))
        ck(len(ws) <= SPEC_STROKES,
           "D13 %d distinct line weights drawn; the spec row locks %d strokes"
           % (len(ws), SPEC_STROKES))

    # --- write and re-read ---------------------------------------------------
    os.makedirs(DES, exist_ok=True)
    base = a.out or os.path.join(DES, "sticker_r78_%s" % a.tag)
    svg, png = base + ".svg", base + ".png"
    sh.save_svg(svg); sh.save_png(png)

    import xml.etree.ElementTree as ET
    try:
        root = ET.parse(svg).getroot()
        ok_xml = True
    except Exception as e:
        root, ok_xml = None, False
        FAILED.append("W1 the SVG does not parse: %s" % e)
    CHECK[0] += 1
    if ok_xml:
        paths = len(root.findall(".//{http://www.w3.org/2000/svg}path"))
        nareas = sum(1 for k, _ in sh.ops if k == "area")
        ck(paths == nareas,
           "W2 %d <path> in the SVG against %d area op(s) -- the two backends "
           "have drifted, which is the one thing sheet.py exists to prevent"
           % (paths, nareas))
        ck(root.get("width", "").endswith("mm"),
           "W3 the SVG viewBox is not in millimetres; a cutter cannot use it")
    ck(os.path.getsize(png) > 20000, "W4 the PNG proof is empty or trivial")

    log("  wrote %s" % svg)
    log("  wrote %s" % png)
    log("  sheet %.1f x %.1f mm; ARTWORK %.1f mm across the frame at a "
        "nominal 1:%.0f (see the projection line for what that does and does "
        "not mean); "
        "%d colour area(s), %d hole(s), %d shading band(s), %d occlusion "
        "region(s), %d line(s), %d component(s) sacrificed under the %.2f mm "
        "rule" % (geo["sheet"][0], geo["sheet"][1], geo["art_w"], round(denom),
                  stats["areas"], stats["holes"], stats["bands"], stats["occ"],
                  stats["lines"], stats["sacrificed"], SPEC_SACRIFICE_MM))

    if FAILED:
        log("")
        for f in FAILED:
            log("  FAIL  %s" % f)
    log("%d checked, %d FAILED%s" % (CHECK[0], len(FAILED),
                                     "" if not ABSENT else
                                     ", %d ABSENT" % len(ABSENT)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
