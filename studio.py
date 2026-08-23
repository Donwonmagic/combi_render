"""white cyclorama studio, PHYSICAL camera, lighting rig, render driver

rev 7 -- the camera was a pinhole with infinite depth of field and the rig was
six neutral rectangles. Both are loud CGI tells at hero resolution:

  * A pinhole renders the tail as sharp as the near arch. No lens does that.
    The camera now has a real sensor size, a real focal length and a real
    f-number, and focuses on the near front arch. Every view logs its measured
    near/far DoF limits so the depth falloff is a number, not a claim.
  * Six rectangles each draw a short specular blob and the eye reads blobs as
    plastic. One long narrow source draws a CONTINUOUS streak that runs the
    length of the flank and bends where the panel curves -- which is what
    actually says "sheet metal". Still large and soft per SPEC sec.6; it just
    has an aspect ratio now.
  * A render with no lens or film artefacts at all reads as synthetic even when
    everything else is right. Restrained chromatic aberration, vignette, bloom
    on the brightest speculars and fine grain are added in the compositor, in
    the order a real camera imposes them.

Every effect is switchable from the environment so any of it can be A/B'd or
zeroed without editing code. T1_FX=0 disables the whole optics chain.
"""
import bpy, math, os
from mathutils import Vector


def _envf(k, d):
    return float(os.environ.get(k, d))


def _envi(k, d):
    return int(float(os.environ.get(k, d)))


# --------------------------------------------------------------------- clay
def clay_all(rgb=(0.62, 0.62, 0.63)):
    m = bpy.data.materials.get("__clay")
    if not m:
        m = bpy.data.materials.new("__clay")
        m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (*rgb, 1)
        b.inputs["Roughness"].default_value = 0.40
        b.inputs["Specular IOR Level"].default_value = 0.35
    for ob in bpy.data.objects:
        if ob.type == 'MESH':
            ob.data.materials.clear()
            ob.data.materials.append(m)


def cyclorama(size=90.0, **kw):
    """
    Flat shadow-catching ground.  Deliberately NOT a curved cyc wall: a wall
    sits between the subject and any orthographic camera placed outside it,
    which is what blanked the front elevation.  Background comes from the
    compositor (pure white) instead.
    """
    me = bpy.data.meshes.new("cyc")
    h = size / 2
    me.from_pydata([(-h, -h, 0), (h, -h, 0), (h, h, 0), (-h, h, 0)], [],
                   [(0, 1, 2, 3)])
    me.validate()
    ob = bpy.data.objects.new("cyc", me)
    bpy.context.collection.objects.link(ob)
    mat = bpy.data.materials.new("cyc_white")
    mat.use_nodes = True
    b = mat.node_tree.nodes["Principled BSDF"]
    # rev 8: was 0.94 -- near-PTFE. A real studio sweep is 0.70-0.80, and at
    # 0.94 the floor bounced enough NEUTRAL light back up the flank to be the
    # single largest desaturator in the scene. See the saturation experiment in
    # SPEC 10.9.
    b.inputs["Base Color"].default_value = (float(os.environ.get("T1_CYCALB", 0.76)),) * 3 + (1,)
    b.inputs["Roughness"].default_value = 0.68
    b.inputs["Specular IOR Level"].default_value = 0.20
    ob.data.materials.append(mat)
    # rev 12, audit `optics-6` -- logged for four revisions, never applied.
    # MEASURED, not asserted: on a 1400x933 side probe the ground read 255.00
    # at EVERY row from 3 px below the contact patch outward, and with the
    # backdrop forced to linear 1.0 (T1_BGW=1.0) the ground under the tyre read
    # 177.00 against open ground at 177.00 -- identical to two decimal places.
    # The catcher was contributing exactly nothing, so the vehicle floated.
    #
    # A shadow catcher writes its shadow into ALPHA and composite_on_white()
    # then lays the frame over linear 24.87. A real photograph on a real white
    # sweep still has a contact shadow: the sweep is a LIT SURFACE, not a matte.
    # TESTED, and the obvious fix is REFUTED: rendering the sweep as a real lit
    # surface (T1_CATCH=0) does put a shadow under the body -- 175.2 mean /
    # 161.2 min on the row below the contact against 255 -- but it also brings
    # back defect D3 in full. The sweep falls off to a 166 grey with a hard
    # horizon line across the frame, and SPEC 6 locks the backdrop to PURE
    # WHITE. Trading the studio's whole look for a contact shadow is not a fix.
    #
    # So the catcher stays ON and `optics-6` stays OPEN, but it is now open with
    # a number instead of an impression: the previous note said the shadow
    # "dies within 11 mm of the tyre", which implies a shadow that decays. It
    # does not decay -- it is not there at all, alpha is identically zero. The
    # next attempt should look at why the catcher writes no alpha under a
    # vehicle that plainly occludes the rig, NOT at softening or lengthening a
    # shadow that does not exist. T1_CATCH=0 reproduces the A/B in one render.
    #
    # rev 17, and the paragraph above is PARTLY WRONG -- corrected by the matte
    # tap, which is the first thing in this project that could look at the
    # alpha directly (see matte_tap.__doc__ for the full numbers). On a 400x300
    # hero34f the catcher's alpha is NOT identically zero: there is a large
    # soft pool under and to the left of the vehicle reaching alpha 0.4980,
    # 19.1 % of the frame is non-zero more than 4 px clear of the silhouette,
    # and the subject-deleted control puts the same far field at 1/174 of that
    # mean, so it is the vehicle's shadow and not noise. The beauty frame does
    # carry it: 249.31 DN mean where 0 < alpha < 1 against 255.00 where
    # alpha == 0. So the open item is NOT "the catcher writes no alpha"; it is
    # "the catcher's shadow survives the alpha-over at a few code values".
    # The rev-12 measurement is not thereby refuted -- it was a SIDE ORTHO with
    # T1_BGW=1.0 and read rows below the contact patch, where this view also
    # shows the pool at its weakest (mean alpha 0.0038 in the 4-30 px band
    # directly below the silhouette). `optics-6` stays OPEN, with a different
    # symptom.
    ob.is_shadow_catcher = bool(int(os.environ.get("T1_CATCH", "1")))
    return ob


# ----------------------------------------------------------------- lighting
# rev 49 -- W6.  THE OWNER CHOSE "re-light to match your photographs".
#
# WHY THIS IS THE KNOB, AND WHY THE OBVIOUS ONES ARE NOT.
# SPEC 10.9 decomposes the flank as  R_lin = a_R . E + A,  with A = 0.0592 a
# NEUTRAL ADDITIVE term -- 12 % of the red channel.  A is the specular
# reflection of large white sources.  The published G/R is the red normalised
# to the cream IN THE SAME FRAME, so it is EXPOSURE-INVARIANT: scaling every
# light together (T1_KEY) scales a_R.E and A alike and moves it by exactly
# nothing.  Measured, rev 45: T1_W_FADESAT and T1_MOT_AMP are bit-identical.
#
# What DOES move it is the sources' RADIANCE.  Specular return goes with
# radiance (power / area); diffuse return goes with total flux.  So enlarging
# a source while HOLDING ITS POWER keeps the exposure and weakens the veil.
# That is what a photographer does with a bigger box, and it is the one lever
# that is not a lie about the paint.
#
# WHAT IT IS NOT.  It is NOT T1_SPEC.  t1_mats.py:1697 records that rev 8 set
# the paint's Specular IOR Level to 0.21 to fix exactly this and it was
# REVERTED: "Every dielectric paint is F0 ~ 0.04.  Fixing an environment
# problem inside the BSDF cost the panels all their specular structure."  The
# five-arm ablation's dominant arm is that same rejected fix, and three briefs
# have quoted it as though it were available.
#
# AND IT IS NOT THE CYCLORAMA.  Measured rev 49, watched print: T1_CYCALB
# 0.76 -> 0.30 moves the red by 2-5 % against a 51 % gap, and moves the
# BACKGROUND BY 0.000 -- the white is a compositor constant laid under a keyed
# render, not a photograph of the sweep.  LEDGER_rev45's "about half the excess
# is the specular response to the white cyclorama and its 0.76-albedo floor"
# attributes an un-decomposed lever to the smallest of its four causes.
#
# THE COST, STATED: a larger source has a broader, softer specular, so the
# strip's unbroken shoulder streak -- the read that says "curved metal" --
# loses definition.  That is the trade the owner was actually shown.
# T1_SOFTEN=1.0 restores the rev-48 rig exactly.
#
# ============================ W6 IS CLOSED, rev 50 ============================
# *** THE OWNER RULED: KEEP THE STUDIO RIG AS IT SHIPS.  T1_SOFTEN STAYS 1.0. ***
#
# He was shown the two frames side by side at last, with the cost measured on
# those exact frames rather than quoted, and with the trade he had been offered
# three times shown NOT TO EXIST:
#
#   window                       k = 1.0        k = 3.5      cost
#   cream, cab roof              L 154.5        L 111.4      -27.9 %
#   red flank, under the script  L 128.8        L  75.0      -41.7 %
#   red G/R                      0.6322         0.5437       -0.0884
#   backdrop, two 200x140 boxes  255.000        255.000      max|diff| 0.000
#                                100.00 % at 255 in BOTH
#
# (windows stated because rule 8 requires it; these are hero34f, not the side
# ortho probe_rev45_paint reads, so these ABSOLUTE G/R values are NOT comparable
# to the published 0.455 / 0.351 -- only the direction and the size of the move
# are.)
#
# TWO THINGS THE RECORD HAD WRONG AND THIS CLOSES.  First, the brief told him the
# dome "costs 29 % of the brightness".  That is the CREAM.  The RED loses 42 %,
# and that figure appears in neither LEDGER_rev49 nor the rev-50 brief -- he had
# been choosing without it.  Second, three revisions refused lighting changes to
# protect a clean white background that no lighting change can reach: the
# backdrop is a compositor constant and the two arms are BIT-IDENTICAL.
#
# WHAT THIS RULING RETIRES.  The body red's G/R gap against the photographed
# 0.223 +- 0.066 is no longer a DEFECT to be closed -- it is the accepted
# consequence of a chosen lighting genre, and the street photographs are
# dimensional references, not colour targets.  DO NOT re-open it, do not ablate
# T1_SPEC against it, and do not read a G/R shortfall on any surface as a paint
# error.  Anything still to be gained on the paint is in the MATERIAL (its coat
# and roughness constants, which are separately undocumented), not in the rig.
# T1_SOFTEN is KEPT, working and ablatable, because the measurement it supports
# is worth keeping; it just does not ship.
# =============================================================================
SOFTEN = 1.0                              # set from T1_SOFTEN at call time


def _soften():
    return max(1e-3, float(os.environ.get("T1_SOFTEN", SOFTEN)))


