"""Build HI02H11_L02_S01 — «मात्राओं की रेल» (matra train).

Master-map row (Hindi_content progression.xlsx, row 55):
  HI · 02 · H11 · HI02H11_L02_S01 · grade G2 · lo_code HI02H11_L02
  Skill/LO: "आ, इ, ई मात्रा वाले शब्द पढ़ता है। शब्दों में आने वाली मात्रा पहचानता है।"

REVISION 2026-09-17 — SME feedback deck `HI02H11_L02_S01_SME_Review.pptx` applied. The ask is not a
tweak: it replaces the standard stage (card, option cells, sort bins) with a TRAIN whose coaches are
simultaneously the answer options, the sort bins and the word frames, plus a magnifying-glass poem
hunt. 194 discrete asks, mapped row-by-row in CHANGES.md next to this file.

ENGINE: this game is pinned to the PER-GAME engine copy at ../4_ENGINE/lesson_template.html — the
kit's documented route for a change that must not touch the shared engine/. That copy carries three
pre-existing documented changes (../4_ENGINE/CHANGES.md) plus this revision's r5 additions. It is
DELIBERATELY not the shared factory engine, so unified_build.require_current_engine() cannot be used
here: its content-sync guard compares against the shared maths app.js and would reject a per-game
copy by design. The guard below checks for the FEATURES instead — which is stronger, because
HI01H11_L03_S01 and HIKGH09_L01_S03 both stamp "2026.08.04b-r4-unified" and have different code.
Every check corresponds to something that has already failed silently at least once.
"""
import json
import os
import re
import sys

HERE   = os.path.dirname(os.path.abspath(__file__))          # .../3_CURRENT_BUILD
ROOT   = os.path.dirname(HERE)
ENGINE = os.path.join(ROOT, "4_ENGINE", "lesson_template.html")
CODE   = "HI02H11_L02_S01"
OUT    = HERE

_CARD_TAG = re.compile(r'(<script type="application/json" id="cardData">)(.*?)(</script>)', re.S)

# ---------------------------------------------------------------------------------------------
# ENGINE FEATURE GUARD — refuse to build on a drifted or re-copied engine.
# ---------------------------------------------------------------------------------------------
REQUIRED_FEATURES = [
    # --- the three pre-existing engine_local changes (4_ENGINE/CHANGES.md) ---
    ('RIGHT_SPACING_MATRAS = new Set(["ा", "ी"])',
     "ी missing from RIGHT_SPACING_MATRAS — the ई in-word highlight would silently vanish"),
    ('padding-bottom:24px',
     "the matra callout spacing fix is gone — the ◌ि pill collides with आगे"),
    ('case "letter":',
     'conceptTileHTML has no "letter" case — a landing letter strip renders EMPTY with no error'),
    ('sg-letter-glyph',
     "the landing letter-strip CSS/JS back-port is incomplete"),
    # --- r5: this revision's additions ---
    ("const TrainChrome",
     "TRAIN_CHROME missing — 7 screens have no shell"),
    ("SlideModules.MATRA_PAIRS",   "MATRA_PAIRS module missing (deck page 4)"),
    ("SlideModules.MATRA_BUILD",   "MATRA_BUILD module missing (deck pages 5, 7, 9)"),
    ("SlideModules.MEET_EXAMPLES", "MEET_EXAMPLES sequencer missing (deck pages 6, 8, 10)"),
    ("SlideModules.TRAIN_TAP",     "TRAIN_TAP module missing (deck pages 11, 12, 13)"),
    ("SlideModules.TRAIN_SORT",    "TRAIN_SORT module missing (deck pages 14, 15, 17)"),
    ("SlideModules.MATRA_FILL",    "MATRA_FILL module missing (deck page 16)"),
    ("SlideModules.POEM_SEARCH",   "POEM_SEARCH module missing (deck page 18)"),
    ('_scafRule("hand_on_attempt", 99)',
     "the 3-attempt ladder's rung-2 hand is missing (deck row X1)"),
    ('_scafRule("silent_on_late_correct", false)',
     "silent-on-late-correct is missing — a 3rd-attempt success would still be praised (row X1)"),
    ('classList.toggle("no-prompt"',
     "the empty-prompt band collapse is missing — the train screens would show an empty blue pill"),
    # --- the cover-page entrance (deck page 3 / rows #6, #8, #9, #14) ---
    ("train_spritesheet.webp",
     "the cover is off the SME spritesheet — back on the train.gif re-encode, which carries the "
     "black-matte fringe and the palette dither the sheet does not have"),
    ("spin:71, rest:35",
     "the spin/rest pair has drifted — SPIN must be congruent to REST mod 36 or the train's "
     "last frame jumps as it stops"),
    ("window.__landingTrainEnter",
     "the train entrance is not deferred — it would run BEHIND the 1600ms brand loader and be "
     "over before the child sees the landing"),
    ('class="lt-smoke"',
     "no chimney smoke on the cover train"),
    # --- the VO / SFX folder split ---
    ('const VO_DIR  = "assets/Audio/VO/"',
     "the engine is back on a flat assets/Audio folder — every VO path would 404"),
    ('const SFX_DIR = "assets/Audio/SFX/"',
     "the engine is back on a flat assets/Audio folder — every SFX path would 404"),
    ("const _inkCentre",
     "the matras are back to BOX-centring — ि and ी paint a hook the others do not, so they "
     "sit ~6.5px high in their panels unless the INK is what gets centred"),
    ("const spinSprite",
     "the spritesheet frame driver is gone — the travelling train would be a single frame"),
    ("travelEase(p) * SPR.spin",
     "the chug is no longer coupled to the travel easing — the wheels would run at a constant "
     "rate and stop dead the instant the loco halts, which is what read as abrupt"),
    ("_inkCentre(sp)",
     "placeTrainParts is no longer using the ink centre to place the matras"),
]

