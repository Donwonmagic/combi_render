# LEDGER — rev 68

## §1 WHAT REV 68 WAS ASKED FOR, AND WHAT IT DID

Asked: §3 item 1 — **make the nose fixtures follow the skin (F217), add the
verify row that would have caught it, then re-parameterise, then FIT
`NOSE_BULGE` to F221's bracket of B ≈ 40 mm, then render, crop and LOOK.**

**DONE:** the fixtures follow the skin; the guard exists and was watched failing;
the honesty repairs of §3 items 4 and 5; and the adversaries of §3 item 7.

**NOT DONE, AND DELIBERATELY: THE FIT.** Rev 68 refutes the target it was told to
fit to. **F221 measured the BUMPER and scored it against the SHELL** — two
different pressings — and the built bumper is **DEAD FLAT over precisely F221's
own window**, so the instructed fit would have moved the measured quantity by not
one micron. **F222/F223.** The register row *directly above* F221 — F216, same
revision, same grade — already said so, and F221 does not cite it. F209's shape,
one revision later.

---
## §2 THE HEADLINE — F221 MEASURED THE WRONG PRESSING (F222)

`t1_detail.bumper(front=True)` appends eleven points at CONSTANT x under its own
comment `# flat nose face`:

```
    seq.append((nose[0], -nose[1] + 2 * nose[1] * i / 12))    # nose = raw[-1]
```

`_plan_curve` returns `(x, T.WX(x) * T.G(z))`. At the blade's authored z = 0.4800:

```
    T.G(0.48) = 0.9656   T.WX(2.108) = 0.7244   ->  flat run spans |y| <= 0.6995
    F221 forward-models  x(y) = x0 + B(1 - (y/0.70)^2)  over  |y| <= 0.70
                                          THE SAME SPAN
```

**MEASURED ON THE MESH, TWICE, BY TWO INDEPENDENT BUILDS:**

```
    built bumper_f TOP EDGE     |y|=0.00 x=2.1305   |y|=0.45 x=2.1305
                                |y|=0.60 x=2.1305   |y|=0.70 x=2.1304
    ==> BUMPER plan bulge  x(0) - x(0.70) = +0.05 mm   (mine)
                                             0.077 mm   (adversary, own build)
    SHELL at the same height    +8.26 mm
    SHELL at z 0.65/0.80/0.95/1.10   +19.64 / +19.83 / +19.99 / +16.84 mm
```

**AND `NOSE_BULGE` CANNOT REACH THE BUMPER AT ALL.** The bulge ellipse is
`((z-1.00)/0.46)^2 <= 1`, i.e. **z in (0.540, 1.460)**; the blade centre is
**0.480**, where `max(0, 1-r) = 0` for every y. `grep -n "nose_shape" *.py`
returns **one call**, on `body`. Nothing drapes or re-registers `bumper_f`.

**WHAT SURVIVES IS BETTER THAN F221, BECAUSE IT NEEDS NO CAMERA.** A straight
3-D line images straight under ANY pinhole camera at any pose, so the SIGN is
projection-invariant. The photographed bumper's near half is curved at
**11–14 σ**; the built bumper is straight **by construction, everywhere**. The
defect's EXISTENCE is proven with no camera model, no EXIF, no F26, no distortion
term — **and it lands on `t1_detail.bumper`, not `t1_shell.NOSE_BULGE`.**

**CEILING, AND IT NARROWS THE CLAIM.** The curvature is **not uniform across the
window**: over `u < 220`, the half spanning the centreline, the sagitta is
**+0.08 ± 0.36 px, consistent with ZERO**. A plan parabola has constant second
derivative in y, so the single-parabola fit is a mis-model and the ±0.09 px is a
formal error on it.

---
## §3 WHAT REV 68 BUILT (F217 IS CLEARED)

`t1_shell.nose_bulge_at()` is now **ONE expression with TWO callers** —
`nose_shape()` displaces the shell with it, `build.py` asks it how far the skin
under a fixture has moved. `nose_fixture_dx()` is the difference of two
evaluations, hence **EXACTLY 0.0 at the authored bulge** and 13.38 mm at 0.045.
Arithmetic, not a raycast: a raycast baseline would depend on `T1_SUB`.

`HL_X = HL_X0 + S.nose_fixture_dx(HL_X0, HL_Y, HL_Z)`; the indicator likewise, at
**its own station** rather than inheriting the lamp's — the pod sits 130 mm
outboard and 206 mm above, on differently-curved metal (rule 7).

