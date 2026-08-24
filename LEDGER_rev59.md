# LEDGER rev 59 — every number, with where it came from

**Read `NEXT_CONTEXT_PROMPT_rev60.md` for the map. This file is the arithmetic.**

Grades follow `OPEN_FINDINGS.md`: `MEASURED-rev59` means a script in this repo
printed it during this revision.

---

## §1. PICKUP — MEASURED, NOT TRANSCRIBED, AND THE HANDOFF WAS WRONG

```
rev 58 and 58b WERE MERGED, through PR #18 (fbcec2e).
HEAD claude/new-session-ocymb5  =  0 ahead / 0 behind origin/main.
git diff --name-only HEAD...origin/main  ->  EMPTY.  No photographs arrived.
bootstrap.sh  9 PASSED, 1 FAILED  -- row 9, STRANDED:
              origin/claude/bus-model-rev57-yvrlhi(6 commits, 16 files)
              the string is byte-identical to the one the brief predicted.
verify_clone.sh  ALL 261 PASS on the clean tree at pickup.
```

**THE INCOMING HANDOFF SAID THE OPPOSITE.** It stated *"HEAD =
`claude/combi-render-rev-58-lg0746`, 13 ahead / 0 behind — rev 58 and 58b are
UNMERGED"* and told me to ask the owner whether those 13 commits go to `main`
via a PR. They were already there. **That is the FIFTH revision running in which
the prose guessed the merge state and the machine corrected it**, and it is why
`CLAUDE.md` §"Before you touch anything" item 1 exists. It also means the
question the handoff wanted put to the owner **must not be asked** — there is
nothing to merge.

**AND THE NINTH DELETION HAPPENED, ON SCHEDULE.** `git fetch --prune` printed

```
 - [deleted]         (none)     -> origin/claude/new-session-ocymb5
```

which is **the branch this revision was told to develop on**, deleted before this
revision had pushed anything — the **FOURTH RUNNING** to hit the current
revision's own branch. The rev-59 brief predicted it in those words (*"Expect it
at rev 59"*). It was recreated by the first push. **Expect it again at rev 60.**

**THE TOOLCHAIN WAS ABSENT AGAIN.** `/tmp/blender/blender` did not exist and
`bpy` was not importable. `./bootstrap.sh` rebuilt both; the
`pip install bpy==4.5.3` branch ran and worked, for the third revision running.

**AND `out/` WAS EMPTY, WHICH THE HANDOFF ALSO GOT WRONG.** It said *"`out/` is
untracked but NOT empty"* and warned about mtimes. `out/` was empty on the clone.
Every frame in this ledger was rendered this revision.

---

## §2. THE BASELINES, RECORDED BEFORE ANYTHING WAS TOUCHED

On `out/r59a_*.png` (T1_SUB=1, 1600×1100, 96 spp, one build, three views):

| gate | reading | matches the handoff? |
|---|---|---|
| `flank_compare.py` | **FAIL 1 of 4**, worst region **`i` 0.685**; ink area 0.9796, aspect 2.3686 vs 2.3259, IoU 0.7587 | yes, exactly |
| `gloss_compare.py` | **FAIL 0.426** against a 0.60 bar; brightest 1 % at 0.146 | yes, exactly |
| `gloss_compare.py --selftest` | **PASS**, exposure-free, 0.6036 at ×0.70 / ×1.00 / ×1.40 | — |
| `probe_rev45_nose.py` | **8 checked, 0 FAILED** — and it had never been invoked | see §5 |

---

## §3. ITEM A — THE CAB DOOR. THE ARITHMETIC.

### §3.1 The instrument, and its five controls

`probe_rev59_door.py`. Every control runs the **identical pixel code** on the
side render, whose front arch is a circle of `ARCH_R` about `X_AXLE_F` **by
construction**, so the truth is computable from the source.

