# HANDOFF — rev 9 → rev 10

## THE STANDARD — read this before anything else

Donald, 2026-08-10, in his own words:

> **"I want a big reminder that the final product should be nearly
> indistinguishable from the original. Any single measurement off is
> unacceptable."**

> **"we are recreating a photo realistic version of that exact bus"**

This is not a quality aspiration to be traded against schedule. It is the
acceptance criterion, and it is **per-measurement**, not on average. A model
that is right in ninety places and wrong in one is not ninety-nine percent
done — it is wrong, because the owner will look straight at the one.

What that means in practice, and every one of these has been broken before:

* **No element ships on a plausible-looking approximation.** If it was not
  measured off a photograph of *his* vehicle, it is not finished. SPEC §10.10
  is the standing requirement; §10.15 is what happens when a photograph itself
  is assumed rather than confirmed.
* **A number is only as good as its datum.** §10.11 (the ground line carries
  ~70 mm of common-mode error) and §10.12 (the locked flank hue came off a
  thumbnail contaminated by the gold folk art) are both cases where a
  confidently-quoted figure was wrong at the source. Re-derive by a second,
  independent method before trusting one.
* **A claim in prose is not a guard.** The canvas ragtop shipped for three
  revisions after §0.2 retired it; `audit.py` printed a fabricated belt line
  for six; `studio.playa()`'s docstring promised dappled shade that no code
  produced. If it matters, assert it in `verify.py` and run both SUB levels.
* **Never report a self-assigned score.** Report the measurement against the
  reference, and report the ceiling alongside it so the number means something.
* **"Good enough" is not a stopping condition.** The stopping condition is that
  a measurement against the photograph no longer improves.

`HEAD` at handoff: see `STATE.md` (machine-written, it wins over this file).

## 0. Authority order — unchanged, and it caught things again this revision

1. Donald's memory: `/areas/tacombi-combi-sticker.md` and `/preferences.md`.
   **Read them before any code.** In rev 9 they carried the locked lids-OPEN
   decision and the standing artwork-replication requirement, and the "front
   paint not true to reality" complaint in the first file turned out to be the
   thread that led to the flank-hue finding (§10.12).
2. `STATE.md` — machine-written by `audit.py` from the mesh built in the same
   process, with the git SHA and a dirty-tree flag.
3. `SPEC.md` §10, then §10.9–§10.14 (they supersede §10 where they differ).
4. `SKEPTIC_PASS.md`.
5. This file.
6. `REF_MEASUREMENTS.md` — **now with a caveat, see §10.11.**

## 1. Reproduction contract

Blender 4.5.3 LTS. Run **both** levels, every time:

```bash
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=2 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=1 /tmp/blender/blender -b --python audit.py
```

Expect at both levels `0 fail, 1 warn`, warn = `roof @ rear axle 1.923 vs spec
1.960 (-37 mm)` (deliberate). Also `TYRE_D=0.6650`, 3 open apertures, four shut
lines `100 % open`, band `1.372–1.775` un-dropped, bay widths `0.507 0.516
0.525`, **132 meshes**, 0 non-manifold edges, `cutters rolled back: none`.

Box: 2 cores / 8 GB. Timings measured this revision — **use these, not
rev 8's**: `hero34f` 1200×800 / 24 samples single-pass **100 s**; the same frame
as four padded strips **174 s**; a full 2400×1600 / 64-sample hero as six
padded strips **~20–25 min**, 3–5 min per strip.

**A single shell command here is killed at 10 minutes.** That is why `hero.py`
has `--only N` and `--stitch-only`: drive one strip per call, then stitch.
Background processes are still reaped — `nohup`/`setsid`/`disown` all fail.

## 2. What rev 9 did

**The heroes landed.** First in nine revisions. `out/hero_studio.png` and
`out/hero_playa.png`, both 2400×1600 / 64 samples / six overlapping strips /
`post.py` once on the stitch. Worst seam z = 1.88 and 1.45 against a threshold
of 4.

**The strip machinery had a real defect and it is fixed.** Run as prescribed —
four abutting strips — it seams measurably: z +5.2 / +19.4 / +8.2 against a
single-pass reference of the same frame. Cause is mainly OpenImageDenoise's
receptive field, not the 1.5 px reconstruction filter. 48 px of overlap per
strip, copying only owned rows, takes it to z −0.3 / +2.2 / +0.7 and pixels
over 20 DN near a seam from 47 to 0. `hero.py`, `stitch.py`, SPEC §10.14.

