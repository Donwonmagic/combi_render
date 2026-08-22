# LEDGER — rev 55

Every figure below was printed by a script in this tree during this revision. Where a figure is
inherited it says so. Where an instrument was wrong, the retraction is in the SOURCE as well as
here (rule 15).

---

## §0. AT PICKUP, MEASURED — NOT TRANSCRIBED

```
HEAD  claude/new-session-4uh2wh  22ff90b   0 ahead / 0 behind origin/main
every remote branch                        0 ahead
git diff --name-only HEAD...origin/main    (empty -- no photographs arrived)
./bootstrap.sh                             ALL 10 PASS   (row 9 IS the branch check)
./verify_clone.sh                          ALL 173 PASS
```

**Rev 54 WAS merged, through PR #11.** The rev-55 brief offered two shapes and said "measure
which": this is the first — merged, HEAD level with `main`. `fetch --prune` printed
`- [deleted] (none) -> origin/claude/new-session-4uh2wh`, so the DESIGNATED branch's remote copy
has now been deleted a **fifth** time in the rev-51..55 series. Row 9 passed because HEAD carries
everything.

`out/` started empty, as the brief said. Three renders were made before any probe that reads a
frame was quoted: `r55_side` 1600×1100, `r55c_side` 1248×858, `r55_hero` 1600×1100.

---

## §1. ITEM A — ANSWERED, AND IT EXONERATES THE ARTWORK

### §1.1 THE QUESTION HAD A FALSE PREMISE, AND THE PAINTED WINDOW IS WHAT SHOWED IT

The brief's item A: *"Measure the CREAM either side of the ink in the same two frames, through one
painted window."*

**THERE IS NO CREAM EITHER SIDE OF THAT INK.** The flank lockup is silver on the **RED** body; the
cream band is above the belt line, ~400 mm up and outside both crops. `flank_compare.py`'s own
docstring had already said so in passing — the render's `Senor` reads (179, 90, 78) *"against a
ground endmember of (194, 87, 74)"*, which is red — and one look at the crop settles it
(`probe_scratch/rev55_A_refcrop_x4.png`).

The control used instead is the **RED ground hugging the ink**, which is the stronger control:
same panel, same paint, same local lighting, no second registration.

### §1.2 THE WINDOW

An annulus around **each frame's own ink**, at a **matched physical standoff**, so neither window
is placed by hand and both sides are the same rule. Three bands, because if the answer moves with
the band then the window is the measurement:

| | 20–40 mm | 40–70 mm | 70–120 mm |
|---|---|---|---|
| reference mean | (147.9, 16.8, 7.0) | (142.7, 15.1, 5.9) | (134.0, 14.4, 5.5) |
| reference G/R | 0.114 | 0.106 | 0.107 |
| render mean | (193.9, 89.5, 77.3) | (190.9, 88.6, 76.7) | (185.5, 85.3, 73.8) |
| render G/R | 0.462 | 0.464 | 0.460 |

Standoff floor is set by the reference's own PSF (FWHM 3.98 px = 19.4 mm), so 20 mm is one FWHM
and 40 mm is two. Enclosed ground — the letter counters — is dropped by a **flood fill from the
border**, geometry rather than a threshold, because ground surrounded by ink carries the silver's
halo from every side. Median is printed beside mean so no outlier threshold has to be invented.

**PAINTED AND LOOKED AT BEFORE IT PRODUCED A NUMBER**: `probe_scratch/rev55_fc_ground.png`, both
frames at matched mm/px. Both annuli sit on paint in both frames; no gold rosette and no dark
scroll got in. The two reds differ visibly by eye, which is what the G/R column says.

### §1.3 THE ANSWER

Raw offsets first, which is all the brief had:

```
INK    render - reference  (+41.3, +38.6, +36.2) DN
GROUND render - reference  (+46.0, +72.6, +70.4) DN
the ground carries 171 % of the ink's own offset (luma +66.8 DN against +39.0 DN)
```

But two DN means from two frames differ by their **exposure** and their **illuminant** before they
differ by anything about the vehicle. The statistic that cancels both is the ink divided by its
own ground, in the same frame:

| | R | G | B |
|---|---|---|---|
| photograph | **0.857** | 7.045 | 17.527 |
| render | **0.867** | 1.757 | 2.048 |

