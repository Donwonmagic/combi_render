# NEXT CONTEXT PROMPT — rev 33

Please act as my expert. Continue the Señor Tacombi combi build. **Thirty-two
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 0 — CHECK A FOLDER IS CONNECTED BEFORE YOU PLAN ANYTHING

Call `get_device_info`. **In rev 32 `~/Desktop/tacombi_bus_render` was ALREADY in
`connectedFolders` on the first call and no request was needed** — the first
revision where that was true. It timed out unanswered in rev 28 and rev 29, and
was granted on the first request in rev 30 and rev 31. **Do not assume any of
those three outcomes** — call it, and say plainly what came back.

**THE BRIDGE HAS A THROUGHPUT CEILING, NOT JUST A SIZE ONE — CONFIRMED THREE
TIMES.** `device_stage_files` times out on files above ~3 MB. **Three files now
need splitting:** the 19.5 MB base bundle (7 parts) and the 8.5 MB
`rev14_unified` (3 parts). **Everything rev15–rev32 is under 3 MB and crosses
whole** — `tacombi_rev32_incremental.bundle` is **2 376 375 bytes**, md5
`4bc11cec5d4ed536983524d0515bf974`, despite carrying two question PNGs.
*(An earlier draft of this file said rev 32's bundle was over the ceiling. It
had been cut from the rev-30 tip by mistake, so it carried rev 31's commits too
and measured 3.63 MB. Corrected before shipping: A BUNDLE'S SIZE IS A
MEASUREMENT TOO, and it depends on the base you cut it from.)*
Split with `device_bash`, stage 1–2 per call, `cat`
back, **check md5 on both sides** — it matched in rev 30, rev 31 and rev 32.

**TRANSIENT FAILURES ARE NOT DROPS.** In rev 32 two files inside one 19-file
batch returned `upload failed` and **both crossed on a single individual
retry**, and one `device_bash` call died on a Cloudflare **502** and worked on
retry. **The bridge also genuinely DROPS** — it dropped three times in rev 31
and came back on its own each time. Do not retry in a loop; do cloud-side work
and come back. **`ref_workshop.jpg`, `ref_side.jpg` and `ref_rear34.jpg` are IN
THE REPO**, so all reference measurement survives an outage.

## Step 1 — read my memory BEFORE you read any code

`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17` … `-rev31`, then
**`/areas/tacombi-combi-3d-rev32.md`** (SEPARATE FILES; each revision's file does
NOT carry the next), then `/areas/tacombi-combi-sticker.md`, then
`/preferences.md`. If you cannot read them, say so explicitly.

**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner. **Do not ask me what the real vehicle looks like.**
Ask me what a PHOTOGRAPH shows — that has now paid off twenty-one times.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)

See §1. **TWENTY bundle lines now, and the rev14b line is a `fetch` that must
come BEFORE rev15.** rev 20 through rev 32 all restored CLEAN — do not assume
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

**THE GUARDS ARE 0 fail / 0 WARN.** **NO GEOMETRY MOVED IN REV 31 OR REV 32** —
the last geometry change is still rev 30's. **THE HERO IS NOT OWED:
`rev30_hero34f.png` IS A RENDER OF THE REV-30 BUILD** and rev 31 proved it by
content. Do not re-shoot it to check.

**AND RUN THE PROBES YOU INHERIT, NOT ONLY THE ONES YOU WRITE.** rev 32 found
`probe_dust_scope.py` had been **failing one of its own eight controls since rev
30** — a hard-coded "audit.py publishes 185" that rev 30's `orb_bar` took to
186 — because neither rev 30 nor rev 31 ever ran it. **A CONTROL NOBODY RUNS IS
NOT A CONTROL.**

## Step 4 — read, in this order

`STATE.md` → `SPEC.md` §10, then §10.9 through §10.86 → this file →
**`HANDOFF_rev32.md`** → `HANDOFF_rev31.md` → … → `AUDIT_rev18_loft.md` →
`LOFT_GROUND_rev15.md` → `AUDIT_rev12.md` → `REF_MEASUREMENTS.md`.
`STATE.md` is machine-written; **if it and any prose disagree, it is right.**

**§10.86 IS REV 32's. IT MOVES NO GEOMETRY.** It does four things:

1. **SWEEPS §10.85's CORRECTED ANCHOR THROUGH ITS CONSUMERS**, which §10.85 said
   in its own words it had not done. Four live carriers of `311.5` found.
