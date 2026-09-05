# PICKUP — rev 76. READ THIS IF YOU WERE TOLD TO LOOK FOR "THE MISSING CONTENT".

**Branch `claude/rev-75-pickup-po0rs3`. Everything named here is COMMITTED AND PUSHED.**
Verified on a cold clone: `bootstrap.sh` **ALL 10 PASS**, `verify_clone.sh` **ALL 437 PASS**
(5 rows correctly SKIPPING because `out/` does not exist on a clone — that is right, not a fault).

---
## THE CONTENT THAT WAS NEARLY LOST, AND WHERE IT IS NOW

A 92-agent workflow (92/92 complete, 11.2M subagent tokens) produced the rev-76 design program.
**Its output lived only in `~/.claude/` and `/tmp` — outside the repository — and the earlier draft
of `DESIGN_PROGRAM_rev76.md` pointed at that path.** That storage died once mid-session already.
**It is now in the repo. These four files are CARRIERS (rule 16). Do not compact them.**

| file | what it holds |
|---|---|
| **`DESIGN_PROGRAM_rev76.md`** | the program: spine, the 12 critic findings, shortlist, critical path, first deliverable, owner questions, and **§9 the EXPANSION BRIEF — your actual job** |
| **`WORKFLOW_rev76_CONCEPTS.md`** | **all 78 concepts IN FULL** — the image, emotional claim, formats, why-not-derivative, production notes, model work required, screener note. *(the program file carries TITLES ONLY)* |
| **`WORKFLOW_rev76_SYNTHESIS.md`** | the executive synthesis, the **6 AMPLIFIED concepts**, and the completeness critique verbatim |
| **`WORKFLOW_rev76_output.json`** | the complete structured return: **7 grounding reports**, **7 expert discipline plans**, 78 concepts, **36 audit verdicts** with every improvement |

⚠⚠ **THE SYNTHESIS AND THE AMPLIFIED CONCEPTS WERE NEVER READ BY THE CONTEXT THAT WROTE
`DESIGN_PROGRAM_rev76.md`.** It acted on the critique and skipped those two. **So
`WORKFLOW_rev76_SYNTHESIS.md` may carry material the program file does not reflect. READ IT FIRST.**

**The grounding reports in the JSON are the most under-used thing here** — seven researchers on the
pipeline, the motif inventory, the owner's rulings, the fidelity ceilings, art direction off the
reference frames, the market, and prior art. They contain measured findings that appear nowhere else.

---
## THREE THINGS THAT WILL BITE YOU IF YOU DO NOT READ THEM

1. ⚠ **DO NOT PRINT `109.5 / 129.5` PILLARS AS FACT.** Rev 76 published it and retracted it.
   The asymmetry is **20.0 mm against a 30.0 mm σ = 0.67σ** — three equal pillars sit inside the
   measurement. `DESIGN_PROGRAM_rev76.md` §0 has the arithmetic and the two ways out.
2. **THE SPINE WAS RECOVERED FROM A LOST SENTENCE.** `NEXT_CONTEXT_PROMPT_rev39.md` §7, the owner's
   own words: *"cartoon with rendered depth — **vector line and flat colour, shading and occlusion
   sampled from the 3D asset**."* The italic half was dropped between rev 39 and rev 43 and was
   absent from every carrier since. **It is a render recipe, and it is the technical spine.**
3. **VERIFIED, NOT INHERITED** (re-check anything else before you trust it):
   * **No line-extraction capability exists** — the one grep hit is `use_pass_object_index` in an
     unrelated rev-24 counter probe. Grease Pencil Line Art → SVG is the route; nothing is built.
   * **`side` ortho is NOT clipped** (5.90 → 4.0563 m); **`front`/`rear` ARE** (3.55 → 2.4406 m
     against `bbox top 3.132`). An agent claimed this "blocks every elevation" — it does not block
     the one the top concepts need.
   * **`T1_ALPHA` has never been exercised** — zero ledgers mention it, every frame in `out/` is
     mode RGB, and `deliver.py` correctly refuses them.

---
## YOUR JOB IS §9, NOT THE SHORTLIST

> *[owner]* **"I don't want to be tied down by current ideas, I want fresh ones, good ones, and lots
> of em"** · **"turning up all quality knobs before execution"**

**GROW THE IDEAS BEFORE EXECUTING ANY OF THEM.** The completeness critic found the range is not real
(11 concepts, one aesthetic) and that a taqueria programme contains **no food and no people**.
§9.1 lists **13 missing registers** as directorial slots and 4 promotions off the bench.
§9.2 names the knobs: **xhigh/max effort on DREAM and AMPLIFY only**, **a third of directors with NO
assigned territory**, a fourth audit lens asking only *"has the improvement removed what made this
dangerous?"*, and **two completeness critics run before the synthesis as well as after.**

**AND SHIP SOMETHING HE CAN LOOK AT.** §6 Session A — `SHEET 3 OF 4: NOT ISSUED` — needs no line
pass, no render, no alpha and no geometry. **Nobody in this programme has looked at a single
rendered line. Every concept is still a description.**
