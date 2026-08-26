# NEXT CONTEXT PROMPT — rev 60

## §0.0 DO THIS FIRST — THE WHOLE DECISION, IN TWENTY LINES

**Before you read another word, put the machine to work. It is CPU-bound and idle right now.**

```bash
cd /home/user/combi_render
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
nohup env T1_SUB=1 T1_PREVIEW=front,side,hero T1_PFX=r60 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py > /tmp/r60.log 2>&1 &
```

`out/` is untracked and **starts EMPTY** — it did at rev 59, whatever the previous handoff said.
**`bootstrap.sh` first**: at rev 58 AND rev 59 `/tmp/blender/blender` did not exist and `bpy` was not
importable, and the script rebuilt both from nothing. Then start the render, then read.
`T1_PREVIEW` takes a LIST and pays the ~20 s scene build once. **`grep -c Saved: /tmp/r60.log` must
be 3** — a backgrounded runner's exit code is the redirect's and tells you nothing.
`front` feeds `probe_rev59_nose.py`, `side` feeds `flank_compare.py` **and `probe_rev59_door.py`**,
`hero` feeds `gloss_compare.py` and is the frame the owner actually judges.

**THE OWNER'S REV-58b RANKING STILL GOVERNS. TWO OF HIS FIVE ARE NOW CLOSED.**

> *[owner, rev 58b]* **"There is a weird arc above the back wheel just kind of floating there. The nose
> is still not the right shape. The rear hatch open is not true to size/scale/material. The door cuts
> a little bit closer to the wheel well at the front. Señor in Señor Tacombi still is not clear and
> well defined."**

| # | do | state | gate |
|---|---|---|---|
| **A** | **THE DOOR** — *"the door cuts a little bit closer to the wheel well at the front"* | **FIXED AT REV 59 AND VERIFIED.** Built 0.7098 / 0.9600 against the photograph's 0.7096 / 0.9598 — 0.1 mm. **Verify before building on it** | `probe_rev59_door.py` M2, **PASSING** |
| **B** | **THE NOSE — the two-tone break must rise ~74 mm.** The instrument is BUILT and pose-free; the FIX is not done | **MEASURED, NOT FIXED.** §3.1. It is a **re-solve against TWO constraints**, the shape of F65 — no single constant does it, and each was inverted on its own at rev 58 | `probe_rev59_nose.py` M1, **watched failing** |
| **C** | **F63/F69 — THE VW GLYPH BUILDS AS AN X**, on the nose AND on four hubcaps. **Visible by eye in the rev-59 elevation** | **GATED AND FAILING.** `probe_rev46_vw.py` C6: photograph **7** cream cells, built **6** | **C6, watched failing** |
| **D** | **F67 — NO GROUND SHADOW AND NO UNDERBODY.** The largest illusion defect on the register | **OPEN, never attempted** | none |
| **E** | **F45 — the galley and roof-aperture interiors are untextured white blocks** | **OPEN** | none |

**FIXED AT REV 59 — verify these still hold before building on them:**

* **the door** — `DOOR_LOBE_A/B` were built off the WHEEL HUB column against a datum that is the
  **ARCH centre** (9.83 px apart — rule 34), and off `39.54 px`, a scale obtained by **assuming the
  radius it then measures**. Both re-measured in the flank plane, so the ratio carries **no px/m and
  no parallax term**. The step moved **aft 67 mm**; the ramp's WIDTH was already right to **1.07 %**.
  `VERIFY: 0 fail, 0 warn` and both shut lines **100 % open at `T1_SUB=1` AND `T1_SUB=2`**.
  Ablation `T1_DOOR_STALE=1`, watched failing.
* **the clearance assert** — it **forbade the vehicle**. Both thresholds were regression baselines at
  rev 41's accidental **0.0653 of `ARCH_R`**; the photographed vehicle clears its own arch by
  **0.0226 R = 8.4 mm**, a third of that. Re-based against the photograph, with the cause named; the
  companion test is `verify.py`'s **direct** rows (no boolean rolled back; non-manifold edges), not a
  second proxy.

**AND TWO CLAIMS IN THE INCOMING BRIEF WERE REFUTED BY MEASUREMENT. DO NOT REBUILD THEM:**

* **"the step must move aft ~95 mm"** — it is **67 mm**. §3.10's `A = 41.50 px` measures **38.66 px**
  vertically and **37.28 px** as a fitted radius; the render control recovers those to **+1.7 %** and
  **−0.07 %**.
* **"the front arch is up to 0.13 A ≈ 48 mm inboard of a circle"** — **a METHOD ARTEFACT (F82).**
  Its r/A-about-a-guessed-centre sweep, run unchanged on the render's KNOWN circle, invents swings of
  **±0.07 R** and misstates R by **+17 %**. The real departure, by circle fit, is **1.171 % of R =
  4.4 mm rms** — five times the instrument floor, so REAL, but an order of magnitude smaller and
  **below SPEC §2's ±8 mm lock**. The arch is therefore **NOT rebuilt**, and the forward half below
  the door line **cannot be recovered from what we hold**.

**STILL WRONG AND STILL OPEN:** the mural board is **12–14 % SHORT**; its **top border is 2.5× the
photograph**; the **props cross 97 % of the painted face** (**OWNER DECISION**); the **S renders as
three fragments** (**OWNER DECISION**, A12); **91 px of `Senor` reference ink is undrawn**; the flank
gate's worst region is **`i` at 0.685**.

**THE OWNER RULED ON ALL THREE OPEN DECISIONS AT REV 59. DO NOT RE-ASK ANY OF THEM.**

1. **THE BRANCH COLLISION — RULED: *"Merge it, renumber its IDs."*** Done, at rev 59.
   `origin/claude/bus-model-rev57-yvrlhi` is merged; its ten findings are renumbered **F88–F97**,
   with **main's F58–F67 untouched** and **every renumbered row carrying its old ID on the row** so
   `LEDGER_rev57.md` and `NEXT_CONTEXT_PROMPT_rev58.md` — which still use the old numbering — can be
   translated. `probe_rev58_ceiling.py` is **on this tree now**, and `probe_rev58_gloss.py` carries
   **BOTH** arms, rev 58's dark-card and rev 57b's **MIRROR** arm (`T1_GL_MIRROR`).
   **`bootstrap.sh` row 9 is GREEN for the first time in three revisions — ALL 10 PASS.**
2. **THE STUDIO — RULED: *"Keep studio, fix the model"* STANDS**, put to him again at rev 59 with
   F62 and F86 both on the table and the headlamp crop attached. **STOP RE-PUTTING IT.** The
   consequence he accepted: **F80's headlamp gap is partly a consequence of the surround and is
   ceiled there** — the photograph has a sky for the lens to reflect and the cyclorama does not.
   What remains live is **F86**, the red/cream LEVEL, which is a paint question and not a rig one.