def _softbox(name, loc, aim_at, size, power, colour=(1, 1, 1), spread=None,
             soften=False):
    """soften=True opts this source into T1_SOFTEN.

    OPT-IN, NOT OPT-OUT, AND THAT IS DELIBERATE.  `cabin_fill` is a 0.8 m box
    sitting INSIDE the cabin and `fill_galley*` are 0.42 m boxes inside the
    serving bays; studio.py's own note on cabin_fill records that moving it a
    third of a metre made it "spill straight out through the three open serving
    bays, which is exactly the kind of leak that makes a fill light a cheat".
    Scaling those with the rig would reproduce that leak.  Only the six RIG
    sources in lighting() opt in.
    """
    d = bpy.data.lights.new(name, 'AREA')
    d.shape = 'RECTANGLE'
    k = _soften() if soften else 1.0
    # BOTH AXES.  AND THE CAPPED VERSION WAS TRIED FIRST AND MEASURED DEAD.
    #
    # THE SWEEP, WATCHED PRINT, probe_rev45_paint.py, P1 = body red G/R:
    #
    #     both axes   k=1.0  0.455   k=2.5  0.379   k=3.5  0.351   k=5.0  0.322
    #     short axis  k=3.5  0.452   <-- against a base of 0.455.  DEAD.
    #
    # The second row is the one that matters.  Growing only the short axis --
    # 16 x 0.55 m -> 16 x 1.93 m, a 3.5x area, exactly what "use a bigger
    # softbox" means -- moves the red by 0.003.  So the colour gain in the
    # first row is NOT the specular being softened.  It is the sources growing
    # past the subject (at k=3.5 the strip is 56 m long) until the rig stops
    # being directional and becomes an ENVELOPING DIFFUSE DOME.
    #
    # THAT IS THE HONEST DESCRIPTION OF THIS KNOB.  It does not tune the
    # studio; it progressively REPLACES it.  Which is also why it works: an
    # overcast or shaded outdoor light is a dome, and every photograph in the
    # reference set was taken under one.
    #
    # IT ALSO CHANGES EXPOSURE, MEASURED: at k=3.5 the cream falls to 0.706 of
    # base and the red flank to 0.545.  The published G/R is normalised to the
    # cream in the same frame and so is exposure-invariant -- P1's improvement
    # is real -- but the PICTURE changes brightness too, and that is a look
    # decision, not a fidelity one.  Restore it with T1_EXP if wanted.
    #
    # DEFAULT IS 1.0 AND NOTHING SHIPS CHANGED.  P1 = 0.455 at k=1.0
    # reproduces rev 48's rig exactly, watched print.
    d.size, d.size_y = (size[0] * k, size[1] * k)
    d.energy = power                       # HELD -- area up, radiance down
    d.color = colour
    if spread is not None:                     # narrow spread = crisper streak
        d.spread = math.radians(spread)
    o = bpy.data.objects.new(name, d)
    bpy.context.collection.objects.link(o)
    o.location = loc
    v = Vector(aim_at) - Vector(loc)
    o.rotation_euler = v.to_track_quat('-Z', 'Y').to_euler()
    return o


# ===========================================================================
# rev 44 -- THE CABIN FILL.  SPEC 10.105.
#
# WHY IT EXISTS.  SPEC 10.104 built a cab -- two-spoke wheel, fascia,
# instrument, two seats, visors, mirror, lever, pedals -- and the first hero
# rendered after it showed NONE OF IT.  Measured on that frame, the cab
# interior read 10-30 DN against a cream body of ~200: a ratio of 0.05-0.15.
#
# THE TARGET IS MEASURED, NOT CHOSEN.  `ref_nolita_doorshut.jpg`'s cab door
# window, 9x crop, shows the far wall, the seat back, the column and the
# steering wheel's rim plainly.  Its interior mid-tone runs 100-180 DN against
# a cream body band of 230-245 -- a ratio of about 0.50.  We were four to six
# times too dark inside, and a cab you cannot see is a cab that was not worth
# building.
#
# WHY THE RIG DOES NOT DO THIS ON ITS OWN, STATED RATHER THAN PATCHED AROUND.
# In the photograph the cab is lit THROUGH THE FAR SIDE -- the opposite cab
# door's glazing is the brightest thing in that frame.  In the studio the same
# path exists but arrives through two tinted panes and past `galley_backdrop`,
# so it lands an order of magnitude down.  This light stands in for that path.
# It is a PRESENTATION DEVICE and it is declared as one: it is inside the
# cabin, it is invisible to the exterior (a rectangle 0.9 x 0.9 m sitting
# BELOW the roof skin and BEHIND the B-pillar), and `T1_NOCABFILL=1` removes
# it so any exterior measurement can be re-run without it.
#
# IT MUST NOT MOVE THE EXTERIOR.  That is asserted by ablation, not by
# argument: the A/B is one environment variable (SPEC 10.45).
# ===========================================================================
CABFILL_POWER = 13.0                # calibrated -- see SPEC 10.105


def cabin_fill(key=1.0):
    if os.environ.get("T1_NOCABFILL"):
        return []
    p = float(os.environ.get("T1_CABFILL", CABFILL_POWER)) * key
    if p <= 0.0:
        return []
    # x 1.05, not 0.72: at 0.72 the box sits aft of the B-pillar and spills
    # straight out through the three open serving bays, which is exactly the
    # kind of leak that makes a fill light a cheat instead of a stand-in.
    return [_softbox("cabin_fill", (1.05, 0.00, 1.62), (1.62, 0.00, 1.06),
                     (0.80, 0.80), p, colour=(1.00, 0.985, 0.955))]


def lighting(key=1.0):
    """
    One long raking strip carries the image; everything else is support.

    The strip is 16 m long and 0.55 m deep, sitting high on the show side and
    raking down the flank. Its reflection is a single unbroken highlight that
    tracks the body's shoulder line from nose to tail and pinches where the
    panel turns -- the read that says "this is a curved metal surface" rather
    than "this is a shaded polygon". Its spread is narrowed so the streak has
    an edge; a full 180 deg area light washes and the streak dissolves.
    """
    c = Vector((0, 0, 1.0))

    # --- the hero source ------------------------------------------------
    _softbox("strip", (0.85, 8.30, 5.90), (0.00, 0.55, 1.28),
             (16.0, 0.55), 511.5 * key, (1.0, 0.998, 0.992), spread=78,
             soften=True)
    # a second, much shorter and lower strip picks out the counter lip and the
    # louvre block, which the high strip rakes straight over
    _softbox("strip_lo", (1.60, 7.40, 1.95), (-0.80, 0.60, 1.05),
             (7.5, 0.34), 77.5 * key, (1.0, 0.995, 0.985), spread=92,
             soften=True)

    # --- support --------------------------------------------------------
    _softbox("top",   (0.6, 1.2, 8.6), (0, 0, 1.3), (13.0, 8.5), 305.3 * key,
             soften=True)
    _softbox("fillR", (2.4, -9.0, 2.4), (0, 0, 1.1), (9.0, 3.6), 92.4 * key,
             (0.975, 0.985, 1.0), soften=True)
    _softbox("rim",   (-9.2, 3.4, 4.2), c, (5.0, 4.0), 145.2 * key,
             soften=True)
    _softbox("nose",  (10.6, 1.6, 1.5), (1.6, 0.0, 1.05), (3.2, 2.6),
             39.6 * key, soften=True)
    # SPEC r4 sec.6 (old D4): the galley is a closed 2.8 mm box lit only by
    # EXTERIOR sources, so the three serving hatches rendered as flat black
    # holes. This sits just outboard of the show flank and rakes into the bays
    # so the openings read as depth. Small and dim: it must not spill onto the
    # paint or wash the contact shadow.
    # rev 13: `gal_ceiling`, the emissive stand-in for the roof opening, is
    # DELETED -- the rig now lights the galley through the hole that has been
    # real geometry since rev 12.  Measured on a 1400x933 side ortho, matched
    # windows, against the photograph's 154 / 169 / 181 mean and 38.0 / 32.3 /
    # 17.7 sd:
    #     rev 12 (stand-in)  132 / 158 / 172   sd 17.1 / 18.5 / 17.4
    #     rev 13 (real hole) 141 / 164 / 175   sd 27.6 / 21.8 / 26.9
    # Every mean moved toward the photograph and the two FLAT bays gained real
    # internal contrast -- from the physics, not from dressing.  The remaining
    # deficit was a LEVEL, so this is the one constant that retunes; swept 10.2
    # / 15.0 / 21.0 and measured, not guessed:
    #     10.2 -> 141.8 / 164.0 / 175.0
    #     15.0 -> 140.4 / 164.8 / 177.9
    #     21.0 -> 142.8 / 167.2 / 180.8    <- bays 2 and 3 land within 2 DN
    # Bay 1 stays 11 DN low and that is a DISTRIBUTION problem, not a level one:
    # cranking the global further over-lights the other two.  Logged, not
    # cranked.
    #
    # SPILL, measured rather than asserted, because the rev-11 docstring's whole
    # justification for keeping this source small was "it must not spill onto
    # the paint": 15.0 -> 21.0 moves the aft cream 195.83 -> 198.83 (+1.5 %) and
    # the aft red 128.16 -> 131.04 (+2.2 %).  Accepted on SPEC 10.9's finding
    # that the beauty-pass flank value is an OUTCOME of the rig and not a
    # target; the albedo, which is the guarded quantity, does not move at all.
    #
    # rev 15, work-list item 6 -- IT IS PER-BAY NOW, and the sign of the lever
    # is the opposite of what four revisions of "lift the galley" assumed.
    # MEASURED by ablation on a 1248x858 side ortho (211.5 px/m, the scale of
    # ref_side.jpg itself), windows = each bay's own projected aperture inset
    # 8 px, against a light-that-cannot-reach-the-bays null of mean|d| 0.4-0.8:
    #     rig as shipped      sd 24.74 / 19.52 / 22.55
    #                         mean 145.4 / 168.2 / 181.6
    #     fill_galley ABLATED sd 28.09 / 23.66 / 26.04
    #                         mean 136.0 / 158.9 / 170.6
    # Removing the source RAISES the contrast in all three bays by 3.4-4.1 sd.
    # It is a frontal wash at near-normal incidence: it lifts the far wall of
    # the galley without casting anything, so it adds level and subtracts
    # structure.  The photograph (same windows, located on its own aperture
    # edges) wants sd 24.16 in bay 2 at mean 158.0 -- which is where bay 2
    # lands with NO fill at all (23.66 at 158.9), and bay 3 already ran over.
    # So the fix is not more light, it is less light IN ONE BAY, and the source
    # has to be split to do that: one 1.7 m box spanning x -1.20...+0.50 covers
    # all three bays and cannot be aimed.
    #
    # Three boxes, one per bay, riding t1_shell.BAYS so they follow the
    # apertures if those ever move again.  BAY 2'S IS OFF.
    #
    # Splitting the source is necessary but NOT sufficient: three 0.55 m boxes
    # at the old stand-off of 1.48 m from the flank still spill into bay 2 from
    # 0.625 m away and it only reached sd 21.53 (bay 2 mean +4.9 DN over the
    # no-fill floor).  Two further changes, both swept and measured, kill the
    # spill: bring the boxes IN to 0.48 m off the flank (clear of the counter
    # nosing, which is the outermost thing on this side at y = 1.173) and cut
    # the emission SPREAD to 30 deg, which at that stand-off confines the
    # footprint to ~0.68 m -- about one bay.  Spread alone at the old distance
    # is worthless and was tried: it just concentrates the same watts (bay
    # means 198 / 182 / 226).
    # Swept at (y = 1.35, 0.42 m box, spread 30), watts per bay 1/3:
    #     0.25 / 0.29 -> sd 23.62 / 23.44 / 21.84   mean 147.1 / 159.4 / 182.5
    #     0.40 / 0.46 -> sd 22.67 / 23.31 / 20.67   mean 152.2 / 159.7 / 187.2
    #     0.60 / 0.70 -> sd 22.22 / 23.16 / 19.53   mean 157.9 / 160.1 / 192.7
    # against the photograph's 33.69(18.50 man-masked) / 24.16 / 21.36 at mean
    # 147.7 / 158.0 / 178.3.  0.25 / 0.29 is taken: bay 2 goes 19.52 -> 23.44
    # against a target of 24.16 -- 84 % of the gap -- while bay 3 moves 22.55 ->
    # 21.84 TOWARD the photograph rather than further over it, and bay 1's mean
    # lands on 147.1 against 147.7.  Residual spill into bay 2 is +0.5 DN over
    # the no-fill floor, down from +4.9.
    #
    # A/B RE-RUN AT THE END, same tree, same seed, one render each, +/- is the
    # sd over nine +/-3 px window placements:
    #   before (one 1.7 m box, 21 W)  sd 24.72+-0.64 / 19.51+-0.31 / 22.55+-1.13
    #   after  (this)                 sd 23.63+-0.57 / 23.44+-0.22 / 21.85+-0.91
    #   ref_side.jpg                  sd 33.69+-0.99 / 24.16+-0.76 / 21.36+-1.38
    #   means  before 145.4 / 168.2 / 181.5   after 147.1 / 159.4 / 182.5
    #                                         photo 147.7 / 158.0 / 178.3
    # Photograph windows, printed so this is reproducible: each bay's aperture
    # CUT EDGE found by row/column gradient in ref_side.jpg and inset 8 px --
    # bay1 u[332,422] v[330,399], bay2 u[463,554] v[325,393],
    # bay3 u[596,689] v[319,388]; those boxes are 106/107/109 px wide and 85 px
    # tall against the render's own projected apertures at 107.3/107.3/107.4
    # and 85.1, which is the cross-check that the two window sets are the same
    # physical rectangle.  BAY 1 IS NOT A TARGET: a man in a white shirt fills
    # its window in the photograph -- his forearm crosses the full width and
    # the shirt covers the right two thirds -- so 33.69 is him, and the audit's
    # man-masked 18.50 +/- 2.02 is the only usable ceiling there.
    #
    # THE ONE SIDE EFFECT, measured and not hidden: total galley-fill wattage
    # falls 21.0 -> 0.54 W, because a 30 deg 0.42 m box at 0.48 m stand-off is
    # ~30x more efficient per watt INSIDE the bay (7.6 W at the old stand-off
    # and 0.25 W here both put bay 1 at mean 146-147).  The bays get the
    # same light
    # (their means match the photograph better than before); what disappears is
    # the part that was never lighting the galley at all.  On a 900x620 side
    # ortho, model-space patches: the aft cream roof shoulder moves 219.77 ->
    # 219.43 (-0.16 %) and the FORWARD RED FLANK 124.53 -> 117.38 (-5.75 %),
    # whole subject (L < 250, 209 022 px) 139.51 -> 134.51.  So the shipped
    # 21 W source was carrying about 4 % of the show flank's key from 1.5 m
    # away -- it was never the "small and dim" source the docstring above
    # promises, and this restores that promise.  SPEC 10.9 governs: the
    # beauty-pass flank VALUE is an outcome of the rig, not a target, and the
    # guarded quantity -- the red albedo saturation -- is a material property
    # and cannot move with a light.  T1_FILLG_SPR=180 T1_FILLG_Y=2.35
    # T1_FILLG_S=0.55 T1_FILLG1=7.6 T1_FILLG3=8.8 reproduces the wide version.
    try:
        import t1_shell as _S
        _bcx = tuple((b[0] + b[1]) / 2.0 for b in _S.BAYS)
    except Exception:                       # studio.py must stand alone
        _bcx = (0.6720, 0.0470, -0.5980)
    # T1_FILLG is kept as the MASTER, scaled off its old 21.0, so every existing
    # A/B recipe (T1_FILLG=0 ablates the galley fill) still does what it did.
    _gk = _envf("T1_FILLG", 21.0) / 21.0
    _gw = (_envf("T1_FILLG1", 0.25), _envf("T1_FILLG2", 0.0),
           _envf("T1_FILLG3", 0.29))
    _gy = _envf("T1_FILLG_Y", 1.35)         # 0.48 m off the flank
    _gs = _envf("T1_FILLG_S", 0.42)
    _gsp = _envf("T1_FILLG_SPR", 30.0)      # >=180 restores the omni wash
    for _i, _bx in enumerate(_bcx):
        if _gw[_i] * _gk <= 0.0:
            continue
        _softbox("fill_galley%d" % (_i + 1), (_bx, _gy, 1.58), (_bx, 0.0, 1.47),
                 (_gs, _gs), _gw[_i] * _gk * key, (1.0, 0.965, 0.915),
                 spread=(_gsp if 0 < _gsp < 180 else None))

    w = bpy.data.worlds.new("w")
    bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
    # cut from 0.30: a bright white world dumps achromatic fill into every
    # shadow and desaturates the paint (SPEC rev4 sec.3)
    # rev 8: 0.17 -> 0.05. Pure achromatic fill landing on saturated paint.
    w.node_tree.nodes["Background"].inputs[1].default_value = float(
        os.environ.get("T1_WORLD", 0.05))


