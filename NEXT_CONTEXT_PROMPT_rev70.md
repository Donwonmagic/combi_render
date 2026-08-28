# NEXT CONTEXT PROMPT — rev 70

## §0.0 DO THIS FIRST — THE WHOLE DECISION, IN TWENTY LINES

**Before you read another word, put the machine to work. It is CPU-bound and idle right now.**

```bash
cd /home/user/combi_render
./bootstrap.sh                 # the toolchain is NOT on the clone -- this builds it
pip install pillow             # bootstrap FAILS 3 of 10 without it, EVERY revision
nohup setsid env T1_SUB=1 T1_PREVIEW=front,side,hero34f,hero34r T1_PFX=r70 T1_RX=1600 T1_RY=1100 \
  T1_SAMP=96 /tmp/blender/blender -b -P build.py > /tmp/r70.log 2>&1 < /dev/null &
```

**`grep -c Saved: /tmp/r70.log` must be 4** — a backgrounded runner's exit code is the redirect's.
**USE `setsid`, NOT A BARE `nohup &`** (F173). `out/` is untracked and **starts EMPTY**.

**AND CHECK YOUR CLONE IS THE TIP.** Rev 62 through **rev 69** all arrived **SHALLOW** — **twelve
running** — and the designated branch's remote copy was **DELETED** the same twelve times. A content
check cannot detect that you are on an old commit. **Only `git fetch --unshallow` and the ahead/behind
loop in §1 find it.**

**⚠ THE PREVIEW PATH NEVER CALLS `post.py` (F146).** Run `./judge_set.sh r70` and judge photorealism on
the `_post` set, never the raw one. *(**ONLY `bloom` defaults to 0.0** — `ca`, `vig` and `grain` default
to **1.0**; F189a.)*

**READ `LEDGER_rev69.md` §2 AND §5 BEFORE YOU PLAN** — what rev 69 refuted, and the five things it got
wrong in its own work.

---
## §0.01 ⚠ THE OWNER NAMED THREE THINGS. THEY ARE THE REVISION. NOTHING ELSE IS.

> *[owner, rev 69, closing]* **"It is important that we finish the nose render, make the emblem
> correct (a bare minimum qualification) and fix the opening."** … **"I meant to say the back opening."**

**HE ALSO SAID, IN THE SAME BREATH: *"It's been weeks, and a lot of compute, this is unacceptable."***
**He is right, and the ledger's §6 says exactly where the time went: into INSTRUMENTS, not GEOMETRY.**
Rev 69 built five new instruments and shipped one visual change. **Do not repeat that.**

| # | his words | what it IS, measured | where |
|---|---|---|---|
| 1 | *"finish the nose render"* | the bumper's plan bow is **BUILT and guarded** (F232). What is NOT done is **rendering it and looking at it at delivery size** | §0.06 |
| 2 | *"make the emblem correct"* | the glyph misses by **0.38 IoU with the pose fitted out**, against a control ceiling of 0.98, and **no constant in this tree expresses a stroke PATH** (F236/F237) | §0.07 |
| 3 | *"the back opening"* | the rear hatch is **NOT MODELLED** — a 550 mm blade stands where a full-width propped panel belongs (F163/F165), **RULED by him at rev 62 and never built** | §0.05 |

**RANK: 3, then 2, then 1.** The back opening is un-built geometry the owner ruled on eight revisions
ago; the emblem needs a new construction and has a working instrument waiting; the nose needs a render
and a look. **But he listed them in his own order and the owner outranks the ranking — if you can only
finish one, finish the one he names first when you ask.**

---
## §0.02 THIS BRIEF WAS AUDITED AGAINST THE MACHINE — WHAT THE AUDIT FOUND, AND WHERE IT IS WEAKEST

**HOW (rule 17).** Every figure in §0.01, §0.05–§0.09 and §3 was RE-RUN or READ OFF THE SOURCE at the
handoff commit, not transcribed. `audit_brief.py` and `audit_adversary.py` were both run as scripts,
and **an adversary was DISPATCHED at this document** (rule 15) with instructions to recompute every
figure, grep every quoted string, open every cited crop and **diff this brief against rev 69's for
dropped carrier content**.

**WHAT THE AUDIT ACTUALLY FOUND — FOUR DEFECTS, ALL IN THIS BRIEF'S OWN FIRST DRAFT:**

1. **A DROPPED CARRIER, CAUGHT BY THE MACHINE.** `audit_adversary.py`'s *"is the ring-ellipse fit still
   named as the emblem's close?"* **BROKE.** My first draft of §9 kept *"what moved at rev 67"* and
   **silently dropped the rev-66 and rev-65 lines**, taking **F185's ring-ellipse** with them. §9 is a
   **CARRIER — re-rank it, do not rewrite it.** Restored, and the catch is recorded in the line itself.
   **THIS IS THE FAILURE MODE RULE 16 EXISTS FOR AND IT HAPPENED ON THE FIRST TRY.**
2. **`STATE.md` WAS STALE.** *"is STATE.md CURRENT for the geometry?"* **BROKE** — `t1_mats.py` moved
   after it was written. Regenerated at `T1_SUB=2` on a clean tree: it moved **ONLY in provenance**,
   every vertex count and dimension identical, **which is itself the evidence rev 69's one shipped
   change touched no geometry.**
3. **AN INHERITED CONTRADICTION IN §0.** The rev-69 brief said **"ALL 351 PASS … 342
   SELF-CONSISTENCY"** in one sentence. Both halves must be the same number — every row is
   self-consistency and none is fidelity. Carried from rev 68's re-base and fixed here.
4. **A MISLABELLED COMMIT.** `6af7819` is titled *"rev 70: …"* and is **rev 69's work**. Recorded in
   `LEDGER_rev69.md` §5 rather than hidden.

