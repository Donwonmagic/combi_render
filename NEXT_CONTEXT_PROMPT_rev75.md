# NEXT CONTEXT PROMPT — rev 75   ·   **ACTION BRIEF**

**REV 74 SHIPPED GEOMETRY: THE TYRE'S TRANSVERSE TREAD (F308).** `t1_detail.tyre()` returned
`T.revolve(...)` — **rotationally symmetric BY CONSTRUCTION**, so its four grooves are
CIRCUMFERENTIAL rings and the transverse lugs the photograph shows were **not a free parameter of
the model at all** (rule 54, second time in this project). 64 grooves are cut INWARD from the crown;
`T1_TYRE_TREAD=0` restores the rev-73 tyre exactly. **Run `python3 revstats.py` and read ITS
numbers.** Every carrier lives in `HANDOFF_CARRIERS.md`; every finding in `OPEN_FINDINGS.md`; every
measurement in a probe that RUNS. **This file is only what to do next. DO NOT GROW IT.**

> *[owner, rev 74, shown `probe_scratch/rev74_weight_ask.png`]* **"I can't tell them apart — stop
> tuning the weight."** — **F314. THE WEIGHT IS *UNRESOLVED*, NOT SETTLED. DO NOT RE-ASK IT.**
> *[owner, rev 71]* **"The ultimate goal is a 3d render from which to build promotional material
> from."** and **"I certainly want physics closed."**
> *[owner, rev 72]* **"set up for success so that it can only carry forward, no regression allowed."**

**THE EMBLEM IS STILL HIS NINTH REPORT AND IT IS STILL WRONG. F191 AND F234 BOTH STAND.**

---
## §0 DO THIS FIRST — THE MACHINE IS IDLE WHILE YOU READ

```bash
cd /home/user/combi_render
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
pip install pillow             # bootstrap FAILS 3 of 10 without it, EVERY revision
nohup setsid env T1_SUB=1 T1_PREVIEW=front,side,hero34f,hero34r T1_PFX=r75 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r75.log 2>&1 < /dev/null &
```
**`grep -c Saved: /tmp/r75.log` must be 4**, ~5.5 min a frame. `setsid`, not a bare `nohup &` (F173).
**`out/` starts EMPTY** — re-render before quoting any frame. **DO NOT EDIT SOURCE WHILE THE QUEUE
RUNS** (probes and `.md` are fine; `build.py` and the `t1_*` modules are not).

## §0b BEFORE YOU MEASURE ANYTHING
```bash
python3 photometry.py          # 9 checked, 0 FAILED
```
**READ LINEAR / REFUSE CLIPPED / MEDIAN NOT MEAN / PAINT THE WINDOW. Import it; do not re-derive it.**

---
## §1 ⚠ **`bootstrap.sh` WILL STOP ON YOU AT PICKUP, AND IT IS NOT YOUR FAULT — FIX IT FIRST (F311)**

At rev 74's pickup, on a **clean tree, before anything was touched**: `bootstrap.sh` read
**9 PASSED, 1 FAILED** and `verify_clone.sh` read **417 PASSED, 6 FAILED**.

**FOUR ARE ONE CAUSE — NOT FIVE, AND THE DIFFERENCE MATTERS.** The `F296`/`F300` rows run
`python3 probe_rev73_tailboard.py` and grep for its PASS lines — but **that probe needs a
`*_side.png` in `out/`, and `out/` is untracked and starts EMPTY**, so it correctly prints
`0 checked, 0 FAILED, 2 ABSENT — no side render` (rule 37) and every grep returns 0.
⚠ **BUT THE FIFTH — `ck "F296 ... and the 7-degree ROTATION KILL fires"` — STAYS RED EVEN WITH A
FRAME, BECAUSE T3 IS GENUINELY FAILING (F312/F312b). DO NOT RE-BASE IT: it is correctly reporting a
failure.**

