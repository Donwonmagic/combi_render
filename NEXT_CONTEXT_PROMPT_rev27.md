# NEXT CONTEXT PROMPT — rev 27
Please act as my expert. Continue the Señor Tacombi combi build. **Twenty-six
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 1 — read my memory BEFORE you read any code
`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17`, `-rev18`, `-rev19`,
`-rev20`, `-rev21`, `-rev22`, `-rev23`, `-rev24`, `-rev25`, then
**`/areas/tacombi-combi-3d-rev26.md`** (these are SEPARATE FILES; each
revision's file does NOT carry the next), then `/areas/tacombi-combi-sticker.md`,
then `/preferences.md`. Five prior contexts skipped them; one cost half a day and
produced the wrong body type. If you cannot read them, say so explicitly rather
than quietly proceeding.

**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner, the person this is for. **Do not ask me what the
real vehicle looks like.** Ask me what a PHOTOGRAPH shows — that has now paid
off fifteen times — but measure the surface, never ask about it.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)
See §1 below. **FOURTEEN bundle lines now, and the rev14b line is a `fetch`.**
rev 18 opened with rev 17 missing and rev 19 with rev 18 missing; **rev 20
through rev 26 all opened CLEAN** — do not assume either way, check.

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
`STATE.md` → `SPEC.md` §10, then §10.9 through §10.74 → this file →
**`HANDOFF_rev26.md`** → `HANDOFF_rev25.md` → `HANDOFF_rev24.md` →
`HANDOFF_rev23.md` → `HANDOFF_rev22.md` → `HANDOFF_rev21.md` →
`HANDOFF_rev20.md` → `HANDOFF_rev19.md` → `AUDIT_rev18_loft.md` →
`HANDOFF_rev18.md` → `LOFT_GROUND_rev15.md` → `AUDIT_rev12.md` →
`REF_MEASUREMENTS.md`.
`STATE.md` is machine-written by `audit.py`. **If it and any prose disagree, it
is right.** It has no known phantoms.

**Retirements that touch many numbers:** §10.11 (ground line, ~70 mm) and
§10.34 (hub chain, ~29 mm) and §10.29's ONE REF-wide correction (`:899`).
§10.46 corrects §10.37; **§10.45–48 retire NO §10.34 claim.** §10.57 retires
rev 20's boxes A and B. §10.59 RETIRES `H_ROOF`. §10.61 corrects the crossing
count. §10.62 ARMS item 4. §10.63 finds `folk_gen`'s bake frame stale.
§10.65 finds `solve_ctan` measured THE WHOLE SCENE through a top-only mask.
§10.66 finds rev 23 BROKE `folk_gen.composition()`. §10.67 REFUTES rev 24's own
work-item-2 brief. §10.68 REFUTES rev 24's `_ZB_AUTH` brief and re-bakes
fourteen-revision-old artwork. §10.69 takes `_RETIRED_VALUES` 5 → 15 rows.

**§10.70–74 are rev 26's, and THREE of them refute a brief I wrote myself:
§10.70 IDENTIFIES the `COUNTERTAN` pedestal as the settled-dust film and shows
§10.56 measured the wrong derivative; §10.71 finds `W_DUST_FAC_UP` anchored to
the WRONG MATERIAL; §10.72 finds work item 3 MALFORMED — both bumper numbers are
the factory catalogue halved; §10.73 finds work item 2 an ARTEFACT — a run mean
compared with a station value; §10.74 records two defects in rev 25's own
record.**

## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them
This has now paid off fifteen times. **My answers are not infallible — ask me
anyway, then measure what I say.** Show me a crop, mark the regions, give me
options, and **print the crop box**. rev 14's box was 120 px off; rev 19's
straddled a dark roof opening; rev 20's A and B straddled TWO MATERIALS; rev
21's redrawn N1 STILL straddled two materials; rev 22 found SPEC's OWN FOUNDING
CROP for `COUNTERTAN` straddling the counter top and the brass nosing; rev 23's
first draft of its own question figure straddled the A-pillar and the windscreen
aperture and was thrown away rather than sent; **rev 26's first draft put box A
on the green body ABOVE the tube it was pointing at and box B across the blade
and a foreground trolley rail — also thrown away rather than sent.**
**Say plainly whether a box is a POINTER or a SAMPLING WINDOW.** rev 26's were
pointers and no number was taken from them; rev 20/21's were sampling windows
and straddling was fatal.

