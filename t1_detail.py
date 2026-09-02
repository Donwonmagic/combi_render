"""Wheels, bright-work, lamps, counter, galley, interior."""
import bpy
import numpy as _np, bmesh, math, os
from mathutils import Vector, Matrix
import t1_core as T

TAU = math.pi * 2
NEW = []

# ---------------------------------------------------------------- registries
# FLAT              objects that must NOT be smooth-shaded.  build.py's A()
#                   calls shade_smooth() unconditionally, which averages the
#                   normals across a 90 deg pressed edge and turns a louvre
#                   lip or a counter corner into a soft blob.  build.py calls
#                   D.shade_fix() once, after the last A(), to undo that.
# VISIBILITY_WATCH  objects that must be reachable by a camera ray.  See
#                   visibility_fails() at the bottom of this file -- that is
#                   the guard for the defect Task 4 existed to fix.
FLAT = []
VISIBILITY_WATCH = []


def keep(o, mat=None, smooth=True):
    if smooth and o.type == 'MESH':
        o.data.shade_smooth()
    if mat:
        o["mat"] = mat
    NEW.append(o)
    return o


def place(o, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
    from mathutils import Euler
    m = (Matrix.Translation(loc)
         @ Euler(rot, 'XYZ').to_matrix().to_4x4()
         @ Matrix.Diagonal(Vector(scale)).to_4x4())
    for v in o.data.vertices:
        v.co = m @ v.co
    o.data.update()
    return o


# ============================================================== WHEEL / TYRE
# --------------------------------------------------------------------- rev 74
# F308 -- THE TYRE'S TRANSVERSE TREAD.
#
# `T.revolve` is ROTATIONALLY SYMMETRIC BY CONSTRUCTION, so the tyre's four
# grooves are CIRCUMFERENTIAL rings and NO amount of profile tuning could ever
# produce the transverse lugs the photograph shows on the shoulder.  That is
# rule 54 exactly -- the quantity is not a free parameter of the model -- so it
# needs new construction, not a swept constant.  The lugs were LOOKED AT FIRST,
# at TRUE PIXEL RESOLUTION with no interpolation, before any of this was
# written: probe_scratch/r74_tread_nearest.png, off ref_playa_34.png.
#
# *** THE COUNT IS A DECLARED CHOICE INSIDE A MEASURED BRACKET.  IT IS NOT A
# MEASUREMENT AND MUST NOT BE QUOTED AS ONE. ***  probe_rev74_tread.py's T2
# puts the bracket at 48..84 lugs per revolution -- a 1.73x span -- because two
# independent estimators (a groove PEAK COUNT and an FFT of the same angular
# signal) disagree by ~30 % and each moves with the radius it is read at.  The
# tread pitch is ~3 px in a 500x400 frame.  This is the same standing as
# t1_shell.TB_WIDTH's "POSE CHOICE, NOT MEASURED", and it is labelled the same
# way.  WHAT **IS** MEASURED IS THE KIND: the tyre must not be a surface of
# revolution, and T3 reads 0.000000 m of angular variation before this change.
TREAD_LUGS = 64          # DECLARED, inside the MEASURED bracket 48..84 (F308)
TREAD_CUT  = 0.0060      # DECLARED groove depth, m.  NOT measured -- see above
TREAD_SEG  = 6           # revolve segments per lug: 2 groove + 4 land
# The threshold is a PHASE, and the revolve emits phases at exact multiples of
# 1/TREAD_SEG.
#
# *** THE FIRST CUT OF THIS GOT IT HALF RIGHT AND SHIPPED AN IRREGULAR TREAD
# (F319).  It used threshold 0.25 with no phase offset, reasoning that 0.25
# sits midway between 1/6 and 2/6 so float error cannot flip a segment.  THAT
# PROTECTS ONLY THE TRAILING EDGE.  The LEADING edge sits at phase exactly 0 --
# the modulo wrap -- where the margin is ZERO, so every phase-0 segment was a
# coin flip.  MEASURED on the mesh: 99 of 384 vertices cut instead of 128, in
# runs of 1 and 2 (34 lugs two segments wide, 31 one segment wide).  Found by a
# rule-17 adversary, not by me. ***
#
# FIXED by offsetting the phase HALF A SEGMENT, so vertex phases land at
# (2k+1)/12 of a turn -- 1/12, 3/12, 5/12 ... -- and NO vertex sits on a
# boundary.  With the threshold at 1/3 = 4/12 the two grooved segments are at
# 1/12 and 3/12, each a full 1/12 of a turn clear of the cut.  The realised
# duty is then genuinely 2 of 6, and probe_rev74_tread's T7 MEASURES it rather
# than trusting this comment (rule 10).
TREAD_PHASE = 0.5 / TREAD_SEG        # half a segment, so no vertex is on an edge
TREAD_DUTY = 1.0 / 3.0
TREAD_HALF = 0.0522      # tread band half-width, from the profile in tyre()


def _cut_tread(ob):
    """Cut TREAD_LUGS transverse grooves into the tread band, INWARD.

    INWARD IS THE WHOLE POINT: the crown's maximum RADIUS is the same object
    before and after, and probe_rev74_tread.py's T5 reads that delta as
    5.56e-10 m.

    *** BUT "SO IT CANNOT MOVE A GUARDED DIMENSION" WAS FALSE AND IS WITHDRAWN
    (F319).  `verify.py` does not lock the maximum radius; `_measure_wheels`
    locks `TYRE_D = max(zs) - min(zs)`, a Z BOUNDING-BOX EXTENT.  The vertex
    nearest the +Z pole falls inside a groove, so that extent DOES shrink:
    0.6650000 -> 0.6649555, a delta of 0.0445 mm.  It is harmless -- verify.py's
    own TOL is 0.025 m, so this is 560x inside it, and it is a DISCRETISATION
    artefact (which discrete vertex lands nearest the pole), not a change in the
    tyre's diameter over its lands.  What is NOT harmless is a guard that does
    not measure the quantity it names (rule 38), so T5 now reads BOTH and says
    which is which.  Caught by a rule-17 adversary. ***
    """
    me = ob.data
    for v in me.vertices:
        if abs(v.co.y) > TREAD_HALF:
            continue
        r = math.hypot(v.co.x, v.co.z)
        if r < T.TIRE_R - 0.030:              # sidewall/bead, not the crown
            continue
        _ph = (math.atan2(v.co.z, v.co.x) * TREAD_LUGS
               + T.TAU * TREAD_PHASE) % T.TAU
        if _ph < T.TAU * TREAD_DUTY:
            k = (r - TREAD_CUT) / r
            v.co.x *= k
            v.co.z *= k
    me.update()


def tyre(name="tyre"):
    """5.60-15 bias-ply cross-section; ribbed tread"""
    R = T.TIRE_R
    # sidewall, bead -> shoulder (+Y half)
    up = [
        (0.0530, 0.1905), (0.0625, 0.2020), (0.0705, 0.2220),
        (0.0728, 0.2340),                       # 3  whitewall inner edge
        (0.0745, 0.2500), (0.0752, 0.2760),
        (0.0744, 0.2905),                       # 6  whitewall outer edge
        (0.0735, 0.2980), (0.0690, 0.3110), (0.0640, 0.3195),
        (0.0578, 0.3262),
    ]
    # crowned tread band with four circumferential grooves
    def crown(y):
        return R - 0.0042 * (abs(y) / 0.0522) ** 2
    tread = []
    for (y, d) in [(-0.0522, 0), (-0.0400, 0), (-0.0378, 1), (-0.0300, 1),
                   (-0.0278, 0), (-0.0150, 0), (-0.0128, 1), (-0.0022, 1),
                   (0.0000, 0), (0.0128, 0), (0.0150, 1), (0.0256, 1),
                   (0.0278, 0), (0.0400, 0), (0.0422, 1), (0.0500, 1),
                   (0.0522, 0)]:
        tread.append((y, crown(y) - (0.0080 if d else 0.0)))
    # rev 15 -- THE BEAD SITS ON T.RIM_R, NOT ON A 15in LITERAL.
    # The sidewall above was authored for a 15in flange (BEAD_AUTHORED), but
    # the rims are 16in (t1_core.RIM_R, flange OD 0.4396) and that constant was
    # referenced by nothing.  Measured in ref_side.jpg, rear wheel, crop box
    # (680,530,825,685): cream-ring D / tyre D = 0.660 +/- 0.008 against 0.5729
    # built -- 11 sigma.  Fix by moving the BEAD out, never by shrinking the
    # tyre: the shoulder (and hence the tread band and TYRE_D 0.665, LOCKED and
    # guarded) is held fixed and only the sidewall height changes.  That is
    # exactly what a 16in rim under a 0.665 m tyre means -- a lower-profile
    # sidewall -- and REF_MEASUREMENTS sec.8 already calls the tyre "a modern
    # low-profile radial".
    BEAD_AUTHORED = 0.1905                            # 15in flange the list uses
    SHOULDER      = up[-1][1]                         # held: tread/TYRE_D fixed
    _k = (SHOULDER - T.RIM_R) / (SHOULDER - BEAD_AUTHORED)

    def _bead(r):
        return SHOULDER - (SHOULDER - r) * _k

    up = [(y, _bead(r)) for (y, r) in up]
    prof = list(up)                                   # +Y sidewall
    prof += tread[::-1]                               # tread, +Y -> -Y
    prof += [(-y, r) for (y, r) in up[::-1]]          # -Y sidewall
    _ib = _bead(0.1880)                               # inner bead, same map
    prof += [(-0.0500, _ib), (0.0500, _ib)]
    # SPEC r4: BLACKWALL. The white ring in the reference is the painted
    # steel rim, not a whitewall band (measured: SPEC 8.1). Single slot -
    # this also removes the materials.clear() index-loss bug (old D2).
    #
    # rev 74, F308: seg goes 112 -> TREAD_SEG*TREAD_LUGS so each lug gets six
    # segments.  T1_TYRE_TREAD=0 restores BOTH the old seg AND the plain
    # revolve, i.e. the rev-73 tyre exactly -- the switch moves two things and
    # that is stated rather than hidden, because its job is "back to what
    # shipped".  seg does not touch the maximum radius either way (revolve
    # places every vertex at exactly its profile radius), so TYRE_D is
    # independent of both halves.
    _tread = os.environ.get("T1_TYRE_TREAD", "1") != "0"
    ob = T.revolve(prof, seg=(TREAD_SEG * TREAD_LUGS) if _tread else 112,
                   axis='Y', name=name)
    if _tread:
        _cut_tread(ob)
    return ob


# rev 51: the disc face profile, hoisted out of rim() so it can be compared with
# the hubcap's.  Radii are AUTHORED against FLANGE_AUTHORED and scaled by S inside
# rim(); the y column is NOT scaled.  Unchanged in value -- only its scope moved.
RIM_DISC_PROF = [
    (0.0500, 0.1600), (0.0560, 0.1560), (0.0570, 0.1400),
    (0.0520, 0.1200), (0.0450, 0.0900), (0.0430, 0.0620),
    (0.0450, 0.0400), (0.0470, 0.0000),
]


def rim(name="rim"):
    """16in steel wheel (t1_core.RIM_R): barrel + domed disc.

    rev 15: the flange radius is T.RIM_R, not a literal.  The barrel and disc
    profiles below were authored against a 15in flange (FLANGE_AUTHORED) and
    are scaled radially onto RIM_R, so the live geometry now REFERENCES the
    constant instead of shadowing it with a hand-tuned absolute.
    """
    FLANGE_AUTHORED = 0.1905
    S = T.RIM_R / FLANGE_AUTHORED
    prof = [
        (0.0600, 0.1905), (0.0640, 0.1885), (0.0625, 0.1820),
        (0.0560, 0.1795), (0.0520, 0.1720), (0.0480, 0.1660),
        (0.0300, 0.1640), (0.0080, 0.1650), (-0.0080, 0.1700),
        (-0.0200, 0.1790), (-0.0230, 0.1860), (-0.0190, 0.1900),
        (-0.0250, 0.1905), (-0.0300, 0.1880), (-0.0290, 0.1800),
        (-0.0180, 0.1690), (-0.0060, 0.1600), (0.0120, 0.1560),
        (0.0330, 0.1560), (0.0480, 0.1590), (0.0540, 0.1660),
        (0.0570, 0.1760), (0.0560, 0.1840),
    ]
    prof = [(y, r * S) for (y, r) in prof]
    barrel = T.revolve(prof, seg=96, axis='Y', name=name + "_barrel")
    # disc face (slightly dished).  HOISTED to RIM_DISC_PROF at module level at
    # rev 51 so the hubcap's seat can be DERIVED from it instead of typed --
    # the two surfaces have to be compared, and a local list cannot be.
    disc_prof = [(y, r * S) for (y, r) in RIM_DISC_PROF]
    verts, faces = [], []
    seg = 96
    n = len(disc_prof)
    for k in range(seg):
        a = TAU * k / seg
        ca, sa = math.cos(a), math.sin(a)
        for (y, r) in disc_prof:
            verts.append((r * ca, y, r * sa))
        for (y, r) in [(v - 0.010, r2) for (v, r2) in reversed(disc_prof)]:
            verts.append((r * ca, y, r * sa))
    m = 2 * n
    for k in range(seg):
        k2 = (k + 1) % seg
        for i in range(m):
            j = (i + 1) % m
            faces.append((k * m + i, k * m + j, k2 * m + j, k2 * m + i))
    me = bpy.data.meshes.new(name + "_disc")
    me.from_pydata(verts, [], faces); me.validate()
    disc = bpy.data.objects.new(name + "_disc", me)
    bpy.context.collection.objects.link(disc)
    T.fix_normals(disc)
    # Five vent holes -- DELIBERATELY NOT scaled by S.  They must stay under
    # the hubcap (R 0.1345, which is CORRECT at 0.35 sigma and locked): they
    # reach 0.1415, so only 7 mm (1.5 px in ref_side.jpg) of each crescent
    # clears the cap.  Scaling them would put them at 0.1633 -- 29 mm / 6 px
    # of dark notch in a cream annulus that the photograph shows unbroken.
    cuts = []
    for i in range(5):
        a = TAU * i / 5 + 0.31
        cuts.append(T.cylinder((VENT_CENTRE_R * math.cos(a), 0.048,
                                VENT_CENTRE_R * math.sin(a)),
                               (0, 1, 0), VENT_CUT_R, 0.10, seg=28,
                               name=f"vent{i}"))
    for c in cuts:
        T.boolean(disc, c)
    T.apply_mods(disc)
    for c in cuts:
        bpy.data.objects.remove(c, do_unlink=True)
    return barrel, disc


CAP_R = 0.1345          # hubcap dome radius.  LOCKED: hubcap D / tyre D
                        # measures 0.4134 against 0.4211 built (ref_side.jpg,
                        # rear wheel, 302-ray circle fit, sd 0.79 px) -- correct,
                        # and it is the control that validated the tyre radius
                        # used for the rim fix above.  Do not touch.
CAP_D = 2 * (CAP_R + 0.0025)        # what the profile below actually reaches


def _cap_prof():
    """the hubcap's revolve profile, (y, r).  rev 51: made a function so the
    seat derivation below can read the SAME list the mesh is built from."""
    R = CAP_R
    return [
        (0.0745, 0.0000), (0.0736, 0.0300), (0.0710, 0.0560),
        (0.0664, 0.0800), (0.0596, 0.1010), (0.0502, 0.1180),
        (0.0378, 0.1288), (0.0236, 0.1342), (0.0120, R),
        (0.0040, R + 0.0025), (-0.0035, R + 0.0010), (-0.0020, R - 0.0060),
        (0.0080, R - 0.0090), (0.0220, 0.1315), (0.0362, 0.1262),
        (0.0484, 0.1155), (0.0576, 0.0988), (0.0644, 0.0780),
        (0.0690, 0.0545), (0.0716, 0.0292), (0.0725, 0.0000),
    ]


def hubcap(name="cap"):
    """large solid RED dome (SPEC rev3.2) -- not a small chrome moon cap"""
    return T.revolve(_cap_prof(), seg=96, axis='Y', name=name)


# ==================================================== THE HUBCAP'S SEAT, rev 51
# A HUBCAP CLIPS ONTO THE WHEEL.  Until rev 51 this one did not: build.py placed
# the cap at the SAME y as the tyre, barrel and disc, so its outer lip floated
# 47.7 mm INBOARD of the disc face it should sit on.  The consequence was the
# most visible defect in every shipped frame -- the cream disc crossed in front
# of the red dome at r = 0.11973 m and the five vent holes became the only
# places the cap still showed, so every wheel rendered a FIVE-PETAL FLOWER with
# five dark notches instead of a dome.
#
# MEASURED, rev 51, and it is why this moved.  How proud the dome actually
# stands was recovered from photographs by the emblem's projected offset from
# the cream-ring ellipse centre in obliquely-seen wheels -- a SHAPE-FREE
# estimator (the emblem sits on the axle axis, so no dome profile enters):
#     IMG_2073.jpeg        (GREEN bus, chrome cap)   phi 49.6 deg   49.8 +- 8.7 mm
#     ref_rear34.jpg       (RED, current artwork)    phi 70.2 deg   62.1 +- 16.0 mm
#     ref_nolita_front34   (RED, earlier artwork)    phi 58.3 deg   49.4 +- 20.5 mm
#     ---- weighted                                                 52.2, 1sd ~7 mm
# CONTROLS, all passed: the side ORTHO render at phi = 0 returns q = +0.0002
# +- 0.0025 (the dome term vanishes, as it must); the low34 render, where the
# answer is KNOWN to be 10.5 mm, reads back 12.6 +- 9.2; ref_side.jpg at
# phi = 10.5 deg correctly returns UNRECOVERABLE (+-33.9 mm).
#     as built, 10.5 mm  ->  EXCLUDED at 5.8 sigma
#     seated,   58.2 mm  ->  CONSISTENT at 0.8 sigma
# Corroborated scale-free and with no depth model at all by the visible red
# radius / rim radius ratio: photographs 0.60-0.65, built INTENT 0.6233,
# rendered 0.535-0.557 -- the render is ~14 % small, the signature of a buried
# cap, and the photographs agree with the intent.
#
# SO THE AUTHORED DOME IS RIGHT AND ONLY ITS MOUNTING WAS WRONG.  The implied
# dome depth is 52.2 + 12.3 = 64.5 mm against the authored 70.5 -- inside 1
# sigma, so the PROFILE IS NOT TOUCHED on this evidence.  (A rev-51 hypothesis
# that the dome depth itself was the defect is REFUTED by this measurement;
# recorded so nobody re-proposes it.)  CAP_R stays locked: it is a RADIUS,
# validated against a ratio of two DIAMETERS, and it never bore on depth.
#
# DERIVED, NOT TYPED (rule 2): the lip lands on the disc face at its own radius.
def _cap_seat_dy():
    """Outboard shift that seats the cap's outer lip on the wheel disc.

    Reads the SAME two tables the meshes are built from, so the two cannot
    drift apart.  Returns metres along +y (outboard) in cap-local coordinates.
    """
    cap = _cap_prof()
    r_lip = max(r for (_y, r) in cap)                       # 0.1370 = CAP_R + 0.0025
    y_lip = max(y for (y, r) in cap if abs(r - r_lip) < 1e-12)
    S = T.RIM_R / 0.1905                                    # rim()'s own scale
    dr = [r * S for (_y, r) in RIM_DISC_PROF][::-1]
    dy = [y for (y, _r) in RIM_DISC_PROF][::-1]
    y_disc_at_lip = _np.interp(r_lip, dr, dy)
    return float(y_disc_at_lip - y_lip)


CAP_SEAT_DY = _cap_seat_dy()            # 0.0477 m, derived
CAP_LIP_R = max(r for (_y, r) in _cap_prof())

# THE VENTS MUST STAY UNDER THE CAP, AND UNTIL REV 51 THEY DID NOT.
# rim()'s own comment already required it -- "They must stay under the hubcap
# ... they reach 0.1415, so only 7 mm of each crescent clears the cap" -- and
# then accepted the 7 mm.  THE PHOTOGRAPHS EXCLUDE IT.  A 5-fold angular
# harmonic test on the cream annulus just outboard of the cap returns a CLEAN
# NULL on every photograph we hold (A5 0.0024-0.0571, SNR 0.5-3.3), against the
# side-ortho render's own notch signature of A5 = 0.214 at SNR 8-11 on the same
# statistic -- which would have shown on IMG_2073 at 41 sigma and on ref_side at
# 46 sigma.  The notches are excluded outright, and NOT by the seating fix:
# seating moves the cap outboard but leaves the vents reaching 4.5 mm past its
# lip.  So the reach is now bounded by the cap, with the authored cutter SIZE
# kept and only the station moved (the smaller change of the two available).
VENT_CUT_R = 0.0235                     # authored cutter radius, unchanged
VENT_MARGIN = 0.0020                    # stated, not tuned: 2 mm inside the lip
VENT_CENTRE_R = CAP_LIP_R - VENT_CUT_R - VENT_MARGIN     # 0.1115, was 0.1180


def cap_clearance_check(seat_dy, log=print):
    """Is the seated cap in FRONT of the wheel disc across its whole face?

    NOT a tautology: it compares two INDEPENDENTLY AUTHORED surfaces -- the cap
    profile and rim()'s disc profile -- at a shift supplied by the caller.  Pass
    seat_dy = 0 (T1_CAPSINK=1) and it fires on the real, shipped-for-50-revisions
    defect, reporting the crossover radius.  Pass the derived seat and it clears.
    """
    cap = _cap_prof()
    S = T.RIM_R / 0.1905
    # FRONT HALF ONLY.  The profile is NOT monotonic in r: it runs from the apex
    # out to the lip and then RETURNS along the cap's back face, so sorting the
    # whole list by radius conflates the two surfaces and reads the return where
    # the front belongs.  My first version of this guard did exactly that and
    # fired on a correctly seated cap, reporting -7.1 mm at r = 0.1355 -- which
    # is the BACK point (-0.0035, R + 0.0010).  Cut at the outermost point.
    _imax = max(range(len(cap)), key=lambda i: cap[i][1])
    front = cap[:_imax + 1]
    crs = [r for (_y, r) in front]
    cys = [y + seat_dy for (y, _r) in front]
    dr = [r * S for (_y, r) in RIM_DISC_PROF][::-1]
    dy = [y for (y, _r) in RIM_DISC_PROF][::-1]
    rr = _np.linspace(0.0, CAP_LIP_R, 4001)
    gap = _np.interp(rr, crs, cys) - _np.interp(rr, dr, dy)
    worst = float(gap.min()); r_worst = float(rr[int(gap.argmin())])
    if worst < 0.0:
        bad = rr[gap < 0.0]
        raise AssertionError(
            "HUBCAP IS BURIED IN THE WHEEL DISC: the cream disc stands in front "
            "of the red cap from r = %.5f m outward (worst %.1f mm at r = %.4f). "
            "The five vent holes then look THROUGH the disc onto the cap and "
            "every wheel renders a FIVE-PETAL FLOWER.  Seat the cap: "
            "CAP_SEAT_DY = %.4f m, derived from the two profiles."
            % (float(bad.min()), worst * 1000, r_worst, CAP_SEAT_DY))
    if VENT_CENTRE_R + VENT_CUT_R > CAP_LIP_R + 1e-9:
        raise AssertionError(
            "VENT HOLES REACH PAST THE CAP: they reach r = %.4f against a cap "
            "lip of %.4f, so %.1f mm of each crescent clears the cap and cuts a "
            "DARK NOTCH into the cream annulus.  Five photographs return a clean "
            "5-fold null there (A5 0.0024-0.0571) against the notched render's "
            "A5 = 0.214, which would have shown at 41-46 sigma."
            % (VENT_CENTRE_R + VENT_CUT_R, CAP_LIP_R,
               (VENT_CENTRE_R + VENT_CUT_R - CAP_LIP_R) * 1000))
    log("  hubcap seated: +%.1f mm outboard (DERIVED), cap clears the disc by "
        "%.1f mm at worst (r %.4f); apex stands %.1f mm proud of the flange "
        "against a photographed %.1f +- 7 mm; vents reach %.4f under a lip of "
        "%.4f" % (seat_dy * 1000, worst * 1000, r_worst,
                  (0.0745 + seat_dy - 0.0640) * 1000, 52.2,
                  VENT_CENTRE_R + VENT_CUT_R, CAP_LIP_R))


# ref_side.jpg, rear wheel, crop box (736,591,764,619): the white emblem on the
# red dome spans 18 +/- 1 px vertically and 19 +/- 1 px horizontally against a
# hubcap disc of 58.370 px, so
#
#     emblem D / hubcap D = 0.317 +/- 0.017        photograph
#                           0.1897                 built (rev 14)   -> 7.0 sigma
#                           0.3170                 built (this fix)
#
# Same defect as the nose roundel and the same fix: a fraction of the disc it
# sits on, never a fresh absolute.  0.0345 was absolute.
CAP_EMBLEM_D = 0.3170 * CAP_D
CAP_EMBLEM_WFRAC = 0.2087           # w/R as authored (0.0072 / 0.0345), kept
# rev 54 -- WHAT THIS CONSTANT DENOMINATES IS NOT WHAT A PHOTOGRAPH MEASURES,
# and the top job is about to compare the two.  MEASURED, probe_rev54_wfrac.py:
# `vw_bars` is called with R=1.0 and the finished outline is then scaled by
# `_fit_glyph`, which reads the outline's OWN extreme corner.  That corner sits
# at rmax = 0.81400 of the nominal unit, not at 1.0 -- measured on isolated
# glyphs at four widths, and the same 0.814 at every one of them.  So
#
#     built stroke / OUTER RADIUS  =  wfrac / 0.81400
#         hubcap  0.2087 / 0.814 = 0.25639     (mesh, via the built caps: 0.2587)
#         nose    0.1986 / 0.814 = 0.24398     (vw_logo_fit's wfrac, the REAL
#                                               call site -- vw_logo's own
#                                               signature default is not used)
#
# A frame measures the SECOND column.  Comparing a frame against 0.2087 itself
# understates by 18.6 %.  The estimator was calibrated before it was believed:
# it recovers a known width to +0.33..+0.52 % over w = 0.12..0.28.
# The two badge DESIGNS differ by 5.09 %, and NEITHER has been compared to any
# frame.  That comparison is still the open half -- see PHOTOS_WANTED item 7.

# The emblem plate: ONE plane, ONE thickness, shared by the ring and the glyph.
# Named because rev 17 added the ring and the two must never drift apart -- the
# reference shows every stroke end running INTO the ring band, which is only
# true if they are coplanar.  Both numbers are inherited from the rev-15 glyph
# exactly as authored; nothing here re-derives them.
CAP_EMBLEM_PLANE = 0.0805           # offset of the plate's mid-plane along +n
CAP_EMBLEM_DEPTH = 0.0060           # plate thickness (prism is centred: +-half)

# rev 17.  THE HUBCAP RING -- rev 15 left it open ("this build has no hubcap
# ring at all") and it is now measured and built.
#
# What "the ring" is: the emblem is a VW inside a closed annulus, the same
# badge geometry as the nose roundel.  Its OUTER boundary is the emblem's own
# outer extent, i.e. exactly CAP_EMBLEM_D -- so the ring adds NO new diameter.
# The one new number is the band's radial width, as a fraction of that D.
#
# WHY THE BAND IS NOT MEASURED ON ref_side.jpg.  Measured this revision from an
# isolated step edge (the red dome / cream rim boundary, 720-ray erf fit):
#
#     ref_side.jpg      PSF sigma 1.625 px      emblem outer D  18.1 px
#     ref_workshop.jpg  PSF sigma 0.689 px      badge  outer D  91.7 px
#
# The band is ~0.09 D.  In ref_side that is 1.7 px = 1.05 sigma -- UNRESOLVED,
# and a half-level crossing there reads 0.18 D, double the truth, because the
# blurred band never reaches its own plateau.  In ref_workshop the same band on
# the same badge design is 8.0 px = 11.6 sigma -- RESOLVED.  This is precisely
# the compression asymmetry the rev-17 work list flagged, and it decides which
# frame the number comes from.
#
# MEASURED, all three ratios dimensionless and taken WITHIN one feature, so no
# px -> metre scale and no projective correction is involved:
#
#   ref_workshop.jpg nose badge, crop box (258,494,352,604)
#     vertical axis    band  8.021 +/- 0.119 px / outer D 91.729 px = 0.0874
#     horizontal axis  band  6.240 +/- 1.105 px / outer D 62.705 px = 0.0995
#   ref_side.jpg hubcap, crop box (700,550,805,660), PSF-forward-modelled
#     (ideal annulus blurred by sigma 1.625, fitted r = 4..14 px)     = 0.065
#         profile-likelihood: rms 2.10 at 0.08, 2.85 at 0.18, 3.72 at 0.28
#
#     ring band / ring outer D = 0.093 +/- 0.012        adopted
#
# ------------------------------------------------------------------- rev 57
# TWO VALUES FOR ONE BOUNDARY, AND NEITHER WAS RETRACTED.  F37.
#
# The block above gives this badge's ring OUTER D as 91.729 px vertical /
# 62.705 px horizontal.  `vw_logo_fit`'s docstring, further down THIS FILE and
# about THE SAME boundary in THE SAME frame and THE SAME crop box, gives
# 91.885 / 63.143 -- carried on into REFERENCE_FRAMES_rev45.md as SPEC
# 10.107's published conic.  They differ by 0.17 % and 0.70 %.  Nothing said
# which was live, and rule 34 says a requirement inherits its object exactly
# as a retirement does: before leaning on either, check which sentence is
# about what.  Recorded here rather than in a ledger alone, because rule 15
# says a retraction that lands in a ledger and not in the source is half a
# retraction.
#
# A THIRD, INDEPENDENT READING, rev 57 (probe_rev57_badge.py, sec.1): the
# outermost crossing of the half level between the local cream and the ring's
# own trough, walked INWARD and bounded per ray, then a conic fit --
#     vertical D 92.728 px   horizontal D 63.299 px   radial resid 0.2345 px
#     over 685 rays; the same trace at the 0.35 and 0.65 levels reads
#     93.388 / 64.068 (resid 0.1918) and 91.761 / 61.911 (resid 0.5807).
# So the edge LEVEL moves the vertical D by 1.8 % across that range, which is
# ten times the 0.17 % the two record values differ by.  NOTHING IS CHANGED
# HERE: the adopted 0.093 +/- 0.012 stands, and all three readings sit inside
# it.  What is fixed is that the disagreement is now stated where a reader
# meets it.
#
# AND THE BUILT BAND IS AT THE TOP OF THE ADOPTED RANGE.  Off vw_ring's own
# mesh the built band / outer D is 0.10086, against 0.09209 +/- 0.00292
# (threshold) and 0.09280 +/- 0.00319 (gradient) measured on this frame over
# 25 rays on the major axis, and against the 0.0874 above: +9.5 % and +15.4 %.
# It is INSIDE the adopted +/- 0.012 and is NOT changed -- moving it moves the
# glyph's fit radius with it, through `_BAND_FRAC = 0.028 / 0.140` in
# vw_logo_fit.  Reported as F38.  This is the FIRST comparison of either
# badge's BUILT geometry against a photograph; verify.py's own line says of
# the other one "hubcap badge is SELF-CONSISTENCY ONLY".
#
# The +/- is the vertical-vs-horizontal systematic on the workshop badge (its
# two sides read 5.24 and 7.34 px -- the badge is proud, so the near side shows
# its wall) plus the transfer to the hubcap.  CEILING: the statistical floor on
# the resolved measurement alone is +/- 0.0013; the transfer cannot be tested
# better than about +/- 0.03 in this photo set, because the hubcap's own band
# is 1.05 sigma wide in the only frame that shows it face-on.  No sharper
# number is available without a sharper photograph.
#
# The outer diameter was re-derived independently while doing this, with the
# same PSF forward model: outer R 9.04 +/- 0.15 px against a hubcap dome R of
# 29.06 px (erf fit) -> 0.311 +/- 0.007 against the locked 0.317 +/- 0.017,
# i.e. 0.35 sigma.  CAP_EMBLEM_D is confirmed and untouched.
#
# CORROBORATION, found after the fact and not used to derive anything: the NOSE
# roundel's ring, authored years ago in roundel() as the absolute R - 0.028,
# measures 0.1005 of its own built outer D (0.2802 m).  That is 0.6 sigma from
# the 0.093 measured here off the photograph.  Two rings authored by different
# routes agree.
#
# NEGATIVE CONTROL for "the ring is visible at all", ref_side.jpg, 720-ray
# angular-mean creamness annulus detector, radii 5-11 px:
#     at the emblem centre (748.15,606.00)   peak r 7.50 px, amp +55.0,
#                                            angular coverage 1.00 (720/720)
#     six centres displaced 16 px onto blank dome, same detector, same frame:
#                                            amp -16.3 .. -2.3, coverage
#                                            0.20 .. 0.51  -- no annulus
# and in ref_workshop.jpg the OTHER van's front hubcap (crop 610,680,700,770)
# is a plain cream dome with no roundel at all: the same detector run at
# ring-scale radii returns amp -13.3 .. -2.8, coverage 0.27 .. 0.32.
CAP_RING_BANDFRAC = 0.093           # band / ring outer D, measured above


def cap_ring(y, side):
    """the cream annulus the VW sits inside, coplanar with the glyph.

    Expressed ENTIRELY in terms of CAP_EMBLEM_D and the shared plate constants.
    There is no absolute metre value here on purpose: the glyph merged into an
    X twice because a size derived from another size was written down as a
    literal and went stale.  If CAP_EMBLEM_D moves, the ring moves with it and
    the strokes stay flush with the band, which is what the reference shows.
    """
    ro = CAP_EMBLEM_D / 2                       # = the glyph's own fit radius
    ri = ro * (1.0 - 2.0 * CAP_RING_BANDFRAC)   # band = 0.093 * outer D
    y0 = y + side * CAP_EMBLEM_PLANE - CAP_EMBLEM_DEPTH / 2
    y1 = y0 + CAP_EMBLEM_DEPTH
    return T.revolve([(y0, ri), (y1, ri), (y1, ro), (y0, ro)],
                     seg=96, axis='Y', name=f"capring{side}")


def cap_emblem(y, side):
    """white VW inside its ring, in the centre of the red dome.

    RELIEF, reported rather than invented: the ring's proud height is not
    measurable on the hubcap in any frame.  It is measurable on the nose badge
    -- the left and right bands of the workshop roundel read 5.24 and 7.34 px
    at an axis ratio of 0.684, and that asymmetry is the badge's own wall, so
    h ~ 1.44 px = 0.0157 of its outer D, about 4.4 mm on a 280 mm badge.  The
    plate this build already uses is 6.0 mm thick and stands 3-5 mm off the
    dome, which is right for the nose and about 4x too thick scaled to an
    87 mm hubcap emblem.  That is rev-15's glyph plane, it is not this
    revision's brief, and the ring MUST share whatever plane the glyph is in --
    so both now read the same two constants and neither was changed.

    EXPOSED BY BUILDING THE RING, reported not fixed because the cause is
    t1_core.vw_bars' V_SPINE which this file may not edit: the W's outer arms
    and legs land flush on the band (rmax 0.043429 = CAP_EMBLEM_D/2 exactly),
    but the V's arm tips reach only 0.031069, i.e. 0.7154 of the fit radius,
    while the band's inner edge is at 0.8140.  The V therefore stops 4.28 mm
    short of the ring -- 4.9 % of the emblem D -- where every reference frame
    shows both V arms running into the band.  Same defect on the nose roundel
    with the same spine (V reaches 0.7211 of that ring's outer radius, band
    inner at 0.7990 -> 10.9 mm short).  To close it, V_SPINE's tips must grow
    by a factor 0.8140 / 0.7154 = 1.138 about the apex, i.e. (+/-0.400, 0.560)
    -> (+/-0.455, 0.646), which leaves the arm angle and the W untouched.
    """
    glyph = T.vw_bars(1.0, CAP_EMBLEM_WFRAC,
                      (0.0, y + side * CAP_EMBLEM_PLANE, 0.0),
                      (1, 0, 0), (0, 0, 1), (0, side, 0), CAP_EMBLEM_DEPTH,
                      tag=f"capvw{side}")
    # _fit_glyph reads rmax off the objects it is GIVEN, so the ring must not
    # be in that list -- the ring is already at CAP_EMBLEM_D/2 and passing it
    # in would make the unit glyph's rmax the divisor for both and shrink the
    # ring by ~20x.  Fit first, then prepend.
    _fit_glyph(glyph, CAP_EMBLEM_D / 2, ax=('x', 'z'))
    return [cap_ring(y, side)] + glyph


def wheel_assembly(x, y, steer=0.0):
    grp = []
    t = tyre(f"tyre_{x:.2f}_{y:.2f}")
    keep(t, "rubber")
    b, d = rim(f"rim_{x:.2f}_{y:.2f}")
    keep(b, "wheelpaint"); keep(d, "wheelpaint")
    c = hubcap(f"cap_{x:.2f}_{y:.2f}")
    keep(c, "chrome")
    s = 1 if y > 0 else -1
    for o in (t, b, d, c):
        if s < 0:
            for v in o.data.vertices:
                v.co.y = -v.co.y
            T.fix_normals(o)
        place(o, loc=(x, y, T.TIRE_R), rot=(0, 0, steer))
        grp.append(o)
    return grp


# ================================================================== BUMPERS
def _plan_curve(z, x0, x1, steps=26):
    """(x, y) of the body surface at height z, x0 -> x1"""
    g = T.G(z)
    pts = []
    for i in range(steps + 1):
        x = x0 + (x1 - x0) * i / steps
        pts.append((x, T.WX(x) * g))
    return pts


# rev 10.  Donald read the front bumper as thin.  It is not: the blade section
# measures 0.110 +/- 0.010 m against BUMP_PROFILE's 0.113, and blade/wheel
# 0.166 +/- 0.016 in two frames agreeing to 2 %.  The blade is right and stays.
# The defect is the STANDOFF -- measured >= 0.080 m from the body (0.16 m from
# the tucked skin) against 0.032 m built.  A correct blade held tight against
# the body reads thin because nothing separates it from the shell.  SPEC 10.22.
# rev 10: this was moved to 0.0555 (80 mm of standoff) on a measurement that
# said ">= 0.08 m from the body against 0.032 m built", and then moved BACK,
# because a second, independent method refutes that application.
#
# The second method: the FRONTAL SILHOUETTE of ref_side.jpg. Scanning for the
# left-most vehicle column row by row, the nose crown stands at column 78 and
# the bumper blade's front face at 82-91 -- the bumper is 4-13 px BEHIND the
# crown, i.e. 17-56 mm behind it at the nose station's 231 px/m. At 0.0555 the
# blade lands 63 mm PROUD of the crown, which no scan of the photograph
# supports and which also breaks the locked overall length (4.327 against
# 4.290 +/- TOL -- verify.py caught it, as it should have).
#
# Two independent measurements and one locked dimension now agree against the
# standoff figure AS APPLIED. Most likely the ">= 0.08 m" is measured from the
# tucked apron at bumper height, not from the forward-most nose, and the build
# offsets along the apron normal -- i.e. the two numbers use different datums.
# Reverted pending a third method. SPEC 10.24, logged OPEN not closed.
BUMP_OFF = 0.0075          # standoff so the outer face lands on x = +/-2.140

BUMP_PROFILE = [           # (outward, up)  channel section, 108 mm tall
    (0.000, 0.0560), (0.0150, 0.0532), (0.0225, 0.0430), (0.0248, 0.0210),
    (0.0230, 0.0000), (0.0248, -0.0220), (0.0225, -0.0440),
    (0.0150, -0.0540), (0.000, -0.0570), (0.000, -0.0400),
    (0.0105, -0.0360), (0.0120, 0.0360), (0.000, 0.0400),
]


# ------------------------------------------------------------- rev 69, F222
# THE FRONT BUMPER'S PLAN BOW.  It stays on its own line as a bare literal so a
# verifier row can grep `^BUMP_BOW = 1.0`, exactly as NOSE_BULGE does.
#
# IT IS A FRACTION, NOT A MILLIMETRE FIGURE, AND THAT IS THE POINT.  1.0 means
# "follow the body's own plan curve exactly", which is what a wrap-around
# pressing does and what needs no photograph.  It is NOT a measurement of the
# real bus's bow -- that number cannot be recovered from what we hold (F231).
# When it arrives, from the parts literature or a frame shot from the other
# side, it replaces the BODY's NOSE_BULGE and this constant does not move.
#
# T1_BUMP_BOW is MEASUREMENT-ONLY and 0.0 restores the straight face's SHAPE.
# NOT the mesh: `n_f` went 12 -> 24 in the same edit, so the ablated bumper is
# 1105 verts against the pre-rev-69 949 and reads +0.22 mm rather than F222's
# historical +0.05.  Shape-identical, RE-TESSELLATED -- an adversary caught this
# stated as "bit for bit" in three places.  It is `verify.py`'s bumper-bow
# row's kill, and both arms go red on it.
BUMP_BOW = 1.0

# THE STATION WHOSE PLAN CURVE THE BLADE PARALLELS, un-dropped.
#
# NOT the blade's own height, and that distinction is the whole of rev 69's
# second wrong turn.  Draping the blade onto the body at its OWN z gave a bow of
# +1.56 mm and a lumpy profile, because at z = 0.4800 the body is down in the
# valance where it tucks under -- and, more to the point, because
# `nose_shape`'s bulge ellipse is `((z - 1.00) / 0.46)^2 <= 1`, i.e. z in
# (0.540, 1.460), so THE PLAN BOW IS SWITCHED OFF BELOW z = 0.540 and the
# bumper, the valance and the whole lower nose sit beneath it.  The flat bumper
# was a SYMPTOM of that, not an independent defect.
#
# A REAL BUMPER IS NOT THE BODY'S SECTION AT ITS OWN HEIGHT.  It is a separate
# pressing standing off on irons, and its plan curve PARALLELS the front face.
# So the blade takes its SHAPE from the face and keeps its own standoff.
#
# WHY 1.100 AND NOT THE ELLIPSE'S CENTRE.  This paragraph argued for 1.000 --
# "the bulge ellipse's own centre height" -- while the constant said 1.100, and
# an adversary caught the mismatch: the station was moved to clear the HEADLAMP
# BORES (at 1.000 the sampling ray runs through them at 4 of 23 stations, and
# the refusal below fired) and the prose was not rewritten.
#
# AND THE BAND IT QUOTED WAS FROM THE WRONG INSTRUMENT.  It said "the shell
# reads +19.6 .. +20.0 mm of bow across the whole face"; those are `verify`'s
# max-x-in-a-y-bin figures, not the raycast THIS code uses.  Measured on the
# drape's own quantity, s(0) - s(corner), over the build's own stations,
# un-dropped:
#     0.650 +14.64 | 0.800 +20.74 | 1.100 +21.07 <- SHIPPED | 1.200 +19.46
#     1.300 +14.89 | 1.400  +9.71
# So the true spread across the whole face is +9.7 .. +21.4 mm, and "worth well
# under a millimetre" holds ONLY inside un-dropped 0.800..1.150 (spread
# 0.63 mm).  1.100 sits in the middle of that plateau AND clears the bores by
# 81 mm.  Both reasons are the reason; neither alone would fix the station.
#
# THIS INVENTS NO NUMBER.  The bow is the model's OWN front face, measured by
# raycast at build time, not a figure taken from a photograph -- which is the
# right posture, because the real bus's bow CANNOT be recovered from the frames
# we hold (F231).  When that number arrives it moves NOSE_BULGE, and the blade
# follows it for free.
BUMP_BOW_Z = 1.100


def _bump_bow():
    v = os.environ.get("T1_BUMP_BOW")
    return BUMP_BOW if v is None else float(v)


def _nose_plan_x(z):
    """Return f(y) -> the body's outer skin x at (y, z), or None if no body.

    RAYCASTS THE BUILT SHELL, which is the only honest source for "where is the
    body at this station": `_plan_curve`'s `T.WX(x) * T.G(z)` is the LOFT's
    authored half-width and knows nothing about `nose_shape`'s plan bulge, so a
    bumper built from it would go straight back to ignoring the nose (F217's
    failure mode, one object over).

    Returns None rather than guessing when `T1_body` is not in the scene -- a
    bumper built with no body to follow must fall back to the straight face and
    SAY SO, not silently invent a curve (rule 37)."""
    try:
        import bpy
    except Exception:
        return None
    ob = bpy.data.objects.get("T1_body")
    if ob is None:
        return None
    mw = ob.matrix_world
    inv = mw.inverted()
    d = (inv.to_3x3() @ Vector((-1.0, 0.0, 0.0))).normalized()

    def f(y):
        hit, loc, _n, _i = ob.ray_cast(inv @ Vector((3.5, y, z)), d)
        if not hit:
            return None
        wx = (mw @ loc).x
        return wx if wx > 1.5 else None      # fell through an aperture
    return f


def bumper(front=True, z=0.4800, name="bumper"):
    """
    Swept channel following the body plan curve.  Traversal order is chosen so
    that sweep()'s side vector (tangent x up) always points OUTBOARD:
      front:  -Y flank forward -> across the flat nose face -> +Y flank back
      rear:   +Y flank aft     -> across the flat tail face -> -Y flank forward
    """
    if front:
        # ------------------------------------------------------- rev 44
        # THE FRONT BUMPER OVERLAPPED THE CAB DOOR.  He reported it; measured
        # on the built mesh it is unambiguous: `bumper_f` ran x 1.7350..2.1403
        # while the door aperture starts at DOOR_X1 = 1.8171, so 82 mm of
        # bumper sat INSIDE the door, and 89 of its 91 vertices in that span
        # were ABOVE the door's own bottom outline -- the worst by 114 mm.
        # In ref_nolita_doorshut.jpg the bumper's aft end is plainly FORWARD of
        # the door's lower-front corner; the two never meet.
        #
        # 1.735 was a BARE LITERAL with no derivation, and SPEC 10.72 had
        # already struck the bumper's x extents as UNMEASURED ("X_BUMP_F/R have
        # zero read sites ... neither value is measured").  So there is nothing
        # to preserve, and the aft end is now EXPRESSED IN TERMS OF THE DOOR it
        # must not touch rather than re-typed -- SPEC 10.25's rule, which is
        # exactly the coupling this project keeps getting burned by.
        #
        # A CLEARANCE, NOT A MEASUREMENT.  The reference cannot give the wrap
        # length to better than a few centimetres at 480 px, so this does not
        # pretend to: it takes the hard geometric constraint (the bumper may
        # not enter the door aperture), adds 10 mm, and stops.  The wrap goes
        # 373 mm -> 281 mm as a consequence, and that consequence is stated
        # rather than tuned.
        import t1_shell as _SH
        _aft = max(p[0] for p in _SH.DOOR_GAP_S) + 0.010
        raw = _plan_curve(z, _aft, 2.108, 30)           # x increasing
        nose = raw[-1]
        _bow = _bump_bow()
        _skin = _nose_plan_x(BUMP_BOW_Z)       # the FACE's station, not the blade's
        _s0 = _skin(0.0) if _skin is not None else None

        def _drape(_y):
            """the face's x offset at half-width _y: 0 at the centreline,
            drawing back to the corner.  None if the skin cannot be read."""
            if _skin is None or _bow == 0.0 or _s0 is None:
                return 0.0
            _v = _skin(abs(_y))
            return None if _v is None else _bow * (_v - _s0)

        TAPER_N = 8                    # wrap points that blend the offset in
        _raw2, _tmiss = [], 0
        for _i, (_x, _y) in enumerate(raw):
            _t = max(0.0, (_i - (len(raw) - 1 - TAPER_N)) / float(TAPER_N))
            _w = _t * _t * (3 - 2 * _t)
            _d = _drape(_y) if _w > 0 else 0.0
            if _d is None:
                _tmiss += 1
                _d = 0.0
            _raw2.append((_x + _w * _d, _y))
        raw = _raw2
        nose = raw[-1]
        seq = [(x, -y) for (x, y) in raw]
        # ------------------------------------------------------ rev 69, F222
        # THE NOSE FACE FOLLOWS THE BODY'S PLAN CURVE.  IT USED TO BE A STRAIGHT
        # LINE, AND THAT WAS THE DEFECT.
        #
        # WHAT STOOD HERE:
        #     for i in range(1, 12):                    # flat nose face
        #         seq.append((nose[0], -nose[1] + 2 * nose[1] * i / 12))
        # -- eleven points at CONSTANT x.  Measured on the built mesh, the front
        # bumper's plan bulge over |y| <= 0.70 was +0.05 mm: DEAD FLAT, by
        # construction, over precisely the span the photographs are traced on.
        # The photographed bumper's near half is curved at 11-14 sigma, and that
        # sign is PROJECTION-INVARIANT -- a straight 3-D line images straight
        # under any pinhole camera at any pose -- so the defect needs no camera
        # model, no EXIF and no distortion term to establish (F222).
        #
        # WHY THIS IS NOT A GUESSED NUMBER, AND WHY IT NEEDED NO PHOTOGRAPH.
        # The plan bow's MAGNITUDE cannot be recovered from the frames we hold
        # (F231: every frame is shot from the same front-left quarter, so the
        # far-side landmarks are on or beyond the silhouette; the bores in the
        # one bare-shell frame are EMPTY and read their own interior wall; and
        # the parts literature is EGRESS_BLOCKED here).  So this does not invent
        # one.  A wrap-around bumper is a pressing that FOLLOWS THE BODY, and
        # the body's own plan curve at this blade's height is already built and
        # already measured: the shell carries +8.26 mm of plan bulge there while
        # the bumper carried +0.05.  A bumper flat against a curved body is
        # INTERNALLY INCONSISTENT whatever the photograph says.  So the face is
        # draped onto the body, exactly as the roundel is (`T.drape_x`), and the
        # bumper now follows `NOSE_BULGE` and everything else for free -- which
        # is F217's lesson applied to a much larger object.
        #
        # THE STANDOFF IS PRESERVED AT THE CENTRELINE, so this changes the bow
        # and nothing else: `dx` is measured at y = 0 and subtracted, leaving
        # x(0) exactly where it was.  A rebuild with BUMP_BOW = 0 is the old
        # straight line, bit for bit -- that is the ablation the guard is
        # watched failing under.
        # A PARTIALLY DRAPED FACE IS WORSE THAN EITHER, AND MY FIRST CUT BUILT
        # ONE SILENTLY.  RULE 37, in code whose own docstring forbids it.
        #
        # `_nose_plan_x` returns None per point when the ray misses, and the
        # first version of this loop left that point at `nose[0]` and said
        # nothing.  Built, it produced a face that dipped 7.8 mm at |y| = 0.15
        # and came back to -0.1 mm at 0.70 -- NON-MONOTONE, with a net bow of
        # +0.15 mm, i.e. still flat.  The draped points had moved and the
        # missing ones had not, and nothing in the log said so.  The misses are
        # now COUNTED and a face that cannot be fully draped is REFUSED.
        # ANCHORED AT THE CENTRELINE, AND THE WRAP IS TAPERED TO MEET IT.
        #
        # THE ANCHOR DECIDES WHERE THE WHOLE BLADE SITS, NOT JUST ITS SHAPE, AND
        # AN ADVERSARY CAUGHT REV 69 GETTING THAT WRONG.  Anchoring at the
        # CORNER holds the corners still and sends the centre 21 mm FORWARD.
        # That built a correct bow and three side effects, all with VERIFY green:
        #   - the blade's front face went 2.1403 -> 2.1614, i.e. +34.4 mm proud
        #     of the nose crown, where the rev-10 scan recorded in this very
        #     file says the bumper images 17-56 mm BEHIND the crown -- the same
        #     direction as a move this project already REVERTED once;
        #   - `bumper_irons` are frozen at x = 2.045 + 0.150, so the blade's back
        #     face at IRON_Y pulled AWAY from its own brackets: +4.5 mm of
        #     overlap became -10.1 mm of OPEN AIR, and nothing measured it;
        #   - the subject bbox grew, and `studio.fit_view` centres and fills
        #     0.92 of the frame from `subject_bbox()`, so EVERY preview reframed.
        #
        # ANCHORING AT THE CENTRELINE INSTEAD holds x(0) exactly where it was
        # and draws the CORNERS BACK, which is the same bow and none of the
        # three.  It also deepens the iron overlap instead of breaking it.
        #
        # THE STEP THAT MADE ME REJECT THIS FIRST TIME IS REAL AND IS FIXED
        # HERE.  `raw` ends at the corner, so a face anchored at the centre no
        # longer meets it -- my first cut left an 8 mm discontinuity and built a
        # lumpy outline (-8.22 mm at |y| = 0.10, recovering to -0.22 at 0.70).
        # The wrap's last TAPER_N points now take the same offset through a
        # smoothstep, so the flank is untouched, the corner carries the full
        # offset, and the junction is continuous BY CONSTRUCTION.
        n_f = 24                               # was 12; the curve needs samples
        _face, _miss = [], 0
        for i in range(1, n_f):
            _y = -nose[1] + 2 * nose[1] * i / n_f
            _sy = _skin(_y) if (_skin is not None and _bow != 0.0) else None
            if _skin is not None and _bow != 0.0 and (_s0 is None or _sy is None):
                _miss += 1
            _face.append((_y, _sy))
        # AND THE NO-BODY PATH MUST REFUSE TOO.  An adversary found that the
        # verifier row written for this refusal exercised the ONE BRANCH THAT
        # DOES NOT REFUSE: with `_skin is None` the miss counter stays 0, no
        # error is raised, and the face is built FLAT -- the exact defect this
        # code exists to remove -- behind nothing but a suffix on a log line.
        # A flat face is not a fallback, it is the defect (rule 37).
        if _skin is None and _bow != 0.0:
            raise RuntimeError(
                "t1_detail.bumper: there is no T1_body in the scene to drape "
                "the nose face onto, so the face would be built FLAT -- which "
                "is the defect F222 exists to remove, not a safe fallback. "
                "Build the body first, or set T1_BUMP_BOW=0 deliberately.")
        _miss += _tmiss
        if _miss:
            raise RuntimeError(
                "t1_detail.bumper: the nose face could not be draped onto the "
                "body at %d of %d stations (z=%.4f) -- the raycast found no "
                "skin forward of x=1.5 there. A PARTIALLY draped face is not a "
                "plan curve: it dips where the ray hit and stays flat where it "
                "missed. Fix the station or set T1_BUMP_BOW=0 deliberately; do "
                "NOT ship the half-draped face (F222, rule 37)."
                % (_miss, n_f - 1, z))
        _prof = []
        _x0 = nose[0] - (_drape(nose[1]) or 0.0)     # the centreline's own x
        for _y, _sy in _face:
            _x = nose[0] if _sy is None else _x0 + _bow * (_sy - _s0)
            _prof.append((_y, _x))
            seq.append((_x, _y))
        # LOG WHAT WAS ACTUALLY BUILT, not what was intended.  Rev 69 inferred
        # this profile from the finished mesh twice and was wrong both times --
        # the mesh is a SWEPT CHANNEL whose section rotates with the path, so
        # max-x over the object is not the path.  Print the path.
        if _prof:
            _xs = [p[1] for p in _prof]
            _mid = min(_prof, key=lambda p: abs(p[0]))
            print("  bumper_f nose face: BUMP_BOW %.3f, %d stations, path x "
                  "%.4f..%.4f, bow at y=0 %+.2f mm vs the corner (shape taken "
                  "from the face at z=%.3f)%s"
                  % (_bow, len(_prof), min(_xs), max(_xs),
                     1000 * (_mid[1] - nose[0]), BUMP_BOW_Z,
                     "" if _skin is not None else "  [NO BODY -- face left FLAT]"))
        seq += [(x, y) for (x, y) in reversed(raw)]
    else:
        # rev 16: anchored to the tail skin (was -1.775 / -2.108, i.e.
        # X_TAIL_OLD + 0.333 and X_TAIL_OLD exactly).
        raw = _plan_curve(z, T.X_TAIL + 0.333, T.X_TAIL, 28)   # x decreasing
        tail = raw[-1]
        seq = [(x, y) for (x, y) in raw]
        for i in range(1, 12):                          # flat tail face
            seq.append((tail[0], tail[1] - 2 * tail[1] * i / 12))
        seq += [(x, -y) for (x, y) in reversed(raw)]

    n = len(seq)
    path = []
    for i, (x, y) in enumerate(seq):
        j0, j1 = max(0, i - 1), min(n - 1, i + 1)
        tg = Vector((seq[j1][0] - seq[j0][0], seq[j1][1] - seq[j0][1], 0))
        tg.normalize()
        nrm = Vector((tg.y, -tg.x, 0))                  # outboard by construction
        path.append((x + nrm.x * BUMP_OFF, y + nrm.y * BUMP_OFF, z))
    return T.sweep(path, BUMP_PROFILE, up=(0, 0, 1), name=name)


# HOISTED IN REV 37, VALUES UNCHANGED.  These three were written inline below.
# SPEC 10.91 stands the over-rider POSTS on the bumper irons, and this project's
# rule (SPEC 10.25) is that a constant tuned against another constant must be
# EXPRESSED IN TERMS OF IT -- otherwise moving the iron would silently leave the
# post behind.  This is a HOIST ONLY: every guard figure must be unchanged after
# it, and that was checked at both subdivision levels before anything was built.
IRON_Y = 0.470             # bumper iron lateral station, rev 16
IRON_W = 0.062             # iron section across y
IRON_H = 0.030             # iron section in z


def bumper_irons(front=True):
    obs = []
    x = 2.045 if front else (T.X_TAIL + 0.078)   # rev 16: was -2.030
    z0, z1 = 0.470, 0.585
    for s in (1, -1):
        pts = T.rrect(IRON_W, IRON_H, 0.010, seg=3)
        obs.append(T.solid_prism((x, s * IRON_Y, 0.525), (0, 1, 0), (0, 0, 1),
                                 (1, 0, 0), pts, 0.150,
                                 name=f"iron{s}{'F' if front else 'R'}"))
    return obs


# ---------------------------------------------------------------------------
# SPEC 10.83, rev 30.  THE FRONT OVER-RIDER BAR.  WORKSHOP-STAGE.
#
# The owner ruled in rev 26 (SPEC 10.75) that the transverse tube across the
# nose of `ref_workshop.jpg` is ON THE BUS, and chose MODEL IT, TAGGED
# WORKSHOP-STAGE.  Nothing was built for four revisions because there was no
# scale on the nose/bumper plane.  rev 30 measured one.
#
# EVERY NUMBER BELOW CARRIES ITS PROVENANCE.  Three different grades:
#
#   MEASURED, scale-free, on ref_workshop.jpg (probe_orb_blade.py):
#     tube / headlamp-aperture-vertical  = 0.1387, over 76 columns, +-5.5 %
#     tube top -> bumper blade top       = 38.7 px at the same station
#     Both are ratios to ONE ruler, the headlamp aperture, whose lower rim the
#     OWNER placed on the thin dark line in rev 30 -> vertical extent 71.11 px.
#
#   BOUNDED, model-free (probe_orb_hoop.py):
#     D <= 10.38 px.  The smallest horizontal chord anywhere on the hoop bend
#     is an upper bound on the diameter for ANY axis slope, because
#     W_h = D sqrt(1+s^2) >= D.  This is what EXCLUDED the second arm of the
#     question the owner answered CAN'T TELL (14.98 px, 44 % over the bound).
#
#   CATALOGUE-ANCHORED, therefore SPEC 10.72's struck class, and tagged as such
#   wherever it appears:
#     the aperture is taken as 0.180 m.  That is a STOCK T1 figure, NOT a
#     measurement of this vehicle.  It is the ONLY step between the measured
#     ratios and metres, and if it moves, BAR_DIA and BAR_RISE move with it
#     PROPORTIONALLY -- which is why they are written as the ratio times the
#     anchor, not as bare numbers.
#
#   UNMEASURED, and named rather than implied:
#     the bar's STANDOFF in x.  A depth cannot be recovered from this frame.
#     The convention adopted is that the bar's outer face lands in the SAME
#     plane as the bumper blade's, x = 2.1403, which is a CHOICE, not a
#     reading.
#     the bar's lateral EXTENT and the hoop ends' radius.  REF section 9 warns
#     that lateral scale varies by more than 2:1 across this panel and that a
#     fitted projection model did not close, so no lateral metre figure is
#     admissible.  BAR_HALF_Y is set to span the nose the way the photograph
#     shows and is tagged E -- shape from the photograph, dimension not.
#
# NOT BUILT, deliberately: the vertical POST (SPEC 10.75's box C).  rev 30
# REFUTES 10.75's description of it as being "at the vehicle's centreline":
# the centreline is the two-tone V apex at u = 311.5 (REF section 9) and the
# post's own columns are 357-374.  Its lateral position is bracketed only
# between the centreline and the near headlamp, which is not a measurement.
# Building it at a refuted position would be worse than leaving the gap named.
#
# CORRECTED TWICE SINCE, AND THE FIVE LINES ABOVE ARE KEPT ONLY AS THE RECORD
# OF WHAT REV 30 BELIEVED (SPEC 10.86, rev 32):
#   * "REFUTES" is wrong.  SPEC 10.84 (rev 31) downgraded it to UNDECIDED --
#     the two terms are at DIFFERENT DEPTHS, the apex on the nose skin and the
#     post in the bumper plane, separated by a standoff this file itself calls
#     "a CHOICE, not a reading" twenty lines up.
#   * "u = 311.5" is wrong.  SPEC 10.85 (rev 31b): that point is the V's RIGHT
#     ARM's occlusion point at the over-rider bar THIS FILE BUILDS, not the
#     apex.  The apex is at u = 288.8 +- 3 px.
#   * "357-374" is a POINTER box that rev 30 took a number from.  rev 32
#     re-measured it properly at u 355-377 (cream-run scan, rows 676-700), so
#     the number survives to within 2 px; the process defect stands.
# WHAT IS UNCHANGED: the post is NOT BUILT, and neither position is settled.
# rev 32 measured two routes to its lateral position and published both as
# NOT CLOSING on this frame -- see SPEC 10.86.
APERTURE_M = 0.1800        # CATALOGUE, stock T1.  SPEC 10.72's class.  TAGGED.
BAR_RATIO = 0.1387         # MEASURED, scale-free, 76 columns, +-5.5 %
BAR_RATIO_MAX = 0.1460     # BOUNDED, model-free, from the hoop chord
BAR_RISE_RATIO = 38.7 / 71.1109    # MEASURED: tube top above blade top
BAR_DIA = BAR_RATIO * APERTURE_M           # 0.02497 m
BAR_RISE = BAR_RISE_RATIO * APERTURE_M     # 0.09797 m
BLADE_TOP_Z = 0.4800 + 0.0560              # bumper() z + BUMP_PROFILE max
BAR_Z = BLADE_TOP_Z + BAR_RISE - BAR_DIA / 2.0
BAR_X = 2.1403 - BAR_DIA / 2.0             # outer faces coplanar -- a CHOICE
# ---------------------------------------------------------------------------
# rev 36, SPEC 10.90.  THE HOOP ENDS NOW MEET THE BUMPER.
#
# THE OWNER'S REPORT (rev 35, verbatim): "the upper bar appears to also connect
# with the main bumper on either end.  In the current version, there is no
# connection made."  And rev 36, shown the far end: "that circle is the post
# that connects the bumper to the bar, and both continue past the post.  past
# that, out of sight the bar wraps downwards, and meets with the bumper, the
# same way it does on the close side."
#
# THREE THINGS WERE WRONG WITH THE OLD END, AND ONLY ONE OF THEM WAS THE GAP.
#
# 1. THE GAP.  Measured by RAY-CAST THROUGH THE BUILT SCENE, not by arithmetic
#    on constants: 23.59 mm of clear air, 0.945 x BAR_DIA, both ends, symmetric
#    to 0.002 mm.  Rev 35 published 8.1 mm PLUS a second, fore-aft gap of
#    52.4 mm.  THERE WAS ONE GAP, NOT TWO, and it was 2.9x the published size;
#    the tip sits 0.51 mm behind the blade face, coplanar by construction.  Both
#    of rev 35's figures came from spending BAR_END_DROP and BAR_END_BACK AT
#    FULL VALUE when the code turned the hoop only 0.62 of a quarter turn.
#    A CLAIM IN PROSE IS NOT A GUARD -- and neither is a claim read off a
#    constant whose consumer modifies it.
#
# 2. A TANGENT DISCONTINUITY.  The old arc's first segment left the horizontal
#    bar at 61.2 deg below horizontal INSTANTLY -- a kink in a swept tube, which
#    is a modelling error needing no measurement to call -- and then FLATTENED
#    to 43.4 deg by its end, because the rearward BAR_END_BACK term grew faster
#    than the drop term.  Nobody had looked at the tangent.
#
# 3. IT FLATTENED WHERE THE PHOTOGRAPH STEEPENS.  Tracing the tube's centreline
#    through the near bend of ref_workshop.jpg (111 samples; the tube's own
#    apparent diameter, 10.0 px, is the scale ruler, so the result is
#    SCALE-FREE): horizontal, then a bend of radius 1.35 tube diameters, then a
#    descent at 69 deg below horizontal which it HOLDS.  Bend then steepen --
#    the opposite of kink then flatten.
#
# GRADES.  Two measured ratios, each stated WITH THE DIRECTION OF ITS BOUND,
# and everything else derived:
#
#   BEND_R_RATIO  MEASURED, image, scale-free.  A LOWER BOUND on the true
#                 radius -- the bend plane is foreshortened, which compresses it
#                 and makes the bend look tighter than it is.
#   BEND_THETA    MEASURED, image.  An UPPER BOUND on the true angle, by the
#                 same foreshortening, in the same direction.
#   BAR_LEG_LEN   DERIVED.  Solved so the tube's end lands ON the blade.
#   BAR_HALF_Y    DERIVED.  No longer a free grade-E constant.
#
# THE BAR'S OUTER EXTENT DOES NOT MOVE.  `BAR_HALF_Y = 0.6000` was graded E with
# the comment "spans the nose as photographed, NOT measured" -- so what was
# matched to the photograph was the bar's VISIBLE SPAN, i.e. its TIPS.  The tip
# is therefore FROZEN at exactly its rev-30..35 value, written as the OLD
# FORMULA so the equality is provable rather than asserted, and BAR_HALF_Y now
# follows from it.  Every fraction this project has published about this
# assembly carries BAR_HALF_Y in its denominator; freezing the tip rather than
# the root is what keeps the silhouette identical while the end changes.
#
# BAR_END_BACK IS RETIRED, NOT RE-TUNED.  Grade E, no support, and its only
# effect was to carry the hoop's end 17.5 mm rearward -- off the back of a blade
# top face only 24.8 mm deep, so NO amount of extra drop could ever have landed
# the tube on it.  The hoop is now planar at BAR_X.
#
# WHAT IS STILL NOT KNOWN, stated rather than papered over: WHERE ALONG THE BAR
# the junction sits.  He says the bar continues past the far post and wraps out
# of sight, so the span is a LOWER bound, not a reading.  A construction to
# recover it was ENUMERATED AND ABANDONED BEFORE IT WAS BUILT: a 1-D
# projectivity needs three collinear images; the two posts give two; the third
# would have to be the centreline's image AT THE BAR'S HEIGHT AND DEPTH --
# exactly the feature SPEC 10.89 killed the harmonic route for lacking.
# u = 288.8 is the V-swage apex, a different height at a different depth.
# THE SAME MISSING FEATURE, A THIRD TIME.  Not opened.
_OLD_HALF_Y = 0.6000                        # rev 30-35's value, to freeze the tip
_OLD_DROP = 2.6 * BAR_DIA                   # rev 30-35's BAR_END_DROP
_OLD_AMAX = 0.62 * math.pi / 2.0            # rev 30-35's capped sweep angle
BAR_TIP_Y = _OLD_HALF_Y + 0.55 * _OLD_DROP * math.sin(_OLD_AMAX)    # FROZEN

BEND_R_RATIO = 1.35                         # MEASURED image, LOWER bound
BEND_R = BEND_R_RATIO * BAR_DIA
BEND_THETA = math.radians(69.0)             # MEASURED image, UPPER bound

# THE LANDING DATUM IS NOT `BLADE_TOP_Z`.
#
# The first version of this derivation landed the tube on BLADE_TOP_Z and the
# built gap came out at 2.32 mm instead of zero.  BLADE_TOP_Z is the blade's
# CROWN -- `bumper() z + BUMP_PROFILE max` -- and BUMP_PROFILE's max sits at
# outward 0.000, hard against the body.  The channel's top face SLOPES AWAY
# from there: 0.0560 at outward 0, 0.0532 at 0.0150, 0.0430 at 0.0225.  The
# tube stands at outward 0.0123, where the blade is 2.30 mm lower than its
# crown -- which is the 2.32 mm, to 0.02 mm.
#
# A DATUM ERROR, the same family as SPEC 10.24's indicator-lens depth, which
# was applied and then refuted because it measured proud-of-PLINTH against a
# body-skin target.  Caught here by a ray-cast, not by re-reading the algebra.
# Recorded, not quietly fixed.
#
# BLADE_TOP_Z IS DELIBERATELY LEFT ALONE.  It is the datum for BAR_Z and for
# verify.py's over-rider row ("97.51 mm above the blade top"); moving it to
# suit this derivation would silently move the bar's height and re-baseline a
# guard.  The landing datum is a SEPARATE, LOCAL quantity.
def _blade_top_at(outward):
    """World z of the bumper channel's UPPER face at a given outward offset.

    Interpolates BUMP_PROFILE's top edge -- the run of points with decreasing
    'up' from the crown -- so this tracks the profile if the profile changes,
    rather than restating a number from it.
    """
    # The top edge runs from the crown outward, with 'up' falling and 'outward'
    # rising.  Stop as soon as EITHER stops holding, or the walk carries on
    # round the outer face and down the underside -- which is monotonic in 'up'
    # but NOT in 'outward', and would make the bracketing search ambiguous.
    top = []
    for o, u in BUMP_PROFILE:
        if top and (u >= top[-1][1] or o <= top[-1][0]):
            break
        top.append((o, u))
    if len(top) < 2:
        raise RuntimeError("BUMP_PROFILE has no descending top edge")
    if outward <= top[0][0]:
        return 0.4800 + top[0][1]
    for (o0, u0), (o1, u1) in zip(top, top[1:]):
        if o0 <= outward <= o1:
            t = (outward - o0) / (o1 - o0)
            return 0.4800 + u0 + t * (u1 - u0)
    return 0.4800 + top[-1][1]


# DERIVED.  A tube's end cap is a disc normal to the tangent, so for a tube of
# radius r whose axis descends at THETA the cap's lowest point sits
# r*cos(THETA) below the axis end -- and, the tangent lying in the y-z plane,
# that lowest point sits at x = BAR_X exactly.  Solve the straight leg that
# puts THAT point on the blade's top face AT THAT STATION.
_BAR_R = BAR_DIA / 2.0
_PROF_MAX_OUT = max(o for o, _ in BUMP_PROFILE)     # 0.0248
_BLADE_PATH_X = 2.1403 - _PROF_MAX_OUT              # the sweep path's own x
_BAR_OUTWARD = BAR_X - _BLADE_PATH_X                # where the tube stands
_LAND_Z = _blade_top_at(_BAR_OUTWARD)               # THE LANDING DATUM
_Z_AXIS_END = _LAND_Z + _BAR_R * math.cos(BEND_THETA)
_DROP_TOTAL = BAR_Z - _Z_AXIS_END
_DROP_BEND = BEND_R * (1.0 - math.cos(BEND_THETA))
BAR_LEG_LEN = (_DROP_TOTAL - _DROP_BEND) / math.sin(BEND_THETA)     # DERIVED
_Y_EXC = BEND_R * math.sin(BEND_THETA) + BAR_LEG_LEN * math.cos(BEND_THETA)
BAR_HALF_Y = BAR_TIP_Y - _Y_EXC                                     # DERIVED
assert BAR_LEG_LEN > 0.0, "the bend alone over-runs the blade"
assert BAR_HALF_Y > 0.0, "the bend consumes the whole bar"


def overrider_bar(name="orb_bar"):
    """The transverse over-rider tube across the nose.  Each end turns down
    through a TRUE CIRCULAR BEND, tangent to the bar where it leaves it, then
    runs straight until it meets the bumper's top.  Workshop-stage.

    The bend stops at BEND_THETA (69 deg) rather than at vertical, which is
    both what the photograph measures AND what keeps sweep() away from its
    frame singularity: sweep()'s side vector is t x UP, whose magnitude here is
    cos(BEND_THETA) = 0.358, not zero.  The old code dodged that singularity by
    capping the turn at 0.62 of a quarter turn -- A NUMERICAL WORKAROUND THAT
    HAD BECOME THE SHAPE, and therefore the gap the owner reported.
    """
    path = []
    n = 24
    for i in range(n + 1):
        y = -BAR_HALF_Y + 2 * BAR_HALF_Y * i / n
        path.append((BAR_X, y, BAR_Z))
    for s, at in ((-1, 0), (1, len(path))):
        arc = []
        m = 10
        for k in range(1, m + 1):                       # circular bend
            a = BEND_THETA * k / m
            arc.append((BAR_X,
                        s * (BAR_HALF_Y + BEND_R * math.sin(a)),
                        BAR_Z - BEND_R * (1.0 - math.cos(a))))
        y_t = BAR_HALF_Y + BEND_R * math.sin(BEND_THETA)
        z_t = BAR_Z - BEND_R * (1.0 - math.cos(BEND_THETA))
        for k in range(1, 4):                           # straight leg
            L = BAR_LEG_LEN * k / 3.0
            arc.append((BAR_X,
                        s * (y_t + L * math.cos(BEND_THETA)),
                        z_t - L * math.sin(BEND_THETA)))
        if at == 0:
            path = list(reversed(arc)) + path
        else:
            path = path + arc
    prof = T.rrect(BAR_DIA, BAR_DIA, BAR_DIA / 2.0, seg=6)
    return T.sweep(path, prof, up=(0, 0, 1), name=name)


# ---------------------------------------------------------------------------
# SPEC 10.91, rev 37.  THE OVER-RIDER POSTS.  WORKSHOP-STAGE.
#
# THE OWNER'S RULING, rev 26 (SPEC 10.75), box C at (357,681)-(374,697):
#   "ON THE BUS -- an over-rider joining A to B."
# and the SCOPE he set in the same exchange: "MODEL THEM, TAGGED WORKSHOP-STAGE."
# THE BAR (box A) WAS BUILT IN REV 30.  THE POST WAS NOT, FOR ELEVEN REVISIONS,
# and the instruction had been lost from every carrier that crosses contexts --
# it survived only in memory.  Recovered in rev 37 by checking the brief against
# memory BEFORE opening the code, which is exactly why SPEC 10.90 says to.
#
# THERE ARE TWO POSTS, NOT ONE (SPEC 10.90.7, rev 36).  10.83 spent five
# revisions trying to place "the post at the centreline"; the question was
# unanswerable because it assumed there was one.  They straddle it.
#
# WHY THIS ADDS NO NEW CONSTANT -- the whole point of the entry.
# Rev 36 RETIRED two grade-E constants (BAR_END_DROP, BAR_END_BACK).  Adding a
# member back with two fresh grade-E constants would be a net provenance loss on
# the same assembly one revision later.  It is not necessary:
#
#   POST_Y   = IRON_Y     the EXISTING bumper-iron station (rev 16).  A post is
#                         carried by the bumper's own bracket.  This is a
#                         STRUCTURAL INFERENCE, NOT A READING OF THE FRAME, and
#                         it is graded and falsifiable, not asserted -- see the
#                         two predictions below.
#   POST_DIA = BAR_DIA    the tube it joins.  The image bracket on
#                         post-section / tube-diameter is 0.68 .. 1.52 (rev 36's
#                         capped-bridge widths 8 px near / 12 px far against
#                         rev 26's threshold-swept tube 7.9-11.7 px).  Ratio 1.00
#                         sits INSIDE that bracket, so BAR_DIA is not excluded --
#                         and it is the only value that introduces nothing.
#                         THE BRACKET IS OPERATOR-MISMATCHED and is stated as
#                         such: the two widths come from different detectors.
#   POST_LEN            DERIVED.  Zero freedom: the post spans the blade's top
#                         face to the bar tube's underside, and both are already
#                         established quantities.
#
# TWO PREDICTIONS THIS STATION MAKES, NEITHER OF WHICH WAS USED TO CHOOSE IT:
#   (1) The owner said in rev 36 "both continue past the post."  IRON_Y 0.470
#       against the DERIVED BAR_HALF_Y 0.574387 is 0.8183 of the half-span, so
#       the bar continues 104.4 mm outboard past the post before it even begins
#       to turn, and 159.5 mm to the frozen tip.  HIS SENTENCE IS SATISFIED
#       RATHER THAN ASSUMED.
#   (2) It is a +- pair straddling the centreline, which is independently what
#       rev 36 found at 41:1 against the null.  That finding is SUGGESTIVE, NOT
#       ESTABLISHED (it crosses the band boundary) and is NOT promoted here --
#       this is a consistency check, not a derivation from it.
#
# WHAT IS STILL NOT MEASURED, NAMED RATHER THAN IMPLIED:
#   the posts' TRUE lateral station in metres.  SPEC 10.72 admits no px/m on the
#   bumper plane; 10.88 and 10.89 each retired a route on a precondition; 10.90.8
#   enumerated a third and abandoned it before building it.  NO METRE SCALE IS
#   INVENTED HERE.  If a square-on frame of the front ever arrives it closes this
#   and the post may move -- which is what WORKSHOP-STAGE tagging is for.
POST_Y = IRON_Y                       # EXISTING, bumper_irons.  Not a new lever.
POST_DIA = BAR_DIA                    # EXISTING.  Inside the 0.68-1.52 bracket.

# THE LANDING DATUM IS THE SAME ONE THE HOOP USES, AND THE FIRST VERSION OF THIS
# GOT IT WRONG IN EXACTLY THE WAY SPEC 10.90 WARNED ABOUT.
#
# The post stands coaxial in x with the tube, so its footprint spans the same
# outward offsets the tube's does.  The blade's top face SLOPES.  The first
# attempt took `max(_blade_top_at(lo), _blade_top_at(hi))` over the footprint,
# reasoning that the highest point cannot penetrate -- and that returned
# `BLADE_TOP_Z`, THE CROWN, which is precisely the datum 10.90 established is
# NOT the landing datum.  The built post floated 2.08 mm, against the 2.30 mm
# crown-to-station slope 10.90 measured.  10.24's family, third appearance.
#
# IT FAILED THROUGH A FALL-THROUGH, WHICH IS WORTH RECORDING SEPARATELY.
# `_POST_OUT_HI` exceeds `_PROF_MAX_OUT` by 2e-6 m -- two microns -- so
# `_blade_top_at()` missed every bracket and returned its final-point fallback,
# 35 mm low.  A function that ANSWERS ANYWAY outside its domain supplied a datum.
# SPEC 10.36's rule is that a probe which cannot answer must return None rather
# than an endpoint; the same applies to a geometry helper.  The sampling is now
# CLAMPED to the profile's own domain and asserted, so it cannot recur silently.
POST_X = BAR_X
_POST_OUT_LO = max(0.0, _BAR_OUTWARD - POST_DIA / 2.0)
_POST_OUT_HI = min(_PROF_MAX_OUT, _BAR_OUTWARD + POST_DIA / 2.0)
assert 0.0 <= _POST_OUT_LO < _POST_OUT_HI <= _PROF_MAX_OUT, (
    "the post's footprint is outside BUMP_PROFILE's top edge, so _blade_top_at "
    "would answer from its fallback rather than from the profile")
_POST_Z_BOT = _blade_top_at(_BAR_OUTWARD)     # rev 36's _LAND_Z, the AXIS station
# The overlap this leaves at the inboard rim, where the blade's crown stands
# above the axis station.  DERIVED FROM THE PROFILE, never chosen -- it is the
# bound the guard allows on the WELD side, and if BUMP_PROFILE changes it moves.
POST_WELD_MAX = max(_blade_top_at(_POST_OUT_LO),
                    _blade_top_at(_POST_OUT_HI)) - _POST_Z_BOT
_POST_Z_TOP = BAR_Z - BAR_DIA / 2.0   # the tube's underside in its STRAIGHT run
POST_LEN = _POST_Z_TOP - _POST_Z_BOT                                # DERIVED

# The post must stand where the bar is STRAIGHT, or its top datum is wrong: past
# BAR_HALF_Y the tube is bending and its underside is no longer BAR_Z - r.
assert POST_Y < BAR_HALF_Y, (
    "POST_Y %.6f is outboard of BAR_HALF_Y %.6f -- the post would meet the "
    "bend, not the straight run, and _POST_Z_TOP would be wrong"
    % (POST_Y, BAR_HALF_Y))
assert POST_LEN > 0.0, "the bar's underside is at or below the blade's top face"


def overrider_posts(name="orb_post"):
    """The two vertical posts joining the over-rider bar to the bumper blade.

    Workshop-stage.  One per side, at the bumper irons' own lateral station.
    Section equal to the tube's.  Length DERIVED from the two members it joins,
    so it cannot go stale if either moves.
    """
    obs = []
    for s in (1, -1):
        obs.append(T.cylinder((POST_X, s * POST_Y, _POST_Z_BOT + POST_LEN / 2.0),
                              (0, 0, 1), POST_DIA / 2.0, POST_LEN, seg=24,
                              name=f"{name}{'P' if s > 0 else 'M'}"))
    return obs


# =================================================================== LAMPS
def headlamp(x_off=0.0):
    """returns (bezel ring, lens, bowl) for one side; y positive

    The ring's material is chosen at the CALL SITE in build.py, not here --
    see SPEC 10.111.  This docstring said "chrome ring" for thirty-five
    revisions while build.py assigned "brass"; the contradiction is resolved
    there, and the word is neutral here so it cannot go stale again.
    """
    R = 0.0862
    ring_prof = [
        (-0.004, R + 0.0165), (0.008, R + 0.0155), (0.019, R + 0.0060),
        (0.0235, R - 0.0060), (0.0195, R - 0.0135), (0.006, R - 0.0155),
        (-0.004, R - 0.0090),
    ]
    ring = T.revolve(ring_prof, seg=72, axis='X', name="hl_ring")
    # ------------------------------------------------- rev 45, SPEC 10.111
    # THE LENS WAS DISHED THE WRONG WAY ROUND.  The retired profile ran
    # (x, r) = (0.0000, 0.0000) at the centre out to (0.0290, 0.0862) at the
    # rim -- i.e. CONCAVE, a saucer whose deepest point is on the axis.  A
    # headlamp lens is CONVEX.
    #
    # It was never visible as a shape error because of what it did instead.
    # Raycast down the near lamp's own axis, rev 45, on the built body:
    #     hit T1_body   at x = 2.1116      <- the nose's outer skin
    #     hit T1_body   at x = 2.1088      <- its inner skin, 2.8 mm behind
    #     hit hl_lens   at x = 2.1015      <- the lens, 10.1 mm INSIDE the body
    # so on the axis the camera sees RED SHEET METAL and the lens only emerges
    # near its rim.  That is the whole of the "dark red hole" -- and it is the
    # SAME defect class as SPEC 10.110's roundel: a part authored in its own
    # local frame and never once checked against the panel it is fitted to.
    #
    # Turned convex, apex forward, sitting 3.0 mm behind the bezel's own front
    # face (ring_prof's 0.0235) so the glass fills the aperture and the chrome
    # still stands proud of it.  Radius of curvature 0.263 m over the 0.0862 m
    # lens -- a gently domed lens, which is the part.
    LENS_APEX = 0.0205                       # ring_prof's front is 0.0235
    lens_prof = [
        (LENS_APEX, 0.0000), (0.0200, 0.0300), (0.0186, 0.0520),
        (0.0160, 0.0700), (0.0120, 0.0810), (0.0060, 0.0862),
        (0.0020, 0.0862), (0.0075, 0.0790), (0.0105, 0.0640),
        (0.0130, 0.0400), (0.0145, 0.0150),
    ]
    lens = T.revolve(lens_prof, seg=72, axis='X', name="hl_lens")
    bowl_prof = [
        (0.000, 0.0000), (-0.030, 0.0420), (-0.052, 0.0680),
        (-0.062, 0.0840), (-0.040, 0.0840), (-0.036, 0.0700),
        (-0.020, 0.0440), (0.000, 0.0180),
    ]
    bowl = T.revolve(bowl_prof, seg=64, axis='X', name="hl_bowl")
    return ring, lens, bowl


def bullet_indicator(name="ind"):
    """SPEC rev3.2: amber pod standing proud of the nose on a plinth"""
    base = T.revolve([(0.000, 0.0000), (0.000, 0.0395), (0.0140, 0.0378),
                      (0.0225, 0.0330), (0.0225, 0.0300), (0.0130, 0.0330),
                      (0.000, 0.0345)], seg=48, axis='X', name=name + "_base")
    # rev 10: a measurement pass read the lens as standing ~65 mm proud (the
    # build gives 41.5 mm of its plinth) and the lens was deepened to 87.5 mm
    # of x extent -- then reverted, for the same reason as BUMP_OFF above. The
    # frontal silhouette of ref_side.jpg puts the indicator's front face at
    # column 80 against the nose crown's 78, i.e. the pod is ~9 mm BEHIND the
    # forward-most point of the vehicle. Deepened to 0.0875 it reaches 58 mm
    # PROUD of the crown. So either the 65 mm is measured from a panel that is
    # itself set back from the crown -- in which case the fix is the pod's
    # MOUNTING STATION, not its depth -- or the 65 mm is wrong. Both are
    # geometry changes to the nose that deserve a derivation rather than a
    # guess. Reverted; SPEC 10.24, OPEN.
    lens = T.revolve([(0.0210, 0.0000), (0.0215, 0.0140), (0.0250, 0.0248),
                      (0.0320, 0.0316), (0.0420, 0.0348), (0.0530, 0.0330),
                      (0.0600, 0.0250), (0.0632, 0.0130), (0.0640, 0.0000)],
                     seg=48, axis='X', name=name + "_lens")
    return base, lens


def small_lamp(r=0.032, depth=0.026, name="lamp"):
    prof = [
        (0.000, 0.0000), (depth * 0.45, r * 0.55), (depth * 0.82, r * 0.88),
        (depth, r), (depth - 0.004, r + 0.004), (0.000, r + 0.006),
    ]
    return T.revolve(prof, seg=48, axis='X', name=name)


# ============================================================== VW  ROUNDEL
def roundel(R=0.1680):
    ring_prof = [
        (0.0000, R), (0.0100, R - 0.002), (0.0135, R - 0.012),
        (0.0120, R - 0.024), (0.0030, R - 0.028), (0.0000, R - 0.020),
    ]
    ring = T.revolve(ring_prof, seg=88, axis='X', name="vw_ring")
    disc_prof = [
        (0.0000, 0.0000), (0.0055, R - 0.030), (0.0035, R - 0.024),
        (-0.0060, R - 0.024), (-0.0060, 0.0000),
    ]
    disc = T.revolve(disc_prof, seg=88, axis='X', name="vw_disc")
    return ring, disc


# ================================================================== GUTTER
# rev 50, A14 -- A SECOND `def gutter()` WAS DEFINED HERE AND IT WAS DEAD CODE.
# Python binds the LAST definition, so `build.py:403 A(D.gutter(), "paint")` has
# always called the rev-16 version at the bottom of this file, and this one has
# never run.  It is DELETED rather than left in place because it was not an inert
# stub: it still carried `z = zt - rt * 0.72`, the pre-rev-16 drip-rail form that
# the live version's own comment says "would drag the drip rail 28 mm up the new
# roll", and it swept only the cab (x 0.442..1.806) against the live run from
# T._aft(-1.880) -- about 2.1 m short.  Anyone reading this file top-down read the
# RETIRED formula as the live one, and anyone deleting the LATER copy to remove
# the duplicate would have silently reverted rev 16 and taken the bulb string
# with it (t1_detail.bulb_string hangs off the same roll start).
# This is rule 15's failure shape: a retraction that landed in a ledger and not
# in the source.  The live gutter() is unchanged and is the only one.


# ============================================================ SIDE MOULDING
def moulding(z=1.372):
    prof = [(0.0000, 0.0000), (0.0075, 0.0035), (0.0090, 0.0000),
            (0.0075, -0.0035)]
    obs = []
    for s in (1, -1):
        path = []
        for i in range(37):
            x = 0.905 + (1.800 - 0.905) * i / 36
            y = T.WX(x) * T.G(z)
            path.append((x, s * (y + 0.001), z))
        pr = [(a * -s, b) for (a, b) in prof]
        obs.append(T.sweep(path, pr, up=(0, 0, 1), name=f"mould{s}"))
    return obs


# ======================================================= CANTILEVERED COUNTER
# MEASURED off ref_side.jpg and ref_rear34.jpg.  FRAME: UN-DROPPED -- these
# build in build.py step 6, before step 8b subtracts the rake shear from every
# vertex.
#
# !! THE "Subtract 0.065 for above-ground" LINE THAT USED TO BE HERE IS WRONG,
# !! AND IT IS THE WHOLE OF THE ~40 mm CNT_ZB RESIDUAL IN HANDOFF_rev11 ITEM 4.
# Since rev 8 the drop is a LINE, not a scalar: t1_core.rake_drop(x) =
# 0.0365 + 0.0330 x, and RIDE_DROP survives only as its value at
# X_DROP_REF = +0.8636.  It is NOT a frame conversion (t1_core says so in as
# many words).  The counter runs +0.918 to -2.423, i.e. almost entirely AFT of
# that station, where rake_drop is far smaller -- 0.0117 at its mean station
# and -0.0435 at its tail.  So converting the AG measurement with the retired
# scalar put CNT_ZT 1.189 + 0.065 = 1.254, and the built slab then reads 1.240
# AG at its mean station against REF sec.6's 1.189 / 1.205.  The 40 mm is the
# frame conversion, not the geometry.
#
# The residual is RESOLVED, and it resolves to LEAVE THE NUMBER ALONE.
# Re-placed by the only method SPEC 10.11 permits -- a ratio inside a panel
# whose two ends are both locked, never the ground line -- with the window-band
# sill (y_ref 392.0 <-> z 1.3720) and the cab-door two-tone break (y_ref 413.1
# <-> Z_BELT 1.2720) as the ruler, 21.1 px = 0.100 m:
#     brass band, half-max saturation, 113 columns   y_ref 414.61 +- 0.59
#     -> z = 1.2720 - (414.61 - 413.1) * 0.004739    = 1.2649 un-dropped
# and REF sec.6's own 416.8 is the band's CENTRE, not its top edge (my band is
# 414.61-419.12, centre 416.87), which is why 1.254 came out of it.  Against
# the shipped 1.2540 that is +11 mm, inside the +-16 mm the outboard-parallax
# term alone carries.  The two answers differ by 68 mm = 0.0330 * (0.8636 -
# (-1.2000)), the rake between X_DROP_REF and the rear-axle station the AG
# frame quotes at -- which is SPEC 10.11's ~70 mm common-mode ground-line error
# re-entering through an AG comparison.  Do not "fix" it in the AG frame.
#
#                     measured AG   un-dropped   shipped   error
#   X0 front            +0.918        +0.918      +0.920   ok
#   X1 rear             -2.323        -2.323      -1.340   983 mm SHORT
#   Z top                1.189         1.254       1.362   108 mm high
#   Z bottom             1.082         1.147       1.277   130 mm high
#   thickness            0.107         0.107       0.085   22 mm thin
#   Y outboard            --           1.166       1.245   79 mm proud
#   Y inboard             --           0.845       0.845   ok
#
# RE-MEASURED by the locked-ends ratio above, for the record and NOT applied:
#   counter top    (brass band top    y_ref 414.61)  1.2649 flank-plane
#   counter bottom (cream/red break   y_ref 439.45)  1.1472 flank-plane
#   edge depth                        24.84 px       0.1176 +- 0.0031
# both flank-plane readings, i.e. before the outboard-parallax term.  The
# counter's outer face is ~0.295 m nearer the camera than the ruler, and REF
# sec.6 puts that at +16 mm at the nosing and +21 mm at the break; my own
# independent handle on it -- the counter top's foreshortened depth, 3.5 +- 0.7
# px, which IS the parallax expressed in pixels -- gives +15 to +31 mm
# depending on how (camera height, distance) split, so the term is real but
# only known to about +-10 mm.  1.254 / 1.147 / 0.107 are all inside that band
# and all three are SPEC 10.5 locks, so they STAY.  Three findings were applied
# from a measurement, broke something independently locked and were reverted in
# rev 10 (SPEC 10.24); this is the same shape of finding and the rule earned
# there is to measure it a third way before moving a lock.  What the third way
# would be: the counter top's inner edge, which sits ON the flank plane and
# needs no parallax at all -- unusable in ref_side.jpg because the body cream
# just above the counter ramps smoothly from saturation 0.10 to 0.35 with no
# step to find, but it IS a clean step in ref_rear34.jpg (y 423 at x 700) and
# that image only needs a local vertical scale to close.
#
# Y inboard 0.845 penetrates the flank by ~26 mm at counter height (measured
# body surface 0.8709 at x = -1.34, z = 1.200).  That is correct for a
# cantilever -- the slab is carried by the body, not butted against it.
# !! CNT_X1 INTERACTS WITH verify.py ROW 1 -- READ BEFORE "FIXING" A LENGTH FAIL
# verify._bounds() measures overall length across EVERY mesh object and skips
# only "cyc".  Before this counter existed the rear-most object was the tail
# lamp at x = -2.131, giving L = 4.291 against SPEC's 4.290 -- a 1 mm margin.
# The measured counter tail wrap reaches x = -2.323 (nosing -2.330), so
# verify reports  "length 4.490 vs spec 4.290 (+200 mm)".  That is NOT a
# geometry regression: it is the guard measuring a conversion FITTING as part
# of the vehicle.  SPEC sec.4 explicitly lists a "radiused counter tail
# OVERHANGING the body", and ref_side.jpg measures the overhang at ~0.33 m.
# The fix is one line in verify.py (see visibility_fails() at the bottom of
# this file for the exact text).  Do not shorten the counter to silence it.
CNT_X0 = 0.9180
# rev 16: the counter's tail wrap is a MEASURED OVERHANG past the body, not
# an absolute station -- ref_side.jpg puts the cream fascia's aft edge ~65 px
# behind the rearmost sheet metal, 0.29 m at the tail's own longitudinal
# scale, and the built overhang was X_TAIL_OLD - (-2.4230) = 0.3150 m.  The
# tail re-space moves X_TAIL 235 mm forward, so the counter moves with it and
# the overhang is preserved by construction rather than by luck.
CNT_OVERHANG = 0.3150
CNT_X1 = T.X_TAIL - CNT_OVERHANG
CNT_ZT, CNT_ZB = 1.2540, 1.1470             # 107 mm thick
CNT_Y_IN, CNT_Y_OUT = 0.8450, 1.1660        # 321 mm plan depth
# INFERRED, not measured.  ref_rear34.jpg shows the cream slab and its gold
# nosing running continuously round the rear corner and across the tail, and
# shows that the corner is radiused rather than mitred -- but the radius
# itself and the front chamfer are not measurable from the photographs.
CNT_R = 0.1500                              # tail corner radius, in plan
CNT_CH = 0.0500                             # 45 deg front outer corner chamfer
# MEASURED, ref_side.jpg.  The brass nosing caps this FRACTION of the slab's
# outer edge.  113 columns over x_img 340-920, saturation half-max on both
# edges of the gold band: band 4.52 +- 0.23 px (stat) +- 0.5 px (4:2:0 chroma
# subsampling is the floor here), whole counter edge -- brass top to the
# cream/red break -- 24.84 px, ratio 0.182.  ref_rear34.jpg over x 520-700,
# the only run clear of the napkin dispensers, gives 0.191.
# It is stored as a FRACTION and not as a depth on purpose: it was measured
# AGAINST the slab edge, so a depth would silently stop meaning what it was
# measured to mean the moment CNT_ZT/CNT_ZB move (SPEC 10.25).
CNT_NOSE_F = 0.1860
CNT_XA = CNT_X1 + CNT_R                     # -2.173  tail arc tangent point
CNT_YA = CNT_Y_OUT - CNT_R                  #  1.016  tail arc tangent point
CNT_X_IN = CNT_X1 + (CNT_Y_OUT - CNT_Y_IN)  # -2.002  tail leg inner face
# rev 16: aft brackets re-spaced with the shell they hang off.
CNT_BRACKETS = tuple(T._aft(_b) for _b in
                     (0.780, 0.120, -0.560, -1.080, -1.800))


def _counter_outer(side=1, seg=8):
    """outer plan edge: front -> aft -> round the corner -> across the tail"""
    p = [(CNT_X0, CNT_Y_OUT - CNT_CH), (CNT_X0 - CNT_CH, CNT_Y_OUT),
         (CNT_XA, CNT_Y_OUT)]
    for i in range(1, seg + 1):                    # show-side corner 90->180
        a = math.radians(90 + 90 * i / seg)
        p.append((CNT_XA + CNT_R * math.cos(a), CNT_YA + CNT_R * math.sin(a)))
    p.append((CNT_X1, -CNT_YA))
    for i in range(1, seg + 1):                    # off-side corner 180->270
        a = math.radians(180 + 90 * i / seg)
        p.append((CNT_XA + CNT_R * math.cos(a), -CNT_YA + CNT_R * math.sin(a)))
    return [(x, side * y) for (x, y) in p]


def _counter_inner(side=1):
    """inner plan edge, offset from the outer by the constant 321 mm depth.
    At a corner whose radius (150 mm) is smaller than the offset the inner
    edge degenerates to a sharp corner, which is what a real offset does."""
    return [(x, side * y) for (x, y) in
            [(CNT_X0, CNT_Y_IN), (CNT_X_IN, CNT_Y_IN),
             (CNT_X_IN, -CNT_Y_IN), (CNT_XA, -CNT_Y_IN)]]


def plank_counter(side=1):
    """cream-PAINTED slab counter cantilevered under the three serving bays
    and wrapped round the rear corner and across the tail
    (SPEC r4 8.5: measured saturation 0.07 - painted, not bare timber;
     SPEC sec.4: brass edge strip on the counter lip)"""
    obs = []
    plan = _counter_outer(side) + list(reversed(_counter_inner(side)))
    ob = T.solid_prism((0.0, 0.0, (CNT_ZT + CNT_ZB) / 2),
                       (1, 0, 0), (0, 1, 0), (0, 0, 1),
                       plan, CNT_ZT - CNT_ZB, name="counter")
    obs.append(ob)
    FLAT.append(ob)

    # NB the brass nosing is NOT returned here.  build.py:116 calls this
    # through A(..., "countercream"), and A() puts everything it is handed in
    # ASSIGN, whose material loop would then paint the brass strip cream.
    # It is built in counter_nosing() and routed with a null key instead.

    # ---- brackets.  The 5th, at x = -1.80, carries the new tail overhang.
    for bx in CNT_BRACKETS:
        b = T.solid_prism((bx, side * 1.0000, CNT_ZB - 0.0200),
                          (1, 0, 0), (0, 1, 0), (0, 0, 1),
                          T.rrect(0.048, 0.300, 0.008, seg=2),
                          0.040, name=f"bracket{bx}")
        FLAT.append(b)
        obs.append(b)
    return obs


# ================================================================== GALLEY
def galley():
    """cooking fit-out visible through the serving bays"""
    obs = []
    pts = T.rrect(0.470, 2.500, 0.02, seg=3)
    obs.append(T.solid_prism((-0.300, 0.560, 1.1600), (0, 1, 0), (1, 0, 0),
                             (0, 0, 1), pts, 0.470, name="galley_top"))
    pts = T.rrect(0.560, 0.780, 0.02, seg=3)
    obs.append(T.solid_prism((0.520, -0.180, 1.1900), (0, 1, 0), (1, 0, 0),
                             (0, 0, 1), pts, 0.530, name="plancha"))
    # rev 38: 1.400 -> FLOOR_W.  At 1.400 the half-width is 0.700 and the REAR
    # tyre's inner face is at y 0.604, so this slab passed THROUGH both rear
    # wheels -- 152 overlapping face pairs per tyre, 110 per rim barrel, BVH
    # overlap on the evaluated world-space meshes (probe_rev38_floorpen.py).
    # Found as the CONTROL for the cab-floor test, and the control FAILING is
    # what showed the defect is systemic rather than a cab quirk.  1.400 was
    # AUTHORED -- it appears nowhere in SPEC.md or REF_MEASUREMENTS.md.
    # rev 59.  NOTCHED round the rear wheel houses -- see _notched_rrect for
    # the measurement that forced it and for why FLOOR_W itself does not move.
    # T1_WHFLAT=1 restores the un-notched slab so the census stays testable.
    if os.environ.get("T1_WHFLAT") == "1":
        pts = T.rrect(FLOOR_W, 2.700, 0.02, seg=3)
    else:
        pts = _notched_rrect(FLOOR_W, 2.700, 0.02,
                             floor_notches(-0.500, (T.X_AXLE_R,)),
                             WH_Y_IN - 0.002, seg=3)
    obs.append(T.solid_prism((-0.500, 0.000, 0.5400), (0, 1, 0), (1, 0, 0),
                             (0, 0, 1), pts, 0.040, name="van_floor"))
    # rev 11 carried two 0.900 x 0.240 steel slabs at x -1.500 and -1.780,
    # z 1.405-1.435.  REMOVED.  They sit AFT of gal_end_a, the galley's own aft
    # wall at x = -1.300, so no serving aperture can see them: bay 3, the
    # rear-most, ends at x = -0.960 and verify's SOLID_PROBE_X asserts sheet
    # metal at x -1.05 / -1.30 / -1.55 / -1.80, which is the flank they sat
    # behind.
    #
    # CORRECTION to the premise, recorded so nobody re-derives it: they were
    # NOT visible from nowhere.  t1_shell puts the rear glazing at REAR_Z 1.450
    # +- REAR_H/2, i.e. z 1.280-1.620, and the ray from the hero34r camera
    # position in _cam_locs() to (-1.500, -0.300, 1.435) crosses the tail plane
    # at y = 0.32, z = 1.58 -- inside that opening, with nothing between.  So
    # the reason to delete them is not that no ray reaches them; it is that
    # they are 0.9 m unsupported slabs floating in a dead cavity, no
    # photograph shows a shelf at that station, and what the same ray now lands
    # on is gal_end_a's white wall, which is a better read than two floating
    # steel plates.
    return obs


# ================================================================ INTERIOR
# rev 38, SPEC 10.96.  The interior floor pans are NARROWED so they clear the
# wheels, and wheel houses are added so the arch apertures are closed.
#
# WHAT HIS REPORT 6 ACTUALLY WAS.  Off `rev37_hero34f.png` he asked "there
# seems to be a bar obstructing the front wheel?".  The rev-38 brief proposed
# `doorback1`.  ABLATED (T1_ABLATE, built for this) and the member did not
# move -- 612 px of 1.7 M changed, none of them the bar.  Ray-cast from the
# hero34f camera then named it BY CONSTRUCTION: `cab_floor`, 308 rays through
# the front arch, first hit, nothing in front of it.  Not a door part.
#
# WHY IT WAS VISIBLE AT ALL: there is no wheel house anywhere in this build
# (grep: no liner, inner_wing, wheelwell, splash).  Each arch is a cylinder cut
# clean through the skin with nothing behind it, so the cab interior is in
# plain sight from outside.
#
# THE NUMBERS.  cab_floor was 1.560 (half-width 0.780) against a front tyre
# whose OUTER face is at 0.760 -- 20 mm proud of the wheel.  van_floor was
# 1.400 (half-width 0.700) against a rear tyre inner face at 0.604.  BOTH were
# AUTHORED; neither appears in SPEC.md or REF_MEASUREMENTS.md, so nothing
# measured is being overturned.  FLOOR_W = 1.200 gives half-width 0.600, which
# clears the front tyre's inner face (0.609) by 9 mm and the rear's (0.604) by
# 4 mm.  A narrow footwell between two wheel-house humps is also what a real T1
# has; the 1.560 slab was not merely invisible-and-wrong, it was impossible.
#
# THIS IS NOT A MEASUREMENT OF THE VEHICLE and is not tagged as one.  It
# replaces an authored number that is geometrically impossible with an authored
# number that is possible.  Its ceiling: no photograph shows this vehicle's
# cab floor, and none is claimed.
FLOOR_W = 1.200                     # AUTHORED, rev 38; see SPEC 10.96
WH_R = 0.3735                       # FRONT ARCH ONLY: = t1_shell.ARCH_R, and
                                    # the front cutter really is a circle of
                                    # that radius -- grep
                                    # `T.cylinder((T.X_AXLE_F`.  THE REAR
                                    # APERTURE IS NOT A CIRCLE and has not been
                                    # since rev 16 (grep `ARCH_W_REAR` and
                                    # `rear_arch_outline`); the rear liner is
                                    # driven off that outline, see
                                    # wheel_houses().
WH_T = 0.010                        # house shell thickness
WH_Y_IN = 0.500                     # inboard face; wheel spans y 0.604..0.760
WH_INSET = 0.0026                   # outboard face this far inside flank_y (skin 2.8 mm)
WH_SWEEP = 2.0                      # degrees past horizontal each side


def wh_x_halfspan(xa):
    """Half the x extent the wheel-house tub occupies at axle xa.

    Taken from the APERTURE ITSELF -- the rear's `rear_arch_outline`, the
    front's circle of ARCH_R -- so ARCH_W_REAR's +-0.03 m moves the floor
    notch with it and no second width constant exists to go stale.  The 10 mm
    is clearance, not a measurement.
    """
    import t1_shell as S
    if abs(xa - T.X_AXLE_R) < 1e-9:
        return max(abs(dx) for dx, _ in S.rear_arch_outline(xa)[:-2]) + 0.010
    return S.ARCH_R + 0.010


def floor_notches(x_origin, axles):
    """(v0, v1) bands, in a floor prism's own v axis, for the given axles."""
    out = []
    for xa in axles:
        h = wh_x_halfspan(xa)
        out.append((xa - h - x_origin, xa + h - x_origin))
    return out


def _notched_rrect(w, h, r, notches, hu, seg=3):
    """`T.rrect` with rectangular NOTCHES cut into BOTH long edges.

    rev 59, F: THE FLOOR PANS PASS 100 mm THROUGH THE WHEEL-HOUSE WALL, AND
    THAT IS WHY THE BAR IS STILL THERE AFTER THE LINER WAS FIXED.

    MEASURED, not argued.  With the rear liner corrected to the aperture, the
    census through the side ortho still reads 177 van_floor rays -- 176 before
    the fix.  The reason is geometric and it applies to a liner of ANY radius:
    an ORTHOGRAPHIC side ray keeps its radius about the axle all the way in,
    so it NEVER crosses the tub's cylindrical band.  The only surface that can
    stop it is the tub's INBOARD wall, which stands at WH_Y_IN = 0.500 -- and
    both floor pans reach FLOOR_W / 2 = 0.600, i.e. 100 mm OUTBOARD of it.
    The ray therefore lands on the floor's 40 mm side face before the wall.

    THE FRONT AXLE PROVES IT IS NOT THE LINER'S RADIUS.  The front liner has
    always filled its circular aperture exactly (the reach row reads
    -0.0 .. +0.0 mm) and the same census reads 151 `cab_floor` rays.

    rev 38 sized FLOOR_W against the TYRES -- "clears the front tyre's inner
    face (0.609) by 9 mm and the rear's (0.604) by 4 mm" -- and the wheel
    houses, added in the SAME revision, were never in that sum.  FLOOR_W is
    NOT changed here: a real T1's floor is notched round its wheel houses and
    that is what this does, over the wheel house's own x span only, taken from
    the aperture outline rather than from a second constant.

    `notches` is a list of (v0, v1) bands in the outline's own v axis; `hu` is
    the half-width the floor drops to inside them.  Winding matches
    `T.rrect` -- CCW, first point on the +u edge -- because the notches are
    inserted INTO the two straight edges in the direction each is already
    travelling.
    """
    r = min(r, w / 2 - 1e-4, h / 2 - 1e-4)
    a, b = w / 2 - r, h / 2 - r
    bands = []
    for v0, v1 in notches:
        v0, v1 = max(min(v0, v1), -b), min(max(v0, v1), b)
        if v1 - v0 > 1e-6:
            bands.append((v0, v1))
    bands.sort()
    arcs = []
    for cx, cy, a0 in ((a, b, 0.0), (-a, b, math.pi / 2),
                       (-a, -b, math.pi), (a, -b, 1.5 * math.pi)):
        arcs.append([(cx + r * math.cos(a0 + (math.pi / 2) * i / seg),
                      cy + r * math.sin(a0 + (math.pi / 2) * i / seg))
                     for i in range(seg + 1)])
    pts = list(arcs[0]) + list(arcs[1])
    for v0, v1 in reversed(bands):                 # -u edge runs v HIGH -> LOW
        pts += [(-w / 2, v1), (-hu, v1), (-hu, v0), (-w / 2, v0)]
    pts += list(arcs[2]) + list(arcs[3])
    for v0, v1 in bands:                           # +u edge runs v LOW -> HIGH
        pts += [(w / 2, v0), (hu, v0), (hu, v1), (w / 2, v1)]
    # A band clamped exactly onto b lands its first (or last) point on top of a
    # corner arc's end point.  A zero-length edge is not a self-intersection but
    # every segment test says it is, and `solid_prism` caps the outline -- so it
    # is removed rather than tolerated.  WATCHED: without this the cab pan's
    # outline reported 2 self-intersections and the van pan's 0.
    out = []
    for q in pts:
        if not out or abs(q[0] - out[-1][0]) > 1e-9 or abs(q[1] - out[-1][1]) > 1e-9:
            out.append(q)
    while len(out) > 3 and abs(out[0][0] - out[-1][0]) < 1e-9 \
            and abs(out[0][1] - out[-1][1]) < 1e-9:
        out.pop()
    return out


def _arc_liner(xa, zc, sgn, a0, a1, seg, name, outline=None):
    """A wheel-house shell: an arc tube about the axle whose OUTBOARD face
    follows the flank skin instead of sitting at a fixed y.

    rev 59 -- AND WHOSE RADIUS NOW FOLLOWS THE APERTURE INSTEAD OF A CONSTANT.
    Pass `outline` a list of (dx, dz) stations about (xa, zc) -- the aperture's
    OWN outline, dropped of its two floor points -- and the sweep runs through
    those stations at their own radii instead of round a circle of WH_R.  Pass
    None and the behaviour is the circle, bit for bit, which is what the FRONT
    arch wants and what T1_WHCIRC=1 restores for the rear.

    TWO THINGS THIS FIXES, BOTH CAUGHT BY LOOKING RATHER THAN BY A GUARD:
      1. A FULL 360 revolve is wrong.  The bodywork exists only above the
         arch's horizontal diameter; below it the arch is open to the road.
         rev 38's first attempt revolved the full circle and every guard
         passed -- 0 fail, 0 warn, 0 non-manifold, 0 interior rays -- while
         the render showed a dark skirt hanging in mid-air below the sill.
      2. A FIXED outboard y is wrong.  Measured on the arch rim,
         `T.flank_y` runs 0.873 at the crown down to 0.801 (front) and 0.787
         (rear) near horizontal, so one number stands proud of the skin by up
         to 90 mm at the sector ends -- which is what the second render showed.
    IT WAS THE HERO THAT CAUGHT BOTH, NOT THE GUARDS.  That is rev 37's rule
    earning its keep twice inside one revision.
    """
    R_IN = 0.030
    verts, faces = [], []
    n = 6
    if outline is not None:
        seg = len(outline) - 1
    for k in range(seg + 1):
        if outline is None:
            a = a0 + (a1 - a0) * k / seg
            ca, sa = math.cos(a), math.sin(a)
            R = WH_R
        else:
            # The aperture's own station, at its own radius and its own
            # direction.  a0/a1/WH_SWEEP are NOT applied here: t = +-1 is the
            # outline's foot by construction, and sweeping past it would put
            # the flat end caps back below the rocker -- the mid-air skirt
            # rev 38 removed.
            dx, dz = outline[k]
            R = math.hypot(dx, dz)
            ca, sa = dx / R, dz / R
        x = xa + R * ca
        z = zc + R * sa
        # rev 59 RISK 1.  This was `try: ... except: y_out = 0.870 - WH_INSET`.
        # A silent substitution here is the rev-38 defect exactly: 0.870 stands
        # PROUD of the skin wherever the flank is narrower than that, and
        # widening the sector drives the end stations to x -1.5600 / -0.6400
        # where flank_y reads 0.8176.  It now RAISES.  (T.flank_y is
        # WX(x) * G(z), two np.interp calls that clamp rather than throw, so
        # the branch was dead already -- a completed build is the evidence it
        # never fires, and both SUB levels complete.)
        try:
            y_out = T.flank_y(x, z) - WH_INSET
        except Exception as e:
            raise RuntimeError(
                "%s: flank_y(%.4f, %.4f) failed and there is no safe "
                "substitute -- a fixed outboard y stands proud of the skin "
                "(rev 38): %s" % (name, x, z, e))
        if y_out <= WH_Y_IN + WH_T:
            raise RuntimeError(
                "%s: outboard face y %.4f is not outboard of the inboard face "
                "%.4f at (x %.4f, z %.4f) -- the profile would be inverted"
                % (name, y_out, WH_Y_IN + WH_T, x, z))
        prof = [(WH_Y_IN,        R),
                (y_out,          R),
                (y_out,          R - WH_T),
                (WH_Y_IN + WH_T, R - WH_T),
                (WH_Y_IN + WH_T, R_IN),
                (WH_Y_IN,        R_IN)]
        if sgn < 0:
            prof = list(reversed([(-t, r) for (t, r) in prof]))
        for (t, r) in prof:
            verts.append((r * ca, t, r * sa))
    for k in range(seg):
        for i in range(n):
            j = (i + 1) % n
            faces.append((k * n + i, k * n + j, (k + 1) * n + j, (k + 1) * n + i))
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(seg * n + i for i in range(n)))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.validate()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    T.fix_normals(ob)
    return ob


