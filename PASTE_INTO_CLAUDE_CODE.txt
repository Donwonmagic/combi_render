# NEXT CONTEXT PROMPT — rev 79   ·   **ACTION BRIEF**

> ## ⚠⚠ **THE OWNER RE-RULED AT REV 78, LOOKING AT A PROOF, AND IT IS A METHOD RULING.**
> > **"Oh god that looks terrible. I'm worried we're too committed to the model rather
> > than the combi itself."**
>
> Put as multiple choice, he chose **DRAW IT, MODEL AS UNDERLAY. F346.** The model is
> asked only **WHERE** things are — which it knows exactly, through the material index —
> and an **AUTHORED palette** decides what each prints in. **He was right and his
> diagnosis was better than the pipeline's:** the first proof clustered the *rendered
> albedo*, which `SPEC` §3 deliberately WEATHERS, so the inks were spent on grime; and it
> drew **EVERY stroke the line pass returned**, so the drawing rendered its own kitchen
> through the serving apertures. Rebuilt: **190 of 2103 on the `flank` capture, 176 of 1719
> on `nose`.** ⚠ **NAME THE CAPTURE WHENEVER YOU QUOTE EITHER — they differ, and the pass
> is not run-to-run stable. The "2091" the first draft of this brief printed reproduces
> from no capture on this tree and is withdrawn (rule 13).**
>
> ⚠⚠ **AND THE SECOND HALF OF HIS SENTENCE IS NOT ANSWERED. F346 says so in terms.**
> Whether the PROJECT is too committed to the model is a question about the project, and
> **F18 waiting 34 revisions behind *"build it after the model is done"* is evidence for
> him.** Do NOT read F345 as closing it. **If you rank work this revision, rank that
> question too.**
>
> **F18 IS DRAWN. F345.** The register's oldest live row since rev 44, the project's
> original deliverable. `LEDGER_rev44.md` §7.3's *"no code, no asset, nothing on disk"* is
> now FALSE. **IT IS NOT CLOSED** — see §2.2.

**REV 78 SHIPPED NO VEHICLE GEOMETRY AND SAYS SO AT THE TOP OF ITS LEDGER (rule 55).**
`revstats.py` prints **`LAST FIVE REVISIONS (74-78): 138 geometry lines, 0 findings
closed`** — FIVE, which is what the script says and what the first draft of this line
miscounted as six. ⚠ **THE TRUE CONSECUTIVE RUN IS SEVEN: rev 72 through rev 78 all read
`0` closed, and rev 71 closed 2. Counted from the script's own table, not incremented by
hand.** **Rev 79 should close something.** Run the script; do not trust this line.

---
## §0 DO THIS FIRST — THE MACHINE IS IDLE WHILE YOU READ

```bash
cd /home/user/combi_render     # <- OR YOUR CLONE'S ROOT
./bootstrap.sh                 # READ ROW 9.  Row 10 is verify_clone.sh
nohup setsid env T1_SUB=1 T1_PREVIEW=front,side,hero34f,hero34r T1_PFX=r79 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r79.log 2>&1 < /dev/null &
```
**`grep -c Saved: /tmp/r79.log` must be 4**, ~5.5 min a frame. `setsid`, not a bare `nohup &`.
**`out/` DOES NOT EXIST on a clone.** **DO NOT EDIT `build.py` OR `t1_*` WHILE THE QUEUE RUNS**
(probes, `.md` and the design scripts are fine).

⚠ **DO NOT WRITE `until ! pgrep -f build.py; do …` TO WAIT FOR IT.** The loop's own command
line contains `build.py`, so `pgrep` matches the waiting shell and it never exits. Rev 78
lost ten minutes to exactly that, twice. Match on `Saved:` in the log instead.

## §0b BEFORE YOU MEASURE ANYTHING
```bash
python3 photometry.py          # 9 checked, 0 FAILED
git fetch --all --prune
for b in $(git branch -r | grep -v HEAD); do printf "%-52s ahead %-3s behind %s\n" "$b" \
  "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"; done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
```
**MEASURE THE BRANCH, DO NOT TRANSCRIBE IT, INCLUDING THIS SENTENCE.** At rev 78's pickup
row 9 PASSED and HEAD was 0/0 against `origin/main`; rev 77's branch had been MERGED, which
the incoming prose did not say. Rev 78 worked on `claude/rev-78-scope-decision-07l8d1`.

