# NEXT CONTEXT PROMPT — rev 32

Please act as my expert. Continue the Señor Tacombi combi build. **Thirty-one
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 0 — CHECK A FOLDER IS CONNECTED BEFORE YOU PLAN ANYTHING

Call `get_device_info`; if `connectedFolders` is empty, request
`~/Desktop/tacombi_bus_render` immediately and say so plainly. It timed out
unanswered in rev 28 and rev 29; **it was granted on the FIRST request in rev 30
AND AGAIN IN REV 31.** Do not assume either way — send it and say you have.

**THE BRIDGE HAS A THROUGHPUT CEILING, NOT JUST A SIZE ONE — CONFIRMED TWICE.**
`device_stage_files` times out on files above ~3 MB. **Only two files need it:**
the 19.5 MB base bundle (7 parts) and the 8.5 MB `rev14_unified` (3 parts).
**Everything rev15–rev31 is under 3 MB and crosses whole**, so this costs about
6 calls, not the 10 rev 30 budgeted. Split with `device_bash`, stage 1–2 per
call, `cat` back, **check md5 on both sides** — it matched in rev 30 and rev 31.

**THE BRIDGE ALSO DROPS MID-SESSION.** It dropped once in rev 31 and came back
on its own about ten minutes later. Do not retry in a loop; do cloud-side work
and come back to it. **`ref_workshop.jpg`, `ref_side.jpg` and `ref_rear34.jpg`
are IN THE REPO**, so all reference measurement survives a bridge outage.

## Step 1 — read my memory BEFORE you read any code

`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17` … `-rev30`, then
**`/areas/tacombi-combi-3d-rev31.md`** (SEPARATE FILES; each revision's file does
NOT carry the next), then `/areas/tacombi-combi-sticker.md`, then
`/preferences.md`. If you cannot read them, say so explicitly.

**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner. **Do not ask me what the real vehicle looks like.**
Ask me what a PHOTOGRAPH shows — that has now paid off twenty-one times.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)

See §1. **NINETEEN bundle lines now, and the rev14b line is a `fetch` that must
come BEFORE rev15.** rev 20 through rev 31 all restored CLEAN — do not assume
either way, check.

## Step 3 — install Blender 4.5.3 and run BOTH guards before proposing anything

```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
/tmp/blender/4.5/python/bin/python3.11 -m pip install pillow scipy
```

That pip line is required. Guards are `T1_SUB=n T1_VERIFY=1 blender -b
--python build.py` and `T1_SUB=n blender -b --python audit.py`. Report the
guards' ACTUAL output, both levels. **`audit.py` rewrites `STATE.md` every run —
`git checkout STATE.md` after.**

**THE GUARDS ARE 0 fail / 0 WARN.** **NO GEOMETRY MOVED IN REV 31** — the last
geometry change is still rev 30's. **THE HERO IS NOT OWED: `rev30_hero34f.png`
IS A RENDER OF THE REV-30 BUILD** and rev 31 proved it by content. Read §10.84.

## Step 4 — read, in this order

`STATE.md` → `SPEC.md` §10, then §10.9 through §10.84 → this file →
**`HANDOFF_rev31.md`** → `HANDOFF_rev30.md` → … → `AUDIT_rev18_loft.md` →
`LOFT_GROUND_rev15.md` → `AUDIT_rev12.md` → `REF_MEASUREMENTS.md`.
`STATE.md` is machine-written; **if it and any prose disagree, it is right.**

**§10.84 IS REV 31's. IT MOVES NO GEOMETRY AND IT CORRECTS §10.83 IN PLACE** —
that section's refutation of "post at the vehicle's centreline" is **DOWNGRADED
FROM REFUTED TO UNDECIDED**, because its two terms are at DIFFERENT DEPTHS.

