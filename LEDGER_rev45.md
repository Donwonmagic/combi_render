# THE LEDGER — rev 45

**Supersedes `LEDGER_rev44.md`.** Same four classes, same rule, same purpose: it is the only artefact
in this project that answers *"how far are we"*. Done is **class 1 all green, class 2 all still red,
class 3 empty, class 4 empty.**

> **A tally that matches the list means the probe is healthy; only a tally that differs is a finding.**

**Machine:** Linux x86_64, **4 cores**, 15 GB. Blender **4.5.3 LTS** via `pip install bpy==4.5.3`,
because `download.blender.org` returns **403** through this environment's proxy — re-tested at rev 45,
still 403. Two shims reproduce the layout the repo hard-codes in eight `.py`/`.sh` files; **not one of
those eight was edited.** `START_HERE.md` carries the recipe. One correction to it: the interpreter
shim does not need a venv if `bpy` is installed against the system `python3.11` — `#!/bin/sh` +
`exec /usr/bin/python3.11 "$@"` is enough, and it still must `exec` rather than be a symlink.

---

## §1. THE HEADLINE, AND IT IS NOT A MEASUREMENT

**SEVENTEEN COMMITS OF REV-44 AND REV-44b WORK WERE NEVER MERGED.**

`origin/claude/tacombi-combi-rev-44-h4ipmg` sat seventeen commits above the point where PR #2 was
merged. Neither `origin/main` nor the branch rev 45 started from had any of them. Missing from the
mainline until this revision:

| what | where |
|---|---|
| **`SPEC.md` §10.102 – §10.109**, 632 lines, all eight rev-44b sections | `SPEC.md` |
| §10.100's door-wrap **retraction** and §10.106's forward lower lobe | `t1_shell.py` |
| §10.107's six stroke ends on the ring | `t1_core.py` |
| §10.108's prop fix — 49° of rake down to 3° | `t1_shell.py` |
| `cab_fitout`, `door_hinges` — the whole cab interior, +460 lines | `t1_detail.py` |
| `cabin_fill` and the delivery frame | `studio.py` |
| `round_edges` on all 42 materials | `t1_mats.py` |
| the roundel's 13.5 mm mounting plane | `build.py` |
| the hubcap red, the bumper/door overlap | `t1_mats.py`, `t1_shell.py` |
| **three of the four Nolita reference frames** | tree |

`SPEC.md` on `main` ends at **§10.101**.

### What that does to §0 of the rev-45 brief

The brief opens on the observation that the owner has reported the same defects three times while
every guard stayed green, and offers three candidate causes — he means something else, the fix is
sub-threshold, he is looking at an old image. **There is a fourth and it is simpler than all of
them: the fixes were measured, committed, and left on a branch.** The brief was written from a
working tree that had them and handed to a context that did not.

It also makes **W1 unexecutable as written**: its entire method is specified against
`ref_nolita_front34.jpg`, a file that was not in the tree. See `REFERENCE_FRAMES_rev45.md`.

**All seventeen are merged.** Three conflicts, resolved: rev 44b's props and question figure win,
rev 45's drape wins, both guards kept. SPEC §10.113.4.

> **NEW RULE. A REVISION THAT IS NOT MERGED DID NOT HAPPEN.** Before diagnosing why a fix did not
> land, check that the fix is *in the tree you are looking at*. `git log HEAD..<the branch the last
> revision worked on>` is eleven characters and it would have saved this revision an entire
> investigation.

---

## §2. WHAT REV 45 DID, IN ONE TABLE