**THE MACHINE'S OWN VERDICT ON THIS DOCUMENT:**

```
audit_brief.py        10 checked, 0 FAILED   (71 paths, 55 T1_* switches, 31 scripts)
audit_adversary.py    57 asked,   0 BROKE    -- FOUR questions REPLACED
```

**THE FOUR REPLACED QUESTIONS ARE BEHAVIOURAL, NOT GREPS (rule 50).** The rev-63 batch was the oldest
and all four replaced were greps. The new four **RUN something**: the tyre's road-film lift recomputed
from `t1_mats.py`'s own constants; `_on_band` fed two points of the same direction and different
magnitude (rule 54's basis); the emblem's INDEPENDENT frame re-extracted; and
`probe_rev70_tyre`'s band finder re-run on a synthetic of known ratio. **THREE OF THE FOUR WERE WATCHED
FAILING** — a wheel with no hubcap, an empty crop box, and a non-normalising stand-in — because a
control that has only been seen passing is not a control (rule 3).

**WHERE THIS BRIEF IS WEAKEST, AND YOU SHOULD START AN ADVERSARY HERE:**
* **§0.05's rear-hatch numbers are INHERITED from F165 (rev 62) and were NOT re-measured this
  revision.** The angle, the chord and their two-significant-figure ceiling are seven revisions old.
  **`TB_TILT_DEG`, `TB_CHORD` and `TB_WIDTH` were read off `t1_shell.py` live; the PHOTOGRAPHED pair
  was not.** Re-measure before you fit to it.
* **§2's REFUTED LIST**, which an adversary has broken in four consecutive revisions (fourteen at
  rev 64, thirteen at rev 67, twelve at rev 68, and at rev 69 its own headline was found sitting under
  **F104**, unread since rev 60).
* **§0 and §4 remain the two longest carriers and are still mostly inherited text.**

---
## §0.05 THE BACK OPENING — RULED AT REV 62, MEASURED AT REV 62, NEVER BUILT

> *[owner, rev 62, shown `probe_scratch/rev62_q_rear.png`]* ***"The bus's rear hatch, propped open."***

**THIS IS THE OLDEST UN-BUILT THING THE OWNER HAS EXPLICITLY RULED ON. F163 is `RULED-rev62, NOT
BUILT` and has sat for SEVEN revisions.**

**WHAT STANDS THERE NOW.** `t1_shell.tail_board()` builds a flat plate — measured off the mesh at
x −2.420…−1.846, y −0.275…0.275, z 1.754…2.209 — which renders as **a thin blade carrying a bulb row
on two wires, with no panel, no recess and no underside.** The live constants:

```
    TB_TILT_DEG = 38.0      # MEASURED +-2.3, FROM HORIZONTAL
    TB_CHORD    = 0.7110    # MEASURED +-0.028, in the vehicle's XZ plane
    TB_WIDTH    = 0.5500    # *** "POSE CHOICE, NOT MEASURED.  Inside the 0.59 bound" ***
```

**F165 MEASURED THE TWO THAT ARE WRONG, ON `IMG_3840.jpeg` AT 107.92 px/m, EVERY LANDMARK PAINTED
FIRST (`probe_scratch/rev62_hatch_marks.png`):**

```
                       PHOTOGRAPHED        BUILT          verdict
    angle above horiz.   28.0 deg          38.4 deg       ~10 deg TOO STEEP
    visible chord        0.829 m           0.732 m        TOO SHORT -- and 0.829 is a
                                                          LOWER BOUND: the hinge is
                                                          OCCLUDED by the rear roof dome
```

**AND `TB_WIDTH` IS NOT A MEASUREMENT AT ALL — its own comment says so.** 550 mm on a **1750 mm** body
is 31 % of the width. **Nothing has ever measured it.** That is the third defect and the largest.

**WHAT THE PHOTOGRAPHS ACTUALLY SHOW — LOOKED AT AT REV 69, NOT TRANSCRIBED.**
`IMG_3840.jpeg` cropped to (355, 85)–(480, 215) shows the hatch on the **chalkboard** vehicle: a panel
with **visible EDGE THICKNESS**, an **orange top face**, a **dark angled recess cut into its
forward-lower area**, emerging **from behind the rounded rear roof dome** — the hinge is not visible.
`ref_rear34.jpg` cropped to (820, 0)–(1200, 300) shows the same panel **on the RED bus**: a **CREAM
face, a RED edge stripe along its raised edge, and a string of lit BULBS running along that edge.**

> **⚠ SO THE COLOUR IS ALREADY ROUGHLY RIGHT AND THE DEFECT IS FORM. F163's own correction says this
> and a brief has never carried it forward:** *"OUR TAIL_BOARD'S COLOURING — cream blade, red edge,
> bulbs — IS ALREADY ROUGHLY RIGHT, which narrows F163 to FORM rather than paint."*
> **DO NOT re-open the colour. DO NOT paint it orange** — the orange face is `IMG_3840.jpeg`'s
> **chalkboard livery**, and rule 11 forbids transferring paint between livery states. **Geometry
> transfers; paint does not.**

**WHAT TO BUILD, AND EVERY PART OF IT IS IN THE RECORD ALREADY:**
1. a panel with **real thickness and an underside**, not a plate;
2. at **28.0°**, not 38.0° — and re-derive `TB_CHORD` from the ≥0.829 m lower bound rather than the
   0.711 that is in the file;
3. **`TB_WIDTH` MEASURED, not chosen** — it is the one number nobody has ever taken, and both frames
   show the panel's outer edge;
4. the **dark angled recess** in its forward-lower area;
5. the bulb strip kept on the **OUTER/aft edge**, where it already is.

