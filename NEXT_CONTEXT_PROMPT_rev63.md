# NEXT CONTEXT PROMPT — rev 63

## §0.0 DO THIS FIRST — THE WHOLE DECISION, IN TWENTY LINES

**Before you read another word, put the machine to work. It is CPU-bound and idle right now.**

```bash
cd /home/user/combi_render
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
nohup env T1_SUB=1 T1_PREVIEW=front,side,hero,hero34r T1_PFX=r63 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r63.log 2>&1 &
```

`out/` is untracked and **starts EMPTY**. **`bootstrap.sh` first**: at rev 58–62 `/tmp/blender/blender`
did not exist. Then start the render, then read.
**`grep -c Saved: /tmp/r63.log` must be 4** — a backgrounded runner's exit code is the redirect's.

**AND CHECK YOUR CLONE IS THE TIP.** Rev 62's clone arrived **SHALLOW (depth 50) AND EIGHTEEN
REVISIONS STALE** — HEAD at rev 43 while `origin/main` was at rev 61. `verify_clone.sh` passed
**65 of 66** on it, because a content check cannot detect that you are on an old commit of the
same repository. **Only `git fetch --unshallow` and the ahead/behind loop in §1 found it.** Run
§1 before you trust anything.

**THEN RUN `./judge_set.sh r63`.** `post.py` implements bloom → CA → vignette → grain, defaults
every gain to **0.0**, and the preview path **never calls it** (F146). Judge photorealism on the
`_post` set, never on the raw one.

**READ `LEDGER_rev62.md` §7 BEFORE YOU PLAN** — it is the list of what rev 62 did NOT do, said
plainly, and it is shorter than what it did.

---
## §0.05 THIS BRIEF WAS AUDITED AGAINST THE MACHINE — AND MORE WEAKLY THAN THE LAST ONE

**SAY THIS FIRST BECAUSE IT MATTERS MORE THAN ANYTHING ELSE IN THE SECTION: NO INDEPENDENT
ADVERSARY AGENT WAS RUN ON THIS DOCUMENT.** Rev 62's session was instructed not to spawn
subagents. Rules 15 and 17 were discharged by their **committed script halves** —
`audit_brief.py` and `audit_adversary.py` — plus the author's own pass. **That is the mechanical
half only.** Rev 61 ran a real adversary and it returned TWENTY findings, of which the author had
seen none. **Assume this brief carries defects of that class and put an agent on it first.**

**WHAT THE AUTHOR DID CATCH IN HIS OWN WORK, all of it by painting a window and looking:**

* **THE FIRST WORKSHOP MASK TOOK ONE FLANK OF EVERY STROKE.** The pressing is chrome lit from the
  right, so each stroke is a shadow flank beside a specular flank, and a level threshold eats one
  and drops the other. It produced six plausible landmark deltas — **L3 −0.3128, L2 −0.2554** —
  and **every one was an artefact**. That is F08's recorded failure mode arriving on a new
  statistic, in a project whose rule 8 exists for exactly this.
* **TWO OF THE AUTHOR'S OWN CONTROLS WERE WRONG.** `C2w` compared crop margins rather than badges
  and failed on a correct mask; `C3w` was aimed at the workshop **wall and floor** rather than the
  vehicle. Both repaired — `C2w` now agrees with F09's independently-fitted conic to **0.7 px**.
* **`C16` FAILED AND STOPPED A PUBLICATION.** The author had *"`Señor` is 43 mm out of place"*
  ready; the control showed the same offset on `Tacombi`, i.e. it is `flank_compare`'s own
  registration shift. **Withdrawn before it was written down.**
* **AN EDIT OF THE AUTHOR'S SHIPPED A MISLEADING FIGURE FOR ONE RUN.** `script_gen.py`'s
  *"tarnished luma"* line reads the tarnish weight; after the `Señor` ruling that array and the
  APPLIED array are no longer the same, and it printed **201.1** — a blend of the cleaned word and
  the still-tarnished zones, a plausible number describing no pixel set. Fixed to read the applied
  array.

**AND A HYPOTHESIS OF THE AUTHOR'S WAS REFUTED BY READING THE SOURCE**, which is worth as much:
C8's 3.39 is **not** inflated by the badge's foreshortening — `cell_elongation` already corrects
it with `squash = mask.shape[0]/mask.shape[1]`.

**`verify_clone.sh` WAS RUN ON THE ACTUAL HANDOFF COMMIT, not on the tree later.** ALL 275 PASS.

---
## §0.06 THE BIG ONE: C8's TARGET HAS A SILENT FAILURE MODE, AND NOTHING SWEEPS IT

**`cell_elongation()` measures inside an ellipse inscribed in THE MASK ARRAY'S RECTANGLE, not in
the badge** — `n0, n1 = mask.shape`. The shipped crop is tight, so it works. Widen it and the disc
escapes the roundel.

```
crop window            C8's photograph target
    +-0 px  (shipped)         3.390
    +-1 px                    3.188
    +-2 px                    2.950
    +-3 px                    1.553   <- the BUILT glyph reads 1.49
```

At ±3 px the cream nose **outside** the ring becomes a **479 px** "cream cell" against the true
cells' 215, **39 % of it outside the ring's own bounding box**. **At that window C8 reports the
owner's top defect CLOSED and no control fires.** C1 sweeps six thresholds × five windows for
L1–L6; **this target is swept by nothing.** That is now `probe_rev62_landmarks.py`'s C11 and C12.

