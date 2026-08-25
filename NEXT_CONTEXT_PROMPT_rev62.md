# NEXT CONTEXT PROMPT — rev 62

## §0.0 DO THIS FIRST — THE WHOLE DECISION, IN TWENTY LINES

**Before you read another word, put the machine to work. It is CPU-bound and idle right now.**

```bash
cd /home/user/combi_render
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
nohup env T1_SUB=1 T1_PREVIEW=front,side,hero,hero34r T1_PFX=r62 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r62.log 2>&1 &
```

`out/` is untracked and **starts EMPTY**. **`bootstrap.sh` first**: at rev 58, 59, 60 AND 61
`/tmp/blender/blender` did not exist. Then start the render, then read.
**`grep -c Saved: /tmp/r62.log` must be 4** — a backgrounded runner's exit code is the redirect's.

**THEN RUN `./judge_set.sh r62`.** New at rev 61 and it matters: `post.py` implements
bloom → CA → vignette → grain, defaults every gain to **0.0**, and the preview path **never
called it**, so *sixty revisions of fidelity judgement were made on raw frames* (F146). Judge
photorealism on the `_post` set, never on the raw one.

**READ `LEDGER_rev61.md` §4 BEFORE YOU PROPOSE ANY FIX.** It lists **NINE proposals killed by
ablation at rev 61**, four of them from the expert panel the owner commissioned. If your idea is
on that list it is already dead and the measurement is there.

---

## §0.05 THIS BRIEF WAS AUDITED AGAINST THE MACHINE, AND SO WAS THE LAST ONE

**Rule 15/17.** An independent adversary was put on the OUTGOING document, not only the incoming
one. What it found is recorded in §0.07 below rather than quietly fixed.

**AND REV 61 RETRACTED THREE OF ITS OWN PUBLISHED CLAIMS.** *"M1 PASSES — item B is fixed"*
(a ruler mismatch, F136); *"the 0.860 divisor is dead"* (the gate was blind, F134); and a source
comment "correcting" `senor_trace.py`'s prose that was itself wrong. **Budget for this. Rev 61
threw away ELEVEN painted measurement windows, every one of which produced a plausible number
first** — including one that landed on **a child's hair** and one that read the **ride drop** as
a 70 mm defect. That is rule 4, and it is normal here.

---

## §0.06 THE BIG ONE: A GATE WAS MEASURING THE WRONG OBJECT FOR TWO REVISIONS

**`probe_rev59_nose.py`'s M1 was reading the headlamp's CHROME BEZEL, not the two-tone break.**
Its walk was `v = int(v0) - 2; while not cream[v, ucol]: v -= 1`. `v0` is the top of the LENS
blob — segmented as dark AND unsaturated — but the bezel above it is **bright** and unsaturated,
so `cream` is TRUE on it and the walk stopped there every time. The bezel's top is at a fixed
offset from the lamp centre, so M1 returned ~1.18 **whatever the paint did**.

```
render                 M1 said     TRUE break
V_POW 0.60 (was)         1.183       1.789
V_POW 0.15               1.186       3.800
T1_VNOSE_DIV 0.600       1.184       3.788
```

**THEREFORE F106 AND F107 ARE RETRACTED.** `V_POW`, `V_POW_Z`, `V_RISE` and the 0.860 divisor
are **NOT inert** — the instrument was blind to them. **Any sentence in an older document saying
"the whole remedy programme is refuted" is wrong.**

**`V_POW = V_POW_Z = 0.52` NOW SHIPS**, and the three by-value rows in `verify_clone.sh` moved
with it (§10.8: never relax one copy). The value is **F77's**, which had been orphaned in
`REMAINING_WORK_rev61.md` §I — the section that brief admits is *"in NEITHER outgoing
document"*. F77 fits the exponent POSE-INVARIANTLY with a validated control (recovers a source
truth of 0.600 as 0.605/0.620, ±0.02) on three frames reading 0.517 / 0.521 / 0.531.
**Measured effect +24 mm at the lamp, against F77's predicted +24.5.**

**ITEM B IS IMPROVED BY 24 mm, NOT CLOSED — AND M1's PASS IS NOT EVIDENCE.** F136: this probe's
ruler is the LENS interior, F75's bar is RIM-ruled, and F75 says that **1.19 conversion CANNOT
BE CHECKED from any frame we hold.** M1 now prints the BEZEL-ruled figure beside it — **1.550
against a rim-ruled 1.951–2.121**. F75's verdict stands: honest range **50–80 mm**, best single
estimate **52 mm**, no single constant fixes it.