**THE GUARD, IN THE SAME EDIT (rule 13).** `verify._nose_fixture_reg` RAYCASTS
the built mesh and measures each fixture's REARMOST face against the skin at its
own (y, z) — an independent ruler from the arithmetic that placed it (rule 38),
and it asks the geometry, not the pose.

**WATCHED, ALL THREE (rule 3):**

```
    NOSE_BULGE 0.019 shipped                VERIFY: 0 fail, 0 warn
    NOSE_BULGE 0.045, T1_NOSE_FIXFOLLOW=0   VERIFY: 8 fail, 1 warn  <- REFUSES
    NOSE_BULGE 0.045, follow ON             VERIFY: 0 fail, 1 warn  (length)
```

**THE WINDOW IS PART OF THE MEASUREMENT (rule 8).** My first cut took the ray's
first hit. At the headlamp station the ray goes **straight through the cut bore**
and lands on the REAR of the bus at x = −1.8702, printing a "gap" of **+3967 mm**
— a number that looks like a measurement. Hits must be forward of x = 1.5;
`hl_bowl` sits wholly behind the bore, returns all misses, and is reported **NOT
GRADEABLE** rather than silently skipped.

**CONTAINMENT, MEASURED THREE WAYS.** `HL_X` evaluates to the float `2.1015` and
`IND_X` to `2.096` — the old literals to the bit; `STATE.md` regenerated at
`T1_SUB=2` moved **only in provenance** plus the new row's log lines, every vertex
count and dimension identical; and the render diff is at the noise floor (§5).

---
## §4 WHAT REV 68 GOT WRONG IN ITS OWN WORK

1. **I ASKED THE OWNER THE WRONG QUESTION.** I put the straight-edge-and-ruler ask
   to him as the brief instructed. He rejected the premise: ***"This has to be a
   commonly available measurement."*** He is right — a T1 bumper is a catalogue
   pressing on one of the most documented vehicles ever built. **F229**, and the
   ask is RETIRED in `PHOTOS_WANTED_rev52.md`.
2. **MY FIRST REGISTRATION MEASUREMENT PRINTED +3967 mm AND I NEARLY BELIEVED IT.**
   Rule 8 again; caught by the number being absurd rather than by reasoning.
3. **MY FIRST CONTAINMENT CHECK WAS A DIFFERENCE WITH NO FLOOR UNDER IT.** I
   diffed the render before and after, got 2.436 % of pixels moving by >8 levels,
   and had no idea whether that was my change. It was not — see §5. **A
   percentage-changed with nothing to compare it against is not a measurement**,
   and I had to render the control twice to find that out.
4. **MY FIRST OWNER FIGURE WAS ILLEGIBLE** — legend text in white-on-photograph,
   the "B" label overlapping the curve it labelled. Caught by rendering it and
   LOOKING at it before sending, which is the only reason it did not go out.
5. **THE `ck` COMPARISON WITH A SPACE IN IT FAILED ON WHITESPACE**, printing
   `got 13.380.00 want 13.38 0.00`. Trivial, but it is the same class as reading
   an exit code: the harness ate the thing I thought I was comparing.

---
## §5 THE RENDER NOISE FLOOR — MEASURED FOR THE FIRST TIME (F228)

```
    IDENTICAL TREE, TWO RUNS   >8 levels 42 955 px = 2.441 %   worst channel 40
    BEFORE vs AFTER my change  >8 levels 42 876 px = 2.436 %   worst channel 40
```

Indistinguishable to three decimals. No Cycles seed is set anywhere in this tree.

**AND IT PARTLY REFUTES F217's OWN RENDER EVIDENCE.** F217 published *"2.54 % of
pixels differ by >8 levels, worst channel difference 179"*. **The floor is
2.44 % by that same statistic**, so the pixel-COUNT half proves nothing. What
survives is the half that should have been quoted: **worst channel 179 against a
floor of 40**, and the LOCALISATION. **Binding on every future render A/B,
including the emblem's: render the control twice and publish the floor.**

---
## §6 THE MACHINE'S VERDICT AT CLOSE OF REV 68 — every one watched print

