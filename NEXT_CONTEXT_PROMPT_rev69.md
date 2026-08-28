# NEXT CONTEXT PROMPT — rev 69

## §0.0 DO THIS FIRST — THE WHOLE DECISION, IN TWENTY LINES

**Before you read another word, put the machine to work. It is CPU-bound and idle right now.**

```bash
cd /home/user/combi_render
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
nohup setsid env T1_SUB=1 T1_PREVIEW=front,side,hero,hero34r T1_PFX=r69 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r69.log 2>&1 < /dev/null &
```

**⚠ `bootstrap.sh` FAILED 3 OF 10 AT REV 68's PICKUP AND THE FIX IS ONE LINE.**
`numpy, pillow, scipy — missing: PIL`, which also fails the shim-import row and
`verify_clone.sh`. **`pip install pillow`, then re-run — bootstrap then reports 10 of 10.** Do not
debug it; the toolchain simply does not come up clean here.

`out/` is untracked and **starts EMPTY**. **`bootstrap.sh` first**, then start the render,
then read. **`grep -c Saved: /tmp/r69.log` must be 4** — a backgrounded runner's exit code is
the redirect's. **USE `setsid`, NOT A BARE `nohup &`** (F173).

**AND CHECK YOUR CLONE IS THE TIP.** Rev 62 through **rev 68** all arrived **SHALLOW** —
**eleven running**, and the designated branch's remote copy was **DELETED** the same eleven
times. A content check cannot detect that you are on an old commit. **Only `git fetch
--unshallow` and the ahead/behind loop in §1 find it.**

**THEN RUN `./judge_set.sh r69`.** `post.py` implements bloom → CA → vignette → grain and the
preview path **never calls it** (F146). Judge photorealism on the `_post` set, never the raw
one. *(**ONLY `bloom` defaults to 0.0** — `ca`, `vig` and `grain` default to **1.0**; F189a.)*

**READ `LEDGER_rev68.md` §2, §4 AND §7 BEFORE YOU PLAN** — the headline refutation, the five
things rev 68 got wrong in its own work, and what it did not do.

---
## §0.05 THIS BRIEF WAS AUDITED AGAINST THE MACHINE — AND WHERE IT IS WEAKEST

