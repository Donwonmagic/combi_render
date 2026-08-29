# NEXT CONTEXT PROMPT — rev 71   ·   **ACTION BRIEF**

**This document is SHORT ON PURPOSE. Read it end to end before you touch anything; it fits.**
**Everything else — every carrier, every refuted route, every owner ruling, the rules canon, the
gate tables — is in `HANDOFF_CARRIERS.md`, complete and verbatim. Nothing was deleted.**

> *[owner, rev 70]* **"I feel that we were way more productive in the first 20 or so handoffs and
> I fear we have drifted since then."** — **He is right and it is MEASURED: run `python3 revstats.py`
> and read ITS numbers, not these.** The shape at rev 70's close: geometry per revision fell from
> **~721 lines** (rev 8–20) to **~215** (rev 61–70) while prose rose, and the brief went **12 KB →
> 95 KB**. **Findings closed at rev 66, 67, 68, 69 were 0, 0, 0, 0 — and rev 70 closed 3, so the
> streak is broken.** **The handoff was split at rev 70 to reverse the drift. Do not re-merge it.**
> *(Figures here go stale every commit — the script is the authority, and §9 requires you to run it.)*

---
## §0 DO THIS FIRST — THE MACHINE IS IDLE WHILE YOU READ

```bash
cd /home/user/combi_render
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
pip install pillow             # bootstrap FAILS 3 of 10 without it, EVERY revision
nohup setsid env T1_SUB=1 T1_PREVIEW=front,side,hero34f,hero34r T1_PFX=r71 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r71.log 2>&1 < /dev/null &
```

**`grep -c Saved: /tmp/r71.log` must be 4.** A backgrounded runner's exit code is the redirect's.
**USE `setsid`, NOT A BARE `nohup &`** (F173). **`out/` is untracked and starts EMPTY**, so every
figure quoted from a frame must be re-rendered before you quote it.

**⚠ THE PREVIEW PATH NEVER CALLS `post.py` (F146).** Run `./judge_set.sh r71` and judge
photorealism on the `_post` set. *(Only `bloom` defaults to 0.0; `ca`, `vig`, `grain` default 1.0.)*

**DO NOT EDIT SOURCE WHILE A RENDER QUEUE RUNS.** Freeze the tree for the duration.

---
## §1 THE OWNER NAMED THREE THINGS. THEY ARE THE REVISION. NOTHING ELSE IS.

> *[owner, rev 69, closing]* **"It is important that we finish the nose render, make the emblem
> correct (a bare minimum qualification) and fix the opening."** … **"I meant to say the back
> opening."** — and, in the same breath, ***"It's been weeks, and a lot of compute, this is
> unacceptable."***

| # | his words | what it IS, measured | § |
|---|---|---|---|
| 1 | *"the back opening"* | **REV 70 TRIED AND RETRACTED (F245).** A chord change 0.7110 → 0.8250 was shipped and reverted **in the same revision**: it broke a 2.9σ two-height closure. **The chord is OPEN with a measured 11 % conflict.** The ANGLE is **unreconciled, not refuted**. What IS visibly wrong is the board's **paint** — red stripe, navy stripe, lit bulbs — which do not read | §2 |
| 2 | *"make the emblem correct"* | the glyph scores **IoU 0.7345 pose-free against a control ceiling of 0.9882** — a deficit of **0.2537**, of which **73.6 % is inside the ring**, and **no constant in this tree expresses a stroke PATH** | §3 |
| 3 | *"finish the nose render"* | the shape is **BUILT and guarded**. What is missing is **rendering it and looking at it** | §4 |

**RANK: 2, 3, then 1.** Item 1 has now had a revision spent on it and its geometry question is a
**measurement conflict, not a build** (§2) — it needs a resolved ruler before another constant moves.
**The emblem is the live build item and its instrument is ready.**

---
## §2 ITEM 1 — THE BACK OPENING · **REV 70 TRIED IT AND RETRACTED. READ THIS FIRST.**

> *[owner, rev 62]* ***"The bus's rear hatch, propped open."***

**THE REGISTER ROWS ARE F242, F244 AND — most importantly — F245.**