**§10.85 IS REV 31b's AND IT IS UPSTREAM OF BOTH.** He looked at the rev-31
figure and said the apex marking did not look right. **He was right.**
REF §9's "two-tone V apex (centreline) (311.5, 669) ± 4 px" **IS NOT THE APEX**
— the V's arms have not converged there, the over-rider bar's top edge is at
`v = 672.5` and occludes the vertex, and the published point is the V's **RIGHT
ARM's occlusion point at the bar**. The arms, traced and intersected, cross at
**u = 288.8 ± 3 px**: a **−22.7 px** shift. `REF_MEASUREMENTS.md` is corrected in
place. **Everything anchored on 311.5 inherits this.**

## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them

This has now paid off twenty-one times. Show me a crop, mark the regions, give
me options, **print the crop box**, and **say plainly whether a box is a POINTER
or a SAMPLING WINDOW** — rev 30's two boxes were SAMPLING WINDOWS and said so;
**rev 31's four were ALL POINTERS and said so, because rev 31 took no samples.**
Show the photograph **BESIDE a render of the current build**.

**A CLASS GATE IS A PROBE TOO, and so is a BRIEF, a TARGET, a SUBAGENT'S
FINDING, A CITATION, A GUARD YOU JUST WROTE, AN ESTIMATOR YOU JUST BUILT,
A QUESTION YOU ARE ABOUT TO ASK ME, A THRESHOLD, A SAMPLING WINDOW, A NULL
PATCH, and — NEW, rev 31 — A REFUTATION SOMEONE ELSE ALREADY BANKED, and THE
AXIS YOUR DETECTOR SEARCHES ALONG.**

rev 31 killed its own first probe on its own controls, killed its own first seam
detector twice (wrong axis, then no power), and named a process defect that
destroyed its own work.

**DO NOT ASK ME WHAT MEASUREMENT CAN ANSWER.** rev 31 refuted the brief's whole
route by measurement rather than asking me about it, and the two questions I did
get were the ones only I could answer. **AND, NEW: MY ANSWER MAY NOT BE ONE OF
YOUR OPTIONS.** Both of rev 31's answers were outside the offered set and both
were better than the set. **Leave room for that and re-examine the frame against
what I actually said.**

## Step 6 — the work

§6 below is the ordered list. **THE OLDEST UNDONE ITEM IS STILL THE OVER-RIDER
POST, but it is no longer blocked on a READING — it is blocked on a
CONSTRUCTION**, and §10.84 names it.

## Step 7 — resolution

rev 25 shipped 4800×3200 in 20 strips, worst seam z 1.91. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips ~5–7 min each,
edge strips ~1.5 min. **`hero.py` STRIPS IN ROW SPACE — SEAMS ARE HORIZONTAL.**
rev 31 built a seam detector on the wrong axis; do not repeat it.

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

Everything in the rev-31 prompt's equivalent section still stands, **with ONE
REMOVAL AND TWO ADDITIONS.**

**REMOVED — §10.75's "post at the vehicle's centreline" is NO LONGER SETTLED.**
rev 30 listed it as REFUTED and rev 31 downgraded it to **UNDECIDED** (§10.84).
Its two terms are at different depths — the V apex is on the NOSE SKIN, the post
stands in the BUMPER plane forward of it by a standoff §10.83 itself grades "A
CHOICE, not a reading". The whole offset is **54.0 px** and the parallax sign is
unestablished at **1.38 σ**. **It is NOT hereby claimed the post IS on the
centreline. The post stays UNBUILT. Do not treat either position as settled.**

**THE FRONT OVER-RIDER BAR IS BUILT (§10.83)**, WORKSHOP-STAGE, on a ratio to
the headlamp aperture measured at the tube's own station. **`BAR_DIA` and
`BAR_RISE` are written as `ratio × APERTURE_M` and must stay that way** — the
anchor is a **CATALOGUE** 0.180 m, SPEC 10.72's struck class.

**The 10.83 verify row's reference is FROZEN IN `verify.py`, not read from
`t1_detail`.** Its window is `x > 2.100`, not `x > 2.132`.

**NEW, rev 31 — THE POST IS BAR-TO-BLADE ONLY.** *[stated]* "bar to blade only,
much like the view of the other bar which shows us a triangular bar extending
from the bumper upwards and away from the body panel". **It does NOT run back to
the body panel.** So its depth IS the bumper plane and the parallax against the
nose skin is certainly present.