**HOW IT WAS AUDITED (rule 17).** Every figure in §0.06, §0.065 and §3 was RE-RUN at the
handoff commit, not transcribed. `audit_brief.py` and `audit_adversary.py` were both run, and
**four of the adversary's questions were REPLACED** — §10 item 5. Two could no longer fail
(the fixture-to-skin defect is FIXED, so the question now guards the fix; the nose-constant
question was a GREP that broke on a refactor and now RUNS the ablation in a fresh process) and
two asserted states the register has refuted (C8 *"still failing"* while C8 PASSES; *"144
perturbed builds gave 7 not once"*, refuted by F209).

**⚠ AND THE THING THIS BRIEF MOST WANTS YOU TO KNOW: REV 68's INSTRUCTION WAS TO FIT THE NOSE
TO A NUMBER, AND THE NUMBER WAS MEASURED OFF A DIFFERENT OBJECT.** §3 item 1 of the rev-68
brief said *"THEN fit to F221's bracket"*. Had rev 68 done as it was told, it would have moved
`NOSE_BULGE` and **changed the measured quantity by not one micron**. See §0.06. **The lesson
is not "F221 was sloppy" — it is that a brief's own top item can be aimed at the wrong
object, and only opening the source stops it.**

**WHERE THIS BRIEF IS WEAKEST:** **§0's inherited gate table** and **§4**, still the two
longest carriers and still mostly inherited text. **AND §2's REFUTED LIST**, which an
adversary has now broken in three consecutive revisions (fourteen at rev 64, thirteen at
rev 67, twelve at rev 68). **Start an adversary there again — it has paid every time.**
**AND THE ROWS IN §0.07's TABLE THAT NOBODY HAS RE-RUN THIS REVISION** are marked as such;
do not quote them as fresh.

---
## §0.06 THE NOSE: THE TARGET WAS MEASURED OFF THE WRONG PRESSING (F222/F223)

> *[owner, rev 66, asked whether rev 67 should do the nose or finish the emblem]*
> **the NOSE.**

**F221 PUT THE REAL BUS AT B ≈ 40 mm AND THE REV-68 BRIEF SAID TO FIT `NOSE_BULGE` TO IT.
F221's SAGITTA IS TRACED ON THE BUMPER'S TOP EDGE; ITS 19.6 mm DENOMINATOR IS THE SHEET-METAL
FACE. TWO DIFFERENT PRESSINGS.**

**AND THE REGISTER ROW DIRECTLY ABOVE F221 ALREADY SAID SO.** F216 — same revision, same
grade, one row earlier: *"The bumper is a separate wrap-around pressing, below all four of the
z stations (0.65…1.10) at which F207's mm figure is defined … **says nothing about the
sheet-metal face**."* **F221 does not cite, rebut or mention it.** This is F209's shape
exactly, one revision later. **READ THE REGISTER FOR A FINDING BEFORE YOU DERIVE ANYTHING.**

**THE BUILT BUMPER IS DEAD FLAT OVER PRECISELY F221's OWN WINDOW.** `t1_detail.bumper` appends
eleven points at CONSTANT x under its own comment `# flat nose face`:

```
    T.G(0.48) = 0.9656   T.WX(2.108) = 0.7244   ->  the flat run spans |y| <= 0.6995
    F221 forward-models  x(y) = x0 + B(1 - (y/0.70)^2)  over  |y| <= 0.70   SAME SPAN

    MEASURED ON THE MESH, two independent builds:
      built bumper_f TOP EDGE   x(0) - x(0.70) =  +0.05 mm  /  0.077 mm
      SHELL at the same height                    +8.26 mm
      SHELL at z 0.65 / 0.80 / 0.95 / 1.10        +19.64 / +19.83 / +19.99 / +16.84 mm
```

**AND `NOSE_BULGE` CANNOT REACH THE BUMPER AT ALL.** The bulge ellipse is
`((z-1.00)/0.46)^2 <= 1`, i.e. **z ∈ (0.540, 1.460)**; the blade centre is **0.480**, where
`max(0, 1-r) = 0` for every y. `grep -n "nose_shape" *.py` returns **one call**, on `body`.

**WHAT SURVIVES IS BETTER THAN F221, BECAUSE IT NEEDS NO CAMERA.** A straight 3-D line images
straight under ANY pinhole camera at any pose, so the SIGN is projection-invariant. **The
photographed bumper's near half is curved at 11–14 σ; the built bumper is straight BY
CONSTRUCTION, everywhere.** No camera model, no EXIF, no F26, no distortion term. **The defect
lands on `t1_detail.bumper`.**

**CEILING, AND IT NARROWS THE CLAIM.** The curvature is **not uniform across the window**:
over `u < 220` — the half spanning the centreline — the sagitta is **+0.08 ± 0.36 px,
consistent with ZERO**. A plan parabola has constant second derivative in y, so the
single-parabola fit is a mis-model and the ±0.09 px is a formal error on it.

**AND NOTHING IN THE RECORD NOW EXCLUDES THE SHIPPED 19.6 mm NOSE (F223).** Propagating
F221's OWN failed validation instead of setting it aside — ring foreshortening 0.533 against
0.556 (**1.57°**) and the belt line **18 px** out (1.90° at f = 544) — and combining with its
own distortion bracket gives **B ∈ [16, 76] mm**, which **contains 19.6**. The wheelbase check
offered as corroboration is `|P₁−P₂|` from `ρ = fR/a`: **invariant under camera rotation,
hence blind to elevation BY CONSTRUCTION** — and `B ∝ 1/sin(el)` at el ≈ 6.75°.
**AND F221 EXISTS IN NO SCRIPT.** `git show --stat c1707cf` touches only `OPEN_FINDINGS.md`
and `probe_rev67_nose.py`. Not reproducible, not ablatable, no kill.

**WHAT IS NOT REFUTED: THE OWNER'S RULING.** *"Rounder than D"* (F214) is a ruling on
DIRECTION and carries no number. **It outranks all of the above.**

---
## §0.065 AND FOUR MORE INSTRUMENTS WERE FOUND REPORTING THINGS THAT ARE NOT MEASUREMENTS

**F224 — `T1_VW_SOLVE=1`, §3's PRESCRIBED FIX FOR C4, CANNOT MOVE `VW_W_ARM_X` AT ALL.**
`solve()` clips every X parameter: `if p.endswith("_X") and not (0.05 < trial[p] < 0.95):
continue`, with `step["VW_W_ARM_X"] = 0.140`. **Shipped `VW_W_ARM_X = 1.1002` is OUTSIDE that
interval** — zero admissible trials over all nine step halvings, and `solve(REV45)` starts at
0.760 so it **cannot even return to the shipped point**. The owner's *"the W's outer arms sit
too low"* maps onto the one constant it cannot touch. **`T1_VW_CELLSOLVE`'s box excludes two
of six** as well (`_hi["VW_W_ARM_X"] = 1.05`, `_lo["VW_APEX_Z"] = 0.15`).

**F226 — C8's TARGET WAS NEVER RE-BASED. F194 AND §9's *"re-basing C8's target"* ARE TRUE IN
PROSE ONLY.** `photo_elongation()` still returns the 69/41 bbox squash; the live run prints
**`PHOTOGRAPH elongation 3.39 … [PASS] C8`**; an independent replica gives 3.3896, and
`grep -rn "2\.627\|2\.960" --include=*.py .` returns **zero hits anywhere in the tree**.
**Corollary: §2 row 2's *"F152 was scored on C8's OLD target"* is FALSE — the target is the
same today.** And **three probes still hard-code `PHOTO_E, PHOTO_N = 3.390, 7`** —
`probe_rev63_ablate.py`, `probe_rev63_shapefit.py`, `probe_rev63_final.py` — where in
`ablate` **`PHOTO_N` is a hard SEARCH CONSTRAINT**. **§2 says chasing 7 is refuted and §6 of
the rev-68 brief told you to run that search.**

**F225 — `probe_rev67_nose.py` SILENTLY DROPPED P3 ON THE BARE INVOCATION AND REPORTED A CLEAN
PASS.** `4 checked, 0 FAILED`, exit 0, while §0.07 of the rev-68 brief published *"5 checked,
1 FAILED — P3"* and §0.05 held that row up as proof its audit worked. **FIXED at rev 68**; and
**this brief prints the frame argument, which no brief ever did.**

**F228 — THE RENDER NOISE FLOOR, MEASURED FOR THE FIRST TIME.**

```
    IDENTICAL TREE, TWO RUNS   >8 levels 42 955 px = 2.441 %   worst channel 40
    BEFORE vs AFTER a change   >8 levels 42 876 px = 2.436 %   worst channel 40
```

**F217 published *"2.54 % of pixels differ by >8 levels"* as evidence its change moved the
render. THAT IS THE FLOOR.** What survives is worst-channel (179 vs 40) and localisation.
**BINDING: render the CONTROL TWICE and publish the floor beside any render A/B.**

**F227 — F218's *"+9.66 mm"* is 2.60 mm by its own two numbers**, and its fold ceiling
belongs to the **REVERTED** form. **The SHIPPED form cannot fold at any B** (analytic, and
empirical to 0.40). What actually binds a bulge change is `length`: **0.045 gives
`warn length 4.073 vs spec 4.055 (+18 mm)`**, and `dΔ/d(NOSE_BULGE) ≈ 0.72 m`.

---
## §0.07 THE MACHINE'S VERDICT AT CLOSE OF REV 68 — every one watched print

```
bootstrap.sh              ALL 10 PASS -- but only after `pip install pillow`.
                          Clone arrived SHALLOW, the ELEVENTH running
verify_clone.sh           ALL 348 PASS on a clean tree, AT THE HANDOFF COMMIT
                          <- 0 FIDELITY, 348 SELF-CONSISTENCY.  336 -> 342.
                          ONE row RE-BASED, cause named + FIVE companion rows.
                          NO row relaxed.
build.py T1_VERIFY=1      VERIFY: 0 fail, 0 warn at SUB=1
audit.py T1_SUB=2         VERIFY: 0 fail, 0 warn -- STATE.md moved ONLY in
                          provenance plus the new row's log lines.  Every vertex
                          count and dimension identical = the change was contained
verify.py nose fixtures   NEW.  WATCHED REFUSING: 8 fail at NOSE_BULGE 0.045 with
                          T1_NOSE_FIXFOLLOW=0; 0 fail with the follow ON
probe_rev46_vw.py         12 checked, 1 FAILED -- C4 ONLY, at 0.0755 (bar 0.045).
                          BUT SEE F210/F211/F226 before quoting any of it.
                          C6 PASSES 6 = 6 -- **ON THE RASTER.  ON THE RENDER THE SAME
                          FUNCTION READS 3 AGAINST THE PHOTOGRAPH'S 6 (F205), AND REV 67
                          RE-MEASURED THAT ON ITS OWN FRAME (F212).**  A gate can be
                          corrected, guarded, killed, swept and still be measuring the
                          wrong object -- rule 41.  RUN THE EMBLEM GATES ON THE FRAME
probe_rev67_nose.py       **PASS IT A FRAME**: `python3 probe_rev67_nose.py
                          out/r69_front.png` -> 5 checked, 1 FAILED (P3, a correct
                          REFUSAL).  BARE it now SAYS P3 did not run (F225)
F205 ON THE FRAME         PHOTOGRAPH 6  |  render 4 / 3 / 2 at thr 20/30/40
                          <- the gate that matters, and it is RED.  NOT re-run at
                          rev 68; looked at on out/r68b_front.png and the W's
                          outer arms visibly stop short of the ring
probe_rev65_unproject.py  10 checked, 0 FAILED
probe_rev64_shear.py      6 checked, 0 FAILED -- but its S4 guards the target 7
                          that F200 RETIRED (F226)
probe_rev63_trace.py      ALL CONTROLS PASS -- FIVE of its NINE are ctl(..., True,
                          ...) and cannot fail.  (The rev-68 brief said "five of
                          ten"; the file has NINE ctl( calls.)  Not a verdict
probe_rev63_reach.py      ALL CONTROLS PASS -- SIX ring contacts at 16, 66, 114,
                          163, 248, 292 deg.  **F180's live text says FOUR and is
                          STALE.**  And what moved four -> six is NOT the arc cut:
                          under T1_VW_NOARC=1 it still reads six
vw_pressing.py            5 checked, 0 FAILED
trace_outline.py          SELFTEST PASS ;  svgraster.py  SELFTEST PASS
audit_brief.py            10 checked, 0 FAILED
audit_adversary.py        57 asked, 0 BROKE -- FOUR questions REPLACED
T1_VW_CAPMIN=1            now REFUSES, exit 1 (was a bit-identical NO-OP)
T1_VW_PUREFIT=1           now REFUSES with a summary line, exit 3 (was a traceback)
T1_VW_WFRAC=0.1800        now REFUSES with a summary line, exit 3 -- **this is
                          F204's OWN before-side, and it could not be re-run**
flank_compare.py          FAILS -- NOT re-run at rev 68, inherited
gloss_compare.py          FAILS at 0.441 (bar 0.60) -- NOT re-run at rev 68
probe_rev59_nose.py       5 checked, 0 FAILED -- NOT re-run at rev 68
probe_rev59_door.py       8 checked, 1 FAILED (M3, BY DESIGN).  PASS IT THE **side**
                          frame -- NOT re-run at rev 68
```

**AND THE STANDING WARNING, WHICH `verify_clone.sh` PRINTS ITSELF.** A green check is not
evidence about the vehicle. **Not one of those rows compares the model to a photograph.**
The three that do are `flank_compare`, `gloss_compare` and `probe_rev46_vw` — **and two of the
three still fail.**

---

## §0. THE GOAL, AND HOW FAR OFF IT WE ACTUALLY ARE

**CARRIED FORWARD FROM THE REV-55…68 BRIEFS. It is not mine and it is not to be dropped —
rule 16.**

**PHOTO-REALISTIC PARITY WITH THAT EXACT BUS.** Not "a convincing VW bus" — *that one*, the
red Señor Tacombi combi in the frames on this repo. **Any single measurement off is
unacceptable, per-measurement and not on average.** A model right in ninety places and wrong
in one is not 99 % done, because he will look straight at the one. **At rev 58 he did exactly
that, at the emblem, for the fifth time. At rev 61 he did it again. At rev 62 he said *"I am
sick and tired of not being able to execute a publicly available emblem."***

**AT REV 63 THE EMBLEM CHANGED AND NOW READS AS A V OVER A W ON THE NOSE. IT IS NOT RIGHT,
AND AT REV 64, 65, 67 AND 68 IT DID NOT MOVE. AT REV 66 IT MOVED: the strokes were measured
24 % too thin and are fitted, and the terminal caps are cut on the band's arc.** Held next to
the photographs, four things are still visibly wrong: the glyph does not fill its ring the way
both photographs do, the V is too narrow, the W's outer arms are too short, and the strokes
are thinner than the pressing's. **The W's two outer arms visibly FLOAT short of the ring —
looked at again on `out/r68b_front.png` at rev 68, unchanged.**

**AND HERE IS THE HONEST DISTANCE — THE GATE TABLE, WHICH AN ADVERSARY ONCE CAUGHT A BRIEF
DROPPING.** `verify_clone.sh` ends **ALL 348 PASS**: **0 FIDELITY, 342
SELF-CONSISTENCY.**

| gate | state MEASURED at close of rev 64 unless noted |
|---|---|
| `flank_compare.py` | **runs, FAILS.** Worst region **`i` at 0.687 of its own ceiling**; the `Senor` row scores a **DELIBERATE DEPARTURE** — F156, **EIGHT revisions un-re-based** |
| `gloss_compare.py` | **runs, FAILS at 0.441** (bar 0.60). Model-side lever EXHAUSTED (F60/F62) — **but F62's ceiling is DISPUTED on measurements** |
| `probe_rev46_vw.py` | **RE-MEASURED AT REV 68: 12 checked, 1 FAILED — C4 ONLY, at 0.0755 (bar 0.045).** **AND `T1_VW_SOLVE`, the prescribed fix, CANNOT MOVE `VW_W_ARM_X` (F224).** **AND C8's target was never re-based (F226).** Read §0.065 before quoting any of it |
| `verify.py` nose fixtures | **NEW at rev 68 (F217).** Raycasts each fixture's rearmost face against the skin at its own (y, z). **WATCHED REFUSING**, 8 fail |
| `probe_rev64_shear.py` | **6 checked, 0 FAILED** — but S4 guards the retired target 7 (F226) |
| `probe_rev63_trace.py` | **ALL CONTROLS PASS.** The trace is sound; what it traced is a sheared frame (F183) |
| `probe_rev59_nose.py` | **M1 PASSES lens-ruled — AND THAT IS NOT CLOSURE (F136).** Bezel-ruled 1.550 / 1.584 against rim-ruled 1.951–2.121 |
| `mottle_measure.py` | **runs, and it is NOT measuring the mottle** — 1.1–2.0 % of it |
| `probe_rev45_ground.py` | item D's gate, `T1_NOUNDER`'s only consumer. **G4 0.3602 built / 0.5475 ablated / 0.057 photographed** |
| `probe_rev59_door.py` | `T1_DOOR_STALE`'s gate. **8 checked, 1 FAILED (M3, BY DESIGN)** |
| `cream_rms.py` | `run()` is the LIVE photograph-side cream path |
| `visibility_budget.py` | the RANKING, not a gate. **PASS IT A `.png`** — `visibility_budget.py 3840` alone falls back to globbing `out/*hero*.png` by mtime, **which IS F132's defect** (F189) |
| everything else | self-consistency |

**AND AT REV 61 HE ADDED A STANDARD.** *"I want this 3d model to look like new. Enhanced from
the photo."* That is not the same as WEATHERED, which SPEC §3 locks. **Where the two collide,
say so and put it to him** — do not silently pick one.

### §0.1 THE REFERENCE SET IS COMPLETE, AND IT IS GUARDED FRAME BY FRAME

> *[owner, rev 54]* **"we have all references that we need on repo and I want to make sure
> that is never forgotten."**

**ONE: WHAT WE HOLD IS WHAT WE GET. STOP PARKING WORK BEHIND A PHOTOGRAPH.** Where a frame
genuinely cannot answer, the result is *"it cannot be recovered from what we hold"* — a real
result, stated with its ceiling. **Rev 61 produced four; rev 63 one; rev 64 one; rev 68 one
(F223: nothing in the record excludes the shipped nose).**

> **⚠ AND REV 68 ADDS THE LIMIT ON THAT PRINCIPLE, AND IT IS AN OWNER RULING (F229).** Asked
> to lay a straight edge across the front bumper corners, he answered ***"This has to be a
> commonly available measurement."*** **He is right.** A T1 bumper and front panel are
> catalogue pressings on one of the most documented vehicles ever built. **"What we hold" means
> the PHOTOGRAPHS of THIS vehicle. It was never meant to bar the factory literature for a
> FACTORY PART** — rule 11 already holds that a pressing is GEOMETRY and transfers, and it
> follows that its dimensions are public. **Before asking him for any measurement of a factory
> part, check the catalogue literature first.**

**TWO: THEY CANNOT BE RE-SHOT, SO THEY ARE CHECKSUMMED INDIVIDUALLY.** **16 `ck "ref …"` rows
name them one at a time** *(the "18" in the rev-63/64 briefs counted two aggregate rows that
by their own words do not name a frame — F189)*:

* **the RED target bus** — `ref_side.jpg`, `ref_rear34.jpg`, `ref_playa_34.png`,
  `ref_nolita_front34.jpg`, `ref_nolita_front34b.jpg`, `ref_nolita_flank.jpg`,
  `ref_nolita_doorshut.jpg`
* **NOT the target, geometry only** — `ref_workshop.jpg` is the **GREEN** vehicle;
  **`IMG_2073.jpeg` is ALSO the GREEN vehicle**; `bus_model_ref.JPG` is a **SCHOOL BUS**, a
  fidelity bar only. **Paint and artwork do not transfer between vehicles; geometry does
  (rule 11)** — *and the nose roundel's SHAPE is the factory chrome PRESSING, which is geometry
  and DOES transfer; only its colour is artwork (F141).* **REV 64's LIMIT: the shape transfers,
  the PROJECTION does not (mirror IoU 0.4111, F184).**
* **AND RULE 11 APPLIES BETWEEN LIVERY STATES OF THE SAME VEHICLE**, which killed F99, F100
  and F140: `ref_nolita_front34b.jpg` has a chalkboard lid and no folk art.
* **AND IT APPLIES BETWEEN ERAS OF A TRADEMARK** — F168. `vw_canonical_2019.svg` is a
  **different object** from the 1955–67 pressing. **Deliberately NOT named `ref_*`.**
* **derived/annotated** — `ref_grid.png`, `ref_side_grid.png`, `ref_nose_grid.png`,
  `ref_band_grid.png`, `ref_x6_lanczos.png`
* **retired** — `ref_source.jpeg`, a 246×197 thumbnail the record itself retired
* a **floor of 54** reference-class tracked images, and **the five byte-identical pairs are
  asserted to stay five** — a sixth group means a duplicate arrived, which is **not
  corroboration** and has fooled this project before.

**AND TWO FRAME FACTS WORTH CARRYING (rev 67):** **`ref_side.jpg` has the CAB DOOR OPEN** and
occludes the nose to a sliver; **`ref_nolita_doorshut.jpg` has it SHUT** and is the
unambiguous side elevation for nose geometry, at 107 px/m against `ref_side`'s 220.
**`ref_playa_34.png` IS UNDER-USED** — its white balance is neutral on the paving
(116,119,120); `ref_side.jpg` and `ref_rear34.jpg` are both globally WARM.

**AND THE EXIF, WHICH NOTHING IN THIS TREE HAD EVER READ BEFORE REV 67 (F219, RE-VERIFIED AT
REV 68):** `ref_nolita_front34.jpg` is `SONY DSC-RX100`, `FocalLength 10.4`,
`FocalLengthIn35mmFilm 28`, `DigitalZoomRatio 1.0`, 700×467 → **f = 544.4 px ± ~2 %**.
**But `ref_nolita_doorshut.jpg`'s "f = 320.0 px" is NOT from EXIF** — it carries no
`FocalLengthIn35mmFilm` and `exif_focal()` returns **`None`**; 320.0 is a sound INFERENCE from
a 36 mm sensor, not a carried intrinsic. Say which it is.

---
---
## §1 START HERE — MEASURE THE BRANCH, DO NOT TRANSCRIBE IT

```bash
git fetch --all --prune
git rev-parse --is-shallow-repository        # <- rev 62..68 ALL arrived TRUE
for b in $(git branch -r | grep -v HEAD); do
  printf "%-52s ahead %-3s behind %s\n" "$b" \
    "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"
done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
./bootstrap.sh          # read ROW 9, and read the "N ahead / M behind" NOTE line
./verify_clone.sh       # ALL 348 PASS -- and read its verdict block
```

**MEASURED AT REV 68 PICKUP:** the clone was **SHALLOW** — the **ELEVENTH running**, and
`bootstrap.sh` unshallowed it to 626 commits; **`bootstrap.sh` FAILED 3 of 10 because PIL was
missing** (`pip install pillow` fixed it); `fetch --prune` printed `- [deleted]
origin/claude/nose-fixture-alignment-r68-rrqyqx`, **the designated branch, before anything had
been pushed to it, THE ELEVENTH RUNNING**; HEAD was **0 ahead / 0 behind** `origin/main`;
**row 9 PASSED**; and `git diff --name-only HEAD...origin/main` was **EMPTY** — no new
photographs. **EXPECT ALL OF IT AGAIN AT REV 69.**

> **AND THE LESSON THAT COST EIGHT REVISIONS: no sentence about branch state survives the
> hour. `bootstrap.sh` row 9 outranks every sentence, INCLUDING THIS ONE.**

**AND MEASURE IT AGAIN BEFORE YOU FINISH.** `origin/main` moved mid-revision at rev 51 and
rev 55; the pickup figure is NOT the close figure. **AT REV 68's CLOSE, see `LEDGER_rev68.md`
§8.**

---
## §2 THE EMBLEM — **READ `EMBLEM_HANDOFF.md` FIRST, AND READ ITS §5b.2 RETRACTION.**

> *[owner, rev 62]* **"I am sick and tired of not being able to execute a publicly available
> emblem."**

> **⚠ AND READ THIS BEFORE `EMBLEM_HANDOFF.md`, NEW AT REV 68: THAT FILE'S §3 IS A SECOND,
> STALE COPY OF THE LIST BELOW.** Eleven rows, ending at F170, **none of them annotated**. Its
> row 1 is `reach T1_VW_CAPMIN cells 6 -> 2 F101` (dead — F208); it carries
> `stroke weight T1_VW_WFRAC -> 0.48 … F102` (a row absent from this list) and F152's *"moves
> the WRONG WAY"* (which turned out to be rev 66's actual fix); and its F168 row publishes
> *"the photograph's 7 / 3.390"*, **both re-based**. Its §7b warning names F198/F200/F203 only.
> **Nothing in it mentions F208, F210, F211, F224 or F226.**

**WHAT IS IN THE TREE AT REV 68's CLOSE (unchanged by rev 68 — the nose took the revision):**
rev 63's six spine constants (`VW_V_TIP_X 0.3287`, `VW_APEX_Z 0.0538`, `VW_W_ARM_X 1.1002`,
`VW_W_ARM_Z 0.4350`, `VW_W_TROUGH_X 0.3111`, `VW_W_TROUGH_Z -0.6445`) — **UNCHANGED** — plus
rev 66's **ARC-CUT TERMINAL** (F202, ON by default, `T1_VW_NOARC=1` ablates it) and the NOSE's
stroke weight **`wfrac 0.2283`** (F204, was 0.1800).

