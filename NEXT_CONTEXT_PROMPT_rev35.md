# NEXT CONTEXT PROMPT — rev 35

Please act as my expert. Continue the Señor Tacombi combi build. **Thirty-four
revisions sit behind this.** You are picking up mid-stream, not starting.

## Step 0 — CHECK A FOLDER IS CONNECTED BEFORE YOU PLAN ANYTHING

Call `get_device_info`. **In rev 32, rev 33 AND rev 34 `~/Desktop/tacombi_bus_render`
was ALREADY in `connectedFolders` on the first call** — three in a row. It timed
out unanswered in rev 28 and rev 29 and was granted on the first request in
rev 30 and rev 31. **Do not assume any of those outcomes** — call it, and say
plainly what came back.

**THE BRIDGE HAS A THROUGHPUT CEILING, NOT JUST A SIZE ONE — CONFIRMED FIVE
TIMES.** `device_stage_files` times out above ~3 MB. **Only TWO files need
splitting:** the 19.5 MB base bundle (7 parts) and the 8.5 MB `rev14_unified`
(3 parts). **Everything rev15–rev34 is under 3 MB and crosses whole.**

**REV 34 REUSED REV 33's `_xfer33/` SPLIT PARTS RATHER THAN RE-SPLITTING** —
they are still on his disk, md5-verified on both sides. Check they are there
before spending `device_bash` calls re-splitting.

**IN REV 33 AND REV 34 ALL FILES CROSSED WITH ZERO TRANSIENT FAILURES.** Do
not read that as the new normal: rev 32 had two `upload failed` in one batch
that both crossed on a single retry, and a `device_bash` 502 that worked on
retry. **TRANSIENT FAILURES ARE NOT DROPS**, and the bridge also genuinely
drops (three times in rev 31, each recovering on its own). Do not retry in a
loop; do cloud-side work and come back.

**`device_bash` DOES NOT SEE `/Users/...`.** The connected folder is mounted at
`/sessions/<session-id>/mnt/tacombi_bus_render`. `pwd` then `ls mnt/` finds it.
**`device_stage_files` DOES take the `/Users/...` path** — the two tools take
different roots and that is not a typo. **AND YOUR SHELL'S `~` IS `/root`, NOT
`/home/claude`** — after a long `Bash` call the cwd may reset; use absolute
paths. **`hero.py`'s `BLENDER` constant must be pointed at `/tmp/blender/blender`
before any render** (rev 34 committed that change).

**`ref_workshop.jpg`, `ref_side.jpg` and `ref_rear34.jpg` are IN THE REPO**, so
all reference measurement survives an outage.

## Step 1 — read my memory BEFORE you read any code

`/areas/tacombi-combi-3d.md`, then `-rev14`, `-rev17` … `-rev33`, then
**`/areas/tacombi-combi-3d-rev34.md`** (SEPARATE FILES; each revision's file
does NOT carry the next), then `/areas/tacombi-combi-sticker.md`, then
`/preferences.md`. If you cannot read them, say so explicitly.

**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner. **Do not ask me what the real vehicle looks
like.** Ask me what a PHOTOGRAPH shows — that has now paid off twenty-six times.

## Step 2 — restore, and verify BY CONTENT (never by hash or commit count)

See §1. **TWENTY-TWO bundle lines now, and the rev14b line is a `fetch` that
must come BEFORE rev15.** rev 20 through rev 34 all restored CLEAN — do not
assume either way, check.

## Step 3 — install Blender 4.5.3 and run BOTH guards before proposing anything

```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
/tmp/blender/4.5/python/bin/python3.11 -m pip install pillow scipy
```

That pip line is required. Guards are `T1_SUB=n T1_VERIFY=1 blender -b
--python build.py` and `T1_SUB=n blender -b --python audit.py`. Report the
guards' ACTUAL output, both levels. **`audit.py` rewrites `STATE.md` every run
— `git checkout STATE.md` after.**

