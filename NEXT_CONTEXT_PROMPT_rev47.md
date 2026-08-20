# NEXT CONTEXT PROMPT — rev 47

**Read this whole file before you touch anything.** It is written for a context that knows nothing
about this project. Everything you need to start is here; everything you need to be *correct* is in
`SPEC.md` and `LEDGER_rev46.md`, and this file tells you where to look.

---

## §0. WHAT HE SAID THIS REVISION, AND WHAT IS LEFT

Rev 46 answered four standing reports and three new ones. **`LEDGER_rev46.md` is the record — read
its §0 table first.** The short version:

| his words | state |
|---|---|
| "100% calidad off center" | **FIXED.** (−0.1167, +0.1117) → (+0.0001, −0.0001), guarded, guard watched fail. |
| "the vw logo wrong" | **FIXED.** Landmark residual 0.1167 → 0.0347, at the photograph's noise floor. |
| "señor Tacombi still isn't clearer" | **HALF FIXED — YOUR FIRST JOB. See §1.** |
| "the nose is too flat" | **CONFIRMED, NOT FIXED.** See §2. |
| "remove the upper triangles" | **DONE.** |
| "the lines seem to be vent slats" | **DONE**, and it leaves new geometry to build. See §3. |
| "the bottom word does not collide with the top one either" | **CONFIRMED, measured, NOT FIXED.** See §4. |
| "the lettering looks off as well" | **NOT EVALUABLE at 23×39 px.** Ask him. See §7. |

> **HIS REPEAT IS A MEASUREMENT.** If he reports the same defect twice, the prior closure was wrong
> or incomplete. Go and find the axis nobody checked. Every repeat in rev 45 and rev 46 turned out
> to be right, and in every case the missing axis was one a prior revision had explicitly declined
> to look at.

---

## §1. YOUR FIRST JOB — the script is BLURRED, and the cause is already found

**Three revisions chased a contrast number for a sharpness defect.** Rev 46 fixed the contrast half
(*Señor* was 2.7× too dark and is now on its photographed target) and then found the real fault.

**The cause is arithmetic, not art.** In `script_gen.py`:

* `Canvas` draws at `SS = 12` — **3552 px across**.
* `Canvas.alpha()` **box-downsamples that to mask space, 271 px across the ink** — throwing away all
  twelve times of it.
* `main()` then **LANCZOS-upscales those 271 px to `OUT_W = 4096`**.

The texture is 4096 px wide carrying **271 px of real detail**. Every edge is a 15-px ramp. The
3552-px raster it threw away is already almost exactly the output resolution.

**The fix, drafted by rev 46 and deliberately not applied** (it must not ride in on a colour commit):

1. add `Canvas.alpha_box(k)` that downsamples by `k` rather than by `SS`;
2. keep `alpha() = alpha_box(SS)` so the existing `_ref_mask()` equality guard stays **bit-identical**
   — that guard compares mask-space rasters exactly, and breaking it silently is the obvious trap;
3. have `main()` crop the hi-res raster at `[y0*SS:(y1+1)*SS, x0*SS:(x1+1)*SS]` before resizing.

That turns a 15.1× upscale into a 1.26× one.

**Use the right metric this time.** The 10–90 % alpha edge width divided by the mean stroke width —
dimensionless, comparable between a 4096-px texture and a 1024-px photograph, and it is what
"clearer" actually means. Built now: **0.215** of ink pixels lie in the 0.1–0.9 alpha band. Measure
built against `ref_side.jpg` before and after.

**And look at it.** Composite `tex/senor.png` over the body red `(196,49,36)` and put it beside
`ref_side.jpg` rows 462–598, cols 318–614 at matched magnification. The photograph has hard corners,
legible spirals in the a/o/b and a readable "Señor" **with its tilde**. That is the bar.

---

## §2. W4 — the nose is flat, and it still has no photographed anchor

Raycast against the built body at z = 1.25, mm behind the centreline crown:

```
    y=0.00   0.10   0.20   0.30   0.40   0.50   0.60   0.70
      0.0   -0.4   -1.6   -3.6   -6.5  -10.2  -12.9  -14.3
```

**14.3 mm over 0.70 m of half-width — a plane.** The only forward bulge in the whole model is one
constant, `bulge = 0.019` in `t1_shell.nose_shape`.

> **THE TRAP.** Ledger finding 6, *"the nose shape, `V_POW` locked 0.60"*, is about a **different
> axis**. `V_POW_Z` drives `zV(y)`, the **painted** two-tone break line's height. It is a paint
> curve. Fixing it would not have answered him, and `verify_clone` locks it at 0.60 for a reason.

