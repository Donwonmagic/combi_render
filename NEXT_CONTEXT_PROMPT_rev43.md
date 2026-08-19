# NEXT CONTEXT PROMPT — rev 43
Please act as my expert. Continue the Señor Tacombi combi build. **Forty-two
revisions sit behind this.** You are picking up mid-stream, not starting.

**THE PROJECT IS ON GITHUB AND YOU ARE RUNNING ON HIS MACHINE.** Revisions 1–42
ran in an ephemeral Linux cloud sandbox with a file bridge to his Desktop. You
are Claude Code on his Mac, sitting in a real working copy. That changes Steps
0–2 completely and changes nothing at all about the model, the record, or the
standard. **Where this brief and the machine disagree, the machine is right —
say so and correct the brief in the same revision.**

**VERIFY BY CONTENT. THERE IS NOW A SCRIPT FOR IT:** `./verify_clone.sh`.
Sixty-six checks, exit 0 or exit 1. Until rev 43 those checks were thirty lines
of prose re-typed by hand every revision — which is a drift surface, and this
project has already shipped a measurement quoted from a thirty-revision-old
comment. **A number in a script that runs cannot go stale the way a number in a
paragraph can.** See §11.

---

## Step 0 — prove the tree you are sitting in is the right one
```bash
pwd && git remote -v            # expect .../Donwonmagic/combi_render
git fetch origin && git status -sb
./verify_clone.sh               # must print ALL 66 PASS and exit 0
```
**DO NOT RE-CLONE.** You are already in his working copy, and it holds things a
fresh clone does not: **every rendered hero and `out/` — those two are
gitignored and exist nowhere else.** (The marked question crops are NOT
gitignored: `.gitignore` excludes only `rev*_hero*.png`, and **17 marked crops
are tracked and committed.** Rev 43 must commit its own. `verify_clone.sh`
counts them.)

**IF `verify_clone.sh` EXITS 1, STOP.** Report the failing line and its ACTUAL
value and do not build. **A failing check is a finding, not a broken
instrument** — and do not edit the script to make it pass. That rule has been
earned four separate times in this project; §9.

**THERE IS NO BRIDGE AND NO STAGING STEP ANY MORE. HIS DISK IS YOUR DISK.**
`~/Desktop/tacombi_bus_render` is a real local folder. Renders and marked crops
go there with `cp`, and `open <path>` puts them on his screen. That is the whole
delivery mechanism now. **Every file is directly readable — no upload, no
transfer, no size cap.** This is a real gain; use it.

**AN ABSENCE HAS A TIMESTAMP TOO.** Rev 41 reported a delivery as never made
four minutes before it arrived. So report what `ls -l` actually returned and
when you ran it — never what you assume you wrote.

**WHAT IS IN THE WORKING TREE AND NOT IN THE REPO:** every rendered hero
(gitignored, ~15 MB each — `rev42_hero34f.png` should be current), `out/`, and
the old git bundles. **TAKE THE INVENTORY WITHOUT SWALLOWING THE ERRORS:**
```bash
ls -l out/ 2>&1 | head -5
ls -l rev4*_hero34f.png 2>&1
ls -ld ~/Desktop/tacombi_bus_render 2>&1
```
**No `2>/dev/null`.** A "No such file" line IS the finding, and this brief's own
rule is that an absence has a timestamp too. **Do not assume any of these three
exist** — report what came back. **The bundles are dead weight now that the repo
exists.**

## Step 0.5 — SEND ME A STATUS MESSAGE INSIDE TWENTY MINUTES, AND FIRE THE TWO ASKS
**DO THIS WHILE BLENDER IS STILL DOWNLOADING. DO NOT WAIT FOR THE GUARDS.**
Rev 42's brief had no instruction to contact me before the work was done, so my
first contact was whenever the session happened to surface. **The two things
item 1 is blocked on are human round-trips — they have the longest latency in
the revision and they must be fired first.**

Send exactly this shape. **No number you did not watch print. An absence is a
LINE in this report, not a gap in it.**
```
REV 43 - OPENING STATUS, <time of the last command you ran>

TREE     ./verify_clone.sh -> <paste the verdict line, do not paraphrase> exit <n>
         git HEAD <sha>  |  modified tracked files <n>
MACHINE  uname -m <v> | cores <n> | RAM <n> | free on . and /tmp <n>
         => Blender build I am installing: <x64|arm64>;  Cycles: <CPU-only|Metal>
ON DISK  out/            <the ls -l line, or the literal "No such file" line>
         rev4*_hero34f   <same>
         ~/Desktop/...   <same>
BRIEF vs MACHINE   <every place this brief disagrees with what I just ran, both
                    values. Write "none" only if there are none.>

BLOCKED ON YOU - item 1 cannot start without these:
  Q1. <one crop, one mark, the question as 2-3 lettered choices>
  Q2. folk_door.md - cited 20x in folk_gen.py, not in the repo. Can you send it?
      If not, say so and I will record in SPEC that the plan proceeds without
      the measurement its targets came from.

WHILE I WAIT, in this order, none of it blocked:
  0a <state> 0b <state> 0c <state> 0d <state>
NOT TOUCHING this revision: items <n, n, n>
```

### And launch the record fan-out NOW — it runs while the .dmg downloads
Rev 42's brief praised this and never commissioned one, so every session read
the record serially anyway, because inventing the questions IS the work. **Here
are the questions. Seven agents, disjoint files, all read-only, each returning
under 400 words.**

| agent | files | the question, verbatim |
|---|---|---|
| A1 | `HANDOFF_rev38..42.md` | Every item stated OPEN, CARRIED FORWARD or UNAPPLIED, with the revision that opened it and the last that touched it. **Flag any item whose stated age disagrees between two handoffs — quote both.** |
| A2 | `HANDOFF_rev30..37.md` | Every direct quotation of the owner, **verbatim**, with file and line. Mark each DECISION / QUESTION ANSWERED / STANDING INSTRUCTION / NOT YET ANSWERED. **Quote, do not summarise.** |
| A3 | `SPEC.md` §10.83–§10.101, **by anchor** | Every route recorded REFUTED, RETIRED, REFUSED, DISSOLVED, WITHDRAWN or CLOSED BY HIM. For each: the route, why it closed, and the instrument that must therefore NOT be re-tuned. **This is a do-not-touch list, not a summary.** |
| A4 | `folk_gen.py`, `t1_mats.py`, SPEC §10.10 + §10.100 + §10.101 | Locate `DOOR_H` **by symbol**: multiplier or divisor, how many call sites? Then state `folk_gen`'s mapping contract as it appears in source, and list every §10.10 target that must be re-measured if the flank UV map **replaces** rather than reproduces that affine map. **Cite symbols back to me, never line numbers.** |
| A5 | the 31 `probe_*.py` headers only | For each of the twelve with no published tally: its subject, whether its own docstring says a control is expected to fail, whether it needs `bpy`, and **whether its subject belongs to a route A3 reports as closed.** Answer from the file, not from this brief. |
| A6 | **this brief** + the repo | **Refute this document.** Every checkable claim in Steps 0–4 — counts, tallies, filenames, symbol locations, "N of M" figures — verified against the tree, PASS/FAIL with the actual value. **Start with the check count in Step 0.** |
| A7 | `analysis/`, `workflows/`, all `*.py` headers | `grep -rl '/home/claude'` across the whole repo. Count per directory and every distinct hard-coded absolute path. **macOS has no `/home`** — anything here is dead, not latent. (`workflows/tacombi-rev11-audit.js` hard-codes `/home/claude/work/tacombi` too, which item 0d walks into.) |

**A6 IS THE ONE THAT PAYS.** Rev 43's brief shipped saying the verify script
prints 49 checks when it prints 66 — stated three times, hit in minute one, and
found by an adversary agent rather than by the author. **Point one at this
document every revision.**

---

## Step 1 — the memory files are NOT reachable from here. Do not pretend to read them.
Revisions 14–42 kept a running record in a cloud assistant's memory store at
`/areas/tacombi-combi-3d-rev*.md`. **Those are not files on this laptop and no
tool here can open them.** Say so plainly rather than inventing their contents.

