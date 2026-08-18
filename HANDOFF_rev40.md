# HANDOFF rev 40 — the revision that STOPPED its own item 1. No geometry, no artwork, no constant moved.

> **THE STANDARD, in the owner's words.** The final product should be nearly
> indistinguishable from the original. **Any single measurement off is
> unacceptable.** The criterion is PER-MEASUREMENT. And above clinical accuracy:
> *"I want the owner to remember standing in the kombi, in this very picture that
> was provided."* — **that owner is the restaurant's owner. Donald has never
> stood in the bus. Never ask him what the vehicle looks like; ask what a
> PHOTOGRAPH shows, then measure it.**

## 1. What rev 40 did

It was told to move the two-tone break line by **81 ± 7 mm** — *"the item with
the most evidence behind it in the project"*. **It did not, because the 81 mm is
a datum error.** Full account in **SPEC §10.98**, thirteen parts.

`probe_rev39_flank.py` warps the render onto `ref_side.jpg` using two datum lines
transcribed from `flank_compare.py`, whose own comment says they are *"the SAME
cream/red break … the same physical edge, so the two are used as ONE datum and
its height never enters."*

**They are opposite edges of the counter fascia.** They are fitted with
**different estimators in different row windows** — a LUMINANCE gradient over
rows 425–452 on the reference, a REDNESS gradient on the render — and on a
cream / gold-nosing / beige-fascia / red stack those are not the same boundary.
§10.45: *a claim in prose is not a guard*, and this one cost a headline.

## 2. The four things that establish it

* **Which edge, measured** (`probe_rev40_datum.py`, READ-ONLY). Render datum at
  authored **z = 1.1459** against `t1_detail.CNT_ZB` **1.1470** — **1.1 mm**,
  read with `ast` at run time, never a colour gate. Reference datum **0.69 px**
  from the photograph's fascia TOP, **19.46 px** from its bottom.
* **The joint whole-vehicle registration, one line.** rev-39 datum
  **(+19, −1) px = +92 mm**; rev-40 datum **(−1, −4) px = −5 mm.**
