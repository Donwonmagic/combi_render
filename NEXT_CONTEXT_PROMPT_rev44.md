# NEXT CONTEXT PROMPT — rev 44
Please act as my expert. Continue the Señor Tacombi combi build. **Forty-three revisions sit behind
this.** You are picking up mid-stream, not starting.

**WHERE THIS BRIEF AND THE MACHINE DISAGREE, THE MACHINE IS RIGHT — say so and correct the brief in
the same revision.** Rev 43 corrected four things in its own brief by running them. Do the same.

---

## Step 0 — prove the tree, and DO NOT INHERIT THE PLATFORM
```bash
pwd && git remote -v && git fetch origin && git status -sb
./verify_clone.sh                 # must print ALL 66 PASS and exit 0
uname -m && (nproc || sysctl -n hw.ncpu) && df -h . /tmp
```

**THE REV-43 BRIEF SAID "YOU ARE CLAUDE CODE ON HIS MAC". REV 43 RAN ON LINUX.** Do not assume
either. **Detect the platform before you read another line of Step 2.** What rev 43 hit:

* **`download.blender.org` returned 403 through the environment's proxy** — the `.dmg` AND the Linux
  tarball. If that happens to you, the route that worked is **`pip install bpy==4.5.3` from PyPI**
  against a Python **3.11** interpreter, then two shims reproducing the layout the repo hard-codes:
  ```bash
  mkdir -p /tmp/blender/4.5/python/bin
  printf '#!/usr/bin/env python\n...'  > /tmp/blender/blender          # see HANDOFF_rev43.md sec.0
  printf '#!/bin/sh\nexec <venv>/bin/python "$@"\n' > /tmp/blender/4.5/python/bin/python3.11
  chmod +x /tmp/blender/blender /tmp/blender/4.5/python/bin/python3.11
  ```
  **THE INTERPRETER SHIM MUST `exec`, NOT BE A SYMLINK.** venv resolution keys off `sys.executable`'s
  own directory to find `pyvenv.cfg`; a symlink from `/tmp` lands outside the venv and imports
  nothing. That cost rev 43 a cycle.
  **SATISFY THE LAYOUT. DO NOT EDIT THE EIGHT FILES THAT HARD-CODE `/tmp/blender`.** Rev 43 edited none.
* **`~/Desktop/tacombi_bus_render` may not exist and there may be no `open`.** Do not assume a
  delivery mechanism — check, and if it is absent, deliver in the session.
* **`out/` and the heroes are gitignored and may exist nowhere.** `out/p_side.png` re-renders in
  **57 s** on 4 cores. **There is currently NO HERO in the repo**, so nothing can be audited against
  a render until one is shot.

**RE-TIMED ON 4 CORES:** build SUB=1 **24 s**, SUB=2 **61 s**, audit **24 s / 69 s**, p_side **57 s**.
§5's old SUB=2 budget of ~104 s is loose by 1.7×.

## Step 0.5 — status inside twenty minutes, and fire the asks first
Same shape as rev 43's brief. **The questions have the longest latency in the revision; fire them
before the guards.** The ones outstanding are in §6 below.

**AND POINT ONE AGENT AT THIS DOCUMENT, TOLD TO REFUTE IT.** Rev 43's brief shipped claiming its own
verify script prints 49 checks when it prints 66 — stated three times, caught in minute one by an
adversary rather than by its author. **That agent has paid for itself twice now.**

---

## Step 1 — THE LEDGER IS THE SPINE. Read it first.
**`LEDGER_rev43.md` is new and it replaces guesswork about what "done" means.** The owner was asked
and chose **"every instrumented measure green."** That cannot be read literally — seven probes carry
KILL controls *written to fail*, two are deliberately left failing, one refuses to rule. **A run
where every probe exits 0 is a REGRESSION.** The ledger's four classes make it operational:

| class | rule | at rev 43 |
|---|---|---|
| GREEN-REQUIRED | must pass | **all green** |
| RED-BY-DESIGN | must **stay** red | **all still red** |
| OPEN FINDINGS | must reach zero — **the burn-down** | **22** |
| UNINSTRUMENTED REQUIREMENT | needs an instrument before "green" means anything | **7** |

**KEEP IT CURRENT. It is the only artefact in this project that answers "how far are we".**

