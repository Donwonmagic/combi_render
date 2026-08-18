# HANDOFF rev 39 — a MEASUREMENT revision. No geometry, no artwork, no constant moved.

> **THE STANDARD, in the owner's words.** The final product should be nearly
> indistinguishable from the original. **Any single measurement off is
> unacceptable.** The criterion is PER-MEASUREMENT. And above clinical accuracy:
> *"I want the owner to remember standing in the kombi, in this very picture that
> was provided."* — **that owner is the restaurant's owner. Donald has never
> stood in the bus. Never ask him what the vehicle looks like; ask what a
> PHOTOGRAPH shows, then measure it.**

## 1. What rev 39 did

It ran **his own method**, which no revision had ever carried out: the broadside
render laid over `ref_side.jpg` at matched scale. He chose that over doing his
Report 5 directly, over Reports 3+4, and over the sticker, on the argument that
it grounds the door fix rather than authoring it.

Full account in **SPEC §10.97**, fourteen parts. The three that matter:

* **`flank_compare.py` was EXECUTED for the first time in the project.** It was
  recorded NOT RUN in rev 10 and is not mentioned again in twenty-eight
  revisions. Its verdict is FAIL on one region; its *finding* is that the script
  lockup must move **+76.2 mm forward and +61.9 mm down**, cross-checked in the
  same run by a route sharing no step with it (`SCR`'s x extents +83 / +80 mm
  aft of `flank_X(LOCKUP)`), with the height **31.5 mm short, not rev 17's
  12–24**. §10.97.2.
* **SPEC 10.35's flank map is validated end to end for the first time: −5 mm**
  across the whole vehicle. Twenty-three revisions of use, never checked against
  a rendered model across its full range. §10.97.4.
* **The body sits 81 ± 7 mm high against the cream/red two-tone break**, flat in
  u (5 bands, spread 4 px) and flat in z (7 bands answered of 10, spread 19 mm
  over the whole height). One rigid offset — **the break line is the misplaced
  member.** §10.97.5.

## 2. Why that last one is the revision

It is **his Report 3** — *"the paint job and the headlights are not alligned"* —
and it is the **fourth** derivation of §10.24, the first that uses **no headlamp,
no roundel and no scale on the lamp**.

It also explains why §10.24 kept being reverted. Its findings were applied once
and reverted once, killed each time by the frontal silhouette of `ref_side.jpg`
refuting the finding **as applied** — and *as applied* meant **moving the
headlamps**. The misplaced member is the **break line**. Moving the break is a
different change: the **roundel does not move at all** (§10.24's explicit
constraint satisfied by construction), the **lamps do not move** (so the
frontal-silhouette refutation does not bear on it), and it is the RELATIONSHIP
his report names rather than either half of it. §10.97.6.

**NOT BUILT.** Four geometry changes at the tail of a shipped revision is how
this project has been burned. It is rev 40's item 1 with the number in hand, and
`SCR`'s +76 / +62 must wait on it because the break is `SCR`'s own datum.

## 3. His three decisions

* **The mural board has TEN flower heads, not nine.** His rev-8 count of nine had
  never been checked against the build in twenty-eight revisions; `lid_gen.py`
  has built ten since rev 10, and rev 11 "verified" that ten **against rev 10's
  own ten**. Shown the board rectified flat he answered TEN. SPEC §0's rev-8 line
  is struck. §10.97.11.
* **Broadside overlay first, then Report 5 off it**, over three alternatives.
* On the sticker's papel picado: *"Leave it open, I'll decide when the sticker is
  actually being built."* Nothing is blocked by it; do not re-put it until then.

## 4. Two things the inherited brief had wrong

* **§6 item 1 names the wrong frame for Report 5.** It says to measure the door's
  lower cutaway off `ref_side.jpg` "if the man's red shirt does not occlude it".
  The shirt is not the blocker: **the cab door is OPEN 49° in that frame**, which
  SPEC already records in two places. The only frame with it CLOSED is
  `ref_workshop.jpg`, which carries no admissible px/m on the door plane. The
  route is a scale-free ratio against the arch, whose radius is locked.
  §10.97.12.
* **`STATE.md` arrived with `working tree | DIRTY`**, commit 205 against a HEAD
  of 207 — not the clean parent-provenance pattern the brief describes. Resolved
  by REGENERATION, not trust: byte-identical except the four provenance rows.
  §10.97.13.

## 5. Seven detector defects of mine, not one found by inspection

A class gate that excluded its own subject (0/10 positive); a negative control
that failed on the occluding man; a drip-rail finder on the wrong edge; **a hub
detector that locked onto the man's RED SHIRT** — §10.7's trap, fourth instance;
a tyre gate whose luminance band contained the red body and would have printed
"the tyre is 11.3 % too small"; **a z-ladder that reported the end of its own
search range as a peak**, manufacturing a fictional 13 % vertical scale error;
and **a verdict printed as a constant string** in the probe that documents
§10.50. All in §10.97.7–9.

**A false lead of mine killed by measurement:** the overlay reads as if the
wheels are too large. Measured at the rear-axle column *the map placed*, the tyre
is **651 ± 13 mm against the locked 665** — inside the ±15 mm floor. **The tyre
is right.** §10.97.10.

## 6. Guards — unchanged, because nothing moved

**0 fail / 0 warn at BOTH levels on BOTH tools**, on arrival and at the end.
131 objects, 190 meshes, 42 materials, 5 constant-rough, 0 non-manifold, roof
crown 1.9835 / 1.9833, roof hole 68564v / 252749v, rake 17.75, L=4.065 W=1.750,
arch gaps 39.7 / 40.7 mm, bays 0.516 0.515 0.516, off flank 804.9 mm, over-rider
rows NOT APPLICABLE (stated). All 27 inherited probes match their published
tallies. `probe_rev39_flank.py` makes it 28.

## 7. Rev 40's ordered work list

1. **THE BREAK LINE, 81 ± 7 mm.** His Report 3. Move the break, NOT the lamps and
   NOT the roundel. Re-run `probe_rev39_flank.py` after — it is the guard for it.
2. **THEN `SCR`'s +76.2 / +61.9 mm**, re-measured after the break moves, never
   before: the break is its datum.
3. **REPORT 5**, by a scale-free ratio against the arch in `ref_workshop.jpg`.
   Not `ref_side.jpg` — the door is open there.
4. **REPORT 4**, the VW glyph's 52 mm interpenetration.
5. **REPORT 7**, "100% Calidad" — texture-versus-panel FIRST.
6. `probe_clean_top` / `probe_dust_anchor` — rewrite or retire. **Seven
   revisions.**
7. **A hero, after anything that moves geometry.** Camera absolutely last.