**The script is rebuilt as explicit letterforms** (`script_gen.py`). No font.
Whole-lockup IoU 0.511 against a measured ceiling of 0.77–0.81. Acceptance
test: `flank_compare.py` crops the rendered flank by projecting the panel's
model extents through the known ortho camera — geometry, not eye — and
`compare_script.py` reports per-glyph IoU and writes a mask overlay.

**Calidad built for the first time** (`cal_gen.py`) and moved **198 mm
forward** on a panel-fraction datum.

**Four findings locked into SPEC:** §10.11 the ground-line datum, §10.12 the
flank hue, §10.13 the Playa rig, §10.14 strip seams. Read them; each one
invalidates a method a previous revision trusted.

## 3. What Donald said at the end of rev 9 — start here

He called time on the context with three things, and all three are correct:

1. **"Doesn't quite look the same font as the original though"** and, on
   seeing it again: **"the Señor Tacombi text is better but I think deserves a
   more finely tuned recreation pass. There are a lot of features that are
   missed or improperly displayed in what I see."**

   He is right, and the numbers agree: 0.511 against a ceiling of 0.77–0.81 is
   the same statement in another form. The *character* is now right — fat
   rounded psychedelic, real spiral counters, ribbon swash, arced baseline. The
   specific letterforms are not, and there is a whole class of feature the
   generator does not attempt at all.

   **Do not restart this.** The measurement infrastructure is the asset:
   `script_gen.py` holds control points in the photograph's own pixel frame,
   `compare_script.py` gives per-glyph IoU plus a mask overlay, and
   `flank_compare.py` crops the rendered flank by projecting the panel through
   the ortho camera rather than by eye. Work the list below against those.

   **Missed entirely — not a tuning problem, a feature the generator lacks:**

   * **The silver is flat.** In `ref_side.jpg` the ink varies: per-channel std
     16–19, luma p5–p95 spanning **85–135**. `tex/senor.png` is a constant
     `(214, 216, 218)` with the whole shape carried in alpha. Real silver leaf
     on a hand-painted panel is mottled, tarnished unevenly, and brushed. At
     hero scale this flatness is very likely the strongest "it is CG" tell in
     the lettering, ahead of any outline error.
   * **No keyline and no drop shadow.** SPEC §3 says the script carries both.
     Worth knowing before chasing it: **it is not measurable in `ref_side.jpg`
     at this resolution.** Sampling outward from the ink edge gives luma 80.5 /
     63.1 / 61.7 at +1/+2/+3 px against open ground 58.7 — a monotone decay,
     i.e. edge blur, with no dark ring anywhere. So either find it in a better
     photograph or retire §3's claim; do not add a keyline because the spec
     says so.
   * **Uniform stroke weight and uniform terminals.** The reference has strong
     thick/thin modulation *within* each glyph and bulbous terminals of varying
     size; the generator uses round caps of one radius per stroke end.

   **Improperly displayed — per-glyph, worst first:**

   | glyph | IoU | what is wrong |
   |---|---|---|
   | `Señor` | 0.089 | not fitted at all; see §4.4. The number is meaningless, not good |
   | `b` | 0.41 | ascender too short and too even; the flag at its top is a guess |
   | `a` | 0.45 | drawn as a symmetric bowl; the reference bowl is asymmetric with a distinct stem |
   | `i` | 0.50 | exit flourish is a plain taper where the reference hooks |
   | `m` | 0.54 | generic arches; reference has narrow slot counters with rounded tops and a spur |
   | `c` | 0.62 | aperture is a plain wedge cut; reference has rolled terminals top and bottom |
   | `o` | 0.61 | closest of the bowls; groove phase still slightly off |
   | swash | 0.62 | arch and roll are right; the taper along the ribbon is not |
   | `T` | 0.68 | best of them; foot flare shape is approximate |

   Whole lockup is also **8 % heavier** than the reference (8609 ink px vs
   7982) — thin globally before chasing individual outlines.
