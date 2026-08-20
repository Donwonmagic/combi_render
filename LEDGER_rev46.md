# LEDGER — rev 46

**Everything this revision measured, changed, refuted and retracted.** Figures here were watched
print unless a line says otherwise. Where this ledger and the machine disagree, the machine is right.

---

## §0. THE OWNER'S REPORTS, AND WHAT EACH TURNED OUT TO BE

At the close of rev 45 he wrote:

> *"I still see a lot of problems, including the 100% calidad off center, the vw logo wrong, señor
> Tacombi still isn't clearer, the nose of the car is too flat which is inaccurate in shape, among
> other things."*

Mid-revision he added three more, each of which turned out to be right and none of which any prior
revision had looked at:

> *"Remove the upper triangles from that please"* — *"The lines seem to be vent slats"* —
> *"The bottom word does not collide with the top one either"* — *"The lettering looks off as well"*

| his words | verdict | where |
|---|---|---|
| "100% calidad off center" | **CONFIRMED and FIXED.** Type sat (−0.1167, +0.1117) off the burst's centre; now (+0.0001, −0.0001). | §1 |
| "the vw logo wrong" | **CONFIRMED and FIXED.** Landmark residual 0.1167 → 0.0347, now at the photograph's own noise floor. | §2 |
| "señor Tacombi still isn't clearer" | **CONFIRMED, HALF FIXED.** *Señor* was 2.7× too dark and is corrected. **The dominant defect is BLUR, not contrast** — cause found, fix drafted, not applied. | §3 |
| "the nose is too flat" | **CONFIRMED, NOT FIXED.** 14.3 mm recession over 0.70 m. Still no photographed anchor. | §4 |
| "remove the upper triangles" | **CONFIRMED and DONE.** 15 pennants no frame supports. | §5 |
| "the lines seem to be vent slats" | **CONFIRMED and DONE**, and it leaves a new finding: the model has **no rear vents at all**. | §5 |
| "the bottom word does not collide" | **CONFIRMED, NOT FIXED.** The two words share **1110 pixels**. | §6 |
| "the lettering looks off" | **NOT EVALUABLE from what we hold.** 23×39 px is the best frame. | §6 |

---

## §1. W1 — the Calidad type was off-centre INSIDE the decal *(FIXED)*

**Not the defect rev 44 closed.** That one was the decal **panel's placement on the vehicle**
(Report 7, 0.180 of texture width). This is the **type's placement within the decal**, which nobody
had measured in forty-five revisions. Both are true; they are different things. The placement stays
closed.

Measured on the generator's own output, pre-rotation: the type block's centroid sat at
(0.3735, 0.6309) of the canvas against `starburst()`'s centre (0.5050, 0.5750). In the shipped
raster the miss was **(−0.1167, +0.1117)** — "100%" hung off the burst onto bare cream and "Calidad"
ran off the panel's bottom edge (bbox reached y 0.953).

**Fix, structural rather than tuned.** `BURST_CX/BURST_CY` promoted to constants; `TYPE_SHIFT`
**expressed as (burst centre − measured pre-rotation centroid)** rather than frozen as its
arithmetic result, so it re-derives after any glyph change (SPEC 10.25). And the block now rotates
about the **burst's** centre instead of (0.500, 0.600) — those differ, so the −19.7° rotation was
swinging a correctly-laid-out block back off centre. A rotation fixes its own centre, so the
centring is now exact and independent of `ANG`.

Result **(+0.0001, −0.0001)**; bbox x 0.272–0.762, y 0.292–0.841 — inside the burst on every side.

**Guard, added in the same edit (rule 12).** `cal_gen` refuses to write a decal whose type is more
than 0.004 off centre. **Watched fail (rule 19)** at (−0.1099, +0.1127) on the rev-45 layout and at
(−0.0132, +0.0134) on 12 % of the correction — it catches the residual, not just the gross miss.

### RETRACTION — the rev-46 brief's photographed target is withdrawn

**(+0.0455, +0.0746) is not a measurement of anything.** Calibrated against a synthetic decal at the
photograph's own scale with the type displaced by a *known* offset, the instrument that produced it
reported ≈(−0.01, −0.04) for **every** truth value tried — (0,0), (±0.10, 0), (0, ±0.10) and
(−0.14, +0.13) alike. It is blind to the quantity it names: the closed-and-filled burst mask traps
cream between the spikes, cream is bright and low-saturation, so the "type" centroid it returns is
the burst's own centre whatever the type does. The photographed target is **"centred"**, established
visually and stable across thresholds; the residual is not resolvable at 23×39 px. The correction
made is 0.117, an order of magnitude above that floor.

---

