"""
line_pass.py -- THE KEYSTONE OF THE DESIGN PROGRAM: vector line extracted from
the model by Grease Pencil Line Art, projected into camera space, and written as
polylines that `sheet.py` can draw.

WHY.  The owner's style ruling, recovered at rev 76 from `NEXT_CONTEXT_PROMPT_
rev39.md` sec.7 and absent from every carrier since rev 43, is his own sentence:

    "cartoon with rendered depth -- VECTOR LINE AND FLAT COLOUR, SHADING AND
     OCCLUSION SAMPLED FROM THE 3D ASSET."

That is a render recipe, not a mood, and until rev 77 nothing in this tree could
produce the first half of it: `grep -rl "freestyle|gpencil|use_pass_" *.py` found
nothing.  Line Art is preferred to Freestyle because it emits EDITABLE VECTOR
STROKES, which is what screen positives, flexo plates and die-cut cutters want --
and F18's die-cut sticker, fired by the owner at rev 77 (F330), is a cutter job.

WHAT IT WRITES, AND WHY NOT SVG DIRECTLY.  Blender's own
`wm.grease_pencil_export_svg` works and was watched working (3.46 MB off the
`side` view).  It is not what this module emits, because its output is one flat
soup of paths at Blender's own weights and colours, and every artefact in this
programme needs its OWN line weights, tints and composition.  So this writes
polylines in CAMERA-NORMALISED coordinates -- x,y in 0..1 with y already flipped
to image order -- and the sheet layer decides how to draw them.  Nothing is lost:
the same bake can still be exported to SVG with `--svg`.

THE TRAP THIS MODULE EXISTS TO REMOVE.  `bpy.ops.object.lineart_bake_strokes()`
bakes THE WHOLE SCENE FRAME RANGE.  The first spike baked 250 identical frames in
220 s and wrote 5,060,569 points to get the 20,234 it needed.  The frame range is
pinned to one frame here.  If a future context finds this slow, that is why.

CEILINGS, STATED (rule 12):
  * Line Art runs on the EVALUATED mesh at whatever `T1_SUB` built.  A stroke
    count is therefore a property of (geometry, subdivision, camera, crease
    angle) and is NOT comparable across builds.  The summary line prints all
    four so a figure can never be quoted without them.
  * `crease_threshold` is an angle between face normals.  `T1_body` is
    shade-smooth, so a LOW threshold finds the subdivision instead of the form.
    Default 40 deg, and `--crease` sweeps it.  This is a POSE CHOICE, not a
    measurement, and it is labelled as one wherever it is printed.
  * Chaining, smoothing and `use_detail_preserve` all alter the point count
    without altering the drawing.  Compare DRAWINGS, not point counts.

THE ABLATION (rule 3 -- a control is finished when you have WATCHED IT FAIL):
  T1_LINE_NOCREASE=1   creases OFF.  The crease stroke count must COLLAPSE.
  T1_LINE_NOCONTOUR=1  contour OFF.  The silhouette must vanish.
Both print what they did and neither is on by default.

Run:
  python3 line_pass.py --view side --out probe_scratch/line_side
  python3 line_pass.py --view side --wheel front --out design_out/la_rueda_line
"""
import os, re, sys, json, math, time, argparse

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

# The ROAD WHEEL's parts, by the LEADING ALPHABETIC RUN of the object name --
# `tyre1.31`, `cap-1.1-1`, `capring1`, `capvw10`, `rim1.31_disc` all reduce to a
# word here.  The first cut split on "." and got `tyre1`, `cap1`, `capring1`, so
# it silently selected TWO objects out of eleven and would have drawn a rim with
# no tyre and no hubcap.  Caught by PRINTING the window and looking at it
# (rule 8: a measurement's window is part of the measurement).
# `wheelhouse*` is EXCLUDED on purpose: it is the arch liner, not the wheel.
# `wheel_hub/_rim/_spoke/_horn` are the STEERING wheel and are excluded too.
WHEEL_PREFIXES = ("tyre", "rim", "cap", "capring", "capvw")
_STEM = re.compile(r"^[A-Za-z_]+")


def stem(name):
    m = _STEM.match(name)
    return m.group(0).rstrip("_") if m else name


def build_scene(sub=None):
    """exec build.py the way audit.py does -- one definition of the model."""
    import bpy
    if sub:
        os.environ["T1_SUB"] = str(sub)
    os.environ.setdefault("T1_SUB", "1")
    src = open(os.path.join(ROOT, "build.py")).read().split('if os.environ.get("T1_SAVE")')[0]
    g = {"__name__": "__build__", "__file__": os.path.join(ROOT, "build.py")}
    exec(compile(src, "build.py", "exec"), g)
    return g