2. **"I don't believe that La Santa part of the roof exists."** — and then,
   looking at the crop: **"That is also the front end of the bus open towards
   the front. What we are looking at is the inside of the front panel."**

   Take this second statement as the headline finding of the handoff. It is not
   a detail about one decal. **`ref_rear34.jpg` has been mis-identified.** Its
   name, and every crop attributed to it in `SPEC.md` §10.10 and
   `REF_MEASUREMENTS.md`, assumes it is a rear three-quarter. Donald — who has
   stood in this vehicle — says the cream lettered panel in it is the **inside
   face of the FRONT panel**, with the front of the roof opening **forward**.

   Consequences, none of them checked yet, all of them to be checked first
   thing in rev 10:
   * the roof does not only open aft-and-over-the-counter. There is a section
     that opens **forward over the nose**, and the lettering is on its
     underside. `t1_detail`/`lid_gen` model a main lid + a smaller aft lid;
     that topology is now in question.
   * every measurement taken off `ref_rear34.jpg` is attributed to the wrong
     end of the vehicle. That includes the flank paisley source crop
     (620,560)-(1200,820) — SPEC §10.10 item 2, currently marked **done** — and
     the "1963" plate surround (1330,780)-(1500,860), item 8.
   * `lid_gen.py:291` draws "La Santa" in a horizontal red serif via
     `_font(158)`. The photograph shows **red brush script rising diagonally
     with a red star over the S**. Face, angle, star and probably the word are
     all wrong, and it is a system font — the exact failure mode §10.10 names.

   **Do not carry any `ref_rear34.jpg`-derived number forward until the view is
   re-established.** Ask Donald to name what each supplied photograph shows
   before measuring anything else from it; three revisions of geometry rest on
   an assumption nobody ever put to him.
3. **"The model is drifting a bit from the reference photo and I want to
   reinforce that we are recreating a photo realistic version of that exact
   bus."** This is the governing instruction for rev 10. Read it as a standing
   check on every change: does this come from a photograph of *his* vehicle?

## 3a. The front fascia is drifting — his observation, 2026-08-10

> "One thing I am currently seeing is that the front fascia is starting to
> drift"

He is right, and the two front references make it concrete. **Note which
photographs these are**: `ref_workshop.jpg` (green, mid-conversion, front
three-quarter) and the front/cab region of `ref_side.jpg` at (60,330)-(330,700)
— plus `ref_rear34.jpg`, which per §10.15 is a FRONT view and has never been
used as one.

Confirmed against those photographs, none of it yet applied:

1. **The folk art on the cab door and lower nose is far too faint and too
   sparse.** `ref_side.jpg` shows **bold graphic scrollwork covering most of
   the door**: large yellow acanthus scrolls, heavy dark-brown outlined
   curlwork, and rows of white/cream rosettes with dark centres, at high
   contrast against the red. The model's flank art is pale, thin and widely
   spaced. This is the single most visible fascia drift and it is a *density
   and contrast* failure, not a placement one. Note it also contradicts
   `SPEC.md` §10.9's measured "0.0–0.2 % gold coverage from X +1.47 to −0.40" —
   that band covers the cab door, and the photograph shows it densely painted.
   **Re-measure; the door is OPEN in that frame (SKEPTIC §B2) and a coverage
   scan run along body x will have sampled the wrong surface.**
2. **The headlamp bezels read gold/brass in the photograph**, visible at the
   left edge of the same crop. The model assigns `"chrome"` at `build.py:291`.
   This is audit `materials-6`, still open: measured bezel R−B is +0.38/+1.15
   where brass would be ≈ +89.
3. **The VW roundel is undersized and sits high** — audit `livery-9`, ⌀0.336
   against SPEC's 0.370 (9 % under) and centre 32 mm high. `ref_workshop.jpg`
   shows a large raised emblem sitting well up inside the cream V. rev 8
   rebuilt the glyph as two mitred prisms; **confirm whether it carried the
   size and height fix or only the glyph.**
4. **The nose silhouette is too wide at the top** — audit `geometry-4`, the
   transverse roof dome is absent: G(z) holds 0.987/0.975/0.949/0.931 where the
   factory section gives 0.923/0.880/0.830/0.699, i.e. **+83 mm/side too wide
   at z 1.53 and +203 mm/side at z 1.85**. This is a silhouette error and it
   shows on every front and three-quarter frame.
5. **The indicators are the wrong type and mounted 20 mm inboard** — audit
   `inventory-9`. REF §V6 resolves them as fish-eye, 74 ± 6 mm, ~78 mm proud,
   centred 0.163 m above and ≥ 0.10 m outboard of the headlamp centre;
   `t1_detail.bullet_indicator()` still builds a period-wrong bullet pod and
   `build.py:294` places it at y = s·0.5250, inboard of the headlamp's ±0.545.
6. **The front bumper reads thin.** Both front references show a deep, chunky
   cream blade with a pronounced roll. Not yet measured — do it.

