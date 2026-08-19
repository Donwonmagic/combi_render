# THE LEDGER — rev 43

**What this file is, and why it did not exist before.** The owner was asked what DONE means for
the 3D model and chose the strictest of the options offered: **every instrumented measure green.**
That answer cannot be read literally — seven probes carry KILL controls *written to fail*, two more
are deliberately left failing, and one refuses to rule — so a run where every probe exits 0 would
be a **regression**, not success. What it must mean instead is the brief's own rule:

> **A tally that matches the list means the probe is healthy; only a tally that differs is a finding.**

So this ledger sorts every instrumented measure into four classes, and **done is: class 1 all green,
class 2 all still red, class 3 empty, class 4 empty.** Class 3 is the burn-down. Class 4 is the one
that makes the definition honest — SPEC §5's *"non-overlapping"* sat in the document for
**thirty-nine revisions with no probe**, and the moment rev 42 built one it revealed 56 % of the
painted surface self-overlapping. A requirement nobody has instrumented is not a requirement.

Machine: Linux x86_64, 4-core Intel Xeon @ 2.10 GHz, 15 GB. Blender 4.5.3 LTS via `bpy` from PyPI
(see CAVEAT at the end — `download.blender.org` is unreachable from this environment).

---

## CLASS 1 — GREEN-REQUIRED. Must pass. **All green.**

| measure | SUB=1 | SUB=2 | expected | state |
|---|---|---|---|---|
| `build.py` VERIFY | 0 fail, 0 warn | 0 fail, 0 warn | 0/0 | ✅ |
| `audit.py` | 0 fail, 0 warn | 0 fail, 0 warn | 0/0 | ✅ |
| roof crown @ rear axle | 1.9835 | 1.9833 | 1.9835 / 1.9833 | ✅ |
| cut roof hole | 70069 v | 254428 v | 70069 / 254428 | ✅ |
| objects at `materials:` | — | 131 | 131 | ✅ |
| mesh objects | 190 | 190 | 190 | ✅ |
| distinct materials | 42 | 42 | 42 | ✅ |
| constant-roughness materials | 5 | 5 | 5 | ✅ |
| non-manifold edges (body) | 0 | 0 | 0 | ✅ |
| body faces | 59885 quad / 458 tri / 4617 ngon | 238897 / 1200 / 6569 | rev-42 baseline | ✅ |
| rake | 17.75 mm/m (locked 17.75) | same | 17.75 | ✅ |
| dims | L=4.065 W=1.750 | same | 4.065 / 1.750 | ✅ |
| bay widths | 0.516 0.515 0.516 | same | equal | ✅ |
| arch gaps rear / front | 39.7 / 40.7 mm | same | 39.7 / 40.7 | ✅ |
| off flank | 804.9 mm (baseline −0.0 mm) | same | 804.9 | ✅ |
| over-rider rows | NOT APPLICABLE, **stated** | same | stated, not skipped | ✅ |

Probes required green, each read from **its own summary line**, not re-derived:

| probe | own summary line | expected | state |
|---|---|---|---|
| `probe_rev32_pointer` | `CONTROLS: 10 checked, 0 FAILED` | 10/0 | ✅ |
| `probe_dust_scope` | `CONTROLS: 8 checked, 0 FAILED` | 8/0 | ✅ |
| `probe_updust_pointer` | `CONTROLS: 6 checked, 0 FAILED` | 6/0 | ✅ |
| `probe_rev36_posts` | `ALL 5 CONTROLS PASSED` | 5/0 | ✅ |
| `probe_rev38_wheelbar` | all `[PASS]` C1–C6 | 6/0 | ✅ |
| `probe_rev38_floorpen` | `[PASS] C1` | 1/0 | ✅ |
| `probe_rev39_flank` | `CONTROLS: 3 checked, 0 FAILED` | 3/0 | ✅ |
| `probe_psf_lines` | `RESULT: clustering controls pass` | 2 FAILED, both EXPECTED | ✅ |
| `probe_f90` | `VERDICT: T1_CTAN_SP=0 IS a COMPLETE specular ablation` | — | ✅ |

---

## CLASS 2 — RED-BY-DESIGN. Must **stay** red. Going green is a regression.

