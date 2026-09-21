# Art — HI02H11_L02_S01 «मात्राओं की रेल»

Regenerated 2026-09-17 after applying the SME deck **and generating the art**.

## Object art — all 10 produced

Flat-vector, transparent, autocropped, magenta-keyed. None is pink (house rule).
Every one was eyeballed on a contact sheet (`_review_shots/_art_contact_sheet.png`).

| key | size | what it is |
|---|---|---|
| `obj_bal.png` | 578×313 | a blue dumbbell — बल (strength) |
| `obj_bil.png` | 410×296 | an earth mound with a burrow hole — बिल |
| `obj_gati.png` | 273×367 | a boy running — गति (motion) |
| `obj_jaal.png` | 350×580 | a round mesh net on a wooden handle — जाल |
| `obj_jal.png` | 442×225 | a shallow puddle of blue water with a droplet — जल |
| `obj_kal.png` | 464×448 | a wall calendar — कल |
| `obj_keel.png` | 220×541 | a grey metal nail — कील |
| `obj_ladki.png` | 275×571 | a girl in a yellow top and blue skirt — लड़की |
| `obj_matka.png` | 440×500 | a terracotta clay water pot — मटका |
| `obj_pari.png` | 486×490 | a fairy in a teal dress with golden wings — परी |

### Two notes on these

* **बल is drawn as a dumbbell, not a flexed arm.** The arm was generated twice and refused twice by
  the keyer's hollow-object guard: skin tone sits ~82–100 from both the magenta and the green
  chroma, i.e. inside the halo radius, so the keyer ate the arm. A saturated subject keys cleanly.
  बल is abstract either way — say the word if you would rather have the arm and I will hand-key it.
* **परी wears teal, not pink.** A pink fairy fights the magenta key (the house rule's "keep objects
  never pink"). Your mockup draws her in pink — easy to change if you want it, on a green chroma.

## UI chrome — generated 2026-09-20 on your explicit instruction

The house rule is that engine chrome art is **COPIED from the assets kit, never model-generated**.
Neither of these exists in the kit, and you asked twice for the images to be generated, so they were
— flagging the deviation rather than making it silently. Both were keyed, eyeballed and are the only
reason the game now contains **zero emoji fallbacks**.

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

`assets/GIFandVIDEO/train.gif` → `assets/UI/train_cover.webp`: 18 frames @100ms, i.e. the **same
1.8s loop**, **1291KB → 287KB**. The artwork already carries a locomotive and three cream coach
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
| `sfx_train_arrive` | 2.05s | locomotive entry — every train screen and the cover page |
| `sfx_whistle` | 1.35s | round / lesson completion |

## Still outstanding — three SFX (deck row X4)

Chrome, and still copied-not-generated. Each id already resolves at runtime and swaps to the real
take with no code change; until then the engine's procedural tone plays.

| id | used for |
|---|---|
| `sfx_sparkle` | a matra or word snapping into a coach |
| `sfx_chime` | a letter transforming (ज → जा) |
| `sfx_shake` | a wrong drop |
