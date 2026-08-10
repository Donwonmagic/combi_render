# TACOMBI COMBI — LOCKED BUILD SPECIFICATION  (rev 7)
**Status: AUTHORITATIVE.** Nothing in the build may contradict this file.
Change this file *first*, log it, then change code. `verify.py` asserts the
machine-checkable rows on every build.

**Working method (standing):** ground in the reference → build → *adversarial*
audit against the reference → iterate. Never build before grounding; never
call it done off self-review.

---

## 0. Evidence grades used in this file

| Grade | Meaning |
|---|---|
| **M** | **Measured by me** from `ref_source.jpeg` — pixel sampling or radial/column profile. Reproducible; method recorded in §8. |
| **S** | **Sourced** — Tacombi's own published text, or a factory/marque reference. URL in §8. |
| **R** | **Research-agent visual read** of higher-resolution photographs **that I could not fetch and view myself**. Treat as strong but unconfirmed. |
| **E** | **Expert inference** — not observed, derived from what a correct 1963 T1 must be. |
| **U** | Unresolved. |

The primary user photograph is **246 × 197 px**. That is a thumbnail. It can
settle large-scale colour, aperture count and wheel construction; it cannot
settle small hardware. Rows below are graded accordingly and **must not be
silently upgraded**.

---

## 0.1 Subject — grounded

The **Playa del Carmen combi**: a **1963 Volkswagen Type 2 (T1)**, bought in
Mexico City in 2006, driven through the Yucatán and converted into a taco
stand. **This is the Playa bus, NOT the Nolita one** — see §7.

**S** — Tacombi's own account: *"We purchased a 1963 'combi' bus in Mexico
City, wheeled it slowly (very slowly) through the Yucatan peninsula and parked
it comfortably in … Playa del Carmen. The engine was scrapped, transmission
sold, seats swapped for cooking equipment, and the roof was reeled back to
produce a taco serving stand."*

**S** — Founder Dario Wolos: the bus was **green** when bought, cost **$3,000**,
was **"missing three of its windows"** and **"only had the front bench"**; he
*"figured out how to **cut open** the Tacombi"*. Opened 6 February 2006.

**E** — "Missing three of its windows" is almost certainly *why* the show side
became three serving hatches: the donor bus already had no glass there.

---

## 0.2 Retired readings — regressions if they reappear

Rows marked ⚠ were **locked incorrectly in rev 3** and corrected in rev 4.

- open-bed single-cab pickup with drop-sides, corner posts or a canopy
- gold side script — it is **silver**
- "Estilo Tacombi" — it reads **"Señor Tacombi"**
- plain font capital T — it is an **ornate swash**
- VW roundel upside down — **V above W**, always
- glazed side windows where there should be **open serving hatches**
- ⚠ **whitewall tyres** — the white annulus is the **cream-painted steel rim**;
  the tyres are **blackwall** (**M**, §8.1)
- ⚠ **chrome bumpers** — they are **painted cream** (**M**, §8.2)
- ⚠ **VW nose roundel painted cream** — it is painted **red on the cream nose**
  (**M**, §8.3)
- ⚠ **a fourth side bay, glazed/frosted, carrying "100% CALIDAD"** — there are
  **three apertures only**, then **solid cream sheet metal** at the rear
  corner. The decal sits **on that sheet metal** (**M**, §8.4)
- ⚠ **folding canvas ragtop** — the roof is **cut into rigid hinged steel
  lids** (**S** + **R**)
- ⚠ **timber plank counter** — the counter is a **cream-painted slab** (**M**, §8.5)
- ⚠ **amber bullet indicators** — bullet pods ended **Aug 1961**; a 1963 has
  flat oval **"fish-eye"** lenses (**S**)
- ⚠ **bus lowered 65 mm / 110 mm** — **unsupported by any evidence**. Stock ride height
- ⚠ **clean restoration gloss** — the subject is **weathered**; see §3.9
- chrome hubcaps — they are **red domes with a light VW**

---

## 1. Body configuration — FROZEN

**S/E** — The donor is an **11-window Kombi/Microbus**: split windscreen, two
cab door glasses, **three side windows per side**, one rear window, **no roof
skylights, no curved rear corner glass** (those are Deluxe/Samba only, and the
corner glass was deleted from Aug 1963 anyway).

| Item | Value | Grade |
|---|---|---|
| Body | T1 **Kombi**, full height nose to tail | **M** |
| Roof | **cut into rigid hinged steel lids**, modelled **OPEN** (rev 8, locked 2026-08-10); main lid hinges fore-aft at the off-side edge and swings up and over the counter, underside carrying the flower mural + yellow menu strips; a second smaller lid aft, lettered "LA SANTA…" | **S**+**R**+**M** |
| Side, show side (+Y) | cab door glazing, then the **THREE stock side windows with the glass removed** — open serving hatches. Aft of the third: **solid cream sheet metal** carrying the "100% Calidad" decal | **M** |
| Counter | **cantilevered cream-painted slab counter** under the three hatches, chamfered front end, running past the tail | **M** |
| Side, off side (−Y) | twin outward-hinged cargo doors + three glazed windows in the same bay positions | **E** (never photographed) |
| Cab door | front-hinged; vent wing + main drop glass; **"ice-pick" pull-lever handle** (push-buttons are Dec 1963+) | **S** |
| Rear | **small** hatch + small window (the big hatch is MY1964), engine lid below, cream rear bumper | **S** |
| Interior | **galley** — counter, plancha, shelving. Not passenger seats | **S** |

### 1.1 Serving-bay layout (show side, x in metres) — **THREE bays only**
| Bay | Front edge | Rear edge | Treatment |
|---|---|---|---|
| 1 | **+0.820** | **+0.313** | open serving hatch |
| 2 | **+0.195** | **−0.321** | open serving hatch |
| 3 | **−0.435** | **−0.960** | open serving hatch |
| — | **−0.960** | **−2.007** | **SOLID sheet metal**, 1.046 m wide. "100% Calidad" sunburst + pink star applied here |

Measured from `ref_side.jpg` (§8.6). Widths 0.507 / 0.516 / 0.526 — they are
**not** identical; they grow slightly toward the tail. rev-3's "three evenly
sized, evenly spaced" was an approximation.

Band: sill **z = 1.402**, head **z = 1.798**, corner radius 0.055, pillars 0.11.
**Bay 4 is deleted.** Any object named `glass_bay3_*` or a fourth aperture
cutter is a regression.

---

## 2. True-to-scale hard points — FROZEN

Frame: **+X forward, +Y left, +Z up, ground Z = 0**, metres.
All values **S** (1963 factory brochure) unless noted.

| Dimension | Value | Was (rev 3) |
|---|---|---|
| Overall length, factory configuration | **4.280 ± 0.06** — front overhang 0.849 + wheelbase 2.400 + rear overhang 0.809 + bumper standoffs | 4.280 |
| Overall length **as it stands today** | **4.06 ± 0.04** — the rear bumper has been removed, see §2.4 | — |
| Overall width | **1.750** | 1.720 |
| Overall height, unladen | **1.941** | 1.940 |
| Wheelbase | **2.400** (front +1.300, rear −1.100) | same |
| Track front / rear | **1.369 / 1.359** | 1.375 / 1.360 |
| Tyre — **NOT 6.40-15** | dia **0.665 ± 0.015** (R 0.3325), section ≈0.129. Tyre/flange ratio measures **1.512 ± 0.02** in `ref_side` and 1.43–1.49 in `ref_workshop`, against 1.64–1.68 for a 6.40-15. Implied fitment ≈ **215/60R16**. rev 4 "corrected" this to the factory 0.683 and was wrong — rev 3's 0.665 was right | 6.40-15 / 0.683 |
| Rim — **16 inch, not 15** | flange OD **0.4396** (R 0.2198), PCD 5×205. Wheelbase/flange measures **5.46 ± 0.08**; a 15" rim requires 5.77 (4σ away), a 16" gives 5.44. Ellipse axis ratio 0.984 rules out perspective. A 1963 left the factory on 15" — **these are not the original wheels** | R 0.1905 (15") |
| Hubcap | dia **0.280**, depth ≈ 0.080 | — |
| Body max half-width | **0.875** | 0.860 |
| **Ride height** | **LOWERED.** Rear arch-to-tyre gap **41 mm** (rev 5 said 71; corrected in the verification pass) against a stock 90–120. Front bumper top 0.348 against a stock ≈0.47. Donald's original rev-3.1 reading was right; rev 4 wrongly zeroed it on absence-of-evidence from a thumbnail. **Set `RIDE_DROP = 0.065` and `ARCH_R = TIRE_R + 0.041`** | rev4 said stock — WRONG |
| **Stance rake** | body sits **nose-down ~1.7°** relative to the axle line (72 mm over the wheelbase). Every height falls ≈28 mm per metre forward. Not modelled yet | — |
| Roof edge / crown | 1.8935 / +0.032 | same |
| Belt line (two-tone break) | ~~z = 1.386~~ **superseded by §10** | same |
| Front / rear sheet metal | x = +2.108 / −2.108. **Note §10.7: the tail measures −2.007 on the vehicle and the factory overhang gives −2.009, so the model is ~99 mm long at the tail. Unresolved.** | same |
| Bumper faces | x = ±2.145 | ±2.140 |
| Bumper centreline | **stock height, z ≈ 0.480** — *not* straddling the wheel centre | "low" |

Tolerance **±25 mm** on L/W/H. **The front end has been flagged as wrong
before — front dimensions and front hardware get checked explicitly every
iteration.**

### 2.1 Belt/sill conflict — RESOLVED against the side elevation
rev 4 flagged a 16 mm sill-to-belt gap where the factory drawing implies ≈90 mm.
Measured on `ref_side.jpg`: **window sill 1.307, body two-tone break 1.207** —
the break sits **100 mm below the sill**. The build's 16 mm is out by ~6×.
**Action: lower Z_BELT to sill − 0.100.**

Note the trap that caused the original misreading: on the serving flank the
visible cream/red edge is **the counter fascia bottom at 1.082**, not the paint
break. The true break is only visible **forward of the counter, on the cab
door**. Do not measure it aft of x ≈ +0.9.

