# Señor Tacombi combi — a photoreal 3D reconstruction

A procedural Blender reconstruction of **one specific vehicle**: the 1963 VW
Type 2 converted into the Señor Tacombi taco stand in Playa del Carmen. Not a
generic T1. The owner's standard, in his words:

> "We are recreating a photo realistic version of **that exact bus**."
> "**Any single measurement off is unacceptable.**"

The acceptance criterion is **per-measurement**, not on average. A model right
in ninety places and wrong in one is not 99 % done, because the owner will look
straight at the one.

---

## Start here

1. **The highest-numbered `NEXT_CONTEXT_PROMPT_rev*.md`** — the live brief. Read
   it first, in full. **Find it with `ls`; do not trust a filename typed in any
   document, including this line** (`CLAUDE.md`). It was rev 63 when this line was
   last touched. Then `CLAUDE.md` (method, loads every session) and the
   highest-numbered `LEDGER_rev*.md`.
2. **`STATE.md`** — machine-written by `audit.py`. If it and any prose in this
   repo disagree, **it is right** — but check its provenance rows first,
   especially `working tree`. If that says DIRTY, the file records nothing.
3. **`SPEC.md`** — the specification and the complete decision log. §10 is the
   spine: §10.1 → §10.101, every finding, every refutation, every rule and why
   it exists. It is cumulative, so it contains its own history.
4. **The `LEDGER_rev*.md` series, newest first** — what each revision actually
   did, with its arithmetic. *(The `HANDOFF_rev*.md` series ENDED at rev 45 and
   is history, not truth; do not restart it. `HANDOFF.md` and `SPEC_AUDIT.md`
   are rev-3 era — `START_HERE.md` says so and it is right.)*
5. **`REF_MEASUREMENTS.md`** — measurements taken off the reference
   photographs, with their admissibility grades.

```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
/tmp/blender/4.5/python/bin/python3.11 -m pip install pillow scipy
```

## Verify first

```bash
./verify_clone.sh          # exit 0 or 1; it PRINTS its own row total
```
Content checks that replace what used to be thirty hand-typed `grep` lines in
the brief plus a prose guard table. **The count is not written here on purpose**
— it moves every revision, and a number in prose goes stale silently. The script
prints `ALL n PASS` on a clean tree and the newest brief must state that same
n, which a row enforces. **Identity is ancestry, not
arithmetic** — it tests that rev 42's tip is an ancestor of HEAD, so it stays
valid as you commit. **It locates by symbol, never by line number.** It checks
locked *values* (not just that a symbol exists), the signboard gate's
**polarity**, all eight texture md5s, and the guard figures read out of the
machine-written `STATE.md`. Proved against ten null tests. **If it exits 1, stop
— and do not edit the script to make it pass.**

## Build it

Two guards, and **both must be run at both subdivision levels** — the cab-door
booleans passed at SUB=1 and collapsed the shell at SUB=2 for six revisions:

```bash
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=2 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=1 /tmp/blender/blender -b --python audit.py
git checkout -- STATE.md
T1_SUB=2 /tmp/blender/blender -b --python audit.py
git checkout -- STATE.md
```

`audit.py` rewrites `STATE.md` on every run — check it out again afterwards.
**The restore is on its own line, NOT chained with `&&`** (corrected rev 44):
`audit.py` exits non-zero whenever it reports a failure, and `&&` would skip the
restore in exactly the case that leaves the tree dirty.

**Expected: 0 fail / 0 warn on all four runs.** The inventory and every
dimension that used to be typed here live in **`STATE.md`**, which `audit.py`
writes from the mesh it just built. **This paragraph carried a rev-42 snapshot
for sixteen revisions** — 131 objects and 190 meshes against the 223 the machine
now reports — which is exactly the failure mode `CLAUDE.md` opens with: *if you
find a number here, that is the bug.* Read `STATE.md`.

## The hero

```bash
T1_SUB=2 /tmp/blender/blender -b -P hq_render.py   # ONE build, 10 margin'd bands
python3 stitch.py out/hq_hero_raw.png <declared spans>   # CHECK ITS EXIT CODE: 2 = seam
python3 post.py out/hq_hero_raw.png out/hq_hero.png      # optics LAST, never per strip
```

`hero.py` still exists and still works, but **`hq_render.py` is the measured
recipe** (rev 57b): it builds the scene ONCE instead of ten times, renders each
band with MARGIN because Blender's border rounds inward, and it carries the
studio rig itself, because a single-session runner otherwise SKIPS `build.py`'s
preview block — where the lighting is built — and renders an **unlit** frame
that passes every automated check (F51; it shipped once, as a black bus).

