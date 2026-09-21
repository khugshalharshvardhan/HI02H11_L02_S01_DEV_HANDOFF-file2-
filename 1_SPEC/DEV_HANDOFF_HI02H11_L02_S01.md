# DEV HANDOFF — HI02H11_L02_S01 · «मात्राओं की रेल»

**Skill:** आ, इ, ई मात्रा वाले शब्द पढ़ता है। शब्दों में आने वाली मात्रा पहचानता है।
*(Hindi_content progression.xlsx, row 55)*

**Source of truth for this document:** the SME's own recommendations, written into the speaker
notes of `HI02H11_L02_S01_SME_Review.pptx` (16 screens, 2026-09-16) plus the visual mockups
embedded in the same deck. Every recommendation is reproduced **verbatim** in
[`_SME_RECOMMENDATIONS.md`](_SME_RECOMMENDATIONS.md) and quoted per screen below, so the SME's
words and my engineering reading never blur. Mockups are extracted to
[`_SME_MOCKUPS/`](_SME_MOCKUPS/), named by deck slide.

Machine-readable form of everything below: [`dev_spec_HI02H11_L02_S01.json`](dev_spec_HI02H11_L02_S01.json).

---

## 1. Read this first — the size of the ask

This is **not a revision of the built lesson. It is a new game concept.**

The lesson that exists today (`HI02H11_L02_S01.html`, engine `2026.08.04b`, 19 slides, all art and
voice complete, receipt 0 FAIL / 0 WARN) uses the standard stage: a card, a title bar, option
cells, sort bins. The SME's recommendations replace that with a **train** — a locomotive with
coaches that are simultaneously the answer options, the sort bins and the word frames — plus a
magnifying-glass poem hunt and a ghost guide character.

The flow is **17 screens** — the landing plus 16 activity screens. 16 of them carry a written
recommendation; the celebration carries none and ships as built.

| verdict | screens | which |
|---|---|---|
| **ships today** | 2 | `INTRO` (content change only), `CELEBRATION` |
| existing module + **new train chrome** | 7 | landing, tap-a-coach ×3, word→coach sort, matra→coach sort, picture→coach sort |
| **new module** | 7 | matra-build transformation ×3, two-example teach ×3, matra-fill ×1 |
| **blocked on a content ruling** | 1 | poem hunt (§4) |

So: **2 screens are free, 7 are reskins, 8 need new engine work.** Two of the eight — the train
shell (which the 7 reskins also depend on) and the poem hunt — are substantial; the other six are
moderate.

**None of this is a reason not to do it** — the concept is good, the train genuinely unifies the
lesson, and the matra-build transformation teaches the thing the outcome actually asks for far
better than the current pick slides. It is a reason to **sequence it** (§8) and to decide
explicitly whether the existing 19-slide build ships in the meantime (§9).

---

## 2. Cross-cutting engine work

These are shared by most screens. Build them first; they are most of the cost.

### 2.1 `TRAIN_CHROME` — the shared visual shell  🔴 new, blocking 7 screens

> **SME:** "Train comes through animation from right to left. Train stops at the centre of the
> screen." · "Add a soft train arrival / whistle SFX when the train enters." · "Keep the existing
> mascot and overall UI/UX style unchanged."

A renderer, not a slide module — the landing and six activity modules mount inside it.

```
TrainChrome.mount(host, {
  coaches: N,                     // 2..4; mockups all use 3
  coach_label: [..],              // rendered ABOVE the coach  (ा | जाल | "आ (ा)")
  coach_body:  [..],              // rendered INSIDE the coach (word, blank-word, or empty drop zone)
  drop_zone:   true|false,        // does the coach interior accept a drop
  entry:       "right_to_left",   // locomotive + coaches slide in, settle centred
  on_enter:    cb                 // fires when the entry animation settles
})
```

Required coach states; the six activity screens all use them:

| state | trigger | visual |
|---|---|---|
| `idle` | — | flat colour (mockups: coach 1 pink/red, 2 green, 3 amber) |
| `hover` | a card is dragged over it | soft glow |
| `correct` | right tap / right drop | glow + sparkle/confetti burst **around that coach** |
| `wrong` | wrong tap / wrong drop | short horizontal **shake/wiggle**, then revert |
| `locked` | card placed correctly | card fixed inside, no longer draggable |
| `nudge` | 2nd wrong attempt | soft pulse + the guiding hand on **the correct** coach |
| `complete` | all coaches solved | all coaches glow together + **whistle / steam** animation |

**Reduced motion:** the right-to-left entry and the steam must degrade to a static settled train
under `prefers-reduced-motion`. Note `capture_pages.py` injects `*{animation:none !important}` for
review captures, so **anything that exists only inside `@keyframes` will be invisible in the review
deck** — this already cost us four attempts on the landing letter glow. Put the settled state on the
base rule and let the animation only move it.

### 2.2 The scaffold ladder changes from 2 attempts to 3  🟠 engine change, affects every test screen

The SME specifies the same ladder on all nine test screens, and it is **not** what the engine does.

> **SME:** "**1st Wrong Attempt** — Wrong coach should wiggle / shake. **No hand nudge.** Only hint
> VO should come. **2nd Wrong Attempt** — Wrong coach should again wiggle / shake. Hint VO should
> play. **Show hand nudge on the correct answer.** **Correct Answer on 3rd Attempt** — Show confetti
> / sparkle. Correct coach highlights. Next button becomes active. **No VO.**"

| | engine today (`2026.08.04b`) | SME asks for |
|---|---|---|
| `max_attempts` | 2 | **3** |
| 1st wrong | `hint1` VO + Swiftie tryagain | `hint1` VO only, **explicitly no hand** |
| 2nd wrong | terminal help: reveal, dim other options, **hand appears**, correct answer effectively given | `hint2` VO + **hand nudge on the correct coach**, child still answers themselves |
| 3rd attempt correct | n/a (already revealed) | confetti + `correct` state, **silent — no VO** |
| card marked | `answer_revealed`, mastery miss | still a miss, but the child produced the answer |

This is a better ladder — the current one hands over the answer one rung too early. Proposed
`scaffold_rules` extension, defaulting to today's behaviour so no shipped game changes:

```json
"scaffold_rules": {
  "nudge_timeout_ms": { "guided": 6000, "practice": 8000 },
  "max_attempts": 3,
  "hand_on_attempt": 2,          // default 2 today via terminalHold; now explicit
  "reveal_on_attempt": null,     // null = never reveal, the child always answers
  "silent_on_late_correct": true // no `correct` VO when solved on the final attempt
}
```

`silent_on_late_correct` matters: `celebrateThenAdvance(slide, revealed)` currently always plays
`correct` or `reveal`. The SME wants the 3rd-attempt success celebrated **visually but not spoken**,
so the child is not told "शाबाश" for something they got twice wrong.

### 2.3 On-screen instruction text is removed everywhere  🟢 card-only, but confirm the shell

> **SME, on nine separate screens:** "No instruction text on screen. Only VO should play." ·
> "Remove any extra explanatory text that is not required." · "Keep the screen clean and minimal."

The engine already supports `prompt_hi: ""` and the built lesson uses it on teach slides
([S03P2-l]). **Confirm the non-tutorial shell collapses the heading band when `prompt_hi` is empty**
rather than leaving a blank blue pill — the mockups show no heading strip at all on the train
screens (`_SME_MOCKUPS/slide14`, `slide15`, `slide17`).

Note the mockups are inconsistent with the notes here: `slide11_image12.png` **does** print
«जिन डिब्बों में आ की मात्रा वाले शब्द है, उन डिब्बों पर टैप करो।» at the top. The notes are
explicit and repeated, so **the notes win**; flagged in §7 for confirmation.

### 2.4 New SFX  🟢 asset work

The SME names five sounds that do not exist in `assets/UI`. Today's set is `sfx_tap`,
`sfx_correct`, `sfx_wrong`, `sfx_pop`, `sfx_celebrate`.

| new id | used for |
|---|---|
| `sfx_train_arrive` | locomotive entry |
| `sfx_whistle` | round / lesson completion steam-and-whistle |
| `sfx_sparkle` | matra or word snapping into a coach |
| `sfx_chime` | a letter transforming (ज → जा) |
| `sfx_shake` | wrong drop — SME asks for a "soft error/shake sound", distinct from `sfx_wrong` |

