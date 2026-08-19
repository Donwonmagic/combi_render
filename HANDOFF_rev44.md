# HANDOFF — rev 44

**Read `LEDGER_rev44.md` first.** It is the spine and it supersedes `LEDGER_rev43.md`. This file is
the narrative: what rev 44 ran, what it corrected, and what it could not reach.

---

## 0. THE TREE WAS NOT THE TREE THE BRIEF DESCRIBED

**Three things were wrong before a single measurement was taken, and the first one would have wasted
the whole revision.**

1. **`LEDGER_rev43.md`, `AUDIT_rev43.md`, `PLAN_rev43_item1.md` and `HANDOFF_rev43.md` were NOT ON
   THE BRANCH.** The rev-44 brief is built on all four. They lived on
   `origin/claude/combi-render-pickup-4qohx9`; the working branch was cut from the rev-42 lineage
   plus two brief commits. `verify_clone.sh` said so in its own success banner — *"This tree is the
   rev-42 state"* — while passing. **Fixed by a clean fast-forward:** 0 commits unique to the working
   branch, 6 ahead on rev 43's. No merge, no conflict, no history rewritten.
2. **`./verify_clone.sh` does not print `ALL 66 PASS` on a fresh clone.** It prints **65 PASSED, 1
   FAILED** and **exits 1**. The clone is **shallow** — 50 commits against the ≥227 it requires.
   `git fetch --unshallow` and it is 66. A hint is now in the script; **the check was not touched.**
3. **Not a Mac.** Linux x86_64, 4 cores — the same platform rev 43 hit, and the brief warned not to
   assume either. `download.blender.org` is **still 403**, re-tested. The PyPI-`bpy` route works and
   the recipe now lives in `START_HERE.md` instead of in a brief nobody will read again.

---

## 1. THE ADVERSARY PAID FOR ITSELF A THIRD TIME

One agent, pointed at the brief and told to refute it, returned **19 refutations**. The five that
changed what rev 44 did:

| the brief said | the machine says |
|---|---|
| "THE DESIGN LANE NEVER RAN … the sticker's art direction spec is still owed" | **It ran.** `AUDIT_rev43.md` records a DESIGN lane of **23** findings and a full STICKER art-direction dimension. The brief's own §6.1 says *"both lanes"* one paragraph earlier. **The ASSET is missing, not the specification.** |
| "**119** findings sit unverified" | **89.** The other 30 are the FIDELITY half of the same 60 already verified, title for title. 119 double-counts. |
| "Highest-severity **unverified**, both ordinal, both roof" | Both sit in `AUDIT_rev43.md` §2 among the **55 that survived two refuters**. Inherited verbatim from `HANDOFF_rev43.md`, which was committed *before* the audit landed. |
| "**seven** probes carry KILL controls" | **Eight.** |
| "All **31** probes reproduce … use the ledger's table rather than re-deriving" | 31 existed; **the ledger's tables name 20.** Rev 44 ran the other eleven and classified them. |

It also caught that the brief silently changed *"the workshop **script** is 210×140 px"* into *"the
workshop **view** is foreshortened at 210×140"*. The frames are **1200×824** and **1024×768**; those
figures are the SCRIPT CROPS. Corrected in SPEC §7.3.

---

## 2. THE OWNER ANSWERED FOUR QUESTIONS, AND ONE OF THEM WAS AN OFFER

1. **Door art: EXTEND at drawn scale**, do not stretch.
2. **`ref_nolita_doorshut.jpg` is the SAME VEHICLE** as `ref_side.jpg`. §7's standing *"whether it is
   physically the same vehicle is U"* is answered after 29 revisions. **Rev 43's corroboration of
   §10.100's door outline stands** — the other answer would have evaporated it.
3. **Finding 22's scoping SANCTIONED:** letterform geometry admissible from `ref_workshop.jpg`,
   colour and weathering barred.
4. On photographs: *"we can get anything, why don't you give me the links and I will save the photos
   and add them to the repo."* → **`PHOTOS_WANTED_rev44.md`**.

---

## 3. REPORT 3 — THE ORDINAL IS TOPOLOGICAL, AND REV 43'S ARM NEVER DISCRIMINATED

The brief asked for the above/below read off the build's constants — exact, no camera. Done, and it
**overturns the arm rev 43 published**.