**EVERYTHING LOAD-BEARING IN THEM IS ALSO IN THE REPO, WITH PROVENANCE:**
`SPEC.md` §10 (cumulative, it contains its own history), `HANDOFF_rev42.md` back
to `HANDOFF_rev7.md`, `AUDIT_rev11.md`, `AUDIT_rev12.md`, and the superseded
`NEXT_CONTEXT_PROMPT_rev*.md`. Read those. **If you ever cite something that
exists only in memory, mark it unverified.**
**A RECORD ENTRY IS A CLAIM TOO — GREP IT.** Rev 37 found memory had invented
`MIGRATION_APPENDIX_rev32.md`, a file that has never existed; rev 39 through 42
re-checked and it still has not. `ls MIGRATION_APPENDIX_rev32.md` must fail.
**CHECK THIS PROMPT AGAINST MEMORY BEFORE TRUSTING ITS WORK LIST.**
**REV 40 REFUSED ITS BRIEF'S ITEM 1. REV 41 GRADED ITS ITEM 1 SOUND AND DID IT,
AND REFUSED ITS ITEM 3. REV 42 GRADED ITEMS 1 AND 7 SOUND, DID BOTH, AND
CORRECTED A WORDING ERROR IN ITS BRIEF.** Grade every item before you build it —
and notice that grading is not the same as refusing.
**I have never stood in the bus.** The "remember standing in the kombi" bar is
about the RESTAURANT'S owner. **Do not ask me what the real vehicle looks like.**
Ask me what a PHOTOGRAPH shows — that has paid off thirty-three times, twice in
rev 42 alone.
**AND ASK IT AS MULTIPLE CHOICE WITH THE REFERENCE MATERIAL ATTACHED. ONE CROP,
ONE MARK, ONE SENTENCE.** This is the highest-yield technique in the whole
project and it belongs here, at the front, not buried at the end: **that format
closed region 3 after twenty-one revisions and report 5 after five.** And **if I
do not understand the question, the FIGURE is the defect, not me.**

## Step 2 — Blender 4.5.3 on macOS, and BOTH guards before you propose anything
**THE REPO HARD-CODES `/tmp/blender`. DO NOT INSTALL BLENDER SOMEWHERE SENSIBLE
AND FIND OUT HOURS LATER.** Eight files bake that path in: `hero.py`,
`flank_compare.py` (twice), `probe_rev42_uv.py`, and the headers of
`probe_clean_top`, `probe_dust_anchor`, `probe_psf_lines`, `probe_psf_owner`,
`probe_psf_workshop`. Satisfy the layout instead of editing eight files —
editing them is a diff the guards do not cover and it churns every revision.

```bash
# ARCHITECTURE FIRST. This costs 40 ms and picks the right 320 MB download.
uname -m        # x86_64 -> macos-x64 below.  arm64 -> swap in macos-arm64.dmg,
                # and note Cycles then has METAL, so every timing in 5 is wrong
                # in your favour.  His desktop reported x64; CONFIRM, do not inherit.
# macOS ships a .dmg, NOT the linux tarball rev 42 used. Skip if 4.5.3 is installed.
curl -fsSL -o b.dmg https://download.blender.org/release/Blender4.5/blender-4.5.3-macos-x64.dmg
hdiutil attach -nobrowse -quiet b.dmg
cp -R "/Volumes/Blender/Blender.app" "$HOME/blender-4.5.3.app"
hdiutil detach -quiet /Volumes/Blender
xattr -dr com.apple.quarantine "$HOME/blender-4.5.3.app"   # else Gatekeeper kills -b

# reproduce the layout the repo expects
mkdir -p /tmp/blender
printf '#!/bin/sh\nexec "%s/Contents/MacOS/Blender" "$@"\n' "$HOME/blender-4.5.3.app" \
  > /tmp/blender/blender && chmod +x /tmp/blender/blender
ln -sfn "$HOME/blender-4.5.3.app/Contents/Resources/4.5" /tmp/blender/4.5
/tmp/blender/4.5/python/bin/python3.11 -m ensurepip
/tmp/blender/4.5/python/bin/python3.11 -m pip install pillow scipy
/tmp/blender/blender -b --version        # WATCH IT PRINT 4.5.3
```
**macOS empties `/tmp` on reboot.** Re-run the `mkdir`/`printf`/`ln` three lines
at the start of any session where `/tmp/blender/blender` is missing. One second,
and every hard-coded path stays valid.

That pip line is required. **BOTH GUARDS, BOTH LEVELS — `n` IS NOT A VALUE, IT IS 1 AND THEN 2.**
`build.py` does `int(os.environ.get("T1_SUB", "2"))`, so a literal `T1_SUB=n`
raises `ValueError` before anything builds:
```bash
for n in 1 2; do
  T1_SUB=$n T1_VERIFY=1 /tmp/blender/blender -b --python build.py
  T1_SUB=$n /tmp/blender/blender -b --python audit.py
  git checkout -- STATE.md    # NOT `&&` -- if audit.py exits non-zero the restore
done                          # would be skipped, leaving STATE.md rewritten and
                              # tripping verify_clone.sh into a false STOP
```
**All four runs, every revision. The cab-door booleans passed at SUB=1 and
collapsed the shell 205562v → 12v at SUB=2 for six revisions.**
Report the guards' ACTUAL output, both levels. **If a guard does not print
0 fail / 0 warn, that is the revision's first finding — report it before you
touch anything.** **`audit.py` rewrites `STATE.md` every run — `git checkout
STATE.md` after.**
**THE GUARDS ARE 0 fail / 0 WARN. GEOMETRY MOVED IN REV 42** — the cab door's
lower shut line. **131 objects, 190 meshes, every figure identical to rev 38's
EXCEPT the two roof-hole vertex counts, re-baselined at 70069 / 254428.**

## Step 3 — run the probes you inherit, not only the ones you write
**READ THIS BOX BEFORE YOU RUN ANYTHING. IT IS WHAT STEP 3 TRIPS.**
* **THE FRONT OVER-RIDER ASSEMBLY WAS WITHDRAWN BY HIM IN REV 37** (SPEC §10.93,
  §10.91.8). `build.py`'s two calls are **COMMENTED, NOT DELETED**, and
  `STATE.md` logs both guards as **`NOT APPLICABLE`** — *"Stated, not silently
  skipped."* **THAT IS NOT A GUARD FAILURE**, notwithstanding Step 2's "if a
  guard does not print 0 fail / 0 warn, report it". **FIVE PROBES EXIST ONLY TO
  MEASURE THAT DEAD SUBSYSTEM** — `probe_orb_hoop`, `probe_orb_post`,
  `probe_orb_blade`, `probe_v_apex`, `probe_psf_workshop` — and all five are in
  the twelve with no published tally. **Run them if you like; do not build a
  case to rebuild a bumper bar he killed.**
* **THE RETIRED ESTIMATOR ROUTES.** Cross-ratio retired on a precondition
  (SPEC §10.88.4), harmonic-conjugate retired on a missing feature (§10.89),
  §10.83's post question dissolved (§10.90.6). `rev33_barend 7/4`,
  `rev34_levels 8/4`, `rev34_ruling 6/4`, `rev35_harmonic 18/6` are the tallies
  of **closed routes**, not of instruments at 75 % health. **Do not "improve"
  them.**
* **`probe_v_apex`'s ANCHOR IS FALSE AND SPEC SAYS SO.** §10.85: the "two-tone V
  apex" is not the apex — it is the V's right arm vanishing behind the
  over-rider bar, and the anchor is **22.7 px off**. Anyone reaching for a
  centreline reaches for this first.
* **TWO BARRED DATUMS.** SPEC §10.11 — the ground-line datum carries a
  **common-mode error, do not place from it**. §10.15 — `ref_rear34.jpg` is
  mis-identified, **treat every number off it as suspect**, which includes item
  2b's `y 423, x 700`.