---
## §1 ⚠ WHAT REV 78 BUILT, AND THE ONE THING YOU MUST NOT MIS-CITE

```bash
python3 sticker.py --selftest                  # 6 checked, 0 FAILED, ~2 s
python3 sticker_pass.py --tag flank --lines    # ~3 min.  ⚠ A FULL CYCLES RENDER
python3 sticker.py --tag flank                 # 37 checked, 1 FAILED -- C4, BY DESIGN
```
**C4's RED IS A FINDING ABOUT THE SPEC ROW, NOT ABOUT THE DRAWING. DO NOT RE-BASE IT.**
`AUDIT_rev43.md` claims the vehicle is *"ONE 70° hue wedge plus four neutrals"*; the built
asset **MEASURES 89.6°** over all 24 chromatic materials and 89.2° over the 16 holding
≥ 0.1 % of chromatic area. **F353.** ⚠ **The `nose` capture measures 200.0° on the SAME asset. It is UNEXPLAINED. ⚠⚠ AND IT IS
NOT A "WRAP-AROUND ARTEFACT" — the first draft of this brief said so and that was a GUESS
WEARING A DIAGNOSIS'S CLOTHES (rule 13). `sticker.py`'s `_arc()` is `360 − max(gap)` over
sorted hues, which IS the wrap-safe minimal covering arc, so the nose capture's visible
material set genuinely spans 200°. Quote neither figure without naming its capture, and do
not repeat the explanation.** ⚠ **And the red/gold classification margin
is 0.18° — ON A MATERIAL HOLDING 0.1 % OF THE CHROMATIC AREA. NEVER QUOTE THE MARGIN
WITHOUT THE AREA; a thin margin on a 0.1 % material is not the finding a thin margin on a
60 % one would be. The split is REPORTED, not settled.**

⚠⚠ **`sticker_pass.py` IS NOT A PROBE. It calls `bpy.ops.render.render()` at 48 spp over
the whole scene. DO NOT RUN IT WHILE §0's QUEUE IS GOING** — CLAUDE.md forbids fanning out
Blender, and §0's parenthetical *"probes, `.md` and the design scripts are fine"* does NOT
license this one. Wait for `grep -c Saved: /tmp/r79.log` to read 4.

**WITH NO CAPTURE `sticker.py` PRINTS `0 checked, 0 FAILED, 1 ABSENT` AND TELLS YOU WHAT TO
RUN** (rule 37 — an absent input must never read as a measurement). ⚠ **BUT THAT IS NOT WHAT
A CLONE SEES, AND THE FIRST DRAFT OF THIS LINE SAID IT WAS. RETRACTED (rule 13), FOUND BY
THE §7.6 COLD CLONE.** `probe_scratch/` is **TRACKED** here — 1493 files — which is why
F329's remedy is `git checkout -- probe_scratch/` and not a delete. Rev 78's 14 capture
files (**6.1 MB**) ship with it, so **`python3 sticker.py --tag flank` reads `38 checked,
1 FAILED` on a COLD CLONE with no Blender run at all.** That is deliberate: the artefact is
reproducible from the repository. **The cost is 6.1 MB and it is stated, not hidden.**

**THE SCALE IS RECOVERED, NOT GIVEN. F347.** The surviving spec never states it.
`t1_detail.LOUV_PITCH` (0.021111 m, IMPORTED) at the spec's 0.30 mm gives **1:70.37**, and
it cross-checks: the 0.159 m minimum cut feature lands at **2.259 mm**. ⚠ **CEILING: a
78 mm lens is not orthographic, so 1:70 holds only at the vehicle's centre depth — across
the bbox the scale spreads 44.4 %, MEASURED. "1:70" is nominal.**

---
## §2 RANKED WORK FOR REV 79 — **AND THE OWNER OUTRANKS THE RANKING**

**RANK BY PIXELS OF THE DELIVERY FRAME** — `python3 visibility_budget.py 3840
out/r79_hero34f.png` — **and the owner outranks the ranking.** ⚠ **READ THAT TABLE'S OWN
CEILING: *"pixels are not visibility … catch ORDERS OF MAGNITUDE, not rank neighbours."***
⚠⚠ **AND REV 78 IS EVIDENCE THE OWNER REALLY DOES OUTRANK IT: he redirected the method
mid-revision, looking at a proof, and no pixel budget would have said so.**

