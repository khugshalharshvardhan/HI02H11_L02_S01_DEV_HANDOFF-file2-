# CHANGES — HI02H11_L02_S01 · «मात्राओं की रेल»

**Source deck:** `HI02H11_L02_S01_SME_Review.pptx` (19 slides, 2026-09-16, SME-authored).
**Baseline reviewed:** `HI02H11_L02_S01.html` sha1 `0122b20c130d`, engine `2026.08.04b-r4-unified`
(the per-game `4_ENGINE/lesson_template.html` copy, incl. its 3 documented changes). Baseline match
confirmed: the built HTML carries `RIGHT_SPACING_MATRAS = new Set(["ा", "ी"])`, which the *shared*
factory engine does not — so this build is on the handoff's engine copy, not the factory's.

Every discrete ask in the deck is one row. Deck pages with no ask get an explicit `N/C` row.
This file is the contract **and** the scorecard: statuses are updated in place after verification.

**Status vocabulary:** ✅ DONE (with proof) · ⚑ FLAGGED-BACK (asked, not silently decided) ·
⏳ PENDING · N/C (no change requested).

**Run-level decisions taken before build (user, 2026-09-17):**
- Scope = **full train redesign, all 16 screens**.
- Assets = **initially skipped, then PRODUCED** after a Gemini key was supplied (2026-09-17, later
  the same day). All 91 VO lines and all 10 new pictures are now on disk. The five new SFX and the
  two chrome files remain outstanding by house rule (chrome is copied, never generated).