Items 2–5 are all *already-logged findings that were never applied*. The fascia
did not drift because something was changed; it drifted because the rest of the
vehicle advanced and the front did not.

## 4. Open, ranked by what it would change

1. **The Playa hero does not meet its own brief.** It is seam-clean, correctly
   exposed, and reads as an empty pale plain — not Playa del Carmen. The
   emotional bar in his words is that the viewer feels they were there and the
   owner remembers standing in the kombi. `ref_rear34.jpg` shows what is
   actually behind the vehicle: **dense green palm foliage, close**, flowers
   along the lid edge, warm shade. rev 9 added a palm-dapple gobo and a ground
   haze; the scene still has **no vegetation at all**. That is the single
   biggest gap between the render and the memory.
2. **The mural on the lid underside is far too sparse and too dark.**
   `ref_rear34.jpg` shows a dense full field of large orange/yellow flower
   heads with green foliage on a warm cream ground. The model's board reads
   dark brown with widely spaced heads. This is one of the two art items
   previously marked **done**; the photograph shows it is not — and per §3.2
   even *which lid it belongs to* is now unconfirmed.
3. **The lettered panel** (§3.2 above) — and the roof topology it implies.
4. **`Señor`** — the reference letters are tarnished to green-black and cannot
   be segmented. It is placed from the visual and excluded from IoU tuning.
   Its 0.089 is not a result. Fit it by eye against the 10× crop.
5. **Tail is still 99 mm long** (model −2.108, measured −2.007); the counter's
   `X1` moves with it. Untouched in rev 9.
6. **Six materials still report a constant roughness** (amber, bulb, glass,
   lens, reflector, ruby). `STATE.md` lists them each run.
7. **The rake-versus-arch-gap contradiction** (§10.9) is logged, not resolved.
   Needs a photograph with an unoccluded front wheel.
8. **~23 high-value `AUDIT_RECOVERED.md` findings** still open and never
   through a skeptic pass. The highest-impact for a hero: `materials-5` (three
   serving bays share one reflection, NCC 0.94–0.97 — the most "CG" read at
   hero scale), `materials-14` (both flanks carry the same folk art, mirrored —
   fatal on a two-angle set), `geometry-4` (the transverse roof dome is absent,
   +83 mm/side too wide at z 1.53), `optics-6` (contact shadow dies within
   11 mm of the tyre), `apertures-7` (three surfaces within 1–2 px along every
   bay rim).

## 5. Do not re-open without new evidence

Everything on rev 8's list still stands: the 0.665 m tyre on a 16-inch rim;
`Z_BELT` is not sill − 100 mm; lids-closed / the canvas ragtop; scanning SPEC
§0.2 for material names; **and "raise the flank saturation to 0.816" — §10.12
changed the hue and left the saturation exactly where §10.9 put it.**

Added this revision:

* **Never set a vertical position from REF §0.3's ground line** (§10.11). It
  carries a ~70 mm common-mode error: three independently locked features all
  land low from it by the same sign and magnitude. Use the belt, or a vertical
  extent in which the offset cancels.
* **A single linear pixel→metre scale does not hold across the flank.** The
  rear panel measures 194.8 px/m against 211.5 px/m at mid-body. Place aft
  features by ratio within a panel whose ends are both locked.
* **Do not render `T1_SCENE=playa` with `transparent=True`** (§10.13). It
  composites the world away and you get a blown white sky.

## 6. Mistakes that have now been made more than once

All of rev 8's, plus one new one, and it is the expensive kind:

**A reference photograph was never confirmed with the person who was there.**
`ref_rear34.jpg` was named and treated as a rear three-quarter for several
revisions. Donald looked at one 6× crop of it and said it is the front of the
bus. Nobody had asked. The cheapest check available — showing him a crop and
asking what it is — was skipped in favour of measuring.

**A docstring claimed something no code did.** `studio.playa()` has said
"broken palm shadow rather than an even key — the reference is dappled" since
rev 8; nothing implemented it and the vehicle sat in flat light for a whole
revision. The same shape of failure as the canvas ragtop shipping for three
revisions after §0.2 retired it, and as `audit.py` printing a hardcoded belt
line for six. **A claim in prose is not a guard.** If a rig says it does
something, grep for the node that does it.

## 7. The rule Donald restated, and it governs rev 10

> we are recreating a photo realistic version of that exact bus

Not a 1963 T1. Not a generic taqueria combi. **His.** Every element gets
checked against a photograph of the actual vehicle before it ships, and the
test is whether the owner recognises it — not whether it looks plausible.
