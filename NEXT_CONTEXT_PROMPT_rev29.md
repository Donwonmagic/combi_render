# NEXT CONTEXT PROMPT — rev 29

Please act as my expert. Continue the Señor Tacombi combi build. **Twenty-eight
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 0 — CHECK A FOLDER IS CONNECTED BEFORE YOU PLAN ANYTHING
**NEW, and rev 28 lost real time to it.** If no folder is connected, the seventeen
bundle files and all three reference photographs are unreachable and every item in §6
is blocked. Call `get_device_info`; if `connectedFolders` is empty, request
`~/Desktop/tacombi_bus_render` immediately and say so plainly. **The dialog can
time out** — rev 28's first request went unanswered and had to be re-sent.

## Step 1 — read my memory BEFORE you read any code
`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17`, `-rev18`, `-rev19`,
`-rev20`, `-rev21`, `-rev22`, `-rev23`, `-rev24`, `-rev25`, `-rev26`, `-rev27`,
then **`/areas/tacombi-combi-3d-rev28.md`** (these are SEPARATE FILES; each
revision's file does NOT carry the next), then `/areas/tacombi-combi-sticker.md`,
then `/preferences.md`. Five prior contexts skipped them; one cost half a day and
produced the wrong body type. If you cannot read them, say so explicitly rather
than quietly proceeding.
**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner, the person this is for. **Do not ask me what the
real vehicle looks like.** Ask me what a PHOTOGRAPH shows — that has now paid
off seventeen times — but measure the surface, never ask about it.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §1 below. **SIXTEEN bundle lines now, and the rev14b line is a `fetch`.**
rev 18 opened with rev 17 missing and rev 19 with rev 18 missing; **rev 20
through rev 28 all restored CLEAN** — do not assume either way, check.

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
model — rev 22 RETIRED the test that produced the warn, and **NO GEOMETRY HAS
MOVED SINCE REV 23, AND NO ARTWORK SINCE REV 25.** Read §10.59.

## Step 4 — read, in this order
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.81 → this file →
**`HANDOFF_rev28.md`** → `HANDOFF_rev27.md` → `HANDOFF_rev26.md` →
`HANDOFF_rev25.md` → `HANDOFF_rev24.md` → `HANDOFF_rev23.md` →
`HANDOFF_rev22.md` → `HANDOFF_rev21.md` → `HANDOFF_rev20.md` →
`HANDOFF_rev19.md` → `AUDIT_rev18_loft.md` → `HANDOFF_rev18.md` →
`LOFT_GROUND_rev15.md` → `AUDIT_rev12.md` → `REF_MEASUREMENTS.md`.
`STATE.md` is machine-written by `audit.py`. **If it and any prose disagree, it
is right.** It has no known phantoms.
**Retirements that touch many numbers:** §10.11 (ground line, ~70 mm) and
§10.34 (hub chain, ~29 mm) and §10.29's ONE REF-wide correction (`:899`).
§10.46 corrects §10.37; **§10.45–48 retire NO §10.34 claim.** §10.57 retires
rev 20's boxes A and B. §10.59 RETIRES `H_ROOF`. §10.61 corrects the crossing
count. §10.62 ARMS item 4. §10.63 finds `folk_gen`'s bake frame stale. §10.65
finds `solve_ctan` measured THE WHOLE SCENE through a top-only mask. §10.66
finds rev 23 BROKE `folk_gen.composition()`. §10.67 REFUTES rev 24's own
work-item-2 brief. §10.68 REFUTES rev 24's `_ZB_AUTH` brief. §10.69 takes
`_RETIRED_VALUES` 5 → 15 rows. §10.70 IDENTIFIES the `COUNTERTAN` pedestal as
the settled-dust film. §10.71 finds `W_DUST_FAC_UP` anchored to the WRONG
MATERIAL. §10.72 finds the bumper item MALFORMED. §10.73 finds work item 2 an
ARTEFACT. §10.74 records two defects in rev 25's record. §10.75 is an OWNER
READING — the front bumper carries an OVER-RIDER BAR and a POST. §10.76 shows
the `W_DUST_FAC_UP` patch STRADDLED and that against `COUNTERTAN` there is NO
COVERAGE AT ALL. §10.77 REFUTES the F90 worry. §10.78 finds `T1_CYCALB`
VACUOUS and `T1_GAL_SKY` a DEAD LEVER. §10.79 builds a VALIDATED PSF estimator
that then DECLINES.
**§10.80–81 are rev 28's, and BOTH refute something a previous revision wrote:**
**§10.80 MEASURES THE PSF at last — my own §10.79 reading was WRONG, its five
ROIs are THREE edges, two of its five published rms figures are FICTION, and its
76 % spread was ONE THRESHOLD ARM, not mixed edge classes; §10.81 records the
owner reading the counter top as CLEAN — which CONTRADICTS a live assert — and
finds a SECOND TAUTOLOGY in the same chain.**

## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them
This has now paid off seventeen times. **My answers are not infallible — ask me
anyway, then measure what I say.** Show me a crop, mark the regions, give me
options, and **print the crop box**. rev 14's box was 120 px off; rev 19's
straddled a dark roof opening; rev 20's A and B straddled TWO MATERIALS; rev
21's redrawn N1 STILL straddled two materials; rev 22 found SPEC's OWN FOUNDING
CROP for `COUNTERTAN` straddling; rev 23's first draft of its own question figure
straddled the A-pillar and was thrown away; rev 26's first draft put box A on the
green body ABOVE the tube it was pointing at; rev 27 found that SPEC's founding
patch for `W_DUST_FAC_UP` NECESSARILY straddled; **rev 28 found that rev 27's
five PSF boxes EACH CONTAINED MORE THAN ONE EDGE, so the question could not be
answered at all — draw the LINE, not the region containing it.**
**Say plainly whether a box is a POINTER or a SAMPLING WINDOW.** rev 28's Q1
boxes were pointers and were verified clean by a PLANE-REMOVED straddle
indicator against a proven-straddling positive control (0.0/0.6 % vs 32.4 %).
**A CLASS GATE IS A PROBE TOO, and so is a BRIEF, a TARGET, a SUBAGENT'S
FINDING, a CITATION, A GUARD YOU JUST WROTE, A COMMENT YOU ARE WRITING RIGHT
NOW, AN ESTIMATOR YOU JUST BUILT, and A QUESTION YOU ARE ABOUT TO ASK ME.**
Three of rev 17's four items came back refuted; rev 19's single item refuted
three ways; rev 21 refuted all FIVE routes to its own headline; rev 22 refuted
its OWN item-3 target; rev 23 refuted TWO claims in its own briefing; rev 24
REFUTED ITS OWN WORK ITEM 2; rev 25 refuted its own item 2's brief AND a figure
in a comment it was writing; rev 26 refuted TWO of its own three work items;
rev 27 refuted TWO of its own hypotheses, its OWN first guard, its OWN first PSF
estimator and its OWN first three PSF ROIs; **rev 28 refuted rev 27's PSF
reading, rev 27's diagnosis of its own spread, THREE figures in rev 27's
`EDGE_NOTES`, and its OWN first control TWICE.**

## Step 6 — the work
§6 below is the ordered list. **The loft is DONE and AUDITED. The arch is FIXED.
`H_ROOF` is RETIRED. `CREAM` is UNCHANGED. ITEM 4 IS ARMED and the show flank is
at 0.0 mm. THE ARTWORK IS CURRENT. `COUNTERTAN`'s pedestal IS IDENTIFIED.
THE F90 QUESTION IS CLOSED. THE PSF IS MEASURED at σ 0.5594 ± 0.0280 px.
THE OLDEST UNDONE ITEM IS STILL THE FRONT OVER-RIDER, and it is now blocked on
A SCALE, not on a reading.**

## Step 7 — resolution
rev 25 shipped 4800×3200 in 20 strips, worst seam z 1.91. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips ~5–7 min each,
edge strips ~1.5 min. **`rev25_hero34f.png` photographs the CURRENT mesh and the
CURRENT artwork** — nothing has moved in rev 26, 27 or 28. Do not re-shoot
unless something moves.

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
**`solve_ctan`'s measured frame is ISOLATED** — do not remove `_only`.
**Every absolute linear figure in SPEC §10.56 is a THREE-STACKED-RIG number.**
**§0.2 is NOT self-arming and never was.** `_retired_value_drift()` is the
mechanism that sees retired VALUES; **never widen it or add exemption tokens.**
**EVERY constant in `folk_gen.py` is PARSED and every parse RAISES.**
**The committed `tex/*.png` are CURRENT** — `swirl.png` `4ee4e09e`,
`swirl_b.png` **`d201597e`**, `nose.png` `b31ea156`. **The bake is
DETERMINISTIC** (seeds 196301 / 771963).
**Do NOT add a `_RETIRED_VALUES` row for the ±2.145 bumper faces** — neither
value is live. Never correct this vehicle toward the VW factory catalogue.
**`COUNTERTAN`'s pedestal IS the settled-dust film** — dust carries
**57.1/52.6/36.6 %**, dust + spec + coat **89.3/87.9/84.8 %**. **`k` is 0.0368
shipped and 0.0871 with dust+spec+coat off — a factor 2.37.** Any future solve
must re-derive it; **never carry the old secant gain, and never carry rev 24's
"+40 %".** **`T1_CTAN_WEAR=0` is TWO LEVERS.** **`_DOOR_TOP_AUTH` STAYS at
1.8140** — §10.73 settles it at **0.315 mm**. **No re-bake is owed.**
`DOOR_H = 1.013467`. **`X_BUMP_F/R` are DEAD.**
**`W_DUST_FAC_UP`'s founding patch NECESSARILY STRADDLED** — largest clean
rectangle **1060–1512 px** against the **2700** it needs — **but the straddle is
NOT the explanation**; cleaning it makes the disagreement WORSE.
**`_UP_MEASURED` lies OUTSIDE the segment [`COUNTERTAN`, `W_DUST_COL_UP`] in all
three channels — there is no coverage error, because THERE IS NO COVERAGE.**
**The live assert's three-channel agreement is a TAUTOLOGY** (spread 5.2e-05).
**`t1_mats.py`'s "(0.9676, 0.7784, 0.4976)" is the VON-KRIES GAIN, not `CREAM`.**
**`T1_CTAN_SP=0` IS a COMPLETE specular ablation** — 0.00 % left at 83° grazing.
**Do not re-open F90.** **`T1_CYCALB=0` IS A VACUOUS ARM** — the cyclorama is
excluded by ABSENCE (`build.py:600` vs the probe's cut at 586). **`T1_GAL_SKY`
IS A DEAD LEVER.** **`T1_WORLD` and `T1_GAL_LUM` carry 2.64/2.78/2.91 % —
REFUTED.** The **scene→top bounce is the only named candidate left.**
**NEW, rev 28 and now settled:**
**THE PSF FOR `ref_workshop.jpg` IS σ = 0.5594 ± 0.0280 px, FWHM 1.317 px** —
CORE ARMS ONLY (20–80, 25–75), n = 32, four owner-confirmed occlusion steps
agreeing to 12.4 %. **DO NOT POOL THE 10–90 ARM BACK IN.**
**§10.79's "probably unmeasurable" reading is REFUTED BY THE OWNER**:
**D1, D2, D3, D4, D6, D7, D8, D9 are PHYSICAL STEPS; D5 is NOT.**
**`EDGE_NOTES` IS PROSE AND TWO OF ITS FIVE rms FIGURES ARE FICTION** — 0.069
and 0.129 exist nowhere among the 35 candidates. Do not quote that block.
**rev 27's FIVE ROIs are THREE EDGES** — E1/E2/E3 are ONE, colinear to 0.1 px.
**The 35 candidates cluster to 14 DISTINCT EDGES**; rev 27 named three.
**D9 is EXCLUDED and PRICED at +0.176 px / 32 %** — it carries the bulb string.
**D1/D4/D8 are UNMEASURABLE**; D1 misses the monotone threshold by **0.0002** —
**do not widen it to collect D1.**
**[stated] THE COUNTER TOP IS CLEAN VARNISHED PLYWOOD**, which **CONTRADICTS**
`W_DUST_FAC_UP`'s live assert of 0.548 coverage. **But f = 0 alone does NOT
reconcile the model** — clean `COUNTERTAN` is still **34.0 % short in B** — and
the best-matching arm is dusty `COUNTERCREAM`, **the wrong material**. §10.60
still rules the pair INADMISSIBLE. **Do NOT set `W_DUST_FAC_UP` to 0 blind.**
**TAUTOLOGY 2: the founding patch's own E-free ratio × `CREAM` IS
`_UP_MEASURED`** — it can NEVER disagree with the assert it founded. **Use
§10.76's band-following CLEAN sample (median sRGB 208,176,132) instead.**

## Hard-won rules — every one was learned by breaking it
* Never set a vertical position from the ground line (~70 mm common-mode) — the
  HUB-referenced chain has the same disease at ~29 mm.
* A single linear px→metre scale does not hold along the flank; the map is
  projective. **And a scale measured on one plane is not the scale on another.**
* **An image slope of a fore-aft line is not a rake.**
* A rendered ratio is only an albedo ratio between two surfaces of the **same
  class** under the same light. **AN OBSERVED PIXEL IS NOT AN ALBEDO.**
* **IF TWO REFERENCE SURFACES ARE CLAIMED TO SHARE A LIGHT, TEST IT.**
* A constant tuned against another constant must be expressed in terms of it.
* **A claim in prose is not a guard — INCLUDING WHEN THE PROSE IS INSIDE THE
  GUARD, INSIDE THE PROBE, AND INCLUDING WHEN YOU ARE WRITING IT RIGHT NOW.**
* **A MASK IS NOT A MEASUREMENT UNTIL THE MEASURED FRAME IS ISOLATED TOO.**
* **CHECK WHETHER YOUR INSTRUMENT'S LIGHT RIG IS THE ONE YOU THINK.**
* **A MAGNITUDE CAN BE EXACTLY RIGHT AND THE CONCLUSION STILL WRONG**, and
  **A SMALL MAGNITUDE DOES NOT MEAN A SMALL CONTRIBUTION.**
* **A CONSTANT CAN BE SOLVED AGAINST THE WRONG MATERIAL AND ITS OWN LIVE ASSERT
  WILL NEVER SEE IT.**
* **A DERIVED CONSTANT'S OWN SOURCE PATCH CAN NEVER FALSIFY IT.** Check whether
  your test data is upstream of the thing you are testing. *(NEW, rev 28 —
  this is Tautology 2, and it is the second one found in the same chain.)*
* **A QUESTION THAT CANNOT BE ANSWERED UNAMBIGUOUSLY IS THE ASKER'S DEFECT.**
  Draw the LINE, not the region containing it. *(NEW, rev 28)*
* **A THRESHOLD SWEEP THAT DISAGREES IS REPORTING SOMETHING — READ IT BEFORE
  BLAMING THE DATA.** rev 27's 76 % spread was one arm's tail sensitivity and
  was diagnosable on a single edge. *(NEW, rev 28)*
* **VALIDATE THE ARM YOU ACTUALLY USE.** A control on a pooled estimator
  validates something the result does not rest on. *(NEW, rev 28)*
* **PRICE AN EXCLUSION.** Print what dropping an outlier costs, every run.
  *(NEW, rev 28)*
* **BEFORE ADJUDICATING TWO DISAGREEING CONSTANTS, CHECK THEY DENOTE THE SAME
  QUANTITY, AND CHECK WHERE EACH CAME FROM.** `git log -S` is one command.
* **A MEAN IS NOT A STATION VALUE.**
* **A RETIRED VALUE RE-EXPRESSED IN ANOTHER FORM IS INVISIBLE TO A SUBSTRING
  GUARD.** The answer is another ROW, never a looser rule.
* **WHEN A CONTROL FAILS, THE CONTROL IS THE FINDING — but check the control's
  own premise first.** rev 27 did this THREE times; **rev 28 did it TWICE more
  and the second one found Tautology 2.**
* **AN ARC LENGTH IS NOT A PENETRATION DEPTH.**
* **DO NOT INHERIT A GUARD'S RATIONALE ALONG WITH ITS SHAPE.**
* **DO NOT ARM A GUARD AT ZERO AGAINST GEOMETRY NOBODY HAS PHOTOGRAPHED.**
* **A RAY-VISIBILITY FLAG IS NOT AN ABLATION.** Remove the ALBEDO. **AND CHECK
  THE LEVER REACHES ONLY WHAT YOU THINK.**
* **AN INERT ABLATION CAN MEAN THE WRONG ESTIMATOR — OR THAT THE THING YOU ARE
  ABLATING IS NOT IN THE SCENE AT ALL.**
* **A GUARD ON A MAX IS BLIND TO EVERY CHANNEL BUT ONE.** Assert the TRIPLE.
* **A PROBE THAT MEASURES THE OPTICS MUST NOT ADD OPTICS OF ITS OWN.**
* **AN ESTIMATOR CANNOT TELL AN OCCLUSION STEP FROM A PAINT BOUNDARY.** That is
  an OWNER READING — **and when you get one, it can refute your own probe's
  published conclusion, as it did in rev 28.**
* **A MEASUREMENT WITH NO RECORDED CROP IS NOT REPRODUCIBLE — BUT IT MAY BE
  RECOVERABLE.** Then check whether the recovery is UNIQUE, and say so when it
  is not.
* **Build the CONTROL first and prove it is a no-op, then run the experiment —
  and CHECK THE CONTROL ITSELF.**
* **AN ILLUMINANT REFERENCE MUST CARRY SUBSTANTIAL ALBEDO IN ALL THREE
  CHANNELS.**
* **BEFORE DE-ILLUMINATING ANYTHING, TEST WHETHER A NEUTRAL TRANSFORM CAN RELATE
  THE TWO FRAMES AT ALL.**
* **A SUBAGENT'S FINDING IS A CLAIM, NOT A MEASUREMENT.**
* **VERIFY A CODE CHANGE BY EXECUTING IT, NOT BY READING IT.**
* **A CARRIED-FORWARD FIGURE IS A CLAIM TOO — AND SO IS ITS CITATION.**
* **WHEN TWO ROWS OF A MEASUREMENT AGREE EXACTLY, SUSPECT A BUG — THEN CHECK.**
* **MEASURE THE PSF BEFORE QUOTING ANYTHING NEAR THE LIMIT**, and **sweep the
  threshold rather than picking one**.
* **A negative control turns a number into a measurement.**
* **Before scheduling a solve, ABLATE THE CONSTANT TO ZERO.**
* **CLIPPING DESTROYS TEXTURE.** **An ORTHO render has an EXACT px/m.**
* **A restore check that only greps THIS revision's strings cannot detect a lost
  ANCESTOR** — and **AN ANCESTOR CHECK IS ONLY AS GOOD AS THE NEWEST COMMIT IN
  IT. Both checks must reach the tip. AND A CONTENT CHECK MUST BE SATISFIABLE ON
  A FRESH CLONE.**
* **Do not put a figure in an acceptance test — or a HANDOFF — unless you
  watched it print.**
* **If a change trips a guard, THAT IS THE GUARD WORKING. Never widen it.**
* **A probe that cannot answer must return None, not an endpoint.**
* When a finding breaks something independently locked, measure it a third way.
* **Watch for the lamppost** — `ref_side.jpg` columns 62–79. **`ref_workshop.jpg`
  has no lamppost.**
* A single shell command is killed at 10 minutes. This box has 2 cores — spawn
  2–4 `Agent`s on **disjoint files**, read-only for audits, rather than a
  Workflow. **A hero strip killed at the limit may still have written a valid
  file — let the SEAM CHECK adjudicate it.**
* **Backticks in `git commit -m` hit shell substitution.** Use `git commit -F`.
* **The device bridge may drop mid-transfer.** Try the direct call FIRST — rev
  28 moved SIXTEEN bundles in ONE call — and fall back to `split` + parallel
  single-file calls + **md5 against my disk** only on failure. `device_bash`
  cannot `rm`. **Split the OUTBOUND batch.**

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
git pull --ff-only ../tacombi_rev24_incremental.bundle HEAD      # -> 107
git pull --ff-only ../tacombi_rev25_incremental.bundle HEAD      # -> 115
git pull --ff-only ../tacombi_rev26_incremental.bundle HEAD      # -> 120
git pull --ff-only ../tacombi_rev27_incremental.bundle HEAD      # -> 126
git pull --ff-only ../tacombi_rev28_incremental.bundle HEAD      # -> 130
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
Content checks — **the first eight reach the TIP on purpose.** There is no `ls`
of a hero here: **the hero is gitignored and lives only on my disk** (§10.74).
```bash
git status                                              # clean
grep -c '### 10.80' SPEC.md                             # 1  rev 28
grep -c '### 10.81' SPEC.md                             # 1  rev 28
grep -c 'TAUTOLOGY 2' SPEC.md                           # 2  rev 28
grep -c 'CORE' probe_psf_owner.py                       # 12  rev 28
grep -c 'OWNER_STEP' probe_psf_owner.py                 # 5  rev 28
grep -c 'CLEAN_TOP_SRGB' probe_clean_top.py             # 2  rev 28
grep -c 'same_edge' probe_psf_lines.py                  # 3  rev 28
ls HANDOFF_rev28.md probe_psf_lines.py probe_psf_owner.py probe_clean_top.py mark_rev28_q.py
grep -c 'SPEC 10.76' t1_mats.py                         # 4  ANCESTOR rev 27
grep -c 'PUBLISHED_CLEAN' probe_ctan_pedestal.py        # 3  ANCESTOR rev 26
grep -c '_ceval' folk_gen.py                            # 19 ANCESTOR rev 25
grep -c '_retired_value_drift' verify.py                # 3 ANCESTOR rev 24
grep -c 'OFF_CROSS_BASELINE' t1_shell.py                # 1 ANCESTOR rev 23
grep -c 'H_ROOF_REGRESSION' verify.py                   # 7 ANCESTOR rev 22
grep -c 'T1_CTAN_NOBOUNCE' shader_solve.py              # 4 ANCESTOR rev 20
grep -c '_BODY' cream_rms.py                            # 4 ANCESTOR rev 19
grep -c '_arch_lip_z' verify.py                         # 2 ANCESTOR rev 18
grep -c 'matte_tap' studio.py                           # 6 ANCESTOR rev 17
grep -c '_coons_cap' t1_core.py                         # 3 ANCESTOR rev 16
grep -c 'The threshold is not the parameter' post.py    # 1 ANCESTOR rev 13
```
**EVERY VALUE ABOVE IS FILLED FROM A FRESH-CLONE VERIFICATION RUN.** Never type
one from memory — `grep -c` counts LINES, not occurrences, and that has produced
a wrong figure in eleven revisions.
Ancestry:
```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```
**Known limitation, stated rather than hidden:** the ancestry loop's newest
entry is a rev-19 commit, because a hash cannot be written into the file that
contains it without amending, and rev 14 learned not to amend. **The TIP is
covered by the rev-28 content greps instead.**
Texture md5s on the restored tree — **all three must match:**
```bash
md5sum tex/swirl.png tex/swirl_b.png tex/nose.png
# 4ee4e09e...   d201597e...   b31ea156...
```

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
**EVERY GEOMETRY FIGURE IS IDENTICAL TO REV 23's. NO GEOMETRY MOVED IN REV 24,
25, 26, 27 OR 28, AND NO ARTWORK IN REV 26, 27 OR 28.**

## 3. What rev 28 changed — `HANDOFF_rev28.md` has the full account
- **`SPEC.md`** — §10.80, §10.81 and two change-log rows.
- **`probe_psf_lines.py`**, **`probe_psf_owner.py`**, **`probe_clean_top.py`**,
  **`mark_rev28_q.py`** — all NEW, all READ-ONLY.
- **NO CONSTANT CHANGED. NO GEOMETRY. NO ARTWORK.** `CREAM`, `COUNTERTAN`,
  `COUNTERCREAM`, `W_DUST_FAC_UP`, `RED`, the rake, the roof and all three
  textures UNCHANGED.
**Things you must not silently undo — `HANDOFF_rev28.md` §4**, and rev 27's §4,
rev 26's §4, rev 25's §4, rev 24's §4, rev 23's §4, rev 22's §3, rev 21's §4,
rev 20's §4, rev 19's §4 and rev 18's §4 all still stand in full.

## 4. Still open
See `HANDOFF_rev28.md` §5 for the full list. The ones that matter:
- **THE FRONT OVER-RIDER (§10.75).** The owner has ruled the tube and the post
  are BOTH ON THE BUS and chose **model them tagged workshop-stage**. The model
  has NO member for either. **The PSF blocker is CLEARED (§10.80).** What is
  left: **a scale on the nose/bumper plane, or a proof none is admissible.**
  **NOT ATTEMPTED IN REV 28.**
- **§10.81 — `W_DUST_FAC_UP` is CONTRADICTED by an owner reading**, and f = 0
  alone does not reconcile the model. **Do not repair it blind.**
- **The residual pedestal, 6.6 / 6.6 / 8.5 %** — only the **scene→top bounce**
  remains. **NOT STARTED IN REV 28.**
- **THE FRONT BUMPER FACE IS UNMEASURED** — both catalogue values struck.
- **`CREAM`** — needs a same-light, same-CLASS, three-channel reference.
- **THE ABSOLUTE ROOF HEIGHT.** **THE OFF FLANK**, 804.9 mm.
- `GAL_SKY` is a dead lever. `PLATE_W = 0.3300` has no provenance.
  `probe_rev16.py:90` prints `xa` vs `xa`.

## 5. FIRST QUESTIONS FOR THE OWNER — NONE OUTSTANDING
Both of rev 27's questions were **answered in rev 28** and both changed the
work. **No decision is outstanding.**
What would still move the most is one photograph: **a head-on rear (or front)
elevation from roof height or above, with the counter and the lids clear of the
section.** It is the only realistic route to closing **`CREAM`**, **the absolute
roof height** and now **§10.81**. A clear view of the **off flank** would
additionally close 804.9 mm of unadjudicated crossing. **And for the over-rider
specifically: any frame showing the FRONT of the vehicle with a feature of known
size in the bumper plane.**

## 6. Ordered work list for rev 29
1. **§10.81 — the counter top.** Now the best-posed item: an owner reading
   CONTRADICTS a live assert, and the arithmetic is done. **Do not set
   `W_DUST_FAC_UP` to 0 blind** — clean `COUNTERTAN` is still 34.0 % short in
   B, so removing the dust is necessary and NOT sufficient, and f = 0 would
   discard §10.70's pedestal work. Needs a `CREAM` reference or a same-class,
   differing-orientation pair.
2. **THE FRONT OVER-RIDER (§10.75, §10.80).** A scale on the nose/bumper plane
   **or a proof that none is admissible**, then size and build, **every number
   tagged workshop-stage**. σ = 0.5594 ± 0.0280 px is available for the tube's
   7.9–11.7 px bracket. **This moves geometry and invalidates
   `rev25_hero34f.png`.** Strike ±2.145 / ±2.140 from §2 either way (§10.72).
3. **The residual 6.6/6.6/8.5 % pedestal — the scene→top bounce**, the only
   named candidate left. Remove `gal_warmer` / `gal_caddy0` / `gal_caddy1` and
   **re-derive the mask** (a visibility flag is barred by §10.56). Note the
   harness has **no cyclorama** (§10.78) — state that, do not silently fix it.
4. Tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
5. A hero ONLY if geometry or artwork moves — **item 2 WILL move it.**
   `rev25_hero34f.png` photographs the current mesh and artwork until then.
6. Camera absolutely last.

## 7. THE COMMIT COUNT AND THE CONTENT FIGURES
This section is written LAST, after the final commit, and every figure in §1 was
read off a fresh-clone verification run rather than typed from memory. **This has
gone wrong in ELEVEN revisions during handoff assembly.** rev 23, 24, 25, 26 and
27 were clean runs.
**FINAL COUNT: 130 commits, clean tree.**
