# NEXT CONTEXT PROMPT — rev 25

Please act as my expert. Continue the Señor Tacombi combi build. **Twenty-four
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 1 — read my memory BEFORE you read any code

`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17`, `-rev18`, `-rev19`,
`-rev20`, `-rev21`, `-rev22`, `-rev23`, then **`/areas/tacombi-combi-3d-rev24.md`**
(these are SEPARATE FILES; each revision's file does NOT carry the next), then
`/areas/tacombi-combi-sticker.md`, then `/preferences.md`. Five prior contexts
skipped them; one cost half a day and produced the wrong body type. If you
cannot read them, say so explicitly rather than quietly proceeding.

**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner, the person this is for. **Do not ask me what the
real vehicle looks like.** Ask me what a PHOTOGRAPH shows — that has now paid
off fourteen times — but measure the surface, never ask about it.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)

See §1 below. **TWELVE bundle lines now, and the rev14b line is a `fetch`.**
rev 18 opened with rev 17 missing and rev 19 with rev 18 missing; **rev 20, 21,
22, 23 and 24 all opened CLEAN** — do not assume either way, check.

## Step 3 — install Blender 4.5.3 and run BOTH guards before proposing anything

```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
/tmp/blender/4.5/python/bin/python3.11 -m pip install pillow scipy
```

That pip line is required. Guards are `T1_SUB=n T1_VERIFY=1 blender -b
--python build.py` and `T1_SUB=n blender -b --python audit.py`. Report the
guards' ACTUAL output. Both levels. **`audit.py` rewrites `STATE.md` every run
but only its provenance rows — `git checkout STATE.md` after.**

**THE GUARDS ARE 0 fail / 0 WARN.** That is still NOT an improvement in the
model — rev 22 RETIRED the test that produced the warn, and **rev 24 moved NO
GEOMETRY AT ALL.** Read §10.59.

## Step 4 — read, in this order

`STATE.md` → `SPEC.md` §10, then §10.9 through §10.67 → this file →
**`HANDOFF_rev24.md`** → `HANDOFF_rev23.md` → `HANDOFF_rev22.md` →
`HANDOFF_rev21.md` → `HANDOFF_rev20.md` → `HANDOFF_rev19.md` →
`AUDIT_rev18_loft.md` → `HANDOFF_rev18.md` → `LOFT_GROUND_rev15.md` →
`AUDIT_rev12.md` → `REF_MEASUREMENTS.md`.

`STATE.md` is machine-written by `audit.py`. **If it and any prose disagree, it
is right.** It has no known phantoms.

**Retirements that touch many numbers:** §10.11 (ground line, ~70 mm) and
§10.34 (hub chain, ~29 mm) and §10.29's ONE REF-wide correction (`:899`).
§10.46 corrects §10.37; **§10.45–48 retire NO §10.34 claim.** §10.57 retires
rev 20's boxes A and B. §10.59 RETIRES `H_ROOF`. §10.61 corrects the crossing
count. §10.62 ARMS item 4. §10.63 finds `folk_gen`'s bake frame stale.
**§10.65–67 are rev 24's: §10.65 finds `solve_ctan` measured THE WHOLE SCENE
through a top-only mask; §10.66 finds rev 23 BROKE `folk_gen.composition()`;
§10.67 REFUTES rev 24's own work-item-2 brief and arms the guard that can
actually see §10.64's defect class.**

## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them

This has now paid off fourteen times. **My answers are not infallible — ask me
anyway, then measure what I say.** Show me a crop, mark the regions, give me
options, and **print the crop box**. rev 14's box was 120 px off; rev 19's
straddled a dark roof opening; rev 20's A and B straddled TWO MATERIALS; rev
21's redrawn N1 STILL straddled two materials; rev 22 found SPEC's OWN FOUNDING
CROP for `COUNTERTAN` straddling the counter top and the brass nosing; rev 23's
first draft of its own question figure straddled the A-pillar and the windscreen
aperture and was thrown away rather than sent.

**A CLASS GATE IS A PROBE TOO, and so is a BRIEF, a TARGET, a SUBAGENT'S
FINDING, a CITATION, and a GUARD YOU JUST WROTE.** Three of rev 17's four items
came back with their briefs refuted; rev 19's single item came back refuted
three ways; rev 21 refuted all FIVE routes to its own headline; rev 22 refuted
its OWN item-3 target; rev 23 refuted TWO claims in its own briefing;
**rev 24 REFUTED ITS OWN WORK ITEM 2 OUTRIGHT, and its new guard was wrong
TWICE — producing 4 false positives out of 8 — before it was right.**