| control | result |
|---|---|
| C1 hub finder recovers the model's own front axle | **du +1.28 px, dv +1.62 px** = +4.7 mm, +6.0 mm |
| C2 circle fit recovers the render's own `ARCH_R` | **R 101.22 px against 101.29, −0.07 %**; centre du +0.16, dv +0.13 |
| C3 the render's arch fits a circle | **rms 0.239 px = 0.237 % of R** — the instrument floor |
| C4 lobe feet recover the built `DOOR_LOBE_A/B` | aft **+0.67 px (+2.5 mm)**, fwd **−2.19 px (−8.1 mm)** |
| C5 the whole chain, end to end | A **−0.65 %**, B **+2.48 %** |

**C1 FAILED FIRST, AND THE FAILURE WAS MINE.** The hubcap mask thresholded
luminance inside a box that the **white studio floor** reached, dragging the
fitted centre 35.7 px low — a 132 mm error that would have propagated into every
figure below. Caught by painting the mask and looking at it (rule 8). Excluding
near-white unsaturated pixels fixed it.

**AND THE CROWN-COLUMN METHOD FAILED ITS CONTROL TOO, WHICH IS §3.4's FINDING.**

### §3.2 The two stale constants

```
DOOR_LOBE_A = (91.1 - 56.0) / 39.54      # 0.8877
DOOR_LOBE_B = (91.1 - 46.0) / 39.54      # 1.1406
```

* **The FEET are right.** Re-traced by a tracked walk along the shut line:
  **aft 56.069, fwd 46.741**, ramp fit **rms 0.112 px**, and identical to three
  decimals across three different walk parameter sets (half=4/5/6, depth 2/3/4).
  rev 44b had 56.0 and 46.0; §3.10's re-measure had 56.19 and 46.84.
* **`91.1` is the WHEEL HUB column.** The datum it is used against is
  `_ARCH_CX`, the **arch's** centre. Fitted on the lip, the arch centre column is
  **82.53** — **9.83 px apart**. Rule 34 exactly: the requirement changed object.
* **`39.54 px` is not the arch's radius in that image.** It is
  `ARCH_R × 105.9`, a scale obtained by **assuming the radius it is then used to
  measure**. Fitted directly: **37.28 px**.

### §3.3 The answer, and why it is free of the ±4 % parallax floor

```
DOOR_LOBE_A = (82.53 - 56.069) / 37.28 = 0.7096
DOOR_LOBE_B = (82.53 - 46.741) / 37.28 = 0.9598
```

against a built 0.8877 / 1.1406 — **aft by 66.5 mm and 67.5 mm**.

**BOTH FEET MOVE BY THE SAME AMOUNT, TO 1 mm.** That is a translation, not a
re-shaping, and it is corroborated independently: the ramp's **WIDTH** in the
photograph is **0.2502 of R** against the built **0.2529**, **−1.07 %**. The step
was the right SIZE in the wrong PLACE.

**NO PARALLAX TERM.** The door line and the arch lip are **both on the flank
plane**, so this is a ratio of two flank-plane lengths in one frame. It carries
no px/m. §3.10 attached a ±4 % floor to its own figure because it mixed the
flank plane (the crown) with the wheel plane (the hub); nothing here does.

**NOT 95 mm.** §3.10 said ~95 mm from `A = 41.50 px`. Measured here, A is
**38.66 px** vertically and the fitted R is **37.28 px**; the render control
recovers A to **+1.7 %** and R to **−0.07 %**, so the smaller ruler is the
supported one. **§3.10's 95 mm is retracted here, in the register (F81) and in
the rev-60 brief.**

### §3.4 §3.10's SECOND claim is REFUTED — it is a method artefact (F82)

§3.10: *"the real lip sits up to 0.13 A ≈ 48 mm inboard of a circle"*, from
r/A about (crown column, hub row), reading **1.0241 → 0.9582 → 0.9129 → 0.8723**.

**Run that same sweep on the side render, whose arch is EXACTLY a circle:**

