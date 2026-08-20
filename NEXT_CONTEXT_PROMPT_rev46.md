# NEXT CONTEXT PROMPT — rev 46

**Read this whole file before you touch anything.** It is written for a context that knows nothing
about this project. Everything you need to start is here; everything you need to be *correct* is in
`SPEC.md` and `LEDGER_rev45.md`, and this file tells you where to look.

---

## §0. HIS FOUR REPORTS, VERBATIM, AND ALL FOUR ARE ALREADY MEASURED

At the close of rev 45 the owner wrote:

> *"I still see a lot of problems, including the 100% calidad off center, the vw logo wrong, señor
> Tacombi still isn't clearer, the nose of the car is too flat which is inaccurate in shape, among
> other things."*

**Rev 45 did not argue with any of it. It measured all four before handing over, so you start with
findings and not with questions.** Every number below was watched print. The details are §5.

| his words | measured, rev 45 | where |
|---|---|---|
| *"100% calidad off center"* | **CONFIRMED, and it is a NEW defect.** The white type sits **0.1195 of the decal's width LEFT** and **0.1782 of its height BELOW** the burst's centre. The photograph has it **+0.0455 right, +0.0746 below** — so the horizontal error is **in the wrong direction** and is 0.165 of the decal wide. | §5 / W1 |
| *"the vw logo wrong"* | **CONFIRMED, with a scale-free specification of exactly what.** Vertical-only, as a fraction of the ring's diameter: the **V's apex sits at 0.254 built against 0.353 photographed — 0.099 too high, 27.7 mm on a 280 mm badge.** The V is squat and the W stretched. | §5 / W2 |
| *"señor Tacombi still isn't clearer"* | **CONFIRMED.** Michelson contrast of ink against its red ground: **0.217 built, 0.324 photographed.** Two-thirds of the contrast it should have. | §5 / W3 |
| *"the nose of the car is too flat"* | **CONFIRMED, and the ledger's existing nose finding is about a DIFFERENT AXIS.** The built nose recedes **14.3 mm over 0.70 m of half-width** — essentially planar. The only forward bulge in the whole model is one constant, `bulge = 0.019` in `t1_shell.nose_shape`. | §5 / W4 |

**Read §5 before you touch geometry.** Two of the four have a trap in them: the Calidad defect is
*not* the one rev 44 measured and closed, and the nose defect is *not* `V_POW`.

### And the thing that outranks all four

**He has now reported the VW logo in four consecutive revisions.** Rev 44 fixed its drawing, rev 45
found it was sunk 32 mm into the bodywork and fixed that, and he still says it is wrong — and rev
45's own measurement above says he is right, by 27.7 mm on the one axis nobody had checked.

> **HIS REPEAT IS A MEASUREMENT.** When he reports the same thing twice, the prior's closure was
> wrong or incomplete, and the correct response is to go and find the axis nobody looked at — not
> to re-explain the fix. Rev 45 closed the badge on the drape and did **not** check its vertical
> proportions, and said so at the time. That gap is W2.

---

## §1. THE OBJECTIVE, IN HIS WORDS

A photoreal 3D model and hero render of **Señor Tacombi** — a 1963 VW T1 Kombi converted into a taco
truck. He supplied a catalogue-grade product render of a school bus as the bar and asked for *"the
very highest resolution, fidelity, and detail possible. Cutting edge stuff, and I need you to guide
it."* And: **"Keep tuning the bus until it is perfect!!"**

The standing instruction, from the original brief and still in force:

> **WHERE THIS BRIEF AND THE MACHINE DISAGREE, THE MACHINE IS RIGHT — say so and correct the brief in
> the same revision.**

That applies to *this document* too. Rev 45 exercised it four times against its own brief.

---

## §2. THIS MACHINE IS NOT THE OLD MACHINE. READ THIS BEFORE PLANNING ANY WORK.

**Every prompt before this one was written for a slow local Mac and its advice is now partly wrong.**
The prior briefs say things like *"render small and often; render big once"* and *"a 4800×3200 at 300
samples was quoted at 4½ hours and was killed."* Some of that still holds and some of it does not.

