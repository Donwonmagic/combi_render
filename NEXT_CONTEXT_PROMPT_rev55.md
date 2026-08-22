# NEXT CONTEXT PROMPT — rev 55

**Read this whole file before you touch anything.** Then `CLAUDE.md` (method only, loads every
session), then `LEDGER_rev54.md` — which is where every number below comes from — then
`SURVEY_rev49_photoreal.md` §6, still the work list.

---

## §1. START HERE — MEASURE THE BRANCH, DO NOT TRANSCRIBE IT

```bash
cd /home/user/combi_render
git fetch --unshallow 2>/dev/null || true
git fetch --all --prune
for b in $(git branch -r | grep -v HEAD); do
  printf "%-52s ahead %-3s behind %s\n" "$b" \
    "$(git rev-list --count origin/main..$b)" "$(git rev-list --count $b..origin/main)"
done
git diff --name-only HEAD...origin/main        # <- HIS PHOTOGRAPHS ARRIVE HERE
./bootstrap.sh          # ALL 10 PASS  -- THE BRANCH CHECK IS ROW 9
./verify_clone.sh       # ALL 173 PASS -- and read what its verdict block says
```

**THE DESIGNATED BRANCH'S REMOTE COPY WAS DELETED A FOURTH TIME AT REV 54.**
`fetch --prune` printed `- [deleted] (none) -> origin/claude/tacombi-rev-54-u7hvys` — rev 51, 52, 53
and now 54. HEAD measured **0 ahead / 0 behind** `origin/main`, every remote branch measured
**0 ahead**, and rev 53's work had landed in `main` through **PR #10** (not #9 — #9 was rev 52's,
and the rev-54 brief's §1 said #9; corrected here off `git log`). MEASURED at pickup, not
transcribed. **Expect this shape a fifth time and measure it.**

> **ROW 9, NOT ROW 10** — confirmed again at rev 54 by reading the machine's own output:
> row 8 clone depth, **row 9 "no branch carries work HEAD does not have"**, row 10 `verify_clone.sh`.

**Re-measure before you finish, too.** `origin/main` moved mid-revision at rev 51.

---

## §2. WHAT REV 54 DID

### §2.1 THE FASCIA FOLD IS NOT SILENT. THE QUESTION HAD A FALSE PREMISE

Brief §3 item 2 asked **why the counter fascia's bottom fold produces no edge signal.** It produces
one. Rendered as an emission AOV — which is what the brief asked for instead of a fourth hypothesis
— the gate fires at **0.28992** against `W_EDGE_90 = 0.29289`, i.e. **99.0 % of the theoretical
maximum for a 90° fold**.

**What it makes is a chip band ONE MILLIMETRE tall.** Bands measured up from the fold, at
0.1875 mm/px:

| band above fold | 0–1 mm | 1–2 | 2–3 | 3–4 | 4–6 | 6–9 | 9–12 |
|---|---|---|---|---|---|---|---|
| `hard>0.5` | **11.833 %** | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

**1 mm at the shipped side render's own 271.2 px/m is 0.27 px**, and 0.21 px at `ref_side.jpg`'s
211.5. Three revisions hunted a cause for a silence that was never in the shader — it was in the
sampling. Every 0.000 % ever read on that fascia was a correct reading of an unresolvable band.

**AND THE RADIUS LEVER IS LIVE AT THIS FOLD**, which rev 53 could not see at 271 px/m:

| Bevel radius | 1.00 mm | **2.75 (shipped)** | 6.00 | 12.00 |
|---|---|---|---|---|
| EDGE reach | 0.625 mm | 1.375 mm | 2.625 mm | 5.125 mm |
| chip coverage | 0.0995 % | **0.3084 %** | 0.6769 % | **1.3717 %** |

Linear at **0.114 % per mm of radius**. The 2.75 mm case rendered twice at different sample counts
gives **0.3084 / 0.3140 %**, so the sampling floor is **~1.8 %** and the **4.45×** rise is far above
it. **So rev 53's "the fascia is UNCHANGED at 0.000 %" was A TRUE READING AND A FALSE INFERENCE** —
the shader moved 4.45× and the estimator could not resolve it. What must clear a pixel is not the
RADIUS but the BAND, and the band is **0.43–0.63 of the radius**.

**CONFIRMED BY LOOKING, WITH CONTROLS.** `probe_rev54_look.py` renders the same window through the
studio rig at four real scales. The four largest AOV-predicted chip sites were cropped from the
beauty render, and four control tiles were cropped on the same fold where the AOV predicts nothing.
All four predicted tiles show a dark ragged bite in the cream; all four controls are clean
(`probe_scratch/rev54_look_chiptiles.png`, predicted first). By 3.687 mm/px they are gone
(`probe_scratch/rev54_look_ladder.png`). Peak `wear` falls **0.634 → 0.107** across that ladder.

