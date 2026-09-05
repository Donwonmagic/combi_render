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
> **THIRD — A LOCATIONAL SERIES HE FLOATED. F340 / F341. NOT A RULING, AND THIS BRIEF CALLED IT ONE
> (corrected, rule 13).** *"I also want to **maybe** make a locational series. Starting with the main
> hero, Bethesda. Or taqueria Buena Bethesdita. Also one for Arlington Taqueria El Cristal."*
> F340 says in terms: ***"a DIRECTION HE FLOATED, not a ruling he made"*** — and the register outranks
> prose. **F341's two rulings are real but govern HOW, not THAT, still less FIRST. F18 is the one he
> actually fired. RANK THEM YOURSELF.** The generator is **HISPANICISE THE NEIGHBOURHOOD** — Bethesda →
> *Buena Bethesdita*. ⚠ **CRYSTAL CITY → *EL CRISTAL* IS THE ASKER'S INFERENCE, NOT HIS WORDS. If it is
> wrong the whole generator is wrong — CONFIRM IT BEFORE PRINTING IT AS THE SYSTEM'S RATIONALE.**
> **HE RULED ON EXECUTION: missing glyphs DRAWN AND LABELLED AUTHORED; the NAME is the system, across
> name board, per-site plate and table item, format per site.** ⚠ **BUT THE FIRST QUESTION'S FRAMING WAS
> BORROWED FROM ANOTHER OBJECT (rule 34): he was asked under `SPEC.md` §10.10's *"hard bar"*, quoted
> accurately — but §10.10 governs *"every painted element ON THIS VEHICLE"* and its table is eight
> painted elements of the combi. A shop sign in Bethesda is not one. The ruling may survive re-framing;
> the framing needs stating to him.**
>
> **REV 77's JOB WAS §9 OF THE REV-76 PROGRAM: GROW THE IDEAS BEFORE EXECUTING THEM. IT RAN** — 75
> concepts, 25 directors at `xhigh`, all 13 named-absent registers filled, **COMMITTED IN FULL in
> `CONCEPT_BENCH_rev77.md`.** Rev 76's bench was not committed and its bodies are gone (F335).
> **If it is not in `git ls-files`, it does not exist.**

**REV 77 SHIPPED NO VEHICLE GEOMETRY AND SAYS SO AT THE TOP OF ITS LEDGER (rule 55).** What it shipped
is **THREE finished artefacts and the capability under them** — `design_out/sheet3_not_issued.svg`,
`design_out/loteria_la_rueda.svg` and **`design_out/calendario_ano_xxii.svg`** — plus `line_pass.py`,
`sheet.py`, `la_rueda.py`, `calendario.py`. ⚠ **THE CALENDAR WAS MISSING FROM BOTH HANDOFF DOCUMENTS
UNTIL THE FINAL AUDIT (F344): rule 55's own statement of what the owner can LOOK AT omitted one of the
three things he can look at, and the register row owed for its known defect was lost when F341 was
assigned twice. It carries a live defect — read F344 BEFORE showing it to him.**
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
## §1 ⚠ **T3 IS DECIDED (F334). THE VERIFIER NO LONGER TURNS ON RENDER LUCK.**

**SETTLED — §3 says do not re-open it. The FULL account is F334 in `OPEN_FINDINGS.md` and
`LEDGER_rev77.md`; this section is the part you must not mis-cite.** Rev 77 rendered five `side`
frames of ONE unchanged tree and read the ladder off each BY NAME, which needed giving
`probe_rev73_tailboard.py` a frame argument it never had — the reason a distribution had never been
measured.

```
  the -7.0 rung, FIVE renders of ONE tree, no source change:  -8.75 -8.75 -6.50 -9.00 -6.50
      range 2.50 deg, sd 1.282 deg, on a rung whose bar is 1.5.   2 PASS / 3 FAIL
  PER-RUNG sd:  -7.0 1.282   +3.0 0.326   +5.0 0.112   +7.0 0.224   +10.0 0.285
  MONOTONIC in 5 of 5.
```
⚠ **THESE ARE A RECORD, NOT FILES YOU CAN RE-READ. `out/` is untracked and §0 renders ONE side frame,
so `probe_rev77_t3floor.py` prints `n = 1` on your tree. REPRODUCING §1 COSTS FIVE RENDERS, ~25 min.**
⚠ **AND T3's OWN FLOOR PARAGRAPH IS A HARDCODED STRING LITERAL on every frame of every tree — F320f's
class, second instance.** ⚠ **`probe_rev77_t3floor.py` ALSO DROPS A FRAME IT CANNOT PARSE WITHOUT
SAYING SO: six `*_side.png` on the rev-77 tree, `n = 5` printed, `fierro_side.png` silently discarded
because its ladder would not parse — and that is the frame where the detector failed HARDEST. The
distribution is CONDITIONED ON BEING READABLE. Rule 37; unfixed.**

