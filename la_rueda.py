"""
la_rueda.py -- CARD ZERO of EL COMBI · LA LOTERIA, drawn from the line pass.

The rev-76 program's own instruction for the deck was *"ship card zero -- one
card end to end -- before drawing the other 23"*, and it named LA RUEDA as the
subject: small, radially symmetric, fully built, needing neither the emblem nor
the clipped `front` camera.  This is that card.

HOW IT IS DRAWN, AND WHY IT IS A HYBRID.  `line_pass.py` gives real vector line
off the model.  On this object it gives two DIFFERENT qualities of line and the
card treats them differently rather than pretending they are one thing:

  * THE BADGE reads perfectly.  It is a raised plate seen square-on, so its
    contour is a true silhouette and Line Art traces it cleanly.  It is drawn
    exactly as the line pass gives it, point for point.  *(Worth noting: the VW
    mark the owner has rejected NINE times in photoreal renders is legible and
    correct in line -- which is the whole argument for the line programme.)*
  * THE CONCENTRIC RINGS FRAGMENT.  They are creases and material boundaries on
    a surface nearly TANGENT to the view, so the occlusion test flickers along
    them and a ring comes back as forty arcs.  MEASURED, chaining swept on one
    build: `chaining_image_threshold` 0.001 -> 0.01 -> 0.05 takes it from
    461 -> 337 -> 182 strokes with the longest run 88 -> 102 -> 156 points.
    Better, and still fragments.

SO THE RINGS ARE **MEASURED, NOT TRACED**: the radius of every stroke point is
taken about the wheel centre, histogrammed, and the peaks are drawn as TRUE
CIRCLES.  That is not a cosmetic repair -- it converts a broken trace into a
measurement, which is the only move this project allows, and the card's own key
says which lines came from which route.

AND IT IS CHECKED AGAINST AN INDEPENDENT QUANTITY (rule 6).  The measured radii
are compared to the constants in `t1_detail.py`, parsed from source at draw
time -- `CAP_R`, `CAP_D = 2*(CAP_R+0.0025)`, `CAP_EMBLEM_D = 0.3170*CAP_D` --
and to `STATE.md`'s mesh-measured `tyre diameter`.  The two routes never share a
number.  A disagreement beyond the stated tolerance REFUSES and prints both.

Run:  python3 line_pass.py --view side --wheel front --out probe_scratch/rueda
      python3 la_rueda.py probe_scratch/rueda.json
"""
import os, re, sys, json, math

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import sheet as SH

CHECK, FAILED = [0], []


def row(ok, msg):
    CHECK[0] += 1
    if not ok:
        FAILED.append(msg)
    return ok


def source_constants():
    """CAP_R, CAP_D, CAP_EMBLEM_D, TREAD_LUGS from t1_detail.py; tyre D from
    STATE.md.  Parsed, never typed -- a constant in a docstring goes stale."""
    d = open(os.path.join(ROOT, "t1_detail.py")).read()
    st = open(os.path.join(ROOT, "STATE.md")).read()
    g = lambda pat, txt=d: re.search(pat, txt, re.M)
    out = {}
    m = g(r"^CAP_R\s*=\s*([\d.]+)")
    out["CAP_R"] = float(m.group(1)) if m else None
    m = g(r"^CAP_D\s*=\s*2 \* \(CAP_R \+ ([\d.]+)\)")
    out["CAP_D"] = 2 * (out["CAP_R"] + float(m.group(1))) if (m and out["CAP_R"]) else None
    m = g(r"^CAP_EMBLEM_D\s*=\s*([\d.]+) \* CAP_D")
    out["CAP_EMBLEM_D"] = float(m.group(1)) * out["CAP_D"] if (m and out["CAP_D"]) else None
    c = open(os.path.join(ROOT, "t1_core.py")).read()
    m = g(r"^RIM_R\s*=\s*([\d.]+)", c)
    out["RIM_OD"] = 2 * float(m.group(1)) if m else None
    m = g(r"^TREAD_LUGS\s*=\s*(\d+)")
    out["TREAD_LUGS"] = int(m.group(1)) if m else None
    m = g(r"^TREAD_LUGS\s*=\s*\d+\s*#\s*DECLARED, inside the MEASURED bracket (\d+)\.\.(\d+)")
    out["LUG_BRACKET"] = (int(m.group(1)), int(m.group(2))) if m else None
    m = g(r"\| tyre diameter \| ([\d.]+)", st)
    out["TYRE_D"] = float(m.group(1)) if m else None
    m = g(r"front arch lip above hub [\d.]+ m \(ARCH_R [\d.]+\) -> tyre gap ([\d.]+) mm", st)
    out["ARCH_GAP_F"] = float(m.group(1)) if m else None
    for k, v in out.items():
        row(v is not None, "source constant %s not found" % k)
    return out


