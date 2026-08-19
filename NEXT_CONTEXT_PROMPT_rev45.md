# NEXT CONTEXT PROMPT — rev 45

Please act as my expert. Continue the Señor Tacombi combi build. **Forty-four revisions sit behind
this.** You are picking up mid-stream, not starting.

**WHERE THIS BRIEF AND THE MACHINE DISAGREE, THE MACHINE IS RIGHT — say so and correct the brief in
the same revision.** Rev 43 corrected its own brief by running it. Rev 44 corrected **nineteen**
things in its brief, four things in the ledger it was told to trust, and **one thing it had itself
committed forty minutes earlier**. Do the same.

---

## Step 0 — prove the tree. THREE THINGS BIT REV 44 HERE.

```bash
pwd && git remote -v && git fetch origin && git status -sb
git rev-parse --is-shallow-repository        # if true: git fetch --unshallow
./verify_clone.sh                            # ALL 66 PASS, exit 0
uname -m && nproc && df -h . /tmp
ls LEDGER_rev44.md HANDOFF_rev44.md PHOTOS_WANTED_rev44.md
```

1. **CHECK THE FOUR SPINE DOCUMENTS ARE ACTUALLY ON YOUR BRANCH.** Rev 44's brief was built on
   `LEDGER_rev43.md`, `AUDIT_rev43.md`, `PLAN_rev43_item1.md` and `HANDOFF_rev43.md` — **and none of
   them existed on the working branch.** They were on a different remote branch. The last `ls` line
   above is not decoration.
2. **`verify_clone.sh` FAILS ON A FRESH CLONE AND THE TREE IS FINE.** It prints **65 PASSED, 1
   FAILED**, exit 1, because a shallow clone has 50 commits against the ≥227 it wants.
   `git fetch --unshallow`. **Do not edit the check** — the script now says so itself.
3. **DO NOT INHERIT THE PLATFORM.** Rev 43's brief said macOS; rev 43 and rev 44 both ran on **Linux
   x86_64, 4 cores**. Detect it.

**`download.blender.org` RETURNS 403 THROUGH THIS PROXY.** Re-tested at rev 44, both the tarball and
the `.dmg`. **The working recipe is now in `START_HERE.md`** — `pip install bpy==4.5.3` against
Python 3.11 plus two shims reproducing `/tmp/blender`. **THE INTERPRETER SHIM MUST `exec`, NOT BE A
SYMLINK.** Eight `.py`/`.sh` files hard-code that path; **rev 43 and rev 44 each edited zero of
them.** Keep it that way.

**TIMINGS ON 4 CORES, measured rev 44:** build SUB=1 **17.4 s**, SUB=2 **61.9 s**, `out/p_side.png`
**64.2 s**, `probe_rev42_uv` **~25 min** (it is the long pole — start it first and do other work).

---

## Step 0.5 — fire the asks first, and point one agent at this document

**The owner questions have the longest latency in the revision.** Fire them before the guards.

**AND POINT ONE AGENT AT THIS DOCUMENT, TOLD TO REFUTE IT.** That agent has now paid for itself three
times running. Rev 44's returned **19 refutations**, five of which changed what the revision did —
including that the brief declared the DESIGN lane never ran when it had produced 23 findings.
**Tell it what is already known so it hunts for new things**, and tell it to check every count by
running it.

---

## Step 1 — `LEDGER_rev44.md` IS THE SPINE. Read it first.

Four classes; done is **class 1 all green, class 2 all still red, class 3 empty, class 4 empty.**

| class | rule | at rev 44 |
|---|---|---|
| GREEN-REQUIRED | must pass | **all green**, four guard runs |
| RED-BY-DESIGN | must **stay** red | **all still red** — **EIGHT** KILL probes, not seven |
| OPEN FINDINGS | the burn-down | **23** |
| UNINSTRUMENTED | needs an instrument first | **7** |

**A run where every probe exits 0 is a REGRESSION.** Read each probe's **OWN SUMMARY LINE**, never
its exit code.

