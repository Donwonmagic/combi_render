# HANDOFF rev 31 — the post's blocker was §10.83's own refutation

**NO GEOMETRY MOVED.** No constant changed, nothing was built, nothing retuned.
Guards **0 fail / 0 warn at BOTH subdivision levels**, every published figure
identical to rev 30's. **150 commits, clean tree.**

What this revision produced is a **status correction to a claim recorded as
settled**, a **route refuted before it was spent**, and **an item removed from
the work list because it was already done**.

---

## 1. Item 1 — A HERO WAS OWED TWICE OVER. IT WAS ALREADY SHOT.

`rev30_hero34f.png` sits on his Desktop: 4800×3200, 15.5 MB, timestamped
**~10 hours AFTER `NEXT_CONTEXT_PROMPT_rev31.md` was written**, which is why
that prompt does not know it exists. It was not assumed to be anything. It was
measured:

- it carries the **over-rider bar and its hoop end** — a member present in no
  revision before rev 30. `rev25_hero34f.png` at the same crop is a clean
  negative control: bare blade, nothing above it.
- **CONTROL:** the backdrop is **bit-identical** between the two frames, max
  channel difference **0**. So the 11.74 % of differing pixels is signal, not
  render noise between two runs.
- the difference is **41.22 % inside the silhouette against 0.21 % outside**,
  concentrating on **up-facing** surfaces — cab roof mean 9.94, counter top
  5.58, against the vertical flank's 2.64. That is rev 29's split up-face dust
  deposit, corroborating the SHADING independently of the geometry.

**Twenty strip renders were not spent re-shooting it.**

### My first seam test was on the wrong axis, and its own control killed it

It looked for **vertical** seams. `hero.py` strips in **ROW** space, so seams
are **horizontal**. It also fired hardest at `x = 2086`, which is not a strip
boundary — it was reading real image content — and a positive control then
showed it could barely see a full 1-code step (3.14 → 3.66). **No seam figure
was reported off it.** Rebuilt on rows, over subject rows only:

| | worst \|z\| | median |
|---|---|---|
| **OBSERVED** | **2.97** | 0.93 |
| control +1.00 code/seam | 17.36 | 7.34 |
| control +0.25 code/seam | 5.17 | 2.00 |
| control +0.10 code/seam | 3.52 | 0.78 |

Observed sits **below the +0.10-code control**. **CEILING ~0.1 code values.**
This is a different metric from `hero.py`'s stitch-time figure and is **NOT**
comparable to rev 25's 1.91.

---

## 2. Item 2 — the brief's route, ruled on BEFORE it was spent

The brief asked for single-view metrology off the WORKSHOP's architecture, or a
proof it will not close, and to say which first. **RULING: it will not close,
and the reason is not the architecture.**

Any such chain must reach the **vehicle's** fore-aft direction.
`probe_orb_post.py` (NEW, read-only) tries to read it off the vehicle's own long
edges. Three of five pass an rms gate; their pairwise intersections:

| pair | u |
|---|---|
| drip rail × counter lower edge | **+1529** |
| drip rail × belt break | **+1284** |
| counter lower edge × belt break | **−5843** |

Spread **7 372 px across a 1 200 px frame**, and they **change side**. C1 FAIL,
C3 FAIL. **Two of those edges fit straight lines to rms 0.091 and 0.096 px**, so
this is not tracing error — the vehicle's "horizontal" edges are genuinely not
parallel in 3D, and this repo says why: `t1_mats.z_belt(x)` is a SLOPED line and
the roof carries rake and crown.

The building's own lines would calibrate cleanly, but they give the **building's**
frame. Transferring it needs the vehicle's **yaw**, whose only route is the
wheel–ground contacts, and the foreground trolley occludes the front one. **That
is an extra unmeasured link the brief's framing does not carry.**

---

## 3. §10.84 — the refutation that blocks the post compares TWO DEPTHS

§10.83 refuted §10.75's "post at the vehicle's centreline" by setting the post's
columns (357–374, centre **365.5**) against the V apex at **u = 311.5**.

**The apex is on the NOSE SKIN. The post stands in the BUMPER plane**, forward
of it by a standoff **§10.83 itself grades "A CHOICE, not a reading"**. A
centreline point translated forward does not keep its column. The refutation used
one depth's centreline as if it were the other's, and the whole thing is a
**54.0 px** offset.

**The sign of that parallax could not be established and that is reported as a
failure, not leaned on.** The only two centreline features at different depths —
roundel **306.0**, apex **311.5** — differ by **+5.5 px** against REF §9's own
**±4 px** band: **1.38 σ**. C4 FAIL.