def measure_rings(strokes, ortho, aspect, min_frac=0.010):
    """The wheel centre and its concentric radii, measured off the line pass.

    The centre is the mid-point of the stroke cloud's bounding box: the outer
    tyre contour is a complete circle in this view, so its bbox centre IS the
    axle.  Radii come from a histogram of every point's distance from it.  A
    peak must carry at least `min_frac` of all points to count -- otherwise a
    handful of stray occlusion fragments would each become a 'ring'.
    """
    # NORMALISED -> METRES.  `ortho_scale` spans the LONG axis only, so x maps
    # by `ortho` and y by `ortho / aspect`.  The first cut scaled x by `aspect`
    # AND then everything by `ortho`, which made every radius `aspect` times too
    # big -- the tyre read 966 mm against its measured 664.9.  It was caught by
    # the source-constant cross-check below refusing, which is what the check is
    # for (rule 6: compare two independently obtained quantities).
    P = [(p[0] * ortho, p[1] * ortho / aspect) for s in strokes for p in s]
    x0, x1 = min(p[0] for p in P), max(p[0] for p in P)
    y0, y1 = min(p[1] for p in P), max(p[1] for p in P)
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    rs = sorted(math.hypot(p[0] - cx, p[1] - cy) for p in P)           # metres
    if not rs:
        return None, None, []
    nb = 400
    hi = rs[-1] * 1.001
    hist = [0] * nb
    for r in rs:
        hist[min(nb - 1, int(r / hi * nb))] += 1
    need = max(3, int(len(rs) * min_frac))
    peaks, i = [], 0
    while i < nb:
        if hist[i] >= need:
            j = i
            while j + 1 < nb and hist[j + 1] >= need:
                j += 1
            wsum = sum(hist[k] for k in range(i, j + 1))
            ctr = sum(hist[k] * (k + 0.5) / nb * hi for k in range(i, j + 1)) / wsum
            peaks.append((ctr, wsum))
            i = j + 1
        else:
            i += 1
    return (cx, cy), rs[-1], peaks