**AND THE COUNT ROW CANNOT AGREE WHILE ANY OTHER ROW IS RED — BY CONSTRUCTION, NOT BY DEFECT.** It
is `ck "…" "$((PASS+1))" "$_BRIEF_TOTAL"`, so `PASS` drops by one for every red row and the row
misses by exactly that many. **On this tree it reads `got 428, want 427`: 428 is the ALL-PASS total
that `audit_brief.py --fix-count` wrote, and the 1 is the ROTATION KILL.** ⚠ **DO NOT "FIX" IT BY
WRITING 427 — that would encode today's failure as the target and break the row the moment T3 is
repaired.** The gap is a live count of genuine reds, and reading it that way is more useful than
making it green. The sixth is `ck "newest brief states THIS script's row count" "$((PASS+1))"`, which can
only agree once the rest are green. With a side frame present the script reads **421 PASSED,
2 FAILED** — 417 + 4, which is the arithmetic that gives the fifth row away.

**THIS IS F307's SHAPE ONE LEVEL UP.** F307 taught `audit_brief.py` to SKIP a probe that wants a
frame; **nobody checked whether `verify_clone.sh` had the same rows, and it has five that HARD-FAIL
rather than skip.** `verify_clone.sh`'s own header claims it needs *"no render … and `out/` is
untracked and starts EMPTY"* — **false for these five rows.**
**REV 74 RECORDED IT AND DID NOT PATCH IT**, because the repair is a re-base of five rows and needs
the cause NAMED plus companion rows. **That is rev 75's first job.** `probe_rev74_tread.py`'s **T6**
is the worked example: it SKIPS with a message when `out/` has no side frame.

**AND MEASURE THE BRANCH, DO NOT TRANSCRIBE IT, INCLUDING THIS SENTENCE:**
```bash
git fetch --all --prune
for b in $(git branch -r | grep -v HEAD); do printf "%-52s ahead %-3s behind %s\n" "$b" \
  "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"; done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
```
**At rev 74 the designated branch again had NO REMOTE COPY at pickup (F317) — second revision
running. Nothing was stranded: row 9 PASSED, all 27 remote branches `ahead 0`, the diff empty.**
**The "N consecutive revisions" count in every brief is HAND-INCREMENTED AND DERIVED FROM NOTHING.
Believe row 9 and the loop, never a sentence.**

---
## §2 RANKED WORK FOR REV 75

**RANK BY PIXELS OF THE DELIVERY FRAME** — `python3 visibility_budget.py 3840 out/r75_hero34f.png` —
**and the owner outranks the ranking.** ⚠ **READ THAT TABLE'S OWN CEILING: *"pixels are not
visibility … catch ORDERS OF MAGNITUDE, not rank neighbours."*** The ranked list is
`REMAINING_WORK_rev61.md`, triaged into `ROADMAP_rev68.md`.

### **1. FIX §1's SIX RED ROWS.** Cheap, and it unblocks every future pickup. See §1.

### **2. SHIP GEOMETRY. RULE 55 IS STILL THE BINDING CONSTRAINT.**
⚠ **AND CHECK THE GROUNDING BEFORE YOU BUILD — THAT IS THE LESSON REV 74 PAID FOR TWICE.**
**F143's roof loudspeakers are now RETIRED as a geometry item (F309): they are a POSE.** The
identification was right, but **three frames of the same vehicle show the roof BARE** — decisively
`ref_playa_34.png`, **the same location** as `ref_rear34.jpg`. Building it would plant removable
event gear permanently into every delivery frame. `probe_scratch/r74_F143_grounding.png`.
**So the live geometry candidates are: the tail's barrel, the shut lines, the glass, and the tyre
tread's own open constants (§2.3).** Check each one's grounding FIRST.

### **3. THE TREAD'S COUNT, DEPTH AND DUTY ARE ALL DECLARED, NOT MEASURED (F308b).**
`probe_rev74_tread.py`'s **T2 REFUSES to publish a count** and prints six estimates instead —
**peak 55 / fft 64 / peak 61 / fft 74 / peak 48 / fft 84**, a **48..84 bracket** (1.73× on the unrounded floats the probe prints; 84/48 = 1.75 on the rounded ones — **quote the bracket, not the ratio**) — because two
independent methods disagree by ~30 % and each moves with the radius. The pitch is **~3 px in a
500×400 frame**. **`TREAD_LUGS = 64` has exactly the standing of `TB_WIDTH`'s "POSE CHOICE, NOT
MEASURED".** ⚠ **AND THE FIRST CUT SHIPPED AN IRREGULAR TREAD — 99 of 384 cut in runs of 1 AND 2,
because the phase threshold left the LEADING edge on the modulo wrap with zero margin (F319).
Fixed, and T7 now MEASURES the regularity rather than trusting the comment.** ⚠ **DO NOT QUOTE 64 AS A MEASUREMENT, and do not read T6's recovery of 64 from the
render as confirmation of it — that is rule 6.** **What would close it is a CLOSER TYRE FRAME, and
`PHOTOS_WANTED` has never had a tyre item. Consider adding one.**

