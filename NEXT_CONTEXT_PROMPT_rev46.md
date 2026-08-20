# NEXT CONTEXT PROMPT — rev 46

**Read this whole file before you touch anything.** It is written for a context that knows nothing
about this project. Everything you need to start is here; everything you need to be *correct* is in
`SPEC.md` and `LEDGER_rev45.md`, and this file tells you where to look.

---

## §0. DO THIS FIRST. IT TAKES ELEVEN CHARACTERS AND IT COST REV 45 AN INVESTIGATION

```bash
cd /home/user/combi_render
git log --oneline HEAD..origin/claude/project-improvement-id3a9o     # and every other claude/* branch
git branch -r
```

**Rev 45 opened on a brief whose §0 said the owner had reported the same defects three times while
every guard stayed green, and offered three explanations — all of them about how he is being shown
things.** The real explanation was none of those:

> **SEVENTEEN COMMITS OF REV-44 AND REV-44b WORK HAD NEVER BEEN MERGED.**

`origin/claude/tacombi-combi-rev-44-h4ipmg` sat seventeen commits above the point where PR #2 landed.
`SPEC.md` on `main` ended at **§10.101** — §10.102–§10.109, all eight rev-44b sections, were not
there. Neither were `cab_fitout`, `door_hinges`, `cabin_fill`, `round_edges`, the door-wrap
retraction, the prop fix, or **three of the four reference photographs the brief said were tracked**.
Item **W1** of the rev-45 brief — the entire roundel task — was specified against
`ref_nolita_front34.jpg`, a file that was not in the tree.

Rev 45 merged all seventeen. **Check this again anyway.** The rule is now in `SPEC` §10.113.5:

> **A REVISION THAT IS NOT MERGED DID NOT HAPPEN.**

---

## §1. THE OBJECTIVE, IN HIS WORDS

A photoreal 3D model and hero render of **Señor Tacombi** — a 1963 VW T1 Kombi converted into a taco
truck. He supplied a catalogue-grade product render of a school bus as the bar and asked for *"the
very highest resolution, fidelity, and detail possible. Cutting edge stuff, and I need you to guide
it."* And: **"Keep tuning the bus until it is perfect!!"**

The standing instruction, from the original brief and still in force:

> **WHERE THIS BRIEF AND THE MACHINE DISAGREE, THE MACHINE IS RIGHT — say so and correct the brief in
> the same revision.**

That applies to *this document* too. Rev 45 exercised it three times against its own brief (§4's
photo inventory, §2's `T1_PREVIEW` names, §5's W1).

---

## §2. THE THING REV 45 LEARNED, WHICH OUTRANKS EVERY GEOMETRIC ITEM BELOW

**This project has measured beautifully and looked at almost nothing.**

The nose badge rendered as a **clock face** for thirty-five revisions. Eight correct measurements of
that emblem exist — §10.25's air gap, §10.107's six stroke ends, `probe_rev44_lampmove`'s two height
chains, rev 45's own stroke width at 0.7 σ. **Every one was taken in the glyph's own plane**, and
every one was blind to a 32 mm error in the direction nobody looked: the badge is a flat plate and the
nose is curved, so its upper half floated 32 mm proud and its lower half — the whole W — was inside
the sheet metal.

The same defect class, found the same way, on the same day: the **headlamp lens was dished concave**
with its centre 10 mm inside the nose, and the **sign props were footed inside the roof aperture**,
standing on nothing.

> **NEW RULE, §10.110.8: A PART MEASURED IN ISOLATION FROM WHAT IT IS FITTED TO IS NOT MEASURED.**
> Rule 10 says *a detail you cannot see is not a detail*. This is its converse — **a detail that
> measures perfectly and renders wrong is being measured in the wrong frame.**

**So: render it, crop it, and look at it, before and after every change.** `probe_rev45_nose.py` is
the instrument for that and it is new. It **does not type crop boxes** — every other crop box in this
repository is a hand-typed literal that goes stale the moment a camera or a constant moves. It
projects known 3-D landmarks through the render camera and samples where they land. Copy it.

---

## §3. PROVE THE TREE — ONE COMMAND

```bash
cd /home/user/combi_render
./bootstrap.sh            # toolchain + tree.  ~1 min warm, ~5 min cold.
./bootstrap.sh --guards   # ... and both builds and the probes.  ~6 min more.
```

