"""PBR materials.  Body two-tone + livery is driven by object-space position
so no UV unwrap of the shell is needed.

SPEC rev6 sec.3 locks the finish as WEATHERED -- chalky, sun-faded, uneven,
chipped edges, dusty lower body.  Every exterior material therefore runs its
Base Color / Roughness / Normal through the shared WEATHER node group below.

"nothing on this vehicle carries a constant roughness" stood here for four
revisions and was PROSE, not a guard: `audit.py` counts the offenders off the
live mesh and STATE.md put the count at 9 the day this line was written.  The
count is a measurement and this file does not get to assert it -- see
`rough_field()` and the adjudication at the foot of `build_all()`, which
leaves exactly the transmissive four, the sealed reflector, and the roof
aperture stand-in, each argued by name.

NO SUBSURFACE ANYWHERE.  Every material sits at Subsurface Weight 0.0 and
verify.py asserts it.

MEASURED RESULT (2026-08-09, /sessions/.../tmp/rms_metric.py, side ortho
500x340 @ 9.90 mm/px, 16 samples, plain cream tiles on the rear-corner panel,
noise-corrected texture residual sd(L - boxblur)/mean at matched physical
scale):

                                   25 mm   100 mm   400 mm
  ref_side.jpg, patch as specified  3.37 %   7.03 %  10.54 %
  ref_side.jpg, flat part only      1.06 %   3.63 %   4.78 %
  ref_side.jpg, flat + detrended    1.00 %   3.42 %   3.97 %
  build BEFORE this change          0.22 %   0.24 %   0.33 %
  build AFTER  this change          0.37 %   0.81 %   1.42 %

Two things stop the display-referred figure reaching the design target, both
measured, neither fixable in a shader:

 1. 55 % of the 400 mm target is the tail curving out of the light.  The
    reference patch is 45 px wide and its last 7 columns run 235 -> 182 code
    values down the rear corner.  Dropping them takes the target from 10.54 %
    to 4.78 %.

 2. AgX + "AgX - Punchy" is nearly flat where the cream sits.  Measured by
    exposure derivative on this scene (T1_EXP -0.25 / 0 / +0.25):
    d(code)/dEV = 16.60 at cream mean 224.9, i.e. a local gain of 0.106
    display-fraction per unit scene-linear fraction.  On the red lower body,
    two stops darker, the same measurement gives 0.309.  A gamma-2.4 camera
    response would be ~0.42 before its own highlight shoulder.  So the cream
    panel throws away ~90 % of any albedo modulation before it reaches a code
    value, and the same shader reads three times stronger on the red.

Working back through the measured gain, the 1.42 % display residual here is
13.4 % albedo sd in linear reflectance.  The reference's flat + detrended
3.97 % corresponds to 11-16 % albedo sd for a camera highlight gain of
0.25-0.35.  In linear reflectance the paint now carries the same texture
amplitude as the real vehicle; it is the view transform that hides it.
"""
import bpy, math, os
import t1_core as T          # rev 8: the rake coefficient has one home

TEXDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tex")

# SPEC r4 sec.3: measured (196,106,36) sRGB in sun -> faded orange-red /
# vermillion, hue ~26deg. NOT a deep crimson.
# rev 9: sRGB(196,49,36). See the note below and SPEC 10.12 -- the previous
# value's hue came off the retired 246x197 thumbnail and matches the reference
# GOLD folk-art hue to 2.9%, which is what contamination looks like on a
# thumbnail where the flank is ~100 px wide. Saturation is UNCHANGED at 0.816:
# SPEC 10.9 settled that and this does not re-open it. Revert with
# T1_RED=196,106,36.
RED = (0.5520, 0.0294, 0.0176)   # = sRGB(196,49,36), hue 5.0, sat 0.816
_RED_THUMB = (0.5520, 0.1441, 0.0176)   # sRGB(196,106,36), hue 26.2 (retired)
                                 # rev-3 shipped (0.5250,0.0395,0.0072) =
                                 # sRGB(192,56,20), hue 12.5 sat 0.894 -- a
                                 # DEEP CRIMSON, which SPEC 0.2 retires by
                                 # name. Its green channel was 3.6x low.


def _srgb_to_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


# rev 9: T1_RED="r,g,b" (sRGB 0-255) overrides the flank albedo, so the hue
# question below can be A/B'd without editing a locked constant.
#
# The locked (196,106,36) comes from the retired 246x197 thumbnail. Measured on
# ref_side.jpg instead, the red flank reads hue 4.0-4.3 deg in its least-lit
# patches and 19-23 deg where warm bounce is strong. The hue-invariant ratio
# (G-B)/(R-B) -- which any NEUTRAL additive term leaves unchanged, so SPEC
# 10.9's specular pedestal cannot move it -- is 0.067 in deep shade against
# 0.438 for the locked value. And 0.438 matches the reference GOLD folk-art
# motif's 0.450 to 2.9%: on a thumbnail where the flank is ~100 px wide and
# the gold covers much of it, that is what contamination looks like.
# Nothing is changed by default. See SPEC 10.12.
if os.environ.get("T1_RED"):
    RED = tuple(_srgb_to_lin(float(v))
                for v in os.environ["T1_RED"].split(","))
# measured (206,208,200) sRGB -> sun-bleached near-neutral off-white
CREAM = (0.6172, 0.6308, 0.5776) # = sRGB(206,208,200). rev-3 had R > G;
                                 # the measurement has G > R, and rev-3 was
                                 # 24 code values bright.
GOLD = (0.8600, 0.5400, 0.0600)

# two-tone break line:  belt line on the flanks, V-swage across the nose
#
# FRAME NOTE (measured 2026-08-09, not assumed).  build.py step 8b subtracts
# T.RIDE_DROP from every vertex AFTER the materials are assigned, but a shader
# reads Geometry->Position at RENDER time, i.e. from the already-dropped mesh.
# The shader therefore sees the DROPPED frame, and Position.Z is the true
# height above the ground plane (the cyclorama sits at z = 0 and the tyres
# bottom out at z = 0.010 +- one 9.9 mm pixel).
# Verified empirically: in the side ortho probe the painted cream/red break on
# the rear quarter (clear of the counter, tblend = 0 so the mix is pure Z_BELT)
# lands between pixel rows 128 and 130 with row 129 the mixed pixel; row 129 is
# z = 1.3859 against Z_BELT = 1.3860.  A shader reading the UN-dropped frame
# would have put it on row 135.6.  So height ramps below are written in
# TRUE ABOVE-GROUND METRES with NO ride-drop offset added.
# CORRECTED 2026-08-09, re-derived off the high-resolution photographs.
# All four are ABOVE-GROUND metres (see the frame note above).  The pressed
# swage in t1_shell.nose_shape.zV() carries the same three numbers + 0.065,
# because THAT is geometry and is cut before the drop.  If you change one,
# change the other in the same commit or the swage and the paint de-register.
# V_APEX <= 0.396 above ground is a HARD BOUND, not an estimate: the cream
# wedge is still 14 px wide where the bumper occludes it in ref_workshop.jpg
# and the bumper top measures 0.331 +- 0.020 above ground.  That bound is
# independent of any px/m conversion.  V_POW < 1 -- the profile is CONCAVE.
# rev 8: THE BELT IS A LINE, NOT A CONSTANT.
# Step 8b no longer subtracts a scalar -- it shears, because the vehicle sits
# nose-down ~1.9 deg (t1_core.rake_drop). A shader reading Position.Z off the
# sheared mesh therefore sees a break whose height FALLS as x rises:
#
#     break_z(x) = Z_BELT0 - RAKE_DZDX * x            (above ground)
#
# Z_BELT0 / V_APEX0 are the above-ground values AT x = 0, i.e.
# authored - RAKE_Z0, where the old constants were authored - RIDE_DROP. The
# rake term is subtracted once, AFTER the flank/nose mix, so it applies equally
# to both branches and V_APEX0 + V_RISE == Z_BELT0 keeps holding at every
# station -- which is what makes the swage arms land on the belt line.
RAKE_DZDX = T.RAKE_DZDX                 # single source of truth
# rev 13, SPEC 10.25.  These were literals with the derivation only in a
# comment -- "= 1.2720 authored - RAKE_Z0 0.0365" -- which is exactly the shape
# that merged the VW glyph into an X twice.  Changing RAKE_Z0 would have left
# the PAINTED break where it was while the PRESSED swage (t1_shell.V_APEX_Z,
# authored) moved with the shear, de-registering two things SPEC 10.2 verifies
# to 0.0 mm.  Now expressed in terms of the constant they are tuned against.
# The authored values are the geometry-frame ones and they do NOT change.
Z_BELT_AUTH = 1.2720                    # un-dropped, geometry frame
V_APEX_AUTH = 0.4050                    # un-dropped == t1_shell.V_APEX_Z
Z_BELT0 = Z_BELT_AUTH - T.RAKE_Z0       # above ground at x = 0
V_APEX0 = V_APEX_AUTH - T.RAKE_Z0       # above ground at x = 0
V_RISE = 0.8670
V_POW = 0.60

# Above-ground value at any station, for probes and reports.
def z_belt(x):
    return Z_BELT0 - RAKE_DZDX * x


def v_apex(x):
    return V_APEX0 - RAKE_DZDX * x


# Back-compat scalars, evaluated at the station where the old uniform drop and
# the rake agree (t1_core.X_DROP_REF). Anything that wants a height at a
# specific x must call z_belt(x)/v_apex(x) -- a bare Z_BELT is now only correct
# at one station.
Z_BELT = z_belt(T.X_DROP_REF)           # == 1.2070, the rev-7 value
V_APEX = v_apex(T.X_DROP_REF)           # == 0.3400

assert abs((V_APEX0 + V_RISE) - Z_BELT0) < 1e-9, (
    "V_APEX0 + V_RISE must equal Z_BELT0: the V-swage arms have to land on the "
    "flank belt line at |y| = 0.86, at every station")
assert abs((V_APEX + V_RISE) - Z_BELT) < 1e-9
# The bumper-occlusion bound is a statement about the NOSE, so it is tested at
# the nose station, not at x = 0.
assert v_apex(2.108) <= 0.3960, "V_APEX at the nose above the bumper-occlusion bound"

# ---------------------------------------------------------------- WEATHER
# Tunables for the shared weathering field.  W_ALBEDO is the one that is
# actually measured against the reference: see the residual table in the
# handover.  Roughness modulation alone is nearly invisible at Specular IOR
# Level 0.21 / Roughness 0.42 because the body is diffuse-dominated.
# rev 15, work-list item 2.  These four were fixed literals; they are now
# overridable because a NEGATIVE CONTROL showed the amplitude lever is inert at
# 25 mm and the SCALE/persistence levers are the live ones.  See SPEC 10.31.
W_N1_SCALE = float(os.environ.get("T1_W_N1SC", 3.5))
W_N1_DETAIL = float(os.environ.get("T1_W_N1DT", 6.0))
W_N1_ROUGH = float(os.environ.get("T1_W_N1RG", 0.55))
W_N2_SCALE = float(os.environ.get("T1_W_N2SC", 22.0))
W_N2_DETAIL = float(os.environ.get("T1_W_N2DT", 4.0))
W_N1_W, W_N2_W = 0.65, 0.35
W_ROUGH_SWING = 0.09           # +- about the material's base roughness
W_ALBEDO = float(os.environ.get("T1_W_ALB", 0.260))
# rev 14, SPEC 10.29: the flank cream is too CLEAN, not too weathered. The
# rendered local luminance variation is 1.24 % RMS at 25 mm against SPEC
# 10.4's 4.22 % target and a direct re-measure of ref_side.jpg at 7.37 % --
# 3.4-6x too uniform. The owner's "weathering looks too heavy" impression was
# measured and REFUTED for the flank; it was the cab ROOF, a different node.
# 0.130 -> 0.260 is the first step of that solve and it is NOT the solve: the
# relationship is not linear (this file's own calibration below records 0.06
# realising 1.2 % albedo sd and 0.13 % display residual, while 0.130 realises
# 1.24 % display -- so most of the shipped 1.24 % is coming from somewhere
# other than this node). Measured after the change and reported; the residual
# is left open rather than tuned to a number nobody watched print.
# The other lever is the MAP WINDOW, exposed below: the noise Fac is
# approximately N(0.5, s) and a 0.30-0.70 window passes most of the
# distribution, so only ~20 % of the half-range is realised. Move ONE of the
# two at a time.
                               # +- albedo half-range over the 0.30-0.70 map
                               # window.  The design entered 0.06; measured,
                               # that realises only 1.2 % albedo sd and 0.13 %
                               # display residual (see the report).  0.70
                               # realises 14.2 % albedo sd.
_NOSE_SEL = [None]          # rev 11: nose-decal selector handoff
W_MAP_LO = float(os.environ.get("T1_W_MAPLO", 0.30))
W_MAP_HI = float(os.environ.get("T1_W_MAPHI", 0.70))
# rev 10.  This was 0.30 -- a 30 % opacity ceiling on hand-painted signwriting,
# put there in rev 8 to stop the folk art dragging the flank saturation down.
# It is the arithmetic cause of Donald's "far too faint and sparse": measured
# through the shader the gold read x1.455 against the adjacent red where the
# photograph reads x2.048, and at 0.30 even a PURE WHITE ink only reaches
# x2.15, so the measured contrast was unreachable by construction. The tile is
# now authored at measured coverage (29.1 % on the cab door, not the 0.0-0.2 %
# a scan of the OPEN door produced) and measured colour, so the ceiling has
# nothing left to protect against. SPEC 10.21.
W_ART = float(os.environ.get("T1_W_ART", 1.00))   # folk-art opacity ceiling

# curvature edge wear.  Pointiness RE-MEASURED off the built mesh 2026-08-09
# by rendering Geometry->Pointiness to a 32-bit EXR through the side ortho,
# at BOTH subdivision levels (mean / p95 / max over the sampled window):
#                          T1_SUB=1                T1_SUB=2
#   flat flank        0.5002 / .5004 / .5005   0.5001 / .5003 / .5005
#   front arch lip    0.5326 / .5926 / .6084   0.5324 / .5926 / .6084
#   rear arch lip     0.5031 / .5096 / .5099        (never reaches 0.52)
#   bumper front      0.5101 / .5463 / .5950   0.5085 / .5463 / .5950
#   counter lip       0.5794 / .6150 / .6690   0.5764 / .6150 / .6690
#   above 0.520          27.9 % of frame          24.2 % of frame
#   above 0.600           3.99 %                   3.94 %
# The design's figures (flank 0.503, arch lip 0.552, bumper crown 0.571, drip
# rail 0.591, counter lip 0.617) are close for the bumper and the counter, but
# the flank is 0.500 not 0.503 and the REAR arch lip never crosses 0.520 at
# all, so it gets no chips.  SUB=1 and SUB=2 agree to <0.003 everywhere --
# pointiness here is NOT mesh-density sensitive, because the subsurf runs
# before solidify and the arches / bumper / counter are unsubdivided detail
# geometry.  The 0.520 / 0.600 window is kept: it clears the flank by 20 sigma.
W_PT_LO, W_PT_HI = 0.520, 0.600
W_CHIP_SCALE, W_CHIP_DETAIL = 60.0, 3.0
W_CHIP_LO, W_CHIP_HI = 0.42, 0.58
W_CHIP_CUT = 0.35
# Pointiness is a PER-VERTEX quantity. On the subdivided shell it does what
# the design assumes, but on unsubdivided detail geometry every vertex is a
# corner, so the ramp saturates over the whole face: measured, the counter
# slab reads pw = 1.0 across its entire top (55 % of the top-down frame at
# pw > 0.5), which turned Wear 0.7 into 29 % chip coverage on a flat slab
# instead of a chipped lip. A second, low-frequency cluster gate breaks the
# chipping into runs -- which is also what the design asks for ("not a uniform
# pen line") -- and brings the slab back to a believable coverage without
# touching the per-material Wear weights.
W_CLUST_SCALE, W_CLUST_DETAIL = 7.0, 2.0
W_CLUST_LO, W_CLUST_HI = 0.44, 0.60
W_PRIMER = (0.1290, 0.1070, 0.0920)     # linear oxide grey
W_STEEL = (0.5600, 0.5620, 0.5680)      # bare steel
W_STEEL_LO, W_STEEL_HI = 0.80, 1.00     # deepest ~20 % of the wear ramp
W_STEEL_ROUGH = 0.55
# The pointiness histogram on this mesh is BIMODAL -- 49 % of the visible
# surface sits at 0.500-0.505 (flat panel) and the edges jump straight to
# 0.58-0.61.  "the deepest 20 % of the ramp" therefore selects ~100 % of the
# chips, not 20 % of them: measured 4.20 % steel against 4.42 % primer on the
# lower flank.  A second, finer mask cuts the bare-metal core back to a fifth
# of the chip, which is also what a real chip looks like: primer ring, small
# bright core.
W_CORE_SCALE, W_CORE_DETAIL, W_CORE_CUT = 110.0, 2.0, 0.573

