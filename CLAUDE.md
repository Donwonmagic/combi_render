# CLAUDE.md — how work is done here

This is a long-running project that recreates ONE specific vehicle photorealistically in
Blender. It is picked up mid-stream every revision. This file carries METHOD ONLY and is
never rewritten per revision.

**Nothing in this file is a measurement. If you find a number here, that is the bug —
delete it.** Every figure in this project lives in a script that runs, because a figure in a
paragraph goes stale silently. That is why `verify_clone.sh` exists.

## Authority, in order

The machine outranks the prose. The owner outranks the record. The record outranks nothing.
Where a brief and the machine disagree, **the machine is right — say so and correct the brief
in the same revision.**

## Before you touch anything

1. **MEASURE the merge state; never transcribe it.** The branch instruction in the prose has
   been stale SIX revisions running, most recently with the designated branch's remote copy
   DELETED while the work sat 39 ahead elsewhere. Run the ahead/behind loop and believe the output.
   `bootstrap.sh`'s row **9** -- "no branch carries work HEAD does not have" -- outranks any
   sentence, including this one. (It is row 9, NOT row 10. Row 10 is `verify_clone.sh`. The
   "row 10" in every brief through rev 51 is wrong and was propagated for three revisions.)
2. `./bootstrap.sh` and `./verify_clone.sh` must both end all-PASS on a **clean** tree.
   A failing row is a FINDING: report it with its actual value. Do not edit a script to make
   it pass. A re-base is allowed only with the cause named AND a companion row that makes the
   cause separately testable.
3. Read the highest-numbered `NEXT_CONTEXT_PROMPT_rev*.md` in full — find it with `ls`, do not
   trust a filename typed in any document, including this one.
4. Re-run `git diff --name-only HEAD...origin/main` EVERY session. Reference photographs arrive
   there mid-revision without warning.

## The rules that have each cost this project a revision

1. **RENDER IT, CROP IT, AND LOOK AT IT — before and after every change.** A trunk lid that
   opened inwards, a board's foot buried inside the roof, a bay lining built below its own
   aperture, a disc of body red at the centre of every tail lamp, hubcaps that render as
   five-petal flowers: all green through VERIFY, all found by looking at a crop.
2. **A green check is not evidence about the vehicle.** `verify_clone.sh` says so itself in its
   own verdict block. It tests that the RECORD is self-consistent. Never quote its total as
   fidelity.
3. **A control is finished when you have WATCHED IT FAIL on the defect** — not when it passes.
   A guard that crashes reports nothing. That is what the ablation switches are for.
4. **An instrument that has never been wrong has never been tested.** Every recent revision has
   caught four to seven of its OWN instruments being wrong, and every one produced a plausible
   number that would have been published. Budget for this; it is normal here.
5. **Never put a figure in an acceptance test unless you watched it print.**
6. **A guard that derives its threshold from the same expression it checks is a tautology.**
   Compare two independently obtained quantities.
7. **A guard written against a pose encodes that pose.** Ask the geometry — a foot is the lowest
   point — never the pose it happens to be in.
8. **YOU MUST NOT PUBLISH A NUMBER FROM A MASK OR WINDOW YOU HAVE NOT PAINTED AND LOOKED AT.**
   Painted BEFORE the number, not marked afterwards. This is the most-repeated defect in the
   project's history: in one revision alone, FIVE of NINE wrong instruments were a mask
   selecting the wrong pixels -- a "cab roof" window that was on the mural lid and the
   background, a "flank cream" window that included the bulb string, a "roundel" window on the
   V and W strokes, an "emblem" window on the rim ring, a "cap" window on the painted rim.
   Every one was caught by painting the selection and looking; NONE by reasoning about it.
   A measurement's window is part of the measurement.
9. **Read each probe's own summary line, never its exit code.**
10. **A claim in prose is not a guard. A claim in a source comment is not a measurement.
    Grepping for an object name is not a test that a feature is built** — lofted and swept
    features have no object name. Ask the mesh, or ask `STATE.md`.
11. **Check WHICH OBJECT and WHICH ARTWORK STATE.** Geometry transfers between the reference
    frames; paint and artwork do not. Several reference files are byte-identical duplicates of
    others — a duplicate is not corroboration. Before relying on any "the record requires X",
    check what object that sentence is about and check that the cited line still exists.