### What is actually true here, measured this session

```
cores            4          RAM 15 GB        Blender 4.5.3 via pip install bpy
build  T1_SUB=1             ~20 s
build  T1_SUB=2             ~75-100 s        <- the GUARDED case
render 1100x760   56 spp    ~1 m 54 s        T1_SUB=1
render 1600x1100  96 spp    ~8 to 11 min PER VIEW,  T1_SUB=2
```

### The thing that is genuinely new, and the trap inside it

You have **parallel subagents and workflow orchestration**. That is a real multiplier and the prior
contexts did not have it. **But it does not multiply renders.**

> **CYCLES ALREADY USES ALL FOUR CORES. FANNING OUT RENDERS ACROSS AGENTS MAKES THEM SLOWER, NOT
> FASTER — the arms contend for the same four cores and you pay the build cost N times over.**
> A five-arm ablation run in parallel on this box finishes *later* than the same five run in
> sequence, and every arm's timing becomes meaningless for comparison.

**Fan out the things that are not renders.** They are most of the work:

* **measuring the reference photographs** — nine frames, all static, all CPU-light. Four agents each
  measuring a different frame against the same question is a genuine 4×, and it gives you
  independent readings of the same quantity, which is worth more than the speed.
* **reading and cross-checking the record** — `SPEC.md` is ~9800 lines across §10.1–§10.117 and
  `AUDIT_RECOVERED.md` has **89 unverified findings**. That is exactly the shape of work to fan out.
* **adversarial verification** — this project's entire failure mode is instruments that look healthy
  and are wrong (§4). Put a skeptic on each finding whose job is to REFUTE it, before it ships.
* **drafting probes, SPEC sections and the ledger** in parallel with a render that is already running.

**And do run renders in the background** (`run_in_background`) while you do analysis in the
foreground. An 8-minute hero should never be 8 minutes of idle.

### Render budget

He has twice said *"Kill it. Don't waste the computer."* A **1600×1100 at 96 samples** is the honest
working hero here and costs 8–11 minutes. Nothing in the current work list needs more. **Do not start
a 3200×2133 or larger without a specific reason and without telling him it is running.**

---

## §3. PROVE THE TREE — ONE COMMAND

```bash
cd /home/user/combi_render
./bootstrap.sh            # toolchain + tree.   ~1 min warm, ~5 min cold.
./bootstrap.sh --guards   # ... and both builds and all four probes.  ~10 min more.
```

`bootstrap.sh` is rev 45's and it exists because every context before it spent its first twenty
minutes on the same four things by hand. It installs `bpy`, builds the two shims at the paths **eight
files hard-code and none of which may be edited**, deepens a shallow clone, checks that **no branch
carries work `HEAD` does not have**, and runs `verify_clone.sh`. Expect **ALL 10 PASS**, and
**16 PASS** with `--guards`.

Proved from scratch: `rm -rf /tmp/blender && ./bootstrap.sh` rebuilds and passes. **The one path it
has never exercised is `pip install bpy==4.5.3`** — bpy was already present in the container it was
written in. It says so in its own header. If that row fails, the fallback is `START_HERE.md`.

**Network:** `WebSearch` works. `WebFetch` and `curl` are 403 on every domain except
`raw.githubusercontent.com`.

### Build, verify, render

```bash
/tmp/blender/blender -b -P build.py                      # T1_SUB defaults to 2
T1_VERIFY=1 /tmp/blender/blender -b -P build.py          # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=hero34f,side,front34 T1_PFX=r T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py
```

**There is no view called `hero`.** The keys are `hero34f`, `hero34r`, `front34`, `side`, `front`,
`rear`, `detail_f`, `low34`, `topdown`, `playa`, `playa_ref`, `playa_w`, `counter`. The rev-45 brief
said `hero` and it dies with `KeyError` **after a full build**.