**THE PROBE CENSUS, corrected rev 44 by running all of them.** 34 `probe_*.py` on disk: **25**
control-bearing with a parseable summary line, **2** with controls in a format the reading rule
cannot parse (`probe_orb_blade`, `probe_orb_hoop`), **7** reporters that were never gates
(`probe_v_apex`, `probe_cross_anatomy`, `probe_shutlines`, `probe_rev16`, `probe_ctan_index`,
`probe_ctan_pedestal`, `probe_orb_post`). Rev 43's *"31 of 31 probes run"* conflated the three while
its tables named only 20.

**SEVERAL PROBES ARE PLAIN-PYTHON, NOT BLENDER.** Run under `blender -b --python` they read
`sys.argv[1]` as a render path, get `'-b'`, and die with `FileNotFoundError`. That is the wrong
interpreter, not a shim defect. `probe_rev39_flank`, `probe_rev40_datum` and the flank family also
need `out/p_side.png`, which is gitignored — **render it first**, command in `README.md`.

---

## Step 2 — the guards

`T1_SUB` is 1 **and then** 2, both tools, four runs. `audit.py` rewrites `STATE.md`; restore with
`git checkout -- STATE.md` **on its own line, not with `&&`** — `README.md` was fixed at rev 44 and
now says why.

**Rev 44's watched print, all four runs 0 fail / 0 warn:** **190** meshes, **5** constant-rough,
roof **1.9835 / 1.9833**, rake **17.75**, **L=4.065 W=1.750**, bays **0.516 0.515 0.516**.

---

## §3. WORK LIST FOR REV 45

### 1. ITEM 1 — NOW PROPERLY SIZED. **READ `HANDOFF_rev44.md` §4 BEFORE TOUCHING ANYTHING.**

**The owner answered: the art KEEPS ITS DRAWN SCALE and EXTENDS down. It does not stretch.**

Three things the record had wrong, all instrumented in `probe_rev44_doorart.py`:

* **`DOOR_H` divides nothing and is not the v-map.** Two read sites, both `h = sv * DOOR_H`, both
  multiplying, for two motifs. SPEC §10.100.6 and `t1_shell.py:546` both corrected at rev 44.
* **`door_pv` is the v-map and it ALREADY drives off the door's own outline per station.** The old
  brief's proposed fix is already what happens. **Nothing needs building for it.**
* **And `door_pv` is PROPORTIONAL, so the obvious one-line re-point STRETCHES the art** — it moves a
  fixed `v` by **309.1 mm** at the front corner. That is the option the owner rejected.

**The added depth is TWO CORNER LOBES, not a band:** 272.2 mm rear, 387.5 mm front, **1.8 mm over the
front wheel arch**. A re-point does not scale the art, it **shears** it (+59.7 / +84.2 / +0.4 %).

**THE JOB: make `door_pv` belt-anchored and metric, then GROW the inventory to fill two corner
lobes.** A drawing job. Budget it as one.

### 2. THE 89 IN `AUDIT_RECOVERED.md`, STILL UNVERIFIED SINCE REV 6

**It is 89, not 119** — the other 30 are the FIDELITY half of the 60 `AUDIT_rev43.md` already
verified. **Four audits have now been killed before their verify phase**: a container restart, two
CPU cores, a session token limit, and a branch that did not carry the output. **Pipeline verification
behind each finder so a stall cannot strand the lot, and commit whatever completes, immediately.**

**AND APPLY REV 43'S RULE, WHICH REV 44 SHOWED HAS TEETH: AN ADVERSARIAL VERIFIER MUST RE-DERIVE THE
WINDOW, NOT ONLY THE METHOD.** Better still, follow `probe_rev44_typo.py` and use tests that have **no
window at all** — connected components, hole counts, orderings. A test with no window cannot inherit
one.

### 3. `AUDIT_rev43.md` NEEDS TWO REPAIRS

* **§2 still lists the RETRACTED tilde finding among its surviving severity-5s.** §0 and §1 were
  updated; §2's table was not. **So "55 surviving" over-counts by one — it is 54.**
* **§0 says the tilde is 16 px; §5's typography ceiling says 62 px at 7.8σ.** The only component near
  62 px is the 61 px one, and it sits **under the S**, not over the `n`. The 16 px is right —
  `probe_rev44_typo` C5. Settle the document.

### 4. REPORT 3 — THE FIX, WITH A GATE ALREADY ARMED