House rule: **chrome and SFX are COPIED, never generated.** These need to come from the design/audio
team, not from a model.

### 2.5 The ghost guide  🔴 new, poem screen only

> **SME:** "Use a small friendly ghost character/effect as a search guide, **not as decoration**." ·
> "If the child is idle for a few seconds, the ghost appears near the magnifying glass and gently
> moves toward the poem." · "On 2nd wrong attempt … Ghost floats toward one correct target word. It
> gently points/pulses near that word. **This acts as the hint instead of adding extra text.**" ·
> "Do not keep ghost constantly moving on screen."

This is a **second nudge actor** alongside the existing hand (`pointNudgeAt` / `nudgeHand`). It
carries the idle cue AND the rung-2 hint on that screen. Cleanest build: extend the existing nudge
system with a pluggable actor (`hand` | `ghost`) rather than adding a parallel timer, so the
"one nudge at a time" and `state.hintActive` guards keep working.

⚠️ **A ghost is an odd choice for a 7-year-old's reading task and it is new to the fleet** — every
other game guides with the hand or the mascot. Suggest the existing mascot (Swiftie) with a
magnifying glass does the same job with no new character, no new art line, and no "is a ghost
frightening" question. **Raised, not decided** — see §7.

---

## 3. New slide modules

### 3.1 `MATRA_BUILD` — the transformation teach  🔴 new · screens 3, 5, 7

The core teaching idea of the whole redesign, and the best thing in it: the child sees and hears
a word **change** when a matra joins.

> **SME:** "आइए, देखें कि आ की मात्रा लगने से शब्द की आवाज़ कैसे बदलती है।" · "जल appears. VO reads:
> 'जल'. The letter ज is highlighted. ा appears beside ज. Show: ज + ा = जा. Play the sound difference
> clearly: 'ज' → 'जा'. Then ल joins. Final word appears: जाल. Highlight ा inside जाल." ·
> "**Avoid showing all stages together at the start.**" · "Give a small pause between each sound so
> the child can hear the change."

Mockup: `_SME_MOCKUPS/slide05_image5.png` — three panels, arrow-separated: `जल` → `ज + ा = जा` → `जाल`,
each with a supporting picture and a caption.

```json
{
  "type": "MATRA_BUILD",
  "phase": "tutorial",
  "prompt_hi": "",
  "audio": {
    "prompt":  "vo_mb_jal_intro",   // आइए, देखें कि आ की मात्रा लगने से…
    "base":    "vo_name_jal",       // "जल"
    "onset":   "vo_snd_ja",         // "जा"   <-- SEE THE TTS WARNING IN §6
    "result":  "vo_name_jaal",      // "जाल"
    "explain": "vo_mb_jal_explain"  // अब जल में आ की मात्रा लगाने पर — जाल बनता है।
  },
  "data": {
    "base_word":   "जल",
    "base_img":    "obj_jal",
    "consonant":   "ज",
    "matra":       "ा",
    "syllable":    "जा",
    "result_word": "जाल",
    "result_img":  "obj_jaal",
    "auto": true
  }
}
```

Staging contract, in order, each step gated on the previous **clip ending** (not a timer — see
`[32b nocut]`, where fixed 1400 ms advances truncated 27–35% of every reveal line):