| # | finding | how it was found | state |
|---|---|---|---|
| A | **The nose badge was a flat plate on a curved nose.** Upper half 32 mm proud, lower half 0.3 mm *inside*. The whole W was in the sheet metal; it rendered as a **clock face**. | Radial raycast, 8 angles × 3 radii, against the built body. **Rev 44 found the same thing independently by a forward-most-x scan.** | **FIXED**, §10.110. `t1_core.drape_x`. Front faces 6.96–15.10 mm proud. Guarded; the guard fired twice on its own change. |
| B | **The headlamp lens was dished the wrong way round** — concave, its centre 10.1 mm *inside* the nose, so the aperture rendered as a dark red hole. | Raycast down the lamp's own axis: `T1_body` at 2.1116 **before** `hl_lens` at 2.1015. | **FIXED**, §10.111. Convex, apex 3 mm behind the bezel face. lens (R−B)/cream **+0.571 → +0.082** against −0.024 photographed. |
| C | **The bezel was brass.** | `ref_nolita_front34.jpg` at 4× the scale of the rev-10 frame: bezel b\* **+2.7 / +6.7** against that frame's own neutral **+6.9** and its red **+61.8**. | **RETIRED to chrome**, §10.111.3. Rev 10 is called **uncontrolled**, not wrong. `T1_HL_BEZEL=brass` renders the retired arm. |
| D | **"100 % Calidad" rendered peach.** The gradient's 0.42 bias started the ramp 42 % along, so the core evaluated to 84 % ORANGE and *nothing in the texture was the RED the generator declares nine lines above*. | Sampled `tex/calidad.png` straight off disk: core (237, 120, 22), G/R 0.508, against `RED = (214, 46, 30)`, G/R 0.215. | **FIXED**, §10.112. Bias → 0. Core now (216.6, 55.1, 28.2), G/R **0.255**, against the body red's 0.250. |
| E | **The sign props stood in the hole.** Both feet at y = +0.44, *inside* the roof aperture (−0.545…+0.565), so each prop rose out of thin air and ran a metre across the board's face. | Built-mesh bbox of `lid_strut*` against `lid_board`. **Rev 44b found it independently (§10.108).** | **FIXED — by rev 44b's patch, not rev 45's.** Rev 45's typed offset is discarded in favour of walking `roof_z` to the roof's own edge. Rev 45 keeps only its complementary Y guard. |
| F | **The reference frames were never committed.** | `git ls-files`. | **RECOVERED**, and the two identifications published as *unproven* were then found md5-identical to rev 44b's. `verify_clone.sh` now counts them. |
| H | **`optics-6` — the vehicle floated, open since rev 12.** G1 tight contact 0.9756, G3 under-body pool 0.9132, against a photographed 0.650 ± 0.210. | `probe_rev45_ground` — the first instrument that can read a contact shadow at all. The three prior measurements were taken in a side ORTHO or on a 400×300 matte, where the ground plane is edge-on. | **CLOSED, §10.116.** G1 **0.8729**, G3 **0.8406**, backdrop unmoved at 254.45. Two levers refuted first. `T1_SHADOW=1.0` restores the floating arm. |
| G | **The body red renders 3.5 σ too pale, and it is the studio, not the paint.** | Illuminant-free red/cream chroma over **four** photographs + a five-arm ablation. | **INSTRUMENTED, NOT APPLIED.** See §3 — it needs the owner. |

---

## §3. THE ONE THING REV 45 MEASURED AND REFUSED TO CHANGE

**The red renders too pale, the albedo is right, and the cause is the lighting rig — which is the
same rig that kills the contact shadow.**

Measured as the red paint's chroma **normalised to the cream in the same frame**, which removes
exposure and illuminant colour together (rule 14):

| frame | R | G | B | **G/R** |
|---|---|---|---|---|
| `ref_side.jpg` | 0.590 | 0.102 | 0.057 | **0.173** |
| `ref_nolita_doorshut.jpg` | 0.611 | 0.100 | 0.067 | **0.164** |
| `ref_nolita_flank.jpg` | 0.647 | 0.196 | 0.156 | **0.304** |
| `ref_playa_34.png` | 0.814 | 0.204 | 0.132 | **0.250** |
| **photographed mean** | | | | **0.223 ± 0.066** |
| **the render** | 0.995 | 0.443 | 0.383 | **0.455** |