## Step 6 — the work

§6 below is the ordered list. **The loft is DONE and AUDITED. The arch is FIXED.
`H_ROOF` is RETIRED. `CREAM` is UNCHANGED. ITEM 4 IS ARMED and the show flank is
at 0.0 mm. `COUNTERTAN`'s pedestal is DOWN from ~69 % to ~59 % and is STILL
UNIDENTIFIED. `folk_gen.composition()` RUNS AGAIN. THE HERO IS THE OLDEST
UNDONE ITEM — nothing has photographed the current mesh since rev 22, and the
geometry moved in rev 23.**

## Step 7 — resolution

rev 22 shipped 4800×3200 in 20 strips, worst seam z 1.91. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips ~6 min each.
**`rev22_hero34f.png` NO LONGER PHOTOGRAPHS THE CURRENT MESH** — rev 23 moved
the cab door and the vent. **rev 24 did not shoot it either, and says so.**
It is item 1.

## How I work

* Ground in the reference → build → adversarial audit → iterate. Never build
  before grounding. Never call it done off self-review.
* Report the measurement against the reference, **with its ceiling**. Never a
  self-assigned score.
* Do not tell me anything is ready. Tell me what is fixed, what is still wrong,
  and what you measured.
* Keep visible cadence on long work and send renders as they land.
* Travel between contexts consciously, every time.

## Already settled — do not re-open without new evidence AND a different method

Tyre OD 0.665 m on 16-inch rims. No rear bumper in service; front bumper cream.
ONE roof opening under the flower-mural lid. The cream "La Santa" panel is a
**DETACHED SIGN** and is **NOT a cream reference**. The counter has a
bare/varnished plywood top with brass nosing. Flank RED sRGB (196,49,36),
**albedo saturation 0.816 LOCKED**. Rake **17.75 mm/m**. Serving bays **EQUAL at
0.5155 m**. `optics-6` CLOSED. `materials-5` CLOSED. Tail lamp **round**.
Windscreen **split, two panes**. **The cab door glass is DIVIDED into a vent
wing plus a main pane.** Nolita admissible **FOR GEOMETRY ONLY**, every such
number TAGGED. SPEC §6's pure-white backdrop lock **RETIRED**. `W_ALBEDO`
**CLOSED for good**. `ref_side.jpg` is the **worst frame**. Hubcap ring
**0.093 ± 0.012**. `vw_bars`' air gap **never existed**. The rear arch **holds
its crown**, tyre gap **39.7 mm**. px/m on `ref_rear34.jpg`'s **plate plane** is
**344.1 ± 6.7**; the cream's flank plane is **337 ± 7**, a BRACKET. The shipped
mottle arm is dC\* **0.220/0.227/0.231**; **the cream map's chroma is NOT short**.
N2/N3 are **white paper napkins**; **N1 STRADDLES two materials**; M1 is **bare
stainless**; rev 20's C/D/E are **inside the galley**; `ref_rear34`'s red is
**+31 sd** from the locked albedo, so **no neutral transform relates that frame
to the locked constants**; **`CREAM` UNCHANGED at (206,208,200)**.
**`H_ROOF = 1.960` is RETIRED as an accuracy target** and must not be re-added;
the probe is a LABELLED regression catcher at baseline **1.9835, band ±5 mm**,
and **the band must never be widened**. **The absolute roof height is OPEN.**
**`COUNTERTAN` UNCHANGED** — hue disagreement **≤3°**; its cab-roof reference arm
is **INADMISSIBLE**. The shut-line × aperture invariant is **TOPOLOGICAL**. The
**SHOW flank is armed at ZERO and is at 0.0 mm**; the **OFF flank is a LABELLED
regression catcher at 804.9 mm ± 10 mm and must NOT be tightened to zero.**
**`B_PILLAR = 0.0120` and `VENT_TOP_DROP = 0.0280` are AUTHORED.**
**`folk_gen`'s constants are PARSED and the parse RAISES — never re-type them.**
**The committed `tex/*.png` were baked in the STALE frame.**

