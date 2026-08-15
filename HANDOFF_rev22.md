# HANDOFF rev 22

**Final state: 99 commits, clean tree. Guards 0 fail / 0 WARN at BOTH levels.**
Read `NEXT_CONTEXT_PROMPT_rev23.md` for the restore recipe and the work list.

---

## 1. What rev 22 did

Four items. **One shipped a deliverable, one implemented the owner's decision,
and two had their own briefs refuted on measurement.**

### Item 1 — THE HERO, first since rev 16
`rev22_hero34f.png`, **4800x3200, SUB=2, 56 samples, 20 strips, pad 48 px**.
**Worst seam z = 1.91** against a threshold of 4; rev 16 shipped 1.89, so seam
quality is unchanged at the same resolution. All 19 seams OK; interior
row-delta mean 0.5916 sd 0.4781 DN. `post.py` was run **ONCE** on the stitched
frame -- `bloom=0.00`, `backdrop=headroom`, both of which are the owner's rev-15
decisions.

This is the first photograph of the **rev-18 rear-arch fix**, **rev 17's hubcap
rings** and **rev 19's cream fade-mottle map**. Strip times 92-445 s.

### Item 2 — `H_ROOF` RETIRED (SPEC 10.59). The owner's call, after five revisions.
**SAY IT THIS WAY: the +23 mm warn is gone because THE TEST WAS WITHDRAWN, not
because the model improved. THE MESH DID NOT MOVE.** Every other guard figure
is identical.

`H_ROOF = 1.960` had no admissible derivation left: REF sec.1 derived it from
the ground line 10.11 bans (~70 mm common-mode), 10.34 found the hub chain
carries the same disease at ~29 mm, and 1.960's only ground-line-free support
-- `LOFT_GROUND` sec.1.2's 1.9621 -- was withdrawn by 10.34 *without noting it
was the last one* (10.48 found that).

**It was NOT re-valued to the mesh probe.** The owner rejected that and was
right: a guard set to the model's own reading compares the model to itself and
can never fail, and it clears a warn by tuning.

The probe survives as a **LABELLED REGRESSION CATCHER, band +-5 mm**, exactly as
10.47 did for `STATE.md`'s height row. **Baseline WATCHED PRINT at both levels
before it was written into the file: SUB=1 -> 1.9835, SUB=2 -> 1.9833.**

**FALSIFIED TWO WAYS after repair, not merely re-run:**
| arm | perturbation | result |
|---|---|---|
| 1 | baseline displaced -10 mm | **FAIL** `MOVED +10.0 mm` |
| 2 | `CR_ALL` crown raised **+8.0 mm IN THE GEOMETRY** | **FAIL** `MOVED +7.9 mm` |

Arm 2 proves the row reads the **MESH**, which the old arch guard never did.
The row FAILS past the band rather than warning. `audit.py`'s prose was
corrected in the same commit so it cannot contradict the build.

**The real vehicle's absolute roof height is now OPEN and UNMEASURED.**

### Item 3 — `COUNTERTAN`'s HUE: TARGET REFUTED (SPEC 10.60). Constant UNCHANGED.
The cited **28.4 deg / 0.333 is an OBSERVED PIXEL**; `COUNTERTAN` is an
**ALBEDO**. That is the 10.21 trap. Tested before acting, per 10.58.

| quantity | hue | sat |
|---|---|---|
| OBSERVED tan-top pixel (n=162, 0.00 % clipped) | **32.3** | 0.364 |
| ALBEDO via fascia arm | **39.3** | 0.225 |
| ALBEDO via cab-roof arm | **41.7** | 0.289 |
| **BUILT `COUNTERTAN`** | **42.3** | **0.254** |

Claimed error ~14 deg; real disagreement **at most ~3 deg**, saturation already
inside the bracket. Nothing moves on that while the LEVEL is unresolved.

**Two new findings from controls never previously run:**
- **(a) The founding crop straddles two materials** -- rows 411-415 include the
  shadowed transition (54 code values darker than row 413) and run into the
  **brass nosing** (rows 416-419, sat 0.669, r/g 2.356). The counter top is only
  ~3 px tall because the camera is at roof height. **Thirteenth instance**, and
  it is in SPEC's own founding measurement. Clean rows are 412-414.
- **(b) The cab-roof reference is NOT under the same light as the fascia:**
  observed roof/fascia `(0.5873,0.6345,0.7464)` against the albedo-only
  expectation `(0.8397,0.8822,0.8752)` leaves a residual illuminant at
  **B/R 1.219 -- 22 % bluer**. Under 10.21 that arm is **inadmissible**, and the
  LEVEL bracket's upper end (G 0.569) rests on it. **RECORDED, NOT APPLIED** --
  the fascia arm has its own orientation weakness, so neither is clean.

*Process note: my FIRST control failed, and the failure was mine -- I referenced
the fascia to `CREAM` when the model assigns it `COUNTERCREAM`. Checking the
control itself is what caught it.*

