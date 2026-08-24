# LEDGER rev 58 — every number, with where it came from

**Read `NEXT_CONTEXT_PROMPT_rev59.md` for the map. This file is the arithmetic.**

Grades follow `OPEN_FINDINGS.md`: `MEASURED-rev58` means a script in this repo
printed it during this revision.

---

## §1. PICKUP — MEASURED, NOT TRANSCRIBED

```
rev 57 was MERGED, through PR #17 (c1e5134).
HEAD 0 ahead / 0 behind origin/main.
All 15 remote branches 0 ahead.
git diff --name-only HEAD...origin/main  -> EMPTY.  No photographs arrived.
bootstrap.sh  ALL 10 PASS  (row 9 = the branch check, passing)
```

**AND THE EIGHTH DELETION HAPPENED, ON SCHEDULE.** `git fetch --prune` printed

```
- [deleted]  (none) -> origin/claude/combi-render-rev-58-lg0746
```

the branch this revision was told to develop on, deleted before it had pushed
anything. That is the **THIRD RUNNING** revision to lose its own designated
branch at pickup, and the rev-58 brief predicted it in those words. **Expect it
at rev 59.**

**THE TOOLCHAIN WAS NOT PRESENT.** `/tmp/blender/blender` did not exist on this
clone; `bpy` was not importable. `./bootstrap.sh` reproduced both from nothing
and returned ALL 10 PASS. The `pip install bpy==4.5.3` branch ran again and
worked. This is what that script is for and it is the second recorded cold run.

---

## §2. ITEM A0 — THE STUDIO RIG (F51). DONE

The rig — `cyclorama` / `lighting` / `cabin_fill` / `camera` — was built inside
`build.py`'s `if os.environ.get("T1_PREVIEW"):`, so every tool that exec'd
`build.py` to MEASURE got a scene with no lights, silently.

**FIVE copies existed, not the two the record claimed:** `build.py`,
`hq_render.py`, `probe_rev58_gloss.py`, `probe_rev54_look.py`, and
`render_rev36_bumper.py` — the fifth was **incomplete**, missing `cabin_fill`
entirely, so that script rendered the cab dark while every other view lit it.
All five now call `studio.rig()`.

**THE DUPLICATION WAS THE LESSER HALF. THE SILENCE WAS THE ONE THAT BIT.**
`studio.assert_lit()` refuses to render a scene with 0 lights and no world, and
it sits in `render_set()`, the one choke point every preview render passes
through. **WATCHED FAILING** with `T1_NORIG=1`:

```
RuntimeError: REFUSING TO RENDER AN UNLIT SCENE -- 0 light objects and world
strength 0.000.  The studio rig was never built.
```

Emissive materials are deliberately **not** counted: the black-bus frame HAD a
lit bulb string, and *"something is emitting"* is exactly the reading that let
it through.

### §2.1 THE CONTROL THAT STOPPED A FALSE REGRESSION BEING REPORTED

Pre- and post-refactor renders of one 200×140 frame at 4 spp differed by
**max 41 DN, mean 0.473**. That looks like a regression. Two runs of the **SAME**
code differ by **max 41, mean 0.469**:

| pair | max | mean |
|---|---|---|
| new vs new (same code, two runs) | 41 | 0.4693 |
| old vs new | 41 | 0.4726 |
| old vs new (second run) | 41 | 0.4799 |

Cycles is nondeterministic at this sample count and the refactor sits inside
that noise. **Without the control this would have been published as a real
change.**

Positive control on the new path: `rig: 9 light(s), 1185 W total, world 0.050`,
frame written.

---

## §3. F58 — A VERIFIER ROW THAT PASSED ONLY IN THE TREE THAT WROTE IT

Found by running `./verify_clone.sh`, not by reading it.

`ck "gloss_compare is exposure-free"` called `gloss_compare.py` with **no
argument**. The script's default was a hard-coded **`out/r57_hero.png`** — and
`out/` is untracked and starts **EMPTY on every clone**. So the row passed for
its author and failed for everybody else, reporting the missing file as

```
FAIL  gloss_compare is exposure-free   got MOVED:[]  want OK
```

**an ABSENT INPUT dressed as a MOVED STATISTIC**, pointing the reader at the
estimator instead of at the path. This is the rev-57b audit's own lesson —
*"the sweep checked `os.path.exists` on the machine that WROTE the brief"* —
recurring one revision later, inside a verifier row.

**FIXED** by making exposure invariance a property of the ESTIMATOR:
`gloss_compare.py --selftest` runs the real `spread()` over a synthetic red
patch. No frame, no filename to rot. The live default now takes the newest
`out/*_hero.png` and prints `NO RENDER` in those words when there is none.

