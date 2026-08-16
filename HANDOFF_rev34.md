# HANDOFF rev 34

**NO GEOMETRY MOVED. NO SHADER. NO ARTWORK.** The last geometry change is
still rev 30's. Guards **0 fail / 0 warn at both subdivision levels**, every
figure identical to rev 30/31/32/33's.

rev 34 did five things:

1. **Graded the instrument BEFORE spending a question on the owner** — and
   found §10.87's A7 comparing a LIVE sensitivity against a SYNTHETIC one.
2. **Made a pre-commitment that FAILED before the question went out**, and
   said so on the question figure itself.
3. **Asked the far-strut question anyway**, for the column it does buy, with
   the brackets on both sides the rev-34 brief demanded.
4. **Consumed two owner answers and RETIRED the cross-ratio route** — on a
   precondition failure, not a precision shortfall.
5. **Recorded five defects of my own**, three of them the same family, one
   caught only by an arm that could not have fired.

---

## 1. What arrived, and how it was verified

Folder **already in `connectedFolders` on the first `get_device_info`** —
third revision running (32, 33, 34). No grant needed.

Bridge: **30 files, ~9 calls, zero transient failures** — second revision in a
row. rev 33's `_xfer33` split parts were reused rather than re-split; **7 md5s
matched on both sides**, including both reassembled bundles.

Restore CLEAN, every waypoint on the published chain:
34 → 59 → *(rev14b fetched)* → 67 → 71 → 75 → 81 → 87 → 93 → 96 → 101 → 105 →
107 → 115 → 120 → 126 → 130 → 135 → 148 → 158 → 166 → **173**, clean tree.
**42/42 content greps, 12/12 ancestry, 3/3 texture md5s.**

`STATE.md` on arrival was **healthy** — generated 2026-08-16 19:51 UTC,
`working tree | clean`, byte-identical to `STATE_rev33.md` and *not* to
`STATE_rev31.md`. Its hash `83fd5b8` is commit #170; the file landed in #171
and only three doc commits follow. **§10.87.5's fix held.**

## 2. Guards, both levels — actual output

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 0 warn** | **0 fail, 0 warn** |
| audit.py | **0 fail, 0 warn** | **0 fail, 0 warn** |
| roof crown @ rear axle | 1.9835 (−0.0 mm) | 1.9833 (−0.2 mm) |
| rear arch lip → gap | 0.3722 → 39.7 mm | same |
| front arch (control) | 0.3732 → 40.7 mm | same |
| rake | 17.75 mm/m (locked 17.75) | same |
| dims | L=4.065 W=1.750 | same |
| cut roof hole | 68564v | 252749v |
| objects at `materials:` | 127 | 127 |
| shut line × aperture | 0.0 mm / 804.9 mm | same |
| `CARGO_GAP` samples | 154 | same |
| bay widths | 0.516 0.515 0.516 | same |
| over-rider row | 97.51 mm above blade top, dia 24.97 mm | same |

186 meshes, 42 materials, 5 constant-rough, 0 non-manifold, band 1.372–1.775.
**Every geometry figure identical to rev 30's, 31's, 32's and 33's.**

## 3. Inherited probes — all twenty run

| probe | result | matches published |
|---|---|---|
| `probe_rev33_barend.py` | **7 checked, 4 FAILED** (A4–A7) | ✓ all four are the result |
| `probe_orb_xratio.py` | **6 checked, 1 FAILED** (C5 KILL) | ✓ |
| `probe_rev32_pointer.py` | 10 checked, 0 FAILED | ✓ |
| `probe_dust_scope.py` | 8 checked, 0 FAILED | ✓ |
| `probe_updust_pointer.py` | 6 checked, 0 FAILED | — |
| `probe_psf_lines.py` | 2 FAILED, **both expected** (rev-28 finding) | — |
| `probe_clean_top.py` | H2/H3 FAIL | ✓ left failing on purpose |
| `probe_dust_anchor.py` | FAIL | ✓ left failing on purpose |

The degeneracy was reproduced live rather than taken on trust: `probe_clean_top`
prints `dusty COUNTERTAN (SHIPPED)` and `CLEAN COUNTERTAN (f = 0)` as the
**same triple** `(0.9511, 0.7815, 0.5298)`, then `dusty 34.0 % -> clean 34.0 %`,
while its prose two lines below still argues removing the dust is NECESSARY.
**Neither probe was touched.**

**THE `bpy` MEMBERSHIP IN THE REV-34 BRIEF IS RIGHT FOR THE WRONG REASON.**
Six probes need Blender and the count is correct, but a `grep` for `bpy`
returns **two false positives** (`probe_clean_top`, `probe_dust_anchor` — the
token appears only in a comment explaining why they parse `t1_mats` with `ast`)
and **two false negatives** (`probe_cross_anatomy`, `probe_shutlines` — they
import it transitively, with the token nowhere in the file). **4 − 2 + 2 = 6.**

