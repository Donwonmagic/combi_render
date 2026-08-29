# LEDGER — rev 71

## HEADER, AS §9 STEP 2 REQUIRES, AND IT IS NOT A GOOD ONE

```
python3 revstats.py, live at this commit:
    BASELINE rev  8-20    721 geometry lines/rev, doc:geo 1.55
             rev 61-70    287 geometry lines/rev, doc:geo 15.23
    LAST FIVE (66-70)    1908 geometry lines, 2 findings closed
```

> **⚠ THE FIGURES THREE CARRIERS PUBLISH FOR THAT SECOND ROW ARE WRONG.** The brief says
> *"~215"*, `HANDOFF_CARRIERS.md` and `CLAUDE.md` say **209**, and the live value is **287**;
> doc/rev is **4383**, not 2923; doc:geo is **15.23**, not 13.98. **The drift is worse than
> published on the ratio and better on the geometry.** The brief also says *"rev 70 closed 3"*;
> `revstats.py` says **2**. Corrected in all three files this revision.

**RULE 55, ANSWERED PLAINLY AND IN THE NEGATIVE: REV 71 SHIPPED NO VISIBLE CHANGE TO THE
VEHICLE. NOT ONE CONSTANT MOVED.** `STATE.md` regenerated at `T1_SUB=2` differs from rev 70's
**only in its provenance block** — generated-time, commit hash, subject — which is the machine's
own confirmation that the mesh did not move.

**WHY, AND IT IS A REASON AND NOT AN EXCUSE: THE RULER FOR THE OWNER'S TOP ITEM TURNED OUT TO BE
BROKEN, AND I FOUND IT BEFORE I SHIPPED ON IT.** Rev 70's whole lesson (F245) is that shipping a
geometry change on a ruler you have not checked costs a revision. The emblem's ruler — the
pose-free IoU that rev 69 built and this brief ranks as the revision's live build item — **fails
its own control when the control is framed the way its measurements are framed (F246).** I had a
candidate emblem construction measuring **+0.024 / +0.015** on two frames by that ruler. **I did
not ship it.** That is the same call rev 70 should have made and did not.

---
## WHAT REV 71 DID

| # | the owner's item | what happened |
|---|---|---|
| **2** | *"make the emblem correct"* | **the instrument is refuted (F246), the prescribed build is refuted (F252), and one open constant is CLOSED (F251)** |
| **3** | *"finish the nose render"* | **rendered at 3200-class settings, cropped and LOOKED AT.** `probe_rev67_nose.py`'s P3 **REFUSES** on the frame |
| **1** | *"the back opening"* | **F134 answered after ten revisions (F249), both its levers measured inert, a gate built and watched failing** |

---
## §1 THE EMBLEM — THE CONTROL DOES NOT CONTROL THE MEASUREMENT (F246)

**THIS IS THE REVISION'S RESULT AND IT INVALIDATES A PUBLISHED HEADLINE.**

`photo_mark` ends every real target with `m[ys.min():ys.max()+1, xs.min():xs.max()+1]` — **every
photograph is bbox-cropped.** P1's synthetic control is **not**: it is the raw output of `warp`,
centred on the output frame. And `fit()` searches **no translation**, while its docstring asserts
the premise that would make that safe — *"both masks are already centred on their own bounding
boxes"* — which is **false for a bbox crop**, because a projected disc's bbox centre is not its
centre.

```
    the SAME search, the SAME model, the SAME known 37 deg / 0.62 / shear / perspective view
        framed as P1 frames it        (uncropped)      IoU 0.9882
        framed as photo_mark frames every real target      0.4988
    the MARK itself, on ref_workshop.jpg                   0.7345
```

**THE CONTROL SCORES 0.25 BELOW THE SPECIMEN IT CERTIFIES.** A control that loses to its own
specimen is not a ceiling (rule 42). **So `0.9882 - 0.7345 = 0.2537` is not a shape deficit**, and
**F237's *"all seven constants buy 4.4 % of the deficit"* is a ratio against a number that is not
what it claims.** F237's *direction* survives — the levers ARE nearly inert, re-measured at
**+0.0124** — but its magnitude does not.

**HOW MUCH OF IT IS REGISTRATION:** two translation terms in the same coordinate descent lift the
mark **0.7345 → 0.8324** (`ref_workshop.jpg`) and **0.6553 → 0.7944** (`IMG_2073.jpeg`, re-cut
box). **Two independent frames, same direction, ~0.10–0.14 each.**

**AND IT IS NOT REPAIRED, DELIBERATELY (rule 44).** The same two terms lift the bbox-framed
**control** only **0.4988 → 0.5403** — still far below its 0.90 bar. **Translation is NECESSARY
and NOT SUFFICIENT**, so `fit()` was not changed, `P1b` is in the probe and **REFUSES**, and the
diagnosis prints beside it every run. **The next revision's first job on the emblem is a pose
search whose P1b PASSES. Until then the emblem has no trustworthy scalar.**

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

### §1b THE FIT DEPTH IS CLOSED (F251) — AND IT WAS ALREADY RIGHT

The item three briefs called *"still UNMEASURED"* and dropped three times. **⚠ And it is in
`t1_detail.vw_logo_fit`, NOT `t1_core.py` where the brief cites it** — `grep -n "BAND_FRAC"
t1_core.py` returns nothing (rule 18).

```
    FIT_R    ref_workshop   IMG_2073 (re-cut)
    0.700      0.6449          0.5475
    0.820      0.7362          0.6518      <- best on the fit frame, by +0.0017
    0.840      0.7345          0.6553      <- SHIPPED, and best on the INDEPENDENT frame
    1.000      0.6894          0.6334
```

**Within one sweep step of the argmax on both frames**, and the sweep spans 0.0913 so it can
plainly see the constant. `probe_rev71_emblem.py`: **3 checked, 0 FAILED.**

**AND THE ENABLING INSTRUMENT IS KEPT.** `probe_rev71_proxy.py` — a 2-D replica of the emblem
raster **PROVEN BIT-IDENTICAL to the bpy build**: IoU **1.000000**, **41255 on-pixels each side**,
at 276 rows. **~0.01 s an evaluation against ~2 s through `bpy`.** Rev 66 proved this method and
then no revision kept the replica. This one is kept, with a `prove()` that must run first (rule 3).

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
**Discarded.** **And (1) was circular as well** (rule 6): it selected *warm* pixels and reported
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
## §6 THE MACHINE AT CLOSE

```
bootstrap.sh          ALL 10 PASS (after pip install pillow), row 9: 0 ahead / 0 behind origin/main
verify_clone.sh       ALL 358 PASS on a clean tree -- 0 FIDELITY, 358 SELF-CONSISTENCY
build.py T1_VERIFY=1  VERIFY: 0 fail, 0 warn at T1_SUB=1 and T1_SUB=2
STATE.md              regenerated at T1_SUB=2; differs ONLY in provenance
judge_set.sh r71      exit 0, four _post frames -- INCLUDING hero34f, a first (F248)
probe_rev69_fitpose   5 checked, 2 FAILED -- P1b (NEW, correct refusal) and P2
probe_rev71_emblem    3 checked, 0 FAILED
probe_rev71_proxy     PROXY vs BUILT IoU 1.000000
probe_rev71_bulbs     3 checked, 1 FAILED (B2, correct); bare exit 3
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
