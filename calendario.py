"""
calendario.py -- CALENDARIO DE LA CASA, ANO XXII.  The header board, drawn.

WHY THIS IS A SCRIPT AND NOT A LAYOUT.  The one number on the front of this
object is the house's own age, and the concept this file replaces printed it
WRONG -- it said "ANO XXI runs Feb 2027 to Jan 2028", which is off by one on its
own stated epoch and off by two against a realistic ship date.  CLAUDE.md's
first paragraph: "If you find a number here, that is the bug -- delete it."
So the numeral, the twelve leaf grids and the twenty-two NO EMITIDO rows are all
COMPUTED from one constant, OPENED = 2006-02-06, and cannot be typed.

CONVENTION, DECLARED ON THE SHEET (the handed concept declared none and was
self-contradictory between its masthead and its back list):
    ANO N is the ORDINAL year of trading and begins 6 February (2005 + N).
    ANO I   = 2006-02-06 .. 2007-02-05
    ANO XXI = 2026-02-06 .. 2027-02-05   <- CURRENT at time of writing
    ANO XXII= 2027-02-06 .. 2028-02-05   <- the first issuable year

EVERY VEHICLE FIGURE IS READ OUT OF STATE.md AT DRAW TIME and the script
REFUSES if one is missing (rule 37), the pattern sheet3_notissued.py already
uses.  The drawing in the image window is line_pass.py's own output, not an
illustration: probe_scratch/line_pass.json, camera-normalised polylines.

CEILINGS (rule 12):
  * The masthead lettering is set in the sheet engine's mono/sans faces.  The
    HOUSE's own lettering is hand-painted -- see ref_rear34.jpg, the sign on the
    palm -- and is NOT reproducible from anything in this tree.  This sheet is a
    POSITION PROOF for that lettering, and says so on its face.
  * The line pass is a property of (geometry, subdivision, camera, crease).  Its
    own meta block is printed in the colophon so the drawing can never be quoted
    without them.
  * No colour separation is implied.  One ink.

Run:  python3 calendario.py            -> design_out/calendario_ano.{svg,png}
      python3 calendario.py --year 2028
"""
import os, sys, json, math, re, datetime, argparse

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import sheet as S

OPENED = datetime.date(2006, 2, 6)          # SPEC grade-S: the day it opened
CHECK = [0]
MISSING = []

# ------------------------------------------------------------------ the ink
RED   = (196, 49, 36)       # measured body red, the sheet's ONE ink
STOCK = (238, 231, 214)     # warm uncoated

MESES = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO",
         "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
DIAS = ["L", "M", "M", "J", "V", "S", "D"]


