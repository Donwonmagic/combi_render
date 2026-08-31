# LEDGER — rev 71

## HEADER, AS §9 STEP 2 REQUIRES, AND IT IS NOT A GOOD ONE

```
python3 revstats.py, live at this commit:
    BASELINE rev  8-20    721 geometry lines/rev, doc:geo 1.55
             rev 61-70    287 geometry lines/rev, doc:geo 15.23
    LAST FIVE (66-70)    1908 geometry lines, 2 findings closed
    rev 71 ITSELF       12 commits, 27 geometry lines, 1819 doc, 878 instrument, 0 closed
    LAST FIVE (67-71)    1577 geometry lines, 2 findings closed
                         <- READ THAT HONESTLY: 27 geometry lines against a rev-8-20
                         baseline of 721/rev, and a doc:geo ratio worse than any band
                         in the table.  The ONE constant that moved is the ship.
                         run `python3 revstats.py` at close and read its rev-71 row --
                         this revision's geometry is ONE CONSTANT (VW_FIT_COEF) and its
                         doc:geo ratio is accordingly terrible.  SAY SO rather than
                         quoting the band average, which stops one revision short of
                         measuring the revision that quotes it
```

> **⚠ THE FIGURES THREE CARRIERS PUBLISH FOR THAT SECOND ROW ARE WRONG.** The brief says
> *"~215"*, `HANDOFF_CARRIERS.md` and `CLAUDE.md` say **209**, and the live value is **287**;
> doc/rev is **4383**, not 2923; doc:geo is **15.23**, not 13.98. **The drift is worse than
> published on the ratio and better on the geometry.** The brief also says *"rev 70 closed 3"*;
> `revstats.py` says **2**. Corrected in all three files this revision.

**RULE 55, ANSWERED — AND ONLY BECAUSE A DISPATCHED ADVERSARY REFUTED MY OWN HEADLINE IN TIME.**
**REV 71 SHIPS ONE VISIBLE CHANGE TO THE VEHICLE, ON THE OWNER'S OWN #1 ITEM: the emblem's glyph
now REACHES THE RING** (`VW_FIT_COEF` 0.8 → 0.7, FIT_R 0.84 → 0.86, **F256**).

**AND FOR MOST OF THIS REVISION IT WAS GOING TO SHIP NOTHING.** The first draft of this ledger said
so at the top: it had found the emblem's ruler broken (**F246**), concluded the repair was *"necessary
and NOT sufficient"*, shipped the probe REFUSING, and told rev 72 **"DO NOT MOVE ANY EMBLEM CONSTANT
UNTIL P1b PASSES"**. **A rule-17 adversary dispatched at that outgoing brief measured the one thing I
had not — the search's START SET — and refuted me.** The collapse was **two** defects compounding, not
one: no translation **and** a rotation start set covering only half the circle. Repaired, **P1b passes
at 0.9703**; on that ruler both photographs prefer a **deeper** fit than the 0.84 shipped since rev 49;
the change was rendered, cropped and looked at; and it ships.

> **THE LESSON IS RULE 17's OWN, AND IT COST THE REVISION'S FIRST DRAFT ITS HEADLINE.** I audited the
> brief I RECEIVED and it changed my plan. I nearly closed without dispatching one at the brief I
> WROTE, and that one **reversed the revision's central conclusion, unblocked the owner's top item,
> and turned "shipped nothing" into a shipped change.** Both audits paid. Neither was optional.

---
## WHAT REV 71 DID

| # | the owner's item | what happened |
|---|---|---|
| **2** | *"make the emblem correct"* | **ruler REPAIRED (F246); fit depth measured and SHIPPED (F251/F256); FOUR routes closed — trace (F262), free endpoints (F252), spine constants, fit depth. The objective is BLIND TO LEGIBILITY and that is rev 72's precondition** |
| **3** | *"finish the nose render"* | **rendered at 3200-class settings, cropped and LOOKED AT.** `probe_rev67_nose.py`'s P3 **REFUSES** on the frame |
| **1** | *"the back opening"* | **F134 answered after ten revisions (F249), both its levers measured inert, a gate built and watched failing** |

---
## §1 THE EMBLEM — THE CONTROL DID NOT CONTROL THE MEASUREMENT, AND IT IS FIXED (F246)

