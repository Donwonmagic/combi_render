# LEDGER — rev 61

**Every figure this revision produced, with how it was obtained and what it is ceilinged by.**
Nothing here is transcribed from a paragraph. Where a number replaces an earlier one, the
earlier one is shown struck rather than deleted.

---

## §0 THE ONE-LINE SUMMARY

**Rev 61 fixed a GATE, not a model.** `probe_rev59_nose.py`'s M1 had been measuring the
headlamp's chrome bezel for two revisions. Everything that follows from that — F106, F107, the
"whole remedy programme is refuted", and my own first reading of the 0.860 divisor — is
retracted. The nose moved **+24 mm**, measured, exactly as the orphaned F77 predicted.

**And rev 61 refuted more than it shipped, deliberately.** Nine proposals were killed by
ablation BEFORE anything was tuned — four of them from the expert panel the owner commissioned,
two of them my own. That is the method working; it is not idling.

---

## §1 WHAT SHIPPED

| change | file | evidence |
|---|---|---|
| `V_POW = V_POW_Z = 0.52` (was 0.60) | `t1_mats.py`, `t1_shell.py`, 3 rows in `verify_clone.sh` re-based together | F77's POSE-INVARIANT fit: render control recovers a source truth of 0.600 as 0.605/0.620 (±0.02); three frames read 0.517 / 0.521 / 0.531. Effect **+24 mm** at the lamp against F77's predicted **+24.5** |
| the `Señor` `S` restored to ONE continuous letter | `senor_trace.py`, `tex/senor.png` (checksum re-based with a companion row) | the owner's rev-61 ruling. Watched both ways: shipped 1 component `[361 px]`, `T1_SENOR_BREAKS=1` gives 3 `[251, 61, 14]` |
| M1's bezel bug fixed | `probe_rev59_nose.py` | see §2 |
| **C8 / C9** — the first scale-stable instrument for the X | `probe_rev46_vw.py` | see §3 |
| **`judge_set.sh`** — the optics chain, on the frames that get judged | new | see §5 |
| `T1_VNOSE_DIV`, `T1_BULB_STR`, `T1_BULB_BASEV` | `t1_mats.py` | measurement-only ablations; all three shipped values are the literals |

---

## §2 THE NOSE — F134, F135, F136

**THE BUG.** `probe_rev59_nose.py` walked up from the lamp and stopped at the first `cream`
pixel. `cream = (sat < 45) & (lum > 110)`; `v0` is the top of the LENS blob, segmented as
`(~cream) & (~redm)` — dark AND unsaturated. **The chrome bezel above the lens is BRIGHT and
unsaturated, so `cream` is TRUE on it** and the walk halted there, two pixels up, every run.
The bezel's top sits at a fixed offset from the lamp centre, so M1 returned ~1.18 lamp radii
whatever the paint did.

```
render                  M1 said     TRUE break
V_POW 0.60 (shipped)      1.183       1.789
V_POW 0.15                1.186       3.800
T1_VNOSE_DIV 0.600        1.184       3.917
```

**⚠ CORRECTED-rev61 BY AN ADVERSARY: the third row was a HAND-WALK OF ONE COLUMN mixed into a table of the probe's TWO-LAMP MEANS — rule 38's own defect, in the document that introduces rule 38. Re-run with the shipped probe it is **3.917**, not the 3.788 first published. Rows 1 and 2 reproduce exactly.**

**CROSS-CHECKED TWO WAYS BEFORE ACTING.** A separately-written hand-walk of the same column
gives **1.730** where the fixed probe gives **1.731** — agreement to 0.001 lamp radii. And the
NODE GRAPH is vindicated: it predicts d(zv) = **0.1502 m** across V_POW 0.60→0.15 and the
renders move **0.1518 m**, agreeing to **1.6 mm**. The graph was right all along.

**THE RULER MISMATCH, AND MY OWN RETRACTION.** I published *"M1 PASSES at 2.114 — item B
fixed"* for one commit. **Retracted.** This probe's ruler is the DARK LENS INTERIOR; F75 says
its red-bus bar came from *"the red-bus frames WHOSE RULER IS THE CHROME RIM … NO FRAME WE HOLD
SHOWS A RIM AND ITS APERTURE TOGETHER, so that 1.19 conversion CANNOT BE CHECKED."* M1 now
prints the BEZEL-ruled figure beside it every run:

```
                 lens-ruled   BEZEL-ruled     F75 bar (rim-ruled)
V_POW 0.60          1.789         1.31              1.951 .. 2.121
V_POW 0.52          2.114         1.550
```

**ITEM B IS IMPROVED BY A MEASURED 24 mm, NOT CLOSED.** F75's verdict stands: honest range
**50–80 mm**, best single estimate **52 mm**, and no single constant fixes it.

---

## §3 THE EMBLEM — F137, F138, F139, F141

**THE X, AS A NUMBER, FOR THE FIRST TIME.** C6 counts CELLS and F105 already found that count
is not scale-stable. C8 measures cream-cell ELONGATION, area-weighted median:

```
photograph                 3.39
built, shipped             1.49   at 276 rows AND 1.49 at 69   <- SCALE-STABLE
a plain cross              1.39   <- the built glyph is barely above this
six parallel bars         10.71
built, T1_VW_CAPMIN        1.58   <- F101's refutation CONFIRMED independently
```

C9 is the kill and runs on two synthetic cases whose answer is known by construction. A first
attempt used the W-collapse ablation and moved only 1.49 → 1.56, which is a coincidence waiting
to happen, not a control.

**THE CONSTRAINED SOLVE — THE MOST USEFUL RESULT ON THE EMBLEM IN SIX REVISIONS.** Using the
probe's OWN functions (`err`, `built_landmarks`, `glyph_only_mask`, `cell_elongation`) at
**0.02 s per evaluation**, **8,174 candidates**:

```
max elongation subject to C4's own bar (residual < 0.045) and cells == 6   =  1.634
photograph                                                                =  3.39
```

**The landmark set L1–L6 and the photograph's cell shape are INCOMPATIBLE.** No arrangement of
the six spine constants satisfies both. That closes the search space rather than adding another
failed attempt to it. With the constraint dropped entirely the search reaches 4.644 — so the
CONSTRUCTION can produce sliver-like cells; the LANDMARKS are what forbid it.

**TWO OF MY OWN ROUTES REFUTED, BOTH BY BUILDING THEM.**

* **The kink hypothesis (F138).** I argued the X came from the V's arm and the W's inner arm
  meeting 9.48° apart. Wrong twice: those angles were on the UN-PROJECTED spine (post-solve they
  are V −57.3°, W-inner −47.2°), and decisively **the photographs have the same size kink,
  opposite sign** — −8 to −10° photographed against +10.1° built.
* **The reference-angle route (F141).** Ring-sampling the segmented badge on `ref_workshop.jpg`
  (93×63 px, 1.86× the area of the 41×69 source every constant was fitted to) gave a stable 6
  strokes at **99 / 147 / 197 / 250 / 307 / 357°**. Shipped those angles and measured:
  elongation **1.54**, residual **0.1800** — both WORSE than shipped, and worse than the
  deliberately-bad rev-45 control at 0.1167. **Two ceilings, both unfixable:** at r = 0.68–0.72
  the ring crosses each stroke ALONG ITS LENGTH, not at its terminal, and pushing out to r ≥
  0.76 explodes the count to 15 and 23 on the band's own noise; and `ref_nolita_front34` at
  40×68 px gives 7 / 5 / 8 strokes at three neighbouring radii — no stable count at all.

**C6's TARGET OF 7 IS CONTAMINATED (F139).** The photograph's smallest counted cell, 68 px,
sits **ENTIRELY INSIDE THE RING BAND** (r 0.878–0.968, band inner ≈ 0.80) with no left-hand
counterpart — a hole in the red mask, not a glyph cell. The genuine glyph count is **6, the same
as the build**, and 7 is topologically unreachable for a symmetric V-over-W. **So C6 goes green
on a glyph that still reads as an X once the artefact is excluded** — F64 again.

---