**THE INSTABILITY IS ONE RUNG OF FIVE AND NOBODY HAD LOOKED AT THE OTHER FOUR.** That rung is now
reported **TOLERANCE-ungated** (`_mono` still runs the FULL ladder, so a wild reading still reds it);
**no bar was relaxed, monotonicity was ADDED**, watched failing on seven fabricated ladders, four
companion rows. ⚠⚠ **DO NOT READ THAT AS A STRENGTHENING — rev 77's first draft did. RETRACTED
(rule 13).** Over those five ladders **the OLD condition passes 2 of 5 and the NEW passes 5 of 5**:
INCOMPARABLE, not ordered, and on this tree a **NET LOOSENING**; monotonicity is near-vacuous, the
rungs never coming within 1.75° of crossing. The re-base is defensible — the ungated rung IS below its
own noise — **but not on the word that licensed it under rule 44.**

⚠ **F324's *"TWO DISJOINT CLUSTERS"* IS REFUTED (rule 13):** one unchanged tree produced −9.00 AND
−8.75 AND −6.50 across what it called two builds. **TRUE STRENGTH: that refutes DISJOINTNESS AS
EVIDENCE; it does NOT test build-dependence — neither the no-tread nor the irregular-tread build was
rendered. And the MECHANISM is unchanged: `verify_clone.sh` still calls the probe BARE.**

⚠⚠ **THE GAIN CLAIM: REV 77 WITHDREW IT AND THE WITHDRAWAL WAS WRONG. RETRACTED (rule 13).**
0.967 / 0.979 / 0.936 / 0.935 / 0.893 — mean 0.942, sd 0.033, departure 0.058. The first draft divided
that by the sd of **INDIVIDUALS**, printed *"1.8 σ"*, and called it not a result. **THE SCALE FOR A
MEAN IS THE SEM** (`sd/√5 = 0.0150`) → **3.86 σ** (re-deriving from the five printed gains gives 3.88;
an unexposed rounding chain, and the frames are gone). ⚠ **The 7.00 σ variant rests on `mean 0.8955`,
which is NOT a subset mean of those five — none is below 0.9328 — but a DIFFERENT quantity the probe
never prints. Check it against the probe, not the list.** **THE SUB-UNITY GAIN IS ESTABLISHED ON THIS
TREE and T3 MAY quote it.** CEILING: n = 5, one tree. ⚠ **HYPOTHESIS, NOT FINDING: −7.0 is the only
NEGATIVE rotation — n = 1, confounded with magnitude and order. A −3.0 and a −10.0 rung would separate
sign from magnitude cheaply; offered, not instructed.**

---
## §2 RANKED WORK FOR REV 78

**RANK BY PIXELS OF THE DELIVERY FRAME** — `python3 visibility_budget.py 3840 out/r78_hero34f.png` —
**and the owner outranks the ranking.** ⚠ **READ THAT TABLE'S OWN CEILING: *"pixels are not visibility
… catch ORDERS OF MAGNITUDE, not rank neighbours."*** The ranked list is `REMAINING_WORK_rev61.md`,
triaged into `ROADMAP_rev68.md`.

### **1. THE LOCATIONAL SERIES — BETHESDA FIRST. F340 / F341. THIS IS THE LIVE DIRECTION.**
**He raised it himself — with the word *"maybe"*. It is the only item on this list he raised at all,
and it is not the only one he ruled on.** Bethesda is the hero and would set the format for every site
after it. **The measured constraint is done for you: `script_gen.py` is NOT a font** — seven separable
glyphs plus `Señor` as ONE composite.