# ि must NOT be in the right-spacing set: it is a reordering matra and the pixel-column method
# paints part of the द instead of the hook. Tried, rendered, reverted — see 4_ENGINE/CHANGES.md.
FORBIDDEN_FEATURES = [
    ('RIGHT_SPACING_MATRAS = new Set(["ा", "ि"',
     "ि is back in RIGHT_SPACING_MATRAS — दिन will mis-clip and show the wrong glyph as the matra"),
]


def require_engine():
    if not os.path.exists(ENGINE):
        raise SystemExit(f"  X  ENGINE GUARD: per-game engine missing: {ENGINE}")
    mono = open(ENGINE, encoding="utf-8").read()
    ev = re.search(r'ENGINE_VERSION\s*=\s*["\']([^"\']+)["\']', mono)
    if not ev:
        raise SystemExit("  X  ENGINE GUARD: engine is UNSTAMPED")
    missing = [why for needle, why in REQUIRED_FEATURES if needle not in mono]
    present = [why for needle, why in FORBIDDEN_FEATURES if needle in mono]
    if missing or present:
        for why in missing:
            print(f"  X  MISSING FEATURE: {why}", file=sys.stderr)
        for why in present:
            print(f"  X  FORBIDDEN:       {why}", file=sys.stderr)
        raise SystemExit("  X  ENGINE GUARD failed — nothing was written.")
    print(f"  OK  engine guard: {ev.group(1)} + all {len(REQUIRED_FEATURES)} required features present")
    return mono