One strip per call, then stitch. `post.py` runs **once** on the stitched frame,
never per strip. Strip timings rise down the frame, **peak around strip 16, and
fall again** — 153 s at strip 1, 614 s at strip 16, 390 s at strip 19, because
the bottom strips are mostly ground. **The measured delivery frame at rev 57b:
3840×2640, 256 spp, `T1_SUB=2`, ten bands, seam-free at worst z = 1.62, in
106.8 min** — and the single-session saving over the old ten-build loop is
**8.4 min, 7.3 %**, not the 2.94× an unlit run once appeared to show.

**Full-size heroes are gitignored and are not in this repo. One DOWNSIZED
delivery reference per revision IS tracked** — the owner ruled it at rev 57b so
each revision has the frame it is told to beat without a 107-minute re-render.
The guard is by DIMENSION, not by name: a tracked hero PNG must be ≤ 1600 px
wide.

## The probes

The read-only instruments are `probe_*.py` — **count them with `ls`, do not
trust a number typed here** (it said 31 for sixteen revisions and is now well
past that). **Run the ones you inherit, not only
the ones you write** — and **read each probe's own summary line rather than
grepping for a pattern**, because the wordings differ and a summary grep
under-read six probes in rev 37 and again in rev 39.

Several are **deliberately left failing** and must not be "fixed":
`probe_clean_top` and `probe_dust_anchor` fail by design; `probe_psf_lines`
fails two controls, both expected; `probe_rev40_datum` C3, `probe_rev41_gate`
C4 and `probe_rev42_uv` C3 are all supposed to fail. `probe_rev36_barend`
prints *"REFUSING TO PRINT A RULING"* and that is correct. The expected tallies
are listed in `NEXT_CONTEXT_PROMPT_rev43.md` §3 — **that citation is to rev 43
deliberately, not a stale pointer: the tallies are in THAT brief's §3, and the
highest-numbered brief's §3 is different content.**

## How this project works

Ground in the reference → build → **adversarially** audit → iterate. Never build
before grounding. Never call it done off self-review. Report the measurement
against the reference **with its ceiling**, never a self-assigned score.

Rules earned the hard way, all of them by being broken first (the full set is in
`SPEC.md` §10):

* **A claim in prose is not a guard.** Grep for the node that does it.
* **Never put a figure in an acceptance test unless you watched it print** — and
  a figure in a *comment* may be thirty revisions stale.
* **A control that fails is a result, not a broken instrument.**
* **When a verdict moves with the threshold, publish the sweep, not the verdict.**
* **A gate without a null is not a gate.**
* **An ordinal fact needs no ruler** — which is what makes it admissible where a
  metric is barred.
* **A line you drew is not evidence.** Check the unmarked frame.
* **A guard firing on your own change is the guard working.** Fix the
  construction, never the bar.
* **Ask what a photograph shows before measuring from it.** One marked crop and
  one sentence has settled questions that revisions of measurement could not.

## Reference photographs — the only ground truth

* `ref_side.jpg` — in service, show flank. **The cab door is OPEN 49°** in this
  frame; a closed door's outline cannot be measured from it.
* `ref_workshop.jpg` — the conversion stage, green livery. **The only frame with
  the cab door SHUT.** Everything measured here ships tagged *workshop-stage*.
* `ref_rear34.jpg` — rear three-quarter.
* `ref_*grid*.png`, `ref_x6_lanczos.png` — annotated derivatives, read by no
  code; kept as working reference.

**No supplied frame carries both a closed cab door and an admissible px/m on the
door plane** (§10.62, §10.73). Several measurement routes are closed for good
reasons that are written down; read §10 before assuming a number is obtainable.

## What is NOT in this repo

* **The rendered heroes** — gitignored, ~15 MB each.
* `out/` — all render output.
* The per-revision `SPEC_revN.md` / `STATE_revN.md` snapshots, which are
  redundant: `SPEC.md` is cumulative and `STATE.md` is regenerated by `audit.py`.

## `.gitignore`

Browsers commonly skip dotfiles when a folder is dragged into GitHub's web
uploader. **Check that `.gitignore` actually landed.** If it did not, recreate
it with:

```
out/
*.blend
*.blend1
__pycache__/
rev*_hero*.png
rev*_playa*.png
```

---

## Repository layout

Everything the build actually executes lives at the **root**, because the probes
resolve `build.py`, `ref_side.jpg` and `ref_rear34.jpg` relative to their own
directory. **Do not move any `.py` file or any `ref_*.jpg` out of the root** —
it will break them. Only `STATE.md` is ever opened by code (written by
`audit.py`); every other `.md` reference in the source is a prose citation in a
comment, which is why the historical documents could be foldered.

