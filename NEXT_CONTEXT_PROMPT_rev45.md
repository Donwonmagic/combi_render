# NEXT CONTEXT PROMPT — rev 45

**Read this whole file before you touch anything.** It is written for a context
that knows nothing about this project. Everything you need to start is here;
everything you need to be *correct* is in `SPEC.md` and `LEDGER_rev44.md`, and
this file tells you where in them to look.

---

## §0. THE ONE THING THAT MATTERS MOST, AND IT IS NOT A MEASUREMENT

**The owner has now reported the same defects three times, and rev 44 "fixed"
them twice.** Verbatim, in order:

1. *rev 44* — "The logo is off. %100 calidad is off. The door does not continue
   on the other side of the wheel well."
2. *rev 44b* — "**The vw still doesn't look right.** Also, the door curves
   around the front of the wheel well and not the back. So you removed too much
   door. Also, the props for the sign seem to meet something from the sides of
   the sign."
3. *rev 44b, after all of the above shipped* — "**Definitely still a lot of the
   same problems.** ... Keep tuning the bus until it is perfect!!"

Rev 44 answered each report with a measurement, a SPEC section and a guard.
Eight SPEC sections (§10.102–§10.109), thirty-odd findings, every guard green.
**And he still sees the same problems.** That is the finding. It outranks
every geometric item on the work list below.

**THE LOOP BETWEEN "MEASURED FIX" AND "HE CAN SEE IT" IS BROKEN. FIXING THAT
LOOP IS REV 45's FIRST JOB.** Three concrete causes are plausible and you can
discriminate between them cheaply — do that before building anything:

* **(a) He is looking at a different thing than you are.** "The VW" may mean the
  roundel's *drawing* (which rev 44b measured and corrected — all six stroke
  ends now reach the ring), or its *size and position on the nose* (which nobody
  has checked this revision, and see item **W1** below, where a first pass
  suggests it may be **60 mm too low relative to the headlamps**). "The logo is
  off" is compatible with both. **You cannot tell from the words.**
* **(b) The fixes are real but sub-threshold at the size he views them.** A
  2.75 mm shader bevel is 1.6 px at 600 px/m. A 0.116 change in glyph reach is
  ~8 px on a 140 px roundel.
* **(c) He is looking at an older image.** Every reply must carry the *current*
  render of the thing being discussed, cropped to it.

### THE TOOL FOR THIS ALREADY EXISTS IN THIS REPO AND REV 44 NEVER USED IT

`mark_rev23_q.py` … `mark_rev37_region3.py` — **eleven scripts**, one per
revision, that render a crop with an **identification box** drawn round the
thing being asked about and put **one question** to the owner. `mark_rev36_ends`
documents the format: *"[C] IDENTIFICATION BOX — a dashed box round the thing
being asked about."* SPEC §10.100.3 calls the format *"one crop, one mark, one
sentence"* and records that it **"settled the SHAPE of a member that had been
unmeasurable for five revisions."**

**REV 45, STEP ONE: write `mark_rev45_q.py`.** Render the current hero, cut
four crops — the **nose emblem**, the **cab door's lower edge over the front
wheel**, the **"100% Calidad" decal**, and the **sign board with its props** —
put a dashed box on each, number them, and ask him **one question per crop**:
*"is this the thing that still looks wrong, and what about it?"* Send the image.

Do not spend rev 45 measuring things he has not pointed at. **Rev 44 did that
and it produced eight correct SPEC sections and an unhappy owner.**

---

## §1. THE OBJECTIVE, IN HIS WORDS

A photoreal 3D model and hero render of **Señor Tacombi** — a 1963 VW T1 Kombi
converted into a taco truck. The owner supplied a catalogue-grade product render
of a school bus as the bar and asked for *"the very highest resolution,
fidelity, and detail possible. Cutting edge stuff, and I need you to guide it."*
And: **"Keep tuning the bus until it is perfect!!"**

**The standing instruction, from the original brief and still in force:**

> **WHERE THIS BRIEF AND THE MACHINE DISAGREE, THE MACHINE IS RIGHT — say so and
> correct the brief in the same revision.**

