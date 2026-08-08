# TACOMBI COMBI — LOCKED BUILD SPECIFICATION  (rev 3)
**Status: AUTHORITATIVE.** Nothing in the build may contradict this file.
Change this file *first*, log it, then change code. `verify.py` asserts the
machine-checkable rows on every build.

**Working method (standing):** ground in the reference → build → *adversarial*
audit against the reference → iterate. Never build before grounding; never
call it done off self-review.

---

## 0. Subject — grounded

The **Playa del Carmen combi**: a **1963 Volkswagen Type 2 (T1) Kombi**, bought
in Mexico City, driven through the Yucatán and converted into a taco stand.
Engine scrapped, transmission sold, seats replaced with cooking equipment.
**This is the Playa bus, NOT the Nolita one.**

Grounding sources: user reference photograph (primary), Tacombi's own company
history, VW T1 factory dimensions, prior project context.

### 0.1 Retired readings — regressions if they reappear
- open-bed single-cab pickup with drop-sides, corner posts or a canopy
- gold side script — it is **silver**
- "Estilo Tacombi" — it reads **"Señor Tacombi"**
- plain font capital T — it is an **ornate swash**
- VW roundel upside down — **V above W**, always
- glazed side windows where there should be **open serving hatches**
- chrome hubcaps — they are **red domes with a white VW**
- flush indicator lenses — they **stand proud**
- bumpers carried high — they sit **low**

---

## 1. Body configuration — FROZEN

| Item | Value |
|---|---|
| Body | T1 **Kombi / Microbus van**, full height nose to tail |
| Roof | **intact** — folding canvas ragtop modelled **CLOSED**, panel + frame visible as a seam |
| Side, show side (+Y) | cab door glazing, then **THREE evenly sized, evenly spaced SERVING OPENINGS** (glass removed), then a **FOURTH window at the rear**, frosted, carrying a **"100% CALIDAD"** decal |
| Counter | **cantilevered timber plank counter** beneath the three serving openings, on brackets |
| Side, off side (−Y) | double cargo doors (panel gaps), glazed windows in the same bay positions |
| Cab door | front-hinged; front vent wing + main drop glass |
| Rear | rear window in the upper tail, engine lid below, rear bumper |
| Interior | **galley** — counter, plancha, shelving. Not passenger seats |

### 1.1 Serving-bay layout (show side, x in metres)
| Bay | Front edge | Rear edge | Treatment |
|---|---|---|---|
| 1 | +0.860 | +0.260 | open serving hatch |
| 2 | +0.150 | −0.450 | open serving hatch |
| 3 | −0.560 | −1.160 | open serving hatch |
| 4 | −1.270 | −1.870 | frosted glass, "100% CALIDAD" decal |

Band: sill **z = 1.402**, head **z = 1.798**, corner radius 0.055, pillars 0.11.

---

## 2. True-to-scale hard points — FROZEN

Frame: **+X forward, +Y left, +Z up, ground Z = 0**, metres.

| Dimension | Value |
|---|---|
| Overall length over bumpers | **4.280** |
| Overall width | **1.720** |
| Overall height | **1.940 ± 0.02** |
| Wheelbase | **2.400** (front axle +1.300, rear −1.100) |
| Track front / rear | 1.375 / 1.360 |
| Tyre 5.60x15 | dia **0.665** (R 0.3325), section 0.145 |
| Rim | R 0.1905 |
| Body max half-width | 0.860 |
| **Ride height** | **LOWERED. The Playa combi sits noticeably lower than stock — body dropped `RIDE_DROP` (65 mm) relative to the wheels. Wheels stay on the ground; arches stay concentric with the tyres.** |
| Roof edge / crown | 1.8935 / +0.032 |
| Belt line (two-tone break) | **z = 1.386** |
| Front / rear sheet metal | x = +2.108 / -2.108 |
| Bumper faces | x = +/-2.140 |

