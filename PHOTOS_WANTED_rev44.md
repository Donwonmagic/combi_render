# PHOTOGRAPHS WANTED — rev 44

**You offered:** *"we can get anything, why don't you give me the links and I will save the photos
and add them to the repo."* This is that list.

**READ THIS FIRST — WHAT I COULD AND COULD NOT DO.** This environment can run **WebSearch** but
**`WebFetch` and `curl` are both blocked by the network egress proxy** (403 on every domain tried,
including `download.blender.org`, `tacombi.com` and `flickr.com`). So **I found these links by
search and I have NOT opened a single one.** I cannot confirm what any page actually shows. Treat
every URL below as *a lead worth ten seconds of your time*, not as a verified source. Rev 43's
environment could not even search, so this is new — but it stops well short of me seeing anything.

**The one thing that matters more than any link:** if you have your own photographs, or can walk up
to the bus, **that beats everything here.** Four of the five gaps below are gaps no stock photo will
close, because they need a specific angle and something of known size in shot.

---

## PART 1 — WHAT THE MODEL ACTUALLY NEEDS, IN PRIORITY ORDER

Each entry says what is open, what a **usable** frame must contain, and — importantly — **what makes
a frame useless**, because we have been burned by unusable frames before.

### 1. THE OFF SIDE (the right-hand flank). **Highest value. Nothing else comes close.**

* **What is open:** the off flank sits at **804.9 mm**, graded **E**, and has never been adjudicated
  (ledger finding 13). More seriously, **we do not know what is painted on that side.** The model
  currently carries a de-mirrored variant of the near-side art on the assumption that it is *not*
  a mirror — an assumption made at rev 10 and never tested against a photograph.
* **A usable frame:** the right-hand side of the bus, roughly square-on, whole vehicle in shot,
  wheels visible.
* **What makes it useless:** a three-quarter view. We already have three-quarter views. The whole
  point is a flat-on flank.
* **If the art on that side turns out to be a mirror of the near side, that is a one-line change
  and it closes a fourteen-revision assumption.**

### 2. ANYTHING THAT SETTLES THE ABSOLUTE ROOF HEIGHT. **The most embarrassing gap in the project.**

* **What is open:** the model reads **1.9835 m** at the rear axle. **That number rests on nothing.**
  `H_ROOF` was retired as an accuracy target at rev 22 and never replaced. The build prints a
  paragraph on every run explaining that the figure is unsupported. It has been open since rev 22.
* **A usable frame:** the bus with **a person standing beside it**, or in a doorway of known height,
  or beside anything whose size you can tell me. Straight-on side view is best.
* **Simplest possible fix:** stand next to it, have someone take one photo, tell me your height.
  **That single frame closes an eleven-revision hole.**
* **What makes it useless:** a low angle looking up, or the roof lids open. The lids are open in
  both frames we currently hold, which is *why* the roof surface is unmeasurable from them.

### 3. HEAD-ON REAR — and specifically **THE TRUNK LID**.

* **What is open:** you have referred to a **trunk lid** at the tail. `grep -c trunk` over the build
  returns **0 and 0** — it does not exist in the model. Two independent audit dimensions (roof and
  tail) found the same thing. There is also a question about the **main lid being raked the wrong
  way** — the model leans the mural board *away* from the counter at 104°.
* **A usable frame:** straight on the back of the bus, lid closed if that is possible, and a second
  with it open.
* **Context that may matter:** press reports say the **engine was scrapped and the transmission
  sold**, so whatever is behind that lid is not a stock engine bay and I should not model it as one.

### 4. THE DOOR, FULL OUTLINE, **WITH THE ART ON IT**.

* **What is open:** you answered rev 44's question — the art **keeps its drawn scale and extends
  down** to reach the door's bottom edge. Good; that is now decided and I have written it in.
  **But no frame we hold shows the door's whole outline with art on it.** The one frame that shows
  the full outline (`ref_nolita_doorshut.jpg`) carries no art at all.
* **Why I still want it:** the door's added depth is **not a uniform band**. It is **272 mm at the
  rear corner, 387 mm at the front, and 1.8 mm over the front wheel arch** — two corner lobes. I now
  have to *draw new art* into those two lobes, and I would much rather copy what is there than
  invent it.
* **A usable frame:** the sliding door, square-on, whole door in shot including where it meets the
  sill, art visible.