**Rev 46 dispatched a measurement task for the anchor and its result had not returned when the
revision was recorded. Do not assume it succeeded.** Look for a report; if there is none, run it
yourself. The three candidate methods, in order:

1. **Shading gradient across the cream nose panel** in `ref_nolita_front34.jpg` / `ref_playa_34.png`,
   with the render's comparison box chosen by **projecting the same 3-D band through the render
   camera** — never typed. That is the exact flaw that killed rev 45's attempt.
2. **The corner wrap in silhouette.** A domed front turns away smoothly; a flat one ends in a hard
   corner. `ref_workshop.jpg` is 1200×824 and shows a T1 nose at three-quarter.
3. **Published T1 body dimensions.** `WebSearch` works.

**Whatever you build, watch a control fail on it:** a rendered flat panel and a rendered domed panel
must give different numbers, or the estimator is blind. Rev 45 threw its result away rather than
publish a number about nothing, and that was the right call.

---

## §3. NEW GEOMETRY — the model has NO REAR VENTS

`grep -rn 'vent|louvre|louver|slat|intake'` over every source returns the cab door's quarter-light
and `studio.py`'s lighting rig, **and nothing else**. The T1's rear air-intake louvres were being
faked as two red bars inside `tex/calidad.png` — wrong colour (they are dark grey), wrong material,
and with no depth they can neither self-shadow nor catch a highlight. Rev 46 retired them from the
artwork at his instruction. **Nothing replaces them yet.**

They are visible in `ref_playa_34.png` above the Calidad burst and, per him, in the workshop side
shot. **Count, pitch, length and height above the decal are all unmeasured** — see §7.

---

## §4. TO EVALUATE — the two words collide

**Measured, confirmed, not fixed.** In the built decal "100%" and "Calidad" **share 1110 pixels**.
Their boxes overlap by 0.0335 of the canvas height, **14.4 % of the "100%" cap height**:

```
  100%     x 0.3033-0.6381   y 0.3390-0.5716   (h 0.2326)
  Calidad  x 0.3304-0.7660   y 0.5381-0.7890   (h 0.2509)
```

The two anchors are `(0.150, 0.395)` and `(0.180, 0.645)` plus `TYPE_SHIFT`. Their **relative**
offset is untouched by rev 46's centring, which moved the block as one.

> **THE TRAP, AND THE GUARD WILL CATCH YOU.** Opening the gap changes the relative offset, which
> moves the block's centroid off the burst. **Re-derive `TYPE_PRE_CENTROID` and `TYPE_SHIFT` in the
> same edit.** `cal_gen` refuses to write a decal whose type is more than 0.004 off centre.

---

## §5. THIS MACHINE, AND THE ONE COMMAND THAT PROVES THE TREE