**NEW, rev 24 and now settled:**
**`solve_ctan`'s measured frame is ISOLATED now** — do not remove `_only`;
`T1_CTAN_NOISOLATE=1` reproduces the old contaminated arm.
**Every absolute linear figure in SPEC §10.56 is a THREE-STACKED-RIG number**
(`ST.lighting()` stacks 8 lights per call and nothing removes them); the ratio
is comparable across rig counts, **the level is not**.
**`COUNTERTAN`'s albedo sensitivity `k` is 40 % LARGER than believed** — any
future solve must re-derive, never carry the old secant gain.
**§0.2 is NOT self-arming and never was** — it compares MATERIAL NAMES.
`_retired_value_drift()` is the mechanism that sees retired VALUES; **never
widen it or add exemption tokens to silence it.**
Never correct this vehicle toward the VW factory catalogue.

## Hard-won rules — every one was learned by breaking it

* Never set a vertical position from the ground line (~70 mm common-mode) — the
  HUB-referenced chain has the same disease at ~29 mm.
* A single linear px→metre scale does not hold along the flank; the map is
  projective. **And a scale measured on one plane is not the scale on another.**
* **An image slope of a fore-aft line is not a rake** — that cost five revisions.
* A rendered ratio is only an albedo ratio between two surfaces of the **same
  class** under the same light.
* **AN OBSERVED PIXEL IS NOT AN ALBEDO.**
* **IF TWO REFERENCE SURFACES ARE CLAIMED TO SHARE A LIGHT, TEST IT.**
* A constant tuned against another constant must be expressed in terms of it.
* **A claim in prose is not a guard — INCLUDING WHEN THE PROSE IS INSIDE THE
  GUARD.** rev 24's work item 2 was briefed off a comment, sitting above the ban
  it described, asserting the list was "DERIVED from §0.2" when it is a
  hand-written dict. Grep for the node that does it. *(EXTENDED, rev 24)*
* **A MASK IS NOT A MEASUREMENT UNTIL THE MEASURED FRAME IS ISOLATED TOO.**
  `solve_ctan` isolated its mask and rendered the whole scene; a third of the
  mask was other objects for four revisions. **Isolate BOTH.** *(NEW, rev 24)*
* **CHECK WHETHER YOUR INSTRUMENT'S LIGHT RIG IS THE ONE YOU THINK.**
  `ST.lighting()` STACKS — 8 / 16 / 24 — so a probe that calls it three times
  measures a scene lit three times over. Absolute levels from any such probe are
  not comparable across probes. *(NEW, rev 24)*
* **AN INFERENCE THAT LOOKS LIKE A CORRECTION IS STILL AN INFERENCE.** Correcting
  occlusion by arithmetic assumes the occluders do not respond to the variable
  being ablated. They sit on the surface and catch its bounce. **Re-run both
  arms.** *(NEW, rev 24)*
* **A GUARD THAT IS RIGHT FOR THE WRONG REASON IS NOT A GUARD.** rev 24's new
  guard caught a real stale line at `SPEC.md:2701` — by accident, because a
  sub-heading reset its section exemption. Fixed the tracking, fixed the line by
  hand, and recorded both. *(NEW, rev 24)*
* **ADDING TO A SECTION CAN SILENTLY DISABLE THE GUARD THAT WATCHES IT.**
  `### 0.2b` contains `## 0.2` as a substring, so the drift guard's split went
  back to reading 16 bullets of 29 and printed a reassuring `16`. **Watch the
  count print.** *(NEW, rev 24)*
* **AN ARC LENGTH IS NOT A PENETRATION DEPTH.** Ask what a statistic MEASURES
  before you guard on it.
* **DO NOT INHERIT A GUARD'S RATIONALE ALONG WITH ITS SHAPE.**
* **DO NOT ARM A GUARD AT ZERO AGAINST GEOMETRY NOBODY HAS PHOTOGRAPHED.**
* **A RAY-VISIBILITY FLAG IS NOT AN ABLATION.** Remove the ALBEDO.
* **Build the CONTROL first and prove it is a no-op, then run the experiment —
  and CHECK THE CONTROL ITSELF.** Three consecutive revisions where the control
  or the probe was the bug; rev 24's first dynamic probe of `composition()` was
  ill-posed and proved nothing, and the AST proof replaced it.
