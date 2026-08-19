# THE LEDGER — rev 44

**Supersedes `LEDGER_rev43.md`.** Same four classes, same rule, same purpose: it is the only artefact
in this project that answers *"how far are we"*. Done is **class 1 all green, class 2 all still red,
class 3 empty, class 4 empty.**

> **A tally that matches the list means the probe is healthy; only a tally that differs is a finding.**

**Machine:** Linux x86_64, **4 cores**, 15 GB. Blender **4.5.3 LTS** via `pip install bpy==4.5.3`,
because `download.blender.org` still returns **403** through this environment's proxy — re-tested at
rev 44, still 403, for both the tarball and the `.dmg`. Two shims reproduce the layout the repo
hard-codes in **eight** `.py`/`.sh` files; **not one of those eight was edited.** See `START_HERE.md`,
which now carries the recipe instead of pointing at a Blender download that fails.

---

## WHAT REV 44 CORRECTED IN THE LEDGER ITSELF

`LEDGER_rev43.md` was the spine and it carried four errors of its own. All four found by running or
counting, not by reading.

| ledger rev 43 said | the machine says |
|---|---|
| "**seven** probes carry KILL controls written to fail" | **EIGHT.** CLASS 2's own table lists 8 intended-fail tallies, plus 1 refusing and 2 deliberately failing = 11 rows. 8+1+2, not 7+2+1. |
| "**31 of 31 probes run.** 31 of 31 match their expected state." | **31 probes existed; the ledger's tables name only 20.** Eleven had no row and no expected tally anywhere in it: `probe_cross_anatomy`, `probe_ctan_index`, `probe_ctan_pedestal`, `probe_orb_blade`, `probe_orb_hoop`, `probe_orb_post`, `probe_psf_owner`, `probe_psf_workshop`, `probe_rev16`, `probe_shutlines`, `probe_v_apex`. **"31 of 31" was unsupported by the document's own tables.** |
| CLASS 3 finding **15**, front roof lid needs two-sided artwork, listed **open** | **KILLED BY BOTH REFUTERS** in `AUDIT_rev43.md` §4 — the contract it rests on was retired eleven revisions earlier (§10.26/§10.28, the owner overturned it at rev 12). It should never have been carried as open. |
| CLASS 3 finding **22**, "89 findings … never verified", and the rev-44 brief's "**119** sit unverified" | **89.** The other 30 live in `AUDIT_rev43_PARTIAL.json` and are the **FIDELITY half of the same 60** `AUDIT_rev43.md` verified — title-for-title. 89 + 30 = 119 **double-counts**. |

---

## CLASS 1 — GREEN-REQUIRED. Must pass. **All green, re-run this revision.**

Four guard runs, all watched print on this machine at rev 44:

| run | result |
|---|---|
| `T1_SUB=1 T1_VERIFY=1 build.py` | **VERIFY: 0 fail, 0 warn** (17.4 s) |
| `T1_SUB=1 audit.py` | **0 fail, 0 warn, 190 meshes, 5 materials constant-rough** |
| `T1_SUB=2 T1_VERIFY=1 build.py` | **VERIFY: 0 fail, 0 warn** (61.9 s) |
| `T1_SUB=2 audit.py` | **0 fail, 0 warn, 190 meshes, 5 materials constant-rough** |

Re-run again after the only two source edits this revision (`t1_shell.py` comment, `SPEC.md`):
**0 fail, 0 warn.** `./verify_clone.sh`: **ALL 66 PASS, exit 0.**

**`./verify_clone.sh` DOES NOT PRINT 66 PASS ON A FRESH CLONE, and the rev-44 brief said it must.**
It prints **65 PASSED, 1 FAILED** and **exits 1**, because the clone is **shallow** — 50 commits
against the ≥227 the script requires. `git fetch --unshallow`, then 66. A hint to that effect is now
in the script; **the check itself was not touched.**

Probes required green, each read from **its own summary line**:

| probe | own summary line | expected | rev 44 |
|---|---|---|---|
| `probe_rev32_pointer` | `CONTROLS: 10 checked, 0 FAILED` | 10/0 | ✅ |
| `probe_dust_scope` | `CONTROLS: 8 checked, 0 FAILED` | 8/0 | ✅ |
| `probe_updust_pointer` | `CONTROLS: 6 checked, 0 FAILED` | 6/0 | ✅ |
| `probe_rev36_posts` | `ALL 5 CONTROLS PASSED` | 5/0 | ✅ |
| `probe_rev38_wheelbar` | all `[PASS]` C1–C6 | 6/0 | ✅ |
| `probe_rev38_floorpen` | `[PASS] C1` | 1/0 | ✅ |
| `probe_psf_lines` | `RESULT: clustering controls pass` | 2 FAILED, both EXPECTED | ✅ |
| `probe_f90` | `VERDICT: T1_CTAN_SP=0 IS a COMPLETE specular ablation` | — | ✅ |
| `probe_psf_owner` | `RESULT: controls pass` | **newly tabled, rev 44** | ✅ |
| `probe_psf_workshop` | `RESULT: controls pass` | **newly tabled, rev 44** | ✅ |
| `probe_rev39_flank` | `CONTROLS: 3 checked, 0 FAILED` | 3/0 | ✅ — needed `out/p_side.png` rendered first |
| `probe_rev44_lampmove` | `CONTROLS: 6 checked, 0 FAILED` | 6/0 | ✅ **new, rev 44** — arms SPEC:7005's *"DO NOT MOVE THE ROUNDEL WITH THE LAMPS"* on the built mesh, and watches the roundel's height from **both** chains (finding 26) |

---

## CLASS 2 — RED-BY-DESIGN. Must **stay** red. Going green is a regression.

**EIGHT probes carry KILL controls written to fail**, one refuses to rule, two are deliberately
failing. Eleven rows.

| probe | own summary line | expected | rev 44 |
|---|---|---|---|
| `probe_orb_xratio` | `CONTROLS: 6 checked, 1 FAILED` | 6/1 | ✅ still red |
| `probe_rev33_barend` | `CONTROLS: 7 checked, 4 FAILED` | 7/4 | ✅ still red |
| `probe_rev34_levels` | `CONTROLS: 8 checked, 4 FAILED` | 8/4 | ✅ still red |
| `probe_rev34_ruling` | `CONTROLS: 6 checked, 4 FAILED` | 6/4 | ✅ still red |
| `probe_rev35_harmonic` | `CONTROLS: 18 checked, 6 FAILED` | 18/6 | ✅ still red |
| `probe_rev41_gate` | `CONTROLS: 5 checked, 1 FAILED` | 5/1, C4 by design | ✅ still red |
| `probe_rev42_uv` | `CONTROLS: 5 checked, 1 FAILED` / `FAILED: C3` | 5/1, C3 by design | ✅ still red |
| `probe_rev40_datum` | `CONTROLS: 4 checked, 1 FAILED` | 4/1, C3 by design | ✅ still red |
| `probe_rev36_barend` | `REFUSING TO PRINT A RULING` | refuses | ✅ still refusing |
| `probe_clean_top` | `RESULT: controls FAIL` | deliberately failing | ✅ still red |
| `probe_dust_anchor` | `RESULT: FAIL` | deliberately failing | ✅ still red |

**NEW IN CLASS 2, rev 44:**

