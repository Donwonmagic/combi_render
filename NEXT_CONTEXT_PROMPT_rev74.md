# NEXT CONTEXT PROMPT — rev 74   ·   **ACTION BRIEF**

**REV 73 SHIPPED NO GEOMETRY. `revstats.py` SAYS `73 | 0 geometry | 476 instrument | 0 closed`, AND
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
own designated branch was DELETED from the remote.** **NINE CONSECUTIVE REVISIONS OF STALE BRANCH
PROSE. Believe row 9 and the loop, never this paragraph.**

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
**THE RANKING'S OWN #1 ITEM HAS NEVER BEEN IN ANY BRIEF: `F67`, THE CONTACT SHADOW'S FOOTPRINT ON
THE GROUND, `3.83e6 px²` — 1.33× the whole gloss aggregate and 115× the emblem (F291).**
`HANDOFF_CARRIERS.md` §0.09 has carried it since rev 69 and no brief has named it. It was **not**
among the options the owner was shown at rev 72. **Check it against the frame before ranking it —
`visibility_budget.py`'s own ceiling says pixels are not visibility — but do not let a third
revision pass without geometry.** Also unbuilt and cheap: the tyres' TREAD, the tail's barrel, the
shut lines, **F143 the roof loudspeakers (unmodelled for 57 revisions)**.

### **2. THE EMBLEM — HIS NINTH REPORT, AND REV 73 FOUND THE BRIEF HAD BURIED A LIVE LEVER (F289).**
**DO NOT REPEAT *"EVERY CHEAP LEVER IS DEAD"*. IT IS NOT TRUE AS WRITTEN.**
* The rev-73 brief printed *"free endpoints measured **0.0010 WORSE** (F252)"* **while F252's own
  row says *"EVERY FIGURE IN THIS ROW WAS COMPUTED ON THE BROKEN RULER (F246) AND HAS NOT BEEN
  RE-RUN ON THE REPAIRED ONE."*** Measured: `grep -c "0.0010 WORSE"` → **1**,
  `grep -c "BROKEN RULER"` → **0**. The figure travelled; its ceiling did not (rule 46).
* **F252's OPTION (C) IS NAMED IN NO BRIEF AT ALL** — the 1400-start global search, **0.7586 fit /
  0.6698 independent**, *"the only one of the three that improves BOTH frames"*, **never shipped**.
  `probe_rev71_emblem.py`, `T1_REV71_SEARCH=ABC`.
* **⚠ AND THE ONE THING REV 73 DID NOT VERIFY: an adversary re-ran `T1_REV71_SEARCH=AB` and reports
  the free-endpoint lever at `+0.0056 / +0.0090`, BOTH POSITIVE — the sign REVERSES.** F289 grades
  that **`INHERITED`** on purpose. **RE-RUN IT BEFORE YOU ACT ON IT.** ⚠ **Budget ~13 MINUTES, not
  the "~40 s" the probe's own comment claims.**
* Rule 56 still stands: **the objective has no legibility term, and the traced glyph renders as
  SHARDS (F262).** Watch any new term REJECT the traced glyph before trusting a search against it.

### **3. THE NOSE — CLOSED AT REV 73 AS FAR AS A `front` FRAME CAN CLOSE IT (F284/F285). READ THE CEILING BEFORE RE-OPENING IT.**
`probe_rev67_nose.py`'s **P3 now reads the render's bumper edge** — the first render-side reading
this project has had. **BEFORE `rms 113.70 px = 12 % of span, 481 of 481 points clipped, REFUSED`;
AFTER `sagitta +0.45 px ± 0.07 over 640 px, rms 0.81 px, 0 of 340 clipped, ONE EDGE`.**
**⚠ AND IT CANNOT SEE THE PLAN BOW, WHICH `P3w` MEASURES RATHER THAN ASSERTS: a 100 mm X
displacement of a window anchor moves its pixel by 0 under the front ORTHOGRAPHIC camera. The bow
is an X quantity.** So +0.45 px is the edge's curvature **IN ELEVATION** and says nothing about
`BUMP_BOW`. **THE HALF REV 73 DID NOT SPEND, AND IT IS THE ACTIONABLE ONE:** P2's ceiling says a
three-quarter frame cannot separate plan bow from elevation curvature. **A `front` frame measures
the ELEVATION term ALONE. Build the three-quarter render-side reading and SUBTRACT IT.** That is a
real route to `BUMP_BOW`, and F231's *"cannot be recovered"* was never tested against it.
**`P3c` FAILS BY DESIGN on a `front` frame** — 340 of 641 columns, vertex u 839 in the gap
836–847, because the cream V-swage meets the cream bumper at the centreline. **READ ITS MESSAGE.**
**DO NOT ASK HIM THE NOSE AGAIN — both askings are spent (F214/F215).**

