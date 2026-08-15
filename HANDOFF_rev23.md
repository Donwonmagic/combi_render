# HANDOFF rev 23 — item 4 ARMED, the B-pillar had negative width, and the bake frame was stale

> **THE STANDARD, in the owner's words.** *"The final product should be nearly
> indistinguishable from the original. Any single measurement off is
> unacceptable."* The criterion is PER-MEASUREMENT. And above clinical accuracy:
> *"I really want this to give the person the opportunity to feel like they were
> on Playa del Carmen all those years ago."* **That owner is the restaurant's
> owner, not Donald. Donald has never stood in the bus — never ask him what the
> vehicle looks like; ask what a PHOTOGRAPH shows, then measure it.**

---

## 1. How rev 23 opened — CLEAN, fourth revision running

All six rev-22 deliverables were on his Desktop at the exact sizes memory
records (bundle 119 874, tarball 19 719 496, SPEC 223 497, STATE 8 032, HANDOFF
8 666, prompt 20 223), plus `rev22_hero34f.png`. **Twelve files crossed the
bridge in TWO direct `device_stage_files` calls** — no splitting.

Six bundle md5s re-verified against memory, all match, rev 22's included
(`a0f5087f…`). Restore ran 34 → 59 → *(fetch b14)* → 67 → 71 → 75 → 81 → 87 →
93 → 96 → **101 commits, clean tree**, no divergent-branches error.
**12/12 content checks exact** (including `H_ROOF_REGRESSION = 7`, the value rev
22 corrected from its console). **8/8 ancestry.**

Guards on arrival, both levels: **0 fail / 0 warn**, every figure reproduced.

---

## 2. Guards — ACTUAL output, both levels, after everything

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 0 warn** | **0 fail, 0 warn** |
| roof crown @ rear axle | **1.9835** (baseline 1.9835, −0.0 mm) | **1.9833** (−0.2 mm) |
| rear arch lip → gap | 0.3722 → **39.7 mm** | same |
| front arch (control) | 0.3732 → **40.7 mm** | same |
| rake | **17.75 mm/m** (locked 17.75) | same |
| dome deficit / rear overhang | +0 / **0.7730** | same |
| dims | L=4.065 W=1.750 | same |
| **cut roof hole** | **68564v** ← was 68052 | **252749v** ← was 252123 |
| objects at `materials:` | **126** | **126** |
| **shut line × aperture, SHOW** | **0.0 mm** (invariant) | **0.0 mm** |
| **shut line × aperture, OFF** | **804.9 mm** (baseline 804.9, −0.0) | same |
| **`CARGO_GAP` samples** | **154** ← was 28 | same |

Also: **185 meshes**, 42 materials, 5 constant-rough, **0 non-manifold**, three
open apertures on +Y, four shut lines 100 % open, band 1.372–1.775, bay widths
**0.516 0.515 0.516**.

**THE ROOF-HOLE VERTEX COUNT MOVED and it is flagged, not hidden:**
68052 → **68564** and 252123 → **252749**. That is the cab-door and vent
outlines moving plus the denser cargo outline. **Re-baseline against 68564 /
252749 from rev 24 onward.** Every other figure is identical to rev 18–22.

---

## 3. What rev 23 changed

### Item 1 — THE ASSERT IS ARMED (SPEC §10.62)

§10.61's brief said *expect it to FAIL; fix the geometry, not the threshold*.
**A brief is a probe too.** `probe_cross_anatomy.py` (READ-ONLY, new) asked the
three questions §10.61 never asked, and all three change the answer:

| pair | arc | **penetration** | flank |
|---|---|---|---|
| `gap_door × bay0` | 118.8 mm | **5.2 mm** | show + off |
| `gap_door × door_vent` | 11.8 mm | **20.7 mm** | show + off |
| `gap_cargo × bay0` | 402.0 mm | 49.7 mm | off only |
| `gap_cargo × bay2` | 402.0 mm | 139.8 mm | off only |

**Arc length overstates the worst defect by 23×.** **SHOW flank 130.6 mm; OFF
flank 934.6 mm = 87.7 % of the total.**

**The arch assert's rationale was NOT inherited.** It exists because a shut line
crossing an ARCH LIP collapsed the shell 205562 v → 12 v at SUB=2. All six
crossings were live at SUB=2 with **zero non-manifold edges**, so that does not
transfer. The invariant armed instead is **topological** — *an aperture cannot
extend past the boundary of the panel it is cut in* — which needs no
photograph, no scale and no datum.