**NEW, rev 31 — THE BAR'S FAR END IS PRESENT BUT CONFOUNDED.** *[stated]*
"Appears to be covering the bumper, the post, and the far end of the bar."
The far end is a **superposition of three members inside a ~29 px blob**
(`u 203–232, v 626–702`), with **brace structure SPEC had never recorded**. The
bar's two ends therefore DO bracket the post, and that ~29 px is the precision
bound on any construction that uses them.

**REF §9's V-APEX ANCHOR IS CORRECTED: `u = 288.8 ± 3 px`, NOT 311.5.** The
published point was the V's right arm disappearing behind the over-rider bar —
it lies **3.98 px** from that arm and **30.75 px** from the other, and *a vertex
is equidistant from both*. The band is **SYSTEMATIC, from a half-band split**; a
bootstrap returns ±0.2 px and **that is a false precision**, pricing scatter
rather than the 0.93× extrapolation's straightness assumption. Only the COLUMN
is published — the V is radiused at the tip, so the crossing's ROW is not a
measurement. **The post's offset becomes +76.7 px, not +54.0 — AND THAT CHANGES
NOTHING FOR §10.84**, whose objection was the DEPTH mismatch, not the offset's
size. **§10.83's centreline claim stays UNDECIDED.**

**THE VEHICLE HAS NO RECOVERABLE FORE-AFT VANISHING POINT.** Three long edges
pass an rms gate (two at **rms 0.091 and 0.096 px**) and their pairwise
intersections are **u = +1529, +1284, −5843** — they do not converge and they
change side. `t1_mats.z_belt(x)` is a SLOPED line and the roof carries rake and
crown, so those edges are genuinely not parallel. **Do not try to fit one.**

**THE HERO IS SHOT AND PROVED BY CONTENT.** Backdrop bit-identical to rev 25
(max diff 0), difference **41.22 % inside the silhouette vs 0.21 % outside**,
concentrated on up-faces. Seams below **0.10 code values** against a graded
positive control. **Do not re-shoot it to check.**

## Hard-won rules — every one was learned by breaking it

Every rule in the rev-31 prompt still stands. **NEW in rev 31:**

* **A REFUTATION WHOSE TWO TERMS ARE NOT COMMENSURABLE MEASURES NOTHING.** A
  fifth tautology class, one level above a guard: *two features at different
  depths are not two readings of one quantity.*
* **CHECK WHICH AXIS YOUR DETECTOR SEARCHES ALONG BEFORE YOU BELIEVE IT.**
* **A DETECTOR WITH NO POWER IS NOT A NEGATIVE RESULT.** Grade the positive
  control until it fails, and publish the level at which it does.
* **NEVER `git checkout` A FILE TO UNDO A FALSIFICATION ARM.** Commit the real
  work first, or the arm eats it. It ate a whole SPEC section in rev 31.
* **A SETTLED-LIST ENTRY IS A PROBE TOO.** rev 31's most useful finding was that
  something already banked as settled could not carry its own weight.
* **MY ANSWER MAY NOT BE ONE OF YOUR OPTIONS.**
* **A FEATURE NAMED IN A REFERENCE FILE IS A PROBE TOO — CHECK THAT THE NAMED
  POINT IS THE THING THE NAME SAYS.** REF §9's "apex" carried that word and a
  ±4 px band through nine revisions and into two SPEC sections, and it was a
  point on an arm.
* **AN OCCLUDER ADDED TO THE MODEL LATER CAN INVALIDATE A READING TAKEN BEFORE
  IT.** The bar that hides this vertex was measured and built in rev 30, from
  this same frame, without anyone noticing it lands on the anchor.
* **A BOOTSTRAP PRICES SCATTER, NOT YOUR MODEL ASSUMPTION.** When the answer is
  an extrapolation, the band comes from splitting the data, not from resampling
  it.

---

> **THE STANDARD, in the owner's words.** The final product should be nearly
> indistinguishable from the original. **Any single measurement off is
> unacceptable.** The criterion is PER-MEASUREMENT. And above clinical
> accuracy: *"I want the owner to remember standing in the kombi, in this very
> picture that was provided."* — **that owner is the restaurant's owner.**