Tolerance **+/-25 mm** on L/W/H. **The front end has been flagged as wrong
before — front dimensions and front hardware get checked explicitly every
iteration.**

---

## 3. Livery — FROZEN

| Element | Specification |
|---|---|
| Upper body + roof | warm cream / off-white |
| Lower body | deep tomato red |
| Break | belt line z = 1.386, sweeping down across the nose into the T1 **V-swage**, apex (y 0, z ~ 0.872) rising to the belt at the corners |
| Folk art | **gold + yellow + white** Mexican folk-art florals over the **red only**. **Density graded** — dense bouquet on the nose flanks, trailing vine along the belt, sparse at the tail. Not uniform wallpaper |
| Side script | **"Señor Tacombi"**, **SILVER**, dark keyline, two-line lockup (small "Señor" raised over large "Tacombi"), capital **T an ornate swash** — arcing crossbar with curled terminals, S-curved stem, sweeping foot flourish |
| Rear-bay decal | **"100% CALIDAD"** on frosted glass, bay 4, **must be legible** |
| VW nose emblem | painted cream, **V above W**, not chrome |
| Wheels | **WHITEWALL tyres** + solid **RED domed hubcaps** carrying a **white VW logo** in the centre. Red steel rim behind. Chrome caps are a regression |
| Bright work | chrome bumpers, headlamp bezels, handles, mirrors, drip rails |
| Bumpers | sit **LOW** on this modified bus — bumper centreline straddles the wheel centre height, not up at the valance |
| Indicators | amber **bullet pods standing proud** of the nose above the headlamps, on a visible standoff base. Flush lenses are a regression |
| Finish | **clean restoration** — deep gloss show paint, crisp colour boundaries |

---

## 4. Mesh & texture quality bar

- Watertight, manifold body shell. No floating or intersecting artifacts.
- Crisp, regular quad topology on the shell; no n-gon pinching on the nose.
- Sharp colour boundaries (procedural, resolution-independent).
- Decals 3K-4K, non-overlapping, correctly oriented.

## 5. Render — FROZEN

Cycles CPU + OpenImageDenoise. White seamless studio, shadow-catcher composited
to pure white with a soft contact shadow (per the school-bus reference).
Large soft sources only. **Hero stills, not turntables.**
Final >= **2400 x 1600**, AgX.

Deliverables: 3/4 front-left hero (reference angle), 3/4 rear-left, 3/4
front-right, ortho side / front / rear, nose detail, low 3/4.

---

## 6. Regression guards (verify.py)

1. L / W / H outside section 2 tolerance -> FAIL
2. Wheelbase, track or tyre diameter off spec -> FAIL
3. Any object named `*bed*` `*gate*` `*canopy*` `*fascia*` `*post*` -> FAIL
4. Fewer than 3 open serving bays on +Y, or bay 4 not glazed -> FAIL
5. Missing materials: paint, cream, chrome, glass, **red wheel paint**,
   **silver script**, frosted decal -> FAIL
6. Body top below 1.90 anywhere aft of x = -1.60 -> FAIL
7. Non-manifold body shell -> FAIL

---

## Change log

| Date | Change |
|---|---|
| 2026-08-08 | Initial lock. Body corrected from single-cab pickup to Kombi van. |
| 2026-08-08 | Script text corrected to "Señor Tacombi"; capital T must be an ornate swash. |
| 2026-08-08 | Script colour corrected to **silver**. |
| 2026-08-08 | rev 3.2 — modified-bus details locked: whitewall tyres, red domed hubcaps with white VW, low bumpers, proud bullet indicators. |
| 2026-08-08 | rev 3.1 — bus is **lowered**: body dropped 65 mm relative to the wheels, arches kept concentric. Overall height = stock minus the drop. |
| 2026-08-08 | rev 3 — grounded against prior project context: this is the **Playa** bus with an **intact roof, three serving openings and a cantilevered plank counter**. Side bays specified. "100% CALIDAD" frosted rear bay added. Finish = clean restoration. Front end flagged as a repeat defect area. |