⚠⚠ **AND THE INVENTORY IS CASE-SENSITIVE, WHICH EVERY EARLIER STATEMENT OF IT MISSED. CORRECTED
(rule 13).** `script_gen.py` holds **ONE CAPITAL AND SIX LOWERCASE** — `draw_T`'s docstring says
*"Capital T"*; `draw_a` (*"The `a` was a solid ellipse"*), `draw_c`, `draw_o`, `draw_m`, `draw_b`,
`draw_i` (*"the `i` is ONE connected stroke"*) are lowercase letterforms. So the hand is `T a c o m b i`
— exactly the letters of *Tacombi*, in the case *Tacombi* uses. **The published missing sets reproduce
ONLY under case-INSENSITIVE matching, against names this brief prints in CAPITALS:**
```
                                distinct   MISSING as caps        (the old case-blind figure)
    TAQUERIA EL CRISTAL            10       9:  A C E I L Q R S U      was 6:  E L Q R S U
    TAQUERIA BUENA BETHESDITA      12      11:  A B D E H I N Q R S U  was 8:  D E H N Q R S U
```
**AND THERE IS NO MIXED-CASE ESCAPE:** any capitalised second word needs a capital `C`, `E` or `B`,
none of which exists. ⚠ **THE OWNER'S RULING STANDS; THE QUANTITY HE WAS GIVEN DOES NOT** — he was
shown "six to eight" for a setting that needs nine to eleven. **Tell him the corrected figure.**
**HE RULED: draw them, label them AUTHORED — on the artefact, not just in a comment.** Rev 77 already
shipped one sheet that called an authored ink MEASURED and had to correct it in the same revision.
**THE RECOVERY IS WORTH WEIGHING BEFORE THE INVENTION, AND IT IS YOUR CALL, NOT THIS BRIEF'S:**
segmenting the `Señor` composite recovers glyphs from the PHOTOGRAPH rather than authoring them.
⚠ **BUT PRICE IT CASE-EXACTLY: the composite is lowercase `S e ñ o r` bar its capital `S`, so against a
CAPITALISED setting it recovers `S` and `R`'s lowercase cousin only — it does NOT deliver `E Ñ O R` as
caps.** ⚠ **AND F340's OWN RESIDUAL LIST IS WRONG: it says removing `S E ñ o r` leaves `Q U L D H`;
recomputed for BUENA BETHESDITA it leaves `D H N Q U` — the register drops `N` and imports `L`, which
belongs to EL CRISTAL. Both are length 5, so the "eight to five" count is right BY ACCIDENT and the
letters are not.** Corrected here and in F340 (rule 13).
⚠ **AND THE SERIES CROSSES BOTH LINES, so F331 bites per CARRIER, not once: a name board is adult, a
table item is the children's line that is owed and still empty.**

### **2. DRAW THE STICKER. F18. HE FIRED IT AND NOTHING BLOCKS IT.**
It is the register's oldest live row, the project's original deliverable, and **the only artefact with
an owner-locked style, a locked scene, a named audience and a written spec.** The style is his own
recovered sentence: *"cartoon with rendered depth — vector line and flat colour, shading and occlusion
sampled from the 3D asset."* **The line half is BUILT (`line_pass.py`); the occlusion half is NOT —
no normal pass, no AO pass.** ⚠ **AN EARLIER DRAFT SAID *"Build that first or the sticker is line
only"*. THAT WAS A DICTATED BUILD ORDER, NOT A MEASUREMENT, and `CONCEPT_ROUND_rev77.md` §5.2 argues
the opposite — the daylight face first, BECAUSE it needs no occlusion. Gating the project's original
deliverable on an infrastructure job the day its trigger was fired is your call to make, not this
brief's.**
⚠ **`AUDIT_rev43.md`'s sticker spec survives only TRUNCATED — 8 rows hard-cut. Read it, do not assume.**

