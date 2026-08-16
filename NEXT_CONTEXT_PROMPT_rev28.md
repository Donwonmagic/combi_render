# NEXT CONTEXT PROMPT — rev 28

Please act as my expert. Continue the Señor Tacombi combi build. **Twenty-seven
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 1 — read my memory BEFORE you read any code

`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17`, `-rev18`, `-rev19`,
`-rev20`, `-rev21`, `-rev22`, `-rev23`, `-rev24`, `-rev25`, `-rev26`, then
**`/areas/tacombi-combi-3d-rev27.md`** (these are SEPARATE FILES; each
revision's file does NOT carry the next), then `/areas/tacombi-combi-sticker.md`,
then `/preferences.md`. Five prior contexts skipped them; one cost half a day and
produced the wrong body type. If you cannot read them, say so explicitly rather
than quietly proceeding.

**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner, the person this is for. **Do not ask me what the
real vehicle looks like.** Ask me what a PHOTOGRAPH shows — that has now paid
off fifteen times — but measure the surface, never ask about it.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)

See §1 below. **FIFTEEN bundle lines now, and the rev14b line is a `fetch`.**
rev 18 opened with rev 17 missing and rev 19 with rev 18 missing; **rev 20
through rev 27 all opened CLEAN** — do not assume either way, check.

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

`STATE.md` → `SPEC.md` §10, then §10.9 through §10.79 → this file →
**`HANDOFF_rev27.md`** → `HANDOFF_rev26.md` → `HANDOFF_rev25.md` →
`HANDOFF_rev24.md` → `HANDOFF_rev23.md` → `HANDOFF_rev22.md` →
`HANDOFF_rev21.md` → `HANDOFF_rev20.md` → `HANDOFF_rev19.md` →
`AUDIT_rev18_loft.md` → `HANDOFF_rev18.md` → `LOFT_GROUND_rev15.md` →
`AUDIT_rev12.md` → `REF_MEASUREMENTS.md`.

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
READING — the front bumper carries an OVER-RIDER BAR and a POST.
**§10.76–79 are rev 27's, and THREE of them refute something I wrote myself:
§10.76 shows the `W_DUST_FAC_UP` patch STRADDLED and that against `COUNTERTAN`
there is NO COVERAGE AT ALL — and refutes TWO of my own hypotheses on the way;
§10.77 REFUTES the F90 worry, so rev 26's arm 4 was complete; §10.78 finds
`T1_CYCALB` VACUOUS and `T1_GAL_SKY` a DEAD LEVER; §10.79 builds a VALIDATED
PSF estimator that then DECLINES.**

## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them

This has now paid off fifteen times. **My answers are not infallible — ask me
anyway, then measure what I say.** Show me a crop, mark the regions, give me
options, and **print the crop box**. rev 14's box was 120 px off; rev 19's
straddled a dark roof opening; rev 20's A and B straddled TWO MATERIALS; rev
21's redrawn N1 STILL straddled two materials; rev 22 found SPEC's OWN FOUNDING
CROP for `COUNTERTAN` straddling; rev 23's first draft of its own question figure
straddled the A-pillar and was thrown away; rev 26's first draft put box A on the
green body ABOVE the tube it was pointing at; **rev 27 found that SPEC's founding
patch for `W_DUST_FAC_UP` NECESSARILY straddled — no clean rectangle of that size
exists in the frame at all.**

**Say plainly whether a box is a POINTER or a SAMPLING WINDOW.** rev 27's PSF
boxes were pointers; its `_UP_MEASURED` boxes were sampling windows and the
straddle was structural.