**The red channel agrees to 1.1 %, against the reference ink's own R-channel spread of 10.7 %.**

**THE INK IS NOT PAINTED LIGHT RELATIVE TO THE PAINT IT SITS ON. DO NOT TOUCH AN INK CONSTANT.**
The whole +41 DN is the frame, not the artwork. Every other flank item was blocked on this and is
now unblocked.

### §1.4 WATCHED FAILING, BOTH HALVES, ON A CLEAN TREE

`T1_FC_INKGAIN` adds DN to the **render's ink only**, leaving its ground untouched — exactly the
"the artwork is painted too light" case.

| | shipped | `T1_FC_INKGAIN=30` |
|---|---|---|
| render ink / its ground, R | 0.867 | **1.022** |
| disagreement with the photograph | **1.1 %** | **19.2 %** |
| the printed verdict | "NOT painted light" | **"the ink IS off relative to its own ground"** |

**THE ABLATION CAUGHT MY OWN INSTRUMENT.** The first version printed *"the ink is NOT painted
light"* as a **constant string**, and said it at 19.2 % too. `cream_rms.py` had already earned that
rule — *"a conclusion that cannot fail is not a measurement"* — and I re-earned it. The verdict is
derived now, against the reference ink's own spread rather than a bar I liked.

### §1.5 THE CEILING, AND IT IS HARD

The red's hue gap is real and large — **G/R 0.114 in the photograph against 0.462 in the render**,
B/R 0.047 against 0.399 — and it **cannot be split between paint and illuminant with what we
hold.** The only near-neutral surface in the crop is the silver, and `script_gen.SILVER_CHROMA =
(127.4, 124.9, 130.0)` is *the photograph's own measured silver carried into the render*, so its
G/R agreeing on both sides (0.936 / 0.936) is **BY CONSTRUCTION, not evidence.** I nearly published
that agreement as an independent white-balance check.

W6 makes colour his call either way. **Reported, NOT acted on.**

---

## §2. ITEM C — BOTH FAILING ROWS ARE ONE UNKNOWN, AND IT IS AN INSTRUMENT

The brief: *"The two standing `flank_compare` failures … Both are measured, both are model-side."*
**The second half does not hold.**

### §2.1 THE ASPECT ROW IS DECIDED BY WHICH VERTICAL INSTRUMENT IS BELIEVED

Three readings of the same difference, all printed by the same run:

| reading | value | verdict at the 5 % bar |
|---|---|---|
| raw reference pixels | **+0.94 %** | PASS |
| the map's own vertical scale | **+2.86 %** | PASS |
| `k_t` (SPEC 10.34) — **the row that is quoted** | **+5.23 %** | **FAIL** |

`flank_compare.py`'s own header already said the two vertical instruments *"disagree by 2.3 % at
the hub"* and that *"one of the two instruments is 2.3 % out"* **without saying which**. The brief
quoted only the failing reading.

### §2.2 HEIGHT, ASPECT AND AREA ARE NOT THREE WITNESSES

An earlier draft of this revision's own commit called them three independent quantities agreeing.
**That was wrong and it is retracted here.** `ref_area` is `(flank_mpp / flank_kv).sum()`, so all
three are reductions of the same two masks through the same vertical instrument and a 2.3 % error
in `k_t` moves all three together.

### §2.3 `Senor` IS THE SAME UNKNOWN, NOT A SECOND DEFECT

`senor_trace.py` scores **0.913 IoU** against the measured 934 px mask, so the glyph is not in
question. `Senor` sits at the lockup's top-left extreme, where a height error hurts most once the
global shift has absorbed the translation. New ablation **`T1_FC_ZSTRETCH`** stretches the render
mask vertically before scoring:

| stretch | 1.000 | 1.020 | 1.040 | 1.060 | 1.080 |
|---|---|---|---|---|---|
| IoU / ceiling | 0.888 | 0.910 | **0.920** | 0.910 | 0.892 |
| `Senor` of ceiling | 0.483 | — | 0.712 | **0.795** | — |

A clean parabola, vertex **1.0398**. At 1.056 the worst region becomes `i` at 0.770 and **the row
PASSES**. So **one quantity — the panel's height — accounts for BOTH failing rows.**

