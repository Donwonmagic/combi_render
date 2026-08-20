# LEDGER — rev 47

**Everything this revision measured, changed, refuted, retracted and corrected.** Figures here were
watched print unless a line says otherwise. **Where this ledger and the machine disagree, the machine
is right.**

---

## §0. THE OWNER'S REPORTS THIS REVISION

| his words | verdict | where |
|---|---|---|
| *(rev 46 standing)* "señor Tacombi still isn't clearer" | **BLUR HALF FIXED.** Edge ratio 0.0924 → 0.0062. Contrast half still gated on W6. | §2 |
| *(rev 46 standing)* "the bottom word does not collide with the top one either" | **COLLISION CLEARED** (1110 → 0 px) **BUT HE REPEATED IT.** Not closed. | §3 |
| **NEW** "I only meant to use that bus as a reference for the level of detail" | **RECORDED.** `bus_model_ref.JPG` is a FIDELITY BAR, not a vehicle reference. | §1 |
| **NEW** "Use the clarity in the workshop photo too to inform you" | **RECORDED and used.** `ref_workshop.jpg` is a second frame of the flank script. | §1, §2 |
| **NEW** "we're going to need the trunk open like it's in service" | **NOT STARTED.** New requirement, no geometry investigated beyond a grep. | §5 |
| **NEW** "It still does not read as two separate words" | **HIS REPEAT — the gap I opened is too small. OPEN.** | §3 |

> **RULE 21 FIRED AGAIN, AND IT FIRED ON ME.** I opened the word gap to 0 shared pixels and 11.1 %
> of the cap height, measured it, looked at it, and shipped it. He looked at the same picture and
> said it still does not read as two words. **A clearance measurement is not a legibility
> measurement, and I substituted one for the other.** See §3.

---

## §1. CORRECTIONS TO THE REV-47 BRIEF — the machine disagreed three times

### 1a. THE BRANCH INSTRUCTION WAS STALE, AND OBEYING IT LITERALLY LOSES A FILE

`NEXT_CONTEXT_PROMPT_rev47.md` and `PASTE_INTO_CLAUDE_CODE.txt` both say rev 46's **five commits are
on `claude/new-session-3tof54` and are NOT on main**, and instruct the next context to expect
`git rev-list --count origin/main..HEAD` **= 5**.

**Measured at pickup: 1, not 5.** PR #5 merged those five commits into `main` before this revision
started. Worse, the instruction is now **inverted**: `main` carried a commit the named branch did
**not** —

```
a166304  Add files via upload   (Donwonmagic, 2026-08-20 13:10 EDT)   bus_model_ref.JPG
```

— an **owner upload**. A context that checked out `claude/new-session-3tof54` and worked from it, as
instructed, would have silently missed owner-supplied material. Merged in at `44ba526`.

**The rule that produced the stale instruction is still right** (§10.113.5, a revision that is not
merged did not happen). **The instruction derived from it went out of date the moment the PR
merged.** An ahead-count written into prose is a fact with an expiry date. **Rev 48: verify the
merge state, do not transcribe it.**

### 1b. THE CANVAS WIDTH IN §1 IS WRONG — 3480, not 3552

Both the brief §1 and `LEDGER_rev46.md` §3 say `Canvas` draws at **"3552 px across"**.
`MW, MH = 290, 114` and `SS = 12`, so the canvas is **`MW * SS` = 3480 px**. 3552 would need
`MW = 296`. The ink spans 271 mask px → **3252 px** drawn. Everything the brief *concluded* from the
figure is correct — the upscale really is 15.11×, the fixed one really is 1.260× — so this is a
transcription error in a load-bearing paragraph, not a reasoning error. **Corrected.**

### 1c. WHAT THE BRIEF GOT RIGHT, RE-MEASURED RATHER THAN ASSUMED