## §2. W2 — the VW glyph's vertical proportions *(FIXED)*

**His fourth consecutive report of this emblem.** HIS REPEAT IS A MEASUREMENT.

**What was wrong.** rev 44 set the **spine's** apex to 0.284 because that is 0.358 of the ring's
diameter from the top and the photograph's apex landmark reads 0.353. But the photographed landmark
is the row where the V's two arms **merge into one run** — a property of the **outline** — and the
strokes have width, so they merge well *above* the spine's apex. Setting a spine constant to an
outline measurement put the built merge at 0.251 against 0.343. **SPEC 10.110.8 exactly.**

Landmarks are run-count transitions, **registered on the ring's own top and bottom edge rows** so a
crop margin cannot move them:

| landmark | photo | rev 45 | rev 46 |
|---|---|---|---|
| L1 V arms clear the ring band | 0.1940 | 0.1455 | 0.1745 |
| L2 V apex / the central knot | 0.3433 | 0.2509 | 0.3418 |
| L3 W outer arms leave the band | 0.4776 | 0.5018 | 0.4764 |
| L4 W troughs reach the lower band | 0.8060 | 0.8509 | 0.8073 |
| L5 V arm separation / ring width | 0.2361 | 0.2248 | 0.2625 |
| L6 V arm stroke / ring width | 0.1528 | 0.1514 | 0.1417 |
| **residual** | — | **0.1167** | **0.0347** |

The V was **squat** and the W **stretched**. Residual is 3.4× closer and now comparable to the
photograph's own uncertainty (0.025 in quadrature).

**L5 and L6 are why the angles became touchable.** Rev 45 refused to move any angle because
de-foreshortening a three-quarter view of a circle needs the ring's axis ratio and the two fits
disagree by 10 %. That refusal was right *for rev 44's number*, which divides a **horizontal** arm
separation by the ring's **vertical** diameter. **A horizontal divided by a horizontal at the same
row is invariant to rotation about a vertical axis — the cosine cancels.** Same trick as SPEC
10.107.2, applied on the other axis.

Both controls earned their keep: without L5 the solver widened the V to `VW_V_TIP_X` 0.435, past
what the photograph supports; without L6 it thinned a stroke that was already correct.

**A hypothesis refuted rather than acted on.** Beside the photograph the built strokes *looked* too
thick, merging V and W into the X of SKEPTIC_PASS §D. Measured at the same structural row:
photograph 0.1528 ± 0.002, built 0.1514. **The stroke width was right**; the impression came from
squashing a circular raster to the photograph's elliptical aspect.

**Unchanged and checked:** all six stroke ends still reach 0.8400 R, 3.6 mm into the band,
bit-identical to rev 45. `probe_rev44_lampmove` stays **6 checked, 0 FAILED**. SPEC 7005 untouched.

### Instrument errors caught by controls — all three mine

* **L4** was "first 3-run row after L3" and landed on a transient that exists at thresholds 25–40
  and vanishes at 45–50, making a **stable** photograph look unstable (spread 0.166) and sending the
  solver at 0.691 when the landmark is 0.806. It is the **last** 3-run row. C1 caught it.
* **Registration** was "first 2-run row", which a two-pixel noise speck at threshold 25 moved by
  0.088. It is the ring's own first and last non-empty row — the ring is a closed annulus, so those
  *are* its extent.
* **The solver's own console reports 0.0262** for these constants; it reads them in a scene it has
  already built in. The clean number is **0.0347**, watched print twice, bit-identical. *The
  solver's figure is not quotable.*

### CORRECTION TO THE BRIEF (its own standing instruction)

`NEXT_CONTEXT_PROMPT_rev46.md` lists the first landmark as photo 0.147 / built 0.104. **0.147 does
not appear in the photograph at any threshold from 25 to 50 or in any of five crop windows** — it is
the *built* value transcribed into the photo column, and 0.104 is the built ring-split row. The
photographed landmark is 0.206 unregistered, 0.1940 registered.

---

## §3. W3 — "Señor Tacombi still isn't clearer" *(HALF FIXED — read this before touching it)*

**Measuring the two words separately dissolves the contradiction that stalled this for three
revisions.** Prior revisions took one Michelson figure over the whole script and ran finding 19 (the
ink is already too light, so darkening makes it worse) against finding 30 (it needs more contrast).
They pull opposite ways only because they are averaged over both words. Apart:

| | photographed | built rev 45 | built rev 46 |
|---|---|---|---|
| Tacombi | 0.4673 ± 0.0009 | 0.4480 | 0.4488 |
| **Señor** | **0.1922 ± 0.0060** | **0.0711** | **0.1912** |

