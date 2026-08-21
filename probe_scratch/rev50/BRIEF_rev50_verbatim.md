# Rev 50 operator brief -- verbatim, as received

Please act as my expert. You are picking up a 49-revision project mid-stream,
not starting one. Do these six things in this order, and do not skip ahead.

1. Get the repo, then MEASURE which branch to work from. Do not transcribe one.
   [clone/unshallow/fetch commands]
   THE BRANCH INSTRUCTION HAS NOW BEEN STALE FOUR REVISIONS RUNNING. Rev 47's
   named one with an ahead-count of 5; the real count was 1. Rev 48's named one
   that was 0 ahead and 1 BEHIND main. Rev 49's designated branch was created
   at main itself -- 0 ahead -- while the real work sat 15 ahead somewhere
   else, so obeying it would have thrown away the whole of rev 48.
   [the for-loop ahead/behind measurement]
   git diff --name-only HEAD...origin/main    # <- I push photos straight here
   Work from whichever ref is furthest ahead of main with nothing behind it. If
   your HEAD is an ANCESTOR of it, fast-forward -- nothing is lost. I upload
   reference photographs to main from the web UI, mid-revision, without telling
   you. Re-run that diff EVERY session, not once.
   Then: ./bootstrap.sh must end ALL 10 PASS, and ./verify_clone.sh ALL 113
   PASS -- 113 now, not 110. If a line fails, STOP and tell me the failing line
   with its actual value. Do not edit the script to make it pass -- a failing
   check is a finding, not a broken instrument. Note verify_clone needs a CLEAN
   tree; commit first, then verify.
   AND NOTE: bootstrap's row 10 is "no branch carries work HEAD does not have".
   It caught the stale branch at rev 49 on its own. If that row is green you
   are on the right ref. Believe it over any sentence in the brief.

2. Read NEXT_CONTEXT_PROMPT_rev50.md IN FULL before you touch anything else.
   Then SURVEY_rev49_photoreal.md, then LEDGER_rev49.md, then LEDGER_rev48.md.
   Start to finish, not by grep. Between them they tell you what is settled,
   what is deliberately left failing, what was RETRACTED, and what not to touch.

3. THERE ARE THREE ARTWORK STATES IN THE REFERENCE SET, NOT TWO BUSES, AND THIS
   IS THE EASIEST WAY TO WASTE A REVISION. A red bus in its CURRENT artwork
   (ref_side, ref_rear34) -- that is the vehicle we are recreating. A GREEN bus
   (ref_workshop, IMG_2073) -- geometry only. And the SAME RED BUS IN AN
   EARLIER STATE (the four "nolita" frames): plain red flank, TACOMBI.COM, no
   scrollwork, no Senor Tacombi script, no Calidad burst at all. Geometry
   transfers between all of them; PAINT AND ARTWORK DO NOT. Rev 47 measured a
   decal off the green bus and applied it to the red one and nothing caught it
   for a revision. Checking "which bus" is NOT enough -- check which STATE.
   Also: five of the reference files are byte-identical duplicates of five
   others. There are NINE distinct frames, not fifteen. Do not count a duplicate
   as corroboration.

4. Grade the brief before you trust it -- AND KNOW THAT IT CUTS BOTH WAYS. Rev
   40 refused its brief's item 1; rev 41 refused item 3; rev 46 retracted two
   of its own numbers; rev 47 caught its branch instruction stale and inverted;
   rev 48 found its brief wrong seven times; REV 49 FOUND ITS BRIEF WRONG TEN
   TIMES. Where the brief and the machine disagree, THE MACHINE IS RIGHT -- say
   so and correct the brief in the same revision. Put an agent on the brief
   first whose only job is to refute it, AND DO NOT CLOSE UNTIL IT REPORTS.
   BUT: rev 49 also REFUSED a job it should have built, because the record had
   inherited a retirement from the wrong object for four revisions, and I had
   to correct it. So the machine outranks the prose -- and I outrank the
   record. If something in the record looks like it settles a question, check
   WHICH OBJECT the ruling was actually about before you rely on it.

