# NEXT CONTEXT PROMPT — rev 78   ·   **ACTION BRIEF**

> ## ⚠⚠ **F18's TRIGGER IS FIRED. THE OWNER SAID *"YES — START IT NOW."***
> The die-cut sticker has been the register's oldest live row since **rev 44** and it is the project's
> ORIGINAL DELIVERABLE. **F330.** The line pass it needed did not exist until rev 77; **it exists now
> (F332).** ⚠ **AND ITS CEILING TRAVELS WITH IT: he was asked whether the MODEL is done enough, NOT
> whether the EMBLEM is. He did not withdraw F191 and was not asked to.**
>
> **SECOND RULING: THE AUDIENCE IS SPLIT DELIBERATELY — *"kids get one line, adults another."* F331.**
> The deadpan-catalogue register is CONFIRMED for the adult half and is no longer a drift to correct;
> it is now HALF the programme and a children's line of equal standing is owed. **Every future
> shortlist must say WHICH LINE each item is in.**
>
> **REV 77's JOB WAS §9 OF THE REV-76 PROGRAM: GROW THE IDEAS BEFORE EXECUTING THEM. IT RAN.**
> **75 new concepts, 25 directors at `xhigh`, all 13 named-absent registers filled — and they are
> COMMITTED IN FULL in `CONCEPT_BENCH_rev77.md`, which is the CARRIER. `DESIGN_PROGRAM_rev77.md`
> ranks and decides.** Rev 76's bench was NOT committed and its bodies are gone (F335) — do not
> repeat that. **If it is not in `git ls-files`, it does not exist.**

**REV 77 SHIPPED NO VEHICLE GEOMETRY AND SAYS SO AT THE TOP OF ITS LEDGER (rule 55).** What it shipped
is **two finished artefacts and the capability under them** — `design_out/sheet3_not_issued.svg` and
`design_out/loteria_la_rueda.svg`, plus `line_pass.py`, `sheet.py`, `la_rueda.py`.
**Run `python3 revstats.py` and read ITS numbers.** Every carrier is in `HANDOFF_CARRIERS.md`; every
finding in `OPEN_FINDINGS.md`; every measurement in a probe that RUNS. **DO NOT GROW THIS FILE.**

---
## §0 DO THIS FIRST — THE MACHINE IS IDLE WHILE YOU READ

```bash
cd /home/user/combi_render     # <- OR YOUR CLONE'S ROOT.  Nothing needs this exact path
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
nohup setsid env T1_SUB=1 T1_PREVIEW=front,side,hero34f,hero34r T1_PFX=r78 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r78.log 2>&1 < /dev/null &
```
**`grep -c Saved: /tmp/r78.log` must be 4**, ~5.5 min a frame. `setsid`, not a bare `nohup &` (F173).
**`out/` DOES NOT EXIST on a clone** — re-render before quoting any frame. **DO NOT EDIT `build.py` OR
THE `t1_*` MODULES WHILE THE QUEUE RUNS** (probes, `.md` and the design scripts are fine).

## §0b BEFORE YOU MEASURE ANYTHING
```bash
python3 photometry.py          # 9 checked, 0 FAILED
```
**READ LINEAR / REFUSE CLIPPED / MEDIAN NOT MEAN / PAINT THE WINDOW. Import it; do not re-derive it.**

**AND MEASURE THE BRANCH, DO NOT TRANSCRIBE IT, INCLUDING THIS SENTENCE:**
```bash
git fetch --all --prune
for b in $(git branch -r | grep -v HEAD); do printf "%-52s ahead %-3s behind %s\n" "$b" \
  "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"; done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
```
⚠ **NAME YOUR BRANCH: rev 77 worked on `claude/rev-76-concept-growth-gcrew8`, named for the PREVIOUS
revision. Decide where rev 78's work belongs and say so in your ledger.** At rev 77's pickup
`bootstrap.sh` row **9** PASSED, HEAD was 0 ahead / 0 behind `origin/main`, and the diff was empty.
**The "N consecutive revisions" count in every brief is HAND-INCREMENTED. Believe row 9 and the loop.**

