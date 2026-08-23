# NEXT CONTEXT PROMPT — rev 58

## §0.0 DO THIS FIRST — THE WHOLE DECISION, IN TWENTY LINES

**Before you read another word, put the machine to work. It is CPU-bound and idle right now.**

```bash
cd /home/user/combi_render
nohup env T1_SUB=1 T1_PREVIEW=side T1_PFX=r58 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py > /tmp/r58side.log 2>&1 &
```

`out/` is untracked and starts empty, and every revision until now has waited ~10 minutes for that
before it could touch a gate. **Start it, then read.**

**THE RANKING RULE CHANGED AT REV 57b, AND IT IS THE MOST IMPORTANT LINE IN THIS FILE.**
The old rule was *"gate availability"*. It selected the least visible work available, for four
revisions running, and `AUDIT_rev57_efficiency.md` measures the damage: **the last four revisions
changed six lines of model code between them, two of them zero, against 6,503 lines of prose.**

> **THE RULE IS NOW: RANK BY PIXELS OF THE DELIVERY FRAME. `python3 visibility_budget.py` prints
> the table. Gate availability is a TIE-BREAKER, not the rule.**

**What that makes rev 58's order** (run the script; do not trust this table, it is a copy):

| # | do | worth | gate |
|---|---|---|---|
| **A** | **THE PAINT HAS ALMOST NO GLOSS.** `gloss_compare.py` FAILS at **0.392** of the photograph's spread, bar 0.60; its specular headroom is **0.139** of the photograph's | **3.4 × 10⁶ px²** — the largest thing in the frame | **`gloss_compare.py`, new at rev 57b** |
| **B** | **THE GALLEY AND ROOF-APERTURE INTERIORS ARE UNTEXTURED WHITE BLOCKS**, seen through four openings, dead centre | **7.4 × 10⁵ px²** | none — build one, or accept it and say so |
| **C** | **F15 / A7** — the unlit roofed run between the last light inlet and the tail | 8.2 × 10⁵ px² | none |
| **D** | **F01/F39** — `Senor`, 28.5 % of its ink, in the ARTWORK not the render | 2.7 × 10⁴ px² | `flank_compare.py` |
| **E** | **F43** — what the other 93.5 % of the cream's albedo breakup is (NOT the mottle; rev 57 refuted that). Ablate `dust`/`wear`/`peel` one at a time | large area, subtle amplitude: sd **4.000 DN** over the cream body | `mottle_measure.py` albedo arm, **at `T1_MM_SAMP=16`** |
| **—** | **F08 the badge stroke weight** | **1.4 px²** | **CEILED. Do not.** |

**AND THE DELIVERY FRAME NOW EXISTS.** `out/hq_hero.png` — 3840×2640, 256 spp, SUB=2, ten stitched
strips through `post.py`, made at rev 57b. **It is the baseline you have to beat.**
Re-make it at the end of your revision and put the two side by side.

---

**Read this whole file before you touch anything.** Then `CLAUDE.md` (method only, loads every
session), then `LEDGER_rev57.md` — which is where every number below comes from — then
`OPEN_FINDINGS.md`, and `SURVEY_rev49_photoreal.md` §6.

---

## §0. THE GOAL, AND HOW FAR OFF IT WE ACTUALLY ARE

**CARRIED FORWARD FROM THE REV-55, REV-56 AND REV-57 BRIEFS. It is not mine and it is not to be
dropped — rule 16.**

**PHOTO-REALISTIC PARITY WITH THAT EXACT BUS.** Not "a convincing VW bus" — *that one*, the red
Señor Tacombi combi in the frames on this repo. **Any single measurement off is unacceptable,
per-measurement and not on average.** A model right in ninety places and wrong in one is not 99 %
done, because he will look straight at the one. This paragraph is first because every revision has
drifted toward whatever was measurable that week, and the goal is not "add rows".

**AND HERE IS THE HONEST DISTANCE, MEASURED AT REV 57.** `verify_clone.sh` ends **ALL 244 PASS** and
its own verdict block says what that is worth: **0 FIDELITY, 244 SELF-CONSISTENCY. Not one of those
rows compares the vehicle to a photograph.** *(The rev-57 brief quoted the right ALL-n-PASS
total and then, four words later, gave a self-consistency figure SIX LOWER than it — two numbers for
one line, in one sentence. The wrong figure is DESCRIBED here and deliberately NOT reprinted; see
§2.5. The block read 227 at rev-57 pickup and 240 now.)*

**AND REV 57 CHANGED WHAT THE TWO GATES ARE WORTH. READ THIS BEFORE PLANNING ANYTHING.**

| gate | state at rev 57 |
|---|---|
| `flank_compare.py` | **runs, FAILS 1 of 4.** `Senor` **0.656** against a 0.75 bar. Rev 57 narrowed it: the deficit is in the **artwork alpha and its placement**, not the render — §2.3 |
| `mottle_measure.py` | **runs, and it is NOT measuring the mottle.** Ablating the mottle entirely moves its five ratios by **1.1–2.0 %** against a **7.7–35.0 %** gap. **Rev 56's reading of this gate, and the whole of rev 57's inherited item B, are refuted** — §2.2 |
| `cream_rms.py` | `run()` is the LIVE re-based path |
| the badge | **the first built-against-frame row on either badge exists now** (the ring band, §2.1). The STROKE WEIGHT is **CEILED**: it cannot be recovered from what we hold |
| **`gloss_compare.py`** | **NEW at rev 57b, and the first gate on the surface the eye lands on.** FAILS: the render's paint spreads **0.392** of the photograph's (bar 0.60), specular headroom **0.139**. Exposure-free and resolution-stable, both controlled; **not** a colour comparison, so W6 does not bite |
| `visibility_budget.py` | **NEW at rev 57b.** Not a gate — the RANKING. Converts every finding to pixels of the delivery frame |
| everything else | self-consistency |

**SO PARITY IS MEASURED BY ONE-AND-A-HALF WORKING GATES, NOT TWO.** `flank_compare` is sound.
`mottle_measure` is a real measurement of *something*, but not of what its name says, and no
`MOTTLE_*` constant can move it. **Adding a 241st self-consistency row is still not progress.**

**The frame reads as clay and the cause is the environment, not the shaders** — the surround is a
featureless white cyclorama, so the paint has nothing to reflect. **He was shown that, told the cost,
offered four routes, and ruled "keep studio, fix the model".** Parity is to be won on the MODEL, with
that rig. **Do not re-litigate it.**

### §0.1 THE REFERENCE SET IS COMPLETE, AND IT IS GUARDED FRAME BY FRAME

> *[owner, rev 54]* **"we have all references that we need on repo and I want to make sure that is
> never forgotten."**

**Read that as two instructions and obey both.**

**ONE: WHAT WE HOLD IS WHAT WE GET. STOP PARKING WORK BEHIND A PHOTOGRAPH.** For five revisions the
top job has been logged as *"blocked on a photograph"*. It is not blocked; it is **hard**.
`PHOTOS_WANTED_*` is a wish list, not a gate — carry it (rule 16, and items 1–5 are still not to be
re-asked) but **do not let it license parking an item.** Rev 54 found a live route to the badge
stroke weight in frames already on this repo and did not take it; **rev 55 did not take it; REV 56
DID NOT TAKE IT EITHER, and that is rev 56's clearest omission against this instruction.** Three
revisions running. **TAKE IT** (§3.3). Where a frame genuinely cannot answer, the result is *"it
cannot be recovered from what we hold"* — a real result, stated with its ceiling. Rev 56 produced
two such results honestly: the flank plane's absolute scale (§2.2) and the front rim disc (§2.4).

**TWO: THEY CANNOT BE RE-SHOT, SO THEY ARE CHECKSUMMED INDIVIDUALLY.** **18 rows name them one at a
time**, so a loss says *which*:

* **the RED target bus** — `ref_side.jpg`, `ref_rear34.jpg`, `ref_playa_34.png`,
  `ref_nolita_front34.jpg`, `ref_nolita_front34b.jpg`, `ref_nolita_flank.jpg`,
  `ref_nolita_doorshut.jpg`, `IMG_2073.jpeg`
