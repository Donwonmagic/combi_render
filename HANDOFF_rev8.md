# HANDOFF — end of the rev 8 context

Read `STATE.md` first. It is machine-written by `audit.py` from the mesh built
in the same process, carries the git SHA and a dirty-tree flag, and **if it and
any prose disagree, it is right.**

---

## 0. Read this first, in this order

1. `/areas/tacombi-combi-sticker.md` and `/preferences.md` in **memory** —
   before any code. They were present and readable in this container and they
   caught a live regression within the first ten minutes (see §2). Two prior
   contexts skipped them. If you cannot read them, say so explicitly rather
   than quietly proceeding.
2. `STATE.md`
3. `SPEC.md` **§10 and §10.9** — §10.9 is rev 8 and supersedes §10 where they
   differ.
4. `SKEPTIC_PASS.md`
5. this file
6. `REF_MEASUREMENTS.md`

## 1. Reproduce the state

```bash
git clone tacombi_history_rev8.bundle tacombi     # HEAD should be the rev 8 tip
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
cd tacombi
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=2 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=1 /tmp/blender/blender -b --python audit.py
```

Expect at **both** levels: `0 fail, 1 warn`, the warn being
`roof @ rear axle 1.923 vs spec 1.960 (-37 mm)`, which is **deliberate and
logged** — see §3. Also: `TYRE_D=0.6650`, 3 open apertures, four shut lines
`100 % open`, band `1.372–1.775` un-dropped, bay widths `0.507 0.516 0.525`,
**132 meshes**, 0 non-manifold edges, `cutters rolled back: none`.

> 132, not rev 7's 147. The VW glyph went from six bars per emblem to two
> mitred prisms (−20 objects) and the canvas ragtop's three objects were
> replaced by eight lid objects. Do not "restore" the count.

This container had **2 cores / 8 GB**, not the 4 cores / 3.9 GB rev 7 assumed.
Fewer cores, more headroom. Re-time your render budget rather than inheriting
rev 7's numbers.

## 2. What rev 8 changed

**The stance is a line, not a scalar.** Step 8b shears:
`v.co.z -= (0.0365 + 0.0330 * v.co.x)`. Roof at the rear axle **1.871 → 1.923**
against §2.3's measured 1.960. `Z_BELT` is a line (`t1_mats.z_belt(x)`),
`verify.py`'s frame offset is a function of x, and `audit.py`'s height row is a
three-station roof-line check. Wheels are **excluded** from the shear — they are
circles on flat ground; shearing them would swing each hubcap glyph 1.9° off
vertical. Full detail and the derivation are in `SPEC.md` §10.9.

**Caught in passing, and it would have been a silent regression:** the rake
lifts the front arch 14.4 mm, which ate the cab-door shut-line clearance rev 7
had just fixed. The old 0.7800 bottom run would have sat 5.4 mm *below* the arch
lip — the exact condition that collapsed the shell 205562 v → 12 v at SUB=2 for
six revisions. Bottom run lifted to 0.8000–0.8160 and **the clearance is now
asserted at import** in `t1_shell`, not described in a comment.

**The canvas ragtop was still shipping.** `t1_shell.ragtop()` built a folding
canvas roof — five Gaussian bow sticks, a sailcloth sag term, a `canvas`
material and a Metallic-1.0 `chrome_dull` frame down the middle of a white roof.
`SPEC.md` §0.2 retired that reading **in rev 4**. It survived three revisions
because `verify.py` banned only the three retired materials somebody remembered
to type. Replaced with **rigid hinged steel lids, modelled OPEN** (Donald locked
OPEN on 2026-08-10; both in-service photographs show them up and no photograph
shows the vehicle closed).

The guard is now a reviewed map **plus a drift check on §0.2 itself**: if §0.2
gains a bullet, `verify` warns until someone reviews the map. My first attempt
scanned §0.2 for material names directly and **flagged six correct materials** —
every bullet is "retired reading — correction" and the names appear on both
sides. Do not re-try that approach.

**Flank saturation diagnosed.** Folk-art coverage and AgX Punchy are both
**refuted** with measurements (Punchy *adds* 0.127). The deficit is a 0.0592
achromatic specular term; SPEC's 0.816 is an **albedo** number no beauty pixel of
a dielectric under a white softbox can reach. Target restated in §10.9. Fresnel
corrected 0.21 → 0.50, sweep albedo 0.94 → 0.76, world 0.17 → 0.05, clamps
released, glass roughness 0.004 → 0.022, `capred` de-glossed, backdrop white
point keyed on the (transform, **look**) pair, 16-bit output.

**Folk-art density ran backwards** — measured, gold coverage is 0 % from X +1.47
to −0.40 and 36.9 % at the tail, against a model ramp that peaked at the nose.
Two measured lobes now.

**Art reproduction pass, scoped by Donald to four pieces.** Mural: done
(`lid_gen.py`) — nine heads, correct concentric-ring structure with the cream
lobe ring and peace centres, thick vermillion stems, gold almond leaves, dense
red+gold calligraphic tendrils, yellow frame all four sides with slab caps,
stars and painted food vignettes. Paisley: done (`folk_gen.py`) — the old tile
measured **0.0 % red and 0.0 % dark**; the real vocabulary is gold acanthus
scrolls + thin tendrils + orange/cream rosettes + **dark-brown dotted commas**,
all four now present, and the tile now maps once across the flank rather than
repeating 1.8×. **Script and Calidad: NOT DONE — see §3.**