**THE GUARD, IN THE SAME EDIT (rule 13).** There is no gate on this object at all. Build one that
compares the built angle and chord against F165's photographed pair, **and watch it refuse at the
shipped 38.0°/0.711 before you believe it passing at the new values** (rule 3). **F165's CEILING IS
BINDING AND MUST BE IN THE ROW'S OWN TEXT: the frame is 480×320 and the hatch spans ~90 px — TWO
SIGNIFICANT FIGURES. Do not fit to 28.0 as though it were 28.00** (rule 38, rule 48).

**AND ONE THING REV 69 SAW AND DID NOT MEASURE — HAND IT ON RATHER THAN ASSERT IT.** In
`out/r69_hero34r.png` a **large dark rectangle** sits below the blade with red visible through it.
Rev 69 did **not** establish whether that is `glass_rear` rendering black (which would be F71's flat
glazing, a different finding) or an actual hole in the shell. **`STATE.md` says the roof aperture is
"open, and solid fore / aft / both sides", which is about a DIFFERENT aperture.** **Measure it before
you name it** — and note `lid_trunk` is a **different object** (a plate at x −1.87, z 0.608…1.103,
below the counter) and is **NOT** this hatch (F163).

---
## §0.06 THE NOSE — THE SHAPE IS BUILT AND GUARDED. WHAT IS MISSING IS THE LOOK.

**REV 69 SHIPPED THE NOSE'S ONLY MEASURED, CAMERA-FREE DEFECT.** `t1_detail.bumper` appended eleven
points at CONSTANT x under its own `# flat nose face` comment; the face is now **draped onto the body's
own front-face plan curve, raycast at build time**. `BUMP_BOW = 1.0`, station `BUMP_BOW_Z = 1.100`,
ablation `T1_BUMP_BOW`. **Measured on the mesh: +0.05 mm → +21.55 mm** (`STATE.md`, row
*"bumper plan bow (F222)"*), against the shell's +20.38 mm at the same station, floor 8.0 mm.
**`verify._bumper_bow` was WATCHED FAILING: `T1_BUMP_BOW=0` → `VERIFY: 2 fail`, both arms red.**

**SO "FINISH THE NOSE RENDER" IS NOT MORE GEOMETRY. IT IS THE STEP THIS PROJECT SKIPS (rule 1):**

```bash
T1_SUB=1 T1_PREVIEW=front T1_PFX=r70 T1_RX=3200 T1_RY=2200 T1_SAMP=128 \
  /tmp/blender/blender -b -P build.py      # then CROP THE NOSE AND LOOK AT IT
python3 probe_rev67_nose.py out/r70_front.png    # PASS IT A FRAME -- bare, P3 does not run (F225)
python3 probe_rev59_nose.py out/r70_front.png    # READ BOTH RULERS
```

**AND RENDER THE CONTROL TWICE (F228, rule 49).** The floor at 1600×1100/96 spp is **2.441 % of pixels
differing by >8 levels, worst channel 40**. Publish it beside any render A/B.

**WHAT IS STILL OPEN ON THE NOSE, AND IT IS A CEILING, NOT A TASK.** The bow's **magnitude** has no
independent number. **F231: it cannot be recovered from the frames we hold** — three painted mechanisms,
and every front-facing frame we hold is shot from the SAME front-left quarter, so the far-side symmetric
landmarks are on or beyond the silhouette in all of them. **F229's literature route was `EGRESS_BLOCKED`
in two consecutive containers** (`thesamba.com`, `en.wikipedia.org`, HTTP 000). **TRY IT AGAIN — the
network policy is per-environment** — but do not budget the revision on it. **F223's bracket
B ∈ [16, 76] mm contains the shipped 19.6**, so the shipped nose is not excluded by anything we hold.

**DO NOT FIT `NOSE_BULGE` TO 40 mm** — that instruction was aimed at the wrong object (F222), and
**DO NOT ASK HIM THE NOSE AGAIN: both askings are spent** (F214, F215).

---
## §0.07 THE EMBLEM — "BARE MINIMUM CORRECT", AND REV 69 FOUND THE ROUTE BY ELIMINATION

> *[owner, rev 69, shown an A/B]* ***"Just what the fuck. Are you telling me? That looks right to you?"***
> and, asked to choose between the shipped mark and the solver's own best fit: ***"Neither — both still
> wrong."*** **His EIGHTH and NINTH reports of this emblem.**

**REV 69 BUILT THE COMPARISON THIS PROJECT NEVER HAD, AND IT CHANGES WHAT "CORRECT" MEANS.**
Every emblem statistic in this tree reads an OBLIQUE photograph against a HEAD-ON raster — F184's trap.
`probe_rev69_fitpose.py` **inverts it**: do not un-project the photograph, **PROJECT THE MODEL and fit
the pose out as a nuisance parameter.** The residual that survives the best pose is SHAPE.
**CONTROL P1, watched: it recovers the model from a known 37°/0.62-foreshortened/sheared/perspective
view of itself at IoU 0.9882.** That is the ceiling every number below is quoted against.

```
    THE MARK, POSE FITTED OUT, on ref_workshop.jpg      IoU 0.7345   (ceiling 0.9882)
      the RING BAND alone                                   0.8874   <- the ring is FINE
      INSIDE the ring alone                                 0.6168   <- 73.6 % of the miss
      photo-only / model-only inside the ring             296 / 378   <- NEAR BALANCED
```

**THE INK IS THE RIGHT AMOUNT AND THE WRONG ARRANGEMENT.** That is F104, which the register has carried
since rev 60 and no revision has acted on, now confirmed pose-free. **And F235 says what "arrangement"
means, in a number: the built strokes fan over a spread of 60.9° where the photograph's six span
28.6° — they RADIATE where the real mark's strokes are near-PARALLEL**, and two of the six built cells
are round blobs (aspect 1.09, 1.27) where every photographed cell is a sliver.

**EVERY LEVER THE EMBLEM HAS WAS MEASURED AGAINST THAT RESIDUAL AND THEY ARE ALL EXHAUSTED (F237):**