def roman(n):
    out, v = "", [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"),
                  (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"),
                  (5, "V"), (4, "IV"), (1, "I")]
    for a, b in v:
        while n >= a:
            out += b
            n -= a
    return out


def ano_of(issue_year):
    """ORDINAL year of trading beginning 6 Feb issue_year.  Computed, never typed."""
    n = issue_year - OPENED.year + 1
    start = datetime.date(issue_year, OPENED.month, OPENED.day)
    end = datetime.date(issue_year + 1, OPENED.month, OPENED.day) - datetime.timedelta(days=1)
    return n, start, end


def grab(text, pattern, what, group=1, cast=float):
    CHECK[0] += 1
    m = re.search(pattern, text)
    if not m:
        MISSING.append(what)
        return None
    try:
        return cast(m.group(group)) if cast else m.group(group)
    except Exception:
        MISSING.append(what)
        return None


def month_grid(y, m):
    """rows of 7, Monday-first, 0 for blanks.  Computed from the calendar."""
    first = datetime.date(y, m, 1)
    nxt = datetime.date(y + (m == 12), (m % 12) + 1, 1)
    ndays = (nxt - first).days
    lead = first.weekday()                 # Mon = 0
    cells = [0] * lead + list(range(1, ndays + 1))
    while len(cells) % 7:
        cells.append(0)
    return [cells[i:i + 7] for i in range(0, len(cells), 7)]



def find_badges(strokes, ortho, aspect, wheelbase, cap_emblem_d):
    """Locate the two hubcap VW glyphs BY MEASUREMENT, not by eye.

    Small strokes are single-link clustered at 45 mm.  A cluster is accepted as a
    hubcap badge only if the two best clusters' CENTRE SEPARATION reproduces the
    mesh-measured WHEELBASE -- two independently obtained quantities (rule 6):
    the separation comes from projected line-art strokes, the wheelbase from
    STATE.md's mesh audit.  If they disagree the caller REFUSES rather than
    suppressing whatever happens to be there.
    """
    E = []
    for st in strokes:
        xs = [p[0] * ortho for p in st]
        ys = [p[1] * ortho / aspect for p in st]
        if max(max(xs) - min(xs), max(ys) - min(ys)) < 0.060:
            E.append((sum(xs) / len(xs), sum(ys) / len(ys)))
    used, groups = [False] * len(E), []
    for i in range(len(E)):
        if used[i]:
            continue
        g, used[i], k = [i], True, 0
        while k < len(g):
            for j in range(len(E)):
                if not used[j] and math.hypot(E[g[k]][0] - E[j][0],
                                              E[g[k]][1] - E[j][1]) < 0.045:
                    used[j] = True
                    g.append(j)
            k += 1
        xs = [E[i2][0] for i2 in g]
        ys = [E[i2][1] for i2 in g]
        cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
        rad = max(math.hypot(E[i2][0] - cx, E[i2][1] - cy) for i2 in g)
        if len(g) > 20 and rad < cap_emblem_d / 2.0 * 1.10:
            groups.append((len(g), cx, cy, rad))
    groups.sort(reverse=True)
    if len(groups) < 2:
        return None, "only %d badge-sized cluster(s) found" % len(groups)
    a, b = sorted(groups[:2], key=lambda g: g[1])
    sep = b[1] - a[1]
    if abs(sep - wheelbase) > 0.005:
        return None, ("badge cluster separation %.4f m does not reproduce the "
                      "mesh wheelbase %.4f m (%+0.1f mm)" %
                      (sep, wheelbase, (sep - wheelbase) * 1000.0))
    return ((a[1], a[2], a[3]), (b[1], b[2], b[3]), sep), None


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=2027,
                    help="ISSUE year: the calendar handed out on 6 February of it")
    ap.add_argument("--out", default=os.path.join(ROOT, "design_out"))
    a = ap.parse_args(argv)

    N, start, end = ano_of(a.year)
    NUM = roman(N)

    # ------------------------------------------------- figures, read at draw time
    state = open(os.path.join(ROOT, "STATE.md")).read()
    F = {}
    F["commit"] = grab(state, r"\| git commit \| `([0-9a-f]+)`", "STATE.md commit", cast=None)
    F["gen"] = grab(state, r"\| generated \| ([0-9\- :]+UTC)", "STATE.md stamp", cast=None)
    F["wb"] = grab(state, r"\| wheelbase \| ([0-9.]+) \|", "wheelbase")
    F["len"] = grab(state, r"dims  L=([0-9.]+)", "body length")
    F["wid"] = grab(state, r"\| overall width \(body\) \| ([0-9.]+) \|", "body width")
    F["tyre"] = grab(state, r"\| tyre diameter \| ([0-9.]+) \|", "tyre diameter")
    F["bays"] = grab(state, r"bay widths ([0-9.]+) ([0-9.]+) ([0-9.]+)", "bay widths", cast=None)
    F["nap"] = grab(state, r"open serving apertures on \+Y: (\d+)", "aperture count", cast=int)
    F["capd"] = 0.2740      # t1_detail CAP_D = 2*(CAP_R+0.0025), cross-checked
    F["capemb"] = 0.0869    # CAP_EMBLEM_D = 0.3170 * CAP_D
    F["rake"] = grab(state, r"rake ([0-9.]+) mm/m", "rake")

    lp_path = os.path.join(ROOT, "probe_scratch", "line_pass.json")
    if not os.path.exists(lp_path):
        print("NO LINE PASS: %s absent.  Nothing was drawn (rule 37).\n"
              "Make it:  python3 line_pass.py --view side --out probe_scratch/line_pass"
              % lp_path)
        return 2
    LP = json.load(open(lp_path))
    meta, strokes = LP["meta"], LP["strokes"]
    CHECK[0] += 1
    if meta.get("view") != "side":
        MISSING.append("line pass is view=%s, not side" % meta.get("view"))

    if MISSING:
        for w in MISSING:
            print("  MISSING: %s" % w)
        print("CALENDARIO: %d figure(s) NOT FOUND -- REFUSING (rule 37)." % len(MISSING))
        return 3

    # ------------------------------------------------------------------ board
    W, H = 480.0, 680.0
    sh = S.Sheet(W, H, ink=RED, stock=STOCK, dpi=150, ss=2)
    M = 26.0                                # margin

    # --- masthead ---------------------------------------------------------
    # the house's own sign is a BEADED frame round a header band over a white
    # field (playa_env.C_SIGN_FRAME / _HEAD / _FIELD / _INK, four colours that
    # have sat measured for revisions and that no artefact has ever used).
    y = M
    sh.rect(M, y, W - 2 * M, 104.0, lw=1.2)
    sh.rect(M + 3.0, y + 3.0, W - 2 * M - 6.0, 98.0, lw=0.4)
    # the bead course, drawn as the sign draws it
    nb = int((W - 2 * M - 6.0) / 6.0)
    for i in range(nb + 1):
        bx = M + 3.0 + i * (W - 2 * M - 6.0) / nb
        sh.circle(bx, y + 3.0, 1.15, w=0.3)
        sh.circle(bx, y + 101.0, 1.15, w=0.3)
    sh.text(W / 2, y + 26.0, "CALENDARIO DE LA CASA", pt=27, font="sans-b",
            align="c", track=1.6)
    sh.line(M + 30, y + 34.0, W - M - 30, y + 34.0, w=0.5)
    sh.text(W / 2, y + 60.0, "ANO %s" % NUM, pt=44, font="sans-b", align="c", track=4.0)
    sh.text(W / 2, y + 76.0, "%s  -  %s" % (start.strftime("%d.%m.%Y"),
                                            end.strftime("%d.%m.%Y")),
            pt=10, font="mono", align="c", track=0.8)
    sh.text(W / 2, y + 91.0, "ABIERTO DESDE EL 6 DE FEBRERO DE 2006",
            pt=9.5, font="sans-b", align="c", track=1.2)

    # --- image window: THE LINE PASS -------------------------------------
    iy0, iy1 = 142.0, 340.0
    sh.rect(M, iy0, W - 2 * M, iy1 - iy0, lw=0.5)
    # ASPECT.  world_to_camera_view normalises EACH AXIS over the frame, so a
    # uniform scale of (x, y) stretches the drawing by res[0]/res[1] = 1.4545.
    # x spans `ortho` metres; y spans `ortho / aspect`.  la_rueda.py records the
    # same bug being made and fixed -- see its measure_rings() comment.
    ASPECT = meta["res"][0] / float(meta["res"][1])
    xs = [p[0] * meta["ortho"] for st in strokes for p in st]
    ys = [p[1] * meta["ortho"] / ASPECT for st in strokes for p in st]
    bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
    DRAWN_W, DRAWN_H = bx1 - bx0, by1 - by0
    # RULE 6: two INDEPENDENTLY obtained quantities.  The drawing's own extent is
    # measured off projected strokes; STATE.md's is measured off the mesh.
    st_len = grab(state, r"\| overall length \(ex counter\) \| ([0-9.]+)", "STATE overall length")
    st_top = grab(state, r"\(bbox top ([0-9.]+)\)", "STATE bbox top")
    if st_len is None or st_top is None:
        for w in MISSING:
            print("  MISSING: %s" % w)
        print("CALENDARIO: cross-check figure absent -- REFUSING (rule 37).")
        return 3
    dL, dH = (DRAWN_W - st_len) * 1000.0, (DRAWN_H - st_top) * 1000.0
    if abs(dL) > 5.0 or abs(dH) > 5.0:
        print("LINE PASS DOES NOT REGISTER WITH THE MESH: drawn %.4f x %.4f m against "
              "STATE %.4f x %.4f (%+0.1f / %+0.1f mm).  REFUSING." %
              (DRAWN_W, DRAWN_H, st_len, st_top, dL, dH))
        return 4
    pad = 12.0
    aw, ah = (W - 2 * M) - 2 * pad, (iy1 - iy0) - 2 * pad
    sc = min(aw / (bx1 - bx0), ah / (by1 - by0))
    ox = M + pad + (aw - (bx1 - bx0) * sc) / 2.0
    oy = iy0 + pad + (ah - (by1 - by0) * sc) / 2.0
    # ---- THE MARK.  Found by measurement, suppressed, and DECLARED ----------
    # Rule 1 caught this by LOOKING at the first proof: a true side elevation
    # does NOT compose the Volkswagen roundel out.  The nose PRESSING is edge-on,
    # but each HUBCAP carries the same mark square-on, and F333 records that it
    # traces cleanly.  At this sheet's scale it prints at CAP_EMBLEM_D * scale --
    # printed below -- which is under the size at which the owner's nine
    # rejections could be resolved.  Printing an unjudgeable mark is worse than
    # not printing one, so the glyph is replaced by a plain disc of its own
    # measured diameter and the sheet says so.  The JUDGEABLE view is la_rueda.py.
    BADGES, why = find_badges(strokes, meta["ortho"], ASPECT, F["wb"], F["capd"])
    CHECK[0] += 1
    if BADGES is None:
        print("CANNOT LOCATE THE HUBCAP MARKS: %s.\n"
              "Nothing was drawn -- this sheet must not ship with an unlocated "
              "trademark on it (rule 37)." % why)
        return 6
    (ax, ay, ar), (bx, by, br), sep = BADGES
    supp = 0

    def _in_badge(st):
        """A stroke is glyph if it is SMALLER than the badge and CENTRED in it.

        The first cut required every point inside the badge radius and left a
        visible fragment of the V on the proof -- caught by cropping the hub and
        LOOKING at it (rule 1), not by reasoning.  Strokes that poke a little
        outside are still glyph; the big concentric hubcap rings are excluded by
        the size test, not by the position test.
        """
        xs = [p[0] * meta["ortho"] for p in st]
        ys = [p[1] * meta["ortho"] / ASPECT for p in st]
        if max(max(xs) - min(xs), max(ys) - min(ys)) >= F["capemb"]:
            return False
        cx0, cy0 = sum(xs) / len(xs), sum(ys) / len(ys)
        for cx, cy in ((ax, ay), (bx, by)):
            if math.hypot(cx0 - cx, cy0 - cy) < F["capemb"] / 2.0 * 1.15:
                return True
        return False

    npts = 0
    for st in strokes:
        if _in_badge(st):
            supp += 1
            continue
        pts = [(ox + (p[0] * meta["ortho"] - bx0) * sc,
                oy + (p[1] * meta["ortho"] / ASPECT - by0) * sc) for p in st]
        if len(pts) > 1:
            sh.poly(pts, w=0.26)
            npts += len(pts)
    for cx, cy in ((ax, ay), (bx, by)):
        sh.circle(ox + (cx - bx0) * sc, oy + (cy - by0) * sc,
                  F["capemb"] / 2.0 * sc, w=0.26)
    sh.text(M, iy1 + 7.0,
            "ELEVACION LATERAL - PROYECCION ORTOGRAFICA VERDADERA - NO ES UNA FOTOGRAFIA",
            pt=7.2, font="mono", track=0.4)

    # --- the index of years ----------------------------------------------
    # THE DANGER LENS: "at a size a person reads standing up."  Two columns of
    # eleven so that every year of the house is on the FACE and none is dropped;
    # the earlier 3x7 layout silently BINNED the current year, which is the one
    # row the sheet exists to carry.  Row count is len(range(1, N+1)), asserted.
    ty = 366.0
    sh.text(M, ty, "LOS ANOS DE LA CASA", pt=11, font="sans-b", track=1.4)
    sh.text(W - M, ty, "%d DE %d NO EMITIDOS" % (N - 1, N), pt=11, font="sans-b",
            align="r", track=1.0)
    sh.line(M, ty + 4.5, W - M, ty + 4.5, w=0.7)
    rows = 11
    cols = int(math.ceil(N / float(rows)))
    cw = (W - 2 * M) / cols
    drawn_rows = 0
    for i in range(1, N + 1):
        c, r = (i - 1) // rows, (i - 1) % rows
        x = M + c * cw
        yy = ty + 20.0 + r * 10.4
        s0 = datetime.date(2005 + i, 2, 6)
        sh.text(x, yy, roman(i), pt=8.6, font="mono-b")
        sh.text(x + 34.0, yy, "%d-%d" % (s0.year, s0.year + 1), pt=8.0, font="mono")
        if i < N:
            sh.text(x + 84.0, yy, "NO EMITIDO", pt=8.6, font="mono-b")
        else:
            sh.fill(x - 3.0, yy - 7.4, cw - 8.0, 10.2, tint=1.0)
            sh.text(x + 84.0, yy, "ESTE", pt=8.6, font="mono-b", tint=0.0)
            sh.text(x, yy, roman(i), pt=8.6, font="mono-b", tint=0.0)
            sh.text(x + 34.0, yy, "%d-%d" % (s0.year, s0.year + 1), pt=8.0,
                    font="mono", tint=0.0)
        drawn_rows += 1
    CHECK[0] += 1
    if drawn_rows != N:
        print("INDEX DROPPED %d ROW(S) -- REFUSING." % (N - drawn_rows))
        return 5

    # --- the block: twelve leaves, drawn to size --------------------------
    by = 514.0
    sh.line(M, by - 12.0, W - M, by - 12.0, w=0.9, dash=(2.0, 2.0))
    sh.text(M, by - 16.0, "BLOQUE DE 12 HOJAS - COSIDO CON ALAMBRE AL PIE", pt=7.0,
            font="mono", track=0.4)
    gw = (W - 2 * M) / 4.0
    gh = 42.0
    for k in range(12):
        mi = (OPENED.month - 1 + k) % 12
        yr = a.year + (1 if (OPENED.month - 1 + k) >= 12 else 0)
        gx = M + (k % 4) * gw
        gy = by + (k // 4) * gh
        sh.text(gx + 1.0, gy + 7.0, "%s %d" % (MESES[mi], yr), pt=6.4,
                font="sans-b", track=0.5)
        for d in range(7):
            sh.text(gx + 4.0 + d * 12.0, gy + 14.0, DIAS[d], pt=5.2, font="mono", align="c")
        grid = month_grid(yr, mi + 1)
        for ri, row in enumerate(grid):
            for ci, dnum in enumerate(row):
                if not dnum:
                    continue
                sh.text(gx + 4.0 + ci * 12.0, gy + 20.0 + ri * 5.2, "%d" % dnum,
                        pt=5.2, font="mono", align="c")
        # the anniversary is marked on its own leaf
        if mi == OPENED.month - 1:
            for ri, row in enumerate(grid):
                for ci, dnum in enumerate(row):
                    if dnum == OPENED.day:
                        sh.circle(gx + 4.0 + ci * 12.0, gy + 18.2 + ri * 5.2, 3.4, w=0.6)

    # --- foot -------------------------------------------------------------
    fy = H - 22.0
    sh.line(M, fy - 8.0, W - M, fy - 8.0, w=0.5)
    sh.text(M, fy, "TACOMBI", pt=10, font="sans-b", track=2.0)
    sh.text(W - M, fy - 1.0,
            "DIBUJO: line_pass.py  %d trazos / %d puntos  vista %s  sub %s  pliegue %s deg" %
            (meta["n_strokes"], meta["n_points"], meta["view"], meta["sub"], meta["crease_deg"]),
            pt=5.6, font="mono", align="r")
    sh.text(W - M, fy + 6.0,
            "GEOMETRIA: STATE.md @ %s  -  L %.3f m  DE EJES %.3f m  ANCHO %.4f m  %d HUECOS %s m" %
            (F["commit"], F["len"], F["wb"], F["wid"], F["nap"], F["bays"][0]),
            pt=5.6, font="mono", align="r")
    sh.text(M, fy + 6.0, "ROTULO POR ENCARGAR - ESTA PRUEBA FIJA LA POSICION, NO LA LETRA",
            pt=5.6, font="mono", track=0.3)

    os.makedirs(a.out, exist_ok=True)
    stem = os.path.join(a.out, "calendario_ano_%s" % NUM.lower())
    sh.save_svg(stem + ".svg")
    sh.save_png(stem + ".png")

    print("ANO %s (%d)  %s .. %s   [ordinal from OPENED %s -- COMPUTED, not typed]"
          % (NUM, N, start, end, OPENED))
    print("index rows drawn: %d, of which NO EMITIDO: %d" % (N, N - 1))
    print("line pass: %d strokes / %d points placed, %d points drawn" %
          (meta["n_strokes"], meta["n_points"], npts))
    print("scale 1 : %.1f  (%.4f mm paper per m)" % (1000.0 / sc, sc))
    print("HUBCAP MARKS: 2 located, separation %.4f m against mesh wheelbase "
          "%.4f m (%+0.1f mm) -- %d glyph stroke(s) SUPPRESSED, plain discs drawn"
          % (sep, F["wb"], (sep - F["wb"]) * 1000.0, supp))
    print("  the mark would have printed at %.2f mm dia; judgeable view is la_rueda.py"
          % (F["capemb"] * sc))
    print("registration: drawn %.4f x %.4f m against STATE %.4f x %.4f (%+0.1f / %+0.1f mm)"
          % (DRAWN_W, DRAWN_H, st_len, st_top, dL, dH))
    print("wrote %s.svg / %s.png  (%.0f x %.0f mm, one ink %s on %s)"
          % (stem, stem, W, H, RED, STOCK))
    print("%d checked, 0 FAILED -- every vehicle figure read from STATE.md at draw time"
          % CHECK[0])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
