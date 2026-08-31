# LEDGER — rev 72

**RULE 55, AT THE TOP, NOT IN A FOOTNOTE. THIS REVISION SHIPPED A VISIBLE CHANGE TO THE VEHICLE:
`seal_rear`** — the rear aperture's rubber surround, which is the ONE glazed aperture on this
vehicle that has never had one, on the item the owner named. It is built, it swings with the pane,
it has three ablation switches and a `verify.py` row, and **all three of that row's kills were
watched firing.** The A/B is `probe_scratch/r72_seal_ab.png`, rendered before and after and looked at.

**`python3 revstats.py` (FIXED THIS REVISION — see F273): rev 72 ran 124 geometry / 453 instrument
lines against rev 71's 88 / 1502.** Run it; do not quote this line.

---

## 1. WHAT SHIPPED, AND ITS CEILING

**`seal_rear` (F268).** `bay_seals()` builds eleven rubber rings and `windscreen_seals()` two more.
`rear_glass()` sits directly beneath them under the header `REAR GLAZING` and had **none** — so with
`REAR_OPEN_DEG` swinging the pane out at step 8c, the back of the vehicle was a bare 2.8 mm shell cut
edge over unlit cavity. It now carries a gasket, built from `windscreen_seals()`'s own section
(outer = pane + 0.0125, inner = pane − 0.0055, thickness 0.0090), centred on the pane's own centre
plane so **no new constant is typed**, and carried through the SAME `_swing_open` call as the glass —
the thing `open_rear_hatch()`'s docstring has promised since rev 48 (*"anything mounted on the pane
could be carried through the identical call. **Nothing is, today.**"*) and which nothing used.

> **⚠ ITS CEILING, STATED PLAINLY.** This is an **INTERNAL-CONSISTENCY** fix, not a photographic one,
> and the difference matters. What is CERTAIN is the model-side fact — grep `seal_` and count. What
> the photographs support is WEAKER: `ref_rear34.jpg` at (1035…1200, 200…290) shows a glazed window
> on the rear third of this vehicle carrying a thick black rubber surround, gridded and looked at at
> `probe_scratch/r72_rearwin_grid.png` — but **rev 72 could NOT establish from that frame whether that
> window is on the REAR PANEL or is the rearmost FLANK bay**, and says so rather than publishing the
> stronger claim. A T1 rear window being rubber-glazed is a FACTORY PRESSING fact, admissible under
> rule 52 without asking the owner. **AND AT DELIVERY SCALE THE CHANGE IS SMALL** — it reads as a
> framed hatch where there was a frameless sheet. It does not fix the pane rendering opaque, and it
> does not touch the 64° pose.

**`REAR_OPEN_DEG` got a switch and a guard (F269).** `T1_REAR_OPEN` sets the pose; `verify._rear_hatch`
reads the built pane's own best-fit plane normal off its vertices and compares it to the declared
constant. **Neither row is a tautology (rule 6):** R2 compares two separate meshes' normals to each
other and never looks at the constant at all; R3 compares a MESH to a DECLARATION.

**THE ANGLE STILL CANNOT BE MEASURED, AND THAT IS THE RESULT (rule 12), NOT A TASK LEFT UNDONE.**
Every frame we hold that shows this vehicle's rear was looked at: `ref_rear34.jpg` shows the
rear-third glazing **SHUT AND SEALED**, not propped; `ref_side.jpg` is broadside so the tail face is
edge-on; `IMG_3840.jpeg` is 480×320 with the tail dome occluding the station. 64.0 remains a POSE
CHOICE and is now labelled one in three places instead of one.

**THE KILLS, EVERY ONE RUN AND READ (rule 3):**

```
    T1_REAR_SEAL=0       VERIFY: 1 fail   "rear hatch has NO SEAL: seal_rear is absent while
                                           every other glazed aperture ... carries one"
    T1_REAR_SEALSTAY=1   VERIFY: 1 fail   "rear GASKET DRIFT: seal_rear's plane stands 64.04 deg
                                           off glass_rear's"
    T1_REAR_NOSWING=1    VERIFY: 1 fail   "rear hatch POSE DRIFT: ... 0.00 deg off the tail plane,
                                           against REAR_OPEN_DEG = 64.0 declared -- -64.00 deg"
    T1_REAR_OPEN=0       VERIFY: 0 fail   **SHUT** -- the HONEST close, and the distinction
                                           between it and the injected drift above is the point
    shipped build        VERIFY: 0 fail   pane 64.00 deg declared 64.0; gasket tracks it 0.045 deg
```

## 2. WHAT WAS MEASURED