3. **THE FRONT ARCH — RULED: *"Leave it circular."*** The departure is **4.4 mm rms**, below SPEC
   §2's ±8 mm lock, and the forward half below the door line **cannot be recovered from what we
   hold**. **Do not build it, and do not mirror the half that can be seen.**
   `probe_rev59_door` **M3 stays failing as the honest open record** — if it ever reads PASS without
   the arch being rebuilt, the instrument was relaxed rather than the model fixed.

**RANK BY PIXELS OF THE DELIVERY FRAME**, `python3 visibility_budget.py`; gate availability is a
tie-breaker — **but the owner outranks it.** `CLAUDE.md`: *"The machine outranks the prose. The owner
outranks the record."*

---

**Now read this whole file before you CHANGE anything.** Then `CLAUDE.md`, then `LEDGER_rev59.md`
(where every number in §2 comes from), then `OPEN_FINDINGS.md`, then `AUDIT_rev57_efficiency.md`.

---

## §0.05 THIS BRIEF WAS AUDITED AGAINST THE MACHINE — AND WHAT THE AUDIT FOUND

**Rule 17: audit the brief you WRITE, not only the one you receive.** Both halves ran as scripts.

* `python3 audit_brief.py` — see the run recorded at close of rev 59.
* `python3 audit_adversary.py` — **its questions were REPLACED for this revision.** Rev 59's set
  graded a tree whose door constants have since moved; a question that can no longer fail is not a
  control.

**AND THE REV-59 AUDIT'S BIGGEST FINDING WAS ABOUT THE INCOMING BRIEF, NOT THE OUTGOING ONE.** Two
of §3.10's three headline figures did not survive re-measurement (95 mm → 67 mm; 48 mm → 4.4 mm), and
the second failed because **the method it used invents that signal on a shape known to be circular**.
Both are corrected in the source, the register (F81, F82, F83) and here. **The lesson is rule 36's:
run your instrument on a case whose answer you already know, BEFORE you publish what it says about a
case you don't.**

**AND MY OWN INSTRUMENTS WERE WRONG FOUR TIMES IN THIS REVISION, WHICH IS NORMAL HERE (rule 4).**
A hubcap mask that swallowed the **white studio floor** (132 mm centre error); a lip tracer that
locked onto **folk-art motifs** (factor-2.0 error in the ruler); a cream window on the **roundel's
strokes**; a second cream window **straddling the V-arm**. **Every one was caught by painting the
window and looking at it. None by reasoning about it.**

---
## §0. THE GOAL, AND HOW FAR OFF IT WE ACTUALLY ARE

**CARRIED FORWARD FROM THE REV-55, 56, 57 AND 58 BRIEFS. It is not mine and it is not to be
dropped — rule 16.**

**PHOTO-REALISTIC PARITY WITH THAT EXACT BUS.** Not "a convincing VW bus" — *that one*, the red
Señor Tacombi combi in the frames on this repo. **Any single measurement off is unacceptable,
per-measurement and not on average.** A model right in ninety places and wrong in one is not 99 %
done, because he will look straight at the one. **At rev 58 he did exactly that, at the emblem,
for the fifth time, while every automated check was green.**

**AND HERE IS THE HONEST DISTANCE.** `verify_clone.sh` ends **ALL 261 PASS** and its own verdict
block says what that is worth: **0 FIDELITY, 261 SELF-CONSISTENCY. Not one of those rows compares
the vehicle to a photograph.**

| gate | state at rev 58 |
|---|---|
| `flank_compare.py` | **runs, FAILS 1 of 4.** `Senor` **0.651** against a 0.75 bar. The deficit is the **artwork alpha and its placement**, not the render (F39) |
| `mottle_measure.py` | **runs, and it is NOT measuring the mottle** — 1.1–2.0 % of it. Rev 56's reading and rev 57's item B are REFUTED |
| `gloss_compare.py` | **runs, FAILS at 0.426** (bar 0.60). Mask corrected at rev 58 (F59); the model-side lever is now **exhausted** (F60/F62) |
| **`probe_rev46_vw.py`** | **NOW FAILS C6, and that is the point.** photograph 7 cream cells, built 6. It reported 0 FAILED for three revisions while the glyph was an X |
| `cream_rms.py` | `run()` is the LIVE re-based path |
| the badge STROKE WEIGHT | **CEILED-rev57.** Different finding from F63 |
| `visibility_budget.py` | the RANKING, not a gate |
| everything else | self-consistency |

**The frame reads as clay and the cause is the environment, not the shaders** — the surround is a
featureless white cyclorama, so the paint has nothing to reflect. **He was shown that, told the
cost, offered four routes, and ruled "keep studio, fix the model".** **Rev 58 MEASURED that
ceiling** (F62): this flank's specular image is white cyclorama **19.3 m** away. **Do not
re-litigate it.**

### §0.1 THE REFERENCE SET IS COMPLETE, AND IT IS GUARDED FRAME BY FRAME

> *[owner, rev 54]* **"we have all references that we need on repo and I want to make sure that is
> never forgotten."**

**ONE: WHAT WE HOLD IS WHAT WE GET. STOP PARKING WORK BEHIND A PHOTOGRAPH.** `PHOTOS_WANTED_*` is a
wish list, not a gate — carry it (rule 16, and items 1–5 are still not to be re-asked) but **do not
let it license parking an item.** Where a frame genuinely cannot answer, the result is *"it cannot
be recovered from what we hold"* — a real result, stated with its ceiling. **Rev 58 produced two:**
the residual gloss gap (F62) and the photograph's inability to resolve the V/W centre gap at 68 px.

**TWO: THEY CANNOT BE RE-SHOT, SO THEY ARE CHECKSUMMED INDIVIDUALLY.** **18 rows name them one at a
time**, so a loss says *which*:

* **the RED target bus** — `ref_side.jpg`, `ref_rear34.jpg`, `ref_playa_34.png`,
  `ref_nolita_front34.jpg`, `ref_nolita_front34b.jpg`, `ref_nolita_flank.jpg`,
  `ref_nolita_doorshut.jpg`
