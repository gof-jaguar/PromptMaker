# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Run Command

```bash
python3 -m streamlit run app.py
```

No build step, no environment variables, no API keys required. Single dependency: `streamlit>=1.30.0`.

Deployed on Streamlit Cloud — pushing to `main` on GitHub auto-deploys to https://promptmaker.streamlit.app/.

## Architecture

Single-file Streamlit app (`app.py`, ~5900 lines) structured in sequential sections:

1. **TRANSLATIONS** — Bilingual dictionary (EN/TH) with 1332 keys. Every UI string goes through `t(key)` helper.
2. **ENGLISH_VALUES** — Maps option keys to English prompt text for AI output (e.g. `"hair_long"` → `"long flowing hair"`). Dropdown/selectbox options that affect the generated prompt need entries here.
3. **HELPERS** — `t()` for translation, `eng()` for prompt values, `make_option()` for selectbox pairs, `translate_to_english()` for Thai→English with a mini dictionary, `look_desc()` which builds one person's hair/bangs/expression/makeup phrase while skipping any "None / Not specified" pick.
3.5. **OPTION KEY LISTS + RANDOMIZER** — Module-level `*_KEYS` constants (single source of truth for every selectbox's option keys, including `MT_KEYS` model types, `LENS_KEYS`, `GD_KEYS`/`AG_KEYS`/`ET_KEYS` identity lists, `MU_KEYS` makeup, `NS_KEYS` people count, `SH_KEYS` footwear), `PHOTO_MODEL_KEYS` (photographic model types that get the lens spec), `AR_RATIOS` (raw ratio strings per aspect key), `RANDOM_WIDGETS` (widget key → option list map), `SCENE_RANDOM_WIDGETS` (scene/camera subset), `PRESET_WIDGETS` (save/load field map), and the `randomize_look()`, `randomize_scene()`, `apply_look_preset()`, `reset_hair_on_gender_change()`, `reset_person_hair()` callbacks, plus `GM_KEYS` (group gender mix), `HAIR_GENDER_WIDGETS` (hairstyle widget → gender widget map) and `hair_pool_for_label()`. Also `PET_KEYS` (companion animal), `THEME_PRESETS` + `apply_theme()` (built-in look/scene bundles applied via the shared `_apply_preset_dict()` helper), and `PHOTO_SET_SF_KEYS`/`PHOTO_SET_CA_KEYS`/`PHOTO_SET_POSE_EXCLUDE`/`PHOTO_SET_SIZE` + `request_photo_set()` for Photo Set mode. v5.7 adds the pose builder (`PC_KEYS`, `POSE_CATEGORIES` → derived `PO_KEYS`, `pose_keys_for_category()`, `BD_KEYS`/`HD_KEYS`/`HA_KEYS`/`LG_KEYS` in `POSE_DETAIL_WIDGETS`, `GZ_KEYS`, `PE_KEYS`) and outfit layers (`OM_KEYS`, `DR_KEYS`, `OSET_KEYS`, `OUT_KEYS`, `FIT_KEYS`, `LEG_KEYS`, `DET_KEYS`), plus `LOOK_BASE` (neutral values themes are applied over) and `garment_picker()`. v5.8 adds subject detail lists (`ST_KEYS` skin tone, `FSH_KEYS`, `EYE_KEYS`, `EC_KEYS`, `BROW_KEYS`, `LIP_KEYS`, `FM_KEYS`, `FH_KEYS`, `SKF_KEYS`, `HF_KEYS`, `NL_KEYS`), Character Lock (`CHAR_WIDGETS`, `lock_character()`, `_lock()`, `unlock_character()`, `load_library_character()`, `enforce_character_lock()`, `widget_option_value()`), camera/scene lists (`CH_KEYS`, `CD_KEYS`, `CS_KEYS`, `CF_KEYS`, `LD_KEYS`, `LC_KEYS`, `LQ_KEYS`, `ATM_KEYS`, `BGP_KEYS`, `LFX_KEYS`, `LCAT_KEYS` + `LOC_CATEGORIES` → derived `LO_KEYS`, `loc_keys_for_category()`), `CAM_MIGRATION`, `MULTI_WIDGETS` (all multiselects), `SCENE_BASE` and `_reset_scene_pickers()`. `LANG_DEPENDENT_WIDGETS` is now derived from `PRESET_WIDGETS` + `MULTI_WIDGETS`.
4. **CSS** — Injected via `st.markdown(unsafe_allow_html=True)`. Responsive breakpoints at 768px (mobile) and 1400px (desktop). Uses Noto Sans Thai font. `.streamlit/config.toml` sets `disableWidgetStateDuplicationWarning` because widgets are deliberately set via session state while passing a default index.
5. **MAIN UI** — 5 expanders (Subject, Outfit, Pose, Scene, Advanced); Scene has Lighting and Camera sub-groups + sidebar (language, aspect ratio, model type, target platform).
6. **GENERATE + OUTPUT** — Builds 7 prompt sections, stores in `st.session_state` with `ta_*` keys for editable text areas, combines into final prompt. Also records each generated prompt into `st.session_state["prompt_history"]` (last 10, shown in an expander at the bottom).

## Key Patterns

**Adding a new dropdown/selectbox option** (e.g. a new hair style):
1. Add key to `TRANSLATIONS["en"]` and `TRANSLATIONS["th"]`
2. Add English prompt text to `ENGLISH_VALUES`
3. Add key to the relevant module-level `*_KEYS` constant (e.g. `HR_KEYS`) — the UI and the Random Look button both read from these
4. If it affects prompt generation, update the corresponding section in the generate block

**Adding a new checkbox option** (e.g. a new accessory or weather effect):
1. Add key to both `TRANSLATIONS` dicts
2. Add English prompt text to `ENGLISH_VALUES` (for accessories) or handle inline in the generate block (for weather effects)
3. Add the `st.checkbox()` call in the UI section
4. Wire it into the prompt generation logic

**Translation system:** `t(key)` reads `st.session_state["lang"]` ("en"/"th") and returns the translated label. `eng(key)` always returns the English prompt value regardless of UI language.

**Session state for editable output:** When "Generate" is clicked, sections are stored as `st.session_state["ta_technical"]`, `["ta_subject"]`, etc. These keys are bound directly to `st.text_area(key=...)` widgets so users can edit sections inline. The combined prompt rebuilds from current widget values on every rerun.

**Thai text handling:** `translate_to_english()` detects Thai characters (Unicode `\u0e00`–`\u0e7f`), applies a ~50-entry mini dictionary for common fashion/location terms, and wraps any remaining Thai in parentheses.

**Reference photos:** No file upload — checkboxes toggle prompt instructions (e.g. "the exact same person as in the attached reference photo, preserving their facial identity and features precisely") and show reminder notes in the output. Four checkboxes: subject (face/person), outfit (mannequin/flat-lay images allowed), pose (`attach_pose` — copies only body position/limbs/head angle from e.g. a mannequin pose sheet; disables the pose/category/detail pickers, gaze + mood + free text still apply), scene.

**Model types (9, sidebar):** Realistic Photography, Cinematic Film Still, Analog Film Photo, Fashion Editorial, Anime, Digital Painting, Watercolor, Comic/Manga, 3D Render. Only the four photographic types (in `PHOTO_MODEL_KEYS`) get a lens spec appended to the Technical section; the lens selectbox (24/35/50/85/135mm, default 35mm, `LENS_KEYS`) only renders for those types.

**Makeup style (16, Subject expander):** `MU_KEYS`, None-first; K-beauty options (dewy glow, gradient lips), Douyin C-beauty, igari blush, glam, goth, editorial, faux freckles, sun-kissed bronzed, Y2K glitter, smoky, red lip, no-makeup look. Appended to the subject section after the expression.

**Subject expander layout (v5.8):** Character Lock box → reference checkbox → sub-headed groups: Identity (gender, age, ethnicity, skin tone `ST_KEYS` light→dark, body type, appearance) · Face Details (face shape, eye shape + eye color → combined as `"{shape} {color} eyes"`, brows, lips, skin finish `SKF_KEYS` — replaces the old skin-texture checkbox, charm-point multiselect `face_marks`/`FM_KEYS` e.g. mole under eye, aegyo-sal, dimples, snaggletooth; facial hair `FH_KEYS` only rendered for non-female) · Hair (style, color, bangs, hair finish `HF_KEYS`) · Expression, Makeup & Nails (`NL_KEYS`) · People & Companion. A local `pick()` helper renders each selectbox and disables it when the widget is in `CHAR_WIDGETS` and a character is locked. The main person's description = `with {face details}` + `look_desc(…, hf_k)` + nails; skin tone joins the traits; skin finish is appended at the end.

**Character Lock:** Name + "Lock" button store `st.session_state["char_lock"] = {"name", "data"}` where data maps `CHAR_WIDGETS` (identity, skin tone, body, appearance, face details, facial hair, hair style/color/bangs) to option keys; it's also added to a per-session library (`char_library`, selectbox `w_char_lib` + "Load & lock"). `enforce_character_lock()` runs at the top of the Subject expander and re-sets any locked widget whose label differs — so Random Look, themes, presets and language switches can't change the character (no special-casing needed in those callbacks). Prompt: solo → `"{name}, a …"`, duo/trio → `the first ({name})`, group → `the central person ({name})`, plus `", the same recurring character with a consistent face and identity in every image"`. "Download character" exports `{"char_name": …, **data}`; pasting such JSON into Apply Look unlocks, applies, then locks the resulting character.

**Number of People (Subject expander):** `NS_KEYS` — solo (default, "a {…}"), duo/trio/group. Ignored when the subject reference photo checkbox is on. Deliberately not randomized. Group shows a Group Genders selectbox (`w_group_mix`, `GM_KEYS`: same as main gender / mixed) — "mixed" prompts `… people, a mixed group of men and women`.

**Per-person looks (duo/trio):** When duo or trio is selected, extra "Person 2/3" rows render with their own gender / hair / hair color / expression selectboxes (keys `w_gender_p2`, `w_hair_p2`, `w_hair_color_p2`, `w_expr_p2`, `_p3` variants; staggered default indexes so people differ out of the box). Each person's hairstyle pool follows *their own* gender (`w_gender_pN` `on_change=reset_person_hair` pops that person's stale hair pick; changing the main gender resets the per-person genders and all hair picks). Person 1 uses the main subject selectors. When all genders match, the prompt reads `two {…} {gender}s, {body}, {vibe}, the first with …; the second with …`; with mixed genders it becomes `two {…} people, …, the first a female, with …; the second a male, with …`. Group (5) instead details the central person and instructs "each person with a clearly distinct hairstyle, outfit variation and expression". `HAIR_GENDER_WIDGETS` maps each hairstyle widget to its gender widget — gender changes and preset loads validate/reset each against that person's hair pool; Random Look also randomizes the p2/p3 widgets.

