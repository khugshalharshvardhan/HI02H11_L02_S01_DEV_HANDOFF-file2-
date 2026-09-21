# HI02H11_L02_S01 — build receipt

**आ, इ, ई मात्रा वाले शब्द पढ़ता है। शब्दों में आने वाली मात्रा पहचानता है।**
Curriculum sheet row 55. Built 2026-09-14.

## What shipped

| | |
|---|---|
| slides | **19** — tutorial 4, guided 6, practice 9 |
| engine | `2026.08.04b-r4-unified`, the game's own `engine_local/` copy (3 changes, all guarded) |
| illustrations | **13/13** generated, eyeballed at full size |
| voice clips | **95** = 87 recorded for this lesson + 8 copied chrome/phase-gate |
| spoken length | ~253 s |
| asset receipt | **0 FAIL / 0 WARN** (`_verify_assets.py`) |
| runtime | **108/108 declared assets return 200**, verified by fetching every one from the live page |
| mechanic gate | 14 test slides — drag 6 (43%), pick 8 (57%), ceiling 60% |
| review deck | `HI02H11_L02_S01_SME_Review.pptx` — 20 pages + title + overview |

## Verified live, not just built

- **The SME's hint ladder fires in the authored order.** Instrumented `play()` on G2 (दिन) and
  tapped through: `vo_prompt_pick_word` → `vo_name_din` → first wrong → **`vo_again_din`**
  («फिर से सुनो, दिन।») at scaffold 1 → second wrong → **`vo_sound_din`**
  («दि-न। 'दि' में कौन-सी मात्रा सुनाई दे रही है?») at scaffold 3 with terminal help, the wrong
  option `crossed faded`. Correct tap → `opt-cell correct`, slide locks.
- **The matra highlight.** नाक renders ा red in-word; तीर renders ी red in-word; दिन renders the
  `◌ि` callout and it clears the आगे button.
- **The landing letter strip renders** — three tiles, amber glow, `sg-ex-letter` styled.
- **The image-free slides really have no stimulus.** `P5_has_stimulus: false` on राम.
- **Sort bins and tiles are wired.** G4: bins `I`/`E` labelled «छोटी इ ◌ि» / «बड़ी ई ◌ी», four
  tiles each carrying the right bin code and its own word clip.
- **32/32 factual claims in the review notes were checked against `card.json`** by script — slide
  counts, phase split, clip and image counts, every option triple quoted in the notes, the mastery
  mode alternation, bin counts, and that `सिर` appears nowhere in the card.

## Five defects found and fixed during this build

Recorded because **every one of them passes a naive existence-and-size check**. Each now has a
guard so it cannot recur silently.

### 1. The landing letter strip rendered completely empty
`conceptTileHTML` in this engine copy had no `case "letter"`, so every cell fell through to
`default: return ""`. No console error, no failed request, no warning — the card was correct and
the strip was simply not there.

The cause is worth escalating on its own: **`HI01H11_L03_S01` and `HIKGH09_L01_S03` both stamp
`ENGINE_VERSION = "2026.08.04b-r4-unified"` and have different `conceptTileHTML` bodies.** The
version string does not tell you what the engine can do. Fixed by back-porting the case verbatim
from the copy that has it; the builder now checks for the **feature**, not the version.

### 2. Ten voice clips were truncated — present, valid, correctly sized, and half-spoken
An **em-dash before a short final word makes the TTS model cut the clip.** `vo_yes_din`
(«शाबाश! दिन — इसमें छोटी इ की मात्रा है।», 39 chars) came back at **0.89–1.29 s across four
deterministic retries** while its identically-templated siblings ran 4.09 s and 4.29 s.

Probed head to head, same words, 3 takes each: **em-dash 0.73–1.05 s · comma 1.53–2.21 s ·
danda 1.13–2.01 s**. The dash also had the worst refusal rate. Every short line now uses a comma;
the SME's words are unchanged.

**The detector that works is peer comparison, not an absolute rate.** Seconds-per-character is
useless alone — a 3-character word carries fixed silence, so its s/char is ~4× a sentence's, and a
band wide enough for both catches nothing. `_verify_assets.py` groups clips by text length and
flags any clip under 55% of its group median.

### 3. Two slides spoke the same sentence in two different voices
The first build minted a clip id **per slide**, so `vo_p5_prompt` and `vo_p7_prompt` carried the
same sentence; one was refused and recovered on a fallback voice. Fixed structurally: **clip ids
are keyed by word/line, not by slide.** Same text is now one clip — which also took the recording
sheet from 116 lines to 87.

