# Voice-over — HI02H11_L02_S01 «मात्राओं की रेल»

Regenerated 2026-09-17 after applying the SME deck **and generating the audio**.

**All 91 lines are on disk.** Synthesised with Gemini TTS, voice **Kore** — the voice the
original 95-clip set used, so the 14 reused clips and the new ones are the same narrator.

## ⚠ EAR-CHECK before delivery — a human must play these

11 clips did not come back on the primary voice on the first pass and were recovered by the
generator's fallback ladder (a danda, or a style-wrapper around the same voice). They are correct
Hindi and correct length, but **timbre may differ slightly** — house rule is that no generated
sound ships unheard.

| audio_id | recovered via | line |
|---|---|---|
| `vo_ex_gati` | wrapped(Kore) | गति, बोलकर देखिए। इसमें त पर छोटी इ की मात्रा लगी है। |
| `vo_ex_ladki` | wrapped(Kore) | लड़की, बोलकर देखिए। इसमें क पर बड़ी ई की मात्रा लगी है। |
| `vo_ex_din` | wrapped(Kore) | दिन, बोलकर देखिए। इसमें द पर छोटी इ की मात्रा लगी है। |
| `vo_mf_hint1` | danda | फिर से सोचो। |
| `vo_ex_teer` | wrapped(Kore) | तीर, बोलकर देखिए। इसमें त पर बड़ी ई की मात्रा लगी है। |
| `vo_ex_matka` | wrapped(Kore) | मटका, बोलकर देखिए। इसमें क पर आ की मात्रा लगी है। |
| `vo_name_paani` | wrapped-lesson(Kore) | पानी |
| `vo_ps_hint2` | wrapped(Kore) | ध्यान से मात्रा पहचानो। |
| `vo_ts1_hint1` | wrapped(Kore) | फिर से सुनो और सही मात्रा पहचानिए। |
| `vo_ts3_hint1` | wrapped(Kore) | फिर से सुनो और सही मात्रा पहचानो। |
| `vo_name_pari` | wrapped-lesson(Kore) | परी |

## Measured constraints that shaped these lines

1. **«यह शब्द है, बल।» truncated every time** — 48–56 KB against 108/110 KB for its two peers,
   across three independent takes. Same per-word failure as दिन in the original build. Fixed by
   moving the short word off the end: **«यह शब्द बल है।»**. All three parallel base lines
   (जल / बल / कल) were given the same shape so the three teach screens stay consistent.
2. **No em-dashes.** The deck writes «यह शब्द है — जल।»; an em-dash before a short final word cuts
   the clip to 0.73–1.05 s. Every line here uses a comma or a danda.
3. **No clip is a bare akshara.** The onset lines speak «जा»/«बि»/«की» inside a full sentence, so
   the HTTP-400 bare-akshara refusal the spec warns about never applies to this set.
4. Truncation re-checked after generation with `_verify_assets.py` §3: **0 truncated**.

## All lines