**THE VERDICT SURVIVES; THE CEILING DOES NOT.** Within ±2 px the target reads 3.390 / 3.188 /
2.950 and the segmentation sweep gives **2.969 .. 3.415**. **The built glyph is 1.99× .. 2.27×
too round — a RANGE. Do not quote the point 2.27× again; four documents do.**

**AND THE SHIPPED PROBE CARRIES A STALE FIGURE.** `probe_rev46_vw.py`'s header says
*"photograph 3.33"* under a *"WATCHED, all of it"* banner. It prints **3.39**.

**THIS IS THE THIRD TARGET IN THIS ONE INSTRUMENT FAMILY FOUND CONTAMINATED OR MIS-RULED** —
C6's 7 (F139), M1's ruler (F136), and now C8's window. **Sweep the target before you trust a
gate here. It is not a coincidence; it is the pattern.**

---
## §0.07 THE MACHINE'S VERDICT AT CLOSE OF REV 62 — every one watched print

```
bootstrap.sh          ALL 10 PASS
verify_clone.sh       ALL 275 PASS on a clean tree, AT THE HANDOFF COMMIT
                      <- 0 FIDELITY, 275 SELF-CONSISTENCY.  THREE rows added this
                         revision: the T1_SENOR_TARNISH companion row and the two
                         that guard the T1_ALPHA delivery path
flank_compare.py      FAILS: worst region `i` 0.686 of its own ceiling
                      ink area ratio 1.0342 PASS (was 0.9766 -- the Senor ruling)
                      `Senor` 1488 px against 1261  <- 118 %, AND THAT IS DELIBERATE, see F156
probe_rev46_vw        9 checked, 2 FAILED -- C6 and C8
                      C8 photograph 3.39 (2.95..3.42 over its own window), built 1.49
probe_rev62_landmarks 9 checked, 2 FAIL BY DESIGN -- C11 and C14 ARE the findings
probe_rev62_senor     3 checked, 1 FAILED -- C16, and it stopped an over-claim
senor_trace.py        the `S` rasterises as 1 component, per the rev-61 ruling
STATE.md              UNCHANGED, and that is a CONTROL: rev 62 touched zero files
                      under t1_*.py / build.py / studio.py
```

**AND THE STANDING WARNING, WHICH `verify_clone.sh` PRINTS ITSELF.** A green check is not
evidence about the vehicle. **Not one of those 274 rows compares the model to a photograph.**

---
## §0. THE GOAL, AND HOW FAR OFF IT WE ACTUALLY ARE

**CARRIED FORWARD FROM THE REV-55…61 BRIEFS. It is not mine and it is not to be dropped —
rule 16.**

**PHOTO-REALISTIC PARITY WITH THAT EXACT BUS.** Not "a convincing VW bus" — *that one*, the red
Señor Tacombi combi in the frames on this repo. **Any single measurement off is unacceptable,
per-measurement and not on average.** A model right in ninety places and wrong in one is not
99 % done, because he will look straight at the one. **At rev 58 he did exactly that, at the
emblem, for the fifth time. At rev 61 he did it again, for the sixth.**

**AND HERE IS THE HONEST DISTANCE — THE GATE TABLE, WHICH AN ADVERSARY CAUGHT THIS BRIEF
DROPPING.** `verify_clone.sh` ends **ALL 275 PASS** and its own verdict block says what that is
worth: **0 FIDELITY, 275 SELF-CONSISTENCY.**

| gate | state MEASURED at close of rev 61 |
|---|---|
| `flank_compare.py` | **runs, FAILS.** Worst region **`i` at 0.687**; `Senor` **979 px of ink against 1261 (77.6 %)** at 0.721 of its ceiling. The deficit is the **artwork's alpha and its placement**, not the render (F39) |
| `gloss_compare.py` | **runs, FAILS at 0.426** (bar 0.60). The model-side lever is EXHAUSTED (F60/F62) — **but F62's ceiling is now DISPUTED on measurements, see §3 item 4** |
| `probe_rev46_vw.py` | **C6 AND C8 both FAIL.** C8: photograph 3.39, built 1.49, a plain cross 1.39 |
| `probe_rev59_nose.py` | **M1 PASSES lens-ruled — AND THAT IS NOT CLOSURE (F136).** Bezel-ruled 1.549 / 1.585 against a rim-ruled 1.951–2.121 |
| `mottle_measure.py` | **runs, and it is NOT measuring the mottle** — 1.1–2.0 % of it. Rev 56's reading and rev 57's item B are REFUTED |
| `probe_rev45_ground.py` | item D's gate, and `T1_NOUNDER`'s only consumer. **G4 0.3602 built / 0.5475 ablated / 0.057 photographed** |
| `probe_rev59_door.py` | item A's gate, and `T1_DOOR_STALE`'s. **8 checked, 1 FAILED (M3, BY DESIGN)** |
| `cream_rms.py` | `run()` is the LIVE photograph-side cream path |
| `visibility_budget.py` | the RANKING, not a gate — and **pass it the frame** (F132) |
| everything else | self-consistency |

**AND AT REV 61 HE ADDED A STANDARD.** *"I want this 3d model to look like new. Enhanced from
the photo."* That is not the same as WEATHERED, which SPEC §3 locks. **Where the two collide,
say so and put it to him** — do not silently pick one.

### §0.1 THE REFERENCE SET IS COMPLETE, AND IT IS GUARDED FRAME BY FRAME

> *[owner, rev 54]* **"we have all references that we need on repo and I want to make sure that
> is never forgotten."**