### Item 4 — GROUNDED, NOT ARMED (SPEC 10.61). Two carried figures corrected.
`probe_shutlines.py`, READ-ONLY. 10.45's "five crossings, 1209 mm, one on the
show flank" had been carried four revisions without being reproduced.

**MEASURED: SIX crossings, 1065.1 mm, and TWO on the show flank.**
`gap_door+1 x bay0` 118.8 mm (known) and `gap_door+1 x door_vent` **11.8 mm**,
which no prior revision named. `gap_cargo x bay0` and `x bay2` are **402.0 mm
each** -- identical, which normally means a bug; it is not, because both cargo
verticals cross a bay over the **full aperture height** and
`Z_HEAD - Z_SILL = 403.0 mm`.

**THE ARCH HALF IS MOSTLY NOT APPLICABLE.** Four of six shut-line x arch pairs
cannot be tested (the outline does not span the station; the probe returns
**None**, never an endpoint). The two that can are exactly the pair the existing
assert covers, at **+23.6 mm clear**. **The gap in `t1_shell:451` is the
APERTURES, not the arches.**

**`CARGO_GAP`: both carried numbers are true and are different statistics.**
20 of 28 points (**71.4 %**) lie on the corner arcs; the corner arcs are
**5.2 % of the outline BY LENGTH**, reproducing 10.45 exactly. "ALL" is the
imprecise word. Sharper: **71.4 % of the samples are spent on 5.2 % of the
outline, leaving 94.8 % of the length with 8 samples.**

---

## 2. Guards -- ACTUAL output, both levels, after everything

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 0 warn** | **0 fail, 0 warn** |
| roof crown @ rear axle | **1.9835** (baseline 1.9835, -0.0 mm) | **1.9833** (-0.2 mm) |
| rear arch lip / gap | 0.3722 -> **39.7 mm** | same |
| front arch (control) | 0.3732 -> **40.7 mm** | same |
| rake | **17.75 mm/m (locked 17.75)** | same |
| dome deficit / rear overhang | +0 / **0.7730** | same |
| dims | **L=4.065 W=1.750** | same |
| cut roof hole | **68052v** | **252123v** |
| objects at `materials:` | **126** | **126** |
| meshes / materials / const-rough | **185 / 42 / 5** | same |
| non-manifold | **0** | **0** |
| bay widths | **0.516 0.515 0.516** | same |

Every figure except the roof row is identical to rev 18/19/20/21.

---

## 3. Things you must not silently undo
rev 21's sec.4, rev 20's sec.4, rev 19's sec.4 and rev 18's sec.4 **all still
stand in full**, plus:
- **`H_ROOF` must not be re-added to `SPEC`** and the regression band must never
  be widened. If the row trips, that is the guard working.
- **`COUNTERTAN` must not be moved onto an OBSERVED pixel value.** 10.60.
- The cab-roof arm of `COUNTERTAN`'s bracket is **inadmissible** -- do not quote
  the G 0.569 upper end as if it were supported.
- `probe_shutlines.py` is READ-ONLY grounding; it is not a guard.

---

## 4. Still open
- **`CREAM`** -- unchanged at (206,208,200), and the reason is understood
  (10.57's +31 sd invariant). Needs a same-light, same-CLASS, three-channel
  reference or an established neutral transform. **Neither exists in the three
  photographs.** May have to be accepted as bracketed and LABELLED.
- **The absolute roof height** -- NEW this revision. 1.960 is retired and
  nothing replaced it.
- **`COUNTERTAN`'s ~69 % pedestal** -- UNIDENTIFIED. Best lead is still the
  occlusion hypothesis; needs an object-index pass. **New input:** the level
  bracket's upper arm is inadmissible (10.60b).
- **Item 4's assert, unarmed** -- six pairs, 1065.1 mm. Expect it to FAIL; fix
  the geometry, never the threshold.
- `folk_gen.py`'s banned flat px/m at `:1884` and four stale constants.
- SPEC 10.3's table still lists the RETIRED red (196,106,36) as "locked";
  10.9's table still lists the retired rake 0.0330 and `Z_BELT0`/`V_APEX0`
  derived from it. `PLATE_W = 0.3300` still has no provenance.
- `SPEC.md:1983` uses **N1** -- the crop the owner REFUTED -- as an arm of route
  A's clipping control. The conclusion survives on N2/N3 alone (12.1 % clipped
  reads MORE saturated than 0.00 %), but the text should drop N1.
- Tail-lamp material slot; `Senor` at 0.504 of its 0.782 ceiling; `SCR` +80 mm
  aft; `probe_rev16.py`'s `xa` vs `xa`; the ~12 unverified image URLs.

---

## 5. The one photograph that would move the most
Unchanged, and now it would close **two** things rather than one: **a head-on
rear (or front) elevation from roof height or above, with the counter and the
lids clear of the section.** It is the only realistic route to closing `CREAM`
**and** it is now the only route to an absolute roof height.
