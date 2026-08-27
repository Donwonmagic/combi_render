# START HERE — read this before touching anything

> **THIS FILE IS rev 7 (2026-08-09) AND IS KEPT AS A HISTORICAL INTAKE DOOR, NOT
> AS CURRENT INSTRUCTION.** It predates `bootstrap.sh`, `verify_clone.sh`,
> `CLAUDE.md` and `lid_gen.py`, which it mentions ZERO times, and its paths and
> core count below are wrong for this machine. **Current entry: `CLAUDE.md`, then
> the highest-numbered `NEXT_CONTEXT_PROMPT_rev*.md` (find it with `ls`; rev 68 at this edit), then
> `EMBLEM_HANDOFF.md` (the CARRIER for the owner's top item -- six reports, and the
> reason it has never been fixed), then
> `LEDGER_rev67.md` (what rev 67 measured and, in its §6 and §4, what it did NOT do and what
> it got wrong in its own work), then
> `REMAINING_WORK_rev61.md` (the RANKED EXECUTION LIST -- what is left, sorted into work,
> ceiled, the owner's call and process debt; its §I carries rows that were in no document
> at all), then `./bootstrap.sh` and `./verify_clone.sh`.** Not deleted — it is the only carrier
> of the rev-7 causal tests below (`CLAUDE.md` rule 16).
>
> **rev 7 (2026-08-09): read `HANDOFF_rev7.md` and `STATE.md` first.** Much of
> the detail below is superseded. In particular: "guards green" was only ever
> true at **SUB=1** — the production build was silently losing both cab-door
> shut lines; the belt/V-swage/aperture numbers listed as outstanding are now
> **applied**; and `STATE.md` is machine-written from live geometry, so believe
> it over any prose in this repo, including this file.

This file exists because progress kept being lost between sessions. Follow the
order below. It takes about five minutes and it is not optional.

---

## 1. Read the user's memory FIRST — before the code, before the spec

The previous context skipped this and rebuilt from a 246×197 thumbnail, which
cost about half a day and produced a wrong body type. Donald's memory holds his
own stated readings and the settled decisions.

Read `/areas/tacombi-combi-sticker.md` and `/preferences.md`.

**Standing process he requires:** ground in the reference → build → *adversarial*
audit → iterate, and keep going rather than stopping at good enough. He has
explicitly rejected self-reported scores. Report the measurement against the
reference, never a number you assigned yourself. Never declare anything ready.

## 2. Install Blender and run the guards before proposing anything

```bash
curl -fsSL -o b.tar.xz https://download.blender.org/release/Blender4.5/blender-4.5.3-linux-x64.tar.xz
tar -xf b.tar.xz && mv blender-4.5.3-linux-x64 /tmp/blender
cd /home/user/combi_render        # rev 7 said /home/claude/tacombi -- WRONG PATH
T1_SUB=1 T1_VERIFY=1 /tmp/blender/blender -b --python build.py
T1_SUB=1 /tmp/blender/blender -b --python audit.py
git checkout -- STATE.md
```

Expected as of rev 6: **0 fail, 0 warn**, `TYRE_D=0.6650`, 3 open apertures,
`lowered 65 mm`. If you see anything else, something regressed — find out what
before building on top of it.

## 3. Read `SPEC.md` (rev 6). It is authoritative.

`§0.2` lists retired readings. Any reappearance is a regression, not a variation.
`§8` records how every measurement was taken, so you can re-run it rather than
trust it.

**`SPEC_AUDIT.md` and `HANDOFF.md` are HISTORY, not truth.** Both are rev-3 era.
`HANDOFF.md` claims "0 fail, 0 warn" over a state that had one of each, and
claims six git commits that never existed. Do not act on either.

---

## The reference photographs — ranked

| File | What it settles |
|---|---|
| `ref_side.jpg` 1024×768 | **Primary.** Near-orthographic side elevation. Scale, apertures, belt line, ride height, counter |
| `ref_workshop.jpg` 1200×824 | Green mid-conversion. Nose geometry, bare rims, cut roof lids, empty lamp apertures |
| `ref_rear34.jpg` 1200×824 | Tail hardware, counter wrap, rear wheel |
| `ref_source.jpeg` 246×197 | The original thumbnail. **Superseded.** Do not settle anything new on it |

`REF_MEASUREMENTS.md` holds the full measurement working plus the verification
pass that resolved the three contested claims. Read it before re-measuring
anything — the work is probably already done.

---

## Two failure modes that have already bitten, twice each

**Correcting the vehicle toward the factory spec.** This bus is not a standard
1963 T1. rev 4 "corrected" the tyre to the factory 6.40-15 and zeroed the
lowering, and was wrong on both — rev 3 had them right. It has 16-inch rims,
≈0.665 m tyres, no rear bumper, and it sits 65 mm low with about 1.7° of
nose-down rake. **Measure the vehicle, do not assume the catalogue.**

**Measuring the belt line aft of the counter.** On the serving flank the visible
cream/red edge is the *counter fascia bottom* at 1.082 m, not the paint break.
The true break is at 1.207 m and is only visible forward of the counter, on the
cab door. This produced a 6× error.

---