**Footwear (21, Outfit expander):** `SH_KEYS`, None-first, A-Z (boots, heels, sneakers, flats, sandals, barefoot). Appended to the outfit section after the garments. Random Look picks footwear only in its garment-led branches.

**Garment counts:** 31 tops + None (`TOP_KEYS`, incl. jackets/outerwear like leather, bomber, varsity, puffer, trench) and 30 bottoms + None (`BOT_KEYS`, incl. jeans variants, skirt lengths, joggers, palazzo, skort).

**Midjourney stylize/seed (sidebar):** When Target Platform is Midjourney, a `--stylize` number input (0–1000, default 100, only emitted when ≠ 100) and optional `--seed` text input (emitted only if digits) appear; both are appended to the `--ar` parameter block.

**Scene location modes:** Three radio options — preset list, free-text description, or real place/travel (landmark + city + country fields). The real place mode builds location strings like `"at Eiffel Tower, Paris, France"`.

**Weather & atmosphere:** A multiselect (`atm_multi`, `ATM_KEYS`, A-Z) replaced the four weather checkboxes — rain, snow, autumn leaves, gentle breeze plus after-rain reflections, fog, cherry petals, fireflies, bubbles, dust in light, sparkles, smoke, steam, confetti. Background people (`BGP_KEYS`) is appended after it in the environment section.