**31 now.** Under `blender -b --python`: `probe_ctan_index`, `probe_dust_scope`,
`probe_f90`, `probe_rev16`,
`probe_rev36_barend`, both rev38 probes, and `probe_rev42_uv`. (Rev 42's brief
also listed `probe_cross_anatomy` and `probe_shutlines` here; **`grep -c bpy`
on both returns 0** — they run under plain python. Harmless either way, but it
is a misclassification in the one paragraph whose whole job is classification.) Everything else
under `/tmp/blender/4.5/python/bin/python3.11`, including `probe_clean_top` and
`probe_dust_anchor` (their only `bpy` is in a comment) and `probe_rev39_flank`,
`probe_rev40_datum`, `probe_rev41_gate`. **Do not reach for the system
`python3` — macOS's has neither numpy nor Pillow.**
**READ EACH PROBE'S OWN SUMMARY LINE. DO NOT RE-DERIVE IT.** Wordings differ —
`probe_rev36_posts` prints `ALL 5 CONTROLS PASSED`, not `CONTROLS: n checked`.
**A SUMMARY GREP UNDER-READ SIX PROBES IN REV 37 AND AGAIN IN REV 39.**
**EVERY FAILURE IN THE LIST BELOW IS BY DESIGN. A TALLY THAT MATCHES THE LIST
MEANS THE PROBE IS HEALTHY; ONLY A TALLY THAT DIFFERS IS A FINDING.** **Seven
probes carry explicit KILL controls** — controls written to fail, because a
control that cannot fail proves nothing (`grep -ln 'KILL' probe_*.py`:
`orb_hoop`, `orb_xratio`, `rev33_barend`, `rev34_levels`, `rev34_ruling`,
`rev35_harmonic`, `rev42_uv`). **Others fail by design without saying so** —
which is the point of the tally below. `probe_orb_xratio` prints *"EXIT CODE 1 IS THE
INTENDED RESULT HERE"* in as many words. Under an owner whose standard is *any
single measurement off is unacceptable*, an unannotated `8/4` reads as four
regressions. **It is not. Read the expected tally first, then the probe.**
**`probe_rev40_datum` AND `probe_rev41_gate` DO NOT SAY SO THEMSELVES** — this
brief is their only carrier, and it is the one place §3's "read the probe's own
summary line" is not enough.

Expected: **`rev42_uv` 5/1 — C3 SUPPOSED TO FAIL**, **`rev41_gate` 5/1 — C4
SUPPOSED TO FAIL**, **`rev40_datum` 4/1 — C3 SUPPOSED TO FAIL**,
`rev39_flank` 3/0, `rev38_wheelbar` 6/0, `rev38_floorpen` 1/0, `rev36_posts`
5/0, `rev35_harmonic` 18/6, `rev34_levels` 8/4, `rev34_ruling` 6/4,
`rev33_barend` 7/4, `orb_xratio` 6/1, `rev32_pointer` 10/0, `dust_scope` 8/0,
`updust_pointer` 6/0, `psf_lines` 2 FAILED both EXPECTED, `clean_top` and
`dust_anchor` DELIBERATELY LEFT FAILING.
**`probe_rev36_barend` PRINTS "REFUSING TO PRINT A RULING"** — correct.
**`probe_rev39_flank` PRINTS "NOT flat, so the offset-versus-scale question is
NOT settled here"** — and note that phrase is split across two `print()` calls,
so a literal grep for it returns 0. `NO RULING` *is* a live branch in that file;
it fires when fewer than four bands answer. **Do not "fix" `rev36_barend`'s or
`rev39_flank`'s wording — the refusals ARE the finding.** `clean_top` and
`dust_anchor` are the different case: they fail on purpose and §6 item 6
disposes of them.
**TWELVE PROBES HAVE NO PUBLISHED TALLY.** Run them, record their output
verbatim into the handoff, and do NOT treat an unfamiliar line as a regression —
rev 44 needs the baseline you are about to create.
**`out/p_side.png` IS NEEDED BY EXACTLY THREE:** `probe_rev39_flank`,
`probe_rev40_datum`, `probe_rev41_gate` (and `flank_compare.py`). See §10.

## Step 4 — read, in this order — AND FAN THE BULK OF IT OUT
**THERE IS NO `docs/` DIRECTORY.** All 37 handoffs and every prompt are at the
repo ROOT; `verify_clone.sh` checks both facts. **Write yours there too.**

You are already inside this file, so: `STATE.md` → **`SPEC.md` §10.99–§10.101,
yourself** → `HANDOFF_rev42.md` → `HANDOFF_rev41.md` → … → `REF_MEASUREMENTS.md`
— **and Step 0.5's A1/A2/A3 are already reading most of that for you.**

**DO NOT READ 550 KB OF SPEC SERIALLY INTO THIS CONTEXT.** Fan it out: one
subagent per five handoffs, each with a named extraction question. That is §5's
single best use of parallelism and it is available to you from the first minute.
**SPEC's §10 IS NOT IN FILE ORDER.** §10.11–§10.33 come first, then §10.49–§10.75,
then — at roughly line 3936 — *"## 10. rev 7 — the canonical constants
(supersedes any value above)"*, then §10.1–§10.9 and §10.34–§10.48, then
§10.83–§10.101. **§10.9 and §10.10 are `##` headings, not `###`.** Read by
anchor, never by scrolling: `grep -n '^#\{2,4\} 10\.' SPEC.md` first, then jump.
`STATE.md` is machine-written; **if it and any prose disagree, it is right — BUT
CHECK ITS PROVENANCE ROWS FIRST**, including `working tree`. **If that says
DIRTY, the file is not a record of anything.** rev 39–42 all shipped it CLEAN.
**Check it anyway.**

---

# §5. THROUGHPUT — what actually parallelises here, and what does not

Use expanded workflows and parallel execution — but against the machine that
exists.

**MEASURE THIS MACHINE AND REPLACE THIS BLOCK BEFORE YOU SCHEDULE ANYTHING:**
```bash
uname -m && sysctl -n hw.ncpu hw.memsize && df -h . /tmp
```
**`uname -m` IS IN STEP 2 AND EVERY FIGURE BELOW DEPENDS ON ITS ANSWER.** On
**Apple Silicon** Cycles has Metal and this whole section is wrong in your
favour. **On arm64, do NOT `pip install` into a copied `.app`** — it invalidates
the notarised signature, which Intel tolerates and Apple Silicon does not.
Every timing below was measured on the **old 2-core cloud box** (Intel Xeon @
2.10 GHz, 7.8 GB, 28 GB free). His Mac is not that machine. Treat these as an
UPPER bound and a shape, not a prediction: **re-time SUB=1 and SUB=2 once, print
both, and budget off your own numbers.** Carry the new figures into rev 44's
brief — that is the single most useful thing you can leave behind about
throughput.
**Cycles on Intel macOS is CPU-only and a laptop throttles on a multi-hour
frame.** A strip that runs long late in a render is thermal, not a hang.

### What DOES parallelise — and the old "3 to 5 agents" cap is DEAD
**READ THIS BEFORE YOU PLAN THE REVISION.** Every parallelism rule in the
record was written against a **2-core** cloud box. **You are on his Mac, which
reports at least 8 cores, and you are Claude Code — you can orchestrate real
multi-agent work, not just spawn a helper or two.** Rev 11 deferred the biggest
job in the project purely because two cores could not run it. **That constraint
is gone. Do not inherit its conclusions.**

**THE ONE RULE THAT SURVIVES UNCHANGED: DO NOT FAN OUT BLENDER.** It is
CPU-bound and two concurrent instances make both slower. Everything else below
is now open to you.
Agent reasoning is API-bound, not CPU-bound, so several genuinely run at once
even on two cores. **This is where the throughput is.**
* **Reading and grepping the record.** `SPEC.md` is 550 KB and there are 37
  handoffs. Rev 42 put ten memory files through one subagent and got a
  structured extraction back while the main context ran the guards.
* **INDEPENDENT MEASUREMENT ROUTES.** The most valuable fan-out in this project:
  give N agents the SAME question with DIFFERENT photographs, or the same
  photograph with different estimators, and compare. §10.99 exists because one
  route was checked against a second that shared no step with it.
* **ADVERSARIAL VERIFICATION.** He has asked directly: *"Have you conducted
  truly adversarial audits?"* The pattern that works is N skeptics per finding,
  each instructed to REFUTE it, majority kills it. **Findings this project
  accepted without that have been overturned more often than not.**
* **Writing SPEC / HANDOFF / the next prompt** while a render holds the CPU.