2. **RULES OUT THE POST'S CROSS-RATIO ROUTE** with a graded positive control.
3. **RE-RUNS §10.84's ARM 2** on the corrected anchor and finds the control that
   was reported as a clean FAILURE would now PASS — **and does not take it**,
   because the arm has two terms it never had.
4. **ASKS §10.82's two-revision-old question**, and corrects the work list's own
   description of it in passing.

## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them

This has now paid off twenty-one times. Show me a crop, mark the regions, give
me options, **print the crop box**, and **say plainly what each mark IS**.
rev 30's two boxes were SAMPLING WINDOWS and said so; rev 31's four were ALL
POINTERS and said so; **rev 32's Q2 used three POINTERS and its Q1 used a third
kind — CANDIDATE LINES, which are neither** — and the figure said so.
Show the photograph **BESIDE a render of the current build**.

**A CLASS GATE IS A PROBE TOO, and so is a BRIEF, a TARGET, a SUBAGENT'S
FINDING, A CITATION, A GUARD YOU JUST WROTE, AN ESTIMATOR YOU JUST BUILT,
A QUESTION YOU ARE ABOUT TO ASK ME, A THRESHOLD, A SAMPLING WINDOW, A NULL
PATCH, A REFUTATION SOMEONE ELSE ALREADY BANKED, THE AXIS YOUR DETECTOR SEARCHES
ALONG, and — NEW, rev 32 — A LINE IN THE WORK LIST, and A FALSIFICATION ARM YOU
JUST RAN.**

rev 32 killed its own first hub-cap pointer on rev 29's unchanged band, killed
its own headline route on its own graded control, and caught **three of its own
falsification arms doing nothing at all**.

**DO NOT ASK ME WHAT MEASUREMENT CAN ANSWER.** **AND MY ANSWER MAY NOT BE ONE OF
YOUR OPTIONS** — both of rev 31's answers were outside the offered set and both
were better than the set. Leave room for that and re-examine the frame against
what I actually said.

## Step 6 — the work

§6 below is the ordered list. **THE OLDEST UNDONE ITEM IS STILL THE OVER-RIDER
POST, and rev 32 narrowed what blocks it to ONE COLUMN** — the bar's far
termination, which is inside the three-member superposition you identified in
rev 31. **rev 32 asked me about exactly that column. If I have answered, that
answer is the whole of item 1.**

## Step 7 — resolution

rev 25 shipped 4800×3200 in 20 strips, worst seam z 1.91. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips ~5–7 min each,
edge strips ~1.5 min. **`hero.py` STRIPS IN ROW SPACE — SEAMS ARE HORIZONTAL.**
A 900×600 `T1_PREVIEW=hero34f T1_SAMP=24` frame takes **90 s** and is enough for
a question figure — rev 32 shot two.

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

Everything in the rev-32 prompt's equivalent section still stands, **with these
changes.**

**§10.83's "post at the vehicle's centreline" is STILL UNDECIDED**, for the
third revision running. rev 30 called it REFUTED, rev 31 downgraded it to
UNDECIDED, rev 32 found that §10.84's second arm would now PASS on the corrected
anchor **and refused to take it**. **It is NOT claimed that the post IS on the
centreline. The post stays UNBUILT. Do not treat either position as settled.**

