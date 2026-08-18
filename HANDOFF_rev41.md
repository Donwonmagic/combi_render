# HANDOFF rev 41

**No geometry moved. No artwork moved. No constant moved.** Guards 0 fail /
0 warn at both levels on both tools; 131 objects, 190 meshes, 42 materials,
5 constant-rough, 0 non-manifold. All 29 inherited probes match their published
tallies, read off each probe's own summary line.

Rev 41 is a **measurement revision that closed one item by answering it and one
item by refusing it**, and both answers are negative results.

---

## 1. Arrival

* Folder already in `connectedFolders` on the first `get_device_info` — **tenth
  revision running**. Step 0 kept anyway.
* **AN ABSENCE HAS A TIMESTAMP TOO, AND I QUOTED MINE AS THOUGH IT DID NOT.**
  My first recursive listing ran at **12:04:01** and returned **zero** files
  matching `rev40`. I reported rev 40 as having delivered nothing. The rev-40
  artefacts were written at **12:08** — four minutes after I looked. Both checks
  were real and both were correct *when they ran*; the error was reporting a
  timestamped absence as a permanent one. Rev 40's own memory says the bridge
  dropped **at delivery**, and the right reading of that was "delivery may be in
  flight", not "delivery never happened". Corrected in the same session, on his
  word to check again.
* `_xfer33/` parts reused for the **eighth** revision, sizes checked
  byte-exactly first: **19,478,840** and **8,519,034**, both exact.
  **36 files in 8 bridge calls, zero transient failures.**
* Restore CLEAN 34 → 59 → *(fetch rev14b)* → 67 … → 211 → **215**.
  **28/28 content checks exact, 19/19 ancestry, 3/3 texture md5s, 29 probes,
  hero correctly absent.** The rev-40 bundle's md5 is
  `8ff41105a1e1c17d2ac92c7767071d15`, matching its recorded value — independent
  confirmation the file that appeared at 12:08 is the one rev 40 cut.
* `STATE.md` provenance checked BEFORE trusting it: `working tree | clean`,
  commit `69fe7d2` = HEAD.
* **The `MIGRATION_APPENDIX_rev32.md` phantom is still a phantom** — 0 files in
  the tree, **0 paths in the whole git history across every ref**. Fifth check.

## 2. Item 1 — the gate cannot be re-derived, and there is now a number saying why

SPEC **10.99**, seven parts. `probe_rev41_gate.py`, READ-ONLY.

**Criterion 1 was stated before the run and refuted by it.** G3 — two-sided
half-prominence descent — admits **10 of 10** bands including all three bad ones.
Their curves *do* descend on both sides. §10.97.7's ramp-on-a-bound mechanism
does not survive the corrected datum.

**The negative control is the finding.** Displace the reference 120–360 px, every
offset ≥ 2 × `SEARCH`, so no true `dy` is reachable inside the window by
construction: **the inherited gate answers on 181 of 260 = 70 %.** Null
prominences reach **2.13–3.11×** against an inherited bar of **1.08×**, and
**nine of ten bands' real prominences sit below their own null maxima**.

**Criterion 2, G4** — a band answers only if its prominence beats **that band's
own null maximum**. Not a number anyone chose, per-band, and built where the
answer is unreachable. **1 of 10 answers → NO RULING.** The survivor, z
0.90–1.20 at **−1 px = −5 mm**, reproduces the joint fit from a tenth of the
pixels.

**And the verdict was tested for being mine.** One sweep of the bar returns
**FLAT (19 mm), NO RULING, and NOT FLAT (415 mm)**. The ladder's answer is a
function of the acceptance bar, not of the vehicle.

**Conclusion: the flat-versus-scale question is not awaiting a better gate — the
z-ladder cannot answer it.** The **JOINT whole-vehicle registration (−1, −4) px
= −5 mm z, −19 mm x** is untouched, and §10.98's headline does not rest on the
ladder.

## 3. Item 3 — refused, on the repo's own numbers

§10.98.11's **−6.5 mm** counter fascia compares the right FEATURE on the WRONG
RULER. Both photographic readings are taken on the counter's outer face — **0.295
m nearer the camera** — and divided by the **flank plane's** px/m.
`t1_detail.py` states exactly this of the very 113-column run that yields the
94.3 mm.

REF §6's own parallax pair (1.189→1.205, 1.082→1.103) fits a one-parameter
scale-about-horizon model **exactly**, reproducing REF's stated **+16 / +21 mm**
with **s = 0.9533** and camera height **1.531 m**. Applying it:
**93.6 → 89.2 mm** and **94.3 → 89.9 mm**, so **model − photo = −2.1 to −2.8 mm**,
and across `t1_detail`'s documented **+15…+31 mm** bracket the residual
**changes sign**.

**The third route agrees and shares no step:** REF §6's slab edge **22.65 px =
0.107 ± 0.005 m** against the built **`CNT_ZT − CNT_ZB` = 0.1070 m** — **zero**.

**No geometry moved for item 3 and no hero is owed.** What would re-open it is
the route `t1_detail.py` already names and nobody has built: the counter top's
**INNER** edge, on the flank plane, needing no parallax — a clean step in
`ref_rear34.jpg` at y 423, x 700.

## 4. Defects of mine, four, all caught by controls

* **C1's target was TRANSPOSED** — I typed `(-4, -1)` for the published
  `(-1, -4)`. My computation was right; my transcription was not.
* **C3's first draft was INVALID** — rolled the edge map without the mask,
  manufacturing a spurious instability signal. Replaced with an END-TO-END
  control that shifts the render image and re-derives the warp: predicted
  −10.5 px, observed −11.
* **A CONSTANT VERDICT STRING** — the bar sweep printed *"no bar supports FLAT"*
  three lines below a row printing **FLAT, 19 mm**. §10.50's defect, **third
  instance in this repo, second by me**, in the hour I quoted both earlier ones.
  Now derived.
* **C6 exists because the fast scorer is a SECOND INSTRUMENT** — proven equal to
  the inherited `np.roll` form to **6.75e-13**, not asserted in a comment.

## 5. What rev 42 inherits

* His **eight defect reports** remain the spine. **Reports 6 and 8 closed
  (rev 38). Report 3 is NOT closed** and is back where rev 38 left it (§10.24).
* **Report 3's counter-fascia route is now closed as a route** (§10.99.6) — it
  was never independent of the flank ruler.
* Untouched and live: Report 5 (doors, off `ref_workshop.jpg`), Report 4 (the VW
  glyph's 52 mm interpenetration), Report 7 (Calidad, texture-versus-panel
  first), `V_POW`, and `probe_clean_top` / `probe_dust_anchor` — **nine
  revisions**.
* **§7's standing instructions are unchanged**, including the die-cut sticker
  (the original deliverable, still unbuilt), the Playa hero (deprioritised, not
  cancelled), Nolita (authorised, still unused), the GitHub migration, the
  two-sided front roof lid and the trunk lid, and the never-run UV-overlap and
  texture-resolution check.
* **No question is outstanding with him.**
