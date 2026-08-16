# HANDOFF — rev 33

**NO GEOMETRY MOVED. NO SHADER. NO ARTWORK.** The last geometry change is
still rev 30's. Guards **0 fail / 0 warn at both levels**, every figure
identical to rev 30's, rev 31's and rev 32's.

## 1. What rev 33 was handed, and what it did first

Folder **already connected on the first `get_device_info` call** — second
revision running. All 26 bridge files crossed with **zero transient
failures**, a first. Restore 34 → 59 → *(fetch rev14b)* → 67 … → 166.
**47/47 content greps, 11/11 ancestry, 3/3 texture md5s**, both split files
md5-matched on both sides.

## 2. THE OWNER ANSWERED THREE QUESTIONS

- **Q1** — the over-rider bar's far termination is at **candidate line 1,
  u = 205**.
- **Q1b** — it is **AT line 1, NOT left of it**.
- **Q2** — the bumper top, the rim face and the hub cap are **ALL CLEAN**.

## 3. SPEC §10.87, in six parts

**§10.87.1 — §10.82's NAMED GAP CLOSES.** The global `f = 0` gains three
surfaces of owner support, 0.751 m² of up-face area at the front of every
hero. **The film does NOT need to become LOCAL.** Nothing was tuned — §10.82
retired a DERIVATION. Ceiling kept: two of the three pointers are on
`ref_side.jpg` and **there is no answered anchor on that frame at all.**

**§10.87.2 — TWO MORE INHERITED PROBES ARE DEGENERATE.** `probe_clean_top.py`
fails H1/H2/H3; `probe_dust_anchor.py` fails two C3 arms. Both print
`live coverage f = 0.000000` — they were written in rev 27/28 against the
pre-retirement chain. **One is worse than a failing control:**
`probe_clean_top` now prints `dusty COUNTERTAN (SHIPPED)` and
`CLEAN COUNTERTAN (f = 0)` as **identical triples** and
`worst channel |err|: dusty 34.0 % -> clean 34.0 %`, while its prose still
argues "removing the dust is NECESSARY". **Its A-vs-B comparison has become
A-vs-A and nothing about it is red.**

**§10.87.3 — `STATE.md` WAS ONE REVISION STALE.** Byte-identical to
`STATE_rev31.md` (`a74f534c…`); rev 32 never re-committed it. Provenance-only
diff, so no figure was wrong. **Recorded in SPEC FIRST, regenerated SECOND**,
in that order, so the evidence survives the fix.

**§10.87.4 — REV 32's Q1 FIGURE QUOTED A PLANTED SYNTHETIC VALUE AS A
MEASUREMENT.** `0.626` is P1b's `f_true`, planted on a synthetic map; the live
value at u = 209 is **0.6160**. `0.820` at u = 224 reproduces nowhere; C5
gives **0.7943**. And **candidate lines 4 and 5 sat at/beyond
`strut_u = 228.0`**, where C5 declares ORDER BROKEN — two of five options the
route could not consume. Rebuilt as `rev33_q1_barend.png`, which hard-codes no
`f` and **refuses to draw** if its positive control fails.

**§10.87.5 — THE OWNER CLOSED THE FAR END; THE ROUTE STILL FAILS.**
`f` at u = 205 is **0.5897**. With Q1b bounding the left side the residual is
**3.5 px → 5.4 %, inside the published dU ≤ 4 px / 6.2 % level. ON THE FAR
END, HE CLOSED IT.** But the cross-ratio consumes **four** columns: C3
measured two, P1b graded one, and **the FAR STRUT at u 228 was never measured
and never graded** — hard-coded, its own print labelling it `(blob)`, and
u 228 is rev 32's candidate line 4, inside the same superposition. Graded
here for the first time, far end held at 205:

| far strut moves | `f` swings |
|---|---|
| ± 4 px | **11.1 %** |
| ± 8 px | **23.7 %** |

