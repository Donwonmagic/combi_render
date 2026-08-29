# NEXT CONTEXT PROMPT — rev 71   ·   **ACTION BRIEF**

**This document is SHORT ON PURPOSE. Read it end to end before you touch anything; it fits.**
**Everything else — every carrier, every refuted route, every owner ruling, the rules canon, the
gate tables — is in `HANDOFF_CARRIERS.md`, complete and verbatim. Nothing was deleted.**

> *[owner, rev 70]* **"I feel that we were way more productive in the first 20 or so handoffs and
> I fear we have drifted since then."** — **He is right and it is MEASURED. Run `python3
> revstats.py`.** Geometry output fell from **721 lines/revision** (rev 8–20) to **209** (rev 61–70)
> while prose rose; the brief went **12 KB → 95 KB**; and findings CLOSED at rev 66, 67, 68, 69, 70
> were **0, 0, 0, 0, 0**. **The handoff was split at rev 70 to reverse that. Do not re-merge it.**

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
| 1 | *"the back opening"* | **BUILT AT REV 70 (F242/F243).** The chord was the defect — 0.7110 → **0.8250 m**, agreed by two frames. **The ANGLE was NOT a defect and 28.0° is REFUTED: the board is HINGED.** What is left is that its **red stripe, navy stripe and lit bulbs do not READ in the render** — paint and emission, not form | §2 |
| 2 | *"make the emblem correct"* | the glyph misses by **0.38 IoU pose-free** against a control ceiling of 0.98, and **no constant in this tree expresses a stroke PATH** | §3 |
| 3 | *"finish the nose render"* | the shape is **BUILT and guarded**. What is missing is **rendering it and looking at it** | §4 |

**RANK: 1, 2, 3 — his own order.** Item 1 is un-built geometry with the ruling already given and
the measurement already taken. **It needs no new instrument to start. START THERE.**

---
## §2 ITEM 1 — THE BACK OPENING · **BUILT AT REV 70. READ THIS BEFORE YOU TOUCH IT.**

> *[owner, rev 62]* ***"The bus's rear hatch, propped open."*** *[owner, rev 70]* ***"Now build the
> back opening."***

**F163 IS DISCHARGED AND F165 IS SPLIT. The register rows are F242, F243, F244.**

**⚠ THE FIRST THING TO KNOW IS THAT THIS SECTION'S OWN PREVIOUS INSTRUCTION WAS WRONG.** Rev 70's
brief told you to move the angle from 38.0° to a *"photographed 28.0°"*. **Doing that would have made
the model WORSE.** Re-measured on both frames, every pick painted first:

```
    ref_side.jpg    RED bus, CURRENT livery, F163's PRIMARY frame     38.8 deg
    IMG_3840.jpeg   the SAME board, CHALKBOARD livery                 21.0 deg
    BUILT                                                             38.0 deg   <- matches PRIMARY
    F165 published                                                    28.0 deg   <- matches NEITHER
