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

1. **`NEXT_CONTEXT_PROMPT_rev43.md`** — the live brief. Read it first, in full.
2. **`STATE.md`** — machine-written by `audit.py`. If it and any prose in this
   repo disagree, **it is right** — but check its provenance rows first,
   especially `working tree`. If that says DIRTY, the file records nothing.
3. **`SPEC.md`** — the specification and the complete decision log. §10 is the
   spine: §10.1 → §10.101, every finding, every refutation, every rule and why
   it exists. It is cumulative, so it contains its own history.
4. **`HANDOFF_rev42.md`**, then `HANDOFF_rev41.md`, backwards — what each
   revision actually did.
5. **`REF_MEASUREMENTS.md`** — measurements taken off the reference
   photographs, with their admissibility grades.

```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
/tmp/blender/4.5/python/bin/python3.11 -m pip install pillow scipy
```

## Verify first

```bash
./verify_clone.sh          # 66 checks, exit 0 or 1
```
Sixty-six content checks that replace what used to be thirty hand-typed `grep`
lines in the brief plus a prose guard table. **Identity is ancestry, not
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
T1_SUB=1 /tmp/blender/blender -b --python audit.py && git checkout STATE.md
T1_SUB=2 /tmp/blender/blender -b --python audit.py && git checkout STATE.md
```

`audit.py` rewrites `STATE.md` on every run — check it out again afterwards.

**Expected at rev 42: 0 fail / 0 warn on all four runs.** 131 objects,
190 meshes, 42 materials, 5 constant-roughness, **0 non-manifold edges**,
roof @ rear axle 1.9835 / 1.9833, cut roof hole 70069v / 254428v, rake
17.75 mm/m, L = 4.065 W = 1.750, arch gaps 39.7 / 40.7 mm, bay widths
0.516 / 0.515 / 0.516.

## The hero

```bash
python3 hero.py hero34f --res 4800x3200 --samples 56 --strips 20 --sub 2 --only N
python3 hero.py hero34f --res 4800x3200 --samples 56 --strips 20 --sub 2 --stitch-only
```

One strip per call, then stitch. `post.py` runs **once** on the stitched frame,
never per strip. Strip timings rise down the frame, **peak around strip 16, and
fall again** — 153 s at strip 1, 614 s at strip 16, 390 s at strip 19, because
the bottom strips are mostly ground. 18 measured strips came to 7631 s; budget
~2.3 h for the frame. Heroes are gitignored and are not in this repo.

## The probes

31 read-only instruments, `probe_*.py`. **Run the ones you inherit, not only
the ones you write** — and **read each probe's own summary line rather than
grepping for a pattern**, because the wordings differ and a summary grep
under-read six probes in rev 37 and again in rev 39.

Several are **deliberately left failing** and must not be "fixed":
`probe_clean_top` and `probe_dust_anchor` fail by design; `probe_psf_lines`
fails two controls, both expected; `probe_rev40_datum` C3, `probe_rev41_gate`
C4 and `probe_rev42_uv` C3 are all supposed to fail. `probe_rev36_barend`
prints *"REFUSING TO PRINT A RULING"* and that is correct. The expected tallies
are listed in `NEXT_CONTEXT_PROMPT_rev43.md` §3.

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
                                   brief NEXT_CONTEXT_PROMPT_rev43.md, .gitignore
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
  `out/p_side.png` and will raise `FileNotFoundError` until you render it —
  see §10 of the live brief for the one command that produces it.

## Open at rev 42, in the order the next revision should take them

1. **The door's art frame and the body's missing UV layout — one job.** Rev 42
   moved the cab door's bottom 272–388 mm but deliberately left `folk_gen`'s art
   frame at `DOOR_H = 1.013467`; separately, 55.97 % of painted surface
   self-overlaps because `T1_body` has no UV layout at all. **Both fixes are the
   same texture re-bake.** §10.100.6 and §10.101.
2. **Report 3** — the counter top's inner edge in `ref_rear34.jpg` at y 423,
   x 700, the one route that needs no parallax term. §10.99.6.
3. **Report 4** — the VW glyph's V and W fuse into an X. §10.94.
4. **Report 7** — "100% Calidad" off centre, `cal_gen.py:246`. §10.95.3.
5. **`V_POW`** locked at 0.60 against an implied 0.30–0.48. `t1_mats.py:149`
   and `t1_shell.py:1086`.
6. **`probe_clean_top` / `probe_dust_anchor`** — rewrite or retire, ten
   revisions open.
7. **`lidsign.png` is worn by no object; `tex/emblem.png` is referenced by
   nothing at all.**

The die-cut vinyl sticker for children at the restaurant — the **original**
deliverable — is still unbuilt, and the warm low-light "Playa" hero is
deprioritised but **not cancelled**: it carries the emotional bar that sits
above clinical accuracy.