---
## §1 ⚠ **T3 IS DECIDED. THE VERIFIER NO LONGER TURNS ON RENDER LUCK.**

**F334.** The rev-76 brief ranked *"DECIDE T3"* first and named the missing input: five or six side
renders of one tree. **Rev 77 rendered five and read the ladder off each BY NAME** — which needed
giving `probe_rev73_tailboard.py` a frame argument, something it never had, and which is why a
distribution across frames had never been measured.

⚠ **THESE FIVE READINGS ARE A RECORD, NOT FILES YOU CAN RE-READ. `out/` is untracked and §0 renders
ONE side frame, so `probe_rev77_t3floor.py` will print `n = 1` and `sd n/a (n=1)` on your tree. TO
REPRODUCE §1 YOU MUST RENDER FIVE `side` FRAMES — ~25 minutes.** ⚠ **AND THE FLOOR PARAGRAPH INSIDE
T3's OWN MESSAGE IS A HARDCODED STRING LITERAL, printed on every frame of every tree — F320f's class
(*"T6's FLOOR IS STILL A STRING LITERAL"*), now with a second instance.**

```
  the -7.0 rung, FIVE renders of ONE tree, no source change:  -8.75 -8.75 -6.50 -9.00 -6.50
      range 2.50 deg, sd 1.282 deg, on a rung whose bar is 1.5.   2 PASS / 3 FAIL
  PER-RUNG sd over the same five frames:
      -7.0  1.282   +3.0  0.326   +5.0  0.112   +7.0  0.224   +10.0  0.285
  MONOTONIC in 5 renders of 5.
```
**THE INSTABILITY IS ONE RUNG OF FIVE AND NOBODY HAD EVER LOOKED AT THE OTHER FOUR.** That rung is now
**REPORTED WITHOUT GATING**, carrying `[UNGATED -- BELOW ITS OWN FLOOR]` in the row's own message.
**NO BAR WAS RELAXED** and **MONOTONICITY WAS ADDED**. ⚠⚠ **BUT DO NOT READ THAT AS A
STRENGTHENING, AND REV 77's FIRST DRAFT DID — RETRACTED (rule 13), caught by its own rule-17
adversary.** Run over rev 77's five ladders, **the OLD condition passes 2 of 5 and the NEW passes
5 of 5: three flip FAIL→PASS and none flips back.** The two are **INCOMPARABLE, not ordered**, and on
this tree the change is a **NET LOOSENING**; monotonicity is near-vacuous here, the rungs never coming
within 1.75° of crossing. **The re-base is still defensible — the ungated rung IS below its own noise
— but not on the word that licensed it under rule 44.** ⚠ **AND "UNGATED" IS A HAIR TOO STRONG:
`_mono` runs over the FULL ladder, so a −7.0 reading of +5.0 would still red the row. It is
TOLERANCE-ungated.** **Watched failing on seven fabricated ladders**; four companion rows.

⚠ **AND F324's *"TWO DISJOINT CLUSTERS"* IS REFUTED (rule 13).** It attributed −9.00/−9.00/−8.75 to
rev 74's tree and −7.00/−8.50/−6.50 to rev 75's and called it a BUILD-dependence. **One tree — this
one, unchanged — produced −9.00 AND −8.75 AND −6.50.** ⚠ **STATE IT AT ITS TRUE STRENGTH: that refutes
DISJOINTNESS AS EVIDENCE. It does NOT test build-dependence — rev 77 rendered neither the no-tread nor
the irregular-tread build. "NO EVIDENCE OF build-dependence", not "no build-dependence".** ⚠ **AND THE
MECHANISM IS UNCHANGED: `verify_clone.sh` still calls the probe BARE, so it still reads the
alphabetically-last side frame. Only the margin widened.**