That applies to *this document* too. If you measure something here to be wrong,
it is wrong; fix it here in the same revision you find it.

---

## §2. PROVE THE TREE. THREE THINGS BIT REV 44 HERE.

```bash
cd /home/user/combi_render
git branch --show-current        # must be claude/tacombi-combi-rev-44-h4ipmg
git log --oneline -5
./verify_clone.sh                # expect 65 PASSED, 1 FAILED (see below)
```

* **`verify_clone.sh` is the content verifier.** It checks by SYMBOL AND
  CONTENT, never by line number. It currently reports **65 PASSED, 1 FAILED**,
  and the one failure is *"modified tracked files got 1 want 0"* — i.e. it fires
  whenever the tree is dirty. **On a clean checkout it is 66/0.** Five counts
  were re-based in rev 44b (`DOOR_ARCH_G`, `_G_BUILD`, `_arch_radial`, the
  `0.024426` citations and the `nolita` citations); **each carries a comment
  saying exactly why it moved.** Its own rule stands: *a failing line is a
  FINDING — report it with its actual value; do NOT edit this script to make it
  pass.* Re-basing a count because the code legitimately changed is allowed
  **only with the reason written in above it**, which is what those five now do.
* **Blender is not installed as an application.** `download.blender.org` returns
  403 through the egress proxy. Blender 4.5.3 is obtained by
  `pip install bpy==4.5.3`, and **two shims** reproduce the paths eight files
  hard-code:
  * `/tmp/blender/blender` — the CLI
  * `/tmp/blender/4.5/python/bin/python3.11` — the interpreter. **This one must
    `exec`, not be a symlink.**
  If either is missing, rebuild them. **Do not edit the eight files that
  hard-code the path.**
* **Network:** `WebSearch` works. `WebFetch` and `curl` are **403 on every
  domain** except **`raw.githubusercontent.com`**, which returns 200 — that is
  the only route for image files.

### Build, verify, render

```bash
/tmp/blender/blender -b -P build.py                    # T1_SUB defaults to 2
T1_VERIFY=1 /tmp/blender/blender -b -P build.py        # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=hero,side,detail_f T1_PFX=r T1_RX=1400 T1_RY=960 T1_SAMP=56 \
  /tmp/blender/blender -b -P build.py                  # -> out/r_hero.png etc.
```

Useful env: `T1_SUB` (subdivision, **2 is the guarded case**), `T1_SAMP`,
`T1_ADAPT`, `T1_RX`/`T1_RY`, `T1_PFX`, `T1_OUT`, `T1_SAVE`, `T1_KEY`,
`T1_SCENE=playa`, `T1_CLAY`, and the **ablation switches** `T1_NOBEVEL`,
`T1_NOCABFILL`, `T1_CATCH`, `T1_GRAIN`, `T1_BPILLAR`, `T1_SPEC`, `T1_VT`.

**A build at T1_SUB=2 takes ~70–100 s. A 3200×2133 hero at 192 samples takes
~55 min on this CPU. A 4800×3200 at 300 samples was quoted at 4½ hours and was
killed — do not start one.** The owner has twice said *"Kill it. Don't waste the
computer."* Render small and often; render big once.

---

## §3. THE SPINE — READ THESE, IN THIS ORDER

1. **`LEDGER_rev44.md`** — the burn-down, in four classes. **This is the spine.**
   * **CLASS 1 GREEN-REQUIRED** — must pass, re-run every revision.
   * **CLASS 2 RED-BY-DESIGN** — probes with KILL controls *written to fail*.
     **Going green is a regression.** Read each probe's **own summary line**,
     never its exit code.
   * **CLASS 3 OPEN FINDINGS** — the burn-down. **Done = this table empty.**
     Findings 1–37; 1, 3, 4, 15, 28, 29, 32–37 are closed, the rest are open.
   * **CLASS 4 UNINSTRUMENTED** — no probe exists, so "green" is meaningless.
     **The cab interior was added to this class in rev 44b.**