* **AN ILLUMINANT REFERENCE MUST CARRY SUBSTANTIAL ALBEDO IN ALL THREE
  CHANNELS.**
* **BEFORE DE-ILLUMINATING ANYTHING, TEST WHETHER A NEUTRAL TRANSFORM CAN RELATE
  THE TWO FRAMES AT ALL.**
* **A SUBAGENT'S FINDING IS A CLAIM, NOT A MEASUREMENT.** rev 24 ran three and
  verified every load-bearing claim by hand; **the ones it could not verify are
  labelled UNVERIFIED in the handoff rather than reported as findings.**
* **A CARRIED-FORWARD FIGURE IS A CLAIM TOO — AND SO IS ITS CITATION.**
* **IF A DERIVED CONSTANT IS YOUR FALSIFICATION LEVER, WORK OUT WHAT VALUE
  REPRODUCES THE OLD STATE.**
* **WHEN TWO ROWS OF A MEASUREMENT AGREE EXACTLY, SUSPECT A BUG — THEN CHECK.**
* **MEASURE THE PSF BEFORE QUOTING ANYTHING NEAR THE LIMIT**, and **sweep the
  threshold rather than picking one**.
* **A negative control turns a number into a measurement.**
* **Before scheduling a solve, ABLATE THE CONSTANT TO ZERO.**
* **CLIPPING DESTROYS TEXTURE.** rev 24 reproduced this exactly: at 70 % clipped
  the radiance shares collapsed onto the pixel shares.
* **An ORTHO render has an EXACT px/m.**
* **A restore check that only greps THIS revision's strings cannot detect a lost
  ANCESTOR** — and **AN ANCESTOR CHECK IS ONLY AS GOOD AS THE NEWEST COMMIT IN
  IT. Both checks must reach the tip.**
* **Do not put a figure in an acceptance test — or a HANDOFF — unless you
  watched it print.**
* **If a change trips a guard, THAT IS THE GUARD WORKING. Never widen it.**
  rev 24 tripped its OWN clipping guard and fixed the cause — which is how the
  stacked light rig was found.
* **A probe that cannot answer must return None, not an endpoint.**
* When a finding breaks something independently locked, measure it a third way.
* **Watch for the lamppost** — `ref_side.jpg` columns 62–79 have produced four
  confident wrong numbers about the front of the vehicle.
* A single shell command is killed at 10 minutes. This box has 2 cores — spawn
  3–4 `Agent`s on **disjoint files**, read-only for audits, rather than a
  Workflow.
* **Backticks in `git commit -m` hit shell substitution.** Use `git commit -F`.
* **The device bridge may drop mid-transfer.** Try the direct call FIRST — rev
  24 moved twelve bundles in ONE call — and fall back to `split` + parallel
  single-file calls + **md5 against my disk** only on failure. `device_bash`
  cannot `rm`.

---

> **THE STANDARD, in the owner's words, and it governs every line below.**
> The final product should be nearly indistinguishable from the original.
> **Any single measurement off is unacceptable.** We are recreating a photo
> realistic version of **that exact bus**. The criterion is PER-MEASUREMENT.
>
> And above clinical accuracy: *"I really want this to give the person the
> opportunity to feel like they were on Playa del Carmen all those years ago.
> I want the owner to remember standing in the kombi, in this very picture
> that was provided."* — **that owner is the restaurant's owner, not me.**

---

## 1. Restore and verify — BY CONTENT, never by hash or commit count

```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull --ff-only ../tacombi_rev14_unified.bundle HEAD          # -> 59
git fetch ../tacombi_rev14b_incremental.bundle HEAD:refs/heads/b14   # FETCH
git pull --ff-only ../tacombi_rev15_incremental.bundle HEAD      # -> 67
git pull --ff-only ../tacombi_rev16_incremental.bundle HEAD      # -> 71
git pull --ff-only ../tacombi_rev17_incremental.bundle HEAD      # -> 75
git pull --ff-only ../tacombi_rev18_incremental.bundle HEAD      # -> 81
git pull --ff-only ../tacombi_rev19_incremental.bundle HEAD      # -> 87
git pull --ff-only ../tacombi_rev20_incremental.bundle HEAD      # -> 93
git pull --ff-only ../tacombi_rev21_incremental.bundle HEAD      # -> 96
git pull --ff-only ../tacombi_rev22_incremental.bundle HEAD      # -> 101
git pull --ff-only ../tacombi_rev23_incremental.bundle HEAD      # -> 105
git pull --ff-only ../tacombi_rev24_incremental.bundle HEAD      # -> see §7
```

