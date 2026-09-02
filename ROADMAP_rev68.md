# THE ROAD TO THE FINAL RENDER — the whole remaining list, triaged

**Written at rev 68, at the owner's request: *"What is left to be done? Can we establish a list
so that we can attack it methodically to get to the point of investing in the final render?"***

**THIS FILE DISCHARGES `REMAINING_WORK_rev61.md` §I** — the 27 untriaged rows that had been open
for eight revisions. Every one of them is placed in a tier below. `REMAINING_WORK_rev61.md`
remains a carrier and is NOT deleted (rule 16); this file supersedes its ranking only.

**EVERY FIGURE HERE WAS RE-RUN AT REV 68's HANDOFF COMMIT, NOT TRANSCRIBED.** Where a number is
inherited and was not re-measured this revision, it says so in the row.

---

## THE ONE THING TO UNDERSTAND FIRST

**THE LIST IS LONG. THE CRITICAL PATH IS SHORT, AND THE OWNER DEFINED IT HIMSELF.**

He has held the delivery render four times — rev 58, 64, 65 and again at 65 — and each time he
named what the hold is *for*:

> *"Keep holding — fix the emblem first."* (rev 64, F191)
> *"I don't think the bus is ready yet. We need the bus to be ready before investing seriously
> in the render."* (rev 65, F193)
> *"I can't believe that we can't even accomplish a publicly available emblem, and we still have
> work to do on the shape of the nose."*

**So TIER 0 is the whole of the critical path: the EMBLEM and the NOSE.** Everything in tiers 1–8
is real work that would make the model better, and **none of it is what he is waiting on.** A
revision spent on tier 3 while tier 0 is red is a revision that does not move the render closer.

**The honest shape of it:**

| | items | is it on the critical path? |
|---|---|---|
| **TIER 0 — what he named** | 2 | **YES. Nothing else is.** |
| **TIER 1 — the gates that fail against a photograph** | 2 | one is probably a GATE decision, not a defect |
| **TIER 2 — big-area, measured, untouched** | 4 | no — but these are the largest pixel counts in the frame |
| **TIER 3 — the panel items** | 10 | no |
| **TIER 4 — comparisons never done** | 2 | no, and they are the only rows that can find an UNKNOWN defect |
| **TIER 5 — inherited claims, not numbers** | 6 | no |
| **TIER 6 — instrument debt** | 8 | no, but it costs revisions when it bites |
| **TIER 7 — needs HIM, not code** | 5 | **two of these gate the render's SIZE** |
| **TIER 8 — the original deliverable** | 1 | separate deliverable |

---

## TIER 0 — THE CRITICAL PATH. THIS IS WHAT "THE BUS IS READY" MEANS.

### 0.1 THE EMBLEM — his SEVENTH report of the same object

**TWO live sub-defects, and they are not the same finding.**

**(a) F205 — the render cuts THREE interior cells where the photograph cuts SIX.**
Measured at rev 67 on the frame: photograph **6**, render **4 / 3 / 2** at ink thresholds
20 / 30 / 40. **NOT re-run at rev 68.**
**⚠ AND THE INSTRUMENT DOES NOT EXIST AS A SCRIPT.** `probe_rev46_vw.py`'s C6 reads the
**RASTER** and passes 6 = 6; the render-side count that disagrees was an ad-hoc measurement and
is in no committed file. **First job: commit the render-side instrument, then re-measure on
`out/r69_front.png`.** A gate that passes on a proxy while the delivered pixels fail is rule 41.

**(b) C4 — the W's outer arms, 0.0755 against a bar of 0.045.** The owner's own words: *"The W's
outer arms sit too low."* Largest single error is L4 at **+0.0634**.
**⚠ THE PRESCRIBED FIX CANNOT WORK AS WRITTEN (F224).** `T1_VW_SOLVE=1` clips every X parameter
to `(0.05, 0.95)`; the shipped `VW_W_ARM_X` is **1.1002**, outside it — **zero admissible trials
over all nine step halvings**, and the solver cannot even return to the shipped point.
`T1_VW_CELLSOLVE`'s box excludes two of six as well. **Widen the clip from the CONSTRUCTION and
add a reachability row BEFORE running it** — do not widen it to admit only the current value.