### **3. THE CHILDREN'S LINE. F331 MAKES IT HALF THE PROGRAMME AND IT DOES NOT EXIST.**
`CONCEPT_BENCH_rev77.md`'s `THE CHILD'S EYE` slot has three concepts. **He has now ruled twice that
children are an audience — the F18 spec's *"spark joy … for children"* and F331.** Nothing has been
made for them.

### **4. THE GARMENT SLOT FAILED AND IT IS THE MOST INTERESTING FAILURE IN THE ROUND.**
⚠ **ONE director, three concepts — NOT three directors, and rev 77's first draft said three in two
documents. Corrected (rule 13).** That slot was aimed straight at *"cut-and-sew — the belt line as a
SEAM, not a print"*, which the rev-76 critic called **"the only genuinely premium object in the whole
document"**, and it **screened 5.07 — the lowest BEST-of-slot of all 25; its MEAN is 4.58 (5.07 /
4.67 / 4.00), also the lowest.** ⚠ **THE RANKING SURVIVES, THE EVIDENTIAL WEIGHT DOES NOT: three
attempts by ONE director is far weaker evidence than three independent ones — so the slot's last place
is not established. How to fix that is yours.**

### **5. F318 — THE TREAD'S ONE MEASURED COST — IS STILL OPEN AND ITS FIX IS PRESCRIBED AND UNDONE.**
`probe_rev70_tyre.py`'s T2 moves **0.2457 → 0.2558** between the no-tread and shipped-tread builds,
**25× its measured 0.0004 two-render floor**. ⚠ **DO NOT "FIX" IT BY LOWERING `T1_TYRE_FILM`** — that is earned.
The rest is a SUGGESTION carried unchanged and undone for three revisions, which is evidence it is not
landing: give T2 a band measured to lie inside the rubber (PAINT IT FIRST, rule 8), or build a better
instrument. Neither frame is on your tree — `out/r74_side.png` is a `side` render with
`T1_TYRE_TREAD=0`; the other is just HEAD rendered.

### **6. THE EMBLEM.** His ninth report. **0.8528 against P1b's ceiling of 0.9465 and the objective
STILL HAS NO LEGIBILITY TERM (rule 56).** F314 closes the WEIGHT to tuning but does NOT resolve it.
⚠ **AND ONE NEW OBSERVATION AT ITS TRUE STRENGTH (F333): THE VW BADGE TRACES CLEANLY AND IS LEGIBLE
IN LINE.** One object, one scale, one view. **NOT a claim the emblem is fixed. F191 and F234 stand.**

### **7. F156 — the `Senor` gate row scores a DELIBERATE DEPARTURE.** Unacted (rule 40). **Read the
grade, not any of the four different revision-counts the carriers give for it.**

---
## §3 WHAT REV 77 SETTLED — **DO NOT RE-OPEN ANY OF IT**

⚠ **READ THE INSTRUMENT BEFORE THE WORD: `revstats.py` reads rev 77 as `0 findings closed` and THAT
IS ACCURATE** — every rev-77 row is graded `RULED-` or `MEASURED-rev77`; none was RETIRED. Rev 77
refuted, superseded and corrected. **`73–77: 261 geometry lines, 0 findings closed`. Rev 78 should
close something.** ⚠ **`LEDGER_rev77.md` §7's revstats row is ALREADY STALE (19 commits / 6804 doc);
live is 26 / 8731 / 374 instr. Run the script — the ledger's own heading says nothing in it is
transcribed, and that row is.**

| closed | the result |
|---|---|
| **T3 / F324 (F334)** | **DECIDED — see §1.** `verify_clone.sh`'s total no longer depends on which side frame is alphabetically last. |
| **THE LINE PASS (F332)** | **BUILT.** Line Art → polylines → SVG. ⚠ **`source_type='COLLECTION'` is a SILENT NO-OP** — FEWER points over an UNFILTERED window; the route is `OBJECT` over a joined duplicate. Caught by DRAWING 718 "wheel" strokes and seeing a complete bus, never by a count. |
| **THE RINGS (F333)** | Line art fragments any edge on a near-tangent surface; no chaining setting repairs it. The rings are MEASURED off the stroke cloud, cross-checked to 0.8 mm against four independent source constants, watched refusing on the ablated pass. |
| **F330 / F331** | **TWO OWNER RULINGS.** See the head of this file. **F340 IS NOT A THIRD.** |
| **F335 / F336** | A carrier pointing outside the repository; and the pillar thesis, which `AUDIT_rev43.md` refuted harder than rev 76's retraction did. |
| **F344** | **A THIRD SHIPPED ARTEFACT WAS MISSING FROM BOTH HANDOFF DOCUMENTS, AND ITS OWED REGISTER ROW WAS LOST TO A DOUBLE-ASSIGNED F341.** See the register. |
| **F343** | ⚠⚠ **DO NOT RUN `./verify_clone.sh` TWICE AT ONCE — 20 FIXED `/tmp` PATHS, EACH RUN `rm -f`s THE OTHER'S EVIDENCE.** The failure mode is a **plausible red row** (`got <empty>`, `got 0`), and §3b tells you to read a red row as a finding about YOUR change. **Hit TWICE at rev 77's close, from DISJOINT path sets — mine `442/7` on `_r72*`+`_r73a`, the adversary's `441/4` on `_r73f`. Both `ALL 445 PASS` re-run alone.** ⚠ **THIS BITES rules 15 and 17: an adversary's first act is to run this script, and §7.6's cold clone is a third runner. SERIALISE THEM, or fix it — a `mktemp -d` plus a row that reds on any surviving bare `/tmp/_` path.** |
| **F342** | **YOUR STARTUP LOAD FELL 70 %.** `CLAUDE.md` said `HANDOFF_CARRIERS.md` was NOT imported while an at-sign in that sentence imported it — 111,863 of a 160,208-byte auto-load, now **48,345**. ⚠ **THE CONSEQUENCE IS YOURS: that carrier is no longer free. `cat HANDOFF_CARRIERS.md` WHEN THIS BRIEF POINTS AT IT** — §2's refuted emblem routes, §4's rulings, §5's rules 34–58. |

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
  # count row is red BY CONSTRUCTION until --fix-count runs LAST.  ⚠ IT COVERS 5 OF THE ~9
  # PROBE COUNTS THIS SECTION PUBLISHES -- it is not the rule-17 half, only a piece of it
```

