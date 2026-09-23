# Art — HI02H11_L02_S01 «मात्राओं की रेल»

## Object art — YOUR artwork, 2026-09-21

You supplied three composite sheets (2172×724, already carrying real alpha). They were split into
one transparent PNG per object and now **replace** the previously generated art.

| key | word | what it is | size |
|---|---|---|---|
| `obj_jal` | जल | water splash | 604×466 |
| `obj_jaal` | जाल | net on a handle | 568×496 |
| `obj_bal` | बल | flexed arm | 506×484 |
| `obj_bil` | बिल | a bill / receipt with ₹ | 474×527 |
| `obj_kal` | कल | desk calendar | 537×535 |
| `obj_keel` | कील | nail | 389×553 |
| `obj_naak` | नाक | nose | 444×513 |
| `obj_din` | दिन | smiling sun | 591×589 |
| `obj_teer` | तीर | arrow | 640×499 |
| `assets/UI/ui_magnifier.webp` | — | magnifying glass, now the POEM_SEARCH lens | 420×385 |

### Two meaning changes that came with your art — worth a look

* **`obj_bil` is now a BILL/RECEIPT, not a burrow.** बिल carries both senses; the previous generated
  art was a burrow hole. Your sheet is a receipt with a ₹ field, so the emoji fallback moved 🕳️ → 🧾.
  The VO («अब बल में छोटी इ की मात्रा लगाने पर, बिल बनता है।») works for either reading.
* **`obj_bal` is now the flexed arm** you'd expect. It replaces the dumbbell I substituted earlier —
  that substitution only existed because the magenta keyer kept eating skin tones. Your art arrives
  with real alpha, so no keying was needed and the arm works.

### How the sheets were split

Column-gap detection worked on two sheets. The third (`net water nose,bal.png`) came back as one
blob — faint speckle bridged the gaps, and no alpha threshold separated the objects without eating
real edges; connected-component labelling also merged them because the objects abut. The column
**profile** showed true zero-ink columns at x=575, 1194, 1649, so that sheet was cut at those
measured valleys. Every cut was then autocropped, capped to 640px, and checked for a sane opaque
fraction (8–96%) before being written.

The three source sheets were removed from `assets/Images/` after splitting — left there they would
ship as unreferenced orphans and each is over 600KB.

### The magnifier's glass is off-centre

The artwork's glass sits at **67.9% across / 35.2% down, radius 25% of the width** — not the centre
of the image. `POEM_SEARCH`'s magnify hit-test reads through those coordinates, so the child is
looking through the glass rather than the handle. If the artwork is ever swapped, update `GLASS`
in the module.

## UI chrome — generated 2026-09-20 on your explicit instruction

The house rule is that engine chrome art is **COPIED from the assets kit, never model-generated**.
Neither of these exists in the kit, and you asked twice for the images to be generated, so they were
— flagging the deviation rather than making it silently. Both were keyed and eyeballed. (The magnifier that now
replaces the CSS-drawn lens came from your own sheet — see above.)

| file | size | what it is |
|---|---|---|
| `assets/UI/train_loco.webp` | 436×383, 14KB | the painted locomotive: red body, blue roof, yellow funnel, facing left with the coaches trailing right, as the mockups draw it. `TrainChrome` loads it first and still falls back to the inline SVG if it is ever removed. |
| `assets/UI/ui_ghost.webp` | 275×300, 13KB | the friendly ghost search-guide the SME asked for (deck page 18). Falls back to the 👻 glyph if removed. |

Two layout fixes went with them: the loco box is now 232×176 with `object-position:bottom`, because
`object-fit:contain` was letterboxing a portrait render into a landscape box and leaving the engine
floating above the rail; and the resting ghost's opacity went .4 → .62, since "fades slightly" should
still read as present.

**If your design team would rather supply their own**, both drop straight in at the same paths with
no code change.

## Cover-page train — your artwork, wired in 2026-09-21

`assets/GIFandVIDEO/train.gif` → `assets/UI/train_cover.webp`: **lossless**, 36 frames @50ms — identical to your source frame-for-frame, **1291KB → 883KB**. The artwork already carries a locomotive and three cream coach
panels, so the deck's "three matra boxes" are those panels — ा · ि · ी are placed on them and
appear one by one after the landing VO.

Placement is computed in JS from the image's **measured** box, not from CSS percentages: `.sg-art`
caps the image (`max-width:92%`, `max-height:250px`) and the wrap is a flex item, so wrap width
never equals image width and percentage placement drifted right by up to 7.7%. Panel centres,
measured off the artwork (634×182): **41.1% · 64.3% · 87.5%** across, 47.3% down. If you swap the
artwork for one with different coach positions, update `landing_hero.spots` in the card — no code
change needed.

## Train SFX — generated 2026-09-21 on request

There is no SFX generator in the kit (gen_tts is speech, gen_objects is pictures) and Gemini will
not produce a steam whistle, so these are synthesised from first principles with the stdlib:
accelerating filtered-noise chuffs for the approach, detuned sine partials with vibrato for the
whistle. Deterministic seed, so a re-run gives the same take. Both verified non-silent and
non-clipped. **Both go on the EAR-CHECK list — a human plays them before delivery.**

| id | length | used for |
|---|---|---|
| `sfx_train_arrive` | 2.05s | locomotive entry on the in-game train screens |
| `sfx_train_move` | 1.75s | the cover train chugging while it travels in |
| `sfx_whistle` | 1.35s | round / lesson completion |

## Still outstanding — three SFX (deck row X4)

Chrome, still copied-not-generated. Each id resolves at runtime and swaps to the real take with no
code change; until then the engine's procedural tone plays.