**`bootstrap.sh` is new at rev 45 and it exists because every context before you
spent its first twenty minutes doing the same four things by hand from a recipe
that lives in prose and has drifted twice.** It installs `bpy`, builds the two
shims, deepens a shallow clone, checks that **no branch carries work `HEAD` does
not have** (§0), and then runs `verify_clone.sh`. Expect **ALL 10 PASS**.

It is idempotent and it was proved from scratch: `rm -rf /tmp/blender &&
./bootstrap.sh` rebuilds the whole toolchain and passes.

It also carries a **positive control on the shim itself** — several probes read
`sys.argv[sys.argv.index("--")+1:]`, and a shim that rewrites argv makes those
read the wrong slice silently. Without that control "the shim works" is untested.

If you would rather do it by hand, everything below still applies.

**Blender is not installed as an application.** `download.blender.org` returns 403 through the egress
proxy. Blender 4.5.3 comes from `pip install bpy==4.5.3`, and **two shims** reproduce the paths eight
files hard-code:

* `/tmp/blender/blender` — a Python shim parsing `-b [-P|--python] FILE [-- args]`, importing `bpy`,
  and `runpy.run_path(FILE, run_name="__main__")`. It must leave the **full** command line in
  `sys.argv`, because the repo uses the `sys.argv[sys.argv.index("--")+1:]` idiom.
* `/tmp/blender/4.5/python/bin/python3.11` — `#!/bin/sh` + `exec /usr/bin/python3.11 "$@"`.

**CORRECTION TO `START_HERE.md`, rev 45:** it insists on a venv at `/tmp/bpyvenv`. That is not
required — installing `bpy` against the system `python3.11` works and the shim can `exec` that
directly. What *is* required is that the interpreter shim **`exec`s and is not a symlink**.

**Network:** `WebSearch` works. `WebFetch` and `curl` are 403 on every domain except
`raw.githubusercontent.com`.

### Build, verify, render

```bash
/tmp/blender/blender -b -P build.py                    # T1_SUB defaults to 2
T1_VERIFY=1 /tmp/blender/blender -b -P build.py        # -> "VERIFY: 0 fail, 0 warn"
T1_PREVIEW=hero34f,side,detail_f T1_PFX=r T1_RX=1400 T1_RY=960 T1_SAMP=56 \
  /tmp/blender/blender -b -P build.py
```

**CORRECTION TO THE REV-45 BRIEF §2: there is no view called `hero`.** It said
`T1_PREVIEW=hero,side,detail_f`; `studio.views()` has **no such key** and the run dies with
`KeyError: 'hero'` after a full build. The keys are `hero34f`, `hero34r`, `front34`, `side`, `front`,
`rear`, `detail_f`, `low34`, `topdown`, `playa`, `playa_ref`, `playa_w`, `counter`.

Useful env: `T1_SUB` (**2 is the guarded case**), `T1_SAMP`, `T1_RX`/`T1_RY`, `T1_PFX`, `T1_OUT`,
`T1_SAVE`, `T1_KEY`, `T1_SCENE=playa`, `T1_CLAY`, and the ablation switches `T1_NOBEVEL`,
`T1_NOCABFILL`, `T1_CATCH`, `T1_GRAIN`, `T1_BPILLAR`, `T1_SPEC`, `T1_VT`, plus rev 45's
`T1_HL_BEZEL`, `T1_HL_LENS_RG`, `T1_HL_REFL_RG`, `T1_HL_REFL_MET`, `T1_HL_BOWL`.

**A build at `T1_SUB=2` takes ~80–100 s. A 3200×2133 hero at 192 samples takes ~55 min. A 4800×3200
at 300 samples was quoted at 4½ hours and was killed — do not start one.** He has twice said *"Kill
it. Don't waste the computer."* Render small and often; render big once.

---

## §4. THE SPINE — READ THESE, IN THIS ORDER

1. **`LEDGER_rev45.md`** — the burn-down, four classes. **This is the spine.** §1 is the merge, §3 is
   the one finding rev 45 measured and refused to apply.
2. **`SPEC.md`** — ~9600 lines, §10.1 … §10.115. Each §10.x is a dated record of one revision's
   reasoning. **Sections are never deleted**; a retracted one gets a banner pointing at its
   retraction.
3. **`REFERENCE_FRAMES_rev45.md`** — what each of the nine frames can and cannot carry. **Read this
   before measuring anything off a photograph.**
4. **`PHOTOS_WANTED_rev45.md`** — the standing list, with *why each cannot be settled from what we
   hold*.
5. `START_HERE.md`, `README.md`, `STATE.md` — orientation, and see §3's correction.

---

## §5. WORK LIST FOR REV 46