2. **`SPEC.md`** — ~8600 lines, §10.1 … §10.109. Each §10.x is a dated record of
   one revision's reasoning. **Sections are never deleted**; a retracted one
   gets a banner at the top pointing at its retraction (see §10.100 → §10.102).
3. **`HANDOFF_rev44.md`** — rev 44's narrative, plus §10–13 for the rev-44b
   fidelity pass.
4. **`STATE.md`, `README.md`, `START_HERE.md`** — orientation.

---

## §4. THE MAP — WHAT LIVES WHERE

| file | what it owns |
|---|---|
| `t1_core.py` | primitives (`solid_prism`, `revolve`, `cylinder`, `rrect`, `sweep`, `conform_*`, `flank_y`, `ZB`), the rake/ride-drop constants, **`vw_bars()` — the VW emblem, shared by nose and hubcaps** |
| `t1_shell.py` | the body: windscreen, cab-door glazing, serving bays, wheel arches, **`DOOR_GAP` and the cut outline**, roof lids and their props, panel gaps. **Most module-level asserts live here and fire at import.** |
| `t1_detail.py` | tyres, rims, hubcaps, bumper, lamps, mirrors, wipers, **`cab_fitout()`**, `door_hinges()`, the galley and its dressing, `vw_logo_fit()` |
| `t1_mats.py` | all 42 materials, the shared `WEATHER` node group, `round_edges()` (the shader bevel), `rough_field()` |
| `build.py` | the pipeline: loft → arches → solidify → cut → glaze → fit-out → brightwork → signwriting → **step 8b shear (`RIDE_DROP`)** → materials → `round_edges()` → optional verify → optional preview |
| `studio.py` | cyclorama, lighting, **`cabin_fill()`**, cameras, **`fit_view()`/`subject_bbox()`**, `render_set`, the compositor |
| `verify.py` | SPEC §9's machine-checkable rows, run by `T1_VERIFY=1` |
| `audit.py` | watched prints |
| `folk_gen / script_gen / cal_gen / sign_gen / lid_gen / texgen` | the painted artwork, baked to `tex/*.png` |
| `probe_*.py`, `mark_*.py` | instruments and owner-question renders |

**Reference photographs (8, all tracked):** `ref_side.jpg` (1024×768, the
primary flank), `ref_source.jpeg` (**246×197 — a thumbnail; resolution is the
binding constraint on almost everything**), `ref_workshop.jpg` (three-quarter,
**inadmissible for metrics on the door plane** — §10.62, §10.73),
`ref_rear34.jpg`, and the four Nolita frames — `ref_nolita_doorshut.jpg`
(**square-on, door shut, the whole cab-door outline**), `ref_nolita_flank.jpg`,
`ref_nolita_front34.jpg` (**the clearest roundel in the set**),
`ref_nolita_front34b.jpg`. The owner has confirmed Nolita and Playa are **the
same physical vehicle**, so Nolita geometry is admissible.

---

## §5. WORK LIST FOR REV 45

**W0 — CLOSE THE LOOP. `mark_rev45_q.py`.** See §0. Nothing else starts until
this is sent.

**W1 — THE ROUNDEL'S PLACEMENT ON THE NOSE, WHICH NOBODY HAS CHECKED.** Rev 44b
fixed the emblem's *drawing* (§10.107 — all six stroke ends now reach the ring
at 0.840 of its radius; four of six had been floating since rev 15). It did
**not** check where the badge sits. A first pass on `ref_nolita_front34.jpg`:

* roundel bbox cols 152–192, rows 192–257 → **centre (172.0, 224.5), vertical
  D 66 px**;
* a bright-blob centroid in rows 240–299 gave **row 258.5**, which would make
  *(lamp row − roundel row) / roundel D* = **0.515** against the model's
  **0.300** — i.e. the badge would be **~60 mm too low relative to the
  headlamps**.