* **NOT the target, geometry only** — `ref_workshop.jpg` is the **GREEN** vehicle; `bus_model_ref.JPG`
  is a **SCHOOL BUS**, a fidelity bar only. **Paint and artwork do not transfer between vehicles;
  geometry does (rule 11).** Rev 56 leaned on exactly that distinction to accept the owner's
  `lid_rail` ruling off `ref_workshop.jpg` — a structural member, not a colour (§2.5).
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
./bootstrap.sh          # ALL 10 PASS  -- THE BRANCH CHECK IS ROW 9
./verify_clone.sh       # ALL 244 PASS -- and read what its verdict block says
```

**AT PICKUP, REV 57 MEASURED:** rev 56 **was merged, through PR #16** — not the "no PR opened"
its own brief predicted, which is the **third revision running** that the brief has guessed the
merge state and the machine has corrected it. HEAD **0 ahead / 0 behind** `origin/main`, all
**14** remote branches **0 ahead**, `git diff --name-only HEAD...origin/main` **empty** (no
photographs arrived), `bootstrap.sh` **10/10** with row 9 passing, `verify_clone.sh` **227/227**
at pickup.

**AND `fetch --prune` PRINTED `- [deleted] (none) -> origin/claude/bus-model-rev57-yvrlhi`.** That
is the **SEVENTH** deletion in the rev-51…57 series and the **SECOND RUNNING** to hit the branch the
incoming brief named for the CURRENT revision, before that revision had pushed anything. Rev 56
recorded the sixth and said "expect it again". It happened again. **Expect it at rev 58.**

**WHAT YOU WILL MEASURE IS PROBABLY NOT WHAT THIS PARAGRAPH SAYS.** Rev 57 closed with its work
pushed to `claude/bus-model-rev57-yvrlhi` and **no PR opened, because none was asked for** — which
is what rev 55 and rev 56 both said, and both were merged through PRs anyway. **Measure which
shape you are in:**

* **rev 57 was merged** → HEAD 0 ahead / 0 behind, the branch possibly deleted again.
* **rev 57 was NOT merged** → that branch carries commits `main` does not have, and
  **`bootstrap.sh` ROW 9 WILL FAIL** if you are sitting on `main`, naming it. **That failure is the
  handoff, not a defect.** Check the branch out or merge it before anything else and re-run both
  scripts from there. Do not "fix" row 9 by ignoring it.

**Either way, believe the output and not this paragraph.**

> **ROW 9, NOT ROW 10** — confirmed again at rev 57 by reading the machine's own output:
> row 8 clone depth, **row 9 "no branch carries work HEAD does not have"**, row 10 `verify_clone.sh`.

**RE-MEASURE BEFORE YOU FINISH, TOO.** `origin/main` moved mid-revision at rev 51 and rev 55, and
both times **row 9 was the only thing that caught it**. It did **not** move mid-revision at rev 56
or rev 57 (re-checked at close both times: 0 ahead / 0 behind, diff empty). **Run the ahead/behind
loop again before you close, every time.**

---

## §2. WHAT REV 57 DID

### §2.1 ITEM A — THE TOP JOB TAKEN AFTER THREE REVISIONS, AND CLOSED WITH A CEILING

`probe_rev57_geom.py` (Blender; dumps the built badge to `probe_scratch/rev57_glyph.npz`) +
`probe_rev57_badge.py` (pure numpy) run it end to end and paint every window they use.

**WHAT A FRAME MEASURES, OFF THE MESH.** Not `CAP_EMBLEM_WFRAC`. All six strokes read
**w / ring OUTER radius = 0.20455**, agreeing to **0.13 %** — a constant-width bar, which is the
internal control — **= 0.10227 of the outer D, 28.69 mm on a 280.56 mm ring**. Glyph extreme /
ring outer R = **0.840159** against `vw_logo_fit`'s 0.84. **The brief's denominator was SOUND:**
its `0.1986/0.814 × 0.840159` = 0.20498, **0.21 %** off the mesh.

**AND IT DOES NOT CLOSE.** Two estimators, each first calibrated on a synthetic render of the built
glyph blurred to this frame's own PSF (σ 0.689 px) at this frame's own scale:

| estimator | on the SYNTHETIC (truth 0.20455) | on the PHOTOGRAPH |
|---|---|---|
| threshold + distance-transform ridge | 0.20592, **+0.67 %** | 0.23985, **+17 %** |
| level-free edge-gradient fit | width ×1.000, **+0.0 %** | 0.14318, **−30 %** |

**47 points apart and in opposite directions, and each refuted by its own painted window** (rule 8,
twice): a pure ×1.18 width error costs only IoU 0.885, but the threshold mask's best achievable IoU
against the glyph is **0.537 at width ×1.80** — it is eating the proud pressing's **shadow**; and
the edge fit, painted, **locked onto the specular highlight running along each stroke**.

**THE CONTROL THAT MAKES THE CEILING A MEASUREMENT.** Both estimators on the **RING BAND of the same
badge in the same frame**: **0.09209 ± 0.00292** and **0.09280 ± 0.00319**, 25 rays.
**They differ by 0.8 % there against 68 % on the stroke** — so the divergence is the **TARGET**, not
the tools. The probe's verdict line is **computed from those two gaps, not asserted.**

> **THE STROKE WEIGHT CANNOT BE RECOVERED FROM WHAT WE HOLD.** Bracket **0.14318 … 0.23985**
> (**−30 % … +17 %** on the built 0.20455). The built value is **inside** it, so the frame does not
> refute it, but the bracket is **47 points wide** against the **5.09 %** it was meant to see —
> **out by a factor of nine. NO STROKE NUMBER IS PUBLISHED.** F08 is now **CEILED-rev57**.

**AND TWO THINGS ARE DELIVERED THAT WERE NOT ASKED FOR:**

* **THE FIRST BUILT-AGAINST-FRAME ROW ON EITHER BADGE (F38).** band / ring outer D: **BUILT 0.10086**
  off `vw_ring`'s mesh, against **0.09209** and **0.09280** measured here and the record's **0.0874**
  — **+9.5 %** and **+15.4 %**. It is **INSIDE** the adopted 0.093 ± 0.012, at the top of it, while
  three readings of the frame cluster at 0.087–0.093. **Reported, NOT changed:** moving it moves the
  glyph's fit radius with it, through `_BAND_FRAC = 0.028 / 0.140`.
* **THE BRIEF'S CEILING (a) IS RESOLVED, AND IT WAS NEVER THE BLOCKER (F09, CLOSED).** The green
  vehicle's nose badge in this frame is already load-bearing in the shipped model in **two** places:
  the ring band, and the glyph's own fit radius which runs through that same band. A third use would
  have been no worse. **What blocks the stroke weight is the FRAME, not the vehicle.**

**F37, FOUND WHILE DOING IT:** `t1_detail.py` states this badge's ring outer D **twice with
different values** — the band comment's *"outer D 91.729 px"* / *"62.705 px"* against
`vw_logo_fit`'s *"vertical D 91.885 px, horizontal 63.143"*, also carried as SPEC §10.107. Neither
was retracted. Rev 57's own fit is a third reading (**92.728 / 63.299**, resid **0.2345 px**), and
the edge LEVEL moves the vertical D by **1.8 %** across a 0.35–0.65 range — ten times the 0.17 % the
two record values differ by. **Retracted in the source, not only here** (rule 15), and two verifier
rows hold it.

### §2.2 ITEM B — REFUTED. THE GATE DOES NOT MEASURE THE MOTTLE

**The brief said: sweep `MOTTLE_M`, the gate is live. Swept. It does not move.**

| run | 3.0 mm | 5.9 | 11.9 | 23.7 | 35.6 |
|---|---|---|---|---|---|
| **base** — M 0.024, ROUGH 0.62, AMP 0.55 | 0.538 | 1.048 | 1.861 | 2.971 | 3.614 |
| `T1_MOT_M=0.016` | 0.544 | 1.055 | 1.869 | 2.978 | 3.616 |
| `T1_MOT_M=0.004` — **six times finer** | 0.562 | 1.057 | 1.857 | 2.950 | 3.586 |
| `T1_MOT_RGH=0.90` | 0.544 | 1.048 | 1.853 | 2.956 | 3.596 |
| `T1_MOT_AMP=1.10` — **double the amplitude** | 0.573 | 1.109 | 1.932 | 3.045 | 3.693 |
| **`T1_MOT_AMP=0.0` — THE MOTTLE ENTIRELY OFF** | **0.527** | **1.027** | **1.837** | **2.937** | **3.574** |
| **the photograph** | **0.804** | **1.135** | **1.455** | **2.201** | **3.183** |

**The mottle's ENTIRE contribution is 1.1–2.0 %. The gap it was blamed for is 7.7–35.0 %.**
Sweeping `MOTTLE_M` over a **factor of six** closes **3 points of the 33** at 3 mm. And **doubling the
amplitude makes the coarse rows WORSE** — 23.7 mm goes 1.35 → **1.38** — while the fine row reaches
only **0.71** of 1.00. **No mottle constant brings any row to 1.00 and two move away from it.**

**AT PIXEL LEVEL** — the two renders differ only in the mottle, so their difference **is** the
mottle: render breakup **sd 4.000 DN**, the mottle alone **sd 0.2594, p2p 1.603** = **6.5 %**.

> **AND THE DIAGNOSIS WAS INVERTED, SO ACTING ON IT WOULD HAVE MADE THE FRAME WORSE.** Painted:
> `probe_scratch/rev57_alb_off.png` (mottle removed) is a **coarse cloud**;
> `probe_scratch/rev57_alb_diff.png` (the mottle alone) is a **fine speckle**. The mottle **is** the
> fine-scale term. Shrinking `MOTTLE_M` would have shrunk the only fine-scale thing the cream has —
> the opposite of what the 3 mm ratio asks — and could not touch the coarse excess, which is not the
> mottle's. **DO NOT TUNE `MOTTLE_M`.**

**WHY, FROM THE SOURCE.** The mottle reaches base colour by one path: `FADEV_MOTTLE` → the WEATHER
group's `FadeVert` → `ffac` → the **Fac of a HueSaturation** whose entire authority is
`W_FADE_SAT = 0.88` and `W_FADE_VAL = 1.04`, capped at `MOTTLE_AMP` 0.55 — **at most ~2 % of value
on a near-white surface. Measured: 1.603 DN peak-to-peak.** **And its other half is invisible to
this arm BY CONSTRUCTION:** the same `ffac` drives roughness (`faderough = MOTTLE_RGH_K` 0.18, up to
**0.099 of roughness**), and **an ALBEDO pass cannot see roughness at all.** Rev 56 woke the arm
that is blind to the larger half of the thing it is named for.

**AND THE SOURCE ASKED FOR THIS TEST AND NOBODY RAN IT** — `t1_mats.py`, beside `FADEV_CREAM`:
*"its authority over the rendered cream has to be demonstrated, not assumed."* **Demonstrated: 6.5 %.**

**F42 — THE READER THROWS AWAY HALF THE BITS BEHIND A GUARD THAT CANNOT FIRE.**
`shader_solve._render` asks for `color_depth = '16'` and Blender delivers (the PNG's IHDR reads
**bit depth 16, colour type 6**), then reads it with `Image.open(real).convert("RGBA")`, **which
returns uint8**. The next line, `a /= 65535.0 if a.max() > 255.0 else 255.0`, **can never take the
16-bit branch** — the test is on the wrong side of the conversion. Measured with a stdlib decoder
**controlled against PIL** (top byte bit-identical for **100.0000 %** of pixels): patch sd
**3.9999** at 16 bits against **4.0200** through the shipped path, **+0.50 %**. **The aggregate cost
is small and is stated as small.** What it destroys is the mottle: its own sd **0.2594** against an
8-bit quantisation noise floor of **1/√12 = 0.289**. **The gate quantises the thing it is named for
to 0.9 of one step.** **NOT FIXED** — `_render` is a shared path and every consumer would move; the
decoder is written and controlled and the fix is rev 58's.

### §2.3 ITEM C — `Senor` NARROWED TO THE ARTWORK, WITHOUT REDRAWING ANY INK

Gate 1 on `out/r57_side.png`: area **0.9703** PASS, aspect **+1.85 %** PASS, IoU **0.7519** PASS,
`Senor` **0.656** FAIL against 0.75. **Two things off a table that has printed every run and that
nobody had read for this region:**

1. **`Senor` is the ONLY one of nine regions with an area outlier: 901 render px against 1261
   reference px = −28.5 %.** The other eight span **−3.3 % (`swash`) to +5.4 % (`b`)**.
2. **The `tex-only` column — the texture's own alpha on the `SCR` rectangle, no render and no mask
   rule in it — reads 0.689 against the render's 0.656.** `flank_compare.py`'s own sentence is
   *"Where it is as low as the render column, the glyph's problem is the PANEL, not the render."*
   **It is as low.**

**So the deficit is in the ARTWORK ALPHA and its placement on `SCR` — not the render, not the
shader, and not the lockup height, which rev 56 already removed.** F39. This does **not** license
redrawing the script: `senor_trace.py` calls that *"inventing ink the photograph does not show"* and
**A12 is an OWNER RULING, not a do-now.**

### §2.4 RULE 1 — RENDERED, CROPPED, LOOKED AT

`out/r57_hero.png` and `out/r57_side.png`, 1600×1100 at 96 spp, both from this head.
**THE REV-55 "X" LEAD DISSOLVES FOR THE SECOND TIME** (F40, CLOSED): the half-size hero again shows
the nose roundel as a circle with an **X** in it; at full size it is a **legible V over W**
(`probe_scratch/rev57_roundel_x5.png`). The brief's own warning — *"Crops generate leads, not
findings"* — held. **A control that finds nothing is still a result**, and it is recorded so a third
revision does not spend itself on it.

### §2.5 REFUTED AT REV 57 / STILL REFUTED — DO NOT REBUILD THESE

* **"the render's cream mottle is too coarse-grained, and `MOTTLE_M` is the lever"** — **REFUTED,
  §2.2, and inverted: the mottle IS the fine-scale term.**
* **"`mottle_measure.py`'s albedo arm is a live fidelity comparison of the MOTTLE"** — **REFUTED.**
  It is live, and it is not about the mottle: 1.1–2.0 % of it.
* **"`verify_clone.sh`'s verdict block's self-consistency total is six lower than its own
  ALL-n-PASS line"** — **REFUTED**: they are the same number, and it read 227 at pickup. A
  transcription slip in a file whose first section forbids transcription. **The wrong figure is not
  reprinted here** — rev 54, 55, 56 and 57 each re-committed a defect in the very row written to
  explain it, and the rev-57 brief calls that trap STRUCTURAL. Describing beats quoting.
* **"the `Senor` deficit might be the render"** — **REFUTED**, §2.3. It is the artwork.
* **"`ref_workshop.jpg` being the GREEN vehicle is what blocks the badge"** — **REFUTED**, §2.1.
  The frame blocks it; the vehicle never did.
* **"the nose roundel reads as an X"** — **REFUTED for the second time**, §2.4.
* **"`shader_solve._render` handles 16-bit"** — **REFUTED**, §2.2, F42.
* Everything rev 50–56 refuted — all still refuted, including: the 2.3 % instrument conflict;
  "for an oblique view the horizontal scale must be the smaller"; `flank_kv`'s quadratic carry law;
  "the render's flank lockup is short in height"; "the re-base of `cream_rms` is open";
  "`lid_rail`'s width cannot be established"; there is no cream either side of the flank ink; the
  flank ink is NOT painted light; height/aspect/area are not three witnesses; the true normal is NOT
  the fix for the chip gate; the nose roundel's V arms do not stop short; the cap's dome depth; the
  m5 "convention conflict"; `LID_W ≤ 1.2797 m`; A7's aft wall; `gal_end_f` widened to `REAR_W/2`.
* **§2b of the rev-52 brief — HIS SETTLED RULINGS — IS UNCHANGED AND STILL BINDING.** W6 (keep the
  studio rig; **a G/R shortfall on any surface is NOT a paint error**); the roof strips' 0.3 m
  retired; the wipers withdrawn entire, commented not deleted; the lower bay SHUT; the RED bus is
  the target and **paint and artwork do not transfer between vehicles**; the tail board IS on the
  vehicle; the marks above the burst are STARS. **Do not re-open or re-ask any of them.**
  `playa_env.py` is not on the table. **And rev 54's ruling stands: "Keep studio, fix the model".**

### §2.6 REV 57 ASKED HIM NOTHING

Every item it touched was answerable from the repository, which is what §0.1 says to do. **Nothing
was put to him, and nothing is inherited as unasked.** If rev 58 wants a question, F38 (the ring
band at the top of its adopted range) and F39 (the `Senor` artwork) are the two worth his time —
**decide, do not inherit.**

### §2.7 THIS FILE WAS AUDITED AGAINST THE MACHINE, TWICE, AND THE SWEEP IS NOW A SCRIPT

Rule 17 (*is what the file says true?*) and rule 15's adversary (*what would make it false?*) are
**different instruments** and both were run.

**AND THE SWEEP IS NO LONGER THROWN AWAY.** Rev 54, 55 and 56 each wrote it by hand, ran it, and
discarded it — and the next revision re-committed the same defect, three revisions running for the
directory-less path alone. It is now **`audit_brief.py`**, committed, and it asks the mechanical
questions every time: does every path resolve; does every `T1_*` **read the environment** rather
than merely appear in a comment; does every script named exist; is this file byte-identical to
`PASTE_INTO_CLAUDE_CODE.txt`; does it state `verify_clone.sh`'s own row count; do `README.md` and
`START_HERE.md` name it; and the three **self-referential traps** that have actually fired here.
**It does not check that the numbers are true — only the revision that measured them can, which is
why the ledger exists and why rule 17 says RECOMPUTE.**

**WHAT THE TWO PASSES FOUND ON THIS FILE AND ITS LEDGER**

| what the draft said | what the machine says |
|---|---|
| the sweep's FIRST run reported **eleven unresolved paths** | **nine of them were not paths.** `REAR_W/2`, `0.1986/0.814`, `origin/main`, `git`, `a`, and the TEMPLATE names `LEDGER_rev<N>.md` and `HANDOFF_rev*.md`. **The defect was in the SWEEP, not the brief** — and a sweep that cries wolf on a quotient gets ignored, which is worse than not having one. It now requires a known extension and rejects globs and placeholders. **51 paths checked, 0 unresolved** |
| the sweep reported the row count as *"script says None"* | **`verify_clone.sh` prints `ALL n PASS` only on a clean tree**; on a dirty one it prints `n PASSED, m FAILED` and the regex found nothing. It looked exactly like a brief defect and was an instrument defect. **Both forms are read now.** *Two of the sweep's own three failures on its first run were its own* |
| the region spread in the ledger read *"the other eight sit within ±5 %"* | **`b` is +5.4 %.** Recomputed from the two px columns rather than eyeballed; the ledger now reads **−3.3 % (`swash`) to +5.4 % (`b`)** |
| §0 gave the self-consistency total as a figure **six lower** than the `ALL n PASS` it quoted four words earlier | that was inherited from the rev-57 brief, where it was already wrong. **Corrected — and DESCRIBED rather than reprinted**, because rev 54, 55, 56 and 57 each re-committed a defect inside the row written to explain it |
| a bare **`243`** survived on that same line | the row count moved **three times** during this revision (238 → 239 → 240, each fix adding a passing row), and a `sed` keyed on `ALL 243 PASS` did not touch `243 now`. **§10.3 is right and it bit again.** Write the count LAST and grep for the bare number afterwards, not just the phrase |
| the full-size roundel tile — the EVIDENCE for §2.4 — was cited by a path that **resolves here and not on a clone** | **`.gitignore` line 9 excludes `rev*_hero*.png`.** The sweep checked `os.path.exists` on the machine that WROTE the brief, which is the one place the path is guaranteed to work and the one place the brief is never read. **A sweep over the working tree cannot see a `.gitignore`.** The tile is renamed `probe_scratch/rev57_roundel_x5.png` and force-added, and **`audit_brief.py` now checks `git ls-files`, not the filesystem** — 52 paths, 0 unresolved, tracked |
| `README.md` and `START_HERE.md` still said rev 57 | both **FAILED** their rows. Updated |

**WHAT THE ADVERSARY TRIED, AND IT BROKE NOTHING — ten questions, written as a script and RUN, so
this list is what executed rather than what was drafted:**

* *"Does turning the mottle off really move the gate by only 1.1–2.0 %?"* — **recomputed from the
  logs, not the prose: 2.0 / 2.0 / 1.3 / 1.1 / 1.1 %.**
* *"Does doubling the amplitude really move the coarse row the WRONG way?"* — **yes**, 23.7 mm goes
  2.971 → **3.045**.
* *"Is the 0.20455 in this brief the MESH's number?"* — recomputed off the dump: **0.20455**, ring
  outer D **0.28056 m**.
* *"Was a bar moved to make anything pass?"* — the diff of `flank_compare.py` and `verify.py` is
  **0 lines**. No `*_TOL`, no `REGION_IOU_FRAC`.
* *"Did rev 57 change any CODE, or only comments?"* — **0 non-comment lines** across the three
  edited source files. **Rev 57 changed no geometry, no shader value and no threshold.**
* *"Does the badge probe still refuse?"* — it prints `NO STROKE NUMBER IS PUBLISHED`, and its band
  control's verdict line is **derived**, not a constant string.
* *"Is the band control on the MAJOR axis?"* — 0.09209 ± 0.00292, the tight spread.
* *"Is anything claimed done that is not?"* — **F08 is CEILED, not closed**, and `LEDGER_rev57.md`
  §5 lists every omission on purpose.
* *"Does the brief reproduce a defect it only means to describe?"* — **IT DID, and this pass caught
  it.** Fixed as above. **This is the one thing either pass broke.**
* *"Do the gates still run from this head?"* — gate 1 runs and fails **exactly one** row,
  `Senor` 0.656.

**AND THE MECHANICAL SWEEP IS COMMITTED NOW.** `audit_brief.py` — 9 checks, **0 failed** on this
file. Rev 58 should EXTEND it rather than rewrite it, and add the question its own revision needed.

**THIS FILE MUST STAY BYTE-IDENTICAL TO `PASTE_INTO_CLAUDE_CODE.txt`.** `CLAUDE.md` imports that
file into every session as the entry procedure. **WHEN YOU WRITE THE REV-59 BRIEF, `cp` IT OVER
`PASTE_INTO_CLAUDE_CODE.txt` IN THE SAME COMMIT, OR `verify_clone.sh` FAILS AND NAMES THE ROW.**

---

## §3. THE WORK LIST FOR REV 58

### §3.0 START HERE — THE ORDER, AND WHY IT CHANGED

**Rev 57b audited this handoff for efficiency and found the ranking rule was the defect.** Full
evidence in `AUDIT_rev57_efficiency.md`; the short form is in §0.0 and the table is a script.
**He ruled "keep studio, fix the model", so this is still a MODEL revision** — and §0.0's order is
what "fix the model" means once the work is ranked by what shows.

**THE ONE THING TO INTERNALISE:** the method in `CLAUDE.md` is not in question and none of it is
relaxed. Every rule was earned. What changed is *which item the method gets pointed at*. Rigour
applied to a 1.4 px² question is still 1.4 px².

**A WARNING ABOUT LOOKING, NOW TWICE EARNED.** Rev 55 called the nose roundel an "X" off a
half-size hero; rev 57 looked at full size and it is a clean V over W. **Crops generate leads, not
findings.** Take the lead, paint the window, then believe the number.

**AND A WARNING ABOUT GATES — rule 36, the most expensive lesson of rev 57.**
**BEFORE YOU TUNE ANYTHING AGAINST A GATE, ABLATE THE THING YOU ARE ABOUT TO TUNE AND CHECK THE
GATE MOVES.** Rev 56 woke a gate, read it, and named the constant to turn. Rev 57 turned it over a
factor of six and the gate did not move, because the gate could not see it. **One five-minute
ablation would have saved a revision.**

**AND A THIRD, NEW AT REV 57b — DO NOT LET THE MACHINE IDLE.** Blender is CPU-bound and cannot be
fanned out, so wall-clock is the binding constraint on this project, not tokens. Launch the render
you will need before you read; run ablations at `T1_MM_SAMP=16` (rev 56 measured the statistic
stable across 16/32/48 and the gate has run at 64 ever since — that alone cost 30 minutes of the
rev-57 sweep); and analyse in the foreground while Blender runs in the background.

### §3.1 ITEM A IN DETAIL — THE GLOSS, AND WHERE IT LIVES IN THE SOURCE

**Rev 57b found the mechanism by reading, and it is two constants.** `body_paint()` in
`t1_mats.py` sets, for `T1_paint` — the material that carries **the whole two-tone body, red and
cream both**:

```
bsdf.inputs["Roughness"].default_value      = 0.420
bsdf.inputs["Specular IOR Level"]           = 0.50   (T1_SPEC)
bsdf.inputs["Coat Weight"].default_value    = 0.02
bsdf.inputs["Coat Roughness"].default_value = 0.300
```

**`Coat Weight` 0.02 is, to two figures, NO CLEARCOAT.** Automotive paint is a clearcoat at weight
~1.0 over a base, with coat roughness ~0.03. And a base roughness of **0.420** is semi-matte
plastic; car paint sits at 0.05–0.15. `Specular IOR Level` is already right (0.50 → F0 ≈ 0.04, the
physical dielectric value, fixed at rev 8).

**SO ITEM A IS A THREE-RUN EXPERIMENT, NOT A REVISION'S WORK** — provided you obey rule 36 and
ablate first:

1. baseline `gloss_compare.py` on a fresh `hero` — **0.392 today**;
2. `Coat Weight` 0.02 → 1.0, `Coat Roughness` 0.300 → 0.03 — the clearcoat alone;
3. and then base `Roughness` 0.420 → ~0.25.

**AND THE TRAP, WHICH THE SOURCE ITSELF SETS.** Four lines above those constants:
*"the red measured sat 0.37 against the reference's 0.82 and read salmon. **Chalky finish restores
the chroma.**"* **The high roughness is load-bearing for the COLOUR.** Lowering it may re-break the
red's saturation — and **colour is the owner's call under W6, gloss is not.** So measure BOTH on
every run and report both: `gloss_compare.py` for the gloss and `flank_compare.py`'s own G/R block
for the chroma. **If they trade against each other, that is a finding and a question for him, not a
number to split the difference on.**

**THE CEILING, AND IT IS REAL.** The rig's sources are large-area softboxes — `top` is 13.0 × 8.5 m.
Even a mirror-smooth paint under a 13 m source gives a **broad, soft** highlight, where the
photograph's market-hall lamps give small intense ones. **So `gloss_compare.py` will not reach 1.000
under this rig and it is not supposed to.** The owner's *"keep studio, fix the model"* stands.
What the gate can tell you is how much of the gap is the MODEL's, and it can tell you that in
three runs. **Find out where the ceiling is and report it with the number, rather than tuning
toward 1.0.**

**F47, found while reading:** the `WEATHER` header comment still says *"nearly invisible at
Specular IOR Level 0.21 / Roughness 0.42"*. **`Specular IOR Level` has been 0.50 since rev 8** —
its own fix-note four lines from the live assignment says so. The comment's conclusion (the body is
diffuse-dominated) survives at roughness 0.42; its stated premise is stale by nine revisions.

### §3.1 ITEM E IN DETAIL — THE MOTTLE GATE, AND WHAT REV 57 HANDS YOU

`mottle_measure.py`'s albedo arm is a **working instrument with a known meaning**: it measures the
band-passed rms of the render's cream albedo against `ref_rear34.jpg`'s, and **1.1–2.0 % of what it
sees is the mottle.** The patch is confirmed **all cream** (R/G = 1.00, no red), so the two-tone
boundary is **REFUTED** as the cause — checked before it produced a number.

The remaining candidates are the paint's other spatial terms, all applied in the same
`apply_weather(M["paint"], dust=1.0, wear=…, fade=1.0, peel=1.0, …)` call. **Ablate them one at a
time** exactly as rev 57 ablated the mottle: two renders that differ in one term, subtract, and the
difference **is** that term with nothing modelled. `out/mottle_alb*.png` is keyed by `MOTTLE_AMP`,
so give each ablation its own filename or it will overwrite the last one.

**AND USE THE 16-BIT DECODER (F42)** if the term you are chasing is small: 8 bits put the mottle
below one quantisation step, and it will do the same to anything else of that size.

### §3.2 THE mm AXIS — STILL NOT ATTEMPTED, TWO REVISIONS RUNNING

`PXM_REF = 337.0` px/m is a **bracket** (330–344), not a measurement, and it sets the mm axis of
every figure in §2.2. **Rev 56's §2.1 sqrt-law algebra applies to `ref_rear34.jpg` too.** Not
attempted at rev 56, not at rev 57. *(Rev 55's correction stands: `depth_correct()` is defined
NOWHERE in this repo.)* **Note what it does and does not affect:** rev 57's ablation results are
render-against-render and do **not** depend on it; anything comparing the render to the photograph
in millimetres does.

### §3.3 THE BADGE — CEILED, NOT OPEN. DO NOT RE-RUN IT BLIND

**F08 is CEILED-rev57 and the route is EXHAUSTED for this photo set.** §2.1 has the bracket and the
two refuted windows. **Do not re-attempt the stroke weight on `ref_workshop.jpg` without a new
idea** — and "a better threshold" is not one; both threshold and gradient were tried, calibrated,
painted and refuted, and the ring-band control shows the fault is the target.

**WHAT WOULD ACTUALLY MOVE IT**, in order of cost: a frame of one hubcap square on and close
(`PHOTOS_WANTED_rev52.md` item 7, still the only outstanding ask); or an estimator that models the
**proud chrome pressing** — highlight, cast shadow and rounded edge together — rather than
thresholding it, which is a revision's work and may still fail. **DO NOT REBUILD:** the badge's
REACH is settled (rev 54, 720-ray profile, all six stroke ends on the band).

**F38 IS THE LIVE PART OF THE BADGE NOW:** the built ring band is at the top of its adopted range
(**0.10086** against three frame readings at 0.087–0.093). It is inside the record's own ±0.012 and
was deliberately not changed, because moving it moves the glyph's fit radius with it. **That is a
decision to take, not a measurement to repeat.**

### §3.4 FINISH A9, AND THE THREE HOLES REV 52 LEFT OPEN

**A9: two of four parts done; the galley is still ~103 mm too far aft. PROVENANCE, GRADED: the
per-feature deltas are INHERITED from the rev-52 brief and have NOT been re-measured at rev 52, 53,
54, 55, 56 or 57.** The offset is **NOT rigid** (−0.09574 at hook u=0.13 to −0.11035 at
`gal_appliance` u=0.80, so one additive constant leaves ±7.3 mm). Re-derive each X from `BAYS`, the
way `gal_rail` now is. *(The survey's ~106 mm and its +0.096..+0.113 range are both wrong.)*

**THE THREE HOLES.** F11–F13 were re-measured at rev 56 and reproduce exactly. **F14's 260.0 mm and
20.0 mm sight lines are rev 52's and have NOT been re-measured since — five revisions. §8 says an
INHERITED row that survives three more revisions should be re-measured or downgraded; this one is
past that.**
* `gal_end_f` sees past by **260.0 mm** on the show side and 20.0 mm on the off side. Needs its own
  sight line established first — **do not inherit `REAR_W/2`** (rule 34: that figure belongs to the
  rear window, which is not what looks at it).
* The **sixth hook at X −0.907 lies 51.25 mm beyond `BAYS[2]`'s own aft edge (−0.855750)**; the six
  hook stations' span centre is **−0.7050** against the rail's **−0.5980** — **107.0 mm**. **They
  disagree and one is wrong.**
* A7's real defect: `roof_cutters()`'s aft edge is `LID_X1`, which is **not** greppable as
  `LID_X1 = -1.0700` — the source line is `LID_X0, LID_X1 = 0.9640, -1.0700` in `t1_shell.py`, so
  **803 mm of roofed body** sits between the last light inlet and the tail skin. Unbuilt. A7 is
  **ILLUMINATION, not dressing.**

### §3.5 A13 / A16 / A12, A11's SECTION, A14, AND THE CHEAP COLOUR ITEM

**A13 / A16 / A12** — the isolated star built BELOW the burst where both red frames put it above;
every flank rosette drawn at the diameter of its **gold core**; *A12 is an OWNER RULING, not a
do-now* — `senor_trace.py` calls the remedy *"inventing ink the photograph does not show"*.
**Rev 57's F39 does not change that**: it says where `Senor`'s deficit lives, not that it may be
redrawn.

**A11's SECTION, A14** — a chrome lever lying in a dish **pressed into** the skin against a 12 mm
**proud** prism.

**A CHEAP UNBLOCKED ITEM, STILL NOT DONE AFTER SIX REVISIONS:** `SPEC` §8's colour locks are all
graded **M** = *"measured by me from `ref_source.jpeg`"* — a 246×197 thumbnail the record itself
calls retired. They can be re-derived on `ref_playa_34.png` at **4× the area** with no new
photograph. **Report the re-derived values; do not change the constants without his ruling** — W6
makes colour his call. *(And `ref_playa_34.png` is byte-identical to `IMG_3842.png`; a duplicate is
not corroboration — rule 11.)* The render's flank red reads **G/R 0.462 against the photograph's
0.114**, and the split between paint and illuminant **cannot be recovered from what we hold**.

### §3.6 THE PROCESS ROWS, STILL OPEN

`OPEN_FINDINGS.md` is the register — see §8; the standing-instructions carrier deleted at rev 44,
which took the **die-cut sticker — the project's original deliverable** — with it, **still open and
carried as F18**; SPEC §0.2's two rev-4 corrections later refuted; rev 48's refuted *"B stays
open"* still live in `build.py` and, **split across two lines so a flat grep misses it**, in
`t1_shell.py`; the tail board still has **zero rows in either verifier**.

### §3.7 THE HABITS THAT PAID AT REV 57

**ABLATE BEFORE YOU TUNE.** §3.0's warning. It is the whole of rev 57's item B.

**CALIBRATE THE ESTIMATOR ON A SYNTHETIC WHERE THE ANSWER IS KNOWN — then it can refuse.** Both
badge estimators recovered the built glyph to +0.67 % and +0.0 % from a synthetic blurred to the
frame's own PSF. That is the only reason their 47-point disagreement on the photograph could be
read as *the target is hard* rather than *my code is wrong*.

**GIVE A CONTROL A FEATURE WITH A KNOWN ANSWER.** The ring band turned "two instruments disagree"
into "they agree to 0.8 % on the band and 68 % apart on the stroke, so it is the target".

**MAKE THE VERDICT DERIVED.** The band control's first version printed a **constant** conclusion
that **contradicted the two numbers above it**. A verifier row now forbids the measured values
appearing as literals in the file that measures them.

**AND PAINT THE WINDOW — THE PROBE, NOT THE ANALYST, SHOULD PAINT IT.** Rev 57's first band control
ran its rays down the **MINOR** axis and read 0.109/0.131 at sd 0.025 instead of 0.092/0.093 at
sd 0.003. Both numbers were plausible. `probe_rev57_badge.py` now paints every window it uses, so
the next reader does not have to take the caption's word for it.

## §4. WHAT WAS ASKED OF HIM — A CARRIER, NOT A LIST OF BLOCKERS

> **READ §0.1 FIRST.** At rev 54 he ruled that **the reference set on the repo is complete**. This
> section is kept in full because `CLAUDE.md` rule 16 forbids dropping a carrier, and because it
> records what was asked and what was refused — which is why items 1–5 must never be re-asked.
> **But it is no longer a licence to park work.** Nothing below blocks an item; it only says what a
> new frame would have made easier. Work every item from what we hold, or close it with
> *"it cannot be recovered from what we hold"* and its ceiling.

**`PHOTOS_WANTED_rev52.md` is the carrier for item 7 (ONE HUBCAP, SQUARE ON AND CLOSE)**. Items
**1–5** keep their full text in `PHOTOS_WANTED_rev49.md`: the tail board's footing; the decal darker;
the nose square on; a raking-light frame of the louvres (**ONE item — the pressing depth**; the
"block length, station and V swage" expansion is a proposal, not the record); the off side, any
frame. **He has said 1–5 are not possible now. DO NOT RE-ASK THEM.** Item 6 (an obliquely-seen
wheel) was **DISSOLVED at rev 51** — struck, not outstanding.

**CARRIED FROM REV 53, still no carrier outside these briefs:** a frame showing the cream **where it
IS chipped** — any close frame of a worn edge. **Rev 54 lowered its urgency and rev 55 lowered it
again**: the band is 0.27 px at every scale this project ships, AND the gate that would place those
chips on the red is not built. Only worth asking if a close counter view is ever wanted.

**ANSWERED AT REV 56 AND NOT TO BE RE-ASKED:** `lid_rail`'s width — *"narrow lip, ~as wide as it is
tall"*. That was the only question rev 56 put to him.

**REV 57 PUT HIM NOTHING, AND NOTHING IS INHERITED AS UNASKED.** Every item it touched was
answerable from the repository, which is what §0.1 says to do. **Two things are now worth his time
and neither has been asked:** **F38** — the built nose ring band sits at the top of its adopted
range (0.10086 against three frame readings at 0.087–0.093), and moving it moves the glyph's fit
radius with it; and **F39** — `Senor`'s ink deficit is in the artwork, which A12 makes his call.
**Decide whether to ask. Do not simply carry them.**

---

## §5. THE RULES — `CLAUDE.md` CARRIES THE METHOD, NOT THE NUMBERED CANON

The canon (rules 1–33) is printed in `NEXT_CONTEXT_PROMPT_rev50.md` §11. **Rules 34 and 35 live only
in the rev-51…56 briefs and `LEDGER_rev50.md` §0, so they are carried here too — that is
`CLAUDE.md`'s own rule 16 firing on this file:**

> **34. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Before relying on any
> *"the record requires X"*, check which object the sentence is about — and check the cited line
> exists. **Rev 52 applied this deliberately**: `gal_end_f` was left alone because `REAR_W/2`
> belongs to the rear window. **Rev 54 applied it to a photograph**: item 7's four closed routes are
> all about the HUBCAP badge and none closes the NOSE badge. **Rev 55 applied it to a function**:
> `cream_rms.py` cited `depth_correct()`, which is defined NOWHERE in this repo. **Rev 56 applied it
> to a CAMERA**: `flank_compare.py`'s header attributes a recovered camera position to
> `ref_side.jpg` that `studio.py` attributes to the PLAYA frame — the same three numbers in two
> places about two photographs. **NOT resolved at rev 56; nothing rev 56 published depends on it,
> because the anisotropy was measured off the wheel rather than predicted from a pose. Check it
> before any future work leans on that camera.**

> **35. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Guards that identify a part's foot or
> free edge by `min(y)` are only right while the part leans one way. Ask the geometry.
> **Rev 53 broke this and was caught by it**; **rev 54 broke it again** — a global `min(z)` for a
> fold that SLOPES, wrong by 25 mm; **rev 55 broke it a third time** — a TYPED crop window for the
> counter control that caught 418 px of it. **Rev 56 broke its FRAME-relative cousin** — a probe
> comparing a DROPPED vertex against the AUTHORED `roof_z` and reporting a rail 43.7 mm below a roof
> it sits 21.3 mm above (§2.5).

> **36. A GATE ONLY COUNTS FOR WHAT IT CAN SEE — ABLATE THE THING YOU ARE ABOUT TO TUNE, FIRST.**
> **Earned at rev 57 and it cost the whole of that revision's item B.** Rev 56 woke
> `mottle_measure.py`, read a real spectrum off it and named the constant to turn. Rev 57 turned it
> over a factor of six and the gate did not move — because the mottle is **1.1–2.0 %** of what that
> gate measures, and its larger half (roughness) is invisible to an ALBEDO pass **by construction**.
> A live gate, a real number, a plausible diagnosis, and the lever was not connected to it.
> **One five-minute ablation would have caught it.** Before tuning ANY constant against ANY gate,
> set that constant to zero and check the gate moves. This is rule 3 — *a control is finished when
> you have watched it fail* — pointed at the instrument instead of at the guard.

> **Rule 29.3:** no finding is attributed to a cause until a control separates it. **Rule 29:** a
> retirement inherits the object it was made about. **Rule 15:** a retraction that lands in a ledger
> and not in the source is half a retraction — **rev 56's withdrawal of "one of the two instruments
> is 2.3 % out" is in `flank_compare.py`'s own printed block and in `flank_kv.__doc__`, and four
> rows hold it there.**

---

---

## §6. THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build  T1_SUB=1 ~20 s     render 1600x1100 96 spp ~4.5 min PER VIEW
mottle_measure.py (albedo arm, 64 spp) ~4.8 min PER RUN -- budget ablations in fives
```