**WATCHED FAILING** via `T1_GC_ABSSPREAD=1`, which drops the `/p50`:

```
x0.70  spread 35.8691
x1.00  spread 51.2416
x1.40  spread 71.7382
SELFTEST FAIL -- exposure-free     rc=1
```

**Those three figures were TYPED AS A PREDICTION first** (0.5090 / 0.7271 /
1.0180) **and were wrong by two orders of magnitude.** Corrected in the same
edit. Rule 5, caught by obeying rule 5.

---

## §4. ITEM A — THE GLOSS (F44). LEVER TAKEN, CEILING MEASURED

### §4.1 F59 — THE GATE'S HEADROOM WAS A THIRD ARTWORK

Painted the window and looked, before trusting the number.

`spread()`'s red mask (`R > G*1.35 & R > B*1.35`) correctly excludes cream,
chrome, the silver script and the teal: the kept set is **95.0 % body red**. So
the raw rectangle's **42.9 %** red fraction — my first reading — **OVERSTATES
the problem, and that is stated because it was wrong.**

But **3.4 %** of the kept pixels are the gold flank ink and they are the BRIGHT
ones: the p99 pixels average RGB **(194.8, 119.0, 78.7)**, G/R **0.61**. And
HEADROOM is defined on p99.

| statistic | render | photo |
|---|---|---|
| SPREAD, excluding the ink | **+0.6 %** | +0.8 % |
| HEADROOM, excluding the ink | **−31.6 %** | +0.1 % |

