# NEXT CONTEXT PROMPT — rev 24
Please act as my expert. Continue the Señor Tacombi combi build. **Twenty-three
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 1 — read my memory BEFORE you read any code
`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17`, `-rev18`, `-rev19`,
`-rev20`, `-rev21`, `-rev22`, then **`/areas/tacombi-combi-3d-rev23.md`** (these
are SEPARATE FILES; each revision's file does NOT carry the next), then
`/areas/tacombi-combi-sticker.md`, then `/preferences.md`. Five prior contexts
skipped them; one cost half a day and produced the wrong body type. If you
cannot read them, say so explicitly rather than quietly proceeding.

**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner, the person this is for. **Do not ask me what the
real vehicle looks like.** Ask me what a PHOTOGRAPH shows — that has now paid
off fourteen times — but measure the surface, never ask about it.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §1 below. **ELEVEN bundle lines now, and the rev14b line is a `fetch`.**
rev 18 opened with rev 17 missing and rev 19 with rev 18 missing; **rev 20, 21,
22 and 23 all opened CLEAN** — do not assume either way, check.

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
model — rev 22 RETIRED the test that produced the warn. Read §10.59.

## Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.64 → this file →
**`HANDOFF_rev23.md`** → `HANDOFF_rev22.md` → `HANDOFF_rev21.md` →
`HANDOFF_rev20.md` → `HANDOFF_rev19.md` → `AUDIT_rev18_loft.md` →
`HANDOFF_rev18.md` → `LOFT_GROUND_rev15.md` → `AUDIT_rev12.md` →
`REF_MEASUREMENTS.md`.

`STATE.md` is machine-written by `audit.py`. **If it and any prose disagree, it
is right.** It has no known phantoms.

**Retirements that touch many numbers:** §10.11 (ground line, ~70 mm) and
§10.34 (hub chain, ~29 mm) and §10.29's ONE REF-wide correction (`:899`, the
100 mm origin error) — **rev 23 refuted the claim, carried by rev 23's own
brief, that §10.29 holds TWO.** §10.46 corrects §10.37; **§10.45–48 retire NO
§10.34 claim — also refuted by rev 23.** §10.57 retires rev 20's boxes A and B.
§10.59 RETIRES `H_ROOF`. §10.60 refutes rev 22's item-3 target. §10.61 corrects
the crossing count. **§10.62–64 are rev 23's: §10.62 ARMS item 4 and finds the
B-pillar had NEGATIVE width; §10.63 finds `folk_gen`'s bake frame built on four
retired numbers; §10.64 finds FOUR retired values still published as "locked"
and THREE broken citations.**

## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them
This has now paid off fourteen times. **My answers are not infallible — ask me
anyway, then measure what I say.** Show me a crop, mark the regions, give me
options, and **print the crop box**. rev 14's box was 120 px off; rev 19's
straddled a dark roof opening; rev 20's A and B straddled TWO MATERIALS; rev
21's redrawn N1 STILL straddled two materials; rev 22 found SPEC's OWN FOUNDING
CROP for `COUNTERTAN` straddling the counter top and the brass nosing;
**rev 23's FIRST DRAFT of its own question figure straddled the A-pillar and
the windscreen aperture and was thrown away rather than sent — fourteenth
instance, and the first caught before it reached me.**

**A CLASS GATE IS A PROBE TOO, and so is a BRIEF, a TARGET, a SUBAGENT'S
FINDING, and a CITATION.** Three of rev 17's four items came back with their
briefs refuted; rev 19's single item came back refuted three ways; rev 21
refuted all FIVE routes to its own headline; rev 22 refuted its OWN item-3
target; **rev 23 refuted TWO claims in its own briefing and found THREE
citations pointing at sections that do not contain the cited text.**

## Step 6 — the work
§6 below is the ordered list. **The loft is DONE and AUDITED. The arch is FIXED.
`H_ROOF` is RETIRED. The cream map is BUILT, WIRED and MEASURED. `CREAM` is
UNCHANGED. ITEM 4 IS ARMED and the show flank is at 0.0 mm. `folk_gen`'s
constants are LIVE. `COUNTERTAN`'s pedestal is the oldest open thread.**