**Read the split first.** Two items are blocked on the owner and everything else is not, so if no
answer has come back, start at W3 and do not sit waiting.

| | | |
|---|---|---|
| **BLOCKED on him** | W0 | Q5 (the sign board) and Q6 (the paint) — both are decisions, not measurements |
| **UNBLOCKED, in order** | W3 W4 W5 | the cab, fasteners, the ledger tail |
| **BLOCKED on a photograph** | W1 | the badge's drawing — needs the square-on frame |


**W0 — SEND HIM `rev45_ba.png` AND GET Q5 AND Q6 ANSWERED.** Two of rev 45's six questions are not
fixes, they are decisions only he can make, and both block real work:

* **Q6, the paint.** The red renders **3.5 σ too pale** against four of his own photographs, the
  albedo is **right**, and about half the excess is the white cyclorama reflecting in the paint —
  the same rig that is why the bus has no contact shadow (`optics-6`, open since rev 12). **These are
  one defect with two symptoms.** Softening the studio trades the catalogue-clean white background he
  supplied as the bar. `LEDGER_rev45.md` §3 has the numbers and the five-arm ablation.
* **Q5, the sign board.** The build paints a flower mural; every frame we hold shows a hand-chalked
  **blackboard** in a cream frame. Nobody has ever asked him which he wants.

**W1 — THE BADGE'S DRAWING, IF AND ONLY IF HE SENDS THE SQUARE-ON FRAME.** Rev 45 fixed why it
rendered as a clock (§10.110) and deliberately did **not** touch the spine. Reading stroke angles off
a three-quarter view needs the ring's axis ratio and the two available fits disagree by **10 %**,
which is several degrees on every angle — the whole size of the effect. **Do not try again without a
square-on frame.** Rev 44's `V half-angle` correction, merged this revision, used the one method that
survives: **vertical extents only**, per §10.107.2.

**~~W2 — FINDING 41, THE HEADLAMP APERTURE.~~ DONE, rev 45, §10.115.** Bored in step 3 with the
other apertures; `T1_HL_BOWL=0` restores the un-bored arm. Two things in it are worth reading before
you touch a lamp: the bore is **coupled to the reflector** (un-bored, the lens was backed by sheet
metal and read as a mid-grey disc — accidentally close to the photograph for the wrong reason), and
the bore's **depth and section are authored, not measured** — no frame we hold resolves them.

**W3 — THE CAB IS STILL CLASS 4.** Merged this revision, type-correct 1963 T1, **not measured**; no
frame resolves it. Related and open: the driving position is 622 mm seat-back-to-hub, ~150 mm more
reach than a T1 driver has.

**W4 — FASTENERS.** `probe_rev44_fidelity` counted rivet 0, bolt 0, screw 0, nut 0, latch 0. The four
cab-door hinge assemblies show the pattern: place hardware off a member that is **already guarded**,
never by eye. Next tranche by return per effort: rivets along the counter nosing and the gallows,
bumper bolts, hatch latches, drip-rail clips.

**W5 — REMAINING OPEN LEDGER ITEMS**, `LEDGER_rev45.md` §6: finding 2 (**no UV layout at all**,
~56 % self-overlap), 11 and 13 (both at the top of the photo list), 16 (**a trunk lid** — `grep -c
trunk` is 0 and 0), 21, 22 (**89 unverified findings in `AUDIT_RECOVERED.md`**), 26, 27, and rev 45's
new 38–41.

---

## §6. SETTLED — DO NOT RE-OPEN

* **The paint's *finish*.** §10.104.8 refuses it in writing: the reference is a factory-clean product
  render, this is a weathered 1963 working truck, and §4.3's chalky finish is **measured**. **The
  detail bar transfers; the finish does not.** Note carefully that rev 45's finding 38 is about the
  **studio**, not the finish, and does not re-open this.
* **Finding 29 — "the body red renders 2× too light."** Retracted; it was a unit error. The render
  reproduces its **own albedo** to 0.000. Rev 45's finding 38 is the question that retraction never
  asked: whether the albedo reproduces the **photograph**.
* **§10.100's door wrap.** Retracted by §10.102 and partially restored by §10.106 — the door's bottom
  rail is **flat over the arch** and drops around the **front** of the wheel well only.
* **The rear bumper was removed after the conversion**; the over-rider bar and posts were **withdrawn
  by the owner** at rev 37.
* **There is no fourth serving bay.**
* **The sign props' `LID_X1 + 0.16` / `LID_X0 - 0.16` is an INSET, not an outset.** `LID_X1` is the
  aft end at −1.0700 and `LID_X0` the forward one at +0.9640. **Two contexts have now "fixed" this
  and both were wrong.** Run the build before you believe the source.