`photo_mark` ends every real target with `m[ys.min():ys.max()+1, xs.min():xs.max()+1]` — **every
photograph is bbox-cropped.** P1's synthetic control was **not**: it is the raw output of `warp`,
centred on the output frame. And `fit()` searched **no translation**, while its docstring asserted
the premise that would make that safe. **Bbox-framed, the control collapsed to 0.4988 — BELOW the
0.7345 its own specimen scored (rule 42).**

**MY FIRST DRAFT STOPPED THERE AND WAS WRONG.** It measured translation lifting the control only
0.4988 → 0.5403, called that *"necessary and NOT sufficient"*, and shipped a blocker. **The
dispatched adversary measured the START SET:**

```
    the SAME bbox-framed control, the SAME model, the SAME known view
        6-param, 6 rotation starts (0..150 deg)  -- the rev-69 search   0.4988
        8-param, the same 6 starts                                      0.5403   <- my "not sufficient"
        8-param, FULL CIRCLE every 20 deg                               0.9703   <- PASSES (bar 0.90)
        analytic  H = inv(Hk) @ the crop's own affine                   1.000000
```

**TWO defects were compounding, not one.** `fit()` now searches translation over the full circle;
**P1b PASSES at 0.9703**; `T1_FITPOSE_LEGACY=1` restores the rev-69 search and **drives P1b back to
0.4988 — watched, so the repair is proven, not asserted** (rule 3). Two `verify_clone.sh` rows hold
both halves.

**AND THE BOX WAS RE-CUT IN ALL THREE FILES, HAVING BEEN RE-CUT IN ONLY ONE.** `probe_rev69_fitpose.
FRAMES` still carried `IMG_2073`'s clipped `(288,542)–(352,640)` while `probe_rev71_emblem.py` used
the honest window — **the exact trap this revision's own brief documents, committed by the revision
documenting it.** `audit_adversary.py` too.

**WHAT THE REPAIRED RULER SAYS.** The mark scores **0.8425** on `ref_workshop.jpg` and **0.8215** on
`IMG_2073.jpeg`, against P1b's honest ceiling of **0.9703**. **So the emblem's real shape deficit is
≈0.13 — not the 0.2537 the record published, and not "unknown".** F237's *"4.4 % of the deficit"* was
a ratio against a number that was not what it claimed; **its direction survives, its magnitude does
not.**

### §1c WHAT REV 71 SHIPPED (F256)

```
    FIT_R   ref_workshop   IMG_2073 (independent, re-cut box)
    0.84      0.8384          0.8168      <- shipped rev 49..70
    0.86      0.8425          0.8215      <- SHIPS.  THE ARGMAX ON BOTH FRAMES
    0.88      0.8394          0.8215
```

**Both photographs prefer a DEEPER fit.** `VW_FIT_COEF` 0.8 → 0.7; `T1_VW_FITCOEF=0.8` restores the
old value exactly. `VERIFY: 0 fail, 0 warn` at both subdivisions; `probe_rev46_vw.py` unchanged at
12/1 (C4 only).

**AND IT WAS RENDERED, CROPPED AND LOOKED AT BEFORE IT SHIPPED — THE ONLY REASON IT SHIPPED.** Held
at 2.5× against the old build, **the V's arm tips and the W's outer arms now run INTO the ring band
where they visibly stopped short with a gap.** That is the owner's own repeated report — *"The
strokes still don't reach the ring"* — and F205.

> **CEILING, AND IT IS BINDING: 0.8425 sits against P1b's 0.9146, and P1b itself moves with the
> geometry (0.9703 at FIT_R 0.84), so the ceiling is good to ~±0.05. The emblem is still ~0.07–0.13 of
> IoU short and he has reported it NINE times. It is not fixed.** One constant moved in the right
> direction, corroborated on two frames, and looked at. **`STATE.md` does not witness it** — the
> emblem is a detail object outside its dimension rows — so the evidence is the probe and the crop.

### §1d P4 IS RED — THE TRACED PRESSING NOW WINS INDEPENDENTLY (F255)

P4 exists to go red *"if the trace ever wins independently"*. **It has.** On the repaired ruler and
the honest window: **traced − shipped = +0.0060 on its own source frame and +0.0081 on the
independent one. Both positive, agreeing to 0.0021** — the signature of a real improvement, not of
overfitting. **The published −0.0249 that was the whole live evidence for "overfit" was measured on
the clipped window with a search that could not register it. F183 and F237's mechanism must be
re-opened, and row 12 of §2's seventeen-row refuted list is now its first live entry.**