def playa(key=1.0):
    """Playa del Carmen, as the reference photograph actually measures.

    rev 10.  This rig was rebuilt against measurement and four of its previous
    elements were REMOVED because the photograph refutes them.  The rev-8/9
    docstring described "a low warm sun", "broken palm shadow", "a cool sky
    fill" and a haze band.  None of those are in ref_rear34.jpg:

      * NO SUN.  The brightest ground patches sit only +5 L* over their
        surround with 7.4 px edges -- softer than the softest painted edge in
        the frame is sharp.  And the bright/dark ground split measures
        db* +2.4: the SHADOWS ARE WARMER.  A sun/skylight pair has the
        opposite sign by construction, so there is no sun/skylight pair.
      * NO DAPPLE GOBO, for the same reason.  rev 9 added one to honour a
        docstring; the docstring was wrong.
      * NO SKY.  The world ramp topped out at (0.286, 0.452, 0.720) -- a blue
        sky -- at strength 1.30.  There is no sky in frame; the set is under a
        closed canopy with one lateral opening.
      * NO HAZE.  Aerial perspective measures ZERO: the canopy shadow floor
        holds at Y p5 = 0.014-0.019 across the whole depth range and the
        airlight bound is dY < 0.004.

    What IS there is one large, low, LATERAL source -- a palapa opening -- and
    an absorbing ceiling.  The signature that identifies it: the same red paint
    reads 3.95 : 1 between the flank facing the opening and the tail face 72
    deg away, the palm trunk runs 12.5 : 1 across its own diameter with the
    peak 33 deg off the view ray, and an up-facing cream surface is DARKER than
    a vertical one facing the opening (0.93 : 1) while being brighter than one
    turned away (1.87 : 1).  Only a near-horizontal key under a dark ceiling
    does all three.

    Calibrated against those three numbers before any albedo was touched:
    this rig renders flank:f72 = 4.00 (measured 3.95), roof:f72 = 1.91
    (measured 1.87), and up-facing cream 0.787 (measured 0.772 -- a surface
    that was never fitted to).  SPEC 10.23.
    """
    import math as _m
    # rev 10.  The rig geometry and the RATIOS below were solved against the
    # photograph in scene-linear (flank:f72 4.00 against a measured 3.95).
    # The absolute level is a separate question and it is set by the FILM, not
    # by the photograph: this pipeline runs AgX + Punchy, under which the
    # studio's paper white sits at linear 21.0 to reach display 253 (SPEC 10.8).
    # A rig solved at cream = 0.787 linear therefore lands ~5.6 stops down.
    # T1_KEY_PLAYA carries the whole rig -- key, world and galley fill together
    # -- so the solved ratios are untouched by it.
    # Solved by sweep against the film, 2026-08-10.  The reference's cream
    # bodywork sits at display code ~205, i.e. linear 0.593.  Sweep of the
    # up-facing cream roof, in linear: key 30 -> 0.566, 150 -> 0.865,
    # 600 -> clipped.  35 lands it at 0.593.
    key = key * float(os.environ.get("T1_KEY_PLAYA", 35.0))
    KEY_AZ, KEY_EL, KEY_D = 89.0, 10.0, 9.5
    AZ, EL = _m.radians(KEY_AZ), _m.radians(KEY_EL)

    kd = bpy.data.lights.new("key_playa", 'AREA')
    kd.shape = 'RECTANGLE'
    kd.size, kd.size_y = 8.5, 5.0
    kd.energy = 306.4 * key
    kd.color = (1.0, 0.972, 0.936)
    ko = bpy.data.objects.new("key_playa", kd)
    bpy.context.collection.objects.link(ko)
    ko.location = (KEY_D * _m.cos(EL) * _m.cos(AZ),
                   KEY_D * _m.cos(EL) * _m.sin(AZ),
                   KEY_D * _m.sin(EL) + 1.0)
    ko.rotation_euler = (Vector((0, 0, 1.15)) - Vector(ko.location)) \
        .to_track_quat('-Z', 'Y').to_euler()

    # rev 11: this was `12.5 * key`, and `key` is multiplied by T1_KEY_PLAYA
    # (35.0) six lines above -- so it ran at 437, forty-three times the studio
    # rig's 10.2.  It was calibrated when the galley was a black box with no
    # source of its own.  The galley now carries measured practicals whose
    # output is ABSOLUTE, so a softbox scaling with the environment key drowns
    # them.  Held at the studio value, where the galley is solved to within
    # 2.3 % of the photograph on all three bays.
    _softbox("fill_galley", (-0.35, 2.35, 1.58), (-0.35, 0.0, 1.47),
             (1.7, 0.55), 10.2, (1.0, 0.940, 0.860))

    # --- the absorbing canopy.  It is what makes an up-facing surface darker
    #     than a vertical one facing the opening, which is the measured
    #     signature.  Camera-invisible: it shades, it is never in frame.
    ceil = bpy.data.materials.new("absorb_playa")
    ceil.use_nodes = True
    _cb = ceil.node_tree.nodes["Principled BSDF"]
    _cb.inputs["Base Color"].default_value = (0.115, 0.102, 0.086, 1)
    _cb.inputs["Roughness"].default_value = 0.95
    _cb.inputs["Specular IOR Level"].default_value = 0.02

    def _plate(name, verts, faces):
        me = bpy.data.meshes.new(name)
        me.from_pydata(verts, [], faces)
        me.validate()
        ob = bpy.data.objects.new(name, me)
        bpy.context.collection.objects.link(ob)
        ob.data.materials.append(ceil)
        ob.visible_camera = False
        return ob

    _plate("palapa_roof", [(-15.0, -3.0, 3.55), (-1.20, -3.0, 3.55),
                           (-1.20, 7.20, 3.55), (-15.0, 7.20, 3.55)],
           [(0, 1, 2, 3)])
    _R = 11.56          # the one free parameter, solved against roof:f72
    _plate("canopy",
           [(_m.cos(t) * _R - 2.0, _m.sin(t) * _R + 2.0, 7.5)
            for t in [i * 2 * _m.pi / 48 for i in range(48)]],
           [tuple(range(48))])
    _plate("backwall", [(-34.0, -20.0, 0), (34.0, -20.0, 0),
                        (34.0, -20.0, 7.5), (-34.0, -20.0, 7.5)],
           [(0, 1, 2, 3)])

    # --- a uniform dark ambient, NOT a sky gradient.  Open shade.
    w = bpy.data.worlds.new("w_playa")
    bpy.context.scene.world = w
    w.use_nodes = True
    bgn = w.node_tree.nodes["Background"]
    bgn.inputs[0].default_value = (0.92, 0.95, 1.0, 1)
    # The 0.30 : 306 W ratio was solved in an open test cell.  In the built
    # scene the world is a UNIFORM ambient that also lights 90 m of ground the
    # canopy does not cover, so at the solved ratio the terrace blew out and
    # dragged the whole frame flat and pink.  Swept against the reference's own
    # display codes (cream 152, red 167, foliage 81): key 35 / world 0.25 gives
    # cream 160, red 195, foliage 75.
    bgn.inputs[1].default_value = 0.30 * key * float(
        os.environ.get("T1_WORLD_PLAYA", 0.10))

    # --- the place itself ---------------------------------------------------
    # Procedural vegetation and set dressing, placed by inverting the reference
    # photograph's recovered camera: every mass sits at the (image column,
    # depth) the measurement puts it at.  This is the single biggest gap
    # between the rev-9 hero and the memory -- that render had no vegetation in
    # it at all and read as an empty pale plain.  No lamps, no fog, no gobo,
    # and no bunting: the band across the top of the reference is a continuous
    # flowering mass (55.1 % foliage / 13.4 % crimson heads / 5.5 % cream
    # florets), not papel picado.
    import playa_env
    env = playa_env.build(seed=int(os.environ.get("T1_ENV_SEED", 0)))
    print("  playa_env: %d objects, %d instanced polys, band %s"
          % (env["_objects"], env["_instanced_polygons"],
             env["_band_fractions"]))