```
  /                     81 files   the runnable project: 71 .py, the 4 source
                                   photographs, SPEC.md, STATE.md,
                                   REF_MEASUREMENTS.md, README.md, the live
                                   brief NEXT_CONTEXT_PROMPT_rev*.md (highest
                                   number wins -- rev 64 at this edit), EMBLEM_HANDOFF.md (the
                                   CARRIER for the owner's top item), CLAUDE.md,
                                   .gitignore
  docs/                 83 files   37 handoffs, 37 superseded context prompts,
                                   the audit documents, START_HERE, SKEPTIC_PASS
  docs/figures/         19 files   the marked question crops and A/B figures
                                   that settled owner readings
  docs/reference_grids/  5 files   annotated derivatives of the photographs;
                                   read by no code
  tex/                   8 files   the baked artwork — irreplaceable
  analysis/             27 files   one-off measurement scripts, rev 4–11 era
  workflows/             1 file    the deferred specialist-audit workflow
```

## Uploading this to GitHub through the web interface

GitHub's web uploader takes **at most 100 files per drag**, which is why the
tree is foldered this way. Four drags, in this order:

1. Open the repo → **Add file → Upload files**. Select the **81 files at the
   root of `tacombi_github/`** (the files themselves, not the folder) and drop
   them. Commit.
2. Drag the **`docs`** folder in. Commit.
3. Drag **`tex`**, **`analysis`** and **`workflows`** in together. Commit.
4. Confirm `.gitignore` is present in the repo listing. Browsers routinely skip
   dotfiles; if it is missing, use **Add file → Create new file**, name it
   `.gitignore`, and paste the block above.

If you would rather not fight the uploader, from a terminal in the unzipped
folder there is no file limit at all:

```bash
git init && git add -A && git commit -m "rev 42"
git branch -M main
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

## Two known issues in this tree, stated rather than silently fixed

* **`analysis/a1_wheels.py`, `a8_tyreedge.py` and `a10_prof.py` hard-code
  `/home/claude/tacombi/ref_side.jpg`** — an absolute path from the original
  container. They will not run anywhere else until that is changed to
  `ref_side.jpg`. They are rev 4–11 era one-offs, nothing in the build or the
  guards calls them, and they are left as found rather than edited blind.
* **`out/` is gitignored and is not here.** The flank probes
  (`probe_rev39_flank`, `probe_rev40_datum`, `probe_rev41_gate`) need
  `out/p_side.png` and will raise `FileNotFoundError` until you render it.
  **The command is here now** (corrected rev 44 — it used to say *"see §10 of
  the live brief"*, and the rev-44 brief has no §10):

  ```bash
  T1_SUB=1 T1_PREVIEW=side T1_SAMP=24 T1_RX=1400 T1_RY=933 T1_FX=0 \
    T1_PFX=p /tmp/blender/blender -b --python build.py
  ```

  `T1_FX=0` is load-bearing — every mask in that chain is a chromaticity rule.
  **1400 px wide is a FLOOR:** `flank_compare` documents a verdict flip across
  its aspect tolerance at 900 px for no change in the model.

## Where the open work lives — NOT here

**This section used to be a ranked work list dated rev 42, and it sat here for
sixteen revisions competing with the live brief.** It is deliberately gone.
There are exactly three live registers and this file is none of them:

* **`REMAINING_WORK_rev61.md`** — the RANKED EXECUTION LIST, written at rev 60c
  because the owner asked for *"a comprehensive list of just what exactly is
  left, so we know what we need to execute"*. It sorts the register's open rows
  into REAL WORK / CEILED / the owner's call / process debt, and its **§I**
  carries the rows that were in no document at all. **It is a CARRIER.** It was
  an ORPHAN for one revision — no file in the repository named it — which is how
  a carrier gets lost (rule 16); it is named here, in `START_HERE.md`, in the
  brief's reading order and in `verify_clone.sh` so that cannot recur.
* **`OPEN_FINDINGS.md`** — every open finding with an ID and a **provenance
  grade** (`MEASURED` / `RECOMPUTED` / `INHERITED` / `RULED` / `CEILED`). It is
  a CARRIER: rows leave it only by being closed with the measurement that closed
  them, or retired with the ruling that retired them.
* **the highest-numbered `NEXT_CONTEXT_PROMPT_rev*.md`** — this revision's order,
  ranked by `visibility_budget.py` (pixels of the delivery frame), plus §4.1,
  the owner's standing instructions, restored at rev 57b after being deleted at
  rev 44.

**The die-cut vinyl sticker for children at the restaurant — the original
deliverable — is still unbuilt, and the warm low-light "Playa" hero is
deprioritised but NOT cancelled: it carries the emotional bar that sits above
clinical accuracy.** Both are carried as `F18` and `F62`. **This paragraph was
the only place either survived between rev 44 and rev 57b**, which is why it is
kept here as well as in the register.