# ===========================================================================
# rev 60 -- THE UNDERBODY.  F67, the owner's item D, never attempted.
#
# THE DEFECT, MEASURED IN THE FRAME AND NOT ARGUED.  A vertical luminance
# profile down `out/r59a_hero.png` at cols 930-990 -- between the wheels,
# clear of both -- runs: red flank 152 DN, darkening to 131 at the body's
# lower edge (v 828), and then the very next rows are GROUND, rising 155 ->
# 224 by v 880.  THERE IS NO DARK BAND AT ALL.  The same profile on
# `ref_side.jpg` at cols 350-500 runs: body 63, then a FORTY-ROW BAND AT
# 8.5 DN (v 609-648), then the ground emerging at 650 and reaching its open
# plateau of ~140 by v 700.
#
#     under-sill ground / open ground   render 0.68   photograph 0.14
#     the dark band's floor / open      render  none  photograph 0.061
#
# WHY IT WAS BRIGHT: `t1_mats.body_paint` drives the two-tone off object-space
# Z, and the shell's bottom face at `t1_core.ZB` ~ 0.386 sits BELOW the belt
# line, so the underside was being painted BODY RED and lit like a flank.
# Sampled in the hero it reads (159, 117, 112) -- 0.509 of open ground where
# the photograph's cavity is 0.061.  The pan below hides that face rather than
# re-plumbing the paint graph, because a normal-based selector in the paint
# would also have to be right about every OTHER downward face on the vehicle.
#
# THE DEPTH IS AN ASSUMPTION AND IT IS STATED AS ONE (rule 12), AND THE SCALE
# IT RESTS ON WAS PUBLISHED WRONG TWICE BEFORE IT WAS RIGHT.
#
# RETRACTED, rev 60b: this comment first said "258.6 px/m from the REAR tyre's
# horizontal extent at its own hub row (172 px)", then "251-284, threshold
# dependent".  BOTH ARE DEAD.  An independent audit painted that window and the
# dark run is not the tyre: at the hub row the tyre reads 11-13 DN and the
# wheel-arch shadow above it reads 15-22 DN, so the two are CONTIGUOUS and a
# luminance threshold cannot separate them.  The "tyre span" ran from inside
# the arch shadow out onto the kerb.  Painted and looked at -- rule 8, on the
# instrument that set the scale for the whole revision.
#
# THE SCALE, RE-DERIVED AND PAINTED.  Both cream rim rings are fitted as
# circles instead:
#     rear rim   centre (749.5, 604.6)  r 39.79 px   n=828   rms 1.11 px
#     front rim  centre fixed to that radius (241.8, 609.8)  rms 2.25 px, n=107
#     hub-to-hub 507.8 px / 2.400 m LOCKED  ->  211.6 px/m
# The rear rim fits a CIRCLE to 1.11 px, i.e. it images round, so there is no
# yaw foreshortening at that wheel and this scale applies to VERTICAL extents
# too -- which matters, because the band below is vertical.  (A wheelbase and a
# tyre are foreshortened by the SAME cosine, so the two routes must agree; when
# they disagreed by 23 % one of them was simply mis-measured, and it was mine.)
#
# THE CEILING, RECOMPUTED.  The photograph's dark band is threshold-dependent
# too -- 33 px at 15 DN to 66 px at 60 DN -- which the first cut corrected for
# the tyre and NOT for the band it divides, in the same paragraph:
#     33..66 px / 211.6 px/m  =  0.156 .. 0.312 m
# THAT BAND CONTAINS BOTH THE UNDERBODY AND THE SHADOWED GROUND UNDER IT, and
# no feature in the profile separates them, so this is a CEILING and NOT a
# value.  The pan's visible drop below the shell is 0.090-0.100 m, under even
# the lowest of those.  What the frames cannot give is the underbody's true
# depth: that is a NEW-FRAME item (a low raking shot under the sill).
#
# NOT BUILT, deliberately: exhaust, fuel tank, spare, engine.  `ref_side.jpg`'s
# cavity is a featureless 8.5 DN with a std of 1.9 -- it resolves NOTHING
# inside itself, so anything modelled in there would be invention.
# `ref_nolita_flank.jpg` does show ONE member and that is the single rail pair
# below.
# ===========================================================================
UNDER_W    = 1.560                  # ASSUMPTION: inboard of the sills (1.750)
# rev 60b -- THE PAN IS DEFINED BY ITS FLOOR, NOT BY ITS TOP.
#
# The floor is the only edge anyone can see; the top is buried inside the
# shell.  Defining the top and subtracting a depth (the first cut) left a
# HAIRLINE SLOT at the aft end, because `t1_core.ZB` is not flat.
#
# rev 60c -- AND `ZB` IS NOT THE SHELL'S UNDERSIDE EITHER, WHICH IS WHY THE
# SLOT SURVIVED THAT FIX.  rev 60b set UNDER_TOP 0.410 "above max(ZB) = 0.397"
# and declared the top could not leave a gap.  Ray-cast up at the shell from
# below and the shell's own bottom face, in the AUTHORED frame, is a curve
# that RISES AT BOTH ENDS, well above ZB at the tail:
#
#     x      -1.760  -1.800  -1.820  -1.830  -1.840  -1.850     +1.780  +1.850  +1.900
#     shell   0.4055  0.4098  0.4170  0.4224  0.4299  0.4391     0.4084  0.4122  0.4165
#
# so a flat top at 0.410 was BELOW the shell over the last 60 mm of the tail
# and at the very front, and the measured gaps were -29.1 mm at x -1.85 and
# -2.3 mm at x +1.85 on the centreline.  Each end now has its OWN outer top,
# set from the table above plus a stated margin, and the flat is raised.
#
# rev 60b's stated cause for the first slot was ALSO wrong and is retracted
# here: it blamed the rake shear.  Step 8b subtracts RAKE_Z0 + RAKE_DZDX*x
# from pan and shell alike, so a shear that is a pure function of x cannot
# open a gap between two things at the SAME x.  The cause was only ever the
# shell's underside varying with x -- which is what the table measures.
UNDER_FLOOR = 0.2960                # the visible underside.  ZB - 0.090 amidships
UNDER_TOP  = 0.4200                 # buried.  Clears the shell by >= 11.6 mm
#                                   # at BOTH pan ends (see the table above)
UNDER_DROP = UNDER_TOP - UNDER_FLOOR
# UNDER_DROP IS NOT THE VISIBLE DROP and has not been since rev 60b, which
# changed its meaning without saying so: it is the pan prism's DEPTH, most of
# it buried.  What a photograph could compare against is the floor's drop
# below the shell, which is this:
UNDER_VIS  = 0.0900                 # ZB - UNDER_FLOOR amidships.  The STATED
#                                   # ASSUMPTION under a measured 0.137-0.155 m
#                                   # ceiling -- the photograph's band contains
#                                   # both the metal and the shadowed ground.
# rev 60c -- T1_UNDER_VIS OVERRIDES IT, FOR MEASUREMENT ONLY.  It exists to
# SEPARATE the two named contributors to G4's residue (rule 29.3): the white
# cyclorama filling a shallow cavity (F62's ceiling) and this assumed drop.
# It is not a tuning knob -- the shipped value stays 0.090, because the
# 0.137-0.155 band is a CEILING that contains both the metal and the ground
# shadow, and setting the constant to a ceiling would assume the band is all
# metal.  What the override buys is an attribution, not a fix.
UNDER_VIS = float(os.environ.get("T1_UNDER_VIS", UNDER_VIS))
UNDER_FLOOR = UNDER_FLOOR - (UNDER_VIS - 0.0900)
UNDER_DROP = UNDER_TOP - UNDER_FLOOR   # recomputed: the floor may have moved
UNDER_X0, UNDER_X1 = 1.780, -1.700  # clear of BOTH wheel-house notches:
#   front notch 0.9165..1.6835 (X_AXLE_F +- ARCH_R + 10 mm)
#   rear  notch -1.570..-0.630 (X_AXLE_R +- ARCH_W_REAR/2 + 10 mm)
# so both ends of the pan are at FULL width and the end ramps below can close
# them.  The first cut of this stopped at -1.800 while the body runs on to
# -2.108, and the pan's square aft cap then hung in open air behind the rear
# wheel -- plainly visible in the hero, found by CROPPING THE RENDER, not by
# any check.
#
# AND THE AFT END IS BOUNDED BY THE LENGTH ROW, NOT BY THE SHEET METAL.  The
# first cut ran the pan to -1.980 with its ramp reaching -2.100 and
# `verify.py` went red: "length 4.260 vs spec 4.055 (+205 mm)".  The body's
# skin does run to -2.108, but everything aft of -1.905 is on a SWUNG part
# (lid_trunk, glass_rear, englid_handle, plate_1963), which `_bounds()`
# excludes -- so the vehicle's FIXED aft limit is -1.905 and the pan may not
# reach it.  The guard caught this in the same edit; the number above is set
# from the guard's own limit rather than from the skin.
RAIL_DROP  = 0.0350                 # the rail's VISIBLE drop below the floor
RAIL_EMBED = 0.0100                 # rev 60c: and this much buried INSIDE the
# pan.  rev 60b's "origins are centres" fix was applied to the pan and the rail
# independently and made their shared face EXACTLY coincident -- pan floor and
# rail top both landed on 0.29599999999999999, bit-identical, two opaque faces
# back to back over the rails' whole 3.14 m footprint on one material.  Before
# that fix the rail was 27.5 mm inside the pan and there was no coincidence.
# A flush condition is not a construction: the rail now OVERLAPS the pan.
RAIL_TAPER = 0.120                  # rev 60c: each rail end ramps up into the
# pan floor over this much x.  rev 60b freed the rails from being 78 % buried
# and so exposed, for the first time, that they stop 200 mm short of the pan at
# each end with a SQUARE 35 mm face -- a step in the underbody silhouette
# directly behind the rear wheel, which is the same "ends in mid-air" defect
# UNDER_RAMP was introduced to remove for the pan itself.  Found by an
# independent adversary reading the extents, not by any check.
RAIL_Y     = 0.300
RAIL_W     = 0.090
RAIL_INSET = 0.100                  # rail ends, inboard of the pan's own ends
# THE END CLOSERS.  Each end gets its OWN length and its OWN outer top: the
# body is symmetric in neither.
UNDER_RAMP_F = 0.120                # front: to x +1.900
UNDER_RAMP_A = 0.100                # aft:   to x -1.800, and NOT further --
# rev 60c: the aft ramp ran to -1.880 at a FLAT 0.780 half-width while the
# tail tapers away under it.  Measured on the mesh, body max|y| against that
# 0.780:
#     x      -1.800  -1.820  -1.840  -1.850  -1.860  -1.870
#     max|y|  0.8358  0.8175  0.7894  0.7729  0.7565  0.7322
#     proud   -55.8   -37.5    -9.4    +7.1   +23.5   +47.8   mm
# so the closer stood up to 48 mm PROUD of the skin over the last 30 mm of the
# tail, and its final 7 mm hung past the rearmost bodywork (x -1.8730) in open
# air -- a black wedge 156 mm across, lit on its top face, in the lower third
# of the delivery frame.  That is the SAME defect class as the 685 mm error
# this function was repaired for, 40 mm away from where it was repaired.
# rev 60c-ii -- AND -1.830 WAS STILL TOO FAR AFT, FOR A SECOND AND DIFFERENT
# REASON: not the skin's width but the shell's UNDERSIDE at the CORNERS.  The
# tail's underside is a DISH that turns up violently into the flank over the
# last 30 mm.  Authored frame, ray-cast at the pan's own outer edge:
#
#     x        -1.700  -1.740  -1.760  -1.780  -1.800  -1.830
#     y 0.05    0.4045  0.4052  0.4054  0.4059  0.4096  0.4224
#     y 0.777   0.3995  0.4012  0.4027  0.4066  0.4167  0.4863   <- the corner
#
# The corner is FLAT to -1.780 and then climbs 80 mm in 30 mm of x.  A ramp
# reaching -1.830 at a flat top left a measured **-53.4 mm OPEN SLOT** at both
# outer corners -- which the first version of verify.py's slot row could not
# see, because its outermost sample was y 0.74 (F126).  The aft closer now
# stops at -1.800, where the corner is still only 0.4167, and the pan itself
# starts its ramp 60 mm further forward so the run stays a ramp (53 deg) and
# does not become a wall.  Everything aft of -1.800 is closed by the shell's
# OWN sheet metal, which is what that dish is.
# A ramp reaching further would have to taper in y, and nothing a photograph
# shows would settle its shape.
UNDER_TOP_F  = 0.4270               # >= shell 0.4165 at x +1.900, +10.5 mm
UNDER_TOP_A  = 0.4300               # >= shell 0.4167 at x -1.800, +13.3 mm
#                                   # -- and that is the CORNER value, not the
#                                   # centreline's 0.4096.  See the table below.
UNDER_RAMP_W = UNDER_W              # the ramps are the PAN's OWN width.
# The first cut made them 1.400 against the pan's 1.560, and the 80 mm ledge
# of pan left proud on each side kept its square aft face -- so the block
# still ended in mid-air behind the rear wheel and the ramp fixed nothing.
# Found by cropping the render AGAIN, at the same place, after the first fix.
# 1.400 had been chosen against WX at x -2.070 (0.777), a station the ramp no
# longer reaches.
#
# rev 60c RETRACTS what rev 60b then wrote here.  It read: "at its real
# stations, x 1.900 and -1.880, WX is 0.866 and 0.873, so the pan's own 0.780
# half-width clears the body at both."  WX(+1.900) is 0.8664, but
# WX(-1.880) is 0.7122 -- 0.873 is WX(-1.700), a station 180 mm away.  The
# sentence licensed the proudness above with a reading of the wrong station,
# in the commit whose subject was that a constant had been misused.