### 2.4 Rear bumper — REMOVED on the real vehicle
`ref_workshop.jpg` shows a cream rear bumper with tubular over-riders fitted at
the conversion stage. Neither in-service photo has one: the tail apron rolls
under to a lip, with only a 14×24 px chrome bracket stub left. It is **not**
hidden behind the counter — the counter fascia bottom is at 1.08 m and a bumper
would sit at 0.35–0.48 m. **Model it absent.** Rear overhang is factory at
0.809 ± 0.02.

### 2.5 Settled by the verification pass
- **Front indicator: fish-eye / teardrop, correct for a 1963.** Fitted lamp
  measures 71 mm base × 78 mm protrusion, ratio 1.05; a bullet pod is ≈45 mm
  base at ratio ≈2. It only *reads* as a bullet in side elevation. Workshop
  aperture is a round 74 ± 6 mm hole.
- **VW nose roundel is RED in the red livery.** Emblem strokes measure
  R/G = 1.590 against a cream nose at 1.047, with no neutral specular anywhere;
  the workshop chrome reads R/G = 0.974.
- **Counter overhang past the factory bumper line: 0.10 m** (rev 5 said 0.31).

### 2.2 Contested measurements — ALL THREE NOW RESOLVED (kept for the record)
A measurement pass on the high-res photos returned three extraordinary claims.
Each is plausible but would overturn a factory dimension, so each needs
independent re-derivation before it enters the build:
- **RESOLVED — CONFIRMED, but the number was wrong.** Tyres are NOT 6.40-15, but the OD is 0.665 not 0.606; the prior 128 px came from the ground/shadow line, not the tyre edge. The rims are 16". Original: Wheelbase-derived scale (211.2 px/m) and
  tyre-derived scale (187.4 px/m) disagree by 12.7 %, which resolves if the
  tyre OD is ≈0.606 rather than 0.683. Corroborated by a tyre/rim ratio of
  1.39–1.47 measured on the bare rims in `ref_workshop.jpg` against 1.69 stock.
- **RESOLVED — CONFIRMED.** See §2.4. Original: Not visible in either in-service photo. Conflicts with a
  cream rear bumper reported in `ref_workshop.jpg`. It may have been removed
  when the counter wrap was fitted.
- **RESOLVED — REFUTED.** The body is NOT shortened; the scale was right (211.5 ± 1.3 px/m) and 4.06 m is the *current* length with the rear bumper removed. Factory configuration is 4.28. Original: This would mean a shortened body, which
  is a very large claim. More likely the front hub centre — the lower-confidence
  of the two, being occluded by the leaning man — is misplaced. **Re-derive the
  scale from an unoccluded feature before accepting.**

### 2.3 Confirmed additions
- A **rear serving opening** exists in the tail, and the **counter wraps the
  tail** with a 0.313 m overhang and ≈0.30 m outboard projection.
- Overall height measures **1.960** with the lids closed — *above* stock 1.93
  despite the lowering, implying the roof-lid frame stands proud by 0.10–0.15.
- Front indicator aperture in `ref_workshop.jpg` is a plain **round ≈75 mm
  hole**. Lens type remains **U** — neither bullet base nor fish-eye oval
  confirmed.

---

## 3. Livery — FROZEN

| Element | Specification | Grade |
|---|---|---|
| Upper body + roof | sun-bleached off-white, near-neutral. Measured (206, 208, 200) sRGB in full sun | **M** |
| Lower body | faded **orange-red / vermillion**, measured (196, 106, 36) sRGB in full sun — hue ≈ 26°. **Not** a deep crimson | **M** |
| Break | belt line, sweeping down across the nose into the T1 **V-swage**: apex low **on the centreline**, arms **rising** to the belt at the corners. The light colour forms a **downward wedge** down the nose centre; the **red occupies the two outboard lower zones and contains both headlamps** | **M** + **S** |
| Folk art | **gold + yellow + white + dark-red** Mexican folk-art florals over the **red only**. **Density graded** — dense bouquet on the nose flanks and rear quarter, trailing vine along the belt, sparse under the script | **M** |
| Side script | **"Señor Tacombi"**, **SILVER** with a dark keyline and drop shadow, two-line lockup (small "Señor" raised over large "Tacombi"), capital **T an ornate swash**; decorative spirals inside the counters of a/c/o/m/b | **R** (text/colour also **S**) |
| Rear-corner decal | **"100% Calidad"** — white slanted type on a **red-to-orange spiky sunburst**, on **solid cream sheet metal** aft of bay 3, with a small pink star to its left | **M** (position) + **R** (content) |
| VW nose roundel | painted **RED on the cream nose**, **V above W**, pressed relief not chrome. ⌀ ≈ 0.370, centre z ≈ 1.130 | **M** + **E** |
| Wheels | **BLACKWALL** tyres; **cream/off-white painted steel rims**; **red domed hubcaps** with a **light VW** in the centre | **M** |
| Bumpers | **painted cream**, front and rear, stock blade section, **two vertical overriders each** | **M** + **S** |
| Bright work | headlamp bezels read **warm/brass**, not bright chrome. Drip rail, handles, mirror: dulled | **R** |
| Indicators | **flat oval "fish-eye"** lenses in a rim, above and slightly outboard of each headlamp, standing proud. **Bullet pods are period-wrong for 1963** | **S** |
| Finish | **WEATHERED** — chalky, sun-faded, uneven, chipped edges, dusty lower body. Locked by user decision 2026-08-08 | user |

---

## 4. Detail inventory — must all be present

**Stock 1963 T1 (S/E):** roof peak vent over the windscreen · two bottom-pivot
wipers · **10 rear-quarter air-intake louvres per side** (10th added March
1963) · **fuel filler flap on the RIGHT rear quarter, immediately aft of the
louvres** · small rear hatch + small window · oval tail lamps · rear number
plate on the engine lid with lamp above · engine lid T-handle · drip rail full
length · ice-pick cab handles · driver's-side mirror · bumper overriders.

**Tacombi-specific (R — unverified by me, model but flag):** white bobble /
ball-fringe trim round each serving aperture · printed menu cards on the
pillars between apertures · string of small bulbs along the drip rail · brass
edge strip on the counter lip · radiused counter tail overhanging the body ·
chrome number-plate surround on the engine lid reading **"1963"**, empty ·
underside of the raised roof lid painted with flowers and menu strips
(only visible if the lid is ever modelled open).

---

## 5. Mesh & texture quality bar

- Watertight, manifold body shell. No floating or intersecting artifacts.
- Crisp, regular quad topology on the shell; no n-gon pinching on the nose.
- Sharp colour boundaries (procedural, resolution-independent).
- Decals 3K-4K, **non-overlapping**, correctly oriented, correct handedness.

## 6. Render — FROZEN

Cycles CPU + OpenImageDenoise. White seamless studio, shadow-catcher
composited to **pure white** with a soft contact shadow. Large soft sources
only. Interior fill required so the serving hatches read as depth, not holes.
**Hero stills, not turntables.** Final ≥ **2400 × 1600**.

Deliverables: 3/4 front-left hero (reference angle), 3/4 rear-left, 3/4
front-right, ortho side / front / rear, nose detail, low 3/4.

---

## 7. Do not mix references

Tacombi has used more than one bus. The **Nolita / New York** bus has **no
folk art**, **no side script**, **glazed** apertures with gold frames and
hand-painted menu names, a **chalkboard** roof board, a narrow shelf counter,
and "251 ELIZABETH STREET / NUEVA YORK" on the rear corner. **Any photograph
showing those features is the wrong bus.** Whether it is physically the same
vehicle is **U**.

---

## 8. Measurement provenance (reproducible)

**8.1 Blackwall + cream rim, not whitewall.** Radial colour profile about the
front hub at px (114.5, 160.5), clean sector 185–265°: r 0–7 px strongly red
(sat 0.70–0.83) = hubcap; r 7–10 px luminance **rises** to 169 while
saturation **falls** to 0.27 = pale annulus; r 12–17 px dark (lum 34–93, sat
< 0.08) = tyre. **There is no dark rubber between the hubcap and the pale
annulus.** A whitewall requires black sidewall inboard of the white band.
Therefore the pale annulus is the painted rim.

**8.2 Cream bumper.** Bumper blade (193, 175, 169) sat 0.13 vs roof cream
(206, 208, 200) sat 0.04 and rear panel cream (189, 176, 171) sat 0.10 —
same family. Chrome in open sun would split into a bright sky band and a dark
ground band, not a flat mid-tone.

**8.3 Red roundel.** Ring arc (155, 114, 105) sat 0.32; interior/strokes
(177, 115, 107) sat 0.40 — a 60-unit R-over-G bias. Cream nose is sat 0.01;
clean red is sat 0.82. A neutral shadow would hold R ≈ G ≈ B. The roundel is a
faded red.

**8.4 Three apertures, then sheet metal.** Column luminance minima in the
window band: cab window lum 131.5, then dark openings at px x 137–158,
163–180, 185–202, then a **bright** region x 205–228 at lum 178–204 matching
cream, carrying a pink/red decal blob. Bay darkness 61.6 / 71.6 / 106.4 vs the
cab window's 131.5 supports open apertures over glass.

**8.5 Painted counter, not timber.** Counter top (212, 208, 197) **sat 0.07**;
fascia (187, 179, 170) sat 0.09. Natural timber sits at sat 0.25–0.45 with a
strong R > G > B ramp.

**Sources (S):** tacombi.com/our-story · totalfood.com/dario-wolos-tacombi-qa
· cnbc.com 2023-01-09 · 1963 VW factory brochures via thesamba.com archives ·
coolairvw.co.uk splitscreen production changes · type2.com tyre FAQ.

---

## 9. Regression guards (verify.py)

1. L / W / H outside §2 tolerance → FAIL
2. Wheelbase, track and tyre diameter **measured from geometry** off spec → FAIL
3. Any object named `*bed* *gate* *canopy* *fascia* *post*` → FAIL
4. **Exactly three** open serving apertures on +Y, **verified by ray-testing the
   shell**, not by counting panes → FAIL
5. **No** fourth bay aperture and **no** `glass_bay3_*` object → FAIL
6. Missing materials: paint, cream, chrome, glass, wheel cream, silver script,
   calidad decal → FAIL
