# NEXT CONTEXT PROMPT — rev 73   ·   **ACTION BRIEF**

**REV 72 SHIPPED GEOMETRY AND ITS DOC/GEO RATIO WENT THE RIGHT WAY. KEEP IT THAT WAY.**
`python3 revstats.py` — **and read ITS numbers, because rev 72 FIXED that script (F273): it had been
double-counting every revision landed by pull request, so every drift figure this project has ever
published off it was wrong.** rev 71's honest doc:geo is **39.44**, not the 35.39 its own brief printed.
Every carrier lives in `HANDOFF_CARRIERS.md`; every finding in `OPEN_FINDINGS.md`; every measurement in
a probe that RUNS. **This file is only what to do next. DO NOT GROW IT.**

> *[owner]* **"finish the nose render, make the emblem correct (a bare minimum qualification) and fix
> the opening"** … **"I meant to say the back opening."**
> *[owner, rev 71]* **"The ultimate goal is a 3d render from which to build promotional material
> from."** and **"I certainly want physics closed."**

**REV 72 DID THE BACK OPENING. THE EMBLEM AND THE NOSE ARE STILL HIS, STILL OPEN, AND THE EMBLEM IS
HIS NINTH REPORT.** Do not let rev 73 be another instrument revision.

---
## §0 DO THIS FIRST — THE MACHINE IS IDLE WHILE YOU READ

```bash
cd /home/user/combi_render
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
pip install pillow             # bootstrap FAILS 3 of 10 without it, EVERY revision
nohup setsid env T1_SUB=1 T1_PREVIEW=front,side,hero34f,hero34r T1_PFX=r73 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r73.log 2>&1 < /dev/null &
```
**`grep -c Saved: /tmp/r73.log` must be 4**, ~5.5 min a frame. `setsid`, not a bare `nohup &` (F173).
**`out/` starts EMPTY** — re-render before quoting any frame. **DO NOT EDIT SOURCE WHILE THE QUEUE
RUNS** (probes and `.md` are fine; `build.py` and the `t1_*` modules are not).
Then `./judge_set.sh r73`.

## §0b BEFORE YOU MEASURE ANYTHING

```bash
python3 photometry.py          # 9 checked, 0 FAILED -- five kills, every one watched
```
**READ LINEAR / REFUSE CLIPPED / MEDIAN NOT MEAN / PAINT THE WINDOW. Import it; do not re-derive it.**

**⚠ AND REV 72 CLOSED THE THING REV 72's BRIEF CALLED ITS BIGGEST GIFT, WITH A NULL (F271).**
The rev-72 brief said re-reading the gates at 16 bits was *"a project-wide re-measurement waiting to
happen, and it is CHEAP"*. **IT IS NOT WORTH DOING.** `probe_rev72_bits.py` re-computes
`gloss_compare.spread()`'s own arithmetic — the shipped function's source, exec'd, agreeing to
1e-12 — changing only the reader: **spread 0.49601 → 0.49292, a move of 0.623 %, on a gate that
misses its bar by 30 %.** And the ratio's other side is an **8-bit JPEG that can never be re-read**
(rule 38). **WHERE IT DOES MATTER IS EXPOSURE, NOT GATE**: B4 stops the same window down and the
divergence is 0.46 % at ×1.0 and 0.07 % at ×0.25 before the mask floor refuses. That is why F266's
dark-channel ratio was decisively wrong at 8 bits and these gates are not. **DO NOT SPEND REV 73 ON IT.**

---
## §1 THE BRANCH — MEASURE IT, DO NOT TRANSCRIBE IT, **INCLUDING THIS SENTENCE**

```bash
git fetch --all --prune
for b in $(git branch -r | grep -v HEAD); do printf "%-52s ahead %-3s behind %s\n" "$b" \
  "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"; done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
```
**EIGHT CONSECUTIVE REVISIONS OF STALE BRANCH PROSE (F253/F267), rev 71's stale within the HOUR and in
the OPPOSITE direction from rev 70's. A BRIEF CANNOT CARRY A TRUE STATEMENT ABOUT BRANCH STATE ACROSS
A BOUNDARY.** Believe `bootstrap.sh` row 9 and the loop above, never this paragraph. **AND F267's own consequence
is now DISCHARGED: `bootstrap.sh` row 9's note used to say *"Carry the number into the handoff"* — the
advice that caused F267 — and rev 72 re-cut it to say the opposite. If your run prints a note telling
you to carry the number, you are on an old tree.**

