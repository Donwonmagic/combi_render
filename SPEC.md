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

### 0.2b Retired since rev 4 — added rev 24, and READ WHAT THIS DOES

> **This list does NOT arm `verify`'s material guard, and rev 24's own brief
> said it would.** `verify._retired_material_tokens()` returns the hand-written
> `_RETIRED_MAT` dict, not anything parsed from this section;
> `_retired_section_drift()` reads §0.2 only to COUNT bullets and never reads a
> bullet's content. The ban it feeds compares **material datablock names**.
> Every entry below is a VALUE, a METHOD, a CROP or a withdrawn TEST — **not one
> is a material name**, so not one is reachable by that mechanism. Of ~100
> retirements in §10, exactly one was ever a material (the canvas ragtop, above,
> already covered).
>
> What this section buys is the **forced review**: adding to it changes the
> bullet count, which trips `_retired_section_drift()` until a human re-reads
> the map. That is real and it is all it is. The mechanism that catches a
> retired *value* republished as locked is **`verify._retired_value_drift()`**,
> added in rev 24 — it FAILS on any retired literal appearing unstruck in the
> FROZEN front matter, and it caught §1.1 and §3 on its first run.

- ⚠ **`RED` (196, 106, 36), hue 26** — off the 246×197 thumbnail, contaminated
  by the gold folk art. Live **(196, 49, 36), hue 5.0**, saturation 0.816 (§10.12)
- ⚠ **aperture band sill 1.402 / head 1.798** — live **1.372 / 1.775** (§10.2)
- ⚠ **bay taper 0.507 / 0.516 / 0.526** — the rev-13 100 mm ORIGIN ERROR; the
  bays are **EQUAL at 0.5155** (§10.29, §10.47)
- ⚠ **`RAKE_DZDX = 0.0330`** — rejected at 4.5 σ; live **0.017750** (§10.29)
- ⚠ **`W_ART = 0.30`** — a 30 % opacity ceiling on hand-painted signwriting;
  live **1.00**, and the table published 0.30 for thirteen revisions (§10.64)
- ⚠ **`H_ROOF = 1.960` as an accuracy target** — retired by the owner in rev 22;
  the probe is a LABELLED regression catcher at 1.9835 ± 5 mm and **the absolute
  roof height is OPEN**. Do not re-add it as a target (§10.59)
- ⚠ **the GROUND-LINE datum** (~70 mm common-mode) **and the HUB-referenced
  chain** (~29 mm) as vertical placement sources (§10.11, §10.34)
- ⚠ **`REF_PPM = 211.2`, a single flat px/m across the flank** — the map is
  projective, and a scale measured on one plane is not the scale on another (§10.43)
- ⚠ **`ref_side.jpg` as a body-cream source** — it contains no usable
  body-cream patch at all (§10.38); and **the "La Santa" panel** as a cream
  reference — it is a **DETACHED SIGN**, not the bus (§10.49)
- ⚠ **crop N1** as a napkin reference — it straddles a napkin and the dispenser
  body; route A stands on N2/N3 (§10.57)
- ⚠ **the pure-white backdrop lock** — retired by the owner in rev 15;
  `BACKDROP` defaults to `headroom` (§10.32)
- ⚠ **a ray-visibility flag as an ablation** — in Cycles the ray passes through
  and substitutes the background. Remove the ALBEDO (§10.56)
- ⚠ **arc length as a crossing metric** — it overstates penetration by up to
  23× (§10.62)

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
| 1 | ~~**+0.820**~~ | ~~**+0.313**~~ | open serving hatch |
| 2 | ~~**+0.195**~~ | ~~**−0.321**~~ | open serving hatch |
| 3 | ~~**−0.435**~~ | ~~**−0.960**~~ | open serving hatch |
| — | ~~**−0.960**~~ | ~~**−2.007**~~ | **SOLID sheet metal**, ~~1.046 m wide~~. "100% Calidad" sunburst + pink star applied here |

**THE FOUR ROWS ABOVE ARE RETIRED — §10.69, rev 25.** They carry the same two
retired errors as the struck sentence below, RE-EXPRESSED AS EDGE PAIRS and so
invisible to a guard keyed on the width form. Differenced, the published edges
give **0.507 / 0.516 / 0.525** — bit-for-bit the retired taper — and their
midpoints sit **105.5 / 110.0 / 99.5 mm AFT** of the live centres, which is
§10.29's 100 mm ORIGIN ERROR. **LIVE:** `t1_shell.BAY_W = 0.5155`, equal, with
`BAYS = (+0.41425…+0.92975), (−0.21075…+0.30475), (−0.85575…−0.34025)`. The
solid panel runs `BAYS[2][0] = −0.85575` to `X_TAIL = −1.8730` and is therefore
**1.0175 m** wide, not 1.046 — the 1.046 inherits the refuted `−2.007` tail.

~~Measured from `ref_side.jpg` (§8.6). Widths 0.507 / 0.516 / 0.526 — they are
**not** identical; they grow slightly toward the tail.~~ **RETIRED by §10.29
and §10.47** — that taper was the 100 mm ORIGIN ERROR of rev 13, not a real
taper, and §10.47 removed the same sentence from `STATE.md` as hand-authored.
**The bays are EQUAL at `BAY_W = 0.5155`**, centres +0.672 / +0.047 / −0.598
(`t1_shell.py:150-152`); the live widths are printed by `verify` every run
(0.516 / 0.515 / 0.516) and are never typed here. rev-3's "three evenly sized,
evenly spaced" was retired for a different reason and stays retired.

~~Band: sill **z = 1.402**, head **z = 1.798**~~ — **RETIRED by §10.2.** Live
`Z_SILL = 1.372`, `Z_HEAD = 1.775` (+27 / +25 mm); `verify.py:193` already
called 1.402/1.798 "the retired band" while this line still published it.
Corner radius 0.055, pillars 0.11.
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
| **Stance rake** | ~~body sits **nose-down ~1.7°** relative to the axle line (72 mm over the wheelbase). Every height falls ≈28 mm per metre forward. Not modelled yet~~ **RETIRED, §10.69.** It IS modelled — `t1_core.rake_drop()`, applied at `build.py:537` step 8b and asserted at `:551` — and the magnitude is **`RAKE_DZDX = 0.017750` = 17.75 mm/m, 1.02°**, 42.6 mm over the 2.400 m wheelbase. The status was closed by §10.9 ("Consequences, all implemented"); the magnitude went 28 → 33.0 → 17.75, the last step by §10.29 at 4.5σ. **Provenance stated honestly: no §10 sentence retires the literals "1.7°" / "≈28 mm per metre" / "72 mm" BY NAME — they are superseded by that chain. "Not modelled yet" is retired explicitly.** | — |
| Roof edge / crown | 1.8935 / +0.032 | same |
| Belt line (two-tone break) | ~~z = 1.386~~ **superseded by §10** | same |
| Front / rear sheet metal | ~~x = +2.108 / −2.108. **Note §10.7: the tail measures −2.007 on the vehicle and the factory overhang gives −2.009, so the model is ~99 mm long at the tail. Unresolved.**~~ **RETIRED, §10.69.** The NOSE half survives — `t1_core.X_NOSE = 2.108`. The TAIL is **`X_TAIL = −1.8730`** since rev 16 re-spaced the overhang `O_OLD 1.008 → O_NEW 0.773` (§10.35), and §10.7's "~99 mm" is **REFUTED at 10σ** — it subtracted two numbers in different origins (`SPEC.md` §10.35). Nothing here is unresolved. | same |
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
- ~~**Front indicator: fish-eye / teardrop, correct for a 1963.** Fitted lamp
  measures 71 mm base × 78 mm protrusion, ratio 1.05; a bullet pod is ≈45 mm
  base at ratio ≈2. It only *reads* as a bullet in side elevation. Workshop
  aperture is a round 74 ± 6 mm hole.~~ **RETIRED, §10.69.** §10.22 REFUTED the
  flat-oval proposal by measurement — *"the existing bullet is closer to the
  photograph"* — and kept the type while moving the lamp outboard. **LIVE:**
  `build.py:354` calls `t1_detail.bullet_indicator()`. This section is headed
  *"Settled by the verification pass"*, which is what made it dangerous.
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
- ~~Overall height measures **1.960** with the lids closed — *above* stock 1.93
  despite the lowering, implying the roof-lid frame stands proud by 0.10–0.15.~~
  **RETIRED, §10.69, and BOTH halves separately.** `H_ROOF = 1.960` was retired
  as an accuracy target by the OWNER in rev 22 (§10.59) — it came from the
  ground line §10.11 bans and lost its only ground-line-free support; the direct
  mesh probe reads **1.9835** and is a LABELLED regression catcher, not a
  target, and **the real vehicle's absolute roof height is OPEN and UNMEASURED**.
  The proud-frame half is separately **refuted at ~13σ** by §10.9: measured
  proud height is **26 ± 7 mm**, not 100–150.
- Front indicator aperture in `ref_workshop.jpg` is a plain **round ≈75 mm
  hole**. ~~Lens type remains **U** — neither bullet base nor fish-eye oval
  confirmed.~~ **RETIRED, §10.69** — §10.22 resolved the type: flat-oval
  REFUTED, bullet kept and built (`build.py:354`).

---

## 3. Livery — FROZEN

| Element | Specification | Grade |
|---|---|---|
| Upper body + roof | sun-bleached off-white, near-neutral. Measured (206, 208, 200) sRGB in full sun | **M** |
| Lower body | faded **orange-red / vermillion**. ~~measured (196, 106, 36) sRGB in full sun — hue ≈ 26°~~ **RETIRED by §10.12** — it came off the 246×197 thumbnail, where the flank is ~100 px wide and the value is contaminated by the GOLD folk art. Live `RED` = **(196, 49, 36), hue 5.0**, saturation 0.816 LOCKED (`t1_mats.py:67`). **Not** a deep crimson | **M** |
| Break | belt line, sweeping down across the nose into the T1 **V-swage**: apex low **on the centreline**, arms **rising** to the belt at the corners. The light colour forms a **downward wedge** down the nose centre; the **red occupies the two outboard lower zones and contains both headlamps** | **M** + **S** |
| Folk art | **gold + yellow + white + dark-red** Mexican folk-art florals over the **red only**. **Density graded** — dense bouquet on the nose flanks and rear quarter, trailing vine along the belt, sparse under the script | **M** |
| Side script | **"Señor Tacombi"**, **SILVER** with a dark keyline and drop shadow, two-line lockup (small "Señor" raised over large "Tacombi"), capital **T an ornate swash**; decorative spirals inside the counters of a/c/o/m/b | **R** (text/colour also **S**) |
| Rear-corner decal | **"100% Calidad"** — white slanted type on a **red-to-orange spiky sunburst**, on **solid cream sheet metal** aft of bay 3, with a small pink star to its left | **M** (position) + **R** (content) |
| VW nose roundel | painted **RED on the cream nose**, **V above W**, pressed relief not chrome. ~~⌀ ≈ 0.370, centre z ≈ 1.130~~ **RETIRED, §10.69** — §10.22 measured **0.280 ± 0.030 m** by a relation needing no camera pose and found the centre **0.149 ± 0.030 m BELOW the belt**, i.e. the build's 0.370 was **32 % over** and **113 mm high**. **LIVE:** `build.ROUNDEL_D = 0.2800`, `build.ROUNDEL_Z_AG = 1.0170`. The stale 0.370 also fused the VW glyph into an X twice (§10.25). | **M** + **E** |
| Wheels | **BLACKWALL** tyres; **cream/off-white painted steel rims**; **red domed hubcaps** with a **light VW** in the centre | **M** |
| Bumpers | **painted cream**, front and rear, stock blade section, **two vertical overriders each** | **M** + **S** |
| Bright work | headlamp bezels read **warm/brass**, not bright chrome. Drip rail, handles, mirror: dulled | **R** |
| Indicators | ~~**flat oval "fish-eye"** lenses in a rim, above and slightly outboard of each headlamp, standing proud. **Bullet pods are period-wrong for 1963**~~ **RETIRED, §10.69** — §10.22 REFUTED the flat-oval by measurement and kept the BULLET, moving it **0.130 ± 0.035 m outboard** (the position finding was confirmed but 7× understated). **LIVE:** `t1_detail.bullet_indicator`, `build.py:354`. Note §10.24 left the lens *depth* open at 1.2σ — that is a different quantity and is NOT retired. | **S** |
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
~~composited to **pure white**~~ **RETIRED, §10.69 — THE OWNER'S DECISION, rev
15 (§10.32).** Shown the A/B on a real hero he chose the **headroom** arm:
corners 246.043 against 248.997, exactly-white fraction 0.66 % against 0.92 %,
grain sd 0.9415 against 0.4718. **LIVE:** `post.BACKDROP = "headroom"`,
`BACKDROP_PEAK = 252.0`; `--backdrop white` still gives the old behaviour for a
keyable 255 backdrop. The pure-white lock erased the designed vignette and grain
rather than adding anything — with a soft contact shadow. Large soft sources
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
10. ~~`RIDE_DROP` ≠ 0 → FAIL~~ **RETIRED, §10.69, and it published the INVERSE
    of the guard that runs.** This is rev 4's "stock ride height" position,
    reversed by rev 5 on Donald's own reading (change log 2026-08-08) and by §2's
    own **Ride height** row in this same frozen front matter. **LIVE:**
    `verify.py:125` `RIDE_DROP_SPEC = 0.065` and `verify.py:796` FAILs unless
    `RIDE_DROP` equals it to 1e-9 — so the published rule would fail every
    current build, and §2 and §9 contradicted each other inside the front matter.
    §10.45 additionally labels the row an algebraic identity (residual exactly
    0.000e+00) and it is kept as a LABELLED lock on the authored constants.

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

### 10.29 rev 13 -- the rake falls, and a 100 mm origin error surfaces twice

**THE RAKE IS 17.75 mm/m, NOT 33.0, AND THE OWNER AUTHORISED RE-OPENING IT.**
His settled list names ~1.9 deg. The condition he set was a fourth derivation
before anything moved, and this is it. The method needs **no ground line, no
px/m and no vanishing point**: both hub centres sit at exactly one tyre radius
above flat ground BY CONSTRUCTION, so the rocker's height above its own hub,
taken at each axle and scaled by that wheel's own tyre, differences straight
into the rake.

| station | hub, sub-pixel polar fit | local px/m | rocker above hub |
|---|---|---|---|
| front axle | u 242.60, v 607.84 | 204.4 | **-0.0004 m** |
| rear axle | u 749.27, v 604.13 | 213.5 | **+0.0422 m** |

`rake = 0.0426 / 2.400 =` **0.01775 m/m, 17.6 +/- 3.4 mm/m**. From the built
0.0330 that is **4.5 sigma -- rejected**. From the audit line's independent
14.4 +/- 3.1 it is 0.70 sigma -- consistent.

Three things made this unresolvable for five revisions and all three are now
named:

1. **An image slope of a fore-aft line is not the rake.** Every one of rev 8's
   chains measured one. All of the vehicle's own horizontal lines converge on a
   vanishing point at u ~ -11700, so a raw slope carries the perspective term
   as well. Re-fitting the rocker trim ridge sub-pixel gives -0.025415 +/-
   0.000178 px/px (rms 0.299, n = 324) -- **neither candidate**, because it is
   not the quantity.
2. **The front wheel is 54 % unoccluded**, not unusable. Polar sectors
   -40...+66 and +110...+198 are clear of the man; that is enough for a
   constrained circle fit. Every previous attempt used a bounding-box search
   and locked onto his red shirt.
3. **The arch-gap identity is a BOUND, not an estimator.** `rear - front =
   rake x wheelbase` holds only if both lips sit at the same height above their
   own hub, and on a T1 they are different pressings -- so it confounds the rake
   with a design difference. It still bounds: a non-negative front gap needs
   rake <= 0.0171, which kills 0.0330 on its own. **10.9's contradiction is
   closed against the built value.** The rear gap itself re-measures 41.0 +/-
   3.5 mm -- exactly the built `ARCH_R - TIRE_R` -- refuting the audit line's
   own 52 mm at 3 sigma.

`RAKE_Z0` is re-anchored in the same solve, not carried over: the model sat
-0.0088 above its hub at the front and +0.0704 at the rear, so **both ends
move**, the nose up 8 mm and the tail down 28 mm. `X_DROP_REF` is now DERIVED
from the rake (10.25), which holds `RIDE_DROP` at exactly 0.0650 and therefore
keeps `Z_BELT` = 1.2070 and `V_APEX` = 0.3400 **bit-identical** through the
change. `t1_mats.Z_BELT0` / `V_APEX0` were literals carrying their derivation
only in a comment -- the same shape of bug that merged the VW glyph into an X
twice -- and are now expressed in terms of `RAKE_Z0`.

**THE ROOF GUARD IS STRENGTHENED, NOT WIDENED.** The lower rake takes the crown
1.923 -> 1.894, so the raw residual against REF 2.3's 1.960 grows -37 -> -66 mm.
That is not the rake getting worse; it is a second, separately measured defect
becoming visible. The transverse roof section is **3.9x too flat**: crown R
**2.45 +/- 0.15 m** measured against 9.65 built, gutter-to-crown **0.188 +/-
0.015 m** against 0.083. Two frames, two physics -- crown-minus-drip-rail at the
same column in `ref_side.jpg`, and the open lid's forward CUT EDGE in
`ref_workshop.jpg`, which is literally a transverse section of the roof and fits
a circle at rms 0.49 px against a straight line's 4.51. So the crown sits
**0.098 +/- 0.010 m** below where its own gutter puts it. Encoded as a named
`DOME_DEFICIT` that **must be driven to zero** when the section is rebuilt,
rather than by widening a band that would then also swallow a rake regression.
The RAW residual is logged every run so it cannot go quiet. This also
**overturns 10.22's `geometry-4` NOT MEASURABLE**: rev 10 could not find a
datum, and the drip-rail gutter is one.

**THE 100 mm ORIGIN ERROR, found independently in two dimensions.**
`REF_MEASUREMENTS` maps the photograph as `X = (495.8 - u)/211.5` and calls
X = 0 mid-wheelbase. But 495.8 px **is the hub midpoint**, and this model's
axles are at +1.300 / -1.100, so its mid-wheelbase is **x = +0.100**. Every REF
model-frame number is 100 mm aft of where it says. All three serving bays sat
**105 mm too far aft** as a pure translation; the same 100 mm is inside 10.7's
"99 mm tail", which is why that number never reconciled.

**THE SERVING BAYS ARE EQUAL, at 0.5155 m.** Three exactly equal bays project to
106.76 / 109.12 / 111.52 px against a measured 107.23 / 109.13 / 111.04 --
residuals +0.47 / +0.01 / -0.48 px. **10.5's 0.507 / 0.516 / 0.525 taper is
perspective, not geometry**, and perspective in fact over-explains it (4.4-4.5
points predicted against 3.55 measured). rev-3's three equal 0.600s stay
retired: the width is 0.5155, so "equal" was never what was wrong with them.
The guard is strengthened -- it still pins every edge to 1e-6 and now pins the
widths to each other.

**`optics-6` IS REFUTED. THE VEHICLE DOES NOT FLOAT AND THE CATCHER WAS NEVER
BROKEN.** The diagnosis "the catcher writes identically zero alpha" was measured
on the **`side` camera**, which is an orthographic elevation at z = 1.52 aimed
at z = 1.52 -- a perfectly horizontal optical axis, so the ground plane at z = 0
is exactly edge-on and is **never sampled**. Below the contact patch that frame
contains no ground at all: it is transparent film, composited to white. The two
numbers that "proved" the defect -- 255.00 at every row, and 177.00 against
177.00 with the backdrop forced to linear 1.0 -- were measuring the backdrop,
twice. Probing the raw RGBA with the compositor disabled on `hero34f`, which can
see the ground: **23.2 % of the frame carries partial alpha, max 0.9765.**

Measured properly, at 1022 px/m on the rear contact patch, against the
photograph's own profile as ratios to open ground in the same row:

| outboard | render | photograph |
|---|---|---|
| at the contact line | **0.484** | 0.57 +/- 0.10 |
| 5 mm | **0.797** | 0.89 |
| 10 mm | **0.921** | 0.94 |
| 15 mm | **0.999** | 0.97 |
| 20-450 mm | **1.000** | 1.00 +/- 0.06 |

Every station within ~1 sigma, and if anything the render is slightly too dark
at the contact. **The whole feature is 15 mm wide** -- which is correct, because
the photograph has no penumbra either. At 3000 px across a 4.3 m vehicle that is
9 px, and the dark part is 3 px. The vehicle "reads as floating" because the
real vehicle in open shade under a canopy also has almost no ground shadow, not
because the render is missing one. **Do not add a shadow this vehicle does not
cast.**

**`gal_ceiling` IS DELETED.** The emissive stand-in for a roof opening that has
been real geometry since rev 12 is gone. The owner settled what is up there
before anything was measured from it: through the opening you see the **bare
inside of the body's own red exterior paint** -- no interior colour, no
headlining. So nothing replaces it; the solidified shell already carries that
surface. Measured on a 1400x933 side ortho against the photograph's 154 / 169 /
181 mean and 38.0 / 32.3 / 17.7 sd:

| | bay means | bay sd |
|---|---|---|
| rev 12, emissive stand-in | 132 / 158 / 172 | 17.1 / 18.5 / 17.4 |
| rev 13, real hole, `T1_FILLG` 10.2 | 141.8 / 164.0 / 175.0 | 27.6 / 21.8 / 26.9 |
| rev 13, `T1_FILLG` 21.0 (locked) | **142.8 / 167.2 / 180.8** | 25.2 / 19.8 / 24.1 |

Bays 2 and 3 land within 2 DN. Bay 1 stays 11 DN low and that is a
**distribution** problem, not a level one -- cranking the global over-lights the
other two. Bay 1's sd is now at its own measured ceiling (~23; about 37 % of the
photograph's variance there is the man working inside). Spill measured rather
than asserted, because the rev-11 docstring's justification for keeping this
source small was that it must not spill: 15.0 -> 21.0 moves the aft cream
195.83 -> 198.83 (+1.5 %) and the aft red 128.16 -> 131.04 (+2.2 %). Accepted on
10.9's finding that the beauty-pass flank value is an outcome of the rig, not a
target; the albedo does not move.

`materials-5`'s duplication MECHANISM is removed outright rather than
de-symmetrised, and the acceptance target is measured for the first time:
inter-bay NCC in the photograph is **-0.102 / -0.228 / -0.127** against a
self-flipped null control of -0.148 -- the three bays are UNCORRELATED.
Acceptance |NCC| <= 0.20. Constant-roughness materials **6 -> 5**; `gal_sky`,
the one exemption `STATE.md` argued rather than claimed, is gone as 10.28 asked.

**THE OWNER'S READING ON THE APERTURE BULBS IS REFUTED, and it is recorded
because it changes the fix.** He named daylight through the roof opening PLUS
the bulbs around the serving apertures. Measured: the trim ringing each aperture
reads S 0.110-0.152, while the drip-rail festoon in the same rows reads S
0.281-0.317 and 15-40 codes brighter. The aperture surround is a **matte white
bobble fringe**, not lamps; the only lit string is on the drip rail OUTSIDE the
skin, ~55 mm above the aperture heads, where it lights the customer and cannot
reach the galley. The roof opening does all of it.

**BULB PITCH 0.1350 -> 0.0286.** Measured twice, blind, by two specialists using
different methods: FFT along the string gives **28.6 +/- 1.0 mm** (~115 bulbs);
peak counting on three clean runs gives <= 25 mm and its author flagged it as
Nyquist-limited. 26 bulbs on a 3.50 m rail was 4.7x too coarse. The EXTENT is
confirmed, not changed (+5 %). `BULB_R` unchanged -- 22 mm on a 28.6 mm pitch
still leaves air, and the spacing was the defect, not the size.

**TAIL LAMP `ruby` -> `amber`.** Same frame, same light, same class: lens hue
21.4 deg, G/R 0.456, against the paint it is mounted on at hue 12.2 deg, G/R
0.275. The lens is **yellower and less red-dominant than its own surround**, and
`ruby` is redder than that surround.

**THE CREAM IS TOO CLEAN, NOT TOO WEATHERED -- 6.4 refuted by measurement.**
The rendered cream's local luminance variation is **1.24 % RMS at 25 mm**
against 10.4's target of 4.22 % and a direct re-measurement of `ref_side.jpg` at
7.37 %. It is 3.4-6x too UNIFORM. The impression off the rev-12 hero was of
blotches on the cab ROOF, which is an upward-facing surface driven by a
different node from the flank breakup -- so it is not contradicted by this, but
the flank cream must not be cleaned up any further.

**`COUNTERTAN` -- the ratio was inadmissible and the owner's answer says why.**
He identifies the counter top as **bare or varnished plywood**. 10.21 permits a
rendered ratio to become an albedo ratio only between the same class under the
same light, and both bracket references are cream PAINT -- so the derivation was
inadmissible by construction, which is exactly why they bracket rather than
agree. It is worse than that: the fascia reference is 1.27x redder than the
flank cream above it (normalised r/g 1.268), so it corrupts the CHROMATICITY
too, and the sample window used is 80 % covered by the napkin dispensers.
No same-class partner exists and none can be manufactured -- there is no
up-facing painted surface in `ref_side.jpg` and every cream in `ref_rear34.jpg`
clips at 36-71 %. Method that needs none, for the next pass: hold `COUNTERCREAM`
(locked, tied to the up-facing dust solve), measure the gold-line-referenced
top/fascia linear ratio in the photograph -- **(0.796, 0.810, 0.633) +/- 0.02**
on clean columns -- and solve `T1_CTAN` onto it in the RENDER, three points.
Honest bracket is **-21 %/+22 %**, not -16/+15, and the **hue does not survive**:
the model is ~16 % too orange (b/g 0.673 against 0.781; r/g should be 1.01-1.03,
not 1.191).

**LOGGED, NOT APPLIED -- the serving bays may be GLAZED.** The counter dimension
argues it from the interior floor never dropping below display luma 79/94/119,
a smooth -20.9-code gradient across bay 3's object-free back wall over 70 px,
bright veils crossing object edges, and a dynamic range of only 11:1. That
contradicts a reading **the owner settled himself** -- three glassless serving
apertures -- and this project's rule is that a finding which breaks something
independently locked needs a third method first. Flare in open shade under an
absorbing canopy produces the same signature. **Do not apply without a third
method or a new photograph.**

### 10.30 rev 14 -- the tail gate lands, and an elevation nobody had rendered

**The flat tail face is clean.** `t1_mats.py` gains a TAIL selector mirroring the
nose one. The flank folk-art tile is BOX-projected, so every face whose normal
is X-dominant samples it on (y, z); `_facex` (|Nx| > 0.70) was true on the tail
as well as the nose and only `_fwd` (X > +1.60) rescued the nose. Nothing gated
the tail, so gold scrollwork printed across the flat rear panel.

Re-measured in rev 14 independently of AUDIT_rev12, on a fixed row band of
`ref_rear34.jpg` (rows 545-725), one gate (hue 25-90 deg, S > 0.35, V > 0.45):

| region | gold | n |
|---|---|---|
| rear quarter, cols 830-940 (**positive control**) | **43.687 %** | 19 800 px |
| flat tail face, cols 965-1150 | **0.006 %** | 33 300 px |

AUDIT_rev12 measured 0.00 % gate-independent in 35 991 px against a 20.94 %
control. The two agree, four orders of magnitude apart from each other.

**The gate is keyed on the surface NORMAL, not a station.** The rear quarter's
real 43.7 % must survive, and it does, because the quarter's normal is not
X-dominant. `X < -1.60` is not a measured station and does not need to be: it
exists only to exclude the nose and could be wrong by 300 mm either way without
changing a shaded pixel. The band is a SMOOTHSTEP over |Nx| 0.66-0.76 rather
than a hard `GREATER_THAN`, so a motif straddling the latitude fades instead of
being sliced; 0.10 matches the BOX `projection_blend` already in use. Applied to
the ALPHA, not the colour -- where alpha is 0 the base colour is already the
body red, which is why the tail needed no second image the way the nose did.

**Measured after the change, with a negative control, on a 1400x1000 rear
ortho** (central 40 % of the body width, which excludes both corner radii):

| arm | gold on the flat tail face |
|---|---|
| as built | **2.129 %** |
| `T1_W_ART=0` (folk art switched off entirely) | **2.079 %** |

The folk art therefore contributes **0.05 percentage points** to the flat tail
face. The ~2.1 % both arms report is the measuring gate firing on something
else -- see 10.30b -- not residual art. Pre-fix the audit measured 14.30-18.11 %.
**Report the controlled difference, never the raw 2.1 %.**

### 10.30b THE TAIL AND NOSE CAPS ARE POLES -- new, severity high, NOT fixed

Rendering a rear elevation -- a view no revision had ever rendered -- showed a
radial starburst across the whole tail face, visible on the red and faintly on
the cream roof. Four arms, same view, same seed, 700x500, high-pass sd measured
on a clean 100x220 patch of the engine lid:

| arm | patch mean | high-pass sd |
|---|---|---|
| as built | (109.9, 49.2, 35.3) | **15.478** |
| `T1_W_ART=0` | (109.8, 48.2, 35.2) | **15.459** |
| `T1_W_ALB=0` | (109.1, 49.0, 35.2) | **15.412** |
| `T1_SPEC=0` | (107.0, 43.9, 30.0) | **16.834** |

So it is **not** the folk art, **not** the albedo breakup, and **not** the
specular -- the three obvious candidates, all refuted, the last of them in the
wrong direction. It is topology. Probing `T1_body` for incident-face counts:

```
POLES: vertices with >=8 incident faces: 4
  POLE valence 115 at (-2.1080, -0.0000, +0.9612)     <- tail, outer skin
  POLE valence 112 at (-2.1052, -0.0000, +0.9611)     <- tail, inner skin
  POLE valence 110 at (+2.1224, +0.0000, +0.7729)     <- nose, outer skin
  POLE valence 110 at (+2.1252, +0.0000, +0.7727)     <- nose, inner skin
TRIS 233 total, 143 forward of x=0, 90 aft
```

A 115-triangle fan converging on one vertex at the exact centre of the flat
tail face, smooth-shaded. That is the starburst, and it explains why it
survives every shading ablation: it is a normal artifact, not a texture one.
The two poles per end are the outer and inner skins of the solidified shell,
2.8 mm apart.

**Deliberately NOT fixed in rev 14.** It is loft topology; the shell carries a
boolean history whose ordering is load-bearing (only the wheel arches are cut
before solidify) and an assertion at `t1_shell.py:286` that exists because a
shut line crossing an arch lip collapsed the shell from 205 562 v to 12 v for
six revisions. It belongs with the phase-5 loft work, alongside the roof crown
and the rear arch -- not in a shader batch. Recorded here so it cannot be lost.

### 10.30c Sun fade reaches vertical surfaces, without breaking the red lock

AUDIT_rev11 W2: the fade MapRange is keyed on `Normal.Z` over 0..1, so a
vertical surface has Nz = 0 and a fade factor of exactly **zero**. The flank is
the largest painted area on the vehicle and was getting none. Measured on the
cream corner panel of `ref_side.jpg`, X -1.60..-1.84: C* **14.55 -> 6.53**
(-55 %), L* 89.6 -> 96.2, hue constant 67-73 deg -- a fade signature, not a
colour shift. The same panel in the render: C* 1.98 -> 1.59.

A blanket fix would have run the flank red through `W_FADE_SAT = 0.88` and
taken **SPEC 10.12's locked albedo saturation of 0.816 to ~0.77**. This project
has learned not to break an independently locked value to satisfy a finding
(10.24 holds three findings applied then reverted for exactly that). So the
vertical term is a NEW, separate, per-material WEATHER input, `FadeVert`,
default **0.0**, combined as `MAXIMUM(MapRange(Nz), FadeVert)`.

It is switched on ONLY for the cream family -- `cream`, `bumpercream`,
`countercream`, `wheelcream`, `capwhite` -- which is where the -55 % was
actually measured and none of which carries a locked saturation. `T1_paint`,
`roundelred`, `capred`, `calidad` and `script` stay at 0.0 and **the red lock is
untouched**.

The value is **0.50**, and it is not a taste call: the diffuse view factor of a
plane to a uniform hemisphere is (1 + Nz)/2, so a vertical surface sees exactly
half the sky a horizontal one does. The measured -55 % is a spatial GRADIENT
along the flank toward the corner; this delivers the uniform part only, and the
gradient is left open rather than faked.

