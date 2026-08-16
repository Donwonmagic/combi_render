# HANDOFF rev 28 — 2026-08-16

**129 commits, clean tree. Guards 0 fail / 0 warn at BOTH subdivision levels.**
**NO GEOMETRY MOVED. NO ARTWORK MOVED. NOTHING WAS TUNED.**

> The standard, in the owner's words, governs every line below: *"The final
> product should be nearly indistinguishable from the original. **Any single
> measurement off is unacceptable.**"* The criterion is PER-MEASUREMENT. And
> above clinical accuracy: *"I really want this to give the person the
> opportunity to feel like they were on Playa del Carmen all those years
> ago."* **That owner is the restaurant's owner, not Donald.**

---

## 1. How rev 28 opened

**NOT CLEAN — and the failure was environmental, not the repo's.** No folder
was connected to the session, so the fifteen restore bundles and the three
reference photographs were unreachable, and the first folder-access dialog
closed unanswered. Once granted, everything was in order:

- All six rev-27 deliverables on his Desktop at the exact sizes memory records
  (bundle 57 755, tarball 19 773 831, SPEC 332 497, STATE 8 447, HANDOFF
  11 445, prompt 28 570).
- **SIXTEEN bundles crossed in ONE `device_stage_files` call.** All eleven
  md5s recorded in memory matched exactly.
- Restore 59 → 67 → 71 → 75 → 81 → 87 → 93 → 96 → 101 → 105 → 107 → 115 →
  120 → **126, clean**, no divergent-branches error.
- **21/21 content checks exact, 8/8 ancestry**, three texture md5s correct
  including the corrected `swirl_b` `d201597e`.
- Guards on arrival **0 fail / 0 warn at both levels**, every figure in the
  rev-28 prompt's §2 table reproduced.
- Blender 4.5.3 + pillow 12.3.0 + scipy 1.17.1.

**Lesson for the next context, and it is new:** the restore is not the only
thing that can be missing on arrival. **Check that a folder is connected before
planning the revision** — everything in §6 of the prompt is blocked without one,
and the dialog can time out.

---

## 2. §10.80 — THE PSF IS MEASURED, and §10.79's own reading was what was wrong

§10.79 built a validated estimator and **correctly declined**, because an
estimator cannot tell an occlusion step from a paint boundary. It offered its
own reading — the candidates sit on the cream/green two-tone break, so the frame
is probably unmeasurable — and **explicitly did not rely on it**. Right to offer
it, right not to rely on it: **it is wrong.**

### The question had to be rebuilt before it could be answered

rev 27 sent five 60×60 boxes. **Every one contains more than one edge**, so the
owner was being asked to guess which edge the estimator had locked onto.
`probe_psf_lines.py` (NEW, read-only) re-runs the **shipped** `find_edges`,
recovers the fitted line each candidate actually used, and **draws that line**.
**A question that cannot be answered unambiguously is the asker's defect.**

### Three defects in `EDGE_NOTES`, which is a hardcoded string

Printed verbatim by `probe_psf_workshop.main()` while the run reports
"candidates 35, accepted 29". **A CLAIM IN PROSE IS NOT A GUARD, INCLUDING WHEN
THE PROSE IS INSIDE THE PROBE** — §10.67 found the identical shape in
`verify.py`'s own comment.

1. **E1, E2, E3 ARE ONE EDGE**, colinear to ~0.1 px.
2. **rms 0.069 and 0.129 exist NOWHERE** among the 35 candidates (real values
   0.073/0.072 and 0.067/0.046). **Eleventh unwatched figure.**
3. **"Best fit first" is wrong** — the frame's best is rms **0.025**, at a ROI
   not in the list at all.

Clustered under a stated infinite-line rule with three asserted controls, the
35 candidates are **14 DISTINCT EDGES**. rev 27 named three.

### The owner's reading

> [stated] **D1, D2, D3, D4, D6, D7, D8, D9 are PHYSICAL STEPS. D5 is not.**

Eight of nine. **He excluded exactly one edge, which hands the probe a NEGATIVE
CONTROL that is his, not mine.**

### The finding: the spread was the 10–90 arm, not mixed classes

With the classes settled the pooled spread went **UP to 86 %** from rev 27's
76 %. **Refuted.** The cause reproduces **on one edge** — across D2's nine
independent windows of *identical data*:

| arm | range on D2 | spread |
|---|---|---|
| 10–90 | 0.584 – 2.203 px | **3.77×** |
| 20–80 | 0.569 – 0.595 px | 4.4 % |
| 25–75 | 0.561 – 0.608 px | 8.1 % |

**On a clean synthetic the 10–90 arm still recovers a known σ to 10.7 %**, so it
is **tail-sensitive on real windows, not broken**, and the sweep was doing its
job by reporting it.

### THE RESULT

**σ = 0.5594 ± 0.0280 px, FWHM 1.317 px.** Core arms only, n = 32, four
independent confirmed steps agreeing to **12.4 %**: D2 0.5806 ± 0.0113 (n=18),
D3 0.5301 ± 0.0121, D6 0.5405 ± 0.0202, D7 0.5136 ± 0.0016.

- **D9 EXCLUDED AND PRICED at +0.176 px / 32 %.** The reason is not that it
  disagrees: it is **the only candidate whose edge carries the bulb string**, so
  the far side of its step is not a uniform surface — the one thing an ESF
  requires. n = 1.
- **D1, D4, D8 unmeasurable and NAMED** (too few ESF bins, or the monotone test
  rejected them). D1 is the frame's best-fitting edge and misses by 0.0002.

### The negative control failed, then passed, and the premise was the defect

Pooled, D5 read **sharper** than the steps (0.660 vs 0.736) — **FAIL**. On the
core arms it reads **18.0 % SOFTER** (0.6603 ± 0.0167 vs 0.5594), with internal
scatter far below the effect. **The 10–90 contamination was in the control too.
Premise fixed, band NOT widened.** Fourth instance. `N2` — rev 26's fixed-axis
method on the same edges — still reads **1.59× larger**, so that correction is
intact.

---

## 3. §10.81 — the owner reads the counter top as CLEAN, and a SECOND tautology

> [stated] **`ref_rear34.jpg` shows the counter top as CLEAN VARNISHED
> PLYWOOD.**

That **contradicts** a shipped settled-dust film at **mean coverage 0.548**,
recomputed by a **live assert** every build, which §10.70 identified as
**57.1/52.6/36.6 % of the `COUNTERTAN` pedestal**. §10.76 had it merely
UNSUPPORTED; it is now contradicted by an owner reading of the only frame that
shows the surface.

**The pointer boxes were checked before they were sent**: raw luma spread 27.7 %
/ 15.0 %, but **0.0 % / 0.6 % once a least-squares PLANE is removed**, against a
positive control — §10.76's own proven-straddling founding patch — at **32.4 %**.
The raw figure was the top's own illumination gradient.

**TAUTOLOGY 2, NEW.** The founding patch's own E-free ratio × `CREAM`
reproduces `_UP_MEASURED` **exactly**. It must — `_UP_MEASURED` was derived from
that patch through the von-Kries gain — so **the founding patch can never
disagree with the assert it founded.** Any future test must use §10.76's
band-following CLEAN sample. Found because **my own control failed and I checked
its premise first** (fifth instance): the premise was mine, and §10.76's
published triple is the CLEAN sample's, reproducing to three decimals.

**What clean predicts:** f = 0 moves every channel TOWARD the photograph, worst
channel **42.5 % → 34.0 %** — real corroboration. **But f = 0 alone does not
reconcile it**: clean `COUNTERTAN` is still **34.0 % short in B**, and the
implied top albedo (0.6519, 0.5577, 0.4637) differs from `COUNTERTAN` almost
entirely in **BLUE**. The best-matching arm is **dusty `COUNTERCREAM` at 8.0 %**
— **the wrong material for the surface** (§10.71) — and **§10.60 rules the
up-facing/vertical pair INADMISSIBLE, so none of it binds either way.**

**NOTHING TUNED.** `W_DUST_FAC_UP` 0.7313, `COUNTERTAN`, `COUNTERCREAM`,
`CREAM` all UNCHANGED.

---

## 4. Things you must not silently undo

`HANDOFF_rev27.md` §4, and rev 26's §4, rev 25's §4, rev 24's §4, rev 23's §4,
rev 22's §3, rev 21's §4, rev 20's §4, rev 19's §4 and rev 18's §4 **all still
stand in full.** Added by rev 28:

- **`EDGE_NOTES` in `probe_psf_workshop.py` is PROSE and two of its five rms
  figures are fiction.** Do not quote it. `probe_psf_lines.py` computes the
  real list.