**A CLASS GATE IS A PROBE TOO, and so is a BRIEF, a TARGET, a SUBAGENT'S
FINDING, a CITATION, a GUARD YOU JUST WROTE, and A COMMENT YOU ARE WRITING RIGHT
NOW.** Three of rev 17's four items came back with their briefs refuted; rev 19's
single item came back refuted three ways; rev 21 refuted all FIVE routes to its
own headline; rev 22 refuted its OWN item-3 target; rev 23 refuted TWO claims in
its own briefing; rev 24 REFUTED ITS OWN WORK ITEM 2 OUTRIGHT; rev 25 refuted its
own work item 2's brief AND a figure inside a comment it was writing at that
moment; **rev 26 refuted TWO of its own three work items and the founding
inference of the section its remaining item lived in.**

## Step 6 — the work
§6 below is the ordered list. **The loft is DONE and AUDITED. The arch is FIXED.
`H_ROOF` is RETIRED. `CREAM` is UNCHANGED. ITEM 4 IS ARMED and the show flank is
at 0.0 mm. `folk_gen.composition()` RUNS and was EXECUTED, not read. THE
ARTWORK IS CURRENT — proven this revision by THREE byte-identical re-bakes.
`COUNTERTAN`'s pedestal IS IDENTIFIED after six revisions. THE OLDEST UNDONE
ITEM IS NOW §10.71's wrong-material anchor, which is NEW and much better posed.**

## Step 7 — resolution
rev 25 shipped 4800×3200 in 20 strips, worst seam z 1.91. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips ~5–7 min each,
edge strips ~1.5 min. **`rev25_hero34f.png` photographs the CURRENT mesh and the
CURRENT artwork** — re-verified in rev 26 by re-baking three times to
byte-identical md5s. Do not re-shoot unless something moves.

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
**§0.2 is NOT self-arming and never was** — it compares MATERIAL NAMES.
`_retired_value_drift()` is the mechanism that sees retired VALUES; **never
widen it or add exemption tokens to silence it.**
**EVERY constant in `folk_gen.py` is PARSED and every parse RAISES** — never
re-type one back in. `_ceval` is deliberately tiny.
**The committed `tex/*.png` are CURRENT** — `swirl.png` `4ee4e09e`,
`swirl_b.png` **`d201597e`** *(rev 25 recorded `d2015971`; wrong in the eighth
character, the FILE was always right — §10.74)*, `nose.png` `b31ea156`.
**The bake is DETERMINISTIC** (fixed seeds 196301 / 771963) — rev 26 re-baked
three times and `git status tex/` was empty every time. A bake diff is always
provenance, never noise.
**Do NOT add a `_RETIRED_VALUES` row for the ±2.145 bumper faces** — now for the
STRONGER §10.72 reason: **neither value is live**, so a row would assert one is.
Never correct this vehicle toward the VW factory catalogue.