## Hard constraints — learned by breaking them

- Pipeline order in `build.py`: subsurf applied before any boolean; wheel arches
  cut while the shell is still a closed solid; every other aperture cut after
  solidify.
- Do not remove the boolean rollback guard in `cut()`. One tangent cutter once
  destroyed the shell from 202 k to 9 k verts and still passed a naive check.
- ~~Keep panel-gap outlines ≥ 20 mm clear of roll-over regions~~ **REFUTED in
  rev 7 by causal test** — skip the wheel-arch cutters and the identical cutter
  at the identical z succeeds at subsurf 2. The real rule: **a panel-gap outline
  must not cross the lip of another aperture.** See SPEC §10.6.
- The body must stay a single continuous nose-to-tail loft. Separate cab and rear
  lofts leave a visible seam.
- **4 CPU cores** (rev 7 said 2). Do NOT fan out Blender: it is CPU-bound and two
  instances make both slower. Background every long render (`nohup … &`); the shell times out at
  two minutes. A 2400×1600 hero is 20–50 min. **Batch all changes into one
  rebuild** rather than rendering between fixes.
- **`verify.py` runs AFTER the ride-height drop** — this file said "before" and
  was wrong; probing a 5.5 mm shut line in the wrong frame read 26 % open
  instead of 100 %. Still do not subtract `RIDE_DROP` from the height
  expectation: it is compared against a height measured off the same dropped
  mesh, which is why "correcting" it produces the phantom 60 mm failure.
  There are **three** frames — see SPEC §10.1.

---

## Where the work actually stands

Done and verified: three apertures with a solid rear panel; blackwall tyres on
cream 16-inch rims with red hubcaps; cream bumpers, rear one absent; red VW
roundel; the Calidad sunburst on sheet metal; lowering reinstated; belt/sill
conflict resolved; white backdrop fixed (`bg_white_level()` — the cause was
linear 1.0 sitting upstream of AgX, not the shadow catcher); galley fill added.

Outstanding, in rough priority order:

1. **Apply the measured aperture edges** from `SPEC §1.1` — the code still has
   the rev-3 approximations, which were evenly spaced. They are not.
2. **Belt line to sill − 0.100.** `Z_BELT` is still 1.386; it needs 1.302, and
   `V_RISE` must move with it so `V_APEX + V_RISE == Z_BELT` still holds.
3. **Nose-down rake, ~1.7°.** Not modelled at all.
4. **Materials.** SPEC rev 4 locked the finish as weathered; most materials are
   still a single constant roughness, which is the physical definition of the
   plastic look. Needs roughness breakup, curvature-driven edge wear, a dust mask
   weighted to upward normals and the lower body, and a sun-fade gradient.
5. **Camera.** Still a pinhole with infinite depth of field — the loudest CGI
   tell at hero resolution. Needs a real focal length, sensor size and f-stop
   around f/8–f/11, plus mild chromatic aberration, vignette and grain.
6. **Missing detail inventory** — see `SPEC §4`. Rear-quarter louvres, fuel
   filler, aperture trim and bulbs, menu cards on the pillars, drip-rail bulb
   string, counter brass edge strip, the "1963" plate surround.
7. **`AUDIT_RECOVERED.md` — 89 findings, 13 critical, 44 major.** The six-lens
   audit completed all six find passes, then the container restarted and killed
   the verify and synthesise phases. So these findings are **UNVERIFIED** —
   no skeptic has attacked them. They also predate the high-resolution
   photographs, so where they disagree with `REF_MEASUREMENTS.md`, **the
   measurements win.** Re-run a skeptic pass over the criticals before acting
   on any of them; past experience is that roughly a third do not survive.

---

## Keeping this file honest

This file drifted last time because it was written by hand. The fix, not yet
built: have `audit.py` emit a `STATE.md` containing the measured dimensions,
guard results and object inventory, so the status section cannot claim a passing
build that isn't. Until that exists, **re-run the guards and believe them over
any prose in this repo, including this file.**


## IF `download.blender.org` RETURNS 403 (it does, through some proxies)

Both the `.dmg` and the Linux tarball fail. The route that works is PyPI:

```bash
python3.11 -m venv /tmp/bpyvenv
/tmp/bpyvenv/bin/python -m pip install bpy==4.5.3 pillow numpy scipy
```

Then reproduce the layout the repo hard-codes in **eight** `.py`/`.sh` files, so
that not one of them has to be edited:

* `/tmp/blender/blender` — a Python shim parsing `-b --python FILE [-- args]`,
  importing `bpy`, and `runpy.run_path(FILE, run_name="__main__")`. It must
  leave the FULL command line in `sys.argv`, because the repo uses the
  `sys.argv[sys.argv.index("--")+1:]` idiom.
* `/tmp/blender/4.5/python/bin/python3.11` — `#!/bin/sh` + `exec
  /tmp/bpyvenv/bin/python "$@"`.

**THE INTERPRETER SHIM MUST `exec`, NOT BE A SYMLINK.** venv resolution keys off
`sys.executable`'s own directory to find `pyvenv.cfg`; a symlink from `/tmp`
lands outside the venv and imports nothing. That cost rev 43 a cycle.