# dust: measured tide line.  In CIELAB C*/(L*+16) on the real vehicle is flat
# to +-7 % from h = 0.40 m to h = 0.92 m and only collapses at 0.36 (-21 %).
# The 35 % luminance fall toward the rocker is ILLUMINATION, not pigment.
# So there is no dust on the flank above 0.48 m at all.
#
# rev 12: W_DUST_Z_LO was 0.220 and that is a RAMP HEIGHT of 0.260 m, which
# SPEC 10.4 does not describe.  Re-measured on ref_side.jpg, in that
# photograph's own frame, by the method SPEC 10.11 requires (a difference
# inside a panel whose ends are locked -- NEVER the ground line):
#
#   datum   the cream/red paint break, traced by the first row where sRGB
#           saturation crosses 0.45 scanning down, 64 columns x = 320..640
#           (clear of the cab door, which B2 shows is swung open, and clear
#           of the tail where the counter occludes the belt).  Least squares
#           y_break = -0.03538 x + 441.873, residual rms 0.53 px.  At the
#           script station that is y 424.4 against SPEC 10.11's independently
#           derived 426.4 -- 2 px, so this is the same line 10.11 used.
#   scale   the rear wheel's cream rim flange, VERTICAL chord through the
#           centre: top 557.5, bottom 650.5, D = 93.0 px on a 16 in flange
#           of 0.440 +- 0.008 m -> 211.4 px/m.  (Reproduces REF_MEASUREMENTS'
#           92.97 px.  The 194.8 px/m quoted at the tail is a HORIZONTAL
#           foreshortening; the vertical scale does not carry it.)
#   height  z(x, y) = z_belt(x) - (y - y_break(x)) / 211.4
#
#   C*/(L*+16) on the red flank, 45 266 px with Lab hue in [30,45) and C* > 20,
#   binned in 10 mm of height:
#       z 0.42 .. 0.84   1.395 .. 1.430      flat to +-1.5 %
#       z 0.86 / 0.90    1.383 / 1.349       -3 % / -5 %   (counter shadow)
#       z 0.429          1.394               -2 %
#       z 0.420          1.275              -10 %
#       z 0.410          1.201              -16 %
#       z 0.401          0.779              -45 %
#   -> leaves the +-7 % band at h = 0.424 +- 0.020, 50 % collapse at
#      h = 0.398 +- 0.020, gone by 0.39.  Below 0.40 the flank is not
#      observable in this photograph at all (the body turns under into its own
#      shadow, L* 19 falling to 3), so the LOWER end of the ramp cannot be
#      measured here and SPEC 10.4's "full <= 0.30" stands as the authority.
#   Uncertainty: +-2 % on the 0.440 m flange over an 0.83 m offset (+-17 mm)
#   plus +-2 px of edge (+-9 mm) -> +-20 mm.
#
# 0.480 -> 0.300 satisfies all three of SPEC 10.4's numbers at once: zero at
# 0.48, full at 0.30, smoothstep knee (50 %) at 0.390 against the measured
# 0.398 +- 0.020 and against 0.40 +- 0.04.  It also makes the ramp 0.180 m
# tall, which is what SPEC 10.4's "the intuitive smoothstep(0.75 -> 0.25) is
# ~3x too tall" MEANS: 0.500 / 0.180 = 2.78.  The old 0.260 m ramp was only
# 1.92x smaller than the intuitive one and put its knee at 0.350, outside the
# 0.40 +- 0.04 window, while never reaching full above 0.220.
# Check on the clean side: with this ramp the deposit reaches 2.9 % at
# z = 0.440, which is where the red's C*/(L*+16) falls 7 % -- against the
# measured 0.424 +- 0.020.  Inside 1 sigma at both ends of the knee.
W_DUST_Z_HI, W_DUST_Z_LO = 0.480, 0.300      # true above-ground metres
W_DUST_RAG_SCALE, W_DUST_RAG_DETAIL, W_DUST_RAG_AMP = 6.0, 2.0, 0.045
W_DUST_NZ_LO, W_DUST_NZ_HI = 0.25, 0.85      # upward-normal ramp
W_DUST_UP_W = 0.85
W_DUST_MOT_SCALE, W_DUST_MOT_DETAIL = 14.0, 4.0
W_DUST_MOT_LO, W_DUST_MOT_HI = 0.35, 0.70
W_DUST_MOT_MIN, W_DUST_MOT_MAX = 0.35, 1.00
# Expectation of the mottle multiplier above.  Blender's noise Fac is ~N(0.5,s)
# and E[motm] = 0.630 +- 0.005 for every s in 0.08..0.15, so the coverage model
# below does not depend on which noise Blender ships.
W_DUST_MOT_MEAN = 0.630
W_DUST_COL = (0.4400, 0.3900, 0.3100)        # pale limestone ROAD FILM
W_DUST_ROUGH = 0.28                          # ADDITIVE, clamped at 0.85
W_ROUGH_CEIL = 0.85

# ---- the two deposits are NOT the same dirt -------------------------------
# rev 12.  There is one colour and one strength ramp in the graph and two
# physically different deposits sharing them: road film thrown up from the
# ground (the tide line) and dust that SETTLES on upward faces.  Splitting
# them is what makes SPEC 10.4's upward-facing row reachable -- with one
# colour it is not, at any coverage.
#
# MEASURED, ref_rear34.jpg, and this is a SAME-CLASS comparison with a KNOWN
# albedo difference removed, not a rendered ratio across classes:
#   patches   counter top (upward, cream paint)   sRGB(202,172,127), n=2160
#             cream flank rear quarter (side)     sRGB(203,186,146), n=2153
#             both middle-80 % of L*, medians
#   The two are different paints, so the raw delta is inadmissible.  Both
#   albedos are LOCKED constants in this file, so the difference between them
#   is known and can be removed: fit a von-Kries gain from the side patch and
#   this file's CREAM, push COUNTERCREAM through the
#   same gain, and the clean counter top would render L* 80.35 C* 23.87
#   h 85.73.  Against the observed dirty L* 71.96 C* 27.58 h 80.53 that is
#       dL* -8.39   dC* +3.71   dhue -5.20 deg   C*/(L*+16) x1.266
#   against SPEC 10.4's dL* -8.8, dC* +5.0, dhue -6.6.  Independent
#   confirmation of 10.4 to 0.4 / 1.3 / 1.4 units.  (ref_workshop.jpg is a
#   DIFFERENT, unpainted vehicle in a shed and carries no weathering signal.)
#
# Solving that de-illuminated triple for the deposit leaves one degeneracy --
# a paler deposit at more coverage looks the same -- and the deposit HUE is
# invariant under it: 79.4 deg at coverage 0.41 through 80.8 deg at 0.75.  The
# degeneracy is closed by the rule that a constant tuned against another
# constant is expressed in terms of it: the settled dust is the SAME MINERAL
# as the road film, so it keeps W_DUST_COL's L*, and the coverage falls out.
#   -> W_DUST_COL_UP  L* 69.10 (== W_DUST_COL), C* 20.29, hue 79.61
#   -> W_DUST_FAC_UP  0.7313, i.e. mean coverage 0.548 on the counter top
#      ^^^^^^^^^^^^^^^^^^^^^^ RETIRED in rev 29, SPEC 10.82.  See below.
# The 0.35 that used to sit here is NOT deleted: it was doing two jobs, and
# its tide-line job (thinning the road film where the tide line runs out)
# survives verbatim as W_DUST_FAC_TOP, so this change moves the flank not at
# all.  Verified below by assert, not by inspection.
#
# ============================ rev 29, SPEC 10.82 ============================
# W_DUST_FAC_UP IS RETIRED TO 0.0.  THIS IS A RETIREMENT OF A DERIVATION, NOT
# A TUNE.  Read this before restoring 0.7313.
#
# WHAT THE PARAGRAPH ABOVE ASSUMED.  Every line of that solve assumes the
# counter top in ref_rear34.jpg carries a settled-dust film.  _UP_MEASURED is
# even commented "dirty counter top, de-illuminated".  The coverage was solved
# to reproduce that dirty top.
#
# WHY THE ASSUMPTION IS GONE.  Two owner readings of the ONLY frame that shows
# these surfaces, taken a revision apart, on two DIFFERENT surfaces:
#   [stated, rev 28, SPEC 10.81] the COUNTER TOP is CLEAN VARNISHED PLYWOOD.
#   [stated, rev 29, SPEC 10.82] the ROOF is CLEAN.
# Both were asked with the crop box printed, as POINTERS with no number taken
# from them, and both pointers were validated before they were sent against a
# PROVEN straddler and an answered anchor (probe_updust_pointer.py, 6 controls).
#
# WHY THE SECOND READING IS THE ONE THAT SETTLES IT.  SPEC 10.81 barred a blind
# f = 0 because the counter reading is LOCAL and this constant is not.
# probe_dust_scope.py established BY EXECUTION -- not by reading -- that
# W_DUST_FAC_UP is ONE MULTIPLY node inside the file's ONE shared WEATHER
# node-tree, reaching ELEVEN materials, and that T1_W_DUP=0 takes ALL ELEVEN to
# zero.  The largest surface it films is not the counter at all: it is
# T1_body under T1_paint, 12.3697 m^2 of up-facing area at mean coverage
# 0.3916, against the counter top's 1.5768 m^2.  So the roof reading
# contradicts the film on 86.4 % of the area it paints.  That is what a LOCAL
# reading could not do and this one does.
#
# WHAT THIS DOES NOT CLAIM, stated rather than left to be discovered:
#   * It does NOT fix COUNTERTAN.  SPEC 10.81 measured that a clean counter top
#     is still 34.0 % short in B.  Removing the film was NECESSARY AND IS NOT
#     SUFFICIENT, and the residual is still a COUNTERTAN/CREAM problem.
#   * It DOES retire SPEC 10.70's 57.1/52.6/36.6 % of the COUNTERTAN pedestal
#     as a MODELLED FEATURE.  10.70's measurement of what that film contributed
#     stands; what is withdrawn is the claim that it belongs on the vehicle.
#   * It asserts more than two readings strictly support -- that NO up-facing
#     surface on this vehicle carries settled dust.  The bumper top, the rim
#     barrels and the hub caps are filmed by the same node and NOBODY HAS BEEN
#     ASKED about them.  Named, not hidden.  A per-material constant would be
#     AUTHORED; this is the minimal change consistent with both readings.
#   * The ROAD film is untouched.  With fup = 0 the graph's MAXIMUM at :938
#     collapses to `flow`, and `dsel` -> 0 so `dcol` -> W_DUST_COL.  The tide
#     line, the rocker and the tyres are bit-identical.  Asserted, not assumed.
# ============================================================================
W_DUST_COL_UP = (0.5077, 0.3775, 0.2340)     # settled ochre, sRGB(189,165,133)
W_DUST_FAC_TOP = 0.35        # road film where the tide line fades out
W_DUST_FAC_LOW = float(os.environ.get("T1_W_DLO", 0.50))   # road film, rocker
# rev 29: 0.7313 RETIRED (SPEC 10.82).  The override is kept so the retired
# arm can still be rendered for comparison -- T1_W_DUP=0.7313 restores it.
W_DUST_FAC_UP = float(os.environ.get("T1_W_DUP", 0.0))     # RETIRED, rev 29

# the two locked albedos the solve above consumed, and its answer
COUNTERCREAM = (0.7350, 0.7150, 0.6600)
_UP_MEASURED = (0.6104, 0.5300, 0.4265)   # dirty counter top, de-illuminated
# rev 27, SPEC 10.76 -- TWO CORRECTIONS TO THE PARAGRAPH ABOVE, both verified:
#  (a) "(0.9676, 0.7784, 0.4976)" used to sit beside the words "this file's
#      CREAM".  It is NOT CREAM.  CREAM is (0.6172, 0.6308, 0.5776) at line 96.
#      That triple is the VON-KRIES GAIN ITSELF -- lin(203,186,146)/CREAM
#      reproduces it to 4.7e-5.  The arithmetic of the solve was right; only
#      the label was wrong.  Parenthetical moved out of the CREAM phrase.
#  (b) NEITHER source patch has coordinates anywhere in this repo.  They were
#      recovered forensically in rev 27 by searching ref_rear34.jpg for the box
#      whose middle-80%-of-L* median IS the recorded triple:
#          flank  u 914-983  v 298-337  (69x39 = 2691 px, trimmed n = 2153)
#                 -- EXACT, and unique; but its right ~12 columns run past the
#                    panel edge, 15 past _BODY's own u1 = 968.  Median-robust:
#                    clipping it back moves the answer by ONE code value.
#          top    u 556-656  v 397-424  (100x27 = 2700 px, trimmed n = 2160)
#                 -- exact, but NOT unique; several boxes reproduce it.
#      What IS box-independent: the counter top is a diagonal band 15-25 px
#      deep, and the largest axis-aligned rectangle lying entirely on it is
#      1060-1512 px across a swept class gate.  The patch needs 2700.  So the
#      founding patch STRADDLED whichever box was used -- 66-82 % tan, 8-19 %
#      cream, 6-9 % brass nosing, 2-4 % a tin can standing on the counter.
#      The straddle is real and is NOT the explanation: on a clean
#      band-following sample the disagreement gets WORSE, not better.
#      See probe_dust_anchor.py, which asserts all of this rather than
#      claiming it.

# ---------------------------------------------------------- counter top, tan
# rev 12.  The OWNER was shown marked crops of the counter and ruled: "tan top,
# brass nosing on the OUTER EDGE, body cream below".  The model painted the
# whole fitting `countercream`; a tan top is a material the spec never had.
#
# Derived as a RATIO against a surface of the SAME CLASS, never from an absolute
# pixel value -- SPEC sec.10.21, the rule that cost rev 10 one wrong silver.
# Both references are matte painted/laminate, measured in ref_side.jpg (the
# lower-exposure frame; every cream in ref_rear34.jpg clips at 249-254 and a
# clipped reference cannot carry a ratio):
#
#   tan top      x 700-780, y 411-415   sRGB (200,167,128)  lin (.5776,.3866,.2159)
#   counter fascia, VERTICAL, same fitting, 10 px away, same light
#                x 700-780, y 421-427   sRGB (212,189,166)  lin (.6585,.5089,.3813)
#   cab roof cream, UP-FACING, same orientation, 4 m away
#                x 180-270, y 270-280   sRGB (188,175,167)  lin (.5030,.4287,.3864)
#
# The two references bracket rather than agree, and the disagreement is real and
# structural, so it is carried rather than averaged away silently:
#   * against the FASCIA (same light, wrong orientation, and it takes red bounce
#     off the body that the up-facing top does not): albedo G 0.416, r/g 1.129
#   * against the CAB ROOF (right orientation, different local surround -- it is
#     out from under the lid and the roof overhang): albedo G 0.569, r/g 1.246
# Level is the midpoint, G 0.493, with the bracket [0.416, 0.569] = -16 %/+15 %.
# Chromaticity is the robust part: an illuminant gain divides out of a ratio,
# and the two references agree on b/g to 0.62 +/- 0.06.
#
# So: the HUE of this constant is measured, the LEVEL is bracketed and its
# bracket is +/-16 %. Override with T1_CTAN=r,g,b to test the ends.
COUNTERTAN = (0.5870, 0.4930, 0.3060)     # = sRGB (201,186,150), h 42, s 0.25
if os.environ.get("T1_CTAN"):
    COUNTERTAN = tuple(float(v) for v in os.environ["T1_CTAN"].split(","))


def counter_tan():
    """The tan laminate datablock, for t1_detail's counter_top().

    t1_detail's spec4_details() runs at build.py step 7, BEFORE build_all() at
    step 9, so a bare bpy.data.materials.get() cannot see it. simple() resolves
    by name, so calling this early and calling it again from build_all() hands
    back the same datablock rather than a second copy.
    """
    # rev 15: the finish numbers live HERE, not at the build_all() call site --
    # simple() resolves by name and this function runs first (step 7 vs step 9),
    # so build_all()'s arguments are dead.  A four-arm coat/spec ablation set at
    # the LATER site read identical to four decimals, which is what exposed it.
    return simple("countertan", COUNTERTAN,
                  rough=float(os.environ.get("T1_CTAN_RG", 0.42)),
                  coat=float(os.environ.get("T1_CTAN_CT", 0.05)),
                  spec=float(os.environ.get("T1_CTAN_SP", 0.32)))