Useful env: `T1_SUB` (**2 is the guarded case**), `T1_SAMP`, `T1_RX`/`T1_RY`, `T1_PFX`, `T1_OUT`,
`T1_SAVE`, `T1_KEY`, `T1_SCENE=playa`, `T1_CLAY`, `T1_ABLATE`, and the ablation switches
`T1_NOBEVEL`, `T1_NOCABFILL`, `T1_CATCH`, `T1_GRAIN`, `T1_BPILLAR`, `T1_SPEC`, `T1_VT`,
`T1_HL_BEZEL`, `T1_HL_LENS_RG`, `T1_HL_REFL_RG`, `T1_HL_REFL_MET`, `T1_HL_BOWL`, `T1_SHADOW`,
`T1_SHADOW_FLOOR`.

---

## §4. THE THING REV 45 LEARNED, WHICH OUTRANKS EVERY GEOMETRIC ITEM BELOW

**This project measures beautifully and its instruments keep being wrong.**

Rev 45's three new probes were wrong **eight times** before they were right, and every single error
produced a plausible number that would have been published:

* a sample contaminated by the body — **the cream renders (192,192,188), so it passes any "neutral"
  test** and the ground sample was reading the vehicle's own flank;
* **three separate kill controls** that sampled off-screen, returned `<no sample>`, and **passed**;
* a level control that read the frame's top corners and called a frame **with a hard horizon across
  it** "PURE WHITE";
* a measurement window that started 8 cm out when the whole shadow lives in the first 5;
* **three flank landmarks out of three that were behind a decal, a fringe and a rim** — because
  `world_to_camera_view` maps a point to a pixel whether or not the point can be *seen*.

And before that: the nose badge rendered as a **clock face** for thirty-five revisions while **eight
correct measurements of it existed**, every one taken in the glyph's own plane and blind to a 32 mm
error in the direction nobody looked.

> **§10.116.6 — AN INSTRUMENT THAT HAS NEVER BEEN WRONG HAS NEVER BEEN TESTED.**
> **§10.115.4 — A CONTROL IS NOT FINISHED WHEN IT PASSES. IT IS FINISHED WHEN YOU HAVE WATCHED IT
> FAIL ON THE DEFECT.** Every ablation switch listed in §3 exists to make that check cheap.
> **§10.110.8 — A PART MEASURED IN ISOLATION FROM WHAT IT IS FITTED TO IS NOT MEASURED.**

**So: render it, crop it, and LOOK at it, before and after every change.** Three probes now do the
looking for you — `probe_rev45_nose`, `probe_rev45_ground`, `probe_rev45_paint`. Copy their pattern:
**project known 3-D landmarks through the render camera and sample where they land**, never type a
crop box. And copy `probe_rev45_paint.visible()` — it is the half `probe_rev45_nose` does not have.

---

## §5. WORK LIST FOR REV 46 — his four reports first, each with its measurement and its trap

**Nothing here is blocked on him.** W5 and W6 are.

### W1 — "100% CALIDAD OFF CENTER". The type is off-centre INSIDE the decal.

Measured on `tex/calidad.png` and on `ref_playa_34.png`, as centroid offsets of the white type from
the red burst's centroid, in fractions of the decal:

| | horizontal | vertical |
|---|---|---|
| built | **−0.1195** | **+0.1782** |
| photographed | **+0.0455** | **+0.0746** |

**The horizontal error is in the wrong DIRECTION.** The type's bbox runs cols 0.155–0.645 — it
occupies the left two-thirds and stops well short of the right edge, while the burst spans
0.015–0.951.

> **THE TRAP.** Ledger finding 5 says *"the defect is COLOUR, not position"* and rev 44 closed the
> position half. **That was about the decal panel's placement ON THE VEHICLE** — Report 7's "off
> centre at 0.180 of texture width". **Nobody ever measured the type's placement WITHIN the decal.**
> Both statements are true and they are about different things. Do not re-open the placement.

The fix is in `cal_gen.py`: `starburst()`'s centre is `(w*0.505, h*0.575)` and the type is laid out
against its own coordinates. Re-centre the **type on the burst**, then re-measure with the script
above and check the burst still fills its panel.