Photographed on `ref_side.jpg`, the frame the script was traced from, over 6 thresholds × 4 windows.
**"Tacombi" was never the problem.** "Señor" is fully tarnished and rendered at luminance 95 against
a ground of 79 — not low-contrast, very nearly **invisible**. He named the word.

The lift is **derived**: luminance is linear in it, so `K' = K + (1−K)·lift` solves in closed form
against the photographed target. Solved lift 0.2180.

**It is a declared departure, with its size and its retirement condition.** `TARNISH_K` is a measured
ratio and the generator reproduced it faithfully (built Señor/Tacombi 0.451 against a photographed
0.496). Correcting that ratio *alone* reaches only 0.1385. **The rest is not the ink — it is the
ground:** the built body red renders 11 % brighter relative to the ink than the photograph's
(ground/Tacombi 0.376 built against 0.338), which is **W6**, and **W6 is blocked on the owner**. So
the lift overshoots the photographed ink ratio to 0.560 against 0.496. **That 0.064 is the
departure.** When W6's paint is settled, **re-derive this lift** — it will shrink, and if the red
lands where the photograph puts it the departure goes to zero on its own.

### THE DOMINANT DEFECT IS BLUR, AND IT IS NOT FIXED

**Three revisions have been chasing an amplitude metric for a spatial-frequency fault.** Put the
built script beside `ref_side.jpg` at the same magnification: the photograph has hard edges, sharp
corners, legible spirals in the a/o/b and a clearly readable "Señor" **with its tilde**. The build is
mush in both words; "Señor" has no letterforms at all.

**The cause is arithmetic, not art.** `Canvas` draws at `SS = 12`, i.e. 3552 px across.
`Canvas.alpha()` then **box-downsamples that to mask space, 271 px across the ink**, throwing away
all twelve times of it. `main()` then **LANCZOS-upscales those 271 px to `OUT_W = 4096`**. The
texture is 4096 px wide carrying 271 px of real detail: every edge is a 15-px ramp. The 3552-px
raster it threw away is already almost exactly the output resolution.

**The fix, drafted and deliberately not applied** (it must not ride in on a colour commit):

1. add `Canvas.alpha_box(k)` downsampling by `k` rather than by `SS`;
2. keep `alpha() = alpha_box(SS)` so the existing `_ref_mask()` equality guard stays bit-identical;
3. have `main()` crop the hi-res raster at `[y0*SS:(y1+1)*SS, x0*SS:(x1+1)*SS]` before resizing.

That turns a 15.1× upscale into a 1.26× one. **Measure the 10–90 % alpha edge width over the mean
stroke width**, built against photographed, before and after — it is dimensionless and it is the
metric this item should have been using all along. (Current built softness: 0.215 of ink pixels lie
in the 0.1–0.9 alpha band.)

---

## §4. W4 — the nose is flat *(CONFIRMED, NOT FIXED)*

Raycast against the built body at z = 1.25, mm behind the centreline crown:

```
    y=0.00   0.10   0.20   0.30   0.40   0.50   0.60   0.70
      0.0   -0.4   -1.6   -3.6   -6.5  -10.2  -12.9  -14.3
```

**14.3 mm over 0.70 m of half-width — the nose is a plane.** The only forward bulge anywhere in the
model is one constant, `bulge = 0.019` in `t1_shell.nose_shape`.

**THE TRAP, unchanged:** ledger finding 6 ("the nose shape, `V_POW` locked 0.60") is about a
**different axis**. `V_POW_Z` drives `zV(y)`, the painted two-tone break line's height. It is a paint
curve and has nothing to do with how far the sheet metal bulges forward.

**Still no photographed anchor.** A measurement task was dispatched to a subagent this revision to
find one by the three candidate methods (shading gradient with the render box chosen by *projecting*
the same 3-D band, corner wrap in silhouette, published T1 body dimensions). **Its result had not
returned when this revision was recorded — do not assume it succeeded; check for its report and
re-run the measurement if none exists.** Rev 45 attempted this and threw its result away because the
render and photograph boxes were not comparable; that remains the failure mode to avoid.

---

## §5. THE BUNTING IS RETIRED — the lines are VENT SLATS *(DONE, at his instruction)*

**Stage 1 — "Remove the upper triangles."** `cal_gen` drew two red bars across the top of the burst
with **15 triangular pennants** hanging from them. **No frame we hold shows them.** Magnifying
`ref_playa_34.png` 16× over the strip between the roof and the burst gives two thin **straight** lines
with plain cream between them and the burst. Because the pennants are `BUNT` red (R − G = 158, which
passes any red test) they also **contaminated every "burst" mask ever taken of this texture**.