**3.5 σ.** (`ref_nolita_front34.jpg` is excluded: its red channel clips at 240+ over the nose.)

**The albedo is not the defect.** `t1_mats.RED` is sRGB(196, 49, 36), G/R **0.250** — 0.4 σ from the
photographed mean. Finding 29's retraction established that the render reproduces its own albedo to
0.000; it never asked whether the render reproduces the *photograph*. It does not.

Five-arm ablation, `T1_SUB=1`, side view, red/cream G/R:

| arm | G/R | Δ |
|---|---|---|
| base | **0.455** | — |
| `T1_SPEC=0` | **0.347** | **−0.108** ← the dominant lever |
| `T1_W_MAPLO=0.98 T1_W_MAPHI=1.0` (no wear) | 0.425 | −0.030 |
| `T1_W_FADESAT=1.0` | 0.455 | **0.000 — bit-identical** |
| `T1_MOT_AMP=0` | 0.455 | **0.000 — bit-identical** |
| everything off | **0.297** | −0.158 |

**Two knobs everyone assumes matter do nothing at all**, which is the same class of result rev 44 got
for `WEAR['calidad']`. About **half** the excess is the specular response to the white cyclorama and
its 0.76-albedo floor.

**And that is the same finding as `optics-6`.** §10.109.4 records that "a 16 m strip plus a
0.76-albedo floor fills the vehicle's own shadow" — the rig that kills the contact shadow is the rig
that washes the paint. They are one defect with two symptoms.

**IT IS NOT APPLIED, AND IT MUST NOT BE APPLIED WITHOUT HIM.** §7 of the brief locks the paint's
finish in writing and §10.104.8 refuses to re-open `Roughness` or `Coat Weight`. Softening the studio
is a **presentation** change and it trades the catalogue-clean white background — which is the bar he
supplied — for paint that reads as it does in his own photographs. **Q6 of `mark_rev45_ba.py` puts
exactly that to him.** The template if he says yes is `cabin_fill` (§10.105): a declared, ablatable
presentation device with its ablation reported.

**One thing that is NOT a defect and was checked:** the fine speckle on the red. High-pass sd is
16.4 in the base render and **17.8 with every weathering arm ablated** — it is sampling noise at 24
samples, not the mottle map. Render heroes at more samples; change nothing.

---

## §4. CLASS 1 — GREEN-REQUIRED. Must pass.

| run | rev 45 |
|---|---|
| `T1_SUB=1 T1_VERIFY=1 build.py` | **VERIFY: 0 fail, 0 warn** |
| `T1_SUB=2 T1_VERIFY=1 build.py` | **VERIFY: 0 fail, 0 warn** |
| `T1_SUB=1 audit.py` | see §6 |
| `T1_SUB=2 audit.py` | see §6 |
| `./verify_clone.sh` | see §6 — and **`git fetch --unshallow` first**, or the `commits >= 227` line fails on `short:73` |
| `./bootstrap.sh` | **NEW, rev 45. ALL 10 PASS.** Reproduces the toolchain from a bare container and then runs `verify_clone.sh`. Proven from scratch: `rm -rf /tmp/blender && ./bootstrap.sh` rebuilds and passes. `--guards` adds both builds and the probes. |

**NEW IN CLASS 1, rev 45:**

| probe | own summary line | expected |
|---|---|---|
| `probe_rev45_nose` | `CONTROLS: 8 checked, 0 FAILED` | 8/0 — **C5 is a KILL**, see below |
| `probe_rev45_ground` | `CONTROLS: 4 checked, 0 FAILED` | 4/0 — **C4 is a KILL**. Reports G1 (tight contact), G3 (under-body pool) and G2 (backdrop). §10.116 |