### 4. Four clips had their text edited while keeping their clip id
So the old audio stayed on disk with nothing flagging it — `vo_t1_instruction` was still a 16.25 s
recording of a line that had been cut to 56 characters. Caught by the same duration check.

### 5. Two illustrations were wrong rather than missing
- `obj_din` v1: "a sun with rays" came back as a **plain yellow smiley with no rays**, which reads
  as an emoji, not as «दिन» — and दिन is a tutorial word used on four slides. It passed every
  automated check, because nothing automated knows what a sun looks like. **It also looked fine on
  the 230 px contact sheet** and was only obviously wrong at full resolution.
- `obj_din` v2: demanding "clearly separated" rays came back **blank** (175×349, 10 KB) — separated
  rays are disconnected components, so `keep_largest` discarded the disc and kept a 1-pixel sliver.
  This is the `obj_sapna` failure from the sibling lesson with a different cause.
- v3 demanded **one single connected silhouette** ("rays fused directly onto the disc"): correct.
  The working prompt and the reason are recorded in `_art_manifest.json`.

All five are appended to `silly_mistakes_ledger.md` in all three kit copies.

## Guards this bundle now carries

Build-time, in `scripts/build_skill_HI02H11_L02_S01.py` — the build **refuses** rather than warns:

| guard | prevents |
|---|---|
| `ी` ∈ / `ि` ∉ `RIGHT_SPACING_MATRAS` | losing the in-word highlight · mis-clipping दिन |
| `.meet-col` spacing present | the matra callout colliding with आगे |
| `case "letter"` + `sg-letter-glyph` + `.sg-ex-letter{` | the landing strip rendering empty |
| all 8 modules present | a slide type mounting as nothing |
| every highlighted matra is in its word | a callout for a matra the word lacks |
| every sort tile has a bin on its own slide | an undroppable tile |
| ≤ 6 tray items | `.sort-tray` is `flex-wrap:nowrap` and overflows past 6 |
| exactly 1 correct option, and it has a clip | a silent correct cell · two correct answers |
| no distractor is another real lesson word | a distractor that is defensibly also right |
| gesture family ≤ 60% of test slides | the mechanic-diversity gate, before art is paid for |
| every image declared **and** used | wasted generation · a 404 to emoji |
| preload hints + mounted modules resolve | the sibling's stale `sit_*` preload defect |
| `img_ext` matches the files on disk | kit defect A3 |

Post-build, in `_verify_assets.py`: existence, wiring, **truncation by peer comparison**, long-clip
watch, the blank-PNG opacity/colour screen, emoji fallbacks, and `img_ext` agreement.

## Open for the SME

1. **Punctuation** — your «फिर से सुनो — दिन।» now uses a comma. Words untouched. Say if you want
   the dash back and I will flag those clips for human recording instead.
2. **One word swapped** — सिर → हिरण, because सिर and बाल would be near-identical pictures at
   116 px and बाल is in your required final set.
3. **Landing greeting** — this lesson says «स्विफ्टी» and «सीखेंगे»; the sibling carries «swiftee»
   and «जानेगें» verbatim from your note. One ruling settles both.
4. **Register at the phase gates** — lesson is tum, the three shared gate clips are still aap.
   Same open ruling as the sibling; one decision covers G2 and G3.
5. **Two clips on Aoede** — `vo_again_din` and `vo_h2_din`. Kore truncates them no matter how many
   retries (the word दिन triggers it). A reword brings them back to the lesson voice.

## Open for the dev team

1. **Divergent code under one `ENGINE_VERSION`** — this is what made defect 1 possible and will
   keep doing so.
2. **`ी` into the shared `RIGHT_SPACING_MATRAS`** — currently a per-game change; every matra lesson
   in the fleet would benefit.
3. **`concept_strip` landings never receive the glow class** — the branch returns before
   `el.classList.add("show","hint-glow")`. Affects all 11 reference bundles that use it. This
   bundle carries its own scoped style; `engine/` untouched.
4. **`MATRA_FILL`** — a module that renders a word with a matra slot and lets the child drag a
   matra into it. This is the SME's Screens 5–7 as literally written; nothing in any engine does
   it, and it is substituted here rather than approximated.
5. **Tapping a matra inside a rendered word** — the SME's Screen 12. Needs the word split into
   tappable parts, which `SENTENCE_FIND` does for words in a sentence but nothing does for a matra
   in a word.