**DO NOT ACT ON THAT NUMBER.** The blob is glare-contaminated: thresholding at
195 returns **one blob 131 px wide spanning cols 150–280**, which is the cream
nose, not a lamp. **The correct method is to fit the headlamp's CHROME RIM as a
conic** — the technique §10.99/§10.10 already use for the rim flange and the
roundel — or to use the *lit lens's warm chroma* rather than its brightness. Get
the lamp's geometric centre, then re-take the ratio. Vertical extents only: the
frame is a three-quarter and a rotation about a vertical axis preserves vertical
ratios (§10.107.2's rule).
**If it survives, this is very likely what "the logo is off" has meant all
along**, and note that `HL_Z` moved **down 97 mm** in rev 44 (§10.24 item 3,
Report 3 applied after 34 revisions) — so this ratio has *just* changed and has
never been checked against a photograph since.

**W2 — "100% CALIDAD" (ledger finding 5, open).** Re-measured in rev 44: the
defect is **colour, not position**. Core, top-decile saturation: model
**(213,131,111)** G/R 0.617 against reference **(237,103,90)** G/R 0.434 — it
renders **orange where the photograph is red**, and not from exposure (the model
is *darker* overall and still less saturated, the wrong way round for a
washout). Two causes ruled out **by test**: `WEAR['calidad']` is not the lever
(re-rendered at 0.22, core bit-identical), and the material adds no cream. The
source is the texture: `tex/calidad.png` core is **(235,112,20)** while
`cal_gen.py:55` declares `RED = (214,46,30)` — the burst is RED-filled at `:93`
but the **RED→ORANGE→YELLOW gradient at `:106` dominates the area**. This is a
re-derivation of the decal's colour design, in `cal_gen.py`. **He has reported
it twice.**

**W3 — "SEÑOR TACOMBI" LEGIBILITY (ledger finding 30, open, HIS REQUEST).**
Contrast script-ink to body-red is **1.734** built against **2.748**
photographed (Michelson 0.269 vs 0.466). But the attribution is **retracted**
with finding 29 — the photograph's red flank is in shade, which lifts its
contrast, and the render's red is correct to its own albedo to **0.000**. So
this is an **art-direction ask, not a fidelity bug**. Note the obvious lever
runs **backwards**: finding 19 says `senor.png` emits opaque mean (205,194,200)
against a measured target of (127.4,124.9,130.0), so darkening the ink toward
its target makes legibility **worse** (190/109 → 126/109). Any fix is a
deliberate departure from a measurement and **needs his sanction**.

**W4 — THE CONTACT SHADOW (`optics-6`, open since rev 12).** The last visible
gap against his reference: **the vehicle floats.** History in
`studio.cyclorama`'s comment and §10.109.4 — rev 12 measured the ground under
the tyre at 177.00 against open ground at 177.00; rev 17's matte tap corrected
that (the alpha pool reaches **0.4980**) but it is **0.0038 mean alpha in the
4–30 px band directly below the silhouette**, so the composite over white moves
a few code values. The obvious lever is **refuted**: `T1_CATCH=0` does produce a
shadow (175.2 mean below the contact) and brings back a 166-grey sweep with a
hard horizon line, which **§6 forbids** — the backdrop is locked to pure white.
The cause is **the rig**: a 16 m strip plus a 0.76-albedo floor fills the
vehicle's own shadow. **No photograph of this vehicle on a white sweep exists**,
so there is nothing to calibrate against. **This is art direction — put it to
him.** The template if he says yes is `cabin_fill()` (§10.105): a declared,
ablatable presentation device with its ablation reported.

**W5 — FASTENERS.** `probe_rev44_fidelity.py` counted **rivet 0, bolt 0, screw
0, nut 0, latch 0** and, before rev 44b, **hinge 0**. Four cab-door hinge
assemblies now exist (§10.104.6) and they show the pattern: place hardware off a
member that is **already guarded** — `DOOR_GAP`'s front edge for the rake,
`t1_core.flank_y` to seat it on the skin — never by eye. Next tranche, by
return per effort: **rivets along the counter nosing and the gallows, bumper
bolts, hatch latches, drip-rail clips.**

**W6 — THE CAB IS CLASS 4.** §10.104's furniture is type-correct 1963 T1 and
**not measured** — no frame resolves the cab interior. It is placed off members
that *are* fixed (the cab floor, `Z_SILL`, the windscreen corners `P_TOP`/
`P_BOT`, the column, the rev-8 seat footprint) so it cannot drift independently
of the shell, but that is a **coupling, not a measurement**. Related and open:
the **driving position** is 622 mm from the seat back to the hub, ~150 mm more
reach than a T1 driver has; closing it needs the seat's fore-aft position, which
is rev-8 authored.

**W7 — THE BODY'S LOWER EDGE IS UNMEASURED, AND DO NOT RE-DERIVE IT THE WAY REV
44b DID.** §10.106.7: I raised a ~49 mm discrepancy, settled the datum question
(one continuous rocker, no valance step) and published it — then killed it.
`ref_nolita_doorshut.jpg` **cannot see the edge**: down column 132 the red runs
(151,31,17) → (80,19,16) and then rows **278–298 are RGB (0,0,0)**, twenty-five
rows clipped to pure black. Sweeping the mask R>90 → R>30 does not move the
answer; at R>20 it jumps to **303, the floor**. `ref_side.jpg` disagreed in
**sign**, and that trace was bad too — at cols 900–920 the pixels are neutral
(R≈G≈B) and an `R > G*1.25` mask passes warm grey shadow as red. **`RIDE_DROP`
is not implicated by anything.** If you want this number you need a frame with
**open shade or fill under the sill** and a **chroma** mask with a stated rule.

**W8 — REMAINING OPEN LEDGER ITEMS**, unchanged: finding 2 (the body has **no UV
layout at all**, ~56 % self-overlap — sized, not fixed), 13 (the off flank at
804.9 mm, graded **E**, never adjudicated), 14 (Nolita authorised for geometry
at rev 15, **not one frame measured** until rev 44), 16 (a **trunk lid** —
`grep -c trunk` is 0 and 0), 17 (counter clutter), 21, 22 (**89 unverified
findings in `AUDIT_RECOVERED.md`**), 31 (the hubcap ratio — **measured against
him and not moved**, his call).

---

## §6. WHAT ONLY THE OWNER CAN GIVE

`PHOTOS_WANTED_rev44.md` is the standing list. **Ranked, and the top two have
not moved in three revisions:**

1. **The off side** — a flat-on right flank. The off flank sits at 804.9 mm,
   graded **E**, and **we do not know what is painted on it**; the model carries
   a de-mirrored variant on an assumption made at rev 10 and never tested.
   *A three-quarter view is useless here.*
2. **Anything settling the absolute roof height** — `H_ROOF` was retired as an
   accuracy target at rev 22 and never replaced. The build prints a paragraph
   every run saying the figure is unsupported. **One photo of him standing
   beside it, plus his height, closes an eleven-revision hole.**
3. **NEW, rev 44b — a square-on CAB INTERIOR frame.** The cab is class 4.
4. Head-on rear, and the **trunk lid** question.
5. The door, full outline, **with the art on it**.

**Do NOT ask him again for:** the over-rider assembly, the signboard, region 3,
the ten flower heads, tyre diameter, the counter slab, break-to-sill, the
Z-ladder's gate, the door outline's arch clearance, whether it is one vehicle
(**it is**), whether the door art stretches (**it does not**), or whether the
workshop frame may be used for letterforms (**it may, geometry only**).

---

## §7. SETTLED — DO NOT RE-OPEN

* **The paint's finish.** §10.104.8 refuses it **in writing**: the reference is a
  factory-clean product render, this is a weathered 1963 working truck, and
  §4.3's chalky finish (`Roughness` 0.420, `Coat Weight` 0.02) is **measured** —
  rev 3's mirror clearcoat is what made the red read salmon at 0.37 against
  0.82. **The detail bar transfers. The finish does not.** Read §10.104.8 before
  touching `Roughness` or `Coat Weight`.
* **Finding 29 — "the body red renders 2× too light".** **Retracted, it was a
  unit error**: a linear albedo ratio compared against gamma-encoded pixels.
  Encoded, the albedo is 104.4/207.0 = **0.504** against the render's **0.504**.
  The render reproduces its own albedo to 0.000.
* **§10.100's door wrap.** Retracted by §10.102 and **partially restored** by
  §10.106 — the door's bottom rail is **flat over the arch** and drops around
  the **front** of the wheel well only. Both halves are measured; do not
  re-litigate either without a new frame.
* **The rear bumper was removed after the conversion** (SPEC rev 6 §2.4); the
  over-rider bar and posts were **withdrawn by the owner** at rev 37.
* **There is no fourth serving bay.** Aft of bay 3 is solid sheet metal carrying
  the Calidad decal.

---

## §8. THE RULES. EVERY ONE OF THESE WAS EARNED BY A DEFECT.

1. **A claim in prose is not a guard** (§10.45). If it matters, assert it.
2. **A constant tuned against another constant must be EXPRESSED in terms of
   it** (§10.25), never typed. This rule has been broken and cost the emblem
   twice.
3. **Read each probe's own summary line, never its exit code.**
4. **Never put a figure in an acceptance test unless you watched it print**
   (rev 13). Third instance was a figure quoted from a **thirty-revision-old
   comment**.
5. **Do not inherit a guard's rationale along with its shape** (rev 23).
6. **An ordinal fact licenses a SIGN, never a SHAPE** (§10.102.8). If an ordinal
   reading is about to force a *construction*, stop and find a frame that can
   carry the magnitude.
7. **A leading question is not evidence, even when the answer is yes**
   (§10.102.8). §10.100 was built on one and took thirty revisions of geometry
   with it.
8. **A measurement's window is part of the measurement** (§10.106.6). §10.102
   published "flat over 62 px of door" — true — and then guarded "the door is
   flat". **State the window in the guard, not just the prose.**
9. **A threshold-based "lowest X" trace is only valid if the feature's FAR SIDE
   is resolved** (§10.106.7). Check what is on the other side of the edge, and
   whether the sensor can still see it, before you publish the edge.
10. **A detail you cannot see is not a detail** (§10.105.7). Every detail pass
    ships with the frame that shows it, or it does not ship.
11. **When a fix cannot be built at any tolerance, suspect the thing it is
    fixing** (§10.102.8). Three constructions each stopped by a different guard
    is the geometry telling you the feature is not there.
12. **Add the guard in the same edit as the change.** In rev 44b the prop guard
    fired on my own inverted "fix" **on the first build**, and the wheel/dash
    clearance guard caught a **173 mm interference** that neither member had
    ever been solid enough to reveal.
13. **Inventory the frames you already hold before asking the owner for a new
    one.** §10.102's refutation took eleven minutes on a file that had been
    tracked for two revisions and was named in the wanted-list in the same
    paragraph that asked for it.
14. **Prefer dimensionless measurements.** The three available scales on
    `ref_nolita_doorshut.jpg` span **3 %** (arch radius 105.9, rear rim OD
    104.2, hub-to-hub wheelbase 107.4 px/m). Anchor to two features of the same
    member and the scale question disappears (§10.106.3).
15. **Retract in the same revision you find the error, in SPEC, in the ledger
    and to the owner.** Rev 44b retracted three of its own claims — a docstring
    that contradicted its next print, a prop "sign error" that was not one, and
    a 49 mm finding that no frame could see.

---

## §9. THE STATE OF THE MACHINE AT HANDOFF

```
build            T1_SUB=2, 257 642 v, clean
verify.py        VERIFY: 0 fail, 0 warn
verify_clone.sh  66 PASSED, 0 FAILED on a clean tree
objects          162   materials 42   textures 7 (1K-4K)
triangles        ~656 000 before the cab and hinges; 77 % of it in T1_body
bevels           shader-level on all 42 materials, radius GAPW/2 = 2.75 mm
branch           claude/tacombi-combi-rev-44-h4ipmg   (push here, nowhere else)
```

**Rendered and delivered this revision:** `out/fx_side.png`, `out/fx_hero.png`,
`out/fx_detail_f.png` (1400×960), `out/HERO_hero.png` (3200×2133, **front wheel
clipped — superseded**), `out/HERO2_hero.png` (3200×2133, framing solved by
`fit_view()`).

**Go and read §0 again before you start.**
