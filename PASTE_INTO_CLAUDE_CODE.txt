# NEXT CONTEXT PROMPT — rev 65

## §0.0 DO THIS FIRST — THE WHOLE DECISION, IN TWENTY LINES

**Before you read another word, put the machine to work. It is CPU-bound and idle right now.**

```bash
cd /home/user/combi_render
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
nohup setsid env T1_SUB=1 T1_PREVIEW=front,side,hero,hero34r T1_PFX=r65 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r65.log 2>&1 < /dev/null &
```

`out/` is untracked and **starts EMPTY**. **`bootstrap.sh` first**: at rev 58–62
`/tmp/blender/blender` did not exist. Then start the render, then read.
**`grep -c Saved: /tmp/r65.log` must be 4** — a backgrounded runner's exit code is the
redirect's. **USE `setsid`, NOT A BARE `nohup &`** (F173).

**AND CHECK YOUR CLONE IS THE TIP.** Rev 62, 63 **and 64** all arrived **SHALLOW**. A content
check cannot detect that you are on an old commit of the same repository. **Only `git fetch
--unshallow` and the ahead/behind loop in §1 find it.** Run §1 before you trust anything.

**THEN RUN `./judge_set.sh r65`.** `post.py` implements bloom → CA → vignette → grain and the
preview path **never calls it** (F146). Judge photorealism on the `_post` set, never the raw
one. *(**ONLY `bloom` defaults to 0.0** — `ca`, `vig` and `grain` default to **1.0**. Three
documents said "every per-stage gain" until rev 64; F189a.)*

**READ `LEDGER_rev64.md` §4 AND §5 BEFORE YOU PLAN** — what rev 64 did NOT do, and the four
things it got wrong in its own work.

---
## §0.05 THIS BRIEF WAS AUDITED AGAINST THE MACHINE — AND AN ADVERSARY DID RUN ON ITS
## PREDECESSOR, WHICH IS WHY FOURTEEN OF ITS CLAIMS CHANGED

**HOW THIS DOCUMENT WAS AUDITED, so the next context knows where it is weak (rule 17).**
Every figure in §0.07 was RE-RUN at the handoff commit, not transcribed — that is how the
inherited `36 asked` was caught reading 42. Every path it names resolves (`audit_brief.py`,
**10 checked, 0 FAILED**) and `audit_adversary.py` asks **48, 0 BROKE**. **THAT IS THE
MECHANICAL HALF ONLY.** The half no script can do — recomputing every figure — was done by
hand for §0.06, §0.07 and §2, and **NOT** for §0's inherited gate table beyond the four
gates re-run this revision. **The weakest part of this document is §4: it is the longest
carrier, it is almost entirely inherited text, and rev 64 found a SEVEN-REVISION
misattribution sitting in it (F188). Start an adversary there.**

**Rev 62 and rev 63 both shipped with no independent adversary. Rev 64 ran one (rule 15) and
it returned FOURTEEN findings the author had not seen** — including that the brief's top item
carried a diagnosis that was **not in the probe it credited**, and that a **question about to
be put to the owner rested on a figure that is in no source file**. **PUT ONE ON THIS
DOCUMENT TOO. Assume it carries defects of the same class.**

**WHAT REV 64 CAUGHT IN ITS OWN WORK — four, and they are listed in `LEDGER_rev64.md` §5:**
a column carrying a THIRD ruler under a SECOND one's label; a re-implementation that differs
from the original by half a pixel *because the original was wrong*; **a grade guard going red
on rev 64's own register row, and the vocabulary NOT being widened to make it pass**; and the
near-miss on the owner question above.

**`verify_clone.sh` WAS RUN ON THE ACTUAL HANDOFF COMMIT, not on the tree later.**

---
## §0.06 THE BIG ONE: THE EMBLEM'S TARGETS ARE MEASURED ON IMAGES THAT ARE NOT MIRROR-SYMMETRIC

**THE VW MARK IS MIRROR-SYMMETRIC ABOUT ITS VERTICAL. THE MODEL IS. THE TWO PHOTOGRAPHS ARE
NOT.** Mirror IoU of each mask against its own left-right flip:

```
    the BUILT glyph  (symmetric by construction)     0.9777
    the WORKSHOP badge -- what rev 63 traced         0.4111
    the TARGET BUS badge, ref_nolita_front34.jpg     0.4812
    KILL: the built glyph sheared by 0.30            0.2732
```

`probe_rev63_angles.desquash()` rescales the axes and **NEVER ROTATES**, so a three-quarter
view's shear survives it. **Then shear the BUILT glyph and change nothing else:**

```
    shear   mirror IoU   elongation   cells
     0.00     0.9777       2.388        6
     0.20     0.3574       2.809        8
     0.40     0.2716       3.400        8
     0.60     0.2294       3.853        8
    PHOTO   0.411/0.481    3.390        7
```

**C8's 3.390 TARGET AND C6's 7 BOTH LIE INSIDE THE RANGE A PURE SHEAR OF THE GLYPH ALREADY IN
THE TREE SWEEPS.** Neither gate can separate *"the glyph is the wrong shape"* from *"the frame
is oblique"*. F175 showed the gates pass on a bad glyph; **this shows their TARGETS carry the
viewing angle.** Rule 39. `python3 probe_rev64_shear.py`, and **look at
`probe_scratch/rev64_shear.png` before you believe any of it.** **F184.**

**CEILING, AND IT IS NOT AN OVERCLAIM (F185).** This does NOT show shear is the WHOLE gap: at
the shear that first matches the photographs' own mirror IoU the elongation is **2.809, not
3.390**. **That is §3 item 1.**

---
## §0.07 THE MACHINE'S VERDICT AT CLOSE OF REV 64 — every one watched print