**REF §9's V-SWAGE ABSOLUTE HEIGHT IS A BRACKET, NOT A READING.** `~0.49 m
above ground` consumed BOTH coordinates of the retired 311.5 point. The apex row
is bracketed `669 < v < 701.1`, so the height is **≈0.40–0.49 m** and the
published figure is the **TOP of that bracket**. Its "at the same image x, hence
the same depth" premise is gone with the column. **No replacement number is
published** — re-deriving needs the blade's top boundary at `u = 288.8`, and the
blade and the V-swage are BOTH CREAM, so a cream-run scan cannot find it.

**REF §9's OTHER THREE ABSOLUTE HEIGHTS DO NOT INHERIT §10.85.** V arms ← the
flank belt line; headlamp ← the V arm at its own x; indicator ← the headlamp.
They inherit the 422 px/m near-side scale and its >2:1 warning, which is a
separate and older caveat. **And `422 px/m` is CONSUMED NOWHERE in the tree** —
named once, in rev 29's carry-forward, only to warn against it. Sweep done.

**THE CROSS-RATIO ROUTE TO THE POST IS DEAD.** Four collinear points in the
bumper plane, no VP, no scale, no depth — the estimator is exact to **3.55e-15**
on planted values, and it still fails, because `(1+f)²/4f` bottoms out at 1 and
the map back to `f` is nearly vertical there. **The positive control passes 10 %
error at dU = 8 px; at 29 px there is NO REAL ROOT AT ALL.** Do not rebuild it.

**THE TRANSVERSE VP BY HARMONIC CONJUGATE IS NOT REFUTED, IT IS UNPUBLISHED.**
The construction is legitimate — **the transverse VP is shared by every lateral
line on the vehicle regardless of height, so it transfers into the bumper plane
without the vehicle's YAW**, which is what killed rev 31's ARM 1. It is withheld
because the far headlamp's dark region runs into the nose's own silhouette
(±5 px moves `f` by 9 %), four row-wise VP estimates off the V arms scatter over
**154 px**, and the bar-symmetry assumption's only check disagrees at 17 %.
**A square-on frame of the front still collapses this entirely.**

**THE FRONT OVER-RIDER BAR IS BUILT (§10.83)**, WORKSHOP-STAGE, on a ratio to
the headlamp aperture measured at the tube's own station. **`BAR_DIA` and
`BAR_RISE` are written as `ratio × APERTURE_M` and must stay that way.**
**The 10.83 verify row's reference is FROZEN IN `verify.py`**, window `x > 2.100`.

**THE POST IS BAR-TO-BLADE ONLY** *[stated, rev 31]*, so its depth IS the bumper
plane. **THE BAR'S FAR END IS PRESENT BUT CONFOUNDED** *[stated, rev 31]* — a
superposition of bumper + post + bar inside `u 203–232`.

**§10.75's POINTER IS VINDICATED.** `357–374` was a POINTER rev 30 took a number
from. rev 32 re-measured it: **`u 355–377`, centre 365.5, stable to 0.5 px over
five thresholds.** The number survives to within 2 px; the process defect
stands.

**THE VEHICLE HAS NO RECOVERABLE FORE-AFT VANISHING POINT.** Do not try to fit
one. **THE HERO IS SHOT AND PROVED BY CONTENT.** Do not re-shoot it to check.

## Hard-won rules — every one was learned by breaking it

Every rule in the rev-32 prompt still stands. **NEW in rev 32:**

* **A CONTROL THAT FAILS CAN HIDE THE DEFECTS DOWNSTREAM OF IT.** When you
  correct the input to a failed control, re-read the WHOLE ARM, not just its
  verdict. §10.84's ARM 2 had no depth-ordering term and no height term for a
  whole revision, invisible because C4 failed first.
* **AN ARM THAT DOES NOT APPLY IS INDISTINGUISHABLE FROM A GUARD THAT DOES NOT
  FIRE.** Three of rev 32's first falsification arms were no-ops — two `sed`
  patterns missed their lines and one injected into a §10 body, which
  `_retired_value_drift` states in its own ceiling it cannot see. **Print the
  changed line before you believe the arm.**
* **A FEATURE NAMED IN A WORK LIST IS A PROBE TOO.** Four documents said "the
  workshop frame shows all three" of §10.82's surfaces. It shows two.
* **A CONTROL NOBODY RUNS IS NOT A CONTROL.**
* **CORRECTING AN ANCHOR IS NOT SWEEPING IT.** §10.85 corrected in place and
  said so, and the consumers still had to be chased a revision later.
* **WHEN A ROUTE'S ALGEBRA IS EXACT, GRADE ITS CONDITIONING AND PUBLISH THE
  LEVEL AT WHICH THE POSITIVE CONTROL FAILS.** "dU = 8 px" is usable; "it is
  ill-conditioned" is not.
* **A PROBE THAT CANNOT REPRODUCE ITS OWN PUBLISHED RESULT IS NOT A RECORD.**
  That is why `probe_orb_post.py` still carries `V_APEX_U = 311.5`.

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
git pull --ff-only ../tacombi_rev32_incremental.bundle HEAD      # -> 164
```

**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
The hero is gitignored and lives only on my disk.