```
bootstrap.sh              ALL 10 PASS -- clone arrived SHALLOW, the ELEVENTH
                          running, AND PIL WAS MISSING (3 FAILED until
                          `pip install pillow`).  Row 9 PASSED.
verify_clone.sh           ALL 342 PASS on a clean tree.  336 -> 342.
                          ONE row RE-BASED with the cause named and FIVE
                          companion rows.  NO row relaxed.
build.py T1_VERIFY=1      VERIFY: 0 fail, 0 warn at SUB=1
audit.py T1_SUB=2         VERIFY: 0 fail, 0 warn -- STATE.md moved ONLY in
                          provenance plus the new row's log lines
probe_rev46_vw.py         12 checked, 1 FAILED -- C4 ONLY, at 0.0755
probe_rev67_nose.py       WITH A FRAME: 5 checked, 1 FAILED (P3, a correct
                          refusal).  BARE: now says P3 DID NOT RUN (F225)
probe_rev64_shear.py      6 checked, 0 FAILED
probe_rev65_unproject.py  10 checked, 0 FAILED
probe_rev63_trace.py      ALL CONTROLS PASS -- five of its NINE cannot fail
probe_rev63_reach.py      ALL CONTROLS PASS
vw_pressing.py            5 checked, 0 FAILED
trace_outline.py          SELFTEST PASS ;  svgraster.py  SELFTEST PASS
audit_brief.py            10 checked, 0 FAILED
audit_adversary.py        57 asked, 0 BROKE -- FOUR questions REPLACED
T1_VW_CAPMIN=1            REFUSES, exit 1 (was a bit-identical no-op)
T1_VW_PUREFIT=1           REFUSES with a summary line, exit 3 (was a traceback)
T1_VW_WFRAC=0.1800        REFUSES with a summary line, exit 3 (was a traceback)
                          <- this is F204's OWN before-side
```

**AND THE STANDING WARNING.** Not one of those 342 rows compares the model to a
photograph. The three that do are `flank_compare`, `gloss_compare` and
`probe_rev46_vw` — **and two of the three still fail.**

---
## §7 WHAT REV 68 DID **NOT** DO

1. **THE BUMPER IS NOT FIXED.** F222 identifies the defect and measures it at
   0.05 mm; nothing was built. It is rev 69's top item.
2. **`NOSE_BULGE` DID NOT MOVE**, and now for a THIRD reason: not the fixtures
   (fixed), not the photographs (F221 retargeted) — **nothing in the record
   excludes the shipped 19.6 mm** once F221's own failed validation is propagated
   (F223, B in [16, 76] mm).
3. **C4 IS STILL RED** at 0.0755, and F224 now shows `T1_VW_SOLVE=1` **cannot
   move `VW_W_ARM_X` at all** — the clip is (0.05, 0.95), the shipped value
   1.1002.
4. **F205 IS UNCHANGED AND STILL RED.** Looked at on `out/r68b_front.png`: the
   W's outer arms visibly stop short of the ring.
5. F226's `PHOTO_E, PHOTO_N = 3.390, 7` literals in three probes; F156 (eight
   revisions); `REMAINING_WORK_rev61.md` §I (27 rows, eight revisions);
   `probe_rev63_shapefit.py`; glass, tyres, the tail's barrel, the shut lines,
   F143's roof loudspeakers; `delivery/READ_ME_FIRST.txt`.

---
## §8 THE BRANCH, MEASURED AT PICKUP AND AT CLOSE

```
AT PICKUP   clone SHALLOW -- the ELEVENTH revision running.
            AND bootstrap.sh FAILED 3 of 10 on a fresh clone: PIL was missing.
            `pip install pillow` fixed it; the toolchain does NOT come up clean.
            fetch --prune printed
              - [deleted]  origin/claude/nose-fixture-alignment-r68-rrqyqx
            -- THE DESIGNATED BRANCH, before anything was pushed, THE ELEVENTH.
            HEAD 0 ahead / 0 behind origin/main.  bootstrap row 9 GREEN.
            git diff --name-only HEAD...origin/main -> EMPTY (no new photographs).
AT CLOSE    re-measured with `git fetch --all --prune` first, AFTER the push:
              HEAD 5 ahead / 0 behind origin/main
              clone NOT shallow (unshallowed at pickup, 626 commits)
              git diff --name-only HEAD...origin/main -> EMPTY -- origin/main did
                NOT move during the revision and NO new photographs arrived
              working tree CLEAN;  verify_clone.sh ALL 342 PASS;  bootstrap ALL 10 PASS
            branch: claude/nose-fixture-alignment-r68-rrqyqx, pushed, tracking.
```