```
bootstrap.sh            ALL 10 PASS   <- row 9 GREEN for the first time in SEVEN revisions
verify_clone.sh         ALL 298 PASS on a clean tree, AT THE HANDOFF COMMIT
                        <- 0 FIDELITY, 298 SELF-CONSISTENCY.  285 -> 287 (the stranded
                           merge) -> 298 (eleven rows).  NO row was relaxed.
audit.py                0 fail, 0 warn at T1_SUB=2, 228 meshes.  STATE.md REGENERATED and
                        IDENTICAL apart from provenance -- THAT IS THE CONTROL
probe_rev63_trace.py    ALL CONTROLS PASS   (rev 63: FAILED T3)
probe_rev64_shear.py    6 checked, 0 FAILED   -- NEW
vw_pressing.py          5 checked, 0 FAILED   -- NEW
probe_rev46_vw.py       9 checked, 3 FAILED -- C4, C5, C6.  UNCHANGED from rev 63
probe_rev63_canon.py    5 checked, 0 FAILED
probe_rev63_reach.py    ALL CONTROLS PASS
trace_outline.py        SELFTEST PASS (10 shapes);  svgraster.py SELFTEST PASS (9)
audit_brief.py          10 checked, 0 FAILED
audit_adversary.py      48 asked, 0 BROKE   <- rev 63's brief claimed 36 when it was 42
                        (F189b).  SIX questions REPLACED at rev 64, and ONE RETIRED IN
                        PLACE because its own text repeated the false "RING (0.508)"
flank_compare.py        FAILS.  worst region `i` at 0.687 of its own ceiling
gloss_compare.py        FAILS at 0.442 of the photograph's spread (bar 0.60)
probe_rev59_nose.py     5 checked, 0 FAILED.  BEZEL-ruled 1.550 / 1.584 vs rim-ruled
                        1.951..2.121 -- F136 stands, a PASS here is NOT closure
probe_rev59_door.py     8 checked, 1 FAILED (M3, BY DESIGN)
```

**AND THE STANDING WARNING, WHICH `verify_clone.sh` PRINTS ITSELF.** A green check is not
evidence about the vehicle. **Not one of those 298 rows compares the model to a photograph.**

---
## §0. THE GOAL, AND HOW FAR OFF IT WE ACTUALLY ARE

**CARRIED FORWARD FROM THE REV-55…64 BRIEFS. It is not mine and it is not to be dropped —
rule 16.**

**PHOTO-REALISTIC PARITY WITH THAT EXACT BUS.** Not "a convincing VW bus" — *that one*, the
red Señor Tacombi combi in the frames on this repo. **Any single measurement off is
unacceptable, per-measurement and not on average.** A model right in ninety places and wrong
in one is not 99 % done, because he will look straight at the one. **At rev 58 he did exactly
that, at the emblem, for the fifth time. At rev 61 he did it again. At rev 62 he said *"I am
sick and tired of not being able to execute a publicly available emblem."***

**AT REV 63 THE EMBLEM CHANGED AND NOW READS AS A V OVER A W ON THE NOSE. IT IS NOT RIGHT,
AND AT REV 64 IT DID NOT MOVE.** Held next to the photographs, four things are still visibly
wrong: the glyph does not fill its ring the way both photographs do, the V is too narrow, the
W's outer arms are too short, and the strokes are thinner than the pressing's. **The W's two
outer arms visibly FLOAT short of the ring — C6 measures it at 18.9 mm and you can see it in
`probe_scratch/rev64_front_emblem.png`.** What is new is that **two of the three gates that
would score a fix are now known not to mean what they were taken to mean** (§0.06).

**AND HERE IS THE HONEST DISTANCE — THE GATE TABLE, WHICH AN ADVERSARY ONCE CAUGHT A BRIEF
DROPPING.** `verify_clone.sh` ends **ALL 298 PASS**: **0 FIDELITY, 298 SELF-CONSISTENCY.**

| gate | state MEASURED at close of rev 64 |
|---|---|
| `flank_compare.py` | **runs, FAILS.** Worst region **`i` at 0.687 of its own ceiling**; the `Senor` row scores a **DELIBERATE DEPARTURE** — F156, **FOUR revisions un-re-based** |
| `gloss_compare.py` | **runs, FAILS at 0.442** (bar 0.60). Model-side lever EXHAUSTED (F60/F62) — **but F62's ceiling is DISPUTED on measurements** |
| `probe_rev46_vw.py` | **C4, C5, C6 FAIL; C7, C8 PASS — AND C6's AND C8's TARGETS ARE NOW UNDER F184.** Read §0.06 before quoting either |
| `probe_rev64_shear.py` | **NEW. 6 checked, 0 FAILED.** The reason the two above cannot decide the emblem |
| `probe_rev63_trace.py` | **ALL CONTROLS PASS.** The trace is sound; what it traced is a sheared frame (F183) |
| `probe_rev59_nose.py` | **M1 PASSES lens-ruled — AND THAT IS NOT CLOSURE (F136).** Bezel-ruled 1.550 / 1.584 against rim-ruled 1.951–2.121 |
| `mottle_measure.py` | **runs, and it is NOT measuring the mottle** — 1.1–2.0 % of it |
| `probe_rev45_ground.py` | item D's gate, `T1_NOUNDER`'s only consumer. **G4 0.3602 built / 0.5475 ablated / 0.057 photographed** |
| `probe_rev59_door.py` | `T1_DOOR_STALE`'s gate. **8 checked, 1 FAILED (M3, BY DESIGN)** |
| `cream_rms.py` | `run()` is the LIVE photograph-side cream path |
| `visibility_budget.py` | the RANKING, not a gate. **PASS IT A `.png`** — `visibility_budget.py 3840` alone falls back to globbing `out/*hero*.png` by mtime, **which IS F132's defect**, so the command printed in every brief through rev 64 reproduces the bug the sentence beside it warns against (F189) |
| everything else | self-consistency |

