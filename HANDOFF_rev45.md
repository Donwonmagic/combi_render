# HANDOFF — rev 45

`NEXT_CONTEXT_PROMPT_rev46.md` is what you execute from. This is the narrative: what rev 45 did, what
it got wrong on the way, and what it deliberately refused.

---

## §1. THE ONE-LINE VERSION

Rev 45 opened on a brief asking why the owner kept reporting the same defects while every guard
stayed green. **The answer was that seventeen commits of rev-44/44b work had never been merged.** It
merged them, then found and fixed four defects nobody had seen — all four by the same method: *render
it, crop it, and look at it.* Then he reported four more, and rev 45 measured all four before handing
over.

---

## §2. THE MERGE, WHICH IS THE REAL FINDING

`origin/claude/tacombi-combi-rev-44-h4ipmg` sat **seventeen commits** above the point where PR #2 was
merged. Neither `origin/main` nor the branch rev 45 started from had any of them. Missing from the
mainline: **`SPEC.md` §10.102–§10.109** (632 lines, all eight rev-44b sections), the §10.100 door-wrap
retraction, §10.107's stroke ends, §10.108's prop fix, `cab_fitout` and `door_hinges` (the whole cab
interior), `cabin_fill`, `round_edges` on all 42 materials, the roundel's 13.5 mm mounting plane, the
hubcap red, the bumper/door overlap, and **three of the four Nolita reference photographs**.

`SPEC.md` on `main` ended at **§10.101**.

That last item made brief item W1 **unexecutable as written** — its entire method was specified
against `ref_nolita_front34.jpg`, a file that was not in the tree. Rev 45 had already recovered those
frames from the owner's own re-upload before finding out why they were missing; the two
identifications it published as *unproven* then came back **md5-identical** to rev 44b's, three for
three. The ordering matters and is recorded in `REFERENCE_FRAMES_rev45.md`.

> **§10.113.5 — A REVISION THAT IS NOT MERGED DID NOT HAPPEN.** `bootstrap.sh` now enforces it: it
> fails if any remote branch carries commits `HEAD` does not have.

---

## §3. WHAT SHIPPED

| | SPEC | what it was |
|---|---|---|
| **The nose badge was a flat plate on a curved nose** | §10.110 | Upper half 32 mm proud, lower half 0.3 mm *inside* the sheet metal. The whole W was buried; it rendered as a **clock face**. `t1_core.drape_x`; front faces now 6.96–15.10 mm proud. **Rev 44 found the same thing independently from the other direction.** |
| **The headlamp lens was dished the wrong way round** | §10.111 | Concave, its centre 10.1 mm *inside* the nose. Turned convex. Lens (R−B)/cream **+0.571 → +0.082** against −0.024 photographed. |
| **The bezel was brass** | §10.111.3 | Retired to chrome. Rev 10's reading is called **uncontrolled**, not wrong — its five neutrals contain no small mirror-finish torus ringed by a warm panel. `T1_HL_BEZEL=brass` renders the retired arm. |
| **"100 % Calidad" rendered peach** | §10.112 | The gradient's 0.42 bias started the ramp 42 % along, so **nothing in the texture was the RED the generator declares nine lines above.** Bias → 0. |
| **The sign props stood in the hole** | §10.113 | Both feet inside the roof aperture. Rev 44b found it independently and **its patch is the one that ships** — it walks `roof_z` to the roof's own edge where rev 45 typed an offset. |
| **No headlamp aperture in the nose** | §10.115 | The lamp was fitted into unbroken sheet metal. Bored in step 3 with the other apertures. |
| **`optics-6` — the vehicle floated, open since rev 12** | §10.116 | G1 tight contact **0.9756 → 0.8729** against a photographed 0.8713; backdrop unmoved. Two levers refuted first. |
| **The paint, instrumented** | §10.117 | And it is **one** finding, not three. |

Plus `bootstrap.sh` — one command from a bare container to a proven tree — and three new probes that
**project 3-D landmarks through the render camera instead of typing crop boxes**.

---

## §4. WHAT REV 45 GOT WRONG, AND THIS IS THE PART WORTH READING