⚠⚠ **THE GAIN CLAIM: REV 77 WITHDREW IT AND THE WITHDRAWAL WAS WRONG. RETRACTED (rule 13).**
0.967 / 0.979 / 0.936 / 0.935 / 0.893 — mean 0.942, sd 0.033, departure from 1.000 **0.0579**. The
first draft divided that by the sd of **INDIVIDUALS**, got **1.727**, printed *"1.8 σ"* and called it
not a result. **THE SCALE FOR A MEAN IS THE SEM** — `sd/√5 = 0.0150` — **giving 3.86 σ**; excluding
the −7.0 rung this row itself calls unusable, **mean 0.8955, departure 0.1045, 7.00 σ on the SEM.**
**THE SUB-UNITY GAIN IS ESTABLISHED ON THIS TREE and T3 MAY quote it.** CEILING: n = 5, one tree.
⚠ **A HYPOTHESIS, NOT A FINDING: −7.0 is the ONLY NEGATIVE rotation in the ladder. n = 1, confounded
with magnitude and order, UNTESTED. Add a −3.0 and a −10.0 rung. It is cheap.**

---
## §2 RANKED WORK FOR REV 78

**RANK BY PIXELS OF THE DELIVERY FRAME** — `python3 visibility_budget.py 3840 out/r78_hero34f.png` —
**and the owner outranks the ranking.** ⚠ **READ THAT TABLE'S OWN CEILING: *"pixels are not visibility
… catch ORDERS OF MAGNITUDE, not rank neighbours."*** The ranked list is `REMAINING_WORK_rev61.md`,
triaged into `ROADMAP_rev68.md`.

### **1. DRAW THE STICKER. F18. HE FIRED IT AND NOTHING BLOCKS IT.**
It is the register's oldest live row, the project's original deliverable, and **the only artefact with
an owner-locked style, a locked scene, a named audience and a written spec.** The style is his own
recovered sentence: *"cartoon with rendered depth — vector line and flat colour, shading and occlusion
sampled from the 3D asset."* **The line half is BUILT (`line_pass.py`).** ⚠ **THE OCCLUSION HALF IS
NOT: there is still no normal pass and no AO pass. Build that first or the sticker is line only.**
⚠ **`AUDIT_rev43.md`'s sticker spec survives only TRUNCATED — 8 rows hard-cut. Read it, do not assume.**