**AND AT REV 61 HE ADDED A STANDARD.** *"I want this 3d model to look like new. Enhanced from
the photo."* That is not the same as WEATHERED, which SPEC §3 locks. **Where the two collide,
say so and put it to him** — do not silently pick one.

### §0.1 THE REFERENCE SET IS COMPLETE, AND IT IS GUARDED FRAME BY FRAME

> *[owner, rev 54]* **"we have all references that we need on repo and I want to make sure
> that is never forgotten."**

**ONE: WHAT WE HOLD IS WHAT WE GET. STOP PARKING WORK BEHIND A PHOTOGRAPH.** Where a frame
genuinely cannot answer, the result is *"it cannot be recovered from what we hold"* — a real
result, stated with its ceiling. **Rev 61 produced four; rev 63 one; rev 64 one more**: F185,
the amount of shear in the two badge frames, which cannot be separated from shape until the
ring is fitted as an ellipse.

**TWO: THEY CANNOT BE RE-SHOT, SO THEY ARE CHECKSUMMED INDIVIDUALLY.** **16 `ck "ref …"` rows
name them one at a time** *(the "18" in the rev-63 and rev-64 briefs counted two aggregate
rows that by their own words do not name a frame — F189)*:

* **the RED target bus** — `ref_side.jpg`, `ref_rear34.jpg`, `ref_playa_34.png`,
  `ref_nolita_front34.jpg`, `ref_nolita_front34b.jpg`, `ref_nolita_flank.jpg`,
  `ref_nolita_doorshut.jpg`
* **NOT the target, geometry only** — `ref_workshop.jpg` is the **GREEN** vehicle;
  **`IMG_2073.jpeg` is ALSO the GREEN vehicle**; `bus_model_ref.JPG` is a **SCHOOL BUS**, a
  fidelity bar only. **Paint and artwork do not transfer between vehicles; geometry does
  (rule 11)** — *and the corollary rev 63 leaned on: the nose roundel's SHAPE is the factory
  chrome PRESSING, which is geometry and DOES transfer; only its colour is artwork (F141).*
  **REV 64 ADDS THE LIMIT ON THAT COROLLARY: the shape transfers, but the PROJECTION does
  not. `ref_workshop.jpg` shows the pressing obliquely (mirror IoU 0.4111) and no de-squash
  removes it (F184).**
* **AND RULE 11 APPLIES BETWEEN LIVERY STATES OF THE SAME VEHICLE**, which killed F99, F100
  and F140: `ref_nolita_front34b.jpg` has a chalkboard lid and no folk art.
* **AND IT APPLIES BETWEEN ERAS OF A TRADEMARK** — F168. `vw_canonical_2019.svg` is the mark
  as REDRAWN IN 2019 and is **a different object** from the 1955–67 pressing: 3 cells /
  elongation 1.597 against the photographed badge's 7 / 3.390 at one raster. **It is
  deliberately NOT named `ref_*`.**
* **derived/annotated** — `ref_grid.png`, `ref_side_grid.png`, `ref_nose_grid.png`,
  `ref_band_grid.png`, `ref_x6_lanczos.png` *(a 6× upsample of the RETIRED thumbnail —
  "interpolation, no new information")*
* **retired** — `ref_source.jpeg`, a 246×197 thumbnail the record itself retired
* a **floor of 54** reference-class tracked images, and **the five byte-identical pairs are
  asserted to stay five** — a sixth group means a frame arrived that duplicates one we hold,
  which is **not corroboration** and has fooled this project before.

**AND `ref_playa_34.png` IS UNDER-USED.** Rev 61 verified its white balance **neutral** on the
paving (116,119,120) and used it, not `ref_side.jpg`, to judge paint. `ref_side.jpg` and
`ref_rear34.jpg` are both globally WARM.

---
## §1 START HERE — MEASURE THE BRANCH, DO NOT TRANSCRIBE IT

```bash
git fetch --all --prune
git rev-parse --is-shallow-repository        # <- rev 62, 63 AND 64 all arrived TRUE
for b in $(git branch -r | grep -v HEAD); do
  printf "%-52s ahead %-3s behind %s\n" "$b" \
    "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"
done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
./bootstrap.sh          # read ROW 9, and read the "N ahead / M behind" NOTE line
./verify_clone.sh       # ALL 298 PASS -- and read its verdict block
```

**MEASURED AT REV 64 PICKUP:** the clone was **SHALLOW**; `fetch --prune` printed
`- [deleted] origin/claude/new-session-e854rn` — **the designated branch, before anything had
been pushed to it, the EIGHTH RUNNING**; HEAD was **0 ahead / 0 behind** `origin/main`; and
**row 9 FAILED** on `origin/claude/bus-model-rev57-yvrlhi`, 6 commits, **stranded since rev
57 under an owner ruling to merge it**. **IT IS NOW MERGED (F188). EXPECT THE BRANCH DELETION
AGAIN AT REV 65.**

> **AND THE LESSON THAT COST SEVEN REVISIONS: the rev-64 brief's §1 asserted rev 63 had
> measured "no branch carried work HEAD did not have". It was true when written and false
> 24 minutes later. `bootstrap.sh` row 9 outranks that sentence and every sentence like it,
> INCLUDING THIS ONE.**

**AND MEASURE IT AGAIN BEFORE YOU FINISH.** `origin/main` moved mid-revision at rev 51 and
rev 55. **At rev 64's CLOSE, HEAD was 11 ahead / 0 behind `origin/main`** — the pickup figure is
NOT the close figure, and an adversary once caught a brief shipping only the pickup one.