### W2 — "THE VW LOGO WRONG". The V's apex is 27.7 mm too high, and this is measurable without the axis ratio.

**Rev 45 refused to touch the spine because de-foreshortening a three-quarter view of a circle needs
the ring's axis ratio and the two available fits disagree by 10 %.** That refusal was right for
angles and **wrong to stop there**, because vertical extents need no axis ratio at all — §10.107.2's
own rule. Rev 45 then did the vertical-only measurement and it is unambiguous.

Structure read off run-counts per row, as a fraction of the ring's vertical diameter from its top:

| landmark | photographed | built | error |
|---|---|---|---|
| V's arms clear the ring band (counter opens) | 0.147 | 0.104 | −0.043 |
| **V's apex / the central knot** | **0.353** | **0.254** | **−0.099** |
| W's outer arms leave the ring band | 0.485 | 0.507 | +0.022 |
| W's troughs reach the lower band | ~0.81 | 0.866 | +0.056 |

**The V occupies 0.15 of the ring's height built against 0.206 photographed; the W occupies 0.61
against 0.46.** The V is squat and the W stretched, which is why it still reads wrong at every size.

* Photograph: `ref_nolita_front34.jpg`, emblem rows 191–259, cols 152–192. A **red emblem on cream**
  segments cleanly; the workshop frame's chrome does not.
* The spine lives in `t1_core.vw_bars` — `V_SPINE` and `W_SPINE`. Move the V's apex DOWN and the W's
  troughs UP, in ring-radius units, and re-run the row-structure comparison.

#### W2a — THE OWNER'S POINT, AND IT CHANGES THE METHOD: **THIS IS A FACTORY PART**

At the close of rev 45 he asked: *"I imagine the logo badge has to be the same dimensions as other vw
logo badges right?"*

**He is right, and it matters more than it looks.** Confirmed on `ref_nolita_front34.jpg` at 10×: the
badge **casts a shadow onto the cream at its lower right** and the ring carries its own thickness
shading. It is a three-dimensional pressing painted red — **not a painted-on graphic.** So it is a
catalogue part with a part number and a specified diameter.

**`ROUNDEL_D` is currently a PHOTOGRAMMETRIC ESTIMATE WITH A ±30 mm ERROR BAR.** From `build.py`'s
own comment: *"the outer diameter is 0.28 ± 0.03 m … Method: D_roundel / D_aperture = (m_ro/2)(1/m_near
+ 1/m_far) = 1.384 off `ref_workshop.jpg`."* **±10.7 % on a part that has a specification.** A
catalogue figure would beat that by an order of magnitude and needs no frame at all.

**What rev 45 found, and the trap it stopped on.** The part number for a 1963 bus is
**`241853601A`** (Type 2 front emblem, 1955–1967). **A citable diameter for THAT part was not
found**, and the diameters that *were* findable are era-specific and wildly different:

| part | fits | diameter |
|---|---|---|
| `211853601E` | Bus 72½–79 | **7 in** ≈ 178 mm |
| `211853601B` | Bus 68–72½ | **9¾ in** ≈ 248 mm |
| a listed "vintage original" | probably the 1950–55 barndoor | **12½ in** ≈ 318 mm |
| **`241853601A`** | **Bus 1955–1967 — OURS** | **NOT FOUND** |

> **DO NOT GUESS FROM THE TABLE.** Four eras, four sizes, and picking the wrong row would be worse
> than the ±30 mm estimate already in the tree. Rev 45 did **not** change `ROUNDEL_D`.

**How to close it, in order of preference:**

1. **A supplier's dimensioned listing or a restoration manual for `241853601A`.** `WebSearch` works in
   this environment; `WebFetch` and `curl` are 403 on every domain except `raw.githubusercontent.com`,
   so you may be able to *find* a page and not *read* it. Search result snippets carrying the number
   are usable if the part number is in the same snippet as the dimension.
2. **Ask him.** He is standing next to the vehicle. *"Tape measure across the VW badge on the nose,
   outer edge to outer edge"* is a fifteen-second job and it is worth more than any photograph in
   this repository. **This is now the cheapest open item in the whole project** — add it to
   `PHOTOS_WANTED` as a MEASUREMENT rather than a photograph.