**THE GUARDS ARE 0 fail / 0 WARN.** **NO GEOMETRY MOVED IN REV 31, 32, 33 OR
34** — the last geometry change is still rev 30's. **THE HERO IS NOT OWED:
`rev30_hero34f.png` IS A RENDER OF THE REV-30 BUILD.** Do not re-shoot it.

**AND RUN THE PROBES YOU INHERIT, NOT ONLY THE ONES YOU WRITE.** rev 32 found
`probe_dust_scope.py` failing one of its own controls since rev 30. rev 33
found two more, one DEGENERATE. **rev 34 ran all twenty and found the brief's
own sentence about them wrong** (§10.88.5).

**SIX PROBES NEED BLENDER — BUT NOT THE SIX A GREP NAMES.** Run under
`blender -b --python`: `probe_ctan_index`, `probe_dust_scope`, `probe_f90`,
`probe_rev16` (direct `import bpy`), **plus `probe_cross_anatomy` and
`probe_shutlines`, which import it TRANSITIVELY with the token appearing
nowhere in the file.** Run under `/tmp/blender/4.5/python/bin/python3.11`:
everything else — **including `probe_clean_top` and `probe_dust_anchor`, whose
only `bpy` is inside a comment explaining why they parse `t1_mats` with `ast`.**
**A grep gives two false positives and two false negatives and they CANCEL.**

## Step 4 — read, in this order

`STATE.md` → `SPEC.md` §10, then §10.9 through §10.88 → this file →
**`HANDOFF_rev34.md`** → `HANDOFF_rev33.md` → … → `AUDIT_rev18_loft.md` →
`LOFT_GROUND_rev15.md` → `AUDIT_rev12.md` → `REF_MEASUREMENTS.md`.

`STATE.md` is machine-written; **if it and any prose disagree, it is right —
BUT CHECK ITS PROVENANCE ROWS FIRST.** In rev 33 the committed `STATE.md` was
one revision stale. **rev 34's is current** — regenerated on the clean rev-34
tree at commit `f1d82cb`, `working tree | clean`, with `STATE_rev34.md`
alongside. **It has a `working tree` row; if that says DIRTY, the file is not
a record of anything.**

**§10.88 IS REV 34's. IT MOVES NO GEOMETRY.** It does five things:

1. **GRADES THE INSTRUMENT BEFORE SPENDING A QUESTION** — and finds §10.87's
   A7 comparing a LIVE sensitivity against a SYNTHETIC one.
2. **MAKES A PRE-COMMITMENT THAT FAILS BEFORE THE QUESTION GOES OUT**, and
   prints it on the question figure.
3. **NAMES A GENERAL RULE**: a tolerance in the units of the MEASUREMENT does
   not transfer between columns.
4. **CONSUMES TWO OWNER ANSWERS AND RETIRES THE CROSS-RATIO ROUTE** — on a
   PRECONDITION failure, not a precision shortfall.
5. **RECORDS FIVE DEFECTS OF MY OWN**, three of them the same family.

## Step 5 — ASK ME WHAT THE PHOTOGRAPHS SHOW before you measure from them

This has now paid off twenty-six times. Show me a crop, mark the regions,
give me options, **print the crop box**, and **say plainly what each mark IS.**
rev 30's two marks were SAMPLING WINDOWS; rev 31's four were POINTERS; rev 32,
33 and 34 used CANDIDATE LINES — and rev 34 added a fourth class, **an ORDERING
WALL**, drawn as a wall and labelled *not a candidate, and not my choice*.

Show the photograph **BESIDE a render of the current build.** A 900×600
`T1_SAMP=24` `hero34f` preview takes **71 s** and is enough for this.

