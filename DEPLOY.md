# Deploying to Vercel

Static deploy of the repo root. **Nothing about the folder layout changes** — `vercel.json` just
makes the existing layout reachable.

Import settings that match this config:

| Vercel field | value |
|---|---|
| Application Preset | **Other** |
| Root Directory | `./` (leave as-is) |
| Build Command | none |
| Output Directory | none |

## What the two rules do

**`/` → `/3_CURRENT_BUILD/HI02H11_L02_S01.html`**
There is no `index.html` at the repo root; the playable file lives inside `3_CURRENT_BUILD/`. Without
this rule the root URL 404s. `/index.html` and `/play` map to the same file.

**`/assets/:path*` → `/3_CURRENT_BUILD/assets/:path*`**
This is the rule that is easy to miss. The built HTML references its assets **relatively**
(`assets/Audio/…`, `assets/Images/…`, `assets/UI/…`). A rewrite keeps the browser URL at `/`, so
those resolve to `/assets/…` — which does not exist at the repo root. Without this second rule the
page would load and **every picture and every audio clip would 404**.

The deep path `/3_CURRENT_BUILD/HI02H11_L02_S01.html` also keeps working; it is a real file.

## Verified before handover

The routing was simulated locally (same precedence Vercel uses: a real file wins, otherwise a
rewrite applies) and the whole lesson was played through it from the root URL:

```
document URL : /
engine       : 2026.08.04b-r4-unified
card         : HI02H11_L02_S01 / 16 slides
cover train  : 634x182 from assets/UI/train_cover.webp
broken images across all 16 slides : NONE
404s : favicon.ico, sfx_sparkle.ogg   <- the one SFX still outstanding
```

`vercel.json` is also validated against Vercel's published schema
(`https://openapi.vercel.sh/vercel.json`), which sets `additionalProperties: false` — that is why a
`_comment` key was rejected on the first import attempt, and why this explanation lives here rather
than inside the config.

## Secrets

`3_CURRENT_BUILD/.env` holds a Gemini API key. It is **git-ignored and was never committed**
(verified with `git log --all` and a key-pattern grep over all tracked files), so a Git-based Vercel
deploy cannot contain it. It is also listed in `.vercelignore`, which covers a `vercel` CLI deploy.

Note that Vercel evaluates rewrites **after** the filesystem, so a deployed file is always served and
no rule in `vercel.json` can hide one. Keeping the file out of the deployment is the only real
protection — which is what the two mechanisms above do.

## Deployment size

`.vercelignore` keeps non-runtime material out: mockups, the SME `.pptx`, build screenshots,
`4_ENGINE/`, review shots and the source GIF. None of it is fetched by the page.

**174 MB → 36.8 MB (230 files).**