```

**THE BOARD IS HINGED, SO ITS ANGLE IS A POSE, NOT A DIMENSION.** The two frames are 18° apart because
somebody propped it differently on two different days; 28.0 sits between them and describes neither.
**DO NOT "FIX" IT.** `verify._tail_board_pose`'s angle arm was **watched firing at exactly 28.0**, and
`T1_TB_TILT` lets you see that for yourself in one command.

**WHAT SHIPPED: `TB_CHORD` 0.7110 → 0.8250 m.** Two independent frames, two scales, two picks:
`ref_side.jpg` **≥0.822 m** (177.1 px between painted ends at the file's own `k_t = 215.5 ± 3.0`) and
`IMG_3840.jpeg` **≥0.829 m** (F165). They agree to **0.9 %**. **Both are LOWER BOUNDS and so is the
shipped value** — the board sits inboard of the flank plane, where px/m is smaller and the metric
length larger. 0.8250 is the shortest length consistent with both frames, not an estimate of the true
one.

**THE GATE THIS OBJECT HAD NEVER HAD:** `verify._tail_board_pose`. It reads the board's **PRINCIPAL
AXIS in XZ off the built mesh** and says so in its own text, because **F165's published "built 38.4° /
0.732 m" is the BOUNDING-BOX DIAGONAL** and the constants are 38.0 / 0.7110 — a ruler mismatch
(rule 38). Both arms watched failing: `T1_TB_CHORD=0.7110` → `VERIFY: 1 fail`; `T1_TB_TILT=28.0` →
`VERIFY: 1 fail`.

**WHAT IS LEFT ON THIS OBJECT, AND IT IS PAINT, NOT FORM.** Held against `ref_side.jpg` the render's
board is a **plain white plank with pale bulbs**, where the photograph shows a **cream face, a RED
edge stripe, a dark NAVY stripe and LIT amber bulbs**. `tb_edge_red`, `tb_edge_dark`, `tb_bulbs` and
`tb_bulbflex` all EXIST in the mesh — the red stripe is visible from the rear ¾ — so **this is a
materials/emission question, not a geometry one.** Start by rendering `side` and cropping the board.

**TWO THINGS ARE CLOSED — DO NOT RE-OPEN THEM.**
* **The dark rectangle under the board is `glass_rear`, the rear WINDOW** — 72 verts, x −2.151…−1.850,
  z 1.455…1.606, material `glass` at **Transmission 1.00**, and 5 of 9 rays fired forward hit the
  shell. It reads black because a fully transmissive pane looks into an **unlit interior**. That is
  **F71's branch — flat glazing — NOT a hole** (F244).
* **The "dark angled recess" was NOT built, and that is a result (rule 12).** It appears only on the
  CHALKBOARD frame, on a surface the primary frame does not show, and at 480 px cannot be separated
  into geometry, paint or shadow. **It cannot be recovered from what we hold.**

**AND THE METHOD NOTE WORTH MORE THAN THE RESULT: RULE 8 KILLED THREE WINDOWS HERE.** A "cream face"
mask on `ref_side.jpg` selected **the wall** (33.5°); a "bulb string" mask selected **the red wall
graphics** (24.7°, rms 27.6 px on a 174 px baseline); and the orange face's **principal axis** read
21.7°, because a foreshortened wedge's principal axis is not its chord. **Three plausible,
publishable numbers, every one wrong, every one caught by PAINTING and none by reasoning.**

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

---
## §4 ITEM 3 — THE NOSE

**The geometry is BUILT and guarded.** `t1_detail.bumper`'s eleven constant-x points are draped onto
the body's own front-face plan curve, raycast at build time. `BUMP_BOW = 1.0`, `BUMP_BOW_Z = 1.100`,
ablation `T1_BUMP_BOW`. Measured on the mesh **+0.05 mm → +21.55 mm** (`STATE.md`). Watched failing:
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
> All 54 existing rules are about not being WRONG; not one was about shipping. Rev 66–70 wrote
> 1,122 geometry lines and closed **zero** findings. `verify_clone.sh` now has a row for this.

**BEFORE YOU CLOSE:**
1. `./bootstrap.sh` and `./verify_clone.sh` both all-PASS on a **clean** tree.
2. `python3 revstats.py` — **and put its geometry/closure line in the ledger header.** If this
   revision closed nothing and shipped nothing, say so at the top, not in a footnote.
3. Regenerate `STATE.md` (`T1_SUB=2 … audit.py`) — **commit first**.
4. **Put an adversary on the brief you WROTE, not only the one you received (rule 17), and DISPATCH
   it.** The last one returned **21 defects, four on the top item**.
5. **Keep the split.** Action brief short; carriers in `HANDOFF_CARRIERS.md`; `cp` the brief over
   `PASTE_INTO_CLAUDE_CODE.txt` in the same commit. **`HANDOFF_CARRIERS.md` §10 has the rest.**

**⚠ THIS BRIEF WAS AUDITED AGAINST THE MACHINE.** `audit_brief.py` 10 checked / 0 FAILED;
`audit_adversary.py` 57 asked / 0 BROKE, four questions replaced with behavioural ones and three
watched failing; a dispatched adversary returned **21 defects on the long form of this document —
four on its own #1 item**, all addressed. **The full audit record is `HANDOFF_CARRIERS.md` §0.02.**
**Where it is still weakest: §2's photographed angle and chord are INHERITED from rev 62 and were
NOT re-measured; and every figure quoted from `out/` needs a re-render before you quote it.**
