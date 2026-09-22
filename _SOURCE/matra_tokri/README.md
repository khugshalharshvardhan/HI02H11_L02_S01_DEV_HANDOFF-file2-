# मात्रा टोकरी — Matra Tokri (BV, G1)

Catch-the-matra-word arcade. Words drift down out of the sky; the child slides a
basket along the grass and collects only the words carrying the matra being asked
for. Three rounds, five words each.

| # | Matra | VO prompt | Words |
|---|---|---|---|
| 1 | ◌ा | आ की मात्रा वाले शब्दों को टोकरी में डालो। | नाव, हाथ, बाल, काम, दाल |
| 2 | ◌ि | अब इ की मात्रा वाले शब्दों को टोकरी में डालो। | दिन, तिल, सिर, दिल, हिरन |
| 3 | ◌ी | अब बड़ी ई की मात्रा वाले शब्दों को टोकरी में डालो। | नदी, तीर, चीनी, मछली, नीम |

After the fifth word of a round lands in the basket the prompt changes and the
next matra starts. After the third round: confetti, a
star burst, and **"शाबाश! तुमने सभी मात्राओं के सही शब्दों को टोकरी में रख लिया है।"**

## Nothing is written on screen

The only Devanagari a child reads is **the falling words themselves**. Every
instruction is spoken. What is left on screen is pictures and one glyph:

| | |
|---|---|
| title screen | painted cover + wordmark and an icon-only play button — nothing else |
| HUD | the matra chip (which matra we are hunting) and five slots (how many are home) |
| round change | one big matra glyph in a circle, 2.4s |
| correct / wrong | green or red on the word-cloud outline and the basket outline |
| win | mascot, three stars, confetti |

No sentence, no score number, no labels, no tick, no cross. That makes the VO
load-bearing rather than decorative — if a clip is missing, that instruction is
simply gone.

**Word choice is deliberate.** Every target word carries *only* the matra being
asked for — no पानी (ा + ी), no बिल्ली (ि + ी) — and every distractor carries
one of the other two, never the target. A child who is genuinely discriminating
matras cannot be tripped by a word that is technically correct for two rounds.

**Wrong word in the basket costs nothing.** The word's cloud outlines red and buzzes,
the basket outlines red and wiggles, and the word is tossed back out. No score
penalty, no lives, no cross — positive reinforcement only, exactly as
अक्षर वर्षा does with consonants.

**The play button is the only thing that moves on the cover.** The wordmark does
not bob, and the mascot and the three matra chips were removed from that screen
entirely — markup and rules both — so the one pulsing object is unmistakably the
one you press. (The kit's recipe-1 sky drift still runs behind everything: one
breathing glow and ~87 drifting sparkles. That is ambient background, not an
element; delete the two `.sg-*` divs from `#title-screen` to stop it.)

**The stage is 1333x750 — 16:9 — and fills the display.** The scaler used to
subtract a hardcoded 16px before fitting, which forced a gutter on all four
sides even on a screen that was exactly 16:9; that is what the black border
actually was. What remains on a display that is NOT 16:9 is the genuine
aspect-fit letterbox, and rather than leave it black the page behind the stage
is painted with the same artwork scaled to `cover` — the play plate during the
game, the cover art while the title is up. Being the identical image, every
colour in the margin matches the edge it touches, so the scene simply runs on.

Single file, no build step: open `index.html`.
`?still=1` is the reduced-motion switch (kit R5); `?nomusic=1` turns the
background music off.

---

## Files

