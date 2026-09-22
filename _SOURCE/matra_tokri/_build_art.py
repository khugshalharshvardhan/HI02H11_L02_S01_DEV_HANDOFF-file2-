"""Generate the raster art for मात्रा टोकरी with Gemini image models.

    py -3 _build_art.py --list              which image models this key can see
    py -3 _build_art.py --all               every asset
    py -3 _build_art.py basket cloud_a      just these
    py -3 _build_art.py --all --force       re-cut even if the file exists

Key comes from .env (GKEY=...) or the environment, same as _build_vo.py.
Set IMG_MODEL to override the model.

Raw model output lands in assets/_raw/ untouched. Nothing is written into
assets/UI/ by this script — keying, cropping and resizing are a separate,
reviewable step (_finish_art.py), because the model's framing is never
exactly the frame the game needs.

THE ALPHA RULE. basket/ cloud_* must carry REAL transparency: the basket sits
inside .ol-alpha and the game derives its green/red answer outline from the
art's own alpha (index.html recipe 21, engine A). A painted-in background
means no outline, which kills the correct/wrong feedback. Every asset flagged
alpha=True is checked after download and loudly reported if it came back
opaque, so we find out immediately rather than at integration time.
"""
import base64, json, os, sys, time, urllib.request, io
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW  = os.path.join(HERE, "_raw")
REF  = os.path.join(HERE, "UI", "mascot_swifty.webp")