---

## §7. THE RULES. EVERY ONE WAS EARNED BY A DEFECT.

1. **A claim in prose is not a guard** (§10.45). If it matters, assert it.
2. **A constant tuned against another constant must be EXPRESSED in terms of it** (§10.25).
3. **Read each probe's own summary line, never its exit code.**
4. **Never put a figure in an acceptance test unless you watched it print** (rev 13).
5. **Do not inherit a guard's rationale along with its shape** (rev 23).
6. **An ordinal fact licenses a SIGN, never a SHAPE** (§10.102.8).
7. **A leading question is not evidence, even when the answer is yes** (§10.102.8).
8. **A measurement's window is part of the measurement** (§10.106.6).
9. **A threshold-based "lowest X" trace is only valid if the feature's FAR SIDE is resolved**
   (§10.106.7).
10. **A detail you cannot see is not a detail** (§10.105.7).
11. **When a fix cannot be built at any tolerance, suspect the thing it is fixing** (§10.102.8).
12. **Add the guard in the same edit as the change.** Rev 45's emblem guard fired **twice** on its own
    change, at −15.11 mm and −3.59 mm, and both were real.
13. **Inventory the frames you already hold before asking the owner for a new one.**
14. **Prefer dimensionless measurements** (§10.106.3). Rev 45's whole paint finding is one: the red
    normalised to the cream **in the same frame**, which cancels exposure and illuminant together.
15. **Retract in the same revision you find the error**, in SPEC, in the ledger and to the owner.
16. **NEW, §10.110.8 — A PART MEASURED IN ISOLATION FROM WHAT IT IS FITTED TO IS NOT MEASURED.**
17. **NEW, §10.113.5 — A REVISION THAT IS NOT MERGED DID NOT HAPPEN.**
18. **NEW, §10.111.2 — A RATIO THAT IS RIGHT FOR THE WRONG REASON IS NOT A CONTROL.**
    `probe_rev45_nose`'s C4 tests the headlamp lens's **luminance** and it **passed at 0.432 while the
    aperture was rendering red**. C6, the chroma control, is what catches it. When you write a
    control, ask what it would still pass on.
19. **NEW, §10.115.4 — A CONTROL IS NOT FINISHED WHEN IT PASSES. IT IS FINISHED WHEN YOU HAVE WATCHED
    IT FAIL ON THE DEFECT.** C8 was written straight off the measurement that found finding 41 and
    **passed in both arms**, because that measurement predated §10.111.1's convex lens. Every ablation
    switch in this repo exists to make that check cheap: `T1_HL_BOWL=0`, `T1_HL_BEZEL=brass`,
    `T1_CATCH=0`, `T1_SPEC=0`. Use them on your own controls.
20. **NEW, §10.115.4 — RULE 10 CUTS BOTH WAYS.** A detail you cannot see is not a detail, **and a
    detail you looked at badly is not looked at.** The headlamp bore was very nearly reverted on a
    48-sample `T1_SUB=1` crop that read as "worse"; the A/B at 64 samples against the photograph
    overturned it outright.

---

## §8. THE STATE OF THE MACHINE AT HANDOFF

```
bootstrap.sh     ALL 10 PASS  (and from a bare container: rm -rf /tmp/blender first)
build            T1_SUB=2, clean
verify.py        VERIFY: 0 fail, 0 warn  at T1_SUB=1 and T1_SUB=2
audit.py         0 fail, 0 warn, 221 meshes
verify_clone.sh  ALL PASS on a clean tree
probes           probe_rev45_nose      8 checked, 0 FAILED  (C5 a KILL, red by design)
                 probe_rev44_lampmove  6 checked, 0 FAILED
branch           claude/project-improvement-id3a9o
SPEC             sec.10.1 .. sec.10.115
frames           9 tracked + 5 IMG_* uploads kept as provenance
```

**AND ONE THING THAT IS NOT DONE AND IS NOT A GEOMETRY ITEM.** At handoff this branch is **31
commits ahead of `origin/main` and 0 behind**. Nothing is stranded on any other branch — but the work
only reaches `main` through a pull request, and rev 45's whole §0 finding is what happens when it does
not. **Check `git rev-list --count origin/main..HEAD` before you start and again before you finish.**

**Delivered this revision:** `rev45_ba.png` — six questions, BEFORE | AFTER | PHOTOGRAPH.

**Go and read §0 again before you start.**
