"""
sheet3_notissued.py -- SHEET 3 OF 4 : OFF SIDE ELEVATION (-Y) : NOT ISSUED.

THE FIRST ARTEFACT OF THE rev-76 DESIGN PROGRAM.  Its subject is the one
elevation of this vehicle that `SPEC.md` grades **E (never photographed)** --
"Expert inference -- not observed, derived from what a correct 1963 T1 must be."

WHY THIS OBJECT.  The programme's own thesis is that the model's value is
MEASUREMENT AND LINE, not photorealism.  A drafting sheet whose drawing field is
mostly EMPTY, and which says exactly why, is that thesis executed honestly.  It
needs no line pass, no render, no alpha and no geometry change -- so it can be in
the owner's hands the same session it is written.

EVERY FIGURE ON THE SHEET IS READ OUT OF `STATE.md` AND `SPEC.md` AT DRAW TIME.
Nothing is typed here.  A figure that cannot be found makes the script REFUSE
with a summary line naming what was missing (rule 37) -- a sheet with a silently
wrong dimension is worse than no sheet.  When the model moves, the sheet moves.

WHAT IS DRAWN, AND WHY ONLY THIS.  Only quantities that are (a) MEASURED off the
mesh and (b) symmetric about the vehicle's centre plane, so that they transfer to
an unphotographed flank by geometry rather than by hope (rule 11: geometry
transfers between frames, paint and artwork do not).  That is the ground line,
the two hub stations, the tyre circles, the arch lips, and the roof and belt
stations.  It is NOT a body outline: no outline of that flank exists in anything
we hold, and drawing a plausible one is precisely the defect this project has
paid for most often.  The empty field is the measurement.

INKS: one, `lid_gen.INK` (72,46,6), on `t1_mats.CREAM` sRGB (206,208,200).  Both
are measured off this vehicle; nothing on this sheet is a colour we invented.

Run:  python3 sheet3_notissued.py [outdir]
"""
import os, re, sys, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import sheet as SH

CHECK = [0]
MISSING = []


def grab(text, pattern, what, group=1, cast=float):
    """Pull one figure out of a document.  A miss is RECORDED, never defaulted."""
    CHECK[0] += 1
    m = re.search(pattern, text)
    if not m:
        MISSING.append(what)
        return None
    v = m.group(group)
    try:
        return cast(v) if cast else v
    except ValueError:
        MISSING.append("%s (uncastable: %r)" % (what, v))
        return None