# =============================================================================================
# VOICE-OVER — every line is the SME's own wording from the deck.
# Two systematic substitutions, both deck-instructed, both flagged in CHANGES.md:
#   * «बड़ी आ» -> «आ»  (deck page 4: "removing chota or bada"; आ has no छोटी/बड़ी counterpart)
#   * em-dash -> comma (§6.2: an em-dash before a short final word truncates the clip to
#     0.73-1.05s vs 1.53-2.21s with a comma; ten clips shipped half-spoken this way)
# =============================================================================================
VO = {
    # ---- «मात्रा टोकरी» (G7) — carried over from the standalone build, ids renamed to
    # this lesson's convention. The clips themselves are the SME's takes, transcoded
    # from mp3 to the .ogg every other clip here uses so they ride the normal VO path.
    "vo_mt_intro": "टोकरी को उँगली से इधर-उधर ले जाओ।",
    "vo_mt_round_aa": "आ की मात्रा वाले शब्दों को टोकरी में डालो।",
    "vo_mt_round_i": "अब इ की मात्रा वाले शब्दों को टोकरी में डालो।",
    "vo_mt_round_ee": "अब बड़ी ई की मात्रा वाले शब्दों को टोकरी में डालो।",
    "vo_mt_cheer_i": "बहुत बढ़िया! अब इ की मात्रा वाले शब्दों को टोकरी में डालो।",
    "vo_mt_cheer_ee": "बहुत बढ़िया! अब बड़ी ई की मात्रा वाले शब्दों को टोकरी में डालो।",
    "vo_mt_done": "शाबाश! तुमने सभी मात्राओं के सही शब्दों को टोकरी में रख लिया है।",
    "vo_mt_w_naav": "नाव",
    "vo_mt_w_haath": "हाथ",
    "vo_mt_w_baal": "बाल",
    "vo_mt_w_kaam": "काम",
    "vo_mt_w_daal": "दाल",
    "vo_mt_w_din": "दिन",
    "vo_mt_w_til": "तिल",
    "vo_mt_w_sir": "सिर",
    "vo_mt_w_dil": "दिल",
    "vo_mt_w_hiran": "हिरन",
    "vo_mt_w_nadi": "नदी",
    "vo_mt_w_teer": "तीर",
    "vo_mt_w_chini": "चीनी",
    "vo_mt_w_machhli": "मछली",
    "vo_mt_w_neem": "नीम",
    # ---- landing (deck page 3) -------------------------------------------------------------
    "vo_landing": "हेलो दोस्त! मैं हूँ स्विफ्टी। आज हम मात्राओं के बारे में जानेंगे।",

    # ---- Screen 1 · the three matras (deck page 4) ------------------------------------------
    "vo_s1_prompt":  "आज हम आ की मात्रा, छोटी इ की मात्रा और बड़ी ई की मात्रा वाले शब्द पढ़ेंगे।",
    "vo_matra_aa2":  "आ की मात्रा",
    "vo_matra_i":    "छोटी इ की मात्रा",
    "vo_matra_ee":   "बड़ी ई की मात्रा",

    # ---- Screen 2 · MATRA_BUILD जल -> जा -> जाल (deck page 5) --------------------------------
    "vo_mb_jal_intro":   "आइए, देखें कि आ की मात्रा लगने से शब्द की आवाज़ कैसे बदलती है।",
    "vo_mb_jal_base":    "यह शब्द जल है।",
    "vo_mb_jal_onset":   "ज में आ की मात्रा लगाने पर, जा बनता है।",
    "vo_name_jaal":      "जाल",
    "vo_mb_jal_explain": "अब जल में आ की मात्रा लगाने पर, जाल बनता है।",
    "vo_mb_jal_sounds":  "ज, जा, जाल।",

    # ---- Screen 3 · examples नाक / मटका (deck page 6) ----------------------------------------
    "vo_ex_aa_intro": "आइए, आ की मात्रा वाले कुछ शब्द देखें।",
    "vo_ex_naak":     "नाक, बोलकर देखिए। इसमें न पर आ की मात्रा लगी है।",
    "vo_ex_matka":    "मटका, बोलकर देखिए। इसमें क पर आ की मात्रा लगी है।",

    # ---- Screen 4 · MATRA_BUILD बल -> बि -> बिल (deck page 7) --------------------------------
    "vo_mb_bil_intro":   "आइए, देखें कि छोटी इ की मात्रा लगाने से शब्द की आवाज़ कैसे बदलती है।",
    "vo_mb_bil_base":    "यह शब्द बल है।",
    "vo_mb_bil_onset":   "ब में छोटी इ की मात्रा लगाने पर, बि बनता है।",
    "vo_name_bil":       "बिल",
    "vo_mb_bil_explain": "अब बल में छोटी इ की मात्रा लगाने पर, बिल बनता है।",
    "vo_mb_bil_sounds":  "ब, बि, बिल।",

    # ---- Screen 5 · examples दिन / गति (deck page 8) -----------------------------------------
    "vo_ex_i_intro": "आइए, छोटी इ की मात्रा वाले कुछ शब्द देखें।",
    "vo_ex_din":     "दिन, बोलकर देखिए। इसमें द पर छोटी इ की मात्रा लगी है।",
    "vo_ex_gati":    "गति, बोलकर देखिए। इसमें त पर छोटी इ की मात्रा लगी है।",

    # ---- Screen 6 · MATRA_BUILD कल -> की -> कील (deck page 9) --------------------------------
    "vo_mb_keel_intro":   "आइए, देखें कि बड़ी ई की मात्रा लगाने से शब्द की आवाज़ कैसे बदलती है।",
    "vo_mb_keel_base":    "यह शब्द कल है।",
    "vo_mb_keel_onset":   "क में बड़ी ई की मात्रा लगाने पर, की बनता है।",
    "vo_name_keel":       "कील",
    "vo_mb_keel_explain": "अब कल में बड़ी ई की मात्रा लगाने पर, कील बनता है।",
    "vo_mb_keel_sounds":  "क, की, कील।",

    # ---- Screen 7 · examples तीर / लड़की (deck page 10) ---------------------------------------
    "vo_ex_ee_intro": "आइए, बड़ी ई की मात्रा वाले कुछ शब्द देखें।",
    "vo_ex_teer":     "तीर, बोलकर देखिए। इसमें त पर बड़ी ई की मात्रा लगी है।",
    "vo_ex_ladki":    "लड़की, बोलकर देखिए। इसमें क पर बड़ी ई की मात्रा लगी है।",

    # ---- Screen 8 · TRAIN_TAP आ (deck page 11) -----------------------------------------------
    "vo_tt_aa_prompt":  "जिस डिब्बे में आ की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए।",
    "vo_tt_aa_correct": "शाबाश! हाथ शब्द में आ की मात्रा है।",
    "vo_tt_aa_hint1":   "फिर से सोचो। आ की मात्रा वाला शब्द कौन-सा है?",
    "vo_tt_aa_hint2":   "ध्यान से देखो और सही डिब्बे पर टैप कीजिए।",
    "vo_rev_tt_aa":     "सही डिब्बा यह है। हाथ शब्द में आ की मात्रा है।",

    # ---- Screen 9 · TRAIN_TAP छोटी इ (deck page 12) ------------------------------------------
    "vo_tt_i_prompt":  "जिस डिब्बे में छोटी इ की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए।",
    "vo_tt_i_correct": "शाबाश! पिन शब्द में छोटी इ की मात्रा है।",
    "vo_tt_i_hint1":   "फिर से सोचो। छोटी इ की मात्रा वाला शब्द कौन-सा है?",
    "vo_tt_i_hint2":   "ध्यान से देखो और सही डिब्बे पर टैप करो।",
    "vo_rev_tt_i":     "सही डिब्बा यह है। पिन शब्द में छोटी इ की मात्रा है।",

    # ---- Screen 10 · TRAIN_TAP बड़ी ई (deck page 13) -----------------------------------------
    "vo_tt_ee_prompt":  "जिस डिब्बे में बड़ी ई की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए।",
    "vo_tt_ee_correct": "शाबाश! पानी शब्द में बड़ी ई की मात्रा है।",
    "vo_tt_ee_hint1":   "फिर से सोचो। बड़ी ई की मात्रा वाला शब्द कौन-सा है?",
    "vo_tt_ee_hint2":   "ध्यान से देखो और सही डिब्बे पर टैप करो।",
    "vo_rev_tt_ee":     "सही डिब्बा यह है। पानी शब्द में बड़ी ई की मात्रा है।",
    "vo_name_paani":    "पानी",

    # ---- Screen 11 · TRAIN_SORT word -> matra coach (deck page 14) ---------------------------
    "vo_ts1_prompt":   "हर शब्द को उसकी सही मात्रा वाली बोगी में डालिए।",
    "vo_ts1_ok_haath": "शाबाश! हाथ शब्द में आ की मात्रा है।",
    "vo_ts1_ok_pin":   "शाबाश! पिन शब्द में छोटी इ की मात्रा है।",
    "vo_ts1_ok_neem":  "शाबाश! नीम शब्द में बड़ी ई की मात्रा है।",
    "vo_ts1_hint1":    "फिर से सुनो और सही मात्रा पहचानिए।",
    "vo_ts1_hint2":    "ध्यान से देखो, इस शब्द में कौन-सी मात्रा है?",

    # ---- Screen 12 · TRAIN_SORT matra -> word coach (deck page 15) ---------------------------
    "vo_ts2_prompt":  "सही मात्रा को सही शब्द वाली बोगी में डालिए।",
    "vo_ts2_ok_jaal": "शाबाश! जाल शब्द में आ की मात्रा लगी है।",
    "vo_ts2_ok_sir":  "शाबाश! सिर शब्द में छोटी इ की मात्रा लगी है।",
    "vo_ts2_ok_keel": "शाबाश! कील शब्द में बड़ी ई की मात्रा लगी है।",
    "vo_ts2_hint1":   "फिर से सोचो। इस शब्द में कौन-सी मात्रा लगी है?",
    "vo_ts2_hint2":   "ध्यान से देखो और शब्द को फिर से पढ़ो।",

    # ---- Screen 13 · MATRA_FILL (deck page 16) -----------------------------------------------
    "vo_mf_prompt":   "सही मात्रा को सही जगह पर खींचकर डालो और शब्द पूरा करिए।",
    "vo_mf_ok_jaal":  "शाबाश! जाल बन गया।",
    "vo_mf_ok_pari":  "शाबाश! परी बन गया।",
    "vo_mf_ok_hiran": "शाबाश! हिरण बन गया।",
    "vo_mf_hint1":    "फिर से सोचो।",
    "vo_mf_hint2":    "ध्यान से देखो। कौन-सी मात्रा लगेगी?",
    "vo_name_pari":   "परी",

    # ---- Screen 14 · TRAIN_SORT pictures only (deck page 17) ---------------------------------
    "vo_ts3_prompt":   "चित्र को सुनो और उसे सही मात्रा वाली बोगी में डालिए।",
    "vo_ts3_ok_haath": "शाबाश! हाथ में आ की मात्रा है।",
    "vo_ts3_ok_naak":  "शाबाश! नाक में आ की मात्रा है।",
    "vo_ts3_ok_pin":   "शाबाश! पिन में छोटी इ की मात्रा है।",
    "vo_ts3_ok_hiran": "शाबाश! हिरण में छोटी इ की मात्रा है।",
    "vo_ts3_ok_neem":  "शाबाश! नीम में बड़ी ई की मात्रा है।",
    "vo_ts3_ok_keel":  "शाबाश! कील में बड़ी ई की मात्रा है।",
    "vo_ts3_hint1":    "फिर से सुनो और सही मात्रा पहचानो।",
    "vo_ts3_hint2":    "शब्द को ध्यान से सुनो।",

    # ---- Screen 15 · POEM_SEARCH (deck page 18) ----------------------------------------------
    "vo_ps_r1":    "आ की मात्रा वाले शब्द ढूँढो।",
    "vo_ps_r2":    "अब छोटी इ की मात्रा वाले शब्द ढूँढो।",
    "vo_ps_r3":    "अब बड़ी ई की मात्रा वाले शब्द ढूँढो।",
    "vo_ps_ok":    "शाबाश!",
    "vo_ps_hint1": "फिर से देखो।",
    "vo_ps_hint2": "ध्यान से मात्रा पहचानो।",

    # ---- celebration (deck page 19 · N/C — ships as built) ------------------------------------
    "vo_cel_prompt": "शाबाश! आज हमने सीखा — आ, इ और ई की मात्रा पहचानना, और मात्रा वाले शब्द पढ़ना।",

    # ---- reused unchanged from the existing 95-clip set ---------------------------------------
    "vo_name_haath": "हाथ",
    "vo_name_naak":  "नाक",
    "vo_name_din":   "दिन",
    "vo_name_pin":   "पिन",
    "vo_name_neem":  "नीम",
    "vo_name_teer":  "तीर",
    "vo_name_hiran": "हिरण",
    "vo_pt_tutorial": "ध्यान से देखिए और मेरे साथ जानिए। चलिए, शुरू करें!",
    "vo_pt_guided":   "बहुत बढ़िया! अब हम साथ मिलकर शुरू करते हैं। चलिए, साथ में करें!",
    "vo_pt_practice": "वाह! अब आपकी बारी।",
    "sfx_celebrate": "celebration sound",
}

