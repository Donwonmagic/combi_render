# WHAT IS LEFT — the whole remaining list, ranked for execution

**Written at rev 60c-ii, at the owner's request: *"a comprehensive list of just what exactly is
left, so we know what we need to execute, and we can streamline work."***

**THIS IS A CARRIER (`CLAUDE.md` rule 16).** Rows leave it only by being CLOSED with the
measurement that closed them or RETIRED with the ruling that retired them. It does not replace
`OPEN_FINDINGS.md` — that register holds 121 rows with their provenance grades and stays the
system of record. **This file answers a different question: of those rows, which are WORK?**

**HOW THIS WAS BUILT.** Every number in §A–§C was watched print in this session, on the render
named beside it. Anything carried from an earlier revision is labelled `[carried]` and is a claim
until re-measured. The ranking column is `visibility_budget.py 3840` — pixels of the delivery
frame — which the brief says to run before choosing, **with its own stated ceiling: pixels are not
visibility, a hard-edged error reads louder per pixel than a soft one. Use it for orders of
magnitude, not to rank neighbours.**

---

## THE ONE-SCREEN ANSWER

| | count | what it means |
|---|---|---|
| **§A REAL WORK, gated and failing** | **3** | these are what "the model is right" means |
| **§B REAL WORK, visible but UNGATED** | **6** | cheap, concrete, nobody has touched them |
| **§C NEVER-DONE COMPARISONS** | **2** | the only rows that can find an UNKNOWN defect |
| **§D INHERITED, un-re-measured** | **6** | claims, not numbers — re-measure or downgrade |
| **§E CEILED — NOT WORK** | **5** | ruled or unrecoverable. **Do not spend a revision here** |
| **§F THE OWNER'S CALL** | **3** | needs a question, not code |
| **§G THE ORIGINAL DELIVERABLE** | **1** | open since rev 44, no gate, no ruling |
| **§H INSTRUMENT / PROCESS DEBT** | **7** | not fidelity; costs revisions when it bites |

**The honest summary: about NINE things are actual model fidelity work, two of them are hard
research problems with every obvious remedy already refuted, and five more are ceiled and should
never be worked again.**

---

## §A THE THREE THAT ARE GATED AND FAILING

**The owner ruled at rev 58 that the full delivery render waits until the model is right. These
three are what that sentence means: each has a gate, each gate FAILS, and each is on his own
ranked list.**

### A1. THE EMBLEM BUILDS AS AN X — his top item, five reports [~5.5e4 px²]
`probe_rev46_vw.py` **C6 FAILS**: photograph **7** cream cells, built **6** — and at the
photograph's own scale the built glyph reads **4** (F105, so C6 UNDERSTATES it). `[carried]`

* **CAUSE, localised and painted:** the photograph's cream is **seven thin SLIVERS**, the build's
  is **four fat WEDGES**. The V and the W are each ONE mitred polyline and they fuse into two long
  diagonals crossing at the centre — that crossing IS the X.
* **FOUR ROUTES ALREADY REFUTED — do not re-spend on them.** Reach (F101: `T1_VW_CAPMIN` gives
  6→2 cells). Weight (F102: ink fraction 0.5903 built vs 0.6062 photographed; sweeping
  `T1_VW_WFRAC` to 0.48 leaves the count at 6). A six-constant spine solve (F103: 7 cells only at
  landmark residual 0.2498 against a bar of 0.045, and it collapses to 6 at the photograph's
  scale). **And the "build them as separate strokes" fix (F113) — `t1_core.vw_bars`' own docstring
  records that rev 8 did exactly that and it produced an X.**
* **WHAT IS LEFT:** F114, the angular spacing of the six terminals — **and note F103 partly
  undercuts it**, since `_on_band` preserves angle and the six spine constants are what
  `T1_VW_CELLSOLVE` already searched. **If no angular arrangement reaches 7 substantial cells at
  the photograph's own scale, say so with the number. That is a real result.**
* **IT IS ON FIVE OBJECTS, NOT ONE** (F69): the nose roundel and four hubcaps. A fix landing only
  on the nose misses 1.5e4 px² of hubcap.

### A2. THE NOSE TWO-TONE BREAK IS TOO LOW — an IMPASSE, and a localised one [5.0e4 px²]
`probe_rev59_nose.py` **M1 FAILS at 1.187** lamp radii against a photographed **1.951–2.121**.
`[carried]` The honest bracket on the error is **50–80 mm**, best single estimate 52 mm.

