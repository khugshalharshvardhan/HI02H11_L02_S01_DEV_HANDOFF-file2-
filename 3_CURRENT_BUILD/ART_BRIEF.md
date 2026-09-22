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