### **1. ASK HIM. THREE QUESTIONS ARE OPEN AND ONE HAS BEEN SENT AND NOT ANSWERED.**
* ⚠⚠ **F348 — THE VIEWPOINT, AND REV 78 GOT THIS WRONG AND RETRACTS IT (rule 13).** The
  first draft of this brief said the disambiguating sentence *"does not survive — that row
  is hard-cut"*, and put an A/B to the owner on that basis. **THAT IS FALSE. MEASURED: the
  VIEWPOINT row's DESIGN cell is 142 characters and ENDS IN A FULL STOP** — *"…The face and
  the flank are provably exclusive; choose the flank."* What is hard-cut at 120 is a
  DIFFERENT COLUMN, the trailing symbol list, on ALL EIGHT rows; only rows 2 and 8 end
  mid-thought, at 149 and 150 characters. **So the record ANSWERS the face/flank question,
  in favour of the flank, and an owner question was spent on something already settled.**
  The genuine residual is only WHICH AXIS the 18° is measured from, and the flank reading
  (azimuth 72°) is the one consistent with the surviving sentence. `sticker_r78_nose`
  renders a reading the record EXCLUDES and is kept only as painted evidence for that.
  ⚠ **`CONCEPT_ROUND_rev77.md` §5.0b item 5 CARRIES THE SAME ERROR — it also calls the row
  hard-cut. Do not inherit it.** **NO DOCUMENT MAY QUOTE 18° ITSELF AS MEASURED.**
* **F352 — THE CAB DOOR.** `AUDIT_rev43.md` carries a row headed **`OWNER QUESTION,
  MULTIPLE CHOICE`** about the cab door, and its DESIGN cell **ends mid-quote** at
  `and "nothing but the bus" `. **It has never been put to him and is unrecoverable from
  the record.** ⚠ *(MEASURED: that cell is 149 characters, and the colour-separation row's
  is 150. The "153 characters" the first draft printed is a BYTE count for one of the two
  and is withdrawn — the two rows are not cut at the same place.)*
* **THE WHEELS.** *"I like how the wheels were drawn in the earlier cartoon version"* —
  **that version is not in this repository** and rev 76 already looked. Ask him for it.
* **STILL OWED AND STILL NOT SUPPLIED: a photograph of a real Tacombi shopfront or sign.**
  Every reference in this tree is the vehicle.

### **2. F18 IS DRAWN BUT NOT FINISHED, AND NOTHING IN THIS TREE CAN GRADE IT.**
**There is no instrument here that can tell you whether the sticker is good, and none of
the 37 checks tries.** It got better because he redirected it, not because a number moved.
Read `LEDGER_rev78.md` §6 before touching it. ⚠ **`sheet.py`'s TINT TRAP IS STILL THERE
(F350): `mix()` blends toward the STOCK, so any future artefact that draws one colour over
another through `tint` paints OPAQUE GREY. Rev 78 worked around it in `sticker.py` rather
than fixing the module.**