```bash
git status                                                   # clean
grep -c '### 10.86' SPEC.md                                  # 1   rev 32
grep -c '10.86' SPEC.md                                      # 4   rev 32
grep -c 'A CONTROL THAT FAILS CAN HIDE' SPEC.md              # 2   rev 32
grep -c 'A FEATURE NAMED IN A WORK LIST IS A PROBE TOO' SPEC.md   # 2   rev 32
grep -c 'CORRECTING AN ANCHOR IS NOT SWEEPING IT' SPEC.md    # 1   rev 32
grep -c 'SPEC 10.86' t1_detail.py                            # 2   rev 32
grep -c 'SPEC 10.86' REF_MEASUREMENTS.md                     # 1   rev 32
grep -c '0.40-0.49 m' REF_MEASUREMENTS.md                    # 1   rev 32
grep -c '10.86' verify.py                                    # 3   rev 32
grep -c '76.7' verify.py                                     # 2   rev 32
grep -c 'publishes 186' probe_dust_scope.py                  # 1   rev 32
grep -c 'V_APEX_U_R32' probe_orb_post.py                     # 3   rev 32
grep -c 'NO REAL ROOT' probe_orb_xratio.py                   # 3   rev 32
grep -c 'KILL' probe_orb_xratio.py                           # 3   rev 32
grep -c 'broke_at' probe_orb_xratio.py                       # 8   rev 32
grep -c 'B3_TRIED' probe_rev32_pointer.py                    # 3   rev 32
grep -c 'ANSWERED' probe_rev32_pointer.py                    # 12  rev 32
grep -c 'CANDIDATE LINES' mark_rev32_q.py                    # 3   rev 32
grep -c 'POINTERS, NOT SAMPLING WINDOWS' mark_rev32_q.py     # 2   rev 32
ls HANDOFF_rev32.md STATE_rev32.md probe_orb_xratio.py probe_rev32_pointer.py
ls mark_rev32_q.py rev32_q1_barend.png rev32_q2_surfaces.png
grep -c '### 10.85' SPEC.md                                  # 1   ANCESTOR rev 31b
grep -c 'UNDECIDED' SPEC.md                                  # 8   MOVED BY 10.86
grep -c 'commensurable' SPEC.md                              # 2   ANCESTOR rev 31
grep -c '288.8' SPEC.md                                      # 8   MOVED BY 10.86
grep -c '288.8' REF_MEASUREMENTS.md                          # 4   MOVED BY 10.86
grep -c 'UNDECIDED' verify.py                                # 3   MOVED BY 10.86
grep -c 'V_APEX_TOL' probe_orb_post.py                       # 12  MOVED BY 10.86
grep -c '### 10.84' SPEC.md                                  # 1   ANCESTOR rev 31
grep -c '### 10.83' SPEC.md                                  # 1   ANCESTOR rev 30
grep -c 'ORB_RISE_SPEC' verify.py                            # 6   ANCESTOR rev 30
grep -c 'BAR_RATIO' t1_detail.py                             # 3   ANCESTOR rev 30
grep -c 'overrider_bar' build.py                             # 1   ANCESTOR rev 30
grep -c 'W_h' probe_orb_hoop.py                              # 6   ANCESTOR rev 30
grep -c '### 10.82' SPEC.md                                  # 1   ANCESTOR rev 29
grep -c '### 10.80' SPEC.md                                  # 1   ANCESTOR rev 28
grep -c 'CORE' probe_psf_owner.py                            # 12  ANCESTOR rev 28
grep -c 'SPEC 10.76' t1_mats.py                              # 4   ANCESTOR rev 27
grep -c 'PUBLISHED_CLEAN' probe_ctan_pedestal.py             # 3   ANCESTOR rev 26
grep -c '_ceval' folk_gen.py                                 # 19  ANCESTOR rev 25
grep -c '_retired_value_drift' verify.py                     # 3   ANCESTOR rev 24
grep -c 'OFF_CROSS_BASELINE' t1_shell.py                     # 1   ANCESTOR rev 23
grep -c 'H_ROOF_REGRESSION' verify.py                        # 7   ANCESTOR rev 22
grep -c 'T1_CTAN_NOBOUNCE' shader_solve.py                   # 4   ANCESTOR rev 20
grep -c '_BODY' cream_rms.py                                 # 4   ANCESTOR rev 19
grep -c '_arch_lip_z' verify.py                              # 2   ANCESTOR rev 18
grep -c 'matte_tap' studio.py                                # 6   ANCESTOR rev 17
grep -c '_coons_cap' t1_core.py                              # 3   ANCESTOR rev 16
grep -c 'The threshold is not the parameter' post.py         # 1   ANCESTOR rev 13
```

