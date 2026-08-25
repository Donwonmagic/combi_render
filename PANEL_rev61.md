# EXPERT PANEL — rev 61 scorecard

**Commissioned by the owner:** *"have an expert panel judge the result, specialists with
focus in 3d modeling, high resolution photography, hyper-realistic animation, etc, and have
them seriously judge every aspect of the bus and assign them point values."*

Three independent panellists, each given the SAME four frames and the SAME reference set,
each forbidden to run Blender, each required to paint every measurement window before
publishing a number. They did not see each other's reports.

**Frames judged:** `out/r61f_{front,side,hero,hero34r}.png` — 1600x1100, 96 spp, SUB=1,
rendered at the rev-61 state (V_POW 0.52, the restored `Señor`).

---

## THE SCORE: **83 / 240**

| panel | score | headline |
|---|---|---|
| **3D hard-surface modelling** | **34 / 80** | proportion is genuinely good (length/height to 0.3 %); the tail is a box where the real one is a barrel; every shut line is a 1-px ink stroke |
| **Look development / materials** | **28 / 80** | the paint CONSTANTS are right and the render is not; `lidmural.png` is a 4096 file carrying ~484 px of real detail |
| **High-resolution photography** | **21 / 80** | optics 1/10 and sensor character 2/10 — because `post.py` has never been run on any frame this project has judged |

### Per category

| # | modelling | | lookdev | | photography | |
|---|---|---|---|---|---|---|
| 1 | proportion & stance | **8** | body paint | **5** | gestalt | **3** |
| 2 | silhouette & continuity | **4** | weathering & wear | **3** | tonal / exposure | **4** |
| 3 | panel gaps & edges | **3** | chrome & bright metal | **3** | colour science | **5** |
| 4 | wheels, tyres, arches | **4** | glass & transparent | **2** | specular behaviour | **2** |
| 5 | glazing & reveals | **3** | rubber | **2** | optics | **1** |
| 6 | small parts & hardware | **3** | artwork & decals | **5** | sensor / film | **2** |
| 7 | the conversion | **4** | interior & galley | **4** | contact realism | **2** |
| 8 | topology / mesh | **5** | texture res & UV | **4** | micro-detail at 100 % | **2** |

**The single highest score on the page is proportion and stance, 8/10.** The geometry's
overall dimensions are not the problem. Everything below 5 is surface, material, optics and
the small parts.

---

## WHAT THE PANEL AGREED ON, INDEPENDENTLY

* **The VW roundel reads as an X.** All three said so unprompted, on the nose AND the four
  hubcaps. The owner's top item, confirmed for the sixth time.
* **The bulbs are unlit** — modelling and lookdev both. This corroborates F144.
* **The tyres are wrong** — no tread, no lettering, too light. Two panels, independently.
* **The glass is a flat slab** — 0.5 % sd against the photograph's 12.8 %, a 26x deficit.

## WHAT THEY DISPUTED — and these are the valuable ones

* **The photography panel DISPUTES F62's studio ceiling**, with numbers: the specular-event
  census is **0.024 % of red pixels against 7.07 %** in the FLATTEST-lit photograph we hold,
  and the render's own SIDE frame reaches a panel spread of 0.521 — inside the reference
  range — on the same shader that gives the hero 0.224. Its argument is that the deficit
  tracks camera/light geometry, not the surround. **Not adopted, but not dismissed: this
  needs testing before F62 is quoted again.**
* **It also disputes the ground-shadow ceiling**, noting a cyclorama floor cannot light a
  200 mm cavity — photographers have to ADD light under a car in a cyc, not subtract it.
* **The modelling panel measures the rear valance with the OPPOSITE SIGN** to the earlier
  body audit, and **DISPUTES the B-pillar claim** (it measures 77 mm, not 12 mm, and says
  the 12 mm figure is about the aperture REVEAL, not the pillar).

---

## ONE PANEL CLAIM I CHECKED AND CORRECTED

The lookdev panel called the restored `Señor` a **regression** — *"the bridging has fused the
letters into one continuous unbroken ribbon"*. **I verified that against the two textures and
it is overstated.** Before: the `S` is a C-shape plus a DETACHED curl. After: one connected
`S`. The `eñor` mass is **pixel-identical in both** — the bridge fused nothing beyond the `S`
it was written to fuse, which is what its guard asserts and what the guard measures.

**But the panel's INDEPENDENT finding stands and is the real defect.** Live on
`flank_compare.py`: the `Señor` region carries **979 px of ink against the reference's 1261
— 77.6 %**, at IoU **0.721** of its own measured ceiling. My bridge moved that by **1 px**.
So the deficit is letterform SIZE and WEIGHT across the whole word, not the `S`'s breaks, and
the owner's *"clearer than the photo, well defined"* is **not yet delivered**.

---

## THE RANKED PROGRAMME, MERGED FROM ALL THREE

Point gains are the panels' own estimates, on their own 80-point scales.

| # | work | from | est. gain |
|---|---|---|---|
| 1 | **Run `post.py` on every judged frame** — bloom, CA, vignette, grain are implemented, in the right order, and default to gain 0.0 (F146) | photo | **+4 to +6** |
| 2 | **Give the studio a key and a floor**, and re-test F62 rather than quoting it | photo | +7 to +10 *(contested)* |
| 3 | **Rebuild the tail as a barrel**; add the windscreen-header crease and the rear-panel seam | model | +3.0 |
| 4 | **Systematic edge pass** — real gap width + leading-edge chamfer on every shut line, arch lips, drip-rail section | model | +3.0 |
| 5 | **Rebuild the glass** — thickness, IOR, seal section, Fresnel; lamp lenses with reflectors | lookdev | +3.5 |
| 6 | **Tyres** — tread, sidewall lettering, bead, shoulder; darken to 0.18 of body white; strip the paint mottle off the rubber | lookdev | +3.0 |
| 7 | **Cut the cream's dust/mottle** to the measured 9.9 % blotch (it is at 26.6 % — 2.7x DIRTIER than the photograph, so it fails BOTH the WEATHERED lock and "like new") | lookdev | +3.0 |
| 8 | **Make the bright metal metal** — hubcap ring, brass bezels, and the mirror, which reads near-BLACK where a white studio demands near-white | lookdev | +3.0 |
| 9 | **Regenerate `lidmural`/`lidsign` at TRUE 4K** — 12 % effective resolution today | lookdev | +2.5 |
| 10 | **Glazing reveal** — 30-50 mm of modelled sheet thickness on every aperture | model | +2.5 |
| 11 | **The roundel** — separate V and W, flatten it (it is a glossy TORUS where the photograph is flat paint), ring down ~11 % | both | +2 to +3 |
| 12 | **Small parts** — tail lamps to tall ovals, mirror head/arm/base, 150 mm door pull, louvres to 9-10 slots at 25 mm pitch pressed into the flat panel | model | +2.0 |

**Modelling panel's own ceiling estimate if its eight land cleanly: ~51/80.** Past that it
says the surround is required, which the owner has ruled on.

---

## PROVENANCE, AND WHY THESE NUMBERS ARE WORTH SOMETHING

Between them the three panellists **painted and REJECTED at least fifteen measurement
windows** before publishing, and **retracted nine claims they had formed by eye** once they
measured them — including "the cream is too cool" (refuted: two of four references match the
render), "the mural is desaturated" (refuted: sat 0.777 vs 0.784), and "the folk art is
globally sparse" (refuted: 14.5 % vs 16.3 %). That is this project's own standard, applied by
outsiders, and it is why the surviving findings are worth acting on.
