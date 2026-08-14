# HANDOFF rev 18

**81 commits, clean tree, guards 0 fail / 1 warn at BOTH subdivision levels.**
Read off the console after the last commit, then the bundle was re-cut and
verified again from a fresh clone.

---

## 0. THE FIRST THING THAT HAPPENED, AND IT NEARLY COST THE REVISION

**rev 17's deliverables were not on disk when this context started.** The rev-17
memory said "confirm it reached his disk"; it had not. The only rev-17-named file
in the folder was `NEXT_CONTEXT_PROMPT_rev17.md`, which rev *16* wrote.

The restore to rev 16 was clean and content-verified. What caught the loss was
the **content greps** — `### 10.44` = 0, `A CLASS GATE IS A PROBE TOO` = 0,
`CAP_RING_BANDFRAC` = 0, `matte_tap` = 0.

**What did NOT catch it: the ancestry loop, which passed 5 of 5.** `7ce3d03` is
the **rev-16 tip**, not a rev-17 commit — its subject is literally *"rev 16:
commit the SUB=1 STATE.md and correct the commit count I did not watch print"*.

> **NEW RULE, generalising rev 15's: AN ANCESTOR CHECK IS ONLY AS GOOD AS THE
> NEWEST COMMIT IN IT.** rev 15 learned that a content check greping only this
> revision's strings cannot detect a lost ancestor. The twin is that an ancestor
> loop whose newest entry predates the revision you are verifying cannot detect
> that revision's loss. **Both checks must reach forward to the tip.** The
> ancestry loop below now ends at `efc1268`, a rev-18 commit.

The guards proved it was *precisely* rev 17 that was missing and nothing else:
every figure in the rev-18 prompt's §2 table reproduced except **objects at
`materials:` 122 vs 126** and **meshes 181 vs 185** — both off by exactly four,
rev 17's four hubcap rings.

The owner recovered the files mid-session. rev 17 pulled clean to **75 commits**,
7/7 content checks, 5/5 ancestry, and rev 18's three commits rebased onto it with
**one conflict, in `audit.py`, where rev 17 and rev 18 had independently made the
same fix** (importing `verify.SPEC["L"]`). rev 17's comment was kept.

**Environment fact worth carrying:** the device bridge moved **1 MB per call,
one file per call**. 4 MB failed every time and four 1 MB files in one call
failed; four *separate* single-file calls issued in parallel all succeeded.
`split -b 1000000` into a fresh subfolder, stage in parallel, `cat` back, verify
by md5. `device_bash` cannot `rm`, so use a new subfolder name.

---

## 1. RESTORE — SIX bundle lines now

```bash
git clone tacombi_history_rev9.bundle tacombi && cd tacombi
git pull --ff-only ../tacombi_rev14_unified.bundle HEAD          # -> 59
git fetch ../tacombi_rev14b_incremental.bundle HEAD:refs/heads/b14   # FETCH
git pull --ff-only ../tacombi_rev15_incremental.bundle HEAD      # -> 67
git pull --ff-only ../tacombi_rev16_incremental.bundle HEAD      # -> 71
git pull --ff-only ../tacombi_rev17_incremental.bundle HEAD      # -> 75
git pull --ff-only ../tacombi_rev18_incremental.bundle HEAD      # -> 81, clean
```

Content checks — the last four are rev 18's, the middle ones are ancestors:

```bash
grep -c '### 10.48' SPEC.md          # 1   rev 18
grep -c '_arch_lip_z' verify.py      # 2   rev 18
grep -c '_ARCH_DMIN' t1_shell.py     # 2   rev 18
grep -c '_ROOF_FLOOR' audit.py       # 4   rev 18
grep -c '### 10.44' SPEC.md          # 1   ANCESTOR rev 17
grep -c 'A CLASS GATE IS A PROBE TOO' cream_rms.py   # 1   ANCESTOR rev 17
grep -c 'matte_tap' studio.py        # 6   ANCESTOR rev 17
grep -c '### 10.37' SPEC.md          # 1   ANCESTOR rev 16
grep -c '_coons_cap' t1_core.py      # 3   ANCESTOR rev 16
grep -c 'The threshold is not the parameter' post.py # 1   ANCESTOR rev 13
```

Ancestry — **note the last entry is a rev-18 commit, which is the point**:

```bash
for c in f3c53f4 87aeaa6 d519fc6 5087b84 7ce3d03 f3cde44 efc1268; do
  git merge-base --is-ancestor $c HEAD && echo "$c ok" || echo "$c LOST"; done
```

---

## 2. GUARDS — the figures I watched print

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 1 warn** | **0 fail, 1 warn** |
| warn | roof crown @ rear axle **1.983** vs 1.960 (**+23 mm**) | **1.983** |
| **rear arch lip above hub** | **0.3722 m → tyre gap 39.7 mm** | **same** |
| **front arch (control)** | **0.3732 m → 40.7 mm** | **same** |
| **rake** | **17.75 mm/m (locked 17.75)** | same |
| dome deficit | +0 | +0 |
| rear overhang | 0.7730 | 0.7730 |
| dims | L=4.065 W=1.750 | same |
| cut roof hole | **68052v** | **252123v** |
| objects at `materials:` | **126** | **126** |

Also: 185 meshes; 42 materials; 5 constant-rough; **0 non-manifold**; three open
apertures on +Y; four shut lines 100 % open; band 1.372–1.775; bay widths
**0.516 0.515 0.516**; roof aperture open and solid fore/aft/both sides.

**The roof-hole vertex counts changed by 36 / 212** from rev 17 — that is the
corrected rear-arch outline and nothing else.

---

## 3. WHAT REV 18 DID

### 3.1 The first adversarial audit of the rev-16 loft — `AUDIT_rev18_loft.md`

Four agents on disjoint files (`t1_core`, `t1_shell`, `verify`+`audit`, the
prose), all **read-only**, each told to REFUTE. Three ran concurrently on the
2-core box; that remains the pattern.

**Two of the four defects I briefed them to find do not exist**, and both were
killed by measurement:

- The "12.7 σ overhang violation" is an artefact of `probe_rev16.py` printing a
  **metric** ratio under an **image** label. `verify.py:371-381` states the
  distinction correctly and is the best-written passage in rev 16; 0.773
  reproduces from the projective map to **0.7727**.
- The "3 mm agreement" on D is a **units-of-definition error**: `RT+CR` is
  roll-start-to-crown and the photograph measures lip-to-crown, differing by the
  3.62 mm gutter term. Properly compared, **the model reproduces the photograph
  to 0.18 mm.** Rev 16 was more accurate than it claimed.

**Rev 16 confirmed right on eight counts, recorded so nobody re-opens them:** the
`zlo` fix is real and its margin tracks the crown (hole open at 315/315 grid
points; the historical "worked by luck by 6 mm" reproduces at **+6.1 mm**);
`vol 3.651e-01` is the **cutter's own volume**, not removed material; `_aft()` is
exactly the identity forward of the rear axle over 4001 samples at
`delta 0.000e+00`; the n-gon cap's 1.4 mm forward pull is gone (**+0.014 mm** over
11 304 vertices); the Coons cap is watertight with max valence 4 and zero
coincident vertices; `NHALF = 57` was chosen on a reproducible guard result; the
aft foot lands at **313.0 mm**; the +23 mm warn is a **real probe**, 1.9835 ±
0.0007, agreeing with analytic to 0.03 mm.

Two agents caught **themselves** — one binned a 42 mm defect that did not exist
after finding its estimator was locking onto an LUT knot 1 mm from the roll
start; the other predicted a probe could not see something, then found the
function it had read was shadowed by a second definition 300 lines below.

### 3.2 Three dead `verify` rows and one constants-only guard — §10.45

Each repaired by expressing the threshold in terms of the constant it shadows,
and each **falsified after the repair**. Full detail in §10.45 and in the audit.

### 3.3 The rear arch — §10.46

Crown double-count, refuted trace point, mirrored sign. Applied together.
**Tyre gap 20.2 → 39.7 mm**, front arch unchanged at 40.7 mm as the control.
The guard was not widened.

### 3.4 `STATE.md`'s three phantoms — §10.47

Including one nobody had found: the mid-wheelbase roof height was **the rocker,
seen through the roof hole**, off by **−1612.8 mm**.

### 3.5 px/m on `ref_rear34.jpg` — §10.48

**344.1 ± 6.7 px/m** on the plate plane, with rev 15's own gradient for that
feature refuted by a third method. **`PLATE_W = 0.3300` has no provenance
anywhere in the repo** and that must travel with the number.

---

## 4. THINGS THE NEXT CONTEXT MUST NOT SILENTLY UNDO