3. Only then fall back to photogrammetry.

**AND THE BIGGER PRIZE IS THE GLYPH, NOT THE RING.** The VW monogram is a **registered trademark with
fixed proportions**. Four revisions have now tried to derive its spine from a 68-pixel emblem and he
has reported it wrong every time. **Build the canonical mark and use the photograph to VERIFY, not to
derive** — the numbers in W2's table above become the acceptance test rather than the source. That
inverts the method that has failed four times, and it is what his question implies.


* **`probe_rev44_lampmove` C5/C6 hold the badge's HEIGHT on the nose from two chains and must stay
  6/0.** They watch where the badge sits, not what it draws; this change must not move them.
* SPEC:7005 forbids moving the roundel in the same change as the lamps. Still in force.

### W3 — "SEÑOR TACOMBI STILL ISN'T CLEARER". His third report IS the sanction.

Michelson contrast of the script's ink against the red it sits on: **0.217 built, 0.324
photographed** (rev 45's boxes; the ledger's finding 30 has 0.269 / 0.466 on different boxes — the
ratio is the same story either way).

> **THE TRAP, AND IT IS THE REASON THIS HAS NOT BEEN FIXED IN THREE REVISIONS.** Finding 19 says
> `senor.png` emits opaque mean (205,194,200) against a *measured* target of (127.4,124.9,130.0).
> **So darkening the ink toward its own measured target makes it LESS legible, not more.** The two
> findings pull opposite ways and every prior revision stopped there and asked for sanction.

**He has now asked three times. That is the sanction.** Ship a deliberate departure, say in SPEC that
it *is* one, and record which measurement it departs from. The likely lever is not the ink's value
at all but its **edge** — a darker outline or a drop shadow raises Michelson without moving the ink's
mean toward or away from finding 19's target. Measure before and after.

### W4 — "THE NOSE IS TOO FLAT". It is, by a lot — and it is NOT `V_POW`.

Raycast against the built body, surface x versus y at z = 1.25, as mm behind the centreline crown:

```
    y=0.00   0.10   0.20   0.30   0.40   0.50   0.60   0.70   0.80
      0.0   -0.4   -1.6   -3.6   -6.5  -10.1  -12.8  -14.3  -32.5
```

**14.3 mm of recession over 0.70 m of half-width.** The nose is a plane. The only forward bulge
anywhere in the model is a single constant in `t1_shell.nose_shape`:

```python
    bulge = 0.019 * w * max(0.0, 1.0 - r)      # 19 mm, blended over x 1.86..2.03
```

> **THE TRAP.** Ledger finding 6 is *"Report 1 — the nose shape, `V_POW` locked 0.60"* and it is
> **about a different axis entirely**. `V_POW_Z` drives `zV(y)`, the **painted two-tone break
> line's** height across the nose. It is a paint curve. It has nothing to do with how far the sheet
> metal bulges forward, and fixing it would not have answered him.

**What rev 45 could NOT do and you must.** It has no photographed anchor for the plan curvature. It
tried a horizontal luminance profile across the cream nose panel and **threw the result away** —
the render and photograph boxes were not comparable and publishing it would have been a number about
nothing. Candidate methods, in the order rev 45 would try them:

1. **`ref_nolita_front34.jpg` / `ref_playa_34.png` shading gradient** across the cream nose, with the
   render's box chosen by **projecting the same 3-D band** rather than by eye. That fixes the exact
   flaw that killed rev 45's attempt.
2. **The corner wrap in silhouette.** In a three-quarter, a domed front turns away smoothly and a
   flat one ends in a hard corner. `ref_workshop.jpg` is 1200×824 and shows a T1 nose at
   three-quarter.
3. **Ask him for a head-on frame of the nose** — §6 already wants one for the badge and it would
   settle both. One photograph, two findings.

---

### W5 — BLOCKED ON HIM: the sign board (Q5 of `rev45_ba.png`)