def underbody():
    """The closed pan under the body, plus the one chassis member a frame
    actually shows.  Ablations: T1_NOUNDER=1 omits the lot and
    probe_rev45_ground.py's C5 must REFUSE; T1_UNDER_YBUG / T1_UNDER_ZBUG /
    T1_UNDER_PROUD each restore one shipped defect so verify.py's underbody
    rows stay WATCHABLE (rule 3).

    NO SPEC SECTION.  rev 60b's docstring cited "SPEC 10.117", which is
    "rev 45 -- THE PAINT, INSTRUMENTED"; SPEC.md ends at 10.123 and has no
    underbody section at all.  Rule 34: the citation is withdrawn rather than
    replaced, because writing one would be inventing the record.  What this
    assembly is answerable to is `probe_rev45_ground.py` and verify.py's
    underbody rows, not a paragraph."""
    obs = []
    if os.environ.get("T1_NOUNDER") == "1":
        return obs
    # T1_UNDER_ZBUG=1 restores rev 60's z error -- the pan half its own depth
    # low, leaving a 45 mm slot, and the rails 78 % buried.  An independent
    # adversary reinstated exactly this on the repaired tree and every check
    # stayed green, because the rev-60b repair guarded only the ONE axis
    # STATE.md happened to already print.  verify.py's slot row must REFUSE it.
    _zbug = os.environ.get("T1_UNDER_ZBUG") == "1"
    _ztop = UNDER_TOP - UNDER_DROP / 2.0 if _zbug else UNDER_TOP
    xc = (UNDER_X0 + UNDER_X1) / 2.0
    ln = UNDER_X0 - UNDER_X1
    pts = _notched_rrect(UNDER_W, ln, 0.030,
                         floor_notches(xc, (T.X_AXLE_F, T.X_AXLE_R)),
                         WH_Y_IN - 0.002, seg=3)
    # rev 60b -- `_frame` extrudes +-depth/2 ABOUT THE ORIGIN ("extruded
    # +-depth/2 along w", its own docstring).  The first cut of this function
    # was written as if it extruded origin -> origin+depth, so EVERY prism here
    # was placed half its own depth wrong.  Origins are CENTRES.
    obs.append(T.solid_prism((xc, 0.000, _ztop - UNDER_DROP / 2.0),
                             (0, 1, 0), (1, 0, 0), (0, 0, 1), pts,
                             UNDER_DROP, name="underpan"))
    # the rails: built in the (x, z) plane and extruded across y, which is the
    # only orientation that can taper their ends into the pan.
    _rz_t = _ztop - UNDER_DROP + RAIL_EMBED
    _rz_b = _ztop - UNDER_DROP - RAIL_DROP
    if _zbug:                       # rev 60's rails: top flush, 78 % buried
        _rz_t, _rz_b = _rz_t + RAIL_DROP / 2.0, _rz_b + RAIL_DROP / 2.0
    _rx0, _rx1 = UNDER_X1 + RAIL_INSET, UNDER_X0 - RAIL_INSET
    rp = [(_rx0 + RAIL_TAPER, _rz_b), (_rx1 - RAIL_TAPER, _rz_b),
          (_rx1, _rz_t), (_rx0, _rz_t)]
    for sy in (1, -1):
        obs.append(T.solid_prism((0.0, sy * RAIL_Y, 0.0),
                                 (1, 0, 0), (0, 0, 1), (0, 1, 0), rp,
                                 RAIL_W, name="chassis_rail%+d" % sy))
    # the end closers: a ramp from the pan's floor up INTO the body's own
    # underside, so neither end stops in mid-air and neither leaves a slot.
    # Built in the (x, z) plane and extruded across y, which is the only
    # orientation that can taper in z.
    zb = _ztop - UNDER_DROP
    for xe, xo, zt_out, nm in ((UNDER_X0,  UNDER_RAMP_F, UNDER_TOP_F, "f"),
                               (UNDER_X1, -UNDER_RAMP_A, UNDER_TOP_A, "a")):
        # T1_UNDER_PROUD=1 restores rev 60b's aft ramp, which ran to x -1.880
        # at a flat half-width and top, and stood up to 48 mm proud of the
        # tapering tail.  verify.py's proudness row must REFUSE it.
        # rev 60c-ii: PINNED TO THE ABSOLUTE STATION, not to a length.  It was
        # written as `xo = -0.120`, which reproduced -1.880 only while the pan
        # ended at -1.760; when the pan's end moved to -1.700 the ablation
        # silently became a -1.820 ramp, which is INBOARD of the skin, and it
        # stopped exercising the proudness row at all.  An ablation expressed
        # as an offset from a constant that moves is not an ablation.
        if os.environ.get("T1_UNDER_PROUD") == "1" and nm == "a":
            xo, zt_out = (-1.880 - xe), UNDER_TOP
        prof = [(xe, zb), (xe + xo, zt_out), (xe, _ztop)]
        # y origin is 0.0 -- the CENTRELINE.  The first cut passed
        # -UNDER_RAMP_W/2 as well as the depth, so the two offsets ADDED and
        # both closers were built wholly on the off side, y -1.560..0.000,
        # 685 mm proud of the bodywork at their own station (1.560 - 0.875;
        # rev 60b wrote 919 mm in three files and it is reachable from no
        # half-width this vehicle has).  STATE.md printed the extent --
        # full-Y [-1.064, 1.150] -> [-1.560, 1.150] -- and nobody read the line.
        # T1_UNDER_YBUG=1 restores that error so verify.py's lateral-extent
        # row stays WATCHABLE (rule 3).  It must FAIL under it.
        _y0 = -UNDER_RAMP_W / 2.0 if os.environ.get("T1_UNDER_YBUG") == "1" else 0.0
        obs.append(T.solid_prism((0.0, _y0, 0.0),
                                 (1, 0, 0), (0, 0, 1), (0, 1, 0), prof,
                                 UNDER_RAMP_W, name="under_close_%s" % nm))
    return obs