**A CLASS GATE IS A PROBE TOO, and so is a BRIEF, a TARGET, a SUBAGENT'S
FINDING, a CITATION, A GUARD YOU JUST WROTE, A COMMENT YOU ARE WRITING RIGHT
NOW, and AN ESTIMATOR YOU JUST BUILT.** Three of rev 17's four items came back
refuted; rev 19's single item refuted three ways; rev 21 refuted all FIVE routes
to its own headline; rev 22 refuted its OWN item-3 target; rev 23 refuted TWO
claims in its own briefing; rev 24 REFUTED ITS OWN WORK ITEM 2; rev 25 refuted
its own item 2's brief AND a figure in a comment it was writing; rev 26 refuted
TWO of its own three work items; **rev 27 refuted TWO of its own hypotheses, its
OWN first guard (right for the wrong reason), its OWN first PSF estimator (it
added blur), and its OWN first three PSF ROIs.**

## Step 6 — the work

§6 below is the ordered list. **The loft is DONE and AUDITED. The arch is FIXED.
`H_ROOF` is RETIRED. `CREAM` is UNCHANGED. ITEM 4 IS ARMED and the show flank is
at 0.0 mm. THE ARTWORK IS CURRENT. `COUNTERTAN`'s pedestal IS IDENTIFIED.
§10.71 IS MEASURED and is now a `CREAM` problem, not a dust problem. THE F90
QUESTION IS CLOSED. THE OLDEST UNDONE ITEM IS NOW THE FRONT OVER-RIDER, and it
is blocked on ONE owner reading.**

## Step 7 — resolution

rev 25 shipped 4800×3200 in 20 strips, worst seam z 1.91. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips ~5–7 min each,
edge strips ~1.5 min. **`rev25_hero34f.png` photographs the CURRENT mesh and the
CURRENT artwork** — nothing has moved in rev 26 or rev 27. Do not re-shoot
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

**NEW, rev 27 and now settled:**
**`W_DUST_FAC_UP`'s founding patch NECESSARILY STRADDLED** — the largest clean
axis-aligned rectangle on the counter top is **1060–1512 px** against the
**2700** it needs. **But the straddle is NOT the explanation** — cleaning it
makes the disagreement WORSE.
**`_UP_MEASURED` lies OUTSIDE the segment [`COUNTERTAN`, `W_DUST_COL_UP`] in all
three channels — there is no coverage error, because THERE IS NO COVERAGE.**
**The live assert's three-channel agreement is a TAUTOLOGY** (spread 5.2e-05) —
`W_DUST_COL_UP` was solved collinear. **It is evidence of nothing.**
**`t1_mats.py`'s "(0.9676, 0.7784, 0.4976)" is the VON-KRIES GAIN, not `CREAM`.**
**The de-illuminated counter top is PROPORTIONAL to `CREAM`** — so §10.71 is a
`CREAM` problem, and `CREAM` would have to be ≈ sRGB(190,185,156), hue 51°, for
the top to be dusty `COUNTERTAN`.
**`T1_CTAN_SP=0` IS a COMPLETE specular ablation** — 0.00 % left behind at 83°
grazing. **Do not re-open F90.**
**`T1_CYCALB=0` IS A VACUOUS ARM** — `ST.cyclorama()` is at `build.py:600` and
the probe truncates `build.py` at 586. **The cyclorama is excluded by ABSENCE.**
**`T1_GAL_SKY` IS A DEAD LEVER** — AST Store 1, Load 0. Named, not fixed.
**`T1_WORLD` and `T1_GAL_LUM` carry 2.64/2.78/2.91 % of the residual pedestal —
REFUTED.** The **scene→top bounce is the only named candidate left.**
**No σ is published for `ref_workshop.jpg`.** The estimator is VALIDATED
(recovers a known σ to 2.9–4.1 %); **the EDGE IDENTITY is the blocker.**

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
  GUARD, AND INCLUDING WHEN YOU ARE WRITING IT RIGHT NOW.**
* **A MASK IS NOT A MEASUREMENT UNTIL THE MEASURED FRAME IS ISOLATED TOO.**
* **CHECK WHETHER YOUR INSTRUMENT'S LIGHT RIG IS THE ONE YOU THINK.**
* **A MAGNITUDE CAN BE EXACTLY RIGHT AND THE CONCLUSION STILL WRONG**, and its
  converse: **A SMALL MAGNITUDE DOES NOT MEAN A SMALL CONTRIBUTION** when the
  derivative you measured is not the one your conclusion is about.