* **NOT the target, geometry only** — `ref_workshop.jpg` is the **GREEN** vehicle; **`IMG_2073.jpeg` is ALSO
  the GREEN vehicle and was MISFILED under the red bus in this very register until rev 58 measured it**
  (body **G−R +21.7** on the lower flank and **+28.5** on the rear quarter, against `ref_side.jpg`'s **−67.6**);
  `bus_model_ref.JPG`
  is a **SCHOOL BUS**, a fidelity bar only. **Paint and artwork do not transfer between vehicles;
  geometry does (rule 11).**
* **retired** — `ref_source.jpeg`, a 246×197 thumbnail the record itself retired
* **derived/annotated** — `ref_grid.png`, `ref_side_grid.png`, `ref_nose_grid.png`,
  `ref_band_grid.png`, `ref_x6_lanczos.png`
* a **floor of 54** reference-class tracked images, and **the five byte-identical pairs are asserted
  to stay five** — a sixth group means a frame arrived that duplicates one we already hold, which is
  **not corroboration** and has fooled this project before (rule 11).

---

---

## §1. START HERE — MEASURE THE BRANCH, DO NOT TRANSCRIBE IT

```bash
cd /home/user/combi_render
git fetch --unshallow 2>/dev/null || true
git fetch --all --prune
for b in $(git branch -r | grep -v HEAD); do
  printf "%-52s ahead %-3s behind %s\n" "$b" \
    "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"
done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
./bootstrap.sh          # ALL 10 PASS at rev 59 close -- row 9 went GREEN when the
#     stranded rev-57b branch was merged on the owner's ruling.  MEASURE IT
#     ANYWAY: row 9 is "no branch carries work HEAD does not have", and it had
#     been red for THREE revisions.  A new red here means a new stranded branch.
./verify_clone.sh       # ALL 261 PASS in ~70 s -- and read what its verdict block says
```

**AT PICKUP, REV 59 MEASURED — AND THE HANDOFF IT WAS GIVEN WAS WRONG.** The handoff stated
*"HEAD = `claude/combi-render-rev-58-lg0746`, 13 ahead / 0 behind — rev 58 and 58b are UNMERGED"*.
**They were already merged, through PR #18** (`fbcec2e`). HEAD measured **0 ahead / 0 behind**,
`git diff --name-only HEAD...origin/main` **empty**. That is the **FIFTH revision running** in which
the prose guessed the merge state and the machine corrected it.

**AND THE NINTH DELETION HAPPENED, ON SCHEDULE.** `fetch --prune` printed
`- [deleted] (none) -> origin/claude/new-session-ocymb5` — **the branch rev 59 was told to develop
on**, deleted before rev 59 had pushed anything, the **FOURTH RUNNING** to hit the current
revision's own branch. It was recreated by the first push. **Expect it at rev 60.**

**AND `out/` WAS EMPTY**, which the handoff also denied. **Render before quoting any probe.**

**RE-MEASURE BEFORE YOU FINISH, TOO.** `origin/main` moved mid-revision at rev 51 and rev 55, and
both times row 9 was the only thing that caught it. It did not move at rev 56–59.

---

## §2. WHAT REV 59 DID

**Every figure below is in `LEDGER_rev59.md` with its provenance. Nothing here is transcribed.**

### §2.1 ITEM A — THE DOOR, MEASURED, FIXED, AND LOOKED AT (F81)

`probe_rev59_door.py` runs the **identical pixel code** on the side render, whose front arch is a
circle of `ARCH_R` about `X_AXLE_F` **by construction**, so the truth is computable from the source:

| control | result |
|---|---|
| C1 hub finder recovers the model's own front axle | **+4.7 mm, +6.0 mm** |
| C2 circle fit recovers the render's own `ARCH_R` | **−0.07 %**; centre to **0.16 px** |
| C3 the render's arch fits a circle | **rms 0.237 % of R** — the instrument floor |
| C4 lobe feet recover the built constants | aft **+2.5 mm**, fwd **−8.1 mm** |
| C5 the whole chain end to end | A **−0.65 %**, B **+2.48 %** |

**C1 FAILED FIRST AND THE FAILURE WAS MINE** — the hubcap mask swallowed the white studio floor and
put the fitted centre **132 mm** low. Caught by painting the mask (rule 8).

**THE ANSWER.** Photograph `DOOR_LOBE_A` **0.7096**, `DOOR_LOBE_B` **0.9598** against a built 0.8877
/ 1.1406 — **aft by 66.5 and 67.5 mm**. Both feet move by the same amount to **1 mm**, and the
ramp's **WIDTH** was already right: **0.2502 of R against 0.2529, −1.07 %.** The step was the right
SIZE in the wrong PLACE. After the fix, M2 reads **+0.1 / +0.1 mm**.

### §2.2 THE ASSERT THAT FORBADE THE VEHICLE (F84)

Moving the lobes trips `_MIN_RAD >= DOOR_ARCH_G`, exactly as §3.10 predicted. **So the vehicle's own
clearance was traced**: minimum **0.844 px = 0.0226 of `ARCH_R` = 8.4 mm**, against rev 41's inherited
bar of **0.0653 R = 24.4 mm** — nearly **three times** it, and a 10 mm floor the vehicle also fails.
The bar was an accident of rev 41's outline. Its inherited rationale is refuted **in this repo** by
`SPEC.md` §10.62 (line 2491, quoted verbatim in the ledger). Re-based against the photograph.

### §2.3 §3.10's SECOND CLAIM IS A METHOD ARTEFACT (F82), AND WHAT THE ARCH REALLY DOES (F83)

Run §3.10's r/A sweep on the render's **known circle** and it returns `fwd 1.0155 → 1.2043`,
`aft 0.9204 → 0.7537` — **±0.07 R of invented signal**, and a first pass put the ruler out by a
**factor of 2.0** because thin folk-art motifs satisfied the red→black test. The weak link is the
**crown column**: near the crown the arc is flat, so row noise maps to **+5.5 to +26 px** of column
error where the truth is 0.

The real departure, by circle fit at matched angular span: **1.171 % of R rms against a 0.237 %
floor — 5.0×, so REAL; 4.4 mm rms on `ARCH_R`, below SPEC §2's ±8 mm lock.** **The arch is NOT
rebuilt.** My own forward trace dies at 30° and RISES over the span it reaches, so §3.10's *"both
flanks fall symmetrically"* is **not reproducible either**. `probe_rev59_door` **M3 fails BY DESIGN**
and must keep failing until the arch is rebuilt or the owner rules.

### §2.4 ITEM B — THE INSTRUMENT IS BUILT, POSE-FREE (F87)

`probe_rev59_nose.py` on `T1_PREVIEW=front`, the orthographic elevation `studio.py` has carried all
along and nothing had pointed at the nose. **4 controls PASS** — two lamps, symmetric about the
frame's own centre column to **0.23 px**, same size and height, and the two **independent** lamps
agree to **3.4 %**. **M1 FAILS: 1.184 lamp radii against the photographs' 1.951–2.127.
To reach 2.127 the break must rise 33.2 px = 74 mm** — inside §3.11's honest 50–80 mm range, at the
top of it. **F75 stands, now pose-free.**

### §2.5 F80 IS RE-FRAMED — IT MAY NOT BE THE LAMP (F86)

`probe_rev45_nose.py` was **run for the first time**: **8 checked, 0 FAILED**, including **C4
lens/cream 0.553 against a photographed 0.565**. That contradicts F80, which reads the same lamp
against **body red**. Measured in one frame each, every window **painted and looked at**:

| ratio | render | `ref_playa_34` | render ÷ photo |
|---|---|---|---|
| lens / cream | 0.636 | 0.688 | 0.92 |
| lens / red | 1.292 | 1.973 | 0.65 |
| **red / cream** | **0.493** | **0.349** | **1.41** |

**The lens is nearly right against cream; the render's red is 1.41× brighter relative to its cream.**
**CEILING STATED: a sunlit exterior against a cyclorama — exposure-free only under linear response
and uniform illumination, which does not hold between them. F86 is a LEAD, no cause attributed
(rule 29.3).** **Do not assume F80 is the lamp.**

### §2.6 REFUTED AT REV 59 / STILL REFUTED — DO NOT REBUILD THESE

* **"the door step must move aft ~95 mm"** — **REFUTED, it is 67 mm** (F81).
* **"the front arch is up to 48 mm inboard of a circle"** — **REFUTED as a method artefact** (F82).
  It IS non-circular, by **4.4 mm rms** (F83).
* **"both flanks of the front arch fall symmetrically"** — **not reproducible**; the forward half
  below the door line is **not recoverable from what we hold**.
* **"`_RAIL_SPAN` weakens silently when `_LOBE_XA` moves aft"** — **measured both ways: n=4 and
  16.000 mm BEFORE and AFTER.** It did not. A dense guard was added anyway, because four points
  cannot see a sag between them.
* **"the glyph is a legible V over W at full size"** — **REFUTED, F63**, and now visible by eye in
  the rev-59 orthographic elevation.
* **"`probe_rev46_vw.py` clears the emblem"**; **"the clearcoat is item A's lever"**; **"`T1_GL_SPOT`
  measures the rig ceiling"**; **"the render's headroom is 0.132 of the photograph's"** (it is
  0.090); **"the mottle is the lever"**; **"the `Senor` deficit might be the render"** — all still
  refuted, see the rev-59 brief §2.5.