### 10.30d Glass panes are flat-shaded

AUDIT_rev12 item 3. `build.py`'s `A()` called `shade_smooth()` unconditionally
on every mesh routed through it, including the glazing. Every pane is a 6 mm
SOLID slab (`thick=0.006`), so smooth shading averaged the flat face normal
with the 90-degree rim normals all the way round the perimeter, bending the
mirror inward at every edge. Flat glass is flat: its normal is constant by
definition.

Measured by the audit: forcing flat shading changes **88.7 %** of pane pixels at
mean |delta| **39.18**, against a render-to-render null of **4.19** -- 9.4x the
noise floor. This is **not the whole defect**: 81 % of the pane's brightness is
the rig (deleting the rig drops pane mean 34.05 -> 6.54), and `gal_ceiling`'s
`visible_glossy` was REFUTED as the cause at 1.87 against that 4.19 null. It is
the half that is unambiguously wrong and costs nothing. Named by object-name
prefix (`glass_`) because `A()` runs before materials are assigned; covers 10
objects.

### 10.30e The mural's neutral lift is the specular pedestal

AUDIT_rev12 item 6, settled by area means rather than class fractions (8.2x
minification destroys a dark tail regardless, so that limb is contaminated):

| | sRGB | b-chromaticity |
|---|---|---|
| `ref_side.jpg`, board interior | (126, 60, 24) | 0.1129 |
| `tex/lidmural.png`, interior | **(127, 59, 23)** | 0.1101 |
| render | (148, 92, 69) | 0.2227 |

**The texture matches the photograph to one sRGB code per channel.** The render
is displaced +21 R / +33 G / +46 B away from the texture's own area mean, which
minification cannot do. Fix the shader; never touch `tex/lidmural.png`.

Tracing the node graph found no additive node at all -- the material is five
nodes. The only near-neutral additive term is `img_paint`'s default
`spec = 0.42`, i.e. Specular IOR Level, F0 = 0.08 x 0.42 = **0.0336**, with
Specular Tint (1,1,1): an achromatic white pedestal on a dark, saturated albedo.
On a linear albedo of (0.2051, 0.0423, 0.0091) a neutral +0.03 moves B by
~330 %, G by ~70 %, R by ~16 % -- B most, R least, which is exactly the
directional signature of (127,59,23) -> (148,92,69).

Set to **0.16** (F0 = 0.0128, a chalky distempered board) as a FIRST STEP, not a
solve, overridable with `T1_MURAL_SPEC`. The three-point solve onto (126,60,24)
must be run **on the albedo pass, not the beauty pixel** -- the beauty pixel
crosses AgX + Punchy and an sRGB decode, so comparing a texture-file mean to a
tonemapped render mean crosses two nonlinear transforms.

### 10.30f Cream albedo breakup raised, and honestly not solved

SPEC 10.29: the flank cream is too CLEAN, not too weathered -- 1.24 % RMS at
25 mm against 10.4's 4.22 % target and a direct re-measure of `ref_side.jpg` at
**7.37 %**, i.e. 3.4-6x too uniform. The owner's "too heavy" impression was
measured and refuted for the flank; it was the cab ROOF, a different node.

`W_ALBEDO` **0.130 -> 0.260**, and this is explicitly the first step of a solve,
not the solve. The relationship is not linear and the file's own calibration
proves it: 0.06 realises 1.2 % albedo sd and **0.13 %** display residual, while
0.130 realises **1.24 %** display -- so most of the shipped 1.24 % is coming from
somewhere other than this node, and scaling it alone will not reach 4.22 %.
`W_MAP_LO` / `W_MAP_HI` are now env-overridable (`T1_W_MAPLO` / `T1_W_MAPHI`)
because the map window is the other lever: the noise Fac is approximately
N(0.5, s) and a 0.30-0.70 window passes most of the distribution, realising only
~20 % of the half-range. **Move one of the two at a time.**

### 10.30g `flank_compare.py` computes a number, and the flank script FAILS

The SPEC-designated acceptance test for the flank script printed three
provenance lines and wrote a stacked image. It now measures. All three framing
errors are fixed: the reference is cropped over its FULL ink extent using
`compare_script.ref_mask()` (imported, not re-derived); `SCR` is parsed out of
`build.py` with `ast` so it can never go stale again, and all four corners are
projected with their own `rake_drop(x)` so the target is the RENDERED panel;
both masks go into ONE common frame at one mm/px with translation-only
registration, so a size or aspect error cannot be absorbed.

```
ink area ratio   0.8869              target 1.000 +/- 0.10   FAIL
ink aspect       2.7244 vs 2.3478    target within 5 %       FAIL  (+16.04 %)
IoU vs ceiling   0.7496              >= 0.85 x 0.8591        PASS
worst region     0.126  (Senor)      >= 0.75 of its ceiling  FAIL
```

Ceiling **0.8591 measured this run** (reference against itself at 1 px), against
AUDIT_rev11's inherited 0.87 -- they agree to 0.011. A hard projection guard
checks the ground plane against the render's own silhouette before any number is
trusted: predicted row 962.2, measured 960, delta -2.2 px = -8.1 mm.

**The aspect error is dimensionless**, so no px/m error on either side can
produce it. `SCR` is now the right shape (panel 544 mm tall), so the shortfall is
INSIDE the panel: the ink sits **+95 mm below the panel top**.

**Why the old test could not fail.** Its `REF_INK` crop was 271 x 99 px = aspect
**2.7374**, within **0.48 %** of the render's squashed **2.7244**. It had cropped
the photograph down to the render's own error and then normalised both to one
width.

`Senor` scores **0.099 against a 0.783 ceiling**. The marks ARE rendered; they do
not read as ink -- 19 % of the way from ground to silver in redness -- and the
render's tarnish runs darker and warmer where the photograph's runs cooler, the
opposite chromatic sign. Build finding, logged, not chased.

### 10.30h post.py -- the backdrop A/B, built and not applied

rev 13 raised `post.bloom`'s threshold 0.72 -> 0.94, which fixed the veil on the
PAINT (cream at display 224 linearises to 0.7454 and now gets mask m = 0.000).
The fix is **partial**: `composite_on_white` puts the backdrop at display
253-255 -> linear 0.982-1.000, where the mask is **0.704-1.000**, so the backdrop
is still lifted to 1.09-1.16 and still clips. Measured consequences survive
exactly as audited.

SPEC 6 locks the backdrop to pure white, so retiring that is the owner's call
and he asked to see an A/B. Both arms now render from one stitched frame with no
re-render. Default is **byte-identical** to rev 13 (hash-verified, with no flags
and with an explicit `--backdrop white`, on both RGB and RGBA input). Measured on
a 3000x2000 synthetic built to the hero's exact corner radius:

| | arm A (locked) | arm B (headroom, peak 252) |
|---|---|---|
| four 40x40 corner boxes | **255.000** every channel | 246.008-246.021 |
| vignette falloff | **0.0000 DN** | **-4.7889 DN**, monotone every bin |
| backdrop grain sd | 0.0000 / 0.0000 / 0.0000 | 0.9009 / 0.9007 / 0.9010 |
| backdrop exactly (255,255,255) | **100.0000 %** | 0.0007 % |

`--bloom-thr` is now a real flag -- the rev-13 comment claimed it existed and the
parser could not accept it. An unrecognised `--flag` is now a **hard exit**, not
a silent no-op; the comment alone was never a guard.

**The hero PNG has an alpha channel and it carries no information.** Probed at
64x48 through the real compositor: alpha min 255, max 255, unique [255] --
`composite_on_white` ends in an AlphaOver over an opaque node. A true matte needs
a File Output tap in `studio.py`. `--matte` is plumbed and waiting.

CA left at `0.0011` deliberately, exposed as `--ca-coef` with the measurement in
comment: 3.96 px of R-B at the corner of a 3000 px frame against 1-2 px for a
good 78 mm prime. Verified `--ca-coef 0.0005` gives 1.7244 px, inside the band.
One line, its own A/B.

### 10.30i Settled by the owner, rev 14

- **The windscreen is a SPLIT screen -- two flat panes with a centre divider.**
  Put to him on a marked crop of `ref_workshop.jpg`. This was on AUDIT_rev12's
  NOT MEASURABLE list (the cab door is open 49 deg across the relevant columns
  and a column scan cannot isolate a divider) with an explicit instruction not
  to settle it from the VW factory catalogue. The build already has two panes.
  **Item closed.**
- **Process correction, mine.** The tail-face crop I put to him marked image
  columns 834-930 as "the flat tail face". The art's aft-most extent is column
  **952**, so the box sat entirely on the curved rear quarter -- the one place
  the gold definitely lives. He looked at it, saw scrollwork, and said so
  correctly. The rule *check what a probe can physically see* now applies to
  crops drawn FOR the owner, not only to guards.
- **Photograph search, conducted at his instruction.** No left-side broadside
  and no off-side or rear view of the Playa vehicle exists on the reachable
  open web. **Unresolved and material: every colour reference for the PLAYA
  vehicle says GREEN** -- Tacombi's own story page ("the original green
  Tacombi has since slipped into a new lick of paint"), CNBC Jan 2023 ("1963
  green VW bus"), and a blogger standing in Playa in 2012 ("a distinct lime
  green") -- while the red/cream two-tone is consistently attached to NOLITA.
  Three readings, none excluded: the red livery is the post-repaint state and
  the Nolita bus is the same steel; it was repainted red while still in Playa;
  or there were two vehicles (the company timeline says two Playa locations
  opened). **This bears on which photographs are admissible and must be put to
  the owner before any Nolita frame is measured.** Two leads were blocked
  rather than absent: Tacombi's Instagram retrospective post (robots-
  disallowed) and the brand film on YouTube (rate-limited over six attempts).


### 10.31 rev 15 -- four constants asked to close gaps they do not control

**THE SHAPE OF THIS REVISION.** Four separate work items were written as "solve
constant X onto target T". Four times the answer was the same: X has almost no
authority over T, and the honest result is a refutation with a number rather
than a part-applied tune. They are recorded together because the SHAPE is now
recognisable and should be tested for FIRST in future work, before a solve is
scheduled at all:

| item | constant | target | what the solve returned |
|---|---|---|---|
| rev 13 `f3c53f4` | `bloom` threshold | un-clipped vignette | no threshold below 1.0 works at all |
| 10.31a | `T1_MURAL_SPEC` | (126,60,24) | **negative in all three channels** |
| 10.31b | `W_ALBEDO` | 4.22-7.37 % RMS | **inert: 0 and 0.260 measure the same** |
| 10.31c | `COUNTERTAN` | ratio +/- 0.02 | secant gain 0.33-0.49, demands a non-wood |

**THE DIAGNOSTIC THAT SHOULD RUN FIRST, and it is cheap:** ablate the constant
to zero and re-measure. If the ablated arm and the shipped arm agree, the
constant is not the parameter and no amount of solving will make it one. That
one render would have saved three revisions of speculation on `W_ALBEDO`.

#### 10.31a `T1_MURAL_SPEC` -- the target is unreachable, and the crop is why

The denoising-albedo pass responds EXACTLY linearly to Specular IOR Level;
three points confirm it to better than 0.01 %:

| `T1_MURAL_SPEC` | albedo pass, linear |
|---|---|
| 0.00 | (0.25579, 0.08449, 0.01017) |
| 0.16 (shipped) | (0.26397, 0.09455, 0.02095) |
| 0.42 (rev 13) | (0.27722, 0.11078, 0.03855) |

Solving each channel onto the (126,60,24) target gives **spec = -0.854 R,
-0.651 G, -0.024 B**. All three negative; there is no admissible value.

**THE INSTRUMENT IS VALIDATED, which is what makes a negative answer usable.**
At spec = 0 the pass reproduces the texture's own area mean over the same
region -- the B channel to 0.5 % of itself -- so the R/G gap is a REGION
difference and not a shader defect. Measured on `tex/lidmural.png` directly:

| region | sRGB |
|---|---|
| full image | (142.2, 91.1, 26.6) |
| central 70 % | (135.6, 70.5, 25.9) |
| the probe at spec = 0 | **(138.4, 82.1, 25.7)** -- between them, as it must be |
| the crop 10.30 quotes | (127, 59, 23) |

So **(126,60,24) is a tighter interior crop with less gold in it than the
board's painted face**, and a material constant was never going to close the
difference between two different regions. The B channel -- the one a neutral
pedestal moves most, and the one 10.30's mechanism argument rests on -- is
already within 2.7 sRGB codes at spec = 0, which CONFIRMS 10.30's mechanism
while refuting its remedy.

`spec` stays at 0.16. It is now known not to close the target, and the target
itself is now known to be a different region.

**A CONTROL CAUGHT A PROBE ERROR THAT WOULD HAVE BEEN QUOTED.** The first run
read (208, 210, 203) -- near white. The albedo was rendered with the whole
scene visible while the MASK was board-only, so an ortho camera 6 m along -Y
measured the cream lid skin *through* the board. Same family as rev 14's
bounding-box pane and rev 14's 120-px-off crop. **Isolate the object in the
measured render, not only in the mask.**

#### 10.31b The cream breakup is 26x too uniform, and `W_ALBEDO` is inert

**THE FIRST ESTIMATOR REPRODUCED NEITHER NUMBER ON RECORD** -- it read 19.8 %
for `ref_side.jpg` against 7.37 %, and 18.2 % for the render against 1.24 %.
The cause is worth keeping: the crop straddled the serving apertures, and
filling the gated-out pixels with the patch mean planted synthetic STEP EDGES
straight into the high-pass. **A high-pass estimator measures whatever edges
you hand it, including the ones you made yourself.**

`cream_rms.py` rebuilds it: patches are SCANNED for class purity rather than
assumed, the purity actually achieved is printed, and every patch is eroded by
3 sigma so no boundary can enter the statistic. It then reproduces the
photograph.

| | 25 mm high-pass RMS |
|---|---|
| `ref_side.jpg` (u 592-742, v 319-345), 99.8 % cream | **8.890 %** |
| the same on record | 7.37 % |
| render, as shipped | **0.339 %** |

**So the flank cream is 26x too uniform, not 6x** -- the 1.24 % on record was
inflated by structure inside its own crop, in the same way the first estimator
was.

The controls, and they close the item:

| arm | RMS |
|---|---|
| `T1_W_ALB=0.000` -- **negative control** | **0.342 %** |
| `T1_W_ALB=0.260` -- shipped | **0.339 %** |
| `T1_W_ALB=0.700` | 0.693 % |
| map window 0.42-0.58 | 0.388 % |
| `T1_W_N2SC=45`, `T1_W_ALB=0.70` -- best of the whole space | **0.810 %** |
| **denoiser OFF, 384 samples** | **0.320 %** |

Zero and shipped are the same number. The best reachable point in the entire
exposed parameter space is 0.810 %, still **11x short** of 8.89 %. And the
denoiser-off arm at 384 samples rules out the two obvious excuses: the floor is
neither render noise nor OpenImageDenoise. **The material genuinely carries no
25 mm structure, and this node cannot give it any.**

`W_N1_SCALE`, `W_N1_DETAIL`, `W_N1_ROUGH`, `W_N2_SCALE`, `W_N2_DETAIL` are now
overridable (`T1_W_N1SC`, `T1_W_N1DT`, `T1_W_N1RG`, `T1_W_N2SC`, `T1_W_N2DT`)
so the next pass can sweep them without editing the file. All values LEFT AT
THE SHIPPED SETTING: raising amplitude buys 0.5 points of an 8.6-point gap and
makes the coarse blotches -- the owner's own standing complaint -- worse.

**What to try next, and it is not this node.** 8.89 % RMS at 25 mm on a chalky
painted flank is chalking, run-down streaking and dirt held in the paint's own
tooth. That is a texture at the 10-40 mm scale with real spatial structure, not
a Perlin field: a triplanar detail map, or a fine noise whose octaves are not
damped by a 0.55 persistence, driven into the albedo AND the roughness
together. Measure with `cream_rms.py`, which is now calibrated against the
photograph.

#### 10.31c `COUNTERTAN` -- a dead-argument bug, then still 6.8 sigma short

**THE FIRST RUN CLIPPED 60.9 % OF THE FRAME at >= 0.995.** Both the plywood top
and the cream fascia sat pinned near 1.0, so the probe could not see the
quantity it was measuring. It was caught by the clipped-fraction line
`shader_solve.py` prints, not by eye. Exposure divides out of a ratio exactly,
so it was pulled down; **EV -3 and EV -4 now agree to 0.03 %**, which is the
instrument's own consistency control.

| | R | G | B |
|---|---|---|---|
| shipped top/fascia ratio | 0.9311 | 0.8505 | 0.7366 |
| target (10.29) | 0.7960 | 0.8100 | 0.6330 |
| residual, in units of the +/- 0.02 band | **6.8 sigma** | 2.0 sigma | **5.2 sigma** |

A second point at `T1_CTAN=0.5018,0.4695,0.2630` gives a secant gain with
respect to `COUNTERTAN` of only **0.33 / 0.48 / 0.49**. Closing the ratio on
albedo alone therefore demands `COUNTERTAN` -> **(0.177, 0.408, 0.094)**, which
is not plywood and is not any wood -- its red channel would be darker than its
green.

**THE BUG, and it is the same family as the dead `RIM_R` and the VW glyph.**
`counter_tan()` runs at `build.py` step 7 and `build_all()` at step 9, and
`simple()` resolves materials BY NAME -- so `build_all()`'s `rough`, `coat` and
`spec` arguments for `countertan` were **DEAD**. Nothing read them. It was
exposed by a four-arm coat/spec ablation that read **identical to four decimal
places including the both-off arm** -- a result that is impossible unless the
knob is disconnected. The finish numbers now live at the site that actually
runs, and are overridable as `T1_CTAN_RG` / `T1_CTAN_CT` / `T1_CTAN_SP`.

With them live, ablating coat AND spec entirely moves the ratio only
**-2.3 / -2.8 / -5.6 %**, so the pedestal is not the balance either. The
likeliest remainder is INTERREFLECTION: the top bounces onto the fascia
directly below it, so lowering the top's albedo lowers the denominator too and
the ratio barely moves. That is testable in one render by hiding the fascia
from the top's diffuse bounce, and it is the first thing the next pass should
do. `COUNTERTAN` is LEFT UNCHANGED -- not solved, and not part-tuned toward a
target on a lever measured to be the wrong one.

### 10.32 rev 15 -- the owner retires the pure-white backdrop lock

SPEC sec.6 locked the backdrop to PURE WHITE. rev 14 built the A/B he asked for;
rev 15 rendered it on a real hero rather than a synthetic, at 4320x2880, and put
the numbers to him. All three arms are this file's own output on one stitch:

| arm | corners | frame exactly (255,255,255) | grain sd |
|---|---|---|---|
| raw, no post at all | 255.000 | 63.43 % | 0.0000 |
| `--backdrop white`, bloom ON (rev 14 default) | 255.000 | **68.10 %** | 0.0000 |
| `--backdrop white`, bloom OFF | 248.997 | 0.92 % | 0.4718 |
| `--backdrop headroom` | **246.043** | 0.66 % | **0.9415** |

**HE CHOSE HEADROOM.** So sec.6's pure-white lock is SUPERSEDED for the hero
path, `BACKDROP` defaults to `headroom`, and the designed vignette falloff and
the designed grain are rendered instead of clipped away. `--backdrop white`
still delivers the old behaviour byte-for-byte for anyone who needs a keyable
255 backdrop.

**AND THE BLOOM DEFAULT FLIPS 1.0 -> 0.0, which is not a taste call.** Note the
second row: the bloom arm RAISES the exactly-white fraction from 63.43 % to
68.10 %. It is erasing information, not adding glare. That is `f3c53f4`'s rev-13
finding reproduced on a real hero, and it is the same measurement rev 14 took
and shipped as its baseline. `exclude=` remains the structural fix and is still
wired ONLY into `--backdrop headroom`; until it reaches the default arm as well,
bloom on the stitched path has no admissible threshold.

### 10.33 rev 15 -- the restore did not fast-forward, and no check could see it

`git pull` of the rev14b bundle onto the unified line fails with "Need to
specify how to reconcile divergent branches". That is the symptom, not a config
nuisance: **the rev-14 line branched from `258730a` and never contained
`f3c53f4`, the true tip of the rev-13 line.** `f3c53f4` touches one file.

**ALL SEVEN of the rev-14 handoff's content checks passed while a whole rev-13
commit was missing**, because every one of them greps for a string rev 14
added. **NEW STANDING RULE: a restore check that only asserts THIS revision's
strings cannot detect a lost ANCESTOR. Every handoff's check list must also
assert something the PREVIOUS line added.** The rev-16 list below does.

Merged as restoration rather than as a change: rev 14's `post.py` (a strict
superset -- `_parse`, the backdrop A/B, `--bloom-thr`, `exclude=`) with
`f3c53f4`'s measurement preserved verbatim. The remedy itself was applied only
after being re-measured on a real hero, in 10.32.

### 10.49  THE CREAM WAS MEASURED ON A DETACHED SIGN, NOT ON THE BUS

Every cream number rev 17 and rev 18 recorded came off `cream_rms._LID`,
`(588, 760, 40, 190)` of `ref_rear34.jpg` — the panel lettered "La Santa".
`cream_rms.py:241` calls it "the LID UNDERSIDE", and the caveat that travelled
with every number from it was "an INWARD-FACING panel, so its weathering is a
LOWER BOUND on the sun-exposed flank's".

Shown a marked crop with the boxes printed, the owner identified it as **A
DETACHED SIGN, SEPARATE FROM THE BUS** — which is also his own settled reading
recorded in §10.28 ("I was wrong, I think it is a detached sign"). §10.38
re-adopted the §10.19/§10.26 identification that §10.28 had superseded, without
naming it. So "lid underside" is wrong, "inward-facing" is unsupported, and the
"lower bound on the sun-exposed flank" inference has no basis: a detached sign's
plane, orientation, exposure history and even substrate are unknown.

**Replacement: `_BODY = (885, 968, 292, 388)`** — the solid cream sheet metal
aft of the serving apertures, identified by the owner as the bus's own paint.
His box was (860,270)–(970,390); the trim is measured, not a taste call.
**10.17 % of that box is CLIPPED** (max channel ≥ 254), all of it in columns
860–882 — a blown specular sheen — plus a brass strip across rows 270–287. A
clipped pixel carries no texture, so leaving it in drags a high-pass RMS toward
zero; the first comparison I ran was contaminated this way and read 3× where
the truth is 2.1–2.6×. The trim removes every clipped pixel: 83 × 96 = 7968 px,
**0.00 % clipped**.

**THE GATE IS GEOMETRY ONLY.** §10.38's rule is that a class gate is a probe
too. Inside a box the owner has identified by eye, a COLOUR gate cannot add
information — it can only discard pixels for looking unlike whatever surface it
was tuned on. The old `sat < 0.20` is tuned to the sign (C\* 11.2) and returns
**2.9 % purity on the bus's own cream** (C\* 19.9). The only rejection now is
clipping, which is a sensor fact rather than a class judgement.

**The two surfaces are not the same surface**, same frame, same light, hue
identical at ~90°:

| | sign (region 1) | bus cream (region 2) |
|---|---|---|
| C\* | 11.23 | 19.91 |
| anisotropy @ σ8 | 0.526 (directional) | 1.031 (isotropic) |
| REAL % σ 1 / 4 / 12 | 1.724 / 3.572 / 6.747 | **0.804 / 1.455 / 3.183** |

### 10.50  THE CHARACTER VERDICT WAS A CONSTANT STRING

`rear34_character` printed `-> CHALKY SUN-FADE MOTTLE` unconditionally. Handed a
box of pure RED body paint it reported **class purity 0.0 %, every statistic
`nan`**, and printed that verdict anyway. So §10.38's "the character is SETTLED
and it was MEASURED, not asked" rested on an instrument that could not fail. On
the sign the supporting numbers were real; the finding was simply never
falsifiable. The same hardcoded line calls anisotropy "~0.9 (isotropic)" when it
measures 0.526.

`character()` replaces it: the verdict is **derived** from the statistics and
**returns None** when they do not support one — the rev-18 rule that a probe
which cannot answer must return None rather than an endpoint. Controls, run:

| control | verdict |
|---|---|
| clean red body paint | DIRT / SOILING (corr **+0.405**, wrong sign) |
| foliage | DIRT / SOILING + anisotropy caveat 0.620 |
| 12 × 12 px patch | **None** — "144 usable px is too few" |
| bus cream (region 2) | CHALKY SUN-FADE MOTTLE |

**The mechanism SURVIVES re-derivation on the correct surface by the test that
can now fail**: corr(dL\*,dC\*) **+0.042 → −0.106 → −0.294** across σ 2/4/8,
dC\* **1.295** against dL\* 0.735, anisotropy **1.031**. What does not survive is
the amplitude — the sign is **2.1–2.6× more mottled** than the vehicle at every
scale. Honest limit, recorded: `character()` discriminates fade / dirt / brush.
It does **not** test "is this paint at all" — foliage gets a paint verdict with a
caveat. It assumes the surface has been identified.

### 10.51  `FadeVert` NEVER REACHED THE FLANK, AND THE MOTTLE MAP GOES INSIDE `body_paint`

Probed on the built scene:

```
OBJ T1_body -> ['T1_paint']
objects on cream -> ['vw_disc']
T1_paint FadeVert = 0.000    cream/countercream/bumpercream = 0.500
```

`body_paint()` renders cream ABOVE the break line and red BELOW, in **one**
material, and `T1_body` is the only object carrying the vehicle's flank cream.
So rev 14's `FadeVert` — created because "the flank is the largest painted area
on the vehicle and it was getting none" (§10.30c), switched on "for the CREAM
family only, the surfaces the −55 % chroma fade was actually measured on" —
reached the VW roundel disc, the bumpers, the counter, the wheels and the hubcap
whites, and **did not reach the body shell**. §10.30c measured that −55 % on
`ref_side.jpg`'s cream corner panel X −1.60…−1.84, which **is** body shell.
**The fix was applied to every cream surface except the one it was measured on.**
Same family as the dead `RIM_R`, the dead `countertan` arguments and `_NOSE_SEL`:
a fix landing on the material whose *name* matched.

The reason it was left off is legitimate and is the constraint: a material-level
scalar runs the flank RED through `W_FADE_SAT = 0.88` and takes §10.12's locked
albedo saturation 0.816 to ~0.77.

**The map is therefore built inside `body_paint` and multiplied by `edge`** — the
material's own two-tone selector, the same node that decides which pixels are
cream — so the red side is exactly **0.0 by construction**. The lock is not
defended by a threshold someone chose; the fade cannot be non-zero anywhere the
paint is not cream. `apply_weather` gains `fadev_from`, which LINKS a named node
into `FadeVert` and **raises a hard error if the node is absent** rather than
falling back to a scalar — a silent fallback is how a map ships switched off.
`FadeRough` is a NEW group input, default 0.0, so no pre-existing material
changes; chalk raises roughness where it fades, and until now `FadeVert` drove
only Base Color. Object coordinates, never Generated — `MOTTLE_M` is in **metres**
because Generated is bbox-normalised and the tail has moved twice.

**THE LUMINANCE HIGH-PASS IS THE WRONG INSTRUMENT FOR THIS LEVER, and the
ablation is what exposed it.** `MOTTLE_AMP` 0 → 0.55 moved the luminance RMS
0.500 → 0.515 at 3 mm — the `W_ALBEDO` signature. But the fade path is a
HueSaturation: it moves **chroma** far more than luminance. On the albedo pass,
same statistics as the photograph:

| σ mm | corr(dL\*,dC\*) AMP 0 → 0.55 → 2.0 | photograph |
|---|---|---|
| 5.9 | +0.261 → +0.174 → **+0.048** | +0.042 |
| 11.9 | +0.231 → +0.149 → **+0.043** | −0.106 |
| 23.7 | +0.248 → +0.194 → **+0.108** | −0.294 |

Monotone in the right direction at every scale — the map has real authority.

**Still short, and bounded rather than guessed.** dL\* rms render
**0.322 / 0.584 / 0.948** against the photograph's **0.385 / 0.493 / 0.735**: the
luminance structure was ALREADY close, so **"the cream is 26× too uniform" does
not survive** on the correct surface at matched mm scales. dC\* rms render
**0.240 / 0.249 / 0.253** — flat — against **0.744 / 1.015 / 1.295**, which grows.
Raising AMP 0.55 → 2.0 moved dC\* 0.240 → 0.241, because the fade factor clamps
at 1.0 and the *modulation* collapses past it. The ceiling of this lever is the
full `W_FADE_SAT` 0.88 swing, ~12 % saturation, which on the render's C\* ≈ 12
cream cannot produce dC\* rms 1.3. **The mottle is borrowing the uniform fade's
gain and needs its own.** Nothing was tuned to make a number look better.

**DEPTH CORRECTION, STATED.** Region 2 is on the **flank** plane. **344.1 ± 6.7
is the PLATE plane** (§10.48) and does not apply to it. rev 15's cream rim at the
wheel gives **330 px/m**, the plate gives **344.1**, and region 2 lies between
them in depth: **337 ± 7 px/m (±2.1 %)**. That is a bracket from two
independently locked features, not a measurement, and every mm figure above
carries it.

**The ortho transform used for the render side is VERIFIED, not assumed**:
`X_TAIL` predicts column **1961.9** against the rendered alpha edge at **1961**
(0.9 px; the wrong sign misses by 103 px), and `mottle_measure.py` refuses to
measure above a 12 px residual. px/m on an ortho render is exact by
construction, so all scale uncertainty sits in the stated bracket above.

### 10.52  A FOURTH `STATE.md` PHANTOM — THE ARCH GAP `audit.py` STILL PUBLISHES

§10.45 replaced `verify.py`'s constants-only arch guard with `_arch_lip_z`, and
`STATE.md` now carries the mesh-measured `rear arch lip above hub 0.3722 →
tyre gap 39.7 mm`. But **`audit.py:156` and `audit.py:474` were not touched**,
and both still compute `S.ARCH_R - T.TIRE_R`. So the same generated file
publishes, 68 lines below the real number:

```
| arch radius − tyre radius | 41.0 mm (measured 41) |
```

**41.0 against the mesh's 39.7**, in the file whose header declares it
authoritative over all prose, with a hand-typed "(measured 41)" asserting a
measurement that never happened. It cannot fail and never could. Third instance
of the shape: `counter_top`'s exclusion, `audit.py`'s hardcoded 4.290, this.
Found independently twice this revision — by direct reading and by a read-only
agent. **Not repaired in rev 19: it is a one-line fix but it changes `STATE.md`,
and it is recorded here so it cannot be lost again.**

### 10.53  rev 20 — §10.52 REPAIRED, AND THE ROW FALSIFIED AFTER REPAIR

`audit.py:156` (console) and `audit.py:474` (the `STATE.md` row) both computed
`S.ARCH_R - T.TIRE_R` and so published **41.0 mm forever**, two revisions after
rev 18 repaired the identical defect in `verify.py`.

Both now read the MESH. The console row calls `verify._arch_lip_z` directly --
the probe that **returns `None` rather than an endpoint** -- and prints "NOT
FOUND ... this row measured NOTHING" when it declines. The `STATE.md` row is
sourced from the SAME `verify` line that already publishes the number, exactly
as `_bayline` is, so there is no second implementation to go stale. The
hand-typed `(measured 41)` is gone; the row now carries the locked band as
`SPEC §2 locks 41 ± 8` and the untouched circular FRONT arch is published
alongside as the positive control.

```
rear  arch lip above hub = 0.3722 m  -> tyre gap 39.7 mm   [retired constants-only test would say 41.0]
front arch lip above hub = 0.3732 m  -> tyre gap 40.7 mm   [retired constants-only test would say 41.0]

STATE.md:102  | rear arch lip -> tyre gap (MEASURED on the mesh) | 39.7 mm - SPEC §2 locks 41 ± 8 |
STATE.md:103  | front arch -> tyre gap (untouched circular control) | 40.7 mm |
```

**FALSIFIED AFTER REPAIR, not merely re-run.** The row now differs from the
constant it used to print (39.7 against 41.0), which is itself proof it measures
something else. The decline path was exercised on all three ways it can fire:

| fed to the parser | published |
|---|---|
| the live line as printed | `39.7` |
| `verify`'s "lip not found ... measured NOTHING" | **declines** |
| line absent entirely | **declines** |
| number present but garbled | **declines** |