### **3. THE CHILDREN'S LINE NOW HAS EXACTLY ONE OBJECT IN IT.** F331 made it half the
programme. The sticker is that one object. `CONCEPT_BENCH_rev77.md`'s `THE CHILD'S EYE` slot
holds three entries — `ERA VERDE`, `MI COMBI` and `¿YA ALCANZAS?` — of which **`MI COMBI`
IS the sticker rev 78 built, so TWO are untouched, not three** (the first draft of this
line said three). **Every shortlist must say WHICH LINE each item is in.**

### **4. THE LOCATIONAL SERIES — BETHESDA. F340 / F341.** He floated it with the word
***"maybe"***; F340 grades itself *"a DIRECTION HE FLOATED, not a ruling he made"*. **He
ruled on HOW, not THAT.** ⚠ **Two corrections travel with it and both are owed to him:**
the glyph inventory is **case-sensitive** — `script_gen.py` holds ONE capital (`draw_T`)
and six lowercase, so against ALL-CAPS settings `TAQUERIA EL CRISTAL` is missing **9** and
`TAQUERIA BUENA BETHESDITA` **11**, not the 6 and 8 he was shown when he ruled; and
**F359** — the `Señor`-recovery saving is **eleven-to-ten, ONE letter**, not eight-to-five,
because segmenting `Señor` recovers the capital `S` only. ⚠ **`CRYSTAL CITY → EL CRISTAL`
IS AN INFERENCE, NOT HIS WORDS — confirm before printing it as the system's rationale.**
⚠ **And his ruling was framed under `SPEC.md` §10.10's "hard bar", which governs *"every
painted element ON THIS VEHICLE"*. A shop sign in Bethesda is not one (rule 34).**

### **5. SEVEN OWNER-GRADED ROWS WERE IN NO CARRIER AND ARE NOW CARRIED ONLY BY NAME. F356.**
`F56` `F91` `F93` `F94` `F164` `F166` `F259` — they are in §6's grep list and in F356's row,
which is a NAME-CARRY, not a carry: **none of them is summarised anywhere a context would
read.** Rule 16 asks for the substance, not the identifier. **F94** is the artwork bar
itself — *"ABSOLUTE REPLICATION OF ALL ARTWORK", "a hard bar"* — which the rev-77 brief's
whole re-framing argument turned on without naming. **F91** is his standing check
*"REMEMBER TO HOLD UP NEXT TO THE ACTUAL SOURCE PHOTOS"*, whose own row says **the tail and
the roof have still never been done.** **Carrying them properly is owed.**

### **6. F318 — the tread's one measured cost — is still open and its fix is still
prescribed and undone for four revisions.** `probe_rev70_tyre.py`'s T2 moves
**0.2457 → 0.2558**, 25× its measured 0.0004 floor. **DO NOT "fix" it by lowering
`T1_TYRE_FILM`.** Give T2 a band measured to lie inside the rubber (**PAINT IT FIRST**), or
build a better instrument.

### **7. DE-RANKED FROM REV 77's LIST, SAID OUT LOUD RATHER THAN DROPPED SILENTLY:**
**F156** (the `Senor` gate row scoring a DELIBERATE DEPARTURE, unacted — rev 77's item 7)
and **THE GARMENT SLOT** (rev 77's item 4, the cut-and-sew belt-line seam the rev-76 critic
called *"the only genuinely premium object in the whole document"*). **Neither is done and
neither is withdrawn.** F156 is live in `OPEN_FINDINGS.md` and carried in
`HANDOFF_CARRIERS.md`; the garment slot is in `CONCEPT_BENCH_rev77.md`. They rank below the
sticker and the questions this revision, and that is a RANKING, not a judgement.

### **8. THE EMBLEM.** His ninth report. **0.8528 against P1b's 0.9465 and the objective
still has no legibility term.** **F191 STANDS — he did not withdraw it and was not asked
to**, which the rule-15 adversary confirmed against the register.

---
## §3 WHAT REV 78 SETTLED — **DO NOT RE-OPEN**

| closed | the result |
|---|---|
| **F345 / F346** | **The sticker exists, and the owner re-ruled the method while it was being built.** |
| **F347** | The scale, recovered by inversion and cross-checked. Two independently obtained quantities (rule 6). |
| **F349 / F350 / F351** | **Three of rev 78's own instruments, wrong and retracted in the same revision (rule 13).** The spec's cut-line rule applied to artwork; `sheet.py`'s tint painting opaque grey; the ink separation read off unconnected node defaults. |
| **F352 / F353 / F359** | three of the rule-15 adversary's findings, MEASURED and settled. ⚠ **IT RETURNED FOURTEEN. Eight have rows (F352–F359) and SIX ARE UNLOCATED — not in the register, not in the ledger. The ledger's "all carried" is withdrawn. Rule 16, on the revision that made rule 16 a headline.** |

⚠⚠ **AND WHAT §3 DOES *NOT* COVER, BECAUSE THE FIRST DRAFT OF THIS TABLE PUT IT HERE AND IT
DOES NOT BELONG (caught by the rule-17 adversary): `F348` `F354` `F355` `F356` `F357` `F358`
ARE ALL GRADED `OPEN-rev78`. THEY ARE LIVE WORK, NOT SETTLED RESULTS.** A context obeying
this section's heading would have skipped six live rows. **`F350` is graded MEASURED but its
own row says `sheet.py` IS UNCHANGED AND THE TRAP IS STILL THERE** — settled as a diagnosis,
open as a repair. **READ THE GRADE IN `OPEN_FINDINGS.md`, NOT THIS TABLE.**

## §3b ⚠ REV 72–78's FIXES ARE LOCKED. **A red row is a FINDING ABOUT YOUR CHANGE.**
A re-base needs the cause NAMED and a companion row making that cause separately testable.
**RUN `./bootstrap.sh --guards` ONCE THIS REVISION** — ~20 min, and not while a queue runs.

---
## §4 THE MACHINE — **and F357 is new and bites the closing sequence**

⚠⚠ **`verify_clone.sh` IS NOT SAFE TO RUN TWICE AT ONCE (F343), AND THERE ARE FOUR RUNNERS,
NOT THREE: yours, an adversary's, §7's cold clone, and — NEW, F357 — `audit_brief.py`,
which shells it internally.** The rev-78 adversary hit it live. **SERIALISE THEM.**
F343's own figure is wrong too: there are **21** fixed `/tmp` paths, not 20.

```bash
./verify_clone.sh                             # ALL 449 PASS on rev 78's tree --
  # 0 FIDELITY, 449 SELF-CONSISTENCY.  ⚠ THAT COUNT IS WHAT `audit_brief.py`
  # PARSES OUT OF THIS FILE, and `--fix-count` can only REWRITE it, never create
  # it: delete the line and check 5 reds permanently.  With an EMPTY out/ six
  # rows SKIP and say UNGUARDED; the PASS total is the same either way (F323).
  # READ THE VERDICT BLOCK: not one row measures the vehicle against a photograph
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
python3 sticker.py --selftest                 # NEW.  6 checked, 0 FAILED
python3 sticker_pass.py --tag flank --lines   # NEW.  ~3 min
python3 sticker.py --tag flank                # NEW.  37 checked, 1 FAILED -- C4 BY DESIGN
python3 probe_rev73_tailboard.py out/r79_side.png   # 5 checked, 1 FAILED -- T4 only
python3 probe_rev77_t3floor.py                # ⚠ ITS "0 FAILED" IS A STRING LITERAL (F354)
python3 probe_rev74_tread.py out/r79_side.png # 8 checked, 0 FAILED
T1_TYRE_TREAD=0 python3 probe_rev74_tread.py  # THE KILL.  REDS **TWO** ROWS: T3 and T7
python3 probe_rev46_vw.py                     # 12 checked, 2 FAILED -- C4 AND C10
python3 probe_rev69_fitpose.py                # 5 checked, 1 FAILED -- P4 only.  ⚠ P1's
  # MESSAGE hardcodes 0.9703 while P1b PRINTS 0.9465; read the NUMBERS, not the prose