def wheel_source(which, log=print):
    """The road wheel nearest a named axle, on the SHOW (+Y) flank.

    Selected by POSITION, never by a typed object name (rule 35: a guard written
    against a pose encodes that pose; a list of names encodes a build).  Every
    object it picks is PRINTED, because a selection is part of the measurement
    (rule 8) and a silent 'the wheel' is exactly the kind of window this project
    has published wrong five times in one revision.
    """
    import bpy
    from mathutils import Vector
    cands = [o for o in bpy.data.objects
             if o.type == "MESH" and stem(o.name) in WHEEL_PREFIXES]
    if not cands:
        return None, []
    # the two axle groups fall out of the x coordinate; +y is the show flank
    xs = sorted(set(round(sum((o.matrix_world @ Vector(c)).x for c in o.bound_box) / 8.0, 2)
                    for o in cands))
    if not xs:
        return None, []
    want_x = max(xs) if which == "front" else min(xs)
    picked = []
    for o in cands:
        ctr = sum((o.matrix_world @ Vector(c) for c in o.bound_box), Vector()) / 8.0
        if abs(ctr.x - want_x) < 0.35 and ctr.y > 0:
            picked.append(o)
    # ---------------------------------------------------------------- F332
    # source_type = "COLLECTION" IS A NO-OP ON THIS BUILD AND FAILS SILENTLY.
    # MEASURED, three arms, one process, Blender 4.5.3, same camera and crease:
    #   SCENE (control)          strokes span x -2.420 .. +2.160   19471 pts
    #   COLLECTION, 7 objects    strokes span x -2.420 .. +2.128    5933 pts
    #   OBJECT = tyre1.31        strokes span x +0.968 .. +1.632    1331 pts
    # The COLLECTION arm returns FEWER points and still draws the WHOLE VEHICLE,
    # which is the worst kind of failure: a filtered-looking number over an
    # unfiltered window.  It was caught by DRAWING the result and looking at it
    # -- 718 "wheel" strokes rendered a complete bus -- never by reading a count.
    # An explicit view_layer.update() and a depsgraph refresh do not fix it.
    # SO THE ROUTE IS OBJECT, and to give it one object the parts are DUPLICATED
    # and JOINED.  The duplicate is drawn; the build is not touched.  Material
    # slots survive the join, so tyre/rim/cap boundaries still fire use_material.
    bpy.ops.object.select_all(action="DESELECT")
    for o in picked:
        o.select_set(True)
    bpy.context.view_layer.objects.active = picked[0]
    bpy.ops.object.duplicate(linked=False)
    dups = list(bpy.context.selected_objects)
    bpy.context.view_layer.objects.active = dups[0]
    bpy.ops.object.join()
    joined = bpy.context.object
    joined.name = "LP_WHEEL_%s" % which
    log("  wheel window: %s axle, +Y flank, x ~ %+.3f -- %d object(s): %s"
        % (which, want_x, len(picked), ", ".join(sorted(o.name for o in picked))))
    log("  joined into %s (%d verts) -- source_type=OBJECT, because COLLECTION "
        "is a silent no-op here (F332)" % (joined.name, len(joined.data.vertices)))
    return joined, picked


def bake(view="side", crease_deg=40.0, res=(1600, 1100), only=None,
         thickness=1.0, log=print):
    import bpy
    import studio as ST

    sc = ST.setup_render(res, 8, True)
    cam = ST.camera()
    v = ST.views()[view]
    ST.aim(cam, v["loc"], v["tgt"], lens=v.get("lens"), ortho=v.get("ortho"))
    sc.camera = cam

    # ONE FRAME.  See the module docstring -- the default range bakes 250.
    sc.frame_start = sc.frame_end = sc.frame_current = 1

    bpy.ops.object.grease_pencil_add(type="LINEART_SCENE", align="WORLD",
                                     location=(0, 0, 0))
    gp = bpy.context.object
    m = gp.modifiers[0]
    # OBJECT, never COLLECTION -- see F332 in wheel_source() above.
    m.source_type = "OBJECT" if only else "SCENE"
    if only:
        m.source_object = only
    m.use_contour = os.environ.get("T1_LINE_NOCONTOUR") != "1"
    m.use_crease = os.environ.get("T1_LINE_NOCREASE") != "1"
    m.use_material = True
    m.use_edge_mark = True
    m.use_intersection = True
    m.use_loose = False
    m.crease_threshold = math.radians(crease_deg)
    m.thickness = int(round(thickness))
    if not m.use_contour:
        log("  T1_LINE_NOCONTOUR=1 -- CONTOUR OFF (ablation)")
    if not m.use_crease:
        log("  T1_LINE_NOCREASE=1 -- CREASE OFF (ablation)")

    t0 = time.time()
    bpy.ops.object.lineart_bake_strokes()
    log("  baked in %.1f s at crease %.0f deg (a POSE CHOICE, not a measurement)"
        % (time.time() - t0, crease_deg))
    return gp, cam, sc