def ground_playa(size=90.0):
    """Pale limestone paving instead of the white sweep, and it RECEIVES."""
    me = bpy.data.meshes.new("cyc")
    h = size / 2
    me.from_pydata([(-h, -h, 0), (h, -h, 0), (h, h, 0), (-h, h, 0)], [],
                   [(0, 1, 2, 3)])
    me.validate()
    ob = bpy.data.objects.new("cyc", me)
    bpy.context.collection.objects.link(ob)
    mat = bpy.data.materials.new("paving")
    mat.use_nodes = True
    nt = mat.node_tree
    b = nt.nodes["Principled BSDF"]
    # rev 9: at eye height the ground occupies the whole lower third of the
    # frame, so one noise octave at scale 5.5 read as flat grey mud. Two scales
    # now: a slow one that varies the colour of the paving in patches, and a
    # fast one for the surface itself. Base is warmer -- pale limestone in warm
    # light, not neutral aggregate.
    b.inputs["Roughness"].default_value = 0.84
    b.inputs["Specular IOR Level"].default_value = 0.30
    slow = nt.nodes.new("ShaderNodeTexNoise")
    slow.inputs["Scale"].default_value = 0.55
    slow.inputs["Detail"].default_value = 4.0
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].position = 0.36
    # rev 10: halved.  Measured against ref_rear34.jpg the terrace sits at
    # display 108 against the cream bodywork's 241 -- a ratio of 0.45.  At the
    # rev-9 albedo the render put it at 209/243 = 0.86, i.e. the paving was
    # nearly as bright as the paint.  That is not only wrong in itself: a
    # terrace that bright throws a large bounce up onto the red flank, and the
    # red below the counter came out at display 198 against the reference's
    # 118.  This is limestone in deep open shade, not a lit apron.
    cr.color_ramp.elements[0].color = (0.245, 0.216, 0.176, 1)
    cr.color_ramp.elements[1].position = 0.68
    cr.color_ramp.elements[1].color = (0.367, 0.339, 0.285, 1)
    nt.links.new(slow.outputs["Fac"], cr.inputs[0])
    # rev 9: 90 m of paving meeting the sky at full contrast gives a hard
    # cut-out horizon. Fade the ground into the haze band beyond ~14 m so the
    # join reads as distance rather than as the edge of a plane.
    tc2 = nt.nodes.new("ShaderNodeTexCoord")
    vlen = nt.nodes.new("ShaderNodeVectorMath")
    vlen.operation = 'LENGTH'
    nt.links.new(tc2.outputs["Object"], vlen.inputs[0])
    far = nt.nodes.new("ShaderNodeMapRange")
    far.inputs["From Min"].default_value = 14.0
    far.inputs["From Max"].default_value = 52.0
    far.inputs["To Min"].default_value = 0.0
    # rev 10: was 0.88.  Aerial perspective in the reference measures ZERO --
    # the canopy shadow floor holds at Y p5 = 0.014-0.019 across the whole
    # depth range and the airlight bound is dY < 0.004.  There is nothing for
    # a haze band to reproduce, and beyond ~6 m the frame is now filled with
    # measured vegetation rather than with empty ground.  Left wired at 0 so
    # the node graph still shows what was there.
    far.inputs["To Max"].default_value = 0.00
    nt.links.new(vlen.outputs["Value"], far.inputs["Value"])
    hazemix = nt.nodes.new("ShaderNodeMix")
    hazemix.data_type = 'RGBA'
    hazemix.inputs[7].default_value = (0.930, 0.882, 0.790, 1)   # the haze band
    nt.links.new(far.outputs["Result"], hazemix.inputs[0])
    nt.links.new(cr.outputs["Color"], hazemix.inputs[6])
    nt.links.new(hazemix.outputs[2], b.inputs["Base Color"])
    n = nt.nodes.new("ShaderNodeTexNoise")
    n.inputs["Scale"].default_value = 26.0
    n.inputs["Detail"].default_value = 10.0
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.16
    nt.links.new(n.outputs["Fac"], bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    ob.data.materials.append(mat)
    return ob                               # NOT a shadow catcher: it renders


# ------------------------------------------------------------------- camera
SENSOR_W = 36.0            # full-frame 35 mm, the reference most people read
COC = 0.030                # circle of confusion, mm, for a full-frame sensor


def camera():
    d = bpy.data.cameras.new("cam")
    d.sensor_fit = 'HORIZONTAL'
    d.sensor_width = SENSOR_W
    o = bpy.data.objects.new("cam", d)
    bpy.context.collection.objects.link(o)
    bpy.context.scene.camera = o
    return o


# --------------------------------------------------------------------- rig
# rev 58, F51.  THE ONE DEFINITION OF THE SHOOTING RIG.
#
# Until this revision the four calls that build the rig lived INSIDE
# `build.py`'s `if os.environ.get("T1_PREVIEW"):` block, so the rig was a side
# effect of asking for a preview.  Anything that exec'd build.py to MEASURE got
# a scene with no lights, and the failure is silent: an unlit render is a valid
# PNG, it is cheap, and every automated check passes it.  It produced a BLACK
# BUS delivery frame at 3840x2640 that passed stitch.py (exit 0), the seam
# detector (a clean z = 3.63) and looked like a 2.94x speed win.  Only LOOKING
# at it found it (F52).  It is also the cause of F05, `mottle_measure.py`'s
# dead beauty arm, whose note reads "shader_solve._render() builds no studio
# rig".
#
# Four scripts then DUPLICATED the sequence and a verify_clone row compared
# them so the copies could not rot.  That row was a workaround for the absence
# of this function, and it is replaced by the behavioural rows described in
# `assert_lit` below.
#
# ORDER IS LOAD-BEARING and is the order build.py used: backdrop, then clay
# (which must overwrite materials before the lights are placed against them),
# then the lights, then the cabin fill, then the camera.
def rig(key=1.0, scene="studio", clay=False, log=None):
    """Build the whole shooting rig and return the camera.

    THE SINGLE DEFINITION.  Call this instead of re-typing the sequence; a
    hand-rolled copy is how F51 happened.  `scene` is "studio" (cyclorama +
    lighting) or "playa" (ground_playa + playa).
    """
    if scene == "playa":
        ground_playa()
    else:
        cyclorama()
    if clay:
        clay_all()
    if scene == "playa":
        playa(key)
    else:
        lighting(key)
    # rev 44, SPEC 10.105 -- the cab was built and then rendered invisible.
    cabin_fill(key)
    cam = camera()
    if log:
        log("rig built: %s + lighting + cabin_fill + camera  (key %.2f%s)"
            % ("ground_playa" if scene == "playa" else "cyclorama", key,
               ", CLAY" if clay else ""))
    return cam


def rig_from_env(log=None):
    """`rig()` with the switches build.py has always read from the environment.

    The reads are written out literally rather than folded into a helper:
    `verify_clone.sh` asserts every T1_ switch appears as `os.environ.get(
    "NAME")` in source, and a helper taking the name as a variable hides it
    from that row.  Rev 57b was caught by exactly that (sec.10.8).
    """
    return rig(key=float(os.environ.get("T1_KEY", "1.0")),
               scene=os.environ.get("T1_SCENE", "studio"),
               clay=bool(os.environ.get("T1_CLAY")),
               log=log)


def lit_report(scene=None):
    """What is actually lighting this scene, as numbers.  Reports, never raises.

    Returns (n_lights, total_watts, world_strength).  Emissive MATERIALS are
    deliberately NOT counted: the black-bus frame had a lit bulb string and
    nothing else, so "something is emitting" is exactly the reading that let
    it pass.  This counts the RIG.
    """
    sc = scene or bpy.context.scene
    lights = [o for o in sc.objects if o.type == 'LIGHT']
    watts = sum(getattr(o.data, "energy", 0.0) for o in lights)
    ws = 0.0
    w = sc.world
    if w is not None and w.use_nodes:
        bg = w.node_tree.nodes.get("Background")
        if bg is not None:
            ws = float(bg.inputs[1].default_value)
    return len(lights), watts, ws


def assert_lit(scene=None, why="render"):
    """REFUSE to render a scene with no rig.  This is the guard F51 lacked.

    F51's cost was not that the rig was easy to forget -- it is that forgetting
    it is SILENT.  Factoring `rig()` removes the duplication; this removes the
    silence, which is the half that actually bit.  It is deliberately placed in
    `render_set`, the one choke point every preview render goes through, so a
    future script cannot opt out of it by forgetting to call it.

    WATCHED FAILING (rule 3): `T1_SUB=1 T1_NORIG=1 ... build.py` builds the
    scene, skips the rig and reaches this, and it raises rather than writing a
    black frame.  A guard that has not been watched failing reports nothing.
    """
    n, watts, ws = lit_report(scene)
    if n == 0 and ws <= 0.0:
        raise RuntimeError(
            "REFUSING TO %s AN UNLIT SCENE -- 0 light objects and world "
            "strength %.3f.  The studio rig was never built.  Call "
            "studio.rig() (or rig_from_env()) before rendering; that is F51, "
            "and it shipped a BLACK BUS delivery frame that passed every "
            "other automated check." % (why.upper(), ws))
    return n, watts, ws


def dof_limits(lens_mm, fstop, dist_m):
    """near / far sharp limits and hyperfocal, metres -- reported, not claimed"""
    f = float(lens_mm)
    H = (f * f) / (fstop * COC) + f                       # mm
    s = dist_m * 1000.0
    near = (H * s) / (H + (s - f))
    far = (H * s) / (H - (s - f)) if H > (s - f) else float('inf')
    return near / 1000.0, far / 1000.0, H / 1000.0


def aim(cam, loc, target, lens=None, ortho=None, focus=None, fstop=None):
    cam.location = loc
    v = Vector(target) - Vector(loc)
    cam.rotation_euler = v.to_track_quat('-Z', 'Y').to_euler()
    d = cam.data
    d.sensor_fit = 'HORIZONTAL'
    d.sensor_width = SENSOR_W
    if ortho:
        d.type = 'ORTHO'
        d.ortho_scale = ortho
        d.dof.use_dof = False
        return None
    d.type = 'PERSP'
    d.lens = lens or 85
    fs = _envf("T1_FSTOP", fstop or 0)
    if fs <= 0:
        d.dof.use_dof = False
        return None
    # focus on the near front arch by default -- the nearest thing on the
    # vehicle that the eye checks for sharpness
    fp = Vector(focus if focus is not None else target)
    dist = (fp - Vector(loc)).length
    d.dof.use_dof = True
    d.dof.focus_object = None
    d.dof.focus_distance = dist
    d.dof.aperture_fstop = fs
    d.dof.aperture_blades = 9          # a real iris, so out-of-focus speculars
    d.dof.aperture_rotation = math.radians(11)   # are 9-sided, not perfect discs
    return (dist, fs) + dof_limits(d.lens, fs, dist)


# ------------------------------------------------------------- white backdrop
def bg_white_level(scene):
    """
    Linear value that the ACTIVE view transform maps to display white.

    The compositor works in LINEAR, upstream of the view transform. Laying the
    render over linear 1.0 and then pushing it through AgX gives a 0.69 GREY
    backdrop -- that was defect D3, and the shadow catcher / film_transparent /
    compositor were all innocent. Drive the backdrop to the transform's white
    point instead.
    """
    # rev 8 (audit optics-7): this keyed on view_transform ALONE, but
    # setup_render then selects the look "AgX - Punchy", under which linear 21.0
    # maps to display 253, not 255 -- the "white" studio backdrop was two code
    # values grey and the vehicle sat on a faintly dirty card. Keyed on the
    # (transform, look) pair.
    vt = scene.view_settings.view_transform
    look = getattr(scene.view_settings, "look", "") or ""
    lvl = {'Standard': 1.0, 'Khronos PBR Neutral': 1.0,
           'AgX': 21.0, 'Filmic': 16.0, 'Filmic Log': 16.0}.get(vt, 21.0)
    if vt == 'AgX' and 'Punchy' in look:
        lvl = 24.87
    return float(os.environ.get("T1_BGW", lvl))


# ------------------------------------------------------------------- optics
def _grain_texture():
    t = bpy.data.textures.get("__grain")
    if not t:
        t = bpy.data.textures.new("__grain", type='NOISE')
    return t


def composite_on_white(scene, rgb=None, optics=True):
    """
    Render with alpha, then lay it over pure white -- and impose the artefacts
    a real lens and a real film stock impose, in the order they impose them.

      bloom   BEFORE the white, on the linear render. After the white it would
              bloom a linear-21.0 background and flare the whole frame.
      CA      after, because dispersion is a property of the taking lens and
              applies to the whole projected image including the backdrop.
      vignette / grain last, for the same reason.

    Vignette is deliberately tiny. SPEC sec.6 says the backdrop composites to
    PURE WHITE, and a visible corner falloff contradicts that; the value here
    is set so the extreme corner sits about one code value below white -- felt,
    not seen. T1_VIG=0 removes it entirely.
    """
    if rgb is None:
        w = bg_white_level(scene)
        rgb = (w, w, w)
    scene.use_nodes = True
    nt = scene.node_tree
    nt.nodes.clear()

    rl = nt.nodes.new("CompositorNodeRLayers"); rl.location = (-900, 0)
    src = rl.outputs["Image"]
    x = -650
    log = []

    on = optics and _envi("T1_FX", 1)

    # --- deepen the contact shadow, rev 45, SPEC 10.116 ------------------
    # `optics-6`, open since rev 12: THE VEHICLE FLOATS.
    #
    # MEASURED at rev 45 by probe_rev45_ground, in `hero34f` -- a raised
    # three-quarter, which is the only kind of frame a contact shadow can be
    # read in at all.  The three previous measurements were all taken in a side
    # ORTHO or on a 400x300 matte, where the ground plane is edge-on and there
    # is no contact patch to see:
    #
    #     ground just in front of the camera-side tyres / open ground, built
    #         0.9975      <- 0.25 % darkening.  It floats.
    #     the same ratio, PHOTOGRAPHED, four readings on his own truck
    #         0.3049  ref_playa_34, front wheel
    #         0.7300  ref_playa_34, rear wheel
    #         0.6950  ref_nolita_front34
    #         0.8713  ref_nolita_flank
    #         mean 0.6503, sd 0.2101
    #
    # THE SPREAD IS LARGE AND THE TARGET IS THEREFORE THE WEAK END, NOT THE
    # MEAN.  Different frames, different light, hand-placed boxes.  What the
    # four agree on is a SIGN, not a magnitude (rule 6): every photograph of
    # this vehicle has a substantial contact shadow and the render has none.
    # So this is set to land on 0.871 -- THE WEAKEST PHOTOGRAPHED READING --
    # rather than on 0.650, because moving anything to a mean whose sd is a
    # third of its value is what this project calls laundering.  Watched print
    # at T1_SHADOW=9.0, T1_SHADOW_FLOOR=0.030:
    #     G1 0.9756 -> 0.8729   against ref_nolita_flank's photographed 0.8713
    #     G3 0.9132 -> 0.8406   (the under-body pool, which is what reads as
    #                            "planted"; G1 is the tight contact darkening
    #                            and the two move at very different rates)
    #     G2 254.97 -> 254.45   the backdrop, unmoved
    # Pushed to T1_SHADOW=20 the backdrop finally goes and C3 fires.  It is not
    # pushed there.
    #
    # WHY IT IS DONE HERE AND NOT IN THE RIG.  Rev 12 tested the obvious lever,
    # T1_CATCH=0, and refused it: a real lit sweep does produce a shadow but it
    # brings a HARD HORIZON across the frame, and SPEC sec.6 locks the backdrop
    # to PURE WHITE.  Rev 45 re-ran that A/B with an instrument and REV 12 IS
    # RIGHT -- T1_CATCH=0 buys G1 0.9975 -> 0.6924 and pays with a margin whose
    # row-to-row step goes 0.100 -> 22.123 DN.  Refused again.
    #
    # A gain on the shadow catcher's ALPHA cannot make that trade.  The
    # backdrop is alpha == 0 and 0 ** k == 0 for every k, so it stays exactly
    # white BY CONSTRUCTION, not by tuning; the subject is alpha == 1 and
    # 1 ** k == 1, so it is untouched too.  Only the partial-alpha shadow moves.
    #
    # AND IT MUST RUN BEFORE THE BLOOM.  The first placement was immediately
    # above the AlphaOver, i.e. AFTER the FOG_GLOW -- and C3 caught it: the
    # backdrop's level fell 254.97 -> 250.91 as the gain rose, on a control
    # that reads only the upper margins where nothing but backdrop can be.
    # Bloom spreads a little energy AND a little alpha across the whole frame,
    # so downstream of it the backdrop is no longer alpha == 0, and a power
    # function amplifies tiny alpha enormously (0.001 ** 0.31 = 0.11).  Moved
    # to the raw render layer, where the backdrop's alpha is exactly zero and
    # the "0 ** k == 0" argument above is true rather than nearly true.
    #
    # DECLARED AND ABLATABLE, which is SPEC 10.105's template for a
    # presentation device: T1_SHADOW=1.0 restores the floating arm exactly.
    _sh = _envf("T1_SHADOW", 9.0)
    if on and _sh > 1.0:
        try:
            sep = nt.nodes.new("CompositorNodeSeparateColor")
            sep.location = (x - 200, 260)
            nt.links.new(src, sep.inputs[0])
            # SUBTRACT THE CATCHER'S NOISE FLOOR FIRST, and this is the whole
            # reason the first two attempts leaked onto the backdrop.
            #
            # The "sweep" is not empty space -- it is the cyclorama, a SHADOW
            # CATCHER, and it fills most of the frame.  A catcher's alpha far
            # from the subject is not zero, it is a noise floor of a few
            # thousandths.  A power function amplifies small numbers hardest
            # (0.002 ** 0.31 = 0.13), so ANY gain greys the entire sweep before
            # it meaningfully deepens the contact shadow.  Measured: C3's
            # upper-margin level fell 254.97 -> 250.91 across the sweep, and
            # moving the node upstream of the bloom changed NOTHING, which is
            # what refuted the bloom as the cause.
            #
            # So the floor is removed before the gain and the result clamped:
            #     a' = clamp((a - T1_SHADOW_FLOOR) / (1 - T1_SHADOW_FLOOR))
            #     a'' = a' ** (1 / T1_SHADOW)
            # Below the floor the backdrop goes to EXACTLY zero, which is what
            # the "0 ** k == 0" argument needs to be true rather than nearly
            # true.  The cost is stated rather than hidden: it also erodes the
            # faintest real shadow, so the floor is kept as small as C3 allows.
            _fl = _envf("T1_SHADOW_FLOOR", 0.030)
            sub = nt.nodes.new("CompositorNodeMath"); sub.location = (x - 130, 340)
            sub.operation = 'SUBTRACT'
            nt.links.new(sep.outputs["Alpha"], sub.inputs[0])
            sub.inputs[1].default_value = _fl
            dv = nt.nodes.new("CompositorNodeMath"); dv.location = (x - 130, 200)
            dv.operation = 'DIVIDE'
            dv.use_clamp = True
            nt.links.new(sub.outputs[0], dv.inputs[0])
            dv.inputs[1].default_value = max(1.0 - _fl, 1e-6)
            pw = nt.nodes.new("CompositorNodeMath"); pw.location = (x - 20, 260)
            pw.operation = 'POWER'
            pw.use_clamp = True
            nt.links.new(dv.outputs[0], pw.inputs[0])
            pw.inputs[1].default_value = 1.0 / _sh
            sa = nt.nodes.new("CompositorNodeSetAlpha"); sa.location = (x, 140)
            sa.mode = 'REPLACE_ALPHA'
            nt.links.new(src, sa.inputs["Image"])
            nt.links.new(pw.outputs[0], sa.inputs["Alpha"])
            src = sa.outputs[0]
            log.append("contact shadow: alpha floor %.4f then ** %.4f "
                       "(T1_SHADOW=%.2f)" % (_fl, 1.0 / _sh, _sh))
            x += 250
        except Exception as e:
            log.append("contact shadow SKIPPED (%s)" % e)

    # --- bloom, on the transparent linear render -------------------------
    if on and _envf("T1_BLOOM", 1.0) > 0:
        try:
            gl = nt.nodes.new("CompositorNodeGlare"); gl.location = (x, 120)
            gl.glare_type = 'FOG_GLOW'
            gl.quality = 'MEDIUM'
            thr = _envf("T1_BLOOM_THR", 3.2)      # linear: speculars only
            sz = _envi("T1_BLOOM_SIZE", 7)
            for holder, key, val in ((gl, "threshold", thr), (gl, "size", sz)):
                if hasattr(holder, key):
                    setattr(holder, key, val)
                elif key.capitalize() in [i.name for i in gl.inputs]:
                    gl.inputs[key.capitalize()].default_value = val
            gl.threshold = getattr(gl, "threshold", thr)
            # -1 = untouched, +1 = glare only. Restrained.
            gl.mix = -1.0 + 2.0 * (0.075 * _envf("T1_BLOOM", 1.0))
            nt.links.new(src, gl.inputs[0]); src = gl.outputs[0]
            log.append("bloom thr=%.2f size=%d mix=%.3f" % (thr, sz, gl.mix))
            x += 250
        except Exception as e:
            log.append("bloom SKIPPED (%s)" % e)

    # --- lay over pure white --------------------------------------------
    bg = nt.nodes.new("CompositorNodeRGB"); bg.location = (x - 200, -300)
    bg.outputs[0].default_value = (*rgb, 1)
    over = nt.nodes.new("CompositorNodeAlphaOver"); over.location = (x, -60)
    nt.links.new(bg.outputs[0], over.inputs[1])
    nt.links.new(src, over.inputs[2])
    src = over.outputs[0]
    x += 250

    # --- chromatic aberration -------------------------------------------
    if on and _envf("T1_CA", 1.0) > 0:
        try:
            ld = nt.nodes.new("CompositorNodeLensdist"); ld.location = (x, -60)
            ld.use_projector = False
            ld.use_jitter = False
            ld.use_fit = True
            # socket names moved between versions; address by index and fall
            # back to name, so this never silently no-ops again
            disp = _envf("T1_CA", 1.0) * 0.0045
            try:
                ld.inputs[1].default_value = 0.0        # Distort
                ld.inputs[2].default_value = disp       # Dispersion
            except Exception:
                ld.inputs["Distortion"].default_value = 0.0
                ld.inputs["Dispersion"].default_value = disp
            nt.links.new(src, ld.inputs[0]); src = ld.outputs[0]
            log.append("CA disp=%.4f" % disp)
            x += 250
        except Exception as e:
            log.append("CA SKIPPED (%s)" % e)

    # --- vignette --------------------------------------------------------
    if on and _envf("T1_VIG", 1.0) > 0:
        try:
            em = nt.nodes.new("CompositorNodeEllipseMask")
            em.location = (x - 200, -420)
            em.width, em.height = 1.36, 1.36
            em.x, em.y = 0.5, 0.5
            em.mask_type = 'ADD'
            bl = nt.nodes.new("CompositorNodeBlur"); bl.location = (x, -420)
            bl.filter_type = 'FAST_GAUSS'
            bl.use_relative = True
            bl.factor_x = bl.factor_y = 28.0
            nt.links.new(em.outputs[0], bl.inputs[0])
            # remap the blurred mask into [1-amt, 1] so it only ever darkens
            amt = _envf("T1_VIG", 1.0) * 0.055
            mr = nt.nodes.new("CompositorNodeMapRange"); mr.location = (x, -560)
            mr.inputs[1].default_value = 0.0
            mr.inputs[2].default_value = 1.0
            mr.inputs[3].default_value = 1.0 - amt
            mr.inputs[4].default_value = 1.0
            nt.links.new(bl.outputs[0], mr.inputs[0])
            mx = nt.nodes.new("CompositorNodeMixRGB"); mx.location = (x + 240, -60)
            mx.blend_type = 'MULTIPLY'
            mx.inputs[0].default_value = 1.0
            nt.links.new(src, mx.inputs[1])
            nt.links.new(mr.outputs[0], mx.inputs[2])
            src = mx.outputs[0]
            log.append("vignette %.1f%% at corner" % (amt * 100))
            x += 480
        except Exception as e:
            log.append("vignette SKIPPED (%s)" % e)

    # --- fine grain ------------------------------------------------------
    if on and _envf("T1_GRAIN", 1.0) > 0:
        try:
            tx = nt.nodes.new("CompositorNodeTexture"); tx.location = (x, -380)
            tx.texture = _grain_texture()
            amt = _envf("T1_GRAIN", 1.0) * 0.016
            sub = nt.nodes.new("CompositorNodeMixRGB"); sub.location = (x + 200, -380)
            sub.blend_type = 'SUBTRACT'
            sub.inputs[0].default_value = 1.0
            sub.inputs[1].default_value = (0.5, 0.5, 0.5, 1)
            nt.links.new(tx.outputs["Color"], sub.inputs[2])
            add = nt.nodes.new("CompositorNodeMixRGB"); add.location = (x + 420, -60)
            add.blend_type = 'ADD'
            add.inputs[0].default_value = amt * 2.0
            nt.links.new(src, add.inputs[1])
            nt.links.new(sub.outputs[0], add.inputs[2])
            src = add.outputs[0]
            log.append("grain %.3f" % amt)
            x += 660
        except Exception as e:
            log.append("grain SKIPPED (%s)" % e)

    out = nt.nodes.new("CompositorNodeComposite"); out.location = (x + 240, -60)
    nt.links.new(src, out.inputs[0])
    return log


# -------------------------------------------------------------- the matte
def matte_tap(scene, outdir, log=print):
    """File Output node tapping the render's OWN alpha, written BESIDE the frame.

    THE DEFECT, re-measured here and NOT taken on trust (SPEC 10.30h,
    HANDOFF_rev14): `composite_on_white` ends in an AlphaOver whose background
    is an opaque RGB node, so the alpha that reaches the Composite output is 1
    everywhere.  Confirmed on a 400x300 hero34f through the real compositor,
    16-bit RGBA PNG: alpha min 255, max 255, unique [255], 1 distinct value.
    The file HAS an alpha channel and it carries no information, exactly as
    recorded.  Nothing downstream of the AlphaOver can recover the silhouette,
    so the separation has to be taken UPSTREAM of it -- straight off Render
    Layers `Alpha` -- and written to its own file.

    THE CONTRACT IS post.py'S, not a new one.  Read out of `post._mask`:

        mi = np.asarray(Image.open(o["matte"]).convert("L")).astype(np.float64)
        if mi.shape != srgb.shape[:2]: sys.exit(...)
        return 1.0 - mi / 255.0, "matte %s (white=subject)"

    so the file must be (a) openable by PIL, (b) EXACTLY the frame's HxW, (c)
    read as WHITE = SUBJECT on a 0-255 scale, and (d) linear in coverage,
    because `backdrop_headroom` lerps its scale by that value across the
    anti-aliased silhouette.  Three settings follow from (c) and (d) and each
    one is load-bearing:

      * color_mode 'BW'.  `convert("L")` on an RGBA file takes the LUMA of RGB
        and throws the alpha away, so an RGBA matte would hand post.py the
        beauty image, not the matte.
      * color_depth '8'.  setup_render puts the beauty frame at 16 bit (audit
        optics-16) and that is right for the beauty frame, but PIL reads a
        16-bit GREY png as mode "I" and `convert("L")` then CLIPS at 255
        instead of scaling -- every alpha above 255/65535 would come back as
        subject.  Measured below.
      * color_management OVERRIDE + view transform 'Raw'.  A File Output slot
        otherwise inherits the scene view transform, and this scene runs
        AgX/Punchy, which is a heavy S-curve: alpha 1.0 would be written as
        display ~232 and alpha 0.5 as ~180, so the matte would neither be
        white on the subject nor linear in coverage.  'Raw' is the identity.

    This is a TAP, not a change of output.  The claim to make is that the
    Composite chain is untouched, and BYTE-IDENTITY IS NOT THE TEST THAT SHOWS
    IT, because this pipeline is not bit-reproducible against itself: two
    400x300 hero34f renders with the tap OFF and nothing else changed differ by
    max 40 DN, mean 0.2465 DN, over 12.86 % of pixels (OIDN and adaptive
    sampling).  So two tests are given instead, and the second is the real one:

      * numerically, tap-ON sits INSIDE that null.  off_A vs off_B max 40 /
        mean 0.2465 / 12.86 % ; off_A vs ON max 41 / mean 0.2458 / 12.85 % ;
        off_B vs ON max 41 / mean 0.2438 / 12.82 %.  The tap is not
        distinguishable from re-running the same render.
      * structurally, the subgraph reachable backwards from the Composite node
        -- every node type, every input default, every incoming link -- is
        serialised before and after `matte_tap` and compares EQUAL.  The tap
        adds one leaf hanging off Render Layers and touches nothing else.

    It is opt-in via T1_MATTE=1 regardless, so the shipped path does not even
    gain the node.

    WHAT THE MATTE ACTUALLY MEASURES, 400x300 hero34f, 16 samples, T1_SUB=1,
    and this is the whole point of the item -- the alpha now carries
    information where the beauty PNG's carried one value:

        beauty PNG alpha   min 255  max 255  1 unique value
        matte              min 0.0000  max 1.0000  256 unique values
                           26.00 % of pixels strictly between 0 and 1
                           subject cover (a > 0.5)   26.1475 %
                           backdrop cover (1-a > 0.5) 73.8525 %

    against the heuristic mask on the SAME frame at 69.4150 % backdrop (the
    recorded 67.76 % is the same heuristic on the shipped hero).  The two
    disagree in ONE direction only: 0 px are subject in the matte and backdrop
    in the heuristic, and 5325 px are the reverse.  Vertical orientation is
    checked rather than assumed -- subject IoU against the heuristic is 0.8549
    upright and 0.5542 flipped.

    NEGATIVE CONTROL, because an all-255 matte and a correct matte both
    "exist": the same rig rendered with the subject deleted (cyclorama +
    lighting + camera, no vehicle) gives cover 0.0000 % and mean alpha
    0.000069 against 0.267238 -- a factor of 3900.  Its residual is 1.40 % of
    pixels at 1/255-9/255, Monte-Carlo noise concentrated in the top two rows
    where the 1.5 px reconstruction filter loses support; far from the
    silhouette the subject arm carries 174x the control's mean alpha.

    AND IT REFUTES PART OF THE RECORD.  `cyclorama`'s rev-12 note says the
    shadow catcher's alpha "is not there at all, alpha is identically zero".
    On this view it is not: the matte shows a large soft pool under and to the
    left of the vehicle reaching alpha 0.48, 19.1 % of the frame is non-zero
    more than 4 px clear of the silhouette, and the beauty frame is 249.31 DN
    mean where 0 < alpha < 1 against 255.00 where alpha == 0.  The catcher is
    writing a shadow.  What is true is that the shadow is FAINT -- a few code
    values -- which is a different defect from the one recorded, and it is not
    fixed here.

    WITH T1_BORDER (hero.py's strips): the tap writes a FULL-SIZE matte with
    content only in the rendered band -- measured on a y 0.500-1.000 border at
    400x300, alpha is non-zero only in rows 0-149 -- so the strips' mattes
    stitch under exactly the row-ownership rule hero.py already uses for the
    beauty strips.  hero.py does not do that today and this file cannot make
    it; until it does, the matte for a stripped hero has to come from a
    single-pass render.
    """
    scene.use_nodes = True
    nt = scene.node_tree
    rl = next((n for n in nt.nodes if n.type == 'R_LAYERS'), None)
    if rl is None:                          # e.g. transparent=False, no optics
        rl = nt.nodes.new("CompositorNodeRLayers")
        rl.location = (-900, 0)
    fo = nt.nodes.new("CompositorNodeOutputFile")
    fo.name = fo.label = "__matte_tap"
    fo.location = (rl.location[0] + 250, rl.location[1] - 760)
    fo.base_path = outdir
    f = fo.format
    f.file_format = 'PNG'
    f.color_mode = 'BW'
    f.color_depth = '8'
    f.compression = 15
    f.color_management = 'OVERRIDE'
    f.view_settings.view_transform = 'Raw'
    f.view_settings.look = 'None'
    f.view_settings.exposure = 0.0
    f.view_settings.gamma = 1.0
    nt.links.new(rl.outputs["Alpha"], fo.inputs[0])
    if not scene.render.film_transparent:
        # NOT silently tolerated: with an opaque film the alpha is 1 everywhere
        # and the matte would be a plausible-looking all-white file.
        log("  matte tap: WARNING film_transparent is OFF -- the film alpha is "
            "1 everywhere, so this matte will be blank (all subject)")
    log("  matte tap: RLayers.Alpha -> File Output, PNG/BW/8/Raw, base %s"
        % outdir)
    return fo


def _matte_collect(fo, scene, outdir, stem, log=print):
    """Rename the frame-numbered File Output file to `<stem>_matte.png`.

    A File Output slot always appends the frame number, so the node writes
    `<stem>_matte0001.png`.  post.py takes a literal path, and hero.py's
    documented recipe is `--matte out/<tag>_matte.png`, so the number is taken
    off here.  If the file is not there this RAISES: a missing matte that is
    silently skipped is exactly the failure mode this item exists to fix.
    """
    src = os.path.join(outdir, "%s_matte%04d.png" % (stem, scene.frame_current))
    dst = os.path.join(outdir, "%s_matte.png" % stem)
    if not os.path.exists(src):
        raise RuntimeError("matte tap produced no file at %s" % src)
    os.replace(src, dst)
    log("  matte -> %s" % dst)
    return dst


# ------------------------------------------------------------------- render
def setup_render(res=(1600, 1100), samples=64, transparent=False):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = samples
    sc.cycles.adaptive_threshold = _envf("T1_ADAPT", 0.008)
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    sc.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
    sc.cycles.max_bounces = 12
    sc.cycles.transmission_bounces = 12
    sc.cycles.transparent_max_bounces = 12
    # rev 8 (audit optics-10): the clamps were never touched, so
    # sample_clamp_indirect sat at the factory 10.0 against a paper white of
    # 21-25 -- every reflected highlight was ceilinged about a stop BELOW the
    # backdrop and then blurred. Nothing in frame could read as polished metal.
    # rev 15, work-list item 4 ("the glass, the rig half") -- REFUTED, and the
    # clamps stay at 0.0.  The brief was that the rear pane still renders as a
    # mirror at CV 1.22 against the photograph's 0.24, that 81 % of its
    # brightness is the rig, and that the cause was a near-specular strip, or
    # these two clamps letting one bright sample through.  MEASURED on hero34r
    # at 1560x1080, the pane isolated by the CONVEX HULL OF ITS OWN PROJECTED
    # VERTICES eroded 4 px (13 075 px) -- not by a bounding box, which is what
    # produced the old number: the pane is a tilted rounded rectangle, so its
    # axis-aligned box catches cream bodywork in all four corners and reads
    # CV 0.772 on the very same render that the mask reads 0.214 on.
    # All three rows below at 160 samples, same mask, same seed:
    #     rear pane, tree as it stands          CV 0.222   mean 26.65
    #     same pane re-SMOOTH-shaded (pos ctrl) CV 0.833   mean 27.85, max 196
    #     whole rig ablated (neg ctrl)          mean  7.38 (rig = 72 % of level)
    #     ref_side.jpg cab door glazing, four independently placed windows
    #                                           CV 0.221 / 0.232 / 0.287 / 0.293
    #     render cab door glass, same mask rule CV 0.244
    # The mirror was the SMOOTH SHADING, and build.py's `_FLAT_SHADED` already
    # killed it in rev 14: the positive control reproduces the reported defect
    # at 3.8x the fixed pane on request.  There is nothing left in the rig to
    # fix on the rear pane, and softening or de-rating `strip` to chase it
    # would cost the streak that carries the whole flank for no measured gain.
    # (Separately: with T1_GRAIN=0 the pane reads CV 0.142 and the seed-to-seed
    # null collapses from sd 5.56 to 0.575 -- essentially ALL of the residual
    # spread on a dark pane is the compositor's film grain, which also lifts
    # the pane's displayed mean 16.9 -> 26.7 because AgX is steep down there.
    # Any future CV work on dark glass must state whether grain is on.)
    # STILL OPEN and NOT fixed here: the windscreen reads CV 0.94 on the same
    # mask rule, from a hard-edged pale wedge in its upper outboard corner that
    # survives ablation of every single light (largest single contributor
    # `strip`, mean|d| 6.60 against a null of 4.69-4.84).  It is not compared
    # here because NO reference photograph shows this vehicle's windscreen --
    # judging it against a cab-door number measured on a different pane in a
    # different scene is the comparison this project keeps getting burned by.
    sc.cycles.sample_clamp_direct = 0.0
    sc.cycles.sample_clamp_indirect = 0.0
    sc.cycles.caustics_reflective = True
    sc.cycles.caustics_refractive = False        # no lensing through the glass
    sc.cycles.blur_glossy = 0.2
    sc.render.image_settings.color_depth = '16'  # audit optics-16
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = transparent
    sc.render.use_compositing = True
    sc.render.dither_intensity = 1.0
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.compression = 15
    # a real lens is not a box filter. 1.5 px is close to a photographic MTF
    # and stops the render looking laser-etched at hero resolution.
    # (Cycles owns this in 4.x; RenderSettings.filter_width is BI-era.)
    for holder in (sc.cycles, sc.render):
        if hasattr(holder, "filter_width"):
            holder.filter_width = _envf("T1_FILTER", 1.50)
            break
    vt = os.environ.get("T1_VT", "AgX")
    sc.view_settings.view_transform = vt
    lk = os.environ.get("T1_LOOK", "AgX - Punchy" if vt == 'AgX' else 'None')
    try:
        sc.view_settings.look = lk
    except TypeError:
        sc.view_settings.look = 'None'
    sc.view_settings.exposure = float(os.environ.get("T1_EXP", "0.0"))
    return sc


# ------------------------------------------------------------------ presets
# focus points are on the NEAR FRONT ARCH unless a view has no such thing --
# it is the nearest part of the vehicle and the first place an eye checks.
ARCH_F = (1.30, 0.875, 0.36)
ARCH_F_R = (1.30, -0.875, 0.36)


def _pull_in(loc, tgt, dist, tgt_z=None):
    """`loc` moved along its own axis to `dist` metres from the target.

    The direction is preserved exactly, so a view derived this way keeps the
    parent view's perspective character and differs only in how much of the
    frame the subject fills.
    """
    t = Vector(tgt)
    if tgt_z is not None:
        t = Vector((t.x, t.y, tgt_z))
    d = (Vector(loc) - Vector(tgt)).normalized()
    return tuple(t + d * dist)


def subject_bbox(exclude=("cyc", "pl_", "ground", "playa")):
    """World-space bbox of everything that is the SUBJECT, not the set."""
    lo = [1e9] * 3; hi = [-1e9] * 3
    for ob in bpy.data.objects:
        if ob.type != 'MESH' or ob.name.startswith(exclude):
            continue
        for c in ob.bound_box:
            w = ob.matrix_world @ Vector(c)
            for i in range(3):
                lo[i] = min(lo[i], w[i]); hi[i] = max(hi[i], w[i])
    return lo, hi


def fit_view(direction, lens, aspect, fill=0.92, sensor=36.0, bbox=None):
    """Camera loc/target that CENTRES the subject and fills `fill` of the frame.

    rev 44b, SPEC 10.109.  The rev-44 `hero` view was derived by scaling
    `hero34f`'s offset vector by a ratio read off a render -- and the 3200 px
    delivery frame it produced CLIPPED THE FRONT WHEEL at the bottom row, with
    the subject 74 % of the width and hard against the lower edge.  Scaling a
    distance does not centre anything, and a subject seen from above does not
    project symmetrically about its own centroid: the near wheel is closest to
    the camera and drops furthest down the frame.

    Solved instead.  Both the lateral offset and the distance are iterated on
    the projected corners of the SCENE'S OWN bbox, read live, so re-posing the
    lids or adding a part re-solves the frame instead of quietly clipping it.
    Converges in a handful of passes; 60 are run because they are free.
    """
    import itertools
    lo, hi = bbox if bbox else subject_bbox()
    corners = [Vector(p) for p in itertools.product(*zip(lo, hi))]
    sh = sensor / aspect
    d = Vector(direction).normalized()

    def project(dist, tgt):
        C = tgt + d * dist
        f = (tgt - C).normalized()
        r = f.cross(Vector((0, 0, 1))).normalized()
        u = r.cross(f)
        us, vs = [], []
        for P in corners:
            v = P - C
            z = v.dot(f)
            if z <= 1e-6:
                return None, C, r, u
            us.append(v.dot(r) / z * lens / (sensor / 2))
            vs.append(v.dot(u) / z * lens / (sh / 2))
        return (min(us), max(us), min(vs), max(vs)), C, r, u

    tgt = Vector(((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2))
    dist = max(hi[i] - lo[i] for i in range(3)) * 3.0
    for _ in range(60):
        e, C, r, u = project(dist, tgt)
        if e is None:
            dist *= 1.5; continue
        u0, u1, v0, v1 = e
        # PLUS, not minus: moving the TARGET toward the side the subject is
        # already on swings the camera that way and brings it back to centre.
        # The first draft of this had the sign inverted and the iteration ran
        # off to 2e18 metres in sixty passes -- which is why the loop now
        # carries a divergence guard as well as a fixed count.
        tgt = tgt + r * ((u0 + u1) / 2) * (sensor / 2) / lens * dist \
                  + u * ((v0 + v1) / 2) * (sh / 2) / lens * dist
        e, C, r, u = project(dist, tgt)
        if e is None:
            dist *= 1.5; continue
        m = max(abs(x) for x in e)
        dist *= m / fill
        assert dist < 1.0e4, (
            "fit_view diverged: distance %.3g m. The subject bbox is %r/%r "
            "(SPEC 10.109)." % (dist, lo, hi))
    e, C, r, u = project(dist, tgt)
    assert max(abs(x) for x in e) <= 1.0, (
        "fit_view returned a CLIPPED frame: u %.4f..%.4f v %.4f..%.4f. This "
        "is the defect it exists to prevent (SPEC 10.109)." % e)
    return tuple(C), tuple(tgt), dist, e


def _hero_fit(lens=78.0, fill=0.92):
    """`hero`, solved live against the scene's own bbox (SPEC 10.109)."""
    sc = bpy.context.scene
    aspect = (sc.render.resolution_x / sc.render.resolution_y) if sc else 1.5
    d = Vector((12.35, 8.55, 2.21))
    loc, tgt, dist, e = fit_view(d, lens, aspect, fill=fill)
    return dict(loc=loc, tgt=tgt, lens=lens, focus=ARCH_F, fstop=8.0)


def views(dist=1.0):
    return {
        # 3/4 front-left, the reference-photo angle
        # rev 8: the lids are OPEN, so the subject is ~3.0 m tall, not 1.94.
        # SPEC 10.8 locks the 78 mm lens and f/8, so the frame is opened by
        # moving the camera BACK and raising the target rather than by going
        # wider -- the lens is what carries the perspective character.
        "hero34f":  dict(loc=(12.20, 8.55, 3.55), tgt=(-0.15, 0.00, 1.34),
                         lens=78, focus=ARCH_F, fstop=8.0),
        # rev 44 -- THE DELIVERY FRAME.  `hero34f` is kept bit-identical
        # because every rev-8-to-43 measurement was taken through it, and this
        # is a SECOND view rather than an edit to it.
        #
        # MEASURED on the rev-44 hero: the subject fills 70 % of the frame
        # vertically and 61 % horizontally, floating in white.  The reference
        # the owner set the bar with fills its frame.  Nothing about the
        # vehicle changes here -- the camera moves in along the SAME AXIS, so
        # the perspective character SPEC 10.8's 78 mm lens carries is
        # untouched, and only the distance and the target height move.
        #
        # DERIVED, NOT TYPED: 70 % -> 88 % of frame height is a distance scale
        # of 70/88, applied to hero34f's own offset vector.  The target rises
        # to z 1.55 because the subject is 3.046 m tall with the lids up (the
        # build's own printed bbox) and 1.34 left only 64 mm of headroom.
        "hero":     _hero_fit(),
        # 3/4 rear-left, shows the counter wrap and the louvre block
        "hero34r":  dict(loc=(-11.30, 9.05, 3.80), tgt=(0.10, 0.00, 1.38),
                         lens=76, focus=(-1.50, 0.95, 1.10), fstop=8.0),
        # 3/4 front-right
        "front34":  dict(loc=(13.30, -6.60, 3.10), tgt=(0.25, 0.00, 1.32),
                         lens=76, focus=ARCH_F_R, fstop=8.0),
        "side":     dict(loc=(0.0, 26.0, 1.52), tgt=(0.0, 0.0, 1.52),
                         lens=None, ortho=5.90),
        "front":    dict(loc=(26.0, 0.0, 1.52), tgt=(0.0, 0.0, 1.52),
                         lens=None, ortho=3.55),
        "rear":     dict(loc=(-26.0, 0.0, 1.52), tgt=(0.0, 0.0, 1.52),
                         lens=None, ortho=3.55),
        # nose detail -- longer lens, wider aperture, shallower field
        "detail_f": dict(loc=(4.90, 2.15, 1.85), tgt=(1.95, 0.05, 1.16),
                         lens=100, focus=(2.10, 0.00, 1.14), fstop=6.3),
        "low34":    dict(loc=(11.60, 7.90, 1.55), tgt=(-0.10, 0.0, 1.30),
                         lens=78, focus=ARCH_F, fstop=8.0),
        "topdown":  dict(loc=(2.60, 4.60, 6.40), tgt=(-0.30, 0.0, 1.20),
                         lens=62, focus=(0.60, 0.60, 1.60), fstop=11.0),
        # rev 8b: standing AT the counter, eye height. This is the shot that
        # carries the place rather than the specification -- a person's view,
        # looking slightly up at the mural board with the counter lip in the
        # near field. Wider aperture than the studio heroes: at f/3.5 the tail
        # and the background go soft the way an eye does.
        "playa":    dict(loc=(3.15, 5.75, 1.60), tgt=(-0.30, 0.45, 1.40),
                         lens=42, focus=(0.10, 1.05, 1.30), fstop=3.5),
        # rev 10.  The reference photograph's own camera, recovered from the
        # rear rim flange (139.1 px conic fit = 0.440 m -> 316 px/m), the
        # horizon row (230 +/- 30) and the wheel-ellipse axis ratio: it sits at
        # (-4.83, +2.22, 1.90) -- level with the bus's roof line -- with a
        # 53.1 deg horizontal field, i.e. a 36 mm lens.  Confirmed by a feature
        # the solve never saw: it predicts the bus's far top corner at image
        # column 554.6 and the cream lid panel is read at 555.
        #
        # This is the frame Donald wants the owner to remember standing in.
        # Everything playa_env places is placed by inverting THIS camera, so it
        # is also the one view where every plant is exactly where it was
        # measured to be.
        "playa_ref": dict(loc=(-4.829, 2.222, 1.900), tgt=(-0.55, -0.10, 1.28),
                          lens=36, focus=(-1.20, 0.55, 1.20), fstop=4.5),
        "playa_w":  dict(loc=(6.40, 6.90, 1.70), tgt=(-0.30, 0.20, 1.42),
                         lens=50, focus=(0.90, 0.95, 1.25), fstop=4.5),
        # serving counter three-quarter, close -- the shot that says taqueria
        "counter":  dict(loc=(3.40, 5.20, 1.98), tgt=(-0.55, 0.75, 1.26),
                         lens=90, focus=(0.20, 1.05, 1.22), fstop=6.3),
    }


def _cull_foreground(loc, tgt, margin=2.20, log=print):
    """Hide environment geometry that stands between the camera and the vehicle.

    playa_env places its masses by inverting the REFERENCE photograph's camera,
    which is the right thing to do -- every plant is at the depth and bearing
    the measurement puts it at.  But the hero cameras are not the reference
    camera, and a plant that is correctly 6 m behind the vehicle from one
    bearing is correctly in front of it from another.  The rev-10 probe from
    `playa_w` was a wall of fronds with the bus behind it.

    So this hides from the LENS ONLY (visible_camera) anything named pl_* whose
    origin lies closer to the camera than the vehicle's near side.  It still
    shades, still casts, still bounces light -- the scene is unchanged
    radiometrically, and only the occluders are taken out of the shot.  That is
    a framing decision, not a lighting one.
    """
    import mathutils
    C = mathutils.Vector(loc)
    T = mathutils.Vector(tgt)
    fwd = (T - C)
    L = fwd.length
    if L < 1e-6:
        return
    fwd = fwd / L
    hid = 0
    for ob in bpy.data.objects:
        if ob.type != 'MESH' or not ob.name.startswith("pl_"):
            continue
        was = ob.visible_camera
        rel = ob.matrix_world.translation - C
        t = rel.dot(fwd)                       # depth along the view ray
        perp = (rel - fwd * t).length          # lateral offset from the ray
        # in front of the vehicle, and close enough to the axis to occlude it
        front = (t < L - margin) and (perp < max(3.0, 0.55 * t))
        ob.visible_camera = not front
        if front and was:
            hid += 1
    if hid:
        log("  culled %d pl_* objects from the lens (they still shade)" % hid)


def render_set(names, outdir, prefix="r", res=(1600, 1100), samples=64,
               transparent=True, log=print, matte=None):
    sc = setup_render(res, samples, transparent)
    # rev 58, F51: the choke point every preview render goes through.  An
    # unlit scene is a valid, cheap, silently-wrong PNG; refuse it here rather
    # than let a later reader discover it by looking.  T1_NORIG=1 is the
    # ablation that watches this fail.
    _nl, _w, _ws = assert_lit(sc, why="render")
    log("rig: %d light(s), %.0f W total, world %.3f" % (_nl, _w, _ws))
    fx = []
    if transparent:
        fx = composite_on_white(sc)
    # OPT-IN. build.py is the only entry point and it does not pass kwargs, so
    # the flag has to be an environment variable like every other switch here.
    # Default OFF, so the shipped path is untouched -- see matte_tap.__doc__.
    mt = None
    if matte if matte is not None else _envi("T1_MATTE", 0):
        mt = matte_tap(sc, outdir, log=log)
    cam = bpy.context.scene.camera or camera()
    V = views()
    os.makedirs(outdir, exist_ok=True)
    log("optics: %s" % ("; ".join(fx) if fx else "NONE"))
    log("film: filter_width=%.2f px  samples=%d  adaptive=%.4f"
        % (getattr(sc.cycles, "filter_width", 0.0), sc.cycles.samples,
           sc.cycles.adaptive_threshold))
    # Strip rendering. The sandbox reaps background processes, so a 20-minute
    # hero cannot run to completion in one go; T1_BORDER="lo,hi" renders a
    # horizontal band of the SAME full-size frame (crop_to_border stays off so
    # the framing is identical in every strip) and the bands are stitched
    # afterwards. Optics are applied to the stitched image in post.py, never
    # per strip, or bloom and vignette would band at the seams.
    bd = os.environ.get("T1_BORDER")
    if bd:
        y0, y1 = (float(t) for t in bd.split(","))
        sc.render.use_border = True
        sc.render.use_crop_to_border = False
        sc.render.border_min_x, sc.render.border_max_x = 0.0, 1.0
        sc.render.border_min_y, sc.render.border_max_y = y0, y1
        log("border render: y %.3f-%.3f of the full %dx%d frame"
            % (y0, y1, res[0], res[1]))
    else:
        sc.render.use_border = False

    for n in names:
        v = V[n]
        d = aim(cam, v["loc"], v["tgt"], v.get("lens"), v.get("ortho"),
                v.get("focus"), v.get("fstop"))
        _cull_foreground(v["loc"], v["tgt"], log=log)
        if d:
            dist, fs, near, far, H = d
            log("cam %-9s %.0f mm  f/%.1f  focus %.2f m  "
                "sharp %.2f-%s m  (hyperfocal %.1f m)"
                % (n, cam.data.lens, fs, dist, near,
                   "inf" if far == float('inf') else "%.2f" % far, H))
        else:
            log("cam %-9s ortho %.3f  (no DoF)" % (n, v.get("ortho") or 0))
        sc.render.resolution_x, sc.render.resolution_y = res
        sc.render.filepath = os.path.join(outdir, f"{prefix}_{n}.png")
        if mt:
            mt.file_slots[0].path = f"{prefix}_{n}_matte"
        bpy.ops.render.render(write_still=True)
        log(f"rendered {n} -> {sc.render.filepath}")
        if mt:
            _matte_collect(mt, sc, outdir, f"{prefix}_{n}", log=log)