The build paints the raised board as a **flower mural with menu strips**. Every frame we hold shows a
hand-chalked **BLACKBOARD** in a cream frame, TACOMBI across the top, BIENVENIDOS down the side.
Nobody has ever asked him which he wants. Ledger finding 39.

### W6 — BLOCKED ON HIM: the paint and the studio (Q6 of `rev45_ba.png`)

Fully instrumented by `probe_rev45_paint` and **deliberately not gated**:

| | built | photographed | σ |
|---|---|---|---|
| body red, G/R of red÷cream | 0.455 | 0.223 ± 0.066 | **3.5** |
| hubcap red, G/R of cap÷cream | 0.603 | 0.274 ± 0.096 | **3.4** |
| cream warmth, (R−B)/G | +0.0263 | +0.037 ± 0.013 | 0.8 |

**It is ONE finding, not three.** The hubcaps are wrong the same way as the flank; the cream's hue is
right and reads grey only because it sits against pure white with a washed red beside it. The albedo
is right to 0.4 σ. About half the excess is the white cyclorama's own specular — `T1_SPEC=0` alone
moves it 0.455 → 0.347 — and **the same rig is why the vehicle needed §10.116's shadow work.**
Softening it trades the catalogue-clean white background he supplied as the bar. **His call.**

### W7 — the rest of the burn-down

`LEDGER_rev45.md` §6: finding 2 (**no UV layout on the body at all**, ~56 % self-overlap), 11 and 13
(both top of the photo list), 16 (**a trunk lid** — `grep -c trunk` is 0), 17, 21, 22 (**89
unverified findings in `AUDIT_RECOVERED.md`** — fan this out), 26, 27, 39, 40. The cab is still
**class 4**: built, type-correct, and **not measured**, because no frame resolves it.

---

## §6. WHAT ONLY HE CAN GIVE — `PHOTOS_WANTED_rev45.md` is the list

Ranked, and every entry says *why it cannot be settled from what we hold*:

1. **The off side** — a flat-on right flank. 804.9 mm, graded **E**, and **we do not know what is
   painted on it.**
2. **Anything settling the absolute roof height.** One photo of him beside it, plus his height.
3. **A TAPE MEASURE ACROSS THE NOSE BADGE, outer edge to outer edge.** Fifteen seconds, and it
   replaces a ±30 mm photogrammetric estimate on a catalogue part. **The cheapest open item in the
   project.** See W2a.
4. **The nose, SQUARE ON** — now worth double: it settles W2's remaining angles *and* W4's plan
   curvature. Reading angles off a three-quarter needs the ring's axis ratio and the two fits
   available disagree by 10 %.
5. **The cab interior, square on through the windscreen.** The cab is class 4.
6. The sign board (W5), a head-on rear and the trunk lid, and the cab door's full outline with the
   art on it.

**Do NOT ask him again for:** the over-rider assembly, the signboard's existence, region 3, the ten
flower heads, tyre diameter, the counter slab, break-to-sill, the Z-ladder's gate, whether it is one
vehicle (**it is**), whether the door art stretches (**it does not**), or the three Nolita frames
(**he sent them; they are tracked**).

---

## §7. SETTLED — DO NOT RE-OPEN

* **The paint's *finish*.** §10.104.8 refuses it in writing. **W6 is about the STUDIO, not the
  finish, and does not re-open this.**
* **Finding 29** — "the red renders 2× too light" — retracted, a unit error.
* **`T1_CATCH=0`** — refused at rev 12 and **re-refused at rev 45 with numbers**: it buys the contact
  shadow and pays with a backdrop whose row-to-row step goes 0.100 → 22.123 DN.
* **§10.100's door wrap** — retracted by §10.102, partially restored by §10.106.
* **The rear bumper was removed after the conversion**; the over-rider bar and posts were withdrawn
  by the owner at rev 37. **There is no fourth serving bay.**
* **The sign props' `LID_X1 + 0.16` / `LID_X0 - 0.16` is an INSET.** `LID_X1` is the aft end at
  −1.0700. **Two contexts have now "fixed" this and both were wrong.** Run the build before you
  believe the source.

