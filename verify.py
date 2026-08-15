"""Regression guard — asserts the machine-checkable rows of SPEC.md sec.9 (rev 4).

Design note: rev 3's version counted *panes* to decide whether the serving bays
existed. That is not a test of the shell — a boolean that silently rolled back
would leave the panes untouched and the guard green. Row 4 below now tests the
sheet metal itself.
"""
import bpy, bmesh
from mathutils import Vector

TOL = 0.025
import t1_core as _T

# SPEC rev 4 sec.2 — factory-sourced 1963 T1 hard points
#
# FRAME. MEASURED 2026-08-09, and the note that used to sit here was wrong.
# build.py calls run() at line 354, AFTER step 8b has already subtracted
# RIDE_DROP from every vertex, so the mesh run() sees is DROPPED. Two
# consequences, and they pull in opposite directions:
#
#  1. SPEC["H"] = 1.941 is a DROPPED figure and must stay as it is. It is
#     compared against a height measured off the same dropped mesh (1.936).
#     "Correcting" it to 1.941 - RIDE_DROP is what produced a phantom +60 mm
#     failure once. Do not.
#  2. Every probe coordinate taken from AUTHORED geometry -- Z_SILL, Z_HEAD,
#     DOOR_GAP, REAR_Z, WS_MID -- is in the UN-DROPPED frame and MUST have
#     RIDE_DROP subtracted before it is used to aim a ray. Skipping that on a
#     5.5 mm shut line reads 26 % open instead of 100 %.
#
# _frame_dz() below carries (2) so the two never get confused again.
# rev 16.  L IS NO LONGER THE FACTORY FIGURE, and it is not re-typed either.
#
# 4.290 came from the 1950-67 T1 catalogue ("overall length 4280 mm over
# bumpers").  The rear overhang has now been MEASURED dimensionlessly off
# ref_side.jpg -- 0.3412 +- 0.0015 of the wheelbase against 0.4200 built -- and
# it is 235 mm shorter than the catalogue.  The standing instruction on this
# project is to never correct this vehicle toward the VW factory catalogue, so
# the measurement wins and the target follows it.
#
# Written as an EXPRESSION, not as 4.055: it is the catalogue length minus the
# tail correction actually applied in t1_core, so re-measuring the overhang can
# never leave this row asserting a stale number.  The forward end of L is still
# X_NOSE, which has never been measured -- the lamppost at ref_side.jpg columns
# 62-79 occludes it and has produced three separate confident wrong numbers --
# so this row is a REGRESSION CATCHER, not a measurement.  The measurement is
# the new overhang row below, which is the quantity that was actually observed.
SPEC = dict(L=4.290 - (_T.O_OLD - _T.O_NEW), W=1.750, H=1.941, WB=2.400,
            TRACK_F=1.369, TRACK_R=1.359, TYRE_D=0.665)

# ---------------------------------------------------------------------------
# H_ROOF -- RETIRED AS AN ACCURACY TARGET by the owner, rev 22.  READ THIS
# BEFORE RE-ADDING IT TO SPEC.
#
# rev 8 put H_ROOF = 1.960 in the accuracy dict: REF_MEASUREMENTS sec.2.3
# measures 1.960 on the fixed roof aft of the lid opening at the rear-axle
# station, and the rake was tuned to reproduce it.  It produced the standing
# "+23 mm" warn from rev 16 onward.
#
# WHY IT WAS RETIRED, and this is a chain of withdrawals, not a preference:
#   (a) REF sec.1 derived 1.960 from the GROUND LINE, which SPEC sec.10.11
#       BANS -- three features placed from that datum land low by the same sign
#       and magnitude, a ~70 mm common-mode error.  rev 16 additionally found
#       the HUB-referenced chain carries the same disease at ~29 mm, so the
#       obvious substitute datum is not clean either.
#   (b) 1.960's ONLY ground-line-free confirmation was LOFT_GROUND sec.1.2's
#       1.9621.  SPEC sec.10.34 WITHDREW that reading's interpretation -- the
#       "proud strip 253.21" IS the roof -- without noting that it was 1.960's
#       only escape from the banned datum.  rev 18 (sec.10.48) found that.
#   (c) So the target has no admissible derivation left.  A guard whose target
#       is underived cannot report accuracy; it can only report disagreement
#       between the model and a number of unknown provenance.
#
# WHAT WAS DELIBERATELY *NOT* DONE: H_ROOF was NOT re-valued to the mesh probe.
# The owner rejected that explicitly and he was right -- a guard set to the
# model's own current reading compares the model to itself and can never fail,
# and it would clear a standing warn by tuning.  Both are forbidden here.
#
# STATE THIS PLAINLY WHEREVER THE WARN'S DISAPPEARANCE IS REPORTED:
#   THE WARN IS GONE BECAUSE THE TEST WAS WITHDRAWN, NOT BECAUSE THE MODEL
#   IMPROVED.  The mesh did not move.  Guards were 0 fail / 1 warn before this
#   change and 0 fail / 0 warn after it, with every other figure identical.
#
# The absolute roof height of the real vehicle is now an OPEN, UNMEASURED
# quantity.  Closing it needs a head-on rear or front elevation from roof
# height or above -- the same photograph that would close CREAM.
H_ROOF_RETIRED = 1.960

# The probe survives as a REGRESSION CATCHER, exactly as rev 18 did for
# STATE.md's height row.  It asserts NOTHING about the real vehicle.  It
# asserts only that the modelled roof crown at the rear axle has not MOVED.
#
# Baseline WATCHED PRINT on a clean rev-22 tree, both levels, before it was
# written here:  SUB=1 -> 1.9835,  SUB=2 -> 1.9833  (0.2 mm apart).
# Band +-5 mm, which both levels clear by ~4.8 mm.  If a future change trips
# this row, THAT IS THE GUARD WORKING: move the geometry back, or re-baseline
# deliberately and say so -- never widen the band.
H_ROOF_REGRESSION = 1.9835
H_ROOF_REGRESSION_BAND = 0.005
# rev 13.  The rake came down from 33.0 to 17.75 mm/m on a scale-free
# hub-referenced measurement (t1_core), which drops the rear axle 28 mm and
# takes the crown from 1.923 to 1.894 -- so the raw residual against REF 2.3's
# 1.960 grows from -37 mm to -66 mm.  That is NOT the rake getting worse; it is
# a SECOND, separately measured defect becoming visible now that the first is
# out of the way.
#
# The transverse roof section is 3.9x too flat.  Measured two ways, two frames,
# two physics: crown-minus-drip-rail at the same column in ref_side.jpg gives
# 0.188 +/- 0.015 m, and the open lid's forward CUT EDGE in ref_workshop.jpg --
# which is literally a transverse section of the roof -- fits a circle at
# rms 0.49 px against a straight line's 4.51 px, giving crown R 2.45 +/- 0.15 m.
# The model's `roof_z` parabola is R 9.65 m and 0.0832 m gutter-to-crown.  So the
# model's crown sits 0.098 +/- 0.010 m BELOW where its own gutter puts it.
#
# Encoded as a named constant rather than by widening the band, because a band
# wide enough to swallow it would also swallow a rake regression.  The raw
# number is still logged every run so the defect can never go quiet, and
# DOME_DEFICIT MUST BE DRIVEN TO ZERO when the roof section is rebuilt -- at
# which point this guard tightens automatically.
# rev 16: DRIVEN TO ZERO.  The transverse section was re-fitted jointly with
# the roof edge (SPEC sec.10.34) -- RT_ALL 0.054 -> 0.0949 and CR_ALL 0.032 ->
# 0.1179, D = 0.2128 against LOFT_GROUND sec.1.3's independently measured
# 0.2116 +- 0.035.  The dome is now MODELLED, so there is no deficit left to
# carry and this guard tightens automatically, as its own comment promised.
DOME_DEFICIT = 0.000
RIDE_DROP_SPEC = 0.065        # rev 6: the bus IS lowered. See SPEC sec.2.
# rev 18: SPEC 10.9 / t1_core:120 -- the rake, re-derived four ways in rev 13,
# with 33.0 mm/m rejected at 4.5 sigma.  NOT a new constant: it is the locked
# value this file previously did not guard at all.
RAKE_SPEC = 0.01775