**WHAT IS ALREADY REFUTED AND MUST NOT BE RE-TRIED:** seventeen rows, `NEXT_CONTEXT_PROMPT_rev69.md`
§2. Every obvious remedy is on it. **Budget a whole revision, and be willing to close it with a
number that says no arrangement of the six constants works** — that is a real result here.

### 0.2 THE NOSE — retargeted at rev 68, and it now has a measured, camera-free object

**THE DEFECT IS THE BUMPER'S FLAT PLAN FACE (F222), NOT `NOSE_BULGE`.**
Built `bumper_f` top edge: **x(0) − x(0.70) = +0.05 mm** — dead flat, by construction, over
precisely the window the photograph was measured on. The photographed bumper's near half is
curved at **11–14 σ**, and that sign is **projection-invariant**: it needs no camera model, no
EXIF, no distortion term.

**WHAT IS NEEDED IS THE NUMBER, AND THERE ARE TWO ROUTES:**
* **The literature.** The owner ruled it: *"This has to be a commonly available measurement."*
  (F229). Named sources: `thesamba.com/vw/forum/viewtopic.php?p=9884153` ("Dimensions front mask
  VW T1") and `thesamba.com/vw/archives/info/split_bus_dimensions.php`. **Every one was
  `EGRESS_BLOCKED` in the rev-68 container — try again, the policy is per-environment.**
* **F216's camera-free route, which needs nothing from anybody.** The symmetric hard points
  (`HL_Y 0.5450`, `IND_Y 0.6750`, corners |y| ≈ 0.875) give the y-vanishing point from the frame
  itself at sensitivity `sin(az) = 0.80` — **4.1× the bumper-edge route.** `ref_workshop.jpg` and
  `IMG_2073.jpeg` show both bores, both indicators and both corners unoccluded. **This is the
  measurement this project should have made three revisions ago.**

**DO NOT fit `NOSE_BULGE` to 40 mm.** F223: propagating F221's own failed validation gives
B ∈ [16, 76] mm, which **contains the shipped 19.6**. The owner's *"rounder than D"* stands as a
ruling on DIRECTION and carries no number.
**ENABLING WORK IS DONE:** F217 is cleared — the fixtures follow the skin, guarded, watched
failing. What binds a bulge change now is `length` (0.045 → `warn 4.073 vs 4.055`), not the fold.

---

## TIER 1 — THE TWO GATES THAT COMPARE THE MODEL TO A PHOTOGRAPH, AND FAIL

**These are the only three gates in the tree that score against a frame, and two fail.
RE-RUN AT REV 68 on `out/r68_*.png`, watched printing:**

| gate | live figure | what it is |
|---|---|---|
| **`flank_compare.py`** | **FAIL — worst region `i` at 0.680**, target ≥ 0.75. Ink area 1.0535 PASS, aspect 2.3581 vs 2.3259 PASS, IoU 0.7472 PASS | **Only ONE row now fails.** But **F156: the `Senor` row scores a DELIBERATE DEPARTURE** — the owner ruled the script should be *clearer than the photograph*, and the gate scores against the photograph. **EIGHT revisions un-re-based.** Rule 40: this gate stopped meaning what it meant |
| **`gloss_compare.py`** | **FAIL — 0.441 of the photograph's spread**, bar 0.60. Brightest 1 % sits 0.157 above its own median | **Probably a GATE decision, not a defect.** Its own verdict says part of the gap is *"the white cyclorama having nothing to reflect, which the owner has ruled stays"*. Model-side lever is recorded EXHAUSTED (F60/F62) — **but F62's ceiling is DISPUTED on measurements.** Decide: re-base the bar against the ruled studio, or reopen F62 |

**THE STANDING WARNING:** `verify_clone.sh`'s 342 rows are **0 FIDELITY, 342 SELF-CONSISTENCY**.
Not one compares the model to the vehicle. **Never quote its total as fidelity.**

---

## TIER 2 — THE LARGEST DEFECTS BY DELIVERY-FRAME AREA, MEASURED AND UNTOUCHED

**Ranked by `visibility_budget.py 3840 out/r68_hero.png`, RE-RUN AT REV 68.**
**Its ceiling: pixels are not visibility. Use it for ORDERS OF MAGNITUDE, and the owner has
overridden it three times.**

| rank | id | what | area |
|---|---|---|---|
| 1 | **F67** | the contact shadow's footprint on the ground — *what makes it read planted rather than floating* | **4.56e6 px²** |
| 2 | **F44** | the paint's gloss, cream upper body | **2.48e6 px²** |
| 3 | **F44** | the paint's gloss, red flank | 9.61e5 px² |
| 4 | **F15** | **A7 — an 803 mm run of unlit roofed body** between the last light inlet and the tail skin. Illumination over a large area, not dressing | 8.23e5 px² |
| 5 | **F45** | the roof-aperture interior — **never separately measured**, dead centre of the hero frame | 3.46e5 px² |

**⚠ THE BUDGET FILE IS ITSELF PARTLY STALE and says so where it is:** its `F63/F69 "the VW glyph
builds as an X"` row predates rev 63's change (it is no longer an X); `F99` is DOWNGRADED (wrong
vehicle state, rule 11). **Read the rows, not just the ranking.**