**EVERY VALUE ABOVE WAS FILLED FROM A FRESH-CLONE VERIFICATION RUN.** Never type
one from memory — `grep -c` counts LINES, not occurrences, and that has produced
a wrong figure in eleven revisions. **NOTE THE SEVEN ROWS MARKED "MOVED BY
10.86".** rev 31 published `UNDECIDED` in SPEC as 5, `288.8` in SPEC as 2,
`288.8` in REF as 1, `UNDECIDED` in verify as 2 and `V_APEX_TOL` as 5. **Every
one of those was correct when written and is now wrong**, because rev 32 edited
the files they count. *A grep count is invalidated by any later edit to the file
it counts — including a later revision's.*

Ancestry — **rev 32 adds `6f87977`, the rev-31 TIP:**

```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201 b08e424 e792d73 6f87977; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```

Texture md5s — **all three must match, and rev 32 changed NO artwork:**

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
band 1.372–1.775. **EVERY GEOMETRY FIGURE IS IDENTICAL TO REV 30's AND REV 31's.**

Probe controls, on the fresh clone: `probe_rev32_pointer.py` **10 checked, 0
FAILED**; `probe_dust_scope.py` **8 checked, 0 FAILED** (was 1 FAILED before rev
32 fixed the literal); `probe_orb_xratio.py` **6 checked, 1 FAILED — AND THAT
FAILURE IS THE RESULT.** C5 is a KILL control: it asks whether the route
survives the far end's blob, and it does not. **A green run there would have
meant the post could be built.** Do not "fix" it.

## 3. What rev 32 changed — `HANDOFF_rev32.md` has the full account

- **`SPEC.md`** — NEW §10.86; **§10.75's in-place annotation corrected** (it had
  read REFUTED for a whole revision after §10.84 downgraded it, and on the wrong
  anchor); **§10.83's apex reference and post columns annotated in place.**
- **`REF_MEASUREMENTS.md`** — §9's V-swage absolute height **withdrawn as a
  reading and replaced by a bracket**, with the negative sweep result recorded.
- **`t1_detail.py`** — the `overrider_bar()` comment corrected, **original kept**
  as the record of what rev 30 believed.
- **`verify.py`** — the `_RETIRED_VALUES` row is **KEPT for the third time**,
  reason corrected again, offset 54.0 → **76.7 px**. **Watched FIRE.**
- **`probe_orb_post.py`** — corrected anchor added BESIDE the original, which is
  deliberately left at 311.5.
- **`probe_dust_scope.py`** — mesh-count literal **185 → 186**.
- **`probe_orb_xratio.py`**, **`probe_rev32_pointer.py`**, **`mark_rev32_q.py`**,
  **`rev32_q1_barend.png`**, **`rev32_q2_surfaces.png`** — all NEW, all READ-ONLY.
- **NO GEOMETRY. NO SHADER. NO ARTWORK.** `CREAM`, `COUNTERTAN`,
  `COUNTERCREAM`, `RED`, the rake, the roof, the over-rider bar and all three
  textures UNCHANGED.

**Things you must not silently undo — `HANDOFF_rev32.md` §8**, and rev 31's §6
through rev 18's §4 all still stand in full.

## 4. Still open

- **THE OVER-RIDER POST.** Blocked on ONE COLUMN: the bar's far termination,
  inside the ~29 px three-member superposition. **rev 32 asked about exactly
  that column** (`rev32_q1_barend.png`, five candidate lines at
  `u = 205/212/219/228/240`). **If the owner has answered, that answer IS item
  1** — feed it into `probe_orb_xratio.py`'s C5 and see whether the swing
  collapses. **If he says none of them, that binds and the route is closed for
  good.**
- **§10.82's THREE SURFACES** — asked in `rev32_q2_surfaces.png`. **ALL CLEAN**
  → the global zeroing gains three surfaces of support and §10.82's named gap
  closes. **ANY DUSTY** → a global `f = 0` is contradicted there and the film
  must become LOCAL (per-material `dust` input), not one lever.
- **§10.83's centreline claim is UNDECIDED**, third revision running.
- **REF §9's V-SWAGE ABSOLUTE HEIGHT is a bracket, ≈0.40–0.49 m**, and closing
  it needs the blade's top boundary at `u = 288.8` against a cream-on-cream
  edge.
- **§10.70's percentages must be RE-RUN** before being quoted again. The harness
  has **no cyclorama** (§10.78) — state that, do not silently fix it.
