# HI02H11_L02_S01 — design mapping

**आ, इ, ई मात्रा वाले शब्द पढ़ता है। शब्दों में आने वाली मात्रा पहचानता है।**

Your 14-screen design, mapped onto modules that already exist and are already proven in a
sibling lesson. **This file describes what was BUILT**, not what was planned — an earlier draft
proposed building on engine 2026.08.14a for `DECODE_TAP`; that module had to be dropped and this
records why.

## What the curriculum row adds to your design

Quoted verbatim from row 55 of the fed sheet:

- **Suggested interaction:** «मात्रा-जोड़ बिल्डर: बच्चा आ/इ/ई मात्रा व्यंजन पर खींचता है, बदली ध्वनि
  सुनता है और बना शब्द पढ़ता है।» — your Screens 5–7, and the row wants the child to *hear the
  sound change* as the matra joins.
- **Misconceptions:** «मात्रा अनदेखी कर बिना-मात्रा वाला शब्द पढ़ देता है» → 'नाना' को 'ननन';
  «छोटी इ और बड़ी ई की स्थिति/ध्वनि गड्डमड्ड करता है» → 'दिन' को 'दीन'.

Your instinct to drop **नदी** from the final set was right, and for a second reason too: several
otherwise-obvious matra words carry **two** matras (किताब = ि + ा, चाबी = ा + ी, मिट्टी = ि + ी),
and a two-matra word cannot be a clean item for "which matra does this word have?" — nor can it go
in a sort bin at all. Your safer set (राम / पिन / सीप / बाल) follows exactly that rule, and every
word in the lesson does too.

## The reference lesson that already solves most of this

`HI01H11_L03_S02` — *'ि' और 'ी' मात्रा वाले शब्द पढ़िए* — is the direct G1 sibling: same LO family,
two of our three matras. It carries one pattern worth copying exactly: its word options are **the
same word spelled with the wrong matra**.

```
target चीनी   →   options:  चीनी  ·  चिनि  ·  चनन
```

`चिनि` is the ि/ी swap and `चनन` is the dropped matra — **your two named misconceptions, already
built and signed off**. Every pick slide in this lesson uses that shape rather than unrelated
distractors, so a wrong tap tells us *which* error the child made.

## Engine: the game's own `engine_local/` copy of 2026.08.04b

Not 08.14a. `DECODE_TAP` — the akshara-join module that would have been the literal
«मात्रा-जोड़ बिल्डर» — **was dropped**, because its core interaction is "tap an akshara, hear its
sound" and that audio cannot be produced:

| tested | result |
|---|---|
| bare aksharas `क`, `न`, `द`, `त` | **all HTTP 400** |
| `अक्षर त।` | ✓ synthesises |
| `अक्षर न।`, `अक्षर द।` | **refuse, after 3 retries each** |

So the module would have shipped silent tiles on some letters and spoken ones on others. With it
gone there is no reason to be on 08.14a, and 08.04b is the better base: same engine as the sibling
`HI02H11_L01_S01` and the version the dev team's `verify_bundle` expects.

Matra **names** do synthesise («छोटी इ की मात्रा») and are the fleet's existing convention
(`vo_tap_matra_i` in the G1 sibling), so the matra clips are safe — it is only the bare consonants
that are not.

Two per-game engine fixes live in `engine_local/`; see `engine_local/CHANGES.md`:

1. **`ी` added to `RIGHT_SPACING_MATRAS`** → ी is coloured **red inside the word**, not shunted to
   a separate callout. Takes the in-word highlight from 1 of your 3 matras to 2.
2. **The callout no longer collides with आगे** — measured overlap, measured fix.

`ि` was tried in that set and **reverted**: it is a reordering matra, so दिन mis-clipped and the
red landed on part of `द`. Showing a child the wrong glyph as "the matra" is worse than no
highlight, so `ि` keeps the callout path.

The builder **verifies all four of these facts and refuses to build** if any has drifted.

## Screen-by-screen — what shipped

19 slides, `{tutorial: 4, guided: 6, practice: 9}`.

