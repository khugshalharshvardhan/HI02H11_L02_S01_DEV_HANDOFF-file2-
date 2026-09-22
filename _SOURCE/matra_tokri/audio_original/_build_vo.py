"""Re-render every voiceover clip for मात्रा टोकरी with Gemini TTS.

    set GKEY=<your Google AI Studio key>      (never commit the key)
    set VOICE=Leda                            (Kore / Aoede / Zephyr / ... )
    py -3.13 _build_vo.py .                   (all 23 clips)
    py -3.13 _build_vo.py . vo-win s-naav     (just these)

Existing files are skipped, so delete the ones you want re-cut first.
Needs ffmpeg on PATH: the API returns raw PCM and this trims the silence,
loudness-normalises to -16 LUFS and writes 96k mono mp3.

NOTE: s-naav is the one clip gemini-2.5-flash-preview-tts refuses
(finishReason OTHER, no audio, every time). It was cut with
    set TTS_MODEL=gemini-3.1-flash-tts-preview
which handles it. Same voice, and the loudnorm pass makes it sit level with
the rest.
"""
import base64, json, os, subprocess, sys, time, urllib.request, wave, io

KEY = os.environ["GKEY"]
MODEL = os.environ.get("TTS_MODEL", "gemini-2.5-flash-preview-tts")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}"


def synth(text, voice, tries=4):
    body = {
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}
            },
        },
    }
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(
                URL, data=json.dumps(body).encode(),
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.load(r)
            p = d["candidates"][0]["content"]["parts"][0]["inlineData"]
            rate = 24000
            for tok in p.get("mimeType", "").split(";"):
                if tok.strip().startswith("rate="):
                    rate = int(tok.split("=")[1])
            return base64.b64decode(p["data"]), rate
        except Exception as e:
            last = e
            body_txt = ""
            if hasattr(e, "read"):
                try: body_txt = e.read().decode()[:300]
                except Exception: pass
            print(f"   retry {i+1}: {e} {body_txt}", flush=True)
            time.sleep(4 + i * 6)
    raise last


def write_mp3(pcm, rate, out):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes(pcm)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "wav", "-i", "pipe:0",
         # trim leading/trailing silence, normalise, 96k mono mp3
         "-af", "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
                "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse,"
                "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-ar", "44100", "-ac", "1", "-b:a", "96k", out],
        input=buf.getvalue(), check=True)



OUT   = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
VOICE = os.environ.get("VOICE", "Leda")

TEACHER = ("आप एक प्यारी हिंदी शिक्षिका हैं और कक्षा एक के बच्चों से बात कर रही हैं। "
           "गर्मजोशी, साफ़ उच्चारण और धीमी रफ़्तार के साथ केवल यह वाक्य बोलिए: ")
WORD    = ("आप एक हिंदी शिक्षिका हैं और कक्षा एक के बच्चे को शब्द सिखा रही हैं। "
           "बहुत साफ़, धीरे और प्यार से केवल यह एक शब्द बोलिए: ")
CHEER   = ("आप एक हिंदी शिक्षिका हैं। बच्चे ने सही किया है। "
           "खुश होकर, उत्साह से केवल यह बोलिए: ")

CLIPS = []

# --- spoken instructions -------------------------------------------------
CLIPS += [
    ("vo-tutorial",  TEACHER + "टोकरी को उँगली से इधर-उधर ले जाओ।"),
    ("vo-round-aa",  TEACHER + "आ की मात्रा वाले शब्दों को टोकरी में डालो।"),
    ("vo-round-i",   TEACHER + "अब इ की मात्रा वाले शब्दों को टोकरी में डालो।"),
    ("vo-round-ee",  TEACHER + "अब बड़ी ई की मात्रा वाले शब्दों को टोकरी में डालो।"),
]

# --- praise between rounds ----------------------------------------------
CLIPS += [
    ("vo-good-1", CHEER + "बहुत बढ़िया!"),
    ("vo-good-2", CHEER + "शाबाश!"),
    ("vo-good-3", CHEER + "कमाल कर दिया!"),
]

# --- level complete: praise AND the next instruction, in one breath -------
# One clip, not two chained ones. SwiftPalAudio stops whatever is playing when a
# new clip starts, so praise-then-instruction as two files is a seam the child
# hears; and the celebration screen has to stay up for exactly as long as the
# voice, which is one duration to wait on rather than two.
CLIPS += [
    ("vo-level-i",  CHEER + "बहुत बढ़िया! अब इ की मात्रा वाले शब्दों को टोकरी में डालो।"),
    ("vo-level-ee", CHEER + "बहुत बढ़िया! अब बड़ी ई की मात्रा वाले शब्दों को टोकरी में डालो।"),
]

# --- the win line --------------------------------------------------------
CLIPS += [
    ("vo-win", "आप एक हिंदी शिक्षिका हैं। बच्चे ने पूरा खेल जीत लिया है। "
               "बहुत खुश होकर, तालियों वाले उत्साह से केवल यह बोलिए: "
               "शाबाश! तुमने सभी मात्राओं के सही शब्दों को टोकरी में रख लिया है।"),
]

# --- the 15 words --------------------------------------------------------
WORDS = [
    ("s-naav", "नाव"), ("s-haath", "हाथ"), ("s-baal", "बाल"),
    ("s-kaam", "काम"), ("s-daal", "दाल"),
    ("s-din", "दिन"), ("s-til", "तिल"), ("s-sir", "सिर"),
    ("s-dil", "दिल"), ("s-hiran", "हिरन"),
    ("s-nadi", "नदी"), ("s-teer", "तीर"), ("s-chini", "चीनी"),
    ("s-machhli", "मछली"), ("s-neem", "नीम"),
]
CLIPS += [(n, WORD + w) for n, w in WORDS]

only = set(sys.argv[2:])
fail = []
for i, (name, text) in enumerate(CLIPS):
    if only and name not in only:
        continue
    path = os.path.join(OUT, name + ".mp3")
    if os.path.exists(path) and os.path.getsize(path) > 2000:
        print(f"[{i+1}/{len(CLIPS)}] {name} — already there, skipping", flush=True)
        continue
    print(f"[{i+1}/{len(CLIPS)}] {name} ...", flush=True)
    try:
        pcm, rate = synth(text, VOICE)
        write_mp3(pcm, rate, path)
        print(f"        {os.path.getsize(path)} bytes", flush=True)
    except Exception as e:
        print(f"        FAILED: {e}", flush=True)
        fail.append(name)
    time.sleep(1.5)

print("\nDONE. failed:", fail if fail else "none")