## 4. SPEC §10.88 — the substance

### 10.88.1 The instrument, graded before the question

`probe_rev34_levels.py` — **8 controls, 4 FAILED.**

`probe_rev33_barend.py` gates **in two units inside one file**: A3 in PIXELS
(`dU <= 4`), A7 in PER CENT (`sw4 <= interp_error(4)` → 6.2 %). `interp_error`
reads a frozen dict whose own comment says it is **P1b's SYNTHETIC map, planted
f 0.626**. So A7 prices the strut LIVE and the far end SYNTHETICALLY.

The map's columns against the live ones: far end 208.9 vs 205.0, strut 224.6 vs
228.0, post **356.6 vs 365.5 (8.9 px)**, hoop 487.2 vs 485.0. **The map is wrong
by up to 8.9 px about a configuration whose 4 px errors it is used to price.**

- **K1 FAILS** — the curve **under-prices by 1.39× at 4 px, 1.28× at 8 px**.
  The published **6.2 % closing level is 8.6 % live**; the **14.3 % failing
  level is 18.3 % live**.
- **K3 PASSES** — the strut IS the more sensitive column like for like.
  **§10.87's A6/A7 conclusion survives.** Its margin does not: **1.79×
  published, 1.28× like for like, a 39 % overstatement.**
- **K2 FAILS** — the two units disagree across the decision boundary on
  §10.87's own residual. Its justifying sentence converts px → % unnecessarily
  and lands on the synthetic value: **live it is 7.5 %, not 5.4 %.**
- **K4 FAILS** — the same 4 px costs 8.6 % on the far end and 11.1 % on the
  strut, a **constant 1.28×** at every perturbation.

### 10.88.2 The pre-commitment — it failed before the question went out

**K5 FAILED BEFORE THE OWNER SAW ANYTHING.** Far end already spends 7.5 % of
an 8.6 % live tolerance, leaving 4.27 % in quadrature → the strut needs
**±1.5 px**. A 7 px set returns ±3.5 px (12.2 % total); 4 px lines return
±1.8 px (8.9 % total) — still over. **Printed on the question figure in red.**

### 10.88.3–4 The two answers, and the ruling

- **Q1** *[stated]*: **S1 or S2 — LEFT of the hard-coded 228.**
- **Q1b** *[stated]*: **B1 or left of it — u 205 to 208.**

Both leftmost. **Q1's left side was already walled** — the cross-ratio requires
`far_end < strut`, so with the far end at 205 everything at or left of 205
returns ORDER BROKEN. S1 sat **7 px from a hard wall**, not a boundary I chose.
**Interval closed on both sides: u ∈ (205, 208].**

`probe_rev34_ruling.py` — **6 controls, 4 FAILED.**

**What the answers bought:** the last hard-coded column in the estimator is now
a measured value with a two-sided interval. **And u 228 was outside it
entirely** — 20 to 23 px away, `f` 0.5897 against 0.835–0.950. **Every C5 row
since rev 32 ran at a column the owner does not put the feature near.**

**R3 FAILS** — the strut sits **1.5 px** from the far end, whose own residual
is **±3.5 px, 2.3× the gap**. Not separable.

**R4 FAILS** — sweeping the far end across its own 201.5–208.5: `f` 0.7947,
0.8246, 0.8809, 0.9292, then **ORDER BROKEN at 206.5, 207.5, 208.5**. **29 % of
the far end's own error bar violates the construction's precondition.**

> **THE FOUR-POINT CROSS-RATIO HAS DEGENERATED TO THREE — a PRECONDITION
> failure, not a precision one.** No further measurement on those two columns
> repairs it.

**R5** corroborates: ±1 px costs **9.5 %** in the answered regime against
**2.7 %** where the levels were graded, **3.6× worse**, and ±1.5 px returns
nothing. **R6**: 13.6 % against 8.6 %.

**Every prior revision assumed 23 px of separation.** The owner's reading makes
it 1.5 px. **Nobody could have found this by measuring harder.**

**THE POST STAYS UNBUILT. NO `f` IS PUBLISHED AS A BUILD VALUE.**

## 5. Defects of my own — five, all recorded

- **My `swing()` silently dropped an `ORDER BROKEN` sample** and computed the
  spread over the survivors, so R5's ±1.5 px cell printed **5.5 %** for a
  regime that had broken, while the prose below said it returned nothing.
  **A narration contradicting its own table.** Fixed.
- **An arm that could not have fired.** Arm A refit P1b's synthetic map to
  reproduce all four live columns exactly. **K1 did not move** — its synthetic
  side reads a **frozen literal**, not the map. Arm B replaced the dict; K1 and
  K2 flipped to PASS. **Refitting a map cannot move a control that reads a
  hard-coded dict.**