```
    deficit to close                                     0.9882 - 0.7345 = 0.2537
    stroke weight swept alone, wfrac 0.12 .. 0.52        peak 0.7393 at 0.26   +0.0048
    ALL SEVEN (six spine constants + weight) together    0.7457                +0.0112  = 4.4 %
    T1_VW_TRACED on ref_workshop.jpg  (ITS OWN SOURCE)   0.8250                +0.0905
    T1_VW_TRACED on IMG_2073.jpeg     (INDEPENDENT)      0.6421 vs 0.6671      -0.0249
```

> **THE TRACE'S WHOLE ADVANTAGE LIVES ON THE FRAME IT WAS TRACED FROM. F183 STANDS, and now with a
> mechanism: it is OVERFIT.** `probe_rev69_fitpose.py`'s **P4** re-scores it in a fresh process on both
> frames every run and **goes RED if the trace ever wins independently**, which is the finding that
> would re-open F183.

**⚠ AND `IMG_2073.jpeg` IS THE EMBLEM'S SECOND FRAME. THIS PROJECT HAD NEVER USED IT.** The GREEN
vehicle, a different camera and a different pose — admitted by **rule 11**, because the roundel is the
factory chrome **PRESSING**, which is geometry and transfers; only its colour is artwork (F141). Its
mark sits at box **(288, 542)–(352, 640)**, extracts clean and connected with all six cells, and it is
**the overfit detector**: fit on one frame, score on the other.

**SO THE ROUTE IS NOT ANOTHER SOLVE. IT IS A NEW CONSTRUCTION, AND HERE IS WHY, FROM THE SOURCE.**
`t1_core._spines()` builds the V from **3** points and the W from **5**, and then:

```
    for _p in (V_SPINE[0], V_SPINE[2], W_SPINE[0], W_SPINE[1], W_SPINE[3], W_SPINE[4]):
        assert abs((_p[0]**2 + _p[1]**2)**0.5 - _RING_INNER_FRAC) < 1e-12
```

**EVERY TERMINAL IS FORCED ONTO THE BAND CIRCLE, and `_on_band` NORMALISES, so each pair contributes
only a DIRECTION — its magnitude divides out (F224, corrected at rev 69).** The only interior freedom
is the V's apex and the W's peak. **A stroke's ANGLE is therefore not an independent parameter of this
model at all** — which is exactly why fitting all seven moves the shape by 4 %, and why C1–C5, which
fit L1–L6 (VERTICAL LANDMARK POSITIONS on the ring), optimise a quantity that is not the defect.

**WHAT TO BUILD:** give each stroke its own centreline with free endpoints — **not** forced onto the
band circle — so the six strokes can be made near-parallel, and fit that against
`probe_rev69_fitpose.fit()` **on BOTH frames jointly, holding one out to detect overfit**, with
**F235's angular spread (60.9° → ~28.6°) as the interpretable target** and P1's 0.9882 as the ceiling.

**BEFORE YOU START, READ §2's REFUTED LIST — SEVENTEEN ROWS — AND DO NOT RE-TRY ANY OF THEM.** And
**check the register for a finding before you derive anything**: that is how F139 was found sitting
under F200 (F209), how F216 was found sitting under F221 (F222), and how F104 was found sitting under
this revision's own headline.

---
## §0.08 WHAT REV 69 SHIPPED, AND THE TWO THINGS IT BUILT AND DID NOT SHIP

**SHIPPED — ONE VISUAL CHANGE, AND IT IS THE LOUDEST THING IN THE DELIVERY FRAME (F238).** The record
carried *"the tyres are 35 % too light"* for eight revisions **with no instrument under it**.
`probe_rev70_tyre.py` is that instrument and it says **1.90×**. It is **exposure-free (rule 38)** —
the tyre is scored against **the cream rim ring in the same image** — and it **encodes no pose
(rule 35)**: nothing in it is a typed radius, the wheel centre comes from the hubcap's own colour, its
RADIUS from that blob's area, and both bands are read off the radial profile in units of that radius.

```
    tyre / cream rim ring, IN THE SAME IMAGE          photograph ref_side.jpg   0.1953
                                                      render BEFORE             0.3718  = 1.90x
                                                      render AFTER              0.2458  = 1.26x
    T1_TYRE_FILM 1.0 -> 0.15      T1_TYRE_FILM=1.0 restores the old road film exactly
```

The mechanism needed **no render**: `dust_film` mixes the rubber (linear 0.0225 = sRGB 42) toward
`W_DUST_COL`, a **pale limestone** (linear 0.44 = sRGB 175), at up to `fac_low` 0.34 — landing
sRGB 94–108, a lift of **2.2–2.6×** against the 1.90× measured. **The owner ruled the finish at rev 61:
*"I want this 3d model to look like new. Enhanced from the photo."*** A limestone road film is the
opposite of new.

**NOT SHIPPED — THE GLOSS (F239), AND THE NEGATIVE IS WORTH MORE THAN THE ATTEMPT.** F60/F62 recorded
the model-side lever **EXHAUSTED**. It was not — **F54's clearcoat and F60's roughness were each tested
ALONE in a FEATURELESS WHITE VOID**, where a mirror can only veil and never glint, because a highlight
needs something bright NEXT TO something dark. `studio._refl_env` gives the world a softbox band over a
dark floor, shown to **GLOSSY RAYS ONLY** so the backdrop and every diffuse-calibrated gate are
untouched. **Four configurations, against a TWO-RENDER FLOOR of 0.001 on the spread:**

```
    env  0 (shipped) + coat 0.02     spread 0.412    headroom 0.126   <- SHIPS
    env  1.0         + coat 0.02     spread 0.416    headroom   --
    env 21.0         + coat 0.02     spread 0.389    headroom 0.118
    env 21.0         + coat 0.55     spread 0.399    headroom 0.181
```