**THIS DOES NOT REOPEN HIS RULING.** He ruled *"Follow the photograph — clean cream"*; the shipped
build still reads 0.000 % through the frame's optics and nothing about what ships has changed. What
changed is the REASON: the cream is clean because the band is 0.27 px, not because the gate is off.
**The build does carry a 1 mm chip band there**, and a close view puts it back on screen — at
1 mm/px the peak is still **0.416**, and `studio.views()["counter"]` is a 90 mm lens at ~6 m,
roughly 1.5 mm/px on this part. **Stated as a consequence, NOT acted on.**

### §2.2 TWO HYPOTHESES DIED WITHOUT A RENDER, BY ASKING THE MESH FIRST

* **"the gate uses the SHADING normal, so a smoothed fold collapses it."** The code does use
  `geo.outputs["Normal"]` while its own comment says *"true geometric normal"*, and `True Normal`
  appears **nowhere** in the tree. **But `counter` is FLAT-shaded** — 26 polys, 0 smooth — so
  shading normal *is* true normal there. Refuted by the mesh, at no render cost.
* **"the wear weight is zero on that material."** `countercream` carries **Wear = 0.7000**.
* The fold is real: **2 edges at 90.87° mean, 0.3417 m long**, on a mesh with **0 boundary edges**.

### §2.3 REFUTED AT REV 54 / STILL REFUTED — DO NOT REBUILD THESE

* **"the counter fascia's bottom fold produces no edge signal"** — REFUTED, §2.1.
* **"the fascia is unchanged when the radius changes"** — REFUTED: 4.45× at 5333 px/m.
* **"the gate uses the true normal"** (the source comment) — false, and left standing on purpose
  because it is inert on flat geometry. **See §3 item 2: it is LIVE on the smooth shell.**
* Rev 52's **sub-pixel radius** claim stays refuted on its own terms (12 mm is 3.25 px, not
  sub-pixel) — but its INSTINCT was right about the wrong quantity. Both halves matter.
* **"the fascia's bottom edge is a butt joint"** — refuted at rev 53 by the mesh, still refuted.
* Everything rev 50/51/52/53 refuted — all still refuted. The cap's dome depth; the m5 "convention
  conflict"; the wear field does not clone; `LID_W ≤ 1.2797 m`; A7's aft wall; `gal_end_f` widened
  to `REAR_W/2`; **"ONLY THE WORST-REGION NUMBER IS ROBUST"**.
* **§2b of the rev-52 brief — HIS SETTLED RULINGS — IS UNCHANGED AND STILL BINDING.** W6 (keep the
  studio rig; **a G/R shortfall on any surface is NOT a paint error**); the roof strips' 0.3 m
  retired; the wipers withdrawn entire, commented not deleted; the lower bay SHUT; the RED bus is
  the target and **paint and artwork do not transfer between vehicles**; the tail board IS on the
  vehicle; the marks above the burst are STARS. **Do not re-open or re-ask any of them.**
  `playa_env.py` is not on the table.

### §2.4 THE SOURCE ASSERTED BOTH DEFAULTS AT ONCE, AND THE GUARD PASSED THROUGHOUT

`t1_mats.py`'s chip block carried `# DEFAULT IS STILL POINTINESS.` and, 38 lines later,
`# rev 53: THE DEFAULT IS NOW THE RAY-TRACED EDGE SIGNAL.` **The `verify_clone` row that guards the
flip passed the whole time**, because it is anchored on the CODE — and the code was right; only the
prose lied. **A guard on the code does not guard the comment beside it.** Retracted in place, and a
row now counts the stale sentence and wants 0.

### §2.5 THE BADGE CONSTANT DOES NOT DENOMINATE WHAT A PHOTOGRAPH MEASURES

