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
import array, contextlib, wave    # [r38] cue measurement
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
    # [r38] pages 3, 5, 7 moved onto the sibling's MEET_PAIR, whose beats are placed by the
    # measured cues below rather than by fixed delays. MEET_EXAMPLES stays required: it is still
    # reached from MEET_LETTER by cards that author data.examples[].
    ("SlideModules.MEET_PAIR",    "MEET_PAIR missing - pages 3, 5, 7 have no module"),
    ("function matraHLSoon",
     "the ink-mask matra highlight is missing - rung 2 on pages 8-13 lights ONE matra inside a "
     "word, which the older clip-column method cannot do for a word with two of them"),
    ("function hintHold",
     "the hint ladder's screen-hold is missing - the gaps BETWEEN a rung-2 chain's clips would "
     "leave the screen live, and a tap in one of them starts rung 3 on top of rung 2"),
    ('ladder3: { demo: tapDemo, lock: tapLock }',
     "TRAIN_TAP is not passing the three-rung ladder - pages 8-10 would fall back to two rungs"),

    ("SlideModules.TRAIN_TAP",     "TRAIN_TAP module missing (deck pages 11, 12, 13)"),
    ("SlideModules.TRAIN_SORT",    "TRAIN_SORT module missing (deck pages 14, 15, 17)"),
    ("SlideModules.MATRA_FILL",    "MATRA_FILL module missing (deck page 16)"),
    ("SlideModules.OBJECT_HUNT",   "OBJECT_HUNT module missing (deck slides 18, 19, 20 — the "
                                   "object hunt that replaces the poem search)"),
    (".oh-scene{",                 "the OBJECT_HUNT scene CSS is missing — the objects would "
                                   "stack at the top-left with no scene behind them"),
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
    # [r38] page 1 reads each letter and THEN names its matra; the matra lights on the
    # second clause (see _cue_ms), so the glow lands on the words that name it.
    "vo_pair_aa":         "यह है आ। इसकी मात्रा है।",
    "vo_pair_i":          "यह है इ। इसकी मात्रा है।",
    "vo_pair_ee":         "यह है ई। इसकी मात्रा है।",
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
    "vo_tt_aa_prompt":  "“आ” की मात्रा वाले शब्द पर टैप कीजिए।",
    "vo_tt_aa_correct": "शाबाश! हाथ शब्द में आ की मात्रा है।",
    "vo_tt_aa_hint1":   "फिर से पढ़िए। जिस शब्द में “आ” की मात्रा आ रही है, उस पर टैप कीजिए।",
    "vo_tt_aa_hint2":   "जिस शब्द में “आ” की मात्रा है, उस पर टैप कीजिए।",
    "vo_rev_tt_aa":     "सही डिब्बा यह है। हाथ शब्द में आ की मात्रा है।",

    # ---- Screen 9 · TRAIN_TAP छोटी इ (deck page 12) ------------------------------------------
    "vo_tt_i_prompt":  "“इ” की मात्रा वाले शब्द पर टैप कीजिए।",
    "vo_tt_i_correct": "शाबाश! पिन शब्द में छोटी इ की मात्रा है।",
    "vo_tt_i_hint1":    "फिर से पढ़िए। जिस शब्द में “इ” की मात्रा आ रही है, उस पर टैप कीजिए।",
    "vo_tt_i_hint2":    "जिस शब्द में “इ” की मात्रा है, उस पर टैप कीजिए।",
    "vo_rev_tt_i":     "सही डिब्बा यह है। पिन शब्द में छोटी इ की मात्रा है।",

    # ---- Screen 10 · TRAIN_TAP बड़ी ई (deck page 13) -----------------------------------------
    "vo_tt_ee_prompt":  "“ई” की मात्रा वाले शब्द पर टैप कीजिए।",
    "vo_tt_ee_correct": "शाबाश! पानी शब्द में बड़ी ई की मात्रा है।",
    "vo_tt_ee_hint1":   "फिर से पढ़िए। जिस शब्द में “ई” की मात्रा आ रही है, उस पर टैप कीजिए।",
    "vo_tt_ee_hint2":   "जिस शब्द में “ई” की मात्रा है, उस पर टैप कीजिए।",
    "vo_rev_tt_ee":     "सही डिब्बा यह है। पानी शब्द में बड़ी ई की मात्रा है।",
    "vo_name_paani":    "पानी",

    # [r37] RUNG 3 on the tap screens - the answer is NAMED while it glows under the hand.
    # The doc's own template: "देखिए, ‘पुल’ में त ...".
    "vo_tt_aa_hint3":   "देखिए, “हाथ” में “आ” की मात्रा है। “हाथ” पर टैप कीजिए।",
    "vo_tt_i_hint3":    "देखिए, “पिन” में “इ” की मात्रा है। “पिन” पर टैप कीजिए।",
    "vo_tt_ee_hint3":   "देखिए, “पानी” में “ई” की मात्रा है। “पानी” पर टैप कीजिए।",


    # [r37] THE REVIEW-1 LADDER ON THE DRAG SCREENS (pages 12, 13).
    # The three matra names are shared: on page 12 they are what each COACH is labelled
    # with, on page 13 they are the name of the thing being DRAGGED.
    "vo_letter_aa":       "“आ” की मात्रा।",
    "vo_letter_i":        "“इ” की मात्रा।",
    "vo_letter_ee":       "“ई” की मात्रा।",
    "vo_name_sir":        "सिर",

    # page 12 - rung 2 names the word that was mis-dropped, rung 3 names its coach
    "vo_ts1_h2_haath":    "ध्यान से सुनिए — “हाथ”। “हाथ” में “आ” की मात्रा है।",
    "vo_ts1_h3_haath":    "“हाथ” में “आ” की मात्रा है। इसे “आ” की मात्रा वाले डिब्बे में डालिए।",
    "vo_ts1_h2_pin":      "ध्यान से सुनिए — “पिन”। “पिन” में “इ” की मात्रा है।",
    "vo_ts1_h3_pin":      "“पिन” में “इ” की मात्रा है। इसे “इ” की मात्रा वाले डिब्बे में डालिए।",
    "vo_ts1_h2_neem":     "ध्यान से सुनिए — “नीम”। “नीम” में “ई” की मात्रा है।",
    "vo_ts1_h3_neem":     "“नीम” में “ई” की मात्रा है। इसे “ई” की मात्रा वाले डिब्बे में डालिए।",

    # page 13 - the reverse round: the MATRA is dragged into the word it belongs in
    "vo_ts2_h2_aa":       "यह “आ” की मात्रा है। देखिए, किस शब्द में यह मात्रा लगेगी।",
    "vo_ts2_h3_aa":       "“आ” की मात्रा “जाल” में लगेगी। इसे “जाल” वाले डिब्बे में डालिए।",
    "vo_ts2_h2_i":        "यह “इ” की मात्रा है। देखिए, किस शब्द में यह मात्रा लगेगी।",
    "vo_ts2_h3_i":        "“इ” की मात्रा “सिर” में लगेगी। इसे “सिर” वाले डिब्बे में डालिए।",
    "vo_ts2_h2_ee":       "यह “ई” की मात्रा है। देखिए, किस शब्द में यह मात्रा लगेगी।",
    "vo_ts2_h3_ee":       "“ई” की मात्रा “कील” में लगेगी। इसे “कील” वाले डिब्बे में डालिए।",

    # ---- Screen 11 · TRAIN_SORT word -> matra coach (deck page 14) ---------------------------
    # [r29 · SME] the watch-only screen that comes BEFORE the first drag activity
    "vo_ts0_prompt":   "देखिए, शब्द को उसकी सही मात्रा वाले डिब्बे में इस तरह ले जाते हैं।",
    "vo_ts1_prompt":   "हर शब्द को उसकी सही मात्रा वाले डिब्बे में डालिए।",
    "vo_ts1_ok_haath": "शाबाश! हाथ शब्द में आ की मात्रा है।",
    "vo_ts1_ok_pin":   "शाबाश! पिन शब्द में छोटी इ की मात्रा है।",
    "vo_ts1_ok_neem":  "शाबाश! नीम शब्द में बड़ी ई की मात्रा है।",
    "vo_ts1_hint1":       "फिर से पढ़िए। शब्द में कौन-सी मात्रा है, देखिए और उसे उसी मात्रा वाले डिब्बे में डालिए।",
    "vo_ts1_hint2":    "ध्यान से देखो, इस शब्द में कौन-सी मात्रा है?",

    # ---- Screen 12 · TRAIN_SORT matra -> word coach (deck page 15) ---------------------------
    "vo_ts2_prompt":  "सही मात्रा को सही शब्द वाले डिब्बे में डालिए।",
    "vo_ts2_ok_jaal": "शाबाश! जाल शब्द में आ की मात्रा लगी है।",
    "vo_ts2_ok_sir":  "शाबाश! सिर शब्द में छोटी इ की मात्रा लगी है।",
    "vo_ts2_ok_keel": "शाबाश! कील शब्द में बड़ी ई की मात्रा लगी है।",
    "vo_ts2_hint1":       "फिर से देखिए। मात्रा को ध्यान से देखिए और उसे सही शब्द वाले डिब्बे में डालिए।",
    "vo_ts2_hint2":   "ध्यान से देखो और शब्द को फिर से पढ़ो।",

    # ---- Screen 13 · MATRA_FILL (deck page 16) -----------------------------------------------
    "vo_mf_prompt":   "मात्रा को सही डिब्बे में डालकर शब्द पूरा कीजिए।",
    "vo_mf_ok_jaal":  "शाबाश! जाल बन गया।",
    "vo_mf_ok_pari":  "शाबाश! परी बन गया।",
    "vo_mf_ok_hiran": "शाबाश! हिरण बन गया।",
    "vo_mf_hint1":        "फिर से देखिए। चित्र का नाम सोचिए और सही मात्रा लगाइए।",
    "vo_mf_hint2":        "नाम ध्यान से सुनिए। जो मात्रा सही लग रही है, वही चुनिए।",
    "vo_mf_hint3":        "देखिए, जिस शब्द पर हाथ है उसी की खाली जगह में यह मात्रा लगेगी। इसे वहीं डालिए।",
    "vo_name_pari":   "परी",

    # ---- Screen 14 · TRAIN_SORT pictures only (deck page 17) ---------------------------------
    "vo_ts3_prompt":   "चित्र देखकर उसे सही मात्रा वाले डिब्बे में डालिए।",
    "vo_ts3_ok_haath": "शाबाश! हाथ में आ की मात्रा है।",
    "vo_ts3_ok_naak":  "शाबाश! नाक में आ की मात्रा है।",
    "vo_ts3_ok_pin":   "शाबाश! पिन में छोटी इ की मात्रा है।",
    "vo_ts3_ok_hiran": "शाबाश! हिरण में छोटी इ की मात्रा है।",
    "vo_ts3_ok_neem":  "शाबाश! नीम में बड़ी ई की मात्रा है।",
    "vo_ts3_ok_keel":  "शाबाश! कील में बड़ी ई की मात्रा है।",
    "vo_ts3_hint1":    "फिर से सुनो और सही मात्रा पहचानो।",
    "vo_ts3_hint2":    "शब्द को ध्यान से सुनो।",

    # ---- Screens 15-17 · OBJECT_HUNT (deck slides 18, 19, 20) --------------------------------
    # The screen prompts, the ladder's two hints, and the round's closing line.
    "vo_oh_aa_intro":  "आ की मात्रा वाले चित्र खोजिए और उन पर टैप कीजिए।",
    "vo_oh_i_intro":   "छोटी इ की मात्रा वाले चित्र खोजिए और उन पर टैप कीजिए।",
    "vo_oh_ee_intro":  "बड़ी ई की मात्रा वाले चित्र खोजिए और उन पर टैप कीजिए।",
    "vo_oh_aa_wrong":  "फिर से सोचिए। आ की मात्रा वाला चित्र खोजिए।",
    "vo_oh_i_wrong":   "फिर से सोचिए। छोटी इ की मात्रा वाला चित्र खोजिए।",
    "vo_oh_ee_wrong":  "फिर से सोचिए। बड़ी ई की मात्रा वाला चित्र खोजिए।",
    "vo_oh_hint1":     "चित्र का नाम ध्यान से सुनिए और मात्रा पहचानिए।",
    "vo_oh_aa_hint2":  "ध्यान से देखिए और आ की मात्रा वाले चित्र पर टैप कीजिए।",
    "vo_oh_i_hint2":   "ध्यान से देखिए और छोटी इ की मात्रा वाले चित्र पर टैप कीजिए।",
    "vo_oh_ee_hint2":  "ध्यान से देखिए और बड़ी ई की मात्रा वाले चित्र पर टैप कीजिए।",
    "vo_oh_aa_done":   "शाबाश! आपने आ की मात्रा वाले सभी चित्र खोज लिए।",
    "vo_oh_i_done":    "शाबाश! आपने छोटी इ की मात्रा वाले सभी चित्र खोज लिए।",
    "vo_oh_ee_done":   "शाबाश! आपने बड़ी ई की मात्रा वाले सभी चित्र खोज लिए।",

    # Per-object praise. ok_* names the matra (used when the screen is finished by that tap);
    # more_* praises and sends the child back for the rest, which is what a mid-screen tap
    # needs to hear.
    "vo_oh_aa_ok_aam":   "शाबाश! आम में आ की मात्रा है।",
    "vo_oh_aa_ok_maala":   "शाबाश! माला में आ की मात्रा है।",
    "vo_oh_aa_ok_gaajar":   "शाबाश! गाजर में आ की मात्रा है।",
    "vo_oh_aa_ok_taala":   "शाबाश! ताला में आ की मात्रा है।",
    "vo_oh_i_ok_pin":   "शाबाश! पिन में छोटी इ की मात्रा है।",
    "vo_oh_i_ok_kitaab":   "शाबाश! किताब में छोटी इ की मात्रा है।",
    "vo_oh_i_ok_chidiya":   "शाबाश! चिड़िया में छोटी इ की मात्रा है।",
    "vo_oh_i_ok_hiran":   "शाबाश! हिरण में छोटी इ की मात्रा है।",
    "vo_oh_ee_ok_ladki":   "शाबाश! लड़की में बड़ी ई की मात्रा है।",
    "vo_oh_ee_ok_paani":   "शाबाश! पानी में बड़ी ई की मात्रा है।",
    "vo_oh_ee_ok_ghadi":   "शाबाश! घड़ी में बड़ी ई की मात्रा है।",
    "vo_oh_ee_ok_machhli":   "शाबाश! मछली में बड़ी ई की मात्रा है।",

    "vo_oh_aa_more_aam": "बहुत बढ़िया, आम! अब और आ की मात्रा वाले चित्र ढूँढिए।",
    "vo_oh_aa_more_maala": "बहुत बढ़िया, माला! अब और आ की मात्रा वाले चित्र ढूँढिए।",
    "vo_oh_aa_more_gaajar": "बहुत बढ़िया, गाजर! अब और आ की मात्रा वाले चित्र ढूँढिए।",
    "vo_oh_aa_more_taala": "बहुत बढ़िया, ताला! अब और आ की मात्रा वाले चित्र ढूँढिए।",
    "vo_oh_i_more_pin": "बहुत बढ़िया, पिन! अब और छोटी इ की मात्रा वाले चित्र ढूँढिए।",
    "vo_oh_i_more_kitaab": "बहुत बढ़िया, किताब! अब और छोटी इ की मात्रा वाले चित्र ढूँढिए।",
    "vo_oh_i_more_chidiya": "बहुत बढ़िया, चिड़िया! अब और छोटी इ की मात्रा वाले चित्र ढूँढिए।",
    "vo_oh_i_more_hiran": "बहुत बढ़िया, हिरण! अब और छोटी इ की मात्रा वाले चित्र ढूँढिए।",
    "vo_oh_ee_more_ladki": "बहुत बढ़िया, लड़की! अब और बड़ी ई की मात्रा वाले चित्र ढूँढिए।",
    "vo_oh_ee_more_paani": "बहुत बढ़िया, पानी! अब और बड़ी ई की मात्रा वाले चित्र ढूँढिए।",
    "vo_oh_ee_more_ghadi": "बहुत बढ़िया, घड़ी! अब और बड़ी ई की मात्रा वाले चित्र ढूँढिए।",
    "vo_oh_ee_more_machhli": "बहुत बढ़िया, मछली! अब और बड़ी ई की मात्रा वाले चित्र ढूँढिए।",

    # Per-distractor correction. A wrong tap must say WHICH matra the word really carries
    # when it carries one of the other two — that names the confusion instead of just
    # denying the answer. कुत्ता and किताब do; पतंग, सूरज and गेंद carry none of the three.
    "vo_oh_w_patang_aa":  "पतंग में आ की मात्रा नहीं है। फिर से कोशिश कीजिए।",
    "vo_oh_w_sooraj_aa":  "सूरज में आ की मात्रा नहीं है। फिर से कोशिश कीजिए।",
    "vo_oh_w_sooraj_i":   "सूरज में छोटी इ की मात्रा नहीं है। फिर से कोशिश कीजिए।",
    "vo_oh_w_gend_i":     "गेंद में छोटी इ की मात्रा नहीं है। फिर से कोशिश कीजिए।",
    "vo_oh_w_kutta":      "कुत्ता में आ की मात्रा है। फिर से कोशिश कीजिए।",
    "vo_oh_w_kitaab_ee":  "किताब में छोटी इ की मात्रा है। फिर से कोशिश कीजिए।",

    # The object names, spoken on hover/focus so the child hears the word before judging it.
    "vo_name_aam":     "यह आम है।",
    "vo_name_maala":   "माला।",
    "vo_name_gaajar":  "गाजर।",
    "vo_name_taala":   "ताला।",
    "vo_name_patang":  "पतंग।",
    "vo_name_sooraj":  "यह सूरज है।",
    "vo_name_chidiya": "यह चिड़िया है।",
    "vo_name_kitaab":  "किताब।",
    "vo_name_kutta":   "कुत्ता।",
    "vo_name_gend":    "गेंद।",
    "vo_name_ladki":   "लड़की।",
    "vo_name_ghadi":   "यह घड़ी है।",
    "vo_name_machhli": "मछली।",

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