> **AND ONE THING THE LOOP WILL SHOW YOU THAT IS NOT A FINDING:**
> `origin/claude/bus-model-rev57-yvrlhi` still reads **6 ahead of `origin/main`** at rev 64's
> close. **It is merged into HEAD**, which is why `bootstrap.sh` row 9 — which asks about
> HEAD, not about main — is green. It goes to 0 the moment rev 64's branch reaches `main`.
> **If row 9 is RED at your pickup, that is a different branch and a real finding.**

---
## §2 THE EMBLEM — **READ `EMBLEM_HANDOFF.md` FIRST, AND READ ITS §5b.2 RETRACTION.**

> *[owner, rev 62]* **"I am sick and tired of not being able to execute a publicly available
> emblem."**

**WHAT IS IN THE TREE:** rev 63's six spine constants (`VW_V_TIP_X 0.3287`, `VW_APEX_Z
0.0538`, `VW_W_ARM_X 1.1002`, `VW_W_ARM_Z 0.4350`, `VW_W_TROUGH_X 0.3111`, `VW_W_TROUGH_Z
-0.6445`) and the NOSE's `wfrac=0.1800`. **`EMBLEM_HANDOFF.md` §5b.2 and F170 both said these
were NOT shipped, for a whole revision, in the designated carrier for this item. Retracted at
rev 64 — F190. Rule 13.**

**DO NOT re-try any of these. Every one is measured, not argued:**

```
reach            T1_VW_CAPMIN            cells 6 -> 2                       (F101)
stroke weight    T1_VW_WFRAC alone       moves the WRONG way against C8     (F152)
six-constant cell-count solve            7 cells only at residual 0.2498    (F103)
separate strokes                         rev 8 did it and got an X          (F113)
the V/W kink                             the PHOTOGRAPHS have the same kink (F138)
terminal angles off the badges           residual 0.1800, WORSE than a bad
                                         control at 0.1167                  (F141)
the workshop badge's LANDMARKS           CEILED -- scale confound           (F153)
THE CANONICAL 2019 VECTOR as a TARGET    a DIFFERENT OBJECT                 (F168)
A REACH TERM as the discriminator        the trident touches in all SIX     (F179)
"no spine can satisfy the cell shape"    REFUTED: 6.877 at 7 cells          (F174)
TRACING THE PRESSING AND MESHING IT      BUILT, RENDERED, WORSE.  It traced
  (new at rev 64 -- the rev-64 brief's   a SHEARED frame.  T1_VW_TRACED
   TOP ITEM, refuted by doing it)        exists and MUST STAY OFF      (F183)
TUNING AGAINST C6 OR C8 AS THEY STAND    their targets carry the viewing
  (new at rev 64)                        angle -- a pure shear spans both   (F184)