| brief / ledger rev 46 | machine, rev 47 | |
|---|---|---|
| ink is 271 px across in mask space | x 5–275, **271 px** | ✔ |
| upscale 15.1× | **15.11×** | ✔ |
| post-fix 1.26× | **1.260×** | ✔ |
| "0.215 of ink px in the 0.1–0.9 band" | **0.2154** | ✔ |
| "100%" and "Calidad" share **1110 px** | **1110** | ✔ |
| both word bboxes, 4 dp | reproduced to 4 dp | ✔ |
| anchors (0.150, 0.395) / (0.180, 0.645) | present in `cal_gen` | ✔ |
| `cal_gen` refuses type >0.004 off centre | present, fires | ✔ |
| `bulge = 0.019` is the only forward bulge | not independently re-checked this revision | — |

### 1d. `bus_model_ref.JPG` — EXPLAINED BY HIM, AND IT IS NOT A T1

2000 × 1125, an American yellow school bus, a studio 3-D product render, not a photograph and not a
VW. **He has said what it is for: "I only meant to use that bus as a reference for the level of
detail."** It is a **FIDELITY BAR**, not a shape reference. Nothing about the T1's geometry, paint or
proportions may be taken from it. What it does say is the standard: crisp panel edges, small features
carried as **real geometry with depth** rather than as paint — its nose louvres are modelled slots
that self-shadow. **That is the bar §5's missing rear vents have to meet**, and it is the reason
painting louvres into a decal was wrong three times over.

---

## §2. W3 — the script was BLURRED, and the blur was arithmetic *(FIXED, with its ceiling)*

**Cause confirmed exactly as rev 46 drafted it.** `Canvas` draws at `SS = 12`; `alpha()` reduced that
to mask space, **271 px of ink**; `main()` then LANCZOS-magnified those 271 px to `OUT_W = 4096`.

> **THE SHARPEST WAY TO SAY IT.** The photograph's script in `ref_side.jpg` is **also 271 px wide**.
> The shipped 4096-px texture carried **exactly as much real information as the JPEG crop it was
> traced from**, and not one bit more.

**Fix — rev 46's three steps, applied unchanged.** `Canvas.alpha_box(k)`; `alpha()` **is**
`alpha_box(SS)`; `main()` finds the bbox in mask space as before but crops and resizes the **drawn**
raster, 3252 px → 4096.

**MASK SPACE IS BIT-IDENTICAL.** `build()` `4a6f4e8cd0489fa1`, `senor_only()` `82d6cf56dd660b47`,
before and after. No mask-space figure in this project moved.

| | rev 46 | rev 47 |
|---|---|---|
| 10–90 % alpha edge width | 14.077 px | **0.941 px** |
| mean stroke width | 152.37 px | 151.21 px |
| **edge / stroke** | **0.0924** | **0.0062** |
| soft fraction | 0.2154 | 0.0160 |
| upscale | 15.11× | 1.260× |

**THE CEILING, STATED.** 0.941 px is **at the instrument's floor** — an ideal antialiased edge at
this resolution measures **1.000 px** on the same estimator. The correct claim is that the residual
blur is **≤ ~1 px and not resolvable by this instrument**. It is **not** a claim that the texture is
perfect, and nobody should quote 0.0062 as an accuracy.

**STILL WRONG:** *Señor* is legible **with its tilde** in **both** photographs and is still a
formless blob in the build. That is the **contrast** half, `TARNISH_K`'s declared departure, and it
**retires itself when W6 lands**. W6 is blocked on the owner.

### The instrument, and the two things it killed

`probe_rev47_sharp.py` — **9 controls, 0 FAILED.** Calibrated *before* it was believed (rule 20,
rule 22): C1 sharp edge reads 1.000 px; C2 recovers a built 400-px stroke to 0.25 %; C3 tracks a
**known** Gaussian blur to 2.5 %; C3b records the sub-10-px floor; **C4 KILL** sharp vs blurred
differ 39×; C5 the ratio is scale-invariant 4096 vs 2048; **C6 WATCHED-FAIL**; **C7 WATCHED-FAIL**;
C8 stroke weight matches the photograph.