def main(src):
    if not os.path.exists(src):
        print("NO LINE PASS: %s does not exist.  Run\n"
              "  python3 line_pass.py --view side --wheel front --out %s\n"
              "Nothing was drawn (rule 37)." % (src, os.path.splitext(src)[0]))
        print("0 checked, 0 FAILED, 1 ABSENT")
        return 2
    d = json.load(open(src))
    S, M = d["strokes"], d["meta"]
    row(M.get("wheel") is not None, "the line pass was not run with --wheel")
    row(M.get("ortho"), "the line pass frame is not orthographic -- radii would carry perspective")
    aspect = M["res"][0] / float(M["res"][1])
    K = source_constants()

    (cx, cy), rmax, peaks = measure_rings(S, M["ortho"], aspect)
    print("LA RUEDA -- rings MEASURED off the line pass, about the axle:")
    for r, n in peaks:
        print("   r %7.4f m  ->  D %7.1f mm   (%d points)" % (r, r * 2000, n))

    # ---- the two independent routes, compared.  Never derived from each other.
    dia = sorted(r * 2 for r, _ in peaks)
    def nearest(target):
        return min(dia, key=lambda v: abs(v - target)) if dia else None
    tyre_seen, cap_seen, emb_seen = (nearest(K["TYRE_D"]), nearest(K["CAP_D"]),
                                     nearest(K["CAP_EMBLEM_D"]))
    for name, seen, want, tol in (("tyre", tyre_seen, K["TYRE_D"], 0.010),
                                  ("hubcap", cap_seen, K["CAP_D"], 0.010),
                                  ("badge", emb_seen, K["CAP_EMBLEM_D"], 0.010),
                                  ("rim OD", nearest(K["RIM_OD"]), K["RIM_OD"], 0.010)):
        ok = seen is not None and abs(seen - want) <= tol
        print("   %-7s line pass %7.1f mm   source %7.1f mm   delta %+6.1f mm  %s"
              % (name, (seen or 0) * 1000, want * 1000, ((seen or 0) - want) * 1000,
                 "ok" if ok else "OUT"))
        row(ok, "%s: line pass %.4f vs source %.4f, beyond %.0f mm"
               % (name, seen or 0, want, tol * 1000))

    if FAILED:
        print("LA RUEDA REFUSES -- nothing was drawn (rule 37).")
        for f in FAILED:
            print("   %s" % f)
        print("%d checked, %d FAILED" % (CHECK[0], len(FAILED)))
        return 2

    # ------------------------------------------------------------- THE CARD
    W, H = 90.0, 140.0
    INK, STOCK = (72, 46, 6), (206, 208, 200)
    s = SH.Sheet(W, H, ink=INK, stock=STOCK, dpi=300, ss=2)
    s.rect(3, 3, W - 6, H - 6, lw=0.6)
    s.rect(4.6, 4.6, W - 9.2, H - 9.2, lw=0.15, tint=0.5)

    # the numeral box.  The deck ORDER is not set, so it prints an em dash
    # rather than a number nobody decided.
    s.rect(7.5, 7.5, 11, 11, lw=0.3)
    s.text(13.0, 15.4, "—", pt=11, font="sans-b", align="c")
    s.text(W - 7.5, 12.0, "EL COMBI", pt=5.0, font="mono-b", align="r", track=1.1)
    s.text(W - 7.5, 16.0, "LA LOTERÍA", pt=5.0, font="mono", align="r", track=1.1, tint=0.7)

    # ---- the engraving
    ECX, ECY, ER = W / 2.0, 48.0, 26.0
    m2k = ER / rmax                                 # sheet mm per METRE
    f = lambda p: (ECX + (p[0] * M["ortho"] - cx) * m2k,
                   ECY + (p[1] * M["ortho"] / aspect - cy) * m2k)

    # the MEASURED rings, drawn as true circles.  Weight by provenance: the
    # tyre's outer edge is the silhouette and carries the heaviest line.
    for r, n in peaks:
        heavy = abs(r * 2 - K["TYRE_D"]) < 0.010
        s.circle(ECX, ECY, r * m2k, w=0.42 if heavy else 0.22,
                 tint=1.0 if heavy else 0.85)

    # THE TREAD, drawn from the DECLARED lug count in the DECLARED tint.  The
    # count is `TREAD_LUGS`, which `t1_detail.py`'s own comment calls "DECLARED,
    # inside the MEASURED bracket 48..84" -- so it is drawn lighter than every
    # measured line on the card, and the bracket is printed beside it.  That is
    # the card's argument in one mark: the wheel you can measure is heavy, the
    # wheel somebody decided is faint.
    if len(dia) >= 2 and K["TREAD_LUGS"]:
        r_out, r_in = dia[-1] / 2.0, dia[-2] / 2.0
        for i in range(K["TREAD_LUGS"]):
            a = 2 * math.pi * (i + 0.25) / K["TREAD_LUGS"]
            s.line(ECX + math.cos(a) * r_in * m2k, ECY + math.sin(a) * r_in * m2k,
                   ECX + math.cos(a) * r_out * m2k, ECY + math.sin(a) * r_out * m2k,
                   w=0.16, tint=0.45)

    # the BADGE, drawn as the line pass gives it -- traced, not measured
    br = K["CAP_EMBLEM_D"] / 2.0 * 1.06
    for st in S:
        pts = [f(p) for p in st]
        if all(math.hypot(q[0] - ECX, q[1] - ECY) <= br * m2k for q in pts):
            s.poly(pts, w=0.18)

    # y=23 is chosen so both notes clear the tyre circle: at that height the
    # circle spans x 37.9..52.1 on this card and the two notes end at 34.5 and
    # begin at 55.5.  Set at y=24/28 they collided with it -- looked at, moved.
    s.text(7.5, 23.0, "ESCALA 1:%.1f" % (1.0 / (m2k / 1000.0)),
           pt=3.8, font="mono", tint=0.55, track=0.4)
    s.text(W - 7.5, 23.0, "LADO · ORTOGRÁFICA", pt=3.8, font="mono", align="r",
           tint=0.55, track=0.4)

    # ---- the dimensions, on the face, as the audit asked
    figs = [("LLANTA · TYRE", "Ø %.1f mm" % (K["TYRE_D"] * 1000), "MEASURED OFF THE MESH", 1.0),
            ("TAPÓN · HUBCAP", "Ø %.1f mm" % (K["CAP_D"] * 1000), "CAP_R + 2.5 mm", 1.0),
            ("EMBLEMA · BADGE", "Ø %.1f mm" % (K["CAP_EMBLEM_D"] * 1000),
             "0.3170 × HUBCAP", 1.0),
            ("TACOS · LUGS", "%d" % K["TREAD_LUGS"],
             "DECLARED · BRACKET %d–%d" % K["LUG_BRACKET"], 0.45)]
    # Each block is [rule][label + value][provenance].  The first cut put the
    # rule BETWEEN the value and its own provenance line, which made every
    # provenance read as a caption for the row BELOW it -- i.e. the tyre's
    # "MEASURED OFF THE MESH" appeared to certify the hubcap.  On a card whose
    # whole argument is provenance, that is the one mistake it cannot make.
    y = 82.0
    for lab, val, prov, tint in figs:
        s.line(7.5, y - 4.4, W - 7.5, y - 4.4, w=0.12, tint=0.35)
        s.text(7.5, y, lab, pt=4.2, font="mono", tint=0.75)
        s.text(W - 7.5, y, val, pt=5.6, font="mono-b", align="r", tint=tint)
        s.text(7.5, y + 3.4, prov, pt=3.6, font="mono", tint=0.5)
        y += 8.2

    # ---- the name, the archetype it displaces, and the dicho
    s.line(7.5, H - 28.0, W - 7.5, H - 28.0, w=0.4)
    s.text(W / 2.0, H - 19.0, "LA RUEDA", pt=13.5, font="sans-b", align="c", track=2.0)
    s.text(W / 2.0, H - 14.4, "desplaza a  ·  el mundo", pt=4.2, font="mono",
           align="c", tint=0.6)
    s.text(W / 2.0, H - 9.4, "SESENTA Y CUATRO TACOS EN LA LLANTA.", pt=4.5,
           font="mono-b", align="c")
    s.text(W / 2.0, H - 5.6, "NADIE LOS HA CONTADO EN LA FOTO.", pt=4.5,
           font="mono-b", align="c")

    outdir = os.path.join(ROOT, "design_out")
    os.makedirs(outdir, exist_ok=True)
    svg = s.save_svg(os.path.join(outdir, "loteria_la_rueda.svg"))
    png = s.save_png(os.path.join(outdir, "loteria_la_rueda.png"))
    print("  %s" % svg)
    print("  %s" % png)
    print("LA RUEDA %gx%g mm, one ink %s on %s, %d measured ring(s), badge traced "
          "from the line pass  [%s, T1_SUB=%s, crease %.0f deg]"
          % (W, H, INK, STOCK, len(peaks), M["view"], M["sub"], M["crease_deg"]))
    print("%d checked, 0 FAILED" % CHECK[0])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else
                  os.path.join(ROOT, "probe_scratch", "rueda.json")))
