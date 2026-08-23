# EFFICIENCY AUDIT OF THE HANDOFF — written at rev 57b, for the owner

**You asked for an audit of the handoff aimed at efficiency, and for a plan that gets to a
significantly improved render without losing the quality of the method. This is the audit. The
plan it produces is in `NEXT_CONTEXT_PROMPT_rev58.md`.**

**The short version: the method is excellent and it is pointed at the wrong things.** Nothing below
argues for less rigour. Every rule in `CLAUDE.md` was earned by a real defect and all of them stay.
What has gone wrong is *target selection*, and it has a single measurable cause.

---

## §1. THE FINDING — THE PROJECT HAS STOPPED CHANGING THE MODEL

Non-comment lines of **model code** (`t1_core`, `t1_shell`, `t1_detail`, `t1_mats`, `build`,
`lid_gen`, `script_gen`, `studio`) changed per revision, measured from git:

| rev | 48 | 49 | 50 | 51 | 52 | 53 | 54 | 55 | 56 | 57 |
|---|---|---|---|---|---|---|---|---|---|---|
| **model code lines** | 266 | 297 | 145 | 102 | 34 | 10 | **0** | 3 | 3 | **0** |
| prose lines added | — | — | — | 1781 | 804 | 1023 | 1540 | 1691 | 1642 | 1630 |

**The last four revisions changed six lines of model code between them. Two of them changed none.**
Over the same four revisions the project wrote **6,503 lines of prose**. That is a ratio of about
**1,000 lines of writing per line of model.**

The repository today: **model 15,169 lines; prose 107,957 lines.** Prose is **7.1×** the model;
everything-that-is-not-the-model is **10×** it.

**And the record says so itself, in its own voice.** The rev-57 brief, describing rev 56: *"Rev 56
fixed two instruments and woke a second gate. **Neither moved the vehicle.**"* My own rev 57 closed
by *proving* it had changed no geometry — I regenerated `STATE.md`, found only the provenance header
had moved, and reported that as **a control**. That is the inversion in one sentence: *the project
now treats "changed nothing" as a quality signal.*

---

## §2. THE CAUSE — THE RANKING RULE SELECTS THE LEAST VISIBLE WORK

The brief states the rule in its own words:

> *"Gate availability is the ranking rule — an item with a gate outranks an item without one,
> because only the gated one can tell you whether you improved the photograph."*

That is a good rule for deciding what you can **trust**. It is the wrong rule for deciding what to
**do**, because in this project measurability and visibility are **anti-correlated**: a small
isolated feature is easy to gate *precisely because* it is small and isolated, while the things that
dominate a photograph are large, diffuse and hard to reduce to one number.

`visibility_budget.py` converts each open finding into pixels of a 3840-wide delivery frame
(scale measured off a real render: **801 px/m, 1.25 mm per pixel**):

| rank | finding | area affected |
|---|---|---|
| 1 | the paint's **gloss**, cream upper body | **2.5 × 10⁶ px²** |
| 2 | the paint's **gloss**, red flank | 9.6 × 10⁵ px² |
| 3 | **F15 / A7** — unlit roofed body | 8.2 × 10⁵ px² |
| 4 | galley interior reads as untextured white blocks | 4.0 × 10⁵ px² |
| 5 | roof-aperture interior, same | 3.5 × 10⁵ px² |
| 6 | **F01/F39** — `Senor`, 28.5 % of its ink | 2.7 × 10⁴ px² |
| 7 | **F10** — galley 103 mm too far aft | 6.8 × 10³ px² |
| 8 | **F03/F04** — the cream mottle's feature size | 3.7 × 10² px² |
| 9 | **F08** — the badge stroke's whole 47-point bracket | 1.2 × 10² px² |
| 11 | **F08** — the 5.09 % it was meant to settle | **1.4 px²** |

**The top of that list is 1.8 million times the bottom, and the bottom was the top job for four
revisions.** At the delivery frame the badge question is worth **1.2 pixels**.

*Ceiling on the table, stated because it is real: pixels are not visibility. A hard edge reads
louder per pixel than a soft gradient — `Senor` is small and loud. Use it to catch orders of
magnitude, not to rank neighbours.*

---

## §3. THE THING NOTHING MEASURES, MEASURED

Two of the three surfaces above are the same defect: **the paint has almost no gloss.** Nothing in
240 verifier rows or two fidelity gates looks at it. So I built the gate — `gloss_compare.py`.

It measures how widely one red panel's luminance spreads about **its own median**, so it is free of
exposure, of white balance and of every open px/m bracket. **It is not a colour comparison**, so W6
does not bite.

| | spread (p95−p5)/median | headroom p99/median − 1 |
|---|---|---|
| render, flat red flank | **0.468** | **0.140** |
| photograph, flat red door | **1.192** | **1.007** |

**The render's paint spreads 0.392 of the photograph's, against a 0.60 bar — FAIL. Its brightest
1 % sits at 0.139 of the photograph's headroom: about one seventh of the specular life.**

Calibrated before it was believed: **exposure-free** (identical to four decimals at 0.70× and 1.40×
brightness) and **resolution-stable** (3.9 % between the full and half-size reference). Both windows
are painted — `probe_scratch/rev57_gloss_render.png` / `_photo.png`. The first attempt caught the
lit headlamp and inflated the photograph's p99; painting it is what found that.