**KILL 1 — my own calibration harness was wrong, and its own controls said so.** The first harness
drew 60-px bars and blurred them to σ = 40. At σ = 20 the alpha at a bar's **centre** is 0.866 — it
never reaches 0.9 — so the whole bar counted as "band" and the estimator over-reported by 26 %, then
44 %. **That is the synthetic violating the estimator's validity regime (edge ≪ stroke), not the
estimator failing.** The harness was fixed and the thresholds were **not** loosened; **C6 now watches
the break happen**, so the limit is demonstrated rather than believed.

**KILL 2 — "the built strokes are too fat" was refuted rather than shipped.** With the blur gone the
strokes *look* bloated beside the photograph. Measured at 4096 px they are 0.84× the photograph:
**7.9 σ**, a publishable-looking defect. **C7 shows the EDT stroke estimator carries a 16.6 %
resolution bias across that 15× gap**, so that number is about the instrument. At the photograph's
own 271 px: **built 0.04317 vs photo 0.04414 ± 0.00090 — 1.1 σ, agreement.** This is the same
illusion rev 46 had about the VW glyph's strokes, and it evaporates the same way. **SPEC 10.110.8, on
the resolution axis.**

**`ref_workshop.jpg` corroborates the bar independently**, at his instruction. It carries the same
flank script on a green vehicle: hard edges, **open** counters in the a/c/o spirals, *Señor* legible
**with its tilde**. Its script is ~145 px wide and foreshortened, so it is **weaker than
`ref_side.jpg` for absolute metrics** and is used here only as corroboration.

---

## §3. W4 — the words no longer collide, and that was not the defect he reported

**Reproduced before touching anything**, to four decimals:

```
  100%     x 0.3033-0.6381  y 0.3390-0.5716    1110 shared px
  Calidad  x 0.3304-0.7660  y 0.5381-0.7890    bbox overlap 0.0337 (14.5% of cap)
```

**After:** `LINE_GAP = 0.26` of the "100 %" cap height → **0 shared pixels**, clear gap **0.0258** of
canvas height = **11.1 %** of cap height. W1 guard still exact at (+0.0000, −0.0001).

### HE LOOKED AT IT AND SAID IT STILL DOES NOT READ AS TWO WORDS

**HIS REPEAT IS A MEASUREMENT, AND THE MISSING AXIS IS MINE.** I proved **clearance** — that no
pixel is shared — and reported it as though it answered **legibility**. They are different
quantities. Two lines of type can share zero pixels and still read as one word: the words are set at
−19.7° and **staggered**, "100 %" up-left and "Calidad" down-right, so the `%` sits almost directly
above the `l`/`i` of *Calidad* and the eye joins them. **Zero shared pixels was necessary and it was
not sufficient.**

**OPEN. `LINE_GAP` must grow, and possibly the horizontal stagger must shrink.** Neither magnitude is
measurable from what we hold — see §4.

### THE MAGNITUDE IS DECLARED NOT-A-MEASUREMENT, IN THE SOURCE

**Rule 6: an ordinal fact licenses a SIGN, never a SHAPE.** `ref_playa_34.png` supports only that the
two words are *separate*. **A de-rotated row profile of the type inside the burst is one broad smear
with no trough between the words** — at 4–6 px per word the bright/low-saturation rule that finds the
type also finds the cream, **the same estimator failure `LEDGER_rev46` §1 retracted a published
number for**. `LINE_GAP` therefore carries `NOT MEASURED` in its own comment, is expressed as a
fraction of the cap height rather than of the canvas, and `verify_clone` now **requires** that
declaration to stay present.

### THE TRAP THE BRIEF NAMED IS REMOVED, NOT STEPPED AROUND

Brief §4 warns that opening the gap moves the block's centroid and that `TYPE_PRE_CENTROID` /
`TYPE_SHIFT` must be re-derived **in the same edit** or the W1 guard fires. **Re-deriving a frozen
figure by hand leaves the trap armed for the next revision.** `TYPE_SHIFT` is now **computed at
generation time** from the centroid of the actual laid-out type. rev 46's frozen (0.3735, 0.6309) was
correct only for rev 46's spacing; this layout prints **(0.3735, 0.6607)** and derives its own shift.
**SPEC 10.25.**