```
fwd r/A  1.0155  1.0461  1.1136  1.1356  1.1737  1.2043   (10..60 deg)
aft r/A  0.9204  0.8800  0.8417  0.8081  1.2679  0.7537
A = 202.8 px on a truth of 101.29   ->   and after the folk-art fix, 103.05 (+1.7 %)
```

The method invents swings of **±0.07 R** on a shape with none, and a first pass
put A out by a **factor of 2.0** because thin folk-art motifs satisfied the
red→black test (fixed by requiring the fall to be SUSTAINED for 8 rows).
**§3.10's 15 % fall sits inside its own artefact band.**

The weak link is the **crown column**: near the crown the arc is flat, so row
noise maps to enormous column error — **+5.5 px** by minimum-row and **+26 px**
by parabola, on a render where the truth is **0**.

**A circle fit over a radius-scaled window replaces it**, and its window
sensitivity was measured rather than assumed:

| half-window | render centre du | render R error | rms |
|---|---|---|---|
| 40 px | +3.20 | −14.94 % | 0.292 px |
| **70 px** | **+0.29** | **−0.52 %** | **0.237 px** |
| 85 px | +0.09 | −0.53 % | 0.247 px |
| 120 px | +3.03 | +9.11 % | 5.357 px |

### §3.5 What the arch's real departure is (F83)

At matched **angular** span, photograph **1.171 % of R rms** (n=54) against the
render's **0.237 %** on a known circle — **5.0×** the floor, so the departure is
**REAL**. On `ARCH_R` that is **4.4 mm rms**, not 48 mm, and it is **below SPEC
§2's ±8 mm tyre-gap lock**.

**THE ARCH IS THEREFORE NOT REBUILT, AND THAT IS A RESULT, NOT AN OMISSION.**
The forward half below the door line is deep shade with the white bumper cutting
in; my own forward trace dies at 30° and, over the span it does reach, **RISES**
(1.0075 → 1.0287 → 1.0358) rather than falling — so §3.10's *"both flanks fall
symmetrically"* is not reproducible either. Building a symmetric non-circle would
be inventing the half we cannot see. **`probe_rev59_door` M3 fails BY DESIGN and
must keep failing** until the arch is rebuilt or the owner rules.

**AND THE REBUILD TURNED OUT NOT TO BE NEEDED FOR ITEM A.** §3.10 says the two
are "ONE job" because moving the lobes trips the assert. It does trip — and the
assert was the thing that was wrong (§3.6).

### §3.6 The assert forbade the vehicle (F84)

Moving the lobes gives `_MIN_RAD` **0.00660 m = 0.0177 of `ARCH_R`**, and

```
AssertionError: cab-door shut line is CLOSER to the front wheel arch than
rev 41's was: min radial clearance 0.0066 m against rev 41's 0.0244 m.
```

**So what does the vehicle do?** Traced on the photograph — the door line's
clearance from the photographed arch circle, column by column:

```
  u 52.0  +0.0970 R  +36.2 mm        u 48.0  +0.0230 R   +8.6 mm
  u 50.0  +0.0464 R  +17.3 mm        u 47.0  +0.0226 R   +8.5 mm   <- MINIMUM
  u 49.0  +0.0306 R  +11.4 mm        u 46.0  +0.0389 R  +14.5 mm
```

**The real vehicle clears its own arch by 0.0226 of `ARCH_R` = 8.4 mm.** rev 41
demanded **0.0653 R = 24.4 mm**, nearly **three times** it. The bar was an
accident of rev 41's outline, and it forbade the vehicle. The second assert's
10 mm floor is refuted by the same reading.

**Its inherited rationale is already refuted in this repo.** `SPEC.md` §10.62,
quoted verbatim from line 2491: *"That does not transfer: all six crossings were
live at SUB=2 with zero non-manifold edges."*

