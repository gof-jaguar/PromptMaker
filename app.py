"""
=============================================================================
 Advanced AI Image Prompt Generator — Bilingual (Thai / English)
 Responsive design: iPhone · Android · iPad · Mac · PC
 v5.0 — More styles: model types, hair, expressions, outfits, scenes, poses
=============================================================================
 Run    : streamlit run app.py
=============================================================================
"""

import html as html_mod
import json
import random
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# ── Page Config ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Prompt Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="auto",
)

# ═══════════════════════════════════════════════════════════════════════════
#  1. TRANSLATION DICTIONARY
# ═══════════════════════════════════════════════════════════════════════════

from translations import TRANSLATIONS  # UI strings (EN/TH) live in translations.py

# ═══════════════════════════════════════════════════════════════════════════
#  2. ENGLISH-VALUE LOOKUP
# ═══════════════════════════════════════════════════════════════════════════

from prompt_values import (  # English prompt text lives in prompt_values.py
    ENGLISH_VALUES, COMPACT_VALUES, COMPACT_STRIP_SUFFIXES,
    SHORT_VALUES, SHORT_DROP_PREFIXES, SHORT_CUTS)


# ═══════════════════════════════════════════════════════════════════════════
#  3. HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def t(key: str) -> str:
    lang = st.session_state.get("lang", "en")
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

# Prompt length (sidebar). The chosen option key is mirrored into
# "prompt_len_key" so the choice survives a language switch.
PL_KEYS = ["pl_short", "pl_standard", "pl_detailed"]


def prompt_len() -> str:
    return st.session_state.get("prompt_len_key", "pl_standard")


def eng(key: str) -> str:
    """English prompt text for an option key, worded for the selected prompt
    length: Detailed = ENGLISH_VALUES as written; Standard = tighter wording
    (COMPACT_VALUES) with default settings left unsaid; Short = essentials."""
    full = ENGLISH_VALUES.get(key, "")
    mode = prompt_len()
    if not full or mode == "pl_detailed":
        return full
    short = mode == "pl_short"
    if short and key.startswith(SHORT_DROP_PREFIXES):
        return ""
    if short and key in SHORT_VALUES:
        return SHORT_VALUES[key]
    val = COMPACT_VALUES.get(key, full)
    for prefix, suffix in COMPACT_STRIP_SUFFIXES.items():
        if key.startswith(prefix) and val.endswith(suffix):
            val = val[:-len(suffix)]
    if short:
        for prefix, sep in SHORT_CUTS.items():
            if key.startswith(prefix):
                val = val.split(sep)[0]
    return val


def request_generate():
    """Widget callback: rebuild the prompt in this rerun."""
    st.session_state["force_generate"] = True

def look_desc(hr_k, hc_k, bn_k=None, ex_k=None, mu_k=None, hf_k=None):
    """Hair/bangs/expression/makeup description for one person.

    Any "None / Not specified" pick maps to an empty English value and is
    skipped, so the phrase stays grammatical no matter what is unset.
    """
    hair_bits = [b for b in (eng(hr_k), eng(hc_k), eng(hf_k) if hf_k else "") if b]
    parts = []
    if hair_bits:
        parts.append("with " + ", ".join(hair_bits))
    for k in (bn_k, ex_k, mu_k):
        v = eng(k) if k else ""
        if v:
            parts.append(v)
    return ", ".join(parts)

def make_option(keys):
    return [t(k) for k in keys], keys

def translate_to_english(text: str) -> str:
    thai_chars = sum(1 for c in text if "\u0e00" <= c <= "\u0e7f")
    if thai_chars == 0:
        return text.strip()
    mini_dict = {
        "ชุดนักเรียนญี่ปุ่น": "Japanese school uniform", "ชุดนักเรียน": "school uniform",
        "เสื้อครอป": "crop top", "กระโปรงสั้น": "mini skirt", "กระโปรงยาว": "long skirt",
        "เดรสราตรี": "evening gown", "เดรสยาว": "long flowing dress", "เดรส": "dress",
        "ชุดว่ายน้ำ": "swimsuit", "บิกินี่": "bikini", "ชุดกิโมโน": "kimono",
        "ชุดไทย": "traditional Thai costume", "ชุดฮันบก": "Korean hanbok",
        "เสื้อเชิ้ต": "button-up shirt", "เสื้อยืด": "t-shirt", "กางเกงยีนส์": "jeans",
        "ชุดสูท": "formal suit", "สูท": "suit", "ชุดแต่งงาน": "wedding dress",
        "เสื้อกันหนาว": "sweater", "แจ็คเก็ต": "jacket",
        "โบว์สีแดง": "red ribbon bow", "โบว์": "ribbon bow",
        "ถุงน่อง": "stockings", "รองเท้าส้นสูง": "high heels", "รองเท้าผ้าใบ": "sneakers",
        "สีขาว": "white", "สีดำ": "black", "สีแดง": "red", "สีชมพู": "pink",
        "สีน้ำเงิน": "blue", "สีเขียว": "green", "สีทอง": "gold", "สีเงิน": "silver",
        "ผมยาว": "long hair", "ผมสั้น": "short hair",
        "โบเก้": "bokeh", "หลังเบลอ": "blurred background",
        "ความชัดลึกตื้น": "shallow depth of field", "โทนภาพยนตร์": "cinematic color grading",
        "ดอกไม้": "flowers", "ฝน": "rain", "หิมะ": "snow", "แสงแดด": "sunlight",
        "พระอาทิตย์ตก": "sunset", "ผูกโบว์สีแดง": "with red ribbon bow",
        "ถนนในโตเกียว": "Tokyo street", "ตอนกลางคืน": "at night",
        "ป้ายนีออน": "neon signs", "พื้นเปียกฝน": "wet rainy pavement",
        "ซากุระ": "cherry blossoms", "ทุ่งลาเวนเดอร์": "lavender field",
        "สวนญี่ปุ่น": "Japanese garden", "วัดไทย": "Thai temple",
        "ตลาดกลางคืน": "night market", "ห้องนั่งเล่น": "living room",
        "ระเบียง": "balcony", "สระว่ายน้ำ": "swimming pool",
        "หมวก": "hat", "ผ้าพันคอ": "scarf",
    }
    result = text.strip()
    for th, en_val in sorted(mini_dict.items(), key=lambda x: -len(x[0])):
        result = result.replace(th, en_val)
    remaining = sum(1 for c in result if "\u0e00" <= c <= "\u0e7f")
    if remaining > 0:
        result = f"({result})"
    return result


# ═══════════════════════════════════════════════════════════════════════════
#  3.5 OPTION KEY LISTS + RANDOMIZER
# ═══════════════════════════════════════════════════════════════════════════

# Raw ratio per aspect key — formatted per target platform at generate time
AR_RATIOS = {
    "ar_1_1": "1:1", "ar_16_9": "16:9", "ar_9_16": "9:16", "ar_4_5": "4:5",
    "ar_3_2": "3:2", "ar_2_3": "2:3", "ar_4_3": "4:3", "ar_3_4": "3:4",
    "ar_iphone": "1179:2556", "ar_android": "1080:2400",
}

MT_KEYS = ["model_realistic", "model_cinematic", "model_film", "model_fashion",
           "model_anime", "model_digital_painting", "model_watercolor",
           "model_comic", "model_3d"]
# Model types that are photographic — these get the lens spec
PHOTO_MODEL_KEYS = {"model_realistic", "model_cinematic", "model_film", "model_fashion"}
LENS_KEYS = ["lens_24", "lens_35", "lens_50", "lens_85", "lens_135"]
GD_KEYS = ["gender_female", "gender_male", "gender_nb"]
# Group gender mix (only shown for Group shots)
GM_KEYS = ["gg_same", "gg_mixed"]
AG_KEYS = ["age_none", "age_20_25", "age_5_9", "age_10_14", "age_15_19",
           "age_26_35", "age_36_45", "age_46_60", "age_60plus"]
ET_KEYS = ["eth_none", "eth_asian", "eth_se_asian", "eth_south_asian", "eth_european",
           "eth_african", "eth_latin", "eth_middle_east", "eth_mixed"]
NS_KEYS = ["ns_solo", "ns_duo", "ns_trio", "ns_group"]
# Companion animal (None-first, A-Z) — appended to the subject section
PET_KEYS = ["pet_none", "pet_bird", "pet_butterflies", "pet_cat", "pet_dog",
            "pet_kitten", "pet_puppy", "pet_rabbit"]
# Hairstyles are grouped (long → short → tied → braids → traditional); the
# groups only show as an emoji in front of each option (see OPTION_EMOJI).
HAIR_GROUPS_WOMEN = {
    "hg_long": ["hair_long", "hair_straight", "hair_loose_waves", "hair_wavy",
                "hair_beach_waves", "hair_mermaid", "hair_hollywood", "hair_scurl",
                "hair_curly", "hair_afro", "hair_layered", "hair_butterfly",
                "hair_hush_cut", "hair_hime", "hair_jellyfish", "hair_wet_slick"],
    "hg_short": ["hair_mid_length", "hair_c_curl", "hair_lob", "hair_bob",
                 "hair_french_bob", "hair_wavy_bob", "hair_wolf_cut", "hair_shag",
                 "hair_pixie"],
    "hg_tied": ["hair_ponytail", "hair_high_ponytail", "hair_low_pony",
                "hair_ribbon_pony", "hair_bubble_pony", "hair_twintails",
                "hair_half_twin", "hair_low_pigtails", "hair_half_up", "hair_half_bun",
                "hair_bun", "hair_messy_bun", "hair_low_bun", "hair_ballerina",
                "hair_space_buns", "hair_claw_clip"],
    "hg_braid": ["hair_braids", "hair_french_braid", "hair_side_braid",
                 "hair_twin_braids", "hair_fishtail", "hair_crown_braid",
                 "hair_box_braids"],
    "hg_trad": ["hair_flower_updo", "hair_thai_chignon", "hair_jp_updo",
                "hair_kr_daenggi", "hair_cn_updo"],
}
HAIR_GROUPS_MEN = {
    "hgm_short": ["hair_short", "hair_buzz", "hair_crew_cut", "hair_ivy", "hair_fade",
                  "hair_textured_crop", "hair_undercut", "hair_side_part", "hair_bald"],
    "hgm_mid": ["hair_middle_part", "hair_two_block", "hair_dandy", "hair_curtain_m",
                "hair_quiff", "hair_slick_back", "hair_perm_m", "hair_curly_fringe",
                "hair_messy_m", "hair_wolf_m", "hair_mullet"],
    "hgm_long": ["hair_long_m", "hair_man_bun", "hair_topknot", "hair_dreads"],
}
HR_KEYS_WOMEN = ["hair_none"] + [k for g in HAIR_GROUPS_WOMEN.values() for k in g]
HR_KEYS_MEN = ["hair_none"] + [k for g in HAIR_GROUPS_MEN.values() for k in g]
# Full list (used for non-binary and as the language-reset superset)
HR_KEYS = HR_KEYS_WOMEN + HR_KEYS_MEN[1:]  # skip duplicate hair_none

def hair_keys_for_gender(gd_key: str):
    """Hairstyle option pool filtered by the selected gender."""
    if gd_key == "gender_female":
        return HR_KEYS_WOMEN
    if gd_key == "gender_male":
        return HR_KEYS_MEN
    return HR_KEYS
# Hair color: natural dark → blonde & light → red → fashion → multi-tone
HC_GROUPS = {
    "hcg_dark": ["hc_black", "hc_blue_black", "hc_dark_brown", "hc_chocolate",
                 "hc_ash_brown", "hc_milk_tea", "hc_caramel", "hc_light_brown"],
    "hcg_light": ["hc_honey_blonde", "hc_blonde", "hc_ash_blonde", "hc_strawberry",
                  "hc_platinum", "hc_silver", "hc_white", "hc_salt_pepper"],
    "hcg_red": ["hc_copper", "hc_red", "hc_burgundy", "hc_rose_gold"],
    "hcg_fashion": ["hc_pink", "hc_peach", "hc_purple", "hc_blue", "hc_mint"],
    "hcg_multi": ["hc_ombre", "hc_balayage", "hc_highlights", "hc_money_piece",
                  "hc_peekaboo", "hc_split"],
}
HC_KEYS = ["hc_none"] + [k for g in HC_GROUPS.values() for k in g]
BN_KEYS = ["bangs_none", "bangs_straight", "bangs_see_through", "bangs_side",
           "bangs_curtain", "bangs_wispy", "bangs_micro", "bangs_hime"]
# Expressions: happy → cute & playful → calm → cool & bold → moody
EX_GROUPS = {
    "exg_happy": ["expr_smile", "expr_bright_smile", "expr_grin", "expr_laugh",
                  "expr_candid_laugh", "expr_giggle", "expr_excited"],
    "exg_cute": ["expr_wink", "expr_tongue", "expr_pout", "expr_puff", "expr_kiss",
                 "expr_doe_eyes", "expr_playful", "expr_shy", "expr_blush",
                 "expr_sleepy", "expr_curious"],
    "exg_calm": ["expr_soft_gaze", "expr_lips_parted", "expr_neutral", "expr_peaceful",
                 "expr_eyes_closed", "expr_dreamy", "expr_pensive", "expr_longing"],
    "exg_cool": ["expr_confident", "expr_smirk", "expr_brow_raise", "expr_fierce",
                 "expr_cold", "expr_serious", "expr_determined", "expr_sultry"],
    "exg_moody": ["expr_surprised", "expr_bored", "expr_sulky", "expr_sad",
                  "expr_tearful"],
}
EX_KEYS = ["expr_none"] + [k for g in EX_GROUPS.values() for k in g]
BT_KEYS = ["bt_none", "bt_slim", "bt_petite", "bt_lean", "bt_athletic",
           "bt_hourglass", "bt_curvy", "bt_tall", "bt_average"]
AP_KEYS = ["app_none", "app_beautiful", "app_cpop", "app_charming", "app_chic",
           "app_cool", "app_cute", "app_doll", "app_elegant",
           "app_fierce", "app_girl_next_door", "app_handsome",
           "app_jpop", "app_kpop", "app_natural", "app_sweet", "app_youthful"]
MU_KEYS = ["mu_none", "mu_red_lip", "mu_douyin", "mu_editorial", "mu_freckles",
           "mu_glam", "mu_goth", "mu_gradient", "mu_igari", "mu_dewy",
           "mu_natural", "mu_no_makeup", "mu_smoky", "mu_soft_matte",
           "mu_bronzed", "mu_glitter"]
# Fashion styles by group (A-Z inside each group)
FS_GROUPS = {
    "fsg_daily": ["fs_casual", "fs_minimalist", "fs_korean", "fs_streetwear",
                  "fs_smart_casual", "fs_office", "fs_suit", "fs_elegant",
                  "fs_date_night", "fs_cozy", "fs_all_black", "fs_all_white",
                  "fs_denim", "fs_tomboy", "fs_cityboy", "fs_resort", "fs_vintage",
                  "fs_preppy", "fs_teen"],
    "fsg_trend": ["fs_clean_girl", "fs_old_money", "fs_coquette", "fs_cottagecore",
                  "fs_soft_girl", "fs_fairycore", "fs_y2k", "fs_acubi",
                  "fs_office_siren", "fs_blokette", "fs_dark_academia",
                  "fs_light_academia", "fs_parisian", "fs_barbiecore", "fs_bohemian",
                  "fs_japanese", "fs_grunge", "fs_gothic", "fs_egirl", "fs_rockstar",
                  "fs_biker", "fs_racing", "fs_skater", "fs_gorpcore", "fs_cyberpunk",
                  "fs_western"],
    "fsg_event": ["fs_idol_stage", "fs_festival", "fs_dance", "fs_evening",
                  "fs_wedding", "fs_school", "fs_cheer"],
    "fsg_sport": ["fs_athleisure", "fs_yoga", "fs_tennis", "fs_golf", "fs_basketball",
                  "fs_ski", "fs_bikini", "fs_one_piece", "fs_beach_cover", "fs_swim_m"],
    "fsg_trad": ["fs_thai", "fs_kimono", "fs_yukata", "fs_hanbok", "fs_hanfu",
                 "fs_ao_dai", "fs_saree"],
}
for _keys in FS_GROUPS.values():
    _keys.sort(key=lambda k: TRANSLATIONS["en"][k].lower())
FS_KEYS = [k for g in FS_GROUPS.values() for k in g]
FB_KEYS = ["fab_none", "fab_chiffon", "fab_corduroy", "fab_cotton", "fab_crochet",
           "fab_denim", "fab_knit", "fab_jersey", "fab_lace", "fab_leather",
           "fab_linen", "fab_organza", "fab_satin", "fab_sequin", "fab_sheer",
           "fab_silk", "fab_tulle", "fab_tweed", "fab_velvet", "fab_wool"]
CP_KEYS = ["col_none", "col_black", "col_baby_blue", "col_beige", "col_blue",
           "col_brown", "col_burgundy", "col_butter", "col_colorblock", "col_cool",
           "col_coral", "col_earthy", "col_gold", "col_green", "col_grey",
           "col_hot_pink", "col_ivory", "col_khaki", "col_lilac", "col_mint",
           "col_mono", "col_navy", "col_orange", "col_pastel", "col_peach",
           "col_pink", "col_purple", "col_red", "col_sage", "col_silver",
           "col_teal", "col_vibrant", "col_warm", "col_white", "col_yellow"]
TOP_KEYS = ["top_none", "top_blazer", "top_blouse", "top_bodysuit",
            "top_bomber", "top_bralette", "top_button_shirt", "top_camisole",
            "top_cardigan", "top_corset", "top_crop", "top_denim_jacket",
            "top_halter", "top_hoodie", "top_knit_vest", "top_leather_jacket",
            "top_long_sleeve", "top_off_shoulder", "top_oversized_shirt",
            "top_polo", "top_puff_sleeve", "top_puffer", "top_sports_bra",
            "top_sweater", "top_sweatshirt", "top_tshirt", "top_tank",
            "top_trench", "top_tube", "top_turtleneck", "top_varsity",
            "top_wrap"]
BOT_KEYS = ["bot_none", "bot_a_line", "bot_baggy", "bot_bike_shorts",
            "bot_cargo", "bot_cargo_skirt", "bot_culottes",
            "bot_denim_shorts", "bot_denim_skirt", "bot_flare", "bot_jeans",
            "bot_joggers", "bot_leggings", "bot_maxi_skirt", "bot_midi_skirt",
            "bot_mini_skirt", "bot_overalls", "bot_palazzo", "bot_parachute",
            "bot_pencil_skirt", "bot_pleated_skirt", "bot_ripped",
            "bot_slip_skirt", "bot_shorts", "bot_skort", "bot_sweatpants",
            "bot_trousers", "bot_tennis_skirt", "bot_tulle_skirt",
            "bot_wide_leg", "bot_yoga"]
SH_KEYS = ["sh_none", "sh_ankle_boots", "sh_ballet", "sh_barefoot",
           "sh_chelsea", "sh_chunky", "sh_combat", "sh_cowboy",
           "sh_espadrilles", "sh_flip_flops", "sh_heels", "sh_kitten_heels",
           "sh_knee_boots", "sh_loafers", "sh_mary_janes", "sh_mules",
           "sh_oxford", "sh_platform", "sh_running", "sh_sandals",
           "sh_sneakers"]
# Location categories (first-level picker). Every location belongs to exactly
# one category; LO_KEYS is derived from this map.
LCAT_KEYS = ["lcat_all", "lcat_indoor", "lcat_home", "lcat_city", "lcat_shops",
            "lcat_nature", "lcat_water", "lcat_luxury", "lcat_travel", "lcat_thai",
            "lcat_asia", "lcat_leisure", "lcat_fantasy"]