### **2. THE CHILDREN'S LINE. F331 MAKES IT HALF THE PROGRAMME AND IT DOES NOT EXIST.**
`CONCEPT_BENCH_rev77.md`'s `THE CHILD'S EYE` slot has three concepts. **He has now ruled twice that
children are an audience — the F18 spec's *"spark joy … for children"* and F331.** Nothing has been
made for them.

### **3. THE GARMENT SLOT FAILED AND IT IS THE MOST INTERESTING FAILURE IN THE ROUND.**
⚠ **ONE director, three concepts — NOT three directors, and rev 77's first draft said three in two
documents. Corrected (rule 13).** That slot was aimed straight at *"cut-and-sew — the belt line as a
SEAM, not a print"*, which the rev-76 critic called **"the only genuinely premium object in the whole
document"**, and it **screened 5.07 — the lowest BEST-of-slot of all 25; its MEAN is 4.58 (5.07 /
4.67 / 4.00), also the lowest.** ⚠ **THE RANKING SURVIVES, THE EVIDENTIAL WEIGHT DOES NOT: a negative
result over three attempts by ONE director is far weaker than over three independent ones. Re-run it
with three directors before concluding anything.**

### **4. F318 — THE TREAD'S ONE MEASURED COST — IS STILL OPEN AND ITS FIX IS PRESCRIBED AND UNDONE.**
`probe_rev70_tyre.py`'s T2 moves **0.2457 → 0.2558** between the no-tread and shipped-tread builds,
**25× its measured 0.0004 two-render floor**. ⚠ **DO NOT "FIX" IT BY LOWERING `T1_TYRE_FILM`.**
**THE PRESCRIBED FIX: give T2 a band MEASURED to lie inside the rubber (PAINT IT FIRST, rule 8) and
re-read both frames.** Neither frame is on your tree — `out/r74_side.png` is a `side` render with
`T1_TYRE_TREAD=0`; the other is just HEAD rendered.

### **5. THE EMBLEM.** His ninth report. **0.8528 against P1b's ceiling of 0.9465 and the objective
STILL HAS NO LEGIBILITY TERM (rule 56).** F314 closes the WEIGHT to tuning but does NOT resolve it.
⚠ **AND ONE NEW OBSERVATION AT ITS TRUE STRENGTH (F333): THE VW BADGE TRACES CLEANLY AND IS LEGIBLE
IN LINE.** One object, one scale, one view. **NOT a claim the emblem is fixed. F191 and F234 stand.**

### **6. F156 — the `Senor` gate row scores a DELIBERATE DEPARTURE.** Unacted (rule 40). **Read the
grade, not any of the four different revision-counts the carriers give for it.**

---
## §3 WHAT REV 77 SETTLED — **DO NOT RE-OPEN ANY OF IT**

⚠ **AND READ THE INSTRUMENT BEFORE THE WORD: `revstats.py` reads rev 77 as `0 findings closed`, and
THAT IS ACCURATE.** Every rev-77 row is graded `RULED-rev77` or `MEASURED-rev77`; not one row was
RETIRED or marked CLOSED. Rev 77 **refuted, superseded and corrected** rows — it did not retire any.
*(The first draft of this heading said CLOSED and contradicted the instrument it tells you to run.
Corrected, rule 13.)* **The five-revision line still reads `73–77: 261 geometry lines, 0 findings
closed`. Rev 78 should close something.**

| closed | the result |
|---|---|
| **T3 / F324 (F334)** | **DECIDED.** One rung of five is below its own floor and is now UNGATED; no bar relaxed; monotonicity ADDED; F324's cluster claim REFUTED by one tree producing both. `verify_clone.sh`'s total no longer depends on which side frame is alphabetically last. |
| **THE LINE PASS (F332)** | **BUILT.** Grease Pencil Line Art → polylines → SVG. `source_type='COLLECTION'` is a SILENT NO-OP — it returns FEWER points over an UNFILTERED window; the route is `OBJECT` over a joined duplicate. Caught by DRAWING 718 "wheel" strokes and seeing a complete bus. |
| **THE RINGS (F333)** | Line art fragments any edge on a near-tangent surface and no chaining setting repairs it. The rings are MEASURED off the stroke cloud instead, cross-checked against four independent source constants to within 0.8 mm, and watched refusing on the ablated pass. |
| **F330 / F331** | **TWO OWNER RULINGS.** See the head of this file. |
| **F335 / F336** | A carrier pointing outside the repository; and the pillar thesis, which `AUDIT_rev43.md` already refuted harder than rev 76's retraction did. |

## §3b ⚠ REV 72–77's FIXES ARE LOCKED. YOU CANNOT REGRESS THEM SILENTLY.
**A red row is a FINDING ABOUT YOUR CHANGE. A re-base needs the cause NAMED and a companion row making
that cause separately testable.** Rev 77 re-based THREE rows and all three carry their cause and companions:
T3's condition in the probe (four companions, the first an arithmetic kill over seven fabricated
ladders); the sticker presence row (three companions, one a watched kill); and `verify_clone.sh`'s
SKIPPED bound, 5 → 6, forced by F337 (one companion, which derives the number from source).
⚠ **The first draft of this line said TWO. Counted, not transcribed — this project's own record names
"four, five and six in one document" as a defect class.** **RUN `./bootstrap.sh --guards` ONCE THIS
REVISION — ~20 min, and not while a render queue is going.**

---
## §4 THE MACHINE

```bash
./bootstrap.sh                                # READ ROW 9.  Row 10 is verify_clone.sh
./verify_clone.sh                             # ALL 445 PASS -- 0 FIDELITY, 445 SELF-CONSISTENCY.
  # With an empty out/, SIX rows SKIP and say UNGUARDED; PASS is the same either way.
  # (it was five before rev 77 added F334's sixth -- the guard that bounds this is a
  #  literal, so a companion row DERIVES the six from the source and they must agree)
  # READ THE VERDICT BLOCK: not one row measures the vehicle against a photograph
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
python3 photometry.py                         # 9 checked, 0 FAILED
python3 probe_rev73_tailboard.py out/r78_side.png   # NEW AT REV 77: IT TAKES A FRAME.
  # 5 checked, 1 FAILED -- T4 only, BY DESIGN.  T3 no longer flips.  Bare, it reads the
  # alphabetically-last side frame, unchanged.  With no out/: 0 checked, 0 FAILED, 2 ABSENT