### AN ESTIMATOR DISCARDED FOR SAYING SOMETHING PLAUSIBLE

A containment check reported **"42 % of type pixels outside the burst"** — alarming, and wrong. The
type meets the burst boundary, so its counters are not enclosed regions and `binary_fill_holes`
cannot close them. **The rendered decal shows the type inside the burst on every side.** The figure
is quoted nowhere except here, as a caught error.

---

## §4. WHY THE DECAL PHOTOGRAPH IS NOW THE BINDING CONSTRAINT

Two of his open reports — **the word gap** and **"the lettering looks off"** — are both blocked on
the same missing frame, and `ref_playa_34.png` is the only frame in the set that shows this decal at
all. **The burst spans 23 × 39 px; the letters are 4–6 px tall.** Nothing about a typeface, a word
gap or a spike count is measurable there, and this revision declined to invent any of it.

**This is now the single highest-value missing input in the project.** It unblocks two standing owner
reports at once.

---

## §5. NEW REQUIREMENT — "the trunk open like it's in service" *(NOT STARTED)*

Recorded, not investigated beyond a grep. What is known:

* `t1_shell.engine_lid_gap()` (line 994) cuts a lid **gap** into the body — a seam, not an openable part.
* `t1_shell.roof_lids()` (line 1241) builds the **roof** lids, which **are** modelled open and served
  by `lid_gen.py`; `audit.py` §87 records `lid_strut0` spanning z 1.8994–3.0169, i.e. the roof lids
  are already in their **open, serving** pose.
* `lid_gen.py` §1 states the settled topology: **"There are two roof lids plus a trunk lid."**

