"""Generate the background music loop for मात्रा टोकरी with Lyria.

    py -3 _build_music.py .            writes audio/bgm.mp3
    py -3 _build_music.py . --force    re-cut even if it exists

Key from .env (GKEY=...) or the environment, same as _build_vo.py.
Set MUSIC_MODEL to override the model.

TWO THINGS THIS SCRIPT DOES THAT THE MODEL DOES NOT.

1. SEAMLESS LOOP, twice over. Lyria returns a finished 30s piece with a
   beginning and an end, which clicks every time it wraps. The tail is crossfaded
   into the head: the first LOOP_XF seconds are cut off the front and mixed over
   the last LOOP_XF seconds, so the end of the file already IS the start.
   The output is then OGG VORBIS, not mp3 — mp3 carries encoder delay and padding
   that a browser plays as a GAP at every `loop` wrap, and no amount of
   crossfading inside the audio can fix that. The rest of this folder is .ogg too.

2. LEVEL. The voice-over in this activity is load-bearing — an instruction that
   is not heard is an instruction that did not happen — so the music is
   normalised far below it: -30 LUFS against the VO's -16. index.html ducks it
   further while any clip is playing. Music in a learning game is furniture.
"""
import base64, json, os, subprocess, sys, tempfile, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else HERE
ROOT = os.path.dirname(HERE)

LOOP_XF   = 2.5      # seconds of tail-into-head crossfade
TARGET_I  = -30      # LUFS — deliberately far under the VO
MODEL     = os.environ.get("MUSIC_MODEL", "lyria-3-clip-preview")

PROMPT = (
    "Gentle, warm, cheerful background music for a young children's learning game. "
    "Soft marimba and glockenspiel with a light acoustic guitar, a simple friendly melody "
    "in a major key, relaxed mid tempo, played quietly and evenly. "
    "It must sit far BEHIND a teacher's speaking voice: no drums, no strong beat, no builds, "
    "no drops, no big dynamic changes, nothing attention-grabbing, no sudden accents. "
    "Calm, steady, repetitive and unobtrusive the whole way through, suitable for looping. "
    "Instrumental only, no voices, no singing, no sound effects."
)


def load_key():
    if os.environ.get("GKEY"):
        return os.environ["GKEY"]
    env = os.path.join(ROOT, ".env")
    for line in open(env, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() in ("GKEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"):
            return v.strip().strip('"').strip("'")
    sys.exit("No key. Put GKEY=<key> in .env at the repo root.")


def generate(key, tries=3):
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{MODEL}:generateContent?key={key}")
    body = {"contents": [{"parts": [{"text": PROMPT}]}],
            "generationConfig": {"responseModalities": ["AUDIO"]}}
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=600) as r:
                d = json.load(r)
            for p in d["candidates"][0]["content"]["parts"]:
                inl = p.get("inlineData") or p.get("inline_data")
                if inl:
                    mime = inl.get("mimeType") or inl.get("mime_type") or ""
                    rate = 48000
                    for tok in mime.split(";"):
                        if tok.strip().startswith("rate="):
                            rate = int(tok.split("=")[1])
                    return base64.b64decode(inl["data"]), mime, rate
            raise RuntimeError("no audio part: " + json.dumps(d)[:400])
        except Exception as e:
            last = e
            detail = ""
            if hasattr(e, "read"):
                try: detail = e.read().decode()[:400]
                except Exception: pass
            print(f"   retry {i+1}: {e} {detail}", flush=True)
            time.sleep(5 + i * 8)
    raise last


def main():
    dst   = os.path.join(OUT, "bgm.ogg")
    cache = os.path.join(OUT, "_bgm_raw.bin")   # gitignored; re-encode for free
    if os.path.exists(dst) and "--force" not in sys.argv:
        print(f"=  {dst} exists, skipping (use --force)"); return

    # The generation is the expensive half, the encode is not — so the model's
    # raw bytes are kept and reused. Re-encoding (different loop length, level,
    # codec) costs nothing; --regen asks for genuinely new music.
    if os.path.exists(cache) and "--regen" not in sys.argv:
        raw, mime, rate = open(cache, "rb").read(), "audio/mpeg", 48000
        print(f"   reusing cached generation ({len(raw)} bytes) — --regen for new music")
    else:
        key = load_key()
        print(f"model: {MODEL}")
        print(">  generating ~30s ...", flush=True)
        raw, mime, rate = generate(key)
        open(cache, "wb").write(raw)
        print(f"   {len(raw)} bytes, {mime or 'unknown mime'}")

    tmp = tempfile.mkdtemp()
    src = os.path.join(tmp, "src.wav")
    # Lyria returns a CONTAINER (audio/mpeg here), not the bare PCM the TTS
    # endpoint hands back — feeding an mp3 to -f s16le decodes it as noise, so
    # only take the raw path when the mime actually says so and otherwise let
    # ffmpeg sniff the format.
    low = mime.lower()
    blob = os.path.join(tmp, "src.bin")
    open(blob, "wb").write(raw)
    if "l16" in low or "pcm" in low:
        subprocess.run(["ffmpeg", "-y", "-f", "s16le", "-ar", str(rate), "-ac", "2",
                        "-i", blob, src], check=True, capture_output=True)
    else:
        subprocess.run(["ffmpeg", "-y", "-i", blob, src], check=True, capture_output=True)

    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
        capture_output=True, text=True, check=True).stdout.strip())
    print(f"   source {dur:.1f}s")

    # Tail-into-head crossfade: drop the first LOOP_XF seconds off the front and
    # fade them back in over the tail, so the file's end already is its start.
    xf = min(LOOP_XF, max(0.5, dur / 6))
    fc = (f"[0:a]atrim=0:{xf},asetpts=N/SR/TB[h];"
          f"[0:a]atrim={xf},asetpts=N/SR/TB[b];"
          f"[b][h]acrossfade=d={xf}:c1=tri:c2=tri[x];"
          f"[x]loudnorm=I={TARGET_I}:TP=-2:LRA=7[o]")
    subprocess.run(["ffmpeg", "-y", "-i", src, "-filter_complex", fc, "-map", "[o]",
                    "-ac", "2", "-c:a", "libvorbis", "-q:a", "2", dst],
                   check=True, capture_output=True)

    out_dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst],
        capture_output=True, text=True, check=True).stdout.strip())
    print(f"   -> {os.path.relpath(dst, ROOT)}  {out_dur:.1f}s seamless, "
          f"{os.path.getsize(dst)/1024:.0f} KB, {TARGET_I} LUFS")


if __name__ == "__main__":
    main()