**Location categories:** `LOC_CATEGORIES` maps 11 categories (`LCAT_KEYS` + `lcat_all`: studio & indoor, home & bedroom, city, cafés & shops, nature, beach & water, luxury, landmarks & travel, Thailand, Japan & Korea, sports & leisure) to locations; `LO_KEYS` is derived (`loc_none`, `loc_studio`, then A-Z), so **a new location only needs translations, an `ENGLISH_VALUES` entry and a slot in `LOC_CATEGORIES`**. `w_loc_cat` filters `w_location` (stale label popped before render; preset loads fall back to "All" when needed).

**Lighting layers:** Lighting style (`LT_KEYS`) + direction (`LD_KEYS`: Rembrandt, butterfly, clamshell, split, loop, side, back…) + color (`LC_KEYS`: warm, cool, teal & orange, pink & blue…) + quality (`LQ_KEYS`: soft, hard, high/low contrast).

**Camera (v5.8 — replaces the single Camera Angle / `w_angle`):** Framing + camera height (`CH_KEYS`, ordered high→low, default eye level) + camera position around the subject (`CD_KEYS`, ordered front→back) + special shot (`CS_KEYS`: selfie, POV, mirror, CCTV, fisheye, dutch, telephoto, through foreground/window). These spatial lists deliberately break the A-Z rule. A caption previews the camera text live. Camera body / film stock (`CF_KEYS`, e.g. Portra 400, CineStill 800T, Fujifilm, Leica, iPhone, disposable) renders only for `PHOTO_MODEL_KEYS` and is emitted in the Technical section. Lens & film effects multiselect (`lfx_multi`, `LFX_KEYS`) is appended to the camera section as `with a, b and c`. Old look.json `w_angle` values are mapped through `CAM_MIGRATION`. Random Look/Scene (`_reset_scene_pickers()`) draw height/position from the portrait-friendly Photo Set pools and always reset the special shot and location category.