```bash
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=side T1_PFX=r58 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py
T1_PREVIEW=hero   ...                                        # LOOK at it, at FULL size
T1_PREVIEW=hero34r ...                                       # the REAR 3/4 -- A7 lives here
T1_SUB=2 /tmp/blender/blender -b -P audit.py                 # rewrites STATE.md -- COMMIT FIRST
python3 lid_gen.py                                           # regenerates tex/lidmural.png
python3 flank_compare.py out/r58_side.png /tmp/fc.png        # GATE 1.  FAILS 1 of 4 today.
python3 gloss_compare.py out/r58_hero.png                    # GATE 3.  FAILS at 0.392 today.
python3 visibility_budget.py 3840                            # THE RANKING.  Run it before choosing.
T1_SUB=1 T1_GL_COATW=1.0 T1_GL_COATR=0.03 T1_GL_PFX=g1 \
  /tmp/blender/blender -b -P probe_rev58_gloss.py            # ITEM A's ablation, changes NO source
python3 cream_rms.py                                         # the LIVE photograph-side cream
T1_SUB=1 T1_MM_ALBEDO=1 T1_MM_SAMP=16 /tmp/blender/blender -b -P mottle_measure.py  # GATE 2
#   ^ 16, NOT the default 64.  Rev 56 measured this statistic stable across
#     16/32/48 and it has run at 64 ever since: 4.8 min a run against 1.5.
#     Rev 57's nine-run sweep paid 30 minutes for nothing.
T1_SUB=1 /tmp/blender/blender -b -P probe_rev57_geom.py      # dumps the built badge -> npz
python3 probe_rev57_badge.py                                 # ITEM A, end to end, paints its windows
python3 audit_brief.py                                       # rule 17's MECHANICAL half -- NEW at rev 57
python3 probe_rev56_kv.py                                    # the vertical scale, both halves
python3 probe_rev53_chip.py                                  # the chip measurement, all six arms
T1_SUB=1 T1_AOVSAMP=64  /tmp/blender/blender -b -P probe_rev54_aov.py    # the EDGE AOV + sweep
T1_SUB=1 T1_LOOKSAMP=192 /tmp/blender/blender -b -P probe_rev54_look.py  # the scale ladder
/tmp/blender/blender -b -P probe_rev54_wfrac.py              # the badge denominator, calibrated
T1_SUB=1 /tmp/blender/blender -b -P probe_rev54_badge.py     # the badge off the built mesh
T1_SUB=1 T1_TNSAMP=64 /tmp/blender/blender -b -P probe_rev55_truenorm.py  # RUN IT AT SUB=1 AND 2
```