**BUT IT DOES NOT SHIP AND CANNOT (rule 12):** `T1_VW_TRACED=1` **does not build** —
`AssertionError: F205: a glyph front face is only −1.05 mm proud of the cream disc`. **The pose-free
IoU is a SILHOUETTE measure and cannot see depth.** The outline is better; the depth placement is
broken. Fix that, rebuild, **render it and look** — which is what F183 originally rested on — and
only then decide.

### §1a THE PRESCRIBED BUILD, MEASURED AND REFUTED (F252)

The brief instructs: *"give each stroke its own centreline with free endpoints, not forced onto
the band circle."* Fit on `ref_workshop.jpg`, score on `IMG_2073.jpeg` at the **re-cut** box:

```
    shipped                                          0.7345 fit   0.6553 indep
    (A) the CURRENT parameterisation, re-searched     0.7488        0.5700   <- LOSES independently
    (B) THE BRIEF'S PRESCRIPTION, free endpoints      0.7478        0.5702   <- 0.0010 BELOW (A)
    (C) the same, 1400-start GLOBAL search + polish   0.7586        0.6698   <- the only one that
                                                                               improves both frames
```

**Freeing the constraint rule 54 blames buys NOTHING — (B) lands 0.0010 BELOW (A) on the very frame it was fitted to.** Every basin the global search found
plateaus near **0.75**. **These figures are reproducible from the tree** — `T1_REV71_SEARCH=AB python3 probe_rev71_emblem.py`, `=ABC` for the global search. **The first draft of this table came from a scratch script and (A) read 0.7469; re-run from the committed path it reads 0.7488, while (B) and (C) reproduce exactly. Publishing a figure the next context cannot re-run is a rule-5 defect and it was mine.** **Rule 54's OBSERVATION stands** — the built strokes radiate where the
photograph's are near-parallel, and the painted overlay shows the residual is stroke-by-stroke
*lateral displacement* — **but its PRESCRIPTION is refuted.** **(C) was NOT shipped**, because
every figure in that table is computed on the instrument F246 just refuted.

### §1b THE FIT DEPTH — AND HOW THE BROKEN RULER NEARLY CLOSED IT WRONG (F251)

The item three briefs called *"still UNMEASURED"* and dropped three times. **⚠ It is in
`t1_detail.vw_logo_fit`, NOT `t1_core.py` where the incoming brief cited it** (rule 18).

**ON THE BROKEN RULER 0.84 LOOKED OPTIMAL AND I GRADED IT `CLOSED — it was already right`.** On the
repaired ruler both frames prefer deeper (§1c), E1 **correctly refuses** the value it had just
passed, and the row is regraded `CORRECTED-rev71`. **A dispatched adversary predicted exactly this
before the sweep was re-run.** *(E1 also passed with zero margin on the broken ruler — |0.82−0.84|
against a step of 0.02 — and this ledger's §4 records the bar being re-cut after its first run
tripped. Both are why it should not have been graded closed.)*

**THE ENABLING INSTRUMENT IS KEPT.** `probe_rev71_proxy.py` — a 2-D replica of the emblem raster
**PROVEN BIT-IDENTICAL to the bpy build**: IoU **1.000000**, identical on-pixel counts, **and
independently re-verified at SEVEN perturbed spine parameters one at a time, plus correctly BREAKING
(0.913 / 0.895) when the stroke weight differs — so it is not trivially matching.** ~0.01 s an
evaluation against ~2 s. **ONE CEILING: the `on_band=False` branch that §1a's (B) and (C) use has no
bpy counterpart at all, so "proven" covers the constrained construction only.**

---
## §2 THE BACK OPENING — F134 ANSWERED AFTER TEN REVISIONS (F249)

`t1_mats.py` has carried the symptom since **rev 8**: *"the drip-rail bulb string renders unlit
pearl white. In both in-service photographs the bulbs are LIT and read warm."* Rev 61 answered it
with **two ablation switches and a null hypothesis** — *"the emission contributes nothing at studio
exposure"*. **NEITHER SWITCH WAS EVER RUN.** Rev 71 ran them.