```

---
## §3 THE WORK LIST FOR REV 65

**RANK BY PIXELS OF THE DELIVERY FRAME** — `python3 visibility_budget.py 3840 out/r65_hero.png`
— **and PASS IT A `.png`, or it globs `out/` by mtime and reproduces F132.** Its ceiling:
pixels are not visibility, so use it for ORDERS OF MAGNITUDE. **And the owner outranks it.**

**WHICH RANKING GOVERNS: THIS ONE.** `REMAINING_WORK_rev61.md` remains a CARRIER and its §I
still holds **27 untriaged rows** — **FOUR revisions running**. `PANEL_rev61.md` is a carrier.

1. **FIT THE BADGE'S RING AS AN ELLIPSE AND UN-PROJECT BOTH FRAMES (F185). THIS IS THE
   EMBLEM'S CLOSE AND IT IS WELL-POSED.** The ring is a **circle on the real object**, so its
   image is an ellipse whose centre, axes AND ROTATION give the homography outright. Fit it
   on `ref_workshop.jpg` and on `ref_nolita_front34.jpg`, invert it, and **re-read every
   emblem target on the mark instead of on a photograph of it**: C6's 7, C8's 3.390, L1–L6,
   and F181's six contact angles, which have had no target since rev 63. **The acceptance
   test is already written: `probe_rev64_shear.py`'s mirror-IoU must come up from 0.41/0.48
   toward the built glyph's 0.9777 after un-projection.** If it does not, the fit is wrong.
   **Nothing in this project has ever fitted that ellipse.**
2. **PUT AN ADVERSARY ON THIS BRIEF (rule 15).** Rev 64 did; it found fourteen.
3. **F156 — `flank_compare`'s `Senor` row scores a DELIBERATE DEPARTURE. FOUR revisions
   unacted.** Re-base the reference or annotate the row. Rev 62, 63 and 64 all did neither.
4. **FIX `probe_rev63_shapefit.py`, WHICH THIS BRIEF'S §6 TELLS YOU TO RUN.** Its baseline is
   **stale** (reads `_vw.C` live, and rev 63 moved those constants: the brief's "shipped"
   row of 0.4172 / 1.485 measures **0.4752 / 2.497** now) **and it reads `SHIP_W =
   CAP_EMBLEM_WFRAC`, the HUBCAP's stroke weight, where the nose ships 0.1800 — F178's exact
   trap, still unfixed.** F189, from the adversary.
5. **TRIAGE `REMAINING_WORK_rev61.md` §I** — 27 rows, four revisions.
6. **PROVE THE LARGE-FORMAT PATH (F192).** He ruled **"bigger — large-format print"**.
   `hq_render.py` defaults 3840×2640 and **`stitch.py`'s seam check (F49, exit 2) has never
   been exercised above it**. Prove the chain at a larger size **without** running the
   delivery frame, which he has held (F191). **Ask him the medium only when you have
   something to show him** — do not re-ask it cold.
7. **TEST THE TWO DISPUTED CEILINGS** (specular-event census **0.024 % against 7.07 %**; the
   ground shadow). Recorded, NOT adopted.
8. **THE SURVIVING PANEL ITEMS**, untouched by rev 61–64: the glass is a flat slab (0.5 % sd
   against the photograph's 12.8 %); **the tyres have no tread, no sidewall lettering, and
   are 35 % too light — CONFIRMED BY EYE at rev 64 in `probe_scratch/rev64_hub_front.png`**;
   the tail is a box where the real one is a barrel; every shut line is a 1-px ink stroke
   with no leading-edge highlight; the galley is monochrome; the counter is a floating slab.
9. **F143 — TWO LOUDSPEAKERS STAND ON THE ROOF AND ARE UNMODELLED.** Known since
   `AUDIT_rev12.md` — **52 revisions**. *(Its register row still says it is in no carrier;
   it has been in `OPEN_FINDINGS.md` since rev 61. F189.)*
10. **THE INHERITED CLUSTER** — F14 (**twelve** revisions un-re-measured), F15, F10, F20.
11. **`delivery/READ_ME_FIRST.txt` LISTS THE MODEL'S KNOWN DEFECTS TO HIM.** Keep it current
    or it becomes a lie — it does not yet mention the rev-63 emblem change or F184.

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
renumber its IDs"* — **DISCHARGED AT REV 64, seven revisions late (F188)**; the studio *"keep
studio — ruling stands"* (twice); the front arch *"leave it circular"*.

> **AND ONE LINE OF THAT LIST WAS NEVER HIS — CORRECTED BY ASKING HIM, AFTER REV 62.**
> It carried *"`playa_env.py` is not on the table — do not re-propose it"* from rev 52 to
> rev 64. **That entered as a brief's INFERENCE from W6, whose object is the studio RIG, and
> was applied to a SECOND DELIVERABLE — rule 34 exactly.** Put to him as multiple choice with
> both readings quoted, he ruled the Playa hero **"DEPRIORITISED, NOT CANCELLED"** — which is
> what his own rev-43 words said before that carrier was deleted at rev 44 (**F92**).
> **The correction sat on an UNMERGED BRANCH from rev 57 to rev 64 while every brief kept
> publishing the misattribution (F188).**
>
> **WHAT IT LICENSES: NOTHING TO DO NOW.** *"Focus on the 3d model"* stands, *"keep studio"*
> stands, **no revision works the Playa hero until he opens it**, and **nothing re-proposes
> `playa_env.py` as the delivery frame** — which is also why **F57** stays recorded rather
> than fixed. What changes is that it is a LIVE agreed second deliverable carried in the
> register, and that *"the emotional bar that sits ABOVE clinical accuracy"* is back in the
> record. **Do not re-ask it; do not act on it either.**

**RULED AT REV 64 — BOTH NEW, BOTH BINDING:**

> ***"Keep holding — fix the emblem first."*** — the full delivery render. **His rev-58 gate
> is REAFFIRMED, and this time against a revision that could have shipped.** Asked with the
> crop attached, and with the plain statement that the route rev 63 nominated had been built,
> rendered and refuted. **F191. NO DELIVERY RENDER UNTIL HE SAYS SO.**

> ***"Bigger — large-format print."*** — over the pipeline's 3840×2640 default. **THE EXACT
> DIMENSION IS STILL OPEN**: the option invited him to name the medium and he did not. **Do
> NOT re-ask it cold — ask once you have something to show him.** What is settled: **3840 is
> not the target**, so the banded path must be proven larger. **F192.**
> *(And note what the question corrected: the rev-63 and rev-64 briefs both stated
> `deliver.py` "shipped a set at 2400×1650". **That figure is in no source file and no
> ledger** — `deliver.py` carries no output resolution at all. The premise was withdrawn in
> the asking. F189d.)*

**RULED AT REV 62, STILL BINDING:**

> ***"Bright silver, same as Tacombi."*** — the `Señor` word's finish. **This OVERRIDES SPEC
> §3's WEATHERED LOCK FOR THAT WORD ONLY.** SHIPPED as `script_gen.SENOR_TARNISH = 0.0`.
> `T1_SENOR_TARNISH=1` restores the pre-ruling texture byte for byte. **F157.**

> ***"It is going on different backgrounds for promotional material etc. give me everything I
> might need."*** **BUILT**: `T1_ALPHA=1` renders RGBA with the contact shadow in partial
> alpha (**F159**), and `deliver.py` packages full-frame, trimmed and SEPARATED
> vehicle/shadow layers with a plain-language `delivery/READ_ME_FIRST.txt` (**F160**).
> **It does NOT retire the rev-58 hold, which he has now reaffirmed (F191).**

> ***"this is just the render to plug into company merch with different backgrounds once i
> determine the model is done"*** — **HE DID NOT AUTHORISE THE BOUNCE CARD; "keep studio"
> stands.** Consequences in **F155**: the white backdrop is **scaffolding**, a clean matte
> matters, and **the gate is HIM determining the model is done.**

**RULED AT REV 61:** ***"senor Tacombi should be clearer in the render than in that photo.
Well defined. I want this 3d model to look like new. Enhanced from the photo."*** **It
creates a live tension with SPEC §3's WEATHERED lock — surface it, do not silently pick a
side.**

**CARRIED FROM REV 53, AND STILL IN NO OTHER DOCUMENT:** a frame showing the cream **where it
IS chipped**. Rev 54 and rev 55 both lowered its urgency — the band is 0.27 px at every scale
this project ships — but it is **not struck**, and F19 covers the MODELLING of chipping, not
the photograph request.

**AND HE VOLUNTEERED, STILL BINDING:** the emblem needs a fix, and **the full delivery render
waits until the model is right.**

**STILL WORTH HIS TIME AND NOT ASKED:** **F38** — the nose ring band at the top of its adopted
range, which interacts with the emblem *(and with F185: fitting the ring on the frame gives
this a target too)*; **F39/A3** — `Senor`'s ink deficit; and **the local bounce card** both
panels proposed independently, which is a studio change under a ruling he has given twice.

---
## §5 THE RULES — `CLAUDE.md` CARRIES THE METHOD, NOT THE NUMBERED CANON

The canon (rules 1–33) is printed in `NEXT_CONTEXT_PROMPT_rev50.md` §11. Rules 34–44 live
only in the briefs and are carried here — that is rule 16 firing on this file:

> **34. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Check which object
> a *"the record requires X"* sentence is about, and check the cited line exists. **F26 is
> still open. And rev 64 found rule 34's own textbook case still live in §4 for the
> thirteenth revision — see F188.**

> **35. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Ask the geometry, never the pose
> it happens to be in. **Rev 64's sibling: a VERIFY row counted "two mitred prisms per wheel"
> and went red on a glyph built as one object — the row encodes the CONSTRUCTION.**

> **36. A GATE ONLY COUNTS FOR WHAT IT CAN SEE — ABLATE THE THING YOU ARE ABOUT TO TUNE,
> FIRST.** **Rev 64 ablated the FRAME rather than the glyph, and that is what found F184.**

> **37. AN ABSENT INPUT MUST NEVER READ AS A MEASUREMENT.** A probe that cannot run must say
> **"NO RENDER"** and exit non-zero.

> **38. TWO SIDES OF A RATIO MUST SHARE A RULER, AND IF THEY CANNOT, SAY SO IN THE ROW'S OWN
> NAME.** **Rev 64 found this twice in one probe: a 9 % scale error worth 0.30 of IoU (F186),
> and a whole comparison column that broke it toward the conclusion it was used for (F187).**

> **39. A GATE'S TARGET IS AN INSTRUMENT TOO, AND MUST BE SWEPT LIKE ONE.** C6's 7 (F139),
> M1's ruler (F136), C8's window (F151) — **and now C6's AND C8's targets together, which are
> read off images that are not mirror-symmetric (F184). This is rule 39's largest instance.**

> **40. WHEN AN OWNER RULING MAKES THE MODEL DEPART FROM THE REFERENCE, THE GATE THAT SCORES
> AGAINST THAT REFERENCE STOPS MEANING WHAT IT MEANT.** **F156, and rev 62, 63 and 64 all
> failed to act on it.**

> **41. A GATE PASSING IS NOT EVIDENCE THE THING IS RIGHT. BUILD THE COUNTEREXAMPLE.** C6,
> C8 and IoU all passed on a glyph that rendered as a Y (F175). **AND AT REV 64 IT FIRED
> AGAIN, ON THE ITEM IT WAS WRITTEN ABOUT: the traced pressing won on cells, on elongation
> and on IoU, and rendered as a blob (F183). The render is the arbiter.**

> **42. A CONTROL'S KILL IS A PRECONDITION ON ITS PASS.** If the kill cannot go red at a
> point in parameter space, the control's PASS there means nothing. **C7 was dead exactly
> where C6 went green (F176). Read the kill first.**

> **43. NEW AT REV 64 — A PHOTOGRAPH IS A PROJECTION, AND A DE-SQUASH IS NOT AN
> UN-PROJECTION.** Rescaling two axes cannot undo a rotation or a shear. Before taking ANY
> shape statistic off a frame, ask what symmetry the real object has and check the frame
> still has it. **The VW mark is mirror-symmetric; both badge frames read 0.41–0.48 against
> the model's 0.9777 (F184).**

> **44. NEW AT REV 64 — WHEN A GUARD GOES RED ON YOUR OWN NEW WORK, THE GUARD IS THE DEFAULT
> WINNER.** Rev 64 graded its own register row with a word outside the register's vocabulary
> and the grade guard failed it. **The vocabulary was not widened; the row was regraded.**
> Widening a guard to admit your own output is the laundering these guards exist to stop.

---

## §6 THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build  T1_SUB=1 ~20 s     render 1600x1100 96 spp ~4.5-5.5 min PER VIEW
```

