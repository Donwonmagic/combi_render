# HANDOFF rev 26 — the pedestal is the dust film, and two of three work items were malformed

> **THE STANDARD, in the owner's words, and it governs every line below.**
> The final product should be nearly indistinguishable from the original.
> **Any single measurement off is unacceptable.** We are recreating a photo
> realistic version of **that exact bus**. The criterion is PER-MEASUREMENT.
>
> And above clinical accuracy: *"I really want this to give the person the
> opportunity to feel like they were on Playa del Carmen all those years ago.
> I want the owner to remember standing in the kombi, in this very picture
> that was provided."* — **that owner is the restaurant's owner, not Donald.
> Donald has never stood in the bus.** Ask what a PHOTOGRAPH shows; never ask
> what the vehicle looks like.

---

## 1. Arrival state — rev 26 OPENED CLEAN, seventh revision running

**Fourteen bundles crossed the device bridge in ONE `device_stage_files` call.**
All nine md5s recorded in memory matched exactly. Restore ran
59 → 67 → 71 → 75 → 81 → 87 → 93 → 96 → 101 → 105 → 107 → **115, clean tree**,
with no divergent-branches error at any line. **20/20 content greps exact, 8/8
ancestry.** Guards on arrival **0 fail / 0 warn at both levels**, every figure
reproducing rev 25's table.

Blender 4.5.3 + pillow + scipy installed as prescribed.

**Two defects in rev 25's own record, caught on the way in (§10.74).** Neither
touches the model; both would have cost the next context real time.

1. **`NEXT_CONTEXT_PROMPT_rev26.md:283`'s check cannot pass on a fresh clone.**
   It asks `ls HANDOFF_rev25.md rev25_hero34f.png`, but `.gitignore:9` is
   `rev*_hero*.png` and commit `091ff2e` is titled *"keep the hero OUT of the
   repo, as every prior revision did"* — which §7 of the **same document**
   explains at length. §1 and §7 contradict each other. The check is **DELETED,
   not loosened** (the rev-21 `STRADDLING` precedent, not rev 22's
   `H_ROOF_REGRESSION` one: this string can never match a clean tree, rather
   than merely having the wrong count).
2. **`swirl_b.png`'s md5 is wrong in its eighth character.** `SPEC.md:2821` and
   the prompt both say `d2015971`; the committed file is **`d201597e`**. The
   FILE was always right — working tree and `HEAD` agree byte-for-byte and it is
   what `9ad9a3b` wrote. Corrected in SPEC.

## 2. Guards at the end of rev 26 — every figure IDENTICAL to arrival

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 0 warn** | **0 fail, 0 warn** |
| roof crown @ rear axle | **1.9835** (baseline 1.9835, −0.0 mm) | **1.9833** (−0.2 mm) |
| rear arch lip → gap | **0.3722 → 39.7 mm** | same |
| front arch (control) | **0.3732 → 40.7 mm** | same |
| rake | **17.75 mm/m (locked 17.75)** | same |
| dome deficit / rear overhang | +0 / **0.7730** | same |
| dims | L=4.065 W=1.750 | same |
| cut roof hole | **68564v** | **252749v** |
| objects at `materials:` | **126** | **126** |
| shut line × aperture, SHOW | **0.0 mm** | **0.0 mm** |
| shut line × aperture, OFF | **804.9 mm** (baseline 804.9, −0.0) | same |
| `CARGO_GAP` samples | **154** | same |

Also **185 meshes**, 42 materials, 5 constant-rough, **0 non-manifold**, three
open apertures on +Y, four shut lines 100 % open, band 1.372–1.775, bay widths
**0.516 0.515 0.516**.

**NO GEOMETRY MOVED AND NO ARTWORK MOVED IN REV 26.** The three committed
textures are byte-identical — proven by re-baking three separate times, not
asserted (§3 below).

## 3. What rev 26 did

### §10.70 — item 1: `COUNTERTAN`'s pedestal is the SETTLED-DUST FILM

Six revisions on the list as "UNIDENTIFIED". Four arms, two albedo points ×
dust on/off, through rev 24's index-clean mask at ONE purged rig, EV −4,
0.001–0.002 % clipped everywhere, null control exact in every arm:

| arm | pedestal `P/R` | `k` |
|---|---|---|
| shipped | **60.8 / 58.2 / 59.5 %** | 0.0368 / 0.0362 / 0.0372 |
| `T1_CTAN_WEAR=0` | 55.3 / 52.5 / 53.4 % | 0.0446 / 0.0440 / 0.0451 |
| **`T1_CTAN_DUST=0`** | **25.1 / 25.0 / 31.9 %** | 0.0731 / 0.0716 / 0.0740 |
| dust **and** spec **and** coat off | **6.6 / 6.6 / 8.5 %** | 0.0871 / 0.0860 / 0.0889 |

Dust carries **57.1 / 52.6 / 36.6 %** of the pedestal; dust + spec + coat carry
**89.3 / 87.9 / 84.8 %**. Wear carries **3.2 / 3.7 / 5.1 %**.

**The harness control is what makes this readable:** the shipped arm reproduces
§10.65's published clean pedestal — **60.8 / 58.2 / 59.5 %** — to three
significant figures in all three channels, on a tree restored independently
from the bundles. Noise floor 0.211 % against a ~35-point effect.

**Why five revisions missed it.** §10.56 ablated dust, saw the top's radiance
rise only +4.1 / +8.6 / +13.3 %, and concluded *"REFUTED — and it was
HELPING."* **That does not follow.** Removing a mix of coverage `f` and
base-independent colour `D` changes radiance by `f·(A−D)` — small *precisely
because* `W_DUST_COL_UP` is within **13.5 %** of `COUNTERTAN` in R — while
contributing `f·D` to the pedestal, which is large. **Both true at once; the
wrong derivative was measured.** The coverage was never hidden: `t1_mats.py:366`
says *"mean coverage 0.548 on the counter top"* in prose and a **live assert**
recomputes 0.548256 on every build.

**Independent cross-check from an unrelated route:** a base-independent mix at
coverage `f` must raise `k` by `1/(1−f) = 2.214×` when removed. Measured
**1.988 / 1.978 / 1.989**. Agreement claimed to ~10 % and no better.

**The lever was checked before it was believed**, per §10.56's own rule: `Dust`
reaches `dfac → cdust → Base Color` and **nothing else** (Roughness is the fade
path, Metallic the wear path), so it removes the ALBEDO. `T1_CTAN_WEAR=0` also
drops Metallic and is labelled as **two levers**, not presented as pure.

**Nothing was tuned. `COUNTERTAN` UNCHANGED at (0.5870, 0.4930, 0.3060), sixth
revision running.** This is not an error — the dust film is a modelled, measured
feature. What it settles is *why* `COUNTERTAN` was never solvable: `k` is
**2.37× weaker** in the shipped configuration than the bare surface allows, by
construction. rev 15's *"closing on albedo demands (0.177, 0.408, 0.094), not
any wood"* is **explained, not overturned**.

Instrument shipped as **`probe_ctan_pedestal.py`**, which ASSERTS the harness
control rather than claiming it in prose, and prints what is NOT claimed.

### §10.71 — found while verifying that, RECORDED NOT APPLIED