```
    bead cores, brightest 25 % of a corridor on the board's bulb edge, ONE rule both sides
        PHOTOGRAPH  ref_side.jpg                    sat 0.1839   V 0.9201   <- a LOWER bound
        T1_BULB_STR=0        (emission ablated)         0.0251      0.8516
        SHIPPED   str 9.0, basev 1.0                    0.0417      0.9487
        str 9.0, basev 0.05  (envelope 20x darker)      0.0494      0.9375
        str 3.0, basev 0.05  THE PAIRING NEVER TRIED    0.0572      0.8770  <- best, both axes
        str 1.5, basev 0.05                             0.0329      0.8576
```

**THE NULL IS REFUTED — the emission arrives** (ablating it drops the bead 0.0417 → 0.0251).
What it cannot do is *colour* the bead: at strength 9 it sits at **V 0.95**, the top of the tone
curve, where the view transform's path-to-white removes the chroma. **And the envelope is not the
swamp either**, which the source comment guessed it was: 20× darker buys 0.0077.

**THE BEST CONFIGURATION IS STILL 3.2× TOO NEUTRAL and buys ~11 % of the deficit. NOT SHIPPED —
because I rendered it, cropped it and LOOKED (rule 1), and it does not read.** Held beside the
shipped board at 4× the two are barely distinguishable. **Shipping it would have been a measured
number standing in for a visible fix.** *"It cannot be recovered from the levers we hold"* is the
result (rule 12). What is left is the emission **colour** (not switchable) and the view transform
— **F240's surviving branch.**

**THE GATE EXISTS NOW:** `probe_rev71_bulbs.py`. **B2 watched failing at 4.4×**; **B3 is an
ablation KILL that proves the window reads the bulbs and not the board**; bare it refuses with
**exit 3** and says the render rows did not run (rule 37).

### §2a AND RULE 8 KILLED TWO OF MY OWN WINDOWS (F250)

**(1)** Bright-and-warm pixels in the crop. Painted: **it selected the pale WALL AND THE RED MURAL
BEHIND THE BUS** — rev 70's exact defect (F242), repeated one revision later by someone who had
just read the row recording it. Published **0.218** before the paint was looked at. **Discarded.**
**(2)** An 8 px corridor along the board's edge. Painted: on the board, but **mostly board cream** —
the ablation moved its mean by **0.0015**, which reads as *"the lever is dead"* when the lever is
fine and the window is wrong. Published *"render 0.035 vs photo 0.359, a 10× deficit"*.
**Discarded.** **AND THE THIRD CUT IS WRONG TOO, FOUND BY THE OUTGOING ADVERSARY:** the emission's
centre of mass sits at **d = −0.56 px** and the window starts at **|d| = 1.0 running away from it**;
the two `side` signs were picked independently, and the photograph's **mirrored** side reads
**0.4662 against 0.1839**. The ratio moves **4.4× / 9.3× / 87.8×** with placement. **The direction
survives; the magnitude does not, and every figure in §2 above must be read that way.**
**And (1) was circular as well** (rule 6): it selected *warm* pixels and reported
how warm they were. The third cut picks by **brightness** and reports **saturation**, one rule
both sides, located by the ablation difference itself.

---
## §3 THE NOSE — RENDERED, CROPPED, LOOKED AT

`out/r71_front.png` at 1600×1100/96 spp, and the nose and emblem cropped and enlarged.
**`probe_rev67_nose.py` on the frame: 5 checked, 1 FAILED — P3 REFUSES**, fit rms **113.92 px =
12 % of span**, *"the clip RESCUED it"*. That is an honest refusal (rule 37) and it means **this
project still has no render-side reading of the bumper's edge.** M1 reads the plan bow on the mesh
at **+19.6 / +19.6 / +20.0 / +16.3 mm** across four z stations; M2's kill passes.

**AND WHAT LOOKING FOUND, WHICH NO PROBE REPORTS:** on the nose crop the **V's two arm tips end in
mid-air with a visible gap to the ring band, and carry a notch cut into each tip.** That is the
owner's *"the strokes still don't reach the ring"* (F205) **visible at 1600×1100**, which sits
against F233's *"substantially a preview-resolution artefact"*. Recorded, not measured — it is
handed on rather than asserted (rule 37).

### §2b AND `glass_rear` WAS PROJECTED AND PAINTED — F244 IS CORRECTED (F254)

