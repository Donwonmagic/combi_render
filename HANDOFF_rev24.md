# HANDOFF rev 24 — the solve was measuring the whole scene, and the "self-arming" guard never was

> **THE STANDARD, in the owner's words.** *"The final product should be nearly
> indistinguishable from the original. Any single measurement off is
> unacceptable."* The criterion is PER-MEASUREMENT. And above clinical accuracy:
> *"I really want this to give the person the opportunity to feel like they were
> on Playa del Carmen all those years ago. I want the owner to remember standing
> in the kombi, in this very picture that was provided."*
> **That owner is the restaurant's owner, not Donald. Donald has never stood in
> the bus — never ask him what the vehicle looks like; ask what a PHOTOGRAPH
> shows, then measure it.**

---

## 1. How rev 24 opened — CLEAN, fifth revision running

All six rev-23 deliverables on his Desktop at the exact sizes memory records
(bundle 41 895, tarball 19 698 000, SPEC 240 858, STATE 8 457, HANDOFF 12 908,
prompt 22 509). **Twelve bundles crossed in ONE `device_stage_files` call.**
Seven bundle md5s re-verified against memory, all match, rev 23's included
(`72a72fba…`).

Restore ran 34 → 59 → *(fetch b14)* → 67 → 71 → 75 → 81 → 87 → 93 → 96 → 101 →
**105 commits, clean tree**, no divergent-branches error.
**15/15 content checks exact. 8/8 ancestry.** Guards on arrival, both levels:
**0 fail / 0 warn**, every figure in the prompt's §2 table reproduced.

Blender 4.5.3 + pillow 12.3.0 + scipy 1.17.1.

---

## 2. Guards — ACTUAL output, both levels, after everything

| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 0 warn** | **0 fail, 0 warn** |
| roof crown @ rear axle | **1.9835** (baseline 1.9835, −0.0 mm) | **1.9833** (−0.2 mm) |
| rear arch lip → gap | 0.3722 → **39.7 mm** | same |
| front arch (control) | 0.3732 → **40.7 mm** | same |
| rake | **17.75 mm/m** (locked 17.75) | same |
| dome deficit / rear overhang | +0 / **0.7730** | same |
| dims | L=4.065 W=1.750 | same |
| cut roof hole | **68564v** | **252749v** |
| objects at `materials:` | **126** | **126** |
| shut line × aperture, SHOW | **0.0 mm** | **0.0 mm** |
| shut line × aperture, OFF | **804.9 mm** (baseline 804.9, −0.0) | same |
| `CARGO_GAP` samples | **154** | same |

Also: **185 meshes**, 42 materials, 5 constant-rough, **0 non-manifold**, three
open apertures on +Y, four shut lines 100 % open, band 1.372–1.775, bay widths
**0.516 0.515 0.516**.

**NO GEOMETRY MOVED THIS REVISION.** Every figure above is identical to arrival.
rev 24 is measurement, guards and SPEC only. The roof-hole counts are rev 23's
re-baselined 68564 / 252749, reproduced.

---

## 3. What rev 24 changed

### Item 1 — `COUNTERTAN`'s pedestal (SPEC §10.65)

**The occlusion hypothesis is CONFIRMED, quantified, and it does NOT close the
pedestal.** Carried four revisions unrun. `solve_ctan` renders its masks in
isolation (`shader_solve.py:175`) and its **measured frame with the whole scene**
(`:425-427`). `solve_mural` has carried the fix since rev 15 (`:234`).

rev 20 discarded the *probe*, not the hypothesis, at 21.7 % per-pixel noise —
**the wrong statistic**. Region means over ~10⁴ px put that at **0.21 %**.

`probe_ctan_index.py` (NEW, read-only) uses an **object-index pass**, chosen over
a visibility flag by §10.56's own rule: IndexOB suppresses nothing.

| control | result |
|---|---|
| NULL — IndexOB under `_only(tops)` | **IoU 1.0000, 0 disagreeing px, 0 foreign** |
| POSITIVE — must name a foreign surface | names `gal_warmer`, `gal_caddy0/1`, `T1_body` |
| HARNESS — reproduce §10.56's chain | ratio reproduces; **clipping guard tripped twice** |