def wheel_houses():
    """Close each wheel arch from inside -- the missing feature behind report 6.

    rev 59, THE OWNER: "a weird arc above the back wheel just kind of floating
    there".  Both liners were built as circles of radius WH_R and WH_R's own
    comment said that was `= t1_shell.ARCH_R, the arch cut's radius`.  THAT
    COMMENT WAS TRUE OF THE FRONT ARCH ONLY.  The front cutter is
    `T.cylinder((T.X_AXLE_F` -- a plain circle of ARCH_R, which the circular
    liner fills exactly, and the front wheel renders clean.  The REAR cutter
    is `T.solid_prism(... rear_arch_outline(T.X_AXLE_R) ...)`: superelliptical,
    ARCH_W_REAR = 0.920 m wide but only ARCH_R tall above the hub.  A 0.747 m
    circle inside a 0.920 m hole left the aperture UNLINED at both ends --
    measured on the outline itself, the circle is short by up to 87.2 mm of
    radius -- and through that crescent the render showed (a) the liner's rim
    and flat end caps as a dark arc stopping in mid-air and (b) van_floor's
    40 mm edge, seen edge-on, as a horizontal bar at hub height.  ref_side.jpg
    shows the real arch dropping to a uniform dark void with neither.

    ONE CAUSE, BOTH ARTEFACTS: the bar is only visible BECAUSE the liner
    under-fills the aperture, so nothing here touches FLOOR_W.

    The rear liner is driven from `rear_arch_outline` ITSELF, called exactly as
    the cutter calls it, so the two share their stations and ARCH_W_REAR's
    +-0.03 m cannot leave the liner behind.  Its two FLOOR points are dropped:
    they are the cutter's skirt down to z -0.400, not lip.
    """
    import os
    import t1_shell as S
    obs = []
    a0 = -math.radians(WH_SWEEP)
    a1 = math.pi + math.radians(WH_SWEEP)
    # ABLATION.  T1_WHCIRC=1 restores the circular rear liner so verify.py's
    # wheel-house reach row stays separately testable (rule 3: a control is
    # finished when you have WATCHED IT FAIL).
    circ = os.environ.get("T1_WHCIRC", "") == "1"
    for xa in (T.X_AXLE_F, T.X_AXLE_R):
        zc = S.arch_z(xa)
        # The FRONT stays on the circle -- it is the negative control, and its
        # cutter really is one.
        outline = None
        if xa == T.X_AXLE_R and not circ:
            outline = S.rear_arch_outline(xa)[:-2]
        for sgn in (1, -1):
            ob = _arc_liner(xa, zc, sgn, a0, a1, 56, f"wheelhouse{xa:.0f}{sgn}",
                            outline=outline)
            # Bake the offset into the MESH, not the object transform.  Setting
            # ob.location tripped build.py's step-8b assert -- the shear reads
            # v.co.x as world x and requires an identity transform on every
            # mesh.  The guard fired on the first run and it was right; the
            # geometry is what moves, never the guard.
            for v in ob.data.vertices:
                v.co.x += xa
                v.co.z += zc
            obs.append(ob)
    return obs