**If a pull says "Need to specify how to reconcile divergent branches", STOP.**

Content checks — **the first eight reach the TIP on purpose**:

```bash
git status                                              # clean
grep -c '### 10.65' SPEC.md                             # 1   rev 24
grep -c '### 10.66' SPEC.md                             # 1   rev 24
grep -c '### 10.67' SPEC.md                             # 1   rev 24
grep -c '_retired_value_drift' verify.py                # 3   rev 24
grep -c '_RETIRED_BULLETS_REVIEWED = 29' verify.py      # 1   rev 24
grep -c 'T1_CTAN_NOISOLATE' shader_solve.py             # 2   rev 24
grep -c 'STEP_M' folk_gen.py                            # 5   rev 24
grep -c '0.2b Retired since rev 4' SPEC.md              # 1   rev 24
ls probe_ctan_index.py HANDOFF_rev24.md                 #     rev 24
grep -c '### 10.62' SPEC.md                             # 1   ANCESTOR rev 23
grep -c 'OFF_CROSS_BASELINE' t1_shell.py                # 1   ANCESTOR rev 23
grep -c '_from_module' folk_gen.py                      # 3   ANCESTOR rev 23
grep -c 'H_ROOF_REGRESSION' verify.py                   # 7   ANCESTOR rev 22
grep -c '### 10.57' SPEC.md                             # 1   ANCESTOR rev 21
grep -c 'T1_CTAN_NOBOUNCE' shader_solve.py              # 4   ANCESTOR rev 20
grep -c '_BODY' cream_rms.py                            # 4   ANCESTOR rev 19
grep -c '_arch_lip_z' verify.py                         # 2   ANCESTOR rev 18
grep -c 'matte_tap' studio.py                           # 6   ANCESTOR rev 17
grep -c '_coons_cap' t1_core.py                         # 3   ANCESTOR rev 16
grep -c 'The threshold is not the parameter' post.py    # 1   ANCESTOR rev 13
```

**EVERY ONE OF THESE WAS READ OFF A FRESH-CLONE VERIFICATION RUN.** See §7.

Ancestry:

```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```

**Known limitation, stated rather than hidden:** the ancestry loop's newest
entry is a rev-19 commit, because a hash cannot be written into the file that
contains it without amending, and rev 14 learned not to amend. **The TIP is
covered by the eight rev-24 content greps instead.**

## 2. Both guards, and the figures I watched print

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 0 warn** | **0 fail, 0 warn** |
| roof crown @ rear axle | **1.9835** (baseline 1.9835, −0.0 mm) | **1.9833** (−0.2 mm) |
| rear arch lip → gap | **0.3722 → 39.7 mm** | same |
| front arch (control) | **0.3732 → 40.7 mm** | same |
| rake | **17.75 mm/m (locked 17.75)** | same |
| dome deficit / rear overhang | +0 / **0.7730** | same |
| dims | L=4.065 W=1.750 | same |
| cut roof hole | **68564v** | **252749v** |
| objects at `materials:` | **126** | **126** |
| shut line × aperture, SHOW | **0.0 mm** | **0.0 mm** |
| shut line × aperture, OFF | **804.9 mm** (baseline 804.9, −0.0) | same |
| `CARGO_GAP` samples | **154** | same |

Also: **185 meshes**; 42 materials; 5 constant-rough; **0 non-manifold**; three
open apertures on +Y; four shut lines 100 % open; band 1.372–1.775; bay widths
**0.516 0.515 0.516**.

**EVERY FIGURE IS IDENTICAL TO REV 23's. NO GEOMETRY MOVED IN REV 24.**

## 3. What rev 24 changed — `HANDOFF_rev24.md` has the full account