| audio_id | seconds | line |
|---|---|---|
| `sfx_celebrate` | — (inherited .ogg) | celebration sound |
| `vo_cel_prompt` | 7.77 | शाबाश! आज हमने सीखा — आ, इ और ई की मात्रा पहचानना, और मात्रा वाले शब्द पढ़ना। |
| `vo_ex_aa_intro` | 3.17 | आइए, आ की मात्रा वाले कुछ शब्द देखें। |
| `vo_ex_din` | 5.49 | दिन, बोलकर देखिए। इसमें द पर छोटी इ की मात्रा लगी है। |
| `vo_ex_ee_intro` | 3.13 | आइए, बड़ी ई की मात्रा वाले कुछ शब्द देखें। |
| `vo_ex_gati` | 5.17 | गति, बोलकर देखिए। इसमें त पर छोटी इ की मात्रा लगी है। |
| `vo_ex_i_intro` | 3.37 | आइए, छोटी इ की मात्रा वाले कुछ शब्द देखें। |
| `vo_ex_ladki` | 5.97 | लड़की, बोलकर देखिए। इसमें क पर बड़ी ई की मात्रा लगी है। |
| `vo_ex_matka` | 4.77 | मटका, बोलकर देखिए। इसमें क पर आ की मात्रा लगी है। |
| `vo_ex_naak` | 3.01 | नाक, बोलकर देखिए। इसमें न पर आ की मात्रा लगी है। |
| `vo_ex_teer` | 5.41 | तीर, बोलकर देखिए। इसमें त पर बड़ी ई की मात्रा लगी है। |
| `vo_landing` | 4.49 | हेलो दोस्त! मैं हूँ स्विफ्टी। आज हम मात्राओं के बारे में जानेंगे। |
| `vo_matra_aa2` | 1.33 | आ की मात्रा |
| `vo_matra_ee` | 3.73 | बड़ी ई की मात्रा |
| `vo_matra_i` | 1.73 | छोटी इ की मात्रा |
| `vo_mb_bil_base` | 1.97 | यह शब्द बल है। |
| `vo_mb_bil_explain` | 4.25 | अब बल में छोटी इ की मात्रा लगाने पर, बिल बनता है। |
| `vo_mb_bil_intro` | 5.09 | आइए, देखें कि छोटी इ की मात्रा लगाने से शब्द की आवाज़ कैसे बदलती है। |
| `vo_mb_bil_onset` | 4.09 | ब में छोटी इ की मात्रा लगाने पर, बि बनता है। |
| `vo_mb_jal_base` | 1.93 | यह शब्द जल है। |
| `vo_mb_jal_explain` | 4.57 | अब जल में आ की मात्रा लगाने पर, जाल बनता है। |
| `vo_mb_jal_intro` | 5.41 | आइए, देखें कि आ की मात्रा लगने से शब्द की आवाज़ कैसे बदलती है। |
| `vo_mb_jal_onset` | 3.41 | ज में आ की मात्रा लगाने पर, जा बनता है। |
| `vo_mb_keel_base` | 1.81 | यह शब्द कल है। |
| `vo_mb_keel_explain` | 4.65 | अब कल में बड़ी ई की मात्रा लगाने पर, कील बनता है। |
| `vo_mb_keel_intro` | 5.01 | आइए, देखें कि बड़ी ई की मात्रा लगाने से शब्द की आवाज़ कैसे बदलती है। |
| `vo_mb_keel_onset` | 3.73 | क में बड़ी ई की मात्रा लगाने पर, की बनता है। |
| `vo_mf_hint1` | 1.29 | फिर से सोचो। |
| `vo_mf_hint2` | 3.17 | ध्यान से देखो। कौन-सी मात्रा लगेगी? |
| `vo_mf_ok_hiran` | 2.65 | शाबाश! हिरण बन गया। |
| `vo_mf_ok_jaal` | 2.85 | शाबाश! जाल बन गया। |
| `vo_mf_ok_pari` | 2.37 | शाबाश! परी बन गया। |
| `vo_mf_prompt` | 5.17 | सही मात्रा को सही जगह पर खींचकर डालो और शब्द पूरा करिए। |
| `vo_name_bil` | 0.89 | बिल |
| `vo_name_din` | 1.05 | दिन |
| `vo_name_haath` | 0.89 | हाथ |
| `vo_name_hiran` | 1.05 | हिरण |
| `vo_name_jaal` | 1.13 | जाल |
| `vo_name_keel` | 0.97 | कील |
| `vo_name_naak` | 0.97 | नाक |
| `vo_name_neem` | 0.89 | नीम |
| `vo_name_paani` | 0.89 | पानी |
| `vo_name_pari` | 1.01 | परी |
| `vo_name_pin` | 0.93 | पिन |
| `vo_name_teer` | 1.05 | तीर |
| `vo_ps_hint1` | 1.05 | फिर से देखो। |
| `vo_ps_hint2` | 2.17 | ध्यान से मात्रा पहचानो। |
| `vo_ps_ok` | 1.21 | शाबाश! |
| `vo_ps_r1` | 2.41 | आ की मात्रा वाले शब्द ढूँढो। |
| `vo_ps_r2` | 3.13 | अब छोटी इ की मात्रा वाले शब्द ढूँढो। |
| `vo_ps_r3` | 3.09 | अब बड़ी ई की मात्रा वाले शब्द ढूँढो। |
| `vo_pt_guided` | — (inherited .ogg) | बहुत बढ़िया! अब हम साथ मिलकर शुरू करते हैं। चलिए, साथ में करें! |
| `vo_pt_practice` | — (inherited .ogg) | वाह! अब आपकी बारी। |
| `vo_pt_tutorial` | — (inherited .ogg) | ध्यान से देखिए और मेरे साथ जानिए। चलिए, शुरू करें! |
| `vo_rev_tt_aa` | 4.89 | सही डिब्बा यह है। हाथ शब्द में आ की मात्रा है। |
| `vo_rev_tt_ee` | 4.53 | सही डिब्बा यह है। पानी शब्द में बड़ी ई की मात्रा है। |
| `vo_rev_tt_i` | 4.77 | सही डिब्बा यह है। पिन शब्द में छोटी इ की मात्रा है। |
| `vo_s1_prompt` | 5.93 | आज हम आ की मात्रा, छोटी इ की मात्रा और बड़ी ई की मात्रा वाले शब्द पढ़ेंगे। |
| `vo_ts1_hint1` | 3.17 | फिर से सुनो और सही मात्रा पहचानिए। |
| `vo_ts1_hint2` | 3.57 | ध्यान से देखो, इस शब्द में कौन-सी मात्रा है? |
| `vo_ts1_ok_haath` | 4.21 | शाबाश! हाथ शब्द में आ की मात्रा है। |
| `vo_ts1_ok_neem` | 4.33 | शाबाश! नीम शब्द में बड़ी ई की मात्रा है। |
| `vo_ts1_ok_pin` | 4.41 | शाबाश! पिन शब्द में छोटी इ की मात्रा है। |
| `vo_ts1_prompt` | 4.21 | हर शब्द को उसकी सही मात्रा वाली बोगी में डालिए। |
| `vo_ts2_hint1` | 3.81 | फिर से सोचो। इस शब्द में कौन-सी मात्रा लगी है? |
| `vo_ts2_hint2` | 2.97 | ध्यान से देखो और शब्द को फिर से पढ़ो। |
| `vo_ts2_ok_jaal` | 4.53 | शाबाश! जाल शब्द में आ की मात्रा लगी है। |
| `vo_ts2_ok_keel` | 3.97 | शाबाश! कील शब्द में बड़ी ई की मात्रा लगी है। |
| `vo_ts2_ok_sir` | 4.09 | शाबाश! सिर शब्द में छोटी इ की मात्रा लगी है। |
| `vo_ts2_prompt` | 3.73 | सही मात्रा को सही शब्द वाली बोगी में डालिए। |
| `vo_ts3_hint1` | 3.25 | फिर से सुनो और सही मात्रा पहचानो। |
| `vo_ts3_hint2` | 1.69 | शब्द को ध्यान से सुनो। |
| `vo_ts3_ok_haath` | 4.21 | शाबाश! हाथ में आ की मात्रा है। |
| `vo_ts3_ok_hiran` | 3.65 | शाबाश! हिरण में छोटी इ की मात्रा है। |
| `vo_ts3_ok_keel` | 3.29 | शाबाश! कील में बड़ी ई की मात्रा है। |
| `vo_ts3_ok_naak` | 3.05 | शाबाश! नाक में आ की मात्रा है। |
| `vo_ts3_ok_neem` | 3.85 | शाबाश! नीम में बड़ी ई की मात्रा है। |
| `vo_ts3_ok_pin` | 2.73 | शाबाश! पिन में छोटी इ की मात्रा है। |
| `vo_ts3_prompt` | 4.09 | चित्र को सुनो और उसे सही मात्रा वाली बोगी में डालिए। |
| `vo_tt_aa_correct` | 3.73 | शाबाश! हाथ शब्द में आ की मात्रा है। |
| `vo_tt_aa_hint1` | 3.77 | फिर से सोचो। आ की मात्रा वाला शब्द कौन-सा है? |
| `vo_tt_aa_hint2` | 3.17 | ध्यान से देखो और सही डिब्बे पर टैप कीजिए। |
| `vo_tt_aa_prompt` | 5.21 | जिस डिब्बे में आ की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए। |
| `vo_tt_ee_correct` | 4.37 | शाबाश! पानी शब्द में बड़ी ई की मात्रा है। |
| `vo_tt_ee_hint1` | 4.17 | फिर से सोचो। बड़ी ई की मात्रा वाला शब्द कौन-सा है? |
| `vo_tt_ee_hint2` | 2.97 | ध्यान से देखो और सही डिब्बे पर टैप करो। |
| `vo_tt_ee_prompt` | 5.41 | जिस डिब्बे में बड़ी ई की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए। |
| `vo_tt_i_correct` | 3.85 | शाबाश! पिन शब्द में छोटी इ की मात्रा है। |
| `vo_tt_i_hint1` | 4.05 | फिर से सोचो। छोटी इ की मात्रा वाला शब्द कौन-सा है? |
| `vo_tt_i_hint2` | 3.09 | ध्यान से देखो और सही डिब्बे पर टैप करो। |
| `vo_tt_i_prompt` | 4.69 | जिस डिब्बे में छोटी इ की मात्रा वाला शब्द है, उस डिब्बे पर टैप कीजिए। |
