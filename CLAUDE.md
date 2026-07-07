# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Run Command

```bash
python3 -m streamlit run app.py
```

No build step, no environment variables, no API keys required. Single dependency: `streamlit>=1.30.0`.

Deployed on Streamlit Cloud — pushing to `main` on GitHub auto-deploys to https://promptmaker.streamlit.app/.

## Architecture

Single-file Streamlit app (`app.py`, ~2710 lines) structured in sequential sections:

1. **TRANSLATIONS** — Bilingual dictionary (EN/TH) with 563 keys. Every UI string goes through `t(key)` helper.
2. **ENGLISH_VALUES** — Maps option keys to English prompt text for AI output (e.g. `"hair_long"` → `"long flowing hair"`). Dropdown/selectbox options that affect the generated prompt need entries here.
3. **HELPERS** — `t()` for translation, `eng()` for prompt values, `make_option()` for selectbox pairs, `translate_to_english()` for Thai→English with a mini dictionary.
3.5. **OPTION KEY LISTS + RANDOMIZER** — Module-level `*_KEYS` constants (single source of truth for every selectbox's option keys, including `MT_KEYS` model types, `LENS_KEYS`, `GD_KEYS`/`AG_KEYS`/`ET_KEYS` identity lists, `MU_KEYS` makeup, `NS_KEYS` people count, `SH_KEYS` footwear), `PHOTO_MODEL_KEYS` (photographic model types that get the lens spec), `AR_RATIOS` (raw ratio strings per aspect key), `RANDOM_WIDGETS` (widget key → option list map), `SCENE_RANDOM_WIDGETS` (scene/camera subset), `PRESET_WIDGETS` (save/load field map), and the `randomize_look()`, `randomize_scene()`, `apply_look_preset()`, `reset_hair_on_gender_change()` callbacks.
4. **CSS** — Injected via `st.markdown(unsafe_allow_html=True)`. Responsive breakpoints at 768px (mobile) and 1400px (desktop). Uses Noto Sans Thai font.
5. **MAIN UI** — 4 expanders (Subject, Outfit, Scene, Advanced) + sidebar (language, aspect ratio, model type, target platform).
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

**Reference photos:** No file upload — checkboxes toggle prompt instructions (e.g. "the exact same person as in the attached reference photo, preserving their facial identity and features precisely") and show reminder notes in the output. Three checkboxes: subject (face/person), outfit, scene.

**Model types (9, sidebar):** Realistic Photography, Cinematic Film Still, Analog Film Photo, Fashion Editorial, Anime, Digital Painting, Watercolor, Comic/Manga, 3D Render. Only the four photographic types (in `PHOTO_MODEL_KEYS`) get a lens spec appended to the Technical section; the lens selectbox (24/35/50/85/135mm, default 35mm, `LENS_KEYS`) only renders for those types.

**Makeup style (10, Subject expander):** `MU_KEYS`, None-first; K-beauty options (dewy glow, gradient lips), Douyin C-beauty, glam, smoky, red lip, no-makeup look. Appended to the subject section after the expression.

**Number of People (Subject expander):** `NS_KEYS` — solo (default, "a {…}"), duo/trio/group phrasing (`two/three/a group of five {…} {gender}s, … both/all with {hair}…`). Ignored when the subject reference photo checkbox is on. Deliberately not randomized.

**Footwear (11, Outfit expander):** `SH_KEYS`, None-first, A-Z. Appended to the outfit section after the garments. Random Look picks footwear only in its garment-led branch.

**Midjourney stylize/seed (sidebar):** When Target Platform is Midjourney, a `--stylize` number input (0–1000, default 100, only emitted when ≠ 100) and optional `--seed` text input (emitted only if digits) appear; both are appended to the `--ar` parameter block.

**Scene location modes:** Three radio options — preset list, free-text description, or real place/travel (landmark + city + country fields). The real place mode builds location strings like `"at Eiffel Tower, Paris, France"`.

**Weather effects:** Three checkboxes (rain, snow, autumn leaves) under the Season selector. These append weather text to the environment section during prompt generation.

**Picture style:** Dropdown in the Scene & Lighting expander with styles like dreamy, cinematic, B&W, etc. Appended to the camera/lighting section in the generated prompt.

**Outfit top/bottom garments with independent fabric & color:** Two columns (Top and Bottom) each with their own garment selector, fabric selector, and color selector. Garments default to a "None (let fashion style decide)" first option (`top_none`/`bot_none`, empty `ENGLISH_VALUES`) so fashion presets alone can define the outfit without clashing; fabric & color selectboxes are only rendered when a garment is chosen, and fabric/color also have "Not specified" first options (`fab_none`/`col_none`). If both a fashion preset and an explicit garment are set, a hint caption (`outfit_clash_hint`) warns about possible clashes. In the generate block, each non-None garment gets its own fabric and color description (each part omitted when unset): `wearing a crop top made of silk fabric in white and cream color tones, wearing jeans made of denim in blue color tones`.

**Hair styles filtered by gender:** `HR_KEYS_WOMEN` (23 styles) and `HR_KEYS_MEN` (10 styles) are separate lists; `HR_KEYS = HR_KEYS_WOMEN + HR_KEYS_MEN` is the superset used for non-binary and language resets. `hair_keys_for_gender(gd_key)` picks the option pool for the hairstyle selectbox based on the gender selectbox (key `w_gender`), whose `on_change=reset_hair_on_gender_change` pops the stale `w_hair` selection.

**Hair colors (19):** Ordered dark→light→fashion colors, incl. popular shades: blue black, ash brown, milk tea brown, honey blonde, burgundy/cherry, rose gold.

**Bangs selectbox:** Independent of hairstyle — users can combine any hairstyle with any bangs type (none, straight, see-through, side, curtain, wispy, micro, hime sidelocks). In the generate block, bangs text is inserted between hair color and expression: `with {hair}, {color}, {bangs}, and {expression}`. When "None" is selected, the bangs part is omitted entirely.

**Expressions (19):** Ordered cheerful→neutral→moody, incl. charming/cute options: bright beaming smile, giggling, soft gaze, doe eyes, cute pout, smirk.

**Appearance / Vibe options (16, A-Z):** Includes general looks (cute, beautiful, cool, charming, chic, doll-like, girl-next-door, youthful, etc.) plus idol-specific looks: K-pop Idol, J-pop Idol, and C-pop Star, each with tailored prompt descriptions for skin, makeup, and feature characteristics.

**Poses (45 total, A-Z sorted):** Standard poses, idol/cute poses (heart hands, mini heart, peace sign, hands framing face, hugging knees, winking, etc.), and model/editorial poses: runway walk, high-fashion stance, editorial model pose, elegant graceful pose, hand on hip, chin up, head tilt, candid motion, dancing, stretching, sitting on stairs, leaning toward camera, looking up.

**Locations (34, `loc_studio` first then A-Z):** Includes airport, aquarium, art gallery, bridge, castle, desert, European old town, grand staircase, gym, lakeside pier, luxury hotel lobby, mountain viewpoint, neon alley, rice field, snowy landscape, subway, university campus, waterfall alongside the original 16.

**Camera angles (13), DOF/background (9), compositions (12):** Angles add worm's eye, ground level, POV, and from-behind. DOF adds bokeh light orbs, motion-blur background, blurred foreground framing, and clean studio background. Composition adds diagonal lines, fill-the-frame, reflection/mirror, and layered depth.

**Look-at-camera checkbox:** Independent of pose — appends `"looking directly at the camera with engaging eye contact"` to any selected pose. Located below the pose selectbox.

**Target AI Platform (sidebar):** Universal (Gemini · Imagen) / Midjourney / Stable Diffusion. Controls output formatting at generate time: Midjourney gets `--ar {ratio}` and the negative prompt is appended inline as `--no {negative}` (no separate negative block shown); other platforms get plain-English `in {ratio} aspect ratio` and the negative prompt shown separately. Raw ratios live in `AR_RATIOS`.

**Random Look button (🎲):** Next to Generate. Its `on_click=randomize_look` callback assigns a random translated label to every style widget key in `RANDOM_WIDGETS` (identity fields — gender, age, ethnicity — are deliberately not randomized), then handles two special cases: hair is drawn from the pool matching the current gender, and the outfit is randomized as either 1–2 fashion presets (garments set to None) **or** explicit top/bottom garments with fabric & color (presets cleared) — never both. Sets `force_generate=True` so the prompt is generated in the same rerun.

**Random Scene button (🎬):** Third button in the row. `randomize_scene()` randomizes only the widgets in `SCENE_RANDOM_WIDGETS` (location, time, lighting, season, picture style, framing, angle, DOF, composition) — subject, outfit and pose stay fixed, for consistent-character variations. Also auto-generates.

**Save / Load Look (Advanced expander):** `st.download_button` exports the current selections as `look.json` mapping widget keys → *option keys* (language-independent, via `PRESET_WIDGETS`). Loading = paste JSON into a text area + "Apply Look" button whose `apply_look_preset()` callback validates each key against its option list (hair additionally against the gender's pool), sets widget labels via `t()`, and auto-generates. Invalid JSON sets `preset_status` = "error" which renders an `st.error`.

**Language-switch state clearing:** Keyed selectboxes store the *translated label* in session state. When the language radio changes, all keys in `LANG_DEPENDENT_WIDGETS` are popped so stale labels can't collide with the new option lists (this resets those widgets to defaults, same as pre-keyed behavior).

**Prompt history:** Each Generate prepends the combined prompt to `st.session_state["prompt_history"]` (consecutive duplicates skipped, capped at 10). Rendered in a `🕘` expander at the bottom via `st.code` (which has a built-in copy icon).

**Download button:** `st.download_button` next to the copy button saves the combined prompt (plus negative prompt for non-Midjourney platforms) as `prompt.txt`. A character/word count caption is shown under the final prompt.

**Copy button:** Uses `streamlit.components.v1.html()` (not `st.markdown`) because Streamlit strips JS event handlers from markdown. Uses `navigator.clipboard.writeText()` with `execCommand('copy')` fallback. Prompt text is escaped via `json.dumps()` for proper JS string escaping inside `<script>` tags (not `html.escape()`, which breaks apostrophes in values like "bird's eye view").

**Sorting convention:** All selectbox/multiselect option lists are sorted A-Z by their English label. This applies to: fashion presets, top garments, bottom garments, fabric, color palette, poses, and appearance options.

## Prompt Generation Sections

The generate block builds these sections (in order), each stored as an editable `st.text_area`:
1. **Technical** — model type + "shot on 35mm lens" (photographic model types only) + quality tags
2. **Subject** — gender, age, ethnicity, body type, appearance, hair, hair color, bangs, expression
3. **Outfit** — fashion presets + top garment (with fabric & color) + bottom garment (with fabric & color) + free text + accessories
4. **Pose** — selected pose + optional look-at-camera
5. **Environment** — location + time of day + season + weather effects
6. **Camera & Lighting** — lighting style + shot framing + camera angle + DOF + composition + picture style
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