**Also:** VW glyph rebuilt as two closed mitred prisms and `t1_detail.vw_logo`
now delegates to `t1_core.vw_bars` (two independent copies is why they drifted);
`brass` folded into `t1_mats.build_all()`; bulb string given an emissive
material; a **Playa del Carmen lighting rig** added (`studio.playa()`,
`studio.ground_playa()`, `T1_SCENE=playa`) with two eye-height cameras.

## 3. What is still wrong — measured, not guessed

**1. THE SCRIPT IS WRONG AND DONALD SAID SO.** Looking at `out/p9_hero34f.png`
he said, flatly, *"That script i see on the p9 hero is NOT it."* He is right and
I did not fix it before running out of room. This is the top of your list.

What the real lettering is, read off `ref_side.jpg` at 5× (crop
`(300,470)-(620,570)`): a fat, rounded, late-1960s psychedelic display script in
**silver**, not white and not gold. "Señor" small and raised to the upper left;
"Tacombi" large. The capital **T** carries a long sweeping ribbon swash that
runs back over "Señor". The **o, a, c and b have rolled SPIRAL counters** — an
actual spiral wound inside the bowl of each letter. Strong thick/thin contrast,
bulbous terminals, a slight dark keyline on some edges.

`sign_gen.py` already has `swash_T()`, `spiral()` and `counter_spirals()`, so
the machinery exists — what ships does not look like the photograph. Treat this
as a **letterform** job: either drive those primitives from traced control
points, or build the glyphs as explicit outlines. Do not accept a system font
with flourishes bolted on; that is what is there now and it is what he rejected.

**2. The Calidad decal is untouched by the art pass.** `cal_gen.py` draws a flat
red sunburst. The real one (crop `(735,295)-(860,390)`) is a spiky starburst
with a **red-orange → orange/yellow gradient**, white **bold italic** "100%"
over "Calidad" set at roughly −20°, and there are **two red bunting bars with
triangular pennants above it** that are not modelled at all.

**3. Roof at the rear axle is 37 mm short** (1.923 vs 1.960). The rake closed
52 mm of the original 89 mm gap; this is the residual, 1.2σ on §2.3's own
±30 mm band. Logged as a warn, not hidden.

**4. Rake versus the arch gap — a real contradiction, unresolved.**
`0.0330 × 2.400 = 79 mm`, so the front arch gap must be 79 mm less than the
rear. The rear measures ≈30 mm off `ref_side.jpg` and §2 locks 41 mm; either way
the front comes out **negative**. Held: arches follow their own wheel
(`t1_shell.arch_z(x)`), which keeps both measured numbers and produces no
impossible geometry. Resolving it needs a photograph with an **unoccluded front
wheel** — a man stands directly in front of it in `ref_side.jpg` and every
attempt to measure the front arch locked onto his red shirt.

**5. NO HERO HAS LANDED. Still.** This context produced probes only
(`out/p9_*`, `out/pl_playa.png`). The strip machinery in `studio.render_set`
(`T1_BORDER="lo,hi"`) remains **untested end to end**. Render four strips at
0.00/0.25/0.50/0.75 with `T1_FX=0`, stitch, then run `post.py` once on the
stitched frame — never per strip, they band at the seams.

**6. The tail is still 99 mm long** (model −2.108, measured −2.007, factory
arithmetic −2.009). Loft change; the counter's `X1` must move with it.

**7. Six materials still carry a constant roughness.** `brass` was folded in but
`audit.py` still counts 6 — re-check which, and whether the shim in
`t1_detail._brass()` is resolving to the shared datablock as intended.

**8. The 44 major / 32 minor findings in `AUDIT_RECOVERED.md`** have still not
been through a skeptic pass. A triage exists in this context's history: 23
high-value open, 18 low-value open, 24 already fixed, 13 refuted. Roughly eight
of the 23 were applied in rev 8; the rest are open.

## 4. Donald's brief, in his own words — this reframed the deliverable

> "I really want this to give the person the opportunity to feel like they were
> on playa del carmen all those years ago. I want the owner to remember standing
> in the kombi, in this very picture that was provided. I want it to be so real
> it evokes emotion."

A white-studio still **cannot** do that — by construction it removes the place.
Agreed shape: deliver the white-studio hero as the fidelity benchmark **and** a
warm Playa hero for the memory. The Playa rig exists and renders; it has not
been art-directed.

He also scoped the art reproduction pass himself, to exactly four pieces:
**the mural, the paisley, the "Señor Tacombi" script, and the 100% Calidad
decal.** Two are done, two are not.

## 5. Claims already considered and rejected — do not re-open

Everything in `HANDOFF_rev7.md` §5 still stands: the tyre is **0.665** on a
16-inch rim, and `Z_BELT` is **not** derived from sill − 100 mm. Add to that
list:

- **"The canvas ragtop should come back" / "model the lids closed."** Locked
  OPEN by Donald 2026-08-10 with the reasoning recorded in memory.
- **"Scan SPEC §0.2 for material names to build the ban list."** Tried; flags
  six correct materials. §1 above explains why.
- **"Raise the flank saturation to 0.816."** It is an albedo number. §10.9.

## 6. Process note

Donald asked mid-context to be passed to a fresh context because he was
worried about continuity. Everything is committed, `STATE.md` is regenerated
against a clean tree, and the repo, bundle, updated docs and probe renders are
written back to his disk. **Anything not on his disk does not exist** — a
container restart has already killed one workflow mid-run.