## §4 NINE PROPOSALS KILLED — AND **THIS IS NOT A KILL LIST FOR EVERYTHING IN IT**

**⚠ READ THIS BEFORE USING THE TABLE. An independent adversary caught the outgoing brief
telling the next context *"if your idea is on that list it is already dead"* — and ROW 1 IS A
LEVER THAT IS ALIVE.** Row 1 is a RETRACTION of my own false refutation: the 0.860 divisor
**does** move the nose break (1.789 → 3.917), and §0.06 of the brief says so in bold. **Rows
2–9 are dead. Row 1 is live and its entry is the retraction, not the kill.**

**AND ONLY FOUR OF THE NINE WERE KILLED BY ABLATION.** Rows 2, 3, 4 and 5 were. Rows 6, 7, 8
and 9 were killed by SOURCE INSPECTION or MESH MEASUREMENT, which is a different and weaker
class of evidence — a source reading can be wrong about what the renderer does, where an
ablation cannot be. **Five of the nine are panel-sourced, not four**, as this heading previously
said and as the brief repeated twice.

**The panel's point estimates are NOT bankable.**

| proposal | source | ablation | verdict |
|---|---|---|---|
| ~~the 0.860 divisor is inert~~ **NOT A KILL — THIS ROW IS A RETRACTION AND THE LEVER IS ALIVE** | rev-61 brief §3.2 | 0.860 → 0.600 gives 1.183 → 1.184 **by a BLIND M1** | **my own reading, RETRACTED.** The true break moves **1.789 → 3.917**. **DO NOT strike this lever** |
| bulb emission strength | F144 | `T1_BULB_STR=60` (6.7×) moves the saturation ratio **1.40 → 0.88** | **WORSE.** The bead clips toward white and clipped pixels are neutral |
| bulb envelope reflectance | F144 | `T1_BULB_BASEV=0.30` moves it **1.40 → 1.50** | nothing |
| cut the cream's dust/mottle (+3.0) | lookdev panel #1 | `T1_MOT_AMP` **0.55 → 0.30 → 0.00** moves the blotch **11.8 → 11.9 → 11.9 %** | **INERT.** At AMP = 0 the texture is GONE and the number does not move — it is the shading gradient on the curved nose panel |
| make the bright metal metal (+3.0) | lookdev panel #2 | `T1_WORLD` 0.05 → 1.00: mirror **100 → 170 DN**, red saturation **0.459 → 0.377**, cream **140 → 171** | **the LEVER is refuted** — it costs the paint more than it gains the metal, and the shipped 0.05 gives the HIGHEST red saturation. The panel's actual proposal, a LOCAL bounce card, survives and is the owner's call |
| tail lamps are 2× too wide, should be ovals (+2.0) | modelling panel #7 | `small_lamp` is `T.revolve(axis='X')` — circular in 3D — on the tail's CORNER ROUNDING, where a circle projects as a tall ellipse. `TAIL_LAMP_OD = 1.1627 * PLATE_OUTER_H` against a photographed **1.119**, within 4 % | **REFUTED, and F128 predicted this exact error** |
| regenerate `lidmural` at true 4K (+2.5) | lookdev panel #5 | `lid_gen.py` draws at W = 4096; the softness is two Gaussians expressed as FRACTIONS of W, encoding a fixed real-world softness. Combined ~4.2 px sigma predicts ~13 DN/texel peak gradient; **measured 10** | **REFRAMED.** Not upsampled; a 4K regeneration buys nothing. What is open is whether ~6 mm of edge softness is right, and my instrument SATURATED — not settled |
| the `Señor` bridge is a regression | lookdev panel | the two textures show the `eñor` mass is **pixel-identical**; the bridge fused only the `S` | **OVERSTATED.** The panel's INDEPENDENT finding stands though — see §6 |
| the cab glazing stops ~80 mm short (F71/B2) | carried 3 revisions | `glass_dm1` spans **x 0.9992..1.5680** against `DOOR_MAIN_S`'s **0.9952..1.5720** — 4.0 mm inset, exactly `poly_offset(-0.004)` | **REFUTED at the mesh.** The pane covers its aperture. The real defect is the INTERIOR seen through it |