# Every clip that already exists on disk with EXACTLY this text — reused untouched. Regenerating an
# unchanged clip produces a different take, which is itself a change the deck never asked for.
REUSED = {
    "vo_name_haath", "vo_name_naak", "vo_name_din", "vo_name_pin", "vo_name_neem",
    "vo_name_teer", "vo_name_hiran", "vo_matra_i", "vo_matra_ee", "vo_cel_prompt",
    "vo_pt_tutorial", "vo_pt_guided", "vo_pt_practice", "sfx_celebrate",
}

# Pictures. The ten new ones are NOT generated this pass (user decision: assets skipped); every one
# has an emoji fallback so no screen is ever blank, and they are listed in ART_BRIEF.md.
IMAGES = {
    # existing on disk
    "obj_haath": "✋", "obj_naak": "👃", "obj_din": "☀️", "obj_pin": "📌",
    "obj_neem": "🌳", "obj_teer": "🏹", "obj_hiran": "🦌",
    # NEW — pending art
    "obj_jal": "💧", "obj_jaal": "🕸️", "obj_bal": "💪", "obj_bil": "🧾",
    "obj_kal": "📅", "obj_keel": "🔩", "obj_matka": "🏺", "obj_gati": "🏃",
    "obj_ladki": "👧", "obj_pari": "🧚",
}
NEW_ART = ["obj_jal", "obj_jaal", "obj_bal", "obj_bil", "obj_kal", "obj_keel",
           "obj_matka", "obj_gati", "obj_ladki", "obj_pari"]


def A(**kw):
    """audio block helper"""
    return dict(kw)