### **4. THE EMBLEM.** His ninth report. P2 crossed its 0.85 bar at **0.8528** against P1b's own
ceiling of **0.9465**, so it is still ~0.09 short, and **the objective still has no legibility term**
(rule 56). **The weight is closed to further tuning by F314 but is NOT resolved** — F302 and F303
both stand. **F252's option (C)** — the 1400-start global search, **0.7586 / 0.6698** — is still
built by nobody; ⚠ **and every figure in that row was computed on the BROKEN RULER (F246) and has
never been re-run** (F316b(d): the rev-74 brief carried those figures without that ceiling, which is
F289 recurring).

### **4b. THE TREAD'S ONE MEASURED COST IS OPEN (F318).** `probe_rev70_tyre.py`'s T2 moved
**0.2457 → 0.2522** (1.26× → 1.29×) — **16× its measured two-render floor of 0.0004**, so real; but
**2.6 % against the probe's own `±20 %` ceiling**, and **its painted band straddles the wheel-arch
shadow and the outer silhouette** (`probe_scratch/rev70_tyre_render.png`), so the mechanism is NOT
established. ⚠ **DO NOT "FIX" IT BY LOWERING `T1_TYRE_FILM`** — that tunes shading to mask geometry
and leaves the ablation too dark. **Give T2 a band MEASURED to lie inside the rubber (paint it
first) and re-read both frames.**

### **5. F156 — the `Senor` gate row scores a DELIBERATE DEPARTURE.** TWELVE revisions unacted (rule 40).

---
## §3 WHAT REV 74 CLOSED — **DO NOT RE-OPEN ANY OF IT**

| closed | the result |
|---|---|
| **THE TYRE'S TREAD (F308)** | **SHIPPED — GEOMETRY, AND IT REACHES THE RENDER.** T3 goes **0.0000 → 0.0060 m**; T4's KILL WATCHED restoring the revolve; T5 reads `TYRE_D` unmoved to **5.56e-10 m** (grooves cut INWARD, so a locked dimension cannot move *by construction*). `VERIFY: 0 fail, 0 warn`. |
| **IS IT VISIBLE? (F308)** | **THE PIXEL-DIFF STATISTIC IS A FLAT NULL — INCLUDING LOCALLY.** front wheel `4.418 %` change vs `4.372 %` box-local floor = **1.01×**; rear **1.04×**; whole frame **1.00×**. ⚠ **I read the painted diff's two bright wheel rings as localisation and the box floor REFUTED it — they are a noise feature.** **WHAT SEES IT IS STRUCTURAL: the rendered silhouette's angular rms goes 0.0503 → 0.5286 px at exactly 64 cycles/rev, amplitude 4 → 161 (on `out/r74f_side.png`; the irregular first cut read 0.4499 / 130). ⚠ **THE FLOOR IS A RECORDED READING, NOT ONE ANY ROW RECOMPUTES (F320f)** — it was read once on a frame of the ablated tree that is not retained, so `0.0503 / 4` are STRING LITERALS in T6's message, which now says so. **Re-derive them with one `T1_TYRE_TREAD=0` render before quoting.** The *reasoning* is sound (a revolve has no angular structure); the *figures* are unverified.** |
| **F143, THE ROOF LOUDSPEAKERS (F309)** | **RETIRED AS A GEOMETRY ITEM — IT IS A POSE.** 57 revisions of the record called it *"an unmodelled object"* without anyone checking whether it belongs to the vehicle. ⚠ **And its second frame is not an independent sighting**: that crop sits where the mural board, its frame, its bulb string and the roof all overlap. |
| **THE OWNER'S WEIGHT QUESTION (F313/F314/F315)** | **ASKED AND ANSWERED.** The crop the rev-74 brief pointed at was **stale** (captioned `SHIPPED wfrac 0.2283`; 0.2205 ships) **and compared an oblique photograph against head-on masks** — F184's trap. Rebuilt in one projection. **And fitting each candidate to its own pose inflated the A/B from 89 px / 2.83 % to 226 px / 7.20 % — more than half the apparent disagreement was POSE.** |
| **MY OWN HEADLINE ROW (F310)** | **WRONG FIRST TIME, CAUGHT BY WATCHING IT FAIL.** T3's first cut pooled every crown vertex and read the PROFILE's radial variation — a confident `0.0119 m` PASS on a tyre that IS a revolve. Fixed by binning on exact `y`. **Written after the build it would have passed for the wrong reason and guarded nothing.** |

