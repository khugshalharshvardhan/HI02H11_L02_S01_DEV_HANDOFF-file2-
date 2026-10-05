# मात्रा टोकरी — standalone

A hostable copy of just the «मात्रा टोकरी» catch-the-word game, for showing on its own.

## Hosting

Static — no build step. `index.html` is at the root with `assets/` beside it, so the whole
folder can be dropped straight onto Vercel, Netlify, GitHub Pages or any web server.

Serve it over **http(s)**, not by opening the file directly: on a `file://` URL the browser
blocks the audio fetches the game needs.

## What it is

Cut from the current lesson build (`3_CURRENT_BUILD/HI02H11_L02_S01.html`) by replacing its
card with a one-slide card, so it runs the **same engine as the reviewed version** and carries
every fix made to this game since it was ported in — the lesson's own hand nudge, no round
banner, the playfield cleared on both the level cheer and the win, and no Next button.

It is deliberately **not** rebuilt from `_SOURCE/matra_tokri/index.standalone.html`: that is the
pre-port original and predates all of those.

## Differences from the game inside the lesson

| | in the lesson | here |
|---|---|---|
| Cover | the train, titled «मात्राओं की रेल» | title + शुरू करें only, titled «मात्रा टोकरी» |
| After the win | moves on to the lesson's celebration slide | holds on the game's own win screen |

The cover is kept on purpose: its शुरू करें button is the user gesture browsers require before
any audio will play. Without it the game would open silent on a hosted domain.

Reloading the page restarts the game.

## Contents

- `index.html` — the game, engine inlined
- `assets/UI/` — game art (`mt_*`) plus the engine's own chrome
- `assets/Audio/VO/` — the 23 voice clips this card names
- `assets/Audio/SFX/` — sound effects

~13 MB total.

Rebuilt with `make_tokri.py` (kept with the session notes, not in this folder).
