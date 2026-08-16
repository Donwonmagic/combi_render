# HANDOFF rev 30 — the front over-rider BAR is measured and BUILT

**143 commits, clean tree. Both guards 0 fail / 0 warn at BOTH subdivision
levels. GEOMETRY MOVED — the first time since rev 23.**

---

## 1. What rev 30 changed

| file | change |
|---|---|
| `t1_detail.py` | **NEW** `overrider_bar()` + its constants. SPEC 10.83. |
| `build.py` | one line: `A(D.overrider_bar(), "bumpercream")`, workshop-stage |
| `verify.py` | **NEW** 10.83 row (frozen derivation, three arms) + **two** `_RETIRED_VALUES` rows |
| `SPEC.md` | **NEW** §10.83; §10.75's centreline claim marked **REFUTED** |
| `probe_orb_blade.py` | **NEW**, read-only |
| `probe_orb_hoop.py` | **NEW**, read-only |
| `mark_rev30_q.py` | **NEW**, read-only; `rev30_q_overrider.png` |

**NO ARTWORK MOVED.** `CREAM`, `COUNTERTAN`, `COUNTERCREAM`, `RED`, the rake,
the roof, all three textures and every shader constant are UNCHANGED. The only
mesh change is one new object.

Counts: **126 → 127 objects** at `materials:`, **185 → 186 meshes**. Every
other guard figure is identical to rev 23's.

---

## 2. The measurement, in one page

**The blocker was never occlusion and never the threshold.** It was that rev 26
measured the tube at `u 248–272`, where there is no ruler, because that is
where box A had been drawn.

- **Occlusion REFUTED by geometry.** Trolley rail top edge fits
  `v = −0.3053 u + 817.675` to **rms 0.289 px over 65 columns** and lies
  **6.6–61.3 px BELOW** the blade's lower boundary in every clean column of the
  tube's run. The owner was NOT asked a question measurement had answered.
- **rev 29's scale-free ratio REFUTED as a fix.** Seven thresholds: tube
  ±16.8 %, blade ±9.0 %, **ratio ±12.8 %** — between them. C5 FAIL, reported.
- **The frame's own yardstick:** the rail's edge is **1.76 px = 1.23× the ideal
  step** predicted by §10.80's σ = 0.5594. **An independent corroboration of
  rev 28's PSF from a different edge class**, and it was not sought.
- **The tube runs the whole way across the nose.** At `u 385–460` it passes
  **directly beneath the headlamp aperture** — same station, measured
  vertically, so REF §9's lateral 2:1 warning does not bite. There its
  thickness holds to **±5.5 % over 76 columns** against rev 26's ±19 %.

### The owner's answers

| | question | answer | effect |
|---|---|---|---|
| Q1 | where does the tube end? | **CAN'T TELL** | barred taking my own lean; bracket 9.86–14.98 px |
| Q2 | where is the aperture's lower rim? | **the THIN DARK LINE** | the ruler is 71.11 px, not REF §9's 75.6 |

### How Q1 was closed WITHOUT an answer

The tube **turns down and back in a rounded hoop end at `u ≈ 468–490` that SPEC
has never recorded.** Through the bend both ends of a horizontal chord are
LATERAL silhouettes. For any axis slope, `W_h = D·√(1+s²) ≥ D`, so **every
chord is an upper bound on D** — no fit, no derivative, no free parameter.

**Smallest chord over 15 rows: 10.38 px → D ≤ 10.38 px.**
arm 1 (9.86) **ADMISSIBLE**; arm 2 (14.98) **EXCLUDED, 44 % over**.

Closed by refuting one arm, not by choosing between them. **NOT CLAIMED:** that
the dark band IS a cast shadow. Still open; irrelevant to the diameter.

---

## 3. Things you must NOT silently undo

rev 29's §4 and every §4 back to rev 18 still stand in full, plus:

1. **`BAR_DIA` and `BAR_RISE` are written as `ratio × APERTURE_M`, never as
   bare numbers.** The anchor is a **CATALOGUE** 0.180 m — SPEC 10.72's struck
   class — and writing the products as literals would hide that.
2. **The 10.83 verify row's reference is FROZEN IN `verify.py`, not read from
   `t1_detail`.** The first version was a tautology and read 0 fail on a 3 mm
   source change. Do not "simplify" it back.
3. **Its sampling window is `x > 2.100`, not `x > 2.132`.** The tighter window
   never sees the blade's top at all (`BUMP_PROFILE` tops out at outward
   0.000). Window was the defect; the band is untouched at ±1.5 mm.
4. **§10.75's "post at the vehicle's centreline" is REFUTED and marked.** Do
   not restore it and do not build the post at the centreline.
5. **The bar is WORKSHOP-STAGE.** One line in `build.py` deletes it if an
   in-service frame of the nose ever appears.
6. **The two new `_RETIRED_VALUES` rows** (`14.98`, `post at the vehicle's
   centreline`) were both watched FIRE. Do not relax them; a re-expressed
   retired value needs ANOTHER ROW.

---

## 4. Still open

- **THE OVER-RIDER POST.** Blocked on a LATERAL position, which REF §9 bars on
  this panel. Its columns are 357–374 against the V apex at 311.5. The only
  bracket available is "between the centreline and the near headlamp", which is
  not a measurement.
- **A HERO IS OWED TWICE OVER** — shading moved in rev 29, geometry in rev 30.
  `rev25_hero34f.png` photographs neither.
- **§10.70's percentages must be RE-RUN** on the post-retirement build before
  being quoted. Harness has no cyclorama (§10.78) — state it, do not fix it.
- **§10.82's unasked surfaces** — bumper top, rim barrels, hub caps.
- `COUNTERTAN` still **34.0 % short in B**. The front bumper FACE. `CREAM`. The
  absolute roof height. The off flank, 804.9 mm. `GAL_SKY` dead lever.
  `PLATE_W = 0.3300` no provenance. `probe_rev16.py:90` prints `xa` vs `xa`.

---

## 5. Rules earned or re-earned in rev 30

- **A GUARD WHOSE REFERENCE IS THE THING IT GUARDS CAN ONLY CATCH DELETION.**
  Third instance of a tautology inside a guard (§10.81, rev 24, now this).
  **Freeze the reference.**
- **A FLATNESS FIGURE YOU DO NOT GATE ON IS NOT A CONTROL.** I printed a null
  patch's sd and did not test it. Two patches wrong before one was right.
- **MEASURE SOMEWHERE ELSE BEFORE YOU BUILD A THIRD ESTIMATOR.** Two estimators
  died in `probe_orb_hoop.py`; the answer was a BOUND that needed neither.
- **A "CAN'T TELL" IS A RESULT AND IT BINDS.** It barred my lean, and the lean
  only survived because an independent bound killed the alternative — which is
  a different thing from having been followed.
- **ASK ONLY WHAT MEASUREMENT CANNOT ANSWER.** The brief's first task — which
  columns show the true blade bottom — was answered by a line fit, so it was
  not asked.