python3 probe_rev71_proxy.py                  # must read IoU 1.000000
python3 visibility_budget.py 3840 out/r79_hero34f.png ; python3 revstats.py
T1_SUB=2 /tmp/blender/blender -b -P audit.py  # rewrites STATE.md -- COMMIT FIRST, and
  # AFTER your LAST source edit.  ⚠ THEN regenerate the design artefacts, which read it
  # ⚠⚠ F344: design_out/calendario_ano_xxii.svg STILL PRINTS "2711 trazos / 19471 puntos"
  #   -- ONE DRAW of a count the line pass does not reproduce, published as a constant.
  #   DO NOT SHOW THE CALENDAR TO HIM WITH THAT LINE ON IT WITHOUT SAYING SO.  The
  #   rev-77 brief carried this warning in its head; rev 78's first draft DROPPED it,
  #   which is rule 16, and the rule-17 adversary caught it.
python3 audit_brief.py ; python3 audit_adversary.py   # ⚠ THE FIRST ONE RUNS THE VERIFIER
```
⚠⚠ **17+ PROBES REPAINT TRACKED FILES (F329). THE RULE, NOT THE LIST:**
`git status --porcelain ; git checkout -- probe_scratch/` — ⚠ **and F358: `la_rueda.py`
and `calendario.py` write into TRACKED `design_out/`, which that remedy does NOT reach.**

**THE ABLATIONS.** `verify_clone.sh` runs `T1_REAR_*`, `T1_NOSE_NOWIN`, `T1_VW_FREE`,
`T1_TYRE_TREAD`. ⚠ **IT DOES NOT RUN THE LINE-PASS ONES AND THE REV-77 BRIEF READ AS
THOUGH IT DID (F355): `T1_LINE_NOCONTOUR` / `T1_LINE_NOCREASE` appear in `line_pass.py`
ONLY. Rev 78's `T1_STK_NOOPEN` / `T1_STK_NOBRIDGE` / `T1_STK_NOHOLES` are in the same
position — watched by hand, not by the verifier.** "ALL PASS" does not cover any of them.

**FACTS THAT BITE:** the render is **not** run-to-run deterministic (~2.04 % of pixels
>8 levels at 1600×1100/96 spp), and **the line pass is not either** — two captures of one
unchanged tree differed by one stroke during rev 78. ⚠ *(An ANECDOTE, not a figure: only
the surviving capture is on disk, so the pair is not re-derivable. `CONCEPT_ROUND_rev77.md`
§5.0b measured the instability properly — cite that, not this.)* `lid_gen.py` / `script_gen.py` are **not** called by `build.py`.
`audit.py` rewrites `STATE.md` — **commit first**. **A backgrounded runner's `rc=$?` is the
redirect's.** ⚠ **Blender 4.x's default view transform is AgX, and a File Output node
APPLIES IT — every data pass must force `view_transform = "Raw"` or it is a picture, not
data. It rendered the bus ORANGE at rev 78 while all 32 checks passed.**

---
## §5 THE RULES THAT WILL BITE YOU

⚠⚠ **TWO INCOMPATIBLE CANONS FOR 1–33.** **`CLAUDE.md`'s numbered list (1–18) IS IN
FORCE.** `NEXT_CONTEXT_PROMPT_rev50.md` §11 carries a DIFFERENT 1–33 whose numbers
COLLIDE. **Rules 34–58 are in `HANDOFF_CARRIERS.md` §5 — whose first line says 34–52, and
which holds TWO rule 56s and TWO rule 57s. Say which you mean.**

**55 — EVERY REVISION SHIPS A VISIBLE CHANGE TO THE VEHICLE, OR SAYS PLAINLY WHY IT COULD
NOT**, at the TOP of its ledger. **REV 78 COULD NOT AND SAYS SO: the vehicle did not move,
and what shipped is the project's ORIGINAL DELIVERABLE as a thing he can look at.** ⚠ **REV
77 ALREADY FLAGGED THAT THIS RULE'S LETTER AND ITS PURPOSE COME APART FOR THE DESIGN
PROGRAMME, and rev 78 is the second revision running to hit it. A future context should
decide whether rule 55 needs a second clause — do NOT assume either ledger settled it.**

**Which bit rev 78, and it is one rule above all: 1 and 2.** Every one of six wrong
instruments printed a plausible number, and **not one was found by reasoning** — five by
looking at a picture, one by a fabricated-mask selftest. **The worst of them survived 34
passing checks and two correctly-firing ablation kills, and was caught by the OWNER
looking at the proof.** Also **8** (five times), **13** (three retractions), **3**, **4**,
**37**, **12**, **55**.

---
## §6 WHERE EVERYTHING ELSE LIVES

| file | what it holds |
|---|---|
| `LEDGER_rev78.md` | what rev 78 did, **including its six wrong instruments and how each was caught** |
| `OPEN_FINDINGS.md` | the register. **F345–F359 are rev 78's; DERIVE the next free ID, do not read it here:** `grep -oE '\*\*F[0-9]+\*\*' OPEN_FINDINGS.md \| sort -uV \| tail -1` |
| **`HANDOFF_CARRIERS.md`** | **NOT auto-imported. `cat` it when pointed at.** Every carrier: the goal, the reference set, the refuted emblem routes, §4 the owner's rulings, §5 rules 34–58 |
| **`CONCEPT_BENCH_rev77.md`** | **THE CARRIER. All 75 concepts in full. 510 KB. Do not compact it** |
| **`CONCEPT_ROUND_rev77.md`** | 255 KB: the synthesis, the audit-based ranking that **SUPERSEDES `DESIGN_PROGRAM_rev77.md` §2**, and §5.0b's measurements — including the one that already said no camera matches the sticker's 18° |
| **`CONCEPT_AUDIT_rev77.md`** | 765 KB, the adversarial verdicts across four lenses |
| `AUDIT_rev43.md` | **the sticker spec — in `## 2. SURVIVING FINDINGS`, NOT §5, which F18's own row gets wrong (F352)** |
| `STATE.md` | machine-written; outranks every prose description |
| `SPEC.md`, `REF_MEASUREMENTS.md`, `SURVEY_rev49_photoreal.md`, `ROADMAP_rev68.md`, `REMAINING_WORK_rev61.md`, `EMBLEM_HANDOFF.md`, `PHOTOS_WANTED_*` | large; load the one the task needs |