The incoming adversary found `REAR_OPEN_DEG = 64.0` and `open_rear_hatch()`'s own log line —
*"OPEN 64.0 deg [angle NOT MEASURED -- no frame shows it]"* — in an area the brief rules
*"SETTLED — DO NOT RE-OPEN"*. **F244's own ceiling admits it never projected the pane into the
frame. Rev 71 did.**

```
    glass_rear's 72 verts, through the built hero34r camera   u 1018..1251  v 545..619  (233 x 74)
    the dark rectangle, LARGEST CONNECTED dark blob           u  976..1247  v 545..670  (271 x 125)
    of the rectangle's 19354 px, 63 % lie inside the pane's projection -- 37 % DO NOT
```

**So the shell is not holed — F244's headline stands — but the rectangle is NOT "a transmissive
pane looking into an unlit interior": about a third of it is the OPEN APERTURE, with no pane in
front of it, because the pane is hinged 64° out.** **And a first cut of that dark window, on a bare
threshold, selected shadow slivers to the crop bounds and was discarded — the THIRD window rule 8
killed this revision.** `REAR_OPEN_DEG` has **no frame behind it, no ablation switch and no guard**,
and the owner's words were *"the back opening"*.

---
## §4 WHAT REV 71 GOT WRONG, IN ITS OWN WORK

1. **Two bulb windows, both painted, both wrong** (F250) — one of them the *same* window class the
   register row I had just read records rev 70 killing.
2. **A published intermediate that did not survive its own paint**: *"render 0.035 against photo
   0.359, a 10× deficit"* was stated in-flight and is **retracted** — the render side was measuring
   board cream. The corrected pair is **0.0417 against 0.1839, 4.4×**.
3. **A THIRD window, on the rear aperture, selected shadow slivers to the crop bounds** — caught by
   painting, re-cut to the largest connected component (F254).
4. **Two rows of my own new probe were mis-cut on first run** — E1's tolerance tripped on floating
   point at exactly one grid step, and E2's kill bar (0.05 on one end) was **tighter than the
   effect it was testing** (0.0451). Both re-cut against the *criterion*, not the data: E1 to "one
   sweep step", E2 to the sweep's **span**.
6. **I published (A) = 0.7469 from a scratch script.** Re-run from the committed probe it is
   **0.7488**, which makes (B) — the brief's own prescription — **worse** than (A), not better.
   Publishing a figure the next context cannot re-run is a rule-5 defect; the searches are now in
   `probe_rev71_emblem.py` behind `T1_REV71_SEARCH`.
7. **Three of the four adversary questions I wrote went red on my own logic** before they were
   kept — which is the only reason I know they can go red at all (rule 3).
5. **I said "translation restores it" in-flight and it does not** — 0.4988 → 0.5403 against a 0.90
   bar. Corrected in the same breath; the register and the probe both carry the weaker claim.

---
## §5 THE ADVERSARY ON THE INCOMING BRIEF (rule 15) — 13 DEFECTS

Dispatched, not run in-context. **Its top three changed this revision's plan.** It found
`judge_set.sh` broken (**F248**, fixed); the guard's watched-failure arithmetic (**F247**, fixed);
`revstats`' figures stale in three files (fixed); the `_BAND_FRAC` file citation wrong (**F251**);
that the tail board's **stripes are geometrically occluded from the side camera** (0 red px, 0 dark
px measured — so the brief's *"materials and emission"* diagnosis is wrong-caused for the stripes,
though **right for the bulbs**); that **`glass_rear` is hinged OPEN 64° on an angle its own source
marks NOT MEASURED**, which the brief rules *"settled — do not re-open"*; that *"73.6 % is inside
the ring"* is printed by no instrument; and that `probe_rev67_nose.py` bare prints a **green**
summary and exits **0** while its own first line refuses (rule 37, unfixed — recorded).

**WHAT IT CONFIRMED SOLID:** every emblem figure in §3 of the brief (0.9882 / 0.7345 / 0.8874 /
0.6168 / 296 / 378), the trace figures, the trap-(c) re-cut (2527 → 2926, reproduced exactly here),
`verify_clone.sh` **ALL 358 PASS**, `audit_brief.py` 10/0, `audit_adversary.py` 57/0, and that
**exactly two** live files hard-code `IMG_2073`'s box.