---
## §2 RANKED WORK FOR REV 73

**RANK BY PIXELS OF THE DELIVERY FRAME** before you choose — `python3 visibility_budget.py 3840
out/r73_hero34f.png` — **but the owner outranks the ranking, and both his open items are below.**
The ranked list is `REMAINING_WORK_rev61.md`, triaged into `ROADMAP_rev68.md`.

### **1. THE EMBLEM — HIS NINTH REPORT, AND THE PRECONDITION IS NOW THE WHOLE JOB.**
**RENDERED AND LOOKED AT AT REV 72, AND THE DEFECT IS PLAIN IN A CROP.** Put
`probe_scratch/r72_emblem_crop.png` beside `probe_scratch/r72_ref_emblem_workshop.png`: **the real
mark's six strokes are STEEP and NEAR-PARALLEL and the mark is mostly open space; ours RADIATE, and
the W's outer arms read as detached slivers.** That is F104, pose-free, confirmed by eye.
**EVERY CHEAP LEVER IS DEAD BY MEASUREMENT OR BY RULING** — the six spine constants are RETIRED BY
OWNER RULING (F234), free endpoints measured **0.0010 WORSE** (F252), the traced pressing renders as
**SHARDS** (F262). **So the route is a NEW CONSTRUCTION, and the objective needs a LEGIBILITY /
STROKE-CONTINUITY term FIRST — and you must WATCH IT REJECT THE TRACED GLYPH** (rule 3, rule 56)
before you trust a search run against it. ⚠ **CEILING ON THAT WARNING: n = 1.** Moving a constant and
LOOKING needs no new term. **Do not let the precondition eat the revision.**