# ══════════════════════════════════════════════════════════════════════════════════════════
#  SPEECH SEGMENTS — what the karaoke highlighting needs in order to stay in step.
#
#  karaokePlay spreads a line's words across the clip in proportion to akshara weight, which
#  silently assumes the voice speaks CONTINUOUSLY. It does not. Measured on this lesson's own
#  clips: vo_again_baal runs 1.81s of which only 0.96s is speech - the rest is the pause at its
#  danda. Wall-clock keeps running through a pause while the walk keeps advancing, so the
#  highlight creeps AHEAD of the voice and finishes early. This is the same defect the L01
#  bundle's SME reported as "the highlighting does not sync with the VO".
#
#  So the build measures it. assets.audio_speech carries [[start, end], ...] for every clip that
#  actually pauses, and the engine walks SPEECH-elapsed rather than wall-clock.
#
#  Ported from HI02H11_L01_S01/build_skill_HI02H11_L01_S01.py. The one change is the decoder:
#  that bundle's build-stage clips are WAV under an .ogg name, so it read them with the stdlib.
#  Ours are real Ogg Vorbis, so ffmpeg decodes them.
SPEECH_NOISE_DB = -38.0      # the floor ffmpeg's own silencedetect uses
SPEECH_MIN_SIL  = 0.10       # a gap shorter than this is articulation, not a pause
SPEECH_FRAME    = 0.010