LOC_CATEGORIES = {
    "lcat_indoor": [
            "loc_art_gallery", "loc_dance_studio", "loc_library", "loc_studio",
            "loc_classroom", "loc_white_studio", "loc_color_backdrop", "loc_elevator",
            "loc_parking", "loc_office", "loc_stage", "loc_backstage"],
    "lcat_home": [
            "loc_balcony", "loc_bedroom", "loc_kitchen", "loc_living", "loc_vanity",
            "loc_window_seat", "loc_desk", "loc_closet", "loc_backyard"],
    "lcat_city": [
            "loc_bridge", "loc_bus_stop", "loc_crosswalk", "loc_neon_alley",
            "loc_night_market", "loc_railway", "loc_rooftop", "loc_shopping", "loc_subway",
            "loc_train", "loc_university", "loc_street", "loc_graffiti", "loc_skywalk",
            "loc_car", "loc_gas_station", "loc_rain_street", "loc_skyline", "loc_bus",
            "loc_subway_car"],
    "lcat_shops": [
            "loc_bookstore", "loc_cafe", "loc_convenience", "loc_boutique",
            "loc_flower_shop", "loc_bakery", "loc_laundromat", "loc_supermarket",
            "loc_record_store", "loc_bar", "loc_thrift", "loc_bubble_tea", "loc_ice_cream",
            "loc_diner", "loc_mall"],
    "lcat_nature": [
            "loc_autumn_park", "loc_cherry", "loc_desert", "loc_flower_field",
            "loc_forest", "loc_garden", "loc_greenhouse", "loc_lavender", "loc_mountain",
            "loc_brick_ruin", "loc_overgrown", "loc_rice_field", "loc_snow",
            "loc_sunflower", "loc_vineyard", "loc_meadow", "loc_tulip", "loc_pampas",
            "loc_pine", "loc_starry_field", "loc_country_road", "loc_aurora"],
    "lcat_water": [
            "loc_beach", "loc_cliff", "loc_harbor", "loc_lake", "loc_pool",
            "loc_lighthouse", "loc_waterfall", "loc_boat", "loc_river", "loc_underwater",
            "loc_infinity_pool", "loc_tropical"],
    "lcat_luxury": [
            "loc_ballroom", "loc_mansion", "loc_fine_dining", "loc_stairs",
            "loc_hotel_lobby", "loc_yacht", "loc_penthouse", "loc_private_jet",
            "loc_sports_car", "loc_opera", "loc_red_carpet"],
    "lcat_travel": [
            "loc_airport", "loc_castle", "loc_old_town", "loc_santorini", "loc_temple",
            "loc_venice", "loc_hoi_an", "loc_bali", "loc_india_palace", "loc_morocco",
            "loc_paris", "loc_nyc", "loc_london", "loc_cappadocia", "loc_swiss",
            "loc_amalfi", "loc_rome", "loc_pyramids", "loc_maldives", "loc_singapore",
            "loc_la"],
    "lcat_thai": [
            "loc_th_rooftop", "loc_th_chiangmai", "loc_th_floating", "loc_th_wat",
            "loc_th_shophouse", "loc_th_tea", "loc_th_island", "loc_th_tuktuk",
            "loc_th_palace", "loc_th_ruins", "loc_th_river_temple", "loc_th_white_temple",
            "loc_th_teak", "loc_th_sala", "loc_th_lotus", "loc_th_lantern",
            "loc_th_krathong", "loc_th_chinatown", "loc_th_canal", "loc_th_street_food",
            "loc_th_rice_terrace", "loc_th_bts", "loc_th_songkran", "loc_th_phuket_old",
            "loc_th_flower_market", "loc_th_fresh_market"],
    "lcat_asia": [
            "loc_bamboo", "loc_kr_hanok", "loc_jp_ryokan", "loc_kr_street", "loc_jp_torii",
            "loc_jp_street", "loc_jp_castle", "loc_jp_zen", "loc_jp_tea_house",
            "loc_jp_gion", "loc_jp_fuji", "loc_jp_izakaya", "loc_jp_shibuya",
            "loc_jp_matsuri", "loc_jp_onsen", "loc_jp_station", "loc_jp_school",
            "loc_kr_palace", "loc_kr_han_river", "loc_kr_pocha", "loc_cn_garden",
            "loc_cn_lantern_street", "loc_cn_water_town", "loc_cn_great_wall",
            "loc_jp_vending", "loc_jp_sakura_river", "loc_jp_snow_village", "loc_kr_cafe",
            "loc_cn_bund", "loc_hk_neon", "loc_tw_jiufen"],
    "lcat_leisure": [
            "loc_amusement", "loc_aquarium", "loc_arcade", "loc_basketball", "loc_gym",
            "loc_ice_rink", "loc_karaoke", "loc_cinema", "loc_photo_booth", "loc_bowling",
            "loc_skatepark", "loc_stadium", "loc_tennis", "loc_carousel", "loc_concert",
            "loc_camp", "loc_picnic", "loc_golf", "loc_ferris", "loc_club", "loc_football"],
    "lcat_fantasy": [
            "loc_clouds", "loc_fairy_forest", "loc_flower_room", "loc_space",
            "loc_cyber_city", "loc_candy", "loc_mirror_room", "loc_balloon_room",
            "loc_ice_palace"],
}
# None, Studio (the default), then category by category, A-Z inside each
LO_KEYS = ["loc_none", "loc_studio"] + [
    k for keys in LOC_CATEGORIES.values()
    for k in sorted(keys, key=lambda k: TRANSLATIONS["en"][k].lower())
    if k != "loc_studio"]


def loc_keys_for_category(lcat_key: str):
    """Location option pool for the selected category (None stays first)."""
    if lcat_key in LOC_CATEGORIES:
        return ["loc_none"] + [k for k in LO_KEYS if k in LOC_CATEGORIES[lcat_key]]
    return LO_KEYS

# Time of day runs chronologically (dawn → night), not A-Z
TD_GROUPS = {
    "tdg_morning": ["tod_dawn", "tod_sunrise", "tod_morning"],
    "tdg_day": ["tod_noon", "tod_afternoon", "tod_overcast"],
    "tdg_evening": ["tod_golden", "tod_sunset", "tod_blue", "tod_dusk"],
    "tdg_night": ["tod_night", "tod_midnight", "tod_starry"],
}
TD_KEYS = ["tod_none"] + [k for g in TD_GROUPS.values() for k in g]
TD_DEFAULT = TD_KEYS.index("tod_golden")
# Lighting: natural light → studio → night & ambient
LT_GROUPS = {
    "ltg_natural": ["lit_natural", "lit_window", "lit_golden", "lit_backlit",
                    "lit_overcast", "lit_open_shade", "lit_hard_sun", "lit_dappled",
                    "lit_blinds", "lit_godrays", "lit_silhouette", "lit_moonlight"],
    "ltg_studio": ["lit_studio", "lit_highkey", "lit_lowkey", "lit_beauty", "lit_ring",
                   "lit_rim", "lit_dramatic", "lit_cinematic", "lit_flash", "lit_gel",
                   "lit_spotlight"],
    "ltg_night": ["lit_neon", "lit_signage", "lit_streetlamp", "lit_headlights",
                  "lit_lamp", "lit_fairy", "lit_lantern", "lit_candle", "lit_bonfire",
                  "lit_fireworks", "lit_screen", "lit_disco"],
}
LT_KEYS = ["lit_none"] + [k for g in LT_GROUPS.values() for k in g]
SN_KEYS = ["season_none", "season_spring", "season_summer",
           "season_autumn", "season_winter", "season_rainy"]
# Picture style: clean & realistic → film & retro → cinematic → dreamy & fantasy
PS_GROUPS = {
    "psg_clean": ["ps_natural", "ps_commercial", "ps_editorial", "ps_bright_airy",
                  "ps_minimal", "ps_soft", "ps_vivid", "ps_documentary", "ps_bw"],
    "psg_film": ["ps_vintage", "ps_nostalgic", "ps_jfilm", "ps_matte", "ps_polaroid",
                 "ps_digicam", "ps_90s", "ps_70s", "ps_vhs"],
    "psg_cine": ["ps_cinematic", "ps_kdrama", "ps_moody", "ps_dark_luxe", "ps_noir",
                 "ps_hk_cinema"],
    "psg_dream": ["ps_dreamy", "ps_glow", "ps_pastel", "ps_storybook", "ps_fantasy",
                  "ps_fairytale", "ps_cyber", "ps_vaporwave", "ps_surreal"],
}
PS_KEYS = ["ps_none"] + [k for g in PS_GROUPS.values() for k in g]
# Framing runs tight → wide (a scale, not A-Z); the detail shot comes last
SF_GROUPS = {
    "sfg_close": ["sf_extreme_cu", "sf_closeup", "sf_medium_cu"],
    "sfg_half": ["sf_medium", "sf_cowboy", "sf_medium_full"],
    "sfg_full": ["sf_full", "sf_ootd"],
    "sfg_wide": ["sf_wide", "sf_extreme_wide"],
    "sfg_detail": ["sf_detail"],
}
SF_KEYS = ["sf_none"] + [k for g in SF_GROUPS.values() for k in g]
# Subject: skin tone (light → dark), face details, skin & hair finish, nails
ST_KEYS = ["st_none", "st_porcelain", "st_fair", "st_light_warm", "st_medium",
           "st_olive", "st_tan", "st_brown", "st_deep"]
FSH_KEYS = ["fsh_none", "fsh_heart", "fsh_sharp", "fsh_oval", "fsh_round",
            "fsh_small", "fsh_v"]
EYE_KEYS = ["eye_none", "eye_almond", "eye_big", "eye_doe", "eye_double",
            "eye_monolid", "eye_droopy", "eye_cat"]
EC_KEYS = ["ec_none", "ec_amber", "ec_black", "ec_blue", "ec_dark_brown",
           "ec_green", "ec_grey", "ec_hazel"]
BROW_KEYS = ["brow_none", "brow_feathery", "brow_arched", "brow_straight",
             "brow_thick", "brow_thin"]
LIP_KEYS = ["lip_none", "lip_cat", "lip_full", "lip_heart", "lip_plump",
            "lip_small", "lip_thin"]
FM_KEYS = ["fm_aegyo", "fm_mole_lip", "fm_dimples", "fm_high_nose", "fm_lashes",
           "fm_mole_eye", "fm_freckles", "fm_rosy", "fm_button_nose", "fm_snaggle"]
FH_KEYS = ["fh_none", "fh_clean", "fh_full_beard", "fh_goatee", "fh_stubble",
           "fh_mustache", "fh_short_beard"]
SKF_KEYS = ["skf_none", "skf_dewy", "skf_porcelain", "skf_glass", "skf_natural",
            "skf_matte", "skf_sunkissed", "skf_real"]
HF_KEYS = ["hf_none", "hf_messy", "hf_strands", "hf_glossy", "hf_sleek",
           "hf_tucked", "hf_voluminous", "hf_wet", "hf_windswept"]
NL_KEYS = ["nl_none", "nl_black", "nl_chrome", "nl_red", "nl_natural", "nl_french",
           "nl_glitter", "nl_long", "nl_nude", "nl_pastel"]
# Lighting direction / color / quality — layered on top of the lighting style
LD_KEYS = ["ld_none", "ld_back", "ld_butterfly", "ld_clamshell", "ld_front",
           "ld_loop", "ld_rembrandt", "ld_side", "ld_split", "ld_top", "ld_under"]
LC_KEYS = ["lc_none", "lc_amber", "lc_cool", "lc_green", "lc_red", "lc_neutral",
           "lc_pink_blue", "lc_purple", "lc_teal_orange", "lc_warm"]
LQ_KEYS = ["lq_none", "lq_hard", "lq_high_contrast", "lq_low_contrast", "lq_soft"]
# Camera: height (high → low) and position around the subject (front → back)
# are spatial scales, so they keep that order instead of A-Z
CH_KEYS = ["ch_none", "ch_aerial", "ch_top", "ch_high", "ch_slight_high", "ch_eye",
           "ch_chest", "ch_waist", "ch_slight_low", "ch_low", "ch_ground",
           "ch_worm"]
CD_KEYS = ["cd_none", "cd_front", "cd_front_3q", "cd_side", "cd_back_3q", "cd_back",
           "cd_over_shoulder"]
# Special shots / perspectives (optional, rarely combined)
CS_KEYS = ["cs_none", "cs_telephoto", "cs_cctv", "cs_dutch", "cs_pov", "cs_fisheye",
           "cs_mirror", "cs_selfie", "cs_through", "cs_window"]
# Camera body / film stock — photographic model types only (technical section)
CF_KEYS = ["cf_none", "cf_digicam", "cf_arri", "cf_canon", "cf_cinestill",
           "cf_disposable", "cf_superia", "cf_fuji", "cf_hasselblad", "cf_ilford",
           "cf_instax", "cf_iphone", "cf_gold", "cf_portra", "cf_leica",
           "cf_polaroid", "cf_sony"]
# Weather & atmosphere (multiselect) and background people
ATM_KEYS = ["atm_puddles", "atm_leaves", "atm_petals", "atm_confetti", "atm_dust",
            "atm_fireflies", "atm_fog", "atm_wind", "atm_sparkles", "atm_rain",
            "atm_smoke", "atm_snow", "atm_bubbles", "atm_steam"]
BGP_KEYS = ["bgp_none", "bgp_few", "bgp_crowd", "bgp_empty"]
# Lens & film effects (multiselect)
LFX_KEYS = ["lfx_chromatic", "lfx_double", "lfx_date", "lfx_grain", "lfx_halation",
            "lfx_flare", "lfx_leak", "lfx_motion", "lfx_prism", "lfx_bloom",
            "lfx_vignette"]
# Old single camera-angle keys (look.json ≤ v5.7) → new camera widget + key
CAM_MIGRATION = {
    "cam_eye": ("w_cam_height", "ch_eye"),
    "cam_low": ("w_cam_height", "ch_low"),
    "cam_worm": ("w_cam_height", "ch_worm"),
    "cam_ground": ("w_cam_height", "ch_ground"),
    "cam_high": ("w_cam_height", "ch_high"),
    "cam_bird": ("w_cam_height", "ch_top"),
    "cam_overhead": ("w_cam_height", "ch_top"),
    "cam_aerial": ("w_cam_height", "ch_aerial"),
    "cam_drone": ("w_cam_height", "ch_aerial"),
    "cam_3q": ("w_cam_dir", "cd_front_3q"),
    "cam_profile": ("w_cam_dir", "cd_side"),
    "cam_over_shoulder": ("w_cam_dir", "cd_over_shoulder"),
    "cam_back": ("w_cam_dir", "cd_back"),
    "cam_selfie": ("w_cam_special", "cs_selfie"),
    "cam_dutch": ("w_cam_special", "cs_dutch"),
    "cam_pov": ("w_cam_special", "cs_pov"),
    "cam_cctv": ("w_cam_special", "cs_cctv"),
    "cam_fisheye": ("w_cam_special", "cs_fisheye"),
}
DOF_KEYS = ["dof_none", "dof_sharp", "dof_portrait", "dof_shallow", "dof_bokeh_lights",
            "dof_motion", "dof_fg_blur", "dof_clean_bg",
            "dof_tiltshift", "dof_soft"]
CMP_KEYS = ["comp_center", "comp_rot_left", "comp_rot_right",
            "comp_golden", "comp_leading", "comp_framed",
            "comp_negative_space", "comp_symmetry", "comp_diagonal",
            "comp_fill", "comp_reflection", "comp_depth"]
# Pose categories (first-level picker). Every pose belongs to exactly one
# category; PO_KEYS is derived from this map: category by category, A-Z inside.
PC_KEYS = ["pc_all", "pc_standing", "pc_walking", "pc_sitting", "pc_kneeling",
          "pc_lying", "pc_crouching", "pc_cute", "pc_social", "pc_daily", "pc_props",
          "pc_sport"]
POSE_CATEGORIES = {
    "pc_standing": [
            "pose_arms_up", "pose_cross_arms", "pose_arms_open", "pose_back_camera",
            "pose_hair_both", "pose_hands_hips", "pose_chin_up", "pose_contrapposto",
            "pose_elegant", "pose_hand_collar", "pose_hand_hair", "pose_hand_hip",
            "pose_hands_back", "pose_arms_behind_head", "pose_hands_pocket",
            "pose_hands_nape", "pose_lean", "pose_railing", "pose_looking_away",
            "pose_over_shoulder", "pose_look_up", "pose_foot_kick", "pose_s_curve",
            "pose_stand", "pose_stretch", "pose_tiptoe", "pose_wall_foot", "pose_doorway",
            "pose_hold_hair_wind", "pose_look_down_smile"],
    "pc_walking": [
            "pose_candid", "pose_carefree_walk", "pose_dance", "pose_hair_flip",
            "pose_jump", "pose_look_back_walk", "pose_run", "pose_runway", "pose_skip",
            "pose_twirl", "pose_walk", "pose_walk_away", "pose_walk_toward",
            "pose_bag_strap", "pose_puddle_hop", "pose_run_laugh", "pose_stairs_down"],
    "pc_sitting": [
            "pose_cross_leg", "pose_hug_knees", "pose_meditate", "pose_sit_side",
            "pose_sit", "pose_sit_chair_back", "pose_sit_floor_cross", "pose_sit_ledge",
            "pose_sit_stairs", "pose_sit_cheek_knee", "pose_legs_extended",
            "pose_sit_knee_up", "pose_w_sit", "pose_sit_bed_edge", "pose_sit_window",
            "pose_sit_table_chin", "pose_sit_floor_lean", "pose_sit_swing"],
    "pc_kneeling": [
            "pose_kneel", "pose_kneel_upright", "pose_kneel_hair", "pose_kneel_look_up",
            "pose_one_knee", "pose_seiza"],
    "pc_lying": [
            "pose_lying", "pose_lie_back_hair", "pose_lie_back_knee", "pose_lie_side",
            "pose_lie_stomach", "pose_lie_arm_pillow", "pose_lie_flowers"],
    "pc_crouching": [
            "pose_bend_knees", "pose_crouch", "pose_crouch_chin", "pose_crouch_look_back",
            "pose_lean_forward", "pose_squat"],
    "pc_cute": [
            "pose_big_heart", "pose_blow_kiss", "pose_bunny_ears", "pose_cat_paw",
            "pose_double_peace", "pose_finger_frame", "pose_finger_heart",
            "pose_fist_cheeks", "pose_flower_chin", "pose_sleeve_smile", "pose_hand_chin",
            "pose_cheek_hands", "pose_head_tilt", "pose_heart_hands", "pose_mini_heart",
            "pose_ok_sign", "pose_peace", "pose_peek_fingers", "pose_salute",
            "pose_please", "pose_point_camera", "pose_poke_cheek", "pose_rawr",
            "pose_shush", "pose_self_hug", "pose_sweater_paws", "pose_thumbs_up",
            "pose_hair_tuck", "pose_wave", "pose_wink", "pose_yawn", "pose_peace_eye",
            "pose_cheek_heart", "pose_finger_gun_chin", "pose_cover_laugh"],
    "pc_social": [
            "pose_fix_jacket", "pose_adjust_glasses", "pose_phone_check", "pose_curtsy",
            "pose_editorial", "pose_high_fashion", "pose_coat_lapels", "pose_skirt_hem",
            "pose_mirror_selfie", "pose_reach_camera", "pose_selfie", "pose_shield_sun",
            "pose_hold_hat", "pose_wai", "pose_bow", "pose_05x", "pose_follow_me",
            "pose_ootd"],
    "pc_daily": [
            "pose_eat", "pose_drink_straw", "pose_ice_cream", "pose_bubble_gum",
            "pose_cook", "pose_laptop", "pose_write", "pose_headphones", "pose_phone_call",
            "pose_shopping", "pose_makeup", "pose_tie_hair", "pose_guitar", "pose_paint",
            "pose_watering", "pose_hug_plush", "pose_rain_hand", "pose_suitcase",
            "pose_sing_mic", "pose_drive"],
    "pc_props": [
            "pose_touch_plants", "pose_bouquet", "pose_coffee", "pose_hold_camera",
            "pose_umbrella", "pose_balloons", "pose_peek_tree", "pose_pick_flower",
            "pose_read_book", "pose_smell_flower", "pose_bicycle", "pose_parasol"],
    "pc_sport": [
            "pose_ballet", "pose_boxing", "pose_dribble", "pose_dynamic",
            "pose_skateboard", "pose_lunge", "pose_tennis_swing", "pose_yoga", "pose_jog",
            "pose_golf_swing", "pose_kpop_dance", "pose_high_kick", "pose_bike_ride",
            "pose_badminton", "pose_football"],
}
PO_KEYS = ["pose_none"] + [
    k for keys in POSE_CATEGORIES.values()
    for k in sorted(keys, key=lambda k: TRANSLATIONS["en"][k].lower())]