### **2. THE NOSE — IT NOW REFUSES HONESTLY, WHICH IS WHERE REV 72 LEFT IT.**
`probe_rev67_nose.py` bare printed `4 checked, 0 FAILED`, rc 0 while its first line refused —
recorded at rev 70 AND rev 71, fixed at NEITHER, **fixed at rev 72 (F275): now `2 checked, 0 FAILED,
1 ABSENT`, rc 2.** **WHAT IS STILL MISSING IS UNCHANGED: this project has NO render-side reading of
the bumper's edge.** P3 refuses on a three-quarter frame (fit rms ~113 px = 12 % of span, `out/
r72_front.png`) because a whole-frame column scan catches every cream-under-red boundary in the
frame. **Give it a true elevation frame or re-cut the row.** ⚠ It builds the shell in-process (~74 s);
`--nomesh` skips that. **DO NOT ASK HIM THE NOSE AGAIN — both askings are spent (F214/F215).** Check
the catalogue literature first (F229, rule 52); sources named in `HANDOFF_CARRIERS.md` §0.06.

### **3. WHAT REV 72 LEFT ON THE BACK OPENING, STATED SO IT IS NOT RE-DONE.**
`seal_rear` is BUILT and guarded (F268/F269) and **the angle CANNOT be recovered from what we hold —
that is a RESULT, not a task** (F269: `ref_rear34.jpg` shows the rear-third glazing SHUT and sealed,
`ref_side.jpg` is broadside, `IMG_3840.jpeg` is 480×320). **TWO THINGS REMAIN AND BOTH ARE LOOKING
JOBS:** the pane renders **OPAQUE DARK** rather than glazed (`probe_scratch/r72b_backopening.png` —
is that F71's flat glazing, or correct for a dark interior? MEASURE IT, do not name it); and
**§0.05's item 1 is REFUTED (F276) — `tail_board()` is already a 22 mm solid prism. DO NOT give that
board an underside it already has.** Its items 2–5 stand; the **dark angled recess** is genuinely absent.

### **4. F156 — the `Senor` gate row scores a DELIBERATE DEPARTURE.** TEN revisions unacted (rule 40).

---
## §3 WHAT REV 72 CLOSED — **DO NOT RE-OPEN ANY OF IT**

| closed | the result |
|---|---|
| **THE BACK OPENING (F268/F269/F270)** | **SHIPPED.** `seal_rear` built from `windscreen_seals()`'s own section, **no new constant typed**, carried through the SAME `_swing_open` call as the pane — the promise `open_rear_hatch()`'s docstring has carried unkept since rev 48. `T1_REAR_OPEN` / `T1_REAR_SEAL` / `T1_REAR_SEALSTAY` / `T1_REAR_NOSWING`, and `verify._rear_hatch` with **three kills all watched firing**. **CEILING: an INTERNAL-CONSISTENCY fix, not a photographic one, and small at delivery scale.** |
| **THE 16-BIT RE-READ (F271)** | **NULL — 0.623 %.** See §0b. **DO NOT REDO IT.** |
| **`revstats.py` (F273)** | **Double-counted every PR-landed revision.** rev 71: 176 → **88** geometry lines. One merge contributed **1 172** lines of `origin/main` to one revision. **rev 65's 313 collapses to 0.** |
| **F263's ATTRIBUTION (F272)** | **REFUTED by F42's own text** — F42 already said READER, and `shader_solve.py` records a controlled 16-bit decoder written at rev 57 and **never committed**. **F263's SCOPE claim stands.** |
| **`gloss_compare` / `probe_rev67_nose` (F274/F275)** | Both died or went green on an absent input. Both fixed, both watched. |
| **§0.05's "no underside" (F276)** | **REFUTED.** A 22 mm solid prism. It was an edge-on view. |

---
## §4 THE MACHINE

```bash
./bootstrap.sh                                # ALL 10 PASS -- read ROW 9
./verify_clone.sh                             # ALL 381 PASS -- read the verdict block too
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
python3 photometry.py                         # 9 checked, 0 FAILED
python3 probe_rev72_bits.py out/r73_hero34f.png   # NEW at rev 72.  5 checked, 0 FAILED.
                                              # BARE it refuses: 2 ABSENT, rc 2
python3 probe_rev69_fitpose.py                # the emblem.  P1b PASSES; P2 and P4 fail BY DESIGN --
                                              # READ P4's MESSAGE, its red is NOT a licence (F262)