---
## §3b ⚠ REV 72's, 73's AND 74's FIXES ARE LOCKED. YOU CANNOT REGRESS THEM SILENTLY.

They RUN the thing and read what it does (rule 50). **YOU MAY IMPROVE ANY OF IT; YOU MAY NOT SILENTLY
UNDO IT.** A red row is a FINDING ABOUT YOUR CHANGE. A re-base needs the cause NAMED **and** a
companion row making that cause separately testable. **§1's six rows are the one exception already
diagnosed — fix them with the cause named, per F311** (and read F312b before touching the fifth).
**Rev 74 added FIVE rows of its own** covering the tread: the probe's clean run, the mesh reading
that the tyre is not a revolve, the `T1_TYRE_TREAD=0` KILL, the tread's REGULARITY (128 of 384), and
T5b's distinction between the max radius and the bbox extent `verify.py` actually locks. **They are
deliberately FRAME-INDEPENDENT so they cannot repeat F311.**

**RUN `./bootstrap.sh --guards` ONCE THIS REVISION** (~10 min, and it BUILDS BLENDER EIGHT TIMES —
**not while the §0 queue is going**). It is the only thing that exercises the five rear-hatch kills.

---
## §4 THE MACHINE

```bash
./bootstrap.sh                                # READ ROW 9
./bootstrap.sh --guards                       # NOT while a render queue runs
./verify_clone.sh                             # ALL 428 PASS -- 0 FIDELITY, 428 SELF-CONSISTENCY.
  # ⚠ AND THAT TOTAL IS NOT REACHED ON A CLEAN CLONE, WHICH IS §1's WHOLE SUBJECT: four rows
  # want a rendered frame, one is correctly reporting a real failure (F312b), and the count
  # row can only agree once the rest are green.  READ THE VERDICT BLOCK TOO: not one row
  # measures the vehicle against a photograph, so NEVER quote this total as fidelity
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
python3 photometry.py                         # 9 checked, 0 FAILED
python3 probe_rev74_tread.py out/r75_side.png   # NEW at rev 74.  8 checked, 0 FAILED.
  # NAME YOUR FRAME: with no argument it takes the alphabetically-last out/*_side.png and
  # PRINTS which -- rev 74 attributed a reading to a frame a probe could not have read
  # (F320c).  Bare, with an empty out/, T6 SKIPS and says so: 7 checked, 0 FAILED, 1 ABSENT
  # -- the pattern §1 wants, and why verify_clone's five new tread rows pin FAILED not CHECKED
T1_TYRE_TREAD=0 python3 probe_rev74_tread.py  # THE KILL.  T3 must go RED (0.0000 m)
python3 probe_rev67_nose.py out/r75_front.png
  # ⚠ THE REV-74 BRIEF SAID "7 checked, 1 FAILED -- P3c BY DESIGN".  ON out/r74_front.png IT
  # READ 7 checked, 0 FAILED AND P3c PASSED (F316).  THE OUTCOME IS FRAME-DEPENDENT.  NAME
  # YOUR FRAME AND READ THE ROWS -- do not assume a red P3c is by design
python3 probe_rev73_tailboard.py              # ⚠ 5 checked, **2** FAILED on out/r74_side.png --
  # T3 (a WATCHED KILL, bar 1.5, the -7.0 rung misses at 1.75) AND T4.  The rev-74 brief said
  # 1.  Cause NOT established: no source moved, rev 73's frame is gone, and T3's bar has no
  # floor under it.  TWO side renders of ONE tree would settle it (F312)
python3 probe_rev46_vw.py                     # 12 checked, 2 FAILED -- C4 AND C10 (F304)
python3 probe_rev69_fitpose.py                # 5 checked, 1 FAILED -- P4 only.  ⚠ P1's MESSAGE
  # hardcodes a 0.9703 ceiling while P1b prints 0.9465; read the NUMBERS, not the prose
python3 gloss_compare.py out/r75_hero34f.png ; python3 flank_compare.py out/r75_side.png /tmp/fc.png
  # ⚠ flank_compare read 0.688 on out/r74_side.png, NOT the 0.676 the rev-74 brief printed
python3 probe_rev71_proxy.py                  # must read IoU 1.000000
python3 probe_rev71_red.py out/r75_side.png --transform=agx   # REFUSES with a summary line
  # F266's PHYSICS RECIPE: T1_VT=Raw T1_LOOK=None T1_EXP=-2.5, then --transform=raw
python3 probe_rev70_tyre.py out/r75_side.png ; python3 probe_rev46_vw.py
python3 visibility_budget.py 3840 out/r75_hero34f.png ; python3 revstats.py
T1_SUB=2 /tmp/blender/blender -b -P audit.py            # rewrites STATE.md -- COMMIT FIRST
python3 audit_brief.py ; python3 audit_adversary.py     # rules 15/17, MECHANICAL half only
```

