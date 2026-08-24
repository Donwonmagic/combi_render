"""audit_adversary.py -- rule 15's half of the outgoing-brief audit.

`audit_brief.py` asks *is what the file says TRUE?* -- paths, switches, counts.
This asks the other question: *what would make it FALSE?*  They are different
instruments and rev 55 onward has required both.  The difference is that this
one RECOMPUTES the brief's headline figures from the source, the photographs
and the renders rather than checking that a string is present.

Written as a script and RUN, so the list a revision reports is what actually
executed rather than what it meant to try.  REPLACE the questions each
revision -- they are about THAT revision's claims, and a question that can no
longer fail is not a control.  Keep the shape: recompute, don't re-read.

REV 59's questions.  Rev 58's twelve are retired with rev 58's claims: they
asked about the roughness lever, the emblem reach control and the gloss frames,
and one of them BROKE for the wrong reason -- it wanted `out/r58_hero.png`,
which does not exist on a clone, so it was reporting the untracked directory
rather than anything about the brief.  That is F58's shape and it is designed
out here: every question below either needs NO render, or SAYS SO and breaks
rather than passing silently (rule 37).

    python3 audit_adversary.py
"""
import os, re, subprocess, sys
import numpy as np
from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))
P = print
bad = []
NQ = [0]

BRIEF = 'NEXT_CONTEXT_PROMPT_rev60.md'


def t(q, ok, d=""):
    NQ[0] += 1
    P("  %-5s %s" % ("ok" if ok else "BROKE", q))
    P("         %s" % d)
    if not ok:
        bad.append(q)


B = open(BRIEF).read()
P("=" * 78)
P("  audit_adversary.py -- what would make %s false?" % BRIEF)
P("=" * 78)

# ---------------------------------------------------------------- the source
import t1_shell as S
import t1_core as T

t("are the door lobes REALLY where the brief says, in the SOURCE?",
  abs(S.DOOR_LOBE_A - 0.7096) < 0.002 and abs(S.DOOR_LOBE_B - 0.9598) < 0.002,
  "t1_shell computes %.4f / %.4f; the brief says 0.7098 / 0.9600 and the "
  "photograph 0.7096 / 0.9598" % (S.DOOR_LOBE_A, S.DOOR_LOBE_B))

t("are they an EXPRESSION of the measurement, or re-typed numbers?",
  "(_DS_ARCH_CX - _DS_FOOT_A) / _DS_ARCH_R" in open('t1_shell.py').read(),
  "a bare 0.7096 in the source is how the next re-measurement gets lost")

t("is DOOR_ARCH_G still DEFINED but no longer used as a BAR?",
  "min(_arch_radial(p) for p in _GAP41_S)" in open('t1_shell.py').read()
  and "_MIN_RAD >= DOOR_ARCH_G" not in open('t1_shell.py').read(),
  "kept as the historical anchor and REPORTED; enforcing it again would "
  "re-forbid the vehicle (F84)")

t("does the dense rail guard actually cover a span, or has it collapsed?",
  len(S._RAIL_DENSE) >= 10 and S._DENSE_SPREAD < 0.030,
  "n=%d over x %.4f .. %.4f, spread %.2f mm -- four raw points cannot see a "
  "sag between them, which is why this exists"
  % (len(S._RAIL_DENSE), S._RAIL_DENSE[0][0], S._RAIL_DENSE[-1][0],
     S._DENSE_SPREAD * 1000))

# ---- CAN the re-based guard still fail?  A guard that cannot is not a guard.
r = subprocess.run([sys.executable, "-c", "import t1_shell"],
                   env=dict(os.environ, T1_DOOR_STALE="1"),
                   capture_output=True, text=True)
t("can the re-based clearance guard still REFUSE?  (it must, or it reports nothing)",
  r.returncode != 0 and "clear the front arch the way the photograph" in r.stderr,
  "T1_DOOR_STALE=1 restores rev 44b's two constants and the import fails, at "
  "0.0653 of ARCH_R against the photograph's 0.0226")

# ------------------------------------------------------- the photograph side
def _load(p):
    a = np.asarray(Image.open(p).convert('RGB')).astype(float)
    return a[..., 0] - 0.5 * (a[..., 1] + a[..., 2]), a.mean(axis=2)

import importlib.util
spec = importlib.util.spec_from_file_location("pd", "probe_rev59_door.py")
pd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pd)
red_p, lum_p = _load(pd.PHOTO)
pu, pv = pd.despike(*pd.trace_lip(red_p, 58, 132, 236, 300, hold=4))
pcu, pcv, pR, prms, pn = pd.arch_fit(pu, pv)
door = pd.walk(lum_p, 60, 239.4, 36, 4, 4.0)
clear = (np.hypot(door[:, 0] - pcu, door[:, 1] - pcv) - pR) / pR

t("does the PHOTOGRAPH really clear its own arch by 0.0226 of ARCH_R?",
  abs(clear.min() - 0.0226) < 0.004,
  "recomputed %.4f R = %.1f mm at u %.1f.  If this is wrong the re-base is "
  "wrong, because this number IS the new bar"
  % (clear.min(), 1000 * clear.min() * S.ARCH_R, door[clear.argmin(), 0]))

t("is the photographed arch's departure really only ~1.2 pct of R?",
  0.008 < prms / pR < 0.016,
  "recomputed rms %.3f px = %.3f %% of R over n=%d.  The brief REFUTES a 48 mm "
  "claim on the strength of this being small (F82/F83)"
  % (prms, 100 * prms / pR, pn))