```
index.html                     the whole activity
assets/UI/mascot_swifty.webp   fleet mascot (from fln-animation-toolkit/assets)
assets/UI/bg_plate.webp        sky + grass, no sun, horizon aligned to y=465
assets/UI/basket.webp          the WHOLE basket — recipe 21 reads its alpha
assets/UI/basket_front.webp    its near rim + body, cut along the bowl's inner
                               arc; the word sinks between the two
assets/UI/cloud_a|b|c.webp     UNUSED — scenery clouds, removed from both screens
                               (see "no scenery clouds" below); safe to delete
assets/_build_art.py           re-generates the art; key from .env, never inline
assets/_finish_art.py          keys the fake background out, fits, exports @2x
assets/_raw/                   untouched model output (gitignored)
assets/UI/bgdeco_star.svg      recipe 1 — sky drift
assets/UI/bgdeco_star_o.svg
assets/UI/bgdeco_spark.svg
assets/UI/hand_nudge.webp      recipes 3 + 4 — nudge hand (supplied art; the kit's
                               nudge_hand_new.svg is no longer referenced)
assets/UI/word_cloud.webp      the falling word chip — ONE pink raster, recoloured
                               per word by hue-rotate
assets/UI/cover_bg.webp        title screen only — painted cover, 16:9
assets/UI/play_btn.webp        title screen only — the painted play button
assets/UI/title.webp           title screen only — the painted wordmark
assets/UI/progress_bar.webp    the five-slot catch track in the header
assets/UI/matra_box.webp       UNUSED — the HUD matra chip, removed; safe to delete
                               ** currently reads अक्षर वर्षा, the SIBLING game **
assets/UI/nudge_fx_ring_inner.svg
assets/UI/nudge_fx_ring_outer.svg
assets/UI/nudge_fx_sparks.svg
audio/vo-tutorial.mp3          23 VO clips, Gemini TTS (voice: Leda)
audio/vo-round-aa|i|ee.mp3
audio/vo-level-i|ee.mp3        level-complete celebration (praise + next instruction)
audio/vo-good-1|2|3.mp3
audio/vo-win.mp3
audio/s-*.mp3                  the 15 words
audio/_build_vo.py             re-cuts the VO; key from $GKEY, never a file
audio/AUDIO_SCRIPT.xlsx        24 entries — the sheet a human VO artist would read
audio/_build_xlsx.py           regenerates the sheet
audio/correct.ogg              FLN Animation Kit, CC0 (Kenney)
audio/wrong.ogg
audio/burst.ogg
audio/sfx_celebrate.ogg
audio/SFX_LICENCE.txt
audio/sfx-incorrect.mp3        team's own wrong cue — currently UNUSED, see below
audio/bgm.ogg                  background music loop, Lyria (lyria-3-clip-preview)
audio/_build_music.py          re-cuts it; caches the raw generation in _bgm_raw.bin
```

## Voiceover — 23 clips, all rendered

Cut with **Gemini TTS**, model `gemini-2.5-flash-preview-tts`, voice **Leda**,
then silence-trimmed and loudness-normalised to -16 LUFS by `ffmpeg`.

| clip | plays |
|---|---|
| `vo-tutorial` | over the nudge-hand tutorial — "टोकरी को उँगली से इधर-उधर ले जाओ।" |
| `vo-round-aa/i/ee` | the round instruction. Words hold until it finishes. |
| `s-<word>` x15 | the word itself, the moment it lands in the basket |
| `vo-level-i/ee` | the level-complete celebration: praise AND the next matra's instruction, in ONE clip |
| `vo-good-1/2/3` | no longer played — the praise is now the first half of `vo-level-*` |
| `vo-win` | the closing line |

**Re-cutting them** — `audio/_build_vo.py`, key from the environment, never a file:

```bash
GKEY=<your Google AI Studio key> VOICE=Kore py -3.13 audio/_build_vo.py
```

It skips clips that already exist, so delete the ones you want re-cut first, or
name them: `py -3.13 audio/_build_vo.py . vo-win s-naav`. Handing the sheet to a
human VO artist works the same way — the file names are the contract and
`index.html` does not change.

**One clip needed a different model.** `gemini-2.5-flash-preview-tts` refuses
`s-naav` every time — `finishReason: OTHER`, no audio, no safety rating, across
four prompt variants and on `gemini-2.5-pro-preview-tts` too.
`gemini-3.1-flash-tts-preview` renders it fine, same voice, and the loudnorm
pass makes it sit level with the rest. Set `TTS_MODEL` to override.

**The round prompt gates the round.** `startRound` holds `paused` until the
instruction clip ends (6s hard floor if an mp3 is ever missing), so words never
start falling over the top of the sentence that says what to do with them.
Round-end praise chains the same way, on the clip's own `onEnd` rather than a
fixed delay, because `SwiftPalAudio` cuts whatever is playing when a new clip
starts.