python3 probe_rev77_t3floor.py                # NEW.  T3's rung off EVERY side frame, with its sd
python3 line_pass.py --view side --wheel front --out probe_scratch/rueda   # NEW.  ~25 s
python3 la_rueda.py probe_scratch/rueda.json  # NEW.  14 checked, 0 FAILED
python3 sheet3_notissued.py                   # NEW.  45 checked, 0 FAILED
python3 probe_rev74_tread.py out/r78_side.png # 8 checked, 0 FAILED.  NAME YOUR FRAME
T1_TYRE_TREAD=0 python3 probe_rev74_tread.py  # THE KILL.  IT REDS **TWO** ROWS: T3 and T7
python3 probe_rev67_nose.py out/r78_front.png # ⚠ FRAME-DEPENDENT.  NO document may state a count
python3 probe_rev46_vw.py                     # 12 checked, 2 FAILED -- C4 AND C10 (F304)
python3 probe_rev69_fitpose.py                # 5 checked, 1 FAILED -- P4 only.  ⚠ P1's MESSAGE
  # hardcodes a 0.9703 ceiling while P1b prints 0.9465; read the NUMBERS, not the prose
python3 gloss_compare.py out/r78_hero34f.png  # FAILS (bar 0.60)
python3 flank_compare.py out/r78_side.png /tmp/fc.png   # FAILS
python3 probe_rev71_proxy.py                  # must read IoU 1.000000
python3 probe_rev70_tyre.py out/r78_side.png
  # ⚠⚠ IT REPAINTS TRACKED FILES, AND SO DO 16 OTHERS (F329).  THE RULE, NOT THE LIST:
  #   git status --porcelain ; git checkout -- probe_scratch/
python3 visibility_budget.py 3840 out/r78_hero34f.png ; python3 revstats.py
T1_SUB=2 /tmp/blender/blender -b -P audit.py            # rewrites STATE.md -- COMMIT FIRST,
  # and do it AFTER your LAST source edit.  ⚠ sheet3_notissued.py READS STATE.md, so
  # REGENERATE THE SHEET AFTER regenerating STATE.md or it goes stale
python3 audit_brief.py ; python3 audit_adversary.py     # rules 15/17, MECHANICAL half only.
  # audit_brief's count row is red BY CONSTRUCTION until --fix-count runs LAST
