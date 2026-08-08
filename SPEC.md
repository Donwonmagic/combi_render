# TACOMBI COMBI — LOCKED BUILD SPECIFICATION  (rev 5)
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
| Roof | **cut into rigid hinged steel lids**, modelled **CLOSED**; fore-aft seam and a second smaller lid visible | **S**+**R** |
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
| Overall length over bumpers | **4.290** | 4.280 |
| Overall width | **1.750** | 1.720 |
| Overall height, unladen | **1.941** | 1.940 |
| Wheelbase | **2.400** (front +1.300, rear −1.100) | same |
| Track front / rear | **1.369 / 1.359** | 1.375 / 1.360 |
| Tyre **6.40-15** | dia **0.683** (R 0.3415), section **0.165** | 5.60x15, 0.665 / 0.145 |
| Rim | 4½ K × 15, R 0.1905, PCD 5×205, ET ≈ 45 | R 0.1905 |
| Hubcap | dia **0.280**, depth ≈ 0.080 | — |
| Body max half-width | **0.875** | 0.860 |
| **Ride height** | **LOWERED — reinstated in rev 5.** Rear arch-to-tyre gap measures **71 ± 10 mm** against a stock 90–120 mm; front bumper top sits at **0.348 m** against a stock ≈0.47 m. Donald's original rev-3.1 reading was right; rev 4 wrongly set this to 0 on absence-of-evidence from a thumbnail. See §8.6 | rev4 said stock — WRONG |
| **Stance rake** | body sits **nose-down ~1.7°** relative to the axle line (72 mm over the wheelbase). Every height falls ≈28 mm per metre forward. Not modelled yet | — |
| Roof edge / crown | 1.8935 / +0.032 | same |
| Belt line (two-tone break) | **z = 1.386** — hold, but see §2.1 | same |
| Front / rear sheet metal | x = +2.108 / −2.108 | same |
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

### 2.2 Contested measurements — DO NOT bake in without a second pass
A measurement pass on the high-res photos returned three extraordinary claims.
Each is plausible but would overturn a factory dimension, so each needs
independent re-derivation before it enters the build:
- **Tyres are NOT 6.40-15.** Wheelbase-derived scale (211.2 px/m) and
  tyre-derived scale (187.4 px/m) disagree by 12.7 %, which resolves if the
  tyre OD is ≈0.606 rather than 0.683. Corroborated by a tyre/rim ratio of
  1.39–1.47 measured on the bare rims in `ref_workshop.jpg` against 1.69 stock.
- **No rear bumper.** Not visible in either in-service photo. Conflicts with a
  cream rear bumper reported in `ref_workshop.jpg`. It may have been removed
  when the counter wrap was fitted.
- **Overall length 4.05 m, not 4.29.** This would mean a shortened body, which
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

## Change log

| Date | Change |
|---|---|
| 2026-08-08 | Initial lock. Body corrected from single-cab pickup to Kombi van. |
| 2026-08-08 | Script text corrected to "Señor Tacombi"; capital T must be an ornate swash. |
| 2026-08-08 | Script colour corrected to **silver**. |
| 2026-08-08 | rev 3.2 — modified-bus details locked: whitewall tyres, red domed hubcaps with white VW, low bumpers, proud bullet indicators. |
| 2026-08-08 | rev 3.1 — bus is **lowered**: body dropped 65 mm relative to the wheels. |
| 2026-08-08 | rev 3 — grounded against prior project context. |
| 2026-08-08 | **rev 4 — evidence audit.** Added evidence grades (§0) and measurement provenance (§8). **Corrected against measurement:** whitewall → blackwall + cream rim; chrome → cream bumpers; cream → **red** VW roundel; four bays → **three** + solid rear panel; canvas ragtop → **cut steel lids**; timber → **painted** counter; bullet → **fish-eye** indicators; lowered → **stock** ride height. **Corrected against factory sources:** L 4.280 → 4.290, W 1.720 → 1.750, tyre 5.60-15 → **6.40-15** (dia 0.665 → 0.683), track → 1.369/1.359. Finish changed to **weathered** by user decision. Added §4 detail inventory, §7 wrong-bus warning, §2.1 unresolved belt/sill conflict. Guards extended to 10. |

| 2026-08-08 | **rev 5 — high-resolution photographs supplied by Donald.** Three large photos (workshop/green, side elevation, rear 3/4) supersede the 246x197 thumbnail as primary reference. **Ride height LOWERED reinstated — rev 4 was wrong to zero it; Donald's original reading was correct.** Belt/sill conflict resolved: break sits 100 mm below the sill, not 16. Aperture positions re-measured and are not evenly sized. Rear serving opening and counter tail-wrap added. Three contested measurements quarantined in §2.2 pending independent re-derivation. Full working in REF_MEASUREMENTS.md. |