- **THE FRONT BUMPER FACE IS UNMEASURED.** **`CREAM`.** **THE ABSOLUTE ROOF
  HEIGHT.** **THE OFF FLANK, 804.9 mm.** `COUNTERTAN` 34.0 % short in B.
- `GAL_SKY` dead lever. `PLATE_W = 0.3300` no provenance.
  `probe_rev16.py:90` prints `xa` vs `xa`.

## 5. FIRST QUESTIONS FOR THE OWNER — TWO ARE OUTSTANDING

**Q1 `rev32_q1_barend.png`** — where does the over-rider bar end on the far side?
**Q2 `rev32_q2_surfaces.png`** — do the bumper top, the rim face and the hub cap
carry dust?

**Read the answers before planning anything.** And remember rev 31's rule: **his
answer may not be one of the options, and both times that happened the answer
was better than the set.**

What would still move the most is one photograph: **a head-on rear (or front)
elevation from roof height or above, with the counter and the lids clear of the
section** — the only realistic route to closing `CREAM`, the absolute roof height
and the B residual. A clear view of the **off flank** closes 804.9 mm. **And for
the POST: any frame showing the FRONT of the vehicle square-on collapses the
lateral-scale problem entirely.**

## 6. Ordered work list for rev 33

1. **THE POST, on the owner's Q1 answer.** Feed the chosen column into
   `probe_orb_xratio.py`'s C5. **Say before you start whether it will close** —
   at dU ≤ 4 px of residual uncertainty it will (6 % on `f`); at dU ≥ 8 px it
   will not (14 %), and those levels are already published. If it closes,
   express the post as a **FRACTION of the bar's half-width** so it inherits
   `BAR_HALF_Y`'s grade E rather than adding a new lateral choice.
2. **§10.82, on the owner's Q2 answer.** Either close the named gap or make the
   film LOCAL. **Do not tune the lever; the retirement was a DERIVATION being
   retired, not a constant being set** (SPEC 10.82).
3. **Re-run §10.70's arms** on the post-retirement build before quoting any of
   its percentages, then the scene→top bounce.
4. Tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
5. Camera absolutely last.

## 7. THE COMMIT COUNT AND THE CONTENT FIGURES

This section is written LAST, after the final commit, and every figure in §1 was
read off a fresh-clone verification run rather than typed from memory. **This has
gone wrong in ELEVEN revisions during handoff assembly.**

**FINAL COUNT: 164 commits, clean tree.** *(Verified: this line lands in commit
164 itself, which is what makes it true — the count lands in its own commit,
rev 29's pattern, kept since.)*

**THE GREP TRAP FIRED AGAIN AND IT FIRED ACROSS REVISIONS THIS TIME.** rev 31b
found its OWN later section moving its OWN earlier published counts. rev 32
found something one step worse: **seven counts rev 31 published correctly are now
wrong**, because rev 32 edited the files they count. Nothing was wrong when
written. **A grep count is invalidated by any later edit to the file it counts —
including a later revision's — so every one of them has to be re-read, not
inherited.** All seven are marked "MOVED BY 10.86" in §1.

**AND THE COUNT MOVED ONCE WHILE THIS FILE WAS BEING WRITTEN, FOR A GOOD
REASON.** The first draft of Step 0 said rev 32's bundle was over the bridge's
throughput ceiling. It was — but only because I had cut it from the rev-30 tip
by mistake, so it carried rev 31's commits as well. Cut correctly from `6f87977`
it is **2.38 MB and crosses whole**. Corrected, which cost one commit, which is
why the count is 164 and not 163. **A BUNDLE'S SIZE IS A MEASUREMENT TOO, AND IT
DEPENDS ON THE BASE YOU CUT IT FROM.**

**A NEW TRAP, AND IT IS THE MOST DANGEROUS ONE THIS PROJECT HAS FOUND.**
**THREE OF REV 32's FALSIFICATION ARMS DID NOTHING AT ALL** — two `sed` patterns
missed their target lines and one injected a retired phrase into a `§10` body,
which `_retired_value_drift` says in its own stated ceiling it cannot see. **All
three printed "VERIFY: 0 fail, 0 warn", which is exactly what a guard that
failed to fire prints.** Caught by printing the changed line and re-running. **An
arm that does not apply is indistinguishable from a guard that does not fire, and
it is the one kind of self-check that fails SILENTLY IN THE SAFE DIRECTION.**