**THE 16-BIT RE-READ IS A NULL, AND THE BRIEF CALLED IT THE REVISION'S CHEAPEST WIN (F271).**
`probe_rev72_bits.py` re-computes `gloss_compare.spread()`'s own arithmetic — **the shipped function's
source, exec'd, agreeing to 1e-12** — off the same window, changing one thing: the reader.

```
    out/r72_hero34f.png    IHDR depth 16    64 734 distinct levels in the file, 256 through PIL
                                            low byte nonzero in 99.8 % of pixels
    spread   8-bit 0.49601   16-bit 0.49292   -0.00309 = 0.623 %   (bar missed by 30 %)
    mask       28 012 px       28 006 px      -6 px
```

**AND WHERE IT DOES MATTER, MEASURED RATHER THAN ARGUED.** B4 stops the same window down: 0.46 %
apart at ×1.0, 0.07 % at ×0.25, and below that the window falls under the mask's own `L>25` floor and
the probe REFUSES. **The distinguishing variable is the region's EXPOSURE, not the gate** — which is
exactly why F266's dark-channel ratio was decisively wrong at 8 bits while these gates are not.
**B1's kill is watched: on a frame whose signal lives only in the low byte the 8-bit read reports a
FLAT patch (spread 0.000000) and the 16-bit read 0.002230.**

> **⚠ THE STRUCTURAL CEILING (rule 38): `gloss_compare`'s verdict is a RATIO against a PHOTOGRAPH that
> is an 8-bit JPEG. There is no 16-bit form of it and never will be, so the re-read can only ever move
> the numerator.** B3 tests this by asking `read_png` for the photograph's depth and watching it refuse.

**THE GATES, LIVE ON REV-72 FRAMES:** `gloss_compare` **0.412** (brief 0.411), `flank_compare` worst
region **0.689 (i)** (brief 0.689). Both reproduce inside the 2.441 % render-nondeterminism floor.

## 3. INSTRUMENTS FOUND WRONG — FOUR, AND ALL FOUR FIXED

* **F273 `revstats.py` DOUBLE-COUNTED EVERY REVISION LANDED BY PR, AND IT IS THE OWNER'S OWN DRIFT
  INSTRUMENT.** `git show --numstat <merge>` emits the merge's diff against its first parent — for a
  PR merge, the entire branch again. **rev 71 read 176 geometry lines and reads 88; rev 65's published
  313 collapses to 0** (its six commits touch no geometry file — the ellipse fit is +330 in
  `probe_rev65_unproject.py`, an INSTRUMENT); and one `Merge remote-tracking branch 'origin/main'`
  contributed **1 172** geometry lines of main's history to a single revision. **rev 71's honest
  doc:geo is 39.44 — WORSE than the 35.39 the brief published and than the 28.97 the unfixed script
  printed.** Two independent derivations agree.
* **F274 `gloss_compare.py`** died with a raw `FileNotFoundError` on a NAMED missing frame — no summary
  line for rule 9 to read — on the gate the brief ranks #2. Fixed and watched (rc 3).
* **F275 `probe_rev67_nose.py`** bare printed `4 checked, 0 FAILED`, rc 0, while its first line refused.
  **Recorded at rev 70 AND rev 71 and fixed at neither.** Now `2 checked, 0 FAILED, 1 ABSENT`, a
  `⚠ NOT A PASS` line, **rc 2**.
* **F270** is in this list too and it is mine: see §4.

## 4. WHAT I GOT WRONG IN MY OWN WORK

1. **`T1_REAR_OPEN=0` CRASHED THE BUILD ON ITS FIRST RUN, AND THE COMMENT I WROTE BESIDE IT CLAIMED IT
   WORKED (F270).** `AssertionError: rear hatch opened the WRONG WAY: its free edge moved dx +0.0000
   dz +0.0000`. A comment asserting a behaviour the code did not provide — inside the edit that added
   the switch. **Rule 47 exists for exactly this and I only found it because I ran the switch.**
   Retracted and fixed in the same edit, using the trunk lid's own zero-pose precedent.
2. **MY FIRST `verify` DRAFT EXCUSED ITS OWN KILL.** `T1_REAR_SEAL=0` printed *"not applicable"*
   instead of going red, which would have left R1 a control that can never fire — **rule 36's shape,
   inside the guard written to satisfy rule 3.** Corrected before it shipped; it now follows
   `T1_NOSE_FIXFOLLOW`'s precedent and REFUSES.