### **4. THE GLOSS — F239's PRESCRIPTION IS CLOSED BY MEASUREMENT. DO NOT RE-RUN THIS GRID.**
Eleven renders, the full 3 × 3 of `T1_BODY_RGH` × `T1_REFLENV`, two-render floor **0.001 / 0.002**:

| `T1_BODY_RGH` → | **0.060** | **0.120** | **0.250** *(shipped)* |
|---|---|---|---|
| **`T1_REFLENV` 0.0** | — | 0.408 / 0.113 | **0.412 / 0.120** |
| **`T1_REFLENV` 1.0** | 0.410 / 0.116 | 0.411 / 0.116 | **0.416 / 0.126** |
| **`T1_REFLENV` 21.0** | 0.388 / 0.108 | 0.388 / 0.110 | 0.388 / 0.118 |

**F239's *"the binding constraint is the ROUGHNESS"* IS REFUTED: lowering roughness costs spread at
EVERY environment level** (0.412→0.408; 0.416→0.411→0.410; 0.388→0.388→0.388). The only cell above
shipped is **environment ALONE at 1.0**, and it is **INVISIBLE**: A/B **2.367 %** of pixels >8
levels against a **2.044 %** floor, `>32` levels **0.044 % vs 0.043 %**. Chroma cost on F266's Raw
path: red linear G/R **0.1091 → 0.1099** (photograph 0.0307). **NOTHING SHIPPED.**
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
./verify_clone.sh                             # read the verdict block too
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
python3 photometry.py                         # 9 checked, 0 FAILED
python3 probe_rev67_nose.py out/r74_front.png    # 7 checked, 1 FAILED -- P3c BY DESIGN.
  # PASS IT THE `front` FRAME: it REFUSES any other by name (rule 42).  --nomesh -> 1 ABSENT,
  # because the window is PROJECTED and there is no window without the build (~74 s).
  # BARE reads 4 checked / 1 ABSENT, NOT 2 -- 2 is the --nomesh count (F287).
T1_NOSE_NOWIN=1 python3 probe_rev67_nose.py out/r74_front.png   # THE KILL.  P3 must go RED
python3 gloss_compare.py out/r74_hero34f.png      # PASS IT A FRAME
python3 flank_compare.py out/r74_side.png /tmp/fc.png   # 0.676 (i) at rev 73, NOT 0.689
python3 probe_rev69_fitpose.py                # the emblem.  P2 and P4 fail BY DESIGN
python3 probe_rev71_emblem.py                 # ⚠ T1_REV71_SEARCH=AB is ~13 MIN, not the 40 s
python3 probe_rev71_proxy.py                  # must read IoU 1.000000
python3 probe_rev71_red.py out/r74_side.png --transform=agx   # REFUSES *with a summary line* now
  # F266's PHYSICS RECIPE: render Raw 16-bit stopped down (T1_VT=Raw T1_LOOK=None T1_EXP=-2.5)
  # and pass --transform=raw.  He asked for physics closed; do not lose the pointer.
  # T1_DIFFB / T1_SPEC / T1_CYCALB / T1_BODY_COAT are the ablations.
python3 probe_rev71_bulbs.py out/r74_side.png # ceiling is DILUTION, not misplacement (F250)
python3 probe_rev72_bits.py out/r74_hero34f.png   # 5 checked, 1 FAILED -- B4 REFUSES BY DESIGN
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
| `OPEN_FINDINGS.md` | the register. **F284–F291 are rev 73's.** It outranks prose |
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
