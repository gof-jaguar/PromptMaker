#!/usr/bin/env python3
"""Pre-deploy check for PromptMaker. Run from the repo root:

    python3 scripts/check.py

Pushing to main deploys straight to the live site, so .githooks/pre-push runs
this first (enable once with: git config core.hooksPath .githooks).

Checks: EN/TH key parity, every option key has a label (and prompt text where
needed), themes and culture looks only use real keys, no duplicate labels in
a selectbox, and a headless run of the app in both languages (themes, Random
Look in every style, Random Scene, Photo Set).
"""
import logging
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)
logging.disable(logging.CRITICAL)  # silence Streamlit's bare-mode warnings

errors = []


def check(ok, message):
    if not ok:
        errors.append(message)


from translations import TRANSLATIONS  # noqa: E402
from prompt_values import ENGLISH_VALUES  # noqa: E402

en, th = set(TRANSLATIONS["en"]), set(TRANSLATIONS["th"])
check(en == th, f"EN/TH parity: only EN {sorted(en - th)}, only TH {sorted(th - en)}")

import app  # noqa: E402  (bare mode: Streamlit calls are no-ops)

# Option lists whose keys never reach the prompt through eng()
NO_PROMPT_TEXT = ("lcat_", "pc_", "oscat_", "rs_", "gg_", "om_", "pl_", "soc_", "fsg_")
for name, keys in vars(app).items():
    if not (name.endswith("_KEYS") and isinstance(keys, list)):
        continue
    check(len(keys) == len(set(keys)), f"{name}: duplicate keys")
    for k in keys:
        check(k in en, f"{name}: '{k}' has no translation")
        if not k.startswith(NO_PROMPT_TEXT):
            check(k in ENGLISH_VALUES, f"{name}: '{k}' has no ENGLISH_VALUES entry")
    for lang in ("en", "th"):
        labels = [TRANSLATIONS[lang].get(k, k) for k in keys]
        dupes = sorted({l for l in labels if labels.count(l) > 1})
        check(not dupes, f"{name}: duplicate {lang} labels {dupes}")

# Grouped lists: every option carries its group's emoji, and the defaults the
# UI relies on (index 1 / index 2) still point at the intended option
for name in ("HR_KEYS", "HC_KEYS", "EX_KEYS", "FS_KEYS", "TD_KEYS", "LT_KEYS",
             "PS_KEYS", "SF_KEYS", "PO_KEYS", "LO_KEYS"):
    missing = [k for k in getattr(app, name) if k not in app.OPTION_EMOJI
               and not k.endswith("_none")]
    check(not missing, f"{name}: no group emoji for {missing}")
for name, index, expected in (("HR_KEYS_WOMEN", 1, "hair_long"), ("HR_KEYS_MEN", 1, "hair_short"),
                              ("HC_KEYS", 1, "hc_black"), ("EX_KEYS", 1, "expr_smile"),
                              ("LO_KEYS", 1, "loc_studio"), ("LT_KEYS", 1, "lit_natural"),
                              ("SF_KEYS", 2, "sf_closeup")):
    check(getattr(app, name)[index] == expected, f"{name}[{index}] should be {expected}")

from prompt_values import COMPACT_VALUES, SHORT_VALUES  # noqa: E402

for name, table in (("COMPACT_VALUES", COMPACT_VALUES), ("SHORT_VALUES", SHORT_VALUES)):
    for k, v in table.items():
        check(k in ENGLISH_VALUES, f"{name}: unknown key '{k}'")
        check(len(v) < len(ENGLISH_VALUES.get(k, "")), f"{name}: '{k}' is not shorter")

options = {**app.PRESET_WIDGETS, **app.MULTI_WIDGETS}
for theme_key, preset in app.THEME_PRESETS.items():
    check(theme_key in en, f"theme '{theme_key}' has no translation")
    for wk, val in preset.items():
        for v in (val if isinstance(val, list) else [val]):
            check(wk in options and v in options[wk], f"{theme_key}: bad {wk}={v}")

for culture, look in app.CULTURE_LOOKS.items():
    for field, pool in (("sets_f", app.OSET_KEYS), ("sets_m", app.OSET_KEYS),
                        ("locs", app.LO_KEYS), ("hair", app.HR_KEYS),
                        ("poses", app.PO_KEYS)):
        for k in look[field]:
            check(k in pool, f"culture {culture}: bad {field} key '{k}'")
for wk, pool in app.CULTURE_POOLS.items():
    for k in pool:
        check(k in options[wk], f"CULTURE_POOLS: bad {wk} key '{k}'")
for prefix in app.OSCAT_PREFIXES.values():
    check(any(k.startswith(prefix) for k in app.OSET_KEYS), f"no sets for '{prefix}'")
check(all(k.startswith(tuple(app.OSCAT_PREFIXES.values())) for k in app.OSET_KEYS[1:]),
      "an outfit set key has no category prefix")

# ── Headless run in both languages ──
from streamlit.testing.v1 import AppTest  # noqa: E402


def run_ok(at, what):
    check(not at.exception, f"{what}: {[e.value for e in at.exception]}")
    return not at.exception


def widget(items, key):
    return next(w for w in items if w.key == key)