* **A CONSTANT CAN BE SOLVED AGAINST THE WRONG MATERIAL AND ITS OWN LIVE ASSERT
  WILL NEVER SEE IT.**
* **BEFORE ADJUDICATING TWO DISAGREEING CONSTANTS, CHECK THEY DENOTE THE SAME
  QUANTITY, AND CHECK WHERE EACH CAME FROM.** `git log -S` is one command.
* **A MEAN IS NOT A STATION VALUE.**
* **A RETIRED VALUE RE-EXPRESSED IN ANOTHER FORM IS INVISIBLE TO A SUBSTRING
  GUARD.** The answer is another ROW, never a looser rule.
* **WHEN A CONTROL FAILS, THE CONTROL IS THE FINDING — but check the control's
  own premise first.** rev 27 did this THREE times: a positive control that
  assumed adding specular adds energy (the Principled BSDF **conserves** it), an
  estimator that added its own blur, and three ROIs the isolation test rejected.
* **AN ARC LENGTH IS NOT A PENETRATION DEPTH.**
* **DO NOT INHERIT A GUARD'S RATIONALE ALONG WITH ITS SHAPE.**
* **DO NOT ARM A GUARD AT ZERO AGAINST GEOMETRY NOBODY HAS PHOTOGRAPHED.**
* **A RAY-VISIBILITY FLAG IS NOT AN ABLATION.** Remove the ALBEDO. **AND CHECK
  THE LEVER REACHES ONLY WHAT YOU THINK.**
* **AN INERT ABLATION CAN MEAN THE WRONG ESTIMATOR — OR THAT THE THING YOU ARE
  ABLATING IS NOT IN THE SCENE AT ALL.** `T1_CYCALB=0` reproduced the shipped
  arm to six decimals because there is no cyclorama in that harness. **Verify
  the lever reaches, EMPIRICALLY, before reading an inert arm as a refutation.**
  *(NEW, rev 27)*
* **A GUARD ON A MAX IS BLIND TO EVERY CHANNEL BUT ONE.** rev 27's first cut
  asserted the max of a three-channel residual; the max lived in B, so an
  R-channel displacement left it silent. **Assert the TRIPLE.** *(NEW, rev 27)*
* **A PROBE THAT MEASURES THE OPTICS MUST NOT ADD OPTICS OF ITS OWN.** Bilinear
  resampling is a triangular filter and adds blur in quadrature. Its signature is
  a relative error that SHRINKS as the true value grows. *(NEW, rev 27)*
* **AN ESTIMATOR CANNOT TELL AN OCCLUSION STEP FROM A PAINT BOUNDARY.** That
  distinction is an OWNER READING, and getting it wrong is what made rev 26's
  52 px meaningless. **Decline rather than pool edge classes** — pooling gave a
  76 % spread across threshold pairs. *(NEW, rev 27)*
