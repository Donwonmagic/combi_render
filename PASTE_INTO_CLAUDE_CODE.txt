# NEXT CONTEXT PROMPT — rev 76   ·   **ACTION BRIEF**

**REV 75 SHIPPED NO GEOMETRY AND SAYS SO AT THE TOP (rule 55).** It repaired the pickup (F323),
refuted F312b with the experiment F312 itself prescribed (F324), and **checked the grounding of the
one geometry candidate it took to the bench and REFUSED IT on the measurement** (F325). **Run
`python3 revstats.py` and read ITS numbers.** Every carrier lives in `HANDOFF_CARRIERS.md`; every
finding in `OPEN_FINDINGS.md`; every measurement in a probe that RUNS. **This file is only what to do
next. DO NOT GROW IT.**

> *[owner, rev 74, shown `probe_scratch/rev74_weight_ask.png`]* **"I can't tell them apart — stop
> tuning the weight."** — **F314. THE WEIGHT IS *UNRESOLVED*, NOT SETTLED. DO NOT RE-ASK IT.**
> *[owner, rev 71]* **"The ultimate goal is a 3d render from which to build promotional material
> from."** and **"I certainly want physics closed."**
> *[owner, rev 72]* **"set up for success so that it can only carry forward, no regression allowed."**

**THE EMBLEM IS STILL HIS NINTH REPORT AND IT IS STILL WRONG. F191 AND F234 BOTH STAND.**

---
## §0 DO THIS FIRST — THE MACHINE IS IDLE WHILE YOU READ

```bash
cd /home/user/combi_render     # <- OR YOUR CLONE'S ROOT.  Nothing here needs this exact path
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
  # ⚠ bootstrap INSTALLS pillow ITSELF (`for m in numpy PIL scipy`), and has since rev 45, so
  # every brief's "pip install pillow FIRST" is BACKWARDS.  If it still reads 3 of 10 FAILED
  # on PIL, run `pip install pillow` and re-run it (F327)
nohup setsid env T1_SUB=1 T1_PREVIEW=front,side,hero34f,hero34r T1_PFX=r76 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r76.log 2>&1 < /dev/null &
```
**`grep -c Saved: /tmp/r76.log` must be 4**, ~5.5 min a frame. `setsid`, not a bare `nohup &` (F173).
**`out/` starts EMPTY** — re-render before quoting any frame. **DO NOT EDIT SOURCE WHILE THE QUEUE
RUNS** (probes and `.md` are fine; `build.py` and the `t1_*` modules are not).

## §0b BEFORE YOU MEASURE ANYTHING
```bash
python3 photometry.py          # 9 checked, 0 FAILED
```
**READ LINEAR / REFUSE CLIPPED / MEDIAN NOT MEAN / PAINT THE WINDOW. Import it; do not re-derive it.**

---
## §1 ⚠ **THE PICKUP SHOULD NOW BE CLEAN. MEASURE IT; DO NOT BELIEVE THIS SENTENCE.**

**F311 IS REPAIRED (F323).** The five `verify_clone.sh` rows that hard-failed for want of a rendered
side frame now **SKIP and say so** — `ok … [UNGUARDED -- input absent; run the brief's sec.0 render]
ABSENT` — via the new `ckabs` helper. **`PASS` is unchanged either way**, so the self-referential
count row stays meaningful.

⚠ **THE COUNT WAS FIVE, NOT FOUR.** All five rows keyed on `probe_rev73_tailboard.py` hard-fail on
an empty `out/`, **the ROTATION KILL included**; repairing "the four" would have left the pickup red.
⚠ **BE FAIR TO THE REV-75 BRIEF ABOUT THIS, WHICH REV 75's OWN FIRST DRAFT WAS NOT.** Its three
numbers — *"FOUR ARE ONE CAUSE — NOT FIVE"*, *"it has five that HARD-FAIL"*, *"§1's six rows"* — had
three DIFFERENT stated referents and were a partition, not three counts of one thing. **The partition
was wrong only because F312b was wrong.** Calling it "four, five and six in three places" overstates
it, and that phrasing is corrected here and in F323.

**MEASURED AT REV 75 — expect DIFFERENT numbers, the script has 437 rows now:**
```
  PICKUP  bootstrap 9 PASSED, 1 FAILED   ·  verify_clone 423 PASSED, 6 FAILED  (429 rows)
  CLOSE   verify_clone ALL 437 PASS on a clean tree -- with an EMPTY out/ (5 rows
          SKIPPING) and with four frames.  bootstrap ALL 10 PASS; --guards ALL 25 PASS
          ALL-PASS TOTAL 437  (WATCHED, empty out/ AND with four frames)
```
⚠ **AND THE REV-75 INCOMING BRIEF'S *"ALL-PASS IS NOT REACHABLE"* IS REFUTED** — as is its §2.1
*"clearing the pickup needs T3 diagnosed as well — that is a second job"*. **Both rested on F312b,
which F324 refutes.**

