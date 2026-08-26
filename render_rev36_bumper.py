# render_rev36_bumper.py -- rev 36, READ-ONLY, not part of the build
#
# Renders the CURRENT build's front bumper / over-rider assembly so the
# photograph can be shown BESIDE a render of the build, per the standing rule.
#
# It does NOT edit studio.py.  It imports the scene, then adds one view to a
# LOCAL COPY of views() and renders that.  No build file is touched, so this
# script cannot change what ships.
#
# CONTROL: the added view name must not already exist in views(), or this
# would be silently overriding a shipped camera.  Checked, and it refuses.

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.pop("T1_PREVIEW", None)      # build must not render on import
import build as B                        # noqa: F401
import studio as ST

VIEW = "rev36_bumper"
_V = ST.views()
if VIEW in _V:
    print("REFUSING: '%s' already exists in studio.views() -- this script "
          "would be shadowing a shipped camera." % VIEW)
    sys.exit(1)

_orig_views = ST.views
def views(dist=1.0):
    v = _orig_views(dist)
    # Front, slightly to the serving (+y) side, a little above the bar, on a
    # long lens so the two hoop ends and the blade read at the same scale.
    v[VIEW] = dict(loc=(6.30, 1.35, 1.12), tgt=(2.05, 0.00, 0.55),
                   lens=95, focus=(2.10, 0.35, 0.55), fstop=8.0)
    return v
ST.views = views

# rev 58, F51: ONE definition of the rig, in studio.rig().
# STATED BEHAVIOUR CHANGE, not a silent one: the three calls this replaces did
# NOT include cabin_fill, so this rev-36 bumper preview rendered the cab dark
# while every other view in the project lit it (SPEC 10.105, "the cab was built
# and then rendered invisible").  rig() includes it.  Nothing gates this script,
# and the change moves it TOWARDS the shipped rig rather than away from it.
ST.rig(key=1.0, scene="studio")
ST.render_set([VIEW],
              os.environ.get("T1_OUT", "/tmp/prev"),
              prefix=os.environ.get("T1_PFX", "r36"),
              res=(int(os.environ.get("T1_RX", "1600")),
                   int(os.environ.get("T1_RY", "1100"))),
              samples=int(os.environ.get("T1_SAMP", "40")),
              transparent=True, log=print)
print("done")