# ===========================================================================
# rev 44 -- THE CAB.  SPEC 10.104.
#
# THE OWNER SET THE BAR WITH A CATALOGUE-GRADE PRODUCT RENDER.  In a 78 mm
# front three-quarter hero the windscreen is a large, bright, TRANSPARENT part
# of the frame and the eye goes straight through it.  `probe_rev44_fidelity`
# counted what was behind it: `dash` **12 triangles**, `seat_back` 76,
# `seat_base` 76, and `wheel_rim` 448 -- a bare ring with no spokes and no
# hub.  Nothing else.  No second seat, no instrument, no gear lever, no
# pedals, no visors, no mirror.  A 4 m vehicle whose most-looked-at aperture
# opens onto four boxes.
#
# AND THE STEERING WHEEL WAS FACING SIDEWAYS.  `place(w, rot=(radians(72),
# 0, 0))` rotates a Z-normal disc about X, which takes its axis to
# (0, -0.951, 0.309) -- 18 degrees off the vehicle's own Y axis.  It was
# mounted like a ship's wheel on the cabin wall.  This needs no photograph and
# no scale to establish: it is a sign error, and the built dimensions print it
# -- 0.402 x 0.124 x 0.382, i.e. the disc's full diameter lies in X and Z and
# its 0.124 m Y extent is the projection of a disc whose normal is nearly Y.
#
# THE COLUMN CARRIED THE SAME SIGN ERROR, and the two are the same bug.  `col`
# ran along (+0.30, 0, 0.95) -- up and FORWARD -- which put its upper end at
# x 1.798 while the wheel it is supposed to carry sat at x 1.640, **158 mm
# behind it**.  A steering column rises from the box at the front beam and
# leans BACK to the driver, who is at x 0.98.  Corrected to (-0.30, 0, 0.95).
#
# THE WHEEL IS NOT RE-AIMED BY EYE.  A steering wheel is normal to its column
# and centred on the column's end -- that is what a steering wheel IS, and it
# is a constraint, not a measurement.  So the wheel's plane and centre are now
# both DERIVED FROM `col`: change the column and the wheel follows.  The angle
# that falls out is 17.5 degrees from horizontal, which is flat and bus-like,
# and it is flat because the column is at 17.5 degrees -- not because a number
# was chosen to make it look right.
#
# EVERYTHING ELSE HERE IS TYPE-CORRECT 1963 T1 CAB FURNITURE and it is
# DECLARED AS SUCH: no frame in this repo resolves the cab interior, so none
# of it is measured and none of it is offered as measured.  It is placed off
# members that ARE fixed -- the cab floor's top face, `Z_SILL`, the windscreen
# corners `P_TOP` / `P_BOT`, the column, and the existing seat's own
# footprint -- so it cannot drift independently of the shell.  Ledger class 4.
# ===========================================================================
# rev 44 -- COL_MID's x MOVED 1.735 -> 1.540, AND IT IS SOLVED, NOT NUDGED.
# Building a real fascia (DASH_SECT, rear face x 1.6900) exposed that the
# rev-8 column put the wheel's hub 18 mm BEHIND the dash's rear face, so the
# rim's forward sweep -- 0.1915 m at this column angle -- drove 173 mm of
# steering wheel THROUGH the dashboard.  Neither member had been built solidly
# enough before for the two to meet.
#
# Solved rather than eyeballed.  With a = (-sin f, 0, cos f) the rim's
# forward-most point is  COL_MID.x - sin f * COL_LEN/2 + R * cos f, so
# requiring DASH_CLEAR of daylight against DASH_SECT's rear face gives
# COL_MID.x <= 1.5467.  1.540 is that bound rounded down, and `_wheel_clear()`
# asserts it on the built numbers so the two can never drift back into each
# other (SPEC 10.45 -- a claim in prose is not a guard).
#
# WHAT THIS DOES NOT FIX, AND IT IS NAMED RATHER THAN ABSORBED: the DRIVING
# POSITION.  The hub now sits 622 mm ahead of the seat back's front face,
# which is roughly 150 mm more reach than a T1 driver has.  Closing that needs
# the seat's fore-aft position, which is rev-8 authored and UNMEASURED -- a
# second lever, and this revision already moved the column.  Ledger class 4.
COL_MID = (1.540, 0.372, 1.045)
COL_AX = (-0.30, 0.0, 0.95)        # rev 44: up and BACK.  Was +0.30 -- the
                                   # column leaned away from the driver.
COL_LEN = 0.420
COL_R = 0.019


def _col_top():
    a = Vector(COL_AX).normalized()
    return Vector(COL_MID) + a * (COL_LEN * 0.5), a


def _wheel_rot():
    """Rotation taking a Z-normal disc onto the column's axis.

    Ry(t) . (0,0,1) = (sin t, 0, cos t), so t = atan2(ax, az).  Written as the
    inverse of the thing it must satisfy rather than as an angle, so it stays
    correct if COL_AX ever moves (SPEC 10.25).
    """
    a = Vector(COL_AX).normalized()
    return (0.0, math.atan2(a.x, a.z), 0.0)


def _steering_wheel():
    """rim + two spokes + hub + horn button, all in the column's plane"""
    obs = []
    top, ax = _col_top()
    rot = _wheel_rot()
    RIM_MAJ, RIM_MIN = 0.1920, 0.0088          # unchanged from rev 8
    w = T.revolve([(0.0, RIM_MIN), (RIM_MIN, 0.0), (0.0, -RIM_MIN),
                   (-RIM_MIN, 0.0)], seg=72, axis='Z', name="wheel_rim")
    bm = bmesh.new(); bm.from_mesh(w.data)
    for v in bm.verts:
        r = math.hypot(v.co.x, v.co.y)
        if r > 1e-9:
            v.co.x *= (1 + RIM_MAJ / r); v.co.y *= (1 + RIM_MAJ / r)
    bm.to_mesh(w.data); bm.free()
    obs.append((place(w, loc=top, rot=rot), "dark"))

    # two spokes.  A 1963 T1 wheel is a TWO-spoke wheel and they run across
    # the car, which after the column rotation is this disc's local X.
    HUB_R, BOSS = 0.0480, 0.0110
    for s in (1, -1):
        pts = [(s * 0.038, -0.026), (s * (RIM_MAJ - 0.006), -0.0125),
               (s * (RIM_MAJ - 0.006), 0.0125), (s * 0.038, 0.026)]
        if s < 0:
            pts = pts[::-1]
        sp = T.solid_prism((0, 0, -0.004), (1, 0, 0), (0, 1, 0), (0, 0, 1),
                           pts, BOSS, name=f"wheel_spoke{s}")
        obs.append((place(sp, loc=top, rot=rot), "dark"))
    hub = T.cylinder((0, 0, -0.012), (0, 0, 1), HUB_R, 0.040, seg=40,
                     name="wheel_hub")
    obs.append((place(hub, loc=top, rot=rot), "dark"))
    horn = T.cylinder((0, 0, 0.012), (0, 0, 1), 0.0330, 0.012, seg=36,
                      name="wheel_horn")
    obs.append((place(horn, loc=top, rot=rot), "chrome_d"))
    return obs


# ------------------------------------------------------------------ the dash
# The section is a T1 fascia: a deep pressed panel whose top face lands on
# Z_SILL (the cab door's window sill, guarded every revision) and whose lower
# lip returns under.  Depth 215 mm, height 182 mm.  It replaces a 165 x 115 mm
# four-point box.  x is absolute; the section is swept the full cab width.
DASH_SECT = [
    (1.6900, 1.1900), (1.6900, 1.3720), (1.8000, 1.3745),
    (1.8800, 1.3600), (1.9050, 1.3000), (1.8800, 1.2300),
    (1.7900, 1.1900),
]
DASH_W = 1.520
DRIVER_Y = 0.372                    # = the column's y, not a second number


def _dash():
    obs = []
    d = T.solid_prism((0, 0, 0), (1, 0, 0), (0, 0, 1), (0, 1, 0),
                      DASH_SECT, DASH_W, name="dash")
    obs.append((d, "paint"))         # a T1 dash is painted the body colour

    # speedometer, normal to the column like everything the driver looks at
    rot = _wheel_rot()
    cx, cz = 1.8480, 1.3160
    for (r, ln, off, nm, key) in ((0.0760, 0.016, 0.000, "speedo_bezel", "chrome_d"),
                                  (0.0680, 0.010, -0.014, "speedo_face", "dark"),
                                  (0.0690, 0.004, 0.006, "speedo_glass", "glass")):
        c = T.cylinder((0, 0, off), (0, 0, 1), r, ln, seg=44, name=nm)
        obs.append((place(c, loc=(cx, DRIVER_Y, cz), rot=rot), key))

    # the centre "letterbox" -- radio grille aperture, recessed
    pts = T.rrect(0.2300, 0.0620, 0.012, seg=5)
    g = T.solid_prism((1.8830, 0.0000, 1.2960), (0, 1, 0), (0, 0, 1),
                      (1, 0, 0), pts, 0.020, name="dash_grille")
    obs.append((g, "dark"))

    # glovebox lid on the CABIN face, passenger side, with its knob
    pts = T.rrect(0.4000, 0.1150, 0.014, seg=5)
    gb = T.solid_prism((1.6870, -0.3900, 1.2750), (0, 1, 0), (0, 0, 1),
                       (1, 0, 0), pts, 0.014, name="dash_glovebox")
    obs.append((gb, "paint"))
    kn = T.cylinder((1.6760, -0.3900, 1.2750), (1, 0, 0), 0.0125, 0.016,
                    seg=24, name="dash_knob")
    obs.append((kn, "chrome_d"))
    return obs


# ------------------------------------------------------------------- seating
SEAT_Y = 0.400                       # the rev-8 driver's seat, kept exactly
SEAT_CORNER_SEG = 10                 # was 4: a 50 mm radius in 4 steps reads
                                     # as a chamfer, not as upholstery


def _seat(y, tag):
    obs = []
    pts = T.rrect(0.560, 0.470, 0.05, seg=SEAT_CORNER_SEG)
    obs.append((T.solid_prism((0.980, y, 0.8650), (0, 1, 0), (1, 0, 0),
                              (0, 0, 1), pts, 0.180, name=f"seat_base{tag}"),
                "dark"))
    pts = T.rrect(0.560, 0.470, 0.05, seg=SEAT_CORNER_SEG)
    obs.append((T.solid_prism((0.790, y, 1.1900), (0, 1, 0), (0, 0, 1),
                              (1, 0, 0), pts, 0.130, name=f"seat_back{tag}"),
                "dark"))
    # piping: a thin cream welt round the cushion's top edge, which is what
    # separates an upholstered seat from a block at any distance
    pts = T.rrect(0.548, 0.458, 0.05, seg=SEAT_CORNER_SEG)
    obs.append((T.solid_prism((0.980, y, 0.9540), (0, 1, 0), (1, 0, 0),
                              (0, 0, 1), pts, 0.016, name=f"seat_welt{tag}"),
                "cream"))
    return obs


# ----------------------------------------------------- visors, mirror, levers
def _cab_furniture():
    obs = []
    # Sun visors and the interior mirror hang just inside the windscreen, so
    # their x is SOLVED against the screen's own plane rather than typed.  The
    # screen runs P_TOP -> P_BOT, so x(z) = P_TOP.x + (P_TOP.z - z) * slope;
    # every part below is placed at that x minus GLASS_CLEAR.  Written this way
    # because the first draft of this block put the visor 21 mm and the mirror
    # stem 36 mm THROUGH the glass, and a number typed against a plane goes
    # stale the moment the plane moves.
    import t1_shell as S
    _slope = ((S.P_BOT.x - S.P_TOP.x) / (S.P_TOP.z - S.P_BOT.z))

    def _screen_x(z):
        return S.P_TOP.x + (S.P_TOP.z - z) * _slope

    for s in (1, -1):
        pts = T.rrect(0.3000, 0.1250, 0.018, seg=5)
        zv = 1.7250
        v = T.solid_prism((_screen_x(zv) - GLASS_CLEAR - 0.0625, s * 0.3400, zv),
                          (0, 1, 0), (1, 0, 0), (0, 0, 1), pts, 0.014,
                          name=f"visor{s}")
        obs.append((v, "cream"))
    # interior mirror, hung off the header rail on a short stem
    zm = 1.7000
    xm = _screen_x(zm) - GLASS_CLEAR - 0.0080
    pts = T.rrect(0.1700, 0.0520, 0.012, seg=4)
    obs.append((T.solid_prism((xm, 0.0000, zm), (0, 1, 0), (0, 0, 1),
                              (1, 0, 0), pts, 0.016, name="mirror_int"),
                "chrome_d"))
    # the stem leans UP AND BACK, because the screen does
    obs.append((T.cylinder((xm - 0.0050, 0.0, zm + 0.0290), (-0.35, 0, 0.94),
                           0.008, 0.050, seg=16, name="mirror_stem"),
                "chrome_d"))
    # gear lever -- floor mounted, rising up and back, with its knob
    obs.append((T.cylinder((1.2350, 0.0300, 0.8700), (-0.34, 0.05, 0.94),
                           0.0105, 0.400, seg=18, name="gear_lever"), "chrome_d"))
    kb = T.revolve([(-0.026, 0.0), (-0.018, 0.018), (0.0, 0.0245),
                    (0.018, 0.018), (0.026, 0.0)], seg=28, axis='Z',
                   name="gear_knob")
    obs.append((place(kb, loc=(1.1670, 0.0500, 1.0570)), "dark"))
    # pedals: clutch, brake, accelerator.  Small, but their absence is what
    # makes a cab floor read as a shelf.
    for (yy, w_, nm) in ((0.4800, 0.062, "pedal_c"), (0.3550, 0.062, "pedal_b"),
                         (0.2150, 0.048, "pedal_a")):
        pts = T.rrect(w_, 0.090, 0.010, seg=4)
        p = T.solid_prism((1.6100, yy, 0.6960), (0, 1, 0), (1, 0, 0),
                          (0, 0, 1), pts, 0.013, name=nm)
        obs.append((p, "dark"))
    return obs


# --------------------------------------------------------- cab door hinges
# rev 44, SPEC 10.104.  `probe_rev44_fidelity` counted the scene's fasteners
# and secondary hardware: rivet 0, bolt 0, screw 0, nut 0, HINGE 0, latch 0.
# A 1963 T1's cab door hangs on TWO EXTERNAL BUTT HINGES on its forward edge
# and they are among the most legible pieces of hardware on the flank -- they
# stand proud of the skin, they catch the key light on their barrels, and
# their absence is one of the things that makes a shell read as a shell.
#
# THEY ARE NOT PLACED BY EYE.  Both sit ON the cab door's own forward shut
# line -- `t1_shell.DOOR_GAP`'s front edge, which rakes back 0.0951 m over
# 0.950 m of height -- and the barrel's axis is that rake, so the hinge line
# is parallel to the edge it hangs from by construction.  Each is seated on
# the body surface by `t1_core.flank_y`, the same function the shut lines and
# the script use, so a hinge cannot float off a curved flank.
#
# The two heights are the only authored numbers and they are declared as
# authored: no frame in this repo resolves them.  They are placed at the
# quarter points of the door's own front edge, expressed that way rather than
# typed, so re-measuring the door moves them (SPEC 10.25).
HINGE_BARREL_R = 0.0112
HINGE_H = 0.0760
HINGE_PROUD = 0.0135


def door_hinges():
    import t1_shell as S
    edge = [(x, z) for (x, z) in S.DOOR_GAP if z > 0.80 and x > 1.70]
    edge.sort(key=lambda p: p[1])
    z0, z1 = edge[0][1], edge[-1][1]

    def edge_x(z):
        for i in range(len(edge) - 1):
            (xa, za), (xb, zb) = edge[i], edge[i + 1]
            if za <= z <= zb:
                t = (z - za) / (zb - za)
                return xa + t * (xb - xa)
        return edge[-1][0]

    rake = (edge[-1][0] - edge[0][0]) / (z1 - z0)
    ax = (rake, 0.0, 1.0)
    obs = []
    for frac in (0.25, 0.75):                 # quarter points of the edge
        z = z0 + (z1 - z0) * frac
        x = edge_x(z)
        for s in (1, -1):
            y = T.flank_y(x, z)
            obs.append(T.cylinder(
                (x, s * (y + HINGE_PROUD), z), ax, HINGE_BARREL_R, HINGE_H,
                seg=20, name=f"hinge_barrel{s}_{frac:.2f}"))
            pts = T.rrect(0.0480, HINGE_H * 0.86, 0.006, seg=4)
            obs.append(T.solid_prism(
                (x - 0.0180, s * (y + HINGE_PROUD * 0.42), z),
                (1, 0, 0), (0, 0, 1), (0, 1, 0), pts, HINGE_PROUD * 0.84,
                name=f"hinge_leaf{s}_{frac:.2f}"))
    return obs


DASH_CLEAR = 0.0150            # daylight the wheel keeps from the fascia
GLASS_CLEAR = 0.0120           # daylight cab fittings keep from the screen


def _wheel_clear():
    """Assert the steering wheel's rim clears the fascia's rear face.

    rev 44.  The first build of the real fascia drove 173 mm of steering wheel
    through it and nothing in the repo noticed, because neither member had
    ever been solid enough for the two to meet.  This is that check, armed on
    the built numbers rather than on the derivation, so re-angling the column,
    re-sectioning the dash or re-sizing the rim all re-run it.
    """
    a = Vector(COL_AX).normalized()
    top = Vector(COL_MID) + a * (COL_LEN * 0.5)
    # unit vector in the wheel's plane with the largest x
    u = Vector((a.z, 0.0, -a.x)).normalized()
    rim_max_x = top.x + 0.2008 * abs(u.x)
    dash_rear = min(p[0] for p in DASH_SECT)
    clear = dash_rear - rim_max_x
    assert clear >= DASH_CLEAR - 1e-4, (
        "the steering wheel's rim is INSIDE the dashboard: rim reaches "
        "x %.4f against the fascia's rear face at %.4f (%.1f mm of "
        "interference). SPEC 10.104." % (rim_max_x, dash_rear, -clear * 1000.0))
    return clear


def cab_fitout():
    """Everything inside the cab, as (object, material key) pairs.

    Returned as PAIRS rather than a flat list because `build.py` assigns one
    material per call, and the whole point of this revision is that the cab is
    not one dark mass: the fascia is body-coloured, the instrument is chrome
    and glass, the welts are cream.
    """
    _wheel_clear()
    obs = []
    obs += _steering_wheel()
    obs += _dash()
    obs += _seat(SEAT_Y, "")           # names kept: probe_rev38_wheelbar reads
    obs += _seat(-SEAT_Y, "_p")        # `seat_base` / `seat_back` by name
    obs += _cab_furniture()
    obs.append((T.cylinder(COL_MID, COL_AX, COL_R, COL_LEN, seg=20,
                           name="col"), "dark"))
    return obs


def interior():
    """The cab shell members that are ONE material -- floor and the slot
    backings.  Everything with furniture in it moved to `cab_fitout()` in
    rev 44, because a cab assigned a single "dark" key is a cab that reads as
    a void (SPEC 10.104).
    """
    obs = []
    # rev 59, same cause as van_floor: this pan reached 100 mm past the front
    # wheel house's inboard wall and its edge shows through the front arch --
    # 151 census rays through the side ortho, with a liner that fits its
    # aperture to -0.0 .. +0.0 mm.  See _notched_rrect.
    if os.environ.get("T1_WHFLAT") == "1":
        pts = T.rrect(FLOOR_W, 0.960, 0.05, seg=4)
    else:
        pts = _notched_rrect(FLOOR_W, 0.960, 0.05,
                             floor_notches(1.360, (T.X_AXLE_F,)),
                             WH_Y_IN - 0.002, seg=4)
    obs.append(T.solid_prism((1.360, 0, 0.6400), (0, 1, 0), (1, 0, 0),
                             (0, 0, 1), pts, 0.070, name="cab_floor"))
    obs += interior_fill()
    return obs


# ------------------------------------------------------- SPEC sec.6 backing
def _clip_below(pts, zmax):
    """the part of a closed (x, z) outline at or below zmax, closed off flat"""
    out = []
    n = len(pts)
    for i in range(n):
        x0, z0 = pts[i]
        x1, z1 = pts[(i + 1) % n]
        if z0 <= zmax:
            out.append((x0, z0))
        if (z0 - zmax) * (z1 - zmax) < 0.0:
            t = (zmax - z0) / (z1 - z0)
            out.append((x0 + t * (x1 - x0), zmax))
    return out


def interior_fill():
    """Back the through-slots and the serving bays so they read as DEPTH.

    MEASURED before this existed: at the `side` ortho camera 41 of the 76
    rays sampled along the cab-door outline crossed NO surface at all -- the
    two door gaps are collinear slots through both flanks, so the bus was
    see-through along the shut line.  Separately a ray through any of the
    three open serving bays hit nothing but the off-side glass pane at
    3.83 m: three 600 x 396 mm holes with nothing behind them.

    The physically honest fix, and the one that solves both: an inner skin.
    A dark door card 20 mm inboard of the outer skin spanning the door
    outline, and a galley backdrop behind the bays.

    Runs from D.interior(), i.e. AFTER every boolean, so it cannot perturb
    the shell.  All coordinates are UN-DROPPED (build.py step 8b has not run
    yet).  The 20 mm standoff matters: T.flank_y() is wrong by -5.6...+3.9 mm
    off the flat of the flank, so anything nearer than ~10 mm can punch back
    out through the 2.8 mm skin.
    """
    import t1_shell as S
    obs = []

    # ---- cab door: card below the glass, plus a ribbon behind the shut line
    # The outline is the CENTRELINE of a 5.5 mm slot, so a card bounded by it
    # leaves the outer half of the slot open.  The ribbon (+-10 mm, 3.6x the
    # slot) covers the whole groove including the top and side runs, where the
    # card cannot reach without blocking the door glazing.
    ZCARD = 1.4400                      # just above DOOR_MAIN's 1.402-1.438
    lower = _clip_below(S.DOOR_GAP_S, ZCARD)
    for s in (1, -1):
        obs.append(T.conform_solid(lower, s, off=-0.020, thick=0.004,
                                   name=f"doorcard{s}"))
        obs.append(T.conform_ring(S.DOOR_GAP_S, s, 0.020, off=-0.020,
                                  thick=0.004, name=f"doorback{s}"))

    # ---- the galley backdrop USED to be built here, in `dark` (albedo 0.115).
    # MEASURED, ref_side.jpg, inside the cut edge of bay 3: the wall you see
    # through the aperture is sRGB (175.2, 175.3, 174.8) -- neutral to 0.003
    # HSV saturation -- against the vehicle's own cream rear-corner panel in
    # the same frame at (238, 209, 202). An 11.5 %-albedo wall 1.34 m inside an
    # unlit box cannot produce that. It has moved to galley_dressing() below,
    # where it keeps its NAME and its POSITION (both were load bearing -- see
    # verify.py row 11f) and gets a measured albedo and a light to sit under.
    return obs


# =================================================================== GUTTER
def gutter():
    prof = [(0.0000, 0.0000), (0.0135, -0.0025), (0.0160, -0.0100),
            (0.0120, -0.0155), (0.0035, -0.0140), (0.0000, -0.0090)]
    obs = []
    # rev 16: the aft end follows the re-spaced shell.
    _gx0 = T._aft(-1.880)
    xs = [_gx0 + (1.806 - _gx0) * (i / 60) for i in range(61)]
    for s in (1, -1):
        path = []
        for x in xs:
            zt, rt = T.ZT_ALL(x), T.RT_ALL(x)
            # rev 16: RT_ALL grows 0.054 -> 0.0949 with the re-fitted roof
            # section, so `zt - 0.72*rt` is a constant tuned against another
            # constant and would drag the drip rail 28 mm up the new roll.
            # Expressed in terms of what it was tuned against: at rt = 0.054
            # the old form sat 0.01512 above the roll start zt0 = zt - rt.
            z = (zt - rt) + 0.01512
            path.append((x, s * (T.WX(x) * T.G(z) + 0.0015), z + 0.004))
        pr = [(a * -s, b) for (a, b) in prof]
        obs.append(T.sweep(path, pr, up=(0, 0, 1), name=f"gutter{s}"))
    return obs


# ==================================================================== MISC
def mirrors():
    obs = []
    for s in (1, -1):
        obs.append(T.cylinder((1.815, s * 0.905, 1.545), (0.16, s * 0.98, 0.10),
                              0.0105, 0.185, seg=18, name=f"mir_arm{s}"))
        head = T.revolve([(0.000, 0.0000), (0.014, 0.0620), (0.020, 0.0640),
                          (0.006, 0.0655), (-0.004, 0.0600),
                          (-0.004, 0.0000)], seg=44, axis='Y',
                         name=f"mir_head{s}")
        place(head, loc=(1.845, s * 1.052, 1.567), rot=(0, 0, s * -0.13))
        obs.append(head)
    return obs


# ==================================================================== WIPERS
# The shipped pair were BURIED.  Measured to 0.1 mm by an independent pass:
# the blade centre sat 17.3 mm BEHIND the windscreen plane and 8.5 mm below
# the aperture's lower edge, and every ray from either object toward every
# camera crossed exactly 2 body surfaces -- they rendered as nothing.  The
# geometry was wrong too: rrect(0.020, 0.300, 0.006) extruded along (0, 0, 1)
# is a flat plate lying in the XY plane, not a blade on a 63 deg raked screen,
# and wiper_pivot was a VERTICAL cylinder rather than a spindle normal to the
# cowl.
#
# MEASURED cowl surface (un-dropped): directly outboard of the old pivot the
# skin is at (2.0497, 0.150, 1.3852); 220 mm down-screen at y = +0.150 it is
# at (2.0520, 0.1500, 1.3868) with outward normal (0.791, 0.010, 0.612) --
# 37.7 deg from vertical, and 15.8 mm outboard of the windscreen plane.
# S.WS_N = (0.8886, 0, 0.4588).
COWL_PIVOT = (2.0500, 0.1500, 1.3860)       # un-dropped, |y|
COWL_N = (0.791, 0.010, 0.612)              # outward normal at the pivot
WIPE_LEN = 0.3000                           # blade length, along the screen
WIPE_STANDOFF = 0.0240                      # blade plane, out along WS_N
WIPE_PARK_DEG = 20.0                        # INFERRED: park lean, outboard
                                            # of screen-vertical.  Not
                                            # measurable in any reference we
                                            # hold; bottom-pivot and the
                                            # sweep direction are SPEC sec.4.


def wipers():
    """Two bottom-pivot wipers, period-correct for a 1963 T1.

    The blade is built IN the windscreen plane from S.WS_DIR / S.WS_N and
    pushed WIPE_STANDOFF out along the screen normal; the spindle is built
    along the measured cowl normal, not along +Z.  Everything here is
    registered in VISIBILITY_WATCH so visibility_fails() re-proves, off the
    built mesh, that a camera ray reaches them.
    """
    import t1_shell as S
    obs = []
    N = Vector(S.WS_N).normalized()          # out of the screen
    U = -Vector(S.WS_DIR).normalized()       # up-screen
    ph = math.radians(WIPE_PARK_DEG)
    for s in (1, -1):
        C = Vector((COWL_PIVOT[0], s * COWL_PIVOT[1], COWL_PIVOT[2]))
        Nc = Vector((COWL_N[0], s * COWL_N[1], COWL_N[2])).normalized()

        # spindle: axis along the cowl normal, 4 mm rooted / 30 mm proud
        piv = T.cylinder(tuple(C + Nc * 0.0130), tuple(Nc), 0.0090, 0.0340,
                         seg=16, name=f"wiper_pivot{s}")
        # profile deliberately does NOT close back on the axis: a
        # r=0 -> r=0 segment revolves into a ring of zero-area faces.
        boss = T.revolve([(0.0000, 0.0000), (0.0000, 0.0175),
                          (0.0060, 0.0168), (0.0085, 0.0120)],
                         seg=20, axis='X', name=f"wiper_boss{s}")
        _align_x(boss, Nc, C + Nc * 0.0015)
        obs += [piv, boss]

        # blade + arm live in the screen plane, parked leaning OUTBOARD;
        # the sweep from here is up and inboard (SPEC sec.4).
        S_AX = Vector((0.0, float(s), 0.0))          # outboard, in-plane
        d = (U * math.cos(ph) + S_AX * math.sin(ph)).normalized()
        bb = C + N * (WIPE_STANDOFF - _plane_d(C, S))
        base = bb + d * 0.0500                       # blade starts ON the glass
        tip = base + d * WIPE_LEN                    # 58 mm short of the head
        w = d.cross(N).normalized()                  # in-plane, across blade

        blade = _bar(base, tip, w, N, 0.0130, 0.0075, f"wblade{s}")
        # the arm sits 8 mm PROUD of the blade, as a real one does -- laid in
        # the same plane it was completely hidden behind the blade and the
        # spindle, which visibility_fails() caught: 0 of 24 samples reachable.
        arm = _bar(C + Nc * 0.0280,
                   bb + N * 0.0080 + d * 0.2000, w, N, 0.0075, 0.0055,
                   f"wiper_arm{s}")
        obs += [blade, arm]
        VISIBILITY_WATCH.extend([blade.name, arm.name, piv.name])
    FLAT.extend(o for o in obs if o.name.startswith(("wblade", "wiper_arm")))
    return obs


def _plane_d(p, S):
    """signed distance of p from the windscreen plane, along S.WS_N"""
    return (Vector(p) - S.WS_MID).dot(Vector(S.WS_N).normalized())


def _align_x(ob, axis, origin):
    """rotate a revolve(axis='X') so its axis points along `axis`"""
    a = Vector(axis).normalized()
    q = Vector((1.0, 0.0, 0.0)).rotation_difference(a)
    m = Matrix.Translation(origin) @ q.to_matrix().to_4x4()
    for v in ob.data.vertices:
        v.co = m @ v.co
    ob.data.update()
    return ob


def _bar(p0, p1, side_ax, up_ax, width, thick, name):
    """rectangular bar from p0 to p1, `width` across side_ax, `thick` deep"""
    c = (Vector(p0) + Vector(p1)) / 2.0
    L = (Vector(p1) - Vector(p0)).length
    ax = (Vector(p1) - Vector(p0)).normalized()
    pts = T.rrect(L, width, min(width, thick) * 0.35, seg=2)
    return T.solid_prism(tuple(c), tuple(ax), tuple(Vector(side_ax).normalized()),
                         tuple(Vector(up_ax).normalized()), pts, thick,
                         name=name)


def handles():
    """SPEC sec.4 / 2.3: ICE-PICK pull-lever cab handles.  Push-button
    handles are Dec 1963+, so the lever is the correct part for this bus."""
    obs = []
    # *** rev 50, A11 -- THE HANDLE WAS ON THE WRONG SIDE OF THE BELT. ***
    #
    # z = 1.330 was typed THREE times here with no citation anywhere in the repo
    # (grep finds 1.330 nowhere else).  S.Z_BELT_AUTH is 1.2720 in the same
    # un-dropped frame, so the handle was placed 58 mm ABOVE the two-tone break
    # BY CONSTRUCTION and rendered on the CREAM.  Both photographed vehicles put
    # it below the break, on the RED.
    #
    # MEASURED ON THE RED TARGET BUS IN ITS CURRENT ARTWORK -- not on the green
    # one.  ref_side.jpg has the cab door swung open, and a door swings about a
    # VERTICAL axis, so every z is preserved and the frame is admissible for the
    # STATION even though the door has moved.  Column band x 168..200, clear of
    # the leaning man (he starts at x ~210), 32-column means:
    #     cream/red break   row 438.1   (L 203.1 -> 81.3, R-G 7.6 -> 93.5)
    #     glazing sill      row 419.8   (L ~100 -> 208.7)
    #     the handle        row 477     (L 66.7 -> 162.9 -> 90.9 with R-G
    #                                    COLLAPSING 119.5 -> 30.3 -- achromatic,
    #                                    i.e. chrome, not paint and not a shadow)
    # QUOTED AS A RATIO, NOT A READING (rule 14), because the door is at its own
    # depth and no px/m on the flank applies to it:
    #     drop / band = (477 - 438.1) / (438.1 - 419.8) = 38.9 / 18.3 = 2.126
    # The GREEN bus gives 2.24 band-heights by the same construction -- 5 % away,
    # on a different vehicle, a different camera and a different artwork state.
    #
    # WHY THIS IS A RATIO AND NOT 0.289 m.  I nearly published a metric drop and
    # it does not survive: the band is 0.136 m if you take the survey's render
    # reading and 0.100 m if you take S.Z_SILL - S.Z_BELT_AUTH, a 32 % swing that
    # moves the answer from 0.219 m to 0.289 m.  I cannot adjudicate that from
    # the frames we hold, so the metric value is DERIVED FROM THE MODEL'S OWN
    # BAND at run time.  Whatever that band turns out to be, the handle follows
    # it, and the photograph contributes only the dimensionless 2.126.
    #
    # STILL WRONG, MEASURED, NOT BUILT: the SECTION.  ref_side.jpg at 7x
    # (probe_scratch/rev50/E1_ref_cabdoor_x7.png) shows a chrome pull lever lying
    # in an elliptical dish PRESSED INTO the door skin -- upper arc shadowed,
    # lower arc lit, which is a recess and not a proud part under top light.  The
    # build makes an rrect prism standing 12 mm PROUD with an 18 mm lever on top,
    # and it renders as a featureless white blob.  That is a separate change with
    # its own boolean, and it is NOT made here; this edit moves the station only.
    HANDLE_DROP_BANDS = 2.126        # MEASURED, ref_side.jpg, dimensionless
    # imported INSIDE the function on purpose: build.py loads t1_mats AFTER this
    # module, so a top-level import would be circular.  handles() is only ever
    # called at build time, by which point both are loaded.
    import t1_shell as _S, t1_mats as _MT
    _belt = _MT.Z_BELT_AUTH
    _band = _S.Z_SILL - _belt
    HANDLE_Z = _belt - HANDLE_DROP_BANDS * _band
    # GUARD, SAME EDIT (rule 12).  The handle must be BELOW the belt.  That is
    # the whole of what both photographs settle without any scale, and it is the
    # half that was wrong.  WATCHED FAIL on T1_HANDLEHI=1, which restores 1.330.
    if os.environ.get("T1_HANDLEHI"):
        HANDLE_Z = 1.330
    assert HANDLE_Z < _belt, (
        "cab door handle at z=%.4f is ABOVE the two-tone break at %.4f, so it "
        "renders on the CREAM.  Both photographed vehicles put it on the RED, "
        "below the break (ref_side.jpg, the RED target bus, at 7x)."
        % (HANDLE_Z, _belt))
    for s in (1, -1):
        y = T.WX(1.100) * T.G(HANDLE_Z)
        base = T.solid_prism((1.075, s * (y + 0.006), HANDLE_Z), (1, 0, 0),
                             (0, 0, 1), (0, s, 0),
                             T.rrect(0.115, 0.030, 0.012, seg=3), 0.012,
                             name=f"handle{s}")
        # the lever: a tapered pull standing 22 mm proud, pointed aft
        lever = T.solid_prism((1.060, s * (y + 0.018), HANDLE_Z), (1, 0, 0),
                              (0, 0, 1), (0, s, 0),
                              [(-0.048, -0.0075), (0.030, -0.0090),
                               (0.046, -0.0020), (0.046, 0.0020),
                               (0.030, 0.0090), (-0.048, 0.0075)],
                              0.018, name=f"handlever{s}")
        obs += [base, lever]
        FLAT.extend([base, lever])
        VISIBILITY_WATCH.append(lever.name)
    return obs