**THE COMPANION TEST IS NOT A SECOND PROXY.** `CLAUDE.md` licenses a re-base
*"with the cause named AND a companion row that makes the cause separately
testable"*. The collapse is a TOPOLOGY event, and `verify.py` already tests it
**directly**, with no threshold to tune: *"no boolean may have rolled back"* and
the shell's non-manifold edge count. Both pass:

```
T1_SUB=1  VERIFY: 0 fail, 0 warn   shut line door+1 / door-1: 100 % open
T1_SUB=2  VERIFY: 0 fail, 0 warn   shut line door+1 / door-1: 100 % open
STATE.md  cutters rolled back: none   non-manifold edges (body): 0
```

`DOOR_ARCH_G` is **kept and REPORTED** as the historical anchor in the new
guard's message rather than enforced as a bar.

**ABLATION `T1_DOOR_STALE=1`** restores rev 44b's two constants and the new
guard **REFUSES** them, at 0.0653 R against the photograph's 0.0226 R.
**Watched failing.**

### §3.7 `_RAIL_SPAN` — the warned-of weakening did NOT happen, and it is armed anyway

The handoff warned `_RAIL_SPAN` *"weakens SILENTLY"* when `_LOBE_XA` moves aft.
**Measured both ways: n=4 and `_BOT_SPREAD` 16.000 mm before AND after** —
`DOOR_GAP` simply has no table points between the rear corner and the ramp. So
the warning did not materialise, **but four points cannot see a sag between
them**, and the object the boolean uses is `DOOR_GAP_S`, not that table. A second
guard is armed densely on the outline that actually cuts:

```
_RAIL_DENSE  n=10  x 0.9881 .. 1.4735  spread 14.63 mm   (bar 30 mm)
```

**Both end corners are excluded by 60 mm and the span is stated in the message.**
That matters: reading the rear corner as rail sag reports **76.7 mm** of descent
that is not there (the outline turns UP there, z 0.8700 against the rail's
0.8007). The photograph holds the same feature flat to **0.81 px = 8 mm**.

### §3.8 After the fix

```
probe_rev59_door.py out/r59b_side.png
  C1..C5 PASS
  M1 the ramp's WIDTH agrees with the built width        -0.01 %
  M2 the built lobes sit where the photograph puts them  PASS -- +0.1 / +0.1 mm
  M3 the arch is a circle to the render's own floor      FAIL BY DESIGN (F83)
```

**AND IT WAS LOOKED AT.** Before/after crops of `out/r59a_side.png` and
`out/r59b_side.png` at the front arch: the ramp has moved aft and now descends
alongside the arch's forward lip with a narrow strip of red between, which is
what `ref_nolita_doorshut.jpg` shows. Before, it stood well forward of the arch
with a wide gap.

### §3.9 The probe re-typed the constants, and its own controls caught it

The first cut of `probe_rev59_door.py` pasted rev 44b's `DOOR_LOBE_A/B` as
literals. The source moved in the same revision — **by this probe's own
finding** — and the controls then graded the new build against the old numbers
and reported the **fix** as a **−20.56 % miss**. It now reads `t1_shell` live.
**A probe that re-types the thing it is checking is checking its own typing.**

---

## §4. ITEM B — THE NOSE

### §4.1 The orthographic elevation, built and shipped (F87)

`probe_rev59_nose.py`, on `T1_PREVIEW=front` — which `studio.py` has carried all
along and which, as §3.11 says, nothing in this tree had ever pointed at the
nose. Orthographic, so it removes perspective and plan-curvature bias entirely:
**no camera to recover, no `flank_kv`, and F26's camera ambiguity never arises.**

| control | result |
|---|---|
| C1 two headlamp blobs found | 2 |
| C2 symmetric about the frame's own centre column | midpoint **800.23** against 800.0, **+0.23 px** |
| C3 same size and height | radii 34.50 / 33.00 px; rows 854.8 / 854.3 |
| C4 the two INDEPENDENT lamps agree | **1.164 and 1.204**, 3.4 % apart |

