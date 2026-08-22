# ADDENDUM — for the rev-55 context that was started on the SUPERSEDED prompt

**This file is a POINTER AND A DELTA, not a second source of truth.** The authoritative brief is
`NEXT_CONTEXT_PROMPT_rev55.md`, byte-identical to `PASTE_INTO_CLAUDE_CODE.txt`, which `CLAUDE.md`
auto-imports. **This file RETIRES the moment `origin/main` carries the 191-row brief** — check with
`grep -c 'ALL 191 PASS' PASTE_INTO_CLAUDE_CODE.txt` and delete it when that is 1 on main.

## Why it exists

The rev-55 context was launched from a copy of the brief cut BEFORE its last two commits. That copy
is **internally consistent** — it says `ALL 173 PASS` and `origin/main` really does have 173 rows, so
nothing will fail. It is simply **missing the three things the owner asked for last.**

## FIRST, GET THE RIGHT TREE

```bash
git fetch --all --prune
git merge --no-edit origin/claude/tacombi-rev-54-u7hvys   # 3 ahead of main, 0 behind
./verify_clone.sh        # MUST read ALL 191 PASS.  If it reads 173 you are still on main.
```

**Do not "fix" the row count anywhere.** 173 and 191 are both correct, for different trees.

## THE FIVE DELTAS

**1. `verify_clone.sh` is 191 rows, not 173.** Eighteen reference rows were added (delta 3).

**2. §0 — THE GOAL, now stated before any work item.** Photo-realistic parity with **that exact
bus**, per measurement and not on average. Beside it, the measured distance: **191 rows, 0 of them
fidelity.** Parity rests on two scripts — `flank_compare.py` runs and **FAILS 2 of 4** (ink aspect
2.3689 vs 2.2512; worst region 0.476 Senor), and `cream_rms.py` is **DEAD** until it is re-based on
`ref_rear34.jpg`, which is the remedy the script itself prints and has been open since rev 17.
**Adding a 192nd self-consistency row is not progress toward the goal; making a second gate run is.**

**3. §0.1 — OWNER RULING, rev 54:** *"we have all references that we need on repo and I want to make
sure that is never forgotten."* Two binding consequences:

* **NOTHING IS "BLOCKED ON A PHOTOGRAPH" ANY MORE.** For four revisions the top job was parked that
  way. It is not blocked, it is **hard**. `PHOTOS_WANTED_*` is a wish list, not a gate — carry it
  (rule 16; items 1–5 are still never to be re-asked) but do not let it license parking an item.
  Work every item from what we hold, or close it with *"it cannot be recovered from what we hold"*
  and its ceiling. A live route to the badge stroke weight exists in frames already on this repo.
* **18 ROWS NOW CHECKSUM EVERY REFERENCE FRAME INDIVIDUALLY**, so a loss says WHICH — plus a floor of
  **54** reference-class tracked images and an assertion that the **five** byte-identical pairs stay
  five (a sixth group = a re-sent frame being mistaken for corroboration, rule 11). Until rev 54 not
  one row anywhere named a reference photograph.

**4. §4 is re-framed** from *"what only he can give"* to a carrier and a record of what was asked and
refused. **It is not a list of blockers.**

**5. OWNER RULING, rev 54: "keep studio, fix the model."** He was shown the rendered delivery frame
and told the cost — it reads as clay because the surround is a featureless white cyclorama, so the
paint has nothing to reflect, and that is the ENVIRONMENT, not the shaders — and he was offered four
routes including an environment hero as a SECOND frame that would have moved nothing already
measured. He declined. **Rev 55 is a MODEL revision. Do not propose an environment frame again.**

## THE WORK ORDER (§3.0), because the first three each have a GATE

| | do this | gate |
|---|---|---|
| **A** | **Separate the flank ink LEVEL from the rig's exposure.** Render ink is **+41.2/+38.6/+36.3 DN** on the photograph's, with **G/R 0.936 in BOTH** — hue right, level not. **NOT yet attributed.** Measure the cream either side of the ink in the same two frames through one painted window. If the cream is also ~39 DN high it is the studio lighting, which is his call, and the artwork is exonerated. **Do not touch an ink constant before this.** | `flank_compare.py`'s colour block |
| **B** | Re-base `cream_rms.py` onto `ref_rear34.jpg` | the script's own guards |
| **C** | The two standing `flank_compare` failures | 2 of 4 → 4 of 4 |

## AND THE HABIT THAT PAID TWICE AT REV 54

**Crops generate leads, not findings.** Rev 54 called two defects off crops and **both dissolved**
when the window was painted — a "ring" that spanned all four wheels, and roundel V arms that reach
the band perfectly. Take the lead, paint the window, THEN believe the number.