**⚠ REV 70 SHIPPED A CHORD CHANGE AND REVERTED IT IN THE SAME REVISION. A DISPATCHED ADVERSARY CAUGHT
IT. DO NOT REPEAT IT.** The reasoning felt decisive: pick the board's two ends on `ref_side.jpg`, paint
them, 177.1 px, divide by the `k_t = 215.5` this file records → 0.822 m; F165 gives 0.829 on the other
frame; ship the mean. **Three things were wrong:**

1. **WRONG RULER (rule 38).** `ref_side.jpg` is a **PROJECTIVE** image and `flank_compare.py` says so
   itself — *"every scalar px/m is wrong somewhere. Two instruments exist and this file uses them."*
   Through `flank_X` and `flank_kv`, **the same picks give 0.7899 m, not 0.822.**
2. **THE SOURCE ALREADY SAID SO, TWO LINES BELOW THE CONSTANT:** *"a single px/m **over-reads by
   4.8 %**"* — and the change adopted a value larger than the over-read.
3. **IT BROKE A MEASURED CLOSURE.** Base z **1.7470 ± 0.027** and tip z **2.184 ± 0.030** are
   independently measured, and `(2.184 − 1.747)/sin 38° = 0.7098`. **THE SHIPPED 0.7110 IS NOT A PIXEL
   READ — IT IS DERIVED FROM TWO MEASURED HEIGHTS.** 0.8250 put the tip **2.9σ** outside one.

**THE CONFLICT IS REAL AND IS THE ACTUAL OPEN QUESTION HERE:**

```
    two-height closure          0.710 m    two MEASURED heights at 38 deg
    calibrated chord read       0.790 m    flank_X / flank_kv, painted picks
    F165 on IMG_3840.jpeg       0.829 m    flat 107.92 px/m -- same ruler flaw
```

**The first two are BOTH from `ref_side.jpg` and disagree by 11 %. One is wrong; nothing in this tree
resolves it. DO NOT AVERAGE THEM — that is precisely the mistake rev 70 made.** Settle the ruler
before you move the constant.

**THE ANGLE IS UNRECONCILED, NOT REFUTED — and rev 70 overstated this too.** `ref_side.jpg` images the
board at **38.8°** (two end picks) but its navy upper stripe fits **43.7°** (rms 0.74 px, 32 columns);
`IMG_3840.jpeg` reads **21.0°**, but on THAT frame the board's own two long edges disagree by **15°**,
which means the board's axis has a large depth component there and an image-plane angle is not a
vehicle angle at all. **The board IS hinged — but this evidence does not establish it, and F165's 28.0
is UNRECONCILED rather than disproved.** The shipped **38.0°** matches the primary frame's end-pick
read. **DO NOT move it without settling the estimator question first.**

**THE GATE, AND WHAT REV 70 GOT WRONG IN IT.** `verify._tail_board_pose` reads the board's **principal
axis in XZ off the built mesh** (not the bbox diagonal — F165's "built 38.4 / 0.732" IS the bbox
diagonal, rule 38). Its first cut had a **chord floor set 29 mm BELOW the weaker of the two bounds it
quoted** — a bar chosen to pass the value being shipped (rule 6). **That floor is deleted.** In its
place, a **TIP-HEIGHT arm**, because tip height is the only quantity on this board with an independent
measured value. **Watched failing at the retracted candidate: tip 2.2790, +95.0 mm, 3.2σ.** Angle band
widened ±4 → ±6 because the frame's own estimators spread ~5°.

**WHAT IS ACTUALLY VISIBLY WRONG, AND IT NEEDS NO NEW MEASUREMENT.** Held against `ref_side.jpg`, the
render's board is a **plain white plank with pale bulbs**; the photograph shows a **cream face, a RED
edge stripe, a dark NAVY stripe and LIT amber bulbs**. `tb_edge_red`, `tb_edge_dark`, `tb_bulbs` and
`tb_bulbflex` all exist in the mesh — the red stripe reads from the rear ¾. **This is materials and
emission, not form, and it is the honest remainder of item 1.**

