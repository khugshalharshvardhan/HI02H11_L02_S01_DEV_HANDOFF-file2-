# engine_local — HI02H11_L02_S01

Per-game engine copy, the kit's documented route for a change that must not touch the shared
`engine/`. Baseline preserved beside it as `_baseline_08.04b.html` so every edit here is diffable.

| | |
|---|---|
| Base engine | **2026.08.04b-r4-unified** |
| Copied from | `KG and G1 refernce ready HTML's/HI01H11_L03_S01/index.html` (the G1 आ-matra lesson) |
| Why 08.04b | It carries every module this lesson uses, and it is the version the dev team's `verify_bundle` expects — same engine as the sibling `HI02H11_L01_S01` |

### REBASED from 08.14a — why

This copy was first taken from 08.14a to get `DECODE_TAP`, the akshara-join module, as the
curriculum's «मात्रा-जोड़ बिल्डर». **`DECODE_TAP` was then dropped**, because its core interaction is
"tap an akshara, hear its sound" and that audio cannot be produced:

- A **bare akshara is refused** by the TTS model — tested `क`, `न`, `द`, `त`: all `HTTP 400`.
- **Carrier forms are unreliable per-letter** — `अक्षर त।` synthesises, but `अक्षर न।` and
  `अक्षर द।` refuse even after three retries each.

So the module would have shipped silent tiles on some letters and spoken ones on others. With
`DECODE_TAP` gone there is no reason to be on 08.14a, and 08.04b is the better base: it matches the
sibling lesson and the dev team's expected version. Both fixes below were re-applied and
re-verified on 08.04b.

Matra **names** do synthesise and are the fleet's existing convention (`vo_tap_matra_i` =
«छोटी इ की मात्रा» in the G1 sibling), so the matra clips are safe — it is only the consonants that
are not.

## Change 1 — `ी` added to `RIGHT_SPACING_MATRAS`

```diff
- RIGHT_SPACING_MATRAS = new Set(["ा"])
+ RIGHT_SPACING_MATRAS = new Set(["ा", "ी"])
```

**Why.** The set decides whether a matra is coloured **red inside the word** or falls back to a
separate `◌<matra>` callout. It contained only `ा`, so of this lesson's three matras just one got
the in-word highlight the SME asked for. `ी` sits to the right of its consonant exactly like `ा`,
so its absence looked like an omission rather than a limitation.

**Tested, not assumed.** Rendered तीर through the probe: the `ी` is correctly isolated in red, त and
र stay navy. `_matraClipCols` is pixel-based (it rasterises the word and finds ink columns below the
shirorekha), so it generalises without any glyph-specific code.

**`ि` was tried and REVERTED.** With `ि` in the set, दिन mis-clips — the red lands on part of `द`
instead of the `ि` hook, because `ि` is a *reordering* matra: it is typed after its consonant but
drawn before it, so the "columns after the consonant" assumption breaks. A child would be shown the
wrong glyph as "the matra", which is worse than no highlight. `ि` therefore keeps the engine's
callout path, which the original comment was right to route it to.

Net effect for this lesson: **ा and ी highlight in-word, ि uses the callout** — 2 of 3 instead of 1.

## Change 2 — the `◌<matra>` callout no longer collides with आगे

```diff
- .meet-col{...gap:30px;}
+ .meet-col{...gap:14px;padding-bottom:24px;}
- .matra-hint{...font-size:32px;gap:14px;padding:8px 26px;}
+ .matra-hint{...font-size:28px;gap:12px;padding:6px 22px;}
- .matra-hint .matra-hl{font-size:56px;...}
+ .matra-hint .matra-hl{font-size:46px;...}
```

**Why.** On every callout-path slide the pill overlapped the आगे button. Measured on the 2× capture
of दिन: pill bottom row 1155, nav pill top row 1130 — a ~12 stage-px overlap. `.meet-col` is
`justify-content:center` inside a box that runs *behind* the nav button.

**The first attempt was wrong and is recorded so it is not repeated.** `padding-bottom:76px` alone
fixed the nav overlap but pushed the whole centred column up until the picture collided with the
title instead. Because the column is centred, padding moves *both* ends.

**The fix was measured.** Bands from the capture: title bottom 343, picture top 392 (49px headroom),
callout bottom ~1125, nav top 1122. Shrinking the column and reserving 24px raises the bottom and
lowers the top at once. After: **top clearance 25 capture px (12.5 stage), bottom clearance ~43
capture px (21 stage)** — both positive, verified by eye on the capture.

Only the callout path builds `.meet-col`, so the in-word (red matra) layout is untouched —
re-checked on नाक after the change.

## Change 3 — `conceptTileHTML` has a `letter` case again (BACK-PORT)

```diff
+ case "letter":
+   return `<div class="sg-ex sg-ex-letter" role="img"${lbl}><span class="sg-letter-glyph">${c.letter || ""}</span></div>`;
```
plus its two CSS rules (`.sg-ex-letter`, `.sg-ex-letter .sg-letter-glyph`).

**Why.** The landing carries a `concept_strip` of the three matras as `type:"letter"` cells — the
same letter strip the SME asked for on the sibling lesson. This engine copy's `conceptTileHTML`
had **no `letter` case**, so every cell fell through to `default: return ""` and
**the strip rendered completely empty, with no error in the console, no failed request, and no
warning anywhere**. It was only caught by looking at the landing.

**This is not a new feature — it is a back-port.** Taken verbatim (JS and CSS) from
`HIKGH09_L01_S03`'s engine, which carries it as `[S03P2-p]`.

**The finding worth keeping: the version string is not enough.** `HI01H11_L03_S01` (the copy this
`engine_local` was taken from) and `HIKGH09_L01_S03` **both** stamp
`ENGINE_VERSION = "2026.08.04b-r4-unified"`, and they have different `conceptTileHTML` bodies. So
"the engine is 08.04b" does not tell you what the engine can do, and a builder cannot rely on the
version alone. The builder therefore checks for the **feature**, not the version — as it already
did for `RIGHT_SPACING_MATRAS` and the callout spacing. That is now three feature checks, and each
one of them corresponds to something that failed silently at least once.

Worth raising with the dev team as its own point: divergent code under one version string is how
all three of these regressions became possible.

## What the builder enforces

`build_skill_HI02H11_L02_S01.py` refuses to build unless all of the following hold, so a drifted
or re-copied engine fails loudly instead of shipping a silent defect:

| check | what it prevents |
|---|---|
| `ी` ∈ `RIGHT_SPACING_MATRAS` | T4 silently losing the in-word highlight |
| `ि` ∉ `RIGHT_SPACING_MATRAS` | दिन mis-clipping and showing the wrong glyph as the matra |
| `padding-bottom:24px` present | the matra callout colliding with आगे |
| `case "letter":` + `sg-letter-glyph` + `.sg-ex-letter{` | the landing strip rendering empty |
| all 8 required modules present | a slide type mounting as nothing |

## Not changed here

Two asks from the design mapping are still engine-level and deliberately **not** hacked into this
copy, because they would benefit every lesson and belong upstream:

- a matra **fill-in-the-blank** module (`न _ क` + draggable matras) — Screens 5–7
- tapping a matra **inside** a rendered word — Screen 12

Both are noted in `_DESIGN_MAPPING.md` with the substitutions used instead.