def pose_keys_for_category(pc_key: str):
    """Pose option pool for the selected pose category (None stays first)."""
    if pc_key in POSE_CATEGORIES:
        return ["pose_none"] + [k for k in PO_KEYS if k in POSE_CATEGORIES[pc_key]]
    return PO_KEYS

# Pose fine-tuning (all None-first, rest A-Z) — appended after the pose
BD_KEYS = ["dir_none", "dir_back", "dir_back_look", "dir_front", "dir_side",
           "dir_slight", "dir_3q"]
HD_KEYS = ["head_none", "head_chin_down", "head_chin_up", "head_shoulder",
           "head_rest_hand", "head_back", "head_tilt", "head_turned"]
GZ_KEYS = ["gaze_none", "gaze_closed", "gaze_camera", "gaze_down", "gaze_away",
           "gaze_upward_glance", "gaze_up", "gaze_side_glance"]
HA_KEYS = ["hands_none", "hands_crossed", "hands_overhead", "hands_relaxed",
           "hands_both_hips", "hands_lips", "hands_hair", "hands_hip", "hands_neck",
           "hands_face", "hands_behind", "hands_clasped", "hands_pockets",
           "hands_strap", "hands_sleeve"]
LG_KEYS = ["legs_none", "legs_ankles_crossed", "legs_kick_back", "legs_knees_in",
           "legs_crossed_knee", "legs_cross_stand", "legs_extended",
           "legs_together", "legs_mid_stride", "legs_tiptoe", "legs_knee_bent",
           "legs_wide"]
PE_KEYS = ["pe_none", "pe_candid", "pe_confident", "pe_cool", "pe_dynamic",
           "pe_elegant", "pe_playful", "pe_relaxed", "pe_shy"]
# Outfit layers: dress / one-piece garments (outfit type "Dress")
DR_KEYS = ["dress_none", "dress_babydoll", "dress_ballgown", "dress_bodycon",
           "dress_corset", "dress_jumpsuit", "dress_knit", "dress_maxi",
           "dress_midi", "dress_mini", "dress_off_shoulder", "dress_pinafore",
           "dress_qipao", "dress_romper", "dress_shirt", "dress_slip",
           "dress_sundress", "dress_tea", "dress_tiered", "dress_wrap"]
# Outer layer worn over the top or dress — noun phrases, prompt adds "layered with"
OUT_KEYS = ["out_none", "out_blazer", "out_bolero", "out_cape", "out_cardigan",
            "out_cropped_cardigan", "out_denim_jacket", "out_faux_fur",
            "out_kimono", "out_leather", "out_wool_coat", "out_open_shirt",
            "out_puffer", "out_shawl", "out_trench", "out_tweed", "out_varsity",
            "out_zip_hoodie"]
FIT_KEYS = ["fit_none", "fit_aline", "fit_body", "fit_cropped", "fit_fitted",
            "fit_flowy", "fit_layered", "fit_oversized", "fit_relaxed",
            "fit_tailored"]
LEG_KEYS = ["leg_none", "leg_ankle", "leg_crew", "leg_fishnet", "leg_frilly",
            "leg_knee", "leg_warmers", "leg_loose", "leg_opaque", "leg_patterned",
            "leg_sheer_black", "leg_nude", "leg_thigh", "leg_white_tights"]
# Design details & prints (multiselect, A-Z, no None)
DET_KEYS = ["det_corset", "det_embroidery", "det_floral", "det_gingham",
            "det_lace_trim", "det_off_shoulder", "det_buttons", "det_collar",
            "det_checks", "det_pleats", "det_polka", "det_puff", "det_bows",
            "det_frills", "det_sailor", "det_sequins", "det_sheer_sleeves",
            "det_slit", "det_square_neck", "det_stripes", "det_tiered",
            "det_v_neck"]
# Ready-made seasonal outfit sets (outfit type "Set"), grouped by season
_OSET_ALL = ["os_spr_frill_knit", "os_spr_floral_cami",
             "os_spr_floral_midi", "os_spr_ribbon_blouse", "os_spr_shirt_dress",
             "os_spr_lace_cami", "os_sum_linen", "os_sum_sundress",
             "os_sum_crop_denim", "os_sum_halter_maxi", "os_sum_gingham",
             "os_sum_resort", "os_aut_trench", "os_aut_corduroy", "os_aut_plaid",
             "os_aut_leather", "os_aut_knit_dress", "os_aut_blazer",
             "os_win_wool_coat", "os_win_puffer", "os_win_fur", "os_win_tweed",
             "os_win_overcoat", "os_win_cozy", "os_par_sequin", "os_par_satin_gown",
             "os_par_tulle", "os_par_velvet_suit", "os_par_lbd",
             # v5.9 — national / traditional costumes
             "os_nat_th_chakkri",
             "os_nat_th_chong_kraben",
             "os_nat_th_lace",
             "os_nat_th_lanna",
             "os_nat_th_isan",
             "os_nat_th_male",
             "os_nat_jp_furisode",
             "os_nat_jp_yukata",
             "os_nat_jp_hakama",
             "os_nat_jp_miko",
             "os_nat_jp_male",
             "os_nat_jp_yukata_m",
             "os_nat_kr_hanbok",
             "os_nat_kr_male",
             "os_nat_cn_hanfu",
             "os_nat_cn_qipao",
             "os_nat_cn_tang",
             "os_nat_vn_ao_dai",
             "os_nat_in_saree",
             "os_nat_in_lehenga",
             "os_nat_id_kebaya",
             "os_nat_de_dirndl",
             # v6.3 — everyday, men's and extra seasonal / party sets
             "os_day_tee_jeans", "os_day_cardigan_mini", "os_day_oversized_tee",
             "os_day_blazer_jeans", "os_day_sweatsuit", "os_day_tank_cargo",
             "os_day_shirt_skirt", "os_day_pajamas",
             "os_men_tee_jeans", "os_men_shirt_chinos", "os_men_street",
             "os_men_suit", "os_men_coat", "os_men_leather", "os_men_korean",
             "os_men_resort",
             "os_sum_tank_linen", "os_sum_bikini_shirt", "os_aut_varsity",
             "os_win_knit_set", "os_par_blazer_dress", "os_par_corset"]
# Set categories (first-level picker) — a set's category is its key prefix
OSCAT_KEYS = ["oscat_all", "oscat_daily", "oscat_spring", "oscat_summer",
              "oscat_autumn", "oscat_winter", "oscat_party", "oscat_men",
              "oscat_national"]
OSCAT_PREFIXES = {"oscat_daily": "os_day_", "oscat_spring": "os_spr_",
                  "oscat_summer": "os_sum_", "oscat_autumn": "os_aut_",
                  "oscat_winter": "os_win_", "oscat_party": "os_par_",
                  "oscat_men": "os_men_", "oscat_national": "os_nat_"}
OSET_KEYS = ["os_none"] + [k for prefix in OSCAT_PREFIXES.values()
                           for k in _OSET_ALL if k.startswith(prefix)]
# Random Look only draws everyday sets: a national costume needs a matching
# scene, so those are picked by hand or through a theme. The men's sets are
# drawn for a male subject only, and are the only sets a male subject gets.
OSET_RANDOM_KEYS = [k for k in OSET_KEYS[1:] if not k.startswith("os_nat_")]


def random_set_keys(gd_key: str):
    """Everyday outfit sets Random Look may draw for this gender."""
    if gd_key == "gender_nb":
        return OSET_RANDOM_KEYS
    return [k for k in OSET_RANDOM_KEYS
            if k.startswith("os_men_") == (gd_key == "gender_male")]


def oset_keys_for_category(oscat_key: str):
    """Outfit-set option pool for the selected set category (None stays first)."""
    prefix = OSCAT_PREFIXES.get(oscat_key)
    if prefix:
        return ["os_none"] + [k for k in OSET_KEYS[1:] if k.startswith(prefix)]
    return OSET_KEYS


# Simple mode's outfit type picker: every fashion-style group and set category
SOC_KEYS = ["soc_all"] + list(FS_GROUPS) + OSCAT_KEYS[1:]


def simple_outfit_keys(soc_key: str):
    """Fashion styles or outfit sets listed under a simple-mode outfit type."""
    if soc_key in FS_GROUPS:
        return FS_GROUPS[soc_key]
    if soc_key in OSCAT_PREFIXES:
        return oset_keys_for_category(soc_key)[1:]
    return FS_KEYS + OSET_KEYS[1:]


# ── Group markers ──────────────────────────────────────────────────────────
# Long lists are ordered group by group and every option shows its group's
# emoji in front (via format_func, so stored values stay plain labels).
GROUP_EMOJI = {
    "hg_long": "💇", "hg_short": "✂️", "hg_tied": "🎀", "hg_braid": "🪢", "hg_trad": "👘",
    "hgm_short": "💈", "hgm_mid": "🌀", "hgm_long": "🧔",
    "hcg_dark": "🌰", "hcg_light": "🌼", "hcg_red": "🍒", "hcg_fashion": "🌈",
    "hcg_multi": "🎨",
    "exg_happy": "😊", "exg_cute": "🥰", "exg_calm": "😌", "exg_cool": "😎",
    "exg_moody": "😢",
    "fsg_daily": "👕", "fsg_trend": "💅", "fsg_event": "🎤", "fsg_sport": "🏃",
    "fsg_trad": "🏮",
    "tdg_morning": "🌅", "tdg_day": "☀️", "tdg_evening": "🌇", "tdg_night": "🌙",
    "ltg_natural": "☀️", "ltg_studio": "💡", "ltg_night": "🌃",
    "psg_clean": "📷", "psg_film": "🎞️", "psg_cine": "🎬", "psg_dream": "✨",
    "sfg_close": "🙂", "sfg_half": "👤", "sfg_full": "🧍", "sfg_wide": "🏞️",
    "sfg_detail": "🔍",
    "pc_standing": "🧍", "pc_walking": "🚶", "pc_sitting": "🪑", "pc_kneeling": "🧎",
    "pc_lying": "🛌", "pc_crouching": "🙇", "pc_cute": "✌️", "pc_social": "🤳",
    "pc_daily": "☕", "pc_props": "💐", "pc_sport": "⚽",
    "lcat_indoor": "📸", "lcat_home": "🏠", "lcat_city": "🏙️", "lcat_shops": "🛍️",
    "lcat_nature": "🌿", "lcat_water": "🌊", "lcat_luxury": "💎", "lcat_travel": "✈️",
    "lcat_thai": "🛕", "lcat_asia": "⛩️", "lcat_leisure": "🎡", "lcat_fantasy": "🔮",
}
# option key (or group key, for category pickers) → emoji
OPTION_EMOJI = dict(GROUP_EMOJI)
for _groups in (HAIR_GROUPS_WOMEN, HAIR_GROUPS_MEN, HC_GROUPS, EX_GROUPS, FS_GROUPS,
                TD_GROUPS, LT_GROUPS, PS_GROUPS, SF_GROUPS, POSE_CATEGORIES,
                LOC_CATEGORIES):
    for _group, _keys in _groups.items():
        OPTION_EMOJI.update({k: GROUP_EMOJI[_group] for k in _keys})


def grouped(keys):
    """format_func for a selectbox/multiselect over `keys`: shows each label
    with its group's emoji in front. Options without a group stay as they are."""
    table = {t(k): f"{OPTION_EMOJI[k]} {t(k)}" for k in keys if k in OPTION_EMOJI}
    return lambda label: table.get(label, label)


# Random Look style (sidebar): everyday looks, or a national costume paired
# with a matching location, hairstyle, pose and light.
RS_KEYS = ["rs_everyday", "rs_national", "rs_thai", "rs_japan", "rs_korea", "rs_china"]
CULTURE_LOOKS = {
    "th": {
        "sets_f": ["os_nat_th_chakkri", "os_nat_th_chong_kraben", "os_nat_th_lace",
                   "os_nat_th_lanna", "os_nat_th_isan"],
        "sets_m": ["os_nat_th_male"],
        "locs": ["loc_th_wat", "loc_th_palace", "loc_th_ruins", "loc_th_river_temple",
                 "loc_th_white_temple", "loc_th_teak", "loc_th_sala", "loc_th_lotus",
                 "loc_th_floating", "loc_th_chiangmai", "loc_th_krathong",
                 "loc_th_lantern"],
        "hair": ["hair_thai_chignon", "hair_flower_updo", "hair_low_bun"],
        "poses": ["pose_wai", "pose_elegant", "pose_stand", "pose_sit_side",
                  "pose_over_shoulder"],
    },
    "jp": {
        "sets_f": ["os_nat_jp_furisode", "os_nat_jp_yukata", "os_nat_jp_hakama",
                   "os_nat_jp_miko"],
        "sets_m": ["os_nat_jp_male", "os_nat_jp_yukata_m"],
        "locs": ["loc_jp_torii", "loc_jp_ryokan", "loc_jp_castle", "loc_jp_zen",
                 "loc_jp_tea_house", "loc_jp_gion", "loc_jp_onsen", "loc_jp_fuji",
                 "loc_bamboo", "loc_cherry", "loc_jp_matsuri", "loc_jp_sakura_river",
                 "loc_jp_snow_village"],
        "hair": ["hair_jp_updo", "hair_low_bun", "hair_flower_updo", "hair_hime"],
        "poses": ["pose_bow", "pose_parasol", "pose_sleeve_smile", "pose_seiza",
                  "pose_look_back_walk", "pose_stand"],
    },
    "kr": {
        "sets_f": ["os_nat_kr_hanbok"], "sets_m": ["os_nat_kr_male"],
        "locs": ["loc_kr_hanok", "loc_kr_palace"],
        "hair": ["hair_kr_daenggi", "hair_low_bun"],
        "poses": ["pose_bow", "pose_skirt_hem", "pose_twirl", "pose_walk", "pose_stand"],
    },
    "cn": {
        "sets_f": ["os_nat_cn_hanfu", "os_nat_cn_qipao"], "sets_m": ["os_nat_cn_tang"],
        "locs": ["loc_cn_garden", "loc_cn_lantern_street", "loc_cn_water_town",
                 "loc_cn_great_wall", "loc_bamboo"],
        "hair": ["hair_cn_updo", "hair_low_bun", "hair_flower_updo"],
        "poses": ["pose_parasol", "pose_sleeve_smile", "pose_elegant", "pose_twirl",
                  "pose_over_shoulder"],
    },
    "vn": {
        "sets_f": ["os_nat_vn_ao_dai"], "sets_m": [],
        "locs": ["loc_hoi_an", "loc_rice_field", "loc_th_lotus"],
        "hair": ["hair_straight", "hair_low_bun"],
        "poses": ["pose_walk", "pose_stand", "pose_over_shoulder", "pose_bicycle"],
    },
    "in": {
        "sets_f": ["os_nat_in_saree", "os_nat_in_lehenga"], "sets_m": [],
        "locs": ["loc_india_palace"],
        "hair": ["hair_braids", "hair_low_bun", "hair_flower_updo"],
        "poses": ["pose_elegant", "pose_twirl", "pose_stand", "pose_over_shoulder"],
    },
    "id": {
        "sets_f": ["os_nat_id_kebaya"], "sets_m": [],
        "locs": ["loc_bali", "loc_rice_field"],
        "hair": ["hair_low_bun", "hair_flower_updo"],
        "poses": ["pose_elegant", "pose_stand", "pose_over_shoulder"],
    },
    "de": {
        "sets_f": ["os_nat_de_dirndl"], "sets_m": [],
        "locs": ["loc_old_town", "loc_castle", "loc_meadow"],
        "hair": ["hair_twin_braids", "hair_french_braid"],
        "poses": ["pose_twirl", "pose_skirt_hem", "pose_stand", "pose_walk"],
    },
}
RS_CULTURES = {"rs_national": list(CULTURE_LOOKS), "rs_thai": ["th"],
               "rs_japan": ["jp"], "rs_korea": ["kr"], "rs_china": ["cn"]}
# Locations whose text already says "night" — they get night time + lantern light
CULTURE_NIGHT_LOCS = {"loc_th_krathong", "loc_th_lantern", "loc_jp_matsuri",
                      "loc_cn_lantern_street"}
# Calm, natural pools so a costume look never gets disco light or pink hair
CULTURE_POOLS = {
    "w_tod": ["tod_golden", "tod_noon", "tod_overcast", "tod_sunrise"],
    "w_lighting": ["lit_natural", "lit_backlit", "lit_dappled", "lit_godrays"],
    "w_pstyle": ["ps_none", "ps_soft", "ps_cinematic", "ps_editorial",
                 "ps_nostalgic", "ps_vivid", "ps_dreamy"],
    "w_makeup": ["mu_none", "mu_natural", "mu_dewy", "mu_red_lip", "mu_soft_matte"],
    "w_hair_color": ["hc_none", "hc_black", "hc_blue_black", "hc_dark_brown"],
    "w_hair_finish": ["hf_none", "hf_glossy", "hf_sleek"],
    "w_light_color": ["lc_none", "lc_warm", "lc_neutral"],
    "w_pose_energy": ["pe_none", "pe_elegant", "pe_relaxed", "pe_candid", "pe_shy"],
}
OM_KEYS = ["om_separates", "om_dress", "om_set"]

# Widget key → option key list, for the Random Look button.
# Identity fields (gender, age, ethnicity) are deliberately NOT randomized.
# Hair and outfit widgets are handled separately in randomize_look():
# hair depends on the selected gender, and the outfit is either style-led
# (fashion presets) or garment-led (top/bottom) — never both, to avoid clashes.
RANDOM_WIDGETS = {
    "w_hair_color": HC_KEYS, "w_bangs": BN_KEYS,
    "w_expr": EX_KEYS, "w_body": BT_KEYS, "w_appearance": AP_KEYS,
    "w_makeup": MU_KEYS,
    "w_location": LO_KEYS, "w_tod": TD_KEYS, "w_lighting": LT_KEYS,
    "w_season": SN_KEYS, "w_pstyle": PS_KEYS, "w_framing": SF_KEYS,
    "w_dof": DOF_KEYS, "w_comp": CMP_KEYS, "w_pose": PO_KEYS,
    "w_gaze": GZ_KEYS, "w_pose_energy": PE_KEYS,
    "w_light_dir": LD_KEYS, "w_light_color": LC_KEYS,
    "w_hair_finish": HF_KEYS, "w_skin_finish": SKF_KEYS, "w_nails": NL_KEYS,
}

# Pose fine-tuning widgets that only make sense for a specific pose — Random
# Look and themes reset them to None instead of randomizing (random hand/leg
# details would contradict the random pose most of the time).
POSE_DETAIL_WIDGETS = {
    "w_body_dir": BD_KEYS, "w_head": HD_KEYS, "w_hands": HA_KEYS, "w_legs": LG_KEYS,
}

# Scene/camera subset for the "Random Scene" button — keeps the subject,
# outfit and pose untouched (useful for consistent-character variations).
SCENE_RANDOM_WIDGETS = {
    "w_location": LO_KEYS, "w_tod": TD_KEYS, "w_lighting": LT_KEYS,
    "w_season": SN_KEYS, "w_pstyle": PS_KEYS, "w_framing": SF_KEYS,
    "w_dof": DOF_KEYS, "w_comp": CMP_KEYS,
    "w_light_dir": LD_KEYS, "w_light_color": LC_KEYS,
}

# Photo Set mode: portrait-friendly framing/angle pools — no CCTV, fisheye,
# aerial etc., so the album reads like one photographer moving around the
# subject. Poses that need a mirror, a phone-in-hand or a sports court are
# excluded for the same reason.
PHOTO_SET_SF_KEYS = ["sf_closeup", "sf_medium_cu", "sf_medium", "sf_cowboy",
                     "sf_medium_full", "sf_full"]
PHOTO_SET_CH_KEYS = ["ch_high", "ch_slight_high", "ch_eye", "ch_chest",
                     "ch_slight_low", "ch_low"]