### What does NOT parallelise — do not fan these out

    build SUB=1 (guard)      ~25 s
    build SUB=2 (guard)      ~104 s
    p_side preview           ~95 s
    probe_ctan_index         ~7 min   (renders)
    probe_rev42_uv           ~9 min   (rasterises every triangle nine times)
    hero, 20 strips          153 s at the top -> 614 s at strip 16 ->
                             390 s at the bottom; 18 measured strips
                             = 7631 s, whole frame ~2.3 h

**Run Blender work strictly one at a time** — it is CPU-bound and two instances
make both slower. That part is machine-independent.
**BUT THE OLD AGENT CEILING DOES NOT APPLY HERE.** Rev 11 launched a 25-agent
Workflow on the 2-core box and two hours later it had started 2 of 25. That was
a CPU artefact of that box, recorded once, in `HANDOFF_rev11.md`. Subagent
concurrency in Claude Code is a tool limit, not a core count. **Do not inherit
that ceiling — measure your own and write it down.**

### The scheduling pattern that won rev 42 back three hours
**THE HERO IS THE LONG POLE.** Start it as soon as nothing further will move
geometry **OR RE-BAKE A TEXTURE** — which means after §6 item 1 lands, not
before. A hero shot before the re-bake photographs the old artwork, and rev 25
already shipped a model wearing artwork fourteen revisions old. Then do every
text-shaped thing in its shadow:
```bash
# CONFIRM THE INTERPRETER FIRST. macOS system python3 has no numpy and no PIL,
# and a nohup'd loop that died on import looks exactly like a render running.
PY=/tmp/blender/4.5/python/bin/python3.11
$PY -c 'import numpy, PIL; print("ok")'
# REDIRECT EXPLICITLY. `nohup` only writes nohup.out when stdout is a TERMINAL;
# under a tool-driven shell stdout is a pipe and the render's output is LOST --
# which is exactly the silent death this check exists to catch.
caffeinate -is nohup bash -c 'for i in $(seq 0 19); do '"$PY"' hero.py hero34f \
  --res 4800x3200 --samples 56 --strips 20 --sub 2 --tag rev43_hero34f --only $i; done' \
  > hero_rev43.log 2>&1 &
sleep 60 && tail -20 hero_rev43.log     # CHECK IT WITHIN THE MINUTE
```
`caffeinate -is` stops the Mac sleeping mid-frame. **Then `--stitch-only`, then
`post.py` ONCE on the stitched frame.** Then write SPEC, the handoff and the next
prompt, and poll. Rev 42 wrote §10.100,
§10.101, its handoff and this prompt while 20 strips rendered. **Do not sit and
wait on a render.**

**CHECKPOINT LONG RENDERS.** The container-restart hazard is gone — nothing
restarts a laptop mid-session — but the session is not immortal: a closed lid, a
killed CLI, a compacted context all lose in-flight work. Rev 42's hero died at
strip 10 of 20 and resumed from 10 **only because `hero.py` writes each strip as
its own file. Never hold three hours of work in a process's memory.** After any
interruption, `hero.py`'s own seam report is what proves the two halves are
consistent; rev 42's read **z = 1.95 against a threshold of 4**.
**`hero.py`'s OWN DOCSTRING IS STALE ON THIS POINT** — it says "the sandbox reaps
background processes (nohup/setsid/disown all fail)". That was rev 9's sandbox.
It works here. Do not "fix" the strip-splitting on the grounds that its stated
rationale no longer holds; the real rationale is seams and the denoiser.

### The one big fan-out he has actually asked for and that has never run
**`workflows/tacombi-rev11-audit.js`** — ten specialist dimensions, an
adversarial verifier per ranked finding instructed to REFUTE, then a synthesis.
He asked for *"a complete and comprehensive workflow by a number of expert
specialists"* and later: *"I think that we should conduct that audit workflow at
some point, I believe you were one that put it on ice."* Rev 11 deferred it for
the 2-core reason above and it has never run.
**RUN IT. THIS REVISION. IT IS THE REASON THE MACHINE CHANGED.**
He asked for *"a complete and comprehensive workflow by a number of expert
specialists"* and then, later, *"I think that we should conduct that audit
workflow at some point, I believe you were one that put it on ice."* **I was.
The reason was two cores** — the file's own header says so, and says the quiet
part too: ***"On a wider box it is a normal fan-out."*** **You are the wider
box. Thirty-two revisions of deferral end here.**

**DO NOT try to execute the file** — `Workflow({scriptPath: …})` is a runner
that does not exist here, and the file hard-codes `/home/claude/work/tacombi`.
**Read it as the SPECIFICATION it is** — it already contains the ten dimension
briefs, the JSON schemas for findings and verdicts, the refuter's instructions
and the synthesis prompt — **and drive the same shape with your own subagents.**

**THE HARNESS, concretely:**
```
STAGE 1  FAN OUT — the five unrun dimensions, concurrently, disjoint files:
         counter/galley internal contrast · wheels and contact shadow ·
         tail · roof · optics/glass
         (proportion, materials, script and fascia were run BY HAND in rev 11
         and AUDIT_rev11.md carries their results. DO NOT REDO THEM. The tenth
         key, `playa`, he deprioritised — replace it with WEATHERING, which the
         file's own header says is now the dominant CG tell.)

STAGE 2  ADVERSARIAL VERIFY — do NOT wait for all five. The moment a dimension
         returns, fan its ranked findings straight into refuters. Each refuter
         is told to REFUTE, not confirm, and to DEFAULT TO REFUTED if it cannot
         independently reproduce the finding. Give them DIFFERENT LENSES rather
         than N identical skeptics: does it reproduce · is the datum admissible
         under SPEC 10.62/10.73 · what does it BREAK if applied. Majority
         refutes -> the finding dies.

STAGE 3  SYNTHESIS — one agent, the owner-facing review. CONFIRMED findings
         ranked; REFUTED findings listed WITH THE REASON, because an
         unrecorded refutation gets re-raised next revision. Write
         AUDIT_rev43.md.
```
**PIPELINE IT, DO NOT BARRIER IT.** A barrier between stage 1 and stage 2 makes
the fastest dimension wait on the slowest for nothing — no verifier needs
another dimension's findings. Let each dimension flow through verify on its own.