* **THE WHOLE REMEDY PROGRAMME IS REFUTED (F106/F107).** An 8× sweep of `V_POW` moves the break by
  **0.004** lamp radii; `V_RISE` and `V_POW_Z` likewise. The switches are NOT inert — the extreme
  arms differ over 128,421 px — the change just lands at the V's **apex**, where it does nothing
  for the lamp.
* **A two-constraint analytic solve was built, predicted 0.604 where the machine measures 1.187,
  and was THROWN AWAY rather than shipped.** Do not rebuild it: solve against the SHADER or
  against renders.
* **THREE UNTESTED CANDIDATES, one render each:** the hard-coded **0.860** divisor in
  `body_paint`'s `u = |y| / 0.860`; `tblend`'s **1.858 → 2.012** smoothstep, which is on **X** and
  clamps to 1 well before the lamp; and `HL_DROP`, the other side of the ratio — refuted at rev 58
  on a 2σ conflict, so that conflict needs re-measuring first.

### A3. "SEÑOR TACOMBI" IS NOT CLEAR — and the deficit is in the ARTWORK, not the render [2.7e4 px²]
`flank_compare.py` on `out/r60d_side.png`: **FAIL, worst region `i` at 0.684** against a 0.75 bar.
Everything else passes — ink area 0.9769, aspect 2.3689, IoU 0.7576 (0.882 of a measured 0.8591
ceiling). **Measured this session.**

| region | IoU | its ceiling | of ceiling | ref px | render px | **tex-only** |
|---|---|---|---|---|---|---|
| `c` | 0.912 | 0.844 | 1.080 | 1025 | 1036 | 1.047 |
| `a` | 0.862 | 0.871 | 0.990 | 1151 | 1203 | 1.050 |
| `o` | 0.811 | 0.847 | 0.958 | 975 | 994 | 0.878 |
| `m` | 0.767 | 0.854 | 0.898 | 1084 | 1057 | 0.854 |
| `b` | 0.645 | 0.863 | 0.747 | 994 | 1052 | 0.709 |
| **`i`** | **0.580** | 0.848 | **0.684** | 657 | 661 | 0.647 |
| **`Senor`** | **0.564** | 0.781 | **0.721** | **1261** | **978** | 0.757 |

* **THE `tex-only` COLUMN IS THE FINDING.** It is `tex/senor.png`'s ALPHA laid on the `SCR`
  rectangle with **no render and no mask rule** — and it tracks the render almost exactly
  (`i` 0.647 vs 0.684; `b` 0.709 vs 0.747). **The render and the whole chromaticity mask rule
  together are worth only +0.014 of ceiling.** So this is not a shader, lighting or resolution
  problem: **it is the artwork's alpha and its placement** (F39).
* **RESOLUTION IS ALREADY DONE AND DID NOT FIX IT.** `tex/senor.png` is **4096 × 1738** and its
  alpha runs to within 12 of its own 4096 columns, so the texture's own extent accounts for only
  3.8 mm. Raising it further will not move this.
* **THE WORD `Señor` IS 283 px OF INK SHORT (1261 → 978, 22 %)** — the largest single discrepancy
  in the table, and a different failure from `i`'s.
* **A12 MAKES THE REMEDY THE OWNER'S CALL** (*"absolute replication of all artwork"*, F94). **But
  measuring it and proposing a specific fix is ours, and has not been done.**

---

## §B REAL WORK, VISIBLE, AND UNGATED — nobody has touched these

**These are the cheapest fidelity wins on the page. Each is concrete, each was measured off a
frame, and none has a gate — which is exactly why they have survived.**

