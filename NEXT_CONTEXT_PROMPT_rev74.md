# NEXT CONTEXT PROMPT — rev 74   ·   **ACTION BRIEF**

**REV 73 SHIPPED GEOMETRY: THE EMBLEM'S FREE-ENDPOINT SPINE (F301), THE OWNER'S NINTH REPORT. `revstats.py` SAYS `73 | 123 geometry | 0 closed` — **RUN IT for the doc and instrument columns; they are still growing as this handoff lands and every figure typed for them here has already gone stale twice**, AND
THAT IS TWO REVISIONS IN THREE THE OWNER CAN SEE NOTHING FROM.** Both of his ranked items were
instrument-shaped and the second returned a null. **DO NOT LET REV 74 BE A THIRD.** Run
`python3 revstats.py` and read ITS numbers. Every carrier lives in `HANDOFF_CARRIERS.md`; every
finding in `OPEN_FINDINGS.md`; every measurement in a probe that RUNS. **This file is only what to
do next. DO NOT GROW IT.**

> *[owner, rev 72]* **"Nose, then gloss/flank."**  — **BOTH DONE AT REV 73, AND THE SECOND IS A NULL.**
> *[owner, rev 71]* **"The ultimate goal is a 3d render from which to build promotional material
> from."** and **"I certainly want physics closed."**
> *[owner, rev 72]* **"set up for success so that it can only carry forward, no regression allowed."**

**THE EMBLEM IS STILL HIS NINTH REPORT AND IT IS STILL WRONG. F191 AND F234 BOTH STAND.** Rev 72's
ruling set an ORDER for ONE revision and that revision is over.

---
## §0 DO THIS FIRST — THE MACHINE IS IDLE WHILE YOU READ

```bash
cd /home/user/combi_render
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
pip install pillow             # bootstrap FAILS 3 of 10 without it, EVERY revision
nohup setsid env T1_SUB=1 T1_PREVIEW=front,side,hero34f,hero34r T1_PFX=r74 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r74.log 2>&1 < /dev/null &
```
**`grep -c Saved: /tmp/r74.log` must be 4**, ~5.5 min a frame. `setsid`, not a bare `nohup &` (F173).
**`out/` starts EMPTY** — re-render before quoting any frame. **DO NOT EDIT SOURCE WHILE THE QUEUE
RUNS** (probes and `.md` are fine; `build.py` and the `t1_*` modules are not).
Then `./judge_set.sh r74`.

## §0b BEFORE YOU MEASURE ANYTHING

```bash
python3 photometry.py          # 9 checked, 0 FAILED
```
**READ LINEAR / REFUSE CLIPPED / MEDIAN NOT MEAN / PAINT THE WINDOW. Import it; do not re-derive it.**

⚠ **AND DO NOT SPEND REV 74 RE-READING THE GATES AT 16 BITS.** F271 measured it a null; the
rev-73 adversary showed the published **0.623 %** does not reproduce (**0.708 %** on a fresh frame,
a move of 13 % of itself, **with no floor under it — rule 49**). The conclusion survives, the
figure does not. **DO NOT REDO IT AND DO NOT RE-QUOTE 0.623 %.**

---
## §1 THE BRANCH — MEASURE IT, DO NOT TRANSCRIBE IT, **INCLUDING THIS SENTENCE**

```bash
git fetch --all --prune
for b in $(git branch -r | grep -v HEAD); do printf "%-52s ahead %-3s behind %s\n" "$b" \
  "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"; done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
```
**⚠ THIS IS NOT A RITUAL. AT REV 73 IT PAID.** `bootstrap.sh` row 9 FAILED on pickup:
**`STRANDED: origin/claude/combi-render-r72-fqgsj5 (2 commits, 6 files)`** — and those two commits
were **the owner's own regression lock**. Until they were merged, `main` had **no `§3b`, no
`bootstrap.sh --guards` sweep, and 381 `verify_clone.sh` rows instead of 392**, while the owner's
message for rev 73 cited §3b and instructed `--guards`. **In the same `git fetch --prune`, rev 73's
own designated branch was DELETED from the remote.** **THE REV-73 BRIEF SAID *"EIGHT CONSECUTIVE REVISIONS"* (F253/F267) AND REV 73 MADE IT
NINE. `LEDGER_rev73.md` §1 SAYS "SEVENTH" AND IS WRONG — IT DROPPED F253/F267's OWN COUNT.
THE COUNT IS HAND-INCREMENTED AND DERIVED FROM NOTHING: DO NOT TRUST IT EITHER. Believe row 9
and the loop, never this paragraph.**

---
## §2 RANKED WORK FOR REV 74