**Lighting (25 + None):** Realistic (natural, window, studio, high-key, low-key, rim, flash, backlight halo, dappled leaves, window-blinds shadows, moonlight, campfire, sunset silhouette) and stylized (neon, fairy lights, paper lanterns, candlelight, chiaroscuro, red/blue color gel, stage spotlight, fireworks, screen glow, projector patterns, disco ball, volumetric god rays).

**Picture style (22):** Realistic looks (clean commercial, editorial magazine, documentary/street, polaroid, Y2K digicam, HDR, matte, vintage film, warm nostalgic film, B&W) and imaginative looks (dreamy, ethereal fantasy, dark fairytale, cyberpunk neon, vaporwave/retrowave, dreamcore surreal, moody, pastel, cinematic grade). Appended to the camera/lighting section in the generated prompt.

**Fashion styles (43) and colors (32):** Fashion presets include trend aesthetics (Barbiecore, Clean Girl, Dark/Light Academia, E-girl, Gorpcore, Mob Wife, Parisian Chic, Rockstar, Skater, Western, Thai Traditional), teen/school looks (Teen/High-School, School Uniform, Cheerleader), swimwear (Bikini, One-piece, Rash Guard/Surf, Beachwear/Cover-up) and sports (Tennis, Golf, Basketball, Ski, Yoga). The color palette (col_none first, then A-Z) covers metallics (gold, silver), trend shades (hot pink, lilac, mint, peach, coral, baby blue, teal, khaki, brown) and a colorblock option.

**Outfit top/bottom garments with independent fabric & color:** Two columns (Top and Bottom) each with their own garment selector, fabric selector, and color selector. Garments default to a "None (let fashion style decide)" first option (`top_none`/`bot_none`, empty `ENGLISH_VALUES`) so fashion presets alone can define the outfit without clashing; fabric & color selectboxes are only rendered when a garment is chosen, and fabric/color also have "Not specified" first options (`fab_none`/`col_none`). If both a fashion preset and an explicit garment are set, a hint caption (`outfit_clash_hint`) warns about possible clashes. In the generate block, each non-None garment gets its own fabric and color description (each part omitted when unset): `wearing a crop top made of silk fabric in white and cream color tones, wearing jeans made of denim in blue color tones`.