**Its three new probes were wrong eight times before they were right.** Every error produced a
plausible number that would have been published had nobody checked.

* A ground sample kept "neutral" pixels on the reasoning that the body is not neutral. **The cream
  renders (192,192,188).** It was measuring the vehicle's flank and calling it ground: G1 = 0.8639.
* **Three separate kill controls** sampled off-screen, returned `<no sample>`, and **passed**.
* A backdrop control read the frame's top two corners and reported **"255.00, PURE WHITE"** for a
  frame with a hard horizon across it — the horizon sits 18 % down; the corners are above it.
* A window ran 0.5–3.5 tyre-widths below the contact patch when **the whole shadow lives in the first
  0.35**. It reported "it floats" while a shadow was plainly in the profile.
* **Three flank landmarks out of three** were behind a decal, the bobble fringe and the hubcap's own
  rim. `world_to_camera_view` maps a point to a pixel whether or not the point can be *seen*.
* `probe_rev45_nose`'s C8 was written straight off the measurement that found finding 41 and
  **passed in both arms** — the measurement predated the convex-lens fix one section earlier.
* And rev 45 bumped a `verify_clone.sh` count to 33 without watching it print. It was 31.

It also **walked into a trap rev 44b had already documented**: the sign props' `LID_X1 + 0.16` reads
as an outset and is an inset. Two contexts, same wrong conclusion, both stopped by running the build.

Three rules came out of it — §10.115.4, §10.116.6, §10.111.2 — and they are §8 items 18–20 of the
rev-46 brief.

---

## §5. WHAT REV 45 REFUSED, AND WHY

* **The badge's stroke ANGLES.** De-foreshortening a three-quarter view of a circle needs the ring's
  axis ratio and the two available fits disagree by **10 %**, which is several degrees on every
  angle. **That refusal was right for angles and wrong to stop there** — vertical extents need no
  axis ratio, and rev 45 came back and did that measurement before handing over. It is W2.
* **The paint.** 3.5 σ too pale, albedo right, cause is the studio — and softening the studio trades
  the catalogue-clean white background he supplied as the bar. **Instrumented and deliberately not
  gated**: gating on a number whose fix has not been sanctioned turns a question into a fait accompli.
* **`T1_CATCH=0`.** Re-tested with an instrument and refused again; rev 12 was right.
* **A horizontal luminance profile across the nose**, for W4's plan curvature. The render and
  photograph boxes were not comparable and the number would have been about nothing. Thrown away
  rather than published; the method that fixes it is in W4.

---

## §6. HIS FOUR NEW REPORTS, MEASURED BEFORE HANDOVER

He wrote: *"the 100% calidad off center, the vw logo wrong, señor Tacombi still isn't clearer, the
nose of the car is too flat."*

**All four confirmed.** Two carry a trap: the Calidad defect is *not* the one rev 44 closed (that was
the panel's placement on the vehicle; this is the type's placement inside the decal), and the nose
defect is *not* `V_POW` (that drives the painted break line, not the sheet metal). Numbers, methods
and traps are §5 of the rev-46 brief.

The badge is his **fourth** report in four revisions, and rev 45's own vertical-only measurement says
he is right by **27.7 mm** on the one axis nobody had checked.

> **Rev 46's new rule, §8 item 21: HIS REPEAT IS A MEASUREMENT.** When he reports the same thing
> twice, the prior closure was wrong or incomplete. Go and find the axis nobody looked at.

---

## §7. STATE

```
bootstrap.sh --guards   16 PASS
T1_SUB=1 / T1_SUB=2     VERIFY 0 fail, 0 warn
audit.py                0 fail, 0 warn, 221 meshes
verify_clone.sh         ALL 69 PASS on a clean tree
probes                  nose 8/0   ground 4/0   paint 4/0   lampmove 6/0
SPEC                    sec.10.1 .. sec.10.117
branch                  claude/project-improvement-id3a9o, 35 ahead of origin/main, 0 behind
```

**The work reaches `main` only through a pull request.** Given §2, that sentence is the whole point.