---

## §5 THE OPTICS CHAIN NOBODY EVER RAN — F146

`post.py` implements bloom → chromatic aberration → vignette → grain **in the correct physical
order**, documents `--backdrop headroom`, and carries its own rev-14 measurement proving the
vignette and grain do not render without that flag. **Every per-stage gain defaults to 0.0 and
the preview path never called it**, so sixty revisions of fidelity judgement were made on raw
frames. An independent photography panel scored OPTICS **1/10** and SENSOR CHARACTER **2/10**
largely on that.

```
frame        pure-255 %          corner DN        HF sigma
front      62.67 ->  0.47     255.0 -> 246.2   0.000 -> 1.317
side       60.55 ->  0.18     255.0 -> 246.2   0.000 -> 1.317
hero       47.89 ->  1.54     255.0 -> 246.4   0.000 -> 1.317
hero34r    57.67 ->  1.21     255.0 -> 246.4   0.000 -> 1.317
```

`judge_set.sh` produces the `_post` set. It does **not** touch the delivery path and does
**not** change what `build.py` writes.

---

## §6 THE OWNER'S RULINGS THIS REVISION, AND WHAT THEY COST

> *"senor Tacombi should be clearer in the render than in that photo. Well defined. I want this
> 3d model to look like new. Enhanced from the photo."*

`senor_trace.py` had been waiting for exactly this, in its own words: *"bridging
`_STROKES[0]->[1]->[2]` would be inventing ink. **It is an OWNER decision, not this file's.**"*

**THE TRADE, STATED.** Drawn ink 1005 → 1040 px against a reference 1062, but IoU against the
TARNISHED mask FALLS — `Senor` 0.8859 → 0.8602, the `S` 0.8825 → 0.8100. Intersection moves
only 323 → 324 px, so the bridge's 35 px land outside the reference mask essentially by
construction. **That is the ruling working as intended.** IoU-against-the-tarnish is now the
WRONG score for the `S`; CONNECTIVITY is the right one and is what is guarded.

**AND IT IS NOT ENOUGH.** Live on `flank_compare.py`, the `Senor` region carries **979 px of ink
against the reference's 1261 — 77.6 %**, at IoU **0.721** of its own ceiling. **My bridge moved
that by 1 px.** The deficit is letterform SIZE and WEIGHT across the whole word. The ruling is
not yet delivered.

> *"Can you have sub agents … make sure that this bus has the perfect body shape, completely
> true to size."*

Done — two specialists, then a three-panel judgement. See `PANEL_rev61.md`.

---

## §7 THE PANEL — 83 / 240

Modelling **34/80**, lookdev **28/80**, photography **21/80**. Full scorecard, per-category
scores, the disputes and the merged ranked programme are in **`PANEL_rev61.md`**, which is a
CARRIER.

**The highest single score on the page is proportion and stance, 8/10** — length-to-height
agrees with `ref_side.jpg` to **0.3 %**, and the rear arch lip sits within **9 mm**. The
geometry's overall dimensions are not the problem. Everything under 5 is surface, material,
optics and small parts.

**TWO CEILINGS THIS PROJECT TREATS AS SETTLED WERE DISPUTED WITH NUMBERS.** The photography
panel put the specular-event census at **0.024 % of red pixels against 7.07 %** in the
FLATTEST-lit photograph we hold, and noted the render's own SIDE frame reaches a panel spread of
0.521 — inside the reference range — on the same shader that gives the hero 0.224. It argues the
deficit tracks camera/light geometry, not the surround. **Recorded, NOT adopted.** It also
disputes the ground-shadow ceiling on the grounds that a cyclorama floor cannot light a 200 mm
cavity. **Both need testing before F62 is quoted again.**

---

## §8 THE ROOF — F142, F143. F91's OTHER HALF, DONE AT LAST

Two thirds of the owner's standing bar; the roof had never once been held against a photograph
in 60 revisions.