**THE ABLATIONS THAT MAKE GATES REFUSE.** ⚠ **`--guards` RUNS ONLY THE `T1_REAR_*` BLOCK — the four
below it are HAND-RUN, and the rev-74 brief's heading claimed otherwise for three of them
(`grep -n "TYRE_TREAD\|NOSE_NOWIN\|VW_FREE" bootstrap.sh` finds nothing). Corrected here rather than
inherited:**
```bash
T1_REAR_SEAL=0      -> 1 fail      T1_REAR_SEALSTAY=1  -> 2 fail
T1_REAR_NOSWING=1   -> 1 fail      T1_REAR_SEALSHIFT=1 -> 2 fail
T1_REAR_FOLD=1      -> 1 fail      T1_REAR_OPEN=0      -> 0 fail (HONEST close)
T1_REAR_OPEN=-64    -> REFUSES at the parse site, naming the switch (F281)
T1_NOSE_NOWIN=1     -> P3 RED (F284)
T1_VW_FREE=0        -> ablates the emblem's free spine to rev 72's (F301)
T1_TYRE_TREAD=0     -> NEW at rev 74.  probe_rev74_tread's T3 goes 0.0060 -> 0.0000 m,
                       and the tyre is a surface of revolution again (F308).
                       verify_clone.sh RUNS this one -- it is the row that stops
                       _cut_tread being deleted silently
```

**FACTS THAT BITE:** `bootstrap.sh` fails 3/10 without pillow. The render is **not** run-to-run
deterministic — floor **~2.04 %** of pixels >8 levels on hero34f at 1600×1100/96 spp, **and take the
floor IN THE BOX YOU ARE READING: it is 4.37 % inside the front-wheel box and 7.90 % on the body**
(F308). `lid_gen.py` / `script_gen.py` are **not** called by `build.py`. `audit.py` rewrites
`STATE.md` — **commit first**. `ck` in `verify_clone.sh` collapses whitespace. **A backgrounded
runner's `rc=$?` is the redirect's.** `bpy` is a pip module, so most probes run in ~1 s.

---
## §5 THE RULES THAT WILL BITE YOU

Full canon in `HANDOFF_CARRIERS.md` §5 — **⚠ WHICH CARRIES RULES 34–58, THOUGH ITS OWN FIRST LINE
SAYS 34–52. RULES 1–33 ARE IN `NEXT_CONTEXT_PROMPT_rev50.md` §11.** **AND §5 CONTAINS TWO DIFFERENT
RULE 56s AND TWO DIFFERENT RULE 57s, AND RULE 42 MEANS TWO DIFFERENT THINGS IN LIVE SOURCE.**
**UNRESOLVED — do not renumber silently, and say which you mean.**

1. **RENDER IT, CROP IT, AND LOOK AT IT.** Rev 74's tread was confirmed by a silhouette trace *and*
   by looking; its pixel-diff A/B is a flat null and would have said "nothing shipped".