**Outfit type + layers (v5.7):** A radio (`w_outfit_mode`, `OM_KEYS`) picks Top + Bottom / Dress / Ready-made Set; only that type's garments are rendered and used. Dress (`DR_KEYS`, 19) has its own fabric/color via the shared `garment_picker()`. Sets (`OSET_KEYS`, 29, emoji-prefixed by season: 🌸 spring, ☀️ summer, 🍂 autumn, ❄️ winter, ✨ party) are complete coordinated looks inspired by layered costume references (layers, legwear, shoes, bag, jewelry) — in Set mode the layer pickers and footwear are hidden. Otherwise: outer layer (`OUT_KEYS`, noun phrases → `layered with {outer} in {color}`), fit/silhouette (`FIT_KEYS`), socks & legwear (`LEG_KEYS`), footwear, and a design-details multiselect (`detail_multi`, `DET_KEYS`: ruffles, ribbon bows, lace trim, puff sleeves, collars, prints… → `featuring a, b and c`). Outfit order: presets, garments/dress/set, outer, fit, details, legwear, footwear, free text, reference, accessories. Fabrics now 18 + None (adds corduroy, crochet, jersey, fine knit, organza, sequin, tulle); colors add butter yellow, grey, ivory.

**Hair styles filtered by gender:** `HR_KEYS_WOMEN` (None + 23 styles) and `HR_KEYS_MEN` (None + 10 styles) are separate lists, each starting with the shared `hair_none`; `HR_KEYS = HR_KEYS_WOMEN + HR_KEYS_MEN[1:]` is the deduped superset used for non-binary and language resets. `hair_keys_for_gender(gd_key)` picks the option pool for the hairstyle selectbox based on the gender selectbox (key `w_gender`), whose `on_change=reset_hair_on_gender_change` pops the stale hair and per-person gender selections; `hair_pool_for_label()` is the same lookup keyed by translated label (used in callbacks).

**Hair colors (19):** Ordered dark→light→fashion colors, incl. popular shades: blue black, ash brown, milk tea brown, honey blonde, burgundy/cherry, rose gold.

**Bangs selectbox:** Independent of hairstyle — users can combine any hairstyle with any bangs type (none, straight, see-through, side, curtain, wispy, micro, hime sidelocks). In the generate block, bangs text is inserted between hair color and expression: `with {hair}, {color}, {bangs}, and {expression}`. When "None" is selected, the bangs part is omitted entirely.

**Expressions (27 + None):** Ordered cheerful→neutral→moody, incl. charming/cute options (bright beaming smile, giggling, winking, tongue out, mischievous grin, soft gaze, doe eyes, cute pout, smirk) and moody ones (fierce gaze, eyes closed, bored, angry, tearful).

**Appearance / Vibe options (16, A-Z):** Includes general looks (cute, beautiful, cool, charming, chic, doll-like, girl-next-door, youthful, etc.) plus idol-specific looks: K-pop Idol, J-pop Idol, and C-pop Star, each with tailored prompt descriptions for skin, makeup, and feature characteristics.

**Poses (140 + None) — two-level picker (Pose expander):** `POSE_CATEGORIES` maps 10 categories (`PC_KEYS`, plus `pc_all`) — standing, walking & motion, sitting, kneeling, lying, crouching & bending, cute hand gestures, social media & fashion, nature & props, sports & action — to pose keys; every pose is in exactly one category. `PO_KEYS` is *derived* (`pose_none` + all mapped poses sorted A-Z by English label), so **a new pose only needs its translations, `ENGLISH_VALUES` entry and a slot in `POSE_CATEGORIES`**. The category selectbox (`w_pose_cat`, `on_change=reset_pose_on_category_change`) filters the pose selectbox via `pose_keys_for_category()`; a stale pose label is popped before render. Random Look / loaded presets set the category back to "All" when needed.

**Pose fine-tuning (Pose expander):** Body orientation (`BD_KEYS`), head position (`HD_KEYS`), arms & hands (`HA_KEYS`), legs & stance (`LG_KEYS`) — these four are `POSE_DETAIL_WIDGETS`, pose-specific, reset to None by Random Look and themes. Gaze (`GZ_KEYS`, replaces the old look-at-camera checkbox — `gaze_camera` keeps its text) and pose mood/energy (`PE_KEYS`) apply to any pose, are randomized, and carry over to every Photo Set shot. Plus a free-text pose description (`pose_text_input`, Thai-translated). Pose section order: pose, orientation, legs, hands, head, gaze, mood, free text.