**ONE: WHAT WE HOLD IS WHAT WE GET. STOP PARKING WORK BEHIND A PHOTOGRAPH.** Where a frame
genuinely cannot answer, the result is *"it cannot be recovered from what we hold"* — a real
result, stated with its ceiling. **Rev 61 produced four**: the emblem's terminal angles at 40×68
and 93×63 px (F141); the roundel/lamp ratio, because the only lamp-off frame is the wrong livery
state (F140); the board's true edge softness (F150); and the red's true colorimetry, since no
frame carries a neutral chart.

**TWO: THEY CANNOT BE RE-SHOT, SO THEY ARE CHECKSUMMED INDIVIDUALLY.** 18 rows name them one at
a time:

* **the RED target bus** — `ref_side.jpg`, `ref_rear34.jpg`, `ref_playa_34.png`,
  `ref_nolita_front34.jpg`, `ref_nolita_front34b.jpg`, `ref_nolita_flank.jpg`,
  `ref_nolita_doorshut.jpg`
* **NOT the target, geometry only** — `ref_workshop.jpg` is the **GREEN** vehicle;
  **`IMG_2073.jpeg` is ALSO the GREEN vehicle**; `bus_model_ref.JPG` is a **SCHOOL BUS**, a
  fidelity bar only. **Paint and artwork do not transfer between vehicles; geometry does
  (rule 11)** — *and rev 61 found the useful corollary: the nose roundel's SHAPE is the factory
  chrome PRESSING, which is geometry and DOES transfer; only its colour is artwork (F141).*
* **AND RULE 11 APPLIES BETWEEN LIVERY STATES OF THE SAME VEHICLE**, which is what killed F99,
  F100 and F140: `ref_nolita_front34b.jpg` has a chalkboard lid and no folk art.
* **derived/annotated** — `ref_grid.png`, `ref_side_grid.png`, `ref_nose_grid.png`,
  `ref_band_grid.png`, `ref_x6_lanczos.png` *(the last is a 6× upsample of the RETIRED
  thumbnail — "interpolation, no new information", so it adds nothing)*
* **retired** — `ref_source.jpeg`, a 246×197 thumbnail the record itself retired
* a **floor of 54** reference-class tracked images, and **the five byte-identical pairs are
  asserted to stay five** — a sixth group means a frame arrived that duplicates one we hold,
  which is **not corroboration** and has fooled this project before.

**AND `ref_playa_34.png` IS UNDER-USED.** Rev 61's lookdev panel verified its white balance
**neutral** on the paving (116,119,120) and used it, not `ref_side.jpg`, as the frame to judge
paint against. `ref_side.jpg` and `ref_rear34.jpg` are both globally WARM.

---

## §1 START HERE — MEASURE THE BRANCH, DO NOT TRANSCRIBE IT

```bash
git fetch --all --prune
for b in $(git branch -r | grep -v HEAD); do
  printf "%-52s ahead %-3s behind %s\n" "$b" \
    "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"
done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
./bootstrap.sh          # read ROW 9, and read the "N ahead / M behind" NOTE line
./verify_clone.sh       # ALL 275 PASS -- and read its verdict block
```

**MEASURED AT REV 62 PICKUP:** HEAD was **0 ahead / 0 behind** `origin/main` after `git fetch --unshallow` -- **and BEFORE that fetch the clone was at rev 43, EIGHTEEN REVISIONS STALE, with `verify_clone.sh` passing 65 of 66 on it.** A content check cannot see that you are on an old commit of the same repository; only this loop can. **The rev-61 branch was NOT deleted this time, breaking a six-revision run.** The rev-62 figure that follows is the PREVIOUS revision's and is kept for the pattern:

**MEASURED AT REV 61 PICKUP:** HEAD was **0 ahead / 0 behind** `origin/main` — rev 59 and rev 60
were merged by PR #19, which the rev-61 brief did **not** know. **That is the eighth consecutive
revision whose prose guessed the merge state. Measure it.**

**AND MEASURE IT AGAIN BEFORE YOU FINISH.** `origin/main` moved mid-revision at rev 51 and
rev 55. **At rev 61's CLOSE, HEAD was 16+ ahead / 0 behind `origin/main`** — the pickup
figure above is NOT the close figure, and an adversary caught this section shipping only
the pickup one.

**AND THE ELEVENTH DELETION HAPPENED, ON SCHEDULE.** `fetch --prune` printed
`- [deleted] origin/claude/senor-tacombi-rev-61-99pz2u` — **this revision's own branch**, before
anything had been pushed to it, the SIXTH RUNNING. It was recreated by the first push.
**Expect it at rev 62.**

---

## §2 THE EMBLEM — HIS TOP ITEM, SIX REPORTS, AND REV 62 KILLED THE LEADING SUSPECT

**IT STILL READS AS AN X.** Confirmed at rev 62 by looking at `out/r62_front_post.png` — four fat
wedges meeting in a knot where the photograph has thin slivers. His sixth report stands.

**DO NOT re-try any of these. Every one is measured, not argued:**

```
reach            T1_VW_CAPMIN            cells 6 -> 2                     (F101)
stroke weight    T1_VW_WFRAC -> 0.48     cells 6 at EVERY value           (F102, and see below --
                                                                          that was against the COUNT)
six-constant cell-count solve            7 cells only at residual 0.2498  (F103)
separate strokes                         rev 8 did it and got an X        (F113)
the V/W kink                             the PHOTOGRAPHS have the same kink, OPPOSITE SIGN (F138)
the terminal angles off the badges       BUILT IT: residual 0.1800, WORSE than the
                                         deliberately-bad rev-45 control (0.1167)   (F141)
THE STROKE WEIGHT AGAINST C8             NEW AT REV 62 -- see below                 (F152)
THE WORKSHOP BADGE'S LANDMARKS           NEW AT REV 62 -- see below                 (F153)
```