**TWO THINGS ARE SETTLED — DO NOT RE-OPEN.** The dark rectangle under the board is **`glass_rear`**,
the rear window: 72 verts, x −2.1510…−1.8501, z 1.4554…1.6064, `glass` at **Transmission 1.00**, 5 of
9 forward rays hit the shell. It reads black because a transmissive pane looks into an **unlit
interior** — **F71's branch, not a hole** (F244). *(CEILING: F244 measures the MESH; it does not
project `glass_rear` into the frame and paint it onto that rectangle. The identification is strong but
the painting was not done.)* And **the "dark angled recess" was NOT built**: it appears only on the
chalkboard frame, on a surface the primary frame does not show, at 480 px where geometry, paint and
shadow cannot be separated. **It cannot be recovered from what we hold** (rule 12).

**⚠ AND `HANDOFF_CARRIERS.md` §0.05 IS THE PRE-REV-70 TEXT. Its "WHAT TO BUILD" list is WRONG: it asks
for "a panel with real thickness and an underside" and calls that "the largest visible defect" —
`TB_T = 0.0220` and `T.solid_prism` have been there since long before rev 70. The board has always had
thickness. Read that section as HISTORY, and this section as the state.**

---
## §3 ITEM 2 — THE EMBLEM

> *[owner]* ***"Neither — both still wrong."*** then ***"Just what the fuck. Are you telling me?
> That looks right to you?"*** — his **eighth and ninth** reports of this emblem.