**What this gate does NOT say.** It does not say the shader is wrong. You ruled *"keep studio, fix
the model"*, and part of this gap is a white cyclorama having nothing to reflect. **That ruling
stands and I am not re-opening it.** The gate is a **ruler, not a verdict on cause** — but a ruler
on the largest surface in the frame is exactly what the project has never had.

---

## §4. WHAT ELSE THE LOOKING FOUND — AND IT IS NOT GEOMETRY

Rendering the hero and cropping it (rule 1) puts the honest list in a different order from any
ledger in this repo:

1. **The galley interior and the roof-aperture interior are untextured white blocks.** They are
   bright, high-contrast, dead-centre, and seen through four openings. Nothing about them is
   measured or gated. They read as placeholder geometry, because they are.
2. **Nothing in the frame has a specular highlight.** §3 puts a number on it.
3. **The lid mural reads as a pasted image**, not a painted panel in light — flat, hard-edged, no
   weathering, no sheen.
4. **The counter top, the bumper and the aperture surrounds are flat untextured slabs.**
5. The Tacombi script, the gold artwork, the wheel arches, the louvre block and the stance all read
   **well**. The model's *shape* is in good order. Its *surfaces* are not.

**And a control that found nothing, reported because that is still a result:** the render's nose
roundel is body-red, which looked wrong to me. `ref_nolita_front34.jpg` shows the red bus's own
roundel and it **is body-red on cream**. The render is right and my suspicion was wrong.

---

## §5. MEASURED WASTE IN THE LOOP — ABOUT 35 MINUTES A REVISION

| waste | measured | fix |
|---|---|---|
| **Ablation renders at 64 spp** | rev 56 recorded the statistic *"stable to ±0.01 across 16/32/48 samples"* and the gate still runs at 64. My own sweep cost **4.8 min × 9 runs = 43 min**; at 16 spp it is ~11 min | run ablations at `T1_MM_SAMP=16`. **~30 min per sweep** |
| **Strip renders rebuild the scene every strip** | measured on tonight's hero: **65 s of build per strip × 10 = 10.8 min**, ~10 % of the job | render every strip in one Blender session |
| **`out/` starts empty** | every revision re-renders the baseline before it can do anything: **~10 min** of dead time at the front | **launch the baseline render in the background as the FIRST action, before reading the brief** |
| **The self-referential row count** | the count moved **three times** at rev 56 and **three times** at rev 57; each move is an edit, a `cp` and a re-run | `audit_brief.py --fix-count` writes it |
| **The brief must be read in full first** | 709 lines, plus `CLAUDE.md`, plus the ledger, plus the register — **~2,000 lines before the first action** | §0 of the new brief is a 20-line decision table; the rest is reference |

---

## §6. WHAT I AM **NOT** RECOMMENDING

* **Not less rigour.** Every rule stays. They exist because measurements were wrong, and they were
  right to exist — rev 57 caught four of its own instruments being wrong, which is the normal rate.
* **Not re-opening the studio ruling.** *"Keep studio, fix the model"* is yours and it stands.
* **Not dropping a carrier.** §0.1, §4, §5, §8 and §9 are carried into the new brief intact.
* **Not abandoning the register or the verifier.** Both are working. The verifier's own verdict
  block already tells the truth about what it is worth.
* **Not redrawing the `Senor` artwork.** A12 is your ruling.

The one thing I am recommending you change is **which item the method gets pointed at**, and the
new brief encodes that as a rule rather than as advice.

---

## §7. THE RENDER

You said you wanted to work up to a high-fidelity, maximum-resolution frame. **Nobody has ever
rendered this model at delivery quality** — every figure in every ledger comes off 1600×1100 at
96 spp, and the strip/stitch/post pipeline that exists for exactly this has gone unused for
revisions.

So it is running now: **`hero` at 3840×2640, 256 samples, SUB=2, in 10 stitched strips**, then
`stitch.py`, then `post.py` for the optics.

**IT TOOK THREE ATTEMPTS AND THE FIRST TWO ARE THE INTERESTING PART.** Attempt 1 came out with
**eight white seams** — Blender's border rounds inward, so a row at each boundary was rendered by
neither strip (F48); `stitch.py` caught it, exited 2, and **my runner ignored the exit code and
posted anyway** (F49). Attempt 2 fixed the seams and came out a **BLACK BUS** — I had moved the
render into one Blender session and `build.py` builds the entire lighting rig inside its
`if T1_PREVIEW:` block, so measuring tools get an unlit scene (F51). **Every automated check passed
that frame**: stitch exited 0, the seam detector read a clean z = 3.63, and it ran 2.94× faster —
which I briefly read as the optimisation working. Attempt 3 is lit, seam-free at worst z = 1.62,
and is what shipped.

**Measured, all three:** 115.2 min (ten processes, lit) → 39.2 min (one process, **unlit, invalid**)
→ **106.8 min** (one process, lit). **The single-session saving is 8.4 min, 7.3 %** — the 2.94× was
the missing lights, and the CPU-contention theory I floated for part of it is **withdrawn**: run 3
was idle and lands 7.3 % from run 1, which the build overhead alone accounts for.

The frame is at **`out/hq_hero.png`**, with `out/hq_hero_white.png` (flat-white backdrop) and
`out/hq_hero_raw.png` (pre-optics) beside it.

**Set your expectations honestly: it will be the same model, rendered beautifully.** It will be
sharp, clean and 6.6× the pixels — and it will still be a matte bus in a white room, because §3's
0.392 is a property of the model and the rig, not of the sample count. **That frame is the
baseline the next revisions have to beat**, and it is the first time this project will have one.