`probe_rev44_report3.py` **C6 is the burn-down gate** and the only control in this project that is
supposed to change class. Today the two-tone break **cuts a 131.9 mm chord across the headlamp
aperture**; in the photograph the lamp is clear of it with 12 px of red above.

**TRAPS, unchanged:** do not move the roundel with the lamps; §10.24's three findings are not one
change. **AND A NEW ONE:** the break at the lamp is the **V-swage**, not the flank belt — comparing
against the belt is a 208 mm error, armed as C5.

### 5. THE PHOTOGRAPHS — HE OFFERED, AND THE LIST IS WRITTEN

**`PHOTOS_WANTED_rev44.md`.** Five gaps, each with what a usable frame must contain and what makes
one useless, plus eight ranked links. **Check whether he has added any before doing anything else** —
the off side and the roof height are the two highest-value unknowns in the project.

**WHAT THIS ENVIRONMENT CAN DO, corrected rev 44:** **`WebSearch` works.** `WebFetch` and `curl` are
egress-blocked, 403 on every domain. So you can find and rank links but **cannot open one**. The
owner is the only route to image files.

### 6. THE STICKER — THE SPEC EXISTS. THE ASSET DOES NOT.

**Do not re-write the art direction.** `AUDIT_rev43.md` §5 carries a full STICKER dimension —
viewpoint (18° front three-quarter, eye height 1.55 m), the cab-door owner question, the flank
triptych, the 48-of-66 sacrifice rule, the 0.159 m minimum cut feature, the 0.15 mm line floor, the
sun, and colour separation. **What is missing is a drawn line.** It remains the original deliverable
and it has **zero code and zero assets on disk after forty-four revisions.** The owner's recorded
decision: build it after the model is done.

### 7. FINDING 20 — STILL UNSETTLEABLE HERE

`probe_rev42_uv` prints **56.15 %** against SPEC §10.101.3's **55.97 %**. **Rev 44 reproduced 56.15 %
a second time**, so the discrepancy is **stable, not noisy**. Settling it needs a real Blender binary
and this environment cannot reach one. **Do not quote either figure as canonical.** It does not move
the ruling — §10.101.6's own sweep spans 59.06–67.50 % against a bar of 10 %.

---

### ITEMS ADDED BY REV 44b — THE FIDELITY PASS

The owner supplied a **catalogue-grade product render of a school bus** and
asked for *"the very highest resolution, fidelity, and detail possible."* That
was turned into numbers before anything was built — `probe_rev44_fidelity.py`,
and **it is the first thing to re-run this revision.** It is cheap and it does
not argue. Rev 44b's baseline: 190 objects, 655 944 tri (**77 % of them in
`T1_body` alone**), **0 Bevel modifiers**, **66 566 hard edges**, **0 rivets /
bolts / screws / nuts / latches**, 0 displacement. See `HANDOFF_rev44.md` §10–13.

**A1. THE ~49 mm AT THE BODY'S LOWER EDGE — FIRST JOB, AND DO IT BEFORE ANYTHING
ELSE TOUCHES z.** `ref_nolita_doorshut.jpg` puts the rocker **37.8 mm ABOVE**
the axle centre; the built model puts it **11.2 mm BELOW**. Cross-checked by
arch-crown-to-rocker: **335.6 mm** measured against **390.0 mm** built. Same sign
both ways, insensitive to which of the three scales is used. The datum question
*is settled* — a column-by-column trace of the lowest red pixel over cols 20–140
shows **one continuous rocker with no valance step**, and the first pass's 80 mm
was the **red hubcap** leaking into the mask over cols 74–104.
**Do not move geometry on this yet.** The built body is lowered **65.7 mm at
x = 1.0** by `RIDE_DROP` plus the rake, so if the photograph is right `RIDE_DROP`
is most of the error — a whole-vehicle change. **Reproduce it independently on
`ref_side.jpg` first.** If it reproduces, it is the largest single accuracy
finding open in the project.

**A2. FASTENERS.** Still zero outside the four cab-door hinge assemblies added in
§10.104.6. Next tranche, in return-per-effort order: rivets along the counter's
nosing and the gallows, bumper bolts, hatch latches, drip-rail clips. Each is
small geometry with a large perceived-detail return, and the hinges show the
pattern: place them off a member that is already guarded (`DOOR_GAP`'s front
edge, `flank_y`), never by eye.