**NEW, rev 26 and now settled:**
**`COUNTERTAN`'s pedestal IS the settled-dust film** — dust carries
**57.1/52.6/36.6 %** of it, dust + spec + coat carry **89.3/87.9/84.8 %**.
**`COUNTERTAN` is UNCHANGED and nothing was tuned** — the dust film is a
modelled feature, not an error.
**`k` is 0.0368 shipped and 0.0871 with dust+spec+coat off — a factor 2.37.**
Any future solve must re-derive it; **never carry the old secant gain, and
never carry rev 24's "+40 %" either** — that is relative to a contaminated-mask
measurement and is not the fascia's.
**`T1_CTAN_WEAR=0` is TWO LEVERS** (albedo chain + Metallic). Not a pure ablation.
**`_DOOR_TOP_AUTH` STAYS at 1.8140** — §10.73 settles it at **0.315 mm**, not
4.2 mm. **No re-bake is owed.** `DOOR_H = 1.013467`.
**Both ±2.145 and ±2.140 are the factory catalogue halved** (4.290/2 and
4.280/2, same diff hunk of `27f6ee6`). **Neither is measured.** `X_BUMP_F/R`
are **DEAD** — zero read sites. The mesh was **fitted to the constant**
(`BUMP_OFF`'s own comment), so it cannot arbitrate.

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
  GUARD, AND INCLUDING WHEN YOU ARE WRITING IT RIGHT NOW.**
* **A MASK IS NOT A MEASUREMENT UNTIL THE MEASURED FRAME IS ISOLATED TOO.**
* **CHECK WHETHER YOUR INSTRUMENT'S LIGHT RIG IS THE ONE YOU THINK.**
* **A MAGNITUDE CAN BE EXACTLY RIGHT AND THE CONCLUSION STILL WRONG. WEIGHT AN
  ERROR BY WHAT IT ACTUALLY TOUCHES.**
* **AND ITS CONVERSE: A SMALL MAGNITUDE DOES NOT MEAN A SMALL CONTRIBUTION,
  WHEN THE DERIVATIVE YOU MEASURED IS NOT THE ONE YOUR CONCLUSION IS ABOUT.**
  §10.56 ablated the dust film, saw the top's radiance move only +4 %, and
  called it refuted. Removing a mix of coverage `f` and base-independent colour
  `D` moves radiance by `f(A−D)` — small *because* the deposit is nearly the
  base's colour — while contributing `f·D` to the pedestal, which is large.
  **Five revisions searched elsewhere.** *(NEW, rev 26)*
* **A CONSTANT CAN BE SOLVED AGAINST THE WRONG MATERIAL AND ITS OWN LIVE ASSERT
  WILL NEVER SEE IT** — because the assert does not read the material the
  surface actually carries. `W_DUST_FAC_UP` passes at 0.0001 against
  `COUNTERCREAM` and fails at 0.1600 against `COUNTERTAN`, the material that is
  actually on the counter top. **Both halves entered in one commit.**
  *(NEW, rev 26)*
* **BEFORE ADJUDICATING TWO DISAGREEING CONSTANTS, CHECK THEY DENOTE THE SAME
  QUANTITY, AND CHECK WHERE EACH CAME FROM.** `git log -S` settled the bumper
  question in one command: both numbers are one catalogue figure halved, from
  the same diff hunk. **The question was malformed, not open.** *(NEW, rev 26)*
* **A MEAN IS NOT A STATION VALUE.** rev 25's "4.2 mm" compared the mean of a
  crowned five-knot run with a value used at a single station. Like for like it
  is 0.315 mm. **Ask what statistic the consuming line needs.** *(NEW, rev 26)*
* **A RETIRED VALUE RE-EXPRESSED IN ANOTHER FORM IS INVISIBLE TO A SUBSTRING
  GUARD.** The answer is another ROW, never a looser rule.
* **WHEN A CONTROL FAILS, THE CONTROL IS THE FINDING — but check the control's
  own premise first.**
* **AN ARC LENGTH IS NOT A PENETRATION DEPTH.**
* **DO NOT INHERIT A GUARD'S RATIONALE ALONG WITH ITS SHAPE.**
* **DO NOT ARM A GUARD AT ZERO AGAINST GEOMETRY NOBODY HAS PHOTOGRAPHED.**
* **A RAY-VISIBILITY FLAG IS NOT AN ABLATION.** Remove the ALBEDO.
* **AND CHECK THE LEVER REACHES ONLY WHAT YOU THINK.** `Dust` reaches Base
  Color alone; `Wear` also drops Metallic and is therefore two levers.
  *(EXTENDED, rev 26)*
* **Build the CONTROL first and prove it is a no-op, then run the experiment —
  and CHECK THE CONTROL ITSELF.**
* **AN ILLUMINANT REFERENCE MUST CARRY SUBSTANTIAL ALBEDO IN ALL THREE
  CHANNELS.**
* **BEFORE DE-ILLUMINATING ANYTHING, TEST WHETHER A NEUTRAL TRANSFORM CAN RELATE
  THE TWO FRAMES AT ALL.**
* **A SUBAGENT'S FINDING IS A CLAIM, NOT A MEASUREMENT.** rev 26 ran two and
  **verified every load-bearing claim by hand** — the door-top arithmetic
  re-implemented from `t1_shell`'s own `_resample`/`_smooth`, the bumper
  provenance by `git log -S` and the diff hunk, the dust coverage by the live
  assert, and the pedestal by four fresh renders.
* **VERIFY A CODE CHANGE BY EXECUTING IT, NOT BY READING IT** — §10.66 cost a
  revision. rev 26 changed only comments in `folk_gen.py` and still imported it,
  ran `composition()` on both sides, and re-baked three times to byte-identical
  md5s. *(REINFORCED, rev 26)*
* **A CARRIED-FORWARD FIGURE IS A CLAIM TOO — AND SO IS ITS CITATION.** The
  bumper row's `(:191)` was **born stale in the commit that wrote it**.
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
* **AND A CONTENT CHECK MUST BE SATISFIABLE ON A FRESH CLONE.** rev 25's §1
  asked a fresh clone to `ls` a file its own §7 explains was deliberately
  removed from the repo. **Delete such a check; never loosen it.** *(NEW, rev 26)*
* **Do not put a figure in an acceptance test — or a HANDOFF — unless you
  watched it print.**
* **If a change trips a guard, THAT IS THE GUARD WORKING. Never widen it.**
* **A probe that cannot answer must return None, not an endpoint.**
* When a finding breaks something independently locked, measure it a third way.
* **Watch for the lamppost** — `ref_side.jpg` columns 62–79 have produced four
  confident wrong numbers about the front of the vehicle, and they are why the
  front bumper face has never been measured. **`ref_workshop.jpg` has no
  lamppost.**
* A single shell command is killed at 10 minutes. This box has 2 cores — spawn
  2–4 `Agent`s on **disjoint files**, read-only for audits, rather than a
  Workflow. **A hero strip killed at the 10-minute limit may still have written
  a valid file — let the SEAM CHECK adjudicate it.**
* **Backticks in `git commit -m` hit shell substitution.** Use `git commit -F`.
* **The device bridge may drop mid-transfer.** Try the direct call FIRST — rev
  26 moved fourteen bundles in ONE call — and fall back to `split` + parallel
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
git pull --ff-only ../tacombi_rev26_incremental.bundle HEAD      # -> see §7
```
**If a pull says "Need to specify how to reconcile divergent branches", STOP.**

Content checks — **the first eight reach the TIP on purpose.** Note there is no
`ls` of a hero here: **the hero is gitignored and lives only on my disk**, and
rev 25's prompt asked a fresh clone for one. §10.74.
```bash
git status                                              # clean
grep -c '### 10.70' SPEC.md                             # __  rev 26
grep -c '### 10.73' SPEC.md                             # __  rev 26
grep -c '### 10.74' SPEC.md                             # __  rev 26
grep -c 'PUBLISHED_CLEAN' probe_ctan_pedestal.py        # __  rev 26
grep -c 'SPEC 10.73' folk_gen.py                        # __  rev 26
grep -c 'd201597e' SPEC.md                              # __  rev 26
ls HANDOFF_rev26.md probe_ctan_pedestal.py              #     rev 26
grep -c '### 10.68' SPEC.md                             # __  ANCESTOR rev 25
grep -c '_ceval' folk_gen.py                            # __  ANCESTOR rev 25
grep -c '### 10.65' SPEC.md                             # __  ANCESTOR rev 24
grep -c '_retired_value_drift' verify.py                # __  ANCESTOR rev 24
grep -c '### 10.62' SPEC.md                             # __  ANCESTOR rev 23
grep -c 'OFF_CROSS_BASELINE' t1_shell.py                # __  ANCESTOR rev 23
grep -c 'H_ROOF_REGRESSION' verify.py                   # __  ANCESTOR rev 22
grep -c '### 10.57' SPEC.md                             # __  ANCESTOR rev 21
grep -c 'T1_CTAN_NOBOUNCE' shader_solve.py              # __  ANCESTOR rev 20
grep -c '_BODY' cream_rms.py                            # __  ANCESTOR rev 19
grep -c '_arch_lip_z' verify.py                         # __  ANCESTOR rev 18
grep -c 'matte_tap' studio.py                           # __  ANCESTOR rev 17
grep -c '_coons_cap' t1_core.py                         # __  ANCESTOR rev 16
grep -c 'The threshold is not the parameter' post.py    # __  ANCESTOR rev 13
```
**EVERY VALUE ABOVE IS FILLED FROM A FRESH-CLONE VERIFICATION RUN.** Never type
one from memory — `grep -c` counts LINES, not occurrences, and that has produced
a wrong figure in five revisions.

Ancestry:
```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```
**Known limitation, stated rather than hidden:** the ancestry loop's newest
entry is a rev-19 commit, because a hash cannot be written into the file that
contains it without amending, and rev 14 learned not to amend. **The TIP is
covered by the rev-26 content greps instead.**

Texture md5s on the restored tree — **all three must match, and `swirl_b` is the
one rev 25 recorded wrong:**
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
25 OR 26, AND NO ARTWORK MOVED IN REV 26.**

## 3. What rev 26 changed — `HANDOFF_rev26.md` has the full account
- **`SPEC.md`** — §10.70 through §10.74, the change log, and the corrected
  `swirl_b` md5.
- **`probe_ctan_pedestal.py`** — NEW, read-only. The four-arm fit, which
  **ASSERTS** the harness control against §10.65's published pedestal rather
  than claiming it in prose, and prints what is NOT claimed.
- **`folk_gen.py`** — COMMENTS ONLY. §10.73's finding recorded at
  `_DOOR_TOP_AUTH`, and `DOOR_H`'s `# ~1.017 m` corrected to the **1.013467**
  the line actually computes. **Verified by EXECUTION**: imported, both sides of
  `composition()` called, and **three re-bakes to byte-identical md5s**.
- **`CREAM`, `COUNTERTAN`, `RED`, the rake, the roof, ALL GEOMETRY and ALL THREE
  TEXTURES UNCHANGED.**

**Things you must not silently undo — `HANDOFF_rev26.md` §4**, and rev 25's §4,
rev 24's §4, rev 23's §4, rev 22's §3, rev 21's §4, rev 20's §4, rev 19's §4 and
rev 18's §4 all still stand in full.

## 4. Still open
See `HANDOFF_rev26.md` §5 for the full list. The ones that matter:
- **§10.71 — `W_DUST_FAC_UP = 0.7313` is anchored to `COUNTERCREAM` on a
  surface that carries `COUNTERTAN`.** Its live assert passes at 0.0001 against
  the cream and fails at **0.1600** against the tan — 80× its own tolerance —
  and it cannot see the difference because it never reads `COUNTERTAN`. **Both
  halves entered in one commit.** NEW, and now the highest-value open item,
  because §10.70 shows this constant dominates the counter top's appearance.
- **The residual pedestal, 6.6 / 6.6 / 8.5 %** — NOT identified. Never-ablated:
  `T1_WORLD`, `T1_CYCALB`, `T1_GAL_LUM`, scene→top bounce, and the grazing lobe
  (`T1_CTAN_SP=0` may leave F90 = 1 — **UNVERIFIED, and free to test**).
- **THE FRONT BUMPER FACE IS UNMEASURED** — both catalogue values struck.
- **`CREAM`** — needs a same-light, same-CLASS, three-channel reference. **Does
  not exist in the three photographs.**
- **THE ABSOLUTE ROOF HEIGHT** — 1.960 retired, nothing replaced it.
- **THE OFF FLANK** — two mutually contradictory **E** features, 804.9 mm.
- **The cab door's true top edge** — both candidates authored; **unmeasurable**
  on the admissible set (§10.73).
- `PLATE_W = 0.3300` has no provenance. `probe_rev16.py:90` prints `xa` vs `xa`.
  `X_NOSE`/`X_TAIL` parsed in `folk_gen`, never LOADED.

## 5. FIRST QUESTION FOR THE OWNER
**ONE QUESTION IS OUTSTANDING**, sent in rev 26 with printed crop boxes on
`ref_workshop.jpg` — the one frame where the front bumper is not occluded by the
lamppost. **A: the upper tube. B: the lower blade. C: the vertical post between
them.** Which belong to the vehicle rather than to shop hardware? **The model
has no member for A at all** — it builds a blade plus two 62 × 30 mm brackets.
If it went unanswered, re-ask it; §10.72 is blocked on it.

What would still move the most is one photograph: **a head-on rear (or front)
elevation from roof height or above, with the counter and the lids clear of the
section.** It is the only realistic route to closing **BOTH** `CREAM` **and**
the absolute roof height. A clear view of the **off flank** would additionally
close 804.9 mm of unadjudicated crossing.

## 6. Ordered work list for rev 27
1. **§10.71's wrong-material anchor** — settle it with a measurement, then decide
   whether `W_DUST_FAC_UP` or `_UP_MEASURED`'s label is wrong. **Do not repair it
   blind; it moves the shipped build.** Highest-value open item.
2. **The residual 6.6/6.6/8.5 % pedestal** — `T1_WORLD=0`, `T1_CYCALB=0`,
   `T1_GAL_LUM=0`, one render each, overrides already exist. **Test the F90
   question FIRST** — it is free and decides whether rev 26's arm 4 was complete.
3. **The front bumper**, once the owner's reading lands — and strike ±2.145 /
   ±2.140 from §2 either way.
4. Tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
5. A hero ONLY if geometry or artwork moves. `rev25_hero34f.png` photographs both.
6. Camera absolutely last.

## 7. THE COMMIT COUNT AND THE CONTENT FIGURES
This section is written LAST, after the final commit, and every figure in §1 was
read off a fresh-clone verification run rather than typed from memory. **This has
gone wrong in ELEVEN revisions during handoff assembly.** rev 23, rev 24 and
rev 25 were clean runs.

**FINAL COUNT: __ commits, clean tree.**