python3 probe_rev71_emblem.py ; python3 probe_rev71_proxy.py   # proxy must read IoU 1.000000
python3 probe_rev67_nose.py out/r73_front.png     # PASS IT A FRAME (--nomesh skips the 74 s build)
python3 gloss_compare.py out/r73_hero34f.png      # PASS IT A FRAME -- it now REFUSES cleanly
python3 flank_compare.py out/r73_side.png /tmp/fc.png
python3 probe_rev70_tyre.py out/r73_side.png ; python3 probe_rev46_vw.py
python3 visibility_budget.py 3840 out/r73_hero34f.png ; python3 revstats.py
T1_SUB=2 /tmp/blender/blender -b -P audit.py            # rewrites STATE.md -- COMMIT FIRST
python3 audit_brief.py ; python3 audit_adversary.py     # rules 15/17, MECHANICAL half only
```

**THE ABLATIONS THAT MAKE GATES REFUSE — RUN THEM, THEY ARE THE ONLY PROOF THE GUARDS WORK:**
```bash
T1_REAR_SEAL=0     T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py   # 1 fail, NO SEAL
T1_REAR_SEALSTAY=1 T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py   # 1 fail, GASKET DRIFT
T1_REAR_NOSWING=1  T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py   # 1 fail, POSE DRIFT
T1_REAR_OPEN=0     T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py   # 0 fail -- HONEST close
```

**FACTS THAT BITE:** `bootstrap.sh` fails 3/10 without pillow. The render is **not** run-to-run
deterministic (floor **2.441 %** of pixels >8 levels, worst channel 40 — publish it beside any A/B).
`lid_gen.py` / `script_gen.py` are **not** called by `build.py`. `audit.py` rewrites `STATE.md` —
commit first. `ck` in `verify_clone.sh` collapses whitespace and **cannot tell a comment from an
assignment**. **A backgrounded runner's `rc=$?` is the redirect's.** `bpy` is a pip module, so most
probes run in ~1 s without the Blender CLI — check before budgeting minutes.

---
## §5 THE RULES THAT WILL BITE YOU

Full canon (1–58) in `HANDOFF_CARRIERS.md` §5.

1. **RENDER IT, CROP IT, AND LOOK AT IT.** Rev 72's emblem finding and its whole back-opening
   diagnosis came from crops, not from any gate.
3. **A control is finished when you have WATCHED IT FAIL.** Rev 72 watched four.
6. **A guard that derives its threshold from the expression it checks is a tautology.**
10. **A CLAIM IN PROSE IS NOT A MEASUREMENT — ASK THE MESH.** It killed §0.05's item 1 at rev 72 (F276).
12. **Report the measurement WITH ITS CEILING.** *"It cannot be recovered"* is a real result (F269).
13. **RETRACT IN THE SAME REVISION YOU FIND THE ERROR.** Rev 72 retracted its own switch (F270).
16. **YOU MUST NOT DELETE A CARRIER.** §0.05 and rule 58 were ANNOTATED at rev 72, not corrected away.
36. **ABLATE THE THING YOU ARE ABOUT TO TUNE, FIRST** — and the ablation must make the gate REFUSE.
    Rev 72's first `verify` draft EXCUSED its own kill and would have shipped a control that can
    never fire.
37. **AN ABSENT INPUT MUST NEVER READ AS A MEASUREMENT.** Two more instances fixed at rev 72.
42. **A CONTROL MUST BE FRAMED THE WAY ITS MEASUREMENT IS FRAMED.** Rev 72's B0 went red on its own
    input framing, not on the gate.
47. **AN ABLATION SWITCH CAN STOP ABLATING — EXERCISE IT.** Rev 72's new switch CRASHED the build on
    its first run while its own comment said it worked.
55. **EVERY REVISION SHIPS A VISIBLE CHANGE TO THE VEHICLE, OR SAYS PLAINLY WHY IT COULD NOT.**
56. **AN INSTRUMENT CAN RANK A THING THE EYE REJECTS, AND IT WILL NOT TELL YOU** (F262).
58. **A LIBRARY CAN THROW AWAY HALF YOUR DATA SILENTLY** — but see F271 for what that is actually
    WORTH on these gates, and F272 for what F263 got wrong about it.

---
## §6 WHERE EVERYTHING ELSE LIVES

| file | what it holds |
|---|---|
| **`HANDOFF_CARRIERS.md`** | every carrier: the goal, the reference set, §2's refuted emblem routes, §4 the owner's rulings, §5 rules 34–58, the horizon. **§0.05 item 1 and rule 58 now carry rev-72 refutations IN PLACE** |
| `OPEN_FINDINGS.md` | the register. **F268–F276 are rev 72's.** It outranks prose. **F261 is `PROVENANCE-REFUTED` — quote F266** |
| `STATE.md` | machine-written; outranks every prose description. `seal_rear` is in it; 229 meshes |
| `LEDGER_rev72.md` | what rev 72 did, **and §4, the four things it got wrong in its own work** |
| `photometry.py` | the measurement protocol, with a selftest |
| `probe_rev72_bits.py` | F271 — what the 16-bit re-read is actually worth, and where |
| `SPEC.md`, `REF_MEASUREMENTS.md`, `SURVEY_rev49_photoreal.md`, `ROADMAP_rev68.md`, `PANEL_rev61.md`, `PHOTOS_WANTED_rev49.md`, `PHOTOS_WANTED_rev52.md`, `EMBLEM_HANDOFF.md` | large; load the one the task needs |

**⚠ IDs THIS BRIEF LEANS ON WITHOUT NAMING, SO A GREP FINDS THEM (rule 16): `F241`** the back opening's
register row, **`F254`** the projected pane, **`F245`** rev 70's chord retraction, **`F242`** the hatch
angle being a POSE not a dimension, **`F134`** the bulbs' null, **`F21`** paint-or-light, answered by
**`F266`**, **`F265`** the paint-over-evidence row, **`F267`** the stale-branch recurrence.

---
## §7 HOW TO CLOSE

**HIS STANDARD:** photo-real parity with **that exact bus**, in service of a promotional render. **Any
single measurement off is unacceptable** — per-measurement, not on average. **Never call it done off
self-review. Report the measurement with its ceiling. Do not say anything is ready.**

1. `./bootstrap.sh` and `./verify_clone.sh` all-PASS on a **clean** tree.
2. `python3 revstats.py` — **put its geometry/closure line in the ledger header; if the revision
   shipped nothing, say so at the top** (rule 55).
3. Regenerate `STATE.md` (`T1_SUB=2 … audit.py`) — **commit first**.
4. **DISPATCH an adversary at the brief you WROTE (rule 17), and one at the brief you RECEIVED
   (rule 15). DO NOT CLOSE UNTIL BOTH REPORT.** At rev 71 the outgoing adversary reversed the
   revision's central conclusion; at rev 72 the incoming one found **13 defects**, four of which
   became this brief's §3 rows.
5. **Keep the split, and KEEP THIS FILE SHORT.** `cp` it over `PASTE_INTO_CLAUDE_CODE.txt` in the
   same commit. `python3 audit_brief.py --fix-count` LAST.

---
**⚠ THIS BRIEF WAS AUDITED AGAINST THE MACHINE, AND BOTH HALVES OF RULE 17 WERE RUN.**

`audit_brief.py` **10 checked, 0 FAILED** — and it FAILED FIRST, on `LEDGER_rev72.md` being named
before it was tracked. `audit_adversary.py` **61 asked, 1 BROKE**, and the break was real: *"is the
ranked work list still named by README, START_HERE and the brief?"* — **this file's first draft had
dropped `REMAINING_WORK_rev61.md`, which is rule 16 firing on the outgoing brief.** Restored above.
**`verify_clone.sh` then failed FIVE rows on the first handoff commit** — the mesh count, this audit
block, the ranking rule, the carrier name and the row count — **every one of them a defect in what I
had just written, not in the machine.** They are listed here rather than quietly fixed, because that
is the evidence the guards work.

**WHERE THIS BRIEF IS WEAKEST, STATED RATHER THAN HIDDEN:**
* **`seal_rear` IS SMALL AT DELIVERY SCALE.** It reads as a framed hatch where there was a frameless
  sheet (`probe_scratch/r72_seal_ab.png`). It is an INTERNAL-CONSISTENCY fix, not a photographic one,
  and rev 72 **could not assign** the sealed window in `ref_rear34.jpg` to the rear panel rather than
  the rearmost flank bay. **The model-side fact is certain; the photographic one is not.**
* **THE PANE STILL RENDERS OPAQUE DARK** and rev 72 did not establish why. §2.3.
* **F271's NULL IS MEASURED ON ONE GATE'S STATISTIC**, on a window whose median sits at 106/255.
  B4's ladder characterises the exposure dependence but **refuses below ×0.25** because the mask's own
  `L>25` floor bites — so the DARK regime is bounded by refusal, not by measurement. Do not read the
  null as covering a dark-channel ratio; F266 is the case where 8 bits was decisively wrong.
* **`REAR_OPEN_DEG`'s ±2.0° guard band is WIDER than anything that has been watched to move it.**
  The shipped build reads 64.00 against 64.0. The band exists so a re-rake cannot trip the row; it is
  not evidence that the angle is right, and the angle is still NOT MEASURED.
* **`audit_adversary.py` STILL PRINTS `ok` ON QUESTIONS WHOSE TEXT ASSERTS REFUTED STATES** — the
  overfit-detector question still quotes F255's withdrawn *"LOSES by 0.0249"*, and the traced-pressing
  question still says *"RENDERS AS AN UNRECOGNISABLE BLOB"* against F262's shards. **Rule 50 recorded
  this shape at rev 68 and it is live at rev 73.** The rev-63 batch is the oldest and is next.
* **Every figure quoted from `out/` needs a re-render before you quote it** — `out/` starts empty.