7. Body top below 1.90 anywhere aft of x = −1.60 → FAIL
8. Non-manifold body shell → **FAIL** (was a warning; SPEC always said FAIL)
9. Any cutter in `FAILED_CUTS` → FAIL
10. `RIDE_DROP` ≠ 0 → FAIL

---

### 10.11 The ground-line datum carries a common-mode error — do not place from it

`REF_MEASUREMENTS.md` §0.3 puts the ground line in `ref_side.jpg` at **y = 670
± 2 px**. Three features placed from it all land low against a model SPEC
independently locks:

| feature | placed from y = 670 | model / SPEC | delta |
|---|---|---|---|
| script ink, z extent | 0.383 → 0.851 | 0.4453 → 0.9177 | **−62 mm** |
| Calidad decal, z extent | 1.376 → 1.721 | 1.4200 → 1.8000 | **−64 mm** |
| belt paint break @ the script station | 1.152 | 1.2315 (`z_belt(x)`) | **−79 mm** |

Three independent features disagreeing with one method **by the same amount and
the same sign** locates the error in the datum, not in three separate
placements — a ground line at y ≈ 683 reconciles all three to within 6 mm. The
±2 px band (±9 mm) does not cover a 13–15 px error.

**Consequence, and it is a rule, not a note: never set a vertical position from
the ground line.** Set it from the belt, which is locked and measured, or from
a vertical EXTENT — a difference, in which any common-mode datum offset
cancels. The rev 9 art pass moved the Calidad decal horizontally by 198 mm and
deliberately moved **nothing** vertically for this reason.

Not resolved: whether y = 670 is itself wrong or whether the px/m scale drifts
with it. Resolving it needs a feature of known height touching the ground in
`ref_side.jpg`, unoccluded. The wheel/ground contact is the obvious candidate
and a man stands in front of the front wheel.

### 10.12 Flank hue — the locked RED came off the retired thumbnail

**Locked:** `RED` = sRGB **(196, 49, 36)**, hue 5.0, saturation 0.816.
**Was:** sRGB (196, 106, 36), hue 26.2, from the 246×197 thumbnail.
Revert with `T1_RED=196,106,36`.

This does **not** re-open §10.9. That section settled the *saturation* question
— 0.816 is an albedo number, no beauty pixel of a dielectric under a white
softbox reaches it, and "raise the flank saturation to 0.816" stays rejected.
Saturation is unchanged here. The claim is about **hue**, which §10.9 never
tested against the reference.

Three lines, each independent:

1. **The rig cannot be the cause.** §10.9's own decomposition is a *neutral*
   additive specular term `A`. The ratio `(G−B)/(R−B)` is invariant under
   adding a constant to all three channels — `(G+A−B−A)/(R+A−B−A)` — so `A`
   moves saturation and leaves hue exactly where it was. A hue error is
   therefore in the albedo, by construction.
2. **Measured on the high-resolution photograph.** Clean red-flank patches in
   `ref_side.jpg`, pooled n = 5218, median (168, 25, 8), hue 6.4. In the
   least-lit patches — least contaminated by warm bounce — hue **4.0–4.3**,
   ratio 0.067. Patches under strong warm bounce read hue 19–23; that bounce is
   not neutral (G lifts to 59–67 while B stays at 5–7), which is what a
   non-neutral additive does and is exactly why the deep-shade patches are the
   ones to trust. White balance checked on well-lit cream: (236, 229, 227),
   R−B +9.
3. **The old value is the folk art.** Locked RED's ratio is 0.438. The
   reference GOLD folk-art motif (audit livery-8, (190,118,59)) is **0.450** —
   they agree to 2.9 %. On a 246×197 thumbnail the flank is ~100 px wide and
   the gold motifs cover a large fraction of it. That is what a contaminated
   average looks like, and it explains why a "red" measured hue 26.

A/B at `out/hue_ab.png`, Playa scene, one variable.

### 10.13 The Playa rig was never showing its environment

Three defects, compounding, all fixed in rev 9. Any one of them alone would
have made the scene unusable and the first two made the third invisible.

1. **The film was keyed and composited on white.** `render_set(transparent=True)`
   runs `composite_on_white()`. `ground_playa()` renders — it is not a shadow
   catcher — but the WORLD does not, so every Playa frame came back with a
   blown white sky and a hard horizon. `build.py` now passes
   `transparent=(scene != "playa")`.
2. **The world ramp was keyed in the wrong space.** A world shader's
   `Generated` coordinate is the **view vector**: Z runs −1…1. The ramp stops
   sat at 0.36/0.72 in 0…1, so every direction at or below the horizon clamped
   to the bottom stop and the background rendered as one flat colour even once
   (1) was fixed. Remapped −1…1 → 0…1 so 0.5 *is* the horizon.
3. **It was lit for a scene that had no sky.** With the world finally reaching
   pixels: three ramp stops (limestone bounce / haze band / tropical sky) not
   two, strength 0.42 → 1.30, sun 3.05 → 4.70 — 3.05 read as overcast once
   there was a sky to read it against — and paving on two noise scales, one
   slow for patch colour and one fast for surface, because at eye height a
   single octave at 5.5 was flat grey mud.

Still not a sunset postcard. The horizon band is warm-pale, not orange:
`SKEPTIC_PASS.md` §B5 is explicit that neither in-service photograph is in
direct sun, so an orange grade would be a different lie from a white one.

### 10.14 Strip rendering: abutting strips seam, overlapping strips do not

The strip machinery was committed in rev 8 and had never been run end to end.
Run exactly as prescribed — four abutting `T1_BORDER` strips, `T1_FX=0`,
`post.py` once on the stitch — it produces a **measurable seam**.

Method: render the same 1200×800 `hero34f` frame single-pass as ground truth
and diff. Frame-wide per-row error **0.090 DN**; at the three seam rows
**0.657 / 2.254 / 0.991 DN**, z = **+5.19 / +19.36 / +8.15** above the frame's
own Monte-Carlo floor. 47 pixels over 20 DN within one row of a seam against 18
in the entire rest of the frame.

Cause is **not** mainly the reconstruction filter (`filter_width` 1.50 px).
Cycles denoising is on, and OpenImageDenoise's receptive field is tens of
pixels, so a band edge is denoised against neighbours that do not exist. A 2 px
filter margin would have fixed the small cause and left the large one.

Fix (`hero.py`): render each strip with **PAD = 48 px** of overlap on each side
and copy only the rows the strip owns. Re-measured against the same reference:
seam z **−0.27 / +2.22 / +0.71**, pixels over 20 DN near a seam **47 → 0**,
frame mean error 0.090 → 0.036 DN. `post.py` applied once to the stitch adds no
banding (seam z ≤ 1.75).

`stitch.py` takes the band mapping as a **declared argument**, never inferred:
with the white composite an unrendered region and a rendered backdrop row are
byte-identical (measured max |diff| = 0 over a full backdrop row), so content
detection cannot find a band edge — a wrong row mapping would survive a test
frame and appear only on the hero.


### 10.15 `ref_rear34.jpg` is mis-identified — treat every number from it as suspect

Donald, 2026-08-10, looking at a 6x crop of the lettered cream panel in
`ref_rear34.jpg`: **"That is also the front end of the bus open towards the
front. What we are looking at is the inside of the front panel."**

The file name, and every crop attributed to it in this document and in
`REF_MEASUREMENTS.md`, assumes a rear three-quarter view. The person who has
stood in the vehicle says it is the front, with the roof opening **forward**
and the lettering on the **underside of the front panel**.

Affected, and unverified as of rev 9:

| item | crop | state before this note |
|---|---|---|
| flank paisley (§10.10 item 2) | (620,560)-(1200,820) | marked **done** |
| rear-lid lettering (§10.10 item 7) | (700,20)-(1050,300) | placeholder |
| "1963" plate surround (§10.10 item 8) | (1330,780)-(1500,860) | modelled |
| roof topology: main lid + smaller aft lid | -- | built, SPEC sec.1 |

**Rule: do not carry a number derived from `ref_rear34.jpg` forward until the
view is re-established with Donald.** More generally -- ask what a supplied
photograph shows before measuring from it. Three revisions of geometry rested
on an assumption nobody had put to him, and the check cost one crop and one
question.


### 10.16 The script's keyline and drop shadow are not measurable

SPEC sec.3 states the side script carries a dark keyline and a drop shadow.
Sampling outward from the ink edge in `ref_side.jpg` does not support it at
this resolution:

| distance outside the ink | mean luma |
|---|---|
| +1 px | 80.5 |
| +2 px | 63.1 |
| +3 px | 61.7 |
| open ground, +5-6 px | 58.7 |

A monotone decay toward ground with no dark ring at any radius -- that is edge
blur, not a keyline. Either establish it from a higher-resolution photograph or
retire the claim. **Do not add a keyline to the generator because sec.3 says
so**; that is the same error as building from the thumbnail.

What the same sampling DOES establish: the silver is **not flat**. Ink
per-channel std is 16-19 and luma spans 85-135 at p5-p95. `tex/senor.png`
currently emits a constant (214, 216, 218) with all shape in alpha, and at hero
scale that flatness is probably a larger fidelity loss than any single glyph
outline error.


### 10.17 The acceptance criterion is per-measurement, not on average

Donald, 2026-08-10: **"I want a big reminder that the final product should be
nearly indistinguishable from the original. Any single measurement off is
unacceptable."** And: **"we are recreating a photo realistic version of that
exact bus."**

Recorded here because it governs how every other section of this document is
read. A model right in ninety places and wrong in one is not 99 % done. There
is no averaging and no trading one dimension against another.

### 10.18 Front fascia — open drift, all of it previously logged and unapplied

Raised by Donald 2026-08-10: "the front fascia is starting to drift". Front
references are `ref_workshop.jpg`, the (60,330)-(330,700) region of
`ref_side.jpg`, and `ref_rear34.jpg` (a FRONT view, see 10.15, never used as
one).

| # | item | source | status |
|---|---|---|---|
| 1 | cab-door and lower-nose folk art far too faint and sparse -- the photograph shows bold yellow acanthus, heavy dark outlined curlwork and rows of white rosettes at high contrast | `ref_side.jpg` front crop | NEW |
| 2 | headlamp bezels read gold/brass, model assigns `chrome` | same crop | audit `materials-6`, open |
| 3 | VW roundel 9 % undersized, centre 32 mm high | `ref_workshop.jpg` | audit `livery-9`, open |
| 4 | transverse roof dome absent: +83 mm/side too wide at z 1.53, +203 mm/side at z 1.85 | factory section | audit `geometry-4`, open |
| 5 | indicators wrong type and 20 mm inboard | REF sec.V6 | audit `inventory-9`, open |
| 6 | front bumper reads thin against a deep chunky cream blade | both front refs | NEW, unmeasured |