`W_DUST_FAC_UP = 0.7313` — the constant that puts 54.8 % base-independent ochre
on the counter top — is pinned by a **live assert that uses the wrong base
material**. `t1_mats.py:441` predicts `_UP_MEASURED` (commented *"dirty counter
top, de-illuminated"*) from **`COUNTERCREAM`**, while the counter top carries
**`COUNTERTAN`** and has since rev 12.

| base | predicted | vs `_UP_MEASURED` | |
|---|---|---|---|
| `COUNTERCREAM` (what the assert uses) | (0.6104, 0.5300, 0.4264) | 0.0001 | PASSES |
| `COUNTERTAN` (what the surface is) | (0.5435, 0.4297, 0.2665) | **0.1600** | **FAILS by 80×** |

**Both halves entered in ONE commit** — `00d3819` *"rev 12: … tan counter top;
weathering + roughness"*. They cannot both be right. The assert cannot see the
difference because it never reads `COUNTERTAN`. Same family as the dead
`RIM_R`, the dead `countertan` arguments, `_NOSE_SEL` and `FadeVert`: **a
constant landed on the material whose NAME matched.** Fifth instance.

### §10.72 — item 3 is MALFORMED: both bumper numbers are the catalogue, halved

`2.145 = 4.290/2` and `2.140 = 4.280/2`, **changed in the same diff hunk** of
`27f6ee6` *"…evidence audit against reference **+ factory sources**"*. The 5 mm
is exactly half of a catalogue revision. `verify.py:33` already records 4.290's
catalogue origin and `:37` invokes the standing instruction — *never correct
this vehicle toward the VW factory catalogue* — to make the measurement win for
`L`; **§2's bumper row never got that treatment**, and §2's header grades the
table **S (factory brochure) unless noted**, with no note on this row.

Also: `X_BUMP_F/R` have **zero read sites**; `BUMP_OFF`'s own comment shows the
mesh was **fitted to the constant** (circular); the rear face is commented out
at `build.py:325` fourteen lines below §2.4's "model it absent"; and the `:191`
citation is stale (`:201`), **born stale in the commit that wrote it**.

**Neither value is measured.** rev 25's instruction *"do NOT add a
`_RETIRED_VALUES` row"* **stands, for a stronger reason** — a row would assert
one of them is live. Strike both; re-open as UNMEASURED.

### §10.73 — item 2 is an ARTEFACT

`_DOOR_TOP_AUTH`'s "4.2 mm" compares a five-knot **run mean** (1.80980) with a
**station value**. `folk_gen.py:503` subtracts `rake_drop(1.36)` from
`_DOOR_TOP_AUTH`, which is only meaningful if it is an un-dropped z at
x = 1.36, and the bottom term is that same station. Compared like for like on
`DOOR_GAP_S` — the smoothed outline that actually **cuts** the geometry:

| quantity | value | vs 1.8140 |
|---|---|---|
| 5-knot run **mean** (what rev 25 quoted) | 1.809800 | −4.200 mm |
| raw `DOOR_GAP` **at x = 1.36** | 1.814333 | +0.333 mm |
| **`DOOR_GAP_S` at x = 1.36** | **1.814315** | **+0.315 mm** |

Chain cross-check in the same computation: `DOOR_REAR_DX` comes out
**17.250 mm**, reproducing §10.68 exactly — which is what shows the
re-implementation is the repo's own arithmetic.

**rev 25's pre-print comment was RIGHT and its print measured a different
quantity.** Value HELD at 1.8140, **no re-bake owed**, `DOOR_H = 1.013467`
unchanged (and `folk_gen.py:503`'s `# ~1.017 m` corrected — 3.5 mm, another
figure never watched print). What IS open is smaller: **both numbers are
authored and the door's true top edge is unmeasured, and unmeasurable on the
admissible set** — no supplied frame carries both a closed cab door and an
admissible px/m on the door plane.

### `folk_gen.py` was EXECUTED, not read

rev 24's lesson was that §10.63 verified a `folk_gen` change **by reading** and
it had broken `composition()`. rev 26 changed only comments in that file and
still: imported it (every parse ran, `DOOR_H` printed 1.013467), called
**`composition()` for both sides** (returns an 8-entry dict each), and **re-baked
three separate times** — `git status tex/` empty every time, all three md5s
unchanged. That independently re-confirms rev 25's determinism claim and that
the committed artwork is what the current source produces, without needing the
bisect.

**My first dynamic probe was ill-posed** — I passed `main()`'s outer per-side
dict where `composition(res)` wants one side's result, and it raised `KeyError`.
Exactly rev 24's shape. Recorded rather than smoothed over.

## 4. Things the next context must NOT silently undo

`HANDOFF_rev25.md` §4, rev 24's §4, rev 23's §4, rev 22's §3, rev 21's §4,
rev 20's §4, rev 19's §4 and rev 18's §4 **all still stand in full.** Adding:

1. **Do not "fix" `_DOOR_TOP_AUTH` to 1.8098.** §10.73 settles it: 1.8098 is a
   run mean, this is a station value, and the like-for-like disagreement is
   **0.315 mm**. rev 25's instruction stands with a measured reason behind it.
2. **Do not tune anything on §10.70.** The pedestal is not an error; the dust
   film is a modelled feature. What §10.70 licenses is *re-deriving* `k`
   (0.0368 shipped, 0.0871 clean) before any future solve — **never carrying the
   old secant gain, and never carrying rev 24's "+40 %" either**, which is
   relative to a contaminated-mask measurement and is not the fascia's.
3. **Do not repair §10.71 blind.** Changing `W_DUST_FAC_UP` or re-anchoring its
   assert moves the shipped build. It is recorded as the next revision's item 1
   precisely so it is done with a measurement.
4. **Do not add a `_RETIRED_VALUES` row for the bumper faces**, now for the
   stronger §10.72 reason: neither value is live, so a row would assert one is.
5. **`T1_CTAN_WEAR=0` is TWO levers** (albedo chain + Metallic). Do not quote it
   as a pure ablation.
6. The off-flank crossing baseline (804.9 mm ± 10 mm) and the `H_ROOF`
   regression band (1.9835 ± 5 mm) **must never be tightened.**

## 5. Still open

- **§10.71 — `W_DUST_FAC_UP` anchored to `COUNTERCREAM` on a `COUNTERTAN`
  surface.** New, named, localised. **The oldest undone item is now this**, and
  it is a much better-posed question than "the pedestal is unidentified".
- **The residual pedestal, 6.6 / 6.6 / 8.5 %.** Not identified. Never-ablated
  paths, each one render, each with an existing override: `T1_WORLD=0`,
  `T1_CYCALB=0`, `T1_GAL_LUM=0`; plus scene→top bounce (`gal_warmer` and the
  caddies sit **on** the top — hide the object, a visibility flag is barred);
  plus the grazing lobe at ~83° off normal, where `T1_CTAN_SP=0` may leave
  F90 = 1 and therefore may not be a complete specular ablation. **UNVERIFIED —
  test before use.**
- **§10.75 — THE FRONT BUMPER CARRIES AN OVER-RIDER BAR THE MODEL DOES NOT
  BUILD. ANSWERED BY THE OWNER.** Shown the photograph beside a render of the
  current build, he ruled **A (the upper tube) and C (the vertical post) are
  BOTH ON THE BUS** — an over-rider bar and its post — and chose **model them,
  tagged workshop-stage**. The model builds one blade plus two 62 × 30 mm
  brackets and **has no member for either**. Measurement NOT done: the first
  pass failed its own consistency check (trolley occlusion, 4.7× spread), the
  swept threshold brackets the tube at **7.9–11.7 px (±19 % systematic)**, and
  **my PSF control was invalid** — it crossed the two-tone break diagonally and
  returned 52 px. A valid PSF and a scale on the nose/bumper plane come first.
- **The front bumper face is UNMEASURED** (§10.72), separately from the above.
- **`CREAM`** — needs a same-light, same-CLASS, three-channel reference. Does
  not exist in the three photographs. Unchanged at (206,208,200).
- **THE ABSOLUTE ROOF HEIGHT** — 1.960 retired, nothing replaced it.
- **THE OFF FLANK** — two mutually contradictory **E** features, 804.9 mm.
- **The cab door's true top edge** — both candidate values authored; unmeasurable
  on the admissible set (§10.73).
- `PLATE_W = 0.3300` has no provenance. `probe_rev16.py:90` prints `xa` vs `xa`.
  `X_NOSE`/`X_TAIL` parsed in `folk_gen` and never LOADED.
- Tail-lamp material slot; `Senor` at 0.504 of its 0.782 ceiling; `SCR`'s
  +80 mm. **None started in rev 26.**

## 6. Ordered work list for rev 27

1. **§10.71 — settle `W_DUST_FAC_UP`'s anchor with a measurement**, then decide
   whether the constant or `_UP_MEASURED`'s label is wrong. It now dominates the
   counter top's appearance by §10.70, so it is the highest-value open item.
2. **The residual 6.6 / 6.6 / 8.5 % pedestal** — `T1_WORLD=0`, `T1_CYCALB=0`,
   `T1_GAL_LUM=0`, one render each, overrides already exist. **Test the F90
   question first** — it is free and it decides whether arm 4 was complete.
3. **THE FRONT OVER-RIDER (§10.75)** — the owner's reading has landed and the
   model is missing a whole assembly. Order: measure a **valid PSF** on
   `ref_workshop.jpg`; establish a scale on the nose/bumper plane or prove none
   is admissible; only then size and build the bar and post, **every number
   tagged workshop-stage**. Strike ±2.145 / ±2.140 from §2 as catalogue-derived
   either way (§10.72). **Building this moves geometry and invalidates
   `rev25_hero34f.png`** — re-shoot after, never before.
4. Tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
5. A hero **only** if geometry or artwork moves — **and item 3 will move it if
   it lands.** `rev25_hero34f.png` still
   photographs the current mesh AND the current artwork — **verified this
   revision by three byte-identical re-bakes**, not assumed.
6. Camera absolutely last.

**NO QUESTION IS OUTSTANDING WITH THE OWNER** — the `ref_workshop.jpg` bumper
reading came back and is recorded as §10.75. The one photograph that would move most still
closes THREE things: a head-on rear or front elevation from roof height closes
`CREAM` and the absolute roof height; a clear off-flank view closes 804.9 mm of
unadjudicated crossing.