**`out/` IS NOT TRACKED and starts empty. Render before quoting any probe that reads a frame.**
**A backgrounded runner's exit code is the WRAPPER'S, not Blender's — grep the log for `Saved:`.**
**`probe_rev54_aov.py` and `probe_rev55_truenorm.py` write EXR into `probe_scratch/` — delete them
before committing and keep the PNGs.**
**`mottle_measure.py`'s BEAUTY arm REFUSES (100 % clipped). Run it with `T1_MM_ALBEDO=1` — and read
§2.2 before you believe the ALBEDO arm is about the mottle, because it is not.**
**`mottle_measure.py` names its output by `MOTTLE_AMP`, so two runs that differ in `MOTTLE_M`
OVERWRITE EACH OTHER'S PNG. Rename per ablation or you will diff a file against itself.**
**EVERY MEASUREMENT THROUGH `shader_solve._render` IS 8-BIT (F42), whatever `color_depth` says.**

**THE DELIVERY FRAME — the recipe, first run at rev 57b.** Nobody had ever
rendered this model at delivery quality before; every figure in every ledger comes off 1600×1100.
Ten strips because `studio.render_set`'s own comment says a long hero gets reaped:

```bash
for i in $(seq 0 9); do
  lo=$(python3 -c "print('%.4f'%($i/10))"); hi=$(python3 -c "print('%.4f'%(($i+1)/10))")
  T1_SUB=2 T1_PREVIEW=hero T1_PFX=hq$i T1_RX=3840 T1_RY=2640 T1_SAMP=256 \
    T1_BORDER="$lo,$hi" /tmp/blender/blender -b -P build.py
done
python3 stitch.py out/hq_hero_raw.png 0.0000,0.1000=out/hq0_hero.png ... # all ten
python3 post.py out/hq_hero_raw.png out/hq_hero.png                      # optics LAST, never per strip
```

