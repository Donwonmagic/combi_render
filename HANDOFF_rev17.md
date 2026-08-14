# HANDOFF rev 17 — THE SHADER AND COMPOSITING BACKLOG

**The headline is not a fix. It is that the revision's first work item was
aimed at a number measured on the wrong surface, and the check that found it
cost one afternoon and no renders.**

Verify by CONTENT, never by hash or commit count.

---

## 0. Guards, and the figures I watched print

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 1 warn** | **0 fail, 1 warn** |
| warn | roof crown @ rear axle (dome-corrected) **1.983** vs spec 1.960 (**+23 mm**) | identical |
| dome deficit | **+0 mm** | **+0 mm** |
| rear overhang | **0.7730** = 0.3221 of the wheelbase | **0.7730** |
| dims | L=**4.065** W=1.750 | same |
| cut roof hole | **68088v** | **252335v** |
| objects at `materials:` | **126** | **126** |

Also printed every run and unchanged: `roof aperture: open, and solid fore /
aft / both sides`; `TYRE_D=0.6650`; 3 open apertures on +Y; four shut lines
`100 % open`; band `1.372–1.775`; bay widths **`0.516 0.515 0.516`**;
**42 distinct materials**; **5 constant-rough**; **0 non-manifold edges**.

**MESH COUNT 181 → 185.** Four new objects, one hubcap ring per wheel. This is
the only figure in the guard block that moved this revision.

`cutters rolled back | none` is a **STATE.md row, not a console print.**

---

## 1. THE HEADLINE — the cream target is the galley, not the paint (§10.38)

`cream_rms.py`'s **8.890 %** is the **galley interior seen through serving
bay 3**. Its search band `v 240–320` overlaps the guarded serving-aperture
band, and its gate `sat < 0.30 & lum > 0.20` is not a test for cream paint — it
is a test for *pale*, which a lit galley, a cream jacket and a whitewashed wall
all pass. The galley is the most uniform pale thing in the frame, so it **wins
the scan**.

Proven against the two locked image lines, not by eye: rev 16's drip-rail fit
and §10.34's 27.7 mm drip-to-aperture put the band at **v 305.6–399.0** at those
columns; the chosen patch is `v 319–345`, **entirely inside**.

So every "the cream is 26× too uniform" statement compares the render's paint
against an open hole.

**`ref_side.jpg` cannot supply a replacement** — 1799 gated body-cream pixels in
the whole frame, best 60×20 window **33.8 % pure** — **and it is the worst frame
this project owns**: 2.32 bits/px, JPEG DC quantiser 4, against `ref_rear34`
9.28 / q1 and `ref_workshop` 8.87 / q1.

**NEW STANDING RULE: A CLASS GATE IS A PROBE TOO.** Gate on GEOMETRY — which
surface of the vehicle — before gating on colour. `cream_rms.py` now carries a
hard guard that refuses to report the old number and prints why.

**And the control for the control was wrong.** "Smooth, re-encode, re-measure"
charges the codec for the blur's own leak, because a Gaussian blur at σ followed
by a Gaussian high-pass at σ does not leave zero. That overstated the floor ~4×.
Done properly — blur by 4σ, measure the leak with no codec, subtract in
quadrature — the codec contributes **0.31–0.66 %** against 8.89 %. A constant
field gives exactly **0.0000 %**. The structure is real; the surface was wrong.

**Re-based on `ref_rear34.jpg`, the owner's choice.** Lid underside, 25 800 px,
80.8 % pure after 3 px erosion. Caveat that must travel with it: **inward-facing
panel, so a LOWER BOUND** on the sun-exposed flank.

**The character, from four scale-free discriminators:** corr(dL\*, dC\*) =
**−0.486** at σ 8 and growing with scale, chroma structure of the same order as
luminance, anisotropy **0.885–0.918** (isotropic). That is **CHALKY SUN-FADE
MOTTLE** — patches oxidised lighter and less chromatic. Not dirt (correlation
would be positive), not brush (chroma flat), not dents (chroma flat, large scale
only).

**Which finally explains `W_ALBEDO`: a scalar multiply on albedo CANNOT change
chroma.** The map must modulate the existing fade path — rev 14's `FadeVert`,
currently spatially constant — and drive roughness with it. **It is not an
albedo-breakup map.** `W_ALBEDO` stays closed.

**NOT BUILT.** The grounding is complete and the mechanism identified, but the
amplitude cannot be tuned against a target whose **mm axis is open**: three
routes to px/m on `ref_rear34.jpg` all failed — aperture band truncated by the
counter (≥320), tyre truncated by the frame (≥397), bulb string **not detected**
(peak/mean 3.6, candidates 225–629). **None was invented.** That is the next
revision's first job.

---

## 2. What else landed, each with its measurement

