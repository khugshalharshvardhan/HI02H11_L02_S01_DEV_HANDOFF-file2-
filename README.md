# HI02H11_L02_S01 — «मात्राओं की रेल» · developer handoff

**Skill:** आ, इ, ई मात्रा वाले शब्द पढ़ता है। शब्दों में आने वाली मात्रा पहचानता है।
*(Grade 2 Hindi FLN — Hindi_content progression.xlsx, row 55)*

This folder is self-contained. You do **not** need the wider SwiftPAL factory to read it, and you
need the factory only to *build* against it.

---

## Read in this order

1. **`1_SPEC/DEV_HANDOFF_HI02H11_L02_S01.md`** — start here. Section 1 tells you the size of the
   ask in one table; section 8 is the build order. **Sections 4 and 7 are decisions that must be
   made before parts of this can be built** — section 4 blocks one screen outright.
2. **`2_MOCKUPS/`** — the SME's visual design, one PNG per screen, named by deck slide so it lines
   up with the spec and the recommendations.
3. **`1_SPEC/dev_spec_HI02H11_L02_S01.json`** — the same information as data: screen order, every
   VO line, coach/card mappings, proposed card schemas for the new modules, and the full asset
   list. Build from this, not from the prose.
4. **`1_SPEC/_SME_RECOMMENDATIONS.md`** — the SME's 16 screen recommendations **verbatim**,
   unedited. Kept separate from the spec on purpose: their words and the engineering reading of
   those words are different things and should stay distinguishable.

---

## What is in here

| folder | what it is |
|---|---|
| `1_SPEC/` | the specification, the machine-readable form, the verbatim recommendations, and the 8 engine requests already filed in the kit's queue |
| `2_MOCKUPS/` | 17 screen mockups from the SME |
| `3_CURRENT_BUILD/` | **the lesson that already exists and runs** — see below |
| `4_ENGINE/` | the per-game engine copy this lesson is pinned to, its unmodified baseline, and a written record of the 3 changes so every one is diffable |
| `5_CURRENT_BUILD_SCREENSHOTS/` | 20 × 2× captures of the current build, page by page, if you would rather not run it |
| `HI02H11_L02_S01_SME_Review.pptx` | the source deck. The recommendations live in its **speaker notes**; `2_MOCKUPS/` and `_SME_RECOMMENDATIONS.md` are just that deck unpacked for convenience |

## The headline, so nobody is surprised

**This is not a revision of the existing lesson. It is a new game concept.** The existing lesson
uses the standard stage (card, title bar, option cells, sort bins). The recommendations replace
that with a train whose coaches are simultaneously the answer options, the sort bins and the word
frames, plus a magnifying-glass poem hunt.

Of 17 screens: **2 ship today, 7 are reskins that all depend on one new shared train shell, and 8
need new engine work.** Details and sequencing in the spec.

## Running the current build

```bash
cd 3_CURRENT_BUILD
python -m http.server 8731
```

then open <http://localhost:8731/HI02H11_L02_S01.html>.

It must be **served, not opened as a file** — the card is injected into the HTML and the assets are
fetched by relative path, so `file://` will not load audio or images.

Verified from *this copy*, not just the working bundle: all 19 slides mount, 120 resources load,
**zero failed requests**, and all 108 declared assets fetch 200.

One thing not to chase: grepping the HTML turns up `assets/UI/hint.png`, `hint_active.png` and
`peeking_pal.gif`, which are not on disk. They are **dead references in the shared engine** — the
hint button is `display:none !important` by a design ruling and `peeking.webp` superseded the gif.
They are absent from the shipped lesson too and are never requested at runtime (confirmed by
walking all 19 slides). Nothing is missing from this copy: its `assets/UI` is byte-identical to the
working bundle's, 20 files.

State of it: 19 slides (4 teach / 6 guided / 9 practice), engine `2026.08.04b-r4-unified`,
13 illustrations, 95 audio clips, asset receipt 0 FAIL / 0 WARN, and all 108 declared assets
verified returning 200 from the live page. `_BUILD_RECEIPT.md` in that folder records what it
contains and the five defects found and fixed while building it — worth skimming, because three of
them are the kind that pass every naive check (a clip that exists and is the right size but is cut
off half way; art that is present and correct-looking but wrong; a landing element that renders
completely empty with no error anywhere).

## Three things that will cost you time if you do not read them first

All three were measured on this lesson, not inferred. They are in the spec but they are easy to
miss and expensive to rediscover.

1. **`ि` cannot be highlighted inside a word by the current method** (spec §5). The engine colours
   ink columns to the right of the consonant, which is correct for `ा` and `ी` and impossible for
   `ि`, because `ि` is typed after its consonant and drawn before it. Adding `ि` to the set makes
   `दिन` put the red on part of the `द`. Tried, rendered, reverted — the record is in
   `4_ENGINE/CHANGES.md`. The real fix is glyph-cluster highlighting and it is filed as its own
   request; it is the highest-leverage item in the batch because it also unlocks `े ै ो ौ ु ू`.
2. **A bare akshara cannot be synthesised** (spec §6). `क`, `न`, `द`, `त` all return HTTP 400, and
   carrier phrases work for some letters and not others. This hits the new `MATRA_BUILD` module
   directly — its whole point is speaking «जा» / «बि» / «की». Budget human recording for those
   clips rather than discovering it late.
3. **An em-dash before a short final word truncates the clip** (spec §6). Measured head to head:
   em-dash 0.73–1.05 s, comma 1.53–2.21 s. Ten clips shipped half-spoken this way before it was
   found, and a truncated clip passes existence and file-size checks. `3_CURRENT_BUILD/_verify_assets.py`
   catches it by comparing each clip against others of the same text length — keep that check in
   whatever pipeline you build.

## Engine requests

The 8 engine asks are **already filed** in the factory's request queue under session
`sme-lxd-matra-train` (5 blocking). `1_SPEC/ENGINE_REQUESTS.md` is the rollup and
`1_SPEC/engine_requests/` holds the individual records. Each one states what was checked to rule
out a card-only fix, which the queue requires. They are reproduced with their ids in spec §10, so
this folder and the live queue agree.

## What is deliberately not in here

- **Superseded assets.** 118 earlier audio takes and 1 earlier image are quarantined in the working
  bundle (never deleted — house rule) and are not copied here. That is 18 MB of build history with
  no value to you.
- **The factory and the other kits.** ~829 MB of the SME and Dev kits and 38 reference bundles.
  Nothing here needs them.
- **Any change to the existing lesson.** The recommendations are specified, not applied. Under the
  agreed workflow they go in only on an explicit go-ahead from the SME. The two content
  corrections in spec §7 (items 2 and 4) are the ones to apply first, because they are corrections
  rather than redesign.

---

*Prepared 2026-09-16 · questions on the content go to the SME (aamir@convegenius.ai); questions on
the module design and the engine requests are answered in the spec.*