**DOF/background (9 + None), compositions (12):** DOF adds bokeh light orbs, motion-blur background, blurred foreground framing, and clean studio background. Composition adds diagonal lines, fill-the-frame, reflection/mirror, and layered depth.

**Target AI Platform (sidebar):** Universal (Gemini · Imagen) / Midjourney / Stable Diffusion. Controls output formatting at generate time: Midjourney gets `--ar {ratio}` and the negative prompt is appended inline as `--no {negative}` (no separate negative block shown); other platforms get plain-English `in {ratio} aspect ratio` and the negative prompt shown separately. Raw ratios live in `AR_RATIOS`.

**Random Look button (🎲):** Next to Generate. Its `on_click=randomize_look` callback assigns a random translated label to every style widget key in `RANDOM_WIDGETS` (identity fields — gender, age, ethnicity — are deliberately not randomized), then handles special cases: hair is drawn from the pool matching the current gender; the pose category resets to All and pose details to None; and the outfit is exactly one of — 1–2 fashion presets / separates with fabric & color / a dress with fabric & color (both garment branches optionally add outer layer, legwear, fit and 0–2 details) / a ready-made set. Sets `force_generate=True` so the prompt is generated in the same rerun.

**Random Scene button (🎬):** Third button in the row. `randomize_scene()` randomizes only the widgets in `SCENE_RANDOM_WIDGETS` (location, time, lighting + light direction/color, season, picture style, framing, DOF, composition; camera height/position via `_reset_scene_pickers()`) — subject, outfit and pose stay fixed, for consistent-character variations. Also auto-generates.

**Photo Set button (📸):** Fourth button in the row. `request_photo_set()` sets `photo_set_request` + `force_generate`; inside the generate block, after the normal sections are built, 6 (`PHOTO_SET_SIZE`) prompt variants are assembled sharing the same technical/subject/outfit/environment sections while the pose is sampled without replacement from `PO_KEYS` (minus `PHOTO_SET_POSE_EXCLUDE` — no mirror selfie, sports poses etc.) and framing/camera height/position are drawn from the portrait-friendly `PHOTO_SET_SF_KEYS`/`PHOTO_SET_CH_KEYS`/`PHOTO_SET_CD_KEYS` pools (light direction/color/quality and lens effects carry over). Poses stay inside the selected pose category when it has ≥ 6 eligible poses (e.g. an all-sitting album); `PHOTO_SET_POSE_EXCLUDE` covers the whole sports category plus selfies/phone. Gaze + mood carry over; pose details and the pose reference don't. Stored in `st.session_state["photo_set_prompts"]`, rendered as numbered `st.code` blocks above the history with a "download all" button (`photo_set.txt`); a subsequent normal Generate clears the stale set.

**Companion animal (Subject expander):** `PET_KEYS` selectbox (`w_pet`, None-first: bird on finger, butterflies, cat, dog, kitten, puppy, rabbit) — appends an interaction phrase (e.g. "gently reaching out to a cute cat…") to the subject section. Saved in look presets; deliberately not randomized.

**Quick Themes (sidebar):** `THEME_PRESETS` maps 6 theme keys (applied over `LOOK_BASE`, so outfit layers/pose details from the previous look are cleared; themes also set gaze + mood) (golden-hour garden — matches the ivy brick-house photoshoot aesthetic —, neon night, café film, beach, studio editorial, cherry blossom) to preset dicts in the `PRESET_WIDGETS` option-key format. A sidebar selectbox (`w_theme`) + "Apply Theme" button call `apply_theme()`, which routes through `_apply_preset_dict()` (shared with Save/Load) and auto-generates. Identity fields (gender/age/ethnicity) are intentionally absent from every theme so the chosen subject persists.