## Step 2 — the guards, then the probes
`T1_SUB` is 1 **and then** 2, both tools, four runs. `audit.py` rewrites `STATE.md`; restore with
`git checkout -- STATE.md` on its own line, **not** with `&&`.

**Rev 43's watched print, all four runs 0 fail / 0 warn:** roof **1.9835 / 1.9833**, cut roof hole
**70069 / 254428 v**, **131** objects, **190** meshes, **42** materials, **5** constant-rough,
**0 non-manifold both levels**, rake **17.75**, **L=4.065 W=1.750**, bays **0.516 0.515 0.516**,
arch gaps **39.7 / 40.7**, off flank **804.9**, over-rider **NOT APPLICABLE, stated**.

**All 31 probes reproduce their expected tally.** Read each probe's **OWN SUMMARY LINE**, never its
exit code. The full table is in `LEDGER_rev43.md` — use it rather than re-deriving.

---

## §6. WORK LIST FOR REV 44

**1. VERIFY THE 30, THEN THE 89. This is the revision.**
`AUDIT_rev43_PARTIAL.json` holds **30 findings from four FIDELITY dimensions** (counter, wheels,
roof, tail). **THEY ARE UNVERIFIED — every adversarial refuter died on a session token limit.**
`AUDIT_RECOVERED.md` holds **89 more**, stranded since a container restart killed that audit's
verify phase around rev 6. **Findings this project accepted without adversarial verification have
been overturned more often than not. Until refuted, all 119 are worth nothing.**
The verification workflow is written and resumable; see `HANDOFF_rev43.md` §7.
**Highest-severity unverified, both ordinal, both roof:** the main lid is raked the WRONG WAY
(`LID_OPEN_DEG=104°` leans the mural board away from the counter) and the open lid at the tail does
not exist. **Corroborated across two independent dimensions: roof AND tail both found the owner's
TRUNK LID unbuilt** — `grep -c trunk t1_shell.py build.py` is still **0 and 0**.

**2. THE DESIGN LANE NEVER RAN.** Typography, branding and the sticker all died with the limit.
The sticker is **the original deliverable** and has **zero code and zero assets on disk after 43
revisions**. The owner's decision, recorded: **build it after the model is done.** Its art direction
spec is still owed.

**3. ITEM 1 — PLANNED, NOT STARTED. Read `PLAN_rev43_item1.md` before anything.**
Its first decision is answered from the code: **REPRODUCE the affine map, do not replace it** — the
flank map `u = U0 + SGN·0.26·x`, `v = 0.263 + 0.26·z` is exactly what a planar UV projection
computes, so `folk_gen` survives untouched.
**DO ACTION 0 FIRST:** the shell is solidified to **2.8 mm**, every outer face has an inner twin
whose normal is still Y-dominant, and BOX therefore lands it on **the same texels**. The probe
splits on the sign of POSITION, so **the inner skin is counted in the 56 %.** Decompose the figure
into invisible inner-skin duplication versus genuine visible collision **before deciding how big
the job is.**
**AND `DOOR_H` CANNOT EXPRESS THE OWNER'S ANSWER.** He said the art reaches the door's bottom edge.
`DOOR_H` is a single scalar; the door's added depth is **272.2 mm rear, 387.5 mm front**. Setting it
to ~1.40 is right at one corner and **115 mm wrong at the other**. Drive the art's extent from the
door's own outline — `z_bot(x)`, which §10.100.4 already builds.
**SPEC §10.100.6 CALLS `DOOR_H` A DIVISOR AND IS WRONG** — the code says multiplier, twice, and
§10.73's own arithmetic agrees. Correct it in the same revision that acts on it.
**§10.10 CONTAINS NO NUMERIC TARGETS.** The de-facto template is **§10.68**, rev 25's own re-bake report.

**4. FINDING 20 — re-run `probe_rev42_uv` ON A REAL BLENDER BINARY.** It printed **56.15 %** against
SPEC §10.101.3's **55.97 %**. The mesh reproduces to the integer, so the likeliest cause is `bpy`
from PyPI rather than the binary. Settle it before either figure is quoted again.

