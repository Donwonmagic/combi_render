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
showing those features is the wrong LIVERY STATE.**

### 7.1 ONE VEHICLE, THREE LIVERY STATES — settled with the owner, rev 44

**"Whether it is physically the same vehicle is U" is ANSWERED: it is the SAME
VEHICLE.** Put to him directly — *is the bus in `ref_nolita_doorshut.jpg` the
same vehicle as `ref_side.jpg`?* — the owner answered **same vehicle**,
photographed in a different livery state.

**What that changes.** GEOMETRY from the Nolita frames is **ADMISSIBLE**. In
particular rev 43's corroboration of §10.100's door outline **stands**; had the
answer gone the other way it would have evaporated and §10.100 would have
reverted to resting on `ref_side.jpg` alone. **What does NOT change:** livery
is still state-dependent, so folk art, script, aperture glazing and roof-board
treatment may never be carried across states. §7's rule survives — it is a rule
about LIVERY, not about vehicles.

### 7.2 THE ERA TAGS WERE WRONG — finding 23, rev 44

**BOTH RED-LIVERY FRAMES THE PROJECT HOLDS ARE MEXICO-SHOT.** `ref_rear34.jpg`
carries a Spanish sign reading **"FAVOR DE ORDENAR Y PAGAR AQUÍ"**, palms and
banana plants, and an open-air patio with café tables; `ref_source.jpeg` is a
Mexican street scene with Spanish signage and a palm. Both readings are direct
and neither needs a ruler.

**AND THE OBVIOUS INFERENCE FROM THAT IS WRONG — RETRACTED IN THE SAME
REVISION THAT MADE IT.** Rev 44 first wrote *"so the red livery is Playa-era,
and the project holds no Nolita photograph of the red bus"*. **That does not
follow, and it is false.** Published descriptions of the Nolita taqueria
describe *"a bright red 1963 Volkswagen bus … parked between several tables"*
with *"its roof cut off and lifted to reveal a chalkboard"* — i.e. **the RED,
folk-art bus is the one standing in Nolita**, having been shipped from Mexico.

**So livery colour is NOT an era discriminator and must never be used as one.**
What the evidence supports is only the narrow claim: **these two particular
frames were shot in Mexico.** The era of any frame must be read from its SCENE
— signage language, vegetation, indoor/outdoor — not from the paint.

**Rev 14's re-admission of Nolita material rested partly on the opposite
premise**, and so did rev 44's first cut of this section. **No measurement
moves** — this is provenance only, and §7.1 keeps the geometry admissible.

**Sourcing note:** the Nolita descriptions are **WebSearch result text, not a
photograph and not fetched** — this environment can search but `WebFetch` and
`curl` are both egress-blocked, so no page was read and no image obtained.
Graded **R** at best. It is strong enough to KILL an inference, which is all it
is used for here; it is not used to support one.

### 7.3 THE SCRIPT IS IN TWO PHOTOGRAPHS — finding 22, scoping SANCTIONED rev 44

`ref_workshop.jpg` carries the same "Señor Tacombi" script on the green body as
`ref_side.jpg`, and until rev 44 no document connected them. **The owner has
sanctioned this scoping: LETTERFORM GEOMETRY is admissible from the workshop
frame; COLOUR AND WEATHERING ARE BARRED from it.**

**Its ceiling, and a correction to how that ceiling has been stated.** The
workshop view is an **INDEPENDENT** view, not a better one: the script region
measures **210 × 140 px** there against `ref_side`'s **320 × 110** near-broadside,
and it is foreshortened. **Those two figures are the SCRIPT CROPS, not the
frames** — the frames themselves are 1200 × 824 and 1024 × 768. The rev-44
brief stated them as view sizes; corrected here.

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
| `livery-9` roundel 9 % undersized, 32 mm high | **REFUTED, and it had been applied in the wrong direction.** Measured **0.280 +/- 0.030 m** by an exact relation needing no camera pose; centre **0.149 +/- 0.030 m BELOW the belt**. The build read `ROUNDEL_D = 0.3700` — 32 % over — and the finding's only photographic support was `ref_source.jpeg`. **FINDING 21, rev 44 — and this entry was corrected TWICE in one revision, the second time against myself.** §10.22's citation *"retired in 0.2"* is wrong: **§0.2 carries no `ref_source` row at all.** But rev 44's first correction then over-reached by concluding *"that frame is NOT retired"* — **it is retired, in §10.2**, which calls it *"the retired 246 × 197 thumbnail"*. The citation was wrong; the retirement is real. **THE CONTRADICTION IS THEREFORE WORSE THAN EITHER STATEMENT OF IT, and it is now measured rather than argued:** §1 defines grade **M** as *measured from `ref_source.jpeg`*, five of §0.2's ⚠ locks carry it (blackwall tyres §8.1, cream bumpers §8.2, the **red nose roundel** §8.3, the three-aperture rear corner §8.4, the cream counter slab §8.5), and **§8.1's own coordinates only resolve on that frame** — its stated hub at px (114.5, 160.5) returns saturation **0.73** inside §8.1's published 0.70–0.83 on `ref_source.jpeg` and **0.11** on `ref_side.jpg`, where those coordinates land nowhere near a hub. (The tyre arm reproduces on luminance, 61 inside the stated 34–93, but reads sat 0.17 against *"< 0.08"* — a sector-average bleeding over the rim edge, so the arm is directional, not exact.) **So §0.2's five locks rest on a frame §10.2 retires.** The resolution ceiling is real and separate: at 246 × 197 the frame runs ~1 px per 40 mm, which is why `livery-9`'s 32 mm claim failed — that finding was refuted on resolution, not the frame on admissibility. **STILL OPEN. It needs the owner, or the five locks re-derived from an admissible frame** | corrected to 0.280, and **113 mm down** |
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

### 10.24 — three things measured, applied, and then reverted. **ITEM 3 IS NOW CLOSED (rev 44); ITEMS 1 AND 2 REMAIN OPEN.**

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
3. **Headlamp vertical position. APPLIED AT REV 44 — thirty-four revisions
   after it opened.** The same pass gives headlamp centre = belt - 0.339
   +/- 0.025 m against the build's belt - 0.242 — a 97 mm discrepancy at
   ~3.9 sigma. The stated blocker was *"a single-chain claim … it deserves a
   second derivation first"*. **That derivation was produced at rev 11 and
   discharged the blocker at rev 37 (SPEC:6999); this entry never learned of
   it** — the carrier failure §10.91.1 names, inside SPEC rather than between
   contexts.

   **Rev 44 re-checked both arms of the discharge before acting, and they are
   NOT equally sound.** The **ORDINAL** arm is unanimous and scale-free —
   rev 11's indicator-below-the-break test, rev 44's chord test (the break cut
   **131.9 mm across a 172.4 mm lens** while `ref_source.jpeg` has the lamp
   clear with 12 px of red above), and the owner's own words. The
   **roundel-ratio MAGNITUDE** arm, *"83 ± 19 mm at 4.4 sigma"*, **DID NOT
   REPRODUCE**: the same arithmetic on today's constants returns **103.4 mm**,
   because `ROUNDEL_Z_AG` is itself stale (ledger finding 26). **That arm was
   set aside as contaminated and NOT used.**

   **So the magnitude came from the belt-relative arm alone**, which touches no
   stale constant and is independently anchored at −2.7 mm by §10.98's
   sill-to-break cross-check. `HL_Z` **1.0300 → 0.9330**.

   **Result:** `probe_rev44_report3` **C6 GREEN** — the lens top now sits
   **45.2 mm BELOW** the break where it stood 51.8 mm above it. Guards 0 fail /
   0 warn at both levels, both tools; 190 meshes, 5 constant-rough, unchanged.

   **THE TRAP WAS RESPECTED AND IS NOW ARMED.** The roundel was not moved —
   measured on the **built mesh** at **1.0170**, and on screen at **dy = +0.01
   px**. `probe_rev44_lampmove` 4/4 keeps it that way. **An independent arm
   agrees after the fact:** the roundel-to-lamp separation lands at 0.1695 m
   against the photographed 0.1758 ± 0.0185 — **0.34 sigma** — from a chain
   never used to derive the move.

   **A re-typed constant was repaired because the fix needed it:** the
   indicator's Z was the literal `1.2360` while its comment claimed *"Z is set
   RELATIVE to the lamp"*. It was not — 1.2360 is 1.0300 + 0.206 re-typed, and
   the lamp would have moved out from under it. Both Y and Z now expressed.
   §10.25's own rule. **TO REVERT: `HL_DROP = 0.0`.**

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
| ~~**trunk lid**~~ **THE TAIL BOARD** | ~~**OPEN**, at the tail~~ **a raised BOARD, not a lid** | present, but its free edge runs off the frame at u=1199 | cream face, RED rim over the tip half, near-black over the base half, amber bulbs on the lower edge |

> **RETRACTED rev 48, AND ANNOTATED HERE ONLY AT REV 49.** The raised thing at
> the tail in `ref_side.jpg` is **not the trunk lid open**. §10.122 refuted it
> and this table was never marked, so the machine went on publishing the
> retired identification in a live row — the fourth instance of exactly the
> failure §10.122.5 names. Two independent refutations:
> **(1)** its base measures **1.747 ± 0.027 m** above ground (the drip rail)
> against `ENGLID_GAP`'s z 0.6025–1.1025 — about 11 σ;
> **(2)** stronger, the engine lid is top-hinged at z 1.103 over a 0.50 m
> panel, so **no opening angle whatever** puts any part of it above z 1.60, and
> this board's tip is at **z 2.184**. Unreachable. And the engine-lid band is
> directly visible in `ref_side.jpg`, **closed**, red, carrying the yellow swirl.
>
> **NOR IS IT `signboard()`'s board.** That is the **"La Santa"** cream +
> red-brush-script sign standing on the **ground behind** the bus in the same
> frame, retired by the owner 2026-08-10 (§10.28, §10.49, §10.122.5). Two
> different objects in one photograph, and the record conflated them.
> **THE OWNER SETTLED IT AT REV 49:** *"That was referring to a different sign.
> This one is part of the vehicle."* Three pieces of physical evidence agree:
> the base sits on the drip rail to 1 px of the locked fit; the board's bulb
> string is **continuous with the drip-rail run — one circuit**; and a power
> cable descends from it into the body. Built as `t1_shell.tail_board()`.

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
post at the vehicle's centreline that the photograph shows. **[REFUTED, rev 30, SPEC 10.83 — the centreline is the two-tone V apex at u = 311.5 (REF §9) and the post's own columns are 357–374, so it is NOT on the centreline; its lateral position is UNMEASURED and the post is deliberately NOT built.]** *[THE ANNOTATION IMMEDIATELY ABOVE IS WRONG ON BOTH OF ITS TERMS — SPEC 10.86, rev 32. (a) STATUS: SPEC 10.84 (rev 31) downgraded this refutation from REFUTED to UNDECIDED because its two terms sit at different DEPTHS. That downgrade was written into 10.83 and was NOT swept back to here, so this line has read "REFUTED" for a whole revision after the claim stopped being refuted. (b) ANCHOR: SPEC 10.85 (rev 31b) established that u = 311.5 is NOT the V apex — it is the V's RIGHT ARM's occlusion point at the over-rider bar — and published the apex at u = 288.8 +- 3 px. Neither position for the post is settled. The post remains UNBUILT, which is the only part of the annotation that still holds.]* Confirmed against a
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
| 2026-08-18 | **rev 41 — THE Z-LADDER'S GATE CANNOT BE RE-DERIVED, AND THE COUNTER-FASCIA FINDING IS A RULER SCOPE ERROR (§10.99).** Item 1's criterion was stated BEFORE the run and **REFUTED BY ITS OWN RUN**: G3, two-sided half-prominence descent, admits **10 of 10** bands including all three at −193/+222/+193 mm — their curves DO descend both sides, so they are not ramps riding a bound but well-formed local maxima in the wrong place, and §10.97.7's mechanism does not survive the corrected datum. **THE NEGATIVE CONTROL IS THE FINDING:** displacing the reference 120–360 px, every offset ≥ 2×SEARCH so no true dy is reachable BY CONSTRUCTION, the inherited gate still answers **181 of 260 = 70 %**, with null prominences reaching **2.13–3.11×** against an inherited bar of **1.08×** — and **nine of ten bands' real prominences sit BELOW their own null maxima**. `MIN_PROM` was never a filter; the gate is not mis-tuned, the statistic has no power. Re-derived as **G4, a max-statistic null test** whose bar is each BAND'S OWN null maximum — not chosen, per-band, and built where the answer is unreachable so it cannot be steered: **1 of 10 answers, NO RULING**, the survivor z 0.90–1.20 at **−1 px = −5 mm** reproducing the joint fit from a tenth of the pixels. **AND THE VERDICT WAS TESTED FOR BEING MINE:** one bar sweep returns **FLAT (19 mm), NO RULING and NOT FLAT (415 mm)** — the ladder's answer is a function of the bar, not of the vehicle. The flat-versus-scale question is NOT awaiting a better gate; **the z-ladder cannot answer it**. The **JOINT registration (−1, −4) px** is untouched and §10.98's headline does not rest on the ladder. **ITEM 3 REFUSED, and not executed:** §10.98.11's −6.5 mm counter fascia compares the right FEATURE on the WRONG RULER — both photographic readings are taken on the counter's outer face (0.295 m nearer the camera) and divided by the FLANK's px/m, which `t1_detail.py` states of that very 113-column run. REF §6's own parallax pair fits a one-parameter model exactly (**s = 0.9533**, reproducing REF's +16/+21 mm, camera height 1.531 m), taking **−6.5 mm → −2.1/−2.8 mm**, sign-changing across `t1_detail`'s documented +15…+31 mm bracket; and the third route sharing no step — REF §6's slab edge **22.65 px = 0.107 ± 0.005 m** against the built **0.1070 m** — is **zero**. §10.98.11's "two readings 0.7 mm apart" is COMMON-MODE, not a cross-check. **NO GEOMETRY MOVED, NO ARTWORK MOVED, no hero owed**; guards 0 fail / 0 warn at both levels on both tools; all 29 inherited probes match their published tallies. **FOUR DEFECTS OF MINE, ALL CAUGHT BY CONTROLS:** a TRANSPOSED C1 target `(-4,-1)` for the published `(-1,-4)`; an INVALID first C3 that rolled the edge map without the mask and manufactured an instability signal, replaced by an end-to-end render shift (predicted −10.5 px, observed −11); a **CONSTANT VERDICT STRING** asserting "no bar supports FLAT" three lines below a row printing FLAT — §10.50's defect, third instance in this repo, second by me; and C6, which proves the fast scorer equals the inherited `np.roll` form to **6.75e-13** rather than claiming it in a comment. |
| 2026-08-18 | **rev 40 — THE 81 mm IS A DATUM ERROR; item 1 was STOPPED before it moved geometry (§10.98).** `probe_rev39_flank.py` pins the model's counter fascia **BOTTOM** onto the photograph's counter fascia **TOP**. `flank_compare.py`'s own comment claimed they are *"the SAME cream/red break ... the same physical edge, so the two are used as ONE datum and its height never enters"* -- **the two lines are fitted with DIFFERENT ESTIMATORS in DIFFERENT ROW WINDOWS** (a LUMINANCE gradient over rows 425-452 on the reference, a REDNESS gradient on the render) and on a cream / gold-nosing / beige-fascia / red stack those are not the same boundary. §10.45: a claim in prose is not a guard. **Measured, `probe_rev40_datum.py`, READ-ONLY:** the render datum sits at authored **z = 1.1459** against `t1_detail.CNT_ZB` **1.1470** (**1.1 mm**, read with `ast` at run time) and `CNT_ZT` 1.2540 (108 mm); the reference datum sits **0.69 px** from the photograph's fascia TOP and **19.46 px** from its bottom. **THE JOINT WHOLE-VEHICLE REGISTRATION SETTLES IT IN ONE LINE: rev-39 datum (+19, -1) px = +92 mm; rev-40 datum (-1, -4) px = -5 mm.** **AN INDEPENDENT ARM SHARING NO DATUM WITH THE WARP CONFIRMS IT:** photographed window-sill-to-body-break **102.7 +/- 6.6 mm** (n=8, cab door -- the only place the body's own break is visible) against a built `Z_SILL - Z_BELT_AUTH` of **100.0 mm** and REF sec.3(a)'s own hand figure of 100.0 -- **-2.7 mm. A break line 81 mm out of place would show ~81 mm here.** **FIXED, opening no new estimator:** the reference datum now uses the redness gradient the render side already used, `v = -0.03412 u +466.632`, **19.8 px = 92 mm below** the rev-39 line -- one counter fascia. `_assert_same_edge()` armed **TWO-SIDED on both fits** (reference step +0.5608, render +0.6598, bar +0.030) and **FALSIFIED with `T1_FC_OLDDATUM=1`**, which restores the old fit and makes the guard **FIRE at -0.0293**. **`SCR` RE-MEASURED AND ITS VERTICAL TERM FLIPS SIGN:** §10.97.2's *+76.2 mm forward and +61.9 mm down* becomes **+76.2 mm forward (unchanged -- the datum never entered x) and -33.3 mm, i.e. 33 mm UP**; 61.9 - 33.3 = 95.2 mm, one fascia height. NOT APPLIED. **A SECOND PROBE DEFECT:** dx and dy were searched **sequentially** and are coupled -- the sequential search returns dx **-15 px (-71 mm)** where the joint returns **-4 px (-19 mm)**. Now joint. Consequence: §10.97.4's *map validated at 5 mm* is withdrawn and re-valued at **19 mm**. **AND THE Z-LADDER NO LONGER RULES FLAT:** seven bands cluster at -5..-24 mm, three return **+/-193-222 mm** -- **the same three that DECLINED under the rev-39 datum**, and +222 mm is the exact figure §10.97.7 says its gate was written to kill. Prominence cannot separate them (1.20/1.30/1.55 against a good band's 1.23). **THE GATE WAS NOT RETUNED**; the derived verdict is spread 415 mm, **NO RULING**. So **§10.97.5's "FLAT, ONE RIGID OFFSET" was a property of the datum, not of the vehicle**, and an acceptance gate calibrated on one datum does not transfer to another. **REGION 3 CLOSED BY HIM** after twenty-one revisions -- *[stated, rev 40]* the pale band under the brass nosing is **THE COUNTER'S FRONT FACE**, superseding rev 12's "body's own belt paint" and explaining his rev-19 non-selection. The model's routing was already right. **That makes the depth measurable: painted fascia 87.1 mm built against 93.6 +/- 2.0 mm (this probe, 5 cols) and 94.3 mm (`t1_detail`'s own independent 113-column half-max run) -- two photographic readings 0.7 mm apart, model -6.5 mm SHORT.** NOT APPLIED. **A SCOPE ERROR OF MINE, IN THE SECTION DOCUMENTING SCOPE ERRORS (§10.98.13):** the first cut published *"13.4 mm TOO DEEP"* by comparing the model's whole **slab** (107.0 mm) against the photograph's **painted fascia** -- `CNT_NOSE_F` caps 19.9 mm of that slab in brass. Corrected to **-6.5 mm, opposite sign**. **Naming a defect class does not immunise you against it.** **MY POSITIVE CONTROL C3 FAILED AND IS PRICED, NOT LOOSENED:** the gate reproduces REF sec.3(a)'s hand-read cab-door table at +1 px on three columns and +2 on the fourth, a one-sided **+1.25 +/- 0.43 px = 6 mm** bias -- and pricing it is what later showed it must NOT be applied to the fascia figure, whose cross-check uses a half-max criterion instead. **§10.24 IS NEITHER RE-OPENED NOR RE-CLOSED** -- what is withdrawn is only §10.97.6's claim to be a fourth, headlamp-free corroboration of it. **NO GEOMETRY, NO ARTWORK AND NO CONSTANT MOVED**; guards 0 fail / 0 warn at both levels on both tools; 3/3 texture md5s unchanged. |
| 2026-08-15 | **rev 26 — the front bumper carries an OVER-RIDER BAR the model does not build (§10.75).** Shown `ref_workshop.jpg` — the ONE frame where the front bumper is not occluded by the lamppost — beside a render of the current build, with three pointer boxes printed in original-frame coordinates, the owner ruled **A (the upper tube) and C (the vertical post) are BOTH ON THE BUS**: a bumper over-rider bar and its post. **The model has no member for either** — `build.py:322` builds one blade and `:326` two 62 × 30 mm brackets. Confirmed against a render made this revision. **Scope also settled by him: model them, TAGGED WORKSHOP-STAGE**, because `ref_workshop.jpg` is the conversion stage and §2.4 records the REAR bumper was removed between that stage and service — so front hardware present in the workshop is not automatically present in service, and no in-service frame shows the front. Tagged the way Nolita geometry is (§10.32), so it can be pulled back out. **THE MEASUREMENT IS NOT DONE AND THE FIRST PASS FAILED ITS OWN CONSISTENCY CHECK, recorded rather than tidied away**: a naive column scan returned blade heights of 30/42/41/36/34/12/9/11 px — a 4.7× spread caused by the foreground trolley occluding the blade's lower edge — giving 0.574 ± 0.507, which is not quoted anywhere. Restricted to the seven clean columns and **sweeping the threshold rather than picking one**, the tube reads **11.7 → 7.9 px across thresholds 110 → 170 with sd ≤ 0.8 within each**: tight per threshold, **±19 % across the choice**, and that systematic is what binds. **MY OWN PSF CONTROL WAS INVALID AND IS RECORDED AS SUCH** — the 10–90 rise I fitted crossed the nose two-tone break DIAGONALLY, so its 52.0 px measured the boundary's slope, not the point spread; §10.38's *check the control itself* applying to a control written in the same session. **No metre figure is available and none is invented**: there is no admissible px/m on the bumper plane in this three-quarter frame, §10.48's 344.1 is the plate plane of a different photograph, and §10.72 has just established the bumper face's own station is unmeasured. **NO GEOMETRY WAS CHANGED on this finding.** rev 27 inherits it well-posed: valid PSF first, then a plane scale or a proof none is admissible, then build. |
| 2026-08-15 | **rev 26 — `COUNTERTAN`'s pedestal is IDENTIFIED after six revisions, and it is the settled-dust film (§10.70).** Four arms — two albedo points × dust on/off — through rev 24's index-clean mask at ONE purged rig: pedestal **60.8/58.2/59.5 % → 25.1/25.0/31.9 %** with `T1_CTAN_DUST=0`, and **→ 6.6/6.6/8.5 %** once spec and coat go too. **Dust carries 57.1/52.6/36.6 % of it; dust + spec + coat carry 89.3/87.9/84.8 %.** The dust-shipped arm **reproduces §10.65's published clean pedestal to three significant figures in all three channels** on an independently restored tree — that harness control is what makes the rest readable; null control exact in every arm, noise floor 0.211 % against a 35-point effect. **WHY FIVE REVISIONS MISSED IT:** §10.56 ablated dust, saw the top's radiance rise only +4.1/+8.6/+13.3 %, and concluded "REFUTED — and it was HELPING". **That does not follow.** Removing a mix of coverage `f` and base-independent colour `D` changes radiance by `f·(A−D)` — small *precisely because* `W_DUST_COL_UP` is within **13.5 %** of `COUNTERTAN` in R — while contributing `f·D` to the pedestal, which is large. Both true at once; §10.56 measured the wrong derivative. **§10.68's rule inverted: a SMALL magnitude does not mean a small contribution.** The coverage was never hidden — `t1_mats.py:366` says "mean coverage 0.548 on the counter top" in prose and a **live assert** recomputes 0.548256 on every build. **Independent cross-check from an unrelated route:** removing a mix at coverage `f` must raise `k` by `1/(1−f) = 2.214×`; measured **1.988/1.978/1.989**, agreement claimed to ~10 % and no better. The lever was checked before it was believed — `Dust` reaches Base Color and nothing else, so it removes the ALBEDO per §10.56's own rule; `T1_CTAN_WEAR=0` also drops Metallic and is stated as two levers. **Nothing tuned: `COUNTERTAN` UNCHANGED, sixth revision.** What this settles is *why* it was never solvable — `k` is **2.37× weaker** in the shipped configuration than the bare surface allows, by construction. **§10.71, found while verifying that and RECORDED NOT APPLIED:** `W_DUST_FAC_UP = 0.7313` is pinned by a live assert that predicts `_UP_MEASURED` ("dirty counter top") from **`COUNTERCREAM`**, while the top carries **`COUNTERTAN`** — re-anchored to the right base the assert **fails by 0.1600, eighty times its own 2e-3 tolerance** — and **both halves entered in ONE commit**, `00d3819` "…tan counter top…". The name-matched-material family again, fifth instance. **§10.72 — work item 3 is MALFORMED:** `2.145 = 4.290/2` and `2.140 = 4.280/2`, both changed in the **same diff hunk** of `27f6ee6` "…against factory sources", so the 5 mm is exactly half a catalogue revision; `verify.py:33` already records 4.290's catalogue origin and `:37` invokes the standing instruction for `L` while §2's bumper row never got it; `X_BUMP_F/R` have **zero read sites**; `BUMP_OFF`'s own comment shows the mesh was **fitted to the constant**; the rear face is commented out at `build.py:325`; and the `:191` citation is stale (`:201`), **born stale in the commit that wrote it**. Neither value is measured — strike both, re-open as UNMEASURED. **§10.73 — work item 2 is an ARTEFACT:** `_DOOR_TOP_AUTH`'s "4.2 mm" compares a five-knot **run mean** with a **station value**; at x = 1.36 on `DOOR_GAP_S`, the outline that actually cuts, the disagreement is **0.315 mm**. rev 25's pre-print comment was right and its print measured a different quantity. Value HELD, **no re-bake owed**, `DOOR_H` 1.013467 unchanged. **§10.74 — two defects in rev 25's own record**, caught on arrival: `swirl_b.png`'s md5 wrong in its eighth character (`d2015971` → **`d201597e`**; the file was always right), and §1's `ls rev25_hero34f.png` check **cannot pass on a fresh clone** because §7 of the same document explains the hero was deliberately filtered out — check deleted, not loosened. **NO GEOMETRY MOVED, NO ARTWORK MOVED**; guards 0 fail / 0 warn at both levels throughout, textures byte-identical. |
| 2026-08-15 | **rev 25 — the bake frame is PARSED, the artwork is RE-BAKED for the first time since rev 11, and the hero photographs it.** Work item 2's own brief REFUTED: `_ZB_AUTH`'s claimed **76 mm at the tail is CONFIRMED exactly** (76.222 mm at `x = X_TAIL`) and **refuted as a defect** — the bake paints NOTHING aft of x = −1.40, so ink-weighted the missing `_aft()` re-space is **0.0023 mm**, not "larger than `DOOR_X0`" but ~7 500× smaller. Two controls isolate it (re-space 75.540, dropped knots 20.925). **The real `_ZB_AUTH` defect was never named — five DROPPED KNOTS**, worst at **+2.085 on the NOSE**, 19.477 mm peak over **3.53 %** of the ink. **`DOOR_X0` dominates and is worse than rev 23 recorded**: `DOOR_REAR_DX = 17.250 mm`, and the uncomputed consequence is **`DOOR_W` 1.935 % too wide** — it divides every u of the door art, displacing **82.5 % of door ink > 2 mm**, ink-weighted **6.290 mm**, with **3 411 px past the true rear shut line** (1.44× the whole B-pillar). **THE CONTROL FAILED AND THAT WAS THE FINDING**: re-baking UNCHANGED does not reproduce the committed art (**4.029 % / 4.261 %**, max Δ 255). Determinism was checked BEFORE interpreting it (two processes, identical md5), then a bisect holding the tree at rev 24 and swapping in ONLY pre-rev-23 `folk_gen.py` reproduced the committed files **BYTE-IDENTICALLY** — **the model was wearing artwork fourteen revisions old**, and rev 23's "nothing in the current build changed" is true of the BUILD while leaving a 4 % divergence from its own corrected source (§10.68). Fixed **structurally**, the work rev 23 declined to do blind: a deliberately tiny `_ceval` reads `t1_shell`'s constant GRAPH (`DOOR_GAP`'s expressions, `BAYS`' comprehension, `B_PILLAR`'s environ default) and `t1_core`'s `ZB` knots, so `DOOR_X0` is EXPRESSED IN TERMS OF `BAYS[0][1]` and `T1_BPILLAR` moves the ART frame with the geometry; three more re-typed literals removed, **all three still AGREEING — exposure, not damage**. **Falsified in four arms, and the fourth cross-confirms from an unrelated route: the B-pillar width reproducing the retired `DOOR_X0 = 0.9084` is −0.005250 m, against §10.62's independently derived −0.0053 for the broken GEOMETRY — 0.050 mm apart.** The door art had been drawn to a door that could not open. `_DOOR_TOP_AUTH` **deliberately NOT parsed**: "within 1 mm" was written into a comment before being watched print and the print refuted it at **4.2 mm**, so it is HELD at 1.8140, `DOOR_H` bit-identical, discrepancy carried forward not absorbed. After the bake: door ink past the shut line **3 411 → 0**, sill error **76.222 → 0.000000 mm**, §10.10 targets held or improved (flank density rms 3.59→3.58 and 3.98→3.96; zone R1 −0.44→+0.29, R2 +0.58→−0.14) — **and door gold 29.09 → 28.90 against 29.08 went the WRONG way, stated rather than hidden**, inside the 28.96–29.19 spread watched printing. **HERO at 4800×3200, 20 strips, worst seam z = 1.91**, `post.py` once, `bloom=0.00`, `backdrop=headroom` — the first frame ever to photograph artwork matching the model's own source; a strip killed by the shell limit was adjudicated by the **seam check** rather than by its file opening cleanly. **`_RETIRED_VALUES` 5 → 15 rows (§10.69)**: of a subagent's "~12", **nine confirmed against three things each and four refuted or mislocated**; guard fired at all 12 predicted lines with **no false positives**, then 0, falsified in four arms with the §0.2 bullet count **watched print at 29/29**. Two are structural — **§1.1's rows defeat the guard BY RE-EXPRESSION** (the retired taper survives as edge pairs, plus the 100 mm origin shift), now stated as the guard's real ceiling; and **§9 row 10 published the INVERSE of the guard that runs**, contradicting §2 inside the same frozen front matter and failing every current build as written. **NO GEOMETRY MOVED**; guards 0 fail / 0 warn at both levels throughout. |

| 2026-08-15 | **rev 27 — §10.71 measured: the founding patch STRADDLED, and against `COUNTERTAN` there is no coverage at all (§10.76).** The two source patches for `W_DUST_FAC_UP` had **no coordinates anywhere in the repo**; both recovered forensically by searching `ref_rear34.jpg` for the box whose middle-80 %-of-L\* median **is** the recorded triple — flank u 914–983 v 298–337, trimmed n **2153**, err **0.0**, exact and unique; top u 556–656 v 397–424, trimmed n **2160**, err **0.0**, exact but NOT unique. **Box-independent result:** the counter top is a diagonal band 15–25 px deep and the largest clean axis-aligned rectangle on it is **1060–1512 px** across a swept gate, against the **2700 px** the patch needs — so it straddled whichever box was used (66–82 % tan, 8–19 % cream, 6–9 % brass, 2–4 % a tin can). **TWO OF MY OWN HYPOTHESES REFUTED BY MY OWN CONTROLS:** the solve did **not** consume a stale `CREAM` — the comment's "this file's CREAM (0.9676, 0.7784, 0.4976)" is the **von-Kries gain itself**, reproduced to 4.7e-5, a mislabel not a numerical error; and the straddle is **not** the explanation — on a band-following clean sample with gate and erosion **swept** (12 arms) the disagreement gets **worse**, (−0.295,−0.320,−1.674) → (−0.82,−0.56,−2.19). **The live assert's three-channel agreement is a TAUTOLOGY** (spread 5.2e-05) because `W_DUST_COL_UP` was solved collinear — it is the solve restated. **The real statement: `_UP_MEASURED` lies OUTSIDE the segment [`COUNTERTAN`, `W_DUST_COL_UP`] in all three channels — no coverage error, because there is no coverage.** E-free: observed top/flank **(1.056,0.884,0.803)** vs dusty `COUNTERTAN`'s **(0.881,0.681,0.461)**, B out by 74 %. **NOT DECIDED, deliberately:** the de-illuminated top is **proportional to `CREAM`**, so this frame cannot separate the two, and the pair is the up-facing/vertical mismatch **§10.60 ruled INADMISSIBLE**. **Nothing tuned; `COUNTERTAN`, `CREAM` and `W_DUST_FAC_UP` all UNCHANGED.** Armed instead: a **LABELLED regression catcher** on the three-channel residual, baseline (−0.066877, −0.100324, −0.159974) — *has not moved*, **not** *is right*; do not tighten it. **The guard was wrong before it was right** — its first cut asserted the **max**, which lives in B, so an R-channel move left it silent; **cause fixed, band not widened**. Falsified in **six arms**. Guards **0 fail / 0 warn at BOTH levels**; **no geometry and no artwork moved.** |
| 2026-08-15 | **rev 27 — the F90 question ANSWERED (§10.77).** `probe_ctan_pedestal.py:170`'s UNVERIFIED worry — that `Specular IOR Level = 0` leaves **F90 = 1**, making `T1_CTAN_SP=0` only a partial specular ablation and part of the surviving 6.6/6.6/8.5 % pedestal specular — is **REFUTED BY MEASUREMENT**. New read-only `probe_f90.py` builds a purpose-made minimal scene (one plane, live `COUNTERTAN`, one light, ortho camera) so it cannot be contaminated by §10.65's occluders or stacked rigs, and renders four arms at normal and at **83° grazing**. **SP0 == TRUE-OFF (spec 0 AND ior 1) == bare DIFFUSE to six decimal places at BOTH angles**; the whole specular is 15.834 % of the true-off arm at grazing and the fraction `T1_CTAN_SP=0` fails to remove is **0.00 %**. **rev 26's arm 4 was COMPLETE and the residual pedestal is NOT specular** — one hypothesis removed from §10.70's never-ablated list; `T1_WORLD`, `T1_CYCALB`, `T1_GAL_LUM` and the scene→top bounce remain live. **THE CONTROL WAS THE DEFECT AGAIN, third time this session:** the first positive control asserted *shipped > diffuse* and FAILED at (0.990,1.025,1.158) because the Principled BSDF **conserves energy** — the specular takes from the diffuse lobe. Premise wrong, finding intact; replaced by *differs at grazing* (15.83 %) and *differs MORE at grazing than normal* (15.83 vs 2.02 %, **7.9×**), which is what shows the rig can see a grazing lobe. Null control 0.000 %. **Nothing tuned; no geometry and no artwork moved.** |
| 2026-08-15 | **rev 27 — the residual pedestal's named candidates run (§10.78).** Two harness controls **exact to six decimals** first — the shipped arm and §10.70's arms 7/8 both reproduce on an independently restored tree; null IoU 1.0000 and 0 foreign px in every arm. On the SHIPPED config `T1_WORLD=0` moves the pedestal **−0.01/−0.05/−0.04 points** and `T1_GAL_LUM=0` **−0.00/−0.02/−0.01**. Re-run on the RESIDUAL config rather than assumed to transfer (§10.65's rule): baseline **(6.56, 6.60, 8.51) %** reproducing §10.70's published 6.6/6.6/8.5, and with both levers off **(6.55, 6.58, 8.48) %** — the two together carry **2.64/2.78/2.91 %** of the residual. **REFUTED; ~97 % survives.** **`T1_CYCALB=0` IS A VACUOUS ARM** — it reproduced the shipped arm to six decimals in both albedo points, which looks like a refutation and is not: `ST.cyclorama()` sits at `build.py:600` and the probe's `_build()` truncates `build.py` at line **586**, so no `cyc` object and no `cyc_white` material exist in the probe scene — verified **empirically, not by reading**. The cyclorama is excluded by **ABSENCE, not ablation**, and rev 15's inert-ablation rule extends: an inert arm can also mean the thing you are ablating **is not in the scene**. **`T1_GAL_SKY` IS A DEAD LEVER** — AST census **Store 1, Load 0**, seventeen lines of "SOLVED, not chosen" commentary and **zero read sites**; sixth instance after `RIM_R`, the `countertan` args, `_NOSE_SEL`, `FadeVert` and `X_BUMP_F/R`. Named, not quietly fixed. **The scene→top bounce is now the ONLY named candidate left** and it has no lever — last hypothesis standing is not the same as the answer. **Nothing tuned; `COUNTERTAN` UNCHANGED, seventh revision; no geometry and no artwork moved.** |
| 2026-08-15 | **rev 27 — a VALIDATED PSF estimator, which then DECLINES (§10.79).** §10.75's first over-rider step. Standard slanted-edge construction — fitted edge line, then **RAW pixels binned by perpendicular distance**, threshold pair SWEPT — **validated against a known answer: σ 0.70 → 0.680 (2.9 %), 1.20 → 1.249 (4.1 %), 1.80 → 1.743 (3.2 %)**. **MY FIRST CUT WAS WRONG AND THE CONTROL CAUGHT IT:** it resampled BILINEARLY, which is a triangular filter, so it added its own blur in quadrature and read 0.70 as **1.068 px (+52 %)**, 1.20 as 1.605, 1.80 as 2.113 — the shrinking relative error of a fixed blur in quadrature. **A probe that measures the optics must not add optics of its own.** **MY FIRST THREE ROIs WERE ALSO WRONG** — the trolley frame is the right KIND of edge (a true occlusion step) but it is a **BAR**, so any window holding its step also holds its other edge: contrast fine in 40/40 columns, gradient spread over the isolation limit in **21–40 of 40**. **The isolation test working**, and loosening it would have been the exact failure the probe exists to prevent. A global hunt returns **five** straight isolated candidates (best fit rms **0.055 px**, tilt −0.193), boxes PRINTED — **but the estimator cannot tell an OCCLUSION step from a PAINT BOUNDARY, and that distinction IS rev 26's error.** The first three appear to sit on the cream/green two-tone break; **offered as my reading, NOT relied on**, and put to the owner. Pooling them gives σ 1.736/1.087/0.986 px across the three threshold pairs — a **76 % spread**, itself evidence the pool mixes classes. **NO σ IS PUBLISHED for ref_workshop.jpg**; the probe declines and prints why. If all five are paint boundaries the PSF is **UNMEASURABLE on the admissible set in this frame** — a result, not a gap. **No geometry moved; no metre scale invented.** |
| 2026-08-16 | **rev 28 — the PSF is MEASURED at last, and §10.79's own reading is what was wrong (§10.80).** rev 27 declined to publish a σ for `ref_workshop.jpg` — correctly, because an estimator cannot tell an OCCLUSION STEP from a PAINT BOUNDARY — and offered, without relying on, the reading that the candidates sit on the cream/green two-tone break so the frame is unmeasurable. **The owner refuted it: D1, D2, D3, D4, D6, D7, D8 and D9 are PHYSICAL STEPS; only D5 is not.** He could only answer because the question was rebuilt: rev 27 sent five 60×60 boxes and **every box contains more than one edge**, so `probe_psf_lines.py` (NEW, read-only) re-runs the **shipped** `find_edges`, recovers the fitted line each candidate actually used, and **draws that line** — a question that cannot be answered unambiguously is the asker's defect. **Three defects in `EDGE_NOTES`, a hardcoded string printed while the run reports 35 candidates:** E1/E2/E3 **are one edge**, colinear to ~0.1 px (E1's line predicts 489.8 at u 850; E3 measures 489.7); **two of the five published rms figures — 0.069 and 0.129 — exist nowhere among the 35** (real values 0.073/0.072 and 0.067/0.046), the **eleventh** unwatched figure and inside a probe whose docstring invokes the rule; and **"best fit first" is wrong**, the frame's best candidate being rms **0.025** at a ROI not in the list. Clustered by a stated infinite-line rule with three asserted controls, the 35 candidates are **14 DISTINCT EDGES**; rev 27 named three. **THE FINDING: §10.79's 76 % threshold spread is NOT mixed edge classes.** With the classes settled the pooled spread went **UP to 86 %** — refuted — and the real cause reproduces **on one edge**: across D2's nine independent windows of identical data the 10–90 arm scatters **3.77×** (0.584–2.203 px) while 20–80 spans 4.4 % and 25–75 spans 8.1 %. The 10–90 rise reaches into the ESF **tails**; on a clean synthetic it still recovers a known σ to 10.7 %, so the arm is **tail-sensitive on real windows, not broken**, and the sweep was doing its job. **RESULT: σ = 0.5594 ± 0.0280 px, FWHM 1.317 px**, core arms only, n = 32, over **four independent confirmed steps agreeing to 12.4 %** (D2 0.5806, D3 0.5301, D6 0.5405, D7 0.5136). **D9 excluded and PRICED at +0.176 px / 32 %** for a stated reason that is not disagreement — it is the only candidate whose edge **carries the bulb string**, so the far side of its step is not a uniform surface, and it is n=1. **D1/D4/D8 unmeasurable and NAMED**, D1 missing the monotone threshold by 0.0002. **The owner's own negative control failed, then passed, and the premise was the defect:** on the pooled arms D5 read **sharper** than the steps (0.660 vs 0.736) and the control FAILED; on the core arms it reads **18.0 % SOFTER** (0.6603 ± 0.0167 vs 0.5594) with scatter far below the effect — **the 10–90 contamination was in the control too. Premise fixed, band not widened.** Fourth instance of the control's own premise being the defect. rev 26's fixed-axis method still reads **1.59× larger**, so that correction is intact. **NOT CLAIMED:** any metre scale on the nose/bumper plane (§10.72 struck both bumper-face constants), that the tube's 7.9–11.7 px bracket is closed, or that D5 *is* a paint boundary. **No geometry and no artwork moved; nothing tuned.** |
| 2026-08-16 | **rev 28 — the owner reads the counter top as CLEAN, contradicting a live assert, and a SECOND tautology surfaces in the same chain (§10.81).** Asked with the boxes PRINTED and stated to be **POINTERS** — §10.76 proved no axis-aligned rectangle large enough to sample that diagonal band can avoid straddling — and the pointers were **checked before they were sent**: raw luma spread 27.7 % / 15.0 %, but **0.0 % / 0.6 % once a least-squares PLANE is removed**, against a positive control (§10.76's own proven-straddling founding patch) reading **32.4 %**. The raw figure was the top's own illumination gradient. **[stated] `ref_rear34.jpg` shows the counter top as CLEAN VARNISHED PLYWOOD** — against a shipped settled-dust film at **mean coverage 0.548** recomputed by a LIVE ASSERT every build, which §10.70 identified as **57.1/52.6/36.6 % of the `COUNTERTAN` pedestal**. §10.76 had it merely UNSUPPORTED; it is now **CONTRADICTED by an owner reading of the only frame that shows the surface**. **TAUTOLOGY 2, NEW:** the founding patch's own E-free ratio × `CREAM` reproduces `_UP_MEASURED` **exactly** — it must, because `_UP_MEASURED` was derived from that patch through the von-Kries gain, so **the founding patch can never disagree with the assert it founded**; any future test must use §10.76's band-following CLEAN sample. **Found because my own control FAILED and I checked its premise first — fifth instance:** `probe_clean_top.py`'s first cut asserted the founding patch reproduces §10.76's published (1.056, 0.884, 0.803) and failed at (0.989, 0.840, 0.738); the premise was mine, the published triple is the CLEAN sample's and reproduces to three decimals. **What CLEAN predicts:** going f = 0 moves every channel TOWARD the photograph, worst channel **42.5 % → 34.0 %** — real corroboration from an independent direction — **but f = 0 alone does NOT reconcile it**, clean `COUNTERTAN` still 34.0 % short in B, so the residual is in `COUNTERTAN` or `CREAM`, exactly where §10.76 left it; the implied top albedo is (0.6519, 0.5577, 0.4637) against (0.5870, 0.4930, 0.3060) and **the gap is almost all BLUE**. **The tension is stated, not smoothed:** the best-matching arm is **dusty `COUNTERCREAM` at 8.0 %** — the WRONG MATERIAL for the surface (§10.71) — so the dust does real numerical work under an anchor that is itself wrong, and **§10.60 rules the up-facing/vertical pair INADMISSIBLE so none of it binds either way**. **`W_DUST_FAC_UP` UNCHANGED at 0.7313; `COUNTERTAN`, `COUNTERCREAM`, `CREAM` UNCHANGED; nothing tuned; no geometry and no artwork moved.** Setting f = 0 blind would discard §10.70's pedestal work and swap one unsupported appearance for another. **Top item for rev 29**, and the deadlock is now sharper: not "is the coverage right" but "the coverage is contradicted and this frame cannot supply the replacement". |
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

### 10.78  rev 27 — the residual pedestal: `T1_WORLD` and `T1_GAL_LUM` REFUTED, `T1_CYCALB` is VACUOUS, and `T1_GAL_SKY` is a DEAD LEVER

§10.70 left the surviving **6.6 / 6.6 / 8.5 %** pedestal NOT identified and named
four never-ablated paths, saying the overrides already exist. rev 27 ran them.
**Nothing was tuned; `COUNTERTAN` is UNCHANGED, seventh revision.**

**TWO HARNESS CONTROLS FIRST, both exact.** Before any arm was believed:
the shipped arm reproduces §10.65's `(0.055051, 0.042708, 0.028070)` and
§10.70's arms 7/8 reproduce `(0.054738, 0.045416, 0.029736)` /
`(0.005333, 0.004718, 0.004308)` — **to six decimal places, on a tree restored
independently from the bundles.** Null control IoU **1.0000**, 0 disagreeing px,
0 foreign px and 0.001–0.002 % clipped in **every** arm below.

**On the SHIPPED configuration** — pedestal `P/R`, and the change from the
shipped arm:

| arm | pedestal (R/G/B) % | ΔP vs shipped (points) |
|---|---|---|
| shipped (harness control) | (60.8, 58.2, 59.5) | — |
| `T1_WORLD=0` | (60.8, 58.1, 59.4) | **−0.01 / −0.05 / −0.04** |
| `T1_GAL_LUM=0` | (60.8, 58.2, 59.4) | **−0.00 / −0.02 / −0.01** |
| `T1_CYCALB=0` | (60.8, 58.2, 59.5) | **0 — VACUOUS, see below** |
| `T1_GAL_SKY=0` | (60.8, 58.2, 59.5) | **0 — DEAD LEVER, see below** |

**And on the RESIDUAL configuration, which is the one actually in question** —
§10.65's rule that an inference is not a measurement, so both levers were re-run
on top of `dust = spec = coat = 0` rather than assumed to transfer:

| arm | residual pedestal (R/G/B) % |
|---|---|
| baseline (reproduces §10.70's published 6.6 / 6.6 / 8.5) | **(6.56, 6.60, 8.51)** |
| `T1_WORLD=0 T1_GAL_LUM=0` | **(6.55, 6.58, 8.48)** |

Change **−0.010 / −0.015 / −0.028 points**; the two together carry
**2.64 / 2.78 / 2.91 %** of the residual. **REFUTED. ~97 % of the residual
survives both.**

**`T1_CYCALB=0` IS A VACUOUS ARM, AND THE INERT READING IS NOT EVIDENCE.** It
reproduced the shipped arm to six decimals in **both** albedo points — which
looks like "the cyclorama contributes nothing" and is not. `ST.cyclorama()` is
called at **`build.py:600`**, and `probe_ctan_index._build()` executes `build.py`
only up to its `if os.environ.get("T1_SAVE")` split at **line 586**. Verified
**empirically, not by reading**: no object named `cyc` exists in the probe's
scene and the material `cyc_white` is `None`, while 185 mesh objects do build.
**So the lever does not reach — and the cyclorama is excluded from the residual
by ABSENCE, not by ablation.** rev 15's rule (*an inert ablation can mean the
wrong instrument, not a dead constant*) extended: **it can also mean the thing
you are ablating is not in the scene.** Recorded as a harness-vs-shipped
difference: the pedestal is measured without the cyclorama the hero has.

**`T1_GAL_SKY` IS A DEAD LEVER — sixth instance of the family.** AST census over
`t1_detail.py`: `GAL_SKY` has **Store = 1, Load = 0**. Zero read sites. Only
`GAL_LUM` is consumed, at `t1_detail.py:2047`. `GAL_SKY` carries seventeen lines
of comment headed *"SOLVED, not chosen"* with a three-point sweep and a
film-slope derivation, and **nothing reads it**. Same family as the dead
`RIM_R`, the dead `countertan` shader arguments, `_NOSE_SEL`, `FadeVert` and
`X_BUMP_F/R`. Not repaired here — repairing it would change the galley lighting,
which is out of this item's scope; **named, not quietly fixed.**

**WHAT SURVIVES, AND IT IS NOT CLAIMED AS IDENTIFIED.** Of §10.70's four named
candidates, two are refuted by measurement, one is vacuous and one does not
exist. The remaining named path is the **scene→top bounce** — `gal_warmer`,
`gal_caddy0`, `gal_caddy1` and `T1_body`, the four surfaces rev 24's index pass
NAMED as sitting inside the top mask. **It has no lever, and a ray-visibility
flag is barred by §10.56**, so testing it means removing the objects and
re-deriving the mask. **That is rev 28's item, and it is now the ONLY named
candidate left.** It is the last hypothesis standing, which is not the same as
being the answer.

### 10.79  rev 27 — a VALIDATED PSF estimator for `ref_workshop.jpg`, which then DECLINES: the blocker is EDGE IDENTITY, not method

§10.75 orders the over-rider work "a **VALID PSF** on `ref_workshop.jpg` first
(mine was invalid — it crossed the two-tone break diagonally and read 52 px)".
rev 27 built one, **validated it against a known answer**, and then **declined to
publish a number for this frame** — because the remaining obstacle turns out not
to be the estimator.

**THE ESTIMATOR IS VALIDATED.** `probe_psf_workshop.py`, READ-ONLY. Standard
slanted-edge construction: per-scanline sub-pixel gradient peaks → a fitted edge
line → **RAW pixels binned by their perpendicular distance to it**, with the
tilt supplying the sub-pixel sampling. Threshold pair **SWEPT** (10–90, 20–80,
25–75), each converted to an equivalent Gaussian σ. **POSITIVE CONTROL: a
synthetic step at a known σ, through the identical estimator —**

| true σ | recovered | error |
|---|---|---|
| 0.70 | 0.680 px | **2.9 %** |
| 1.20 | 1.249 px | **4.1 %** |
| 1.80 | 1.743 px | **3.2 %** |

**AND MY FIRST CUT WAS WRONG, AND THE CONTROL IS WHAT CAUGHT IT.** rev 27's
first version resampled the profile **BILINEARLY** along the perpendicular.
Bilinear interpolation is a triangular filter, so it adds its own blur in
quadrature and the estimator inherited it: it recovered 0.70 as **1.068 px
(+52 %)**, 1.20 as 1.605 (+34 %), 1.80 as 2.113 (+17 %) — the shrinking relative
error that is the signature of a fixed blur added in quadrature. **The control
was doing its job and the ESTIMATOR was the defect.** Replaced with the
raw-pixel construction, which interpolates nothing. **A probe that measures the
optics must not add optics of its own.**

**MY FIRST THREE ROIs WERE ALSO WRONG, AND THE ISOLATION TEST REJECTED THEM.**
I picked the black trolley frame against the white bumper — a true occlusion
step between two depths, and the right *kind* of edge. It fails anyway: the
trolley member is a **BAR**, so any window tall enough to hold its step also
holds its **other** edge. Contrast was fine in **40/40** columns; the gradient
spread exceeded the isolation limit in **21–40 of 40**. **That is the isolation
test working**, and loosening it to obtain a number would have been precisely
the failure this probe exists to prevent. Hand-picked ROIs replaced by a global
hunt.

**AND THE GLOBAL HUNT IS WHERE IT STOPS.** Over the whole frame it returns
**five** straight, isolated, high-contrast candidates:

| box | fit rms | tilt |
|---|---|---|
| u 880–940, v 460–520 | 0.055 px | −0.193 |
| u 880–940, v 430–490 | 0.055 px | −0.193 |
| u 850–910, v 460–520 | 0.058 px | −0.192 |
| u 730–790, v 460–520 | 0.069 px | +0.037 |
| u 850–910, v 250–310 | 0.129 px | +0.020 |

**The estimator cannot tell an OCCLUSION step from a PAINT BOUNDARY, and that
distinction is the whole of rev 26's error.** On inspection the first three
appear to sit on the **cream/green two-tone break** — the *same class of
boundary* that made the 52 px meaningless. **Offered as my reading and NOT
relied on**; it is a question for the owner, put to him in rev 27 with the boxes
**PRINTED**. Pooling the unidentified edges gives σ **1.736 / 1.087 / 0.986 px**
across the three threshold pairs — a **76 % spread**, which is itself evidence
that the pool mixes edge classes and must not be averaged.

**SO: no σ is published for `ref_workshop.jpg`.** The probe DECLINES, and prints
why. If the owner's reading is that all five are paint boundaries, then the PSF
is **UNMEASURABLE on the admissible set in this frame**, which is a result and
not a gap — and §10.75's over-rider sizing would need a different route
entirely, since the tube's **7.9–11.7 px** bracket is dominated by exactly this
systematic.

**NOT CLAIMED:** any metre scale — a PSF is in **pixels**, and §10.72 has struck
both bumper-face constants so the nose/bumper plane has no admissible px/m; that
the tube's width is resolved; and any cross-frame comparison — the two frames'
candidate sets are different features, not a matched pair, and the probe says so.

### 10.80  rev 28 — the PSF is MEASURED: §10.79's "unmeasurable" reading REFUTED by the owner, and its 76 % spread was the 10–90 arm, not mixed edge classes

§10.79 built a validated slanted-edge estimator for `ref_workshop.jpg` and then
**correctly declined**, because an estimator cannot tell an OCCLUSION STEP from
a PAINT BOUNDARY and that is an owner reading. It offered its own reading — the
first three candidates "sit on the cream/green two-tone break", so the frame is
probably unmeasurable — and **explicitly did not rely on it**. Right to offer
it, and right not to rely on it: **it is wrong.**

**THE BOXES WERE NOT AN ANSWERABLE QUESTION, AND THAT WAS A PROBE DEFECT.**
rev 27 sent five 60×60 ROIs. **Every one of them contains more than one edge**,
so the owner was being asked to guess which edge the estimator had locked onto.
`probe_psf_lines.py` (NEW, read-only) re-runs the **shipped** `find_edges`,
recovers the fitted line each candidate actually used
(`roi`/`axis`/`lo`/`hi`/`slope`/`inter` → image coordinates) and **draws that
line**. A question that cannot be answered unambiguously is the asker's defect.

**THREE DEFECTS IN `EDGE_NOTES`, WHICH IS A HARDCODED STRING** printed verbatim
by `probe_psf_workshop.main()` while the run itself reports "candidates 35,
accepted 29". **A CLAIM IN PROSE IS NOT A GUARD, INCLUDING WHEN THE PROSE IS
INSIDE THE PROBE** — §10.67 found the identical shape inside `verify.py`'s own
comment.

1. **E1, E2 and E3 ARE ONE EDGE.** Colinear to ~0.1 px: E1's line at u 880 gives
   v 484.0 and predicts 489.8 at u 850; E3 measures **489.7**. They are three
   overlapping windows on one physical edge. "Five candidates" was never five.
2. **TWO OF THE FIVE PUBLISHED rms FIGURES DO NOT EXIST.** No candidate anywhere
   in the 35 has rms **0.069** (E4) or **0.129** (E5); the real values at those
   ROIs are 0.073/0.072 and 0.067/0.046. **Eleventh instance** of a figure
   written without being watched print — inside a probe whose own docstring
   invokes the rule.
3. **"BEST FIT FIRST" IS WRONG.** The frame's best-fitting candidate is rms
   **0.025** at roi (880,250) and is **not in the list at all**.

Clustered by a stated rule (directions within 0.030 rad; each midpoint within
1.50 px of the other's infinite line — both properties of the INFINITE line, so
an edge seen through two offset windows merges while two parallel edges do not),
the 35 candidates are **14 DISTINCT EDGES**. rev 27 named three of them.
Controls asserted: rev 27's nine E1/E2/E3 candidates land in ONE cluster; that
cluster does NOT absorb the (700/730,460) edge 20–30 px away; no two surviving
clusters are mutually mergeable.

#### The owner's reading, taken against the drawn lines

> [stated] **D1, D2, D3, D4, D6, D7, D8 and D9 are PHYSICAL STEPS. D5 is not.**

Eight of nine. **The PSF is measurable in this frame**, and D2 — rev 27's
E1/E2/E3 — is a step, not the paint break it was read as. **He excluded exactly
one edge, which hands the probe a NEGATIVE CONTROL that is his, not mine.**

#### The finding: the spread was the 10–90 arm all along

Measured on the confirmed steps, the pooled spread came out at **86 %** — WORSE
than rev 27's 76 %. **So §10.79's attribution of that spread to mixed edge
classes is REFUTED: settling the classes did not tighten the pool.**

The cause is reproducible **on a single edge**. On D2's **nine independent
member windows — the identical data**:

| arm | range on D2 | spread |
|---|---|---|
| 10–90 | 0.584 – 2.203 px | **3.77×** |
| 20–80 | 0.569 – 0.595 px | 4.4 % |
| 25–75 | 0.561 – 0.608 px | 8.1 % |

The 10–90 rise reaches into the ESF **tails**, where the profile is contaminated
by whatever else lies in the window. **On a clean synthetic the 10–90 arm
recovers a known σ to 10.7 %** — so the arm is not broken, it is
**tail-sensitive on real windows**, and the threshold SWEEP is doing exactly its
job by reporting that one arm is unreliable here.

#### THE MEASUREMENT

**σ = 0.5594 ± 0.0280 px, FWHM 1.317 px**, on the CORE arms (20–80, 25–75),
n = 32, over **four independent owner-confirmed steps agreeing to 12.4 %**:

| edge | n | σ (core arms) |
|---|---|---|
| D2 | 18 | 0.5806 ± 0.0113 |
| D3 | 6 | 0.5301 ± 0.0121 |
| D6 | 6 | 0.5405 ± 0.0202 |
| D7 | 2 | 0.5136 ± 0.0016 |

**D9 IS EXCLUDED AND THE EXCLUSION IS PRICED.** It reads σ ≈ 3.56 px, 6× every
other confirmed step. The reason is not "it disagrees": **it is the only
candidate whose edge carries periodic hardware** — the bulb string, three red
domes sitting on the rail — so the far side of its step is not a uniform
surface, which is the one thing an ESF requires. It is also n = 1. **Cost,
printed every run: +0.176 px, 32 %.** **D1, D4 and D8 could not be measured at
all** (too few ESF bins, or the monotone test rejected them) and are **named,
not silently dropped** — D1 is the frame's best-fitting edge and misses the
monotone threshold by 0.0002.

#### The negative control failed, then passed, and the premise was the defect

On the POOLED arms D5 read **0.660 against the steps' 0.736 — sharper**, and the
control FAILED. On the CORE arms it reads **0.6603 ± 0.0167 against 0.5594,
18.0 % SOFTER** — the direction his identification predicts — with an internal
scatter of only ±0.017 px, so the 18 % is far outside noise. **The 10–90
contamination was in the control too. Premise fixed, band not widened.** Fourth
time this project has found the control's own premise to be the defect.

`N2`, rev 26's fixed-axis method on the same edges, still reads **1.59× larger**
— that correction is intact.

**NOT CLAIMED:** any metre scale — a PSF is in **pixels**, and §10.72 struck
both bumper-face constants, so the nose/bumper plane still has no admissible
px/m; that the over-rider tube's **7.9–11.7 px** bracket is closed; that D5 **is**
a paint boundary — that is his identification, and this entry tests CONSISTENCY
with it, which is weaker; and any depth-resolved PSF — four edges agree to
12.4 % and that is reported as the spread, not explained.

### 10.81  rev 28 — the owner reads the counter top as CLEAN, which CONTRADICTS a live assert; and a SECOND tautology in the same chain

> [stated] **`ref_rear34.jpg` shows the counter top as CLEAN VARNISHED PLYWOOD.**

Asked with the boxes **PRINTED** and stated to be **POINTERS**, not sampling
windows — the counter top is a diagonal band and §10.76 proved no axis-aligned
rectangle large enough to sample it can avoid straddling. The pointers were
checked before they were sent: raw luma spread 27.7 % and 15.0 %, but
**0.0 % and 0.6 % once a least-squares PLANE is removed**, against a **positive
control — §10.76's own proven-straddling founding patch — reading 32.4 %.** So
the raw figure was the top's own illumination gradient, and the boxes are clean.
A gradient is absorbed by a plane; a material step is not.

**WHAT THE READING CONTRADICTS.** The shipped build paints that surface with a
settled-dust film at **mean coverage 0.548**, recomputed by a **LIVE ASSERT** at
`t1_mats.py:467` on every build, and §10.70 identified that film as
**57.1/52.6/36.6 % of the `COUNTERTAN` pedestal**. §10.76 had already found
`W_DUST_FAC_UP` **unsupported** for this surface. It is now **contradicted by an
owner reading of the only frame that shows the surface** — a stronger statement.

#### TAUTOLOGY 2 — new, and it is in the same chain as rev 27's

rev 27 found ONE tautology: the live assert's three-channel agreement, spread
5.2e-05, because `W_DUST_COL_UP` was solved collinear. **There is a SECOND.**

The founding patch's own **E-free** ratio, multiplied by `CREAM`, reproduces
`_UP_MEASURED` **exactly** — (0.6104, 0.5300, 0.4265) both ways. It must:
`_UP_MEASURED` was *derived* from that patch through the von-Kries gain, so the
patch's E-free ratio is **the assert written backwards**. **The founding patch
can never disagree with the assert it founded**, and any future test of this
chain must use §10.76's band-following CLEAN sample instead.

**THIS WAS FOUND BECAUSE MY OWN CONTROL FAILED AND I CHECKED ITS PREMISE
FIRST** — fifth instance in this project. `probe_clean_top.py`'s first cut
asserted that the founding patch reproduces §10.76's published E-free triple
(1.056, 0.884, 0.803). It FAILED at (0.989, 0.840, 0.738). **The premise was
mine, not §10.76's:** the published triple is computed from the CLEAN sample
(median sRGB 208,176,132 → **1.0562, 0.8842, 0.8027**, reproducing to 3 decimal
places), and §10.76 was right to use it. Recorded, not smoothed over.

#### What a CLEAN top predicts — and why the reading does NOT close the item

E-free top/flank, against the CLEAN sample's observed **(1.056, 0.884, 0.803)**:

| arm | predicted | error R / G / B |
|---|---|---|
| dusty `COUNTERTAN` (**SHIPPED**) | (0.8806, 0.6812, 0.4614) | −16.6 % −23.0 % **−42.5 %** |
| **CLEAN `COUNTERTAN`** (f = 0) | (0.9511, 0.7815, 0.5298) | −10.0 % −11.6 % **−34.0 %** |
| dusty `COUNTERCREAM` (the assert) | (0.9890, 0.8401, 0.7383) | −6.4 % −5.0 % −8.0 % |
| clean `COUNTERCREAM` (f = 0) | (1.1909, 1.1335, 1.1427) | +12.8 % +28.2 % +42.3 % |

* **Going clean moves every channel TOWARD the photograph** — worst channel
  42.5 % → 34.0 %. That is real corroboration of his reading from an
  independent direction.
* **But f = 0 alone does NOT reconcile it.** Clean `COUNTERTAN` is still
  **34.0 % short in B**. Removing the dust is **necessary and not sufficient**,
  so the residual sits in `COUNTERTAN` or `CREAM` — exactly where §10.76 left
  it. The implied top albedo is **(0.6519, 0.5577, 0.4637)** against
  `COUNTERTAN` (0.5870, 0.4930, 0.3060), and **the gap is almost all BLUE**.
* **THE TENSION IS REAL AND IS STATED, NOT SMOOTHED:** the arm that matches the
  photograph best is **dusty `COUNTERCREAM` at 8.0 % worst channel** — and
  `COUNTERCREAM` is the **WRONG MATERIAL** for this surface (§10.71). The dust
  is doing real numerical work under an anchor that is itself wrong. **§10.60
  rules this up-facing / vertical pair INADMISSIBLE, so none of it binds either
  way** — which is why the frame cannot supply the replacement.

#### NOT DONE, and why

**`W_DUST_FAC_UP` UNCHANGED at 0.7313. `COUNTERTAN`, `COUNTERCREAM` and
`CREAM` UNCHANGED. Nothing tuned; no geometry and no artwork moved.**
§10.76 bars a blind repair and this reading is neither of the two things it
named as sufficient. Setting f = 0 would silently discard the 57.1/52.6/36.6 %
of the pedestal §10.70 identified **and** would swap one unsupported appearance
for another, since clean `COUNTERTAN` does not match the photograph either.

**What the reading DOES do is make this the top item for rev 29**, and it
sharpens what is needed: the deadlock is no longer "is the coverage right" but
**"the coverage is contradicted and the frame cannot supply the replacement"**.
Closing it needs a `CREAM` reference or a same-class, differing-orientation
pair — still the head-on rear/front elevation from roof height.

### 10.82  rev 29 — `W_DUST_FAC_UP` is a GLOBAL lever, not a counter-top constant; a second owner reading RETIRES it

> [stated] **The ROOF in `ref_rear34.jpg` is CLEAN.**

SPEC 10.81 recorded the owner reading the COUNTER TOP as clean varnished
plywood, and **barred a blind `f = 0`** — correctly, on the evidence it had.
Its reason was that the reading is LOCAL to one surface. This entry removes
that objection by measuring what the lever actually reaches.

#### THE SCOPE, established BY EXECUTION and not by reading

`t1_mats.py:366` says *"i.e. mean coverage 0.548 on the counter top"* and the
live assert hardcodes `* 1.4`, which is `countertan`'s own `dust` input. Both
read as a counter-top quantity. **They are a global lever with the counter's
input substituted into it.** `probe_dust_scope.py` (NEW, read-only, 8 asserted
controls):

* **`W_DUST_FAC_UP` is ONE MULTIPLY node** at `t1_mats.py:937`, inside the
  file's **ONE** `WEATHER` node-tree — structure, not inference.
* It reaches **ELEVEN materials**: `T1_paint`, `cream`, `bumpercream`,
  `countercream`, `countertan`, `wheelcream`, `capwhite`, `capred`,
  `roundelred`, `calidad`, `script`. Mean coverage **0.3916** at `dust = 1.0`,
  **0.5483** at `dust = 1.4`.
* **FALSIFICATION ARM:** `T1_W_DUP=0` takes **all eleven** rows to 0.0000, not
  just `countertan`. The lever is global, measured.
* Up-facing area filmed, Newell-exact in world space: **6.3354 m² total**, of
  which `countertan` is **0.8645 m² = 13.6 %**. The largest single surface is
  **`T1_body` under `T1_paint`, 12.3697 m² of up-facing area** — the ROOF.
  **86.4 % of what this constant films is not the counter.**

This is rev 26's `CHECK THE LEVER REACHES ONLY WHAT YOU THINK`, earned on
`T1_CTAN_WEAR`, applied for the first time to this constant.

#### TWO DEFECTS IN THAT PROBE, BOTH MINE, BOTH FOUND BY THIS PROJECT'S OWN RULES

1. **C1 failed at 9.34e-09 and the premise was mine** (sixth instance). The
   probe fed itself the `dust` value read back off the node socket, which
   Blender stores as **float32**: the graph's dust is `1.3999999761581421`, so
   the shipped coverage the shader evaluates is **0.54825560066326251** against
   the assert's **0.54825560999999989**. Physically irrelevant at 1.7e-08
   relative; recorded because **it is a figure nobody has watched**. Cause
   fixed, band NOT widened.
2. **The first area estimator was wrong**, and *"when two rows agree exactly,
   suspect a bug"* is what caught it: `counter` and `counter_top` both reported
   **7.2332 m²** on a 1.750 m wide body. `counter_top` is a single n-gon
   tracing a **U-shaped plan wrapping the tail** (`CNT_Y_OUT 1.1660`,
   `CNT_Y_IN 0.8450`, 321 mm plan depth), so a fan of `|cross|` sums
   overlapping triangles. Now Newell. **The control that would have caught it
   was ADDED, and the retired method is PRICED: +50.0 % on a synthetic
   concave U-gon of analytic area 6.**

#### THE POINTER, AND THREE THRESHOLDS OF MINE THAT WERE WRONG

`probe_updust_pointer.py` (NEW, read-only, 6 asserted controls) validated the
roof pointer before it was sent — rev 28's rule that an unanswerable question
is the asker's defect.

* **Correction 1: a PLANE is the wrong model for a CROWN.** A curved panel's
  shading is quadratic, so a planar fit charges curvature to "straddle". The
  fit is now quadratic and the positive control was re-run under it — the
  proven straddler still reads **53.2 %** (planar 55.1 %). The model of
  "gradient" changed; the band was not widened to let the box through.
* **Correction 2: my first threshold would have REJECTED rev 28's own accepted
  pointer.** Under this file's statistic rev 28's box `(640,680,420,435)` reads
  **5.4 %**, and rev 28 published 0.0 %/0.6 % — **a different statistic**.
  Comparing across the two is the carried-forward-figure trap.
* **Correction 3: the second threshold was also wrong**, rejecting that same
  answered box at 3.08 × its floor.
* **The band now has NO FREE PARAMETER.** Both anchors are measured in the same
  run with the same statistic: the PROVEN straddler at **14.14 ×** its floor
  and an **ANSWERED** box at **3.08 ×**, separated by 4.6 ×. A box is accepted
  when it is closer in log-ratio to the answered anchor. The roof pointer
  `u 860–930, v 234–246` reads **3.30 ×** — **20.6 × closer to a box he
  answered than to a proven straddle** — median sRGB **(212, 186, 139)**,
  **0.00 % clipped**.

The question was sent as **multiple choice with the photograph BESIDE a render
of the current build**, with the up-face film ON and OFF — rev 26's method, and
the answered counter-top box drawn alongside in a different colour as the
owner's own scale.

#### THE RETIREMENT

`W_DUST_FAC_UP` **0.7313 → 0.0**, and this is a RETIREMENT OF A DERIVATION, not
a tune. The paragraph that solved it assumes a dirty counter top; `_UP_MEASURED`
is commented *"dirty counter top, de-illuminated"*. **Two owner readings a
revision apart, on two different surfaces, withdraw that premise.**

* **The old derivation assert is RETIRED, NOT WIDENED.** At `f = 0` it misses by
  **0.2335**, a hundredfold — it compares a clean top with a measurement of a
  dirty one, and a band admitting both tests nothing. SPEC 10.59's shape: the
  owner withdrew the target, the probe stays as a labelled catcher.
* **Replaced by a narrower assert that CAN fail** — `_f_up` must be exactly 0 —
  plus a road-film-untouched assert. **FALSIFIED IN SEVEN ARMS, all watched:**
  restoring 0.7313 in source FIRES; `T1_W_DUP=0.7313` still renders the retired
  arm cleanly; `COUNTERTAN` R **+0.020** FIRES; `COUNTERTAN` B **−0.020** FIRES
  (a max-guard would have been blind — rev 27's lesson held); `W_DUST_FAC_TOP`
  0.35 → 0.40 FIRES; and both new `_RETIRED_VALUES` rows FIRE as FAILs when
  their literal is republished unstruck in the frozen front matter.
* **The SPEC 10.76 catcher is DELIBERATELY RE-BASELINED** to
  **(−0.023400, −0.037000, −0.120500)**, band UNCHANGED at 2e-3. rev 23's
  roof-hole precedent. At `f = 0` the prediction IS `COUNTERTAN`, so the
  residual is exactly `COUNTERTAN − _UP_MEASURED`: **the catcher is now
  STRONGER**, watching those two constants with no dust term between them. The
  sign assert still holds in all three channels.
* **Two `_RETIRED_VALUES` rows**, not one: `0.7313` and `mean coverage 0.548`.
  rev 25's rule — a retired value re-expressed in another form is invisible to
  a substring guard, and the answer is another ROW.
* **The road film is untouched.** `fup` enters only through `MAXIMUM(flow, fup)`
  and through `dsel`, so at 0 both collapse to the road branch. The tide line,
  the rocker and the tyres do not move.

#### WHAT THIS DOES NOT CLAIM

* **It does NOT fix `COUNTERTAN`.** SPEC 10.81's arithmetic stands: a clean top
  is still **34.0 % short in B**. Removing the film was **necessary and is not
  sufficient**. The residual is still a `COUNTERTAN`/`CREAM` problem and `CREAM`
  is still this project's largest open constant.
* **It asserts more than two readings strictly support** — that NO up-facing
  surface carries settled dust. The **front bumper top, the rim barrels and the
  hub caps** are filmed by the same node and **nobody has been asked about
  them**. Named, not hidden. A per-material constant would be AUTHORED; this is
  the minimal change consistent with both readings.
* **SPEC 10.70's measurement stands; its status changes.** The 57.1/52.6/36.6 %
  of the `COUNTERTAN` pedestal that film carried was correctly measured. What is
  withdrawn is the claim that it belongs on the vehicle. Any future
  `COUNTERTAN` solve must re-derive `k` — **never carry the old secant gain**.
* **THE SHADING HAS MOVED, so `rev25_hero34f.png` NO LONGER PHOTOGRAPHS THE
  CURRENT BUILD.** Geometry and artwork are untouched and every guard figure is
  identical, but the up-face film is gone from eleven materials. **A hero
  re-shoot is OWED and was NOT done in rev 29.** Stated rather than left to be
  discovered.
* Observed and deliberately NOT converted into a claim: with the film removed
  the model's roof reads **cooler**, and the photograph's roof is warm cream.
  The two are under **different lights** (studio rig vs a palapa), so SPEC
  10.21 bars the comparison. What can be said is directional: **an unsupported
  warm film was partly concealing the open `CREAM` / `T1_paint` question, and
  removing it makes that question more visible rather than less.**

#### PROCESS — a new rule, and I broke it TWICE in the hour I wrote it

* **A `git checkout <file>` used to undo a falsification arm destroyed
  unrelated uncommitted work in the same file — TWICE.** First it wiped three
  edits to `t1_mats.py`; then, twenty minutes after this rule was written into
  this very entry, it wiped this entry itself out of `SPEC.md`. Both recovered
  in full, both recorded rather than quietly redone.
  **NEW RULE: COMMIT BEFORE FALSIFYING.** A falsification arm edits the tree,
  and the undo must be narrower than the change you are protecting. Prefer a
  targeted `sed` reversal, or commit first and let `git checkout` be safe.
  Writing a rule down is not the same as having it.
* **MY FIRST FALSIFICATION OF THE TWO NEW `_RETIRED_VALUES` ROWS DID NOT FIRE,
  AND THE GUARD WAS RIGHT.** I appended the stray literals to the END of
  `SPEC.md`, which sits inside a `### 10.xx` body — a region
  `_retired_value_drift` **deliberately and correctly** does not scan, and says
  so in its own stated ceiling. **The control's premise was mine, seventh
  instance.** Re-run in the frozen front matter, both rows fire as FAILs.
* **A THRESHOLD IS A PROBE TOO** — three of mine were wrong before one was
  right, and the one that is right has no free parameter because it is
  calibrated against a box the owner had already successfully answered.

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
~~**nine flower heads** (five upper, four lower — counted off `ref_side.jpg`)~~
**RETIRED by the owner in rev 39 (§10.97.11): the board carries TEN flower heads
plus one part head cut by the right strip.** `lid_gen.py` has built ten since
rev 10; his rev-8 count of nine was never checked against the build until rev 39
put the rectified board to him, and he answered TEN. The build was right,
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

### 10.83  rev 30 — THE FRONT OVER-RIDER IS MEASURED AND BUILT: a scale on the nose/bumper plane at last, and rev 29's proposed route refuted on the way

**§10.75's item, open since rev 26 and NOT ATTEMPTED in rev 28 or rev 29, is
closed for the BAR.** It is closed by measuring somewhere nobody had looked,
not by loosening anything. **Geometry moves this revision** — the first time
since rev 23.

#### What rev 30 REFUTED before it measured anything

- **THE OCCLUSION FRAMING IS WRONG.** §10.75 recorded the foreground trolley
  occluding the bumper blade's lower edge "in 5 of 8 columns", and the rev-30
  brief made asking which columns are clean the first task.
  `probe_orb_blade.py` (NEW, read-only) settles it **BY GEOMETRY instead**: the
  rail's top edge fits a straight line to **rms 0.289 px over 65 columns**
  (`v = −0.3053 u + 817.675`) and lies **6.6–61.3 px BELOW** the blade's lower
  boundary in **every** clean column of the tube's own run. It does not occlude
  them. rev 26's figure was measured on a WIDER set running past `u ≈ 285`,
  where the rail genuinely does cross. **The owner was not asked a question
  measurement had already answered.**
- **rev 29's SCALE-FREE RATIO IS REFUTED AS A FIX.** Swept over seven luma
  thresholds the tube/blade ratio reads **±12.8 %**, *between* the tube's
  ±16.8 % and the blade's ±9.0 %. The systematic does not cancel. **C5 FAIL,
  reported as a FAIL and not widened.**
- **THE REASON is in the edge widths**, priced against the frame's own
  yardstick — the trolley rail's edge at **1.76 px, 1.23× the ideal step
  predicted by §10.80's σ = 0.5594.** That is an **independent corroboration of
  rev 28's PSF from a different edge class**, and it was not sought; it fell
  out of the control.

| boundary | 10–90 width | × rail |
|---|---|---|
| blade TOP (green→cream) | 1.86 px | **1.06 — a real edge** |
| tube TOP (green→cream) | 2.26 px | **1.28 — a real edge** |
| tube BOT | 4.33 px | 2.46 — a rolloff |
| blade BOT (cream→ground) | 5.27 px | 3.00 — a rolloff |

#### THE MEASUREMENT: a different station, not a different method

The tube runs the **whole way across the nose**, and at `u 385–460` it passes
**directly beneath the headlamp aperture** — the one locked ruler in the frame.
Same station, measured vertically, so **REF §9's "lateral scale varies by more
than 2:1" does not bite**: that warning is about LATERAL scale on a curved
panel. rev 26 measured at `u 248–272` only because that is where box A had been
drawn.

There the tube is isolated against green above and below, its top edge is a
real edge, and its apparent thickness holds to **±5.5 % over 76 columns**
against rev 26's ±19 %.

#### THE OWNER'S TWO ANSWERS, and what each did

Asked with every crop box printed, every fitted line drawn, the photograph
shown beside a render of the shipped build, and **both boxes stated to be
SAMPLING WINDOWS rather than pointers — different from rev 28 and rev 29 and
said so on the figure** (`mark_rev30_q.py`, `rev30_q_overrider.png`):

| | question | answer |
|---|---|---|
| **Q1** | where does the tube END — at the cast-shadow line, or does the dark band belong to it? | **[stated] CAN'T TELL** |
| **Q2** | where is the headlamp aperture's LOWER RIM — the ruler? | **[stated] the THIN DARK LINE → vertical extent 71.11 px** |

**Q1's "can't tell" barred taking my own lean**, which was arm 1, and it is
recorded that it barred it. The bracket was 9.86 px to 14.98 px — a factor of
1.52, which changes the part and not a decimal.

#### HOW Q1 WAS CLOSED WITHOUT AN ANSWER: a bound, not an estimate

`probe_orb_hoop.py` (NEW, read-only). The tube **turns down and back in a
rounded hoop end at `u ≈ 468–490`, which SPEC has never recorded.** Through the
bend a horizontal chord crosses the tube and **both ends of that chord are
LATERAL silhouettes** — neither is the underside the owner could not read.

For a tube of diameter D whose image axis has **any** slope s,
`W_h = D·√(1+s²) ≥ D`. **Every** horizontal chord on the bend is therefore an
upper bound on D, and the smallest is the tightest. **No fit, no derivative, no
slope model and no free parameter enters this.**

- smallest chord over 15 rows: **10.38 px → D ≤ 10.38 px**
- arm 1, **9.86 px — ADMISSIBLE**, 0.52 px under the bound
- arm 2, **14.98 px — EXCLUDED**, 44 % over it

**The question is closed from the other side: by refuting one arm, not by
choosing between them.** **NOT CLAIMED:** that the dark band IS a cast shadow.
That is still open, and it does not matter for the diameter.

#### FOUR DEFECTS OF MY OWN, every one caught by a control and recorded

- **TWO ESTIMATORS DIED IN `probe_orb_hoop.py` AND NEITHER IS PUBLISHED.** A
  slope-corrected chord removed only **14 %** of the slope dependence and
  **over-corrected**; a parameter-free min-distance construction between the
  two fitted silhouettes failed C1 and C2 as well (D drifts 8.4 → 10.6 px
  across the bend). Diagnosis stated rather than tuned: through a bend the two
  curves stop being the two sides of one tube, and **the quadratic's derivative
  at the ends of its own range is the weakest quantity in the construction.** A
  third estimator was not attempted. **The bound needs none.**
- **TWO NULL PATCHES WERE WRONG BEFORE ONE WAS RIGHT.** The first clipped the
  two-tone V (sd 45.9). The second clipped it too (sd 37.6) — and I had
  **PRINTED its flatness without GATING on it**. *A flatness figure you do not
  test is not a control.* The third is gated: sd 2.83, 0 of 50 rows.
- **MY OWN GUARD WAS A TAUTOLOGY AND MY OWN FALSIFICATION ARM CAUGHT IT.** The
  first `verify.py` row compared the MESH against `t1_detail.BAR_RISE` — the
  very constant that builds the mesh. Adding 3 mm to it moved both together and
  the row read **0 fail**. §10.81's second tautology, and rev 24's "the false
  claim was inside the guard itself", now a **third** time. Fixed by **freezing
  the derivation as literals in `verify.py`** and asserting the source against
  them as a separate arm.
- **THE 10.83 ROW FIRED ON ITS FIRST RUN AND THE ROW WAS RIGHT.** Its sampling
  window was `x > 2.132`, which keeps only the blade's outer face —
  `BUMP_PROFILE` reaches its greatest OUTWARD extent at `up = +0.0210` and its
  **topmost** point at outward 0.000, so that window read 0.5230 where the
  blade tops out at 0.5360. **WINDOW FIXED, BAND UNTOUCHED.**

#### WHAT IS BUILT, and at what grade — every number carries its provenance

| quantity | value | grade |
|---|---|---|
| tube / aperture-vertical | **0.1387**, ±5.5 %, 76 columns | MEASURED, scale-free |
| upper bound on that ratio | **0.1460** | BOUNDED, model-free |
| tube top above blade top | **38.7 / 71.11** of the aperture | MEASURED, scale-free |
| headlamp aperture | **0.1800 m** | **CATALOGUE — SPEC 10.72's STRUCK CLASS. TAGGED.** |
| `BAR_DIA` | 24.97 mm | CONSEQUENCE of the anchor |
| `BAR_RISE` | 97.96 mm | CONSEQUENCE of the anchor |
| standoff in x | outer faces coplanar at 2.1403 | **A CHOICE, not a reading** |
| lateral extent, hoop radius | `BAR_HALF_Y = 0.600` | **E — shape from the photograph, dimension NOT** |

`BAR_DIA` and `BAR_RISE` are written in the source **as the ratio times the
anchor, never as bare numbers**, so that replacing the anchor moves them
proportionally and fires the guard. Falsified in **five arms**: `BAR_RISE`
+3 mm FIRES (2 fails), the bar deleted from `build.py` FIRES, `BAR_RATIO` →
the model-free bound FIRES (2 fails), `APERTURE_M` → 0.190 FIRES (3 fails),
control 0 fail / 0 warn.

#### NOT BUILT, deliberately — and §10.75 IS CORRECTED

**§10.75 describes the vertical post (its box C) as "the vertical post at the
vehicle's centreline". THAT IS REFUTED.** *[DOWNGRADED TO **UNDECIDED**, rev 31,
SPEC 10.84 -- the two terms of this refutation are at DIFFERENT DEPTHS: the apex
is on the nose skin, the post stands in the bumper plane forward of it by a
standoff this very section grades "A CHOICE, not a reading", and the owner
confirmed in rev 31 that the post is bar-to-blade only, standing away from the
body panel. The whole offset is 54.0 px and the parallax sign is unestablished
at 1.38 sigma. The post stays UNBUILT either way, but this claim is no longer
settled and must not be listed as settled.]* The centreline is the two-tone V apex
at **`u = 311.5`** (REF §9) *[THE ANCHOR IS CORRECTED: SPEC 10.85 (rev 31b) shows
311.5 is the V's RIGHT ARM's occlusion point at the bar, not the apex; the apex
is at `u = 288.8 ± 3 px`. SPEC 10.86 (rev 32) then re-ran §10.84's ARM 2 on the
corrected anchor and found the control it reported as a clean FAILURE would now
PASS — see 10.86, which also names the two terms that arm never priced. The
claim stays UNDECIDED.]*; the post's own columns are **357–374** *[RE-MEASURED,
rev 32: `u 355–377` by cream-run scan over rows 676–700, centre 366. §10.75
printed 357–374 as a POINTER and its own text says no number was to be taken
from it; rev 30 took one anyway. The pointer is VINDICATED to within 2 px — the
defect was the process, not the number.]*. It is not
on the centreline and it never was. Its lateral position can be bracketed only
between the centreline and the near headlamp, which is **not a measurement**,
and REF §9 bars any lateral metre figure on this panel. **Building it at a
refuted position would be worse than leaving the gap named**, so the post is
NOT built and is carried as the item's remainder.

**Also still open and named:** the depth standoff biases the ratio HIGH by an
amount whose SIGN is known and whose SIZE is not; and no in-service frame shows
the nose, so this whole entry is **WORKSHOP-STAGE** under §10.75's scope ruling
and is deleted by one line in `build.py` if one ever appears.

---

### 10.84  rev 31 — THE POST'S BLOCKER IS §10.83's OWN REFUTATION, AND THAT REFUTATION COMPARES TWO DEPTHS: status corrected to UNDECIDED, and the brief's route refuted before it was spent

**NO GEOMETRY MOVES THIS REVISION.** Nothing is built, nothing is retuned, no
constant changes. What changes is the STATUS of one claim that was recorded as
settled, and the disposition of one route the rev-31 brief proposed.

#### The brief's route was tested at its first link, and the link broke

The rev-31 brief proposed single-view metrology on `ref_workshop.jpg` using the
WORKSHOP's own architecture — masonry courses, roof beams, columns — with the
bumper top at 0.348 m as the known height, to recover the post's LATERAL
position. It asked for a ruling BEFORE the revision was spent. **The ruling is:
it will not close, and the reason is not the architecture.**

Any such chain must reach the VEHICLE's fore-aft direction. `probe_orb_post.py`
(NEW, read-only) tries to read it off the vehicle's own long edges. Five are
traced; three pass an rms gate:

| edge | n | slope | rms |
|---|---|---|---|
| drip rail | 91 | +0.0075 | **0.091 px** |
| counter lower edge | 116 | −0.1876 | **0.096 px** |
| belt break, forward | 96 | −0.1943 | 0.648 px |
| counter upper edge | 118 | −0.0036 | 2.718 px — **EXCLUDED, not a line** |
| rocker, mid run | 71 | −0.7979 | 1.979 px — **EXCLUDED, not a line** |

Their pairwise intersections land at **u = +1529, +1284 and −5843** — a spread
of **7 372 px across a 1 200 px frame** — and they **change side**. C1 FAIL,
C3 FAIL.

**AT 0.09 px RESIDUALS THIS IS NOT A TRACING FAILURE.** Those edges are
genuinely not parallel on the real vehicle, and this repository already says
why: `t1_mats.z_belt(x)` makes the belt a SLOPED line, and the roof carries its
own rake and crown. **There is no single fore-aft vanishing point on this
vehicle to recover.** The building's lines would calibrate cleanly, but they
give the BUILDING's frame; transferring it to the vehicle needs the vehicle's
YAW, whose only route is the wheel–ground contacts, and the foreground trolley
occludes the front one. That is an extra unmeasured link the brief's framing
does not carry.

#### §10.83's refutation of "post at the vehicle's centreline" COMPARES TWO DEPTHS

§10.83 refuted §10.75's phrase by setting the post's own columns (357–374,
centre **365.5**) against the two-tone V apex at **u = 311.5**, which REF §9
gives as the centreline. **The V apex is on the NOSE SKIN. The post stands in
the BUMPER plane, forward of it by a standoff §10.83 ITSELF grades "A CHOICE,
not a reading".** Under perspective a centreline point translated forward does
not keep its column, so the nose-skin centreline column and the bumper-plane
centreline column are different numbers — and the refutation used one as if it
were the other.

The entire refutation is an offset of **54.0 px**. The sign of the unpriced
parallax decides whether that offset is real or manufactured.

**THE SIGN COULD NOT BE ESTABLISHED, AND THAT IS REPORTED AS A FAILURE RATHER
THAN LEANED ON.** The only two centreline features available at different
depths are the VW roundel (**u = 306.0**) and the V apex (**u = 311.5**). They
differ by **+5.5 px** against REF §9's own **±4 px** band on the apex —
**1.38 σ**. C4 FAIL.

**STATUS CORRECTED: §10.83's "REFUTED" on this one claim becomes UNDECIDED.**
It is NOT hereby claimed that the post IS on the centreline. It is claimed that
the measurement which ruled it out cannot bear the weight put on it, and that
the rev-31 prompt's "already settled — do not re-open" listing of it is wrong.
**The post remains UNBUILT either way**: nothing here supplies a lateral
position, and REF §9 bars a lateral metre figure on this panel.

The `_RETIRED_VALUES` row for the phrase is **KEPT** — the phrase still must not
be re-quoted as a live value to build from — and only its stated REASON is
corrected. Retiring it was right; the justification was not. **The corrected row
was watched FIRE**: injected into a non-exempt SPEC section the guard reads
1 fail against the clean tree's 0.

#### A FIFTH TAUTOLOGY CLASS, named: a guard is not the only thing that can be circular

§10.83's refutation is not a guard, so the three previous tautology findings do
not cover it. It is the same defect one level up: **a REFUTATION whose two terms
are not commensurable measures nothing.** The rule this earns is stated with the
others: *two features at different depths are not two readings of one quantity.*

#### THE ONLY SURVIVING ROUTE, and it is blocked on a reading, not a calculation

The near end of the bar turns down in a rounded hoop (§10.83, `u ≈ 468–490`).
**At the FAR end there is a cream feature at `u ≈ 203–232`, `v ≈ 626–702`, which
SPEC has never recorded.** If it is the bar's own mirror-image end, then the
bar's two ends BRACKET the post, and the post's position becomes a **SCALE-FREE
FRACTION of the bar's half-width** — needing no calibration, no ground plane, no
yaw and no standoff, and inheriting `BAR_HALF_Y`'s existing grade E rather than
adding a new unmeasured lateral choice. That is the one route that survives
everything above, and it cannot be started until the feature is classified.

Asked on `rev31_q_post.png` (`mark_rev31_q.py`, NEW, read-only), photograph
beside a render of the current build, every crop box printed on the figure and
on the console, and **every box stated to be a POINTER — none is a sampling
window, because rev 31 takes no samples from any of them**, which is the
converse of rev 30's declaration and is said for the same reason.

#### A HERO WAS OWED TWICE OVER AND IT IS ALREADY SHOT

`rev30_hero34f.png` (4800×3200, on his disk, timestamped ~10 h AFTER
`NEXT_CONTEXT_PROMPT_rev31.md`, which is why that prompt does not know of it)
**is a render of the rev-30 build**, established by content and not assumed:

- it carries the over-rider bar **and its hoop end**, a member present in no
  revision before rev 30; `rev25_hero34f.png` at the same crop is a clean
  negative control — bare blade, nothing above it;
- **CONTROL:** the backdrop is **bit-identical** between the two frames (max
  channel difference **0**), so the 11.74 % of differing pixels is signal;
- the difference is **41.22 % inside the silhouette against 0.21 % outside**,
  and concentrates on UP-FACING surfaces — cab roof mean 9.94, counter top 5.58,
  against the vertical flank's 2.64 — which is rev 29's split up-face deposit,
  corroborating the shading independently of the geometry.

**MY FIRST SEAM TEST WAS ON THE WRONG AXIS AND ITS CONTROL KILLED IT, PRICED
HERE RATHER THAN DELETED.** It searched for VERTICAL seams; `hero.py` strips in
ROW space, so seams are HORIZONTAL. It also fired hardest at `x = 2086`, which
is not a strip boundary at all — it was reading real image content — and a
positive control then showed it could barely see a full 1-code step (3.14 →
3.66). Re-run on rows, over subject rows only, with a graded control:

| | worst \|z\| | median |
|---|---|---|
| **OBSERVED** | **2.97** | 0.93 |
| positive control, +1.00 code per seam | 17.36 | 7.34 |
| positive control, +0.25 code per seam | 5.17 | 2.00 |
| positive control, +0.10 code per seam | 3.52 | 0.78 |

**The observed frame sits below the +0.10-code control.** Any seam is under a
tenth of a code value. **CEILING: ~0.1 code values**; this is a different metric
from `hero.py`'s own stitch-time figure and is NOT comparable to rev 25's 1.91.

#### A PROCESS DEFECT OF MY OWN, recorded because it destroyed work

**I used `git checkout SPEC.md` to undo a test injection in a file that carried
UNCOMMITTED work**, and it discarded this entire section and the §10.83
correction along with the injection. Both had to be rewritten. The rule:
*never revert a file with `git checkout` to undo a falsification arm — commit
the real work first, or the arm eats it.* This is why the arm above is run and
reported AFTER the commit that lands the text it tests.

#### HIS TWO ANSWERS, given while the revision was still running

| | question | answer |
|---|---|---|
| **Q1** | what is the cream feature at the bar's far end, `u 203–232`? | **[stated] "Appears to be covering the bumper, the post, and the far end of the bar."** |
| **Q2** | is the post bumper-plane only, or a stay running back to the body? | **[stated] "bar to blade only, much like the view of the other bar which shows us a triangular bar extending from the bumper upwards and away from the body panel"** |

**NEITHER ANSWER IS THE ONE THE OPTIONS OFFERED, AND BOTH ARE BETTER THAN THE
OPTIONS.** Q1 was offered as a four-way classification; he read it as a
SUPERPOSITION of three members, which none of (a)–(d) expresses. Re-examined at
×10 against his reading, the frame agrees: a cream diagonal runs from the bar
down to an apex at about `(u 240, v 683)`, and the dark wedge beneath it is not
a member at all but **the green body panel seen through the gap between brace,
bar and blade**. It reads as a brace, not as a hoop and not as a plain post.

**WHAT THIS ESTABLISHES THAT SPEC DID NOT HAVE:**

1. **THE BAR'S FAR END IS PRESENT** and runs essentially to the bumper's far
   corner — so the bar spans the full blade, and its two ends DO bracket the
   post. The scale-free-fraction route is ALIVE.
2. **ITS COLUMN IS CONFOUNDED.** The far end is superposed with the bumper
   corner and with a brace inside a ~29 px blob, so the endpoint carries that
   blob as its uncertainty — it is not a clean silhouette like the near hoop.
   **This is a bound on the route's precision, stated before the route is run.**
3. **THERE IS BRACE STRUCTURE AT THE FAR END** — a triangular member from the
   bumper going up and AWAY from the body panel. SPEC has never recorded it.
4. **THE POST IS BUMPER-PLANE ONLY.** This is the load-bearing one.

**Q2's ANSWER CONFIRMS §10.84's STATUS CORRECTION FROM THE OTHER SIDE.** The
argument above was that §10.83 compared two features at different depths, and
that the sign of the parallax could not be priced. A stay running back to the
body would have made the post's depth ambiguous and the whole objection soft.
**He rules it bar-to-blade only, standing away from the body panel — so the post
is DEFINITELY in the bumper plane, and the depth difference between it and the
nose-skin V apex is DEFINITELY the bumper standoff, which is DEFINITELY
non-zero and is graded "A CHOICE, not a reading".** The parallax is therefore
not merely unpriced but **certainly present**. UNDECIDED is confirmed by his
reading, not only by my failure to establish a sign.

**NOT CLAIMED**, and left for rev 32: that the far-end brace and the middle post
are a SYMMETRIC PAIR; that the middle post is itself triangular in the same way;
that the near hoop has no brace hidden behind the corner. The naive midpoint of
the two bar ends is not the projective one and no midpoint is computed here.

---

### 10.85  rev 31b — REF §9's "two-tone V apex" IS NOT THE APEX: it is the V's RIGHT ARM disappearing behind the over-rider bar, and the anchor is 22.7 px off

**THE OWNER CAUGHT THIS FROM THE FIGURE.** Shown `rev31_q_post.png` he said the
apex marking did not look right. He is correct, and the defect is in
**REF_MEASUREMENTS §9**, not in the figure's drawing code — which means it is
upstream of §10.83, §10.84 and everything else anchored on that point.

REF §9 publishes:

```
two-tone V apex (centreline)    (311.5, 669)     ± 4 px
```

**At ×8 the V's two arms have NOT converged at `v = 669`** — the cream wedge is
still ~30 px wide there — **and the over-rider bar's top edge sits at
`v = 672.5`**, three pixels lower, occluding everything beneath. The published
point is where the V's **RIGHT ARM** goes behind the bar.

#### The construction — projective, parameter-free

Both arms are cleanly visible ABOVE the bar. `probe_v_apex.py` (NEW, read-only)
traces each as a cream→green boundary over **42 rows**, fits each as a line, and
intersects them. **Two straight lines meeting at a point in 3D project to two
straight lines meeting at the image of that point**, so the crossing IS the
vertex's image — no scale, no calibration, no depth.

| | value |
|---|---|
| LEFT arm | 42 rows, `du/dv` **+0.2502**, **rms 0.112 px** |
| RIGHT arm | 42 rows, `du/dv` **−0.5841**, **rms 0.806 px** |
| arms cross at | **(288.8, 701.1)** |
| bar top edge, u 280–340 | **v = 672.5** (n = 60) — the crossing is **28.6 px BELOW it** |
| **COLUMN SHIFT vs REF §9** | **−22.7 px** |

#### C3, the null, is what proves the diagnosis rather than merely asserting it

REF §9's point is **3.98 px** from the RIGHT arm and **30.75 px** from the LEFT.
**A vertex is equidistant from both arms — zero from each.** A point 4 px from
one and 31 px from the other is a point ON THAT ARM. The published "apex" is the
right arm's occlusion point, and its own ±4 px band is exactly the distance it
sits from the line it lies on.

#### THE BAND IS SET BY C5, AND THE BOOTSTRAP'S ±0.2 px IS A FALSE PRECISION

The crossing lies **38 rows below the deepest traced row — an extrapolation
0.93× the length of the traced span** — and is valid only while the arms stay
straight. A bootstrap over the traced samples returns **±0.2 px**; *that number
prices scatter and not the straightness assumption, and publishing it would be
a false precision.* **C5 splits the band and re-crosses:**

| | crossing u |
|---|---|
| upper half, far from the tip | 287.4 |
| lower half, near the tip | 290.3 |
| **half-to-half disagreement** | **3.0 px** |

**PUBLISHED: `u = 288.8 ± 3 px`, SYSTEMATIC**, the band set by C5. The RIGHT arm
carries a real quadratic term (`+0.00450 px/row²`, lin rms 0.806 → quad 0.548);
if it continues through the extrapolation the worst case is **~7 px**. The
−22.7 px shift is far outside every one of those bands **and outside REF §9's
own ±4 px**.

#### WHAT THIS DOES AND DOES NOT DO TO §10.84

The post's offset against the corrected anchor is **+76.7 px**, not the +54.0 px
§10.84 priced. **THAT MAKES §10.83's REFUTATION LOOK STRONGER ON THE RAW NUMBER,
AND IT CHANGES NOTHING.** §10.84's objection was never about the size of the
offset — it was that **the two terms are at different depths**, the apex on the
nose skin and the post in the bumper plane, across a standoff graded "A CHOICE,
not a reading". Correcting one term's column does not make the two commensurable.
**§10.83's centreline claim stays UNDECIDED.**

**Only the COLUMN is published.** The T1's two-tone V is radiused at the tip, so
the straight-line crossing sits BELOW the real rounded vertex; its ROW is not a
measurement and is not published.

#### THE RULE THIS EARNS

**A FEATURE NAMED IN A REFERENCE FILE IS A PROBE TOO — CHECK THAT THE NAMED
POINT IS THE THING THE NAME SAYS.** REF §9's point carried the word "apex" and a
±4 px band through nine revisions and into two SPEC sections, and it was a point
on an arm. **AND: AN OCCLUDER ADDED TO THE MODEL LATER CAN INVALIDATE A READING
TAKEN BEFORE IT** — the bar that hides this vertex was measured and built in
rev 30, from the same frame, without anyone noticing it lands on the anchor.

---

### 10.86  rev 32 — THE SWEEP OF §10.85's ANCHOR, AND THE POST'S CROSS-RATIO ROUTE RULED OUT BEFORE IT WAS SPENT

**NO GEOMETRY MOVES THIS REVISION.** Nothing is built, nothing is retuned, no
constant changes, no artwork changes. What moves is the STATUS of three stale
carriers of a corrected anchor, one stale control literal, and one route.

#### The sweep §10.85 did not do

§10.85 corrected REF §9's V-apex anchor in place from `u = 311.5` to
`u = 288.8 ± 3 px` and wrote in REF that *"everything in this file that used
311.5 as the centreline inherits this."* It did not chase the consumers. rev 32
grepped the whole tree. **FIVE carriers, of which FOUR were live:**

| where | defect | disposition |
|---|---|---|
| `REF_MEASUREMENTS.md` §9 line | the anchor itself | already corrected by 10.85 |
| `REF_MEASUREMENTS.md` §9 absolute-height block | **`V-SWAGE APEX ~0.49 m` consumes BOTH of 311.5's coordinates** | WITHDRAWN as a reading, replaced by a BRACKET, no new number published |
| `SPEC.md` §10.75's in-place annotation | **still read "REFUTED" a whole revision after §10.84 downgraded it, AND on the wrong anchor** | corrected in place |
| `t1_detail.py` above `overrider_bar()` | same two defects, in shipped source | corrected in place, original kept as the record of what rev 30 believed |
| `probe_orb_post.py:58` | `V_APEX_U = 311.5` | **deliberately KEPT**, corrected anchor added beside it — see below |

**THE ABSOLUTE-HEIGHT CONSUMER IS THE SUBSTANTIVE ONE.** REF §9 publishes
*"V-SWAGE APEX, on the centreline ~ 0.49 m above ground (49 px above the bumper
top **at the same image x, hence the same depth**; centreline scale ~355 px/m)"*.
It consumes 311.5 **twice**:

- **The ROW.** The 49 px is `718 − 669`, and 669 is the row of the point §10.85
  showed is not the apex. The arms have not converged at 669, so the true apex
  lies BELOW it; their straight-line crossing is at `v = 701.1`, and because the
  V is RADIUSED at the tip the painted apex lies ABOVE that crossing. So
  `669 < v_apex < 701.1` — **16.9 to 49 px above the bumper top, ≈0.40–0.49 m
  above ground. THE PUBLISHED 0.49 m IS THE TOP OF A BRACKET, NOT ITS CENTRE.**
- **The COLUMN, and this is worse.** *"at the same image x, hence the same
  depth"* pairs the apex with the bumper-top reading **because they share a
  column**. They shared 311.5. The apex is at 288.8, so the premise of the
  pairing is gone.

**NO REPLACEMENT NUMBER IS PUBLISHED.** Re-deriving it needs the blade's top
boundary read at `u = 288.8`, and **the blade and the V-swage are BOTH CREAM**,
so a cream-run scan cannot find that boundary. The gap is named, not filled.

**SWEEP RESULT, NEGATIVE AND WORTH RECORDING:** the other three entries in REF
§9's absolute-height block do NOT consume 311.5. The V-arm/body-corner entry is
anchored on the flank belt line; HEADLAMP CENTRE is anchored on the V ARM at the
headlamp's own x `(419, 524)`; INDICATOR CENTRE derives from the headlamp. Those
three inherit the 422 px/m near-side scale and its >2:1 warning, which is a
SEPARATE and older caveat. **They do not inherit §10.85.** And `422 px/m` itself
is CONSUMED NOWHERE in the tree — it is named once, in rev 29's carry-forward,
and only to warn against it.

#### §10.84's ARM 2 would now PASS, and that is a defect finding, not a result

§10.84 tried to price the nose-skin-to-bumper-plane parallax SIGN from the only
two centreline features at different depths, and reported a clean failure:
roundel `306.0` vs apex `311.5` = `+5.5 px` against REF §9's `±4 px` — **1.38 σ,
C4 FAIL**. On §10.85's corrected anchor the same two terms read

    288.8 − 306.0 = −17.2 px  →  5.73 σ on the ±3 px SYSTEMATIC band,
                                 and it still clears 10.85's ±7 px worst case.
    AND THE SIGN FLIPS: the apex was RIGHT of the roundel, and is now LEFT.

**IT IS STILL NOT LEANED ON, AND THE REASON IS A DEFECT IN THE ARM ITSELF.**
Re-reading ARM 2 now that its gate might pass shows two terms it never had:

1. **NO DEPTH-ORDERING TERM.** It prints a column difference and calls that a
   sign. Which of the roundel and the apex is nearer the camera is never
   established, and without it a significant column difference is a MAGNITUDE,
   not a DIRECTION.
2. **NO HEIGHT TERM.** The two features are ~150 px apart in `v`. A centreline
   point's image column depends on its HEIGHT as well as its depth unless the
   camera is level and unrolled, and nothing in this repository establishes that
   it is.

**A CONTROL THAT FAILS CAN HIDE THE DEFECTS DOWNSTREAM OF IT.** Both defects
were present in rev 31 and neither was visible then, because C4 failed and
nothing downstream of it ever ran. That is a new rule and it is the reason
§10.85's *"it changes nothing for 10.84"* was true about the OFFSET and wrong
about the ARM.

`probe_orb_post.py`'s `V_APEX_U = 311.5` is **deliberately left in place** so
the file keeps reproducing what rev 31 published; **a probe that cannot
reproduce its own published result is not a record.** The corrected anchor is
added beside it and ARM 2 is re-run on both, in one output.

**STATUS UNCHANGED: §10.83's centreline claim stays UNDECIDED.** Nothing here
supplies a lateral position. The `_RETIRED_VALUES` row is KEPT for the third
time and only its stated reason is corrected — the offset is **76.7 px**, not
54.0.

#### The post: the CROSS-RATIO route, and the ruling the brief asked for

The rev-32 brief asked for the post as a **FRACTION of the bar's half-width**,
for the transverse VP to be bounded or constructed, and for a ruling on whether
it would close **before** the revision was spent. `probe_orb_xratio.py` (NEW,
read-only) is that ruling.

**THE CONSTRUCTION IS THE RIGHT SHAPE, AND IT REPAIRS §10.84 AT THE ROOT.** Four
points lie on ONE line in the BUMPER PLANE — bar far end, far strut, near post,
bar near end. Four collinear points carry a projective invariant, so this needs
**no vanishing point, no scale, no depth and no camera model**, and every one of
the four is in the SAME plane. rev 31's owner reading is what guarantees that:
*[stated]* the post is "bar to blade only … extending from the bumper upwards
and away from the body panel." **There is no cross-depth term left to price.**
Under symmetry (`ends ±1`, `struts ±f`) the invariant is `(1+f)²/4f`: one
equation, one unknown.

**RULING: IT WILL NOT CLOSE, AND IT FAILS ON EXACTLY ONE TERM.**

- **P1 — the estimator is exact.** Five planted values recovered through a
  synthetic projective map to a worst error of **3.55e-15**. The algebra is not
  the problem.
- **P1b — the positive control was GRADED UNTIL IT FAILED, and the level is
  published.** Injecting error into the far end alone, on the synthetic map
  where truth is known: **1 px → 1.4 %, 4 px → 6.2 %, 8 px → 14.3 %, 15 px →
  44.0 %, 29 px → NO REAL ROOT AT ALL.** `(1+f)²/4f` has a MINIMUM of 1 at
  `f = 1`, so near the measured `X ≈ 1.06` the map back to `f` is nearly
  vertical. **10 % error is reached at dU = 8 px.**
- **C3 — the two good columns are solid.** Over a five-threshold sweep the post
  reads `u 355.0–376.0` (centre **365.5**), right edge moving **0.5 px**; the
  hoop's outer column reads **485.0**, moving **0.0 px**.
- **C4 — the near/far assignment comes from the vehicle, not an assumption.**
  The visible flank recedes to high `u` and the front panel lies to low `u` of
  the body corner at `u ≈ 490`, so the bar's near end is the high-`u` end. REF
  §9 independently calls the headlamp at `u = 419` "the near side".
- **C5 — KILL. It fires.** Sweeping the far bar end across rev 31's own stated
  blob: `203 → f 0.578`, `209 → 0.616`, `215 → 0.666`, `221 → 0.739`, and at
  `228+` **the ordering breaks entirely** — the far end would be inboard of the
  far strut. **f swings 28 % across ~29 px. THE ROUTE DOES NOT CLOSE.**

**THE ~29 px IS NOT "THE STATED PRECISION" ON THIS ROUTE; IT IS FATAL TO IT.**
Reported as a dead route rather than widened into an answer.

**A SECOND ROUTE WAS MEASURED AND ALSO RULED OUT.** The transverse VP by
harmonic conjugate — a symmetric pair plus the centreline on one lateral line
fixes that line's vanishing point, and **the transverse VP is shared by every
lateral line on the vehicle regardless of height, so it transfers into the
bumper plane without needing the vehicle's YAW** (which is what killed rev 31's
ARM 1). Both headlamp apertures are visible, near centre `u ≈ 419`, far
`u ≈ 236`, and with the corrected apex that gives a VP at `u ≈ 111` and a
bumper-plane centreline near `u ≈ 266`. **It is not published**, for three
reasons stated rather than buried: the far headlamp's dark region runs into the
nose's far silhouette and the shadow behind it, and ±5 px there alone moves `f`
by 9 %; four row-wise VP estimates off the V arms scatter over **154 px**,
because every construction available reduces to a difference of two nearly equal
near/far half-widths; and the whole thing assumes the bar is symmetric about the
vehicle centreline, which is an ASSUMPTION whose only check — mirroring the far
strut through the same map — **disagrees at 17 %**, inside the blob's own
confounding and therefore neither a refutation nor a corroboration.

**THE POST STAYS UNBUILT. NO VALUE OF `f` IS PUBLISHED.** It is blocked on ONE
COLUMN, and it is a column measurement cannot reach: rev 31 established from the
owner's own reading that the far end is a **three-member superposition**, and a
superposition is not resolvable by thresholding it. **That is why rev 32 spends
a QUESTION on it and not a third estimator** — rev 30's rule, *measure somewhere
else before you build a third estimator*, and there is nowhere else on this
frame to measure.

#### §10.75's POINTER, taken from and now vindicated

§10.75 drew box C `(357,681)-(374,697)` and its own text says the boxes were
*"stated to him as POINTERS, not sampling windows — no number taken from them."*
**rev 30 took `357–374` as a measurement anyway and rev 31 computed `365.5` from
it.** rev 32 re-measured it properly: `u 355.0–376.0`, centre **365.5**, stable
to 0.5 px over five thresholds. **THE POINTER IS VINDICATED TO WITHIN 2 px.**
The number survives; the process defect stands and is recorded, because the next
pointer taken from may not be right.

#### §10.82's three surfaces — asked, and the item's own description corrected

`probe_rev32_pointer.py` (NEW, read-only) validated the question before sending.
**THE WORK LIST'S OWN DESCRIPTION IS WRONG:** rev 29, rev 30, rev 31 and the
rev-32 brief all say *"the workshop frame shows all three"*. **It does not.** In
`ref_workshop.jpg` **both road wheels are BARE PAINTED RIMS WITH NO HUB CAP** —
the vehicle is at conversion stage. The red VW-logo caps exist only in
`ref_side.jpg`. **A FEATURE NAMED IN A WORK LIST IS A PROBE TOO**, one level out
from §10.85's rule about reference files.

The question was also checked for worth before being asked: the retired lever
reaches **0.4500 m²** of rim barrel, **0.2100 m²** of hub cap and **0.0909 m²**
of `bumper_f` — 0.751 m² against `T1_body`'s 12.294 m², about 6 %, on three
surfaces at the front of every hero frame. **A QUESTION YOU ARE ABOUT TO ASK IS
A PROBE TOO.**

**MY OWN FIRST POINTER FAILED AND WAS MOVED, NOT EXCUSED.** Reusing rev 29's
statistic and rev 29's two calibration anchors with **the band unchanged**, my
first hub-cap box read **8.77×** — closer to a PROVEN straddler (13.54×) than to
a box the owner had already answered (3.14×). It sat on the specular highlight.
**Seven of eight cap boxes fail**, and that is a fact about the cap, not about
my aim: it is a dome with the wheel-arch shadow's EDGE across its lower half,
and a quadratic absorbs a gradient but not an edge. All eight are printed in the
probe. Final: **B1 1.96×, B2 1.81×, B3 2.78×, 10 controls, 0 failed.** CEILING,
stated: rev 29's anchors both live on `ref_rear34.jpg`, two of these boxes do
not, and **there is no answered anchor on `ref_side.jpg` at all** — which is not
load-bearing only because these are pointers and no number is taken from them.

#### An unsought defect: a control that had been failing since rev 30

`probe_dust_scope.py:249` hard-coded *"audit.py publishes 185"*. rev 30 added
`orb_bar` and took the published mesh count to **186**, and this literal was not
swept. **The probe has been failing one of its own eight controls since rev 30,
and neither rev 30 nor rev 31 ran it.** Found while validating an owner
question. The literal is corrected rather than the check loosened — the check's
whole job is to prove the truncated exec built the WHOLE vehicle, and a count
allowed to drift cannot do that job. **A CONTROL NOBODY RUNS IS NOT A CONTROL.**

#### Rules earned this revision

- **A CONTROL THAT FAILS CAN HIDE THE DEFECTS DOWNSTREAM OF IT.** Correct the
  input to a failed control and re-read the whole arm, not just its verdict.
- **A FEATURE NAMED IN A WORK LIST IS A PROBE TOO.**
- **A CONTROL NOBODY RUNS IS NOT A CONTROL.** Run the probes a revision
  inherits, not only the ones it writes.
- **CORRECTING AN ANCHOR IS NOT SWEEPING IT.** §10.85 corrected in place and
  said so; the consumers still had to be chased one revision later.
- **WHEN A ROUTE'S ALGEBRA IS EXACT, GRADE ITS CONDITIONING AND PUBLISH THE
  LEVEL AT WHICH THE POSITIVE CONTROL FAILS.** "dU = 8 px" is a usable number;
  "it is ill-conditioned" is not.

### 10.87  rev 33 — THE OWNER ANSWERS BOTH OUTSTANDING QUESTIONS: §10.82's NAMED GAP CLOSES, and the post's route fails on a column NOBODY EVER MEASURED

**NO GEOMETRY MOVED. NO SHADER. NO ARTWORK.** The last geometry change is
still rev 30's. `CREAM`, `COUNTERTAN`, `COUNTERCREAM`, `RED`, the rake, the
roof, the over-rider bar and all three textures are UNCHANGED.

#### 10.87.1  Q2 — ALL THREE SURFACES ARE CLEAN. §10.82's NAMED GAP CLOSES.

**[stated, rev 33]** The bumper top, the wheel rim face and the hub cap
**carry no settled-dust film.** Asked on `rev32_q2_surfaces.png` with three
POINTERS, declared as such, validated before sending (`probe_rev32_pointer.py`
B1 1.96x, B2 1.81x, B3 2.78x against an ANSWERED box's 3.14x and a PROVEN
straddler's 13.54x, 10 controls 0 failed), and shown beside the current build
with the film OFF and ON.

**WHAT THIS SETTLES.** §10.82 retired the dust film's DERIVATION and left a
named gap: the global zeroing had owner support on the ROOF (rev 29) and on
the COUNTER TOP (rev 28) but none on the three surfaces the same node films
at the front of every hero — 0.751 m² of up-face area, ~6 % of `T1_body`'s
12.294. **That gap is now closed from the owner's own reading.** The global
`f = 0` gains three further surfaces of support and **the film does NOT need
to become LOCAL** (per-material `dust` input). The one-lever treatment stands.

**WHAT IS NOT CLAIMED, and the ceiling is the same one rev 32 stated.** Two
of the three pointers are on `ref_side.jpg`, and **there is no answered
calibration anchor on `ref_side.jpg` at all** — rev 29's anchors are on
`ref_rear34.jpg`. The validation transferred a band across frames and said so.
This answer therefore closes the NAMED GAP; it does not upgrade the pointers
into measurements, and **no number is taken from any of the three boxes.**

**NOTHING WAS TUNED.** §10.82 retired a DERIVATION, not a constant. No lever
was moved in either direction on the strength of this answer.

#### 10.87.2  TWO INHERITED PROBES HAVE BEEN DEGENERATE SINCE THE RETIREMENT, and one of them prints a TAUTOLOGY as a COMPARISON

Running every probe in the tree rather than only the ones this revision wrote
— rev 32's rule, `A CONTROL NOBODY RUNS IS NOT A CONTROL` — found two more:

- **`probe_clean_top.py` fails H1, H2 and H3.**
- **`probe_dust_anchor.py` fails two C3 arms.**

**MECHANISM CONFIRMED, NOT GUESSED.** `probe_clean_top.py` prints
`live coverage f = 0.000000`. Both probes were written in rev 27/28 against
the PRE-retirement chain and their controls reconstruct `_UP_MEASURED` through
a coverage term that is now zero. The failures are a CONSEQUENCE of §10.82,
not a regression, and **no tolerance was widened to silence them.**

**AND ONE IS WORSE THAN A FAILING CONTROL.** `probe_clean_top.py`'s headline
table now prints

```
    dusty COUNTERTAN   (SHIPPED)   (0.9511, 0.7815, 0.5298)  -10.0 % -11.6 % -34.0 %
    CLEAN COUNTERTAN   (f = 0)     (0.9511, 0.7815, 0.5298)  -10.0 % -11.6 % -34.0 %
      worst channel |err|: dusty 34.0 % -> clean 34.0 %
```

**Its A-versus-B comparison has silently become A-versus-A**, while its prose
still argues "removing the dust is NECESSARY". The `42.5 % -> 34.0 %`
improvement that rev 28 quoted as "real corroboration from an independent
direction" **cannot be reproduced by the probe that produced it**, because the
lever it differenced no longer exists.

> **NEW RULE. A PROBE OUTLIVES THE WORLD IT WAS WRITTEN IN. When a lever is
> retired, every probe that DIFFERENCES that lever silently becomes a
> comparison of a value against itself — and it keeps printing, keeps
> formatting, and keeps narrating. A degenerate comparison is more dangerous
> than a failing control, because nothing about it is red.**

This is why §10.70's percentages must be RE-RUN before being quoted again
(carried since rev 29): **they are of the same family**, and the mechanism is
now named rather than merely suspected.

#### 10.87.3  `STATE.md` IS ONE REVISION STALE IN THE COMMITTED TREE

`STATE.md` is **byte-identical to `STATE_rev31.md`** (both md5
`a74f534c866e8870c197d1e0dbf03da9`). rev 32 regenerated `STATE_rev32.md` and
committed it, but never re-committed `STATE.md`, so the tree's machine-written
file still names commit `6f87977`, subject "rev 31b". **The diff against
`STATE_rev32.md` is the three provenance lines and nothing else**, so no
published figure is wrong — consistent with no geometry having moved. But the
handoff instruction "STATE.md is machine-written; if it and any prose disagree,
it is right" points at a file that self-identifies as a rev-31b artifact.
**RECORDED FIRST, THEN REGENERATED — in that order and deliberately.** The
finding is written here, into prose that survives, BEFORE `STATE.md` is
regenerated on the rev-33 tree; regenerating it first would have erased the
only evidence the gap ever existed. `STATE_rev33.md` is written alongside, as
every revision since rev 8 has done.

#### 10.87.4  rev 32's Q1 FIGURE QUOTED A PLANTED SYNTHETIC VALUE AS A MEASUREMENT

Before re-asking Q1, the figure was checked — `A QUESTION YOU ARE ABOUT TO ASK
IS A PROBE TOO`. `rev32_q1_barend.png` carried three defects in the block that
tells the owner why the column matters:

1. **"at u = 209 the post lands at 0.626."** `0.626` is `f_true` in
   `probe_orb_xratio.py`'s **P1b** — a value **PLANTED on a SYNTHETIC
   projective map** to grade conditioning. It is not a reading of this
   vehicle. The live value at u = 209, from C5's own columns, is **0.6160**.
2. **"at u = 224 it lands at 0.820."** C5's machinery gives **0.7943**.
   `0.820` is produced by neither the synthetic map nor the live columns. The
   swing of record is **C5's 28 % over u 203–221**, not 31 %.
3. **Candidate lines 4 (u 228) and 5 (u 240) sit at or beyond C5's
   `strut_u = 228.0`**, where C5 declares ORDER BROKEN. **Two of five options
   could not be consumed by the route the question existed to feed.** They
   were KEPT and LABELLED, not removed — they are legitimate readings of the
   photograph, and choosing one is a decision to close the route.

Rebuilt as `rev33_q1_barend.png` by `mark_rev33_q1.py`, which **hard-codes no
`f`**: every number is recomputed from C5's constants at draw time behind a
positive control that re-derives four of C5's printed rows (worst deviation
**4.24e-05**) and **refuses to write the figure if that control fails.**

> **A NUMBER WRITTEN INTO A QUESTION IS A NUMBER NOBODY RE-READS.** Make the
> figure recompute it, and make the figure refuse to draw if it cannot.

#### 10.87.5  Q1 AND Q1b — THE OWNER CLOSES THE FAR END, AND THE ROUTE STILL FAILS

**[stated, rev 33]** The over-rider bar's far termination is at **candidate
line 1, u = 205**, and **[stated, rev 33]** it is **AT line 1, not left of
it**. `f` at that column is **0.5897** of the bar's half-width.

**THE PRE-COMMITMENT, MADE ON THE FIGURE BEFORE THE ANSWER ARRIVED** (§6 of
the rev-33 brief requires it): *"naming ONE line still leaves ~7 px of
residual and the route does NOT close."*

**A4/A5 — the Q1 answer alone did not bracket.** He chose the **LEFTMOST**
member of the offered set. An endpoint answer leaves the interval OPEN on that
side; the set's left boundary at 205 was rev 32's choice, not the
photograph's, and C5's own sweep started at 203 for the same arbitrary reason.
**20 px of reach to the left moves `f` by 17.8 %.**

**Q1b CLOSED THAT SIDE, and it is worth saying without hedging.** Asked on
`rev33_q1b_leftbound.png` with the crop **widened left to u = 170** and four
new CANDIDATE LINES at u = 185/190/195/200 — marks on the side the first set
never reached. With the left side bounded, the residual is the line spacing
alone: **3.5 px → 5.4 %, INSIDE the published closing level of dU ≤ 4 px
(6.2 %). ON THE FAR END, THE OWNER CLOSED IT.**

**AND THE ROUTE STILL DOES NOT CLOSE — A6 AND A7, ON A COLUMN NOBODY EVER
MEASURED.** The four-point cross-ratio consumes FOUR columns. C3 measured
**two** (post 365.5, hoop outer 485.0). P1b graded **one** (the far end). The
fourth — **the FAR STRUT** — is carried in C5 as a hard-coded
`strut_u = 228.0` **whose own print labels it "(blob)"**, and **u 228 is rev
32's candidate line 4**: the strut column sits INSIDE the same u 203–232
three-member superposition as the far end. Graded here for the first time,
with the far end held at the owner's 205:

| far strut moves | `f` swings |
|---|---|
| ± 4 px | **11.1 %** |
| ± 8 px | **23.7 %** |

**THE UNGRADED COLUMN IS THE MORE SENSITIVE OF THE TWO** — 11.1 % against the
far end's 6.2 % for the same ± 4 px. Bounding the far end, which cost two
revisions and three questions, **does not control the answer.**

**THE POST STAYS UNBUILT. NO `f` IS PUBLISHED AS A BUILD VALUE.**
**NOT CLAIMED:** that the strut is wrong, or that 228.0 is a bad value. The
claim is only that **nothing has ever measured it**, and the estimator is more
sensitive to it than to the column two revisions were spent on.

**THE PRE-COMMITMENT WAS ONLY HALF RIGHT AND IS SCORED AS SUCH.** It asserted
~7 px of residual and no close. On the half-spacing reading that residual is
3.5 px → 5.4 %, **inside** the closing level — so **criterion (1) alone would
have CLOSED the route** and the stated reason was wrong even where the verdict
was right. The verdict survives on A6/A7, which concern **a different column
entirely**.

> **A PRE-COMMITMENT IS A PROBE TOO.** This one was under-specified — it named
> a residual without naming which reading of it applied, and the two readings
> disagree across the decision boundary — **and it was aimed at the wrong
> term.** State which quantity the pre-commitment binds, and check that it is
> the quantity the estimator is most sensitive to.

> **AND THIS IS §10.86's OWN RULE FIRING AGAIN: A CONTROL THAT FAILS CAN HIDE
> THE DEFECTS DOWNSTREAM OF IT.** C5 failed on the far end for two revisions,
> so no revision ever asked what ELSE C5 consumed. The strut has been
> hard-coded and ungraded since rev 32 wrote the probe.

**WHAT WOULD CLOSE IT NOW, in order of value.**
1. **A square-on frame of the FRONT of the vehicle** — collapses the lateral
   scale problem entirely. Unchanged, and still worth more than any answer.
2. **The FAR STRUT's column**, to the same standard the far end now has: an
   owner reading PLUS a bound. It is the only remaining ungraded term and it
   is the sensitive one.
3. **Nothing else.** Do not rebuild the cross-ratio algebra — P1 shows it
   exact to **3.55e-15** and the algebra was never the problem.

#### 10.87.6  CARRIED FORWARD, UNCHANGED

§10.83's "post at the vehicle's centreline" remains **UNDECIDED**, fourth
revision running. REF §9's V-swage absolute height remains a **bracket,
≈0.40–0.49 m**. The transverse-VP-by-harmonic-conjugate route remains
**UNPUBLISHED, not refuted**. `422 px/m` is consumed nowhere. The hero
`rev30_hero34f.png` is proved by content and is not re-shot.

### 10.88  rev 34 — THE STRUT IS MEASURED AT LAST, AND IT RETIRES THE CROSS-RATIO ROUTE ON A PRECONDITION, NOT ON PRECISION

**NO GEOMETRY MOVED.** The last geometry change is still rev 30's. Guards
**0 fail / 0 warn at both subdivision levels**, every figure identical to
rev 30/31/32/33's. This section does five things: it grades the instrument
BEFORE spending a question on the owner, it corrects a live-against-synthetic
comparison inherited from §10.87, it names a general rule about tolerances
stated in the wrong units, it consumes two owner answers, and it **retires the
cross-ratio route** — the one §10.86 opened and §10.87 could not close.

#### 10.88.1  THE INSTRUMENT WAS GRADED BEFORE THE QUESTION WAS ASKED

`probe_rev34_levels.py` (NEW, read-only). **8 controls, 4 FAILED.**

`probe_rev33_barend.py` gates its controls **in two different units inside one
file**. A3 gates in PIXELS (`check(... dU <= CLOSE_AT ...)`, `CLOSE_AT = 4`).
A7 gates in PER CENT (`check(sw4 <= interp_error(4))` → 6.2 %). And
`interp_error` reads the frozen dict `P1B`, whose own comment in that file
says *"P1b's published conditioning levels, on the SYNTHETIC map (planted
f 0.626)"*.

So A7 asks a fair question — *does 4 px on the STRUT cost more than 4 px on
the FAR END costs?* — but prices the strut on the **live** columns and the far
end on a **fabricated** map. **THIS IS §10.87.3's DEFECT, ONE REVISION LATER,
INSIDE THE PROBE WRITTEN TO RECORD THE CORRECTION.**

The map's four columns beside the live four, printed rather than asserted:

| point | synthetic | live | diff |
|---|---|---|---|
| far end (t=−1) | 208.9 | 205.0 | −3.9 px |
| far strut (t=−f) | 224.6 | 228.0 | +3.4 px |
| near post (t=+f) | 356.6 | 365.5 | **+8.9 px** |
| near end (t=+1) | 487.2 | 485.0 | −2.2 px |

**The map is wrong by up to 8.9 px about the configuration whose 4 px errors
it is used to price.**

- **K1 FAILS.** P1b's curve **UNDER-PRICES the live configuration by 1.39× at
  4 px and 1.28× at 8 px.** The published **6.2 % closing level is 8.6 %
  live**; the published **14.3 % failing level is 18.3 % live**. Every per-cent
  figure ever read off that curve and spent on the live columns is that much
  too small.
- **K3 PASSES, and that is a real result.** The strut IS the more sensitive
  column even when both are graded live. **§10.87's A6/A7 conclusion survives.**
  Only its published margin was inflated: **1.79× reported, 1.28× like for
  like — a 39 % overstatement.**
- **K2 FAILS.** On §10.87's own residual the two units **disagree across the
  decision boundary**. Its justifying sentence — *"3.5 px on the stronger
  reading → 5.4 %, INSIDE the published closing level of dU ≤ 4 px"* —
  converts px to per cent and then compares against a px band. The conversion
  is **unnecessary** under the px reading and **wrong** under the per-cent one:
  live it is **7.5 %**, not 5.4 %. **THE VERDICT IS RIGHT AND THE ARITHMETIC
  PRINTED UNDER IT IS NOT** — which is precisely what §10.87 said about its own
  pre-commitment, one quantity over.
- **K4 FAILS, and it is the general one.** The same 4 px costs **8.6 % on the
  far end and 11.1 % on the strut** — a **constant 1.28× at every
  perturbation**, so it is structural, not a scale artefact.

> **NEW RULE: A TOLERANCE STATED IN THE UNITS OF THE MEASUREMENT, NOT OF THE
> QUANTITY, DOES NOT TRANSFER BETWEEN COLUMNS.** Every use of "dU ≤ 4 px" on a
> new column silently assumes a shared px → f map. This is the mechanism
> underneath §10.87's A7, which found the effect and published it as a number
> instead of a principle.

#### 10.88.2  THE PRE-COMMITMENT, MADE BEFORE THE QUESTION WENT OUT

**K5 FAILED BEFORE THE OWNER WAS ASKED ANYTHING.** Taking the *generous*
tolerance — 4 px on the far end is what the project accepted, live 8.6 % — the
far end already spends **7.5 %** at its answered ±3.5 px, leaving **4.27 %** in
quadrature. That needs the strut pinned to **≈ ±1.5 px**. A 7 px candidate set
returns ±3.5 px (9.6 % alone, **12.2 % total**); halving to 4 px lines returns
±1.8 px (**8.9 % total**) — still over. **Stated on the question figure itself:
NO ANSWER TO THIS CLOSES THE POST.** What it was asked for instead is stated
too: to convert the last hard-coded column into a measured value.

#### 10.88.3  THE OWNER'S TWO ANSWERS

- **Q1** *[stated, rev 34]*: the far strut is at **S1 or S2 — LEFT of the
  hard-coded 228.**
- **Q1b** *[stated, rev 34]*: it is at **B1 or left of it — u 205 to 208.**

Both are the leftmost option of their set, so §10.87's endpoint rule applied
twice. **Q1's left side was already bounded, and NOT by a set boundary chosen
by me:** the cross-ratio requires `far_end < strut`, so with the far end at
u 205 every column at or left of 205 is forbidden by the estimator's own order
(`u 204` and `u 205` both return ORDER BROKEN). **S1 sat 7 px from a hard
wall.** In §10.87's Q1 the leftmost option had unbounded reach and 20 px of it
moved `f` by 17.8 %; here there was nowhere for the answer to run to. The Q1b
figure draws that wall **as a wall and labels it as not a candidate**.

**THE INTERVAL IS CLOSED ON BOTH SIDES: u ∈ (205, 208].**

#### 10.88.4  THE RULING — THE ROUTE IS RETIRED ON A PRECONDITION

`probe_rev34_ruling.py` (NEW, read-only). **6 controls, 4 FAILED.**

**WHAT THE ANSWERS BOUGHT, said first.** The far strut was hard-coded at
u 228 on no support of any kind, its own print calling it `(blob)`. **It now
has an owner reading closed on both sides.** And **the hard-coded value was
outside that interval entirely** — 20 to 23 px away, `f` 0.5897 against
0.835–0.950. **Every C5 row published since rev 32 was computed at a column
the owner does not put the feature anywhere near. NOT A REFINEMENT — A
REPLACEMENT.**

**R3 FAILS.** The answered strut sits **1.5 px** from the bar's far end. The
far end's own published residual is **±3.5 px — 2.3× the gap it must stay left
of.** The two points are **not separable at the precision of the readings that
define them.**

**R4 FAILS, and this is what ends it.** Sweeping the far end across its own
stated interval 201.5–208.5 with the strut held at 206.5: `f` 0.7947 at 201.5,
0.8246 at 203.0, 0.8809 at 205.0, 0.9292 at 206.0, then **ORDER BROKEN at
206.5, 207.5 and 208.5**. **29 % of the far end's own error bar puts it at or
right of the strut, which the four-point construction forbids outright.**

> **THE FOUR-POINT CROSS-RATIO HAS DEGENERATED TO THREE. That is a failure of
> its PRECONDITION, not of its precision.** No further measurement on those two
> columns repairs it, because what broke is that they are the same place to
> within their own error bars.

**R5 FAILS** in corroboration: at ±1 px the answered regime costs **9.5 %**
against **2.7 %** where the levels were graded — **3.6× worse** — and at
±1.5 px it returns nothing, the low sample being at the wall. **R6 FAILS**:
13.6 % total against an 8.6 % tolerance.

**EVERY PRIOR REVISION ASSUMED A 23 px SEPARATION** — C5, P1b, A6, A7, and
both of rev 34's own probes. The owner's reading makes it 1.5 px. **Nobody
could have found this by measuring harder; it took asking.**

**NOT CLAIMED:** that the assembly is asymmetric (a large far-side overhang in
3D can project to a small one, and the cross-ratio accounts for that exactly —
that is why it was chosen); that the owner's interval is wrong; that u 228 was
a lie (**u 228 was never a measurement, which is the whole complaint**); or
that the algebra failed (R1 passes, P1's 3.55e-15 stands).

**THE POST STAYS UNBUILT. NO `f` IS PUBLISHED AS A BUILD VALUE.** What closes
it is now the **only** remaining route: **a square-on frame of the FRONT.**
Everything else on this panel has been spent.

#### 10.88.5  DEFECTS OF MY OWN, EVERY ONE RECORDED

- **MY OWN `swing()` SILENTLY DROPPED AN `ORDER BROKEN` SAMPLE** and computed
  the spread over the survivors, so R5's ±1.5 px cell printed **5.5 %** — a
  *smaller* number — for a regime that had actually broken, while the prose
  three lines below said it returned nothing at all. **A NARRATION
  CONTRADICTING ITS OWN TABLE: §10.87.2's family, in a probe written the same
  day as the rule was read.** Fixed by making `swing()` return `None` if ANY
  sample is unreachable, and by computing that sentence from the table.
  **A silently dropped sample is not a smaller error, it is a missing one.**
- **AN ARM THAT COULD NOT HAVE FIRED.** Arm A refit P1b's synthetic map to
  reproduce all four live columns exactly (verified: the fourth point falls out
  at 365.500, so the cross-ratio is preserved). **K1 did not move** — because
  K1's synthetic side reads a **frozen literal**, not the map. **REFITTING A
  MAP CANNOT MOVE A CONTROL THAT READS A HARD-CODED DICT.** Arm B replaced the
  dict with the live curve; K1 and K2 both flipped to PASS and N2 correctly
  failed. Arm C moved the strut 228 → 260; K4 went 1.29× → 1.98×.
- **ARM B CAUGHT A DEFECT IN MY OWN PROBE.** With K2 passing, its detail
  string still narrated *"THE TWO READINGS DISAGREE ACROSS THE DECISION
  BOUNDARY"* — asserted, not computed. Fixed; the verdict word is derived.
- **TWO FIGURE-RENDERING DEFECTS, both caught by cropping the PNG and looking
  at it.** The Q1 figure clipped its header because the canvas was sized off
  one text block while three were drawn — now every drawn string is measured.
  The Q1b figure's wall label landed first across the B1–B4 tags and then
  across the candidate lines; it is now drawn last.
- **THE `bpy` MEMBERSHIP IN THE REV-34 BRIEF IS RIGHT FOR THE WRONG REASON.**
  Six probes need Blender, and the count is correct — but a `grep` for `bpy`
  returns **two false positives** (`probe_clean_top.py`, `probe_dust_anchor.py`
  mention it only in a comment explaining why they parse `t1_mats` with `ast`
  instead) and **two false negatives** (`probe_cross_anatomy.py`,
  `probe_shutlines.py` import it transitively, with the token appearing nowhere
  in the file). **The errors cancel exactly: 4 − 2 + 2 = 6.**
  > **NEW RULE: A DETECTOR WHOSE ERRORS CANCEL IN THE AGGREGATE IT IS QUOTED BY
  > IS INDISTINGUISHABLE FROM A CORRECT ONE, UNTIL SOMEONE NEEDS THE MEMBERS
  > AND NOT THE COUNT.**

#### 10.88.6  CARRIED FORWARD, UNCHANGED

§10.83's "post at the vehicle's centreline" remains **UNDECIDED**, fifth
revision running. REF §9's V-swage absolute height remains a **bracket,
≈0.40–0.49 m**. The transverse-VP-by-harmonic-conjugate route remains
**UNPUBLISHED, not refuted** — and with the cross-ratio retired it is now the
only unspent construction on this panel. `422 px/m` is consumed nowhere. The
hero `rev30_hero34f.png` is proved by content and is not re-shot.
`probe_clean_top.py` and `probe_dust_anchor.py` are **still deliberately
failing** and still need rewriting, not fixing.

### 10.89  rev 35 — THE HARMONIC-CONJUGATE ROUTE IS RETIRED ON A MISSING FEATURE, AND MY OWN REPLACEMENT WAS REFUTED BY MY OWN AUDIT IN THE SAME REVISION

**NO GEOMETRY MOVED.** The last geometry change is still rev 30's. `verify.py`,
`t1_detail.py`, `t1_mats.py`, `build.py`, `t1_shell.py`, `t1_core.py` and every
other build file are BYTE-UNCHANGED from rev 34.

#### 10.89.1  THE ROUTE WAS GRADED BEFORE A QUESTION WAS SPENT — AND EVERY COLUMN IT CONSUMES, NOT THE ONE UNDER ARGUMENT

`probe_rev35_harmonic.py` (NEW, read-only). **18 controls, 6 FAILED.**

**H1 and H2 PASS.** The harmonic algebra is exact (**3.75e-12 px**) and the
transfer claim holds: the transverse VP really is shared by lateral lines at
the bar, the belt and the roof (**worst 4.89e-12 px**). *As with the
cross-ratio, the algebra was never the problem.*

**H3 KILL — THE ROUTE'S THIRD INPUT IS NOT OBSERVED.** The harmonic conjugate
needs THREE columns on the headlamp line: the two lamps **and their midpoint**.
Only two exist. **There is no feature at the centre of the headlamp line, so
there is no image of the midpoint anywhere in the frame.** §10.86 supplies the
third from the V-swage apex, a centreline point **0.625 m below that line**
(z 0.4050 against `t1_detail.py:346`'s 1.0300), at a depth recorded nowhere, on
a panel REF §9 itself calls not planar. Sweeping the VP across its entire
admissible range (VP < the bar's far end, by §10.86 C4) leaves the lamp
midpoint **free over 67.8 px, [259.7, 327.5]**, and `t` **free over 0.8483 bar
half-widths — 17× the 0.05 level**.

> **288.8 IS ONE CHOICE INSIDE THAT INTERVAL, NOT A READING OF IT.** This is a
> PRECONDITION failure of §10.88.4's class, not a precision shortfall. **No
> further measurement on this frame repairs it, because what is missing is not
> accuracy but a FEATURE.**

**H5 FAILS — `u_lamp_far = 236` HAS NO RECORDED DERIVATION ANYWHERE IN THE
TREE.** It appears in exactly two places, §10.86's prose and
`HANDOFF_rev32.md`, and in **neither `REF_MEASUREMENTS.md` nor any probe**. No
band, no threshold sweep, never asked about. **Same class as §10.88.4's
`u 228`, found the same way and one revision later.**

**H4 PASSES, AND ITS PASSING IS THE DEFECT OF THE REVISION — see §10.89.3.**

**G1..G6, graded LIVE and in the units of the QUANTITY.** Dominant columns are
`u_lamp_far` (**±band moves t by 0.1928**) and `u_apex` (**0.0710**); the four
owner-answered or C3-solid columns move it by 0.0015 to 0.0134. **K4 fires
again on new columns: ±1 px buys 0.0240 half-widths on the far lamp and 0.0039
on the near one — 6.08× for the same pixel move.**

**A NEGATIVE RESULT WORTH CARRYING: NO QUESTION WAS ASKED, AND THE REASON IS
ARITHMETIC.** A reading of the far lamp closes nothing — it does not enter the
surviving result at all, and the route is dead independently of its value.
**Asking would have bought a column, not an answer.** §10.88's discipline
requires saying what a question can close *before* asking; here the answer was
*nothing*, so nothing was asked.

**AND THE ROUTE'S ONE PUBLISHED OUTPUT IS STALE.** §10.86's bumper-plane
centreline `≈266` was computed with the far bar end at `u ≈ 209`, which rev 33's
and rev 34's owner answers have since REPLACED with `u ∈ (205, 208]`. At u 205
the same construction gives **261.2**.

#### 10.89.2  WHAT WAS PUT IN ITS PLACE, AND WHAT SURVIVES OF IT

The route being dead does not leave `t` unknown. The post's column **365.5**
lies **+20.5 px right of the bar's mid-column 345.0**, and under perspective the
image of the bar's 3-D MIDPOINT lies at or LEFT of that arithmetic mean, because
the far end recedes (§10.86 C4). **The post is therefore on the NEAR side of the
bar's 3-D midpoint.**

**THE SIGN IS WHAT SURVIVES. THE MAGNITUDES ARE WITHDRAWN.** rev 35 first
published **t ≥ 0.1464** (nominal) and **t ≥ 0.0595** (worst corner of every
band, post read at its left edge 355.0) as holding *"for every admissible
camera"*, *"consuming no vanishing point, no camera model and no symmetry
assumption."* **Its own adversarial audit refuted that, and both figures are
STRUCK rather than quietly re-scoped.**

#### 10.89.3  MY OWN AUDIT REFUTED MY OWN CLAIM, AND THE DEFECT IS THE ONE I HAD JUST CREDITED §10.88 WITH FINDING

**WHAT SURVIVED THE ATTACK, and was checked rather than assumed:** the
monotonicity of `t` in the VP (**10⁶ samples, worst decrease 0.000e+00**; the
infimum is the closed form `(2P−A−B)/(B−A) = 41/280`); the VP's admissibility
(**200 000 random pinholes × random segments, 0 cases with VP ≥ u_far**); and
the cross-ratio formula itself (**50 000 random cameras × planted t, worst
recovery error 1.96e-10**).

**B2 KILL — THE COLLINEARITY PRECONDITION IS VIOLATED BY THE BUILD'S OWN
CONSTANTS.** A cross-ratio requires its four points COLLINEAR in 3-D. **They are
not.** `u 485` is the **HOOP's** outer column, and `t1_detail.py`'s own arc

    x = BAR_X − BACK(1−cos a),  y = HALF_Y + 0.55·DROP·sin a,  z = BAR_Z − DROP·sin a

carries the generating point up to −39.9 mm in x, +35.7 mm in y and −64.9 mm in
z off the straight axis end; the audited generating point sits at **−17.5 /
+29.5 / −53.7 mm**, inside that range on all three axes. **Re-derived from the
arc formula here, not taken on the auditor's word.** Separately, the post's
column was read on rows **676–700** while the bar's top edge is at **v 672.5** —
a different lateral line. **FOUR POINTS, THREE LINES.**

**B3 KILL — THE BOUND IS NOT CAMERA-FREE, WHICH IS EXACTLY WHAT IT CLAIMED TO
BE.** It assumes **zero camera roll** (the magnitude degrades ≈0.00045
half-widths per degree over the pose grid and fails 0.1464 beyond |roll| ≈ 7°)
and **zero post standoff** from the bar's plane (238 px per metre; 60 mm
rearward breaks 0.1464 at the plausible pose). `t1_detail.py` calls that standoff
**"a CHOICE, not a reading"**, and §10.86 says of the roll, one section earlier
and about a different arm, that *"nothing in this repository establishes that"*
the camera is level and unrolled. **The probe relied on exactly that unestablished
property one section later.**

**NOT CLAIMED, and the distinction is load-bearing:** at the plausible pose
(az 48°, el 17°, d 6.2 m) roll *raises* `t` — 0.2606 at 0°, 0.2837 at 30°, my own
run. The auditor's degradation comes from admitting poses this photograph
excludes. **That is not used to rescue the claim.** The zero-roll margins are
**20.50 px of post column at nominal and 8.32 px at the worst corner**, against
a post whose own published extent is 21 px wide. **The SIGN survives to
|roll| ≈ 26° and ≈139 mm of rearward standoff, both excluded on this frame.**

> **THE RULE THIS EARNS: CHECKING THE PRECONDITION YOU WERE WARNED ABOUT IS NOT
> CHECKING THE PRECONDITIONS.** §10.88.4 retired the cross-ratio on its
> **ORDERING** precondition, so rev 35's H4 checked ordering — and PASSED, and
> printed *"no consumed column sits against a precondition wall."* The
> cross-ratio has **another** precondition, collinearity, and rev 35 did not
> check it until an adversarial audit did. **Inheriting one precondition from a
> previous revision's failure tells you nothing about the others. Enumerate what
> the construction REQUIRES, not what the last revision found.**

**AN UNSOUGHT CORROBORATION.** Normalising the bar's silhouette to 205/485 and
projecting the build's own headlamp centres `(2.1015, ±0.5450, 1.0300)` gives
**225 / 466** against the published **236 / 419** — a **47 px** misfit on the near
lamp, best-in-grid **45 px** over 3344 poses at zero roll; the modelled lamp/bar
span ratio is 0.86 against 0.654 observed. **This reproduces REF §9's own "I
fitted a projection model and it did not close" FROM THE MODEL SIDE**, and its
consequence is that the roll loophole **cannot be closed by measurement on this
frame at all.**

#### 10.89.4  FURTHER DEFECTS OF MY OWN, EVERY ONE RECORDED

- **A FALSIFICATION ARM THAT DID NOTHING, CAUGHT BY PRINTING THE CHANGED LINE.**
  ARM 5 was aimed at `swing()`'s unreachable path and returned a finite
  **0.9474** instead, because the band chosen missed the singularity by 0.002 px.
  Re-armed on an exact binary coincidence (`365.5 + 119.5 == 485.0`) it prints
  **`n/a` / UNREACHABLE**, so §10.88.5's fix is genuinely in. **§10.86's rule
  fires for the fourth revision running: an arm that does not apply is
  indistinguishable from a guard that does not fire.**
- **MY FIRST INSTRUMENT WAS GRADED ON A SCENE THAT DID NOT MATCH THE LIVE ONE.**
  The first `probe_rev35_harmonic.py` fitted a synthetic camera and used it for
  H3 and the grading. **The fit hit its bounds at a 178 px residual** and the
  synthetic far lamp landed at u 440 against the live 236. **That is §10.88.1's
  K1 defect — grading on a configuration the live one does not match — committed
  in the probe written to apply K1.** Discarded and rebuilt so that no control
  depends on a fitted pose.
- **THE FIRST ISSUE OF `rev35_bound.png` PRINTED THE WITHDRAWN MAGNITUDES** and
  was sent to the owner. Re-issued with them struck and the two unchecked
  preconditions named on the figure. **The superseded issue is named on the
  replacement.**
- **A NARRATION CONTRADICTING ITS OWN TABLE, CAUGHT ON RE-READING.** After the
  magnitudes were withdrawn in the ruling, B5's scope paragraph still read *"by
  at least 0.0595 of the bar's half-width."* **§10.87.2's family, in the same
  file as the withdrawal.** Fixed; the scope sentence now claims the sign alone.
- **THE INHERITED BRIEF'S §1 IS OFF BY ONE.** Its restore block annotates rev 34
  as `-> 181`; the bundle gives **182**, and the brief's own §7 says 182 and
  explains why (the count lands in its own commit). The inline comment predates
  the final commit. Recorded, not silently corrected.
- **THE PREVIEW TIMING IN THE BRIEF IS 71 s; THE OBSERVED FIGURE IS 79.3 s** for
  900×600 `T1_SUB=1 T1_PREVIEW=hero34f T1_SAMP=24`. Reported rather than rounded
  to the inherited number.

#### 10.89.5  CARRIED FORWARD, UNCHANGED

§10.83's "post at the vehicle's centreline" moves from **UNDECIDED** to **SIGN
ESTABLISHED, MAGNITUDE NOT** — and only under the bar's symmetry about the
centreline, whose only check §10.86 records **disagreeing at 17 %**, with
`BAR_HALF_Y` graded E. **THE POST STAYS UNBUILT.** REF §9's V-swage absolute
height remains a bracket, ≈0.40–0.49 m. `422 px/m` is consumed nowhere. The hero
`rev30_hero34f.png` is proved by content and is not re-shot.
`probe_clean_top.py` and `probe_dust_anchor.py` are **still deliberately failing
and still need rewriting, not fixing** — rev 35 did not reach them.
**A SQUARE-ON FRAME OF THE FRONT REMAINS THE ONLY THING THAT CLOSES THE POST**,
and after §10.89.3 it is also the only thing that could bound the camera's roll.

### 10.90  rev 36 — THE HOOP ENDS MEET THE BUMPER AT LAST; THREE OF REV 35's FIGURES FALL; A COLUMN THE PROJECT HAS CONSUMED SINCE REV 32 IS RENAMED BY THE OWNER; AND §10.83's FIVE-REVISION QUESTION DISSOLVES BECAUSE IT ASSUMED THERE WAS ONE POST

**The first geometry change since rev 30.**

#### 10.90.1  The owner's report, and the three things wrong with the old end

*[stated, rev 35]* "the upper bar appears to also connect with the main bumper
on either end. In the current version, there is no connection made."

Rev 35 confirmed this **"against the build's own constants, no render needed"**
and published two magnitudes. That method is the defect. It read the
CONSTANTS and not the FUNCTION THAT CONSUMES THEM: `overrider_bar()` capped the
hoop's turn at `(π/2)×0.62` = **55.80°**, the code's own comment saying
*"≤ 56 deg from horizontal"*, so the end descended `DROP·sin(a)` and retreated
`BACK·(1−cos a)`, not `DROP` and `BACK`.

Measured instead by **ray-cast through the built scene** — frame-free, and so
immune to the un-dropped/dropped confusion that broke rev 36's own first
attempt at this number by 81.7 mm:

| | rev 35 | **measured, rev 36** |
|---|---|---|
| vertical clear air above the blade | 8.1 mm | **23.59 mm** |
| tip behind the blade face | 52.4 mm | **0.51 mm** |

**THERE WAS ONE GAP, NOT TWO, AND IT WAS 2.9× THE PUBLISHED SIZE** — 0.945 ×
`BAR_DIA`, not 0.32×. The fore-aft figure does not describe this build in any
axis: `BAR_X` is *defined* as `2.1403 − BAR_DIA/2`, "outer faces coplanar", and
the measurement confirms the choice took.

Two further defects, neither of which was the gap:

- **A TANGENT DISCONTINUITY.** The old arc's first segment left the horizontal
  bar at **61.2° below horizontal instantly** — a kink in a swept tube — then
  **flattened to 43.4°** by its end, because the rearward term grew faster than
  the drop term. A kink needs no measurement to call. Nobody had looked at the
  tangent in six revisions.
- **THE 0.62 WAS NEVER A SHAPE DECISION.** The comment gives a NUMERICAL
  reason: `sweep()`'s frame is `t × UP` and degenerates as the tangent
  approaches UP. **A NUMERICAL WORKAROUND HAD BECOME THE SHAPE, AND THEREFORE
  THE DEFECT THE OWNER REPORTED.**

#### 10.90.2  What the photograph measures, scale-free

Tracing the tube's centreline through the near bend of `ref_workshop.jpg`,
**111 samples**, with the tube's own apparent diameter (**10.0 px**) as the
scale ruler: horizontal, then a bend of radius **1.35 tube diameters**, then a
descent at **69° below horizontal which it HOLDS**.

**Bend then steepen. The build kinked then flattened.** Wrong in kind.

Both figures are image-space and **each is published with the direction of its
bound**: the bend plane is foreshortened, which compresses it, so **1.35 is a
LOWER bound on the true radius and 69° is an UPPER bound on the true angle.**

#### 10.90.3  What was built, and what is now derived rather than chosen

A **true circular bend** tangent to the bar (`BEND_R_RATIO` × `BAR_DIA`,
MEASURED), turning to `BEND_THETA` (MEASURED), then a **straight leg whose
length is DERIVED** so the tube's end cap lands on the bumper.

- `BAR_LEG_LEN` — **DERIVED**, 66.06 mm.
- `BAR_HALF_Y` — **DERIVED**, 0.574387. No longer a free grade-E constant.
- `BAR_TIP_Y` — **FROZEN** at the rev-30..35 tip, written as the OLD FORMULA so
  the equality is provable rather than asserted. **THE BAR'S OUTER EXTENT DOES
  NOT MOVE**: `BAR_HALF_Y = 0.6000` was graded E "spans the nose as
  photographed", so what was matched to the photograph was the TIP, and it is
  the tip that is held. Every fraction ever published about this assembly
  carries `BAR_HALF_Y` in its denominator; freezing the tip rather than the root
  is what keeps the silhouette identical while the end changes.
- `BAR_END_BACK`, `BAR_END_DROP` — **RETIRED, not re-tuned.** Both grade E, no
  support. `BAR_END_BACK`'s only effect was to carry the end 17.5 mm rearward,
  **off the back of a blade top face only 24.8 mm deep — so no amount of extra
  drop could ever have landed the tube on it.**

**THE LANDING DATUM IS NOT `BLADE_TOP_Z`, AND THE FIRST ATTEMPT ASSUMED IT WAS.**
It landed on the blade's CROWN and the built gap came out **2.32 mm** instead of
zero. `BLADE_TOP_Z` is `bumper() z + BUMP_PROFILE max`, and that max sits at
outward 0.000, hard against the body; the channel's top **slopes away** — 0.0560
at outward 0, 0.0532 at 0.0150. The tube stands at outward 0.0123, where the
blade is **2.30 mm lower than its crown**, which is the 2.32 mm to 0.02 mm. A
**DATUM ERROR**, SPEC 10.24's indicator-lens family. `BLADE_TOP_Z` is
deliberately left alone — it anchors `BAR_Z` and verify.py's over-rider row, and
moving it to suit this derivation would silently re-baseline a guard.

**RESULT: 23.59 mm → 0.02 mm**, both ends, symmetric to 0.002 mm. The 0.02 mm is
mesh discretisation — the swept profile is a 6-segment rounded rect, not an
analytic circle.

#### 10.90.4  The guard, and the arm that caught its narration

`verify.py` gains **SPEC 10.90**, a **TWO-SIDED** ray-cast guard: it fails both
if the ends float AND if they sink into the blade, because *"touching"* bounded
on one side only is satisfied by driving the tube through the bumper.

Four falsification arms, all firing: landing datum reverted to the crown
(**2 fails**); straight leg removed (**2 fails**, 61.01 mm); leg over-driven
×1.5 (**2 fails**); ends made asymmetric (**2 fails**, including the symmetry
row at 6.166 mm).

**ARM 3 CAUGHT THE GUARD'S NARRATION, NOT ITS VERDICT.** With the tube driven
THROUGH the bumper the guard failed — correctly — with the message
*"floats 77.38 mm"*, **which is the opposite of what had happened.** A downward
ray started inside a solid leaves through a DOWN-facing surface, so the hit
normal's z sign separates float from penetration; the guard now does that.
**SPEC 10.87.2's family, and it was caught by READING THE ARM'S OUTPUT rather
than by noting that it went red.**

#### 10.90.5  THE OWNER RENAMES A COLUMN THE PROJECT HAS CONSUMED SINCE REV 32

Shown a 7× crop of the far end and asked what it shows, he answered — and his
answer was **none of the four options offered**, which by this project's own
rule means the option set did not reach far enough:

*[stated, rev 36]* "that circle is the post that connects the bumper to the bar,
and both continue past the post. past that, out of sight the bar wraps
downwards, and meets with the bumper, the same way it does on the close side"

**`u = 205–208` IS A POST'S OUTER EDGE, NOT THE BAR'S FAR END.** That column was
put to him TWICE — rev 33 Q1 and rev 34 Q1b — under the label *"the bar's far
end"*, and both answers were consumed as readings of a bar terminus. **HIS
READINGS WERE RIGHT; THE LABEL WAS WRONG.** Every C5 row from rev 32 onward
inherits it, and §10.88's retirement of the cross-ratio turned on *"the strut
sits 1.5 px from the bar's far end"* — a statement about a feature that is not
there.

Corroborated independently from the frame: the element stands **20–35 px
outboard of the vehicle's own green silhouette** (body edge cols 229–242, post
edge 205–213). Something proud of the body with the bar and bumper carrying on
behind it is exactly that geometry.

#### 10.90.6  §10.83 DISSOLVES: THERE ARE TWO POSTS AND NEITHER IS ON THE CENTRELINE

`probe_rev36_posts.py`, 5 controls, all passing.

| | column |
|---|---|
| FAR post centre | **219.5** (cols 214–225) |
| NEAR post centre | **362.5** (cols 359–366) |
| midpoint | **291.0** |
| centreline, §10.85 rev 31b, from the V-swage arms | **288.8 ± 3** |

The target is **read from `REF_MEASUREMENTS.md` at run time, not typed into the
probe**, so it was fixed five revisions before the claim existed and cannot have
been tuned to it.

**§10.83 has spent five revisions trying to place "the post at the vehicle's
centreline" and failing. THE QUESTION WAS UNANSWERABLE BECAUSE IT ASSUMED THERE
WAS ONE POST.** There are two and they straddle the centreline.

**PRICED, NOT ADMIRED.** Two columns drawn uniformly from the search window land
within 3 px of 288.8 **2.45 % of the time** — about **41:1**, not proof. And it
is **SENSITIVE**: with this probe's near-post column (362.5) the residual is
**0.73 of the band**; with the column the project has consumed since rev 32
(365.5) it is **1.23 — OUTSIDE**. **A RESULT THAT FLIPS ON A 3 px CHOICE IS
SUGGESTIVE, NOT ESTABLISHED**, and it is recorded at that strength.

**MY FIRST DETECTOR FOR THIS FIRED ON THE VEHICLE'S OWN CREAM V-SWAGE**,
reporting a 30 px "post" at cols 281–310 that is the body. Its falsification arm
caught two more above the bar. Three controls went down and **the probe refused
to rule.** The replacement keys on whether the bridge is **capped by the bar** —
a property of the bridge, not of what happens to be behind it.

#### 10.90.7  A THIRD ESTIMATOR WAS ENUMERATED AND ABANDONED BEFORE IT WAS BUILT

His statement makes the bar's span a **LOWER bound, not a reading** — it
continues past the far post and wraps out of sight. A construction to recover it
looked available: a 1-D projectivity is fixed by three collinear correspondences,
and the two posts plus a centreline would give three.

**IT NEEDS THE CENTRELINE'S IMAGE AT THE BAR'S HEIGHT AND DEPTH.** `u = 288.8`
is the V-swage apex — a different height at a different depth. **THAT IS EXACTLY
THE FEATURE §10.89 KILLED THE HARMONIC ROUTE FOR LACKING. THE SAME MISSING
FEATURE, A THIRD TIME.** Enumerated before building, not after. **NOT OPENED.**

#### 10.90.8  Defects of my own, six

1. **A FRAME ERROR, `verify.py` 11d2's, reproduced.** The first bar-end probe
   compared un-dropped constants against the dropped mesh and failed its own
   control C3 by **81.7 mm**. Caught before a number was published; rebuilt on
   ray-casts, which are frame-free by construction.
2. **A DETECTOR THAT FOUND THE WRONG OBJECT AND RETURNED A PLAUSIBLE NUMBER.**
   `mark_rev36_ends.py`'s first "bumper top edge right of the plate" read the
   **BAR TUBE**, which passes through the same rows, giving 24 px where the true
   rise is ~48. Replaced by a **topological** two-sided test — the column at
   which bar and bumper stop being one white body — which needs no discrimination
   at all.
3. **A SEARCH ANCHORED ON THE BOUNDARY IT WAS LAUNCHED FROM.** That replacement
   started at `EDGE+2`, on the antialiased edge pixel, where the body splits and
   the scan reads two runs immediately. It returned col 210 instead of 226.
4. **A POST DETECTOR KEYED ON BACKGROUND COLOUR** — §10.90.6 above.
5. **A GUARD WHOSE FAILURE MESSAGE DESCRIBED THE OPPOSITE DEFECT** — §10.90.4.
6. **THE LANDING DATUM** — §10.90.3.

**AND A SEVENTH, INHERITED AND NOT MINE: THE BRIEF I WAS HANDED HAD LOST HIS OWN
DEFECT REPORT ENTIRELY.** *"the upper bar appears to also connect with the main
bumper on either end"* appears in **NO** carrier that crosses contexts — not
`SPEC.md`, not `HANDOFF_rev35.md`, not anywhere in `NEXT_CONTEXT_PROMPT_rev36.md`,
whose §6 item 1 is the probe rewrite and whose §5 states *"NO QUESTION IS
OUTSTANDING WITH ME."* All four checked by grep. **The only surviving carrier
was memory.** Had the code been opened first, rev 36 would have rewritten two
probes and never touched the bar. **THE CARRIER THAT FAILED IS THE ONE HE PASTES
IN**, and that is the "travel between contexts consciously" failure by name.

#### 10.90.9  What is still not known, stated rather than papered over

- **WHERE ALONG THE BAR the junction sits.** The span is a LOWER bound. The
  build places it at the frozen tip because that is where the old build put it,
  and that is a CHOICE inherited, not a reading.
- **The manner of the junction at the NEAR end is UNOBSERVED.** Rows **725–732**
  at cols 470–510 carry **ZERO white and 50 % dark** — a black workshop frame
  member crosses the junction. Rev 35 reported *"one continuous white path"*
  there; **it read a junction through an occlusion**, and its crop stopped at
  v 730, inside the band. A **NEW MARK CLASS, the OCCLUSION BAND**, was added to
  say so on the figure — the first mark in this project that marks the *absence*
  of legibility rather than something legible. Its negative control matters:
  clear body reads zero white too, so **zero white alone proves nothing**; the
  band is an occlusion because it is 50 % DARK.
- **`BEND_R_RATIO` and `BEND_THETA` are image-space bounds, not 3-D readings.**

#### 10.90.10  A SEVENTH DEFECT OF MY OWN: I RE-DERIVED A TOTAL THAT THE THING ITSELF REPORTS

Verifying the inherited probe-control counts on the fresh clone, an ad-hoc
counter grepping `[PASS]`/`[FAIL]` tags disagreed with the brief on **three of
eight** probes, each by exactly one: `probe_rev34_levels` 7 against the brief's
8, `probe_rev34_ruling` 5 against 6, `probe_rev32_pointer` 9 against 10.

**THE BRIEF WAS RIGHT AND MY COUNTER WAS WRONG.** Every one of those probes
prints its own total — `CONTROLS: n checked, m FAILED` — and some of their
controls do not emit a bracketed tag, so a tag count under-reads by exactly the
number of untagged ones. Read from the probes' own summary lines, all eight
inherited counts confirm exactly: **18/6, 8/4, 6/4, 7/4, 6/1, 10/0, 6/0, 8/0.**

**THE RULE: WHEN AN INSTRUMENT REPORTS ITS OWN TOTAL, READ THAT TOTAL. DO NOT
RE-DERIVE IT FROM ITS SIDE EFFECTS.** A re-derivation is a second instrument,
and it needs its own control before it may contradict the first. Mine had none,
and had it been trusted it would have published three inherited counts as
"corrected" when they were already right — **the exact inverse of the grep trap,
and worse, because it would have looked like diligence.**

**FOUR OF THIS REVISION'S SEVEN DEFECTS ARE DETECTORS MEASURING THE WRONG
THING** — the bar tube read as the bumper's edge, the search anchored on its own
boundary, the post detector keyed on background colour, and this. Every one was
caught by a control or by a cross-check, none by inspection.


### 10.91  rev 37 — THE OVER-RIDER POSTS ARE BUILT: THE HALF OF THE OWNER'S "MODEL THEM" THAT WENT UNBUILT FOR ELEVEN REVISIONS, RECOVERED FROM MEMORY RATHER THAN FROM ANY CARRIER, AND BUILT WITH NO NEW CONSTANT

#### 10.91.1  THE INSTRUCTION HAD BEEN LOST — AND IT WAS ONE OF FOUR

rev 26 (§10.75) put three marked boxes on `ref_workshop.jpg` to the owner. He
ruled box **A** (the transverse tube) and box **C** (the vertical post between
tube and blade) **BOTH ON THE BUS**, and set the scope himself: **"MODEL THEM,
TAGGED WORKSHOP-STAGE."**

**THE BAR WAS BUILT IN REV 30. THE POST WAS NEVER BUILT.** By rev 37 the
instruction survived in **no document that crosses between contexts** — not in
SPEC's own open-items list, not in `HANDOFF_rev36.md`, not anywhere in
`NEXT_CONTEXT_PROMPT_rev37.md`, whose §6 work list did not name it and whose §5
declared *"NO QUESTION IS OUTSTANDING WITH ME."* **It survived only in memory.**

This is **§10.90's headline failure repeating at four times the scale.** Checking
the inherited brief against memory before opening the code — which §10.90 exists
to mandate — recovered **four** owner instructions, each verified against the
tree rather than taken on memory's word:

| # | his instruction | revision | verified how | state |
|---|---|---|---|---|
| 1 | "model them" — the bar **and the post** | rev 26 | `grep` finds no post member in `t1_detail.py` or `build.py` | **BUILT THIS REVISION** |
| 2 | Nolita photographs **re-admitted FOR GEOMETRY ONLY** | rev 15, §10.32 | `grep -ic nolita`: **8 in SPEC, 0 in REF_MEASUREMENTS** | **UNUSED, 21 revisions** |
| 3 | execute the **GitHub migration** on completion | rev 31c | absent from the rev-37 prompt; and see 10.91.2 | **UNFULFILLED** |
| 4 | region 3 was **not** selected as the bus's cream | rev 19 | contradicts rev 12's settled reading | **CLOSED BY HIM, rev 40 — it is the COUNTER'S FRONT FACE. §10.98.11** |

Item 2 matters beyond its own line: the brief lists `CREAM`, the absolute roof
height and the off flank's 804.9 mm as **photograph-blocked**, while an
**authorised source class for exactly those items has sat unused since rev 15.**

#### 10.91.2  A MEMORY ENTRY IS A CLAIM TOO, AND THIS ONE FAILED ITS CHECK

Memory recorded that the migration procedure was written as
`MIGRATION_APPENDIX_rev32.md` at **commit 159**. Both halves are false.
`git rev-list --all` walked, `git ls-tree` on every commit: **the file has never
existed in this repository**, and commit 159 is `afbf101`, SPEC 10.86.

So the owner's request is unfulfilled **and its supposed artefact is a phantom.**
**THE RULE: A MEMORY ENTRY IS A CLAIM AND MUST BE GREPPED LIKE ONE.** Memory
recovered four real instructions this revision and invented one artefact; the
recovery is only trustworthy *because* each item was checked against the tree.
The same discipline SPEC 10.62 applies to a citation applies here.

#### 10.91.3  WHY THIS ADDS NO NEW CONSTANT — the point of the entry

§10.90 **retired** two grade-E constants (`BAR_END_DROP`, `BAR_END_BACK`).
Re-adding a member with two fresh grade-E constants would be a **net provenance
loss on the same assembly one revision later.** It is not necessary:

| quantity | value | provenance |
|---|---|---|
| `POST_Y` | `IRON_Y` = 0.470 | the **EXISTING** bumper-iron station (rev 16), hoisted to a name so the post cannot be left behind if the iron moves (§10.25) |
| `POST_DIA` | `BAR_DIA` = 24.97 mm | the tube it joins. Inside the measured bracket below |
| `POST_LEN` | 75.29 mm | **DERIVED.** Zero freedom — the span between two established surfaces |

**THE SECTION IS BRACKETED, AND THE BRACKET IS OPERATOR-MISMATCHED, WHICH IS
STATED.** Two detectors in this tree measure the near post's width and disagree
by **2.9×**: rev 32's cream-run scan gives u 355–377 (**23 px**), §10.90.7's
capped-bridge gives u 359–366 (**8 px**). A threshold sweep resolves which is
which — the width jumps discontinuously **37 → 24 px between T=160 and T=170**,
the signature of a **merge separating**, so rev 32's figure is the post merged
with adjacent cream and the capped bridge is the separated core. §10.90 priced
the *centre* sensitivity of these two readings; **nobody had priced the WIDTH
disagreement, and the width is what a section needs.**

Against rev 26's threshold-swept tube (7.9–11.7 px) the post/tube ratio brackets
**0.68 – 1.52**. Ratio **1.00 sits inside it**, so `BAR_DIA` is *not excluded* —
and it is the only value that introduces nothing. **The two widths come from
different detectors and the bracket is therefore operator-mismatched; it is a
containment argument, not a measurement of the ratio.**

**MY OWN FIRST ATTEMPT AT THE SECTION FAILED, IN THE FAMILY §10.90 NAMED.** A
row-scan over cols 340–395 returned post/tube of **3.00–4.11, drifting, with a
discontinuity at T=170** — because the window merged the post with the nose's
cream V-swage. That is **§10.90's own post-detector defect reproduced**, and it
is why the capped bridge exists. Recorded rather than tidied away.

#### 10.91.4  TWO PREDICTIONS THE STATION MAKES, NEITHER USED TO CHOOSE IT

The bracket station is a **STRUCTURAL INFERENCE** — a post is carried by the
bumper's own bracket — **NOT a reading of the frame**, and it is graded as such.
It is falsifiable, and it survives two independent tests it was not fitted to:

1. **The owner's own sentence.** rev 36: *"both continue past the post."*
   `IRON_Y` 0.470 against the **DERIVED** `BAR_HALF_Y` 0.574387 is **0.8183** of
   the half-span, so the bar continues **104.4 mm outboard** before it begins to
   turn and **159.5 mm** to the frozen tip. **HIS SENTENCE IS SATISFIED, NOT
   ASSUMED.**
2. **A ± pair straddling the centreline**, which is independently what §10.90.7
   found at 41:1. That finding is **SUGGESTIVE, NOT ESTABLISHED** and is **NOT
   promoted here** — this is a consistency check, not a derivation from it.

**WHAT IS STILL NOT MEASURED, NAMED RATHER THAN IMPLIED:** the posts' true
lateral station in metres. §10.72 admits no px/m on the bumper plane; §10.88 and
§10.89 each retired a route on a precondition; §10.90.8 enumerated a third and
abandoned it before building it. **NO METRE SCALE IS INVENTED HERE.** A square-on
frame of the front closes it, and the WORKSHOP-STAGE tag is what lets the post
move when it arrives.

#### 10.91.5  A SUBSTRING BAN FIRED ON A MEMBER THE OWNER ASKED FOR

`verify.py`'s `BANNED` contains `"post"` — a **prophylactic** ban on pickup-era
geometry. It entered at the baseline commit with no history behind it, and
`git grep` across every commit in every ref shows **no object has ever been built
in this tree whose name contains "post"**: until rev 37 it had **never fired on
anything at all.** Then it fired on `orb_postP` / `orb_postM`.

**BOTH OBVIOUS REPAIRS ARE WRONG.** Renaming the object dodges the guard rather
than answering it, and leaves the next legitimate "post" failing identically.
Dropping `"post"` from `BANNED` deletes real coverage to fix a **scope** error,
against §10.41's rule that a guard tripping means the guard is working.

**THE REPAIR IS TO MAKE THE BAN SAY WHAT IT MEANS.** `BANNED_EXEMPT` matches the
**WHOLE lowercase name, never a substring**, and carries **its own two-sided
control**, run every time: four planted near-misses (`orb_postp_spare`,
`bedpost`, `post_l`, `xorb_postm`) must still be caught, and every exempt name
must be one `BANNED` actually matches. **A NAMED EXEMPTION IS A HOLE IN A GUARD,
SO PROVE THE HOLE IS THE SIZE IT CLAIMS.**

#### 10.91.6  THE GUARD, AND FOUR DETECTOR DEFECTS OF MY OWN INSIDE IT

SPEC 10.91's guard is **two-sided at BOTH ends** — floating and driven-in, at the
blade and at the bar — because "joins A to B" bounded on one side only is
satisfied by driving the post through the bumper. It **ray-casts**, because
§10.90's first attempt at this same measurement compared un-dropped constants
against the dropped mesh and was wrong by 81.7 mm.

**FOUR DEFECTS, EVERY ONE CAUGHT BY THE GUARD OR BY AN ARM'S OUTPUT, NONE BY
INSPECTION:**

1. **THE LANDING DATUM WAS THE CROWN — §10.90's OWN DATUM ERROR, REPRODUCED.**
   The first version took `max(_blade_top_at(lo), _blade_top_at(hi))` over the
   footprint, reasoning that the highest point cannot penetrate. **It returned
   `BLADE_TOP_Z`.** The mechanism is worth its own line: `_POST_OUT_HI` exceeds
   `_PROF_MAX_OUT` by **two microns**, so `_blade_top_at()` matched no bracket
   and returned its **final-point fallback, 35 mm low**. **A FUNCTION THAT
   ANSWERS ANYWAY OUTSIDE ITS DOMAIN SUPPLIED A DATUM** — §10.36's rule that a
   probe which cannot answer must return None rather than an endpoint, applied
   to a geometry helper. Sampling is now clamped to the profile's domain and
   asserted.
2. **"FOOTPRINT SAMPLING" THAT SAMPLED ONE VERTEX.** Selecting the cap by
   `abs(v.z - zlo) < 1e-6` collapses to a single vertex, because **step 8b
   shears the mesh** and a cap is not planar in z. So the fix for the
   single-vertex defect **was** the single-vertex defect. **It was caught only
   because the numbers did not move.** Caps are now clustered by a sorted split,
   with the separation-versus-spread precondition asserted.
3. **AN "OVERLAP" THAT WAS THE MEMBER'S OWN THICKNESS.** Casting in the
   direction of travel from a face that starts *inside* the target measures the
   distance to where the ray **left** it: it reported **108.24 mm**
   (`BUMP_PROFILE`'s full height) and **24.97 mm** (`BAR_DIA` exactly). Those two
   round numbers are the tell. **A PENETRATION DEPTH IS NOT A DISTANCE TO AN EXIT
   SURFACE.** Now a **signed height against the target's facing surface**,
   approached from outside — so the sign is a *subtraction*, not an inference
   from a normal.
4. **A THRESHOLD THAT CHANGED SIGN UNDERNEATH THE TEST.** Falsification ARM 4b
   lifted the post above the crown, driving `POST_WELD_MAX` to **−5.00 mm**, and
   a negative weld bound **inverts** the weld test: it fired on a **floating**
   post, printing *"DRIVEN INTO the bar — welded in −0.00 mm, past the bound
   −4.00 mm."* **§10.90's ARM-3 defect one level up** — not a message
   contradicting its own state but a *threshold* doing so — and caught the same
   way, **by reading the arm's output rather than noting that it went red.**
   Clamped at source, floored in the guard, with an explicit check so a future
   negative cannot be silently absorbed by the floor.

**THE TOLERANCE IS DELIBERATELY ASYMMETRIC AND SAYS SO.** A **gap** is a defect
at 1.0 mm. An **overlap is a weld** — a post welded to a curved channel top is
scribed into it, it does not hover above the crown — and it is bounded by
`POST_WELD_MAX`, **DERIVED from `BUMP_PROFILE`'s own crown-to-station slope**,
which moves if the profile does. It is not a free tolerance and it is not the
same number as the gap tolerance. **Calling a test "two-sided" without saying
which side is which is what §10.90's ARM 3 did.**

**BUILT RESULT: blade welded 2.25 mm, bar gap 0.41 mm, symmetric, tol 1.0 mm on
the gap side and 3.30 mm on the weld side.** The 2.25 mm is the crown-to-station
slope; the 0.41 mm is the tube's `seg=6` faceting.

#### 10.91.7  FALSIFIED IN SEVEN ARMS, AND ONE OF THEM IS A NON-ARM

| arm | planted | result |
|---|---|---|
| 1 | `POST_Y` outboard of `BAR_HALF_Y` | assert fires, naming both values |
| 2 | post **6 mm short** | *"floats 6.00 mm clear of the bar"* — magnitude and side both right |
| 3 | post **8 mm long** | *"DRIVEN INTO the bar, welded in 8.00 mm"* — the side §10.90's ARM 3 got wrong |
| **4** | **land on the crown** | **0 fail — A NON-ARM** |
| 4b | post lifted 5 mm above the crown | *"floats 5.05 mm clear of the blade"* (after defect 4 above was fixed) |
| 5 | build ONE post | count check fires, citing §10.90.7 |
| 6 | post renamed so it is not exempt | `BANNED` still fires |
| 7 | exemption widened to a name `BANNED` never matched | the exemption's own control fires |

**ARM 4 IS PUBLISHED AS A NON-ARM RATHER THAN QUIETLY DROPPED.** Landing on the
crown — the original defect — gives **0 fail**, because a flat-bottomed post on a
sloping channel touches *somewhere* either way. **THE GUARD BOUNDS THE JOINT TO
WITHIN `BUMP_PROFILE`'s OWN 2.30 mm CROWN-TO-STATION SLOPE BUT DOES NOT FIX WHERE
IN THAT BAND THE BOTTOM SITS. THAT IS ITS CEILING.** Fifth revision running in
which an arm has turned out not to be an arm (§10.89's ARM 5, four revisions).

**AND THE LOG LINE WAS ASSERTING ITS OWN DATUM.** It read *"landed on
`_blade_top_at(axis)`, NOT on the crown"* as fixed prose — **a sentence that was
FALSE under ARM 4 while the guard passed.** §10.52's rule — a claim in prose is
not a guard, *including inside the guard*. It now **prints the measured offset
from the crown**, so ARM 4 self-reports as `+0.00 mm relative to the crown` and
the non-arm is **legible instead of silent.**


### 10.92  rev 37 — REGION 3 IS RE-PUT TO THE OWNER: A CONTRADICTION BETWEEN ONE OF HIS OWN READINGS AND A SETTLED ENTRY, UNASKED SINCE REV 19

> **ANSWERED IN REV 40 — see §10.98.11.** *[stated, rev 40]* the pale band is
> **THE COUNTER'S FRONT FACE**. rev 12's "that band is the body's own belt
> paint" is SUPERSEDED BY HIM. **Do not re-put this question.**

**rev 12**, from his own answer, settled the counter as a *"tan top, brass nosing
on the OUTER EDGE, **body cream below**"* — the pale band under the nosing is the
**vehicle's own belt paint**.

**rev 19**, shown four candidate cream regions and asked which were the bus's own
painted cream, he selected **only region 2** and **did not select region 3**,
which is that band. The two readings disagree. The rev-19 record itself says it
was *"worth re-putting to him, it was not chased in rev 19"* — and it was not
chased in rev 20–36 either, nor did it appear in any open-items list.

**WHAT THE ANSWER CLOSES.** Whether `countercream` should carry that band at all.
It is currently painted by the **counter's** material; if it is the body's belt
paint it belongs to `body_paint`'s cream and inherits the flank's weathering,
fade and dust, **none of which the counter's material applies**. That is a
**shader-routing** consequence, not a geometry one. It also bears on
`COUNTERTAN`'s level bracket, whose fascia arm sits directly below this band.
**NOTHING MOVES UNTIL HE ANSWERS.**

**THE FIGURE IS DELIBERATELY PLAIN, AND THAT IS §10.90's LESSON APPLIED.** One 7×
crop of `ref_side.jpg` (u 556–700, v 396–448, printed), **ONE red circle**, one
sentence. rev 36's first question figure carried five mark classes, printed crop
boxes, a coalescence column and a priced null, and produced *"i don't understand
what is being asked."* The single mark is a **POINTER**; `mark_rev37_region3.py`
**reads no pixels for any number**, because adding a sampling window would mix
mark classes and reproduce the defect. It **refuses to write** if the crop leaves
the frame or if the mark falls outside its own crop.

#### 10.91.8  BUILT, THEN WITHDRAWN BY THE OWNER IN THE SAME REVISION

He chose the post as rev 37's work, was shown what it would cost and what it
would not close, and then — after the build, the guard, the seven arms and the
SPEC entry were complete — said:

> *"I want to change my decision back, sorry. I want to stick to the original
> bumper."*

**THE GEOMETRY IS WITHDRAWN. `build.py`'s call is COMMENTED, NOT DELETED**, and
`overrider_posts()` stays defined — the treatment §2.4 gives the rear bumper
eight lines above it in the same file. Re-enabling is one line. **The model is
back to 127 objects and 186 meshes, and every inherited figure is identical to
rev 30–36's.**

**THE GUARD IS KEPT ARMED, NOT DELETED.** With zero posts it logs **NOT
APPLICABLE — stated, not silently skipped**, the treatment `gap_englid` already
gets; with two it runs in full. **A WITHDRAWN FEATURE WHOSE GUARD WAS DELETED
COMES BACK UNGUARDED**, and this project has been burned that way before. The
one commented line therefore restores full coverage with no edit to `verify.py`.

**WHAT SURVIVES THE WITHDRAWAL, AND IS THE REAL YIELD OF THE REVISION:**

- **Four of his own instructions recovered** from memory and verified against the
  tree (§10.91.1). Three remain outstanding regardless of the post.
- **A memory entry proved to be a phantom** (§10.91.2) — and the rule that a
  memory entry is a claim and must be grepped like one.
- **The near post's WIDTH disagreement priced at 2.9×** and resolved as a merge
  separating at T=170 (§10.91.3). §10.90 priced the *centre* sensitivity of those
  two readings and nobody had priced the width.
- **A substring ban that had never fired in the project's history** was found
  mis-scoped, and repaired with an exemption carrying its own control (§10.91.5).
  **This is live and load-bearing whether or not any post is built.**
- **Four detector defects** of my own (§10.91.6) and a **non-arm published as
  one** with the guard's ceiling stated (§10.91.7).

**NOTHING HERE ARGUES WITH THE DECISION.** The lateral station was always a
STRUCTURAL INFERENCE and never a measurement (§10.91.4); §10.72 still admits no
px/m on the bumper plane. **A member the reference cannot place is a member the
owner is entitled to decline**, and declining it costs the model nothing that was
ever measured.


### 10.93  rev 37 — THE WHOLE OVER-RIDER ASSEMBLY IS WITHDRAWN ON THE OWNER'S DECISION: THE FRONT RETURNS TO A PLAIN BLADE

Having chosen the post as rev 37's work and then reversed that, he was asked how
far back *"the original bumper"* reached — deliberately, because the bar (rev 30)
and its hoop ends (rev 36) are older work and one of them came from his own
defect report. Given three scopes, he chose the widest: **remove the over-rider
bar entirely, leaving a plain bumper blade.**

**THIS IS CONSISTENT WITH THE PROJECT'S OWN PRECEDENT, NOT CONTRARY TO IT**, and
that is worth stating because it looks at first like it overturns his rev-26
ruling. It does not. §10.75 records the scope *he* set — **WORKSHOP-STAGE,
TAGGED** — and the reason he set it: `ref_workshop.jpg` is the **conversion**
stage, §2.4 records that the **rear** bumper was removed between that stage and
service, and **no in-service frame shows the nose.** Workshop-stage hardware is
not automatically in-service hardware. **The tag existed precisely so this could
be pulled back out, and it has been.** `build.py` already carries the rear
bumper commented out on the identical argument, a few lines above.

**His rev-26 reading that the tube and post are ON THE BUS is NOT overturned** —
it was a reading of a workshop photograph and it stands as one. What changed is
the scope decision layered on top of it, and that was always his to make.

**WHAT IS IN THE MODEL NOW:** the front bumper is the cream blade plus its two
irons. **126 objects, 185 meshes, 0 non-manifold, 42 materials, guards 0 fail /
0 warn at both levels.** Every body figure — roof crown, rake, both arch lips,
bay widths, `CARGO_GAP`, shut lines, dimensions — is **identical to rev 30–36's.**

**COMMENTED, NOT DELETED, AND THE GUARDS ARE KEPT ARMED.** `overrider_bar()` and
`overrider_posts()` both stay defined; two `build.py` lines are commented. With
the assembly absent, §§10.83 / 10.90 / 10.91 log **NOT APPLICABLE — stated, not
silently skipped**, the treatment `gap_englid` already gets. **A WITHDRAWN
FEATURE WHOSE GUARD WAS DELETED COMES BACK UNGUARDED**, so nothing was removed,
and the claim that the guards are merely dormant was **PROVEN BY TWO ARMS**, not
asserted:

| arm | result |
|---|---|
| re-enable the bar | §10.83's and §10.90's rows **come back alive**, 127 objects |
| re-enable it with `BAR_LEG_LEN` × 0.8 | §10.90 **FAILS**: *"floats 12.36 mm above the bumper"*, both ends |

**Re-enabling is one line and requires no edit to `verify.py`.**

**WHAT THIS COSTS THE MODEL: nothing that was ever measured.** The bar's scale
was anchored to a **CATALOGUE** 0.180 m aperture — §10.72's struck class — its
standoff in x was a **CHOICE**, its lateral extent was graded **E**, and the
posts' lateral station was a **STRUCTURAL INFERENCE** (§10.91.4). §10.72 still
admits no px/m on the bumper plane. **A MEMBER THE REFERENCE CANNOT PLACE IS A
MEMBER THE OWNER IS ENTITLED TO DECLINE.**

**WHAT SURVIVES AND IS NOW THE REVISION'S YIELD:** everything in §10.91.8's list,
none of which depends on a post or a bar existing — four recovered instructions,
a phantom memory entry, the 2.9× width disagreement priced, the mis-scoped
`BANNED` substring repaired with its own control, four detector defects and a
published non-arm. **The `BANNED` repair is live regardless.**

**DO NOT RE-PROPOSE THE OVER-RIDER** without a square-on frame of the front, or
his say-so. It is answered, not open.


### 10.94  rev 37 — THE OWNER'S FOUR DEFECT REPORTS OFF THE REV-37 HERO, AND THREE OF THEM CORROBORATE FINDINGS THIS PROJECT MEASURED AND NEVER APPLIED

Shown `rev37_hero34f.png`, he reported, verbatim:

> *"I see a few things, the front nose is shaped inaccurately, it looks more like
> the front of an amtrak train than a vw bus, also we need to fix the vw logo,
> also the paint job and the headlights are not alligned"*

**THIS IS THE STRONGEST CORROBORATION EVENT IN THE PROJECT'S HISTORY.** Three of
the four land on findings that were **measured, then refuted on a third method,
then reverted, and left open** — in one case for twenty-seven revisions. Each
mapping below was **verified by grep against SPEC and the build files**, not
taken from memory: this revision's own §10.91.2 rule.

| his report | the existing finding | status before he spoke |
|---|---|---|
| *"the paint job and the headlights are not alligned"* | **§10.24 item 3.** Headlamp centre = belt − 0.339 ± 0.025 m photographed against the build's **belt − 0.242**, a **97 mm discrepancy at ~3.9 σ** | **OPEN since rev 10**, "NOT applied... deserves a second derivation first" |
| *"we need to fix the vw logo"* | **§10.25's PREMISE IS FALSE.** There was never a 12.7 mm air gap between the V's apex and the W's peak — SPEC's own later entry records **"no gap but a 52 mm interpenetration"** | the rev-10 coupling fix made the glyph SMALLER, hiding the fusion without removing it |
| *"the front nose is shaped inaccurately... more like the front of an amtrak train"* | **`V_POW` locked at 0.60** (§10.2, `t1_shell.py:1070`). The rev-11 audit measured the V-swage arm rising **~2× too fast** — lamp station to body edge **0.111 ± 0.015 m photographed against 0.208 built** — implying **`V_POW` ≈ 0.30–0.48** | measured, never applied |

**THE SECOND DERIVATION §10.24 ASKED FOR EXISTS AND WAS NEVER SWEPT BACK INTO
IT.** The rev-11 audit confirmed the headlamp position **twice**: at **83 ± 19 mm,
4.4 σ**, by a pure ratio needing no px/m, no belt and no ground line
(roundel-to-lamp separation 0.628 ± 0.066 roundel diameters); and **by a test
needing no scale at all — in the photograph the indicator aperture lies BELOW the
two-tone break, and in the build it lies ABOVE it.** That last sentence *is* the
owner's report, arrived at independently. **§10.24's stated blocker was
discharged and the entry never learned of it** — the same carrier failure as
§10.91.1, inside SPEC rather than between contexts.

**THE TRAP, RECORDED BEFORE ANYONE ACTS: DO NOT MOVE THE ROUNDEL WITH THE
LAMPS.** The roundel's own height is supported by **both** chains. §10.24's three
findings were applied together once and reverted together once; the lesson from
that revert is that they are **not one change**.

**REPORT 3 IS ONE REPORT ABOUT A RELATIONSHIP, NOT TWO.** He said the paint and
the headlamps are not aligned **with each other**. Splitting it into "the paint"
and "the headlamps" as independent items would lose the only thing it constrains
— and the scale-free test above is a test of exactly that relationship, which is
why it needs no px/m.

**NOTHING WAS BUILT ON THIS IN REV 37.** Four geometry and shader changes at the
end of a shipped revision is how this project has been burned before (§10.89's
rule, written when the bar's ends were left to rev 36). **They are rev 38's item
1, with the numbers already in hand and the trap already named.**

**AND THE HERO IS WHAT SURFACED THEM.** `rev37_hero34f.png` is an honest
photograph of a build with three known defects in its face. That is what a hero
is for, and it is the argument against deferring one again.


### 10.95  rev 37 — HIS SECOND BATCH OFF THE SAME HERO: FOUR MORE, AND TWO OF THEM ARE ONE DEFECT

> *"Also, the doors extend lower, around the wheel well, also there seems to be a
> bar obstructing the front wheel? also '100% calidad' is off center, and we
> there are two bars propping up the art sign on either side, not one"*

**EIGHT DEFECT REPORTS FROM HIM IN ONE SESSION, ALL OFF ONE HERO.** That is the
argument against ever deferring one: `rev30_hero34f.png` was superseded in rev 36
and never re-shot, so these eight sat unseen for seven revisions. **SHOOT THE
HERO ON EVERY REVISION THAT MOVES GEOMETRY.**

#### 10.95.1  REPORT 8 — THE SIGN'S STRUTS. CONFIRMED AGAINST THE BUILD, COST: ONE GREP

**HE IS RIGHT AND THE BUILD IS WRONG.** `t1_shell.signboard()` ends with a
**single** `struts.append(T.cylinder(..., name="sign_strut"))` — **no loop over
sides, one strut.** He reports **two, one on either side.**

**A COUNT IS THE CHEAPEST CLAIM IN THIS PROJECT TO CHECK AND THE HARDEST TO
ARGUE WITH**, and this one took a single grep. It needs no scale, no px/m and no
camera model — which is why it is the first of the eight that should be built.

#### 10.95.2  REPORTS 5 AND 6 ARE ONE DEFECT, NOT TWO

He reports the doors should **extend lower, around the wheel well**, and — as a
**question**, so he is unsure — that **"there seems to be a bar obstructing the
front wheel?"** The geometry says these are the same fault seen from two sides:

| object | extent (dropped frame) |
|---|---|
| `doorback1` — the door's inner back panel | x **[0.918, 1.824]**, y [0.796, 0.857], z **[0.717, 1.755]** |
| `tyre1.31` | z top **0.665** |

`doorback1`'s **lower edge stands 52 mm above the tyre's crown and runs the whole
length of the arch**, at y 0.796–0.857 — just inboard of the skin. **If the cab
door's outer skin does not reach as low as he says it should, the inner back
panel is what shows through the arch opening — and it would read exactly as a
grey bar across the wheel.**

**CORROBORATED BY THE BAR'S OWN END.** In `hero34f` the vehicle's nose is to
frame-left, so image-right is decreasing x. The bar's blunt right-hand end in the
render coincides with **`doorback1`'s rear edge at x = 0.918.**

**THIS IS A WELL-EVIDENCED IDENTIFICATION, NOT A CONFIRMED ONE, AND IT IS
LABELLED AS SUCH.** An ablation was attempted and **did not run** — the harness
failed to resolve the `hero34f` camera, and appending the removal to `build.py`
would have executed *after* the preview render, i.e. in the wrong order. **No
ablation result is reported, because none was obtained.** rev 38's first act on
this item is to run it: delete `doorback1`/`doorback-1`, re-render the crop, and
see whether the bar goes. **If it does, reports 5 and 6 are one fix; if it does
not, report 6 is a separate object and the search starts again.**

`_DOOR_TOP_AUTH` and `DOOR_H` are **AUTHORED, not measured** (§10.73), and the
door's **lower** boundary has never been measured by any revision — so there is
no locked value standing against his reading.

#### 10.95.3  REPORT 7 — "100% CALIDAD" IS OFF CENTRE

`cal_gen.py:246` sets `glyph_calidad(t, w * 0.180, h * 0.645, h * 0.196)` — an
absolute x of **0.180 of the texture width**, not a centred placement. Whether
the defect is inside the texture or in the panel the texture lands on is **not
yet determined and must not be guessed**: §10.20's family, where a lockup looked
wrong because the *panel* aspect was stale rather than the artwork.

**NOTE THE DISTINCTION FROM HIS EARLIER STICKER COMPLAINT.** On the sticker he
raised **"'100% CALIDAD' legibility"**, more than once. **This is a PLACEMENT
report and it is new.** Do not merge them.

#### 10.95.4  WHAT IS BUILT ON ANY OF THE EIGHT: NOTHING

Eight reports, four of them geometry, at the end of a shipped revision. §10.89's
rule — rushing a geometry change at the end of a revision is how this project has
been burned — applies eightfold. **They are rev 38's item 1**, ordered by what
each costs to establish:

1. **the sign's second strut** — a count, confirmed, needs nothing
2. **the door / front-wheel bar** — run the ablation FIRST, then decide if it is one fix or two
3. **the headlamp / two-tone alignment** (§10.94) — the measurement exists at 4.4 σ and its scale-free arm needs no px/m. **DO NOT MOVE THE ROUNDEL WITH IT**
4. **the VW glyph** — §10.25's premise is false; rebuild against the 52 mm interpenetration
5. **`V_POW`** — 0.60 locked against an implied 0.30–0.48; re-fit, and **mirror into `t1_shell.nose_shape.zV` or the pressed swage and the painted break de-register**
6. **"100% Calidad"** — determine texture-versus-panel before touching either

### 10.96  rev 38 — HIS REPORT 6 IS NOT A DOOR PART: IT IS THE CAB FLOOR, SEEN THROUGH A WHEEL ARCH THAT HAS NOTHING BEHIND IT. FOUR WHEEL HOUSES BUILT, BOTH FLOOR PANS NARROWED, AND THE HERO CATCHES TWO DEFECTS THE GUARDS PASSED

His report 6, verbatim, off `rev37_hero34f.png`: *"also there seems to be a bar
obstructing the front wheel?"* — phrased as a question, so treated as an
observation to check, not a settled reading.

#### 10.96.1  The brief's candidate was ablated and REFUTED

`NEXT_CONTEXT_PROMPT_rev38.md` §6 item 2 identified `doorback1`, spanning
x [0.918, 1.824] with its lower edge at z 0.717, and instructed: *"Delete
`doorback1` / `doorback-1`, re-render the crop, and look. If the bar goes,
reports 5 and 6 are ONE fix. If not, report 6 is a different object and the
search restarts."*

Rev 37 attempted this and could not run it, because appending the removal to
`build.py` executes AFTER the `T1_PREVIEW` block has already rendered. Rev 38
added **`T1_ABLATE`** UPSTREAM of that block, with a positive control: **a name
matching nothing RAISES and writes no frame.** An ablation that silently
removes zero objects renders a frame identical to the baseline, and "identical"
is exactly the reading that would be misread as *"the object was not the bar"* —
a false negative dressed as a finding. Armed on a bogus name; it refused.

Ablation run: `doorback1` (304v) and `doorback-1` (304v) removed, `hero34f`
re-rendered at 1600x1067. **612 pixels of 1.7 M changed, none of them the bar.**
The member is pixel-identical. **THE CANDIDATE IS REFUTED**, and by the brief's
own rule the search restarted.

#### 10.96.2  Identified by construction, not by inference

`probe_rev38_wheelbar.py` casts rays from the `hero34f` camera through a grid of
pixels covering the member and reports the FIRST object hit. No colour, no
threshold, no segmentation. Result: **`cab_floor`** — 99 hits in the member
window, **308** across the whole front arch, first hit, nothing in front of it.

**THE ROOT CAUSE IS ONE NUMBER.** `cab_floor` was `rrect(1.560, 0.960)`,
half-width **0.780**, against a front tyre whose OUTER face is at **0.760** — it
stood 20 mm proud of the wheel. `van_floor` was `rrect(1.400, 2.700)`,
half-width 0.700, i.e. 55 mm INBOARD, and the rear arch showed **9** interior
rays against the front's 308. A 34x difference explained entirely by 80 mm a side.

**AND THERE WAS NO WHEEL HOUSE ANYWHERE IN THE BUILD** — `grep` finds no
`liner`, `inner_wing`, `wheelwell`, `wheel_well` or `splash`. Each arch is a
cylinder cut clean through the skin with nothing behind it, so the cab interior
is in plain sight from outside.

#### 10.96.3  THE CONTROL FAILED, AND ITS FAILURE IS THE FINDING

`probe_rev38_floorpen.py` tests floor-vs-wheel interpenetration by BVH overlap
on the EVALUATED, WORLD-SPACE meshes — not a bounding-box test, because
bounding boxes overlap for many pairs that never touch and a bbox claim is not
an interpenetration claim.

    cab_floor  vs tyre1.31 / tyre1.3-1              240 face pairs each
               vs rim1.31_barrel / rim1.3-1_barrel   76 each     632 total
    van_floor  vs tyre-1.11 / tyre-1.1-1            152 each
               vs rim-1.11_barrel / rim-1.1-1_barrel 110 each    524 total

The `van_floor` row was written as the CONTROL for the cab-floor claim, and it
**FAILED**. That failure is what showed the defect is **SYSTEMIC, NOT A CAB
QUIRK**: both floor pans pass through all four wheels, because there are no
wheel houses to stop them. The 1.560 slab was not merely invisible-and-wrong,
it was geometrically impossible. **A CONTROL THAT FAILS IS A RESULT, NOT A
BROKEN INSTRUMENT.**

Both widths were **AUTHORED** — neither 1.560 nor 1.400 appears anywhere in
`SPEC.md` or `REF_MEASUREMENTS.md`. Nothing measured is overturned.

#### 10.96.4  What was built

* **`FLOOR_W = 1.200`** for both pans (half-width 0.600): clears the front
  tyre's inner face (0.609) by 9 mm and the rear's (0.604) by 4 mm. A narrow
  footwell between two wheel-house humps is also what a real T1 has. **THIS IS
  NOT A MEASUREMENT OF THE VEHICLE and is not tagged as one** — it replaces an
  authored number that is impossible with an authored number that is possible.
  No photograph shows this vehicle's cab floor and none is claimed.
* **Four wheel houses**, `wheelhouse{axle}{side}`, arc shells of radius
  `WH_R = ARCH_R` about each axle, flanged inward, sweeping the UPPER sector
  only, with the OUTBOARD face following `T.flank_y`.
* **The second lid strut** — see 10.96.6.

Post-repair, measured: **0 overlapping face pairs** for both pans against all
wheel parts (was 632 / 524), and **0 interior-object rays** through either arch
(front was 308, rear 9).

#### 10.96.5  THE HERO CAUGHT TWO DEFECTS EVERY GUARD PASSED

**This is rev 37's rule earning its keep twice inside one revision.**

1. The first wheel house used `T.revolve` — a FULL 360 degree surface. Guards:
   **0 fail, 0 warn, 0 non-manifold, 0 interior rays, C1-C6 all PASS.** The
   render showed **a dark skirt hanging in mid-air below the sill, outboard of
   the bumper line.** The bodywork exists only above the arch's horizontal
   diameter; below it the arch is open to the road.
2. The second used an arc sector but a FIXED outboard y of 0.877. Guards passed
   again. The render showed the liner standing proud of the skin. **Measured**
   on the arch rim, `T.flank_y` runs **0.873 at the crown down to 0.801 (front)
   and 0.787 (rear)** near horizontal — so one number stands proud by up to
   **90 mm** at the sector ends. Repaired by making the outboard face conform.

**NEITHER WAS VISIBLE TO ANY GUARD OR ANY PROBE.** A guard tests the property
you thought to name. Only the render tests the property you did not.

#### 10.96.6  REPORT 8 — the second strut, and the brief named the wrong function

His words: *"we there are two bars propping up the art sign on either side, not
one"*. A COUNT — the cheapest class of observation, needing no scale, no px/m
and no camera model.

`NEXT_CONTEXT_PROMPT_rev38.md` §6 item 1 attributed this to
`t1_shell.signboard()`'s single `sign_strut` and called it **"CONFIRMED, BUILD
IT FIRST."** **THAT IS THE WRONG OBJECT.** `signboard()` returns
`[], [], []` unless `T1_SIGNBOARD=1`, which is **not the default**, and SPEC and
`HANDOFF_rev12.md` both forbid rendering a hero with it on — so **no
`sign_strut` exists in any shipped frame, including the one he was looking at.**

The strut he can see is **`lid_strut0`**, from `t1_shell.roof_lids()`, where the
loop ran over a ONE-ELEMENT tuple. **HIS REPORT WAS RIGHT; THE ATTRIBUTION WAS
NOT.** Second strut added symmetrically at `LID_X0 - 0.16` against the existing
`LID_X1 + 0.16`. Confirmed in the render: two struts, one at each end.

#### 10.96.7  TWO INHERITED PROBE FIGURES IN THE BRIEF WERE PRE-WITHDRAWAL

The brief published `probe_rev36_barend` **8/0** and `probe_dust_scope` **8/0**.
On arrival, measured:

* `probe_rev36_barend`: `[FAIL] C1 orb_bar: 0 object(s)` ->
  **"REFUSING TO PRINT A RULING -- a positive control is down."** The bar was
  withdrawn in rev 37, so it cannot rule. **The probe behaved correctly; the
  brief's number was stale.** Left alone: it must stay armed for the built case.
* `probe_dust_scope`: **8 checked, 1 FAILED** — `mesh count matches audit.py's
  published 186`, hard-coded, against a build now publishing 185.

**THAT LITERAL HAS NOW DRIFTED TWICE, IN BOTH DIRECTIONS.** rev 30 added
`orb_bar` (185 -> 186) without sweeping it; rev 32 found it and wrote above it
*"A CONTROL NOBODY RUNS IS NOT A CONTROL."* rev 37 withdrew the bar
(186 -> 185) without sweeping it either. Corrected to **190**, not loosened.

**THE RULE THE TWO MISSES SHARE, AND IT IS NEW:** rev 37 wrote down *shoot the
hero every revision that moves geometry*. **IT HAS A SIBLING NOBODY WROTE DOWN:
RE-RUN THE PROBES TOO.** A revision that moves geometry invalidates every
literal that counts it.

#### 10.96.8  Reports 5 and 6 are NOT one fix

The brief hoped they were. The ablation refuted the shared cause. Report 6 is
`cab_floor` plus the missing wheel houses — **CLOSED in rev 38**. Report 5, the
cab door reaching lower and wrapping the wheel well, is the door outline's lower
boundary: `doorback1` runs z **0.717 -> 1.755**, its bottom a straight line
**52 mm above the tyre crown (0.665)**, not following the arch. `_DOOR_TOP_AUTH`
and `DOOR_H` are AUTHORED, not measured, and the door's LOWER boundary has never
been measured. **OPEN, and rev 39's item 1.**

#### 10.96.9  Two detector defects of mine, both caught by controls

* **THE FIRST DRAFT OF `probe_rev38_wheelbar.py` RAN AGAINST BLENDER'S DEFAULT
  STARTUP CUBE.** It never built the vehicle. Every ray hit `Cube` and it
  printed a confident, well-formatted, entirely fictional tally with a bounding
  box. **C1-C3 caught it.** A ray-caster that hits SOMETHING always produces a
  plausible answer. Fixed to use the project's own truncated-exec idiom.
* **MY "REAR ARCH" CONTROL WINDOW LANDED ON THE NOSE** — it was returning
  `vw_ring` and `hl_lens`. Added **C5**, which asserts the window actually lands
  on a rear wheel, rather than reporting a control I had mis-aimed.
* And **C1's SCOPE was wrong, not its result**: the pixel lands on the hub cap,
  which IS a wheel part, and the first draft asked for `"tyre"` in the name.
  **Repair the scope; never re-aim the ray until it hits the name you first
  wrote down.**

#### 10.96.10  A guard fired on the first build and it was right

Setting `ob.location` on the wheel houses tripped `build.py`'s step-8b assert:
the shear reads `v.co.x` as world x and requires an identity transform on every
mesh. The offset was baked into the MESH instead. **The geometry is what moves,
never the guard.**


### 10.97  rev 39 — THE OWNER'S OWN METHOD RUN AT LAST: THE BROADSIDE LAID OVER `ref_side.jpg`. `flank_compare.py` EXECUTED FOR THE FIRST TIME IN THE PROJECT, SPEC 10.35's MAP VALIDATED END TO END AT 5 mm, AND §10.24 CORROBORATED A FOURTH TIME BY A ROUTE THAT TOUCHES NO HEADLAMP

#### 10.97.1  The instruction, and why it had never been carried out

*[stated]* **"For the model work he wants fixes driven off the broadside render
laid over `ref_side.jpg` at matched scale"** — that flank carries the script,
folk art, counter, Calidad decal, belt line, stance and arches. Recorded in
rev 10 and never executed. `flank_compare.py` was written for the SCRIPT LOCKUP,
was recorded NOT RUN in rev 10, and **is not mentioned again in twenty-eight
revisions.** The whole-vehicle comparison has not been made since rev 16.

The owner chose this over doing his Report 5 directly, over Reports 3+4, and
over the sticker, on the argument that it **grounds** the door fix rather than
authoring it.

#### 10.97.2  `flank_compare.py` — the actual output, not a summary

```
PASS  ink area ratio   0.9366            target 1.000 +/- 0.10
PASS  ink aspect       2.3622 vs 2.2527  target within 5 %  (+4.86 %)
PASS  IoU vs ceiling   0.7627 = 0.889 of the 0.8584 measured that run
FAIL  worst region     0.503 (Senor)     target >= 0.75 of its own ceiling
FAIL  -- flank script, render against ref_side.jpg
```

**The verdict is not the finding.** The finding is its registration line:

> *the render's lockup has to move **+76.2 mm forward and +61.9 mm down** to sit
> where the calibrated map puts the photograph's.*

Cross-checked in the same run by a route sharing no step with it: `SCR`'s own x
extents sit **+83 / +80 mm** aft of `flank_X(LOCKUP)`, and the cream/red
differential puts the ink top **−36.9 mm** high. Height **−31.5 mm (−5.5 %)**.

rev 17 carried *"`SCR` is +80 mm aft and 12–24 mm short"* forward for **22
revisions** unapplied. It is now re-measured two ways and **the height deficit is
31.5 mm, not 12–24.**

Its positive control localises the fault and that matters more than the number:
texture-alone IoU **0.7667** against the render's **0.7627**, so **the render and
the whole chromaticity mask rule together are worth −0.005 of ceiling.
Everything between 0.893 and 1.000 is the PANEL.**

**NOT APPLIED.** `SCR`'s vertical term is measured against the cream/red break,
which §10.97.5 shows is itself the misplaced member. Applying both would double
count. §10.29's rule — *re-fit jointly, never separately*.

#### 10.97.3  The whole-flank overlay, and NO NEW ESTIMATOR

`probe_rev39_flank.py`, READ-ONLY. The ortho broadside is carried into
`ref_side.jpg`'s own projective frame using only instruments already calibrated
here and IMPORTED, never re-typed: `flank_compare`'s `flank_X` / `flank_u` /
`flank_mpp` / `flank_kv` (§10.34 + §10.35), its exact ortho `projector()`, and
the cream/red two-tone break which `flank_compare` fits in BOTH frames and uses
as ONE datum precisely so its own height never enters. Neither image is
resampled onto the other.

§10.79 and §10.89 each died on a panel after a second estimator was opened;
§10.90 enumerated a third and abandoned it before building it. **This opens
none.**

* **C1** the projector reproduces `flank_compare`'s own printed self-check —
  model z=0 at render row **827.2**, published 827.2.
* **C2** `flank_kv(749.38)` reduces to §10.34's `k_t` = **215.5 px/m**.

#### 10.97.4  HORIZONTAL: SPEC 10.35's map validated end to end at 5 mm

Registered over the whole vehicle: **−1 px = −5 mm.** The map has been used for
twenty-three revisions and has never before been checked against a rendered
model across its whole range. It is very good.

#### 10.97.5  VERTICAL: 81 ± 7 mm, FLAT, and it is the BREAK LINE

The warp pins the model's break onto the photograph's, so the residual is the
whole BODY against the BREAK. **This is a relative measurement by construction
and must never be quoted as a ride-height one.**

Registered in five COLUMN bands over u 200–900: **+15, +19, +19, +15, +18 px,
spread 4 px**, fit slope 1.0 px over 700 columns. Flat in u.

Registered in ten Z bands, selected by **model z** — the field the warp is built
from — so every band spans the full width and cannot alias onto one horizontal
line:

```
  0.10-0.40  +16  +77 mm      0.90-1.20  +19  +92 mm      1.50-1.80  +16  +77 mm
  0.30-0.60  +16  +77 mm      1.10-1.40  +19  +92 mm      1.70-2.00  +16  +77 mm
  0.50-0.80  +15  +72 mm      1.30-1.60      DECLINED     1.90-2.20      DECLINED
  0.70-1.00      DECLINED
```

**7 answered, 3 declined. dy = 81 ± 7 mm, spread 19 mm over the whole height
z 0.10 → 2.00.** Flat in height.

Flat in u AND flat in z ⇒ **ONE RIGID OFFSET of the body against the cream/red
break. Not a vertical scale error, not a stance error.** Equivalently: **the
two-tone break line sits ~81 mm too low on the body.**

#### 10.97.6  IT IS §10.24, AND IT REFRAMES WHY §10.24 KEPT BEING REVERTED

§10.24 from the other end: photographed the headlamp is **belt − 0.339 m**,
built **belt − 0.242 m** — the built lamp is **97 mm** too high relative to the
belt; and 83 ± 19 mm at 4.4 σ by a ratio needing no px/m. **81 ± 7 mm comes off
the whole silhouette and uses no headlamp, no roundel and no scale on the lamp.**
Fourth derivation, first that does not touch the front of the vehicle.

**And the reframing.** §10.24's findings were applied once and reverted once,
killed each time because a third method — the frontal silhouette of
`ref_side.jpg` — refuted the finding **as applied**, and *as applied* meant
**moving the HEADLAMPS**. This measurement says the misplaced member is **the
BREAK LINE**. Moving the break is a DIFFERENT change with three properties the
reverted one did not have:

* the **roundel does not move at all** — §10.24's explicit constraint is
  satisfied by construction, not by care;
* the **headlamps do not move**, so the frontal-silhouette refutation that killed
  it twice does not bear on it;
* it is the **relationship** the owner's Report 3 names — *"the paint job and the
  headlights are not alligned"* — rather than either half of it.

**NOT BUILT IN REV 39.** Four geometry changes at the tail of a shipped revision
is how this project has been burned. Rev 40's item 1, number in hand.

#### 10.97.7  A PROBE THAT REPORTS THE END OF ITS OWN SEARCH RANGE IS NOT REPORTING A PEAK

The first z-ladder let three bands return the **endpoint of the ±55 px search
range** as if it were a maximum. It manufactured **"+222 mm for the upper body"**
and an apparent **13 % vertical scale error**, both fictional, and I had written
both down before the gate existed. The `or -9` / `_roof_at` shape of §10.47,
third instance.

Acceptance is now stated BEFORE the run: an interior maximum at least 8 samples
from either bound, exceeding the curve's own median by ≥ 8 %; otherwise the band
DECLINES. **FALSIFIED with a lever whose default is a proven no-op**
(`T1_R39_NOGATE=1`): without the gate the spread goes **19 mm → 531 mm** and the
derived verdict flips to NOT FLAT.

#### 10.97.8  AND THE VERDICT WAS A CONSTANT STRING, IN THE PROBE THAT SAYS SO

The first draft of `probe_rev39_flank.py` printed **"FLAT IN HEIGHT"**
unconditionally — §10.50's defect, `rear34_character`'s constant verdict, in a
file written the same hour. It is now derived from the measured spread and prints
**NO RULING** when fewer than four bands answer.

#### 10.97.9  SEVEN DETECTOR DEFECTS OF MINE, NOT ONE FOUND BY INSPECTION

1. Flower-head detector gated `sat < 0.62` for "pale". The heads are **gold and
   saturated**: **0/10 on its own positive control**, and it found the man's
   white cap. §10.42's *a class gate is a probe too*.
2. Its negative control failed **9/200**, all one contiguous region — the same
   man. Priced at **2.79 % of the interior**, inside `lid_gen`'s own recorded
   6.09 % of occluders, and excluded rather than trimmed away.
3. A drip-rail finder locked onto the aperture band at z 1.32; a plausibility
   assert fired and the datum was dropped to one line.
4. A hub detector locked onto **the man's RED SHIRT** (7 776 px). §10.7 records
   that every front-arch attempt has done this. Fourth instance, on me.
5. A tyre gate used luminance alone. **The red body's luma is 79** and it sits
   inside any dark band: it would have printed a confident *"the tyre is 11.3 %
   too small"*. Two-term gate, endmembers printed.
6. The z-ladder's endpoint peaks — §10.97.7.
7. The unconditional verdict string — §10.97.8.

#### 10.97.10  A FALSE LEAD OF MINE, KILLED BY MEASUREMENT

Reading the overlay I took the cyan wheels for too large and nearly wrote it up.
Measured instead at the rear-axle column **the calibrated map placed** rather
than one I chose: rear tyre **651 ± 13 mm** on a swept two-term gate against the
locked **665 mm**, inside the ±15 mm floor the two scales' 2.3 % disagreement
sets. **The tyre is right.** The horizontal arm of that same run was **clipped by
my own crop** and pinned at 857 mm in every threshold arm — discarded, not
quoted.

#### 10.97.11  THE OWNER'S NINE FLOWER HEADS, CHECKED FOR THE FIRST TIME

*[stated, rev 8]* he counted **nine** off the photograph. `lid_gen.py` builds
**`N_FLOWERS = 10`** plus one part head, and its own docstring says the centres
*"reproduce rev 10's ten to better than 0.012"* — **rev 11 verified rev 10's ten
against rev 10's own ten**, a self-consistency check standing in for a check
against him. Nobody compared to his nine in twenty-eight revisions.

Board rectified through `lid_gen`'s documented quad; all four corners round-trip
to **0.000 px** and the independently computed head radii reproduce `lid_gen`'s
stated **176.5 / 168.9 px** at 176.6 / 168.8. Detector: **C1 positive 10/10**,
worst 0.234 R (the head behind the palm fronds); **C2 negative 0 of 200** planted
off-head centres reach even the worst built head's score. Ceiling stated: the
separation is **+0.42 and thin**, driven entirely by head 10.

*[stated, rev 39]* Shown the board flat, unmarked above and marked below, he
answered **TEN**. **His own rev-8 count of nine is SUPERSEDED by him**, and
§0's rev-8 entry is corrected accordingly.

#### 10.97.12  THE INHERITED BRIEF NAMED THE WRONG FRAME FOR REPORT 5

`NEXT_CONTEXT_PROMPT_rev39.md` §6 item 1 says to measure the cab door's lower
cutaway off `ref_side.jpg` *"if the man's red shirt does not occlude it"*. The
shirt is not the blocker. **`SPEC.md` §10.18 and the NOT MEASURABLE list both
record that the cab door is OPEN 49° across the relevant columns in that frame.**
A closed door's outline cannot be measured where the door is swung open.

The only frame with the door CLOSED is `ref_workshop.jpg` — the owner's own
rev-23 reading — which is the CONVERSION stage and which §10.62 establishes
carries **no admissible px/m on the door plane**. **REPORT 5 IS NOT BUILT**, and
the route to it is a scale-free ratio against the arch, whose radius is locked.

#### 10.97.13  `STATE.md` ARRIVED WITH A DIRTY PROVENANCE ROW

The shipped `STATE.md` reads `working tree | **DIRTY**`, `git commit 07c74b9`
= commit 205 against a HEAD of 207 — not the clean-tree parent-provenance pattern
the rev-39 brief describes. rev 38's "clean" describes the file it RECEIVED
(rev 37's, regenerated clean in `054c1ac`), not the one it SHIPPED.

**Resolved by regeneration, not by trust**: `audit.py` re-run on the clean
restored tree produces a file **byte-identical except the four provenance rows**.
Every measurement row reproduces.

#### 10.97.14  `bbox top` DISAGREES BETWEEN THE TWO GUARDS

`audit.py`'s `STATE.md` prints **3.017**; `build.py`'s VERIFY prints **3.046** —
same tree, same subdivision level, same `verify.py` function. Measured: the true
top mesh is `lid_main` at **3.0169**. `verify._bounds()` reads `ob.bound_box`
mid-build without forcing a depsgraph update, so the answer depends on WHEN it is
called. It is a logged line with no target and no guard — §10.47 left it
target-less deliberately — so this is RECORDED, not chased.


### 10.98  rev 40 — THE 81 mm IS A DATUM ERROR. `flank_compare`'s TWO DATUM LINES ARE OPPOSITE EDGES OF THE COUNTER FASCIA, THE PROSE SAYING OTHERWISE WAS NEVER A CHECK, AND ITEM 1 WAS STOPPED BEFORE IT MOVED 81 mm OF GEOMETRY

#### 10.98.1  What rev 40 was told to do, and why it did not do it

`NEXT_CONTEXT_PROMPT_rev40.md` §6 item 1: *"REPORT 3 — THE BREAK LINE. 81 ± 7 mm,
AND IT IS THE ITEM WITH THE MOST EVIDENCE BEHIND IT IN THE PROJECT … MOVE THE
BREAK."* §10.97.5–6 derived it, §10.97.6 argued it was the fourth independent
derivation of §10.24 and the first touching no headlamp.

**It is a datum error.** `probe_rev39_flank.py` pins the model's counter fascia
**BOTTOM** onto the photograph's counter fascia **TOP**, and the ~94 mm between
them is most of the 81 mm. No geometry was moved.

#### 10.98.2  The claim under test was a sentence, not a check

`flank_compare.py` fits two datum lines and says of them, in its own comment:

> *"the SAME cream/red break … the reference's is the same physical edge, so the
> two are used as ONE datum and its height never enters"*

It is fitted with **two different estimators in two different row windows**: a
LUMINANCE gradient over rows 425–452 on the reference, a REDNESS gradient over a
render-relative window on the render. On a cream / gold-nosing / beige-fascia /
red stack a luminance step and a redness step are **not the same boundary**.
§10.45's rule — *a claim in prose is not a guard* — and it cost the project a
headline.

#### 10.98.3  `probe_rev40_datum.py` — which edge each side actually pins

READ-ONLY. No new estimator: the render side is read from the build's **own
authored constants** with `ast` at run time, never from a colour gate, because
§10.97.9 records that a class gate tuned on the photograph does not transfer.

* **C1 PASS.** The reference line refits live to `v = -0.03467 u +446.813`
  (rms 0.118, n=256/269) — `probe_rev39_flank`'s transcription is exact, so the
  defect is not a typo.
* **C2 PASS.** `projinv` puts the RENDER datum at authored **z = 1.1459** at the
  lockup's mid column. `t1_detail.CNT_ZB` = **1.1470** → **−1.1 mm**;
  `CNT_ZT` = **1.2540** → **−108.1 mm**. **The render datum is the counter
  fascia BOTTOM.**
* **SCOPE, and I got this wrong first — see §10.98.13.** The slab edge
  `CNT_ZT − CNT_ZB` is **107.0 mm**, but `CNT_NOSE_F = 0.1860` caps **19.9 mm**
  of it in brass. The reference datum is the **nosing's LOWER edge**, so the
  like-for-like model quantity is the **PAINTED FASCIA, 87.1 mm** — not the slab.
* **C4 PASS.** In the reference, mean `|v_break − fascia top|` = **0.69 px**
  against mean `|v_break − fascia bottom|` = **19.46 px**. **The reference datum
  is the counter fascia TOP**, i.e. the nosing's lower edge. Photographed painted
  fascia, via `flank_kv`: **93.6 ± 2.0 mm** over 5 columns — and `t1_detail`'s own
  `CNT_NOSE_F` comment, an INDEPENDENT 113-column saturation-half-max run, gives
  20.32 px = **94.3 mm**. **Two independent photographic readings 0.7 mm apart.**
* Endmembers PRINTED, two-term gate, because §10.97.9 records the red body's
  luma is 79: fascia beige (0.843, 0.743, 0.658) luma 0.758; body red
  (0.356, 0.047, 0.026) luma 0.111; body cream (0.977, 0.919, 0.850) luma 0.926.

**Consequence, derived not asserted.** Both sides on the fascia TOP (the model's
own 87.1 mm): 81 − 87.1 = **−6.1 mm**. Both sides on the fascia BOTTOM (the
photograph's 93.6 mm): **−12.6 mm**. **The residual changes sign and loses an
order of magnitude**, and the band **[−13, −6] mm** brackets §10.98.6's
independent joint registration at **−5 mm**.

#### 10.98.4  MY OWN POSITIVE CONTROL FAILED, AND IT IS PRICED, NOT LOOSENED

**C3 FAIL.** The gate must reproduce REF §3(a)'s own hand-read cab-door table
(red from rows 436/436/438/438). It returns 437/437/439/**440** — three columns
at +1 px and one at +2. The bias is **+1.25 ± 0.43 px, one-sided on 4/4
columns** = **6 mm** at `k_t`, because a hand call takes the first row that LOOKS
red and a two-term gate takes the first row that IS unambiguously red. **The
tolerance was not widened.** 6 mm one-sided cannot touch a 19 px conclusion.

#### 10.98.5  THE INDEPENDENT ARM — break-to-sill shares no datum with the warp

The body's own two-tone break is visible only on the cab door (REF §3a); aft of
it the counter covers it. Both rows are read **inside `ref_side.jpg`** and both
constants are read **out of the build**, so the fascia mismatch cannot reach it.

```
photographed  window sill -> body break : 102.7 +/- 6.6 mm  (n=8, x 120-200)
built         Z_SILL - Z_BELT_AUTH      : 100.0 mm
REF sec.3(a)'s own hand figure          : 100.0 mm
difference                              :  -2.7 mm
```

**A break line 81 mm out of place would show here as ~81 mm. It shows 3 mm.**
Stated ceiling: this is a body-INTERNAL relationship, so it cannot detect a
common-mode shift of break and sill together — but that is the ride-height
question, not "the break is misplaced on the body", which is what §10.97.6
claimed and what this refutes.

#### 10.98.6  THE JOINT REGISTRATION SETTLES IT IN ONE LINE

The whole-vehicle best `(dy, dx)`, searched **jointly**, same masks, same edges:

```
rev-39 datum (fascia TOP)     (dy, dx) = (+19, -1) px = (+92 mm z,  -5 mm x)
rev-40 datum (fascia BOTTOM)  (dy, dx) = ( -1, -4) px = ( -5 mm z, -19 mm x)
```

**+92 mm becomes −5 mm when both sides pin the same edge.**

#### 10.98.7  THE FIX, AND IT OPENS NO NEW ESTIMATOR

The reference datum now uses the estimator this file **already used on the
render side**: a REDNESS gradient at the fascia bottom, over rows 440–462. Both
sides fit the beige→red step. New line: `v = -0.03412 u +466.632`, rms 0.233,
n=254/269 — **19.8 px = 92 mm below the rev-39 line, one counter fascia.**

`_assert_same_edge()` is armed **TWO-SIDED** on **both** fits: the datum line
must have NOT-RED above and RED below, in that frame's own redness units, or the
run dies. Measured: reference step **+0.5608**, render **+0.6598**, bar +0.030.
**FALSIFIED with `T1_FC_OLDDATUM=1`**, which restores the rev-39 luminance fit:
the reference step goes to **−0.0293** and the guard **FIRES**. A prose claim can
no longer stand in for a check here.

#### 10.98.8  `SCR` RE-MEASURED, AND ITS VERTICAL TERM FLIPS SIGN

§10.97.2 published *"the render's lockup has to move +76.2 mm forward and
**+61.9 mm down**"* and rev 40's item 2 was to apply it. Through the corrected
datum:

```
best integer shift (-16, -7) cells = +76.2 mm in x, -33.3 mm in z
```

**+76.2 mm forward is unchanged** — the datum is a horizontal line and never
entered x. **The vertical term is −33.3 mm: the lockup must move UP 33 mm, not
down 62.** 61.9 − 33.3 = 95.2 mm, one fascia height, which is the arithmetic
check on the whole finding. Also re-read on the corrected datum: IoU **0.7535** =
**0.877** of a measured ceiling **0.8591**; worst region `Senor` **0.459** of its
own ceiling; aspect 2.3622 vs **2.2512**; texture-only control **0.7595**.
**NOT APPLIED** — §10.29's rule, and a re-measured number is not a licence to
move geometry at the tail of the revision that re-measured it.

#### 10.98.9  A SECOND DEFECT IN `probe_rev39_flank.py`: dx AND dy ARE COUPLED

The probe searched the column shift and the row shift **sequentially**. On a
flank whose strong edges are near-horizontal that is not separable. Measured:
with the corrected datum the sequential search returns **dx = −15 px (−71 mm)**
where the joint search returns **−4 px (−19 mm)**. Now searched jointly, and the
per-band row shift is searched **at the global best column shift**.

Consequence for §10.97.4: SPEC 10.35's map validates end to end at **19 mm**, not
the published 5 mm. Still very good for a map used for twenty-three revisions —
but the 5 mm was read through the mismatched datum and is withdrawn.

#### 10.98.10  AND THE Z-LADDER NO LONGER RULES FLAT — reported, not tuned

On the corrected datum the ten bands read

```
  0.10-0.40  -14 mm    0.70-1.00  -193 mm    1.30-1.60  +222 mm    1.90-2.20  +193 mm
  0.30-0.60  -19 mm    0.90-1.20    -5 mm    1.50-1.80   -19 mm
  0.50-0.80  -24 mm    1.10-1.40    -5 mm    1.70-2.00   -19 mm
```

Seven bands cluster at **−5 to −24 mm**, consistent with the joint fit's −5 mm.
**Three bands return ±193–222 mm — and they are the SAME THREE that DECLINED
under the rev-39 datum.** §10.97.7's acceptance gate does not catch them here:
their prominence (1.20/1.30/1.55) overlaps a good band's (1.23), so prominence
cannot separate them, and **+222 mm is precisely the fictional figure §10.97.7
says the gate was written to kill**.

**The gate was NOT retuned.** The probe's derived verdict is therefore
**spread 415 mm, NOT FLAT, no ruling** — and that is itself the finding:
**§10.97.5's "FLAT, ONE RIGID OFFSET" was a property of the mismatched datum,
not of the vehicle.** An acceptance gate calibrated on one datum does not
transfer to another; re-deriving it, with the criterion stated BEFORE the run,
is rev 41's item.

#### 10.98.11  REGION 3 IS CLOSED BY HIM, AND THE COUNTER FASCIA IS 6.5 mm SHORT

**REGION 3 — OPEN SINCE REV 19, PUT TO HIM IN REV 37, NOT RE-PUT IN REV 38 or 39,
ANSWERED IN REV 40.** Shown `rev40_q_region3.png` — one x12 crop of the counter
edge, the pale band bracketed, one sentence — he was asked whether that band is
the COUNTER's front face or the BUS's own painted body.

*[stated, rev 40]* **THE COUNTER'S FRONT FACE.**

* This **supersedes rev 12's** recorded reading that *"the cream band below the
  counter's brass nosing is the body's own cream belt paint, not part of the
  counter"*. It also **explains rev 19**, where he selected region 2 and pointedly
  did NOT select region 3 — his rev-19 non-selection and his rev-40 answer agree
  with each other; it is rev 12's line that is retired.
* **The model was already right on the routing** — `plank_counter()` builds the
  slab `CNT_ZB..CNT_ZT` and `build.py:116` paints it `countercream`, so that band
  is already the counter's face in the build. Nothing to re-route.

**And it makes the depth measurable.** Like for like, painted fascia against
painted fascia:

```
  model  CNT_ZT - CNT_ZB - CNT_NOSE_F x slab            = 87.1 mm
  photo  this probe, 2-term gate, 5 columns             = 93.6 +/- 2.0 mm
  photo  t1_detail's own 113-column half-max run        = 94.3 mm
  model - photograph                                    = -6.5 mm
```

**The counter's painted fascia is ~6.5 mm SHORT** — the OPPOSITE SIGN to what
this section said before §10.98.13 was found, and a quarter of the size. Same
family as rev 12's *"the brass nosing was 1.6× too DEEP, not thin"*.

**CEILING STATED:** C3's +5.8 mm gate bias is **NOT** applied. It was measured
against REF §3(a)'s **hand** reading while the repo's figure is a **saturation
half-max** one; the two criteria sit at different points on the same transition,
so subtracting one from the other would be a third scope error. The −6.5 mm is
quoted against the raw gate, which agrees with the repo's independent half-max
reading to **0.7 mm**.

**NOT APPLIED.** It moves geometry, it therefore owes a hero, and `CNT_ZB` is
`REF §3b`'s measured 1.082 m AG while `CNT_ZT` is not independently measured —
so which end moves is a separate question. **Rev 41's item.**

#### 10.98.12  WHAT THIS COSTS THE RECORD

Withdrawn or re-valued, all of them measured through the mismatched datum:
§10.97.4's **−5 mm** horizontal → **−19 mm**; §10.97.5's **81 ± 7 mm** →
**−5 mm** whole-vehicle; §10.97.5's **FLAT / ONE RIGID OFFSET** → **no ruling**;
§10.97.6's *"the break line sits ~81 mm too low on the body"* → **refuted at
−2.7 mm by break-to-sill**; §10.97.2's **+61.9 mm down** → **−33.3 mm**.

**§10.24 is NOT re-opened or re-closed by this.** Its own three derivations use
the headlamp and the roundel and do not pass through this datum; what is
withdrawn is §10.97.6's claim to be a fourth, independent, headlamp-free
corroboration of it. **§10.24 goes back to exactly where rev 38 left it.**

Not claimed: that the counter is in the right place, that the body is, or that
the residual −5 mm means anything beyond "inside this instrument's floor".


#### 10.98.13  A SCOPE ERROR OF MINE, IN THE REVISION THAT EXISTS TO DOCUMENT ONE

The first cut of §10.98.11 published *"THE COUNTER FASCIA IS 13.4 mm TOO DEEP"*,
comparing the model's whole **slab edge** (107.0 mm) against the photograph's
**painted fascia** (93.6 mm). Those are different quantities: `CNT_NOSE_F` caps
**19.9 mm** of the model's slab in brass, and the reference datum is the nosing's
LOWER edge.

**It is the same class of error this whole section is about — comparing two
things that are not the same physical extent — committed inside the file
documenting it, in the same hour.** §10.97.8's shape, third instance in two
revisions.

Caught by asking what the model's nosing does before publishing, not by review.
Corrected figure **−6.5 mm, opposite sign**. The lesson is not "check the scope";
it is that **naming a defect class does not immunise you against it**, and that
the only thing that caught it was going back to the build's own constants for the
quantity I had already decided I understood.

**AND THE PRICED BIAS EARNED ITS KEEP.** Because C3's +1.25 px was recorded as a
number rather than waved away, it was available to test the corrected figure
against — and testing it is what showed the bias must NOT be applied here either,
because it is referenced to a different edge criterion than the repo's own
reading. A bias you priced can be reasoned about; a bias you loosened away cannot.

### 10.99  rev 41 — THE Z-LADDER'S GATE CANNOT BE RE-DERIVED, BECAUSE THE STATISTIC IT GATES HAS A 70 % FALSE-ANSWER RATE UNDER THE NULL. AND THE COUNTER-FASCIA FINDING IS A SCOPE ERROR ON THE RULER, NOT ON THE FEATURE

Rev 41's item 1 asked for `probe_rev39_flank.py`'s band acceptance gate to be
re-derived, with the criterion stated before the run. It was, twice. The first
criterion was refuted by its own run and the second one changed the question.
`probe_rev41_gate.py` is the instrument, READ-ONLY, and it changes nothing.

#### 10.99.1  CRITERION 1 WAS STATED FIRST AND IS REFUTED — recorded, not deleted

§10.97.7 records that the three bad bands originally *"returned the ENDPOINT of
the ±55 px search range"*, which is what `MIN_EDGE` was written to catch. On that
reading the corrected datum's ~19.8 px shift slid a **ramp's** arg-max just
inside the bound, while `MIN_PROM` never had power over it. The missing clause
would then be:

> **G3, TWO-SIDED HALF-PROMINENCE DESCENT** — on EACH side of the peak the curve
> must fall to ≤ `median + 0.5 × (peak − median)` inside the search range. A
> curve that climbs to the edge of its window and stops has no peak, it has a
> bound.

**G3 ADMITS 10 OF 10 BANDS, INCLUDING ALL THREE BAD ONES.** Their curves *do*
descend on both sides. **The assumed mechanism is wrong**: on the corrected datum
these are not ramps riding a bound, they are well-formed local maxima in the
wrong place. G3 is kept in the probe and printed, because a criterion that fails
is a result.

#### 10.99.2  THE NEGATIVE CONTROL IS THE FINDING — 70 %

Displace the reference by 120–360 px, every offset ≥ 2 × `SEARCH`, so that no
true `dy` is reachable inside the window **by construction**. Then read the peak
prominence.

```
  z band     null prominence  max    mean   | inherited gate answers under null
  0.10-0.40                  2.93x  1.61x   |  19 of 26
  0.30-0.60                  2.72x  1.47x   |  20 of 26
  0.50-0.80                  2.58x  1.40x   |  19 of 26
  0.70-1.00                  2.35x  1.37x   |  16 of 26
  0.90-1.20                  2.85x  1.60x   |  17 of 26
  1.10-1.40                  2.13x  1.40x   |  19 of 26
  1.30-1.60                  2.26x  1.39x   |  18 of 26
  1.50-1.80                  2.37x  1.42x   |  16 of 26
  1.70-2.00                  2.42x  1.48x   |  19 of 26
  1.90-2.20                  3.11x  1.59x   |  18 of 26
                      INHERITED GATE FALSE-ANSWER RATE: 181/260 = 70 %
```

**Prominences of 2–3× arise routinely when there is nothing to find, against an
inherited bar of 1.08×.** Nine of the ten bands' real prominences sit BELOW their
own null maxima. `MIN_PROM` was never a filter. **The gate is not mis-tuned; the
statistic has no power**, and §10.98.10's "prominence cannot separate them" is
true for a much stronger reason than it states.

#### 10.99.3  CRITERION 2, AND WHY IT IS NOT A NUMBER ANYONE CHOSE

> **G4, MAX-STATISTIC NULL TEST** — a band answers only if its actual prominence
> exceeds **the largest prominence that same band reached under the destroyed
> correspondence**.

The bar is the band's OWN null maximum: not chosen, and per-band, so a band with
noisy texture is automatically held higher than a clean one. **The null cannot
contain the answer** — it is built where the true registration is unreachable —
so nothing in it can steer the result toward −5 mm or toward +222 mm. G1 and G2
are inherited verbatim and G4 is ANDed on, so it is **strictly stricter**; no
band that previously declined can now answer.

**RESULT: 1 of 10 bands answers, so the ladder returns NO RULING.** The survivor
is z 0.90–1.20 at **−1 px = −5 mm**, reproducing the joint whole-vehicle
registration's −5 mm from a tenth of the pixels.

**FALSIFIED WITH A LEVER WHOSE DEFAULT IS A PROVEN NO-OP** (rev 20's pattern):
`T1_R41_NOG4=1` removes G4 and all ten bands come straight back, including the
three at −193/+222/+193 mm. That is what shows G4 is load-bearing rather than
decorative.

#### 10.99.4  AND THE VERDICT WAS TESTED FOR BEING MINE RATHER THAN THE VEHICLE'S

```
  bar                          bands answering   ladder verdict
  null MAX (G4, used)                1 of 10     NO RULING
  null 95th percentile               2 of 10     NO RULING
  null 75th percentile               4 of 10     FLAT, 19 mm
  null MEAN (weakest defensible)     3 of 10     NO RULING
  inherited MIN_PROM 1.08           10 of 10     NOT FLAT, spread 415 mm
```

**Three different verdicts — FLAT, NO RULING and NOT FLAT — across one sweep of
the acceptance bar.** The ladder's answer is a function of the bar, not of the
vehicle. At a 70 % null false-answer rate every bar low enough to admit four
bands is already inside the noise.

**SO THE FLAT-VERSUS-SCALE QUESTION IS NOT AWAITING A BETTER GATE. THE Z-LADDER
CANNOT ANSWER IT.** No gate rescues an instrument whose null beats its signal.
What survives untouched is the **JOINT whole-vehicle registration, (−1, −4) px =
−5 mm in z and −19 mm in x**, which uses the entire silhouette rather than a
tenth of it. §10.98's headline finding does not rest on the ladder and is
unaffected.

#### 10.99.5  DEFECTS OF MINE, ALL CAUGHT BY CONTROLS

* **C1 failed on a TRANSPOSED transcription.** I typed the published joint fit as
  `(-4, -1)`; `probe_rev39_flank` publishes `(-1, -4)`. My computation was right
  and my target was wrong — the count trap in a new costume, and the reason C1
  exists is that it caught it.
* **C3's first draft was INVALID.** It rolled the edge map without rolling the
  mask, decoupling them, and manufactured a spurious "the peaks are unstable"
  signal. Replaced by an END-TO-END control that shifts the render image itself
  and re-derives the whole warp: predicted −10.5 px, observed −11.
* **A CONSTANT VERDICT STRING, THIRD INSTANCE IN THIS REPO AND SECOND BY ME.**
  The bar sweep first printed *"NO BAR IN THAT RANGE SUPPORTS FLAT"* while the
  75th-percentile row printed **FLAT, 19 mm** three lines above it. §10.50's
  `rear34_character` defect; `probe_rev39_flank`'s first draft did the same in
  the hour it wrote the rule down; mine did it in the hour I quoted them both.
  Now DERIVED from the sweep and it prints the disagreement.
* **C6 exists because the fast scorer is a SECOND INSTRUMENT.** It reproduces the
  inherited `np.roll` form to **6.75e-13**, proven numerically rather than
  claimed in a comment (§10.45).

#### 10.99.6  ITEM 3 IS REFUSED: THE COUNTER FASCIA IS MEASURED ON THE WRONG RULER

§10.98.11 reports the painted fascia **6.5 mm short** — 87.1 mm built against
93.6 ± 2.0 mm and 94.3 mm photographed. **Both photographic readings are taken on
the counter's OUTER FACE and converted with the FLANK plane's scale.**
`probe_rev40_datum.py` divides by `FC.flank_kv(u)`; the 113-column figure is
`20.32 / FC.K_T`. The counter's outer face is **0.295 m nearer the camera** than
the flank (`CNT_Y_OUT` 1.1660 against a body surface of ~0.871 at counter
height), so a height read there and divided by the flank's px/m comes out too
large.

**This is not an inference. `t1_detail.py` says it of the very 113-column run
that yields the 94.3:** *"both flank-plane readings, i.e. before the
outboard-parallax term. The counter's outer face is ~0.295 m nearer the camera
than the ruler."*

`REF_MEASUREMENTS.md` §6 supplies the correction itself:

```
  gold nosing (outer top)    y_ref 416.8    -> 1.189 m AG   (1.205 parallax-corrected)
  fascia bottom (cream->red) y_ref 439.45   -> 1.082 m AG   (1.103 parallax-corrected)
  FASCIA / SLAB EDGE DEPTH   22.65 px = 0.107 +/- 0.005 m
```

Uncorrected separation **107.0 mm**, corrected **102.0 mm**. Those two REF pairs
fit a single-parameter scale-about-the-horizon model exactly, reproducing REF's
own stated **+16 mm and +21 mm** with **s = 0.9533** and an implied camera height
of **1.531 m** — one parameter, two constraints, exact. Applying that same s:

```
  rev 40's probe, 5 cols     93.6 mm flank-plane  ->  89.2 mm  ->  model - photo  -2.1 mm
  t1_detail's 113-col        94.3 mm flank-plane  ->  89.9 mm  ->  model - photo  -2.8 mm
```

**−6.5 mm becomes −2.1 to −2.8 mm**, and across the parallax bracket `t1_detail`
documents independently (*"+15 to +31 mm depending on how camera height and
distance split"*) **the residual changes sign**, running +1.4 to +2.0 mm at the
far end. It is consistent with zero everywhere in the documented band.

**THE THIRD ROUTE, SHARING NO STEP WITH EITHER READING, AGREES.** REF §6 measures
the whole slab edge at **22.65 px = 0.107 ± 0.005 m** and the build's
`CNT_ZT − CNT_ZB` is **0.1070 m** — **zero difference on a lock measured
directly**.

Two consequences worth naming:

* **§10.98.11 quotes the two readings' 0.7 mm agreement as corroboration. It is
  not.** They share the entire scale chain; the agreement is COMMON-MODE and says
  nothing about the term that separates both from the model. Rev 40's own rule —
  *when a finding is the previous revision's headline, find a route that shares
  no datum with it* — applied to rev 40.
* **§10.98.13 caught the FEATURE half of this scope error and missed the RULER
  half.** It corrected comparing the *slab* against the *painted fascia*, from
  +13.4 mm to −6.5 mm, opposite sign. The surviving −6.5 mm compares the right
  feature on the wrong ruler. Same family, one layer down, inside the section
  documenting the family. **NAMING A DEFECT CLASS DOES NOT IMMUNISE YOU AGAINST
  IT**, twice now.

**NO GEOMETRY MOVES. `CNT_ZT`, `CNT_ZB` and `CNT_NOSE_F` STAY**, and no hero is
owed for item 3. `t1_detail.py` had already refused this move for this reason:
*"1.254 / 1.147 / 0.107 are all inside that band and all three are SPEC 10.5
locks, so they STAY… the rule earned there is to measure it a third way before
moving a lock."*

**WHAT WOULD RE-OPEN IT** is the route `t1_detail.py` already names and nobody has
built: **the counter top's INNER edge, which lies ON the flank plane and needs no
parallax at all** — unusable in `ref_side.jpg` where the cream ramps with no
step, but a clean step in `ref_rear34.jpg` at y 423, x 700, needing only a local
vertical scale to close. That is a genuinely independent third method.

#### 10.99.7  NEW RULES

* **A GATE WITHOUT A NULL IS NOT A GATE.** Any acceptance threshold on a
  correlation statistic must be quoted against that statistic's distribution when
  the correspondence is destroyed. `MIN_PROM = 1.08` sat unexamined for two
  revisions against a null that routinely reaches 2–3.
* **WHEN A VERDICT MOVES WITH THE THRESHOLD, PUBLISH THE SWEEP, NOT THE VERDICT.**
  One bar sweep produced FLAT, NO RULING and NOT FLAT from one dataset.
* **A COMMON-MODE AGREEMENT IS NOT A CROSS-CHECK.** Two readings that share their
  entire scale chain agreeing to 0.7 mm is a statement about their noise, not
  about their accuracy.
* **A SCOPE ERROR HAS TWO HALVES — THE FEATURE AND THE RULER.** Fixing the feature
  and re-publishing is how rev 40's corrected figure kept a systematic.

---

### 10.100  rev 42 — HIS REPORT 5 IS BUILT: THE CAB DOOR NOW WRAPS THE FRONT WHEEL ARCH, AND THE SIGN OF THE OLD ERROR NEEDED NO RULER

> **RETRACTED IN REV 44 — SEE §10.102.** The wrap is gone and rev 41's flat
> chord is restored. `ref_nolita_doorshut.jpg` — square-on, shut, and tracked in
> this repo since rev 42 — holds the door's bottom rail flat to **0 px over 62
> px of door** and stops the rear shut line **on that rail**, 29 mm above the
> arch lip against rev 41's shipped 23–39 mm. §10.100.2's ordinal reading (the
> sign was wrong) still stands; §10.100.4's construction does not. **This section
> is left intact and is a dated record of a rev-42 state, not a current claim.**


His defect report 5, verbatim, rev 37: *"the doors extend lower, around the
wheel well"*. It has been the only untouched item of his that moves geometry
since rev 37, and it is now built.

#### 10.100.1  WHAT WAS WRONG, AND WHY NOBODY COULD MEASURE IT

`t1_shell.DOOR_GAP` cut the cab door's bottom as a **STRAIGHT CHORD ACROSS THE
TOP OF THE FRONT WHEEL ARCH** — z 0.8000–0.8160 un-dropped, **23.0–39.0 mm
ABOVE** the arch crown, whose built value is `_ARCH_TOP_F` =
`arch_z(X_AXLE_F) + ARCH_R` = 0.4035 + 0.3735 = **0.7770**. The rev-41 smoothed
outline's minimum over the arch's x-span is **0.8006, 23.6 mm above the crown**.
Every revision from rev 7 to rev 41 shipped that chord, pinned there by an
import-time assert.

> **A FIGURE OF MINE IN THIS SECTION WAS WRONG AND IS CORRECTED HERE RATHER
> THAN QUIETLY.** My first draft of §10.100 and of `HANDOFF_rev42.md` put the
> crown at **0.7854** and the clearance at **14.6–30.6 mm**. 0.7854 is a
> **rev-8 COMMENT** in `t1_shell.py` (*"The front arch top moves 0.7710 →
> 0.7854"*), describing a state before later changes to the rake and the arch.
> I quoted the comment instead of the value the build prints. **It is exactly
> the trap SPEC §10 already names** — rev 13's *"never put a figure in an
> acceptance test unless you watched it print"* and rev 26's *"another figure
> in a comment that was never watched print"* — reproduced by me in the section
> documenting the repair. **THE GEOMETRY IS UNAFFECTED**: the construction and
> both asserts call `arch_z(T.X_AXLE_F)` live and never touch the literal, so
> nothing built or guarded moves. Only the prose figure was wrong, and it was
> caught by re-running the value rather than re-reading the sentence.

The reason it survived is that it looked unmeasurable. §10.62 and §10.73 both
record that **no supplied frame carries BOTH a closed cab door AND an
admissible px/m on the door plane**: `ref_side.jpg` has the cab door **OPEN
49°** (§10.18, §10.97.12) and `ref_workshop.jpg` is a three-quarter view whose
only locked ruler is the headlamp aperture, on the nose plane, at a catalogue
0.180 m (§10.72's struck class). REF §9 warns in the same breath that lateral
scale varies **more than 2:1** across that panel and that a fitted projection
model **did not close**. So a metric door-plane figure is barred, and rev 42
takes none.

#### 10.100.2  WHAT WAS MEASURED — AND IT IS ORDINAL, SO IT NEEDS NO SCALE

In `ref_workshop.jpg`, the cab door's **front shut line** fits

    x = -0.03467 v + 512.233

over 49 rows (v 520→716, ridge score rising to 93 at the bottom), and it runs
**CONTINUOUSLY from the belt down to the body's lower edge at v = 712**. The
front arch lip's crown in the same frame is at **v ≈ 621**. The door's shut
line therefore reaches **~91 px BELOW the arch crown**.

The build put the door's bottom **ABOVE** the crown. **THE SIGN WAS WRONG, and
a sign does not need a ruler.** That is the whole admissible content of the
photographic half of this finding, and nothing metric is taken from it.

**A CANDIDATE LINE I NEARLY PUBLISHED DID NOT EXIST.** The first marked figure
drew a near-horizontal "door bottom" across x 500–585 at v ≈ 692. Re-examined
contrast-stretched at 9× with no overlay, that region is **FLAT**: ridge scores
4–8 against a noise floor of 3.5–5.5. **The line was my own annotation read
back as evidence.** It was checked before the figure went to him. A real linear
feature does exist over x 604–700 descending v 625 → 600 (scores to 19.8) and
it spans exactly the arch, which is what it belongs to.

#### 10.100.3  HIS TWO READINGS — one crop, three marks, two sentences

*[stated, rev 42]* Shown a 9× crop of `ref_workshop.jpg` with the door shut
line in red, the height of the arch crown in cyan and the body's lower edge in
yellow:

* **"the door extends down to the side rocker it looks like"** — his hedge is
  kept verbatim, because he wrote it.
* Asked whether the door's rear lower corner sweeps **up and over** the front
  wheel arch so that the arch's front lip is part of the door: **YES.**

rev 36's format again — one crop, one mark, one sentence — and it settled the
SHAPE of a member that had been unmeasurable for five revisions. It does **not**
settle any magnitude, and none is claimed.

#### 10.100.4  THE CONSTRUCTION — not one new constant

    z_bot(x) = max( ZB(x) + G ,  arch_z(X_AXLE_F) + sqrt((ARCH_R+G)^2 - (x-X_AXLE_F)^2) )

* the arch is **the build's own circle** — `X_AXLE_F`, `arch_z`, `ARCH_R`, all
  locked and all guarded elsewhere;
* the rocker is **`t1_core.ZB`**, the under-body / sill bottom edge, the same
  table `folk_gen.sill_z` already parses;
* the clearance **G is READ OFF REV 41's OWN OUTLINE**: `DOOR_ARCH_G` is the
  minimum radial distance rev 41's smoothed `DOOR_GAP_S` kept from that circle,
  **0.024426 m**. So the new outline is **nowhere closer to the arch than the
  outline that has been passing T1_SUB=2 since rev 23**, and that is asserted,
  not claimed in prose (§10.45).

Result: the door's bottom is **272.2 mm lower at the rear corner** and
**387.5 mm lower at the front corner**, and rises to z 0.8033 over the arch
crown where rev 41's chord sat at 0.800–0.816.

**THE GUARD FIRED ON THE FIRST ATTEMPT AND IT WAS RIGHT.** Built directly at
`DOOR_ARCH_G`, the resample-plus-smoothing pulled the arc inward and the
smoothed outline came back at **0.0225 m against rev 41's 0.0244 m** — 1.9 mm
CLOSER. The guard was **not** relaxed by 1.9 mm. The construction now solves by
**fixed point** for the build clearance that makes the *smoothed* outline land
on rev 41's value: converged `_G_BUILD` **0.026278**, smoothed minimum
**0.024421** against **0.024426**. It re-solves itself if `_NRES`, `_NBOT` or
the smoothing ever change.

`_NRES` 76 → **200** and `_NBOT` = 61. rev 23's densification precedent
(`CARGO_GAP` 28 → 154): the bottom run is now an ARC and a coarse resample of
an arc is not worth shipping merely because a guard would catch it.

#### 10.100.5  THE GUARD IS RE-SCOPED, AND ITS NEW RATIONALE IS STATED

rev 23's rule: **DO NOT INHERIT A GUARD'S RATIONALE ALONG WITH ITS SHAPE.**

The old assert required the outline to stay 10 mm **above the arch CROWN**.
That shape was only ever a **proxy** for the thing that actually collapsed the
shell **205562 v → 12 v at T1_SUB=2 for six revisions**: the outline **crossing
the arch lip**. A door that wraps the arch violates the proxy while satisfying
the invariant. The guard is therefore rewritten as the invariant it always
meant — a **RADIAL clearance from the arch circle** — and armed at the
clearance **rev 41's own outline kept**, so it can be satisfied only by being
no worse than what shipped, never by a number chosen today. A second assert
keeps a 10 mm absolute floor; a third keeps the outline off the body's own
lower edge (closest approach **26.3 mm**).

#### 10.100.6  WHAT IS **NOT** CHANGED — named, not absorbed

`DOOR_GAP` is left **BIT-IDENTICAL** and keeps its second job: it is the **ART
DATUM**. `folk_gen` parses it for `DOOR_X0` / `DOOR_X1` / `DOOR_W` and for
`_DOOR_BOT_AUTH`, which `panel_bot(x)` returns inside the door span and which
`door_pv` therefore normalises every v-coordinate of the door art over.
**CORRECTED, rev 44 — `DOOR_H` DIVIDES NOTHING, and it is not the v-map.** It
has exactly two read sites, `folk_gen.py:1274` and `:1287`, both `h = sv *
DOOR_H`, and both **MULTIPLY** a normalised motif height into metres for two
motifs (`EDGE_E`'s latch sliver, `DARK_1`). The v-map is `door_pv`, and it is
**PROPORTIONAL** — which is why re-pointing the parse STRETCHES the art rather
than extending it, and why the owner's rev-44 answer cannot be reached that
way. Instrumented at `probe_rev44_doorart.py` C1/C5. Re-pointing that parse at the wrapped outline
moves `DOOR_H` by ~390 mm and forces a re-bake of the flank textures — a
SECOND lever in the same revision, which is exactly what rev 25 refused when it
held `_DOOR_TOP_AUTH` at 1.8140 *"so `DOOR_H` stays bit-identical and only one
lever moves"*. Same call, same reason.

**THE ART FRAME IS THEREFORE STILL REV 41's, AND THAT IS AN OPEN ITEM, NOT A
SOLVED ONE.** The door is now ~390 mm deeper at its front lower corner than the
frame its art was baked into. **The three texture md5s are unchanged this
revision BY CONSTRUCTION.** This is rev 43's item 1.

#### 10.100.7  WHAT IT COST THE GUARDS — nothing

**0 fail / 0 warn at BOTH levels on BOTH tools.** 131 objects, 190 meshes, 42
materials, 5 constant-rough, **0 non-manifold at both levels**. Roof
1.9835/1.9833, rake 17.75, arch gaps 39.7 / 40.7 mm, bays 0.516 0.515 0.516,
off flank 804.9 mm, L=4.065 W=1.750 — every inherited figure identical.

**Two figures MOVE, and both are the direct consequence of a longer outline:**
cut roof hole **68564 → 70069 v** (SUB=1) and **252749 → 254428 v** (SUB=2).
Re-baselined, flagged, not hidden — rev 23's precedent.

**THE T1_SUB=2 SHELL DID NOT COLLAPSE.** That was the risk the old assert
existed to prevent, and it is the reason the new assert is armed at rev 41's
own clearance rather than at a looser one.

**ALL 30 INHERITED PROBES RE-RUN ON THE MOVED GEOMETRY AND ALL 30 REPRODUCE
THEIR PUBLISHED TALLIES.** `probe_rev39_flank`'s JOINT registration is still
**(−1, −4) px = (−5 mm z, −19 mm x)**, `probe_cross_anatomy` still shows flank
**0.0 mm** / off flank **804.9 mm**, `probe_dust_scope` still 8/0 on its
hard-coded 190.

#### 10.100.8  NEW RULES

* **AN ORDINAL FACT NEEDS NO RULER, AND THAT IS WHAT MAKES IT ADMISSIBLE WHERE
  A METRIC IS BARRED.** Report 5 sat unbuildable for five revisions because
  §10.62 and §10.73 bar a px/m on the door plane. What broke it was not a better
  ruler: it was noticing that the door's shut line runs BELOW the arch crown and
  the build put it ABOVE. A SIGN has no units. Look for the ordinal statement
  before concluding a frame cannot answer.
* **A LINE YOU DREW IS NOT EVIDENCE.** My first marked figure produced a "door
  bottom" that, contrast-stretched with no overlay, does not exist — ridge
  scores 4–8 against a noise floor of 3.5–5.5. **Check the UNMARKED frame before
  the marked one goes anywhere.**
* **A GUARD FIRING ON YOUR OWN CHANGE IS THE GUARD WORKING.** The arch-clearance
  assert caught my first outline 1.9 mm too close. Fix the construction, never
  the bar.
* **WHEN SMOOTHING MOVES A CURVE, SOLVE FOR THE INPUT THAT PUTS THE OUTPUT WHERE
  YOU WANT IT** — a fixed point, not a hand-tuned offset, so it re-solves itself
  when the resample count changes.
* **ARM A NEW GUARD AT THE OLD BUILD'S OWN MEASURED VALUE.** `DOOR_ARCH_G` is
  read off rev 41's outline, so the new geometry can satisfy the guard only by
  being no worse than what shipped — never by a threshold chosen today.

---

---

### 10.101  rev 42 — THE UV-OVERLAP AND TEXTURE-RESOLUTION CHECK, RUN FOR THE FIRST TIME IN FORTY-TWO REVISIONS

§5 of this document has said, since rev 3:

    Decals 3K-4K, **non-overlapping**, correctly oriented, correct handedness.

and the owner's own words on the 3D deliverable are *"4K non-overlapping
textures ... no floating artifacts"*. **Nothing had ever measured either half.**
Verified before acting: `grep -ric "uv overlap|texel densit|non-overlapping"`
over `SPEC.md`, `REF_MEASUREMENTS.md` and every `.py` returns **exactly one
hit — SPEC:319, the requirement itself.**

`probe_rev42_uv.py`, NEW, READ-ONLY.

#### 10.101.1  THE CENSUS IS ALREADY A RESULT

Seven image nodes across five materials, and **only ONE meets §5's own 3K
floor**:

| image | size | projection | coords | ≥3072 | wearers |
|---|---|---|---|---|---|
| `nose.png` | 1024×1024 | FLAT | Geometry.Position (Y,Z) → Mapping | **no** | 10 |
| `lidmural.png` | 2048×1238 | FLAT | default UV | **no** | 1 |
| `lidsign.png` | 2048×1238 | FLAT | default UV | **no** | **0** |
| `swirl.png` | 2048×2048 | **BOX** | TexCoord.Object → Mapping | **no** | 10 |
| `swirl_b.png` | 2048×2048 | **BOX** | TexCoord.Object → Mapping | **no** | 10 |
| `calidad.png` | 2400×1771 | FLAT | default UV | **no** | 1 |
| `senor.png` | 4096×1738 | FLAT | default UV | **yes** | 2 |

**`lidsign.png` is loaded by a material worn by NO OBJECT.** `tex/emblem.png`
is on disk and referenced by nothing at all. Both reported, neither removed —
this probe changes nothing.

**REPORTED, NOT RULED ON.** 3K–4K is his bar and the call is his. It is also
not softened: `nose.png` is **1K**, and the nose is the subject of three of his
eight defect reports.

#### 10.101.2  THERE IS NO UV LAYOUT ON THE BODY AT ALL

`T1_paint` — worn by `T1_body` and nine others — drives `swirl` and `swirl_b`
through **BOX projection from OBJECT coordinates**, and `nose.png` through a
FLAT projection of `Geometry.Position`'s (Y, Z). **20 of 190 meshes carry a UV
layer**, and the body is not one of them.

So "non-overlapping UVs" is not merely unchecked on the body — **it is not
well-posed there**, because there are no UVs. A triplanar projection maps 3D to
2D and is multi-valued wherever the surface folds back on itself.

**The repo already knew this and worked around it without measuring it.**
`folk_gen.py`'s own comment: *"no flank op may reach x < XART_LO: at MAP_SCALE
0.26 that wraps onto the cab door's hinge edge (x = -2.029 is the same texel as
x = +1.817)"*. That is a texel collision, documented as a painting restriction.

#### 10.101.3  SELF-OVERLAP vs REUSE — the distinction that changes the answer

A decal worn by two panels shares texels **by design**. `script_L` and
`script_R` both wear one `senor.png`, which scores **100 % colliding** if the
two objects are pooled and **0.00 %** when each object is measured against
itself. Pooling would have published a false defect. Measured per object and
totalled:

| image | SELF-overlap | of its painted area | cross-object (reuse) |
|---|---|---|---|
| `calidad.png` | 0.0000 m² | **0.00 %** | 0.0000 m² |
| `lidmural.png` | 0.0000 m² | **0.00 %** | 0.0000 m² |
| `senor.png` | 0.0000 m² | **0.00 %** | 1.3974 m² |
| `nose.png` | 0.5240 m² | 11.54 % | 0.0000 m² |
| `swirl_b.png` | 13.2032 m² | **48.36 %** | 0.2318 m² |
| `swirl.png` | 18.8473 m² | **83.04 %** | 0.1903 m² |

**TOTAL SELF-OVERLAP 32.5746 m² = 55.97 % of 58.2048 m² painted.** A further
3.13 % is legitimate reuse and is **not** counted against §5.

**EVERY HAND-MADE UV LAYOUT IN THIS BUILD IS CLEAN AT 0.00 %.** All of the
overlap is the procedural projection.

#### 10.101.4  TEXEL DENSITY, area weighted, against a DERIVED bar

| image | p5 | median | p95 texels/m |
|---|---|---|---|
| `calidad.png` | 4639 | **4657** | 4665 |
| `senor.png` | 3149 | **3197** | 3199 |
| `lidmural.png` | 1106 | **1106** | 1106 |
| `nose.png` | 582 | **648** | 656 |
| `swirl_b.png` | 484 | **531** | 532 |
| `swirl.png` | 484 | **532** | 532 |

The shipped hero is 4800 px across a 4.065 m vehicle = **1180.8 px/m**. A
surface delivering fewer texels/m than that is soft in the hero **BY
ARITHMETIC**. That bar is derived and is labelled as derived; it is not a
measurement of the vehicle. On it, `swirl`, `swirl_b` and `nose` deliver
**0.45×, 0.45× and 0.55×** the hero's own sampling rate.

#### 10.101.5  TWO ESTIMATORS WERE KILLED BY THEIR OWN CONTROLS BEFORE THIS ONE

Both are recorded in the probe rather than deleted.

* **DRAFT 1, POINT SAMPLING.** Flag a texel if any two samples in it are far
  apart. **C3 killed it**: the fraction climbed **5.34 → 6.10 → 10.98 %** as the
  sample spacing went 40 → 20 → 10 mm. A "does any pair differ" test can only
  find MORE collisions with more samples; it never converges, so it measured
  the sample count and not the asset. C1 failed for the same reason and the
  >25 % bar was never the problem.
* **DRAFT 2, CONSERVATIVE RASTER WITH A FIXED METRIC TOLERANCE.** **C2 killed
  it at 99.95 %**: a single flat 2 m quad "collided with itself" everywhere,
  because a collision CELL spans a finite distance ON THE SURFACE — 62 mm on
  that quad against a `TOL_M` of 5 mm. **C5 killed it independently** at
  **+53.8 %** area and a coverage ratio of **3.2452**: area accumulated over the
  conservative slop margin.

Draft 3 fixes both **causes**: the tolerance is scale aware (a cell is
colliding when painted from two places farther apart than that cell's own
footprint could account for), and area is **analytic**, not rasterised.
Coverage ratio **1.0255**, area exact to **0.587 %**.

**A DEFECT OF MINE, CAUGHT BY ARITHMETIC RATHER THAN BY A CONTROL.** The
triangle-stream cache was keyed by `(image, selector)` and **not by the object
list**, so the per-object pass re-used the whole-material stream for every
object in turn and printed self-overlap of **332.7618 m² = 571.71 %** of a
58.2048 m² painted area. **A fraction over 100 % is arithmetically impossible**,
which is the only reason it was caught in one read. Key fixed, comment left in
place.

**THE SELECTOR IS PARSED, NOT ASSUMED.** The first cut hard-coded my reading of
`T1_paint`'s Mix chain (centroid y > 0 for the swirl pair; |normal.x| > 0.7 and
x > 1.6 for the nose). That is a re-typed constant of the class this repo has
been punished for repeatedly, and worse than usual here: **if the split were on
the NORMAL rather than the POSITION, the solidified shell's INNER skin would go
to the other tile and the compared sets would not be the ones the renderer
uses.** The chain is now evaluated from the graph, 4 rules for each swirl tile
and 2 for the nose, and anything it cannot evaluate RAISES.

#### 10.101.6  C3 FAILS, THE VERDICT SURVIVES ANYWAY, AND BOTH ARE STATED

| parameter | sweep | spread |
|---|---|---|
| `TOL_M` 1 → 20 mm | 59.09 → 59.09 % | **0.00 pp** |
| `CELL_K` 8 → 4 → 2 texels | 59.58 → 59.09 → 67.50 % | **8.41 pp** |
| `C_FOOT` 2.0 → 5.0 | 67.10 → 59.06 % | **8.04 pp** |

The stated tolerance was 2.0 pp on each. **C3 FAILS and is recorded as failing;
nothing is widened.** The published FIGURE is therefore good to about ±8 pp and
no better.

**But the RULING does not move with the parameters, and that is a separate
fact.** The bar stated before the run was 10 %. **Every value in the entire
sweep — 59.06 % to 67.50 % — lies on the same side of it.** rev 41's rule says
publish the sweep rather than the verdict when the verdict moves with the
threshold; here the sweep is published *and* the verdict is reported, because
the sweep does not reach the bar. A figure that is uncertain to ±8 pp can still
settle a question whose bar is 50 pp away.

#### 10.101.7  WHAT IS **NOT** CLAIMED

* **That an overlap is automatically a defect.** `swirl`/`swirl_b` are REPEAT
  tiles and repetition is their job; their texel keys are deliberately NOT
  wrapped, so what is measured is whether the LAYOUT is injective, ignoring
  intentional tiling. A scope decision, stated.
* **Anything about the artwork's correctness.** This is a layout and sampling
  measurement only.
* **Anything about render quality.** It measures the asset, not a frame.
* **Any repair.** Nothing in this section moves geometry, artwork or a
  constant. Fixing it means giving `T1_body` a real UV layout, which is a
  re-bake of every flank texture and is coupled to §10.100.6's own re-bake.
  **They should be done together, and neither should be done alone.**

#### 10.101.8  NEW RULES

* **A REQUIREMENT NOBODY HAS INSTRUMENTED IS NOT A REQUIREMENT.** §5's
  "non-overlapping" sat in this document for thirty-nine revisions with no
  probe, no number and no owner ever quoting it back.
* **AN ESTIMATOR WITH A FREE PARAMETER MUST SWEEP THE PARAMETER YOU ADDED
  YOURSELF.** `C_FOOT` was mine; it moves the answer 8 pp.
* **POOLING TWO OBJECTS THAT SHARE A DECAL MANUFACTURES A DEFECT.**
  `senor.png` reads 100 % pooled and 0.00 % per object.
* **A FRACTION OVER 100 % IS THE CHEAPEST CONTROL THERE IS.** It caught a cache
  key that no assertion in the probe was watching.

#### 10.101.9  AND ONE MORE RULE, EARNED IN §10.100 AND RECORDED HERE

* **A FIGURE IN A COMMENT IS NOT A MEASUREMENT, AND THE COMMENT MAY BE THIRTY
  REVISIONS OLD.** §10.100.1's crown was first published as 0.7854 because I
  quoted `t1_shell.py`'s rev-8 comment instead of the value the build prints;
  0.7770 is the built value and the comment has been stale since rev 13
  re-derived the rake. rev 13's rule — *never put a figure in an acceptance test
  unless you watched it print* — **third instance in this repo, and the first
  where the stale figure was in a comment rather than a test.** Corrected in
  SPEC, in `HANDOFF_rev42.md` and in the code comment itself, and the rev-8
  comment left in place with a note saying why, because it is a dated record of
  a rev-8 state and not a current claim.

---

### 10.102  rev 44 — **§10.100 IS RETRACTED.** THE CAB DOOR DOES NOT WRAP THE FRONT WHEEL ARCH. THE FRAME THAT REFUTES IT HAS BEEN IN THE REPO SINCE REV 42, AND THE OWNER'S DEFECT REPORT WAS RIGHT TWICE OVER

#### 10.102.1  WHAT THE OWNER SAID, AND WHY IT READ AS TWO DIFFERENT COMPLAINTS

*[verbatim, rev 44]*

* **"The door does not continue on the other side of the wheel well."**
* and, unprompted, a few minutes later: **"Quick note, the door does not
  continue downward behind the wheel."**

Read against rev 42's geometry these are **one complaint stated twice**, and
both halves are exactly right:

* §10.100.4's bottom run is `max(ZB(x)+G, arch circle offset radially by G)`.
  A radial offset of a circle **is a circle**, so the door's bottom rail was
  **concentric with the arch lip by construction and could never diverge from
  it.** Measured on the 3200 px side render (574.4 px/m): the two ran
  **14.0–22.4 px apart with a spread of 8.3 px over 600 mm of x.** Two curves
  that never separate read as **one thick line**, however far apart they are.
  The door's bottom stopped being a line that crosses the wheel well and became
  part of the arch. → *"does not continue on the other side of the wheel well."*
* And the door's rear shut line, under the wrap, ends **on the arc at z 0.5385
  — 135 mm below the arch crown and 127 mm above the rocker** — so it stops in
  the middle of a red panel beside the wheel, reaching neither. → *"does not
  continue downward behind the wheel."*

#### 10.102.2  THE FRAME THAT SETTLES IT — `ref_nolita_doorshut.jpg`, ALREADY TRACKED

`ref_nolita_doorshut.jpg` is the **one frame in the repo that carries the cab
door's whole outline, square-on, shut** — §10.100's own PHOTOGRAPHS WANTED entry
says so ("the one frame that shows the full outline"). It was used in rev 42 to
establish that the door outline exists at all and **was never asked the question
§10.100 was deciding.** Three measurements, all by gradient, none by eye:

| what | how | result |
|---|---|---|
| the door's bottom shut line | row-gradient of the mean over the door's rear half (cols 70–122, rows 225–265) | a 2 px dark line at **rows 238–242, centre 239–240**, `\|dL\|` 18.3 and 21.1 against a floor of 1–4; **and nothing else in 40 rows** |
| is it flat? | darkest-row scan, column by column, rows 234–246 | **row 239, held from col 60 to col 122** — 62 px of door, **0 px of descent** |
| the rear shut line | column-gradient in 8-row bands, cols 112–135 | col 124.5, `\|dL\|` **24–37** for rows 208→240; **rows 240→288 read 0.4–2.2, i.e. the noise floor.** The line **stops at the bottom rail** |
| the clearance | wheel-well dark top edge at cols 85–94 | arch lip **row 241.5**, door line **row 239** → **2.5 px** |
| the scale | hub centroid col 91.0, arch rear foot col 123 → 32 px = `ARCH_R` 0.3735 m | **85.7 px/m**, so 2.5 px = **29 mm** |

**REV 41 SHIPPED 23.0–39.0 mm.** The frame lands in the middle of the band that
shipped, by a route that reads both features off the same image and needs no
absolute scale: the ratio *(door-line-to-lip) / (arch half-width)* is **0.078
measured against 0.065 built.**

Under the wrap, the bottom rail descends **388 mm** across that same span and
the rear shut line continues **another 38 px** to the rocker. **Neither exists
in the photograph.**

#### 10.102.3  WHAT REV 42 ACTUALLY HAD, AND WHY IT WAS NOT ENOUGH

§10.100.3's evidence was **one yes/no question over a 9× crop of
`ref_workshop.jpg`**: *"does the door's rear lower corner sweep up and over the
front wheel arch so that the arch's front lip is part of the door?"* — **YES.**

Three things are wrong with that, and all three were visible at the time:

1. **It is a leading question.** It names the answer and asks for assent. §10.100
   itself banked "his hedge is kept, deliberately, because he wrote it" on the
   *other* sentence — and then took the leading one at full strength.
2. **`ref_workshop.jpg` is a three-quarter frame**, and §10.62 and §10.73 had
   *already ruled it inadmissible for anything metric on the door plane.*
   §10.100.2 was careful to take only an **ordinal** fact from it (the shut line
   runs *below* the arch crown — "the sign was wrong, and a sign does not need a
   ruler"). That was sound. But **§10.100.4 then built a magnitude out of it**,
   and the magnitude is what is refuted.
3. **A square-on frame of the same feature was in the repo.** The ordinal
   argument was never wrong for want of a ruler — it was wrong for want of
   *looking at the other photograph.*

**THE RULE, and it is new:** ***when an ordinal reading forces a construction,
go and find a frame that can carry the magnitude before you build it.*** An
ordinal fact licenses a *sign*, never a *shape*.

#### 10.102.4  THE ATTEMPT TO FIX IT INSIDE THE WRAP IS WHAT PROVED THE WRAP WRONG

Before the frame was measured, the concentricity was attacked directly. Both
attempts failed, and **how** they failed is the finding:

* **Flatten the run to the arc's own crown height** — `_ARCH_CZ + (ARCH_R + G)`
  = 0.7993 authored, against rev 41's shipped chord of 0.800–0.816: a **1 mm**
  match to a shape that shipped for eighteen revisions, not to my reading of a
  photograph. It passed the clearance guard (a horizontal line at the offset
  circle's crown is *tangent* to it, so clearance is ≥ G everywhere and = G only
  at the crown), and divergence went 8.3 → 86.7 px. **And it silently deleted
  §10.100.4's rear corner dip**, because the arc's span reaches x = 0.9021 and
  the door's rear edge is at 0.92565 — *inside* it. The docstring I wrote in the
  same edit claimed "both corner dips survive"; the very next run printed the
  rear corner at 0.8014 where §10.100 had 0.5438. **The claim and its refutation
  were in the same commit-in-progress, four minutes apart.**
* **Carry the rear shut line down to the rocker** — which is what the owner
  asked for in plain words. This is where the geometry answers back. The front
  arch's rear-most point is `X_AXLE_F − ARCH_R` = **0.92650**; the door's rear
  edge is **0.92565**. **They coincide to 0.85 mm.** So:
  * the rocker line `ZB+G` at the door's rear edge sits **0.93 mm** from the
    arch circle — against the guard's 24.4 mm and the hard floor's 10 mm;
  * offsetting the lip **vertically** by G instead of radially puts the corner
    at z 0.4279 (visually on the rocker) but **1.65 mm** from the lip, because
    the lip is vertical there and a vertical offset buys no horizontal gap;
  * moving the door's rear edge aft the 23.5 mm that would clear it drives
    `B_PILLAR` **negative** — the exact rev-22 defect §10.62 was written to
    catch — because `DOOR_REAR_DX = (BAYS[0][1] + B_PILLAR) − _DOOR_REAR_X0`
    and bay 0's edges are locked by §10.29;
  * leaving the edge and dropping only the run's rear end produces a **23 mm
    wide, 400 mm deep tab** hanging off the door's corner.

**A construction that cannot be built at any clearance is usually a construction
that is not there.** It is not: the Nolita frame stops the rear shut line at row
240 for the same reason the geometry does.

#### 10.102.5  WHAT IS RESTORED, AND THE PROOF THAT IT IS A RESTORATION

`DOOR_GAP` — rev 41's table — has been sitting in `t1_shell.py` **bit-identical
this whole time**, because §10.100.6 deliberately kept it as the **art datum**.
It is the cut outline again:

    _NRES        = 76                      # rev 41's, restored with it
    DOOR_GAP_CUT = DOOR_GAP
    DOOR_GAP_S   = _smooth(_resample(DOOR_GAP_CUT, 76), 2)
    assert DOOR_GAP_S == _GAP41_S

`_GAP41_S` is the object §10.100 built *purely to read rev 41's clearance off*.
Asserting the two are the same list is the cheapest possible proof that this is
**a retraction and not a new shape wearing rev 41's name** (§10.45 — a claim in
prose is not a guard). `DOOR_BOT_RUN` is sliced as the **exact complement** of
the `DOOR_GAP[:-3]` rev 42 kept, plus the two corners that slice shared with it,
so the rear-corner point cannot drift between the two definitions.

Measured after the restore: `_MIN_RAD` **0.024426** against rev 41's
**0.024426**; bottom rail 0.8160 / 0.8040 / 0.8000 / 0.8040 / 0.8120, spread
**16.0 mm**, clearance above the arch crown **23.0–39.0 mm**. Built at
**T1_SUB=2**: 252 749 v, `VERIFY: 0 fail, 0 warn`, all four shut lines 100 % open.

#### 10.102.6  A FOURTH GUARD, ARMED ON THE NEW FINDING

The three rev-42 guards are **kept and re-armed**, not reverted with the
geometry — rev 23's rule cuts both ways, and *radial clearance from the arch
circle* is still the invariant the boolean cares about; it is simply satisfied
with room to spare now instead of exactly. One is added, because the finding
this revision established — **the bottom rail is flat** — was not guarded by
anything:

    _BOT_SPREAD = max(z) − min(z) over DOOR_BOT_RUN
    assert _BOT_SPREAD < 0.030

Armed at rev 41's own spread (16.0 mm) plus headroom for smoothing overshoot. A
re-introduced wrap descends **388 mm** and cannot pass it; neither can any
future construction that quietly leans the door's bottom rail.

#### 10.102.7  WHAT THIS CLOSES, AND WHAT IT COSTS THE INSTRUMENTS

**LEDGER finding 1 — "the art frame: the door is 272.2 mm / 387.5 mm deeper than
the art's outline" — IS CLOSED.** It was deeper *because rev 42 made it deeper.*
The art datum and the cut outline are one table again, so the two corner lobes
the art would have had to grow into **do not exist and there is nothing to
draw.** The owner's rev-44 answer to that question ("extend at drawn scale, do
not stretch") is recorded and **no longer has anything to apply to.**

`probe_rev44_doorart.py`'s **C3 and C4 now FAIL BY DESIGN**: they reproduce
§10.100.4's published corner depths (272.2 / 387.5 mm) and crown height
(0.8033), and those figures describe a shape that has been withdrawn. They are
**left armed and re-classified RED-BY-DESIGN** rather than deleted or relaxed —
a retraction that quietly re-points its own instrument is not a retraction.
`C5`, the KILL control on `door_pv`, is unaffected and still passes.

#### 10.102.8  NEW RULES

* **AN ORDINAL FACT LICENSES A SIGN, NEVER A SHAPE.** §10.100.2 was right that
  the sign was wrong and right that a sign needs no ruler. It then spent that
  credit on a magnitude. If an ordinal reading is about to force a
  *construction*, **stop and go find a frame that can carry the magnitude.**
* **A LEADING QUESTION IS NOT EVIDENCE, EVEN WHEN THE ANSWER IS YES.** §10.100.3
  banked a hedge verbatim on one sentence — good — and then took a question that
  named its own answer at full strength.
* **INVENTORY THE FRAMES YOU ALREADY HOLD BEFORE ASKING THE OWNER FOR A NEW
  ONE.** `PHOTOS_WANTED_rev44.md` item 4 asks him for "the door, full outline,
  with the art on it" *and in the same paragraph says we already hold the frame
  that shows the full outline.* The measurement that settled this took eleven
  minutes on a file that had been tracked for two revisions.
* **WHEN A FIX CANNOT BE BUILT AT ANY TOLERANCE, SUSPECT THE THING IT IS FIXING.**
  Three independent constructions for "carry the shut line down behind the wheel"
  each failed against a different guard. That is not three unlucky attempts; it
  is the geometry saying the feature is not there.

---

### 10.103  rev 44 — ROUNDED EDGES ON EVERY SHADER. 66 566 KNIFE EDGES, ZERO BEVELS, AND THE ONE WAY TO FIX IT THAT CANNOT MOVE A MEASURED VERTEX

#### 10.103.1  THE OWNER SET A NEW BAR, AND THE FIRST THING TO DO WITH IT WAS COUNT

*[stated, rev 44]* He supplied a catalogue-grade product render of a school bus
and asked for **"the very highest resolution, fidelity, and detail possible."**
That is a target, not a measurement, so `probe_rev44_fidelity.py` was written to
turn it into numbers off the built scene rather than into an opinion:

| what | built |
|---|---|
| mesh objects | **190** |
| triangles | **655 944** — of which **505 538 (77 %) are in `T1_body` alone** |
| objects with a Bevel modifier | **0 / 190** |
| edges over 28° (hard edges) | **66 566** = 10.3 % of 649 268 |
| rivets / bolts / screws / nuts / hinges / latches | **0 / 0 / 0 / 0 / 0 / 0** |
| materials with true displacement | **0 / 42** |

**The density is all in the skin and almost none of it is in the detail.** And
every one of those 66 566 hard edges is mathematically sharp. **No real
pressed, cast or extruded part has a sharp edge** — it has a fold radius, that
radius carries a thin specular highlight, and that highlight is most of what
the eye reads as *a photographed object* rather than *a computer model*.

#### 10.103.2  WHY THIS IS DONE IN THE SHADER — AND WHY THAT IS NOT A COMPROMISE

A Bevel **modifier** moves vertices. This model's geometry is measured. The
tightest clearance in it is **0.85 mm** (§10.102.4), roughly forty asserts are
armed on distances of a few millimetres, and the shell spent six revisions
recovering from booleans that a chamfer is exactly the kind of thing to break
again.

Cycles' **Bevel node** perturbs the *shading normal* by ray-tracing the local
surface. There is no code path by which it can move a vertex. It is the one way
to buy this at **zero risk to a measured model**, and at this scale it is also
simply the right answer: at 600 px/m a 2.75 mm fold is **1.6 px**, which belongs
in the shading and not in the silhouette.

#### 10.103.3  THE RADIUS IS DERIVED, NOT CHOSEN

`t1_shell.GAPW` is the panel-gap width, **5.5 mm, measured**. A shut line is two
folded panel edges facing each other across that gap, so **each fold's radius
cannot exceed half the gap** or the two folds meet and the gap closes. `GAPW/2`
is therefore the *geometric ceiling* on a fold radius in this vehicle. Written
as the expression, not as 0.00275 (§10.25), so re-measuring the gap moves it.

#### 10.103.4  IT COMPOSES WITH THE WEATHER GROUP RATHER THAN REPLACING IT

Every painted panel already drives `Principled.Normal` from the WEATHER group's
internal Bump — that is the orange peel. `round_edges()` re-routes that source
into the **Bevel node's own Normal input** and the Bevel into the BSDF, so the
peel is *rounded* rather than discarded. Where nothing drives Normal, the Bevel
drives it directly. **42 materials patched, 0 skipped, 0 already had one.**

Idempotent by node type, so a second call is a no-op. **`T1_NOBEVEL=1` stands
the whole pass down**, so the A/B is one environment variable and needs no edit
— rev 20's pattern.

---

### 10.104  rev 44 — THE CAB. A 12-TRIANGLE DASH, ONE BOX SEAT, NO HINGES ANYWHERE, AND A STEERING WHEEL MOUNTED LIKE A SHIP'S WHEEL ON THE CABIN WALL

#### 10.104.1  WHAT WAS BEHIND THE WINDSCREEN

In a 78 mm front three-quarter hero the windscreen is a large, bright,
**transparent** part of the frame and the eye goes straight through it. The
inventory:

| object | triangles | what it is |
|---|---|---|
| `dash` | **12** | a 165 × 115 mm four-point box swept the cab's full width |
| `seat_base` | 76 | a rounded-rect prism, corner radius 50 mm in **4 steps** |
| `seat_back` | 76 | the same |
| `wheel_rim` | 448 | a bare torus — **no spokes, no hub, no horn button** |
| `col` | 60 | a cylinder |

**And nothing else.** No second seat, no instrument, no gear lever, no pedals,
no sun visors, no mirror, no glovebox. A 4 m vehicle whose most-looked-at
aperture opens onto four boxes.

#### 10.104.2  THE STEERING WHEEL WAS FACING SIDEWAYS, AND THE BUILD PRINTED IT

`place(w, rot=(radians(72), 0, 0))` rotates a Z-normal disc about **X**, which
takes its axis to **(0, −0.951, 0.309)** — 18° off the vehicle's own **Y** axis.
It was mounted like a ship's wheel on the cabin wall.

**This needs no photograph and no scale.** The built dimensions say it out loud:
**0.402 × 0.124 × 0.382** — the disc's full 0.402 m diameter lies in X *and* Z,
and the 0.124 m Y extent is 0.402 × 0.309, the projection of a disc whose normal
is nearly Y. A sign error, and a sign does not need a ruler (§10.100.2's one
sound argument, used here for what it is actually good for).

#### 10.104.3  THE COLUMN CARRIED THE SAME BUG, AND THE TWO ARE ONE BUG

`col` ran along **(+0.30, 0, 0.95)** — up and *forward* — putting its upper end
at x 1.798 while the wheel it is supposed to carry sat at x 1.640: **158 mm
behind it.** A steering column rises from the box at the front beam and leans
**back** to the driver, who is at x 0.98. Corrected to **(−0.30, 0, 0.95)**.

#### 10.104.4  THE WHEEL IS NOT RE-AIMED BY EYE — IT IS CONSTRAINED

**A steering wheel is normal to its column and centred on the column's end.**
That is what a steering wheel *is*: a constraint, not a measurement. So both the
wheel's plane and its centre are now **derived from `col`**, as
`atan2(ax, az)` and `COL_MID + normalize(COL_AX)·COL_LEN/2`. Move the column and
the wheel follows. The angle that falls out is **17.5° from horizontal** — flat,
bus-like — and it is flat *because the column is at 17.5°*, not because a number
was picked to make it look right.

#### 10.104.5  WHAT WAS BUILT

Steering wheel: rim (unchanged, 0.1920 major / 0.0088 minor) plus **two spokes**
— a 1963 T1 is a two-spoke wheel and they run across the car — a dished hub and
a chrome horn button. Dash: a **seven-point swept fascia**, 215 mm deep and
182 mm tall, whose top face lands on **`Z_SILL`**, the cab door's window sill,
guarded every revision; a **speedometer** (chrome bezel, dark dial, glass) set
normal to the column like everything else the driver looks at; the centre
**letterbox grille**; a **glovebox lid and knob** on the cabin face. Seating: the
driver's seat kept **at its exact rev-8 footprint**, a **passenger seat**
mirrored to −Y, corner segments **4 → 10**, and a **cream welt** round each
cushion — which is what separates upholstery from a block at any distance. Plus
**sun visors**, an **interior mirror** on its stem, a **gear lever and knob**,
and **three pedals**.

**The fascia is `paint`, not `dark`.** A T1 dash is painted the body colour, and
the cab was one flat "dark" key because `build.py` assigns one material per
call. `cab_fitout()` therefore returns **(object, material key) pairs**.

#### 10.104.6  AND THE FIRST HINGES IN THE PROJECT

The fastener census returned **zero** of everything. A T1's cab door hangs on
**two external butt hinges** on its forward edge; they stand proud of the skin,
their barrels catch the key light, and they are among the most legible pieces of
hardware on the flank.

**They are not placed by eye.** Both sit on the cab door's own forward shut line
— `DOOR_GAP`'s front edge, which rakes back 0.0951 m over 0.950 m — the barrel's
axis **is** that rake, so the hinge line is parallel to the edge it hangs from by
construction, and each is seated on the skin by **`t1_core.flank_y`**, the same
function the shut lines and the script use. The two heights are the **quarter
points of the door's own front edge**, expressed that way rather than typed.

#### 10.104.7  WHAT IS DECLARED, NOT CLAIMED

**No frame in this repo resolves the cab interior.** None of the furniture above
is measured and none of it is offered as measured — it is type-correct 1963 T1
cab furniture, placed off members that *are* fixed (the cab floor's top face,
`Z_SILL`, the windscreen corners, the column, the existing seat's footprint) so
that it cannot drift independently of the shell. **Ledger class 4 —
uninstrumented.** A cab interior frame is now the highest-value photograph on
the wanted list, ahead of everything except the off side.

#### 10.104.8  AND ONE THING DELIBERATELY *NOT* DONE

The reference is a **factory-clean product render**. This is a **weathered 1963
working food truck**, and SPEC §4.3's chalky finish (`Roughness` 0.420,
`Coat Weight` 0.02) is **measured** — rev 3's mirror clearcoat is what made the
red read salmon at 0.37 against the reference's 0.82. **The detail bar
transfers. The finish does not.** Raising the gloss to match a photograph of a
different, newer vehicle would be regressing a measurement to chase an
aesthetic, and it is refused here in writing so it is not quietly done later.

---

### 10.105  rev 44 — THE CABIN FILL, AND THE DELIVERY FRAME. A CAB YOU CANNOT SEE IS A CAB THAT WAS NOT WORTH BUILDING

#### 10.105.1  §10.104 BUILT A CAB AND THE NEXT HERO SHOWED NONE OF IT

Measured on that frame, inside the windscreen: **45 DN against a cream body
band of 138 — a ratio of 0.325.** The two-spoke wheel, the fascia, the
instrument, the second seat, the visors and the lever were all there and all
invisible.

#### 10.105.2  THE TARGET IS MEASURED, AND IT IS A RATIO SO IT NEEDS NO EXPOSURE MATCH

`ref_nolita_doorshut.jpg`'s **cab door window** — 9× crop, rows 141–172,
cols 52–118 — shows the far wall, the seat back, the column and the steering
wheel's rim plainly. Against the cream band **directly below it** (rows 178–186,
same columns), so both sides of the ratio are under the same light:

| | reference |
|---|---|
| cab glazing, median | **108 DN** (p10 56, p90 168, n = 2046) |
| cream band, median | **232 DN** (n = 528) |
| **interior / cream** | **median 0.466, mean 0.494** |

Taking a *ratio against locally-adjacent cream* is deliberate. §10.29's finding
29 was a unit error from comparing quantities that had been through different
transfer functions; a same-frame, same-neighbourhood ratio cannot repeat it.

#### 10.105.3  WHY THE RIG DOES NOT DO THIS ON ITS OWN — STATED, NOT PATCHED AROUND

In the photograph **the cab is lit through the far side**: the opposite cab
door's glazing is the brightest thing in that crop. In the studio the same path
exists but arrives through two tinted panes and past `galley_backdrop`, so it
lands an order of magnitude down. `studio.cabin_fill()` stands in for that path.
It is a **presentation device and it is declared as one**: an 0.80 × 0.80 m box
inside the cabin, below the roof skin and forward of the B-pillar, and
**`T1_NOCABFILL=1` removes it** so any exterior measurement can be re-run
without it.

**It is placed at x 1.05, not 0.72.** At 0.72 the box sits aft of the B-pillar
and spills straight out through the three open serving bays — the kind of leak
that makes a fill light a cheat instead of a stand-in.

#### 10.105.4  THE CALIBRATION, AND IT SATURATES

Four renders, same view, same seed, same 40 samples, same measurement boxes:

| power | windscreen median | interior / cream |
|---|---|---|
| **0 W** (ablated) | 45.0 | 0.325 |
| **13 W** ← shipped | 68.3 | **0.494** |
| 21 W | 71.3 | 0.516 |
| 46 W | 81.0 | 0.586 |

**Strongly saturating** — 0.0091 ratio per watt over the first 21 W and
0.0028 per watt over the next 25 — because the interior is already carrying
bounce and the fill is competing with it. A linear extrapolation from the first
two points would have landed at 46 W and blown the target by 26 %, which is why
four points were rendered and not two.

**13 W lands at 0.494 against a target whose own median and mean are 0.466 and
0.494.** The render sits *inside the reference's own median-to-mean spread*, and
that is where the calibration stops: chasing the median to three digits through
a JPEG at 86 px/m would be precision the source cannot support.

#### 10.105.5  THE EXTERIOR ABLATION

The fill lifts the whole exterior **+0.75 %** (mean 150.42 → 151.55 DN over
111 594 non-backdrop pixels outside the cab aperture). That is light leaving
through the windows, which is what an interior light physically does, and it is
reported rather than suppressed. Per-pixel |Δ| runs 3.44 DN mean — **at 40
samples that is dominated by Monte Carlo noise, not by the light**, and this is
recorded so nobody later reads 3.44 as a signal.

#### 10.105.6  THE DELIVERY FRAME — `hero`, A SECOND VIEW, NOT AN EDIT

Measured on the rev-44 hero: the subject fills **70 % of the frame vertically
and 61 % horizontally**, floating in white. The reference the owner set the bar
with fills its frame.

`hero34f` is **kept bit-identical** — every rev-8-to-43 measurement was taken
through it — and `hero` is a **second view derived from it** by
`_pull_in()`, which moves the camera along **its own axis**. The perspective
character §10.8's 78 mm lens carries is therefore untouched; only the distance
and the target height move. 70 % → 88 % of frame height is a distance scale of
70/88 applied to `hero34f`'s own offset vector, giving **12.20 m**; the target
rises to **z 1.55** because the subject is **3.046 m tall with the lids up** —
the build's own printed bbox — and 1.34 left only 64 mm of headroom.

At 3:2 that is a 3.754 m frame height for a 3.046 m subject: **81 % fill**,
against 70 %.

#### 10.105.7  NEW RULE

**A DETAIL YOU CANNOT SEE IS NOT A DETAIL.** §10.104 spent a revision building
a cab and the very next frame proved none of it. Every future detail pass ships
with the frame that shows it, or it does not ship.

---

### 10.106  rev 44b — **THE FORWARD LOWER LOBE.** §10.102 WAS RIGHT ABOUT THE HALF OF THE DOOR IT MEASURED AND THEN ASSERTED IT OVER THE WHOLE DOOR

#### 10.106.1  HIS REPORT

*[verbatim, rev 44b]* **"the door curves around the front of the wheel well and
not the back. So you removed too much door."**

He is right, and so is the frame. §10.102 retracted §10.100's wrap because
`ref_nolita_doorshut.jpg` holds the bottom rail flat and stops the rear shut
line on it. **That reading was correct for the part of the door it covered.** It
was taken over **cols 60–122** — the arch and everything aft of it — and I then
asserted flatness over the *whole* door and armed a guard on it. Forward of
col 56 the same scan had already printed no line at all in that row band, and I
read that as noise instead of as the line having gone somewhere else. **It had.**

#### 10.106.2  THE MEASUREMENT — sub-pixel, three-point parabolic on the row gradient

| feature | window | row |
|---|---|---|
| bottom rail, over the arch | cols 70–118 | **238.58** |
| arch lip crown | cols 70–118 | **241.46** |
| **forward lower lobe** | cols 30–48 | **264.58** |
| body's lower edge | cols 30–48 | **273.50** |

The lobe's edge peaks at `|dL|` 18.9 against a floor of 0.5–2.0 over thirty
rows. It is not marginal.

#### 10.106.3  EVERY CONSTANT IS DIMENSIONLESS, AND THAT MATTERS HERE

Three independent scales are available and they **span 3 %**: arch radius
**105.9**, rear rim OD **104.2**, hub-to-hub wheelbase **107.4 px/m**. So
nothing below is expressed in metres.

* **DROP** = (264.58 − 238.58) / (273.50 − 238.58) = **0.7443** of the rail's own
  height above the body's lower edge — anchored to two features of *the door
  itself*.
* **RAMP** = the step's two feet at **0.8877** and **1.1406** of the arch's own
  radius forward of the axle. The ramp therefore **straddles the arch's forward
  lip**, which is where a door that clears a wheel puts it.

Built: ramp x 1.6316 → 1.7260 against the arch's forward lip at 1.6735; lobe
bottom z 0.5039, a drop of **308.1 mm = 0.7446** of rail-to-sill.

#### 10.106.4  WHAT IS UNTOUCHED

The rail **above the arch** — 2.88 px = 27 mm above the lip against rev 41's
shipped 23–39 mm. §10.102's finding stands exactly where it was measured; this
adds the part of the door it never looked at. And **`DOOR_GAP` stays
bit-identical as the art datum** (§10.100.6's one good idea): the lobe goes into
the cut outline only, spliced rather than re-typed so the seventeen shared
points cannot disagree. Nothing needs drawing into it — the flank's folk art is
continuous across this panel gap in every frame we hold.

`_MIN_RAD` **0.024381** against rev 41's 0.024426; `_MIN_SILL` 0.124;
T1_SUB=2 builds 257 642 v, `VERIFY: 0 fail, 0 warn`.

#### 10.106.5  THE GUARD THAT SHOULD HAVE EXISTED

§10.102 deleted a feature that a photograph holds and **nothing objected**. Two
guards now:

* `_BOT_SPREAD` is **re-scoped to the span that was actually measured** —
  x ≤ the arch's forward lip. It is a *stronger* test than before, because the
  span is stated instead of assumed, and it still kills §10.100's 388 mm arc.
* `_LOBE_DROP_BUILT` asserts the lobe reproduces **0.7443**, and a second assert
  fires if it is ever flattened below 0.50. **Armed on the dimensionless
  measurement**, so it tests what was measured rather than a metre value derived
  from a px/m the sources disagree about.

#### 10.106.6  NEW RULE

**A MEASUREMENT'S WINDOW IS PART OF THE MEASUREMENT.** §10.102 published "flat
to 0 px over 62 px of door" — true — and then wrote a guard saying the door is
flat. The window was in the sentence and I still generalised past it. **State
the window in the guard, not just in the prose.**

---

### 10.107  rev 44b — **EVERY STROKE END ON THE RING.** THE DOCSTRING HAS CLAIMED IT SINCE REV 15 AND THE GEOMETRY HAS NEVER DONE IT

#### 10.107.1  HIS REPORT, AND WHAT THE BUILT GLYPH ACTUALLY DOES

*[verbatim]* **"The vw still doesn't look right."**

Measured on the built emblem, radius of each stroke end as a fraction of the
ring radius, with the ring's band spanning **0.800–1.000**:

| end | reach |
|---|---|
| W's two **bottom** vertices | **0.840** — into the band |
| W's two **outer arm** tips | **0.738** — 62 mm short of it |
| V's two **arm** tips | **0.724** — 76 mm short of it |

`_fit_glyph` scales by the **single furthest vertex**, so whichever end reaches
furthest lands in the band and **drags every other end short**. Only the W's
bottom has ever touched. **Four of the six strokes have been floating inside the
ring since rev 15** — and rev 17 caught exactly this for the V's tips, scaled
them by 0.8140/0.7154, and then `_fit_glyph`'s divisor moved underneath them
again because the W was left where it was.

#### 10.107.2  THE PHOTOGRAPH IS UNAMBIGUOUS

`ref_nolita_front34.jpg`, red-mask row runs over the roundel's 41 × 66 px bbox:
at **y+6** the V's arms and the ring are **one run** on both sides; at **y+62**
the W's bottoms and the ring's lower arc are **one run**. Nothing floats. rev
15's own docstring says it in words — *"every stroke end — both V arms, both W
outer arms, both W legs — disappears into the ring band"*.

Two things the same frame **confirms** and which are therefore not changed: the
stroke width is **0.098 of the roundel diameter** against `wfrac` 0.1986 R =
0.0993 D, and the V's arm-tip half-separation reads 0.22–0.37 R against
`_V_TIP_X` 0.270.

#### 10.107.3  PUTTING THE SPINE ON THE CIRCLE IS NOT ENOUGH — AND THE FIRST ATTEMPT PROVED IT

Projecting all six spine terminals onto the band circle gave V tips **0.716** and
W bottoms 0.840: *worse for the V than before*. **What must land on the ring is
the OUTLINE, not the spine**, and the two differ by cap geometry — a terminal
end is cut flush *at* its spine point, while an interior vertex (the W's two
bottoms) is a sharp corner that bulges past it by `w / (2 sin(α/2))`.
Compensating analytically needs the mitre half-angle at each vertex, which is
exactly the kind of derived literal that has gone stale here twice.

Solved by **fixed point on the built outline** instead — the same pattern as
`t1_shell._G_BUILD`, and for the same reason: it re-solves itself if the width,
the angles or the mitre ever change. Converged, **all six ends read 0.8400**,
20 % into the band. **No angle moved**: the arm angles, the 12.29° separation,
the apex and the centre peak are all untouched — only the reach.

---

### 10.108  rev 44b — THE SIGN'S PROPS RAKED ACROSS THE ROOF INSTEAD OF STANDING UNDER THE BOARD

*[verbatim]* **"the props for the sign seem to meet something from the sides of
the sign, rather than the sign resting directly on the poles."**

Measured, and he is describing it exactly. Each prop ran from a foot at
**y +0.44** — the *show* side of the roof — diagonally across the whole opening
to a tip at y −0.776: a horizontal travel of 1.22 m against a rise of 1.00 m, a
**49° rake**. And it met the board at **0.86** of the board's width, which on a
board leaning 14° *past* vertical is near its top edge. A thin rod arriving at
49° and touching a nearly-vertical panel near its top does not read as a prop;
it reads as a stay wired to the sign's edge, which is the phrase he reached for.

**Contact was never the defect** — the tips measured 8.6 and 8.7 mm from the
lid's nearest vertex against a 7.5 mm rod radius. The *stance* was.

**Two changes, neither needing a photograph.** A prop stands *under* the thing it
props and meets it *at* the edge that bears — the same class of argument as a
steering wheel being normal to its column (§10.104.4):

* the tip moves **0.86 → 0.97** of the lid's width, onto the free edge, and its
  z now comes from **`zh`, the lid's own hinge origin**, so it lands on the
  panel's plane by construction (local z **0.00000**, at 1.0767 of the lid's
  1.1100 width);
* the foot moves to the **roof's own outboard edge**, found by walking `roof_z`
  outboard until it stops changing rather than by typing a y.

Built lean: **2.5° from vertical**, against 49°. Guarded at < 20°.

#### 10.108.1  AND ONE THING I GOT WRONG IN THE SAME EDIT, RECORDED SO IT IS NOT "FIXED" AGAIN

I first read this as a sign error: the comment says the props are "inset 160 mm"
and the code reads `LID_X1 + 0.16` / `LID_X0 - 0.16`, which looks outset. **It is
not.** `LID_X0` is **0.9640** and `LID_X1` is **−1.0700** — X0 is the larger — so
both are inset exactly as written. I inverted them, and the guard I added in the
same edit fired on the first build: *"roof-lid prop at x −1.2375 is OUTSIDE the
lid's own span 0.9640–−1.0700"*. **The guard was right and the change was
wrong.** The change is reverted, the guard is kept, and its bounds are now
written the way round the constants actually are.

#### 10.106.7  A NUMBER I RAISED AND KILLED IN THE SAME SESSION — AND WHY THE LOBE SURVIVES IT

While writing §10.106 up I traced the reference's body lower edge and published
a **~49 mm** discrepancy against the model, first as "possibly a datum error",
then — after a column-by-column trace showed **one continuous rocker with no
valance step** — as a settled finding, in `HANDOFF_rev44.md` and
`NEXT_CONTEXT_PROMPT_rev45.md`. **It is retracted.** The datum question was the
wrong thing to worry about: **the frame cannot see the edge at all.**

Raw pixels down `ref_nolita_doorshut.jpg` column 132: rows 268–276 run
(151,31,17) → (80,19,16), then rows **278–298 are RGB (0,0,0)** — twenty-five
rows clipped to pure black before the floor returns at row 300. The red does not
fade into the rocker; it hits a wall. Sweeping the mask threshold R>90 → R>30
moves the "lowest red row" from 274 to 277 and no further; at R>20 it jumps to
**303, which is the floor**. **Row 277 is where the shadow clips, not where the
body ends.**

The `ref_side.jpg` cross-check then disagreed in **sign** — rocker 145 mm *below*
the axle against Nolita's 38 mm *above* — and that trace is bad too: at cols
900–920, rows 640–700, the pixels are neutral (R≈G≈B, 58–147), so an
`R > G*1.25` mask passes **warm grey under-body shadow** as red.

**Both traces ran off the end of their data.** The body's lower edge relative to
the axle is **UNMEASURED**, and `RIDE_DROP` is not implicated by anything.

**NEW RULE.** *A threshold-based "lowest X" trace is only valid if the feature's
far side is resolved.* Check what is on the other side of the edge — and whether
the sensor can still see it — before you publish the edge.

**WHY §10.106 STANDS.** The lobe's *position* came from the ramp trace (the line
descending col 56 → col 46), not from the sill, and its *existence* from a
`|dL|` 18.9 edge against a floor of 0.5–2.0 well inside the exposed range. Only
its **depth** touches the sill, as the denominator of a ratio: if the true sill
is 3 px lower than row 273.50, the drop goes 0.744 → 0.686, i.e. 308 mm → 284 mm.
That is worth re-deriving from a frame that resolves the rocker, and it is not
worth moving on this one.

---

### 10.109  rev 44b — THE DELIVERY FRAME CLIPPED THE FRONT WHEEL, AND A FRAME DERIVED BY SCALING A VECTOR WAS NEVER GOING TO CENTRE ANYTHING

#### 10.109.1  WHAT THE FIRST DELIVERY RENDER ACTUALLY DID

§10.105.6 derived `hero` from `hero34f` by **scaling its offset vector** by
70/88 — the ratio of measured frame-fill to wanted frame-fill — and raising the
target to z 1.55 for the open lids. Rendered at 3200 × 2133 it put the subject
at **74 % of the width** and **hard against the bottom row: the front wheel is
clipped.**

**Two things were wrong, and the second is the general one.**

* **A distance scale does not centre.** It changes how much of the frame the
  subject fills and leaves it exactly as off-centre as it was.
* **A subject seen from above does not project symmetrically about its own
  centroid.** The near wheel is closest to the camera, so it drops furthest down
  the frame — which is precisely the part a "raise the target for headroom"
  correction pushes off the bottom edge. Measured: at 12.20 m / z 1.55 the bbox
  projects to v **−1.251 … +0.825**, i.e. **25 % past the lower edge** while
  leaving 18 % of headroom unused.

#### 10.109.2  SOLVED, AND SOLVED LIVE

`studio.fit_view()` iterates **both** the lateral target offset and the distance
against the projected corners of `subject_bbox()` — the scene's own bounding box,
read at render time and excluding the set (`cyc`, `pl_*`, ground). Re-posing the
lids, adding a part, or changing the aspect **re-solves the frame** instead of
quietly clipping it.

Solved for the 3200 × 2133 delivery frame at 78 mm, fill 0.92:

    dist 13.175 m   loc (10.8445, 7.2900, 3.1313)   tgt (0.1275, -0.1294, 1.2135)
    u -0.7373..0.7373    v -0.9200..0.9200    centred to 0.00000 / 0.00000

74 % of the width and 92 % of the height, **centred to five decimal places**,
with 8 % of margin on the binding axis.

#### 10.109.3  THE SIGN, AND WHY THE LOOP CARRIES A DIVERGENCE GUARD

The first implementation subtracted the lateral correction where it should have
added it — moving the **target** toward the side the subject is already on is
what swings the camera that way and brings it back. Inverted, the iteration is
unstable rather than merely wrong: it ran off to **2 × 10¹⁸ metres in sixty
passes** and returned a frame with zero fill. It now asserts on divergence, and
**asserts that the returned frame is not clipped** — which is the defect the
function exists to prevent, so it is the thing worth asserting (§10.45).

#### 10.109.4  WHAT IS NOT FIXED, AND IT IS THE LAST VISIBLE GAP AGAINST HIS REFERENCE

**There is no contact shadow.** `optics-6` has been open since rev 12 with two
prior attempts recorded in `studio.cyclorama`'s comment: rev 12 measured the
ground under the tyre at **177.00 against open ground at 177.00** and concluded
the catcher contributed nothing; rev 17's matte tap corrected that — the alpha
is *not* zero, there is a soft pool reaching **0.4980** — but the pool is
**0.0038 mean alpha in the 4–30 px band directly below the silhouette**, so the
composite over white moves a few code values and the vehicle still reads as
floating. The obvious lever is **refuted**: `T1_CATCH=0` renders the sweep as a
real lit surface and does produce a shadow (175.2 mean on the row below the
contact), but it brings back a 166-grey falloff with a hard horizon line, and
§6 locks the backdrop to pure white.

The cause is **the rig, not the catcher**: a 16 m strip plus a 0.76-albedo floor
fills the vehicle's own shadow. That is physically correct for this studio and
it is why the reference product render — which uses a harder key — has a shadow
and this does not. **It is an art-direction decision, not a fidelity defect**,
and per the standing rule for un-measurable aesthetics (finding 30) it goes to
the owner rather than being tuned. No photograph of this vehicle on a white
sweep exists to calibrate against.

---

### 10.110  rev 45 — **THE BADGE WAS A FLAT PLATE ON A CURVED NOSE.** TWO CONTEXTS FOUND IT INDEPENDENTLY AND NEITHER FOUND IT BY MEASURING THE GLYPH

**This is the section that answers §0 of `NEXT_CONTEXT_PROMPT_rev45.md`**, which
asked why the owner had reported the same defects three times while every guard
stayed green. Part of the answer is §10.113.4 — most of rev 44b was never
merged. The rest is here.

#### 10.110.1  WHAT HE WAS LOOKING AT

Rendered at any size, the nose badge read as a **clock face**: a ring, a V, and
two isolated stubs at 7 and 5 o'clock. No W. Every reference frame shows an
unmistakable V-over-W monogram filling its ring.

#### 10.110.2  EIGHT MEASUREMENTS OF THIS EMBLEM EXIST AND NOT ONE OF THEM COULD SEE IT

§10.25 measured the air gap between the V's apex and the W's peak. §10.107
measured all six stroke ends against the ring band. `probe_rev44_lampmove`
measured the badge's height from two independent chains and held it to 0.66 σ.
rev 45 re-measured the stroke width at **0.218 ± 0.002 R** photographed against
**0.2046 R** built, 0.7 σ, and left it alone.

**Every one of those was taken on the glyph's own outline, in the glyph's own
plane.** Not one involved the body the badge is fitted to. Rasterising
`vw_logo_fit`'s output directly gives a clean, correct V over W — which is
exactly what rev 44 also found, and it is why four separate hypotheses (the
outline, the cap fill, self-intersection, the material) were each cleared before
either context looked at the panel.

#### 10.110.3  THE MEASUREMENT, TWICE, FROM TWO DIRECTIONS

**rev 44** (unmerged until now), forward-most x of the body within |y| < 0.06:

```
    z 0.86-1.01 : the nose reaches x 2.1266 .. 2.1270   <- IN FRONT of the glyph
    z 1.01-1.16 : the nose falls back to 2.1262 .. 2.1194
```

with the glyph's front face at **2.1265**. Below z = 1.01 the nose buries the
emblem; above it the emblem stands proud. **The crossover is the exact height
where the render stops drawing.** The V lives above it; the whole W lives below.

**rev 45**, independently, by radial raycast at eight angles × three radii from
the badge's own centre:

| direction, at the ring radius | nose relative to the badge's front face |
|---|---|
| straight UP | **−31.6 mm** (falls away) |
| up-left / up-right | −19.0 mm |
| sideways | −0.6 mm |
| straight DOWN | **+3.0 mm** (comes forward) |

Same conclusion, different instrument, different scan. **The badge's upper half
floated up to 32 mm off the panel and its lower half was flush with it or
0.3 mm inside it.**

#### 10.110.4  THE FIX, AND WHY REV 44's IS SUPERSEDED RATHER THAN REJECTED

Rev 44 moved the mounting plane forward **13.5 mm** (`ROUNDEL_X` 2.1155 →
2.1290) so the glyph's rear face cleared the nose's maximum by 2 mm. That is
correct as far as it goes and it un-buries the W.

**A uniform shift can only ever be right at one height on a curved panel.** At
13.5 mm the badge still stands ~18 mm proud at its top. So rev 45 adds
`t1_core.drape_x`, which translates each vertex **in X only** by

```
    dx  =  surf_x(y, z)  -  mount  +  standoff
```

off a raycast lattice, where `mount` is the plate's own authored mounting
plane. The badge's front faces now stand **6.96 … 15.10 mm** proud everywhere.

`ROUNDEL_X` is kept, and the drape reads it: the drape is **invariant** to it —
moving it 13.5 mm changed the drape's `dx` from +1.1…+13.1 mm to −13.1…−0.4 mm
and left the built result identical to 0.01 mm. That invariance is the check
that the two fixes are the same fix, done to different tolerances.

#### 10.110.5  NOTHING IN THE GLYPH MOVED, AND THAT IS BY CONSTRUCTION

`drape_x` touches x only. The spine, the stroke width, the fit radius,
`ROUNDEL_D` and `ROUNDEL_Z_AG` are untouched, so `probe_rev44_lampmove`'s two
chains and SPEC:7005's *"DO NOT MOVE THE ROUNDEL WITH THE LAMPS"* trap are
unaffected **by construction, not by inspection**.

#### 10.110.6  WHAT REV 45 TRIED TO FIX AND REFUSED TO

The spine's stroke **angles**. Rev 45 de-foreshortened `ref_workshop.jpg`'s
emblem and read them off a polar unwrap — and then threw the answer away,
because de-foreshortening a three-quarter view of a circle needs the ring's axis
ratio and the two available fits disagree by **10 %** (§10.107's published 0.687
against rev 45's re-fit 0.764). Ten per cent of horizontal stretch is several
degrees on every angle, which is the whole size of the effect. **Rule 14 says
prefer dimensionless measurements; here the scale question *is* the measurement,
and it does not close.**

Rev 44's own angular finding — *"the V was 2.5× too wide-angled"* — used the one
method that survives this: **vertical extents only**, row-runs of the red mask,
per §10.107.2. That is the right instrument and it is now merged. Rev 45 adds
nothing to it and asks the owner for the frame that would close the rest
(`PHOTOS_WANTED_rev45.md`).

#### 10.110.7  THE GUARD, AND IT FIRED TWICE ON ITS OWN CHANGE

`build.py` asserts every emblem **front-face** vertex stands 0.5–30 mm proud of
the nose. It fired twice during this edit, both times correctly:

* at **−15.11 mm**, because the first draft guarded *every* vertex and the ring
  and disc carry material behind the skin on purpose;
* at **−3.59 mm**, because the second draft draped both plates against one
  common datum and the disc's front cone is authored to a different one.

Both are stated rather than quietly widened. The second is why `drape_x` takes a
`mount` per plate.

#### 10.110.8  THE RULE THIS EARNS

> **A PART MEASURED IN ISOLATION FROM WHAT IT IS FITTED TO IS NOT MEASURED.**
> Eight correct measurements of this emblem exist. Every one of them was taken
> in the emblem's own plane and every one of them was blind to a 32 mm error in
> the direction they did not look. Rule 10 says *a detail you cannot see is not
> a detail*; this is its converse — **a detail that measures perfectly and
> renders wrong is being measured in the wrong frame.**

---

### 10.111  rev 45 — THE HEADLAMPS. THE LENS WAS DISHED THE WRONG WAY ROUND, AND THE BEZEL'S BRASS WAS NEVER CONTROLLED

Found by the same method as §10.110 and it is the same defect class: a part
authored in its own local frame and never checked against the panel it is
fitted to.

#### 10.111.1  THE LENS

`t1_detail.headlamp`'s `lens_prof` ran, in (x, r):

```
    (0.0000, 0.0000)  ...  (0.0290, 0.0862)
```

— x = 0 **on the axis**, x = 0.029 **at the rim**. That is **concave**: a
saucer whose deepest point is in the middle. A headlamp lens is convex.

It was never visible as a shape error because of what it did instead. Raycast
down the near lamp's own axis, on the built body:

```
    hit T1_body   at x = 2.1116      <- the nose's outer skin
    hit T1_body   at x = 2.1088      <- its inner skin, 2.8 mm behind
    hit hl_lens   at x = 2.1015      <- the lens, 10.1 mm INSIDE the body
```

**There is no headlamp aperture cut in the nose**, so on the axis the camera
sees red sheet metal and the lens only emerges near its rim. The aperture
rendered as a dark red hole ringed by a brass grommet.

Turned convex, apex 3.0 mm behind the bezel's own front face (`ring_prof`'s
0.0235), radius of curvature 0.263 m over the 0.0862 m lens.

#### 10.111.2  WHAT THE MEASUREMENT WAS, AND WHAT IT WAS NOT

Measured **in the rendered frame** by `probe_rev45_nose`'s projected landmark:

| | render before | render after | photograph, unlit |
|---|---|---|---|
| lens / cream luminance | 0.432 | 0.423 | **0.565** |
| lens (R−B)/cream | **+0.571** | **+0.082** | **−0.024** |

**The luminance was never the defect.** It sat inside any reasonable window
throughout. The **chroma** was, and the first control written for this — a
luminance ratio — passed while the aperture was rendering red. C6 was added
because C4 could not see it.

**A hypothesis was refuted on the way and it is recorded.** The first
explanation was that a 0.018-roughness glass over a mirror bowl needs
roughening to scatter. A **17× sweep of both roughnesses was bit-identical**
(lens RGB 115–118, 41–42, 33 at every setting). Roughness is not the lever;
the geometry was. Both roughnesses are now overridable (`T1_HL_LENS_RG`,
`T1_HL_REFL_RG`) so the sweep can be repeated, and the retired mirror arm still
renders.

#### 10.111.3  THE BEZEL — brass RETIRED to chrome, and rev 10 is not called wrong

`build.py` assigned the ring `"brass"` on a rev-10 measurement while
`t1_detail.headlamp`'s own docstring said *"returns (chrome ring, …)"* — a
contradiction that stood for thirty-five revisions because nobody grepped
across the two files.

Rev 10's reading, on `ref_side.jpg`: bezel a\* +2.1 / b\* **+31.6** at L\* 65.6,
against five neutrals in the same frame at b\* −2.4…+1.6.

Rev 45's reading, on `ref_nolita_front34.jpg` — the same part at about four
times the scale, front three-quarter, resolved over ~15 px of arc, cool indoor
light:

| patch | a\* | b\* |
|---|---|---|
| bezel, top arc | +23.1 | **+2.7** |
| bezel, bottom arc | +16.1 | **+6.7** |
| white wall, same frame | +6.5 | **+6.9** ← the frame's neutral |
| red nose, 10 px outboard | +73.6 | **+61.8** ← the frame's warm |

**The bezel's b\* is indistinguishable from the frame's own neutral** and
nowhere near its warm surfaces.

**Rev 10 is not called wrong. It is called UNCONTROLLED.** Its five neutrals
are a door handle, a wing mirror, counter stainless, a lamppost and pavement.
Not one of them is *a small mirror-finish torus ringed by a large warm panel*,
which is the confound; and on `ref_side.jpg` — a flat side view — the bezel is
a few pixels wide at grazing incidence. A chrome ring surrounded by cream and
red bodywork reading b\* +31.6 in that frame is what the bounce predicts.

`ref_playa_34.png` settles the direction independently: the same part in low
direct sun reads **gold on its sunward arc and dark on the other**. That is
what chrome does. Brass is warm from every direction.

Built: b\* **+25.7** brass → **+1.7** chrome, against +2.7 photographed.
`T1_HL_BEZEL=brass` still renders the retired arm.

#### 10.111.4  THE INSTRUMENT THIS REVISION ADDS

`probe_rev45_nose.py` **does not type crop boxes.** Every previous crop box in
this repository is a hand-typed literal that goes stale the moment a camera or
a constant moves. This probe projects known 3-D landmarks through the render
camera with `bpy_extras.world_to_camera_view` and samples where they land, so a
sample follows `HL_Z` when `HL_Z` moves. Seven controls; **C5 is a KILL written
to fail forever** — a landmark placed one metre in front of the nose must not
land on the roundel, without which "the projection works" is untestable.

---

### 10.112  rev 45 — "100 % CALIDAD". THE GRADIENT THREW AWAY THE COLOUR THE GENERATOR DECLARES. REPORTED BY THE OWNER TWICE

`cal_gen.gradient` computed

```python
    t = ((xx - cx) * 0.62 + (yy - cy) * 0.78) / (1.35 * h)
    t = np.clip(t * 1.5 + 0.42, 0, 1)
```

`t` is **zero at the burst's own centre by construction** — `(cx, cy)` is
`starburst()`'s centre and the axis term is measured from it. A bias of **0.42**
therefore starts the ramp 42 % along, and the core evaluates to
RED × 0.16 + ORANGE × 0.84 = (234, 110, 23).

Measured off `tex/calidad.png` **as shipped**: core **(237.0, 120.3, 22.0)**,
G/R **0.508**. `starburst()` fills the whole polygon with
`RED = (214, 46, 30)`, G/R **0.215**, *nine lines above* — **and nothing in the
finished texture was that colour** except the extreme corner where the clip
bottoms out. The decal rendered **peach** where every photograph is **red**.

**The bias is now zero, and that is not a tuned number.** It is the statement
that the gradient *departs from* the burst's declared colour going outward
rather than starting two-thirds of the way to orange. RED at the core, ORANGE
through the middle distance, YELLOW at the lower-right tips — which is the
direction the docstring's own sampled bands run.

Re-generated core **(216.6, 55.1, 28.2)**, G/R **0.255**, against the body
red's own albedo G/R 0.250. The burst and the coachwork are the same red
family, which is what `cal_gen`'s RED already said.

Rev 44 ruled out two other causes **by test** and both stay ruled out:
`WEAR['calidad']` is not the lever (re-rendered at 0.22, core bit-identical)
and the material adds no cream.

---

### 10.113  rev 45 — THE PROPS, THE MERGE, AND THE REAL REASON THE LOOP WAS BROKEN

#### 10.113.1  THE PROPS STOOD IN THE HOLE

Owner, rev 44b: *"the props for the sign seem to meet something from the sides
of the sign."*

Both feet were `Vector((xs, 0.44, roof_z(xs, 0.44)))`. `roof_z` returns the
roof **surface height** at (x, y) whether or not there is any roof left there —
and the roof aperture **is** the lid's closed footprint, y from `LID_Y_HINGE` to
`LID_Y_HINGE + LID_W` = −0.545 … +0.565. **Both feet sat at y = +0.44, inside
it.** Each prop rose out of thin air in the middle of the open serving hatch and
ran a metre across the board's printed face.

Rev 44b (§10.108) and rev 45 found this independently. **Rev 44b's fix is the
one that ships** and rev 45's is discarded: rev 45 typed `LID_Y_HINGE − 0.14`;
rev 44b walks `roof_z` outboard until it stops changing and lands on the roof's
**own** edge, and moves the tip onto the lid's free edge as well — 49° of rake
down to 3°. A measurement of the body beats a number about it.

Rev 45 keeps only its **Y guard**, which is complementary to rev 44b's lean
guard: the lean catches a prop that *rakes*, the Y catches a prop that *stands
on nothing*.

#### 10.113.2  A TRAP THAT CAUGHT BOTH CONTEXTS

The comment says the struts are *"inset 160 mm"* while the code writes
`LID_X1 + 0.16` and `LID_X0 - 0.16`, which **reads** as an outset. It is not:
`LID_X1` is the **aft** end at −1.0700 and `LID_X0` the forward one at +0.9640,
so both expressions move inward. Built: board x −1.0400…+0.9340, struts at
−0.910 and +0.804.

Rev 44b "fixed" it, its own guard fired on the first build, and it reverted.
Rev 45 read the same lines and reached for the same wrong conclusion, and was
stopped by **running the build instead of reading the source**. Recorded twice
now, so it stops the third context.

#### 10.113.3  THE REFERENCE FRAMES WERE NEVER LOST — THEY WERE NEVER MERGED

`NEXT_CONTEXT_PROMPT_rev45.md` §4 says *"Reference photographs (8, all
tracked)"* and names four Nolita frames. **One was in the tree.** Item **W1** —
the entire roundel-placement task — is specified against measurements taken on
`ref_nolita_front34.jpg`, which had never been committed. **W1 as written was
unexecutable.** See `REFERENCE_FRAMES_rev45.md`.

#### 10.113.4  AND NEITHER WAS THE REST OF REV 44b

`origin/claude/tacombi-combi-rev-44-h4ipmg` carried **seventeen commits above
the point where PR #2 was merged.** Neither `origin/main` nor the branch this
revision started from had any of them. Missing from the mainline:

* **`SPEC.md` §10.102 – §10.109**, all eight sections, 632 lines — including
  §10.100's retraction, the forward lower lobe, the six stroke ends, the props
  and the delivery frame;
* `cab_fitout`, `door_hinges` (`t1_detail.py`, +460 lines);
* `cabin_fill` (`studio.py`);
* `round_edges` on all 42 materials;
* the roundel's 13.5 mm mounting plane (§10.110.4);
* the hubcap red, the bumper/door overlap, the four reference frames.

**`SPEC.md` on `main` ends at §10.101.**

§0 of the rev-45 brief asks why *"the loop between measured fix and he can see
it is broken"* and offers three candidate causes, all of them about how the
owner is shown things. There is a fourth and it is simpler than all of them:
**the fixes were measured, committed, and left on a branch.** The brief was
written from a working tree that had them and handed to a context that did not.

Rev 45 merged all seventeen. Three conflicts — `build.py`, `t1_shell.py`,
`mark_rev45_q.py` — resolved in rev 44b's favour on the props and on
`mark_rev45_q.py`, in rev 45's favour on the drape, and keeping both guards.

#### 10.113.5  THE RULE THIS EARNS

> **A REVISION THAT IS NOT MERGED DID NOT HAPPEN.** Every green guard, every
> SPEC section and every measurement in those seventeen commits was correct and
> none of it reached the mainline. Before diagnosing why a fix did not land,
> check that the fix is *in the tree you are looking at* — `git log HEAD..<the
> branch the last revision worked on>` is eleven characters and it would have
> saved this one an entire investigation.

---

### 10.114  rev 45 — TWO QUESTION FIGURES, AND WHY THAT IS NOT ONE TOO MANY

`mark_rev45_q.py` is rev 44b's and it is right about what it is right about:
rev 36 shipped a figure with five mark classes and got back *"i don't
understand what is being asked"*, then shipped one crop, one circle, one
sentence and got the most valuable answer in ten revisions. **Its rule stands —
if he does not understand the question, the FIGURE is the defect, not him.**

`mark_rev45_ba.py` is rev 45's, and it obeys that rule: no boxes, no arrows, no
leader lines, one sentence per row. What it adds is not a mark class. It is two
more **pictures** per row — every row is **BEFORE | AFTER | PHOTOGRAPH** at
matched scale — because rev 44b's figure crops one render and therefore cannot
show that anything changed, and §0's three candidate causes are each killed by
a different one of those three cells:

* *"he means a different thing"* dies because the photograph is in the row;
* *"the fix is sub-threshold at the size he views it"* dies because the crop is
  magnified;
* *"he is looking at an older image"* dies because BEFORE is labelled next to
  AFTER.

Five controls, and **F5 is a negative control on the ordering of the changes**:
the badge's before/after difference must exceed the decal's, because one is
geometry and the other is a recolour. If that inverts, the wrong files are
wired up.

**Rev 44b's docstring forward-references "SPEC 10.110" for itself.** That
section did not exist when it was written; §10.110 is now the drape and the
question figures are here.

---

### 10.115  rev 45 — THE HEADLAMP BOWLS. FINDING 41 CLOSED, AND THREE CONTROLS THAT COULD NOT SEE THEIR OWN DEFECT

#### 10.115.1  THE DEFECT

**There was no headlamp aperture in the nose at all.** The lamp assembly was
fitted into unbroken sheet metal. Raycast down the near lamp's own axis on the
built body, before this change:

```
    hl_lens.001  ->  T1_body  ->  T1_body  ->  hl_bowl.001
```

The two `T1_body` hits are the 2.8 mm solidified skin. The reflector was behind
it and therefore invisible, and the lens was backed by body paint.

A 1963 T1's headlamp does **not** sit in a plain hole: the nose panel is drawn
back into a shallow bowl and the lamp sits in it, chrome rim on the outer face.
Both frames show it as a shadowed ring round the bezel —
`ref_nolita_front34.jpg` and `ref_playa_34.png` — and that shadow is most of
what makes a lamp read as set **into** a panel rather than stuck **on** it.

#### 10.115.2  THE FIX, AND WHAT IN IT IS AUTHORED

`t1_shell.headlamp_recess_cutters` issues one bore per side in **step 3**, with
the other apertures, while the shell is still a plain solidified skin.
`HL_X`/`HL_Y`/`HL_Z` are **hoisted to step 0 verbatim** rather than duplicated —
a cutter cannot read a constant defined three hundred lines later, and re-typing
it is §10.25's defect class exactly.

**The depth (52 mm) and the straight-sided section are AUTHORED, NOT MEASURED.**
No frame we hold resolves the bowl's section; it is inside the bezel in every
one of them. Both numbers live in one place so a later measurement replaces two
values and nothing else. `PHOTOS_WANTED_rev45.md` asks for the frame.

`T1_HL_BOWL=0` skips the cut and restores the un-bored arm.

#### 10.115.3  THE BORE IS COUPLED TO THE REFLECTOR, AND THAT IS THE INTERESTING PART

Before the bore the lens was backed by sheet metal, which is why it read as a
mid-grey disc — **accidentally close to the photograph, for the wrong reason.**
Cutting the bore exposes `hl_bowl`, a `metal = 1.0` mirror, and a mirror in an
unlit cavity returns the cavity. Measured through `probe_rev45_nose`'s projected
landmark, at the **shipped** reflector settings:

| | un-bored | bored | photographed |
|---|---|---|---|
| lens / cream | 0.423 | **0.549** | 0.565 |
| lens (R−B) / cream | +0.069 | **+0.027** | −0.024 |

Both move toward the photograph. A four-arm sweep of the reflector
(`T1_HL_REFL_MET` × `T1_HL_REFL_RG`) was run and **the shipped defaults win** —
roughening or de-metalling it moves lens/cream to 0.458–0.700 and away from
0.565. Nothing about the reflector is changed.

#### 10.115.4  THE FIRST EYEBALL READ OF THIS SPIKE WAS WRONG, AND SO WAS THE FIRST CONTROL

Two errors on one change, both caught, both recorded.

**The eye.** The first look at the bored arm — a 48-sample `T1_SUB=1` crop —
read as *"worse: a deep dark hole"*, and the spike was very nearly reverted on
it. The A/B at 64 samples against the photograph overturned it outright: bored,
the aperture has a highlight, a bright arc and depth; un-bored it is a flat dull
disc. **Rule 10 cuts both ways — a detail you cannot see is not a detail, and a
detail you looked at badly is not looked at.**

**The control.** C8 was first written as *"the first object down the lamp axis
is `hl_*`, not `T1_body`"*, straight off the measurement that found the defect.
**It passed in both arms.** That measurement was taken on the *concave* lens;
§10.111.1 had since turned the lens convex with its apex at 2.1220, in front of
the nose, so the first hit is the lens whether or not the bore exists. **The
control passed on the very defect it was written for** — rule 18, inside the
probe that rule 18 came from.

Re-written to walk the axis and require that **no `T1_body` face lies between
the lens and the bowl**, which is what the bore actually changes. It now reads:

```
    bored     hl_lens.001 -> hl_bowl.001                        PASS
    un-bored  hl_lens.001 -> T1_body -> T1_body -> hl_bowl.001  FAIL
```

**A control is not finished when it passes. It is finished when you have watched
it fail on the defect.** `T1_HL_BOWL=0` exists so that stays cheap forever.

#### 10.115.5  WHAT IT COST THE GUARDS

The bore changes the body's manifold state, which is the same class of change as
rev 12's roof hole, so `verify.py`'s non-manifold count and every shut-line probe
were re-read at **both** subdivision levels rather than at one.

---

### 10.116  rev 45 — **`optics-6` CLOSED.** THE VEHICLE FLOATED FOR THIRTY-THREE REVISIONS AND EVERY MEASUREMENT OF IT WAS TAKEN SOMEWHERE THE SHADOW ISN'T

#### 10.116.1  THREE PRIOR MEASUREMENTS, ALL IN THE WRONG PLACE

| rev | what was measured | verdict |
|---|---|---|
| 12 | side **ortho**, `T1_BGW=1.0`: ground under the tyre 177.00 against open ground 177.00 | "the catcher contributes exactly nothing" |
| 17 | matte tap on a **400×300** frame: alpha pool reaches 0.4980, but 0.0038 mean in the 4–30 px band below the silhouette | "a different symptom" |
| 44 | none; the ledger carries rev 17's | — |

**Two of the three read a side orthographic view.** In a side ortho the camera
is level with the vehicle and the ground plane is edge-on, so "the band below
the silhouette" is not ground at all — it is the three or four pixels where the
ground vanishes to a line. There is no contact patch to see from there. The
third read a matte in which a tyre is twelve pixels wide.

**A contact shadow is a thing you look DOWN at.** `probe_rev45_ground.py`
measures it in `hero34f`, the delivery frame, and finds the ground by
**projecting the four contact patches through the render camera** — from
`X_AXLE_F`, `X_AXLE_R`, `TRACK_F`, `TRACK_R` and z = 0, none of them typed.

#### 10.116.2  THE PROBE CAUGHT ITSELF FOUR TIMES BEFORE IT CAUGHT THE DEFECT

Every one is recorded at the code rather than tidied away, because each is a
different way for an instrument to look healthy and be wrong.

1. **A contaminated sample.** The first window was an annulus round the contact
   patch keeping "neutral" pixels, on the reasoning that ground and backdrop
   are neutral and the body is not. **The body is** — the cream renders
   (192, 192, 188), max-minus-min 4. It reported G1 = 0.8639, a real-looking
   number about the vehicle's own flank.
2. **An inert kill control.** C4 sampled open ground 10 m ahead, which projects
   off-screen; it returned `<no sample>` and **passed**. Then 4 m to the off
   side — also off-screen, also passing. It now walks a list of candidates and
   prints the one it used.
3. **A blind level control.** C3 read the frame's top two corners and reported
   "255.00, PURE WHITE" for `T1_CATCH=0` — a frame with a **hard horizon across
   it** and a grey sweep filling the lower two-thirds. The horizon sits about
   18 % down; the corners are above it.
4. **The wrong window.** With all of the above fixed, G1 read 0.9975 — "it
   floats" — while a shadow was plainly present. The window was 0.5–3.5
   tyre-widths below the patch, 8 to 54 cm of ground. Profiled in 0.25 TW steps:

   ```
   fl   219 244 246 247 248 249 250 250 251 251 251 252 252 252 252 252
   rl   236 251 252 253 254 255 255 255 255 255 255 255 255 255 255 255
   ```

   against open ground 252. **The whole shadow lives in the first ~0.35 TW —
   about 5 cm — and the window started where it had already ended.** Rule 8: a
   measurement's window is part of the measurement.

#### 10.116.3  THE BASELINE, AND A PHOTOGRAPHED TARGET

| | G1, tight contact | G3, under-body pool |
|---|---|---|
| built, before | **0.9756** | **0.9132** |

Photographed on his own truck — ground at the tyre over open ground, same
frame, which cancels exposure and surface:

| frame | ratio |
|---|---|
| `ref_playa_34.png`, front wheel | 0.3049 |
| `ref_playa_34.png`, rear wheel | 0.7300 |
| `ref_nolita_front34.jpg` | 0.6950 |
| `ref_nolita_flank.jpg` | **0.8713** ← the weakest |
| **mean** | **0.6503 ± 0.2101** |

**The target is the weakest reading, not the mean.** The sd is a third of the
value and the boxes are hand-placed; what the four agree on is a **sign**, not
a magnitude (rule 6). Every photograph of this vehicle has a substantial
contact shadow and the render had none.

#### 10.116.4  TWO LEVERS REFUTED BEFORE THE THIRD WORKED

**`T1_CATCH=0` — refused again, and rev 12 was right.** Re-run with an
instrument: it buys **G1 0.9756 → 0.6924** and pays with a backdrop whose
row-to-row step goes **0.100 → 22.123 DN**, i.e. a hard horizon. SPEC §6 locks
the backdrop to pure white. Refused, this time with both numbers.

**A plain gain on the catcher's alpha — refuted by its own control.** The
argument was that the backdrop is alpha 0 and `0 ** k == 0`, so it stays white
*by construction*. C3 disagreed: the upper-margin level fell **254.97 →
250.91** as the gain rose. Moving the node upstream of the bloom changed
**nothing**, which is what refuted bloom as the cause. The real cause is that
**the "sweep" is not empty space — it is the cyclorama, a shadow catcher, and
it fills most of the frame.** A catcher's alpha far from the subject is not
zero, it is a noise floor of a few thousandths, and a power function amplifies
small numbers hardest (0.002 ** 0.31 = 0.13). So any gain greys the whole sweep
before it deepens the contact shadow.

#### 10.116.5  WHAT SHIPS

Subtract the noise floor, **then** gain, then clamp:

```
    a'  = clamp( (a - T1_SHADOW_FLOOR) / (1 - T1_SHADOW_FLOOR) )
    a'' = a' ** (1 / T1_SHADOW)
```

Below the floor the backdrop goes to **exactly** zero, which is what the
`0 ** k == 0` argument needs to be true rather than nearly true. Applied on the
raw render layer. **The cost is stated rather than hidden: it also erodes the
faintest real shadow, so the floor is kept as small as C3 allows.**

At `T1_SHADOW=9.0`, `T1_SHADOW_FLOOR=0.030`:

| | before | after | photographed |
|---|---|---|---|
| G1 tight contact | 0.9756 | **0.8729** | 0.8713 ← the weakest reading |
| G3 under-body pool | 0.9132 | **0.8406** | — |
| G2 backdrop | 254.97 | **254.45** | must stay ~255 |

Pushed to `T1_SHADOW=20` the backdrop finally goes and C3 fires. **It is not
pushed there.**

**DECLARED AND ABLATABLE**, which is §10.105's template for a presentation
device: `T1_SHADOW=1.0` restores the floating arm exactly.

#### 10.116.6  THE RULE THIS EARNS

> **AN INSTRUMENT THAT HAS NEVER BEEN WRONG HAS NEVER BEEN TESTED.** This probe
> was wrong four times in one sitting — contaminated sample, inert kill, blind
> level, wrong window — and every one of the four produced a plausible number
> that would have been published. Three prior revisions measured `optics-6` and
> none of them found the defect, not because they were careless but because
> **nobody ever asked what their instrument would still pass on.**

---

### 10.117  rev 45 — THE PAINT, INSTRUMENTED. AND IT IS **ONE** FINDING, NOT THREE

Ledger finding 38 was measured once, by hand, in a scratch directory.
`probe_rev45_paint.py` makes it repeatable, and in doing so answers a question
nobody had asked: whether the flank's dullness, the hubcaps' pinkness and the
cream's greyness are one defect or three.

#### 10.117.1  PROJECTION IS NOT VISIBILITY

The probe copied `probe_rev45_nose`'s landmark technique onto the **flank** and
its first three landmarks were **all** wrong. Their visibility raycasts:

```
    red    first hit 'script_L'   the "Senor Tacombi" decal, 17 mm nearer
    cream  first hit 'fringe2'    the bobble fringe,          3 mm nearer
    cap    first hit 'cap1.31'    the cap's own rim,         36 mm nearer
```

**Three for three.** `world_to_camera_view` maps a point to a pixel whether or
not the point can be *seen*, and a flank carrying folk art, a script lockup, a
decal and a bobble fringe has very little clean paint left. The probe reported
the flank's red as RGB (176, 154, 156) — a pale grey — and every number
downstream was about the wrong surface.

Fixed two ways at once. Each quantity is now sampled over a **grid of candidate
points**, and a candidate survives only if the camera's ray reaches **it** first
*and* the pixel classifies as the material asked for. The value is the median of
the survivors and **the survivor count is printed**, because a count that
collapses is itself a finding: `red 21/24, cream 9/15, cap 3/25`.

**`probe_rev45_nose` does not have this test and is correct today by luck of
geometry** — its landmarks are on the nose and nothing on this vehicle overhangs
the nose. Recorded in that file, with instructions to copy `visible()` before
adding any landmark that is not on the front face.

#### 10.117.2  THE NUMBERS, AND THE INDEPENDENT REPRODUCTION

| | built | photographed | σ |
|---|---|---|---|
| **P1** body red, G/R of red÷cream | **0.455** | 0.223 ± 0.066 (4 frames) | **3.5** |
| **P2** hubcap red, G/R of cap÷cream | **0.603** | 0.274 ± 0.096 (3 frames) | **3.4** |
| **P3** cream warmth, (R−B)/G | **+0.0263** | +0.037 ± 0.013 (3 warm frames) | **0.8** |

**P1 reproduces the hand measurement exactly — 0.455 against 0.455 — by a
completely different method.** The hand figure came from a masked region of a
side render; this comes from a visible-population sample at projected landmarks
in the hero. Two methods, one number.

#### 10.117.3  ONE FINDING, NOT THREE

* **P2 tracks P1 at the same magnitude and the same sign** (3.4 σ against 3.5 σ)
  on a different object, a different material and a different part of the frame.
  The hubcaps are not separately wrong; they are wrong *the same way*.
* **P3 is inside 1 σ.** The cream's hue is right. It reads grey because it sits
  against a pure-white backdrop with a washed red beside it — a **context**
  effect, not a colour error.

So there is one cause, and §10.116's ablation already named it: about half the
excess is the white cyclorama's own specular return, and `T1_SPEC=0` alone moves
P1 0.455 → 0.347. **The albedo is not the defect** — `t1_mats.RED` is
sRGB(196, 49, 36), G/R 0.250, which is 0.4 σ from the photographed mean.

#### 10.117.4  P1 AND P2 ARE REPORTED, NOT GATED, AND THAT IS DELIBERATE

Finding 38's fix is an **open question for the owner** — Q6 of `rev45_ba.png`:
softening the studio would move the paint toward his own photographs and would
trade the catalogue-clean white background he supplied as the bar. §7 locks the
paint's *finish* and §10.104.8 refuses to re-open `Roughness` or `Coat Weight`;
this is neither, but it is still his call.

**Gating on a number whose fix has not been sanctioned would turn a question
into a fait accompli.** Only P3, which is already correct, is gated. When he
answers, the gate goes in here.

---

### 10.118  rev 46 — W1, THE CALIDAD TYPE WAS OFF-CENTRE **INSIDE** THE DECAL

**Written into `cal_gen.py` at rev 46 and cited there as SPEC 10.118 for two
revisions before it existed here.** Recovered at rev 48 — see 10.122.4.

Not the defect rev 44 closed. That one was the decal **panel's placement on the
vehicle** (Report 7, 0.180 of texture width). This is the **type's placement
within the decal**, which nobody had measured in forty-five revisions. Both are
true and they are different things; the placement stays closed.

Measured on the generator's own output, pre-rotation: the type block's centroid
sat at (0.3735, 0.6309) of the canvas against `starburst()`'s centre
(0.5050, 0.5750). In the shipped raster the miss was **(−0.1167, +0.1117)** —
"100%" hung off the burst onto bare cream and "Calidad" ran off the panel's
bottom edge (bbox reached y 0.953).

**The fix is structural, not tuned.** `BURST_CX`/`BURST_CY` promoted to
constants; `TYPE_SHIFT` expressed as (burst centre − measured pre-rotation
centroid). And the block now rotates about the **burst's** centre instead of
(0.500, 0.600) — those differ, so the −19.7° rotation was swinging a correctly
laid-out block back off centre. A rotation fixes its own centre, so the
centring is now exact and independent of `ANG`. Result **(+0.0001, −0.0001)**.

**Guard, in the same edit (rule 12).** `cal_gen` refuses to write a decal whose
type is more than 0.004 off centre. **Watched fail** at (−0.1099, +0.1127) on
the rev-45 layout and at (−0.0132, +0.0134) on 12 % of the correction — it
catches the residual, not just the gross miss.

**RETRACTION carried with it.** The rev-46 brief's photographed target
(+0.0455, +0.0746) is **withdrawn**. Calibrated against a synthetic decal at
the photograph's own scale with a *known* displacement, the instrument that
produced it reported ≈(−0.01, −0.04) for **every** truth value tried. It is
blind to the quantity it names: the closed-and-filled burst mask traps cream
between the spikes, and cream is bright and low-saturation. The photographed
target is **"centred"**, established visually; the residual is not resolvable
at 23 × 39 px.

### 10.119  rev 46 — W2, THE VW GLYPH'S VERTICAL PROPORTIONS

**Cited in `t1_core.py` since rev 46; recovered here at rev 48.**

His fourth consecutive report of this emblem. **HIS REPEAT IS A MEASUREMENT.**

Rev 44 set the **spine's** apex to 0.284 because that is 0.358 of the ring's
diameter from the top and the photographed apex landmark reads 0.353. But the
photographed landmark is the row where the V's two arms **merge into one run** —
a property of the **outline** — and the strokes have width, so they merge well
*above* the spine's apex. Setting a spine constant to an outline measurement put
the built merge at 0.251 against 0.343. **This is 10.110.8 exactly.**

Landmarks are run-count transitions, registered on the ring's own top and bottom
edge rows so a crop margin cannot move them:

| landmark | photo | rev 45 | rev 46 |
|---|---|---|---|
| L1 V arms clear the ring band | 0.1940 | 0.1455 | 0.1745 |
| L2 V apex / the central knot | 0.3433 | 0.2509 | 0.3418 |
| L3 W outer arms leave the band | 0.4776 | 0.5018 | 0.4764 |
| L4 W troughs reach the lower band | 0.8060 | 0.8509 | 0.8073 |
| L5 V arm separation / ring width | 0.2361 | 0.2248 | 0.2625 |
| L6 V arm stroke / ring width | 0.1528 | 0.1514 | 0.1417 |
| **residual** | — | **0.1167** | **0.0347** |

**L5 and L6 are why the angles became touchable.** Rev 45 refused to move any
angle because de-foreshortening a three-quarter view of a circle needs the
ring's axis ratio and the two fits disagree by 10 %. That refusal was right *for
rev 44's number*, which divides a **horizontal** arm separation by the ring's
**vertical** diameter. **A horizontal divided by a horizontal at the same row is
invariant to rotation about a vertical axis — the cosine cancels.** Same trick
as 10.107.2, on the other axis. This is rule 23.

**Three instrument errors, all caught by controls, all mine:** L4 landed on a
threshold-transient and is the **last** 3-run row, not the first; registration
was moved 0.088 by a two-pixel speck and is now the ring's own first and last
non-empty row; and the solver's own console figure (0.0262) is **not quotable**
because it reads a scene it has already built in — the clean number is 0.0347.

**A hypothesis refuted rather than acted on.** Beside the photograph the built
strokes *looked* too thick. Measured at the same structural row: photograph
0.1528 ± 0.002, built 0.1514. **The stroke width was right**; the impression
came from squashing a circular raster to the photograph's elliptical aspect.
*(This illusion has now occurred three times. See 10.121.)*

### 10.120  rev 46/47 — W3, THE SCRIPT WAS BLURRED, AND THE BLUR WAS ARITHMETIC

**Cited in `script_gen.py` since rev 46; recovered here at rev 48.**

Three revisions chased an **amplitude** metric for a **spatial-frequency** fault.

`Canvas` draws at `SS = 12`. `Canvas.alpha()` box-downsamples that to mask
space — **271 px of ink** — and `main()` then LANCZOS-magnifies those 271 px to
`OUT_W = 4096`. **The shipped 4096-px texture carried exactly as much real
information as the JPEG crop it was traced from, and not one bit more**: the
script in `ref_side.jpg` is also 271 px wide.

The fix, in three steps: add `Canvas.alpha_box(k)`; keep `alpha()` *as*
`alpha_box(SS)` so the existing `_ref_mask()` equality guard stays
bit-identical; and have `main()` crop the **drawn** raster before resizing,
3252 px → 4096. A 15.11× upscale becomes 1.260×.

| | rev 46 | rev 47 |
|---|---|---|
| 10–90 % alpha edge width | 14.077 px | **0.941 px** |
| mean stroke width | 152.37 px | 151.21 px |
| **edge / stroke** | **0.0924** | **0.0062** |
| soft fraction | 0.2154 | 0.0160 |

**MASK SPACE IS BIT-IDENTICAL** — `build()` `4a6f4e8cd0489fa1`, `senor_only()`
`82d6cf56dd660b47`, before and after. No mask-space figure in this project moved.

**THE CEILING, STATED.** 0.941 px is **at the instrument's floor** — an ideal
antialiased edge measures **1.000 px** on the same estimator. The correct claim
is that the residual blur is **≤ ~1 px and not resolvable by this instrument**.
**Nobody may quote 0.0062 as an accuracy.**

**The contrast half is NOT closed** and retires itself when W6 lands: *Señor* is
legible with its tilde in both photographs and is still a formless blob in the
build. `TARNISH_K`'s declared departure is 0.064, and the residue is the ground
being 11 % too bright, not the ink.

### 10.121  rev 47 — THE RESOLUTION BIAS, AND THE THIRD TIME IT FOOLED SOMEBODY

**Cited in `script_gen.py` since rev 47; recovered here at rev 48.**

With the blur gone the strokes *look* bloated beside the photograph. Measured at
4096 px they are 0.84× the photograph: **7.9 σ**, a publishable-looking defect.

**It is not there.** `probe_rev47_sharp` C7 shows the EDT stroke estimator
carries a **16.6 % resolution bias** across that 15× gap. At the photograph's
own 271 px: **built 0.04317 vs photo 0.04414 ± 0.00090 — 1.1 σ, agreement.**

This is the same illusion 10.119 records about the VW glyph's strokes, and the
same one 10.118's retraction records about the type centroid. **Three times, in
three different quantities, always the same shape: a real estimator compared
across two resolutions.** Expect a fourth.

**The two defences, and they are cheap:**

* **CALIBRATE AGAINST A KNOWN ANSWER AT THE REAL DATA'S RESOLUTION** (rule 22).
* **QUOTE THE RATIO, NOT THE READING** (rule 24) — photographed ÷ built, on the
  identical instrument at the identical scale, so the bias divides out.

**And a harness that broke its own estimator's validity regime.** The first
calibration drew 60-px bars blurred to σ = 20. At that σ the alpha at a bar's
**centre** is 0.866 — it never reaches 0.9 — so the whole bar counted as "band"
and the estimator over-reported by 26 %, then 44 %. **The synthetic violated the
estimator's regime (edge ≪ stroke); the estimator did not fail.** The harness
was fixed, the thresholds were **not** loosened, and C6 now watches the break
happen. This is 10.116.6 and rule 19.
---

### 10.122  rev 48 — TWO JOBS, AND ONE OF THEM WAS ALREADY DONE

#### 10.122.1  THE MODEL HAS HAD REAR VENT LOUVRES ALL ALONG

`LEDGER_rev46.md` §5 recorded a "NEW FINDING — THE MODEL HAS NO REAR VENTS",
`LEDGER_rev47.md` §10c repeated that "nothing replaced them", and
`NEXT_CONTEXT_PROMPT_rev48.md` made building them JOB 2, "geometry the model
does not have at all". **All three are false, and false against the BUILD:**

```
    louvres1 / louvres-1   560 v each   x -1.5371..-1.2419  (len 0.2952)
                                        z  0.8636.. 1.0699
                                        TEN slot rows, pitch 21.111 mm
```

watched print from a `T1_SUB=2` build. `t1_detail.louvres()` has swept 10
pressed louvres per flank, 20 in all, since rev 16.

**The grep those three documents cite as returning "nothing else" returns 140
hits**, among them `t1_detail.py:2122  # ===== REAR-QUARTER AIR LOUVRES`,
`t1_detail.py:2153  def louvres(nx=13)`, and `build.py:761  rear-quarter
louvres (10 per side)`. The grep was never run, or was run and misread.

**How it propagated, and this is the part worth keeping.** Rev 46 was right to
retire the painted bunting from the decal — the owner said the lines were vent
slats and he was right. But the painted lines sat **between the roof and the
burst**; the real louvres are on the quarter panel **half a metre lower**. Rev
46 concluded from retiring the paint that the geometry was absent, and then
**wrote that conclusion into `cal_gen.py:339` as a source comment**, where
every later context read it as machine truth. Rule 1 in reverse: a claim in
prose is not a guard, and a claim in a *source* comment is not a measurement.
Guarded now — see `verify_clone.sh`, "rear louvres are BUILT geometry".

**The count is CONFIRMED, not inherited.** 10 slats on `IMG_2073.jpeg` (rows
468–582, cols 1156–1188, de-sheared s = −0.180), pitch **8.106 ± 0.023 px**,
gap scatter 2.3 %. That confirms rev 47's 8.02 ± 0.42 and tightens it ~18×.
It is measured on the GREEN vehicle, which is admissible **because it is
geometry** — see 10.122.5.

#### 10.122.2  WHAT IS ACTUALLY WRONG WITH THEM IS THAT THEY DO NOT READ

`probe_rev48_louv.py`, 11 checked 0 FAILED. The built block is bounded **by
projection** through `studio.views()["side"]`, parsed out of `studio.py` at run
time together with `t1_detail`'s own `LOUV_*` — nothing transcribed (rule 2).
C6 lands the ground plane on the frame's last non-white row; C7 lands
`X_TAIL` on the silhouette.

```
    ref_side.jpg   signed modulation  -0.0383   |amp| 0.2059
    the render     signed modulation  +0.0343   |amp| 0.1112
    RATIO   |photographed| / |built|   1.85x
```

**THE RATIO BOUNDS PROMINENCE, NOT DEPTH**, and the probe prints that ceiling
beside it every run. See 10.122.3.

#### 10.122.3  THREE INSTRUMENTS BUILT, WATCHED FAIL, AND THROWN AWAY

10.116.6 says an instrument that has never been wrong has never been tested.
Rev 48 tested three and all three were wrong.

* **An automatic periodicity bounder** reported the built block at power 0.958
  and looked authoritative. Blank painted panel reads up to **0.380**; the
  block itself **0.405**. **Not separable.** It had locked onto the belt line.
  Deleted, not re-thresholded: lowering the threshold would have made a blind
  estimator quiet rather than making it see.
* **A silhouette anchor for the projection.** "The rightmost non-white pixel"
  over z 0.81–1.10 gives 1315 — **22 mm past the body's own rearmost vertex**,
  because the TAIL LAMP protrudes. Moved up to z 1.20–1.50 it gives 1396,
  because the SERVING COUNTER SHELF is there. Both plausible, both wrong.
  Replaced by the camera dict, which has no such failure mode.
* **A finding, retracted in the revision that found it** (rule 15). An earlier
  draft concluded that the signs disagree *because* `LOUV_OFF = +0.0020` rides
  the sweep proud, and would have had rev 49 recess it.
  **`ref_nolita_front34.jpg` shows these same real louvres reading BRIGHT.**
  Sign follows the key light, not the pressing. One lighting against another is
  not a comparison of geometry (10.110.8).

**The lighting-independent item, and it is still open.** `t1_detail.louvres()`
is *"A sweep, not a boolean … the shell is never touched"* — the built louvres
are **closed ribs laid on an unbroken flank**, where a T1 louvre is an
**aperture**. That is the fidelity bar `bus_model_ref.JPG` sets, whose own nose
louvres are modelled slots that self-shadow. Guarded as C10.

#### 10.122.3b  AND THEN REV 48 FIXED IT — THE LOUVRES ARE APERTURES NOW

The lighting-independent half of §10.122.2, closed in the same revision that
found it. `t1_detail.louvres()` was *"A sweep, not a boolean … the shell is
never touched"*: twenty **closed ribs laid on unbroken metal**, where a T1
louvre is an **opening**. That is the bar `bus_model_ref.JPG` sets — its own
nose louvres are modelled slots that self-shadow.

**ONE HOLE PER FLANK, NOT TWENTY**, on two measured grounds. `t1_core.py:230`
records `gap_englid` as the model's most fragile boolean and thin cutters are
what make a boolean fragile; and `build.CUTTER_VOL_MIN` is 1.0e-4 m³, which a
single 7 mm slot would sit *on* — twenty times over. The block aperture is
1.79e-2 m³, two orders clear. The blades span the hole; the gaps between them
are the slots.

**THE SIGN MOVED, AND THE SIGN IS THE POINT.**

```
    photographed   -0.0383     the slats self-shadow
    before         +0.0343     the ribs caught the key
    after          -0.2559     the slots self-shadow
```

**AND THE FIRST CUT WAS VISIBLY WRONG WHILE EVERY NUMBER SAID IT HAD WORKED.**
The signed modulation went the right way at the first attempt (+0.0343 →
−0.0287) and `VERIFY` was clean. The **render** came back with **bright white
bars among the slots** — `cabin_fill()` shining out through the new holes, and
in places straight through to the far flank. Behind a T1's rear-quarter
louvres is the **engine bay**: shallow, unlit, boxed off. `louvre_backing()`
puts it back. **Rule 28, on a change made in the same revision that wrote
rule 28.**

**A CONSTANT THAT COULD NOT BE WRONG UNTIL THE SHELL WAS CUT.** The authored
section was **11.0 mm**. The measured pitch is 21.11 mm and the header records
the slot aperture as **~7 mm (INFERRED**, 1.5 px, below `ref_side.jpg`'s
resolution**)**. Those require a **14.1 mm** blade; 11.0 mm leaves a 10.1 mm
slot, 44 % wider than the inferred aperture. **It never showed, because the
"slot" was solid metal** — the number could be wrong without anything being
visibly wrong. `LOUV_SECT = LOUV_PITCH − LOUV_APERTURE`, derived (rule 2).

**THE AMPLITUDE IS A CEILING, NOT A TARGET.** Built |amp| 0.385 against a
photographed 0.206. The photographed block sits in the serving counter's
**shade**; the rendered one is in open key. One lighting against another
(§10.110.8). **Do not tune the pressing depth from it.** A raking-light frame
of six slats settles depth directly — `PHOTOS_WANTED_rev48` item 3.

**AND C7 WAS RESTATED TWICE BEFORE IT WAS TRUE.** "The rightmost non-white
pixel is the tail cap" is false on this vehicle: at z 0.95–1.05 it finds the
**open trunk lid** (1365), at z 1.20–1.30 the **counter shelf** (1396), at
z 0.81–1.10 the **tail lamp** (1315). Hunting for a clean band was the wrong
response — the assumption was wrong, not the window. It now asserts the
invariant that *is* true: things may stick out past the tail, but nothing
forward of the tail cap can be the silhouette's aft edge.

#### 10.122.4  THE TRUNK LID WAS NEVER A SEAM — IT WAS ALREADY A FREE PANEL

> *"we're going to need the trunk open like it's in service"*

Confirmed against the build before anything was written, which is what §9's
sign-props trap demands. Connected-component analysis of `T1_body` from a real
`T1_SUB=2` build gives **six** components, one of them

```
    7982 v   x -1.873..-1.870   y -0.467..+0.467   z 0.608..1.103
```

— `gap_prism`'s outline (y ±0.470, z 0.6025..1.1025) to 3 mm. `build.py:69`
had already recorded the count going *"1 → 6 as each gap cutter frees a
panel"*. So this is **separate, name, hinge, back** — not a rebuild — and the
fragile `gap_englid` boolean is untouched.

**Why it swings AFTER the rake shear.** `_hinge()` rotates about a **fore-aft**
axis: it moves y and z and leaves x alone, which is exactly why a roof lid can
be swung before step 8b and still be sheared at its correct station. A tail lid
hinges **laterally** and does move x. Swung first, step 8b would shear it at
the wrong station and tilt the open lid by the rake angle for nothing.
`_hinge_y()` is the sibling; 8c runs after the shear.

**`TRUNK_OPEN_DEG = 52.0` IS A POSE CHOICE AND SAYS SO.** No frame in this
project shows this lid open. **SPEC 10.26's row "trunk lid | OPEN, at the tail
| `ref_side.jpg`" is REFUTED**: that raised panel is a thin board seen nearly
edge-on, cream-faced, with a RED border and **a string of amber bulbs along its
lower edge**, based at the **roof line** and not the engine deck.
`LEDGER_rev47.md` §5 was right that no frame shows the trunk open. So the angle
carries **NOT MEASURED** in its own comment and `verify_clone` requires that
declaration to stay — the `LINE_GAP` lesson applied *before* the defect instead
of after it. No strut and no counterbalance is built: an invented one would be
a claim.

#### 10.122.5  THERE ARE TWO VEHICLES, AND THE OWNER HAS RULED ON THEM

The reference set holds **two** Señor Tacombi T1s, and no document before rev 48
said so where it mattered:

| | body G/R | raised lid carries |
|---|---|---|
| `ref_side.jpg` **RED** | 0.204 | flower mural + yellow menu strips |
| `ref_rear34.jpg` **RED** | 0.269 | the mural board, plus the "La Santa" cream + red-script board — **two boards, not two faces of one** (see below) |
| `IMG_2073.jpeg` **GREEN** | 1.378 | tufted damask panel, ornate green frame, bulbs |
| `ref_workshop.jpg` **GREEN** | 1.304 | plain cream — mid-conversion |

> **RETRACTION, within rev 48, caught by rev 48's own adversarial verifier.**
> The row above first read *"mural outer / cream + red script inner"* — which
> describes the "La Santa" board as the **inner face of the raised lid**. That
> is precisely the §10.19/§10.26 identification the owner retired in §10.28
> (*"I was wrong, I think it is a detached sign"*) and re-retired in §10.49.
> **§10.49 exists because §10.38 re-adopted it once already; this was the
> third re-adoption, and it was mine.** It is also not what the pixels show:
> at 2× the cream board and the mural board sit on visibly different planes
> with the roof aperture's maroon interior between them. Corrected above.
> **A retired identification that keeps coming back unnamed is the same
> failure mode as a feature that comes back halfway (§10.122.1), and it now
> has three instances.**

A G/R of 0.20 against 1.38 is not a white-balance artefact. **HIS RULING,
rev 48, verbatim in substance:**

* **the RED bus is the vehicle being recreated** — which is what the model is
  already built as, and where W6's photographed target 0.223 ± 0.066 came from;
* **"the geometry appears the same"**, so geometry may be measured from either;
* **paint and artwork may NOT be transferred from the green frames.**

**That ruling has teeth.** The louvre count above is geometry and stands. But
`LINE_GAP` was re-based at rev 47b from the **green** bus's decal in
`IMG_2073.jpeg` — that is **artwork**. It must be re-based onto the red bus's
own decal or explicitly declared as transferred.

**And it dissolves W5 rather than answering it.** The brief says of the raised
sign board: *"The build paints a flower mural with menu strips; every frame
shows a hand-chalked blackboard."* **`ref_side.jpg` — the frame `lid_gen.py` §A
measured the mural from at rev 11 — shows the flower mural with yellow menu
strips, exactly as built.** No frame in the repo shows a chalked blackboard on
the vehicle's own raised lid; the chalked board in `IMG_2073.jpeg` is on a post
beside the bus, as the brief itself says. W5 was never a defect.

#### 10.122.6  THE FOUR SECTIONS THAT WERE CITED FOR TWO REVISIONS AND DID NOT EXIST

`LEDGER_rev46.md` §7 recorded "SPEC sections 10.118 (W1), 10.119 (W2), 10.120
(W3) **written into the sources**". That wording reads as "written into SPEC"
and was not. Until rev 48, `SPEC.md` stopped at **10.117**, while `cal_gen.py`,
`t1_core.py` and `script_gen.py` cited 10.118–10.121 as though they were here.
The brief's own opening line sends the next context to `SPEC.md` for everything
it needs to be correct. **Recovered above from the ledgers, at rev 48.**

Also discharged here rather than in a ledger: `bootstrap.sh`'s header said the
`pip install bpy==4.5.3` branch had **NEVER BEEN EXERCISED** while the rev-48
brief claimed it was discharged at rev 47. It has now run on a cold container
and returned ALL 10 PASS, watched print — and the header now says so.


---

### 10.123  rev 49 — THE TAIL BOARD, A BAY WITH NO MATERIAL, AND A TRADE THAT DID NOT EXIST

#### 10.123.1  THE TAIL BOARD IS ON THE VEHICLE — AND THE RETIREMENT WAS ABOUT A DIFFERENT SIGN

The rev-49 brief's job 1 was to build a raised board at the tail. This revision
**refused it**, on the ground that §10.28 records the owner retiring that panel
— and **the refusal was wrong, and he corrected it**:

> *"That was referring to a different sign. This one is part of the vehicle."*

He is right, and `ref_rear34.jpg` shows why in one frame. **There are two boards
in it.**

| | what it is | where it stands |
|---|---|---|
| **"La Santa"** | cream, **red brush script**, red star | on the **GROUND, BEHIND** the bus — retired 2026-08-10, §10.28 / §10.49 / §10.122.5. This is `signboard()`. |
| **the tail board** | cream face, **red rim**, amber bulbs, tilted 38° | **ON the vehicle**, based on the drip rail at the tail |

`signboard().__doc__` was written from a 3× crop of the **first**. Every later
document read "the raised panel at the tail is retired" and applied it to the
**second**. **A retirement inherits the object it was made about, not the
station it was seen at.**

**THREE PIECES OF PHYSICAL EVIDENCE, not another inference.** §10.28 requires a
photograph of the board's *footing* before this is revisited, and the owner
cannot supply one. He does not need to:

1. the board's base sits **on the drip rail** — 1 px from the project's own
   locked drip-rail fit (predicted v = 293.2 at that column; measured 292–294);
2. its bulb string is **continuous with the drip-rail bulb run**, at a pitch
   (28 ± 2 mm) statistically indistinguishable from the vehicle's own
   `BULB_PITCH` 28.6 ± 1.0 mm — **one circuit**;
3. a **power cable descends from it into the body**.

A sign standing on the ground behind the bus shares no circuit with the bus and
hangs no cable into it.

**AND IT IS NOT THE ENGINE LID, refuted twice.** Rev 48 measured the base at
1.747 ± 0.027 m against `ENGLID_GAP`'s 0.6025–1.1025 — ~11 σ. Stronger, and
new at rev 49: the engine lid is **top-hinged at z 1.103 over a 0.50 m panel**,
so **no opening angle whatever** lifts any part of it above **z 1.60**; the
board's tip is at **2.184**. Unreachable. The engine-lid band is also directly
visible in `ref_side.jpg`, **closed**, red, carrying the yellow swirl.

#### 10.123.2  WHAT WAS MEASURED, AND THE ONE THING THAT CANNOT BE

Measured on `ref_side.jpg` (**RED** — rule 26) through the project's own scale
chain (§10.35's `X(u)` map + `LOFT_GROUND_rev15` §0.4's `k_t`), C0-checked at
`X(242.84) = +1.3000`, `X(749.38) = −1.1000`, `X(922.2) = X_TAIL`. Uncertainties
are Monte-Carlo over endpoint jitter, `k_t` 215.5 ± 3.0 and the datum ± 0.020.

| quantity | value | ceiling |
|---|---|---|
| base station | `X_TAIL + 0.151` ± 0.022 | the map is the **near-flank** plane; re-seated at the centreline the sign flips |
| base height | **1.747 ± 0.027 m** | tightens the brief's 1.78 ± 0.07 by 2.6× |
| tilt | **38.0 ± 2.3° from HORIZONTAL** | **say which datum** — from vertical it is 52.0°, and a bare "39°" does not |
| chord | **0.711 ± 0.028 m** | the *image-plane* chord is 0.745; one px/m over-reads by 4.8 % |
| tip | `X_TAIL − 0.408` ± 0.017, z **2.184 ± 0.030** | the frame's right edge is at −0.441; a read of "0.5" saturates against it |
| bulbs | pitch 28 ± 2 mm | **only 6 resolve**; an FFT finds no 6-px component. The **count is DERIVED**, never observed |
| stay | ONE, endpoints measured, 78° | dia 9 ± 7 mm — **rod vs wire NOT RESOLVED**, it is the blur floor |

**THE WIDTH ACROSS THE VEHICLE IS NOT MEASURED AND IS NOT MEASURABLE FROM
ANYTHING WE HOLD.** The board's plane contains the lateral direction, so its
width projects **only through parallax** — 33.5 px per metre, and, being a cross
product, **identical at base and tip, so the projected width cannot taper**. The
observed silhouette *does* taper (19.9 px at the base, 7.2 over the last 40
columns), so the thickness also carries the board's own material and its rim
band, and the two cannot be separated at 1024 px.

> **§10.123.2a — THE 80 mm FOOT INCONSISTENCY IS WITHDRAWN, rev 49d.** It was never a conflict
> between the photograph and the geometry: **the board was at the wrong station.** The rear roof
> corner falls away fast — the skin reads **1.9608** at x −1.6982, **1.8607** at −1.800, **1.7497**
> at −1.850 and **1.6696** at `X_TAIL` — and exactly one station satisfies both the photographed base
> height and the roof's own surface: photographed **1.747 ± 0.027** against a skin at **1.7497**,
> **2.7 mm**, with the chord then landing the tip at **2.2001** against a measured
> **2.184 ± 0.030**, **16 mm**. Two independent heights close. The station is now solved from
> `T1_body`'s own vertices at run time.
>
> **AND THE GUARD REV 49b WROTE FOR THIS WAS A TAUTOLOGY**, caught by the rev-49 photorealism survey:
> `z0 = ZT_ALL − rake_drop + 0.005` against `_crown = ZT_ALL − rake_drop` differ by +0.005 **by
> construction**, so it could not fire in the shipped path and was only ever testing its own escape
> hatch. **Rule 20, on a guard written in the revision that quoted rule 20.** `ZT_ALL` is also not the
> crown — it is the **roll start**, 93 mm low here, which is why the foot sat **97.1 mm inside the
> roof**. The replacement measures the **built board** against the **built skin** and caught a further
> **3.7 mm** on its first run (`solid_prism` extrudes centred; the standoff is now derived from the
> section rather than typed).
>
> **What remains is one quantity, not two:** the fore-aft **depth plane**. The solved station sits
> 128 mm aft of the near-flank silhouette read, and the stay lands at **72.1°** against a measured
> **77.5°**. Same ambiguity as the width; same photograph closes both.

* **upper bound, admissible: W ≤ 0.59 m.**
* **lower bound: NONE.** 7 px of the tip half is fully accounted for by a 30 mm
  board plus a border.

That bound alone **refutes a full-width board**: the roof aperture is 1.11 m
across and the body 1.750 m, both excluded by more than 2×. `ref_rear34.jpg`
cannot close it — the candidate free edge **runs off the frame at u = 1199**,
and §10.48 admits px/m there only on the plate plane. `TB_WIDTH` and the lateral
centring are **POSE CHOICES and say so**.

**Both GREEN frames also carry a board at this station** — admissible as
*geometry* corroboration under the owner's ruling, and the record never said so.
**No figure and no colour was taken off either.**

#### 10.123.3  THE TRUNK BAY SHIPPED WITH NO MATERIAL, THROUGH EVERY GREEN CHECK

```
build.py:846   for ob, key in ASSIGN:            <- the loop that APPLIES materials
build.py:937   A(S.trunk_bay(log=log), "dark")   <- appends 91 lines AFTER it ran
build.py:939   log("materials: 165 objects")     <- counted trunk_bay in the 165
```

`A()` only **appends** to `ASSIGN`. Step 8c must run *after* step 9 because a
lateral hinge moves `v.co.x` and step 8b shears on `v.co.x` — so this is the
**only `A()` call in the file that lands after its own consumer**. The bay
rendered at Blender's default ~0.8-albedo grey: **1.28× the body red, 1.11× the
cream — the brightest thing on the tail**, where a T1's engine bay is a dark
cavity. After: **0.51×**.

**`VERIFY: 0 fail, 0 warn`. `verify_clone` ALL 110 PASS.** And the one line that
could have reported it printed `len(ASSIGN)` — **appends, not assignments** — so
it asserted coverage instead of measuring it. **Rule 27 inverted: a count that
logs the wrong quantity reads as coverage too.** Rule 28 found it: one rear-3/4
render, one crop.

This is the **same defect rev 48 fixed for the louvre apertures** — light where
a dark bay belongs — **in the same revision**. It was missed here only because
no rev-48 frame showed the tail.

Guarded against the **cause**, not the instance, and watched fail:

```
AssertionError: objects were given a material key but never assigned one: trunk_bay
  -- an A() call landed AFTER step 9's ASSIGN loop (build.py:846)
```

#### 10.123.4  `_bounds()` EXCLUDED NON-BODYWORK BY THE SHAPE ITS OWN DOCSTRING ARGUES AGAINST

`verify._bounds()` argues at length that excluding parts by an **enumerated
list** is wrong because "a list goes stale the moment somebody hangs a new part
on a lid" — and then excluded the counter by a **hard-coded tuple**. It went
stale the moment the tail board was hung: **length red at +370 mm on sheet metal
that had not moved.** Rule 5: the rationale was sound and the shape contradicted
it. Parts now register in **`t1_shell.NOT_BODYWORK`**, and every drop is
**printed by name every run** (rule 27):

```
bounds EXCLUDE 9 non-bodywork part(s): counter, counter_nosing, counter_top,
  tail_board, tail_board_stay, tb_bulbflex, tb_bulbs, tb_edge_dark, tb_edge_red
length excludes opened lids: 4.480 with them, 4.056 without   (spec 4.055)
```

#### 10.123.5  W6 — THE TRADE DID NOT EXIST, AND THE LEVER IS NOT WHAT THE RECORD SAYS

**The owner has been asked for three revisions to choose between accurate paint
and a catalogue-clean white background. THERE IS NO SUCH TRADE.** The white
background is a **compositor constant** laid under a keyed render
(`composite_on_white`, an unconditional `AlphaOver` on `bg_white_level()`), then
renormalised to 252 DN by `post.py`. Measured, base against `T1_CYCALB=0.30`:

```
background mean 255.000 -> 255.000      %at255 100.00 -> 100.00
max | difference |  =  0.000
```

**Nothing done to the lights can reach it.** And the owner **retired the
pure-white backdrop lock himself at rev 15** — SPEC §6 carries "composited to
pure white" *struck through*, marked *"RETIRED, §10.69 — THE OWNER'S DECISION"*.
Three revisions have since refused lighting changes by citing it as live.

**THE SWEEP** — `probe_rev45_paint.py`, 4 controls including its kill, 0 FAILED
on every run:

| lever | P1 body red G/R | verdict |
|---|---|---|
| base (rev-48 rig) | **0.455** (3.5 σ) | — |
| `T1_CYCALB` 0.76 → 0.30 | ~0.45 (−2…5 %) | **DEAD** |
| bigger softbox, **short axis** 3.5× area | **0.452** (−0.7 %) | **DEAD** |
| `T1_SPEC = 0` | 0.347 | works — **but rev 8 made this fix and reverted it** |
| sources 3.5× on **both** axes (12× area) | 0.351 (1.9 σ) | works — see below |
| photographed target | 0.223 ± 0.066 | albedo is already right at 0.250 |

**The short-axis row is the one that matters.** Growing the source 3.5× in the
axis that *sets the streak* — literally "use a bigger softbox" — moves the red
by **0.003**. So the gain in the both-axes row is **not the specular being
softened**; it is the sources growing past the subject (a 56 m strip) until the
rig stops being directional and becomes an **enveloping diffuse dome**.

**`T1_SOFTEN` does not tune the studio. It progressively REPLACES it** — which
is also why it works, since an overcast or shaded outdoor light *is* a dome and
every reference frame was taken under one. It also drops the cream to 0.706 of
base and the red flank to 0.545; the published G/R is normalised to the cream in
the same frame and so is exposure-invariant, but the *picture* changes
brightness too. **Default 1.0. Nothing ships changed. `P1 = 0.455` at k = 1.0
reproduces rev 48 exactly, watched print.**

**`LEDGER_rev45`'s "about half the excess is the specular response to the white
cyclorama and its 0.76-albedo floor" is REFUTED.** It attributes an
un-decomposed lever (`T1_SPEC`, which kills the paint's specular response to
*every* white source) to the smallest of its four possible causes. `studio.py`'s
"the floor … the single largest desaturator in the scene" appears **once in the
whole repository — in that comment** — and cites a §10.9 that contains no such
arm. Rule 1.

#### 10.123.6  RETRACTIONS THAT HAD LANDED IN A LEDGER AND NOT IN THE SOURCE

*A retraction that lands in a ledger and not in the source is half a retraction.*

* **`cal_gen.py:385` still said "the model has NO REAR VENTS"** — **rule 1's own
  founding case**, standing unannotated two revisions after rev 48 cut real
  apertures. Annotated.
* **`cal_gen.py`'s three "DARK GREY" slat readings**, retracted at rev 47 into
  `verify_clone.sh` only. Annotated.
* **`verify.py` called the ~3.0 m bbox top "the raised signboard" in two
  places.** It is **`lid_main`** (zh 2.006 + `LID_W`·sin 104° − `RIDE_DROP` =
  3.018, which is `STATE.md`'s own 3.017). `signboard()` has been gated off
  since rev 12. A retired object's name living on in a live comment on the
  height row for 37 revisions. Corrected.
* **§10.26's table** still published `| trunk lid | OPEN, at the tail |`.
  Annotated above — the fourth instance of the failure §10.122.5 names.

#### 10.123.7  THE OWNER SHUT THE LOWER BAY — AND IT EXPOSED A LATENT REV-48 DEFECT

> *"Leave the lower bay shut, just have the back trunk window open for service."*

**This refutes an INFERENCE rev 48 made and shipped.** Asked at rev 48 which of
the two rear apertures should be open — both marked by projection on a straight
rear view — he chose **A, the rear window**. Rev 48 then reasoned *"he called
the upper one the MAIN bay, not the ONLY one"*, kept the lower lid open as well,
and wrote that reading into §10.122.4 and into `t1_shell.py`. **A choice between
two things is not a licence to keep both.** Rule 6: an ordinal fact licenses a
SIGN, never a SHAPE.

`TRUNK_OPEN_DEG = 0.0` now means **SHUT**, and the swing is **skipped entirely
rather than run at zero** — `_swing_open()` asserts the free edge actually
travels, so calling it with 0.0 would fire a guard on a correctly closed lid. A
guard must fire on the defect, not on a legitimate pose. The panel is still
separated and named; the shut line already existed as `gap_englid`, so a closed
free panel is geometrically identical to the un-separated body and keeps
re-opening one constant away. The T-handle and the 1963 plate are **no longer
carried and no longer join `SWUNG`** — they have not moved, and registering them
would exclude two parts that *are* inside the closed envelope from the vehicle's
own length. That is rule 18, the mirror image of rev 48's stale-`bound_box`
defect. Length returns to **4.065**, the baseline `verify_clone` locks.

**AND CLOSING THE LID EXPOSED A DEFECT THAT HAD BEEN INVISIBLE FOR A REVISION.**

```
lid_trunk   x -1.8730 .. -1.8702      the shut lid's outer face, at X_TAIL
trunk_bay   x -1.8750 .. -1.4550      the lining's face, 2.0 mm AFT of it
```

`trunk_bay()` set its origin to `x_skin - 0.002 + BAY_DEPTH*0.5`. `solid_prism`
extrudes ±depth/2 about its origin, so the aft face landed at `x_skin − 0.002`
— **2 mm PROUD of the tail skin, not 2 mm inside it. The sign of the inset was
inverted.** The comment above it explains, correctly, why the origin is advanced
by half the depth so that changing `BAY_DEPTH` cannot reopen rev 48's +210 mm
defect — and that reasoning is sound and does nothing whatever about the inset's
own sign, because **nothing measured the lining's face against the skin it
lines** (rule 16).

**It was invisible while the lid was open**: nothing stood in front of the
lining, so 2 mm poking past the tail read as the bay's own back wall. With the
lid shut it sat 2 mm *in front of* a closed panel and won the depth test across
the whole of it — **the tail rendered with a dark charcoal rectangle where the
red engine lid belongs.** `VERIFY: 0 fail, 0 warn`; `verify_clone` ALL 110 PASS.
One crop showed it. Rule 28.

Fixed, expressed as a named positive inset, and guarded against the **cause** —
the lining must lie entirely inboard of the skin whatever `BAY_DEPTH` or the
inset do — and **watched fail** on `T1_BAYPROUD=1`:

```
AssertionError: trunk bay lining is PROUD of the tail skin: its aft face is at
x -1.8750 against a skin at x -1.8730 (2.0 mm outside).  With the lid shut this
renders THROUGH the closed panel.
```

Measured, same window, before and after: the lid panel reads **RGB 91.1/75.4/66.7
→ 106.5/72.4/61.8** — from the bay's neutral grey bleeding through, to body red.

**The bay lining is KEPT although it is now unseen**, because the compartment is
real and reopening the lid is one constant away. The build says so every run.