**⚠ IDs LEANED ON WITHOUT NAMING, SO A GREP FINDS THEM (rule 16): `F21` `F56` `F71` `F91`
`F92` `F93` `F94` `F104` `F161` `F163` `F164` `F165` `F166` `F173` `F183` `F188` `F191`
`F192` `F193` `F205` `F214` `F215` `F229` `F234` `F241` `F252` `F259` `F262` `F276` `F281`
`F284` `F289b` `F296` `F301`–`F305` `F308` `F309` `F311` `F312` `F314` `F316` `F317`
`F319`–`F344`.**

---
## §7 HOW TO CLOSE

**HIS STANDARD:** photo-real parity with **that exact bus**, in service of a promotional
render. **Any single measurement off is unacceptable** — per-measurement, not on average.
**Never call it done off self-review. Report the measurement with its ceiling. Do not say
anything is ready.**

1. `./bootstrap.sh` and `./verify_clone.sh` on a **clean** tree. **The honest closing
   condition: every red is one you can name, and none of them is yours.**
2. `python3 revstats.py` — **put its geometry/closure line in the ledger header; if the
   revision shipped no geometry, say so at the TOP** (rule 55).
3. Regenerate `STATE.md` (`T1_SUB=2 … audit.py`) — **commit first, AFTER your last source
   edit. Then REGENERATE THE DESIGN ARTEFACTS, which read it.** Then `audit_adversary.py`.