fb, fa, _, _, framp, _ = pd.feet(pd.walk(lum_p, 60, 239.4, 36, 4, 4.0))
w_photo = (pcu - fb) / pR - (pcu - fa) / pR
t("is the ramp's WIDTH really within ~1 pct of the built width?",
  abs(w_photo / (S.DOOR_LOBE_B - S.DOOR_LOBE_A) - 1) < 0.03,
  "photograph %.4f of R against the built %.4f -- this is the corroboration "
  "that the step was the right SIZE in the wrong PLACE, and it is independent "
  "of where either foot sits" % (w_photo, S.DOOR_LOBE_B - S.DOOR_LOBE_A))

# ------------------------------------------------ rule 37: absent input
for probe, arg in (("probe_rev59_door.py", "out/__nope__.png"),
                   ("probe_rev59_nose.py", "out/__nope__.png")):
    r = subprocess.run([sys.executable, probe, arg], capture_output=True, text=True)
    t("does %s say NO RENDER and exit non-zero with no frame?" % probe,
      r.returncode == 2 and r.stdout.startswith("NO RENDER"),
      "rc=%d, first words %r -- F58 was an ABSENT INPUT dressed as a MOVED "
      "STATISTIC" % (r.returncode, r.stdout.split(".")[0][:58]))

    r2 = subprocess.run([sys.executable, probe], capture_output=True, text=True)
    t("...and with NO ARGUMENT at all, rather than a revision-numbered default?",
      r2.returncode == 2 and r2.stdout.startswith("NO RENDER"),
      "rc=%d -- a default frame under out/ passes only in the tree that wrote "
      "it (F58)" % r2.returncode)

# --------------------------------------------- the renders, which may be absent
side = sorted([f for f in os.listdir('out') if f.endswith('_side.png')]) if os.path.isdir('out') else []
front = sorted([f for f in os.listdir('out') if f.endswith('_front.png')]) if os.path.isdir('out') else []
t("are the frames the brief's item-A and item-B figures need actually present?",
  bool(side) and bool(front),
  "side %r  front %r -- out/ is untracked and starts EMPTY.  If this BROKE, "
  "render before trusting any figure below it, and note that BREAKING here is "
  "the correct behaviour rather than a silent pass" % (side[-1:], front[-1:]))

if side:
    r = subprocess.run([sys.executable, "probe_rev59_door.py", "out/" + side[-1]],
                       capture_output=True, text=True)
    m2 = [l for l in r.stdout.split("\n") if "M2 the built lobes" in l]
    m3 = [l for l in r.stdout.split("\n") if "M3 the photographed front arch" in l]
    t("does the door probe's M2 actually PASS on the shipped tree?",
      bool(m2) and m2[0].strip().startswith("PASS"),
      (m2[0].strip() if m2 else "row absent") + "  -- on out/" + side[-1])
    t("does M3 still FAIL, as the brief says it must BY DESIGN?",
      bool(m3) and m3[0].strip().startswith("FAIL"),
      "if this ever reads PASS without the arch being rebuilt, the instrument "
      "was relaxed rather than the model fixed (F83)")

if front:
    r = subprocess.run([sys.executable, "probe_rev59_nose.py", "out/" + front[-1]],
                       capture_output=True, text=True)
    got = re.search(r"elevation ([0-9.]+) lamp radii", r.stdout)
    t("does the nose elevation really read ~1.18 lamp radii?",
      bool(got) and abs(float(got.group(1)) - 1.184) < 0.05,
      "recomputed %s against the brief's 1.184; the photographs read "
      "1.951-2.127" % (got.group(1) if got else "nothing"))
    c4 = [l for l in r.stdout.split("\n") if "C4 the two independent lamps" in l]
    t("do the nose probe's TWO INDEPENDENT lamps still agree?",
      bool(c4) and c4[0].strip().startswith("PASS"),
      "two lamps disagreeing is how a segmentation failure announces itself; "
      "agreement is the only internal control this instrument has")

# --------------------------------------------------------- brief hygiene
bs = re.findall(r'ALL (\d+) PASS', B)
t("does the brief quote bootstrap's row count as verify_clone's, or vice versa?",
  set(bs) <= {"261"},
  "'ALL n PASS' in the brief: %r -- F66 rewrote the wrong ones of these and "
  "reported the row green.  bootstrap is 9 PASSED / 1 FAILED at rev 59 and is "
  "quoted that way, not as 'ALL 10 PASS'" % sorted(set(bs)))

t("does the brief claim a delivery frame that nobody rendered?",
  "DO NOT RUN IT UNTIL THE MODEL IS RIGHT" in B,
  "the owner held it at rev 58 and items B, C, D and E are still open; the "
  "brief must say so rather than quote a frame nobody made")

t("does the brief still carry the two-letter-scheme collision it inherited?",
  "TWO INCOMPATIBLE" not in B and "§3.11 says" not in B,
  "rev 59 was told its own brief contained two letter schemes and that fixing "
  "it was part of the revision; a leftover cross-reference re-creates it")

P("=" * 78)
P("  %d questions, %d BROKE%s"
  % (NQ[0], len(bad), ("  --  " + "; ".join(bad)) if bad else ""))
P("=" * 78)
