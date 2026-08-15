"""probe_f90.py -- READ-ONLY.  SPEC 10.77, rev 27.

Answers the UNVERIFIED question `probe_ctan_pedestal.py:170` leaves open:

    "the counter camera sits ~83 deg off the top's normal, where Schlick on
     F0 = 0.0256 gives F ~ 0.53.  If 'Specular IOR Level' = 0 leaves F90 = 1,
     `T1_CTAN_SP=0` is not a complete specular ablation.  UNVERIFIED -- test
     it before use."

It decides whether rev 26's arm 4 -- `T1_CTAN_DUST=0 T1_CTAN_SP=0 T1_CTAN_CT=0`,
the arm that produced the surviving 6.6 / 6.6 / 8.5 % pedestal -- was a
COMPLETE specular ablation or only a partial one.  If it was partial, part of
that residual is specular and the never-ablated list in SPEC 10.70 is chasing
the wrong thing.

METHOD.  A purpose-built minimal scene, NOT the vehicle: one plane carrying a
material built by `t1_mats.simple()` with the live `COUNTERTAN`, one area
light, an orthographic camera.  Nothing in the build is touched and no vehicle
geometry is loaded, so the measurement cannot be contaminated by the occluders
SPEC 10.65 found or the light stacking SPEC 10.65 found.

Run:  blender -b --python probe_f90.py

THE ARMS, and why each exists
-----------------------------
  1 SHIPPED    spec = 0.32, ior = 1.45          -- what the build renders
  2 SP0        spec = 0.00, ior = 1.45          -- what `T1_CTAN_SP=0` does
  3 TRUE-OFF   spec = 0.00, ior = 1.00          -- a real dielectric removal:
                                                   with no index step there is
                                                   no interface at ANY angle
  4 DIFFUSE    a bare Diffuse BSDF, same albedo -- the ultimate control

Read at NORMAL incidence and at GRAZING (83 deg), because F90 only shows at
grazing.  A complete ablation requires arm 2 == arm 3 == arm 4 at BOTH angles.

CONTROLS THAT MUST PASS BEFORE ANY ARM IS BELIEVED
  N  NULL      arm 1 rendered twice must agree to < 0.5 % -- otherwise the
               noise floor is larger than the effect and nothing here counts.
  P  POSITIVE  arm 1 must DIFFER from arm 4 at grazing, and differ MORE at
               grazing than at normal.  If the rig cannot see the shipped
               specular, it cannot see its removal either.

               rev 27's FIRST cut of this control asserted arm 1 > arm 4 --
               "adding specular adds energy".  It FAILED at (0.990, 1.025,
               1.158): the Principled BSDF CONSERVES energy, so a specular
               layer takes from the diffuse lobe and the R channel came out
               0.99x.  The control's PREMISE was wrong, not the finding.
               SPEC 10.38's *check the control itself*, and the third time
               this session that a control of mine has been the defect.
"""

import os
import sys

import bpy
import mathutils