1. `base_word` fades in + picture · speak `base`
2. `consonant` highlights inside `base_word`
3. `matra` pops in beside it — **for `ि`, it must visibly travel to the LEFT of the consonant**
   (SME: "The ि मात्रा should visibly move to the left side of ब, so the child notices its written
   position") · `sfx_pop`
4. `consonant + matra = syllable` renders in the centre panel · speak `onset` · `sfx_chime`
5. remaining letters join · `result_word` completes · `sfx_correct`
6. **`matra` highlights red inside `result_word`** · speak `result`
7. speak `explain` → unlock आगे

Step 6 can reuse `_matraWordSVG` / `_matraClipCols` as-is for `ा` and `ी`. **For `ि` it cannot** —
see §5.

### 3.2 `MEET_LETTER` two-example sequencer  🟠 extension · screens 4, 6, 8

> **SME:** "Keep one example visible at a time. First show नाक with the nose image. Highlight only
> the ा matra in the word नाक. After that, show the second example मटका with a clay pot image.
> Highlight the ा matra in मटका as well." · "Keep animation one by one, not all together."

`MEET_LETTER` today renders **one** word and runs one autonomous demo. Add `data.examples[]` and a
sequencer that runs the existing demo once per example, clearing between:

```json
"data": {
  "examples": [
    {"word_hi": "नाक",  "matra": "ा", "img": "obj_naak",  "audio": "vo_meet_naak"},
    {"word_hi": "मटका", "matra": "ा", "img": "obj_matka", "audio": "vo_meet_matka"}
  ],
  "auto": true
}
```

Keep the single-word path byte-identical so the 11 shipped `MEET_LETTER` games are untouched.

### 3.3 `TRAIN_TAP` — tap the coach  🟠 reskin · screens 9, 10, 11

> **SME:** "जिस डिब्बे में आ की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए।" · "Correct coach
> should glow / highlight" · "शाबाश! हाथ शब्द में आ की मात्रा है।"

Mockup `slide11_image12.png`: coaches carry **नाक · दिन · पानी**, one is correct.

This is `mountTapOptions` with `TrainChrome` as the `optionRenderer` and the 3-attempt ladder from
§2.2. No new answer logic. `data.options[]` with `letter` = the coach word, `target` = the correct
word, one clip per coach so speak-on-tap still works.

### 3.4 `TRAIN_SORT` — drag into the coach  🟠 reskin · screens 12, 13, 15

Three variants of one module, all `SORT_GENDER` semantics with `TrainChrome` bins:

| screen | coach label | draggable cards | mockup |
|---|---|---|---|
| 12 | the matra (ा / ि / ी) | **word** cards with pictures — हाथ, पिन, नीम | `slide14_image14.png` |
| 13 | the **word** (जाल / सिर / कील) | **matra** cards — ा, ि, ी | `slide15_image15.png` |
| 15 | the matra (आ (ा) / इ (ि) / ई (ी)) | **picture-only** cards, 2 per matra | `slide17_image17.png` |

Screen 13 is the reverse mapping of 12 and is a genuinely good idea — it stops the child pairing
"card shape" with "coach shape" and forces them to read.

Screen 15 needs one new card flag:

> **SME:** "At the bottom, show pictures only. **Do not show any word text below the pictures.**" ·
> "The word should not be displayed at any point during the question." · "When the child taps or
> starts dragging a picture, play only that picture's name."

`SORT_GENDER` always renders `<span class="lbl">${it.word_hi}</span>`. Add `data.hide_labels: true`
(default false). The word must still be **spoken** on tap — that is what makes it a listening task
rather than a picture-matching one.

Also: `.sort-tray` is `flex-wrap:nowrap` and overflows past ~6 tiles at 104 px. Screen 15 has
exactly 6. **Do not add a 7th without making the tray wrap.**

### 3.5 `MATRA_FILL` — drag the matra into the blank  🔴 new · screen 14

This is the module the SME asked for in the first round and that I substituted a pick for, because
nothing in any engine does it. It is now specified properly.

> **SME:** "Each coach will have an incomplete word with a blank space where the missing matra
> should be added. The child will drag the correct matra from the options given below and drop it
> into the blank space inside the correct coach. As soon as the child drops the correct matra, the
> word will be completed." · "ज + ा + ल = जाल · पर + ी = परी · ह + ि + रण = हिरण" ·
> "**Important correction: Please use 'हिरण' instead of 'हीरा / hira'.**"

Mockup `slide16_image16.png`.

```json
{
  "type": "MATRA_FILL",
  "phase": "practice",
  "prompt_hi": "",
  "audio": { "prompt": "vo_mf_prompt", "hint1": "...", "hint2": "...", "correct_jaal": "..." },
  "data": {
    "slots": [
      {"word": "जाल", "blank_after": 0, "matra": "ा", "img": "obj_jaal",  "audio": "vo_name_jaal"},
      {"word": "परी", "blank_after": 1, "matra": "ी", "img": "obj_pari",  "audio": "vo_name_pari"},
      {"word": "हिरण","blank_after": 0, "matra": "ि", "img": "obj_hiran", "audio": "vo_name_hiran"}
    ],
    "options": ["ा", "ि", "ी"],
    "reuse_options": true
  }
}
```

**`blank_after` is an index into the word's consonant sequence, not into the string.** It must not
be a character offset, because `ि` is a reordering matra: in `हिरण` the `ि` is stored after `ह` but
drawn before it, so `"ह" + "ि" + "रण"` renders as `हिरण` while a naive "insert at character
position 1" on the rendered glyph order puts it in the wrong place. Render the blank as a dashed box
**in the drawn position** and resolve the string by consonant index. The mockup shows `ह _ रा` with
a dashed box after `ह`, which is the stored order — correct as authored, but the drawn blank must
sit before the `ह`.

⚠️ The mockup still shows the **uncorrected** third word (`ह _ रा` + a diamond picture = हीरा). The
SME's note corrects it to **हिरण**. `हिरण` art already exists in this bundle
(`assets/Images/obj_hiran.png`). **हीरा must not be used** — it is `ही` + `रा`, i.e. two in-scope
matras, so it cannot be a single-matra item at all.

### 3.6 `POEM_SEARCH` — «मात्रा खोजो»  🔴 new · screen 16 · largest new module

> **SME:** "Use this as a final 'मात्रा खोजो' challenge." · "A large magnifying glass appears at the
> bottom-right. Child drags the magnifying glass over the poem. **Any word under the glass slightly
> enlarges.** Child taps/selects the word through the magnifying glass. Correct words remain
> highlighted." · Three rounds: "आ की मात्रा वाले शब्द ढूँढो।" → "अब छोटी इ की मात्रा वाले शब्द
> ढूँढो।" → "अब बड़ी ई की मात्रा वाले शब्द ढूँढो।"

Mockup `slide18_image18.png`.

Needs, none of which exists:

1. **A word-level hit-tested poem card.** `SENTENCE_FIND` tokenises a *sentence* into tappable
   chips; this needs a multi-line poem with per-word geometry that survives reflow.
2. **A draggable lens with proximity magnification** — the word under the lens scales up. This is a
   real interaction, not a decoration: it is how the child scans.
3. **Round state** — three sequential targets over the *same* stimulus, each round's found words
   staying highlighted, auto-advancing to the next round's VO on completion.
4. **The ghost actor** (§2.5).

> **SME:** "Remove extra decorative elements like: Ravi / kite / girl / tree / unnecessary
> background objects. Use a clean version of the existing UI so the child's attention stays on the
> activity." — the mockup's scenery is explicitly **not** wanted. Good: plain card, poem, lens.

**⚠️ The target list in the recommendation is incomplete. This is the one defect that would make the
screen mark correct answers wrong.** See §4.

---

## 4. 🔴 BLOCKING CONTENT DEFECT — the poem's target list is incomplete

The SME's poem:

> रवि लाया लाल पतंग, दिन में चमकी सूरज की किरण। नीम तले मीना गाए संग।

Audited every word programmatically against the three in-scope matras:

| matra | words the poem **actually** contains | SME's target list | **missing** |
|---|---|---|---|
| `ा` | लाया, लाल, **मीना**, **गाए** | लाया, लाल | **मीना, गाए** |
| `ि` | रवि, दिन, किरण | रवि, दिन, किरण | — ✅ complete |
| `ी` | नीम, मीना, **चमकी**, **की** | नीम, मीना | **चमकी, की** |

Out of scope and correctly not targets: पतंग (—), में (े), सूरज (ू), तले (े), संग (—).

**Why this blocks:** a child hunting `ी` who taps **चमकी** is *right*, and the screen as specified
would shake it and play «फिर से देखो।» That teaches the opposite of the lesson. Same for **गाए** in
round 1.

Note also that **मीना carries both `ी` and `ा`**, so it is a correct answer in two different rounds.
That is pedagogically fine — arguably good — but the module must support a word belonging to more
than one round, and "correct words remain highlighted" has to survive a word being found twice.

**Two ways to fix. Recommend A.**

- **A — complete the target list (keeps the SME's poem word-for-word).** Round `ा` = लाया, लाल,
  मीना, गाए · round `ि` = रवि, दिन, किरण · round `ी` = चमकी, की, नीम, मीना. Richer task, no rewrite.
  Requires multi-round membership for मीना.
- **B — edit the poem** so each in-scope matra appears only in intended targets. Smaller module, but
  it is the SME's poem and I am not rewriting it unasked.

**Needs an SME ruling before this screen is built.** Until then `POEM_SEARCH` should not be
scheduled — the target list is its entire data model.

---

## 5. 🟠 `ि` cannot be highlighted inside a word — carried forward, still true

Three of the new screens ask for the `ि` matra highlighted inside a rendered word (`बिल`, `दिन`,
`गति`, and step 6 of `MATRA_BUILD`). **The engine's in-word highlight does not work for `ि` and
adding it makes things worse, which was measured, not assumed.**

`_matraClipCols` rasterises the word and colours the ink columns after the consonant. `ा` and `ी`
sit to the right of their consonant, so this works — both are in `RIGHT_SPACING_MATRAS` in this
game's `engine_local` copy and both render correctly (verified on नाक and तीर). **`ि` is a
reordering matra**: typed after its consonant, drawn before it. With `ि` added to the set, `दिन`
mis-clips and **the red lands on part of the `द`** — the child is shown the wrong glyph as "the
matra", which is worse than no highlight. Tried, rendered, reverted; see
[`engine_local/CHANGES.md`](engine_local/CHANGES.md).

Today's fallback is the engine's `◌ि` callout under the word, with the demo hand pointing at it.

**For a proper fix the engine needs glyph-cluster–aware highlighting, not pixel columns** — i.e.
shape the word and colour the run belonging to the matra cluster, which needs the text shaped rather
than rasterised (e.g. render the word as per-cluster `<tspan>`s and recolour one). That is the real
answer and it would serve `े ै ो ौ ु ू` too — every matra lesson in the fleet. **Filed as a
separate engine request** (§10), because it is bigger than this game and it is the single highest-
leverage item in this handoff.

Interim, in priority order: (1) cluster-aware highlight — correct for all matras; (2) keep the `ि`
callout and have `MATRA_BUILD` step 3 make the *travel* of `ि` to the left the teaching moment,
which the SME explicitly asks for anyway and which partly compensates.

---

## 6. 🟠 TTS constraints the VO pipeline must respect — measured on this lesson

Hand these to whoever generates or records the new lines. All four were measured on this bundle,
not inferred.

1. **A bare akshara cannot be synthesised.** `क`, `न`, `द`, `त` all return `HTTP 400`. Carrier forms
   are unreliable *per letter*: «अक्षर त।» synthesises, «अक्षर न।» and «अक्षर द।» refuse after three
   retries. **This directly hits `MATRA_BUILD`'s `onset` clip** (step 4 speaks «जा», «बि», «की»).
   Two-character syllables are safer than bare consonants but must be verified one by one. Plan for
   **human recording of the onset clips** — they are the pedagogical core of the screen and cannot
   be allowed to be silent on some letters and spoken on others.
2. **An em-dash before a short final word truncates the clip.** Probed head to head, same words:
   em-dash `0.73–1.05 s` · comma `1.53–2.21 s` · danda `1.13–2.01 s`. Ten clips in the built lesson
   shipped half-spoken this way. **Use a comma or a danda.** Note several of the SME's new lines use
   the em-dash construction («यह शब्द है — जल।») — those need the substitution or human recording.
3. **A truncated clip passes every naive check** — it exists, it is a valid WAV, it is a normal file
   size. The detector that works is comparing a clip against other clips of the same text length;
   `_verify_assets.py` §3 does this and should be kept in the pipeline.
4. **The word दिन specifically triggers truncation on the Kore voice** regardless of retries; two
   clips in the built lesson are on Aoede for this reason. दिन appears on four of the new screens.

---

## 7. Content questions that need an SME ruling before build

| # | issue | detail | my recommendation |
|---|---|---|---|
| 1 | **Title conflict** | The note says the new heading is **«मात्राओं की रेल»**. The landing mockup (`slide03_image2.png`) reads **«शब्दों की रेल»** with the subtitle «हर शब्द को उसकी सही गाड़ी तक पहुँचाओ!». | Use **«मात्राओं की रेल»** — the note is the later, explicit instruction, and this lesson is about matras, not words generally. |
| 2 | **«बड़ी आ» is not standard** | The notes use both «बड़ी आ की मात्रा» and «आ की मात्रा», and slide 4's note says "(removing chota or bada)". Hindi pairs छोटी इ with बड़ी ई; **आ has no छोटी/बड़ी counterpart**, so «बड़ी आ» is non-standard. The built lesson currently says «बड़ी आ» — my error, worth fixing either way. | **«आ की मात्रा» · «छोटी इ की मात्रा» · «बड़ी ई की मात्रा».** Confirm and I will correct it across both the built lesson and this spec. |
| 3 | **Poem target list** | §4 — blocking. | Option A. |
| 4 | **हीरा → हिरण** | The SME's note corrects it; the mockup still shows हीरा. | हिरण, as instructed. Art already exists. हीरा is unusable anyway (two in-scope matras). |
| 5 | **On-screen text** | Notes say "no instruction text" on nine screens; mockup `slide11_image12.png` prints the instruction. | Notes win — VO only. Confirm. |
| 6 | **The ghost** | New character, fleet-wide precedent is the hand or Swiftie. | Use **Swiftie with a magnifying glass**; same function, no new art line, no new character to validate with children. |
| 7 | **«टैप कीजिए» vs «टैप करो»** | The new lines mix aap («कीजिए», «डालिए», «बोलकर देखिए») and tum («ढूँढो», «टैप करो», «सोचो»), sometimes in the same screen. The built lesson is tum throughout; the three shared phase-gate clips are aap. | One register for the whole of G2/G3. **Recommend tum**, matching the built lesson and the SME's own round-3 copy — but this is a call for the SME, and it also settles the long-open phase-gate mismatch. |
| 8 | **Screen count** | 16 recommended screens vs the 3-phase contract's `phase_distribution`. The teach phase alone is now 8 screens (3 build + 3 two-example + intro + landing). | Fine, but the teach phase is long and fully locked. Consider interleaving one guided screen after each matra's build+examples pair, so the child acts every third screen instead of waiting eight. |

---

## 8. Build order

Nothing here is blocked on the SME except `POEM_SEARCH`.

**Phase 1 — the shell (unblocks six screens)**
1. `TRAIN_CHROME` (§2.1) with all seven coach states
2. `scaffold_rules` 3-attempt ladder (§2.2) — additive, defaults preserve current behaviour
3. The five new SFX (§2.4) — asset request, parallel
4. Empty-`prompt_hi` shell check (§2.3)

**Phase 2 — the reskins (six screens playable)**
5. `TRAIN_TAP` (§3.3)
6. `TRAIN_SORT` + `hide_labels` (§3.4)

**Phase 3 — the teaching**
7. `MEET_LETTER` `examples[]` sequencer (§3.2) — small, high value
8. `MATRA_BUILD` (§3.1) — the concept's centrepiece; needs the onset clips from §6.1 first
9. `MATRA_FILL` (§3.5)

**Phase 4 — cluster-aware matra highlight (§5)** — fleet-wide; can run in parallel from the start,
and every screen above gets better when it lands.

**Phase 5 — `POEM_SEARCH` (§3.6)** — only after the §4 ruling.

---

## 9. What to do with the lesson that already exists

The current build is complete and verified: 19 slides, 13 illustrations, 95 clips, receipt
0 FAIL / 0 WARN, 108/108 assets served, the SME's hint ladder verified firing live. It teaches the
same outcome with the standard stage.

Three options, and this is the SME's and the product lead's call, not mine:

- **Ship it now, build the train as v2.** The outcome is covered today; the train is a better
  vehicle for it. Lowest risk, gets Grade 2 content in front of children.
- **Hold and build the train.** Better final product, but the whole redesign is ~9 pieces of engine
  work and this skill ships nothing meanwhile.
- **Hybrid** — ship the current build, and land Phase 1+2 (train shell + reskins) as an update to
  *this* card, keeping the existing teach slides until `MATRA_BUILD` lands.

I would take the **hybrid**: the train shell is the thing that makes the lesson feel like one game,
it unblocks the most screens for the least work, and the existing teach slides are already correct
and voiced.

Either way, two content fixes from §7 (**«आ की मात्रा»** not «बड़ी आ», and **हिरण** confirmed)
should go into the current build regardless — they are corrections, not redesign.

---

## 10. Engine requests filed

Filed through the kit's queue (`engine_request.py add`), one per change, so they enter the same
pipeline as every other game's asks rather than living only in this document:

Queue: `SME_LXD_Kit/engine_requests/`, rollup at `SME_LXD_Kit/ENGINE_REQUESTS.md`. Filed under
session `sme-lxd-matra-train`, **8 requests, 5 blocking**. Each one states what I checked to rule out
a card-only fix, which `engine_request.py` requires.

| request id | ask | scope | blocking |
|---|---|---|---|
| `…-l02-s01` | `TRAIN_CHROME` shared renderer | this game + any future themed shell | **yes** — 7 screens |
| `…-l02-s01-2` | 3-attempt ladder: `hand_on_attempt` / `reveal_on_attempt` / `silent_on_late_correct` | fleet-wide, additive | **yes** — 9 screens |
| `…-l02-s01-3` | `MATRA_BUILD` module | this game; reusable by every matra lesson | **yes** — 3 screens |
| `…-l02-s01-4` | `MATRA_FILL` module | this game; reusable | **yes** — 1 screen |
| `…-l02-s01-5` | `SORT_GENDER` `hide_labels` flag | fleet-wide, additive, ~3 lines | **yes** — 1 screen |
| `…-l02-s01-6` | `MEET_LETTER` `examples[]` sequencer | fleet-wide, additive | no — 3 screens degrade to one example |
| `…-l02-s01-7` | `POEM_SEARCH` + lens + guide actor | this game | no — **do not schedule until §4 is ruled** |
| `…-l02-s01-8` | **cluster-aware matra highlight** (replaces pixel-column clipping) | **fleet-wide — every matra lesson** | no, but **highest leverage in the batch** |

Full ids are prefixed `20260916-224551-hi02h11`.

Two further asks are carried over from the *build* of this lesson and are unrelated to the redesign
— they are recorded in [`_BUILD_RECEIPT.md`](_BUILD_RECEIPT.md) rather than re-filed here:
`concept_strip` landings never receive the glow class (11 shipped bundles affected), and divergent
engine code under one `ENGINE_VERSION` string (which caused a silently empty landing strip on this
very lesson).

---

## 11. Files in this handoff

| file | what it is |
|---|---|
| `DEV_HANDOFF_HI02H11_L02_S01.md` | this document — rationale, module design, decisions needed |
| [`_SME_RECOMMENDATIONS.md`](_SME_RECOMMENDATIONS.md) | the SME's 16 screen recommendations **verbatim**, unedited |
| [`dev_spec_HI02H11_L02_S01.json`](dev_spec_HI02H11_L02_S01.json) | machine-readable: screen order, content, VO, mappings, proposed schemas, asset list |
| [`_SME_MOCKUPS/`](_SME_MOCKUPS/) | the SME's visual mockups, extracted from the deck, named by slide |
| [`_BUILD_RECEIPT.md`](_BUILD_RECEIPT.md) | what the existing 19-slide build contains and the 5 defects fixed during it |
| [`engine_local/CHANGES.md`](engine_local/CHANGES.md) | the 3 per-game engine changes and the measured `ि` revert |
| [`_verify_assets.py`](_verify_assets.py) | the asset receipt, incl. the truncation check — keep this in the pipeline |

**Nothing in the built lesson has been changed by this handoff.** The recommendations are recorded
and specified; per the agreed workflow they are applied only on an explicit go-ahead. The two
content corrections in §7 (items 2 and 4) are the ones I would apply to the existing build
immediately on your word, since they are corrections rather than redesign.