**MEASURED:** TOP mask **33.06 % foreign px**; FASCIA mask **57.31 %**. Largest
occluder **`gal_warmer`**, never previously named. **`counter_top` is 21.76 % of
the FASCIA mask** and **97.84 % of the top mask lies inside it** — the solve
divides a region by a **superset of itself**.

**Pedestal, both albedo arms re-measured through the clean mask:**

| | R | G | B |
|---|---|---|---|
| contaminated (reproduces §10.56 at 1 rig) | 68.5 | 68.0 | 72.1 % |
| **clean** | **60.8** | **58.2** | **59.5 %** |
| albedo sensitivity `k` | **+40.3** | **+40.3** | **+40.0 %** |

The residual against the target **flips sign in all three channels**. The
arithmetic correction (58.3/55.5/56.8 %) was **not** reported as the answer — it
assumes occluders are albedo-invariant and they sit on the top catching its
bounce. **Measurement, not inference.**

**A ~59 % PEDESTAL SURVIVES AND IS STILL UNIDENTIFIED. `COUNTERTAN` UNCHANGED,
fifth revision.**

**Two instrument defects, both mine, both caught by controls:**
- **`ST.lighting()` STACKS** — 8 / 16 / 24 lights measured. `solve_ctan` calls
  `cam_setup()` three times, so **every absolute linear figure in §10.56,
  `0.12107` included, is a 3-rig number.** Ratio survives; level does not.
- **Exposure must go through the environment** — `_plain_view` overwrites the
  scene value inside every `_render`. First run **70.54 % clipped**, radiance
  shares collapsing onto pixel shares. **My guard tripped a second time and I
  fixed the cause rather than widening it**, which is how the rig was found.

### Item 3 — a rev-23 REGRESSION (SPEC §10.66)

**rev 23 broke `folk_gen.composition()` and nobody ran it.** The `STEP_M` rename
left the use site behind: `mm` had **ZERO Store sites and ONE Load site**, at a
**top-level statement of the function body**. The census a re-bake depends on
(`COMP_TOP`, `COMP_HIST`, `FLANK_MASSES`) raised `NameError` on every call.
§10.63 verified that rename **by reading**. Repaired, **value-preserving**:
53.2645 mm² both ways.

### Item 2 — THE BRIEF IS REFUTED (SPEC §10.67)

**§0.2's guard is not self-arming.** It compares **material datablock names**;
of ~100 §10 retirements exactly **one** was ever a material. **The false claim
was inside the guard's own comment** — which is why the brief said it.

**`_retired_value_drift()` FIRED ON ITS FIRST RUN and caught three defects
§10.64 missed, all in FROZEN sections:** §1.1's bay taper `0.507/0.516/0.526`,
§1.1's band `1.402/1.798`, §3's `RED (196,106,36)` at grade **M**. Plus
`SPEC.md:2701` — the retired rake still deriving a 79 mm consequence **forty
lines below the table rev 23 struck**, under a heading reading "OPEN,
unresolved" that §10.29 had closed.

**The guard was wrong twice before it was right:** its first cut swept the change
log (**4 of 8 FAILs were its own false positives** — §10.11–10.33 are `###`
headings interleaved with the front matter), and a sub-heading reset its
exemption so it found `:2701` **by accident**.

**§0.2b added, bullets 16 → 29 — and adding it SILENTLY DEFEATED the drift
guard**, whose substring split matched `### 0.2b`. It printed a reassuring `16`
while the section held 29. **Caught by watching the count print.** Parse is
line-anchored now and declines rather than passing silently.

**Falsified in four arms:** clean → 0 fail; unmarked retired value in FROZEN §3
→ **1 FAIL at the exact line**; same value marked retired → 0 fail (correct
boundary); a 30th bullet → 1 warn.

---

## 4. Things rev 25 must not silently undo

Everything in `HANDOFF_rev23.md` §4, rev 22's §3, rev 21's §4, rev 20's §4, rev
19's §4 and rev 18's §4 still stands in full. New this revision:

- **Do not remove `_only` from `solve_ctan`'s measured render.** `T1_CTAN_NOISOLATE=1`
  exists to reproduce the old contaminated arm; the default must stay isolated.
- **Do not quote SPEC §10.56's absolute linear figures without saying they are
  3-rig numbers.** The ratio is comparable; the level is not.
- **Do not re-type `folk_gen`'s constants back to literals**, and do not
  re-introduce a bare `mm`.
- **Do not widen `_retired_value_drift` or add exemption tokens to silence it.**
  If it fires, a retired value is being republished — fix SPEC.