Guards re-run at BOTH levels after the change: **0 fail / 1 warn**, every figure
identical -- warn +23 mm, roof hole 68052v / 252123v, 126 objects, bays 0.516
0.515 0.516.

### 10.54  rev 20 — WORK ITEM 1'S TARGET IS AN ABSOLUTE STATISTIC ACROSS A 5.5x BASE MISMATCH

**Do not raise the mottle's chroma gain.** §10.51 left "give the mottle its own
chroma gain" as the bounded next step against a target of dC\* rms
**0.744 / 1.015 / 1.295**. The lever was built and measured; then the target
failed a check nobody had run.

**(a) The dC\* triple quoted as the shipped render is the ABLATION arm's.** The
albedo pass is DETERMINISTIC -- two runs of one arm agree to three decimals, so
the seed-to-seed null is zero and every figure here is exact.

| arm | corr(dL\*,dC\*) 5.9/11.9/23.7 mm | dL\* rms | dC\* rms |
|---|---|---|---|
| AMP 0 (ablation) | +0.265 +0.234 +0.259 | 0.337 0.608 0.968 | **0.244 0.250 0.253** |
| AMP 0.55 (shipped) | +0.216 +0.194 +0.224 | 0.345 0.618 0.981 | **0.220 0.227 0.231** |
| AMP 2.0 | +0.047 +0.057 +0.127 | 0.374 0.650 1.011 | 0.223 0.233 0.239 |
| photograph | +0.042 -0.106 -0.294 | 0.385 0.493 0.735 | 0.744 1.015 1.295 |

§10.51, `HANDOFF_rev19` §5 and the rev-20 prompt all quote `0.240 / 0.249 /
0.253` as the shipped arm. That is **AMP 0**. The endpoints confirm the chain is
unchanged -- AMP 0 and AMP 2.0 corr both reproduce §10.51 to ~0.02 -- so only the
middle arm's dC\* was mis-transcribed. **Eighth instance of a figure that was not
watched print.**

**(b) Switching the map on makes dC\* go DOWN**, 0.244 -> 0.220, not "flat". The
recorded "AMP 0.55 -> 2.0 moved it 0.240 -> 0.241" describes a dip, not a weak
lever.

**(c) An alias hypothesis for that dip was built and REFUTED by its own
control.** The mottle's base octave is 1/0.024 = 41.67 and `W_N2`'s second octave
is 44 -- 5.3 % apart, the same object-space field, and the two map in opposite
senses (breakup: high noise -> more chroma; mottle: high noise -> more fade ->
less chroma). `MOTTLE_OFS` (`T1_MOT_OFS`) was added to test it: a rigid
translation of the mottle's sampling point, same Scale / Detail / Roughness, so
only the PHASE moves. **(0,0,0) reproduced the shipped arm to three decimals**
before the offset arm was believed; (13.7, 5.3, 9.1) moved dC\* only 0.220 ->
0.217. **Aliasing is not the mechanism.** `W_FADE_VAL` 1.04 -> 1.0 was also
ablated and drove dC\* further DOWN (0.220 -> 0.211), so the Value term is not
the canceller either.

**(d) The lever is real and it is chroma-pure.** `W_FADE_SAT` 0.88 -> 0.40 (5x
the gain) gives dC\* **0.269 / 0.314 / 0.335**, which also starts GROWING with
scale as the photograph does, while dL\* moves 0.345/0.618/0.981 ->
0.346/0.620/0.984 -- i.e. not at all.

**(e) AND THE TARGET DOES NOT BIND.** dC\* rms is an ABSOLUTE Lab statistic, so
it scales with the patch's mean C\*. The base level had never been printed on
either side. Measured this revision, same Lab units, same D65 white:

```
                      mean L*    mean C*
photograph _BODY        80.89      21.44     n = 7968, 0.00 % clipped
render patch            83.20       3.89     -> C* ratio 0.182
```

§10.51's "the render's C\* ≈ 12" is wrong by 3x. **The L\* bases agree to
2.9 %, so the dL\* comparison is valid -- which is exactly why §10.51 correctly
found dL\* already close. The C\* bases differ 5.5x, so the dC\* comparison is
not.** Normalised:

| σ | render dC\*/C̄ | photograph dC\*/C̄ |
|---|---|---|
| 5.9 mm | **5.66 %** | 3.47 % |
| 11.9 mm | **5.83 %** | 4.73 % |
| 23.7 mm | **5.94 %** | 6.04 % |

**The mottle's relative chroma modulation already meets or exceeds the
photograph's at every scale.** Raising the gain would drive it to 2-6x the real
vehicle's in order to compensate for a base-chroma difference that lives
elsewhere. Same shape as "the cream is 26x too uniform": a real statistic against
an invalid reference.

**(f) The BEAUTY arm has been reporting zeros.** §10.51 kept it "because the
target is a photograph ... both are reported rather than one being chosen". On
this patch it is **clipped 100.00 %** -- L\* exactly 100.00, C\* exactly 0.00,
dL\* and dC\* exactly 0.000, corr `nan`. It has never been able to report
anything, and the claim that both arms are reported was never true.

**NEW RULE: A TARGET IS A PROBE TOO.** Check the BASE LEVEL of any absolute
statistic before comparing two frames through it -- print the mean as well as the
rms. Ninth instance of check-what-the-probe-can-see, and the first where the
defect was in the statistic's UNITS rather than in a crop, a class gate or a
surface.

### 10.55  rev 20 — THE LOCKED `CREAM` ALBEDO IS THE LIVE LEAD, AND IT IS NOT SETTLED

`CREAM` is locked at sRGB **(206, 208, 200) -- hue 75.0°, HSV sat 0.038**,
essentially neutral, with **G > R**. The bus's own cream in `ref_rear34.jpg` --
`cream_rms._BODY`, the region the owner himself identified in §10.49 -- reads
**(216, 200, 161) -- hue 41.7°, sat 0.255**, with **R > G**. Opposite channel
order and 6.7x the saturation.

This file's own provenance note records that rev 3 had R > G and it was
"corrected" to G > R because "the measurement has G > R". §10.38 and §10.42
established that `ref_side.jpg` -- the likely source of that measurement --
**contains no usable body-cream patch at all** (1799 gated pixels, best 60x20
window 33.8 % pure). That is the §10.49 shape again, one level down.

**NOTHING WAS CHANGED, and it must not be on this evidence.** A photograph is
lit, and this one is open shade under a palapa in dense green foliage. Every
route tried has a stated weakness:

- clean tail RED, box `(1015, 1105, 545, 615)`, 0.00 % clipped: hue 11.2°,
  **HSV sat 0.838 against §10.12's locked 0.816 -- 2.7 %**. But it sits under the
  counter's shadow, so it is **not the same light** as the cream panel, and §10.21
  bars exactly this comparison.
- inverting the illuminant from that red and applying it to the locked `CREAM`
  predicts sRGB(132, 180, 133), a green, against the measured (216, 200, 161).
  Suggestive; does not bind, same reason.
- the napkin dispensers as a white give a cream albedo of hue 51-58° / sat
  0.107-0.147 against the locked 75° / 0.038 -- same direction, 3-4x -- but the
  two dispensers disagree with each other by 11 % because they are shaded
  differently, and dispenser A is 11.6 % clipped.

Useful signal, recorded: in `ref_rear34.jpg` the napkins, the blender collar and
the two galley trays all read hue **33.1-34.6°** across a 2x brightness range,
while the cream panel reads **41.7°** -- a consistent neutral axis near 33.5°.

**BLOCKED ON ONE OWNER READING**, asked with every box printed and zoomed insets
(§10.38's rule, and the crops A-E are MINE and A and B are contaminated -- they
catch the napkins rather than the steel, and A clips at 11.6 %): are A
`(792,838,410,458)` and B `(846,876,408,456)` **white paper napkins** or
something tinted, and is C `(986,1024,330,378)`, D `(1030,1074,392,424)` or E
`(1096,1180,404,436)` **bare stainless** rather than painted or plastic? A
same-light neutral is what separates paint from illumination here.


### 10.56  rev 20 — `COUNTERTAN`'s INTERREFLECTION TEST, RUN AT LAST — AND A RAY-VISIBILITY FLAG IS NOT AN ABLATION

Five revisions on the list. §10.31c's remaining hypothesis was that the counter
top bounces onto the cream fascia directly below it, so lowering the top's
albedo lowers the DENOMINATOR too and the ratio barely moves -- which would
explain a secant gain of only 0.33 / 0.48 / 0.49.

**The instrument's own consistency control passes first:** EV -3 and EV -4 agree
to **0.03 %** (clipped 1.326 % and 0.086 %). At the default EV the frame is
**57.96 % clipped**, so every arm below is run at EV -4. All arms, `T1_SUB=1`:

| arm | top linear | fascia linear | ratio top/fascia |
|---|---|---|---|
| SHIPPED (control) | 0.12107 0.09953 0.07388 | 0.13403 0.12163 0.10453 | 0.9033 0.8183 0.7068 |
| top: `visible_diffuse=False` | 0.11730 0.09697 0.07240 | 0.13252 0.12061 0.10393 | 0.8852 0.8040 0.6966 |
| top: diffuse+glossy+transmission off | 0.11484 0.09509 0.07123 | 0.13157 0.11988 0.10349 | 0.8729 0.7932 0.6883 |
| fascia: `visible_diffuse=False` | 0.12107 0.09952 0.07388 | 0.13399 0.12165 0.10455 | 0.9035 0.8181 0.7066 |
| **`COUNTERTAN` -> (0.02,0.02,0.02)** | 0.08518 0.06973 0.05511 | 0.12201 0.11169 0.09825 | 0.6981 0.6243 0.5609 |

**THE TWO METHODS DISAGREED BY 8x, AND THE DISAGREEMENT IS THE FINDING.**
Killing every outgoing ray path from the top costs the fascia **1.84 / 1.44 /
1.00 %**. Driving the top's albedo to near-black costs the fascia **8.97 / 8.17 /
6.01 %**. Both claim to remove the same light.

**The ray-visibility arm is the invalid one.** In Cycles an object that is not
visible to a ray type does not absorb that ray -- **the ray passes THROUGH it and
hits whatever is behind**, which here is the lit galley and the cyclorama. So
`visible_diffuse = False` does not remove the top as a source; it SUBSTITUTES the
background for it. The flag demonstrably took effect (the top's own radiance fell
3.1 % / 5.1 % across the two arms), so this is not a flag that failed to apply --
it is a flag that does not mean what it was being read to mean.

**NEW RULE: A RAY-VISIBILITY FLAG IS NOT AN ABLATION.** To remove a surface's
contribution, remove its ALBEDO, not its visibility -- or the measurement silently
becomes "swap this surface for whatever stands behind it". Tenth instance of
check-what-the-probe-can-physically-see.

**On the substance, taking the valid arm:**

- **Interreflection is REAL but SECONDARY: 9.0 / 8.2 / 6.0 %** of the fascia's
  radiance comes off the top. §10.31c's hypothesis is confirmed in direction and
  is far too small in magnitude to explain the gain deficit on its own.
- **THE DOMINANT EFFECT IS A BASE-INDEPENDENT PEDESTAL ON THE TOP.** Cutting
  `COUNTERTAN` by **96.6 %** cuts the top's rendered radiance by only **29.6 /
  29.9 / 25.4 %**. So **~70 % of the counter top's rendered radiance does not
  come from `COUNTERTAN` at all**, which is what a secant gain of 0.33-0.49 was
  really reporting. §10.31c already excluded coat and spec (-2.3 / -2.8 / -5.6 %)
  and this revision excludes interreflection.
- **The prime remaining suspect is the DUST OVERLAY, and it is named rather than
  assumed.** `build_all()` calls `apply_weather(M["countertan"], dust=1.4, ...)`
  -- `countertan` is one of only two materials with dust weighted UP -- and
  `W_DUST_COL_UP` is a settled-ochre film whose colour is **independent of the
  base albedo** by construction. A high-coverage dust mix over the albedo
  produces exactly this signature. **NOT YET MEASURED: the dust lever on
  `countertan` has no override, so it could not be ablated in this pass. That is
  the next test, and it is one render once the override exists.**

`COUNTERTAN` is **LEFT UNCHANGED** for the third revision running -- still not
solved, still not part-tuned toward a target on a lever measured to be the wrong
one.

**FOLLOW-UP: THE PEDESTAL IS NOT DUST EITHER, AND IT IS STILL UNIDENTIFIED.**
`T1_CTAN_DUST`, `T1_CTAN_WEAR` and `T1_CTAN_FADE` were added (defaults
unchanged; the unset arm reproduces the control to five decimals) so the colour
chain could be ablated one lever at a time. Top linear against the control
`(0.12107, 0.09953, 0.07388)`:

| arm | top linear | change |
|---|---|---|
| `T1_CTAN_DUST=0` | 0.12604 0.10813 0.08368 | **+4.1 / +8.6 / +13.3 %** |
| `T1_CTAN_WEAR=0` | 0.12720 0.10458 0.07666 | +5.1 / +5.1 / +3.8 % |
| `T1_CTAN_FADE=0` | 0.11965 0.09768 0.07116 | -1.2 / -1.9 / -3.7 % |
| `T1_CTAN_SP=0 T1_CTAN_CT=0` | 0.11728 0.09587 0.06865 | -3.1 / -3.7 / -7.1 % |
| **`COUNTERTAN` -> near-black** | 0.08518 0.06973 0.05511 | **-29.6 / -29.9 / -25.4 %** |

**The dust hypothesis is REFUTED -- and it was helping**, not hurting: removing
it takes the residual from (+0.107, +0.008, +0.074) to (+0.133, +0.058, +0.143).
Note also that §10.31c's "coat and spec move it only 2.3-5.6 %" was measured on
the RATIO, which cancels common-mode; on the top's ABSOLUTE radiance the answer
is 3.1-7.1 %, i.e. the same conclusion by a statistic that could have disagreed.

So dust, wear, fade, coat+spec and interreflection are **all excluded**, and
together they account for roughly a fifth of a pedestal that is **~69 %** of the
top's radiance (fitting `R = kA + P` through the two albedo points gives
`P = 0.0839` against `R = 0.12107`). **THE SOURCE IS NOT IDENTIFIED. Nothing
should be tuned until it is.**

**A HYPOTHESIS TESTED AND THE TEST DISCARDED, not the hypothesis confirmed.**
rev 15 found in `solve_mural` that the mask was rendered from the object in
ISOLATION while the measured frame was rendered with the whole scene, so the
mask covered pixels where something else stands in front -- its rule was
"isolate the object in the measured render, not only in the mask". **That fix
was never applied to `solve_ctan`**, whose `top` mask is built the same way and
whose frame contains napkin dispensers, bottles and the brass nosing. The
obvious per-pixel test -- render at two albedos and ask which mask pixels moved
-- **cannot work at 48 samples: the seed-to-seed noise is 21.7 % per pixel
(median), which is larger than the effect being looked for.** The probe also
failed to reproduce the solve's own control, so it was discarded rather than
read. The occlusion hypothesis is therefore **OPEN and untested**, and the test
needs either a much higher sample count or an object-index pass.



### 10.57  rev 21 — FIVE ROUTES TO DE-ILLUMINATING THE CREAM, ALL FIVE REFUTED

The owner answered §10.55's question. It did **not** unblock `CREAM`, and the
reason is structural rather than a matter of precision. **`CREAM` is UNCHANGED
at sRGB (206,208,200).**

**HIS READING, and it refuted my crop a second time.** rev 20's boxes A
`(792,838,410,458)` and B `(846,876,408,456)` are worse than rev 20 recorded:
each straddles **two materials** — a white napkin face AND the grey dispenser
body between them. That, not differential shading, is why B read 34 code values
darker than A; rev 20's "the two dispensers disagree with each other by 11 %
because they are shaded differently" is **withdrawn**. Redrawn on single
materials and put to him again, he identified:

- **N2 `(816,836,422,450)` and N3 `(868,890,426,452)` are white paper napkins.**
- **N1 `(784,798,420,448)` is STILL straddling** a napkin and the dispenser side
  — my redrawn box was still wrong. **DROPPED.** Twelfth instance of
  check-what-the-probe-can-physically-see, and the second in one revision where
  the defect was a crop I drew.
- **M1 `(844,860,418,452)` is bare / brushed stainless.**

`N3` is the clean reference: **0.00 % clipped, n = 572**, sRGB (236,225,211),
hue 33.2°, sat 0.104.

**C / D / E ARE DEAD AS NEUTRALS, and it is measured, not argued.** rev 20's
three candidates are inside the galley opening. Luminance ÷ the cream panel's:
napkins **1.13 / 1.54 / 1.37**, C/D/E **0.32 / 0.23 / 0.22**. A neutral cannot
be 3–4× *darker* than the cream it shares light with — either they are in the
galley's own dimmer light, in which case the division does not bind, or they are
dark objects and not neutrals. Dropped before use.

**THE FIVE ROUTES.**

- **A — napkin as a same-light neutral.** Implies cream hue **48.2°, sat 0.163,
  R>G** (N3); 44.5° / 0.203 (N2). **Robust to clipping, and that is a control:**
  **N2/N3** clip at **12.1 / 0.00 %** and agree (sat **0.203 / 0.163**).
  Clipping compresses channels toward neutral, so if clipping drove the warmth
  the more-clipped arm would read *less* saturated; it reads a hair *more*. This
  is the route that would refute the locked constant, and it is clean.
  **rev 23: N1 REMOVED from this control.** It was used here as the 22.4 %
  arm — nineteen lines after §10.57 DROPPED it for straddling a napkin face and
  the dispenser body, which is the defect the owner himself caught. The
  conclusion is unchanged and survives on N2/N3 alone (rev 22 verified that
  before this edit); only the contaminated third arm is gone.
- **B — M1 as a neutral. INADMISSIBLE BY §10.21**, not by preference: metal
  against a diffuse dielectric is not the same class, which is precisely the
  silver-leaf trap §10.21 was written for. It also disagrees with A — hue 63.7°,
  sat 0.086, **G>R** — and that disagreement is the tell, not a tiebreak.
- **C — THE THIRD METHOD: does the napkin illuminant recover the independently
  locked `RED`? NO.** Five clean red patches de-illuminated by N3 read hue
  **13.1–13.8°**, sat 0.804–0.873, against locked `RED` hue **5.0°**, sat 0.816.
  **Saturation lands; hue misses by 8.5°, consistently.** Shading does not
  explain it: across **30** clean red patches spanning a **4.27× luminance
  range**, corr(luminance, hue) = **+0.733** but the whole hue swing is only
  **1.7°** — one fifth of the gap.
- **§10.12's OWN INVARIANT SETTLES WHY.** The ratio (G−B)/(R−B) is invariant
  under a neutral additive. Locked `RED` → **0.0813**; `ref_side`'s deep-shade
  red, §10.12's own figure → 0.067; **`ref_rear34`'s red → 0.2225 ± 0.0045
  (n = 6) → +31 sd.** `ref_rear34` is **not related to the locked albedo by any
  neutral transform.** No same-light neutral can remove that, which is exactly
  why route A leaves a residual however clean the napkin is.
- **D — use the locked `RED` as the illuminant reference instead. REFUTED BY ITS
  OWN CONSISTENCY CHECK**: it implies the white paper napkin has albedo hue
  **260–300°, sat 0.30–0.43 — a saturated purple** — and the cream comes out
  magenta (hue 273–352°). **NEW RULE: AN ILLUMINANT REFERENCE MUST CARRY
  SUBSTANTIAL ALBEDO IN ALL THREE CHANNELS.** `RED` is (0.5520, **0.0294,
  0.0176**); dividing an observation by a near-zero channel amplifies the
  additive term without bound. This is also why the observed red reads hue 13
  rather than 5.
- **E — solve §10.9's actual model, `obs_c = albedo_c · E_c + A`,** with the
  locked red plus the napkin as a neutral of unknown albedo `k`: 6 equations,
  5 unknowns (E×3, A, k), over-determined by one. **NO PHYSICAL SOLUTION
  EXISTS** — `A_R − A_B` never crosses zero for any `k` from 0.05 to 0.95.
  Concrete diagnosis rather than a shrug: the red reads **95 % of the napkin's R
  channel**, where an albedo of 0.552 against white paper should put it near
  **65 %**. **The red and the napkin are not under the same light**, so no
  two-surface solve using both is admissible.

**CONCLUSION.** `CREAM` stays at (206,208,200) — not because the evidence is
thin but because the frame demonstrably violates the assumption every route
needs, and a locked constant must not move onto a number whose own validation
failed at 31 sd. What would settle it: a same-light, **same-class**,
three-channel reference; or an established neutral transform between
`ref_rear34` and the frame the locked constants came from. Neither exists in the
three photographs.

### 10.58  rev 21 — `audit.py`'s FOUR LIVERY ROWS: A SUBAGENT CLAIM, TESTED AND HALF REFUTED

A read-only agent reported that `audit.py`'s belt / window-sill / window-head /
V-swage-apex rows are **algebraic identities that cannot fail** — the §10.45
shape. It was tested rather than repeated, and it is **half right**.

- **CONFIRMED — invariant to the rake.** Perturbing `RAKE_DZDX` 17.75 → 21.00
  mm/m moved the ride drops (71.0 / 28.4 → 75.2 / 24.8 mm) and the reporting
  station (x 0.962 → 0.813), and all four rows still printed **1.2070 / 1.3070 /
  1.7100 / 0.3400** with `+0.0 mm ok`. rev 18's rake guard **fired (1 fail)** —
  that guard works.
- **BUT THE INVARIANCE IS DELIBERATE AND DOCUMENTED** at `t1_core.py:165-171`:
  `X_DROP_REF` is *derived* so `RIDE_DROP` stays exactly 0.0650, precisely so
  `Z_BELT` and `V_APEX` do **not** move for a rake change. That is §10.25's rule
  applied correctly. It is not a defect.
- **AND THEY ARE NOT IDENTITIES.** Displacing `Z_BELT_AUTH` by +50 mm made the
  row print **`+50.0 mm OUT`**; displacing the band `Z_SILL`/`Z_HEAD` by −100 mm
  made `verify` throw **2 FAILs**. The rows are real locks on the authored
  constants and they discriminate.

**Residual real findings, both modest and both recorded rather than fixed:**
`V_APEX`'s tolerance is **±0.060 m**, so a 50 mm error passes as "ok"; and
`STATE.md`'s table is headed *Measured dimensions* with a column headed
*measured* for rows that are authored constants checked against REF targets —
the same labelling family as the hand-typed "(measured 41)" §10.53 removed. A
mislabel, not a phantom. Separately: the aperture-existence probe **is** a real
ray-test (`_has_metal` against the body mesh), but `_bay_probe_z` is the
midpoint of `Z_SILL`/`Z_HEAD` — the constants under test — so its station
follows them; `verify:803-804`'s constant-lock is what actually catches a
displaced band.

**NEW RULE: A SUBAGENT'S FINDING IS A CLAIM, NOT A MEASUREMENT.** One of three
agent headlines this revision was half wrong, and the source file's own comment
said so.


### 10.59  rev 22 — `H_ROOF` RETIRED BY THE OWNER, and the probe kept as a labelled regression catcher

**THE OWNER'S DECISION, taken in rev 22 after five revisions of being owed it:**
retire `H_ROOF = 1.960` as an accuracy target; keep the direct mesh probe as a
**LABELLED REGRESSION CATCHER with a ±5 mm band**, exactly as §10.47 did for
`STATE.md`'s height row.

**THE CHAIN OF WITHDRAWALS that left it unsupported** — this is not a
preference, it is the absence of an admissible derivation:

1. `REF_MEASUREMENTS` §1 derived 1.960 **from the ground line**, the datum
   §10.11 BANS: three features placed from it land low by the same sign and
   magnitude, a ~70 mm common-mode error. §10.34 then found the **HUB**-
   referenced chain carries the same disease at ~29 mm, so the obvious
   substitute datum is not clean either.
2. 1.960's **only ground-line-free confirmation** was `LOFT_GROUND` §1.2's
   1.9621. §10.34 **withdrew that reading's interpretation** — the "proud strip
   253.21" IS the roof — *without noting that it was 1.960's only escape from
   the banned datum*. §10.48 found that.
3. A guard whose target has no admissible derivation cannot report accuracy. It
   can only report disagreement with a number of unknown provenance.

**WHAT WAS DELIBERATELY NOT DONE.** `H_ROOF` was **NOT** re-valued to the mesh
probe's 1.9835. The owner rejected that explicitly and was right on this
project's own rules: a guard set to the model's own current reading compares the
model to itself and **can never fail**, and it clears a standing warn **by
tuning**. Both are forbidden here.

**STATE THIS WHEREVER THE WARN'S DISAPPEARANCE IS REPORTED:**
**THE +23 mm WARN IS GONE BECAUSE THE TEST WAS WITHDRAWN, NOT BECAUSE THE MODEL
IMPROVED. THE MESH DID NOT MOVE.** Guards went 0 fail / 1 warn → **0 fail /
0 warn at both levels** with roof hole 68052v / 252123v, 126 objects, 185
meshes, arch 39.7 / 40.7 mm, rake 17.75, overhang 0.7730, bays 0.516 0.515
0.516 — every other figure identical.

**THE BASELINE WAS WATCHED PRINT AT BOTH LEVELS BEFORE IT WAS WRITTEN INTO THE
FILE:** SUB=1 → **1.9835**, SUB=2 → **1.9833**, 0.2 mm apart, both clearing the
±5 mm band by ~4.8 mm.

**FALSIFIED AFTER REPAIR, TWO ARMS, not merely re-run:**

| arm | perturbation | result |
|---|---|---|
| 1 | regression baseline displaced −10 mm | **FAIL** `MOVED +10.0 mm` — exact |
| 2 | `CR_ALL` crown raised **+8.0 mm IN THE GEOMETRY** | **FAIL** `MOVED +7.9 mm` |

**Arm 2 is the one that matters**: it proves the row reads the **MESH**, not two
constants — precisely what the old arch guard (`ARCH_R − TIRE_R`, which returned
41.0 forever, §10.45/§10.52) never had. The 0.1 mm shortfall is loft resampling
and is stated rather than rounded away. The row **FAILS** past the band rather
than warning: an unintended geometry change should stop the build, a deliberate
one should be re-baselined by hand and said out loud, and **the band must never
be widened**. `audit.py`'s prose was corrected in the same commit so it cannot
contradict the build.

**WHAT IS NOW OPEN, and it is larger than what closed:** the real vehicle's
**absolute roof height is UNMEASURED**. Nothing replaced 1.960. Closing it needs
a head-on rear or front elevation from roof height or above — the same
photograph that would close `CREAM`.


### 10.60  rev 22 — `COUNTERTAN`'s HUE: THE TARGET IS AN OBSERVED PIXEL, NOT AN ALBEDO. REFUTED.

The rev-22 work list carried "`COUNTERTAN`'s hue onto its own cited
measurement — built h 42.3° / sat 0.254 against an independent 1266-px read of
**28.4° / 0.333**". That finding came from a subagent, so under §10.58's rule it
was **tested before being acted on. It is refuted, and `COUNTERTAN` is
UNCHANGED.**

**THE ERROR IS A CATEGORY ERROR — the §10.21 trap that cost rev 10 one wrong
silver.** `COUNTERTAN` is an **ALBEDO**, defined by its own docstring as a ratio
against a same-class reference. **28.4° is an OBSERVED PIXEL.** Re-measured here
on a clean single-material crop of the counter top (cols 700–780, rows 413–414,
**n = 162, 0.00 % clipped**) the observed pixel reads **h 32.3°, sat 0.364** —
the same quantity the agent reported. Comparing it to an albedo is not a
comparison.

**De-illuminated through the docstring's own documented method:**

| quantity | hue | sat |
|---|---|---|
| OBSERVED tan-top pixel | **32.3°** | 0.364 |
| ALBEDO via the fascia arm (× `COUNTERCREAM`) | **39.3°** | 0.225 |
| ALBEDO via the cab-roof arm (× `CREAM`) | **41.7°** | 0.289 |
| **BUILT `COUNTERTAN`** | **42.3°** | **0.254** |