```bash
cd /home/user/combi_render
./bootstrap.sh            # toolchain + tree.   ~1 min warm, ~5 min cold.  ALL 10 PASS
./bootstrap.sh --guards   # ... and both builds and the probes.  ~10 min more.
```

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   (bpy already present here)
build  T1_SUB=1   ~20-30 s        build  T1_SUB=2   ~75-100 s   <- the GUARDED case
render 900x620   40 spp  ~2 min   render 1600x1100  96 spp  ~8-11 min PER VIEW
script_gen.py ~25 s      cal_gen.py ~3 s     the VW glyph alone builds in ~4 ms
```

```bash
/tmp/blender/blender -b -P build.py                      # T1_SUB defaults to 2
T1_VERIFY=1 /tmp/blender/blender -b -P build.py          # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=hero34f,side,front34 T1_PFX=r T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py
```

**There is no view called `hero`.** The keys are `hero34f`, `hero34r`, `front34`, `side`, `front`,
`rear`, `detail_f`, `low34`, `topdown`, `playa`, `playa_ref`, `playa_w`, `counter`. `detail_f` is the
nose close-up and it is the one that showed the emblem.

**Parallelism:** Cycles already uses all four cores — **fanning renders across agents makes them
slower**. Fan out the things that are *not* renders: measuring frames, cross-checking the record,
adversarial verification. Run renders with `run_in_background` while you analyse in the foreground.

**Network:** `WebSearch` works. `WebFetch` and `curl` are 403 on every domain except
`raw.githubusercontent.com`.

---

## §6. THE THING THAT OUTRANKS EVERY ITEM ABOVE

**This project measures beautifully and its instruments keep being wrong.** Rev 46 caught **five**
instrument failures, four of them its own, and every one produced a plausible number that would have
been published:

* a centroid estimator that reported **the same answer for every truth value tried** — (0,0),
  (±0.10, 0), (0, ±0.10), (−0.14, +0.13) — because its mask trapped cream between the burst's spikes.
  It had already been published as a measurement in the rev-46 brief. **Retracted.**
* a landmark defined as "first 3-run row after L3", which landed on a transient that exists at some
  exposures and not others, making a **stable** photograph look unstable and sending a solver at the
  wrong target.
* a registration defined as "first 2-run row", moved 0.088 by a **two-pixel noise speck**.
* a solver whose own console reported a residual **26 % better than the truth**, because it read the
  constants in a scene it had already built in.
* a hypothesis — "the glyph's strokes are too thick" — that came from **squashing a circular raster
  to an elliptical aspect** and evaporated on measurement (photograph 0.1528, built 0.1514).

> **§10.116.6 — AN INSTRUMENT THAT HAS NEVER BEEN WRONG HAS NEVER BEEN TESTED.**
> **§10.115.4 — A CONTROL IS NOT FINISHED WHEN IT PASSES. IT IS FINISHED WHEN YOU HAVE WATCHED IT
> FAIL ON THE DEFECT.**
> **§10.110.8 — A PART MEASURED IN ISOLATION FROM WHAT IT IS FITTED TO IS NOT MEASURED.**

**Two patterns rev 46 adds, both cheap and both decisive:**

* **Calibrate against a synthetic with a known answer, at the real data's resolution.** Displace the
  thing you are measuring by a known amount and check the instrument tracks it. That is what exposed
  the blind centroid in ten minutes.
* **A horizontal divided by a horizontal at the same row is invariant to rotation about a vertical
  axis.** The cosine cancels. This is what made the VW glyph's arm angle measurable after rev 45 had
  correctly refused it — the axis ratio is never needed. The same logic as §10.107.2, on the other
  axis. **Reach for it before declaring anything unmeasurable in a three-quarter view.**

**And: render it, crop it, and LOOK at it, before and after every change.** Every real finding this
revision came from looking at an image, not from a number. The script's blur, the invented pennants,
the vent slats, the colliding words — all four were invisible in the metrics and obvious on screen.

---

## §7. WHAT ONLY HE CAN GIVE

1. **The "100 % Calidad" decal, square on and close.** Settles the lettering he reported ("the
   lettering looks off as well"), the target word spacing for §4, the burst's spike count and
   proportions, and the pink star's position. **`ref_playa_34.png` is the only frame that shows this
   decal at all and the burst spans 23 × 39 px in it** — nothing about a typeface is measurable
   there. This is now the highest-value missing frame for the artwork.
2. **The rear panel square on**, showing the vent slats — count, pitch, length, height above the
   decal. Needed to build §3's missing geometry rather than guess it.
3. **The off side** — a flat-on right flank. 804.9 mm, graded **E**, and we do not know what is
   painted on it.
4. **The nose, square on** — settles W2's remaining angles *and* W4's plan curvature.
5. **The cab interior, square on through the windscreen.** The cab is still class 4.
6. Anything settling the absolute roof height; the sign board (W5); a head-on rear.

**Do NOT ask him again for:** the over-rider assembly, the signboard's existence, region 3, the ten
flower heads, tyre diameter, the counter slab, break-to-sill, the Z-ladder's gate, whether it is one
vehicle (**it is**), whether the door art stretches (**it does not**), the three Nolita frames
(**he sent them**), **the bunting pennants** or **the vent slats** — he has answered the last two.

---

## §8. STILL BLOCKED ON HIM

* **W5 — the sign board.** The build paints a flower mural with menu strips; every frame we hold
  shows a hand-chalked **blackboard** in a cream frame. Nobody has ever asked him which he wants.
* **W6 — the paint and the studio.** `probe_rev45_paint`: body red G/R 0.455 built against
  0.223 ± 0.066 photographed (**3.5 σ**); hubcap red 0.603 against 0.274 ± 0.096 (**3.4 σ**); cream
  warmth right to 0.4 σ. **It is ONE finding, not three.** About half the excess is the white
  cyclorama's own specular (`T1_SPEC=0` moves it 0.455 → 0.347), and softening it trades the
  catalogue-clean white background he supplied as the bar. **His call.**
  **W6 now also gates part of W3** — the script's remaining contrast shortfall is the ground being
  11 % too bright, not the ink, and rev 46's declared tarnish departure retires itself when W6 lands.

---

## §9. SETTLED — DO NOT RE-OPEN

* **The paint's *finish*.** §10.104.8 refuses it in writing. W6 is about the **studio**, not the finish.
* **Finding 29** — "the red renders 2× too light" — retracted, a unit error.
* **`T1_CATCH=0`** — refused at rev 12 and re-refused at rev 45 with numbers.
* **§10.100's door wrap** — retracted by §10.102, partially restored by §10.106.
* **The rear bumper was removed after the conversion**; the over-rider bar and posts were withdrawn
  by the owner at rev 37. **There is no fourth serving bay.**
* **The sign props' `LID_X1 + 0.16` / `LID_X0 - 0.16` is an INSET.** Two contexts have now "fixed"
  this and both were wrong. Run the build before you believe the source.
* **The Calidad decal PANEL's placement on the vehicle** (Report 7). Rev 46 fixed the type's
  placement *within* the decal — a different thing. The panel placement stays closed.

---

## §10. THE RULES. EVERY ONE WAS EARNED BY A DEFECT.

1. **A claim in prose is not a guard** (§10.45).
2. **A constant tuned against another constant must be EXPRESSED in terms of it** (§10.25).
3. **Read each probe's own summary line, never its exit code.**
4. **Never put a figure in an acceptance test unless you watched it print** (rev 13). Rev 46 added
   the fifth instance — a solver reporting a residual better than the truth.
5. **Do not inherit a guard's rationale along with its shape** (rev 23).
6. **An ordinal fact licenses a SIGN, never a SHAPE** (§10.102.8).
7. **A leading question is not evidence, even when the answer is yes** (§10.102.8).
8. **A measurement's window is part of the measurement** (§10.106.6).
9. **A threshold "lowest X" trace is only valid if the feature's FAR SIDE is resolved** (§10.106.7).
10. **A detail you cannot see is not a detail** (§10.105.7) — **and a detail you looked at badly is
    not looked at** (§10.115.4).
11. **When a fix cannot be built at any tolerance, suspect the thing it is fixing** (§10.102.8).
12. **Add the guard in the same edit as the change.**
13. **Inventory the frames you already hold before asking him for a new one.**
14. **Prefer dimensionless measurements** (§10.106.3).
15. **Retract in the same revision you find the error** — in SPEC, in the ledger, and to him.
16. **A PART MEASURED IN ISOLATION FROM WHAT IT IS FITTED TO IS NOT MEASURED** (§10.110.8).
17. **A REVISION THAT IS NOT MERGED DID NOT HAPPEN** (§10.113.5).
18. **A RATIO THAT IS RIGHT FOR THE WRONG REASON IS NOT A CONTROL** (§10.111.2).
19. **A CONTROL IS NOT FINISHED WHEN IT PASSES. IT IS FINISHED WHEN YOU HAVE WATCHED IT FAIL ON THE
    DEFECT** (§10.115.4).
20. **AN INSTRUMENT THAT HAS NEVER BEEN WRONG HAS NEVER BEEN TESTED** (§10.116.6).
21. **HIS REPEAT IS A MEASUREMENT** (rev 46). All four standing reports were repeats; all four were right.
22. **NEW, rev 47 — CALIBRATE AGAINST A KNOWN DISPLACEMENT, AT THE REAL DATA'S RESOLUTION.** An
    estimator that returns the same answer for a defect and its absence is blind, and it will look
    healthy forever. Rev 46 published one such number and retracted it the same revision.
23. **NEW, rev 47 — A HORIZONTAL OVER A HORIZONTAL AT THE SAME ROW NEEDS NO AXIS RATIO.** Before
    declaring anything unmeasurable in a three-quarter view, check whether the ratio you want can be
    formed on one axis. This unlocked an angle rev 45 had correctly refused.

---

## §11. THE STATE OF THE MACHINE AT HANDOFF

```
bootstrap.sh      ALL 10 PASS
build             T1_SUB=1, clean
verify.py         VERIFY: 0 fail, 0 warn
verify_clone.sh   ALL 83 PASS on a clean tree      (69 at rev 45)
probes            probe_rev46_vw        5 checked, 0 FAILED   (C3 a KILL, red by design)
                  probe_rev44_lampmove  6 checked, 0 FAILED   <- held across the glyph change
                  probe_rev45_nose / _ground / _paint   unchanged from rev 45
SPEC              10.118 (W1), 10.119 (W2), 10.120 (W3) written into the sources
branch            claude/new-session-3tof54
```

**`probe_rev46_reports.py` IS PARTLY RETRACTED AND MUST BE REBUILT BEFORE IT IS QUOTED.** Its R1
photographed target is withdrawn (§6, and `LEDGER_rev46.md` §1) and its estimator is the blind one.
Its R2 target line carries a transcription error corrected in `LEDGER_rev46.md` §2. Its R3 box is
hand-typed and its ink mask is the same bright/low-saturation rule that fails on cream.
**`probe_rev46_vw.py` is the model to copy** — it identifies landmarks by structure, registers on a
feature nothing it solves can move, and carries a kill control that is red by design.

**`git rev-list --count origin/main..HEAD` before you start and again before you finish.** The work
reaches `main` only through a pull request.