| Your screen | Slide | Module | Faithful? |
|---|---|---|---|
| 4 — का कि की, then ा ि ी named | T1 | `INTRO` auto, `letters:[ा,ि,ी]` + per-matra `phonemes` | ✅ moved to the front as the opener |
| 1 — «क + ा = का», then नाक with only ा lit | T2 | `MEET_LETTER` auto, `matra:"ा"` | ⚠️ **ा IS red in-word**; the build beat is spoken, not tapped — see below |
| 2 — same for दिन / ि | T3 | `MEET_LETTER` auto, `matra:"ि"` | ⚠️ ि uses the ◌ि callout (reordering matra) |
| 3 — same for तीर / ी | T4 | `MEET_LETTER` auto, `matra:"ी"` | ✅ **ी IS red in-word** (engine fix 1) |
| 5 — सही मात्रा लगाओ (नाक) | G1 | `TAP_LETTER_BY_PICTURE` — नाक · निक · नक | ⚠️ choice, not drag-into-blank — see below |
| 6 — सही मात्रा लगाओ (दिन) | G2 | `TAP_LETTER_BY_PICTURE` — दिन · **दीन** · दन | ⚠️ same · carries the named ि/ी confusion head-on |
| 7 — सही मात्रा लगाओ (तीर) | G3 | `TAP_LETTER_BY_PICTURE` — तीर · तिर · तर | ⚠️ same |
| 8–10 — शब्द सुनो, मात्रा पहचानो | G4 | `SORT_VACHAN`, 2 bins ि \| ी — हिरण, पिन \| सीप, नीम | ✅ and it is a **produce** mechanic, not a pick |
| 8–10 | G5 | `MATCH_DRAG_N` — माला, दिन, तीर | ✅ read the word, place it on its picture |
| 8–10 | G6 | `SORT_VACHAN`, 3 bins, one word per bin | ✅ light introduction to three bins |
| 11 — मात्रा के घर में डालो (3 bins) | P1 | `SORT_VACHAN`, 3 bins, **6 items** | ✅ verified: the module iterates `data.bins`; 4-bin sorts already ship |
| 12 — शब्द पढ़ो, मात्रा पर टैप करो | P2 | `TAP_LETTER_BY_NAME` — हाथ · हिथ · हथ | ⚠️ partial — see below |
| 13 — बिना चित्र के पढ़ो | P2 | same slide: `stimulus: null`, **no picture at all** | ✅ this is the image-free reading your LO needs |
| 13 | P3, P4 | `MATCH_DRAG_N` ×2 — बादल/तिल/सीप, then नाक/हिरण/चीनी | ✅ P4 is one word per matra — the mixed load |
| 14 — राम · पिन · सीप · बाल | P5–P8 | `MASTERY_SILENT_PICK` ×4, first-try scored | ✅ your exact set |
| — | CEL | `CELEBRATION` with a spoken recap of the skill | ✅ |

### Screen 14 is deliberately two different modes

राम and सीप are `sound_to_letter` — **no picture at all**; the child hears the word and picks the
spelling. पिन and बाल are `picture_to_letter`. Mixing the modes means a child cannot settle into
one strategy for the whole check. It also lets **राम** appear without being illustrated: it is a
proper noun, and drawing it raises a question no FLN reading item needs to raise.

## The three substitutions you should rule on

These are the same class of gap — the engine has no module for the literal interaction — and none
of them is faked. I would rather tell you than ship something that looks right in a screenshot.

**1. Screens 1–3, the «क + ा = का» build beat.** Gone with `DECODE_TAP`, for the TTS reason above.
It is now **spoken in full** in T1's instruction line: «न के साथ बड़ी आ की मात्रा लगी, तो बना ना।
द के साथ छोटी इ की मात्रा लगी, तो बना दि। त के साथ बड़ी ई की मात्रा लगी, तो बना ती।» The visual is
the shipped G1 sibling's: name the matras, then one word per matra with that matra highlighted.

**2. Screens 5–7, «न _ क» with a draggable matra.** **There is no module that drops a blank into a
word and lets the child drag a matra into it.** I checked all 59 modules in this engine and every
module across all the reference engines. What shipped is the **choice** half of the ask — same
picture, three spellings, your two named misconceptions as the distractors — which is where the
matra *decision* actually gets tested. The produce half is covered by the sorts and drags in G4–G6.

**3. Screen 12, tapping the matra *inside* the rendered word.** Needs the word split into tappable
parts. `SENTENCE_FIND` does that for words inside a sentence; nothing does it for a matra inside a
word. P2 is one tap away: the word is read without a picture and the child picks the whole correct
spelling.

If you would rather have the literal drag-into-blank, that is a new engine module (`MATRA_FILL`)
and a dev ask — say so and I will write it up instead of keeping the substitution.

## Hint ladder — yours, verbatim

Authored exactly as you wrote it, on every pick slide:

- wrong 1 → «फिर से सुनो — दिन।»
- wrong 2 → «दि-न। 'दि' में कौन-सी मात्रा सुनाई दे रही है?»

The engine reads rung 1 from `hint1` and rung 2 from `hint2` (`wrongClip` → `midHint`), so the two
lines land in the order you wrote them. The sort slides get a third line that teaches *where* to
look, because the ि/ी confusion your row names is as much about position as sound: «मात्रा को देखो।
अक्षर के बाद खड़ी लकीर है, तो बड़ी आ। अक्षर से पहले हुक है, तो छोटी इ। अक्षर के बाद हुक है, तो बड़ी ई।»

## Mechanic diversity

Computed at build time and the build **fails** if it regresses: 14 test slides —
**drag 6 (43%), pick 8 (57%)**, ceiling 60%. Two gesture families, two produce mechanics
(`SORT_VACHAN`, `MATCH_DRAG_N`). The sibling lesson's round-1 receipt flagged this gate, so it is
now checked before the art and voice are spent rather than after.

## One content swap from your brief

**सिर → हिरण.** सिर (head) and बाल (hair) are both head illustrations and would be nearly
indistinguishable as 116px sort tiles. बाल is in your required final set, so सिर is the one that
moved; हिरण is also a single-`ि` word and is unmistakable as a picture. Nothing else in your
wording or word choices changed.