`probe_rev45_nose` is the instrument this project was missing: **it does not type crop boxes.** Every
other crop box in this repository is a hand-typed literal that goes stale when a camera or a constant
moves. This one projects known 3-D landmarks through the render camera and samples where they land.
**C5 is a KILL written to fail forever** — a landmark one metre in front of the nose must not land on
the roundel — because without it "the projection works" is untestable: a stub returning a constant
would pass every other control.

**TWO controls that could not see their own defect, both recorded because it is the lesson.**

* **C4** tests the lens's **luminance** ratio and it **passed at 0.432 while the aperture was
  rendering red**. C6, the chroma control, is what catches it.
* **C8** was first written as *"the first object down the lamp axis is `hl_*`, not `T1_body`"*,
  straight off the measurement that found finding 41 — and it **passed in both arms**, because that
  measurement predated §10.111.1's convex lens. Re-written to require that no `T1_body` face lies
  *between* the lens and the bowl, and then **watched to fail** under `T1_HL_BOWL=0`.

**And `probe_rev45_ground` was wrong FOUR TIMES in one sitting** — a contaminated sample (the cream
reads "neutral"), an inert kill control (sampled off-screen, returned `<no sample>`, passed), a blind
level control (read the top corners, reported "PURE WHITE" for a frame with a horizon across it), and
the wrong window (0.5–3.5 tyre-widths, when the whole shadow lives in the first 0.35). Every one
produced a plausible number that would have been published.

*A ratio that is right for the wrong reason is not a control. A control is not finished when it
passes — it is finished when you have watched it fail on the defect. **And an instrument that has
never been wrong has never been tested.***

---

## §5. CLASS 2 — RED-BY-DESIGN. Must **stay** red.

Unchanged from `LEDGER_rev44.md` — eleven rows, plus rev 44's four. Re-read each from **its own
summary line**, never its exit code. Rev 45 added no CLASS 2 probes and retired none.

---

## §6. CLASS 3 — OPEN FINDINGS. The burn-down.

Carried from `LEDGER_rev44.md` with rev 45's changes marked. **Findings 1–37 keep their numbers.**