A KILL control that starts passing means a route the project **closed** has re-opened.

| probe | own summary line | expected | state |
|---|---|---|---|
| `probe_orb_xratio` | `CONTROLS: 6 checked, 1 FAILED` — *"EXIT CODE 1 IS THE INTENDED RESULT HERE"* | 6/1 | ✅ still red |
| `probe_rev33_barend` | `CONTROLS: 7 checked, 4 FAILED` — A4–A7 are KILL | 7/4 | ✅ still red |
| `probe_rev34_levels` | `CONTROLS: 8 checked, 4 FAILED` | 8/4 | ✅ still red |
| `probe_rev34_ruling` | `CONTROLS: 6 checked, 4 FAILED` — R3–R6 are KILL | 6/4 | ✅ still red |
| `probe_rev35_harmonic` | `CONTROLS: 18 checked, 6 FAILED` | 18/6 | ✅ still red |
| `probe_rev40_datum` | `CONTROLS: 4 checked, 1 FAILED` | 4/1, C3 supposed to fail | ✅ still red |
| `probe_rev41_gate` | `CONTROLS: 5 checked, 1 FAILED` | 5/1, C4 supposed to fail | ✅ still red |
| `probe_rev42_uv` | `CONTROLS: 5 checked, 1 FAILED` / `FAILED: C3` | 5/1, C3 supposed to fail | ✅ still red |
| `probe_rev36_barend` | `REFUSING TO PRINT A RULING` | refuses | ✅ still refusing |
| `probe_clean_top` | `RESULT: controls FAIL` | deliberately failing | ✅ still red |
| `probe_dust_anchor` | exit 1 | deliberately failing | ✅ still red |

**31 of 31 probes run. 31 of 31 match their expected state. The instrument floor is intact.**

---

## CLASS 3 — OPEN FINDINGS. The burn-down. **Done = this table empty.**

| # | finding | where | state |
|---|---|---|---|
| 1 | The art frame — `DOOR_H` still rev 41's; door is 272.2 mm / 387.5 mm deeper | `folk_gen.py` `DOOR_H` | **open**, owner answered the art reaches the door edge |
| 2 | The body has **no UV layout at all**; ~56 % self-overlap | `t1_mats.py` `body_paint` | **open**, same re-bake as #1 |
| 3 | Report 3 — headlamps vs the paint break, 97 mm at ~3.9σ, open since rev 10 | SPEC §10.24 item 3 | **open**, new ordinal arm this revision |
| 4 | Report 4 — the VW glyph fuses into an X, 52 mm interpenetration | SPEC §10.94 | **open** |
| 5 | Report 7 — "100% Calidad" off centre at 0.180 of texture width | `cal_gen.py` | **open**, texture-vs-panel undetermined |
| 6 | Report 1 — the nose shape, `V_POW` locked 0.60, audit implies 0.30–0.48 | `t1_mats.py` `V_POW` | **open** |
| 7 | `SCR` measured, checked, condition met, **unapplied** — +76.2 mm fwd, −33.3 mm in z | `build.py` `SCR` | **open** |
| 8 | `probe_clean_top` / `probe_dust_anchor` — rewrite or retire, **ten revisions** | both probes | **open** |
| 9 | `tex/emblem.png` — genuinely orphaned | `texgen.py` | **open** |
| 10 | `analysis/` — 25 of 27 scripts hard-code a dead absolute path | `analysis/` | **open** |
| 11 | Absolute roof height — **OPEN AND UNMEASURED**; model reads 1.9835 on nothing | — | **open**, needs a frame |
| 12 | Ride height — owner states lower than stock; SPEC §0.2 and REF §2 **contradict** | — | **open**, never adjudicated |
| 13 | Off flank 804.9 mm — graded E, never adjudicated | — | **open**, needs a frame |
| 14 | Nolita authorised for geometry rev 15 — **28 revisions, zero frames measured** | — | **open** |
| 15 | Front roof lid needs **two-sided artwork** — owner's settled topology, unbuilt | `t1_shell.roof_lids` | **open** |
| 16 | A **trunk lid**, separate from the roof lids — `grep -c trunk` is 0 and 0 | — | **open** |
| 17 | "Clutter on the counter" — raised more than once, never closed | — | **open** |
| 18 | The `Senor` reconstruction — 0.459 of its own ceiling, rejected twice | `script_gen.py` | **open** |
| 19 | `senor.png` VALUE defect: opaque mean (205,194,200) vs target (127.4,124.9,130.0) | `script_gen.py` | **open** |
| 20 | **NEW, rev 43** — `probe_rev42_uv` does not reproduce its published figure | see below | **open** |
| 21 | **NEW, rev 43** — `ref_source.jpeg` is formally retired *and* load-bearing | SPEC §10.22 vs §0.2 | **open** |
| 22 | **NEW, rev 43** — 89 findings in `AUDIT_RECOVERED.md` never verified | that file | **in progress** |