**THE UNGRADED COLUMN IS THE MORE SENSITIVE OF THE TWO** (11.1 % vs 6.2 %).
**THE POST STAYS UNBUILT. NO `f` IS PUBLISHED AS A BUILD VALUE.**

**§10.87.6 — carried forward unchanged:** §10.83's centreline claim
**UNDECIDED, fourth revision**; REF §9's V-swage height a bracket
**≈0.40–0.49 m**; the transverse-VP route **UNPUBLISHED, not refuted**;
`422 px/m` consumed nowhere; the hero proved by content and not re-shot.

## 4. NEW RULES, both earned by breaking something

> **A PROBE OUTLIVES THE WORLD IT WAS WRITTEN IN.** When a lever is retired,
> every probe that DIFFERENCES that lever silently becomes a comparison of a
> value against itself — and it keeps printing, keeps formatting, and keeps
> narrating. **A degenerate comparison is more dangerous than a failing
> control, because nothing about it is red.**

> **A PRE-COMMITMENT IS A PROBE TOO.** rev 33's was under-specified — it named
> a residual without naming which reading of it applied, and the two readings
> disagree ACROSS the decision boundary — **and it was aimed at the wrong
> term** entirely. State which quantity a pre-commitment binds, and check that
> it is the quantity the estimator is most sensitive to.

And **§10.86's rule fired again**: a control that fails can hide the defects
downstream of it. C5 failed on the far end for two revisions, so no revision
ever asked what ELSE C5 consumed.

## 5. FALSIFIED IN SIX ARMS — AND FOUR OF THEM DID NOTHING ON THE FIRST TRY

| arm | result |
|---|---|
| retired literal into SPEC's FROZEN FRONT MATTER | **1 fail** |
| `BAR_RISE` + 3 mm | **2 fails** |
| `overrider_bar` dropped from `build.py` | **1 fail** |
| `W_DUST_FAC_UP` restored **in source** | **hard AssertionError at import** |
| `STRUT_U` corrupted in `probe_rev33_barend.py` | **A1 FAILS** |
| positive control corrupted in `mark_rev33_q1.py` | **REFUSES TO WRITE, exit 1** |

**FOUR ARMS FAILED TO APPLY BEFORE THEY WORKED, and every one was caught by
printing the changed line** — rev 32's rule, and it paid four times in one
revision:
1. arm 1 injected `311.5`, which **is not a watched literal**; the row watches
   `post at the vehicle's centreline`. Printed **0 fail** — indistinguishable
   from a guard that did not fire.
2. arm 2's `sed` swallowed the trailing comment, putting `+ 0.003` **inside a
   comment** behind an unbalanced paren.
3. arm 4 first inserted into a **comment line** (SyntaxError), then used
   `T1_W_DUP` — **a documented escape hatch whose own comment says it skips
   the assert**. Only restoring `0.7313` in source fired it.
4. arm 6's `# ARM` comment broke the dict literal; the figure "refused to
   write" **because it crashed**, not because the control fired.

## 6. Things you must not silently undo

`HANDOFF_rev32.md` §8, rev 31's §6 through rev 18's §4 all stand in full, plus:

- **`probe_clean_top.py` and `probe_dust_anchor.py` are LEFT FAILING.** Their
  failures are the record of §10.82's retirement. **Do not widen a tolerance
  to green them.** Repairing them means rewriting what they compare, which
  needs a decision about what the post-retirement question even is.
- **`probe_orb_xratio.py`'s C5 is LEFT FAILING.** It is a KILL control.
- **`probe_orb_post.py` keeps `V_APEX_U = 311.5`** beside the corrected
  anchor. A probe that cannot reproduce its own published result is not a
  record.
- **`rev32_q1_barend.png` is KEPT** as the record of what rev 32 sent, beside
  the corrected `rev33_q1_barend.png`.
- **The `_RETIRED_VALUES` row is kept for the fourth time**, offset 76.7 px.
  **Watched FIRE this revision.**
- **`T1_W_DUP` remains a supported render lever** and deliberately skips the
  §10.82 assert. That is not a hole; it is how the Q2 A/B figure was shot.