**`audit.py`'s re-typed 4.290 (§10.39).** `verify.py:47` re-expressed
`SPEC["L"]` when the tail was re-spaced; `audit.py:319` did not. `STATE.md` — the
file this repo declares authoritative over prose — reported the length row
**−225.2 mm OUT** on a quantity verify PASSES at **+9.8 mm**. Now imported from
`verify`, one definition in the repo. *Still open in the same table*: the height
row reports **+1056.9 mm OUT** every run because it measures the **open lid board
standing above the roof**. A prose note under it says the test is wrong; a note
is not a guard.

**`vw_bars`' air-gap docstring (§10.40).** Deleted as false: the V **penetrates**
the W by **52.0 mm**, `0.370` has been stale since rev 10, and no diameter can
open a gap because the spine separation is 0.015 R against mitred half-extensions
an order of magnitude larger. §10.25's premise is wrong; the fusion is correct
and stays. **The V was also short** — 0.7154 of the fit radius against the ring's
inner edge at 0.8140, stopping **4.28 mm** short of the band. Tips grown ×1.1378
about the apex; **angle unchanged at 57.171°**, V radius 0.7898 still below the
W's 0.7965 so `_fit_glyph` does not move.

**The hubcap ring (§10.41).** `CAP_RING_BANDFRAC = 0.093 ± 0.012`, band/outer D,
dimensionless. The decisive step was measuring each frame's **PSF first**: the
band is **1.05 σ in `ref_side.jpg` (unresolved)** and **11.6 σ in
`ref_workshop.jpg`**, and a naive half-level crossing on `ref_side` reads exactly
double. Ceiling stated honestly — statistical floor ±0.0013, but the transfer
between frames cannot be tested better than ≈±0.03. Negative control: the
workshop van's plain hubcap, better PSF, no ring.

**The real matte (§10.42).** File Output off Render Layers `Alpha`. 256 unique
values, 26.00 % partial, control with the subject deleted → 0.0000 % cover.
**Bit-identity on the default path was NOT claimed because it is not true**: two
renders of the same frame with nothing changed differ by max 40 DN over 12.86 %
of pixels. The claim made instead is structural — the compositor subgraph
serialises equal. **Re-read rev 14's "byte-identical, hash-verified" in this
light.**

**`flank_compare.py` (§10.43).** The brief's premise — that rev 16's loft moved
the windows — is **refuted with the measurement**: `SCR` is forward of
`X_AXLE_R` so `_aft()` is the identity on it, the widened arch is 146 mm clear,
the roof junction is 810 mm above. What moved was the instrument (`REF_PPM`, one
scalar for a projective photograph, 4.7 % wrong across the lockup). **The +95 mm
ink offset is 87 mm of missing tarnish in the RENDER mask** — the reference mask
has five thresholds, rev 14's render mask had one. With them: **+3.1 mm**.
Re-measured: area **0.9364** PASS, aspect **+4.86 %** PASS, IoU **0.7631 = 0.889
of a 0.8585 ceiling** PASS, `Senor` **0.504 of its own ceiling** FAIL. No
threshold changed.

---

## 3. `H_ROOF` — delegated, and deliberately NOT changed (§10.44)

The owner delegated it. **It is unchanged and the +23 mm warn stands**, because
**1.981 is a parenthetical I could not reproduce.** Composing the belt chain from
§10.34's own numbers gives 1.9823 — which agrees to 1 mm — but the model's own
belt→drip is 568.0 mm, not the measured 529.7, because rev 16 spent that 38 mm on
the junction. So the terms are not additive in the model's parametrisation and the
agreement may be coincidental. Resolving it needs a **direct probe of the built
mesh**. Changing a locked constant to a number nobody watched print, in the
direction that clears a warn, is the two things this repo forbids at once.

---

## 4. What rev 17 did NOT do

- **The cream map is not built** — grounded and designed, blocked on the mm axis.
- **`COUNTERTAN`'s interreflection test was not run.** Untouched from rev 15.
- **No adversarial audit of the rev-16 loft.** It is still new geometry checked
  only by its own author. This is now the largest unexamined surface in the repo.
- **No camera change**, per the standing order.
- **The tail-lamp material slot is still shared with `amber`** — it needs a new
  material in `t1_mats.py`, which no agent owned this revision.
- **The vision-capable pass over the ~12 unverified image URLs was not run.**

---

## 5. Process, honestly

Three of the four work items came back with their **briefs refuted** — the cream
target, the flank windows, and (from rev 16) the hubcap crop box. Two of the
three wrong crop boxes this revision were **mine**, drawn for the owner or handed
to an agent. The rule "check what a probe can physically see, and print the crop
box" now has six instances behind it and it should be applied to *class gates*
and to *briefs*, not only to crops.

The owner also corrected a misreading carried in my own memory for several
revisions: **he has never stood in the bus.** The "remember standing in the
kombi" bar is about the **restaurant's owner**, the person the work is for. He
can identify what a photograph shows — and that has paid off eight times — but
surface character must be **measured, never asked.**