**`bpy` IS A PIP MODULE HERE**, so `python3 probe_rev46_vw.py` runs in ~1.1 s without the
Blender CLI. **Check whether a probe needs `blender -b -P` before you budget minutes for it.**

```bash
./bootstrap.sh                                               # THE TOOLCHAIN IS NOT ON THE CLONE
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
./judge_set.sh r65                                           # the optics chain (F146)
python3 flank_compare.py out/r65_side.png /tmp/fc.png        # GATE 1
python3 gloss_compare.py out/r65_hero.png                    # GATE 3
python3 probe_rev59_nose.py out/r65_front.png                # READ BOTH RULERS
python3 probe_rev46_vw.py                    # THE EMBLEM GATE -- read C7 first, and read F184
python3 probe_rev64_shear.py                 # WHY C6 AND C8 CANNOT DECIDE IT -- START HERE
python3 probe_rev63_trace.py                 # ALL CONTROLS PASS.  T3 was a rasteriser defect
python3 vw_pressing.py                       # the traced pressing, held to its own source
python3 probe_rev63_canon.py                 # the canonical mark, measured
python3 probe_rev63_ablate.py                # the construction's ceiling
python3 probe_rev63_shapefit.py              # F175's counterexample -- BUT SEE SS3 ITEM 4
python3 probe_rev63_reach.py                 # contacts with the ring, and angles
python3 trace_outline.py ; python3 svgraster.py ; python3 senor_trace.py
python3 cream_rms.py                         # the LIVE photograph-side cream
python3 visibility_budget.py 3840 out/r65_hero.png   # PASS IT A .png -- see F132/F189
T1_SUB=2 /tmp/blender/blender -b -P audit.py         # rewrites STATE.md -- COMMIT FIRST
python3 audit_brief.py ; python3 audit_adversary.py  # rules 15/17, MECHANICAL half only
```