## Step 7 — resolution
rev 22 shipped 4800×3200 in 20 strips, worst seam z 1.91. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips ~6 min each.
**`rev22_hero34f.png` NO LONGER PHOTOGRAPHS THE CURRENT MESH** — rev 23 moved
the cab door and the vent. A fresh hero is item 5.

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
wing plus a main pane** *(NEW, rev 23, from `ref_workshop.jpg`)*. Nolita
admissible **FOR GEOMETRY ONLY**, every such number TAGGED. SPEC §6's
pure-white backdrop lock **RETIRED**. `W_ALBEDO` **CLOSED for good**.
`ref_side.jpg` is the **worst frame**. Hubcap ring **0.093 ± 0.012**.
`vw_bars`' air gap **never existed**. The rear arch **holds its crown**, tyre
gap **39.7 mm**. px/m on `ref_rear34.jpg`'s **plate plane** is **344.1 ± 6.7**;
the cream's flank plane is **337 ± 7**, a BRACKET. The shipped mottle arm is
dC\* **0.220/0.227/0.231**; **the cream map's chroma is NOT short**. N2/N3 are
**white paper napkins**; **N1 STRADDLES two materials — do not use it**; M1 is
**bare stainless**; rev 20's C/D/E are **inside the galley**; `ref_rear34`'s red
is **+31 sd** from the locked albedo, so **no neutral transform relates that
frame to the locked constants**; **`CREAM` UNCHANGED at (206,208,200)**.
**`H_ROOF = 1.960` is RETIRED as an accuracy target** and must not be re-added;
the probe is a LABELLED regression catcher at baseline **1.9835, band ±5 mm**,
and **the band must never be widened**. **The absolute roof height is OPEN.**
**`COUNTERTAN` UNCHANGED** — its hue disagreement is **≤3°**; its cab-roof
reference arm is **INADMISSIBLE** (22 % bluer).
**NEW, rev 23 and now settled:** **the shut-line × aperture invariant is
TOPOLOGICAL** — an aperture cannot extend past the boundary of the panel it is
cut in — and it is **NOT** the arch assert's boolean-collapse rationale, which
does not transfer. **The SHOW flank is armed at ZERO and is at 0.0 mm.** **The
OFF flank is a LABELLED regression catcher at 804.9 mm ± 10 mm and must NOT be
tightened to zero** — both its colliding features are graded **E (never
photographed)** and I could not adjudicate them. **`B_PILLAR = 0.0120` and
`VENT_TOP_DROP = 0.0280` are AUTHORED, not measured; both true values are
OPEN.** **`folk_gen`'s constants are PARSED and the parse RAISES — never
re-type them.** **The committed `tex/*.png` were baked in the STALE frame.**
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
* **A claim in prose is not a guard.** Grep for the node that does it.
* **Check what a guard, a probe, a crop, a CLASS GATE, a BRIEF or a TARGET can
  physically see — including WHICH SURFACE.** Print the crop box.
* **A VERDICT PRINTED AS A CONSTANT STRING IS NOT A MEASUREMENT.**
* **A TARGET IS A PROBE TOO — print the BASE LEVEL of any absolute statistic.**
* **AN ARC LENGTH IS NOT A PENETRATION DEPTH.** rev 23's worst crossing reported
  118.8 mm of arc for a **5.2 mm** overlap — a 23× overstatement, and arming a
  guard on the reported statistic would have chased the wrong number. **Ask what
  the statistic MEASURES before you guard on it.** *(NEW)*
* **DO NOT INHERIT A GUARD'S RATIONALE ALONG WITH ITS SHAPE.** The arch assert
  exists because of a boolean collapse; rev 23's crossings did not threaten the
  boolean at all (0 non-manifold at SUB=2 with all six live). A DIFFERENT
  rationale had to be stated explicitly. *(NEW)*
* **DO NOT ARM A GUARD AT ZERO AGAINST GEOMETRY NOBODY HAS PHOTOGRAPHED.**
  87.7 % of rev 23's crossings were on a flank SPEC itself grades "E (never
  photographed)", between two features that contradict each other. Satisfying
  the guard would have meant INVENTING geometry. Label it and baseline it. *(NEW)*
* **A RAY-VISIBILITY FLAG IS NOT AN ABLATION.** Remove the ALBEDO.
* **Build the CONTROL first and prove it is a no-op, then run the experiment —
  and CHECK THE CONTROL ITSELF.** rev 23's first negative control was ill-posed
  ("an outline is not inside itself" puts every sample ON the boundary) and
  fired immediately. Second consecutive revision where the control was the bug.