---

## §0.07 THE MACHINE'S VERDICT AT CLOSE OF REV 61 — every one watched print

```
bootstrap.sh          ALL 10 PASS
verify_clone.sh       ALL 271 PASS on a clean tree   <- 0 FIDELITY, 271 SELF-CONSISTENCY
probe_rev59_nose      M1 PASSES lens-ruled at 2.114  <- NOT item B closed, see F136
                      BEZEL-ruled 1.550 against a rim-ruled bar 1.951..2.121
probe_rev46_vw        9 checked, 2 FAILED -- C6 and C8
                      C8 photograph 3.39, built 1.49, A PLAIN CROSS 1.39
flank_compare.py      FAILS: worst region `i` 0.687;  `Senor` 979 px of ink against 1261
senor_trace.py        the `S` rasterises as 1 component;  T1_SENOR_BREAKS=1 gives 3
expert panel          83 / 240   (modelling 34, lookdev 28, photography 21)
```

**AND THE STANDING WARNING, WHICH `verify_clone.sh` PRINTS ITSELF.** A green check is not
evidence about the vehicle. **Not one of those 271 rows compares the model to a photograph.**

---

## §0 THE GOAL, AND HOW FAR OFF IT WE ACTUALLY ARE

**CARRIED FORWARD FROM THE REV-55…61 BRIEFS. It is not mine and it is not to be dropped —
rule 16.**

**PHOTO-REALISTIC PARITY WITH THAT EXACT BUS.** Not "a convincing VW bus" — *that one*, the red
Señor Tacombi combi in the frames on this repo. **Any single measurement off is unacceptable,
per-measurement and not on average.** A model right in ninety places and wrong in one is not
99 % done, because he will look straight at the one. **At rev 58 he did exactly that, at the
emblem, for the fifth time. At rev 61 he did it again, for the sixth.**

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
./verify_clone.sh       # ALL 271 PASS -- and read its verdict block
```

**MEASURED AT REV 61 PICKUP:** HEAD was **0 ahead / 0 behind** `origin/main` — rev 59 and rev 60
were merged by PR #19, which the rev-61 brief did **not** know. **That is the eighth consecutive
revision whose prose guessed the merge state. Measure it.**

**AND THE ELEVENTH DELETION HAPPENED, ON SCHEDULE.** `fetch --prune` printed
`- [deleted] origin/claude/senor-tacombi-rev-61-99pz2u` — **this revision's own branch**, before
anything had been pushed to it, the SIXTH RUNNING. It was recreated by the first push.
**Expect it at rev 62.**

---

## §2 THE EMBLEM — HIS TOP ITEM, SIX REPORTS, AND REV 61 CLOSED THE SEARCH SPACE

**DO NOT re-try any of these. Every one is measured, not argued:**

```
reach            T1_VW_CAPMIN            cells 6 -> 2        (F101, and CONFIRMED at rev 61
                                                              by a second statistic: 1.58)
stroke weight    T1_VW_WFRAC -> 0.48     cells 6 at EVERY value           (F102)
six-constant cell-count solve            7 cells only at residual 0.2498  (F103)
separate strokes                         rev 8 did it and got an X        (F113)
the V/W kink                             the PHOTOGRAPHS have the same kink, OPPOSITE SIGN
                                         (-8..-10 deg photographed vs +10.1 built)  (F138)
the terminal angles off the badges       BUILT IT: elongation 1.54, residual 0.1800,
                                         both WORSE than shipped           (F141)