SLIDES = [
    # ============ TUTORIAL · 7 screens =======================================================
    {   # Screen 1 · deck page 4
        "id": "T1", "phase": "tutorial", "eis": "enactive", "type": "MATRA_PAIRS",
        "prompt_hi": "",                                   # row #16 "Remove the current heading text"
        "audio": A(prompt="vo_s1_prompt"),
        "data": {"auto": True, "pairs": [
            {"letter": "आ", "matra": "ा", "audio": "vo_matra_aa2"},
            {"letter": "इ", "matra": "ि", "audio": "vo_matra_i"},
            {"letter": "ई", "matra": "ी", "audio": "vo_matra_ee"},
        ]},
    },
    {   # Screen 2 · deck page 5
        "id": "T2", "phase": "tutorial", "eis": "iconic", "type": "MATRA_BUILD",
        "prompt_hi": "",   # deck: "Do not add extra explanatory text"
        "audio": A(prompt="vo_mb_jal_intro", base="vo_mb_jal_base", onset="vo_mb_jal_onset",
                   result="vo_name_jaal", sounds="vo_mb_jal_sounds",
                   explain="vo_mb_jal_explain"),
        "data": {"auto": True,
                 "base_word": "जल", "base_img": "obj_jal", "base_emoji": "💧",
                 "consonant": "ज", "matra": "ा", "syllable": "जा",
                 "result_word": "जाल", "result_img": "obj_jaal", "result_emoji": "🕸️"},
    },
    {   # Screen 3 · deck page 6
        "id": "T3", "phase": "tutorial", "eis": "iconic", "type": "MEET_EXAMPLES",
        "prompt_hi": "",
        "audio": A(prompt="vo_ex_aa_intro"),
        "data": {"auto": True, "examples": [
            {"word_hi": "नाक",  "matra": "ा", "img": "obj_naak",  "emoji": "👃", "audio": "vo_ex_naak"},
            {"word_hi": "मटका", "matra": "ा", "img": "obj_matka", "emoji": "🏺", "audio": "vo_ex_matka"},
        ]},
    },
    {   # Screen 4 · deck page 7
        "id": "T4", "phase": "tutorial", "eis": "iconic", "type": "MATRA_BUILD",
        "prompt_hi": "",   # deck: "Do not add extra explanatory text"
        "audio": A(prompt="vo_mb_bil_intro", base="vo_mb_bil_base", onset="vo_mb_bil_onset",
                   result="vo_name_bil", sounds="vo_mb_bil_sounds",
                   explain="vo_mb_bil_explain"),
        "data": {"auto": True,
                 "base_word": "बल", "base_img": "obj_bal", "base_emoji": "💪",
                 "consonant": "ब", "matra": "ि", "syllable": "बि",
                 "result_word": "बिल", "result_img": "obj_bil", "result_emoji": "🕳️"},
    },
    {   # Screen 5 · deck page 8
        "id": "T5", "phase": "tutorial", "eis": "iconic", "type": "MEET_EXAMPLES",
        "prompt_hi": "",
        "audio": A(prompt="vo_ex_i_intro"),
        "data": {"auto": True, "examples": [
            {"word_hi": "दिन", "matra": "ि", "img": "obj_din",  "emoji": "☀️", "audio": "vo_ex_din"},
            {"word_hi": "गति", "matra": "ि", "img": "obj_gati", "emoji": "🏃", "audio": "vo_ex_gati"},
        ]},
    },
    {   # Screen 6 · deck page 9
        "id": "T6", "phase": "tutorial", "eis": "iconic", "type": "MATRA_BUILD",
        "prompt_hi": "",   # deck: "Do not add extra explanatory text"
        "audio": A(prompt="vo_mb_keel_intro", base="vo_mb_keel_base", onset="vo_mb_keel_onset",
                   result="vo_name_keel", sounds="vo_mb_keel_sounds",
                   explain="vo_mb_keel_explain"),
        "data": {"auto": True,
                 "base_word": "कल", "base_img": "obj_kal", "base_emoji": "📅",
                 "consonant": "क", "matra": "ी", "syllable": "की",
                 "result_word": "कील", "result_img": "obj_keel", "result_emoji": "🔩"},
    },
    {   # Screen 7 · deck page 10
        "id": "T7", "phase": "tutorial", "eis": "iconic", "type": "MEET_EXAMPLES",
        "prompt_hi": "",
        "audio": A(prompt="vo_ex_ee_intro"),
        "data": {"auto": True, "examples": [
            {"word_hi": "तीर",   "matra": "ी", "img": "obj_teer",  "emoji": "🏹", "audio": "vo_ex_teer"},
            {"word_hi": "लड़की", "matra": "ी", "img": "obj_ladki", "emoji": "👧", "audio": "vo_ex_ladki"},
        ]},
    },

    # ============ GUIDED · 4 screens =========================================================
    {   # Screen 8 · deck page 11
        "id": "G1", "phase": "guided", "eis": "iconic", "type": "TRAIN_TAP",
        "prompt_hi": "",                                   # row #96 "No instruction text on screen"
        "audio": A(prompt="vo_tt_aa_prompt", correct="vo_tt_aa_correct",
                   hint1="vo_tt_aa_hint1", hint2="vo_tt_aa_hint2",
                   reveal="vo_rev_tt_aa", try_again="vo_tt_aa_hint1"),
        "data": {"signal": "matra_tap_first_try", "options": [
            {"word_hi": "हाथ", "audio": "vo_name_haath", "correct": True},
            {"word_hi": "दिन", "audio": "vo_name_din"},
            {"word_hi": "नीम", "audio": "vo_name_neem"},
        ]},
        "signals": {"on_complete": ["matra_tap_first_try"]},
    },
    {   # Screen 9 · deck page 12
        "id": "G2", "phase": "guided", "eis": "iconic", "type": "TRAIN_TAP",
        "prompt_hi": "",
        "audio": A(prompt="vo_tt_i_prompt", correct="vo_tt_i_correct",
                   hint1="vo_tt_i_hint1", hint2="vo_tt_i_hint2",
                   reveal="vo_rev_tt_i", try_again="vo_tt_i_hint1"),
        "data": {"signal": "matra_tap_first_try", "options": [
            {"word_hi": "पिन", "audio": "vo_name_pin", "correct": True},
            {"word_hi": "नाक", "audio": "vo_name_naak"},
            {"word_hi": "तीर", "audio": "vo_name_teer"},
        ]},
        "signals": {"on_complete": ["matra_tap_first_try"]},
    },
    {   # Screen 10 · deck page 13
        "id": "G3", "phase": "guided", "eis": "iconic", "type": "TRAIN_TAP",
        "prompt_hi": "",
        "audio": A(prompt="vo_tt_ee_prompt", correct="vo_tt_ee_correct",
                   hint1="vo_tt_ee_hint1", hint2="vo_tt_ee_hint2",
                   reveal="vo_rev_tt_ee", try_again="vo_tt_ee_hint1"),
        "data": {"signal": "matra_tap_first_try", "options": [
            {"word_hi": "पानी", "audio": "vo_name_paani", "correct": True},
            {"word_hi": "नाक",  "audio": "vo_name_naak"},
            {"word_hi": "दिन",  "audio": "vo_name_din"},
        ]},
        "signals": {"on_complete": ["matra_tap_first_try"]},
    },
    {   # Screen 11 · deck page 14 — word cards into matra coaches
        "id": "G4", "phase": "guided", "eis": "enactive", "type": "TRAIN_SORT",
        "prompt_hi": "",
        "audio": A(prompt="vo_ts1_prompt", hint1="vo_ts1_hint1", hint2="vo_ts1_hint2",
                   try_again="vo_ts1_hint1"),
        "data": {"signal": "matra_sort_correct",
                 "bins": [{"key": "aa", "label": "आ (ा)"}, {"key": "i", "label": "इ (ि)"},
                          {"key": "ee", "label": "ई (ी)"}],
                 "items": [
                     {"key": "aa", "word_hi": "हाथ", "img": "obj_haath", "emoji": "✋",
                      "audio": "vo_name_haath", "correct_audio": "vo_ts1_ok_haath"},
                     {"key": "i",  "word_hi": "पिन", "img": "obj_pin", "emoji": "📌",
                      "audio": "vo_name_pin", "correct_audio": "vo_ts1_ok_pin"},
                     {"key": "ee", "word_hi": "नीम", "img": "obj_neem", "emoji": "🌳",
                      "audio": "vo_name_neem", "correct_audio": "vo_ts1_ok_neem"},
                 ]},
        "signals": {"on_complete": ["matra_sort_correct"]},
    },

    # ============ PRACTICE · 5 screens =======================================================
    {   # Screen 12 · deck page 15 — the REVERSE mapping: matra cards into word coaches
        "id": "P1", "phase": "practice", "eis": "enactive", "type": "TRAIN_SORT",
        "prompt_hi": "",
        "audio": A(prompt="vo_ts2_prompt", hint1="vo_ts2_hint1", hint2="vo_ts2_hint2",
                   try_again="vo_ts2_hint1"),
        "data": {"signal": "matra_sort_correct",
                 "bins": [{"key": "aa", "label": "जाल"}, {"key": "i", "label": "सिर"},
                          {"key": "ee", "label": "कील"}],
                 "items": [
                     {"key": "aa", "glyph": "ा", "correct_audio": "vo_ts2_ok_jaal"},
                     {"key": "i",  "glyph": "ि", "correct_audio": "vo_ts2_ok_sir"},
                     {"key": "ee", "glyph": "ी", "correct_audio": "vo_ts2_ok_keel"},
                 ]},
        "signals": {"on_complete": ["matra_sort_correct"]},
    },
    {   # Screen 13 · deck page 16 — fill the blank.
        # `blank_at` is an index into the CONSONANT-GROUP sequence, never a character offset:
        # in हिरण the ि is stored after ह but DRAWN before it, so the blank sits at index 0.
        # हीरा was CORRECTED to हिरण on the SME's explicit instruction (row #149) — हीरा is
        # unusable anyway, it carries two in-scope matras (ी and ा).
        "id": "P2", "phase": "practice", "eis": "enactive", "type": "MATRA_FILL",
        "prompt_hi": "",
        "audio": A(prompt="vo_mf_prompt", hint1="vo_mf_hint1", hint2="vo_mf_hint2",
                   try_again="vo_mf_hint1"),
        "data": {"signal": "matra_fill_correct",
                 "options": ["ा", "ि", "ी"], "reuse_options": True,
                 "slots": [
                     {"word": "जाल", "parts": ["ज", "ल"], "blank_at": 1, "matra": "ा",
                      "img": "obj_jaal", "emoji": "🕸️", "audio": "vo_name_jaal",
                      "correct_audio": "vo_mf_ok_jaal"},
                     {"word": "परी", "parts": ["पर"], "blank_at": 1, "matra": "ी",
                      "img": "obj_pari", "emoji": "🧚", "audio": "vo_name_pari",
                      "correct_audio": "vo_mf_ok_pari"},
                     {"word": "हिरण", "parts": ["ह", "रण"], "blank_at": 0, "matra": "ि",
                      "img": "obj_hiran", "emoji": "🦌", "audio": "vo_name_hiran",
                      "correct_audio": "vo_mf_ok_hiran"},
                 ]},
        "signals": {"on_complete": ["matra_fill_correct"]},
    },
    {   # Screen 14 · deck page 17 — PICTURES ONLY, no word text at any point
        "id": "P3", "phase": "practice", "eis": "enactive", "type": "TRAIN_SORT",
        "prompt_hi": "",
        "audio": A(prompt="vo_ts3_prompt", hint1="vo_ts3_hint1", hint2="vo_ts3_hint2",
                   try_again="vo_ts3_hint1"),
        "data": {"signal": "matra_sort_correct", "hide_labels": True, "multi": True,
                 "bins": [{"key": "aa", "label": "आ (ा)"}, {"key": "i", "label": "इ (ि)"},
                          {"key": "ee", "label": "ई (ी)"}],
                 "items": [
                     {"key": "aa", "word_hi": "हाथ",  "img": "obj_haath", "emoji": "✋",
                      "audio": "vo_name_haath", "correct_audio": "vo_ts3_ok_haath"},
                     {"key": "aa", "word_hi": "नाक",  "img": "obj_naak", "emoji": "👃",
                      "audio": "vo_name_naak", "correct_audio": "vo_ts3_ok_naak"},
                     {"key": "i",  "word_hi": "पिन",  "img": "obj_pin", "emoji": "📌",
                      "audio": "vo_name_pin", "correct_audio": "vo_ts3_ok_pin"},
                     {"key": "i",  "word_hi": "हिरण", "img": "obj_hiran", "emoji": "🦌",
                      "audio": "vo_name_hiran", "correct_audio": "vo_ts3_ok_hiran"},
                     {"key": "ee", "word_hi": "नीम",  "img": "obj_neem", "emoji": "🌳",
                      "audio": "vo_name_neem", "correct_audio": "vo_ts3_ok_neem"},
                     {"key": "ee", "word_hi": "कील",  "img": "obj_keel", "emoji": "🔩",
                      "audio": "vo_name_keel", "correct_audio": "vo_ts3_ok_keel"},
                 ]},
        "signals": {"on_complete": ["matra_sort_correct"]},
    },
    {   # Screen 15 · deck page 18 — «मात्रा खोजो».
        # TARGET LIST COMPLETED per §4 Option A (ruled 2026-09-17). The deck's own list omitted
        # चमकी and की (both ी) and मीना and गाए (both ा) — a child tapping them correctly would
        # have been buzzed. मीना deliberately belongs to TWO rounds; the module supports that.
        "id": "P4", "phase": "practice", "eis": "symbolic", "type": "POEM_SEARCH",
        "prompt_hi": "",
        # round 1's line IS this slide's instruction; naming it as the prompt role also means the
        # replay chip and the voice-role receipt both have something to point at. The module sets
        # state.ownsAudio, so mountSlide does NOT also autoplay it — no double voice.
        "audio": A(prompt="vo_ps_r1", correct="vo_ps_ok", hint1="vo_ps_hint1", hint2="vo_ps_hint2",
                   try_again="vo_ps_hint1"),
        "data": {"signal": "poem_search_correct",
                 "poem_lines": ["रवि लाया लाल पतंग,",
                                "दिन में चमकी सूरज की किरण।",
                                "नीम तले मीना गाए संग।"],
                 "rounds": [
                     {"matra": "ा", "targets": ["लाया", "लाल", "मीना", "गाए"], "audio": "vo_ps_r1"},
                     {"matra": "ि", "targets": ["रवि", "दिन", "किरण"],          "audio": "vo_ps_r2"},
                     {"matra": "ी", "targets": ["चमकी", "की", "नीम", "मीना"],  "audio": "vo_ps_r3"},
                 ]},
        "signals": {"on_complete": ["poem_search_correct"]},
    },
    {   # deck page 19 · N/C — ships as built
        # «मात्रा टोकरी» - the catch-the-word arcade, folded in as the last activity before the
        # celebration. It was delivered as a standalone single-game build; its own title screen
        # and win overlay are dropped (this lesson has both already) and the rest is a module.
        # Three rounds live INSIDE it (ा then ि then ी), so it is one slide, not three: the
        # round-to-round praise clips are authored as single takes that carry the next
        # instruction, and splitting them across slides would cut every one of them in half.
        "id": "G7", "phase": "practice", "eis": "enactive", "type": "MATRA_TOKRI",
        "prompt_hi": "",          # X2: nothing written on screen, the VO carries it
        "audio": A(prompt="vo_mt_intro"),
        # The module carries its own ROUNDS table, but every clip it will reach for is declared
        # HERE so the engine warms it, the receipt checks it, and a missing take shows up in the
        # build rather than as silence on the twelfth word of round three.
        "data": {"clips": [
                {"audio": "vo_mt_round_aa"},
                {"audio": "vo_mt_round_i"},
                {"audio": "vo_mt_round_ee"},
                {"audio": "vo_mt_cheer_i"},
                {"audio": "vo_mt_cheer_ee"},
                {"audio": "vo_mt_done"},
                {"audio": "vo_mt_w_naav"},
                {"audio": "vo_mt_w_haath"},
                {"audio": "vo_mt_w_baal"},
                {"audio": "vo_mt_w_kaam"},
                {"audio": "vo_mt_w_daal"},
                {"audio": "vo_mt_w_din"},
                {"audio": "vo_mt_w_til"},
                {"audio": "vo_mt_w_sir"},
                {"audio": "vo_mt_w_dil"},
                {"audio": "vo_mt_w_hiran"},
                {"audio": "vo_mt_w_nadi"},
                {"audio": "vo_mt_w_teer"},
                {"audio": "vo_mt_w_chini"},
                {"audio": "vo_mt_w_machhli"},
                {"audio": "vo_mt_w_neem"}
        ]},
    },
    {
        "id": "CEL", "phase": "practice", "eis": "enactive", "type": "CELEBRATION",
        "prompt_hi": "शाबाश! आज हमने सीखा — आ, इ और ई की मात्रा पहचानना, और मात्रा वाले शब्द पढ़ना।",
        "audio": A(prompt="vo_cel_prompt", sfx="sfx_celebrate"),
        "data": {},
    },
]