- **`shader_solve.py`** — `solve_ctan`'s MEASURED frame is now isolated with
  `_only` (rev 15's own rule, never propagated); the light rig is purged before
  each setup because `ST.lighting()` STACKS. `T1_CTAN_NOISOLATE=1` reproduces
  the old arm.
- **`verify.py`** — `_retired_value_drift()`, a FAIL-level guard on retired
  values republished unstruck in the FROZEN front matter; the false
  "self-arming" comment corrected; `_retired_section_drift`'s substring parse
  made line-anchored; `_RETIRED_BULLETS_REVIEWED` 16 → 29.
- **`folk_gen.py`** — `composition()`'s `NameError` repaired, value-preserving.
- **`SPEC.md`** — §10.65, §10.66, §10.67, §0.2b, the change log, and four
  retired values struck in FROZEN sections (§1.1 ×2, §3, §10.9).
- **`probe_ctan_index.py`** — NEW, read-only.
- **`CREAM`, `COUNTERTAN`, `RED`, the rake, the roof and ALL GEOMETRY UNCHANGED.**

**Things you must not silently undo — `HANDOFF_rev24.md` §4**, and rev 23's §4,
rev 22's §3, rev 21's §4, rev 20's §4, rev 19's §4 and rev 18's §4 all still
stand in full.

## 4. Still open

See `HANDOFF_rev24.md` §5 for the full list. The ones that matter:

- **THE HERO — nothing has photographed the current mesh since rev 22, and the
  geometry moved in rev 23. rev 24 did not shoot it. It is item 1.**
- **`CREAM`** — needs a same-light, same-CLASS, three-channel reference. **Does
  not exist in the three photographs.**
- **THE ABSOLUTE ROOF HEIGHT** — 1.960 retired, nothing replaced it.
- **`COUNTERTAN`'s ~59 % pedestal** — down from ~69 %, occlusion now excluded
  alongside dust, wear, fade, coat+spec and interreflection. **STILL
  UNIDENTIFIED.** `k` is 40 % larger than believed — re-derive, never carry the
  old secant gain.
- **THE OFF FLANK** — two mutually contradictory **E** features, 804.9 mm.
- **`_ZB_AUTH` and `DOOR_X0` in `folk_gen.py`** — reported by a read-only agent,
  **UNVERIFIED BY ME**, labelled as claims. `_ZB_AUTH` may carry up to 76 mm of
  z error at the tail from the pre-rev-16 frame, which would be **larger than
  `DOOR_X0`** and would dominate the re-bake decision. **Verify first.**
- **~12 further §10.64-class defects** reported in §1, §2, §3, §6, §10.5, §10.7.
  **I verified five and fixed four; the rest are UNVERIFIED CLAIMS.** Each
  becomes a permanent guard by adding one row to `verify._RETIRED_VALUES`.
- `PLATE_W = 0.3300` has no provenance. `probe_rev16.py:90` prints `xa` vs `xa`.

## 5. FIRST QUESTION FOR THE OWNER

**No decision is outstanding with me.** rev 24 asked no photograph question — it
was a measurement and hygiene revision and had none that a photograph could
answer.

What would move the most is still one photograph: **a head-on rear (or front)
elevation from roof height or above, with the counter and the lids clear of the
section.** It is the only realistic route to closing **BOTH** `CREAM` **and**
the absolute roof height. A clear view of the **off flank** would additionally
close 804.9 mm of unadjudicated crossing.

## 6. Ordered work list for rev 25

1. **A hero at 4800×3200.** Oldest undone item; nothing has photographed the
   current mesh since rev 22 and the geometry moved in rev 23.
2. **Verify the `_ZB_AUTH` claim**, then decide WITH MEASUREMENT whether a
   re-bake is owed under §10.10. `composition()` runs again as of rev 24.
3. **Extend `_RETIRED_VALUES`** with the remaining §10.64-class defects, one
   VERIFIED row at a time.
4. **`COUNTERTAN`'s ~59 % pedestal** — name the next suspect and ablate it.
5. Tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
6. Camera absolutely last.

## 7. THE COMMIT COUNT AND THE CONTENT FIGURES

This section is written LAST, after the final commit, and every figure in §1 was
read off a fresh-clone verification run rather than typed from memory. **This has
gone wrong in ELEVEN consecutive revisions during handoff assembly** — a
truncated console tail, a stale hash, five wrong counts, a `grep -c` that
counted LINES rather than occurrences, and a check string that did not exist.
rev 23 was the first clean run in five.

**Final state: see the figure below** — read off the fresh-clone verification,
plus the commit that writes this paragraph. The bundle was re-cut and
re-verified from a fresh clone AFTER that commit. Treat the count as a
regression catcher only; **verify by content.**

**FINAL COUNT: 107 commits, clean tree.**