```

**THE X IS NOW A NUMBER (F137).** C6 counts cells and F105 showed that count is not
scale-stable. **C8 measures cream-cell ELONGATION** and does not move with raster scale:

```
photograph              3.39
built, shipped          1.49   at 276 rows AND at 69
A PLAIN CROSS           1.39   <- the built glyph is barely distinguishable from an X
six parallel bars      10.71
```

**AND THE SEARCH SPACE IS CLOSED (F137).** Using the probe's OWN functions at 0.02 s per
evaluation, **8,174 candidates**: the maximum elongation achievable **subject to C4's own
landmark bar** (residual < 0.045) and 6 cells is **1.634**, against the photograph's 3.39. With
the constraint dropped it reaches **4.644**. **So the CONSTRUCTION can produce slivers and the
LANDMARKS forbid it: L1–L6 and the photograph's cell shape are INCOMPATIBLE.**

**THAT IS THE NEXT REVISION'S QUESTION, AND IT IS A SHARP ONE:** *which of L1–L6 is wrong?*
F139 already shows **C6's target of 7 is contaminated** — the photograph's smallest counted
cell sits ENTIRELY INSIDE THE RING BAND with no left-hand counterpart, so the genuine count is
**6, the same as the build**, and 7 is topologically unreachable for a symmetric V-over-W.
**If C6's target can be wrong, L1–L6 can be too.** Re-derive them on `ref_workshop.jpg`'s badge
(93×63 px, **1.86× the area** of the 41×69 source every constant was fitted to) — admissible for
SHAPE under the pressing-is-geometry corollary in §0.1 — and see which landmark moves.

**AND IT IS ON FIVE OBJECTS (F69):** the nose roundel and four hubcaps. Two panels confirmed the
X on both independently.

---

## §3 THE WORK LIST FOR REV 62

**RANK BY PIXELS OF THE DELIVERY FRAME** — `python3 visibility_budget.py 3840` — **and PASS IT
THE FRAME.** Rev 60 "repaired" that script and rev 60c-ii found it had reproduced the defect it
fixed (F132): it took its scale off whichever hero was rendered LAST, in an untracked directory,
so the ranking that decides what counts as WORK depended on `out/` mtimes — 724 px/m against 801
with a different newest frame. It names the frame it used on every run now. **Its own ceiling:
pixels are not visibility — a hard-edged error reads louder per pixel than a soft one, so use it
for ORDERS OF MAGNITUDE, not to rank neighbours. And the owner outranks it**, which he used at
rev 58 and again at rev 61.


**Ranked. `PANEL_rev61.md` carries the full merged programme with the panels' own point
estimates — but read §4 of `LEDGER_rev61.md` first, because FOUR of the panel's top items are
already refuted and their point estimates are NOT bankable.**

1. **THE EMBLEM — which landmark is wrong?** See §2. This is his top item and rev 61 turned it
   from "try another constant" into a single well-posed question.
2. **`Señor` IS NOT DELIVERED.** He ruled *"clearer than the photo, well defined … enhanced from
   the photo."* The `S` is now one continuous letter — but the word carries **979 px of ink
   against the reference's 1261 (77.6 %)** at IoU **0.721** of its ceiling, and the rev-61 bridge
   moved that by **1 px**. **The deficit is letterform SIZE and WEIGHT across the whole word.**
   A lookdev panel independently measured the ink bbox at 78 % of the reference's width and
   71 % of its height, and reported no separable letterforms at delivery scale.
3. **THE NOSE, 50–80 mm remaining (F75, F136).** Do NOT chase it with a single constant — F75
   says no single constant fixes it and rev 61's +24 mm is consistent with that. And **fix the
   ruler before quoting any number**: M1 is lens-ruled, the bar is rim-ruled.
4. **TEST THE TWO DISPUTED CEILINGS BEFORE QUOTING F62 AGAIN.** The photography panel measured
   the specular-event census at **0.024 % of red pixels against 7.07 %** in the flattest-lit
   photograph we hold, and noted the render's own SIDE frame reaches a panel spread of 0.521 —
   inside the reference range — on the same shader that gives the hero 0.224. **If that holds,
   a large part of what this project has ceiled to the studio is not the studio.** It also
   disputes the ground-shadow ceiling. **Recorded, NOT adopted. Test it.**
5. **THE SURVIVING PANEL ITEMS**, none of which rev 61 touched: the glass is a flat slab
   (0.5 % sd against the photograph's 12.8 %); the tyres have no tread, no sidewall lettering,
   and are 35 % too light; the tail is modelled as a box where the real one is a barrel; every
   shut line is a 1-px ink stroke with no leading-edge highlight; the galley is monochrome; the
   counter is a floating slab with no fascia.
6. **F143 — TWO LOUDSPEAKERS STAND ON THE ROOF AND ARE UNMODELLED.** Known since
   `AUDIT_rev12.md`, in no live carrier for 49 revisions, corroborated on two independent scenes.
7. **THE INHERITED CLUSTER** — F14 (nine revisions un-re-measured), F15, F10, F20.

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

**RULED AT REV 61, NEW:** ***"senor Tacombi should be clearer in the render than in that photo.
Well defined. I want this 3d model to look like new. Enhanced from the photo."*** That closed
`senor_trace.py`'s standing owner-decision. **It also creates a live tension with SPEC §3's
WEATHERED lock — surface it, do not silently pick a side.**

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
> OWN SEARCH WINDOW MUST NOT PUBLISH.** Two of rev 61's did, and their outputs (134 mm / 81 mm)
> are recorded in F150 as artefacts, not figures.

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
**CARRIED:** `T1_NOUNDER`, `T1_UNDER_ZBUG`, `T1_UNDER_PROUD`, `T1_UNDER_VIS`, `T1_UNDER_YBUG`,
`T1_UNDERSEAL`, `T1_VPOW`/`T1_VPOWZ` (**move them TOGETHER**), `T1_VRISE`, `T1_VW_CAPMIN`,
`T1_VW_PUREFIT`, `T1_VW_WFRAC`, `T1_VW_CELLSOLVE`, `T1_VW_DUMP`, `T1_VW_RES`, `T1_VW_WSWEEP`,
`T1_DOOR_STALE`, `T1_NORIG`, `T1_RIG`, `T1_WORLD`, `T1_MOT_AMP`, `T1_GL_WRGH`, `T1_BODY_RGH`,
`T1_GC_ABSSPREAD`, `T1_GC_LOOSEMASK`, `T1_GL_TILES`, `T1_PG_PAINT`, `T1_BAREMAT`, `T1_CLAY`.

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
emblem's cause, the roof's loudspeakers, and eleven wrong measurement windows were all found
that way, and none by reasoning.**

**When you need something from him, ask as MULTIPLE CHOICE with the reference material attached
— one crop, one mark, one sentence — and ASK IT WITH THE QUESTION TOOL.**

---

## §8 THE OPEN-FINDINGS REGISTER — `OPEN_FINDINGS.md`

**IT IS A CARRIER (rule 16). Rows leave it only by being CLOSED with the measurement that closed
them, or RETIRED with the ruling that retired them. Never by being dropped.**

It carries **150 rows** now. **Rev 61 added F134–F150**, of which **seven are retractions or
refutations**, three of them of rev 61's own published claims.

**THE POINT OF THE FILE IS THE PROVENANCE GRADE, NOT THE LIST.** An `INHERITED` row is a claim.
**GRADE DECAY IS ITSELF A FINDING.**

**STILL INHERITED AND OLDEST:** **F14** (`gal_end_f`'s sight lines, **rev 52 — NINE revisions
un-re-measured**), F15, F20, F10, and **F18** (the die-cut sticker, rev 44 — the oldest live row
and the project's original deliverable).

**AND `REMAINING_WORK_rev61.md` §I IS STILL NOT TRIAGED.** It carries 27 rows that were in no
other document. **Rev 61 proved that section's worth: F77 was sitting in it, it was RIGHT, and
the deficit it named was hidden behind a broken gate for two revisions.** Triage the rest.

---

## §9 THE HORIZON BEYOND REV 62

**CARRIER: re-rank it, do not rewrite it, and say what moved.**

**WHAT MOVED AT REV 61.** The nose's gate was **fixed** and its remedy family **un-refuted**;
the emblem's search space was **closed** with a number; `Señor` got its **owner ruling** and is
still not delivered; the roof half of **F91 is done**; and an expert panel put **83/240** on the
board with two of this project's ceilings **disputed on measurements**.

| horizon | the work | why |
|---|---|---|
| **next** | **THE EMBLEM — which of L1–L6 is wrong?** | Rev 61 proved no spine arrangement satisfies both the landmarks and the photograph's cell shape. The question is now singular |
| **next** | **`Señor`'s letterform size and weight** | His explicit ruling, measured at 77.6 % of the reference's ink, and NOT delivered |
| **near** | **Test the two disputed ceilings** | If the photography panel is right, a large part of what is ceiled to the studio is not the studio |
| **near** | **Glass, tyres, the tail's barrel, the shut lines** | The surviving panel items, none touched |
| **near** | **F143 — the roof loudspeakers** | Unmodelled since rev 12, in no carrier for 49 revisions |
| **then** | **F10–F14 — the galley cluster** | F14 is NINE revisions inherited |
| **CEILED** | **F44/F60/F62 gloss; F83 the front arch; F67's residue; F142's roof colour; F148's dark chrome** | **But F62 is now DISPUTED — see §3.4. Do not quote it without testing it** |
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
