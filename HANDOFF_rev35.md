# HANDOFF rev 35

**NO GEOMETRY MOVED.** The last geometry change is still rev 30's. Every build
file is BYTE-UNCHANGED from rev 34.

## 1. What rev 35 did

1. **Graded the transverse-VP-by-harmonic-conjugate route BEFORE spending a
   question on it**, and graded EVERY column it consumes.
   `probe_rev35_harmonic.py`, **18 controls, 6 FAILED.**
2. **Retired it — on a MISSING FEATURE, not on precision.** The construction
   needs three columns on the headlamp line and only two exist. §10.86 supplied
   the third from the V-swage apex, 0.625 m below that line. Sweeping the VP
   across its whole admissible range leaves the midpoint free over **67.8 px**
   and `t` over **0.8483 half-widths — 17×** the level.
3. **Found `u_lamp_far = 236` has NO RECORDED DERIVATION anywhere in the tree.**
   §10.86 prose and `HANDOFF_rev32.md` only. Same class as `u 228`.
4. **ASKED NO QUESTION, and said why in arithmetic:** the far lamp does not
   enter the surviving result, so a reading of it closes nothing.
5. **Published a replacement, then REFUTED IT with its own adversarial audit
   and struck the numbers.** The SIGN survives; the MAGNITUDES are withdrawn.
6. **Earned one rule: CHECKING THE PRECONDITION YOU WERE WARNED ABOUT IS NOT
   CHECKING THE PRECONDITIONS.**

## 2. Files added — ALL READ-ONLY, none touched by the build

| file | what |
|---|---|
| `probe_rev35_harmonic.py` | the grader. 18 controls, 6 FAILED. REFUSES TO PRINT A RULING if H1/H2 are down |
| `mark_rev35_bound.py` | the result figure. REFUSES TO WRITE if C1–C4 fail |
| `rev35_bound.png` | the figure. **NOT A QUESTION** — a fifth mark class, MEASURED COLUMNS + ONE DERIVED MEAN |
| `STATE_rev35.md` | copy of `STATE.md` regenerated on the clean rev-35 tree |
| `SPEC.md` §10.89 | six parts |

## 3. The controls, as they print on a fresh clone

`probe_rev35_harmonic.py` — **18 checked, 6 FAILED: H3, H5, G1, G3, B2, B3.**
**ALL SIX ARE THE RESULT.** H1, H2, H4, G2, G4, G5, G6, B1, B4, B5, N1, N2 pass.
**DO NOT "FIX" ANY OF THEM.** H4's PASS is itself recorded as the defect of the
revision (§10.89.3): it checks the precondition rev 34 was warned about and not
the one that was actually violated.

## 4. Things you must not silently undo

- **§10.89's withdrawal of `t ≥ 0.1464` and `t ≥ 0.0595`.** They are struck, not
  re-scoped. Do not reinstate them with a caveat.
- **`u_lamp_far = 236` is LEFT IN `probe_rev35_harmonic.py` with an EMPTY
  provenance string**, which is what makes H5 fail. That empty string is the
  record. Do not fill it in from §10.86's prose — that prose is the thing with
  no derivation.
- **`probe_clean_top.py` and `probe_dust_anchor.py` are STILL deliberately
  failing.** rev 35 did not reach them. They need rewriting, not fixing.
- Everything `HANDOFF_rev34.md` §7 and rev 33's §6 through rev 18's §4 protect.

## 5. What rev 35 did NOT do

- **Work-list item 2** (rewrite the two degenerate probes) — not reached.
- **Item 3** (§10.70's arms, the scene→top bounce) — not reached.
- Items 4 and 5 — not reached.
- **No hero was shot.** `rev30_hero34f.png` is still the current hero and is
  still proved by content. A 900×600 `T1_SAMP=24` preview was rendered for the
  figure's right-hand panel and took **79.3 s**, not the brief's 71 s.