3. **A control is finished when you have WATCHED IT FAIL.** Rev 74's T3 was watched at 0.0000 m —
   **and the first version of T3 passed at 0.0119 m on the very defect it exists to detect (F310).**
6. **A guard that derives its threshold from the expression it checks is a tautology.** T6 recovers
   64 cycles/rev from a render built with `TREAD_LUGS = 64`; that is NOT evidence 64 is right.
8. **PAINT THE WINDOW BEFORE THE NUMBER.** Rev 74's first two tread windows were both off the tread.
9. **READ THE SUMMARY LINE, NOT THE EXIT CODE.**
12. **Report the measurement WITH ITS CEILING.**
37. **AN ABSENT INPUT MUST NEVER READ AS A MEASUREMENT** — and it must not read as a FAILING one
    either. **That is F311, and it costs the next context its pickup.**
49. **A DIFFERENCE WITH NO FLOOR UNDER IT IS NOT A MEASUREMENT** — **and take the floor IN THE SAME
    WINDOW.** Rev 74 read a whole-frame floor, called a localised change visible, and its own
    box-local floor refuted it.
50. **A GREP IS NOT A REGRESSION TEST** — `audit_brief.py`'s regex cannot match a command line with a
    frame argument, so it is blind to the largest instance of its own class (F316).
54. **A CONSTRUCTION THAT CANNOT EXPRESS THE DEFECT CANNOT BE TUNED INTO EXPRESSING IT.** The tyre is
    the second instance; the emblem's on-band spine was the first.
55. **EVERY REVISION SHIPS A VISIBLE CHANGE TO THE VEHICLE, OR SAYS PLAINLY WHY IT COULD NOT.**
    **REV 74 DID: the tyre's transverse tread (F308).**
56. **AN INSTRUMENT CAN RANK A THING THE EYE REJECTS, AND IT WILL NOT TELL YOU** (F262).

---
## §6 WHERE EVERYTHING ELSE LIVES

| file | what it holds |
|---|---|
| **`HANDOFF_CARRIERS.md`** | every carrier: the goal, the reference set, §2's refuted emblem routes, §4 the owner's rulings, §5 rules 34–58, the horizon |
| `OPEN_FINDINGS.md` | the register. **F308–F321 are rev 74's** (17 rows, including F308b, F312b and F316b). It outranks prose |
| `STATE.md` | machine-written; outranks every prose description. **Regenerate it before trusting a row that reads it** |
| `LEDGER_rev74.md` | what rev 74 did, **including the reading it made and then refuted itself** |
| `photometry.py` | the measurement protocol, with a selftest |
| `SPEC.md`, `REF_MEASUREMENTS.md`, `SURVEY_rev49_photoreal.md`, `ROADMAP_rev68.md`, `PANEL_rev61.md`, `REMAINING_WORK_rev61.md`, `PHOTOS_WANTED_rev49.md`, `PHOTOS_WANTED_rev52.md`, `EMBLEM_HANDOFF.md` | large; load the one the task needs |

**⚠ IDs THIS BRIEF LEANS ON WITHOUT NAMING, SO A GREP FINDS THEM (rule 16): `F277`, `F283`, `F71`,
`F254`, `F21`, `F298`, `F304`, `F222`/`F223`, `F231`, `F242`, `F262`, `F276`, `F282`, `F295`.**

---
## §7 HOW TO CLOSE

**HIS STANDARD:** photo-real parity with **that exact bus**, in service of a promotional render.
**Any single measurement off is unacceptable** — per-measurement, not on average. **Never call it
done off self-review. Report the measurement with its ceiling. Do not say anything is ready.**

1. `./bootstrap.sh` and `./verify_clone.sh` all-PASS on a **clean** tree. **See §1 first.**
2. `python3 revstats.py` — **put its geometry/closure line in the ledger header; if the revision
   shipped nothing, say so at the TOP** (rule 55).
3. Regenerate `STATE.md` (`T1_SUB=2 … audit.py`) — **commit first**.
4. **DISPATCH an adversary at the brief you WROTE (rule 17), and one at the brief you RECEIVED
   (rule 15). DO NOT CLOSE UNTIL BOTH REPORT.** ⚠ **AND RE-RUN THE OUTGOING ONE AFTER ANYTHING SHIPS.**