BANNED = ("bed", "gate", "canopy", "fascia", "post")   # pickup-era geometry

# Material names this project has ever used for a reading SPEC sec.0.2 retires.
# Only names that are actually MATERIAL keys belong here -- sec.0.2 is prose, so
# the mapping from a retired reading to the datablock that implemented it has to
# be stated once. The guard below reads sec.0.2 and warns about any retired
# reading whose token is NOT in this map, which is what stops the next `canvas`.
_RETIRED_MAT = {
    "whitewall": "whitewall tyres",
    "wheelred": "red rims",
    "timber": "timber plank counter",
    "canvas": "folding canvas ragtop",
}


# Number of bullets in SPEC sec.0.2 that _RETIRED_MAT has been reviewed against.
# Bump this ONLY together with a review of the map above.
_RETIRED_BULLETS_REVIEWED = 29     # rev 24: 16 -> 29, §0.2b added. WATCHED PRINT.


def _retired_material_tokens():
    """Material names banned because SPEC sec.0.2 retires the reading."""
    return set(_RETIRED_MAT)


def _retired_section_drift():
    """Has SPEC sec.0.2 gained a retired reading nobody mapped to a material?

    The first attempt at this scanned sec.0.2 for material names directly. That
    cannot work: every bullet is "<retired reading> — <correction>", and the
    material names are ordinary English words that appear on BOTH sides.
    'gold side script — it is silver' contains 'script'; 'chrome bumpers — they
    are painted cream' contains 'chrome' and 'cream'. It flagged six correct
    materials as retired.

    So the map stays explicit and reviewed, and this checks only that it has
    been reviewed against the CURRENT sec.0.2. That closes the actual failure --
    'canvas' was retired in the spec in rev 4 and nobody armed the guard, so it
    shipped for three revisions -- without inventing false positives.
    """
    import os as _os
    spec = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "SPEC.md")
    # rev 24, SPEC 10.67 -- THIS PARSE WAS SUBSTRING-BASED AND I DEFEATED IT BY
    # ACCIDENT.  It read `txt.split("## 0.2")[1].split("\n## ")[0]`.  Adding a
    # subsection headed `### 0.2b` put the substring "## 0.2" into the file a
    # SECOND time (`### 0.2b`[1:7] == "## 0.2"), so `[1]` became the text
    # between the two headings and the guard silently went back to reading only
    # the original 16 bullets while the section had grown to 30.  It printed a
    # reassuring "16" -- exactly the shape of a guard that cannot fail.  Caught
    # by watching the count print, per this repo's own acceptance-test rule.
    # Line-anchored now: find the heading LINE, read to the next `## ` LINE.
    try:
        lines = open(spec, encoding="utf-8").read().splitlines()
    except Exception:
        return None
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith("## 0.2"):
            start = i + 1
            break
    if start is None:
        return ("SPEC 0.2 heading not found -- the retired-reading drift guard "
                "could not run. It declines rather than passing silently.")
    end = len(lines)
    for j in range(start, len(lines)):
        if lines[j].startswith("## ") and not lines[j].startswith("## 0.2"):
            end = j
            break
    sec = "\n".join(lines[start:end])
    n = sum(1 for ln in sec.splitlines() if ln.strip().startswith("- "))
    if n != _RETIRED_BULLETS_REVIEWED:
        return (f"SPEC 0.2 now has {n} retired readings, last reviewed at "
                f"{_RETIRED_BULLETS_REVIEWED}. Check verify._RETIRED_MAT maps "
                "every one that was implemented as a material, then bump "
                "_RETIRED_BULLETS_REVIEWED. This is how 'canvas' shipped for "
                "three revisions after the spec retired it.")
    return None
# rev 24, SPEC 10.67 -- THE GUARD THE sec.0.2 MECHANISM CANNOT BE.
#
# sec.10.64 found four RETIRED values still published in SPEC as "locked", one
# of them (`W_ART = 0.30`) 3.3x off the live value for thirteen revisions.  The
# structural cause was recorded as "sec.0.2 has gained no entry since rev 4",
# and rev 24's work item 2 was to add sec.10's retirements there.  THAT BRIEF IS
# REFUTED (see the comment at the material loop): sec.0.2's guard reads material
# NAMES, and a retired NUMBER is not a material name.  Adding bullets buys a
# forced review, not detection.
#
# What detects it is this: a retired literal must not appear in SPEC.md except
# in a context that MARKS it retired.  Every entry below was confirmed by hand
# against the live module before being added -- a citation is a claim too.
#
# Each row: (retired literal as it appears in SPEC, live value, live symbol,
#            the section that retired it).
_RETIRED_VALUES = (
    ("196, 106, 36", "(196,49,36)", "t1_mats.RED",        "10.12/10.3"),
    ("z = 1.402",    "1.372",       "t1_shell.Z_SILL",    "10.2"),
    ("z = 1.798",    "1.775",       "t1_shell.Z_HEAD",    "10.2"),
    ("0.507 / 0.516 / 0.526", "equal 0.5155", "t1_shell.BAY_W", "10.29/10.47"),
    ("0.0330",       "0.017750",    "t1_core.RAKE_DZDX",  "10.29"),
    # ---- rev 25, SPEC 10.69.  Nine more.  Each was verified by hand against
    # THREE things before its row was written: the SPEC line, the LIVE value
    # read out of the CODE (never out of other prose), and the sec.10 sentence
    # that retires it.  A read-only subagent proposed "~12"; four of its
    # candidates were refuted or mislocated and are recorded in 10.69 rather
    # than added here -- a subagent's finding is a claim, not a measurement.
    ("⌀ ≈ 0.370",   "0.2800",      "build.ROUNDEL_D",    "10.22"),
    ("centre z ≈ 1.130", "1.0170 AG", "build.ROUNDEL_Z_AG", "10.22"),
    ("x = +2.108 / −2.108", "+2.108 / −1.8730", "t1_core.X_TAIL", "10.35"),
    ("Not modelled yet", "modelled since rev 8", "t1_core.rake_drop", "10.9"),
    ("**+0.820**",   "BAYS[0] +0.41425..+0.92975", "t1_shell.BAYS", "10.29/10.47"),
    ("1.046 m wide", "1.0175",      "t1_shell.BAYS/X_TAIL", "10.29/10.35"),
    ("composited to **pure white**", "headroom", "post.BACKDROP", "10.32"),
    ("fish-eye",     "bullet pod",  "t1_detail.bullet_indicator", "10.22"),
    ("Overall height measures **1.960**", "RETIRED as a target",
     "verify.H_ROOF_RETIRED", "10.59"),
    ("`RIDE_DROP` ≠ 0 → FAIL", "== 0.0650 exactly",
     "verify.RIDE_DROP_SPEC", "rev 5 log"),
)

# A literal is EXEMPT where the line itself says it is retired.  Matching on the
# LINE, not the file, is deliberate: a file-wide "the word RETIRED appears
# somewhere" test would pass on every one of the four defects sec.10.64 found.
_RETIRED_OK = ("RETIRED", "retired", "~~", "superseded", "SUPERSEDED",
               "REFUTED", "refuted", "withdrawn", "WITHDRAWN", "stale")