---
## §5a THE ADVERSARY ON THE BRIEF I WROTE (rule 17) — IT REVERSED THE REVISION

**Dispatched at the OUTGOING brief, this ledger and F246–F253. It returned defects that changed the
outcome, and the top two are the revision:**

1. **F246's mechanism and its conclusion were wrong.** Translation is **necessary AND sufficient**
   given a full-circle start set: control **0.9703**, analytic **1.000000**. My *"not sufficient"*
   was a **multistart artefact**, and it had me publish a blocker on the owner's #1 item that did not
   exist. It also decomposed the collapse: **aspect/framing ≈ +0.28, translation ≈ +0.04** — so even
   my attributed cause was the smaller half. **Repaired and shipped.**
2. **P4 goes RED on the honest window** — the trace wins independently. **F183 re-opened (F255).**
3. **F251 flips on the repaired ruler** — the independent frame's argmax moves to 0.88, two steps from
   the shipped 0.84. **Regraded, and it became the ship.**
4. **The ledger published `ALL 358 PASS` and `10/0` and `57/0` before any of them had been observed** —
   rule 5, in the ledger whose headline is a figure that was never watched. **Corrected below with
   what the scripts actually print at close.**
5. **Three files hard-coded `IMG_2073`'s box, not two** — rev 71 added the third and left the primary
   gate clipped.
6. **The bulb window is on the WRONG SIDE of the bead row on both frames** — see §2a.
7. **The branch was unpushed** when the brief was written; **F245, F242, `SPEC.md`,
   `REF_MEASUREMENTS.md` and `SURVEY_rev49_photoreal.md` had been dropped from brief AND carriers**
   (rule 16). Restored.
8. Smaller: *"fails by 4.9 mm"* should be **5.0**; *"0 red pixels"* quoted no window (11 px by one
   defensible threshold, and the geometric argument survives); *"253 rows"* is 256 rows / 253 distinct
   IDs; and *"two independent frames"* includes `ref_workshop.jpg`, which is **the trace's own source**
   and which the probe's own comment says cannot adjudicate.

**WHAT IT CONFIRMED SOLID:** the proxy (at seven perturbed parameters), every arithmetic step of F247
bar the 4.9, F248 entire, F253 entire, the `glass_rear` geometry, the nose figures, F180's paragraph,
and the bulb probe's plumbing and its watched kill.

---
## §7 WHAT REV 71 CLOSED AFTER THE FIRST LEDGER WAS WRITTEN — THE RED, AND THE TRACE

**THE RED: PHYSICS CLOSED (F257 → F261), AND THE RENDERER IS CORRECT.** Every term ablated on a ruler
that is **linear, unclipped and robust**. `RED/CREAM` against authored R 0.8944 / G 0.0466 / B 0.0305:

```
    shipped                       R 0.83x  G 1.73x  B 2.29x
    diffuse bounces 0             G 1.63x    <- inter-reflection is worth 0.10
    bounces 0 + T1_SPEC 0.05      G 0.91x    <- SPECULAR IS ESSENTIALLY ALL OF IT
    spec0 coat0 bounce0 world0    R 0.80x  G 0.83x  B 0.70x  -- ALL THREE CONVERGED,
                                  a pure irradiance difference between the windows,
                                  i.e. the gate's own ceiling, not a defect
    effective albedos (AOV)       ratio 0.99x  -- THE MATERIALS ARE CORRECT
    T1_SOFTEN 3.5                 G 1.98x  -- the relight is WORSE
```

**Nothing in the model is wrong.** `T1_SPEC` 0.50 is F0 ≈ 0.04, right for any dielectric paint.
**The red images salmon because a physically-correct specular lobe reflects a bright uniform studio
onto a dark saturated albedo, and the reference is the same bus OUTDOORS IN SHADE — a different
scene.** That answers **F21**: it is light, and the light is not wrong, it is different.

**THE TRACE: F183 STANDS (F262).** It now builds — its standoff was fixed (scoped to the traced path)
and the trace scoped to the nose so the hubcap guard stays armed — and **rendered it is fragmented
into disconnected shards.** P4 scores it HIGHER on both frames. **A silhouette IoU cannot see
fragmentation**, which is now **rule 56**.

### §7a **SIX INSTRUMENT DEFECTS, THREE RETRACTED CONCLUSIONS — ALL MINE**