5. **Keep the split, and KEEP THIS FILE SHORT.** `cp` it over `PASTE_INTO_CLAUDE_CODE.txt` in the
   same commit. `python3 audit_brief.py --fix-count` LAST.

---
**⚠ THIS BRIEF WAS AUDITED AGAINST THE MACHINE, AND BOTH HALVES OF RULE 17 WERE RUN.**

**AND THE RULE-17 ADVERSARY CHANGED THE SHIP, WHICH IS THE POINT OF RULE 17.** It returned FOURTEEN
defects and **four of them were repaired in the geometry, not in the prose** (F319/F320):

1. **THE TREAD SHIPPED IRREGULAR** — 99 of 384 equator vertices cut in runs of 1 AND 2, because the
   phase threshold left the LEADING edge on the modulo wrap with **zero** margin. My source comment
   argued the float-safety case and had it exactly half right. **Fixed; 128 of 384, one run width.**
2. **T5 DID NOT MEASURE WHAT IT NAMED** — it compared max RADIUS while claiming to protect `TYRE_D`,
   which `verify.py:690` defines as `max(z)-min(z)`, a bbox extent. **It does move, by 0.0890 mm.**
   ⚠ **`STATE.md` had already recorded it and I read the `+0.0 → -0.0 mm` flip as float noise.**
3. **F309's *"SAME LOCATION"* IS WITHDRAWN** — `ref_rear34.jpg` is a planted café patio,
   `ref_playa_34.png` a paved yard. **The retirement of F143 survives on absence in two independent
   scenes, at n = 1 on the present side. Said at its real strength, not the strength I first gave it.**
4. **THE SHIP HAD NO GUARD ROW AT ALL** — in the revision whose §3b makes *"no silent regression"* a
   heading, `grep -c probe_rev74 verify_clone.sh` returned **0**. **Five rows added.**

**AND THE RULE-15 ADVERSARY ON THE INCOMING BRIEF RETURNED EIGHTEEN** (F316/F316b), the most
consequential being that `probe_rev67_nose.py` reads **`7 checked, 0 FAILED` with P3c PASSING** where
the brief said it fails BY DESIGN — verified independently.

**WHERE THIS BRIEF IS WEAKEST, STATED RATHER THAN HIDDEN:**
* **`verify_clone.sh` READS `426 PASSED, 2 FAILED` ON THIS TREE, AND §1 IS ABOUT WHY.** The
  all-pass total is **428**; the two reds are the ROTATION KILL and, downstream of it, the count row,
  which misses by exactly the number of other reds and **must not be papered over.** One row —
  `F296 ... the 7-degree ROTATION KILL fires` — **is correctly reporting a real failure** (F312/F312b:
  the miss reproduces across three frames at 1.75–2.00 against a 1.5 bar). **It is not re-based here.
  Do not re-base it without reading F312b.**
* **T6's FLOOR IS A STRING LITERAL** (F320f). The reasoning is sound — a revolve has no angular
  structure — but `0.0503 px / amplitude 4` is a recorded reading on a frame not retained, and no row
  recomputes it. **One `T1_TYRE_TREAD=0` render re-derives it.**
* **THE TREAD'S COUNT, DEPTH AND DUTY ARE ALL DECLARED, NOT MEASURED** (F308b). T2 refuses to publish
  a count and prints its six disagreeing estimates instead. **Do not quote 64 as a measurement, and
  do not read T6's recovery of 64 from pixels as confirming it (rule 6).**
* **T7 READS THE EQUATOR RING ONLY.** Lug edges away from `y = 0` are unchecked.
* **THE PIXEL-DIFF A/B IS A FLAT NULL, INCLUDING BOX-LOCALLY**, and I published a "localisation
  confirmed" reading one step before the floor that refutes it.
* **THE EMBLEM IS NOT RIGHT.** P2 crossed its bar at 0.8528 against P1b's 0.9465, the objective still
  has no legibility term (rule 56), and **the weight is closed to tuning by F314 but NOT resolved.**
* **Every figure quoted from `out/` needs a re-render before you quote it** — `out/` starts empty.
