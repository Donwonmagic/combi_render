# NEXT CONTEXT PROMPT — rev 23
Please act as my expert. Continue the Señor Tacombi combi build. **Twenty-two
revisions sit behind this.** You are picking up mid-stream, not starting.
## Step 1 — read my memory BEFORE you read any code
`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17`, `-rev18`, `-rev19`,
`-rev20`, `-rev21`, then **`/areas/tacombi-combi-3d-rev22.md`** (these are
SEPARATE FILES; each revision's file does NOT carry the next), then
`/areas/tacombi-combi-sticker.md`, then `/preferences.md`. Five prior contexts
skipped them; one cost half a day and produced the wrong body type. If you
cannot read them, say so explicitly rather than quietly proceeding.
**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner, the person this is for. **Do not ask me what the
real vehicle looks like.** Ask me what a PHOTOGRAPH shows — that has now paid
off twelve times — but measure the surface, never ask about it.
## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §1 below. **TEN bundle lines now, and the rev14b line is a `fetch`.**
rev 18 opened with rev 17 missing and rev 19 with rev 18 missing; **rev 20, 21
and 22 all opened CLEAN** — do not assume either way, check.
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
**THE GUARDS ARE NOW 0 fail / 0 WARN.** That is NOT an improvement in the
model — rev 22 RETIRED the test that produced the warn. Read §10.59 before you
read anything into it.
## Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.61 → this file →
**`HANDOFF_rev22.md`** → `HANDOFF_rev21.md` → `HANDOFF_rev20.md` →
`HANDOFF_rev19.md` → `AUDIT_rev18_loft.md` → `HANDOFF_rev18.md` →
`HANDOFF_rev17.md` → `LOFT_GROUND_rev15.md` → `AUDIT_rev12.md` →
`AUDIT_rev11.md` → `REF_MEASUREMENTS.md`.
`STATE.md` is machine-written by `audit.py`. **If it and any prose disagree, it
is right.** It has no known phantoms.
**§10.29 carries two corrections that touch every REF number. §10.45–48 RETIRE
claims in §10.34 and §10.37. §10.57 RETIRES rev 20's account of boxes A and B.
§10.59–61 are rev 22's: §10.59 RETIRES `H_ROOF`, §10.60 REFUTES rev 22's own
item-3 target, and §10.61 CORRECTS §10.45's crossing count and total.**
## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them
This has now paid off twelve times. **My answers are not infallible — ask me
anyway, then measure what I say.** Show me a crop, mark the regions, give me
options, and **print the crop box**. rev 14's box was 120 px off; rev 16's
detector locked onto brass nosing; rev 17 drew two wrong boxes; rev 19's first
region-4 box straddled the dark roof opening; rev 20's A and B straddled TWO
MATERIALS; rev 21's redrawn N1 STILL straddled two materials and I caught it;
**rev 22 found SPEC's OWN FOUNDING CROP for `COUNTERTAN` straddling the counter
top and the brass nosing — thirteenth instance, and nobody had drawn it for me.**
**A CLASS GATE IS A PROBE TOO, and so is a BRIEF, a TARGET, and a SUBAGENT'S
FINDING.** Three of rev 17's four work items came back with their briefs
refuted; two of rev 18's four did; rev 19's single item came back refuted three
ways; rev 20's first item came back with its TARGET refuted; rev 21 refuted all
FIVE routes to its own headline; **rev 22 refuted its OWN item-3 target as a
category error and corrected two figures item 4 had carried for four revisions.**
## Step 6 — the work
§6 below is the ordered list. **The loft is DONE and AUDITED. The arch is FIXED.
The guards are REAL. `H_ROOF` is RETIRED. The cream map is BUILT, WIRED and
MEASURED. `CREAM` is UNCHANGED and §10.57 explains why. Item 4 is GROUNDED but
NOT ARMED and §10.61 has the six pairs.**
## Step 7 — resolution
rev 22 shipped 4800×3200 in 20 strips, worst seam z 1.91. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips ~6 min each.
**A HERO EXISTS AGAIN** — `rev22_hero34f.png` is the first since rev 16 and the
first ever to photograph the arch fix, the hubcap rings and the cream mottle.
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
Windscreen **split, two panes**. Nolita admissible **FOR GEOMETRY ONLY**, every
such number TAGGED. SPEC §6's pure-white backdrop lock **RETIRED**.
`W_ALBEDO` **CLOSED for good**. `ref_side.jpg` is the **worst frame**. Hubcap
ring **0.093 ± 0.012**. `vw_bars`' air gap **never existed**. The rear arch
**holds its crown**, tyre gap **39.7 mm**. px/m on `ref_rear34.jpg`'s **plate
plane** is **344.1 ± 6.7**; the cream's flank plane is **337 ± 7**, a BRACKET.
The shipped mottle arm is dC\* **0.220/0.227/0.231**; **the cream map's chroma
is NOT short**; the BEAUTY arm of `mottle_measure.py` is **100 % clipped**.
N2/N3 are **white paper napkins**; **N1 STRADDLES two materials — do not use
it**; M1 is **bare stainless**; rev 20's C/D/E are **inside the galley**;
`ref_rear34`'s red is **+31 sd** from the locked albedo on §10.12's invariant,
so **no neutral transform relates that frame to the locked constants**;
**`CREAM` UNCHANGED at (206,208,200)**.
**NEW, rev 22 and now settled:** **`H_ROOF = 1.960` is RETIRED as an accuracy
target** and must not be re-added to `SPEC`; the probe is a LABELLED regression
catcher at baseline **1.9835, band ±5 mm**, and **the band must never be
widened**. **The absolute roof height is OPEN and UNMEASURED.**
**`COUNTERTAN` UNCHANGED** — its hue target was an OBSERVED PIXEL against an
ALBEDO; the real disagreement is **≤3°** and saturation is already bracketed.
**`COUNTERTAN`'s cab-roof reference arm is INADMISSIBLE** (22 % bluer in B/R),
so the level bracket's upper end G 0.569 is unsupported. **Item 4 is SIX
crossings, 1065.1 mm, TWO on the show flank** — not five/1209/one.
Never correct this vehicle toward the VW factory catalogue.
## Hard-won rules — every one was learned by breaking it
* Never set a vertical position from the ground line (~70 mm common-mode) — the
  HUB-referenced chain has the same disease at ~29 mm.
* A single linear px→metre scale does not hold along the flank; the map is
  projective. **And a scale measured on one plane is not the scale on another.**
* **An image slope of a fore-aft line is not a rake** — that cost five revisions.
* A rendered ratio is only an albedo ratio between two surfaces of the **same
  class** under the same light.
* **AN OBSERVED PIXEL IS NOT AN ALBEDO. Before comparing a measured colour to a
  locked constant, establish which one each is.** That is what killed rev 22's
  item 3, and it is §10.21 wearing a different hat. *(NEW)*
* **IF TWO REFERENCE SURFACES ARE CLAIMED TO SHARE A LIGHT, TEST IT: their
  observed ratio must equal their albedo ratio.** One line, and it found rev
  22's cab-roof arm 22 % bluer. *(NEW)*
* A constant tuned against another constant must be expressed in terms of it.
* **A claim in prose is not a guard.** Grep for the node that does it.
* **Check what a guard, a probe, a crop, a CLASS GATE, a BRIEF or a TARGET can
  physically see — including WHICH SURFACE.** Print the crop box.
* **A VERDICT PRINTED AS A CONSTANT STRING IS NOT A MEASUREMENT.**
* **A TARGET IS A PROBE TOO — print the BASE LEVEL of any absolute statistic
  before comparing two frames through it.**
* **A RAY-VISIBILITY FLAG IS NOT AN ABLATION.** Remove the ALBEDO.
* **Build the CONTROL first and prove it is a no-op, then run the experiment —
  and CHECK THE CONTROL ITSELF.** rev 22's first control failed because it used
  the wrong reference albedo; the failure was in the control, not the finding.
* **AN ILLUMINANT REFERENCE MUST CARRY SUBSTANTIAL ALBEDO IN ALL THREE
  CHANNELS.**
* **BEFORE DE-ILLUMINATING ANYTHING, TEST WHETHER A NEUTRAL TRANSFORM CAN RELATE
  THE TWO FRAMES AT ALL.** §10.12's (G−B)/(R−B) ratio does it in one line.
* **A SUBAGENT'S FINDING IS A CLAIM, NOT A MEASUREMENT.** Test it before you
  report it.
* **A CARRIED-FORWARD FIGURE IS A CLAIM TOO.** §10.45's "five crossings,
  1209 mm" survived four revisions unreproduced and is really SIX and
  1065.1 mm. Reproduce before you guard against it. *(NEW)*
* **WHEN TWO ROWS OF A MEASUREMENT AGREE EXACTLY, SUSPECT A BUG — THEN CHECK.**
  rev 22's two 402.0 mm rows looked like a defect and are real: both cross a
  bay over its full 403.0 mm height. *(NEW)*
* **MEASURE THE PSF BEFORE QUOTING ANYTHING NEAR THE LIMIT**, and **sweep the
  threshold rather than picking one**.
* **A negative control turns a number into a measurement.**
* **Before scheduling a solve, ABLATE THE CONSTANT TO ZERO — then check the
  ablation is measuring the right STATISTIC.**
* **CLIPPING DESTROYS TEXTURE.** Print the clipped fraction on both sides.
* **An ORTHO render has an EXACT px/m.** **Verify a projection before measuring
  through it.**
* **A restore check that only greps THIS revision's strings cannot detect a lost
  ANCESTOR** — and **AN ANCESTOR CHECK IS ONLY AS GOOD AS THE NEWEST COMMIT IN
  IT. Both checks must reach the tip.**
* **Do not put a figure in an acceptance test — or a HANDOFF — unless you
  watched it print.**
* **If a change trips a guard, THAT IS THE GUARD WORKING. Never widen it.**
* **A probe that cannot answer must return None, not an endpoint.**
* When a finding breaks something independently locked, measure it a third way.
* **Watch for the lamppost** — `ref_side.jpg` columns 62–79 have produced four
  confident wrong numbers about the front of the vehicle.
* A single shell command is killed at 10 minutes. This box has 2 cores — spawn
  3–4 `Agent`s on **disjoint files**, read-only for audits, rather than a
  Workflow.
* **Backticks in `git commit -m` hit shell substitution.** Use `git commit -F`.
* **The device bridge may drop mid-transfer.** Try the direct call FIRST — rev
  22 moved TEN bundles (~28 MB) in ONE call — and fall back to `split` +
  parallel single-file calls + **md5 against my disk** only on failure.
  `device_bash` cannot `rm`.
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
git pull --ff-only ../tacombi_rev22_incremental.bundle HEAD      # -> see §7
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
Content checks — **the first five reach the TIP on purpose**:
```bash
git status                                             # clean
grep -c '### 10.59' SPEC.md                            # 1   rev 22
grep -c '### 10.60' SPEC.md                            # 1   rev 22
grep -c '### 10.61' SPEC.md                            # 1   rev 22
grep -c 'H_ROOF_REGRESSION' verify.py                  # 7   rev 22
ls probe_shutlines.py HANDOFF_rev22.md                 #     rev 22
grep -c '### 10.57' SPEC.md                            # 1   ANCESTOR rev 21
grep -c 'ALL THREE CHANNELS' SPEC.md                   # 1   ANCESTOR rev 21
grep -c 'T1_CTAN_NOBOUNCE' shader_solve.py             # 4   ANCESTOR rev 20
grep -c '_BODY' cream_rms.py                           # 4   ANCESTOR rev 19
grep -c '_arch_lip_z' verify.py                        # 2   ANCESTOR rev 18
grep -c 'matte_tap' studio.py                          # 6   ANCESTOR rev 17
grep -c '_coons_cap' t1_core.py                        # 3   ANCESTOR rev 16
grep -c 'The threshold is not the parameter' post.py   # 1   ANCESTOR rev 13
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
covered by the five rev-22 content greps instead**, which cannot pass on a tree
missing rev 22.
## 2. Both guards, and the figures I watched print
| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 0 warn** | **0 fail, 0 warn** |
| roof crown @ rear axle | **1.9835** (baseline 1.9835, −0.0 mm) | **1.9833** (−0.2 mm) |
| **rear arch lip above hub** | **0.3722 → gap 39.7 mm** | same |
| **front arch (control)** | **0.3732 → gap 40.7 mm** | same |
| **rake** | **17.75 mm/m (locked 17.75)** | same |
| dome deficit / rear overhang | +0 / 0.7730 | same |
| dims | L=4.065 W=1.750 | same |
| cut roof hole | **68052v** | **252123v** |
| objects at `materials:` | **126** | **126** |
Also: **185 meshes**; 42 materials; 5 constant-rough; **0 non-manifold**; three
open apertures on +Y; four shut lines 100 % open; band 1.372–1.775; bay widths
**0.516 0.515 0.516**. Every figure except the roof row is identical to rev 18,
19, 20 and 21.
**THE WARN IS GONE BECAUSE THE TEST WAS WITHDRAWN, NOT BECAUSE THE MODEL
IMPROVED. THE MESH DID NOT MOVE.**
## 3. What rev 22 changed — `HANDOFF_rev22.md` has the full account
- **`verify.py` + `audit.py`** — `H_ROOF` retired, regression catcher armed and
  falsified two ways (§10.59).
- **`SPEC.md`** — §10.59, §10.60, §10.61 and the change log.
- **`probe_shutlines.py`** — NEW, read-only grounding for item 4 (§10.61).
- **`rev22_hero34f.png`** — the hero.
- **No geometry moved. `CREAM`, `COUNTERTAN`, `RED` and the rake all UNCHANGED.**
**Things you must not silently undo — see `HANDOFF_rev22.md` §3**, and rev 21's
§4, rev 20's §4, rev 19's §4 and rev 18's §4 all still stand in full.
## 4. Still open
See `HANDOFF_rev22.md` §4 for the full list. The ones that matter:
- **`CREAM`** — still open, reason understood. Needs a same-light, **same-CLASS**,
  three-channel reference. **Does not exist in the three photographs.**
- **THE ABSOLUTE ROOF HEIGHT** — NEW. 1.960 retired, nothing replaced it.
- **`COUNTERTAN`'s ~69 % pedestal** — UNIDENTIFIED. Occlusion hypothesis needs
  an object-index pass. Its level bracket's UPPER arm is now inadmissible.
- **Item 4's assert, unarmed** — six pairs, 1065.1 mm, two on the show flank.
- **`folk_gen.py`** carries the banned flat px/m at `:1884` AND four stale
  constants.
- SPEC §10.3's table still lists the RETIRED red (196,106,36) as "locked";
  §10.9's table still lists the retired rake 0.0330 and the `Z_BELT0`/`V_APEX0`
  derived from it. `PLATE_W = 0.3300` has no provenance.
- `SPEC.md:1983` still uses **N1**, the crop you refuted, as an arm of route A's
  clipping control. The conclusion survives on N2/N3 alone; the text should drop
  N1.
## 5. FIRST QUESTION FOR THE OWNER
**There is no decision outstanding with you for the first time in six
revisions.** `H_ROOF` is answered and implemented.
What would move the most is still one photograph: **a head-on rear (or front)
elevation from roof height or above, with the counter and the lids clear of the
section.** It is now the only realistic route to closing **BOTH** `CREAM` **and**
the absolute roof height.
## 6. Ordered work list for rev 23
1. **ARM ITEM 4'S ASSERT.** §10.61 has the six pairs and their arc lengths.
   **Expect it to FAIL — that is the guard working; fix the geometry, not the
   threshold.** Note the arch generalisation adds no coverage; the gap is the
   APERTURES. Give `CARGO_GAP` samples on its straight runs (94.8 % of the
   length currently carries 8 of 28 points).
2. **`COUNTERTAN`'s pedestal** — the occlusion hypothesis, via an object-index
   pass. NOT the 48-sample per-pixel test (seed noise 21.7 % > the effect).
3. `folk_gen.py`'s stale constants and its flat px/m — §10.10 makes artwork
   replication a hard bar and the bake frame is built on retired numbers.
4. SPEC hygiene, all cheap and all real: §10.3's retired red still marked
   "locked"; §10.9's retired rake and its derived `Z_BELT0`/`V_APEX0`;
   `SPEC.md:1983`'s use of the refuted N1.
5. The tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
6. Camera absolutely last.
## 7. THE COMMIT COUNT AND THE CONTENT FIGURES
This section is written LAST, after the final commit, and every figure in §1 was
read off a fresh-clone verification run rather than typed from memory. **This has
gone wrong in TEN consecutive revisions during handoff assembly** — a truncated
console tail, a stale hash, five wrong counts, a `grep -c` that counted LINES
rather than occurrences, a check string that did not exist, and **rev 22's own,
below**.
**AND IT CAUGHT ITSELF AGAIN, a TENTH time — this revision, in this file.** I
wrote `grep -c 'H_ROOF_REGRESSION' verify.py  # 6`, typed from my own edits
rather than watched. The fresh-clone verification returned **7** — `grep -c`
counts LINES and the constant appears on seven of them, including the comment
block that documents the band. **The expected value was CORRECTED to 7 from the
verification console, not loosened and not deleted** (unlike rev 21's
`STRADDLING` check, which was genuinely unmatchable and was removed). **Fourth
consecutive revision in which the acceptance-test rule caught its own
violation.**
**Final state: 101 commits, clean tree** — the count was read off the console
after the commit that corrects this section, then the bundle was re-cut and
re-verified from a fresh clone. Treat the count as a regression catcher only;
**verify by content.**