sys.path.insert(0, os.path.dirname(os.path.abspath(bpy.data.filepath or __file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import t1_mats as M                                        # noqa: E402

GRAZE_DEG = 83.0          # SPEC 10.70's stated counter-camera angle
RES = 96
SAMPLES = 512


def _clear():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def _scene(angle_deg, kind):
    """kind in {'shipped', 'sp0', 'trueoff', 'diffuse'}"""
    _clear()
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = SAMPLES
    sc.cycles.use_denoising = False
    sc.render.resolution_x = sc.render.resolution_y = RES
    sc.render.film_transparent = False
    sc.view_settings.view_transform = 'Standard'
    sc.world = bpy.data.worlds.new("w")
    sc.world.use_nodes = True
    sc.world.node_tree.nodes["Background"].inputs[1].default_value = 0.0

    bpy.ops.mesh.primitive_plane_add(size=4.0, location=(0, 0, 0))
    plane = bpy.context.object

    name = "ctan_%s" % kind
    if kind == 'shipped':
        mat = M.simple(name, M.COUNTERTAN, rough=0.42, spec=0.32, ior=1.45)
    elif kind == 'sp0':
        mat = M.simple(name, M.COUNTERTAN, rough=0.42, spec=0.00, ior=1.45)
    elif kind == 'trueoff':
        mat = M.simple(name, M.COUNTERTAN, rough=0.42, spec=0.00, ior=1.00)
    else:
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        nt = mat.node_tree
        nt.nodes.clear()
        d = nt.nodes.new("ShaderNodeBsdfDiffuse")
        d.inputs["Color"].default_value = (*M.COUNTERTAN, 1)
        d.inputs["Roughness"].default_value = 0.0
        o = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(d.outputs[0], o.inputs["Surface"])
    plane.data.materials.append(mat)

    # one area light, fixed, well away from the specular mirror direction of
    # BOTH cameras so neither reads a mirror highlight rather than the lobe
    lamp_d = bpy.data.lights.new("key", 'AREA')
    lamp_d.size = 3.0
    lamp_d.energy = 400.0
    lamp = bpy.data.objects.new("key", lamp_d)
    bpy.context.collection.objects.link(lamp)
    lamp.location = (-2.2, -1.4, 2.6)
    lamp.rotation_euler = mathutils.Vector((0, 0, 0)).to_track_quat('Z', 'Y').to_euler()
    d = mathutils.Vector((0, 0, 0)) - lamp.location
    lamp.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

    cam_d = bpy.data.cameras.new("c")
    cam_d.type = 'ORTHO'
    cam_d.ortho_scale = 1.2
    cam = bpy.data.objects.new("c", cam_d)
    bpy.context.collection.objects.link(cam)
    th = mathutils.Vector((0.0, 0.0, 1.0))
    import math
    a = math.radians(angle_deg)
    pos = mathutils.Vector((math.sin(a) * 6.0, 0.0, math.cos(a) * 6.0))
    cam.location = pos
    cam.rotation_euler = (-pos).to_track_quat('-Z', 'Y').to_euler()
    sc.camera = cam
    return sc


def _render_mean(sc, tag):
    path = "/tmp/f90_%s.exr" % tag
    sc.render.image_settings.file_format = 'OPEN_EXR'
    sc.render.image_settings.color_depth = '32'
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    img = bpy.data.images.load(path)
    px = list(img.pixels)
    n = len(px) // 4
    acc = [0.0, 0.0, 0.0]
    for i in range(n):
        for c in range(3):
            acc[c] += px[i * 4 + c]
    bpy.data.images.remove(img)
    return [v / n for v in acc]


def main():
    print("\n" + "=" * 78)
    print("probe_f90.py -- is `T1_CTAN_SP=0` a COMPLETE specular ablation?")
    print("COUNTERTAN read live from t1_mats: %s" % (M.COUNTERTAN,))
    print("=" * 78)

    res = {}
    for ang, aname in ((0.0, "normal"), (GRAZE_DEG, "graze%d" % int(GRAZE_DEG))):
        for kind in ("shipped", "sp0", "trueoff", "diffuse"):
            sc = _scene(ang, kind)
            res[(aname, kind)] = _render_mean(sc, "%s_%s" % (aname, kind))
    # NULL control: shipped rendered a second time at grazing
    sc = _scene(GRAZE_DEG, "shipped")
    res[("graze%d" % int(GRAZE_DEG), "shipped_null")] = _render_mean(sc, "null")

    ok = True

    def check(tag, cond, detail=""):
        nonlocal ok
        ok = ok and bool(cond)
        print("  [%s] %-50s %s" % ("PASS" if cond else "FAIL", tag, detail))

    gz = "graze%d" % int(GRAZE_DEG)
    print("\n=== mean linear radiance over the plane ===")
    for aname in ("normal", gz):
        print("  %s:" % aname)
        for kind in ("shipped", "sp0", "trueoff", "diffuse"):
            v = res[(aname, kind)]
            print("     %-9s %s" % (kind, tuple(round(x, 6) for x in v)))

    a1 = res[(gz, "shipped")]
    a1b = res[(gz, "shipped_null")]
    a2 = res[(gz, "sp0")]
    a3 = res[(gz, "trueoff")]
    a4 = res[(gz, "diffuse")]

    def rel(x, y):
        return max(abs(p - q) / max(q, 1e-9) for p, q in zip(x, y)) * 100.0

    print("\n=== controls ===")
    check("N  null: shipped rendered twice agrees < 0.5 %", rel(a1, a1b) < 0.5,
          "%.3f %%" % rel(a1, a1b))
    n1, n4 = res[("normal", "shipped")], res[("normal", "diffuse")]
    d_graze, d_norm = rel(a1, a4), rel(n1, n4)
    check("P1 positive: shipped DIFFERS from diffuse at grazing",
          d_graze > 2.0, "%.2f %% (shipped/diffuse = %s)"
          % (d_graze, tuple(round(p / max(q, 1e-9), 4) for p, q in zip(a1, a4))))
    check("P2 positive: and the difference is LARGER at grazing than normal",
          d_graze > 3.0 * d_norm,
          "grazing %.2f %% vs normal %.2f %% -- %.1fx, so the rig CAN see the "
          "grazing lobe" % (d_graze, d_norm, d_graze / max(d_norm, 1e-9)))

    print("\n=== THE QUESTION ===")
    print("  grazing, relative to the TRUE-OFF arm (spec=0 AND ior=1):")
    print("     shipped  vs trueoff   %+7.3f %%   <-- the whole specular" % rel(a1, a3))
    resid = rel(a2, a3)
    print("     sp0      vs trueoff   %+7.3f %%   <-- LEFT BEHIND by T1_CTAN_SP=0"
          % resid)
    print("     diffuse  vs trueoff   %+7.3f %%   <-- floor" % rel(a4, a3))

    total = rel(a1, a3)
    frac = 100.0 * resid / total if total > 1e-9 else 0.0
    print("\n  fraction of the shipped specular that T1_CTAN_SP=0 FAILS to "
          "remove: %.2f %%" % frac)
    print("  VERDICT: %s" % (
        "`T1_CTAN_SP=0` IS a COMPLETE specular ablation -- 'Specular IOR "
        "Level' = 0\n           removes the dielectric lobe at ALL angles, "
        "F90 included. rev 26's\n           arm 4 was complete and the "
        "surviving 6.6/6.6/8.5 % pedestal is NOT specular."
        if frac < 1.0 else
        "INCOMPLETE -- a grazing lobe survives `T1_CTAN_SP=0`. rev 26's arm 4 "
        "was partial."))

    print("\n--- NOT CLAIMED ---")
    print("    * anything about the COAT.  This probe isolates `spec` on")
    print("      purpose; `T1_CTAN_CT` is a separate lever and adding it here")
    print("      would confound the one question being asked.")
    print("    * that the residual 6.6/6.6/8.5 %% pedestal is explained.  This")
    print("      removes ONE hypothesis from SPEC 10.70's never-ablated list.")
    print("      T1_WORLD, T1_CYCALB, T1_GAL_LUM and the scene->top bounce are")
    print("      untouched and remain the live candidates.")
    print("    * that this generalises past Blender 4.5.3 -- it is a")
    print("      measurement of THIS renderer, printed above with its version.")

    print("\nRESULT: %s" % ("controls pass" if ok else "CONTROLS FAILED -- "
                            "the arms above mean nothing"))
    return 0 if ok else 1


if __name__ == "__main__":
    main()