**DO NOT re-try any of these. Every one is measured, not argued:**

```
reach            T1_VW_CAPMIN            cells 6 -> 2                       (F101)
                                         *** DEAD.  T1_VW_CAPMIN was a NO-OP
                                         from rev 66 to rev 68 (F208).  AS OF
                                         REV 68 IT REFUSES, exit 1.  Its figures
                                         are UNREPRODUCIBLE on a shipped tree ***
stroke weight    T1_VW_WFRAC alone       "moves the WRONG way against C8"   (F152)
                                         *** SUPERSEDED AT REV 66 AND SHIPPED
                                         AGAINST (F204).  AND ITS "C8's OLD
                                         target" CLAUSE IS FALSE -- C8's target
                                         was NEVER re-based (F226) ***
six-constant cell-count solve            7 cells only at residual 0.2498    (F103)
                                         *** its RESIDUAL half is void (F203);
                                         its "7 IS reached" half STANDS and
                                         REFUTES F200's unreachability leg (F209) ***
separate strokes                         rev 8 did it and got an X          (F113)
                                         *** graded MEASURED but its whole
                                         evidence is a GREP for a docstring ***
the V/W kink                             the PHOTOGRAPHS have the same kink (F138)
                                         *** its built-side angles appear in NO
                                         .py file and are unreproducible ***
terminal angles off the badges           residual 0.1800, WORSE than a bad
                                         control at 0.1167                  (F141)
                                         *** THE CONTROL NOW READS 0.2471, so
                                         0.1800 would score BETTER.  And e45
                                         MOVES with T1_VW_NOARC (-> 0.1306),
                                         so it is a MOVING BASELINE ***
the workshop badge's LANDMARKS           CEILED -- scale confound           (F153)
THE CANONICAL 2019 VECTOR as a TARGET    a DIFFERENT OBJECT                 (F168)
A REACH TERM as the discriminator        the trident touches in all SIX     (F179)
                                         *** RE-RUN AT REV 68 AND STANDS, and
                                         it is NOT a construction fact: under
                                         T1_VW_NOARC=1 it still reads six ***
"no spine can satisfy the cell shape"    REFUTED: 6.877 at 7 cells          (F174)
                                         *** scored entirely through
                                         probe_rev63_ablate.py, whose PHOTO_N=7
                                         is a hard search constraint (F226) ***
TRACING THE PRESSING AND MESHING IT      BUILT, RENDERED, WORSE.
                                         T1_VW_TRACED MUST STAY OFF        (F183)
TUNING AGAINST C6 OR C8 AS THEY STAND    their targets carry the viewing
                                         angle -- a pure shear spans both   (F184)
C8's 3.390 AS A TARGET AT ALL            un-squashed it is 2.63..2.96       (F194)
                                         *** THE RE-BASE NEVER HAPPENED IN THE
                                         INSTRUMENT.  C8's LIVE target is
                                         3.3896 and grep finds no 2.627 (F226) ***
SEARCHING THE MARK'S VERTICAL BY         renders as horizontal bars         (F195)
  MIRROR IoU
T1_VW_CAPMIN + T1_VW_PUREFIT             6 cells / 2.24.  TRIED, REFUTED    (F199)
                                         *** UNSAFE: CAPMIN contributes NOTHING
                                         (F208).  AND T1_VW_PUREFIT=1 ALONE
                                         used to CRASH every emblem probe; as
                                         of rev 68 it REFUSES, exit 3 ***
QUOTING C6's "0.6638 / 18.9 mm"          IT WAS A STRING LITERAL            (F198)
                                         *** FIXED AT REV 66 ***
CHASING C6 TO SEVEN CELLS                SEVEN IS THE PHOTOGRAPH'S RIM.
                                         The mark makes SIX and the build
                                         ALREADY MAKES SIX                  (F200)
                                         *** its "cannot make seven" leg is
                                         REFUTED by F209 ***
```