**THE ABLATIONS.** `verify_clone.sh` runs the `T1_REAR_*` block, `T1_NOSE_NOWIN`, `T1_VW_FREE` and
`T1_TYRE_TREAD`. **NEW AT REV 77: `T1_LINE_NOCONTOUR=1` / `T1_LINE_NOCREASE=1`** ablate the line pass
— contour off takes the front wheel from **462 / 1453 to ~115 / 312**, watched. ⚠ **THE ABLATION IS
REAL AND LARGE; THE FIGURE IS ONE DRAW — a re-run gives 116, and the pass is not run-to-run stable.**

**FACTS THAT BITE:** the render is **not** run-to-run deterministic — floor **~2.04 %** of pixels >8
levels on hero34f at 1600×1100/96 spp. `lid_gen.py` / `script_gen.py` are **not** called by
`build.py`. `audit.py` rewrites `STATE.md` — **commit first**. `ck` in `verify_clone.sh` collapses
whitespace. **A backgrounded runner's `rc=$?` is the redirect's.** `bpy` is a pip module, so most
probes run in ~1 s. ⚠ **`lineart_bake_strokes()` bakes the WHOLE SCENE FRAME RANGE** — rev 77's first
spike wrote ~5.06 M points across 250 frames; `line_pass.py` pins it to one. *(An ANECDOTE, not a
figure: the exact count is not re-derivable — the spike is deleted and the pass is unstable.)*

---
## §5 THE RULES THAT WILL BITE YOU