**The coat makes specular structure for the first time — headroom +44 %, which is 88× F54's
"+0.5 % of gloss" — and every configuration that raises the highlight also lifts the paint's floor, so
the SPREAD falls.** And it reproduces F54's chroma cost exactly: red **G/R 0.422 → 0.520**, where the
photograph is 0.114. **RULE 44: the guard went red on my own new work and the guard wins.**
`T1_REFLENV` and `T1_BODY_COAT` both ship OFF. **WHAT SURVIVES OF F62: the binding constraint is the
ROUGHNESS, not the environment — at 0.250 the lobe is too broad for any environment to glint through,
so the next attempt must move roughness and environment TOGETHER, the one pairing never tried.**

**NOT SHIPPED — TWO CAUSES OF THE RED'S DESATURATION, BOTH CLOSED (F240).** The render's red reads
**G/R 0.42–0.52 against the photograph's 0.114** — the largest colour error in the delivery frame.
**The albedo is not it** (`RED` is linear (0.5520, 0.0294, 0.0176), G/R 0.053). **The view transform is
not it**: AgX 0.572 / Filmic 0.634 / Standard 0.574 on one identical window. **The weathering is not
it either**: `T1_WEATHER` 1.0 / 0.35 / 0.0 → 0.572 / 0.569 / 0.567. **That switch is NEW — `dust`,
`fade` and `peel` were hard 1.0 on all four bodywork materials, so the question could not be asked** —
and it was **watched moving before the null was believed (rule 47): 4.535 % of pixels >8 levels, worst
channel 71, against F228's floor of 2.441 % / 40.** **What is left is the specular/fill path**, which is
F21's own "paint or light" question with two branches now pruned by measurement.

---
## §0.09 THE MACHINE'S VERDICT AT CLOSE OF REV 69 — every one watched print

```
bootstrap.sh              ALL 10 PASS -- but only after `pip install pillow`
verify_clone.sh           ALL 351 PASS on a clean tree, AT THE HANDOFF COMMIT
                          <- 0 FIDELITY, 351 SELF-CONSISTENCY.  NO row relaxed,
                          NO row re-based this revision
build.py T1_VERIFY=1      VERIFY: 0 fail, 0 warn at SUB=1
probe_rev70_tyre.py       NEW.  2 checked, 1 FAILED (T2, a CORRECT refusal at 1.26x
                          against a 1.25 bar).  Its CONTROL was WATCHED FAILING TWICE
                          and caught two real flaws in its own finder
probe_rev69_fitpose.py    NEW.  4 checked, 1 FAILED (P2, a CORRECT refusal:
                          0.7345 against the control's 0.9882)
gloss_compare.py          FAILS at 0.410 (bar 0.60).  Two-render floor on the
                          statistic MEASURED for the first time: 0.001
flank_compare.py          FAILS -- worst region 0.680 (i), target 0.75
probe_rev46_vw.py         12 checked, 1 FAILED -- C4 ONLY, at 0.0755 (bar 0.045).
                          READ F210/F211/F226/F234 BEFORE QUOTING ANY OF IT.
                          C6 PASSES 6 = 6 -- **ON THE RASTER.  ON THE RENDER THE
                          SAME FUNCTION READS 3 AGAINST THE PHOTOGRAPH'S 6 (F205),
                          AND REV 67 RE-MEASURED THAT ON ITS OWN FRAME (F212).**
                          A gate can be corrected, guarded, killed, swept and still
                          be measuring the wrong object -- rule 41.  RUN THE EMBLEM
                          GATES ON THE FRAME.  *(This warning was DROPPED by rev
                          69's first draft of this block and verify_clone.sh's row
                          "the brief warns C6 is a RASTER fact" CAUGHT IT.)*
visibility_budget.py      THE RANKING.  The emblem is item 9 of 16 at 3.32e4 px^2;
                          the top item is 3.83e6 px^2 -- 115x bigger
```

**AND THE STANDING WARNING, WHICH `verify_clone.sh` PRINTS ITSELF.** A green check is not evidence
about the vehicle. **Not one of those rows compares the model to a photograph** except
`flank_compare`, `gloss_compare`, `probe_rev70_tyre` and `probe_rev69_fitpose` — **and all four fail.**

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
DROPPING.** `verify_clone.sh` ends **ALL 351 PASS**: **0 FIDELITY, 351
SELF-CONSISTENCY.** *(⚠ THE REV-69 BRIEF SAID "351 PASS ... 342 SELF-CONSISTENCY" IN ONE SENTENCE —
a transcription defect carried from rev 68's re-base, caught by rev 69's outgoing audit. The two
halves must be the SAME NUMBER: every row is self-consistency and none is fidelity.)*

| gate | state MEASURED at close of rev 64 unless noted |
|---|---|
| `flank_compare.py` | **runs, FAILS.** Worst region **`i` at 0.687 of its own ceiling**; the `Senor` row scores a **DELIBERATE DEPARTURE** — F156, **EIGHT revisions un-re-based** |
| `gloss_compare.py` | **RE-MEASURED AT REV 69: runs, FAILS at 0.410** (bar 0.60). **F60/F62's "model-side lever EXHAUSTED" was measured in a FEATURELESS WHITE VOID and is now a four-row TABLE, not an assertion (F239).** The binding constraint is the ROUGHNESS, not the environment. **Two-render floor on the statistic MEASURED for the first time: 0.001** |
| `probe_rev70_tyre.py` | **NEW at rev 69 (F238).** The tyre against **the cream rim ring in its own image**, so exposure cancels; no typed radius anywhere, so it encodes no pose. **2 checked, 1 FAILED — 0.2458 against the photograph's 0.1953, i.e. 1.26× at a 1.25 bar, which its own ±20 % ceiling calls AT the bar, not a pass.** Its control was **WATCHED FAILING TWICE** |
| `probe_rev69_fitpose.py` | **NEW at rev 69 (F236).** The emblem with **the pose FITTED OUT** — the comparison F184 says the count and the elongation cannot make. **4 checked, 1 FAILED — 0.7345 against a watched control ceiling of 0.9882.** **P4 re-scores `T1_VW_TRACED` on a frame it was NOT traced from and goes RED if the trace ever wins independently** |
| **the REAR HATCH** | **NO GATE EXISTS. F163 is `RULED-rev62, NOT BUILT` and F165's angle/chord pair has never been checked by anything that runs.** §3 item 1 |
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
git rev-parse --is-shallow-repository        # <- rev 62..69 ALL arrived TRUE
for b in $(git branch -r | grep -v HEAD); do
  printf "%-52s ahead %-3s behind %s\n" "$b" \
    "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"