**Fixed, both on the show flank:**
- **The B-pillar had NEGATIVE width.** Bay 0 straddled the cab door's own
  boundary by 5.2 mm: part of the hole in the door, part in the body, so the
  door could not open. Bay edges are LOCKED and the door's rear x has **no
  provenance anywhere in the repo**, so the DOOR moved — as a whole, so its rear
  edge keeps one straight lean. `DOOR_REAR_DX` is **expressed in terms of
  `BAYS[0][1]`**, never a bare number.
- **The vent wing broke the door's top edge by 20.7 mm.** The owner confirmed
  from `ref_workshop.jpg` that the door glass **is** divided into a vent plus a
  main pane, but could **not** resolve whether the vent reaches the top rail, so
  the door's top-front corner — which IS legible in that frame — was left alone
  and the vent's top edge dropped.

**`B_PILLAR = 0.0120` and `VENT_TOP_DROP = 0.0280` are AUTHORED, not measured,
and both true values are OPEN and UNMEASURED.**

**Crossings 6 → 2. Show flank 130.6 → 0.0 mm.**

**FALSIFIED FOUR WAYS**, each through a lever whose default is a proven no-op:

| arm | result |
|---|---|
| `T1_BPILLAR=-0.010` | **FIRES**, `gap_door+1 × bay0 = 223.5 mm` |
| `T1_BPILLAR=0.0` (exact tangency) | passes — correct boundary behaviour |
| `T1_VENTDROP=0` | **FIRES**, `door_vent = 16.7 mm` |
| both, at `DOOR_REAR_DX = 0` | **FIRES**, `12.7` / `120.8 mm` |

That last arm reproduces rev 22's geometry exactly and lands within **1–2 mm**
of its 11.8 / 118.8 — the sampling step.

**Two of my own errors, caught by controls, recorded rather than smoothed over:**
- My first negative control asserted *"an outline is not inside ITSELF"*. It is
  ill-posed — every sample then lies exactly ON the boundary, where a
  ray-crossing test is undefined — and it fired immediately. **The failure was in
  the control.** Replaced with a disjoint box.
- My first falsification env looked like a **2.6× disagreement** between two
  implementations of one measurement. It was not: `DOOR_REAR_DX` is *derived*,
  so `B_PILLAR = -0.0173` moved the door 12 mm further aft than rev 22. The
  value that reproduces rev 22 is **`B_PILLAR = -0.0053` — the negative pillar
  width itself**, an independent confirmation of the 5.2 mm defect. A phantom
  was nearly reported.

**THE OFF FLANK IS NOT ARMED AT ZERO, AND THAT IS THE RESULT.** 804.9 mm across
`gap_cargo × bay0/bay2`. **`SPEC.md:92` grades that whole flank "E (never
photographed)"**, and the two colliding features are BOTH E and contradict each
other — the off-side windows are a mirror of the show side (`side_cutters` loops
`s in (1,-1)`) while the cargo door was placed independently. Shown the workshop
frame's sightlines with every box printed, **the owner answered "cannot tell
from this crop"**. So it is a **LABELLED regression catcher** at a watched
baseline (**804.9 mm, band ±10 mm**): a pass means *the off flank has not
moved*, **NOT** *the off flank is right*.

**`CARGO_GAP` densified 28 → 154 samples**, straight runs **8 → 134**. Pure
no-op on the shape — **signed area asserted equal**, a control not a comment.

### Items 3 and 4 — the bake frame, and four retired "locked" values (§10.63, §10.64)