| probe | own summary line | expected | why |
|---|---|---|---|
| `probe_rev44_report3` | `CONTROLS: 6 checked, 1 FAILED — C5` | 6/1 | **C5 is a KILL** (never green). **C6 was the burn-down gate for §10.24 item 3 and it WENT GREEN THIS REVISION** — the only control in this project that was ever supposed to change class, and it did. |
| `probe_rev44_doorart` | `CONTROLS: 6 checked, 1 FAILED — C5` | 6/1 | C5 is the finding, armed as a KILL: a re-point must not move a fixed `v`. It moves it **309.1 mm**. |
| `probe_rev44_typo` | `CONTROLS: 8 checked, 1 FAILED — N1` | 8/1 | N1 is the one new finding — the tilde is present but **half-weight** (8 px against 16). |
| `probe_rev44_nolita_nose` | `CONTROLS: 4 checked, 1 FAILED — C4` | 4/1 | C4 is a **KILL**: this frame must never be quoted for a magnitude. It gives an **ordinal only** — a third arm for §10.24 item 3. |
| `probe_rev44_vpow` | `CONTROLS: 6 checked, 1 FAILED — C3` | 6/1 | C3 is a finding **against SPEC, not the model**: the published *"V_POW 0.30–0.48"* does not follow from the published 0.111 ± 0.015, which inverts to 0.257–0.344. |

### THE ELEVEN UNTABLED PROBES, CLASSIFIED — rev 44

`LEDGER_rev43.md` claimed *"31 of 31 probes run"* while naming 20. Rev 44 ran the other eleven and
sorted them, so the claim can be made honestly or dropped:

| probe | what it is | readable by the project's own rule? |
|---|---|---|
| `probe_psf_owner` | control-bearing, `RESULT: controls pass` | **yes** — tabled in CLASS 1 above |
| `probe_rev39_flank` | control-bearing, `CONTROLS: 3 checked, 0 FAILED` | **yes** — tabled in CLASS 1 above |
| `probe_psf_workshop` | control-bearing, `RESULT: controls pass` | **yes** — tabled in CLASS 1 above |
| `probe_orb_blade` | controls, but printed as `controls: C1 PASS C2 PASS C3 PASS C5 FAIL` | **no** — non-standard format |
| `probe_orb_hoop` | controls, printed as `controls: C1 FAIL C2 FAIL C3 PASS` | **no** — non-standard format |
| `probe_v_apex` | **reporter** — ends on a CEILING statement, no controls | n/a |
| `probe_cross_anatomy` | **reporter** — ends on `total 804.9 mm` | n/a |
| `probe_shutlines` | **reporter** — describes a guard not yet armed | n/a |
| `probe_rev16` | **reporter** — prints an x-extent inventory | n/a |
| `probe_ctan_index` | **reporter** — 922 lines, no controls | n/a |
| `probe_ctan_pedestal` | **reporter** — ends UNVERIFIED, by its own words | n/a |
| `probe_orb_post` | **reporter** — ends on a CEILING statement | n/a |

**So the honest statement, counted off the RUNS:** there are **34** `probe_*.py` on disk at rev 44
(31 inherited + 3 added here). **25 are control-bearing with a summary line the project's reading
rule can parse — 11 in CLASS 1, 11 in CLASS 2, 3 new — and every one of the 31 inherited among them
reproduced its expected tally this revision.** **2** carry controls in a format the rule cannot parse
(`probe_orb_blade`, `probe_orb_hoop`). **7** are reporters and were never gates at all
(`probe_v_apex`, `probe_cross_anatomy`, `probe_shutlines`, `probe_rev16`, `probe_ctan_index`,
`probe_ctan_pedestal`, `probe_orb_post`). 25 + 2 + 7 = 34. *"31 of 31"* conflated the three kinds.

**AND A METHOD NOTE, BECAUSE THE SHORTCUT WAS WRONG.** A source-grep classifier — "does this file
contain a summary-line string?" — was written to produce that table quickly and **disagreed with the
runs on five probes** (`probe_dust_anchor`, `probe_psf_workshop`, `probe_rev38_floorpen`,
`probe_rev38_wheelbar`, `probe_updust_pointer`), because their summary strings are assembled from
variables rather than written as literals. **The grep was discarded and the table above is built from
what was watched print.** §9's rule applies to derivations as much as to figures.