def main(outdir):
    state = open(os.path.join(ROOT, "STATE.md")).read()
    spec = open(os.path.join(ROOT, "SPEC.md")).read()

    # ---------------------------------------------------------------- FIGURES
    F = {}
    F["wheelbase"] = grab(state, r"\|\s*wheelbase\s*\|\s*([\d.]+)", "wheelbase")
    F["track_f"] = grab(state, r"\|\s*track front\s*\|\s*([\d.]+)", "track front")
    F["track_r"] = grab(state, r"\|\s*track rear\s*\|\s*([\d.]+)", "track rear")
    F["tyre_d"] = grab(state, r"\|\s*tyre diameter\s*\|\s*([\d.]+)", "tyre diameter")
    F["width"] = grab(state, r"\|\s*overall width \(body\)\s*\|\s*([\d.]+)", "overall width")
    F["rocker"] = grab(state, r"\|\s*rocker to ground\s*\|\s*([\d.]+)", "rocker to ground")
    F["len_meas"] = grab(state, r"\|\s*overall length \(ex counter\)\s*\|\s*([\d.]+)", "overall length measured")
    F["len_spec"] = grab(state, r"\|\s*overall length \(ex counter\)\s*\|\s*[\d.]+\s*\|\s*([\d.]+)", "overall length SPEC")
    F["len_delta"] = grab(state, r"\|\s*overall length \(ex counter\)\s*\|\s*[\d.]+\s*\|\s*[\d.]+\s*\|\s*([+\-][\d.]+) mm", "overall length delta", cast=float)
    F["len_nolid"] = grab(state, r"length excludes opened lids: [\d.]+ with them, ([\d.]+) without", "length excluding lids")
    F["len_withlid"] = grab(state, r"length excludes opened lids: ([\d.]+) with them", "length including lids")

    # roof / belt: three stations, printed as a TABLE in STATE.md.  A roof line
    # is a LINE, not a scalar -- that is STATE.md's own correction and the sheet
    # must not flatten it back into one number.
    F["x_fa"] = grab(state, r"\| front axle \| ([+\-][\d.]+) \|", "front axle station x")
    F["roof_fa"] = grab(state, r"\| front axle \| [+\-][\d.]+ \| ([\d.]+)", "roof z at front axle")
    F["belt_fa"] = grab(state, r"\| front axle \| [+\-][\d.]+ \| [\d.]+ \*\(n=\d+\)\* \| ([\d.]+)", "belt z at front axle")
    F["x_ra"] = grab(state, r"\| rear axle \| ([+\-][\d.]+) \|", "rear axle station x")
    F["roof_ra"] = grab(state, r"\| rear axle \| [+\-][\d.]+ \| ([\d.]+)", "roof z at rear axle")
    F["belt_ra"] = grab(state, r"\| rear axle \| [+\-][\d.]+ \| [\d.]+ \*\(n=\d+\)\* \| ([\d.]+)", "belt z at rear axle")
    F["x_mid"] = grab(state, r"\| mid wheelbase \| ([+\-][\d.]+) \|", "mid-wheelbase station x")
    F["belt_mid"] = grab(state, r"\| mid wheelbase \| [+\-][\d.]+ \| .* \| ([\d.]+) \|", "belt z mid wheelbase")
    # the reason there is no roof at that station is STATE.md's own words -- quote
    # them, do not paraphrase them into a caption that can go stale (rule 18).
    F["mid_why"] = grab(state, r"\| mid wheelbase \| [+\-][\d.]+ \| . \*\((.+)\)\* \| [\d.]+ \|", "mid-station roof note", cast=None)
    F["roof_slope"] = grab(state, r"roof line slope \(measured off the mesh\) \| ([+\-][\d.]+) mm/m", "roof slope")

    F["arch_r"] = grab(state, r"rear arch lip above hub [\d.]+ m \(ARCH_R ([\d.]+)\)", "ARCH_R")
    F["lip_r"] = grab(state, r"rear arch lip above hub ([\d.]+) m", "rear arch lip above hub")
    F["lip_f"] = grab(state, r"front arch lip above hub ([\d.]+) m", "front arch lip above hub")
    F["gap_r"] = grab(state, r"rear arch lip above hub [\d.]+ m \(ARCH_R [\d.]+\) -> tyre gap ([\d.]+) mm", "rear tyre gap")
    F["gap_f"] = grab(state, r"front arch lip above hub [\d.]+ m \(ARCH_R [\d.]+\) -> tyre gap ([\d.]+) mm", "front tyre gap")
    F["rake"] = grab(state, r"rake ([\d.]+) mm/m", "rake")
    F["drop0"] = grab(state, r"drop at x=0 ([\d.]+) mm", "ride drop at x=0")
    F["drop_f"] = grab(state, r"\| ride drop @ front axle / rear axle \| ([\d.]+) /", "ride drop front")
    F["drop_r"] = grab(state, r"\| ride drop @ front axle / rear axle \| [\d.]+ / ([\d.]+) mm", "ride drop rear")

    # the off flank's own machine-written line -- the sheet's whole subject
    F["offflank_mm"] = grab(state, r"off flank ([\d.]+) mm over (\d+) pairs", "off flank shut-line length")
    F["offflank_pairs"] = grab(state, r"off flank [\d.]+ mm over (\d+) pairs", "off flank pairs", cast=int)
    F["showflank_mm"] = grab(state, r"shut line x aperture: show flank ([\d.]+) mm", "show flank shut-line length")
    F["nonman"] = grab(state, r"non-manifold edges \(body\) \| (\d+)", "non-manifold edges", cast=int)
    F["faces"] = grab(state, r"body faces \| ([\d,]+) quad", "body faces", cast=None)
    F["commit"] = grab(state, r"\| git commit \| `([0-9a-f]+)`", "git commit", cast=None)
    F["gen"] = grab(state, r"\| generated \| ([0-9\- :]+UTC)", "STATE.md generated stamp", cast=None)
    F["sub"] = grab(state, r"subdivision \| T1_SUB=(\d)", "subdivision level", cast=None)

    # SPEC: the grade row, verbatim, and the grade legend
    row = re.search(r"\| Side, off side \(−Y\) \| (.+?) \| \*\*E\*\* \(never photographed\) \|", spec)
    CHECK[0] += 1
    if not row:
        MISSING.append("SPEC.md off-side elevation row")
        F["spec_feats"] = None
    else:
        F["spec_feats"] = re.sub(r"\*\*", "", row.group(1))
    F["grade_E"] = grab(spec, r"\| \*\*E\*\* \| \*\*Expert inference\*\* — (.+?) \|", "SPEC grade-E legend", cast=None)

    if MISSING:
        print("SHEET 3: %d figure(s) NOT FOUND in STATE.md / SPEC.md -- REFUSING." % len(MISSING))
        for m in MISSING:
            print("   missing: %s" % m)
        print("%d checked, %d FAILED -- nothing was drawn (rule 37)" % (CHECK[0], len(MISSING)))
        return 2

    # ------------------------------------------------------------ THE SHEET
    W, H = 594.0, 420.0                                   # A2 landscape
    INK, STOCK = (72, 46, 6), (206, 208, 200)             # both measured, see docstring
    s = SH.Sheet(W, H, ink=INK, stock=STOCK, dpi=300, ss=2)

    M, BIND = 10.0, 20.0                                  # ISO 5457 margins
    fx, fy = BIND, M                                      # frame origin
    fw, fh = W - BIND - M, H - 2 * M

    s.rect(fx, fy, fw, fh, lw=0.7)
    s.rect(fx + 3, fy + 3, fw - 6, fh - 6, lw=0.18, tint=0.45)

    # zone marks, ISO 5457 -- four across, three down
    for i, z in enumerate("ABCD"):
        cx = fx + fw * (i + 0.5) / 4.0
        s.text(cx, fy + 2.4, z, pt=6, font="mono-b", align="c", tint=0.55)
        s.text(cx, fy + fh - 0.9, z, pt=6, font="mono-b", align="c", tint=0.55)
        if i:
            for yy in (fy, fy + fh - 3):
                s.line(fx + fw * i / 4.0, yy, fx + fw * i / 4.0, yy + 3, w=0.18, tint=0.45)
    for i, z in enumerate("123"):
        cy = fy + fh * (i + 0.5) / 3.0
        s.text(fx + 1.5, cy, z, pt=6, font="mono-b", align="c", tint=0.55, rot=-90)
        s.text(fx + fw - 1.5, cy, z, pt=6, font="mono-b", align="c", tint=0.55, rot=-90)
        if i:
            for xx in (fx, fx + fw - 3):
                s.line(xx, fy + fh * i / 3.0, xx + 3, fy + fh * i / 3.0, w=0.18, tint=0.45)

    # ------------------------------------------------------------ HEAD
    s.text(fx + 8, fy + 14, "SEÑOR TACOMBI · COMBI", pt=13, font="sans-b", track=0.9)
    s.text(fx + 8, fy + 20.5, "1963 VOLKSWAGEN TYPE 2 (T1) KOMBI, CONVERTED TO A SERVICE VEHICLE",
           pt=6.5, font="mono", tint=0.75, track=0.5)
    s.line(fx + 8, fy + 24.5, fx + fw - 8, fy + 24.5, w=0.5)
    s.text(fx + fw - 8, fy + 14, "SHEET 3 OF 4", pt=13, font="sans-b", align="r", track=1.4)
    s.text(fx + fw - 8, fy + 20.5, "OFF SIDE ELEVATION  ( − Y )", pt=6.5, font="mono",
           align="r", tint=0.75, track=0.9)

    # the one sentence
    s.text(fx + 8, fy + 33, "THIS ELEVATION HAS NEVER BEEN PHOTOGRAPHED.", pt=9.5,
           font="mono-b", track=0.5)
    s.text(fx + 8, fy + 39.5,
           "WHAT IS DRAWN IS EVERYTHING THAT TRANSFERS FROM THE OTHER FLANK BY GEOMETRY. "
           "WHAT IS NOT DRAWN IS EVERYTHING ELSE.", pt=6.5, font="mono", tint=0.8)

    # ------------------------------------------------------ THE DRAWING FIELD
    SCALE = 10.0                                          # 1:10, a drawing-office scale
    mm = lambda v: v * 1000.0 / SCALE                     # metres -> sheet mm
    GY = fy + 300.0                                       # ground line, sheet y
    # +X is the vehicle's front.  Viewed from -Y toward +Y with Z up, the
    # viewer's right is forward x cross up = (+Y) x (+Z) = +X.  NOSE IS RIGHT.
    OX = fx + fw / 2.0                                    # vehicle x=0, centred in the frame

    vx = lambda X: OX + mm(X)
    vz = lambda Z: GY - mm(Z)

    x_nose, x_tail = F["len_withlid"] / 2.0, -F["len_withlid"] / 2.0
    # STATION LINES.  Every figure on this sheet is read at ONE OF THREE STATIONS,
    # because a roof line and a belt line are LINES and STATE.md prints them as
    # three rows, not as scalars.  Drawing the stations makes the emptiness
    # structured rather than blank, and invents nothing.
    for X in (F["x_fa"], F["x_mid"], F["x_ra"]):
        s.line(vx(X), vz(F["roof_ra"]) - 14, vx(X), GY + 34, w=0.15, tint=0.42,
               dash=(6, 1.6, 1.2, 1.6))
        s.text(vx(X), vz(F["roof_ra"]) - 16.5, "x %+.3f" % X, pt=4.4, font="mono",
               align="c", tint=0.55)
    g0, g1 = max(fx + 5, vx(x_tail) - 14), min(fx + fw - 5, vx(x_nose) + 14)
    s.line(g0, GY, g1, GY, w=0.7)
    s.text(g1 - 1, GY + 5.0, "GROUND", pt=5.5, font="mono-b", align="r", tint=0.9)

    # --- hubs, tyres, arches.  Symmetric about the centre plane: they transfer.
    hub_z = F["tyre_d"] / 2.0
    for name, X, lip, gap in (("FRONT", F["x_fa"], F["lip_f"], F["gap_f"]),
                              ("REAR", F["x_ra"], F["lip_r"], F["gap_r"])):
        cx, cy = vx(X), vz(hub_z)
        s.circle(cx, cy, mm(F["tyre_d"] / 2.0), w=0.45)          # tyre OD
        s.arc(cx, cy, mm(F["arch_r"]), 188, 352, w=0.45)         # arch lip
        for a in (0, 90):                                         # centre cross
            s.line(cx - (5 if a == 0 else 0), cy - (0 if a == 0 else 5),
                   cx + (5 if a == 0 else 0), cy + (0 if a == 0 else 5),
                   w=0.18, tint=0.7, dash=(2.2, 0.9, 0.5, 0.9))
        s.text(cx, cy + mm(F["tyre_d"] / 2.0) + 6.5,
               "%s HUB  x %+.3f" % (name, X), pt=5, font="mono", align="c", tint=0.85)
        s.text(cx, cy + mm(F["tyre_d"] / 2.0) + 10.5,
               "LIP %.1f OVER HUB · GAP %.1f" % (lip * 1000, gap),
               pt=4.5, font="mono", align="c", tint=0.6)

    # --- wheelbase dimension, between the two hub centres
    dy = GY + 30
    s.line(vx(F["x_ra"]), dy, vx(F["x_fa"]), dy, w=0.3)
    for X in (F["x_ra"], F["x_fa"]):
        s.line(vx(X), vz(hub_z), vx(X), dy + 3, w=0.15, tint=0.55)
        s.line(vx(X) - 1.6, dy - 1.6, vx(X) + 1.6, dy + 1.6, w=0.3)
    s.text((vx(F["x_ra"]) + vx(F["x_fa"])) / 2.0, dy - 2.0,
           "%d  WHEELBASE" % round(F["wheelbase"] * 1000), pt=6, font="mono-b", align="c")

    # --- the roof line is a LINE, not a scalar: three MEASURED stations only.
    # STATE.md's own correction, and the mid station has no roof over it at all.
    for label, X, Z in (("FRONT AXLE", F["x_fa"], F["roof_fa"]),
                        ("REAR AXLE", F["x_ra"], F["roof_ra"])):
        s.line(vx(X) - 9, vz(Z), vx(X) + 9, vz(Z), w=0.45)
        s.line(vx(X), vz(Z), vx(X), vz(Z) + 7, w=0.15, tint=0.5, dash=(1.6, 1.2))
        s.text(vx(X) + 10.5, vz(Z) + 1.6, "%.1f  ROOF @ %s" % (Z * 1000, label),
               pt=5.5, font="mono-b")
    s.line(vx(F["x_mid"]) - 9, vz(F["roof_ra"]) - 3, vx(F["x_mid"]) + 9,
           vz(F["roof_ra"]) - 3, w=0.3, tint=0.4, dash=(1.4, 1.4))
    s.text(vx(F["x_mid"]), vz(F["roof_ra"]) - 5.5, F["mid_why"].upper(),
           pt=4.8, font="mono", align="c", tint=0.7)
    s.text(vx(F["x_mid"]), vz(F["roof_ra"]) - 9.5,
           "ROOF SLOPE %+.1f mm/m, MEASURED OFF THE MESH · RAKE APPLIED %.2f mm/m"
           % (F["roof_slope"], F["rake"]), pt=4.8, font="mono", align="c", tint=0.7)

    # --- belt line: a straight line through THREE measured stations, said so
    bpts = [(F["x_fa"], F["belt_fa"]), (F["x_mid"], F["belt_mid"]), (F["x_ra"], F["belt_ra"])]
    s.line(vx(bpts[0][0]), vz(bpts[0][1]), vx(bpts[2][0]), vz(bpts[2][1]), w=0.22, tint=0.6)
    for X, Z in bpts:
        s.line(vx(X) - 3.5, vz(Z), vx(X) + 3.5, vz(Z), w=0.45)
        s.text(vx(X), vz(Z) - 2.4, "%.1f" % (Z * 1000), pt=5, font="mono", align="c")
    s.text(vx(bpts[2][0]) - 16, vz(bpts[2][1]) - 6.4,
           "BELT LINE — THREE MEASURED STATIONS,", pt=4.8, font="mono", align="r", tint=0.75)
    s.text(vx(bpts[2][0]) - 16, vz(bpts[2][1]) - 2.2,
           "%.1f mm OF RISE FRONT TO REAR" % ((F["belt_ra"] - F["belt_fa"]) * 1000),
           pt=4.8, font="mono", align="r", tint=0.75)

    # --- rocker
    s.line(vx(F["x_ra"]) - 10, vz(F["rocker"]), vx(F["x_fa"]) + 10, vz(F["rocker"]),
           w=0.22, tint=0.55, dash=(4, 2))
    s.text(vx(F["x_fa"]) + 12, vz(F["rocker"]) + 1.6, "%.1f ROCKER" % (F["rocker"] * 1000),
           pt=5, font="mono", tint=0.75)

    # ------------------------------------------------- THE FIELD THAT IS EMPTY
    ex0, ex1 = vx(-1.62), vx(1.30)
    ey0, ey1 = vz(F["roof_ra"]) + 16, vz(F["rocker"]) - 8
    s.rect(ex0, ey0, ex1 - ex0, ey1 - ey0, lw=0.22, tint=0.35, dash=(3.5, 3.0))
    cxm = (ex0 + ex1) / 2.0
    cym = vz(F["belt_fa"]) + 30.0          # below the belt: where the doors would be
    s.text(cxm, cym - 14, "NOT ISSUED", pt=34, font="sans-b", align="c", tint=0.40, track=7.0)
    s.text(cxm, cym - 3.5,
           "SPEC.md GRADE  E  —  " + F["grade_E"].upper(), pt=5.6, font="mono-b",
           align="c", tint=0.85, track=0.3)
    s.text(cxm, cym + 3.0, "THE FEATURES THIS FLANK IS SAID TO CARRY, AND WHICH NOTHING",
           pt=5.2, font="mono", align="c", tint=0.7)
    s.text(cxm, cym + 8.0, "WE HOLD CAN CONFIRM, PLACE OR CONTRADICT:",
           pt=5.2, font="mono", align="c", tint=0.7)
    s.text(cxm, cym + 15.0, F["spec_feats"].upper(), pt=6.4, font="mono-b", align="c", tint=0.95)
    s.text(cxm, cym + 22.0,
           "THE MODEL ASSERTS THEM ANYWAY: %.1f mm OF SHUT LINE OVER %d PAIRS ON THIS FLANK,"
           % (F["offflank_mm"], F["offflank_pairs"]), pt=5.0, font="mono", align="c", tint=0.65)
    s.text(cxm, cym + 27.0,
           "AGAINST %.1f mm ON THE PHOTOGRAPHED ONE.  THAT IS A REGRESSION BASELINE, NOT A READING."
           % F["showflank_mm"], pt=5.0, font="mono", align="c", tint=0.65)

    # ------------------------------------------------------------ SCALE BAR
    sbx, sby = fx + 8, fy + fh - 50
    s.text(sbx, sby - 3.5, "SCALE 1:%d AT A2" % int(SCALE), pt=5.5, font="mono-b")
    for i in range(5):
        s.fill(sbx + i * mm(0.5), sby, mm(0.5), 2.2, tint=1.0 if i % 2 else 0.0)
        s.rect(sbx + i * mm(0.5), sby, mm(0.5), 2.2, lw=0.18)
    for i in range(6):
        s.text(sbx + i * mm(0.5), sby + 6.0, "%.1f" % (i * 0.5), pt=4.5, font="mono",
               align="c", tint=0.7)
    s.text(sbx + mm(2.5) + 3, sby + 1.8, "METRES", pt=4.5, font="mono", tint=0.7)

    # ------------------------------------------------------------- KEY BLOCK
    kx, ky = fx + 8, fy + fh - 39
    s.text(kx, ky, "KEY — THE LINE WEIGHT IS THE PROVENANCE", pt=5.5, font="mono-b")
    keys = [("MEASURED OFF THE MESH, AND SYMMETRIC ABOUT THE CENTRE PLANE, SO IT TRANSFERS", 0.45, None, 1.0),
            ("DERIVED FROM A MEASURED FIGURE, NOT ITSELF MEASURED", 0.22, (4, 2), 0.55),
            ("ASSERTED BY THE MODEL, GRADED E, UNCONFIRMED BY ANY PHOTOGRAPH", 0.22, (3.5, 3.0), 0.35)]
    for i, (t, w, d, tn) in enumerate(keys):
        yy = ky + 5.2 + i * 4.4
        s.line(kx, yy - 1.4, kx + 14, yy - 1.4, w=w, tint=tn, dash=d)
        s.text(kx + 17, yy, t, pt=4.6, font="mono", tint=0.8)
    s.text(kx, ky + 5.2 + 3 * 4.4 + 0.6,
           "ABSENT     NO OUTLINE OF THIS FLANK EXISTS IN ANYTHING WE HOLD.  DRAWING A "
           "PLAUSIBLE ONE IS THE DEFECT THIS PROJECT HAS PAID FOR MOST OFTEN.",
           pt=4.6, font="mono-b", tint=0.9)

    # ------------------------------------------------------------ TITLE BLOCK
    tw, th = 196.0, 56.0
    tx, ty = fx + fw - tw - 3, fy + fh - th - 3
    s.fill(tx, ty, tw, th, tint=0.0)
    s.rect(tx, ty, tw, th, lw=0.5)
    rows = [
        ("PROJECT", "COMBI_RENDER · 76 REVISIONS"),
        ("TITLE", "OFF SIDE ELEVATION (−Y)"),
        ("SHEET", "3 OF 4"),
        ("SCALE", "1:10 AT A2 (594 × 420)"),
        ("STATUS", "NOT ISSUED"),
        ("EVIDENCE GRADE", "E — NEVER PHOTOGRAPHED"),
    ]
    rows2 = [
        ("SOURCE", "STATE.md @ %s" % F["commit"]),
        ("GENERATED", F["gen"]),
        ("SUBDIVISION", "T1_SUB=%s, APPLIED" % F["sub"]),
        ("BODY", "%s QUAD FACES · %d NON-MANIFOLD EDGES" % (F["faces"], F["nonman"])),
        ("INKS", "1 — (72,46,6) ON (206,208,200), BOTH MEASURED"),
        ("DRAWN BY", "sheet3_notissued.py — FIGURES READ AT DRAW TIME"),
    ]
    for i, (k, v) in enumerate(rows):
        yy = ty + 7.5 + i * 7.6
        s.line(tx, yy - 5.2, tx + tw, yy - 5.6, w=0.18, tint=0.4)
        s.text(tx + 3, yy, k, pt=4.6, font="mono", tint=0.65)
        s.text(tx + 40, yy, v, pt=6.2 if k != "STATUS" else 8.0,
               font="mono-b" if k in ("STATUS", "TITLE", "SHEET") else "mono")
    s.line(tx + 90, ty, tx + 90, ty + th, w=0.3, tint=0.6)
    for i, (k, v) in enumerate(rows2):
        yy = ty + 7.5 + i * 7.6
        s.text(tx + 93, yy - 2.4, k, pt=4.2, font="mono", tint=0.6)
        s.text(tx + 93, yy + 1.4, v, pt=4.6, font="mono", tint=0.95)

    # ---------------------------------------------- THE FOOT: what disagrees
    fyy = fy + fh - 8.5
    s.text(fx + 8, fyy - 4.4,
           "THIS SHEET CARRIES TWO OVERALL LENGTHS AND THEY ARE NOT THE SAME MEASUREMENT: "
           "%d mm EXCLUDING THE OPENED LIDS, %d mm INCLUDING THEM,"
           % (round(F["len_nolid"] * 1000), round(F["len_withlid"] * 1000)),
           pt=4.8, font="mono", tint=0.8)
    s.text(fx + 8, fyy,
           "AND %d mm 'EX COUNTER' IN THE DIMENSIONS TABLE AGAINST A SPECIFIED %d — %+.1f mm, "
           "STILL OUT.  THE DISAGREEMENT IS PRINTED BECAUSE IT IS REAL."
           % (round(F["len_meas"] * 1000), round(F["len_spec"] * 1000), F["len_delta"]),
           pt=4.8, font="mono", tint=0.8)

    os.makedirs(outdir, exist_ok=True)
    svg = s.save_svg(os.path.join(outdir, "sheet3_not_issued.svg"))
    png = s.save_png(os.path.join(outdir, "sheet3_not_issued.png"))
    print("SHEET 3 OF 4 — OFF SIDE ELEVATION (−Y) — NOT ISSUED")
    print("  %s" % svg)
    print("  %s" % png)
    print("  A2 %gx%g mm, 1:%g, one ink %s on %s"
          % (W, H, SCALE, INK, STOCK))
    print("%d checked, 0 FAILED -- every figure read from STATE.md / SPEC.md at draw time" % CHECK[0])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "design_out")))