3. **`probe_rev72_bits.py`'s B0 CONTROL FAILED, AND THE FAULT WAS MINE, NOT THE GATE'S.** It fed my
   copy an un-quantised float patch while the shipped function re-read a uint8 PNG, and reported
   0.170992 vs 0.172118 — a 0.7 % "disagreement" that was **entirely my input framing (rule 42).**
   I fixed the INPUT, not the bar. They now agree to 1e-12.
4. **I SPENT REAL BUDGET TRYING TO ASSIGN A WINDOW IN `ref_rear34.jpg` TO THE REAR PANEL AND FAILED.**
   The engine lid, plate and handle are unambiguous (`probe_scratch/r72_plate.png`); the glazed window
   two bands above them is not assignable to the rear panel rather than the rearmost flank bay from
   that frame. **I stopped and wrote the weaker claim** rather than publish the stronger one.

## 4b. WHAT THE OUTGOING ADVERSARY (rule 17) FOUND IN THIS REVISION'S OWN WORK

**IT BROKE THE REVISION'S HEADLINE DELIVERABLE, BY EXPERIMENT, AND BOTH HOLES ARE FIXED (F278).**

5. **`verify._rear_hatch` R2 WAS BLIND TO POSITION.** Its docstring said it checked *"that the gasket
   did not drift off the glass"*; the code compared **plane normals only.** The adversary translated
   `seal_rear` by (0, +1.0, +0.5) m, re-ran the row, and got **no complaint** — a gasket 1.118 m away
   passing at 0.045 deg. Now measured on **bounding-box centres**, with `T1_REAR_SEALSHIFT=1` as its
   watched kill (`VERIFY: 2 fail`, "sits 1118.0 mm from glass_rear's").
   **AND THE FIRST FIX USED THE WRONG STATISTIC TOO:** the VERTEX MEAN read **13.1 mm** between two
   objects that are concentric by construction — an artefact of the ring carrying two outlines to the
   plate's one — and **I had written "0.0 mm apart" into that row's comment from arithmetic instead of
   running it. Rule 5, inside the fix for a rule-5 complaint.** bbox centres read 0.0 mm.
6. **R3 FOLDED THE ANGLE AND WOULD HAVE PASSED A BROKEN POSE.** It read `acos(|n · x̂|)`; at
   `T1_REAR_OPEN=116` it printed **swung = 64.00**. A swing bug applying 116° while the constant said
   64 would have read a difference of zero and **shipped with `VERIFY: 0 fail`** — the
   trunk-lid-opened-INWARDS class. R3 now takes its **sign from the hinge**, recorded off the
   PRE-SWING mesh as a POSITION (so not a tautology). `T1_REAR_FOLD=1` is its watched kill:
   **116.00 against a declared 64.0, +52.00 deg, `VERIFY: 1 fail`.**
7. **`probe_rev72_bits.py` HAD TWO ROWS THAT COULD NEVER FAIL** — `ck(..., True, ...)` — while the
   brief quoted "5 checked, 0 FAILED" as if all five were tests. B2 now tests a falsifiable thing
   (the two readers agree on the eight bits they SHARE). **B4 now FAILS ON PURPOSE**, because its
   ladder reaches only 2 of 4 rungs and **its trend FALLS (0.46 % → 0.07 %) — the OPPOSITE direction
   from the generalisation I drew from it.** That generalisation is retracted in the brief.
8. **THE "SHUT AND SEALED" EVIDENCE INHERITED AN AMBIGUITY I HAD DECLARED ELSEWHERE.** I wrote into
   `rear_seal`'s own comment that the window cannot be assigned to the rear panel rather than the
   rearmost flank bay — and then used that same window as the ground for closing the ANGLE as
   unrecoverable. **Rule 46.** Weakened to what survives: no frame we hold shows the hatch OPEN.
9. **"THE PANE RENDERS OPAQUE DARK" IS REFUTED BY THE CROP I CITED.** Inside the pane at
   (r645, c1050) the ratio is **G/R 0.204** — the red band seen THROUGH the glass — and the
   `tail_board_stay` rod behind it is visible. **The pane transmits; the unlit cavity is dark**, which
   is F254's finding, not F71's.
10. **F272 IS THE REGISTER CATCHING ITSELF A THIRD TIME AND I DID NOT CHECK THE REGISTER (F279).**
    `F162`, `MEASURED-rev62`, already made that correction ten revisions before F263 got it wrong.
11. **`--cc` DOES NOT FIX `--numstat` (F280)**, and my published **1 172** was **1 262** — a figure
    typed rather than run, **inside the finding that fixed a typed figure.** The combined diff is
    parsed as a patch now, and the hard-coded 721 / 1.55 baseline is **computed: 718 / 1.40.**