| id | used for |
|---|---|
| `sfx_sparkle` | a matra or word snapping into a coach |
| `sfx_chime` | a letter transforming (ज → जा) |
| `sfx_shake` | a wrong drop |

## obj_ladki regenerated — 2026-09-21

The girl on screen 7 (लड़की) is new art: an Indian school girl waving, flat vector with bold navy
outlines to match the rest of the object set, 330x640 PNG with real alpha. It replaces the earlier
generated girl (yellow top / blue skirt, 275x571).

Keyed off a flat green field. Two faults measured on the way, both relevant to any future object:

* Only **small** interior holes may be filled back after keying. Protecting every region that is
  not connected to the border welds the background showing through her braids into the hair.
* Distance to the measured background median is not enough on its own — it leaves the soft
  vignette between the backpack straps and the ground shadow the model draws despite the prompt.
  Green **dominance** is treated as background as well, and that test must run **last**, after the
  hole fill, or the fill re-opaques the green wedges at her shoulders.

## The train is now one artwork across the whole lesson — 2026-09-22

The cover's painted train is what pages 8-14 show as well. It ships as two files, both encoded from
`assets/Images/train.png` / `train_spritesheet.png` (the PNG sources stay on disk and out of the
deploy bundle):

| file | size | used |
|---|---|---|
| `assets/UI/train_still.webp` | 814KB, lossless, 2171x724 | the parked train on every train screen |
| `assets/UI/train_spritesheet.webp` | 1076KB, 6x6 cells of 634x182 | the travelling train, cover and interactive alike |

The still is **lossless on purpose**. Composited over white, lossless is pixel-exact; at q90, 4.6%
of pixels moved with a peak delta of 112. Flat vector art with hard edges and a hard alpha takes
visible damage from lossy WebP — the same finding as the cover GIF re-encode.

### Measurements anyone editing the train will need

* Part boundaries (couplings), found by scanning for columns whose ink is thin enough to be
  coupling-and-wheels only: **still px 17 / 650 / 1151 / 1642 / 2155**, **sheet px 2 / 188 / 336 /
  481 / 632**. The two agree to within 0.3% of the train's width.
* Ink boxes, which is what the two layers are aligned on (the still has more transparent padding
  than a sheet cell): still `x17 y48 w2138 h592`, sheet `x2 y3 w630 h175`.
* The cream panel a word sits on, per coach, in still px:
  `{cx 894, cy 341, 409x417}`, `{cx 1392, cy 340, 396x418}`, `{cx 1892, cy 339, 418x417}`.
* Coach fill colours, sampled from the artwork: yellow `#FDCD16`, green `#3FDC2D`, pink `#FC66A0`.
  The label plates use slightly darker versions so a border reads against cream.

`train_loco.webp` is no longer referenced by anything.

## Buttons — 2026-09-22 (final)

The `swiftpal_buttons` SVG set was tried and **reverted**; the files are not in the bundle. The
three pills are HI02H11_L01_S01's, drawn in CSS with their glyphs through `::after`:

| element | look |
|---|---|
| `#navBtn` | the pill, `→` at 52px |
| `#endBtn` | the pill, `→` at 52px |
| `#sgBtn` | the pill, `▶` at 30px, 64px tall, 186px min-width, bottom 40px |

No button carries text; the Hindi is on each as `aria-label`. The start button also has
`.sg-waiting` (grey and genuinely disabled while the cover greeting speaks) and `.idle-pulse`
(the pulse is earned after 5s of stillness, not run from first paint).

The hint bulb and the audio chip are unchanged live SVG — their wave arcs animate while a clip
plays, which a flat background would have killed.

## Your artwork, round two — 2026-09-23

Two more 2172x724 sheets, three objects each, already carrying real alpha. Both split cleanly on
true zero-ink columns — no speckle bridging this time, so no measured-valley fallback was needed.

| from | key | what | size |
|---|---|---|---|
| `haath, pin, neem.png` | `obj_haath` | open hand | 527x640 |
| | `obj_pin` | red push pin | 421x606 |
| | `obj_neem` | neem tree | 640x575 |
| `pari hiran magnifer.png` | `obj_pari` | fairy | 592x640 |
| | `obj_hiran` | fawn | 425x640 |
| | `assets/UI/ui_magnifier.webp` | magnifying glass | 640x617, lossless |

Every cut was autocropped, capped to 640px and checked for a sane opaque fraction (33-54%) before
being written. The six files they replace are kept in the session scratchpad, not deleted in place.

### The magnifier moved its glass, so POEM_SEARCH was re-measured

The new lens sits **up and to the right** of the handle, where the old one sat differently.
`GLASS` in POEM_SEARCH is now `{ x: 0.656, y: 0.391, r: 0.280 }` (was `{0.679, 0.352, 0.25}`).

It was measured off the **gold bezel**, not the glass. The lens interior is nearly white, so a
colour mask on it catches only the rim highlight — 9% fill of its own bounding box, against the
~79% a real disc would give. The bezel is a solid ring, and its largest connected blob gives the
circle directly: centre (420, 241) of 640x617, outer radius 212px, inner radius 184px. `r` is the
**inner** radius, so the hit-test stops where the glass does rather than reaching onto the frame.

Verified by placing the glass centre on each of the first five poem words in turn: the word aimed
at is under the glass every time. It also catches 2-4 neighbours, which is unchanged behaviour —
the glass is simply wider than the word spacing in this poem.

`.ps-lens` went from 196x180 to 196x189 to match the new artwork's aspect.

### The source sheets stay on disk, out of the bundle

Both strips are listed in `.vercelignore`. They are the source of the cuts and worth keeping, but
the page never requests them and each is about 1.4MB.