def _retired_value_drift():
    """Is a RETIRED value still published in SPEC.md as if it were live?

    Returns a list of (literal, line_no, live, symbol, sec) for every
    unstruck occurrence.  Empty list means clean.  Returns None -- never an
    empty list -- if SPEC.md cannot be read, because a probe that cannot
    answer must not answer (SPEC 10.47).
    """
    import os as _os
    spec = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "SPEC.md")
    try:
        lines = open(spec, encoding="utf-8").read().splitlines()
    except Exception:
        return None
    # A sec.10 entry QUOTES a retired value in order to retire it, so scanning
    # those sections reports the retirement itself as the defect.
    #
    # MY FIRST VERSION OF THIS CUT THE FILE AT THE FIRST `## 10.` HEADING AND
    # SCANNED EVERYTHING ABOVE IT.  That is wrong, and it fired 8 FAILs of
    # which 4 WERE ITS OWN FALSE POSITIVES: sec.10.11 through sec.10.33 are
    # `### 10.xx` headings INTERLEAVED WITH THE FRONT MATTER at lines ~321-2400,
    # while `## 10.` sits at 2473.  So the cut swept sec.10.12's and sec.10.29's
    # own bodies -- lines that exist precisely to say "was 0.0330, is 0.017750".
    # CHECK WHAT A GUARD CAN PHYSICALLY SEE, including which SECTION.
    #
    # Section-aware instead: skip any section whose heading is a sec.10 entry or
    # the change log, wherever in the file it happens to sit.
    def _is_log(h):
        h = h.lstrip("#").strip()
        # sec.0.2 IS the retirement list -- it exists to name retired values, so
        # scanning it reports every entry as the defect it is recording.  Same
        # reason sec.10 bodies and the change log are exempt.  Found when the
        # guard fired on sec.0.2b's own bullets on its first run after they were
        # added: the guard was right about the strings and wrong about the
        # section, which is the same class of error as its first section cut.
        return h.startswith("10.") or h.startswith("10 ") or \
            h.startswith("0.2") or h.lower().startswith("change log")
    # HEADING DEPTH IS LOAD-BEARING.  A sub-heading inside a sec.10 entry must
    # INHERIT its parent's exemption.  Without this, `### OPEN, unresolved:
    # rake versus the arch gap` at SPEC.md:2699 -- a subsection of `## 10.9` --
    # reset the skip and the guard fired on 2701, a line inside a sec.10 body.
    # That line IS stale (rev 23 struck 10.9's table and missed the arithmetic
    # forty lines below it), but the guard found it BY ACCIDENT, and a guard
    # that is right for the wrong reason is not a guard.  Fixed by hand instead.
    #
    # STATED CEILING: by construction this guard cannot see inside a sec.10
    # body.  It catches a retired value republished in the FROZEN front matter,
    # which is sec.10.64's defect class; it does NOT catch a sec.10 entry that
    # contradicts itself.  Nothing here should be read as covering that.
    out, skip, depth = [], False, 0
    for i, ln in enumerate(lines, start=1):
        if ln.startswith("#"):
            lvl = len(ln) - len(ln.lstrip("#"))
            if skip and lvl > depth:
                continue                      # sub-heading: inherit the skip
            skip, depth = _is_log(ln), lvl
            continue
        if skip or any(tok in ln for tok in _RETIRED_OK):
            continue
        for lit, live, sym, sec in _RETIRED_VALUES:
            if lit in ln:
                out.append((lit, i, live, sym, sec))
    return out


NEED_MATS = ("T1_paint", "cream", "chrome", "glass", "wheelcream",
             "bumpercream", "roundelred", "countercream", "script", "calidad")

# SPEC rev 4 sec.1.1 — three apertures, then SOLID sheet metal
N_BAYS_OPEN = 3
# rev 6 corrected: the window band is Z_SILL 1.372 / Z_HEAD 1.775 UN-DROPPED
# (1.307 / 1.710 above ground).  Derive the probe height instead of hard-
# coding it — the old literal 1.600 was keyed to the retired 1.402/1.798 band
# and would have silently drifted toward the head rail.
def _bay_probe_z(S):
    return (S.Z_SILL + S.Z_HEAD) / 2.0


# rear corner panel must be metal.  Bay 2's rear edge is at x = -0.960.
SOLID_PROBE_X = (-1.05, -1.30, -1.55, -1.80)

# MEASURED serving-bay edges, (rear, front) to match t1_shell.BAYS
# rev 13.  Re-measured, and BOTH the positions and the widths move.  This guard
# is STRENGTHENED, not relaxed: it still pins every edge to 1e-6, and it now
# also pins the three widths to each other, because the defect it used to
# protect ("rev-3's evenly-spaced bays are retired") turned out to be pointing
# the wrong way.
#
#   POSITION  all three sat 105 mm too far AFT, as a pure translation.
#             REF_MEASUREMENTS maps the photo as X = (495.8 - u)/211.5 and calls
#             X = 0 mid-wheelbase, but 495.8 px IS the hub midpoint and this
#             model's mid-wheelbase is x = +0.100 (axles +1.300 / -1.100).  The
#             same 100 mm is inside SPEC 10.7's "99 mm tail".  Measured centres
#             +0.672 / +0.047 / -0.598 +/- 0.015, six sub-pixel cut edges
#             anchored by ratio to the two hubs.
#   WIDTH     the bays ARE equal, at 0.5155 +/- 0.005 m.  Three exactly equal
#             bays project to 106.76 / 109.12 / 111.52 px against a measured
#             107.23 / 109.13 / 111.04 -- residuals +0.47 / +0.01 / -0.48 px.
#             SPEC 10.5's 0.507/0.516/0.525 taper is PERSPECTIVE.  rev-3's three
#             equal 0.600s stay retired: the width is 0.5155, not 0.600, so
#             "equal" was never the thing that was wrong with them.
BAY_W_SPEC = 0.5155
BAY_CX_SPEC = (0.6720, 0.0470, -0.5980)
BAYS_SPEC = tuple((cx - BAY_W_SPEC / 2.0, cx + BAY_W_SPEC / 2.0)
                  for cx in BAY_CX_SPEC)
BAND_SPEC = (1.3720, 1.7750)           # Z_SILL, Z_HEAD, UN-DROPPED
# a shut line is a 5.5 mm slot; allow a few samples to be occluded by a seal
SLOT_FRAC_MIN = 0.90


def _bounds():
    lo = Vector((1e9, 1e9, 1e9)); hi = -lo
    for ob in bpy.data.objects:
        if ob.type != 'MESH' or ob.name in ("cyc", "counter", "counter_nosing",
                                            "counter_top"):
            continue
        for c in ob.bound_box:
            v = ob.matrix_world @ Vector(c)
            lo = Vector((min(lo[i], v[i]) for i in range(3)))
            hi = Vector((max(hi[i], v[i]) for i in range(3)))
    return lo, hi


def _frame_dz(x=None):
    """z offset from the AUTHORED frame to the frame the mesh is actually in.

    build.py sets RIDE_DROP_APPLIED just after step 8b. Default to "applied"
    if the flag is missing, because that is what build.py has always done and
    an un-offset probe silently under-reports rather than failing loudly.

    rev 8: step 8b SHEARS rather than dropping, so this offset depends on the
    station. `x` is REQUIRED for any probe that aims a ray at a specific place;
    calling it bare returns the offset at t1_core.X_DROP_REF, which is only
    correct at that one station. A probe 5.5 mm wide aimed one station off is
    exactly how rev 6 read a shut line as 26 % open instead of 100 %.
    """
    try:
        import __main__
        applied = getattr(__main__, "RIDE_DROP_APPLIED", True)
    except Exception:
        applied = True
    if not applied:
        return 0.0
    return -_T.rake_drop(_T.X_DROP_REF if x is None else x)


def _roof_z_at(xq, tol=0.05):
    """Highest point of the FIXED roof at station xq (excludes the raised lids)."""
    body = bpy.data.objects.get("T1_body")
    if body is None:
        return float('nan')
    mw = body.matrix_world
    zs = [(mw @ v.co).z for v in body.data.vertices
          if abs((mw @ v.co).x - xq) < tol and abs((mw @ v.co).y) < 0.35]
    return max(zs) if zs else float('nan')


def _has_metal(body, x, z, side=1):
    """True if the shell has sheet metal at (x, z) on the given flank.

    Cast a ray inboard along -Y from well outside the body. A serving aperture
    is a hole: the first hit is then the FAR flank (loc.y on the opposite
    side) or nothing at all. Testing abs(loc.y) alone cannot tell those apart
    — it reports 0.87 either way — so the sign against `side` is what makes
    this a test rather than a coin flip.
    """
    y_start = side * 3.0
    direction = Vector((0.0, -side, 0.0))
    ok, loc, _, _ = body.ray_cast(Vector((x, y_start, z)), direction)
    if not ok:
        return False
    return loc.y * side > 0.5        # near flank sits at |y| ~ 0.86