* **§2b of the rev-52 brief — HIS SETTLED RULINGS — IS UNCHANGED AND STILL BINDING.** W6; the roof
  strips' 0.3 m retired; the wipers withdrawn entire; the lower bay SHUT; the RED bus is the target
  and **paint and artwork do not transfer between vehicles**; the tail board IS on the vehicle; the
  marks above the burst are STARS. **Do not re-open or re-ask any of them.** `playa_env.py` is not on
  the table. **And rev 54's ruling stands: "Keep studio, fix the model"** — see §0.0 for why it is
  worth re-putting, but do not act as though it has changed.

---

## §3. THE WORK LIST FOR REV 60

> **The two-letter-scheme collision that the rev-59 brief warned about is GONE.** There is one
> scheme and it is §0.0's: **A = the door (DONE), B = the nose, C = the emblem, D = the ground
> shadow, E = the interiors.** The sections below use it.

### §3.1 ITEM B — THE NOSE. THE INSTRUMENT EXISTS; THE RE-SOLVE DOES NOT.

```bash
python3 probe_rev59_nose.py out/r60_front.png     # M1 FAILS today: 1.184 vs 1.951-2.127
T1_SUB=1 /tmp/blender/blender -b -P probe_rev45_nose.py    # 8 checked, 0 FAILED -- and see F86
```

**IT IS A RE-SOLVE AGAINST TWO CONSTRAINTS, NOT A CONSTANT.** Rev 58 inverted each on its own and
every one failed: `V_POW` needs **0.345** at the lamp but **0.214** at the indicator; `V_APEX` needs
0.745 vs 0.949, both above the bumper crown 0.5360, **which would expose the wedge apex — refuted**;
`HL_DROP` fits both by construction but takes lamp-to-belt from the photographed **0.339 ± 0.025 m**
to 0.391, a **2σ** conflict with the arm that justified it; `V_HALF_W` gives 0.708 vs 0.736 and is
the most nearly self-consistent. **This is the shape of F65.**

**WHAT REV 59 ADDS.** The elevation is orthographic, so you can now iterate against a **pose-free**
number instead of a three-quarter crop. `probe_rev59_nose.py` prints the required rise in **mm** as
well as in lamp radii. **Its ruler is the DARK LENS INTERIOR** — not the chrome rim, not the bore;
the model's rim stands **16.5 mm outside its own bore** and **no frame we hold shows a rim and its
aperture together**, so that conversion still cannot be checked. Stated in the probe's own header.

**AND TWO CONSTANTS ARE PINNED BY VALUE.** `V_POW` (F77) is in **THREE** `verify_clone.sh` rows
(`V_POW is 0.60`, `V_POW_Z is 0.60`, `V_POW and V_POW_Z agree`) — **re-base all three TOGETHER with
the cause named; never relax one copy.** `IND_DZ` (F78) is contradicted at **4.6σ by its own cited
photograph** (`ref_workshop` ≈ 0.160 m, red-bus frames 0.183, built 0.206 ± 0.010).

**AND READ F86 FIRST.** If the red/cream level is out by 1.41×, some of what looks like nose shape
may be nose TONE. Separate them before tuning either.

### §3.2 ITEM C — THE EMBLEM (F63/F69). UNCHANGED, AND NOW VISIBLE BY EYE.

```bash
T1_SUB=1 /tmp/blender/blender -b -P probe_rev46_vw.py     # C6 FAILS: photo 7, built 6
```

**DO NOT re-try F65's three** — drive the MIN corner (6 → 4); make `vw_logo_fit` a pure unit
conversion (6 → 4); `VW_W_ARM_Z` 0.0019 → 0.30/0.55/0.772 (6, 6, 6). The V's arms and the W's outer
arms **cross the same region BY CONSTRUCTION**. The job is a **re-solve of the W's spine against
reach**: every terminal must meet the ring **radially** — its direction of travel equal to its angle
from centre, a fixed point, not a constant — while L1–L6 still land. `probe_rev46_vw.py` has the
solver (`T1_VW_SOLVE=1`) and the reach measure; **the missing piece is putting `cream_cells` into
`err()` and re-running it.** If no setting of the six parameters reaches 7 cells, **say so with the
number** — *"the current spine family cannot reach the photograph's topology"* is a real result.

### §3.3 ITEM D — THE GROUND SHADOW AND UNDERBODY (F67). NEVER ATTEMPTED.

The largest illusion defect on the register, and it is plain in every frame this revision rendered:
the vehicle floats on white. **Nothing gates it.**

### §3.4 ITEM E — THE UNTEXTURED INTERIORS (F45)

**7.4 × 10⁵ px², ungated, never measured, plainly visible through four openings, dead centre.**
Build one, or accept it and say so with its ceiling.

### §3.5 THE FRONT ARCH — IF IT IS EVER REBUILT (F83)