**THE GATES THE ABLATIONS EXIST TO MAKE REFUSE:**

```bash
T1_SUB=1 T1_NOUNDER=1 /tmp/blender/blender -b -P probe_rev45_ground.py  # C5 must REFUSE
T1_SUB=1 T1_PG_PAINT=1 /tmp/blender/blender -b -P probe_rev45_ground.py # paints G4's window
python3 probe_rev59_door.py out/r65_side.png        # M3 fails BY DESIGN
python3 probe_rev61.py emblem --paint               # every mode paints its window
T1_VW_TRACED=1 T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py  # F183's refutation,
                                                    # rebuildable.  IT MUST NOT SHIP
```

**ABLATION SWITCHES — all MEASUREMENT-ONLY:** **`T1_VW_TRACED` (NEW at rev 64 — builds the
traced pressing. It is REFUTED (F183); two verifier rows hold it OFF)**, `T1_VW_WFRAC`
(**F178: it overrides the NOSE's weight, `vw_logo_fit()`'s signature default — NOT
`CAP_EMBLEM_WFRAC`, which is the HUBCAP's**), `T1_VW_CAPMIN`, `T1_VW_PUREFIT`,
`T1_VW_CELLSOLVE`, `T1_VW_DUMP`, `T1_VW_RES`, `T1_VW_WSWEEP`, `T1_VNOSE_DIV`, `T1_BULB_STR`,
`T1_BULB_BASEV`, `T1_SENOR_BREAKS`, `T1_SENOR_TARNISH`, `T1_ALPHA`, `T1_NOUNDER`,
`T1_UNDER_ZBUG`, `T1_UNDER_PROUD`, `T1_UNDER_VIS`, `T1_UNDER_YBUG`, `T1_UNDERSEAL`,
`T1_VPOW`/`T1_VPOWZ` (**move them TOGETHER**), `T1_VRISE`, `T1_DOOR_STALE`, `T1_NORIG`,
`T1_RIG`, `T1_WORLD`, `T1_MOT_AMP`, `T1_GL_WRGH`, `T1_BODY_RGH`, `T1_GC_ABSSPREAD`,
`T1_GC_LOOSEMASK`, `T1_GL_TILES`, `T1_PG_PAINT`, `T1_BAREMAT`, `T1_CLAY`.

**FACTS ABOUT THIS MACHINE THAT BITE:**
* **EVERY MEASUREMENT THROUGH `shader_solve._render` IS 8-BIT (F42)**, whatever
  `color_depth` says.
* **`mottle_measure.py` names its output by `MOTTLE_AMP`**, so two runs differing only in
  `MOTTLE_M` **OVERWRITE EACH OTHER'S PNG**.
* **`probe_rev54_aov.py` and `probe_rev55_truenorm.py` write EXR into `probe_scratch/`** —
  delete them before committing and keep the PNGs.
* **`script_gen.py` IS NOT CALLED BY `build.py`.** Change it and regenerate `tex/senor.png`
  by hand, or the render silently uses the old texture.
* **`lid_gen.py` is NOT called by `build.py`** either.
* **`vw_pressing.py`'s `trace()` is NOT called by `build.py`** — the outline is a committed
  literal and the selftest is what holds it to the photograph. That is deliberate.
* **`audit.py` rewrites `STATE.md`. COMMIT FIRST** — and regenerate it after ANY geometry
  change.
* **LAUNCH LONG RENDER QUEUES WITH `setsid`, NOT A BARE `nohup &`** — F173.

**THE DELIVERY CHAIN, WHICH IS NOT THE PREVIEW CHAIN:**
```bash
T1_SUB=2 /tmp/blender/blender -b -P hq_render.py    # ONE build, 10 bands, WITH MARGIN
python3 stitch.py out/hq_hero_raw.png ...           # CHECK ITS EXIT CODE -- 2 on a seam (F49)
python3 post.py out/hq_hero_raw.png out/hq_hero.png # optics LAST, never per strip
```

**THE DELIVERY FRAME — DO NOT RUN IT. He REAFFIRMED the hold at rev 64 (F191). And he needs
LARGE FORMAT, which this chain has never been proven at (F192).**

---

## §7 THE STANDARD, IN HIS WORDS

We are recreating a photorealistic version of **that exact bus**, and **any single measurement
off is unacceptable** — per-measurement, not on average. **Ground in the reference, build,
adversarially audit, iterate.** Never build before grounding. Never call it done off
self-review. Report the measurement **with its ceiling**, never a self-assigned score. Do not
say anything is ready — say what is fixed, what is still wrong, and what you measured.

**RENDER IT, CROP IT, AND LOOK AT IT, before and after every change.** Every defect this
project has shipped passed `VERIFY: 0 fail, 0 warn` and was found by looking at a crop.
**At rev 64 the traced pressing won on every statistic the project owns and rendered as an
unrecognisable blob. One crop settled it in ten seconds.**

**When you need something from him, ask as MULTIPLE CHOICE with the reference material
attached — one crop, one mark, one sentence — and ASK IT WITH THE QUESTION TOOL.**
**And CHECK THE PREMISE FIRST: rev 64 came within one step of asking him a question built on
a figure that exists in no source file (F189d).**

---

## §8 THE OPEN-FINDINGS REGISTER — `OPEN_FINDINGS.md`

**IT IS A CARRIER (rule 16). Rows leave it only by being CLOSED with the measurement that
closed them, or RETIRED with the ruling that retired them. Never by being dropped.**

**Rev 64 added F183–F192**, of which **five are refutations** — two of work done in the same
revision — and **two are OWNER RULINGS**. **F184 is the one that changes what "better" means
on the top item.**

**THE POINT OF THE FILE IS THE PROVENANCE GRADE, NOT THE LIST.** An `INHERITED` row is a
claim. **GRADE DECAY IS ITSELF A FINDING.** *(And the grade vocabulary is
MEASURED / RECOMPUTED / INHERITED / RULED / CEILED / OBSERVED. **Do not widen it** — rule 44.)*

**STILL INHERITED AND OLDEST:** **F14** (`gal_end_f`'s sight lines, **rev 52 — TWELVE
revisions un-re-measured**), F15, F20, F10, and **F18** (the die-cut sticker, rev 44 — the
oldest live row and the project's original deliverable).

**AND `REMAINING_WORK_rev61.md` §I IS STILL NOT TRIAGED** — 27 rows, **four revisions**.

---

## §9 THE HORIZON BEYOND REV 65

**CARRIER: re-rank it, do not rewrite it, and say what moved.**

**WHAT MOVED AT REV 64.** The brief's top item was **built and refuted by doing it**; the
reason **refuted both emblem gates with it** and gave the item its first well-posed close in
eighteen revisions; `bootstrap.sh` row 9 went **green after seven revisions** and an
**owner ruling that had been stranded on a branch since rev 57** reached the record; rule 13
was discharged on a carrier that had contradicted the tree for a revision; an adversary ran
for the first time since rev 61 and found fourteen things; and **two new owner rulings**
arrived. **What did NOT move: the emblem itself, and anything outside it.**

**WHAT MOVED AT REV 63.** The emblem changed on the nose and now reads as a V over a W; the
construction was ablated and F137 overturned; a canonical vector was obtained and disqualified
by rule 11; the gate was refuted as sufficient by a rendered counterexample.

| horizon | the work | why |
|---|---|---|
| **next** | **FIT THE RING AS AN ELLIPSE AND UN-PROJECT (F185)** | The emblem's close, well-posed, never attempted, and its acceptance test is already written |
| **next** | **AN ADVERSARY ON THIS BRIEF** | Rev 64's found fourteen |
| **next** | **F156 — the `Senor` gate row scores a DEPARTURE** | FOUR revisions unacted |
| **next** | **Fix `probe_rev63_shapefit.py`** | §6 tells you to run it and it is stale AND reads the hubcap's weight (F178/F189) |
| **near** | **Prove the large-format chain (F192)** | He ruled he needs it; `stitch.py`'s seam check has never run above 3840 |
| **near** | **Triage `REMAINING_WORK_rev61.md` §I** | 27 rows, four revisions |
| **near** | **Test the two disputed ceilings** | A ceiling attributed to a studio that F155 says gets thrown away |
| **near** | **Glass, tyres, the tail's barrel, the shut lines** | The surviving panel items, none touched in four revisions |
| **near** | **F143 — the roof loudspeakers** | Unmodelled since rev 12 — 52 revisions |
| **then** | **F10–F14 — the galley cluster** | F14 is TWELVE revisions inherited |
| **CEILED** | **F153 the workshop landmarks; F168 the 2019 vector; F183 the traced pressing; F44/F60/F62 gloss; F83 the front arch; F67's residue; F142's roof colour; F148's dark chrome** | **But F62 is DISPUTED — do not quote it without testing it** |
| **standing** | **F18 — the die-cut sticker** | The original deliverable. Open since rev 44 |

---

## §10 HOW TO GROW THIS HANDOFF WITHOUT BREAKING IT

1. **The set is three files.** `LEDGER_rev<N>.md`, `NEXT_CONTEXT_PROMPT_rev<N+1>.md`, and
   **`cp` of that file over `PASTE_INTO_CLAUDE_CODE.txt` IN THE SAME COMMIT.**
2. **`README.md` and `START_HERE.md` name the newest brief BY NUMBER.** Two rows check it.
3. **THE ROW COUNT IS SELF-REFERENTIAL AND AUTOMATED.** `python3 audit_brief.py
   --fix-count`. Write it LAST. *(It reads the CLEAN-TREE total. On a dirty tree
   `verify_clone.sh`'s own row expects `PASS+1`, which undercounts by the number of earlier
   failures — that is an artefact of the dirty tree, not a defect in the count.)*
4. **ADD ROWS ANCHORED ON ARITHMETIC OR BEHAVIOUR, NOT ON A GREP.**
5. **RUN BOTH AUDITS AS SCRIPTS AND RECORD WHAT THEY FOUND *IN* THE BRIEF.** **REPLACE the
   adversary's questions each revision** — a question that can no longer fail is not a control.
6. **NEVER DELETE A CARRIER.** §0, §0.1, §4, §5, §8 and §9 are carriers.
   **`EMBLEM_HANDOFF.md`, `PANEL_rev61.md` and `REMAINING_WORK_rev61.md` are carriers too.**
7. **RANK BEFORE YOU CHOOSE** — but **the owner outranks the ranking**.
8. **NEVER RELAX ONE COPY OF A CHECK.** Rev 64 re-based `probe_rev63_trace.py`'s T3 with the
   cause named and **four** companion rows, one of which is a kill that was watched firing.
9. **DO NOT LET THE MACHINE IDLE.** Run `bootstrap.sh`, launch the render, then read.
10. **ROOM TO GROW:** new findings go in `OPEN_FINDINGS.md` with an ID and a grade.