**A CLASS GATE IS A PROBE TOO, and so is a BRIEF, a TARGET, a SUBAGENT'S
FINDING, A CITATION, A GUARD YOU JUST WROTE, AN ESTIMATOR YOU JUST BUILT,
A QUESTION YOU ARE ABOUT TO ASK ME, A THRESHOLD, A SAMPLING WINDOW, A NULL
PATCH, A REFUTATION SOMEONE ELSE ALREADY BANKED, THE AXIS YOUR DETECTOR
SEARCHES ALONG, A LINE IN THE WORK LIST, A FALSIFICATION ARM YOU JUST RAN,
THE ARITHMETIC PRINTED UNDER A FIGURE, A PRE-COMMITMENT YOU JUST MADE, and —
NEW, rev 34 — **THE UNITS YOUR TOLERANCE IS STATED IN**, and **THE DETECTOR
THAT TELLS YOU WHICH FILES A RULE APPLIES TO.**

**DO NOT ASK ME WHAT MEASUREMENT CAN ANSWER.** **AND MY ANSWER MAY NOT BE ONE
OF YOUR OPTIONS.** **IF I PICK THE FIRST OR LAST OPTION, YOUR SET PROBABLY DID
NOT REACH FAR ENOUGH — ask a bounded follow-up before you consume the answer.**
rev 33 did and I closed it; **rev 34 did it twice and the second bound is what
retired the route.**

**BUT CHECK WHETHER THE ENDPOINT IS AGAINST A WALL FIRST.** rev 34's Q1
leftmost option sat **7 px from the estimator's own ordering precondition**, so
the interval was already closed on that side by arithmetic, not by my choice of
set. **An endpoint answer against a hard bound is NOT an open interval, and
saying which one you are looking at is part of the question.**

## Step 6 — the work

§6 below is the ordered list. **THE OVER-RIDER POST IS STILL ITEM 1, BUT ITS
ROUTE HAS CHANGED.** rev 34 RETIRED the cross-ratio. **Do not re-open it and do
not rebuild its algebra** — P1 is exact to 3.55e-15 and the algebra was never
the problem. The only unspent construction on this panel is the **transverse VP
by harmonic conjugate**, UNPUBLISHED and NOT REFUTED.

## Step 7 — resolution

rev 25 shipped 4800×3200 in 20 strips, worst seam z 1.91. Drive
`hero.py --only N` one strip per call then `--stitch-only`; run `post.py`
**once** on the stitched frame, never per strip. Middle strips ~5–7 min each,
edge strips ~1.5 min. **`hero.py` STRIPS IN ROW SPACE — SEAMS ARE HORIZONTAL.**
A 900×600 `T1_PREVIEW=hero34f T1_SAMP=24` frame takes **71 s**.

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

Everything in the rev-34 prompt's equivalent section still stands, **with these
changes.**

**THE CROSS-RATIO ROUTE IS RETIRED.** Not "does not close" — **its PRECONDITION
fails.** The four points must satisfy `far_end < strut < post < hoop`. The far
end is at u 205 ± 3.5; *[stated, rev 34]* the far strut is at **u ∈ (205, 208]**,
centre ~206.5. **The gap is 1.5 px and the far end's own residual is 2.3× it.**
**29 % of the far end's error bar puts it AT OR RIGHT OF the strut.** The
four-point construction has degenerated to three. **No further measurement on
those two columns repairs it.**

**THE FAR STRUT IS MEASURED.** *[stated, rev 34]* Q1: left of 228. *[stated,
rev 34]* Q1b: **at B1 or left of it, u 205–208.** The interval is CLOSED ON BOTH
SIDES. **The hard-coded u 228 was 20–23 px away — OUTSIDE the answered interval
entirely.** `probe_orb_xratio.py`'s `strut_u = 228.0` is **DELIBERATELY LEFT**;
a probe that cannot reproduce its own published result is not a record.

**P1b's CURVE UNDER-PRICES THE LIVE CONFIGURATION BY 1.39× AT 4 px.** The
published **6.2 % closing level is 8.6 % live**; the **14.3 % failing level is
18.3 % live**. **Every per-cent figure ever read off that curve and spent on the
live columns is that much too small.** The curve itself is fine — it exists to
grade the ALGEBRA where truth is known exactly.

**§10.87's A6/A7 CONCLUSION SURVIVES** (K3 passes) — the strut IS the more
sensitive column like for like. **Its published MARGIN does not: 1.79× reported,
1.28× like for like.**