The built constant sits **0.6° above the nearer arm and 3.0° above the further
one**, and its saturation **0.254 falls inside the arms' 0.225–0.289**. The
claimed error was ~14°; the real disagreement is **at most ~3°** and the
saturation is already bracketed. The illuminant is warm — observed r/g **1.506**
against the albedo's **1.166** — and dividing it out is exactly what carries the
hue from 32° to ~40°. **Nothing is moved on a ~3° residual while the LEVEL is
unresolved** (§10.56's ~69 % pedestal): tuning hue against an unidentified
pedestal is tuning against an unknown.

**TWO NEW FINDINGS, both from controls that had never been run.**

**(a) `COUNTERTAN`'s FOUNDING CROP STRADDLES TWO MATERIALS — thirteenth instance
of check-what-the-probe-can-physically-see, and this one is in SPEC's own
founding measurement.** A row scan of cols 700–780 shows the counter top is only
~3 px tall in `ref_side.jpg` (the camera is at roof height, so the top is nearly
edge-on — §10.28's own method note). The docstring's crop is rows **411–415**:
row 411 is the shadowed transition, **54 code values darker** than row 413; row
415 is already running into the **brass nosing**, which occupies rows 416–419 at
**sat 0.669, r/g 2.356** — a completely different material and class. The clean
tan top is rows **412–414**, and rows 413–414 are cleanest. Same defect family as
rev 20's boxes A/B and rev 21's N1.

**(b) THE CAB-ROOF ARM IS NOT UNDER THE SAME LIGHT AS THE FASCIA ARM, and it is
now measured rather than asserted.** The docstring records that the two
references "bracket rather than agree" and calls the disagreement "real and
structural" — but never diagnosed it. A positive control does: if two reference
surfaces share a light, their observed ratio must equal their albedo ratio.

    observed  cab-roof / fascia   = (0.5873, 0.6345, 0.7464)
    expected  CREAM / COUNTERCREAM = (0.8397, 0.8822, 0.8752)   albedo only
    residual illuminant            = (0.6994, 0.7192, 0.8529)   B/R = 1.219

**The cab roof sits in light 22 % bluer in B/R than the fascia.** It is out from
under the lid in open sky-light; the fascia is under the counter in warm bounced
light. §10.21 requires the same light, so **the cab-roof arm is inadmissible for
the ratio** — which means the LEVEL bracket's upper end (G 0.569) rests on an
inadmissible arm. That is a direct input to the §10.56 pedestal work and is
recorded, **not applied**: the fascia arm has its own stated weakness (vertical,
wrong orientation, takes red bounce off the body), so neither arm is clean and
the level stays bracketed exactly as instructed.

**`COUNTERTAN` = (0.5870, 0.4930, 0.3060) UNCHANGED, fourth revision running.**


### 10.61  rev 22 — ITEM 4 GROUNDED: the crossings MEASURED, and two carried figures corrected

Item 4 asked for the `t1_shell:451` assert to be generalised to all four shut
lines, both arches and all five apertures, with the expectation that it would
FAIL when first armed. **The grounding was done first** (`probe_shutlines.py`,
READ-ONLY, changes nothing) because §10.45's crossing count has been carried
forward as a CLAIM through four revisions without being reproduced.

**IT DOES NOT REPRODUCE. Measured, per pair, at ~1 mm sampling:**

| shut line | aperture | side | arc INSIDE | aperture state |
|---|---|---|---|---|
| `gap_door+1` | `door_vent` | +1 | **11.8 mm** | OPEN |
| `gap_door+1` | `bay0` | +1 | **118.8 mm** | OPEN — show flank |
| `gap_door-1` | `door_vent` | −1 | **11.8 mm** | OPEN |
| `gap_door-1` | `bay0` | −1 | **118.8 mm** | glazed |
| `gap_cargo` | `bay0` | −1 | **402.0 mm** | glazed |
| `gap_cargo` | `bay2` | −1 | **402.0 mm** | glazed |

**SIX crossings, 1065.1 mm total** — against the carried **five crossings,
1209 mm**. Both the count and the total are corrected. **TWO are on the show
flank**, not one: `bay0` at 118.8 mm (the crossing §10.45 describes) *and*
`door_vent` at 11.8 mm, which no prior revision named.

**THE PROBE VALIDATES ITSELF against an independent arithmetic check.** The two
`gap_cargo` rows are byte-identical at 402.0 mm, which is exactly the kind of
coincidence that usually means a bug. It is not one: both cargo verticals cross
a bay over the **full aperture height**, and `Z_HEAD − Z_SILL = 403.0 mm`. The
1 mm shortfall is the sampling step. A suspicious number was checked rather
than accepted.

**THE ARCH HALF OF ITEM 4 IS LARGELY NOT APPLICABLE, and that is a result.**
Of the six shut-line × arch pairs, **four cannot be tested at all** — the
outline does not span the arch station, and the probe returns *None* rather
than an endpoint (§10.45's rule). The two testable pairs are the cab-door line
against the FRONT arch, at **+23.6 mm CLEAR** — which is precisely the single
pair the existing assert already covers. **Generalising the arch assert adds
no coverage**, because no other shut line reaches an arch. The gap in
`t1_shell:451` is the APERTURES, not the arches.

`gap_englid` is in the **(y, z) TAIL frame**, cut at `X_TAIL + ENGLID_CUT_DX =
−1.7150`. No flank aperture shares that surface, so a flank crossing test is
**NOT APPLICABLE** — reported explicitly rather than silently skipped, because
looping it in with the flank lines would manufacture crossings out of a
coordinate mismatch.

**`CARGO_GAP`'s SAMPLING — both carried numbers are true and they are DIFFERENT
STATISTICS.** §10.45 records "28 samples ALL on the four corner arcs = 5.2 % of
the outline". Measured: **20 of 28 points (71.4 %) lie on the corner arcs, and
the corner arcs are 5.2 % of the outline BY LENGTH** — reproducing the 5.2 %
exactly. So "ALL" is the imprecise word, and the sharper statement is that
**71.4 % of the samples are spent on 5.2 % of the outline, leaving the straight
runs — 94.8 % of the length — with 8 samples.** The defect is real and is now
stated in a form that can be guarded.

**NOT ARMED THIS REVISION, and named as such.** The assert is the next step and
it should fail on six pairs; fixing that is geometry work, not a threshold
change. The grounding is done so rev 23 arms it against numbers somebody
watched print.

### 10.62  rev 23 — ITEM 4 ARMED: the B-pillar had NEGATIVE width, and the brief was half wrong

§10.61 measured six crossings and 1065.1 mm and left the assert unarmed with the
instruction "expect it to FAIL; fix the geometry, not the threshold". **A brief
is a probe too** (§10.43, §10.54). Before moving any geometry, `probe_cross_
anatomy.py` (READ-ONLY) asked the three questions §10.61 never asked: WHICH
member of each pair is at fault, HOW DEEP the penetration is, and WHICH FLANK
each is on. All three change the answer.

**THE SIX CROSSINGS ARE THREE DEFECTS, NOT ONE, AND ARC LENGTH OVERSTATES THEM
BY UP TO 23×.**

| pair | arc | penetration | flank |
|---|---|---|---|
| `gap_door × bay0` | 118.8 mm | **5.2 mm** in x | show + off |
| `gap_door × door_vent` | 11.8 mm | **20.7 mm** in z | show + off |
| `gap_cargo × bay0` | 402.0 mm | 49.7 mm | off only |
| `gap_cargo × bay2` | 402.0 mm | 139.8 mm | off only |

**SHOW flank 130.6 mm; OFF flank 934.6 mm = 87.7 % of the total.** Arming on
arc length would have chased a number 23× the actual error on the pair that
matters most.

**THE RATIONALE IS NEW AND WAS DELIBERATELY NOT INHERITED.** `t1_shell`'s arch
assert exists for one stated reason — a shut line crossing an ARCH LIP collapsed
the shell 205562 v → 12 v at SUB=2. **That does not transfer:** all six
crossings were live at SUB=2 with **zero non-manifold edges**. The invariant
armed instead is TOPOLOGICAL — *an aperture cut in a panel cannot extend past
that panel's own boundary*, or part of the hole is in the door and part in the
body and the door cannot open. It needs no photograph, no scale and no datum,
which is precisely what makes it safe to assert on a vehicle this project has
only three photographs of.

**FIXED, both on the show flank, geometry not threshold:**
- **The B-pillar had NEGATIVE width.** `DOOR_GAP`'s rear run sat 5.2 mm inside
  `BAYS[0][1]`. Bay 0's edges are LOCKED (equal bays, §10.29; band guarded every
  revision) and the door's rear-run x carries **no provenance anywhere in the
  repo**, so the DOOR moved, as a whole, so its rear edge keeps a single
  straight lean. `DOOR_REAR_DX` is **expressed in terms of `BAYS[0][1]`**, never
  as a bare number (§10.25's rule). **`B_PILLAR = 0.0120` is AUTHORED, not
  measured** — the minimum clearance that makes the topology valid.
  `ref_workshop.jpg` shows this pillar is visibly wider than the pillars between
  the three side windows, but that frame is a three-quarter view with no
  admissible px/m on the door plane, so **no number was taken from it. THE
  B-PILLAR'S TRUE WIDTH IS OPEN AND UNMEASURED.**
- **The vent wing broke the door's top edge by 20.7 mm.** Asked what the
  photograph shows, the owner confirmed the door glass **is divided into a vent
  plus a main pane**, so the vent stays; he could **not** resolve whether its top
  reaches the door's top rail, so the door's top-front corner — which IS legible
  in that frame — was left alone and the vent's top edge dropped instead.
  **`VENT_TOP_DROP = 0.0280` is AUTHORED. The vent's true top edge is OPEN.**

**Crossings 6 → 2. Show flank 130.6 → 0.0 mm.**

**FALSIFIED FOUR WAYS**, each through an env lever whose default is a proven
no-op: `T1_BPILLAR=-0.010` → FIRES at 223.5 mm; `T1_BPILLAR=0.0` (exact
tangency) → passes, the correct boundary behaviour; `T1_VENTDROP=0` → FIRES at
16.7 mm; both, at `DOOR_REAR_DX = 0` → FIRES at 12.7 and 120.8 mm. **That last
arm reproduces rev 22's geometry exactly and lands within 1–2 mm of its 11.8 /
118.8** — the sampling step. An earlier arm looked like a 2.6× disagreement
between two implementations and was NOT one: `DOOR_REAR_DX` is *derived*, so
`B_PILLAR = -0.0173` moved the door 12 mm further aft than rev 22. **The value
that reproduces rev 22 is `B_PILLAR = -0.0053` — the negative pillar width
itself**, an independent confirmation of the 5.2 mm defect.

**MY OWN NEGATIVE CONTROL FAILED FIRST, and the failure was MINE** (§10.55's
rule, second instance this revision). The first draft asserted "an outline is
not inside ITSELF" — ill-posed, because every sample then lies exactly ON the
boundary where a ray-crossing test is undefined. Replaced with a disjoint box.

**THE OFF FLANK IS NOT ARMED AT ZERO, AND THAT IS THE RESULT.** 804.9 mm across
`gap_cargo × bay0/bay2`. **SPEC's own source table grades that entire flank "E
(never photographed)"** — and the two colliding features are BOTH E and
CONTRADICT each other: the off-side windows are a mirror of the show side
(`side_cutters` loops `s in (1,-1)`) while the cargo door was placed
independently. Shown the workshop frame's sightlines through the near openings
with every box printed, the owner answered **"cannot tell from this crop"**. So
this half is a **LABELLED REGRESSION CATCHER** at a watched baseline
(**804.9 mm, band ±10 mm**), exactly as rev 22 did for `H_ROOF`: a pass means
"the off flank has not moved", **NOT** "the off flank is right". Tightening it to
zero would mean moving geometry nobody has ever seen, to satisfy a guard.

**`CARGO_GAP` DENSIFIED, 28 → 154 samples**, straight runs **8 → 134**. The
outline is unchanged: the inserted points are collinear, and **signed area is
asserted equal** — a control, not a comment (§10.50).

**THREE CITATION DEFECTS FOUND, all SPEC hygiene, none load-bearing.** §10.61
attributes to §10.45 a "five crossings, 1209 mm" figure and a "28 samples / 5.2
%" figure that **§10.45's body does not contain** — both strings live in
`HANDOFF_rev18.md:208/211` and `AUDIT_rev18_loft.md:275`. §10.59 credits §10.48
with withdrawing 1.960's last support; **§10.48 is entirely about plate px/m**
and never mentions 1.9621 (`verify.py:66` repeats it). And §10.45 cites the rake
lock to **§10.9, whose own table locks the RETIRED 0.0330** — the lock is
§10.29's. *A carried-forward figure is a claim too* now extends to the CITATION:
rev 22 corrected a number SPEC never carried, and cited the wrong section doing
it.

**ALSO REFUTED, from the rev-23 prompt's own §2:** "§10.45–48 RETIRE claims in
§10.34" — they do not. §10.46 corrects §10.37 three times; the only §10.34
reference in §10.45–48 is `SPEC.md:3267`, a **guard tally**, which criticises
coverage and retires nothing. And "§10.29 carries two corrections that touch
every REF number" — it carries **one** (`:899`, the 100 mm origin error, found
by two routes). The other REF-wide corrections are §10.11's and §10.34's.


### 10.63  rev 23 — `folk_gen.py`'s bake frame was built on four retired numbers

`folk_gen.py` re-typed four `t1_core` / `t1_mats` constants rather than
importing them — legitimately, because it is a standalone texture generator and
cannot `import bpy`. **All four had gone stale, and the drift was measured, not
assumed:**

| constant | re-typed literal | live | drift |
|---|---|---|---|
| `X_TAIL` | −2.108 | **−1.8730** | **+235 mm** |
| `RAKE_DZDX` | 0.0330 | **0.017750** | **−15.25 mm/m** |
| `RAKE_Z0` | 0.0365 | **0.047925** | +11.4 mm |
| `Z_BELT0` | 1.2355 | **1.224075** | −11.4 mm |

Same failure family as the dead `RIM_R`, the dead `countertan` arguments,
`_NOSE_SEL` and `audit.py`'s hardcoded 4.290 — **a constant tuned against
another constant and not expressed in terms of it** (§10.25). §10.10 makes
artwork replication a HARD BAR, and the frame the artwork is baked into was
built on numbers three revisions of geometry work had already retired.

**FIXED STRUCTURALLY, not by re-typing the new values.** The constants are now
parsed out of the sibling modules with `ast`, which is the pattern rev 14 set
for `SCR` in `build.py`, and the parse **raises rather than falling back** — a
silent fallback to a stale literal is exactly how this drifted for ten
revisions. `X_TAIL` is reconstructed from its DEFINITION (`X_AXLE_R − O_NEW`)
because it is derived in `t1_core` and is not a literal there at all.

**THE BANNED FLAT px/m at `folk_gen.py:1884` IS GONE — and it was harmless
where it stood, which is worth stating precisely rather than claiming a fix
that did not happen.** `mm = 1000.0 / 211.21` used the px/m §10.43 retired. But
it set only the SAMPLING INTERVAL of a coverage scan whose x values are already
body-frame metres — it never converted a position. Renamed `STEP_M` and
commented as sampling-only, so it is lethal only if copied and cannot be
copied by name any more.

**NOT RE-BAKED, deliberately.** `build.py` never calls `folk_gen`; `tex/*.png`
are committed pre-baked artefacts, so none of this changes the current build.
A re-bake moves every painted element and §10.10 makes that a MEASURED
operation against the photographs, not a side effect of a constants fix.
**CARRIED FORWARD: the committed artwork was baked in the stale frame.**

**ONE STALENESS LEFT OPEN AND NAMED**: `folk_gen.DOOR_X0` is now 17.3 mm stale
because §10.62 moved the cab door's rear run. It is not parsed like the other
four — `t1_shell.DOOR_GAP`'s rear points are EXPRESSIONS and `B_PILLAR` is an
`os.environ` lookup, so `literal_eval` cannot reach them. Evaluating
`t1_shell`'s constant graph is real work and was not attempted blind at the end
of a revision.

### 10.64  rev 23 — SPEC hygiene: four retired values were still published as "locked"

Each found by a read-only agent and **verified by hand before being acted on**
(§10.58). None is load-bearing on the build; all four are traps for the next
context, and three of them had a *live code value that already disagreed*.

- **§10.3's table published the RETIRED red `(196,106,36)` as `RED` locked**, in
  the section headed "the canonical constants (supersedes any value above)",
  while `t1_mats.py:67` has carried the live `(196,49,36)` since rev 9 (§10.12).
  Struck through; the live row added beside it.
- **§10.3 also published `W_ART = 0.30` as "Locked"** — retired in **rev 10**
  because it made the measured ×2.048 gold-to-red contrast arithmetically
  unreachable, which was the arithmetic cause of the owner's "far too faint and
  sparse". Live value is 1.00: the table was **3.3× off for thirteen
  revisions**.
- **§10.9's table published the RETIRED rake** (`RAKE_DZDX` 0.0330,
  `RAKE_Z0` 0.0365, `X_DROP_REF` +0.8636) under the word "Locked:", 1600 lines
  from §10.29 which rejected it at 4.5 σ, with no link between them — plus
  `Z_BELT0`/`V_APEX0` derived from it and now ~11.4 mm stale. Struck through
  with the live values beside them.
- **`SPEC.md:1983` used N1** — the crop the owner refuted for straddling a
  napkin face and the dispenser body — as the 22.4 %-clipped arm of route A's
  clipping control, **nineteen lines after §10.57 dropped it**. Removed. The
  conclusion is unchanged and stands on N2/N3 alone, which rev 22 had already
  verified.

**Structural cause, and it is worth fixing properly one day:** `verify.py`
auto-arms its retired-material guard **from §0.2** — a genuinely good design —
but **§0.2 has gained no entry since rev 4/rev 8**. None of §10's retirements
is listed there, so the one self-arming mechanism in the repo covers none of
them.

### 10.65  rev 24 — `solve_ctan` measured the whole scene through a top-only mask

**A third of the mask is not the counter top.** SPEC §10.56 left the pedestal
**UNIDENTIFIED** after excluding dust, wear, fade, coat+spec and interreflection.
The remaining hypothesis was rev 15's, carried **four revisions unrun**: masks
are rendered in isolation (`shader_solve.py:175`, via `_only`) but `solve_ctan`'s
**measured frame is rendered with the whole scene present** (`:425-427`) — there
is no `_only` on that path. `solve_mural` has carried the fix since rev 15
(`:234`) and the rule was never propagated.

rev 20 tried this per-pixel at 48 samples and **discarded the probe, not the
hypothesis** — seed noise is 21.7 % per pixel, larger than the effect. That was
**the wrong statistic**: region means over ~10⁴ px put the same noise at 0.21 %.

`probe_ctan_index.py` (NEW, read-only) settles it with an **object-index pass**.
Chosen over a visibility flag precisely because of §10.56's own rule — IndexOB
suppresses nothing, it labels the surface each camera ray terminated on.

**Three controls, because an ill-posed control has been the bug twice running:**

| control | result |
|---|---|
| **NULL** — IndexOB under `_only(tops)`; must be exact | **IoU 1.0000, 0 disagreeing px, 0 foreign px** |
| **POSITIVE** — must NAME a foreign surface | names `gal_warmer`, `gal_caddy0/1`, `T1_body` |
| **HARNESS** — reproduce §10.56's chain | ratio reproduces; **clipping guard tripped twice** |

**MEASURED** (eroded masks, n = 15 728 / 51 938 px):

| mask | target | foreign |
|---|---|---|
| TOP | 66.94 % px, 75.4/71.8/64.5 % radiance | **33.06 % px** |
| FASCIA | 42.69 % px | **57.31 % px** |

The largest occluder is **`gal_warmer`**, which no revision had ever named.
**`counter_top` is 21.76 % of the FASCIA mask**, and **97.84 % of the top mask
lies inside the fascia mask** — the un-isolated solve divides a region by a
**superset of itself**.

**The pedestal, re-measured through BOTH albedo arms with the clean mask:**

| | R | G | B |
|---|---|---|---|
| contaminated (reproduces §10.56's chain at 1 rig) | 68.5 | 68.0 | 72.1 % |
| **clean, index-masked** | **60.8** | **58.2** | **59.5 %** |
| albedo sensitivity `k` | **+40.3** | **+40.3** | **+40.0 %** |

**The counter top's true response to its own albedo is 40 % stronger than
`solve_ctan` measured.** That is what "secant gain 0.33–0.49" was really
reporting. The residual against the target **flips sign in all three channels**
once the masks are clean, so the shipped ratio's near-agreement in G was two
large opposing contaminations.

**THE INFERENCE WAS NOT REPORTED — THE MEASUREMENT WAS.** Correcting by
arithmetic assumes occluder radiance is albedo-invariant; the occluders sit ON
the top and catch its bounce, so it is not. The arithmetic gives 58.3/55.5/56.8 %,
the two-arm measurement **60.8/58.2/59.5 %**. Both are printed.

**A ~59 % pedestal SURVIVES and is STILL UNIDENTIFIED. `COUNTERTAN` is
UNCHANGED at (0.5870, 0.4930, 0.3060), fifth revision running.**

**TWO INSTRUMENT DEFECTS FOUND ON THE WAY, both mine, both caught by controls:**

1. **`ST.lighting()` STACKS.** `studio._softbox` calls `bpy.data.lights.new` on
   every invocation and nothing removes a light — measured **8 / 16 / 24** over
   three calls. `solve_ctan` calls `cam_setup()` three times, so **its measured
   frame is lit by THREE stacked rigs** and every absolute linear figure in
   §10.56, `0.12107` included, is a 3-rig number. The ratio survives a
   near-uniform multiplier; the level and the clipped fraction do not. Purged.
2. **Exposure must go through the ENVIRONMENT.** Setting
   `scene.view_settings.exposure` is overwritten by `_plain_view` inside every
   `_render`. My first run came back **70.54 % clipped** against §10.56's
   0.086 %, and the radiance shares **collapsed onto the pixel shares** — which
   is §10.54's "CLIPPING DESTROYS TEXTURE" reproducing exactly. **My own guard
   then tripped a second time and I fixed the cause rather than widening it**,
   which is how the stacked rig was found.

**Fixed in `shader_solve.py`**, with `T1_CTAN_NOISOLATE=1` reproducing the old
contaminated arm so every §10.56 figure stays reproducible.

**Ceiling, stated:** IndexOB reports the surface a ray TERMINATES on, so a
transmissive surface in front would be mis-reported. The probe asserts no
`glass_*` appears in either mask and **declines** if one ever does.

### 10.66  rev 24 — rev 23 broke `folk_gen.composition()` and nobody ran it

**`composition()` could not complete.** rev 23 renamed `mm = 1000.0/211.21` to
`STEP_M = 1.0/211.21` (§10.63) and **did not update the use site**. AST census:
`mm` had **ZERO Store sites and ONE Load site** module-wide, at `:1976` — a
**top-level statement of the function body**, so it is reached unconditionally.

The function whose own docstring calls it *"the measurement this rev exists
for"* raised `NameError` on every call, so the connected-component census
(`COMP_TOP`, `COMP_HIST`, `FLANK_MASSES`) **could not run at all** — and any
re-bake attempt would abort there.

**This is what "a claim in prose is not a guard" looks like from the inside.**
§10.63 verified the rename **by reading**, and stated it "precisely rather than
claiming a bigger fix than it was" — while the rename had broken the function.
**Nobody executed it.** `build.py` never calls `folk_gen`, so no guard covers it.

Repaired as `STEP_M * 1000.0 * 1000.0`, and the repair is **value-preserving**:
53.2645 mm² both ways, i.e. exactly rev 22's behaviour restored.

**My own first dynamic probe of this was ill-posed** — I passed two arrays where
`composition(res, …)` takes a dict, so it raised `IndexError` inside `look()`
and never reached `:1976`. It proved nothing and is recorded rather than
quietly replaced by the AST proof that did.

### 10.67  rev 24 — the §0.2 guard is NOT self-arming, and its own comment said it was

**WORK ITEM 2'S BRIEF IS REFUTED.** It read: *"add §10's retirements to §0.2 so
`verify`'s self-arming guard covers them."* It does not, and cannot.

- `_retired_material_tokens()` returns `set(_RETIRED_MAT)` — a **hand-written
  dict**, not anything parsed from §0.2.
- `_retired_section_drift()` reads §0.2 **only to count `- ` bullets**; it never
  reads a bullet's content.
- The ban compares **material datablock names**. Of ~100 retirements in §10,
  **exactly one was ever a material** (the canvas ragtop, already covered).
  Every other is a VALUE, METHOD, CROP or withdrawn TEST — **unreachable**.

**And the false claim was INSIDE THE GUARD.** The comment above the ban read
*"The list is now DERIVED from §0.2 itself, so retiring a reading in the spec
arms the guard automatically and this class of miss is closed."* That sentence
is why the brief said what it said. **A CLAIM IN PROSE IS NOT A GUARD —
INCLUDING WHEN THE PROSE IS INSIDE THE GUARD.** Corrected in place.

**`_retired_value_drift()` is the mechanism that can see §10.64's class**: a
retired literal appearing **unstruck** in the FROZEN front matter is a FAIL, not
a warn — that is how `W_ART = 0.30` stood 3.3× wrong for thirteen revisions.

**IT FIRED ON ITS FIRST RUN AND CAUGHT THREE LIVE DEFECTS §10.64 MISSED**, all
in sections headed **FROZEN**:

| line | published as authoritative | live | retired by |
|---|---|---|---|
| §1.1 | bay taper `0.507 / 0.516 / 0.526`, "they are **not** identical" | EQUAL at **0.5155** | §10.29, §10.47 |
| §1.1 | band `sill z = 1.402, head z = 1.798` | **1.372 / 1.775** | §10.2 |
| §3 | `RED` measured **(196, 106, 36)**, hue 26, grade **M** | **(196, 49, 36)**, hue 5.0 | §10.12 |

§10.47 had already removed the taper sentence from `STATE.md` as hand-authored
and `verify.py:193` already called 1.402/1.798 "the retired band" — **while §1.1
went on publishing both.** All three struck, with the live value beside them.

**THE GUARD WAS WRONG TWICE BEFORE IT WAS RIGHT, and both are recorded:**

1. **First cut swept the change log: 8 FAILs of which 4 were its own false
   positives.** It cut the file at the first `## 10.` heading — but §10.11–§10.33
   are `### 10.xx` headings **interleaved with the front matter** at lines
   ~321–2400, while `## 10.` sits at 2473. So it swept §10.12's and §10.29's own
   bodies, i.e. lines that exist to say *"was 0.0330, is 0.017750"*. **CHECK WHAT
   A GUARD CAN PHYSICALLY SEE — INCLUDING WHICH SECTION.** Section-aware now.
2. **A sub-heading reset the exemption.** `### OPEN, unresolved: rake versus the
   arch gap` (a subsection of `## 10.9`) made the guard fire on `:2701`. That
   line **is** stale — but the guard found it **by accident**, and a guard that
   is right for the wrong reason is not a guard. Heading **depth** is tracked
   now, and `:2701` was fixed by hand instead.

**`SPEC.md:2701` — the defect rev 23 missed forty lines below the table it
struck.** rev 23 struck §10.9's table and inserted "every value in this table is
retired", then left an arithmetic line deriving a 79 mm consequence from the
retired `0.0330`, under a heading still reading **"OPEN, unresolved"** — a
subsection §10.29 had **CLOSED**. Struck, the heading corrected, and what
actually holds recorded: at the live rake the term is **42.6 mm**, and the mesh
measures **39.7 mm** rear with the circular front arch at **40.7 mm** as a
positive control.

**§0.2b added** — 13 entries, bullets **16 → 29**, `_RETIRED_BULLETS_REVIEWED`
bumped in the same commit. It is described in the file as **what it actually
buys**: a forced review, not detection.

**AND ADDING IT SILENTLY DEFEATED THE DRIFT GUARD.** `_retired_section_drift`
split on the **substring** `"## 0.2"`, and `"### 0.2b"[1:7] == "## 0.2"`, so the
new heading became a second split point and the guard went back to reading the
original 16 bullets **while the section had grown to 29** — printing a
reassuring `16`. **Caught by watching the count print**, per this repo's own
acceptance-test rule. Parse is **line-anchored** now, and declines (never passes
silently) if the heading is absent.

**FALSIFIED IN FOUR ARMS:** clean tree **0 fail**; an unmarked retired value
inserted into FROZEN §3 → **1 FAIL at the exact line**; the same value marked
retired → **0 fail** (correct boundary behaviour); a 30th §0.2 bullet →
**1 warn**.

**Ceiling, stated:** by construction `_retired_value_drift` does **not** scan
inside a §10 body or §0.2 — those sections exist to name retired values. It
catches a retirement republished in the FROZEN front matter. It does **not**
catch a §10 entry that contradicts itself; `:2701` was found by an adversarial
read, not by this guard, and nothing here should be read as covering that.


### 10.68  rev 25 — the bake frame PARSED, and the artwork re-baked for the first time since rev 11

rev 24 carried an UNVERIFIED claim forward: that `folk_gen._ZB_AUTH` sits in the
pre-rev-16 tail frame, worth **up to 76 mm** of z error at the tail, "**larger
than `DOOR_X0`**", and that it would therefore **dominate** the re-bake decision.
It was verified this revision. **The magnitude is exact and the conclusion is
REFUTED.**

**(a) The 76 mm is real and carries ZERO INK.** `_ZB_AUTH` did copy `t1_core.ZB`'s
authored knots without `aft_lut`'s `_aft()` re-space. Measured against the live
mesh LUT: **max |dz| = 76.222 mm at x = −1.8730**, exactly `X_TAIL`, exactly the
claimed figure. **But the bake paints nothing there.** Binning the baked ink
against x:

| x band | ink | mean \|sill err\| |
|---|---|---|
| −1.873 … −1.400 (the whole 76 mm region) | **0 px** | — |
| −1.400 … +1.900 | 439 185 px | 0.01 mm |
| +2.050 … +2.070 | 21 133 px | 8.44 mm |
| **+2.070 … +2.090** | 12 584 px | **16.39 mm** |

Two controls isolate the mechanisms: re-space alone **75.540 mm**, dropped knots
alone **20.925 mm**; ink-weighted over the live body, total **0.7818 mm** of which
**the re-space contributes 0.0023 mm — two microns.** So where it touches paint
the claimed mechanism is not larger than `DOOR_X0`; it is ~7 500× smaller.

**(b) A DIFFERENT `_ZB_AUTH` defect is real and was never named.** The re-typed
table **omitted five knots** — `−2.086, −2.050, −1.900, −1.200, +2.085`. The one
that reaches ink is **+2.085, at the NOSE**: **19.477 mm** peak, touching
**3.53 %** of the primary-copy ink, and it is essentially the whole ink-weighted
error.

**(c) `DOOR_X0` DOMINATES, and worse than rev 23 recorded.** Verified by hand off
`t1_shell`'s constant graph: `BAYS[0][1] = 0.929750`, `B_PILLAR` default
`0.0120`, `_DOOR_REAR_X0 = 0.9245` → **`DOOR_REAR_DX = 17.250 mm`**. The
consequence nobody had computed is the WIDTH: `folk_gen.DOOR_W` was **0.908700**
against a true **0.891450**, **1.935 % too wide**, and `DOOR_W` is the divisor for
every u-coordinate of the door art. Over the door ink: displacement ink-weighted
**6.290 mm**, max **17.247 mm**, **82.5 % displaced > 2 mm**, 57.9 % > 5 mm, and
**3 411 px past the true rear shut line** — an overhang of **1.44× the entire
B-pillar width**.

**THE CONTROL FAILED, AND THAT WAS THE FINDING.** Re-baking with the constants
**unchanged** does not reproduce the committed artefacts: `swirl.png` **4.029 %**
of pixels differ, `swirl_b.png` **4.261 %**, max Δ **255**; `nose.png` is
byte-identical. The control's own premise was checked before it was interpreted —
two bakes in **separate processes** give identical md5s, so the bake is
**deterministic** and this is not seed noise. A bisect then closed it with no
inference in it: holding the whole tree at rev 24 and swapping in **only** the
pre-rev-23 `folk_gen.py` reproduces the committed files **BYTE-IDENTICALLY**
(`1e1c2bd5…`, `f8ed6e71…`). `git log -- tex/swirl.png` last writes it at
`9a227cd`, **rev 11**. **The model was wearing artwork fourteen revisions old**,
and rev 23's "NOT RE-BAKED — nothing in the current build changed" is true of the
BUILD (no guard figure moved) while leaving a 4 % divergence from its own
corrected source. Under §10.10 that settles the re-bake.

**THE FIX IS STRUCTURAL — the work rev 23 named and declined to do blind.** A
deliberately tiny bounded evaluator `_ceval` (no attribute access, no imports, no
arbitrary calls) reads `t1_shell`'s constant GRAPH — `DOOR_GAP`'s expressions,
`BAYS`' comprehension, `B_PILLAR`'s `os.environ` default — and `t1_core`'s `ZB`
knots, so `DOOR_X0` is **expressed in terms of `BAYS[0][1]`** exactly as
`t1_shell` expresses it, `_ZB_AUTH` is the real table re-spaced by the real
`_aft()`, and **`T1_BPILLAR` now moves the ART frame with the geometry**. Three
further re-typed literals removed (`TIRE_R`, `ARCH_R`, `X_AXLE_R`) — **all three
still AGREED, so that is exposure removed, not damage repaired**, and their
provenance comment was wrong (`t1_core.py:80` / `t1_shell.py:254`, not `:35` /
`:203`). Every parse **RAISES** rather than falling back.

**FALSIFIED IN FOUR ARMS**, and the fourth is a cross-confirmation. The parse
raises on every missing name; `T1_BPILLAR=0.0300` moves `DOOR_X0` to `0.943650`;
and **the B-pillar width that reproduces the retired `DOOR_X0 = 0.9084` exactly
is −0.005250 m** — the NEGATIVE pillar width §10.62 found in the GEOMETRY, whose
independently derived reproducing value was **−0.0053**. **They agree to
0.050 mm, from two unrelated routes** (§10.62's shut-line crossing probe and this
revision's texture frame). The door art had been drawn to a door that could not
open.

**`_DOOR_TOP_AUTH` DELIBERATELY NOT PARSED, and the reason is a mistake of
mine.** I derived it as the mean of the outline's top run and wrote "within 1 mm
of the historical 1.8140" into my own comment **before watching it print**. The
print refuted me at **4.2 mm** (the run means 1.80980). It is HELD at the
authored **1.8140** so `DOOR_H` stays bit-identical and only one lever moves in
this bake; the 4.2 mm is carried forward as an open item rather than absorbed
into an unrelated fix. *Do not put a figure in prose unless you watched it
print — including in a comment you are writing at that moment.*

**RE-MEASURED AFTER THE BAKE:** door ink past the true rear shut line
**3 411 → 0 px**; sill LUT max error over the body **76.222 → 0.000000 mm**;
ink-weighted **0.7818 → 0.000000 mm**; ink where |err| > 10 mm **21 057 → 0**.
**§10.10's own targets held or improved:** flank density rms **3.59 → 3.58**
(show) and **3.98 → 3.96** (off); zone residuals show R1 **−0.44 → +0.29** and
R2 **+0.58 → −0.14**. **One went the other way and is stated, not hidden:** door
gold **29.09 → 28.90** against a 29.08 target — 0.18 off where the committed arm
was 0.01, inside the **28.96–29.19** round-to-round spread watched printing
across seven solver rounds, but not an improvement. `tex/nose.png` UNCHANGED
(md5 `b31ea156`). New: `swirl.png` `4ee4e09e`, `swirl_b.png` `d201597e`.
_(rev 26: this line read `d2015971` — wrong in its eighth character. The FILE
was always correct; only the record was wrong. See §10.74.)_

**NO GEOMETRY MOVED.** Guards 0 fail / 0 warn at both levels, every figure
identical.


### 10.69  rev 25 — nine more §10.64-class defects, each verified against three things

Extending `verify._RETIRED_VALUES` from **5 rows to 15**. A read-only subagent
proposed "**~12 further defects** in §1, §2, §3, §6, §10.5, §10.7". **A
SUBAGENT'S FINDING IS A CLAIM**: every candidate was verified by hand against
**three** things before a row was written — the SPEC line, the LIVE value read
out of the **CODE** (never out of other prose), and the §10 sentence that retires
it. **Nine survived. Four were refuted or mislocated.**

**CONFIRMED and struck** (guard fired at each of these 12 lines, then 0):

| § | line | retired literal | live value, from code |
|---|---|---|---|
| 1.1 | 146–149 | the four bay/panel rows | `BAY_W = 0.5155` equal; panel **1.0175 m** |
| 2 | 187 | "nose-down ~1.7°… **Not modelled yet**" | `RAKE_DZDX = 0.017750`, modelled at `build.py:537` |
| 2 | 190 | `x = +2.108 / −2.108`, "~99 mm… Unresolved" | `X_TAIL = −1.8730`; 99 mm **refuted at 10σ** |
| 2.5 | 227 | "fish-eye / teardrop, correct for a 1963" | `bullet_indicator`, `build.py:354` |
| 2.3 | 246 | "Overall height measures **1.960**" + proud 0.10–0.15 | `H_ROOF` RETIRED (§10.59); proud **26 ± 7 mm** (§10.9) |
| 2.3 | 249 | "Lens type remains **U**" | resolved by §10.22 |
| 3 | 264 | `⌀ ≈ 0.370`, `centre z ≈ 1.130` | `ROUNDEL_D = 0.2800`, `ROUNDEL_Z_AG = 1.0170` |
| 3 | 268 | "flat oval **fish-eye**… bullet pods period-wrong" | bullet kept, flat-oval **REFUTED** (§10.22) |
| 6 | 302 | "composited to **pure white**" | `post.BACKDROP = "headroom"` (§10.32, owner's call) |
| 9 | 371 | `` `RIDE_DROP` ≠ 0 → FAIL `` | `RIDE_DROP_SPEC = 0.065`, FAIL unless EQUAL |

**TWO OF THESE ARE SHARPER THAN THE REST.**

**§1.1's rows defeat the guard's own matching by RE-EXPRESSION.** Row 4 of the
original table keys on the literal `"0.507 / 0.516 / 0.526"` — which now exists
**only inside the strike that retires it**, three lines below. The identical
retired taper survives unstruck **as edge pairs**: differenced they give
**0.507 / 0.516 / 0.525**, and their midpoints sit **105.5 / 110.0 / 99.5 mm
AFT**, i.e. §10.29's 100 mm origin error, carried in the same rows. **A retired
value re-expressed in another form — edges for widths, mm/m for m/m, degrees for
slope — is invisible to a substring guard. That is this guard's real ceiling and
it is now stated rather than discovered later.**

**§9 row 10 published the INVERSE of the guard that runs**, and contradicted §2
inside the same frozen front matter: §9 said any non-zero `RIDE_DROP` is a
failure while `verify.py:796` fails unless it equals `0.065` exactly, and §2's
own **Ride height** row orders `RIDE_DROP = 0.065`. Rev 4 zeroed it, rev 5
reinstated it on Donald's own reading, and §9 was never updated. As published,
the rule would fail every current build.

**REFUTED from the subagent's list, recorded so nobody re-adds them:**

- **"§0.2 bullet 13's refuted fish-eye."** The substance is right, the *location*
  is wrong: `SPEC.md:71-72` is inside §0.2, which `_is_log` exempts **by design**
  (§0.2 exists to name retired readings). The real front-matter republications
  are `:227` and `:268`, which the brief did not name.
- **"§10.5 and §10.7 are defect sites."** They are not. Both sit under
  `## 10. rev 7 — the canonical constants` and are **skipped**. A change log
  recording "rev 7 locked X, we now use Y" is CORRECT, not a defect — §10.67
  already states this ceiling.
- **"~12 defects."** Nine. The brief's own enumerated list was five, of which
  four are real and one is mislocated.
- **Bumper faces `±2.145` (`:191`) vs `X_BUMP_F/R = ±2.140`.** Real 5 mm drift,
  but **no §10 entry retires either value in either direction** — so it is
  DIFFERENT, not RETIRED, and adding a row would assert a retirement that does
  not exist. **Carried forward as an open item, not as a guard row.**

**FALSIFIED IN FOUR ARMS:** clean tree **0 fail**; an unmarked `⌀ ≈ 0.370`
injected into FROZEN §3 → **1 FAIL at the exact line**; the same value marked
retired on its own line → **0 fail** (correct boundary); restored → **0 fail**.
And, per §10.67's own lesson, **the §0.2 bullet count was WATCHED PRINT: 29
counted, 29 in `_RETIRED_BULLETS_REVIEWED`**, with the parse line-anchored.


### 10.70  rev 26 — `COUNTERTAN`'s pedestal is the SETTLED-DUST FILM, and rev 20 measured the wrong derivative

Six revisions on the work list, "UNIDENTIFIED" since §10.56. It is identified,
and the constant that produces it has been in plain text in `t1_mats.py` the
whole time.

**MEASURED.** Four arms — two albedo points (`COUNTERTAN` built-in and
`T1_CTAN=0.02,0.02,0.02`) × dust shipped / dust off — through rev 24's
index-clean mask, at ONE purged light rig (§10.65's stacking defect), EV −4,
0.001–0.002 % clipped in every arm. `R = kA + P` fitted per channel:

| arm | pedestal `P/R` (R / G / B) | `k` (R / G / B) |
|---|---|---|
| shipped (dust 1.4, wear 0.7, spec 0.32, coat 0.05) | **60.8 / 58.2 / 59.5 %** | 0.03677 / 0.03623 / 0.03719 |
| `T1_CTAN_WEAR=0` | 55.3 / 52.5 / 53.4 % | 0.04461 / 0.04396 / 0.04509 |
| **`T1_CTAN_DUST=0`** | **25.1 / 25.0 / 31.9 %** | 0.07310 / 0.07165 / 0.07399 |
| `T1_CTAN_DUST=0` **and** `T1_CTAN_SP=0 T1_CTAN_CT=0` | **6.6 / 6.6 / 8.5 %** | 0.08713 / 0.08604 / 0.08891 |

Share of the shipped pedestal removed: **wear 3.2 / 3.7 / 5.1 %**;
**dust 57.1 / 52.6 / 36.6 %**; **dust + spec + coat together
89.3 / 87.9 / 84.8 %.** What survives all three is **6.6 / 6.6 / 8.5 %**, i.e.
**10.7 / 12.1 / 15.2 % of the original pedestal** — small enough to be the
ordinary interreflection floor, and NOT claimed as identified.

**HARNESS CONTROL — the part that makes this readable.** The dust-shipped arm
reproduces §10.65's published clean pedestal — **60.8 / 58.2 / 59.5 %** — to
three significant figures in all three channels, on a tree restored
independently from the bundles. Same chain. Null control passed **exact** (IoU
1.0000, 0 disagreeing px) in every arm; region-mean noise floor **0.211 %**
against an effect of ~35 percentage points.

**WHY FIVE REVISIONS MISSED IT — this project's own rule, running backwards.**
§10.56 ablated dust, measured the top's radiance RISE at +4.1 / +8.6 / +13.3 %,
and concluded *"the dust hypothesis is REFUTED — and it was HELPING."*
**That does not follow.** For a mix of coverage `f` and base-independent colour
`D` over base `A`, removing the term changes radiance by `f·(A − D)` while it
contributes `f·D` to the pedestal. `W_DUST_COL_UP = (0.5077, 0.3775, 0.2340)`
is **within 13.5 % of `COUNTERTAN` in R**, so `f·(A − D)` is small *precisely
because* the deposit is nearly the colour of the wood — and `f·D` is large at
the same time. **Both observations are true simultaneously.** §10.56 measured
`dR/d(dust)` at the shipped albedo and drew a conclusion about `P`.

This is §10.68's rule inverted, and it should be written down that way: **a
SMALL magnitude does not mean a small contribution, when the derivative you
measured is not the one your conclusion is about.** The same logical defect was
applied to `wear` and `fade` and happened to reach the *right* answer there,
because `W_PRIMER` is ~4.5× darker than the base — **conclusion-safe,
method-unsafe**. The wear arm above confirms it at 3.2 / 3.7 / 5.1 %.

**THE COVERAGE WAS NEVER HIDDEN.** `t1_mats.py:366` states in prose
*"`W_DUST_FAC_UP` 0.7313, i.e. mean coverage 0.548 on the counter top"*, and a
**live assert** at `t1_mats.py:441` recomputes
`W_DUST_UP_W × W_DUST_MOT_MEAN × W_DUST_FAC_UP × 1.4 = 0.548256` on every
build. A base-independent colour at **54.8 % coverage IS a pedestal by
construction.**

**INDEPENDENT CROSS-CHECK, from an unrelated route.** A base-independent mix at
coverage `f` dilutes the base by `(1 − f)`, so removing it must raise `k` by
`1/(1 − f) = 2.214×`. **Measured `k_off/k_on` = 1.988 / 1.978 / 1.989.** Right
direction, right magnitude, ~10 % apart — the residual is chain non-linearity
(the fade `HueSaturation` is not linear in saturation) plus interreflection
across a 29× albedo secant. **Agreement is claimed to ~10 %, not better.**

**THE LEVER WAS CHECKED BEFORE IT WAS BELIEVED**, per §10.56's own rule that a
ray-visibility flag is not an ablation. The WEATHER group's `Dust` input reaches
`dfac → cdust → Base Color` (`t1_mats.py:855, 862, 887`) and **nothing else**:
Roughness comes from the fade path (`r7`), Metallic from the wear path
(`steel`). `T1_CTAN_DUST=0` removes the **ALBEDO**. `T1_CTAN_WEAR=0` also drops
Metallic, so that arm is **two levers, stated rather than presented as pure.**

**WHAT THIS DOES NOT MEAN.** It is **not** an error and nothing is tuned on it.
The dust film is a modelled, measured feature; a 59 % pedestal simply means the
counter top's appearance is dominated by settled deposit and a grazing specular
lobe rather than by the wood albedo. What it *does* settle is **why
`COUNTERTAN` has never been solvable**: `k = 0.0368` in the shipped
configuration against **0.0871** for a clean surface — the albedo lever is
**2.37× weaker than the surface itself allows**, by construction. rev 15's
"closing on albedo demands (0.177, 0.408, 0.094), not any wood" is explained,
not overturned. **`COUNTERTAN` UNCHANGED at (0.5870, 0.4930, 0.3060), sixth
revision running.**

**Also corrected here:** §10.56's `T1_CTAN_SP=0 T1_CTAN_CT=0` arm reads −3.1 /
−3.7 / −7.1 % of the top's *radiance* and was filed as "excluded". As a share
of the **pedestal** the same lever is worth **32 / 35 / 48 points** — the third
instance of the identical non-sequitur inside one section.


### 10.71  rev 26 — `W_DUST_FAC_UP` is solved against the WRONG MATERIAL, and both halves are in one commit

Found while verifying §10.70; **RECORDED, NOT APPLIED**, because it moves the
shipped build.

`t1_mats.py:441-448` is a live assert:

```
_f_up = W_DUST_UP_W * W_DUST_MOT_MEAN * W_DUST_FAC_UP * 1.4     # = 0.548256
_pred = tuple(c + _f_up * (d - c) for c, d in zip(COUNTERCREAM, W_DUST_COL_UP))
assert max(abs(p - m) for p, m in zip(_pred, _UP_MEASURED)) < 2e-3
```

`_UP_MEASURED = (0.6104, 0.5300, 0.4265)` is commented **"dirty counter top,
de-illuminated"**. The assert predicts it from **`COUNTERCREAM`**. But the
counter top carries **`COUNTERTAN`**, and has since rev 12.

| base used | predicted dusty top | vs `_UP_MEASURED` | |
|---|---|---|---|
| `COUNTERCREAM` (what the assert uses) | (0.6104, 0.5300, 0.4264) | max err **0.0001** | PASSES |
| `COUNTERTAN` (what the surface is) | (0.5435, 0.4297, 0.2665) | max err **0.1600** | **FAILS by 80× its own tolerance** |

**Both halves were introduced in the SAME COMMIT** — `00d3819`
*"rev 12: cut the roof hole; signboard is not a lid; **tan counter top**;
weathering + roughness"*. In one commit rev 12 made the top tan and solved the
up-face dust coverage against the cream, using a patch labelled "dirty counter
top". `git log -S '_UP_MEASURED'` returns that commit and no other.

**They cannot both be right.** Either `_UP_MEASURED` is not the counter top —
in which case its comment is a phantom and the constant needs a correct label —
or it is, in which case **`W_DUST_FAC_UP = 0.7313` is unsupported for the
surface whose appearance §10.70 has just shown it dominates.** The assert
cannot see the difference: it would keep passing however far `COUNTERTAN`
moved, because it never reads `COUNTERTAN`.

Same family as the dead `RIM_R`, the dead `countertan` shader arguments,
`_NOSE_SEL` and `FadeVert`: **a constant landed on the material whose NAME
matched, not on the surface it describes.** Fifth instance.

This is rev 27's item 1 and it is now a *named, localised* question rather
than "UNIDENTIFIED".


### 10.72  rev 26 — the ±2.145 / ±2.140 bumper question is MALFORMED: both numbers are the factory catalogue, halved

rev 25 carried this as *"a real 5 mm drift — establish which is right, retire
one."* There is nothing to pick between.

- **`2.145 = 4.290 / 2` exactly; `2.140 = 4.280 / 2` exactly.** Both rows change
  in the **same diff hunk** of `27f6ee6`, *"SPEC rev 4: evidence audit against
  reference **+ factory sources**"* — `Overall length over bumpers 4.280 →
  4.290` on one line and `Bumper faces ±2.140 → ±2.145` on the next. **The 5 mm
  is exactly half of a catalogue revision.** Nothing was re-measured.
- `verify.py:33` already records *"4.290 came from the 1950-67 T1 catalogue"*
  and `verify.py:37` invokes the standing instruction — *never correct this
  vehicle toward the VW factory catalogue* — to make the measurement win for
  `L`. **§2's bumper row never received that treatment.** §2's own header grades
  the table **S (1963 factory brochure) unless noted**, and this row carries no
  note. Two of the other three items in that same rev-4 sentence were later
  refuted (the 6.40-15 tyre by rev 6, the stock ride height by rev 5).
- **`X_BUMP_F` and `X_BUMP_R` are DEAD.** `grep -rn X_BUMP --include=*.py`
  returns exactly two lines: `t1_core.py:73` and `:74`, their own definitions.
  Zero read sites. Already noted in `AUDIT_rev18_loft.md:589` and never acted on.
- **The mesh cannot arbitrate, because it was fitted to the constant.**
  `t1_detail.py:382` reads `BUMP_OFF = 0.0075  # standoff so the outer face
  lands on x = +/-2.140`. Circular.
- **The rear face does not exist.** `build.py:325` has `bumper(False, …)`
  commented out per §2.4, so `±` asserts a rear bumper face **fourteen lines
  below §2.4's own "model it absent"**.
- **CITATION DEFECT, born stale in its own commit.** §10.69, `HANDOFF_rev25.md`
  and the rev-26 prompt all cite the row as `SPEC.md:191`. At HEAD it is
  **`:201`** — `:191` is the Track row. The row moved in `208e92f`, **the same
  commit that wrote the citation.**

**VERDICT: neither value is measured and neither is supported.** The rev-25
instruction *"do NOT add a `_RETIRED_VALUES` row for the ±2.145 bumper faces"*
**still stands and for a stronger reason than it was given** — a row would
assert that one of them is live, and neither is. The correct action is to strike
both as catalogue-derived and re-open the front bumper face as **UNMEASURED**.
**No geometry moved on this finding and none should until it is measured.**

**Why it has never been measured, and the one opening:** in `ref_side.jpg` the
front bumper face is occluded by the lamppost at columns 62–79 — the feature
`verify.py:43` names as the source of three confident wrong numbers, and
§10.24's standoff finding was withdrawn for exactly that reason.
**`ref_workshop.jpg` has no lamppost and the bumper is completely clear.** A
question was put to the owner with printed crop boxes (A the upper tube, B the
lower blade, C the vertical post between them) asking which members belong to
the vehicle — because the model builds only a blade plus two 62 × 30 mm
brackets (`bumper_irons`) and **has no member for the tube at all**. Answer
pending at time of writing. **The boxes were stated to him as POINTERS, not
sampling windows**, and the first draft was thrown away — box A sat on the green
body above the tube and box B straddled the blade and a foreground trolley rail.
**Fifteenth instance of check-what-the-probe-can-see; second caught before it
reached him.**


### 10.73  rev 26 — work item 2 is an ARTEFACT: `_DOOR_TOP_AUTH`'s "4.2 mm" is a mean compared with a station value

rev 25 held `_DOOR_TOP_AUTH` at the authored **1.8140** against the door
outline's top-run mean **1.80980**, carried the 4.2 mm forward as an open item,
and recorded the process lesson *"a claim in prose is not a guard — including a
comment you are writing right now; 'within 1 mm' was refuted at 4.2 mm in the
same minute."*

**The comment was right. The print computed a different quantity.**

`_DOOR_TOP_AUTH` has exactly one use, `folk_gen.py:503`:

```
DOOR_H = ((_DOOR_TOP_AUTH - rake_drop(1.36)) - door_bot_z(1.36))
```

`rake_drop(1.36)` is subtracted from it, which is only meaningful if it is an
**un-dropped z at station x = 1.36** — and the bottom term is evaluated at that
same single station. So `_DOOR_TOP_AUTH` is a **height at a station**, by the
construction of the line that consumes it. `1.80980` is a **run mean** over a
crowned run whose two end knots are corner roll-offs:
`t1_shell.py:487-489` gives z = 1.8020, 1.8130, **1.8150**, 1.8130, 1.8060 —
the rail rises 13 mm off the hinge corner and falls 9 mm into the latch corner,
and averaging the corners into it drags the mean down.

Compared like for like at x = 1.36, re-implementing `_resample`/`_smooth`
(`t1_shell.py:95-110`) as pure arithmetic:

| quantity | value | vs authored 1.8140 |
|---|---|---|
| 5-knot top-run **mean** (the figure rev 25 quoted) | 1.809800 | **−4.200 mm** |
| raw `DOOR_GAP` top edge **at x = 1.36** | 1.814333 | **+0.333 mm** |
| **`DOOR_GAP_S`** top edge at x = 1.36 — *the outline that actually cuts the geometry* | **1.814315** | **+0.315 mm** |
| `DOOR_GAP_S` top-run maximum | 1.814670 | +0.670 mm |

Chain cross-check in the same computation: `DOOR_REAR_DX` comes out
**0.017250 m = 17.250 mm**, reproducing §10.68's independently derived figure
exactly, which is what shows the re-implementation is the repo's own arithmetic.

**`_DOOR_TOP_AUTH = 1.8140` agrees with `t1_shell`'s own door outline to
0.315 mm at the station where it is used.** rev 25's instruction *"do not change
it to 1.8098 without a measurement"* **stands, and for a better reason than the
one given**: adopting 1.8098 would move `DOOR_H` by −4.200 mm (−0.41 % on every
v of the door art) on the strength of a mis-specified statistic. **No re-bake is
owed. `DOOR_H` = 1.013467 unchanged.**

**What IS open is smaller and harder, and it is not what the item said.** Both
numbers are authored: `1.8140` has no provenance anywhere in the repo (six
occurrences, all itself or prose about itself), and `1.80980` is the mean of
five equally unprovenanced literals. **The cab door's true top-edge height is
UNMEASURED and, on the admissible set, unmeasurable**: `ref_side.jpg` has the
door OPEN (§10.11's frame, and the worst in the set at 2.32 bits/px);
`ref_workshop.jpg` has it closed but is a three-quarter view with **no
admissible px/m on the door plane** (`t1_shell.py:471-476` says so); and
`ref_rear34.jpg`'s 344.1 ± 6.7 is the **plate plane only** (§10.48) at the far
end of the vehicle. Nothing on this project measures anything to 0.32 mm — the
best longitudinal measurement in the repo carries ±22 mm.

**Incidental, same line:** `folk_gen.py:503`'s trailing comment reads
`# ~1.017 m` where the line computes **1.013467** — 3.5 mm, another figure in a
comment that was never watched print. Corrected.


### 10.74  rev 26 — two defects in rev 25's own record, caught on the way in

Neither changes the model; both would have cost the next context real time.

- **`swirl_b.png`'s md5 is wrong in its eighth character.** `SPEC.md:2821` and
  `NEXT_CONTEXT_PROMPT_rev26.md:147` record `d2015971`; the committed file is
  **`d201597e`**`1c867b6e1fbedd2c0f8ab306`. The FILE is correct — the working
  tree and `HEAD` agree byte-for-byte and it is what `9ad9a3b` wrote — only the
  record is wrong. `swirl.png` `4ee4e09e` and `nose.png` `b31ea156` both check
  out. Corrected here and in §10.68.
- **`NEXT_CONTEXT_PROMPT_rev26.md:283`'s content check cannot pass on a fresh
  clone.** It asks for `ls HANDOFF_rev25.md rev25_hero34f.png`, but
  `.gitignore:9` is `rev*_hero*.png` and commit `091ff2e` is titled *"keep the
  hero OUT of the repo, as every prior revision did"* — which §7 of the same
  prompt explains at length. **§1 and §7 of one document contradict each other**,
  and a context following §1 literally would have reported a lost commit.
  The hero is on the owner's disk at 15 516 379 bytes, which is where every
  prior revision's hero lives. **The check is DELETED, not loosened** — the
  rev-21 `STRADDLING` precedent, not the rev-22 `H_ROOF_REGRESSION` one, because
  this string can never match a clean tree rather than merely having the wrong
  count.


### 10.75  rev 26 — THE FRONT BUMPER CARRIES AN OVER-RIDER BAR THE MODEL DOES NOT BUILD

**SETTLED BY THE OWNER**, from a marked figure on `ref_workshop.jpg` — the one
frame in the set where the front bumper is **not occluded by the lamppost**
(`ref_side.jpg` columns 62–79, the feature `verify.py:43` names as the source of
three confident wrong numbers, and the reason §10.72 leaves the bumper face
UNMEASURED).

Shown the photograph beside a render of the model's own front end, with three
pointer boxes printed in original-frame coordinates, he ruled:

| box | region | reading |
|---|---|---|
| **A** `(260,664)-(286,673)` | the upper tube across the nose | **ON THE BUS — a bumper OVER-RIDER BAR** |
| **B** `(230,697)-(266,723)` | the lower pale blade | the bumper blade — the model does build this |
| **C** `(357,681)-(374,697)` | the vertical post between them | **ON THE BUS — an over-rider joining A to B** |

**THE MODEL HAS NO MEMBER FOR EITHER A OR C.** `build.py:322` builds one blade
(`D.bumper(True)`) and `build.py:326` builds `bumper_irons(True)` — two
`62 × 30 mm` rounded-rect prisms 150 mm long at `x = 2.045, y = ±0.470`
(`t1_detail.py:~370`). Neither is a transverse tube, and neither is the vertical
post at the vehicle's centreline that the photograph shows. Confirmed against a
render of the current build made this revision: **one plain cream blade, nothing
above it.**

**SCOPE, also settled by him: MODEL THEM, TAGGED WORKSHOP-STAGE.** This matters
because `ref_workshop.jpg` is the CONVERSION stage and §2.4 records that the
**rear** bumper was removed between that stage and service — so front hardware
present in the workshop is not automatically present in service, and no
in-service frame shows the front. Every number derived from this reading is to
be tagged workshop-derived in SPEC, the same treatment Nolita geometry gets
(§10.32), so it can be pulled back out if an in-service frame ever contradicts
it.

**THE MEASUREMENT IS NOT DONE, AND THE FIRST PASS FAILED ITS OWN CONSISTENCY
CHECK.** Recorded rather than tidied away:

- A naive two-run column scan over rows 628–762 returned "blade height" of
  **30, 42, 41, 36, 34, 12, 9, 11 px** across eight columns — a 4.7× spread. The
  cause is that the **foreground trolley rail occludes the blade's lower edge**
  over most columns, and the scan window truncated the tube at its top row. The
  derived ratio came out **0.574 ± 0.507**, i.e. an uncertainty almost as large
  as the value. **It is not quoted anywhere and must not be resurrected.**
- Restricted to columns 248–272, the only run where the blade's lower edge is
  clear, and **sweeping the threshold rather than picking one** (§10.41's rule),
  the tube's diameter reads:

| lum threshold | 110 | 120 | 130 | 140 | 150 | 160 | 170 |
|---|---|---|---|---|---|---|---|
| tube dia (px) | 11.7 | 11.4 | 11.0 | 9.9 | 9.1 | 8.6 | 7.9 |
| sd over 7 columns | 0.5 | 0.5 | 0.8 | 0.4 | 0.4 | 0.5 | 0.4 |

  So the tube is **7.9–11.7 px**: tight *within* any one threshold (sd ≤ 0.8)
  and **±19 % across the threshold choice**. That systematic, not the scatter,
  is the binding uncertainty.

- **MY PSF CONTROL WAS INVALID AND IS RECORDED AS SUCH.** I fitted a 10–90 edge
  rise on the nose two-tone break and got **52.0 px**, which would make a 10 px
  feature unmeasurable. That number is wrong: the window I chose crosses the
  two-tone boundary **diagonally**, so it measured the boundary's slope across
  the window, not the point spread. §10.38's lesson — *check the control itself,
  not only the number* — applying to a control written in the same session.
  **A real PSF on this frame is still owed and no width claim should rest on the
  52 px figure in either direction.**

**NO METRE FIGURE IS AVAILABLE AND NONE IS INVENTED.** There is no admissible
px/m on the bumper plane in this frame: `ref_workshop.jpg` is a three-quarter
view with a projective flank map nobody has built (`t1_shell.py:471-476` says so
for the door plane), §10.48's **344.1 ± 6.7 is the PLATE plane of a different
photograph**, and §10.72 has just established that the bumper face's own station
is unmeasured. The headlamp is the nearest locked candidate ruler and sits on a
different depth and a curved surface.

**WHAT REV 27 INHERITS**, well-posed rather than half-done: the reading is
settled; the gap in the model is confirmed against a render; the tube is
bracketed at 7.9–11.7 px with the threshold systematic identified as the binding
term; a valid PSF and a scale on the nose/bumper plane are the two things that
must come first. **No geometry was changed on this finding in rev 26.**


## Change log

| Date | Change |
|---|---|
| 2026-08-15 | **rev 26 — the front bumper carries an OVER-RIDER BAR the model does not build (§10.75).** Shown `ref_workshop.jpg` — the ONE frame where the front bumper is not occluded by the lamppost — beside a render of the current build, with three pointer boxes printed in original-frame coordinates, the owner ruled **A (the upper tube) and C (the vertical post) are BOTH ON THE BUS**: a bumper over-rider bar and its post. **The model has no member for either** — `build.py:322` builds one blade and `:326` two 62 × 30 mm brackets. Confirmed against a render made this revision. **Scope also settled by him: model them, TAGGED WORKSHOP-STAGE**, because `ref_workshop.jpg` is the conversion stage and §2.4 records the REAR bumper was removed between that stage and service — so front hardware present in the workshop is not automatically present in service, and no in-service frame shows the front. Tagged the way Nolita geometry is (§10.32), so it can be pulled back out. **THE MEASUREMENT IS NOT DONE AND THE FIRST PASS FAILED ITS OWN CONSISTENCY CHECK, recorded rather than tidied away**: a naive column scan returned blade heights of 30/42/41/36/34/12/9/11 px — a 4.7× spread caused by the foreground trolley occluding the blade's lower edge — giving 0.574 ± 0.507, which is not quoted anywhere. Restricted to the seven clean columns and **sweeping the threshold rather than picking one**, the tube reads **11.7 → 7.9 px across thresholds 110 → 170 with sd ≤ 0.8 within each**: tight per threshold, **±19 % across the choice**, and that systematic is what binds. **MY OWN PSF CONTROL WAS INVALID AND IS RECORDED AS SUCH** — the 10–90 rise I fitted crossed the nose two-tone break DIAGONALLY, so its 52.0 px measured the boundary's slope, not the point spread; §10.38's *check the control itself* applying to a control written in the same session. **No metre figure is available and none is invented**: there is no admissible px/m on the bumper plane in this three-quarter frame, §10.48's 344.1 is the plate plane of a different photograph, and §10.72 has just established the bumper face's own station is unmeasured. **NO GEOMETRY WAS CHANGED on this finding.** rev 27 inherits it well-posed: valid PSF first, then a plane scale or a proof none is admissible, then build. |
| 2026-08-15 | **rev 26 — `COUNTERTAN`'s pedestal is IDENTIFIED after six revisions, and it is the settled-dust film (§10.70).** Four arms — two albedo points × dust on/off — through rev 24's index-clean mask at ONE purged rig: pedestal **60.8/58.2/59.5 % → 25.1/25.0/31.9 %** with `T1_CTAN_DUST=0`, and **→ 6.6/6.6/8.5 %** once spec and coat go too. **Dust carries 57.1/52.6/36.6 % of it; dust + spec + coat carry 89.3/87.9/84.8 %.** The dust-shipped arm **reproduces §10.65's published clean pedestal to three significant figures in all three channels** on an independently restored tree — that harness control is what makes the rest readable; null control exact in every arm, noise floor 0.211 % against a 35-point effect. **WHY FIVE REVISIONS MISSED IT:** §10.56 ablated dust, saw the top's radiance rise only +4.1/+8.6/+13.3 %, and concluded "REFUTED — and it was HELPING". **That does not follow.** Removing a mix of coverage `f` and base-independent colour `D` changes radiance by `f·(A−D)` — small *precisely because* `W_DUST_COL_UP` is within **13.5 %** of `COUNTERTAN` in R — while contributing `f·D` to the pedestal, which is large. Both true at once; §10.56 measured the wrong derivative. **§10.68's rule inverted: a SMALL magnitude does not mean a small contribution.** The coverage was never hidden — `t1_mats.py:366` says "mean coverage 0.548 on the counter top" in prose and a **live assert** recomputes 0.548256 on every build. **Independent cross-check from an unrelated route:** removing a mix at coverage `f` must raise `k` by `1/(1−f) = 2.214×`; measured **1.988/1.978/1.989**, agreement claimed to ~10 % and no better. The lever was checked before it was believed — `Dust` reaches Base Color and nothing else, so it removes the ALBEDO per §10.56's own rule; `T1_CTAN_WEAR=0` also drops Metallic and is stated as two levers. **Nothing tuned: `COUNTERTAN` UNCHANGED, sixth revision.** What this settles is *why* it was never solvable — `k` is **2.37× weaker** in the shipped configuration than the bare surface allows, by construction. **§10.71, found while verifying that and RECORDED NOT APPLIED:** `W_DUST_FAC_UP = 0.7313` is pinned by a live assert that predicts `_UP_MEASURED` ("dirty counter top") from **`COUNTERCREAM`**, while the top carries **`COUNTERTAN`** — re-anchored to the right base the assert **fails by 0.1600, eighty times its own 2e-3 tolerance** — and **both halves entered in ONE commit**, `00d3819` "…tan counter top…". The name-matched-material family again, fifth instance. **§10.72 — work item 3 is MALFORMED:** `2.145 = 4.290/2` and `2.140 = 4.280/2`, both changed in the **same diff hunk** of `27f6ee6` "…against factory sources", so the 5 mm is exactly half a catalogue revision; `verify.py:33` already records 4.290's catalogue origin and `:37` invokes the standing instruction for `L` while §2's bumper row never got it; `X_BUMP_F/R` have **zero read sites**; `BUMP_OFF`'s own comment shows the mesh was **fitted to the constant**; the rear face is commented out at `build.py:325`; and the `:191` citation is stale (`:201`), **born stale in the commit that wrote it**. Neither value is measured — strike both, re-open as UNMEASURED. **§10.73 — work item 2 is an ARTEFACT:** `_DOOR_TOP_AUTH`'s "4.2 mm" compares a five-knot **run mean** with a **station value**; at x = 1.36 on `DOOR_GAP_S`, the outline that actually cuts, the disagreement is **0.315 mm**. rev 25's pre-print comment was right and its print measured a different quantity. Value HELD, **no re-bake owed**, `DOOR_H` 1.013467 unchanged. **§10.74 — two defects in rev 25's own record**, caught on arrival: `swirl_b.png`'s md5 wrong in its eighth character (`d2015971` → **`d201597e`**; the file was always right), and §1's `ls rev25_hero34f.png` check **cannot pass on a fresh clone** because §7 of the same document explains the hero was deliberately filtered out — check deleted, not loosened. **NO GEOMETRY MOVED, NO ARTWORK MOVED**; guards 0 fail / 0 warn at both levels throughout, textures byte-identical. |
| 2026-08-15 | **rev 25 — the bake frame is PARSED, the artwork is RE-BAKED for the first time since rev 11, and the hero photographs it.** Work item 2's own brief REFUTED: `_ZB_AUTH`'s claimed **76 mm at the tail is CONFIRMED exactly** (76.222 mm at `x = X_TAIL`) and **refuted as a defect** — the bake paints NOTHING aft of x = −1.40, so ink-weighted the missing `_aft()` re-space is **0.0023 mm**, not "larger than `DOOR_X0`" but ~7 500× smaller. Two controls isolate it (re-space 75.540, dropped knots 20.925). **The real `_ZB_AUTH` defect was never named — five DROPPED KNOTS**, worst at **+2.085 on the NOSE**, 19.477 mm peak over **3.53 %** of the ink. **`DOOR_X0` dominates and is worse than rev 23 recorded**: `DOOR_REAR_DX = 17.250 mm`, and the uncomputed consequence is **`DOOR_W` 1.935 % too wide** — it divides every u of the door art, displacing **82.5 % of door ink > 2 mm**, ink-weighted **6.290 mm**, with **3 411 px past the true rear shut line** (1.44× the whole B-pillar). **THE CONTROL FAILED AND THAT WAS THE FINDING**: re-baking UNCHANGED does not reproduce the committed art (**4.029 % / 4.261 %**, max Δ 255). Determinism was checked BEFORE interpreting it (two processes, identical md5), then a bisect holding the tree at rev 24 and swapping in ONLY pre-rev-23 `folk_gen.py` reproduced the committed files **BYTE-IDENTICALLY** — **the model was wearing artwork fourteen revisions old**, and rev 23's "nothing in the current build changed" is true of the BUILD while leaving a 4 % divergence from its own corrected source (§10.68). Fixed **structurally**, the work rev 23 declined to do blind: a deliberately tiny `_ceval` reads `t1_shell`'s constant GRAPH (`DOOR_GAP`'s expressions, `BAYS`' comprehension, `B_PILLAR`'s environ default) and `t1_core`'s `ZB` knots, so `DOOR_X0` is EXPRESSED IN TERMS OF `BAYS[0][1]` and `T1_BPILLAR` moves the ART frame with the geometry; three more re-typed literals removed, **all three still AGREEING — exposure, not damage**. **Falsified in four arms, and the fourth cross-confirms from an unrelated route: the B-pillar width reproducing the retired `DOOR_X0 = 0.9084` is −0.005250 m, against §10.62's independently derived −0.0053 for the broken GEOMETRY — 0.050 mm apart.** The door art had been drawn to a door that could not open. `_DOOR_TOP_AUTH` **deliberately NOT parsed**: "within 1 mm" was written into a comment before being watched print and the print refuted it at **4.2 mm**, so it is HELD at 1.8140, `DOOR_H` bit-identical, discrepancy carried forward not absorbed. After the bake: door ink past the shut line **3 411 → 0**, sill error **76.222 → 0.000000 mm**, §10.10 targets held or improved (flank density rms 3.59→3.58 and 3.98→3.96; zone R1 −0.44→+0.29, R2 +0.58→−0.14) — **and door gold 29.09 → 28.90 against 29.08 went the WRONG way, stated rather than hidden**, inside the 28.96–29.19 spread watched printing. **HERO at 4800×3200, 20 strips, worst seam z = 1.91**, `post.py` once, `bloom=0.00`, `backdrop=headroom` — the first frame ever to photograph artwork matching the model's own source; a strip killed by the shell limit was adjudicated by the **seam check** rather than by its file opening cleanly. **`_RETIRED_VALUES` 5 → 15 rows (§10.69)**: of a subagent's "~12", **nine confirmed against three things each and four refuted or mislocated**; guard fired at all 12 predicted lines with **no false positives**, then 0, falsified in four arms with the §0.2 bullet count **watched print at 29/29**. Two are structural — **§1.1's rows defeat the guard BY RE-EXPRESSION** (the retired taper survives as edge pairs, plus the 100 mm origin shift), now stated as the guard's real ceiling; and **§9 row 10 published the INVERSE of the guard that runs**, contradicting §2 inside the same frozen front matter and failing every current build as written. **NO GEOMETRY MOVED**; guards 0 fail / 0 warn at both levels throughout. |

| 2026-08-15 | **rev 27 — §10.71 measured: the founding patch STRADDLED, and against `COUNTERTAN` there is no coverage at all (§10.76).** The two source patches for `W_DUST_FAC_UP` had **no coordinates anywhere in the repo**; both recovered forensically by searching `ref_rear34.jpg` for the box whose middle-80 %-of-L\* median **is** the recorded triple — flank u 914–983 v 298–337, trimmed n **2153**, err **0.0**, exact and unique; top u 556–656 v 397–424, trimmed n **2160**, err **0.0**, exact but NOT unique. **Box-independent result:** the counter top is a diagonal band 15–25 px deep and the largest clean axis-aligned rectangle on it is **1060–1512 px** across a swept gate, against the **2700 px** the patch needs — so it straddled whichever box was used (66–82 % tan, 8–19 % cream, 6–9 % brass, 2–4 % a tin can). **TWO OF MY OWN HYPOTHESES REFUTED BY MY OWN CONTROLS:** the solve did **not** consume a stale `CREAM` — the comment's "this file's CREAM (0.9676, 0.7784, 0.4976)" is the **von-Kries gain itself**, reproduced to 4.7e-5, a mislabel not a numerical error; and the straddle is **not** the explanation — on a band-following clean sample with gate and erosion **swept** (12 arms) the disagreement gets **worse**, (−0.295,−0.320,−1.674) → (−0.82,−0.56,−2.19). **The live assert's three-channel agreement is a TAUTOLOGY** (spread 5.2e-05) because `W_DUST_COL_UP` was solved collinear — it is the solve restated. **The real statement: `_UP_MEASURED` lies OUTSIDE the segment [`COUNTERTAN`, `W_DUST_COL_UP`] in all three channels — no coverage error, because there is no coverage.** E-free: observed top/flank **(1.056,0.884,0.803)** vs dusty `COUNTERTAN`'s **(0.881,0.681,0.461)**, B out by 74 %. **NOT DECIDED, deliberately:** the de-illuminated top is **proportional to `CREAM`**, so this frame cannot separate the two, and the pair is the up-facing/vertical mismatch **§10.60 ruled INADMISSIBLE**. **Nothing tuned; `COUNTERTAN`, `CREAM` and `W_DUST_FAC_UP` all UNCHANGED.** Armed instead: a **LABELLED regression catcher** on the three-channel residual, baseline (−0.066877, −0.100324, −0.159974) — *has not moved*, **not** *is right*; do not tighten it. **The guard was wrong before it was right** — its first cut asserted the **max**, which lives in B, so an R-channel move left it silent; **cause fixed, band not widened**. Falsified in **six arms**. Guards **0 fail / 0 warn at BOTH levels**; **no geometry and no artwork moved.** |
| 2026-08-15 | **rev 27 — the F90 question ANSWERED (§10.77).** `probe_ctan_pedestal.py:170`'s UNVERIFIED worry — that `Specular IOR Level = 0` leaves **F90 = 1**, making `T1_CTAN_SP=0` only a partial specular ablation and part of the surviving 6.6/6.6/8.5 % pedestal specular — is **REFUTED BY MEASUREMENT**. New read-only `probe_f90.py` builds a purpose-made minimal scene (one plane, live `COUNTERTAN`, one light, ortho camera) so it cannot be contaminated by §10.65's occluders or stacked rigs, and renders four arms at normal and at **83° grazing**. **SP0 == TRUE-OFF (spec 0 AND ior 1) == bare DIFFUSE to six decimal places at BOTH angles**; the whole specular is 15.834 % of the true-off arm at grazing and the fraction `T1_CTAN_SP=0` fails to remove is **0.00 %**. **rev 26's arm 4 was COMPLETE and the residual pedestal is NOT specular** — one hypothesis removed from §10.70's never-ablated list; `T1_WORLD`, `T1_CYCALB`, `T1_GAL_LUM` and the scene→top bounce remain live. **THE CONTROL WAS THE DEFECT AGAIN, third time this session:** the first positive control asserted *shipped > diffuse* and FAILED at (0.990,1.025,1.158) because the Principled BSDF **conserves energy** — the specular takes from the diffuse lobe. Premise wrong, finding intact; replaced by *differs at grazing* (15.83 %) and *differs MORE at grazing than normal* (15.83 vs 2.02 %, **7.9×**), which is what shows the rig can see a grazing lobe. Null control 0.000 %. **Nothing tuned; no geometry and no artwork moved.** |
| 2026-08-15 | **rev 24 — `solve_ctan` was measuring the whole scene, and the guard that was supposed to be self-arming never was.** **Item 1 (§10.65):** the occlusion hypothesis, carried four revisions unrun, is **CONFIRMED and quantified** by a new read-only object-index probe — chosen over a visibility flag by §10.56's own rule. **33.06 % of the eroded TOP mask and 57.31 % of the FASCIA mask are foreign surfaces**; the largest occluder is **`gal_warmer`**, never previously named; **`counter_top` is 21.76 % of the fascia mask** and **97.84 % of the top mask lies inside it**, so the solve divided a region by a **superset of itself**. Null control **IoU 1.0000 / 0 disagreeing px**, positive control names the occluders. Re-measuring **both albedo arms** through the clean mask takes the pedestal **68.5/68.0/72.1 % → 60.8/58.2/59.5 %** and raises the albedo sensitivity **k by 40 % in all three channels** — that is what "secant gain 0.33–0.49" was really reporting, and the residual **flips sign in all three channels**. **The arithmetic correction was NOT reported**: it assumes occluders are albedo-invariant and they sit on the top catching its bounce; measurement, not inference. **A ~59 % pedestal SURVIVES and is still UNIDENTIFIED; `COUNTERTAN` UNCHANGED, fifth revision.** Two instrument defects found by controls, both mine: **`ST.lighting()` STACKS** (8/16/24 lights — every absolute figure in §10.56 is a **3-rig** number) and exposure must go through the environment (first run **70.54 % clipped**, radiance shares collapsing onto pixel shares). **Item 3 (§10.66):** rev 23's `STEP_M` rename **broke `folk_gen.composition()`** — `mm` had ZERO Store sites and ONE Load site, so the census a re-bake depends on raised `NameError` on every call. §10.63 verified that rename **by reading**; nobody ran it. Repaired value-preserving (53.2645 mm² both ways). **Item 2 (§10.67) — THE BRIEF IS REFUTED.** §0.2's guard is **not self-arming**: it compares **material datablock names**, and of ~100 §10 retirements exactly **one** was ever a material. **The false claim was inside the guard's own comment**, which is why the brief said it. New **`_retired_value_drift()`** FAILs on a retired literal republished unstruck in the FROZEN front matter — **it fired on its first run and caught three defects §10.64 missed**, all in FROZEN sections: §1.1's bay taper, §1.1's retired aperture band, and §3's retired `RED` with grade **M**. Plus `SPEC.md:2701`, the retired rake still deriving a consequence **forty lines below the table rev 23 struck**, under a heading reading "OPEN, unresolved" that §10.29 had closed. **The guard was wrong twice before it was right and both are recorded** — its first cut swept the change log (**4 of 8 FAILs were its own false positives**, because §10.11–10.33 are interleaved with the front matter) and a sub-heading reset its exemption so it found `:2701` **by accident**. **§0.2b added, bullets 16 → 29 — and adding it SILENTLY DEFEATED the drift guard**, whose substring split matched `### 0.2b`, sending it back to reading 16 while the section held 29. Caught by watching the count print; parse now line-anchored. Falsified in four arms. Guards **0 fail / 0 warn at BOTH levels**; **no geometry moved this revision.** |
| 2026-08-15 | **rev 23 — item 4 ARMED, and the B-pillar had NEGATIVE width.** §10.61's brief said "expect it to FAIL; fix the geometry". *A brief is a probe too*: a read-only anatomy probe asked which member of each pair is at fault, how deep the penetration is, and which flank it is on, and **all three change the answer** (§10.62). The six crossings are **three defects**, and **arc length overstates them by up to 23×** — `gap_door × bay0` reports 118.8 mm of arc for a **5.2 mm** overlap. **SHOW flank 130.6 mm; OFF flank 934.6 mm = 87.7 %.** The arch assert's rationale (a shut line crossing an arch lip collapsed the shell 205562 v → 12 v) **does not transfer and was not inherited** — all six crossings were live at SUB=2 with **zero non-manifold edges**. The invariant armed instead is TOPOLOGICAL and needs no photograph, scale or datum: *an aperture cannot extend past the boundary of the panel it is cut in.* **Two show-flank defects fixed, geometry not threshold**: the cab door's rear shut line sat **5.2 mm INSIDE bay 0**, so bay 0 straddled the door's own boundary and the door could not open — the door moved (bay edges are locked; the door's rear x had **no provenance anywhere in the repo**) with `DOOR_REAR_DX` **expressed in terms of `BAYS[0][1]`**, never a bare number; and the vent wing broke the door's top edge by **20.7 mm** — the owner confirmed from `ref_workshop.jpg` that the glass **is** divided into a vent plus a main pane but **could not** resolve whether its top reaches the top rail, so the legible door corner was left alone and the vent dropped. **`B_PILLAR` and `VENT_TOP_DROP` are AUTHORED, not measured, and both true values are OPEN.** Crossings **6 → 2**, show flank **130.6 → 0.0 mm**. **FALSIFIED FOUR WAYS** through levers defaulting to proven no-ops; the arm reproducing rev 22's geometry lands within **1–2 mm** of its 11.8 / 118.8. **My own negative control failed first and the failure was MINE** — "an outline is not inside itself" is ill-posed, every sample lies ON the boundary. **The OFF flank is NOT armed at zero, and that is the result**: SPEC's own table grades that flank **"E (never photographed)"**, its two colliding features are BOTH E and contradict each other, and shown the sightlines with every box printed the owner answered **"cannot tell from this crop"** — so it is a **LABELLED regression catcher** at a watched baseline (**804.9 mm, ±10 mm**), meaning "it has not moved", NOT "it is right". `CARGO_GAP` densified **28 → 154** samples (straight runs **8 → 134**) with **signed area asserted equal** as a control. Guards **0 fail / 0 warn at both levels**, non-manifold **0**; **roof-hole vertex count re-baselined 68052 → 68564 / 252123 → 252749**, flagged not hidden. |
| 2026-08-15 | **rev 23 — the bake frame was built on four retired numbers, and four retired values were still published as "locked".** `folk_gen.py` re-typed `X_TAIL` (**235 mm stale**), `RAKE_DZDX` (**15.25 mm/m**), `RAKE_Z0` and `Z_BELT0` (**11.4 mm** each) — the dead-`RIM_R` family again, under §10.10's hard bar on artwork replication (§10.63). Now **parsed with `ast`** in rev 14's `SCR` pattern, **raising rather than falling back**, with `X_TAIL` reconstructed from its definition because it is derived and not a literal. The banned flat px/m at `:1884` is gone — and **it was harmless where it stood**, setting a sampling interval rather than converting a position, which is stated precisely rather than claimed as a bigger fix than it was. **NOT re-baked**: `build.py` never calls `folk_gen`, the textures are committed artefacts, and a re-bake is a measured operation under §10.10 — **carried forward that the committed artwork was baked in the stale frame**, along with `DOOR_X0`, now 17.3 mm stale and named rather than quietly fixed. **SPEC hygiene (§10.64):** §10.3 published the RETIRED red **and** `W_ART = 0.30` (**3.3× off the live value for thirteen revisions**) as "locked"; §10.9 published the RETIRED rake and the `Z_BELT0`/`V_APEX0` derived from it; and `SPEC.md:1983` used **N1**, the crop the owner refuted, as an arm of route A's clipping control **nineteen lines after §10.57 dropped it** — conclusion unchanged, it stands on N2/N3. **Three CITATION defects found**: §10.61 corrects a "five crossings / 1209 mm" figure **§10.45's body never contained** (it is `HANDOFF_rev18.md:208`), §10.59 credits §10.48 with a withdrawal it never made, and §10.45 cites the rake lock to §10.9 **whose own table locks the retired value** — *a carried-forward figure is a claim too*, now extended to the citation. Also refuted from rev 23's own brief: §10.45–48 retire **no** §10.34 claim, and §10.29 carries **one** REF-wide correction, not two. |
| 2026-08-14 | **rev 20 — work item 1 refuted, and §10.52 repaired.** §10.52's two constants-only arch lines now MEASURE the mesh via `verify._arch_lip_z` and the row was FALSIFIED after repair on all three decline paths (§10.53). **The cream map's chroma gain must NOT be raised (§10.54):** the dC\* triple quoted as the shipped arm is the **ABLATION** arm's (shipped is 0.220/0.227/0.231, not 0.240/0.249/0.253 — eighth un-watched figure); switching the map on drives dC\* **down**, not flat; an alias hypothesis was built and refuted by its own no-op control; the lever is real and chroma-pure (`W_FADE_SAT` 0.88→0.40 gives 0.269/0.314/0.335 and dL\* does not move) — **but dC\* rms is an ABSOLUTE statistic and the base levels differ 5.5×** (render C\* **3.89** vs photograph **21.44**; L\* agrees to 2.9 %, which is why dL\* was correctly found close). Normalised, the render is ALREADY at or above the photograph at every scale. The BEAUTY arm is **100 % clipped** and has always reported zeros. **New rule: A TARGET IS A PROBE TOO — print the base level of any absolute statistic.** Live lead is the locked `CREAM` albedo, sat 0.038 / G>R against the bus's 0.255 / R>G, **not changed**, blocked on one owner reading (§10.55). |
| 2026-08-14 | **rev 20 — `COUNTERTAN`'s interreflection test, run at last (§10.56).** Five revisions on the list. **A ray-visibility flag is NOT an ablation** — killing every outgoing ray path from the top costs the fascia 1.8 %, while driving its albedo to near-black costs 9.0 %; in Cycles a ray that cannot see an object passes THROUGH it and hits what is behind, so the flag substitutes the background rather than removing the source. Taking the valid arm: interreflection is **real but secondary at 9.0 / 8.2 / 6.0 %**, and the dominant effect is that **~70 % of the counter top's rendered radiance does not come from `COUNTERTAN` at all** (a 96.6 % albedo cut moves it 29.6 %). Coat and spec were already excluded at 2.3–5.6 %; the prime remaining suspect is the **dust overlay** (`dust=1.4`, `W_DUST_COL_UP` base-independent by construction), named and **not yet measured** — it has no override to ablate. `COUNTERTAN` left unchanged for the third revision. |
| 2026-08-14 | **rev 17 — the cream target was measured through an open serving bay (§10.38).** `cream_rms.py`'s 8.890 % is the GALLEY INTERIOR seen through bay 3: its search band overlaps the guarded aperture band and its gate tests "pale", not "cream paint". Proven against two locked image lines. `ref_side.jpg` cannot supply a replacement — 1799 gated body-cream pixels, best 60×20 window **33.8 % pure** — and it is also the **worst frame in the set** at 2.32 bits/px / DC quantiser 4 against 9.28 and 8.87 at DC quantiser 1. **New rule: A CLASS GATE IS A PROBE TOO** — gate on geometry before colour. The codec-floor control was itself wrong by 4× (blur at σ then high-pass at σ does not leave zero); true codec contribution **0.31–0.66 %**, so the structure is real and only the surface was wrong. Re-based on `ref_rear34.jpg` by the owner's choice; character determined by four scale-free discriminators as **chalky sun-fade mottle** (corr(dL\*,dC\*) −0.486, anisotropy 0.918), which finally explains `W_ALBEDO`: **a scalar multiply on albedo cannot change chroma.** The mm axis is NOT established — three routes to px/m all failed and none was invented. Also: `audit.py`'s re-typed 4.290 (§10.39), `vw_bars`' false air-gap docstring and the V's short arms (§10.40), the hubcap ring at 0.093 ± 0.012 with the PSF that chose its frame (§10.41), a real matte with an identity claim that could not honestly be made (§10.42), `flank_compare.py`'s premise refuted and the +95 mm offset found to be **87 mm of missing tarnish in the render mask** (§10.43), and `H_ROOF` delegated but deliberately **not** changed (§10.44). |
| 2026-08-13 | **rev 13 — the rake falls to 17.75 mm/m and `optics-6` is refuted.** The two divergent lines are merged. The rake is re-derived a fourth way, hub-referenced and scale-free, and 33.0 is rejected at **4.5σ**; §10.9's rake-versus-arch-gap contradiction closes against the built value, and the arch-gap identity is demoted from estimator to bound. A **100 mm origin error** in `REF_MEASUREMENTS` surfaces independently in two dimensions — the bays sat 105 mm aft and §10.7's "99 mm tail" contained it. **The bays are equal at 0.5155 m**; §10.5's taper is perspective. **`optics-6` is refuted**: the catcher was never broken, the diagnosis was measured on a camera that cannot see the ground plane, and the contact profile matches the photograph within ~1σ at every station. **`gal_ceiling` deleted** and the galley lit through the real hole — every bay mean moved toward the photograph and the two flat bays gained real contrast. Bulb pitch 4.7× too coarse, tail lamp amber not ruby. The cream is measured **too clean, not too weathered**. The roof guard is strengthened with a named `DOME_DEFICIT` rather than widened. |
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

### 10.76  rev 27 — §10.71 settled as far as the admissible set allows: the founding patch STRADDLED, and against `COUNTERTAN` there is no coverage at all

§10.71 named the defect and said **do not repair it blind**. rev 27 measured it.
`COUNTERTAN`, `COUNTERCREAM`, `CREAM`, `W_DUST_FAC_UP` and `_UP_MEASURED` are
all **UNCHANGED**. Instrument: `probe_dust_anchor.py`, READ-ONLY, which
**ASSERTS** every statement below rather than claiming it in prose, parses
`t1_mats`' constants rather than re-typing them, and **raises** if a parse
fails.

**C1 — THE CHAIN REPRODUCES EXACTLY.** `lin(202,172,127) / E` gives
**(0.6104, 0.52998, 0.42647)** against the written `_UP_MEASURED =
(0.6104, 0.5300, 0.4265)` — **3.1e-5**. So the constant is exactly what its
comment says it is, and the arithmetic of rev 12's solve was right.

**C2 — THE COMMENT MISLABELS THE GAIN, and my first hypothesis died here.**
`t1_mats.py`'s "this file's CREAM (0.9676, 0.7784, 0.4976)" is **not `CREAM`** —
live `CREAM = (0.6172, 0.6308, 0.5776)`. That triple is the **von-Kries gain
itself**: `lin(203,186,146)/CREAM` reproduces it to **4.7e-5**. I opened
believing the solve had consumed a stale `CREAM`; **the arithmetic refuted
that**. A labelling defect, not a numerical one. Corrected in place.

**C3 — THE LIVE ASSERT'S THREE-CHANNEL AGREEMENT IS A TAUTOLOGY.**
`W_DUST_COL_UP` was solved **collinear** with `COUNTERCREAM` and `_UP_MEASURED`
(the L\* degeneracy-closing step in the same comment block), so the coverage
solve **must** agree in all three channels whatever the numbers are — measured
spread **5.2e-05**. §10.71 reads that agreement as evidence the cream anchor is
right. **It is the solve restated, and it is evidence of nothing.**

**C4 — THE FOUNDING PATCH STRADDLED, AND THIS IS BOX-INDEPENDENT.** Neither
source patch has coordinates anywhere in the repo. Both were recovered by
searching `ref_rear34.jpg` for the box whose middle-80 %-of-L\* median **is** the
recorded triple — a convention itself recovered, not assumed, because it is what
takes 2691 px to exactly **2153** and 2700 px to exactly **2160**, the two counts
the comment records.

| patch | recovered box | trimmed n | median | err |
|---|---|---|---|---|
| cream flank rear quarter | u 914–983, v 298–337 (69×39) | **2153** | (203,186,146) | **0.0** |
| counter top | u 556–656, v 397–424 (100×27) | **2160** | (202,172,127) | **0.0** |

The flank box is **exact and unique**. The top box is exact but **NOT unique** —
several boxes reproduce it, so **which box rev 12 used is NOT claimed**. What is
claimed needs no box: the counter top is a **diagonal band 15–25 px deep**, and
the largest axis-aligned rectangle lying entirely on it is **1060–1512 px** across
a **swept** class gate. The patch needs **2700**. **So it straddled, whichever box
it was** — every err-0.0 candidate measures 66–82 % tan, 8–19 % cream, 6–9 % brass
nosing and 2–4 % of a tin can standing on the counter. **Sixteenth instance** of
check-what-the-probe-can-see, and like §10.60 this one is **SPEC's own founding
measurement**, drawn by nobody but this project.

**C5 — AND THE STRADDLE IS NOT THE EXPLANATION. MY SECOND HYPOTHESIS DIED
HERE.** On a **band-following** clean-tan sample, class gate and edge erosion
**SWEPT not picked** (12 arms, n = 2377–3400), the median goes to **(208,176,132)**
— *brighter* — and the disagreement gets **WORSE**: coverage against `COUNTERTAN`
moves from **(−0.295, −0.320, −1.674)** to **(−0.82, −0.56, −2.19)**. Cleaning the
probe moves it **away** from the constant.

**THE FINDING, and it is stronger than §10.71 states.** §10.71 reports "max err
0.1600, fails by 80× its tolerance", which reads as a mis-tuned coverage. It is
not. **`_UP_MEASURED` lies OUTSIDE the segment [`COUNTERTAN`, `W_DUST_COL_UP`] in
all three channels.** Against `COUNTERTAN` there is no coverage *error* because
**there is no coverage** — solving anyway gives three **negative** values
disagreeing by **5.7×**. The dust is darker than `COUNTERTAN` everywhere;
`_UP_MEASURED` is brighter everywhere (+4 % R, +7.5 % G, **+39 % B**).

**E-FREE STATEMENT, no de-illumination and therefore no `CREAM` dependence.**
Observed top/flank in the same frame = **(1.056, 0.884, 0.803)**. A dusty
`COUNTERCREAM` top predicts (0.989, 0.840, 0.738); a dusty `COUNTERTAN` top
predicts **(0.881, 0.681, 0.461)** — B out by **74 %**.

**WHAT IS DELIBERATELY NOT DECIDED, and why the item CANNOT be closed on the
admissible set.**
1. **The de-illuminated top is PROPORTIONAL to `CREAM`, channel-wise** —
   `de_top = CREAM × (obs_top/obs_flank)`. For the top to be dusty `COUNTERTAN`,
   `CREAM` would have to be about **sRGB(190,185,156), hue 51° / sat 0.18**, which
   sits **between** the locked (206,208,200) 75°/0.038 and rev 20's read of the
   bus's own cream (216,200,161) 41.7°/0.255. **This frame cannot separate
   `COUNTERTAN` from `CREAM`,** and `CREAM` is the project's largest open
   constant with five routes already refuted (§10.57–58).
2. **The pair is up-facing top vs vertical flank** — precisely the orientation
   mismatch **§10.60 ruled INADMISSIBLE** when it struck `COUNTERTAN`'s cab-roof
   arm at 22 % bluer. **UNTESTED here**, because no same-class pair with a locked
   albedo ratio and differing orientations exists in `ref_rear34.jpg`.

So `W_DUST_FAC_UP = 0.7313` is **unsupported for the surface it is applied to,
and cannot be re-solved from this pair.** Nothing was tuned.

**WHAT WAS ARMED INSTEAD.** `t1_mats.py` gains a **LABELLED REGRESSION CATCHER**
on the three-channel `COUNTERTAN`-vs-`_UP_MEASURED` residual, baseline
**(−0.066877, −0.100324, −0.159974)**, plus a sign assert stating the finding
itself (all three negative). It says *this disagreement has not moved*; it does
**NOT** say the disagreement is acceptable, and **driving it to zero would mean
inventing an albedo — do not tighten it and do not tune to it.** This is the
`H_ROOF_REGRESSION` / off-flank pattern. The coupling was previously invisible:
the live assert would have kept passing however far `COUNTERTAN` moved.

**THE GUARD WAS WRONG BEFORE IT WAS RIGHT, AND FALSIFICATION IS WHAT CAUGHT IT.**
rev 27's first cut asserted the **max** over channels. The max lives in **B**, so
displacing `COUNTERTAN`'s **R** by +0.020 left the guard **silent** — a guard that
is right for the wrong reason is not a guard (§10.67). **The CAUSE was fixed, the
band was NOT widened**, and the same defect was then found and fixed in the probe.
**FALSIFIED IN SIX ARMS**: clean tree **0 fail**; `COUNTERTAN` **R**, **G** and
**B** each +0.020 → **FAIL naming the moved channel**; `W_DUST_FAC_UP` default
0.7313 → 0.6800 → **FAIL**; `T1_CTAN` set → **correctly SKIPPED**, so the A/B
lever survives. Guards **0 fail / 0 warn at BOTH levels** before and after.

### 10.77  rev 27 — the F90 question ANSWERED: `T1_CTAN_SP=0` **is** a complete specular ablation, so rev 26's arm 4 stands

`probe_ctan_pedestal.py:170` left this **UNVERIFIED** and told the next
revision to test it before use: *"the counter camera sits ~83° off the top's
normal … if 'Specular IOR Level' = 0 leaves F90 = 1, `T1_CTAN_SP=0` is not a
complete specular ablation."* If that had held, part of the surviving
**6.6 / 6.6 / 8.5 %** pedestal would have been specular and §10.70's
never-ablated list would have been chasing the wrong thing.

**MEASURED, not argued.** `probe_f90.py`, READ-ONLY, builds a **purpose-made
minimal scene** — one plane carrying a material from `t1_mats.simple()` with the
live `COUNTERTAN`, one area light, an ortho camera — so it cannot be
contaminated by §10.65's occluders or §10.65's stacked rigs. Four arms at
**normal** and at **83° grazing**:

| arm | `spec` | `IOR` | grazing radiance |
|---|---|---|---|
| SHIPPED | 0.32 | 1.45 | (0.416698, 0.362301, 0.254087) |
| **SP0** — what `T1_CTAN_SP=0` does | 0.00 | 1.45 | (0.420787, 0.353404, 0.219354) |
| TRUE-OFF — a real dielectric removal | 0.00 | **1.00** | (0.420787, 0.353404, 0.219354) |
| DIFFUSE — bare Diffuse BSDF | — | — | (0.420787, 0.353404, 0.219354) |

**SP0 == TRUE-OFF == DIFFUSE to six decimal places, at BOTH angles.** The whole
specular is **15.834 %** of the true-off arm at grazing; the fraction
`T1_CTAN_SP=0` **fails** to remove is **0.00 %**.

**VERDICT: the concern is REFUTED.** In Blender 4.5.3, `Specular IOR Level = 0`
removes the dielectric lobe at **all angles, F90 included** — it does not leave
a grazing lobe behind. **rev 26's arm 4 was a COMPLETE specular ablation and the
surviving 6.6 / 6.6 / 8.5 % pedestal is NOT specular.** One hypothesis removed
from §10.70's never-ablated list; `T1_WORLD`, `T1_CYCALB`, `T1_GAL_LUM` and the
scene→top bounce are untouched and remain the live candidates.

**AND THE CONTROL WAS THE DEFECT AGAIN — third time this session.** rev 27's
first positive control asserted *shipped **>** diffuse at grazing* — "adding a
specular adds energy". It **FAILED**, at (0.990, 1.025, 1.158): the Principled
BSDF **conserves energy**, so the specular layer takes from the diffuse lobe and
R came out 0.99×. **The control's premise was wrong, not the finding.** Replaced
with the two controls that are actually well-posed — shipped must *differ* from
diffuse at grazing (**15.83 %**), and must differ **more** at grazing than at
normal (**15.83 % vs 2.02 %, 7.9×**), which is what demonstrates the rig can see
a grazing lobe at all. Both pass. Null control: the shipped arm rendered twice
agrees to **0.000 %**, so the noise floor is zero against a 15.8-point effect.

**NOT CLAIMED**, and printed by the probe so it cannot be misread: nothing about
the **coat** (`T1_CTAN_CT` is a separate lever and including it would confound
the one question asked); that the residual pedestal is explained; and that this
generalises past **Blender 4.5.3**, which the probe prints with its own version.

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
| `RED` ~~locked~~ **RETIRED by §10.12** | ~~(0.5520, 0.1441, 0.0176)~~ | ~~(196, 106, 36)~~ | ~~26.3°~~ | 0.816 |
| `RED` **LOCKED (live, §10.12)** | **(0.5520, 0.0294, 0.0176)** | **(196, 49, 36)** | **5.0°** | **0.816** |
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
dragging the measured flank from sat 0.816 to **0.27**. ~~Locked: opacity
ceiling `W_ART = 0.30`.~~ **RETIRED in rev 10** — the 0.30 ceiling made the
measured ×2.048 gold-to-red contrast arithmetically unreachable and was the
cause of the owner's "far too faint and sparse". Live value is
`t1_mats.W_ART = 1.00` (`T1_W_ART`). Marked here in rev 23; it had sat in this
table as "locked" at 3.3× off the shipped value for thirteen revisions.

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
> **EVERY VALUE IN THIS TABLE IS RETIRED — §10.29 rejected the rake at 4.5 σ.**
> Marked in rev 23; it had read "Locked:" for ten revisions, 1600 lines from the
> section that retired it, with no link between them. Follow §10.29, not this.

| constant | ~~rev-8 value, RETIRED~~ | live value (`t1_core`) |
|---|---|---|
| `RAKE_Z0` | ~~**0.0365** m~~ | **0.047925** (§10.29 re-anchored) |
| `RAKE_DZDX` | ~~**0.0330** m/m ± 0.0040, 1.89°~~ | **0.017750** m/m, 1.02° |
| `X_DROP_REF` | ~~+0.8636~~ | **DERIVED** (0.96197), holds `RIDE_DROP` at 0.0650 |

`drop(x) = RAKE_Z0 + RAKE_DZDX·x`. **Shear, never rotation** — every reference
number is a height-versus-X and a 1.9° rotation also shifts x by 63 mm at roof
level. `RIDE_DROP` survives ONLY as the value at `X_DROP_REF`; it is not a frame
conversion. Use `t1_core.rake_drop(x)`.

Consequences, all implemented:

- **`Z_BELT` is a line.** `t1_mats.z_belt(x) = Z_BELT0 − RAKE_DZDX·x`, with
  ~~`Z_BELT0 = 1.2355` and `V_APEX0 = 0.3685`~~ — **BOTH RETIRED with the rake
  above (rev 23 marking).** They were literals derived from `RAKE_Z0 = 0.0365`;
  §10.29 made them DERIVED and they now compute to **1.224075 / 0.357075**, so
  the figures below are ~11.4 mm stale. (above ground at x = 0). The rake is
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

### ~~OPEN, unresolved~~ CLOSED by §10.29: rake versus the arch gap

> **rev 24, §10.67.** This subsection is **CLOSED**, and everything below it is
> **RETIRED**. §10.29 closed the contradiction against the built value: 0.0330
> was rejected at **4.5 σ** and the rake is **0.017750**, and §10.29 re-measured
> the rear gap to **41.0 ± 3.5 mm**, not the ≈30 mm quoted below. rev 23 struck
> this section's *table* and inserted a blockquote saying every value in it is
> retired — and missed this arithmetic **forty lines below**, which then went on
> deriving a 79 mm consequence from the retired number inside a heading still
> reading "OPEN, unresolved". Kept, struck, rather than deleted, because the
> reasoning is the record of how the contradiction was found.
>
> **The retired-VALUE guard could not catch this**: by construction it does not
> scan inside a §10 body (`verify._retired_value_drift`). Found by an
> adversarial read, verified by hand.

~~`RAKE_DZDX × wheelbase = 0.0330 × 2.400 = 79 mm`. So the front arch gap must be
79 mm **less** than the rear. But the rear gap measures **≈30 mm** off
`ref_side.jpg` (arch lip y 524 ± 2 against a tyre top computed at 532.3 from a
rim circle fit at 211.5 px/m) and §2 locks it at 41 mm. Either way
`front = rear − 79 mm` is **negative** — the tyre inside the bodywork. Two
measurements off the real vehicle contradict each other.

Held: the arches follow their own wheel (`t1_shell.arch_z(x)`), which keeps both
measured numbers and produces no impossible geometry. Resolving it needs a
photograph with an **unoccluded front wheel** — in `ref_side.jpg` a man stands
directly in front of it, and every attempt to measure the front arch locked onto
his red shirt.~~

**What actually holds (rev 24):** at the live rake **0.017750** the term is
`0.017750 × 2.400 = 42.6 mm`, not 79 mm, and the geometry is not impossible.
The mesh measures **rear arch → tyre gap 39.7 mm** with the untouched circular
**front arch at 40.7 mm** as a positive control, both identical at SUB=1 and
SUB=2 and both printed by `verify` every run. The "unoccluded front wheel"
photograph is still the only route to an independent front-arch number, and
the lamppost warning of §10.29 applies to any attempt: `ref_side.jpg` columns
62–79 have produced four confident wrong numbers about the front of this
vehicle.

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


### 10.34 rev 16 — THE ROOF SECTION, and why the 63 mm drop was rejected

`LOFT_GROUND_rev15` §1.3 proposed closing the roof by dropping `ZT_ALL` by
**63 mm** at the rear axle, on a hub-referenced measurement of the drip rail.
Applying it breaks two things that are independently locked, so it was measured
a third way before anything was changed — SPEC's own standing rule.

**What it breaks.** The model's drip rail sits 65–69 mm above the serving-
aperture top (`band 1.372–1.775`, guarded). A 63 mm drop leaves **2 mm** of
sheet metal between the drip rail and the top of the bays. Separately, the
windscreen is anchored at absolute `P_TOP = (1.8340, 0, 1.7745)` in `t1_shell`;
dropping `ZT_ALL` puts the shell's top edge 35–57 mm **below** the screen's own
top at that station, so the windscreen cutter would open a notch to the sky.

**THE THIRD METHOD — datum-free.** Two features at the same depth on the same
flank of `ref_side.jpg`, differenced at the same column, so no ground line, no
origin and no absolute scale enters:

| | measured | built | delta |
|---|---|---|---|
| drip-rail groove → **bay 3** aperture top | 6.16 px, 83 cols, sd 0.19 → **28.3 mm** | 68.6 | |
| → **bay 2** | 6.05 px, 83 cols, sd 0.19 → **27.4 mm** | 68.6 | |
| → **bay 1** | 6.13 px, 62 cols, sd 0.21 → **27.5 mm** | 68.6 | |
| **adopted** | **27.7 ± 0.5 mm** | 68.6 | **−41 mm** |

228 columns across three bays agreeing to 0.2 px. A 2 % error in `k_t` moves
27.7 mm by 0.6 mm, so this is effectively scale-free.

**And the aperture band is NOT the error, which is what makes the split
unambiguous.** Referenced to the locked belt line (two-tone break, fitted over
its clean span u[635,733], rms 0.102 px):

```
  belt -> aperture top    500.9 mm measured   503.0 built   -2.1 mm
  belt -> drip rail       529.7 mm measured   568.0 built   -38.3 mm
```

**Why the hub route said 63.** Not a scale error — `k_t = 215.5 px/m` is
*validated* by belt→aperture agreeing to 0.4 %. It is a **datum** error: the
hub-referenced chain puts the locked belt at 1.2145 AG against the model's
1.2436, **29 mm low**. That is the common-mode signature §10.11 bans the ground
line for, and `LOFT_GROUND` §0.4 half-caught it ("the datum is ~6 px low").

**Two figures in `LOFT_GROUND` §1.2 that could not be reproduced, and one that
was reproduced exactly.**

* Drip rail — **reproduced**. Independent fit `v = −0.04409·u + 332.301`, n=83
  over u[746,874], **rms 0.067 px**, giving v = 299.26 at the rear axle against
  their 299.24 ± 0.6 (their slope −0.0436, rms 0.06–0.12).
* Roof silhouette — **not reproduced.** Scanning the top edge at 5-px steps it
  is flat at **252.1–253.6 over u[755,815]** and only then rolls down aft. Their
  "fixed skin 257.2" is 4.7 px below that; their "proud strip 253.21" is, on
  this scan, the roof itself. The proud-strip/coaming reading is therefore
  **withdrawn**, not merely re-valued.
* `D` survives anyway. Drip rail → roof top = 44.92 px = **0.209 m** against
  their **0.2116 ± 0.035**. Agreement to 3 mm by a route sharing only `k_t`.

**APPLIED.** The defect is local to the roof/side junction, so it is spent on
the junction and not on the roof line:

```
  RT_ALL (roof)   0.054  -> 0.0949     roll start / drip-rail seat
  CR_ALL (roof)   0.032  -> 0.1179     transverse crown parameter
  D = RT + CR            -> 0.2128     LOFT_GROUND 0.2116 +- 0.035
  Yt                        0.7273     crown half-width
  R = Yt^2/(2 CR)           2.24 m     QUOTE WITH ITS Yt OR NOT AT ALL
  ZT_ALL, RAKE_DZDX, P_TOP  UNTOUCHED
  DOME_DEFICIT    0.098  -> 0.000
```

`R = 2.45 ± 0.15` stays **refuted**: it requires D = 0.172, not 0.213. `R` here
is a re-expression of `D` and moves with `Yt`; **`D` is the finding.**

**Measured back off the built mesh:** drip-rail lip − aperture top =
**+27.0 mm** against the photograph's 27.7 ± 0.5.

**Consequence, reported not tuned.** The crown lands at **1.9835 AG**, +23 mm
against `SPEC H_ROOF = 1.960`, which trips the warn at its 20 mm threshold. The
uncertainty on `D` is ±35 mm (the depth systematic `LOFT_GROUND` §1.1 names), so
1.960 sits 0.7σ away — no real disagreement. `H_ROOF` was **NOT** changed to
clear the warn. Note for whoever does re-open it: REF §1 derived 1.960 from
`ground = 668.0`, the exact datum §10.11 bans, and the belt-anchored chain here
puts the crown at 1.981.

**A latent bug this exposed.** `t1_shell.roof_cutters` passed `zlo` as
`T.solid_prism`'s origin, but `solid_prism` extrudes ±depth/2 **about** its
origin (`t1_core._frame`). At the old `CR_ALL = 0.032` the crown was shallow
enough that the half-height prism still cleared the roof by 6 mm and the cut
worked by luck; at 0.1179 it stops 18 mm short and the aperture centre goes back
to sealed steel — caught by `verify` 11d2, which is the guard written for
exactly that. Fixed.


### 10.35 rev 16 — THE TAIL, re-spaced and not translated

**Measured dimensionlessly**, from the two hub columns and the tail silhouette
only. No origin, no metre scale, no ground line, nothing within 800 px of the
lamppost:

```
  rear overhang / wheelbase  =  (u_tail - u_rhub)/(u_rhub - u_fhub)
                             =  0.3412 +- 0.0015        ref_side.jpg
  built                      =  1.008 / 2.400 = 0.4200
```

Through the projective flank map of `LOFT_GROUND` §0 that is **0.773 ± 0.022 m**
against 1.008 built — **the tail is 235 ± 22 mm too long.** §10.7's "99 mm" is
**refuted at 10σ**; it subtracted two numbers in different origins.

**THIRD METHOD, and it is the one that made this safe to apply.** The 1-D
projective map was rebuilt here from `LOFT_GROUND` §0's own three constraints
(u at both hubs, and ρ from the two rim flange ODs — the same physical object at
two depths). Written out:

```
  X(u) = 641220.4 / (u + 11140) - 55.0322
    X(242.84) = +1.3000   X(749.38) = -1.1000     (both locked)
    rho = 1.0445                                   (measured 1.0445 +- 0.020)
    X(922.2)  = -1.8727                            the tail
```

The **same map**, applied to a feature pair that shares no datum with the tail,
puts the rear arch's aft foot at **X = −1.5615** against the **−1.560** that the
independently measured arch half-width predicts — **1.5 mm.** The forward foot
lands at −0.6500 / −0.6565 against −0.640.

**APPLIED AS A RE-SPACE.** `t1_core._aft(x)` carries every aft station and every
aft LUT knot by its own fraction f of the old overhang:

```
  f = (x - X_AXLE_R)/(-O_OLD)      X = X_AXLE_R - f * O_NEW
  O_OLD = 1.008   O_NEW = 0.773    X_TAIL  -2.108 -> -1.873
```

`ZB`, `ZT_ALL`, `RT_ALL`, `CR_ALL`, `WX`, `RB_ALL` and `STATIONS` all go through
it, so `LOFT_GROUND` §3.3's tabulated f values are reproduced by construction
rather than re-typed. **Re-typing 21 metre values against an origin that has
already moved once is precisely the mistake §10.7 is made of.**

**Everything anchored to the old tail skin had to move with it**, and this is
the half of the job that is easy to miss: the tail lamps, `plate_1963`,
`englid_handle`, the fuel filler flap, the louvre block, the counter (as a
preserved 0.315 m **overhang**, not an absolute station), the counter brackets,
the drip-rail sweep, the bulb string's aft end, the galley bottles on the
counter's tail run, the rear-window cutter and glass, and the engine-lid gap.
Left alone, the tail lamps became the rear-most objects on the vehicle by
258 mm and `verify` row 1 would have kept **PASSING on a phantom** — the same
failure shape as the `counter_top` length row the rev-12 audit found at
`audit.py:308`.

**`SPEC["L"]` IS NO LONGER THE FACTORY FIGURE.** 4.290 is the T1 catalogue
length; the measurement says the overhang is 235 mm shorter, and the standing
instruction on this project is never to correct this vehicle toward the VW
factory catalogue. It is now written as `4.290 − (O_OLD − O_NEW)` — an
expression, so re-measuring the overhang can never leave it stale. Row 1's
forward end is `X_NOSE`, which has **never** been measured (the lamppost at
`ref_side.jpg` cols 62–79 occludes it and has produced three confident wrong
numbers), so row 1 is a regression catcher and now says so. **A new verify row
guards the rear overhang itself**, which is the quantity that was observed —
a guard strengthened rather than widened.


### 10.36 rev 16 — THE END-CAP POLES, closed (§10.30b)

`t1_core.loft(cap_first/cap_last)` appended one n-gon per end; `build.py` runs
SUBSURF first, and Catmull–Clark turns an n-gon into n quads around a face point
of valence n. That face point was the pole.

**Replaced with a Coons quad grid whose border IS the boundary loop**, so no
vertex is added to the loop and the loft's own topology is untouched:

```
  n = NLOOP -> a = n//4, b = n//2 - a       (sides a/b/a/b, 2(a+b) = n)
  n = 110  -> 27 x 28, corners at 0, 27, 55, 82     NOT mirror-symmetric
  n = 112  -> 28 x 28, corners at 0, 28, 56, 84     mirror-symmetric
```

Interior points by bilinear Coons interpolation of the four border curves.

**THE NHALF DECISION WAS MADE ON A GUARD RESULT, NOT ON TIDINESS.** Both arms
were built at both subdivision levels:

| arm | SUB=1 | SUB=2 |
|---|---|---|
| NHALF 56, cap 27×28 | 0 fail | **1 FAIL** — `gap_englid` rejected, "zero-area faces 0 → 2", rolled back |
| **NHALF 57, cap 28×28** | **0 fail** | **0 fail** |

The engine-lid gap ring is symmetric about y = 0; on a cap grid that is not, its
two sides land differently on the grid and the exact solver returns two
degenerate slivers. **Moving the cutter in x does not fix it** — `T1_ENGLID_DX`
of 0.120, 0.158 and 0.200 all give exactly 2 zero-area faces, which is what
identifies it as an outline/grid coincidence rather than a tangency. `NHALF` is
therefore **57**, `NLOOP` **112**, selectable back to 56 with `T1_NHALF57=0`.

**MEASURED, with a negative control in the same frame.** Rear ortho elevation,
1200×800, 32 samples, high-pass σ = 8 px, red paint only, 3 px erosion:

| patch (x0,y0,x1,y1) | rev 15 | rev 16 |
|---|---|---|
| lower-LEFT corner (335,682,432,764) — the fan | **3.015** | **1.609**  (**−47 %**) |
| lower-RIGHT corner (784,682,878,764) — **NEGATIVE CONTROL**, no visible fan | 1.596 | 1.592  (−0.3 %) |

The residual 1.609 is within 1 % of the control's 1.592: the fan is gone to the
paint's own noise floor, and the control shows the metric did not simply shift.
**Do not compare these to rev 14's quoted 15.478** — that was a different render
and a different crop; this is an internally controlled A/B, not a continuation
of that number.

Topology, measured on the mesh: **max vertex valence 115 → 6**, vertices with
valence > 4 **53 → 14**, non-manifold edges **0** at both levels. The 1.4 mm
forward spike on the flat tail face is gone with it. `plate_1963` and
`englid_handle`, which were fitted to the **artefact** surface at −2.1066, are
re-anchored to `X_TAIL − 0.0004`.


### 10.37 rev 16 — THE REAR ARCH as a flat-crowned ogee

A circle is refuted overwhelmingly (`LOFT_GROUND` §2.2: circle rms **11.41 mm**,
superellipse **2.67 mm**). The **exponent is not used** — it is window-dependent
(3.50 at ±0.249 m, 4.28 at ±0.449 m), so 3.9 ± 0.2 is a property of a choice of
window, not of the arch. `t1_shell._ARCH_PROFILE` carries the assumption-free
normalised table instead, and keeps the trace's small left/right difference
(0.583 forward against 0.593 aft at |Δx/a| = 0.90) rather than averaging it away.

```
  ARCH_W_REAR   0.747 -> 0.920 m     measured 0.92 +- 0.03
                                     dimensionless: width / rim flange OD
                                     = 2.158 +- 0.027
  ARCH_R        0.3735   HELD        lip height above the hub measures
                                     0.3726 +- 0.0052 -- the RADIUS is right
  crown centre  rear axle            confirmed to 0.2 px ~ 1 mm, column-only
```

**The front arch is left circular, deliberately.** It has never been measured —
a man stands directly in front of it in `ref_side.jpg` and every attempt to
trace it has locked onto his red shirt — and widening it would bring the arch
lip to within 57 mm of the cab-door shut line's bottom run, which is the exact
geometry that collapsed the shell 205 562 v → 12 v for six revisions
(`t1_shell.py`'s import-time assert).

Noted and not yet acted on: with the arch at 0.92 m and the tail re-spaced, the
arch's aft foot is at x = −1.560 and the aft skin at −1.873 — **313 mm apart,
against 418 mm before**. `LOFT_GROUND` §3.3 predicted this gets worse, not
better, and it is the thing most likely to constrain a future tail change.

### 10.38 rev 17 — THE CREAM TARGET WAS MEASURED THROUGH AN OPEN SERVING BAY

`cream_rms.py`'s **8.890 %** — the number the whole "cream is 26× too uniform"
finding rests on — is the **galley interior seen through serving bay 3**. It is
not paint, and it never was.

`run()` scans `v 240–320, u 380–780` of `ref_side.jpg` for the best 100 %-class
window and lands on `u 592–742, v 319–345`. Against the two locked image lines —
rev 16's drip-rail fit `v = −0.04409u + 332.301` (rms 0.067 px, n = 83) and
§10.34's `27.7 ± 0.5 mm` drip-to-aperture — the **guarded** aperture band at
those columns is **v 305.6–399.0**. The patch is **entirely inside it**.

It scores 99.8 % "class purity" because the gate is `sat < 0.30 & lum > 0.20`,
which is not a test for cream paint. It is a test for *pale*, and a lit galley,
a cream jacket and a whitewashed wall all pass it. The scan cannot avoid the
band either: the search window's own v-range overlaps it from v 304 down, and
the galley is the most uniform pale thing in the frame, so it **wins**.

**NEW STANDING RULE, and it generalises past this file: A CLASS GATE IS A PROBE
TOO.** Gate on GEOMETRY — which surface of the vehicle — *before* gating on
colour. This file's own docstring already warned that a high-pass estimator
measures whatever edges you hand it; rev 15 fixed the FILL and left the SEARCH
BAND.

**`ref_side.jpg` cannot supply a replacement.** Tight gate — `sat < 0.16`,
`lum > 0.45`, unclipped, below the drip rail, above the belt, outside the
aperture band, forward of the tail column:

```
  body-cream pixels in the whole frame        1799   (0.23 % of frame)
  best 60 x 20 body-cream window              33.8 % pure
```

Same shape as §10.29's `COUNTERTAN` conclusion: no admissible same-class
reference exists in that frame and none can be manufactured.

**AND IT IS THE WORST FRAME THIS PROJECT OWNS.** Measured from the files:

| frame | size | bits/px | JPEG DC quantiser |
|---|---|---|---|
| `ref_side.jpg` | 1024×768 | **2.32** | **4** |
| `ref_rear34.jpg` | 1200×824 | **9.28** | **1** |
| `ref_workshop.jpg` | 1200×824 | **8.87** | **1** |

DC quantiser 1 is essentially lossless. Everything on this project is measured
from the most compressed of the three. That is not a reason to distrust past
work wholesale — but where a feature is visible in more than one frame, prefer
the others, and **measure the PSF before quoting anything near the limit**
(rev 17's hubcap work found the ring's band is 1.05 σ in `ref_side.jpg` and
11.6 σ in `ref_workshop.jpg`; a naive half-level crossing on `ref_side` reads
exactly double, because a blurred band never reaches its own plateau).

**THE CODEC IS NOT THE EXPLANATION, AND THE OBVIOUS CONTROL FOR IT IS WRONG.**
"Smooth the frame, re-encode through its own quantisation tables, re-measure"
charges the codec for the blur's own leak: a Gaussian blur at σ followed by a
Gaussian high-pass at σ **does not leave zero**. That mistake overstated the
floor by about 4×. `codec_floor()` now blurs by 4σ, measures the LEAK with no
codec at all, and subtracts it in quadrature — and prints the leak so it cannot
go unchecked. True codec contribution: **0.31–0.66 %** at every scale, against
8.89 %. A CONSTANT field through the same codec gives exactly **0.0000 %**, so
the estimator has no intrinsic floor. **The structure is real. The surface and
the frame were wrong.**

**RE-BASED ON `ref_rear34.jpg`, settled by the owner.** The largest clean cream
in any frame is the **lid underside**, the panel lettered "La Santa",
`u 588–760, v 40–190`: 25 800 px, **80.8 % class-pure after a 3 px erosion**,
0.2 % clipped. Caveat that must travel with every number from it: it is an
**inward-facing** panel, so it is a **LOWER BOUND** on the sun-exposed flank.

```
  sigma_px   total %    leak %    codec %    REAL %
     1.0       1.752     0.812     0.313     1.724
     2.0       2.254     1.226     0.403     2.218
     4.0       3.608     1.754     0.510     3.572
     8.0       5.769     2.426     0.547     5.743
    12.0       6.771     2.829     0.570     6.747
```

**THE mm AXIS IS NOT ESTABLISHED AND WAS NOT INVENTED.** Three routes to px/m on
that frame were tried and all three failed: the aperture band is **truncated by
the counter** (≥ 320 px/m), the tyre OD is **truncated by the frame edge**
(≥ 397 px/m), and the bulb string — the one locked feature in the lid's own
plane, `BULB_PITCH = 0.0286 m` — is **NOT DETECTED**, peak/mean 3.6 with
candidate periods scattering 225–629 px/m. Do not convert the table above to
millimetres until a scale is locked.

**WHAT KIND OF TEXTURE IT IS — four discriminators, none needing a scale.**

| σ | corr(dL\*, dC\*) | dL\* rms | dC\* rms | anisotropy v/u | skew |
|---|---|---|---|---|---|
| 2.0 | −0.123 | 0.860 | 0.715 | 0.885 | −6.69 |
| 4.0 | −0.315 | 1.410 | 0.967 | 0.894 | +0.02 |
| 8.0 | **−0.486** | 2.071 | 1.210 | **0.918** | +1.73 |

Luminance and chroma are **anti-correlated**, increasingly so with scale; the
chroma structure is of the same order as the luminance structure; and the
anisotropy is ~0.9 at every scale, i.e. **isotropic**. That is **CHALKY
SUN-FADE MOTTLE** — patches oxidised *lighter and less chromatic*. It is not
dirt (both would fall together, correlation positive), not brush or roller
texture (chroma would be flat), and not dents (chroma flat, structure smooth at
large scale only). It reproduces §10.30c's whole-panel fade signature
(C\* −55 %, L\* up, hue constant) at the *local* scale.

**CONSEQUENCE FOR THE FIX, and it finally explains `W_ALBEDO`.** A **scalar
multiply on albedo cannot change chroma**, so no value of `W_ALBEDO` could ever
have reproduced this — which is exactly what its zero-ablation showed in rev 15
(`T1_W_ALB=0` → 0.342 %, shipped 0.260 → 0.339 %, identical) and what
AUDIT_rev11 said in prose before anyone measured it. The map must modulate the
**existing fade path** — rev 14's `FadeVert`, which fades the cream family
toward white and is currently *spatially constant* — and drive **roughness**
with it. **It is not an albedo-breakup map.** `W_ALBEDO` should stay closed.

**NOT BUILT IN rev 17.** The grounding is complete and the mechanism is
identified, but the map itself is not written, because its amplitude cannot be
tuned against a target whose mm axis is open. That is the next revision's first
job and it now has a designed shape rather than a constant to sweep.


### 10.39 rev 17 — a re-typed constant rev 16 fixed in one file and missed in the other

`verify.py:47` re-expressed `SPEC["L"] = 4.290 − (O_OLD − O_NEW)` when the tail
was re-spaced. **`audit.py:319` went on hardcoding `4.290`.** So `STATE.md` —
the file this repo declares authoritative over all prose — reported

```
  overall length (ex counter)  4.0648  vs 4.2900  = -225.2 mm **OUT**
```

on a quantity `verify.py` **PASSES** at **+9.8 mm** against 4.0550. Exactly the
`counter_top` failure shape the rev-12 audit found at this same line, and a
direct breach of the rule that *a constant tuned against another constant must
be expressed in terms of it*.

Fixed by **importing `verify.SPEC["L"]`** rather than recomputing it, so there
is now exactly one definition in the repo and no third copy can appear.

**STILL OPEN, same table, same shape:** `overall height (max, any station)`
reports **3.0169 vs 1.9600 = +1056.9 mm OUT** every run. It is measuring the
**open lid board standing above the roof**, not the vehicle. A prose note under
the row says the test is wrong; a note is not a guard. It has cried wolf for
nine revisions and should either exclude the lid objects or be deleted.


### 10.40 rev 17 — `vw_bars`' air-gap docstring was false, and the V was short

The docstring claimed "a clear 12.7 mm air gap between the V apex and the W peak
at the locked ring diameter of 0.370 m". Measured on the **built** nose roundel
(ring outer D 0.2802 m):

```
  V apex underside      z = -0.03515
  W centre-peak top     z = +0.01686
  -> the V PENETRATES the W by 52.0 mm.  There is no gap.
```

Three separate errors: there is no gap but a 52 mm interpenetration; `0.370` has
been stale since rev 10 (`ROUNDEL_D = 0.2800`, built 0.2802); and **no diameter
can open one** — the spine separation between the V apex `(0, −0.060)` and the W
peak `(0, −0.075)` is 0.015 R while each stroke's mitred half-extension is an
order of magnitude larger. The two fuse **by construction**, which is why
"correcting the diameter" closed the designed gap twice and merged the glyph
into an X twice. **§10.25's premise is wrong; the fusion is correct against the
photographs and stays.** The sentence is deleted rather than re-valued.

This is what "a claim in prose is not a guard" is about: it survived nine
revisions because nobody grepped for the node that does it.

**AND THE V WAS SHORT.** Building the hubcap ring exposed that the V reached
only **0.7154** of the glyph's fit radius while the ring's inner edge sits at
**0.8140** — the V stopped **4.28 mm short of the band (4.9 % of the emblem D)**,
where every reference frame shows both arms running into it. Tips scaled by
`0.8140 / 0.7154 = 1.1378` about the apex → `(±0.400, 0.560)` becomes
`(±0.4551, 0.6455)`. **Arm angle unchanged at 57.171°** and the V's radius
(0.7898) stays below the W's (0.7965), so `_fit_glyph`'s scale does not move.
Written as an expression of the ring's own band fraction so the two can never
drift apart again.


### 10.41 rev 17 — the hubcap ring, and the PSF that decided which frame to measure it in

`CAP_RING_BANDFRAC = 0.093 ± 0.012`, **band width / ring outer D**, dimensionless
and derived from `CAP_EMBLEM_D`, never a metre value.

The decisive step was measuring each frame's **PSF** from isolated step edges
before measuring the feature:

| frame | PSF σ | feature outer D | band at 0.09 D |
|---|---|---|---|
| `ref_side.jpg` | 1.625 px | 18.1 px | **1.05 σ — unresolved** |
| `ref_workshop.jpg` | 0.689 px | 91.7 px | **11.6 σ — resolved** |

A naive half-level crossing on `ref_side.jpg` reads **0.18 D, exactly double**,
because a blurred band never reaches its own plateau. Two routes on the resolved
frame give 0.0874 and 0.0995; a PSF forward model on `ref_side` gives 0.065 and
its profile likelihood **excludes 0.18**.

Ceiling stated honestly: the statistical floor on the one resolved measurement
is ±0.0013, but the **transfer** between frames cannot be tested better than
≈±0.03 in this photo set. Corroboration found *after* the fact and not used to
derive anything: the nose roundel's own ring, authored long ago as the absolute
`R − 0.028`, measures **0.1005** of its outer D — 0.6 σ away.

Negative control: the workshop van's **plain** hubcap, same detector, in the
frame with 2.4× better PSF — no ring. `CAP_EMBLEM_D` re-derived independently as
0.311 ± 0.007 against the locked 0.317 ± 0.017 (**0.35 σ**) and left untouched.


### 10.42 rev 17 — the real matte, and an identity claim that could not honestly be made

A `File Output` tap off Render Layers **`Alpha`**, upstream of the AlphaOver —
the only place the silhouette still exists. Three settings are load-bearing and
each was measured:

* **`BW`** — `post._mask` does `.convert("L")`, which on an RGBA file takes the
  RGB luma and throws alpha away. An RGBA matte would hand post.py the beauty.
* **8-bit** — PIL reads a 16-bit grey PNG as mode `I`, and `.convert("L")`
  **clips**: a 0→65535 ramp came back with **2 unique values**, not 256.
  `setup_render` puts the beauty frame at 16-bit; the matte must not follow it.
* **view transform `Raw`** — otherwise alpha 1.0 writes as ~232 and coverage
  stops being linear, breaking `backdrop_headroom`'s lerp.

```
  beauty PNG alpha (defect reproduced)   min 255  max 255   1 unique
  matte                                  min 0.0000  max 1.0000  256 unique
  strictly between 0 and 1               26.0042 %
  subject cover                          26.1475 %   heuristic mask: 30.585 %
```

Disagreement is one-directional: 0 px subject-in-matte/backdrop-in-heuristic,
5325 px the reverse — the heuristic's erosion plus the shadow pool, which
`level >= 250` calls subject. Orientation checked, not assumed: subject IoU
**0.8549 upright, 0.5542 flipped**. Negative control: subject deleted → cover
**26.1475 % → 0.0000 %**, mean alpha ×3900 lower.

**BIT-IDENTITY ON THE DEFAULT PATH WAS NOT CLAIMED, BECAUSE IT IS NOT TRUE.**
Two renders of the same frame with *nothing changed* differ by **max 40 DN over
12.86 % of pixels** — OIDN plus adaptive sampling. Against that null the tap-on
arm sits **inside** it (max 41, 12.85 %). So the claim made instead is
structural: the subgraph reachable backwards from the `Composite` node — node
types, all input defaults, all incoming links — serialises **EQUAL** before and
after, and with `T1_MATTE` unset the node is never created. **rev 14's
"byte-identical, hash-verified" claim for `post.py` should be re-read in this
light**: it may have been true of that path, but the same words applied to a
render path cannot be.

Gap recorded, not hidden: under `T1_BORDER` the tap writes a full-size matte with
content only in the rendered band, and **`hero.py` does not stitch mattes**. A
matte for a stripped hero must come from a single-pass render until it does.


### 10.43 rev 17 — `flank_compare.py`: the brief's premise was refuted and the real defect found

The rev-17 brief said the flank windows must be re-derived because the rev-16
loft moved the shell. **It did not move any of them**, and that was measured
rather than assumed: `SCR` lies entirely forward of `X_AXLE_R`, so
`t1_core._aft()` is the identity on it; the widened arch's forward foot is
**146 mm** clear of the panel's aft edge; and `RT_ALL`/`CR_ALL` act **810 mm**
above the panel top.

What *had* moved was the **instrument**: `REF_PPM = 211.2`, one scalar for a
projective photograph. Local scale runs **205.21 px/m at u 331 to 214.95 at
u 600** — a 4.7 % gradient, ±6.2 px across the lockup. Retired in favour of the
§10.35 map.

**THE +95 mm INK OFFSET IS 87 mm OF MISSING TARNISH, IN THE RENDER MASK.** In the
render `Señor` comes out **tarnished brown (179, 90, 78) against a ground
endmember of (194, 87, 74)**. The reference mask has five thresholds — silver
plus four measured tarnish zones — and rev 14's render mask had **one**. So
`Senor`'s box returned 3.5 % ink against the reference's 33.8 %.

```
  silver rule alone                          ink top +90.1 mm   (reproduces +95)
  with the four tarnish windows carried in    ink top  +3.1 mm   (padding is 3.8)
```

Not the loft, not the panel.

Re-measured through a common metric frame, both masks warped once, nothing
resampled onto anything:

| metric | value | ceiling / bar | verdict |
|---|---|---|---|
| ink area ratio | **0.9364 ± 0.026** | 1.000 ± 0.10 | PASS (was 0.8869) |
| ink aspect | **+4.86 %** | ±5 %, **±2.3 % instrument floor** | PASS (was +16.04 %) |
| IoU | **0.7631 = 0.889 of ceiling** | ceiling **0.8585 measured this run** | PASS |
| worst region | **`Senor` 0.394 = 0.504** | of its own **0.782** ceiling | **FAIL** |

Controls: a **positive** control that is not tautological — the texture's own
alpha on the `SCR` rectangle, no render and no threshold rule, gives IoU 0.7666
= 0.893 of ceiling against the render's 0.889, so the render plus the entire
mask rule are worth **−0.004** and the remaining 0.107 is the panel against the
map. A **negative** control — the same mask squashed 8 % through the identical
sampler — fires the aspect test (+13.98 %) and costs 0.133 of IoU. A
**resolution** control — 900×600 flips the aspect verdict — so the file now
warns when the render under-resolves the photograph.

**No threshold was changed.** Registration was found to need +76.2 mm forward
and +61.9 mm down, and rev 14's ±66 mm search had its optimum **on the
boundary**, so rev 14's IoU was of a mis-registered pair.

Carried forward for other owners: `SCR` is **+80 mm aft** and **12–24 mm short
in height**; and the projective map and `k_t` disagree by **2.3 %** at the rear
hub, which is the floor under every height ratio in that file.


### 10.44 rev 17 — `H_ROOF` delegated, and deliberately NOT changed

The owner delegated the `SPEC H_ROOF = 1.960` decision ("I trust your
judgment"). **It is unchanged, and the +23 mm warn stands.**

The case for changing it is real: REF §1 derived 1.960 from `ground = 668.0`,
the exact datum §10.11 bans, and `HANDOFF_rev16` records that the belt-anchored
chain puts the crown at **1.981**.

The reason it was not changed is the project's own most-repeated rule. **1.981
is a parenthetical I could not reproduce.** Composing the belt-anchored chain
from the numbers in §10.34 — belt at the rear axle 1.2436, belt → drip rail
529.7 mm measured, drip rail → roof top 209 mm measured — gives **1.9823**,
which agrees to 1 mm; but the model's own belt → drip rail is **568.0 mm**, not
529.7, because rev 16 deliberately spent that 38 mm on the junction rather than
the roof line. So the three terms are not simply additive in the model's
parametrisation and the agreement may be coincidental. Resolving it needs a
direct probe of the built mesh, not arithmetic on tabulated differences.

**Changing a locked constant to a number I have not watched print is exactly
what "do not put a figure in an acceptance test unless you watched it print"
forbids**, and doing it in the direction that clears a warn is what makes it
look like tuning. Left for a revision that can probe the mesh. The warn is
0.7 σ against `D`'s own ±35 mm, so nothing is materially wrong meanwhile.


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

### 10.45 rev 18 — THREE `verify` ROWS THAT COULD NOT FAIL, and one guard that measured two constants

The first adversarial audit ever run on the rev-16 loft (`AUDIT_rev18_loft.md`)
found that the loft's **geometry** is largely sound and its **measurement
infrastructure** is not. Three rows of `verify` returned the same answer for
every possible input, and all three printed something reassuring.

**11e, the engine-lid shut line.** The threshold was the literal `loc.x > -1.95`
while the docstring said "the tail skin sits at x ~ -2.09". It never did: at the
OLD tail station `-2.1080` the threshold was already **158 mm inboard** of the
skin, and after rev 16's re-space the skin is at `-1.8730`, putting `-1.95`
**77.0 mm behind the entire vehicle**. Every ray that hit the tail at all scored
"got through" — 28/28 open, and `1.0000` returned with the outline displaced
+350 mm, −300 mm, +600 mm and squeezed to 20 % of its width.
`t1_shell.engine_lid_gap` cuts at `X_TAIL + ENGLID_CUT_DX` and **expressed it
that way**; verify kept a literal. Now the same expression, passed in by the
caller. Falsified after the repair: displacing the outline
+0.15 / +0.30 / −0.20 / +0.60 m gives **0.1429 / 0.6429 / 0.1429 / 0.0000**,
where the old threshold gave 1.0000 to all four.

**11d, the rear window.** `_ray_clear(body, (-2.40, 0, z), (1,0,0), 0.35)`
terminates at **x = −2.0500**, which is 177 mm short of the tail skin today and
was 58 mm short even at the old station. It touched nothing, so the test was
unconditionally True and "the rear window is cut" was asserted by a ray that
never reached the vehicle. Controls at 0.45 m below, 0.70 m below and 0.15 m
above — all certainly solid — returned True. Unbounded, the same ray travels
**4.3738 m** and first hits the WINDSCREEN. Both endpoints are now offsets from
`X_TAIL`. After the repair the two "below" controls read **False**; the "above"
control still reads True and that is **logged as unresolved, not tuned away**.

**10, the ride height.** `X_DROP_REF = (0.0650 − RAKE_Z0)/RAKE_DZDX` and then
`RIDE_DROP = RAKE_Z0 + RAKE_DZDX·X_DROP_REF`, which cancels to the literal
0.0650 **for any rake**. Residual exactly `0.000e+00`, and `RAKE_Z0` set to
0.000 / 0.020 / 0.200 / 0.500 all pass — i.e. the stance could be reset to
stock, the precise rev-4 regression the row exists to catch. The identity is
kept and correctly LABELLED as an identity; the quantity that actually says this
bus is lowered nose-down — **the rake, locked at 0.01775 by §10.9** — is now
guarded for the first time.

**And the arch guard measured no arch.** `verify.py:527` was
`gap = ARCH_R − TIRE_R`: a subtraction of two source constants, returning
41.0 mm forever regardless of what `rear_arch_outline` built.
`ARCH_W_REAR`, `_ARCH_PROFILE`, `_arch_drop` and `rear_arch_outline` appear
**zero times** in `verify.py` and **zero times** in `audit.py`. Replaced by
`_arch_lip_z`, which walks z upward at the axle station until the flank skin
appears and returns `None` — never an endpoint — if it finds no transition.

**Guard tally at the time of the audit:** of §10.34–37's eleven headline
figures, **one** had a guard that measures the mesh (the rear overhang), **one**
had a guard that could not fail, and **nine** had no guard at all.

### 10.46 rev 18 — THE REAR ARCH: a double-counted crown, a refuted trace point, and a mirrored sign

Three defects, one fix, applied together because any one alone lands the other
two wrong.

**(a) The crown was double-counted.** `rear_arch_outline` evaluates
`z = ARCH_R − h·_arch_drop(t)` and the raw table's smallest drop is 0.057, never
zero — but `ARCH_R` **is** the measured crown lip height. §10.37 says it is
HELD, `t1_shell`'s own header says it "must not move", and `LOFT_GROUND` §2.6
instructs *"hold the crown height, widen to 0.92 m, and use the §2.3 profile."*
The first clause was never implemented. Consequence: the lip sat **20.9 mm low**
at the axle and the tyre gap **20.1 mm against SPEC §2's locked 41 ± 8**.
Confirmed on the built mesh at **20.2 mm**.

**(b) The `(0.10, 0.014)` entry is not a measurement.** Re-traced in rev 18:
reproducing §2.1's own ±7-row half-max method DOES reproduce a 4.5 px spike, but
the raw pixels put the lip edge on row 524→525 at **every** column across it —
the window straddles a dark folk-art speck 5 px above the lip and locks onto the
band. Re-anchored on the edge, the lip reads
**371.4 / 370.9 / 371.4 / 372.1 / 372.3 / 372.1 mm: flat.** And through
LOFT_GROUND §0's own map, `Δx/a = +0.10` is **u = 759.53** — inside the band
§2.1's text says it REJECTED (*"dark folk-art specks at u 657, **758-761**,
844-845"*). **The 9-wide median filter §2.1 announces was never propagated into
the §2.3 table.** Corroborated without any re-trace: §2.4 says the crown is flat
within 1.2 mm over 164 mm, a span containing this station, and 0.046 × h =
16.0 mm is **13×** that.

**(c) The Δx sign convention was mirrored.** §10.37 and `t1_shell`'s note both
assert the table is stated forward at −0.90 and aft at +0.90.
`rear_arch_outline` emits `(t·a, …)` and `solid_prism` is passed `u = (1,0,0)`,
and `+x` is FORWARD — so `t = +0.90` landed forward. Settled empirically, not by
argument: through LOFT_GROUND §0's map increasing `u` runs **aft**, and the
anomalous `+0.10` station lands at u 759.5 in the **aft** rejected band.

**Applied and measured, at BOTH subdivision levels:**

```
rear  arch lip above hub 0.3527 -> 0.3722 m ; tyre gap 20.2 -> 39.7 mm
front arch lip above hub 0.3732 m unchanged ; tyre gap 40.7 mm
VERIFY: 1 fail, 1 warn  ->  0 fail, 1 warn
```

**The front arch is the positive control and it did not move** — rev 16 never
touched it, it is still circular, and it reads `ARCH_R` to **0.3 mm** before and
after. The rear now agrees with it to 1.0 mm and with `ARCH_R` to 1.3 mm, against
39.9 mm predicted from the re-based table. **The guard was not widened**: it
failed because the geometry was wrong and passes because the geometry was fixed.
`ARCH_R`, `ARCH_W_REAR`, the front arch and every station are untouched.

**NOT MEASURABLE, and recorded as such:** the crown's *centring*. After the fix
the built lip's argmax sits 130 mm aft of the axle, but the lip varies only
**3.5 mm over ±130 mm**, so the argmax on a flat crown is ill-conditioned — the
same reason §2.4's "centred to 0.2 px" could be neither confirmed nor refuted
from the photograph. It is not measurable on the mesh either.

### 10.47 rev 18 — `STATE.md` stopped publishing three phantoms, one of them unknown

`STATE.md` is declared authoritative over all prose. It was publishing three
numbers that were not measurements of what they named.

| row | was | mechanism |
|---|---|---|
| overall length | `4.0648 vs 4.2900 = −225.2 mm OUT` | `audit.py` kept the literal 4.290 that rev 16 had already re-expressed in `verify.py`. Fixed in rev 17. |
| overall height | `3.0169 vs 1.9600 = +1056.9 mm OUT` | `H` was max z over EVERY mesh; the lids are modelled open and `lid_strut0` spans to 3.0169 |
| **roof z @ mid-wheelbase** | **`0.3497`** | **the ROCKER, seen through the roof hole** |

**The third was not known before this revision.** `_roof_at`'s window is
`|y| < 0.30` and the roof aperture spans y[−0.5450, +0.5650] over
x[−1.0700, 0.9640], so at mid-wheelbase the **entire** window is inside the
hole and `max()` fell through to whatever else was in the x-slab. Error
**−1612.8 mm**, with **n = 18** selected vertices — a non-empty selection of the
wrong surface, so the `if zs else nan` guard never fired. That is exactly the
failure `audit.py`'s own rev-7 comment describes for `reach()` (*"`or -9` hid
the empty selection behind a plausible number"*), reproduced inside the function
written to replace it. Now floored at the window head, printing `n` at every
station, and reporting *"inside the roof aperture"* rather than a number.

**Knock-on nobody had traced:** `H = 3.0169` was the denominator of four console
percentages. Rocker **10.5 → 16.0 %**, belt line **40.0 → 60.7 %**, sill/head
→ **65.7 / 86.0 %**. The height row also stops carrying a target at all: "max
over ANY station" is not the quantity `H_ROOF` names, since 1.960 is a
**rear-axle** figure. rev 8 spotted this and wrote a prose note under the row
while leaving it emitting OUT. **A prose note is not a guard.**

Two paragraphs were also **hand-authored into a file whose header says nothing
in it is typed by hand** — one quoting roof residuals the table beneath had long
overtaken, one asserting *"0.507 / 0.516 / 0.526 — they are not equal"* four
rows below a live line printing **0.516 0.515 0.516**, which rev 13 settled and
`t1_shell.py:131` explicitly retires.

Free cross-check: the repaired `_roof_at` prints **1.9835 (n=66)** at the rear
axle, matching `verify`'s independent `_roof_z_at` probe to four decimals.

### 10.48 rev 18 — px/m on `ref_rear34.jpg`, and the unsourced constant underneath it

§10.38 left the cream map blocked on one measurement: px/m on `ref_rear34.jpg`.
Three routes had failed. The fourth — the `1963` plate — works.

[OWNER, marked crop, box (1020,580,1200,720) at ×6] **"empty chrome license
plate frame."** `t1_detail.py:1371` already reads `"1963", EMPTY. CONFIRMED in
ref_rear34.jpg`, and the model builds an empty aperture with schematic
seven-segment digits **on the top rail**, which is where the pale marks are.
Reading and build agree.

Gated on **geometry first, then colour** (§10.38's rule): saturation separates
chrome from red paint whether the chrome is bright or tarnished. Box
(1060,615,1185,715), inside rev 15's own probe box for the same feature.
Negative control on clean red body 165 px away: **0.58 % chrome-ish**.

```
top rail    v = -0.082721*u + 725.386   rms 0.563 px  (n=71)
bottom rail v = -0.095033*u + 797.199   rms 0.754 px  (n=75)
H = 57.89 +- 1.13 px   (fit 0.94, level systematic 0.63)
```

The edge is **5.3 px wide (10–90 %)**, so the threshold was **swept, not
picked**: H runs 57.23 → 58.50 over levels 0.30–0.60, spread 2.18 %.

**px/m on the plate plane = 344.1 ± 6.7 (±1.96 %)**, ±2.6 % once
`PLATE_ASPECT`'s ±1.73 % is folded in for the metric conversion.

**rev 15's own published rails for this feature are REFUTED on their gradient.**
They converge at u = −3035, mine at +5833 — opposite sides, so the tail face
recedes the wrong way in one of them. Settled on features that are not the plate:
the two body grooves converge at **u = 8251** (rms 0.476 and 0.368 px on ~175
columns each), agreeing with mine. rev 15's bottom rail was **rms 1.031 px on
n = 15**. Its *height* is only 2.9 % off, so little downstream moves — but the
**gradient** is what carries a scale across a panel.

rev 15's own control passes: the cream rim gives 330 px/m at the wheel, which is
further from the camera, so the plate must exceed it. 344.1, ratio 1.043, right
direction; and its 0.1754 m cap on `PLATE_OUTER_H` holds with 4.1 % to spare.

**THE WEAK LINK, AND IT MUST TRAVEL WITH THE NUMBER: `PLATE_W = 0.3300` has no
provenance anywhere in this repo** — no derivation comment, no SPEC entry, no
`REF_MEASUREMENTS` entry. `PLATE_ASPECT` is properly measured (wheel-as-
protractor, no px/m in the chain); the WIDTH is a bare constant, and any scale
built on `PLATE_OUTER_H` inherits it. If 0.3300 is a catalogue plate width it
collides with the standing instruction never to correct this vehicle toward the
factory catalogue. **Bounded by the wheel control, not measured.**

| 2026-08-10 | **rev 9 addendum — §10.15.** Donald identifies `ref_rear34.jpg` as showing the FRONT of the vehicle with the roof opening forward, not a rear three-quarter. Every crop attributed to that file is now suspect, including the flank paisley that §10.10 marked done. He also restates the governing standard for rev 10: *"we are recreating a photo realistic version of that exact bus."* |
| 2026-08-10 | **rev 9 addendum — §10.17, §10.18.** Donald restates the acceptance criterion as **per-measurement**: "nearly indistinguishable from the original. Any single measurement off is unacceptable." And flags the front fascia as drifting — six items, four of them audit findings logged and unapplied for several revisions, one new (cab-door folk art far too faint), one unmeasured (bumper depth). The folk-art item contradicts §10.9's near-nose coverage lobes, which were scanned by body x across an OPEN cab door. |
| 2026-08-13 | **rev 14 — the tail gate, and a starburst nobody had seen.** The flank tile stops printing on the flat tail face: a TAIL selector mirroring the nose one, keyed on the surface normal so the rear quarter keeps its real 43.687 % gold while the flat face goes to **0.05 percentage points measured against a `T1_W_ART=0` negative control** (photograph 0.006 %, pre-fix render 14.30–18.11 %). Rendering a rear elevation for the first time in fourteen revisions exposed a radial starburst that survives ablation of the folk art, the albedo breakup and the specular — **the tail cap is a valence-115 pole and the nose cap a valence-110 pole**, recorded and deliberately left for the phase-5 loft work. Sun fade reaches vertical surfaces through a new per-material `FadeVert` input at the diffuse view factor 0.50, switched on for the cream family only so SPEC 10.12’s locked red albedo saturation is untouched. Glass panes flat-shaded (88.7 % of pane pixels, 9.4× the null). The mural’s neutral lift identified as `img_paint`’s specular pedestal, 0.42 → 0.16, first step not a solve. `W_ALBEDO` 0.130 → 0.260 with the map window exposed, and honestly not solved. **`flank_compare.py` computes a number for the first time and the flank script FAILS 3 of 4** — aspect +16.04 %, dimensionless; the old test could not fail because it had cropped the photograph down to the render’s own error. `post.py` gains the backdrop A/B the owner asked for, default byte-identical. Owner settles the split windscreen. |
| 2026-08-14 | **rev 15 - four constants refuted, the detail pass lands, and the owner retires the white lock.** The restore DID NOT FAST-FORWARD: the rev-14 line never contained `f3c53f4`, the rev-13 tip, and all seven rev-14 content checks passed anyway because each greps a rev-14 string (10.33). Detail geometry applied with its measurement: cream rim 0.5729 -> 0.6611 against 0.660 +/- 0.008 (10.9 sigma -> 0.13) with the profiles now scaling onto the previously dead `RIM_R`; VW glyph 0.5639 -> 0.7761, the scale read BACK off the built outline so no fraction can go stale; hubcap emblem 0.1897 -> 0.317; T-handle from 240 mm ABOVE the plate to 214 mm below, written as a ratio of `PLATE_OUTER_H`; plate aspect +32.6 % at 14 sigma, solved using the cream rim as a protractor after the vanishing-point method was thrown out at 1.2 sigma; tail lamp OD 0.1030 -> 0.19560. Louvre ends NOT MEASURABLE and not invented. Per-bay galley replaces one 21 W wash with three per-bay boxes -- the lever's sign was backwards, ablating the fill RAISES contrast -- taking bay 2's gap 4.64 -> 0.73 while bay 3 moves TOWARD the photograph. The glass brief is REFUTED: 'rear pane CV 1.22' was a bounding box; on the pane's own hull it reads 0.214 against a photograph at 0.221-0.293. **Four separate solves returned 'the named constant is not the parameter' (10.31)** -- `T1_MURAL_SPEC` solves NEGATIVE in all three channels, `W_ALBEDO` measures identical to its own zero ablation, `COUNTERTAN` has a secant gain of 0.33-0.49 and would demand a non-wood, and rev 13's bloom threshold has no admissible value. A dead-argument bug found: `build_all()`'s rough/coat/spec for `countertan` were never read, exposed by a four-arm ablation identical to four decimals. Hero at **4320x2880**, 18 strips, worst seam z=2.75. Owner retires SPEC sec.6's pure-white lock on the measured A/B (10.32) and re-admits Nolita photographs FOR GEOMETRY ONLY. The loft is grounded but not built: crown R 2.45 +/- 0.15 REFUTED twice, the roof EDGE is 63 +/- 20 mm too high, the tail 235 +/- 22 mm too long. |
| 2026-08-14 | **rev 16 - THE LOFT: roof section, rear arch, tail and the end-cap poles, in one rebuild.** `LOFT_GROUND`'s 63 mm `ZT_ALL` drop is REJECTED and re-measured at **41 mm** by a datum-free route -- drip-rail groove to serving-aperture top, 28.3 / 27.4 / 27.5 mm across bays 3/2/1 over 228 columns at sd 0.19-0.21 px, against 68.6 mm built -- because the 63 would leave 2 mm of metal above the bays and drop the shell's top edge below the windscreen's own anchor. The belt line shows the aperture band is right to **-2.1 mm**, so the error is the junction, and the hub route's extra 22 mm is the same ~29 mm ground-datum common-mode 10.11 bans. Spent on the junction: `RT_ALL` 0.054 -> 0.0949, `CR_ALL` 0.032 -> 0.1179, **D = 0.2128 against LOFT_GROUND's independently measured 0.2116 +- 0.035**, `ZT_ALL` and the rake untouched, `DOME_DEFICIT` -> 0; built mesh measures back at +27.0 mm against 27.7 +- 0.5. `LOFT_GROUND`'s roof-silhouette 257.2 could NOT be reproduced (the top edge is flat at 252.1-253.6 over u[755,815]) and its proud-strip/coaming reading is withdrawn. Rear arch rebuilt as a flat-crowned ogee from the normalised TABLE, not the window-dependent exponent, 0.747 -> **0.920 m**, `ARCH_R` held, front arch left circular because it has never been measured. Tail **re-spaced, never translated**, overhang 1.008 -> **0.773 m** via `_aft()`, with the projective flank map rebuilt from its own constraints and cross-checked on the arch's aft foot to **1.5 mm**. `SPEC['L']` stops being the VW catalogue 4.290 and becomes an expression of the applied tail correction; a new verify row guards the rear overhang itself. **10.30b closed**: Coons quad-grid caps, max valence **115 -> 6**, and the starburst measures **3.015 -> 1.609 (-47 %)** against a negative control in the same frame reading 1.596 -> 1.592. `NHALF` 56 -> 57 so the cap is mirror-symmetric -- chosen on a guard result, not a preference: the 27x28 arm FAILS at SUB=2 with `gap_englid` rolled back, and moving the cutter does not fix it. Two latent bugs exposed: `roof_cutters` passed `zlo` as `solid_prism`'s CENTRE, and every tail-anchored detail would have left `verify` row 1 passing on a phantom. Guards 0 fail / 1 warn at both levels. |
| 2026-08-14 | **rev 18 - THE FIRST ADVERSARIAL AUDIT OF THE LOFT, and three guards that could not fail.** Four agents on disjoint files, all read-only, each told to refute; two refuted their own briefs and two refuted each other's headline statistics. **The loft's geometry is largely sound and its measurement infrastructure is not** (§10.45): the engine-lid row's threshold sat **77 mm behind the entire vehicle** and never worked at any revision; the rear-window ray **terminated 177 mm short of the tail** and returned True aimed at three certainly-solid places; row 10's `RIDE_DROP` test is an **algebraic identity with residual exactly 0.000e+00**; and the arch guard subtracted two source constants, so `ARCH_W_REAR`, `_ARCH_PROFILE`, `_arch_drop` and `rear_arch_outline` appeared **zero times** in either guard file. All four repaired and each falsified after repair. **The rear arch double-counted its own crown** (§10.46) - `ARCH_R` *is* the crown lip height and the profile subtracted a crown drop from it, putting the tyre gap at **20.2 mm against a locked 41 +- 8**; the `(0.10, 0.014)` trace point is **refuted by re-trace** (the lip is flat at 371-372 mm; the station is u 759.5, inside the band §2.1 says it rejected, and the 9-wide median it announces was never propagated into the table); and the Dx sign was **mirrored**. Fixed together: gap **20.2 -> 39.7 mm**, with the untouched front arch reading `ARCH_R` to **0.3 mm** as the positive control in the same run. The guard was not widened. **`STATE.md` stopped publishing three phantoms** (§10.47), one previously unknown - its mid-wheelbase roof height was **the rocker seen through the roof hole**, off by **-1612.8 mm** with n=18 so the empty-selection guard never fired - plus four percentages that were percentages of a lid strut, and two hand-authored paragraphs in a file whose header says nothing is typed by hand. **px/m on `ref_rear34.jpg` is LOCKED at 344.1 +- 6.7** off the plate frame the owner identified as empty (§10.48), refuting rev 15's own gradient for that feature on a third method - but **`PLATE_W = 0.3300` has no provenance anywhere in the repo** and every scale built on it inherits that. Guards **0 fail / 1 warn at both levels**. |
| 2026-08-14 | **rev 19 — the cream was measured on a detached sign, and `FadeVert` never reached the flank.** Shown a marked crop with the boxes printed, the owner identified `cream_rms._LID` — the source of every rev-17/18 cream number — as **a DETACHED SIGN, separate from the bus**, re-confirming §10.28 which §10.38 had silently reverted (§10.49). Re-based on the surface he identified as the bus's own paint, trimmed for a measured reason: **10.17 % of it is CLIPPED** and a clipped pixel carries no texture. Gate is now **geometry only** — the old `sat < 0.20` is tuned to the sign's C\* 11.2 and returns **2.9 % purity on the vehicle's own cream**. **The character verdict was a constant string** (§10.50): handed pure red paint at 0.0 % purity with every statistic `nan`, it still printed CHALKY SUN-FADE MOTTLE. The replacement derives the verdict and returns **None**; controls now separate red paint and foliage as DIRT/SOILING and refuse a 12×12 patch. The mechanism **survives** re-derivation on the correct surface; the amplitude does not — the sign is **2.1–2.6× more mottled** than the bus. **`FadeVert` has never reached the flank** (§10.51): `T1_body` carries `T1_paint`, which renders cream and red in one material and was left at **0.000**, while the material named `cream` carries exactly one object, `vw_disc` — rev 14's fix landed on every cream surface except the one it was measured on. The map now lives inside `body_paint`, multiplied by the material's own two-tone selector so the red is **0.0 by construction**, with `fadev_from` raising a hard error rather than falling back to a scalar. **The ablation exposed that a luminance high-pass is the wrong instrument for this lever** — on the albedo pass the map moves corr(dL\*,dC\*) **+0.261 → +0.048** monotonically toward the photograph's +0.042 — and **"the cream is 26× too uniform" does not survive**: dL\* rms was already 0.322/0.584/0.948 against 0.385/0.493/0.735. What is short is **chroma**, 0.24 flat against 0.74–1.30 growing, and the lever is bounded: the fade factor clamps at 1.0 so the modulation collapses past AMP 1. Depth correction **stated**: region 2 is the **flank** plane at **337 ± 7 px/m**, not the plate's 344.1. A **fourth `STATE.md` phantom** recorded (§10.52) — `audit.py` still publishes the constants-only arch gap as "41.0 mm (measured 41)" against the mesh's 39.7. Guards **0 fail / 1 warn at both levels**, geometry unchanged. |
| 2026-08-15 | **rev 21 - the owner's napkin reading obtained, and five routes to the cream albedo all refuted by their own controls.** He identified N2/N3 as white paper napkins and M1 as bare stainless - and refuted a second crop of mine in the process: rev 20's boxes A and B each straddle a napkin face AND the dispenser body, which is the real reason they disagreed, not shading (10.57). rev 20's C/D/E are dropped on a measurement, not an argument: they sit inside the galley opening at 0.22-0.32x the cream's luminance, and a neutral cannot be 3-4x darker than the surface it shares light with. **Route A, the napkin as a same-light neutral, is clean and robust** - three faces clipping at 22/12/0 % agree on hue 44.5-48.2 and sat 0.163-0.203, R>G, and because clipping compresses toward neutral the agreement is itself the control. **It still must not be applied.** The third method fails: de-illuminated by the napkin the flank red reads hue 13.1-13.8 against the independently locked RED's 5.0, and shading explains only 1.7 of the 8.5 degree gap across 30 patches spanning a 4.27x luminance range. **10.12's own invariant says why** - the ratio (G-B)/(R-B) is 0.2225 +- 0.0045 in `ref_rear34` against 0.0813 for the locked albedo, **+31 sd**, so that frame is not related to the locked constants by ANY neutral transform. Inverting the reference refutes itself: using the locked RED as the illuminant makes the white napkin come out a saturated purple, giving **a new rule - an illuminant reference must carry substantial albedo in all three channels**, and RED's are (0.552, 0.029, 0.018). Solving 10.9's full affine model with both surfaces has **no physical solution** for any napkin albedo, and the diagnosis is concrete: the red reads 95 % of the napkin's R channel where 0.552 against white paper should read 65 %, so the two are not under the same light. **`CREAM` UNCHANGED at (206,208,200).** Separately, a subagent's claim that four `audit.py` livery rows are identities that cannot fail was **tested and half refuted** (10.58) - they are invariant to the rake, which `t1_core.py:165-171` shows is deliberate, but displacing the authored constants makes them print OUT and throw FAILs. Guards **0 fail / 1 warn at both levels**, every figure identical to rev 18/19/20; geometry untouched. |
| 2026-08-15 | **rev 22 - the hero is shot at last, `H_ROOF` is retired by the owner, and item 3's target is refuted as a category error.** First hero since rev 16: **4800x3200, SUB=2, 56 samples, 20 strips, worst seam z = 1.91** against a threshold of 4 (rev 16 shipped 1.89), `post.py` run **once** on the stitched frame - the first photograph of the rev-18 arch fix, rev 17's hubcap rings and rev 19's cream mottle. **`H_ROOF` = 1.960 RETIRED as an accuracy target on the owner's call (10.59)**, after a chain of withdrawals left it with no admissible derivation: REF sec.1 derived it from the ground line 10.11 bans, and its only ground-line-free support - `LOFT_GROUND` sec.1.2's 1.9621 - was withdrawn by 10.34 without noting it was the last one. It was **NOT re-valued to the mesh probe**, which the owner rejected and which would make the guard compare the model to itself and clear a warn by tuning. The probe survives as a **labelled regression catcher, baseline 1.9835 WATCHED PRINT at both levels (SUB=2 reads 1.9833), band +-5 mm**, and was **falsified two ways**: displacing the baseline -10 mm gives `MOVED +10.0 mm`, and raising `CR_ALL`'s crown **+8.0 mm in the GEOMETRY** gives `MOVED +7.9 mm` - the second arm proving it reads the MESH, which the old arch guard never did. Guards **0 fail / 1 warn -> 0 fail / 0 warn at both levels**, and **the warn is gone because THE TEST WAS WITHDRAWN, not because the model improved; the mesh did not move**, every other figure identical. The absolute roof height is now OPEN and UNMEASURED. **`COUNTERTAN`'s hue target REFUTED (10.60)**: the cited 28.4 deg / 0.333 is an **OBSERVED PIXEL** and `COUNTERTAN` is an **ALBEDO** - the 10.21 trap. Re-measured clean (n=162, 0.00 % clipped) the observed top reads 32.3 deg / 0.364, while de-illuminated through the docstring's own arms it reads **39.3 and 41.7 deg against the built 42.3**, with sat 0.254 inside the arms' 0.225-0.289: the claimed ~14 deg error is **at most ~3 deg**, and nothing moves on that while the LEVEL is unresolved. Two new findings from controls never previously run: **the founding crop straddles two materials** (rows 411-415 include the shadowed transition, 54 codes darker, and run into the brass nosing at sat 0.669 / r/g 2.36 - thirteenth instance, and in SPEC's own founding measurement), and **the cab-roof reference is NOT under the same light as the fascia** - after removing the albedo ratio the residual illuminant is B/R **1.219, 22 % bluer** - so that arm is inadmissible under 10.21 and the LEVEL bracket's upper end rests on it. `COUNTERTAN` UNCHANGED, fourth revision running. |