**So the roof lids open and the trunk lid appears to exist only as a seam.** That is the shape of the
job, not its answer — **rev 48 must confirm it against the build before believing it** (§9: the sign
props' inset was "fixed" wrongly by two contexts that trusted the source over the build).

**Unmeasured and needed:** the hinge axis and side, the open angle, whether it is strut-held or
counterbalanced, and what the inner face carries. **No frame we hold shows the trunk open.** This is
a new `PHOTOS_WANTED` entry.

---

## §6. `verify_clone.sh` — THREE ROWS RE-BASED, ONE GUARD RESTATED

**All three failures were mine and none was a defect.** Re-based with the reason recorded *in the
script*; **no tolerance widened, no row deleted**.

* `tex/senor.png` `411ade90` → `92ff3855` — SPEC 10.121, mask space bit-identical.
* `tex/calidad.png` `d8c27a4a` → `ac9d1590` — W4.
* **`calidad TYPE_SHIFT is DERIVED` — rationale kept, shape replaced (rule 5).** The row grepped for
  one literal line expressing `TYPE_SHIFT` against a **frozen** centroid, which satisfies "derived"
  only for rev 46's spacing. Replaced by **two strictly stronger rows** — the runtime derivation must
  be present **and** the frozen literal must be gone — plus a third requiring `LINE_GAP` to keep
  declaring itself unmeasured, so a placeholder cannot be quietly promoted to a measurement.

**`verify_clone.sh` ALL 85 PASS** (83 rows at rev 46; two added).

---

## §7. THE NOSE-ANCHOR TASK REV 46 DISPATCHED — IT DOES NOT EXIST

**Checked, so that rev 48 does not check again.** A sweep over every commit on every ref, every
tracked and untracked file, `/tmp`, and the content of every `.md`/`.json`/`.py` finds **no result
from that task**. Every hit is a restatement of the open problem. The rev-47 brief, written *after*
rev 46 closed, still says "look for a report; if there is none, run it yourself" — **which is itself
proof it never landed.**

**And a pixel budget, which is the part rev 45 skipped.** Only two frames put the nose face in front
of the camera at more than 100 px:

| frame | nose face | the problem with it |
|---|---|---|
| `ref_workshop.jpg` 1200×824 | **~240 px** | green/cream under **flat overhead fluorescent** — almost no directional falloff for a shading method. **Its silhouette is the sharpest in the set: this is method 2's frame.** |
| `ref_nolita_front34.jpg` 700×467 | ~165 px | red channel **clipped** over the nose, near headlamp **blooming** across ~78 px, a child's head occludes the lower quarter |
| everything else | ≤110 px | ~15 mm per pixel or worse |

**Do not read this as "the measurement is impossible."** The quantity in dispute is how far the
*real* nose bulges, which is unknown and may be several times the built 14.3 mm. **Method 2 —
silhouette corner-wrap on `ref_workshop.jpg` — is the live one**, and it is the method that does not
care about lighting.

---

## §8. THE STATE OF THE MACHINE

```
bootstrap.sh      ALL 10 PASS   (the pip install bpy==4.5.3 branch, never
                  exercised before rev 47, RAN CLEAN on a cold container)
verify_clone.sh   ALL 85 PASS   (83 at rev 46)
build             T1_SUB=1, VERIFY: 0 fail, 0 warn   (after W3 and after W4)
probe_rev47_sharp 9 checked, 0 FAILED   (C4 KILL; C6 and C7 WATCHED-FAIL)
render            out/r47_side.png  1600x1100 96spp  3m38s
box               4 cores, 15 GB RAM.  build T1_SUB=1 ~20s.  script_gen ~22s.
                  cal_gen ~48s.  side render 1600x1100 96spp ~3m40s.
branch            claude/combi-render-rev46-t8vhpm
```

**A DISPATCHED TASK THAT HAD NOT RETURNED WHEN THIS WAS WRITTEN.** An adversarial agent was set on
the rev-47 brief to refute it (claim sets A–D, including re-running every probe's own summary line).
**It had not reported when this ledger was recorded. Do not assume it succeeded.** This is exactly
what rev 46 did with the nose task, and §7 is what that cost. **The claims it was sent to check are
the ones in §1c marked ✔ — those I verified myself, by hand, and they stand on their own.** The one
row it was to check that I did **not** verify independently is `bulge = 0.019` being the only forward
bulge constant.

---

## §9. UNCHANGED AND STILL BLOCKED ON HIM

* **W5 — the sign board.** The build paints a flower mural with menu strips; every frame we hold
  shows a hand-chalked **blackboard**. **Nobody has ever asked him which he wants.** Still true.
* **W6 — the paint and the studio.** Body red G/R 0.455 built vs 0.223 ± 0.066 photographed
  (**3.5 σ**); hubcap red 3.4 σ; cream right to 0.4 σ. **ONE finding, not three.** ~Half the excess
  is the white cyclorama's own specular. **His call**, and **it gates the rest of W3.**

---

## §10. REV 47b — HE REPEATED IT, HE SENT A BETTER FRAME, AND THE GAP BECAME MEASURABLE

**He looked at §3's fix and said: "It still does not read as two separate words."** He was right, and
§3 already records why: **I proved CLEARANCE and reported it as LEGIBILITY.**

**Then he sent `IMG_2073.jpeg` (1400 × 933), and it changes several things at once.** It is the best
frame in the project by a wide margin. It shows a green/cream T1 **in service**, roof lids **open**,
and it resolves four things no previous frame could.

### 10a. THE WORD GAP — measured, and carried as a RATIO

`ref_playa_34.png` shows this decal at 23 × 39 px, which is why rev 46 refused to measure it and rev
47 shipped a placeholder. **`IMG_2073.jpeg` shows it at 44 × 61 px** and the two words separate
cleanly under a mask.

```
    photographed gap   0.244 of cap height
    built gap          0.149 of cap height    <- THE SAME estimator, the same scale
    ratio              1.64x       ->   LINE_GAP 0.26 -> 0.43
```

**THE RATIO IS QUOTED AND THE ABSOLUTE IS NOT, DELIBERATELY.** `probe_rev47_gap.py` C1 runs the
estimator on the **built** decal downsampled to the photograph's own size, where the answer is known
by construction: it reads **0.149 against a built 0.111**, a **+34 % absolute bias** from the angle
sweep. That bias **divides out of a ratio** and does not divide out of a reading. Rule 14, and the
same cancellation argument as SPEC 10.107.2.

`probe_rev47_gap.py` — **3 controls, 0 FAILED.** C1 recovers the built gap at the photograph's scale;
C2 recovers a wide synthetic gap; **C3 KILL — words that TOUCH produce no two-band split, so the
estimator refuses rather than inventing a gap.** Without C3 an estimator that always finds two bands
would have "confirmed" the fix at `LINE_GAP` 0.26 and been blind.

**A first attempt was discarded rather than published.** It took the type mask's **principal axis**
as the reading angle and reported a **0.75 px cap height at 102°**. Two stacked words make a roughly
square block whose principal axis means nothing. The angle is now found by **sweeping** it.

### 10b. FOUR NEW DEFECTS IN THE DECAL, VISIBLE ONLY NOW *(NOT FIXED — rev 48)*

Beside `IMG_2073` at matched magnification, all four were invisible at 23 × 39 px:

1. **The spikes are wrong.** The photograph has **many short, fine, near-uniform needle spikes** on a
   nearly circular core. The build has **~20 long, broad, irregular** spikes. Different character,
   not a different tuning.
2. **The burst colour is wrong.** The photograph is a fairly **uniform deep crimson**. The build runs
   a strong **RED → ORANGE → YELLOW** gradient. There is little or no orange in the photograph.
3. **The stars are wrong.** The photograph has **several small magenta stars scattered around the
   decal, outside the burst**. The build has **one** pink star to the left.
4. **The type fills too much of the burst.** In the photograph the type sits in the middle with a
   clear red margin all round; in the build it nearly touches the spikes.

### 10c. THE VENT SLATS — the rev-46 ledger's colour reading is CORRECTED

`LEDGER_rev46.md` §5 says the slats "are **dark grey** in the photograph". **In `IMG_2073` they are
body colour** — green, the same paint as the panel — and they read dark only because **each pressed
slot self-shadows**. The rev-46 reading came from a frame where the shadow was all that survived.

**This strengthens rather than weakens rev 46's conclusion.** A louvre whose darkness *is* its
self-shadow is precisely a thing that cannot be painted into a texture, and it is exactly the
standard the owner set with the school-bus render.

**Measured:** the shadow lines are **regularly spaced at 8.02 ± 0.42 native px** (5 % scatter) on the
rear flank panel. **THE COUNT IS NOT SETTLED and is not published**: a bounded detector found 6 in a
50-px-tall crop that may not span the whole panel, while reading the magnified crop by eye suggests
~10. The pitch is a real measurement; the count is not. **Rev 48: bound the panel first, then count.**

### 10d. THE LIDS OPEN "LIKE IT'S IN SERVICE" — the reference now exists

His new requirement (§5) has a frame. `IMG_2073` shows the vehicle **in service** with the roof lids
raised on visible struts/cables and lit strip lighting along the lid edge. **This is the pose he
wants.** §5's open question — whether the *trunk* lid is a separate openable part or only a seam —
is unchanged and still must be confirmed against the build, not the source.

### 10e. `verify_clone.sh` — a row went red BECAUSE IT WORKED, twice

* `calidad LINE_GAP is declared UNMEASURED` fired the moment `LINE_GAP` became measured. **That is
  the row doing its job.** It is **restated, not deleted**: the source must now cite
  `probe_rev47_gap` **and** name `IMG_2073`, so `LINE_GAP` cannot be retuned by eye without deleting
  a reference to the probe and the frame it came from.
* Those provenance rows were first written with `grep -c` and went red at **"got 2, want 1"** because
  the provenance is cited on two lines — **a cry-wolf false positive, the same failure mode
  `bootstrap.sh`'s stranded-branch row had to fix once.** Changed to a presence test.

**`verify_clone.sh` ALL 86 PASS.**