5. Use your orchestration hard -- I want large, complex workflows, and I want
   this vehicle finished. One rule survives every box: do NOT fan out Blender,
   it is CPU-bound and two instances make both slower. Run renders SEQUENTIALLY
   from one script in the background and analyse in the foreground. Fan out
   everything that is not a render -- measuring frames, cross-checking the
   record, and adversarial verifiers instructed to REFUTE a finding before it
   ships. Subagent concurrency on this box is 2, so prefer fewer, deeper agents
   over many shallow ones.
   And read section 8 of the brief before you build any instrument. This
   project measures beautifully and its instruments keep being wrong -- rev 46
   caught five, rev 47 four, rev 48 four, rev 49 four and THREE OF THOSE WERE
   ITS OWN, including a statistic that was an algebraic identity about its own
   threshold, published as a fact about my photograph. Every one produced a
   plausible number that would have been published.

6. Then work section 6 of the brief in order and tell me what you find.
   Section 6 is not a sketch this time. At the close of rev 49 I asked for a
   large coordinated workflow to establish what remains before photorealism,
   and it ran 19 agents over five hours: twelve subsystem surveys, five
   adversarial refuters, a completeness critic and one ranked synthesis. 78
   findings, 15 of them blocking. It is all in SURVEY_rev49_photoreal.md, with
   every finding carrying its evidence, its ceiling and its own attempted
   self-refutation -- and 130+ ALREADY RIGHT items so you do not spend a
   revision re-litigating settled ground. READ IT BEFORE ITEM 1.
   Its headline is worth having in your head before you start: THE GEOMETRY IS
   NOW CLOSER THAN THE PRESENTATION. The shape errors left are mostly tens of
   millimetres on parts nobody looks at twice. What makes every frame read as a
   render is that the bus barely darkens the ground it stands on, its paint
   delivers chalk where my photographs show polished enamel, every duplicated
   part is a bit-identical clone carrying the same dirt, and every shiny
   surface has a white void to reflect.

The standard, in my words, and it is not rhetorical: we are recreating a photo
realistic version of that exact bus, and any single measurement off is
unacceptable. That is per-measurement, not on average. A model right in ninety
places and wrong in one is not 99% done, because I will look straight at the one.

The level of detail I want is bus_model_ref.JPG -- that is a SCHOOL BUS and it
is NOT my vehicle. It is a FIDELITY BAR only: crisp edges, and small features
built as real geometry with depth rather than painted on. Use the clarity in
ref_workshop.jpg the same way. Take nothing about shape, paint or proportion
from either.

How I want you to work: ground in the reference, build, adversarially audit,
iterate. Never build before grounding. Never call it done off self-review.
Report the measurement against the reference WITH ITS CEILING, never a
self-assigned score. Do not tell me anything is ready -- tell me what is fixed,
what is still wrong, and what you measured. Keep visible cadence on long work.

RENDER IT, CROP IT, AND LOOK AT IT, before and after every change. At rev 48
the trunk lid opened INWARDS through a clean VERIFY and 95 green checks. At rev
49 the engine bay had no material at all and rendered as the brightest thing on
the tail; then a bay lining sat 2 mm proud of the shut lid and painted the tail
charcoal; then a board I built had its foot 120 mm inside the roof. All four
through VERIFY: 0 fail, 0 warn. EVERY ONE WAS FOUND BY LOOKING AT A CROP.

And when you need something from me, ask as MULTIPLE CHOICE with the reference
material attached: one crop, one mark, one sentence. If I do not understand the
question, the figure is the defect, not me. I have never stood in the bus -- do
not ask me what the real vehicle looks like. Ask me what a PHOTOGRAPH shows.

What is waiting on me:
  - W6 needs asking AGAIN, and rev 49 found out why I kept answering a
    different question: the trade I was being offered was not real. My clean
    white background is a compositor constant and NOTHING done to the lights
    can dirty it -- that was measured, the difference was 0.000. I had also
    already retired the pure-white backdrop lock myself at rev 15. Then the
    lever turned out not to be "soften the studio" at all: growing the source
    in the axis that matters moves the red by 0.003. The only thing that works
    REPLACES the directional rig with a diffuse dome and costs 29% of the
    brightness. I chose "re-light to match my photographs" without knowing
    that. Put it to me again with the two frames side by side.
  - The photographs. I said neither was possible right now and that still
    stands, so do not queue up asking me again -- but PHOTOS_WANTED_rev49.md
    now ranks them by exactly what each one unblocks, and the top item CHANGED.
    It is no longer the open tail (I have ruled that lid shut, so nothing in
    that bay shows). It is the TAIL BOARD'S FOOTING, which SPEC 10.28 has
    required since rev 12 and which nobody has ever actually asked me for.