The top job's remaining constant is `CAP_EMBLEM_WFRAC = 0.2087`, documented `# w/R as authored
(0.0072 / 0.0345)` — and 0.0345 was a real OUTER RADIUS, so the intent is w / R_outer. But
`vw_bars` is called with **R = 1.0** and `_fit_glyph` rescales off the outline's **own** extreme
corner, which sits at **rmax = 0.81400** (measured on isolated glyphs at four widths, the same
0.814 at every one). So:

| | authored wfrac | **built stroke / OUTER RADIUS** |
|---|---|---|
| hubcap | 0.20870 | **0.25639** |
| nose (`vw_logo_fit` — the REAL call site) | 0.19860 | **0.24398** |

Cross-checked on the **built mesh** by a second probe: **0.25869**, agreeing to 0.9 %, which is the
estimator's own measured bias. The estimator was **calibrated before it was believed** — it recovers
a known width to **+0.33…+0.52 %** over w = 0.12…0.28.

**THE TRAP: a photograph measures the SECOND column. Comparing a frame against 0.2087 itself
understates by 18.6 %.** The note is in `t1_detail.py` beside the constant and a row holds it there.
**The two badge DESIGNS differ by 5.09 %** and neither has ever been compared to any frame.

*`vw_logo`'s signature defaults (`R=0.1385, w=0.0275`) are NOT what is built — the call site passes
`R=1.0, w=wfrac`. They agree to 4.4e-05 so nothing turned on it, but the signature is not the call
site.*

### §2.6 THE GUARD GAP ON THE WHEEL — THE REV-54 BRIEF OVERSTATED IT, AND IT IS NOW PARTLY CLOSED

The rev-54 brief said *"still not one row anywhere names a wheel, hub, cap, rim or vent."*
**Measured, that is too strong.** `verify.py` already guarded `TRACK_F`, `TRACK_R`, `TYRE_D` and the
rear **arch-to-tyre gap** (real `fails.append`, all printed in `STATE.md`), and `verify_clone.sh`
checksums `tex/emblem.png`.

**What genuinely had nothing** — zero occurrences in either verifier, measured: `capvw`, `capring`,
`wheel_spoke`, `wheel_rim`, `wheel_hub`, `rim1`, `rim-1`, `wheelhouse`, `roof_vent`, `vw_disc`,
`vw_ring`, `CAP_EMBLEM_D`, `CAP_EMBLEM_WFRAC`. And `t1_detail.py`'s `hubcap seated:` line is a
**`log`, not a guard** — four numbers printed, nothing fails if they drift.

`verify.py` **section 13** now measures off the mesh: the assembly's object counts; the ring radius
against `CAP_EMBLEM_D/2` **derived on both sides**; that the four rings agree; that each cap centre
sits on a hub (`z == TIRE_R`, `x` at an axle); and that the glyph is fitted **flush** to the ring,
which is what `_fit_glyph` promises and nothing checked. All six clauses **watched failing on an
injected defect and passing through a refactor** — `LEDGER_rev54.md` §7.1 lists each injection and
the exact line it produced. **It is SELF-CONSISTENCY, not fidelity**, and it says so in its own log
line.

### §2.7 A PAINTED WINDOW CAUGHT MY OWN PROBE, AGAIN — the project's most-repeated defect

The badge probe's first version took every object named `capring*` and called it "the ring".
**There are four hubcaps.** The "ring" came out as a **2.486 m circle spanning the wheelbase** with
two 20 mm glyphs at the axle stations, and `w/R` read **0.01136**. **Caught in one second by looking
at the painted PNG** — the red circle is the whole vehicle. Nothing about reasoning would have
caught it. Instances are clustered on the ring centroids now and all four are reported so they
control each other (spread **0.00**).

**AND THE AOV'S OWN FOLD ROW WAS WRONG THE SAME WAY.** The fascia **SLOPES 5.25 mm across a 300 mm
window**, so a single global `min(z)` put the fold at row **373** while the mask's own lowest row was
**239** — **134 px = 25 mm wrong**. The fold is tracked **PER COLUMN** off the mask now. Rev 53's
arm D had already learned this and I re-learned it. **Rule 7: ask the geometry, never the pose.**

### §2.8 THIS FILE WAS AUDITED AGAINST THE MACHINE, AND THE AUDIT FOUND SEVEN THINGS

Rule 17. Every file cited below was opened, every quoted string grepped, every figure recomputed
against the probes' own printouts and against the source. **What it found:**

| what the draft said | what the machine says |
|---|---|
| `verify_clone.sh` **ALL 165 PASS** (carried from rev 54's §1) | **173** — this revision added eight rows |
| rev 53's work landed through **PR #9** (rev 54's §1) | **PR #10.** #9 was rev 52's. Read off `git log`, not carried |
| "not one row anywhere names a wheel, hub, cap, rim or vent" | **too strong** — track, tyre diameter and the arch-to-tyre gap are all guarded in `verify.py`. See §2.6 |
| the two glyphs "differ by 25.32 % as built" | **5.09 %.** The 25 % was MY comparison error — the nose is fitted to 0.84 × its ring, the hubcap flush, so I divided by two different denominators. Recorded because it was wrong for a plausible reason |
| `T1_EDGERAD=12` is **3.3 px** (rev 54's own audit said 3.25) | **3.25 px**, and this brief no longer quotes 3.3 |
| the draft cited **`rev54_look_ladder.png`** | **the path does not resolve** — it is `probe_scratch/rev54_look_ladder.png`. Caught by a sweep that tries to `stat` every file the brief names; the other 33 all resolved. Rule 18's neighbourhood: a citation nobody can follow |
| a paragraph said this brief *"deliberately does NOT name the retired `T1_EDGEBEVEL` switch"* | **false the moment it printed the name** — and it silently re-created the dependency it claimed to remove, because the `every T1_ switch the brief names exists` row sweeps every `T1_*` the brief mentions and only one surviving `probe_rev53_chip.py` comment keeps that row green. Rewritten to say so; **see §6** |

**Two of the seven were found only by RUNNING the audit as a script rather than re-reading the
draft** — the unresolvable path and the self-refuting paragraph. Re-reading had already passed over
both. **Five of the seven were transcription or self-contradiction, not measurement**, in a file
whose own §1 says not to transcribe.

**VERIFIED CLEAN BY THE SAME AUDIT** — recomputed or grepped, not re-read: every file cited below
exists; `CAP_EMBLEM_WFRAC = 0.2087` and the new denominator note are both in `t1_detail.py`;
`T1_PTWEAR` and `T1_EDGERAD` are real levers in `t1_mats.py`; `W_EDGE_90 = 1.0 - cos(45°) = 0.29289`
recomputes exactly; 1000/271.2 = **3.687 mm/px** and 1000/211.5 = **4.728**; 0.2087/0.814 =
**0.25639** and 0.1986/0.814 = **0.24398**; the coverage/radius ratios recompute to
0.0995/0.112/0.113/0.114; **`BAYS[2]`'s aft edge is still exactly −0.855750 and the sixth hook still
51.25 mm beyond it**; and the **A7 gap is 803.0 mm** off the live `t1_core.X_TAIL = −1.873000` — not
re-derived by hand here, because rev 53 made it a `verify_clone` row **derived on both sides** and
that row passes, which is worth more than a fourth transcription of the figure.

**THIS FILE MUST STAY BYTE-IDENTICAL TO `PASTE_INTO_CLAUDE_CODE.txt`.** `CLAUDE.md` imports that
file into every session as the entry procedure, and rev 52 let it go two revisions stale. **WHEN YOU
WRITE THE REV-56 BRIEF, `cp` IT OVER `PASTE_INTO_CLAUDE_CODE.txt` IN THE SAME COMMIT, OR
`verify_clone.sh` FAILS AND NAMES THE ROW.**

---

## §3. THE WORK LIST FOR REV 55

**1. THE TWO VW BADGES — HIS REPORT AT REV 51, STILL THE TOP JOB.**
**The DIAMETER route on `ref_side.jpg` is EXHAUSTED** (0.3474 vs the built 0.3170 — 9.6 % small but
only **1.8 sigma**; rev 51's figure, INHERITED, do not re-run it). **The open constant is the STROKE
WEIGHT**, and rev 54 established what it actually denominates (§2.5) — **compare a frame against
0.25639, not against 0.2087.** Full text and the four closed routes in **`PHOTOS_WANTED_rev52.md`
item 7**. The guard gap on the part is now partly closed (§2.6) but **still nothing measures the
badge against a photograph.**

**2. THE CHIP GATE READS THE SHADING NORMAL, NOT THE TRUE NORMAL — AND ON THE SHELL THAT MATTERS.**
New at rev 54 and the natural successor to item 2. `t1_mats.py` links `geo.outputs["Normal"]` into
the dot product while its own comment says *"true geometric normal"*. On `counter` (FLAT) the two
are identical, so the rev-54 result is unaffected. **`T1_body` is SMOOTH-shaded with 61 737 polys**,
and there the shading normal is already interpolated across every fold — which is exactly what the
Bevel node approximates, so `EDGE` may be **suppressed on the whole red shell**. The AOV probe
already exists and takes a tap by graph walk: point it at a shut line or an arch lip, then swap the
dot's second input to `True Normal` and measure the difference. **Cheap, unblocked, and it decides
whether the red's edge wear is real.** It also decides whether the comment or the code is the defect.

**3. FINISH A9. Two of its four parts are done; the galley is still ~103 mm too far aft.**
**PROVENANCE, GRADED: the per-feature deltas are INHERITED from the rev-52 brief and have NOT been
re-measured at rev 52, 53 or 54.** The offset is **NOT rigid** (−0.09574 at hook u=0.13 to −0.11035
at `gal_appliance` u=0.80, so one additive constant leaves ±7.3 mm). Re-derive each X from `BAYS`,
the way `gal_rail` now is. *(The survey's ~106 mm and its +0.096..+0.113 range are both wrong.)*

**4. THE THREE HOLES REV 52 LEFT OPEN, all cheap to reach.**
**PROVENANCE, GRADED: the 260.0 mm and 20.0 mm sight lines are rev 52's and were NOT re-measured at
rev 53 or 54.** The other two figures WERE recomputed at rev 54's audit and reproduce exactly.
* `gal_end_f` sees past by **260.0 mm** on the show side and 20.0 mm on the off side. Needs its own
  sight line established first — **do not inherit `REAR_W/2`** (rule 34: that figure belongs to the
  rear window, which is not what looks at it).
* The **sixth hook at X −0.907 lies 51.25 mm beyond `BAYS[2]`'s own aft edge (−0.855750)**. The six
  hook stations are typed literals with irregular spacing whose span centre is **−0.705** against the
  rail's measured **−0.598**. **They disagree and one of them is wrong.**
* A7's real defect: `roof_cutters()`'s aft edge is `LID_X1`, which is **not** greppable as
  `LID_X1 = -1.0700` — the source line is `LID_X0, LID_X1 = 0.9640, -1.0700` in `t1_shell.py`, so
  **803 mm of roofed body** sits between the last light inlet and the tail skin. Unbuilt. A7 is
  **ILLUMINATION, not dressing.**

**5. A13 / A16 / A12** — the isolated star built BELOW the burst where both red frames put it above;
every flank rosette drawn at the diameter of its **gold core**; *A12 is an OWNER RULING, not a
do-now* — `senor_trace.py` calls the remedy *"inventing ink the photograph does not show"*.

**6. A11's SECTION, A14** — a chrome lever lying in a dish **pressed into** the skin against a 12 mm
**proud** prism; the `lid_rail` WIDTH (§3.1).

**A CHEAP UNBLOCKED ITEM, STILL NOT DONE AFTER THREE REVISIONS:** `SPEC` §8's colour locks are all
graded **M** = *"measured by me from `ref_source.jpeg`"* — a 246×197 thumbnail the record itself
calls retired. They can be re-derived on `ref_playa_34.png` at **4× the area** with no new
photograph. **Report the re-derived values; do not change the constants without his ruling** — W6
makes colour his call. *(And `ref_playa_34.png` is byte-identical to `IMG_3842.png`; a duplicate is
not corroboration — rule 11.)*

**THE PROCESS ROWS, still open:** the **open-findings** register abandoned at rev 45 (21 rows); the
standing-instructions carrier deleted at rev 44, which took the **die-cut sticker — the project's
original deliverable** — with it, **still open**; SPEC §0.2's two rev-4 corrections later refuted;
rev 48's refuted *"B stays open"* still live in `build.py` and, **split across two lines so a flat
grep misses it**, in `t1_shell.py`; the tail board still has **zero rows in either verifier**.
**`cream_rms.py` IS NOT DORMANT — IT IS DEAD, AND REV 54 RAN IT TO FIND OUT.** Three briefs have
carried *"it was not run"* as if running it were the task. Run on `out/r54c_side.png` (a 1248 px side
ortho, the 211.5 px/m scale the script's own defaults expect), it **refuses to emit a number** and
says why: `ref_side.jpg` holds **1799 body-cream pixels = 0.23 % of the frame**, its best 60×20
window is **33.8 % pure**, and the legacy patch is **100 % inside the guarded serving-aperture band**
— the galley interior seen through bay 3, not paint. Its own printed remedy is
*"Re-base on `ref_rear34.jpg` (rev 17)"*. **THAT re-base is the task, and it has been open since
rev 17.** Still zero rows in either acceptance script.
**`flank_compare.py` WAS RE-RUN AT REV 54** on a fresh `out/r54_side.png`, and still fails 2 of 4 —
read its own summary line, not its exit code:

| | rev 53 | **rev 54** | |
|---|---|---|---|
| ink area ratio | 0.9417 | **0.9425** | PASS |
| ink aspect | 2.3689 | **2.3689** | **FAIL** — 2.3689 vs a reference 2.2512, +5.2 % |
| IoU vs ceiling | 0.7608 | **0.7618** | PASS |
| worst region (Senor) | 0.471 | **0.476** | **FAIL** — target ≥ 0.75 of its own ceiling |

The rev-53 figures reproduce to <1 %, so they were sound and the small moves are render-to-render,
not regression.

**AND THE COLOUR BLOCK UNDER THAT SUMMARY HAS NEVER BEEN QUOTED IN A BRIEF.** Same run:

```
reference untarnished ink  mean (126.8, 118.7, 122.2)  sd (13.6, 14.7, 16.6)  luma p5-p95  94-133
render     all ink         mean (168.0, 157.3, 158.5)  sd ( 9.4, 17.2, 20.6)  luma p5-p95 128-176
```

**The render's flank ink is +41.2 / +38.6 / +36.3 DN brighter on the three channels.** Its **HUE is
right**: G/R is **0.936 in the photograph and 0.936 in the render**, so this is NOT the G/R shortfall
W6 ruled on — it is a LEVEL difference, and it is large. **What it is NOT yet separated from is the
rig's own exposure**: if the cream around the ink is also ~39 DN high then this is the studio
lighting, which is his settled call, and not an artwork defect. **That separation is one painted
window away and rev 54 did not do it. Do it before touching any ink constant** (rule 29.3: no finding
is attributed to a cause until a control separates it).

### §3.1 `lid_rail` — STILL MEASURED AT ZERO AREA, STILL GUARDED, STILL DELIBERATE

Both objects are **0.000000000 m² with 18 of 18 faces degenerate**. `STATE.md`'s zero-area sweep
still reports *"2 of 223 meshes have zero area; 2 exempt and KNOWN OPEN"*. **It is exempt in
`verify.py`, not fixed, because the rail's WIDTH is measured NOWHERE.** The exemption is two-sided
and cannot outlive the defect. **This is an owner question.**

### §3.2 THE HABIT THAT PAID AT REV 54, TWICE, AND THE HALF OF RULE 3 THAT MATTERS

**PAINT THE WINDOW AND LOOK AT IT BEFORE IT PRODUCES A NUMBER.** Rev 54 caught **two** of its own
windows this way and neither by reasoning: the four-wheel "ring" (§2.7) and the sloping fold's row
(§2.7). Both produced a plausible number that would have been published.

**A GUARD NEEDS BOTH HALVES — watch it FAIL on the defect AND PASS through a legitimate re-wording,
on a CLEAN tree.** Rev 54 added **fourteen** guards: eight `verify_clone.sh` rows and six
`verify.py` section-13 mesh clauses. All fourteen were watched both ways — **but the six were only
watched AFTER the revision had once been reported as finished** (`LEDGER_rev54.md` §7.1). The eight
grep-rows were exercised the same hour they were written and the six mesh clauses were not, because
`VERIFY: 0 fail, 0 warn` reads like evidence and is only the PASS half. **If you add a clause to
`verify.py`, injecting its defect is not optional and `VERIFY: 0 fail` does not stand in for it.**
And when an injection does NOT fire, suspect the injection first: one of mine patched a shared
builder that `build.py` calls with the same arguments four times, so the branch never ran (§7.1).
The one that
matters most: the row banning the stale `DEFAULT IS STILL POINTINESS` sentence must not fire on a
comment that merely **quotes** it — and the shipped tree contains exactly such a quote, so that half
is live, not hypothetical. It is anchored on the line **starting** with the claim.

**AND A GUARD ON THE CODE DOES NOT GUARD THE PROSE BESIDE IT.** §2.4: the flip-guard passed for a
whole revision while the block above it asserted the opposite default.

**A PREDICTION WITH CONTROLS BEATS A COVERAGE NUMBER.** The AOV's claim was tested by cropping the
beauty render at the AOV's own predicted chip sites **and at control sites on the same fold**. Four
of four predicted showed chips; four of four controls were clean. A single coverage figure could not
have said that.

---

## §4. WHAT ONLY HE CAN GIVE

**`PHOTOS_WANTED_rev52.md` is the carrier for item 7 (ONE HUBCAP, SQUARE ON AND CLOSE)**. Items
**1–5** keep their full text in `PHOTOS_WANTED_rev49.md`: the tail board's footing; the decal darker;
the nose square on; a raking-light frame of the louvres (**ONE item — the pressing depth**; the
"block length, station and V swage" expansion is a proposal, not the record); the off side, any
frame. **He has said 1–5 are not possible now. DO NOT RE-ASK THEM.** Item 6 (an obliquely-seen wheel)
was **DISSOLVED at rev 51** — struck, not outstanding.

**CARRIED FROM REV 53, still no carrier outside these briefs:** a frame showing the cream **where it
IS chipped** — any close frame of a worn edge. **Rev 54 lowers its urgency further, not raises it:**
the band is 0.27 px at every scale this project ships, so grounding the radius changes nothing
visible. It is only worth asking if a close counter view is ever wanted.

**NEW AT REV 54 — A ROUTE TO THE STROKE WEIGHT THAT THE RECORD DOES NOT LIST, AND ITS CEILING.**
`PHOTOS_WANTED_rev52.md` item 7 closes four routes, and all four are about the **hubcap** badge.
Neither closes the **NOSE** badge, and the nose badge is the same design — the record says so and
already **transferred its RING BAND from one to the other** (`t1_detail.py`: *"ref_workshop.jpg nose
badge … = 0.0874 / 0.0995 … ring band / ring outer D = 0.093 ± 0.012 adopted"*).

* `ref_workshop.jpg` shows the nose badge at **91.7 px vertical D, PSF sigma 0.689 px** — a stroke
  of ~0.25 R is ~11 px, **resolved**. Verified at rev 54: the record's crop box **(258,494,352,604)**
  is correct and the badge is cleanly legible in it (`probe_scratch/rev54_wsbadge_x8.png`).
* **CEILING, AND IT IS WHY THIS IS A ROUTE AND NOT A RESULT.** (a) `ref_workshop.jpg` is the **GREEN**
  vehicle (`SPEC.md`: *"carries the same 'Señor Tacombi' script on the green body"*), and his
  standing ruling is that **paint and artwork do not transfer between vehicles**. A pressed factory
  badge is arguably GEOMETRY, which rule 11 says does transfer — **but that is an argument, not a
  measurement, and the same argument already underwrites the shipped ring band.** Either both are
  legitimate or the ring band is grounded on the wrong vehicle. **Resolve that before publishing a
  number from it.** (b) The badge is **strongly oblique** — 62.7/91.7 = **0.684 axis ratio** — so it
  must be de-projected first, and only vertical extents are trustworthy. (c) The RED bus's own nose
  roundel is in `ref_nolita_front34.jpg` at a **41 × 66 px** bbox (`SPEC.md`'s own figure) — the
  right vehicle, but a 700×467 JPEG.
* **NOT ATTEMPTED AT REV 54, deliberately.** Rev 51 spent a whole revision on the diameter by this
  kind of route and reached 1.8 sigma. This is scoped as a revision's work, not a spare hour.

---

## §5. THE RULES — `CLAUDE.md` CARRIES THE METHOD, NOT THE NUMBERED CANON

The canon (rules 1–33) is printed in `NEXT_CONTEXT_PROMPT_rev50.md` §11. **Rules 34 and 35 live only
in the rev-51/52/53/54 briefs and `LEDGER_rev50.md` §0, so they are carried here too — that is
`CLAUDE.md`'s own rule 16 firing on this file:**

> **34. A REQUIREMENT INHERITS ITS OBJECT EXACTLY AS A RETIREMENT DOES.** Before relying on any
> *"the record requires X"*, check which object the sentence is about — and check the cited line
> exists. **Rev 52 applied this deliberately**: `gal_end_f` was left alone because `REAR_W/2` belongs
> to the rear window, which is not what looks at it. **Rev 54 applied it to a photograph**: item 7's
> four closed routes are all about the HUBCAP badge and none of them closes the NOSE badge (§4).

> **35. A GUARD WRITTEN AGAINST A POSE ENCODES THAT POSE.** Guards that identify a part's foot or
> free edge by `min(y)` are only right while the part leans one way. Ask the geometry.
> **Rev 53 broke this and was caught by it**; **rev 54 broke it again** — a global `min(z)` for a
> fold that SLOPES, wrong by 25 mm (§2.7).

> **Rule 29.3:** no finding is attributed to a cause until a control separates it. **Rule 29:** a
> retirement inherits the object it was made about. **Rule 15:** a retraction that lands in a ledger
> and not in the source is half a retraction — **rev 54's retraction of "this fold is silent" is in
> `t1_mats.py`, not only in `LEDGER_rev54.md`, and a row holds it there.**

---

## §6. THIS MACHINE

```
cores 4   RAM 15 GB   Blender 4.5.3 via pip install bpy   subagent concurrency 2
build  T1_SUB=1 ~19 s     render 1600x1100 96 spp ~4-7 min PER VIEW
```

```bash
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b -P build.py     # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=side T1_PFX=r55 T1_RX=1600 T1_RY=1100 T1_SAMP=96 \
  /tmp/blender/blender -b -P build.py