### §2.1 L6 IS NOT THE ANSWER — REFUTED BY ABLATION (F152)

**F102 swept `T1_VW_WFRAC` and called it inert. THAT WAS AGAINST C6, THE CELL COUNT. C8 did not
exist until rev 61**, so the shipped lever for stroke weight had never been tested against the
statistic that measures the defect. Rule 36.

```
    wfrac    elongation   cells
    0.08        1.76        5
    0.10        1.82        5      <- the construction's limit
    0.12        1.49        6      (69-row reading 1.88 -- see the warning below)
    0.1986      1.49        6      <- SHIPPED
    0.28        1.45        6
    0.44        1.07        6
```

**It moves the WRONG WAY** — thicker strokes give rounder cells. **Thinning to the construction's
limit reaches 1.82 against 3.39 — 54 % of the way — and costs a cell.** So **abandoning the
stroke-width landmark ENTIRELY still cannot reach the target.** That extends F137: **the landmark
bar is not what is holding elongation down.**

**AND C8's ADVERTISED SCALE-STABILITY DOES NOT HOLD ACROSS THE SWEEP.** At wfrac 0.12 it reads
**1.49 at 276 rows against 1.88 at 69**. The stability is a property of the shipped point, not of
the statistic. **Do not quote "does NOT move with raster scale" as a general property again.**

### §2.2 THE WORKSHOP BADGE CANNOT DECIDE IT, AND L1 IS CORROBORATED (F153)

The rev-62 brief prescribed re-deriving L1–L6 on `ref_workshop.jpg`'s badge. Taken, with
`probe_rev46_vw.py`'s own `landmarks()` **lifted by `ast`** so the two rulers cannot drift (C0w
agrees to 0.00003).

```
              nolita   workshop     delta
    L1        0.1940     0.1957    +0.0016     <- CORROBORATED across two vehicles, 1.71x the area
    L2        0.3433     0.3261    -0.0172
    L3        0.4776     0.5109    +0.0333
    L4        0.8060     0.7609    -0.0451
    L5        0.2361     0.2685    +0.0324
    L6        0.1528     0.1204    -0.0324
```

**Resampling the workshop badge to the nolita badge's raster scale moves L6 0.1204 → 0.132 ±
0.013 — a third of the largest gap is the SCALE CONFOUND.** At matched scale no landmark clears
its combined spread by more than ~1.5 σ. **CEILED: it cannot be recovered from what we hold.**

**THIS IS THE SECOND ROUTE THIS FRAME HAS FAILED ON** — F141 was the first — **and the cause is
the same both times: the pressing is chrome, and chrome has no flat tone to threshold.** Before
proposing a third route through `ref_workshop.jpg`, say how it avoids that.

### §2.3 SO WHAT IS LEFT, AND IT IS A REAL QUESTION

F137: no spine arrangement satisfies both L1–L6 and the photograph's cell shape. F152: it is not
L6. F153: the second frame cannot arbitrate. **F139 already showed C6's target of 7 is
contaminated.** The live candidates, in the author's order and NOT measured:

1. **The incompatibility is in the CONSTRUCTION, not the landmarks.** `vw_bars` may not be able to
   make a sliver at any parameter — F137 reached 4.644 with the bar dropped, so the construction
   CAN; but that was six spine parameters, not the shipped topology. **Ablate the construction.**
2. **L2 — the merge landmark.** SPEC 10.110.8 already records that rev 44 set a SPINE constant to
   an OUTLINE measurement here and was wrong. It is the landmark with the known history.
3. **The photograph's cells are cut by TARNISH AND BLUR, not by strokes.** Nobody has tested
   whether the 41×69 raster's cell shapes survive its own PSF.

---
## §3 THE WORK LIST FOR REV 63

**RANK BY PIXELS OF THE DELIVERY FRAME** — `python3 visibility_budget.py 3840` — **and PASS IT THE
FRAME** (F132). Its ceiling: pixels are not visibility, so use it for ORDERS OF MAGNITUDE, not to
rank neighbours. **And the owner outranks it**, which he used at rev 58, 61 and again at 62.

**WHICH RANKING GOVERNS: THIS ONE.** `REMAINING_WORK_rev61.md` remains a CARRIER and its §I still
holds **27 untriaged rows** — rev 62 did not triage them either, which is two revisions running.
`PANEL_rev61.md` is a carrier too.

1. **PUT AN ADVERSARY ON THIS BRIEF FIRST (rule 15).** Rev 62 could not — see §0.05. This is the
   only item that is ranked first for a process reason and it is still the right call.
2. **`Señor`'s SIZE.** The finish is RULED AND SHIPPED (§4). The size is measured and NOT fixed:
   bbox **0.833 × 0.857** on the separable `S`, **but C16 showed part of that is global** —
   `Tacombi` reads 0.950 × 0.902 — so **separate the global from the word before touching either**.
   The weight half of the old diagnosis is **refuted**; do not thicken strokes.
3. **F156 — `flank_compare`'s `Senor` row now measures a DELIBERATE DEPARTURE.** Its ink went
   **973 → 1488 against a reference 1261** and its of-ceiling **0.717 → 0.751** by moving AWAY
   from the photograph. **A future revision reading that as convergence would be wrong, and one
   "fixing" the overshoot would be undoing an owner ruling.** Re-base the reference or annotate
   the row. Rev 62 did neither.