| # | what | measured | why it is cheap |
|---|---|---|---|
| **B1** | **F73 — a ~0.305 m MEMBER PROJECTS FROM THE TAIL SKIN AND ENDS IN MID-AIR**, 0.28 m clear of any surface, with a blunt cut | two hairlines meet the tail skin at side (1309, 531); one is `tail_board_stay` at 68 px = 0.251 m against its own logged 0.247 m, **correct**; the other runs down-and-aft 82.8 px = **0.305 m into empty white** | **unidentified — could not be named without Blender.** Candidates: a second segment from `T.sweep(wire,…)` on the 2-point stay wire, a `lid_strut`, or `tb_bulbflex`'s start segment. **One build and a name closes it** |
| **B2** | **F71 — the cab glazing is a FLAT COLOUR FIELD and stops short of its own aperture** | pane sd **(0.84, 0.71, 0.70)**, range 139–145 — **6 DN of structure** — against `studio.py`'s own cabin_fill target of an **80 DN** range. The LEVEL is right (143), the STRUCTURE is absent. And the glazing stops **21 px ≈ 80 mm** inboard of the aperture, full height | the SHORT half is a constant. The FLAT half is not |
| **B3** | **F72 — the exterior counter props are the same value as the painted body**, silhouetted against cream in the brightest part of the hero | warmer **186.6**, caddy **185.4**, painted cream **187.8** — within **2.4 DN**. `ref_side.jpg` shows a **60+ DN spread** across the same rank | cause named: `GAL_STEEL` at rough 0.44 / metal 1.0 under a white surround |
| **B4** | **F74(a) — `tex/lidmural.png` is CROPPED AT THE BOTTOM** — flowers sliced mid-bloom, yellow side columns truncated, where `ref_side.jpg` shows a board framed on all four sides | the render is faithful to the asset, so the defect is in `lid_gen.py`'s output | **⚠ `lid_gen.py` is NOT called by `build.py` — regenerate by hand or the render silently uses the old texture** |
| **B5** | **F74(b) — `GAL_RED` is a dusty beige-pink** | `(0.5350, 0.3600, 0.3120)` ≈ sRGB (196, 163, 153), on two squeeze-bottle caps, where `ref_rear34.jpg` shows **saturated red and yellow** | one constant |
| **B6** | **F86 — the red/cream LEVEL at the nose, and it is NOT ceiled** | the two nose instruments disagree by **1.41×**, and the reason is the red/cream level, not the lamp | **F80's headlamp gap IS ceiled to the surround; F86 is a paint-level question and is not.** Distinguish them |

---

## §C THE TWO COMPARISONS NEVER DONE — the only rows that can find an UNKNOWN defect

**Everything in §A and §B works a defect that is already known. These two can turn up something
nobody has seen. Rev 51 did exactly this for the NOSE and found THREE real defects by eye alone —
flush headlamps, the roundel's short V-arms, a flat nose — that no gate had ever reported.**

* **C1. F91 — THE TAIL AND THE ROOF AGAINST A PHOTOGRAPH. Two thirds of the owner's own standing
  bar, never once done in 60 revisions.** `ref_rear34.jpg` exists and is the target bus.
  **FIRST PASS DONE at rev 60c-ii on the TAIL (F128); the ROOF is still not done.** What it found:
  * **The red's excess blue is the SURROUND, not the paint — and that refutes a fix nobody had
    tried yet.** Photograph red B/R **0.046** (`ref_rear34`) and **0.047** (`ref_side`), two scenes
    with very different light — spread **0.001**. Render **0.218** (`hero34r`) and **0.351**
    (`side`), two views of ONE build — spread **0.133, 133× wider**. A term that swings that much
    with camera position is what the paint REFLECTS, i.e. E1's ceiling. **Do not warm a paint
    constant to close it.**
  * **The tail lamp is close**: within-frame lamp/red luma 0.877 photographed vs 0.801 rendered.
  * **NOT a defect, checked**: the two horizontal lines on the rear panel are the engine lid's own
    shut line, which `ENGLID_GAP` builds. **Recorded so nobody chases a swage that is there.**
  * **NOT comparable, deliberately not claimed**: the lamp's aspect ratio — it is pose-dependent
    by the model's own control (1.189–1.847) and `hero34r` is not pose-matched to the reference.
  * **STILL TO DO: the ROOF**, and a tail pass from a camera actually matched to `ref_rear34.jpg`
    — in `hero34r` the tail is small and half-occluded by the counter.
* **C2. F45's ROOF-APERTURE INTERIOR — never separately measured** [3.5e5 px²]. F98 refuted the
  "untextured white blocks" claim for the GALLEY bays only; the roof aperture half was never
  measured and appears in no ledger because nothing could gate it.

---

## §D INHERITED AND UN-RE-MEASURED — claims, not numbers

**`OPEN_FINDINGS.md`'s own rule: an `INHERITED` row that survives three more revisions without
being re-measured should be re-measured or downgraded. All six are past that.**