* **An independent arm that shares no datum with the warp.** Photographed
  window-sill-to-body-break **102.7 ± 6.6 mm** (n=8, cab door — the only place
  the body's own break is visible) against a built `Z_SILL − Z_BELT_AUTH` of
  **100.0 mm** and REF §3(a)'s own hand figure of 100.0. **−2.7 mm. A break line
  81 mm out of place would show ~81 mm here.**
* **The falsification.** `T1_FC_OLDDATUM=1` restores the rev-39 fit and the new
  two-sided guard **FIRES** at a redness step of **−0.0293** against a bar of
  +0.030.

## 3. What was fixed, and it opens no new estimator

The reference datum now uses the redness gradient **the render side already
used**: `v = -0.03412 u +466.632`, **19.8 px = 92 mm below** the rev-39 line —
one counter fascia. `_assert_same_edge()` is armed **TWO-SIDED on both fits** so
prose can never again stand in for a check.

`probe_rev39_flank.py` had a **second** defect: it searched dx and dy
**sequentially** and they are coupled. Sequential returns **dx −15 px (−71 mm)**
where joint returns **−4 px (−19 mm)**. Now joint, and the per-band row shift is
searched at the global best column shift.

## 4. What that costs the record — all measured through the mismatched datum

| §10.97 published | now |
|---|---|
| horizontal map validated at **−5 mm** | **−19 mm** |
| body **81 ± 7 mm** high against the break | **−5 mm** whole-vehicle |
| **FLAT / ONE RIGID OFFSET** | **no ruling** |
| *"the break line sits ~81 mm too low"* | **refuted at −2.7 mm** |
| `SCR` **+61.9 mm down** | **−33.3 mm, i.e. 33 mm UP** |

`SCR`'s **+76.2 mm forward is unchanged** — the datum is a horizontal line and
never entered x. 61.9 − 33.3 = 95.2 mm, one fascia height: the arithmetic check
on the whole finding. **NOT APPLIED.**

**§10.24 is neither re-opened nor re-closed.** Its own three derivations use the
headlamp and the roundel and do not pass through this datum. What is withdrawn is
only §10.97.6's claim to be a fourth, headlamp-free corroboration of it. §10.24
goes back to exactly where rev 38 left it.

## 5. And the z-ladder no longer rules flat — reported, not tuned

Seven bands cluster at **−5 to −24 mm**, consistent with the joint fit. **Three
return ±193–222 mm, and they are the SAME THREE that DECLINED under the rev-39
datum** — +222 mm being the exact figure §10.97.7 says its gate was written to
kill. Prominence cannot separate them (1.20/1.30/1.55 against a good band's
1.23). **The gate was not retuned.** Derived verdict: spread 415 mm, **NO
RULING**. So **§10.97.5's "FLAT, ONE RIGID OFFSET" was a property of the datum**,
and an acceptance gate calibrated on one datum does not transfer to another.

## 6. HIS ANSWER — region 3, open since rev 19, closed in rev 40

Shown `rev40_q_region3.png` — one ×12 crop, the pale band bracketed, one
sentence — he was asked whether that band is the COUNTER's front face or the
BUS's own painted body.

*[stated, rev 40]* **THE COUNTER'S FRONT FACE.**

It **supersedes rev 12's** *"the cream band below the counter's brass nosing is
the body's own cream belt paint"*, and it **explains rev 19**, where he selected
region 2 and pointedly did not select region 3. His two readings agree with each
other; it is rev 12's line that retires. **The model's routing was already
right** — `plank_counter()` paints that band `countercream`. **Do not re-put
this question.**

It also makes the depth measurable: painted fascia **87.1 mm** built against
**93.6 ± 2.0 mm** (this probe, 5 columns) and **94.3 mm** (`t1_detail`'s own
independent 113-column half-max run) — two photographic readings **0.7 mm**
apart, model **−6.5 mm short**. **NOT APPLIED**; it moves geometry and owes a
hero, and which end moves is a separate question because `CNT_ZB` is REF §3b's
measured 1.082 m AG while `CNT_ZT` is not independently measured.

## 7. My own defects, both recorded

* **A SCOPE ERROR IN THE SECTION DOCUMENTING SCOPE ERRORS (§10.98.13).** The
  first cut published *"the counter fascia is 13.4 mm TOO DEEP"*, comparing the
  model's whole **slab** (107.0 mm) with the photograph's **painted fascia** —
  `CNT_NOSE_F` caps **19.9 mm** of that slab in brass. Corrected to **−6.5 mm,
  opposite sign**. Caught by going back to the build's own constants for a
  quantity I had already decided I understood. **Naming a defect class does not
  immunise you against it.**
* **C3, my positive control, FAILED and is PRICED not loosened.** The gate
  reproduces REF §3(a)'s hand-read cab-door table at +1 px on three columns and
  +2 px on the fourth — one-sided **+1.25 ± 0.43 px = 6 mm**. And pricing it
  paid: it was then available to test the corrected fascia figure against, which
  is what showed it must **not** be applied there either, because the repo's
  cross-check uses a saturation-half-max criterion rather than a hand one.

## 8. Guards and probes — unchanged, because nothing in the build moved

**0 fail / 0 warn at BOTH levels on BOTH tools.** 131 objects, 190 meshes, 42
materials, 5 constant-rough, 0 non-manifold, roof crown 1.9835 / 1.9833, roof
hole 68564v / 252749v, rake 17.75, L=4.065 W=1.750, arch gaps 39.7 / 40.7 mm,
bays 0.516 0.515 0.516, off flank 804.9 mm, over-rider rows NOT APPLICABLE
(stated). **All 28 inherited probes match their published tallies**, read off
each probe's own summary line. `probe_rev40_datum.py` makes it 29.

**No hero is owed** — the mesh has not moved since rev 38 shot
`rev38_hero34f.png`.

## 9. Rev 41's ordered work list

1. **RE-DERIVE `probe_rev39_flank.py`'s BAND ACCEPTANCE GATE**, with the
   criterion stated BEFORE the run. Three bands return ±193–222 mm and the
   inherited gate does not catch them. **Do not widen anything; the gate needs a
   criterion that is not prominence.**
2. **`SCR`: +76.2 mm forward, −33.3 mm up.** Now measured through a checked
   datum. Re-measure once more after any counter change, then apply.
3. **THE COUNTER FASCIA, −6.5 mm.** Decide which end moves — `CNT_ZB` is
   measured, `CNT_ZT` is not. Moves geometry, so it owes a hero.
4. **REPORT 5**, the doors around the wheel well, by a scale-free ratio against
   the arch in `ref_workshop.jpg`. Not `ref_side.jpg` — the door is open 49°.
5. **REPORT 4**, the VW glyph's 52 mm interpenetration.
6. **REPORT 7**, "100% Calidad" — texture-versus-panel FIRST.
7. `probe_clean_top` / `probe_dust_anchor` — rewrite or retire. **EIGHT
   revisions.**
8. **A hero, after anything that moves geometry.** Camera absolutely last.

**REPORT 3 IS NOT CLOSED** — it is back where rev 38 left it, as §10.24, with
its own three headlamp-and-roundel derivations intact and rev 39's fourth one
withdrawn.