**⚠ THE OWNER'S REV-72 RULING IS SPENT — IT WAS EXPLICITLY FOR ONE REVISION (F282). DO NOT READ IT
AS STANDING ORDER, AND DO NOT INVENT A NEW ONE FOR HIM.** **RANK BY PIXELS OF THE DELIVERY FRAME** —
`python3 visibility_budget.py 3840 out/r74_hero34f.png` — and **the owner outranks the ranking**.
⚠ **AND READ THAT TABLE'S OWN CEILING BEFORE USING IT: *"pixels are not visibility … Use this to
catch ORDERS OF MAGNITUDE, not to rank neighbours."*** At rev 72 the brief claimed the owner and
the ranking *"AGREED for the first time"*; the ranking cannot support that — his first item, the
nose, is item 8 at 4.20e4 px², only **1.27×** the emblem he put third, which is neighbours (F291).
The ranked list is `REMAINING_WORK_rev61.md`, triaged into `ROADMAP_rev68.md`.

### **1. SHIP GEOMETRY. ANY GEOMETRY. RULE 55 IS THE BINDING CONSTRAINT ON REV 74.**
**⚠ AND THE FIRST DRAFT OF THIS SECTION NAMED §0.05's ITEM 2 — the *"dark angled recess"* — AS
THAT GEOMETRY, *"needs NO NEW MEASUREMENT"*. REV 73 THEN WENT AND LOOKED, AND WITHDREW IT (F295).**
In RAW pixels the feature is **64 px below luminance 100, 30 × 12 px in a 480 × 320 JPEG, and it is
a BENT LINE one to four pixels thick, not an area.** And the primary frame cannot corroborate it by
construction: **`ref_side.jpg` shows the board almost exactly EDGE-ON**, so its FACE is invisible
there — the same fact F276 used to kill item 1, applied to item 2. **Two readings survive and
nothing separates them: a slot cut in the face, or the shadowed GAP between the board and the roof
dome — which the model ALREADY produces, standing `+4.0 mm clear`.** Building the first would
invent a feature and hide a correct one. **ITEM 3 IS NOW MEASURED (F296) AND ALSO LICENSES NO
CHANGE.** So the honest geometry candidates for rev 74 are elsewhere: the tyres' TREAD, the tail's
barrel, the shut lines, **F143 the roof loudspeakers (unmodelled for 57 revisions)** — **and every
one of them needs its grounding checked FIRST, which is the lesson of items 2 and 3.**

**⚠ AND ONE THING THE FIRST DRAFT OF THIS SECTION GOT FLATLY WRONG, CORRECTED BY THE RULE-17
ADVERSARY BEFORE THIS FILE SHIPPED — KEPT VISIBLE RATHER THAN QUIETLY EDITED, BECAUSE IT WOULD HAVE
COST REV 74 ITS TOP JOB.** It said *"the ranking's own #1 item has never been in any brief: `F67`,
the contact shadow, `3.83e6 px²`… no brief has named it."* **THREE THINGS WERE WRONG:**
* **F67 IS THE OWNER'S OWN ITEM D** and had whole sections — `NEXT_CONTEXT_PROMPT_rev60.md` §3.3
  *"ITEM D — THE GROUND SHADOW AND UNDERBODY (F67). NEVER ATTEMPTED."*, `rev61` §2.1 *"ITEM D — THE
  UNDERBODY, BUILT (F67)"*. It was partly built at rev 61.
* **THE FIGURE WAS PUBLISHED AT REV 71** — `NEXT_CONTEXT_PROMPT_rev71.md` prints *"3.32e4 px²
  against a top item of 3.83e6 px², **115× bigger**"*.