def _lstar(c):
    """CIE L* of a linear-sRGB reflectance triple (D65, Yn = 1)."""
    y = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    return 116.0 * (y ** (1.0 / 3.0)) - 16.0 if y > (6 / 29.) ** 3 else \
        116.0 * (y / (3 * (6 / 29.) ** 2) + 4 / 29.) - 16.0


assert abs(_lstar(W_DUST_COL_UP) - _lstar(W_DUST_COL)) < 0.05, (
    "the settled dust is the same mineral as the road film and must carry its "
    "L*; re-solve W_DUST_COL_UP if W_DUST_COL moves")
if not (os.environ.get("T1_W_DUP") or os.environ.get("T1_W_DLO")):
    _f_up = W_DUST_UP_W * W_DUST_MOT_MEAN * W_DUST_FAC_UP * 1.4   # counter dust
    # ---- rev 29, SPEC 10.82.  THE DERIVATION ASSERT IS RETIRED, NOT WIDENED.
    #
    # What used to stand here asserted that the up-face deposit reproduces
    # _UP_MEASURED to 2e-3 -- i.e. that the model's counter top matches a
    # DIRTY counter top.  Two owner readings of the only frame that shows
    # these surfaces have withdrawn that target:
    #   [stated, rev 28] the counter top is CLEAN VARNISHED PLYWOOD
    #   [stated, rev 29] the roof is CLEAN
    # and probe_dust_scope.py showed the constant films the ROOF over 86.4 %
    # of the area it reaches, so the second reading is not a second opinion
    # about the counter -- it is a reading of the surface that dominates the
    # lever.  The assert did not start failing because a number drifted.  Its
    # PREMISE was withdrawn.  This is SPEC 10.59's shape exactly: the owner
    # retired H_ROOF as a target and the probe was kept as a LABELLED
    # regression catcher rather than deleted or re-valued to the model.
    #
    # WIDENING THE OLD BAND WOULD HAVE BEEN THE WRONG REPAIR and is barred:
    # at f = 0 the old assert misses by 0.2335, a hundredfold, because it is
    # comparing a clean top with a measurement of a dirty one.  A band that
    # admits both is a band that tests nothing.
    #
    # What replaces it is narrower and can actually fail: the shipped up-face
    # coverage must be EXACTLY zero.  If anyone restores 0.7313 in source --
    # as opposed to rendering the retired arm through T1_W_DUP, which is
    # deliberately still supported -- this fires.  WATCHED FIRE, rev 29.
    assert _f_up == 0.0, (
        "SPEC 10.82: W_DUST_FAC_UP is RETIRED to 0.0 on two owner readings "
        "(counter top rev 28, roof rev 29). The shipped up-face coverage is "
        "%.6f, not 0. Restoring the film needs a photograph, not an edit; to "
        "render the retired arm use T1_W_DUP=0.7313, which skips this block."
        % _f_up)
    # And the road film must be untouched by the retirement.  fup enters the
    # graph only through MAXIMUM(flow, fup) at :938 and through dsel at :944,
    # so at fup = 0 both collapse to the road branch exactly.  Stated here and
    # MEASURED in probe_dust_scope.py rather than asserted by inspection.
    assert W_DUST_FAC_TOP == 0.35 and abs(W_DUST_FAC_LOW - 0.50) < 1e-12, (
        "SPEC 10.82 retired the UP-FACE deposit only. The road film's own "
        "constants moved, which the retirement does not license.")

    # ---- rev 27, SPEC 10.76.  ARMING THE COUPLING THE ASSERT ABOVE CANNOT SEE.
    #
    # READ THIS BEFORE TOUCHING THE NUMBER BELOW.  It is a LABELLED REGRESSION
    # CATCHER, exactly like verify.py's H_ROOF_REGRESSION and the off-flank
    # crossing baseline.  It says "this disagreement HAS NOT MOVED".  It does
    # NOT say the disagreement is acceptable, and driving it to zero would mean
    # inventing an albedo.  DO NOT TIGHTEN IT AND DO NOT TUNE TO IT.
    #
    # The assert above solves the up-face dust coverage against COUNTERCREAM.
    # The counter top carries COUNTERTAN, and has since rev 12 -- both halves
    # entered in the SAME commit, 00d3819.  The assert cannot see that, because
    # it never reads COUNTERTAN.  So it would keep passing however far
    # COUNTERTAN moved.  SPEC 10.71.
    #
    # Two further things rev 27 measured, and they make the item sharper than
    # "the coverage is wrong":
    #   * The agreement above is a TAUTOLOGY, not a check.  W_DUST_COL_UP was
    #     solved collinear with COUNTERCREAM and _UP_MEASURED, so the three
    #     channels MUST agree -- measured spread 5.2e-05.  It is the solve
    #     restated.
    #   * Against COUNTERTAN there is no coverage error, because THERE IS NO
    #     COVERAGE.  _UP_MEASURED lies OUTSIDE the segment [COUNTERTAN,
    #     W_DUST_COL_UP] in all three channels; solving anyway gives
    #     f = (-0.295, -0.320, -1.674), three negative values disagreeing by
    #     5.7x.  On a clean band-following sample, gate and erosion swept over
    #     12 arms, every arm is more negative still.
    #
    # NOT decided here, deliberately: whether COUNTERTAN or _UP_MEASURED's
    # label is wrong.  The de-illuminated top is PROPORTIONAL to CREAM
    # channel-wise, and CREAM is this project's largest open constant; and the
    # pair is up-facing top vs vertical flank, the same orientation mismatch
    # SPEC 10.60 ruled INADMISSIBLE when it struck COUNTERTAN's cab-roof arm.
    # The baseline is the THREE-CHANNEL residual, not its max.  rev 27's first
    # cut asserted only the max; falsifying it exposed that the max lives in B,
    # so displacing COUNTERTAN's R by +0.020 left the guard silent.  A guard
    # that is right for the wrong reason is not a guard (SPEC 10.67) -- the
    # CAUSE was fixed, the band was not widened.  Every figure below was
    # watched print.
    if not os.environ.get("T1_CTAN"):
        _pred_tan = tuple(c + _f_up * (d - c)
                          for c, d in zip(COUNTERTAN, W_DUST_COL_UP))
        _resid_tan = tuple(p - m for p, m in zip(_pred_tan, _UP_MEASURED))
        # rev 29, SPEC 10.82: RE-BASELINED, and the reason is stated because a
        # re-baseline is the one move that can quietly turn a guard off.  The
        # rev-26 baseline (-0.066877, -0.100324, -0.159974) was the residual
        # WITH the up-face film at f_up = 0.548256.  That film is retired, so
        # the old figure is unreachable by construction, not merely stale --
        # this is rev 23's roof-hole precedent (68052 -> 68564 after the door
        # outlines moved), a DELIBERATE re-baseline after a deliberate change,
        # never a widening.  The band is UNCHANGED at 2e-3.
        #
        # The new baseline is STRONGER than the old one: at f_up = 0 the
        # prediction IS COUNTERTAN, so the residual is exactly
        # COUNTERTAN - _UP_MEASURED and this catcher now watches those two
        # constants directly, with no dust term standing between them.
        # Every digit below was watched print, not typed from memory.
        _RESID_BASELINE = (-0.023400, -0.037000, -0.120500)
        assert max(abs(r - b) for r, b in
                   zip(_resid_tan, _RESID_BASELINE)) < 2e-3, (
            "SPEC 10.76 regression catcher: the COUNTERTAN-vs-_UP_MEASURED "
            "residual has MOVED, %s against the rev-26 baseline %s. Something "
            "in {COUNTERTAN, W_DUST_COL_UP, W_DUST_FAC_UP, W_DUST_UP_W, "
            "W_DUST_MOT_MEAN, _UP_MEASURED} changed. This is NOT a failure to "
            "fix by widening the band -- re-run probe_dust_anchor.py and "
            "re-ground SPEC 10.71."
            % (tuple(round(v, 6) for v in _resid_tan), _RESID_BASELINE))
        # And the sign statement, which is the finding itself: no physical
        # coverage reaches _UP_MEASURED from COUNTERTAN.  If this ever stops
        # holding, SPEC 10.71 has been resolved by something and must be re-read.
        assert all(r < 0 for r in _resid_tan), (
            "SPEC 10.76: _UP_MEASURED used to lie OUTSIDE the segment "
            "[COUNTERTAN, W_DUST_COL_UP] in all three channels. It no longer "
            "does: residual %s" % (tuple(round(v, 6) for v in _resid_tan),))

# sun fade -- a DESIGN VALUE, not a measurement.  Neither in-service photo is
# in direct sun (ref_side.jpg open shade, ref_rear34.jpg under a palapa), so
# fade cannot be separated from exposure.  Kept well under the dust term.
# ---------------------------------------------------------------- rev 19 --
# CREAM CHALKY SUN-FADE MOTTLE.  Every one of these is overridable so the map
# can be ablated and swept without editing source -- the rule that cost three
# revisions on W_ALBEDO.  MOTTLE_AMP = 0.0 is the ABLATION arm and must render
# identically to the pre-rev-19 tree.
#
# MOTTLE_M is the mottle's characteristic size IN METRES, because the noise is
# fed OBJECT coordinates: Scale = 1/MOTTLE_M.  Quoting it in metres rather
# than as a bare Scale is deliberate -- the target spectrum is scale-indexed
# and a bare Scale cannot be compared with it.
MOTTLE_M      = float(os.environ.get("T1_MOT_M",     0.024))
MOTTLE_DETAIL = float(os.environ.get("T1_MOT_DET",   4.0))
MOTTLE_ROUGH  = float(os.environ.get("T1_MOT_RGH",   0.62))
MOTTLE_LO     = float(os.environ.get("T1_MOT_LO",    0.34))
MOTTLE_HI     = float(os.environ.get("T1_MOT_HI",    0.66))
MOTTLE_AMP    = float(os.environ.get("T1_MOT_AMP",   0.55))
MOTTLE_RGH_K  = float(os.environ.get("T1_MOT_RGHK",  0.18))
# rev 20: a rigid TRANSLATION of the mottle's sampling point in object space.
# It changes which part of the noise field the flank sees and NOTHING else --
# same Scale, same Detail, same Roughness, so the map's own statistics are
# identical by construction and only its PHASE relative to the other object-
# space noises moves.  (0,0,0) is therefore an exact no-op and is the control.
#
# WHY IT EXISTS.  Every noise in this material is fed the SAME `Object` vector
# and Blender's noise is one field sampled at different Scales, so two noises
# whose scales are close alias onto each other.  W_N2 (Scale 22, Detail 4) has
# octaves at 22 / 44 / 88 / 176; the mottle's base octave is 1/0.024 = 41.67,
# which sits 5.3 % from W_N2's second octave.  The albedo breakup maps high
# noise to MORE chroma and the mottle maps high noise to MORE fade, i.e. LESS
# chroma -- so an aliased pair subtracts.  Measured, not assumed: see SPEC.
MOTTLE_OFS    = tuple(float(v) for v in
                      os.environ.get("T1_MOT_OFS", "0,0,0").split(","))

W_FADE_SAT = float(os.environ.get("T1_W_FADESAT", 0.88))
W_FADE_VAL = float(os.environ.get("T1_W_FADEVAL", 1.04))

# orange peel.  rev-3 had Scale 190 with the noise Vector UNLINKED, so it fell
# back to Generated (bounding-box) coordinates: 22.3 / 9.2 / 8.1 mm on T1_body
# at 2.75:1, and the SAME material on gutter+-1 where it is 140:1.  Object
# coordinates fix the anisotropy.  Resolvable peel goes in the Bump; the
# 0.3-1.5 mm microstructure does NOT -- an A/B put a 0.5 mm bump at Strength
# 0.35 on the Monte-Carlo noise floor, where it only aliases.  Fold it into
# Roughness instead.
W_PEEL_SCALE, W_PEEL_DETAIL = 220.0, 2.0
W_PEEL_STRENGTH, W_PEEL_DIST = 0.12, 0.0006
W_MICRO_SCALE, W_MICRO_DETAIL = 1400.0, 1.0
W_MICRO_LO, W_MICRO_HI, W_MICRO_AMP = 0.35, 0.65, 0.035

# per-material wear weights (SPEC rev6 sec.3)
WEAR = dict(bumpercream=1.0, wheelcream=0.8, countercream=0.7, countertan=0.7,
            capred=0.6,
            capwhite=0.6, T1_paint=0.55, calidad=0.55, cream=0.3,
            roundelred=0.25)