**§10.87's "ON THE FAR END, THE OWNER CLOSED IT" IS RIGHT ON ITS OWN GATE
(px) AND WRONG IN THE ARITHMETIC PRINTED UNDER IT.** A3 gates in pixels; the
sentence converts to per cent unnecessarily and lands on the synthetic 5.4 %.
Live it is 7.5 %.

**§10.82's NAMED GAP IS CLOSED** — bumper top, rim face, hub cap all clean, the
global `f = 0` holds, **the film does not become local**. Unchanged by rev 34.

**§10.83's "post at the vehicle's centreline" is STILL UNDECIDED**, fifth
revision running. **The post stays UNBUILT.**

**REF §9's V-SWAGE ABSOLUTE HEIGHT IS A BRACKET, NOT A READING** — ≈0.40–0.49 m.
**REF §9's OTHER THREE ABSOLUTE HEIGHTS DO NOT INHERIT §10.85.** **`422 px/m`
IS CONSUMED NOWHERE.**

**THE TRANSVERSE VP BY HARMONIC CONJUGATE IS NOT REFUTED, IT IS UNPUBLISHED** —
and with the cross-ratio retired it is now the **only unspent construction on
this panel.** Withheld because the far headlamp runs into the nose's silhouette
(±5 px moves `f` by 9 %), four row-wise estimates scatter over **154 px**, and
the symmetry check disagrees at 17 %.

**A square-on frame of the front still collapses this entirely.**

**THE FRONT OVER-RIDER BAR IS BUILT (§10.83)**, WORKSHOP-STAGE. **`BAR_DIA` and
`BAR_RISE` are written as `ratio × APERTURE_M` and must stay that way** — and
note **`BAR_RISE` IS NOT A LITERAL**, so an arm that greps for `BAR_RISE = <num>`
matches nothing and prints 0 fail. Arm `BAR_RISE_RATIO` instead.

**THE VEHICLE HAS NO RECOVERABLE FORE-AFT VANISHING POINT.** Do not fit one.
**THE HERO IS SHOT AND PROVED BY CONTENT.**

## Hard-won rules — every one was learned by breaking it

Every rule in the rev-34 prompt still stands. **NEW in rev 34:**

* **A TOLERANCE STATED IN THE UNITS OF THE MEASUREMENT, NOT OF THE QUANTITY,
  DOES NOT TRANSFER BETWEEN COLUMNS.** 4 px buys 8.6 % on one column and
  11.1 % on another — a constant 1.28×, so it is structural. Every use of a px
  band on a new column silently assumes a shared px→quantity map.
* **A DETECTOR WHOSE ERRORS CANCEL IN THE AGGREGATE IT IS QUOTED BY IS
  INDISTINGUISHABLE FROM A CORRECT ONE, until someone needs the members and not
  the count.** The `bpy` grep: two false positives, two false negatives, 4−2+2=6.
* **A SILENTLY DROPPED SAMPLE IS NOT A SMALLER ERROR, IT IS A MISSING ONE.**
  A helper that filters `None` out of a set and computes over the survivors
  reports a *smaller* number for a regime that has actually broken.
* **A RULING THAT NARRATES ITS OWN CONTROLS MUST REFUSE TO PRINT WHEN A
  POSITIVE CONTROL IS DOWN.** Both rev-34 probes now do. Verified by arm.
* **REFITTING A MAP CANNOT MOVE A CONTROL THAT READS A HARD-CODED DICT.** An
  arm aimed at the wrong layer is a non-arm, and it looks exactly like a guard
  that did not fire.
* **AN ENDPOINT ANSWER AGAINST A HARD BOUND IS NOT AN OPEN INTERVAL.** Check
  whether the estimator's own preconditions already close the side before
  spending a follow-up widening it.