---

## TIER 3 — THE PANEL ITEMS: VISIBLE, CONCRETE, CHEAP, AND NOBODY HAS TOUCHED THEM

**Eight revisions untouched. Each was measured off a frame; each has a named cause; none has a
gate — which is exactly why they survived.** These are the highest fidelity-per-hour on the page.

| # | what | the measurement |
|---|---|---|
| **3.1** | **the cab glazing is a FLAT COLOUR FIELD and stops short of its own aperture** (F71) | pane sd (0.84, 0.71, 0.70), range **6 DN** against `studio.py`'s own **80 DN** target. Level right (143), structure absent. Glazing stops **21 px ≈ 80 mm** inboard of the aperture, full height |
| **3.2** | **the tyres have no tread, no sidewall lettering, and are 35 % too light** | inherited from the panel list; **not re-measured at rev 68** |
| **3.3** | **the tail is a box where the real one is a barrel** | inherited; **not re-measured** |
| **3.4** | **every shut line is a 1-px ink stroke with no leading-edge highlight** | inherited; **not re-measured** |
| **3.5** | **F73 — a ~0.305 m MEMBER PROJECTS FROM THE TAIL SKIN AND ENDS IN MID-AIR**, 0.28 m clear of any surface, blunt cut | traced on `side` at (1309, 531): 82.8 px = 0.305 m into empty white. **Unidentified — one build and a name closes it.** Candidates: a second segment from `T.sweep(wire,…)`, a `lid_strut`, or `tb_bulbflex`'s start |
| **3.6** | **F72 — the exterior counter props are the same value as the painted body**, silhouetted in the brightest part of the hero | warmer 186.6, caddy 185.4, painted cream 187.8 — within **2.4 DN**, where `ref_side.jpg` shows a **60+ DN spread**. Cause named: `GAL_STEEL` rough 0.44 / metal 1.0 under a white surround |
| **3.7** | **F74(a) — `tex/lidmural.png` is CROPPED AT THE BOTTOM**, flowers sliced mid-bloom | the render is faithful to the asset; the defect is in `lid_gen.py`'s output. **⚠ `lid_gen.py` is NOT called by `build.py` — regenerate by hand or the render silently uses the old texture** |
| **3.8** | **F74(b) — `GAL_RED` is a dusty beige-pink** | (0.5350, 0.3600, 0.3120) ≈ sRGB (196,163,153) where `ref_rear34.jpg` shows saturated red and yellow. **One constant** |
| **3.9** | **the galley is monochrome; the counter is a floating slab** | inherited; **not re-measured** |
| ~~**3.10**~~ **RETIRED** | ~~**F143 — TWO LOUDSPEAKERS STAND ON THE ROOF AND ARE UNMODELLED**~~ | ⚠ **RETIRED AT REV 74 (F309). *"They are on the vehicle in the frames"* IS THE CLAIM THAT WAS WRONG** — they are on it in ONE frame, with the mural board up, and the roof is BARE in two independent scenes. **REMOVABLE EVENT GEAR, i.e. a POSE. Annotated, not deleted (rule 16). Read F309.** |

---

## TIER 4 — THE COMPARISONS NEVER DONE. THE ONLY ROWS THAT CAN FIND AN *UNKNOWN* DEFECT.

**Rev 51 did exactly this for the nose and found THREE real defects by eye alone — flush
headlamps, short V-arms, a flat nose — that no gate had ever reported. It is the highest-yield
thing on this page and it has been done once in 68 revisions.**