* Build: headlamp centre **34.4 mm BELOW** the two-tone break at the lamp's own column.
* Photograph (§10.24's own figure): **131.4 mm BELOW**.
* **Both below.** So rev 43's *"20 px BELOW, 10× the reading uncertainty, STRONG"* is **consistent
  with the build** and is not evidence of the defect. An ordinal comparison of centres cannot
  discriminate here, and it was published as though it could.

**What does discriminate needs no scale at all.** In the build the two-tone line **CUTS ACROSS THE
HEADLAMP APERTURE**: a **131.9 mm chord** over a 172.4 mm lens, **159.9 mm** over the 205.4 mm chrome
ring, the lamp's upper rim standing **51.8 mm ABOVE** the break. In `ref_source.jpeg` the lamp sits
entirely in the red with **12 px of clear red above it**. That is *"the paint job and the headlights
are not alligned"*, exactly as he filed it, and no view or px/m conversion can argue with it.

The break at the lamp is the **V-swage**, not the flank belt — comparing against the belt is a 208 mm
error, armed as C5 and written to fail. **C3 reproduces §10.24's published `belt − 0.242` to 5e-5**,
which is what validates the frame; C4 proves the rake cancels. **C6 is the burn-down gate: it is the
only control in this project that is supposed to change class**, and it goes green when the defect is
fixed. `rev44_report3_lamp.png` is the marked crop.

Rev 43's 20 px gap **reproduces exactly** (137−117). Its absolute rows 120/140 are 3 px low — a
red-threshold difference that leaves the gap untouched.

---

## 4. ITEM 1 — THE RECORD WAS WRONG ABOUT THE MECHANISM, AND THE ONE-LINE FIX IS THE WRONG FIX

* **`DOOR_H` divides nothing, and it is not the v-map.** Two read sites, `folk_gen.py:1274` and
  `:1287`, both `h = sv * DOOR_H`, both **multiplying**, for two motifs. SPEC §10.100.6 **and
  `t1_shell.py:546`** both called it a divisor of *"every v-coordinate of the door art"*. **Both
  corrected.** The brief caught the SPEC one, got the multiplier right, scoped the fix to SPEC — and
  left the identical sentence in the code.
* **The v-map is `door_pv`, and it already drives off the door's own outline per station.** The
  brief's proposed fix — *"drive the art's extent from the door's own outline, `z_bot(x)`"* — **is
  already what happens.** `panel_bot(x) == door_bot_z(x)` inside the door span. Nothing needs
  building for it.
* **And that is the problem.** `door_pv` normalises over the panel height, so it is a **STRETCH**
  map. Re-pointing the art's parse at the wrapped outline moves a fixed `v` by **309.1 mm** at the
  front corner — **the one option the owner rejected.**
* **The added depth is TWO CORNER LOBES, not a band.** §10.100.4's `z_bot` reproduces to 0.1 mm —
  **272.2 mm rear, 387.5 mm front, crown 0.8033** — but only **1.8 mm** over the front wheel arch. A
  re-point therefore **shears** the art: **+59.7 % rear, +84.2 % front, +0.4 % at the crown.** The
  brief's *"right at one corner and 115 mm wrong at the other"* understates it.

**THE JOB, STATED PROPERLY:** make `door_pv` belt-anchored and metric, and **grow the inventory** to
fill two corner lobes. That is a drawing job. It is not a constant change and it is not a re-point.

**AN ESTIMATOR ERROR OF MY OWN, RECORDED NOT REPLACED.** A first cut used *"lowest z near x"* on
`DOOR_GAP_S` — which is the **whole door perimeter**, verticals included — and so read the vertical
edges at the corners and published **252 / 380 mm**. The bottom rail is `DOOR_BOT_RUN`. A first prose
detector also false-positived on `SPEC.md:3254`, where *"divides every u"* belongs to `DOOR_W`.

---

## 5. ITEM 3 ACTION 0 — THE 56 % IS NOT INFLATED BY THE INNER SKIN, AND THE PROBE ALREADY PROVED IT

The brief's premise: the shell is solidified to 2.8 mm, the probe splits on the sign of POSITION, so
*"the inner skin is counted in the 56 %"* — decompose it before sizing the job.

**It is counted, and it contributes nothing.** `probe_rev42_uv`'s own sweep, stated before the run
and printed on every run:

```
    TOL_M    1.0 mm  ->  59.28 %
    TOL_M   20.0 mm  ->  59.28 %
```

`TOL_M` is how far apart two positions must be to count as different places. The inner skin sits
**2.8 mm** from its outer twin — **between those two bounds**. If inner-skin duplication were driving
the count, moving the threshold across 2.8 mm would move the number. **It does not move at all.**

The inner skin does enter the painted-area **denominator**, so if anything the visible-surface figure
is **worse** than 56 %, not better. **Either way the brief's worry is refuted and the job is as big
as it looks.** No new code was needed — the answer was already printing on every run.

---

## 6. BOTH DOWNGRADED TYPOGRAPHY SEVERITY-5s — RE-VERIFIED AND REFUTED

`AUDIT_rev43.md` §0's retraction produced the rule: **an adversarial verifier must re-derive the
WINDOW, not only the method.** `probe_rev44_typo` applies it **by having no window at all** — every
statement is a connected-component or topological property of the whole mask.

* **"The capital `S` is in three fragments" — TRUE, AND TRUE OF THE PHOTOGRAPH.** Three pieces
  measured, three generated. `senor_trace.py`'s **own docstring** says it reproduces those breaks
  deliberately: the spine drops below the chromaticity threshold under tarnish, and bridging it
  *"would be inventing ink the photograph does not show"*. **A faithful copy of a photographic
  artefact is not a generator defect. REFUTED as a defect.**
* **"The `e`'s bowl and eye are gone" — REFUTED on topology.** The `e`-bearing component carries
  **two holes in the photograph and two in the generator**, same component, same place.
* The published decomposition reproduces exactly: **934 ink px, 6 components, 252/332/16/258/61/15.**

**Three new findings fell out of it.** The generator's tilde is **half-weight** (8 px against 16).
`AUDIT_rev43.md` **disagrees with itself** — §0 says the tilde is 16 px, §5's ceiling says **62 px at
7.8σ**, and the only piece near 62 px is the 61 px one that sits **under the S**. And §2 **still
lists the RETRACTED tilde finding among its surviving severity-5s**, so **"55 surviving" over-counts
by one.**

**A FIRST CUT OF THE DIACRITIC TEST WAS WRONG AND IS RECORDED IN THE SOURCE RATHER THAN REPLACED:**
it compared **bounding boxes**, so it could not see a mark floating over *one* letter, and returned
NONE on both masks. **That is the same class of error as the window it was written to avoid.**

---

## 7. FINDINGS 21, 22, 23 — AND ONE RETRACTED IN THE SAME REVISION THAT MADE IT

* **Finding 21 is CLOSED and its premise was FALSE.** §0.2 never retired `ref_source.jpeg` and
  carries no `ref_source` row; §10.22's *"retired in 0.2"* is a mis-citation, struck. **Five ⚠ locks
  are graded M**, i.e. measured from that frame — retiring it would unlock all five. What is real is
  a **resolution** ceiling: 246 × 197 px is ~1 px per 40 mm, which is why `livery-9`'s 32 mm claim
  failed. **The finding was refuted on resolution, not the frame on admissibility.**
* **Finding 23 — and this is the one to read.** Both red-livery frames the project holds ARE
  Mexico-shot: `ref_rear34.jpg` carries a Spanish sign *"FAVOR DE ORDENAR Y PAGAR AQUÍ"*, palms and
  an open-air patio. **The obvious inference from that is wrong, and I shipped it before killing
  it.** §7.2 first read *"so the red livery is Playa-era, and the project holds no Nolita photograph
  of the red bus"*. Published descriptions of the Nolita taqueria put *"a bright red 1963 Volkswagen
  bus … parked between several tables"* with the chalkboard roof — **the red folk-art bus IS the one
  standing in Nolita.** **LIVERY COLOUR IS NOT AN ERA DISCRIMINATOR.** Era is read from the SCENE.
* **Finding 22's scoping sanctioned**, and the 210×140 / 320×110 figures corrected from views to
  script crops.

---

## 8. WHAT THIS ENVIRONMENT CAN AND CANNOT DO — CORRECTED FROM REV 43

Rev 43 recorded that it *"could not fetch images at all — `WebFetch` egress-blocked for every domain,
two scouts, clean null on all five targets"*.

**`WebSearch` WORKS HERE.** `WebFetch` and `curl` do not — 403 through the egress proxy on every
domain tried, including `download.blender.org`, `tacombi.com` and `flickr.com`. **So I can find and
rank links but cannot open one.** Every URL in `PHOTOS_WANTED_rev44.md` is labelled unverified, and
the owner remains the only route to the image files themselves.

---

## 9. WHAT REV 45 SHOULD DO

1. **Item 1, now that it is properly sized.** `door_pv` → belt-anchored and metric; then draw the
   two corner lobes. Read §4 above before touching anything: the one-line fix is the wrong fix.
2. **The 89 in `AUDIT_RECOVERED.md`**, still unverified since a container restart around rev 6.
   **Pipeline verification behind each finder** so a stall cannot strand the lot — that is the
   fourth audit killed before its verify phase.
3. **`AUDIT_rev43.md` §2 needs its retracted row removed** and its 16-vs-62 px disagreement settled.
4. **Report 3's fix**, with `probe_rev44_report3` C6 as the gate.
5. **The photographs**, if he has added any. `PHOTOS_WANTED_rev44.md` says what makes each usable.
6. **The sticker asset** — the specification exists; nothing has ever been drawn.