4. **THE EMBLEM — see §2.3.** Ablate the construction before proposing another landmark.
5. **TEST THE TWO DISPUTED CEILINGS** (specular-event census **0.024 % against 7.07 %**; the
   ground shadow). **Recorded, NOT adopted, and now MORE urgent:** F155 says the studio gets
   replaced, so a ceiling attributed to "the studio" may be attributed to a thing that is thrown
   away.
6. **ASK HIM ABOUT AN ALPHA CHANNEL.** F155: the render is *"to plug into company merch with
   different backgrounds"*. Nobody has asked whether he needs a cut-out. One line, and it changes
   the delivery chain.
7. **THE SURVIVING PANEL ITEMS**, none of which rev 61 or rev 62 touched: the glass is a flat slab
   (0.5 % sd against the photograph's 12.8 %); the tyres have no tread, no sidewall lettering, and
   are 35 % too light; the tail is modelled as a box where the real one is a barrel; every shut
   line is a 1-px ink stroke with no leading-edge highlight; the galley is monochrome; the counter
   is a floating slab with no fascia.
8. **F143 — TWO LOUDSPEAKERS STAND ON THE ROOF AND ARE UNMODELLED.** Known since `AUDIT_rev12.md`,
   in no live carrier for 50 revisions now, corroborated on two independent scenes.
9. **THE INHERITED CLUSTER** — F14 (**ten** revisions un-re-measured), F15, F10, F20.

---
## §4 WHAT WAS ASKED OF HIM — A CARRIER, NOT A LIST OF BLOCKERS

> **READ §0.1 FIRST.** At rev 54 he ruled the reference set on the repo is complete. This
> section is kept in full because rule 16 forbids dropping a carrier.

**`PHOTOS_WANTED_rev52.md` is the carrier for item 7 (ONE HUBCAP, SQUARE ON AND CLOSE).** Items
**1–5** keep their full text in `PHOTOS_WANTED_rev49.md`. **He has said 1–5 are not possible now.
DO NOT RE-ASK THEM.** Item 6 was **DISSOLVED at rev 51**.

**HIS SETTLED RULINGS — DO NOT RE-OPEN OR RE-ASK ANY OF THESE.** W6 makes colour his call; the
roof strips' 0.3 m retired; the wipers withdrawn entire; the lower bay SHUT; the RED bus is the
target and paint/artwork do not transfer between vehicles; the tail board IS on the vehicle; the
marks above the burst are STARS; `lid_rail`'s width *"narrow lip, ~as wide as it is tall"*; the
roughness trade *"ship 0.250"*; the stranded rev-57b branch *"merge it, renumber its IDs"*; the
studio *"keep studio — ruling stands"* (twice); the front arch *"leave it circular"*.
**`playa_env.py` is not on the table.**

**RULED AT REV 62, NEW, AND BOTH ARE BINDING:**

> ***"Bright silver, same as Tacombi."*** — the `Señor` word's finish. Asked with
> `probe_scratch/rev62_q_senor.png`, four options including *"match the photograph exactly"*.
> **This OVERRIDES SPEC §3's WEATHERED LOCK FOR THAT WORD ONLY** — the collision the rev-62 brief
> required be surfaced rather than silently decided. **SHIPPED** as
> `script_gen.SENOR_TARNISH = 0.0`; luma **117.1 → 201.1**. The b flag, i dot and swash keep their
> tarnish. `T1_SENOR_TARNISH=1` restores the pre-ruling texture **byte for byte**. See **F157**.

> ***"this is just the render to plug into company merch with different backgrounds once i
> determine the model is done"*** — his answer when asked to rule on the local bounce card.
> **HE DID NOT AUTHORISE THE CARD; the "keep studio" ruling stands and he has now given its
> rationale.** The consequences are in **F155** and they are not small: the white backdrop is
> **scaffolding**, the model will be composited on backgrounds nobody has chosen, a clean matte
> matters, and **the gate is HIM determining the model is done**. **NOBODY HAS ASKED HIM WHETHER
> HE NEEDS AN ALPHA CHANNEL** — see §3 item 6.

**RULED AT REV 61:** ***"senor Tacombi should be clearer in the render than in that photo.
Well defined. I want this 3d model to look like new. Enhanced from the photo."*** That closed
`senor_trace.py`'s standing owner-decision. **It also creates a live tension with SPEC §3's
WEATHERED lock — surface it, do not silently pick a side.**

**CARRIED FROM REV 53, AND STILL IN NO OTHER DOCUMENT — an adversary caught rev 62's first
draft dropping it, which is the mechanism that lost the die-cut sticker at rev 44 and the
findings register at rev 45:** a frame showing the cream **where it IS chipped**. Rev 54 and
rev 55 both lowered its urgency — the band is 0.27 px at every scale this project ships, and
the gate that would place those chips is not built — but it is **not struck**, and F19 covers
the MODELLING of chipping, not the photograph request.

**AND HE VOLUNTEERED, STILL BINDING:** the emblem needs a fix, and **the full delivery render
waits until the model is right.**

**STILL WORTH HIS TIME AND NOT ASKED:** **F38** — the nose ring band at the top of its adopted
range, which interacts with the emblem; **F39/A3** — `Senor`'s ink deficit, now measured well
enough to ask; and **the local bounce card** the photography and lookdev panels BOTH proposed
independently, which would light the chrome without the achromatic fill that `T1_WORLD` dumps on
the paint (F148). **That last one is a studio change under a ruling he has given twice — it is
his call and rev 61 deliberately did not make it.**

---

## §5 THE RULES — `CLAUDE.md` CARRIES THE METHOD, NOT THE NUMBERED CANON

The canon (rules 1–33) is printed in `NEXT_CONTEXT_PROMPT_rev50.md` §11. Rules 34–37 live only
in the briefs and are carried here — that is rule 16 firing on this file:

> **34. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Check which object a
> *"the record requires X"* sentence is about, and check the cited line exists. **F26 is still
> open**: `flank_compare.py`'s header attributes a camera to `ref_side.jpg` that `studio.py`
> attributes to the PLAYA frame.

> **35. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Ask the geometry, never the pose it
> happens to be in. **Rev 61 earned this twice**: the emblem's ring-crossing angles are not
> terminal angles, and F149's tail-lamp "defect" is a circle on a corner rounding.

> **36. A GATE ONLY COUNTS FOR WHAT IT CAN SEE — ABLATE THE THING YOU ARE ABOUT TO TUNE, FIRST.**
> **Rev 61 earned this NINE times in one revision — see `LEDGER_rev61.md` §4.** Four of the nine
> came from an expert panel. `T1_MOT_AMP` at **0.00** — the texture GONE — moves its statistic by
> 0.1 %.

> **37. AN ABSENT INPUT MUST NEVER READ AS A MEASUREMENT.** A probe that cannot run must say
> **"NO RENDER"** and exit non-zero. **Rev 61 adds a sibling: AN INSTRUMENT THAT SATURATES ITS
> OWN SEARCH WINDOW MUST NOT PUBLISH.** ONE of rev 61's did, on TWO frames, and its two outputs (134 mm / 81 mm)
> are recorded in F150 as artefacts, not figures.

> **39. NEW AT REV 62 — A GATE'S TARGET IS AN INSTRUMENT TOO, AND MUST BE SWEPT LIKE ONE.**
> C1 sweeps six thresholds × five windows for L1–L6. C8's photograph target -- the whole basis for
> the owner's top defect -- was swept by NOTHING, and it collapses from 3.39 to 1.553 on a 3 px
> crop change because `cell_elongation`'s disc is inscribed in the CROP, not the badge. **Three
> targets in one instrument family have now been found contaminated or mis-ruled: C6's 7 (F139),
> M1's ruler (F136), C8's window (F151).** Sweep the target, not only the measurement.

> **40. NEW AT REV 62 — WHEN AN OWNER RULING MAKES THE MODEL DEPART FROM THE REFERENCE, THE GATE
> THAT SCORES AGAINST THAT REFERENCE STOPS MEANING WHAT IT MEANT.** `flank_compare`'s `Senor` row
> IMPROVED (0.717 → 0.751 of ceiling) by moving AWAY from the photograph. Re-base it or annotate
> it in the same revision as the ruling, or the next context reads the improvement as convergence
> and the one after that "fixes" the overshoot and undoes the ruling. **F156, and rev 62 did
> NOT do it.**

> **38. NEW AT REV 61 — TWO SIDES OF A RATIO MUST SHARE A RULER, AND IF THEY CANNOT, SAY SO IN
> THE ROW'S OWN NAME.** M1 compared a LENS-ruled render figure to a RIM-ruled photographed bar
> for two revisions and its PASS was quoted as closure for one commit. F75 had already recorded
> that the 1.19 conversion **cannot be checked**. The row is renamed so its PASS cannot be
> misread (F136).

---

## §6 THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build  T1_SUB=1 ~20 s     render 1600x1100 96 spp ~4.5-5.5 min PER VIEW
```

**AND THE MOST USEFUL THING REV 61 LEARNED ABOUT THIS MACHINE:** `bpy` is a pip module here, so
**`python3 probe_rev46_vw.py` runs in 0.84 s** without the Blender CLI. That is what made an
8,174-candidate emblem solve possible. **Check whether a probe needs `blender -b -P` at all
before you budget minutes for it.**

```bash
./bootstrap.sh                                               # THE TOOLCHAIN IS NOT ON THE CLONE
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=front,side,hero,hero34r T1_PFX=r62 ... build.py   # ALL FOUR views, ONE build
./judge_set.sh r62                                           # NEW -- the optics chain (F146)
python3 flank_compare.py out/r62_side.png /tmp/fc.png        # GATE 1
python3 gloss_compare.py out/r62_hero.png                    # GATE 3
python3 probe_rev59_nose.py out/r62_front.png                # ITEM B -- READ BOTH RULERS
T1_SUB=1 /tmp/blender/blender -b -P probe_rev46_vw.py        # ITEM C -- C6 and C8 both FAIL
T1_SUB=1 T1_VW_DUMP=1 ... probe_rev46_vw.py                  # PAINT the cells.  LOOK.
python3 senor_trace.py                                       # the `S` connectivity guard
python3 cream_rms.py                                         # the LIVE photograph-side cream
python3 visibility_budget.py 3840                            # THE RANKING -- pass it the FRAME
T1_SUB=2 /tmp/blender/blender -b -P audit.py                 # rewrites STATE.md -- COMMIT FIRST
python3 audit_brief.py ; python3 audit_adversary.py          # rules 15 and 17, MECHANICAL half
```

**ABLATIONS NEW AT REV 61 — all MEASUREMENT-ONLY, all shipped values are the literals:**
**`T1_VNOSE_DIV`** (the `u = |y| / 0.860` divisor — **NOT inert**, see §0.06),
**`T1_BULB_STR`** / **`T1_BULB_BASEV`** (both REFUTED as fixes, F144),
**`T1_SENOR_BREAKS`** (restores the tarnish-faithful broken `S`; the connectivity guard must read
3 instead of 1).
**NEW AT REV 62: `T1_SENOR_TARNISH`** (restores the pre-ruling tarnish on the `Señor` word;
the shipped value 0.0 is the owner's ruling, and `=1` reproduces the old `tex/senor.png` BYTE FOR
BYTE -- a `verify_clone.sh` row asserts it).
**CARRIED:** `T1_NOUNDER`, `T1_UNDER_ZBUG`, `T1_UNDER_PROUD`, `T1_UNDER_VIS`, `T1_UNDER_YBUG`,
`T1_UNDERSEAL`, `T1_VPOW`/`T1_VPOWZ` (**move them TOGETHER**), `T1_VRISE`, `T1_VW_CAPMIN`,
`T1_VW_PUREFIT`, `T1_VW_WFRAC`, `T1_VW_CELLSOLVE`, `T1_VW_DUMP`, `T1_VW_RES`, `T1_VW_WSWEEP`,
`T1_DOOR_STALE`, `T1_NORIG`, `T1_RIG`, `T1_WORLD`, `T1_MOT_AMP`, `T1_GL_WRGH`, `T1_BODY_RGH`,
`T1_GC_ABSSPREAD`, `T1_GC_LOOSEMASK`, `T1_GL_TILES`, `T1_PG_PAINT`, `T1_BAREMAT`, `T1_CLAY`.

**THE GATES THE ABLATIONS EXIST TO MAKE REFUSE — an adversary caught this brief listing the
switches without the gates, which is rule 3 with its second half deleted:**

```bash
T1_SUB=1 T1_NOUNDER=1 /tmp/blender/blender -b -P probe_rev45_ground.py  # C5 must REFUSE
T1_SUB=1 T1_PG_PAINT=1 ... probe_rev45_ground.py    # paints G4's window -- LOOK before quoting
python3 probe_rev59_door.py out/r62_side.png        # ITEM A.  M3 fails BY DESIGN
T1_SUB=1 T1_MM_ALBEDO=1 T1_MM_SAMP=16 ... mottle_measure.py             # GATE 2
python3 probe_rev61.py emblem|blotch|world|bulb [--paint]   # NEW at rev 61 -- see below
```

**`probe_rev61.py` IS NEW AND IT EXISTS BECAUSE AN ADVERSARY FOUND FOUR HEADLINE REV-61 RESULTS
RESTING ON UNCOMMITTED INSTRUMENTS.** It carries the emblem solve, the cream blotch, the
`T1_WORLD` trade and the bulb ratio, and **every mode paints its window on `--paint`**.

**FACTS ABOUT THIS MACHINE THAT BITE, AND WHICH THIS BRIEF NEARLY DROPPED:**
* **EVERY MEASUREMENT THROUGH `shader_solve._render` IS 8-BIT (F42)**, whatever `color_depth` says.
* **`mottle_measure.py` names its output by `MOTTLE_AMP`**, so two runs differing only in
  `MOTTLE_M` **OVERWRITE EACH OTHER'S PNG**.
* **`probe_rev54_aov.py` and `probe_rev55_truenorm.py` write EXR into `probe_scratch/`** — delete
  them before committing and keep the PNGs.
* **`script_gen.py` IS NOT CALLED BY `build.py` EITHER, and this file named only `lid_gen.py` for
  nineteen revisions.** Change it and regenerate `tex/senor.png` by hand, or the render silently
  uses the old texture. `tex/senor.png` is CHECKSUMMED, so a forgotten regeneration is caught --
  but only after you have rendered and measured a stale frame.
* **`lid_gen.py` is NOT called by `build.py`.** Change it and regenerate by hand, or the render
  silently uses the old texture.
* **`audit.py` rewrites `STATE.md`. COMMIT FIRST** — and regenerate it after ANY geometry change.
  **Rev 61 shipped a stale `STATE.md` and an adversary caught it**: `V_POW_Z` is the pressed
  swage, i.e. geometry, and 19 verify rows read that file.

**THE DELIVERY CHAIN, WHICH IS NOT THE PREVIEW CHAIN:**
```bash
T1_SUB=2 /tmp/blender/blender -b -P hq_render.py    # ONE build, 10 bands, WITH MARGIN
python3 stitch.py out/hq_hero_raw.png ...           # CHECK ITS EXIT CODE -- 2 on a seam (F49)
python3 post.py out/hq_hero_raw.png out/hq_hero.png # optics LAST, never per strip
```

**THE DELIVERY FRAME — DO NOT RUN IT UNTIL THE MODEL IS RIGHT (owner, rev 58, STILL BINDING).**

---

## §7 THE STANDARD, IN HIS WORDS

We are recreating a photorealistic version of **that exact bus**, and **any single measurement
off is unacceptable** — per-measurement, not on average. **Ground in the reference, build,
adversarially audit, iterate.** Never build before grounding. Never call it done off
self-review. Report the measurement **with its ceiling**, never a self-assigned score. Do not
say anything is ready — say what is fixed, what is still wrong, and what you measured.

**RENDER IT, CROP IT, AND LOOK AT IT, before and after every change.** Every defect this project
has shipped passed `VERIFY: 0 fail, 0 warn` and was found by looking at a crop. **At rev 61 the
emblem's cause, the roof's loudspeakers, and eleven wrong measurement windows and instruments were all found
that way, and none by reasoning.**

**When you need something from him, ask as MULTIPLE CHOICE with the reference material attached
— one crop, one mark, one sentence — and ASK IT WITH THE QUESTION TOOL.**

---

## §8 THE OPEN-FINDINGS REGISTER — `OPEN_FINDINGS.md`

**IT IS A CARRIER (rule 16). Rows leave it only by being CLOSED with the measurement that closed
them, or RETIRED with the ruling that retired them. Never by being dropped.**

It carries **157 rows** now. **Rev 62 added F151–F157**, of which **three are refutations** --
one of the rev-62 brief's own diagnosis (F154), one of its leading emblem suspect (F152), and one
of a route it prescribed (F153). **Two are owner rulings** (F155, F157) and **one is a trap laid
for the next context by an owner ruling** (F156).

**Rev 61 added F134–F150**, of which **seven are retractions or refutations**, three of them of
rev 61's own published claims.

**THE POINT OF THE FILE IS THE PROVENANCE GRADE, NOT THE LIST.** An `INHERITED` row is a claim.
**GRADE DECAY IS ITSELF A FINDING.**

**STILL INHERITED AND OLDEST:** **F14** (`gal_end_f`'s sight lines, **rev 52 — TEN revisions
un-re-measured**), F15, F20, F10, and **F18** (the die-cut sticker, rev 44 — the oldest live row
and the project's original deliverable).

**AND `REMAINING_WORK_rev61.md` §I IS STILL NOT TRIAGED.** It carries 27 rows that were in no
other document. **Rev 61 proved that section's worth: F77 was sitting in it, it was RIGHT, and
the deficit it named was hidden behind a broken gate for two revisions.** Triage the rest.

---

## §9 THE HORIZON BEYOND REV 63

**CARRIER: re-rank it, do not rewrite it, and say what moved.**

**WHAT MOVED AT REV 62.** The emblem's leading suspect (L6) was **killed by ablation** and the
second badge frame was **ceiled**; C8's target was found to have a **silent failure mode** and its
verdict narrowed from a point to a **range**; `Señor` got an **owner ruling, shipped**, and its
brief-published diagnosis was found **half wrong**; and the owner said **what the render is for**,
which retires the bounce card and re-frames every studio ceiling. **What did NOT move: any
geometry at all.**

**WHAT MOVED AT REV 61.** The nose's gate was **fixed** and its remedy family **un-refuted**;
the emblem's search space was **closed** with a number; `Señor` got its **owner ruling** and is
still not delivered; the roof half of **F91 is done**; and an expert panel put **83/240** on the
board with two of this project's ceilings **disputed on measurements**.

| horizon | the work | why |
|---|---|---|
| **next** | **AN ADVERSARY ON THIS BRIEF** | Rev 62 shipped without one — §0.05. Nothing else is first |
| **next** | **THE EMBLEM — ABLATE THE CONSTRUCTION** | Rev 62 killed L6 and ceiled the second frame. §2.3 names what is left |
| **next** | **`Señor`'s SIZE — the weight half is REFUTED** | The FINISH is ruled and shipped (F157). The size is measured and part of it is GLOBAL (F154/C16) |
| **next** | **F156 — the `Senor` gate row now scores a DELIBERATE DEPARTURE** | It improved by moving away from the photograph. Re-base or annotate it |
| **near** | **Test the two disputed ceilings** | If the photography panel is right, a large part of what is ceiled to the studio is not the studio |
| **near** | **Glass, tyres, the tail's barrel, the shut lines** | The surviving panel items, none touched |
| **near** | **F143 — the roof loudspeakers** | Unmodelled since rev 12, in no carrier for 49 revisions |
| **then** | **F10–F14 — the galley cluster** | F14 is NINE revisions inherited |
| **CEILED** | **F153 — the workshop badge's landmarks; F44/F60/F62 gloss; F83 the front arch; F67's residue; F142's roof colour; F148's dark chrome** | **But F62 is now DISPUTED — see §3 item 4. Do not quote it without testing it** |
| **standing** | **F18 — the die-cut sticker** | The original deliverable. Open since rev 44 |

---

## §10 HOW TO GROW THIS HANDOFF WITHOUT BREAKING IT

1. **The set is three files.** `LEDGER_rev<N>.md`, `NEXT_CONTEXT_PROMPT_rev<N+1>.md`, and **`cp`
   of that file over `PASTE_INTO_CLAUDE_CODE.txt` IN THE SAME COMMIT.**
2. **`README.md` and `START_HERE.md` name the newest brief BY NUMBER.** Two rows check it.
3. **THE ROW COUNT IS SELF-REFERENTIAL AND AUTOMATED.** `python3 audit_brief.py --fix-count`.
   Write it LAST.
4. **ADD ROWS ANCHORED ON ARITHMETIC OR BEHAVIOUR, NOT ON A GREP.**
5. **RUN BOTH AUDITS AS SCRIPTS AND RECORD WHAT THEY FOUND *IN* THE BRIEF.** **REPLACE the
   adversary's questions each revision** — a question that can no longer fail is not a control.
6. **NEVER DELETE A CARRIER.** §0, §0.1, §4, §5, §8 and §9 are carriers. **`PANEL_rev61.md` and
   `REMAINING_WORK_rev61.md` are carriers too.**
7. **RANK BEFORE YOU CHOOSE** — but **the owner outranks the ranking**, and at rev 58 and again
   at rev 61 he used that.
8. **NEVER RELAX ONE COPY OF A CHECK.** Rev 61 moved three `V_POW` rows together.
9. **DO NOT LET THE MACHINE IDLE.** Run `bootstrap.sh`, launch the render, then read.
10. **ROOM TO GROW:** new findings go in `OPEN_FINDINGS.md` with an ID and a grade.