**A PROCEDURAL NOTE THAT COST ME A CYCLE, RECORDED SO IT DOES NOT COST THE NEXT ONE.**
`probe_rev39_flank`, `probe_rev40_datum`, `probe_v_apex` and several others are **plain-Python**
probes, not Blender ones. Run under `/tmp/blender/blender -b --python`, they read `sys.argv[1]` as a
render path and get `'-b'`, dying with `FileNotFoundError: '-b'`. **That is not a shim defect** —
real Blender leaves the same `sys.argv` — **it is the wrong interpreter.** They also need
`out/p_side.png`, which is gitignored and renders in **64.2 s**.

---

## CLASS 3 — OPEN FINDINGS. The burn-down. **Done = this table empty.**

| # | finding | state at rev 44 |
|---|---|---|
| 1 | The art frame — the door is 272.2 mm / 387.5 mm deeper than the art's outline | **CHARACTERISED, rev 44.** The owner answered: **EXTEND at drawn scale, do not stretch.** `probe_rev44_doorart` shows the record was wrong about the mechanism — see below. **Open, and bigger than it looked.** |
| 2 | The body has **no UV layout at all**; ~56 % self-overlap | **SIZED, rev 44 — and it is NOT inflated by the inner skin.** See below. **Open.** |
| 3 | ~~Report 3 — headlamps vs the paint break, 97 mm at ~3.9σ, open since rev 10~~ | **CLOSED, rev 44 — APPLIED after 34 revisions.** `HL_Z` 1.0300 → 0.9330. The gate `probe_rev44_report3` C6 is **GREEN**: the lens top sits 45.2 mm BELOW the break where it stood 51.8 mm above it. Trap respected and armed — `probe_rev44_lampmove` 4/4, roundel measured on the built mesh at 1.0170, unmoved. |
| 4 | Report 4 — the VW glyph fuses into an X, 52 mm interpenetration | open |
| 5 | Report 7 — "100% Calidad" off centre at 0.180 of texture width | open |
| 6 | Report 1 — the nose shape, `V_POW` locked 0.60 | **INSTRUMENTED, rev 44 (`probe_rev44_vpow`); NOT applied.** The built rise reproduces SPEC's published **0.208** and the build is **1.87× too steep** against the photographed 0.111 ± 0.015 — the audit's *"~2× too fast"* is confirmed. **But SPEC's stated range does not reproduce from SPEC's own numbers:** inverting 0.111 ± 0.015 gives **V_POW 0.257–0.344**, not *"0.30–0.48"*; the 0.48 end needs 0.111 + 0.048, over **3σ** out. **Still ONE CHAIN**, and §10.24's own lesson is that a single-chain claim moving the FACE of the vehicle needs a second derivation. **Safe to apply when one exists:** the hard bound `V_APEX ≤ 0.396` is untouched by `V_POW`, and a refit to 0.300 *improves* Report 3's clearance 45.2 → 141.8 mm rather than re-breaking it. |
| 7 | `SCR` measured, checked, condition met, **unapplied** | open |
| 8 | `probe_clean_top` / `probe_dust_anchor` — rewrite or retire, **eleven revisions** | open |
| 9 | `tex/emblem.png` — genuinely orphaned | open |
| 10 | `analysis/` — 25 of 27 scripts hard-code a dead absolute path | open |
| 11 | **Absolute roof height — OPEN AND UNMEASURED**; model reads 1.9835 on nothing | open — **but for the first time there is a frame that could close it.** `ref_nolita_front34.jpg` (owner upload, rev 44) carries **people standing on the ground beside the vehicle**, which no earlier reference did. Not yet measured. |
| 12 | Ride height — owner states lower than stock; SPEC §0.2 and REF §2 contradict | open, never adjudicated |
| 13 | Off flank 804.9 mm — graded E, never adjudicated | open — **top of the photo list** |
| 14 | Nolita authorised for geometry rev 15 — **29 revisions, zero frames measured** | open — **but §7.1 now settles that it is ONE VEHICLE, so the frames are admissible** |
| 15 | ~~Front roof lid needs two-sided artwork~~ | **CLOSED, rev 44 — it was never open.** Killed by both refuters; the contract was retired at rev 12 by the owner. Carried in error. |
| 16 | A **trunk lid**, separate from the roof lids — `grep -c trunk` is **0 and 0** | open, **re-confirmed by running it this revision** |
| 17 | "Clutter on the counter" — raised more than once, never closed | open |
| 18 | The `Senor` reconstruction — 0.459 of its own ceiling, rejected twice | open |
| 19 | `senor.png` VALUE defect: opaque mean (205,194,200) vs target (127.4,124.9,130.0) | open |
| 20 | `probe_rev42_uv` does not reproduce SPEC §10.101.3's published figure | **REPRODUCED A SECOND TIME, rev 44: 56.15 %** against the published 55.97 %. Two independent runs on this platform agree exactly. **Cannot be settled** — `download.blender.org` is still 403, so no binary exists here to compare against. **Open, and now known to be stable rather than noisy.** |
| 21 | `ref_source.jpeg` is formally retired *and* load-bearing | **RE-OPENED, rev 44, against my own correction made the same day.** I closed it on *"the frame is NOT retired"* — **false**: §10.2 calls it *"the retired 246 × 197 thumbnail"*. What IS right is that §10.22's citation to §0.2 is bogus. **The contradiction is sharper than either statement:** §8.1's own coordinates resolve **only** on `ref_source.jpeg` (sat **0.73**, inside its published 0.70–0.83; `ref_side.jpg` gives 0.11 and no hub), so §0.2's five **M**-graded ⚠ locks rest on a frame §10.2 retires. **Open — needs the owner, or the five locks re-derived.** |
| 22 | **89** findings in `AUDIT_RECOVERED.md` never verified | open at **89** — not 119 |
| 23 | **NEW, rev 44** — the generator's tilde is **half-weight**: 8 px against the photograph's 16 | open, low severity, `probe_rev44_typo` N1 |
| 24 | **NEW, rev 44** — `AUDIT_rev43.md` disagrees with itself on the tilde: §0 says **16 px**, §5's typography ceiling says **62 px at 7.8σ** | open — the 61 px component sits **under the S**, not over the `n`. Does not change the retraction; both numbers say the tilde exists. |
| 25 | **NEW, rev 44** — `AUDIT_rev43.md` §2 still lists the **RETRACTED** tilde finding among its surviving severity-5s | open — so **"55 surviving" over-counts by one.** §0 and §1 were updated; §2's table was not. |
| 27 | **NEW, rev 44** — SPEC's *"`V_POW` ≈ 0.30–0.48"* **does not reproduce from its own published measurement** | open — inverting 0.111 ± 0.015 gives **0.257–0.344**. The 0.48 end needs a rise of 0.159, **3.2σ** above the published figure. `probe_rev44_vpow` C3. Nobody has ever re-derived it because nobody ever inverted it. |
| 26 | **NEW, rev 44** — `ROUNDEL_Z_AG = 1.0170` is a constant **tuned against a datum that has since moved, and not expressed in terms of it** | **INSTRUMENTED, rev 44; the geometry is NOT moved and the first statement of this finding was OVER-CLAIMED.** Its comment cites two figures that no longer compute: *"rake_drop(2.1155) is 0.1063"* computes **0.0855**, *"break_z(2.1155) = 1.166 AG"* computes **1.1865** (0.1063 reproduces under neither the current `RAKE_Z0` nor the one it says it replaced — it predates the rev-13 rake). **That part stands and is SPEC §10.25's own defect class**, nine lines above where §10.25's lesson is written. **What does NOT stand is "the roundel is ~20.5 mm TOO LOW"**, which rev 44 published from one chain's point estimate without its error bar or the second chain. Both chains, measured: **A** belt-relative 1.0375 ± 0.0300 (**0.68σ**), **B** roundel/lamp 1.0234 ± 0.0185 (**0.34σ**), joint 1.0274 ± 0.0157 (**0.66σ**). **All three inside 1σ — the roundel is NOT significantly mis-placed**, and moving geometry on a 0.7σ difference is laundering. **The real defect was that nothing was watching; `probe_rev44_lampmove` C5/C6 now watch, from both chains.** |