**Swapping the wrong cue.** The game uses the kit's `wrong.ogg`, which was
measured as a pair with `correct.ogg`. To go back to the fleet's own cue, change
one line in the game script: `SFX.play('wrong.ogg')` → `SFX.play('sfx-incorrect.mp3')`.
Changing only one of the pair will make the two verdicts sound like they came
from different games.

### Round transitions

Finishing a round runs a **celebration screen**: Swifty springs on over a white
wash with a confetti burst, and one clip both praises the round just finished and
names the next matra. `startRound(i, skipVo)` is then called with `skipVo` so the
instruction is not said twice.

**One clip, not two.** `SwiftPalAudio.play()` stops whatever is playing, so
praise-then-instruction as two chained files is a seam the child hears — and the
celebration has to stay up for exactly as long as the voice, which is one
duration to wait on rather than two.

**The fifth word says its name.** `finishRound()` used to be called on the same
tick as the fifth catch, and since `play()` stops the current clip, that cut the
word's own pronunciation off the instant it started — every word in the round was
spoken except the one that completed it. The round now closes on that clip's
`onEnd`; `roundDone` latches at the catch so nothing can be collected during the
wait, while `finishing` guards `finishRound` itself. Two flags, because they no
longer happen on the same tick.

## Background music

`audio/bgm.ogg` — a 26s seamless loop cut with **Lyria** (`lyria-3-clip-preview`),
re-cut by `audio/_build_music.py`. Three things about it are deliberate.

**It is mixed as furniture.** The VO in this activity IS the instruction — one
that is not heard did not happen — so the music is held far under it at every
stage: normalised to **-30 LUFS** against the VO's -16, played at 0.38, and
ducked to 0.12 whenever any clip is speaking. Ducking is wired by *wrapping*
`SwiftPalAudio.play`/`stop` in the game script rather than editing them, because
core.js is inlined shared code that every game gets a copy of.

**It is .ogg, not .mp3.** mp3 carries encoder delay and padding that a browser
plays as an audible gap at every `loop` wrap, which no amount of crossfading
inside the audio can fix. The tail is *also* crossfaded into the head — the
first 2.5s are cut off the front and mixed over the last 2.5s — so the end of
the file already is its start.

**It starts on the play button.** No browser autoplays audio before a user
gesture, and the title screen has none.

`_build_music.py` caches the model's raw bytes in `audio/_bgm_raw.bin`
(gitignored), so re-encoding at a different length, level or codec is free;
`--regen` asks for genuinely new music.

---

## FLN Animation Kit — install report

Installed from `fln-animation-toolkit/ANIMATIONS.md` (cloned into
`FINAL GAMES/fln-animation-toolkit/`). Every block keeps its `BEGIN`/`END`
markers: `grep -rn "FLN ANIMATION KIT" .`

| # | Recipe | State |
|---|---|---|
| — | core + reduced-motion | installed |
| 1 | Start screen stars (drift) | installed — two layers, `#sky-start` and `#sky-end` |
| 3 | Nudge hand press (treatment C) | installed |
| 4 | Nudge hand tap ripple | installed |
| 7 | Correct answer confetti | installed — end screen, two waves |
| 8 | Celebration star burst | installed — end screen |
| 19 | Correct answer select | installed — on the falling word tile |
| 20 | Wrong answer select | installed — on the falling word tile |
| 21 | Tap the object (engine A) | installed — on the basket |
| 22 | Sound | **skipped** — see below |

### Where each effect acts

Recipes 19/20 were installed as a pair, as the kit requires. The "tile" here is
the falling word chip; the "object" in recipe 21 is the basket. One catch fires
both halves at the same tempo, so the tile and the basket always agree:

```
correct catch  →  cloud: green stroke + ckPop + spark crown  (19)
                  basket: green outline + olYes pop          (21)
                  rim:    sparkle burst as the word drops in  (local, not recipe 7)
wrong catch    →  cloud: red stroke + wgNo buzz, then release (20)
                  basket: red outline + olNo wiggle          (21)
```

Both read `--fx-beat` / `--fx-reward` from `:root`, so the whole feedback set
retimes from one number.

### Structural notes