CARD = {
    "version": "0.2",
    "skill_code": CODE,
    "lo_code": "HI02H11_L02",
    "grade": "02",
    "attribute": "H11",
    "skill_type": "CORE",
    "part_label": "",
    "medium": "hi",
    # deck row #3 — the note's title wins over the mockup's «शब्दों की रेल» (§7.1): it is the later,
    # explicit instruction, and this lesson is about matras, not words generally.
    "title": {"hi": "मात्राओं की रेल", "en": "The matra train"},
    "subtitle_hi": "",                       # row #4 "Remove all extra text that is not required."
    "theme": "toybox",
    "skill_description_hi": "आ, इ, ई मात्रा वाले शब्द पढ़ता है। शब्दों में आने वाली मात्रा पहचानता है।",
    "landing_audio": "vo_landing",
    # rows #6, #8, #9, #14 — the three matra boxes ARE the train's coaches (mockup slide03)
    "landing_hero": {"kind": "matra_train", "matras": ["ा", "ि", "ी"]},
    "phase_transition_audio": {"tutorial": "vo_pt_tutorial", "guided": "vo_pt_guided",
                               "practice": "vo_pt_practice"},
    # the journey beats are a LOCKED house behaviour — preserved verbatim from the shipped card
    "phase_transition_title": {"tutorial": "चलो, शुरू करें!", "guided": "साथ में करें।",
                               "practice": "अब तुम्हारी बारी।"},
    "phase_distribution": {"tutorial": 7, "guided": 4, "practice": 5},
    # ---- deck row X1: the SME's 3-attempt ladder --------------------------------------------
    # rung 1 = hint VO, explicitly NO hand · rung 2 = hint VO + the hand on the CORRECT target,
    # child still answers · 3rd-attempt correct = visual celebration, SILENT.
    # `hand_in_practice` is the deck-scoped opt-in past the engine's round-3 hand ban — FLAGGED
    # in CHANGES.md for a ruling, never silently applied fleet-wide.
    "scaffold_rules": {
        "nudge_timeout_ms": {"guided": 6000, "practice": 8000},
        "max_attempts": 3,
        "hand_on_attempt": 2,
        "silent_on_late_correct": True,
        "hand_in_practice": True,
    },
    "signals_expected": ["slide_entered", "slide_completed", "matra_tap_first_try",
                         "matra_sort_correct", "matra_fill_correct", "poem_search_correct",
                         "lesson_completed", "mastery_score"],
    "_emoji_fallback": dict(IMAGES),
    "slides": SLIDES,
}