def _clip_pcm(path, rate=16000):
    """16-bit mono PCM at `rate`. (None, 0) means "cannot tell", never a guessed number."""
    import array, subprocess
    try:
        out = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-acodec", "pcm_s16le",
             "-ac", "1", "-ar", str(rate), "-"], capture_output=True, timeout=60)
        if out.returncode != 0 or not out.stdout:
            return None, 0
        a = array.array("h")
        a.frombytes(out.stdout[: len(out.stdout) // 2 * 2])
        return a, rate
    except Exception:
        return None, 0


def _speech_segments(path):
    """[[start, end], ...] seconds where the clip is sounding, plus its duration."""
    import math
    a, rate = _clip_pcm(path)
    if not a or not rate:
        return None, 0.0
    fl = max(1, int(rate * SPEECH_FRAME))
    thr = (10.0 ** (SPEECH_NOISE_DB / 20.0)) * 32768.0
    try:                                   # audioop is C-speed; gone in 3.13, so never required
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            import audioop
        raw = a.tobytes()
        loud = [audioop.rms(raw[i * 2:(i + fl) * 2], 2) >= thr
                for i in range(0, len(a) - fl + 1, fl)]
    except Exception:
        loud = []
        for i in range(0, len(a) - fl + 1, fl):
            acc = 0
            for v in a[i:i + fl]:
                acc += v * v
            loud.append(math.sqrt(acc / fl) >= thr)
    dur = len(a) / float(rate)
    need = int(round(SPEECH_MIN_SIL / SPEECH_FRAME))
    segs, i, n = [], 0, len(loud)
    while i < n:
        if not loud[i]:
            i += 1
            continue
        j = i
        while j < n:
            if loud[j]:
                j += 1
                continue
            k = j
            while k < n and not loud[k]:
                k += 1
            if (k - j) < need and k < n:      # too short to be a pause - keep walking
                j = k
                continue
            break
        segs.append([round(i * SPEECH_FRAME, 3), round(min(dur, j * SPEECH_FRAME), 3)])
        i = j
    return (segs or None), round(dur, 3)


def _measure_speech(audio_ids):
    """(audio_speech, audio_dur) for the card."""
    speech, durs = {}, {}
    for aid in sorted(audio_ids):
        p = os.path.join(OUT, "assets", "Audio",
                         "SFX" if aid.startswith("sfx_") else "VO", aid + ".ogg")
        if not os.path.exists(p):
            continue
        segs, dur = _speech_segments(p)
        if dur:
            durs[aid] = dur
        if not segs:
            continue
        spoken = sum(e - st for st, e in segs)
        # One segment covering essentially the whole clip tells the engine nothing new: the plain
        # proportional walk is already right for those, and carrying them just grows the card.
        if len(segs) == 1 and spoken >= 0.95 * dur:
            continue
        speech[aid] = segs
    return speech, durs



# ══════════════════════════════════════════════════════════════════════════════════════════
#  THE TRANSITION GATE and THE CELEBRATION SWIFTIE
#  Both ported from MTG2A04_L01_S01 (github.com/CodeWithPiyush0/MTG204_L01_S01), whose engine is
#  this same 2026.08.04b-r4-unified lineage. The ART is theirs, used as delivered. The TIMING is
#  measured here from OUR clips, which is the whole point of carrying the generators rather than
#  the numbers: our celebration line is not their celebration line, so their lip-sync track would
#  put the beak on the wrong syllables.

# ══════════════════════════════════════════════════════════════════════════════════════════
#  WHERE A PHRASE FALLS INSIDE A CLIP — ported from HI02H11_L02_S02_DEV_HANDOFF's builder.
#  Pages 1-7 light things ON the words that name them, and a fixed delay cannot do that: our
#  teaching clips run from 1.9s to 7.6s, so any constant is early on one and late on another.
# ══════════════════════════════════════════════════════════════════════════════════════════
def _cue_ms(audio_id, line, phrase):
    """When, inside `line`'s recording, `phrase` starts — in ms.

    There is no forced aligner in this toolchain, so the cue is the clip's REAL duration scaled
    by where the phrase begins in the text. Devanagari is close enough to evenly paced over one
    sentence, and these cues drive a ~1.2s glow — it only has to start inside the right phrase,
    not on the exact sample. Computed from the file on disk, so a re-recorded clip recomputes it.
    """
    path = os.path.join(OUT, "assets", "Audio", "VO", audio_id + ".ogg")
    try:
        with contextlib.closing(wave.open(path)) as w:
            secs = w.getnframes() / float(w.getframerate())
    except Exception:
        return 1300                      # a plausible middle for a ~4s line
    i = line.find(phrase)
    if i < 0:
        return int(secs * 1000 * 0.35)
    # strip spaces on both sides of the split: they are not spoken, and there are more of them in
    # the second half, which would otherwise push the cue late
    before = len(line[:i].replace(" ", ""))
    total = len(line.replace(" ", "")) or 1
    return int(secs * 1000 * (before / float(total)))


def _sound_cues_ms(audio_id, n=3):
    """Where each of the `n` sounds STARTS inside «ज, जा, जाल।» — in ms.

    This clip is not prose, it is three sounds with deliberate silence between them, and that
    silence is measurable — so unlike _cue_ms, which has to estimate from character proportion,
    this reads the ACTUAL onsets. Lighting each part of the equation exactly as its own sound is
    spoken is what makes «ज» / «जा» / «जाल» distinguishable; lighting the whole equation for all
    three says nothing about which is which.

    Returns None when the clip does not resolve into exactly `n` runs — better for the screen to
    fall back to one glow than to flash the wrong element confidently.
    """
    path = os.path.join(OUT, "assets", "Audio", "VO", audio_id + ".ogg")
    try:
        with contextlib.closing(wave.open(path)) as w:
            if w.getsampwidth() != 2 or w.getnchannels() != 1:
                return None
            sr = float(w.getframerate())
            a = array.array("h")
            a.frombytes(w.readframes(w.getnframes()))
    except Exception:
        return None
    if not len(a):
        return None
    hop = max(1, int(sr * 0.01))
    peak = max(1, max(abs(v) for v in a))
    loud = [max(abs(v) for v in a[i:i + hop]) > peak * 0.10
            for i in range(0, len(a) - hop, hop)]
    runs, i, minq = [], 0, int(0.14 / 0.01)      # 140ms of quiet ends a sound (ours are commas,
    while i < len(loud):                          # not dandas, so the gaps are shorter than the
        if loud[i]:                               # sibling's 180ms)
            j, q = i, 0
            while j < len(loud):
                if loud[j]:
                    q = 0
                else:
                    q += 1
                    if q >= minq:
                        break
                j += 1
            runs.append(i)
            i = j
        i += 1
    if len(runs) != n:
        return None
    return [int(r * 10) for r in runs]


def A(**kw):
    """audio block helper"""
    return dict(kw)


SLIDES = [
    # ============ TUTORIAL · 7 screens =======================================================
    {   # Screen 1 · deck page 4
        "id": "T1", "phase": "tutorial", "eis": "enactive", "type": "MATRA_PAIRS",
        "prompt_hi": "",                                   # row #16 "Remove the current heading text"
        "audio": A(prompt="vo_s1_prompt"),
        # [r38] cue_ms is when «इसकी मात्रा है» starts inside each clip. The matra is
        # highlighted THEN rather than when it pops in, so the glow lands on the words that
        # name it — measured per clip, because the three takes are not the same length.
        "data": {"auto": True, "no_heading": True, "pairs": [
            {"letter": "आ", "matra": "ा", "audio": "vo_pair_aa",
             "cue_ms": _cue_ms("vo_pair_aa", VO["vo_pair_aa"], "इसकी")},
            {"letter": "इ", "matra": "ि", "audio": "vo_pair_i",
             "cue_ms": _cue_ms("vo_pair_i", VO["vo_pair_i"], "इसकी")},
            {"letter": "ई", "matra": "ी", "audio": "vo_pair_ee",
             "cue_ms": _cue_ms("vo_pair_ee", VO["vo_pair_ee"], "इसकी")},
        ],
        # the bare matra, spoken on its own, for the phoneme tap
        "phonemes": {"ा": "vo_matra_aa2", "ि": "vo_matra_i", "ी": "vo_matra_ee"}},
    },
    {   # Screen 2 · deck page 5
        "id": "T2", "phase": "tutorial", "eis": "iconic", "type": "MATRA_BUILD",
        "prompt_hi": "",   # deck: "Do not add extra explanatory text"
        "audio": A(prompt="vo_mb_jal_intro", base="vo_mb_jal_base", onset="vo_mb_jal_onset",
                   result="vo_mb_jal_explain", sounds="vo_mb_jal_sounds",
                   explain="vo_mb_jal_explain"),
        "data": {"auto": True,
                 "base_word": "जल", "base_img": "obj_jal", "base_emoji": "💧",
                 "consonant": "ज", "matra": "ा", "syllable": "जा",
                 "result_word": "जाल", "result_img": "obj_jaal", "result_emoji": "🕸️",
                 # [r38] WHERE THE VISUALS BELONG INSIDE EACH LINE, so the screen follows the
                 # voice instead of running ahead of it. Measured off the clips that exist, so a
                 # re-record moves them rather than leaving them stranded.
                 #   onset  «… लगाने पर, X बनता है।»  -> the syllable forms on «बनता»
                 #   result «अब … लगाने पर, जाल बनता है।» -> the whole word lands on «जाल»
                 "travel": "down", "no_heading": True,
                 "syl_ms":   _cue_ms("vo_mb_jal_onset",   VO["vo_mb_jal_onset"],   "बनता"),
                 "join_ms":  _cue_ms("vo_mb_jal_explain", VO["vo_mb_jal_explain"], "जाल"),
                 # «ज, जा, जाल।» - which of the three is being said, at each moment. Read from the
                 # clip's ACTUAL silences, not estimated; None if it does not resolve into three.
                 "sound_ms": _sound_cues_ms("vo_mb_jal_sounds", 3)},
    },
    {   # Screen 3 · deck page 6
        "id": "T3", "phase": "tutorial", "eis": "iconic", "type": "MEET_PAIR",
        "prompt_hi": "",
        "audio": A(prompt="vo_ex_aa_intro"),
        "data": {"auto": True, "no_heading": True, "examples": [
            {"word": "नाक",  "matra": "ा", "img": "obj_naak", "emoji": "👃",
             "audio_line": "vo_ex_naak", "matra_audio": None,
             # «नाक,» the word is already up · «बोलकर देखिए।» the picture arrives
             # · «इसमें … लगी है।» the matra lights. Both offsets measured off the clip.
             "pic_ms":   _cue_ms("vo_ex_naak", VO["vo_ex_naak"], "बोलकर"),
             "matra_ms": _cue_ms("vo_ex_naak", VO["vo_ex_naak"], "इसमें")},
            {"word": "मटका", "matra": "ा", "img": "obj_matka", "emoji": "🏺",
             "audio_line": "vo_ex_matka", "matra_audio": None,
             # «मटका,» the word is already up · «बोलकर देखिए।» the picture arrives
             # · «इसमें … लगी है।» the matra lights. Both offsets measured off the clip.
             "pic_ms":   _cue_ms("vo_ex_matka", VO["vo_ex_matka"], "बोलकर"),
             "matra_ms": _cue_ms("vo_ex_matka", VO["vo_ex_matka"], "इसमें")},
        ]},
    },
    {   # Screen 4 · deck page 7
        "id": "T4", "phase": "tutorial", "eis": "iconic", "type": "MATRA_BUILD",
        "prompt_hi": "",   # deck: "Do not add extra explanatory text"
        "audio": A(prompt="vo_mb_bil_intro", base="vo_mb_bil_base", onset="vo_mb_bil_onset",
                   result="vo_mb_bil_explain", sounds="vo_mb_bil_sounds",
                   explain="vo_mb_bil_explain"),
        "data": {"auto": True,
                 "base_word": "बल", "base_img": "obj_bal", "base_emoji": "💪",
                 "consonant": "ब", "matra": "ि", "syllable": "बि",
                 "result_word": "बिल", "result_img": "obj_bil", "result_emoji": "🕳️",
                 # [r38] WHERE THE VISUALS BELONG INSIDE EACH LINE, so the screen follows the
                 # voice instead of running ahead of it. Measured off the clips that exist, so a
                 # re-record moves them rather than leaving them stranded.
                 #   onset  «… लगाने पर, X बनता है।»  -> the syllable forms on «बनता»
                 #   result «अब … लगाने पर, बिल बनता है।» -> the whole word lands on «बिल»
                 "travel": "down", "no_heading": True,
                 "syl_ms":   _cue_ms("vo_mb_bil_onset",   VO["vo_mb_bil_onset"],   "बनता"),
                 "join_ms":  _cue_ms("vo_mb_bil_explain", VO["vo_mb_bil_explain"], "बिल"),
                 # «ज, जा, जाल।» - which of the three is being said, at each moment. Read from the
                 # clip's ACTUAL silences, not estimated; None if it does not resolve into three.
                 "sound_ms": _sound_cues_ms("vo_mb_bil_sounds", 3)},
    },
    {   # Screen 5 · deck page 8
        "id": "T5", "phase": "tutorial", "eis": "iconic", "type": "MEET_PAIR",
        "prompt_hi": "",
        "audio": A(prompt="vo_ex_i_intro"),
        "data": {"auto": True, "no_heading": True, "examples": [
            {"word": "दिन", "matra": "ि", "img": "obj_din", "emoji": "☀️",
             "audio_line": "vo_ex_din", "matra_audio": None,
             # «दिन,» the word is already up · «बोलकर देखिए।» the picture arrives
             # · «इसमें … लगी है।» the matra lights. Both offsets measured off the clip.
             "pic_ms":   _cue_ms("vo_ex_din", VO["vo_ex_din"], "बोलकर"),
             "matra_ms": _cue_ms("vo_ex_din", VO["vo_ex_din"], "इसमें")},
            {"word": "गति", "matra": "ि", "img": "obj_gati", "emoji": "🏃",
             "audio_line": "vo_ex_gati", "matra_audio": None,
             # «गति,» the word is already up · «बोलकर देखिए।» the picture arrives
             # · «इसमें … लगी है।» the matra lights. Both offsets measured off the clip.
             "pic_ms":   _cue_ms("vo_ex_gati", VO["vo_ex_gati"], "बोलकर"),
             "matra_ms": _cue_ms("vo_ex_gati", VO["vo_ex_gati"], "इसमें")},
        ]},
    },
    {   # Screen 6 · deck page 9
        "id": "T6", "phase": "tutorial", "eis": "iconic", "type": "MATRA_BUILD",
        "prompt_hi": "",   # deck: "Do not add extra explanatory text"
        "audio": A(prompt="vo_mb_keel_intro", base="vo_mb_keel_base", onset="vo_mb_keel_onset",
                   result="vo_mb_keel_explain", sounds="vo_mb_keel_sounds",
                   explain="vo_mb_keel_explain"),
        "data": {"auto": True,
                 "base_word": "कल", "base_img": "obj_kal", "base_emoji": "📅",
                 "consonant": "क", "matra": "ी", "syllable": "की",
                 "result_word": "कील", "result_img": "obj_keel", "result_emoji": "🔩",
                 # [r27 · SME] "the कील is looking slightly bigger, make it 10 percent smaller."
                 # Every result picture shares the same 180x150 box, so all three already render
                 # at the same 170px height - कील's art is a 389x553 spike, so filling that height
                 # makes it read as the biggest object on the page. This trims the cap for this
                 # one picture; the other two are untouched.
                 "result_img_scale": 0.9,
                 # [r38] WHERE THE VISUALS BELONG INSIDE EACH LINE, so the screen follows the
                 # voice instead of running ahead of it. Measured off the clips that exist, so a
                 # re-record moves them rather than leaving them stranded.
                 #   onset  «… लगाने पर, X बनता है।»  -> the syllable forms on «बनता»
                 #   result «अब … लगाने पर, कील बनता है।» -> the whole word lands on «कील»
                 "travel": "down", "no_heading": True,
                 "syl_ms":   _cue_ms("vo_mb_keel_onset",   VO["vo_mb_keel_onset"],   "बनता"),
                 "join_ms":  _cue_ms("vo_mb_keel_explain", VO["vo_mb_keel_explain"], "कील"),
                 # «ज, जा, जाल।» - which of the three is being said, at each moment. Read from the
                 # clip's ACTUAL silences, not estimated; None if it does not resolve into three.
                 "sound_ms": _sound_cues_ms("vo_mb_keel_sounds", 3)},
    },
    {   # Screen 7 · deck page 10
        "id": "T7", "phase": "tutorial", "eis": "iconic", "type": "MEET_PAIR",
        "prompt_hi": "",
        "audio": A(prompt="vo_ex_ee_intro"),
        "data": {"auto": True, "no_heading": True, "examples": [
            {"word": "तीर",   "matra": "ी", "img": "obj_teer", "emoji": "🏹",
             "audio_line": "vo_ex_teer", "matra_audio": None,
             # «तीर,» the word is already up · «बोलकर देखिए।» the picture arrives
             # · «इसमें … लगी है।» the matra lights. Both offsets measured off the clip.
             "pic_ms":   _cue_ms("vo_ex_teer", VO["vo_ex_teer"], "बोलकर"),
             "matra_ms": _cue_ms("vo_ex_teer", VO["vo_ex_teer"], "इसमें")},
            {"word": "लड़की", "matra": "ी", "img": "obj_ladki", "emoji": "👧",
             "audio_line": "vo_ex_ladki", "matra_audio": None,
             # «लड़की,» the word is already up · «बोलकर देखिए।» the picture arrives
             # · «इसमें … लगी है।» the matra lights. Both offsets measured off the clip.
             "pic_ms":   _cue_ms("vo_ex_ladki", VO["vo_ex_ladki"], "बोलकर"),
             "matra_ms": _cue_ms("vo_ex_ladki", VO["vo_ex_ladki"], "इसमें")},
        ]},
    },

    # ============ GUIDED · 4 screens =========================================================
    {   # Screen 8 · deck page 11
        "id": "G1", "phase": "guided", "eis": "iconic", "type": "TRAIN_TAP",
        # [r8] The spoken line is written on screen in the question band on every question page
        # (8-14). This supersedes row #96 "No instruction text on screen" for these screens.
        "prompt_hi": "“आ” की मात्रा वाले शब्द पर टैप कीजिए।",
        "audio": A(prompt="vo_tt_aa_prompt", correct="vo_tt_aa_correct",
                   hint1="vo_tt_aa_hint1", hint2="vo_tt_aa_hint2", hint3="vo_tt_aa_hint3",
                   reveal="vo_rev_tt_aa", try_again="vo_tt_aa_hint1"),
        "data": {"signal": "matra_tap_first_try", "options": [
            {"word_hi": "हाथ", "matra": "ा", "audio": "vo_name_haath", "correct": True},
            {"word_hi": "दिन", "matra": "ि", "audio": "vo_name_din"},
            {"word_hi": "नीम", "matra": "ी", "audio": "vo_name_neem"},
        ]},
        "signals": {"on_complete": ["matra_tap_first_try"]},
    },
    {   # Screen 9 · deck page 12
        "id": "G2", "phase": "guided", "eis": "iconic", "type": "TRAIN_TAP",
        "prompt_hi": "“इ” की मात्रा वाले शब्द पर टैप कीजिए।",
        "audio": A(prompt="vo_tt_i_prompt", correct="vo_tt_i_correct",
                   hint1="vo_tt_i_hint1", hint2="vo_tt_i_hint2", hint3="vo_tt_i_hint3",
                   reveal="vo_rev_tt_i", try_again="vo_tt_i_hint1"),
        "data": {"signal": "matra_tap_first_try", "options": [
            {"word_hi": "पिन", "matra": "ि", "audio": "vo_name_pin", "correct": True},
            {"word_hi": "नाक", "matra": "ा", "audio": "vo_name_naak"},
            {"word_hi": "तीर", "matra": "ी", "audio": "vo_name_teer"},
        ]},
        "signals": {"on_complete": ["matra_tap_first_try"]},
    },
    {   # Screen 10 · deck page 13
        "id": "G3", "phase": "guided", "eis": "iconic", "type": "TRAIN_TAP",
        "prompt_hi": "“ई” की मात्रा वाले शब्द पर टैप कीजिए।",
        "audio": A(prompt="vo_tt_ee_prompt", correct="vo_tt_ee_correct",
                   hint1="vo_tt_ee_hint1", hint2="vo_tt_ee_hint2", hint3="vo_tt_ee_hint3",
                   reveal="vo_rev_tt_ee", try_again="vo_tt_ee_hint1"),
        "data": {"signal": "matra_tap_first_try", "options": [
            {"word_hi": "पानी", "matra": "ी", "audio": "vo_name_paani", "correct": True},
            {"word_hi": "नाक", "matra": "ा",  "audio": "vo_name_naak"},
            {"word_hi": "दिन", "matra": "ि",  "audio": "vo_name_din"},
        ]},
        "signals": {"on_complete": ["matra_tap_first_try"]},
    },
    {   # Screen 11 · [r29 · SME] THE DRAG, DEMONSTRATED. "we will teach how to drag element to
        # the drop zone; in this page we are not allowing user to do anything, we will show it
        # with animation, and here only two options will be there."
        #
        # It sits BEFORE G4, not after it. Pages 8-10 are all TAP; this is the first screen in
        # the lesson that asks for a DRAG, and a demonstration a child watches after they have
        # already had to do the thing teaches nothing. The screen it demonstrates follows
        # immediately, with the same train, the same coaches and the same landing.
        #
        # TWO cards and TWO coaches, not three: the deck asks for two options, and a third empty
        # coach left over at the end would read as something the demo forgot to do. आ and इ are
        # the two matras taught first, and both words are already known from earlier screens.
        "id": "G4D", "phase": "guided", "eis": "enactive", "type": "TRAIN_SORT",
        "prompt_hi": "देखिए, शब्द को उसकी सही मात्रा वाले डिब्बे में इस तरह ले जाते हैं।",
        "audio": A(prompt="vo_ts0_prompt"),
        "data": {"demo": True,          # watch only: no drag handlers, nothing scored
                 "bins": [{"key": "aa", "label": "“आ” (ा)"},
                          {"key": "i",  "label": "“इ” (ि)"}],
                 "items": [
                     {"key": "aa", "word_hi": "हाथ", "img": "obj_haath", "emoji": "✋",
                      "audio": "vo_name_haath", "correct_audio": "vo_ts1_ok_haath"},
                     {"key": "i",  "word_hi": "पिन", "img": "obj_pin", "emoji": "📌",
                      "audio": "vo_name_pin", "correct_audio": "vo_ts1_ok_pin"},
                 ]},
        "signals": {"on_complete": []},
    },
    {   # Screen 12 · deck page 14 — word cards into matra coaches
        "id": "G4", "phase": "guided", "eis": "enactive", "type": "TRAIN_SORT",
        "prompt_hi": "हर शब्द को उसकी सही मात्रा वाले डिब्बे में डालिए।",
        "audio": A(prompt="vo_ts1_prompt", hint1="vo_ts1_hint1", hint2="vo_ts1_hint2",
                   try_again="vo_ts1_hint1"),
        "data": {"signal": "matra_sort_correct",
                 "bins": [{"key": "aa", "label": "“आ” (ा)", "label_audio": "vo_letter_aa"}, {"key": "i", "label": "“इ” (ि)", "label_audio": "vo_letter_i"},
                          {"key": "ee", "label": "“ई” (ी)", "label_audio": "vo_letter_ee"}],
                 "items": [
                     {"key": "aa", "word_hi": "हाथ", "img": "obj_haath", "emoji": "✋",
                      "audio": "vo_name_haath", "correct_audio": "vo_ts1_ok_haath", "matra": "ा", "hint2_audio": "vo_ts1_h2_haath", "hint3_audio": "vo_ts1_h3_haath"},
                     {"key": "i",  "word_hi": "पिन", "img": "obj_pin", "emoji": "📌",
                      "audio": "vo_name_pin", "correct_audio": "vo_ts1_ok_pin", "matra": "ि", "hint2_audio": "vo_ts1_h2_pin", "hint3_audio": "vo_ts1_h3_pin"},
                     {"key": "ee", "word_hi": "नीम", "img": "obj_neem", "emoji": "🌳",
                      "audio": "vo_name_neem", "correct_audio": "vo_ts1_ok_neem", "matra": "ी", "hint2_audio": "vo_ts1_h2_neem", "hint3_audio": "vo_ts1_h3_neem"},
                 ]},
        "signals": {"on_complete": ["matra_sort_correct"]},
    },

    # ============ PRACTICE · 5 screens =======================================================
    {   # Screen 12 · deck page 15 — the REVERSE mapping: matra cards into word coaches
        "id": "P1", "phase": "practice", "eis": "enactive", "type": "TRAIN_SORT",
        "prompt_hi": "सही मात्रा को सही शब्द वाले डिब्बे में डालिए।",
        "audio": A(prompt="vo_ts2_prompt", hint1="vo_ts2_hint1", hint2="vo_ts2_hint2",
                   try_again="vo_ts2_hint1"),
        "data": {"signal": "matra_sort_correct",
                 "bins": [{"key": "aa", "label": "जाल", "label_audio": "vo_name_jaal"}, {"key": "i", "label": "सिर", "label_audio": "vo_name_sir"},
                          {"key": "ee", "label": "कील", "label_audio": "vo_name_keel"}],
                 "items": [
                     {"key": "aa", "glyph": "ा", "correct_audio": "vo_ts2_ok_jaal", "audio": "vo_letter_aa", "hint2_audio": "vo_ts2_h2_aa", "hint3_audio": "vo_ts2_h3_aa"},
                     {"key": "i",  "glyph": "ि", "correct_audio": "vo_ts2_ok_sir", "audio": "vo_letter_i", "hint2_audio": "vo_ts2_h2_i", "hint3_audio": "vo_ts2_h3_i"},
                     {"key": "ee", "glyph": "ी", "correct_audio": "vo_ts2_ok_keel", "audio": "vo_letter_ee", "hint2_audio": "vo_ts2_h2_ee", "hint3_audio": "vo_ts2_h3_ee"},
                 ]},
        "signals": {"on_complete": ["matra_sort_correct"]},
    },
    {   # Screen 13 · deck page 16 — fill the blank.
        # `blank_at` is an index into the CONSONANT-GROUP sequence, never a character offset:
        # in हिरण the ि is stored after ह but DRAWN before it, so the blank sits at index 0.
        # हीरा was CORRECTED to हिरण on the SME's explicit instruction (row #149) — हीरा is
        # unusable anyway, it carries two in-scope matras (ी and ा).
        "id": "P2", "phase": "practice", "eis": "enactive", "type": "MATRA_FILL",
        "prompt_hi": "मात्रा को सही डिब्बे में डालकर शब्द पूरा कीजिए।",
        "audio": A(prompt="vo_mf_prompt", hint1="vo_mf_hint1", hint2="vo_mf_hint2", hint3="vo_mf_hint3",
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
        "prompt_hi": "चित्र देखकर उसे सही मात्रा वाले डिब्बे में डालिए।",
        "audio": A(prompt="vo_ts3_prompt", hint1="vo_ts3_hint1", hint2="vo_ts3_hint2",
                   try_again="vo_ts3_hint1"),
        # [r29 · SME] "after the train comes and the instructions are complete, each option will
        # come and display on the screen one by one, taking the name of each element." The cards
        # are pictures with no labels here, so hearing each name AS it lands is the only way the
        # child learns what they are being asked to sort. It waits for the instruction to finish,
        # not for a timer off the train's arrival, or the names talk over it.
        # (Shuffling was already in: the tray is Fisher-Yates'd on every mount.)
        "data": {"signal": "matra_sort_correct", "hide_labels": True, "multi": True,
                 "announce_items": True,
                 "bins": [{"key": "aa", "label": "“आ” (ा)"}, {"key": "i", "label": "“इ” (ि)"},
                          {"key": "ee", "label": "“ई” (ी)"}],
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
    # ---- Screens 15-17 · OBJECT_HUNT (deck slides 18, 19, 20) --------------------------------
    # The deck retires the poem: "Convert this activity into an interactive object hunt."
    # Three screens, one per matra, each a hotspot layer over the delivered scene.
    #
    # EVERY DISTRACTOR IS AUDITED AGAINST THE TARGET. Two earlier ones were wrong and are gone:
    # कुत्ता ends in ा, so on the आ screen a child who tapped the dog was RIGHT and was buzzed;
    # तितली ends in ी, the same fault on the ई screen. A distractor must not contain the matra
    # being hunted — otherwise the screen teaches the opposite of what it is for.
    #
    # x/y/w/h are percentages of the scene, each one placed by cropping it out of the artwork AND
    # out of the rendered page, and looking at it.
    {   # Screen 15 · deck slide 18 — आ की मात्रा
        "id": "P4", "phase": "practice", "eis": "symbolic", "type": "OBJECT_HUNT",
        "prompt_hi": "“आ” की मात्रा वाले चित्र खोजिए और उन पर टैप कीजिए।",
        "audio": A(prompt="vo_oh_aa_intro", result="vo_oh_aa_done",
                   try_again="vo_oh_aa_wrong", hint1="vo_oh_hint1", hint2="vo_oh_aa_hint2"),
        "data": {"signal": "object_hunt_correct", "letter": "आ", "matra": "ा",
                 "scene": "assets/UI/scene_hunt1.webp",
                 "objects": [
                   {"word_hi": "आम", "audio": "vo_name_aam", "emoji": "🥭",
                    "ok_audio": "vo_oh_aa_ok_aam", "more_audio": "vo_oh_aa_more_aam",
                    "correct": True, "x": 19.1, "y": 18.6, "w": 21.5, "h": 19.1},
                   {"word_hi": "माला", "audio": "vo_name_maala", "emoji": "📿",
                    "ok_audio": "vo_oh_aa_ok_maala", "more_audio": "vo_oh_aa_more_maala",
                    "correct": True, "x": 66.7, "y": 65.9, "w": 9.5, "h": 10.0},
                   {"word_hi": "गाजर", "audio": "vo_name_gaajar", "emoji": "🥕",
                    "ok_audio": "vo_oh_aa_ok_gaajar", "more_audio": "vo_oh_aa_more_gaajar",
                    "correct": True, "x": 45.8, "y": 82.4, "w": 20.9, "h": 15.9},
                   {"word_hi": "ताला", "audio": "vo_name_taala", "emoji": "🔒",
                    "ok_audio": "vo_oh_aa_ok_taala", "more_audio": "vo_oh_aa_more_taala",
                    "correct": True, "x": 94.0, "y": 51.0, "w": 5.0, "h": 11.0},
                   # distractors — neither carries ा
                   {"word_hi": "पतंग", "audio": "vo_name_patang", "emoji": "🪁",
                    "wrong_audio": "vo_oh_w_patang_aa", "x": 36.9, "y": 28.7, "w": 10.5, "h": 15.9},
                   {"word_hi": "सूरज", "audio": "vo_name_sooraj", "emoji": "☀️",
                    "wrong_audio": "vo_oh_w_sooraj_aa", "x": 72.5, "y": 10.8, "w": 9.9, "h": 19.7},
                 ]},
        "signals": {"on_complete": ["object_hunt_correct"]},
    },
    {   # Screen 16 · deck slide 19 — छोटी इ की मात्रा
        "id": "P5", "phase": "practice", "eis": "symbolic", "type": "OBJECT_HUNT",
        "prompt_hi": "छोटी “इ” की मात्रा वाले चित्र खोजिए और उन पर टैप कीजिए।",
        "audio": A(prompt="vo_oh_i_intro", result="vo_oh_i_done",
                   try_again="vo_oh_i_wrong", hint1="vo_oh_hint1", hint2="vo_oh_i_hint2"),
        "data": {"signal": "object_hunt_correct", "letter": "इ", "matra": "ि",
                 "scene": "assets/UI/scene_hunt2.webp",
                 "objects": [
                   {"word_hi": "चिड़िया", "audio": "vo_name_chidiya", "emoji": "🐦",
                    "ok_audio": "vo_oh_i_ok_chidiya", "more_audio": "vo_oh_i_more_chidiya",
                    "correct": True, "x": 44.7, "y": 22.3, "w": 8.1, "h": 13.2},
                   {"word_hi": "हिरण", "audio": "vo_name_hiran", "emoji": "🦌",
                    "ok_audio": "vo_oh_i_ok_hiran", "more_audio": "vo_oh_i_more_hiran",
                    "correct": True, "x": 69.7, "y": 51.8, "w": 10.2, "h": 26.6},
                   {"word_hi": "किताब", "audio": "vo_name_kitaab", "emoji": "📕",
                    "ok_audio": "vo_oh_i_ok_kitaab", "more_audio": "vo_oh_i_more_kitaab",
                    "correct": True, "x": 21.2, "y": 65.8, "w": 12.0, "h": 14.0},
                   {"word_hi": "पिन", "audio": "vo_name_pin", "emoji": "📌",
                    "ok_audio": "vo_oh_i_ok_pin", "more_audio": "vo_oh_i_more_pin",
                    "correct": True, "x": 50.3, "y": 84.3, "w": 6.0, "h": 9.0},
                   # distractors — none carries ि. कुत्ता carries ा, which its line says.
                   {"word_hi": "कुत्ता", "audio": "vo_name_kutta", "emoji": "🐶",
                    "wrong_audio": "vo_oh_w_kutta", "x": 46.1, "y": 63.0, "w": 11.0, "h": 15.9},
                   {"word_hi": "गेंद", "audio": "vo_name_gend", "emoji": "⚽",
                    "wrong_audio": "vo_oh_w_gend_i", "x": 37.1, "y": 66.4, "w": 6.2, "h": 10.0},
                   {"word_hi": "सूरज", "audio": "vo_name_sooraj", "emoji": "☀️",
                    "wrong_audio": "vo_oh_w_sooraj_i", "x": 77.6, "y": 10.9, "w": 11.1, "h": 18.1},
                 ]},
        "signals": {"on_complete": ["object_hunt_correct"]},
    },
    {   # Screen 17 · deck slide 20 — बड़ी ई की मात्रा
        "id": "P6", "phase": "practice", "eis": "symbolic", "type": "OBJECT_HUNT",
        "prompt_hi": "बड़ी “ई” की मात्रा वाले चित्र खोजिए और उन पर टैप कीजिए।",
        "audio": A(prompt="vo_oh_ee_intro", result="vo_oh_ee_done",
                   try_again="vo_oh_ee_wrong", hint1="vo_oh_hint1", hint2="vo_oh_ee_hint2"),
        "data": {"signal": "object_hunt_correct", "letter": "ई", "matra": "ी",
                 "scene": "assets/UI/scene_hunt3.webp",
                 "objects": [
                   {"word_hi": "लड़की", "audio": "vo_name_ladki", "emoji": "👧",
                    "ok_audio": "vo_oh_ee_ok_ladki", "more_audio": "vo_oh_ee_more_ladki",
                    "correct": True, "x": 53.8, "y": 30.0, "w": 12.0, "h": 16.5},
                   {"word_hi": "पानी", "audio": "vo_name_paani", "emoji": "💧",
                    "ok_audio": "vo_oh_ee_ok_paani", "more_audio": "vo_oh_ee_more_paani",
                    "correct": True, "x": 51.1, "y": 44.0, "w": 5.5, "h": 11.0},
                   {"word_hi": "घड़ी", "audio": "vo_name_ghadi", "emoji": "🕐",
                    "ok_audio": "vo_oh_ee_ok_ghadi", "more_audio": "vo_oh_ee_more_ghadi",
                    "correct": True, "x": 80.9, "y": 65.4, "w": 7.2, "h": 18.5},
                   {"word_hi": "मछली", "audio": "vo_name_machhli", "emoji": "🐟",
                    "ok_audio": "vo_oh_ee_ok_machhli", "more_audio": "vo_oh_ee_more_machhli",
                    "correct": True, "x": 8.2, "y": 73.3, "w": 10.2, "h": 8.9},
                   # distractors — neither carries ी. तितली was removed: it ends in ी.
                   {"word_hi": "कुत्ता", "audio": "vo_name_kutta", "emoji": "🐶",
                    "wrong_audio": "vo_oh_w_kutta", "x": 36.2, "y": 61.4, "w": 10.4, "h": 19.1},
                   {"word_hi": "किताब", "audio": "vo_name_kitaab", "emoji": "📕",
                    "wrong_audio": "vo_oh_w_kitaab_ee", "x": 65.4, "y": 70.2, "w": 12.7, "h": 8.3},
                 ]},
        "signals": {"on_complete": ["object_hunt_correct"]},
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
    # [r24 · SME] The coaches NAME the letter and bracket its matra, the same shape the
    # TRAIN_SORT bins already use ("“आ” (ा)"). A bare ा/ि/ी is an orphan combining mark, so the
    # font drew it with a dotted placeholder circle and the cover asked a child to read ◌ा.
    # Order stays आ → इ → ई, which is the order every other screen in the lesson teaches in.
    # [r33] The sibling's cover (HI02H11_L02_S02) renders the coach itself as «letter (matra)»,
    # so the two halves travel separately now: `matras` is the bare mark, which its matraGlyph()
    # draws, and `letters` is what is said in front of it. The r24 inverted commas stay - that was
    # this lesson's own call, and the sibling's own comment says this form exists so the cover
    # names the pair exactly as the sorting screens later will.
    "landing_hero": {"kind": "matra_train",
                     "matras":  ["ा", "ि", "ी"],
                     "letters": ["“आ”", "“इ”", "“ई”"]},
    "phase_transition_audio": {"tutorial": "vo_pt_tutorial", "guided": "vo_pt_guided",
                               "practice": "vo_pt_practice"},
    # the journey beats are a LOCKED house behaviour — preserved verbatim from the shipped card
    "phase_transition_title": {"tutorial": "चलो, शुरू करें!", "guided": "साथ में करें।",
                               "practice": "अब तुम्हारी बारी।"},
    "phase_distribution": {"tutorial": 7, "guided": 5, "practice": 5},   # [r29] + the drag demo
    # ---- deck row X1: the SME's 3-attempt ladder --------------------------------------------
    # rung 1 = hint VO, explicitly NO hand · rung 2 = hint VO + the hand on the CORRECT target,
    # child still answers · 3rd-attempt correct = visual celebration, SILENT.
    # `hand_in_practice` is the deck-scoped opt-in past the engine's round-3 hand ban — FLAGGED
    # in CHANGES.md for a ruling, never silently applied fleet-wide.
    "scaffold_rules": {
        "nudge_timeout_ms": {"guided": 6000, "practice": 8000},
        "max_attempts": 3,
        "hand_on_attempt": 2,
        # [r37] THE REVIEW-1 LADDER, from HI02H11_L02_S02_DEV_HANDOFF. Three rungs of three
        # different KINDS of help rather than two of the same kind:
        #   1 refocus     - the wrong thing shakes, one line is spoken, nothing is marked
        #   2 demonstrate - the screen reads the choices out, lighting each word's own matra
        #   3 guide       - the answer is named, it glows, the hand goes to it, the rest lock
        # Drop hint_levels and every module falls back to the two rungs it shipped with, so this
        # engine stays usable by a card that has not been re-authored.
        "hint_levels": 3,
        # the hand at rung 3 reaches PRACTICE screens, which ruling [28f] otherwise bans. The
        # rule is not edited - the engine widens the phase set around that one synchronous call
        # and restores it (see withHand3). Set this false and [28f] applies exactly as before.
        "hand_on_hint3": True,
        "silent_on_late_correct": True,
        "hand_in_practice": True,
    },
    "signals_expected": ["slide_entered", "slide_completed", "matra_tap_first_try",
                         "matra_sort_correct", "matra_fill_correct", "poem_search_correct",
                         "lesson_completed", "mastery_score"],
    "_emoji_fallback": dict(IMAGES),
    "slides": SLIDES,
}


def gate_spec():
    """peek once -> talk while the gate VO sounds -> rest, from the moment it ends.

    peek_ms is read off the file rather than guessed, so the talk starts on her last rising frame.
    Falls back to the engine's own stock gate if the art is not on disk.
    """
    peek = os.path.join(OUT, "assets", "UI", "gate_peek.webp")
    if not os.path.isfile(peek):
        return None
    try:
        from PIL import Image, ImageSequence
        ms = sum((f.info.get("duration") or 40) for f in ImageSequence.Iterator(Image.open(peek)))
    except Exception:
        ms = 1520
    return {"img": "assets/UI/gate_peek.webp", "peek": "assets/UI/gate_peek.webp",
            "talk": "assets/UI/gate_talk.webp", "rest": "assets/UI/gate_rest.webp",
            "peek_ms": ms, "hold_ms": 450}


def cel_anim():
    """The lip-sync track for OUR celebration line, plus the sprite facts.

    One character per 25ms of vo_cel_prompt: '1' on a syllable beat (beak open), '0' between them.
    Not merely "voice on" - the mouth opens where the clip is loud AND near its own local peak, so
    it opens on each syllable nucleus and shuts in the dips, which is what stops her looking like
    she is humming through a whole word. Re-measured every build, so a re-recorded line re-syncs.
    """
    meta_p = os.path.join(OUT, "_cel_sprite.json")
    clip = os.path.join(OUT, "assets", "Audio", "VO", "vo_cel_prompt.ogg")
    if not (os.path.isfile(meta_p) and os.path.isfile(clip)):
        return None
    import array, math, subprocess
    with open(meta_p, encoding="utf-8") as _f:
        meta = json.load(_f)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", clip, "-ac", "1", "-ar", "16000",
                          "-f", "s16le", "-"], capture_output=True).stdout
    if not raw:
        return None
    a = array.array("h")
    a.frombytes(raw[: len(raw) // 2 * 2])
    step = 400                                                   # 25 ms at 16 kHz
    rms = [math.sqrt(sum(x * x for x in a[i:i + step]) / step) for i in range(0, len(a) - step, step)]
    if not rms:
        return None
    mx = max(rms) or 1
    W = 4
    bits = ["1" if (r > 0.10 * mx and r >= 0.62 * max(rms[max(0, i - W):i + W + 1])) else "0"
            for i, r in enumerate(rms)]
    t = "".join(bits)
    t = t.replace("101", "111").replace("101", "111")            # a 25ms close inside a syllable = flicker
    t = t.replace("010", "000")                                  # a lone 25ms open = flicker
    sh = meta["sheets"]
    return {"cols": meta["cols"], "fw": meta["fw"], "fh": meta["fh"], "step_ms": 25, "bits": t,
            "vo": "vo_cel_prompt",
            "shabaash": {"src": sh["shabaash"]["src"], "pre": list(range(0, 6)),    # standing, shut
                         "word": list(range(6, 30)),                                 # the jump
                         "post": list(range(30, 36))},                               # lands, shut
            "talk": {"src": sh["talk"]["src"], "open": sh["talk"]["open"]},
            "idle": {"src": sh["idle"]["src"],
                     "loop": [0, 1, 2, 3, 4] + list(range(24, 36))}}                 # shut frames only


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
                                                 # [r37] the Review-1 ladder's third rung, and the
                                                 # per-item rung-2/rung-3 ids the drag screens carry
                                                 # (a word's own "ध्यान से सुनिए, पिन…" line). Without
                                                 # these the walker silently drops them: the card still
                                                 # points at the id, audio_text has no entry for it, and
                                                 # the child hears nothing on that rung.
                                                 "hint3", "hint", "hint2_audio", "hint3_audio",
                                                 "label_audio",
                                                 # [r38] MEET_PAIR names its clip `audio_line`, not
                                                 # `audio`. Without this the six example clips fell
                                                 # out of used_audio entirely: they still PLAYED
                                                 # (the module builds the path itself) but carried
                                                 # no duration, no preload and no karaoke timing,
                                                 # and PENDING VO stopped checking them.
                                                 "audio_line", "matra_audio",
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

    # [r31] the ported gate + celebration, both measured from this lesson's own files
    _gate = gate_spec()
    if _gate:
        CARD["gate"] = _gate
    _cel = cel_anim()
    if _cel:
        CARD["end_anim"] = _cel

    # [r30] karaoke timing. Measured from the clips on disk every build, so a re-recorded line
    # cannot leave the highlighting walking to the old one's rhythm.
    _speech, _dur = _measure_speech(used_audio)
    if _speech:
        CARD["assets"]["audio_speech"] = _speech
    if _dur:
        CARD["assets"]["audio_dur"] = _dur

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
    _g = CARD.get("gate"); _c = CARD.get("end_anim")
    print(f"  gate: {'peek/talk/rest, peek ' + str(_g['peek_ms']) + 'ms' if _g else 'stock (art missing)'}")
    print(f"  celebration: {'lip-sync ' + str(len(_c['bits'])) + ' steps x 25ms' if _c else 'stock mascot'}")
    _sp = CARD["assets"].get("audio_speech", {})
    print(f"  karaoke timing: {len(CARD['assets'].get('audio_dur', {}))} clips measured, "
          f"{len(_sp)} carry pauses")
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