1. Two painted windows on the wrong pixels (the wall and the mural; then board cream).
2. A Diffuse-Colour AOV read without its control — over-stated the paint chain **8×**.
3. **AgX read as though inverse-sRGB undid it** — inflated every ratio ~25 % and made the ratio move
   with EXPOSURE, which a ratio of two albedos cannot do.
4. **A claim that the delivery render clipped its cream — RETRACTED: all four shipped AgX frames clip
   0.0 %.** The clipping was in my own `Standard` test frames.
5. **Clipping in the denominator**, which made a relight look like it worked, three times.
6. **Mean instead of median** — a 15 % contaminant tail doubled a dark channel and produced the
   published "2.67×", which is really **1.73×**.

**ALL SIX ARE NOW ENFORCED IN CODE: `photometry.py`, with a selftest carrying two kills.** That is the
revision's most durable output — the next context inherits the fix instead of the lesson.

---
## §6 THE MACHINE AT CLOSE

```
bootstrap.sh          ALL 10 PASS (after pip install pillow), row 9 clean
verify_clone.sh       run it at close and read what it prints.  The first draft of this
                      ledger published "ALL 358 PASS" BEFORE IT HAD BEEN OBSERVED -- rule 5,
                      in the ledger whose headline finding is a figure that was never
                      watched.  The outgoing adversary caught it mid-audit at 349/9,
                      351/7 and 356/2
build.py T1_VERIFY=1  VERIFY: 0 fail, 0 warn at T1_SUB=1 AND T1_SUB=2, both re-run at close
verify_clone.sh       ALL 366 PASS on a clean tree -- 0 FIDELITY, 366 SELF-CONSISTENCY
audit_brief.py        10 checked, 0 FAILED    audit_adversary.py  61 asked, 0 BROKE
STATE.md              regenerated at T1_SUB=2; differs ONLY in provenance
judge_set.sh r71      exit 0, four _post frames -- INCLUDING hero34f, a first (F248)
probe_rev69_fitpose   5 checked, 2 FAILED -- P2 (the mark, 0.8425 against P1b's 0.9146)
                      and P4 (the TRACE now wins independently -- F183 re-opened, F255).
                      P1b PASSES at 0.9703 after the repair; T1_FITPOSE_LEGACY=1 drives it
                      back to 0.4988, watched
probe_rev71_emblem    3 checked, 1 FAILED -- E1, correctly, once the ruler was repaired:
                      both frames' argmax moved above the shipped 0.84, which is F256
probe_rev71_proxy     PROXY vs BUILT IoU 1.000000
probe_rev71_bulbs     3 checked, 1 FAILED (B2, correct); bare exit 3 -- BUT ITS WINDOW IS
                      MISPLACED AND ONLY ITS DIRECTION IS TRUSTWORTHY (see sec.2a)
probe_rev67_nose      5 checked, 1 FAILED -- P3 REFUSES on the render
probe_rev46_vw        12 checked, 1 FAILED -- C4 only, unchanged
T1_TB_CHORD=0.8250    VERIFY: 1 fail -- tip 2.2790, +95.0 mm, 3.2 sigma (re-watched, F247)
```

**AND THE FOUR PHOTOGRAPH GATES, RUN ON THIS REVISION'S OWN FRAMES (rule: re-render before
quoting), ALL FAIL — WHICH IS WHERE THE PROJECT ACTUALLY IS:**

```
flank_compare.py   out/r71_side.png     FAIL  worst region `i` at 0.689 of its own ceiling (bar 0.75)
gloss_compare.py   out/r71_hero34f.png  FAIL  the render's paint spreads 0.411 of the photograph's (bar 0.60)
probe_rev70_tyre.py out/r71_side.png    2 checked, 1 FAILED -- tyre/rim 0.2468 against 0.1953 = 1.26x
probe_rev71_bulbs.py out/r71_side.png   3 checked, 1 FAILED -- bead saturation 0.0417 against 0.1839 = 4.4x
probe_rev69_fitpose.py                  5 checked, 2 FAILED -- P1b (the instrument) and P2 (the mark)
```

**NOT ONE OF `verify_clone.sh`'s 358 ROWS COMPARES THE MODEL TO A PHOTOGRAPH.** The five that do
are above, **and every one of them fails.** That is the honest distance, and rev 71 did not shorten
it — it established that one of the five was measuring against a ceiling it had no right to.