### 5. NOLITA, ANY ANGLE.

* **What is open:** Nolita material was authorised for geometry at **rev 15** and in **twenty-nine
  revisions not one frame has been measured** (ledger finding 14). We hold exactly one Nolita frame.
* You have confirmed it is the **same physical vehicle**, so its geometry is admissible — which
  makes Nolita frames genuinely useful, not just decorative.
* **The bus is indoors and static there**, so these should be the easiest photographs on this list
  to obtain, and they can be taken deliberately rather than found.

---

## PART 2 — THE LINKS

**All found by search. None opened. None verified.** Ranked by how likely I think they are to carry
something we do not already have.

| # | link | why |
|---|---|---|
| 1 | https://www.flickr.com/photos/randall-mexico/3440153780 | Titled *"VW Tacombi — a VW Bus (commonly known as COMBIS in Mexico)"*. A Flickr original may be **much higher resolution** than anything we hold, and Flickr pages usually carry date and location. **Try this one first.** |
| 2 | https://www.tripadvisor.com/LocationPhotoDirectLink-g60763-d2436362-i134660667-Tacombi_Nolita-New_York_City_New_York.html | Titled *"VW Van Inside Tacombi"* — a Nolita interior. Directly serves gap 5. |
| 3 | https://www.yelp.com/biz/tacombi-nolita-new-york-3 | Listed as **1313 photos**. Customer photographs of an indoor, static bus from every angle in the room — the single most likely source of an **off-side** view (gap 1) and of **someone standing next to it** (gap 2). |
| 4 | https://www.tripadvisor.com/ShowTopic-g150812-i23-k4520239-VW_Taco_Van-Playa_del_Carmen_Yucatan_Peninsula.html | A Playa del Carmen forum thread *"VW Taco Van??"* — likely **Playa-era** photographs, i.e. the same era as the two frames we already hold. |
| 5 | https://www.alamy.com/stock-photo-interior-of-tacombi-a-mexican-street-food-eatery-in-nolita-which-serves-93710119.html | Stock photo of the Nolita interior. Watermarked previews are usually still large enough to measure geometry from. |
| 6 | https://www.youtube.com/watch?v=kiW5eOrk5vU | *"Tacos, a VW Bus and a Dream — The Story of Tacombi Founder Dario Wolos."* **Video may be the best source on this list:** it will pan around the vehicle, which means the off side and the rear both go past the camera. A paused frame is a photograph. |
| 7 | https://www.tacombi.com/our-story | The company's own history page. Most likely to carry a clean, high-resolution **archival** shot of the bus. |
| 8 | https://www.pinterest.com/pin/vw-tacombi--472455817137393820/ | Pinterest re-host of a "VW Tacombi" image; may lead back to a larger original. |

---

## PART 3 — HOW TO SAVE THEM SO THEY ARE USABLE

1. **Do not crop, do not rotate, do not resize.** `ref_source.jpeg` is **246 × 197 px**, and that
   single fact is why a 32 mm finding could not be settled from it (SPEC §10.22, corrected rev 44).
   Resolution is the binding constraint on almost everything here — **always take the largest
   version offered.**
2. **Name them plainly** — `ref_offside.jpg`, `ref_rear_headon.jpg`, `ref_roofheight.jpg`,
   `ref_door_art.jpg`, `ref_nolita_2.jpg`. I will re-tag them properly.
3. **Tell me where each came from and, if you know, roughly when.** Era now has to be read from the
   scene rather than the paint — see SPEC §7.2, where I got exactly this wrong and retracted it in
   the same revision. **Livery colour is not a date.**
4. **Check the repo before adding.** Rev 43 was handed a frame that was called new evidence and
   correlated **1.000** with `ref_source.jpeg`, which was already tracked. No harm done, but two
   findings came out of chasing it.

---

## PART 4 — WHAT I WILL NOT ASK YOU FOR AGAIN

Settled, and I will stop raising them: the over-rider assembly, the signboard, region 3 (the
counter's front face), the ten flower heads, tyre diameter, the counter slab, break-to-sill, the
Z-ladder's gate, and the door outline's arch clearance. And, as of this revision: whether it is one
vehicle (**it is**), whether the door art stretches (**it does not**), and whether the workshop
frame may be used for letterforms (**it may, geometry only**).