*(The first run of this ablation had the SIGN WRONG: `sampler_gen`'s `zsq` divides, so `zsq<1`
squashes. I compressed the mask and read "the fix makes it worse". Caught by the negative control's
own docstring, which calls `zsq=0.92` "squashed 8 %".)*

### §2.4 AND THAT OPTIMUM IS NOT INDEPENDENT EVIDENCE — I NEARLY PUBLISHED IT AS IF IT WERE

The reference mask is carried into the metric frame by the **same `flank_kv`**. Stretching the
render to overlap a reference that may itself have been placed 2.3 % too tall improves the overlap
**circularly**: it measures agreement with the instrument, not with the vehicle.

**What IS independent points the other way.** `tex/senor.png` was authored from the reference's RAW
pixels (its 2.357 AR against the reference bbox's 2.3478), and in raw pixels the render is
+0.94 % — right. And the file's own physical argument: for an oblique view of a vertical plane the
**horizontal** scale must be the smaller of the two, and it is not (220.45 against `k_t`'s 215.5).
If the map is the sound one then `k_t` is too SMALL, the reference's ink height in metres is
**overstated**, and the render may not be short at all.

### §2.5 SO `SCR` WAS NOT STRETCHED

Stretching it would encode one instrument's own 2.3 % error into the geometry that instrument
exists to measure — and `build.py`'s comment above `SCR` (*"GROWN UPWARD … the missing height
belongs at the TOP"*) would have made it look corroborated when it is **the same unknown twice**.
No bar and no verdict was changed: a script is not edited to make it pass.

**WHAT WOULD CLOSE THIS:** one independent vertical scale on `ref_side.jpg`'s flank plane. Until
then both rows stay FAILING and **UNATTRIBUTED**.

---

## §3. ITEM 2 — THE CHIP GATE IS DEAD ON THE RED SHELL. THE CODE IS THE DEFECT

### §3.1 CONFIRMED, NOT REFUTED

`t1_mats.py` builds `EDGE = 1 - dot(bevel_normal, geo.outputs["Normal"])` while its own design note
says, verbatim, *"edge = 1 - dot(bevel_normal, true_normal)"* and *"On a flat face the two normals
are identical and edge == 0 BY CONSTRUCTION"*. `Normal` is the **shading** normal.

`probe_rev55_truenorm.py` asks the mesh first (rule 10 — grepping a name is not a test):

```
T1_body    61737 polys,  61737 smooth (100.0 %)  -> the two sockets DIFFER
counter       26 polys,      0 smooth (  0.0 %)  -> the two sockets are the SAME vector
```

One variable: the same build, camera, sample count and emission AOV; only which socket feeds input
1 of that dot product.

| crop | frac > `W_EDGE_LO` as shipped | on `True Normal` | ratio |
|---|---|---|---|
| flank (`T1_body`) | 0.002668 | **0.134578** | **50.4×** |
| rear arch lip (`T1_body`) | **0.000000** | **0.208417** | dead → alive |
| counter (FLAT, **the control**) | 0.013771 | 0.013771 | **1.00×** |

### §3.2 THE CONTROL IS WHY THIS CAN BE BELIEVED — AND IT FAILED FIRST

`counter` is flat, so the two sockets are the same vector there and the arms **must** agree.

* **First run: the control did not run at all.** My typed window put 418 px of counter in frame and
  the probe **REFUSED** rather than report a control it did not have. The window was rederived
  **from the counter's own mesh** (rule 7).
* **Second run: the control FAILED at 5.98 %** — on a 3.09 m-wide crop at 3.44 mm/px, where the
  bevel radius is **0.80 px**. A percentage on a ray-traced quantity means nothing without the
  sampler's own spread, so a **NULL ARM** was added: arm S rendered twice, same socket, same
  samples, **different seed**.
* **Third run, at 8.25 px per bevel radius: `S`-to-`T` 0.00 %, `S`-to-`S` floor 0.10 %.** The bar is
  3× the measured floor, not a number I liked. **CONTROL HOLDS.**

### §3.3 PAINTED, AND IT IS NOT SUBTLE

`probe_scratch/rev55_tn_flank.png`, `rev55_tn_arch.png` — left as shipped, right on the true
normal. **As shipped the whole red shell is BLACK**: no edge signal at any arch lip, panel aperture
or shut line. On the true normal the arch lip, the aperture surround and the shut lines all light
up.

**So the red carries NO edge chipping at all** — while `SPEC` §3 and the owner's own rev-53
narrowing (*"WEATHERED is NARROWED to the red and the running gear"*) both require that it should.

### §3.4 AND THEN MY OWN FIRST CONCLUSION WAS REFUTED, IN THE SAME REVISION

The obvious reading of §3.1–3.3 is *"the code is the defect, flip the link."* **That was this
revision's first conclusion and it is withdrawn.**

On a **SMOOTH-shaded** mesh the true normal is **piecewise constant** — one value per polygon —
while the bevel normal is smooth. So `1 - dot(bevel_n, true_n)` is non-zero across **every facet
boundary of a curved panel**: it detects **TESSELLATION, not folds**. That is precisely the flaw
the design note says this construction exists to escape — *"an edge detector that does not know the
vertex count"* — so the true normal reintroduces Pointiness's defect by another route.

**THE DIRECT TEST IS THE VERTEX COUNT**, because `T1_SUB` is what changes it. The probe was run at
both levels (61 737 → 235 716 polys, 3.8×):

| frac > `W_EDGE_LO` | `T1_SUB=1` | `T1_SUB=2` | |
|---|---|---|---|
| flank, **arm T** | 0.134578 | 0.112530 | **−16 %** |
| arch, **arm T** | 0.208417 | 0.100381 | **−52 %** |
| flank, arm S | 0.002668 | 0.002675 | +0.3 % (stable) |

**A quantity that halves when you subdivide is not measuring the vehicle.**

**AND LOOKING SETTLES IT.** `probe_scratch/rev55_ASK_truenorm.png` — under `T1_TRUENORM=1` the
trunk lid, which is **CREAM**, comes up **blotched across its whole face**, not chipped along its
edges. His rev-53 ruling on that exact surface is *"Follow the photograph — clean cream"*. The flip
would break a settled ruling as well as being wrong on its own terms.

*(The hero A/B diff — 1.07 % of the frame moving by >16 DN — is a superposition of the shader
change and ordinary sampling noise, and I did not render a null hero, so only the **structured,
edge-localised** component of `probe_scratch/rev55_tn_herodiff.png` is attributable. The diffuse
speckle is not. Stated because the raw 1.07 % was nearly published as if it were all shader.)*

### §3.5 WHERE THAT LEAVES THE GATE

On **FLAT** geometry it works, and every counter result from rev 53 and rev 54 stands — measured,
not assumed. On the **SMOOTH red shell NEITHER socket is right**: `Normal` is dead and
`True Normal` counts facets. **The red's edge wear is UNBUILT and cannot be built by changing this
link.** A construction that works on both would have to come off the geometry (a real crease or
edge-angle attribute), and that is a revision's work.

`T1_TRUENORM=1` is kept as the lever that **demonstrates** this. **It is not the default and must
not become one.** The retraction is in `t1_mats.py` and in the probe's own printed verdict, not
only here (rule 15).

---

## §4. WHAT THE BRIEF GOT WRONG, MEASURED

| the rev-55 brief said | the machine says |
|---|---|
| item A: *"measure the CREAM either side of the ink"* | **there is no cream there** — the lockup is silver on RED, §1.1 |
| item C: *"Both are measured, both are model-side"* | both are **one instrument disagreement**, §2 |
| item B: the `cream_rms` re-base is open since rev 17 | **narrower than that** — `mottle_measure.py` already runs the re-based render-vs-photograph cream comparison on `cream_rms._BODY` at `PXM_REF = 337.0`. What is genuinely open is that `cream_rms.run()` itself is still the dead `ref_side.jpg` path, and that **neither file has one row in either verifier** |
| — | `cream_rms.py` cites **`depth_correct()`**, which is **defined nowhere in this repo** — a dangling citation in the middle of the scale caveat |
| — | `mottle_measure.py` assigns **`PHOT` twice, 2 lines apart**; the first dict is dead code, so the file carries two different sets of "the photograph's" figures and silently discards one |
| item 0: the nose roundel is not a defect | **confirmed by looking** — I read it as an "X" at half size in the hero and it dissolved at full size into a proper V-over-W. The brief's own warning ("crops generate leads, not findings") fired on me |


---

## §5. ITEM B — NOT DONE, AND THE BRIEF'S FRAMING OF IT IS TOO BROAD

**What the brief says:** *"Re-base `cream_rms.py` onto `ref_rear34.jpg` … Open since rev 17."*

**What is actually true, measured:**

* The **photograph side is ALREADY LIVE AND CORRECT.** `cream_rms.spectrum(_BODY,
  "ref_rear34.jpg")` runs today and returns the REAL (codec-subtracted) spectrum
  **0.804 / 1.135 / 1.455 / 2.201 / 3.183 %** at sigma 1/2/4/8/12 px, on 7968 px at 100 %
  unclipped. `_BODY = (885, 968, 292, 388)` is the owner-identified bus cream.
* The **render side already exists too**, in `mottle_measure.py`, which projects a model-space
  patch through an ORTHO render (px/m exact by construction) and compares it at matched physical
  scale against a `TARGET` dict — and that `TARGET` **is** those five numbers, verified this
  revision by running `spectrum()` and reading them off.
* So the re-base is **substantially done, in another file.**

**What is genuinely open, and it is narrower:**

1. `cream_rms.run()` — the thing a reader runs — is still the **dead `ref_side.jpg` legacy path**
   that refuses and prints its own remedy. It has not been pointed at the live work.
2. **Neither file has one row in either verifier.** `verify_clone.sh`'s `brief still names
   cream_rms` guards that the BRIEF mentions the string — a carrier guard, not a measurement
   guard. So the brief's *"still zero rows in either acceptance script"* is TRUE.
3. The **mm axis is still not established** on that plane: `PXM_REF = 337.0` px/m is a bracket
   (330–344), not a measurement, and the function cited as its remedy did not exist.

**NOT ATTEMPTED THIS REVISION, deliberately.** Items A, C and 2 each had a gate; this one needs a
render pass on `mottle_measure.py` and a decision about which file owns the number, and starting it
badly would have cost more than leaving it stated. **Two of its defects WERE closed** (§4).

---

## §6. THE GUARDS THIS REVISION ADDED — TEN ROWS, ALL WATCHED BOTH WAYS

`verify_clone.sh` goes **173 → 183 rows** (182 pass + the brief-count row, which passes once the
rev-56 brief states 183). Every row was watched **FAILING** by deleting its anchor and **PASSING**
again on a clean tree, in the same hour it was written.

| row | forced failure |
|---|---|
| flank_compare carries the ground control | got 0, want 1 |
| that control's verdict has both branches | got 1, want 2 |
| T1_FC_INKGAIN ablation exists | got 0, want 1 |
| T1_FC_ZSTRETCH ablation exists | got 0, want 1 |
| the aspect row carries its instrument note | got 0, want 1 |
| t1_mats carries the true-normal retraction | got 0, want 1 |
| t1_mats keeps the facet-counting half | got 0, want 1 |
| T1_TRUENORM lever exists in the shader | got 0, want 1 |
| cream_rms cites no undefined depth_correct | got 1, want 0 |
| mottle_measure binds PHOT exactly once | got 2, want 1 |

**`t1_mats` gets TWO rows, not one, on purpose:** either half of that retraction alone is a claim
that would get the default flipped. *"The shipped socket is dead"* without *"the true normal counts
facets"* is exactly the wrong lesson to inherit.

**AN EXISTING ROW CAUGHT MY OWN EDIT.** *"rev52's sub-pixel reason is RETRACTED in the source"*
anchors on a phrase that must be UNIQUE, and my new `t1_mats` comment used *"IS RETRACTED HERE"*
as well — got 2, want 1. The comment was reworded; the row was not loosened.

---

## §7. WHAT I GOT WRONG THIS REVISION, IN ORDER

Budgeted for, per `CLAUDE.md` rule 4 — every recent revision catches four to seven of its own
instruments being wrong, and every one produced a plausible number.

1. **The ground control's verdict was a CONSTANT STRING.** It printed *"the ink is NOT painted
   light"* and went on saying it at 19.2 % under the ablation. Caught by running the ablation, not
   by re-reading. Derived now, against the reference ink's own spread.
2. **`T1_FC_ZSTRETCH`'s sign was inverted.** `sampler_gen`'s `zsq` divides, so `zsq<1` squashes. I
   compressed the mask and read *"correcting the height makes it worse"*. Caught by the negative
   control's own docstring, which calls `zsq=0.92` "squashed 8 %".
3. **I called height, aspect and area three independent witnesses.** They share `flank_kv`.
4. **I nearly published the IoU stretch optimum as independent evidence** that the lockup is short.
   It is circular — the reference is placed by the same instrument.
5. **I nearly published the silver's G/R agreement as a white-balance check.** It is by
   construction: `SILVER_CHROMA` is the photograph's own silver carried into the render.
6. **The true-normal probe's control did not exist on the first run** (418 px window, typed not
   derived) and **FAILED on the second** (5.98 %, on a crop with 0.80 px of bevel radius). Only the
   third run — window from the mesh, null arm for the floor — could support anything.
7. **"The code is the defect, flip the link"** was my own conclusion and my own next measurement
   refuted it.
8. **I read the nose roundel as an "X"** in the half-size hero. At full size it is a proper
   V-over-W. The brief's own warning fired on me: crops generate leads, not findings.
9. **My new comment collided with an existing guard's unique anchor** (§6).

---

## §8. THE RETIRED ADDENDUM, RE-READ AFTER THE FACT — AND THE ONE DELTA THAT HAD NOT LANDED

`HANDOFF_rev55_ADDENDUM.md` was written for *"the rev-55 context that was started on the SUPERSEDED
prompt"* — which is exactly what this context was. **It had already retired itself before it was
re-read.** Its own condition:

> *"This file RETIRES the moment `origin/main` carries the 191-row brief — check with
> `grep -c 'ALL 191 PASS' PASTE_INTO_CLAUDE_CODE.txt` and delete it when that is 1 on main."*

**Measured, not assumed:** that grep returns **2** on `origin/main`; the file was deleted there in
commit `c5c01cd` (*"rev 54: retire the rev-55 addendum — its own condition is met"*); and the branch
it told me to merge, `origin/claude/tacombi-rev-54-u7hvys`, is **0 ahead of main**. So its whole
content arrived through the mid-revision merge (§0/§1), and it was spent.

**BUT IT IS A DELTA DOCUMENT, SO EACH OF ITS FIVE DELTAS WAS CHECKED AGAINST THE OUTGOING BRIEF —
AND FOUR OF FIVE HAD LANDED:**

| delta | state in `NEXT_CONTEXT_PROMPT_rev56.md` |
|---|---|
| 1. `verify_clone.sh` is 191, not 173 | carried — and now **202** |
| 2. §0, the GOAL stated before any work item | carried, updated to rev 55's measurements |
| 3. §0.1, the owner's reference-set ruling | carried in full |
| 4. **§4 re-framed** from *"WHAT ONLY HE CAN GIVE"* to *"A CARRIER, NOT A LIST OF BLOCKERS"* | **NOT CARRIED** |
| 5. "keep studio, fix the model" | carried |

**DELTA 4 IS THE ONE THAT MATTERS, because the old heading is what licensed four revisions of
parking the top job behind a photograph.** `main` re-framed it inside rev 55's §4; this revision
merged that change and then **wrote the OLD heading into its own outgoing brief.** The re-framing
lived in a section of the *previous* brief and never propagated to the *next* one.

**AND IT SURVIVED THIS REVISION'S OWN RULE-17 AUDIT.** That audit `stat`ed every path, grepped every
quoted string, resolved every `T1_*` switch and recomputed every figure — and **none of those asks
"was a re-framing carried forward".** A sweep over content cannot see a heading that should no
longer exist. **That is the gap, and it is now a row**:

```
ck "newest brief drops the retired sec.4 heading" 0 \
   "$(grep -cE '^#+ .*WHAT ONLY HE CAN GIVE' "$_LATEST_BRIEF")"
```

**ANCHORED ON THE LINE THAT *IS* THE HEADING, NOT ON THE PHRASE** — because a brief that explains why
the heading was retired has to be able to quote it, and the rev-56 brief does. This repo had already
earned that lesson on the `DEFAULT IS STILL POINTINESS` row. **Both halves watched: it passes with
the phrase quoted twice in prose (0) and fires when the heading is real (got 1).**

**The parking language went with it.** §4's badge route no longer reads *"scoped as a revision's
work, not a spare hour"* as a deferral; it says that is a statement of COST, that §0.1 forbids
reading it as a reason to defer, and that **rev 55's failure to take that route is the clearest
thing it did against §0.1.**