PHOTO_SET_CD_KEYS = ["cd_front", "cd_front_3q", "cd_side", "cd_back_3q",
                     "cd_over_shoulder"]
PHOTO_SET_POSE_EXCLUDE = ({"pose_none", "pose_meditate", "pose_mirror_selfie",
                           "pose_selfie", "pose_phone_check", "pose_05x",
                           "pose_cook", "pose_laptop", "pose_write", "pose_drive",
                           "pose_makeup", "pose_suitcase", "pose_phone_call",
                           "pose_sing_mic", "pose_guitar", "pose_paint",
                           "pose_watering", "pose_sit_bed_edge", "pose_sit_window",
                           "pose_sit_swing", "pose_lie_flowers", "pose_stairs_down",
                           "pose_puddle_hop"}
                          | set(POSE_CATEGORIES["pc_sport"]))
PHOTO_SET_SIZE = 6

# Hairstyle widget → the gender widget whose hair pool it depends on
HAIR_GENDER_WIDGETS = {
    "w_hair": "w_gender",
    "w_hair_p2": "w_gender_p2",
    "w_hair_p3": "w_gender_p3",
}


def hair_pool_for_label(gd_label):
    """Hair option pool for a gender given as its *translated label*."""
    if gd_label == t("gender_male"):
        return HR_KEYS_MEN
    if gd_label == t("gender_nb"):
        return HR_KEYS
    return HR_KEYS_WOMEN

# Widget key → option key list, for saving/loading a look as JSON.
# Presets store option KEYS (language-independent), not translated labels.
PRESET_WIDGETS = {
    "w_gender": GD_KEYS, "w_age": AG_KEYS, "w_eth": ET_KEYS,
    "w_hair": HR_KEYS, "w_hair_color": HC_KEYS, "w_bangs": BN_KEYS,
    "w_expr": EX_KEYS, "w_body": BT_KEYS, "w_appearance": AP_KEYS,
    "w_makeup": MU_KEYS, "w_pet": PET_KEYS,
    "w_top": TOP_KEYS, "top_fabric_sel": FB_KEYS, "top_color_sel": CP_KEYS,
    "w_bottom": BOT_KEYS, "bot_fabric_sel": FB_KEYS, "bot_color_sel": CP_KEYS,
    "w_shoes": SH_KEYS,
    "w_gender_p2": GD_KEYS,
    "w_hair_p2": HR_KEYS, "w_hair_color_p2": HC_KEYS, "w_expr_p2": EX_KEYS,
    "w_gender_p3": GD_KEYS,
    "w_hair_p3": HR_KEYS, "w_hair_color_p3": HC_KEYS, "w_expr_p3": EX_KEYS,
    "w_group_mix": GM_KEYS,
    "w_location": LO_KEYS, "w_tod": TD_KEYS, "w_lighting": LT_KEYS,
    "w_season": SN_KEYS, "w_pstyle": PS_KEYS, "w_framing": SF_KEYS,
    "w_dof": DOF_KEYS, "w_comp": CMP_KEYS, "w_pose": PO_KEYS,
    "w_pose_cat": PC_KEYS, "w_gaze": GZ_KEYS, "w_pose_energy": PE_KEYS,
    **POSE_DETAIL_WIDGETS,
    "w_outfit_mode": OM_KEYS, "w_dress": DR_KEYS,
    "dress_fabric_sel": FB_KEYS, "dress_color_sel": CP_KEYS,
    "w_outfit_set": OSET_KEYS, "w_outer": OUT_KEYS, "outer_color_sel": CP_KEYS,
    "w_set_cat": OSCAT_KEYS,
    "w_fit": FIT_KEYS, "w_legwear": LEG_KEYS,
    "w_skin_tone": ST_KEYS, "w_face_shape": FSH_KEYS, "w_eye_shape": EYE_KEYS,
    "w_eye_color": EC_KEYS, "w_brows": BROW_KEYS, "w_lips": LIP_KEYS,
    "w_facial_hair": FH_KEYS, "w_skin_finish": SKF_KEYS, "w_hair_finish": HF_KEYS,
    "w_nails": NL_KEYS,
    "w_loc_cat": LCAT_KEYS, "w_cam_height": CH_KEYS, "w_cam_dir": CD_KEYS,
    "w_cam_special": CS_KEYS, "w_camera_film": CF_KEYS, "w_light_dir": LD_KEYS,
    "w_light_color": LC_KEYS, "w_light_quality": LQ_KEYS, "w_bg_people": BGP_KEYS,
}

# Multiselect widgets (lists of option keys in presets)
MULTI_WIDGETS = {
    "fashion_multi": FS_KEYS, "detail_multi": DET_KEYS, "face_marks": FM_KEYS,
    "atm_multi": ATM_KEYS, "lfx_multi": LFX_KEYS,
}

# Widgets whose stored value is a translated label — must be reset when the
# UI language changes, otherwise the stale label is no longer a valid option.
LANG_DEPENDENT_WIDGETS = (list(PRESET_WIDGETS) + list(MULTI_WIDGETS)
                          + ["w_theme", "w_random_style", "w_prompt_len"])

# Character Lock: identity, face, body and hair. While a character is locked
# these widgets are disabled and re-set from the lock on every run, so Random
# Look, themes and presets can only change styling, pose and scene.
CHAR_WIDGETS = [
    "w_gender", "w_age", "w_eth", "w_skin_tone", "w_body", "w_appearance",
    "w_face_shape", "w_eye_shape", "w_eye_color", "w_brows", "w_lips",
    "face_marks", "w_facial_hair", "w_hair", "w_hair_color", "w_bangs",
]

# Neutral outfit-layer + pose-detail values. Built-in themes are applied on
# top of this so leftovers from the previous look (a dress, leg warmers,
# "hands in pockets"…) can't clash with the theme's own outfit and pose.
LOOK_BASE = {
    "w_pose_cat": "pc_all", "w_gaze": "gaze_none", "w_pose_energy": "pe_none",
    **{wk: keys[0] for wk, keys in POSE_DETAIL_WIDGETS.items()},
    "w_outfit_mode": "om_separates", "w_dress": "dress_none",
    "dress_fabric_sel": "fab_none", "dress_color_sel": "col_none",
    "w_outfit_set": "os_none", "w_outer": "out_none", "outer_color_sel": "col_none",
    "w_set_cat": "oscat_all",
    "w_fit": "fit_none", "w_legwear": "leg_none", "detail_multi": [],
}

# Neutral scene/camera extras, applied under every built-in theme
SCENE_BASE = {
    "w_loc_cat": "lcat_all", "w_cam_height": "ch_none", "w_cam_dir": "cd_none",
    "w_cam_special": "cs_none", "w_camera_film": "cf_none", "w_light_dir": "ld_none",
    "w_light_color": "lc_none", "w_light_quality": "lq_none", "w_bg_people": "bgp_none",
    "atm_multi": [], "lfx_multi": [],
}


def widget_option_value(widget_key):
    """Current option key (or list of keys) of a widget, from its label(s)."""
    val = st.session_state.get(widget_key)
    if widget_key in MULTI_WIDGETS:
        return [k for k in MULTI_WIDGETS[widget_key] if t(k) in (val or [])]
    return next((k for k in PRESET_WIDGETS[widget_key] if t(k) == val), None)


def _lock(name, data):
    """Store a character lock (option keys) and add it to the session library."""
    entry = {"name": name,
             "data": {wk: data[wk] for wk in CHAR_WIDGETS if data.get(wk) is not None}}
    st.session_state["char_lock"] = entry
    st.session_state.setdefault("char_library", {})[name or t("char_unnamed")] = entry


def lock_character():
    """Lock the character currently shown in the Subject section."""
    _lock(st.session_state.get("char_name_input", "").strip(),
          {wk: widget_option_value(wk) for wk in CHAR_WIDGETS})


def unlock_character():
    st.session_state.pop("char_lock", None)


def load_library_character():
    """Load a character saved earlier in this session, and lock it."""
    entry = st.session_state.get("char_library", {}).get(st.session_state.get("w_char_lib"))
    if entry:
        st.session_state["char_lock"] = entry
        st.session_state["char_name_input"] = entry["name"]
        st.session_state["force_generate"] = True


def enforce_character_lock():
    """Re-apply the locked character's values before the widgets render."""
    lock = st.session_state.get("char_lock")
    if not lock:
        return
    for wk, val in lock["data"].items():
        label = [t(k) for k in val] if isinstance(val, list) else t(val)
        if st.session_state.get(wk) != label:
            st.session_state[wk] = label


# Character library + prompt history are mirrored into the browser's
# localStorage through a tiny static component (browser_store/index.html), so
# they survive a refresh. Nothing is stored on the server.
_browser_store = components.declare_component(
    "browser_store", path=str(Path(__file__).parent / "browser_store"))


def _valid_library_entry(entry):
    """True if a stored character only uses known widgets and option keys."""
    if not (isinstance(entry, dict) and isinstance(entry.get("name"), str)
            and isinstance(entry.get("data"), dict)):
        return False
    for wk, val in entry["data"].items():
        if wk not in CHAR_WIDGETS:
            return False
        if wk in MULTI_WIDGETS:
            if not (isinstance(val, list) and all(v in MULTI_WIDGETS[wk] for v in val)):
                return False
        elif val not in PRESET_WIDGETS[wk]:
            return False
    return True


def sync_browser_store():
    """Load the saved library/history once per session, then keep the browser
    copy up to date. Called at the end of every run."""
    loaded = st.session_state.get("_store_loaded", False)
    payload = None
    if loaded:
        payload = json.dumps({
            "char_library": st.session_state.get("char_library", {}),
            "prompt_history": st.session_state.get("prompt_history", []),
        }, ensure_ascii=False, sort_keys=True)
    stored = _browser_store(payload=payload, key="browser_store", default=None)
    if loaded or not isinstance(stored, dict):
        return
    st.session_state["_store_loaded"] = True
    try:
        data = json.loads(stored.get("data") or "{}")
    except (TypeError, ValueError):
        data = {}
    if not isinstance(data, dict):
        data = {}
    changed = False
    library = st.session_state.setdefault("char_library", {})
    saved_library = data.get("char_library")
    for name, entry in (saved_library.items() if isinstance(saved_library, dict) else []):
        if isinstance(name, str) and name not in library and _valid_library_entry(entry):
            library[name] = entry
            changed = True
    history = st.session_state.get("prompt_history", [])
    saved_history = data.get("prompt_history")
    for item in (saved_history if isinstance(saved_history, list) else []):
        if isinstance(item, str) and item not in history and len(history) < 10:
            history.append(item)
            changed = True
    st.session_state["prompt_history"] = history
    if changed:
        st.rerun()


# ── Simple mode ────────────────────────────────────────────────────────────
# (real widget key, label key, option keys — None = hair pool by gender,
#  default index of the real widget). Each simple picker is a mirror: it shows
#  the real widget's current value and writes changes back to it.
SIMPLE_ROWS = [
    [("w_gender", "gender", GD_KEYS, 0), ("w_age", "age_group", AG_KEYS, 1),
     ("w_hair", "hair_style", None, 1), ("w_hair_color", "hair_color", HC_KEYS, 1)],
    [("w_expr", "expression", EX_KEYS, 1), ("OUTFIT_CAT", "simple_outfit_cat", None, 0),
     ("OUTFIT", "simple_outfit", None, 0)],
    [("w_pose_cat", "pose_category", PC_KEYS, 0), ("w_pose", "pose", None, 0),
     ("w_framing", "shot_framing", SF_KEYS, 2)],
    [("w_loc_cat", "location_category", LCAT_KEYS, 0), ("w_location", "location", None, 1),
     ("w_tod", "time_of_day", TD_KEYS, TD_DEFAULT)],
    [("w_lighting", "lighting", LT_KEYS, 1), ("w_pstyle", "picture_style", PS_KEYS, 0)],
]
OUTFIT_NONE_WIDGETS = (("w_top", "top_none"), ("w_bottom", "bot_none"),
                       ("top_fabric_sel", "fab_none"), ("bot_fabric_sel", "fab_none"),
                       ("top_color_sel", "col_none"), ("bot_color_sel", "col_none"),
                       ("w_shoes", "sh_none"))


def sync_simple(real_key):
    """A simple-mode picker changed — copy its value to the real widget."""
    st.session_state[real_key] = st.session_state[f"sm_{real_key}"]
    if real_key == "w_gender":
        reset_hair_on_gender_change()
    elif real_key in ("w_location", "w_loc_cat"):
        if real_key == "w_loc_cat":
            reset_location_on_category_change()
        st.session_state["scene_mode_radio"] = t("scene_mode_preset")
        st.session_state["attach_scene"] = False
    elif real_key in ("w_pose", "w_pose_cat"):
        if real_key == "w_pose_cat":
            reset_pose_on_category_change()
        st.session_state["attach_pose"] = False


def _simple_keys(real_key):
    """Option keys of a simple picker whose list depends on another pick."""
    if real_key == "w_pose":
        return pose_keys_for_category(widget_option_value("w_pose_cat") or "pc_all")
    if real_key == "w_location":
        return loc_keys_for_category(widget_option_value("w_loc_cat") or "lcat_all")
    return hair_pool_for_label(st.session_state.get("w_gender", t("gender_female")))


def _simple_outfit_key():
    """Which single outfit the full editor currently describes: a fashion
    style key, an outfit set key, "os_none", or None for anything richer
    (garments, a dress, several styles) that the simple list can't show."""
    mode = widget_option_value("w_outfit_mode") or "om_separates"
    styles = widget_option_value("fashion_multi")
    garment_widgets = {"om_separates": (("w_top", "top_none"), ("w_bottom", "bot_none")),
                       "om_dress": (("w_dress", "dress_none"),)}.get(mode, ())
    if any(widget_option_value(wk) not in (None, none_key)
           for wk, none_key in garment_widgets):
        return None
    if mode == "om_set":
        set_key = widget_option_value("w_outfit_set")
        if set_key is None or (set_key != "os_none" and styles):
            return None
        if set_key != "os_none":
            return set_key
    if len(styles) > 1:
        return None
    return styles[0] if styles else "os_none"


def _simple_outfit_cat():
    """Outfit type currently picked in simple mode ("soc_all" by default)."""
    label = st.session_state.get("sm_outfit_cat")
    return next((k for k in SOC_KEYS if t(k) == label), "soc_all")


def _set_simple_outfit(key):
    """Replace the whole outfit with one fashion style, one set, or nothing."""
    for widget_key, val in LOOK_BASE.items():
        if widget_key.startswith(("w_pose", "w_gaze")) or widget_key in POSE_DETAIL_WIDGETS:
            continue
        st.session_state[widget_key] = val if isinstance(val, list) else t(val)
    for widget_key, none_key in OUTFIT_NONE_WIDGETS:
        st.session_state[widget_key] = t(none_key)
    st.session_state["fashion_multi"] = [t(key)] if key in FS_KEYS else []
    st.session_state["attach_outfit"] = False
    if key in OSET_KEYS[1:]:
        st.session_state["w_outfit_mode"] = t("om_set")
        st.session_state["w_outfit_set"] = t(key)


def sync_simple_outfit():
    """Simple-mode outfit picker: one fashion style or one ready-made set."""
    label = st.session_state.get("sm_outfit")
    key = next((k for k in ["os_none"] + FS_KEYS + OSET_KEYS[1:] if t(k) == label), None)
    if key is not None:  # None = the "custom" entry — leave the outfit as it is
        _set_simple_outfit(key)


def sync_simple_outfit_cat():
    """Outfit type changed — an outfit from another type no longer fits."""
    current = _simple_outfit_key()
    if current not in (None, "os_none") and current not in simple_outfit_keys(_simple_outfit_cat()):
        _set_simple_outfit("os_none")


def render_simple_panel():
    """The simple-mode pickers. Runs before the (hidden) full editor."""
    locked = bool(st.session_state.get("char_lock"))
    enforce_character_lock()
    for row in SIMPLE_ROWS:
        for col, (real_key, label_key, keys, default) in zip(st.columns(len(row)), row):
            with col:
                if real_key == "OUTFIT_CAT":
                    # Themes / Random Look may have set an outfit of another type
                    current = _simple_outfit_key()
                    cat = _simple_outfit_cat()
                    if current not in (None, "os_none") and current not in simple_outfit_keys(cat):
                        cat = "soc_all"
                    st.session_state["sm_outfit_cat"] = t(cat)
                    st.selectbox(t(label_key), [t(k) for k in SOC_KEYS], key="sm_outfit_cat",
                                 format_func=grouped(SOC_KEYS),
                                 on_change=sync_simple_outfit_cat)
                    continue
                if real_key == "OUTFIT":
                    current = _simple_outfit_key()
                    outfit_keys = ["os_none"] + simple_outfit_keys(_simple_outfit_cat())
                    labels = [t(k) for k in outfit_keys]
                    if current is None:
                        labels.insert(0, t("simple_outfit_custom"))
                    st.session_state["sm_outfit"] = labels[0] if current is None else t(current)
                    st.selectbox(t(label_key), labels, key="sm_outfit",
                                 format_func=grouped(outfit_keys),
                                 on_change=sync_simple_outfit)
                    continue
                keys = keys or _simple_keys(real_key)
                labels = [t(k) for k in keys]
                mirror = f"sm_{real_key}"
                if st.session_state.get(real_key) in labels:
                    st.session_state[mirror] = st.session_state[real_key]
                else:  # real widget not set yet → both show the same default
                    st.session_state.pop(mirror, None)
                st.selectbox(t(label_key), labels, index=default, key=mirror,
                             format_func=grouped(keys),
                             on_change=sync_simple, args=(real_key,),
                             disabled=locked and real_key in CHAR_WIDGETS)
    st.caption(t("simple_caption"))


def reset_all():
    """Back to a clean start: every picker, accessory and reference toggle.
    A locked character and the saved library/history are kept."""
    for key in list(st.session_state):
        if (key in LANG_DEPENDENT_WIDGETS or key.startswith(("acc_", "attach_", "sm_"))
                or key in ("scene_mode_radio", "photo_set_prompts")):
            st.session_state.pop(key, None)


def reset_pose_on_category_change():
    """Pose category changed — the old pose may not be in the new pool."""
    st.session_state.pop("w_pose", None)


def reset_set_on_category_change():
    """Set category changed — the old outfit set may not be in the new pool."""
    st.session_state.pop("w_outfit_set", None)


def delete_library_character():
    """Remove the selected character from the saved library."""
    st.session_state.get("char_library", {}).pop(st.session_state.get("w_char_lib"), None)
    st.session_state.pop("w_char_lib", None)


def clear_prompt_history():
    st.session_state["prompt_history"] = []


def _pick_culture(gd_key):
    """Culture code for the selected Random Look style, or None for everyday
    looks. Only cultures that have a costume for this gender are eligible."""
    label = st.session_state.get("w_random_style")
    rs_key = next((k for k in RS_KEYS if t(k) == label), "rs_everyday")
    eligible = [c for c in RS_CULTURES.get(rs_key, []) if _culture_sets(c, gd_key)]
    return random.choice(eligible) if eligible else None


def _culture_sets(culture, gd_key):
    look = CULTURE_LOOKS[culture]
    if gd_key == "gender_female":
        return look["sets_f"]
    if gd_key == "gender_male":
        return look["sets_m"]
    return look["sets_f"] + look["sets_m"]


def _apply_culture_look(culture, gd_key):
    """National costume + matching location, hairstyle, pose and calm light.
    Runs after the generic randomization, overriding the parts that matter."""
    look = CULTURE_LOOKS[culture]
    for widget_key, pool in CULTURE_POOLS.items():
        st.session_state[widget_key] = t(random.choice(pool))
    st.session_state["w_outfit_mode"] = t("om_set")
    st.session_state["w_outfit_set"] = t(random.choice(_culture_sets(culture, gd_key)))
    loc = random.choice(look["locs"])
    st.session_state["w_location"] = t(loc)
    st.session_state["w_season"] = t("season_none")
    st.session_state["w_nails"] = t("nl_none")
    if loc in CULTURE_NIGHT_LOCS:
        st.session_state["w_tod"] = t("tod_night")
        st.session_state["w_lighting"] = t("lit_lantern")
        st.session_state["w_light_color"] = t("lc_warm")
    st.session_state["w_pose"] = t(random.choice(look["poses"]))
    # Traditional hairstyles are in the women's pool; men keep their random cut
    hair = [k for k in look["hair"] if k in hair_keys_for_gender(gd_key)]
    if hair:
        st.session_state["w_hair"] = t(random.choice(hair))
        st.session_state["w_bangs"] = t("bangs_none")