**Save / Load Look (Advanced expander):** `st.download_button` exports the current selections as `look.json` mapping widget keys → *option keys* (language-independent, via `PRESET_WIDGETS`); per-person gender/hair/color/expression and the group mix are included when visible. Loading = paste JSON into a text area + "Apply Look" button whose `apply_look_preset()` callback sets all gender widgets first, validates each key against its option list (hair additionally against that person's gender pool via `HAIR_GENDER_WIDGETS`), sets widget labels via `t()`, and auto-generates. Invalid JSON sets `preset_status` = "error" which renders an `st.error`.

**Language-switch state clearing:** Keyed selectboxes store the *translated label* in session state. When the language radio changes, all keys in `LANG_DEPENDENT_WIDGETS` are popped so stale labels can't collide with the new option lists (this resets those widgets to defaults, same as pre-keyed behavior).

**Prompt history:** Each Generate prepends the combined prompt to `st.session_state["prompt_history"]` (consecutive duplicates skipped, capped at 10). Rendered in a `🕘` expander at the bottom via `st.code` (which has a built-in copy icon).

**Download button:** `st.download_button` next to the copy button saves the combined prompt (plus negative prompt for non-Midjourney platforms) as `prompt.txt`. A character/word count caption is shown under the final prompt.

**Copy button:** Uses `streamlit.components.v1.html()` (not `st.markdown`) because Streamlit strips JS event handlers from markdown. Uses `navigator.clipboard.writeText()` with `execCommand('copy')` fallback. Prompt text is escaped via `json.dumps()` for proper JS string escaping inside `<script>` tags (not `html.escape()`, which breaks apostrophes in values like "bird's eye view").

**"None / Not specified" options:** Nearly every selectbox has a none-first option (`age_none`, `eth_none`, `hair_none`, `hc_none`, `expr_none`, `bt_none`, `app_none`, `pose_none`, `tod_none`, `lit_none`, `loc_none`, `sf_none`, `cam_none`, `dof_none`, plus the pre-existing `mu_none`, `bangs_none`, `season_none`, `ps_none`, `comp_center`, garment/fabric/color/footwear nones) mapping to an empty `ENGLISH_VALUES` string. The generate block filters out empty parts everywhere, so any combination of unset fields stays grammatical. Because None sits at index 0, the selectboxes pass an explicit `index=` to keep the old meaningful defaults (e.g. hair `index=1`, framing `index=2`, DOF `index=2`); pose now defaults to None.

**Sorting convention:** All selectbox/multiselect option lists are sorted A-Z by their English label. This applies to: fashion presets, top garments, bottom garments, fabric, color palette, poses, and appearance options.

## Prompt Generation Sections

The generate block builds these sections (in order), each stored as an editable `st.text_area`:
1. **Technical** — model type + lens + camera/film stock (photographic model types only) + quality tags
2. **Subject** — [character name] + gender, age, ethnicity, skin tone, body type, appearance, face details, hair (+ color, finish, bangs), expression, makeup, nails, skin finish, companion, [lock consistency phrase] (per person for duo/trio)
3. **Outfit** — fashion presets + top/bottom, dress, or outfit set (garments with fabric & color) + outer layer + fit + details + legwear + footwear + free text + accessories
4. **Pose** — pose reference *or* pose + orientation + legs + hands + head, then gaze + mood + free text
5. **Environment** — location + time of day + season + atmosphere + background people
6. **Camera & Lighting** — lighting style + direction + color + quality + framing + camera height + position + special shot + DOF + composition + picture style + lens effects
7. **Custom** — free-text additions

Plus aspect ratio appended at the end (formatted per target platform) and negative prompt shown separately (or embedded via `--no` for Midjourney).

## Bilingual Conventions

- All user-facing strings must exist in both `TRANSLATIONS["en"]` and `TRANSLATIONS["th"]`
- Prompt output is always in English (via `ENGLISH_VALUES`), regardless of UI language
- Thai placeholder/help text should use natural Thai, not transliterated English
- Verify key parity after changes: every key in EN must exist in TH and vice versa

## Verification After Changes

Check syntax and key parity with:
```bash
python3 -c "
import ast
with open('app.py') as f: tree = ast.parse(f.read())
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name) and t.id == 'TRANSLATIONS':
                d = ast.literal_eval(node.value)
                en, th = set(d['en']), set(d['th'])
                print(f'EN: {len(en)}, TH: {len(th)}')
                print(f'Only EN: {en - th}') if en - th else None
                print(f'Only TH: {th - en}') if th - en else None
                if en == th: print('Parity OK')
"
```