⚠⚠ **TWO INCOMPATIBLE CANONS FOR RULES 1–33, AND EVERY BRIEF BEFORE REV 76 SENT YOU TO THE WRONG
ONE.** **`CLAUDE.md`'s numbered list (1–18) IS IN FORCE.** `NEXT_CONTEXT_PROMPT_rev50.md` §11 carries
a DIFFERENT 1–33 whose numbers COLLIDE. **Rules 34–58 are in `HANDOFF_CARRIERS.md` §5 — whose first
line says 34–52, and which holds TWO rule 56s and TWO rule 57s. Say which you mean.**

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
| **`DESIGN_PROGRAM_rev77.md`** | the register table and a top-16 shortlist. ⚠⚠ **ITS RANKING IS SUPERSEDED AND ITS §4.2 IS STALE** — it still says *"STILL MISSING: 11 of 14 amplifications, the synthesis, and BOTH late critics"* and *"no concept has been through the full chain"*, which the round then finished. **`CONCEPT_ROUND_rev77.md` §1 says its text IS this file's missing §5 and that *"placement is yours"* — IT WAS NEVER PLACED. Read §5 there, not the ranking here** |
| **`CONCEPT_AUDIT_rev77.md`** | ⚠ **NAMED IN NO EARLIER DRAFT OF THIS TABLE (rule 16). 765 KB, the adversarial verdicts across four lenses, its own §1 saying READ IT BEFORE §2.** The audit is what F338 says to rank on |
| **`CONCEPT_ROUND_rev77.md`** | ⚠ **ALSO UNNAMED UNTIL NOW. 255 KB: the synthesis, the audit-based ranking that SUPERSEDES `DESIGN_PROGRAM_rev77.md` §2, the last six amplifications, both late critics, and §5.0b's five new measurements** — among them the line pass's run-to-run instability and the AO-absence check |
| `DESIGN_PROGRAM_rev76.md` | rev 76's program. **Its §3 still prints the retracted `109.5 \| 129.5` — see F336** |
| **`HANDOFF_CARRIERS.md`** | every carrier: the goal, the reference set, the refuted emblem routes, §4 the owner's rulings, §5 rules 34–58, the horizon |
| `OPEN_FINDINGS.md` | the register. **F330–F343 are rev 77's — THE NEXT FREE ID IS F345.** It outranks prose. ⚠ **This row said "F330–F336" while the same brief leaned on F337, F338, F340 and F341; that is exactly how F341 came to be assigned TWICE (see F344). Corrected (rule 13) — COUNT THE REGISTER, do not trust this row either** |
| `STATE.md` | machine-written; outranks every prose description |
| `LEDGER_rev77.md` | what rev 77 did, **including what it got wrong, written BEFORE the closing audits** |
| `EMBLEM_HANDOFF.md`, `SPEC.md`, `REF_MEASUREMENTS.md`, `SURVEY_rev49_photoreal.md`, `ROADMAP_rev68.md`, `PANEL_rev61.md`, `REMAINING_WORK_rev61.md`, `PHOTOS_WANTED_rev49.md`, `PHOTOS_WANTED_rev52.md` | large; load the one the task needs |

**⚠ IDs LEANED ON WITHOUT NAMING, SO A GREP FINDS THEM (rule 16): `F21` `F71` `F92` `F104` `F163`
`F165` `F173` `F183` `F188` `F191` `F192` `F193` `F205` `F229` `F234` `F241` `F252` `F262` `F276`
`F281` `F284` `F289b` `F296` `F301`–`F303` `F305` `F308` `F309` `F311` `F312` `F316` `F317`
`F319`–`F323` `F325`–`F329`.**

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
   (rule 15). DO NOT CLOSE UNTIL BOTH REPORT.** ⚠ **RE-RUN THE OUTGOING ONE AFTER ANYTHING SHIPS** —
   rev 77 did, and it returned 20 more. ⚠ **SERIALISE THEIR VERIFIER RUNS AGAINST YOURS (F343).**
5. **Keep the split, and KEEP THIS FILE SHORT.** `cp` it over `PASTE_INTO_CLAUDE_CODE.txt` in the same
   commit. `python3 audit_brief.py --fix-count` LAST.
6. ⚠⚠ **THEN COLD-CLONE AND RUN `./bootstrap.sh` — LAST, ON A FRESH CLONE (F328).**
7. ⚠ **AND COMMIT ANY CONCEPT ROUND'S OUTPUT IN FULL, IN THE REPOSITORY, IN THE SAME COMMIT THAT
   ANNOUNCES IT (F335). If it is not in `git ls-files`, it does not exist.**

---
**⚠ BOTH ADVERSARIES RAN AND BOTH FOUND REAL DEFECTS. THE OUTGOING ONE FOUND TWENTY, SIX AT TOP
SEVERITY, ALL ACTED ON IN THIS FILE — including the case-blind glyph inventory (§2.1), the missing
calendar (F344), F340 miscalled a RULING, and two carriers absent from §6.** The incoming one found
twenty, one of them **in an artefact already shipped** (Sheet 3 called an AUTHORED ink MEASURED).
⚠ **`LEDGER_rev77.md` §5's own heading says "5 TOP" where its list and §6 say six — it contradicts
itself twice about its own count. Four, five and six in one document. Read the LIST, not a heading.**