T1_PREVIEW=hero34r ...                                       # the REAR 3/4 -- A7 lives here
T1_SUB=2 /tmp/blender/blender -b -P audit.py                 # rewrites STATE.md -- COMMIT FIRST
python3 lid_gen.py                                           # regenerates tex/lidmural.png
python3 flank_compare.py out/r55_side.png /tmp/fc.png        # THE FIDELITY GATE.  Exits 1 today.
python3 probe_rev53_chip.py                                  # the chip measurement, all six arms
T1_SUB=1 T1_AOVSAMP=64  /tmp/blender/blender -b -P probe_rev54_aov.py    # the EDGE AOV + sweep
T1_SUB=1 T1_LOOKSAMP=192 /tmp/blender/blender -b -P probe_rev54_look.py  # the scale ladder
/tmp/blender/blender -b -P probe_rev54_wfrac.py               # the badge denominator, calibrated
T1_SUB=1 /tmp/blender/blender -b -P probe_rev54_badge.py      # the badge off the built mesh
```

**`out/` IS NOT TRACKED and starts empty. Render before quoting any probe that reads a frame.**
**A backgrounded runner's exit code is the WRAPPER'S, not Blender's — grep the log for `Saved:`.**
**`probe_rev54_aov.py` deletes nothing but writes ~6 MB of EXR into `probe_scratch/`; rev 54 removed
them before committing and kept the PNGs and one 4 KB `.npz`.**

**ABLATIONS — every one exists to WATCH A GUARD FAIL.** `T1_PTWEAR=1` (restores the Pointiness chip
gate and moves nothing else — proven by render at rev 53: **8.795 %** under the switch against
**8.826 %** when Pointiness was the default and **0.000 %** shipped) and **`T1_EDGERAD`** (the Bevel
radius in **millimetres**; unset keeps the derived `GAPW/2`, and rev 54 swept it at 1 / 2.75 / 6 / 12).
Carried from before: `T1_TARNCONTAM=1`, `T1_RAILSTALE=1`, `T1_ENDSHORT=1`, `T1_CAPSINK=1`,
`T1_LIDDEG=104`, `T1_BAYSTALE=1`, `T1_LAMPSINK=1`, `T1_LIDASPECT=1.2`, `T1_HANDLEHI=1`,
`T1_BAREMAT=1`, `T1_TBFOOT=1`, `T1_BAYPROUD=1`. Also live: `T1_NOBEVEL=1` (stands the whole
round-edges pass down) and `T1_BEVEL_SAMPLES`.
*`T1_EDGEBEVEL` is RETIRED — it became the default at rev 53 and is **gone from the shader**. Do not
cite it as a lever. **AND NAMING IT HERE HAS A COST, WHICH THE AUDIT OF THIS FILE CAUGHT:** the
`every T1_ switch the brief names exists` row sweeps every `T1_*` this brief mentions, and the only
thing keeping that row green for this one is a single surviving comment in `probe_rev53_chip.py`.
A draft of this paragraph claimed the brief "deliberately does NOT name" it — which was false the
moment it printed the name. Either keep that comment or drop the name from the brief; the two are
tied together.*

---

## §7. THE STANDARD, IN HIS WORDS

We are recreating a photorealistic version of **that exact bus**, and **any single measurement off is
unacceptable** — per-measurement, not on average. A model right in ninety places and wrong in one is
not 99 % done, because he will look straight at the one.

`bus_model_ref.JPG` is a **SCHOOL BUS** and is **NOT the vehicle** — a FIDELITY BAR only. Use
`ref_workshop.jpg` the same way, and remember it has **no headlamps and no hubcaps fitted** and is
the **GREEN** vehicle (§4).

**Ground in the reference, build, adversarially audit, iterate.** Never build before grounding. Never
call it done off self-review. Report the measurement **with its ceiling**, never a self-assigned
score. Do not say anything is ready — say what is fixed, what is still wrong, and what you measured.

**RENDER IT, CROP IT, AND LOOK AT IT, before and after every change.** Every defect this project has
shipped passed `VERIFY: 0 fail, 0 warn` and was found by looking at a crop. **Rev 54's whole result
turned on this: the AOV said the chips were there, and only the cropped beauty render with its four
control tiles proved it.**

**When you need something from him, ask as MULTIPLE CHOICE with the reference material attached — one
crop, one mark, one sentence — and ASK IT WITH THE QUESTION TOOL.** He has never stood in the bus: do
not ask what the real vehicle looks like, ask what a PHOTOGRAPH shows. **Rev 53's whole A6 result
turned on one such question, and the crop had all three states at the same mm/px so he could compare
them by eye.** **Rev 54 asked him nothing** — everything it did was measurable without him, and that
is stated rather than dressed up as consultation.

**`git rev-list --count origin/main..HEAD` before you start and again before you finish. And
`git diff --name-only HEAD...origin/main` — that is where his photographs arrive. EVERY session.**