def _flank_open(body, x, z, side):
    """True if a ray inboard at (x, z) gets past the near skin: hole or slot"""
    return not _has_metal(body, x, z, side)


def _ray_clear(body, origin, direction, dist):
    """True if the body has no surface within `dist` of `origin` along `direction`"""
    return not body.ray_cast(Vector(origin), Vector(direction).normalized(),
                             distance=dist)[0]


def _slot_frac(body, outline, side, dzf):
    """rev 8: dzf is a CALLABLE of x, not a scalar -- the shear moves the frame
    33 mm for every metre forward, and a 5.5 mm shut line probed one station off
    reads closed."""
    """fraction of samples along a flank (x, z) outline that are open slots"""
    n = sum(1 for (x, z) in outline if _flank_open(body, x, z + dzf(x), side))
    return n / max(len(outline), 1)


def _englid_frac(body, outline, dz, thru_x):
    # engine lid is at a fixed tail station, so a scalar dz is correct here
    """fraction of samples along the tail (y, z) outline that are open slots.

    Cast forward along +X from well behind the tail. A ray that is BLOCKED
    stops on the tail skin at x = X_TAIL; a ray that gets through the slot
    carries on far forward.  `thru_x` is the plane that separates the two.

    rev 18 -- THIS ROW WAS DEAD, AT EVERY REVISION, AND IT PRINTED "100 %".
    The threshold was the literal -1.95 while the docstring said "the tail
    skin sits at x ~ -2.09".  It never did: at the OLD tail station -2.1080
    the threshold was already 158 mm INBOARD of the skin, and after rev 16's
    tail re-space the skin is at -1.8730, so -1.95 sits 77 mm BEHIND THE
    ENTIRE VEHICLE and every ray that hits the tail at all scored "got
    through".  Measured: 28/28 open, and 1.0000 returned with the outline
    moved +350 mm, -300 mm, +600 mm and squeezed to 20 % of its width.

    `t1_shell.engine_lid_gap` cuts at `X_TAIL + ENGLID_CUT_DX` and EXPRESSED
    it that way.  verify kept a literal.  That is the project's own rule --
    a constant tuned against another constant must be expressed in terms of
    it -- broken inside the guard that was supposed to enforce the geometry.
    The threshold is now that same expression, passed in by the caller.
    """
    ok_n = 0
    for (y, z) in outline:
        hit, loc, _, _ = body.ray_cast(Vector((-3.0, y, z + dz)),
                                       Vector((1, 0, 0)))
        if (not hit) or loc.x > thru_x:
            ok_n += 1
    return ok_n / max(len(outline), 1)


def _arch_lip_z(body, x, side, z0, z1, step=0.0005):
    """Lowest z at station x where the flank skin exists -- i.e. the wheel-arch
    lip, MEASURED ON THE BUILT MESH.

    rev 18.  There was no such probe.  `verify` row 10's arch-to-tyre gap was
    `ARCH_R - TIRE_R`, a subtraction of two SOURCE CONSTANTS, so it returned
    41.0 mm forever no matter what the arch outline did -- and
    `ARCH_W_REAR`, `_ARCH_PROFILE`, `_arch_drop` and `rear_arch_outline`
    appear ZERO times in this file and zero times in audit.py.  Rev 16
    rebuilt the rear arch and nothing measured the result.

    Returns None if the transition is not found inside [z0, z1], so a caller
    can report "not found" rather than silently publishing an endpoint --
    the `or -9` failure audit.py's own rev-7 comment warns about.
    """
    z = z0
    prev = _has_metal(body, x, z, side)
    while z < z1:
        z += step
        cur = _has_metal(body, x, z, side)
        if cur and not prev:
            return z - step / 2.0
        prev = cur
    return None