* **`HANDOFF_CARRIERS.md` GRADES IT `CEILED`** (§9's table) — and it is **NOT GEOMETRY**: it is a
  compositor/lighting item, `SURVEY_rev49_photoreal.md` records *"THE CONTACT SHADOW'S MAGNITUDE IS
  DELIVERED ON THE DIRECT PATH AND MATCHES ITS DECLARED TARGET… Do not re-tune `T1_SHADOW`"*.
**So F67's 3.83e6 px² is real and it is still the largest item on the delivery frame, and F291's
point stands that it was not among the options the owner was shown at rev 72 — but it is CEILED,
it is not new, and it will not satisfy rule 55.** Check its live residue (`hero.py`'s `T1_FX=0` on
the **stitched** path) before spending anything on it.

### **2. THE EMBLEM — THE FREE-ENDPOINT SPINE SHIPPED AT REV 73 (F301). LOOK BEFORE YOU TOUCH IT.**
**`probe_scratch/rev73_emblem_render_ab.png` — the shipped build against the new one, rendered.**
In the OLD build the W's right outer arm is a **DETACHED SLIVER floating inside the ring**, which is
the owner's own F205 (*"the strokes still don't reach the ring"*). **In the new one both outer arms
reach the ring**, the strokes are steeper and more parallel, nothing is fragmented.
`T1_VW_FREE=0` ablates it back to the rev-72 spine exactly.

**WHY IT SHIPPED, AND ON WHAT:** pose-free IoU **+0.0103 fit / +0.0060 independent** (the spine
carries it — the weight alone buys +0.0015 / +0.0003); `probe_rev46_vw`'s **L6 0.1532 against the
photograph's 0.1528**; and **it was rendered, cropped and LOOKED AT** (rule 1, rule 56).

⚠ **WHAT IT COST, AND DO NOT LET THIS GO UNREAD: C4's landmark residual regressed 0.0689 → 0.0745**
against a 0.045 bar it fails either way. §0.07 and F184 hold those L-landmarks *"optimise a quantity
that is not the defect"* and name the pose-free IoU as the objective — **but two photograph-facing
rulers disagree about this change and rev 73 followed one of them.** If you can build a legibility
term (there still is none), that is the tiebreak the objective has always lacked.

⚠ **AND THE WEIGHT IS NOT SETTLED (F302).** It ships at **0.2205**, the LIVE L6 crossing. F204 fixed
0.2283 on TWO agreeing statistics and **rev 73 re-ran only ONE of them** — the ink-inside-band
statistic, which F204 says crosses at 0.2280, **has not been re-run**. Do that before treating
0.2205 as settled. Live L6 also reads **0.1579** at 0.2283 against F204's recorded 0.1530, and
`T1_VW_RES` does not change it.

* **STILL OPEN, AND UNCHANGED BY THIS:** F252's **option (C)** — the 1400-start global search,
  **0.7586 / 0.6698**, *"the only one of the three that improves BOTH frames"* — **is still named in
  no brief and has never been built.** `probe_rev71_emblem.py`, `T1_REV71_SEARCH=ABC`, ~9 min.
  `T1_REV71_SCORE=1` scores a construction on this probe's own targets with the shipped pair as a
  control that REFUSES if it drifts (~2 min).
* Rule 56 still stands: **the objective has no legibility term, and the traced glyph renders as
  SHARDS (F262).** Watch any new term REJECT the traced glyph before trusting a search against it.

### **3. THE NOSE — CLOSED AT REV 73 AS FAR AS A `front` FRAME CAN CLOSE IT (F284/F285). READ THE CEILING BEFORE RE-OPENING IT.**
`probe_rev67_nose.py`'s **P3 now reads the render's bumper edge** — the first render-side reading
this project has had. **BEFORE `rms 113.70 px = 12 % of span, 481 of 481 points clipped, REFUSED`;
AFTER `sagitta +0.45 px ± 0.07 over 640 px, rms 0.81 px, 0 of 340 clipped, ONE EDGE`.**
**⚠ AND REV 73's OWN CENTRAL CEILING WAS TOO STRONG AND ITS OWN ABLATION REFUTED IT (F292/F294).**
`P3w` proves the **WINDOW** is X-blind (100 mm along X moves a window anchor's pixel by
**0.000e+00**), and the first draft slid from that to *"the reading says NOTHING about `BUMP_BOW`"*.
A rule-17 adversary caught the slide: **`T1_BUMP_BOW` had never been run — rule 36 unfired on the
headline row.** It was run, then laddered to six rungs (0.00–2.50), all tracing as ONE EDGE,
two-render floor **0.0026 px**.
**DETECTION YES** — 0.00 against 1.00 is **0.3776 px, 145× the floor, 3.7σ**. The trace IS
bow-sensitive, not geometrically but **PHOTOMETRICALLY**: bowing the blade turns it against the
light and moves the sub-pixel red/cream threshold.
**INVERSION NO** — the first rung is **0.2σ, UNRESOLVED** (⚠ *on the between-render floor alone it
is 7.9× and a real inversion; the two noise models disagree and rev 73 does not know which is
right*), the slope varies **170×** across the range and reverses sign once, and the blow-up's onset
is unconstrained anywhere in **31.6–52.7 mm**. **F231's *"cannot be recovered"* STANDS; what
survives is a REGRESSION DETECTOR.** ⚠ **SHADING IS NOT A RULER — 0.3776 px converts to no
millimetres.** Full table, every sagitta/rms/mesh bow, and the 3/4 route's rule-6 trap:
**`HANDOFF_CARRIERS.md` §0.10**; also `LEDGER_rev73.md` §4b. **DO NOT RE-RUN IT.**

**`P3c` FAILS BY DESIGN on a `front` frame** — 340 of 641 columns, vertex u 839 in the gap
836–847, because the cream V-swage meets the cream bumper at the centreline. **READ ITS MESSAGE.**
**DO NOT ASK HIM THE NOSE AGAIN — both askings are spent (F214/F215).**

### **4. THE GLOSS — F239's PRESCRIPTION IS CLOSED BY MEASUREMENT. DO NOT RE-RUN THIS GRID.**
**Eight configurations of the 3 × 3** of `T1_BODY_RGH` × `T1_REFLENV` (only `(0.060, env 0.0)` was
not rendered), **10 renders in all — 8 `hero34f` plus 2 `side` on the Raw path for the chroma**.
Two-render floor **0.001 spread / 0.002 headroom**:

| `T1_BODY_RGH` → | **0.060** | **0.120** | **0.250** *(shipped)* |
|---|---|---|---|
| **`T1_REFLENV` 0.0** | *(not rendered)* | 0.408 / 0.113 | **0.412 / 0.120** |
| **`T1_REFLENV` 1.0** | 0.410 / 0.116 | 0.411 / 0.116 | **0.416 / 0.126** |
| **`T1_REFLENV` 21.0** | 0.388 / 0.108 | 0.388 / 0.110 | 0.388 / 0.118 |

**F239's *"the binding constraint is the ROUGHNESS"* IS NOT SUPPORTED — AND HERE IS EXACTLY HOW FAR
THAT GOES, BECAUSE THE FIRST DRAFT OF THIS PARAGRAPH OVERSTATED IT AND AN ADVERSARY CAUGHT IT.**
It claimed roughness *"costs spread at EVERY environment level"*. **Against the revision's own
0.001 floor, only TWO steps clear it:** `0.416 → 0.411` at env 1.0 (5× the floor) and
`0.412 → 0.408` at env 0.0 (4×). **At env 21.0 the three cells read `0.388 / 0.388 / 0.388` — no
cost at all**, and `0.411 → 0.410` is exactly one floor. **So the honest statement is: lowering
roughness never HELPS at any environment level, and where it moves the gate at all it moves it
DOWN. That refutes the prescription; it is not a monotone trend across nine cells.**
The only cell above shipped is **environment ALONE at 1.0**, and it is **INVISIBLE**: A/B **2.367 %**
of pixels >8 levels against a **2.044 %** floor, `>32` levels **0.044 % vs 0.043 %**.
**NOTHING SHIPPED.**
**CHROMA COST on F266's Raw path: red linear G/R `0.1091 → 0.1099`.** ⚠ **DO NOT PUT A SINGLE
FIGURE ON THE PHOTOGRAPH'S SIDE OF THAT RATIO. `probe_rev71_red.py` PRINTS THE PROHIBITION ITSELF,
DIRECTLY ABOVE THE NUMBER: *"the photograph's red G/R is 0.0149 .. 0.0344, a 2.3x span. DO NOT
QUOTE A SINGLE FIGURE FOR IT. This span is larger than most of the effects the red has been tuned
against."*** The rev-73 ledger's *"0.0307 … 3.55× the photograph"* inherits that defect and the
multiple is not quotable; **the RENDER-side pair, 0.1091 vs 0.1099, is measured on one window and
is comparable to itself.**

**WHAT IS STILL OPEN: the gate misses by 30 % and neither lever reaches it. F62's own answer —
*"this flank's specular image is white cyclorama 19.3 m away"* — is now the only one left, and the
owner has ruled *"keep studio"* TWICE. If you want to re-open it, ask him; do not just do it.**

### **5. F156 — the `Senor` gate row scores a DELIBERATE DEPARTURE.** ELEVEN revisions unacted (rule 40).

---
## §3 WHAT REV 73 CLOSED — **DO NOT RE-OPEN ANY OF IT**

| closed | the result |
|---|---|
| **THE NOSE'S P3 (F284)** | **WINDOWED AND PASSING.** Window PROJECTED off `hl_ring`/`ind*_lens`/`tyre*` through `studio.views()["front"]`, **never off the bumper**. Kill `T1_NOSE_NOWIN=1` watched; rule-42 and rule-37 refusals watched; true exit codes 2/2/2/1/1. **Two of its own defects caught by its own controls first: the tyres are `tyre1.31` not `tyre.001` (found 0 of 4, REFUSED), and `aim()` leaves `matrix_world` stale (projected to u 1745 on a 1600 px frame).** |
| **F239's UNTRIED PAIRING (§2.4)** | **NULL, and the surviving claim REFUTED.** See §2.4. |
| **`probe_rev71_red.py` (F286)** | Died on a **bare traceback with no summary line** on the command §4 prints. **Rule 9 had nothing to read.** Fixed and watched: rc 3, `0 checked, 0 FAILED, 1 REFUSED`. |
| **F275's "bare" COUNT (F287)** | *"bare → 2 checked"* is the **`--nomesh`** reading; **bare is 4**. Wrong in five carriers **including the guard row written to lock it, which was NAMED "bare" and RAN `--nomesh`**. Renamed + companion row. |
| **THE `BUMP_BOW` LADDER (F294)** | **DETECTION YES, INVERSION NO.** Six rungs, floor 0.0026 px. The slope varies **170×** across the range and reverses sign once; the blow-up's onset is unconstrained anywhere in 31.6–52.7 mm. **F231's *"cannot be recovered"* stands.** What survives is a regression detector at 145× the floor. **DO NOT RE-RUN IT.** |
| **§0.05 ITEM 2, THE RECESS (F295)** | **CANNOT BE BUILT FROM WHAT WE HOLD.** 64 px, 30 × 12, a bent LINE not an area, in one 480 × 320 frame; the primary frame is EDGE-ON and cannot see a face feature at all. Two readings survive and nothing separates them. |
| **§0.05 ITEM 3, THE TILT (F296) — ⚠ HALF RETRACTED SAME REVISION (F300)** | **WHAT STANDS: the RENDER-SIDE CALIBRATION.** The ortho `side` view projects an XZ angle TRUE, and two detectors recover the mesh's own 38.0 from pixels (silhouette 37.995, gradient 38.62). **WHAT IS WITHDRAWN: everything the photograph half said.** Its bracket's span was the detector's own 8° peak-separation constant — 38.0 falls inside at that ONE value and outside at sep 2/4/6/10/12 — and the "second peak" is the FOURTH strongest. **ITEM 3 IS STILL NOT MEASURED.** `probe_rev73_tailboard.py` now reads **5 checked, 1 FAILED — T4 sweeps and REFUSES BY DESIGN**. |
| **THE EMBLEM'S SPINE (F301/F301b)** | **SHIPPED — GEOMETRY, AND VISIBLE.** Free endpoints, `T1_VW_FREE=0` ablates. IoU **+0.0103 / +0.0060** (both frames), L6 **0.1532** vs the photograph's 0.1528, and **rendered and looked at**. **THREE CONTROLS WENT RED AND ALL THREE WERE RIGHT** — the proxy stopped matching the mesh, C12 perturbed a dead constant, C3/C5's baseline collapsed; each repaired at its cause. ⚠ **C4's residual regressed 0.0689 → 0.0745.** |
| **F228's FLOOR** | **RE-MEASURED: 2.044 % / worst 41** on hero34f, against the published 2.441 % / 40. ⚠ F228's frame and view are unrecorded, so say **"2.044 % on hero34f"**, not "F228 was wrong". |

---
## §3b ⚠ REV 72's AND REV 73's FIXES ARE LOCKED. YOU CANNOT REGRESS THEM SILENTLY.

**11 behavioural rows in `verify_clone.sh` and 8 in `bootstrap.sh --guards` from rev 72, plus rev
73's.** They RUN the thing and read what it does (rule 50). **YOU MAY IMPROVE ANY OF IT; YOU MAY NOT
SILENTLY UNDO IT.** A red row is a FINDING ABOUT YOUR CHANGE. A re-base needs the cause NAMED **and**
a companion row making that cause separately testable.

**RUN `./bootstrap.sh --guards` ONCE THIS REVISION** (~10 min, and it BUILDS BLENDER EIGHT TIMES —
**do not run it while the §0 queue is going**, `CLAUDE.md` says do not fan out Blender). It is the
only thing that exercises the five rear-hatch kills. **AT REV 73 IT PAID: it read
`T1_REAR_SEALSTAY=1 → 2 fail` against the rev-73 brief's `# 1 fail` (F288).**

---
## §4 THE MACHINE

```bash
./bootstrap.sh                                # 10 PASS -- read ROW 9
./bootstrap.sh --guards                       # ALL 25 PASS.  NOT while a render queue runs
./verify_clone.sh                             # ALL 418 PASS -- 0 FIDELITY, 402
  # SELF-CONSISTENCY.  READ THE VERDICT BLOCK TOO: not one row measures the vehicle
  # against a photograph, so never quote this total as fidelity
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
python3 photometry.py                         # 9 checked, 0 FAILED
python3 probe_rev67_nose.py out/r74_front.png    # 7 checked, 1 FAILED -- P3c BY DESIGN.
  # PASS IT THE `front` FRAME: it REFUSES any other by name (rule 42).  --nomesh -> 1 ABSENT,
  # because the window is PROJECTED and there is no window without the build (~74 s).
  # BARE reads 4 checked / 1 ABSENT, NOT 2 -- 2 is the --nomesh count (F287).
T1_NOSE_NOWIN=1 python3 probe_rev67_nose.py out/r74_front.png   # THE KILL.  P3 must go RED
python3 gloss_compare.py out/r74_hero34f.png      # PASS IT A FRAME
python3 flank_compare.py out/r74_side.png /tmp/fc.png   # 0.676 (i) at rev 73, NOT 0.689
python3 probe_rev69_fitpose.py                # the emblem.  P1b PASSES; P2 and P4 fail BY
  # DESIGN -- READ P4's MESSAGE, its red is NOT a licence (F262, rule 56)
python3 probe_rev71_emblem.py                 # ⚠ T1_REV71_SEARCH=AB is ~13 MIN, not the 40 s
python3 probe_rev71_proxy.py                  # must read IoU 1.000000
python3 probe_rev71_red.py out/r74_side.png --transform=agx   # REFUSES *with a summary line* now
  # F266's PHYSICS RECIPE: render Raw 16-bit stopped down (T1_VT=Raw T1_LOOK=None T1_EXP=-2.5)
  # and pass --transform=raw.  He asked for physics closed; do not lose the pointer.
  # T1_DIFFB / T1_SPEC / T1_CYCALB / T1_BODY_COAT are the ablations.
python3 probe_rev71_bulbs.py out/r74_side.png # ceiling is DILUTION, not misplacement (F250)
python3 probe_rev72_bits.py out/r74_hero34f.png   # 5 checked, 1 FAILED -- B4 REFUSES BY DESIGN
python3 probe_rev73_tailboard.py             # NEW at rev 73.  5 checked, 0 FAILED.  It
  # CALIBRATES on the mesh's own 38.0 before it reads a photograph, and its T3 row is a
  # 7-degree ROTATION KILL.  Bare it needs a *_side.png in out/ and REFUSES without one
python3 probe_rev70_tyre.py out/r74_side.png ; python3 probe_rev46_vw.py
python3 visibility_budget.py 3840 out/r74_hero34f.png ; python3 revstats.py
T1_SUB=2 /tmp/blender/blender -b -P audit.py            # rewrites STATE.md -- COMMIT FIRST
python3 audit_brief.py ; python3 audit_adversary.py     # rules 15/17, MECHANICAL half only
```

**THE ABLATIONS THAT MAKE GATES REFUSE — `--guards` RUNS ALL OF THESE. The fail counts below are
`--guards`' OWN OUTPUT at rev 73, not typed (F288):**
```bash
T1_REAR_SEAL=0      -> 1 fail      T1_REAR_SEALSTAY=1  -> 2 fail
T1_REAR_NOSWING=1   -> 1 fail      T1_REAR_SEALSHIFT=1 -> 2 fail
T1_REAR_FOLD=1      -> 1 fail      T1_REAR_OPEN=0      -> 0 fail (HONEST close)
T1_REAR_OPEN=-64    -> REFUSES at the parse site, naming the switch (F281)
T1_NOSE_NOWIN=1     -> P3 RED (rev 73, F284)
T1_VW_FREE=0        -> ablates the emblem's free spine back to rev 72's (F301);
                       probe_rev46_vw's L6 goes 0.1532 -> 0.1579 and C12 names
                       VW_W_ARM_X instead of VW_FREE_W_ARM_X
```

**FACTS THAT BITE:** `bootstrap.sh` fails 3/10 without pillow. The render is **not** run-to-run
deterministic — floor **2.044 %** of pixels >8 levels, worst channel 41, on hero34f at 1600×1100/96
spp (F228's published 2.441 %/40 is on an unrecorded frame). `lid_gen.py` / `script_gen.py` are
**not** called by `build.py`. `audit.py` rewrites `STATE.md` — **commit first**, and
`audit_adversary.py` has a row that goes red when `STATE.md` is stale for the geometry. `ck` in
`verify_clone.sh` collapses whitespace. **A backgrounded runner's `rc=$?` is the redirect's — and
so is `rc=$?` after a PIPE, which is how rev 73 first mis-read this probe suite's exit codes.**
`bpy` is a pip module, so most probes run in ~1 s without the Blender CLI.

---
## §5 THE RULES THAT WILL BITE YOU

Full canon in `HANDOFF_CARRIERS.md` §5 — **⚠ WHICH CARRIES RULES 34–58 ONLY. RULES 1–33 ARE IN
`NEXT_CONTEXT_PROMPT_rev50.md` §11**, as that file's own first line says; the rev-73 brief pointed
at the wrong file. **AND §5 CONTAINS TWO DIFFERENT RULE 56s AND TWO DIFFERENT RULE 57s, AND RULE 42
MEANS TWO DIFFERENT THINGS IN LIVE SOURCE** (*"a control's kill is a precondition on its pass"* in
`probe_rev46_vw.py`, *"a control must be framed the way its measurement is framed"* in
`probe_rev67_nose.py`). **UNRESOLVED — do not renumber silently, and say which you mean.**

1. **RENDER IT, CROP IT, AND LOOK AT IT.** Rev 73's P3 passed at rms 0.81 px and the PAINT showed
   the trace broken across the middle — which is the whole of F285.
3. **A control is finished when you have WATCHED IT FAIL.** Rev 73 watched five.
6. **A guard that derives its threshold from the expression it checks is a tautology.** P3w TESTS
   this rather than claiming it.
8. **PAINT THE WINDOW BEFORE THE NUMBER.** Twice this revision it was the paint, not the
   arithmetic, that caught the defect.
9. **READ THE SUMMARY LINE, NOT THE EXIT CODE** — and if a probe has no summary line to read, that
   is a defect in the probe (F286).
12. **Report the measurement WITH ITS CEILING.**
37. **AN ABSENT INPUT MUST NEVER READ AS A MEASUREMENT.**
46. **A REFUTATION INHERITS ITS INSTRUMENT** — F289 is this rule firing on the brief itself.
49. **A DIFFERENCE WITH NO FLOOR UNDER IT IS NOT A MEASUREMENT.**
50. **A GREP IS NOT A REGRESSION TEST** — and neither is a row's NAME (F287).
55. **EVERY REVISION SHIPS A VISIBLE CHANGE TO THE VEHICLE, OR SAYS PLAINLY WHY IT COULD NOT.**
    **REV 73 COULD NOT. SEE THE TOP OF THIS FILE AND `LEDGER_rev73.md`.**
56. **AN INSTRUMENT CAN RANK A THING THE EYE REJECTS, AND IT WILL NOT TELL YOU** (F262).

---
## §6 WHERE EVERYTHING ELSE LIVES

| file | what it holds |
|---|---|
| **`HANDOFF_CARRIERS.md`** | every carrier: the goal, the reference set, §2's refuted emblem routes, §4 the owner's rulings, §5 rules 34–58, the horizon |
| `OPEN_FINDINGS.md` | the register. **F284–F300 are rev 73's** (17 rows; F296's photograph half is retracted by F300 and F285's by F292 — read the annotations, not just the rows). It outranks prose |
| `STATE.md` | machine-written; outranks every prose description. **Regenerate it before trusting a row that reads it — 19 verify rows do** |
| `LEDGER_rev73.md` | what rev 73 did, **and §6, the four things it got wrong in its own work** |
| `photometry.py` | the measurement protocol, with a selftest |
| `SPEC.md`, `REF_MEASUREMENTS.md`, `SURVEY_rev49_photoreal.md`, `ROADMAP_rev68.md`, `PANEL_rev61.md`, `REMAINING_WORK_rev61.md`, `PHOTOS_WANTED_rev49.md`, `PHOTOS_WANTED_rev52.md`, `EMBLEM_HANDOFF.md` | large; load the one the task needs |

**⚠ IDs THIS BRIEF LEANS ON WITHOUT NAMING, SO A GREP FINDS THEM (rule 16): `F282`** the owner's
spent one-revision ruling, **`F252`** the emblem's free-endpoint row and its option (C), **`F246`**
the broken ruler those figures were computed on, **`F277`** the refuted "give it an elevation
frame" prescription, **`F231`** the plan bulge's "cannot be recovered", **`F222`/`F223`** the bumper
as the nose's measured object, **`F283`** the `--guards` false failure rev 72 re-based 4 → 5,
**`F267`** the branch-prose defect §1 exists for, **`F71`** the flat-glazing branch (REFUTED as the
cause of the dark rectangle), **`F254`** the projected pane, **`F21`** paint-or-light, answered by
**`F266`**, **`F143`** the roof loudspeakers.

---
## §7 HOW TO CLOSE

**HIS STANDARD:** photo-real parity with **that exact bus**, in service of a promotional render.
**Any single measurement off is unacceptable** — per-measurement, not on average. **Never call it
done off self-review. Report the measurement with its ceiling. Do not say anything is ready.**

1. `./bootstrap.sh` and `./verify_clone.sh` all-PASS on a **clean** tree.
2. `python3 revstats.py` — **put its geometry/closure line in the ledger header; if the revision
   shipped nothing, say so at the TOP** (rule 55).
3. Regenerate `STATE.md` (`T1_SUB=2 … audit.py`) — **commit first**.
4. **DISPATCH an adversary at the brief you WROTE (rule 17), and one at the brief you RECEIVED
   (rule 15). DO NOT CLOSE UNTIL BOTH REPORT.** At rev 73 the incoming one found **18 defects**,
   six of which became `OPEN_FINDINGS.md` rows and two of which were live code defects.
5. **Keep the split, and KEEP THIS FILE SHORT.** `cp` it over `PASTE_INTO_CLAUDE_CODE.txt` in the
   same commit. `python3 audit_brief.py --fix-count` LAST.

---
**⚠ THIS BRIEF WAS AUDITED AGAINST THE MACHINE, AND BOTH HALVES OF RULE 17 WERE RUN.**

`audit_brief.py` **12 checked, 0 FAILED** — and it FAILED FIRST, on the row count.
`audit_adversary.py` **61 asked, 0 BROKE** — and it BROKE at pickup on *"is `STATE.md` CURRENT for
the geometry? (19 verify rows read it)"*, a staleness inherited from rev 72's close;
`STATE.md` was regenerated and **its diff is three provenance lines and nothing else**, which is the
machine agreeing that rev 73 moved no geometry. **`verify_clone.sh` then failed THREE rows on the
first handoff commit — the modified-tree row, the ranking-rule row and this audit block — every one
a defect in what I had just written, not in the machine.** They are listed here rather than quietly
fixed, because that is the evidence the guards work.

**AND THE RULE-17 ADVERSARY DISPATCHED AT *THIS* FILE RETURNED 18 DEFECTS AND REVERSED THIS
REVISION'S OWN CENTRAL CONCLUSION. TOP FOUR, ALL FIXED BEFORE CLOSE:**
1. **F285's *"P3 says NOTHING about `BUMP_BOW`"* IS REFUTED BY REV 73's OWN ABLATION (F292).**
   `P3w` displaces a **window anchor**, so it proves the WINDOW is X-blind and says nothing about
   the TRACE — and **`T1_BUMP_BOW` had never been run**, rule 36 unfired on the headline row.
   Run: **+0.45 → +0.07 px against a two-render floor of 0.01 px — 38×.** The trace IS bow-sensitive,
   photometrically. **§2.3 now carries the ladder that would calibrate it.**
2. **§2.1 CLAIMED F67 *"has never been in any brief"*. FALSE THREE WAYS** — it is the owner's own
   item D with whole sections in the rev-60 and rev-61 briefs, its figure was printed at rev 71, and
   `HANDOFF_CARRIERS.md` grades it **`CEILED`**. It is also not geometry. **Rewritten, and the
   cheap geometry that WAS available (§0.05 items 2–5) named in its place.**
3. **§2.4 SAID ROUGHNESS *"costs spread at EVERY environment level"*. FALSE ON ITS OWN TABLE** — at
   env 21.0 the three cells are `0.388 / 0.388 / 0.388`, no cost at all, and one other step is
   exactly one floor. **Weakened to the two steps that clear the floor.**
4. **THE PHOTOGRAPH'S RED G/R WAS QUOTED AS A SINGLE FIGURE (0.0307)** against `probe_rev71_red.py`'s
   own printed prohibition, on the same screen: *"0.0149 .. 0.0344, a 2.3x span. DO NOT QUOTE A
   SINGLE FIGURE FOR IT."* **The 3.55× multiple is withdrawn; the render-side pair stands.**

**WHERE THIS BRIEF IS WEAKEST, STATED RATHER THAN HIDDEN:**
* **REV 73 SHIPPED NO GEOMETRY, AND ITS EXPLANATION IS ABOUT THE OWNER'S ITEMS, NOT ABOUT WHAT WAS
  AVAILABLE.** §0.05 items 2–5 were live, unrefuted and needed no new measurement. **This is why it
  *chose not to*, which is not the same as *could not*.** §2.1.
* **F292 ESTABLISHES SENSITIVITY, NOT CALIBRATION. TWO POINTS.** 0.38 px converts to no
  millimetres, the response may not be monotone, and **shading is not a ruler.** The ladder in §2.3
  is a proposal, not a result.
* **P3's WINDOW IS `front`-ONLY AND THE 3/4 EXTENSION HAS A KNOWN TAUTOLOGY IN IT** — the fixtures'
  X follows `NOSE_BULGE` and the bumper's bow is raycast off the same shell, so a 3/4 window would
  move with the quantity it measures. **`HANDOFF_CARRIERS.md` §0.10 carries it in full** *(it was
  dropped from this file by the 32 KB shrink, where it was its only home; a second rule-17 adversary
  caught that — rule 16 firing on the outgoing brief twice in one revision)*.
* **F289b's LEVER IS SCORED BUT NEVER LOOKED AT.** The search completed and all four deltas are
  positive, **but nothing was built, rendered or cropped.** Rule 56's counterexample — the traced
  pressing — scored positive on both frames and renders as shards. **A silhouette IoU at ~220 px
  cannot see fragmentation, and this objective still has no legibility term.**
* **THE GLOSS GRID IS 8 OF 9 CELLS AT ONE FRAME, ONE VIEW, ONE STATISTIC.** Roughness **above**
  0.250 was never tested, and only the one winning cell got a chroma render.
* **THE `--guards` CEILING FROM F283 IS NOT DISCHARGED.** Rev 73 ran the suite and read its rows but
  did **not** audit the remaining count rows against their probes' live output.
* **THE STALE-BRANCH COUNT IS HAND-INCREMENTED AND DERIVED FROM NOTHING** — §1 says nine, the ledger
  said seventh, rev 73's brief said eight. **Do not trust any of them; run the loop.**
* **`revstats.py`'s DOC FIGURE FOR REV 73 IS READ BEFORE THE HANDOFF COMMIT THAT INVALIDATES IT.**
  ~600 lines of doc land after it is measured, against 0 geometry. **Re-run it after this lands.**
* **Every figure quoted from `out/` needs a re-render before you quote it** — `out/` starts empty.