**STATUS CORRECTED: REFUTED → UNDECIDED.** It is **not** claimed the post *is*
on the centreline. It is claimed the measurement that ruled it out cannot bear
the weight, and that the rev-31 prompt's "already settled — do not re-open"
listing of it is **wrong**. **The post stays UNBUILT either way.**

### A FIFTH TAUTOLOGY CLASS

§10.83's refutation is not a guard, so the three prior tautology findings do not
cover it. Same defect one level up: **a refutation whose two terms are not
commensurable measures nothing.**

---

## 4. His two answers, given while the revision was still running

| | answer |
|---|---|
| **Q1** far-end feature | **[stated] "Appears to be covering the bumper, the post, and the far end of the bar."** |
| **Q2** the post | **[stated] "bar to blade only, much like the view of the other bar which shows us a triangular bar extending from the bumper upwards and away from the body panel"** |

**Neither is one of the options offered, and both are better than the options.**
Q1 was posed as a four-way classification; he read a **superposition of three
members**, which none of (a)–(d) expresses. Re-examined at ×10 against his
reading the frame agrees: a cream diagonal runs down to an apex near
`(u 240, v 683)`, and the dark wedge beneath it is **the green body panel seen
through the gap between brace, bar and blade** — not a member at all.

**What that establishes:**

1. **the bar's far end IS present** and runs to the bumper's far corner, so the
   bar's two ends **do bracket the post** — the scale-free-fraction route is
   ALIVE;
2. **its column is CONFOUNDED** inside a ~29 px blob with the corner and a
   brace, which is that route's precision bound, **stated before it is run**;
3. **there is BRACE structure at the far end** SPEC has never recorded;
4. **the post is BUMPER-PLANE ONLY** — which **confirms §10.84 from the other
   side**: a stay to the body would have made the post's depth ambiguous and the
   objection soft. Bar-to-blade only, standing away from the panel, means the
   depth difference is **certainly present**, not merely unpriced.

---

## 5. A process defect of my own that destroyed work

**I used `git checkout SPEC.md` to undo a test injection in a file carrying
UNCOMMITTED work.** It discarded the whole of §10.84 and the §10.83 correction
along with the injection, and both had to be rewritten. The arm was re-run
**after** the commit, and the corrected `_RETIRED_VALUES` row **was watched
FIRE**: injected into a non-exempt SPEC section the guard reads **1 fail**
against the clean tree's **0**, with the corrected reason in the message.

**Rule: never revert a file with `git checkout` to undo a falsification arm —
commit the real work first, or the arm eats it.**

---

## 6. What changed on disk

- **`SPEC.md`** — NEW §10.84; §10.83 corrected **in place** (its "THAT IS
  REFUTED" now carries a DOWNGRADED-TO-UNDECIDED marker).
- **`verify.py`** — the `_RETIRED_VALUES` row for the phrase is **KEPT** and only
  its stated reason corrected. **Watched FIRE.**
- **`probe_orb_post.py`**, **`mark_rev31_q.py`**, **`rev31_q_post.png`** — all
  NEW, all READ-ONLY.
- **`STATE.md`** regenerated; `STATE_rev31.md` alongside.
- **NO ARTWORK, NO GEOMETRY, NO SHADER.** `CREAM`, `COUNTERTAN`, `COUNTERCREAM`,
  `RED`, the rake, the roof, the bar and all three textures **UNCHANGED**.

**Things you must not silently undo — rev 30's §3, and rev 29's §4 through
rev 18's §4, all still stand in full.**

---

## 7. Still open

- **THE OVER-RIDER POST.** Now blocked on a *construction*, not a reading: the
  bar's two ends bracket it, the far end is confounded to ~29 px, and the
  projective midpoint needs the transverse VP or an argument that bounds it.
  **The naive midpoint is not the projective one — do not take it.**
- **§10.83's centreline claim is UNDECIDED**, not refuted, and not settled.
- §10.70's percentages must be RE-RUN before being quoted. Harness has no
  cyclorama (§10.78) — state that, do not silently fix it.
- §10.82's unasked surfaces — bumper top, rim barrels, hub caps. **The workshop
  frame shows all three.**
- FRONT BUMPER FACE unmeasured. `CREAM`. ABSOLUTE ROOF HEIGHT. OFF FLANK
  804.9 mm. `COUNTERTAN` 34.0 % short in B.
- `GAL_SKY` dead lever. `PLATE_W = 0.3300` no provenance. `probe_rev16.py:90`
  prints `xa` vs `xa`.