def reset_location_on_category_change():
    """Location category changed — the old location may not be in the new pool."""
    st.session_state.pop("w_location", None)


def reset_hair_on_gender_change():
    """Main gender changed — per-person genders default to it, so drop the
    per-person gender picks and every hairstyle pick (their pools changed)."""
    for wk in list(HAIR_GENDER_WIDGETS) + ["w_gender_p2", "w_gender_p3"]:
        st.session_state.pop(wk, None)


def reset_person_hair(hair_widget_key):
    """A per-person gender changed — drop only that person's hairstyle."""
    st.session_state.pop(hair_widget_key, None)


def randomize_look():
    """Pick a random label for every style widget, then auto-generate."""
    for widget_key, option_keys in RANDOM_WIDGETS.items():
        st.session_state[widget_key] = t(random.choice(option_keys))
    # Hair: pick from the pool matching each person's selected gender
    gd_label = st.session_state.get("w_gender", t("gender_female"))
    st.session_state["w_hair"] = t(random.choice(hair_pool_for_label(gd_label)))
    # Extra persons (only visible for duo/trio) get distinct random looks too
    for suffix in ("_p2", "_p3"):
        p_gd_label = st.session_state.get(f"w_gender{suffix}", gd_label)
        p_pool = hair_pool_for_label(p_gd_label)
        st.session_state[f"w_hair{suffix}"] = t(random.choice(p_pool))
        st.session_state[f"w_hair_color{suffix}"] = t(random.choice(HC_KEYS))
        st.session_state[f"w_expr{suffix}"] = t(random.choice(EX_KEYS))
    _reset_scene_pickers()
    # Pose: drawn from the full list, so show all categories; the per-pose
    # details (hands, legs…) go back to None so they can't contradict it
    st.session_state["w_pose_cat"] = t("pc_all")
    for widget_key, option_keys in POSE_DETAIL_WIDGETS.items():
        st.session_state[widget_key] = t(option_keys[0])
    # Outfit: a fashion style, explicit separates, a dress, or a ready-made
    # set — one source per look, never mixed, to avoid clashes
    for widget_key, val in LOOK_BASE.items():
        if widget_key.startswith(("w_pose", "w_gaze")) or widget_key in POSE_DETAIL_WIDGETS:
            continue
        st.session_state[widget_key] = val if isinstance(val, list) else t(val)
    for widget_key, none_key in (("w_top", "top_none"), ("w_bottom", "bot_none"),
                                 ("top_fabric_sel", "fab_none"), ("bot_fabric_sel", "fab_none"),
                                 ("top_color_sel", "col_none"), ("bot_color_sel", "col_none"),
                                 ("w_shoes", "sh_none")):
        st.session_state[widget_key] = t(none_key)
    st.session_state["fashion_multi"] = []
    st.session_state["force_generate"] = True
    gd_key = next((k for k in GD_KEYS if t(k) == gd_label), "gender_female")
    culture = _pick_culture(gd_key)
    if culture:
        _apply_culture_look(culture, gd_key)
        return
    roll = random.random()
    if gd_key == "gender_male" and 0.6 <= roll < 0.85:
        roll = 0.5  # the dress branch → separates
    if roll < 0.3:
        st.session_state["fashion_multi"] = [t(k) for k in random.sample(FS_KEYS, random.randint(1, 2))]
    elif roll < 0.85:
        if roll < 0.6:
            st.session_state["w_top"] = t(random.choice(TOP_KEYS[1:]))
            st.session_state["w_bottom"] = t(random.choice(BOT_KEYS[1:]))
            st.session_state["top_fabric_sel"] = t(random.choice(FB_KEYS[1:]))
            st.session_state["bot_fabric_sel"] = t(random.choice(FB_KEYS[1:]))
            st.session_state["top_color_sel"] = t(random.choice(CP_KEYS[1:]))
            st.session_state["bot_color_sel"] = t(random.choice(CP_KEYS[1:]))
        else:
            st.session_state["w_outfit_mode"] = t("om_dress")
            st.session_state["w_dress"] = t(random.choice(DR_KEYS[1:]))
            st.session_state["dress_fabric_sel"] = t(random.choice(FB_KEYS[1:]))
            st.session_state["dress_color_sel"] = t(random.choice(CP_KEYS[1:]))
        # Optional layers on top of the garments
        if random.random() < 0.35:
            st.session_state["w_outer"] = t(random.choice(OUT_KEYS[1:]))
        if random.random() < 0.35:
            st.session_state["w_legwear"] = t(random.choice(LEG_KEYS[1:]))
        st.session_state["w_fit"] = t(random.choice(FIT_KEYS))
        st.session_state["detail_multi"] = [t(k) for k in random.sample(DET_KEYS, random.randint(0, 2))]
        st.session_state["w_shoes"] = t(random.choice(SH_KEYS[1:]))
    else:
        st.session_state["w_outfit_mode"] = t("om_set")
        st.session_state["w_outfit_set"] = t(random.choice(random_set_keys(gd_key)))
    st.session_state["force_generate"] = True


def _reset_scene_pickers():
    """Random picks come from the full location list, use portrait-friendly
    camera heights/positions (the Photo Set pools) and never a special shot
    (CCTV, fisheye…) — those are deliberate choices, not random ones."""
    st.session_state["w_loc_cat"] = t("lcat_all")
    st.session_state["w_cam_special"] = t("cs_none")
    st.session_state["w_cam_height"] = t(random.choice(PHOTO_SET_CH_KEYS))
    st.session_state["w_cam_dir"] = t(random.choice(["cd_none"] + PHOTO_SET_CD_KEYS))


def randomize_scene():
    """Randomize only scene/camera widgets, keeping subject/outfit/pose fixed."""
    for widget_key, option_keys in SCENE_RANDOM_WIDGETS.items():
        st.session_state[widget_key] = t(random.choice(option_keys))
    _reset_scene_pickers()
    st.session_state["force_generate"] = True


def _apply_preset_dict(data):
    """Set widgets from a dict of option keys (shared by pasted looks and
    built-in themes), validating every key against its option list."""
    # Genders first — each person's hairstyle pool depends on their gender
    for gender_widget in ("w_gender", "w_gender_p2", "w_gender_p3"):
        gv = data.get(gender_widget)
        if gv in GD_KEYS:
            st.session_state[gender_widget] = t(gv)
    for widget_key, option_keys in PRESET_WIDGETS.items():
        val = data.get(widget_key)
        if not isinstance(val, str) or val not in option_keys:
            continue
        # Hairstyles must exist in the pool of that person's (new) gender
        if widget_key in HAIR_GENDER_WIDGETS:
            gd_label = st.session_state.get(
                HAIR_GENDER_WIDGETS[widget_key],
                st.session_state.get("w_gender", t("gender_female")))
            if val not in hair_pool_for_label(gd_label):
                st.session_state.pop(widget_key, None)
                continue
        st.session_state[widget_key] = t(val)
    for widget_key, option_keys in MULTI_WIDGETS.items():
        vals = data.get(widget_key)
        if isinstance(vals, list):
            st.session_state[widget_key] = [t(k) for k in vals if k in option_keys]
    # look.json from ≤ v5.7 stored a single camera angle
    old_angle = CAM_MIGRATION.get(data.get("w_angle"))
    if old_angle:
        st.session_state[old_angle[0]] = t(old_angle[1])
    # A loaded location must be selectable in the current location category
    loc = data.get("w_location")
    if loc in LO_KEYS:
        lcat_label = st.session_state.get("w_loc_cat", t("lcat_all"))
        lcat_key = next((k for k in LCAT_KEYS if t(k) == lcat_label), "lcat_all")
        if loc not in loc_keys_for_category(lcat_key):
            st.session_state["w_loc_cat"] = t("lcat_all")
    # A loaded outfit set must be selectable in the current set category
    oset = data.get("w_outfit_set")
    if oset in OSET_KEYS and oset not in oset_keys_for_category(
            widget_option_value("w_set_cat") or "oscat_all"):
        st.session_state["w_set_cat"] = t("oscat_all")
    # A loaded pose must be selectable in the (possibly loaded) pose category
    pose = data.get("w_pose")
    if pose in PO_KEYS:
        cat_label = st.session_state.get("w_pose_cat", t("pc_all"))
        cat_key = next((k for k in PC_KEYS if t(k) == cat_label), "pc_all")
        if pose not in pose_keys_for_category(cat_key):
            st.session_state["w_pose_cat"] = t("pc_all")
    st.session_state["force_generate"] = True


def apply_look_preset():
    """Load a saved look: parse pasted JSON of option keys and set widgets."""
    try:
        data = json.loads(st.session_state.get("preset_paste", ""))
        if not isinstance(data, dict):
            raise ValueError("not a dict")
    except (ValueError, TypeError):
        st.session_state["preset_status"] = "error"
        return
    # A character.json (has "char_name") replaces the locked character
    is_character = isinstance(data.get("char_name"), str)
    if is_character:
        unlock_character()
    _apply_preset_dict(data)
    if is_character:
        _lock(data["char_name"].strip(),
              {wk: widget_option_value(wk) for wk in CHAR_WIDGETS})
        st.session_state["char_name_input"] = data["char_name"].strip()
    st.session_state["preset_status"] = "ok"


def apply_theme():
    """Apply the built-in theme selected in the sidebar, then generate."""
    label = st.session_state.get("w_theme")
    for theme_key, preset in THEME_PRESETS.items():
        if t(theme_key) == label:
            _apply_preset_dict({**LOOK_BASE, **SCENE_BASE, **preset})
            break


def request_photo_set():
    """Generate a set of prompt variations sharing subject/outfit/scene."""
    st.session_state["photo_set_request"] = True
    st.session_state["force_generate"] = True


def garment_picker(keys, label_key, widget_key, fab_label_key, fab_widget,
                   col_label_key, col_widget):
    """Garment selectbox plus fabric/color pickers (shown once a garment is
    chosen). Returns (garment_key, fabric_key, color_key)."""
    g_labels, _ = make_option(keys)
    g_sel = st.selectbox(t(label_key), g_labels, key=widget_key)
    g_key = keys[g_labels.index(g_sel)]
    fb_key, cp_key = "fab_none", "col_none"
    if g_key != keys[0]:
        fb_labels, _ = make_option(FB_KEYS)
        fb_key = FB_KEYS[fb_labels.index(st.selectbox(t(fab_label_key), fb_labels, key=fab_widget))]
        cp_labels, _ = make_option(CP_KEYS)
        cp_key = CP_KEYS[cp_labels.index(st.selectbox(t(col_label_key), cp_labels, key=col_widget))]
    return g_key, fb_key, cp_key


# Built-in theme presets: curated look + scene bundles applied through the
# same machinery as pasted look.json presets. Identity fields (gender, age,
# ethnicity) are deliberately absent so the chosen subject stays unchanged.
THEME_PRESETS = {
    "theme_golden_garden": {
        "w_hair": "hair_loose_waves", "w_hair_color": "hc_dark_brown",
        "w_bangs": "bangs_none", "w_expr": "expr_soft_gaze",
        "w_makeup": "mu_natural", "fashion_multi": [],
        "w_top": "top_tshirt", "top_fabric_sel": "fab_cotton",
        "top_color_sel": "col_white",
        "w_bottom": "bot_denim_shorts", "bot_fabric_sel": "fab_denim",
        "bot_color_sel": "col_blue", "w_shoes": "sh_sneakers",
        "w_location": "loc_brick_ruin", "w_tod": "tod_golden",
        "w_lighting": "lit_backlit", "w_season": "season_summer",
        "w_pstyle": "ps_nostalgic", "w_framing": "sf_medium",
        "w_cam_height": "ch_eye", "w_dof": "dof_fg_blur",
        "w_light_dir": "ld_back", "w_light_color": "lc_warm", "w_camera_film": "cf_portra",
        "atm_multi": ["atm_wind", "atm_dust"], "lfx_multi": ["lfx_flare"],
        "w_comp": "comp_framed", "w_pose": "pose_smell_flower",
        "w_pose_energy": "pe_relaxed",
    },
    "theme_neon_night": {
        "w_hair": "hair_straight", "w_hair_color": "hc_black",
        "w_bangs": "bangs_none", "w_expr": "expr_confident",
        "w_makeup": "mu_smoky", "fashion_multi": ["fs_streetwear"],
        "w_top": "top_none", "top_fabric_sel": "fab_none",
        "top_color_sel": "col_none",
        "w_bottom": "bot_none", "bot_fabric_sel": "fab_none",
        "bot_color_sel": "col_none", "w_shoes": "sh_chunky",
        "w_location": "loc_neon_alley", "w_tod": "tod_night",
        "w_lighting": "lit_neon", "w_season": "season_none",
        "w_pstyle": "ps_cyber", "w_framing": "sf_medium",
        "w_cam_height": "ch_low", "w_dof": "dof_bokeh_lights",
        "w_light_color": "lc_pink_blue", "w_camera_film": "cf_cinestill",
        "atm_multi": ["atm_puddles"], "lfx_multi": ["lfx_halation"],
        "w_comp": "comp_center", "w_pose": "pose_lean",
        "w_gaze": "gaze_camera", "w_pose_energy": "pe_cool",
    },
    "theme_cafe_film": {
        "w_hair": "hair_lob", "w_hair_color": "hc_milk_tea",
        "w_bangs": "bangs_see_through", "w_expr": "expr_smile",
        "w_makeup": "mu_natural", "fashion_multi": ["fs_korean"],
        "w_top": "top_none", "top_fabric_sel": "fab_none",
        "top_color_sel": "col_none",
        "w_bottom": "bot_none", "bot_fabric_sel": "fab_none",
        "bot_color_sel": "col_none", "w_shoes": "sh_none",
        "w_location": "loc_cafe", "w_tod": "tod_overcast",
        "w_lighting": "lit_window", "w_season": "season_autumn",
        "w_pstyle": "ps_vintage", "w_framing": "sf_medium_cu",
        "w_cam_height": "ch_eye", "w_cam_dir": "cd_front_3q", "w_dof": "dof_portrait",
        "w_light_quality": "lq_soft", "w_light_color": "lc_warm", "w_camera_film": "cf_gold",
        "lfx_multi": ["lfx_grain"],
        "w_comp": "comp_negative_space", "w_pose": "pose_hand_chin",
        "w_gaze": "gaze_away", "w_pose_energy": "pe_relaxed",
    },
    "theme_beach": {
        "w_hair": "hair_loose_waves", "w_hair_color": "hc_light_brown",
        "w_bangs": "bangs_none", "w_expr": "expr_laugh",
        "w_makeup": "mu_bronzed", "fashion_multi": ["fs_beach_cover"],
        "w_top": "top_none", "top_fabric_sel": "fab_none",
        "top_color_sel": "col_none",
        "w_bottom": "bot_none", "bot_fabric_sel": "fab_none",
        "bot_color_sel": "col_none", "w_shoes": "sh_barefoot",
        "w_location": "loc_beach", "w_tod": "tod_golden",
        "w_lighting": "lit_natural", "w_season": "season_summer",
        "w_pstyle": "ps_vivid", "w_framing": "sf_full",
        "w_cam_height": "ch_eye", "w_dof": "dof_shallow",
        "w_light_color": "lc_warm", "w_camera_film": "cf_superia", "atm_multi": ["atm_wind"],
        "w_comp": "comp_golden", "w_pose": "pose_shield_sun",
        "w_pose_energy": "pe_candid",
    },
    "theme_studio": {
        "w_hair": "hair_bun", "w_hair_color": "hc_black",
        "w_bangs": "bangs_none", "w_expr": "expr_fierce",
        "w_makeup": "mu_editorial", "fashion_multi": ["fs_elegant"],
        "w_top": "top_none", "top_fabric_sel": "fab_none",
        "top_color_sel": "col_none",
        "w_bottom": "bot_none", "bot_fabric_sel": "fab_none",
        "bot_color_sel": "col_none", "w_shoes": "sh_heels",
        "w_location": "loc_studio", "w_tod": "tod_none",
        "w_lighting": "lit_studio", "w_season": "season_none",
        "w_pstyle": "ps_editorial", "w_framing": "sf_medium",
        "w_cam_height": "ch_eye", "w_dof": "dof_clean_bg",
        "w_light_dir": "ld_clamshell", "w_light_quality": "lq_soft",
        "w_light_color": "lc_neutral", "w_camera_film": "cf_hasselblad",
        "w_comp": "comp_center", "w_pose": "pose_high_fashion",
        "w_gaze": "gaze_camera", "w_pose_energy": "pe_confident",
    },
    "theme_cherry": {
        "w_hair": "hair_half_up", "w_hair_color": "hc_dark_brown",
        "w_bangs": "bangs_see_through", "w_expr": "expr_bright_smile",
        "w_makeup": "mu_dewy", "fashion_multi": ["fs_korean"],
        "w_top": "top_none", "top_fabric_sel": "fab_none",
        "top_color_sel": "col_none",
        "w_bottom": "bot_none", "bot_fabric_sel": "fab_none",
        "bot_color_sel": "col_none", "w_shoes": "sh_mary_janes",
        "w_location": "loc_cherry", "w_tod": "tod_noon",
        "w_lighting": "lit_dappled", "w_season": "season_spring",
        "w_pstyle": "ps_soft", "w_framing": "sf_medium_full",
        "w_cam_height": "ch_slight_high", "w_dof": "dof_shallow",
        "w_light_quality": "lq_soft", "w_camera_film": "cf_fuji", "atm_multi": ["atm_petals"],
        "w_comp": "comp_depth", "w_pose": "pose_look_back_walk",
        "w_pose_energy": "pe_playful",
    },
    "theme_thai_temple": {
        "w_hair": "hair_thai_chignon", "w_hair_color": "hc_black",
        "w_bangs": "bangs_none", "w_expr": "expr_smile",
        "w_makeup": "mu_natural", "fashion_multi": [],
        "w_top": "top_none", "top_fabric_sel": "fab_none",
        "top_color_sel": "col_none",
        "w_bottom": "bot_none", "bot_fabric_sel": "fab_none",
        "bot_color_sel": "col_none", "w_shoes": "sh_none",
        "w_outfit_mode": "om_set", "w_outfit_set": "os_nat_th_chakkri",
        "w_location": "loc_th_wat", "w_tod": "tod_golden",
        "w_lighting": "lit_natural", "w_season": "season_none",
        "w_pstyle": "ps_editorial", "w_framing": "sf_medium_full",
        "w_cam_height": "ch_eye", "w_dof": "dof_portrait",
        "w_light_color": "lc_warm", "w_light_quality": "lq_soft",
        "w_comp": "comp_symmetry", "w_pose": "pose_wai",
        "w_gaze": "gaze_camera", "w_pose_energy": "pe_elegant",
    },
    "theme_kyoto_kimono": {
        "w_hair": "hair_jp_updo", "w_hair_color": "hc_black",
        "w_bangs": "bangs_none", "w_expr": "expr_soft_gaze",
        "w_makeup": "mu_natural", "fashion_multi": [],
        "w_top": "top_none", "top_fabric_sel": "fab_none",
        "top_color_sel": "col_none",
        "w_bottom": "bot_none", "bot_fabric_sel": "fab_none",
        "bot_color_sel": "col_none", "w_shoes": "sh_none",
        "w_outfit_mode": "om_set", "w_outfit_set": "os_nat_jp_furisode",
        "w_location": "loc_jp_gion", "w_tod": "tod_overcast",
        "w_lighting": "lit_natural", "w_season": "season_autumn",
        "w_pstyle": "ps_nostalgic", "w_framing": "sf_full",
        "w_cam_height": "ch_eye", "w_cam_dir": "cd_front_3q", "w_dof": "dof_shallow",
        "w_light_quality": "lq_soft", "w_camera_film": "cf_fuji",
        "atm_multi": ["atm_leaves"],
        "w_comp": "comp_leading", "w_pose": "pose_parasol",
        "w_gaze": "gaze_away", "w_pose_energy": "pe_elegant",
    },
    "theme_matsuri": {
        "w_hair": "hair_low_bun", "w_hair_color": "hc_dark_brown",
        "w_bangs": "bangs_wispy", "w_expr": "expr_bright_smile",
        "w_makeup": "mu_dewy", "fashion_multi": [],
        "w_top": "top_none", "top_fabric_sel": "fab_none",
        "top_color_sel": "col_none",
        "w_bottom": "bot_none", "bot_fabric_sel": "fab_none",
        "bot_color_sel": "col_none", "w_shoes": "sh_none",
        "w_outfit_mode": "om_set", "w_outfit_set": "os_nat_jp_yukata",
        "w_location": "loc_jp_matsuri", "w_tod": "tod_night",
        "w_lighting": "lit_lantern", "w_season": "season_none",
        "w_pstyle": "ps_cinematic", "w_framing": "sf_medium",
        "w_cam_height": "ch_eye", "w_dof": "dof_bokeh_lights",
        "w_light_color": "lc_warm", "w_camera_film": "cf_cinestill",
        "w_bg_people": "bgp_few", "lfx_multi": ["lfx_halation"],
        "w_comp": "comp_depth", "w_pose": "pose_look_back_walk",
        "w_pose_energy": "pe_playful",
    },
}