# ---------------------------------------------------------------- key / model
def load_key():
    if os.environ.get("GKEY"):
        return os.environ["GKEY"]
    env = os.path.join(ROOT, ".env")
    if os.path.exists(env):
        for line in open(env, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() in ("GKEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"):
                return v.strip().strip('"').strip("'")
    sys.exit("No key. Put GKEY=<key> in .env (repo root) or set it in the environment.")


KEY = load_key()
API = "https://generativelanguage.googleapis.com/v1beta"

# Preference order. The first one the key actually has is used. Names drift, so
# --list is the source of truth, not this list.
MODEL_PREFS = [
    "gemini-3-pro-image",
    "gemini-3-pro-image-preview",
    "gemini-3.1-flash-image",
    "gemini-3.1-flash-image-preview",
    "gemini-2.5-flash-image",
    "gemini-3.1-flash-lite-image",
    "gemini-2.0-flash-preview-image-generation",
]


def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def list_models():
    out, tok = [], ""
    while True:
        d = get(f"{API}/models?key={KEY}&pageSize=200" + (f"&pageToken={tok}" if tok else ""))
        out += d.get("models", [])
        tok = d.get("nextPageToken", "")
        if not tok:
            break
    return out


def image_models():
    names = []
    for m in list_models():
        n = m.get("name", "").replace("models/", "")
        methods = m.get("supportedGenerationMethods", [])
        if ("image" in n or "imagen" in n) and ("generateContent" in methods or "predict" in methods):
            names.append(n)
    return names


def pick_model():
    if os.environ.get("IMG_MODEL"):
        return os.environ["IMG_MODEL"]
    have = image_models()
    for p in MODEL_PREFS:
        if p in have:
            return p
    if have:
        return have[0]
    sys.exit("This key exposes no image-capable model. Run --list to see what it has.")


# ---------------------------------------------------------------- style lock
# Derived from assets/UI/mascot_swifty.webp, which is the fleet mascot and is
# NOT being regenerated — every new asset has to sit beside it without looking
# imported from a different game. The reference image is also sent with every
# request; this paragraph is the part the model reads.
STYLE = (
    "Children's mobile-game cartoon illustration, matching the reference image's style exactly. "
    "Bold clean outlines in a soft desaturated NAVY BLUE (#2E5A8F) — never black. "
    "Flat saturated fills with gentle soft cel shading and a subtle darker tone at the edges. "
    "Rounded, chunky, friendly sticker-like forms. Cheerful and warm, Grade-1 age appropriate. "
    "Vector-clean, no photographic texture, no visible brush strokes, no grain, no noise. "
    "No text, no letters, no numbers, no watermark, no signature, no border, no frame."
)

ALPHA = (
    "CRITICAL: output the subject on a FULLY TRANSPARENT background with a real alpha channel. "
    "Absolutely no background, no backdrop, no scenery, no ground, no floor, no shadow cast "
    "onto any surface, no white fill, no checkerboard pattern. Only the subject's own pixels are "
    "opaque; every other pixel must be fully transparent. Crisp clean edges."
)

# name -> (prompt, aspect, needs_alpha)
ASSETS = {
    # --- the big one ---------------------------------------------------------
    "basket": (
        "A single woven wicker basket for collecting things, viewed straight from the FRONT at "
        "eye level, sitting upright and perfectly symmetrical, centred in frame. "
        "Warm golden-brown woven cane with a visible over-under weave pattern, a thick sturdy "
        "rolled rim at the top, and a wide OPEN mouth so the dark inside of the basket is clearly "
        "visible as an ellipse at the top. Empty — nothing inside it. No handle over the top. "
        "The rim is the widest part and sits in the upper third of the frame; the body tapers "
        "gently toward a rounded base. "
        "The basket fills the frame with a small even margin on all sides.",
        "1:1", True,
    ),

    # A deeper-mouthed basket, for the two-layer sandwich. The whole point is the
    # WINDOW: the taller and more open the bowl's dark interior, the longer a
    # caught word stays visible inside it before the near rim covers it. The
    # first basket's mouth was only 25% of the art's height, which is ~39px on
    # screen. This asks for a wide-open one, seen from slightly above.
    "basket_deep": (
        "A single woven wicker basket for collecting things, seen from the FRONT but from "
        "SLIGHTLY ABOVE, so the wide circular opening reads as a big open ellipse and you can "
        "see DEEP DOWN INSIDE the basket. Upright, perfectly symmetrical, centred in frame. "
        "The dark hollow interior is the most prominent feature: a large, tall, clearly visible "
        "opening taking up roughly the top HALF of the basket, shading from mid-brown at the far "
        "wall down to very dark brown at the bottom, so the basket reads as deep rather than "
        "shallow. A thick sturdy rolled rim runs all the way round the opening, clearly separating "
        "the inside from the outside. Below the rim, warm golden-brown woven cane with a visible "
        "over-under weave. Empty — nothing inside it. No handle over the top. "
        "The basket fills the frame with a small even margin on all sides.",
        "1:1", True,
    ),

    # --- sky decor -----------------------------------------------------------
    "cloud_a": (
        "One single fluffy cartoon cloud, seen from the side, wide and puffy with soft rounded "
        "lobes. Pure white with a very light blue-grey soft shading underneath. Centred, "
        "filling the frame edge to edge.",
        "16:9", True,
    ),
    "cloud_b": (
        "One single fluffy cartoon cloud, seen from the side — a SMALLER, rounder, more compact "
        "shape than a wide cloud, with three or four soft lobes. Pure white with very light "
        "blue-grey soft shading underneath. Centred, filling the frame.",
        "16:9", True,
    ),
    "cloud_c": (
        "One single fluffy cartoon cloud, seen from the side — a LONG low stretched shape with "
        "a flat bottom and several small bumps along the top. Pure white with very light "
        "blue-grey soft shading underneath. Centred, filling the frame.",
        "16:9", True,
    ),

    # --- background plate ----------------------------------------------------
    # 1333x750 is exactly 16:9, so the plate needs no aspect surgery — only a
    # horizon nudge, which _finish_art.py does after measuring it.
    "bg_plate": (
        "A wide, simple, cheerful outdoor meadow background for a children's game — EMPTY scenery "
        "only, with nothing in the foreground. "
        "The top 62 percent is a clear even sky graduating from pale cyan at the horizon to a "
        "soft sky blue at the top. The sky brightness is COMPLETELY EVEN from left to right — "
        "no sun, no sun glow, no sunbeams, no warm yellow anywhere, no bright corner, no vignette, "
        "no light source of any kind. "
        "The bottom 38 percent is a smooth bright green grassy meadow with a gentle suggestion of "
        "grass texture, slightly lighter green right at the horizon line. "
        "The horizon is a clean, perfectly HORIZONTAL, straight line across the full width, "
        "positioned at exactly 62 percent of the image height from the top. "
        "No clouds, no trees, no plants, no flowers, no hills, no mountains, no path, no fence, "
        "no buildings, no animals, no people, no objects of any kind. "
        "Very simple and uncluttered — this is a backdrop that game pieces sit on top of.",
        "16:9", False,
    ),

    # --- nudge hand (recipes 3 + 4) -----------------------------------------
    # The kit centres the tap ripple on the fingertip, so the finger must point
    # straight UP and sit near the top-centre of the frame — see the .nh-tapfx
    # geometry note in index.html, which _finish_art.py re-derives by measuring.
    "nudge_hand": (
        "A friendly cartoon hand wearing a WHITE glove, pointing straight UP with the index "
        "finger fully extended and the other fingers curled into a soft fist — the classic "
        "'tap here' pointing hand. Viewed from the front, upright, not tilted. "
        "White glove with soft blue-grey shading in the creases, a rounded cuff at the wrist, "
        "exactly like the mascot's gloves in the reference image. "
        "The extended fingertip is at the TOP CENTRE of the frame with only a small margin "
        "above it, and the wrist is at the bottom. No arm, no sleeve beyond the cuff. "
        "Chunky, rounded and friendly.",
        "3:4", True,
    ),
}


# ---------------------------------------------------------------- generation
def ref_part():
    """The mascot, as a style anchor on every request."""
    if not os.path.exists(REF):
        return None
    data = base64.b64encode(open(REF, "rb").read()).decode()
    return {"inline_data": {"mime_type": "image/webp", "data": data}}


def generate(model, prompt, aspect, tries=3):
    parts = [{"text": prompt}]
    r = ref_part()
    if r:
        parts.append(r)
        parts.insert(0, {"text": "Use the attached image as the STYLE REFERENCE only — match its "
                                 "line weight, outline colour, shading and palette. Do NOT copy or "
                                 "include the character itself."})

    body = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": aspect},
        },
    }

    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(
                f"{API}/models/{model}:generateContent?key={KEY}",
                data=json.dumps(body).encode(),
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=240) as resp:
                d = json.load(resp)
            for p in d["candidates"][0]["content"]["parts"]:
                if "inlineData" in p:
                    return base64.b64decode(p["inlineData"]["data"])
                if "inline_data" in p:
                    return base64.b64decode(p["inline_data"]["data"])
            raise RuntimeError("no image part in response: " + json.dumps(d)[:400])
        except Exception as e:
            last = e
            detail = ""
            if hasattr(e, "read"):
                try:
                    detail = e.read().decode()[:400]
                except Exception:
                    pass
            # Older models reject IMAGE-only and/or imageConfig. Peel them off.
            if "responseModalities" in detail or "IMAGE" in detail:
                body["generationConfig"]["responseModalities"] = ["TEXT", "IMAGE"]
            if "imageConfig" in detail or "aspectRatio" in detail:
                body["generationConfig"].pop("imageConfig", None)
            print(f"   retry {i+1}: {e} {detail}", flush=True)
            time.sleep(4 + i * 6)
    raise last