Item 1 also **contradicts 10.9's** measured "0.0-0.2 % gold coverage from
X +1.47 to -0.40". That band covers the cab door and the photograph shows it
densely painted. The cab door is OPEN in `ref_side.jpg` (SKEPTIC B2), so a
coverage scan indexed by body x sampled the wrong surface. **Re-measure before
trusting 10.9's density lobes near the nose.**

The fascia did not drift because anything was changed. It drifted because the
rest of the vehicle advanced through rev 8 and rev 9 and the front did not:
items 2-5 have been logged and unapplied for several revisions.


### 10.19 `ref_rear34.jpg` — the view, settled with the owner 2026-08-10

SPEC 10.15 quarantined every number derived from this photograph because the
frame had been treated as a rear three-quarter and Donald had then said, of a
crop of the lettered cream panel, "that is also the front end of the bus open
towards the front". Put to him directly with marked crops, the answer resolves
both readings and they are not in conflict:

| region | what it is |
|---|---|
| near end, right of frame (x >= ~930) | the **TAIL** — engine lid, chrome-framed "1963" plate, oval amber tail lamp with chrome bezel, chrome T-handle |
| cream panel lettered in red script with a red star (x 555-860, y 5-215) | the **UNDERSIDE OF THE LID OVER THE FRONT** — the roof lids open FORWARD |
| counter overhang | past the **tail only**, as SPEC already had it |

So the FRAME is a rear three-quarter and the LIDS open forward. Numbers
attributed to the near end are correctly attributed to the tail and are
released from quarantine. Numbers that treated the lettered panel as a REAR
lid are wrong and are re-attributed to the front lid.

**The quarantine is lifted for: the "1963" plate surround, the flank paisley
source crops, and the tail-end topology. It stands for: the lettered panel's
placement.**

### 10.20 The script's reference mask was dropping 14 % of the ink

The rev-9 reference segmentation was `sat < 0.36 & 55 < max < 228`. That finds
untarnished silver and nothing else, and the ink is not all untarnished.

| | px |
|---|---|
| rev-9 segmentation | 7 982 |
| rev-10, silver rule alone | 8 006 (agrees to 0.3 % — the rule was fine) |
| tarnish zones add | +1 123 |
| **true ink footprint** | **9 129 +/- 300** |

Two recorded "generator defects" were artefacts of the wrong target:

* `Senor` scored 0.089 and was written off as unfittable. It is not: the word
  is invisible in LUMA (Michelson 0.132) but obvious in CHROMATICITY — the red
  ground carries B = 6.0 +/- 3.6 DN and the word carries B = 21-81.
* The lockup was recorded as running **8 % heavy**. Against the true footprint
  it runs **6 % LIGHT**. The rev-9 handoff prescribed thinning it globally.

The mask rule is now the measured one and lives in `compare_script.py`: `T` is
the redness of a 50 %-area optical mix of the ink and ground endmembers, mixed
in LINEAR light and re-encoded. That is the geometrically correct mask edge —
the locus where a pixel is half covered by paint. The gamma encoding makes the
mapping strongly non-linear (25 % coverage sits at r = 0.275), so a naive
midpoint threshold is badly wrong. Tarnished ink is a different endmember and
its four measured zones each carry their own threshold.

**The comparison window also clipped the reference.** It ran y 486-599 while
the ink runs 474-588 — twelve rows of real ink, the top of `Senor`, were
outside the test entirely, and the generated lockup was 99 px tall against a
reference 114 px. The canvas now carries a 16-row pad above y = 0.

### 10.21 The silver, and one error made and corrected inside rev 10

Measured on untarnished, PSF-safe stroke interiors:

| quantity | measured |
|---|---|
| clean silver | (127.4, 124.9, 130.0), std (7.4, 8.5, 9.0) |
| genuine mottle | **7.4 DN** against a 1.5 DN imaging noise floor |
| mottle structure | **no dominant period**; correlation length 13-16 px along the stroke against 3.5-5.0 px across (z = +6.5 at 150 deg against an isotropic null) |
| edge concentration | **none** — r = +0.086 once the 2.07 px PSF ring is excluded |
| tarnish hue | **WARM**, not green-black: darkest quartile a\* +14.0 against lightest +6.9 |
| `Senor` vs clean silver | median (85, 46, 35) against (126, 123, 127) = (0.675, 0.374, 0.276) |
| thick/thin ratio | swash 3.61, b 3.50, o 2.92, c 2.69, a 2.41, i 1.68, m 1.60, T 1.26 |

**The error, kept because the reasoning is the trap.** The first attempt read
"the silver sits at 0.293 of the cream's linear luminance in ref_side.jpg" and
set the ALBEDO to 0.293 x CREAM. It rendered as dull blue-grey paint. That
0.293 is a ratio of RENDERED values between a near-mirror METAL and a diffuse
dielectric, and those do not scale together when the environment changes. The
leaf is dark in the reference BECAUSE the reference is open shade under an
absorbing canopy. Under a white softbox the same leaf is bright, and that is
not an error — it is what a photograph of the real vehicle in a white studio
would show.

**Rule, generalising SPEC 10.12: a rendered ratio is only an albedo ratio
between two surfaces of the SAME class under the SAME light.**

### 10.22 Front fascia — three findings applied, two refuted, one not measurable

