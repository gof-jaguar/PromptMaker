# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Run Command

```bash
python3 -m streamlit run app.py
```

No build step, no environment variables, no API keys required. Single dependency: `streamlit>=1.30.0`.

Deployed on Streamlit Cloud — pushing to `main` on GitHub auto-deploys to https://promptmaker.streamlit.app/.

## Architecture

Single-file Streamlit app (`app.py`, ~1770 lines) structured in 6 sequential sections:

1. **TRANSLATIONS** — Bilingual dictionary (EN/TH) with 373 keys. Every UI string goes through `t(key)` helper.
2. **ENGLISH_VALUES** — Maps option keys to English prompt text for AI output (e.g. `"hair_long"` → `"long flowing hair"`). Dropdown/selectbox options that affect the generated prompt need entries here.
3. **HELPERS** — `t()` for translation, `eng()` for prompt values, `make_option()` for selectbox pairs, `translate_to_english()` for Thai→English with a mini dictionary.
4. **CSS** — Injected via `st.markdown(unsafe_allow_html=True)`. Responsive breakpoints at 768px (mobile) and 1400px (desktop). Uses Noto Sans Thai font.
5. **MAIN UI** — 4 expanders (Subject, Outfit, Scene, Advanced) + sidebar (language, aspect ratio, model type).
6. **GENERATE + OUTPUT** — Builds 7 prompt sections, stores in `st.session_state` with `ta_*` keys for editable text areas, combines into final prompt.

## Key Patterns

**Adding a new dropdown/selectbox option** (e.g. a new hair style):
1. Add key to `TRANSLATIONS["en"]` and `TRANSLATIONS["th"]`
2. Add English prompt text to `ENGLISH_VALUES`
3. Add key to the relevant `*_keys` list in the UI section
4. If it affects prompt generation, update the corresponding section in the generate block

**Adding a new checkbox option** (e.g. a new accessory or weather effect):
1. Add key to both `TRANSLATIONS` dicts
2. Add English prompt text to `ENGLISH_VALUES` (for accessories) or handle inline in the generate block (for weather effects)
3. Add the `st.checkbox()` call in the UI section
4. Wire it into the prompt generation logic

**Translation system:** `t(key)` reads `st.session_state["lang"]` ("en"/"th") and returns the translated label. `eng(key)` always returns the English prompt value regardless of UI language.

**Session state for editable output:** When "Generate" is clicked, sections are stored as `st.session_state["ta_technical"]`, `["ta_subject"]`, etc. These keys are bound directly to `st.text_area(key=...)` widgets so users can edit sections inline. The combined prompt rebuilds from current widget values on every rerun.

**Thai text handling:** `translate_to_english()` detects Thai characters (Unicode `\u0e00`–`\u0e7f`), applies a ~50-entry mini dictionary for common fashion/location terms, and wraps any remaining Thai in parentheses.

**Reference photos:** No file upload — checkboxes toggle prompt instructions like "matching the provided reference photo exactly" and show reminder notes in the output.

**Scene location modes:** Three radio options — preset list, free-text description, or real place/travel (landmark + city + country fields). The real place mode builds location strings like `"at Eiffel Tower, Paris, France"`.

**Weather effects:** Three checkboxes (rain, snow, autumn leaves) under the Season selector. These append weather text to the environment section during prompt generation.

**Picture style:** Dropdown in the Scene & Lighting expander with styles like dreamy, cinematic, B&W, etc. Appended to the camera/lighting section in the generated prompt.

**Outfit top/bottom garments:** Two selectboxes (Top and Bottom) in the Outfit expander between fashion presets and free-text input. Values are appended to `outfit_parts` in the generate block via `eng(top_key)` and `eng(bot_key)`.

**Hair styles grouping:** Hair styles are ordered women's first (18 styles), then men's (8 styles) in both TRANSLATIONS and the UI `hr_keys` list. Comments in the code mark the grouping boundaries.

**Bangs selectbox:** Independent of hairstyle — users can combine any hairstyle with any bangs type (none, straight, side, curtain, wispy, micro). In the generate block, bangs text is inserted between hair color and expression: `with {hair}, {color}, {bangs}, and {expression}`. When "None" is selected, the bangs part is omitted entirely.

**Copy button:** Uses `streamlit.components.v1.html()` (not `st.markdown`) because Streamlit strips JS event handlers from markdown. Uses `navigator.clipboard.writeText()` with `execCommand('copy')` fallback. Prompt text is escaped via `html.escape()`.

## Prompt Generation Sections

The generate block builds these sections (in order), each stored as an editable `st.text_area`:
1. **Technical** — model type + quality tags
2. **Subject** — gender, age, ethnicity, body type, appearance, hair, hair color, bangs, expression
3. **Outfit** — fashion presets + top/bottom garments + free text + fabric + color palette + accessories
4. **Pose** — selected pose
5. **Environment** — location + time of day + season + weather effects
6. **Camera & Lighting** — lighting style + shot framing + camera angle + DOF + composition + picture style
7. **Custom** — free-text additions

Plus aspect ratio appended at the end and negative prompt shown separately.

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