* **A CONSTRUCTION CAN FAIL ON ITS PRECONDITION RATHER THAN ITS PRECISION**, and
  that failure is not repairable by measuring harder. Ask what the construction
  REQUIRES of its inputs, not only how accurate they are.

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
git pull --ff-only ../tacombi_rev32_incremental.bundle HEAD      # -> 166
git pull --ff-only ../tacombi_rev33_incremental.bundle HEAD      # -> 173
git pull --ff-only ../tacombi_rev34_incremental.bundle HEAD      # -> 181
```

**If a pull says "Need to specify how to reconcile divergent branches", STOP.**
The hero is gitignored and lives only on my disk.

```bash
git status                                                   # clean
grep -c '^### 10.88' SPEC.md                                 # 1   rev 34
grep -c '^#### 10.88' SPEC.md                                # 6   rev 34
grep -c '10.88' SPEC.md                                      # 7   rev 34
grep -c 'A TOLERANCE STATED IN THE UNITS OF THE MEASUREMENT' SPEC.md   # 1   rev 34
grep -c 'A DETECTOR WHOSE ERRORS CANCEL' SPEC.md             # 1   rev 34
grep -c 'DEGENERATED TO THREE' SPEC.md                       # 1   rev 34
grep -c 'ORDER BROKEN' probe_rev34_ruling.py                 # 2   rev 34
grep -c 'REFUSING TO PRINT A RULING' probe_rev34_ruling.py   # 1   rev 34
grep -c 'REFUSING TO PRINT A RULING' probe_rev34_levels.py   # 1   rev 34
grep -c 'ORDERING WALL' mark_rev34_strutb.py                 # 4   rev 34
grep -c 'REFUSING TO WRITE' mark_rev34_strut.py              # 1   rev 34
grep -c 'CANDIDATE LINES' mark_rev34_strut.py                # 8   rev 34
grep -c 'SYN_' probe_rev34_levels.py                         # 8   rev 34
ls HANDOFF_rev34.md STATE_rev34.md probe_rev34_levels.py probe_rev34_ruling.py
ls mark_rev34_strut.py mark_rev34_strutb.py rev34_q_strut.png rev34_q_strutb.png
grep -c 'UNDECIDED' SPEC.md                                  # 10  MOVED BY 10.88
grep -c '^### 10.87' SPEC.md                                 # 1   ANCESTOR rev 33
grep -c 'STRUT_U' probe_rev33_barend.py                      # 11  ANCESTOR rev 33
grep -c 'KILL' probe_rev33_barend.py                         # 11  ANCESTOR rev 33
grep -c 'CANDIDATE LINES' mark_rev33_q1b.py                  # 4   ANCESTOR rev 33
grep -c '### 10.86' SPEC.md                                  # 1   ANCESTOR rev 32
grep -c '288.8' SPEC.md                                      # 8   ANCESTOR rev 32
grep -c '288.8' REF_MEASUREMENTS.md                          # 4   ANCESTOR rev 32
grep -c 'UNDECIDED' verify.py                                # 3   ANCESTOR rev 32
grep -c 'V_APEX_TOL' probe_orb_post.py                       # 12  ANCESTOR rev 32
grep -c '76.7' verify.py                                     # 2   ANCESTOR rev 32
grep -c 'publishes 186' probe_dust_scope.py                  # 1   ANCESTOR rev 32
grep -c 'NO REAL ROOT' probe_orb_xratio.py                   # 3   ANCESTOR rev 32
grep -c 'ANSWERED' probe_rev32_pointer.py                    # 12  ANCESTOR rev 32
grep -c 'ORB_RISE_SPEC' verify.py                            # 6   ANCESTOR rev 30
grep -c 'BAR_RATIO' t1_detail.py                             # 3   ANCESTOR rev 30
grep -c 'overrider_bar' build.py                             # 1   ANCESTOR rev 30
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

**EVERY VALUE ABOVE WAS FILLED FROM A FRESH-CLONE VERIFICATION RUN.** Never
type one from memory — `grep -c` counts LINES, not occurrences, and that has
produced a wrong figure in eleven revisions.