def main():
    mono = require_engine()

    used_audio = set()

    def walk(o):
        if isinstance(o, list):
            for x in o:
                walk(x)
        elif isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and (k in ("audio", "correct_audio", "prompt", "base",
                                                 "onset", "result", "explain", "sounds", "hint1", "hint2",
                                                 "try_again", "correct", "reveal", "sfx")
                                           and re.fullmatch(r"(vo|sfx)_[\w]+", v)):
                    used_audio.add(v)
                else:
                    walk(v)

    walk(CARD["slides"])
    used_audio.add(CARD["landing_audio"])
    used_audio.update(CARD["phase_transition_audio"].values())

    unknown = sorted(used_audio - set(VO))
    if unknown:
        raise SystemExit(f"  X  slides reference audio ids with no text authored: {unknown}")

    # [audio-split] SFX and VO live in separate folders. One helper, so the card, the
    # existence check below and the engine's VO_DIR/SFX_DIR can never drift apart.
    def audio_path(k):
        return f"assets/Audio/{'SFX' if k.startswith('sfx_') else 'VO'}/{k}.ogg"

    CARD["assets"] = {
        "audio": {k: audio_path(k) for k in sorted(used_audio)},
        "audio_text": {k: VO[k] for k in sorted(used_audio)},
        "image": {k: f"assets/Images/{k}.png" for k in sorted(IMAGES)},
        "audio_ext": "ogg",
        "img_ext": "png",
    }

    cardjson = json.dumps(CARD, ensure_ascii=False).replace("</script>", "<\\/script>")
    html, n = _CARD_TAG.subn(lambda m: m.group(1) + "\n" + cardjson + "\n" + m.group(3), mono, count=1)
    if n != 1:
        raise SystemExit("  X  cardData tag not found in the engine")

    # ---- first-slide image preload -----------------------------------------------------------
    # The engine template arrived carrying two HARDCODED preloads for ANOTHER game's images
    # (pic_kaam / pic_naak), which put 2 SEVERE 404s on every page load of this one. Removed from
    # the template; the preload is generated per-game here instead, and ONLY for files that are
    # actually on disk — preloading a not-yet-produced image would just recreate the 404s.
    first_keys, seen = [], []
    def _walk_img(o):
        if isinstance(o, list):
            for x in o: _walk_img(x)
        elif isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and k in ("img", "base_img", "result_img", "label_img")                         and re.fullmatch(r"[\w-]+", v):
                    if v not in seen:
                        seen.append(v); first_keys.append(v)
                else:
                    _walk_img(v)
    _walk_img(CARD["slides"][:3])
    on_disk = [k for k in first_keys
               if os.path.exists(os.path.join(OUT, "assets", "Images", k + ".png"))]
    links = "".join(f'<link rel="preload" as="image" fetchpriority="high" '
                    f'href="assets/Images/{k}.png">' for k in on_disk)
    assert "</head>" in html, "no </head> in built HTML — preload injection would be silent"
    html = html.replace("</head>", links + "</head>", 1)

    # newline="" (i.e. NO newline translation). Python's default text mode rewrote every LF
    # as CRLF on Windows, so a rebuild that changed NOTHING still reported 18k changed lines
    # and buried the real diff. The engine template is LF; the build output now matches it.
    html_path = os.path.join(OUT, f"{CODE}.html")
    with open(html_path, "w", encoding="utf-8", newline="") as f:
        f.write(html)
    with open(os.path.join(OUT, "card.json"), "w", encoding="utf-8", newline="") as f:
        f.write(json.dumps(CARD, ensure_ascii=False, indent=2))

    # ---- report what still has to be produced -------------------------------------------------
    img_dir = os.path.join(OUT, "assets", "Images")
    on_disk_audio = lambda k: os.path.exists(os.path.join(OUT, audio_path(k).replace("/", os.sep)))
    missing_audio = [k for k in sorted(used_audio) if not on_disk_audio(k)]
    missing_img = [k for k in sorted(IMAGES)
                   if not os.path.exists(os.path.join(img_dir, k + ".png"))]

    types = sorted(set(s["type"] for s in CARD["slides"]))
    print(f"  Built {CODE}: {len(CARD['slides'])} slides · {len(used_audio)} audio ids · "
          f"{len(IMAGES)} images · phases {CARD['phase_distribution']}")
    print(f"  types: {types}")
    print(f"  PENDING VO  ({len(missing_audio)}): {', '.join(missing_audio) or 'none'}")
    print(f"  PENDING ART ({len(missing_img)}): {', '.join(missing_img) or 'none'}")
    print(f"  reused unchanged: {len(REUSED & used_audio)} clips")
    print(f"  first-slide preloads emitted: {len(on_disk)} ({', '.join(on_disk) or 'none on disk yet'})")
    # A clip whose FILE exists but whose TEXT changed is the dangerous case: it passes every
    # existence check and ships the wrong words. vo_landing is one — its id is hardcoded in the
    # engine boot, so it cannot be re-minted and MUST be re-recorded.
    prev = os.path.join(OUT, "card.pre_revise.json")
    if os.path.exists(prev):
        oldtext = json.load(open(prev, encoding="utf-8"))["assets"]["audio_text"]
        rerec = [k for k in sorted(used_audio)
                 if k in oldtext and oldtext[k] != VO[k] and on_disk_audio(k)]
        print(f"  RE-RECORD (file exists, TEXT CHANGED): {', '.join(rerec) or 'none'}")


if __name__ == "__main__":
    main()