**⚠⚠ THE ONE THING TO ASK HIM FOR, AND IT IS NOW LOAD-BEARING: A PHOTOGRAPH OF AN EXISTING TACOMBI
SHOPFRONT OR SIGN.** Every reference image in this tree is the VEHICLE. ⚠ *(The **"18"** three
documents carried is WRONG — `git ls-files` gives 22 reference-class entries, `HANDOFF_CARRIERS.md`
§0.1 a floor of 54; some are DERIVED grids and `bus_model_ref.JPG` is a SCHOOL BUS. The point holds,
the number was prose.)* Rev 76's critic finding 9(d) — *"an identity system is proposed against a
brand whose identity nobody has seen"* — **now bites directly: rev 78 authors letterforms that will
sit above a real door, with no sight of the signage they must live beside.** Proceed without it if you
must — the glyphs are defensible extrapolations from the bus's own hand — but **say so on the
artefact.** *(Asked for at rev 77's close; not yet supplied.)*

**WHERE THIS BRIEF IS WEAKEST, STATED RATHER THAN HIDDEN:**
* **THE ROUND IS COMPLETE, BUT ITS RANKING IS NOT WHAT THE SCREEN SAID (F338).** Screen and audit are
  ESSENTIALLY UNCORRELATED — Pearson **+0.173** over the 14 finalists — and **the concept that screened
  FIRST of 75 audits LAST of 14.** `dangerIntact` TRUE for only 4 of 14. **RANK ON THE AUDIT**, whose
  ranking lives in `CONCEPT_ROUND_rev77.md` §5, NOT in `DESIGN_PROGRAM_rev77.md` §2. ⚠ **CEILING: the
  14 were selected BY the screen, so that correlation is range-restricted and would likely be WEAKER
  over all 75; single judge per lens; n = 14.**
* ⚠ **THE ORCHESTRATION RE-RAN WORK ON EVERY RESUME — 110 audit verdicts where 56 were needed, 42
  amplify agents for 14 concepts.** The finalist list was built by iterating an object whose insertion
  order depended on which screen agent returned first, so ties resolved differently and the cache
  missed. **If you fan out and intend to resume, SORT YOUR WORK LIST ON A STABLE KEY.**
* **NOTHING FROM THE CONCEPT ROUND HAS BEEN SHOWN TO THE OWNER** — and the brief ranks seven items
  for a context that could instead spend an hour putting the top four to him. **His answer outranks
  this list; getting one is a legitimate first move.**
* ⚠ **FOUR PUBLISHED FIGURES IN THE ROUND'S OWN DOCUMENTS DO NOT SURVIVE RECOMPUTATION, AND THE
  CONCLUSIONS THEY CARRY ALL DO. `LEDGER_rev77.md` §11 has each with its arithmetic:** *"60 verdicts
  across 14 finalists at 4 lenses"* (14×4 = 56 — one concept was audited twice); F338's Spearman
  ρ = +0.222 (tie-corrected **+0.050**; Pearson +0.173 reproduces exactly); the line pass's four bare
  stroke counts (**it is not run-to-run stable**, and §4's `115 / 312` re-runs as `116 / 312`); and
  *"55 of 75 food or people"* (its own document's second critic says **21**). **RE-DERIVE ANY FIGURE
  YOU INTEND TO QUOTE.**
* **THE OCCLUSION HALF OF THE OWNER'S OWN STYLE SENTENCE IS NOT BUILT.** No normal pass, no AO pass.
* **T3's GAIN CLAIM: THE LIVE FIGURE IS 3.86 σ ON THE SEM, n = 5, ONE TREE — the CEILING is the
  weakness, not the σ.** ⚠ **THIS BULLET USED TO SAY *"1.8 σ"* — the figure §1 retracts — restating it
  as the brief's standing position in the last paragraph a reader sees. F322's class, an amendment
  reaching some sections and not others, in the brief whose §1 boasts of catching it. Caught by the
  rule-17 adversary on the FINAL handoff; corrected (rule 13).**
* **THE EMBLEM IS NOT RIGHT.** 0.8528 against P1b's 0.9465, no legibility term, nine reports.