def project(gp, cam, sc, log=print):
    """Camera-normalised polylines, y flipped to image order."""
    import bpy
    from bpy_extras.object_utils import world_to_camera_view
    dg = bpy.context.evaluated_depsgraph_get()
    mw = gp.matrix_world
    out, npts, off = [], 0, 0
    for lay in gp.data.layers:
        for fr in lay.frames:
            if fr.frame_number != sc.frame_current:
                continue
            for st in fr.drawing.strokes:
                pl = []
                for p in st.points:
                    co = world_to_camera_view(sc, cam, mw @ p.position)
                    if not (-0.25 <= co.x <= 1.25 and -0.25 <= co.y <= 1.25):
                        off += 1
                    pl.append((round(co.x, 6), round(1.0 - co.y, 6)))
                if len(pl) > 1:
                    out.append(pl)
                    npts += len(pl)
    log("  %d stroke(s), %d point(s); %d point(s) outside the frame" % (len(out), npts, off))
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--view", default="side")
    ap.add_argument("--crease", type=float, default=40.0)
    ap.add_argument("--wheel", default=None, choices=("front", "rear"))
    ap.add_argument("--out", default=os.path.join(ROOT, "probe_scratch", "line_pass"))
    ap.add_argument("--sub", type=int, default=None)
    ap.add_argument("--rx", type=int, default=1600)
    ap.add_argument("--ry", type=int, default=1100)
    ap.add_argument("--svg", action="store_true",
                    help="also write Blender's own Grease Pencil SVG export")
    a = ap.parse_args(argv)

    import bpy
    print("LINE PASS -- Grease Pencil Line Art -> polylines")
    build_scene(a.sub)
    sub = os.environ.get("T1_SUB", "?")
    only = None
    if a.wheel:
        only, picked = wheel_source(a.wheel)
        if not picked:
            print("NO WHEEL OBJECTS: nothing matching %s was found in the build, so "
                  "nothing was measured (rule 37)." % (WHEEL_PREFIXES,))
            print("1 checked, 1 FAILED")
            return 2
    gp, cam, sc = bake(a.view, a.crease, (a.rx, a.ry), only)
    strokes = project(gp, cam, sc)
    if not strokes:
        print("NO STROKES: Line Art produced nothing for view %r. Nothing was "
              "measured (rule 37)." % a.view)
        print("1 checked, 1 FAILED")
        return 2

    os.makedirs(os.path.dirname(os.path.abspath(a.out)) or ".", exist_ok=True)
    meta = dict(view=a.view, crease_deg=a.crease, sub=sub, res=[a.rx, a.ry],
                wheel=a.wheel, blender=bpy.app.version_string,
                contour=(os.environ.get("T1_LINE_NOCONTOUR") != "1"),
                crease=(os.environ.get("T1_LINE_NOCREASE") != "1"),
                ortho=sc.camera.data.ortho_scale if sc.camera.data.type == "ORTHO" else None,
                n_strokes=len(strokes), n_points=sum(len(s) for s in strokes))
    json.dump(dict(meta=meta, strokes=strokes), open(a.out + ".json", "w"))
    print("  -> %s.json" % a.out)

    if a.svg:
        bpy.ops.object.select_all(action="DESELECT")
        gp.select_set(True)
        bpy.context.view_layer.objects.active = gp
        bpy.ops.wm.grease_pencil_export_svg(filepath=a.out + "_blender.svg",
                                            selected_object_type="ACTIVE", use_fill=False)
        print("  -> %s_blender.svg (%d B)" % (a.out, os.path.getsize(a.out + "_blender.svg")))

    # THE SUMMARY LINE.  A stroke count means nothing without all four of these
    # (see the docstring's ceilings), so they travel with it, always.
    print("LINE PASS %s%s: %d strokes / %d points  [T1_SUB=%s, crease %.0f deg, "
          "%dx%d, contour=%s crease=%s]"
          % (a.view, "/" + a.wheel + " wheel" if a.wheel else "", meta["n_strokes"],
             meta["n_points"], sub, a.crease, a.rx, a.ry, meta["contour"], meta["crease"]))
    print("1 checked, 0 FAILED")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