**`folk_gen.py` re-typed four constants and all four were stale:** `X_TAIL`
**235 mm**, `RAKE_DZDX` **15.25 mm/m**, `RAKE_Z0` and `Z_BELT0` **11.4 mm**
each. Now parsed with `ast` (rev 14's `SCR` pattern), **raising rather than
falling back**; `X_TAIL` reconstructed from its definition because it is derived
in `t1_core` and is not a literal there.

**The banned flat px/m at `:1884` is gone — and it was HARMLESS where it stood.**
It set a sampling interval, never converted a position. Renamed `STEP_M`. Stated
precisely rather than claimed as a bigger fix than it was.

**NOT re-baked, deliberately.** `build.py` never calls `folk_gen`; `tex/*.png`
are committed pre-baked artefacts, so nothing in the current build changes. A
re-bake moves every painted element and §10.10 makes that a MEASURED operation.

**SPEC hygiene, all four confirmed by hand before acting:** §10.3 published the
RETIRED red **and** `W_ART = 0.30` (**3.3× off the live value for thirteen
revisions**) as "locked"; §10.9 published the RETIRED rake and the
`Z_BELT0`/`V_APEX0` derived from it; `SPEC.md:1983` used **N1**, the crop the
owner refuted, as route A's clipping-control arm **nineteen lines after §10.57
dropped it** — removed, conclusion unchanged on N2/N3.

**THREE CITATION DEFECTS.** §10.61 corrects a "five crossings / 1209 mm" figure
**§10.45's body never contained** (it lives in `HANDOFF_rev18.md:208`); §10.59
credits §10.48 with a withdrawal it never made (`verify.py:66` repeats it); and
§10.45 cites the rake lock to §10.9, **whose own table locks the retired
0.0330**. *A carried-forward figure is a claim too* — now extended to the
citation.

**AND TWO CLAIMS IN REV 23'S OWN BRIEF ARE REFUTED**, both verified by hand:
**§10.45–48 retire NO §10.34 claim** (the only reference is `SPEC.md:3267`, a
guard tally), and **§10.29 carries ONE REF-wide correction, not two**
(`:899`, the 100 mm origin error, found by two routes; the others are §10.11's
and §10.34's).

---

## 4. Things rev 24 must not silently undo

Everything in `HANDOFF_rev22.md` §3, rev 21's §4, rev 20's §4, rev 19's §4 and
rev 18's §4 still stands in full. New this revision:

- **Do not tighten the OFF-flank crossing band to zero.** Both members are
  graded E and the owner could not adjudicate. The fix is a photograph.
- **Do not re-add `H_ROOF` to `SPEC`** (rev 22), and **do not widen the
  regression bands** — roof ±5 mm, off-flank crossings ±10 mm.
- **Do not re-type `folk_gen`'s constants back to literals.** The parse raises
  on purpose.
- **Do not re-bake `tex/*.png` casually** — §10.10 makes it a measured operation
  and the committed art was baked in the stale frame.
- `B_PILLAR` and `VENT_TOP_DROP` are AUTHORED. If either is ever measured, say
  so explicitly and re-baseline.

---

## 5. Still open

- **`CREAM`** — unchanged at (206,208,200). Needs a same-light, same-CLASS,
  three-channel reference; **does not exist in the three photographs**.
- **THE ABSOLUTE ROOF HEIGHT** — 1.960 retired, nothing replaced it.
- **THE B-PILLAR'S TRUE WIDTH** — NEW. Authored at 12 mm. `ref_workshop.jpg`
  shows it is visibly wider than the pillars between the three side windows, but
  that frame is a three-quarter view with no admissible px/m on the door plane,
  so no number was taken.
- **THE VENT WING'S TRUE TOP EDGE** — NEW. Dropped 28 mm by authorship.
- **THE OFF FLANK** — cargo doors vs three mirrored windows, both E, mutually
  contradictory, 804.9 mm of crossing.
- **`COUNTERTAN`'s ~69 % pedestal** — UNIDENTIFIED; occlusion hypothesis needs
  an object-index pass, NOT the 48-sample per-pixel test (seed noise 21.7 %).
- **The committed artwork was baked in the stale frame**; `folk_gen.DOOR_X0` is
  now 17.3 mm stale from §10.62 and is named, not quietly fixed.
- `PLATE_W = 0.3300` still has no provenance. `probe_rev16.py:90` still prints
  `xa` against `xa`. **§0.2 has gained no entry since rev 4/rev 8**, so
  `verify`'s self-arming retired-material guard covers none of §10's
  retirements.
- Tail-lamp material slot; `Senor` at 0.504 of its 0.782 ceiling; `SCR` +80 mm.
- **`probe_shutlines.py` can no longer run when the show-flank assert fires** —
  correct behaviour for a structural assert, but worth knowing.

---

## 6. Ordered work list for rev 24

1. **`COUNTERTAN`'s pedestal** — the occlusion hypothesis via an object-index
   pass. Fourth revision on the list. NOT the 48-sample per-pixel test.
2. **§0.2's retirement list** — add §10's retirements so `verify`'s self-arming
   guard actually covers them. Cheap, structural, and it is the mechanism that
   would have caught §10.64's four stale "locked" rows automatically.
3. `folk_gen.DOOR_X0` — parse `t1_shell`'s constant graph properly, or state why
   not. Then decide, with measurement, whether a re-bake is owed under §10.10.
4. The tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
5. **A hero at 4800×3200** — the geometry moved this revision, so
   `rev22_hero34f.png` no longer photographs the current mesh.
6. Camera absolutely last.

---

## 7. The commit count and the content figures

Written LAST, after the final commit, every figure read off a fresh-clone
verification run rather than typed from memory. **This has gone wrong in ELEVEN
consecutive revisions during handoff assembly.**

**Note on commit 102:** its message names only §10.62, but `git add -A` swept
the §10.63/§10.64 work into the same commit. **Stated rather than amended** —
rev 14 learned not to `--amend` a commit whose `STATE.md` predates the amend.
The change log and this handoff carry both.

Content checks for rev 24 and the final count are in
`NEXT_CONTEXT_PROMPT_rev24.md` §1, read off the verification console.