def report(path, want_alpha):
    """Say plainly what came back — size, mode, and whether alpha is real."""
    im = Image.open(path)
    w, h = im.size
    note = f"   {w}x{h} {im.mode}"
    if want_alpha:
        if im.mode != "RGBA":
            print(note + "  ** NO ALPHA CHANNEL — needs keying **")
            return False
        a = im.getchannel("A")
        lo, hi = a.getextrema()
        clear = sum(1 for p in a.getdata() if p < 8)
        pct = 100.0 * clear / (w * h)
        if lo > 8:
            print(note + f"  ** alpha present but nothing transparent (min={lo}) — needs keying **")
            return False
        print(note + f"  alpha OK — {pct:.0f}% of pixels fully transparent")
        return True
    print(note)
    return True


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}

    if "--list" in flags:
        names = image_models()
        print("image-capable models on this key:")
        for n in names:
            print("  ", n)
        if not names:
            print("   (none)")
        return

    os.makedirs(RAW, exist_ok=True)
    model = pick_model()
    print(f"model: {model}\n")

    todo = list(ASSETS) if "--all" in flags else args
    if not todo:
        sys.exit("Nothing to do. Pass asset names, or --all. Known: " + ", ".join(ASSETS))

    bad = []
    for name in todo:
        if name not in ASSETS:
            print(f"!  unknown asset {name!r}"); continue
        prompt, aspect, want_alpha = ASSETS[name]
        out = os.path.join(RAW, name + ".png")
        if os.path.exists(out) and "--force" not in flags:
            print(f"=  {name} exists, skipping"); continue

        print(f">  {name} ({aspect})", flush=True)
        full = prompt + "\n\n" + STYLE + ("\n\n" + ALPHA if want_alpha else "")
        try:
            png = generate(model, full, aspect)
        except Exception as e:
            print(f"!  {name} FAILED: {e}\n"); bad.append(name); continue
        open(out, "wb").write(png)
        if not report(out, want_alpha):
            bad.append(name)
        print()

    print("raw output in", RAW)
    if bad:
        print("needs attention:", ", ".join(bad))


if __name__ == "__main__":
    main()
