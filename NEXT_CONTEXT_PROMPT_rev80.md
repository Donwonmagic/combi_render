# NEXT CONTEXT PROMPT — rev 81   ·   **ACTION BRIEF**

> ## ⚠⚠ **THE MODEL IS FROZEN (F361) AND THE OWNER SPENT REV 80 PUSHING THE DRAWING LINE. HE OUTRANKS ANY RANKING IN THIS FILE.**
> Three instructions, verbatim, in order:
> *"I simply want a collection of promotional images utilizing the combi. Very
> similar to this sign, but I want to make it special, distinguished in a way."*
> → *"It's not about the palette, it's just an example of a promotional
> product."* → *"Remember that the model is simply an underlay for the hero of
> each piece. **It should be done in different styles too.**"*
> Asked which of six styles and which of four categories: **"All."**
>
> ⚠⚠ **HE REJECTED A WHOLE ROUND FIRST — "None of them yet" — WITH EVERY CHECK
> GREEN ON ALL SEVEN PIECES.** That is the **THIRD consecutive revision** in
> which he has caught an artefact no instrument here could (rev 78 *"Oh god that
> looks terrible"*; rev 79 *"that's not a product"*, F366). He named the cause
> himself: `promo.py` had **pasted the render in as the artwork** instead of
> drawing from it. **NOTHING IN THIS TREE CAN GRADE A DRAWING. HE IS THE
> INSTRUMENT.**
>
> **AND HE SUPPLIED A PHOTOGRAPH** — `ref_sign_aframe.jpg`, a real Tacombi
> A-frame sidewalk sign. **The first photograph of a real Tacombi SIGN this
> repository has ever held.** It closes a request open since rev 52.

**REV 80 CLOSED THREE: F369, F371, F372, and AMENDED F368.** ⚠ **RUN
`python3 revstats.py` AND READ ITS OWN NUMBER — but see F375 first: that
instrument CANNOT SEE THIS REVISION'S WORK AT ALL.**

---
## §0 DO THIS FIRST — THE MACHINE IS IDLE WHILE YOU READ

```bash
cd /home/user/combi_render     # <- OR YOUR CLONE'S ROOT
./bootstrap.sh                 # READ ROW 9.  Row 10 is verify_clone.sh
nohup setsid env T1_SUB=1 T1_PREVIEW=front,side,hero34f,hero34r T1_PFX=r81 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r81.log 2>&1 < /dev/null &
```
**`grep -c Saved: /tmp/r81.log` must be 4**, ~5.5 min a frame. `setsid`, not a bare `nohup &`.
**`out/` DOES NOT EXIST on a clone.** **DO NOT EDIT `build.py` OR `t1_*` WHILE THE QUEUE RUNS**
(probes, `.md` and the design scripts are fine).

⚠ **REV 79's SILENT DEATH AT 3 FRAMES OF 4 DID NOT REPRODUCE AT REV 80** — all
four landed. **ONE CLEAN RUN IS NOT A DIAGNOSIS.** The cause was never found.
**CHECK THE COUNT, DO NOT ASSUME IT.**

⚠ **DO NOT WRITE `until ! pgrep -f build.py; do …`** — the loop's own command
line contains `build.py`, so `pgrep` matches the waiting shell. Match `Saved:`
or use `buil[d].py`.

⚠⚠ **DO NOT RUN `verify_clone.sh` THROUGH A WRAPPER THAT MAY REAP IT.** At rev
80 a wrapped run died at **408 rows with no verdict block** and looked clean.
Run it detached and **check the verdict block is there**, not just the count.

## §0b BEFORE YOU MEASURE ANYTHING
```bash
python3 photometry.py          # 9 checked, 0 FAILED
git fetch --all --prune
for b in $(git branch -r | grep -v HEAD); do printf "%-52s ahead %-3s behind %s\n" "$b" \
  "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"; done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
```
**MEASURE THE BRANCH, DO NOT TRANSCRIBE IT, INCLUDING THIS SENTENCE.** Rev 80
worked on `claude/combi-promotional-images-b9c2mt`.

---
## §1 WHAT REV 80 BUILT

```bash
python3 estilos.py             # 16 checked, 0 FAILED, ~60 s
T1_EST_NOKEY=1 python3 estilos.py --out /tmp/ab      # THE KILL: 4 recovery rows RED
python3 coleccion.py           # 28 checked, 0 FAILED, ~55 s
T1_COL_BADGE=1 python3 coleccion.py --only mercancia_chapa --out /tmp/ab  # rim guard REDS
python3 promo.py               # 20 checked, 0 FAILED   (17 on a clone -- see below)
T1_PROMO_COLLIDE=1 python3 promo.py --only 07_hero --out /tmp/ab          # 2 collisions RED
```
All three run on a **COLD CLONE with no Blender** (verified) — they draw from
the tracked captures — **except `promo.py`'s `07_hero`**, which needs a rendered
`*hero34f*` frame. `out/` is gitignored, so on a clone that piece SKIPs and the
count is **17, not 20**, while the artefact itself is committed.

**`estilos.py` — THE COMBI DRAWN IN SIX STYLES**, over the model as underlay
(F361: asked only WHERE things are). `plano` flat vector · `linea` engraving ·
`papel` papel picado, one ink, artwork PUNCHED OUT · `riso` duotone,
misregistered · `azulejo` blueprint · `sello` stencil. A check compares all six
pairwise — closest pair `papel`/`sello` at **15.37**, floor 6.0.

**`coleccion.py` — 15 PIECES, HIS FOUR CATEGORIES.** `calle` aframe, carta,
vidriera, horario · `social` cuadro, historia, cabecera · `impreso` cartel,
postal, lealtad, volante · `mercancia` playera, bolsa, vaso, chapa.

---
## §2 RANKED WORK FOR REV 81 — **AND THE OWNER OUTRANKS THE RANKING**

**RANK BY PIXELS OF THE DELIVERY FRAME** — `python3 visibility_budget.py 3840
out/r81_hero34f.png` — **and the owner outranks the ranking.** ⚠ **READ THAT
TABLE'S OWN CEILING: pixels are not visibility; it catches ORDERS OF MAGNITUDE,
not rank neighbours.** ⚠⚠ **AND UNDER F361 IT RANKS A FROZEN OBJECT. A pixel
budget over the vehicle cannot rank DRAWN WORK at all, which is the main line.**
Top by area, reproduced at rev 80: **F67** contact shadow `3.83e+06 px²`;
**F44** gloss `2.08e+06` and `8.08e+05`; **F15** `6.92e+05`. **The emblem's four rows are ranks
9, 11, 14 and 16** at `3.32e+04`, `1.28e+04`, `9.79e+01`, `1.15e+00` — ⚠ **NOT
9/11/15/16: rank 15 is `F38`, the nose ring band, a different finding.**
**Largest / smallest = 3 335 815×**, and the table's verdict says the item at the
bottom was the top job for four revisions. ⚠ **NOT an argument to drop the
emblem: F191 stands.**

### **1. ASK HIM. FIVE QUESTIONS ARE OWED AND FOUR ARE STALE.**
* **THE FIFTEEN PIECES.** He asked for all styles and all categories and has
  them. **He has not seen them since the F371/F372 repairs.** One question.
* **THE LAMP A/B (F362).** Drawn at rev 79, **still unanswered**.
* **THE SCALE (F362).** 234.06 mm as drawn, or 1:23.79 for 200 mm. ⚠ F347's
  44.4 % scale ceiling applies to both.
* **THE CAB DOOR (F352).** `AUDIT_rev43.md`'s `OWNER QUESTION, MULTIPLE CHOICE`
  row, DESIGN cell **149 chars**, ends mid-quote. Never put to him.
* **THE WHEELS.** *"the earlier cartoon version"* is **not in this
  repository**; rev 76 looked.
* **STILL OWED: a photograph of a real Tacombi SHOPFRONT.** ⚠ **THE SIGN HALF OF
  THIS REQUEST IS NOW ANSWERED** — `ref_sign_aframe.jpg`. See `PHOTOS_WANTED_rev52.md`.

### **1b. ⚠⚠ THE FIFTEEN PIECES REPRODUCE THE MODEL'S TWO WORST OPEN ARTWORK
DEFECTS, AT POSTER SIZE (F379).** `visibility_budget.py`: **`F01/F39 — Señor,
28.5 % of its ink missing`, rank 10, `2.26e+04 px²`**, and **`F63/F69 — the VW
glyph builds as an X`, ranks 9 and 11, GATED AND FAILING (C6), his report NINE
times over.** **The `wordmark` recovered by F370 and printed on ALL FIFTEEN
PIECES IS that `Señor` artwork**, and `plano`, `riso` and `azulejo` all draw the
hubcaps. **F361 froze the model; it did not make the frozen model's defects
invisible — it multiplied them by fifteen.** ⚠ **SAY THIS WHEN THE SHEET GOES TO
HIM.** Fixing it means unfreezing the model, which is his ruling to make.

### **1c. ⚠ HIS PHOTOGRAPH IS AN OFFER SIGN AND NOTHING IN THE COLLECTION
ANSWERS THAT.** `ref_sign_aframe.jpg` reads `DOWNLOAD OUR APP & GET $5 OFF
TODAY`, `PLUS $5 ON YOUR NEXT VISIT!`, and carries a **QR code**. He said *"very
similar to this sign"*. **Not one of the fifteen pieces has a QR code, an app
callout, or any call to action.** The category was read as *poster with wordmark
and hero*; his sign's actual category is *sidewalk offer*. **That is an owner
question, not a defect to fix blind.**

### **2. THE COPY ON EVERY PIECE IS PROVENANCED — KEEP IT THAT WAY (F372).**
`MEDIDO` off the mural lid · `LETRERO` off his own photograph · `AUTORADO` mine.
⚠ **`LETRERO` IS `TAQUERIA y CERVECERIA` — NO ACCENTS, LOWERCASE `y`, EXACTLY AS
THE SIGN SPELLS IT (F376).** The first version added two acutes and upper-cased
the conjunction while every piece printed a colophon claiming the string came
off his sign. **F94 — *absolute replication* — outranks Spanish orthography when
the claim being made is provenance.**
**No piece states a price, an opening time or a date at all** — every drawn
literal was scanned for digits and there are none — and the hours card ships
BLANK RULES on purpose. ⚠ **`impreso/lealtad` DOES state an offer in words**
(`OCHO VISITAS · LA NOVENA ES NUESTRA`); what saves it is
`OFERTA DE MUESTRA · NO APROBADA` set directly beneath it. **Say that, rather
than denying the class.** **`CONCEPT_BENCH_rev77.md` warns *"WE
MAY BE SELLING FOOD HE NO LONGER SERVES … only he can"*.**

### **3. THE CHILDREN'S LINE HAS TWO OBJECTS.** `MI COMBI` and `APAGA LA LUZ`.
`CONCEPT_BENCH_rev77.md`'s `THE CHILD'S EYE` slot holds a third, `¿YA ALCANZAS?`,
untouched. **Every shortlist must say WHICH LINE each item is in (F331).**

### **4. THE CONCEPT ROUND IS STILL ON THE SHELF.** Rank on the AUDIT
(`CONCEPT_ROUND_rev77.md` §5), **not** the screen — Pearson **+0.173**. Blocked
on nothing: `DIRECTO` (2.25, ~2 h), `MANDIL 515` (1.88), `A LA ALTURA · 118`
(1.75). **Drawing one beats describing all of them** — revs 78–80 all confirm.

### **5. `apaga.py` HAS THREE NAMED DEFECTS AND THE OLD ONE IS RETRACTED.**
⚠⚠ **DO NOT CHASE THE 1075 px. IT IS RETRACTED (F364) AND A8 NOW READS 0 px BY
CONSTRUCTION.** What IS live: **(a)** the opening is still built as a
**bounding-box slice** per seal component (`open_reg[sl] = True`), which is the
bbox criticism F364 made; **(b) `probe_scratch/apaga_resid.png` IS ENTIRELY
BLACK** — it paints the RESIDUAL and **never paints `open_reg`, the window whose
correctness is the whole subject of F364**, so it cannot distinguish "nothing
leaks" from "the window selects nothing"; **(c) it writes that mask to `ROOT`
REGARDLESS OF `--out`**, so the ablation overwrites the tracked evidence of the
normal path. **`--out` is NOT sufficient (F358 is incomplete).**

### **6. F318 — the tread's one measured cost — OPEN FOR A SIXTH REVISION.**
`probe_rev70_tyre.py`'s T2 moves **0.2457 → 0.2558**, 25× its 0.0004 floor.
**DO NOT "fix" it by lowering `T1_TYRE_FILM`.** F361 DE-RANKED THIS; IT DID NOT
ANSWER IT.

### **7. SEVEN OWNER-GRADED ROWS CARRIED ONLY BY NAME. F356.** `F56` `F91` `F93`
`F94` `F164` `F166` `F259`. **F94** is the artwork bar — *"ABSOLUTE REPLICATION
OF ALL ARTWORK"*. **F91** is *"REMEMBER TO HOLD UP NEXT TO THE ACTUAL SOURCE
PHOTOS"*, whose row says the tail and roof have **still never been done**.
⚠ **F164 IS GRADED `RULED-rev62`, NOT CLOSED** — rev 79's brief said it was
closed; the register disagrees and the register wins. Substance is in
`HANDOFF_CARRIERS.md` §0.12.

### **8. THE LOCATIONAL SERIES — BETHESDA. F340 / F341, `RULED-rev77`.** He
floated it with *"maybe"*; **he ruled on HOW, not THAT.** Detail, the two
corrections owed him, and the `SPEC.md` §10.10 scope problem are in
**`HANDOFF_CARRIERS.md` §0.13.** Read it before acting.

### **9. THE EMBLEM. F191 STANDS.** 0.8528 against P1b's 0.9465, still no
legibility term. His ninth report.

### **10. STILL OPEN, CARRIED HERE SO IT IS NOT DROPPED:**
* **F18 IS DRAWN BUT NOT CLOSED** — the register's oldest live row.
* **SIX OF THE REV-78 ADVERSARY'S FOURTEEN FINDINGS ARE UNLOCATED.**
* **F347's 44.4 % SCALE CEILING travels with every scale figure.**
* **`la_rueda.py` needs `probe_scratch/rueda.json`, UNTRACKED AND ABSENT** — it
  correctly REFUSES (0 checked, 1 ABSENT), and **no verifier row binds that leg.**
* **F344: `calendario_ano_xxii.svg` STILL PRINTS `2711 trazos / 19471 puntos`**,
  one draw of a count the line pass does not reproduce (2711–2716 / 19468–19475
  at n=5). **DO NOT SHOW THE CALENDAR TO HIM WITH THAT LINE ON IT.**
* **F156** (the `Señor` gate row scoring a DELIBERATE DEPARTURE) and **THE
  GARMENT SLOT**: de-ranked, neither done nor withdrawn.
* **F365 — NEVER PRINT A BARE LAMP COUNT.** The `bulb` MATERIAL is on
  `bulb_string()` **AND** `tail_board_bulbs()`, so the owner's A/B moves the
  flank's **118** PLUS **~26** on the tail board, and the drawn mask traces
  **122** regions — a third number. ⚠ **§2.1 sends you to put that A/B to him,
  which is exactly where a bare count gets printed.**
* **F323 — WITH AN EMPTY `out/`, SIX VERIFIER ROWS SKIP AND SAY `UNGUARDED`;
  THE PASS TOTAL IS THE SAME.** A cold-clone reader sees six SKIPs and must not
  read them as failures.
* **F345 / `LEDGER_rev44.md`** — that ledger's §7.3 *"no code, no asset, nothing
  on disk"* is the sentence F345 FALSIFIED, and it is why **F18 is drawn but not
  closed**. Without both, F18's status is unrecoverable from this brief.
* **F363** — `revstats.py` counted closure STRINGS, not findings, and **rev 71
  closed 1, not 2.** ⚠ Its successor defect is F375, and rev 70 still reads 3
  because F363's OWN row is attributed to it.
* **`LEDGER_rev78.md`** — where the **six unlocated rev-78 adversary findings**
  would be found if they are anywhere.
* **`flank_compare.py` and `cream_rms.py` are the paint instruments** if a flank
  question returns. **F44 is items 2 and 3 in the pixel ranking above.**
* **`gal_tube` IS ZERO PIXELS ON BOTH CAPTURES** (0 of 566 208 at az 72, 0 of
  561 033 at az 90) — the emitter cannot be seen; **what is drawn is the room it
  lights**, and that is a DECLARED DEPARTURE.
* ⚠ **THE CONCEPT'S *"FIRST STEP: ~$0, one A4 sheet and an evening"* IS THE
  VINYL TEST AND DOES NOT COVER THE DRAWING. Never quote the one as the cost of
  the other.**

---
## §3 WHAT REV 80 SETTLED — **READ THE GRADE IN `OPEN_FINDINGS.md`, NOT THIS TABLE**

| closed | the result |
|---|---|
| **F369** | F368's *"the artwork is not recoverable"* is **FALSE**. Key **by colour WITHIN each material region**: `T1_paint` splits **33.1 / 59.4 / 7.5 %**, `lidmural` **27.3 %** flower. F368's row is **AMENDED in place**. |
| **F371** | **The type ceiling rev 80 published was false in both halves and was quoted as "measured".** PIL 12.3.0 DOES load Charter's Type1 (`('Bitstream Charter','Bold')`, 7702 ink px); the CDN probe hit **the wrong host** — `fonts.googleapis.com` returns **200**. Rule 10 inside a rule-12 ceiling. |
| **F372** | **A docstring claimed the menu was read off the vehicle. It was invented** — dropped `GOURMET`, reordered `JUICES`, and every sub-line is in no record. Provenance is now **printed on every piece**. |

**STILL OPEN FROM REV 80:** **F370** (the vehicle carries its own type),
**F373** (three layout instruments, one wrong on first writing), **F374**
(`CLAUDE.md` carried a wrong measurement AND the guard greps decimals only),
**F375** (`revstats.py` is blind to drawing).

⚠ **GRADES THE REV-79 BRIEF GOT WRONG, CORRECTED HERE:** **F350 and F356 are
`CLOSED-rev79`**, not `MEASURED-rev78`/`OPEN-rev78` — that brief's §3 sent rev 80
to finish a `sheet.py` repair the machine says shipped. **F348, F355, F357, F358
are `OPEN-rev78`.** **F362 and F365 are `OPEN-rev79`.**

## §3b ⚠ REV 72–80's FIXES ARE LOCKED. **A red row is a FINDING ABOUT YOUR CHANGE.**
A re-base needs the cause NAMED and a companion row making it separately testable.
**RUN `./bootstrap.sh --guards` ONCE THIS REVISION** — ~20 min, not while a queue runs.

---
## §4 THE MACHINE

⚠⚠ **`verify_clone.sh` IS NOT SAFE TO RUN TWICE AT ONCE (F343), AND THERE ARE
FOUR RUNNERS: yours, an adversary's, §7's cold clone, and `audit_brief.py`,
which shells it internally (F357). SERIALISE THEM.** There are **21** fixed
`/tmp` paths in it. ⚠ **AND THE F360 KILL ROW PLANTS A REAL FILE IN THE
REPOSITORY ROOT** (`./.f360_plant_$$.tmp`), not in a `mktemp -d` as the rev-79
brief claimed: an interrupt between the `printf` and the `rm -f` **leaves the
tree dirty and permanently reds the row above it**, and two concurrent runs
plant two files and break both rows. **That is a sharper F343 than the one
documented.**

```bash
./verify_clone.sh                             # ALL 458 PASS on rev 80's tree --
  # 0 FIDELITY, 458 SELF-CONSISTENCY.  READ THE VERDICT BLOCK -- not one row
  # measures the vehicle against a photograph.  ⚠ THE COUNT IS PARSED OUT OF
  # THIS FILE by audit_brief.py; --fix-count can REWRITE it, never create it.
  # ⚠ AND THE THIRD AND FOURTH "458" (in §8, not §7) carry no `ALL n PASS` wrapper, so
  # --fix-count CANNOT reach it -- it will go stale silently.
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # "VERIFY: 0 fail, 0 warn"
python3 apaga.py --selftest                   # 7 checked, 0 FAILED
python3 apaga.py --tag side                   # 17 checked, 0 FAILED
  # ⚠⚠ 17, NOT the 13 the rev-79 brief printed TWICE.  Typed, not watched
  # printing -- rule 5, the same defect that brief documents for sticker's 37/38
T1_APAGA_NOSHUT=1 python3 apaga.py --tag side --out /tmp/ab   # THE KILL -- A8 REDS
  # at 52643 px (9.383 %) against a 5610 px bar.  ⚠ --out DOES NOT PROTECT
  # probe_scratch/apaga_resid.png, which is written to ROOT regardless (§2.5c)
python3 sticker.py --selftest                 # 6 checked, 0 FAILED
python3 sticker.py --tag flank                # 38 checked, 1 FAILED -- C4 BY DESIGN
  # 37 is the count of ck( CALL SITES (6 in selftest, 31 in main); the 38th is
  # W1, which increments the counter directly.  ⚠ `grep -c 'ck('` gives 40, not
  # 38: it counts `def ck(` AND two `np.dstack(` at lines 606 and 955
python3 sticker_pass.py --tag flank --lines   # ~3 min.  ⚠⚠ NOT A PROBE: it renders
  # the whole scene.  DO NOT RUN IT WHILE §0's QUEUE IS GOING, AND IT OVERWRITES
  # THE TRACKED CAPTURE, whose line pass is NOT run-to-run stable
python3 probe_rev73_tailboard.py out/r81_side.png   # 5 checked, 1 FAILED -- T4 only
python3 probe_rev74_tread.py out/r81_side.png       # 8 checked, 0 FAILED
T1_TYRE_TREAD=0 python3 probe_rev74_tread.py        # THE KILL.  REDS T3 AND T7
python3 probe_rev46_vw.py                     # 12 checked, 2 FAILED -- C4 AND C10
python3 probe_rev69_fitpose.py                # 5 checked, 1 FAILED -- P4 only.  ⚠ P1's
  # MESSAGE hardcodes 0.9703 while P1b PRINTS 0.9465; read the NUMBERS
python3 probe_rev71_proxy.py                  # IoU 1.000000
python3 probe_rev77_t3floor.py                # 1 checked, 0 FAILED; verdict is REAL (F354)
python3 visibility_budget.py 3840 out/r81_hero34f.png ; python3 revstats.py
T1_SUB=2 /tmp/blender/blender -b -P audit.py  # rewrites STATE.md -- COMMIT FIRST, and
  # AFTER your LAST source edit.  ⚠ THEN regenerate the design artefacts (F344)
python3 audit_brief.py ; python3 audit_adversary.py   # ⚠ THE FIRST RUNS THE VERIFIER
```
**THE TRACKED CAPTURE'S COST:** `probe_scratch/sticker/` holds **21 tracked
files, 10.1 MB**. That is why `sticker.py`, `apaga.py`, `estilos.py` and
`coleccion.py` all run on a cold clone with no Blender.

⚠⚠ **17+ PROBES REPAINT TRACKED FILES (F329). THE RULE, NOT THE LIST:**
`git status --porcelain ; git checkout -- probe_scratch/` — ⚠ **and F358:
`la_rueda.py`, `calendario.py` and `apaga.py` write into TRACKED `design_out/`,
which that remedy does NOT reach.** `estilos.py` and `coleccion.py` write their
paintings into the `--out` directory, so their ablations are safe.

**THE ABLATIONS.** `verify_clone.sh` runs `T1_REAR_*`, `T1_NOSE_NOWIN`,
`T1_VW_FREE`, `T1_TYRE_TREAD`. ⚠ **IT DOES NOT RUN THE LINE-PASS, STICKER OR
DESIGN ONES (F355):** `T1_LINE_NOCONTOUR` / `T1_LINE_NOCREASE`, `T1_STK_NOOPEN`
/ `T1_STK_NOBRIDGE` / `T1_STK_NOHOLES`, `T1_APAGA_NOSHUT`, and rev 80's
`T1_EST_NOKEY` / `T1_COL_BADGE` / `T1_PROMO_COLLIDE` are **all watched BY HAND.**
"ALL PASS" does not cover any of them.

**FACTS THAT BITE:** the render is **not** run-to-run deterministic (~2.04 % of
pixels >8 levels), and **the line pass is not either** — strokes 2711–2716,
points 19468–19475 at n = 5 on one unchanged tree. `lid_gen.py` / `script_gen.py`
are **not** called by `build.py`. `audit.py` rewrites `STATE.md` — **commit
first.** **A backgrounded runner's `rc=$?` is the redirect's.** ⚠ **Blender 4.x's
default view transform is AgX and a File Output node APPLIES IT — every data
pass must force `view_transform = "Raw"` or it is a picture, not data.**

---
## §5 THE RULES THAT WILL BITE YOU

⚠⚠ **TWO INCOMPATIBLE CANONS FOR 1–33.** **`CLAUDE.md`'s numbered list (1–18) IS
IN FORCE.** `NEXT_CONTEXT_PROMPT_rev50.md` §11 carries a DIFFERENT 1–33 whose
numbers COLLIDE. **Rules 34–58 are in `HANDOFF_CARRIERS.md` §5 — whose first line
says 34–52, and which holds TWO rule 56s and TWO rule 57s. Say which you mean.**

**55 — EVERY REVISION SHIPS A VISIBLE CHANGE TO THE VEHICLE, OR SAYS PLAINLY WHY
IT COULD NOT**, at the TOP of its ledger. ⚠⚠ **REV 80 IS THE FIFTH RUNNING TO
SHIP NO GEOMETRY, AND THE SECOND WHERE THAT IS THE OWNER'S RULING (F361). THE
SECOND CLAUSE REVS 77–79 ALL SAID WAS OWED IS STILL NOT WRITTEN.** ⚠ **AND SEE
F375: the instrument this rule tells you to quote CANNOT SEE DRAWING WORK, so
quoting it alone now misreports the revision.**

**Which bit rev 80: 10 and 5 above all** — a ceiling asserted from memory and
published as "measured" (F371), and a menu invented under a docstring saying it
was not (F372). Also **1** (the seal blot was invisible on the contact sheet and
obvious at full size), **3**, **13**, **8**, **16**.

---
## §6 WHERE EVERYTHING ELSE LIVES

| file | what it holds |
|---|---|
| `LEDGER_rev80.md` | what rev 80 did, **including its TEN wrong instruments and how each was caught** |
| `LEDGER_rev79.md` | the night panels, and rev 79's three wrong instruments |
| `OPEN_FINDINGS.md` | the register. **F368–F375 are rev 80's; DERIVE the next free ID:** `grep -oE '\*\*F[0-9]+\*\*' OPEN_FINDINGS.md \| sort -uV \| tail -1` |
| **`HANDOFF_CARRIERS.md`** | **NOT auto-imported. `cat` it when pointed at.** Every carrier: the goal, the reference set, the refuted emblem routes, §4 the owner's rulings, §5 rules 34–58, §0.12 the seven owner-graded rows, §0.13 the locational series |
| **`CONCEPT_BENCH_rev77.md`** | **THE CARRIER. All 75 concepts in full. 510 KB. Do not compact it** |
| **`CONCEPT_ROUND_rev77.md`** | 255 KB: the synthesis and the audit ranking that **SUPERSEDES `DESIGN_PROGRAM_rev77.md` §2**. ⚠ Its §5.0b item 5 still says the sticker VIEWPOINT row is hard-cut. **IT IS NOT — 142 chars, ends in a full stop. F360** |
| **`CONCEPT_AUDIT_rev77.md`** | 765 KB, adversarial verdicts across four lenses. **A carrier nothing points at is a carrier already half gone** |
| **`WORKFLOW_rev76_CONCEPTS.md` / `WORKFLOW_rev76_SYNTHESIS.md`** | 1.0 MB |
| `AUDIT_rev43.md` | **the sticker spec — in `## 2. SURVIVING FINDINGS`, NOT §5 (F352)** |
| `estilos.py` / `coleccion.py` / `promo.py` | **NEW.** The six styles and the fifteen pieces. ⚠ **`promo.py` IS NOT SUPERSEDED — `coleccion.py` imports nine symbols from it**, including the font table, the letterspacing engine and all three layout instruments (F373). Deleting or rewriting it breaks all fifteen pieces |
| `ref_sign_aframe.jpg` | **NEW.** His photograph of a real Tacombi sign |
| `fonts/` | **NEW.** Alfa Slab One, Oswald **and Bitter** — OFL, fetched after F371. ⚠ **`Bitter.ttf` is tracked and referenced by NOTHING** (44 880 B) |
| `STATE.md` | machine-written; outranks every prose description |
| `SPEC.md`, `REF_MEASUREMENTS.md`, `SURVEY_rev49_photoreal.md`, `ROADMAP_rev68.md`, `REMAINING_WORK_rev61.md`, `EMBLEM_HANDOFF.md`, `PHOTOS_WANTED_rev52.md` | large; load the one the task needs |

**⚠ IDs LEANED ON WITHOUT NAMING, SO A GREP FINDS THEM (rule 16): `F15` `F18`
`F21` `F44` `F56` `F67` `F71` `F91` `F92` `F93` `F94` `F104` `F156` `F161` `F163`
`F164` `F165` `F166` `F173` `F183` `F188` `F191` `F192` `F193` `F205` `F214`
`F215` `F229` `F234` `F241` `F252` `F259` `F262` `F276` `F281` `F284` `F289b`
`F296` `F301`–`F305` `F308` `F309` `F311` `F312` `F314` `F316` `F317` `F319`–`F375`.**

---
## §7 HOW TO CLOSE

**HIS STANDARD:** photo-real parity with **that exact bus**, in service of a
promotional render. **Any single measurement off is unacceptable** —
per-measurement, not on average. **Never call it done off self-review. Report
the measurement with its ceiling. Do not say anything is ready.**

1. `./bootstrap.sh` and `./verify_clone.sh` on a **clean** tree. **The honest
   closing condition: every red is one you can name, and none of them is yours.**
2. `python3 revstats.py` — put its line in the ledger header **and say in the
   same breath what F375 says it cannot see.**
3. Regenerate `STATE.md` (`T1_SUB=2 … audit.py`) — **commit first, AFTER your
   last source edit. Then REGENERATE THE DESIGN ARTEFACTS**, then `audit_adversary.py`.
4. **DISPATCH an adversary at the brief you WROTE (rule 17) and one at the brief
   you RECEIVED (rule 15). DO NOT CLOSE UNTIL BOTH REPORT.** ⚠ **SERIALISE THEIR
   VERIFIER RUNS AGAINST YOURS.**
5. **Keep the split, and KEEP THIS FILE SHORT** (<32 KB, machine-checked).
   `cp` it over `PASTE_INTO_CLAUDE_CODE.txt` in the same commit.
   `python3 audit_brief.py --fix-count` LAST.
6. ⚠⚠ **THEN COLD-CLONE AND RUN `./bootstrap.sh` — LAST, ON A FRESH CLONE (F328).**
7. ⚠ **COMMIT ANY ROUND'S OUTPUT IN FULL, IN THE SAME COMMIT THAT ANNOUNCES IT
   (F335). If it is not in `git ls-files`, it does not exist.**

---
**⚠ THIS BRIEF WAS AUDITED AGAINST THE MACHINE.** The rule-15 pass against the
brief rev 80 was handed returned **24 findings, fifteen of which changed what rev
80 did** — including three against rev 80's own new modules, all three real. §8
records them, and the rule-17 pass against THIS file is recorded there as items
16–25 with its own ceiling. **The
phrases `verify_clone.sh` binds VERBATIM are carried:** the ranking sentence
opening §2, rule 55's wording in §5, and the first line of this paragraph — **IF
YOU SHORTEN THIS FILE, RE-RUN THE VERIFIER AFTERWARDS AND ON A COLD CLONE (F328).**

**WHERE THIS BRIEF IS WEAKEST, STATED RATHER THAN HIDDEN:**
* **NOTHING IN THIS TREE CAN GRADE ANY OF THE FIFTEEN PIECES**, and he has
  already rejected one full round of them.
* **THE FIFTEEN HAVE NOT BEEN PUT TO HIM SINCE THE F371/F372 REPAIRS.**
* **F374's GUARD GAP IS STATED, NOT CLOSED** — `CLAUDE.md carries no
  measurements` greps **decimals only**; its green does not mean what it says.
* **F375 IS STATED, NOT FIXED** — `revstats.py` scores this revision `0 / 0`.
* **`apaga.py`'s PAINTED MASK IS ALL BLACK** and never paints its window.
* **THE FOUR-FRAME QUEUE's REV-79 DEATH IS UNDIAGNOSED.** One clean run is not a fix.
* **EVERY AUTHORED CONSTANT IN `apaga.py`, `estilos.py` AND `coleccion.py` WAS
  TUNED BY LOOKING.**
* **F353's HUE HEADLINE:** `sticker.py` C4 prints **43.2°** and **2.79 %** — not
  the `42.8°` / `2.84 %` the rev-79 brief published. **`T1_paint`'s "hue" is
  1.80° on the flank and 42.86° on the nose — the same material, at saturation
  0.101, so the figure is a property of which side the camera is on. NOBODY HAS
  PAINTED THAT WINDOW.**
* **THE EMBLEM IS NOT RIGHT.** 0.8528 against 0.9465, no legibility term.

---
## §8 ⚠ WHAT THE ADVERSARIES FOUND, RECORDED AS RULE 17 REQUIRES

**The rule-15 pass returned 24 against the incoming brief and rev 80's own work;
fifteen changed what rev 80 did. Nineteen are itemised below and the remaining
five are carried at the end of this section.**

1. ⚠⚠ **F369 RETRACTED F368 IN A SUCCESSOR ROW ONLY** — F368's row still carried
   the retracted claim, so a grep for *"flat illustration"* landed on it with
   nothing beside it. **Rule 13 says retract IN the source.** F368 is now
   `AMENDED-rev80`.
2. ⚠⚠ **THE TYPE CEILING WAS FALSE IN BOTH HALVES AND SAID "measured".** F371.
3. ⚠⚠ **THE MENU WAS INVENTED UNDER A DOCSTRING SAYING IT WAS NOT.** F372.
4. **`estilos.py` CLAIMED "PAINTED AND LOOKED AT" AND WROTE NO MASK**, and had
   no ablation at all. Both fixed: it paints every layer every run and
   `T1_EST_NOKEY=1` reds four recovery rows.
5. **`CLAUDE.md` CARRIED A WRONG MEASUREMENT** — `287` where `revstats.py` prints
   **153** — in the sentence explaining why measurements were deleted from it.
   **And the guard named for exactly that greps decimals only.** F374.
6. **`revstats.py` IS BLIND TO DRAWING.** F375.
7. **THE REV-79 BRIEF'S GRADES FOR F350 AND F356 WERE WRONG** (both
   `CLOSED-rev79`), in a paragraph headed *READ THE GRADE IN `OPEN_FINDINGS.md`,
   NOT THIS TABLE*. Corrected in §3.
8. **F164 WAS ASSERTED CLOSED AND LISTED AS OWED IN THE SAME BRIEF.** The
   register grades it `RULED-rev62`. Corrected in §2.7.
9. **`apaga.py --tag side` READS 17, NOT 13.** Rule 5. Corrected in §4.
10. **§2.5 ORDERED REV 80 TO FINISH THE 1075 px THE SAME BRIEF RETRACTS.**
    Rewritten to the three defects that are actually live.
11. **`probe_scratch/apaga_resid.png` IS ENTIRELY BLACK** and never paints its window; and it
    is written to `ROOT` **regardless of `--out`**, so the ablation overwrites
    the tracked evidence. **F358 is incomplete.**
12. **`verify_clone.sh`'s F360 KILL PLANTS A FILE IN THE REPOSITORY ROOT**, not
    in a `mktemp -d`. Sharper F343 than documented. §4.
13. **§7 SAID THE FOURTH FRAME NEVER LANDED** while §2 said the budget ran on it;
    all four are present and every budget figure reproduces.
14. **§8's HUE FIGURES WERE NOT WHAT THE MACHINE PRINTS** — 43.2 / 2.79, not
    42.8 / 2.84. Rule 5.
15. **§7 LISTED THE NOSE 200° AS UNEXPLAINED** while §8 explained it (`lens` 180°
    against `script` 340°).

**Also found and carried:** `promo.py` reads **17 on a clone, 20 here**, and
ships a committed artefact no clone can regenerate; `--fix-count`'s PAIR regex
cannot match the brief's own wrapped text and **can never reach the third
`458`**; the `emit=(` quadruple `0/0/1/0` is **unordered and unreproducible as
written** (the hit is `gal_tube` at `t1_detail.py`); and `sticker.py`'s 37-vs-38
explanation needed one more clause (37 call sites, 6 + 31, W1 is the 38th).

**THE RULE-17 PASS AGAINST THIS FILE RETURNED 28. Ten changed what shipped.**
16. ⚠⚠ **THE LEDGER ANNOUNCED AN ABLATION GUARD THAT DID NOT EXIST, AND THE
    ADVERSARY PROVED IT BY OVERWRITING EIGHT TRACKED ARTEFACTS.** F377. Built.
17. ⚠⚠ **THE F371 RETRACTION NEVER REACHED `estilos.py` OR `coleccion.py`**,
    while F371's grade cell certified that it had. **F360 verbatim, one
    revision later.** Carried into all three modules.
18. **THE RULE-8 PAINTING LEFT 15.5 % OF THE VEHICLE WHITE** — the same white as
    the page — so a sixth of the subject was invisible in the one artefact
    offered as evidence. F378. Now magenta, with a coverage check.
19. **`LETRERO` WAS NOT REPLICATED** — two accents added, conjunction
    upper-cased, on the one string sourced to his photograph. F376.
20. **THE COLLECTION REPRODUCES F01/F39 AND F63/F69 FIFTEEN TIMES.** F379.
21. **`promo.py` WAS HARD-PINNED TO `out/r80_hero34f.png`**, so `07_hero` would
    have SKIPped silently from rev 81 on. Now globs the newest frame.
22. **`audit_brief.py`'s F306 ROW HAS MATCHED NOTHING SINCE REV 77** and passes
    on an empty match set. F380.
23. **THE EMBLEM RANKS WERE 9/11/14/16, NOT 9/11/15/16.** Corrected in §2.
24. **NINE RULE-16 CARRIER DROPS** — F323, F345, F363, F365's substance,
    `LEDGER_rev44.md`, `LEDGER_rev78.md`, `cream_rms.py`, `flank_compare.py`,
    the `gal_tube` and FIRST-STEP notes. **All restored in §2.10.**
25. **THE "NO DISCOUNT AS FACT" SENTENCE WAS STRONGER THAN THE ARTEFACT.**
    Softened in §2.2.

⚠ **AND ITS FIVE UNRECORDED SIBLINGS FROM THE RULE-15 PASS, CARRIED HERE SO
"all are carried" IS TRUE:** `promo.py` had no ABSENT accounting for a skipped
piece; the `emit=(` quadruple `0/0/1/0` is unordered and unreproducible as
written (the hit is `gal_tube` in `t1_detail.py`); `--fix-count`'s PAIR regex
cannot match the brief's own wrapped text; `verify_clone.sh` writes
`./.f360_plant_$$.tmp` into the repo root; and `audit_brief.py` prints green
over that empty match set (F380).

**⚠ THE RULE-15 PASS'S OWN CEILING, IN ITS WORDS:** it did not run
`verify_clone.sh`, `bootstrap.sh`, `audit_brief.py`, `audit.py`,
`sticker_pass.py` or any Blender command, **so the 458, every ablation run
through the verifier, and `VERIFY: 0 fail, 0 warn` are unverified by it.** It did
not run `apaga.py --tag side` or the four `probe_rev*` scripts, because all of
them write into tracked paths. **And, like every pass before it: nothing it ran
can say whether any of these drawings is any good.**