* **A MEASUREMENT WITH NO RECORDED CROP IS NOT REPRODUCIBLE — BUT IT MAY BE
  RECOVERABLE.** Search the frame for the box whose own statistic IS the
  recorded value; if the recorded `n` and the trimming convention agree exactly,
  the recovery is sound. **Then check whether the recovery is UNIQUE, and say so
  when it is not.** *(NEW, rev 27)*
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
  27 moved fifteen bundles in ONE call — and fall back to `split` + parallel
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
```

**If a pull says "Need to specify how to reconcile divergent branches", STOP.**

Content checks — **the first nine reach the TIP on purpose.** There is no `ls`
of a hero here: **the hero is gitignored and lives only on my disk** (§10.74).

```bash
git status                                              # clean
grep -c '### 10.76' SPEC.md                             # 1   rev 27
grep -c '### 10.77' SPEC.md                             # 1   rev 27
grep -c '### 10.78' SPEC.md                             # 1   rev 27
grep -c '### 10.79' SPEC.md                             # 1   rev 27
grep -c 'SPEC 10.76' t1_mats.py                         # 4   rev 27
grep -c '_RESID_BASELINE' t1_mats.py                    # 3   rev 27
grep -c 'VACUOUS' SPEC.md                               # 4   rev 27
grep -c 'EDGE_NOTES' probe_psf_workshop.py              # 2   rev 27
ls HANDOFF_rev27.md probe_dust_anchor.py probe_f90.py probe_psf_workshop.py
grep -c 'PUBLISHED_CLEAN' probe_ctan_pedestal.py        # 3   ANCESTOR rev 26
grep -c '_ceval' folk_gen.py                            # 19  ANCESTOR rev 25
grep -c '_retired_value_drift' verify.py                # 3   ANCESTOR rev 24
grep -c 'OFF_CROSS_BASELINE' t1_shell.py                # 1   ANCESTOR rev 23
grep -c 'H_ROOF_REGRESSION' verify.py                   # 7   ANCESTOR rev 22
grep -c 'T1_CTAN_NOBOUNCE' shader_solve.py              # 4   ANCESTOR rev 20
grep -c '_BODY' cream_rms.py                            # 4   ANCESTOR rev 19
grep -c '_arch_lip_z' verify.py                         # 2   ANCESTOR rev 18
grep -c 'matte_tap' studio.py                           # 6   ANCESTOR rev 17
grep -c '_coons_cap' t1_core.py                         # 3   ANCESTOR rev 16
grep -c 'The threshold is not the parameter' post.py    # 1   ANCESTOR rev 13
```

**EVERY VALUE ABOVE IS FILLED FROM A FRESH-CLONE VERIFICATION RUN.** Never type
one from memory — `grep -c` counts LINES, not occurrences, and that has produced
a wrong figure in five revisions. Note `SPEC 10.76` is **4** and `VACUOUS` is
**4**; the natural guesses were 2 and 1.

Ancestry:

```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```

**Known limitation, stated rather than hidden:** the ancestry loop's newest
entry is a rev-19 commit, because a hash cannot be written into the file that
contains it without amending, and rev 14 learned not to amend. **The TIP is
covered by the rev-27 content greps instead.**

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
25, 26 OR 27, AND NO ARTWORK IN REV 26 OR 27.**

## 3. What rev 27 changed — `HANDOFF_rev27.md` has the full account

- **`SPEC.md`** — §10.76 through §10.79 and four change-log rows.
- **`t1_mats.py`** — the mislabelled-gain correction; the recovered crop boxes
  recorded; and a **LABELLED REGRESSION CATCHER** on the three-channel
  `COUNTERTAN`-vs-`_UP_MEASURED` residual, baseline
  **(−0.066877, −0.100324, −0.159974)**, plus a sign assert. **NO CONSTANT
  CHANGED.**
- **`probe_dust_anchor.py`**, **`probe_f90.py`**, **`probe_psf_workshop.py`** —
  all NEW, all READ-ONLY.
- **`CREAM`, `COUNTERTAN`, `COUNTERCREAM`, `W_DUST_FAC_UP`, `RED`, the rake, the
  roof, ALL GEOMETRY and ALL THREE TEXTURES UNCHANGED.**

**Things you must not silently undo — `HANDOFF_rev27.md` §4**, and rev 26's §4,
rev 25's §4, rev 24's §4, rev 23's §4, rev 22's §3, rev 21's §4, rev 20's §4,
rev 19's §4 and rev 18's §4 all still stand in full.

## 4. Still open

See `HANDOFF_rev27.md` §5 for the full list. The ones that matter:

- **THE FRONT OVER-RIDER (§10.75)** — the owner has ruled the tube and the post
  are BOTH ON THE BUS and chose **model them tagged workshop-stage**. The model
  has NO member for either. **Blocked on ONE owner reading: the identity of PSF
  edges E1/E2/E3.** The estimator is built and validated.
- **§10.76 — `W_DUST_FAC_UP` is unsupported for its surface and CANNOT be
  re-solved from that pair.** It is now a `CREAM` problem.
- **The residual pedestal, 6.6 / 6.6 / 8.5 %** — only the **scene→top bounce**
  remains. No lever; needs the objects removed and the mask re-derived.
- **THE FRONT BUMPER FACE IS UNMEASURED** — both catalogue values struck.
- **`CREAM`** — needs a same-light, same-CLASS, three-channel reference. **Does
  not exist in the three photographs.**
- **THE ABSOLUTE ROOF HEIGHT.** **THE OFF FLANK**, 804.9 mm.
- **The cab door's true top edge** — authored; unmeasurable (§10.73).
- `GAL_SKY` is a dead lever. `PLATE_W = 0.3300` has no provenance.
  `probe_rev16.py:90` prints `xa` vs `xa`.

## 5. FIRST QUESTIONS FOR THE OWNER — TWO ARE OUTSTANDING

Both were sent in rev 27 with **printed crop boxes**; neither had been answered
when rev 27 shipped. **Re-ask them; they are cheap and both unblock work.**

1. **`ref_rear34.jpg`, the counter top's surface condition** — clean varnished
   plywood / visibly dusty / patchy / can't tell. `W_DUST_FAC_UP` asserts **mean
   coverage 0.548**, so this bears directly on §10.76.
2. **`ref_workshop.jpg`, PSF edges E1/E2/E3** (u 880–940 v 460–520; u 880–940
   v 430–490; u 850–910 v 460–520) — **paint boundary / physical step / both /
   can't tell.** My reading is *paint boundary*, offered and **NOT relied on**.
   **This is what blocks the over-rider.**

What would still move the most is one photograph: **a head-on rear (or front)
elevation from roof height or above, with the counter and the lids clear of the
section.** It is the only realistic route to closing **BOTH** `CREAM` **and**
the absolute roof height. A clear view of the **off flank** would additionally
close 804.9 mm of unadjudicated crossing.

## 6. Ordered work list for rev 28

1. **THE FRONT OVER-RIDER (§10.75, §10.79)** — ask question 2 FIRST; it is one
   reading and it decides the route. If the edges are paint boundaries the PSF is
   unmeasurable in that frame and the tube's **7.9–11.7 px, ±19 %** bracket must
   be closed another way or declared unclosable. Then a scale on the nose/bumper
   plane **or a proof that none is admissible**, then size and build, **every
   number tagged workshop-stage**. **This moves geometry and invalidates
   `rev25_hero34f.png`.** Strike ±2.145 / ±2.140 from §2 either way (§10.72).
2. **The residual 6.6/6.6/8.5 % pedestal — the scene→top bounce**, the only
   named candidate left. Remove `gal_warmer` / `gal_caddy0` / `gal_caddy1` and
   **re-derive the mask** (a visibility flag is barred by §10.56). Note the
   harness has **no cyclorama** (§10.78) — state that, do not silently fix it.
3. **§10.76** — only reopen with a `CREAM` reference or a same-class,
   differing-orientation pair. **Do not repair `W_DUST_FAC_UP` blind.**
4. Tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
5. A hero ONLY if geometry or artwork moves — **item 1 WILL move it.**
   `rev25_hero34f.png` photographs the current mesh and artwork until then.
6. Camera absolutely last.

## 7. THE COMMIT COUNT AND THE CONTENT FIGURES

This section is written LAST, after the final commit, and every figure in §1 was
read off a fresh-clone verification run rather than typed from memory. **This has
gone wrong in ELEVEN revisions during handoff assembly.** rev 23, 24, 25 and 26
were clean runs.

**FINAL COUNT: 126 commits, clean tree.**