- **Do not describe §0.2 as self-arming.** It buys a forced review, nothing more.
- `B_PILLAR` and `VENT_TOP_DROP` remain AUTHORED. The OFF-flank band stays at
  804.9 ± 10 mm. `H_ROOF` stays retired, band ±5 mm, never widened.

---

## 5. Still open

- **`CREAM`** — unchanged at (206,208,200). Needs a same-light, same-CLASS,
  three-channel reference; **does not exist in the three photographs**.
- **THE ABSOLUTE ROOF HEIGHT** — 1.960 retired, nothing replaced it.
- **`COUNTERTAN`'s ~59 % pedestal** — reduced from ~69 % and **still
  UNIDENTIFIED**. Occlusion is excluded now, alongside dust, wear, fade,
  coat+spec and interreflection. **The next suspect must be named and ablated,
  not guessed.** `k` being 40 % larger than believed changes the arithmetic of
  any future solve — re-derive, do not carry the old secant gain.
- **NOT DONE, and named: the 4800×3200 hero (item 5).** The geometry has not
  moved since rev 23, so `rev22_hero34f.png` still does not photograph the
  current mesh — the cab door, the vent and the cargo outline all moved in rev
  23 and **nothing has photographed them yet.** This is rev 25's item 1.
- **NOT DONE: item 4** — tail-lamp material slot; `Senor` at 0.504 of its 0.782
  ceiling; `SCR` +80 mm.
- **`_ZB_AUTH` in `folk_gen.py` is in the PRE-REV-16 TAIL FRAME** — reported by a
  read-only agent, **not yet verified by me**, so treat it as a claim: it copies
  `t1_core.ZB`'s authored knots without `aft_lut`'s `_aft()` re-space, giving up
  to **76 mm** of z error at the tail. If it holds it is **larger than
  `DOOR_X0`** and dominates the re-bake decision. **Verify before acting.**
- **`folk_gen.DOOR_X0`** — 17.25 mm against the control point, **19.31 mm**
  against the smoothed outline actually cut. Also unverified by me.
- **The committed artwork was baked in the stale frame.** A re-bake is a MEASURED
  operation under §10.10 and `composition()` had to be repaired before one was
  even possible.
- `PLATE_W = 0.3300` still has no provenance. `probe_rev16.py:90` still prints
  `xa` against `xa`.
- **A read-only agent reported ~12 further §10.64-class defects** in §1, §2, §3,
  §6, §10.5 and §10.7 (retired `ROUNDEL_D 0.370`, the refuted fish-eye lens, the
  pure-white lock in §6, `X_TAIL −2.108`, the "not modelled yet" rake).
  **I verified five and fixed four; the rest are UNVERIFIED CLAIMS.** Extending
  `_RETIRED_VALUES` is the cheap way to convert each into a guard.

---

## 6. Ordered work list for rev 25

1. **A hero at 4800×3200** — nothing has photographed the current mesh since
   rev 22, and the geometry moved in rev 23. One strip per `hero.py --only N`
   call, then `--stitch-only`, then `post.py` **once** on the stitched frame.
2. **Verify the `_ZB_AUTH` claim**, then decide WITH MEASUREMENT whether a
   re-bake is owed under §10.10. `composition()` runs again as of rev 24.
3. **Extend `_RETIRED_VALUES`** with the remaining §10.64-class defects, one
   verified row at a time. Each row is cheap and each is a permanent guard.
4. **`COUNTERTAN`'s ~59 % pedestal** — name the next suspect and ablate it.
5. Tail-lamp material slot; `Senor`'s letterforms; `SCR`'s +80 mm.
6. Camera absolutely last.

**NO DECISION IS OUTSTANDING WITH HIM.** The one photograph that would move most
still closes THREE things: a head-on rear or front elevation from roof height or
above closes `CREAM` **and** the absolute roof height; a clear off-flank view
closes 804.9 mm of unadjudicated crossing.

---

## 7. The commit count and the content figures

Written LAST, after the final commit, every figure read off a fresh-clone
verification run rather than typed from memory. **This has gone wrong in ELEVEN
consecutive revisions during handoff assembly**; rev 23 was the first clean one.

Content checks for rev 25 and the final count are in
`NEXT_CONTEXT_PROMPT_rev25.md` §1, read off the verification console.