* **The roof's colour difference is CEILED, and that forecloses a chase.** roof/cream saturation
  **0.276 built against 0.756 photographed** — but the roof and the flank cream are **THE SAME
  MATERIAL**, both `body_paint` above the break. The whole difference is a white cyclorama
  lighting an UP-facing surface neutrally where the photograph's roof sits under a warm canopy.
  **Warming a paint constant to close it is the laundering this project names.**
* **AN UNMODELLED OBJECT STANDS ON THE ROOF AND HAS SINCE REV 12.** `AUDIT_rev12.md` records
  *"the unmodelled roof box (§2/25) occupies image x 592–635"* and uses it to bracket the roof
  aperture's forward station — and it is in **no live carrier**. Re-found by looking; my crop
  reproduces rev 12's image range exactly. **At 8× it resolves as a PAIR OF LOUDSPEAKER
  CABINETS**, corroborated on a second independent scene (`ref_side.jpg`, crop x 307–324).

---

## §9 EVERY WINDOW I PAINTED AND THREW AWAY

**Eleven, which is normal here (rule 4), and every one produced a plausible number first.**

1. A `ref_rear34.jpg` "bulb string" window that swallowed the **MURAL LID** and returned a
   believable **4.48** against the true 3.82.
2. A tail-lamp window that landed on **A CHILD'S HAIR** in `ref_nolita_front34.jpg` and would
   have published a roundel/lamp ratio from it.
3. A "flank cream" window in `r61f_hero34r` that landed on the **WHITE BACKGROUND**
   (232.5/229.3/228.6, sat 0.016) and made the roof look 0.725 of its cream.
4. A nose-blotch window on `ref_playa_34.png` that **straddled the body edge into the
   background** (min 41 DN).
5. A second one that **clipped the windscreen gasket**.
6. A glass-extent selector keyed on "grey-green" that measured the part of the pane that LOOKS
   like glass (83 px) and reported a short pane on a pane that is not short.
7. A comparison of `DOOR_MAIN_S` (authored, UN-dropped) against `glass_dm1` (post-step-8b) that
   read the **RIDE DROP** as a 70 mm defect.
8. Three tail-lamp thresholds in `ref_rear34.jpg` that returned aspects of 1.14, 0.68 and 1.29
   before a DRAWN AND VERIFIED box gave 1.57.
9. A "99 % cumulative radial power" effective-resolution statistic that reported `senor.png` at
   12 % when its edges are **1.0 texel** — it measures low-frequency content, not sharpness.
10. An edge-width instrument that **SATURATED ITS OWN SEARCH WINDOW** on both frames (medians of
    24 and 20 px against a 25 px window) and produced 134 mm / 81 mm. Not published.
11. The first C9 kill, which moved 1.49 → 1.56 — a 0.07 margin is a coincidence, not a control.
    Replaced with two synthetic cases whose answer is known by construction.

**AND THREE CLAIMS I PUBLISHED AND RETRACTED IN THE SAME REVISION:** *"M1 passes, item B is
fixed"*; *"the 0.860 divisor is dead"*; and a comment "correcting" `senor_trace.py`'s prose from
3 `S` fragments to 4 when the prose was right and my guard was counting specks.

---

## §10 THE MACHINE'S VERDICT AT CLOSE OF REV 61

```
bootstrap.sh          ALL 10 PASS
verify_clone.sh       ALL 271 PASS on a clean tree   <- 0 FIDELITY, 271 SELF-CONSISTENCY
probe_rev59_nose      M1 PASSES lens-ruled at 2.114  <- AND THAT IS NOT ITEM B CLOSED (F136)
                      BEZEL-ruled 1.550 against a rim-ruled bar of 1.951..2.121
probe_rev46_vw        9 checked, 2 FAILED -- C6 and C8
                      C8: photograph 3.39, built 1.49, a plain cross 1.39
flank_compare.py      FAILS: worst region `i` 0.687; `Senor` 979 px against 1261
senor_trace.py        `S` rasterises as 1 component; T1_SENOR_BREAKS=1 gives 3
expert panel          83 / 240
```

**AND THE STANDING WARNING, WHICH `verify_clone.sh` PRINTS ITSELF.** Not one of those 271 rows
compares the vehicle to a photograph.