- **Three layers on the basket**, because each element owns exactly one
  transform: `.basket` (JS `translateX`), `.basket-lift` (catch bounce),
  `div.ol.ol-alpha` (recipe 21's outline + `olNo`/`olYes`). Recipe 21's own
  gotcha — placement goes on a wrapper, never on the outlined element.
- **Two layers on the falling word**, for the same reason: `.drop` (JS owns the
  fall, plus the sink/eject/land keyframes) and `.drop-tile` (recipes 19/20).
- **Recipe 21 engine A is on a `<div>` wrapping the basket `<img>`, not on the
  image.** A CSS filter on the div still derives the outline from the art's
  alpha, and a div has `offsetWidth` — which `objectOutline.set()` needs for its
  forced reflow.
- **The basket art must keep a real alpha channel.** The outline is five chained
  `drop-shadow` passes over that alpha, so a plate with a background baked in
  produces no outline at all and the correct/wrong beat silently disappears.
  Gemini returns a *painted checkerboard* when asked for transparency, never an
  alpha channel; `assets/_finish_art.py` floods from the image border to cut it,
  which is also why a white cloud survives — its body is walled off by the
  continuous navy outline, so the flood cannot reach it.
- **The word rides a pastel CLOUD, and the mark is a ring around it.** The kit
  puts correct/wrong on the tile's `border-color`; this tile has no border, so
  the verdict is drawn the way the basket's is — recipe 21 engine A, four
  zero-blur drop-shadows off the art's own alpha. Same colours, same tempo, same
  house rule. The fill never changes, so the word stays readable through
  correct, wrong and release. No tick, no cross.
- **One cloud raster serves every word.** It is painted pink (hue 339, fill and
  outline alike) and each chip picks a `hue-rotate` from `CLOUD_HUES`. The list
  deliberately contains no rotation landing on green or red: the answer ring is
  drawn just outside the cloud's own outline in exactly those colours, and a
  green cloud wearing a green ring communicates nothing.
- **The chip is a FIXED 204x128 box**, not width-follows-the-word. One painted
  cloud cannot be stretched a third wider for a long word without the lobes
  smearing, so the font adapts instead and `TILE_W`/`TILE_H` are the single
  source of truth for the physics.
- **The basket is TWO layers and the word goes between them.** `.basket` (z4) is
  the whole basket; `.basket-front` (z6) is its near rim and body; a sinking word
  sits at z5 in between. Inside the bowl's mouth the word is therefore drawn over
  the dark interior — it is *in* the basket — and only then does the near rim
  cover it.
  **Both layers are cut from ONE generated image**, never generated separately:
  two runs of an image model would not register to the pixel. `_finish_art.py`
  splits `basket_deep` along the bowl's inner edge PER COLUMN, finding the
  interior as the largest connected blob of dark *warm* pixels — warm excludes
  the navy linework, largest excludes the wicker's own shading. Following the
  rim's arc is the whole reason to do this in the art rather than with
  `clip-path: inset()`, which can only cut a straight line.
  **The back layer stays the COMPLETE basket** on purpose: recipe 21 derives the
  answer outline from its alpha, and half a basket would outline half a
  silhouette. The front piece carries no filter.
  `.drop` is raised to z5 ONLY while `.sink` is on it; raising it permanently
  would let a MISSED word sail over the basket.
- **EVERY transform must be applied to BOTH halves, or the basket comes apart.**
  This is the trap the two-layer approach sets. `basketBounce` lifts its element
  15px and fires at the exact moment a word is landing — with it on the back half
  only, the basket visibly separated into two baskets just as the child looked at
  it. `setBasketX()`, `bounceBasket()` and `answerBasket()` exist so there is one
  place each motion is applied; never write `basketLift.classList.add('bounce')`
  or `objectOutline.correct(basketArt)` directly.
  The front half gets recipe 21's *animations* but never its *filter*: a second
  alpha-derived outline would trace this piece alone and draw a coloured ring
  along the cut arc, across the middle of the basket.
- **`setBasketX()` rounds to whole pixels.** Both halves are separately
  composited (both carry `will-change`, the back one a filter), so at a
  fractional offset they can rasterise half a pixel apart and the cut shows as a
  hairline.
- **The basket pair is the only LOSSLESS art in the folder** (102 KB + 68 KB
  against ~25 KB lossy). Two layers meant to be the same pixels, compressed
  separately, pick up different artefacts along the cut. Everything else stays
  lossy webp.
- **Both halves move through `setBasketX()`.** They must not drift apart by a
  pixel. Only the horizontal move needs mirroring — the catch bounce (420ms) and
  recipe 21's `olYes` pop (540ms) are both over by the time the sink starts at
  420ms, so the word is never between two halves doing different things.
- **A caught word RIDES the basket.** The catch captures a position into
  `--catch-x`, but the player's finger does not stop — pinned to that captured x
  the word sank where the basket used to be, so dragging straight after a catch
  walked the basket out from under it and the word fell in open air. `tick()`
  re-points every entry in `carried` each frame, after `moveBasket()`. Rewriting
  the custom property re-resolves the running `dropSink` keyframes without
  restarting them, so the word keeps descending while tracking sideways.
  Two things this needs: `catchDrop` clears the INLINE transform `positionDrop`
  has been writing (inline beats the `.drop.caught` rule; animations do not, so
  the sink needs no such help), and a wrongly-caught word sets `stopCarry` as it
  is ejected, since from then on it is airborne.
- **`.caught` goes on at the CATCH, `.sink` 180ms later — and the z-index rides
  `.caught`.** The catch freezes the word at the rim and holds it there through
  the confirm beat before the sink starts. With the z-index hung off `.sink`,
  the word spent those 180ms behind the basket and then jumped in front of it,
  which read as dipping behind the basket before going in.
- **The pointer is tracked on `window`, not `.play-area`.** The basket only
  reads the pointer's X, but a play-area listener stopped receiving moves as
  soon as the pointer crossed into the 96px header or left the stage, so the
  basket froze until you wandered back. `onPointerMove` clamps X to the stage,
  so tracking everywhere is safe.
- **The cursor is visible.** It used to be `cursor:none` on the idea that the
  basket *is* the cursor, but the basket eases toward the pointer rather than
  sitting on it and stops at the stage edges — with nothing to point at, there
  was no way to see why it had stopped following.
- **The caught word is hidden by the BASKET, never by a fade.** `.drop` is
  z-index 2 against the basket's 4 and is its own stacking context, so anything
  below the rim is simply occluded. An earlier version ran `opacity` to 0 while
  the chip was still at rim height — it dissolved in mid-air and never looked
  like it went in. `dropSink` now stays opaque throughout and is paced in three
  beats (lift + shrink, cross the rim, drop), because the catch fires when the
  chip's BOTTOM reaches the rim and a straight descent from there is over before
  the eye finds it.
- **There are no scenery clouds in the play area at all.** The falling words are
  themselves clouds, so decorative clouds put the thing to be read and the thing
  to be ignored in the same shape — a child scanning for a word has to rule out
  every cloud first. The play sky is empty; `cover_bg` keeps its painted clouds
  because nothing falls on the title screen. (They were static before this, for
  a related reason: sideways scenery motion gets read as the word itself
  sliding.)
- **The mascot is not on the play screen.** The basket is dragged the full width
  of the stage and the two overlapped constantly. It opens and closes the
  activity instead, where nothing moves across it.

### Deviations from the recipes, and why

1. **Recipe 1's mandatory `.start-bg` → `startnew_bg_plain.webp` swap is
   omitted.** That line exists because the fleet's start background has the
   decorations painted into it. There is no `.start-bg` element here — the title
   screen is painted by `bg_plate.webp`, the same plate the play area uses — and
   the plate is plain sky, sun and grass with no decoration in it, so it *is*
   the `_plain` the recipe is asking for. The "two sets of stars" gotcha cannot
   occur here.
2. **`host-bridge` block (new, ~15 lines, clearly marked).** This engine scales
   the stage with `--stage-scale`; the kit reads `--scale` (R1). One listener
   mirrors the value so every recipe below it pastes verbatim with no coordinate
   edits. It also sets `window.__skyManual` (this game has two sky layers, and
   the recipe's auto-init only fills the first `.sg-sky` it finds) and wires
   `?still=1` to `html.no-anim`.
3. **Recipe 22 (Sound) skipped.** The prompt's `SFX: <include / skip>` was left
   blank, recipe 22 is not one of the seven that were asked for, and this
   activity already ships `SwiftPalSound` for generated cues — two audio buses in
   one file is the duplication the kit itself warns about. The kit's four CC0
   *recordings* are used, played through plain `<audio>` by a 10-line `SFX`
   helper. Say the word and the full recipe-22 engine can go in instead.

### Kit defect found (one-line fix applied, worth upstreaming)

Recipe 20's JS calls `tempo(el)`, but `tempo` is declared inside **recipe 19's**
IIFE and never exported. As published, `FLNMotion.wrongSelect.play()` throws
`ReferenceError: tempo is not defined` — swallowed by `M.guard`, so the entire
wrong-answer beat is *silently dead* and only a `console.warn` shows. Recipe 19's
block here adds `M.tempo = tempo;` and recipe 20 reads it. Both sites carry a
`KIT DEFECT FIX` comment. This is the smallest change that makes the documented
"one tempo, two effects" behaviour actually work.

### Not verified

- **Nobody has heard the VO yet.** The clips were generated, trimmed and
  length-checked (words 0.6-1.2s, prompts 3.4-5.7s, win 5.2s — all consistent
  with the text, so no clip is reading its own style instruction aloud), and the
  whole 23-clip sequence was confirmed to fire in the right order. But they were
  not listened to. **Play it through once before it goes to a classroom** —
  synthesis can mispronounce a Hindi word without anything in the numbers
  showing it.
- **Portrait / `html.rotated`** — this engine has no rotation mode, so recipe 1's
  `html.rotated` rule is present but never exercised. Untested, by absence.
- **Touch emulation** — pointer listeners are registered `{passive:false}` (R6)
  and the play area is `touch-action:none`, but a real touch device was not
  available. Nothing in the play area is tappable, so there is no control
  underneath the new elements for a tap to fall through to.
- **`ENGINE_VERSION`, `ASSET_BYTES`, `#bootLoader`, `verify_bundle.py`** do not
  exist in this engine — R9/R10 and install step 10 are N/A. Every entry point
  is still wrapped in `FLNMotion.guard` (R4).
- **The nudge assets were authored, not copied.** The three ripple layers are not
  in the toolkit repo and no sibling activity in `FINAL GAMES/` has them. The
  hand itself is now `nudge_hand.webp`, generated and keyed like the rest of the
  art; the kit's original `nudge_hand_new.svg` is kept in the folder but is no
  longer referenced.
  **Swapping the hand means re-deriving two numbers**, because the ripple is
  centred on the FINGERTIP, not on the box. `_finish_art.py` measures the
  topmost opaque row and prints both: the painted hand's tip lands at
  (53.5, 0.2) inside the 86×108 `#nudgeHand` box, so `.nh-tapfx` is offset
  `6.19px / -47.08px` — where the old SVG's tip was at (34.2, 15.8) and the
  recipe's pasted `-13.08px / -31.48px` was correct for it. `NUDGE_OPTS` dx/dy
  moved by the same delta, plus a further lift so the wrist is not clipped by
  `.play-area`. Do not eyeball any of these four figures. If the team has the real
  fleet assets, dropping them in needs no CSS change.

### Verified

Served at `localhost:5503`, checked in-browser:

- Title screen, sky drift (87 elements per layer), nudge hand + ripple, gameplay,
  all three round transitions with the right matra and prompt, and the win screen.
- A full run fires all 23 VO clips in exactly this order: tutorial, round-aa,
  five आ words, good-1, round-i, five इ words, good-2, round-ee, five ई words,
  good-3, win.
- A full autoplayed run collects exactly 5 distinct words per round, 0 duplicates,
  score 150, one `startRound` per round, one `endGame`.
- `?still=1`: green `#00B132` and red `#F93544` border marks both land and stay;
  the spark crown is never built and `.wg-pulse` is `display:none`; the basket's
  outline filter goes red with the motion dropped. Nothing throws.
- Confetti (90 pieces, 3 nested elements each) and the star-burst canvas both
  mount on the end screen.
- Console clean apart from 404s for the 19 unrecorded VO mp3s.

CSS animation playback and `requestAnimationFrame` could not be watched live —
the test browser pane does not produce frames while backgrounded, so the game
loop was driven by a `setTimeout` shim and the visual states were captured under
`?still=1`, where transitions land on their end values. **Worth one pass on a
real device to watch the motion at speed.**