```
M1 FAIL  elevation 1.184 lamp radii
         against ref_nolita_front34 2.121, ...34b 2.100, ref_playa_34 1.951,
         ref_workshop 2.127
         to reach 2.127 the break must rise 33.2 px = 74 mm
```

**F75 STANDS, now on a pose-free instrument, and the magnitude is 74 mm** —
inside §3.11's honest 50–80 mm range, at the top of it. The ruler is the **dark
lens interior**, not the chrome rim and not the bore; §3.11 records that the rim
stands 16.5 mm outside its own bore and that **no frame we hold shows a rim and
its aperture together**, so that conversion still cannot be checked. Stated in
the probe's own header.

**AND IT WAS LOOKED AT.** Side by side with `ref_nolita_front34.jpg`, three
register rows are visible by eye in the elevation at once: the glyph builds as an
**X** where the photograph shows a clean V over W (F63/F69); the lamps read as
**dark holes** (F80); the break passes far closer above the lamp than the
photograph's (F75).

### §4.2 `probe_rev45_nose.py` was run — it had never been invoked (F86)

**8 checked, 0 FAILED.** Including **C4: lens/cream 0.549–0.553 against a
photographed 0.565.** That directly contradicts F80's *"the headlamp renders as a
dark hole"*, which reads the same lamp against **body red** and finds a large
gap. **Both instruments were run this revision and both stand.**

So all three patches were measured **in one frame each**, with every window
**painted and looked at first**:

| ratio | render `p45_front34` | photograph `ref_playa_34` | render ÷ photo |
|---|---|---|---|
| lens / cream | 0.636 | 0.688 | **0.92** |
| lens / red | 1.292 | 1.973 | **0.65** |
| **red / cream** | **0.493** | **0.349** | **1.41** |

**The lens is nearly right against cream; the render's red is 1.41× brighter
relative to its cream than the photograph's.** That is where most of F80's gap
lives — **not in the lamp.**

**AND RULE 8 FIRED ON ITS OWN AUTHOR, TWICE.** The first cream window landed on
the **roundel's strokes** (sd 57.69) and the second **straddled the V-arm**
(sd 45.78) — the same two mask defects §"rule 8" lists by name from an earlier
revision. Both were caught by painting the window and looking, neither by
reasoning. The third window reads sd 8.61 on plain cream.

**ITS CEILING, STATED.** The two frames are a **sunlit exterior** and a
**cyclorama**. The ratios are exposure-free only under linear response and
uniform illumination across the three patches, which does not hold between them.
**F86 is graded a LEAD, not a finding, and no cause is attributed (rule 29.3).**
What it does say is that the next revision **must not assume F80 is the lamp**.

Worth noting alongside it: `ref_playa_34` is bright daylight with a **sky for the
lens to reflect**. F62 measured this model's specular image as featureless
cyclorama 19.3 m out. **F80 and the studio ruling are coupled**, which bears on
the owner decision carried in the rev-60 brief.

---

## §5. WHAT WAS NOT DONE, SAID PLAINLY

* **F75 is measured, NOT fixed.** §3.11's own analysis says no single constant
  fixes it — `V_POW` needs 0.345 at the lamp but 0.214 at the indicator, `V_APEX`
  is refuted outright, `HL_DROP` creates a 2σ conflict — so it is a re-solve
  against two constraints, the same shape as F65. This revision built the
  instrument it needed and stopped there.
* **`V_POW` (F77) and `IND_DZ` (F78) are untouched.** Both are pinned by value in
  `verify_clone.sh` (`V_POW` in **three** rows) and both need re-basing together
  with the cause named.
* **Items C, D and E are untouched** — the emblem (F63), the ground shadow (F67),
  the interiors (F45).
* **The front arch is not rebuilt** — deliberately, see §3.5.
* **The delivery render was not run**, per the owner's standing instruction.