**Strips vary with content: 11.4 min for the ground strip, 18.4 for the first body strip. 65 s of every strip is rebuilding the scene — 10.8 min across ten strips is pure repeat.**
Rendering every strip inside ONE Blender session would take ~10 % off; nobody has written that yet
and it is worth writing before the next delivery frame.

**ABLATIONS — every one exists to WATCH A GUARD FAIL, and at rev 57 one of them was used to watch a
GATE fail to move, which is the same idea pointed at an instrument.**
**USED AT REV 57:** **`T1_MOT_AMP=0.0`** (the mottle ENTIRELY off — the gate moves 1.1–2.0 %, which
is the whole of §2.2), **`T1_MOT_M`**, **`T1_MOT_RGH`**, **`T1_MOT_DET`** (all four read the
environment in `t1_mats.py`; two verifier rows hold `T1_MOT_M` and `T1_MOT_AMP` there).
Carried: `T1_FC_KVQUAD` (restores `flank_kv`'s old QUADRATIC carry law; the aspect row goes back to
+5.23 % and FAILS), `T1_RAILFLAT` (restores `lid_rail`'s `xa == xb`; VERIFY goes 0 fail -> 3 fail),
`T1_CR_LEGACY` (runs `cream_rms`'s dead `ref_side.jpg` path), `T1_FC_INKGAIN` (at +30 the ink/ground
R ratio moves 0.867 -> 1.022 and the verdict flips), `T1_FC_ZSTRETCH` (the IoU parabola peaks at
1.0398 — rev 56 explains why), **`T1_TRUENORM`** (swaps the chip gate onto the true normal — **a
DEMONSTRATION, not a fix; do not make it the default**), `T1_PTWEAR=1`, `T1_EDGERAD`,
`T1_MM_ALBEDO`, `T1_SOLVE_NODENOISE`, `T1_TARNCONTAM=1`, `T1_RAILSTALE=1`, `T1_ENDSHORT=1`,
`T1_CAPSINK=1`, `T1_LIDDEG=104`, `T1_BAYSTALE=1`, `T1_LAMPSINK=1`, `T1_LIDASPECT=1.2`,
`T1_HANDLEHI=1`, `T1_BAREMAT=1`, `T1_TBFOOT=1`, `T1_BAYPROUD=1`, `T1_NOBEVEL=1`,
`T1_BEVEL_SAMPLES`, `T1_FC_OLDDATUM=1`.

## §7. THE STANDARD, IN HIS WORDS

We are recreating a photorealistic version of **that exact bus**, and **any single measurement off is
unacceptable** — per-measurement, not on average. A model right in ninety places and wrong in one is
not 99 % done, because he will look straight at the one.

`bus_model_ref.JPG` is a **SCHOOL BUS** and is **NOT the vehicle** — a FIDELITY BAR only. Use
`ref_workshop.jpg` the same way, and remember it has **no headlamps and no hubcaps fitted** and is
the **GREEN** vehicle (§4).

**Ground in the reference, build, adversarially audit, iterate.** Never build before grounding. Never
call it done off self-review. Report the measurement **with its ceiling**, never a self-assigned
score. Do not say anything is ready — say what is fixed, what is still wrong, and what you measured.

**RENDER IT, CROP IT, AND LOOK AT IT, before and after every change.** Every defect this project has
shipped passed `VERIFY: 0 fail, 0 warn` and was found by looking at a crop. **Rev 56's whole item-B
result turned on this: the ratios said 0.00 five times, and only LOOKING at the frame said the patch
was pure white.**

**When you need something from him, ask as MULTIPLE CHOICE with the reference material attached — one
crop, one mark, one sentence — and ASK IT WITH THE QUESTION TOOL.** He has never stood in the bus: do
not ask what the real vehicle looks like, ask what a PHOTOGRAPH shows. **Rev 56 asked him exactly one
thing — `lid_rail`'s width — and it closed a defect that had been exempt for four revisions.**

**`git rev-list --count origin/main..HEAD` before you start and again before you finish. And
`git diff --name-only HEAD...origin/main` — that is where his photographs arrive. EVERY session.**

---

---

## §8. THE OPEN-FINDINGS REGISTER — `OPEN_FINDINGS.md`

**A register existed once and was ABANDONED AT REV 45 WITH 21 ROWS, and nobody noticed for eleven
revisions.** The standing-instructions carrier went the same way at rev 44 and took the project's
original deliverable with it. Rev 56 reinstated it; rev 57 carried it to **43 rows**.

**IT IS A CARRIER (rule 16). Rows leave it only by being CLOSED with the measurement that closed
them, or RETIRED with the ruling that retired them. Never by being dropped.** A verifier row now
checks the IDs run **unbroken from F01**, so a dropped row fails the build rather than going
unnoticed for eleven revisions.

**THE POINT OF THE FILE IS THE PROVENANCE GRADE, NOT THE LIST.** Every row is marked
`MEASURED-revN` / `RECOMPUTED-revN` / `INHERITED-revN` / `RULED-revN` / `CEILED`. This project's
recurring failure is not losing numbers — it is **re-quoting inherited ones as though they had been
measured**. An `INHERITED` row is a claim. Treat it as one.

**GRADE DECAY IS ITSELF A FINDING.** An `INHERITED` row that survives three more revisions without
being re-measured should be re-measured or downgraded — not quietly re-quoted a fourth time.

**REV 57 MOVED SEVEN ROWS AND ADDED SEVEN.** Closed: **F09** (the green-vehicle ceiling — it was
never the blocker) and **F40** (the "X" roundel, dissolved twice). Re-graded: **F08 → CEILED**,
**F03 → REFUTED as a mottle finding**, **F04** restated, **F05 promoted to blocking**, **F01**
narrowed. Added: **F37** (two ring-D values in one file), **F38** (the built ring band vs the
frame — the first such row on either badge), **F39** (`Senor` is the artwork), **F41** (the albedo
arm is blind to the roughness half), **F42** (the 8-bit reader), **F43** (what the other 93.5 % is).

**WHAT IS STILL INHERITED AND OLDEST — and F14 is now past the decay rule:** **F14**
(`gal_end_f`'s 260.0 / 20.0 mm sight lines, **rev 52 — five revisions un-re-measured**), F15 (A7's
803 mm, rev 52), F20 (the colour locks, rev 52), F10 (the galley offset, rev 52), F18 (the die-cut
sticker, rev 44 — **the oldest thing in the file**).

---

## §9. THE HORIZON BEYOND REV 58 — WHERE THIS IS GOING

**Rev 58's own order is §3.0. This section is the longer arc, so the project stops lurching from
item to item.** It is a CARRIER too: each revision should re-rank it, not rewrite it, and **say what
moved**.

**WHAT MOVED AT REV 57, AND WHY.** F08 was *"next"* and is now *"parked, CEILED"* — the route was
taken and the frame cannot answer. F03/F04 were *"next"* and were **refuted as mottle findings**, so
F43 replaces them. F05 rose because F41 shows it is the only arm that can see the mottle.

**AND THEN REV 57b RE-RANKED THE WHOLE TABLE, WHICH IS A BIGGER CHANGE THAN ANY ROW.** The ordering
rule itself was audited and replaced: **pixels of the delivery frame, not gate availability**
(`AUDIT_rev57_efficiency.md`, `visibility_budget.py`). Under the old rule the top job was worth
**1.4 px²**; under the new one it is **3.4 × 10⁶ px²**. Two items that had never appeared in this
table at all — the paint's gloss and the untextured interiors — are now first and second, because
nothing had gated them and the old rule could not see anything it could not gate.

| horizon | the work | worth | why it is in this order |
|---|---|---|---|
| **next** | **the paint's GLOSS.** `gloss_compare.py` fails at 0.392 of the photograph's spread | 3.4 × 10⁶ px² | The largest surface in the frame, newly gated, and never measured before rev 57b |
| **next** | **the untextured galley and roof-aperture interiors** | 7.4 × 10⁵ px² | Bright, central, seen through four openings, and pure placeholder |
| **next** | **F15 — A7.** Illumination, not dressing | 8.2 × 10⁵ px² | A large unlit region changes how the whole rear reads |
| **near** | **F01/F39 — `Senor`**, now known to be the artwork alpha and its placement | 2.7 × 10⁴ px² | Small but HARD-EDGED, so it reads louder per pixel than the table implies |
| **near** | **F43/F05/F41 — the cream's albedo texture and the beauty arm** | large area, subtle | The mottle is 1.1–2.0 % of its own gate; the beauty arm is the only one that can see the roughness half |
| **near** | **F42 — the 8-bit reader.** Decoder written and controlled | — | Cheap; lifts every consumer of `_render`. Re-run them all in the same revision |
| **then** | **F10–F14 — the galley cluster.** F14 is five revisions INHERITED and past the decay rule | 6.8 × 10³ px² | Re-derive each X from `BAYS` |
| **then** | **F02/F06 — the two absolute scales** | — | Every render-to-photograph figure in millimetres runs through a bracket |
| **parked** | **F08 — the badge stroke weight. CEILED-rev57** | **1.4 px²** | Taken, calibrated, refuted in both directions. **Needs a new frame or a pressing model, not another threshold — and it is worth 1.4 px²** |
| **later** | **F19** the red's edge wear; **F16/F17/F20/F23–F28, F37/F38** | — | Unblocked but ungated, or a decision rather than a measurement |
| **standing** | **F18 — the die-cut sticker** | — | The original deliverable. No gate, no owner ruling, open since rev 44 |

**WHAT WOULD CHANGE THIS ORDER:** a new photograph (§0.1 says none is coming), an owner ruling, or a
gate becoming available for something currently ungated — **or, as at rev 57, a gate turning out not
to see the thing it was ranked for.**

## §10. HOW TO GROW THIS HANDOFF WITHOUT BREAKING IT

**Written because rev 56 spent three passes fighting the mechanics rather than the work.**

1. **The set is three files.** `LEDGER_rev<N>.md` (what you did, with every number),
   `NEXT_CONTEXT_PROMPT_rev<N+1>.md` (this file), and **`cp` of that file over
   `PASTE_INTO_CLAUDE_CODE.txt` IN THE SAME COMMIT.** `CLAUDE.md` imports the `.txt` into every
   session, and a byte-identity row fails if you forget. *(The `HANDOFF_rev*.md` series ended at
   rev 45; do not restart it.)*
2. **`README.md` and `START_HERE.md` name the newest brief BY NUMBER.** Two rows check it. Update
   both when you write the brief, not after the verifier tells you.
3. **THE ROW COUNT IS SELF-REFERENTIAL — AND IT IS AUTOMATED NOW, SO STOP HAND-EDITING IT.**
   `python3 audit_brief.py --fix-count` writes the clean-tree total into the brief AND into
   `PASTE_INTO_CLAUDE_CODE.txt`. It cost **three edit cycles at rev 56 and three at rev 57**;
   it should cost one command. The warning below is kept because the mechanism is unchanged:

   **THE ROW COUNT IS SELF-REFERENTIAL AND IT WILL BITE YOU.** `verify_clone.sh` asserts the newest
   brief states the script's own total. **Every row you add changes the number the brief must
   state**, so write the count LAST, and re-run after every fix — including the fixes your own
   audit demands, which add rows of their own. Rev 56's count moved three times.
4. **ADD ROWS ANCHORED ON ARITHMETIC OR BEHAVIOUR, NOT ON A GREP.** A grep passes on a comment. Rev
   56's rows RUN `flank_kv` at two columns, RUN `cream_rms.run()`, and compare two source offsets to
   prove a guard precedes a print. The one row rev 56 wrote as a bare grep needed fixing twice
   because the phrase it counted legitimately appears more than once.
5. **RUN BOTH AUDITS, AS SCRIPTS, AND RECORD WHAT THEY FOUND *IN* THE BRIEF.** The rule-17 sweep
   asks *"is what the file says true?"*; the adversary asks *"what would make it false?"*. They are
   different instruments and they find different things — at rev 56 the sweep found a
   directory-less path and a typo, and **four of the five defects came from running
   `./verify_clone.sh` against the outgoing brief**, which neither pass thought to do until it did.
6. **NEVER DELETE A CARRIER.** §0, §0.1, §4, §5, §8 and §9 are carriers. If a section is the only
   home of something, carry it or hand it on by name. Two carriers have been lost in this project's
   history and both losses took years of context with them.
7. **RANK BEFORE YOU CHOOSE.** `python3 visibility_budget.py` before picking the revision's item,
   every time. The rule it encodes replaced *"gate availability"* at rev 57b after that rule sent
   four consecutive revisions at a **1.4 px²** question. If you find yourself about to work an item
   the script puts in the bottom half, say in the ledger why.
8. **DO NOT LET THE MACHINE IDLE.** Blender is CPU-bound and must not be fanned out, so wall-clock
   is the binding constraint — not tokens, and not context. Launch the render you will need before
   you read the brief; ablate at `T1_MM_SAMP=16`; analyse in the foreground while Blender runs
   behind you. Rev 57 measured ~35 minutes a revision going to avoidable waiting.
9. **ROOM TO GROW:** new findings go in `OPEN_FINDINGS.md` with an ID and a grade, not into this
   file's prose. This file points AT the register. That way the brief stays a map and the register
   becomes the memory, and neither has to be rewritten to add one fact.