**Read F82 before you touch this.** The departure is **4.4 mm rms**, five times the instrument floor
but **below SPEC §2's ±8 mm lock**, and the forward half below the door line is **deep shade with the
white bumper cutting in — not recoverable**. Building it symmetric is **inventing the half we cannot
see**. The machinery exists for the rear (`rear_arch_outline`, `_arch_drop`, `ARCH_W_REAR`). **This
is an OWNER DECISION or a NEW-FRAME item, not a do-now.**

### §3.6 THE CHEAP ROWS THAT ARE STILL OPEN

* **F85 — `gloss_compare.py` REWRITES A TRACKED FILE** (`probe_scratch/rev57_gloss_render.png`).
  Running the gate dirties the tree and `verify_clone.sh`'s *"modified tracked files"* row then
  fires. It cost rev 59 one wasted hunt. **One-line fix; nobody has done it.**
* **F05 is still cheap** — F51 is fixed, `studio.rig()` exists, and the beauty arm is the only arm
  that can see the **roughness** half of the mottle (F41).
* **F42 — the 8-bit reader.** Decoder written and controlled; lifts every consumer of `_render`.
* **SPEC §8's colour locks are all graded M** off `ref_source.jpeg`, a **246×197 thumbnail the
  record itself retired**. Re-derivable on `ref_playa_34.png` at **4× the area** with no new
  photograph. **Report the values; do not change the constants without his ruling** — W6 makes
  colour his call. **F86 gives this new urgency.**

### §3.7 FINISH A9, AND THE THREE HOLES REV 52 LEFT OPEN

**A9: two of four parts done; the galley is still ~103 mm too far aft. PROVENANCE, GRADED: the
per-feature deltas are INHERITED from the rev-52 brief and have NOT been re-measured at rev 52–59.**
The offset is **NOT rigid** (−0.09574 at hook u=0.13 to −0.11035 at `gal_appliance` u=0.80), so one
additive constant leaves ±7.3 mm. Re-derive each X from `BAYS`.

**THE THREE HOLES.** F11–F13 reproduce exactly. **F14's 260.0 mm and 20.0 mm sight lines are rev
52's and have NOT been re-measured since — SEVEN revisions, well past §8's decay rule.**
* `gal_end_f` needs its own sight line established first — **do not inherit `REAR_W/2`** (rule 34).
* The **sixth hook at X −0.907 lies 51.25 mm beyond `BAYS[2]`'s aft edge**; the hook span centre is
  **−0.7050** against the rail's **−0.5980** — **107.0 mm**. They disagree and one is wrong.
* A7's real defect: `roof_cutters()`'s aft edge is `LID_X1`, **not greppable as `LID_X1 = -1.0700`**
  — the source line is `LID_X0, LID_X1 = 0.9640, -1.0700` in `t1_shell.py`. **803 mm** of roofed
  body sits unlit between the last light inlet and the tail. A7 is **ILLUMINATION, not dressing.**

### §3.8 A13 / A16 / A12, A11's SECTION, A14, AND THE mm AXIS

**A13 / A16 / A12** — the isolated star built BELOW the burst where both red frames put it above;
every flank rosette drawn at the diameter of its **gold core**; *A12 is an OWNER RULING* —
`senor_trace.py` calls the remedy *"inventing ink the photograph does not show"*.

**A11's SECTION, A14** — a chrome lever lying in a dish **pressed into** the skin against a 12 mm
**proud** prism.

**THE mm AXIS — STILL NOT ATTEMPTED, FOUR REVISIONS RUNNING.** `PXM_REF = 337.0` px/m is a
**bracket** (330–344), not a measurement. *(Rev 55's correction stands: `depth_correct()` is defined
NOWHERE in this repo.)* Render-against-render ablations do **not** depend on it. **Note that rev 59's
door figures do not either** — they are ratios of two flank-plane lengths in one frame.

### §3.9 THE PROCESS ROWS, STILL OPEN

`OPEN_FINDINGS.md` is the register — see §8; the standing-instructions carrier deleted at rev 44,
which took the **die-cut sticker — the project's original deliverable** — with it, **still open and
carried as F18**; SPEC §0.2's two rev-4 corrections later refuted; rev 48's refuted *"B stays open"*
still live in `build.py` and, **split across two lines so a flat grep misses it**, in `t1_shell.py`;
the tail board still has **zero rows in either verifier**.

### §3.10 THE HABITS THAT PAID AT REV 59

**RUN YOUR INSTRUMENT ON A CASE WHOSE ANSWER YOU ALREADY KNOW, BEFORE YOU PUBLISH WHAT IT SAYS ABOUT
A CASE YOU DON'T.** That single step killed a 48 mm finding, corrected a 95 mm one to 67 mm, and
caught four of my own instruments being wrong.

**PAINT THE WINDOW AND LOOK AT IT.** Four wrong instruments this revision: a hubcap mask that
swallowed the white floor; a lip tracer that locked onto folk art; a cream window on the roundel's
strokes; a second one straddling the V-arm. **All four caught by looking. None by reasoning.**

**A PROBE THAT RE-TYPES THE THING IT IS CHECKING IS CHECKING ITS OWN TYPING.**
`probe_rev59_door.py` pasted the constants it was testing, the source moved in the same revision, and
its controls reported the **fix** as a −20.56 % miss. It reads `t1_shell` live now.

**WHEN A GUARD REFUSES A MEASURED CHANGE, SUSPECT THE GUARD'S PROVENANCE.** The clearance assert had
never been armed at a measurement; it was armed at rev 41's accident, and it forbade the vehicle.
**Check whether the threshold was ever measured before you assume the geometry is wrong.**

**FINISH WHAT YOU DISPATCH, AND LOOK AT THE FRAME BEFORE AND AFTER.** The door fix was confirmed by
a before/after crop, not by the green check.

---
## §4. WHAT WAS ASKED OF HIM — A CARRIER, NOT A LIST OF BLOCKERS

> **READ §0.1 FIRST.** At rev 54 he ruled that **the reference set on the repo is complete**. This
> section is kept in full because `CLAUDE.md` rule 16 forbids dropping a carrier, and because it
> records what was asked and what was refused — which is why items 1–5 must never be re-asked.
> **But it is no longer a licence to park work.**

**`PHOTOS_WANTED_rev52.md` is the carrier for item 7 (ONE HUBCAP, SQUARE ON AND CLOSE)**. Items
**1–5** keep their full text in `PHOTOS_WANTED_rev49.md`: the tail board's footing; the decal darker;
the nose square on; a raking-light frame of the louvres (**ONE item — the pressing depth**); the off
side, any frame. **He has said 1–5 are not possible now. DO NOT RE-ASK THEM.** Item 6 (an obliquely
seen wheel) was **DISSOLVED at rev 51** — struck, not outstanding.

**CARRIED FROM REV 53, still no carrier outside these briefs:** a frame showing the cream **where it
IS chipped**. Rev 54 and rev 55 both lowered its urgency; the band is 0.27 px at every scale this
project ships, and the gate that would place those chips is not built.