4. **DISPATCH an adversary at the brief you WROTE (rule 17) and one at the brief you
   RECEIVED (rule 15). DO NOT CLOSE UNTIL BOTH REPORT.** ⚠ **SERIALISE THEIR VERIFIER RUNS
   AGAINST YOURS — and remember `audit_brief.py` is one of them (F357).**
5. **Keep the split, and KEEP THIS FILE SHORT.** `cp` it over `PASTE_INTO_CLAUDE_CODE.txt`
   in the same commit. `python3 audit_brief.py --fix-count` LAST.
6. ⚠⚠ **THEN COLD-CLONE AND RUN `./bootstrap.sh` — LAST, ON A FRESH CLONE (F328).**
7. ⚠ **COMMIT ANY ROUND'S OUTPUT IN FULL, IN THE SAME COMMIT THAT ANNOUNCES IT (F335).
   If it is not in `git ls-files`, it does not exist.**

---
**⚠ THIS BRIEF WAS AUDITED AGAINST THE MACHINE, TWICE, AND BOTH PASSES FOUND REAL DEFECTS.**
The incoming one (rule 15) returned **14**, including a hidden fourth `verify_clone.sh`
runner and seven owner-graded rows in no carrier. The outgoing one (rule 17) returned
**29** against THIS file — nine of them changing what rev 79 should do, among them a
register row that was not a row, a viewpoint claim that was false in four places including
the shipped artefact, and a guard that could never fire. **All nine are fixed and §8 records
them.** ⚠ **AND THE §7.6 COLD CLONE THEN FOUND A THIRD CLASS THE ADVERSARIES COULD NOT:
shortening this brief DROPPED THREE PHRASES THAT `verify_clone.sh` ROWS BIND VERBATIM** —
the ranking sentence that opens §2, rule 55's own wording in §5, and the first line of this
paragraph — **so the verifier read 446 rather than 449 on a fresh clone. Rule 16 in
miniature: a document was compacted and took guarded content with it.**
⚠⚠ **AND TWO OF THOSE THREE ROWS WANT THE PHRASE ON *EXACTLY ONE LINE* (`grep -c … 1`), so
you cannot quote them a second time to explain them — which is why this paragraph names
them by location instead. IF YOU SHORTEN OR RESTRUCTURE THIS FILE, RE-RUN THE VERIFIER
AFTERWARDS, NOT BEFORE, AND ON A COLD CLONE (F328): the main tree's run predated this file
existing and could not have caught it.**

**WHERE THIS BRIEF IS WEAKEST, STATED RATHER THAN HIDDEN:**
* **THE OWNER CALLED THE FIRST PROOF TERRIBLE AND THE SECOND IS BETTER ONLY BY HIS OWN
  REDIRECT.** No measurement says it improved. **Nothing in this tree can grade it.**
* **HIS BIGGER WORRY IS UNANSWERED (F346)** and this brief cannot answer it: *"too
  committed to the model rather than the combi itself."*
* **SEVEN CONSECUTIVE REVISIONS WITH ZERO CLOSURES (72–78), counted off `revstats.py`'s own
  table.** Rev 78 opened fifteen rows and closed none.