- **The five rev-27 ROIs are THREE edges, not five.** E1/E2/E3 are one.
- **σ = 0.5594 ± 0.0280 px is on the CORE ARMS ONLY.** Do not pool the 10–90
  arm back in; it is tail-contaminated on real windows and it broke a control.
- **D9's exclusion is priced at +0.176 px / 32 % and must stay priced.**
- **The founding patch for `_UP_MEASURED` can never disagree with its own
  assert.** Use the CLEAN band-following sample.
- **`W_DUST_FAC_UP` is CONTRADICTED, not merely unsupported — and setting it to
  0 blind is still barred.** Clean `COUNTERTAN` does not match the photograph
  either, and f = 0 would silently discard §10.70's pedestal work.

---

## 5. Still open

- **THE FRONT OVER-RIDER (§10.75).** The PSF blocker is **CLEARED**. What
  remains: **a scale on the nose/bumper plane, or a proof that none is
  admissible**, then size and build, every number tagged workshop-stage.
  **NOT ATTEMPTED IN REV 28 — named, not hidden.** This moves geometry and
  invalidates `rev25_hero34f.png`. Strike ±2.145 / ±2.140 either way (§10.72).
- **The residual 6.6/6.6/8.5 % pedestal — the scene→top bounce.** The only
  named candidate left. **NOT STARTED IN REV 28.** Remove `gal_warmer` /
  `gal_caddy0` / `gal_caddy1` and **re-derive the mask** (a visibility flag is
  barred by §10.56). The harness has **no cyclorama** (§10.78) — state that, do
  not silently fix it.
- **§10.81 is the top item for rev 29**, and the deadlock is sharper than
  §10.76's: not "is the coverage right" but "**the coverage is contradicted and
  this frame cannot supply the replacement**".
- **THE FRONT BUMPER FACE IS UNMEASURED** — both catalogue values struck.
- **`CREAM`** — needs a same-light, same-CLASS, three-channel reference. Does
  not exist in the three photographs.
- **THE ABSOLUTE ROOF HEIGHT.** **THE OFF FLANK**, 804.9 mm.
- The cab door's true top edge — authored; unmeasurable (§10.73).
- `GAL_SKY` is a dead lever. `PLATE_W = 0.3300` has no provenance.
  `probe_rev16.py:90` prints `xa` vs `xa`.
- **D1/D4/D8 could not be measured** and D1 is the frame's best-fitting edge —
  it misses the monotone threshold by **0.0002**. Worth one look, and worth
  resisting the urge to widen the threshold to get it.

---

## 6. Process rules earned in rev 28

- **A QUESTION THAT CANNOT BE ANSWERED UNAMBIGUOUSLY IS THE ASKER'S DEFECT.**
  rev 27 sent boxes; every box held more than one edge. Draw the thing you are
  asking about, not the region containing it.
- **A THRESHOLD SWEEP THAT DISAGREES IS REPORTING SOMETHING — READ IT BEFORE
  BLAMING THE DATA.** The 76 % spread was one arm's tail sensitivity, and it
  was diagnosable on a single edge.
- **VALIDATE THE ARM YOU ACTUALLY USE.** A positive control on the pooled
  estimator would have validated something the result does not rest on.
- **A DERIVED CONSTANT'S OWN SOURCE PATCH CAN NEVER FALSIFY IT.** Check whether
  the test data is upstream of the thing being tested.
- **PRICE AN EXCLUSION.** D9 is dropped for a stated physical reason and the
  cost is printed on every run.
- **CHECK THE CONTROL'S OWN PREMISE** — fifth instance, and it is what found
  Tautology 2.
- **CHECK THAT A FOLDER IS CONNECTED BEFORE PLANNING THE REVISION.**

---

## 7. Deliverables

`tacombi_rev28_incremental.bundle` (applies onto the rev-27 tip `598e523`),
`tacombi_rev28_tree.tar.gz`, `SPEC_rev28.md`, `STATE_rev28.md`,
`HANDOFF_rev28.md`, `NEXT_CONTEXT_PROMPT_rev29.md`, plus the two question
figures `rev28_q1_countertop.png` and `rev28_q2_psf_lines.png`.

**`rev25_hero34f.png` still photographs the current mesh and the current
artwork.** Nothing moved in rev 26, rev 27 or rev 28. Do not re-shoot.