**ANSWERED AT REV 56 AND NOT TO BE RE-ASKED:** `lid_rail`'s width — *"narrow lip, ~as wide as it is
tall"*.

**ASKED AND ANSWERED AT REV 58:** the roughness/chroma trade — **"ship 0.250"** (F60). That is the
only thing put to him, and it was put as multiple choice with the crop attached.

**ASKED AND ANSWERED AT REV 59 — THREE RULINGS, NONE TO BE RE-ASKED.** All three were put as
multiple choice with the crops attached, in one batch:
1. **the stranded rev-57b branch** — ***"Merge it, renumber its IDs."*** Done; F88–F97; row 9 green.
2. **the studio** — ***"Keep studio — ruling stands."*** Put to him WITH F62 and F86 and the
   headlamp crop. **F80's headlamp gap is ceiled to the surround; F86's red/cream level is not.**
3. **the front arch** — ***"Leave it circular."*** **Do not build it and do not mirror it.**

**AND HE VOLUNTEERED TWO INSTRUCTIONS AT REV 58, BOTH BINDING:** the emblem needs a fix (F63, item
A), and **the full delivery render waits until the model is right.**

**STILL WORTH HIS TIME AND NOT ASKED:** **F38** — the built nose ring band sits at the top of its
adopted range (0.10086 against three frame readings at 0.087–0.093), and moving it moves the glyph's
fit radius with it, **which now interacts with F63**; and **F39** — `Senor`'s ink deficit is in the
artwork, which A12 makes his call. **Decide whether to ask. Do not simply carry them.**

---

## §5. THE RULES — `CLAUDE.md` CARRIES THE METHOD, NOT THE NUMBERED CANON

The canon (rules 1–33) is printed in `NEXT_CONTEXT_PROMPT_rev50.md` §11. **Rules 34–36 live only in
the rev-51…58 briefs and `LEDGER_rev50.md` §0, so they are carried here too — that is `CLAUDE.md`'s
own rule 16 firing on this file:**

> **34. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Before relying on any
> *"the record requires X"*, check which object the sentence is about — and check the cited line
> exists. **Rev 56 applied it to a CAMERA**: `flank_compare.py`'s header attributes a recovered
> camera position to `ref_side.jpg` that `studio.py` attributes to the PLAYA frame — the same three
> numbers in two places about two photographs (**F26, still open**). **Check it before any future
> work leans on that camera — item B does.**

> **35. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Guards that identify a part's foot or
> free edge by `min(y)` are only right while the part leans one way. Ask the geometry.

> **36. A GATE ONLY COUNTS FOR WHAT IT CAN SEE — ABLATE THE THING YOU ARE ABOUT TO TUNE, FIRST.**
> Earned at rev 57 and it cost that revision's item B. **Rev 58 extends it: a gate can be blind to a
> whole AXIS, not just to one constant.** `probe_rev46_vw.py` fits vertical landmarks and reported
> 0 FAILED for three revisions while the glyph was an X, because reach is a radius and every
> landmark it owns is a row (**F64**). **When you build a gate, write down which axes it does NOT
> see.**

> **37. NEW AT REV 58 — AN ABSENT INPUT MUST NEVER READ AS A MEASUREMENT.** `gloss_compare`'s
> missing default frame came back as `MOVED: []`, i.e. *"the estimator moved"*, and pointed the
> reader at the statistic instead of the path (**F58**). A probe that cannot run must say **"NO
> RENDER"** in those words and exit non-zero. **And a check whose input lives in an untracked
> directory passes only in the tree that wrote it.**

> **Rule 29.3:** no finding is attributed to a cause until a control separates it. **Rule 15:** a
> retraction that lands in a ledger and not in the source is half a retraction — **rev 58 retracted
> F47 in `t1_mats.py` itself.**

---