for lang_index, lang in enumerate(("en", "th")):
    at = AppTest.from_file("app.py", default_timeout=120).run()
    if lang_index:
        radio = at.sidebar.radio[0]
        radio.set_value(radio.options[lang_index]).run()
    if not run_ok(at, f"[{lang}] first load"):
        continue
    tr = TRANSLATIONS[lang]

    def click(label_key, sidebar=False):
        pool = at.sidebar.button if sidebar else at.button
        next(b for b in pool if tr[label_key] in b.label).click().run()

    for theme_label in list(widget(at.selectbox, "w_theme").options):
        widget(at.selectbox, "w_theme").select(theme_label).run()
        click("apply_theme_btn", sidebar=True)
        run_ok(at, f"[{lang}] theme {theme_label}")
    for style_label in list(widget(at.selectbox, "w_random_style").options):
        widget(at.selectbox, "w_random_style").select(style_label).run()
        for _ in range(4):
            click("random_btn")
            if not run_ok(at, f"[{lang}] Random Look ({style_label})"):
                break
    click("random_scene_btn")
    run_ok(at, f"[{lang}] Random Scene")
    click("photo_set_btn")
    run_ok(at, f"[{lang}] Photo Set")
    check(len(at.session_state["photo_set_prompts"]) == app.PHOTO_SET_SIZE,
          f"[{lang}] Photo Set size")
    click("generate_btn")
    run_ok(at, f"[{lang}] Generate")
    check(bool(at.session_state["prompt_history"]), f"[{lang}] no prompt generated")
    # Simple mode (on by default): each mirror picker must write through to
    # the real widget, a category picker must narrow its list, and the outfit
    # picker must switch to a ready-made set
    for real_key, keys in (("w_hair", app.HR_KEYS_WOMEN), ("w_location", app.LO_KEYS),
                           ("w_pose", app.PO_KEYS), ("w_framing", app.SF_KEYS)):
        widget(at.selectbox, f"sm_{real_key}").select(tr[keys[-1]]).run()
        run_ok(at, f"[{lang}] simple picker {real_key}")
        check(at.session_state[real_key] == tr[keys[-1]],
              f"[{lang}] simple picker {real_key} did not reach the real widget")
    for cat_widget, cat, item_widget, pool in (
            ("w_pose_cat", "pc_daily", "w_pose", app.pose_keys_for_category("pc_daily")),
            ("w_loc_cat", "lcat_thai", "w_location", app.loc_keys_for_category("lcat_thai"))):
        widget(at.selectbox, f"sm_{cat_widget}").select(tr[cat]).run()
        run_ok(at, f"[{lang}] simple category {cat}")
        check(at.session_state[cat_widget] == tr[cat], f"[{lang}] {cat} did not reach {cat_widget}")
        shown = widget(at.selectbox, f"sm_{item_widget}")
        check(len(shown.options) == len(pool), f"[{lang}] {cat}: list not narrowed")
        check(at.session_state[item_widget] in [tr[k] for k in pool],
              f"[{lang}] {cat}: {item_widget} is outside the category")
        shown.select(tr[pool[-1]]).run()
        check(at.session_state[item_widget] == tr[pool[-1]],
              f"[{lang}] {cat}: pick did not reach {item_widget}")
    widget(at.selectbox, "sm_outfit_cat").select(tr["fsg_sport"]).run()
    run_ok(at, f"[{lang}] simple outfit type")
    outfit = widget(at.selectbox, "sm_outfit")
    check(len(outfit.options) == len(app.FS_GROUPS["fsg_sport"]) + 1,
          f"[{lang}] simple outfit type did not narrow the list")
    outfit.select(tr["fs_tennis"]).run()
    check(at.session_state["fashion_multi"] == [tr["fs_tennis"]],
          f"[{lang}] simple outfit did not select the style")
    widget(at.selectbox, "sm_outfit_cat").select(tr["oscat_men"]).run()
    run_ok(at, f"[{lang}] simple outfit type change")
    check(at.session_state["fashion_multi"] == [], f"[{lang}] old outfit kept after type change")
    last_set = app.OSET_KEYS[-1]
    widget(at.selectbox, "sm_outfit_cat").select(tr["soc_all"]).run()
    widget(at.selectbox, "sm_outfit").select(tr[last_set]).run()
    run_ok(at, f"[{lang}] simple outfit")
    check(at.session_state["w_outfit_set"] == tr[last_set],
          f"[{lang}] simple outfit did not select the set")
    click("reset_all")
    run_ok(at, f"[{lang}] Reset all")
    click("generate_btn")
    at.toggle[0].set_value(False).run()
    run_ok(at, f"[{lang}] full mode")
    # Prompt length: same selections must give Short <= Standard <= Detailed,
    # with no empty ", ," gaps left by dropped parts
    lengths = []
    for mode in app.PL_KEYS:
        widget(at.selectbox, "w_prompt_len").select(tr[mode]).run()
        run_ok(at, f"[{lang}] prompt length {mode}")
        prompt = at.session_state["prompt_history"][0]
        check(", ," not in prompt and ",," not in prompt, f"[{lang}] {mode}: empty gap in prompt")
        lengths.append(len(prompt))
    check(lengths == sorted(lengths), f"[{lang}] prompt lengths not ordered: {lengths}")

if errors:
    print(f"FAILED — {len(errors)} problem(s):")
    for e in errors:
        print("  ✗", e)
    sys.exit(1)
print(f"OK — {len(en)} translation keys in parity, {len(app.LO_KEYS) - 1} locations, "
      f"{len(app.PO_KEYS) - 1} poses, {len(app.OSET_KEYS) - 1} outfit sets, "
      f"{len(app.THEME_PRESETS)} themes; headless run passed in EN and TH.")