**5. REPORT 3 — read the ordinal off the BUILD's own constants.** Rev 43 added a photographic arm:
on `ref_source.jpeg` the **headlamp sits 20 px BELOW the two-tone break**, 10× the reading
uncertainty. The indicator arm is only 3 px and **was deliberately not published**. The owner's
words are *"the paint job and the **headlights** are not alligned"*, so the headlamp arm is the one
that matters. **Now read the same above/below off the build's constants — exact, no camera, no
hero.** Traps unchanged: **do not move the roundel with the lamps**; §10.24's three findings are
not one change.

**6. FINDING 22 — THE SCRIPT IS IN TWO PHOTOGRAPHS.** `ref_workshop.jpg` carries the identical
"Señor Tacombi" script on the green body, and no document in the repo connects them. §7.7 has been
rejected twice and authored against `ref_side.jpg` alone. **Ceiling: the workshop view is
FORESHORTENED at 210×140 px against `ref_side`'s 320×110 near-broadside — it is an INDEPENDENT view,
not a better one.** The proposed scoping — letterform geometry admissible, colour and weathering
barred — **is not yet sanctioned by the owner. Get that before using it.**

**7. FINDING 21 — `ref_source.jpeg` is retired by §10.22 and load-bearing for §0.2's red-roundel
lock at the same time.** Resolve it in SPEC.

**8. FINDING 23 — BOTH RED FRAMES ARE MEXICO.** Palms, an open-air patio, and a Spanish sign in
`ref_rear34.jpg`. **The red livery is Playa-era and the project holds no Nolita photograph** except
the one rev 43 committed. Rev 14's Nolita re-admission rested partly on the opposite premise. Fix
the era tags; no measurement moves.

---

## §7. WHAT ONLY THE OWNER CAN GIVE
1. **Stretch or extend?** Does the door art stretch to fill the deeper door, or keep its drawn scale
   and extend further down? They differ by ~38 % and **no photograph can settle it** — the only frame
   showing the door's full outline carries no art.
2. **Is the bus in `ref_nolita_doorshut.jpg` the same vehicle as `ref_side.jpg`?** It carries no
   folk art and no script — a third livery state. **If it is a different vehicle, its door geometry
   is not admissible and rev 43's corroboration of §10.100 evaporates.**
3. **Sanction for finding 22's scoping.**
4. **THE PHOTOGRAPHS, still.** No off-side. No head-on rear. Nothing settling the absolute roof
   height, which is **OPEN AND UNMEASURED** — the model reads 1.9835 on nothing.
   **Rev 43's environment could not fetch images at all** — `WebFetch` was egress-blocked for every
   domain, two scouts, clean null on all five targets. **The only route is him.**

## §8. SETTLED — do not re-open
Over-rider assembly (withdrawn, rev 37). Signboard/`lidsign` (not part of the vehicle; gated at
`T1_SIGNBOARD=0`; **no hero with it on**). Region 3 (the counter's front face). Ten flower heads.
Tyre diameter. Counter slab to 0.0 mm. Break-to-sill to 2.7 mm. The Z-ladder's gate — **no power,
70 % false-answer rate; only its JOINT registration may be quoted.** The door outline's arch
clearance, armed at rev 41's own value.

## §9. RULES THAT BIT AGAIN IN REV 43
* **A FIGURE YOU DID NOT WATCH PRINT IS NOT A MEASUREMENT.** A figure shipped saying y=113 where the
  run printed y=115 — and that changed the conclusion.
* **CHECK WHAT YOUR DETECTOR CAN PHYSICALLY SEE.** A break detector returned the **VW roundel**
  because the roundel is red too. A door-bottom detector switched between three features and its
  number was discarded rather than published.
* **CHECK THE REPO BEFORE CALLING SOMETHING NEW.** A supplied frame was called new evidence and
  correlates **1.000** with a file already tracked. Two findings came out of chasing that error —
  which is why you say it out loud rather than quietly fixing it.
* **AN ORDINAL FACT NEEDS NO RULER** — and state which arm is strong and which is not. Rev 43
  published a 20 px arm and withheld a 3 px one from the same figure.
* **A FINDING NOBODY REFUTED IS NOT A FINDING.** Three separate audits have now been killed before
  their verify phase: a container restart, two CPU cores, and a session token limit. **119 findings
  sit unverified because of it.** Pipeline verification behind each finder so a stall cannot strand
  the lot — and commit whatever completes, immediately.