```

**THE ABLATIONS.** `verify_clone.sh` runs the `T1_REAR_*` block, `T1_NOSE_NOWIN`, `T1_VW_FREE` and
`T1_TYRE_TREAD`. **NEW AT REV 77: `T1_LINE_NOCONTOUR=1` and `T1_LINE_NOCREASE=1`** ablate the line
pass — contour off takes the front wheel from **462 strokes / 1453 points to 115 / 312**, watched.

**FACTS THAT BITE:** the render is **not** run-to-run deterministic — floor **~2.04 %** of pixels >8
levels on hero34f at 1600×1100/96 spp. `lid_gen.py` / `script_gen.py` are **not** called by
`build.py`. `audit.py` rewrites `STATE.md` — **commit first**. `ck` in `verify_clone.sh` collapses
whitespace. **A backgrounded runner's `rc=$?` is the redirect's.** `bpy` is a pip module, so most
probes run in ~1 s. ⚠ **`lineart_bake_strokes()` bakes the WHOLE SCENE FRAME RANGE** — rev 77's first
spike wrote 5,060,569 points across 250 identical frames; `line_pass.py` pins it to one.

---
## §5 THE RULES THAT WILL BITE YOU

⚠⚠ **THERE ARE TWO INCOMPATIBLE CANONS FOR RULES 1–33 AND EVERY BRIEF BEFORE REV 76 SENT YOU TO THE
WRONG ONE.** **`CLAUDE.md`'s own numbered list (1–18) IS THE ONE IN FORCE** and is what LIVE SOURCE
means. `NEXT_CONTEXT_PROMPT_rev50.md` §11 carries a DIFFERENT numbered 1–33 and **the numbers
COLLIDE** — its rule 3 is *"read the summary line"* where `CLAUDE.md`'s rule 3 is *"a control is
finished when you have WATCHED IT FAIL"*. **For rules 1–18 read `CLAUDE.md`. Rules 34–58 are in
`HANDOFF_CARRIERS.md` §5 — whose own first line says 34–52, and which contains TWO different rule 56s
and TWO different rule 57s. Say which you mean.**

**55 — EVERY REVISION SHIPS A VISIBLE CHANGE TO THE VEHICLE, OR SAYS PLAINLY WHY IT COULD NOT**, at
the TOP of its ledger. ⚠ **REV 77 IS THE FIRST REVISION WHERE THAT RULE'S LETTER AND ITS PURPOSE COME
APART, AND IT SAYS SO RATHER THAN QUIETLY REINTERPRETING IT.** The vehicle did not move; two finished
artefacts were shipped and the owner can look at both. **The redirect at rev 76 is what pulls them
apart. A future context should decide whether rule 55 needs a second clause for the design programme
— do NOT assume rev 77's ledger settled it.**

Which bit rev 77: **1** (the COLLECTION no-op was caught by LOOKING, never by a count), **3**, **5**,
**8**, **9**, **13** (three retractions: F324's clusters, F335's overstatement, my own "BOTH
MEASURED"), **37**, **44**, **49**, **50** (twice — a grep-count guard that failed on the register
carrying MORE of what it protects, and a grep whose pipes were literal), **55**.

---
## §6 WHERE EVERYTHING ELSE LIVES

| file | what it holds |
|---|---|
| **`CONCEPT_BENCH_rev77.md`** | **THE CARRIER. All 75 concepts in full, both completeness critics, the register table's raw material. 510 KB. Do not compact it.** |
| **`DESIGN_PROGRAM_rev77.md`** | ranks and decides: the register table, the top-16 shortlist, and what the round did NOT fix |
| `DESIGN_PROGRAM_rev76.md` | rev 76's program. **Its §3 still prints the retracted `109.5 \| 129.5` — see F336** |
| **`HANDOFF_CARRIERS.md`** | every carrier: the goal, the reference set, the refuted emblem routes, §4 the owner's rulings, §5 rules 34–58, the horizon |
| `OPEN_FINDINGS.md` | the register. **F330–F336 are rev 77's.** It outranks prose |
| `STATE.md` | machine-written; outranks every prose description |
| `LEDGER_rev77.md` | what rev 77 did, **including what it got wrong, written BEFORE the closing audits** |
| `EMBLEM_HANDOFF.md`, `SPEC.md`, `REF_MEASUREMENTS.md`, `SURVEY_rev49_photoreal.md`, `ROADMAP_rev68.md`, `PANEL_rev61.md`, `REMAINING_WORK_rev61.md`, `PHOTOS_WANTED_rev49.md`, `PHOTOS_WANTED_rev52.md` | large; load the one the task needs |

**⚠ IDs LEANED ON WITHOUT NAMING, SO A GREP FINDS THEM (rule 16): `F21`, `F71`, `F92`, `F104`, `F163`,
`F165`, `F173`, `F183`, `F188`, `F191`, `F192`, `F193`, `F205`, `F229`, `F234`, `F241`, `F252`,
`F262`, `F276`, `F281`, `F284`, `F289b`, `F296`, `F301`, `F302`, `F303`, `F305`, `F308`, `F309`,
`F311`, `F312`, `F316`, `F317`, `F319`–`F323`, `F325`–`F329`.**

---
## §7 HOW TO CLOSE

**HIS STANDARD:** photo-real parity with **that exact bus**, in service of a promotional render.
**Any single measurement off is unacceptable** — per-measurement, not on average. **Never call it done
off self-review. Report the measurement with its ceiling. Do not say anything is ready.**

1. `./bootstrap.sh` and `./verify_clone.sh` on a **clean** tree. **All-PASS IS reachable and is now
   STABLE — T3 no longer flips (F334).** The honest closing condition: **every red is one you can
   name, and none of them is yours.**
2. `python3 revstats.py` — **put its geometry/closure line in the ledger header; if the revision
   shipped nothing, say so at the TOP** (rule 55).
3. Regenerate `STATE.md` (`T1_SUB=2 … audit.py`) — **commit first, and AFTER your LAST source edit.**
   **Then REGENERATE THE DESIGN ARTEFACTS, which read `STATE.md`.** Then `audit_adversary.py`.
4. **DISPATCH an adversary at the brief you WROTE (rule 17), and one at the brief you RECEIVED
   (rule 15). DO NOT CLOSE UNTIL BOTH REPORT.** ⚠ **RE-RUN THE OUTGOING ONE AFTER ANYTHING SHIPS.**
5. **Keep the split, and KEEP THIS FILE SHORT.** `cp` it over `PASTE_INTO_CLAUDE_CODE.txt` in the same
   commit. `python3 audit_brief.py --fix-count` LAST.
6. ⚠⚠ **THEN COLD-CLONE AND RUN `./bootstrap.sh` — LAST, ON A FRESH CLONE (F328).**
7. ⚠ **AND COMMIT ANY CONCEPT ROUND'S OUTPUT IN FULL, IN THE REPOSITORY, IN THE SAME COMMIT THAT
   ANNOUNCES IT (F335). If it is not in `git ls-files`, it does not exist.**

---
**⚠ THIS BRIEF WAS AUDITED AGAINST THE MACHINE.** The rule-15 adversary on the INCOMING brief returned
**20 defects**, of which the ledger lists **six** at top severity *(its §5 describes one, then heads a
list "THE OTHER TOP FOUR" and numbers five under it — the header is wrong, the list is right)*, and
one of them was **in an artefact rev 77 had already shipped**: the Sheet 3
title block printed its inks as *"BOTH MEASURED"* when `lid_gen.py` says the ink is an AUTHORED
darkening of a measured median. **Fixed in the same revision (rule 13), and the same pass made the
sheet stronger** — it now carries the owner's own *"cannot tell from this crop"* reading of that
elevation, which was in `SPEC.md` all along and unused. The full account is in `LEDGER_rev77.md`.

**WHERE THIS BRIEF IS WEAKEST, STATED RATHER THAN HIDDEN:**
* **THE AUDIT AND AMPLIFY STAGES OF THE CONCEPT ROUND ARE INCOMPLETE** — a session limit. **No concept
  in the shortlist has been through all four adversarial lenses, so NO RISK CLAIM IN IT HAS BEEN
  ADVERSARIALLY TESTED.** The screen ranking is three machine lenses and nothing else.
* **NOTHING FROM THE CONCEPT ROUND HAS BEEN SHOWN TO THE OWNER.**
* **THE OCCLUSION HALF OF THE OWNER'S OWN STYLE SENTENCE IS NOT BUILT.** No normal pass, no AO pass.
* **T3's GAIN CLAIM IS 1.8 σ** and may not be quoted to refute the photograph rows' error model.
* **THE EMBLEM IS NOT RIGHT.** 0.8528 against P1b's 0.9465, no legibility term, nine reports.