| # | finding | state at rev 45 |
|---|---|---|
| 4 | ~~Report 4 — the VW glyph fuses into an X, 52 mm interpenetration~~ | **CLOSED, and the diagnosis was wrong for thirty-five revisions.** The glyph never was the defect: rasterised in isolation it draws a clean V over W. It was **sunk into the bodywork** (§10.110). Rev 44's V half-angle correction is merged and the drape is applied on top. |
| 5 | Report 7 — "100 % Calidad" | **CLOSED, §10.112.** Position was settled at rev 44; the colour is fixed at its root in `cal_gen.py`. |
| 2 | The body has **no UV layout at all**, ~56 % self-overlap | open — sized, not fixed |
| 6 | Report 1 — the nose shape, `V_POW` locked 0.60 | open — instrumented, one chain, needs a second |
| 7 | `SCR` measured, checked, condition met, **unapplied** | open |
| 8 | `probe_clean_top` / `probe_dust_anchor` — rewrite or retire, **twelve revisions** | open |
| 9 | `tex/emblem.png` — genuinely orphaned | open |
| 10 | `analysis/` — 25 of 27 scripts hard-code a dead absolute path | open |
| 11 | **Absolute roof height — OPEN AND UNMEASURED** | open — **top of the photo list** |
| 12 | Ride height — owner states lower than stock; SPEC §0.2 and REF §2 contradict | open |
| 13 | Off flank 804.9 mm — graded E, never adjudicated | open — **top of the photo list** |
| 14 | Nolita authorised for geometry at rev 15 | **effectively closed by use.** Rev 44b measured it and rev 45 measured four of the five frames. |
| 16 | A **trunk lid**, separate from the roof lids — `grep -c trunk` is 0 | open |
| 17 | "Clutter on the counter" | open |
| 18 | The `Senor` reconstruction — 0.459 of its own ceiling | open |
| 19 | `senor.png` VALUE defect | open |
| 20 | `probe_rev42_uv` vs §10.101.3's published figure | open, stable not noisy |
| 21 | `ref_source.jpeg` retired *and* load-bearing | open — needs the owner |
| 22 | **89** findings in `AUDIT_RECOVERED.md` never verified | open at 89 |
| 23 | The generator's tilde is half-weight | open, low severity |
| 24 | `AUDIT_rev43.md` disagrees with itself on the tilde | open |
| 25 | `AUDIT_rev43.md` §2 still lists the retracted tilde finding | open |
| 26 | `ROUNDEL_Z_AG = 1.0170` tuned against a moved datum | open — instrumented, geometry not moved, all three chains inside 1 σ |
| 27 | SPEC's *"`V_POW` ≈ 0.30–0.48"* does not reproduce from its own measurement | open |
| ~~optics-6~~ | ~~the vehicle floats — open since rev 12~~ | **CLOSED, rev 45, §10.116.** And note what it cost to close: the probe was wrong **four times** before it was right — contaminated sample, inert kill control, blind level control, wrong window — each producing a plausible number that would have been published. |
| **42** | **NEW, rev 45 — "100 % CALIDAD" — THE TYPE IS OFF-CENTRE INSIDE THE DECAL, and this is not what rev 44 closed.** Type centroid minus burst centroid: built **(−0.1195, +0.1782)** of the decal, photographed **(+0.0455, +0.0746)** on `ref_playa_34.png`. **The horizontal error is in the wrong direction.** Type bbox cols 0.155–0.645 against a burst spanning 0.015–0.951. | **HIS REPORT, rev 45 close. Open.** Finding 5's "the defect is COLOUR, not position" was about the PANEL'S PLACEMENT ON THE VEHICLE (Report 7, 0.180 of texture width). Both true, different things. `cal_gen.py`. |
| **43** | **NEW, rev 45 — THE VW GLYPH'S VERTICAL PROPORTIONS ARE WRONG, measured without any axis ratio.** As a fraction of the ring's vertical diameter from its top: V's apex **0.254 built against 0.353 photographed — 0.099, i.e. 27.7 mm on a 280 mm badge.** V's arms clear the band at 0.104 vs 0.147; W's troughs 0.866 vs ~0.81. The V occupies 0.15 of the ring's height against 0.206; the W 0.61 against 0.46. | **HIS FOURTH REPORT OF THIS BADGE. Open.** Rev 45 fixed the drape (§10.110) and explicitly did not check the spine, because ANGLES need the axis ratio. **Vertical extents do not** — §10.107.2's own rule. `t1_core.vw_bars`. |
| **44** | **NEW, rev 45 — THE NOSE IS PLANAR, and finding 6 is about a different axis.** Raycast at z = 1.25: the surface recedes **14.3 mm over 0.70 m of half-width**. The only forward bulge in the model is `bulge = 0.019` in `t1_shell.nose_shape`. | **HIS REPORT. Open, and NOT YET ANCHORED** — rev 45 has no photographed measurement of the plan curvature and threw away an uncontrolled attempt rather than publish it. `V_POW_Z` drives the PAINTED break line, not the metal. |
| **45** | **NEW, rev 45 — the script's contrast, re-measured and HIS THIRD REPORT.** Michelson ink-against-red **0.217 built, 0.324 photographed** (finding 30 has 0.269/0.466 on different boxes; same ratio). | **THE SANCTION FINDING 30 WAS WAITING FOR HAS ARRIVED.** He has asked three times. Ship a deliberate departure and say in SPEC that it is one. Note finding 19 pulls the other way, so the lever is the EDGE, not the ink's mean. |
| **38** | **NEW, rev 45 — the body red renders 3.5 σ too pale and it is the STUDIO, not the paint.** Same root cause as `optics-6`. | **INSTRUMENTED, NOT APPLIED — needs the owner.** §3 above; Q6 of `mark_rev45_ba.py`. Now guarded by `probe_rev45_paint`, which **reproduces the hand measurement exactly (P1 = 0.455) by a completely different method** — a visible-population sample at projected landmarks, against a hand-masked region. **And it settles that this is ONE finding, not three:** the hubcap red reads P2 = 0.603 against a photographed 0.274 ± 0.096, i.e. **3.4 σ, the same magnitude and the same sign as the flank**, while the cream's own warmth is **within 0.8 σ** (P3 +0.0263 against +0.037 ± 0.013). The cream is not mis-coloured; it reads grey because it sits against pure white with a washed red beside it. |
| **39** | **NEW, rev 45 — the roof sign board's artwork is a flower mural; every photograph shows a hand-chalked BLACKBOARD** in a cream frame with TACOMBI across the top and BIENVENIDOS down the side. | **NOT TOUCHED — art direction.** Q5 of `mark_rev45_ba.py`. |
| **40** | **NEW, rev 45 — the emblem's backing disc is buried.** `roundel()`'s `disc_prof` puts its front surface *on* the mounting plane at r = 0, so with the ring's bead 13.5 mm proud the disc's centre sits behind the nose. Harmless (cream on cream) but it is dead geometry that z-fights. | open, low severity |
| ~~41~~ | ~~there is no headlamp aperture cut in the nose~~ | **CLOSED, rev 45, §10.115.** Bored in step 3 with the other apertures. Raycast down the lamp axis goes `hl_lens -> T1_body -> T1_body -> hl_bowl` un-bored and `hl_lens -> hl_bowl` bored. lens/cream **0.423 -> 0.549** against 0.565 photographed; chroma **+0.069 -> +0.027** against −0.024. The bore's DEPTH and SECTION are authored, not measured. `T1_HL_BOWL=0` restores the un-bored arm. |