**ANCHOR YOUR HEADING COUNTS WITH `^`.** `grep -c '### 10.88'` is **7**, not 1,
because `#### 10.88.1` contains the pattern. rev 33 hit this within a minute of
writing the section.

**NOTE THE ROW MARKED "MOVED BY 10.88".** rev 34's prompt published `UNDECIDED`
in SPEC as 9; §10.88 added one and it is now **10**. *A grep count is
invalidated by any later edit to the file it counts — including a later
revision's.*

Ancestry — **rev 34 adds `2253399`, the rev-33 TIP:**

```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268 456b201 b08e424 e792d73 6f87977 cac32b9 2253399; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```

Texture md5s — **all three must match, and rev 34 changed NO artwork:**

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
band 1.372–1.775. **EVERY GEOMETRY FIGURE IS IDENTICAL TO REV 30's, 31's, 32's
AND 33's.**

Probe controls on the fresh clone: `probe_rev34_levels.py` **8 checked, 4
FAILED — K1, K2, K4, K5, and all four ARE the result** (K3 PASSES and that is
a real result too); `probe_rev34_ruling.py` **6 checked, 4 FAILED — R3, R4, R5,
R6, and R3/R4 ARE the ruling**; `probe_rev33_barend.py` **7 checked, 4 FAILED**;
`probe_orb_xratio.py` **6 checked, 1 FAILED** (C5, a KILL); `probe_rev32_pointer.py`
**10 checked, 0 FAILED**; `probe_dust_scope.py` **8 checked, 0 FAILED**;
`probe_updust_pointer.py` **6 checked, 0 FAILED**; `probe_psf_lines.py`
**2 FAILED, both EXPECTED** (the rev-28 finding, its own text says so);
`probe_clean_top.py` and `probe_dust_anchor.py` **DELIBERATELY LEFT FAILING**
(§10.87.2). **Do not "fix" any of these.**

## 3. What rev 34 changed — `HANDOFF_rev34.md` has the full account

- **`SPEC.md`** — NEW §10.88, six parts.
- **`STATE.md`** — regenerated on the clean rev-34 tree at `f1d82cb`,
  `working tree | clean`. **`STATE_rev34.md`** written alongside.
- **`probe_rev34_levels.py`**, **`probe_rev34_ruling.py`**,
  **`mark_rev34_strut.py`**, **`mark_rev34_strutb.py`**,
  **`rev34_q_strut.png`**, **`rev34_q_strutb.png`**, **`HANDOFF_rev34.md`** —
  all NEW, all READ-ONLY.
- **`hero.py`** — one line: `BLENDER` pointed at `/tmp/blender/blender`.
  **This is the only non-doc, non-probe change in the revision.**
- **NO GEOMETRY. NO SHADER. NO ARTWORK.** `CREAM`, `COUNTERTAN`,
  `COUNTERCREAM`, `RED`, the rake, the roof, the over-rider bar and all three
  textures UNCHANGED. **`verify.py`, `t1_detail.py`, `t1_mats.py`, `build.py`,
  `t1_shell.py`, `t1_core.py` and every other build file are BYTE-UNCHANGED
  from rev 33.**

**Things you must not silently undo — `HANDOFF_rev34.md` §7**, and rev 33's §6
through rev 18's §4 all still stand in full.

## 4. Still open

- **THE OVER-RIDER POST.** The cross-ratio route is **RETIRED** (§10.88.4). The
  only unspent construction is the **transverse VP by harmonic conjugate**,
  UNPUBLISHED and NOT REFUTED. **A square-on frame of the FRONT collapses it
  entirely and is worth more than any further measurement on this panel.**
- **`probe_clean_top.py` and `probe_dust_anchor.py` need REWRITING, not
  fixing.** What they compare no longer exists. Decide first what the
  post-retirement question is. **Do not widen a tolerance.**
- **§10.70's percentages must be RE-RUN** before being quoted again. The
  harness has **no cyclorama** (§10.78) — state that, do not silently fix it.