**THE COMPARISON THIS PROJECT NEVER HAD, BUILT AT REV 69.** Every other emblem statistic reads an
OBLIQUE photograph against a HEAD-ON raster (F184's trap). `probe_rev69_fitpose.py` **projects the
model and fits the pose out as a nuisance parameter**; the residual that survives is SHAPE.

```
    CONTROL P1, watched                                 IoU 0.9882   <- the ceiling
    the mark, pose fitted out, on ref_workshop.jpg           0.7345
      the RING BAND alone                                    0.8874   <- the ring is FINE
      INSIDE the ring alone                                  0.6168   <- 73.6 % of the miss
      photo-only / model-only inside the ring              296 / 378  <- NEAR BALANCED
```

**THE INK IS THE RIGHT AMOUNT AND THE WRONG ARRANGEMENT** (F104, carried since rev 60, never acted
on). **Every lever is exhausted, measured against that residual:** the stroke weight swept alone
peaks at **+0.0048**; **all seven constants together buy +0.0112 — 4.4 % of a 0.2537 deficit.**

**WHY, FROM THE SOURCE.** `t1_core._spines()` asserts every terminal onto the band circle and
`_on_band` **normalises**, so each pair contributes only a DIRECTION — magnitude divides out.
**A stroke's ANGLE is not a free parameter of this model at all** (rule 54). That is why eight
revisions of solving moved nothing.

**BUILD:** give each stroke its **own centreline with free endpoints**, not forced onto the band
circle, so the six strokes can be made near-parallel. Fit against `probe_rev69_fitpose.fit()`.

> **⚠ FOUR TRAPS.** **(a) DO NOT FIT TO AN ANGLE.** `probe_rev69_angles.py`'s own control **A1
> FAILS at 36.30° rms**, larger than the residual it reports, and the live photographed spread reads
> **46.5°, not the 28.6° F235 published**. Use the pose-free IoU; quote angles only as description.
> **(b) FIT ON ONE FRAME, SCORE ON THE OTHER — never both jointly.** The two frames are not
> comparable (0.7345 vs 0.6671 for the same build is frame quality). **(c) RE-CUT `IMG_2073`'s BOX
> FIRST** — `(288,542)–(352,640)` discards **~14 % of the mark's ink** and was never painted;
> `(283,537)–(357,662)` is the honest window. **(d) THE TRACE IS OVERFIT, NOT BETTER:**
> `T1_VW_TRACED` wins **+0.0905 on the frame it was traced from** and **loses 0.0249** on an
> independent one. P4 goes red if it ever wins independently. **It stays OFF.**

**READ `HANDOFF_CARRIERS.md` §2 — SEVENTEEN REFUTED ROWS — BEFORE YOU TRY ANYTHING HERE.**

**AND TWO EMBLEM ITEMS THAT KEEP FALLING OUT OF THIS DOCUMENT — THIS IS THEIR THIRD DROP (rule 16):**
* **F180 IS STALE AND NO REVISION HAS CLOSED IT** — it says **FOUR** ring contacts; `probe_rev63_reach.py`
  reports **SIX**. What moved four → six is **not** the arc cut (it reads six under `T1_VW_NOARC=1`) and
  **not** the spine constants; the remaining candidate is **F204's stroke weight**.
* **THE FIT DEPTH IS STILL UNMEASURED** — the glyph's extreme is fitted 20 % into the band,
  `1.0 - 0.8 * _BAND_FRAC` in `t1_core.py`. **The answer is a MEASUREMENT, not a guess.**
* ⚠ **Dropped by rev 69's first draft, restored by an adversary; dropped again by the split, restored
  again. If you rewrite this section, carry them.**

**⚠ AND IF YOU RE-CUT `IMG_2073`'s BOX, TWO FILES HARD-CODE IT:** `probe_rev69_fitpose.py`'s `FRAMES`
table **and** `audit_adversary.py`'s second-frame question. Re-cut one only and the guard silently
keeps checking the old, clipped window.

---
## §4 ITEM 3 — THE NOSE

**The geometry is BUILT and guarded.** `t1_detail.bumper`'s eleven constant-x points are draped onto
the body's own front-face plan curve, raycast at build time. `BUMP_BOW = 1.0`, `BUMP_BOW_Z = 1.100`,
ablation `T1_BUMP_BOW`. Measured on the mesh **+21.55 mm at `T1_SUB=2`** (`STATE.md`); ablated it reads **+0.22 mm at `T1_SUB=1`** — **name the subdivision, the two differ**. Watched failing:
`T1_BUMP_BOW=0` → `VERIFY: 2 fail`.

**SO "FINISH THE NOSE RENDER" IS NOT MORE GEOMETRY. IT IS THE STEP THIS PROJECT SKIPS (rule 1):**

```bash
T1_SUB=1 T1_PREVIEW=front T1_PFX=r71 T1_RX=3200 T1_RY=2200 T1_SAMP=128 \
  /tmp/blender/blender -b -P build.py      # then CROP THE NOSE AND LOOK AT IT
python3 probe_rev67_nose.py out/r71_front.png    # PASS IT A FRAME -- bare, P3 does not run
python3 probe_rev59_nose.py out/r71_front.png    # READ BOTH RULERS
```

**Render the control TWICE and publish the floor** — 1600×1100/96 spp is **2.441 % of pixels >8
levels, worst channel 40** (rule 49).

> **⚠ CEILINGS, NOT TASKS.** The guard's own docstring: *"a 28 % error in the one constant it exists
> to police would PASS"* and *"NOT A FIDELITY CLAIM."* **"Guarded" means the face is not FLAT.**
> The bow's MAGNITUDE cannot be recovered from the frames we hold (F231); F223's bracket
> **B ∈ [16, 76] mm contains the shipped 19.6**, so nothing excludes the shipped nose.
> **DO NOT ASK HIM THE NOSE AGAIN — both askings are spent.** Check the catalogue literature
> first (F229, rule 52); the sources are named in `HANDOFF_CARRIERS.md` §0.06.

---
## §5 THE BRANCH — MEASURE IT, DO NOT TRANSCRIBE IT

```bash
git fetch --all --prune
git rev-parse --is-shallow-repository        # <- rev 62..69 ALL arrived TRUE
for b in $(git branch -r | grep -v HEAD); do
  printf "%-52s ahead %-3s behind %s\n" "$b" \
    "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"; done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
```

> **⚠ MEASURED AT REV 70's CLOSE: `origin/claude/nose-fixture-alignment-r68-rrqyqx` IS AHEAD OF
> `origin/main` AND MERGED NOWHERE.** `bootstrap.sh` prints the number and says so itself:
> *"Row 9 cannot see this axis — it only finds branches ahead of HEAD."* **A fresh clone defaults to
> `main` and would silently redo a whole revision on a stale tree** — that is exactly how rev 57b's
> work sat stranded from rev 57 to rev 64. **Check out the branch before reading another file.**
> **⚠ AND IT IS WORSE THAN STALENESS: `origin/main` HAS NO `HANDOFF_CARRIERS.md`, NO rev-71 BRIEF AND
> NO `LEDGER_rev70.md`. Its `PASTE_INTO_CLAUDE_CODE.txt` is the rev-70 brief, whose #1 instruction is
> to move the hatch angle to 28.0° — the instruction rev 70 spent a revision showing you must not
> follow.** A clone that lands on `main` is actively misdirected, not merely behind. **CARRY THE
> AHEAD/BEHIND NUMBER `bootstrap.sh` prints — it tells you to — and note the branch may also be
> BEHIND: `origin/main` moved during rev 70's own audit.**
> **And re-measure at close: no sentence about branch state survives the hour.**

---
## §6 THE MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build T1_SUB=1 ~20 s      render 1600x1100 96 spp ~4.5-5.5 min PER VIEW
```

**`bpy` IS A PIP MODULE**, so most probes run in ~1 s without the Blender CLI. **Do not fan out
Blender** — it is CPU-bound; render sequentially in the background and analyse in the foreground.

```bash
./bootstrap.sh                                # ALL 10 PASS -- read ROW 9 and its NOTE
./verify_clone.sh                             # ALL 358 PASS -- read its verdict block
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py    # -> "VERIFY: 0 fail, 0 warn"
python3 flank_compare.py out/r71_side.png /tmp/fc.png   # photograph gate 1 -- NAME THE FRAME
python3 gloss_compare.py out/r71_hero34f.png            # photograph gate 2
python3 probe_rev70_tyre.py out/r71_side.png            # photograph gate 3 -- PASS IT A FRAME
python3 probe_rev69_fitpose.py                          # photograph gate 4 -- the emblem, pose-free
python3 probe_rev46_vw.py                               # C4 is the only red row
python3 cream_rms.py                                    # the LIVE photograph-side cream
python3 visibility_budget.py 3840 out/r71_hero34f.png   # PASS IT A .png or it globs by mtime
python3 revstats.py                                     # THE DRIFT DETECTOR -- run it at close
T1_SUB=2 /tmp/blender/blender -b -P audit.py            # rewrites STATE.md -- COMMIT FIRST
python3 audit_brief.py ; python3 audit_adversary.py     # rules 15/17, MECHANICAL half only
```

**FACTS THAT BITE:** `bootstrap.sh` fails 3/10 without `pip install pillow`. Every measurement
through `shader_solve._render` is 8-bit. **The render is NOT run-to-run deterministic** — no Cycles
seed. `lid_gen.py` and `script_gen.py` are **not** called by `build.py`. `audit.py` rewrites
`STATE.md` — commit first. **`ck` in `verify_clone.sh` collapses whitespace.**

**⚠ `probe_rev46_vw.py`'s C6 passes 6 = 6 — ON THE RASTER. On the RENDER the same function reads 3
against the photograph's 6 (F205).** A gate can be corrected, guarded, swept and still be measuring
the wrong object (rule 41). **Run the emblem gates on the FRAME.**

**RANK BY PIXELS OF THE DELIVERY FRAME** before you choose — the emblem is item 9 of 16 at
3.32e4 px² against a top item of 3.83e6 px², **115× bigger** — **but the owner outranks the ranking,
and §1 IS him.**

---
## §7 THE RULES THAT WILL BITE YOU THIS REVISION

The full canon (1–54) is in `HANDOFF_CARRIERS.md` §5 and `NEXT_CONTEXT_PROMPT_rev50.md` §11.
These eight cost this project a revision each and are the ones this work will touch:

1. **RENDER IT, CROP IT, AND LOOK AT IT** — before and after every change. Every defect this project
   shipped passed `VERIFY: 0 fail, 0 warn` and was found by looking at a crop.
3. **A control is finished when you have WATCHED IT FAIL on the defect**, not when it passes.
8. **YOU MUST NOT PUBLISH A NUMBER FROM A MASK OR WINDOW YOU HAVE NOT PAINTED AND LOOKED AT.**
   Painted BEFORE the number. Five of nine wrong instruments in one revision were this.
12. **Report the measurement WITH ITS CEILING.** *"It cannot be recovered from what we hold"* is a
    real result and is worth more than a guess.
13. **Add the guard in the same edit as the change.**
16. **YOU MUST NOT DELETE A CARRIER.** It may be MOVED and cited by name — that is what
    `HANDOFF_CARRIERS.md` is — but it may not be dropped.
34. **A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Check which object a *"the
    record requires X"* sentence is about, and check the cited line still exists.
35. **A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Ask the geometry, never the pose.

---
## §8 WHERE EVERYTHING ELSE LIVES

| file | what it holds | read it when |
|---|---|---|
| **`HANDOFF_CARRIERS.md`** | **every carrier: §0 goal + gate table, §0.1 the reference set, §2's seventeen refuted emblem routes, §4 the owner's rulings, §5 rules 34–54, §6 the full machine notes, §7 the standard, §8 the register's conventions, §9 the horizon, §10 how to write the next handoff** | **before re-trying anything, quoting any gate, or asking him anything** |
| `OPEN_FINDINGS.md` | 244 rows, 118 open. **The register outranks prose.** | before you derive anything — F104, F209 and F222 were all found sitting there unread |
| `STATE.md` | machine-written; **outranks every prose description** | before quoting any dimension |
| `LEDGER_rev70.md` | what rev 70 did, and **§4, where its own brief was wrong about its own top item** | before you plan |
| `EMBLEM_HANDOFF.md` | the emblem's own carrier — **its §3 is a STALE second copy of the refuted list** | emblem work only |
| `SPEC.md`, `SURVEY_rev49_photoreal.md`, `REF_MEASUREMENTS.md`, `ROADMAP_rev68.md`, `PHOTOS_WANTED_rev49.md`, `PHOTOS_WANTED_rev52.md`, `REMAINING_WORK_rev61.md`, `PANEL_rev61.md` | large; load the one the task needs | on demand |

---
## §9 HOW TO CLOSE THIS REVISION

**THE OWNER'S STANDARD, IN HIS WORDS:** photo-realistic parity with **that exact bus**. **Any single
measurement off is unacceptable** — per-measurement, not on average. Ground in the reference, build,
adversarially audit, iterate. **Never call it done off self-review. Report the measurement with its
ceiling, never a self-assigned score. Do not say anything is ready** — say what is fixed, what is
still wrong, and what you measured.

**AND THE NEW ONE, WHICH THE MEASUREMENT AT THE TOP OF THIS FILE EARNED:**

> **55. EVERY REVISION SHIPS A VISIBLE CHANGE TO THE VEHICLE, OR SAYS PLAINLY WHY IT COULD NOT.**
> All 54 existing rules are about not being WRONG; not one was about shipping. Rev 66–69 wrote
> ~900 geometry lines and closed **zero** findings; rev 70 closed **3**. **Run `revstats.py` for the
> live pair — do not quote this sentence.** `verify_clone.sh` now has a row for this.

**BEFORE YOU CLOSE:**
1. `./bootstrap.sh` and `./verify_clone.sh` both all-PASS on a **clean** tree.
2. `python3 revstats.py` — **and put its geometry/closure line in the ledger header.** If this
   revision closed nothing and shipped nothing, say so at the top, not in a footnote.
3. Regenerate `STATE.md` (`T1_SUB=2 … audit.py`) — **commit first**.
4. **Put an adversary on the brief you WROTE, not only the one you received (rule 17), and DISPATCH
   it.** The last one returned **21 defects, four on the top item**.
5. **Keep the split.** Action brief short; carriers in `HANDOFF_CARRIERS.md`; `cp` the brief over
   `PASTE_INTO_CLAUDE_CODE.txt` in the same commit. **`HANDOFF_CARRIERS.md` §10 has the rest.**

**⚠ THIS BRIEF WAS AUDITED AGAINST THE MACHINE, AND THE AUDIT REVERSED ITS TOP ITEM.**
`audit_brief.py` 10 checked / 0 FAILED; `audit_adversary.py` 57 asked / 0 BROKE. **A dispatched
adversary audited THIS document (not an earlier one) and its most important finding is F245: the
chord change this brief's previous draft announced as shipped was a REGRESSION, and it is reverted.**
It also found F180 and the fit-depth item dropped for a THIRD time (restored, §3), the carriers' run
block pointing at stale frames (fixed), and this brief's own headline publishing a closure streak the
script it cites says is broken (fixed). *(The rev-70 record — 21 defects on the pre-split long form —
is in `HANDOFF_CARRIERS.md` §0.02.)*
**WHERE IT IS STILL WEAKEST:** **§2's chord conflict is UNRESOLVED — 0.710 vs 0.790 from the same
frame, an 11 % disagreement nothing in this tree settles**; the angle is unreconciled, not refuted;
`HANDOFF_CARRIERS.md` §0.05 is pre-rev-70 text whose build list is wrong; and every figure quoted from
`out/` needs a re-render before you quote it.