| # | row | age |
|---|---|---|
| **D1** | **F14** — `gal_end_f`'s 260.0 / 20.0 mm sight lines | **rev 52 — EIGHT revisions** |
| **D2** | **F15** — A7, an **803 mm** run of unlit roofed body between the last light inlet and the tail skin, unbuilt. `roof_cutters()`'s aft edge is `LID_X1` | rev 52. **8.2e5 px² — the 4th largest item in the whole budget** |
| **D3** | **F10** — the galley sits ~103 mm too far aft | rev 52 |
| **D4** | **F20** — SPEC §8's colour locks, graded **M off a RETIRED 246×197 thumbnail**. Re-derivable on `ref_playa_34.png` at **4× the area** | rev 52. Report the values; W6 makes the change his call |
| **D5** | **F16 / F17** — gold core; pressed-into | rev 4x |
| **D6** | **F06 / F25** | rev 1x / rev 5x |

---

## §E CEILED — NOT WORK. Do not spend a revision on any of these.

**Each is either ruled by the owner or established as unrecoverable from what we hold. Rule 12:
*"it cannot be recovered from what we hold"* is a real result. Re-opening these has cost this
project revisions.**

| # | row | the ceiling |
|---|---|---|
| **E1** | **F44 / F60 / F62 — THE PAINT'S GLOSS.** `gloss_compare.py` **FAILS at 0.426** (bar 0.60) on `out/r60c_hero.png`, measured this session | **The model-side lever is EXHAUSTED.** F62 measured what this flank actually reflects: a featureless white cyclorama **19.3 m** away. The frame reads as clay because the paint has nothing to reflect. **The owner was shown this, told the cost, offered four routes, and ruled *"keep studio, fix the model"*.** The gate is a RULER, not a verdict |
| **E2** | **F67's RESIDUE — the ground shadow.** G4 **0.3602** built / 0.5475 ablated / **0.2581** at the top of the photographed ceiling band / **0.057** photographed. Measured this session | **APPORTIONED at rev 60c, which is new:** the assumed 0.090 m drop owns **0.1021** of the residue; even at the most generous drop the photograph is still **0.202** away, **and that remainder is the studio — E1's ceiling**. The shipped constant stays 0.090 deliberately: the 0.137–0.155 m band is a CEILING containing both the metal and the ground shadow, and setting a constant to a ceiling would assume the band is all metal. **A low raking shot under the sill is the one new frame that would settle it** |
| **E3** | **F83 — the front arch** | Real, but **4.4 mm rms**, inside SPEC §2's ±8 mm lock, forward half unrecoverable. **Owner ruled *"leave it circular"*. Do not build it and do not mirror it.** `probe_rev59_door` M3 stays failing as the honest open record |
| **E4** | **F80 — the headlamp reads as a dark hole** | **Ceiled to the surround** — the photograph has a sky for the lens to reflect and the studio does not. **F86 is the part that is NOT ceiled (see B6)** |
| **E5** | **F08 — the badge STROKE WEIGHT** | **CEILED-rev57.** Different finding from F63. The photograph cannot resolve the V/W centre gap at 68 px |

---

## §F THE OWNER'S CALL — needs a question, not code

**Ask as MULTIPLE CHOICE, one crop, one mark, one sentence, with the reference attached, and ASK IT
WITH THE QUESTION TOOL. A revision has been lost to sending the figures and forgetting to ask.**