* **AN ILLUMINANT REFERENCE MUST CARRY SUBSTANTIAL ALBEDO IN ALL THREE
  CHANNELS.**
* **BEFORE DE-ILLUMINATING ANYTHING, TEST WHETHER A NEUTRAL TRANSFORM CAN RELATE
  THE TWO FRAMES AT ALL.**
* **A SUBAGENT'S FINDING IS A CLAIM, NOT A MEASUREMENT.** rev 23's agent was
  right twice and I checked both before reporting.
* **A CARRIED-FORWARD FIGURE IS A CLAIM TOO — AND SO IS ITS CITATION.** rev 23
  found THREE citations pointing at sections that do not contain the cited text,
  including one in the very section written to cure carried-forward claims.
  **Grep the cited section before you trust the citation.** *(NEW)*
* **IF A DERIVED CONSTANT IS YOUR FALSIFICATION LEVER, WORK OUT WHAT VALUE
  REPRODUCES THE OLD STATE.** rev 23 nearly reported a 2.6× phantom because
  `DOOR_REAR_DX` is derived and the obvious lever value overshot. *(NEW)*
* **WHEN TWO ROWS OF A MEASUREMENT AGREE EXACTLY, SUSPECT A BUG — THEN CHECK.**
* **MEASURE THE PSF BEFORE QUOTING ANYTHING NEAR THE LIMIT**, and **sweep the
  threshold rather than picking one**.
* **A negative control turns a number into a measurement.**
* **Before scheduling a solve, ABLATE THE CONSTANT TO ZERO.**
* **CLIPPING DESTROYS TEXTURE.**
* **An ORTHO render has an EXACT px/m.**
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
  23 moved twelve files in TWO calls — and fall back to `split` + parallel
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
git pull --ff-only ../tacombi_rev23_incremental.bundle HEAD      # -> see §7
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**