| finding | verdict | action |
|---|---|---|
| `materials-6` bezels are brass not chrome | **CONFIRMED** — bezel b\* +31.6 at L\* 65.6 against five neutrals in the same frame at b\* -2.4...+1.6; not a bounce (every warm surface there carries a\* with its b\*; the bezel's ratio is 0.07) | applied |
| `livery-9` roundel 9 % undersized, 32 mm high | **REFUTED, and it had been applied in the wrong direction.** Measured **0.280 +/- 0.030 m** by an exact relation needing no camera pose; centre **0.149 +/- 0.030 m BELOW the belt**. The build read `ROUNDEL_D = 0.3700` — 32 % over — and the finding's only photographic support was `ref_source.jpeg`, retired in 0.2 | corrected to 0.280, and **113 mm down** |
| `geometry-4` roof dome +83/+203 mm per side | **NOT MEASURABLE** — no elevation exists in the admissible set; in `ref_workshop` the camera sits at 1.93 m against a ~1.9 m crown so the roof's upper boundary is a tangent locus, not a section; and the lids are open in both usable frames, so the surface the finding describes is physically absent | NOT applied. The blueprint was not passed through |
| `inventory-9` indicators 20 mm inboard | position **CONFIRMED but 7x understated**: measured **0.130 +/- 0.035 m OUTBOARD**. The proposed flat-oval lens is **REFUTED** — the existing bullet is closer to the photograph | Y moved outboard; type kept |
| front bumper reads thin | blade is **already correct** (0.110 +/- 0.010 measured against 0.113 built; blade/wheel 0.166 +/- 0.016 in two frames agreeing to 2 %) | see 10.24 |

### 10.23 The Playa rig described four things the photograph does not contain

| removed | why |
|---|---|
| the sun | brightest ground patches are **+5 L\*** over surround with **7.4 px** edges, and the bright/dark ground split measures **db\* +2.4** — the SHADOWS ARE WARMER, which is the opposite sign to a sun/skylight pair |
| the dapple gobo | same evidence. rev 9 added it to honour a docstring; the docstring was wrong |
| the sky | the world ramp topped out at (0.286, 0.452, 0.720) at strength 1.30. There is no sky in frame |
| the haze band | aerial perspective measures **zero** — canopy shadow floor holds at Y p5 = 0.014-0.019 across the full depth range, airlight bound dY < 0.004 |

And **there is no papel picado.** The band across the top of the reference is a
continuous flowering mass — 55.1 % foliage, 13.4 % crimson heads, 5.5 % cream
florets, jagged interpenetrating lower edge, no flag silhouettes. Bunting in
that render would be an invention.

What IS there: ONE large low LATERAL source under an absorbing ceiling.
Signature — the same red reads **3.95 : 1** between the flank facing the
opening and the tail face 72 deg away; the palm trunk runs **12.5 : 1** across
its own diameter; and an up-facing cream surface is DARKER than a vertical one
facing the opening (0.93 : 1) while brighter than one turned away (1.87 : 1).
The rig reproduces 4.00 / 1.91 / 0.787 against measured 3.95 / 1.87 / 0.772,
and the last of those was never fitted to.

**Absolute level is set by the FILM, not by the photograph.** The rig was
solved in scene-linear at cream = 0.787; this pipeline runs AgX + Punchy under
which the studio's paper white sits at linear 21.0 (SPEC 10.8), so the solved
rig lands ~5.6 stops down. `T1_KEY_PLAYA` scales the whole rig together so the
solved ratios are untouched.

### 10.24 OPEN — three things measured, applied, and then reverted

Each was applied from a measurement, broke something that is independently
locked, and was reverted rather than laundered. None is closed.

1. **Front bumper standoff.** Measured ">= 0.080 m from the body against
   0.032 m built". Applied, it put the blade **63 mm PROUD of the nose crown**
   and took the overall length to 4.327 against the locked 4.290 — `verify.py`
   failed it, correctly. A third method, the frontal silhouette of
   `ref_side.jpg` scanned row by row for the left-most vehicle column, puts the
   **nose crown at column 78 and the bumper face at 82-91** — the bumper is
   17-56 mm BEHIND the crown. Most likely the two figures use different datums
   (the tucked apron at bumper height versus the forward-most nose).
2. **Indicator lens depth.** Measured ~65 mm proud against 41.5 mm built.
   The same silhouette puts the indicator's front face at column 80 against the
   crown's 78 — ~9 mm behind. If the 65 mm is right, the fix is the pod's
   MOUNTING STATION, not its depth.
3. **Headlamp vertical position.** The same pass gives headlamp centre =
   belt - 0.339 +/- 0.025 m, against the build's belt - 0.242 — a 97 mm
   discrepancy at ~3.9 sigma. NOT applied: it is a single-chain claim that
   moves the face of the vehicle, and it deserves a second derivation first.

### 10.25 The VW glyph merged into an X again, by a new route

`SKEPTIC_PASS` sec.D fixed this in rev 8 by rebuilding the emblem as two closed
mitred prisms. It returned in rev 10 for a different reason: `vw_logo`'s R and
w were ABSOLUTE (0.1385 / 0.0275), tuned against the then-locked ring diameter
of 0.370, while the ring is driven by `ROUNDEL_D`. Correcting `ROUNDEL_D` to
the measured 0.280 shrank the ring 24 % and left the glyph at its old size, so
the designed 12.7 mm air gap between the V's apex and the W's peak closed.

Nothing about the glyph code was wrong. **The coupling was missing.** The two
are now tied: glyph R = 0.7486 of the ring's outer radius, bar width = 0.1986
of that R — the rev-8 proportions, which hold the arms 12.29 deg apart with
clear air between them at ANY diameter.

*Lesson worth keeping: a constant tuned against another constant must be
expressed in terms of it, or correcting one silently breaks the other.*


### 10.26 The roof topology — settled by the owner, and 10.19 is corrected

10.19 recorded "the roof lids open FORWARD". That is **refuted**. Donald was shown
marked crops of both in-service frames and identified each panel, and then made
the observation that resolves everything:

> "the separate roof panel that we see in the playa photo is still closed on the
> side ref photo"

| panel | `ref_side.jpg` | `ref_rear34.jpg` | artwork |
|---|---|---|---|
| **front lid** | **CLOSED**, flat in the roof | **OPEN** | cream underside, red brush script + red star |
| **main / mid lid** | OPEN | OPEN, seen from behind, aft of the cream one | flower mural + three yellow menu strips |
| **trunk lid** | **OPEN**, at the tail | closed | none |

His words on the motion: there are two roof lids, front and back, "inward facing";
the roof lid opens toward the **passengers' side**; the front one lifts toward the
**driver's side**; the back may lift toward the rear.

**Corroborated by a measurement made without knowledge of any of this.** The open
lid in `ref_side.jpg` has a long axis of **426 px = 2.0 m** at 211 px/m. On a
1.75 m body that is only possible **fore-aft**. Its long edges converge on the
vehicle's own fore-aft vanishing point (-10509, 733), which predicts a bulb-string
slope of **-0.03806** against a measured **-0.03877 +/- 0.002**.

**The code was already right and the prose was wrong.** `t1_shell.roof_lids()`
hinges both lids about a fore-aft axis at `LID_Y_HINGE` and swings them sideways.
Nothing in the build ever opened them forward. This is the fourth time in this
project that a claim in prose has disagreed with what the code does; the rule from
10.7 applies -- **if a document says the rig does something, grep for the node that
does it.**

**What is NOT settled**, and must not be guessed:
* Whether the front lid is forward of `LID_X0` (+0.964). 10.9 measured the cab roof
  dome as unbroken to X +0.964, which leaves no room forward of the main lid. So
  either 10.9's dome measurement or the front lid's station is wrong.
* Whether the mural is on the main lid's own skin or on a board carried by it.
* What the rear lid carries. `ref_rear34` shows a second flowered panel with its
  own yellow strips and food vignettes aft of the cream one; that may be the main
  lid seen from behind, or a third artwork.

### 10.27 The roof hole is never cut, and that is why the galley was black

`build.py` step 3 issues windscreen, side-glazing, serving-bay, rear-window and
panel-gap cutters. **It issues no ROOF cutter.** `t1_shell.roof_lids()` builds the
lids as free panels floating over an unbroken roof skin.

So in the model the galley is a **sealed 2.8 mm steel box**. No exterior source can
physically reach the interior, which is why every attempt to fix the black serving
bays by changing `fill_galley` failed for several revisions -- the light had nowhere
to enter. Measured: the three apertures read 22 / 33 / 24 display luma against the
photograph's 137 / 157 / 175.

rev 11 stands the opening in with an emissive panel at the plane where the hole
physically is, and the bays now read 130 / 160 / 167. **That is a stand-in, not the
fix.** The fix is a roof cutter, and it is real geometry: the opening is
1.11 x 2.03 m, it must be cut AFTER solidify like every other aperture except the
wheel arches (the pipeline order in 10.1 is load-bearing), and it will change the
roof's manifold state, so `verify.py`'s non-manifold count and the shut-line probes
must both be re-run at BOTH subdivision levels.


### 10.28 rev 12 -- the roof hole, and a panel that turned out not to exist

Four readings settled WITH THE OWNER from marked crops, before anything was
measured from them, plus one he volunteered that retired a panel entirely.

| # | question | his answer |
|---|---|---|
| 1 | how much roof is cut, fore-aft | **ONE opening only**, under the flower-mural lid; solid roof forward over the cab and solid aft to the tail |
| 2 | how much roof survives across | **a strip on both sides** -- the 1.11 m transverse width stands |
| 3 | what the cream lettered panel is | first "a separate signboard, not a cut roof lid", then, unprompted: **"I was wrong, I think it is a detached sign"** |
| 4 | what the counter is | **tan top, brass nosing on the OUTER EDGE, body cream below** |

**Why these had to be asked.** `ref_side.jpg` puts the camera at roof height, so
the roof plane is edge-on and the surviving strip between the lid's base and the
near drip rail is ~13 px tall. No transverse number off that frame is worth
anything. `ref_rear34.jpg` is the only frame with elevation on the roof: it shows
maroon interior through the opening -- the first direct sight of the inside of
the hole in any frame -- but neither end of it.

**THE ROOF HOLE IS CUT.** `t1_shell.roof_cutters()`, issued from `build.py` step
3, after solidify, like every aperture except the wheel arches. The opening is
expressed in terms of `LID_X0` / `LID_X1` / `LID_Y_HINGE` / `LID_W`, never as
four fresh constants (10.25), so moving the lid moves the hole. Measured result:

```
cut roof hole: 56446v   worst v-ratio 0.9826 f-ratio 0.9796 vol 2.434e-01   SUB=1
cut roof hole: 207959v  worst v-ratio 0.9790 f-ratio 0.9772 vol 2.434e-01   SUB=2
non-manifold edges 0 ; 0 fail 1 warn at BOTH levels
```

**The guard, `verify.py` 11d2, is two-sided** -- the opening must be OPEN and the
roof must be SOLID everywhere the owner says it is. Nothing asserted a roof
opening for eleven revisions except prose, in this file, in `t1_shell`'s
docstrings and in three handoffs. A claim in prose is not a guard.

**The guard failed first, and both causes were the guard.** Probes placed as
fractions of the opening span landed at |y| = 0.81, off the roof entirely; and
the rays were aimed in the UN-DROPPED frame while `run()` executes AFTER step 8b.
The 0.30 m ray stopped 26 mm above a perfectly solid roof. Re-derived by
ray-casting the built mesh on a 13x9 grid: the residual against `roof_z` came out
as exactly `-rake_drop(x)` at every station, which is the proof it was a FRAME
error and not a geometry error. 10.1 exists for this and it still caught me.

**The detached sign.** Modelled since rev 8 as `lid_rear`, a second hinged lid
over a second opening `build.py` never cut; briefly re-modelled this revision as
a roof-mounted signboard; now emitting nothing. It is not part of this vehicle.
That is also why it never appears in `ref_side.jpg` -- not folded flat, which is
what I had reasoned, simply not there. Geometry kept behind `T1_SIGNBOARD=1`,
which is NOT the default and which no hero may be rendered with. The owner has
revised this one panel three times; if it is revisited, it needs a photograph
that shows its footing, not another inference.

**The counter top is TAN, and `COUNTERTAN` is half-measured -- say so.** Derived
as a ratio against a surface of the SAME CLASS (10.21), in `ref_side.jpg` because
every cream in `ref_rear34.jpg` clips at 249-254 and a clipped reference cannot
carry a ratio. Two references bracket rather than agree, and the disagreement is
structural: the counter fascia (same light, wrong orientation, takes red bounce)
gives albedo G 0.416; the cab roof (right orientation, different local surround)
gives 0.569. Locked at the midpoint 0.493, bracket -16 %/+15 %. **The HUE is
measured; the LEVEL is bracketed.** `T1_CTAN=r,g,b` tests the ends.

**`optics-6` is still OPEN but it is now open with a number.** The previous note
said the contact shadow "dies within 11 mm of the tyre", which implies a shadow
that decays. Measured on a 1400x933 side probe: the ground reads **255.00 at
every row from 3 px below the contact patch outward**, and with the backdrop
forced to linear 1.0 the ground under the tyre reads **177.00 against open ground
at 177.00** -- identical to two decimal places. The shadow does not decay; it is
not there, the catcher writes identically zero alpha. The obvious fix is REFUTED:
rendering the sweep as a real lit surface does put a shadow down (175.2 mean /
161.2 min against 255) but brings back defect D3 in full, a 166 grey sweep with a
hard horizon, and sec.6 locks the backdrop to pure white. `T1_CATCH=0` reproduces
the A/B in one render. Next attempt: ask why the catcher writes no alpha, do not
soften a shadow that does not exist.

**Constant-roughness materials 9 -> 6.** The three the rev-11 galley dressing
added are gone. The surviving six are transmissive or the sealed reflector, which
`STATE.md` names as the only legitimate exemptions -- plus `gal_sky`, argued
rather than claimed, and which should be DELETED now the aperture is real.

## Change log

| Date | Change |
|---|---|
| 2026-08-10 | **rev 12.** The roof hole is CUT -- one opening, settled with the owner, cut after solidify, guarded two-sided by `verify.py` 11d2; non-manifold still 0 and 0 fail / 1 warn at both levels. The galley is no longer a sealed steel box. The cream lettered panel is a DETACHED SIGN and is off the vehicle (10.28). Counter given a measured tan top and its brass nosing re-measured -- it was 1.6x too DEEP, not thin. Weathering: the dust tide line re-fitted to h 0.424 +/- 0.020 and the upward-facing deposit split from the road film, which had been delivering dC* +0.58 against a target of +5.0. Constant-roughness materials 9 -> 6. `optics-6` measured properly and its obvious fix refuted. |
| 2026-08-10 | **rev 11.** Roof topology settled by the owner and 10.19 corrected -- the lids do NOT open forward; the main lid hinges fore-aft and opens to the serving side, corroborated by a vanishing-point fit agreeing with the bulb string to 2 % (10.26). The roof hole is never cut, which is why the galley was black (10.27). Galley dressed and lit: bays 22/33/24 -> 130/160/167 against a measured 137/157/175. Mural un-lifted -- `EXPOSURE = 1.58` was a scalar rev 9 baked into every measured colour; removed, and every palette class now lands within half a point. Flower heads measured at EIGHT petals not twelve; THREE menu strips not four. Folk art recomposed: 84.4 % of the photograph gold sits in three connected masses, rev 10 had 67.9 % in its largest three, rev 11 has 81.0 %. Nose given its own decal -- the flank tile is box-projected and the nose face was sampling the cab door u-band. |
| 2026-08-10 | **rev 10.** Photograph identity settled with the owner (10.19). Script reference mask corrected -- it was dropping 14 % of the ink and two recorded generator defects were artefacts of it (10.20); whole-lockup IoU 0.511 -> 0.942, `Senor` 0.089 -> 0.825. Silver measured and modelled as LEAF, with one albedo-versus-rendered-ratio error made and corrected in flight (10.21). Folk art: `W_ART` 0.30 opacity ceiling retired -- it made the measured x2.048 gold-to-red contrast arithmetically unreachable; cab-door coverage 0.0-0.2 % -> 29.1 %; both flanks de-mirrored (materials-14). Fascia: roundel 0.370 -> 0.280 and 113 mm down, bezels to brass, indicators outboard (10.22). Playa rig: sun, dapple, sky and haze all removed as unsupported; vegetation built and placed by inverting the reference camera (10.23). Three findings reverted and logged OPEN (10.24). VW glyph coupling fixed (10.25). |
| 2026-08-08 | Initial lock. Body corrected from single-cab pickup to Kombi van. |
| 2026-08-08 | Script text corrected to "Señor Tacombi"; capital T must be an ornate swash. |
| 2026-08-08 | Script colour corrected to **silver**. |
| 2026-08-08 | rev 3.2 — modified-bus details locked: whitewall tyres, red domed hubcaps with white VW, low bumpers, proud bullet indicators. |
| 2026-08-08 | rev 3.1 — bus is **lowered**: body dropped 65 mm relative to the wheels. |
| 2026-08-08 | rev 3 — grounded against prior project context. |
| 2026-08-08 | **rev 4 — evidence audit.** Added evidence grades (§0) and measurement provenance (§8). **Corrected against measurement:** whitewall → blackwall + cream rim; chrome → cream bumpers; cream → **red** VW roundel; four bays → **three** + solid rear panel; canvas ragtop → **cut steel lids**; timber → **painted** counter; bullet → **fish-eye** indicators; lowered → **stock** ride height. **Corrected against factory sources:** L 4.280 → 4.290, W 1.720 → 1.750, tyre 5.60-15 → **6.40-15** (dia 0.665 → 0.683), track → 1.369/1.359. Finish changed to **weathered** by user decision. Added §4 detail inventory, §7 wrong-bus warning, §2.1 unresolved belt/sill conflict. Guards extended to 10. |

| 2026-08-08 | **rev 5 — high-resolution photographs supplied by Donald.** Three large photos (workshop/green, side elevation, rear 3/4) supersede the 246x197 thumbnail as primary reference. **Ride height LOWERED reinstated — rev 4 was wrong to zero it; Donald's original reading was correct.** Belt/sill conflict resolved: break sits 100 mm below the sill, not 16. Aperture positions re-measured and are not evenly sized. Rear serving opening and counter tail-wrap added. Three contested measurements quarantined in §2.2 pending independent re-derivation. Full working in REF_MEASUREMENTS.md. |

| 2026-08-08 | **rev 6 — verification pass on the three quarantined claims.** All three resolved by independent methods. Body NOT shortened (factory 4.28 stands; 4.06 is today's length minus the removed rear bumper). Rear bumper genuinely absent in service — model it off. **Tyres are not 6.40-15: OD 0.665 and the rims are 16 inch, not 15** — rev 4's "correction" to the factory 0.683 was wrong and rev 3's 0.665 was right. Rear arch gap corrected 71 → **41 mm**. Indicator settled as fish-eye (period-correct). Roundel settled as RED. Counter overhang corrected 0.31 → 0.10 m. |

---

## 10. rev 7 — the canonical constants (supersedes any value above)

Everything in this section was re-derived from the high-resolution photographs
by an adversarial skeptic pass over the 13 critical findings in
`AUDIT_RECOVERED.md`, and then implemented and verified against the built mesh.
`STATE.md` is regenerated from the live geometry by `audit.py` on every run; if
this table and `STATE.md` disagree, **`STATE.md` is right and the build has
drifted**.

### 10.1 The three frames — get this wrong and everything moves 65 mm

| what | frame | why |
|---|---|---|
| `t1_shell` / `t1_core` / `t1_detail` constants, all outlines | **UN-DROPPED** | `build.py` step 8b subtracts `RIDE_DROP = 0.065` from every vertex last |
| `t1_mats` shader constants (`Z_BELT`, `V_APEX`, `V_RISE`) | **DROPPED = above ground** | a shader reads `Geometry→Position` off the already-dropped mesh at render time |
| `verify.py` | runs **AFTER** the drop | its own header denied this until rev 7; probing a 5.5 mm shut line in the wrong frame read 26 % open instead of 100 % |

Proved by measurement, not assumed: the painted break lands at z = 1.3859
against `Z_BELT` = 1.3860, and the window band reads 1.3070/1.7100 above ground
against `Z_SILL`/`Z_HEAD` = 1.372/1.775 un-dropped.

### 10.2 Two-tone break and nose V-swage — LOCKED

| constant | value | frame | was | error |
|---|---|---|---|---|
| `Z_SILL` | **1.372** | un-dropped (1.307 AG) | 1.4020 | +27 mm |
| `Z_HEAD` | **1.775** | un-dropped (1.710 AG) | 1.7980 | +25 mm |
| `Z_BELT` | **1.207** | above ground | 1.3860 | **+111 mm** |
| `V_APEX` | **0.340** | above ground | 0.8720 | **+476 mm** |
| `V_RISE` | **0.867** | = `Z_BELT − V_APEX` | 0.5140 | — |
| `V_POW` | **0.60** | — | 1.16 | profile is concave, not convex |

`V_APEX ≤ 0.396 un-dropped` is a **hard bound, not an estimate**: the cream
wedge is still 14 px wide where the bumper occludes it in `ref_workshop.jpg`,
and the bumper top measures 0.331 ± 0.020 AG. Independent of any px/m scale.

The audit's proposed replacements — belt 1.240 and apex 0.620 — are **both
wrong** (32 mm low and 224 mm high respectively) and both rest on a **Samba**
blueprint or the retired 246×197 thumbnail. See `SKEPTIC_PASS.md`.

**Do not derive the belt from `sill − 100 mm` using the model's own sill.**
That is a restatement of two measurements, not a physical law; feeding the
model's sill into it launders the sill's own error into the belt. Set each from
its own measurement and let the 100 mm fall out as a *check*.

Mirror `V_APEX`/`V_RISE`/`V_POW` into `t1_shell.nose_shape.zV` whenever they
change, or the pressed swage and the painted break de-register. Verified: they
register to **0.0 mm**.

### 10.3 Livery colour — rev-3 shipped a retired reading

| | linear albedo | = sRGB | hue | sat |
|---|---|---|---|---|
| `RED` **locked** | **(0.5520, 0.1441, 0.0176)** | (196, 106, 36) | 26.3° | 0.816 |
| `RED` rev-3 shipped | (0.5250, 0.0395, 0.0072) | (192, 56, 20) | 12.5° | 0.894 |
| `CREAM` **locked** | **(0.6172, 0.6308, 0.5776)** | (206, 208, 200) | 75.0° | 0.038 |
| `CREAM` rev-3 shipped | (0.7900, 0.7700, 0.7150) | (230, 227, 220) | 44.2° | 0.043 |

rev-3's `RED` had its **green channel 3.6× too low**, making it a **deep
crimson** — which §0.2 retires *by name* ("**Not** a deep crimson"). The
retired reading survived in code for four revisions because nobody converted
§3's own measured sRGB back to linear. rev-3's `CREAM` also had R > G where the
measurement has G > R.

**Folk art is a graded bouquet, not wallpaper.** The density mask ran at the
tile's own alpha in its dense regions, covering the red almost completely and
dragging the measured flank from sat 0.816 to **0.27**. Locked: opacity ceiling
`W_ART = 0.30`.

### 10.4 Weathering — measured targets, not adjectives

| target | value | source |
|---|---|---|
| cream local luminance variation @ 25 / 100 / 400 mm | 4.22 / 7.26 / 10.54 % RMS | `ref_side.jpg` |
| dust tide line | knee **h = 0.40 ± 0.04 m**, full ≤ 0.30, zero by 0.48 | CIELAB `C*/(L*+16)` |
| flank above 0.40 m | **clean** — chroma ratio flat to ±7 % up to 0.92 m | same |
| upward-facing dirt | ΔL\* −8.8, ΔC\* +5.0, Δhue −6.6° toward ochre | `ref_rear34.jpg` |
| edge-wear Pointiness window | **0.520 → 0.600** (flat flank reads 0.500–0.503) | emission bake |

The intuitive `smoothstep(0.75 → 0.25)` dust ramp is **~3× too tall** and would
dust a band the reference shows clean. Sun fade is a **design value, not a
measurement** — neither in-service photograph is in direct sun, so fade cannot
be separated from exposure. **No subsurface scattering anywhere**; nothing on
this vehicle is translucent.

### 10.5 Geometry added or corrected in rev 7

| item | locked value (un-dropped unless noted) |
|---|---|
| serving aperture edges | (+0.820, +0.313) (+0.195, −0.321) (−0.435, −0.960); widths 0.507 / 0.516 / 0.525 — **not** three equal 0.600s |
| louvres | 10 per side, x −1.285 → −1.670, pitch 21.1 mm, top slot 1.085, bottom 0.895, built horizontal |
| counter | X0 +0.918, X1 **−2.423**, Z 1.147–1.254, thickness 0.107, Y_out 1.166, tail wrap quarter-arc R 0.150, front chamfer 45° × 0.05 |
| cab-door gap bottom run | **z ≥ 0.780** — must clear the front arch top at 0.771 |
| script decal | X +0.784 → −0.494, Z 0.445 → 0.918; `senor.png` recropped to its ink bbox (AR 2.702) |
| VW roundel | ring ⌀0.370, centre 1.130 AG |
| wipers | translated ≥ +0.025 m along `WS_N`; blade built in the windscreen plane; pivot axis on the cowl normal |

### 10.6 Guards — strengthened, never removed

The rollback guard's `after < before * 0.6` could not detect anything short of
total destruction: worst legitimate ratio is **0.9902** (SUB=1) / **0.9862**
(SUB=2), so a cutter could delete 39 % of the shell and pass. A **no-op**
boolean passed silently. The obvious digest **does not work** — EXACT
re-tessellates n-gons even on a true no-op (Δf = +9, spurious ΔVolume
−3.38e−06 m³); **vertex-count equality is the only clean count test.**

Locked: cutter volume ≥ 1e−4 m³ and bbox-overlap pre-checks; vertex and face
ratios ≥ 0.95; Δv ≠ 0; non-manifold / loose-vert / zero-area must not increase
(zero-area threshold 1e−12 m², because a cutter plane coincident with a subsurf
edge loop legitimately emits 5–20 µm slivers); per-kind sign tests. Validated
against all 44 measured (cutter, level) rows: **2 true positives, 0 false
positives.** Four negative controls fire that the old guard passed.

Positive assertions added: each expected aperture and shut line must actually
exist; `calidad_L`'s material must have Transmission Weight 0; Subsurface
Weight must be 0 scene-wide; **no detail object may be invisible from every
hero camera** (both wipers shipped buried in the nose skin for six revisions).

**The `≥ 20 mm clear of roll-over` rule is REFUTED and replaced.** Causal test:
skip the wheel-arch cutters and the identical door-gap cutter at the identical
z succeeds at SUB=2. The real rule: *a panel-gap outline must not cross the lip
of another aperture, and where it runs near a roll the outer-skin slope
relative to the cutter's extrusion axis must stay below `t_skin / gap_width`*
(0.51 at 2.8 / 5.5 mm).

### 10.7 Known open defects — logged, not fixed

| defect | measured | note |
|---|---|---|
| **overall height 89 mm short** | model **1.871**, `REF_MEASUREMENTS` §2.3 measures **1.960** with the lids closed | the roof-lid frame stands proud by 0.10–0.15 m and is not modelled. This is why the vehicle reads flat and stretched. |
| **tail 99 mm long** | model −2.108, measured −2.007, factory arithmetic −2.009 | fixing it is a loft change; the counter's X1 was set to preserve the *measured* 0.316 m overhang relative to the model's own tail |
| nose-down rake ~1.7° | not modelled | `Z_BELT` becomes a line, not a constant, when it is |
| script ink placement | implemented from the measured ink bbox | the panel-vs-ink distinction cost a 2.2× size error once |

### 10.8 Camera and lighting — LOCKED

Full-frame **36 mm sensor**, real focal lengths, **f/8** on the heroes and
f/6.3 on the detail views, focused on the **near front arch**. Measured on
`hero34f`: 78 mm, f/8, focus 10.12 m, **sharp 7.25 – 16.71 m**, hyperfocal
25.4 m. Ortho views carry no DoF.

Lighting is **one long raking strip** (16.0 × 0.55 m, spread narrowed to 78°)
plus support, not six neutral rectangles — a long narrow source draws a single
unbroken highlight along the shoulder that pinches where the panel turns, which
is the read that says sheet metal. The whole rig was **2.6 EV hot**: cream
measured 233–240 against 206 and AgX desaturates as it approaches white, which
is what dragged the flank to sat 0.27. Rig energies scaled **×0.165**; the
numbers in `studio.py` are now the numbers that render.

Compositor, in the order a real camera imposes them: bloom on the *linear*
render before the white composite (after it, a linear-21.0 backdrop flares the
frame), then chromatic aberration, vignette and grain on the projected image.
Pixel filter widened to 1.50 px. Every stage is switchable from the
environment; `T1_FX=0` disables the chain.

---

| 2026-08-09 | **rev 7 — adversarial skeptic pass, then implementation.** 0 of the 13 criticals killed, 11 corrected; acting on the audit's numbers as written would have introduced fresh errors in six places. **SUB=2 passed for the first time** — both cab-door gap booleans had been collapsing the shell 205562 → 12 v and rolling back, so every hero render this project ever made was of a bus with no cab-door shut line. Belt, V-swage, window band, aperture edges, louvres, counter, script and roundel all set from measurement. `RED` corrected from a **retired deep crimson**; folk art capped from wallpaper to a graded bouquet. Weathering node group built to measured targets. Boolean guard strengthened and validated (2 true positives, 0 false positives); the `≥ 20 mm roll-over` rule refuted and replaced. Physical camera with real DoF; one raking strip replaces the six-rectangle rig; rig found 2.6 EV hot. `audit.py` now emits **`STATE.md`** from live geometry — it had printed a hardcoded, fabricated belt line for six revisions. Open defects logged in §10.7 rather than quietly carried. |

---

## 10.9 rev 8 — the rake, the lids, and what the saturation target actually is

### The stance is a LINE, not a scalar

`build.py` step 8b subtracted `RIDE_DROP` from every vertex. The vehicle read
**89 mm short** and, in Donald's words, flat and stretched. `REF_MEASUREMENTS`
§2.3 inferred a roof-lid frame standing 0.10–0.15 m proud; that is **refuted at
~13σ** by a camera-free measurement (roof silhouette minus drip rail at the same
column: 36.6 ± 0.6 px on the factory cab roof, 35.4 ± 0.9 px on the fixed rear
roof — the same structure; a 0.10 m curb reads 20–22 px). Measured proud height
is **26 ± 7 mm**.

The cause is the unmodelled nose-down rake. Locked:

| constant | value |
|---|---|
| `RAKE_Z0` | **0.0365** m — ride drop at x = 0 |
| `RAKE_DZDX` | **0.0330** m/m ± 0.0040 — nose-down, 1.89° |
| `X_DROP_REF` | +0.8636 — the station where `rake_drop(x)` equals the old scalar 0.0650 |

`drop(x) = RAKE_Z0 + RAKE_DZDX·x`. **Shear, never rotation** — every reference
number is a height-versus-X and a 1.9° rotation also shifts x by 63 mm at roof
level. `RIDE_DROP` survives ONLY as the value at `X_DROP_REF`; it is not a frame
conversion. Use `t1_core.rake_drop(x)`.

Consequences, all implemented:

- **`Z_BELT` is a line.** `t1_mats.z_belt(x) = Z_BELT0 − RAKE_DZDX·x`, with
  `Z_BELT0 = 1.2355` and `V_APEX0 = 0.3685` (above ground at x = 0). The rake is
  subtracted **once, after** the flank/nose mix, so `V_APEX0 + V_RISE == Z_BELT0`
  holds at every station and the swage arms stay on the belt.
- **`verify.py`'s frame offset is a function of x.** A 5.5 mm shut line probed
  one station off reads closed.
- **`audit.py`'s height row is a three-station roof-line check.** A scalar cannot
  express a sloping roof; that row certified the broken dimension for seven
  revisions.
- **Wheels do not rake.** They are circles on flat ground: centre at exactly
  `TIRE_R`, contact patch on z = 0. They are EXCLUDED from the shear rather than
  sheared-and-compensated, which would swing each hubcap VW glyph 1.9° off
  vertical.
- **The cab-door shut line had to move.** The rake lifts the front arch 14.4 mm
  (`rake_drop(1.300)` = 0.0794 against `RIDE_DROP` 0.0650), so the arch top goes
  0.7710 → 0.7854 and rev 7's 0.7800 bottom run would sit **5.4 mm below it** —
  the exact condition that collapsed the shell 205562 v → 12 v at SUB=2. Bottom
  run lifted to **0.8000–0.8160**, and the clearance is now **asserted at import**
  in `t1_shell`, not described in a comment.

Result: roof at the rear-axle station **1.871 → 1.923** against §2.3's measured
1.960. **Residual −37 mm, logged not hidden** — 1.2σ on §2.3's own ±30 mm band.
The guard carries that band explicitly and warns rather than failing.

### OPEN, unresolved: rake versus the arch gap

`RAKE_DZDX × wheelbase = 0.0330 × 2.400 = 79 mm`. So the front arch gap must be
79 mm **less** than the rear. But the rear gap measures **≈30 mm** off
`ref_side.jpg` (arch lip y 524 ± 2 against a tyre top computed at 532.3 from a
rim circle fit at 211.5 px/m) and §2 locks it at 41 mm. Either way
`front = rear − 79 mm` is **negative** — the tyre inside the bodywork. Two
measurements off the real vehicle contradict each other.

Held: the arches follow their own wheel (`t1_shell.arch_z(x)`), which keeps both
measured numbers and produces no impossible geometry. Resolving it needs a
photograph with an **unoccluded front wheel** — in `ref_side.jpg` a man stands
directly in front of it, and every attempt to measure the front arch locked onto
his red shirt.

### The flank saturation target was never a comparable quantity

rev 7 logged flank saturation **0.601 against SPEC's 0.816** and listed three
suspects. Measured, same build, side ortho, one variable each:

| probe | flank sRGB | hue | sat |
|---|---|---|---|
| baseline | (190,124,83) | 23.3 | 0.565 |
| folk art off (`W_ART` → 0) | (189,122,82) | 22.4 | **0.566** |
| weathering albedo off | (189,124,83) | 23.3 | 0.564 |
| sun fade off | (184,118,76) | 23.5 | 0.588 |
| dust off | (184,118,76) | 23.5 | 0.586 |
| AgX Punchy off | (210,152,118) | 22.3 | **0.438** |
| Standard transform | (245,165,96) | 27.7 | 0.607 |

- **Residual folk-art coverage — REFUTED.** ±0.001.
- **AgX Punchy — REFUTED, and the sign is backwards.** Punchy *adds* +0.127.
- Fade / dust / weathering albedo — ≤ 0.002 each.

Decomposing the pixel against the locked albedo, `R_lin = a_R·E + A` and
`B_lin = a_B·E + A`, gives **E = 0.760** and a **neutral additive term
A = 0.0592**, 12 % of the red channel. Falsifiable prediction, then tested:
at Specular IOR Level **0.00** the flank renders **(183,106,39) sat 0.788**
against the target (196,106,36) sat 0.816 — green exact, blue within 3 codes.

**LOCKED: SPEC's 0.816 is the paint's ALBEDO saturation**, measured off a sunlit
photograph where the specular lobe pointed away from the camera. No beauty-pass
pixel of a dielectric under a large white softbox can reach it, because a white
source's specular reflection is achromatic and additive. The correct test is on
the albedo; the beauty value is an **outcome of the rig**, not a target.

| quantity | target | rev 8 |
|---|---|---|
| albedo saturation (the real test) | 0.816 | **0.816** — `RED` is exact |
| beauty-pass flank, white studio | *no target* | 0.586, hue 23.5 |

Also corrected while in there, both physical and both measured:
`Specular IOR Level` **0.21 → 0.50** (0.21 implies F0 0.0168 / IOR 1.29, which no
paint has); studio sweep albedo **0.94 → 0.76** (0.94 is near-PTFE); white world
**0.17 → 0.05**.

### Folk-art density ran backwards — MEASURED

Gold coverage as a fraction of the red+gold flank, `ref_side.jpg`, 40 px columns:

| X | +1.47 … −0.40 | −0.59 | −0.96 | −1.71 | −1.90 |
|---|---|---|---|---|---|
| gold | **0.0–0.2 %** | 4.7 % | 13.8 % | 25.9 % | **36.9 %** |

rev 7 ran a single MapRange, 0.34 at the tail rising to 1.00 at the nose —
densest exactly where the reference is bare red under the script, sparsest on the
rear-quarter bouquet. Replaced with **two measured lobes** (tail bouquet, cab-door
scroll) combined with MAXIMUM. Tile scale 0.63 → **0.42** (period 1.587 m → 2.38 m;
2.7 visible repeats was wallpaper).

### The canvas ragtop was still shipping

`t1_shell.ragtop()` built a folding **canvas** roof — five Gaussian bow sticks, a
sailcloth sag term, a `canvas` material and a Metallic-1.0 `chrome_dull` frame
down the middle of a white roof. §0.2 retired that reading **in rev 4**. It
survived three revisions because `verify.py` banned only the three retired
materials somebody remembered to type.

Replaced with rigid hinged steel lids, **modelled OPEN**. Guard is now an explicit
reviewed map **plus a drift check on §0.2 itself** — if §0.2 gains a bullet, the
guard warns until someone reviews the map. The first attempt scanned §0.2 for
material names directly and flagged **six correct materials**, because every
bullet is "retired reading — correction" and the names appear on both sides.

Lid geometry, measured at 211.5 px/m: main lid **X +0.964 → −1.070**, 1.11 m
hinge-to-free-edge, opened **104°**; `RAG_X0 = +1.4800` is **contradicted** — the
cab roof dome is unbroken to X = +0.964. Second lid **X −1.140 → −1.780** at 82°.
Proud height **0.0228** skin / **0.0213** rail. Mural artwork in `lid_gen.py`:
**nine flower heads** (five upper, four lower — counted off `ref_side.jpg`),
palette ratios measured on the board interior (n = 70400: red 43 %, orange 34 %,
yellow 17 %; generated 52 / 34 / 14).

### Other rev 8 corrections

`brass` folded into `t1_mats.build_all()` with a roughness field — it was the last
illegitimate constant-roughness material. Bulb string given an **emissive**
material; it rendered unlit pearl white and reads lit and warm in both in-service
photographs. VW glyph rebuilt as **two closed mitred prisms** per `SKEPTIC_PASS`
§D, and `t1_detail.vw_logo` now delegates to `t1_core.vw_bars` — two independent
copies of the same glyph is why they drifted. Glass roughness 0.004 → 0.022;
`capred` 0.085/coat 0.85 → 0.165/0.50; render clamps released (indirect sat at the
factory 10.0 against a paper white of 21–25, ceilinging every highlight a stop
below the backdrop); backdrop white point keyed on the (transform, **look**) pair
— under AgX + Punchy linear 21.0 maps to display 253, so the "white" sweep was two
codes grey; 16-bit output.


## 10.10 ABSOLUTE REPLICATION OF ARTWORK — standing requirement

Recorded at Donald's explicit request, 2026-08-10. A **hard bar, not a
preference**, and it outranks convenience everywhere it applies.

> Every painted element on this vehicle must be REPRODUCED from photographs of
> the actual combi. Not approximated. Not invented. Not derived from palette
> statistics.

In scope, none of it optional:

| element | source crop | state at end of rev 8 |
|---|---|---|
| lid mural board | `ref_side.jpg` (300,40)-(770,310) | **reproduced** — `lid_gen.py` |
| flank paisley | `ref_rear34.jpg` (620,560)-(1200,820) | **reproduced** — `folk_gen.py` |
| "Senor Tacombi" script | `ref_side.jpg` (300,470)-(620,570) | **REJECTED BY DONALD** |
| "100% Calidad" decal | `ref_side.jpg` (735,295)-(860,390) | **not started** |
| menu strips on the lid | `ref_side.jpg`, board edges | reproduced with the mural |
| menu cards on the pillars | `ref_side.jpg` (600,600)-(900,700) | untextured white |
| rear-lid lettering | `ref_rear34.jpg` (700,20)-(1050,300) | placeholder |
| "1963" plate surround | `ref_rear34.jpg` (1330,780)-(1500,860) | modelled, never read |

The failure mode this rule exists to stop is exactly what rev 8 did first: the
mural was built from *measured palette ratios* — red 43 % / orange 34 % /
yellow 17 % — which produces something plausible and generically 1960s. The bar
is that the owner recognises **his own vehicle**. A statistically correct flower
pattern does not do that; the actual board does. The same test applies to every
row above.

The resolution constraint dictates the method. The mural occupies ~450 x 270 px
in `ref_side.jpg`, the script ~290 x 80 px. That is enough to read the DESIGN --
motif structure, ring order, letterform skeleton, wording, layout, palette --
and nowhere near enough to resample as a texture. **Replication therefore means
reading the design at 4-5x magnification, redrawing it faithfully at 2-4K, and
then measuring the result back against the crop.** It does not mean tracing
pixels, and it does not mean a system font with flourishes bolted on -- that is
what shipped in rev 8 and Donald rejected it by name.


---

| 2026-08-10 | **rev 8 — the rake, the lids, and the saturation target.** Step 8b shears instead of dropping; roof at the rear axle 1.871 → 1.923 against a measured 1.960, residual −37 mm logged. `Z_BELT` is a line; `verify.py`'s frame offset is a function of x; `audit.py`'s height row is a three-station roof-line check. Wheels held level. Cab-door shut line lifted 20 mm because the rake ate its arch clearance — the SUB=2 collapse condition, now asserted at import. **The retired canvas ragtop was still shipping** and no guard caught it; replaced with rigid hinged steel lids modelled OPEN, mural and lettered rear lid, and the guard rebuilt as a reviewed map plus a §0.2 drift check. Flank saturation diagnosed by measurement: folk art and AgX Punchy both **refuted** (Punchy *adds* 0.127), the deficit is a 0.0592 achromatic specular term, and SPEC's 0.816 is an **albedo** number that no beauty pixel can meet — target restated. Folk-art density measured and found to run backwards; two lobes. Fresnel 0.21 → 0.50, sweep albedo 0.94 → 0.76, world 0.17 → 0.05, clamps released, VW glyph two mitred prisms, brass folded in, bulbs emissive. |
| 2026-08-10 | **rev 9 — the art reproduction pass, and the first heroes to land.** The "Señor Tacombi" script is rebuilt as explicit letterforms (`script_gen.py`); the font-plus-flourishes approach Donald rejected by name is gone. Control points read off `ref_side.jpg` at 6–14× in that photograph's own pixel frame. Corrected by measurement: spiral counters are ~1.1–1.3 turns with a wide groove (the o's counter is 224 px in a 21×25 box, 43 % fill), not tight spirals; the swash is an **arch**, cresting at y 36.2 near x 57 and falling back to 41.5 by x 90, not a monotonic rise; its left terminal is a 0.80-turn spiral about (17,59). Whole-lockup IoU **0.511** against a measured ceiling of 0.77–0.81 — a 1 px shift of the reference against itself costs 0.14 — with a global alignment search buying only +0.012, so the residual is distributed shape error of ~1.5–2 px, not misregistration. **Calidad** built for the first time (`cal_gen.py`): uneven-tipped burst, measured gradient, white bold italic at the measured −19.7°, bunting with pennants, pink star, counters punched on a mask. Moved **198 mm forward** on a panel-fraction datum immune to the perspective foreshortening that makes one linear scale wrong at the tail (194.8 px/m there against 211.5 at mid-body). §10.11 the ground-line datum is refuted as a placement source at ~70 mm common-mode; §10.12 `RED` hue 26.2 → **5.0**, saturation untouched; §10.13 the Playa rig was compositing its own world away; §10.14 abutting strips seam and overlapping strips do not. **White-studio and Playa heroes delivered at 2400×1600, 64 samples, six strips, worst seam z = 1.88 and 1.45 against a threshold of 4 — the first heroes in nine revisions.** |
| 2026-08-10 | **rev 9 addendum — §10.15.** Donald identifies `ref_rear34.jpg` as showing the FRONT of the vehicle with the roof opening forward, not a rear three-quarter. Every crop attributed to that file is now suspect, including the flank paisley that §10.10 marked done. He also restates the governing standard for rev 10: *"we are recreating a photo realistic version of that exact bus."* |
| 2026-08-10 | **rev 9 addendum — §10.17, §10.18.** Donald restates the acceptance criterion as **per-measurement**: "nearly indistinguishable from the original. Any single measurement off is unacceptable." And flags the front fascia as drifting — six items, four of them audit findings logged and unapplied for several revisions, one new (cab-door folk art far too faint), one unmeasured (bumper depth). The folk-art item contradicts §10.9's near-nose coverage lobes, which were scanned by body x across an OPEN cab door. |