**Twenty-two carried in. THREE CLOSED — 15 (was never open), 21 (premise false) and, for the first
time in this project's history of deferring it, 3: SPEC §10.24 item 3 APPLIED. Four opened (23, 24,
25, 26), one re-sized (22). Open from the record: 23.** Plus `AUDIT_rev43.md`'s **55 → 54** (see finding 25), of which **two**
are re-verified and refuted this revision (below).

---

## WHAT REV 44 SETTLED, IN FULL

### Report 3 — the ordinal is TOPOLOGICAL, and the centre comparison never discriminated

The brief asked for the above/below read off the build's constants. Done, and it overturns the arm
rev 43 published:

* Build: headlamp centre **34.4 mm BELOW** the two-tone break at the lamp's own column.
* Photograph (§10.24's own figure): **131.4 mm BELOW**.
* **Both below. The ordinal agrees. Rev 43's "20 px BELOW" is consistent with the build and is not
  evidence of the defect.**

What *does* discriminate needs no scale at all: **in the build the break line CUTS ACROSS THE
HEADLAMP APERTURE** — a **131.9 mm chord** over a 172.4 mm lens, **159.9** over the 205.4 mm chrome
ring, the upper rim standing **51.8 mm above** the break. In `ref_source.jpeg` the lamp sits entirely
in the red with **12 px of clear red above it**. That is *"the paint job and the headlights are not
alligned"*, and no view or px/m conversion can argue with it.

The break at the lamp is the **V-swage**, not the flank belt; comparing against the belt is a 208 mm
error, armed as C5. C3 reproduces §10.24's published `belt − 0.242` to 5e-5, which is what validates
the frame; C4 proves the rake cancels. Rev 43's 20 px gap **reproduces exactly** (137−117); its
absolute rows 120/140 are 3 px low, a red-threshold difference that leaves the gap untouched.

### Item 1 — `DOOR_H` is not the v-map, and the one-line fix is the wrong fix

* **`DOOR_H` divides nothing.** Two read sites, `folk_gen.py:1274` and `:1287`, both `h = sv *
  DOOR_H`, both **multiplying**, for two motifs. SPEC §10.100.6 **and `t1_shell.py:546`** both called
  it a divisor of "every v-coordinate"; **both corrected.** The brief caught the SPEC one and scoped
  the fix to SPEC, leaving the identical sentence in the code — and neither noticed `DOOR_H` is not
  the v-map at all.
* **The v-map is `door_pv`, and it already drives off the door's own outline per station.** The
  brief's proposed fix — *"drive the art's extent from the door's own outline, `z_bot(x)`"* — **is
  already what happens.** Nothing needs building for it.
* **And that is the problem.** `door_pv` normalises over the panel height, so it is a **stretch**
  map. Re-pointing the parse moves a fixed `v` by **309.1 mm** at the front corner: the one option
  the owner rejected.
* **The added depth is two corner lobes, not a band.** §10.100.4's `z_bot` reproduces to 0.1 mm —
  **272.2 mm rear, 387.5 mm front, crown 0.8033** — but only **1.8 mm** over the front wheel arch. A
  re-point therefore **shears** the art: **+59.7 % rear, +84.2 % front, +0.4 % at the crown.** The
  brief's *"right at one corner and 115 mm wrong at the other"* understates it.

**So the job is: make `door_pv` belt-anchored and metric, and GROW the inventory to fill two corner
lobes.** A drawing job, not a constant change.

### Item 3 Action 0 — the 56 % is NOT inflated by the inner skin, and the probe already proved it

The brief's premise: the shell is solidified to 2.8 mm, the probe splits on the sign of POSITION, so
*"the inner skin is counted in the 56 %"* — decompose it before sizing the job.

**It is counted, and it contributes nothing.** `probe_rev42_uv`'s own sweep, stated before the run
and printed on every run:

```
    TOL_M    1.0 mm  ->  59.28 %
    TOL_M   20.0 mm  ->  59.28 %
```

**Identical.** `TOL_M` is how far apart two positions must be to count as different places. The
inner skin sits **2.8 mm** from its outer twin — *between* those two bounds. If inner-skin
duplication were driving the count, moving the threshold across 2.8 mm would move the number. **It
does not move at all.** The collisions are driven by separations far larger than the shell is thick.

The inner skin does enter the **painted-area denominator**, so if anything the visible-surface figure
is **worse** than 56 %, not better. **Either way the brief's worry is refuted and the job is as big
as it looks.**

### Item 1's typography — both downgraded severity-5s REFUTED, window re-derived

`AUDIT_rev43.md` §0's retraction produced the rule: *an adversarial verifier must re-derive the
WINDOW, not only the method.* `probe_rev44_typo` applies it — **by having no window at all.** Every
statement is a connected-component or topological property of the whole mask.

* **"The capital `S` is in three fragments" — TRUE, AND TRUE OF THE PHOTOGRAPH.** Three pieces
  measured, three generated. `senor_trace.py`'s own docstring says it reproduces those breaks
  deliberately: the spine drops below the chromaticity threshold under tarnish, and bridging it
  *"would be inventing ink the photograph does not show"*. **A faithful copy of a photographic
  artefact is not a generator defect. REFUTED as a defect.**
* **"The `e`'s bowl and eye are gone" — REFUTED on topology.** The `e`-bearing component carries
  **two holes in the photograph and two in the generator**, same component, same place.
* The published decomposition reproduces exactly: **934 ink px, 6 components, 252/332/16/258/61/15.**

---

## CLASS 4 — UNINSTRUMENTED REQUIREMENTS. No probe exists, so "green" is meaningless here.

| requirement | source | instrument |
|---|---|---|
| "No floating or intersecting artifacts" | SPEC §5 bullet 1 | **none** |
| "Crisp, regular quad topology; no n-gon pinching on the nose" | SPEC §5 bullet 2 | **none** — 4617 body ngons at SUB=1 counted, not gated |
| "Correctly oriented, correct handedness" decals | SPEC §5 bullet 4 | **none** |
| Absolute replication of all eight artwork elements | SPEC §10.10 | **none** — the scope table is prose and 17 revisions stale. §10.10 does carry source-crop rectangles; what it lacks is **acceptance thresholds**. The de-facto template is **§10.68**. |
| "The owner recognises his own vehicle" | SPEC §10.10 | **none, and probably uninstrumentable** |
| The emotional bar of the Playa hero | §7.4 | **none** |
| The die-cut sticker | §7.3 | **none — no code, no asset, nothing on disk** |

**AND ONE CORRECTION TO THE BRIEF ABOUT THAT LAST ROW.** The rev-44 brief says *"THE DESIGN LANE
NEVER RAN … the sticker's art direction spec is still owed."* **It ran, and the spec is not owed.**
`AUDIT_rev43.md` records a **DESIGN lane of 23 findings**, and its §5 gives a full **STICKER — the
die-cut vinyl sticker (art direction specification)** dimension: viewpoint (18° front three-quarter,
eye height 1.55 m), the cab-door owner question, the flank triptych, the sacrifice rule (48 of 66
gold components), the die-cut path (0.159 m minimum feature), line weight (0.15 mm floor), the sun,
and colour separation (one 70° hue wedge plus four neutrals). The brief's own §6.1 says *"both
lanes"* one paragraph earlier. **What is missing is the ASSET, not the specification.**

---

## CAVEAT ON THIS WHOLE LEDGER

Every figure above was watched print on **this** machine. `download.blender.org` returns **403**
here, re-tested at rev 44; `WebFetch` and `curl` are egress-blocked for every domain tried.
**`WebSearch` works** — which is new, rev 43 had no egress at all — but it returns text, not images,
so the photographs remain the owner's to fetch. `probe_rev42_uv`'s **56.15 %** is the one place a
published figure does not reproduce, and rev 44 reproduced the *discrepancy* rather than resolving
it: it is stable, not noisy, and settling it needs a real Blender binary this environment cannot
reach.
