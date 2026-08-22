"""
probe_rev54_look.py -- rev 54, brief sec.3 item 2, ARM C.

THE FALSIFIABLE TEST.  Arm B's AOV says the fascia's bottom fold carries a
chip band ~1.2 mm tall at the shipped radius.  If that is true then a REAL
shader render at 0.19 mm/px MUST show chips there, and the same window at the
shipped render's own 3.687 mm/px must not.  If the fine crop is clean, arm B
is wrong and I want to know.

Renders the SAME physical window at a ladder of scales, through the project's
own studio rig and its own setup_render(), and saves each as a PNG to look at.
"""
import bpy, bmesh, os, sys, math
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
OUTD = os.path.join(ROOT, "probe_scratch")
os.makedirs(OUTD, exist_ok=True)

src = open(os.path.join(ROOT, "build.py")).read().split('if os.environ.get("T1_SAVE")')[0]
exec(compile(src, "build.py", "exec"))

P = print
def hdr(t): P("\n=== %s ===" % t)

import studio as ST
from PIL import Image

hdr("THE WINDOW -- the same one arm B measured, derived the same way")
ob = bpy.data.objects["counter"]
bm = bmesh.new(); bm.from_mesh(ob.data); bm.transform(ob.matrix_world)
V = [v.co.copy() for v in bm.verts]; bm.free()
FAS = [v for v in V if v.y > 0.90]
FX0, FX1 = min(v.x for v in FAS), max(v.x for v in FAS)
FZ0 = min(v.z for v in FAS)
cx = (FX0 + FX1) / 2.0
X0, X1 = cx - 0.15, cx + 0.15
Z0, Z1 = FZ0 - 0.030, FZ0 + 0.070
P("fascia x %.4f..%.4f  bottom fold z %.4f" % (FX0, FX1, FZ0))
P("window  x %.4f..%.4f  z %.4f..%.4f  (%.3f x %.3f m)"
  % (X0, X1, Z0, Z1, X1 - X0, Z1 - Z0))

ST.cyclorama()
ST.lighting(float(os.environ.get("T1_KEY", "1.0")))
ST.cabin_fill(float(os.environ.get("T1_KEY", "1.0")))

cam_d = bpy.data.cameras.new("lookcam"); cam_d.type = 'ORTHO'
cam_d.ortho_scale = X1 - X0
cam = bpy.data.objects.new("lookcam", cam_d)
bpy.context.scene.collection.objects.link(cam)
cam.location = ((X0 + X1) / 2.0, 26.0, (Z0 + Z1) / 2.0)
cam.rotation_euler = (math.radians(90), 0, math.radians(180))
bpy.context.scene.camera = cam

PXM = [("fine", 5333.3), ("mid", 1000.0), ("shipped", 271.2), ("refside", 211.5)]
SAMP = int(os.environ.get("T1_LOOKSAMP", "192"))
for tag, pxm in PXM:
    RX = max(16, int(round((X1 - X0) * pxm)))
    RY = max(16, int(round((Z1 - Z0) * pxm)))
    sc = ST.setup_render((RX, RY), SAMP, False)
    sc.camera = cam
    cam_d.ortho_scale = X1 - X0
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGB'
    fp = os.path.join(OUTD, "rev54_look_%s" % tag)
    sc.render.filepath = fp
    P("\n%-8s %.1f px/m -> %dx%d  (%.4f mm/px)  %d spp"
      % (tag, pxm, RX, RY, 1000.0 / pxm, SAMP))
    bpy.ops.render.render(write_still=True)
    P("  wrote %s.png" % fp)
P("\nDONE -- LOOK AT probe_scratch/rev54_look_*.png")