Content checks — **the first six reach the TIP on purpose**:
```bash
git status                                             # clean
grep -c '### 10.62' SPEC.md                            # 1   rev 23
grep -c '### 10.63' SPEC.md                            # 1   rev 23
grep -c '### 10.64' SPEC.md                            # 1   rev 23
grep -c 'OFF_CROSS_BASELINE' t1_shell.py               # 1   rev 23
grep -c 'VENT_TOP_DROP' t1_shell.py                    # 4   rev 23
grep -c '_from_module' folk_gen.py                     # 3   rev 23
ls probe_cross_anatomy.py HANDOFF_rev23.md             #     rev 23
grep -c '### 10.59' SPEC.md                            # 1   ANCESTOR rev 22
grep -c 'H_ROOF_REGRESSION' verify.py                  # 7   ANCESTOR rev 22
grep -c '### 10.57' SPEC.md                            # 1   ANCESTOR rev 21
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
covered by the six rev-23 content greps instead.**

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
| **cut roof hole** | **68564v** *(rev 22: 68052)* | **252749v** *(252123)* |
| objects at `materials:` | **126** | **126** |
| **shut line × aperture, SHOW** | **0.0 mm** | **0.0 mm** |
| **shut line × aperture, OFF** | **804.9 mm** (baseline 804.9, −0.0) | same |
| **`CARGO_GAP` samples** | **154** *(rev 22: 28)* | same |

Also: **185 meshes**; 42 materials; 5 constant-rough; **0 non-manifold**; three
open apertures on +Y; four shut lines 100 % open; band 1.372–1.775; bay widths
**0.516 0.515 0.516**.

**THE ROOF-HOLE VERTEX COUNT MOVED THIS REVISION** and it is flagged rather than
hidden — the cab door and vent outlines moved and the cargo outline densified.
Everything else is identical to rev 18–22.

## 3. What rev 23 changed — `HANDOFF_rev23.md` has the full account
- **`t1_shell.py`** — item 4's invariant ARMED at import (show flank, zero
  tolerance), the B-pillar and vent-wing geometry FIXED, `CARGO_GAP` densified
  28 → 154 with signed area asserted equal.
- **`verify.py`** — new row 11e2 reporting both flanks, off flank as a LABELLED
  regression catcher.
- **`folk_gen.py`** — four stale constants now parsed with `ast`, parse RAISES;
  the banned flat px/m renamed and scoped.
- **`SPEC.md`** — §10.62, §10.63, §10.64 and the change log.
- **`probe_cross_anatomy.py`** — NEW, read-only.
- **`CREAM`, `COUNTERTAN`, `RED`, the rake and the roof all UNCHANGED.**

**Things you must not silently undo — `HANDOFF_rev23.md` §4**, and rev 22's §3,
rev 21's §4, rev 20's §4, rev 19's §4 and rev 18's §4 all still stand in full.

## 4. Still open
See `HANDOFF_rev23.md` §5 for the full list. The ones that matter:
- **`CREAM`** — needs a same-light, same-CLASS, three-channel reference. **Does
  not exist in the three photographs.**
- **THE ABSOLUTE ROOF HEIGHT** — 1.960 retired, nothing replaced it.
- **THE B-PILLAR'S WIDTH and THE VENT WING'S TOP EDGE** — NEW, both AUTHORED.
- **THE OFF FLANK** — two mutually contradictory **E** features, 804.9 mm.
- **`COUNTERTAN`'s ~69 % pedestal** — UNIDENTIFIED, oldest open thread.
- **The committed artwork was baked in the stale frame**; `folk_gen.DOOR_X0` is
  17.3 mm stale.
- **§0.2 has gained no entry since rev 4/rev 8**, so `verify`'s self-arming
  retired-material guard covers none of §10's retirements. That is the
  structural cause of §10.64.
- `PLATE_W = 0.3300` has no provenance. `probe_rev16.py:90` prints `xa` vs `xa`.

## 5. FIRST QUESTION FOR THE OWNER
**No decision is outstanding with me.** rev 23 asked two photograph questions
and got both answers: the cab door glass IS divided into a vent plus a main
pane; the far flank **could not be resolved** from the workshop frame.

What would move the most is still one photograph: **a head-on rear (or front)
elevation from roof height or above, with the counter and the lids clear of the
section.** It is the only realistic route to closing **BOTH** `CREAM` **and**
the absolute roof height. A clear view of the **off flank** would additionally
close 804.9 mm of unadjudicated crossing.

## 6. Ordered work list for rev 24
1. **`COUNTERTAN`'s pedestal** — the occlusion hypothesis via an object-index
   pass. Fourth revision on the list. NOT the 48-sample per-pixel test (seed
   noise 21.7 % > the effect).
2. **§0.2's retirement list** — add §10's retirements so `verify`'s self-arming
   guard covers them. Cheap, structural, and it is the mechanism that would have
   caught §10.64's four stale "locked" rows automatically.
3. `folk_gen.DOOR_X0` — parse `t1_shell`'s constant graph properly, or state why
   not; then decide WITH MEASUREMENT whether a re-bake is owed under §10.10.
4. The tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
5. **A hero at 4800×3200** — the geometry moved, so `rev22_hero34f.png` no
   longer photographs the current mesh.
6. Camera absolutely last.

## 7. THE COMMIT COUNT AND THE CONTENT FIGURES
This section is written LAST, after the final commit, and every figure in §1 was
read off a fresh-clone verification run rather than typed from memory. **This has
gone wrong in ELEVEN consecutive revisions during handoff assembly** — a
truncated console tail, a stale hash, five wrong counts, a `grep -c` that
counted LINES rather than occurrences, and a check string that did not exist.

**Note on commit 102:** its message names only §10.62, but `git add -A` swept
the §10.63/§10.64 work into the same commit. **Stated rather than amended** —
rev 14 learned not to `--amend` a commit whose `STATE.md` predates the amend.

**AND FOR THE FIRST TIME IN FIVE REVISIONS IT CAUGHT NOTHING — because there was
nothing to catch.** All fifteen content checks in §1 were read off the console
BEFORE being written into this file, not typed from my own edits afterwards. The
fresh-clone verification returned **15/15 exact and 8/8 ancestry** on the first
run. rev 19, 20, 21 and 22 each caught their own violation at this step; rev 23
did not produce one. That is the rule working upstream instead of downstream.

**Final state: 105 commits, clean tree** — 104 at the fresh-clone verification,
plus the commit that writes this paragraph. The bundle was re-cut and
re-verified from a fresh clone AFTER that commit. Treat the count as a
regression catcher only; **verify by content.**