* **REV 78's OWN AUTHORED CONSTANTS WERE TUNED BY LOOKING** — `DESPECKLE_MM`,
  `ALBEDO_BLUR_MM`, `SHADE_BLUR_MM`, `SHADE_MULT`, `AO_MULT`, `LINE_MIN_MM`, `BLEED_MM`.
  Reported every run and labelled on the artefact, but a different context would tune them
  differently and get a different sticker.
* **THE `nose` CAPTURE'S 200.0° HUE WEDGE IS UNEXPLAINED (F353).**
* **THE EMBLEM IS NOT RIGHT.** 0.8528 against 0.9465, no legibility term, nine reports.

---
## §8 ⚠ WHAT THE RULE-17 ADVERSARY FOUND IN **THIS** FILE — RECORDED, AS RULE 17 REQUIRES

Dispatched at this brief, `LEDGER_rev78.md` and F345–F359, read-only. It returned
**29 findings. NINE change what rev 79 should do, and all nine are fixed above** — because
it found them, not before it did:

1. ⚠⚠ **`F345` WAS NOT A ROW.** It had been appended to F344's line with no newline — one
   3465-character line carrying two findings — so the register's own table could not render
   the project's oldest live row. **On the revision that made F344 (*a finding with no
   register row*) a headline.** Fixed; every rev-78 row now starts its own line.
2. ⚠⚠ **THE VIEWPOINT ROW IS NOT TRUNCATED** — see §2.1. The claim was wrong in this brief,
   in `OPEN_FINDINGS.md` F348, in `sticker_pass.py`'s module docstring **and on the shipped
   artefact's own colophon**. All four corrected.
3. **§3 listed six `OPEN-rev78` rows under a heading reading DO NOT RE-OPEN.**
4. **`audit_brief.py` check 5 would have redded permanently** — this file carried no
   `ALL N PASS` string, and `--fix-count` can only rewrite one, never create it.
5. **`README.md` and `START_HERE.md` still said rev 77**, which check 6 asserts against.
6. **`sticker.py`'s S1 was a TAUTOLOGY** — it asserted the identity that DEFINES the scale,
   residual exactly 0.0, so it could never red. Replaced with a comparison against
   `STATE.md`'s own overall length (**65.1 mm at 1:70.37**) and **watched failing at 10×
   and ¹⁄₁₀× the scale**.
7. **F344's calendar warning had been dropped from this brief** — rule 16. Restored in §4.
8. **§1 licensed a second Blender render on top of §0's queue.**
9. **"labelled AUTHORED on the artefact" was false for the seven tuning constants** — they
   were reported at run time only. They are now printed on the sheet itself.

**Eight published figures did not recompute** and are corrected or withdrawn above: the
closure run (five per the script, seven in truth, not six); *"2091"* strokes; *"2104"*;
*"153 characters"*; *"three untouched concepts"*; *"14 findings all carried"*; the
*"wrap-around artefact"* explanation; and the 0.18° margin quoted without the 0.1 % area
that sizes it.

**WHAT IT CONFIRMED, WHICH MATTERS AS MUCH:** `6 checked, 0 FAILED` and `37 checked,
1 FAILED — C4 only` on **both** captures; the selftest is **not** a tautology and its T6
closes the loop; `1:70.37`, `2.259 mm`, `28.1 mm`, `44.4 %`, `12 864 px`, `22 of 45` linked
sockets, `view_transform = "Raw"` set before the render, `21` fixed `/tmp` paths, F354's
string literal, F357's `subprocess.run`; **every owner quote traces to its source**,
including the 34-revision gap on F18; all four `AUDIT_rev43.md` quotes verbatim; the spec
rows really are in `## 2. SURVIVING FINDINGS` and not §5; **F191 stands**; the glyph figures
are right to the letter and F359's ten-not-five recomputes exactly; and **nothing in this
brief, the ledger or the rev-78 rows claims a fidelity result.**

⚠ **ITS CEILING: it did not run `verify_clone.sh`, `audit_brief.py`, Blender,
`sticker_pass.py` or `la_rueda.py`.** The 449 total, `--fix-count`'s behaviour (predicted
from reading the code, not watched), the `T1_STK_*` ablations against a REAL capture, and
the third leg of the byte-identity claim are **unverified by it**. ⚠ **`la_rueda.py` needs
`probe_scratch/rueda.json`, which is untracked — so on a clone that third leg CANNOT be
checked at all, and NO VERIFIER ROW BINDS ANY OF IT (F350's companion is still owed).**