## §6. THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build  T1_SUB=1 ~20 s     render 1600x1100 96 spp ~4.5-5.5 min PER VIEW
mottle_measure.py (albedo arm, 64 spp) ~4.8 min PER RUN -- budget ablations in fives
```

```bash
./bootstrap.sh                                               # THE TOOLCHAIN IS NOT ON THE CLONE
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=front,side,hero T1_PFX=r60 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py     # ALL THREE views, ONE build.  It takes a LIST.
T1_RIG=1 ... /tmp/blender/blender -b -P build.py             # rev 58: build the rig WITHOUT a preview
T1_NORIG=1 ...                                               # the ABLATION -- assert_lit must REFUSE
T1_SUB=2 /tmp/blender/blender -b -P audit.py                 # rewrites STATE.md -- COMMIT FIRST
python3 lid_gen.py                                           # regenerates tex/lidmural.png
python3 flank_compare.py out/r60_side.png /tmp/fc.png        # GATE 1.  FAILS 1 of 4 today.
python3 gloss_compare.py out/r60_hero.png                    # GATE 3.  FAILS at 0.426 today.
#   ^ NOTE F85: this REWRITES a TRACKED file (probe_scratch/rev57_gloss_render.png).
#     Restore it before you verify, or the "modified tracked files" row fires.
python3 probe_rev59_door.py out/r60_side.png                # ITEM A.  M2 PASSES, M3 fails BY DESIGN.
python3 probe_rev59_nose.py out/r60_front.png               # ITEM B.  M1 FAILS: 1.184 vs 1.951-2.127.
T1_SUB=1 /tmp/blender/blender -b -P probe_rev45_nose.py     # 8 checked, 0 FAILED -- and read F86.
python3 gloss_compare.py --selftest                          # exposure invariance, NO frame needed
python3 visibility_budget.py 3840                            # THE RANKING.  Run it before choosing.
T1_SUB=1 /tmp/blender/blender -b -P probe_rev46_vw.py        # ITEM A.  C6 FAILS: photo 7, built 6.
T1_SUB=1 T1_VW_SOLVE=1 /tmp/blender/blender -b -P probe_rev46_vw.py   # the solver
T1_SUB=1 T1_GL_WRGH=0.25 T1_GL_PFX=w25 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P probe_rev58_gloss.py            # ITEM A's roughness arm, changes NO source
python3 cream_rms.py                                         # the LIVE photograph-side cream
T1_SUB=1 T1_MM_ALBEDO=1 T1_MM_SAMP=16 /tmp/blender/blender -b -P mottle_measure.py  # GATE 2
#   ^ 16, NOT the default 64.  Rev 56 measured this statistic stable across 16/32/48.
python3 audit_brief.py                                       # rule 17's MECHANICAL half
python3 audit_adversary.py                                   # rule 15's adversary -- REPLACE its questions
```

**`out/` IS NOT TRACKED and starts empty. Render before quoting any probe that reads a frame.**
**A backgrounded runner's exit code is the WRAPPER'S, not Blender's — grep the log for `Saved:`.**
**`probe_rev54_aov.py` and `probe_rev55_truenorm.py` write EXR into `probe_scratch/` — delete them
before committing and keep the PNGs.**
**`mottle_measure.py`'s BEAUTY arm REFUSES (100 % clipped) — but F51 is FIXED now, so wiring it is
cheap (§3.4).**
**`mottle_measure.py` names its output by `MOTTLE_AMP`, so two runs that differ in `MOTTLE_M`
OVERWRITE EACH OTHER'S PNG.**
**EVERY MEASUREMENT THROUGH `shader_solve._render` IS 8-BIT (F42), whatever `color_depth` says.**

**THE DELIVERY FRAME — DO NOT RUN IT UNTIL THE MODEL IS RIGHT (owner, rev 58, and STILL BINDING:
items B, C, D and E are open).**

```bash
T1_SUB=2 /tmp/blender/blender -b -P hq_render.py      # ONE build, 10 bands, WITH MARGIN
python3 stitch.py out/hq_hero_raw.png 0.0000,0.1000=out/hq0_hero.png ...   # DECLARED spans
#   ^^ CHECK ITS EXIT CODE.  It exits 2 on a seam and it MEANS it (F49).
python3 post.py out/hq_hero_raw.png out/hq_hero.png   # optics LAST, never per strip
```

3840×2640, 256 spp, SUB=2, **106.8 min**. `probe_scratch/rev57b_delivery_hq_hero.png` (1600 px) is
the tracked baseline; the full frame is **not** tracked and that is deliberate. The guard is
narrowed **by DIMENSION, not by name** — tracked hero PNGs must be ≤ 1600 px wide.

**ABLATIONS — every one exists to WATCH A GUARD FAIL.**
**NEW AT REV 59:** **`T1_DOOR_STALE`** (restores rev 44b's door lobes; the re-based cab-door/front-arch
clearance guard must REFUSE — watched, at 0.0653 R against the photograph's 0.0226 R).
**CARRIED FROM REV 58:** **`T1_NORIG`** (suppresses the rig; `assert_lit` must refuse — watched),
**`T1_RIG`** (build the rig without asking for a preview), **`T1_GC_ABSSPREAD`** (drops the `/p50`;
the exposure selftest must FAIL — watched), **`T1_GC_LOOSEMASK`** (restores the gloss gate's old
ink-contaminated mask), **`T1_GL_WRGH`** (the WEATHER group's roughness — item A's live lever),
**`T1_BODY_RGH`** (the shipped body roughness), **`T1_GL_DARK`** (the dark-card rig-ceiling arm —
it lands IN FRAME, which is the measurement).
Carried: `T1_GL_SPOT` (**refuted as a ceiling measure, F61**), `T1_GL_COATW`/`T1_GL_COATR`
(**refuted as a route, F54**), `T1_MOT_AMP`/`T1_MOT_M`/`T1_MOT_RGH`/`T1_MOT_DET`, `T1_FC_KVQUAD`,
`T1_RAILFLAT`, `T1_CR_LEGACY`, `T1_FC_INKGAIN`, `T1_FC_ZSTRETCH`, `T1_TRUENORM` (**a
DEMONSTRATION, not a fix**), `T1_PTWEAR`, `T1_EDGERAD`, `T1_MM_ALBEDO`, `T1_SOLVE_NODENOISE`,
`T1_TARNCONTAM`, `T1_RAILSTALE`, `T1_ENDSHORT`, `T1_CAPSINK`, `T1_LIDDEG`, `T1_BAYSTALE`,
`T1_LAMPSINK`, `T1_LIDASPECT`, `T1_HANDLEHI`, `T1_BAREMAT`, `T1_TBFOOT`, `T1_BAYPROUD`,
`T1_NOBEVEL`, `T1_BEVEL_SAMPLES`, `T1_FC_OLDDATUM`.

---

## §7. THE STANDARD, IN HIS WORDS

We are recreating a photorealistic version of **that exact bus**, and **any single measurement off is
unacceptable** — per-measurement, not on average. A model right in ninety places and wrong in one is
not 99 % done, because he will look straight at the one. **He did, at rev 58, at the emblem.**

`bus_model_ref.JPG` is a **SCHOOL BUS** and is **NOT the vehicle** — a FIDELITY BAR only. Use
`ref_workshop.jpg` the same way, and remember it has **no headlamps and no hubcaps fitted** and is
the **GREEN** vehicle (§4).

**Ground in the reference, build, adversarially audit, iterate.** Never build before grounding. Never
call it done off self-review. Report the measurement **with its ceiling**, never a self-assigned
score. Do not say anything is ready — say what is fixed, what is still wrong, and what you measured.

**RENDER IT, CROP IT, AND LOOK AT IT, before and after every change.** Every defect this project has
shipped passed `VERIFY: 0 fail, 0 warn` and was found by looking at a crop. **At rev 58 it was found
by rasterising the badge at the photograph's own scale and putting the two side by side.**

**When you need something from him, ask as MULTIPLE CHOICE with the reference material attached — one
crop, one mark, one sentence — and ASK IT WITH THE QUESTION TOOL.**

---

## §8. THE OPEN-FINDINGS REGISTER — `OPEN_FINDINGS.md`

**A register existed once and was ABANDONED AT REV 45 WITH 21 ROWS**, and nobody noticed for eleven
revisions. Rev 56 reinstated it; it carries **65 rows** now.

**IT IS A CARRIER (rule 16). Rows leave it only by being CLOSED with the measurement that closed
them, or RETIRED with the ruling that retired them. Never by being dropped.**

**THE POINT OF THE FILE IS THE PROVENANCE GRADE, NOT THE LIST.** This project's recurring failure is
**re-quoting inherited numbers as though they had been measured**. An `INHERITED` row is a claim.

**GRADE DECAY IS ITSELF A FINDING.** An `INHERITED` row that survives three more revisions without
being re-measured should be re-measured or downgraded.

**REV 58 ADDED EIGHT AND MOVED TWO.** Added: **F58** (the clone-only verifier row), **F59** (the
gate's headroom was a third artwork), **F60** (roughness, the live lever), **F61** (the rig arm
measures fill), **F62** (what the flank reflects, 19.3 m out), **F63** (the glyph is an X), **F64**
(the solver's blind axis), **F65** (three fixes that failed). Moved: **F44** partly closed,
**F51** closed.

**AND ONE CLOSURE FROM AN EARLIER REVISION IS NOW WRONG: F40** (*"the roundel reads as an X"* —
closed twice, at rev 55 and rev 57). **It was closed on a crop; the project's own rasteriser draws
an X.** F63 supersedes it.

**WHAT IS STILL INHERITED AND OLDEST:** **F14** (`gal_end_f`'s 260.0 / 20.0 mm sight lines, **rev
52 — SIX revisions un-re-measured**), F15 (A7's 803 mm, rev 52), F20 (the colour locks, rev 52),
F10 (the galley offset, rev 52), F18 (the die-cut sticker, rev 44 — **the oldest thing in the file**).

---

## §9. THE HORIZON BEYOND REV 60

**Rev 60's own order is §0.0. This section is the longer arc.** It is a CARRIER: each revision should
re-rank it, not rewrite it, and **say what moved**.

**WHAT MOVED AT REV 59.** The **door** left the table entirely — it was the owner's own item and it is
**closed and verified** (F81/F84). **The nose** moved from *"a lead that needs an instrument"* to
**measured on a pose-free instrument, 74 mm, and awaiting a two-constraint re-solve** (F87/F75) — the
instrument the previous horizon said it needed now exists. **The front arch** entered and left in the
same revision: its 48 mm claim was **refuted as a method artefact** (F82) and its real 4.4 mm
departure is **CEILED and deliberately not built** (F83). **F80 was re-framed** — F86 says the gap is
mostly red/cream level, not the lamp, so it is no longer a lamp item. **F85** is new, cheap, and
one line. And **F63 did not move**: it is still next, still failing, still his fifth report.

**WHAT MOVED AT REV 58.** The **owner** re-ranked the table, which no previous revision's horizon
had allowed for: the emblem was *"parked, CEILED, 1.4 px²"* under F08 and is now **item A** under
F63 — because **they are different findings** and only one of them was ceiled. Item A's gloss moved
from *"next"* to **partly closed with a measured ceiling** (F60/F62). F05 became **cheap** because
F51 was fixed.

| horizon | the work | worth | why it is in this order |
|---|---|---|---|
| **next** | **F63 — the glyph builds as an X.** Gated, failing, and his fifth report | he looks straight at it | The owner ranked it, and the owner outranks the budget |
| **next** | **F75 — the nose two-tone break, +74 mm.** The instrument is BUILT and pose-free (F87) | — | No longer a lead. A two-constraint re-solve, the shape of F65 |
| **next** | **F67 — the ground shadow and underbody.** The owner's item D | the whole frame | Never attempted, nothing gates it, and the vehicle floats on white in every frame |
| **next** | **F45 — the untextured galley and roof-aperture interiors** | 7.4 × 10⁵ px² | Bright, central, seen through four openings, pure placeholder |
| **next** | **F15 — A7.** Illumination, not dressing | 8.2 × 10⁵ px² | A large unlit region changes how the whole rear reads |
| **near** | **F01/F39 — `Senor`**, the artwork alpha and its placement | 2.7 × 10⁴ px² | Small but HARD-EDGED, so it reads louder per pixel than the table implies |
| **near** | **F43/F05/F41 — the cream's albedo texture and the beauty arm** | large area, subtle | **F05 is cheap now that F51 is fixed** |
| **near** | **F42 — the 8-bit reader.** Decoder written and controlled | — | Cheap; lifts every consumer of `_render`. Re-run them all in the same revision |
| **then** | **F10–F14 — the galley cluster.** F14 is SEVEN revisions INHERITED | 6.8 × 10³ px² | Re-derive each X from `BAYS` |
| **then** | **F86 — the red/cream level, 1.41× out.** A LEAD with its ceiling stated | large area | It may be carrying part of F80. Separate it before tuning nose SHAPE |
| **cheap** | **F85 — `gloss_compare.py` rewrites a tracked file** | — | One line. It dirties the tree and costs the next context a wasted hunt |
| **CEILED** | **F83 — the front arch's real 4.4 mm departure** | — | Below SPEC §2's ±8 mm lock, and the forward half is not recoverable from what we hold |
| **then** | **F02/F06 — the two absolute scales** | — | Every render-to-photograph figure in millimetres runs through a bracket |
| **parked** | **F08 — the badge STROKE WEIGHT. CEILED-rev57** | **1.4 px²** | **Not F63.** Needs a new frame or a pressing model |
| **later** | **F19** the red's edge wear; **F16/F17/F20/F23–F28, F37/F38** | — | Unblocked but ungated, or a decision rather than a measurement |
| **standing** | **F18 — the die-cut sticker** | — | The original deliverable. No gate, no owner ruling, open since rev 44 |

## §10. HOW TO GROW THIS HANDOFF WITHOUT BREAKING IT

1. **The set is three files.** `LEDGER_rev<N>.md`, `NEXT_CONTEXT_PROMPT_rev<N+1>.md`, and **`cp` of
   that file over `PASTE_INTO_CLAUDE_CODE.txt` IN THE SAME COMMIT.** `CLAUDE.md` imports the `.txt`
   into every session and a byte-identity row fails if you forget. *(The `HANDOFF_rev*.md` series
   ended at rev 45; do not restart it.)*
2. **`README.md` and `START_HERE.md` name the newest brief BY NUMBER.** Two rows check it.
3. **THE ROW COUNT IS SELF-REFERENTIAL — AND IT IS AUTOMATED, SO STOP HAND-EDITING IT.**
   `python3 audit_brief.py --fix-count` writes the clean-tree total into the brief AND into
   `PASTE_INTO_CLAUDE_CODE.txt`. **Every row you add changes the number the brief must state**, so
   write the count LAST and grep for the bare number afterwards, not just the phrase.
4. **ADD ROWS ANCHORED ON ARITHMETIC OR BEHAVIOUR, NOT ON A GREP.** A grep passes on a comment.
   **Rev 58 broke this and was caught by it in the same session:** a new row meant to forbid a
   revision-numbered default frame matched **its own explanatory comment** and reported the
   explanation as the defect — the **fifth** time a row in that file has done exactly that. It is
   tokenised now. **When you write a row about a string, strip comments first.**
5. **RUN BOTH AUDITS, AS SCRIPTS, AND RECORD WHAT THEY FOUND *IN* THE BRIEF.** `audit_brief.py`
   asks *"is what the file says true?"*; `audit_adversary.py` asks *"what would make it false?"*
   **REPLACE the adversary's questions each revision** — a question that can no longer fail is not
   a control.
6. **NEVER DELETE A CARRIER.** §0, §0.1, §4, §5, §8 and §9 are carriers.
7. **RANK BEFORE YOU CHOOSE** — `python3 visibility_budget.py`. **But the owner outranks it**, and
   at rev 58 he used that. If you work an item the script puts in the bottom half, say why.
8. **NEVER RELAX ONE COPY OF A CHECK.** `audit_brief.py` and `verify_clone.sh` assert some of the
   same things. **Loosen both or neither**, and when a check fails on code you just wrote, suspect
   the code first.
9. **DO NOT LET THE MACHINE IDLE.** Blender is CPU-bound and must not be fanned out. **Run
   `bootstrap.sh` first** — the toolchain was absent at rev 58 — then launch the render, then read.
10. **ROOM TO GROW:** new findings go in `OPEN_FINDINGS.md` with an ID and a grade, not into this
   file's prose. This file points AT the register.