* **4.1 — THE ROOF against a photograph. NEVER DONE.** Two thirds of the owner's own standing bar.
  The TAIL got a first pass at rev 60c-ii (F128); the ROOF never has.
* **4.2 — A TAIL PASS FROM A CAMERA ACTUALLY MATCHED TO `ref_rear34.jpg`.** In `hero34r` the tail
  is small and half-occluded by the counter, so the existing pass is weak.
  *(What 4.1's first pass already established, and it is worth carrying: the red's excess blue is
  the SURROUND, not the paint — photograph B/R 0.046 and 0.047 across two very different scenes,
  spread 0.001; render 0.218 and 0.351 across two views of ONE build, spread 0.133, **133× wider**.
  **Do not warm a paint constant to close it.**)*

---

## TIER 5 — INHERITED CLAIMS, NOT NUMBERS. RE-MEASURE OR DOWNGRADE.

**The register's own rule: an `INHERITED` row surviving three more revisions un-re-measured should
be re-measured or downgraded. All six are far past that.**

| # | row | age |
|---|---|---|
| 5.1 | **F14** — `gal_end_f`'s 260.0 / 20.0 mm sight lines | **rev 52 — SIXTEEN revisions** |
| 5.2 | **F15** — the 803 mm unlit run (also TIER 2 #4 by area) | rev 52 |
| 5.3 | **F10** — the galley sits ~103 mm too far aft | rev 52 |
| 5.4 | **F20** — SPEC §8's colour locks, graded off a **RETIRED 246×197 thumbnail**. Re-derivable on `ref_playa_34.png` at **4× the area** | rev 52 |
| 5.5 | **F16 / F17** — gold core; pressed-into | rev 4x |
| 5.6 | **F06 / F25** | rev 1x / rev 5x |

---

## TIER 6 — INSTRUMENT AND PROCESS DEBT. NOT FIDELITY, BUT IT COSTS REVISIONS.

**Rev 68 alone found FIVE instruments reporting things that are not measurements. This tier is
why.** Budget for it: every recent revision has caught four to seven of its own instruments wrong.

| # | what | state |
|---|---|---|
| 6.1 | **F226 — `PHOTO_E, PHOTO_N = 3.390, 7` is hard-coded in THREE probes**, and in `probe_rev63_ablate.py` `PHOTO_N` is a **hard SEARCH CONSTRAINT** — while §2 says chasing 7 is refuted. Also `probe_rev64_shear.py`'s S4 | **re-point or refuse them before running any of the three** |
| 6.2 | **F226 — C8's target was NEVER re-based.** F194 and the horizon section say it was; the instrument still returns the 69/41 bbox squash, live value **3.3896**, and `grep` for 2.627 finds nothing | either wire the re-base in or stop saying it happened |
| 6.3 | **F224 — the solver's X clip** (also TIER 0) | blocks C4 |
| 6.4 | **`mottle_measure.py` is NOT measuring the mottle** — 1.1–2.0 % of it | the gate is live and reports a number about the wrong thing |
| 6.5 | **F42 — every measurement through `shader_solve._render` is 8-BIT**, whatever `color_depth` says, behind a guard that cannot fire | |
| 6.6 | **F88 / F95 — `gloss_compare.py` rebuilds its red mask from every frame, so the mask can WALK OFF the defect**, and it reads the target's finish off a NOLITA frame admitted for GEOMETRY ONLY (rule 11) | **this touches TIER 1** |
| 6.7 | **F49 / F50 — `stitch.py`'s guard fired and the runner ignored it** | **matters only at delivery — see TIER 7.4** |
| 6.8 | **F115 / H7 — `tex/emblem.png` is 1024×1024 and BLOCKED from regeneration** (`texgen.make_emblem` raises *"no usable font"*). Against the owner's **4K** bar, `tex/calidad.png` and `tex/nose.png` sit at **3072** | the 3K floor is an asserted row; the 4K bar is a decision |

---

## TIER 7 — NEEDS THE OWNER, NOT CODE. **TWO OF THESE GATE THE RENDER ITSELF.**

**Ask as MULTIPLE CHOICE, one crop, one mark, one sentence, with the reference attached, and ASK
IT WITH THE QUESTION TOOL. CHECK THE PREMISE FIRST — rev 68 asked one he rejected outright.**

| # | what | why it is his |
|---|---|---|
| **7.1** | **THE DELIVERY DIMENSION IS STILL OPEN.** *"Bigger — large-format print."* **3840 is NOT the target (F192).** **Do not ask cold — ask once there is something to show him** | **GATES THE RENDER.** You cannot render the final frame without knowing its size |
| **7.2** | **"LOOK LIKE NEW" vs SPEC §3's WEATHERED LOCK.** *"I want this 3d model to look like new. Enhanced from the photo."* (rev 61) collides with the SPEC's weathered lock | **GATES THE RENDER'S WHOLE FINISH. Surface it — do not silently pick a side** |
| 7.3 | **F1 — `Senor`'s ink deficit remedy.** The deficit is in the ARTWORK, and A12 (*"absolute replication of all artwork"*) makes the remedy his. **Measured well enough to ask now** | interacts with F156 in TIER 1 |
| 7.4 | **F38 — the built nose ring band sits at the TOP of its adopted range** (0.10086 against three frame readings at 0.087–0.093), and moving it moves the glyph's fit radius | **interacts with TIER 0.1** |
| 7.5 | **F20 / SPEC §8 colour locks** — report the re-derived values off `ref_playa_34.png`; **W6 makes colour his call** | |

**DO NOT RE-ASK ANY OF THESE — ruled or refuted:** the studio (twice); the front arch; the lower
bay SHUT; the roof strips; the wipers; the tail board; the stars; `lid_rail`'s width; the
roughness trade; `PHOTOS_WANTED` 1–5 and 6; **the bumper straight-edge (F229, rev 68)**; **the
nose, which has had both its askings (F214/F215)**.

---

## TIER 8 — THE ORIGINAL DELIVERABLE, STILL OPEN

**F18 — THE DIE-CUT STICKER.** Open since **rev 44** — the oldest live row in the register. It was
lost when a standing-instructions carrier was rewritten and went undetected for five revisions.
**No gate, no ruling, no owner question outstanding. It is the thing the project was originally
for**, and it is a separate deliverable from the hero render, not a blocker on it.

---

## AND THE DELIVERY CHAIN ITSELF — WHICH HAS NEVER BEEN PROVEN AT THE SIZE HE WANTS

**F192.** `hq_render.py` → `stitch.py` → `post.py` is a different chain from the preview path.
It has never been run at large format. **The owner ruled the MODEL comes first (F193), so this
sits BELOW the model defects — but it is not zero work, and it is the last thing between a
finished model and a delivered file.** When it is time:

```
T1_SUB=2 blender -b -P hq_render.py     # ONE build, 10 bands, WITH MARGIN
python3 stitch.py ...                   # CHECK ITS EXIT CODE -- 2 on a seam (F49)
python3 post.py in.png out.png          # optics LAST, never per strip
```
**And `post.py` is never called by the preview path (F146)** — judge photorealism on the `_post`
set or you are judging the wrong pixels.

---

## THE SHORTEST HONEST PATH TO THE RENDER

1. **TIER 0.1 (the emblem) — one revision, and commit the render-side instrument FIRST.**
   Fix the solver clip (F224) before running the solve, or it is theatre.
2. **TIER 0.2 (the nose/bumper) — one revision.** Get the number from the literature or F216's
   camera-free route, build the bumper's plan curve with a named constant and an ablation switch,
   then render, crop and LOOK — **and render the control twice (F228).**
3. **ASK 7.1 AND 7.2 THE MOMENT TIER 0 IS GREEN.** Both gate the render and neither can be
   answered by code. Do not ask them cold — ask with the finished nose and emblem to show.
4. **THEN TIER 4.1 — the ROOF against a photograph — BEFORE the final render, not after.** It is
   the only thing left that can find a defect nobody knows about, and finding one *after* a
   large-format render costs the render.
5. **TIER 3 is the cheapest quality per hour** and can be done in parallel with waiting on him.
6. **TIER 1's gloss gate is a DECISION, not a defect** — settle whether the bar is scored against
   a studio the owner has ruled stays.

**WHAT I CANNOT TELL YOU:** how many revisions tiers 0.1 and 0.2 take. Every obvious remedy for
the emblem is already refuted and recorded — it is research, not a ticket, and it may close with
a number that says no arrangement of the six constants reproduces the photograph. That is a real
result and it is worth more than a guess.