* **F1. A3's remedy** — `Senor`'s ink deficit is in the artwork, and **A12** (*"absolute
  replication of all artwork"*) makes the remedy his. **This is now measured well enough to ask.**
* **F2. F38** — the built nose ring band sits at the top of its adopted range (**0.10086** against
  three frame readings at 0.087–0.093), and moving it moves the glyph's fit radius with it, **which
  interacts with A1**. Decide whether to ask; do not simply carry it.
* **F3. F20 / SPEC §8 colour locks** — report the re-derived values off `ref_playa_34.png`; **W6**
  makes the change his call.

**DO NOT RE-ASK, ANY OF THESE — all refuted or already ruled:** the studio (ruled twice); the front
arch (ruled); the lower bay SHUT; the roof strips' 0.3 m; the wipers; the tail board; the stars;
`lid_rail`'s width; the roughness trade (*"ship 0.250"*); **F99's interior warmth and F100's gold
surround — both measured on a DIFFERENT STATE of the vehicle (rule 11)**; **F111's glazing — the
bays read OPEN and `STATE.md` already matches**; `PHOTOS_WANTED` items 1–5 (*"not possible now"*)
and item 6 (dissolved at rev 51).

---

## §G THE ORIGINAL DELIVERABLE — still open

**F18 — THE DIE-CUT STICKER.** Open since **rev 44**, the oldest live row in the register. It was
lost when a standing-instructions carrier was rewritten, and went undetected for five revisions.
**No gate, no ruling, no owner question outstanding.** It is the thing the project was originally
for.

---

## §H INSTRUMENT AND PROCESS DEBT — not fidelity, but it costs revisions

| # | row | state |
|---|---|---|
| **H1** | **`mottle_measure.py` is NOT measuring the mottle** — 1.1–2.0 % of it. Rev 56's reading and rev 57's item B are **REFUTED** `[carried]` | the gate is live and reports a number about the wrong thing |
| **H2** | **F42 — every measurement through `shader_solve._render` is 8-BIT**, whatever `color_depth` says, behind a guard that cannot fire | |
| **H3** | **F41 — the ALBEDO arm is blind to the larger half of the mottle BY CONSTRUCTION**; **F05** — the BEAUTY arm refuses (100 % clipped), **cheap now that F51 is fixed** | |
| **H4** | **F88 / F95 — `gloss_compare.py` rebuilds its red mask from every frame so the mask can WALK OFF the defect**, and it reads the target's paint finish off a **NOLITA** frame, which is admitted for GEOMETRY ONLY (rule 11) | |
| **H5** | **F49 / F50 — `stitch.py`'s guard fired and the runner ignored it**; its docstring describes a better design than its code implements | matters only at delivery |
| **H6** | **F97 — the shell's n-gon count has grown 1.8×** (2,876 → **5,191**) and nothing tracks it. 0 non-manifold edges | **LOW.** Deliverables are stills and a sticker, so nothing reads the topology — but the original handoff's condition was *"if the mesh is ever delivered"* |
| **H7** | **F115 — `tex/emblem.png` is 1024×1024 and BLOCKED** from regeneration. **8 of 9 textures now meet SPEC §5's 3K floor** (measured this session); against the owner's stated **4K** bar, `calidad.png` and `nose.png` sit at 3072 | the 3K floor is now an asserted row for the first time |

---

## WHAT THE MACHINE SAYS TODAY — every one watched print this session

```
bootstrap.sh          ALL 10 PASS
verify_clone.sh       ALL 268 PASS on a clean tree   <- 0 FIDELITY, 268 SELF-CONSISTENCY
VERIFY (in build)     0 fail, 0 warn at SUB=1 AND SUB=2
  underbody proudness worst -55.8 mm, INBOARD of the skin everywhere
  underbody/shell fit worst intrusion +10.5 mm over 1400 perimeter stations, both signs of y
probe_rev45_ground    5 checked, 0 FAILED.  G4 0.3602 built / 0.5475 ablated / 0.057 photographed
flank_compare.py      FAIL  worst region `i` 0.684 (bar 0.75)
gloss_compare.py      FAIL  0.426 (bar 0.60)
textures              8 of 9 >= 3072 px; emblem.png 1024 BLOCKED
```

**AND THE STANDING WARNING, WHICH `verify_clone.sh` PRINTS ITSELF:** a green check is not evidence
about the vehicle. **Not one of those 268 rows compares the model to a photograph.** The trunk lid
that opened inwards, the board's foot buried in the roof, the disc of body red in every tail lamp,
the five-petal hubcaps — every one passed this script and was found by **looking at a crop**.

---

## IF YOU WANT THE SHORTEST PATH

1. **§C1 (F91, the tail and roof) and §B — one session.** §C1 is the only thing that can find an
   unknown defect and it is half done; §B is six concrete defects with causes already named. **This
   is the highest ratio of fidelity to effort on the page.**
2. **§A3 (`Senor`) — measure the fix, then ask.** It is measured well enough now that the owner
   question is answerable in one round.
3. **§A1 and §A2 are research, not tickets.** Every obvious remedy is refuted and recorded. Budget
   a whole revision for either, and **be willing to close it with a number that says no
   arrangement works** — that is a real result here.
4. **§E is closed. §D is six re-measurements. §G is one decision nobody has made.**