**RULE 49, THE FIGURE I OWED AND HAD NOT PUBLISHED.** The `seal_rear` A/B against F228's **2.441 %**
floor: globally **2.546 %** of pixels >8 levels — **at the floor; invisible to that statistic** (a roof
control reads 21.59 %). It separates only in the tail: **>32 levels 3.95 % in the seal window against
0.002–0.34 % in controls, worst channel 253 vs the floor's 40, rows 545–596 / cols 1200–1254 — about
1 000 px of 1 760 000 (~0.06 %).** Real, localised, small. ⚠ **And the 2.441 % floor is itself five
revisions old and was not re-measured.**

## 5. RETRACTIONS AGAINST THE RECORD

* **F272 — F263's ATTRIBUTION IS REFUTED BY F42's OWN TEXT**, and the claim is repeated three times
  (F263, the rev-72 brief §0b, rule 58). F263 says *"F42 recorded it as a property of the renderer for
  fifty revisions"*; F42, graded `MEASURED-rev57`, says *"Blender **delivers** … then reads through
  `Image.open(...).convert("RGBA")`, **which returns uint8**"*. **And `shader_solve.py` records a
  stdlib 16-bit decoder "CONTROLLED against PIL … max difference 0" — verbatim rev 71's validation —
  written at rev 57 and NEVER COMMITTED**, which is why `read_png` had to be written again.
  **F263's SCOPE claim (every probe, not just `shader_solve._render`) is real and stands.**
* **F276 — `HANDOFF_CARRIERS.md` §0.05's WHAT-TO-BUILD ITEM 1 IS REFUTED**, and it is the item §0.05
  calls *"the largest visible defect"*. `tail_board()` builds a **22 mm solid rounded-rect prism** — it
  HAS a panel body and an underside. §0.05 was describing an EDGE-ON VIEW (the side elevation looks
  along the board's plane). **The rest of §0.05 stands** — the dark angled recess is genuinely absent,
  the ruler mismatch stands, and `TB_WIDTH`'s 0.59 m bound is verbatim in the source.

## 6. THE MACHINE AT CLOSE

```
bootstrap.sh        ALL 10 PASS.  ROW 9: HEAD 0 ahead / 0 behind origin/main at pickup
verify_clone.sh     ALL 380 PASS on a clean tree -- 0 FIDELITY, 380 SELF-CONSISTENCY
build.py T1_VERIFY  VERIFY: 0 fail, 0 warn at T1_SUB=1, WITH the new row armed
photometry.py       9 checked, 0 FAILED
probe_rev72_bits    5 checked, 0 FAILED  (2 ABSENT bare, rc 2 -- it refuses correctly)
gloss_compare       0.412 (bar 0.60)  FAIL     flank_compare  0.689 (i) (bar 0.75)  FAIL
```

**NOT ONE OF THOSE ROWS IS EVIDENCE ABOUT THE VEHICLE except the two that fail.**

## 6b. THE NOSE — LOOKED AT, MEASURED, AND ONE PRESCRIPTION REFUTED (F277)

`probe_rev67_nose.py` P3's row is NAMED *"…and on a **three-quarter frame** it is NOT"*, and the
rev-72 brief inherited that reading and prescribed *"Give it a true elevation frame or re-cut the
row."* **Rev 72 gave it a true elevation frame — `out/r72_front.png`, the straight-on `front`
preview — and it refused anyway:** sagitta −73.55 px ± 9.46 over 926 px, **fit rms 113.22 px = 12 %
of span**, 475 of 476 points clipped. **The pose is not the cause.** The probe's own source comment
already names it — *"a whole-frame column scan catches EVERY cream-under-red boundary in the frame …
and fits one parabola through the lot"* — and the fix is a **nose-column window**, derived from
something independent of the edge it measures (rule 6) and painted first (rule 8).
**⚠ CEILING: rev 72 did NOT build that window. This refutes a prescription; it does not supply a
replacement.** P1 and P2 pass unchanged on the photograph side.

## 7. WHAT DID NOT MOVE

**The emblem, and the nose.** Both were rendered, cropped and LOOKED AT — that much was done and is
worth having: `probe_scratch/r72_emblem_crop.png` beside `probe_scratch/r72_ref_emblem_workshop.png`
shows the defect plainly and confirms F104 pose-free — **the real mark's six strokes are STEEP and
NEAR-PARALLEL; ours RADIATE, and the W's outer arms read as detached slivers.** Neither was moved,
because the spine constants are RETIRED BY OWNER RULING (F234), free endpoints were measured WORSE at
rev 71 (F252), and the traced pressing renders as SHARDS (F262). **The route is a new construction
with a legibility term in the objective, and that is rev 73's, not a thing I could hide in this one.**