---

## §8. THE RULES. EVERY ONE WAS EARNED BY A DEFECT.

1. **A claim in prose is not a guard** (§10.45).
2. **A constant tuned against another constant must be EXPRESSED in terms of it** (§10.25).
3. **Read each probe's own summary line, never its exit code.**
4. **Never put a figure in an acceptance test unless you watched it print** (rev 13). Four instances
   now; the fourth was rev 45's own and `verify_clone.sh` caught it in a minute.
5. **Do not inherit a guard's rationale along with its shape** (rev 23).
6. **An ordinal fact licenses a SIGN, never a SHAPE** (§10.102.8).
7. **A leading question is not evidence, even when the answer is yes** (§10.102.8).
8. **A measurement's window is part of the measurement** (§10.106.6, and §10.116.2 the hard way).
9. **A threshold "lowest X" trace is only valid if the feature's FAR SIDE is resolved** (§10.106.7).
10. **A detail you cannot see is not a detail** (§10.105.7) — **and a detail you looked at badly is
    not looked at** (§10.115.4).
11. **When a fix cannot be built at any tolerance, suspect the thing it is fixing** (§10.102.8).
12. **Add the guard in the same edit as the change.** Rev 45's emblem guard fired twice on its own
    change, at −15.11 mm and −3.59 mm, and both were real.
13. **Inventory the frames you already hold before asking him for a new one.**
14. **Prefer dimensionless measurements** (§10.106.3). Every rev-45 paint number is one.
15. **Retract in the same revision you find the error** — in SPEC, in the ledger, and to him.
16. **A PART MEASURED IN ISOLATION FROM WHAT IT IS FITTED TO IS NOT MEASURED** (§10.110.8).
17. **A REVISION THAT IS NOT MERGED DID NOT HAPPEN** (§10.113.5). `bootstrap.sh` enforces it.
18. **A RATIO THAT IS RIGHT FOR THE WRONG REASON IS NOT A CONTROL** (§10.111.2).
19. **A CONTROL IS NOT FINISHED WHEN IT PASSES. IT IS FINISHED WHEN YOU HAVE WATCHED IT FAIL ON THE
    DEFECT** (§10.115.4).
20. **AN INSTRUMENT THAT HAS NEVER BEEN WRONG HAS NEVER BEEN TESTED** (§10.116.6).
21. **NEW, rev 46 — HIS REPEAT IS A MEASUREMENT.** If he reports the same defect twice, the prior
    closure was wrong or incomplete. Go and find the axis nobody checked. All four items in §0 are
    repeats, and all four turned out to be right.

---

## §9. THE STATE OF THE MACHINE AT HANDOFF

```
bootstrap.sh      ALL 10 PASS   (16 with --guards; from bare: rm -rf /tmp/blender first)
build             T1_SUB=2, clean
verify.py         VERIFY: 0 fail, 0 warn  at T1_SUB=1 AND T1_SUB=2
audit.py          0 fail, 0 warn, 221 meshes, 5 materials constant-rough
verify_clone.sh   ALL 69 PASS on a clean tree
probes            probe_rev45_nose      8 checked, 0 FAILED   (C5 a KILL, red by design)
                  probe_rev45_ground    4 checked, 0 FAILED   (C4 a KILL)
                  probe_rev45_paint     4 checked, 0 FAILED   (C4 a KILL)
                  probe_rev44_lampmove  6 checked, 0 FAILED
SPEC              sec.10.1 .. sec.10.117
frames            9 tracked + 5 IMG_* uploads kept as provenance
branch            claude/project-improvement-id3a9o
```

**AND ONE THING THAT IS NOT DONE.** At handoff this branch is **35 commits ahead of `origin/main`
and 0 behind**. Nothing is stranded on any other branch — but the work reaches `main` only through a
pull request, and rev 45's whole §0 finding is what happens when it does not.
**`git rev-list --count origin/main..HEAD` before you start and again before you finish.**

**Go and read §0 again before you start.**