**FIRST, UPDATE THE BRIEFS — the file's own header lists exactly what moved and
it is four items:** drop/replace `playa`; the `roof` brief still poses the lid
topology as unresolved (it is resolved, SPEC §10.26 — re-point it at whether the
front lid sits forward of `LID_X0`); the `counter` brief predates the rev-11
galley rebuild (point it at INTERNAL CONTRAST, bay 1 sd 15.3 against the
photograph's 28.4); add the roof cutter (SPEC §10.27) to `proportion` or `roof`.
**They were written against rev 10 and the model has moved 32 revisions.**
**FOUR OF THE TEN DIMENSIONS HAVE ALREADY BEEN RUN BY HAND** — proportion,
`materials` (which `AUDIT_rev11.md` calls "weathering"), script, fascia — and
that file carries their results. Five remain: counter/galley internal contrast,
wheels and contact shadow, tail, roof, optics/glass. **Do not redo the four.**
**FOUR PLUS FIVE IS NINE. THE TENTH KEY IN THE FILE IS `playa`** — and
`AUDIT_rev11.md` drops it silently. It is the warm low-light hero of §7.4,
deprioritised but **not cancelled**. Account for it rather than inheriting the
arithmetic gap.
**Its dimension briefs were written against rev 10 and MUST be updated to rev 42
before it runs** — the file's own header says so.

### The orchestration patterns worth reaching for, now that you can
Not a menu to work through — pick what fits, and compose.
* **ADVERSARIAL VERIFY.** N skeptics per finding, each told to REFUTE, majority
  kills. **Findings this project accepted without that have been overturned
  more often than not** — that is not a slogan, it is the record.
* **PERSPECTIVE-DIVERSE VERIFY.** When a finding can fail in more than one way,
  give each verifier a distinct lens instead of cloning one skeptic. Here the
  natural lenses are: does it reproduce · is the datum admissible · what does
  it break.
* **INDEPENDENT MEASUREMENT ROUTES.** The single most valuable fan-out in this
  project: the SAME question to N agents with DIFFERENT photographs, or the same
  photograph with different estimators, then compare. **SPEC §10.99 exists
  because one route was checked against a second that shared no step with it.**
* **LOOP-UNTIL-DRY.** For unknown-size discovery, keep spawning finders until
  two consecutive rounds return nothing new. Dedup against everything SEEN, not
  against what survived — or judge-rejected findings reappear every round.
* **COMPLETENESS CRITIC.** A final agent asking *what is missing — which route
  was not run, which claim is unverified, which source unread?* What it finds is
  the next round's work.
* **A6, EVERY REVISION.** One agent pointed at the brief itself, told to refute
  it. **Rev 43's brief shipped claiming its own verify script prints 49 checks
  when it prints 66** — stated three times, hit in minute one, and caught by an
  adversary rather than by its author.

### What throughput does NOT mean
Not more findings per hour. **This project's failure mode has never been too
little output; it has been confident output that a control later killed.** Rev 42
alone had two estimators killed by their own controls, a line that turned out to
be its own annotation, a cache key that printed 571 %, and a crown figure quoted
from a stale comment. Every one was caught by a check costing minutes.
**Spend the parallelism on checking, not on producing.**

---

# §6. ORDERED WORK LIST FOR REV 43
**ITEMS 1 AND 2 ARE THE REVISION. EVERYTHING BELOW 2 IS OPPORTUNISTIC.** Rev 40
closed one item, rev 41 one, rev 42 two. Nine is not a plan, it is a menu.
**If you get one thing done, make it item 1 — and if you cannot finish the
re-bake, DO NOT START IT.** Half a re-bake is the worst state this project can
be in: textures moved, the md5 tripwire fired, and no SPEC §10.10 report to show
for it. Say which items you did not touch, by number.

**ITEM 1 IS BLOCKED ON ME AND YOU SHOULD EXPECT THAT FROM THE START.** It needs
two things only I can give: the answer to *did the door get deeper under the
art, or does the art scale with it* (one crop, one mark, one sentence), and
`folk_door.md`, which is not in the repo. **ASK FOR BOTH IN YOUR FIRST MESSAGE
TO ME — do not do a revision's work and then discover you needed them.**

**WHAT TO DO WHILE YOU WAIT ON ME — in this order, none of it blocked:**
0a. Rebuild the instrument floor: Blender, both guards at **both** levels,
    `out/p_side.png`, then all 31 probes against §3's tally.
0b. **Item 8b, `SCR`** — measured, checked, condition met, unapplied for three
    revisions. Small, self-contained, and it moves geometry.
0c. **Item 2's scale-free headlamp test.** SPEC §10.94 already gives it: does
    the indicator aperture sit below or above the two-tone break in the current
    build? It needs no px/m and no answer from me.
0d. **RUN THE SPECIALIST AUDIT HE ASKED FOR THIRTY-TWO REVISIONS AGO.** Update
    `workflows/tacombi-rev11-audit.js`'s four stale dimension briefs, then drive
    its harness with your own subagents — five dimensions, adversarial refuters
    pipelined behind each, one synthesis into `AUDIT_rev43.md`. **§5 has the
    stage-by-stage shape.** It is unblocked, it needs no answer from me, it is
    the single largest thing this project has deferred, and **it was deferred
    for a hardware reason that no longer exists.** If you do one thing beyond
    the instrument floor while you wait on me, do this.
**None of that touches the re-bake, and all of it is work rev 44 would otherwise
inherit.**
**HIS EIGHT DEFECT REPORTS ARE THE SPINE. THREE ARE CLOSED — 6 and 8 in rev 38,
5 in rev 42. DO NOT RE-OPEN ANY. REPORT 3 IS *NOT* CLOSED AND *NOT* SOLVED** —
it is where rev 38 left it, as SPEC §10.24.

1. **THE ART FRAME AND THE BODY'S MISSING UV LAYOUT — ONE JOB, AND THEY MUST BE
   DONE TOGETHER.** The largest piece of work left, and it needs a written plan
   before a line of code.
   * **BOTH FIXES ARE THE SAME RE-BAKE. Doing either alone burns the bake
     twice.** This is rev 25's one-lever rule's stated exception, not a breach
     of it: **the lever IS the bake.** A re-bake is a deliberate act under
     SPEC §10.10 and must report against §10.10's own targets — rev 25 did
     exactly that and its numbers are the template.
   * **"RE-BAKE" HERE DOES NOT MEAN A BLENDER BAKE.** There is no
     `bpy.ops.object.bake` anywhere in this repo and never has been. It means
     re-running `folk_gen.py` under plain python3 (`main()`, needs
     pillow and numpy; **scipy is optional** — it is imported in a `try`, and
     without it only the colour-bleed pass is skipped) — it deliberately never imports `bpy`, it parses
     `t1_shell.py` and `t1_core.py` as source. Also `lid_gen.py`, `cal_gen.py`,
     `texgen.py`.
   * Rev 42 moved the cab door's bottom **272 mm at the rear corner and 388 mm
     at the front corner** (§10.100) and DELIBERATELY left `folk_gen`'s art
     frame at rev 41's `DOOR_H = 1.013467`. **The door is now ~390 mm deeper
     than its art frame AT THE FRONT LOWER CORNER** — 272 mm at the rear. It is
     not one number.
   * **`DOOR_H` SCALES THE DOOR ART VERTICALLY — IT IS A MULTIPLIER, `h = sv *
     DOOR_H`, TWICE IN `folk_gen.py`.** (SPEC §10.100.6 calls it a *divisor*;
     `grep -n 'DOOR_H' folk_gen.py` shows otherwise, and there is no `/ DOOR_H`
     anywhere. The consequence is the same, the mechanism is not — **check the
     code, not the sentence.**) Re-pointing it at the wrapped outline takes it
     1.013 → ~1.40 m and **stretches the art ~38 % vertically.** The art was measured on the door as photographed swung open
     49°. **Nothing says the art extends into the new 390 mm.** *"Did the door
     get deeper UNDER the art, or does the art scale WITH it?"* is a question
     for HIM — one crop, one mark, one sentence — not a coding decision.
   * The second half of the same job: `probe_rev42_uv` measured **55.97 % of
     painted surface self-overlapping** (§10.101). **The body has no UV layout
     at all.** Every hand-made UV layout is 0.00 %.
   * **ONE JOB, TWO MECHANISMS — AND CONFUSING THEM IS THE TRAP.** SPEC
     §10.101.7 is explicit that they *"should be done together, and neither
     should be done alone"* — that is the schedule, and it is why this is item
     1. But they are not the same *edit*, and assuming they are is how the plan
     goes wrong. The
     overlap is not in the artwork — it is `t1_mats.py`'s `swirl`/`swirl_b`
     driven `projection='BOX'` off `TexCoord.Object`. **Re-running `folk_gen`
     changes 0 % of it.** Fixing it means giving `T1_body` a real UV layout and
     rewriting `body_paint` — **and that replaces `folk_gen`'s MAPPING CONTRACT**
     (`u = U0 + SGN·0.26·x`, `v = 0.263 + 0.26·z`) against which all 2455 lines
     of measured composition are authored. **THE PLAN'S FIRST DECISION IS
     WHETHER THE NEW UV LAYOUT REPRODUCES THAT AFFINE MAP ON THE FLANK — so
     `folk_gen` survives — OR REPLACES IT, so `folk_gen` is re-authored and
     every §10.10 target re-measured.** Decide that before anything else.
   * **`folk_door.md` IS NOT IN THE CLONE.** It is cited 20 times in
     `folk_gen.py` at `/home/claude/work/measure/folk_door.md`, and it is the
     source of every door-art number. 0 hits in `SPEC.md` and
     `REF_MEASUREMENTS.md`. **Ask him for it before planning the bake, or state
     explicitly that the plan proceeds without the measurement its targets came
     from.**
   * **TWO RECIPES ARE ALREADY WRITTEN IN `folk_gen.py`'s TRAILING NOTES — DO
     NOT RE-DERIVE THEM.** `grep -nE '0\.2280|\(f\) THE NOSE FRONT FACE' folk_gen.py`
     (**`-E`, not `\|`** — BSD grep takes `\|` literally and finds nothing,
     which reads exactly like the recipes not existing).
     One removes the texture-wrap collision (`Scale 0.2600 → 0.2280`, `Location
     x 0.185 → 0.500`; period becomes 4.386 m, longer than the 4.01 m flank, so
     no two points on the body share a texel). **It cites `t1_mats.py:823` and
     `:815` — LINE NUMBERS, so re-locate by symbol before trusting them.** The
     other, note (f), documents the nose/door shared-window collision and proves
     no tile change can fix it: *"one image cannot hold two different drawings
     for one (u, v)"* — which is the argument for the UV layout, already made.
   * **The eight texture md5s in `verify_clone.sh` are the tripwire**, and this
     item is what moves them. §11 has the procedure; follow it exactly.
2. **REPORT 3 IS THE HEADLAMPS AND THE PAINT BREAK — SPEC §10.24 item 3.**
   97 mm at ~3.9σ, open since rev 10. It is a report about a RELATIONSHIP:
   §10.94 records his words as *the paint and the headlamps are not aligned
   **with each other***.
   * **THE SCALE-FREE ROUTE ALREADY EXISTS AND HAS NEVER BEEN APPLIED.** SPEC
     §10.94 records that in the photograph the indicator aperture lies **BELOW**
     the two-tone break, and in the build it lies **ABOVE** it. That is an
     ORDINAL fact — no px/m, no camera model, admissible where a metric is
     barred. **It is the same class of fact that broke Report 5 open after five
     revisions.** Confirm it still holds on the current build, then move.
   * **TWO TRAPS, both §10.94's. DO NOT MOVE THE ROUNDEL WITH THE LAMPS** — its
     height is supported by both chains independently. And **§10.24's three
     findings were applied together once and reverted together once: they are
     NOT one change.**
2b. *(separate, and lower — do not let it displace 2)* The counter top's **INNER
   edge** in `ref_rear34.jpg` at y 423, x 700 lies ON the flank plane and needs
   no parallax term. **This is rev 41's work-list ITEM 3, not his REPORT 3** —
   SPEC §10.99.6 is titled *"ITEM 3 IS REFUSED"* and the two have been conflated
   before. It re-opens the **fascia depth only**, which §10.99.6 already reports
   as consistent with zero everywhere in the documented band (−2.1 to −2.8 mm,
   sign-flipping across the parallax bracket). **DO NOT re-derive the fascia off
   the flank ruler — that is exactly what rev 41 refused.**
3. **REPORT 4 — THE VW GLYPH.** §10.25's premise is FALSE: SPEC's own later
   entry records *"no gap but a 52 mm interpenetration"*. The V and W fuse into
   an X, and `rev42_hero34f.png` photographs it plainly. §10.94.
4. **REPORT 7 — "100% CALIDAD" OFF CENTRE.** `cal_gen.py:246` places it at an
   absolute **0.180 of texture width**, re-verified at that line in rev 42.
   **DETERMINE TEXTURE-VERSUS-PANEL BEFORE TOUCHING EITHER** (§10.20's family).
   **DISTINCT from his sticker LEGIBILITY complaint — do not merge them.**
   `calidad.png` is 2400×1771, below **SPEC §5**'s 3K floor, UV layout clean at 0.00 %.
5. **REPORTS 1 & 5 — `V_POW`.** Locked at 0.60. **FIND IT BY SYMBOL, NOT BY
   LINE:** `grep -n '^V_POW' t1_mats.py t1_shell.py`. Three separate documents
   have cited its line number and all three are now wrong — SPEC §10.94 says
   `:1070`, `HANDOFF_rev42.md` says `:1086`, and by rev 42 the symbol had moved
   to `:1217` while line 1086 went blank. **That is §9's rule biting the very
   document that states it.** The rev-11 audit implies **0.30–0.48**.
   **MIRROR ANY CHANGE INTO `t1_shell.zV`** or the pressed swage and the painted
   break de-register. Report 5's geometry half is closed; report 1, the nose
   shape, is not.
6. **`probe_clean_top.py` and `probe_dust_anchor.py` — REWRITE OR RETIRE.**
   **TEN revisions open** (rev 42's handoff says TEN; the count has been drifting
   upward un-anchored, so anchor it: `grep -n 'revisions' HANDOFF_rev42.md`).
   **THE QUESTION TO DECIDE FIRST, stated plainly because ten revisions have
   stalled on it being implicit: if these two retire, WHAT INSTRUMENT COVERS THE
   CLAIM THEY WERE STANDING IN FOR?** Name its replacement before deleting
   either. **Do not widen a tolerance.**
7. **ONE ORPHAN, NOT TWO — AND THE OTHER IS A TRAP THAT HAS ALREADY CAUGHT ONE
   REVISION.** `tex/emblem.png` is genuinely unreferenced: `texgen.py` writes
   it, only `audit.py`'s provenance list reads it. Dispose of that one.
   * **`lidsign.png` IS NOT AN ORPHAN. DO NOT DELETE THE TEXTURE, THE MATERIAL
     OR THE FUNCTION.** `build.py` binds it — `A(sign_boards[0], "lidsign")`.
     It is worn by no object because `t1_shell.signboard()` is gated behind
     `T1_SIGNBOARD=1`, and **that gate is HIS decision, not a defect:** he
     retired the panel from the vehicle — *"I was wrong, I think it is a
     detached sign"*, *"it is not part of this vehicle"*. The geometry is kept
     rather than deleted because **he has changed his reading of this one panel
     three times**, and **no hero may be rendered with it on.**
   * **`t1_shell.py` ALREADY CARRIES A LITERAL "NOTE FOR ANY LATER CONTEXT"**
     recording that `NEXT_CONTEXT_PROMPT_rev38.md` §6 item 1 sent a revision at
     this same function by mistake. **and rev 43's brief nearly did it again.** Anything that looks unused
     around `signboard` / `lidsign` / `sign_strut` is that decision.
8. **`analysis/` HARD-CODES `/home/claude/tacombi/ref_side.jpg` IN 25 OF ITS 27
   SCRIPTS** — not three, which is what rev 42's record said.
   Check it yourself: `grep -rl '/home/claude' analysis/ |
   wc -l`. **There is no `/home` on macOS at all**, so this is now a permanently
   dead directory rather than a latent one. They are rev 4–11 one-offs called by
   nothing in the build or the guards. **Decide once:** repoint them at
   `os.path.dirname(__file__)`, or move them to `analysis/attic/` with a README.
   Do not leave a directory that cannot run and do not edit 25 files blind.
8b. **`SCR` IS MEASURED, CHECKED, AND UNAPPLIED FOR THREE REVISIONS.** `build.py`,
   `SCR = dict(...)`. **+76.2 mm forward, −33.3 mm up** (SPEC §10.98 — the
   vertical term flipped sign when the datum was fixed; the +76.2 never depended
   on it). Rev 41's condition was *"re-measure once more after any counter
   change, then apply"* — **the counter has not moved since, so the condition is
   met.** This is the panel half of §7.7's argument that the failure is the
   PANEL and not the render. It moves geometry, so it owes a hero.
9. **A HERO, after anything that moves geometry.** Camera absolutely last.

**SHOOT THE HERO AT THE END, AND SHOOT IT EVERY REVISION THAT MOVES GEOMETRY.
AND RE-RUN THE PROBES TOO.**

---

## §7. INSTRUCTIONS OF MINE STILL OUTSTANDING, IN NO OTHER CARRIER
Grep each before acting — a memory entry is a claim.
1. ~~**DRIVE FIXES OFF THE BROADSIDE RENDER OVER `ref_side.jpg`**~~ — **DONE
   rev 39, DATUM CORRECTED rev 40, GATE ADJUDICATED rev 41.**
   `probe_rev39_flank.py` is a standing instrument. **RE-RUN IT EVERY REVISION
   THAT MOVES THE FLANK — but read §10.99 first: its Z-LADDER has no power and
   only its JOINT registration may be quoted.** It still reads (−1, −4) px after
   rev 42 moved the flank.
2. **"REMEMBER TO HOLD UP NEXT TO THE ACTUAL SOURCE PHOTOS."** A standing check.
   Done for the show flank (rev 39/40/41) and the cab door (rev 42).
   **Still never done for the NOSE, the TAIL or the ROOF.**
3. **THE DIE-CUT VINYL STICKER IS THE ORIGINAL DELIVERABLE AND IS UNBUILT.**
   For children at the restaurant; should spark joy and be something families
   keep. **Style LOCKED by me: cartoon with rendered depth.** **Scene LOCKED by
   me: nothing but the bus, die-cut tight, plus the sun and the papel picado.**
   On the papel-picado conflict: **"Leave it open, I'll decide when the sticker
   is actually being built."** **DO NOT RE-PUT IT UNTIL THEN.** I like how the
   wheels were drawn in the earlier cartoon version.
4. **THE PLAYA HERO IS DEPRIORITISED, NOT CANCELLED** — *"let's not do playa
   right now. Lets focus on the 3d model"*. The agreed deliverable is the
   white-studio hero for fidelity **PLUS** a warm low-light Playa hero, and
   **the Playa one carries the emotional bar that sits ABOVE clinical
   accuracy.**
5. ~~**NINE FLOWER HEADS**~~ — **CLOSED IN REV 39. I ANSWERED TEN.** §10.97.11.
6. **ABSOLUTE REPLICATION OF ALL ARTWORK** — mural board, flank paisley, the
   script, the Calidad decal, the menu strips and cards, the rear-lid lettering,
   the plate surround. A hard bar. Rev 10 recorded the lettered panel reads
   *"La S——— and no further"* and that **"La Santa" is a RECONSTRUCTION**.
7. **THE SEÑOR TACOMBI SCRIPT — I REJECTED IT TWICE.** `flank_compare` puts
   `Senor` at **0.459 of its own ceiling**; its texture-only control scores
   **0.884 overall** — so **the failure is the PANEL and the `Senor`
   reconstruction, not the render.** **THE "SILVER IS FLAT" CLAIM IS FALSE AND
   REV 43 MEASURED IT.** `tex/senor.png` does NOT emit a constant: **0 pixels**
   hold (214,216,218), it carries **5856 unique opaque colours**, per-channel
   std **24.1 / 40.2 / 47.7**. The (214,216,218) figure was quoted from a
   comment in `script_gen.py` whose own sentence is **past tense** — *"rev 10.
   The generator emitted a CONSTANT…"* — describing behaviour that same comment
   then documents as fixed. **§9's rule, biting the brief again: a figure in a
   comment is not a measurement.** There does appear to be a live defect, but it
   is **VALUE, not flatness**: opaque mean **(205, 194, 200)** against
   `script_gen`'s own measured target of **(127.4, 124.9, 130.0)**. Re-state the
   item that way before acting on it. Rev 42 measured `senor.png` at 4096×1738,
   **the only image meeting SPEC §5's 3K bar**, UV layout **clean at 0.00 %** —
   so neither resolution nor layout is the problem.
8. **THE FRONT ROOF LID NEEDS TWO-SIDED ARTWORK** — my settled topology, never
   implemented. `roof_lids()` gives each lid ONE board face. Also mine: **a
   TRUNK LID, separate from the roof lids, and region C is that trunk lid,
   OPEN.** `grep -c trunk t1_shell.py build.py` is **0 and 0**.
9. **"CLUTTER ON THE COUNTER"** — raised more than once, never recorded as
   closed, and rev 11 then dressed the galley with 51 objects.
10. **I STATED THE BUS SITS NOTICEABLY LOWER THAN STOCK.** **NO REVISION HAS
    MEASURED THIS AND NONE MUST BE READ AS HAVING DONE SO** — every flank number
    is relative to the counter fascia or the break by construction and says
    nothing about ride height. Still unadjudicated.
11. **NOLITA IS RE-ADMITTED FOR GEOMETRY ONLY** (rev 15, §10.32).
    `grep -ic nolita`: **9 in SPEC, 0 in REF_MEASUREMENTS.** Twenty-eight
    revisions, **no Nolita frame ever measured. AN AUTHORISED SOURCE CLASS IS
    SITTING UNUSED.** Every Nolita-derived number must be TAGGED.
12. ~~**THE GITHUB MIGRATION**~~ — **EXECUTED IN REV 42, BY HIM.** The repo is
    `https://github.com/Donwonmagic/combi_render`, 227 commits with full
    history. ~~Running Claude Code locally~~ — **DECIDED. THIS SESSION IS
    IT. Do not re-put it.** Open in its place: **re-measure §5 on this machine
    and carry the numbers into rev 44's brief** — every scheduling rule in §5
    was a 2-core artefact.
13. ~~**REGION 3**~~ — **CLOSED BY ME IN REV 40: THE PALE BAND IS THE COUNTER'S
    FRONT FACE.** §10.98.11. **DO NOT RE-PUT IT.**
14. **THE STANDARD, IN MY WORDS:** *"we are recreating a photo realistic version
    of that exact bus"* and *"any single measurement off is unacceptable"*.
    Also 4K non-overlapping textures and no floating artifacts — **MEASURED AT
    LAST IN REV 42, §10.101: one image of seven meets **SPEC §5**'s own 3K floor and
    55.97 % of painted surface self-overlaps. The measurement exists; the repair
    does not.**

## §8. ALREADY SETTLED — do not re-open without new evidence AND a different method
**REPORT 6 CLOSED** (`cab_floor`; four wheel houses; `FLOOR_W = 1.200`).
**REPORT 8 CLOSED** (second `lid_strut`). §10.96.
**REPORT 5 CLOSED FOR ITS GEOMETRY** (rev 42, §10.100) — the cab door wraps the
front wheel arch, on HIS two readings of `ref_workshop.jpg`. **Its ART FRAME is
NOT closed and is §6 item 1.**
**THE FRONT OVER-RIDER ASSEMBLY IS WITHDRAWN — BAR AND POSTS.** His decision,
rev 37. **DO NOT RE-PROPOSE IT** without a square-on frame of the front or his
say-so. `build.py`'s two calls are COMMENTED, NOT DELETED; the guards stay armed
and log NOT APPLICABLE.
**THE MURAL BOARD'S TEN FLOWER HEADS ARE SETTLED BY HIM** (rev 39).
**REGION 3 IS SETTLED BY HIM** (rev 40) — the counter's front face.
**THE TYRE DIAMETER IS RIGHT** — 651 ± 13 mm against the locked 665 (rev 39).
**THE MODEL'S BREAK-TO-SILL IS RIGHT TO 2.7 mm** (rev 40).
**THE COUNTER SLAB IS RIGHT TO 0.0 mm** (rev 41). **Do not move `CNT_ZT`,
`CNT_ZB` or `CNT_NOSE_F` off a flank-plane reading.**
**THE Z-LADDER IN `probe_rev39_flank.py` HAS NO POWER** (§10.99). **Do not
re-tune its gate. Do not quote its bands.**
**THE DOOR OUTLINE'S ARCH CLEARANCE IS ARMED AT REV 41's OWN VALUE**
(§10.100.5). **Do not re-arm it at a number chosen later.**

## §9. HARD-WON RULES — every one was learned by breaking it
Every rule in the rev-42 prompt still stands. **NEW in rev 42:**
* **AN ORDINAL FACT NEEDS NO RULER, AND THAT IS WHAT MAKES IT ADMISSIBLE WHERE A
  METRIC IS BARRED.** Report 5 sat unbuildable for five revisions because §10.62
  bars a px/m on the door plane. What broke it was noticing the door's shut line
  runs BELOW the arch crown and the build put it ABOVE. **A sign has no units.**
* **A LINE YOU DREW IS NOT EVIDENCE.** Rev 42's first marked figure produced a
  "door bottom" that, contrast-stretched with no overlay, does not exist.
  **Check the UNMARKED frame before the marked one goes anywhere.**
* **A GUARD FIRING ON YOUR OWN CHANGE IS THE GUARD WORKING.** Fix the
  construction, never the bar.
* **WHEN SMOOTHING MOVES A CURVE, SOLVE FOR THE INPUT** — a fixed point, not a
  hand-tuned offset, so it re-solves itself when the resample count changes.
* **ARM A NEW GUARD AT THE OLD BUILD'S OWN MEASURED VALUE**, so new geometry can
  satisfy it only by being no worse than what shipped.
* **A REQUIREMENT NOBODY HAS INSTRUMENTED IS NOT A REQUIREMENT.** §5's
  "non-overlapping" sat in SPEC for thirty-nine revisions with no probe.
* **SWEEP THE PARAMETER YOU ADDED YOURSELF.** `C_FOOT` was mine; it moves the
  answer 8 pp.
* **POOLING TWO OBJECTS THAT SHARE A DECAL MANUFACTURES A DEFECT.** `senor.png`
  reads 100 % pooled and 0.00 % per object.
* **A FRACTION OVER 100 % IS THE CHEAPEST CONTROL THERE IS.**
* **C3 CAN FAIL AND THE RULING CAN STILL STAND**, if the whole sweep is on one
  side of the bar. State both.
* **A FIGURE IN A COMMENT IS NOT A MEASUREMENT, AND THE COMMENT MAY BE THIRTY
  REVISIONS OLD.** Rev 42 published the arch crown as 0.7854 off a rev-8 comment
  stale since rev 13; the built value is **0.7770**. **Re-run the value; do not
  re-read the sentence.**

## How I work
* Ground in the reference → build → adversarial audit → iterate. Never build
  before grounding. Never call it done off self-review.
* Report the measurement against the reference, **with its ceiling**. Never a
  self-assigned score.
* Do not tell me anything is ready. Tell me what is fixed, what is still wrong,
  and what you measured.
* Keep visible cadence on long work. **As each render lands: `cp` it to
  `~/Desktop/tacombi_bus_render/`, `open` it, and print the absolute path.** Do
  not batch them to the end, and **a copy you did not `ls -l` afterwards is not
  a delivery.**
* **Ask me questions as MULTIPLE CHOICE with reference material.** Stated in
  full at Step 1, where you need it first.

---
> **THE STANDARD, in the owner's words.** The final product should be nearly
> indistinguishable from the original. **Any single measurement off is
> unacceptable.** The criterion is PER-MEASUREMENT. And above clinical accuracy:
> *"I want the owner to remember standing in the kombi, in this very picture
> that was provided."* — **that owner is the restaurant's owner.**
---

## §10. RESOLUTION AND THE SIDE PROBE
The hero: **4800×3200 in 20 strips**, SUB=2, 56 samples. `hero.py --only N` one
strip per call then `--stitch-only`; `post.py` runs **once** on the stitched
frame, never per strip. **TIMING RISES DOWN THE FRAME, PEAKS MID-FRAME, AND FALLS
AGAIN** — 153 s at strip 1, up to **614 s at strip 16**, back to **390 s at strip
19**, because the bottom strips are mostly ground and the mid-frame strips carry
the bus. **Rev 42 published "TIMINGS RISE MONOTONICALLY DOWN THE FRAME"; that is
wrong in shape, not just in value.** The figures here were re-derived from the
strip files' own mtimes — **and those files are gitignored, so this is the one
claim in this brief you cannot re-check from the repo.** Re-measure it on your
own machine and replace it. **Budget for the peak, not for the last strip.** **Run it with `nohup … &` and poll.** `hero.py`
strips in ROW space — seams are horizontal, and its own seam report is the check
that the frame is consistent (rev 42: **z = 1.95** against a threshold of 4).

**The flank probes NEED `out/p_side.png`**, gitignored, so produce it first
(≈95 s):
```bash
T1_SUB=1 T1_PREVIEW=side T1_SAMP=24 T1_RX=1400 T1_RY=933 T1_FX=0 \
  T1_PFX=p /tmp/blender/blender -b --python build.py
```
`T1_FX=0` is load-bearing: every mask in that chain is a chromaticity rule.
**1400 px wide is a FLOOR, not a suggestion** — `flank_compare` documents a
verdict flip across its aspect tolerance at 900 px for no change in the model.

## §11. VERIFY BY CONTENT — NOW A SCRIPT, NOT A PARAGRAPH
```bash
./verify_clone.sh            # 66 checks. exit 0 = ALL PASS. exit 1 = STOP.
./verify_clone.sh --quiet    # verdict line only
```
**WHY THIS REPLACED SIXTY LINES OF PROSE.** Until rev 43 these checks were
thirty hand-typed `grep -c` lines in the brief plus an eight-row guard table —
a second copy of numbers `STATE.md` already owns, free to drift, in a document
whose central rule is that stale values are the enemy. **Every one of those
lines was a value that could silently go stale.** They are now executable.

**WHAT IT CHECKS, and the three design rules behind it:**
* **IDENTITY IS ANCESTRY, NOT ARITHMETIC.** It does not test `== 227 commits` —
  that would fail the moment *you* commit anything, which is exactly when you
  need it. It tests that rev 42's verified tip `437d543` is an ancestor of HEAD,
  and that counts have not *shrunk*. **Run it as often as you like, mid-revision,
  after every commit.**
* **LOCATE BY SYMBOL, NEVER BY LINE NUMBER.** Nothing in it cites a line. Line
  numbers are precisely what rots — see §6 item 5.
* **A GATE WITHOUT A NULL IS NOT A GATE.** It was proved against five nulls on
  clean committed trees: delete a probe → caught; corrupt a texture → caught;
  silently downcase a SPEC rule → caught; create `docs/` and move a handoff →
  both caught; **move `V_POW_Z` to a different line → correctly NOT caught**,
  because the line number is not the invariant.

**IF IT EXITS 1: STOP, report the failing line with its ACTUAL value, and do not
build.** **Do not edit the script to make it pass.**

**ONE EXCEPTION, AND IT IS THE ONE YOU WILL HIT: `modified tracked files`.** The
moment you edit a tracked file, that check fails by design — it exists to catch
`audit.py`'s rewrite of `STATE.md`. **Mid-revision, expect exactly that one FAIL
and no other. It is not a finding.** Any OTHER failing line, at any time, is.
Commit, then re-run, and it should read ALL PASS again. If a check is genuinely
wrong, fix the check and say in the handoff which one moved and why — in the
same commit as the change that moved it.

**ALL EIGHT TEXTURE md5s ARE IN THERE AND THEY WILL MOVE** when §6 item 1's
re-bake lands. That is the point of the re-bake, not a regression. Re-run `md5`,
paste the new hashes into the script **in the same commit as the new artwork**.
Never a separate commit — that is how a tripwire becomes a rubber stamp.

**ONE NOTE ON CITATIONS IN THIS BRIEF.** `§5`, `§6`, `§10`, `§11` with no prefix
mean **sections of this file**. Anything written **`SPEC §n`** means a section of
`SPEC.md`. Bare `§10.x` always means SPEC — this file has no §10.x
subsections. **When in doubt grep SPEC.md for the anchor: the file is the
authority, not this sentence.**

### Guards, watched print
| check | SUB=1 | SUB=2 |
|---|---|---|
| VERIFY | **0 fail, 0 warn** | **0 fail, 0 warn** |
| `audit.py` | **0 fail, 0 warn** | **0 fail, 0 warn** |
| roof crown @ rear axle | **1.9835** | **1.9833** |
| cut roof hole | **70069v** | **254428v** |
| objects at `materials:` | **131** | **131** |
| meshes | **190** | **190** |
| bay widths | 0.516 0.515 0.516 | same |
| over-rider rows | **NOT APPLICABLE, stated** | same |

42 materials, 5 constant-rough, **0 non-manifold at both levels**, rake 17.75,
L = 4.065 W = 1.750, arch gaps 39.7 / 40.7 mm, off flank 804.9 mm.

**HOW TO SHIP NOW.** Commit and push; that is the whole handover.
1. Write **`HANDOFF_rev43.md`** and **`NEXT_CONTEXT_PROMPT_rev44.md`** at the
   **repo ROOT** — there is no `docs/`, and all 37 handoffs are flat there.
2. Regenerate `STATE.md` on a clean tree (`audit.py`, then `git checkout
   STATE.md` if you are not shipping it).
3. **Run `./verify_clone.sh` one last time and paste its verdict line into the
   handoff.** If you changed anything it checks, update the script IN THE SAME
   COMMIT as the change and say which check moved and why.
4. `git push`.
5. **COMMIT YOUR MARKED CROPS — they are tracked, and 17 predecessors are in
   the repo.** Only the hero and `out/` are gitignored and will not travel by
   push: `cp` those into `~/Desktop/tacombi_bus_render/`, `open` them, and print
   the absolute paths.