**THE LIST IS SEVENTEEN ROWS.** Counted at rev 68 by an adversary, and the rev-68 brief's
cross-references (row 1 = F101, row 15 = F199) are both right.

> **A REFUTATION INHERITS ITS INSTRUMENT (rule 46). Before you accept any row here, check what
> it was measured with — and CHECK THE REGISTER FOR THE FINDING BEFORE ACCEPTING ANYTHING AS
> NEW**, which is how F139 was found sitting under F200 (F209) and how F216 was found sitting
> under F221 (F222).

---
## §3 THE WORK LIST FOR REV 69

> **HIS TWO SENTENCES ARE STILL THE WORK.** *"I can't believe that we can't even accomplish a
> publicly available emblem, and we still have work to do on the shape of the nose."*

1. **THE BUMPER'S FLAT NOSE FACE — THE NOSE'S REAL, MEASURED DEFECT (F222). TOP ITEM.**
   The built front bumper is **flat to +0.05 mm** across its whole face; the photographed one
   is **curved at 11–14 σ**, projection-invariantly. This is *"the shape of the nose"* in the
   only sense the photographs can adjudicate, and it needs **no camera model at all**.
   * The flat run is eleven points at constant x in `t1_detail.bumper` under `# flat nose face`.
     Give it a real plan curve with a **named constant and an ablation switch**, exactly as
     `NOSE_BULGE` has one.
   * **GET THE NUMBER FROM THE LITERATURE FIRST — THE OWNER RULED IT IS PUBLISHED (F229).**
     Two pages by name: **`thesamba.com/vw/forum/viewtopic.php?p=9884153`** ("Split Bus — View
     topic — *Dimensions front mask VW T1*") and
     **`thesamba.com/vw/archives/info/split_bus_dimensions.php`** ("VW Split Bus Frame
     Dimensions"). Also `coolairvw.co.uk/guides/vw-bus-bumpers/`, and the fact a snippet did
     carry: **the 1959–67 deluxe bumper rubber insert is 8 ft = 2438 mm**, an ARC LENGTH which
     against a chord gives the sagitta via `arc = chord + 8h²/(3·chord)`.
     **⚠ EVERY ONE OF THOSE DOMAINS IS `EGRESS_BLOCKED` IN THE REV-68 CONTAINER** — WebFetch
     refuses and curl returns HTTP 000, `en.wikipedia.org` included. **TRY ANYWAY: the network
     policy is per-environment and may differ for you.** If it is still blocked, say so and
     use the route below.
   * **THE CAMERA-FREE ROUTE, WHICH NEEDS NOTHING FROM ANYBODY (F216/F223):** the symmetric
     hard points — `HL_Y 0.5450`, `IND_Y 0.6750`, the corners at |y| ≈ 0.875 — give the
     y-vanishing point from the frame itself, at sensitivity **`sin(az) = 0.80`, 4.1× the
     bumper-edge route**, needing no elevation and no camera solve. `ref_workshop.jpg` and
     `IMG_2073.jpeg` show both bores, both indicators and both corners unoccluded, and rule 11
     permits it. **This is the measurement this project should have made three revisions ago.**
   * **THEN RENDER, CROP AND LOOK — AND RENDER THE CONTROL TWICE (F228).**
2. **DO NOT FIT `NOSE_BULGE` TO 40 mm. THE INSTRUCTION WAS AIMED AT THE WRONG OBJECT (F222),
   AND NOTHING NOW EXCLUDES THE SHIPPED 19.6 (F223, B ∈ [16, 76]).** The owner's *"rounder
   than D"* still stands as a ruling on DIRECTION, and **F217 is CLEARED** — the fixtures
   follow the skin now, so a bulge change is no longer blocked by them. What binds is
   **`length`**: 0.045 gives `warn 4.073 vs 4.055`, and `dΔ/d(NOSE_BULGE) ≈ 0.72 m` (F227).
   **The SHIPPED form cannot fold at any B** — F218's "≈0.13" is about the REVERTED form.
3. **F205 — THE RENDER CUTS THREE INTERIOR CELLS WHERE THE PHOTOGRAPH CUTS SIX.** Photograph
   **6**; render **4 / 3 / 2** at ink thresholds 20 / 30 / 40. **THE EMBLEM'S TOP ITEM AND THE
   OWNER'S OWN SECOND SENTENCE.** **Not re-run at rev 68** — re-measure it on `out/r69_front.png`
   before you act. Read F210 first: the "mesh says 0.8400 R" half was never an independent
   observation.
4. **C4 IS THE EMBLEM'S LAST RED ROW — 0.0755 against a bar of 0.045.** **BUT F224 FIRST:
   `T1_VW_SOLVE=1` CANNOT MOVE `VW_W_ARM_X`** — the clip is `(0.05, 0.95)`, the shipped value
   1.1002, **zero admissible trials**. Widen the clip (and `_hi`/`_lo` for `T1_VW_CELLSOLVE`)
   to admit the shipped point and ADD A REACHABILITY ROW *before* running it. **Derive the
   bound from the construction — do NOT widen it to admit only the current value** (rule 44).
5. **F226 — RE-POINT OR REFUSE `PHOTO_E, PHOTO_N = 3.390, 7`** in `probe_rev63_ablate.py`,
   `probe_rev63_shapefit.py` and `probe_rev63_final.py`, and `probe_rev64_shear.py`'s S4.
   **And either wire F194's re-base into C8 or stop saying C8 was re-based.**
6. **F180 IS STALE — it says four ring contacts; `probe_rev63_reach.py` reports six.** And
   what moved four → six is **not** the arc cut (it reads six under `T1_VW_NOARC=1` too) and
   **not** the spine constants; the remaining candidate is **F204's stroke weight**.
7. **THE FIT DEPTH IS STILL UNMEASURED.** The glyph's extreme is fitted 20 % into the band
   (`1.0 - 0.8 * _BAND_FRAC`). **The answer is a MEASUREMENT, not a guess.**
8. **PUT AN ADVERSARY ON THIS BRIEF (rule 15), AND *DISPATCH* IT — POINT IT AT §2's REFUTED
   LIST AGAIN.** Fourteen at rev 64, thirteen at rev 67, twelve at rev 68. **Tell it to check
   the REGISTER for the finding before accepting that anything is new.**
9. **F156 — `flank_compare`'s `Senor` row scores a DELIBERATE DEPARTURE. EIGHT revisions.**
10. **TRIAGE `REMAINING_WORK_rev61.md` §I** — 27 rows, EIGHT revisions.
11. **THE SURVIVING PANEL ITEMS**, untouched for eight revisions: the glass is a flat slab
    (0.5 % sd against the photograph's 12.8 %); **the tyres have no tread, no sidewall
    lettering, and are 35 % too light**; the tail is a box where the real one is a barrel;
    every shut line is a 1-px ink stroke with no leading-edge highlight; the galley is
    monochrome; the counter is a floating slab.
12. **F143 — TWO LOUDSPEAKERS STAND ON THE ROOF AND ARE UNMODELLED.** 56 revisions.
13. **THE INHERITED CLUSTER** — F14 (**sixteen** revisions un-re-measured), F15, F10, F20.
14. **`delivery/READ_ME_FIRST.txt` LISTS THE MODEL'S KNOWN DEFECTS TO HIM.** It does not yet
    mention the rev-63 emblem change, F184, F194, F197, F200/F202/F204, F207, or **F222's flat
    bumper**.

**RANKING NOTE — AND THE RULE IT CARRIES IS NOT DROPPED.**
**RANK BY PIXELS OF THE DELIVERY FRAME** — `python3 visibility_budget.py 3840
out/r69_hero.png` — **and PASS IT A `.png`**, or it globs `out/` by mtime and reproduces F132.
Its ceiling: pixels are not visibility, so use it for ORDERS OF MAGNITUDE. **But he has
overridden the ranking three times, and the owner outranks it.**

---

## §4 WHAT WAS ASKED OF HIM — A CARRIER, NOT A LIST OF BLOCKERS

> **READ §0.1 FIRST.** At rev 54 he ruled the reference set on the repo is complete. This
> section is kept in full because rule 16 forbids dropping a carrier.

**`PHOTOS_WANTED_rev52.md` is the carrier for item 7 (ONE HUBCAP, SQUARE ON AND CLOSE).**
Items **1–5** keep their full text in `PHOTOS_WANTED_rev49.md`. **He has said 1–5 are not
possible now. DO NOT RE-ASK THEM.** Item 6 was **DISSOLVED at rev 51**.

**HIS SETTLED RULINGS — DO NOT RE-OPEN OR RE-ASK ANY OF THESE.** W6 makes colour his call;
the roof strips' 0.3 m retired; the wipers withdrawn entire; the lower bay SHUT; the RED bus
is the target and paint/artwork do not transfer between vehicles; the tail board IS on the
vehicle; the marks above the burst are STARS; `lid_rail`'s width *"narrow lip, ~as wide as it
is tall"*; the roughness trade *"ship 0.250"*; the stranded rev-57b branch *"merge it,
renumber its IDs"* — **DISCHARGED AT REV 64 (F188)**; the studio *"keep studio — ruling
stands"* (twice); the front arch *"leave it circular"*.

> **AND ONE LINE OF THAT LIST WAS NEVER HIS — CORRECTED BY ASKING HIM, AFTER REV 62.**
> It carried *"`playa_env.py` is not on the table — do not re-propose it"* from rev 52 to
> rev 64. **That entered as a brief's INFERENCE from W6, whose object is the studio RIG, and
> was applied to a SECOND DELIVERABLE — rule 34 exactly.** Put to him as multiple choice with
> both readings quoted, he ruled the Playa hero **"DEPRIORITISED, NOT CANCELLED"** — which is
> what his own rev-43 words said before that carrier was deleted at rev 44 (**F92**).
>
> **The correction sat on an UNMERGED BRANCH from rev 57 to rev 64 while every brief kept
> publishing the misattribution (F188).**
>
> **WHAT IT LICENSES: NOTHING TO DO NOW.** *"Focus on the 3d model"* stands, *"keep studio"*
> stands, **no revision works the Playa hero until he opens it**, and **nothing re-proposes
> `playa_env.py` as the delivery frame** — which is also why **F57** stays recorded rather
> than fixed. What changes is that it is a LIVE agreed second deliverable carried in the
> register, and that ***"the emotional bar that sits ABOVE clinical accuracy"*** is back in
> the record. **Do not re-ask it; do not act on it either.**
>
> ⚠ **AND REV 68 DROPPED THAT SENTENCE FROM THIS SECTION WHEN IT REWROTE THE BRIEF, AND
> `verify_clone.sh` CAUGHT IT** — `"the emotional bar is in BOTH live carriers"  got 1 want 2`.
> **Rule 16 firing on the file that carries rule 16.** Restored before the handoff shipped.
> **If you compact §4, that row is what stops you.**

**RULED AT REV 68 — NEW, BINDING, AND IT CHANGES WHERE MEASUREMENTS COME FROM.**
Asked as multiple choice with `probe_scratch/rev68_bumper_ask.png` attached — the photograph
with the bumper's top edge traced and its chord marked, beside a plan diagram of the model's
flat bumper and the instruction for taking the measurement — whether he could lay a straight
edge across the two front bumper corners and photograph the gap:

> ***"This has to be a commonly available measurement."***
> — **HE DID NOT ANSWER THE OPTION; HE REJECTED THE PREMISE, AND HE IS RIGHT.** A T1 bumper
> and front panel are catalogue pressings on one of the most documented vehicles ever built.
> **F229. THE STRAIGHT-EDGE ASK IS RETIRED — DO NOT RE-ASK IT**, and it is struck in
> `PHOTOS_WANTED_rev52.md`.
>
> **WHAT IT LICENSES, AND IT IS A STANDING METHOD CHANGE: before asking him for ANY
> measurement of a FACTORY PART, check the catalogue literature first.** Rule 11 already holds
> that a factory pressing is GEOMETRY and transfers between vehicles; **it follows that its
> dimensions are public.** §0.1's *"what we hold is what we get"* is about the PHOTOGRAPHS of
> THIS vehicle and was never a bar on the parts literature. **The sources are named in §3
> item 1 — and every one of them was `EGRESS_BLOCKED` in the rev-68 container.**

**RULED AT REV 67 — TWO ASKINGS, BOTH SPENT, AND THE SECOND ONE CHANGED THE METHOD.**

> ***"Rounder than D."*** — i.e. **rounder than the roundest panel offered.** **THIS CONFIRMS
> REV 51's FLAT NOSE and it is a RULING ON THE DIRECTION. F214.** *(The panel he judged was a
> build that FAILS VERIFY — `T1_NOSE_BULGE=0.055` gives "length 4.083 vs spec 4.055". He was
> told as soon as it was known.)*

> ***"I can't quite tell. Can you have an adversarial audit team attack this?"***
> — **AND HE WAS RIGHT ON BOTH COUNTS.** The figure was the defect, four ways (F215):
> mirrored panels that already matched, a pose 17.8° apart, a 26 % anisotropic stretch, and a
> ladder carrying **2 px** of signal across 70 → 135 mm.
> **STANDING METHOD CHANGE: when a figure put to him fails, DISPATCH ADVERSARIES AT IT RATHER
> THAN REDRAWING IT AND ASKING AGAIN.** **DO NOT ASK HIM THE NOSE AGAIN.**

**RULED AT REV 66 — BOTH BINDING:**

> ***"The W's outer arms sit too low"*** AND ***"The strokes still don't reach the ring."***
> — **BOTH, chosen together.** He did **NOT** re-report the strokes as too thin. The arms are
> **C4**, still red at 0.0755 with L4 the largest error at **+0.0634** — **and F224 now shows
> the prescribed solver cannot move that constant.** The reach is **F205**.
> **HIS REPEAT IS A MEASUREMENT. This is his SEVENTH report of this emblem.**

> ***The nose's shape — FIRST.*** **F197 IS A RULING, NOT AN INFERENCE.**

**RULED AT REV 65 — BOTH BINDING:**

> ***"I don't think the bus is ready yet. We need the bus to be ready before investing
> seriously in the render."*** — **HIS THIRD HOLD** (rev 58, 64, 65), VOLUNTEERED. The render
> when it comes is **MULTIPLE SIZES, MAX RESOLUTION, MAX FIDELITY, ALL IN ONE FOLDER. F193.**
> **CONSEQUENCE: F192's "prove the large-format chain" drops BELOW the model defects.**

> ***"we still have work to do on the shape of the nose."*** — **A SECOND DEFECT, AND IT IS
> NOT THE EMBLEM. F197.** *(And at rev 68 it acquired a measured, camera-free object: the
> BUMPER's flat plan face, F222.)*

**RULED AT REV 64 — BOTH STILL BINDING:**

> ***"Keep holding — fix the emblem first."*** — **F191. NO DELIVERY RENDER UNTIL HE SAYS SO.**

> ***"Bigger — large-format print."*** — **THE EXACT DIMENSION IS STILL OPEN.** **Do NOT
> re-ask it cold — ask once you have something to show him.** **3840 is not the target. F192.**
> *(And the rev-63/64 briefs' *"deliver.py shipped a set at 2400×1650"* is in no source file
> and no ledger. The premise was withdrawn in the asking. F189d.)*

**RULED AT REV 62, STILL BINDING:**

> ***"Bright silver, same as Tacombi."*** — **OVERRIDES SPEC §3's WEATHERED LOCK FOR THAT WORD
> ONLY.** `script_gen.SENOR_TARNISH = 0.0`; `T1_SENOR_TARNISH=1` restores it. **F157.**

> ***"It is going on different backgrounds for promotional material etc."*** **BUILT**:
> `T1_ALPHA=1` (**F159**) and `deliver.py` + `delivery/READ_ME_FIRST.txt` (**F160**).
> **It does NOT retire the rev-58 hold (F191).**

> ***"this is just the render to plug into company merch"*** — **HE DID NOT AUTHORISE THE
> BOUNCE CARD; "keep studio" stands.** **F155.**

**RULED AT REV 61:** ***"senor Tacombi should be clearer in the render than in that photo.
Well defined. I want this 3d model to look like new. Enhanced from the photo."*** **Live
tension with SPEC §3's WEATHERED lock — surface it, do not silently pick a side.**

**CARRIED FROM REV 53, AND STILL IN NO OTHER DOCUMENT:** a frame showing the cream **where it
IS chipped**. Rev 54 and 55 lowered its urgency — the band is 0.27 px at every shipped scale —
but it is **not struck**, and F19 covers the MODELLING of chipping, not the photograph request.

**AND HE VOLUNTEERED, STILL BINDING:** the emblem needs a fix, and **the full delivery render
waits until the model is right.**

**STILL WORTH HIS TIME AND NOT ASKED:** **F38** — the nose ring band at the top of its adopted
range; **F39/A3** — `Senor`'s ink deficit; and **the local bounce card**, a studio change under
a ruling he has given twice.

---
## §5 THE RULES — `CLAUDE.md` CARRIES THE METHOD, NOT THE NUMBERED CANON

The canon (rules 1–33) is printed in `NEXT_CONTEXT_PROMPT_rev50.md` §11. Rules 34–52 live only
in the briefs and are carried here — that is rule 16 firing on this file:

> **34. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Check which object a
> *"the record requires X"* sentence is about, and check the cited line exists. **F26 is still
> open. AND AT REV 68 THIS FIRED ON THE PROJECT'S OWN TOP ITEM: F221 measured the BUMPER and
> scored it against the SHELL (F222).**

> **35. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Ask the geometry, never the pose.

> **36. A GATE ONLY COUNTS FOR WHAT IT CAN SEE — ABLATE THE THING YOU ARE ABOUT TO TUNE,
> FIRST.**

> **37. AN ABSENT INPUT MUST NEVER READ AS A MEASUREMENT.** A probe that cannot run must say
> **"NO RENDER"** and exit non-zero. **REV 68: three more instances — C10's 9.9 sentinel,
> probe_rev46_vw's crash-instead-of-refuse, and P3 not running at all (F211/F225).**

> **38. TWO SIDES OF A RATIO MUST SHARE A RULER, AND IF THEY CANNOT, SAY SO IN THE ROW'S OWN
> NAME.**

> **39. A GATE'S TARGET IS AN INSTRUMENT TOO, AND MUST BE SWEPT LIKE ONE.**

> **40. WHEN AN OWNER RULING MAKES THE MODEL DEPART FROM THE REFERENCE, THE GATE THAT SCORES
> AGAINST THAT REFERENCE STOPS MEANING WHAT IT MEANT.** **F156, five revisions unacted.**

> **41. A GATE PASSING IS NOT EVIDENCE THE THING IS RIGHT. BUILD THE COUNTEREXAMPLE.**

> **42. A CONTROL'S KILL IS A PRECONDITION ON ITS PASS.**

> **43. A PHOTOGRAPH IS A PROJECTION, AND A DE-SQUASH IS NOT AN UN-PROJECTION.**

> **44. WHEN A GUARD GOES RED ON YOUR OWN NEW WORK, THE GUARD IS THE DEFAULT WINNER.**

> **45. A TARGET CAN BE UNREACHABLE, AND NOTHING INSIDE THE INSTRUMENT WILL SAY SO.**
> **⚠ CORRECTED AT REV 67 (F209): read it as a rule about GRADE DECAY AND UNREAD CARRIERS, not
> about discovery — `OPEN_FINDINGS.md` already carried F139 at grade `MEASURED-rev61`, five
> revisions before F200, and the "cannot ever produce" half is itself refuted.**

> **46. A REFUTATION INHERITS ITS INSTRUMENT.** *"Tried, refuted"* is only as good as the gate
> that scored it. **REV 68 ADDS: and as good as the OBJECT it scored. F141's "bad control at
> 0.1167" now reads 0.2471 and MOVES with an unrelated switch.**

> **47. AN ABLATION SWITCH CAN STOP ABLATING, AND SILENCE IS ITS FAILURE MODE.** **Ablate every
> switch you rely on and check the output ACTUALLY MOVED**, and when you remove what a switch
> acted on, retire the switch in the same edit. **DISCHARGED AT REV 68: `T1_VW_CAPMIN` now
> REFUSES rather than no-opping.**

> **48. AN ACCEPTANCE BAR EXPRESSED AS A FRACTION OF ITS OWN SPAN CANNOT REFUSE A LONG ENOUGH
> INPUT.** Re-cut as `max(4 px, 3 % of span)`, and that arithmetic is a verifier row.

> **49. NEW AT REV 68 — A DIFFERENCE WITH NO FLOOR UNDER IT IS NOT A MEASUREMENT.** Rev 68
> diffed a render before and after a change it had already PROVEN bit-identical, got **2.436 %
> of pixels moving by >8 levels**, and only found out what that meant by rendering the SAME
> TREE TWICE: the floor is **2.441 %**. **F217 published 2.54 % by that statistic as evidence
> its change moved the render.** Cycles here sets no seed and is not run-to-run deterministic.
> **Render the control twice. Publish the floor beside the difference. Quote worst-channel and
> LOCALISATION, not the percentage.** (F228.)

> **50. NEW AT REV 68 — A GREP IS NOT A REGRESSION TEST, AND IT FAILS IN BOTH DIRECTIONS.**
> `verify_clone.sh`'s `grep -c 'bulge = NOSE_BULGE \* w \* max'` sat in a block whose own
> comment says its rows *"are ARITHMETIC and BEHAVIOUR, not greps for a name"*. It **went red
> on a refactor that preserved every value it existed to protect**, and it would have stayed
> green on any change that kept the string. An adversary found **36–38 of `audit_adversary.py`'s
> 57 questions** are the same shape — including all four of rev 67's new ones — and **two of
> them assert states the register has REFUTED while printing `ok`.** **Anchor on arithmetic or
> behaviour; a grep can tell you a name is present and nothing else** (rule 10's shape, applied
> to the guards themselves).

> **51. NEW AT REV 68 — A MODULE-LEVEL `assert` IN A PROBE IS A GUARD THAT REPORTS NOTHING.**
> `probe_rev46_vw.py`'s `assert cur is not None` killed **at least four configurations** with a
> raw traceback and no summary line — and took `probe_rev63_reach.py`, `probe_rev63_ablate.py`
> and `probe_rev64_shear.py` down with it, because all three import it. **One of the four is
> `T1_VW_WFRAC=0.1800`, F204's OWN before-side: the revision that changed the stroke weight
> could not re-run its own ablation on the gate that scored it.** **Losing the landmarks is a
> RESULT — print it and exit non-zero** (rule 3 + rule 37).

> **52. NEW AT REV 68 — BEFORE ASKING THE OWNER TO MEASURE A PART, CHECK WHETHER THE PART IS IN
> THE CATALOGUE.** ***"This has to be a commonly available measurement."*** — his own words, on
> being asked to put a straight edge across a bumper that half a million were made of. Rule 11
> already holds that a factory pressing is GEOMETRY and transfers; **it follows that its
> dimensions are public.** §0.1's *"what we hold is what we get"* is about the PHOTOGRAPHS of
> THIS vehicle and was never a bar on the parts literature. (F229.)

---
## §6 THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build  T1_SUB=1 ~20 s     render 1600x1100 96 spp ~4.5-5.5 min PER VIEW
```

**`bpy` IS A PIP MODULE HERE**, so `python3 probe_rev46_vw.py` runs in ~1.1 s without the
Blender CLI. **Check whether a probe needs `blender -b -P` before you budget minutes for it.**

**AND NETWORK: WebSearch works; DIRECT PAGE FETCHES DO NOT.** At rev 68 every relevant domain
returned `EGRESS_BLOCKED` from WebFetch and HTTP **000** from curl, `en.wikipedia.org`
included. `curl -sS "$HTTPS_PROXY/__agentproxy/status"` reports the policy. **Try anyway — it
is per-environment — but do not budget a revision on it.**

> **AND A METHOD REV 66 PROVED.** The emblem's whole search was done in a **pure-2-D replica**
> with no `bpy`, validated on a KNOWN ANSWER first, while Blender had all four cores.
> **Prove the proxy on a known answer, then use it.**

```bash
./bootstrap.sh                                               # AND `pip install pillow`
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
./judge_set.sh r69                                           # the optics chain (F146)
python3 flank_compare.py out/r69_side.png /tmp/fc.png        # GATE 1
python3 gloss_compare.py out/r69_hero.png                    # GATE 3
python3 probe_rev59_nose.py out/r69_front.png                # READ BOTH RULERS
python3 probe_rev67_nose.py out/r69_front.png   # **PASS IT A FRAME** -- bare, P3 does
                                                # not run and SAYS SO (F225)
python3 probe_rev46_vw.py                    # THE EMBLEM GATE -- C4 is the only red row
python3 probe_rev64_shear.py ; python3 probe_rev65_unproject.py
python3 probe_rev63_trace.py ; python3 vw_pressing.py ; python3 probe_rev63_canon.py
python3 probe_rev63_ablate.py                # **PHOTO_N=7 IS A HARD SEARCH CONSTRAINT
                                             # AND 7 IS RETIRED -- F226.  Fix before use**
python3 probe_rev63_shapefit.py              # stale baseline AND the HUBCAP's weight (F178)
python3 probe_rev63_reach.py                 # contacts with the ring, and angles
python3 trace_outline.py ; python3 svgraster.py ; python3 senor_trace.py
python3 cream_rms.py                         # the LIVE photograph-side cream
python3 visibility_budget.py 3840 out/r69_hero.png   # PASS IT A .png -- F132/F189
T1_SUB=2 /tmp/blender/blender -b -P audit.py         # rewrites STATE.md -- COMMIT FIRST
python3 audit_brief.py ; python3 audit_adversary.py  # rules 15/17, MECHANICAL half only
```

**THE GATES THE ABLATIONS EXIST TO MAKE REFUSE:**

```bash
T1_SUB=1 T1_NOUNDER=1 /tmp/blender/blender -b -P probe_rev45_ground.py  # C5 must REFUSE
T1_SUB=1 T1_PG_PAINT=1 /tmp/blender/blender -b -P probe_rev45_ground.py # paints G4's window
python3 probe_rev59_door.py out/r69_side.png        # M3 fails BY DESIGN.  **SIDE FRAME**
python3 probe_rev61.py emblem --paint               # every mode paints its window
T1_NOSE_BULGE=0.045 T1_NOSE_FIXFOLLOW=0 T1_SUB=1 T1_VERIFY=1 \
  /tmp/blender/blender -b -P build.py               # NEW at rev 68: the fixture
                                                    # registration row MUST go red, 8 fail
T1_VW_NOARC=1 T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py  # rev 65's
                                                    # perpendicular cap, rebuildable (F202)
T1_VW_TRACED=1 T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py  # F183's refutation.
                                                    # IT MUST NOT SHIP
T1_VW_CAPMIN=1 python3 probe_rev46_vw.py            # must REFUSE, exit 1 (F208)
T1_VW_WFRAC=0.1800 python3 probe_rev46_vw.py        # must REFUSE with a summary line, exit 3
```

**ABLATION SWITCHES — all MEASUREMENT-ONLY:** **`T1_NOSE_FIXFOLLOW` (NEW at rev 68 — disables
the nose fixtures' skin-follow WITHOUT restoring old source; it is `verify.py`'s registration
row's kill, WATCHED FIRING at 8 fail. F217)**, `T1_NOSE_BULGE` (scales the nose's PLAN BULGE;
`probe_rev67_nose.py`'s M2 kill, WATCHED 19.6 → 6.2 mm. F207), `T1_VW_NOARC`, `T1_VW_TRACED`
(**REFUTED, F183; two verifier rows hold it OFF**), `T1_VW_WFRAC` (**F178: it overrides the
NOSE's weight, default now 0.2283, F204**), **`T1_VW_CAPMIN` (RETIRED — it REFUSES on a shipped
tree as of rev 68; still armed under `T1_VW_NOARC=1`. F208)**, `T1_VW_PUREFIT`,
`T1_VW_CELLSOLVE`, `T1_VW_DUMP`, `T1_VW_RES`, `T1_VW_WSWEEP`, `T1_VW_SOLVE` (**F224: it CANNOT
move `VW_W_ARM_X`**), `T1_VNOSE_DIV`, `T1_BULB_STR`, `T1_BULB_BASEV`, `T1_SENOR_BREAKS`,
`T1_SENOR_TARNISH`, `T1_ALPHA`, `T1_NOUNDER`, `T1_UNDER_ZBUG`, `T1_UNDER_PROUD`,
`T1_UNDER_VIS`, `T1_UNDER_YBUG`, `T1_UNDERSEAL`, `T1_VPOW`/`T1_VPOWZ` (**move them
TOGETHER**), `T1_VRISE`, `T1_DOOR_STALE`, `T1_NORIG`, `T1_RIG`, `T1_WORLD`, `T1_MOT_AMP`,
`T1_GL_WRGH`, `T1_BODY_RGH`, `T1_GC_ABSSPREAD`, `T1_GC_LOOSEMASK`, `T1_GL_TILES`,
`T1_PG_PAINT`, `T1_BAREMAT`, `T1_CLAY`, `T1_HL_BOWL`, `T1_HL_BEZEL`.

**FACTS ABOUT THIS MACHINE THAT BITE:**
* **`bootstrap.sh` FAILS 3 OF 10 ON A FRESH CLONE — PIL IS MISSING. `pip install pillow`.**
* **EVERY MEASUREMENT THROUGH `shader_solve._render` IS 8-BIT (F42)**, whatever
  `color_depth` says.
* **THE RENDER IS NOT RUN-TO-RUN DETERMINISTIC.** No Cycles seed is set. Floor at 1600×1100,
  96 spp: **2.441 % of pixels differ by >8 levels, worst channel 40.** **Render the control
  twice (F228, rule 49).**
* **`mottle_measure.py` names its output by `MOTTLE_AMP`**, so two runs differing only in
  `MOTTLE_M` **OVERWRITE EACH OTHER'S PNG**.
* **`probe_rev54_aov.py` and `probe_rev55_truenorm.py` write EXR into `probe_scratch/`** —
  delete them before committing and keep the PNGs.
* **`script_gen.py` IS NOT CALLED BY `build.py`.** Regenerate `tex/senor.png` by hand.
* **`lid_gen.py` is NOT called by `build.py`** either.
* **`vw_pressing.py`'s `trace()` is NOT called by `build.py`** — the outline is a committed
  literal and the selftest is what holds it to the photograph. That is deliberate.
* **`audit.py` rewrites `STATE.md`. COMMIT FIRST** — and regenerate it after ANY geometry
  change. **Rev 68's change moved it ONLY in provenance plus the new row's log lines**, which
  is itself the evidence the change was contained.
* **LAUNCH LONG RENDER QUEUES WITH `setsid`, NOT A BARE `nohup &`** — F173.
* **`ck` IN `verify_clone.sh` COLLAPSES WHITESPACE** — a two-field comparison separated by a
  space reads back as one token. Use `/` or another separator.

**THE DELIVERY CHAIN, WHICH IS NOT THE PREVIEW CHAIN:**
```bash
T1_SUB=2 /tmp/blender/blender -b -P hq_render.py    # ONE build, 10 bands, WITH MARGIN
python3 stitch.py out/hq_hero_raw.png ...           # CHECK ITS EXIT CODE -- 2 on a seam (F49)
python3 post.py out/hq_hero_raw.png out/hq_hero.png # optics LAST, never per strip
```

**THE DELIVERY FRAME — DO NOT RUN IT. He REAFFIRMED the hold at rev 64 (F191) and again at
rev 65 (F193). And he needs LARGE FORMAT, which this chain has never been proven at (F192).**

---
## §7 THE STANDARD, IN HIS WORDS

We are recreating a photorealistic version of **that exact bus**, and **any single measurement
off is unacceptable** — per-measurement, not on average. **Ground in the reference, build,
adversarially audit, iterate.** Never build before grounding. Never call it done off
self-review. Report the measurement **with its ceiling**, never a self-assigned score. Do not
say anything is ready — say what is fixed, what is still wrong, and what you measured.

**RENDER IT, CROP IT, AND LOOK AT IT, before and after every change.** Every defect this
project has shipped passed `VERIFY: 0 fail, 0 warn` and was found by looking at a crop.

**When you need something from him, ask as MULTIPLE CHOICE with the reference material
attached — one crop, one mark, one sentence — and ASK IT WITH THE QUESTION TOOL.**
**CHECK THE PREMISE FIRST: rev 64 came within one step of asking him a question built on a
figure that exists in no source file (F189d), and REV 68 ASKED HIM ONE WHOSE PREMISE HE
REJECTED OUTRIGHT (F229).**

---
## §8 THE OPEN-FINDINGS REGISTER — `OPEN_FINDINGS.md`

**IT IS A CARRIER (rule 16). Rows leave it only by being CLOSED with the measurement that
closed them, or RETIRED with the ruling that retired them. Never by being dropped.**

**Rev 68 added F222–F229**, of which **five are defects in this project's OWN instruments**,
one is an **owner ruling**, and one — **F222** — is the register catching itself for the second
revision running: **F216 already held the refutation of F221, one row above it, at the same
grade.** **Rev 68 also ANNOTATED F101, F196 and F199 with F208** — the rev-67 brief annotated
them in prose and the register, which §8 says outranks prose, went a whole revision without it.
Rev 67 added F207–F221; rev 66 added F200–F206; rev 65 F193–F199; rev 64 F183–F192.

**THE POINT OF THE FILE IS THE PROVENANCE GRADE, NOT THE LIST.** An `INHERITED` row is a
claim. **GRADE DECAY IS ITSELF A FINDING.** *(Vocabulary: MEASURED / RECOMPUTED / INHERITED /
RULED / CEILED / OBSERVED. **Do not widen it** — rule 44.)*

> **⚠ AND A GAP IN THE DECAY RULE, FOUND AT REV 68: all seventeen of §2's refuted rows carry
> `MEASURED-revN` and NONE has ever been downgraded.** The decay convention only bites on
> `INHERITED`, so an eight-revision-old `MEASURED-rev60` row that is now known false reads as
> strong evidence. **F101, F141, F152, F194 and F200 are all in that state.**

**STILL INHERITED AND OLDEST:** **F14** (`gal_end_f`'s sight lines, rev 52 — **SIXTEEN
revisions un-re-measured**), F15, F20, F10, and **F18** (the die-cut sticker, rev 44 — the
oldest live row and the project's original deliverable).

**AND `REMAINING_WORK_rev61.md` §I IS STILL NOT TRIAGED** — 27 rows, **eight revisions**.

---
## §9 THE HORIZON BEYOND REV 69

**CARRIER: re-rank it, do not rewrite it, and say what moved.**

**WHAT REV 68 LEARNED LAST, WHICH RE-RANKS THE REST.** **The brief's own top item was aimed at
the wrong object, and the register already said so one row above the finding it was built on.**
Twice in two revisions (F209, then F222). **Before you derive anything — READ THE REGISTER FOR
IT, AND OPEN THE SOURCE OF THE THING YOU ARE ABOUT TO CHANGE.**

**WHAT MOVED AT REV 68.** **F217 is CLEARED** — the nose fixtures follow the skin, with a
guard watched refusing, and the shipped build is unmoved bit-for-bit. **The nose's photographic
target was refuted and retargeted onto the BUMPER** (F222/F223). **Five more instruments were
found reporting things that are not measurements** (F224 the solver that cannot move its
constant, F225 the control that never ran, F226 the target never re-based, F227 the ceiling
about a reverted form, F228 the difference with no floor). **Three ablations that CRASHED now
REFUSE.** **What did NOT move: the bumper itself, `NOSE_BULGE`, C4, F205, and everything
outside the nose.**

**WHAT MOVED AT REV 67.** The nose got an instrument for the first time (F207); the frames were
found to carry their own EXIF (F219); and the register caught itself (F209).
**WHAT MOVED AT REV 66.** The emblem's stroke weight and the arc-cut terminal shipped; three
emblem instruments were found mis-targeted.
**WHAT MOVED AT REV 65.** The badge's ring was fitted as an ellipse; the reach was measured
live off the mesh.

| horizon | the work | why |
|---|---|---|
| **next** | **THE BUMPER'S FLAT NOSE FACE (§3 item 1, F222)** | **The nose's only MEASURED, CAMERA-FREE defect: built +0.05 mm against a photograph curved at 11–14 σ.** It is *"the shape of the nose"* in the sense the photographs can actually adjudicate |
| **next** | **THE NUMBER FOR IT — literature first (F229), then F216's camera-free route** | **The owner ruled it is publicly available and named no frame.** The two TheSamba URLs are in §3 item 1; the hard-point route needs nothing from anybody and is 4.1× more sensitive |
| **next** | **F205 — THE RENDER CUTS 3 CELLS WHERE THE PHOTOGRAPH CUTS 6 (§3 item 3)** | **The owner's own second sentence, and RED.** Not re-run at rev 68 — re-measure before acting |
| **next** | **C4 — but FIX THE SOLVER FIRST (§3 item 4, F224)** | **`T1_VW_SOLVE` cannot move `VW_W_ARM_X` at all.** Running it as-is is theatre |
| **next** | **F226's retired literals in three probes, and C8's un-re-based target** | §6 tells you to run a search whose objective is a number §2 says is refuted |
| **next** | **AN ADVERSARY, DISPATCHED, ON §2's REFUTED LIST** | Fourteen at rev 64, thirteen at rev 67, twelve at rev 68 |
| **near** | **F156 — the `Senor` gate row scores a DEPARTURE** | EIGHT revisions unacted |
| **near** | **F180's stale contact count, and the fit depth (§3 items 6, 7)** | |
| **near** | **Triage `REMAINING_WORK_rev61.md` §I** | 27 rows, eight revisions |
| **near** | **Glass, tyres, the tail's barrel, the shut lines** | Untouched for eight revisions |
| **near** | **F143 — the roof loudspeakers** | Unmodelled since rev 12 — 56 revisions |
| **LOWERED** | **F192 — prove the large-format chain** | **He ruled the MODEL comes first (F193).** |
| **then** | **F10–F14 — the galley cluster** | F14 is SIXTEEN revisions inherited |
| **CEILED** | **F153; F168; F183; F195; F44/F60/F62 gloss; F83; F67; F142; F148** | **F62 is DISPUTED — do not quote it without testing it** |
| **standing** | **F18 — the die-cut sticker** | The original deliverable. Open since rev 44 |

---
## §10 HOW TO GROW THIS HANDOFF WITHOUT BREAKING IT

1. **The set is three files.** `LEDGER_rev<N>.md`, `NEXT_CONTEXT_PROMPT_rev<N+1>.md`, and
   **`cp` of that file over `PASTE_INTO_CLAUDE_CODE.txt` IN THE SAME COMMIT.**
2. **`README.md` and `START_HERE.md` name the newest brief BY NUMBER.** Two rows check it.
3. **THE ROW COUNT IS SELF-REFERENTIAL AND AUTOMATED.** `python3 audit_brief.py
   --fix-count`. Write it LAST. *(It reads the CLEAN-TREE total.)*
4. **ADD ROWS ANCHORED ON ARITHMETIC OR BEHAVIOUR, NOT ON A GREP — AND RULE 50 NOW SAYS WHY IT
   FAILS IN BOTH DIRECTIONS.**
5. **RUN BOTH AUDITS AS SCRIPTS AND RECORD WHAT THEY FOUND *IN* THE BRIEF.** **REPLACE the
   adversary's questions each revision** — a question that can no longer fail is not a control.
   *(Rev 68 replaced four. The rev-63 batch is now the oldest and is next.)*
6. **NEVER DELETE A CARRIER.** §0, §0.1, §4, §5, §8 and §9 are carriers.
   **`EMBLEM_HANDOFF.md`, `PANEL_rev61.md` and `REMAINING_WORK_rev61.md` are carriers too.**
7. **RANK BEFORE YOU CHOOSE** — but **the owner outranks the ranking**.
8. **NEVER RELAX ONE COPY OF A CHECK.** Rev 68 re-based one row with the cause named and
   **five** companion rows, two of which are behavioural kills.
9. **DO NOT LET THE MACHINE IDLE.** Run `bootstrap.sh`, launch the render, then read.
10. **ROOM TO GROW:** new findings go in `OPEN_FINDINGS.md` with an ID and a grade.