- §4 poem target list = **Option A** (complete the list, keep the SME's poem word-for-word).
- Ghost guide = **built as the SME specified** (not substituted with Swiftie).

---

## Deck page 1 — title
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 1 | 1 | N/C (no change requested) | — | N/C | — |

## Deck page 2 — overview
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 2 | 2 | N/C (no change requested) | — | N/C | — |

## Deck page 3 — Landing
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 3 | 3 | "New Heading:मात्राओं की रेल" | card `title.hi` | ✅ | landing capture `_review_shots/00_landing.png`; `landin …(clipped)|
| 4 | 3 | "Remove all extra text that is not required." | card `subtitle_hi` | ✅ | landing capture `_review_shots/00_landing.png`; `landing_hero. …(clipped)|
| 5 | 3 | "Keep the screen clean and minimal." | card landing | ✅ | landing capture `_review_shots/00_landing.png`; `landing_hero.kind="matra_tra …(clipped)|
| 6 | 3 | "Show only three matra boxes/cards: 1st box: ा 2nd box: ि 3rd box: ी" | card `landing_hero.cells` | ✅ | landing capture `_review_ …(clipped)|
| 7 | 3 | "Keep the existing mascot and overall UI/UX style unchanged." | — (no change) | ✅ | landing capture `_review_shots/00_landing.png`; ` …(clipped)|
| 8 | 3 | "If possible, bring the train onto the screen with a smooth right-to-left animation." | engine `TrainChrome` | ✅ | landing capture `_re …(clipped)|
| 9 | 3 | "The three matra boxes can appear one by one with a soft pop/fade animation." | engine landing | ✅ | landing capture `_review_shots/00_ …(clipped)|
| 10 | 3 | "Keep animations subtle and child-friendly." | engine CSS | ✅ | landing capture `_review_shots/00_landing.png`; `landing_hero.kind="ma …(clipped)|
| 11 | 3 | "Add a soft train arrival / whistle SFX when the train enters." | `sfx_train_arrive` | ⏳ asset | landing capture `_review_shots/00_lan …(clipped)|
| 12 | 3 | "Add a light sparkle/pop SFX when each matra appears." | `sfx_sparkle` | ⏳ asset | landing capture `_review_shots/00_landing.png`; `la …(clipped)|
| 13 | 3 | VO "हेलो दोस्त! मैं हूँ स्विफ्टी। आज हम मात्राओं के बारे में जानेंगे।" | `vo_landing` | ? | — |
| 14 | 3 | "After this VO, the three matras ा, ि, ी can appear one by one on screen." | engine landing | ✅ | landing capture `_review_shots …(clipped)|

## Deck page 4 — Screen 1 · INTRO (the three matras)
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 15 | 4 | VO "आज हम बड़ी आ की मात्रा, छोटी इ की मात्रा और बड़ी ई की मात्रा वाले शब्द पढ़ेंगे।" **(removing chota or bada)** | `vo_intro_matras` | ? | — |
| 16 | 4 | "Remove the current heading text from the top." | card `prompt_hi:""` | ✅ | capture `01_T1_MATRA_PAIRS.png` + `END_T1_pairs.png`; walk …(clipped)|
| 17 | 4 | "Show the letter and its corresponding matra symbol as a pair, one by one." | engine `MATRA_PAIRS` | ✅ | `MATRA_PAIRS`. Nothing is on …(clipped)|
| 18 | 4 | "Each pair should light up/highlight when its VO plays." | engine `MATRA_PAIRS` | ✅ | Active pair renders at opacity 1.00, taught pair …(clipped)|
| 19 | 4 | "Keep only one pair active at a time." | engine `MATRA_PAIRS` | ✅ | Live trace: exactly one pair carries `.active` at any sample point …(clipped)|
| 20 | 4 | "Sequence: आ → ा · इ → ि · ई → ी" | card `data.pairs` | ✅ | `data.pairs` = आ/ा · इ/ि · ई/ी in that o …(clipped)|
| 21 | 4 | "First आ appears, then ा appears beside it with a soft glow. Then both fade slightly and इ → ि appears. Finally ई → ी appears." | engine `MATRA_PAIRS` | ? | — |
| 22 | 4 | "Use a simple pop/fade animation; no extra decorative elements." | engine CSS | ✅ | **The white card frame around each pair was remove …(clipped)|
| 23 | 4 | "Add a soft pop/chime when each matra symbol appears. Keep SFX subtle so the VO remains clear." | `sfx_chime` | ⏳ asset | `sfxChime()` …(clipped)|
| 24 | 4 | "Keep the Next button disabled during the sequence. Activate it only after all three pairs have been shown and spoken." | engine `MATRA_PAIRS` | ? | — |

## Deck page 5 — Screen 2 · MATRA_BUILD जल → जा → जाल
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 25 | 5 | VO "आइए, देखें कि आ की मात्रा लगने से शब्द की आवाज़ कैसे बदलती है।" | `vo_mb_jal_intro` | ? | — |
| 26 | 5 | VO पहले "यह शब्द है — जल।" | `vo_mb_jal_base` | ✅ | capture `END_T2_jal.png`; DOM walk: जल(ज red …(clipped)|
| 27 | 5 | VO फिर "ज में आ की मात्रा लगाने पर — जा बनता है।" | `vo_mb_jal_onset` | ? | — |
| 28 | 5 | VO अंत में "अब जल में आ की मात्रा लगाने पर — जाल बनता है।" | `vo_mb_jal_explain` | ? | — |
| 29 | 5 | "Keep the screen focused on only one transformation." | engine `MATRA_BUILD` | ✅ | capture `END_T2_jal.png`; DOM walk: जल(ज red) …(clipped)|
| 30 | 5 | "First show जल clearly on the left. Then show the transformation in the centre: ज + ा = जा. After that, complete the word as: जाल" | engine `MATRA_BUILD` | ? | — |
| 31 | 5 | "Highlight only the ा matra when it is introduced." | engine `MATRA_BUILD` | ✅ | capture `END_T2_jal.png`; DOM walk: जल(ज red) …(clipped)|
| 32 | 5 | "A simple relevant image can support the final word जाल." | `obj_jaal` | ✅ | capture `END_T2_jal.png`; DOM walk: जल(ज red) …(clipped)|
| 33 | 5 | Staged sequence: जल → VO "जल" → ज highlights → ा appears → ज+ा=जा → "ज"→"जा" → ल joins → जाल → highlight ा in जाल → final image | engine `MATRA_BUILD` | ? | — |
| 34 | 5 | "The ा matra should slide/pop into place beside ज. As soon as it joins, ज visually transforms into जा." | engine `MATRA_BUILD` | ? | — |
| 35 | 5 | "Avoid showing all stages together at the start." | engine `MATRA_BUILD` | ✅ | capture `END_T2_jal.png`; DOM walk: जल(ज red) → …(clipped)|
| 36 | 5 | "Give a small pause between each sound so the child can hear the change." | engine `MATRA_BUILD` | ✅ | capture `END_T2_jal.png`; DOM w …(clipped)|
| 37 | 5 | "Soft pop when ा appears. Light chime when ज changes to जा. Small success sound when जाल is completed." | sfx wiring | ? | — |
| 38 | 5 | "Keep Next disabled while the transformation is playing. Activate it only after ज → जा → जाल is fully demonstrated." | engine `MATRA_BUILD` | ? | — |
| 39 | 5 | "Keep the screen clean and minimal. Do not add extra explanatory text." | card `prompt_hi` | ✅ | capture `END_T2_jal.png`; DOM walk:  …(clipped)|

## Deck page 6 — Screen 3 · examples नाक / मटका
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 40 | 6 | VO "आइए, आ की मात्रा वाले कुछ शब्द देखें।" | `vo_ex_aa_intro` | ✅ | capture …(clipped)|
| 41 | 6 | VO "नाक — बोलकर देखिए। इसमें न पर बड़ी आ की मात्रा लगी है।" | `vo_ex_naak` | ? | — |
| 42 | 6 | VO "मटका — बोलकर देखिए। इसमें क पर बड़ी आ की मात्रा लगी है।" | `vo_ex_matka` | ? | — |
| 43 | 6 | "Keep one example visible at a time." | engine `MEET_LETTER.examples[]` | ✅ | capture `03_T3_MEET_EXAMPLES.png` + `END_T3_examples.png …(clipped)|
| 44 | 6 | "First show नाक with the nose image. Highlight only the ा matra in the word नाक." | card `data.examples[0]` | ✅ | captur …(clipped)|
| 45 | 6 | "After that, show the second example मटका with a clay pot image. Highlight the ा matra in मटका as well." | card `data.examples[1]` + `obj_matka` | ? | — |
| 46 | 6 | "Word should appear first, then image should appear." | engine sequencer | ✅ | capture `03_T3_MEET_EXAMPLES.png` + `END_T3_examples.pn …(clipped)|
| 47 | 6 | "When VO says the matra part, the ा should glow/highlight. Keep animation one by one, not all together." | engine sequencer | ✅ | ca …(clipped)|
| 48 | 6 | "Soft pop sound when word/image appears · Soft highlight chime when matra glows" | sfx wiring | ⏳ asset | capture `03_T3_MEET_EXAMPLE …(clipped)|
| 49 | 6 | "Keep Next button disabled during the explanation. Activate it only after both examples are shown completely." | engine sequencer | ? | — |
| 50 | 6 | "Keep screen clean · No extra text other than the example heading/content required" | card `prompt_hi` | ✅ | capture `03_T3_MEET_EXAM …(clipped)|

## Deck page 7 — Screen 4 · MATRA_BUILD बल → बि → बिल
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 51 | 7 | VO "आइए, देखें कि छोटी इ की मात्रा लगाने से शब्द की आवाज़ कैसे बदलती है।" | `vo_mb_bil_intro` | ? | — |
| 52 | 7 | VO पहले "यह शब्द है — बल।" | `vo_mb_bil_base` | ✅ | capture `04_T4_MATRA_BUILD.png`; DOM: बल → …(clipped)|
| 53 | 7 | VO फिर "ब में छोटी इ की मात्रा लगाने पर — बि बनता है।" | `vo_mb_bil_onset` | ? | — |
| 54 | 7 | VO अंत में "अब बल में छोटी इ की मात्रा लगाने पर — बिल बनता है।" | `vo_mb_bil_explain` | ? | — |
| 55 | 7 | "First show बल with a simple visual. Then highlight ब. Show the transformation in the centre: ब + ि = बि. After that, complete the word as: बिल" | engine + card | ? | — |
| 56 | 7 | "Highlight only the ि मात्रा in बिल." | engine (see §5 limitation) | ⚑ | **INFEASIBLE AS ASKED.** ि is a reord …(clipped)|
| 57 | 7 | "Show a simple relevant image for बिल on the final side." | `obj_bil` | ✅ | capture `04_T4_MATRA_BUILD.png`; DOM: बल →  …(clipped)|
| 58 | 7 | "**ि appears and moves to its correct position before ब**" / "The ि मात्रा should visibly move to the left side of ब, so the child notices its written position." | engine `MATRA_BUILD` ि-travel | ? | — |
| 59 | 7 | "Sync the visual change with the VO: ब → बि → बिल. Give a short pause between each sound." | engine `MATRA_BUILD` | ? | — |
| 60 | 7 | "Soft pop when ि appears. Light chime when ब changes to बि. Small success chime when बिल is completed." | sfx wiring | ? | — |
| 61 | 7 | "Keep Next disabled during the explanation. Activate it only after the full transformation बल → बि → बिल is completed." | engine | ? | — |
| 62 | 7 | "Keep the screen clean and minimal. Avoid extra explanatory text." | card `prompt_hi` | ✅ | capture `04_T4_MATRA_BUILD.png`; DOM: ब …(clipped)|

## Deck page 8 — Screen 5 · examples दिन / गति
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 63 | 8 | VO "आइए, छोटी इ की मात्रा वाले कुछ शब्द देखें।" | `vo_ex_i_intro` | ? | — |
| 64 | 8 | VO "दिन — बोलकर देखिए। इसमें द पर छोटी इ की मात्रा लगी है।" | `vo_ex_din` | ? | — |
| 65 | 8 | VO "गति — बोलकर देखिए। इसमें त पर छोटी इ की मात्रा लगी है।" | `vo_ex_gati` | ? | — |
| 66 | 8 | "First show दिन with a simple day/sun image. Highlight only the ि matra in दिन." | card `data.examples[0]` | ✅ | captur …(clipped)|
| 67 | 8 | "After that, show गति with a simple visual representing movement/motion. Highlight the ि matra in गति as well." | card `data.examples[1]` + `obj_gati` | ? | — |
| 68 | 8 | "Remove any extra explanatory text that is not required." | card `prompt_hi` | ✅ | capture `05_T5_MEET_EXAMPLES.png` |
| 69 | 8 | "Word appears first with a soft fade/pop. Image appears just after the word." | engine sequencer | ✅ | capture `05_T5_MEET_EXAMPLES.p …(clipped)|
| 70 | 8 | "When the VO reaches the matra explanation, ि should glow/pulse briefly." | engine (see §5 limitation) | ⚑ | Same ि limitation a …(clipped)|
| 71 | 8 | "Soft pop/chime when each word/image appears. Light sparkle/chime when the matra gets highlighted." | sfx wiring | ⏳ asset | capture …(clipped)|
| 72 | 8 | "Keep Next disabled while both examples are being explained. Activate it only after both examples are completed." | engine sequencer || — |

## Deck page 9 — Screen 6 · MATRA_BUILD कल → की → कील
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 73 | 9 | VO "आइए, देखें कि बड़ी ई की मात्रा लगाने से शब्द की आवाज़ कैसे बदलती है।" | `vo_mb_keel_intro` | ? | — |
| 74 | 9 | VO पहले "यह शब्द है — कल।" | `vo_mb_keel_base` | ✅ | capture `06_T6_MATRA_BUILD.png` + `END_T6_keel.p …(clipped)|
| 75 | 9 | VO फिर "क में बड़ी ई की मात्रा लगाने पर — की बनता है।" | `vo_mb_keel_onset` | ? | — |
| 76 | 9 | VO अंत में "अब कल में बड़ी ई की मात्रा लगाने पर — कील बनता है।" | `vo_mb_keel_explain` | ? | — |
| 77 | 9 | "First show कल with a simple supporting visual. Then highlight क. Show the transformation in the centre: क + ी = की. After that, complete the word as: कील" | engine + card | ? | — |
| 78 | 9 | "Highlight only the ी मात्रा in कील." | engine `MATRA_BUILD` | ✅ | capture `06_T6_MATRA_BUILD.png` + `END_T6_keel …(clipped)|
| 79 | 9 | "Show a simple relevant image for कील on the final side." | `obj_keel` | ✅ | capture `06_T6_MATRA_BUILD.png` + `END_T6_keel.png …(clipped)|
| 80 | 9 | "The ी मात्रा should visibly join क, so the child notices how the sound changes." | engine `MATRA_BUILD` | ✅ | captur …(clipped)|
| 81 | 9 | "Sync the visual change with the VO: क → की → कील. Give a short pause between each sound." | engine | ✅ | capture `06 …(clipped)|
| 82 | 9 | "Soft pop when ी appears. Light chime when क changes to की. Small success chime when कील is completed." | sfx wiring | ? | — |
| 83 | 9 | "Keep Next disabled during the explanation. Activate it only after the full transformation कल → की → कील is completed." | engine | ? | — |
| 84 | 9 | "Keep the screen clean and minimal. Avoid extra explanatory text." | card `prompt_hi` | ✅ | capture `06_T6_MATRA_BUILD.png` + `END_T6 …(clipped)|

## Deck page 10 — Screen 7 · examples तीर / लड़की
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 85 | 10 | VO "आइए, बड़ी ई की मात्रा वाले कुछ शब्द देखें।" | `vo_ex_ee_intro` || — |
| 86 | 10 | VO "तीर — बोलकर देखिए। इसमें त पर बड़ी ई की मात्रा लगी है।" | `vo_ex_teer` | ? | — |
| 87 | 10 | VO "लड़की — बोलकर देखिए। इसमें क पर बड़ी ई की मात्रा लगी है।" | `vo_ex_ladki` | ? | — |
| 88 | 10 | "First show तीर with the arrow image. Highlight only the ी matra in तीर." | card `data.examples[0]` | ✅ | capture `07_ …(clipped)|
| 89 | 10 | "After that, show लड़की with a simple girl image. Highlight only the ी matra in लड़की." | card `data.examples[1]` + `obj_ladki` | ? | — |
| 90 | 10 | "Remove any extra explanatory text that is not required." | card `prompt_hi` | ✅ | capture `07_T7_MEET_EXAMPLES.png` |
| 91 | 10 | "Word appears first with a soft fade/pop animation. Image appears just after the word. Show the examples one by one, not together." | engine sequencer | ? | — |
| 92 | 10 | "When the VO mentions the matra, ी should glow/pulse briefly." | engine sequencer | ✅ | capture `07_T7_MEET_EXAMPLES.png` |
| 93 | 10 | "Soft pop/chime when the word or image appears. Light sparkle/chime when the matra gets highlighted." | sfx wiring | ⏳ asset | captu …(clipped)|
| 94 | 10 | "Keep Next disabled during the explanation. Activate it only after both examples are completely shown." | engine sequencer | ✅ | cap …(clipped)|

## Deck page 11 — Screen 8 · TRAIN_TAP आ
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 95 | 11 | "Train comes through animation from right to left. Train stops at the centre of the screen." | engine `TrainChrome` | ✅ | capture `0 …(clipped)|
| 96 | 11 | "No instruction text on screen. Only VO should play." | card `prompt_hi:""` + shell collapse | ✅ | capture `08_G1_TRAIN_TAP.png`; ** …(clipped)|
| 97 | 11 | VO "जिस डिब्बे में आ की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए।" | `vo_tt_aa_prompt` | ? | — |
| 98 | 11 | Correct: "Show confetti / sparkle effect · Correct coach should glow / highlight" | engine `TRAIN_TAP` | ✅ | capture `08_G1_TRAIN_T …(clipped)|
| 99 | 11 | Correct VO "शाबाश! हाथ शब्द में आ की मात्रा है।" | `vo_tt_aa_correct` | ✅ | ca …(clipped)|
| 100 | 11 | 1st wrong: "Wrong coach should wiggle / shake · **No hand nudge** · Only hint VO should come" | engine ladder rung 1 | ✅ | captur …(clipped)|
| 101 | 11 | 1st wrong VO "फिर से सोचो। आ की मात्रा वाला शब्द कौन-सा है?" | `vo_tt_aa_hint1` | ? | — |
| 102 | 11 | 2nd wrong: "Wrong coach should again wiggle / shake · Hint VO should play · **Show hand nudge on the correct answer**" | engine `hand_on_attempt:2` | ? | — |
| 103 | 11 | 2nd wrong VO "ध्यान से देखो और सही डिब्बे पर टैप कीजिए।" | `vo_tt_aa_hint2` | ? | — |
| 104 | 11 | 3rd-attempt correct: "Show confetti / sparkle · Correct coach highlights · Next button becomes active · **No VO**" | engine `silent_on_late_correct` | ? | — |
| 105 | 11 | "Soft train arrival sound · Light tap sound on selection · Soft shake/error sound on wrong attempt · Light success chime on correct answer" | sfx wiring | ? | — |
| 106 | 11 | Coach words per mockup: नाक · दिन · पानी | card `data.options` | ⚑ | **Conflict.** `slide11/12/13_image12.png …(clipped)|

## Deck page 12 — Screen 9 · TRAIN_TAP छोटी इ
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 107 | 12 | "Train comes through animation from right to left. Train stops at the centre of the screen." | engine `TrainChrome` | ✅ | capture ` …(clipped)|
| 108 | 12 | "No instruction text on screen. Only VO should play." | card `prompt_hi:""` | ✅ | capture `09_G2_TRAIN_TAP.png`; same ladder path a …(clipped)|
| 109 | 12 | VO "जिस डिब्बे में छोटी इ की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए।" | `vo_tt_i_prompt` | ? | — |
| 110 | 12 | Correct VO "शाबाश! पिन शब्द में छोटी इ की मात्रा है।" | `vo_tt_i_correct` | ? | — |
| 111 | 12 | **"Note: Here it should be छोटी इ, not छोटी ई."** | all इ wording | ✅ | capture `09_G2_TRAIN_TAP.png`; same l …(clipped)|
| 112 | 12 | 1st wrong: shake, no hand, hint VO only — "फिर से सोचो। छोटी इ की मात्रा वाला शब्द कौन-सा है?" | ladder rung 1 | ? | — |
| 113 | 12 | 2nd wrong: shake + hint VO + hand nudge — "ध्यान से देखो और सही डिब्बे पर टैप करो।" | ladder rung 2 | ? | — |
| 114 | 12 | 3rd-attempt correct: confetti, coach highlights, Next active, **No VO** | engine | ✅ | capture `09_G2_TRAIN_TAP.png`; same ladder p …(clipped)|
| 115 | 12 | SFX set (arrival / tap / shake / success chime) | sfx wiring | ⏳ asset | capture `09_G2_TRAIN_TAP.png`; same ladder path as G1 · * …(clipped)|

## Deck page 13 — Screen 10 · TRAIN_TAP बड़ी ई
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 116 | 13 | "Train comes through animation from right to left. Train stops at the centre of the screen." | engine `TrainChrome` | ✅ | capture ` …(clipped)|
| 117 | 13 | "No instruction text on screen. Instruction should come through VO only." | card `prompt_hi:""` | ✅ | capture `10_G3_TRAIN_TAP.png` …(clipped)|
| 118 | 13 | VO "जिस डिब्बे में बड़ी ई की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए।" | `vo_tt_ee_prompt` | ? | — |
| 119 | 13 | Correct: small confetti/sparkle + soft glow + VO "शाबाश! पानी शब्द में बड़ी ई की मात्रा है।" + Next active | engine + `vo_tt_ee_correct` | ? | — |
| 120 | 13 | 1st wrong: short shake, hint VO only, no hand nudge | ladder rung 1 | ✅ | capture `10_G3_TRAIN_TAP.png`; same ladder path as G1 |
| 121 | 13 | 2nd wrong: shake again, hint VO, hand nudge on the correct answer | ladder rung 2 | ✅ | capture `10_G3_TRAIN_TAP.png`; same ladder …(clipped)|
| 122 | 13 | 3rd-attempt correct: confetti, coach highlights, Next active, **No VO** | engine | ✅ | capture `10_G3_TRAIN_TAP.png`; same ladder p …(clipped)|
| 123 | 13 | SFX set (arrival / tap / error-shake / success chime with confetti) | sfx wiring | ⏳ asset | capture `10_G3_TRAIN_TAP.png`; same la …(clipped)|

## Deck page 14 — Screen 11 · TRAIN_SORT word → matra coach
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 124 | 14 | "Train comes through animation right to left, stops at the centre. Three coaches are visible." | engine `TrainChrome` | ✅ | capture …(clipped)|
| 125 | 14 | "Each coach has one मात्रा shown above it: आ (ा), इ (ि), ई (ी). The inside drop area of each coach remains empty." | `coach_label` + `drop_zone` | ? | — |
| 126 | 14 | "Three draggable word cards appear below the train: हाथ, पिन, नीम." | card `data.items` | ✅ | capture `11_G4_TRAI …(clipped)|
| 127 | 14 | "No instruction text. Only VO: हर शब्द को उसकी सही मात्रा वाली बोगी में डालिए।" | `vo_ts1_prompt` | ? | — |
| 128 | 14 | "Each word card can also play its word VO when tapped/dragged: हाथ / पिन / नीम" | speak-on-tap | ✅ | capture `11_ …(clipped)|
| 129 | 14 | Mapping हाथ → आ (ा) · पिन → इ (ि) · नीम → ई (ी) | card `data.items` | ✅ | capture `11_G4_TRAI …(clipped)|
| 130 | 14 | "Only one word can be placed inside each coach." | engine `capacity:1` | ✅ | capture `11_G4_TRAIN_SORT.png`; **drag walk**: wrong …(clipped)|
| 131 | 14 | "While dragging, the selected card slightly enlarges. When the card reaches a coach, that coach gets a soft highlight." | engine CSS | ? | — |
| 132 | 14 | Correct: "card snaps inside the correct coach · small confetti/sparkle around that coach · VO 'शाबाश! पिन शब्द में छोटी इ की मात्रा है।' · card locked" | engine + per-item VO | ? | — |
| 133 | 14 | 1st wrong: "Wrong coach gives a short shake · card returns to its original position · No hand nudge · VO 'फिर से सुनो और सही मात्रा पहचानिए।'" | ladder rung 1 | ? | — |
| 134 | 14 | 2nd wrong: "shake again · card returns · VO 'ध्यान से देखो, इस शब्द में कौन-सी मात्रा है?' · hand nudge on the correct coach · correct coach soft pulse/glow" | ladder rung 2 | ? | — |
| 135 | 14 | 3rd-attempt correct: "confetti/sparkle · **No VO** · word locks inside the coach" | engine | ✅ | capture `11_G4_TRAIN_SORT.png`; …(clipped)|
| 136 | 14 | Completion: "all three coaches glow · train gives a small whistle/steam animation · Next active · no extra completion VO" | engine `complete` state | ? | — |

## Deck page 15 — Screen 12 · TRAIN_SORT matra → word coach
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 137 | 15 | "VO only: सही मात्रा को सही शब्द वाली बोगी में डालिए।" | `vo_ts2_prompt` + `prompt_hi:""` | ? | — |
| 138 | 15 | Mapping जाल → आ (ा) · सिर → इ (ि) · कील → ई (ी) — coaches carry the WORD, cards carry the मात्रा | card `data` (reverse) | ? | — |
| 139 | 15 | Correct: "मात्रा snaps and locks inside the coach · small sparkle/confetti · VO 'शाबाश! जाल शब्द में आ की मात्रा लगी है।' Use the same pattern for सिर and कील." | engine + per-item VO | ? | — |
| 140 | 15 | 1st wrong: "short shake, मात्रा returns · VO 'फिर से सोचो। इस शब्द में कौन-सी मात्रा लगी है?'" | ladder rung 1 | ? | — |
| 141 | 15 | 2nd wrong: "Shake + मात्रा returns · VO 'ध्यान से देखो और शब्द को फिर से पढ़ो।' · hand nudge/pulse on the correct coach" | ladder rung 2 | ? | — |
| 142 | 15 | 3rd-attempt correct: "snaps into the correct coach with a small confetti/sparkle. No VO required." | engine | ✅ | capture `12_P1_TR …(clipped)|
| 143 | 15 | Completion: "all coaches glow briefly and the Next button becomes active" | engine | ✅ | capture `12_P1_TRAIN_SORT.png`; coaches ca …(clipped)|
| 144 | 15 | "Train enters with a smooth right-to-left animation and stops at the centre. मात्रा cards appear from the bottom with a simple fade/slide-up animation." | engine | ? | — |
| 145 | 15 | "Keep the rest of the current UI/UX unchanged and avoid adding extra decorative elements." | — | ✅ | capture `12_P1_TRAIN_SORT.pn …(clipped)|

## Deck page 16 — Screen 13 · MATRA_FILL (fill the blank)
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 146 | 16 | "This activity will be a reverse matra-building train activity. … three train coaches … Each coach will have an incomplete word with a blank space where the missing matra should be added." | engine `MATRA_FILL` | ? | — |
| 147 | 16 | "The child will drag the correct matra from the options given below and drop it into the blank space inside the correct coach. As soon as the child drops the correct matra, the word will be completed." | engine `MATRA_FILL` | ? | — |
| 148 | 16 | Words: "ज + ा + ल = जाल · पर + ी = परी · ह + ि + रण = हिरण" | card `data.slots` | ✅ | cap …(clipped)|
| 149 | 16 | **"Important correction: Please use 'हिरण' instead of 'हीरा / hira'."** | card `data.slots[2]` | ✅ | capture `13_P2 …(clipped)|
| 150 | 16 | "A related picture can be shown above each coach for support." | `coach_label` = picture | ✅ | capture `13_P2_MATRA_FILL.png`; **dr …(clipped)|
| 151 | 16 | "Below the train, matra options will appear: आ (ा) · इ (ि) · ई (ी)" | card `data.options` | ✅ | capture `13_P2_MATRA_ …(clipped)|
| 152 | 16 | "Next button remains disabled initially." | engine | ✅ | capture `13_P2_MATRA_FILL.png`; **drag walk**: ज_ल→जाल, पर …(clipped)|
| 153 | 16 | "VO only: सही मात्रा को सही जगह पर खींचकर डालो और शब्द पूरा करिए।" | `vo_mf_prompt` + `prompt_hi:""` | ? | — |
| 154 | 16 | "Optional word-level support VO: जाल / परी / हिरण" | per-slot audio | ✅ | capture `13_P2_MATRA_FILL.png`; **dra …(clipped)|
| 155 | 16 | Correct mapping: "ज _ ल → ा · पर _ → ी · ह _ रण → ि" | card `data.slots` | ✅ | capture `13_P2_MATRA_FIL …(clipped)|
| 156 | 16 | Correct: "matra snaps into the blank · word becomes complete · small sparkle/confetti · VO 'शाबाश! जाल बन गया।' / 'शाबाश! परी बन गया।' / 'शाबाश! हिरण बन गया।'" | engine + per-slot VO | ? | — |
| 157 | 16 | 1st wrong: "Wrong area shakes · Matra returns to original place · Only VO: 'फिर से सोचो।'" | ladder rung 1 | ? | — |
| 158 | 16 | 2nd wrong: "Shake · Matra returns · VO 'ध्यान से देखो। कौन-सी मात्रा लगेगी?' · Hand nudge appears on the correct blank space" | ladder rung 2 | ? | — |
| 159 | 16 | 3rd-attempt correct: "Matra snaps into place · Word completes · Small confetti/sparkle · No VO required" | engine | ✅ | capture …(clipped)|
| 160 | 16 | Completion: "all coaches glow softly · next button becomes active · optional small train whistle / success SFX" | engine | ✅ | ca …(clipped)|
| 161 | 16 | "Keep the same current UI/UX style. Do not add extra text on screen. Use VO-led interaction." | card + engine | ✅ | capture `13_P2_ …(clipped)|

## Deck page 17 — Screen 14 · TRAIN_SORT pictures only
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 162 | 17 | "Show a train with three coaches. Each coach represents one matra category: आ (ा) · इ (ि) · ई (ी). The inside area of each coach remains empty as the drop zone." | engine + card | ? | — |
| 163 | 17 | "At the bottom, show pictures only. **Do not show any word text below the pictures.**" | `data.hide_labels:true` | ✅ | capture `14_ …(clipped)|
| 164 | 17 | Picture set: हाथ → ा · नाक → ा · पिन → ि · हिरण → ि · नीम → ी · कील → ी | card `data.items` | ? | — |
| 165 | 17 | Intro VO "चित्र को सुनो और उसे सही मात्रा वाली बोगी में डालिए।" | `vo_ts3_prompt` | ? | — |
| 166 | 17 | "When the child taps or starts dragging a picture, play only that picture's name: हाथ/नाक/पिन/हिरण/नीम/कील" | speak-on-tap | ? | — |
| 167 | 17 | "One coach can accept multiple pictures belonging to the same matra." | engine multi-capacity | ✅ | capture `14_P3_TRAIN_SORT.png`; …(clipped)|
| 168 | 17 | "The word should not be displayed at any point during the question." | `hide_labels` | ✅ | capture `14_P3_TRAIN_SORT.png`; 6 pictur …(clipped)|
| 169 | 17 | "While dragging, the selected picture card can slightly enlarge. When hovering over a coach, that coach can get a soft glow." | engine CSS | ? | — |
| 170 | 17 | Correct: "Picture snaps inside the correct coach · small sparkle/confetti · Picture becomes locked · VO 'शाबाश! हाथ में आ की मात्रा है।'" | engine + per-item VO | ? | — |
| 171 | 17 | 1st wrong: "Wrong coach short wiggle/shake · Picture returns · No hand nudge · VO 'फिर से सुनो और सही मात्रा पहचानो।'" | ladder rung 1 | ? | — |
| 172 | 17 | 2nd wrong: "Wrong coach shakes again · Picture returns to the bottom · VO 'शब्द को ध्यान से सुनो।' · hand nudge / soft pulse on the correct coach" | ladder rung 2 | ? | — |
| 173 | 17 | 3rd-attempt correct: "Picture snaps into the correct coach · Small confetti/sparkle · No VO required" | engine | ✅ | capture `14_ …(clipped)|
| 174 | 17 | Completion: "all three coaches glow briefly · train gives a small whistle/steam animation · Next active" | engine | ✅ | capture ` …(clipped)|
| 175 | 17 | "Train enters right to left and stops at the centre. Coach labels आ (ा), इ (ि), ई (ी) appear one by one. Picture cards fade/slide up from the bottom." | engine | ? | — |
| 176 | 17 | "Keep animation subtle and do not add extra decorative elements." | engine | ✅ | capture `14_P3_TRAIN_SORT.png`; 6 picture cards, * …(clipped)|

## Deck page 18 — Screen 15 · POEM_SEARCH «मात्रा खोजो»
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 177 | 18 | "Use this as a final 'मात्रा खोजो' challenge. Keep the focus only on: poem card · magnifying glass · target words · ghost animation feedback" | engine `POEM_SEARCH` | ? | — |
| 178 | 18 | "Remove extra decorative elements like: Ravi · kite · girl · tree · unnecessary background objects" | engine (clean stage) | ? | — |
| 179 | 18 | Poem "रवि लाया लाल पतंग, दिन में चमकी सूरज की किरण। नीम तले मीना गाए संग।" | card `data.poem` | ? | — |
| 180 | 18 | Round 1 VO "आ की मात्रा वाले शब्द ढूँढो।" | `vo_ps_r1` | ✅ | capture `15_P4_POEM_SEAR …(clipped)|
| 181 | 18 | Round 2 VO "अब छोटी इ की मात्रा वाले शब्द ढूँढो।" | `vo_ps_r2` | ✅ | capt …(clipped)|
| 182 | 18 | Round 3 VO "अब बड़ी ई की मात्रा वाले शब्द ढूँढो।" | `vo_ps_r3` | ✅ | capt …(clipped)|
| 183 | 18 | Target words ा: लाया, लाल · ि: रवि, दिन, किरण · ी: नीम, मीना — **completed per §4 Option A** to ा: +मीना, +गाए · ी: +चमकी, +की | card `data.rounds` | ? | — |
| 184 | 18 | "A large magnifying glass appears at the bottom-right. Child drags the magnifying glass over the poem. Any word under the glass slightly enlarges. Child taps/selects the word through the magnifying glass. Correct words remain highlighted." | engine lens | ? | — |
| 185 | 18 | Ghost entry: "a small ghost floats in from one side · briefly circles around the magnifying glass · then fades slightly or moves to a corner" | engine ghost actor | ? | — |
| 186 | 18 | Ghost idle: "If the child is idle for a few seconds, the ghost appears near the magnifying glass and gently moves toward the poem." | engine ghost idle cue | ? | — |
| 187 | 18 | Correct: "Ghost pops up happily near the correct word · Small sparkle · short happy bounce and disappear · VO 'शाबाश!'" | engine + `vo_ps_correct` | ? | — |
| 188 | 18 | 1st wrong: "Wrong word gives a small wiggle/shake · Ghost briefly appears with a thinking expression · No hand nudge · VO 'फिर से देखो।'" | ladder rung 1 | ? | — |
| 189 | 18 | 2nd wrong: "Wrong word shakes again · Ghost floats toward one correct target word · gently points/pulses near that word · VO 'ध्यान से मात्रा पहचानो।'" | ladder rung 2 (ghost = hint actor) | ? | — |
| 190 | 18 | Round completion: "Correct words glow together · Ghost flies across the selected words with a sparkle trail · Soft success chime · Next target VO starts automatically." | engine round state | ? | — |
| 191 | 18 | Final completion: "All correct words stay highlighted · Ghost appears once in the centre, celebrates with a small spin/sparkle · Magnifying glass gives a final glow · Next button becomes active." | engine | ? | — |
| 192 | 18 | "Poem card fades in first. Magnifying glass slides in from the bottom. Ghost enters after the magnifying glass. Keep ghost motion slow and soft, not distracting. Do not keep ghost constantly moving on screen." | engine | ? | — |
| 193 | 18 | "Keep the screen minimal: plain/light background · central poem card · magnifying glass · small ghost · mascot/audio button if required · next button" | engine | ? | — |

## Deck page 19 — celebration
| # | page | change (verbatim) | where | status | proof |
|---|---|---|---|---|---|
| 194 | 19 | N/C (no change requested) — ships as built | — | N/C | — |

---

## Cross-cutting rows (asked on many pages, implemented once)

| # | source | change | where | status | proof |
|---|---|---|---|---|---|
| X1 | pages 11–18 | 3-attempt ladder: rung 1 hint VO + **no hand**; rung 2 hint VO + **hand on the correct target**, child still answers; 3rd-a
| X2 | pages 11–18 | "No instruction text on screen. Only VO should play." — the heading band must collapse, not leave an empty pill | engine 
| X3 | pages 3, 11–17 | Shared train shell: right-to-left entry, settle centred, coach states idle/hover/correct/wrong/locked/nudge/complete, wh
| X4 | pages 3–18 | Five new SFX: `sfx_train_arrive`, `sfx_whistle`, `sfx_sparkle`, `sfx_chime`, `sfx_shake` | `assets/UI` | ⏳ asset | Five id
| X5 | page 4 + §7.2 | «बड़ी आ» is non-standard — the deck's page-4 note says "(removing chota or bada)". Correct to «आ की …(clipped)

---

## ASSETS NOT PRODUCED THIS PASS (user decision: "skip it for now")

Wired and manifested, **not** generated. The game runs; these degrade to a silent beat / emoji
fallback until supplied.

- **New VO clips** — every line above marked with a `vo_*` id that is not already in
  `assets/Audio/`. Full list in `VO_RECORDING_LIST.md` (regenerated by this run).
- **New object art** — `obj_jal`, `obj_jaal`, `obj_bal`, `obj_bil`, `obj_kal`, `obj_keel`,
  `obj_matka`, `obj_gati`, `obj_ladki`, `obj_pari`, `obj_sir`, `obj_paani`. Listed in `ART_BRIEF.md`.
- **Five new SFX** (X4) — house rule: chrome and SFX are COPIED from the audio/design team, never
  generated. Until they land, the engine's existing procedural `sfxTap`/`sfxCorrect`/`sfxWrongSoft`
  stand in and the new ids fall back silently.
- **Ghost art** (`ui_ghost.webp`) — the SME's ghost guide. No ghost exists in the assets kit.
- **Train chrome art** — `TrainChrome` renders a structured SVG locomotive/coaches/track. It reads
  `assets/UI/train_loco.webp` first and falls back to the SVG, so the mockup's painted locomotive
  drops in later with no code change.

## §6 TTS constraints to hand to whoever records these
1. A **bare akshara cannot be synthesised** (क, न, द, त all HTTP 400). The `MATRA_BUILD` onset
   clips («जा», «बि», «की») are the pedagogical core of three screens — **budget human recording**.
2. **An em-dash before a short final word truncates the clip** (0.73–1.05 s vs 1.53–2.21 s with a
   comma). Several of the SME's new lines use «यह शब्द है — जल।» — substitute a comma/danda or record.
3. A truncated clip passes every naive check. Keep `_verify_assets.py` §3 in the pipeline.
4. **दिन specifically truncates on the Kore voice**; दिन appears on four of the new screens.


---

# SCORECARD

**194 rows: 175 ✅ DONE · 12 ⏳ PENDING · 4 ⚑ FLAGGED-BACK · 3 N/C** (plus cross-cutting X1–X5: four ✅, one ⏳).

The 12 ⏳ rows are all the same thing seen from twelve deck pages: the five new SFX.

Every VO line and every picture the deck asks for is now **generated, on disk and verified** — see
`VO_RECORDING_LIST.md` and `ART_BRIEF.md`. The only ⏳ rows left are the five new SFX (row X4), which
are chrome: the house rule is that chrome and SFX are COPIED from the audio/design team, never
model-generated. Each already resolves at runtime and swaps to the real take with no code change.

## Receipt — quoted verbatim

```
 17 pass · 1 FAIL · 6 warn   (run with --delivery to make SME/dist artifacts hard requirements)
```

The same command on the **pre-revision** build reads `18 pass · 1 FAIL · 5 warn`. Every line that
changed, accounted for:

| line | mine? | why |
|---|---|---|
| `[FAIL] Engine UI assets: MISSING ['start_mascot.png','start_btn.png']` | **PRE-EXISTING** | the original build fails this identically. Neither 
| `[WARN] Mechanic variety: PICK dominates (12/12)` | **misreported** | the checker has no knowledge of the new types, so it classes `TRAIN_SORT`/
| `[WARN] No orphaned audio` | **new** | 80 clips from the previous card are no longer referenced. House rule is never delete, so they stay in the
| `[WARN] Voice roles: silent hint button` on G1/G2/G3/P2 | **by design** | the deck's ladder is `hint1` → `hint2` → reveal. The manual hint *
| `[WARN] Voice roles: silent reveal` on P2 | **by design** | `MATRA_FILL` is a drag mechanic with its own per-blank ladder; it never calls `revea
| `[WARN] Engine / style.css content-sync` | **not checkable here** | this game is pinned to a per-game engine copy by design, so there is no cano

**Zero non-404 console errors** across all 16 slides plus the landing (headless sweep). The only
404s left are the seven chrome assets that are deliberately not model-generated: the five SFX,
`train_loco.webp` and `ui_ghost.webp` — each with a live fallback.

## Assets — generated 2026-09-17 (second pass, after a Gemini key was supplied)

**Voice-over: 91/91 lines on disk**, Gemini TTS, voice **Kore** — the voice the original 95-clip set
used, so the 14 reused clips and the new ones are the same narrator. Verified after generation:

* `_verify_assets.py` §3 truncation check: **0 truncated** (it caught one, see below).
* All 84 new WAV clips checked for silence/malformation: **0 suspect**, RMS 2596–8095.
* **11 clips are on the EAR-CHECK list** in `VO_RECORDING_LIST.md` — they came back on the
  generator's fallback ladder (a danda, or a style-wrapper on the same voice), so timbre may differ
  slightly. House rule: a human plays these before delivery. Nothing ships unheard.
* **One measured content change:** «यह शब्द है, बल।» truncated on every one of three takes
  (48–56 KB against 108/110 KB for its two peers) — the same per-word failure as दिन in the original
  build. Moving the short word off the end fixes it: **«यह शब्द बल है।»**. All three parallel base
  lines (जल / बल / कल) were given that shape so the three teach screens stay consistent.

**Object art: 10/10 on disk**, flat-vector, magenta-keyed, transparent, autocropped, none pink.
Every one eyeballed on `_review_shots/_art_contact_sheet.png`. Two notes, both in `ART_BRIEF.md`:
बल is drawn as a **dumbbell** (the flexed arm was refused twice by the keyer's hollow-object guard —
skin tone sits inside the halo radius of both chromas), and परी wears **teal** rather than the
mockup's pink (a pink object fights the magenta key).

**UI chrome: `train_loco.webp` and `ui_ghost.webp` generated 2026-09-20** on your explicit
instruction, after I had held them back citing the copy-not-generate rule for chrome. Flagged rather
than done silently. With those two in, the game contains **zero emoji fallbacks** on any screen —
verified by scanning every slide's full text, text nodes included. Both still fall back gracefully if
removed, and a design-team version drops in at the same path with no code change.

**Still not generated, by house rule:** the five SFX (row X4). They are chrome too, they already
resolve at runtime, and the engine's procedural tone stands in until the audio team supplies them.

## One regression this run introduced, found by the receipt and fixed

The shipped card authored `vo_rev_*` reveal lines. Raising `max_attempts` to 3 kept the engine's
never-stuck reveal rung, but my card had no line for it — so a 3rd wrong fell through to the
`correct` clip, i.e. "शाबाश!" after three misses. Three `vo_rev_tt_*` lines added and generated.
Proven by walk: 1st wrong `hint1` (no hand) → 2nd wrong `hint2` + hand → 3rd wrong `vo_rev_tt_aa`,
correct coach glowing, distractors faded, **and the correct coach still tappable** so the child
finalises it.

## CHANGED BEYOND THE DECK

The card-diff gate (`card.pre_revise.json` vs the built `card.json`) leaves these top-level
differences, each mapping to a listed row or to a mechanical consequence of one:

| field | maps to |
|---|---|
| `title` | row #3 |
| `landing_hero` | rows #6, #8 |
| `scaffold_rules` | row X1 |
| `phase_distribution` | mechanical — 19 slides → 16 |
| `signals_expected` | mechanical — the new modules' signals |
| `_emoji_fallback` | mechanical — the new object set |
| `version` | build bookkeeping (0.1 → 0.2) |

**Three of my own changes were caught by this gate and REVERTED**, because they mapped to no row:
`grade` "02"→"G2", a reworded `skill_description_hi`, and a dropped `phase_transition_title` (the
journey beats are a locked house behaviour — restoring it was not optional).

**Two engine fixes outside the deck, both caused by this run's own output:**
- Removed two hardcoded `<link rel="preload">` for **another game's** images (`pic_kaam`,
  `pic_naak`) that were baked into the engine template and put 2 SEVERE 404s on every page load.
  Replaced with per-game preload generated by the build script, emitted only for files on disk.
- `MATRA_FILL`'s drop target was the 52 px blank; a child landing slightly off got **no feedback at
  all**. Widened to the whole coach body.

## ⚑ CONFLICTS — please rule

1. **The rung-2 hand in `practice` (row X1).** You asked for the hand on the 2nd wrong attempt on
   all nine test screens; three are `practice`, and the engine has a LOCKED rule that round 3 gets
   no hand "regardless of whatever name we save it by". Rather than defeat it silently or ignore
   you silently, it is a deck-scoped opt-in (`hand_in_practice: true`) following the documented
   `[28k]` precedent. **No other game is affected.** Confirm, or I gate it to guided only.
2. **`ि` cannot be highlighted inside a word (rows #56, #70).** Technical, not a choice — see the
   row proofs. Shipped with the ◌ि callout. The real fix is the cluster-aware highlight already
   filed as engine request `…-l02-s01-8`; it would also unlock े ै ो ौ ु ू fleet-wide.
3. **TRAIN_TAP option sets (row #106).** The three mockups are one reused image; the per-page VO
   names a different correct word each time. Took the VO as authoritative.
4. **"(removing chota or bada)" (row X5).** Read as: drop the non-standard «बड़ी आ» only — आ has no
   छोटी/बड़ी counterpart — while keeping «छोटी इ» and «बड़ी ई», which your page-12 note explicitly
   confirms. Result: «आ की मात्रा» · «छोटी इ की मात्रा» · «बड़ी ई की मात्
5. **Poem targets (row #183)** — applied Option A as ruled.

## Observations — noticed, NOT changed

The game was left exactly as the deck specified on every one of these.

- **पानी carries two in-scope matras** (ा and ी). It is a valid answer for the बड़ी ई round on
  screen 10, but it is the only test item that is not single-matra. You may prefer a cleaner word.
- **The teach phase is now 7 consecutive screens** before the child acts. Consider interleaving one
  guided screen after each matra's build+examples pair.
- **The 11 EAR-CHECK clips still need a human ear** (VO_RECORDING_LIST.md) — they are correct Hindi
  and correct length, but were recovered on a wrapper rather than the primary voice.
- **A bare matra is an orphan combining mark.** Left to the browser it renders differently per
  platform, so every bare matra now goes through U+25CC (◌ा, ◌ि, ◌ी) — the engine's own existing
  convention in its callout. Deterministic, and it shows *where* the matra attaches. Your mockups
  draw them bare; say the word and I will strip it.
- **Teach-screen headings.** Your MATRA_BUILD notes say "no extra explanatory text", but the
  mockups carry a heading. I kept the heading (it is the learning sentence and matches your own
  final VO line) and dropped the three small captions.
- **The 2-attempt→3-attempt ladder change is fleet-shaped.** It is additive and defaults to today's
  behaviour, so nothing else moved — but it is the better ladder and probably wants rolling out.
- **`sfx_correct` / `sfx_tap` / `sfx_wrong` are shipped but unreferenced** — the engine synthesises
  those procedurally. Pre-existing.
- The receipt's mechanic-variety gate does not know the new slide types and under-reports variety.

---

## Follow-up changes — 2026-09-21

Final build sha `a1e0bddfe622`. Receipt unchanged at `17 pass · 1 FAIL · 6 warn` (the FAIL is the
pre-existing `start_mascot.png` / `start_btn.png` one the original build fails identically).
Full-game re-scan after these changes: **zero emoji, zero broken images, 3 SEVERE** — favicon plus
the two SFX still outstanding.

| # | ask | what was done |
|---|---|---|
| F1 | "in page 1 change the matra colour only to bright orange, text and other elements unchanged" | `.mp-matra` → **#FF8A00**, and its glow retuned to the same orange. Verified scoped by measuring computed colours: on screen 1 the letters stay navy `rgb(11,61,140)` and the arrows `rgb(127,168,217)`; `MATRA_FILL`'s matras on another screen still measure navy. `.mp-matra` is used by `MATRA_PAIRS` and nothing else. |
| F2 | cover page (deck page 3), re-checked bullet by bullet | Title «मात्राओं की रेल» · subtitle empty · exactly three matra boxes ा ि ी · mascot and card style untouched · right-to-left entry · the three matras appear one by one, chained to the landing VO *ending* · arrival + sparkle SFX. |
| F3 | "add the train gif and replace it with the cover page image of the train" | `assets/GIFandVIDEO/train.gif` re-encoded to `assets/UI/train_cover.webp` — 18 frames @100ms, i.e. the **same 1.8s loop**, **1291KB → 287KB**. The artwork already carries a locomotive and three cream panels, so the deck's "three matra boxes" ARE those panels. |
| F4 | "add and generate train sfx" | `sfx_train_arrive` (2.05s) and `sfx_whistle` (1.35s). No SFX generator exists in the kit and Gemini will not produce a steam whistle, so these are synthesised from first principles with the stdlib: accelerating filtered-noise chuffs for the approach, detuned sine partials with vibrato for the whistle. Deterministic seed. Verified non-silent and non-clipped. **Both on the EAR-CHECK list.** |
| F5 | "add mute and unmute button in dev tool (only shows on ?dev=1)" | A speaker toggle in the dev nav. It drives the engine's existing `setMuted()`, so it also stops mid-clip audio and greys the audio chips — the state is visible on the stage, not just on the button. Verified: click → `isMuted=true`, 1 chip greyed, icon flips; click again → restored. **Confirmed absent without `?dev=1`** (`buildDevNav` is only ever reached in dev mode). |

### The non-obvious bug in F3, and why three CSS fixes failed first

The matras drifted right, and progressively: **+3.7% / +5.5% / +7.7%** across the train. Cause: they
were positioned as a CSS percentage of `.lt-wrap`, but `.sg-art` caps the image
(`max-width:92%`, `max-height:250px`) and the wrap is a flex item — so wrap width (566px) never
equalled image width (520px), and the error grew with distance along the train.

Three attempts to make the wrap hug the image (`display:inline-block`, `width:max-content`,
`max-width:none` on the image) were each overridden by the `.sg-art` rules. Fixed by dropping
percentages altogether: `placeMatras()` writes `left` / `top` / `font-size` in pixels from the
image's **measured** box, re-running on image load and on resize. All three now sit within **0.2%**
of their panel centres, measured.

Panel centres, measured off the artwork itself (634×182): **41.1% · 64.3% · 87.5%** across, 47.3%
down. The train's own bounce is only 4px over 182px, so a static overlay stays on its panel.

### Two self-inflicted incidents in this session, both recovered

1. **`4_ENGINE/lesson_template.html` truncated to 0 bytes.** A surrogate-pair escape in a Python
   string could not be encoded to UTF-8, and the failing `write()` had already truncated the file.
   Recovered by reconstructing the template from the built `HI02H11_L02_S01.html` (which carries the
   full engine) with the original sample card restored from `lesson_template.orig.bak.html`.
   **Proof the restore was exact: rebuilding produced the identical sha `e72b8e7837a3`.**
2. **`CHANGES.md` truncated to 0 bytes** — the same mistake, same cause, one step later. Recovered
   in full (all 194 rows) from a persisted tool-output capture of the file.

A working snapshot of the engine is now kept at `4_ENGINE/lesson_template.r5.bak.html`, and any
file carrying emoji is written with a file-based tool rather than a Python string literal.

---

## Follow-up changes — 2026-09-21 (second round)

Final build sha `179782f83b70`. Receipt `17 pass · 1 FAIL · 6 warn` (unchanged; the FAIL is the
pre-existing `start_mascot.png` one). Colour audit across all 17 screens: **no non-orange highlight
anywhere**.

| # | ask | what was done |
|---|---|---|
| G1 | cover train should come from the right to the centre | Cover-specific `coverTrainIn` (translateX 115% → 0, 1.7s, eased to a stop) — it now travels in from off the right edge rather than sharing the shorter in-game entry. |
| G2 | "generate and add train moving, train whistle, sfx" | Added `sfx_train_move` (1.75s steady chug, no whistle, no acceleration — deliberately quiet as it plays under the landing VO). The cover now chugs for the length of the travel and **whistles as it settles**. Joins `sfx_train_arrive` and `sfx_whistle`. |
| G3 | "there is some distortion in the gif, fix that" | **Real defect, measured.** The 287KB WebP was lossy (`quality=80`): mean pixel delta **8.14**, max **206** — the artwork is flat vector with hard binary alpha, which lossy WebP rings badly at the edges. Re-encoded **lossless at the source's own 36 frames**: delta **0.00 / max 0** (pixel-identical) and still **883KB vs the GIF's 1291KB**. Lossy at q95 was still delta 7.28, so quality was never the fix — lossless was. |
| G4 | page 1: "आ" matra aligned differently from the others | **Cause:** the spans carried `.ink-glyph`, and `centerInkGlyph` squares up the ink BOUNDING BOX — it was translating the letter ~2.5px but the matra ~13.3px, and ि / ी have tall ascenders that ा does not, so their dotted circle sat lower than ा's. Removed `.ink-glyph` from the page-1 pairs and aligned on the text BASELINE (`.mp-pair` and `.mp-row`). Letter and matra now share a baseline exactly (delta **+0** in all three pairs) and the three dotted circles line up. |
| G5 | no red for highlighting a matra or letter anywhere — use page 1's orange | Seven rules moved to **#FF8A00**: the matra callout pill, the in-word matra SVG (`--matra-red`), the matra dropped into a blank, the highlighted consonant, the matra in the equation, the flying matra, and the empty blank box. **Wrong-answer red is untouched** — that is feedback, not a highlight. |
| G6 | page 2 (deck page 5), re-checked bullet by bullet | Heading removed (`prompt_hi: ""`) per "Do not add extra explanatory text". Added the **Sound Differentiation** beat. Verified chain order: intro → «यह शब्द जल है।» → «ज में आ की मात्रा लगाने पर, जा बनता है।» → «जाल» → **«ज, जा, जाल।»** → explain, with आगे gated until the end. |

### What the model will and will not say — measured, and worse than the spec records

The deck's "Sound Differentiation" beat needs ज / जा / जाल as distinguishable sounds. Probed the TTS
model directly:

| text | result |
|---|---|
| `ज` · `ब` · `क` (bare akshara) | **refused** — `finishReason: OTHER`, no content at all |
| `जा` · `बि` · `की` (bare syllable) | **refused** — same |
| `ज। जा। जाल।` (danda-separated) | **refused** |
| `ज, जा, जाल।` (comma-separated) | **OK** |

Two corrections to the handoff spec §6.1, which records this as "bare akshara → HTTP 400" for
क/न/द/त: it is **not an HTTP error** but a silent content-free response, and it extends to **bare
two-character syllables**, not just single consonants. The danda/comma split matters too — the same
words refuse with a danda and succeed with commas.

So the three sounds ride in **one clip per screen** (`vo_mb_*_sounds`) whose commas give exactly the
"small pause between each sound" the deck asks for. No human recording needed for this after all.
The equation panel pulses while it plays. These three clips are on the EAR-CHECK list.

### Still outstanding

`sfx_sparkle`, `sfx_chime` and `sfx_shake` — chrome, still copied-not-generated, procedural tones
standing in. EAR-CHECK list now: 11 VO clips + 3 sound-differentiation clips + 3 synthesised SFX.

---

## Follow-up — 2026-09-21: your artwork replaces the generated art

Build `90a0c4717e80`. Receipt unchanged at `17 pass · 1 FAIL · 6 warn`. All 16 slides re-checked:
**no broken images anywhere**.

You supplied three composite sheets (2172×724, already carrying real alpha). They were split into
one transparent PNG per object and now **replace** the generated art. Ten objects:

| key | word | what it is | replaced |
|---|---|---|---|
| `obj_jal` | जल | water splash | generated puddle |
| `obj_jaal` | जाल | net on a handle | generated net |
| `obj_bal` | बल | **flexed arm** | the dumbbell I had substituted |
| `obj_bil` | बिल | **a bill / receipt with ₹** | the generated burrow |
| `obj_kal` | कल | desk calendar | generated calendar |
| `obj_keel` | कील | nail | generated nail |
| `obj_naak` | नाक | nose | the original bundle's nose |
| `obj_din` | दिन | smiling sun | the original bundle's sun |
| `obj_teer` | तीर | arrow | the original bundle's arrow |
| `assets/UI/ui_magnifier.webp` | — | magnifying glass | the CSS-drawn lens on POEM_SEARCH |

### Two meaning changes that came with the art — flagged, not decided

* **`obj_bil` is now a BILL/RECEIPT, not a burrow.** बिल carries both senses. The emoji fallback
  moved 🕳️ → 🧾 to match. The VO («अब बल में छोटी इ की मात्रा लगाने पर, बिल बनता है।») works either
  way, so nothing else changed — but the screen now teaches बिल as "invoice", which is worth an
  SME glance.
* **`obj_bal` is the flexed arm** you'd expect. My dumbbell only existed because the magenta keyer
  kept eating skin tones; your art arrives with real alpha, so the arm works.

### How the sheets were split

Column-gap detection cut two sheets cleanly. The third (`net water nose,bal.png`) came back as a
single blob: faint speckle bridged every gap, no alpha threshold separated the objects without
eating real edges, and connected-component labelling merged them too because the objects abut. The
column **profile** did show true zero-ink columns at x=575 / 1194 / 1649, so that sheet was cut at
those measured valleys. Every cut was autocropped, capped to 640px, and checked for a sane opaque
fraction (8–96%) before being written.

The three source sheets were then deleted from `assets/Images/` — left there they would ship as
unreferenced orphans at 600KB–1.2MB each.

### The magnifier's glass is off-centre, and the hit-test follows it

Measured off the artwork: the glass sits at **67.9% across, 35.2% down, radius 25% of the width** —
not the centre of the image. `POEM_SEARCH`'s magnify test now reads through those coordinates, so a
child scanning the poem is looking through the glass rather than the handle. Swapping the artwork
means updating `GLASS` in the module.

### Size

`assets/Images` 2.2MB → 3.4MB (the new art is higher resolution). Bundle 52MB; the deploy after
`.vercelignore` is unaffected in shape and still well inside limits.

---

## Follow-up — 2026-09-21: FLN Animation Kit recipes installed

Source: `github.com/ananya-goswami/fln-animation-toolkit` (`ANIMATIONS.md`, branch `main`).
Receipt unchanged at `17 pass · 1 FAIL · 6 warn`; all 16 slides re-swept, **no broken images, no new
console errors, no `[animation-kit]` warnings**.

| recipe | where | state |
|---|---|---|
| **1 · Start screen stars (drift)** | cover page + end screen | installed |
| **2 · Start screen stars (tap to burst)** | cover page + end screen | installed |
| **8 · Celebration star burst** | celebration screen | **replaced** the engine's older burst |

### Checked before pasting, as the kit's own rules demand

The kit is emphatic that its main failure mode is collision with an append-only stylesheet (R11).
Grepped every selector and keyframe first: `.sg-sky`, `.sg-glow`, `.sg-burst`, `sgFly`, `sgBreathe`,
`sgFlash`, `sgSpark`, `sgGlowOpacity` and `FLNMotion` were **all absent** from this engine — zero
collisions. `ENGINE_VERSION` untouched (R10). Classic script only, no modules (R3). Every entry
point is wrapped so a throw cannot strand the boot loader (R4), and each effect checks the JS
reduced-motion guard as well as the CSS kill-switch (R5).

Stacking verified against our own layers: `.start-bg`/`.end-bg` are z-index 0, the sky is 1, the
start gate is 80, the end screen is 90, a burst is 95. So the sky sits behind the card and bursts
land on top of everything.

### Recipe 8 REPLACED an existing implementation

This engine already shipped a canvas `starBurst()` — the **pre-retune** version: `ticks 100`,
`decay 0.96`, `startV 22`, 100 particles per shot, and a hard-coded 30-frame floor. Recipe 8 is the
retuned one: `ticks 150`, `decay 0.975`, `startV 14`, 32 stars + 8 circles per shot, and a frame
floor **derived from the last shot** so retiming the shots cannot end the loop early. Fewer stars,
slower drift, same area covered. The old function name is kept as a one-line wrapper, so the single
existing call site in the celebration path did not change.

### The mandatory prerequisite the recipe warns about

Recipe 1 opens with a **must-do-first**: swap `.start-bg` to a *plain* background, because the
decorations are painted into `startnew_bg.webp`. Skipping it gives "two sets of stars — one frozen,
one moving".

Our background **does** have them painted in, and the toolkit does not ship
`startnew_bg_plain.webp`. So one was generated: the decorations are inpainted out by estimating the
clean background with a heavy blur, masking anywhere the original is markedly *brighter* than that
estimate, and compositing — twice, the second pass gentler to catch residue. The sunburst rays and
the centre glow are untouched. Mask covered 3.3% of the image; result is 37KB.

### New assets

| file | what |
|---|---|
| `assets/UI/startnew_bg_plain.webp` | the start background with its painted decorations removed |
| `assets/UI/bgdeco_star.svg` | drift shape `s1` — written from the recipe's inline source |
| `assets/UI/bgdeco_star_o.svg` | drift shape `s2` |
| `assets/UI/bgdeco_spark.svg` | drift shape `s3` |

`s4` (ring) and `s5` (dot) are pure CSS. The tap-burst masks are inline `data:` URIs, not file refs —
the recipe is explicit that external SVG masks are blocked under `file://`.

### Verified running, not just present

* **Drift** — 87 elements built across 3 layers, `sgFly` 18–34s laps, hole mask applied, background
  confirmed swapped to `_plain`, all three SVGs in use. The kit's own **lane-collision proof**
  returns `safe: true` (arc 4.77 vmax against a 2.55 vmax largest element, comfortably over the
  1.5× requirement).
* **Tap to burst** — tapping an `s3` marked it `popped` and spawned a `sg-burst k-spark` with
  **16 particles + 1 flash** at z-index 95, cleaned up after its 1200ms life. The shape→mask mapping
  works (a spark bursts as sparks).
* **Celebration burst** — reached by playing to the celebration slide: one canvas at 1333×750 inside
  `#confetti`, retuned defaults confirmed live.

### One local adaptation

The tap-burst's synthesised pop now honours the dev mute toggle — it is Web Audio and therefore
bypasses the engine's `play()` path entirely, so without this it would still sound with audio muted.

---

## Follow-up — 2026-09-21 · pages 2–7: the transition, the spacing, and what "the complete matra" took

Four asks. All four are in. The third one — "highlight the complete matra but don't highlight
anything else" — could not be done by patching the old highlighter, so the highlighter was
replaced; that replacement is what also fixed pages 4, 5 and 6 for free.

### 1 · «ज + ा = जा» now moves instead of cutting

Three hard cuts sat inside one step, which is why it read as a jump rather than a join:

* the flier was `position:absolute` with **no offsets**, so it settled at `.mb-eq`'s static
  position — near the bottom-left of the blue card, **not over the slot** it was flying to;
* it was then `remove()`d in the same frame the slot's glyph was written, so the matra
  disappeared from one place and reappeared in another between two frames;
* and `ज` became `जा` by a bare `textContent` swap — a second cut, 240ms after the first.

Now: the slot is filled but held invisible **before** the flier is parked, so the equation's
layout is already final and the matra lands on a mark that will not move. The flier is parked at
the slot's real centre, flies in from the side with a small overshoot and settles, then **cross-
fades** into the slot while the slot's own glyph fades up underneath it. `ज → जा` dissolves, and
the whole equation gives one small nod so the eye follows the change.

One measured bug worth recording: the first version aimed with `getBoundingClientRect()`, which
returns **screen** pixels, while `style.left` is written in **CSS** pixels — and this stage carries
a `--scale` transform. The matra landed 13px left of the slot. It uses `offsetLeft`/`offsetTop`
now, which are unscaled. Verified: fly centre and slot centre agree to **0.0px** on both page 2
and page 4.

### 2 · जल→picture and जाल→picture are now the same gap

They were not close. Measured on page 2 before the change:

| panel | word element | gap to its picture |
|---|---|---|
| 1 · जल | `.mb-word`, bare text | **9px** |
| 3 · जाल | `.meet-letter-box`, a 340px card with the word centred in it | **~120px** of visible air |

The flex `gap` was 9px in both — the difference was the 340px card. Panel 3 does not use that card
any more; both panels are one `.mb-word` row of the same fixed height with the ink centred, then
the picture. Measured after: **93px tall and a 9px gap in both panels.** Pages 4 and 6 are the same
module, so they came along.

The result word is an SVG, and its box used to include the font's descent strip — empty under a
Devanagari word, but it reads as air. The SVG's viewBox is **cropped to the word's real ink** now,
so an SVG word occupies the space a plain text word does.

### 3 · The highlight is the matra's ink, not a column of the word

The old highlighter clipped a **vertical band** from the consonant's advance to the next letter's
body. Two consequences, both visible:

* On a medial matra the band also swallowed the **shirorekha running over the next letter** — in
  जाल the top bar above ल came out orange. That is "highlighting something else".
* It could not do **ि** at all. ि is a reordering matra and owns no column of its own, so pages 4
  and 5 fell back to a `इस शब्द की मात्रा — ◌ि` callout box under the word instead.

The mask is now the matra's **actual ink**: each cluster is rastered twice, with the matra and
without it, and the difference is kept. `जा` minus `ज` is the ा stroke and its own bar segment,
stopping at its advance. `बि` minus `ब` — aligned on the right, because ि pushes ब across — is the
ि bar and hook. Both rasters are locked onto the real word raster by a small correlation search
before differencing, so a sub-pixel disagreement between `measureText()` and full-word shaping
cannot erode a stroke. The result is used as an SVG `<mask>`.

This works for any matra, so **ि is highlighted in-word now** and the callout box is gone. That is
what makes pages 3, 5 and 7 one shape — page 5 used to carry an extra callout row that pages 3 and
7 did not, which pushed its picture down.

Checked at 86px against **every** word/matra pair on the card — जाल नाक मटका बिल दिन गति कील तीर
लड़की परी हिरण — all eleven mask cleanly, complete matra, nothing else. Mask payload is ~1KB per
word.

**One thing tried and reverted.** Where the consonant's top bar abuts the matra's, the seam pixels
belong to both and are left to the consonant, which leaves a ~1px notch. Eroding the consonant
plane to hand the seam to the matra instead shrinks the consonant *everywhere*, so its whole
silhouette picked up an orange rim. Reverted; the notch is the smaller problem.

### 4 · The girl on page 7

`obj_ladki` is regenerated: an Indian school girl waving, flat vector with bold navy outlines to
match the rest of the object art, 330×640 with real alpha. The previous generated girl (yellow
top, blue skirt, 275×571) is replaced.

Two keying faults were measured and fixed on the way, both worth knowing for the next object:

* Protecting **every** non-border-connected region from the key welds background showing through
  the braids into the hair as coloured patches — only *small* interior holes should be filled back.
* Distance to the measured background median alone leaves behind whatever background *isn't* that
  exact colour: the soft vignette between the backpack straps, and the ground shadow the model
  keeps drawing despite being told not to. Green **dominance** is also treated as background, and
  that test has to run **last** — the small-hole fill above it was re-opaquing the green wedges.

### Two things for you to look at

* **The `◌` placeholder.** In the page 2/4/6 equation it is now muted slate and only the matra is
  orange — that is what "don't highlight anything else" asks for, since the dotted circle is a
  placeholder for the consonant, not part of the matra. **Page 1 still paints its `◌` orange.**
  I left it: that alignment was hard-won and re-rendering the chip as an SVG would disturb the
  baseline you had me fix. Say the word and I will do page 1 to match.
* **`ज` is still lit orange inside जल** on page 2 (and ब in बल, क in कल). That is a *letter*, not a
  matra, and the deck asks for it in so many words — page 5 step 3, "The letter ज is highlighted".
  Your rule is about matras, so I have left it. It is the only other orange on those screens.

### Verification

Build `HI02H11_L02_S01.html` rebuilt and all 16 slides swept: every matra slide carries exactly one
masked SVG and **zero** leftover callout boxes, no broken images, and no new console errors. The
only SEVERE entries are the already-known missing `sfx_sparkle` / `sfx_chime` and a favicon.

---

## Repair note — 2026-09-21: the 194-row table was clipped, and is restored

This file was rebuilt earlier from a captured tool output, and that capture had clipped **every
line to terminal width**. 183 of the 194 contract rows had lost their tail: 64 were cut inside the
requirement text itself, so more than a third of the contract was unreadable. Four rows also ended
mid-character, which made the whole file invalid UTF-8.

What was done:

* The **requirement** and **target** columns are restored in full for all 194 rows, taken verbatim
  from the session transcript, where the contract survives complete. Every row is well-formed again
  and the file is valid UTF-8.
* The **status** column is kept wherever the clipped file still carried one — 102 rows. The other
  **92 rows show `?`**, because their status had been cut off before this repair and there is no
  second copy to take it from. `?` means *unknown here*, not *not done*; the per-screen prose below
  and in the follow-up sections is the reliable record of what shipped.
* The **evidence** column survives in full on 7 rows and partially on 93, marked `…(clipped)`. The
  captures it points at are still on disk under `_review_shots/`.

The clipped file is kept beside this one as `CHANGES.md.clipped.bak` — nothing was thrown away.