**Stage 2 — "The lines seem to be vent slats."** He is right, and the generator's own palette is the
evidence against itself: `BUNT` was (198, 40, 36), a saturated **red**, and the lines in the
photograph are **dark grey**. They are the T1's rear air-intake louvres — shadowed slots in sheet
metal, not paint. A louvre drawn into a decal texture is wrong three times over: wrong colour, wrong
material, and it can neither self-shadow nor catch a highlight because it has no depth. The whole
feature is retired from the artwork rather than recoloured.

### NEW FINDING — THE MODEL HAS NO REAR VENTS

`grep -rn 'vent|louvre|louver|slat|intake'` over every source returns the cab door's quarter-light
and `studio.py`'s lighting rig, **and nothing else**. These painted louvres were the only thing
standing in for the real ones, in the one place they could not work. **Building them is bodywork
geometry and is the natural next item.** Their position is visible in `ref_playa_34.png` above the
Calidad burst and, per the owner, in the workshop side shot.

Guarded **by absence, three ways** — the function, the pennant loop and the colour constant must all
be gone — because a feature that comes back halfway is exactly how this one survived.

---

## §6. TO EVALUATE — his two newest reports, one measured, one not measurable

### 6a. "The bottom word does not collide with the top one either" — **CONFIRMED, measured**

In the built decal **"100%" and "Calidad" share 1110 pixels.** Their bounding boxes overlap by
0.0335 of the canvas height, **14.4 % of the "100%" cap height**:

```
  100%     x 0.3033-0.6381   y 0.3390-0.5716   (h 0.2326)
  Calidad  x 0.3304-0.7660   y 0.5381-0.7890   (h 0.2509)
```

**Not fixed.** The two lines' anchors are `(0.150, 0.395)` and `(0.180, 0.645)` plus `TYPE_SHIFT`;
their **relative** offset is untouched by rev 46's centring, which moved the block as one. Opening
the gap means changing that relative offset, which will move the block's centroid — **so re-derive
`TYPE_PRE_CENTROID` and `TYPE_SHIFT` in the same edit, and the W1 guard will catch you if you don't.**

### 6b. "The lettering looks off as well" — **NOT EVALUABLE from what we hold**

`ref_playa_34.png` is the **only** frame in the whole set that shows this decal
(`REFERENCE_FRAMES_rev45.md` §2), and the burst spans **23 × 39 px** in it. At that size the
letterforms are 4–6 px tall. **Nothing about a typeface can be measured there**, and this revision
does not invent a number for it. **This is a photograph request, not a work item** — see §8.

---

## §7. THE STATE OF THE MACHINE

```
bootstrap.sh      ALL 10 PASS
build             T1_SUB=1, clean
verify.py         VERIFY: 0 fail, 0 warn   (T1_SUB=1, after every change here)
verify_clone.sh   ALL 83 PASS on a clean tree   (was 69 at rev 45)
probes            probe_rev46_vw        5 checked, 0 FAILED   (C3 a KILL, red by design)
                  probe_rev44_lampmove  6 checked, 0 FAILED   <- held across W2
                  probe_rev46_reports   R1's photo target RETRACTED, see §1
SPEC sections     10.118 (W1), 10.119 (W2), 10.120 (W3) written into the sources
branch            claude/new-session-3tof54
```

**`probe_rev46_reports.py` R1 must be updated.** Its photographed target `(+0.0455, +0.0746)` is
retracted by §1 and its estimator is the blind one. Its R2 target line also carries the brief's
0.147 transcription error corrected in §2. Its R3 box is hand-typed and its ink mask is the same
bright/low-saturation rule that fails on cream. **Do not quote it until it is rebuilt.**

---

## §8. WHAT ONLY HE CAN GIVE — additions this revision

Ranked additions to `PHOTOS_WANTED`, each saying why it cannot be settled from what we hold:

1. **The "100 % Calidad" decal, square on and close.** Settles §6b (the lettering), §6a's target word
   spacing, the burst's spike count and proportions, and whether the pink star is where we put it.
   **The only frame we hold shows it at 23 × 39 px.** This is now the highest-value missing frame for
   the artwork.
2. **The rear panel square on**, showing the vent slats — their count, pitch, length and height above
   the decal. Needed to build §5's missing geometry rather than guess it.
3. Everything still outstanding from `PHOTOS_WANTED_rev45.md`: the off side, the absolute roof
   height, **the nose square on** (still worth double — W2's remaining angles and W4's plan
   curvature), and the cab interior.

**Do NOT ask him again for** anything in rev 45's do-not-ask list, and do not ask about the pennants
or the vent slats — **he has answered both.**