# =============================================================== VW ROUNDEL
def vw_logo(R=0.1385, w=0.0275, x=2.1215, depth=0.0110):
    """V over W in the Y-Z plane, as TWO closed mitred prisms. Never inverted.

    rev 8: was six independent overlapping bars, the same defect as
    t1_core.vw_bars -- SKEPTIC_PASS sec.D specifies two closed mitred prisms so
    the self-intersection is removed rather than hidden. Both call sites now
    share ONE implementation, which is why they drifted apart in the first place.
    """
    return T.vw_bars(R, w, (x, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 0),
                     depth, tag="vwbar", traced=True)   # THE NOSE opts in


def _fit_glyph(obs, target_r, ax=('y', 'z')):
    """Scale a finished V+W glyph in its own plane so the outline's extreme
    corner lands exactly on `target_r`.  Returns the scale applied.

    The scale is read back off the BUILT outline, not from a copy of
    t1_core's spine tables.  That matters: the glyph merged into an X twice
    because a number derived from those tables was written down as a literal
    and then went stale.  Nothing here can go stale -- if the spine or the
    width fraction ever changes, rmax changes with it.
    """
    rmax = max(math.hypot(getattr(v.co, ax[0]), getattr(v.co, ax[1]))
               for o in obs for v in o.data.vertices)
    s = target_r / rmax
    for o in obs:
        for v in o.data.vertices:
            setattr(v.co, ax[0], getattr(v.co, ax[0]) * s)
            setattr(v.co, ax[1], getattr(v.co, ax[1]) * s)
        o.data.update()
    return s


# ------------------------------------------------------- rev 71, F251/F256
# HOW FAR THE GLYPH'S EXTREME IS DRIVEN INTO THE BAND.  Three briefs called
# this "STILL UNMEASURED" and dropped it three times.  It is measured now,
# by `probe_rev71_emblem.py`'s E1, swept against the POSE-FREE IoU on two
# frames -- and it is measured on the ruler REPAIRED at rev 71 (F246), whose
# control passes at 0.9703.  On the BROKEN ruler 0.84 looked optimal; on the
# repaired one BOTH frames prefer a DEEPER fit.
#     FIT_R   ref_workshop   IMG_2073 (independent, re-cut box)
#     0.84      0.8379          0.8040     <- shipped rev 49..70
#     0.86      0.8425          0.8202     <- argmax on ref_workshop
#     0.88      0.8394          0.8215     <- argmax on IMG_2073
# T1_VW_FITCOEF=0.8 restores the old value exactly.
VW_FIT_COEF = float(os.environ.get("T1_VW_FITCOEF", 0.7))


def vw_logo_fit(ring_r, x=2.1215, depth=0.0110, wfrac=0.2283):
    """V over W sized so its strokes run INTO the roundel ring and stop flush
    with the ring's OUTER radius -- which is what the emblem does.

    rev 15.  MEASURED on ref_workshop.jpg, crop box (258,494,352,604), the
    only frame that shows the nose emblem.  The ring's outer boundary fits a
    conic to 0.111 px sd over 149 rays: vertical D 91.885 px, horizontal
    63.143 px (axis ratio 0.687 -- a strongly oblique view, so ONLY vertical
    extents are used and the ratio below is dimensionless).  Glyph vertical
    extent read off the labelled grid: top y 512.5 +/- 1.5 (the V's arms
    terminate in the ring band), bottom y 581 +/- 2 (the W's legs likewise)
    -> 68.5 +/- 2.5 px.

        glyph height / ring outer D  =  0.746 +/- 0.028     photograph
                                        0.5639              built (rev 14)
                                        0.7761              built (this fix)

    i.e. the glyph was 24 % undersized, 6.6 sigma out.  The fix is a pure
    scale expressed in terms of the ring radius; every angle, the 12.29 deg
    arm separation and the w/R proportion are untouched.

    WHY "flush with the ring's OUTER radius" and not some fitted number: in
    the photograph every stroke end -- both V arms, both W outer arms, both W
    legs -- disappears into the ring band, and the ring's outer boundary is
    unbroken.  Those two facts together fix the size geometrically, with no
    tuned literal to go stale.  It also lands inside both measurements of the
    ratio (0.746 +/- 0.028 here; 0.796 +/- 0.020 in the work-list).

    REFUTED, and reported rather than fixed because it lives in t1_core.py:
    t1_core.vw_bars' docstring claims "a clear 12.7 mm air gap between the V
    apex and the W peak at the locked ring diameter of 0.370".  There is no
    gap and there never was one at any diameter -- the V's outline dips
    37.66 mm below the W's outer-arm tops at ROUNDEL_D 0.280, and because the
    spine and the width both scale with R the overlap is a fixed FRACTION of
    R, so no diameter can open it.  The reference agrees: the V's apex sits
    on the W's centre peak, fused.  SPEC 10.25's premise is wrong, its fix
    (tying the glyph to the ring) is right, and the fusion must stay.
    """
    # ----------------------------------------------------------- rev 44
    # FITTING THE EXTREME TO THE RING'S **OUTER** RADIUS BURIED THE W.
    #
    # The owner reported the logo off the rev-44 hero.  Face-on it rendered as
    # a V, a centre peak and two stubs -- no W arms, no legs.  Isolated in an
    # empty scene the SAME objects render a clean V over W, so neither the
    # outline (rasterised and checked directly), the cap fill (area 0.012193 m2
    # against 0.01232 hand-computed) nor the renderer was at fault.
    #
    # THE RING IS IN FRONT OF THE GLYPH.  Built: ring x 2.1155..2.1290, glyph
    # x 2.1155..2.1265 -- the ring stands 2.5 mm proud.  Its band occupies
    # radius 0.112..0.140 (roundel()'s own profile, R down to R-0.028).  Fitted
    # to the OUTER radius the W's legs land at 0.140, so each arm spends its
    # whole outer half inside the band and is hidden by it.  What survived is
    # exactly what lies inboard of 0.112: the centre peak and the arm tops.
    #
    # The docstring above says the strokes should "stop flush with the ring's
    # OUTER radius ... every stroke end disappears into the ring band".  The
    # ends do -- but fitting the EXTREME there pushes the whole glyph out by
    # 1/0.84, and it is the arms, not just the ends, that go under the band.
    # Fitted instead so the extreme sits 20 % into the band, the ends still
    # visibly run into it and the arms stay clear.
    # rev 60, F63 / item C.  wfrac is the STROKE WEIGHT as a fraction of the
    # ring radius.  T1_VW_WFRAC overrides it so the weight can be swept against
    # the photograph's own topology without editing a constant -- see
    # probe_rev46_vw.py's T1_VW_WSWEEP.
    # rev 60b: the DEFAULT STAYS IN THE SIGNATURE.  The first cut moved it to
    # None and read it here, which broke `probe_rev54_wfrac.py` -- that probe
    # reads this default OUT OF THE SIGNATURE (inspect.signature) to reconcile
    # the nose and hubcap stroke weights, and it died with
    # "TypeError: must be real number, not NoneType".  Nothing invokes it, so
    # nothing caught it.
    # ----------------------------------------------------------- rev 66, F204
    # THE NOSE'S STROKE WEIGHT WAS 0.1800 AND THE PRESSING'S IS 0.2283.
    #
    # *[owner, rev 64]* "the strokes are thinner than the pressing's" -- and he
    # was right by two independent statistics that share no ruler:
    #
    #   probe_rev46_vw.py's OWN L6 -- stroke width / ring width AT THE SAME ROW,
    #     a horizontal divided by a horizontal, so the viewing angle's cosine
    #     cancels and it needs neither an axis ratio nor a radial registration.
    #     Built 0.1178 against the photograph's 0.1528.  L6 crosses 0.1528 at
    #     wfrac 0.2283 (converged 552-row raster: L6 0.1530).
    #   INK INSIDE THE BAND -- the red fraction of the disc strictly inboard of
    #     the band, photograph and build through one function.  Photograph
    #     0.525 +- 0.055, built 0.432.  Crosses at wfrac 0.2280.
    #
    # THE TWO AGREE TO 0.1 %.  L6 had read -0.0350 low since rev 46 and was
    # never acted on because it was buried in a residual that was 96 % ONE
    # BROKEN LANDMARK (F203).
    #
    # CEILING: the photographed roundel is 41 x 69 px and its ring is not
    # concentric with its own bbox (its annulus never reads 100 % red), so the
    # INK side is good to about +-0.02 in wfrac.  L6 does not depend on that
    # registration, which is why it is the one quoted first.
    # ----------------------------------------------------------- rev 73, F301
    # THE WEIGHT FOLLOWS THE SPINE.  F204's 0.2283 is the weight that puts the
    # SHIPPED spine's L6 on the photograph; a different spine has a different
    # L6 at the same weight, so the constant is not transferable and the
    # signature default is only correct for the on-band construction.
    # Swept live under the free spine, L6 crosses 0.1528 at ~0.2205 (F302).
    if T.vw_free():
        wfrac = T.VW_FREE_WFRAC
    wfrac = float(os.environ.get("T1_VW_WFRAC", wfrac))
    _BAND_FRAC = 0.028 / 0.140              # roundel()'s band / outer radius
    _FIT_COEF = VW_FIT_COEF

    obs = vw_logo(R=1.0, w=wfrac, x=x, depth=depth)
    # rev 60, F63 / item C.  T1_VW_PUREFIT=1 makes this a PURE UNIT CONVERSION.
    # t1_core.vw_bars' fixed point has already placed every terminal against
    # the band in R=1 units; re-normalising by the GLOBAL EXTREME here is a
    # SECOND normalisation that undoes it, dragging whichever end is not the
    # extreme back inside the band.  Rev 58 removed this on its own (cells
    # 6 -> 4, worse) and drove the near cap corner on its own (6 -> 4, worse);
    # neither works alone because each is half of one fix.  Together they are
    # the pair the rev-58 note says was never tried.
    if os.environ.get("T1_VW_PUREFIT") == "1":
        for o in obs:
            for v in o.data.vertices:
                v.co.y *= ring_r
                v.co.z *= ring_r
            o.data.update()
    else:
        _fit_glyph(obs, ring_r * (1.0 - _FIT_COEF * _BAND_FRAC))
    return obs


# ###########################################################################
#                       SPEC sec.4 DETAIL INVENTORY
#
# Everything below is built in build.py step 7, i.e. after solidify and after
# every boolean, so no cutter and no pipeline ordering is involved.
#
# FRAME: UN-DROPPED throughout.  build.py step 8b subtracts T.RIDE_DROP =
# 0.065 from every vertex at the very end, so above_ground = z - 0.065.
# ###########################################################################

def join(objs, name):
    """merge several meshes into one object and remove the originals.
    Keeps the object count down: 10 louvre slots per flank are one object,
    not ten, and 65 fringe balls per aperture are one object, not 65."""
    verts, faces = [], []
    for o in objs:
        base = len(verts)
        verts += [tuple(v.co) for v in o.data.vertices]
        faces += [tuple(base + i for i in p.vertices) for p in o.data.polygons]
    me = bpy.data.meshes.new(name + "_j")
    me.from_pydata(verts, [], faces)
    me.validate()
    ob = bpy.data.objects.new(name + "_j", me)
    bpy.context.collection.objects.link(ob)
    for o in objs:
        bpy.data.objects.remove(o, do_unlink=True)
    # rename only AFTER the sources are gone: joining objects whose target name
    # is already taken silently yields "<name>.001", and the caller then looks
    # up <name>, finds nothing, and the detail vanishes.  That cost the bobble
    # fringe its first build.
    ob.name = name
    ob.data.name = name
    return T.fix_normals(ob)


def shade_fix():
    """flat-shade the pressed / hard-surface details.  Call ONCE from build.py
    after the last A(), because A() force-smooths everything it touches."""
    n = 0
    for ob in FLAT:
        try:
            for p in ob.data.polygons:
                p.use_smooth = False
            ob.data.update()
            n += 1
        except ReferenceError:
            pass
    return n


def _brass(name="brass"):
    """rev 8: brass now lives in t1_mats.build_all() like every other material.

    It was defined here because build_all() had no brass key, which made it the
    last illegitimate CONSTANT-roughness material in the scene (STATE.md counted
    6; five are legitimately exempt -- the transmissive ones and the sealed
    reflector -- and this was the sixth). It now carries a roughness field.
    This shim resolves the shared datablock so the counter nosing and the plate
    surround pick up the real material rather than a private copy.
    """
    m = bpy.data.materials.get(name)
    if m:
        return m
    import t1_mats as _MT
    return _MT.tarnished(name, (0.6600, 0.4750, 0.1750), 0.255, 0.34)


# ============================================== TRUE-SURFACE CONFORMED DECAL
_DELTA = {}