# ═══════════════════════════════════════════════════════════════════════════
#  4. CSS
# ═══════════════════════════════════════════════════════════════════════════

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@300;400;600;700&display=swap');
html, body, [class*="css"] {
    font-family: 'Noto Sans Thai', 'Segoe UI', Roboto, sans-serif;
}
@media (max-width: 768px) {
    .stButton > button { min-height: 52px !important; font-size: 1.1rem !important; border-radius: 12px !important; width: 100% !important; }
    .stSelectbox > div > div { min-height: 44px !important; }
    [data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; }
    .block-container { padding: 1rem 0.75rem !important; }
    .app-header h1 { font-size: 1.5rem !important; }
}
@media (min-width: 1400px) {
    .block-container { max-width: 1200px !important; margin: 0 auto !important; }
}
/* App header */
.app-header { padding: 0.25rem 0 0.75rem 0; }
.app-header h1 {
    margin: 0; font-size: 2rem; font-weight: 700; line-height: 1.25;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent;
}
.app-header p { margin: 0.25rem 0 0 0; opacity: 0.65; font-size: 0.95rem; }
/* Expander cards */
div[data-testid="stExpander"] {
    border: 1px solid rgba(102, 126, 234, 0.25) !important;
    border-radius: 14px !important;
    box-shadow: 0 1px 6px rgba(30, 30, 60, 0.06);
    margin-bottom: 0.6rem;
}
div[data-testid="stExpander"] summary { font-weight: 600; }
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important; font-weight: 600 !important; border: none !important;
    padding: 0.75rem 2rem !important; border-radius: 12px !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
}
.ref-attached { background: linear-gradient(135deg, #e0f7fa 0%, #e8f5e9 100%);
    border-left: 4px solid #00897b; padding: 10px 14px; border-radius: 8px; margin: 8px 0; font-size: 0.9rem; color: #1a1a2e; }
.stMultiSelect [data-baseweb="tag"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; border-radius: 20px !important; }
</style>
"""


# ═══════════════════════════════════════════════════════════════════════════
#  5. MAIN UI
# ═══════════════════════════════════════════════════════════════════════════

def main():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # ── Sidebar ──────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### Settings")
        lang_choice = st.radio("Language / ภาษา", ["English", "ภาษาไทย"], index=0, horizontal=True)
        st.session_state["lang"] = "en" if lang_choice == "English" else "th"
        # Widget state stores translated labels — clear it when the language
        # changes so stale labels can't collide with the new option lists
        if st.session_state.get("_prev_lang") not in (None, st.session_state["lang"]):
            for wk in LANG_DEPENDENT_WIDGETS:
                st.session_state.pop(wk, None)
        st.session_state["_prev_lang"] = st.session_state["lang"]
        st.divider()

        ar_keys = ["ar_1_1", "ar_16_9", "ar_9_16", "ar_4_5",
                   "ar_3_2", "ar_2_3", "ar_4_3", "ar_3_4",
                   "ar_iphone", "ar_android"]
        ar_labels, _ = make_option(ar_keys)
        ar_idx = st.selectbox(t("aspect_ratio"), ar_labels, index=0)
        ar_selected_key = ar_keys[ar_labels.index(ar_idx)]

        mt_labels, _ = make_option(MT_KEYS)
        mt_idx = st.selectbox(t("model_type"), mt_labels, index=0)
        mt_selected_key = MT_KEYS[mt_labels.index(mt_idx)]

        # Lens only affects photographic model types (index 1 = classic 35mm)
        lens_key = "lens_35"
        if mt_selected_key in PHOTO_MODEL_KEYS:
            lens_labels, _ = make_option(LENS_KEYS)
            lens_sel = st.selectbox(t("lens"), lens_labels, index=1)
            lens_key = LENS_KEYS[lens_labels.index(lens_sel)]

        pf_keys = ["platform_universal", "platform_midjourney", "platform_sd"]
        pf_labels, _ = make_option(pf_keys)
        pf_sel = st.selectbox(t("target_platform"), pf_labels, index=0)
        pf_selected_key = pf_keys[pf_labels.index(pf_sel)]
        # Prompt length: how wordy each option is in the generated prompt
        pl_labels = [t(k) for k in PL_KEYS]
        pl_sel = st.selectbox(t("prompt_len"), pl_labels,
                              index=PL_KEYS.index(prompt_len()),
                              key="w_prompt_len", on_change=request_generate,
                              help=t("prompt_len_hint"))
        st.session_state["prompt_len_key"] = PL_KEYS[pl_labels.index(pl_sel)]

        # Midjourney-only knobs, appended to the --ar parameter block
        mj_stylize = 100
        mj_seed = ""
        if pf_selected_key == "platform_midjourney":
            mj_stylize = st.number_input(t("mj_stylize"), min_value=0,
                                         max_value=1000, value=100, step=50)
            mj_seed = st.text_input(t("mj_seed"), value="")

        # ── Quick themes: curated look + scene bundles, one click ──
        st.divider()
        st.markdown(f"**🎨 {t('themes_header')}**")
        theme_labels = [t(k) for k in THEME_PRESETS]
        st.selectbox(t("theme_select"), theme_labels, key="w_theme")
        st.button(f"✨ {t('apply_theme_btn')}", on_click=apply_theme,
                  use_container_width=True)
        st.caption(t("theme_hint"))

        # ── Random Look style: everyday, or culture-matched national costumes ──
        st.divider()
        st.markdown(f"**{t('random_style_header')}**")
        st.selectbox(t("random_style"), [t(k) for k in RS_KEYS], key="w_random_style")
        st.caption(t("random_style_hint"))

        st.divider()
        st.caption("v6.2 — AI Prompt Generator")

    # ── Header ───────────────────────────────────────────────────────────
    st.markdown(
        f'<div class="app-header"><h1>🎨 {t("app_title")}</h1>'
        f'<p>{t("app_subtitle")}</p></div>',
        unsafe_allow_html=True,
    )

    # ── Simple mode: a short panel of essentials; the full editor below
    # stays mounted (hidden by CSS) so themes, Random Look and every
    # non-shown option keep working exactly as in full mode ──
    sm_col, reset_col = st.columns([3, 1])
    with sm_col:
        simple_mode = st.toggle(t("simple_mode"), value=True, key="simple_mode",
                                help=t("simple_hint"))
    with reset_col:
        st.button(f"↺ {t('reset_all')}", on_click=reset_all, use_container_width=True)
    if simple_mode:
        st.markdown("<style>.st-key-full_ui{display:none}</style>", unsafe_allow_html=True)
        render_simple_panel()

    with st.container(key="full_ui"):
        # ══════════════════════════════════════════════════════════════════════
        #  EXPANDER 1 — Subject
        # ══════════════════════════════════════════════════════════════════════
        with st.expander(f"👤  {t('exp_subject')}", expanded=True):
            # ── Character Lock ──
            enforce_character_lock()
            char_lock = st.session_state.get("char_lock")
            locked = bool(char_lock)
            st.markdown(f"**🔒 {t('char_lock_header')}**")
            if locked:
                lock_name = char_lock["name"] or t("char_unnamed")
                st.markdown(f'<div class="ref-attached">🔒 <b>{html_mod.escape(lock_name)}</b> '
                            f'{t("char_locked_msg")}</div>', unsafe_allow_html=True)
                cl1, cl2 = st.columns(2)
                with cl1:
                    st.button(f"🔓 {t('char_unlock_btn')}", on_click=unlock_character,
                              use_container_width=True)
                with cl2:
                    st.download_button(f"💾 {t('char_download')}",
                                       json.dumps({"char_name": char_lock["name"], **char_lock["data"]},
                                                  indent=2, ensure_ascii=False),
                                       file_name="character.json", mime="application/json",
                                       use_container_width=True)
                st.caption(t("char_json_hint"))
            else:
                st.caption(t("char_lock_hint"))
                cl1, cl2 = st.columns([2, 1])
                with cl1:
                    st.text_input(t("char_name"), placeholder=t("char_name_placeholder"),
                                  key="char_name_input")
                with cl2:
                    st.markdown("<div style='height:1.75rem'></div>", unsafe_allow_html=True)
                    st.button(f"🔒 {t('char_lock_btn')}", on_click=lock_character,
                              use_container_width=True)
                library = st.session_state.get("char_library", {})
                if library:
                    lb1, lb2, lb3 = st.columns([2, 1, 1])
                    with lb1:
                        st.selectbox(t("char_library"), list(library), key="w_char_lib")
                    with lb2:
                        st.markdown("<div style='height:1.75rem'></div>", unsafe_allow_html=True)
                        st.button(f"📂 {t('char_load_btn')}", on_click=load_library_character,
                                  use_container_width=True)
                    with lb3:
                        st.markdown("<div style='height:1.75rem'></div>", unsafe_allow_html=True)
                        st.button(f"🗑️ {t('char_delete_btn')}", on_click=delete_library_character,
                                  use_container_width=True)
                    st.caption(t("saved_in_browser"))
            st.markdown("---")

            # Reference photo checkbox (no file uploader — just a toggle)
            attach_subject = st.checkbox(t("attach_subject_photo"), key="attach_subject")
            if attach_subject:
                st.markdown(f'<div class="ref-attached">📎 {t("attach_subject_note")}</div>', unsafe_allow_html=True)

            def pick(keys, label_key, widget_key, index=0, **kw):
                """Selectbox over option keys → selected key (locked if part of the character)."""
                labels, _ = make_option(keys)
                sel = st.selectbox(t(label_key), labels, index=index, key=widget_key,
                                   format_func=grouped(keys),
                                   disabled=locked and widget_key in CHAR_WIDGETS, **kw)
                return keys[labels.index(sel)]

            # ── Identity ──
            st.markdown(f"**{t('sub_identity')}**")
            col1, col2, col3 = st.columns(3)
            with col1:
                gd_key = pick(GD_KEYS, "gender", "w_gender", on_change=reset_hair_on_gender_change)
                gd_labels, _ = make_option(GD_KEYS)
            with col2:
                ag_key = pick(AG_KEYS, "age_group", "w_age", index=1)
            with col3:
                et_key = pick(ET_KEYS, "ethnicity", "w_eth", index=1)
            col_st, col_bt, col_ap = st.columns(3)
            with col_st:
                st_key = pick(ST_KEYS, "skin_tone", "w_skin_tone")
            with col_bt:
                bt_key = pick(BT_KEYS, "body_type", "w_body", index=1)
            with col_ap:
                ap_key = pick(AP_KEYS, "appearance", "w_appearance", index=1)

            # ── Face details (all optional) ──
            st.markdown(f"**{t('sub_face')}**")
            fc1, fc2, fc3 = st.columns(3)
            with fc1:
                fsh_key = pick(FSH_KEYS, "face_shape", "w_face_shape")
            with fc2:
                eye_key = pick(EYE_KEYS, "eye_shape", "w_eye_shape")
            with fc3:
                ec_key = pick(EC_KEYS, "eye_color", "w_eye_color")
            fc4, fc5, fc6 = st.columns(3)
            with fc4:
                brow_key = pick(BROW_KEYS, "brows", "w_brows")
            with fc5:
                lip_key = pick(LIP_KEYS, "lips", "w_lips")
            with fc6:
                skf_key = pick(SKF_KEYS, "skin_finish", "w_skin_finish")
            fm_labels = [t(k) for k in FM_KEYS]
            fm_selected = st.multiselect(t("face_marks"), fm_labels, default=[], key="face_marks",
                                         help=t("face_marks_help"), disabled=locked)
            fm_keys = [FM_KEYS[fm_labels.index(lbl)] for lbl in fm_selected]
            fh_key = "fh_none"
            if gd_key != "gender_female":
                col_fh, _ = st.columns(2)
                with col_fh:
                    fh_key = pick(FH_KEYS, "facial_hair", "w_facial_hair")

            # ── Hair ──
            st.markdown(f"**{t('sub_hair')}**")
            col4, col5 = st.columns(2)
            with col4:
                hr_key = pick(hair_keys_for_gender(gd_key), "hair_style", "w_hair", index=1)
            with col5:
                hc_key = pick(HC_KEYS, "hair_color", "w_hair_color", index=1)
            col_bn, col_hf = st.columns(2)
            with col_bn:
                bn_key = pick(BN_KEYS, "bangs", "w_bangs")
            with col_hf:
                hf_key = pick(HF_KEYS, "hair_finish", "w_hair_finish")

            # ── Expression, makeup & nails ──
            st.markdown(f"**{t('sub_expression')}**")
            col_ex, col_mu, col_nl = st.columns(3)
            with col_ex:
                ex_key = pick(EX_KEYS, "expression", "w_expr", index=1)
            with col_mu:
                mu_key = pick(MU_KEYS, "makeup", "w_makeup")
            with col_nl:
                nl_key = pick(NL_KEYS, "nails", "w_nails")

            # ── People & companion ──
            st.markdown(f"**{t('sub_people')}**")
            col_ns, col_pet = st.columns(2)
            with col_ns:
                ns_labels, _ = make_option(NS_KEYS)
                ns_sel = st.selectbox(t("num_subjects"), ns_labels)
                ns_key = NS_KEYS[ns_labels.index(ns_sel)]
            with col_pet:
                pet_key = pick(PET_KEYS, "companion", "w_pet")

            # Per-person looks so a duo/trio doesn't come out as identical clones.
            # Person 1 uses the main selectors above; each extra person gets their
            # own gender / hair / hair color / expression (staggered defaults on
            # purpose). The hairstyle pool follows that person's own gender.
            extra_person_keys = []
            gm_key = "gg_same"
            if ns_key in ("ns_duo", "ns_trio"):
                st.caption(t("multi_person_hint"))
                for pi in range(2, 3 if ns_key == "ns_duo" else 4):
                    st.markdown(f"**{t(f'person_{pi}')}**")
                    pc0, pc1, pc2, pc3 = st.columns(4)
                    with pc0:
                        p_gd_sel = st.selectbox(
                            t("gender"), gd_labels,
                            index=GD_KEYS.index(gd_key),
                            key=f"w_gender_p{pi}",
                            on_change=reset_person_hair,
                            args=(f"w_hair_p{pi}",))
                        p_gd_key = GD_KEYS[gd_labels.index(p_gd_sel)]
                    with pc1:
                        p_hr_options = hair_keys_for_gender(p_gd_key)
                        p_hr_labels, _ = make_option(p_hr_options)
                        p_hr_sel = st.selectbox(
                            t("hair_style"), p_hr_labels,
                            index=min(1 + 3 * (pi - 1), len(p_hr_options) - 1),
                            format_func=grouped(p_hr_options),
                            key=f"w_hair_p{pi}")
                        p_hr_key = p_hr_options[p_hr_labels.index(p_hr_sel)]
                    with pc2:
                        p_hc_labels, _ = make_option(HC_KEYS)
                        p_hc_sel = st.selectbox(
                            t("hair_color"), p_hc_labels,
                            index=min(1 + 6 * (pi - 1), len(HC_KEYS) - 1),
                            format_func=grouped(HC_KEYS),
                            key=f"w_hair_color_p{pi}")
                        p_hc_key = HC_KEYS[p_hc_labels.index(p_hc_sel)]
                    with pc3:
                        p_ex_labels, _ = make_option(EX_KEYS)
                        p_ex_sel = st.selectbox(
                            t("expression"), p_ex_labels,
                            index=min(2 + 9 * (pi - 2), len(EX_KEYS) - 1),
                            format_func=grouped(EX_KEYS),
                            key=f"w_expr_p{pi}")
                        p_ex_key = EX_KEYS[p_ex_labels.index(p_ex_sel)]
                    extra_person_keys.append((p_gd_key, p_hr_key, p_hc_key, p_ex_key))
            elif ns_key == "ns_group":
                st.caption(t("group_hint"))
                col_gm, _ = st.columns(2)
                with col_gm:
                    gm_labels, _ = make_option(GM_KEYS)
                    gm_sel = st.selectbox(t("group_mix"), gm_labels, key="w_group_mix")
                    gm_key = GM_KEYS[gm_labels.index(gm_sel)]

        # ══════════════════════════════════════════════════════════════════════
        #  EXPANDER 2 — Outfit & Style
        # ══════════════════════════════════════════════════════════════════════
        with st.expander(f"👗  {t('exp_outfit')}", expanded=True):
            # Fashion presets (grouped: everyday, trend, occasions, sport, traditional)
            fs_labels = [t(k) for k in FS_KEYS]
            fs_selected_labels = st.multiselect(t("fashion_presets"), fs_labels, default=[],
                                                 help=t("fashion_presets_help"), key="fashion_multi",
                                                 format_func=grouped(FS_KEYS))
            fs_selected_keys = [FS_KEYS[fs_labels.index(lbl)] for lbl in fs_selected_labels]

            st.markdown("---")

            # Outfit type: separates (top + bottom), a dress / one-piece, or a
            # ready-made seasonal set. Only the active type's garments are used.
            om_labels, _ = make_option(OM_KEYS)
            om_sel = st.radio(t("outfit_mode"), om_labels, horizontal=True, key="w_outfit_mode")
            om_key = OM_KEYS[om_labels.index(om_sel)]

            top_key, top_fb_key, top_cp_key = "top_none", "fab_none", "col_none"
            bot_key, bot_fb_key, bot_cp_key = "bot_none", "fab_none", "col_none"
            dr_key, dr_fb_key, dr_cp_key = "dress_none", "fab_none", "col_none"
            os_key = "os_none"
            out_key, out_cp_key = "out_none", "col_none"
            fit_key, leg_key, sh_key = "fit_none", "leg_none", "sh_none"
            det_selected_keys = []

            # Garments default to "None" so a fashion preset alone fully defines
            # the outfit; fabric/color pickers only appear once a garment is chosen.
            if om_key == "om_separates":
                col_top, col_bot = st.columns(2)
                with col_top:
                    top_key, top_fb_key, top_cp_key = garment_picker(
                        TOP_KEYS, "top_garment", "w_top",
                        "top_fabric", "top_fabric_sel", "top_color", "top_color_sel")
                with col_bot:
                    bot_key, bot_fb_key, bot_cp_key = garment_picker(
                        BOT_KEYS, "bottom_garment", "w_bottom",
                        "bot_fabric", "bot_fabric_sel", "bot_color", "bot_color_sel")
            elif om_key == "om_dress":
                col_dr, _ = st.columns(2)
                with col_dr:
                    dr_key, dr_fb_key, dr_cp_key = garment_picker(
                        DR_KEYS, "dress_garment", "w_dress",
                        "dress_fabric", "dress_fabric_sel", "dress_color", "dress_color_sel")
            else:
                # Two-level picker: category → set ("All" lists everything)
                col_sc, col_os = st.columns(2)
                with col_sc:
                    oscat_labels, _ = make_option(OSCAT_KEYS)
                    oscat_sel = st.selectbox(t("outfit_set_category"), oscat_labels,
                                             key="w_set_cat",
                                             on_change=reset_set_on_category_change)
                    oscat_key = OSCAT_KEYS[oscat_labels.index(oscat_sel)]
                with col_os:
                    os_options = oset_keys_for_category(oscat_key)
                    os_labels, _ = make_option(os_options)
                    if st.session_state.get("w_outfit_set") not in os_labels:
                        st.session_state.pop("w_outfit_set", None)
                    os_sel = st.selectbox(t("outfit_set"), os_labels, index=1, key="w_outfit_set")
                    os_key = os_options[os_labels.index(os_sel)]
                st.caption(t("outfit_set_hint"))

            # Gentle warning when a preset style and explicit garments are mixed
            if fs_selected_keys and (top_key != "top_none" or bot_key != "bot_none"
                                     or dr_key != "dress_none" or os_key != "os_none"):
                st.caption(t("outfit_clash_hint"))

            # Layers & finishing — a ready-made set already includes all of these
            if om_key != "om_set":
                col_out, col_outc = st.columns(2)
                with col_out:
                    out_labels, _ = make_option(OUT_KEYS)
                    out_sel = st.selectbox(t("outer_layer"), out_labels, key="w_outer")
                    out_key = OUT_KEYS[out_labels.index(out_sel)]
                with col_outc:
                    if out_key != "out_none":
                        out_cp_labels, _ = make_option(CP_KEYS)
                        out_cp_sel = st.selectbox(t("outer_color"), out_cp_labels, key="outer_color_sel")
                        out_cp_key = CP_KEYS[out_cp_labels.index(out_cp_sel)]
                col_fit, col_leg, col_sh = st.columns(3)
                with col_fit:
                    fit_labels, _ = make_option(FIT_KEYS)
                    fit_sel = st.selectbox(t("fit"), fit_labels, key="w_fit")
                    fit_key = FIT_KEYS[fit_labels.index(fit_sel)]
                with col_leg:
                    leg_labels, _ = make_option(LEG_KEYS)
                    leg_sel = st.selectbox(t("legwear"), leg_labels, key="w_legwear")
                    leg_key = LEG_KEYS[leg_labels.index(leg_sel)]
                with col_sh:
                    sh_labels, _ = make_option(SH_KEYS)
                    sh_sel = st.selectbox(t("footwear"), sh_labels, key="w_shoes")
                    sh_key = SH_KEYS[sh_labels.index(sh_sel)]
                det_labels = [t(k) for k in DET_KEYS]
                det_selected_labels = st.multiselect(t("details"), det_labels, default=[],
                                                     help=t("details_help"), key="detail_multi")
                det_selected_keys = [DET_KEYS[det_labels.index(lbl)] for lbl in det_selected_labels]

            st.markdown("---")
            outfit_text = st.text_input(t("outfit_input"), placeholder=t("outfit_placeholder"))

            # Outfit reference checkbox
            attach_outfit = st.checkbox(t("attach_outfit_photo"), key="attach_outfit")
            if attach_outfit:
                st.markdown(f'<div class="ref-attached">📎 {t("attach_outfit_note")}</div>', unsafe_allow_html=True)

            # ── Accessories: grouped checkboxes ──
            st.markdown(f"**{t('accessories')}**")
            acc_selected = []

            acc_head_keys = ["acc_beanie", "acc_beret", "acc_bucket_hat", "acc_cap",
                             "acc_flower_hair",
                             "acc_glasses", "acc_hair_clip", "acc_ribbon", "acc_hat",
                             "acc_headband", "acc_scrunchie", "acc_sunglasses", "acc_tiara"]
            acc_body_keys = ["acc_anklet", "acc_belt", "acc_bowtie", "acc_bracelet",
                             "acc_choker", "acc_earrings", "acc_necklace", "acc_necktie",
                             "acc_ring", "acc_scarf", "acc_watch"]
            acc_carried_keys = ["acc_backpack", "acc_book", "acc_camera", "acc_clutch",
                                "acc_crossbody", "acc_bouquet", "acc_fan", "acc_bag", "acc_coffee",
                                "acc_parasol",
                                "acc_phone", "acc_tote", "acc_umbrella"]

            st.caption(t("acc_group_head"))
            head_cols = st.columns(4)
            for i, ak in enumerate(acc_head_keys):
                with head_cols[i % 4]:
                    if st.checkbox(t(ak), key=f"acc_{ak}"):
                        acc_selected.append(ak)

            st.caption(t("acc_group_body"))
            body_cols = st.columns(4)
            for i, ak in enumerate(acc_body_keys):
                with body_cols[i % 4]:
                    if st.checkbox(t(ak), key=f"acc_{ak}"):
                        acc_selected.append(ak)

            st.caption(t("acc_group_carried"))
            carried_cols = st.columns(4)
            for i, ak in enumerate(acc_carried_keys):
                with carried_cols[i % 4]:
                    if st.checkbox(t(ak), key=f"acc_{ak}"):
                        acc_selected.append(ak)

        # ══════════════════════════════════════════════════════════════════════
        #  EXPANDER 3 — Pose & Body Language
        # ══════════════════════════════════════════════════════════════════════
        with st.expander(f"🕺  {t('exp_pose')}", expanded=True):
            # Pose reference (e.g. a mannequin pose sheet) — copies only the body
            # position, so the pose pickers are disabled while it's on
            attach_pose = st.checkbox(t("attach_pose_photo"), key="attach_pose")
            if attach_pose:
                st.markdown(f'<div class="ref-attached">📎 {t("attach_pose_note")}</div>', unsafe_allow_html=True)

            # Two-level picker: category → pose (category "All" shows every pose)
            col_pc, col_po = st.columns(2)
            with col_pc:
                pc_labels, _ = make_option(PC_KEYS)
                pc_sel = st.selectbox(t("pose_category"), pc_labels, key="w_pose_cat",
                                      format_func=grouped(PC_KEYS),
                                      on_change=reset_pose_on_category_change,
                                      disabled=attach_pose)
                pc_key = PC_KEYS[pc_labels.index(pc_sel)]
            with col_po:
                po_options = pose_keys_for_category(pc_key)
                po_labels, _ = make_option(po_options)
                if st.session_state.get("w_pose") not in po_labels:
                    st.session_state.pop("w_pose", None)
                po_sel = st.selectbox(t("pose"), po_labels, key="w_pose", disabled=attach_pose,
                                      format_func=grouped(po_options))
                po_key = po_options[po_labels.index(po_sel)]

            # Fine-tuning: orientation / head / hands / legs are pose-specific;
            # gaze and mood apply to any pose (and to every Photo Set shot)
            st.markdown(f"**{t('pose_detail_header')}**")
            st.caption(t("pose_detail_hint"))
            pose_detail_keys = {}
            detail_specs = [("w_body_dir", "body_dir"), ("w_head", "head_pos"),
                            ("w_hands", "hands_pos"), ("w_legs", "legs_pos")]
            detail_cols = st.columns(4)
            for col, (wk, label_key) in zip(detail_cols, detail_specs):
                with col:
                    opts = POSE_DETAIL_WIDGETS[wk]
                    d_labels, _ = make_option(opts)
                    d_sel = st.selectbox(t(label_key), d_labels, key=wk, disabled=attach_pose)
                    pose_detail_keys[wk] = opts[d_labels.index(d_sel)]
            col_gz, col_pe = st.columns(2)
            with col_gz:
                gz_labels, _ = make_option(GZ_KEYS)
                gz_sel = st.selectbox(t("gaze"), gz_labels, key="w_gaze")
                gz_key = GZ_KEYS[gz_labels.index(gz_sel)]
            with col_pe:
                pe_labels, _ = make_option(PE_KEYS)
                pe_sel = st.selectbox(t("pose_energy"), pe_labels, key="w_pose_energy")
                pe_key = PE_KEYS[pe_labels.index(pe_sel)]
            pose_text = st.text_input(t("pose_text"), placeholder=t("pose_text_placeholder"),
                                      key="pose_text_input")

        # ══════════════════════════════════════════════════════════════════════
        #  EXPANDER 4 — Scene & Lighting
        # ══════════════════════════════════════════════════════════════════════
        with st.expander(f"🌅  {t('exp_scene')}", expanded=True):
            # Scene reference checkbox
            attach_scene = st.checkbox(t("attach_scene_photo"), key="attach_scene")
            if attach_scene:
                st.markdown(f'<div class="ref-attached">📎 {t("attach_scene_note")}</div>', unsafe_allow_html=True)

            # Location mode
            scene_mode_labels = [t("scene_mode_preset"), t("scene_mode_custom"), t("scene_mode_place")]
            scene_mode = st.radio(t("scene_mode"), scene_mode_labels, index=0, horizontal=True, key="scene_mode_radio")

            lo_key = "loc_studio"
            scene_custom_text = ""
            place_landmark = ""
            place_city = ""
            place_country = ""

            if scene_mode == scene_mode_labels[0]:
                # Two-level picker: category → location ("All" lists everything)
                col_lc, col_lo = st.columns(2)
                with col_lc:
                    lcat_labels, _ = make_option(LCAT_KEYS)
                    lcat_sel = st.selectbox(t("location_category"), lcat_labels, key="w_loc_cat",
                                            format_func=grouped(LCAT_KEYS),
                                            on_change=reset_location_on_category_change)
                    lcat_key = LCAT_KEYS[lcat_labels.index(lcat_sel)]
                with col_lo:
                    lo_options = loc_keys_for_category(lcat_key)
                    lo_labels, _ = make_option(lo_options)
                    if st.session_state.get("w_location") not in lo_labels:
                        st.session_state.pop("w_location", None)
                    lo_sel = st.selectbox(t("location"), lo_labels, index=1, key="w_location",
                                          format_func=grouped(lo_options))
                    lo_key = lo_options[lo_labels.index(lo_sel)]
            elif scene_mode == scene_mode_labels[1]:
                scene_custom_text = st.text_area(t("scene_custom_input"),
                                                  placeholder=t("scene_custom_placeholder"),
                                                  height=80, key="scene_custom_ta")
            else:
                col_pl1, col_pl2, col_pl3 = st.columns(3)
                with col_pl1:
                    place_landmark = st.text_input(t("place_landmark"),
                                                   placeholder=t("place_landmark_placeholder"),
                                                   key="place_landmark_input")
                with col_pl2:
                    place_city = st.text_input(t("place_city"),
                                               placeholder=t("place_city_placeholder"),
                                               key="place_city_input")
                with col_pl3:
                    place_country = st.text_input(t("place_country"),
                                                  placeholder=t("place_country_placeholder"),
                                                  key="place_country_input")

            st.markdown("---")
            col10, col_season, col_bgp = st.columns(3)
            with col10:
                td_labels, _ = make_option(TD_KEYS)
                td_sel = st.selectbox(t("time_of_day"), td_labels, index=TD_DEFAULT, key="w_tod",
                                      format_func=grouped(TD_KEYS))
                td_key = TD_KEYS[td_labels.index(td_sel)]
            with col_season:
                sn_labels, _ = make_option(SN_KEYS)
                sn_sel = st.selectbox(t("season"), sn_labels, key="w_season")
                sn_key = SN_KEYS[sn_labels.index(sn_sel)]
            with col_bgp:
                bgp_labels, _ = make_option(BGP_KEYS)
                bgp_sel = st.selectbox(t("bg_people"), bgp_labels, key="w_bg_people")
                bgp_key = BGP_KEYS[bgp_labels.index(bgp_sel)]
            atm_labels = [t(k) for k in ATM_KEYS]
            atm_selected = st.multiselect(t("atmosphere"), atm_labels, default=[],
                                          help=t("atmosphere_help"), key="atm_multi")
            atm_keys = [ATM_KEYS[atm_labels.index(lbl)] for lbl in atm_selected]

            # ── Lighting: style + direction + color + quality ──
            st.markdown(f"**{t('sub_lighting')}**")
            col11, col_ld, col_lc2, col_lq = st.columns(4)
            with col11:
                lt_labels, _ = make_option(LT_KEYS)
                lt_sel = st.selectbox(t("lighting"), lt_labels, index=1, key="w_lighting",
                                      format_func=grouped(LT_KEYS))
                lt_key = LT_KEYS[lt_labels.index(lt_sel)]
            with col_ld:
                ld_labels, _ = make_option(LD_KEYS)
                ld_sel = st.selectbox(t("light_dir"), ld_labels, key="w_light_dir")
                ld_key = LD_KEYS[ld_labels.index(ld_sel)]
            with col_lc2:
                lc_labels, _ = make_option(LC_KEYS)
                lc_sel = st.selectbox(t("light_color"), lc_labels, key="w_light_color")
                lc_key = LC_KEYS[lc_labels.index(lc_sel)]
            with col_lq:
                lq_labels, _ = make_option(LQ_KEYS)
                lq_sel = st.selectbox(t("light_quality"), lq_labels, key="w_light_quality")
                lq_key = LQ_KEYS[lq_labels.index(lq_sel)]

            # ── Camera: framing + height + position + special shot ──
            st.markdown(f"**{t('sub_camera')}**")
            st.caption(t("cam_hint"))
            col12, col_ch, col_cd, col_cs = st.columns(4)
            with col12:
                sf_labels, _ = make_option(SF_KEYS)
                sf_sel = st.selectbox(t("shot_framing"), sf_labels, index=2, key="w_framing",
                                      format_func=grouped(SF_KEYS))
                sf_key = SF_KEYS[sf_labels.index(sf_sel)]
            with col_ch:
                ch_labels, _ = make_option(CH_KEYS)
                ch_sel = st.selectbox(t("cam_height"), ch_labels,
                                      index=CH_KEYS.index("ch_eye"), key="w_cam_height")
                ch_key = CH_KEYS[ch_labels.index(ch_sel)]
            with col_cd:
                cd_labels, _ = make_option(CD_KEYS)
                cd_sel = st.selectbox(t("cam_dir"), cd_labels, key="w_cam_dir")
                cd_key = CD_KEYS[cd_labels.index(cd_sel)]
            with col_cs:
                cs_labels, _ = make_option(CS_KEYS)
                cs_sel = st.selectbox(t("cam_special"), cs_labels, key="w_cam_special")
                cs_key = CS_KEYS[cs_labels.index(cs_sel)]
            cam_preview = " · ".join(eng(k) for k in (sf_key, ch_key, cd_key, cs_key) if eng(k))
            if cam_preview:
                st.caption(f"📷 {t('cam_preview')} *{cam_preview}*")

            col14, col15, col_ps = st.columns(3)
            with col14:
                dof_labels, _ = make_option(DOF_KEYS)
                dof_sel = st.selectbox(t("dof"), dof_labels, index=2, key="w_dof")
                dof_key = DOF_KEYS[dof_labels.index(dof_sel)]
            with col15:
                cmp_labels, _ = make_option(CMP_KEYS)
                cmp_sel = st.selectbox(t("composition"), cmp_labels, key="w_comp")
                cmp_key = CMP_KEYS[cmp_labels.index(cmp_sel)]
            with col_ps:
                ps_labels, _ = make_option(PS_KEYS)
                ps_sel = st.selectbox(t("picture_style"), ps_labels, key="w_pstyle",
                                      format_func=grouped(PS_KEYS))
                ps_key = PS_KEYS[ps_labels.index(ps_sel)]

            # Camera body / film stock only makes sense for photographic models
            cf_key = "cf_none"
            col_cf, col_lfx = st.columns([1, 2])
            if mt_selected_key in PHOTO_MODEL_KEYS:
                with col_cf:
                    cf_labels, _ = make_option(CF_KEYS)
                    cf_sel = st.selectbox(t("camera_film"), cf_labels, key="w_camera_film")
                    cf_key = CF_KEYS[cf_labels.index(cf_sel)]
            with col_lfx:
                lfx_labels = [t(k) for k in LFX_KEYS]
                lfx_selected = st.multiselect(t("lens_fx"), lfx_labels, default=[],
                                              help=t("lens_fx_help"), key="lfx_multi")
                lfx_keys = [LFX_KEYS[lfx_labels.index(lbl)] for lbl in lfx_selected]

        # ══════════════════════════════════════════════════════════════════════
        #  EXPANDER 5 — Advanced
        # ══════════════════════════════════════════════════════════════════════
        with st.expander(f"⚙️  {t('exp_advanced')}", expanded=False):
            custom_text = st.text_area(t("custom_prompt"), placeholder=t("custom_placeholder"), height=80)
            negative_text = st.text_area(t("negative_prompt"), placeholder=t("negative_placeholder"), height=80)
            st.markdown(f"**{t('quality_tags')}**")
            qt_keys = ["qt_8k", "qt_detail", "qt_sharp", "qt_pro", "qt_award", "qt_magazine"]
            qt_cols = st.columns(3)
            qt_selected = []
            for i, qk in enumerate(qt_keys):
                with qt_cols[i % 3]:
                    if st.checkbox(t(qk), value=(qk in ("qt_8k", "qt_detail", "qt_sharp"))):
                        qt_selected.append(qk)

            # ── Save / Load Look ──
            # Presets store language-independent option KEYS, so a look saved in
            # Thai loads fine in English (and vice versa).
            st.markdown("---")
            st.markdown(f"**💾 {t('save_load_header')}**")
            current_look = {
                "w_gender": gd_key, "w_age": ag_key, "w_eth": et_key,
                "w_hair": hr_key, "w_hair_color": hc_key, "w_bangs": bn_key,
                "w_expr": ex_key, "w_body": bt_key, "w_appearance": ap_key,
                "w_makeup": mu_key,
                "w_top": top_key, "top_fabric_sel": top_fb_key, "top_color_sel": top_cp_key,
                "w_bottom": bot_key, "bot_fabric_sel": bot_fb_key, "bot_color_sel": bot_cp_key,
                "w_shoes": sh_key, "fashion_multi": fs_selected_keys,
                "w_group_mix": gm_key, "w_pet": pet_key,
                "w_location": lo_key, "w_tod": td_key, "w_lighting": lt_key,
                "w_season": sn_key, "w_pstyle": ps_key, "w_framing": sf_key,
                "w_dof": dof_key, "w_comp": cmp_key, "w_pose": po_key,
                "w_pose_cat": pc_key, "w_gaze": gz_key, "w_pose_energy": pe_key,
                **pose_detail_keys,
                "w_outfit_mode": om_key, "w_dress": dr_key,
                "dress_fabric_sel": dr_fb_key, "dress_color_sel": dr_cp_key,
                "w_outfit_set": os_key, "w_outer": out_key, "outer_color_sel": out_cp_key,
                "w_fit": fit_key, "w_legwear": leg_key, "detail_multi": det_selected_keys,
                "w_skin_tone": st_key, "w_face_shape": fsh_key, "w_eye_shape": eye_key,
                "w_eye_color": ec_key, "w_brows": brow_key, "w_lips": lip_key,
                "face_marks": fm_keys, "w_facial_hair": fh_key, "w_skin_finish": skf_key,
                "w_hair_finish": hf_key, "w_nails": nl_key,
                "w_cam_height": ch_key, "w_cam_dir": cd_key, "w_cam_special": cs_key,
                "w_camera_film": cf_key, "w_light_dir": ld_key, "w_light_color": lc_key,
                "w_light_quality": lq_key, "w_bg_people": bgp_key,
                "atm_multi": atm_keys, "lfx_multi": lfx_keys,
            }
            if scene_mode == scene_mode_labels[0]:
                current_look["w_loc_cat"] = lcat_key
            if om_key == "om_set":
                current_look["w_set_cat"] = oscat_key
            # Extra persons (duo/trio) — only present while those rows are shown
            for pi, (p_gd, p_hr, p_hc, p_ex) in enumerate(extra_person_keys, start=2):
                current_look[f"w_gender_p{pi}"] = p_gd
                current_look[f"w_hair_p{pi}"] = p_hr
                current_look[f"w_hair_color_p{pi}"] = p_hc
                current_look[f"w_expr_p{pi}"] = p_ex
            st.download_button(f"💾 {t('save_look')}",
                               json.dumps(current_look, indent=2),
                               file_name="look.json", mime="application/json")
            st.text_area(t("load_look_paste"), height=80, key="preset_paste")
            st.button(f"📂 {t('load_look')}", on_click=apply_look_preset)
            preset_status = st.session_state.pop("preset_status", None)
            if preset_status == "ok":
                st.success(t("preset_loaded"))
            elif preset_status == "error":
                st.error(t("preset_invalid"))

    # ══════════════════════════════════════════════════════════════════════
    #  6. GENERATE
    # ══════════════════════════════════════════════════════════════════════
    st.markdown("")
    gen_col, rand_col, scene_col, set_col = st.columns([1, 1, 1, 1])
    with gen_col:
        generate_clicked = st.button(f"🚀  {t('generate_btn')}", type="primary", use_container_width=True)
    with rand_col:
        st.button(f"🎲  {t('random_btn')}", on_click=randomize_look, use_container_width=True)
    with scene_col:
        st.button(f"🎬  {t('random_scene_btn')}", on_click=randomize_scene, use_container_width=True)
    with set_col:
        st.button(f"📸  {t('photo_set_btn')}", on_click=request_photo_set, use_container_width=True)
    # Random Look callback sets new widget values, then requests a generate
    if st.session_state.pop("force_generate", False):
        generate_clicked = True

    st.markdown("---")
    st.markdown(f"### {t('result_header')}")

    if generate_clicked:
        # ── Build each section ──
        # Technical — lens spec only makes sense for photographic model types
        specs = [eng(mt_selected_key)]
        if mt_selected_key in PHOTO_MODEL_KEYS:
            specs.append(eng(lens_key))
        if eng(cf_key):
            specs.append(eng(cf_key))
        for qk in qt_selected:
            specs.append(eng(qk))
        technical = ", ".join(s for s in specs if s)

        # Subject (with skin tone + body type + appearance).
        # Every field may be "None / Not specified" — empty parts are skipped.
        # The main person's face details, hair, expression, makeup and nails
        # form one description, reused for solo / person 1 / the group centre.
        eyes = " ".join(x for x in (eng(eye_key), eng(ec_key)) if x)
        face_bits = [eng(fsh_key), f"{eyes} eyes" if eyes else ""] + \
            [eng(k) for k in [brow_key, lip_key] + fm_keys + [fh_key]]
        face_bits = [b for b in face_bits if b]
        main_look = ", ".join(p for p in (
            "with " + ", ".join(face_bits) if face_bits else "",
            look_desc(hr_key, hc_key, bn_key, ex_key, mu_key, hf_key),
            eng(nl_key)) if p)
        look_part = f", {main_look}" if main_look else ""
        traits = [v for v in (eng(st_key), eng(bt_key), eng(ap_key)) if v]
        trait_part = f", {', '.join(traits)}" if traits else ""
        # Character Lock: an optional name + a consistency instruction
        char_name = char_lock["name"] if locked else ""
        if attach_subject:
            subject = ("a photo of the exact same person as in the attached reference photo, "
                       "preserving their facial identity and features precisely"
                       + trait_part + look_part)
        elif ns_key == "ns_solo":
            head = " ".join(x for x in (eng(ag_key), eng(et_key), eng(gd_key)) if x)
            subject = f"a {head}" + trait_part + look_part
            if char_name:
                subject = f"{char_name}, {subject}"
        elif ns_key in ("ns_duo", "ns_trio"):
            # Distinct per-person descriptions so the AI can tell them apart;
            # each extra person has their own gender, hair and expression.
            ordinals = ["first", "second", "third"]
            persons = [(gd_key, main_look)]
            for (p_gd, p_hr, p_hc, p_ex) in extra_person_keys:
                persons.append((p_gd, look_desc(p_hr, p_hc, None, p_ex)))
            mixed_genders = len({p[0] for p in persons}) > 1
            head = " ".join(x for x in (eng(ns_key), eng(ag_key), eng(et_key)) if x)
            head += " people" if mixed_genders else f" {eng(gd_key)}s"
            person_descs = []
            for i, (p_gd, p_look) in enumerate(persons):
                desc_bits = []
                if mixed_genders:
                    desc_bits.append(f"a {eng(p_gd).lower()}")
                if p_look:
                    desc_bits.append(p_look)
                if desc_bits:
                    who = f"the {ordinals[i]}" + (f" ({char_name})" if i == 0 and char_name else "")
                    person_descs.append(f"{who} " + ", ".join(desc_bits))
            subject = head + trait_part
            if person_descs:
                subject += ", " + "; ".join(person_descs)
        else:  # group — detail the central person, vary the rest
            head = " ".join(x for x in (eng(ns_key), eng(ag_key), eng(et_key)) if x)
            if gm_key == "gg_mixed":
                head += " people, a mixed group of men and women"
            else:
                head += f" {eng(gd_key)}s"
            subject = (head + trait_part +
                       ", each person with a clearly distinct hairstyle, outfit variation and expression")
            if main_look:
                who = "the central person" + (f" ({char_name})" if char_name else "")
                subject += f", {who} {main_look}"
        if eng(skf_key):
            subject += f", {eng(skf_key)}"
        if locked:
            subject += (", the same recurring character with a consistent face and identity in every image"
                        if prompt_len() == "pl_detailed" else
                        ", the same recurring character with a consistent face")
        if eng(pet_key):
            subject += f", {eng(pet_key)}"

        # Outfit (top & bottom each with their own fabric + color).
        # Garments set to "None" are omitted so fashion presets don't clash.
        outfit_parts = []
        for fk in fs_selected_keys:
            v = eng(fk)
            if v:
                outfit_parts.append(v)
        for g_key, fb_key, cp_key in ((top_key, top_fb_key, top_cp_key),
                                      (bot_key, bot_fb_key, bot_cp_key),
                                      (dr_key, dr_fb_key, dr_cp_key)):
            garment = eng(g_key)
            if not garment:
                continue
            if eng(fb_key):
                garment += f" made of {eng(fb_key)}"
            if eng(cp_key):
                garment += f" in {eng(cp_key)}"
            outfit_parts.append(garment)
        if eng(os_key):
            outfit_parts.append(eng(os_key))
        if eng(out_key):
            outer = f"layered with {eng(out_key)}"
            if eng(out_cp_key):
                outer += f" in {eng(out_cp_key)}"
            outfit_parts.append(outer)
        if eng(fit_key):
            outfit_parts.append(f"with {eng(fit_key)}")
        det_vals = [eng(k) for k in det_selected_keys if eng(k)]
        if det_vals:
            det_text = (", ".join(det_vals[:-1]) + " and " + det_vals[-1]
                        if len(det_vals) > 1 else det_vals[0])
            outfit_parts.append(f"featuring {det_text}")
        if eng(leg_key):
            outfit_parts.append(f"with {eng(leg_key)}")
        if eng(sh_key):
            outfit_parts.append(eng(sh_key))
        if outfit_text.strip():
            outfit_parts.append(f"wearing {translate_to_english(outfit_text)}")
        if attach_outfit:
            outfit_parts.append("wearing the exact outfit shown in the attached outfit reference image (it may be displayed on a mannequin or as a flat lay), matching its design, layers, colors, fabrics and details")
        for ak in acc_selected:
            v = eng(ak)
            if v:
                outfit_parts.append(v)
        outfit = ", ".join(outfit_parts)

        # Pose — a pose reference image replaces the pickers; otherwise the
        # pose + its fine-tuning details, then gaze, mood and free text.
        # Every part may be "None".
        if attach_pose:
            pose_parts = ["posed exactly like the figure in the attached pose reference image, "
                          "matching its body position, limb placement and head angle, "
                          "but not its appearance, body shape or clothing"]
        else:
            pose_parts = [eng(po_key)] + [eng(pose_detail_keys[wk]) for wk in
                                          ("w_body_dir", "w_legs", "w_hands", "w_head")]
        pose_tail = [eng(gz_key), eng(pe_key)]
        if pose_text.strip():
            pose_tail.append(translate_to_english(pose_text))
        pose = ", ".join(p for p in pose_parts + pose_tail if p)

        # Environment
        if attach_scene:
            env_loc = "in the exact location shown in the attached scene reference image, matching its background and atmosphere"
        elif scene_custom_text.strip():
            env_loc = translate_to_english(scene_custom_text)
        elif place_landmark or place_city or place_country:
            place_parts = []
            if place_landmark.strip():
                place_parts.append(f"at {translate_to_english(place_landmark)}")
            if place_city.strip():
                place_parts.append(translate_to_english(place_city))
            if place_country.strip():
                place_parts.append(translate_to_english(place_country))
            env_loc = ", ".join(place_parts)
        else:
            env_loc = eng(lo_key)
        season_text = eng(sn_key)
        weather_text = ", ".join(eng(k) for k in atm_keys if eng(k))
        env_time = eng(td_key)
        env_parts = [p for p in (env_loc, env_time, season_text, weather_text, eng(bgp_key)) if p]
        environment = ", ".join(env_parts)

        # Camera & Lighting + Picture Style + Composition — all optional
        lfx_vals = [eng(k) for k in lfx_keys if eng(k)]
        lfx_text = ""
        if lfx_vals:
            lfx_text = "with " + (", ".join(lfx_vals[:-1]) + " and " + lfx_vals[-1]
                                  if len(lfx_vals) > 1 else lfx_vals[0])
        light_parts = [eng(k) for k in (lt_key, ld_key, lc_key, lq_key)]
        camera_parts = [p for p in light_parts + [eng(k) for k in (
            sf_key, ch_key, cd_key, cs_key, dof_key, cmp_key, ps_key)] + [lfx_text] if p]
        camera_section = ", ".join(camera_parts)

        # Custom
        custom_eng = translate_to_english(custom_text) if custom_text.strip() else ""

        # Negative
        negative_eng = translate_to_english(negative_text) if negative_text.strip() else ""

        # Ref images notes
        ref_notes = []
        if attach_subject:
            ref_notes.append(t("ref_note_subject"))
        if attach_outfit:
            ref_notes.append(t("ref_note_outfit"))
        if attach_pose:
            ref_notes.append(t("ref_note_pose"))
        if attach_scene:
            ref_notes.append(t("ref_note_scene"))

        # Aspect ratio formatted for the target platform
        ratio = AR_RATIOS[ar_selected_key]
        if pf_selected_key == "platform_midjourney":
            ar_val = f"--ar {ratio}"
            if int(mj_stylize) != 100:
                ar_val += f" --stylize {int(mj_stylize)}"
            if mj_seed.strip().isdigit():
                ar_val += f" --seed {mj_seed.strip()}"
        else:
            ar_val = f"in {ratio} aspect ratio"

        # ── Store each section in session_state (using widget keys) ──
        st.session_state["ta_technical"] = technical
        st.session_state["ta_subject"] = subject
        st.session_state["ta_outfit"] = outfit
        st.session_state["ta_pose"] = pose
        st.session_state["ta_environment"] = environment
        st.session_state["ta_camera"] = camera_section
        st.session_state["ta_custom"] = custom_eng
        st.session_state["ed_negative"] = negative_eng
        st.session_state["sec_ar"] = ar_val
        st.session_state["sec_platform"] = pf_selected_key
        st.session_state["ref_notes"] = ref_notes
        st.session_state["prompt_generated"] = True

        # ── Prompt history (last 10 generated prompts) ──
        history_parts = [technical, subject, outfit, pose, environment, camera_section]
        if custom_eng.strip():
            history_parts.append(custom_eng)
        history_parts.append(ar_val)
        history_entry = ", ".join(p.strip() for p in history_parts if p.strip())
        history = st.session_state.get("prompt_history", [])
        if not history or history[0] != history_entry:
            history.insert(0, history_entry)
        st.session_state["prompt_history"] = history[:10]

        # ── Photo Set: same subject/outfit/scene, varied pose + framing +
        # angle per shot, so the prompts generate one coherent album ──
        if st.session_state.pop("photo_set_request", False):
            # Stay inside the chosen pose category when it has enough poses
            # (e.g. a "Sitting" album); gaze + mood carry over to every shot,
            # pose-specific details and the pose reference do not.
            pose_pool = [k for k in pose_keys_for_category(pc_key)
                         if eng(k) and k not in PHOTO_SET_POSE_EXCLUDE]
            if len(pose_pool) < PHOTO_SET_SIZE:
                pose_pool = [k for k in PO_KEYS
                             if eng(k) and k not in PHOTO_SET_POSE_EXCLUDE]
            set_prompts = []
            for v_pose_key in random.sample(pose_pool, PHOTO_SET_SIZE):
                v_pose_parts = [p for p in [eng(v_pose_key), eng(gz_key), eng(pe_key)] if p]
                v_camera = ", ".join(p for p in light_parts + [
                    eng(random.choice(PHOTO_SET_SF_KEYS)),
                    eng(random.choice(PHOTO_SET_CH_KEYS)),
                    eng(random.choice(PHOTO_SET_CD_KEYS)),
                    eng(dof_key), eng(cmp_key), eng(ps_key), lfx_text] if p)
                parts = [technical, subject, outfit, ", ".join(v_pose_parts),
                         environment, v_camera]
                if custom_eng.strip():
                    parts.append(custom_eng)
                parts.append(ar_val)
                p_text = ", ".join(p.strip() for p in parts if p.strip())
                if pf_selected_key == "platform_midjourney" and negative_eng:
                    p_text += f" --no {negative_eng}"
                set_prompts.append(p_text)
            st.session_state["photo_set_prompts"] = set_prompts
        else:
            # A normal generate reflects new settings — drop the stale set
            st.session_state.pop("photo_set_prompts", None)

    # ── Display: Editable Sections ────────────────────────────────────────
    if st.session_state.get("prompt_generated"):
        st.caption(t("edit_hint"))

        # Section 1: Technical
        st.markdown(f"**🔧 {t('section_technical')}**")
        ed_tech = st.text_area("ta_tech_label", height=68,
                               key="ta_technical", label_visibility="collapsed")

        # Section 2 & 3: Subject + Outfit side by side
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown(f"**👤 {t('section_subject')}**")
            ed_subj = st.text_area("ta_subj_label", height=100,
                                   key="ta_subject", label_visibility="collapsed")
        with col_s2:
            st.markdown(f"**👗 {t('section_outfit')}**")
            ed_outfit = st.text_area("ta_outfit_label", height=100,
                                     key="ta_outfit", label_visibility="collapsed")

        # Section 4 & 5: Pose + Environment
        col_s3, col_s4 = st.columns(2)
        with col_s3:
            st.markdown(f"**🕺 {t('section_pose')}**")
            ed_pose = st.text_area("ta_pose_label", height=68,
                                   key="ta_pose", label_visibility="collapsed")
        with col_s4:
            st.markdown(f"**🌅 {t('section_environment')}**")
            ed_env = st.text_area("ta_env_label", height=68,
                                  key="ta_environment", label_visibility="collapsed")

        # Section 6: Camera & Lighting
        st.markdown(f"**📷 {t('section_camera')}**")
        ed_cam = st.text_area("ta_cam_label", height=68,
                              key="ta_camera", label_visibility="collapsed")

        # Section 7: Custom additions
        st.markdown(f"**✨ {t('section_custom')}**")
        ed_custom = st.text_area("ta_custom_label", height=68,
                                 key="ta_custom", label_visibility="collapsed")

        # ── Combine all sections into final prompt ──
        ar_val = st.session_state.get("sec_ar", "")
        platform_key = st.session_state.get("sec_platform", "platform_universal")
        ed_neg = st.session_state.get("ed_negative", "").strip()
        all_parts = [ed_tech, ed_subj, ed_outfit, ed_pose, ed_env, ed_cam]
        if ed_custom.strip():
            all_parts.append(ed_custom)
        if ar_val:
            all_parts.append(ar_val)
        combined_prompt = ", ".join(s.strip() for s in all_parts if s.strip())
        # Midjourney takes the negative prompt inline via --no
        if platform_key == "platform_midjourney" and ed_neg:
            combined_prompt += f" --no {ed_neg}"

        st.markdown("---")
        st.markdown(f"### 📋 {t('section_final')}")
        st.code(combined_prompt, language=None)
        st.caption(f"{len(combined_prompt)} {t('chars_label')} · {len(combined_prompt.split())} {t('words_label')}")

        # Copy button — use components.html so JS actually executes
        # Use json.dumps for proper JS string escaping (html.escape breaks apostrophes in <script>)
        safe_prompt = json.dumps(combined_prompt).replace("</", "<\\/")
        copy_label = t("copy_btn")
        copy_html = f"""
        <html><body style="margin:0;padding:0;background:transparent;">
        <button id="copy-btn" style="
            background:linear-gradient(135deg,#43e97b 0%,#38f9d7 100%);border:none;
            padding:12px 28px;border-radius:10px;font-size:1rem;font-weight:600;cursor:pointer;
            color:#1a1a2e;min-height:48px;font-family:'Noto Sans Thai','Segoe UI',sans-serif;
            transition:transform 0.15s,box-shadow 0.15s;"
            onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 4px 12px rgba(67,233,123,0.4)';"
            onmouseout="this.style.transform='none';this.style.boxShadow='none';"
            onclick="copyPrompt()">📋 {copy_label}</button>
        <script>
        function copyPrompt() {{
            const text = {safe_prompt};
            const btn = document.getElementById('copy-btn');
            if (navigator.clipboard && window.isSecureContext) {{
                navigator.clipboard.writeText(text).then(() => {{
                    btn.innerText = '✅ Copied!';
                    setTimeout(() => btn.innerText = '📋 {copy_label}', 2000);
                }}).catch(fallbackCopy);
            }} else {{
                fallbackCopy();
            }}
            function fallbackCopy() {{
                const ta = document.createElement('textarea');
                ta.value = text;
                ta.style.position = 'fixed';
                ta.style.left = '-9999px';
                document.body.appendChild(ta);
                ta.select();
                document.execCommand('copy');
                document.body.removeChild(ta);
                btn.innerText = '✅ Copied!';
                setTimeout(() => btn.innerText = '📋 {copy_label}', 2000);
            }}
        }}
        </script></body></html>
        """
        copy_col, dl_col = st.columns([1, 1])
        with copy_col:
            components.html(copy_html, height=60)
        with dl_col:
            dl_text = combined_prompt
            if ed_neg and platform_key != "platform_midjourney":
                dl_text += f"\n\nNegative prompt:\n{ed_neg}"
            st.download_button(f"💾 {t('download_btn')}", dl_text,
                               file_name="prompt.txt", mime="text/plain")

        # Negative prompt (already embedded via --no for Midjourney)
        if ed_neg and platform_key != "platform_midjourney":
            st.markdown("")
            st.markdown(f"**{t('section_negative')}:**")
            st.code(ed_neg, language=None)

        # Reference image notes
        ref_notes = st.session_state.get("ref_notes", [])
        if ref_notes:
            st.markdown("")
            st.markdown(f"### 📎 {t('ref_images_header')}")
            st.info(t("ref_instruction"))
            for note in ref_notes:
                st.markdown(f"- {note}")
    else:
        st.info(t("no_prompt_yet"))

    # ── Photo Set output ──────────────────────────────────────────────────
    set_prompts = st.session_state.get("photo_set_prompts", [])
    if set_prompts:
        st.markdown("---")
        st.markdown(f"### 📸 {t('photo_set_header')}")
        st.caption(t("photo_set_hint"))
        for i, p_text in enumerate(set_prompts, 1):
            st.markdown(f"**{t('photo_set_shot')} {i}/{len(set_prompts)}**")
            st.code(p_text, language=None)
        st.download_button(f"💾 {t('photo_set_download')}",
                           "\n\n".join(set_prompts),
                           file_name="photo_set.txt", mime="text/plain")

    # ── Prompt history ────────────────────────────────────────────────────
    history = st.session_state.get("prompt_history", [])
    if history:
        st.markdown("---")
        with st.expander(f"🕘 {t('history_header')}", expanded=False):
            for item in history:
                st.code(item, language=None)
            st.button(f"🗑️ {t('history_clear')}", on_click=clear_prompt_history)
            st.caption(t("saved_in_browser"))

    sync_browser_store()


if __name__ == "__main__":
    main()