12. **Report the measurement WITH ITS CEILING.** Never a self-assigned score. Never "ready".
    Say what is fixed, what is still wrong, and what you measured. *"It cannot be recovered
    from what we hold"* is a real result and is worth more than a guess.
13. **Add the guard in the same edit as the change; retract in the same revision you find the
    error** — in SPEC, in the source, and to the owner.
14. **FINISH WHAT YOU DISPATCH.** Closing a revision with one agent outstanding has cost a whole
    revision twice, once on the measurement the top job was blocked on.
15. **Put an agent on the incoming brief whose only job is to refute it, and DO NOT CLOSE UNTIL
    IT REPORTS.**
16. **YOU MUST NOT DELETE A CARRIER.** A section headed "instructions still outstanding, in no
    other carrier" was dropped when a brief was rewritten; it took the project's original
    deliverable with it, undetected for five revisions and still open. An open-findings register
    went the same way one revision later. If a document is the only home of something, it is not
    yours to compact, prune or summarise. Carry it or hand it on by name.
17. **AUDIT THE BRIEF YOU WRITE, NOT ONLY THE ONE YOU RECEIVE.** Rule 15 puts an agent on the
    INCOMING brief. The outgoing one ships unread, and it becomes the next context's only map. Before
    closing: open every file it cites, grep every string it quotes, and RECOMPUTE every figure in it.
    The last audit of an outgoing brief found three defects in it, two of them TRANSCRIPTION rather
    than measurement, in a document whose own first section says not to transcribe. Record what the
    audit found IN the brief, so the next context knows it was tested and where it was weak.
18. **CITE STRINGS, NOT LINE NUMBERS.** Line numbers rot within the hour here — half the stale
    citations in this repository are that, including a cited line that turned out to be blank.
    Quote the code and let the reader grep.

## Facts about this machine that bite every session

- **YOU MUST NOT edit source while a render queue is running.** Freeze the tree for the duration,
  and make the runner report Blender's status, not the last command's — `rc=$?` after a redirect
  reports the redirect's.
- **Do not fan out Blender.** It is CPU-bound; two instances make both slower. Render
  sequentially from one script in the background and analyse in the foreground. Prefer fewer,
  deeper agents over many shallow ones.
- `lid_gen.py` is **not** called by `build.py`. Change it and regenerate by hand, or the render
  silently uses the old texture.
- `out/` is **not** tracked and starts empty on a clone. Render before quoting any probe that
  reads a frame.
- `audit.py` rewrites `STATE.md`. Commit first. Regenerate it before trusting any row that
  reads it.
- There are render-vs-photograph gates in this tree that nothing invokes. Run them.

## Asking the owner

One crop, one mark, one sentence, as MULTIPLE CHOICE, with the reference material attached, and
**ask it with the question tool** — a revision has been lost to sending the figures and
forgetting to ask. He has never stood in the vehicle: do not ask what the real one looks like,
ask what a PHOTOGRAPH shows. If he does not understand the question, the figure is the defect.

## Imports

@PASTE_INTO_CLAUDE_CODE.txt — the owner's standing orders and this revision's entry procedure.
@STATE.md — machine-written; outranks every prose description of the build.

**@HANDOFF_CARRIERS.md is the OTHER HALF OF THE BRIEF and it is NOT imported — read it when the
action brief points you at it.** The handoff was SPLIT at rev 70 because the brief had reached 95 KB
and the owner measured what that cost: geometry output per revision fell from 721 lines (rev 8–20) to
209 (rev 61–70), and findings closed at rev 66–70 were 0, 0, 0, 0, 0. Run `python3 revstats.py`.
**Rule 16 requires a carrier to be CARRIED, not to be carried in the WORKING document. Nothing was
deleted, `verify_clone.sh`'s carrier rows search BOTH files, and four companion rows make the split
itself testable. DO NOT RE-MERGE THEM.**

Read on demand, NOT imported: `SPEC.md`, `SURVEY_rev49_photoreal.md`, `REF_MEASUREMENTS.md`,
and the `LEDGER_*` / `HANDOFF_*` / `PHOTOS_WANTED_*` series. They are large; load the one the
task needs. The full numbered rule canon lives in the briefs, not here:
`grep -l "THE RULES. EVERY ONE WAS EARNED BY A DEFECT" *.md` and read the highest-numbered hit.