def _check_opaque(obname):
    """The decal panels sit on SOLID sheet metal. Assert the material bound to
    the object is opaque: Transmission Weight must be UNLINKED and 0.0 on
    every Principled BSDF in it."""
    out = []
    ob = bpy.data.objects.get(obname)
    if not ob:
        return out
    mats = [s.material for s in ob.material_slots if s.material]
    if not mats:
        out.append(f"'{obname}' has no material bound")
        return out
    for m in mats:
        if not m.use_nodes or not m.node_tree:
            continue
        pr = [n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED']
        if not pr:
            out.append(f"'{obname}' material '{m.name}' has no Principled BSDF")
        for n in pr:
            s = n.inputs["Transmission Weight"]
            if s.is_linked:
                out.append(f"'{obname}' material '{m.name}' has Transmission "
                           "Weight LINKED -- it is painted sheet metal, not "
                           "a frosted pane (SPEC 0.2)")
            elif abs(s.default_value) > 1e-6:
                out.append(f"'{obname}' material '{m.name}' has Transmission "
                           f"Weight {s.default_value:.3f}, must be 0.0 -- it "
                           "is painted sheet metal (SPEC 0.2)")
    return out


def _measure_wheels():
    """Track and tyre diameter measured from geometry, not read from constants."""
    out = {}
    for tag, xa in (("F", _T.X_AXLE_F), ("R", _T.X_AXLE_R)):
        ys, zs = [], []
        for ob in bpy.data.objects:
            if not ob.name.startswith("tyre"):
                continue
            vs = [ob.matrix_world @ v.co for v in ob.data.vertices]
            if abs(sum(v.x for v in vs) / len(vs) - xa) > 0.30:
                continue
            ys.append(sum(v.y for v in vs) / len(vs))
            zs += [v.z for v in vs]
        if len(ys) == 2:
            out["TRACK_" + tag] = abs(ys[0] - ys[1])
        if zs:
            out["TYRE_D"] = max(zs) - min(zs)
    return out


def run(body, log=print):
    fails, warns = [], []

    # 1. overall dimensions
    lo, hi = _bounds()
    bb = [body.matrix_world @ Vector(c) for c in body.bound_box]
    bw = max(v.y for v in bb) - min(v.y for v in bb)
    L, W, H = hi.x - lo.x, bw, hi.z
    log(f"  x range [{lo.x:.3f}, {hi.x:.3f}]   full-Y [{lo.y:.3f}, {hi.y:.3f}]")
    # rev 8: HEIGHT IS NOT A SCALAR ANY MORE, twice over. The vehicle is raked,
    # so the roof is a sloping line; and the roof lids are modelled OPEN, so the
    # bbox top is the raised signboard at ~3.0 m, not the vehicle. Measure the
    # ROOF at the rear-axle station -- the highest point of the fixed roof, and
    # the station REF_MEASUREMENTS sec.2.3 took its 1.960 at.
    Hroof = _roof_z_at(_T.X_AXLE_R)
    # The roof row carries REF_MEASUREMENTS sec.2.3's own +/- 0.030 stated band
    # on top of the model tolerance -- it is a photograph measurement, not a
    # factory figure. rev 8 residual: -37 mm (was -89 mm before the rake).
    for nm, got, want, tol in (("length", L, SPEC["L"], TOL),
                               ("width", W, SPEC["W"], TOL)):
        d = got - want
        (fails if abs(d) > tol else warns if abs(d) > tol * 0.5
         else []).append(f"{nm} {got:.3f} vs spec {want:.3f} ({d*1000:+.0f} mm)")

    # 1a. ROOF CROWN AT THE REAR AXLE -- REGRESSION CATCHER, NOT AN ACCURACY
    # TEST.  See the H_ROOF block at the top of this file.  The comparand is
    # the MODEL'S OWN baseline, so a pass here means "the roof has not moved",
    # NOT "the roof is right".  It is a FAIL past the band, not a warn: an
    # unintended geometry change should stop the build, and a deliberate one
    # should be re-baselined by hand and stated.
    _hreg = Hroof + DOME_DEFICIT
    _hd = _hreg - H_ROOF_REGRESSION
    if abs(_hd) > H_ROOF_REGRESSION_BAND:
        fails.append(
            f"roof crown @ rear axle MOVED {_hd*1000:+.1f} mm vs the rev-22 "
            f"regression baseline {H_ROOF_REGRESSION:.4f} "
            f"(band +-{H_ROOF_REGRESSION_BAND*1000:.0f} mm) -- this row is a "
            f"REGRESSION CATCHER, not an accuracy test; re-baseline "
            f"deliberately or move the geometry back, never widen the band")
    # The RAW number is logged unconditionally so the un-modelled dome can never
    # go quiet behind the correction that lets the guard pass, and the retired
    # target is printed alongside it so its withdrawal can never look like an
    # improvement in the model.
    log(f"  dims  L={L:.3f} W={W:.3f} roof@rear-axle={Hroof:.4f} "
        f"(regression baseline {H_ROOF_REGRESSION:.4f}, {_hd*1000:+.1f} mm; "
        f"dome deficit {DOME_DEFICIT*1000:+.0f} mm still unmodelled) "
        f"(bbox top {H:.3f})")
    log(f"  H_ROOF {H_ROOF_RETIRED:.3f} is RETIRED as an accuracy target "
        f"(rev 22, owner's call): its only ground-line-free support was "
        f"withdrawn by SPEC 10.34. The model reads {_hreg:.4f}; the real "
        f"vehicle's absolute roof height is OPEN and UNMEASURED. The +23 mm "
        f"warn is gone because THE TEST WAS WITHDRAWN, not because the model "
        f"improved -- the mesh did not move.")

    # 1b. THE REAR OVERHANG, rev 16.  This is the row that carries the actual
    # measurement; row 1's L cannot, because its forward end is X_NOSE and
    # X_NOSE has never been measured (lamppost, ref_side.jpg cols 62-79).
    #
    # Measured DIMENSIONLESSLY and stated the same way, so no metre scale, no
    # origin and no ground line enters this guard:
    #
    #     rear overhang / wheelbase = 0.3412 +- 0.0015   in the IMAGE
    #     -> 0.773 +- 0.022 m through the projective flank map
    #     -> 0.773 / 2.400 = 0.3221 in the WORLD
    #
    # The image ratio and the world ratio are NOT the same number and must not
    # be compared to each other -- the flank map is projective (u_vp ~ -11140),
    # which is exactly what LOFT_GROUND sec.0.3 refuted REF sec.0.2 over. The
    # world value is what a mesh can be tested against, so it is what is
    # tested here.  Tolerance is the measurement's own +-0.022 m, widened to
    # 0.030 m for mesh/subdivision slack, and NOT to swallow a regression: the
    # value it replaced was 0.4200, which is 26 sigma away.
    _ovh = _T.X_AXLE_R - min(v.x for v in
                             (body.matrix_world @ v.co for v in
                              body.data.vertices))
    _d = _ovh - _T.O_NEW
    (fails if abs(_d) > 0.030 else warns if abs(_d) > 0.015
     else []).append(f"rear overhang {_ovh:.4f} vs measured {_T.O_NEW:.4f} "
                     f"({_d*1000:+.0f} mm)")
    log(f"  rear overhang {_ovh:.4f} m = {_ovh/SPEC['WB']:.4f} of the "
        f"wheelbase (measured 0.773 +- 0.022 m)")

    # 2. wheelbase / track / tyre diameter, MEASURED
    m = _measure_wheels()
    for k in ("TRACK_F", "TRACK_R", "TYRE_D"):
        if k not in m:
            fails.append(f"could not measure {k} from geometry")
            continue
        d = m[k] - SPEC[k]
        if abs(d) > TOL:
            fails.append(f"{k} {m[k]:.4f} vs spec {SPEC[k]:.4f} ({d*1000:+.0f} mm)")
    if m:
        log("  measured " + "  ".join(f"{k}={v:.4f}" for k, v in sorted(m.items())))

    # 3. pickup-era geometry must be gone
    for ob in bpy.data.objects:
        n = ob.name.lower()
        for b in BANNED:
            if b in n:
                fails.append(f"banned object '{ob.name}' (matches '{b}')")

    # 4. exactly three OPEN apertures on the show side — tested on the shell
    import t1_shell as _S
    # rev 8: the probe height is now per-bay, because the shear moves the
    # window band down by 33 mm for every metre forward. One scalar probe z
    # across bays 0.82 m apart would miss by 27 mm.
    _bpz = _bay_probe_z(_S)
    opened = 0
    for i, (xr, xf) in enumerate(_S.BAYS):
        xm = (xr + xf) / 2.0
        BAY_PROBE_Z = _bpz + _frame_dz(xm)       # authored -> mesh frame, at xm
        if not _has_metal(body, xm, BAY_PROBE_Z, _S.SHOW_SIDE):
            opened += 1
        else:
            fails.append(f"serving bay {i} at x={xm:.3f} is NOT open "
                         "(boolean rolled back, or bay never cut)")
    if opened != N_BAYS_OPEN:
        fails.append(f"show side has {opened} open apertures, spec says "
                     f"{N_BAYS_OPEN}")
    log(f"  open serving apertures on +Y: {opened}")

    # 5. no fourth bay — the rear corner panel must be solid sheet metal
    if len(_S.BAYS) != N_BAYS_OPEN:
        fails.append(f"t1_shell.BAYS has {len(_S.BAYS)} entries, spec says "
                     f"{N_BAYS_OPEN} (a fourth bay is a rev-3 regression)")
    for xp in SOLID_PROBE_X:
        if not _has_metal(body, xp, _bpz + _frame_dz(xp), _S.SHOW_SIDE):
            fails.append(f"rear corner panel is open at x={xp:.2f} — it must be "
                         "solid metal carrying the 100% Calidad decal")
    if bpy.data.objects.get("glass_calidad"):
        fails.append("'glass_calidad' exists — the decal goes on sheet metal, "
                     "not a frosted pane (SPEC 0.2)")
    if bpy.data.objects.get("glass_bay3_L"):
        fails.append("'glass_bay3_L' exists — there is no fourth bay")
    if not bpy.data.objects.get("calidad_L"):
        fails.append("missing 'calidad_L' decal panel")
    # 5b. and the material actually ON it must be PAINT, not glass. rev 3's
    # frosted_calidad() set Transmission Weight 0.88 and rendered the panel
    # 51.9 sRGB code values darker than the surrounding cream (55.0 % of its
    # linear reflectance) inside a hard rectangular border. Testing only that
    # the object and a material of that name exist passes with that defect
    # present, which is how it came back.
    fails += _check_opaque("calidad_L")

    # 6b. SPEC: nothing on this vehicle is translucent. No subsurface, ever.
    for mt in bpy.data.materials:
        if not mt.use_nodes or not mt.node_tree:
            continue
        for n in mt.node_tree.nodes:
            if n.type != 'BSDF_PRINCIPLED':
                continue
            s = n.inputs.get("Subsurface Weight")
            if s is None:
                continue
            if s.is_linked or s.default_value > 1e-6:
                fails.append(f"material '{mt.name}' has Subsurface Weight "
                             f"{'linked' if s.is_linked else s.default_value}"
                             " -- SPEC allows none anywhere")

    # 6. materials
    for mt in NEED_MATS:
        if mt not in bpy.data.materials:
            fails.append(f"missing material '{mt}'")
    # rev 8: this used to be the hand-written list ("whitewall", "wheelred",
    # "timber") -- the retired materials somebody remembered to type. `canvas`
    # was never added, so a folding CANVAS ragtop that SPEC sec.0.2 retired in
    # rev 4 shipped green through three revisions and every guard passed over
    # it.
    #
    # rev 24, SPEC 10.67 -- THE SENTENCE THAT STOOD HERE WAS FALSE, and it is
    # the reason rev 24's work item 2 was briefed the way it was.  It read:
    # "The list is now DERIVED from sec.0.2 itself, so retiring a reading in
    # the spec arms the guard automatically and this class of miss is closed."
    # It is NOT derived from sec.0.2.  `_retired_material_tokens()` returns
    # `set(_RETIRED_MAT)` -- the hand-written dict fifteen lines above -- and
    # `_retired_section_drift()` reads sec.0.2 only to COUNT its bullets; it
    # never reads a bullet's CONTENT.  So adding a reading to sec.0.2 does NOT
    # arm this guard.  It bumps a count and forces a human review, which is
    # real but is a different thing.
    #
    # And the loop below can only ever see a MATERIAL DATABLOCK NAME.  Of the
    # ~100 retirements in SPEC sec.10, exactly ONE is a material (the canvas
    # ragtop, already covered).  Every other one is a VALUE, a METHOD, a CROP
    # or a withdrawn TEST, and none of those is reachable from here.  That is
    # why sec.10.64's four stale "locked" rows were not caught: no mechanism
    # existed that could see them.  `_retired_value_drift()` below is the one
    # that can.  A CLAIM IN PROSE IS NOT A GUARD -- including when the prose
    # is inside the guard.
    for banned_mat in _retired_material_tokens():
        if banned_mat in bpy.data.materials:
            uses = [o.name for o in bpy.data.objects if o.type == 'MESH'
                    and any(s.material and s.material.name == banned_mat
                            for s in o.material_slots)]
            if uses:
                fails.append(f"retired material '{banned_mat}' is assigned to "
                             f"{len(uses)} objects e.g. {uses[0]} (SPEC 0.2)")
    _drift = _retired_section_drift()
    if _drift:
        warns.append(_drift)
    # rev 24, SPEC 10.67 -- the retired-VALUE guard.  This is the one that can
    # see sec.10.64's defect class.  It FAILS rather than warns: a retired
    # number published as locked in a FROZEN section is how `W_ART = 0.30`
    # stood 3.3x wrong for thirteen revisions.
    _vd = _retired_value_drift()
    if _vd is None:
        warns.append("could not read SPEC.md -- retired-VALUE guard did not "
                     "run. It declines rather than passing silently.")
    else:
        for lit, ln, live, sym, sec in _vd:
            fails.append(f"SPEC.md:{ln} publishes the RETIRED '{lit}' unstruck "
                         f"({sym} is {live}; retired by SPEC {sec})")
    # ...and the geometry that carried them
    for ob in bpy.data.objects:
        if ob.type == 'MESH' and ob.name.split('.')[0] in ("rag", "ragframe"):
            fails.append(f"'{ob.name}' is folding-ragtop geometry; the roof is "
                         "cut into rigid hinged steel lids (SPEC 0.2)")

    # 7. roof must run to the tail
    zmax_tail = max((body.matrix_world @ v.co).z for v in body.data.vertices
                    if (body.matrix_world @ v.co).x < -1.60)
    if zmax_tail < 1.90 - _T.RIDE_DROP:
        fails.append(f"roof drops to {zmax_tail:.3f} aft of x=-1.60 "
                     "(bed-rail regression)")
    log(f"  roof at tail = {zmax_tail:.3f}")

    # 8. manifold body shell — SPEC has always said FAIL, rev 3 only warned
    bm = bmesh.new(); bm.from_mesh(body.data)
    nm_e = sum(1 for e in bm.edges if not e.is_manifold)
    nm_v = sum(1 for v in bm.verts if not v.is_manifold)
    bm.free()
    if nm_e:
        fails.append(f"{nm_e} non-manifold edges / {nm_v} verts on the shell")

    # 9. no boolean may have rolled back
    try:
        import __main__
        fc = getattr(__main__, "FAILED_CUTS", [])
    except Exception:
        fc = []
    if fc:
        fails.append(f"{len(fc)} boolean(s) rolled back: {', '.join(fc)}")

    # 10. ride height. rev 4 asserted stock and was WRONG; the measured rear
    # arch-to-tyre gap is 41 mm against a stock 90-120. Guard the real value in
    # BOTH directions so neither a reset-to-stock nor a drift reappears.
    # rev 18 -- THE OLD ROW 10 WAS AN ALGEBRAIC IDENTITY AND COULD NOT FAIL.
    # t1_core defines X_DROP_REF = (0.0650 - RAKE_Z0)/RAKE_DZDX and then
    # RIDE_DROP = RAKE_Z0 + RAKE_DZDX*X_DROP_REF, which cancels to the literal
    # 0.0650 for ANY rake.  Measured residual: exactly 0.000e+00, not "small".
    # Setting RAKE_Z0 to 0.000 / 0.020 / 0.200 / 0.500 leaves the row green --
    # i.e. the stance could be reset to stock, the exact rev-4 regression this
    # row exists to catch, and it would still pass.  The identity is kept as a
    # cheap self-consistency assert, correctly LABELLED, and the quantities
    # that actually describe the stance are guarded underneath it.
    if abs(_T.RIDE_DROP - RIDE_DROP_SPEC) > 1e-9:
        fails.append(f"RIDE_DROP={_T.RIDE_DROP:.6f} is no longer the identity "
                     f"{RIDE_DROP_SPEC:.4f}; X_DROP_REF's definition changed")
    # SPEC sec.10.9 / t1_core:120 lock the rake at 0.01775 m/m, re-derived a
    # fourth way in rev 13 and 33.0 mm/m rejected at 4.5 sigma.  THIS is the
    # number that says the bus is lowered nose-down, and nothing guarded it.
    if abs(_T.RAKE_DZDX - RAKE_SPEC) > 0.0020:
        fails.append(f"rake {_T.RAKE_DZDX*1000:.2f} mm/m; SPEC 10.9 locks "
                     f"{RAKE_SPEC*1000:.2f} (re-derived 4 ways, rev 13)")
    log("  rake %.2f mm/m (locked %.2f); drop at x=0 %.1f mm; RIDE_DROP "
        "identity holds" % (_T.RAKE_DZDX * 1000, RAKE_SPEC * 1000,
                            _T.RAKE_Z0 * 1000))

    # rev 18 -- THE ARCH-TO-TYRE GAP IS NOW MEASURED ON THE MESH.
    # It was `ARCH_R - TIRE_R`: two source constants, so it returned 41.0 mm
    # forever regardless of what rear_arch_outline actually built.  Rev 16
    # rebuilt the rear arch as a flat-crowned ogee and NOTHING measured the
    # result -- ARCH_W_REAR, _ARCH_PROFILE, _arch_drop and rear_arch_outline
    # appear zero times in this file and zero times in audit.py.
    # The lip is found by walking z upward at the axle station until the flank
    # skin appears.  The hub is at TIRE_R above ground in the dropped frame.
    _hub_z = _T.TIRE_R
    for _tag, _ax in (("rear", _T.X_AXLE_R), ("front", _T.X_AXLE_F)):
        _lip = _arch_lip_z(body, _ax, +1, _hub_z - 0.02, _hub_z + 0.45)
        if _lip is None:
            fails.append(f"{_tag} arch lip not found at x={_ax:.3f} between "
                         f"{_hub_z-0.02:.3f} and {_hub_z+0.45:.3f} -- the probe "
                         "found no skin transition, so this row measured NOTHING")
            continue
        # lip ABOVE HUB is (lip_z - hub_z); the TYRE GAP is that minus the tyre
        # radius, because the tyre crown sits TIRE_R above the hub.  Keeping the
        # two separate on purpose -- LOFT_GROUND sec.2.6 quotes the first
        # (0.3726 +- 0.0052) and SPEC sec.2 locks the second (41 +- 8 mm), and
        # conflating them is a 332 mm error.
        _above = _lip - _hub_z
        _gap = _above - _T.TIRE_R
        log("  %s arch lip above hub %.4f m (ARCH_R %.4f) -> tyre gap %.1f mm"
            % (_tag, _above, _S.ARCH_R, _gap * 1000))
        if _tag == "rear" and abs(_gap - 0.041) > 0.008:
            fails.append(f"rear arch-to-tyre gap {_gap*1000:.1f} mm MEASURED on "
                         f"the mesh; SPEC sec.2 locks 41 +- 8. "
                         f"ARCH_R-TIRE_R (the old constants-only test) says "
                         f"{(_S.ARCH_R-_T.TIRE_R)*1000:.1f}")

    # ---------------------------------------------------------------------
    # 11. POSITIVE feature assertions.
    #
    # Row 9 only reports FAILED_CUTS. That is a report of the build's own
    # bookkeeping, not a test of the mesh: a boolean that was rolled back
    # leaves a perfectly VALID, manifold, correctly-sized shell with the
    # feature silently missing, and a cut that was never issued at all leaves
    # nothing for row 9 to report. That is exactly how the shipped model went
    # out with no cab-door shut line. Assert instead that every expected
    # aperture and every expected shut line is actually THERE, measured off
    # the geometry.
    #
    # Frame: run() executes BEFORE build.py step 8b, so every z here is
    # UN-DROPPED.
    ss = _S.SHOW_SIDE
    # 11a. cab door glazing — main + vent, both flanks
    for outline, tag in ((_S.DOOR_MAIN_S, "cab door glass"),
                         (_S.DOOR_VENT_S, "cab door vent")):
        cx = sum(p[0] for p in outline) / len(outline)
        cz = sum(p[1] for p in outline) / len(outline) + _frame_dz(cx)
        for s in (1, -1):
            if not _flank_open(body, cx, cz, s):
                fails.append(f"{tag} aperture on {'+' if s > 0 else '-'}Y is "
                             f"NOT cut at ({cx:.3f}, {cz:.3f})")

    # 11b. serving bays — the off side is glazed but still an aperture in the
    # sheet metal, and row 4 only ever tested the show side
    for i, (xr, xf) in enumerate(_S.BAYS):
        xm = (xr + xf) / 2.0
        if not _flank_open(body, xm, _bpz + _frame_dz(xm), -ss):
            fails.append(f"serving bay {i} at x={xm:.3f} is NOT cut on the "
                         "off side")

    # 11c. windscreen — probe along the screen normal, 60 mm each way
    for s in (1, -1):
        yc = s * (_S.WS_DIV + _S.WS_PANE_W / 2)
        o = (_S.WS_MID + Vector((0.0, yc, _frame_dz(_S.WS_MID.x)))
             + _S.WS_N * 0.060)
        if not _ray_clear(body, o, -_S.WS_N, 0.120):
            fails.append(f"windscreen pane {'L' if s > 0 else 'R'} is NOT cut")

    # 11d. rear window
    # rev 18 -- THIS ROW WAS DEAD TOO, and for the same reason.  The ray was
    # cast from the literal x = -2.40 for 0.35 m, so it TERMINATED AT -2.0500
    # -- 177 mm short of the tail skin at X_TAIL = -1.8730, and 58 mm short
    # even at the OLD tail station.  It touched nothing, so `_ray_clear` was
    # unconditionally True and "the rear window is cut" was asserted by a ray
    # that never reached the vehicle.  Controls: aimed 0.45 m and 0.70 m below
    # the window, and 0.15 m above it -- all three certainly SOLID metal --
    # it still returned True.  Unbounded, the same ray travels 4.3738 m and
    # first hits the WINDSCREEN.
    #
    # Both endpoints are now offsets from X_TAIL, so the probe follows the
    # tail when the tail moves.  _RW_BACK puts the origin clear behind the
    # skin; _RW_THRU is how far past the skin the ray must reach to prove the
    # aperture is open.  0.20 m is ~70x the 2.8 mm solidify thickness and
    # still stops 3.5 m short of the windscreen, so it cannot pass by
    # travelling the length of the vehicle.
    _RW_BACK, _RW_THRU = 0.30, 0.20
    if not _ray_clear(body,
                      (_T.X_TAIL - _RW_BACK, 0.0,
                       _S.REAR_Z + _frame_dz(_T.X_TAIL)),
                      (1, 0, 0), _RW_BACK + _RW_THRU):
        fails.append("rear window is NOT cut")

    # 11d2. THE ROOF HOLE, rev 12. build.py issued no roof cutter at all for
    # eleven revisions and nothing caught it, because the only thing asserting
    # a roof opening existed was PROSE -- in SPEC, in t1_shell's docstrings and
    # in three handoffs. A claim in prose is not a guard; this is the node that
    # does it. Two-sided on purpose: the opening must be OPEN, and the roof
    # must still be SOLID everywhere the owner says it is solid (SPEC 10.28 --
    # one opening only, strips surviving on both sides, solid fore and aft).
    # Stations in METRES off the opening's own edges, not fractions: the first
    # cut of this guard used fractions of the opening span and put two probes
    # at |y| = 0.81, which is off the roof entirely, and one at x = +1.21.
    # Every z here is UN-DROPPED and must be carried into the mesh's own frame
    # with _frame_dz(x) -- run() executes AFTER step 8b (SPEC 10.1). The first
    # cut omitted it and the 0.30 m ray stopped 26 mm ABOVE a roof that was
    # perfectly solid. That is the same frame error SPEC 10.1 exists for, and
    # it is why the ray is now long enough that no plausible frame slip can
    # reproduce it silently.
    _xf, _xa = max(_S.LID_X0, _S.LID_X1), min(_S.LID_X0, _S.LID_X1)
    _yo, _ys = _S.LID_Y_HINGE, _S.LID_Y_HINGE + _S.LID_W
    _M = 0.080                       # clear of the 30 mm cut-out corner radius
    for (px, py, want_open, tag) in (
            ((_xf + _xa) / 2, (_yo + _ys) / 2, True, "roof aperture centre"),
            (_xf - 0.20, _yo + 0.20, True,  "roof aperture fore end"),
            (_xa + 0.20, _ys - 0.20, True,  "roof aperture aft end"),
            (_xf + _M, (_yo + _ys) / 2, False, "roof FORWARD of the opening"),
            (_xa - _M, (_yo + _ys) / 2, False, "roof AFT of the opening"),
            ((_xf + _xa) / 2, _yo - _M, False, "off-side roof strip (hinge side)"),
            ((_xf + _xa) / 2, _ys + _M, False, "show-side roof strip (drip rail)")):
        o = (px, py, _S.roof_z(px, py) + _frame_dz(px) + 0.300)
        got_open = _ray_clear(body, o, (0, 0, -1), 0.750)
        if want_open and not got_open:
            fails.append(f"{tag} at ({px:.3f}, {py:.3f}) is NOT cut -- the "
                         "galley is a sealed steel box again")
        if (not want_open) and got_open:
            fails.append(f"{tag} at ({px:.3f}, {py:.3f}) is cut through; SPEC "
                         "10.28 says exactly ONE opening, that size")
    log("  roof aperture: open, and solid fore / aft / both sides")

    # 11e. shut lines. A gap cutter makes a 5.5 mm through-slot; sample the
    # outline and require most samples to pass the near skin.
    for s in (1, -1):
        fr = _slot_frac(body, _S.DOOR_GAP_S, s, _frame_dz)
        if fr < SLOT_FRAC_MIN:
            fails.append(f"cab door shut line on {'+' if s > 0 else '-'}Y is "
                         f"missing: only {fr*100:.0f} % of {len(_S.DOOR_GAP_S)}"
                         f" outline samples are open slots")
        log(f"  shut line door{s:+d}: {fr*100:.0f} % open")
    fr = _slot_frac(body, _S.CARGO_GAP, -ss, _frame_dz)
    if fr < SLOT_FRAC_MIN:
        fails.append(f"cargo door shut line is missing: only {fr*100:.0f} % of "
                     f"{len(_S.CARGO_GAP)} outline samples are open slots")
    log(f"  shut line cargo: {fr*100:.0f} % open")
    # rev 18: the "got through" plane is the cutter's own station, expressed,
    # not a literal.  See _englid_frac -- this row was dead at every revision.
    fr = _englid_frac(body, _S.ENGLID_GAP, _frame_dz(_T.X_TAIL),
                      _T.X_TAIL + _S.ENGLID_CUT_DX)
    if fr < SLOT_FRAC_MIN:
        fails.append(f"engine lid shut line is missing: only {fr*100:.0f} % of "
                     f"{len(_S.ENGLID_GAP)} outline samples are open slots")
    log(f"  shut line englid: {fr*100:.0f} % open")

    # 11e2. SHUT LINE x APERTURE CROSSINGS -- rev 23, SPEC sec.10.62.
    #
    # The SHOW-flank half of this invariant is asserted at IMPORT in t1_shell,
    # so by the time this row runs it has already passed -- the row logs it so
    # the number is visible rather than merely un-failed, which is the whole
    # complaint sec.10.45 made about the four decorative rows.
    #
    # The OFF-flank half is a LABELLED REGRESSION CATCHER, not an accuracy
    # test, for the same reason H_ROOF's row is: BOTH colliding features are
    # graded "E (never photographed)" in SPEC's own source table, they
    # contradict each other, and asked what the frame shows the owner answered
    # "cannot tell from this crop".  A pass here means "the off flank has not
    # moved", NOT "the off flank is right".  Re-baseline deliberately and state
    # it; never widen the band to make a change fit.
    _cross = _S.shutline_aperture_crossings()
    _show = [c for c in _cross if c[2] == _S.SHOW_SIDE]
    _off = [c for c in _cross if c[2] != _S.SHOW_SIDE]
    _offtot = sum(c[3] for c in _off)
    if _show:
        # Unreachable while the import assert stands; kept so that removing
        # that assert cannot silently drop the coverage.
        fails.append(
            "SHOW-flank aperture straddles a shut line: "
            + ", ".join(f"{c[0]}x{c[1]} {c[3]*1000:.1f} mm" for c in _show))
    _od = _offtot - _S.OFF_CROSS_BASELINE
    if abs(_od) > _S.OFF_CROSS_BAND:
        fails.append(
            f"off-flank shut line x aperture crossing MOVED {_od*1000:+.1f} mm "
            f"vs the rev-23 baseline {_S.OFF_CROSS_BASELINE*1000:.1f} mm "
            f"(band +-{_S.OFF_CROSS_BAND*1000:.0f} mm) -- REGRESSION CATCHER, "
            f"not an accuracy test; both members are graded E (never "
            f"photographed), so re-baseline deliberately, never widen")
    log(f"  shut line x aperture: show flank {sum(c[3] for c in _show)*1000:.1f}"
        f" mm (invariant, asserted at import); off flank "
        f"{_offtot*1000:.1f} mm over {len(_off)} pairs "
        f"(baseline {_S.OFF_CROSS_BASELINE*1000:.1f}, {_od*1000:+.1f} mm) "
        f"-- off flank is graded E, NOT a correctness claim")
    log(f"  gap_englid is in the (y,z) TAIL frame at x="
        f"{_T.X_TAIL + _S.ENGLID_CUT_DX:.4f}; no flank aperture shares that "
        f"surface, so a flank crossing test is NOT APPLICABLE (stated, not "
        f"silently skipped)")
    log(f"  CARGO_GAP outline samples {len(_S.CARGO_GAP)} "
        f"(rev 22: 28, of which 20 on the corner arcs = 5.2 % of the length)")

    # 11f. the shut lines and the bays must not be see-through. SPEC sec.6:
    # the hatches read as depth, not as holes. Both door gaps are collinear
    # slots and the bays are cut on both flanks, so without an inner skin a
    # ray straight through crosses nothing at all.
    dg = bpy.context.evaluated_depsgraph_get()
    sc = bpy.context.scene
    for name, samples, side in (("cab door +Y", _S.DOOR_GAP_S, 1),
                                ("cab door -Y", _S.DOOR_GAP_S, -1)):
        thru = 0
        for (x, z) in samples:
            r = sc.ray_cast(dg, Vector((x, side * 3.0, z + _frame_dz(x))),
                            Vector((0.0, -side, 0.0)))
            if (not r[0]) or r[1].y * side < 0.0:
                thru += 1
        if thru:
            fails.append(f"{name} shut line is SEE-THROUGH: {thru} of "
                         f"{len(samples)} rays cross no surface (SPEC 6 wants "
                         "an inner skin behind the slot)")
    for i, (xr, xf) in enumerate(_S.BAYS):
        xm = (xr + xf) / 2.0
        r = sc.ray_cast(dg, Vector((xm, ss * 3.0, _bpz + _frame_dz(xm))),
                        Vector((0.0, -ss, 0.0)))
        if (not r[0]) or abs(r[1].y) > 0.80:
            fails.append(f"serving bay {i} has nothing behind it — a "
                         "600 x 400 mm hole, not a hatch (SPEC 6)")

    # 12. the corrected measured constants, both frames.
    #
    # Z_SILL / Z_HEAD / BAYS / DOOR_GAP live in t1_shell and are UN-DROPPED:
    # they build cutter geometry before step 8b. Z_BELT / V_APEX / V_RISE /
    # V_POW live in t1_mats and are ABOVE-GROUND, because a shader reads
    # Geometry->Position at RENDER time off the already-dropped mesh. Getting
    # that backwards puts the paint 65 mm out. The pressed swage in
    # t1_shell.zV() therefore carries the same numbers PLUS RIDE_DROP; if the
    # two drift the crease and the two-tone line separate.
    import t1_mats as _MT
    if abs((_MT.V_APEX + _MT.V_RISE) - _MT.Z_BELT) > 1e-9:
        fails.append(f"V_APEX {_MT.V_APEX} + V_RISE {_MT.V_RISE} != Z_BELT "
                     f"{_MT.Z_BELT}: the V arms miss the flank belt line")
    if _MT.V_APEX > 0.3960 + 1e-9:
        fails.append(f"V_APEX {_MT.V_APEX:.4f} above ground exceeds the hard "
                     "bound 0.396 set by the bumper occlusion in "
                     "ref_workshop.jpg")
    if _MT.V_POW >= 1.0:
        fails.append(f"V_POW {_MT.V_POW} >= 1: the measured V profile is "
                     "CONCAVE, not convex")
    for nm, geo, sha in (("V_APEX", _S.V_APEX_Z - _T.RIDE_DROP, _MT.V_APEX),
                         ("V_RISE", _S.V_RISE_Z, _MT.V_RISE),
                         ("V_POW", _S.V_POW_Z, _MT.V_POW)):
        if abs(geo - sha) > 1e-6:
            fails.append(f"{nm} de-registered: pressed swage says {geo:.4f} "
                         f"above ground, painted break says {sha:.4f}")
    if abs(_S.zV(_S.V_HALF_W) - (_MT.Z_BELT + _T.RIDE_DROP)) > 1e-6:
        fails.append("the V-swage arms do not land on the belt line at "
                     f"|y| = {_S.V_HALF_W}")
    for nm, got, want in (("Z_SILL", _S.Z_SILL, BAND_SPEC[0]),
                          ("Z_HEAD", _S.Z_HEAD, BAND_SPEC[1])):
        if abs(got - want) > 1e-6:
            fails.append(f"{nm} {got:.4f} un-dropped; measured {want:.4f} "
                         f"({want - _T.RIDE_DROP:.4f} above ground)")
    if len(_S.BAYS) == len(BAYS_SPEC):
        for i, (got, want) in enumerate(zip(_S.BAYS, BAYS_SPEC)):
            if abs(got[0] - want[0]) > 1e-6 or abs(got[1] - want[1]) > 1e-6:
                fails.append(f"serving bay {i} edges {got} vs measured {want} "
                             "(rev-3's evenly-spaced bays are retired)")
    log("  band %.3f-%.3f un-dropped (%.3f-%.3f AG)  bay widths %s"
        % (_S.Z_SILL, _S.Z_HEAD, _S.Z_SILL - _T.RIDE_DROP,
           _S.Z_HEAD - _T.RIDE_DROP,
           " ".join("%.3f" % (b[1] - b[0]) for b in _S.BAYS)))

    # Buried detail must never pass again: both wipers shipped for six
    # revisions fully enclosed in the nose skin. Casts camera -> object, not
    # object -> camera; the outward cast scores a buried part 100 % visible.
    try:
        fails += __import__("t1_detail").visibility_fails()
    except Exception as e:                       # never let the guard vanish
        fails.append("visibility assertion could not run: %s" % e)
    log("  VERIFY: %d fail, %d warn" % (len(fails), len(warns)))
    for f in fails:
        log("    FAIL  " + f)
    for w in warns:
        log("    warn  " + w)
    return not fails