⚠ **BUT ONE THING IS NOW LOAD-BEARING AND YOU MUST READ IT (F324): `verify_clone.sh`'s result
DEPENDS ON WHICH `out/*_side.png` IS ALPHABETICALLY LAST.** `probe_rev73_tailboard.py` takes no
argument and reads that frame; across **THREE renders of ONE tree** T3 **passed twice and failed
once** (F324). So a verifier's verdict now turns on render luck. **That is F311's disease one
level deeper and it is the first thing to decide — see §2.1.**

**AND MEASURE THE BRANCH, DO NOT TRANSCRIBE IT, INCLUDING THIS SENTENCE:**
```bash
git fetch --all --prune
for b in $(git branch -r | grep -v HEAD); do printf "%-52s ahead %-3s behind %s\n" "$b" \
  "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"; done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
```
⚠ **NAME YOUR BRANCH: you are on `claude/rev-75-pickup-po0rs3`, named for the PREVIOUS revision,
and no brief has said where the next revision's work belongs. Decide it and say so in your ledger.** **At rev 75 the designated branch again had no remote copy at pickup
(F317's shape, third revision running). Nothing was stranded: row 9 PASSED, all 29 remote branches `ahead 0`, HEAD 0 ahead / 0
behind `origin/main`, the diff empty.** **The "N consecutive revisions" count in every brief is
HAND-INCREMENTED AND DERIVED FROM NOTHING. Believe row 9 and the loop, never a sentence.**

---
## §2 RANKED WORK FOR REV 76

⚠ **ITEM 2 IS THE BINDING CONSTRAINT, NOT ITEM 1.** Item 1 is a cheap DECISION; item 2 is rule 55
and **rev 75 failed it.** **If you can only do one, SHIP GEOMETRY.**

**RANK BY PIXELS OF THE DELIVERY FRAME** — `python3 visibility_budget.py 3840 out/r76_hero34f.png` —
**and the owner outranks the ranking.** ⚠ **READ THAT TABLE'S OWN CEILING: *"pixels are not
visibility … catch ORDERS OF MAGNITUDE, not rank neighbours."*** The ranked list is
`REMAINING_WORK_rev61.md`, triaged into `ROADMAP_rev68.md`.

### **1. DECIDE T3, WITH THE DATA NOW IN HAND (F324). THIS IS A DECISION, NOT A MEASUREMENT.**
F312 named the experiment; **rev 75 ran it and it lands on F312's SECOND branch:**
```
  render 1   out/r75_side.png    -7.0 -> -7.00   miss 0.00   GAIN 0.883   T3 PASSES
  render 2   (deleted; see the ledger)  -7.0 -> -8.50  miss 1.50  GAIN 0.982  T3 FAILS
  render 3   out/r75b_side.png   -7.0 -> -6.50   miss 0.50   GAIN 0.919   T3 PASSES
```
⚠⚠ **NONE OF THESE THREE FRAMES EXISTS ON YOUR TREE. `out/` is untracked and DOES NOT EVEN EXIST on
a clone — the phrase every document here uses, "out/ starts EMPTY", is weaker than the truth. The
table below is a RECORD OF READINGS, not files you can re-read.** The whole of §2.1 and §2.3 reasons
from **eight** historical frames and **not one of them is on your disk.** Re-deriving any of them
means RE-RENDERING, which draws a fresh sample from the same noisy distribution — that is the point
of the finding, and it is also why you must not quote these numbers as if you had re-read them.

**THREE renders of ONE tree, no source change between any of them. The rung the verdict turns on
reads −7.00 / −8.50 / −6.50 — a RANGE of 2.00°, on a rung whose bar is 1.5.** n = 3, 2 pass / 1 fail.
So *"if they differ, T3 is measuring noise and should not have a 1.5 bar at all"* — F312's own words
— **fires on this tree.** ⚠ **BUT DO NOT READ F312b AS SIMPLY WRONG. Its `r74t_side`/`r74t3_side`
ARE a SAME-TREE pair — F312b's own row says so — and they AGREED TO THE BIN at −9.00/−9.00, both
failing. Rev 74 already ran this experiment and landed on F312's OTHER branch. THE TWO TREES ARE
DISJOINT CLUSTERS: −9.00 / −9.00 / −8.75 against −7.00 / −8.50 / −6.50 — a BUILD-DEPENDENCE on top
of the render scatter, which NEITHER of F312's two branches covers. ⚠ **CALL THEM CLUSTERS, NOT "THE
TWO TREES": THREE builds are in play — no-tread, irregular tread, shipped tread — so rev 74's
cluster itself spans two.** ⚠⚠ **THE DECISIVE FRAME WAS NEVER READ: `out/r74f_side.png` is the
SHIPPED build and NO DOCUMENT REPORTS T3 ON IT — but `git diff --name-only 94b3751 HEAD` is three
files and the `t1_detail.py` diff is COMMENT-ONLY, so HEAD's GEOMETRY *IS* THE REV-74 TREE and §0's
own side render IS that frame. Check nothing out; just read T3 on your §0 frames.** Rev 75's first
draft called F312b refuted on a "three different trees" premise its own row contradicts; retracted
(rule 13). **ANY BAR MUST SURVIVE BOTH CLUSTERS.** ⚠ **NAME THE FRAME: render 2 was deleted and
re-made, so `out/r75b_side.png` is render 3 and reads −6.50; the −8.50 frame is gone (F316/F320c).**
⚠ **THE VERDICT DISAGREES WITH ITS OWN STATISTIC: render 2 has the gain NEAREST 1.000 and four of
five rungs TIGHTEST, and it is the one that fails. And the gain claim is NOT ESTABLISHED — 0.883 /
0.982 / 0.919, a spread of 0.099 against a ~0.072 mean departure from 1.000.**
**REV 75 DID NOT RE-BASE IT** — a bar set on n = 3 is still an invented figure (rule 5) — **but it
did put the floor into T3's own message so the row cannot be quoted without it.**
⚠ **AND A TRAP THIS SETS FOR YOU, NAMED SO YOU DO NOT SPRING IT: `verify_clone.sh` has a row
`grep -c 'MEAN GAIN'` expecting exactly 1, keyed on T3's PROSE — rule 50's own class. Rev 75
reworded that message and the row went red at two matches (rule 44; it reworded, not re-based).
IF YOU EDIT T3's MESSAGE, RUN `verify_clone.sh` BEFORE YOU COMMIT.** ⚠ **DO NOT simply
widen the bar. What the row is FOR is "the detector moves"; the 1:1 requirement is the part that is
not reproducible. And the honest fix needs more than n = 3: rev 75's three renders give a 2.00°
RANGE but no distribution. FIVE OR SIX side renders of one tree is ~30 minutes and would set a real
floor (rule 49) — THEN a bar can be set on something WATCHED rather than invented.**

### **2. SHIP GEOMETRY. RULE 55 IS THE BINDING CONSTRAINT AND REV 75 DID NOT MEET IT.**
⚠ **CHECK THE GROUNDING BEFORE YOU BUILD — and be ready for the answer to be NO.**
**F325: the tail board's *"dark angled recess"*, `HANDOFF_CARRIERS.md` §0.05's build item 2, live since rev 62, IS NOT
GROUNDED — AT ITS TRUE STRENGTH, WHICH IS NARROWER THAN REV 75 FIRST WROTE.** One frame,
**30 × 12 px, 58 px below lum 90**; that frame is byte-identical to `ref_nolita_doorshut.jpg`, so
**n = 1**; `ref_side.jpg` is **EDGE-ON** and cannot corroborate by construction.
⚠ **(a) `HANDOFF_CARRIERS.md` §0.05 NAMES A THIRD FRAME, `ref_rear34.jpg` (820, 0)–(1200, 300), WHICH REV 75 NEITHER
OPENED NOR MENTIONED — the propped board IS in it. LOOK AT IT FIRST; IT MAY OVERTURN THIS REFUSAL.**
⚠ **(b) rev 75's *"shadow, panel gap and recess are not separable"* IS ONE HYPOTHESIS TOO WIDE — the
bands around the blob read median 204–218 with `frac<90` = 0.00 on all four sides, so the dark region
is FULLY INTERIOR to the cream face and the PANEL-GAP reading is refuted from that same window. The
refusal rests on SHADOW versus RECESS, and on depth.** **NOT struck — carried with its ceiling
(rule 16).**
**So the live candidates are: the tail's barrel, the shut lines, the glass, and the tread's own open
constants (§2.3). CHECK EACH ONE'S GROUNDING FIRST — that is what rev 74 paid for twice and what
rev 75 spent its geometry slot on.**

### **3. F318 — THE TREAD'S ONE MEASURED COST — IS STILL OPEN AND ITS FIX IS PRESCRIBED AND UNDONE.**
`probe_rev70_tyre.py`'s T2 moves **0.2457 → 0.2558** (1.26× → 1.31×) between `out/r74_side.png` and
`out/r74f_side.png`, **25× its measured 0.0004 two-render floor**, **4.1 % against the probe's own
±20 % ceiling**. ⚠ **DO NOT "FIX" IT BY LOWERING `T1_TYRE_FILM`** — that tunes shading to mask
geometry and leaves the ablation too dark. **THE PRESCRIBED FIX: give T2 a band MEASURED to lie
inside the rubber (PAINT IT FIRST, rule 8) and re-read both frames.** ⚠ **AND NEITHER FRAME IS ON
YOUR TREE — you must MAKE them: `out/r74f_side.png` is just HEAD rendered (§0 gives you it as
`out/r76_side.png`), and `out/r74_side.png` is the NO-TREAD build, i.e. a `side` render with
`T1_TYRE_TREAD=0`. No document said this and a fresh context would have hunted for the files** — its present band is "the
darkest annulus", which straddles the wheel-arch shadow and the outer silhouette. **Rev 75 had a
side-frame pair in hand and did NOT do this; it is cheap and it closes a finding.**

### **4. THE TREAD'S COUNT, DEPTH AND DUTY ARE ALL DECLARED, NOT MEASURED (F308b).**
T2 **REFUSES to publish a count** and prints six estimates — a **48..84 bracket** (**quote the
bracket, not the ratio**). **`TREAD_LUGS = 64` has exactly the standing of `TB_WIDTH`'s "POSE CHOICE,
NOT MEASURED".** ⚠ **Do not read T6's recovery of 64 from the render as confirmation — that is
rule 6.** **What would close it is a CLOSER TYRE FRAME, and `PHOTOS_WANTED` has never had a tyre
item — nor a tail-board one (F325). Consider adding both.**

### **5. THE EMBLEM.** His ninth report. **0.8528 against P1b's ceiling of 0.9465 — ~0.09 short —
and the objective STILL HAS NO LEGIBILITY TERM (rule 56).** The weight is closed to tuning by F314
but **NOT resolved** (F302, F303 stand). **F252's option (C)**, the 1400-start search
(**0.7586 / 0.6698**), is built by nobody — ⚠ **its figures came off the BROKEN RULER (F246) and
option (C) alone was never re-run; F289b re-ran (A) and (B) at rev 73, and F252's own grade reads
REFUTED AT REV 73.** ⚠ **Fix the legibility term before another search.**

### **6. F156 — the `Senor` gate row scores a DELIBERATE DEPARTURE.** THIRTEEN revisions unacted
(rule 40). ⚠ **THAT COUNT IS HAND-INCREMENTED, like the branch count §1 warns about. It checks out
against F156's `MEASURED-rev62` grade — but `HANDOFF_CARRIERS.md` simultaneously carries "NINE
revisions unacted", "EIGHT revisions un-re-based" and "five revisions unacted" for the SAME finding.
Read the grade, not any of the four sentences.**

---
## §3 WHAT REV 75 CLOSED — **DO NOT RE-OPEN ANY OF IT**

| closed | the result |
|---|---|
| **THE PICKUP (F311 → F323)** | **REPAIRED.** `ckabs` reads the absent flag from **the probe's own summary line** (rule 9); the skip **still calls `ck`** so `PASS` is unchanged (omitting rows re-breaks the count row — measured, 424 vs 428); it prints **ABSENT**, never a number, and says **UNGUARDED** in the label (rule 37). **Four companion rows** (§3b): a WATCHED KILL through both branches with tallies snapshotted, the flag cross-checked against an INDEPENDENT `ls` (rule 6), and `SKIPPED` BOUNDED at 5/0. **T3's comparison is UNTOUCHED.** |
| **F312 / F312b (F324)** | **T3's VERDICT IS RENDER NOISE ON THIS TREE** — three renders of one tree read the deciding rung at **−7.00 / −8.50 / −6.50**, a 2.00° range on a 1.5 bar. ⚠ **F312b is NOT refuted wholesale and rev 75's first draft said it was (retracted, rule 13): its `r74t`/`r74t3` are a SAME-TREE pair that AGREED at −9.00/−9.00.** Only its GENERALISATION falls. **Full detail and the unread decisive comparison are in §2.1 — read that, not this row.** Not re-based (rule 5). |
| **THE ARTEFACT-EDGE HYPOTHESIS (F324)** | **MINE, AND I KILLED IT WITH ITS OWN CONTROL.** T3's `rotate(expand, fillcolor=white)` DOES inject non-rotating axis-aligned edges at ≈179.6°/≈90.4°. **Masking them out changes no rung by more than the histogram's 0.25° bin, and the one that moved got WORSE. Real, and NOT causal.** Figures, frames and two corrections to them: `LEDGER_rev75.md`. |
| **THE RECESS'S GROUNDING (F325)** | **REFUSED ON THE MEASUREMENT, BEFORE BUILDING.** 30 × 12 px, n = 1, the corroborating frame edge-on by construction. *"It cannot be recovered from what we hold"* is the result (rule 12). |
| **A SECOND COPY OF A WITHDRAWN CLAIM** | `t1_detail.tyre()` still read *"so `TYRE_D` is independent of both halves"* — F319 withdrew that at rev 74 and **one copy was missed**. `TYRE_D` is a **bbox extent** and moves by **0.0890 mm**. Withdrawn in place. |

---
## §3b ⚠ REV 72–75's FIXES ARE LOCKED. YOU CANNOT REGRESS THEM SILENTLY.

**YOU MAY IMPROVE ANY OF IT; YOU MAY NOT SILENTLY UNDO IT.** A red row is a FINDING ABOUT YOUR
CHANGE. A re-base needs the cause NAMED **and** a companion row making that cause separately testable.
**Rev 75 added FIVE rows of its own** — four for `ckabs` (F323) and one pinning F325's recess
measurement against the TRACKED `IMG_3840.jpeg`. ⚠ **"Frame-independent" needs one qualification the
rule-17 adversary supplied: two of the four DO read `out/` (`ls out/*_side.png`), so they are
frame-AWARE, not frame-blind — they are correct either way, which is the property that matters, but
do not repeat the phrase without it. And the `SKIPPED` bound catches a new skipping row only when
`out/` is EMPTY: a sixth `ckabs` call whose absent flag were always 0 would leave SKIPPED at 5/0 and
pass unnoticed.** ⚠ **AND REV 75's OWN CHANGE WENT RED ON AN EXISTING ROW: rewording T3's message made
`grep -c 'MEAN GAIN'` match twice. The guard won (rule 44) and the text was reworded.**

**RUN `./bootstrap.sh --guards` ONCE THIS REVISION.** ⚠ **MEASURED AT REV 75 ON A COLD CLONE:
`bootstrap.sh --guards` = ALL 25 PASS in `real 19m25s`.** Its printed *"about six minutes"* is wrong by **3.2×** and two of its comments say *"~10 min"* — **so "budget it from the machine" FAILS here: the
machine's own prose is the least accurate figure available (F327). BUDGET ~20 MIN**, and not while a
render queue is going. It does **not** build Blender — the MODEL is built, `build.py` runs 10
times across 15 invocations. It is the only thing that exercises the five rear-hatch kills.

---
## §4 THE MACHINE

```bash
./bootstrap.sh                                # READ ROW 9.  Row 10 is verify_clone.sh
./verify_clone.sh                             # ALL 437 PASS -- 0 FIDELITY, 437 SELF-CONSISTENCY.
  # ⚠ AND THE TOTAL DEPENDS ON WHICH out/*_side.png IS ALPHABETICALLY LAST (F324) -- see sec.2.1.
  # With an empty out/, five rows SKIP and say UNGUARDED; PASS is the same either way.
  # READ THE VERDICT BLOCK: not one row measures the vehicle against a photograph
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
python3 photometry.py                         # 9 checked, 0 FAILED
python3 probe_rev74_tread.py out/r76_side.png   # 8 checked, 0 FAILED.  NAME YOUR FRAME: bare it
  # takes the alphabetically-last out/*_side.png and PRINTS which.  Bare with an empty out/ it
  # reads 8 checked, 0 FAILED, 1 ABSENT -- EIGHT, because row() does CHECK += 1 BEFORE the
  # ABSENT test.  audit_brief cannot catch that: its regex cannot match a continuation line
T1_TYRE_TREAD=0 python3 probe_rev74_tread.py  # THE KILL.  ⚠ IT REDS **TWO** ROWS, NOT ONE:
  # "8 checked, 2 FAILED, 1 ABSENT -- T3,T7".  T3 goes 0.0060 -> 0.0000 m and T7 reads 0 of 112
  # equator vertices cut.  verify_clone.sh pins T3 only.  The rev-75 brief said "T3 must go RED"
  # and named one -- F322's class again, caught by cold-starting (rev 75)
python3 probe_rev73_tailboard.py              # ⚠ 5 checked, 1 or 2 FAILED -- IT DEPENDS ON THE
  # FRAME (F324) AND THE PROBE TAKES NO ARGUMENT.  T4 always fails BY DESIGN.  T3 is the
  # coin flip.  ** ON A CLONE, WITH NO out/, IT READS "0 checked, 0 FAILED, 2 ABSENT -- no side
  # render" AND EXITS 2.  THAT IS CORRECT (rule 37), NOT A FAILURE. ** After sec.0's render it reads
  # 5 checked, 1 or 2 FAILED depending on the frame.  At rev 75's close BOTH of its surviving
  # frames read 1 FAILED (T4 only) -- but NEITHER SURVIVES ON YOUR TREE.  READ THE FRAME IT PRINTS
python3 probe_rev67_nose.py out/r76_front.png
  # ⚠ THE OUTCOME IS FRAME-DEPENDENT AND NO DOCUMENT MAY STATE AN EXPECTED COUNT.  Measured:
  # r74_front 7 checked 0 FAILED with P3c PASSING (F316); r75_front 7 checked 1 FAILED with
  # P3c RED (333 of 641 columns, vertex u 839 IN the gap 836..847).  NAME YOUR FRAME
python3 probe_rev46_vw.py                     # 12 checked, 2 FAILED -- C4 AND C10 (F304)
python3 probe_rev69_fitpose.py                # 5 checked, 1 FAILED -- P4 only.  ⚠ P1's MESSAGE
  # hardcodes a 0.9703 ceiling while P1b prints 0.9465; read the NUMBERS, not the prose
python3 gloss_compare.py out/r76_hero34f.png  # FAILS at 0.412 on r75_hero34f (bar 0.60)
python3 flank_compare.py out/r76_side.png /tmp/fc.png   # FAILS, worst `i` 0.686 on r75_side
python3 probe_rev71_proxy.py                  # must read IoU 1.000000
python3 probe_rev71_red.py out/r76_side.png --transform=agx   # REFUSES with a summary line
  # F266's PHYSICS RECIPE: T1_VT=Raw T1_LOOK=None T1_EXP=-2.5, then --transform=raw
python3 probe_rev70_tyre.py out/r76_side.png
  # ⚠ FIXED AT REV 75 (F326): with an ABSENT frame this CRASHED -- bare FileNotFoundError, NO
  # summary line, six revisions, in this copy-paste block (rule 37 + rule 51).  It now REFUSES:
  # "NO SUCH FRAME ... nothing was measured (rule 37)", then "1 checked, 0 FAILED".  It was the
  # ONLY frame-consuming probe in sec.4 that did not already refuse cleanly.
  # ⚠⚠ IT REPAINTS TRACKED FILES, AND SO DO 16 OTHERS: MEASURED at rev 75, 17 probes write 42
  # TRACKED probe_scratch/*.png (F329).  Every earlier brief named one or two -- whack-a-mole.
  # ANY probe sweep REDS "modified tracked files" and breaks sec.7 step 1.  THE RULE, NOT THE LIST:
  #   git status --porcelain ; git checkout -- probe_scratch/   # repaints are side effects, NOT work
  # ⚠ AND LOOK BEFORE COMMITTING: a probe run without a frame can repaint a tracked PNG SMALLER and
  # DEGRADED -- rev 75 caught rev69_emblem_render.png going 24578 -> 13500 bytes.  Committing that
  # destroys a painted window rule 8 depends on
python3 visibility_budget.py 3840 out/r76_hero34f.png ; python3 revstats.py
T1_SUB=2 /tmp/blender/blender -b -P audit.py            # rewrites STATE.md -- COMMIT FIRST,
  # and do it AFTER your LAST source edit, THEN run audit_adversary.py
python3 audit_brief.py ; python3 audit_adversary.py     # rules 15/17, MECHANICAL half only.
  # At rev 75's close, AFTER --fix-count: audit_brief 14 checked / 0 FAILED.  Before it the count
  # row is red BY CONSTRUCTION -- that is sec.7.5's ordering, not a defect;
  # audit_adversary 61 asked / 0 BROKE.  ⚠ audit_adversary BREAKS if you cite an F-number
  # in verify_clone.sh before writing its row in OPEN_FINDINGS.md -- it caught exactly that
  # at rev 75 ("does every F-number cited by verify_clone.sh exist in the register?")
```

**THE ABLATIONS.** ⚠ **`--guards` RUNS THE `T1_REAR_*` BLOCK, `T1_REAR_OPEN=-64` INCLUDED. The three
below are NOT hand-run either — `verify_clone.sh` (which IS `bootstrap.sh`'s row 10) runs all three;
the rev-75 brief called them hand-run on the strength of a grep of `bootstrap.sh`, the wrong file
(rule 50 firing on a correction).**
```bash
T1_REAR_SEAL=0      -> 1 fail      T1_REAR_SEALSTAY=1  -> 2 fail
T1_REAR_NOSWING=1   -> 1 fail      T1_REAR_SEALSHIFT=1 -> 2 fail
T1_REAR_FOLD=1      -> 1 fail      T1_REAR_OPEN=0      -> 0 fail (HONEST close)
T1_REAR_OPEN=-64    -> REFUSES at the parse site, naming the switch (F281)
T1_NOSE_NOWIN=1     -> P3 RED (F284).      run by verify_clone.sh
T1_VW_FREE=0        -> ablates the emblem's free spine to rev 72's (F301).  run by verify_clone.sh
T1_TYRE_TREAD=0     -> probe_rev74_tread's T3 goes 0.0060 -> 0.0000 m (F308).  run by verify_clone.sh
```

**FACTS THAT BITE:** `bootstrap.sh` fails 3/10 without pillow. The render is **not** run-to-run
deterministic — floor **~2.04 %** of pixels >8 levels on hero34f at 1600×1100/96 spp, **and take the
floor IN THE BOX YOU ARE READING: 4.37 % inside the front-wheel box, 7.90 % on the body** (F308).
`lid_gen.py` / `script_gen.py` are **not** called by `build.py`. `audit.py` rewrites `STATE.md` —
**commit first**. `ck` in `verify_clone.sh` collapses whitespace. **A backgrounded runner's `rc=$?` is
the redirect's.** `bpy` is a pip module, so most probes run in ~1 s.

---
## §5 THE RULES THAT WILL BITE YOU

⚠⚠ **READ THIS BEFORE YOU LOOK UP ANY LOW-NUMBERED RULE. THERE ARE TWO INCOMPATIBLE CANONS FOR
RULES 1–33 AND EVERY BRIEF UNTIL NOW SENT YOU TO THE WRONG ONE (found by cold-starting this handoff,
rev 75).**

* **`CLAUDE.md`'s own numbered list (1–18) IS THE ONE IN FORCE.** It is what the brief below means,
  and it is what LIVE SOURCE means: `grep -rhoE "rule [0-9]+" --include=*.py --include=*.sh .` gives
  43 hits on rule 8, 42 on rule 3, 22 on rule 9 — all in `CLAUDE.md`'s senses.
* **`NEXT_CONTEXT_PROMPT_rev50.md` §11 carries a DIFFERENT numbered 1–33**, and previous briefs
  (including rev 75's) pointed you at it for "rules 1–33". **The numbers COLLIDE:**

| you look up | `CLAUDE.md` — what the source means | rev50 §11 — what the old pointer gives |
|---|---|---|
| **rule 3** | a control is finished when you have WATCHED IT FAIL | read each probe's summary line |
| **rule 5** | never put a figure in a test you have not watched print | do not inherit a guard's rationale |
| **rule 9** | read the summary line, never the exit code | a threshold trace needs the FAR SIDE resolved |
| **rule 12** | report the measurement WITH ITS CEILING | add the guard in the same edit |
| **rule 16** | YOU MUST NOT DELETE A CARRIER | a part measured in isolation is not measured |

**SO: for rules 1–18 read `CLAUDE.md`. Rules 34–58 are in `HANDOFF_CARRIERS.md` §5 — ⚠ whose own
first line says 34–52.** rev50 §11 is HISTORY, not the canon; **do not cite it and do not renumber
anything silently.** **AND §5 CONTAINS TWO DIFFERENT RULE 56s AND TWO DIFFERENT RULE 57s, AND RULE 42
MEANS TWO DIFFERENT THINGS IN LIVE SOURCE. UNRESOLVED — say which you mean.**

**Read them in `CLAUDE.md` (1–18) and `HANDOFF_CARRIERS.md` §5 (34–58); what follows is only WHICH
ONES BIT REV 75, so you know they are live.** **1** — F325's refusal came from cropping two frames
and LOOKING. **3** — the new guard was watched failing on the same wrong expectation its skip branch
passes. **4** — the artefact-edge hypothesis was plausible and **killed by its own control**. **5** —
why T3 was not re-based on n = 3. **9** — `ckabs`'s absent flag is read from a summary line. **37** —
an absent input must not read as a measurement **nor as a failing one**; that was F311, three
contexts' pickups, now fixed. **44** — fired twice on rev 75's own edits; the guard won both times.
**49** — T3's bar never had a floor. **50** — rev 75 "corrected" a claim with a grep of the wrong
file. **55 — EVERY REVISION SHIPS A VISIBLE CHANGE TO THE VEHICLE, OR SAYS PLAINLY WHY IT COULD NOT**:
rev 75 could not, and says so atop its ledger. **6, 8, 12, 56** all still bite.

---
## §6 WHERE EVERYTHING ELSE LIVES

| file | what it holds |
|---|---|
| **`HANDOFF_CARRIERS.md`** | every carrier: the goal, the reference set, §2's refuted emblem routes, §4 the owner's rulings, §5 rules 34–58, the horizon |
| `OPEN_FINDINGS.md` | the register. **F323–F325 are rev 75's**; F308–F322 are rev 74's. It outranks prose |
| `STATE.md` | machine-written; outranks every prose description. **Regenerate it before trusting a row that reads it** |
| `LEDGER_rev75.md` | what rev 75 did, **including the hypothesis it formed and then refuted itself** |
| `photometry.py` | the measurement protocol, with a selftest |
| `SPEC.md`, `REF_MEASUREMENTS.md`, `SURVEY_rev49_photoreal.md`, `ROADMAP_rev68.md`, `PANEL_rev61.md`, `REMAINING_WORK_rev61.md`, `PHOTOS_WANTED_rev49.md`, `PHOTOS_WANTED_rev52.md`, `EMBLEM_HANDOFF.md` | large; load the one the task needs |

**⚠ IDs LEANED ON WITHOUT NAMING, SO A GREP FINDS THEM (rule 16): `F21`, `F71`, `F222`/`F223`,
`F231`, `F242`, `F254`, `F262`, `F276`, `F277`, `F282`, `F283`, `F289b`, `F295`, `F298`, `F302`,
`F303`, `F304`, `F305`, `F309`, `F319`–`F322`.**

---
## §7 HOW TO CLOSE

**HIS STANDARD:** photo-real parity with **that exact bus**, in service of a promotional render.
**Any single measurement off is unacceptable** — per-measurement, not on average. **Never call it
done off self-review. Report the measurement with its ceiling. Do not say anything is ready.**

1. `./bootstrap.sh` and `./verify_clone.sh` on a **clean** tree. **All-PASS IS reachable now (437)** —
   ⚠ **but read §1's warning: the total DEPENDS ON WHICH SIDE FRAME IS NEWEST, because T3 is a coin
   flip (F324) — rev 75 WATCHED `verify_clone.sh` print **ALL 437 PASS** on a clean tree, and its
   render 2 would have given **432 PASSED, 2 FAILED** — T3 plus the count row, which misses by
   exactly the number of other reds. Decide T3 before you treat all-PASS as a stable bar.** The honest closing condition
   remains: **every red is one you can name, and none of them is yours.**
2. `python3 revstats.py` — **put its geometry/closure line in the ledger header; if the revision
   shipped nothing, say so at the TOP** (rule 55).
3. Regenerate `STATE.md` (`T1_SUB=2 … audit.py`) — **commit first, and AFTER your LAST source edit.**
   Then run `audit_adversary.py`. **If it moved ONLY in provenance, say so — that is evidence your
   change carried no geometry.**
4. **DISPATCH an adversary at the brief you WROTE (rule 17), and one at the brief you RECEIVED
   (rule 15). DO NOT CLOSE UNTIL BOTH REPORT.** ⚠ **AND RE-RUN THE OUTGOING ONE AFTER ANYTHING SHIPS.**
5. **Keep the split, and KEEP THIS FILE SHORT.** `cp` it over `PASTE_INTO_CLAUDE_CODE.txt` in the
   same commit. `python3 audit_brief.py --fix-count` LAST.
6. ⚠⚠ **THEN COLD-CLONE AND RUN `./bootstrap.sh` — LAST, ON A FRESH CLONE (F328).** Rev 75 broke its
   own pickup after three adversary passes AND a cold-start pass: trimming this file to fit the hard
   `<32768` guard deleted a phrase `verify_clone.sh` greps for; bootstrap went 9/1 on a clone while
   `audit_brief` and `audit_adversary` read CLEAN. **Only a cold clone catches that.**

---
**⚠ THIS BRIEF WAS AUDITED AGAINST THE MACHINE. FOUR PASSES, AND EACH ONE CHANGED THE SHIP.**
**The full account is `HANDOFF_CARRIERS.md` §11 (moved there when this file hit its 32 KB guard —
rule 16, nothing deleted); rev 75's own errors are in `LEDGER_rev75.md`.** The headlines:

1. **RULE 15, on the incoming brief — 13 defects.** Its central premise (*"T3 IS GENUINELY FAILING"*,
   *"all-pass is NOT reachable"*) was **refuted by rev 75's own first frame**, which freed the
   revision to run F312's floor experiment instead of chasing a diagnosis.
2. **RULE 17, on this brief — 18 defects, 4 TOP.** All four were one root cause and it was **mine**:
   I called F312b refuted on a premise F312b's own row contradicts. **Retracted (rule 13.)**
3. **RULE 17 RE-RUN AFTER THE SHIPS — 4 more TOP.** My corrections had reached the prose carriers and
   **stopped short of `OPEN_FINDINGS.md`, the file every other document says outranks prose.**
4. ⚠ **A COLD-START PREPAREDNESS PASS — NEW, AND NOBODY HAD EVER RUN ONE. 19 defects, 3 TOP.**
   A fresh clone was made and the pickup followed literally. **The good news is load-bearing: a cold
   clone with NO `out/` reads `bootstrap.sh` ALL 10 PASS and `verify_clone.sh` ALL 437 PASS — F323's
   repair does what it claims.** The three TOP are fixed in this brief: **the rule-canon collision
   (§5), every frame being gone on a clone (§2.1), and `probe_rev70_tyre.py` crashing instead of
   refusing (F326).**
   ⚠ **DO THIS AGAIN AT REV 76's CLOSE. Correctness and PREPAREDNESS are different properties, and
   three revisions of adversaries had only ever tested the first.**

**WHERE THIS BRIEF IS WEAKEST, STATED RATHER THAN HIDDEN:**
* **T3 IS A COIN FLIP AND IT IS NOT RE-BASED.** `verify_clone.sh`'s verdict depends on which side
  frame is alphabetically last. **Left open on purpose** — n = 3 cannot set a bar, and **the decisive
  comparison is unread** (see §2.1: HEAD's geometry IS the rev-74 tree, so §0 renders it for you).
* **REV 75 SHIPPED NO GEOMETRY.** Rule 55's second clause is met with a measurement (F325), but the
  clause exists because the owner cannot see a revision that only measures. **Rev 76 must ship.**
* **EVERY FIGURE IN §2 THAT CAME FROM `out/` IS A RECORD, NOT A FILE** — `out/` does not exist on a
  clone. Re-render before quoting anything.
* **F318's PRESCRIBED FIX WAS NOT DONE**; **T6's FLOOR IS STILL A STRING LITERAL** (F320f, a
  sub-label inside F320's row — `grep F320`, not `grep F320f`); **THE TREAD'S COUNT, DEPTH AND DUTY
  ARE DECLARED, NOT MEASURED** (F308b).
* **THE EMBLEM IS NOT RIGHT.** 0.8528 against P1b's 0.9465, no legibility term (rule 56), weight
  closed to tuning by F314 but **NOT resolved**.