**A3. THE CAB IS CLASS 4.** §10.104's furniture is type-correct and **not
measured** — no frame in this repo resolves the cab interior. It is placed off
members that *are* fixed so it cannot drift independently of the shell, but that
is a coupling, not a measurement. Related and open: the **driving position** is
622 mm from the seat back to the hub, ~150 mm more reach than a T1 driver has,
and closing it needs the seat's fore-aft position, which is rev-8 authored.

**A4. TYRES.** Circumferential grooves exist and are period-correct; there are no
lateral sipes and no sidewall lettering. The next step is a **normal map**, not
geometry — and per §10.105.7 it ships with the frame that shows it or it does not
ship.

**A5. THE PAINT'S FINISH IS NOT ON THIS LIST, DELIBERATELY.** §10.104.8 refuses
it in writing: the reference is a factory-clean product render, this is a
weathered 1963 working truck, and §4.3's chalky finish is **measured** — rev 3's
mirror clearcoat is what made the red read salmon at 0.37 against 0.82. **The
detail bar transfers. The finish does not.** If a later context is tempted, read
§10.104.8 before touching `Roughness` or `Coat Weight`.

## §4. WHAT ONLY THE OWNER CAN GIVE

1. **THE PHOTOGRAPHS.** See §3.5. He has offered; the list is written.
2. **The cab-door multiple choice** for the sticker — `AUDIT_rev43.md` §2 flags it as an explicit
   OWNER QUESTION and it has never been put to him.
3. **Ride height** (ledger finding 12) — he states lower than stock; SPEC §0.2 and REF §2
   **contradict each other** and it has never been adjudicated.

**ANSWERED AT REV 44, do not re-ask:** door art stretches or extends (**extends, drawn scale**);
whether `ref_nolita_doorshut.jpg` is the same vehicle (**it is** — §7.1, and it keeps §10.100's
corroboration alive); finding 22's scoping (**sanctioned**, letterform geometry only).

## §5. SETTLED — do not re-open

Over-rider assembly (rev 37). Signboard/`lidsign`. Region 3. Ten flower heads. Tyre diameter.
Counter slab to 0.0 mm. Break-to-sill (**the settled dimension is 100.0 mm; 2.7 mm is a residual**).
The Z-ladder's gate. The door outline's arch clearance. **The ñ HAS its tilde** — retracted at rev
43, re-confirmed window-free at rev 44. **The `S`'s three fragments and the `e`'s counters are NOT
generator defects** — refuted at rev 44 on topology; the S's breaks are a deliberate reproduction of
a tarnish artefact and `senor_trace.py`'s own docstring says so.

## §6. RULES THAT BIT AGAIN IN REV 44

* **A FIGURE YOU DID NOT WATCH PRINT IS NOT A MEASUREMENT — AND NEITHER IS A DERIVATION.** Rev 44
  wrote a source-grep to classify 34 probes and it **disagreed with the runs on five of them**,
  because their summary strings are built from variables. The grep was discarded.
* **CHECK WHAT YOUR ESTIMATOR IS ACTUALLY MEASURING.** A first cut read *"lowest z near x"* off
  `DOOR_GAP_S` — the **whole door perimeter** — and so measured the door's **vertical edges** at the
  corners, publishing 252/380 mm where the answer is 272.2/387.5. Use `DOOR_BOT_RUN`.
* **AN ORDINAL TEST THAT BOTH SIDES PASS IS NOT EVIDENCE.** Rev 43 published *"the headlamp sits 20 px
  BELOW the break, STRONG"*. The build puts it below too. **Ask what the test would look like if the
  model were right, before publishing it as a defect.**
* **THE OBVIOUS INFERENCE FROM A TRUE OBSERVATION CAN STILL BE FALSE.** Both red frames are
  Mexico-shot — true, measured. *"So the red livery is Playa-era"* — **false**; the red bus stands in
  Nolita. Rev 44 committed that and retracted it in the same revision.
* **A FINDING NOBODY REFUTED IS NOT A FINDING**, and **a refuter given the same window as the finder
  is not an adversary.** Both of rev 43's confirmed a retracted finding because both inherited its
  window.