**THOSE TWO FIGURES ARE CORRECTIONS, MADE AT THE CLOSE OF THIS REVISION.** I
first published **−0.2 %** and **−29.4 %** from an exploratory script that
applied the tighter test in a different order relative to the erosion (n 32418
against the shipped path's 27510). `audit_adversary.py` recomputed the second
one at close and disagreed, so both were re-derived **through the shipped
instrument** — `gloss_compare.py` with and without `T1_GC_LOOSEMASK=1` — and
those are the numbers above. **The conclusion does not move:** the spread ratio
reads **0.3918** loose against **0.3911** tight, so the headline is robust, and
the headroom still falls by about a third.

**The headline 0.392 is ROBUST and survives. The headroom is not:** the render's
is **0.090** of the photograph's, **not the 0.132 published at rev 57b**. The
correction makes the deficit **worse**. `T1_GC_LOOSEMASK=1` restores the old mask.

### §4.2 F60 — ROUGHNESS IS THE LIVE LEVER, 16× THE CLEARCOAT, AND IT SATURATES

F53 established the BSDF `Roughness` socket is LINKED and inert. The live path,
**traced through `t1_mats.py` rather than assumed**: `body_paint()` writes the
socket while it is still unlinked → `apply_weather()` copies that value into the
**WEATHER group's own `Roughness` input** and links the group's output back over
it → the group maps its noise between `rgh ∓ W_ROUGH_SWING (0.09)`.
`probe_rev58_gloss.py`'s new `T1_GL_WRGH` writes that input and **REFUSES** if
the node or socket is not where the trace says.

**ABLATED BEFORE TUNED (rule 36).** All on the same masked red pixels,
1600×1100 at 96 spp:

| rgh | spread | ratio | headroom | G/R | B/R |
|---|---|---|---|---|---|
| **0.420** was shipped | 0.4701 | **0.3911** | 0.0899 | 0.4315 | 0.3617 |
| **0.250** ships now | 0.5122 | **0.4261** | 0.1458 | 0.4364 | 0.3711 |
| 0.050 extreme | 0.5088 | 0.4233 | 0.1408 | 0.4451 | 0.3829 |
| the photograph | 1.2020 | 1.0000 | 1.0000 | 0.1140 | 0.0470 |

**It SATURATES by 0.250**: 0.050 is *worse* on gloss and dearer on chroma.
Against F54's full clearcoat (**+0.5 %** gloss for **+17.9 %** G/R): **16× the
gloss for a fifth of the chroma cost.**

**OWNER RULING, put as multiple choice with the crop attached: "ship 0.250".**

**CONTROL — the shipped constant reproduces the probe's override:**

| | ratio | headroom | G/R |
|---|---|---|---|
| probe override `T1_GL_WRGH=0.25` | 0.4261 | 0.1458 | 0.4364 |
| SHIPPED `body_paint` 0.250 | 0.4259 | 0.1451 | 0.4365 |
| agreement | **−0.07 %** | **−0.51 %** | **+0.04 %** |

### §4.3 THE TWO CHROMA INSTRUMENTS DISAGREE IN SIGN — REPORTED, NOT PICKED

| instrument | G/R before | after | direction |
|---|---|---|---|
| the hero window (this probe) | 0.4315 | 0.4364 | **+1.1 %, AWAY** from 0.114 |
| `flank_compare`'s flank annulus, side render | 0.461 | **0.423** | **−8.2 %, TOWARDS** it |

Different pixels at different incidence. **The +1.1 % is the pessimistic one and
it is what the owner was quoted.** Gate 1's other three rows do not move:
area 0.9679, aspect 2.3686, IoU 0.7506, `Senor` 0.651 (0.648 before).

### §4.4 F61 / F62 — THE RIG ARM MEASURES THE WRONG THING, AND WHY

`T1_GL_SPOT` adds small BRIGHT sources. **Adding light adds FILL:**

| arm | ratio | median L | G/R |
|---|---|---|---|
| rgh 0.250 alone | 0.4261 | 104.7 | 0.4364 |
| + 3 × 250 W spots | **0.3435** | 124.2 | 0.4860 |
| + 3 × 4000 W (the arm's **own default**) | **REFUSED** — 0 px pass the red mask | — | 0.917 |

At its shipped default the panel washes out entirely and the gate refuses it —
**that default was shipped at rev 57b and had never been run.** The refusal is
the mask working and is recorded as such.

**F62 — WHAT THE FLANK ACTUALLY REFLECTS, off the shipped camera and geometry.**
Hero camera **(8.156, 5.603, 1.307)** — essentially at flank height, so the view
is near-grazing. Mirroring the view ray about the flank normal (0,1,0):

```
incoming (-0.8564, -0.5155, -0.0281)   mirror (-0.8564, +0.5155, -0.0281)
-> strikes the FLOOR 19.3 m outboard, at x -31.76, y +20.17
```

The flank's specular image is **featureless cyclorama 19.3 m away, near the
horizon**. That is why lamps at z 5.2–6.4 add only fill, and why a dark card in
the mirror direction is 19 m out and **IN FRAME** at this camera height —
watched: `out/w25dark_hero.png` has the card across two-thirds of the shot and
the gate refused it. **The model-side lever is exhausted at 0.4261 and the
residual is the SURROUND's**, which *"keep studio, fix the model"* rules stays.

**F47 retracted in the source** (rule 15): the WEATHER header cited Specular IOR
Level 0.21 (0.50 since rev 8) and Roughness 0.42 (0.250 since now), and called
roughness modulation *"nearly invisible"* — now measured at 16× a clearcoat.
The conclusion survives; the premise did not.

---

## §5. THE OWNER REDIRECTED, AND HE WAS RIGHT

> *[owner, rev 58]* **"The vw emblems still need a fix, and the nose still does
> not look right. I just want to make sure that is somewhere in the plan.
> We don't need to commit to a full render until everything is fixed right?"**

The 106.8-minute delivery render was **not** started. It is the last step, not a
milestone, and nothing in this revision needed it.

### §5.1 F63 — THE GLYPH BUILDS AS AN X, IN THE PROJECT'S OWN RASTERISER

`probe_rev46_vw.py`'s built raster is an **X in a ring**, with the W's outer arms
as stubby triangles that never reach it. Off the mesh, as a fraction of the ring
OUTER R, band inner **0.7988**:

| end | reach | verdict |
|---|---|---|
| V arm tips | 0.8400, 0.8400 | on the band |
| W legs (troughs) | 0.8394, 0.8394 | on the band |
| **W OUTER ARM tips** | **0.6638, 0.6638** | **FLOAT 18.9 mm** on a 140.1 mm radius |

Ring: centre z 1.01688, **outer R 0.14011 m** (D 0.28021), band inner 0.7988.

**This is his FIFTH report of this emblem** against a probe reporting *"5
controls, 0 FAILED"*. `t1_core` already carries the rule, written at rev 46
about his FOURTH: *"HIS REPEAT IS A MEASUREMENT: when he reports the same thing
twice the prior closure was wrong or incomplete."*

### §5.2 F64 — WHY THE SOLVER COULD NOT SEE IT

**Every landmark it fits (L1–L6) is a VERTICAL position, a row index down the
emblem. Not one is a RADIUS.** So a stroke can end 18.9 mm short of the band
with every landmark still landing. That is rev 46's own discovery — *"the axis
nobody checked"* — recurring on the axis rev 46 did not check. Its vertical fit
is **not** discarded: residual **0.0347** against rev 45's **0.1167** still holds.

**THE MECHANISM, TRACED NOT GUESSED.** A terminal cap is cut PERPENDICULAR to
its stroke, so its two corners sit at different radii. `vw_bars`' fixed point
drives each terminal's **MAX** corner onto the band, leaving the other short by
the cap's whole radial span. The W's outer arm meets the ring at **0.12°** while
travelling at **55.5°**, so that span is **0.176 R** and the far corner lands at
**0.6638**. Then `vw_logo_fit` re-normalises by the **GLOBAL EXTREME** — the very
mechanism rev 44b named and fixed one stage higher (*"scales by the SINGLE
FURTHEST VERTEX … drags every other end short"*), still live one stage below.

### §5.3 GATED NOW — C6, AND IT FAILS

| | cream cells the strokes cut the ring into |
|---|---|
| **PHOTOGRAPH** `ref_nolita_front34.jpg` | **7** — sizes 215, 152, 115, 97, 91, 73, 68 |
| **BUILT** | **6** — sizes 7491, 7451, 4832, 2614, 355, 321 |

A stroke that fails to reach the ring **merges the two cells either side of it**,
so the deficit of one **is** the floating pair. Structural (a region count),
needs no axis ratio, survives blur, and **the photograph and the build go through
the SAME function** — a second copy is how one of two instruments gets quietly
relaxed. **WATCHED FAILING**, and its **KILL** works: collapsing the W's arms
moves the count **6 → 4**.

`probe_rev46_vw.py` now reports **7 checked, 1 FAILED** where it reported
0 FAILED through three revisions.

### §5.4 F65 — THREE FIXES TRIED, ALL THREE FAILED, NONE SHIPPED

| attempt | cream cells |
|---|---|
| drive the **MIN** cap corner instead of the MAX | 6 → **4** (worse) |
| make `vw_logo_fit` a **pure unit conversion** | 6 → **4** (worse) |
| `VW_W_ARM_Z` 0.0019 → 0.30 / 0.55 / 0.772 (arm angle 0.1° → 18.1° / 30.9° / 40.0°) | **6, 6, 6** (no change) |

The glyph stays an X in every one. **The V's arms and the W's outer arms cross
the same region BY CONSTRUCTION**, so this is a **re-solve of the W's spine
against reach**, not a one-constant tweak. `t1_core.py` and `t1_detail.py` are
back at HEAD. **A half-fix to something reported five times is worse than a
measured refusal.**

### §5.5 THE NOSE, BEYOND THE EMBLEM — A LEAD, NOT A FINDING

The render's nose crop and `ref_nolita_front34.jpg` are at **different camera
poses**, and this project's own rule is that **crops generate leads, not
findings** (rev 55's "X" dissolved twice on exactly this). What is visible and
un-quantified: the cream/red boundary's wedge looks narrower and more pointed
than the photograph's, and the headlamps read as dark holes rather than lit
glass. **Neither is measured and neither is claimed.** The measurement that
would settle it is a **pose-matched** render — recover the photograph's camera,
render that view, and compare the boundary — and it is written up as item B of
rev 59, not as a finding here.

---

## §6. WHAT MOVED, AND WHAT DID NOT

`STATE.md` moved **only in its provenance header**. That is correct and is stated
so the next reader does not misread it as "nothing happened": `STATE.md`
tabulates geometry and material counts, and rev 58 changed a **shader scalar**,
which it does not tabulate. The change is real and the gates measure it.

```
T1_SUB=1  VERIFY: 0 fail, 0 warn
T1_SUB=2  VERIFY: 0 fail, 0 warn
audit.py  wrote STATE.md (0 fail, 0 warn, 223 meshes, 5 materials constant-rough)
```

The constant-rough count stays **5**, confirming `T1_paint`'s roughness is still
LINKED and not a constant — an internal consistency check on the F60 edit.

**MODEL CODE CHANGED THIS REVISION:** one shader constant (`body_paint`'s
Roughness, 0.420 → 0.250), plus the rig refactor across `build.py`, `studio.py`
and four callers. Against rev 54–57's **six lines between them**.

---

## §7. WHAT I DID NOT DO, AND WHY — read this before trusting §9 of the brief

* **The delivery frame was not rendered.** The owner said to hold it until the
  model is right. It is 106.8 min and it is the last step.
* **Item B (F45, the untextured galley and roof-aperture interiors) was not
  started.** It is 7.4 × 10⁵ px² and it is still second by the budget. It is
  plainly visible in `out/r58b_hero.png`.
* **Items C, D, E (F15, F39, F43) were not started.**
* **The emblem is diagnosed and gated, NOT fixed.** F65 says what was tried.
* **F14's 260.0 / 20.0 mm sight lines are still un-re-measured** — now **six**
  revisions INHERITED, and still past §8's decay rule.