def flank_delta(body, z, side=1,
                xs=(-1.60, -1.25, -0.85, -0.10, 0.40, 0.70)):
    """(measured body surface |y|) - T.flank_y(x, z), median over `xs`.

    T.flank_y() is the loft CAGE's analytic half width; the shell that gets
    rendered is the Catmull-Clark limit of that cage plus a 2.8 mm solidify,
    and below the bottom roll's tangent point (z ~ 0.508 un-dropped) the two
    part company.  MEASURED off the built mesh:

        z (un-dropped)   0.445   0.550   0.700   0.850   0.918   1.085
        surface - flank  +4.5mm  -0.2mm  -0.3mm  -0.0mm  -0.1mm  -0.0mm

    The script decal's bottom edge is at z = 0.445, so a panel placed on
    flank_y() + 1.6 mm sits 2.9 mm INSIDE the sheet metal there and the foot
    of the lockup disappears -- the same class of defect as the buried wipers.
    The error separates as WX(x) . G(z), so one median over several x samples
    is a correction in z alone; the median (not the mean) is what throws out
    the samples that fall down a shut line or through an aperture.
    """
    key = (round(z, 4), side)
    if key in _DELTA:
        return _DELTA[key]
    d = []
    for x in xs:
        ok, loc, _, _ = body.ray_cast(Vector((x, side * 3.0, z)),
                                      Vector((0.0, -side, 0.0)))
        if ok:
            e = abs(loc.y) - T.flank_y(x, z)
            if abs(e) < 0.020:                 # 20 mm: a slot or an aperture
                d.append(e)                    # reads hundreds of mm out
    d.sort()
    v = 0.0 if not d else (d[len(d) // 2] if len(d) % 2 else
                           0.5 * (d[len(d) // 2 - 1] + d[len(d) // 2]))
    _DELTA[key] = v
    return v


def conform_panel_true(body, x0, x1, z0, z1, side, off=0.0016, nx=40, nz=14,
                       name="pn"):
    """T.conform_panel(), but riding the MEASURED body surface.
    UVs identical to T.conform_panel so the texture is not mirrored."""
    verts, faces, uvs = [], [], []
    for iz in range(nz + 1):
        z = z0 + (z1 - z0) * iz / nz
        dy = flank_delta(body, z, side)
        for ix in range(nx + 1):
            x = x0 + (x1 - x0) * ix / nx
            verts.append((x, side * (T.flank_y(x, z) + dy + off), z))
            u = ix / nx
            uvs.append((u if side > 0 else 1.0 - u, iz / nz))
    for iz in range(nz):
        for ix in range(nx):
            a = iz * (nx + 1) + ix
            b = a + nx + 1
            faces.append((a, a + 1, b + 1, b))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.validate()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    T.fix_normals(ob)
    uvl = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li in poly.loop_indices:
            uvl.data[li].uv = uvs[me.loops[li].vertex_index]
    VISIBILITY_WATCH.append(ob.name)
    return ob


# ================================================ REAR-QUARTER AIR LOUVRES
# SPEC sec.4: 10 rear-quarter air-intake louvres PER SIDE (the 10th was added
# in March 1963).  0 of the 20 existed.
#
# MEASURED on ref_side.jpg, FRAME UN-DROPPED:
#   block X            -1.285 ... -1.670   (+-0.03/0.04), length 0.385
#
#   *** rev 49 -- READ THIS BEFORE QUOTING THAT 0.385. THE BUILD SHIPS 0.2952. ***
#
#   Both endpoints are passed through T._aft() twenty lines below (:2144).  _aft
#   is AFFINE with slope O_NEW / O_OLD = 0.773 / 1.008 = 0.7669, so it does not
#   merely MOVE the block -- IT SCALES ITS LENGTH.  0.385 x 0.7669 = 0.2953,
#   against the watched print of 0.2952 (probe_rev48_louv).  The arithmetic
#   closes to 0.1 mm.
#
#   THE RE-SPACING IS CORRECT AND MUST STAY.  This header says FRAME UN-DROPPED,
#   i.e. the 0.385 was read before the rear overhang was re-measured from
#   O_OLD 1.008 to O_NEW 0.773, so the whole aft end moves and this block moves
#   with it.  The BUILT 0.2952 is the value consistent with ref_side.jpg; a
#   row-profile read of the three strongest slot rows gives 0.286.
#
#   WHAT IS WRONG IS THIS COMMENT.  It presents 0.385 as the measurement of
#   record with nothing beside it, so anyone reading the header believes the
#   block is 385 mm long when the machine ships 295 mm -- a 90 mm gap, 2.2 sigma
#   outside the header's own stated +-0.03/0.04.  Rule 1: a claim in a source
#   comment is not a measurement, and this one outlived the number it described.
#   The block should be re-parameterised as (station, length) so the two cannot
#   drift again -- NOT DONE, because the LENGTH itself is unverified: three
#   independent estimators built at rev 49 to recover it from ref_side.jpg ALL
#   FAILED THEIR OWN KILL OR POSITIVE CONTROLS, one of them on the render where
#   the answer is exact.  PHOTOS_WANTED item 4 (the raking-light frame) is
#   currently scoped to the pressing DEPTH; the LENGTH and the STATION need it
#   too.
#   10 slots, pitch    21.1 mm
#   top slot centre    1.085  (1.020 above ground)
#   bottom slot centre 0.895  (0.830 above ground)
#   slot aperture      ~7 mm  (INFERRED -- 1.5 px, below the photograph's
#                              resolution)
#
# Count: block height 0.189 / pitch 0.0210 = 9 gaps = 10 slots.  Seven slots
# at 21 mm spans 0.126 m, 60 mm short of the measured block.  At 4.5 px pitch
# the signal is under the JPEG 8x8 DCT block, so the failure mode is MERGING;
# under-counting is possible, over-counting is not.
#
# Built HORIZONTAL in the body frame.  Rake measured +3.9 deg but the peak is
# broad (+2.2 ... +4.5) and confounded by JPEG block alignment, and 0-4 deg
# nose-up is not excluded, so horizontal is the defensible choice.
# rev 16: the rear-quarter air-intake louvre block is a station set on the
# quarter panel and re-spaces with it.
LOUV_X0, LOUV_X1 = T._aft(-1.2850), T._aft(-1.6700)
LOUV_N = 10
LOUV_Z_TOP, LOUV_Z_BOT = 1.0850, 0.8950
LOUV_PITCH = (LOUV_Z_TOP - LOUV_Z_BOT) / (LOUV_N - 1)          # 0.021111
# rev 48 -- THE SECTION HEIGHT IS NOW DERIVED, AND THE OLD ONE DID NOT
# RECONCILE.  The measured pitch is 21.11 mm and the header above records the
# slot aperture as ~7 mm (INFERRED -- 1.5 px, below the photograph's
# resolution).  Those two require a blade 21.11 - 7 = 14.1 mm tall.  The
# authored section was 11.0 mm, which leaves a 10.1 mm slot -- 44 % wider than
# the inferred aperture.  It never showed, because until this revision the
# shell was not cut and the "slot" was solid metal: the number could be wrong
# without anything being visibly wrong.
#
# With the aperture cut (louvre_cutters above) it shows immediately.  Measured
# on the identical instrument at the identical scale, probe_rev48_louv:
#     photographed |amp| 0.2059     built, 11.0 mm section  0.3506   1.70x TOO STRONG
# Too much open area reads too dark.  Derived from the two measurements that
# ARE grounded, so it cannot drift from them again (rule 2).
LOUV_APERTURE = 0.0070           # INFERRED, not measured -- 1.5 px in
                                 # ref_side.jpg, below its resolution.  It is
                                 # the one soft number in this block and it is
                                 # the one a raking-light photograph would fix
                                 # (PHOTOS_WANTED_rev48 item 3).
LOUV_SECT = LOUV_PITCH - LOUV_APERTURE            # 0.01411
_LP = [(0.0000, 0.0000), (0.0080, -0.0020),
       (0.0080, -0.0090), (0.0000, -0.0110)]      # authored 11.0 mm section
LOUV_PROFILE = [(a, b * (LOUV_SECT / 0.0110)) for (a, b) in _LP]
LOUV_OFF = 0.0020                       # ride 2 mm proud of the flank
LOUV_BAY_D = 0.070                      # depth of the dark box behind the
                                        # apertures.  NOT MEASURED -- it only
                                        # has to stop the cabin light, and it
                                        # must clear the wheel house.


def louvre_cutters():
    """ONE aperture per flank, behind the louvre blades.  rev 48.

    WHY THIS EXISTS.  `louvres()` below is explicit that it is "A sweep, not a
    boolean ... so the shell is never touched" -- which means the 20 blades
    have always been CLOSED RIBS laid on an UNBROKEN flank.  A T1 louvre is an
    APERTURE: the darkness in it is a cavity, not paint and not a shadow the
    blade happens to cast.  That is the fidelity bar the owner set with
    `bus_model_ref.JPG`, whose own nose louvres are modelled slots.

    ONE HOLE PER SIDE, NOT TWENTY, and that is a deliberate choice on two
    grounds, both measured:

      * ROBUSTNESS.  t1_core.py:230-244 records gap_englid as the model's most
        fragile boolean, and thin cutters are exactly what makes a boolean
        fragile.  Two large rectangles are the safest shape available.
      * THE VOLUME GUARD.  build.CUTTER_VOL_MIN is 1.0e-4 m3.  A single 7 mm
        slot 0.295 m long needs a 48 mm deep cutter just to clear it -- it
        would sit ON the limit, twenty times over.  The block aperture is
        0.19 x 0.295 x 0.30 = 1.7e-2 m3, two orders clear.

    The blades then span the hole and the gaps BETWEEN them are the slots, so
    the aperture is real and the geometry that reads is still the measured
    sweep.  Inset in x so the blade ends land on solid panel.

    AUTHORED FRAME.  This runs in step 3, BEFORE the rake shear, so it uses
    LOUV_Z_TOP/BOT as authored (0.8950/1.0850) and not the post-shear figures.
    """
    obs = []
    half = LOUV_SECT * 0.5              # the blade section's own half-height
    z0 = LOUV_Z_BOT - half - 0.0020
    z1 = LOUV_Z_TOP + half + 0.0020
    x0 = min(LOUV_X0, LOUV_X1) + 0.004
    x1 = max(LOUV_X0, LOUV_X1) - 0.004
    pts = T.rrect(x1 - x0, z1 - z0, 0.004, seg=4)
    pts = [(u + (x0 + x1) * 0.5, v + (z0 + z1) * 0.5) for (u, v) in pts]
    for s in (1, -1):
        obs.append(T.solid_prism((0, s * 0.80, 0), (1, 0, 0), (0, 0, 1),
                                 (0, s, 0), pts, 0.30, name=f"cut_louv{s}"))
    return obs


def louvre_backing():
    """A shallow dark box behind each louvre aperture.  rev 48.

    WITHOUT IT THE APERTURES LOOK STRAIGHT INTO THE LIT CABIN.  The first cut
    was rendered and looked at, and the slots came back as hard black bands
    with BRIGHT WHITE BARS among them -- `studio.cabin_fill()` shining out
    through the new holes, and in places straight through to the far flank's
    louvres.  Nothing in the numbers said so; the signed modulation went the
    right way (+0.0343 -> -0.0287) while the frame was visibly wrong.  SPEC
    10.105.7 and rule 28.

    Behind a T1's rear-quarter louvres is the ENGINE BAY -- shallow, unlit and
    boxed off from the cabin -- not the passenger compartment.  So the fix is
    not to close the slots again; it is to put the bay back.

    Sized off the aperture itself, never typed, and inset so it cannot poke
    through the flank.  Depth is shallow on purpose: it only has to stop the
    light, and a deep box would collide with the wheel house at x -1.29.
    """
    obs = []
    half = LOUV_SECT * 0.5
    z0 = LOUV_Z_BOT - half - 0.0060
    z1 = LOUV_Z_TOP + half + 0.0060
    x0 = min(LOUV_X0, LOUV_X1) - 0.006
    x1 = max(LOUV_X0, LOUV_X1) + 0.006
    pts = T.rrect(x1 - x0, z1 - z0, 0.004, seg=4)
    pts = [(u + (x0 + x1) * 0.5, v + (z0 + z1) * 0.5) for (u, v) in pts]
    for s in (1, -1):
        # T.solid_prism extrudes CENTRED on its origin, so the origin is
        # advanced half the depth to sit the box entirely INBOARD of the skin.
        y_skin = 0.86
        obs.append(T.solid_prism((0, s * (y_skin - LOUV_BAY_D * 0.5 - 0.004), 0),
                                 (1, 0, 0), (0, 0, 1), (0, s, 0),
                                 pts, LOUV_BAY_D, name=f"louvbay{s}"))
    return obs


def louvres(nx=13):
    """Pressed-lip sweeps riding the flank, both flanks, 10 per side = 20.

    A sweep, not a boolean: this runs in step 7, after every cut, so the shell
    is never touched.  The 11 mm section is centred on the measured slot
    centre, so slot k sits at LOUV_Z_BOT + k . pitch +- 5.5 mm.
    T.flank_y() is accurate to 0.1 mm over z = 0.884 ... 1.091 (measured), so
    the analytic ride is safe here -- unlike the decal panel further down the
    flank, which needs flank_delta().
    """
    obs = []
    for s in (1, -1):
        parts = []
        for k in range(LOUV_N):
            z = LOUV_Z_BOT + LOUV_PITCH * k
            path = [(LOUV_X1 + (LOUV_X0 - LOUV_X1) * i / nx,
                     s * (T.WX(LOUV_X1 + (LOUV_X0 - LOUV_X1) * i / nx)
                          * T.G(z) + LOUV_OFF), z)
                    for i in range(nx + 1)]
            pr = [(a * -s, b + LOUV_SECT * 0.5) for (a, b) in LOUV_PROFILE]
            parts.append(T.sweep(path, pr, up=(0, 0, 1),
                                 name=f"louvre{s}_{k}"))
        ob = join(parts, f"louvres{s}")
        FLAT.append(ob)
        VISIBILITY_WATCH.append(ob.name)
        obs.append(ob)
    return obs


# ==================================================== FUEL FILLER FLAP (5.1)
# SPEC sec.4: fuel filler flap on the RIGHT rear quarter, immediately aft of
# the louvres.  Right = -Y = the off side.  The x station and the height are
# INFERRED -- SPEC gives no coordinate and the flap is on the side neither
# photograph shows.  Placed one flap-width aft of the louvre block, centred on
# the louvre band.
# rev 16: FLAP_X is a station on the rear quarter, so it re-spaces with the
# shell.  Left at -1.7950 it would sit 78 mm forward of the tail skin, i.e.
# on the corner roll rather than on the quarter panel.
FLAP_X = T._aft(-1.7950)
FLAP_Z, FLAP_W, FLAP_H = 1.0100, 0.1450, 0.1450


def filler_flap():
    outline = [(u + FLAP_X, v + FLAP_Z)
               for (u, v) in T.rrect(FLAP_W, FLAP_H, 0.030, seg=5)]
    ob = T.conform_solid(outline, -1, off=0.0040, thick=0.0050,
                         name="fuel_flap")
    FLAT.append(ob)
    VISIBILITY_WATCH.append(ob.name)
    return [ob]


# ============================================= APERTURE BOBBLE FRINGE (5.2)
# SPEC sec.4 (grade R, Tacombi-specific): white bobble / ball-fringe trim
# round each serving aperture.  CONFIRMED present in ref_side.jpg -- a
# scalloped row of white balls runs round the inside edge of all three
# apertures.  Ball diameter and pitch are INFERRED (each ball is ~2 px).
FRINGE_R, FRINGE_PITCH, FRINGE_INSET = 0.0090, 0.0260, 0.0130


def _ball(verts, faces, c, r, nu=7, nv=4):
    base = len(verts)
    verts.append((c[0], c[1], c[2] + r))
    for j in range(1, nv):
        pv = math.pi * j / nv
        for i in range(nu):
            pu = TAU * i / nu
            verts.append((c[0] + r * math.sin(pv) * math.cos(pu),
                          c[1] + r * math.sin(pv) * math.sin(pu),
                          c[2] + r * math.cos(pv)))
    verts.append((c[0], c[1], c[2] - r))
    top, bot = base, len(verts) - 1
    for i in range(nu):
        faces.append((top, base + 1 + i, base + 1 + (i + 1) % nu))
    for j in range(nv - 2):
        a0 = base + 1 + j * nu
        b0 = a0 + nu
        for i in range(nu):
            k = (i + 1) % nu
            faces.append((a0 + i, b0 + i, b0 + k, a0 + k))
    a0 = base + 1 + (nv - 2) * nu
    for i in range(nu):
        faces.append((bot, a0 + (i + 1) % nu, a0 + i))


def _resample_closed(pts, pitch):
    """closed (x, z) polyline -> points at ~`pitch` spacing along it"""
    n = len(pts)
    seg = [(pts[i], pts[(i + 1) % n]) for i in range(n)]
    L = [math.dist(a, b) for (a, b) in seg]
    total = sum(L)
    m = max(4, int(round(total / pitch)))
    out, acc, k = [], 0.0, 0
    for i in range(m):
        want = total * i / m
        while k < n - 1 and acc + L[k] < want:
            acc += L[k]; k += 1
        t = 0.0 if L[k] < 1e-9 else (want - acc) / L[k]
        (ax, az), (bx, bz) = seg[k]
        out.append((ax + (bx - ax) * t, az + (bz - az) * t))
    return out


def bobble_fringe():
    """one merged mesh per aperture: the balls plus the tape they hang on"""
    import t1_shell as S
    obs = []
    for i, (xr, xf) in enumerate(S.BAYS):
        cx, cz = S.bay_centre(i)
        out = [(u + cx, v + cz) for (u, v) in S.bay_outline(i)]
        out = T.poly_offset(out, -FRINGE_INSET)
        pts = _resample_closed(out, FRINGE_PITCH)
        verts, faces = [], []
        for (x, z) in pts:
            y = S.SHOW_SIDE * (T.flank_y(x, z) + 0.0075)
            _ball(verts, faces, (x, y, z), FRINGE_R)
        me = bpy.data.meshes.new(f"fringe{i}")
        me.from_pydata(verts, [], faces); me.validate()
        ob = bpy.data.objects.new(f"fringe{i}", me)
        bpy.context.collection.objects.link(ob)
        T.fix_normals(ob)
        # the tape: a 3 mm ribbon on the rim the balls are sewn to
        tape = T.sweep([(x, S.SHOW_SIDE * (T.flank_y(x, z) + 0.0030), z)
                        for (x, z) in pts + [pts[0]]],
                       [(0.0000, 0.0060), (0.0030, 0.0060),
                        (0.0030, -0.0060), (0.0000, -0.0060)],
                       up=(0, 0, 1), name=f"fringetape{i}", caps=True)
        ob = join([ob, tape], f"fringe{i}")
        VISIBILITY_WATCH.append(ob.name)
        obs.append(ob)
    return obs


# ============================================ DRIP-RAIL BULB STRING (5.3)
# SPEC sec.4 (grade R): string of small bulbs along the drip rail.  CONFIRMED
# in ref_side.jpg -- a line of small warm bulbs runs along the rail above the
# cream band on the show side.  Pitch, bulb size and the fact that it is show
# side only are INFERRED.  Rendered as unlit pearl glass: this project has no
# emissive material and t1_mats is owned elsewhere.
# rev 13.  BULB_PITCH was 0.1350, which put 26 bulbs on a 3.50 m rail.  Measured
# TWICE, by two specialists working blind to each other and by different
# methods, and they agree:
#   * FFT along the string in ref_side.jpg, top-5 periods 6.05-6.30 px at
#     211 px/m  ->  pitch 28.6 +/- 1.0 mm, ~115 bulbs
#   * peak counting on three clean runs (x 460-600, 600-760, 770-900; 36 / 38 /
#     27 peaks) -> 4.0 +/- 0.5 px = 19 +/- 3 mm, quoted as <= 25 mm because it
#     is at the JPEG 4:2:0 Nyquist floor
# The FFT number is the admissible one (the peak count is aliasing-limited and
# its author said so).  The EXTENT is confirmed, not changed: the string runs
# model x +1.69 -> -1.64 photographed against -1.80 -> +1.70 built, +5 %.
# BULB_R stays 0.0110 -- 22 mm diameter against a 28.6 mm pitch still leaves
# air between them, which is what the photograph shows.  At the old pitch the
# spacing was the defect, not the size.
# rev 16: BULB_X0 re-spaced with the drip rail it hangs from.  BULB_PITCH is
# a MEASURED 28.8 +- 2.0 mm and must NOT be re-spaced -- the string does not
# stretch, it just runs out sooner.
BULB_X0, BULB_X1, BULB_PITCH, BULB_R = T._aft(-1.8000), 1.7000, 0.0286, 0.0110


def bulb_string(side=1):
    n = int(round((BULB_X1 - BULB_X0) / BULB_PITCH))
    wire, verts, faces = [], [], []
    for i in range(n + 1):
        x = BULB_X0 + (BULB_X1 - BULB_X0) * i / n
        # rev 16: same re-expression as t1_detail.gutter() -- the bulb string
        # hangs off the drip rail, so it must follow the roll START, not a
        # fraction of a roll radius that has since changed.
        z = (T.ZT_ALL(x) - T.RT_ALL(x)) + 0.01512
        y = side * (T.WX(x) * T.G(z) + 0.0180)
        wire.append((x, y, z - 0.0060))
        _ball(verts, faces, (x, y + side * 0.0020, z - 0.0245), BULB_R,
              nu=8, nv=5)
    me = bpy.data.meshes.new("bulbs")
    me.from_pydata(verts, [], faces); me.validate()
    ob = bpy.data.objects.new("bulbs", me)
    bpy.context.collection.objects.link(ob)
    T.fix_normals(ob)
    flex = T.sweep(wire, [(0.0026, 0.0026), (0.0026, -0.0026),
                          (-0.0026, -0.0026), (-0.0026, 0.0026)],
                   up=(0, 0, 1), name="bulbflex")
    ob = join([ob, flex], "bulb_string")
    VISIBILITY_WATCH.append(ob.name)
    return [ob]


# ================================================= PILLAR MENU CARDS (5.4)
# SPEC sec.4 (grade R): printed menu cards on the pillars between apertures.
# CONFIRMED in ref_side.jpg -- portrait cards with red text on each pillar.
#
# rev 11: SIZE AND HEIGHT MEASURED, and they were not "estimated off the
# aperture edges" -- they were guessed.  Card B, on the pillar between bay 1
# and bay 2, found by the column at which HSV saturation steps from the
# pillar's 0.11-0.13 to the card's 0.21-0.26 and back:
#     cols 432.0 - 452.0 (+-0.5)      rows 327.5 - 397.5 (+-0.5)
# Scaled by the local aperture band, whose two ends are both locked (bay 1
# 324.0-405.6, bay 2 314.8-400.0, linearly interpolated to the pillar station
# gives 319.4-402.8 = 83.4 px for 0.403 m) and by bay 1's width (107 px for
# 0.507 m):
#     CARD_W = 20.0/107  * 0.507 = 0.0948     was 0.0750  (+26 %)
#     CARD_H = 70.0/83.4 * 0.403 = 0.3383     was 0.3000  (+13 %)
#     centre  v = 0.5168 of the band          was the band centre exactly
#            -> z = 1.5667, i.e. 6.8 mm BELOW it
# Card centres check out against the model's pillar stations without moving
# them: measured X +0.884 / +0.256 / -0.388 against built +0.864 / +0.254 /
# -0.378, so only the card itself was wrong.
CARD_W, CARD_H, CARD_Z = 0.0948, 0.3383, 1.5667


def menu_cards():
    import t1_shell as S
    obs = []
    # pillar centres: forward of bay 0, and between the three bays
    xs = [(S.BAYS[0][1] + 0.9080) / 2.0,
          (S.BAYS[0][0] + S.BAYS[1][1]) / 2.0,
          (S.BAYS[1][0] + S.BAYS[2][1]) / 2.0]
    cz = CARD_Z
    for i, cx in enumerate(xs):
        outline = [(u + cx, v + cz)
                   for (u, v) in T.rrect(CARD_W, CARD_H, 0.005, seg=2)]
        ob = T.conform_solid(outline, S.SHOW_SIDE, off=0.0040, thick=0.0040,
                             name=f"menucard{i}")
        FLAT.append(ob)
        VISIBILITY_WATCH.append(ob.name)
        obs.append(ob)
    return obs


# ========================================== "1963" NUMBER-PLATE SURROUND (5.5)
# SPEC sec.4 (grade R): chrome number-plate surround on the engine lid reading
# "1963", EMPTY.  CONFIRMED in ref_rear34.jpg.  The digit forms are schematic
# (seven-segment bars); at the hero scale a digit is ~5 px.  FLAGGED.
PLATE_Z = 0.7800
PLATE_W = 0.3300
# rev 15 -- ASPECT CORRECTED.  See plate_1963's docstring for the measurement
# and its two controls.  The WIDTH is held and every Z dimension of the frame
# is scaled by _PV, so the frame keeps its shape and only its aspect changes.
PLATE_ASPECT = 1.9616                  # outer W/H, measured; was 1.4798 built
PLATE_OUTER_H = PLATE_W / PLATE_ASPECT
_PV = PLATE_OUTER_H / 0.2230           # vs the rev-14 authored outer height
PLATE_H = 0.1850 * _PV                 # aperture height
_PR_TOP, _PR_BOT = 0.0380 * _PV, 0.0180 * _PV
_PR_GAP = 0.0100 * _PV                 # top rail stands off the aperture
_PR_OFF = 0.0050 * _PV                 # side rails' vertical centre offset
_PR_SIDE = 0.0180                      # side rail WIDTH -- a y dimension, held
_PD_H = 0.0210 * _PV                   # digit height, must stay inside _PR_TOP
PLATE_TOP_Z = PLATE_Z + PLATE_H / 2 + _PR_GAP + _PR_TOP / 2
PLATE_BOT_Z = PLATE_Z - PLATE_H / 2 - _PR_BOT / 2
PLATE_OUTER_CZ = 0.5 * (PLATE_TOP_Z + PLATE_BOT_Z)
assert abs((PLATE_TOP_Z - PLATE_BOT_Z) - PLATE_OUTER_H) < 1e-12
SEG = {                      # a b c d e f g
    "1": "bc", "9": "abcdfg", "6": "acdefg", "3": "abcdg",
}


def _seg_bars(ch, cx, cy, w, h, t):
    """seven-segment digit -> list of (outline, ) rounded-rect outlines"""
    hw, hh = w / 2.0, h / 2.0
    G = dict(a=(cx, cy + hh, w, t), d=(cx, cy - hh, w, t), g=(cx, cy, w, t),
             f=(cx - hw, cy + hh / 2, t, h / 2), b=(cx + hw, cy + hh / 2, t, h / 2),
             e=(cx - hw, cy - hh / 2, t, h / 2), c=(cx + hw, cy - hh / 2, t, h / 2))
    out = []
    for k in SEG.get(ch, ""):
        x, y, bw, bh = G[k]
        out.append([(u + x, v + y) for (u, v) in
                    T.rrect(bw, bh, min(bw, bh) * 0.35, seg=2)])
    return out


def plate_1963(body=None):
    """chrome surround + schematic '1963' on its top rail, on the engine lid

    rev 15 -- THE "31-66 % TOO TALL" CLAIM IS NOT APPLIED, AND HERE IS WHY.

    Measured in ref_rear34.jpg, probe box (1065,615,1195,760).  Sub-pixel
    50 %-crossings of the paint/chrome step give four edge lines:

        top    y = -0.092442 x + 735.839   resid 0.204 px  (n=15)
        bottom y = -0.078131 x + 779.268   resid 1.031 px  (n=15)
        left   x = +0.052766 y + 1045.786  resid 0.391 px  (n=8)
        right  x = +0.087034 y + 1121.306  resid 0.826 px  (n=8)

    -> corners (1079.4,636.1) (1175.9,627.1) (1181.1,687.0) (1082.4,694.7),
    edge lengths 96.95 / 98.96 / 58.72 / 60.08 px, RAW IMAGE aspect 1.6492.

    The raw image aspect is not the aspect: the panel is oblique.  Rectified
    properly -- both vanishing points from the frame's own opposite edges,
    principal point at the image centre, square pixels, f solved from
    v1' . v2' = -f^2 -- f comes out 1667 px (39.6 deg hFOV, a 50 mm-equivalent
    lens: physically sensible) and

        plate outer W/H  =  1.470          rectified
                            1.4798         built          -> 0.05 sigma

    BUT the vanishing points are only ~1.2 sigma detections (the opposite
    edges' slopes differ by 0.0143 and 0.0342 against combined slope errors of
    0.0120 and 0.0343), so a Monte-Carlo over the four line-fit covariances
    gives 1.42 median with a 16-84 % band of 1.12-1.66 and a 5-95 % band of
    0.87-1.94.  A second, independent systematic: the rear panel is CURVED --
    the two long body grooves at y ~ 575 and ~ 595 fit straight lines with
    2.8 and 3.2 px residuals over 290 px -- so a planar rectification is only
    locally valid here at all.

    That route does not resolve the aspect to better than about +/- 20 %, and
    the built value sits at the centre of it -- so on its own it would have
    said "leave it alone".  IT IS SUPERSEDED, by a route that needs no
    vanishing point at all:

    THE WHEEL IS THE PROTRACTOR.  The cream rim is a circle (its outer
    boundary fits a circle to 0.35 px sd over 354 rays in ref_side.jpg), so
    its apparent aspect in ref_rear34.jpg IS the flank's foreshortening.
    Crop box (695,640,815,824): the cream annulus spans x 712..790 and
    y 660..805, AR = 1.847 +/- 0.055.  The flank normal and the rear-panel
    normal are perpendicular and both horizontal, so cos(theta_rear) =
    sin(theta_flank) and the factor that un-compresses the rear panel's
    HORIZONTAL is k = AR / sqrt(AR^2 - 1) = 1.1894 (+0.016 / -0.014 -- the
    sqrt makes it almost insensitive to AR).  Hence

        plate outer W/H = 1.6492 x 1.1894 = 1.962 +/- 0.034   photograph
                                            1.4798            built (rev 14)
                                                              -> +32.6 %, 14 sigma

    which lands on the LOW end of the work list's "+31 % to +66 %".  Nothing
    in this chain is a px/m scale; it is two image aspect ratios and one
    right angle.

    CONTROL: the tail lamp is round and sits on the corner ROUNDING between
    the two planes, so its apparent AR must fall between k (1.189, flat rear)
    and 1.847 (flank).  Measured 69.06 / 46.8 = 1.476.  It does.
    CONTROL: an independent metric route agrees.  The cream rim's 145 px
    vertical extent over its 0.4396 m OD is 330 px/m at the WHEEL, which is
    FURTHER from the camera than the plate, so 59.40 px of plate height is an
    upper bound of 0.180 m -- and 0.3300/1.962 = 0.168 m sits under it.

    The frame is therefore scaled in Z ONLY, by _PV, holding PLATE_W.
    """
    # rev 16: was -2.1070, fitted to the ARTEFACT tail surface at -2.1066
    # that the 110-gon cap pulled 1.4 mm forward.  With the Coons grid cap
    # the skin is flat at X_TAIL, so a re-typed constant would put this 1.0 mm
    # INSIDE the bodywork.  LOFT_GROUND sec.4.3 item 3.
    x = T.X_TAIL - 0.0004                         # 0.4 mm proud of the skin
    rails = [(0.0, PLATE_Z + PLATE_H / 2 + _PR_GAP, PLATE_W, _PR_TOP),
             (0.0, PLATE_Z - PLATE_H / 2, PLATE_W, _PR_BOT),
             (-PLATE_W / 2 + _PR_SIDE / 2, PLATE_Z + _PR_OFF, _PR_SIDE, PLATE_H),
             (PLATE_W / 2 - _PR_SIDE / 2, PLATE_Z + _PR_OFF, _PR_SIDE, PLATE_H)]
    parts = []
    for i, (cy, cz, w, h) in enumerate(rails):
        parts.append(T.solid_prism((x - 0.0040, 0.0, 0.0), (0, 1, 0), (0, 0, 1),
                                   (-1, 0, 0),
                                   [(u + cy, v + cz) for (u, v) in
                                    T.rrect(w, h, min(w, h) * 0.28, seg=2)],
                                   0.0160, name=f"platerail{i}"))
    frame = join(parts, "plate_1963")
    FLAT.append(frame)
    VISIBILITY_WATCH.append(frame.name)

    dz = PLATE_Z + PLATE_H / 2 + _PR_GAP        # top rail centre
    digits = []
    for i, ch in enumerate("1963"):
        cy = (i - 1.5) * 0.0210
        for j, o in enumerate(_seg_bars(ch, cy, dz, 0.0110, _PD_H, 0.0026)):
            digits.append(T.solid_prism((x - 0.0125, 0.0, 0.0), (0, 1, 0),
                                        (0, 0, 1), (-1, 0, 0), o, 0.0040,
                                        name=f"pd{i}_{j}"))
    d = join(digits, "plate_digits")
    FLAT.append(d)
    return [frame, d]


# =============================== ROOF PEAK VENT / ENGINE LID T-HANDLE (5.6)
def _surface_at(body, origin, direction):
    ok, loc, nor, _ = body.ray_cast(Vector(origin), Vector(direction))
    if not ok:
        return None, None
    return loc.copy(), nor.copy()


def roof_vent(body):
    """SPEC sec.4: roof peak vent over the windscreen.  Schematic -- a raised
    bezel with two ribs on the roof's front slope, not a working flap.
    FLAGGED as inferred: no reference we hold resolves it."""
    loc, nor = _surface_at(body, (1.8120, 0.0, 3.0), (0, 0, -1))
    if loc is None:
        return []
    u = Vector((0.0, 1.0, 0.0))
    w = nor.normalized()
    v = w.cross(u).normalized()
    o = loc + w * 0.0020
    parts = [T.solid_prism(tuple(o), tuple(u), tuple(v), tuple(w),
                           T.rrect(0.3600, 0.0620, 0.0120, seg=4), 0.0090,
                           name="roofvent")]
    for k in (-1, 1):
        parts.append(T.solid_prism(tuple(o + v * (k * 0.0150) + w * 0.0055),
                                   tuple(u), tuple(v), tuple(w),
                                   T.rrect(0.3300, 0.0060, 0.0020, seg=1),
                                   0.0060, name=f"roofvrib{k}"))
    ob = join(parts, "roof_vent")
    FLAT.append(ob)
    VISIBILITY_WATCH.append(ob.name)
    return [ob]


# rev 15 -- THE T-HANDLE IS BELOW THE PLATE, NOT ABOVE IT.
#
# ref_rear34.jpg.  Plate frame outer boundary from sub-pixel 50 %-crossings of
# the paint/chrome step (probe box (1065,615,1195,760); 15 columns per
# horizontal rail, 8 rows per side rail; line-fit residuals 0.20 / 1.03 / 0.39 /
# 0.83 px).  Handle centroid from the same step in probe box (1112,716,1140,754),
# stable to 0.85 px across thresholds RD < 70 / 80 / 90.
#
#     plate outer centre   (1129.69, 661.22) px      outer height 59.40 px
#     handle centroid      (1126.80, 737.27) px
#     displacement resolved along the panel-vertical (the mean of the two side
#     rails' image slopes, dx/dy = 0.0699) = 75.69 px BELOW
#
#     handle drop / plate outer height = 1.274 +/- 0.025      photograph
#                                       -1.076                built (rev 14)
#
# i.e. the build had it 240 mm ABOVE.  The ratio is dimensionless and both
# terms are VERTICAL extents a few tens of px apart, so neither the horizontal
# foreshortening nor any px/m scale enters.
#
# EXPRESSED AS A RATIO OF PLATE_OUTER_H ON PURPOSE, and this is not decoration.
# The plate frame was ALSO 32.6 % too tall (see plate_1963 above), and this
# handle is placed with the plate as its ruler, so the two are the same
# measurement.  Written as an absolute the two would drift: against the rev-14
# plate this ratio puts the handle 284 mm below the plate centre, against the
# corrected plate 214 mm -- and 214 mm is what the work list's own "205 mm
# BELOW" was reaching for.  Anyone who touches PLATE_ASPECT again moves this
# handle with it, automatically, which is the only way the photograph stays
# satisfied.
ENGLID_HANDLE_DROP = 1.274 * PLATE_OUTER_H


def englid_handle():
    """SPEC sec.4: engine lid T-handle, BELOW the number plate on the lid.

    Projection held to 30.6 mm.  This is the rear-most object on the vehicle
    and verify.py row 1 measures overall length across EVERY mesh object, so
    the aft extent here is load bearing: at 43 mm proud (the first cut) it
    alone pushed L to 4.310 and raised a warn.  See the note on CNT_X1.
    The rev-15 move is in Z ONLY -- x, size and material are untouched, and
    since the aft extent is an x quantity the length guard is unaffected.
    """
    # rev 16: same re-anchor as plate_1963 -- see LOFT_GROUND sec.4.3 item 3.
    x = T.X_TAIL - 0.0004     # 0.4 mm proud of the (now flat) tail skin
    z = PLATE_OUTER_CZ - ENGLID_HANDLE_DROP
    base = T.revolve([(0.0000, 0.0000), (0.0000, 0.0250), (0.0075, 0.0235),
                      (0.0100, 0.0170)], seg=24, axis='X', name="englid_esc")
    _align_x(base, Vector((-1.0, 0.0, 0.0)), Vector((x - 0.0020, 0.0, z)))
    stem = T.cylinder((x - 0.0244, 0.0, z), (-1, 0, 0), 0.0060, 0.0140,
                      seg=12, name="englid_stem")
    bar = T.solid_prism((x - 0.0276, 0.0, z), (0, 1, 0), (0, 0, 1), (-1, 0, 0),
                        T.rrect(0.0720, 0.0120, 0.0050, seg=2), 0.0060,
                        name="englid_bar")
    ob = join([base, stem, bar], "englid_handle")
    VISIBILITY_WATCH.append(ob.name)
    return [ob]


# ###########################################################################
#                    GALLEY DRESSING AND GALLEY LIGHT
#
# The three serving apertures are GLASSLESS.  Everything the eye is given at
# hero scale between z = 1.372 and 1.775 over 1.55 m of flank is whatever is
# behind them, and before this section that was one 11.5 %-albedo panel in an
# unlit box.  Measured, side ortho, inside the cut edge with a 25 mm inset:
# the render read display luma 22 / 33 / 24 against the photograph's
# 147 / 157 / 175.
#
# ------------------------------------------------------------ THE MEASUREMENT
# Method for every number below.  `ref_side.jpg`, apertures located by their
# own cut edges (REF_MEASUREMENTS sec.4/5: bay 1 x 323-430 y 324.0-405.6,
# bay 2 x 455-564 y 314.8-400.0, bay 3 x 588-699 y 309.4-398.0), then a
# feature is placed by its FRACTION (u across, v down) of that aperture and
# converted with the aperture's own locked model extents -- SPEC 10.11 and
# RULES 3/4: no ground line, no single px/m scale, and the fraction cancels
# both.  Uncertainty on a fraction read at 12x is +-0.02, i.e. +-10 mm in X
# and +-8 mm in Z.
#
#   feature                          bay  u            v            model
#   utensil rail (hook line)          3   0.02-0.98    0.055        Z 1.753
#   S-hooks on it                     3   .13 .26 .46 .60 .75 .90   X -0.503
#                                                                     -0.572
#                                                                     -0.677
#                                                                     -0.750
#                                                                     -0.829
#                                                                     -0.907
#   two hanging tools                 3   0.13, 0.26   0.05-0.46    Z 1.755-1.59
#   back-wall material change         3   0.34         -            X -0.614
#   worktop slab, front edge          3   0.12-0.52    0.685-0.760  Z 1.501-1.469
#   rack upper rail                   2   0.05-0.95    0.225        Z 1.684
#   rack shelf                        2   0.14-0.86    0.520-0.585  Z 1.565-1.539
#   wrapped item, pale                2   0.52-0.78    0.455-0.530  X -0.073..-0.207
#   wrapped item, green end           2   0.31-0.52    0.500-0.560  X +0.035..-0.073
#   red-labelled row, upper           2   0.02-0.30    0.05-0.35    X +0.185..+0.040
#   red-labelled row, lower           2   0.55-0.80    0.28-0.36    X -0.089..-0.218
#   dark appliance base               2   0.44-0.80    0.86-0.95    Z 1.428-1.392
#   pale stack on a high shelf        1   0.78-0.98    0.03-0.22    Z 1.763-1.686
#   shelf edge under it               1   0.80-0.98    0.22-0.32    Z 1.686-1.646
#   dark band, mid                    1   0.30-0.90    0.29-0.43    Z 1.658-1.602
#   pale item, bright column          1   0.82-0.98    0.50-0.80    Z 1.573-1.454
#   dark band A, under the rail       2   0.15-0.86    0.20-0.31    Z 1.694-1.650
#   dark band B, under the shelf      2   0.16-0.90    0.57-0.71    Z 1.545-1.489
#
# COLOUR, same crops, mean sRGB / HSV saturation:
#   back wall aft of the seam    (175.2, 175.3, 174.8)  S 0.003  NEUTRAL
#   back wall fwd of the seam    (199.0, 185.8, 172.2)  S 0.135  warm cream
#   worktop slab                 (216.1, 209.9, 205.5)  S 0.049
#   rack rail                    (146.3, 137.0, 132.8)  S 0.092
#   dark appliance base          (116.7, 116.0, 118.2)  S 0.018
#   pale stack, bay 1            (196.4, 191.2, 197.4)  S 0.031
#   amber bottle body            (183.2, 174.3, 150.8)  S 0.177
# and for scale, in the SAME frame:
#   cream rear-corner panel      (237.8, 208.5, 202.2)  L 214.3
#   cream flank above bay 3      (218.6, 187.1, 157.2)  L 191.6
#
# The single most important number in the whole table is the one that is NOT
# an object: NOTHING inside any aperture is darker than display luma 73, and
# the 2nd percentiles are 91 / 106 / 127.  The galley is a bright room.
#
# ------------------------------------------------------------------ THE LIGHT
# The physical reason it is bright is that THE ROOF IS CUT OPEN -- the vehicle
# is a convertible taco stand and both lids stand up over the counter, so the
# galley is daylit from above through a 1.11 x 2.03 m hole.
#
# THE SHELL DOES NOT CUT THAT HOLE.  build.py step 3 issues windscreen, side,
# rear and gap cutters and no roof cutter; `t1_shell.roof_lids()` builds the
# lids as free panels floating over an UNBROKEN roof skin.  So in the model
# the galley is a sealed 2.8 mm steel box and no exterior source can reach it,
# which is why no amount of `fill_galley` outside the flank has ever fixed
# this.  That is reported, not worked around: see the handoff.
#
# Until it is cut, the opening is stood in for HERE, at the plane where it
# physically is -- `gal_ceiling` is an emissive panel at the roof line.  It is
# not a cheat light bolted to the outside of the vehicle; it is the roof
# aperture, in the right place, with the right size, radiating downward.  The
# visible practical (`gal_tube`) is the second source and it is a real fitting
# the real vehicle has to have, because it serves after dark.
#
# Both are single scalars so they can be swept without editing this file:
#     T1_GAL_SKY   roof-aperture stand-in, emissive radiance
#     T1_GAL_LUM   the practical strip light
# ###########################################################################
# SOLVED, not chosen.  Both were swept together (the ratio between them is
# held, so the two sources keep their relative parts) against the display luma
# of the three apertures measured off the side ortho at 900 x 675 with the
# same boxes used on the photograph.  Three points on the film:
#     x1.00  ->  bay 3 read 217.1        (T1_GAL_SKY 6.50, T1_GAL_LUM 22.00)
#     x0.25  ->  bay 3 read 187.6
#     x0.138 ->  bay 3 read 174.8   against the photograph's 175.0
# The middle pair fixes the film's LOCAL slope at 49.0 display codes per
# decade of scene-linear, which is worth writing down: it is not the 70 codes
# a naive AgX two-point fit through middle grey and paper white predicts, and
# the first correction overshot because of it.
GAL_SKY = float(os.environ.get("T1_GAL_SKY", 0.90))
GAL_LUM = float(os.environ.get("T1_GAL_LUM", 3.04))

# Albedos.  SPEC 10.21's rule bites here: a rendered ratio is an albedo ratio
# only between two surfaces of the SAME CLASS under the SAME LIGHT, and the
# galley wall and the exterior cream are the same class under DIFFERENT light,
# so 175/214 may NOT be turned into an albedo.  What the photograph does fix
# is the CHROMATICITY (neutral to 0.003 aft of the seam, warm cream forward of
# it) and a LOWER BOUND: interior illumination cannot exceed exterior, so a
# wall reading 0.82x the cream panel's display luma cannot have an albedo
# below the cream's.  Both are therefore set to painted-white values at or
# above the body cream's 0.735, and the chromaticity is the measured one.
GAL_WHITE = (0.7300, 0.7300, 0.7355)     # neutral, aft of the seam
GAL_CREAM = (0.7500, 0.7040, 0.6420)     # warm, forward of the seam
# Brushed 304 stainless: normal-incidence reflectance 0.55-0.60, satin.  The
# first draft ran 0.615 at roughness 0.36 and the counter-top warmer rendered
# at display 211 against the cream counter's 186 -- BRIGHTER than the paint,
# where the photograph has it at 141 against 210.  That ratio may NOT be
# transferred (SPEC 10.21: a rendered ratio is an albedo ratio only between
# surfaces of the same class, and metal against dielectric is not), so this is
# corrected to the physical figures and no further: a white studio genuinely
# does make a stainless box bright, exactly as it genuinely does desaturate
# the paint, and that is the rig's account to settle, not this one's.
GAL_STEEL = (0.5600, 0.5630, 0.5690)     # brushed stainless, not a mirror
# These three ARE legitimate albedo ratios and SPEC 10.21's rule is satisfied
# rather than violated: each is a diffuse surface measured against the galley
# back wall IN THE SAME PHOTOGRAPH, INSIDE THE SAME ROOM, under the same
# light.  Ratios are taken in LINEAR light after undoing the sRGB encoding,
# then multiplied by the wall's 0.730.
#   dark appliance base  L 116.3 / 175.2 -> lin 0.171/0.428 = 0.400 -> 0.292
#   red-labelled rows    L 139.7 / 175.2 -> 0.253/0.428 = 0.591 -> 0.431
#                        L 148.4 / 175.2 -> 0.286/0.428 = 0.668 -> 0.488
# The first draft of this section had the labelled rows at (0.42, 0.07, 0.05),
# a saturated pillar-box red with luminance 0.148.  That is what they LOOK
# like at 12x and it is not what they MEASURE: the cluster means are
# (152.9, 137.0, 127.8) and (154.7, 146.9, 144.9), HSV saturation 0.164 and
# 0.063.  They are small red marks on a pale ground, and the area mean -- the
# only thing that survives to hero scale -- is a warm mid-tone.
GAL_DARK = (0.2900, 0.2880, 0.2970)      # the appliance base, S 0.018
GAL_RED = (0.5350, 0.3600, 0.3120)
GAL_GREEN = (0.1450, 0.3050, 0.1750)
GAL_AMBER = (0.4600, 0.2650, 0.0450)
GAL_SEAM_X = -0.6140                     # measured back-wall material change

GAL_Y_BACK = -0.4800                     # backdrop plane -- UNCHANGED, see 11f
GAL_Z_TOP = 1.4285                       # dark appliance base, measured top
GAL_Z_WORK = 1.5010                      # worktop slab, measured top


def _gm(name, base, rough=0.42, metal=0.0, spec=0.5, emit=None, estr=0.0,
        rvar=0.09, nscale=160.0):
    """A galley material.  Roughness is NEVER a constant on a diffuse surface
    here: STATE.md counts constant-roughness materials as a defect class and
    calls it the physical definition of the plastic look, so every non-
    emissive material below carries a noise field on Roughness."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Specular IOR Level"].default_value = spec
    b.inputs["Subsurface Weight"].default_value = 0.0    # verify row 6b
    if emit is not None:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = estr
    if rvar > 0.0:
        n = nt.nodes.new("ShaderNodeTexNoise")
        n.location = (-640, -220)
        n.inputs["Scale"].default_value = nscale
        n.inputs["Detail"].default_value = 4.0
        n.inputs["Roughness"].default_value = 0.55
        mr = nt.nodes.new("ShaderNodeMapRange")
        mr.location = (-400, -220)
        mr.inputs["From Min"].default_value = 0.32
        mr.inputs["From Max"].default_value = 0.68
        mr.inputs["To Min"].default_value = max(0.02, rough - rvar)
        mr.inputs["To Max"].default_value = min(0.97, rough + rvar)
        mr.clamp = True
        nt.links.new(n.outputs["Fac"], mr.inputs["Value"])
        nt.links.new(mr.outputs["Result"], b.inputs["Roughness"])
    return m


def _gcard():
    """The pillar menu card.

    MEASURED on the card between bay 1 and bay 2, ref_side.jpg (x 432-453,
    y 328-394, 20.4 x 65.7 px = 96 x 311 mm at the local 211.5 px/m):

        whole card      sRGB (225.5, 199.7, 174.5)  L 203.4  S 0.227
        cream pillar    sRGB (250.4, 238.2, 221.5)  L 239.6  S 0.116
        beside it

    So the card is 36 display codes BELOW the pillar it is stuck to and at
    almost exactly TWICE its saturation.  That pair -- darker AND warmer -- is
    the whole read at hero scale, and `capwhite` (0.890, 0.888, 0.872) can
    produce neither.  The layout is resolved at 14x and is the same on all
    three pillars: a thin red rule frames the card; a dark script logo sits in
    the top ~12 %; a red band under it; a body of small warm rows; a red band
    across the bottom ~8 %.  The individual WORDS are 1.5 px tall and are NOT
    MEASURABLE -- what is built is the band structure and the two measured
    colour statistics, not invented text.
    """
    name = "gal_menucard"
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.44
    b.inputs["Specular IOR Level"].default_value = 0.34
    b.inputs["Subsurface Weight"].default_value = 0.0
    tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (-1200, 0)
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); sep.location = (-1010, 0)
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    # v runs 0 at the card foot to 1 at its head (Generated Z on a conformed
    # panel whose long axis is world Z)
    prev = None
    #  (v0,   v1,   colour)              -- bands, foot -> head
    BANDS = [(0.000, 0.075, (0.4400, 0.0900, 0.0620)),   # red footer
             (0.075, 0.760, (0.7550, 0.6350, 0.5250)),   # warm text body
             (0.760, 0.830, (0.4400, 0.0900, 0.0620)),   # red header band
             (0.830, 0.940, (0.1450, 0.1250, 0.1180)),   # dark script logo
             (0.940, 1.000, (0.8100, 0.7600, 0.6900))]   # cream head margin
    x = -820
    for (v0, v1, col) in BANDS:
        rgb = nt.nodes.new("ShaderNodeRGB"); rgb.location = (x, -260)
        rgb.outputs[0].default_value = (*col, 1)
        if prev is None:
            prev = rgb.outputs[0]
            x += 200
            continue
        gt = nt.nodes.new("ShaderNodeMath"); gt.location = (x, -80)
        gt.operation = 'GREATER_THAN'
        gt.inputs[1].default_value = v0
        nt.links.new(sep.outputs["Z"], gt.inputs[0])
        mix = nt.nodes.new("ShaderNodeMix"); mix.location = (x, 60)
        mix.data_type = 'RGBA'
        nt.links.new(gt.outputs[0], mix.inputs["Factor"])
        nt.links.new(prev, mix.inputs[6])
        nt.links.new(rgb.outputs[0], mix.inputs[7])
        prev = mix.outputs[2]
        x += 200
    # the printed rows: a fine stripe field, so the body reads as TYPE and not
    # as a flat wash at any distance the hero cameras actually stand at
    wv = nt.nodes.new("ShaderNodeMath"); wv.location = (-820, 240)
    wv.operation = 'MULTIPLY'
    wv.inputs[1].default_value = 42.0
    nt.links.new(sep.outputs["Z"], wv.inputs[0])
    wave = nt.nodes.new("ShaderNodeMath"); wave.location = (-640, 240)
    wave.operation = 'FRACT'
    nt.links.new(wv.outputs[0], wave.inputs[0])
    ink = nt.nodes.new("ShaderNodeMath"); ink.location = (-460, 240)
    ink.operation = 'GREATER_THAN'
    ink.inputs[1].default_value = 0.55
    nt.links.new(wave.outputs[0], ink.inputs[0])
    inkc = nt.nodes.new("ShaderNodeRGB"); inkc.location = (-460, 420)
    inkc.outputs[0].default_value = (0.5150, 0.2050, 0.1550, 1)
    imix = nt.nodes.new("ShaderNodeMix"); imix.location = (240, 60)
    imix.data_type = 'RGBA'
    imix.inputs["Factor"].default_value = 0.34
    fac = nt.nodes.new("ShaderNodeMath"); fac.location = (60, 240)
    fac.operation = 'MULTIPLY'
    fac.inputs[1].default_value = 0.34
    nt.links.new(ink.outputs[0], fac.inputs[0])
    nt.links.new(fac.outputs[0], imix.inputs["Factor"])
    nt.links.new(prev, imix.inputs[6])
    nt.links.new(inkc.outputs[0], imix.inputs[7])
    nt.links.new(imix.outputs[2], b.inputs["Base Color"])
    return m


def _gbox(name, x0, x1, y0, y1, z0, z1, r=0.004, seg=2):
    """axis-aligned box from two corners, outline in XZ, extruded along Y"""
    ob = T.solid_prism(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
                       (1, 0, 0), (0, 0, 1), (0, 1, 0),
                       T.rrect(abs(x1 - x0), abs(z1 - z0), r, seg=seg),
                       abs(y1 - y0), name=name)
    FLAT.append(ob)
    return ob


def _gcyl(name, c, axis, rad, length, seg=16, smooth=True):
    ob = T.cylinder(c, axis, rad, length, seg=seg, name=name)
    if smooth:
        ob.data.shade_smooth()
    return ob


def galley_dressing():
    """Everything the eye is given through the three serving apertures.

    Returns a flat list of objects that already carry their own materials;
    spec4_details() routes it with a None key so build.py's material loop
    leaves it alone (the same contract counter_nosing() uses).

    DEPTH (Y) IS NOT MEASURABLE.  `ref_side.jpg` is a flank elevation and
    `ref_rear34.jpg` sees the bays at a grazing angle through their own
    frames, so every feature above is located in X and Z and in NEITHER
    photograph in Y.  Y is therefore chosen, not measured, and is chosen to
    two rules: nothing crosses |y| = 0.80 (verify row 11f casts a ray at each
    bay centre and FAILS if the first hit is outboard of that), and nothing
    intersects the fit-out that is already there (galley_top occupies
    y 0.325-0.795 up to z 1.395, the plancha y -0.460-0.100 up to z 1.455).
    """
    import t1_shell as S
    obs = []
    m_white = _gm("gal_white", GAL_WHITE, rough=0.62, spec=0.32, nscale=90.0)
    m_cream = _gm("gal_cream", GAL_CREAM, rough=0.58, spec=0.34, nscale=90.0)
    m_steel = _gm("gal_steel", GAL_STEEL, rough=0.44, metal=1.0, rvar=0.11,
                  nscale=220.0)
    m_dark = _gm("gal_dark", GAL_DARK, rough=0.52, spec=0.40)
    m_red = _gm("gal_red", GAL_RED, rough=0.40, spec=0.45)
    m_green = _gm("gal_green", GAL_GREEN, rough=0.44, spec=0.42)
    m_amber = _gm("gal_amber", GAL_AMBER, rough=0.26, spec=0.55)
    m_pale = _gm("gal_pale", (0.7650, 0.7550, 0.7700), rough=0.48, spec=0.36)
    # ---- rev 13: the roof-aperture EMISSIVE STAND-IN IS GONE.
    # rev 11 stood the un-cut roof opening in with an emissive panel; rev 12 cut
    # the real hole and hid the panel from camera rays but kept it lighting the
    # bays; rev 13 deletes it. The rectangle it occupied is still needed as a
    # footprint by nothing -- the hole is geometry now -- so only the two corner
    # stations survive, and they are still expressed in terms of the lid so that
    # moving the lid moves them (SPEC 10.25).
    #
    # `materials-5` note that must travel: the stand-in's over-run WAS the
    # duplication mechanism -- an emitter longer than all three bays and
    # near-symmetric about their centre subtends nearly the same solid angle at
    # each, so all three rendered the same reflection (NCC 0.94-0.97). Deleting
    # it removes the mechanism outright rather than de-symmetrising it. The
    # photograph's own figure is now measured for the first time and it is the
    # acceptance target: inter-bay NCC -0.102 / -0.228 / -0.127 against a
    # self-flipped null control of -0.148, i.e. the three bays are UNCORRELATED.
    # Acceptance: |NCC| <= 0.20.
    SKY_X0, SKY_X1 = S.LID_X1, S.LID_X0                     # -1.070 .. +0.964
    SKY_Y0, SKY_Y1 = S.LID_Y_HINGE, S.LID_Y_HINGE + S.LID_W  # -0.545 .. +0.565
    # the practical.  Warm-white fluorescent, which is what a taqueria runs.
    m_tube = _gm("gal_tube", (0.8200, 0.8150, 0.7950), rough=0.30, spec=0.40,
                 emit=(1.000, 0.918, 0.790), estr=GAL_LUM, rvar=0.0)

    def A(ob, mat):
        ob.data.materials.append(mat)
        obs.append(ob)
        return ob

    X0, X1 = -1.3000, 1.0400          # galley box, fore-aft
    # ---------------------------------------------------- 1. the liner
    # The backdrop keeps its NAME and its 24 mm slab at y = -0.480 (see
    # interior_fill); it is split at the MEASURED material change.
    A(_gbox("galley_backdrop", GAL_SEAM_X, X0, GAL_Y_BACK - 0.012,
            GAL_Y_BACK + 0.012, 1.2000, 1.8950, r=0.030, seg=3), m_white)
    A(_gbox("gal_backdrop_f", GAL_SEAM_X, X1, GAL_Y_BACK - 0.012,
            GAL_Y_BACK + 0.012, 1.2000, 1.8950, r=0.030, seg=3), m_cream)
    # end returns: without them a 3/4 camera looks along the flank past the
    # ends of the backdrop into unlit body cavity
    A(_gbox("gal_end_f", X1, X1 + 0.030, -0.5000, 0.2600, 1.2000, 1.8600),
      m_cream)
    # rev 52, A7 (brief SS5 item 4, "a second hole, which stands").  This wall
    # exists to stop a camera seeing past the backdrop into unlit body cavity --
    # the comment three lines up says so -- and it did not reach far enough to
    # do it.  MEASURED on the mesh: it spanned y -0.5000 .. +0.4000 against a
    # rear aperture of +-REAR_W/2 = +-0.5200, so 120.0 mm of the SHOW side and
    # 20.0 mm of the off side saw straight past it.  The half-width is now
    # DERIVED from the aperture that looks at it, not typed.
    # NOT the same datum as gal_end_f: that is the FORWARD return and the
    # rear window is not what looks at it (see LEDGER_rev52 SS8).
    # T1_ENDSHORT=1 restores the short wall so the guard can be watched failing.
    _ea_hw = 0.4000 if os.environ.get("T1_ENDSHORT") == "1" else S.REAR_W / 2.0
    A(_gbox("gal_end_a", X0 - 0.030, X0, -_ea_hw, _ea_hw, 1.2000, 1.8600),
      m_white)
    # rev 13: `gal_ceiling` IS DELETED.  It was an emissive stand-in for a roof
    # opening that did not exist; the opening has existed since rev 12 and the
    # stand-in was only still here because deleting it needed renders to
    # converge.  The owner settled what is actually up there before anything was
    # measured from it: looking down through the opening you see the BARE INSIDE
    # OF THE BODY'S OWN RED EXTERIOR PAINT -- no separate interior colour, no
    # headlining, no pale ceiling.  So the correct object is not a dimmer
    # emitter, it is no emitter: the studio rig lights the galley through the
    # hole, and what it lands on is red steel.
    #
    # He also named the sources: daylight through the roof opening, plus the
    # bulbs.  The bulb half of that is REFUTED by measurement and it is recorded
    # here because it changes the fix: the trim ringing each serving aperture
    # reads S 0.110-0.152 while the drip-rail festoon in the same rows reads
    # S 0.281-0.317 and 15-40 codes brighter.  The aperture surround is a matte
    # white bobble fringe, not lamps, and the only lit string is on the drip
    # rail OUTSIDE the skin, ~55 mm above the aperture heads, where it lights
    # the customer and cannot reach the galley.  The roof opening does all of it.
    _ceil = None
    # Nothing replaces it. The body is solidified to a 2.8 mm shell, so the
    # underside of the surviving roof strips either side of the opening is
    # already real geometry carrying the body material -- which IS the inside of
    # the red exterior paint the owner describes. Adding a panel here would put
    # a lid back over the hole, which is the defect rev 12 removed.
    del _ceil

    # ------------------------------------------- 2. the practical strip light
    # Tucked 20 mm under the head rail so the ortho flank and both studio 3/4
    # cameras see its LIGHT and not its filament, while the eye-height playa
    # camera looks up past the rail and sees the fitting -- which is correct,
    # a serving hatch shows you its strip light.
    A(_gbox("gal_tube_ch", 0.9000, -1.2000, -0.1900, -0.0500, 1.8020, 1.8280),
      m_steel)
    A(_gbox("gal_tube", 0.8900, -1.1900, -0.1820, -0.0580, 1.7880, 1.8020),
      m_tube)

    # ------------------------------------------------------- 3. the worktop
    # Top at the MEASURED 1.501, 32 mm slab.  It is a SHELF, not a counter,
    # and it stops at bay 3: the first draft ran it the length of the galley
    # 0.64 m deep and that is refuted by the photograph twice over -- the pale
    # slab is only present at u 0.12-0.52 OF BAY 3, and in bay 2 the field
    # below the same height reads L 170.3 at v 0.62-0.86, i.e. open lit wall
    # where a counter would have put an overhang shadow.  Rendered with the
    # long counter, bay 2 read p5 = 72.5 against the photograph's 110.8.
    A(_gbox("gal_worktop", -0.4200, -1.1800, -0.4400, -0.1800,
            GAL_Z_WORK - 0.032, GAL_Z_WORK), m_steel)
    # and the cupboard under it is set BACK from the shelf's front edge, which
    # is what lets the ceiling reach it: the photograph reads L 192.0 under
    # the slab, brighter than the wall behind the rack, so it is not in shade
    A(_gbox("gal_work_a", -0.4200, -1.1800, -0.4600, -0.2800, 1.2600,
            GAL_Z_WORK - 0.032), m_white)

    # -------------------------------------- 4. bay 3: utensil rail and tools
    rail_z, rail_y = 1.7530, -0.3600
    # rev 52, A9 / SURVEY_rev49 finding 28.  THE RAIL IS DERIVED FROM ITS OWN
    # BAY NOW, NOT TYPED.  It was built centre -0.3800 length 0.660, spanning
    # X -0.050 .. -0.710: 165 mm too LONG and 218 mm too far FORWARD, running
    # across the pillar into BAYS[1] where a rail measured "bay 3" cannot be,
    # and leaving THREE OF THE SIX HOOKS BELOW IT HANGING ON NOTHING (measured:
    # -0.750, -0.829, -0.907 against a rail ending at -0.710).
    # (The survey's own HEADLINE mis-signs this as "165 mm too short"; its body
    # has built 0.660 against measured 0.495, which is too long.  Body is right.)
    # Its measurement is "bay 3, u 0.02-0.98" -- so that is what it is built
    # from, and BAYS[2] carries the 0.5155 bay width and the -0.5980 centre.
    # T1_RAILSTALE=1 restores the typed rail so the guard can be watched failing.
    _RAIL_U0, _RAIL_U1 = 0.02, 0.98          # the rail's own measured extent
    _b3x0, _b3x1 = min(S.BAYS[2]), max(S.BAYS[2])
    _rx0 = _b3x0 + (_b3x1 - _b3x0) * _RAIL_U0
    _rx1 = _b3x0 + (_b3x1 - _b3x0) * _RAIL_U1
    if os.environ.get("T1_RAILSTALE") == "1":
        _rc, _rl = -0.3800, 0.660
    else:
        _rc, _rl = (_rx0 + _rx1) / 2.0, _rx1 - _rx0
    A(_gcyl("gal_rail", (_rc, rail_y, rail_z), (1, 0, 0), 0.0075, _rl),
      m_steel)
    for hx in (-0.5030, -0.5720, -0.6770, -0.7500, -0.8290, -0.9070):
        A(_gcyl(f"gal_hook{hx:+.3f}", (hx, rail_y, rail_z - 0.0180),
                (0, 0, 1), 0.0030, 0.0360, seg=8), m_steel)
    # two long thin tools, measured hanging to v 0.45 / 0.47
    for (hx, zb, w) in ((-0.5030, 1.5940, 0.0180), (-0.5720, 1.5860, 0.0230)):
        A(_gbox(f"gal_tool{hx:+.3f}", hx - w / 2, hx + w / 2,
                rail_y - 0.014, rail_y + 0.014, zb, rail_z - 0.024, r=0.006),
          m_steel)

    # ------------------------------------------------ 5. bay 2: the tube rack
    # y is chosen, not measured (see the docstring), but it is not free: at
    # y -0.42..-0.16 the rack stood 60-320 mm off the back wall and shadowed
    # it, and bay 2 rendered at median 143.0 against the photograph's 164.1
    # while bay 3, which has no rack, sat on target.  The photograph shows no
    # such shadow -- the wall behind the rack reads L 165.4 and L 170.3 in the
    # two bands either side of it -- so the rack is carried FORWARD, toward
    # the aperture, where it shades the counter rather than the wall.
    rk_y0, rk_y1 = -0.3200, -0.0600
    for (rz, nm) in ((1.6840, "gal_rack_hi"), (1.5530, "gal_rack_lo")):
        A(_gcyl(nm, (0.2800, (rk_y0 + rk_y1) / 2, rz), (-1, 0, 0), 0.0070,
                0.680), m_steel)
    A(_gbox("gal_rack_shelf", 0.2800, -0.4000, rk_y0, rk_y1, 1.5460, 1.5530,
            r=0.003), m_steel)
    for ux in (0.2700, -0.3900):
        A(_gbox(f"gal_rack_up{ux:+.3f}", ux - 0.006, ux + 0.006,
                rk_y0 + 0.010, rk_y0 + 0.022, 1.5300, 1.6910, r=0.003),
          m_steel)
    # the wrapped item on the shelf: pale body, green end (measured X spans)
    _wy = (rk_y0 + rk_y1) / 2 - 0.020
    A(_gcyl("gal_wrap", (-0.0730, _wy, 1.5760), (-1, 0, 0), 0.0155,
            0.1340), m_pale)
    A(_gcyl("gal_wrap_g", (-0.0730, _wy, 1.5760), (1, 0, 0), 0.0125,
            0.1080), m_green)
    # The two red-labelled rows are FLAT ON THE WALL, not standing on a shelf.
    # The first draft stood them on a shelf of its own invention; the shelf is
    # not in the photograph, and it shadowed the wall it was meant to dress.
    # Flat printed matter is also what the pixels say: HSV saturation 0.164 and
    # 0.063 over the two clusters is small red marks on a pale ground, which is
    # a poster or a taped-up price list, not five red tins.
    _sy = GAL_Y_BACK + 0.012
    for i, hx in enumerate((0.1700, 0.1150, 0.0600)):
        A(_gbox(f"gal_can_u{i}", hx - 0.0225, hx + 0.0225, _sy, _sy + 0.0060,
                1.6340, 1.7550, r=0.004), m_red)
    for i, hx in enumerate((-0.1100, -0.1850)):
        A(_gbox(f"gal_can_l{i}", hx - 0.0300, hx + 0.0300, _sy, _sy + 0.0060,
                1.6300, 1.6620, r=0.004), m_red)
    # the dark appliance base, measured top 1.4285.  Its identity is NOT
    # MEASURABLE -- it is 4 px tall and reads (117, 116, 118); what is built
    # is a low dark block at the measured X span and the measured top.
    A(_gbox("gal_appliance", -0.0320, -0.2180, 0.2600, 0.5000, 1.3950,
            GAL_Z_TOP, r=0.008), m_dark)

    # ------------------------------------------ 6. bay 1: high shelf and stack
    # The forward end of bay 1 is MEASURABLY darker than the back wall and it
    # is clear of the man who works in the aft two thirds: at u 0.05-0.35 the
    # photograph reads (162.0, 145.9, 139.0) L 148.9 over Z 1.755-1.634 and
    # (135.2, 130.8, 130.6) L 131.7 over Z 1.553-1.392, against the same
    # frame's back wall at L 175.2.  That is 0.50-0.62 of the wall's
    # luminance, warm at the top and neutral at the foot.  WHAT it is is NOT
    # MEASURABLE -- a cupboard, a fridge flank, a stack of crates all fit -- so
    # what is built is a full-height mid-tone upright at the measured X span
    # and the measured reflectance ratio, and nothing is claimed about it.
    A(_gbox("gal_upright", 0.6200, 0.8300, -0.4400, -0.0600, 1.2600, 1.7800,
            r=0.010), _gm("gal_upright_m", (0.4450, 0.4020, 0.3800),
                          rough=0.56, spec=0.30, nscale=110.0))
    A(_gbox("gal_shelf_b1", 0.4700, 0.2900, -0.4200, -0.1800, 1.6740, 1.6860,
            r=0.003), m_steel)
    for i, hx in enumerate((0.4200, 0.3600)):
        A(_gbox(f"gal_stack{i}", hx - 0.0270, hx + 0.0270, -0.3900, -0.2100,
                1.6860, 1.7630 - i * 0.0180, r=0.008), m_pale)

    # ============================== 6b. INTERNAL CONTRAST, bays 1 and 2
    # The bays have the right LEVEL and the wrong SPREAD: measured inside the
    # cut edge, bay 1 renders sd 15.3 against the photograph's 28.4 and bay 2
    # sd 10.2 against 24.7, while bay 3's distribution already matches.
    #
    # METHOD.  ref_side.jpg, each aperture divided into a 10 (u) x 7 (v) cell
    # map of Rec.709 display luma, cells 5 % inset from the cut edge, u = 0 at
    # the FORWARD edge and v = 0 at the head rail; a cell is then converted
    # with that aperture's own locked model extents, which is the only way that
    # survives the flank's non-constant px/m (194.8 at the rear panel against
    # 211.5 mid-body).  x = X_front - width * u,  z = 1.7750 - 0.4030 * v.
    # Everything below is a reflectance RATIO against the back wall in the same
    # frame and the same light -- both are matte painted wall-class surfaces,
    # so the ratio is an albedo ratio and nothing else (SPEC 10.12/10.21).
    # Bays 1 and 2 are FORWARD of the seam, so their wall is the warm cream one
    # at (199.0, 185.8, 172.2), L 187.6, and the ratios are taken against that.
    #
    #   bay 1  dark band     u 0.30-0.90  v 0.29-0.43  L 111.7  ratio 0.595
    #   bay 1  pale item     u 0.82-0.98  v 0.50-0.80  L 200.4  ratio 1.068
    #   bay 2  dark band A   u 0.15-0.86  v 0.20-0.31  L 145.4  ratio 0.775
    #   bay 2  dark band B   u 0.16-0.90  v 0.57-0.71  L 150.1  ratio 0.800
    #
    # WHAT any of these things ARE is NOT MEASURABLE at 1024 x 768 -- the dark
    # bands are 10-12 px deep.  So what is built is the `gal_upright`
    # precedent: a panel at the measured u/v span carrying the measured
    # reflectance ratio, and nothing is claimed about its identity.
    #
    # HONEST LIMIT, twice over.  (a) Bay 1's 28.4 is not all reachable by
    # dressing.  Split the photograph's bay 1 at u 0.35, the line the man works
    # aft of: the man-free forward third reads sd 28.6 and the aft two thirds,
    # which contain him, read 38.0, giving the whole bay 35.9 in this crop.  A
    # bay dressed to look like its own man-free third would therefore reach
    # 28.6/35.9 = 0.80 of the total, i.e. about sd 23 of the quoted 28.4; the
    # other 37 % of the VARIANCE is the man and the surfaces he occludes and no
    # dressing can produce it.  (b) The photograph's 5th percentiles (101.9 /
    # 110.6) sit well below any 10x7 cell mean (min 107 / 130), so a real part
    # of the spread is at a finer scale than this map can resolve -- edges,
    # gaps and shadow lines, which is exactly what bay 3 has in its six hooks
    # and two hanging tools and why bay 3 already matches.  These four elements
    # are what the map SUPPORTS; they are not expected to close the gap alone.
    #
    # Y is chosen, not measured (see the docstring), but it is chosen to two
    # extra rules here: nothing intersects the fit-out already in the bay, and
    # each bay's new panel sits at a DIFFERENT depth (bay 1 at -0.466, bay 2 at
    # -0.450) so the two bays do not repeat one parallax -- the same
    # `materials-5` duplicate the ceiling footprint above is aimed at.
    m_band1 = _gm("gal_band1_m", tuple(0.595 * c for c in GAL_CREAM),
                  rough=0.58, spec=0.30, nscale=110.0)
    m_band2 = _gm("gal_band2_m", tuple(0.775 * c for c in GAL_CREAM),
                  rough=0.58, spec=0.30, nscale=110.0)
    m_band3 = _gm("gal_band3_m", tuple(0.800 * c for c in GAL_CREAM),
                  rough=0.58, spec=0.30, nscale=110.0)
    # bay 1: the dark band, stopped at x 0.620 where gal_upright already
    # occludes the same rows -- running it on would double-count the darkness
    A(_gbox("gal_band1", 0.6200, 0.3637, -0.4660, -0.4460, 1.6017, 1.6582,
            r=0.004), m_band1)
    # bay 1: the pale item at the measured bright column, standing on the
    # plancha (top 1.455) and embedded 1 mm into it so no face is coincident
    A(_gbox("gal_pale1", 0.3130, 0.3860, -0.4400, -0.3300, 1.4540, 1.5730,
            r=0.010), m_pale)
    # bay 2: band A, kept forward of x 0.030 so it clears gal_can_u, and band
    # B, whose top at 1.5453 clears gal_rack_lo's underside at 1.5460 by 0.7 mm
    A(_gbox("gal_band2", 0.0300, -0.2500, -0.4500, -0.4320, 1.6501, 1.6944,
            r=0.004), m_band2)
    A(_gbox("gal_band3", 0.1150, -0.2700, -0.4500, -0.4320, 1.4889, 1.5453,
            r=0.004), m_band3)

    # ------------------------------- 7. counter top, show side (EXTERIOR props)
    # MEASURED in ref_side.jpg.  A stainless warmer stands on the counter and
    # occludes the lower right of bay 3: image x 641-698 -> X -0.686..-0.955
    # by aperture 3's own fraction, top at v -0.31 of the band, i.e. Z 1.495.
    # Its BASE is on the model counter at CNT_ZT; the photograph puts the base
    # 54 mm higher.  That was recorded as the counter-height residual (nosing
    # 1.189-1.205 AG measured against 1.240 built).  RESOLVED, and not the way
    # it reads: 40 mm of it is the retired RIDE_DROP scalar used as a frame
    # conversion on a vehicle whose drop has been a line since rev 8, and the
    # remainder is inside the outboard-parallax band -- see the CANTILEVERED
    # COUNTER header.  CNT_ZT is not moving, so the 54 mm stays absorbed here,
    # but it is now absorbed knowingly.  The TOP is matched, because the top is
    # the aperture read depends on and it is fixed against the locked band.
    cy0, cy1 = 0.9200, 1.1200
    A(_gbox("gal_warmer", -0.6860, -0.9550, cy0, cy1, CNT_ZT, 1.4950,
            r=0.014, seg=3), m_steel)
    A(_gcyl("gal_warmer_tap", (-0.8200, cy1, 1.3100), (0, 1, 0), 0.0170,
            0.0420, seg=12), m_steel)
    # the amber squeeze bottle standing on it -- measured Z 1.501-1.561 with a
    # pale cap over the top 18 mm
    A(_gcyl("gal_sqbottle", (-0.8400, 1.0200, 1.4980), (0, 0, 1), 0.0165,
            0.0470, seg=14), m_amber)
    A(_gcyl("gal_sqcap", (-0.8400, 1.0200, 1.5450), (0, 0, 1), 0.0105,
            0.0170, seg=12), m_pale)
    # two stainless caddies aft of it, image x 715-760, tops at v -0.53
    for i, (bx0, bx1) in enumerate(((-1.0420, -1.1550), (-1.1600, -1.2730))):
        A(_gbox(f"gal_caddy{i}", bx0, bx1, cy0 + 0.010, cy1 - 0.010,
                CNT_ZT, 1.4090, r=0.006), m_steel)
        # rev 52, A9: THE X INSET HAD THE WRONG SIGN.  (bx0, bx1) is authored
        # HIGH-then-LOW (-1.0420, -1.1550), so "bx0 + 0.012, bx1 - 0.012"
        # EXPANDED the fill instead of insetting it: measured 24.0 mm longer
        # than the caddy it fills, standing 12 mm proud of BOTH ends.  Its own
        # kill test is in the same block -- the fill's top is 3 mm BELOW the
        # caddy rim, so it was always meant to sit inside.  Inset from the
        # ordered edges so the sign cannot invert again.
        _fx0, _fx1 = min(bx0, bx1) + 0.012, max(bx0, bx1) - 0.012
        A(_gbox(f"gal_caddy_fill{i}", _fx0, _fx1, cy0 + 0.024,
                cy1 - 0.024, 1.3600, 1.4060, r=0.004), m_pale)
    # ref_rear34.jpg: a rank of squeeze bottles with red and yellow caps
    # stands beside the caddies on the tail run of the counter.  Kept forward
    # of x = -2.10: verify row 1 measures overall length across every mesh
    # object except the counter itself and the margin is 17 mm.
    # rev 16: these stand on the counter's TAIL RUN, so they move with the
    # counter (delta = X_TAIL - X_TAIL_OLD), not with the shell stations.
    _dtail = T.X_TAIL - T.X_TAIL_OLD
    for i, (bx, col) in enumerate(((-1.8600 + _dtail, GAL_RED),
                                   (-1.9250 + _dtail, GAL_AMBER),
                                   (-1.9900 + _dtail, GAL_RED),
                                   (-2.0550 + _dtail,
                                    (0.5400, 0.4200, 0.0700)))):
        A(_gcyl(f"gal_bot{i}", (bx, 1.0300, CNT_ZT), (0, 0, 1), 0.0195,
                0.1350, seg=14), m_pale)
        A(_gcyl(f"gal_botcap{i}", (bx, 1.0300, CNT_ZT + 0.1350), (0, 0, 1),
                0.0120, 0.0260, seg=12),
          _gm(f"gal_cap{i}", col, rough=0.36, spec=0.45))
    return obs


# ===================================================== step-7 entry point
def spec4_details(body):
    """Everything SPEC sec.4 asks for that build.py does not already call.

    Returns [(objects, material_key or None), ...].  A None key means the
    objects carry a material built HERE and must not be re-assigned by
    build.py's material loop.
    """
    import t1_shell as S
    out = []
    out.append((louvres(), "paint"))                 # pressed body sheet metal
    out.append((counter_nosing(S.SHOW_SIDE), None))  # brass, own material
    out.append((counter_top(S.SHOW_SIDE), None))     # tan laminate, own mat
    #   ^ empty until t1_mats ships `countertan`; see _counter_tan()
    out.append((filler_flap(), "paint"))
    out.append((bobble_fringe(), "capwhite"))
    # rev 8: the bulbs are LIT in both in-service photographs and read warm.
    # They rendered unlit pearl white for seven revisions.
    out.append((bulb_string(), "bulb"))
    # rev 11: the cards were `capwhite` (0.890, 0.888, 0.872) against a
    # measured (225.5, 199.7, 174.5) at TWICE the pillar's saturation. They
    # carry their own material now -- see _gcard().
    _cards = menu_cards()
    for _c in _cards:
        _c.data.materials.append(_gcard())
    out.append((_cards, None))
    # rev 11: everything visible through the three serving apertures
    out.append((galley_dressing(), None))
    out.append((plate_1963(), "chrome"))             # SPEC sec.4: CHROME
    out.append((roof_vent(body), "paint"))
    out.append((englid_handle(), "chrome"))
    return out


def counter_nosing(side=1):
    """SPEC sec.4: brass edge strip on the counter lip.  CONFIRMED in
    ref_rear34.jpg and ref_side.jpg -- a gold nosing runs the whole outer edge
    of the cream slab, round the rear corner and across the tail.

    DEPTH IS NOW MEASURED, not inferred.  CNT_NOSE_F above: the brass caps
    0.186 +- 0.021 of the slab edge, i.e. 19.9 mm of gold in elevation against
    the 31.2 mm this strip used to show (+1.2 mm down to -30.0 mm).  So the
    strip was 1.6x too DEEP, not too thin, and the standing complaint that it
    "reads thin" is a CONTRAST defect, not a size one: build.py paints the
    whole slab `countercream`, so the gold has cream above it AND cream below
    it, where the photograph has TAN laminate above and cream below and the
    gold reads as a hard bright line between two different tones.  The fix for
    the complaint is counter_top(), not a bigger strip.  Enlarging it to
    "look heavy" would have been a fourth of the section wrong by measurement.

    PROJECTION (7.0 mm) is unchanged and still INFERRED -- ref_side.jpg is an
    elevation and cannot measure a Y offset.  The SECTION is now a roll rather
    than a flat band: stacked over the tail run of ref_rear34.jpg the band's
    saturation climbs monotonically 0.41 -> 0.71 from its top edge to its
    bottom while its value peaks 6 px down and then falls, which is a curved
    section lit from above; a flat face renders one tone under any light.
    That read comes from few clean columns, so the roll is INFERRED with the
    same status the whole section used to carry.
    """
    h = CNT_NOSE_F * (CNT_ZT - CNT_ZB)          # 19.9 mm of gold in elevation
    z0 = 0.0015                                 # crown, just proud of the top
    path = [(x, y, CNT_ZT) for (x, y) in _counter_outer(side)]
    prof = [(0.0000 * side, z0),                # inboard, at the slab face
            (0.0040 * side, z0 - 0.0004),       # roll starts
            (0.0068 * side, z0 - 0.20 * h),     # crown of the roll
            (0.0070 * side, z0 - 0.62 * h),     # face, max projection
            (0.0050 * side, z0 - h),            # bottom of the gold
            (0.0000 * side, z0 - h - 0.0040)]   # drip, back to the slab face
    strip = T.sweep(path, prof, up=(0, 0, 1), name="counter_nosing")
    strip.data.materials.append(_brass())
    FLAT.append(strip)
    VISIBILITY_WATCH.append(strip.name)
    return [strip]


def _counter_tan():
    """resolve the counter top's TAN laminate -- or None if it has not shipped.

    OWNER, shown marked crops and asked directly: "tan top, brass nosing on the
    outer edge, body cream below."  The model paints the whole slab
    `countercream`, so the largest single horizontal plane on the vehicle is
    the wrong colour in every 3/4 hero.  MEASURED in ref_side.jpg between the
    counter-top clutter and the gold band, x_img 690-900: hue 29-37, saturation
    0.33-0.39, value 0.63-0.83, against the sunlit flank cream immediately
    above it at saturation 0.09-0.13, value 0.87-0.95 -- a different SURFACE,
    not the same paint in shade (a shade difference moves value, not hue and
    saturation together by 3-4x).

    The material is deliberately NOT built here.  This is an exterior painted /
    laminated surface and it has to come off t1_mats.build_all() so it inherits
    apply_weather()'s dust, wear and fade field the way `countercream` does; a
    private _gm() copy would put a tenth constant-roughness material on the
    most-looked-at plane in the model, which is the defect STATE.md counts.
    Until t1_mats ships it this returns None and counter_top() emits nothing,
    so the build is byte-for-byte what it is today.  See the cross-file ask.
    """
    m = bpy.data.materials.get("countertan")
    if m:
        return m
    try:
        import t1_mats as _MT
        f = getattr(_MT, "counter_tan", None)
        return f() if callable(f) else None
    except Exception:
        return None


def counter_top(side=1):
    """the counter's TAN top surface, as a face over the cream slab.

    build.py:256 hands the whole counter to A(..., "countercream") and
    MT.assign() clears the object's material slots before appending, so a
    second slot on the slab itself cannot survive.  The top is therefore its
    own object carrying its own material and routed from spec4_details() with
    a None key -- exactly the contract counter_nosing() and galley_dressing()
    already use.

    3 mm slab centred 0.3 mm under CNT_ZT, so its top face lands at
    CNT_ZT + 0.0012, which is 1.2 mm clear of the slab's own top face (no
    coincident geometry) and 0.3 mm under the nosing's crown at +0.0015 (the
    brass still caps the edge, and the tan butts into it).  Its outer edge is
    inboard of the nosing's 7 mm projection at every station, so no tan is
    visible in elevation -- which is what ref_side.jpg shows: tan, gold, cream,
    with no tan below the gold.
    """
    m = _counter_tan()
    if m is None:
        return []
    plan = _counter_outer(side) + list(reversed(_counter_inner(side)))
    ob = T.solid_prism((0.0, 0.0, CNT_ZT - 0.0003),
                       (1, 0, 0), (0, 1, 0), (0, 0, 1),
                       plan, 0.0030, name="counter_top")
    ob.data.materials.append(m)
    FLAT.append(ob)
    VISIBILITY_WATCH.append(ob.name)
    return [ob]


# ###########################################################################
#                          VISIBILITY ASSERTION
#
# Task 4's defect -- two wipers buried 30 mm inside the nose skin, rendering
# as nothing -- passed every guard in the project, because nothing tested
# that a detail could actually be SEEN.  This is that test, measured off the
# built mesh with the real hero camera positions.
#
# Add ONE line to verify.py, in run(), immediately before the
# 'log("  VERIFY: %d fail, %d warn" ...)' line:
#
#     fails += __import__("t1_detail").visibility_fails()
#
# A SECOND one-line change to verify.py is needed as well, for a different
# reason -- row 1 measures overall length across every mesh object, and the
# measured counter tail wrap is a fitting that overhangs the body by design
# (SPEC sec.4).  In _bounds(), widen the skip list:
#
#     if ob.type != 'MESH' or ob.name in ("cyc", "counter", "counter_nosing"):
#
# Without it verify reports 'length 4.490 vs spec 4.290 (+200 mm)'.  With it,
# both guards are 0 fail 0 warn.  See the note on CNT_X1.
#
# THAT SKIP LIST MUST GROW BY ONE MORE NAME when t1_mats ships `countertan`:
#
#     ("cyc", "counter", "counter_nosing", "counter_top")
#
# counter_top() lays the tan laminate over the same plan as the slab, so it
# reaches the same x = -2.423 and the same guard would read it as vehicle
# length.  It is the identical fitting-versus-vehicle question, not a new one.
# Until `countertan` exists counter_top() returns [], nothing is built, and
# verify is unaffected -- so the two changes can land in either order.
# ###########################################################################
HERO_CAMS = ["hero34f", "hero34r", "front34", "low34", "detail_f"]


def _cam_locs():
    try:
        import studio as _ST
        V = _ST.views()
        return [tuple(V[k]["loc"]) for k in HERO_CAMS if k in V]
    except Exception:
        return [(9.30, 6.52, 2.90), (-8.60, 6.90, 3.10), (10.10, -5.00, 2.35),
                (9.00, 6.10, 1.30), (4.90, 2.15, 1.85)]


def _frame_dz():
    """studio's camera positions are in the RENDER frame; the mesh is only in
    that frame once build.py step 8b has run."""
    try:
        import __main__
        return 0.0 if getattr(__main__, "RIDE_DROP_APPLIED", True) \
            else -T.RIDE_DROP
    except Exception:
        return 0.0


def visibility_fails(names=None, shell="T1_body", nsample=28, log=None):
    """Fail any watched detail that NO hero camera can reach.

    The cast runs FROM the camera TOWARD each sample point, and the sample
    counts as seen only when the first thing the ray lands on is the object
    itself.  Casting the other way round -- outward from the detail -- does
    not work: the ray's first hit is then the far wall of the detail's own
    solid, which is not the body shell, so a wiper buried 30 mm inside the
    nose skin scores 100 % visible.  That false pass was measured, on this
    model, before this was turned round.

    Details legitimately hidden from one viewpoint (the off-side louvres from
    a front-left camera) are fine: the test is reachability from AT LEAST ONE
    of the hero cameras.
    """
    fails = []
    dz = _frame_dz()
    cams = [Vector((c[0], c[1], c[2] + dz)) for c in _cam_locs()]
    sc = bpy.context.scene
    dg = bpy.context.evaluated_depsgraph_get()
    for nm in (names if names is not None else VISIBILITY_WATCH):
        ob = bpy.data.objects.get(nm)
        if ob is None or ob.type != 'MESH':
            fails.append(f"visibility: '{nm}' does not exist")
            continue
        vs = [ob.matrix_world @ v.co for v in ob.data.vertices]
        step = max(1, len(vs) // nsample)
        pts = vs[::step][:nsample]
        best, best_cam, blocker = 0, "", {}
        for ci, cam in enumerate(cams):
            seen = 0
            for p in pts:
                d = (p - cam)
                dist = d.length
                d.normalize()
                r = sc.ray_cast(dg, cam, d, distance=dist + 0.010)
                if r[0] and r[4] is ob:
                    seen += 1
                elif r[0] and r[4] is not None:
                    blocker[r[4].name] = blocker.get(r[4].name, 0) + 1
            if seen > best:
                best, best_cam = seen, (HERO_CAMS[ci] if ci < len(HERO_CAMS)
                                        else str(ci))
        if best == 0:
            who = sorted(blocker.items(), key=lambda kv: -kv[1])[:3]
            fails.append(
                f"visibility: '{nm}' is INVISIBLE -- from every hero camera "
                f"({', '.join(HERO_CAMS[:len(cams)])}) the first surface the "
                f"ray lands on is never this object, for all {len(pts)} "
                f"sampled points. Occluders: "
                + ", ".join(f"{k} x{v}" for k, v in who))
        elif log:
            log(f"  visible {nm}: {best}/{len(pts)} via {best_cam}")
    return fails