**Closed this revision: 4, 5, 41, and `optics-6` after thirty-three revisions. Opened: 38, 39, 40, 41,
and — from his four reports at the close of rev 45, all four measured before handover — 42, 43, 44, 45.
Open from the record: 28.**

> **AND THE PATTERN IN 42–45 IS ITSELF THE FINDING.** All four are things he has reported before.
> Two of them (42, 44) were previously "closed" against a DIFFERENT AXIS of the same part — the
> decal's placement on the body rather than the type's placement in the decal; the painted break
> line rather than the sheet metal's shape. One (43) was left explicitly unchecked by rev 45 on a
> reason that was right for angles and wrong for vertical extents. One (45) has been waiting three
> revisions for a sanction he has now given three times.
> **NEW RULE: HIS REPEAT IS A MEASUREMENT.** When he reports the same defect twice, the prior
> closure was wrong or incomplete. Find the axis nobody checked.

---

## §7. CLASS 4 — UNINSTRUMENTED

* **The cab interior** — merged this revision and still class 4. §10.104's furniture is type-correct
  1963 T1 and **not measured**; no frame resolves the cab. `PHOTOS_WANTED` asks for one.
* **The roof sign board's artwork** — see finding 39. Not measured, and now known to disagree with
  every frame we hold.

---

## §8. THE FRAMES, AND THE ONE THAT IS NEW

`REFERENCE_FRAMES_rev45.md` is the inventory and it replaces the rev-45 brief's §4, which was wrong.
**Nine frames, all tracked**, plus the five `IMG_*` uploads kept as provenance.

`ref_playa_34.png` is **new to this project** — it was not in rev 44's inventory or wanted-list. It is
the **Playa** truck and it is the only frame in the whole set that shows the painted livery this model
reproduces: the folk art, the "Señor Tacombi" script, the Calidad decal, an **unlit** headlamp in
daylight, and the cab door over the front arch. Three of rev 45's measurements come off it.