- **`_arch_lip_z` returns `None`, never an endpoint.** That is the whole point —
  `audit.py`'s `or -9` and `_roof_at`'s fall-through are the two failures this
  repo has had from a probe that answered when it should have declined.
- **`_ARCH_D` is derived from `_ARCH_D0` by expression, not stored as a second
  table.** Re-tracing the profile cannot leave the re-basing stale. The assert on
  both end conditions is load-bearing.
- **`_arch_drop` negates `t` on purpose** (§10.46c). Removing the negation
  mirrors the arch.
- **The engine-lid and rear-window thresholds are offsets from `X_TAIL`.**
  Re-typing either as a literal restores a guard that cannot fail.
- **`H` in `audit.py` excludes `lid_*` by NAME PREFIX**, not by an enumerated
  list, so it cannot go stale the way `_COUNTER_PARTS` nearly did.
- **The height row deliberately has NO target.** It is the wrong test for
  `H_ROOF` and rev 8 already knew that. Do not re-arm it.
- rev 17's own do-not-undo list still stands in `HANDOFF_rev17.md` §3.

---

## 5. STILL OPEN

- **The cream map is still not built.** px/m is now locked, `cream_rms`'s rev-17
  instruments are back, and the mechanism is identified (modulate `FadeVert`
  spatially and drive roughness; **not** albedo breakup). **Ablate to zero
  first.** Note the scale is on the **plate plane** and the cream patches are on
  other planes — the depth correction has to be stated, not assumed.
- **`PLATE_W = 0.3300`** — unsourced. Bounded by the wheel control at
  < 0.1754 m, not measured.
- **`H_ROOF = 1.960` is now UNSUPPORTED**, and this is new. Its only
  ground-line-free confirmation was `LOFT_GROUND` §1.2's 1.9621, whose
  interpretation §10.34 withdrew without noting that it was 1.960's only escape
  from the datum §10.11 bans. The height 253.21 **reproduces**; the fixed-skin
  257.2 does **not** (3.5 σ). Direct mesh probe reads **1.9835 ± 0.0007**.
  Owner's call, still not taken.
- **"R = 2.45 stays refuted" is false** — computed with the retired `RT_ALL` and
  `Yt`. At rev 16's own values, R = 2.45 needs D = 0.2029, **0.17 σ** from the
  clean 0.209, and **R = 2.30 reproduces it to 0.9 mm**.
- **`D = 0.2116 "independently measured"` is `1.960 − 1.7485`** — the banned
  ground line minus the chain §10.34 calls 29 mm low.
- **Five live shut-line × aperture crossings, 1209 mm total, one on the show
  flank** (the cab-door shut line merges with serving bay 0 above z ≈ 1.40).
  Pre-dates rev 16. The `t1_shell:391` assert covers 1 of 4 outlines, 1 of 2
  arches, 0 of 5 apertures; `CARGO_GAP`'s 28 samples all lie on the corner arcs
  = **5.2 %** of the outline, and `gap_cargo_mid` is never sampled at all.
- **`probe_rev16.py`'s docstring is false** and line 90 prints `xa` against `xa`.
- **The rear-window "+0.15 m above" control still passes** after the repair.
  Unresolved, logged, not tuned away.
- **Needle slivers survive at SUB=2** — shortest edge 0.36 µm on a face spanning
  13.3 mm. `ZERO_AREA` is an **area** threshold and area is the wrong statistic.
- **`folk_gen.py:220-227` re-types four `t1_core` constants** under a header
  saying it reads them off `t1_core`: `X_TAIL` **235 mm stale**, `RAKE_DZDX`
  **15.3 mm/m stale**.
- **SPEC §1713's table still lists `RAKE_DZDX` as 0.0330** while the code and
  §10.9 are 0.01775.
- rev 17's open list stands: `COUNTERTAN`'s interreflection test (**still not
  run**), the tail-lamp material slot, `Senor`'s letterforms, `SCR` +80 mm aft
  and 12–24 mm short, the vision pass over the ~12 unverified image URLs, the
  head-on rear elevation, the flat tail-panel height.

---

## 6. THE ONE PHOTOGRAPH STILL WORTH ASKING FOR

Unchanged and now worth more: **a head-on rear (or front) elevation from roof
height or above, with the counter and the lids clear of the section.** It
settles the flat tail panel, the `RT`/`CR` split, and — newly — it would give
`H_ROOF` a datum that is not the banned ground line.