- **Arm B caught a defect in my own probe** — K2's detail string narrated
  "THE TWO READINGS DISAGREE" while the control PASSED. Now computed.
- **Arms 4 and 5 caught a third instance of the same family**: with a POSITIVE
  control down, both probes still printed rulings asserting "R1 passes" and
  "N1 and N2 both pass". **Both probes now REFUSE TO PRINT A RULING if a
  positive control failed** — verified by re-running arm 4.
- **Two guard arms did nothing on the first try**, each caught by printing the
  changed line: `BAR_RISE` is not a literal (it is `BAR_RISE_RATIO ×
  APERTURE_M`), so a regex on `BAR_RISE = <number>` matched nothing and the
  guard printed **0 fail** — *what a guard that failed to fire prints*; and
  `W_DUST_FAC_UP` **is not in `_RETIRED_VALUES`**, so injecting it into SPEC's
  frozen front matter fired nothing. **rev 33's exact mistake, repeated.**
  Re-armed on `BAR_RISE_RATIO` (2 fails) and on the watched literal `0.0330`
  (1 fail).
- **Two figure-rendering defects**, both caught by cropping the PNG and looking
  at it: the Q1 figure clipped its header (canvas sized off one text block
  while three were drawn — now every drawn string is measured); the Q1b wall
  label landed first across the B1–B4 tags and then across the candidate lines
  (now drawn last).

## 6. Falsification — every arm, and the changed line printed first

| arm | change | result |
|---|---|---|
| 1 | `BAR_RISE_RATIO` 38.7 → 41.7 (+3 mm) | **2 fails** |
| 2 | `overrider_bar()` dropped from `build.py` | **1 fail** |
| 3 | retired literal `0.0330` into SPEC's frozen front matter | **1 fail** |
| 4 | `POST_U` 365.5 → 372.5 in the ruling probe | **R1 FAILS, ruling REFUSED** |
| 5 | `SYN_F` 0.626 → 0.640 in the levels probe | **N2 FAILS** |
| A | synthetic map refit to the live columns | **K1 did not move — a non-arm** |
| B | `P1B` replaced by the live curve | **K1 and K2 flip to PASS** |
| C | `STRUT_U` 228 → 260 | K4 1.29× → 1.98× |
| fig | `C5_PUBLISHED[221]` 0.7390 → 0.8390 | **REFUSED TO WRITE, nothing on disk** |

## 7. Things you must not silently undo

- **`probe_clean_top.py` and `probe_dust_anchor.py` are still deliberately
  failing.** They need rewriting, not fixing. Do not widen a tolerance.
- **`probe_orb_xratio.py`'s `strut_u = 228.0` is DELIBERATELY LEFT.** A probe
  that cannot reproduce its own published result is not a record. §10.88 states
  the corrected interval beside it.
- **`probe_orb_post.py`'s `V_APEX_U = 311.5` stays**, same reason (rev 32's
  decision, unchanged).
- **`BAR_DIA` and `BAR_RISE` remain `ratio × APERTURE_M`.** The 10.83 verify
  row's reference is FROZEN in `verify.py`, window `x > 2.100`.
- **The hero `rev30_hero34f.png` is not re-shot.** Proved by content in rev 31.
- rev 32's §8 through rev 18's §4 all still stand in full.

## 8. Still open, in order

1. **THE POST.** The cross-ratio route is now **RETIRED**. The only remaining
   construction on this panel is the **transverse VP by harmonic conjugate**,
   which is **UNPUBLISHED, not refuted** (§10.86). **A square-on frame of the
   FRONT still collapses the whole problem** and is worth more than any
   further measurement.
2. **Rewrite `probe_clean_top.py` and `probe_dust_anchor.py`**, or retire them
   with a stated reason. Decide first what the post-retirement question is.
3. **Re-run §10.70's arms** before quoting any of its percentages; the harness
   has **no cyclorama** (§10.78) — state that, do not silently fix it.
4. §10.83's centreline claim is **UNDECIDED**, fifth revision running.
5. REF §9's V-swage absolute height is a **bracket, ≈0.40–0.49 m**.
6. Tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
7. **THE FRONT BUMPER FACE IS UNMEASURED. `CREAM`. THE ABSOLUTE ROOF HEIGHT.
   THE OFF FLANK, 804.9 mm.** `COUNTERTAN` 34.0 % short in B. `GAL_SKY` dead
   lever. `PLATE_W = 0.3300` no provenance. `probe_rev16.py:90` prints `xa`
   vs `xa`.
8. Camera absolutely last.

## 9. Grep counts INVALIDATED by rev 34

**`grep -c 'UNDECIDED' SPEC.md` was published as 9 in the rev-34 prompt. §10.88
adds one and it is now 10.** *A grep count is invalidated by any later edit to
the file it counts — including a later revision's.* Marked in the rev-35 prompt.