done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
./bootstrap.sh          # read ROW 9, and read the "N ahead / M behind" NOTE line
./verify_clone.sh       # and read its verdict block
```

> **⚠ MEASURED AT REV 69's CLOSE, AND THIS IS THE ONE THAT WILL BITE YOU:**
> **`origin/claude/nose-fixture-alignment-r68-rrqyqx` IS 25 AHEAD OF `origin/main` AND 0 BEHIND.**
> **REV 69's ENTIRE REVISION — THE TYRE FIX, BOTH NEW PROBES, F236–F240 — IS ON THAT BRANCH AND
> `origin/main` DOES NOT HAVE ONE COMMIT OF IT.** A fresh clone defaults to `main`. **If you start
> from `main` you will silently re-do a whole revision on a tree that is 25 commits stale, which is
> precisely how the rev-57b work sat stranded from rev 57 to rev 64 (F188).** Check out the branch,
> or merge it, before you read another file.

**ALSO MEASURED AT REV 69's CLOSE:** the clone arrived **SHALLOW** — the **TWELFTH running**, unshallowed
to **651 commits**; `bootstrap.sh` **FAILED 3 of 10 because PIL was missing** (`pip install pillow` fixed
it, the twelfth running); and `git diff --name-only HEAD...origin/main` was **EMPTY** — no new
photographs. **EXPECT ALL OF IT AGAIN AT REV 70.**

> **AND THE LESSON THAT COST EIGHT REVISIONS: no sentence about branch state survives the hour.
> `bootstrap.sh` row 9 outranks every sentence, INCLUDING THIS ONE.** *(It is row **9**, NOT row 10.
> Row 10 is `verify_clone.sh`. The "row 10" in every brief through rev 51 was wrong and was propagated
> for three revisions.)*

**AND MEASURE IT AGAIN BEFORE YOU FINISH.** `origin/main` moved mid-revision at rev 51 and rev 55; the
pickup figure is NOT the close figure.

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
                                         *** RE-SCORED POSE-FREE AT REV 69 AND IT
                                         STANDS, NOW WITH A MECHANISM: it scores
                                         0.8250 on ref_workshop.jpg -- THE FRAME IT
                                         WAS TRACED FROM -- and 0.6421 against the
                                         shipped 0.6671 on IMG_2073.jpeg, which it
                                         was not.  IT IS OVERFIT.  probe_rev69_
                                         fitpose.py's P4 re-checks this every run
                                         and goes RED if it ever wins independently
                                         (F237) ***
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

> **⚠ REV 69 ADDS THE ROW THIS LIST NEEDED MOST, AND IT WAS NOT NEW — IT WAS UNREAD.** The whole
> emblem was compared **POSE-FREE** for the first time (F236) and every lever above was scored against
> that residual (F237): **the six spine constants and the stroke weight TOGETHER buy 4.4 % of the
> deficit.** The conclusion — *"the ink is the right AMOUNT arranged the WRONG WAY"* — **is F104, which
> `OPEN_FINDINGS.md` has carried since rev 60 and which no revision acted on.** That is F209's shape and
> F222's shape for the THIRD time in three revisions. **CHECK THE REGISTER FOR THE FINDING BEFORE YOU
> DERIVE ANYTHING.**

**THE LIST IS SEVENTEEN ROWS.** Counted at rev 68 by an adversary, and the rev-68 brief's
cross-references (row 1 = F101, row 15 = F199) are both right.

> **A REFUTATION INHERITS ITS INSTRUMENT (rule 46). Before you accept any row here, check what
> it was measured with — and CHECK THE REGISTER FOR THE FINDING BEFORE ACCEPTING ANYTHING AS
> NEW**, which is how F139 was found sitting under F200 (F209) and how F216 was found sitting
> under F221 (F222).

---
## §3 THE WORK LIST FOR REV 70

> **THE OWNER NAMED THREE THINGS AND THEY ARE ITEMS 1–3. §0.01 IS THE RANKING. Everything below item 3
> is the standing list and is NOT this revision unless items 1–3 close early.**

1. **THE BACK OPENING — BUILD THE REAR HATCH (§0.05, F163/F165).** `RULED-rev62, NOT BUILT`, seven
   revisions. A **550 mm blade** stands where a propped panel belongs; **`TB_WIDTH` was never measured
   and its own comment says so**; the angle is **38.0° against a photographed 28.0°** and the chord
   **0.711 m against a ≥0.829 m lower bound**. Build a panel with thickness, an underside and the dark
   angled recess. **DO NOT re-open the colour — F163's own correction settles it and no brief has
   carried it.** **Add the gate in the same edit and watch it refuse at the shipped values.**
   **Then measure the dark rectangle under the blade in `out/r70_hero34r.png` before naming it.**
2. **THE EMBLEM — A NEW CONSTRUCTION, NOT ANOTHER SOLVE (§0.07, F236/F237).** All seven constants
   together buy **4.4 %** of the deficit; the trace is **overfit to its own source frame**. Every
   terminal is **forced onto the band circle** and `_on_band` normalises, so **a stroke's angle is not
   a parameter of this model.** Give the strokes free centrelines, fit against
   `probe_rev69_fitpose.fit()` **on both frames with one held out**, target **F235's spread 60.9° →
   ~28.6°**, ceiling **P1 = 0.9882**. **READ §2's SEVENTEEN REFUTED ROWS FIRST.**
3. **THE NOSE — RENDER IT, CROP IT AND LOOK (§0.06).** The geometry is built and guarded (F232). Render
   `front` at **3200×2200**, crop the nose, look. Run `probe_rev67_nose.py` and `probe_rev59_nose.py`
   **with a frame argument**. Render the control twice and publish the floor (F228). **The magnitude
   stays open with F223's bracket B ∈ [16, 76] mm — that is a CEILING, not a task.**
4. **PUT AN ADVERSARY ON THIS BRIEF (rule 15), AND *DISPATCH* IT — POINT IT AT §2's REFUTED LIST
   AGAIN.** Fourteen broke at rev 64, thirteen at rev 67, twelve at rev 68, and rev 69's audit of §2
   found its own headline sitting under F104 unread. **It has paid every revision.**
5. **F226 — RE-POINT OR REFUSE `PHOTO_E, PHOTO_N = 3.390, 7`** in `probe_rev63_ablate.py`,
   `probe_rev63_shapefit.py` and `probe_rev63_final.py`, and `probe_rev64_shear.py`'s S4. **And either
   wire F194's re-base into C8 or stop saying C8 was re-based.**
6. **THE RED'S DESATURATION — G/R 0.42–0.52 against 0.114, the largest colour error in the frame
   (F240).** Albedo, view transform and weathering are all **excluded by measurement**. What is left is
   the **specular/fill path**. This is the biggest single-colour win available.
7. **THE GLOSS — ROUGHNESS AND ENVIRONMENT TOGETHER (F239).** Never tried. Both switches now exist
   (`T1_BODY_RGH`, `T1_REFLENV`, `T1_BODY_COAT`).
8. **F156 — `flank_compare`'s `Senor` row scores a DELIBERATE DEPARTURE. NINE revisions.**
9. **TRIAGE IS DONE — `ROADMAP_rev68.md` holds it.** `REMAINING_WORK_rev61.md` is **NOT deleted**
   (rule 16) and points at it.
10. **THE SURVIVING PANEL ITEMS**, untouched for nine revisions: the glass is a flat slab (0.5 % sd
    against the photograph's 12.8 %); **the tyres have no tread and no sidewall lettering** — the
    LIGHTNESS half is now fixed (F238), the GEOMETRY half is not; the tail is a box where the real one
    is a barrel; every shut line is a 1-px ink stroke with no leading-edge highlight; the galley is
    monochrome; the counter is a floating slab.
11. **F143 — TWO LOUDSPEAKERS STAND ON THE ROOF AND ARE UNMODELLED.** 57 revisions.
12. **THE INHERITED CLUSTER** — F14 (**seventeen** revisions un-re-measured), F15, F10, F20.
13. **`delivery/READ_ME_FIRST.txt` LISTS THE MODEL'S KNOWN DEFECTS TO HIM.** It does not yet mention
    F222's flat bumper, F232's fix, F238's tyre, or the rear hatch.

**RANKING NOTE — AND THE RULE IT CARRIES IS NOT DROPPED.**
**RANK BY PIXELS OF THE DELIVERY FRAME** — `python3 visibility_budget.py 3840 out/r70_hero34f.png` —
**and PASS IT A `.png`**, or it globs `out/` by mtime and reproduces F132. **MEASURED AT REV 69: the
emblem is item 9 of 16 at 3.32e4 px², and the top item is 3.83e6 px² — 115× bigger.**
**But he has overridden the ranking four times, and the owner outranks it — which is exactly what
§0.01 is.**

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

> **53. NEW AT REV 69 — A REFUTATION MEASURED IN A DEGENERATE ENVIRONMENT IS NOT A REFUTATION.**
> F54's clearcoat and F60's roughness were each tested in a **FEATURELESS WHITE VOID**, where a mirror
> reflects the same white in every direction and can therefore only VEIL — a highlight needs something
> bright NEXT TO something dark. Eight revisions then carried *"the model-side lever is EXHAUSTED"* as
> though it were a property of the PAINT. **Before accepting that a lever is dead, check that the scene
> could have shown it working.** (F239. This is rule 46 — a refutation inherits its instrument — applied
> to the SCENE rather than to the gate.)

> **54. NEW AT REV 69 — A CONSTRUCTION THAT CANNOT EXPRESS THE DEFECT CANNOT BE TUNED INTO EXPRESSING
> IT, AND NO AMOUNT OF SOLVING WILL SAY SO.** The emblem's six spine constants and its stroke weight
> were solved, swept and re-solved for eight revisions against a defect that is **the strokes' ANGLES**
> — and `_spines()` forces every terminal onto the band circle while `_on_band` normalises, so each pair
> contributes only a DIRECTION and an angle is **not a free parameter of the model at all**. Fitting all
> seven moves the pose-free shape by **4.4 %**. **When a lever is measured inert, ask whether the
> quantity you are trying to move EXISTS in the parameterisation before you widen the search.** (F237.)
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
python3 probe_rev69_fitpose.py               # NEW at rev 69 -- THE EMBLEM WITH THE POSE
                                             # FITTED OUT.  Control ceiling 0.9882.  Its P4
                                             # re-scores T1_VW_TRACED on a frame it was NOT
                                             # traced from, in a FRESH process (F236/F237)
python3 probe_rev70_tyre.py out/r70_side.png # NEW at rev 69 -- the tyre against the cream
                                             # rim ring in its own image.  PASS IT A FRAME:
                                             # bare, the render rows do not run (F238)
python3 probe_rev69_emblem.py out/r69_front.png   # **PASS IT A FRAME** -- the RENDER
                                             # side of F205, which existed in no file
                                             # before rev 69.  Bare, it SAYS the render
                                             # rows did not run (F233)
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

**NEW SWITCHES AT REV 69, ALL MEASUREMENT-ONLY:** **`T1_TYRE_FILM`** (the tyre's road film; **SHIPS at
0.15**, `=1.0` restores the old film — the ONE default rev 69 changed), **`T1_WEATHER`** (the bodywork's
dust/wear/fade/peel, which had **no ablation at all**; ships 1.0, **watched moving at 4.535 % of pixels
>8 levels against F228's 2.441 % floor**), **`T1_REFLENV`** (the world's structure for GLOSSY rays only;
**ships 0.0 = OFF**, and that is a RESULT, not a placeholder — F239), **`T1_BODY_COAT` / `T1_BODY_COATRGH`**
(**ship at the shipped 0.02 / 0.300**; at 0.55 / 0.045 they buy +44 % of headroom and cost G/R
0.422 → 0.520, so rule 44 keeps them off).

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

**Rev 69 added F236–F240** — of which **F236's row was CITED BY A COMMIT MESSAGE AND NEVER WRITTEN**,
and was only found because the next finding needed to cite it. **That is rule 16's failure mode inside
the register itself: the instrument shipped, the number was quoted to the owner, and the carrier went a
whole commit without it.** Rev 69 also **corrected F224** (the spine pairs are DIRECTIONS — `_on_band`
normalises — so the clip it complained about was never a geometric bound) and **re-based nothing**.
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
## §9 THE HORIZON BEYOND REV 70

**CARRIER: re-rank it, do not rewrite it, and say what moved.**

**WHAT REV 69 LEARNED LAST, WHICH RE-RANKS THE REST.** **The owner said *"it's been weeks, and a lot of
compute, this is unacceptable"*, and he was right in a way the ledger can show: rev 69 built FIVE
instruments and shipped ONE visual change.** Every one of those instruments was sound and four of them
returned NULL or NEGATIVE results. **A revision that only measures is a revision the owner cannot see.**
**Budget the next one the other way round: build first, instrument the thing you built.**

**WHAT MOVED AT REV 69.** The tyre's road film shipped (F238, 1.90× → 1.26×). The emblem was compared
**pose-free** for the first time and every lever it has was measured against that residual and found
exhausted (F236/F237); the traced pressing was shown **overfit to its own source frame**, and
`IMG_2073.jpeg` was established as the emblem's **second frame**. F62's *"lever exhausted"* was shown to
have been measured in a void, and re-measured to a table (F239). Two causes of the red's desaturation
were closed (F240). **What did NOT move: the back opening, the emblem's geometry, C4, and the nose.**

**WHAT MOVED AT REV 68.** F217 cleared; the nose's photographic target was refuted and retargeted onto
the BUMPER (F222/F223); five instruments were found reporting things that are not measurements.
**WHAT MOVED AT REV 67.** The nose got an instrument for the first time (F207); the frames were found to
carry their own EXIF (F219); the register caught itself (F209).
**WHAT MOVED AT REV 66.** The emblem's stroke weight and the arc-cut terminal shipped; three emblem
instruments were found mis-targeted.
**WHAT MOVED AT REV 65.** The badge's ring was fitted as an ELLIPSE; the reach was measured live off the
mesh. *(⚠ THIS LINE WAS DROPPED BY REV 69's FIRST DRAFT OF THIS SECTION AND `audit_adversary.py` CAUGHT
IT — the question "is the ring-ellipse fit still named as the emblem's close?" BROKE. §9 is a CARRIER:
re-rank it, do not rewrite it. F185 stands: the badge's ring is a CIRCLE on the real object, so its
image gives the homography outright, and **`probe_rev69_fitpose.py` is the first thing in this project
to actually use that fact** — it fits the pose rather than assuming it.)*

| horizon | the work | why |
|---|---|---|
| **next** | **THE BACK OPENING (§3 item 1, F163/F165)** | **HIS WORDS, and `RULED-rev62, NOT BUILT` for seven revisions.** The one item that is pure un-built geometry with the ruling already given |
| **next** | **THE EMBLEM'S NEW CONSTRUCTION (§3 item 2, F237)** | **HIS WORDS, and his NINTH report.** The route is established by elimination and the instrument is built |
| **next** | **THE NOSE, RENDERED AND LOOKED AT (§3 item 3)** | **HIS WORDS.** The geometry is done; the LOOK is the missing step, and it is rule 1 |
| **next** | **AN ADVERSARY, DISPATCHED, ON §2's REFUTED LIST** | Fourteen at rev 64, thirteen at rev 67, twelve at rev 68 |
| **near** | **THE RED's G/R — 0.42–0.52 against 0.114 (F240)** | The largest colour error in the frame, with two branches now pruned |
| **near** | **GLOSS: roughness AND environment together (F239)** | The one pairing never tried |
| **near** | **F156 — the `Senor` gate row scores a DEPARTURE** | NINE revisions unacted |
| **near** | **Glass, the tyres' TREAD, the tail's barrel, the shut lines** | Untouched for nine revisions |
| **near** | **F143 — the roof loudspeakers** | Unmodelled since rev 12 — 57 revisions |
| **LOWERED** | **F192 — prove the large-format chain** | **He ruled the MODEL comes first (F193).** |
| **then** | **F10–F14 — the galley cluster** | F14 is SEVENTEEN revisions inherited |
| **CEILED** | **F153; F168; F183; F195; F231; F44/F60/F62 gloss; F83; F67; F142; F148** | **F62 is now a TABLE, not an assertion — see F239** |
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