def _nt(mat):
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (900, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (560, 0)
    bsdf.inputs["Subsurface Weight"].default_value = 0.0
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    return nt, bsdf


def simple(name, base, rough=0.35, metal=0.0, spec=0.5, coat=0.0,
           ior=1.45, emit=None, transmit=0.0, alpha=1.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    nt, b = _nt(m)
    b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Specular IOR Level"].default_value = spec
    b.inputs["IOR"].default_value = ior
    if coat:
        b.inputs["Coat Weight"].default_value = coat
        b.inputs["Coat Roughness"].default_value = 0.030
    if transmit:
        b.inputs["Transmission Weight"].default_value = transmit
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
        m.blend_method = 'BLEND'
    if emit:
        b.inputs["Emission Color"].default_value = (*emit[0], 1)
        b.inputs["Emission Strength"].default_value = emit[1]
    return m


def img_paint(name, filename, rough=0.50, spec=0.42):
    """Painted board carrying an image albedo, UV-mapped. rev 8: the lid boards.

    Roughness is driven off the image luminance rather than left constant --
    the dark ground on a hand-painted board is thicker, matter paint than the
    pale motifs, and a constant roughness is the physical definition of the
    plastic look SPEC sec.3 locks out.
    """
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    nt, b = _nt(m)
    tex = _img(nt, filename, -620, 60, ext='EXTEND')
    nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
    lum = nt.nodes.new("ShaderNodeRGBToBW"); lum.location = (-420, -180)
    nt.links.new(tex.outputs["Color"], lum.inputs[0])
    rr = _mr(nt, lum.outputs[0], 0.0, 1.0, rough + 0.10, rough - 0.10, -240, -180)
    nt.links.new(rr.outputs[0], b.inputs["Roughness"])
    b.inputs["Specular IOR Level"].default_value = spec
    return m


def emissive(name, colour, strength=8.0, base=(0.85, 0.84, 0.82)):
    """A lit festoon bulb: warm emission over a pearl-white envelope."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    nt, b = _nt(m)
    b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Roughness"].default_value = 0.22
    b.inputs["Specular IOR Level"].default_value = 0.45
    b.inputs["Emission Color"].default_value = (*colour, 1)
    b.inputs["Emission Strength"].default_value = strength
    return m


# ---------------------------------------------------------------------------
def _img(nt, filename, x, y, projection='FLAT', blend=0.0,
         interp='Cubic', ext='CLIP'):
    node = nt.nodes.new("ShaderNodeTexImage")
    node.location = (x, y)
    path = os.path.join(TEXDIR, filename)
    if os.path.exists(path):
        node.image = bpy.data.images.load(path, check_existing=True)
        node.image.colorspace_settings.name = 'sRGB'
    node.projection = projection
    node.projection_blend = blend
    node.interpolation = interp
    node.extension = ext
    return node


def _feed(nt, src, socket):
    """src may be a node, an output socket, or a plain number"""
    if src is None:
        return
    if hasattr(src, 'outputs'):                 # a node
        nt.links.new(src.outputs[0], socket)
    elif hasattr(src, 'node'):                  # an output socket
        nt.links.new(src, socket)
    else:
        socket.default_value = src


def _math(nt, op, a=None, b=None, x=0, y=0, clamp=False):
    n = nt.nodes.new("ShaderNodeMath")
    n.operation = op
    n.location = (x, y)
    n.use_clamp = clamp
    _feed(nt, a, n.inputs[0])
    _feed(nt, b, n.inputs[1])
    return n


def _mr(nt, val, fmin, fmax, tmin, tmax, x=0, y=0, smooth=False, clamp=True):
    """MapRange (float).  smooth -> SMOOTHSTEP interpolation."""
    n = nt.nodes.new("ShaderNodeMapRange")
    n.location = (x, y)
    n.clamp = clamp
    if smooth:
        n.interpolation_type = 'SMOOTHSTEP'
    for src, sock in ((val, 0), (fmin, 1), (fmax, 2), (tmin, 3), (tmax, 4)):
        _feed(nt, src, n.inputs[sock])
    return n


def _noise(nt, vec, scale, detail, x, y, rough=None):
    """noise texture.  vec MUST be supplied -- an unlinked Vector silently
    falls back to Generated (bounding-box) coordinates, which is anisotropic
    and object-size dependent."""
    n = nt.nodes.new("ShaderNodeTexNoise")
    n.location = (x, y)
    n.inputs["Scale"].default_value = scale
    n.inputs["Detail"].default_value = detail
    if rough is not None:
        n.inputs["Roughness"].default_value = rough
    nt.links.new(vec, n.inputs["Vector"])
    return n


def _mixf(nt, fac, a, b, x=0, y=0):
    n = nt.nodes.new("ShaderNodeMix")
    n.data_type = 'FLOAT'
    n.location = (x, y)
    _feed(nt, fac, n.inputs[0])
    _feed(nt, a, n.inputs[2])
    _feed(nt, b, n.inputs[3])
    return n


def _mixc(nt, fac, a, b, x=0, y=0, blend='MIX'):
    n = nt.nodes.new("ShaderNodeMix")
    n.data_type = 'RGBA'
    n.blend_type = blend
    n.location = (x, y)
    n.inputs[0].default_value = 1.0
    _feed(nt, fac, n.inputs[0])
    if isinstance(a, tuple):
        n.inputs[6].default_value = (*a, 1)
    else:
        _feed(nt, a, n.inputs[6])
    if isinstance(b, tuple):
        n.inputs[7].default_value = (*b, 1)
    else:
        _feed(nt, b, n.inputs[7])
    return n


# =========================================================== WEATHER group
def weather_group(name="WEATHER"):
    """Shared weathering field.

    in : Base Color, Roughness, Dust, Wear, Fade, Peel
    out: Base Color, Roughness, Normal, Metallic

    Metallic is not in the original interface list but 2b requires the bare
    steel stage to read as metal rather than grey paint, and a node group
    cannot write a socket it does not expose.  It is 0 everywhere the steel
    mask is 0, so linking it is a no-op on every non-chipped material.
    """
    ng = bpy.data.node_groups.get(name)
    if ng:
        return ng
    ng = bpy.data.node_groups.new(name, "ShaderNodeTree")
    I = ng.interface
    s = I.new_socket("Base Color", in_out='INPUT', socket_type='NodeSocketColor')
    s.default_value = (*CREAM, 1)
    for nm, dv in (("Roughness", 0.42), ("Dust", 0.0), ("Wear", 0.0),
                   ("Fade", 0.0), ("Peel", 0.0), ("FadeVert", 0.0),
                   ("FadeRough", 0.0)):
        s = I.new_socket(nm, in_out='INPUT', socket_type='NodeSocketFloat')
        s.default_value = dv
        s.min_value, s.max_value = 0.0, 2.0
    I.new_socket("Base Color", in_out='OUTPUT', socket_type='NodeSocketColor')
    I.new_socket("Roughness", in_out='OUTPUT', socket_type='NodeSocketFloat')
    I.new_socket("Normal", in_out='OUTPUT', socket_type='NodeSocketVector')
    I.new_socket("Metallic", in_out='OUTPUT', socket_type='NodeSocketFloat')

    nt = ng
    gi = ng.nodes.new("NodeGroupInput"); gi.location = (-2600, 0)
    go = ng.nodes.new("NodeGroupOutput"); go.location = (1800, 0)
    IN = dict(col=gi.outputs["Base Color"], rgh=gi.outputs["Roughness"],
              dust=gi.outputs["Dust"], wear=gi.outputs["Wear"],
              fade=gi.outputs["Fade"], peel=gi.outputs["Peel"],
              fadev=gi.outputs["FadeVert"],
              fadervg=gi.outputs["FadeRough"])

    # ---- front end.  Object coordinates, never Generated.
    texco = ng.nodes.new("ShaderNodeTexCoord"); texco.location = (-2600, -600)
    OBJ = texco.outputs["Object"]
    geo = ng.nodes.new("ShaderNodeNewGeometry"); geo.location = (-2600, -900)
    psep = ng.nodes.new("ShaderNodeSeparateXYZ"); psep.location = (-2420, -860)
    ng.links.new(geo.outputs["Position"], psep.inputs[0])
    nsep = ng.nodes.new("ShaderNodeSeparateXYZ"); nsep.location = (-2420, -1040)
    ng.links.new(geo.outputs["Normal"], nsep.inputs[0])
    PT = geo.outputs["Pointiness"]

    # ---- 2a multi-octave roughness + albedo breakup ---------------------
    n1 = _noise(nt, OBJ, W_N1_SCALE, W_N1_DETAIL, -2200, 400, W_N1_ROUGH)
    n2 = _noise(nt, OBJ, W_N2_SCALE, W_N2_DETAIL, -2200, 120)
    a1 = _math(nt, 'MULTIPLY', n1.outputs["Fac"], W_N1_W, -1980, 400)
    a2 = _math(nt, 'MULTIPLY', n2.outputs["Fac"], W_N2_W, -1980, 240)
    mix = _math(nt, 'ADD', a1, a2, -1820, 320)

    rlo = _math(nt, 'SUBTRACT', IN['rgh'], W_ROUGH_SWING, -1820, 640)
    rhi = _math(nt, 'ADD', IN['rgh'], W_ROUGH_SWING, -1820, 780)
    rough = _mr(nt, mix, W_MAP_LO, W_MAP_HI, rlo, rhi, -1600, 700)

    alb = _mr(nt, mix, W_MAP_LO, W_MAP_HI, 1.0 - W_ALBEDO, 1.0 + W_ALBEDO,
              -1600, 320)
    col = _mixc(nt, 1.0, IN['col'], alb.outputs[0], -1380, 320, blend='MULTIPLY')

    # ---- 2d sun fade (UNDER the dust film) ------------------------------
    # AUDIT_rev11 W2, severity 5: this MapRange is keyed on Normal.Z over
    # 0..1, so a VERTICAL surface has Nz = 0 and receives a fade factor of
    # exactly ZERO.  The flank is the largest painted area on the vehicle and
    # it was getting none.
    #
    # Measured in ref_side.jpg on the CREAM corner panel, X -1.60..-1.84:
    #     chroma  C* 14.55 -> 6.53  (-55 %)
    #     L*      89.6 -> 96.2
    #     hue     constant 67-73 deg      <- a fade signature, not a colour shift
    # the same panel in the render: C* 1.98 -> 1.59.
    #
    # WHY THIS IS NOT A BLANKET FIX, and what stopped me applying one.
    # SPEC 10.12 locks `RED` at sRGB (196,49,36) with saturation 0.816 as an
    # ALBEDO.  Feeding a vertical fade into every material would run the flank
    # red through HueSaturation at W_FADE_SAT = 0.88 and take that locked
    # albedo saturation to ~0.77 -- breaking an independently locked value to
    # satisfy a finding, which this project has learned not to do (10.24 holds
    # three findings applied then reverted for exactly this reason).
    #
    # So the vertical term is a SEPARATE, per-material input, default 0.0, and
    # it is switched on ONLY for the cream family -- which is where the
    # measurement above was actually taken, and none of which carries a locked
    # saturation.  `T1_paint`, `capred`, `roundelred` and `script` keep 0.0 and
    # the red lock is untouched.  See build_all().
    #
    # The value itself is not a fudge: the diffuse view factor of a plane to a
    # uniform hemisphere is (1 + Nz)/2, so a vertical surface sees exactly half
    # the sky a horizontal one does.  0.50 is that view factor, not a taste
    # call.  The measured -55 % is a spatial GRADIENT along the flank toward
    # the corner; this delivers the uniform part of it only, and the gradient
    # is left open rather than faked.
    fz = _mr(nt, nsep.outputs["Z"], 0.0, 1.0, 0.0, 1.0, -1380, -180)
    fz = _math(nt, 'MAXIMUM', fz.outputs[0], IN['fadev'], -1290, -180)
    ffac = _math(nt, 'MULTIPLY', fz, IN['fade'], -1200, -180, clamp=True)
    hs = ng.nodes.new("ShaderNodeHueSaturation"); hs.location = (-1020, 200)
    hs.inputs["Saturation"].default_value = W_FADE_SAT
    hs.inputs["Value"].default_value = W_FADE_VAL
    ng.links.new(ffac.outputs[0], hs.inputs["Fac"])
    ng.links.new(col.outputs[2], hs.inputs["Color"])

    # ---- 2b curvature edge wear -----------------------------------------
    pw = _mr(nt, PT, W_PT_LO, W_PT_HI, 0.0, 1.0, -2200, -420, smooth=True)
    cn = _noise(nt, OBJ, W_CHIP_SCALE, W_CHIP_DETAIL, -2200, -700)
    cm = _mr(nt, cn.outputs["Fac"], W_CHIP_LO, W_CHIP_HI, 0.0, 1.0,
             -2000, -700)
    cl = _noise(nt, OBJ, W_CLUST_SCALE, W_CLUST_DETAIL, -2200, -900)
    clm = _mr(nt, cl.outputs["Fac"], W_CLUST_LO, W_CLUST_HI, 0.0, 1.0,
              -2000, -900)
    cprod = _math(nt, 'MULTIPLY', cm, clm, -1820, -700)
    craw = _math(nt, 'MULTIPLY', pw, cprod, -1820, -560)
    # real chips have hard edges, not a fade
    hard = _math(nt, 'GREATER_THAN', craw, W_CHIP_CUT, -1640, -560)
    wear = _math(nt, 'MULTIPLY', hard, IN['wear'], -1460, -560, clamp=True)
    deep = _mr(nt, pw, W_STEEL_LO, W_STEEL_HI, 0.0, 1.0, -1640, -760,
               smooth=True)
    sn = _noise(nt, OBJ, W_CORE_SCALE, W_CORE_DETAIL, -1820, -920)
    core = _math(nt, 'GREATER_THAN', sn.outputs["Fac"], W_CORE_CUT,
                 -1640, -920)
    dcore = _math(nt, 'MULTIPLY', deep, core, -1460, -860)
    steel = _math(nt, 'MULTIPLY', wear, dcore, -1280, -760, clamp=True)

    cprim = _mixc(nt, wear, hs.outputs[0], W_PRIMER, -820, 200)
    csteel = _mixc(nt, steel, cprim.outputs[2], W_STEEL, -620, 200)

    # ---- 2e orange peel --------------------------------------------------
    pn = _noise(nt, OBJ, W_PEEL_SCALE, W_PEEL_DETAIL, -1200, -1100)
    pstr = _math(nt, 'MULTIPLY', IN['peel'], W_PEEL_STRENGTH, -1200, -1300)
    bump = ng.nodes.new("ShaderNodeBump"); bump.location = (-900, -1150)
    bump.inputs["Distance"].default_value = W_PEEL_DIST
    ng.links.new(pstr.outputs[0], bump.inputs["Strength"])
    ng.links.new(pn.outputs["Fac"], bump.inputs["Height"])

    mn = _noise(nt, OBJ, W_MICRO_SCALE, W_MICRO_DETAIL, -1200, -1500)
    mmr = _mr(nt, mn.outputs["Fac"], W_MICRO_LO, W_MICRO_HI,
              -W_MICRO_AMP, W_MICRO_AMP, -1000, -1500)
    mamt = _math(nt, 'MULTIPLY', mmr, IN['peel'], -820, -1500)
    r2 = _math(nt, 'ADD', rough.outputs[0], mamt, -640, 700)
    # bare steel is not chalky paint
    r3 = _mixf(nt, steel, r2, W_STEEL_ROUGH, -460, 700)

    # ---- 2c dust with a tide line ---------------------------------------
    rag = _noise(nt, OBJ, W_DUST_RAG_SCALE, W_DUST_RAG_DETAIL, -2200, -1300)
    ragc = _math(nt, 'SUBTRACT', rag.outputs["Fac"], 0.5, -2000, -1300)
    ragz = _math(nt, 'MULTIPLY_ADD', ragc, W_DUST_RAG_AMP, -1820, -1300)
    ng.links.new(psep.outputs["Z"], ragz.inputs[2])
    hgt = _mr(nt, ragz, W_DUST_Z_HI, W_DUST_Z_LO, 0.0, 1.0, -1640, -1300,
              smooth=True)
    upn = _mr(nt, nsep.outputs["Z"], W_DUST_NZ_LO, W_DUST_NZ_HI, 0.0, 1.0,
              -1640, -1480)
    upw = _math(nt, 'MULTIPLY', upn, W_DUST_UP_W, -1460, -1480)
    # independent loading paths -> MAXIMUM, not multiply
    dmax = _math(nt, 'MAXIMUM', hgt, upw, -1280, -1380, clamp=True)
    mot = _noise(nt, OBJ, W_DUST_MOT_SCALE, W_DUST_MOT_DETAIL, -1640, -1660)
    motm = _mr(nt, mot.outputs["Fac"], W_DUST_MOT_LO, W_DUST_MOT_HI,
               W_DUST_MOT_MIN, W_DUST_MOT_MAX, -1460, -1660)
    d1 = _math(nt, 'MULTIPLY', dmax, motm, -1100, -1380)
    dust = _math(nt, 'MULTIPLY', d1, IN['dust'], -920, -1380, clamp=True)
    # rev 12: TWO DEPOSITS, each with its own strength AND its own colour.
    # Road film thrown up off the ground fades out with the tide line and is
    # near-neutral limestone; dust that settles on upward faces does not care
    # about height at all and is the measured ochre.  The old graph ran one
    # colour through a single strength ramp driven by hgt, which meant a
    # VERTICAL panel high on the flank was still weighted as though it were an
    # upward face.  The road branch below reproduces the old arithmetic
    # exactly (W_DUST_FAC_TOP is the old constant), so the tide line and the
    # tyres do not move; only the upward branch changes.
    ftop = _mixf(nt, hgt, W_DUST_FAC_TOP, W_DUST_FAC_LOW, -1100, -1900)
    lo1 = _math(nt, 'MULTIPLY', hgt, motm, -920, -1900)
    flow = _math(nt, 'MULTIPLY', lo1, ftop, -740, -1900)
    up1 = _math(nt, 'MULTIPLY', upw, motm, -920, -2060)
    fup = _math(nt, 'MULTIPLY', up1, W_DUST_FAC_UP, -740, -2060)
    dstr = _math(nt, 'MAXIMUM', flow, fup, -560, -1980)
    dfac = _math(nt, 'MULTIPLY', dstr, IN['dust'], -380, -1980, clamp=True)
    # and the colour follows whichever deposit dominates, smoothly -- a hard
    # switch would draw a hue seam along the curve where they are equal
    dsum = _math(nt, 'ADD', flow, fup, -560, -2220)
    dsum2 = _math(nt, 'ADD', dsum, 1e-4, -420, -2220)
    dsel = _math(nt, 'DIVIDE', fup, dsum2, -280, -2220, clamp=True)
    dcol = _mixc(nt, dsel, W_DUST_COL, W_DUST_COL_UP, -140, -2220)
    cdust = _mixc(nt, dfac, csteel.outputs[2], dcol.outputs[2], -380, 200)

    # dust roughness is ADDITIVE so it stacks on the breakup
    dr = _math(nt, 'MULTIPLY', dust, W_DUST_ROUGH, -380, 700)
    r4 = _math(nt, 'ADD', r3, dr, -220, 700)
    r5 = _math(nt, 'MINIMUM', r4, W_ROUGH_CEIL, -60, 700)
    r6 = _math(nt, 'MAXIMUM', r5, 0.030, 100, 700)

    # rev 19: chalk raises roughness where it fades.  SPEC 10.38's mechanism
    # is "modulate the existing fade path AND drive roughness with it", and
    # until now FadeVert drove only the HueSaturation on Base Color -- so a
    # spatial fade map would have produced a colour mottle on a surface of
    # perfectly uniform gloss, which is not what oxidised paint does.
    #
    # `FadeRough` defaults to 0.0, so this branch adds exactly nothing to
    # every material that existed before this revision -- checked, not
    # assumed: at FadeRough = 0 the MULTIPLY is 0 and r7 == r6 identically.
    # It is a NEW input rather than a re-use of `Fade` because the two must
    # be separable: `script` runs fade = 0.5 and must not gain roughness.
    r7 = _math(nt, 'MULTIPLY', ffac.outputs[0], IN['fadervg'], 260, 760)
    r7 = _math(nt, 'ADD', r6, r7, 420, 700)
    r7 = _math(nt, 'MINIMUM', r7, 1.0, 560, 700)

    # index, not name: an output socket may share its name with an input and
    # Blender is free to disambiguate one of them
    ng.links.new(cdust.outputs[2], go.inputs[0])       # Base Color
    ng.links.new(r7.outputs[0], go.inputs[1])          # Roughness
    ng.links.new(bump.outputs[0], go.inputs[2])        # Normal
    ng.links.new(steel.outputs[0], go.inputs[3])       # Metallic
    return ng


def _bsdf(m):
    return next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')


def apply_weather(m, dust=0.0, wear=0.0, fade=0.0, peel=0.0, normal=True,
                  fadev=0.0, fadev_from=None, faderough=0.0):
    """Splice the WEATHER group between the material's colour/roughness
    sources and its Principled BSDF."""
    nt = m.node_tree
    b = _bsdf(m)
    g = nt.nodes.new("ShaderNodeGroup")
    g.node_tree = weather_group()
    g.location = (200, 260)

    cs = b.inputs["Base Color"]
    if cs.links:
        src = cs.links[0].from_socket
        nt.links.remove(cs.links[0])
        nt.links.new(src, g.inputs["Base Color"])
    else:
        g.inputs["Base Color"].default_value = cs.default_value[:]
    # rev 12: Roughness is re-routed the SAME way Base Color already was.
    # `nt.links.new` on an input socket replaces the link that is there, so the
    # old `default_value` read silently threw away any roughness a material had
    # built for itself and put its unlinked default under the group instead.
    # That hit exactly one material and it is the one that could least afford
    # it: `silver_script` maps the leaf texture's own value to Roughness
    # 0.520 (deep tarnish, matt) -> 0.205 (clean leaf) because a metal's
    # appearance is dominated by its specular, and that whole chain was
    # discarded, leaving the leaf at a flat 0.260. Measured on ref_side.jpg
    # (7335 px inside the lockup box x 330..610, y 470..595, saturation < 0.30
    # and 70 < L < 235, minus a 9x9 box blur so panel shading does not count):
    # the leaf carries a de-trended residual of 10.1 DN, and it is ANISOTROPIC
    # -- lag-2 autocorrelation 0.589 along the stroke against 0.454 across --
    # which is the hand-laid signature rev 10 measured at 7.4 DN and 1.6-2.0
    # stroke widths. A flat 0.260 cannot render any of it. Every other
    # weathered material has an unlinked Roughness, so this branch is a no-op
    # for all of them and the group swing now rides ON TOP of the tarnish map.
    rs = b.inputs["Roughness"]
    if rs.links:
        rsrc = rs.links[0].from_socket
        nt.links.remove(rs.links[0])
        nt.links.new(rsrc, g.inputs["Roughness"])
    else:
        g.inputs["Roughness"].default_value = rs.default_value
    g.inputs["Dust"].default_value = dust
    g.inputs["Wear"].default_value = wear
    g.inputs["Fade"].default_value = fade
    g.inputs["Peel"].default_value = peel
    # rev 19: `fadev_from` names a node ALREADY IN THIS MATERIAL whose first
    # output is linked into FadeVert instead of a scalar being written.  That
    # is how the cream mottle map reaches `T1_paint` without touching the red:
    # the map is multiplied by the material's own two-tone selector before it
    # gets here, so the red side is 0.0 BY CONSTRUCTION, not by a threshold.
    # A missing node is a hard error -- a silent fallback to the scalar is how
    # a map gets shipped switched off.
    if fadev_from is not None:
        src = nt.nodes.get(fadev_from)
        if src is None:
            raise RuntimeError(
                "apply_weather(%s): fadev_from=%r not found in this material -- "
                "refusing to fall back to a scalar" % (m.name, fadev_from))
        nt.links.new(src.outputs[0], g.inputs["FadeVert"])
    else:
        g.inputs["FadeVert"].default_value = fadev
    g.inputs["FadeRough"].default_value = faderough

    nt.links.new(g.outputs[0], b.inputs["Base Color"])
    nt.links.new(g.outputs[1], b.inputs["Roughness"])
    if normal:
        nt.links.new(g.outputs[2], b.inputs["Normal"])
    if wear > 0.0:
        nt.links.new(g.outputs[3], b.inputs["Metallic"])
    return m


def rough_field(name, swing=None, scale=180.0, detail=3.0, albedo_w=0.0,
                floor=0.03):
    """Give an ALREADY-BUILT material a roughness FIELD instead of a constant.

    `audit.py` calls a material constant-rough when its Principled Roughness
    socket carries no link, and `STATE.md` counts that as a defect class --
    "the physical definition of the plastic look".  Some of the offenders are
    built in `t1_detail.py`, which runs at build.py step 7, five steps before
    `build_all()`; this patches the DATABLOCK rather than the other file, so
    the two specialists cannot collide.  It is a no-op if the material does
    not exist, is not a node material, has no Principled, or already has a
    field -- so if `t1_detail` grows one of these later, this quietly stands
    down instead of double-driving the socket.

    The amplitude is `W_ROUGH_SWING`, not a new number: none of these surfaces
    is resolved well enough in either in-service photograph to measure a
    roughness variation (the pillar menu card is 20 x 66 px in ref_side.jpg),
    so the swing is a DESIGN value and is expressed in terms of the one swing
    the file already has rather than invented per material.

    albedo_w > 0 additionally drives roughness off the material's own Base
    Color luminance -- dark ink lies smoother than the pale stock under it,
    which is the same model `img_paint()` uses on the lid boards.
    """
    m = bpy.data.materials.get(name)
    if m is None or not m.use_nodes or m.node_tree is None:
        return None
    nt = m.node_tree
    b = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if b is None or b.inputs["Roughness"].links:
        return m
    if swing is None:
        swing = W_ROUGH_SWING
    base = float(b.inputs["Roughness"].default_value)
    x0 = min([n.location[0] for n in nt.nodes] or [0.0]) - 1400.0
    # Object coordinates, never Generated: every mesh carries an identity
    # transform at this point (build.py step 8b asserts it), so object space is
    # metres and the feature size below is a real feature size.
    tc = nt.nodes.new("ShaderNodeTexCoord"); tc.location = (x0, -760)
    n1 = _noise(nt, tc.outputs["Object"], scale, detail, x0 + 220, -760, 0.55)
    out = _mr(nt, n1.outputs["Fac"], 0.32, 0.68,
              base - swing, base + swing, x0 + 440, -760).outputs[0]
    cs = b.inputs["Base Color"]
    if albedo_w > 0.0 and cs.links:
        bw = nt.nodes.new("ShaderNodeRGBToBW"); bw.location = (x0 + 220, -1000)
        nt.links.new(cs.links[0].from_socket, bw.inputs[0])
        ar = _mr(nt, bw.outputs[0], 0.0, 1.0, -albedo_w, albedo_w,
                 x0 + 440, -1000)
        out = _math(nt, 'ADD', out, ar.outputs[0], x0 + 640, -880).outputs[0]
    lo = _math(nt, 'MAXIMUM', out, floor, x0 + 840, -880)
    hi = _math(nt, 'MINIMUM', lo, W_ROUGH_CEIL, x0 + 1020, -880)
    nt.links.new(hi.outputs[0], b.inputs["Roughness"])
    return m


# ===================================================== non-group variants
def _frontend(nt, x=-1900):
    texco = nt.nodes.new("ShaderNodeTexCoord"); texco.location = (x, -400)
    geo = nt.nodes.new("ShaderNodeNewGeometry"); geo.location = (x, -700)
    psep = nt.nodes.new("ShaderNodeSeparateXYZ"); psep.location = (x + 180, -660)
    nt.links.new(geo.outputs["Position"], psep.inputs[0])
    nsep = nt.nodes.new("ShaderNodeSeparateXYZ"); nsep.location = (x + 180, -840)
    nt.links.new(geo.outputs["Normal"], nsep.inputs[0])
    return texco.outputs["Object"], psep, nsep, geo


def _breakup(nt, obj, base_rough, swing=W_ROUGH_SWING, x=-1600):
    """the 2a field, reused by the non-group variants"""
    n1 = _noise(nt, obj, W_N1_SCALE, W_N1_DETAIL, x, 300, W_N1_ROUGH)
    n2 = _noise(nt, obj, W_N2_SCALE, W_N2_DETAIL, x, 60)
    a1 = _math(nt, 'MULTIPLY', n1.outputs["Fac"], W_N1_W, x + 200, 300)
    a2 = _math(nt, 'MULTIPLY', n2.outputs["Fac"], W_N2_W, x + 200, 140)
    mix = _math(nt, 'ADD', a1, a2, x + 380, 220)
    rough = _mr(nt, mix, W_MAP_LO, W_MAP_HI, base_rough - swing,
                base_rough + swing, x + 560, 220)
    return mix, rough


def tarnished(name, base, rough_lo, rough_hi, spec=0.5):
    """chrome / nickel tarnish.  Chrome wears to NICKEL: it dulls and pits,
    it does not chip to primer grey, so the WEATHER group is wrong here."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = simple(name, base, rough=rough_lo, metal=1.0, spec=spec)
    nt = m.node_tree
    b = _bsdf(m)
    obj, psep, nsep, geo = _frontend(nt)
    n1 = _noise(nt, obj, W_N1_SCALE, W_N1_DETAIL, -1600, 300, W_N1_ROUGH)
    n2 = _noise(nt, obj, W_N2_SCALE, W_N2_DETAIL, -1600, 60)
    a1 = _math(nt, 'MULTIPLY', n1.outputs["Fac"], W_N1_W, -1400, 300)
    a2 = _math(nt, 'MULTIPLY', n2.outputs["Fac"], W_N2_W, -1400, 140)
    mix = _math(nt, 'ADD', a1, a2, -1220, 220)
    rgh = _mr(nt, mix, W_MAP_LO, W_MAP_HI, rough_lo, rough_hi, -1040, 220)
    # dark pit speckle
    pit = _noise(nt, obj, 130.0, 2.0, -1600, -160)
    pm = _math(nt, 'GREATER_THAN', pit.outputs["Fac"], 0.615, -1400, -160)
    pmf = _math(nt, 'MULTIPLY', pm, 0.55, -1220, -160)
    col = _mixc(nt, pmf, base, (0.0900, 0.0870, 0.0820), -860, 220)
    rgh2 = _mixf(nt, pmf, rgh, 0.42, -860, 0)
    nt.links.new(col.outputs[2], b.inputs["Base Color"])
    nt.links.new(rgh2.outputs[0], b.inputs["Roughness"])
    b.inputs["Metallic"].default_value = 1.0
    return m


def dust_film(name, base, rough, spec=0.25, fac_up=0.22, fac_low=0.34,
              drough=0.10):
    """tyre / rubber: a sidewall dust film only.  Z ramp + upward term, no
    wear, no peel, no fade.  Blackwall per SPEC 0.2."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = simple(name, base, rough=rough, spec=spec)
    nt = m.node_tree
    b = _bsdf(m)
    obj, psep, nsep, geo = _frontend(nt)
    mix, rgh = _breakup(nt, obj, rough, swing=0.06)
    rag = _noise(nt, obj, W_DUST_RAG_SCALE, W_DUST_RAG_DETAIL, -1600, -1100)
    ragc = _math(nt, 'SUBTRACT', rag.outputs["Fac"], 0.5, -1420, -1100)
    ragz = _math(nt, 'MULTIPLY_ADD', ragc, W_DUST_RAG_AMP, -1240, -1100)
    nt.links.new(psep.outputs["Z"], ragz.inputs[2])
    hgt = _mr(nt, ragz, W_DUST_Z_HI, W_DUST_Z_LO, 0.0, 1.0, -1060, -1100,
              smooth=True)
    upn = _mr(nt, nsep.outputs["Z"], W_DUST_NZ_LO, W_DUST_NZ_HI, 0.0, 1.0,
              -1060, -1280)
    upw = _math(nt, 'MULTIPLY', upn, W_DUST_UP_W, -880, -1280)
    dmax = _math(nt, 'MAXIMUM', hgt, upw, -700, -1180, clamp=True)
    mot = _noise(nt, obj, W_DUST_MOT_SCALE, W_DUST_MOT_DETAIL, -1060, -1460)
    motm = _mr(nt, mot.outputs["Fac"], W_DUST_MOT_LO, W_DUST_MOT_HI,
               W_DUST_MOT_MIN, W_DUST_MOT_MAX, -880, -1460)
    dust = _math(nt, 'MULTIPLY', dmax, motm, -520, -1180, clamp=True)
    dfac0 = _mr(nt, hgt, 0.0, 1.0, fac_up, fac_low, -520, -1360)
    dfac = _math(nt, 'MULTIPLY', dust, dfac0, -340, -1280, clamp=True)
    col = _mixc(nt, dfac, base, W_DUST_COL, -180, 200)
    dr = _math(nt, 'MULTIPLY', dust, drough, -180, 0)
    r2 = _math(nt, 'ADD', rgh, dr, 0, 0)
    r3 = _math(nt, 'MINIMUM', r2, W_ROUGH_CEIL, 160, 0)
    nt.links.new(col.outputs[2], b.inputs["Base Color"])
    nt.links.new(r3.outputs[0], b.inputs["Roughness"])
    return m


def canvas_mat(name="canvas", base=(0.6600, 0.6420, 0.5900)):
    """ragtop duck: woven fibre + water staining, no chips, no peel"""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = simple(name, base, rough=0.86, spec=0.22)
    nt = m.node_tree
    b = _bsdf(m)
    obj, psep, nsep, geo = _frontend(nt)
    # anisotropic weave: stretch the coordinates so warp and weft differ
    mp = nt.nodes.new("ShaderNodeMapping"); mp.location = (-1720, -400)
    mp.inputs["Scale"].default_value = (1.0, 1.0, 0.28)
    nt.links.new(obj, mp.inputs["Vector"])
    weave = _noise(nt, mp.outputs[0], 150.0, 2.0, -1520, -400)
    wm = _mr(nt, weave.outputs["Fac"], 0.30, 0.70, 0.90, 1.08, -1320, -400)
    # water staining: low-frequency blotches that run downward
    stain = _noise(nt, obj, 4.5, 5.0, -1520, -700, 0.62)
    sm = _mr(nt, stain.outputs["Fac"], 0.44, 0.66, 0.0, 1.0, -1320, -700,
             smooth=True)
    scol = _mixc(nt, sm, base, (0.4150, 0.3860, 0.3300), -1000, 200)
    tex = _mixc(nt, 1.0, scol.outputs[2], wm.outputs[0], -800, 200,
                blend='MULTIPLY')
    mix, rgh = _breakup(nt, obj, 0.86, swing=0.05)
    sr = _math(nt, 'MULTIPLY_ADD', sm, 0.06, -600, 0)
    nt.links.new(rgh.outputs[0], sr.inputs[2])
    r2 = _math(nt, 'MINIMUM', sr, 0.94, -420, 0)
    nt.links.new(tex.outputs[2], b.inputs["Base Color"])
    nt.links.new(r2.outputs[0], b.inputs["Roughness"])
    return m


def interior_wear(name, base, rough, metal=0.0, spec=0.5):
    """galley stainless / dark interior: USE wear, not weather.  Scuff and
    handling polish, no dust tide line, no sun fade, no chips to primer."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = simple(name, base, rough=rough, metal=metal, spec=spec)
    nt = m.node_tree
    b = _bsdf(m)
    obj, psep, nsep, geo = _frontend(nt)
    mix, rgh = _breakup(nt, obj, rough, swing=0.07)
    # directional scuff: squash the coordinates along X so it streaks
    mp = nt.nodes.new("ShaderNodeMapping"); mp.location = (-1720, -1100)
    mp.inputs["Scale"].default_value = (1.0, 34.0, 34.0)
    nt.links.new(obj, mp.inputs["Vector"])
    scuff = _noise(nt, mp.outputs[0], 9.0, 3.0, -1520, -1100)
    sm = _mr(nt, scuff.outputs["Fac"], 0.38, 0.62, -0.055, 0.055, -1320, -1100)
    r2 = _math(nt, 'ADD', rgh, sm, -1000, 0)
    r3 = _math(nt, 'MAXIMUM', r2, 0.05, -840, 0)
    alb = _mr(nt, mix, W_MAP_LO, W_MAP_HI, 0.93, 1.07, -1000, 200)
    col = _mixc(nt, 1.0, base, alb.outputs[0], -820, 200, blend='MULTIPLY')
    nt.links.new(col.outputs[2], b.inputs["Base Color"])
    nt.links.new(r3.outputs[0], b.inputs["Roughness"])
    return m


# ============================================================ body paint
def body_paint(name="T1_paint"):
    """
    Cream above the break line, Tacombi red below, gold folk-art swirls
    box-projected over the red.  Weathering (breakup, chips, dust, fade,
    orange peel) comes from the shared WEATHER group.
    """
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    nt, bsdf = _nt(m)

    geo = nt.nodes.new("ShaderNodeNewGeometry"); geo.location = (-1600, 300)
    sep = nt.nodes.new("ShaderNodeSeparateXYZ"); sep.location = (-1420, 300)
    nt.links.new(geo.outputs["Position"], sep.inputs[0])

    # u = |y| / 0.86
    absy = _math(nt, 'ABSOLUTE', sep.outputs["Y"], None, -1240, 240)
    u = _math(nt, 'DIVIDE', absy, 0.860, -1080, 240, clamp=True)
    up = _math(nt, 'POWER', u, V_POW, -920, 240)
    zv = _math(nt, 'MULTIPLY_ADD', up, V_RISE, -760, 240)
    zv.inputs[2].default_value = V_APEX0          # value at x = 0; rake applied below

    # blend factor: 0 on the flanks, 1 across the nose panel
    tblend = nt.nodes.new("ShaderNodeMapRange")
    tblend.location = (-1000, 60)
    tblend.interpolation_type = 'SMOOTHSTEP'
    tblend.clamp = True
    tblend.inputs[1].default_value = 1.858
    tblend.inputs[2].default_value = 2.012
    tblend.inputs[3].default_value = 0.0
    tblend.inputs[4].default_value = 1.0
    nt.links.new(sep.outputs["X"], tblend.inputs[0])

    mixz = nt.nodes.new("ShaderNodeMix"); mixz.location = (-180, 200)
    mixz.data_type = 'FLOAT'
    mixz.inputs[2].default_value = Z_BELT0        # value at x = 0
    nt.links.new(tblend.outputs[0], mixz.inputs[0])
    nt.links.new(zv.outputs[0], mixz.inputs[3])

    # rev 8: apply the rake ONCE, after the mix, so it lands on both the flank
    # belt and the nose V-swage and V_APEX0 + V_RISE == Z_BELT0 keeps holding
    # at every station. break_z(x) = mix - RAKE_DZDX * x.
    rake = _math(nt, 'MULTIPLY_ADD', sep.outputs["X"], -RAKE_DZDX, -60, 90)
    nt.links.new(mixz.outputs[0], rake.inputs[2])

    # hard-ish edge:  cream = 1 when z > break
    dz = _math(nt, 'SUBTRACT', sep.outputs["Z"], rake.outputs[0], -20, 340)
    edge = _math(nt, 'DIVIDE', dz, 0.0045, 140, 340)
    edge = _math(nt, 'ADD', edge, 0.5, 300, 340, clamp=True)

    # ------------------------------------------------ rev 19: CREAM MOTTLE --
    # The CHALKY SUN-FADE MOTTLE map.  SPEC 10.38 supplies the mechanism; the
    # amplitude is re-grounded in 10.49 on the surface the owner identified.
    #
    # WHY IT LIVES HERE AND NOT IN build_all().  `T1_paint` renders cream ABOVE
    # the break line and red BELOW, in ONE material, and `T1_body` is the only
    # object carrying the vehicle's flank cream.  rev 14 could not switch
    # `FadeVert` on for this material because a material-level scalar runs the
    # flank RED through W_FADE_SAT = 0.88 and takes SPEC 10.12's locked albedo
    # saturation 0.816 to ~0.77.  So it was switched on for every OTHER cream
    # and the flank -- the surface 10.30c measured the -55 % on -- got NOTHING.
    # Probed on the built scene: `T1_paint` FadeVert 0.000, while the material
    # literally named `cream` carries exactly one object, `vw_disc`.
    #
    # Multiplying by `edge` -- the material's OWN two-tone selector, the same
    # node that decides which pixels are cream -- makes the red side exactly
    # 0.0 BY CONSTRUCTION.  The lock is not defended by a threshold someone
    # chose; the fade cannot be non-zero anywhere the paint is not cream.
    # That is rev 14's own principle: apply the finding so the lock survives.
    #
    # OBJECT coordinates, never Generated.  Generated is bbox-normalised, so a
    # feature size in metres would silently change if any station moved -- and
    # the tail has moved twice.  In object space, 1/Scale is metres.
    mtc = nt.nodes.new("ShaderNodeTexCoord"); mtc.location = (-900, 620)
    # rev 20: MOTTLE_OFS translates the sampling point only.  At (0,0,0) the
    # Mapping node is the identity, so this is a provable no-op control; the
    # ablation arm must reproduce the pre-rev-20 tree exactly.
    mot_v = mtc.outputs["Object"]
    if any(MOTTLE_OFS):
        mmap = nt.nodes.new("ShaderNodeMapping"); mmap.location = (-820, 620)
        mmap.vector_type = 'POINT'
        mmap.inputs["Location"].default_value = MOTTLE_OFS
        nt.links.new(mot_v, mmap.inputs["Vector"])
        mot_v = mmap.outputs["Vector"]
    mot_n = _noise(nt, mot_v, 1.0 / max(MOTTLE_M, 1e-9),
                   MOTTLE_DETAIL, -700, 620, MOTTLE_ROUGH)
    mot_r = _mr(nt, mot_n.outputs["Fac"], MOTTLE_LO, MOTTLE_HI,
                0.0, MOTTLE_AMP, -520, 620)
    mot = _math(nt, 'MULTIPLY', mot_r.outputs[0], edge, -340, 620, clamp=True)
    mot.name = "FADEV_MOTTLE"; mot.label = "FADEV_MOTTLE"

    # gold swirl decal, box-projected in object space
    texco = nt.nodes.new("ShaderNodeTexCoord"); texco.location = (-1600, -420)
    mp = nt.nodes.new("ShaderNodeMapping"); mp.location = (-1420, -420)
    mp.inputs["Location"].default_value = (0.185, 0.410, 0.263)
    # rev 8 (audit livery-7): 0.63 => a 1.587 m period, ~2.7 visible repeats
    # across the flank -- wallpaper, not signwriting. 0.42 => 2.38 m, 1.8
    # repeats, and the non-monotonic density mask below breaks the rest.
    # rev 8b: swirl.png is now PLACED signwriting (one dominant paisley per
    # quarter + rosettes + dark commas), not a seamless field. 0.42 repeated it
    # 1.8x across the flank and distinct motifs repeat visibly. 0.26 => a
    # 3.85 m period, i.e. essentially one pass over the 4.22 m flank.
    mp.inputs["Scale"].default_value = (0.2600, 0.2600, 0.2600)
    nt.links.new(texco.outputs["Object"], mp.inputs["Vector"])
    # rev 10 (audit materials-14): both flanks carried the SAME art, mirrored.
    # On a two-angle hero set that is fatal -- the studio view sees +Y and the
    # front three-quarter sees -Y, and a viewer comparing them sees the same
    # drawing twice. folk_gen.py now writes two tiles with different
    # compositions obeying identical measured statistics; they are selected on
    # the SIGN OF POSITION Y, which is unambiguous (the surface normal is not,
    # on a crowned flank). Whitened peak cross-correlation between the two
    # drawings sampled onto the same body grid falls 0.175 -> 0.064, and the
    # mirrored pairing no longer wins.
    swirl = _img(nt, "swirl.png", -1180, -420, projection='BOX',
                 blend=0.10, ext='REPEAT')
    nt.links.new(mp.outputs[0], swirl.inputs["Vector"])
    swirl_b = _img(nt, "swirl_b.png", -1180, -640, projection='BOX',
                   blend=0.10, ext='REPEAT')
    nt.links.new(mp.outputs[0], swirl_b.inputs["Vector"])
    sideY = _math(nt, 'GREATER_THAN', sep.outputs["Y"], 0.0, -1180, -760)

    # nose decal selector, built HERE because both the colour mix and the alpha
    # mask consume it and the alpha mask is assembled first.
    _geo = nt.nodes.new("ShaderNodeNewGeometry"); _geo.location = (-1600, -1500)
    _sepN = nt.nodes.new("ShaderNodeSeparateXYZ"); _sepN.location = (-1440, -1500)
    nt.links.new(_geo.outputs["Normal"], _sepN.inputs[0])
    _absx = _math(nt, 'ABSOLUTE', _sepN.outputs["X"], None, -1290, -1500)
    _facex = _math(nt, 'GREATER_THAN', _absx.outputs[0], 0.70, -1140, -1500)
    _fwd = _math(nt, 'GREATER_THAN', sep.outputs["X"], 1.60, -1140, -1620)
    _isNose = _math(nt, 'MULTIPLY', _facex.outputs[0], _fwd.outputs[0],
                    -990, -1560)
    _cmb = nt.nodes.new("ShaderNodeCombineXYZ"); _cmb.location = (-1440, -1380)
    nt.links.new(sep.outputs["Y"], _cmb.inputs[0])
    nt.links.new(sep.outputs["Z"], _cmb.inputs[1])
    _nmp = nt.nodes.new("ShaderNodeMapping"); _nmp.location = (-1290, -1380)
    _nmp.inputs["Scale"].default_value = (0.6410, 0.6410, 1.0)
    _nmp.inputs["Location"].default_value = (0.5000, -0.0128, 0.0)
    nt.links.new(_cmb.outputs[0], _nmp.inputs["Vector"])
    _nose = _img(nt, "nose.png", -1140, -1380, projection='FLAT', ext='CLIP')
    nt.links.new(_nmp.outputs[0], _nose.inputs["Vector"])
    _NOSE_SEL[0] = (_isNose, _nose) if _nose.image else None

    # ---- TAIL selector, rev 14 -----------------------------------------
    # AUDIT_rev12 item 2, severity 5, and the highest visible-defect-per-line
    # item in the whole report: the flank tile is BOX-projected, so EVERY face
    # whose normal is X-dominant samples it on (y, z).  `_facex` above is
    # |Nx| > 0.70 and is therefore true on the TAIL as well as the nose --
    # `_fwd` (X > +1.60) rescues only the nose.  Nothing gated the tail, so
    # gold folk art printed across the flat tail face.
    #
    # MEASURED, rev 14, independently of the audit and on a fixed row band
    # (ref_rear34.jpg rows 545-725), one gate (hue 25-90 deg, S > 0.35,
    # V > 0.45):
    #
    #     rear quarter, cols 830-940   43.687 % gold   n = 19 800 px  <- control
    #     flat tail face, cols 965-1150 0.006 % gold   n = 33 300 px
    #
    # Four orders of magnitude, with a positive control in the same rows of
    # the same frame.  AUDIT_rev12 measured 0.00 % gate-independent in 35 991
    # px against a 20.94 % control; the two agree.
    #
    # THE TRAP, named by the audit and confirmed here: the rear QUARTER's real
    # 43.7 % must survive.  The gate is keyed on |Nx|, and the quarter's normal
    # is not X-dominant -- it is still mostly +-Y on the corner radius -- so the
    # quarter keeps its art and only the rear-FACING panel loses it.  That is
    # also exactly where the photograph's art terminates: the aft-most gold is
    # at image column 952, which is the cream/red branch intersection, i.e. the
    # station where the corner turns.
    #
    # X < -1.60 is not a measured station and does not need to be: |Nx| > 0.70
    # already selects rear-facing geometry, and the X term exists ONLY to
    # exclude the nose, which sits at X > +1.60.  It can be wrong by 300 mm in
    # either direction without changing a single shaded pixel.
    #
    # Blended over 0.66-0.76 rather than a hard GREATER_THAN so a motif that
    # straddles the latitude fades instead of being sliced.  0.10 matches the
    # BOX projection_blend already in use two nodes up.
    _aft = _math(nt, 'LESS_THAN', sep.outputs["X"], -1.60, -1140, -1740)
    _tailface = _mr(nt, _absx.outputs[0], 0.66, 0.76, 0.0, 1.0,
                    -990, -1740, smooth=True)
    _isTail = _math(nt, 'MULTIPLY', _tailface.outputs[0], _aft.outputs[0],
                    -840, -1740)
    _notTail = _math(nt, 'SUBTRACT', 1.0, _isTail.outputs[0], -700, -1740,
                     clamp=True)

    # --- density mask (SPEC sec.3): heaviest on the nose, trailing along the
    #     belt, sparse at the tail. Applied as a spatially varying cutoff on a
    #     low-frequency noise so whole motifs drop out rather than fading.
    # rev 8: MEASURED off ref_side.jpg, gold coverage as a fraction of the
    # red+gold flank, sampled in 40 px columns:
    #
    #   X +1.47 .. -0.40   0.0-0.2 %      <- bare red, the script sits here
    #   X -0.59            4.7 %
    #   X -0.96           13.8 %
    #   X -1.71           25.9 %
    #   X -1.90           36.9 %          <- the rear-quarter bouquet
    #
    # plus a separate scroll on the cab door, forward of X +0.9 (missed by the
    # scan above -- the door is swung open in that photograph and sits outside
    # the band). rev 7 ran a SINGLE MapRange, 0.34 at the tail rising to 1.00 at
    # the nose: monotonic and exactly backwards, densest where the reference is
    # bare and sparsest where the bouquet is. Two lobes, combined with MAXIMUM.
    fx = nt.nodes.new("ShaderNodeMapRange"); fx.location = (-1180, -900)
    fx.interpolation_type = 'SMOOTHSTEP'; fx.clamp = True
    fx.inputs[1].default_value = -0.30
    fx.inputs[2].default_value = -2.05
    fx.inputs[3].default_value = 0.05
    fx.inputs[4].default_value = 1.00
    nt.links.new(sep.outputs["X"], fx.inputs[0])

    # second lobe: the cab-door scroll, forward of X +0.55
    fx2 = nt.nodes.new("ShaderNodeMapRange"); fx2.location = (-1180, -1060)
    fx2.interpolation_type = 'SMOOTHSTEP'; fx2.clamp = True
    fx2.inputs[1].default_value = 0.55
    fx2.inputs[2].default_value = 1.75
    fx2.inputs[3].default_value = 0.05
    fx2.inputs[4].default_value = 0.60
    nt.links.new(sep.outputs["X"], fx2.inputs[0])
    fx = _math(nt, 'MAXIMUM', fx.outputs[0], fx2.outputs[0], -1020, -960)

    bz = _math(nt, 'SUBTRACT', sep.outputs["Z"], 1.045, -1180, -1060)
    bz = _math(nt, 'DIVIDE', bz, 0.300, -1020, -1060)
    bz = _math(nt, 'MULTIPLY', bz, bz, -880, -1060)
    bz = _math(nt, 'MULTIPLY', bz, -1.0, -740, -1060)
    belt = _math(nt, 'EXPONENT', bz, None, -600, -1060)
    beltw = _math(nt, 'MULTIPLY_ADD', belt, 0.62, -460, -1060)
    beltw.inputs[2].default_value = 0.52
    dens = _math(nt, 'MULTIPLY', fx, beltw, -320, -960, clamp=True)

    clut = nt.nodes.new("ShaderNodeTexNoise"); clut.location = (-1180, -1240)
    clut.inputs["Scale"].default_value = 1.15
    clut.inputs["Detail"].default_value = 1.0
    nt.links.new(texco.outputs["Object"], clut.inputs["Vector"])
    thr = _math(nt, 'SUBTRACT', 0.92, dens, -180, -1240)
    keep = _math(nt, 'GREATER_THAN', clut.outputs["Fac"], thr, -40, -1240)
    # rev 10: `keep` is RETIRED, not deleted -- the nodes above are left in
    # place and unlinked so the next reader can see what was there. The mask
    # was a second density profile multiplied on top of the tile's own, and
    # after rev 10 the tile IS the measurement: 29.1 % gold on the cab door
    # with the measured 42 %->5 % gradient across it, 11.44 % on the lower
    # nose, and the rear-quarter bouquet. Multiplying by `keep` applied a
    # wrong profile to a right one. Worse, `fx2`'s door lobe topped out at
    # 0.60 over a window starting at X +0.55 -- its maximum sat on the flank
    # BEHIND the door, not on the door.
    mixA = nt.nodes.new("ShaderNodeMix"); mixA.location = (40, -1240)
    mixA.data_type = 'FLOAT'
    nt.links.new(sideY.outputs[0], mixA.inputs[0])
    nt.links.new(swirl_b.outputs["Alpha"], mixA.inputs[2])
    nt.links.new(swirl.outputs["Alpha"], mixA.inputs[3])
    if _NOSE_SEL[0] is not None:
        _isNose, _nose = _NOSE_SEL[0]
        mixNA = nt.nodes.new("ShaderNodeMix"); mixNA.location = (60, -1400)
        mixNA.data_type = 'FLOAT'
        nt.links.new(_isNose.outputs[0], mixNA.inputs[0])
        nt.links.new(mixA.outputs[0], mixNA.inputs[2])
        nt.links.new(_nose.outputs["Alpha"], mixNA.inputs[3])
        amask = _math(nt, 'MULTIPLY', mixNA.outputs[0], 1.0, 100, -1240)
        # rev 11 AUDIT, severity 5: this line used to read `_NOSE_SEL[0] = None`.
        # The alpha branch is assembled BEFORE the colour branch (line ~990), so
        # clearing the handoff here meant the colour mix never wired -- the nose
        # got nose.png's SHAPE from the alpha path and the flank tile's COLOUR,
        # which is (0,0,0) wherever the flank tile is transparent. The nose
        # rendered as black marks. The selector is freshly assigned at line 871
        # on every call, so there is nothing to clear.
    else:
        amask = _math(nt, 'MULTIPLY', mixA.outputs[0], 1.0, 100, -1240)
    # SPEC sec.3 asks for a graded BOUQUET, not wallpaper. Without a ceiling
    # the dense regions run at the tile's own alpha, which covers the red
    # almost completely and drags the flank from sat 0.82 to 0.27.
    amask = _math(nt, 'MULTIPLY', amask.outputs[0], W_ART, 240, -1240)

    # rev 14: kill the folk art on the flat tail face (selector built above).
    # Done on the ALPHA, not the colour: where alpha is 0 the base colour is
    # already the body red, so the tail face needs no colour branch of its own
    # and there is nothing that can leak.  This is why the tail did not need
    # the second image the NOSE needed.
    amask = _math(nt, 'MULTIPLY', amask.outputs[0], _notTail.outputs[0],
                  380, -1240)

    # red + gold
    mix_g = nt.nodes.new("ShaderNodeMix"); mix_g.location = (-820, -420)
    mix_g.data_type = 'RGBA'
    mix_g.inputs[6].default_value = (*RED, 1)
    if swirl.image:
        hs = nt.nodes.new("ShaderNodeHueSaturation"); hs.location = (-980, -560)
        # SPEC rev4 sec.3: gold + yellow, not pale cream wallpaper. The
        # source tile is light; 1.22 left it reading as beige on the red.
        # rev 10: was 2.45 / 0.94. Saturation 2.45 clamps S to 1.0 for EVERY
        # ink class, not just the gold -- the cream rosettes (218,181,116)
        # came out fully saturated orange and the dark brown lost its blue
        # channel entirely. The tile is now authored at the measured
        # chromaticities (gold 213,161,7; cream 218,181,116; dark 94,24,19),
        # so it must pass through untouched.
        hs.inputs["Saturation"].default_value = 1.00
        hs.inputs["Value"].default_value = 1.00
        mixC = nt.nodes.new("ShaderNodeMix"); mixC.location = (-1120, -560)
        mixC.data_type = 'RGBA'
        nt.links.new(sideY.outputs[0], mixC.inputs[0])
        nt.links.new(swirl_b.outputs["Color"], mixC.inputs[6])
        nt.links.new(swirl.outputs["Color"], mixC.inputs[7])

        # rev 11: THE NOSE FRONT FACE NEEDS ITS OWN IMAGE.
        # The flank tile is BOX-projected, so on the nose (|Nx| dominant) it is
        # sampled on (y, z) -- which lands at u 0.192-0.628, v 0.380-0.575,
        # overlapping the CAB DOOR's own flank footprint at u 0.379-0.579,
        # v 0.471-0.572 over almost the whole door band. That is why the nose
        # renders as the door's scattered comma marks where the photograph
        # shows scrollwork. Per-face UVs alone cannot fix it: the flank already
        # occupies u 0.28-1.34 of the 3.846 m period, so there is no unused
        # band to move the nose into. It needs a SECOND IMAGE.
        # tex/nose.png carries the measured wedge round both front corners
        # (gold 11.34 % against a measured 11.44, dark 2.38 against 2.42) and
        # is deliberately EMPTY in the middle of the face, which the folk-art
        # measurement records as NOT MEASURABLE. ext='CLIP' returns alpha 0
        # outside the window, so a mis-wired selector cannot leak it onto the
        # body.
        if _NOSE_SEL[0] is not None:
            isNose, nose = _NOSE_SEL[0]
            mixNC = nt.nodes.new("ShaderNodeMix"); mixNC.location = (-960, -560)
            mixNC.data_type = 'RGBA'
            nt.links.new(isNose.outputs[0], mixNC.inputs[0])
            nt.links.new(mixC.outputs[2], mixNC.inputs[6])
            nt.links.new(nose.outputs["Color"], mixNC.inputs[7])
            nt.links.new(mixNC.outputs[2], hs.inputs["Color"])
        else:
            nt.links.new(mixC.outputs[2], hs.inputs["Color"])
        nt.links.new(amask.outputs[0], mix_g.inputs[0])
        nt.links.new(hs.outputs[0], mix_g.inputs[7])
    else:
        mix_g.inputs[0].default_value = 0.0
        mix_g.inputs[7].default_value = (*GOLD, 1)

    mix_c = nt.nodes.new("ShaderNodeMix"); mix_c.location = (380, 0)
    mix_c.data_type = 'RGBA'
    nt.links.new(edge.outputs[0], mix_c.inputs[0])
    nt.links.new(mix_g.outputs[2], mix_c.inputs[6])
    mix_c.inputs[7].default_value = (*CREAM, 1)
    nt.links.new(mix_c.outputs[2], bsdf.inputs["Base Color"])

    # SPEC rev4 sec.3: WEATHERED, not show gloss. The rev-3 values
    # (rough .105, coat .75 @ .025) put a mirror clearcoat on the body, which
    # in a white studio laid an achromatic white veil over the paint -- that,
    # not the base colour, is why the red measured sat 0.37 against the
    # reference's 0.82 and read salmon. Chalky finish restores the chroma.
    bsdf.inputs["Roughness"].default_value = 0.420
    bsdf.inputs["Metallic"].default_value = 0.0
    # rev 8 (audit materials-7): was 0.21, i.e. F0 = 0.0168 / IOR 1.29. Every
    # dielectric paint is F0 ~ 0.04. Fixing an environment problem inside the
    # BSDF cost the panels all their specular structure.
    bsdf.inputs["Specular IOR Level"].default_value = float(
        os.environ.get("T1_SPEC", 0.50))
    bsdf.inputs["Coat Weight"].default_value = 0.02
    bsdf.inputs["Coat Roughness"].default_value = 0.300
    # orange peel now lives in the WEATHER group (Object coordinates, split
    # into a resolvable Bump term and a sub-pixel Roughness term)
    return m


def silver_script(name="script"):
    """Senor Tacombi -- silver signwriting, UV-mapped decal panel"""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    nt, b = _nt(m)
    tex = _img(nt, "senor.png", -420, 0)
    alpha = nt.nodes.new("ShaderNodeMath"); alpha.location = (-120, -260)
    alpha.operation = 'MULTIPLY'
    alpha.inputs[1].default_value = 1.0
    trans = nt.nodes.new("ShaderNodeBsdfTransparent"); trans.location = (200, 240)
    mixs = nt.nodes.new("ShaderNodeMixShader"); mixs.location = (740, 120)
    out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]
    if tex.image:
        nt.links.new(tex.outputs["Color"], b.inputs["Base Color"])
        nt.links.new(tex.outputs["Alpha"], alpha.inputs[0])
        nt.links.new(alpha.outputs[0], mixs.inputs[0])
    else:
        mixs.inputs[0].default_value = 0.0
    nt.links.new(trans.outputs[0], mixs.inputs[1])
    nt.links.new(b.outputs[0], mixs.inputs[2])
    nt.links.new(mixs.outputs[0], out.inputs[0])
    # rev 10.  This is silver LEAF, hand-laid on a painted panel and sixty
    # years weathered -- not silver paint.  Metallic 0.55 with a hard 0.025
    # coat was reading as grey plastic under a gloss.  Measured character it
    # has to carry: 7.4 DN of directional mottle on the untarnished leaf, with
    # a correlation length of 1.6-2.0 stroke widths ALONG the brush against
    # 0.44-0.63 across.  Mottle that lives only in base colour cannot show
    # that, because a metal's appearance is dominated by its specular; so the
    # texture's own value also drives ROUGHNESS, and the leaf reads as laid by
    # hand rather than sprayed.
    b.inputs["Roughness"].default_value = 0.260
    b.inputs["Metallic"].default_value = 0.780
    b.inputs["Coat Weight"].default_value = 0.28
    b.inputs["Coat Roughness"].default_value = 0.090
    if tex.image:
        bw = nt.nodes.new("ShaderNodeRGBToBW"); bw.location = (-240, -60)
        nt.links.new(tex.outputs["Color"], bw.inputs[0])
        rg = nt.nodes.new("ShaderNodeMapRange"); rg.location = (-80, -60)
        rg.clamp = True
        rg.inputs[1].default_value = 0.18     # deep tarnish
        rg.inputs[2].default_value = 0.72     # clean leaf
        rg.inputs[3].default_value = 0.520    # tarnish is matt
        rg.inputs[4].default_value = 0.205    # clean leaf is bright
        nt.links.new(bw.outputs[0], rg.inputs[0])
        nt.links.new(rg.outputs[0], b.inputs["Roughness"])
    m.blend_method = 'BLEND'
    m.show_transparent_back = False
    return m


def paint_calidad(name="calidad"):
    """'100% Calidad' on SOLID cream sheet metal aft of bay 3 (SPEC 0.2 and
    sec.3).  rev-3 made this frosted glass with Transmission 0.88; that is a
    retired reading and it rendered the panel 51.9 sRGB code values darker
    than the surrounding cream (55.0 % of its linear reflectance) inside a
    hard rectangular border.  It is paint, matched to T1_paint so it ages
    with the sheet metal it is painted on."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    nt, b = _nt(m)
    tex = _img(nt, "calidad.png", -420, -140)
    mix = _mixc(nt, 0.0, CREAM, CREAM, 60, 60)
    if tex.image:
        nt.links.new(tex.outputs["Alpha"], mix.inputs[0])
        nt.links.new(tex.outputs["Color"], mix.inputs[7])
    nt.links.new(mix.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.420
    b.inputs["Metallic"].default_value = 0.0
    b.inputs["Transmission Weight"].default_value = 0.0
    b.inputs["Specular IOR Level"].default_value = 0.50   # rev 8, see above
    b.inputs["Coat Weight"].default_value = 0.02
    b.inputs["Coat Roughness"].default_value = 0.300
    return m


def build_all():
    M = {}
    M["paint"] = body_paint()
    M["cream"] = simple("cream", CREAM, rough=0.13, coat=0.6, spec=0.55)
    # ---- SPEC rev4 painted-not-plated / painted-not-timber additions ----
    M["wheelcream"] = simple("wheelcream", (0.7100, 0.6900, 0.6350),
                             rough=0.34, coat=0.10, spec=0.40)
    M["bumpercream"] = simple("bumpercream", (0.7550, 0.7350, 0.6800),
                              rough=0.22, coat=0.30, spec=0.50)
    M["roundelred"] = simple("roundelred", (0.4550, 0.0720, 0.0300),
                             rough=0.26, coat=0.25, spec=0.45)
    # the literal moved to the module constant COUNTERCREAM: the upward-facing
    # dust solve is anchored on this exact albedo and the two must not drift
    M["countercream"] = simple("countercream", COUNTERCREAM,
                               rough=0.38, coat=0.06, spec=0.35)
    # rev 15, work-list item 3.  `coat` and `spec` are exposed because the
    # three-point solve on COUNTERTAN alone FAILED: driving the base colour
    # moved the measured top/fascia ratio at a gain of only 0.33-0.49, i.e. most
    # of this surface's rendered radiance is an ACHROMATIC pedestal, not its
    # albedo.  See SPEC 10.31.
    M["countertan"] = simple("countertan", COUNTERTAN,
                             rough=float(os.environ.get("T1_CTAN_RG", 0.42)),
                             coat=float(os.environ.get("T1_CTAN_CT", 0.05)),
                             spec=float(os.environ.get("T1_CTAN_SP", 0.32)))
    # chrome wears to NICKEL, so a primer-grey chip is wrong: tarnish instead
    M["chrome"] = tarnished("chrome", (0.860, 0.868, 0.880), 0.14, 0.30)
    M["chrome_d"] = tarnished("chrome_dull", (0.760, 0.768, 0.780), 0.20, 0.38)
    # rev 8 (audit materials-10): 0.004 is the Blender default and renders a
    # black mirror -- the windscreen was bimodal void+blob.
    M["glass"] = simple("glass", (0.780, 0.845, 0.815), rough=0.022,
                        transmit=1.0, ior=1.47, spec=0.35)
    M["rubber"] = dust_film("rubber", (0.0175, 0.0175, 0.0185), 0.78,
                            spec=0.22)
    M["tyre"] = dust_film("tyre", (0.0225, 0.0225, 0.0240), 0.70, spec=0.25)
    # rev 8 (audit materials-11): 0.085 / coat 0.85 was the lowest-roughness
    # non-metal in the file, on a vehicle SPEC sec.3 locks as WEATHERED. The
    # hubcaps ARE the glossiest thing on it, so this stays above the body's
    # 0.420 -- but show-gloss is retired.
    M["capred"] = simple("capred", (0.4750, 0.0290, 0.0225), rough=0.165,
                         coat=0.50, spec=0.55)
    M["capwhite"] = simple("capwhite", (0.8900, 0.8880, 0.8720), rough=0.115,
                           coat=0.7, spec=0.55)
    # rev 8: `canvas` RETIRED. It skinned a folding ragtop that SPEC sec.0.2
    # retired in rev 4; the roof is cut into rigid hinged steel lids. Removing
    # the material as well as the geometry is what stops it coming back.

    # rev 8: the lid boards. Painted board, matte, NOT emissive -- the warm
    # read in the reference is the scene light, not the paint.
    # AUDIT_rev12 item 6, severity 5 -- "the mural texture is RIGHT and the
    # render is not", settled by area means rather than class fractions
    # (8.2x minification destroys a dark tail regardless, so the class-fraction
    # limb of that finding is contaminated and was set aside):
    #
    #   ref_side.jpg, board interior   (126, 60, 24)   b-chrom 0.1129
    #   tex/lidmural.png, interior     (127, 59, 23)   b-chrom 0.1101   <- 1 code
    #   render                         (148, 92, 69)   b-chrom 0.2227
    #
    # The texture matches the photograph to ONE sRGB code per channel. The
    # render is displaced +21 R / +33 G / +46 B away from the texture's own
    # area mean, which minification cannot do. So: fix the shader. NEVER touch
    # tex/lidmural.png.
    #
    # THE MECHANISM, found by tracing the node graph: this material has no
    # additive node at all. It is 5 nodes -- Image -> Base Color, Image ->
    # RGBToBW -> MapRange -> Roughness, and a Principled. The only near-neutral
    # additive term in the chain is `img_paint`'s default `spec = 0.42`, i.e.
    # Specular IOR Level, F0 = 0.08 x 0.42 = 0.0336, with Specular Tint (1,1,1)
    # -- an achromatic white pedestal laid on top of a DARK, SATURATED albedo.
    # On a linear albedo of (0.2051, 0.0423, 0.0091) a neutral +0.03 moves
    # B by ~330 %, G by ~70 %, R by ~16 %: B most, R least, which is exactly
    # the directional signature of (127,59,23) -> (148,92,69).
    #
    # 0.16 is F0 = 0.0128, a chalky distempered board rather than a varnished
    # one, and it is a FIRST STEP, not a solve. `T1_MURAL_SPEC` overrides it so
    # the three-point solve can be run against the (126,60,24) target without
    # editing this file. The audit's instruction stands: measure it on the
    # ALBEDO pass, not on the beauty pixel -- the beauty pixel crosses AgX +
    # Punchy and an sRGB decode, and comparing a texture-file mean to a
    # tonemapped render mean crosses two nonlinear transforms.
    M["lidmural"] = img_paint("lidmural", "lidmural.png", rough=0.52,
                              spec=float(os.environ.get("T1_MURAL_SPEC", 0.16)))
    M["lidsign"] = img_paint("lidsign", "lidsign.png", rough=0.48)

    # rev 8: brass was defined locally in t1_detail._brass() because this
    # function had no brass key, which made it the last illegitimate
    # constant-roughness material in the scene. Folded in, and given a
    # roughness field like every other real surface.
    M["brass"] = tarnished("brass", (0.6600, 0.4750, 0.1750), 0.255, 0.34)

    # rev 8: the drip-rail bulb string renders unlit pearl white. In both
    # in-service photographs the bulbs are LIT and read warm -- they are the
    # brightest thing on the vehicle after the cream. Emissive, low power: they
    # are festoon bulbs in daylight, not a key light.
    M["bulb"] = emissive("bulb", (1.000, 0.760, 0.442), strength=9.0,
                         base=(0.900, 0.880, 0.840))
    M["script"] = silver_script()
    M["calidad"] = paint_calidad()
    # old D4: at 0.03 albedo the galley was a black void behind the hatches.
    # Lifted so the openings read as depth once fill_galley is on.
    M["dark"] = interior_wear("interior_dark", (0.1150, 0.1080, 0.1000), 0.78)
    M["amber"] = simple("amber", (0.9200, 0.3400, 0.0250), rough=0.09,
                        transmit=0.75, ior=1.49)
    M["ruby"] = simple("ruby", (0.7000, 0.0350, 0.0250), rough=0.09,
                       transmit=0.72, ior=1.49)
    # ------------------------------------------------- rev 45, SPEC 10.111
    # THE HEADLAMP APERTURE RENDERED AS A DARK RED HOLE, and it is the second
    # most conspicuous thing on the face of this vehicle after the roundel.
    #
    # MEASURED, in the rendered frame, by probe_rev45_nose's projected
    # landmark (no hand-typed crop box):
    #     render, unlit lens   RGB (115,  41,  33)   strongly RED
    #     photograph, unlit    RGB (124, 127, 127)   NEUTRAL   (IMG_3842,
    #                          ref_playa_34.png, the only frame in the set with
    #                          an unlit lamp square enough to read)
    # The luminance was never the defect -- lens/cream ran 0.432 built against
    # 0.565 photographed, inside any reasonable window.  THE CHROMA WAS.
    #
    # CAUSE, and it is not a tuning error.  A transmission-0.96 glass at
    # roughness 0.018 is an invisible window, and behind it sits a metal=1.0
    # bowl at roughness 0.055 -- a MIRROR.  A mirror with no bulb in front of
    # it returns an image of whatever surrounds it, which here is the red nose.
    # So the aperture faithfully renders a red panel reflected in a parabola.
    #
    # A 1963 T1 headlamp lens is MOULDED PRISMATIC GLASS -- fluted, not
    # polished -- and the flutes are what make a real lamp read as a bright
    # grey disc from any angle.  Modelling each flute at 0.086 m radius is not
    # this revision's brief; a rough transmissive glass is the honest proxy for
    # a diffuser and it is LABELLED as a proxy rather than passed off as the
    # part.  The reflector is roughened with it, because without a bulb the
    # specular arm of a mirror bowl has nothing correct to return.
    #
    # BOTH ARE OVERRIDABLE so the retired arm can still be rendered for
    # comparison, which is this project's standing pattern for a retirement
    # (cf. W_DUST_FAC_UP / T1_W_DUP, SPEC 10.82):
    #     T1_HL_LENS_RG=0.018 T1_HL_REFL_RG=0.055   restores the mirror arm.
    M["lens"] = simple("lens", (0.900, 0.918, 0.930),
                       rough=float(os.environ.get("T1_HL_LENS_RG", 0.018)),
                       transmit=0.96, ior=1.52, spec=0.42)
    # sealed inside the lamp bowl -- nothing weathers it
    M["reflector"] = simple("reflector", (0.960, 0.962, 0.968),
                            rough=float(os.environ.get("T1_HL_REFL_RG", 0.055)),
                            metal=1.0)
    # brushed galley stainless, not a mirror: at rough 0.28 in an unlit box
    # the hatches filled with specular blobs instead of reading as an interior
    M["steel"] = interior_wear("steel", (0.560, 0.562, 0.568), 0.46, metal=1.0)

    # ------------------------------------------------------- weathering
    # full group: colour breakup + edge wear + dust + fade + orange peel
    # rev 14: `fadev` is the vertical-surface sun-fade term (WEATHER's new
    # FadeVert input).  It is the diffuse view factor of a vertical plane to a
    # uniform hemisphere, 0.50, and it is switched on ONLY for the cream
    # family -- the surfaces the -55 % chroma fade was actually measured on
    # (ref_side.jpg, cream corner panel X -1.60..-1.84).  `paint`,
    # `roundelred`, `capred` and `script` stay at 0.0 because SPEC 10.12 locks
    # RED's albedo saturation at 0.816 and W_FADE_SAT = 0.88 would move it.
    # `calidad` stays at 0.0 for the same reason -- it is a red-orange decal
    # whose gradient was measured, not designed.  See weather_group() 2d.
    # rev 19: exposed for ABLATION.  The standing rule is to ablate a constant
    # to zero and re-measure BEFORE scheduling a solve on it -- `W_ALBEDO` cost
    # three revisions for want of one render.  This is the fade path the cream
    # mottle map is about to modulate spatially, so its authority over the
    # rendered cream has to be demonstrated, not assumed.  Default unchanged.
    FADEV_CREAM = float(os.environ.get("T1_FADEV", 0.50))
    # rev 19: `paint` alone takes the mottle map, LINKED from the node
    # `body_paint` built and already multiplied by its own two-tone selector.
    # `roundelred` and `calidad` keep 0.0 -- they carry no cream at all.
    apply_weather(M["paint"], dust=1.0, wear=WEAR[M["paint"].name],
                  fade=1.0, peel=1.0, fadev_from="FADEV_MOTTLE",
                  faderough=MOTTLE_RGH_K)
    for k in ("roundelred", "calidad"):
        apply_weather(M[k], dust=1.0, wear=WEAR[M[k].name], fade=1.0, peel=1.0)
    apply_weather(M["bumpercream"], dust=1.0, wear=WEAR[M["bumpercream"].name],
                  fade=1.0, peel=1.0, fadev=FADEV_CREAM)
    apply_weather(M["cream"], dust=1.0, wear=WEAR[M["cream"].name],
                  fade=1.0, peel=1.0, fadev=FADEV_CREAM)
    # group minus peel (not sprayed sheet metal), dust weighted up
    #
    # rev 20, SPEC 10.56: `countertan`'s dust is now overridable so it can be
    # ABLATED.  The interreflection test measured that ~70 % of the counter
    # top's rendered radiance does NOT come from `COUNTERTAN` -- a 96.6 %
    # albedo cut moves it only 29.6 % -- and interreflection (9.0/8.2/6.0 %)
    # and coat+spec (2.3-5.6 %, 10.31c) are both far too small to account for
    # it.  `W_DUST_COL_UP` is a settled-ochre film whose colour is INDEPENDENT
    # of the base albedo by construction, so a high-coverage dust mix is the
    # remaining candidate and this is the lever that tests it.  Default 1.4 is
    # unchanged, so the shipped build is untouched.
    # rev 20: `wear` is overridable for the same reason and it is the next
    # candidate after dust was excluded.  The chip path replaces the shaded
    # colour with W_PRIMER and then W_STEEL -- both CONSTANTS, independent of
    # the base albedo -- so a high wear on an upward-facing panel is exactly
    # the shape of a base-independent pedestal.  `countertan` carries
    # WEAR = 0.7, the joint-highest on the vehicle.  Defaults unchanged.
    _CTAN_DUST = float(os.environ.get("T1_CTAN_DUST", 1.4))
    _CTAN_WEAR = float(os.environ.get("T1_CTAN_WEAR",
                                      WEAR[M["countertan"].name]))
    apply_weather(M["countertan"], dust=_CTAN_DUST, wear=_CTAN_WEAR,
                  fade=float(os.environ.get("T1_CTAN_FADE", 1.0)), peel=0.0)
    apply_weather(M["capred"], dust=0.30, wear=WEAR[M["capred"].name],
                  fade=0.25, peel=0.0)
    # rev 44 -- DUST 1.4 -> 0.30, FADE 1.0 -> 0.25.  The owner reported the red
    # hubcaps reading wrong off the hero.  The SIZE is right -- CAP_R is locked
    # against a 302-ray circle fit at sd 0.79 px, 0.4134 photographed against
    # 0.4211 built -- but the COLOUR is not, and that is what reads as bulk.
    # Measured G/R on the cap, model against TWO independent reference frames
    # that agree with each other to 0.002 (ref_side.jpg rear wheel 0.230,
    # ref_nolita_doorshut.jpg 0.228 -- different cameras, different eras):
    #     shipped  dust 1.4 fade 1.0 ....... 0.598      +0.368 off
    #     dust 0.30 fade 0.25 ............... 0.401      +0.171
    #     weather FULLY OFF ................. 0.309      +0.079
    #     TARGET ............................ 0.230
    # Weather is the WHOLE story -- and it ran the wrong way: the shipped cap
    # was more bleached than a perfectly clean one would be, so weathering was
    # not adding grime, it was adding WHITE.  Cutting it halves the error.
    # A RESIDUAL REMAINS AND IS NOT TUNED AWAY: even at zero weather the render
    # sits at 0.309 against 0.230, so ~22 % of the gap is lighting/specular,
    # not weather.  Dropping the clearcoat was tried (coat 0.50 -> 0.12, spec
    # 0.55 -> 0.35) and made it WORSE, 0.378 -- so the coat is not the lever
    # and it is restored exactly as shipped.  The residual needs a lighting
    # pass, and tuning dust further to hide it would be laundering.
    for k in ("countercream", "wheelcream", "capwhite"):
        apply_weather(M[k], dust=1.4, wear=WEAR[M[k].name], fade=1.0, peel=0.0,
                      fadev=FADEV_CREAM)
    # hand-painted silver: inherit the panel's dust and roughness field so it
    # does not float, but chip the paint UNDER it, not the silver
    apply_weather(M["script"], dust=1.0, wear=0.0, fade=0.5, peel=0.0)

    # ------------------------------------ the constant-roughness offenders
    # STATE.md counted 9 and allows exactly two classes through: transmissive,
    # and the sealed reflector.  Adjudicated one at a time, not as a batch:
    #
    #   glass  transmit 1.00 | EXEMPT.  Roughness on a transmissive BSDF is
    #   amber  transmit 0.75 | refraction blur, not a surface finish, and all
    #   ruby   transmit 0.72 | four are moulded/float glass whose finish comes
    #   lens   transmit 0.96 | off a tool, not off sixty years of weather.
    #                          Neither photograph resolves a lens: the ruby
    #                          tail lamp is 45.5 x 27.0 mm, i.e. 9.6 x 5.7 px
    #                          at the 211.4 px/m measured off the rear rim
    #                          flange in ref_side.jpg, so there is nothing to
    #                          measure a field against and inventing one would
    #                          only add refraction noise.
    #   reflector             | EXEMPT, and STATE names it: sealed inside the
    #                           lamp bowl behind `lens`, so nothing reaches it.
    #   gal_sky               | EXEMPT, and it is the one exemption STATE does
    #                           NOT anticipate, so it is argued rather than
    #                           claimed.  It is not a surface of this vehicle:
    #                           t1_detail builds it as an emissive stand-in for
    #                           the roof aperture `t1_shell` does not cut.  It
    #                           radiates at 0.90 with Specular IOR Level 0.05,
    #                           i.e. F0 = 0.004, so its Roughness input steers
    #                           0.4 % of a lobe on a panel that is dominated by
    #                           its own emission -- below the render's noise
    #                           floor.  A roughness field there is microstructure
    #                           invented for a HOLE.  When the roof aperture is
    #                           actually cut, this material should be deleted,
    #                           not given a field.
    #
    # The other three are real surfaces and get a field.
    # feature sizes are 1/scale in metres and are set from each fitting's own
    # size, not copied: a salt film on a 22 mm envelope cannot carry the same
    # grain as a 2.08 m tube.
    rough_field("bulb", scale=520.0)          # r 11 mm envelope -> 1.9 mm
    rough_field("gal_tube", scale=130.0)      # 2.08 m diffuser  -> 7.7 mm
    rough_field("gal_menucard", scale=260.0,  # 96 x 311 mm card -> 3.8 mm
                albedo_w=W_ROUGH_SWING * 0.5)
    return M


# ===========================================================================
# rev 44 -- ROUNDED EDGES ON EVERY SHADER.  SPEC 10.103.
#
# THE OWNER SET THE BAR WITH A CATALOGUE-GRADE PRODUCT RENDER and asked for
# that level of fidelity.  `probe_rev44_fidelity.py` counted what actually
# separates this model from one: **66 566 edges over 28 degrees, and ZERO
# bevel modifiers in 190 objects.**  Every one of those is a mathematically
# knife-sharp edge, and a knife edge is the single loudest tell in computer
# graphics -- no real pressed, cast or extruded part has one.  A real edge
# carries a fold radius, that radius catches a thin specular highlight, and
# THAT HIGHLIGHT IS MOST OF WHAT THE EYE READS AS "a photographed object".
#
# WHY THIS IS DONE IN THE SHADER AND NOT WITH A BEVEL MODIFIER.  A Bevel
# modifier MOVES VERTICES.  This model's geometry is measured -- the tightest
# clearance in it is 0.85 mm (the front arch's rear-most point against the cab
# door's rear edge, SPEC 10.102.4) and roughly forty asserts are armed on
# distances of a few millimetres.  A 2.75 mm chamfer applied to a
# boolean-heavy 250 000-vertex shell would move measured surfaces, could not
# be proven not to, and historically breaks exactly the booleans this shell
# spent six revisions recovering from.
#
# Cycles' Bevel node perturbs the SHADING NORMAL by ray-tracing the local
# surface.  It cannot move a vertex -- there is no code path by which it
# could -- so it is the one way to buy this at zero risk to a measured model.
# The silhouette stays sharp, which is correct at this scale anyway: at 600
# px/m a 2.75 mm fold is 1.6 px, so it belongs in the shading and not in the
# outline.
#
# THE RADIUS IS DERIVED, NOT CHOSEN (10.25's rule).  `t1_shell.GAPW` is the
# panel-gap width, 5.5 mm, MEASURED.  A shut line is two folded panel edges
# facing each other across that gap, so each fold's radius cannot exceed HALF
# THE GAP or the two folds meet and the gap closes.  GAPW/2 is therefore the
# geometric CEILING on a fold radius in this vehicle, expressed in terms of
# the measured constant rather than typed, so re-measuring the gap moves it.
#
# IT COMPOSES WITH THE WEATHER GROUP RATHER THAN REPLACING IT.  Where a
# material already drives Principled.Normal -- every painted panel does, from
# WEATHER's internal Bump -- that source is re-routed into the Bevel node's
# own Normal input, so the orange-peel bump is rounded rather than discarded.
# Where nothing drives it, the Bevel drives it directly.
#
# IDEMPOTENT AND ABLATABLE.  A second call is a no-op (the Bevel node is
# looked for by type).  `T1_NOBEVEL=1` stands the whole pass down, so the A/B
# is one environment variable and needs no edit -- rev 20's pattern.
# ===========================================================================
BEVEL_SAMPLES = int(os.environ.get("T1_BEVEL_SAMPLES", "8"))


def round_edges(radius=None, log=None):
    """Splice a Cycles Bevel node into every Principled BSDF's Normal input.

    Returns (patched, skipped_no_bsdf, already_had_one).
    """
    if os.environ.get("T1_NOBEVEL"):
        if log:
            log("  round_edges: STOOD DOWN by T1_NOBEVEL")
        return (0, 0, 0)
    if radius is None:
        import t1_shell as _SH
        radius = _SH.GAPW / 2.0            # 10.25: expressed, never typed
    done = skip = had = 0
    for m in bpy.data.materials:
        if not m.users or not m.use_nodes or m.node_tree is None:
            continue
        nt = m.node_tree
        b = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if b is None:
            skip += 1
            continue
        if any(n.type == 'BEVEL' for n in nt.nodes):
            had += 1
            continue
        x0 = min([n.location[0] for n in nt.nodes] or [0.0])
        bev = nt.nodes.new("ShaderNodeBevel")
        bev.location = (b.location[0] - 300.0, b.location[1] - 620.0)
        bev.samples = BEVEL_SAMPLES
        bev.inputs["Radius"].default_value = radius
        ns = b.inputs["Normal"]
        if ns.links:
            nt.links.new(ns.links[0].from_socket, bev.inputs["Normal"])
        nt.links.new(bev.outputs[0], ns)
        done += 1
    if log:
        log("  round_edges: %d materials given a %.2f mm fold radius "
            "(%d already had one, %d have no Principled)"
            % (done, radius * 1000.0, had, skip))
    return (done, skip, had)


def assign(ob, mat):
    ob.data.materials.clear()
    ob.data.materials.append(mat)