**Twenty-two open. Countable, and that is the point: the instrument list grows, the findings list
burns down.**

### Finding 20, in full, because it is this revision's own

`probe_rev42_uv` re-run on the current tree prints:

```
  TOTAL SELF-overlap 32.6727 m^2 = 56.15 % of painted area
  TOTAL painted 58.1866 m^2, colliding 34.4939 m^2 = 59.28 %
```

SPEC §10.101.3 publishes **32.5746 m² = 55.97 %** of **58.2048 m²**. So painted area differs by
**−0.0182 m²** and self-overlap by **+0.0981 m²**, moving the headline **+0.18 pp**.

**It does not move the ruling** — §10.101.6's own sweep spans 59.06–67.50 % against a bar of 10 %,
so the verdict is unchanged and the figure was never good to better than ±8 pp. **But it is a
published figure that did not reproduce, and this project's standard is per-measurement.**

Two candidate causes, and I have not separated them:
1. **This environment runs `bpy` as a PyPI module, not the Blender binary.** Same 4.5.3, and the
   mesh reproduces to the *integer* (roof hole 70069 / 254428 v, 190 meshes, 59885/458/4617 body
   faces, 0 non-manifold) — but bit-identical floating-point area summation is **not proven**.
2. **The probe has an order-dependent accumulation.** §10.101.5 records a triangle-stream cache
   keyed wrongly once already, caught only because it printed 571.71 %.

Cause 1 is the more likely and is an artefact of this machine, not of the model. **Stated, not
rounded away.** Rev 44 should re-run it on a real Blender binary before treating either figure as
canonical.

---

## CLASS 4 — UNINSTRUMENTED REQUIREMENTS. No probe exists, so "green" is meaningless here.

**This is the class that keeps the definition of done honest.** Each of these is a stated
requirement with no instrument watching it.

| requirement | source | instrument |
|---|---|---|
| "No floating or intersecting artifacts" | SPEC §5 bullet 1 | **none** |
| "Crisp, regular quad topology; no n-gon pinching on the nose" | SPEC §5 bullet 2 | **none** — 4617 body ngons at SUB=1 are counted but not gated |
| "Correctly oriented, correct handedness" decals | SPEC §5 bullet 4 | **none** — rev 42 instrumented overlap and resolution only |
| Absolute replication of all eight artwork elements | SPEC §10.10 | **none** — the scope table is prose and 15 revisions stale |
| "The owner recognises his own vehicle" | SPEC §10.10 | **none, and probably uninstrumentable** — it is an owner reading |
| The emotional bar of the Playa hero | §7.4 | **none** |
| The die-cut sticker | §7.3 | **none — and no code, no asset, nothing on disk** |

---

## CAVEAT ON THIS WHOLE LEDGER

Every figure above was watched print on **this** machine, which reached Blender 4.5.3 through
`pip install bpy==4.5.3` because `download.blender.org` returns **403 through this environment's
proxy** — the brief's `.dmg` recipe and its Linux tarball equivalent both fail here. The
`/tmp/blender/blender` and `/tmp/blender/4.5/python/bin/python3.11` shims reproduce the layout the
repo hard-codes in eight files, so **not one of those eight was edited**. The guards and 31 of 31
probes reproduce their expected state under it. Finding 20 is the one place where a published
figure did not, and it is flagged rather than absorbed.