- **§10.83's centreline claim is UNDECIDED**, fifth revision running.
- **REF §9's V-SWAGE ABSOLUTE HEIGHT is a bracket, ≈0.40–0.49 m.**
- **THE FRONT BUMPER FACE IS UNMEASURED. `CREAM`. THE ABSOLUTE ROOF HEIGHT.
  THE OFF FLANK, 804.9 mm.** `COUNTERTAN` 34.0 % short in B.
- `GAL_SKY` dead lever. `PLATE_W = 0.3300` no provenance.
  `probe_rev16.py:90` prints `xa` vs `xa`.

## 5. FIRST QUESTION FOR THE OWNER

**NO QUESTION IS OUTSTANDING WITH ME.** I answered both of rev 34's, and the
second one retired the route rather than opening another.

**Before you ask me anything, say what it can close** — rev 34's pre-commitment
failed *before* the question went out, and saying so was the right move rather
than a reason to skip asking.

What would still move the most is one photograph: **a head-on rear (or front)
elevation from roof height or above, with the counter and the lids clear of the
section** — the only realistic route to closing `CREAM`, the absolute roof
height and the B residual. A clear view of the **off flank** closes 804.9 mm.
**And for the POST: any frame showing the FRONT of the vehicle square-on is now
the ONLY thing that closes it.**

## 6. Ordered work list for rev 35

1. **THE POST, if at all — and only by the harmonic-conjugate route.** Say
   before you start whether it can close, and grade **every** column it
   consumes before spending a question, not the one you are arguing about.
   **Do not re-open the cross-ratio.**
2. **REWRITE `probe_clean_top.py` and `probe_dust_anchor.py`**, or retire them
   with a stated reason.
3. **Re-run §10.70's arms** on the post-retirement build before quoting any of
   its percentages, then the scene→top bounce.
4. Tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
5. Camera absolutely last.

## 7. THE COMMIT COUNT AND THE CONTENT FIGURES

This section is written LAST, after the final commit, and every figure in §1
was read off a fresh-clone verification run rather than typed from memory.
**This has gone wrong in ELEVEN revisions during handoff assembly.**

**FINAL COUNT: 182 commits, clean tree.** *(Verified: this line lands in commit
182 itself, which is what makes it true — the count lands in its own commit,
rev 29's pattern, kept since.)*

**THE GREP TRAP FIRED AGAIN, FOUR TIMES, AND THE FRESH-CLONE RUN CAUGHT ALL
FOUR.** I typed four rev-34 counts from estimate rather than reading them off a
run: `DEGENERATED TO THREE` in SPEC (wrote 2, is **1**), `ORDER BROKEN` in
`probe_rev34_ruling.py` (wrote 3, is **2**), `CANDIDATE LINES` in
`mark_rev34_strut.py` (wrote 4, is **8**), and `SYN_` in
`probe_rev34_levels.py` (wrote 19, is **8** — I counted OCCURRENCES; `grep -c`
counts LINES). **Twelfth revision this has happened in, and the fresh-clone
verification is the only thing that has ever caught it.** All four corrected
above from the console.

**THE GREP TRAP.** rev 33 found a SUBSTRING collision inside a single grep
(`### 10.87` matching `#### 10.87.1`). **rev 34's own `UNDECIDED` count moved
9 → 10** because §10.88.6 mentions the word. Anchor headings with `^`, and
re-read every count on the fresh clone.

**AND TWO OF MY FIVE GUARD ARMS DID NOTHING ON THE FIRST TRY.** One targeted
`BAR_RISE`, which is **not a literal** (`BAR_RISE_RATIO × APERTURE_M`), so the
regex matched nothing and the guard printed **0 fail** — *what a guard that
failed to fire prints*. One injected `W_DUST_FAC_UP`, which is **not in
`_RETIRED_VALUES`** — rev 33's exact mistake, repeated. **Both caught by
printing the changed line before believing the arm.** Re-armed on
`BAR_RISE_RATIO` (2 fails) and on the watched literal `0.0330` (1 fail).