---

## 1. Restore and verify — BY CONTENT, never by hash or commit count

```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull --ff-only ../tacombi_rev14_unified.bundle HEAD          # -> 59
git fetch ../tacombi_rev14b_incremental.bundle HEAD:refs/heads/b14   # FETCH, BEFORE rev15
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
git pull --ff-only ../tacombi_rev29_incremental.bundle HEAD      # -> 135
git pull --ff-only ../tacombi_rev30_incremental.bundle HEAD      # -> 148
git pull --ff-only ../tacombi_rev31_incremental.bundle HEAD      # -> 158
```

**If a pull says "Need to specify how to reconcile divergent branches", STOP.**

Content checks — **the first eleven reach the TIP on purpose.** The hero is
gitignored and lives only on my disk.

```bash
git status                                              # clean
grep -c '### 10.85' SPEC.md                             # 1   rev 31b
grep -c 'occlusion point' SPEC.md                       # 1   rev 31b
grep -c 'equidistant' SPEC.md                           # 1   rev 31b
grep -c '76.7' SPEC.md                                  # 1   rev 31b
grep -c '288.8' SPEC.md                                 # 2   rev 31b
grep -c 'SPEC 10.85' REF_MEASUREMENTS.md                # 1   rev 31b
grep -c 'OCCLUSION POINT' REF_MEASUREMENTS.md           # 1   rev 31b
grep -c '288.8' REF_MEASUREMENTS.md                     # 1   rev 31b
grep -c 'FALSE PRECISION' probe_v_apex.py               # 2   rev 31b
grep -c 'CURVATURE' probe_v_apex.py                     # 2   rev 31b
grep -c 'REF_TOL' probe_v_apex.py                       # 3   rev 31b
grep -c '### 10.84' SPEC.md                             # 1   rev 31
grep -c 'DOWNGRADED TO' SPEC.md                         # 1   rev 31
grep -c 'HIS TWO ANSWERS' SPEC.md                       # 1   rev 31
grep -c 'UNDECIDED' SPEC.md                             # 5   rev 31 + 31b
grep -c 'commensurable' SPEC.md                         # 2   rev 31 + 31b
grep -c 'bumper-plane' SPEC.md                          # 2   rev 31
grep -c '10.84' verify.py                               # 3   rev 31
grep -c 'UNDECIDED' verify.py                           # 2   rev 31
grep -c 'ARM 1 IS DEAD' probe_orb_post.py               # 1   rev 31
grep -c 'V_APEX_TOL' probe_orb_post.py                  # 5   rev 31
grep -c 'different depths' probe_orb_post.py            # 3   rev 31
grep -c 'POINTER' mark_rev31_q.py                       # 5   rev 31
grep -c 'SAMPLING WINDOW' mark_rev31_q.py               # 3   rev 31
ls HANDOFF_rev31.md STATE_rev31.md probe_orb_post.py mark_rev31_q.py rev31_q_post.png
ls probe_v_apex.py rev31b_q_apex.png
grep -c '### 10.83' SPEC.md                             # 1   ANCESTOR rev 30
grep -c 'ORB_RISE_SPEC' verify.py                       # 6   ANCESTOR rev 30
grep -c 'BAR_RATIO' t1_detail.py                        # 3   ANCESTOR rev 30
grep -c 'overrider_bar' build.py                        # 1   ANCESTOR rev 30
grep -c 'W_h' probe_orb_hoop.py                         # 6   ANCESTOR rev 30
grep -c '### 10.82' SPEC.md                             # 1   ANCESTOR rev 29
grep -c 'W_DUST_FAC_UP' probe_dust_scope.py             # 14  ANCESTOR rev 29
grep -c '### 10.80' SPEC.md                             # 1   ANCESTOR rev 28
grep -c 'CORE' probe_psf_owner.py                       # 12  ANCESTOR rev 28
grep -c 'SPEC 10.76' t1_mats.py                         # 4   ANCESTOR rev 27
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

**EVERY VALUE ABOVE WAS FILLED FROM A FRESH-CLONE VERIFICATION RUN.** Never type
one from memory — `grep -c` counts LINES, not occurrences, and that has produced
a wrong figure in eleven revisions. **rev 31 caught one live:**
`grep -c 'C1 FAIL' probe_orb_post.py` reads **0**, because that string is built
by an f-string and never appears as a literal. It was dropped rather than
published.

Ancestry — **rev 31 adds `e792d73`, the rev-30 TIP:**

```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201 b08e424 e792d73; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```

Texture md5s — **all three must match, and rev 31 changed NO artwork:**

```bash
md5sum tex/swirl.png tex/swirl_b.png tex/nose.png
# 4ee4e09e...   d201597e...   b31ea156...
```

## 2. Both guards, and the figures I watched print

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 0 warn** | **0 fail, 0 warn** |
| audit.py | **0 fail, 0 warn** | **0 fail, 0 warn** |
| roof crown @ rear axle | **1.9835** (baseline 1.9835, −0.0 mm) | **1.9833** (−0.2 mm) |
| rear arch lip → gap | **0.3722 → 39.7 mm** | same |
| front arch (control) | **0.3732 → 40.7 mm** | same |
| rake | **17.75 mm/m (locked 17.75)** | same |
| dims | L=4.065 W=1.750 | same |
| cut roof hole | **68564v** | **252749v** |
| objects at `materials:` | **127** | **127** |
| shut line × aperture, SHOW / OFF | **0.0 mm / 804.9 mm** | same |
| `CARGO_GAP` samples | **154** | same |
| bay widths | **0.516 0.515 0.516** | same |
| over-rider row | **97.51 mm above the blade top, dia 24.97 mm** | same |

Also: **186 meshes**; 42 materials; 5 constant-rough; **0 non-manifold**;
band 1.372–1.775. **EVERY GEOMETRY FIGURE IS IDENTICAL TO REV 30's, WHICH WAS
IDENTICAL TO REV 23's EXCEPT THE COUNTS.**

## 3. What rev 31 changed — `HANDOFF_rev31.md` has the full account

- **`SPEC.md`** — NEW §10.84; **§10.83 corrected IN PLACE** (REFUTED →
  UNDECIDED on the centreline claim only).
- **`verify.py`** — the `_RETIRED_VALUES` row for "post at the vehicle's
  centreline" is **KEPT**, only its stated reason corrected. **Watched FIRE**
  after the commit: 1 fail against the clean tree's 0.
- **`probe_orb_post.py`**, **`mark_rev31_q.py`**, **`rev31_q_post.png`**,
  **`probe_v_apex.py`**, **`rev31b_q_apex.png`** — all NEW, all READ-ONLY.
- **`REF_MEASUREMENTS.md`** — §9's V-apex line **corrected in place** (§10.85).
- **`SPEC.md`** — also NEW §10.85.
- **NO GEOMETRY. NO SHADER. NO ARTWORK.** `CREAM`, `COUNTERTAN`,
  `COUNTERCREAM`, `RED`, the rake, the roof, the over-rider bar and all three
  textures UNCHANGED.

**Things you must not silently undo — `HANDOFF_rev31.md` §6**, and rev 30's §3
through rev 18's §4 all still stand in full.

## 4. Still open

- **THE OVER-RIDER POST.** No longer blocked on a READING — blocked on a
  CONSTRUCTION. The bar's two ends bracket it; the near end is a clean hoop
  (`u ≈ 468–490`), the far end is a **~29 px superposition** (`u 203–232`). A
  projective midpoint needs the transverse VP or an argument that bounds it, and
  **the naive midpoint is NOT the projective one — do not take it.**
- **§10.83's centreline claim is UNDECIDED.** Neither position is settled.
- **EVERYTHING ELSE IN REF §9 THAT USED 311.5 AS THE CENTRELINE.** §10.85 fixed
  the anchor; it did NOT sweep the file for consumers of the old value. **Do
  that.** REF §9's absolute-height block derives from centreline scale.
- **A HERO IS NO LONGER OWED.**
- **§10.70's percentages must be RE-RUN** before being quoted again.
- **§10.82's unasked surfaces** — bumper top, rim barrels, hub caps. **The
  workshop frame shows all three; rev 31 did not ask, having spent its two
  questions on the post.**
- **THE FRONT BUMPER FACE IS UNMEASURED.** **`CREAM`.** **THE ABSOLUTE ROOF
  HEIGHT.** **THE OFF FLANK, 804.9 mm.** `COUNTERTAN` 34.0 % short in B.
- `GAL_SKY` dead lever. `PLATE_W = 0.3300` no provenance.
  `probe_rev16.py:90` prints `xa` vs `xa`.

## 5. FIRST QUESTIONS FOR THE OWNER — NONE OUTSTANDING

Both of rev 31's questions were answered and **both were answered OUTSIDE the
options offered, and both answers were better than the options.** What would
still move the most is one photograph: **a head-on rear (or front) elevation from
roof height or above, with the counter and the lids clear of the section** — the
only realistic route to closing `CREAM`, the absolute roof height and the B
residual. A clear view of the **off flank** closes 804.9 mm. **And for the POST:
any frame showing the FRONT of the vehicle square-on collapses the lateral-scale
problem entirely.**

## 6. Ordered work list for rev 32

1. **SWEEP REF §9 AND SPEC FOR CONSUMERS OF THE OLD 311.5 ANCHOR.** §10.85
   corrected the anchor in place but did not chase what fed on it.
2. **THE OVER-RIDER POST, by the bar's own two ends.** Bound or construct the
   transverse VP; express the post as a **FRACTION of the bar's half-width**, so
   it inherits `BAR_HALF_Y`'s grade E instead of adding a new lateral choice.
   Carry the far end's ~29 px as the stated precision, and **say before you
   start whether it will close.**
3. **§10.82's unasked surfaces** — bumper top, rim barrels, hub caps. The
   workshop frame shows all three. **Ask.**
4. **Re-run §10.70's arms** on the post-retirement build before quoting any of
   its percentages, then the scene→top bounce. The harness has **no cyclorama**
   (§10.78) — state that, do not silently fix it.
5. Tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
6. Camera absolutely last.

## 7. THE COMMIT COUNT AND THE CONTENT FIGURES

This section is written LAST, after the final commit, and every figure in §1 was
read off a fresh-clone verification run rather than typed from memory. **This has
gone wrong in ELEVEN revisions during handoff assembly, and rev 31 caught a
twelfth live** — `grep -c 'C1 FAIL' probe_orb_post.py` reads 0 because the string
is assembled by an f-string. It was dropped, not published.

**FINAL COUNT: 158 commits, clean tree.** *(Verified: this line lands in commit
158 itself, which is what makes it true — the count lands in its own commit, rev 29's pattern.)*

**A THIRD TRAP, AND THIS ONE IS THE PUREST INSTANCE YET.** rev 31b's own
§10.85 text CONTAINS the words `UNDECIDED` and `commensurable`, so it silently
moved two of rev 31's OWN published grep counts from 4 -> 5 and 1 -> 2. Nothing
about those checks was wrong when written; **a later section in the same
revision invalidated them.** The fresh-clone run caught both. *A grep count is
invalidated by any later edit to the file it counts, including your own.*

**AND A SECOND GREP TRAP CAUGHT LIVE, rev 31b.** `grep -c 'equidistant'` and
`grep -c 'false precision'` on `probe_v_apex.py` both read **0** — the words live
in SPEC and the probe spells it `FALSE PRECISION` in caps. Read off the console,
corrected, and not published wrong. That is the second and third grep miss caught
this revision by running them rather than typing them.

**A PROCESS TRAP CAUGHT AND NAMED, rev 31.** I ran a falsification arm by
injecting a retired phrase into `SPEC.md`, then reverted it with
`git checkout SPEC.md` — **and that discarded the entire uncommitted §10.84 and
the §10.83 correction along with the injection.** Both had to be rewritten and
the arm re-run after the commit. **NEVER `git checkout` A FILE TO UNDO A
FALSIFICATION ARM WHILE THAT FILE CARRIES UNCOMMITTED WORK.**
