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

TRANSLATIONS = {
    "en": {
        # ── Global ──
        "app_title": "AI Image Prompt Generator",
        "app_subtitle": "Generate optimized prompts for Gemini · Imagen 3 · Midjourney",
        "aspect_ratio": "Aspect Ratio",
        "model_type": "Model Type",
        "generate_btn": "Generate Prompt",
        "copy_btn": "Copy to Clipboard",
        "result_header": "Generated Prompt",
        "no_prompt_yet": "Click **Generate Prompt** to see your result here.",
        "target_platform": "Target AI Platform",
        "platform_universal": "Universal (Gemini · Imagen)",
        "platform_midjourney": "Midjourney",
        "platform_sd": "Stable Diffusion / SDXL",
        "random_btn": "Random Look",
        "random_scene_btn": "Random Scene",
        "lens": "Lens (photo modes only)",
        "lens_24": "24mm (wide / environmental)",
        "lens_35": "35mm (classic)",
        "lens_50": "50mm (standard)",
        "lens_85": "85mm (portrait)",
        "lens_135": "135mm (telephoto)",
        "mj_stylize": "Stylize (--stylize)",
        "mj_seed": "Seed (--seed, optional)",
        "download_btn": "Download .txt",
        "history_header": "Prompt History (last 10)",
        "chars_label": "characters",
        "words_label": "words",

        # Aspect Ratio
        "ar_1_1": "1:1  (Square · Instagram)",
        "ar_16_9": "16:9 (Landscape · YouTube)",
        "ar_9_16": "9:16 (Portrait · TikTok/Reels)",
        "ar_4_5": "4:5  (Portrait · Instagram)",
        "ar_3_2": "3:2  (Landscape · Classic Photo)",
        "ar_2_3": "2:3  (Portrait · Classic Photo)",
        "ar_4_3": "4:3  (Landscape · Standard Photo)",
        "ar_3_4": "3:4  (Portrait · Standard Photo)",
        "ar_iphone": "iPhone Wallpaper",
        "ar_android": "Android Wallpaper",

        # Model Type
        "model_realistic": "Realistic Photography",
        "model_cinematic": "Cinematic Film Still",
        "model_film": "Analog Film Photo",
        "model_fashion": "Fashion Editorial",
        "model_anime": "Anime / Illustration",
        "model_digital_painting": "Digital Painting",
        "model_watercolor": "Watercolor Painting",
        "model_comic": "Comic / Manga",
        "model_3d": "3D Render / CGI",

        # ── Subject ──
        "exp_subject": "Subject",
        "attach_subject_photo": "I will attach my reference photo (face/person)",
        "attach_subject_note": "Prompt will instruct AI to match the attached face/identity",
        "gender": "Gender",
        "gender_female": "Female",
        "gender_male": "Male",
        "gender_nb": "Non-binary",
        "age_group": "Age Group",
        "age_5_9": "Child (5-9)",
        "age_10_14": "Preteen (10-14)",
        "age_15_19": "Teenager (15-19)",
        "age_20_25": "Young Adult (20-25)",
        "age_26_35": "Adult (26-35)",
        "age_36_45": "Mature (36-45)",
        "age_46_60": "Middle-aged (46-60)",
        "age_60plus": "Senior (60+)",
        "ethnicity": "Ethnicity",
        "eth_asian": "East-Asian",
        "eth_se_asian": "Southeast-Asian",
        "eth_south_asian": "South-Asian",
        "eth_european": "European / Caucasian",
        "eth_african": "African",
        "eth_latin": "Latin American",
        "eth_middle_east": "Middle-Eastern",
        "eth_mixed": "Mixed / Ambiguous",
        "skin_detail": "Ultra-realistic Skin Texture",
        "num_subjects": "Number of People",
        "ns_solo": "Solo (1 person)",
        "ns_duo": "Duo (2 people)",
        "ns_trio": "Trio (3 people)",
        "ns_group": "Group (5 people)",
        "person_2": "Person 2 — distinct look",
        "person_3": "Person 3 — distinct look",
        "multi_person_hint": "💡 Give each person a different hairstyle, hair color and expression below so the AI can tell them apart.",
        "group_hint": "💡 Group shots describe the central person in detail; the others are prompted to have naturally varied looks.",
        # Makeup styles (None first, then A-Z)
        "makeup": "Makeup Style",
        "mu_none": "— None —",
        "mu_red_lip": "Classic Red Lip",
        "mu_douyin": "Douyin / C-beauty",
        "mu_glam": "Full Glam",
        "mu_gradient": "Gradient Lips (Korean)",
        "mu_dewy": "Korean Dewy Glow",
        "mu_natural": "Natural / Light",
        "mu_no_makeup": "No-Makeup Look",
        "mu_smoky": "Smoky Eyes",
        "mu_soft_matte": "Soft Matte",
        "hair_style": "Hair Style",
        # Women's hairstyles
        "hair_long": "Long Flowing",
        "hair_straight": "Straight Long",
        "hair_loose_waves": "Loose Waves",
        "hair_curly": "Curly",
        "hair_wavy": "Wavy",
        "hair_layered": "Layered",
        "hair_wolf_cut": "Wolf Cut",
        "hair_hush_cut": "Hush Cut",
        "hair_hime": "Hime Cut",
        "hair_bob": "Bob Cut",
        "hair_lob": "Long Bob / Lob",
        "hair_pixie": "Pixie Cut",
        "hair_ponytail": "Ponytail",
        "hair_high_ponytail": "High Ponytail",
        "hair_bun": "Bun",
        "hair_messy_bun": "Messy Bun",
        "hair_space_buns": "Space Buns",
        "hair_braids": "Braids",
        "hair_french_braid": "French Braid",
        "hair_twin_braids": "Twin Braids",
        "hair_twintails": "Twin Tails",
        "hair_half_up": "Half Up Half Down",
        "hair_side_swept": "Side Swept",
        # Men's hairstyles
        "hair_short": "Short",
        "hair_buzz": "Buzz Cut",
        "hair_crew_cut": "Crew Cut",
        "hair_middle_part": "Middle Part (Comma)",
        "hair_textured_crop": "Textured Crop",
        "hair_undercut": "Undercut",
        "hair_fade": "Fade",
        "hair_slick_back": "Slicked Back",
        "hair_man_bun": "Man Bun",
        "hair_bald": "Bald / Shaved",
        "hair_color": "Hair Color",
        "hc_black": "Black",
        "hc_blue_black": "Blue Black",
        "hc_dark_brown": "Dark Brown",
        "hc_ash_brown": "Ash Brown",
        "hc_milk_tea": "Milk Tea Brown",
        "hc_light_brown": "Light Brown",
        "hc_honey_blonde": "Honey Blonde",
        "hc_blonde": "Blonde",
        "hc_platinum": "Platinum Blonde",
        "hc_red": "Red / Auburn",
        "hc_burgundy": "Burgundy / Cherry Red",
        "hc_rose_gold": "Rose Gold",
        "hc_pink": "Pink",
        "hc_purple": "Purple / Lavender",
        "hc_blue": "Blue",
        "hc_silver": "Silver / Gray",
        "hc_white": "White",
        "hc_ombre": "Ombre (dark to light)",
        "hc_highlights": "Highlights / Streaks",
        "bangs": "Bangs",
        "bangs_none": "None",
        "bangs_straight": "Straight Bangs",
        "bangs_see_through": "See-through Bangs",
        "bangs_side": "Side Bangs",
        "bangs_curtain": "Curtain Bangs",
        "bangs_wispy": "Wispy Bangs",
        "bangs_micro": "Micro Bangs",
        "bangs_hime": "Hime Sidelocks",
        "expression": "Facial Expression",
        "expr_smile": "Gentle Smile",
        "expr_bright_smile": "Bright Beaming Smile",
        "expr_laugh": "Laughing",
        "expr_giggle": "Giggling",
        "expr_soft_gaze": "Soft Gentle Gaze",
        "expr_doe_eyes": "Innocent Doe Eyes",
        "expr_pout": "Cute Pout",
        "expr_playful": "Playful",
        "expr_shy": "Shy / Bashful",
        "expr_confident": "Confident",
        "expr_smirk": "Smirk",
        "expr_dreamy": "Dreamy",
        "expr_peaceful": "Peaceful / Serene",
        "expr_neutral": "Neutral",
        "expr_pensive": "Pensive / Thoughtful",
        "expr_serious": "Serious / Stoic",
        "expr_surprised": "Surprised",
        "expr_sad": "Sad / Melancholic",
        "expr_sultry": "Sultry",

        # ── Body Type ──
        "body_type": "Body Type",
        "bt_slim": "Slim / Slender",
        "bt_petite": "Petite",
        "bt_lean": "Lean / Toned",
        "bt_athletic": "Athletic / Fit",
        "bt_hourglass": "Hourglass",
        "bt_curvy": "Curvy",
        "bt_tall": "Tall / Model-like",
        "bt_average": "Average",

        # ── Appearance / Vibe ── (A-Z)
        "appearance": "Appearance / Vibe",
        "app_beautiful": "Beautiful / Gorgeous",
        "app_cpop": "C-pop Star",
        "app_charming": "Charming / Lovely",
        "app_chic": "Chic / Classy",
        "app_cool": "Cool / Edgy",
        "app_cute": "Cute / Adorable",
        "app_doll": "Doll-like",
        "app_elegant": "Elegant / Sophisticated",
        "app_fierce": "Fierce / Bold",
        "app_girl_next_door": "Girl-next-door",
        "app_handsome": "Handsome / Charming",
        "app_jpop": "J-pop Idol",
        "app_kpop": "K-pop Idol",
        "app_natural": "Natural / Fresh-faced",
        "app_sweet": "Sweet / Innocent",
        "app_youthful": "Youthful / Glowing",

        # ── Section Labels (editable output) ──
        "section_technical": "Technical / Quality",
        "section_subject": "Subject / Character",
        "section_outfit": "Outfit & Style",
        "section_pose": "Pose",
        "section_environment": "Environment",
        "section_camera": "Camera & Lighting",
        "section_custom": "Custom Additions",
        "section_final": "Final Combined Prompt",
        "section_negative": "Negative Prompt",
        "edit_hint": "Edit any section below, then copy the combined prompt.",

        # ── Outfit ──
        "exp_outfit": "Outfit & Style",
        "outfit_input": "Describe Outfit (free text)",
        "outfit_placeholder": "e.g. Japanese school uniform with red ribbon",
        "fashion_presets": "Fashion Styles (optional, multi-select)",
        "fashion_presets_help": "Select styles to blend, or skip and describe your own below",
        "outfit_clash_hint": "💡 A fashion style is selected — leave Top/Bottom on “None” to let the style define the outfit, or clear the style to build your own.",
        # Fashion presets (A-Z)
        "fs_athleisure": "Athleisure / Sporty",
        "fs_barbiecore": "Barbiecore / All Pink",
        "fs_bohemian": "Bohemian / Boho",
        "fs_office": "Business Casual / Office",
        "fs_casual": "Casual / Everyday",
        "fs_clean_girl": "Clean Girl",
        "fs_coquette": "Coquette / Balletcore",
        "fs_cottagecore": "Cottagecore / Pastoral",
        "fs_cyberpunk": "Cyberpunk / Techwear",
        "fs_dark_academia": "Dark Academia",
        "fs_egirl": "E-girl / E-boy",
        "fs_elegant": "Elegant / Formal",
        "fs_gorpcore": "Gorpcore / Outdoor",
        "fs_gothic": "Gothic / Dark",
        "fs_grunge": "Grunge / 90s",
        "fs_japanese": "Japanese Harajuku",
        "fs_korean": "Korean Fashion (K-Style)",
        "fs_light_academia": "Light Academia",
        "fs_minimalist": "Minimalist / Clean",
        "fs_mob_wife": "Mob Wife / Fur Glam",
        "fs_old_money": "Old Money / Quiet Luxury",
        "fs_parisian": "Parisian Chic",
        "fs_preppy": "Preppy / Academic",
        "fs_resort": "Resort / Vacation",
        "fs_rockstar": "Rockstar / Band",
        "fs_skater": "Skater",
        "fs_streetwear": "Streetwear / Urban",
        "fs_thai": "Thai Traditional",
        "fs_vintage": "Vintage / Retro",
        "fs_western": "Western / Cowboy",
        "fs_y2k": "Y2K / 2000s Revival",
        # Top garments (A-Z)
        "top_garment": "Top",
        "top_none": "— None (let fashion style decide) —",
        "top_blazer": "Blazer",
        "top_blouse": "Blouse",
        "top_bodysuit": "Bodysuit",
        "top_bomber": "Bomber Jacket",
        "top_bralette": "Bralette",
        "top_button_shirt": "Button-up Shirt",
        "top_camisole": "Camisole",
        "top_cardigan": "Cardigan",
        "top_corset": "Corset Top",
        "top_crop": "Crop Top",
        "top_denim_jacket": "Denim Jacket",
        "top_halter": "Halter Top",
        "top_hoodie": "Hoodie",
        "top_knit_vest": "Knit Vest",
        "top_leather_jacket": "Leather Jacket",
        "top_long_sleeve": "Long-sleeve Tee",
        "top_off_shoulder": "Off-shoulder Top",
        "top_oversized_shirt": "Oversized Shirt",
        "top_polo": "Polo Shirt",
        "top_puff_sleeve": "Puff-sleeve Blouse",
        "top_puffer": "Puffer Jacket",
        "top_sports_bra": "Sports Bra",
        "top_sweater": "Sweater",
        "top_sweatshirt": "Sweatshirt",
        "top_tshirt": "T-Shirt",
        "top_tank": "Tank Top",
        "top_trench": "Trench Coat",
        "top_tube": "Tube Top",
        "top_turtleneck": "Turtleneck",
        "top_varsity": "Varsity Jacket",
        "top_wrap": "Wrap Top",
        # Bottom garments (A-Z)
        "bottom_garment": "Bottom",
        "bot_none": "— None (let fashion style decide) —",
        "bot_a_line": "A-line Skirt",
        "bot_baggy": "Baggy Jeans",
        "bot_bike_shorts": "Bike Shorts",
        "bot_cargo": "Cargo Pants",
        "bot_cargo_skirt": "Cargo Skirt",
        "bot_culottes": "Culottes",
        "bot_denim_shorts": "Denim Shorts",
        "bot_denim_skirt": "Denim Skirt",
        "bot_flare": "Flare Jeans",
        "bot_jeans": "Jeans",
        "bot_joggers": "Joggers",
        "bot_leggings": "Leggings",
        "bot_maxi_skirt": "Maxi Skirt",
        "bot_midi_skirt": "Midi Skirt",
        "bot_mini_skirt": "Mini Skirt",
        "bot_overalls": "Overalls",
        "bot_palazzo": "Palazzo Pants",
        "bot_parachute": "Parachute Pants",
        "bot_pencil_skirt": "Pencil Skirt",
        "bot_pleated_skirt": "Pleated Skirt",
        "bot_ripped": "Ripped Jeans",
        "bot_slip_skirt": "Satin Slip Skirt",
        "bot_shorts": "Shorts",
        "bot_skort": "Skort",
        "bot_sweatpants": "Sweatpants",
        "bot_trousers": "Tailored Trousers",
        "bot_tennis_skirt": "Tennis Skirt",
        "bot_tulle_skirt": "Tulle Skirt",
        "bot_wide_leg": "Wide-leg Pants",
        "bot_yoga": "Yoga Pants",
        # Footwear (None first, then A-Z)
        "footwear": "Footwear",
        "sh_none": "— None —",
        "sh_ankle_boots": "Ankle Boots",
        "sh_ballet": "Ballet Flats",
        "sh_barefoot": "Barefoot",
        "sh_chelsea": "Chelsea Boots",
        "sh_chunky": "Chunky Sneakers",
        "sh_combat": "Combat Boots",
        "sh_cowboy": "Cowboy Boots",
        "sh_espadrilles": "Espadrilles",
        "sh_flip_flops": "Flip-flops",
        "sh_heels": "High Heels",
        "sh_kitten_heels": "Kitten Heels",
        "sh_knee_boots": "Knee-high Boots",
        "sh_loafers": "Loafers",
        "sh_mary_janes": "Mary Janes",
        "sh_mules": "Mules",
        "sh_oxford": "Oxford Shoes",
        "sh_platform": "Platform Shoes",
        "sh_running": "Running Shoes",
        "sh_sandals": "Sandals",
        "sh_sneakers": "Sneakers",
        "attach_outfit_photo": "I will attach outfit reference photo",
        "attach_outfit_note": "Prompt will instruct AI to recreate the attached outfit",
        # Fabric (A-Z) — separate for top & bottom
        "top_fabric": "Top Fabric",
        "bot_fabric": "Bottom Fabric",
        "fab_none": "— Not specified —",
        "fab_chiffon": "Chiffon",
        "fab_cotton": "Cotton",
        "fab_denim": "Denim",
        "fab_lace": "Lace",
        "fab_leather": "Leather",
        "fab_linen": "Linen",
        "fab_satin": "Satin",
        "fab_sheer": "Sheer / Translucent",
        "fab_silk": "Silk",
        "fab_tweed": "Tweed",
        "fab_velvet": "Velvet",
        "fab_wool": "Wool Knit",
        # Color palette (A-Z) — separate for top & bottom
        "top_color": "Top Color",
        "bot_color": "Bottom Color",
        "col_none": "— Not specified —",
        "col_black": "All Black",
        "col_baby_blue": "Baby Blue",
        "col_beige": "Beige & Nude",
        "col_blue": "Blue",
        "col_brown": "Brown & Chocolate",
        "col_burgundy": "Burgundy & Wine",
        "col_colorblock": "Colorblock (bold mix)",
        "col_cool": "Cool Tones (blue, teal, silver)",
        "col_coral": "Coral",
        "col_earthy": "Earthy & Brown",
        "col_gold": "Gold Metallic",
        "col_green": "Green",
        "col_hot_pink": "Hot Pink",
        "col_khaki": "Khaki & Olive",
        "col_lilac": "Lilac",
        "col_mint": "Mint Green",
        "col_mono": "Monochrome",
        "col_navy": "Navy",
        "col_orange": "Orange",
        "col_pastel": "Pastel",
        "col_peach": "Peach",
        "col_pink": "Pink",
        "col_purple": "Purple & Lavender",
        "col_red": "Red",
        "col_sage": "Sage Green",
        "col_silver": "Silver Metallic",
        "col_teal": "Teal",
        "col_vibrant": "Vibrant & Neon",
        "col_warm": "Warm Tones (red, orange, gold)",
        "col_white": "White & Cream",
        "col_yellow": "Yellow & Gold",

        # ── Accessories (checkboxes) ──
        "accessories": "Accessories (select all that apply)",
        "acc_group_head": "Head Accessories",
        "acc_group_body": "Body / Jewelry",
        "acc_group_carried": "Carried Items",
        "acc_beanie": "Beanie",
        "acc_beret": "Beret",
        "acc_bucket_hat": "Bucket Hat",
        "acc_cap": "Cap",
        "acc_glasses": "Prescription Glasses",
        "acc_hair_clip": "Hair Clip",
        "acc_ribbon": "Hair Ribbon Bow",
        "acc_hat": "Hat",
        "acc_headband": "Headband",
        "acc_scrunchie": "Scrunchie",
        "acc_sunglasses": "Sunglasses",
        "acc_tiara": "Tiara / Crown",
        "acc_anklet": "Anklet",
        "acc_belt": "Belt",
        "acc_bowtie": "Bow Tie",
        "acc_bracelet": "Bracelet",
        "acc_choker": "Choker",
        "acc_earrings": "Earrings",
        "acc_necklace": "Necklace",
        "acc_necktie": "Necktie",
        "acc_ring": "Ring",
        "acc_scarf": "Scarf",
        "acc_watch": "Watch",
        "acc_backpack": "Backpack",
        "acc_book": "Book",
        "acc_camera": "Film Camera",
        "acc_clutch": "Clutch Bag",
        "acc_crossbody": "Crossbody Bag",
        "acc_bouquet": "Flower Bouquet",
        "acc_bag": "Handbag",
        "acc_coffee": "Iced Coffee Cup",
        "acc_phone": "Smartphone",
        "acc_tote": "Tote Bag",
        "acc_umbrella": "Umbrella",

        # ── Scene ──
        "exp_scene": "Scene & Lighting",
        "scene_mode": "Location Input",
        "scene_mode_preset": "Choose from List",
        "scene_mode_custom": "Describe / Type",
        "scene_mode_place": "Real Place / Travel",
        "scene_custom_input": "Describe your location",
        "scene_custom_placeholder": "e.g. Tokyo street at night with neon signs and wet pavement",
        "attach_scene_photo": "I will attach scene/background reference photo",
        "attach_scene_note": "Prompt will instruct AI to use the attached background",
        "place_landmark": "Landmark / Tourist Attraction",
        "place_landmark_placeholder": "e.g. Eiffel Tower, Grand Palace, Shibuya Crossing",
        "place_city": "City",
        "place_city_placeholder": "e.g. Paris, Bangkok, Tokyo",
        "place_country": "Country",
        "place_country_placeholder": "e.g. France, Thailand, Japan",
        "location": "Location",
        "loc_studio": "Photography Studio",
        "loc_airport": "Airport Terminal",
        "loc_amusement": "Amusement Park",
        "loc_aquarium": "Aquarium",
        "loc_art_gallery": "Art Gallery / Museum",
        "loc_beach": "Beach / Seaside",
        "loc_bridge": "Bridge / River View",
        "loc_castle": "Castle / Palace",
        "loc_cafe": "Coffee Shop / Café",
        "loc_desert": "Desert Dunes",
        "loc_old_town": "European Old Town",
        "loc_flower_field": "Flower Field",
        "loc_forest": "Forest / Nature",
        "loc_garden": "Garden / Park",
        "loc_stairs": "Grand Staircase",
        "loc_gym": "Gym / Fitness Studio",
        "loc_room": "Indoor Room / Bedroom",
        "loc_lake": "Lakeside Pier",
        "loc_library": "Library / Bookstore",
        "loc_hotel_lobby": "Luxury Hotel Lobby",
        "loc_mountain": "Mountain Viewpoint",
        "loc_neon_alley": "Neon Alley (Cyberpunk)",
        "loc_night_market": "Night Market",
        "loc_pool": "Poolside",
        "loc_rice_field": "Rice Field / Countryside",
        "loc_rooftop": "Rooftop / Cityscape",
        "loc_shopping": "Shopping Street",
        "loc_snow": "Snowy Landscape / Ski",
        "loc_subway": "Subway Station",
        "loc_temple": "Temple / Historic",
        "loc_train": "Train Station",
        "loc_university": "University Campus",
        "loc_street": "Urban Street",
        "loc_waterfall": "Waterfall",
        "time_of_day": "Time of Day",
        "tod_golden": "Golden Hour (Sunset)",
        "tod_blue": "Blue Hour (Twilight)",
        "tod_noon": "High Noon",
        "tod_night": "Nighttime",
        "tod_overcast": "Overcast / Cloudy",
        "tod_sunrise": "Sunrise",
        "season": "Season",
        "season_none": "Not specified",
        "season_spring": "Spring",
        "season_summer": "Summer",
        "season_autumn": "Autumn / Fall",
        "season_winter": "Winter",
        "season_rainy": "Rainy Season",
        "weather_effect": "Weather Effect",
        "weather_rain": "Rain falling",
        "weather_snow": "Snow falling",
        "weather_leaves": "Red/autumn leaves falling",
        "lighting": "Lighting Style",
        "lit_natural": "Natural / Ambient",
        "lit_window": "Soft Window Light",
        "lit_studio": "Studio Softbox",
        "lit_rim": "Rim / Backlit",
        "lit_neon": "Neon / Cyberpunk",
        "lit_fairy": "Fairy / String Lights",
        "lit_candle": "Candlelight / Warm",
        "lit_dramatic": "Dramatic Chiaroscuro",
        "lit_flash": "Direct Flash (Trendy)",
        "lit_backlit": "Golden Backlight / Halo",
        "lit_dappled": "Dappled Light (through leaves)",
        "lit_blinds": "Window Blinds Shadows",
        "lit_gel": "Color Gel (red/blue duotone)",
        "lit_spotlight": "Stage Spotlight",
        "lit_moonlight": "Moonlight",
        "lit_bonfire": "Campfire Glow",
        "lit_godrays": "Volumetric God Rays",

        # ── Picture Style ──
        "picture_style": "Picture Style / Filter",
        "ps_none": "None (Default)",
        "ps_dreamy": "Dreamy / Ethereal",
        "ps_soft": "Soft / Gentle",
        "ps_vivid": "Vivid / Saturated",
        "ps_bw": "Black & White",
        "ps_vintage": "Vintage / Retro Film",
        "ps_cinematic": "Cinematic Color Grade",
        "ps_moody": "Moody / Dark Tone",
        "ps_pastel": "Pastel / Light Airy",
        "ps_hdr": "HDR / High Contrast",
        "ps_matte": "Matte Film Look",
        "ps_commercial": "Clean Commercial",
        "ps_editorial": "Editorial Magazine",
        "ps_documentary": "Documentary / Street",
        "ps_polaroid": "Polaroid Instant",
        "ps_digicam": "Y2K Digicam Flash",
        "ps_fantasy": "Ethereal Fantasy",
        "ps_fairytale": "Dark Fairytale",
        "ps_cyber": "Cyberpunk Neon",
        "ps_vaporwave": "Vaporwave / Retrowave",
        "ps_surreal": "Dreamcore Surreal",

        # ── Shot Framing (NEW) ──
        "shot_framing": "Shot Framing",
        "sf_extreme_cu": "Extreme Close-up (face only)",
        "sf_closeup": "Close-up (head & shoulders)",
        "sf_medium_cu": "Medium Close-up (chest up)",
        "sf_medium": "Medium Shot (waist up)",
        "sf_cowboy": "Cowboy Shot (mid-thigh up)",
        "sf_medium_full": "Medium Full (knees up)",
        "sf_full": "Full Body",
        "sf_wide": "Wide Shot (full body + environment)",

        # ── Camera Angle ──
        "camera_angle": "Camera Angle",
        "cam_eye": "Eye Level",
        "cam_low": "Low Angle (heroic)",
        "cam_high": "High Angle (overhead)",
        "cam_3q": "3/4 View",
        "cam_profile": "Side Profile",
        "cam_selfie": "Selfie Angle",
        "cam_dutch": "Dutch Angle (tilted)",
        "cam_over_shoulder": "Over the Shoulder",
        "cam_bird": "Bird's Eye View",
        "cam_worm": "Worm's Eye (extreme low)",
        "cam_ground": "Ground Level",
        "cam_pov": "POV (first person)",
        "cam_back": "From Behind",

        # ── Depth of Field (NEW) ──
        "dof": "Depth of Field / Background",
        "dof_sharp": "Everything Sharp (deep focus)",
        "dof_portrait": "Portrait Bokeh (f/1.8, subject sharp, background blurred)",
        "dof_shallow": "Shallow DOF (f/1.2, heavy bokeh, dreamy)",
        "dof_tiltshift": "Tilt-shift (miniature effect)",
        "dof_soft": "Soft / Dreamy Glow",
        "dof_bokeh_lights": "Bokeh Light Orbs (night)",
        "dof_motion": "Motion Blur Background",
        "dof_fg_blur": "Blurred Foreground Framing",
        "dof_clean_bg": "Clean Studio Background",

        # ── Composition ──
        "composition": "Composition",
        "comp_center": "Center (Default)",
        "comp_rot_left": "Rule of Thirds — Left",
        "comp_rot_right": "Rule of Thirds — Right",
        "comp_golden": "Golden Ratio",
        "comp_leading": "Leading Lines",
        "comp_framed": "Framed / Doorway",
        "comp_negative_space": "Negative Space",
        "comp_symmetry": "Symmetrical",
        "comp_diagonal": "Diagonal Lines",
        "comp_fill": "Fill the Frame",
        "comp_reflection": "Reflection / Mirror",
        "comp_depth": "Layered Depth (FG/MG/BG)",

        # ── Pose ── (sorted A-Z)
        "pose": "Action / Pose",
        "pose_fix_jacket": "Adjusting Jacket / Collar",
        "pose_adjust_glasses": "Adjusting Sunglasses",
        "pose_arms_up": "Arms Above Head",
        "pose_cross_arms": "Arms Crossed",
        "pose_arms_open": "Arms Open Wide",
        "pose_back_camera": "Back to Camera",
        "pose_blow_kiss": "Blowing a Kiss",
        "pose_candid": "Candid / Natural Motion",
        "pose_chin_up": "Chin Up (Confident)",
        "pose_cross_leg": "Cross-legged Sitting",
        "pose_crouch": "Crouching",
        "pose_dance": "Dancing",
        "pose_dynamic": "Dynamic / Action Pose",
        "pose_editorial": "Editorial Model Pose",
        "pose_elegant": "Elegant Graceful Pose",
        "pose_finger_heart": "Finger Heart (Korean)",
        "pose_hair_flip": "Hair Flip",
        "pose_hand_hair": "Hand in Hair",
        "pose_hand_chin": "Hand on Chin",
        "pose_hand_hip": "Hand on Hip",
        "pose_hands_back": "Hands Behind Back",
        "pose_arms_behind_head": "Hands Behind Head",
        "pose_cheek_hands": "Hands Framing Face",
        "pose_hands_pocket": "Hands in Pockets",
        "pose_head_tilt": "Head Tilt (Cute)",
        "pose_heart_hands": "Heart Hands",
        "pose_high_fashion": "High-Fashion Stance",
        "pose_hug_knees": "Hugging Knees",
        "pose_jump": "Jumping",
        "pose_kneel": "Kneeling",
        "pose_lean": "Leaning Against Wall",
        "pose_railing": "Leaning on Railing",
        "pose_lean_forward": "Leaning Toward Camera",
        "pose_looking_away": "Looking Away",
        "pose_look_back_walk": "Looking Back While Walking",
        "pose_over_shoulder": "Looking Over Shoulder",
        "pose_look_up": "Looking Up (Dreamy)",
        "pose_lying": "Lying Down",
        "pose_mini_heart": "Mini Heart",
        "pose_mirror_selfie": "Mirror Selfie",
        "pose_peace": "Peace Sign",
        "pose_peek_fingers": "Peeking Through Fingers",
        "pose_reach_camera": "Reaching Toward Camera",
        "pose_run": "Running",
        "pose_runway": "Runway Walk",
        "pose_s_curve": "S-Curve Standing",
        "pose_shield_sun": "Shielding Eyes from Sun",
        "pose_sit": "Sitting",
        "pose_sit_stairs": "Sitting on Stairs",
        "pose_legs_extended": "Sitting, Legs Extended",
        "pose_stand": "Standing",
        "pose_squat": "Streetwear Squat",
        "pose_stretch": "Stretching Gracefully",
        "pose_hold_hat": "Touching Hat Brim",
        "pose_hair_tuck": "Tucking Hair Behind Ear",
        "pose_twirl": "Twirling",
        "pose_w_sit": "W-Sitting",
        "pose_walk": "Walking",
        "pose_walk_away": "Walking Away (Candid)",
        "pose_wink": "Winking",
        "look_camera": "Looking at camera",

        # ── Advanced ──
        "exp_advanced": "Advanced & Technical",
        "save_load_header": "Save / Load Look",
        "save_look": "Save Look (JSON)",
        "load_look": "Apply Look",
        "load_look_paste": "Load a saved look — paste its JSON here",
        "preset_loaded": "Look applied!",
        "preset_invalid": "Could not read that look — paste the exact JSON saved from “Save Look”.",
        "custom_prompt": "Custom additions (free text)",
        "custom_placeholder": "e.g. cinematic color grading, lens flare, film grain",
        "negative_prompt": "Negative Prompt (things to avoid)",
        "negative_placeholder": "e.g. blurry, low quality, extra fingers, watermark",
        "quality_tags": "Quality Boost Tags",
        "qt_8k": "8K Ultra HD",
        "qt_detail": "Highly Detailed",
        "qt_sharp": "Sharp Focus",
        "qt_pro": "Professional Photography",
        "qt_award": "Award-winning",
        "qt_magazine": "Magazine Quality",

        # ── Reference reminders in output ──
        "ref_images_header": "Reference Images to Attach",
        "ref_instruction": "When sending the prompt, attach the reference images you selected above alongside the text in your AI tool.",
        "ref_note_subject": "Attach: Your face/person reference photo",
        "ref_note_outfit": "Attach: Outfit/clothing reference photo",
        "ref_note_scene": "Attach: Scene/background reference photo",
    },
    "th": {
        # ── Global ──
        "app_title": "เครื่องสร้างพรอมต์ภาพ AI",
        "app_subtitle": "สร้างพรอมต์สำหรับ Gemini · Imagen 3 · Midjourney",
        "aspect_ratio": "อัตราส่วนภาพ",
        "model_type": "ประเภทโมเดล",
        "generate_btn": "สร้างพรอมต์",
        "copy_btn": "คัดลอก",
        "result_header": "พรอมต์ที่สร้างแล้ว",
        "no_prompt_yet": "กด **สร้างพรอมต์** เพื่อดูผลลัพธ์",
        "target_platform": "แพลตฟอร์ม AI เป้าหมาย",
        "platform_universal": "ทั่วไป (Gemini · Imagen)",
        "platform_midjourney": "Midjourney",
        "platform_sd": "Stable Diffusion / SDXL",
        "random_btn": "สุ่มลุค",
        "random_scene_btn": "สุ่มฉาก",
        "lens": "เลนส์ (เฉพาะโหมดภาพถ่าย)",
        "lens_24": "24มม. (มุมกว้าง / เห็นสภาพแวดล้อม)",
        "lens_35": "35มม. (คลาสสิก)",
        "lens_50": "50มม. (มาตรฐาน)",
        "lens_85": "85มม. (พอร์ตเทรต)",
        "lens_135": "135มม. (เทเลโฟโต้)",
        "mj_stylize": "Stylize (--stylize)",
        "mj_seed": "Seed (--seed ใส่หรือไม่ก็ได้)",
        "download_btn": "ดาวน์โหลด .txt",
        "history_header": "ประวัติพรอมต์ (10 ล่าสุด)",
        "chars_label": "ตัวอักษร",
        "words_label": "คำ",

        # Aspect Ratio
        "ar_1_1": "1:1  (สี่เหลี่ยม · Instagram)",
        "ar_16_9": "16:9 (แนวนอน · YouTube)",
        "ar_9_16": "9:16 (แนวตั้ง · TikTok/Reels)",
        "ar_4_5": "4:5  (แนวตั้ง · Instagram)",
        "ar_3_2": "3:2  (แนวนอน · ภาพถ่ายคลาสสิก)",
        "ar_2_3": "2:3  (แนวตั้ง · ภาพถ่ายคลาสสิก)",
        "ar_4_3": "4:3  (แนวนอน · ภาพถ่ายมาตรฐาน)",
        "ar_3_4": "3:4  (แนวตั้ง · ภาพถ่ายมาตรฐาน)",
        "ar_iphone": "วอลเปเปอร์ iPhone",
        "ar_android": "วอลเปเปอร์ Android",

        # Model Type
        "model_realistic": "ภาพถ่ายสมจริง",
        "model_cinematic": "ภาพนิ่งสไตล์ภาพยนตร์",
        "model_film": "ภาพถ่ายฟิล์มอนาล็อก",
        "model_fashion": "แฟชั่นเอดิทอเรียล",
        "model_anime": "อนิเมะ / ภาพวาด",
        "model_digital_painting": "ดิจิทัลเพนต์ติ้ง",
        "model_watercolor": "ภาพวาดสีน้ำ",
        "model_comic": "การ์ตูน / มังงะ",
        "model_3d": "3D เรนเดอร์ / CGI",

        # ── Subject ──
        "exp_subject": "ตัวละคร",
        "attach_subject_photo": "จะแนบรูปอ้างอิงตัวเอง (ใบหน้า/ตัวตน)",
        "attach_subject_note": "พรอมต์จะสั่งให้ AI อิงจากรูปใบหน้า/ตัวตนที่แนบมา",
        "gender": "เพศ",
        "gender_female": "หญิง",
        "gender_male": "ชาย",
        "gender_nb": "ไม่ระบุเพศ",
        "age_group": "กลุ่มอายุ",
        "age_5_9": "เด็ก (5-9)",
        "age_10_14": "เด็กโต (10-14)",
        "age_15_19": "วัยรุ่น (15-19)",
        "age_20_25": "วัยหนุ่มสาว (20-25)",
        "age_26_35": "ผู้ใหญ่ (26-35)",
        "age_36_45": "วัยกลางคน (36-45)",
        "age_46_60": "วัยกลางคนปลาย (46-60)",
        "age_60plus": "ผู้อาวุโส (60+)",
        "ethnicity": "เชื้อชาติ",
        "eth_asian": "เอเชียตะวันออก",
        "eth_se_asian": "เอเชียตะวันออกเฉียงใต้",
        "eth_south_asian": "เอเชียใต้",
        "eth_european": "ยุโรป / คอเคเชียน",
        "eth_african": "แอฟริกัน",
        "eth_latin": "ลาตินอเมริกัน",
        "eth_middle_east": "ตะวันออกกลาง",
        "eth_mixed": "เชื้อชาติผสม",
        "skin_detail": "ผิวหนังสมจริงสุดๆ (รูขุมขน, กระ)",
        "num_subjects": "จำนวนคน",
        "ns_solo": "เดี่ยว (1 คน)",
        "ns_duo": "คู่ (2 คน)",
        "ns_trio": "3 คน",
        "ns_group": "กลุ่ม (5 คน)",
        "person_2": "คนที่ 2 — ลุคเฉพาะตัว",
        "person_3": "คนที่ 3 — ลุคเฉพาะตัว",
        "multi_person_hint": "💡 เลือกทรงผม สีผม และสีหน้าให้แต่ละคนต่างกันด้านล่าง เพื่อให้ AI แยกแต่ละคนออกจากกันได้",
        "group_hint": "💡 พรอมต์แบบกลุ่มจะบรรยายคนตรงกลางอย่างละเอียด ส่วนคนอื่นๆ จะถูกสั่งให้มีลุคหลากหลายตามธรรมชาติ",
        # Makeup styles (None first, then A-Z)
        "makeup": "สไตล์เมคอัพ",
        "mu_none": "— ไม่ระบุ —",
        "mu_red_lip": "ลิปแดงคลาสสิก",
        "mu_douyin": "โต่วอิน / C-beauty",
        "mu_glam": "ฟูลแกลม",
        "mu_gradient": "ปากไล่สี (เกาหลี)",
        "mu_dewy": "ผิวโกลว์ฉ่ำแบบเกาหลี",
        "mu_natural": "ธรรมชาติ / บางเบา",
        "mu_no_makeup": "ลุคหน้าสด",
        "mu_smoky": "ตาสโมคกี้",
        "mu_soft_matte": "แมตต์เนื้อนุ่ม",
        "hair_style": "ทรงผม",
        # ทรงผมผู้หญิง
        "hair_long": "ยาวสลวย",
        "hair_straight": "ยาวตรง",
        "hair_loose_waves": "ลอนหลวม",
        "hair_curly": "หยิก",
        "hair_wavy": "หยักศก",
        "hair_layered": "ซอยเลเยอร์",
        "hair_wolf_cut": "วูล์ฟคัท",
        "hair_hush_cut": "ฮัชคัท",
        "hair_hime": "ฮิเมะคัท",
        "hair_bob": "บ็อบ",
        "hair_lob": "ลองบ็อบ",
        "hair_pixie": "พิกซี่",
        "hair_ponytail": "หางม้า",
        "hair_high_ponytail": "หางม้าสูง",
        "hair_bun": "มวยผม",
        "hair_messy_bun": "มวยผมหลวม",
        "hair_space_buns": "มวยผมสองข้าง",
        "hair_braids": "ถักเปีย",
        "hair_french_braid": "เปียเฟรนช์",
        "hair_twin_braids": "ถักเปียสองข้าง",
        "hair_twintails": "มัดสองข้าง",
        "hair_half_up": "มัดครึ่ง",
        "hair_side_swept": "ปัดข้าง",
        # ทรงผมผู้ชาย
        "hair_short": "สั้น",
        "hair_buzz": "บัซคัท / เกรียน",
        "hair_crew_cut": "ทรงนักเรียน",
        "hair_middle_part": "แสกกลาง (คอมม่าแฮร์)",
        "hair_textured_crop": "ครอปเท็กซ์เจอร์",
        "hair_undercut": "อันเดอร์คัท",
        "hair_fade": "เฟด",
        "hair_slick_back": "เสยไปด้านหลัง",
        "hair_man_bun": "มัดจุก",
        "hair_bald": "โล้น / โกนผม",
        "hair_color": "สีผม",
        "hc_black": "ดำ",
        "hc_blue_black": "ดำอมน้ำเงิน",
        "hc_dark_brown": "น้ำตาลเข้ม",
        "hc_ash_brown": "น้ำตาลหม่น (แอชบราวน์)",
        "hc_milk_tea": "น้ำตาลชานม",
        "hc_light_brown": "น้ำตาลอ่อน",
        "hc_honey_blonde": "บลอนด์น้ำผึ้ง",
        "hc_blonde": "บลอนด์",
        "hc_platinum": "บลอนด์แพลตินั่ม",
        "hc_red": "แดง / ออเบิร์น",
        "hc_burgundy": "แดงเบอร์กันดี / เชอร์รี่",
        "hc_rose_gold": "โรสโกลด์",
        "hc_pink": "ชมพู",
        "hc_purple": "ม่วง / ลาเวนเดอร์",
        "hc_blue": "น้ำเงิน",
        "hc_silver": "เงิน / เทา",
        "hc_white": "ขาว",
        "hc_ombre": "ออมเบร (เข้มไล่อ่อน)",
        "hc_highlights": "ไฮไลท์ / ทำเส้น",
        "bangs": "หน้าม้า",
        "bangs_none": "ไม่มี",
        "bangs_straight": "หน้าม้าตรง",
        "bangs_see_through": "หน้าม้าซีทรู",
        "bangs_side": "หน้าม้าปัดข้าง",
        "bangs_curtain": "หน้าม้าม่าน",
        "bangs_wispy": "หน้าม้าบาง",
        "bangs_micro": "หน้าม้าสั้น",
        "bangs_hime": "หน้าม้าฮิเมะ (ไซด์ล็อค)",
        "expression": "สีหน้า / อารมณ์",
        "expr_smile": "ยิ้มอ่อน",
        "expr_bright_smile": "ยิ้มสดใสเปล่งประกาย",
        "expr_laugh": "หัวเราะ",
        "expr_giggle": "ยิ้มคิกคัก",
        "expr_soft_gaze": "สายตาอ่อนโยน",
        "expr_doe_eyes": "ตากลมใสไร้เดียงสา",
        "expr_pout": "ทำปากยื่นน่ารัก",
        "expr_playful": "ขี้เล่น / ซุกซน",
        "expr_shy": "เขินอาย",
        "expr_confident": "มั่นใจ",
        "expr_smirk": "ยิ้มมุมปาก",
        "expr_dreamy": "เหม่อฝัน",
        "expr_peaceful": "สงบ / เยือกเย็น",
        "expr_neutral": "เฉยๆ / ปกติ",
        "expr_pensive": "ครุ่นคิด",
        "expr_serious": "จริงจัง / เข้มขรึม",
        "expr_surprised": "ตกใจ / ประหลาดใจ",
        "expr_sad": "เศร้า",
        "expr_sultry": "เย้ายวน",

        # ── Body Type ──
        "body_type": "รูปร่าง",
        "bt_slim": "ผอมเพรียว",
        "bt_petite": "ตัวเล็กกะทัดรัด",
        "bt_lean": "ผอมกระชับ / เฟิร์ม",
        "bt_athletic": "กล้ามเนื้อ / ฟิต",
        "bt_hourglass": "หุ่นนาฬิกาทราย",
        "bt_curvy": "หุ่นโค้งเว้า",
        "bt_tall": "สูง / หุ่นนางแบบ",
        "bt_average": "ปกติทั่วไป",

        # ── Appearance / Vibe ── (A-Z ตามภาษาอังกฤษ)
        "appearance": "ลุค / ไวบ์ภาพรวม",
        "app_beautiful": "สวยงาม / สวยหรู",
        "app_cpop": "ดาราจีน / C-pop",
        "app_charming": "มีเสน่ห์ / น่าหลงใหล",
        "app_chic": "ชิค / คลาสซี่",
        "app_cool": "เท่ / คูล",
        "app_cute": "น่ารัก / คิ้วท์",
        "app_doll": "หน้าตุ๊กตา",
        "app_elegant": "สง่างาม / ดูแพง",
        "app_fierce": "ดุดัน / เข้มขรึม",
        "app_girl_next_door": "สาวข้างบ้าน / เฟรนด์ลี่",
        "app_handsome": "หล่อ / มีเสน่ห์",
        "app_jpop": "ไอดอล J-pop",
        "app_kpop": "ไอดอล K-pop",
        "app_natural": "ธรรมชาติ / สดใส",
        "app_sweet": "หวาน / ใสซื่อ",
        "app_youthful": "อ่อนเยาว์ / ผิวโกลว์",

        # ── Section Labels (editable output) ──
        "section_technical": "เทคนิค / คุณภาพ",
        "section_subject": "ตัวละคร / บุคคล",
        "section_outfit": "เสื้อผ้า & สไตล์",
        "section_pose": "ท่าโพส",
        "section_environment": "สภาพแวดล้อม",
        "section_camera": "กล้อง & แสง",
        "section_custom": "เพิ่มเติม",
        "section_final": "พรอมต์รวมทั้งหมด",
        "section_negative": "สิ่งที่ไม่ต้องการ",
        "edit_hint": "แก้ไขแต่ละส่วนได้ตามต้องการ แล้วคัดลอกพรอมต์รวมด้านล่าง",

        # ── Outfit ──
        "exp_outfit": "เสื้อผ้าและสไตล์",
        "outfit_input": "อธิบายชุด (พิมพ์เอง)",
        "outfit_placeholder": "เช่น ชุดนักเรียนญี่ปุ่นผูกโบว์สีแดง",
        "fashion_presets": "สไตล์แฟชั่น (เลือกได้หลายอัน)",
        "fashion_presets_help": "เลือกสไตล์ผสมกันได้ หรือข้ามไปอธิบายเองด้านล่าง",
        "outfit_clash_hint": "💡 เลือกสไตล์แฟชั่นแล้ว — แนะนำให้ปล่อยเสื้อ/ท่อนล่างเป็น “ไม่ระบุ” เพื่อให้สไตล์กำหนดชุดเอง หรือล้างสไตล์ออกแล้วจัดชุดเองก็ได้",
        # Fashion presets (A-Z)
        "fs_athleisure": "แอธเลเชอร์ / สปอร์ต",
        "fs_barbiecore": "บาร์บี้คอร์ / ชมพูทั้งลุค",
        "fs_bohemian": "โบฮีเมียน / โบโฮ",
        "fs_office": "ออฟฟิศ / ทางการกึ่งลำลอง",
        "fs_casual": "แคชชวล / ลุคทุกวัน",
        "fs_clean_girl": "คลีนเกิร์ล",
        "fs_coquette": "โคเค็ตต์ / บัลเล่ต์คอร์",
        "fs_cottagecore": "คอตเทจคอร์ / ชนบท",
        "fs_cyberpunk": "ไซเบอร์พังก์ / เทคแวร์",
        "fs_dark_academia": "ดาร์กอะคาเดเมีย",
        "fs_egirl": "อีเกิร์ล / อีบอย",
        "fs_elegant": "เอเลแกนท์ / ทางการ",
        "fs_gorpcore": "กอร์ปคอร์ / สายเอาท์ดอร์",
        "fs_gothic": "โกธิค / ดาร์ค",
        "fs_grunge": "กรันจ์ / ยุค 90",
        "fs_japanese": "ฮาราจูกุ ญี่ปุ่น",
        "fs_korean": "แฟชั่นเกาหลี (K-Style)",
        "fs_light_academia": "ไลท์อะคาเดเมีย",
        "fs_minimalist": "มินิมอล / สะอาดตา",
        "fs_mob_wife": "ม็อบไวฟ์ / เฟอร์หรู",
        "fs_old_money": "Old Money / หรูเงียบๆ",
        "fs_parisian": "ปารีเซียงชิค",
        "fs_preppy": "เพรปปี้ / นักเรียนอินเตอร์",
        "fs_resort": "รีสอร์ต / วันหยุดพักร้อน",
        "fs_rockstar": "ร็อคสตาร์ / สายวงดนตรี",
        "fs_skater": "สเก็ตเตอร์",
        "fs_streetwear": "สตรีทแวร์ / อเบอร์แบน",
        "fs_thai": "ชุดไทยประยุกต์",
        "fs_vintage": "วินเทจ / เรโทร",
        "fs_western": "เวสเทิร์น / คาวบอย",
        "fs_y2k": "Y2K / ยุค 2000",
        # Top garments (A-Z)
        "top_garment": "เสื้อ",
        "top_none": "— ไม่ระบุ (ให้สไตล์แฟชั่นกำหนด) —",
        "top_blazer": "เสื้อเบลเซอร์",
        "top_blouse": "เสื้อเบลาส์",
        "top_bodysuit": "บอดี้สูท",
        "top_bomber": "แจ็คเก็ตบอมเบอร์",
        "top_bralette": "บราเล็ต",
        "top_button_shirt": "เสื้อเชิ้ต",
        "top_camisole": "เสื้อสายเดี่ยว",
        "top_cardigan": "เสื้อคาร์ดิแกน",
        "top_corset": "เสื้อคอร์เซ็ต",
        "top_crop": "ครอปท็อป",
        "top_denim_jacket": "แจ็คเก็ตยีนส์",
        "top_halter": "เสื้อคล้องคอ",
        "top_hoodie": "เสื้อฮู้ด",
        "top_knit_vest": "เสื้อกั๊กไหมพรม",
        "top_leather_jacket": "แจ็คเก็ตหนัง",
        "top_long_sleeve": "เสื้อยืดแขนยาว",
        "top_off_shoulder": "เสื้อเปิดไหล่",
        "top_oversized_shirt": "เชิ้ตโอเวอร์ไซซ์",
        "top_polo": "เสื้อโปโล",
        "top_puff_sleeve": "เสื้อแขนพอง",
        "top_puffer": "แจ็คเก็ตพัฟเฟอร์",
        "top_sports_bra": "สปอร์ตบรา",
        "top_sweater": "เสื้อสเวตเตอร์",
        "top_sweatshirt": "เสื้อสเวตเชิ้ต",
        "top_tshirt": "เสื้อยืด",
        "top_tank": "เสื้อกล้าม",
        "top_trench": "เทรนช์โค้ท",
        "top_tube": "เสื้อเกาะอก",
        "top_turtleneck": "เสื้อคอเต่า",
        "top_varsity": "แจ็คเก็ตวาร์ซิตี้",
        "top_wrap": "เสื้อแบบผูก (Wrap)",
        # Bottom garments (A-Z)
        "bottom_garment": "ท่อนล่าง",
        "bot_none": "— ไม่ระบุ (ให้สไตล์แฟชั่นกำหนด) —",
        "bot_a_line": "กระโปรงทรงเอ",
        "bot_baggy": "ยีนส์ทรงหลวม (แบ็กกี้)",
        "bot_bike_shorts": "กางเกงไบค์เกอร์",
        "bot_cargo": "กางเกงคาร์โก้",
        "bot_cargo_skirt": "กระโปรงคาร์โก้",
        "bot_culottes": "กางเกงคูล็อต",
        "bot_denim_shorts": "กางเกงยีนส์ขาสั้น",
        "bot_denim_skirt": "กระโปรงยีนส์",
        "bot_flare": "ยีนส์ขาม้า",
        "bot_jeans": "กางเกงยีนส์",
        "bot_joggers": "กางเกงจ็อกเกอร์",
        "bot_leggings": "เลกกิ้ง",
        "bot_maxi_skirt": "กระโปรงยาว",
        "bot_midi_skirt": "กระโปรงมิดิ",
        "bot_mini_skirt": "กระโปรงสั้น",
        "bot_overalls": "ชุดเอี๊ยม",
        "bot_palazzo": "กางเกงพาลาซโซ",
        "bot_parachute": "กางเกงพาราชูท",
        "bot_pencil_skirt": "กระโปรงทรงดินสอ",
        "bot_pleated_skirt": "กระโปรงพลีท",
        "bot_ripped": "ยีนส์ขาด",
        "bot_slip_skirt": "กระโปรงซาตินสลิป",
        "bot_shorts": "กางเกงขาสั้น",
        "bot_skort": "กระโปรงกางเกง (สเกิร์ต)",
        "bot_sweatpants": "กางเกงวอร์ม",
        "bot_trousers": "กางเกงสแล็ค",
        "bot_tennis_skirt": "กระโปรงเทนนิส",
        "bot_tulle_skirt": "กระโปรงผ้าทูล (โปร่ง)",
        "bot_wide_leg": "กางเกงขาบาน",
        "bot_yoga": "กางเกงโยคะ",
        # Footwear (None first, then A-Z)
        "footwear": "รองเท้า",
        "sh_none": "— ไม่ระบุ —",
        "sh_ankle_boots": "บูทหุ้มข้อ",
        "sh_ballet": "บัลเล่ต์แฟลต",
        "sh_barefoot": "เท้าเปล่า",
        "sh_chelsea": "บูทเชลซี",
        "sh_chunky": "สนีกเกอร์ทรงหนา",
        "sh_combat": "บูทคอมแบท",
        "sh_cowboy": "บูทคาวบอย",
        "sh_espadrilles": "เอสพาดริล",
        "sh_flip_flops": "รองเท้าแตะหูหนีบ",
        "sh_heels": "ส้นสูง",
        "sh_kitten_heels": "ส้นเตี้ยคิตเทนฮีล",
        "sh_knee_boots": "บูทยาวถึงเข่า",
        "sh_loafers": "โลฟเฟอร์",
        "sh_mary_janes": "แมรี่เจน",
        "sh_mules": "รองเท้ามิวล์",
        "sh_oxford": "รองเท้าอ็อกซ์ฟอร์ด",
        "sh_platform": "ส้นตึก",
        "sh_running": "รองเท้าวิ่ง",
        "sh_sandals": "รองเท้ารัดส้น",
        "sh_sneakers": "รองเท้าผ้าใบ",
        "attach_outfit_photo": "จะแนบรูปชุดอ้างอิง",
        "attach_outfit_note": "พรอมต์จะสั่งให้ AI สร้างชุดตามรูปที่แนบ",
        # Fabric (A-Z) — separate for top & bottom
        "top_fabric": "ผ้าเสื้อ",
        "bot_fabric": "ผ้าท่อนล่าง",
        "fab_none": "— ไม่ระบุ —",
        "fab_chiffon": "ผ้าชีฟอง",
        "fab_cotton": "ผ้าฝ้าย",
        "fab_denim": "ผ้ายีนส์",
        "fab_lace": "ลูกไม้",
        "fab_leather": "หนัง",
        "fab_linen": "ผ้าลินิน",
        "fab_satin": "ผ้าซาติน",
        "fab_sheer": "ผ้าบาง / โปร่ง",
        "fab_silk": "ผ้าไหม",
        "fab_tweed": "ผ้าทวีด",
        "fab_velvet": "ผ้ากำมะหยี่",
        "fab_wool": "ผ้าขนสัตว์ถัก",
        # Color palette (A-Z) — separate for top & bottom
        "top_color": "สีเสื้อ",
        "bot_color": "สีท่อนล่าง",
        "col_none": "— ไม่ระบุ —",
        "col_black": "ดำล้วน",
        "col_baby_blue": "ฟ้าอ่อน",
        "col_beige": "เบจและนู้ด",
        "col_blue": "น้ำเงิน",
        "col_brown": "น้ำตาลช็อกโกแลต",
        "col_burgundy": "เบอร์กันดีและแดงไวน์",
        "col_colorblock": "คัลเลอร์บล็อก (สีตัดกัน)",
        "col_cool": "โทนเย็น (น้ำเงิน, เขียวอมฟ้า, เงิน)",
        "col_coral": "ส้มปะการัง",
        "col_earthy": "โทนดินและน้ำตาล",
        "col_gold": "ทองเมทัลลิก",
        "col_green": "เขียว",
        "col_hot_pink": "ชมพูช็อกกิ้งพิงก์",
        "col_khaki": "กากีและเขียวมะกอก",
        "col_lilac": "ม่วงไลแลค",
        "col_mint": "เขียวมิ้นต์",
        "col_mono": "โมโนโครม",
        "col_navy": "กรมท่า",
        "col_orange": "ส้ม",
        "col_pastel": "พาสเทล",
        "col_peach": "พีช",
        "col_pink": "ชมพู",
        "col_purple": "ม่วงและลาเวนเดอร์",
        "col_red": "แดง",
        "col_sage": "เขียวเสจ",
        "col_silver": "เงินเมทัลลิก",
        "col_teal": "เขียวนกเป็ดน้ำ (Teal)",
        "col_vibrant": "สดใสและนีออน",
        "col_warm": "โทนอุ่น (แดง, ส้ม, ทอง)",
        "col_white": "ขาวและครีม",
        "col_yellow": "เหลืองและทอง",

        # ── Accessories ──
        "accessories": "เครื่องประดับ (เลือกได้หลายอย่าง)",
        "acc_group_head": "เครื่องประดับศีรษะ",
        "acc_group_body": "เครื่องประดับร่างกาย / เครื่องเพชร",
        "acc_group_carried": "ของที่ถือ",
        "acc_beanie": "หมวกบีนนี่",
        "acc_beret": "หมวกเบเร่ต์",
        "acc_bucket_hat": "หมวกบักเก็ต",
        "acc_cap": "แก๊ป",
        "acc_glasses": "แว่นสายตา",
        "acc_hair_clip": "กิ๊บติดผม",
        "acc_ribbon": "โบว์ผูกผม",
        "acc_hat": "หมวก",
        "acc_headband": "ที่คาดผม",
        "acc_scrunchie": "ยางมัดผมสครันชี่",
        "acc_sunglasses": "แว่นกันแดด",
        "acc_tiara": "มงกุฎ / เทียร่า",
        "acc_anklet": "กำไลข้อเท้า",
        "acc_belt": "เข็มขัด",
        "acc_bowtie": "โบว์ไท",
        "acc_bracelet": "สร้อยข้อมือ",
        "acc_choker": "โชคเกอร์",
        "acc_earrings": "ต่างหู",
        "acc_necklace": "สร้อยคอ",
        "acc_necktie": "เนคไท",
        "acc_ring": "แหวน",
        "acc_scarf": "ผ้าพันคอ",
        "acc_watch": "นาฬิกา",
        "acc_backpack": "เป้สะพายหลัง",
        "acc_book": "หนังสือ",
        "acc_camera": "กล้องฟิล์ม",
        "acc_clutch": "กระเป๋าคลัตช์",
        "acc_crossbody": "กระเป๋าสะพายข้าง",
        "acc_bouquet": "ช่อดอกไม้",
        "acc_bag": "กระเป๋าถือ",
        "acc_coffee": "แก้วกาแฟเย็น",
        "acc_phone": "สมาร์ทโฟน",
        "acc_tote": "กระเป๋าโท้ต",
        "acc_umbrella": "ร่ม",

        # ── Scene ──
        "exp_scene": "ฉากและแสง",
        "scene_mode": "ระบุสถานที่",
        "scene_mode_preset": "เลือกจากรายการ",
        "scene_mode_custom": "พิมพ์อธิบายเอง",
        "scene_mode_place": "สถานที่จริง / ท่องเที่ยว",
        "scene_custom_input": "อธิบายสถานที่ / ฉากหลัง",
        "scene_custom_placeholder": "เช่น ถนนในโตเกียวตอนกลางคืน มีป้ายนีออนและพื้นเปียกฝน",
        "attach_scene_photo": "จะแนบรูปฉาก/แบ็คกราวด์อ้างอิง",
        "attach_scene_note": "พรอมต์จะสั่งให้ AI ใช้ฉากหลังตามรูปที่แนบ",
        "place_landmark": "สถานที่ท่องเที่ยว / แลนด์มาร์ค",
        "place_landmark_placeholder": "เช่น หอไอเฟล, วัดพระแก้ว, แยกชิบูย่า",
        "place_city": "เมือง",
        "place_city_placeholder": "เช่น ปารีส, กรุงเทพ, โตเกียว",
        "place_country": "ประเทศ",
        "place_country_placeholder": "เช่น ฝรั่งเศส, ไทย, ญี่ปุ่น",
        "location": "สถานที่",
        "loc_studio": "สตูดิโอถ่ายภาพ",
        "loc_airport": "สนามบิน / เทอร์มินอล",
        "loc_amusement": "สวนสนุก",
        "loc_aquarium": "อควาเรียม / พิพิธภัณฑ์สัตว์น้ำ",
        "loc_art_gallery": "หอศิลป์ / พิพิธภัณฑ์",
        "loc_beach": "ชายหาด / ทะเล",
        "loc_bridge": "สะพาน / วิวแม่น้ำ",
        "loc_castle": "ปราสาท / พระราชวัง",
        "loc_cafe": "ร้านกาแฟ / คาเฟ่",
        "loc_desert": "ทะเลทราย",
        "loc_old_town": "ย่านเมืองเก่ายุโรป",
        "loc_flower_field": "ทุ่งดอกไม้",
        "loc_forest": "ป่า / ธรรมชาติ",
        "loc_garden": "สวน / สวนสาธารณะ",
        "loc_stairs": "บันไดหรูหรา",
        "loc_gym": "ยิม / ฟิตเนส",
        "loc_room": "ห้อง / ห้องนอน",
        "loc_lake": "ท่าเรือริมทะเลสาบ",
        "loc_library": "ห้องสมุด / ร้านหนังสือ",
        "loc_hotel_lobby": "ล็อบบี้โรงแรมหรู",
        "loc_mountain": "จุดชมวิวภูเขา",
        "loc_neon_alley": "ตรอกไฟนีออน (ไซเบอร์พังก์)",
        "loc_night_market": "ตลาดกลางคืน",
        "loc_pool": "ริมสระว่ายน้ำ",
        "loc_rice_field": "ทุ่งนา / ชนบท",
        "loc_rooftop": "ดาดฟ้า / วิวเมือง",
        "loc_shopping": "ถนนช้อปปิ้ง",
        "loc_snow": "ภูมิทัศน์หิมะ / ลานสกี",
        "loc_subway": "สถานีรถไฟฟ้าใต้ดิน",
        "loc_temple": "วัด / สถานที่ประวัติศาสตร์",
        "loc_train": "สถานีรถไฟ",
        "loc_university": "มหาวิทยาลัย / แคมปัส",
        "loc_street": "ถนนในเมือง",
        "loc_waterfall": "น้ำตก",
        "time_of_day": "ช่วงเวลา",
        "tod_golden": "ชั่วโมงทอง (พระอาทิตย์ตก)",
        "tod_blue": "ชั่วโมงฟ้า (สนธยา)",
        "tod_noon": "เที่ยงวัน",
        "tod_night": "กลางคืน",
        "tod_overcast": "มีเมฆ / ครึ้มฟ้า",
        "tod_sunrise": "พระอาทิตย์ขึ้น",
        "season": "ฤดูกาล",
        "season_none": "ไม่ระบุ",
        "season_spring": "ฤดูใบไม้ผลิ",
        "season_summer": "ฤดูร้อน",
        "season_autumn": "ฤดูใบไม้ร่วง",
        "season_winter": "ฤดูหนาว",
        "season_rainy": "ฤดูฝน",
        "weather_effect": "เอฟเฟกต์สภาพอากาศ",
        "weather_rain": "ฝนกำลังตก",
        "weather_snow": "หิมะกำลังตก",
        "weather_leaves": "ใบไม้แดง/ใบไม้ร่วงกำลังร่วง",
        "lighting": "สไตล์แสง",
        "lit_natural": "แสงธรรมชาติ",
        "lit_window": "แสงหน้าต่างนุ่มนวล",
        "lit_studio": "ซอฟต์บ็อกซ์สตูดิโอ",
        "lit_rim": "แสงขอบ / แบ็คไลท์",
        "lit_neon": "นีออน / ไซเบอร์พังก์",
        "lit_fairy": "ไฟแฟรี่ / ไฟราว",
        "lit_candle": "แสงเทียน / อบอุ่น",
        "lit_dramatic": "ดราม่า เคียโรสกูโร",
        "lit_flash": "แฟลชตรง (สไตล์เทรนดี้)",
        "lit_backlit": "ย้อนแสงทอง / ฮาโล",
        "lit_dappled": "แสงลอดใบไม้",
        "lit_blinds": "เงามู่ลี่พาดผ่าน",
        "lit_gel": "ไฟเจลสี (แดง/น้ำเงิน)",
        "lit_spotlight": "สปอตไลท์เวที",
        "lit_moonlight": "แสงจันทร์",
        "lit_bonfire": "แสงกองไฟ",
        "lit_godrays": "ลำแสงทะลุเมฆ (God Rays)",

        # ── Picture Style ──
        "picture_style": "สไตล์ภาพ / ฟิลเตอร์",
        "ps_none": "ไม่ระบุ (ค่าเริ่มต้น)",
        "ps_dreamy": "ฝันหวาน / อีเธอเรียล",
        "ps_soft": "นุ่มนวล / อ่อนโยน",
        "ps_vivid": "สดใส / อิ่มสี",
        "ps_bw": "ขาวดำ",
        "ps_vintage": "วินเทจ / ฟิล์มย้อนยุค",
        "ps_cinematic": "ซีนีมาติก / โทนภาพยนตร์",
        "ps_moody": "มู้ดดี้ / โทนมืด",
        "ps_pastel": "พาสเทล / โปร่งเบา",
        "ps_hdr": "HDR / คอนทราสต์สูง",
        "ps_matte": "แมตต์ / ฟิล์มลุค",
        "ps_commercial": "คอมเมอร์เชียลสว่างสะอาด",
        "ps_editorial": "เอดิทอเรียลนิตยสาร",
        "ps_documentary": "สารคดี / สตรีท",
        "ps_polaroid": "โพลารอยด์",
        "ps_digicam": "กล้องดิจิตอล Y2K (แฟลชแรง)",
        "ps_fantasy": "แฟนตาซีเรืองแสง",
        "ps_fairytale": "เทพนิยายด้านมืด",
        "ps_cyber": "ไซเบอร์พังก์นีออน",
        "ps_vaporwave": "เวเปอร์เวฟ / เรโทรเวฟ",
        "ps_surreal": "ดรีมคอร์เหนือจริง",

        # ── Shot Framing ──
        "shot_framing": "ระยะภาพ / เฟรมมิ่ง",
        "sf_extreme_cu": "โคลสอัพมาก (ใบหน้าอย่างเดียว)",
        "sf_closeup": "โคลสอัพ (ศีรษะและไหล่)",
        "sf_medium_cu": "มีเดียมโคลสอัพ (หน้าอกขึ้นไป)",
        "sf_medium": "ภาพครึ่งตัว (เอวขึ้นไป)",
        "sf_cowboy": "คาวบอยช็อต (ต้นขาขึ้นไป)",
        "sf_medium_full": "ภาพเกือบเต็มตัว (เข่าขึ้นไป)",
        "sf_full": "ภาพเต็มตัว",
        "sf_wide": "ภาพกว้าง (เต็มตัว + สิ่งแวดล้อม)",

        # ── Camera Angle ──
        "camera_angle": "มุมกล้อง",
        "cam_eye": "ระดับสายตา",
        "cam_low": "มุมต่ำ (ดูยิ่งใหญ่)",
        "cam_high": "มุมสูง (มองลง)",
        "cam_3q": "มุม 3/4",
        "cam_profile": "มุมด้านข้าง (โปรไฟล์)",
        "cam_selfie": "มุมเซลฟี่",
        "cam_dutch": "มุมเอียง (Dutch Angle)",
        "cam_over_shoulder": "มองข้ามไหล่",
        "cam_bird": "มุมมองจากบน (Bird's Eye)",
        "cam_worm": "มุมหนอน (ต่ำมาก แหงนขึ้น)",
        "cam_ground": "ระดับพื้น",
        "cam_pov": "มุมมองบุคคลที่หนึ่ง (POV)",
        "cam_back": "ถ่ายจากด้านหลัง",

        # ── Depth of Field ──
        "dof": "ความชัดลึก / พื้นหลัง",
        "dof_sharp": "ชัดทั้งภาพ (Deep Focus)",
        "dof_portrait": "หน้าชัดหลังเบลอ (Portrait f/1.8)",
        "dof_shallow": "เบลอหนักมาก (f/1.2, โบเก้ฝัน)",
        "dof_tiltshift": "Tilt-shift (เหมือนโมเดลจิ๋ว)",
        "dof_soft": "นุ่มนวล / เรืองแสง (Dreamy)",
        "dof_bokeh_lights": "โบเก้ดวงไฟกลม (กลางคืน)",
        "dof_motion": "พื้นหลังเบลอเคลื่อนไหว",
        "dof_fg_blur": "ฉากหน้าเบลอ (ถ่ายลอดวัตถุ)",
        "dof_clean_bg": "พื้นหลังเรียบสตูดิโอ",

        # ── Composition ──
        "composition": "การจัดองค์ประกอบ",
        "comp_center": "ตรงกลาง (ค่าเริ่มต้น)",
        "comp_rot_left": "กฎสามส่วน — ซ้าย",
        "comp_rot_right": "กฎสามส่วน — ขวา",
        "comp_golden": "สัดส่วนทอง (Golden Ratio)",
        "comp_leading": "เส้นนำสายตา",
        "comp_framed": "กรอบภาพธรรมชาติ / ประตู",
        "comp_negative_space": "เว้นพื้นที่ว่าง (Negative Space)",
        "comp_symmetry": "สมมาตร (Symmetrical)",
        "comp_diagonal": "เส้นทแยงมุม",
        "comp_fill": "ซับเจกต์เต็มเฟรม",
        "comp_reflection": "เงาสะท้อน / กระจก",
        "comp_depth": "มิติหลายชั้น (หน้า-กลาง-หลัง)",

        # ── Pose ── (sorted A-Z)
        "pose": "ท่าโพส / แอคชั่น",
        "pose_fix_jacket": "จัดปกเสื้อ / แจ็คเก็ต",
        "pose_adjust_glasses": "จัดแว่นกันแดด",
        "pose_arms_up": "ยกแขนเหนือศีรษะ",
        "pose_cross_arms": "กอดอก",
        "pose_arms_open": "กางแขนกว้าง",
        "pose_back_camera": "หันหลังให้กล้อง",
        "pose_blow_kiss": "ส่งจูบ",
        "pose_candid": "แคนดิด / ท่าธรรมชาติ",
        "pose_chin_up": "เชิดคางมั่นใจ",
        "pose_cross_leg": "นั่งไขว่ห้าง",
        "pose_crouch": "นั่งยอง",
        "pose_dance": "เต้นรำ",
        "pose_dynamic": "ท่าไดนามิก / แอคชั่น",
        "pose_editorial": "ท่าแบบนิตยสารแฟชั่น",
        "pose_elegant": "ท่าสง่างาม",
        "pose_finger_heart": "ฟิงเกอร์ฮาร์ท (เกาหลี)",
        "pose_hair_flip": "สะบัดผม",
        "pose_hand_hair": "มือจับผม",
        "pose_hand_chin": "มือจับคาง",
        "pose_hand_hip": "มือเท้าเอวข้างเดียว",
        "pose_hands_back": "มือไขว้หลัง",
        "pose_arms_behind_head": "มือประสานหลังศีรษะ",
        "pose_cheek_hands": "มือเท้าแก้ม",
        "pose_hands_pocket": "มือในกระเป๋า",
        "pose_head_tilt": "เอียงหัวน่ารัก",
        "pose_heart_hands": "ทำมือรูปหัวใจ",
        "pose_high_fashion": "ท่านางแบบไฮแฟชั่น",
        "pose_hug_knees": "นั่งกอดเข่า",
        "pose_jump": "กระโดด",
        "pose_kneel": "คุกเข่า",
        "pose_lean": "พิงกำแพง",
        "pose_railing": "พิงราวระเบียง",
        "pose_lean_forward": "โน้มตัวเข้าหากล้อง",
        "pose_looking_away": "มองไปทางอื่น",
        "pose_look_back_walk": "เดินแล้วหันกลับมามอง",
        "pose_over_shoulder": "เหลียวมองข้ามไหล่",
        "pose_look_up": "แหงนมองขึ้น (ชวนฝัน)",
        "pose_lying": "นอน",
        "pose_mini_heart": "มินิฮาร์ท",
        "pose_mirror_selfie": "เซลฟี่หน้ากระจก",
        "pose_peace": "ชูสองนิ้ว",
        "pose_peek_fingers": "แอบมองผ่านนิ้ว",
        "pose_reach_camera": "ยื่นมือเข้าหากล้อง (Follow Me)",
        "pose_run": "วิ่ง",
        "pose_runway": "เดินแบบรันเวย์",
        "pose_s_curve": "ยืนโพสตัว S",
        "pose_shield_sun": "ยกมือบังแดด",
        "pose_sit": "นั่ง",
        "pose_sit_stairs": "นั่งบนบันได",
        "pose_legs_extended": "นั่งเหยียดขา",
        "pose_stand": "ยืน",
        "pose_squat": "นั่งยองสไตล์สตรีท",
        "pose_stretch": "ท่ายืดตัวสวยงาม",
        "pose_hold_hat": "จับปีกหมวก",
        "pose_hair_tuck": "เกี่ยวผมหลังหู",
        "pose_twirl": "หมุนตัว",
        "pose_w_sit": "นั่งขารูป W",
        "pose_walk": "เดิน",
        "pose_walk_away": "เดินหันหลัง (แคนดิด)",
        "pose_wink": "วิ้งก์ตา",
        "look_camera": "หันมองกล้อง",

        # ── Advanced ──
        "exp_advanced": "ขั้นสูงและเทคนิค",
        "save_load_header": "บันทึก / โหลดลุค",
        "save_look": "บันทึกลุค (JSON)",
        "load_look": "ใช้ลุคนี้",
        "load_look_paste": "โหลดลุคที่บันทึกไว้ — วางโค้ด JSON ที่นี่",
        "preset_loaded": "ใช้ลุคเรียบร้อยแล้ว!",
        "preset_invalid": "อ่านลุคไม่ได้ — กรุณาวาง JSON ที่ได้จากปุ่ม “บันทึกลุค”",
        "custom_prompt": "เพิ่มเติมเอง (พิมพ์ได้เลย)",
        "custom_placeholder": "เช่น โทนภาพยนตร์, เลนส์แฟลร์, ฟิล์มเกรน",
        "negative_prompt": "สิ่งที่ไม่ต้องการ (Negative Prompt)",
        "negative_placeholder": "เช่น เบลอ, คุณภาพต่ำ, นิ้วเกิน, ลายน้ำ",
        "quality_tags": "แท็กเพิ่มคุณภาพ",
        "qt_8k": "8K อัลตร้า HD",
        "qt_detail": "รายละเอียดสูงมาก",
        "qt_sharp": "โฟกัสคมชัด",
        "qt_pro": "ภาพถ่ายมืออาชีพ",
        "qt_award": "ระดับรางวัล",
        "qt_magazine": "คุณภาพนิตยสาร",

        # ── Ref notes ──
        "ref_images_header": "รูปอ้างอิงที่ต้องแนบ",
        "ref_instruction": "ตอนส่งพรอมต์ ให้แนบรูปอ้างอิงที่เลือกไว้พร้อมกับข้อความใน AI ที่ใช้",
        "ref_note_subject": "แนบ: รูปอ้างอิงใบหน้า/ตัวตน",
        "ref_note_outfit": "แนบ: รูปอ้างอิงชุด/เสื้อผ้า",
        "ref_note_scene": "แนบ: รูปอ้างอิงฉาก/แบ็คกราวด์",
    },
}

# ═══════════════════════════════════════════════════════════════════════════
#  2. ENGLISH-VALUE LOOKUP
# ═══════════════════════════════════════════════════════════════════════════

ENGLISH_VALUES = {
    # Gender
    "gender_female": "Female", "gender_male": "Male", "gender_nb": "Non-binary person",
    # Age
    "age_5_9": "child (5-9 years old)", "age_10_14": "preteen (10-14 years old)",
    "age_15_19": "teenager (15-19 years old)", "age_20_25": "young adult (20-25 years old)",
    "age_26_35": "adult (26-35 years old)", "age_36_45": "mature adult (36-45 years old)",
    "age_46_60": "middle-aged adult (46-60 years old)", "age_60plus": "senior (60+ years old)",
    # Ethnicity
    "eth_asian": "East-Asian", "eth_se_asian": "Southeast-Asian",
    "eth_south_asian": "South-Asian", "eth_european": "European Caucasian",
    "eth_african": "African", "eth_latin": "Latin American",
    "eth_middle_east": "Middle-Eastern", "eth_mixed": "mixed-race",
    # Hair Style — Women's
    "hair_long": "long flowing hair", "hair_straight": "long straight hair",
    "hair_loose_waves": "long loose wavy hair", "hair_curly": "curly hair",
    "hair_wavy": "wavy hair",
    "hair_layered": "layered haircut with soft face-framing layers",
    "hair_wolf_cut": "trendy wolf cut with shaggy layers",
    "hair_hush_cut": "Korean hush cut with soft airy layers",
    "hair_hime": "Japanese hime cut with straight sidelocks",
    "hair_bob": "bob cut",
    "hair_lob": "long bob lob hairstyle", "hair_pixie": "pixie cut",
    "hair_ponytail": "ponytail", "hair_high_ponytail": "high ponytail",
    "hair_bun": "hair bun", "hair_messy_bun": "messy bun",
    "hair_space_buns": "cute space buns",
    "hair_braids": "braids", "hair_french_braid": "french braid",
    "hair_twin_braids": "twin braids", "hair_twintails": "twin tails",
    "hair_half_up": "half up half down hairstyle", "hair_side_swept": "side swept hair",
    # Hair Style — Men's
    "hair_short": "short hair", "hair_buzz": "buzz cut",
    "hair_crew_cut": "crew cut",
    "hair_middle_part": "Korean middle-part comma hair",
    "hair_textured_crop": "textured crop haircut with messy fringe",
    "hair_undercut": "undercut hairstyle",
    "hair_fade": "fade haircut", "hair_slick_back": "slicked back hair",
    "hair_man_bun": "man bun", "hair_bald": "bald head",
    # Hair Color
    "hc_black": "black hair", "hc_blue_black": "blue-black hair",
    "hc_dark_brown": "dark brown hair", "hc_ash_brown": "ash brown hair",
    "hc_milk_tea": "milk tea brown hair", "hc_light_brown": "light brown hair",
    "hc_honey_blonde": "honey blonde hair", "hc_blonde": "blonde hair",
    "hc_platinum": "platinum blonde hair", "hc_red": "red auburn hair",
    "hc_burgundy": "burgundy cherry red hair", "hc_rose_gold": "rose gold hair",
    "hc_pink": "pink hair", "hc_purple": "purple lavender hair",
    "hc_blue": "blue hair", "hc_silver": "silver gray hair",
    "hc_white": "white hair",
    "hc_ombre": "ombre hair transitioning dark to light",
    "hc_highlights": "hair with highlights and streaks",
    # Bangs
    "bangs_none": "", "bangs_straight": "with straight bangs",
    "bangs_see_through": "with Korean see-through bangs",
    "bangs_side": "with side-swept bangs", "bangs_curtain": "with curtain bangs",
    "bangs_wispy": "with wispy bangs", "bangs_micro": "with micro bangs",
    "bangs_hime": "with hime-cut sidelocks framing the face",
    # Expression
    "expr_smile": "gentle smile",
    "expr_bright_smile": "bright beaming smile with sparkling eyes",
    "expr_laugh": "laughing joyfully",
    "expr_giggle": "giggling cutely with hand near mouth",
    "expr_soft_gaze": "soft gentle gaze with warm eyes",
    "expr_doe_eyes": "wide innocent doe eyes",
    "expr_pout": "cute playful pout",
    "expr_confident": "confident expression", "expr_serious": "serious stoic expression",
    "expr_smirk": "confident charming smirk",
    "expr_neutral": "neutral expression", "expr_pensive": "pensive thoughtful expression",
    "expr_shy": "shy bashful expression", "expr_surprised": "surprised expression",
    "expr_sad": "sad melancholic expression",
    "expr_dreamy": "dreamy wistful expression", "expr_playful": "playful mischievous expression",
    "expr_sultry": "sultry seductive expression", "expr_peaceful": "peaceful serene expression",
    # Number of People (solo is the implicit "a ..." phrasing)
    "ns_solo": "", "ns_duo": "two", "ns_trio": "three", "ns_group": "a group of five",
    # Makeup
    "mu_none": "",
    "mu_red_lip": "elegant makeup with classic bold red lipstick",
    "mu_douyin": "Douyin-style C-beauty makeup with aegyo-sal, precise brows and vivid lips",
    "mu_glam": "full glam makeup with sculpted contour, defined eyes and bold lashes",
    "mu_gradient": "Korean gradient lip makeup with soft blurred lip color",
    "mu_dewy": "Korean-style dewy makeup with luminous glowing skin",
    "mu_natural": "natural light makeup with subtle enhancement",
    "mu_no_makeup": "no-makeup makeup look with bare fresh skin",
    "mu_smoky": "smoky eye makeup with dark blended eyeshadow",
    "mu_soft_matte": "soft matte makeup with a velvet finish",
    # Body Type
    "bt_slim": "slim slender body", "bt_petite": "petite small body frame",
    "bt_lean": "lean toned body", "bt_athletic": "athletic fit toned body",
    "bt_hourglass": "hourglass figure with balanced proportions",
    "bt_curvy": "curvy body with feminine proportions",
    "bt_tall": "tall model-like body proportions", "bt_average": "average body build",
    # Appearance / Vibe
    "app_beautiful": "beautiful gorgeous striking features",
    "app_charming": "charming lovely aura with a warm captivating presence",
    "app_chic": "chic classy polished look with effortless style",
    "app_cool": "cool edgy sharp features with confident attitude",
    "app_cute": "cute adorable baby-faced features",
    "app_doll": "doll-like delicate features with porcelain skin and long lashes",
    "app_elegant": "elegant sophisticated refined features",
    "app_fierce": "fierce bold intense striking features",
    "app_girl_next_door": "approachable girl-next-door charm with a warm friendly smile",
    "app_handsome": "handsome chiseled jawline and sharp features",
    "app_natural": "natural fresh-faced dewy skin look",
    "app_sweet": "sweet innocent youthful features",
    "app_youthful": "youthful glowing look with radiant luminous skin",
    "app_kpop": "youthful K-pop idol look with flawless porcelain skin, soft dewy makeup, and delicate features",
    "app_jpop": "cute J-pop idol look with soft round features, big expressive eyes, and light natural makeup",
    "app_cpop": "elegant C-pop star look with refined features, luminous glass skin, and graceful beauty",
    # Fashion Presets
    "fs_streetwear": "streetwear urban fashion with oversized hoodie and sneakers",
    "fs_korean": "Korean K-fashion style with clean modern silhouette",
    "fs_japanese": "Japanese Harajuku street fashion with bold colorful layers",
    "fs_minimalist": "minimalist clean fashion with neutral tones and simple lines",
    "fs_bohemian": "bohemian boho style with flowing fabrics and layered accessories",
    "fs_vintage": "vintage retro fashion with classic patterns and nostalgic details",
    "fs_gothic": "gothic dark fashion with black clothing and edgy details",
    "fs_preppy": "preppy academic style with collared shirt and pleated skirt",
    "fs_athleisure": "athleisure sporty fashion with fitted activewear",
    "fs_elegant": "elegant formal fashion with sophisticated tailoring",
    "fs_cottagecore": "cottagecore pastoral fashion with floral dress and natural fabrics",
    "fs_cyberpunk": "cyberpunk techwear fashion with futuristic tactical elements",
    "fs_y2k": "Y2K 2000s fashion with low-rise pants and butterfly clips",
    "fs_old_money": "old money quiet luxury fashion with cashmere and understated elegance",
    "fs_grunge": "90s grunge fashion with flannel shirt and ripped jeans",
    "fs_casual": "casual everyday fashion with a comfortable relaxed fit",
    "fs_coquette": "coquette balletcore fashion with ribbons, bows and soft feminine details",
    "fs_office": "polished business casual office fashion",
    "fs_resort": "breezy resort vacation fashion with light summer fabrics",
    "fs_barbiecore": "Barbiecore fashion in head-to-toe pink with playful glamour",
    "fs_clean_girl": "clean girl aesthetic with slicked-back hair, minimal gold jewelry and effortless basics",
    "fs_dark_academia": "dark academia fashion with tweed blazer, turtleneck and vintage scholarly details",
    "fs_egirl": "e-girl alternative fashion with layered chains, striped sleeves and bold eyeliner",
    "fs_gorpcore": "gorpcore outdoor fashion with technical fleece, puffer vest and hiking details",
    "fs_light_academia": "light academia fashion in cream and beige with soft scholarly elegance",
    "fs_mob_wife": "mob wife aesthetic with faux fur coat, gold jewelry and bold sunglasses",
    "fs_parisian": "effortless Parisian chic with breton stripes, trench coat and timeless elegance",
    "fs_rockstar": "rockstar fashion with leather jacket, band tee and studded details",
    "fs_skater": "skater style with baggy pants, graphic tee and skate shoes",
    "fs_thai": "elegant Thai traditional dress with silk fabric and gold accents",
    "fs_western": "western cowboy fashion with denim, boots and fringe details",
    # Fabric
    "fab_none": "",
    "fab_cotton": "cotton fabric", "fab_silk": "silk fabric",
    "fab_denim": "denim", "fab_leather": "leather",
    "fab_lace": "lace fabric", "fab_satin": "satin fabric",
    "fab_wool": "wool knit", "fab_sheer": "sheer translucent fabric",
    "fab_chiffon": "chiffon fabric", "fab_linen": "linen fabric",
    "fab_tweed": "tweed fabric", "fab_velvet": "velvet fabric",
    # Top Garment
    "top_none": "",
    "top_tshirt": "wearing a t-shirt", "top_crop": "wearing a crop top",
    "top_blouse": "wearing a blouse", "top_button_shirt": "wearing a button-up shirt",
    "top_tank": "wearing a tank top", "top_sweater": "wearing a sweater",
    "top_hoodie": "wearing a hoodie",
    "top_turtleneck": "wearing a turtleneck", "top_off_shoulder": "wearing an off-shoulder top",
    "top_camisole": "wearing a camisole", "top_cardigan": "wearing a cardigan",
    "top_blazer": "wearing a tailored blazer", "top_corset": "wearing a corset top",
    "top_denim_jacket": "wearing a denim jacket", "top_halter": "wearing a halter top",
    "top_puff_sleeve": "wearing a puff-sleeve blouse", "top_sweatshirt": "wearing a sweatshirt",
    "top_bodysuit": "wearing a fitted bodysuit",
    "top_bomber": "wearing a bomber jacket",
    "top_bralette": "wearing a bralette top",
    "top_knit_vest": "wearing a knitted sweater vest",
    "top_leather_jacket": "wearing a leather jacket",
    "top_long_sleeve": "wearing a long-sleeve t-shirt",
    "top_oversized_shirt": "wearing an oversized button-down shirt",
    "top_polo": "wearing a polo shirt",
    "top_puffer": "wearing a puffer jacket",
    "top_sports_bra": "wearing a sports bra",
    "top_trench": "wearing a trench coat",
    "top_tube": "wearing a tube top",
    "top_varsity": "wearing a varsity jacket",
    "top_wrap": "wearing a wrap top",
    # Bottom Garment
    "bot_none": "",
    "bot_jeans": "wearing jeans", "bot_mini_skirt": "wearing a mini skirt",
    "bot_maxi_skirt": "wearing a maxi skirt", "bot_pleated_skirt": "wearing a pleated skirt",
    "bot_shorts": "wearing shorts", "bot_wide_leg": "wearing wide-leg pants",
    "bot_cargo": "wearing cargo pants", "bot_leggings": "wearing leggings",
    "bot_pencil_skirt": "wearing a pencil skirt", "bot_a_line": "wearing an A-line skirt",
    "bot_sweatpants": "wearing sweatpants", "bot_trousers": "wearing tailored trousers",
    "bot_denim_shorts": "wearing denim shorts", "bot_overalls": "wearing overalls",
    "bot_slip_skirt": "wearing a satin slip skirt", "bot_tennis_skirt": "wearing a pleated tennis skirt",
    "bot_baggy": "wearing baggy jeans",
    "bot_bike_shorts": "wearing biker shorts",
    "bot_cargo_skirt": "wearing a cargo skirt",
    "bot_culottes": "wearing culottes",
    "bot_denim_skirt": "wearing a denim skirt",
    "bot_flare": "wearing flared jeans",
    "bot_joggers": "wearing jogger pants",
    "bot_midi_skirt": "wearing a midi skirt",
    "bot_palazzo": "wearing flowing palazzo pants",
    "bot_parachute": "wearing parachute pants",
    "bot_ripped": "wearing ripped jeans",
    "bot_skort": "wearing a skort",
    "bot_tulle_skirt": "wearing a layered tulle skirt",
    "bot_yoga": "wearing yoga pants",
    # Footwear
    "sh_none": "",
    "sh_ankle_boots": "wearing ankle boots",
    "sh_ballet": "wearing ballet flats",
    "sh_combat": "wearing chunky combat boots",
    "sh_heels": "wearing high heels",
    "sh_knee_boots": "wearing knee-high boots",
    "sh_loafers": "wearing polished leather loafers",
    "sh_mary_janes": "wearing mary jane shoes",
    "sh_platform": "wearing platform shoes",
    "sh_sandals": "wearing strappy sandals",
    "sh_sneakers": "wearing clean white sneakers",
    "sh_barefoot": "barefoot",
    "sh_chelsea": "wearing chelsea boots",
    "sh_chunky": "wearing chunky dad sneakers",
    "sh_cowboy": "wearing cowboy boots",
    "sh_espadrilles": "wearing espadrilles",
    "sh_flip_flops": "wearing flip-flops",
    "sh_kitten_heels": "wearing kitten heels",
    "sh_mules": "wearing mule shoes",
    "sh_oxford": "wearing oxford shoes",
    "sh_running": "wearing athletic running shoes",
    # Lens (photographic model types only)
    "lens_24": "shot on 24mm wide-angle lens",
    "lens_35": "shot on 35mm lens",
    "lens_50": "shot on 50mm lens",
    "lens_85": "shot on 85mm portrait lens with beautiful compression",
    "lens_135": "shot on 135mm telephoto lens with strong background compression",
    # Color Palette
    "col_none": "",
    "col_red": "red color tones", "col_pink": "pink color tones",
    "col_orange": "orange color tones", "col_yellow": "yellow and gold color tones",
    "col_green": "green color tones", "col_blue": "blue color tones",
    "col_purple": "purple and lavender color tones",
    "col_white": "white and cream color tones", "col_black": "all black color tones",
    "col_beige": "beige and nude color tones", "col_pastel": "pastel colors",
    "col_mono": "monochrome black and white",
    "col_earthy": "earthy brown and natural tones",
    "col_warm": "warm color tones of red orange and gold",
    "col_cool": "cool color tones of blue teal and silver",
    "col_vibrant": "vibrant neon colors",
    "col_burgundy": "burgundy and wine color tones",
    "col_navy": "navy blue color tones",
    "col_sage": "sage green color tones",
    "col_baby_blue": "soft baby blue color tones",
    "col_brown": "brown and chocolate color tones",
    "col_colorblock": "a bold colorblock combination of contrasting colors",
    "col_coral": "coral color tones",
    "col_gold": "shimmering gold metallic tones",
    "col_hot_pink": "vibrant hot pink color tones",
    "col_khaki": "khaki and olive green color tones",
    "col_lilac": "soft lilac color tones",
    "col_mint": "fresh mint green color tones",
    "col_peach": "soft peach color tones",
    "col_silver": "shimmering silver metallic tones",
    "col_teal": "deep teal color tones",
    # Accessories — Head
    "acc_beanie": "wearing a beanie",
    "acc_beret": "wearing a beret",
    "acc_bucket_hat": "wearing a bucket hat",
    "acc_cap": "wearing a cap",
    "acc_glasses": "wearing prescription glasses",
    "acc_hair_clip": "wearing a hair clip",
    "acc_ribbon": "wearing a ribbon bow in hair",
    "acc_hat": "wearing a hat",
    "acc_headband": "wearing a headband",
    "acc_scrunchie": "wearing a scrunchie",
    "acc_sunglasses": "wearing stylish sunglasses",
    "acc_tiara": "wearing a tiara",
    # Accessories — Body / Jewelry
    "acc_anklet": "wearing an anklet",
    "acc_belt": "wearing a belt",
    "acc_bowtie": "wearing a bow tie",
    "acc_bracelet": "wearing a bracelet",
    "acc_choker": "wearing a choker",
    "acc_earrings": "wearing earrings",
    "acc_necklace": "wearing a necklace",
    "acc_necktie": "wearing a necktie",
    "acc_ring": "wearing a ring",
    "acc_scarf": "wearing a scarf",
    "acc_watch": "wearing a wristwatch",
    # Accessories — Carried Items
    "acc_backpack": "carrying a backpack",
    "acc_book": "holding a book",
    "acc_camera": "holding a vintage film camera",
    "acc_clutch": "carrying a clutch bag",
    "acc_crossbody": "wearing a crossbody bag",
    "acc_bouquet": "holding a flower bouquet",
    "acc_bag": "carrying a handbag",
    "acc_coffee": "holding an iced coffee cup",
    "acc_phone": "holding a smartphone",
    "acc_tote": "carrying a tote bag",
    "acc_umbrella": "holding an umbrella",
    # Location
    "loc_studio": "in a professional photography studio with seamless backdrop",
    "loc_street": "on an urban city street with buildings",
    "loc_cafe": "inside a cozy coffee shop",
    "loc_beach": "on a tropical beach with ocean waves",
    "loc_forest": "in a lush green forest surrounded by trees",
    "loc_rooftop": "on a rooftop overlooking the city skyline",
    "loc_room": "in a stylish modern indoor room",
    "loc_temple": "at an ancient temple with historic architecture",
    "loc_garden": "in a beautiful garden with flowers and greenery",
    "loc_amusement": "at a colorful amusement park with a ferris wheel in the background",
    "loc_flower_field": "in a blooming flower field stretching to the horizon",
    "loc_library": "in a cozy library surrounded by tall bookshelves",
    "loc_night_market": "at a vibrant night market with glowing street food stalls",
    "loc_pool": "at a luxurious poolside with clear blue water",
    "loc_shopping": "on a lively shopping street with stylish storefronts",
    "loc_train": "at a scenic train station platform",
    "loc_airport": "at a modern airport terminal with large glass windows and departure boards",
    "loc_aquarium": "inside an aquarium hall glowing with blue light from giant fish tanks",
    "loc_art_gallery": "in a minimalist art gallery with white walls and framed artwork",
    "loc_bridge": "on a scenic bridge overlooking the river and city skyline",
    "loc_castle": "at a majestic castle with grand historic European architecture",
    "loc_desert": "among golden desert sand dunes under a vast open sky",
    "loc_old_town": "on a charming old European town street with cobblestones and classic facades",
    "loc_stairs": "on a grand elegant staircase with ornate railings",
    "loc_gym": "in a modern gym with sleek fitness equipment",
    "loc_lake": "on a wooden pier by a calm lake with mountain reflections",
    "loc_hotel_lobby": "in a luxurious hotel lobby with marble floors and chandeliers",
    "loc_mountain": "at a mountain viewpoint overlooking rolling peaks and valleys",
    "loc_neon_alley": "in a narrow city alley glowing with colorful neon signs",
    "loc_rice_field": "in a lush green rice field in the peaceful countryside",
    "loc_snow": "in a snowy winter landscape covered in fresh white powder snow",
    "loc_subway": "in a modern subway station with clean architectural lines",
    "loc_university": "on a university campus with classic collegiate architecture",
    "loc_waterfall": "at a tropical waterfall surrounded by lush greenery and misty spray",
    # Time of Day
    "tod_golden": "during golden hour with warm sunset light",
    "tod_blue": "during blue hour twilight",
    "tod_noon": "at high noon with bright overhead sunlight",
    "tod_night": "at nighttime with city lights",
    "tod_overcast": "under overcast cloudy sky with soft diffused light",
    "tod_sunrise": "at sunrise with warm morning light",
    # Season
    "season_none": "", "season_spring": "in spring with cherry blossoms and fresh greenery",
    "season_summer": "in summer with bright warm sunshine",
    "season_autumn": "in autumn with warm-toned foliage background",
    "season_winter": "in winter with cold crisp atmosphere",
    "season_rainy": "during rainy season with overcast wet atmosphere",
    # Lighting
    "lit_natural": "natural ambient lighting", "lit_studio": "professional studio softbox lighting",
    "lit_window": "soft natural window light",
    "lit_rim": "dramatic rim lighting from behind",
    "lit_neon": "colorful neon lights with cyberpunk atmosphere",
    "lit_fairy": "warm glowing fairy string lights",
    "lit_candle": "warm candlelight illumination",
    "lit_dramatic": "dramatic chiaroscuro lighting with deep shadows",
    "lit_flash": "direct on-camera flash photography look",
    "lit_backlit": "golden backlighting creating a glowing halo around the subject",
    "lit_dappled": "dappled sunlight filtering through leaves",
    "lit_blinds": "dramatic shadow stripes from window blinds falling across the scene",
    "lit_gel": "cinematic red and blue color gel lighting in duotone",
    "lit_spotlight": "a single dramatic stage spotlight from above",
    "lit_moonlight": "soft cool moonlight illumination",
    "lit_bonfire": "warm flickering campfire glow",
    "lit_godrays": "volumetric god rays streaming through the atmosphere",
    # Picture Style
    "ps_none": "", "ps_dreamy": "dreamy ethereal atmosphere with soft glow and hazy light",
    "ps_soft": "soft gentle tones with smooth gradients and muted colors",
    "ps_vivid": "vivid highly saturated colors with rich contrast",
    "ps_bw": "black and white monochrome photography with rich tonal range",
    "ps_vintage": "vintage retro film look with warm faded tones and slight grain",
    "ps_cinematic": "cinematic color grading with teal and orange tones",
    "ps_moody": "moody dark atmospheric tones with deep shadows",
    "ps_pastel": "pastel light airy color palette with soft delicate hues",
    "ps_hdr": "HDR high dynamic range with vivid detail in highlights and shadows",
    "ps_matte": "matte film finish with reduced contrast and desaturated highlights",
    "ps_commercial": "clean bright commercial photography style with crisp neutral tones",
    "ps_editorial": "high-end editorial magazine aesthetic with refined color grading",
    "ps_documentary": "authentic documentary street photography style capturing natural imperfect moments",
    "ps_polaroid": "instant polaroid photo look with soft faded colors",
    "ps_digicam": "early-2000s digicam aesthetic with harsh flash and slight overexposure",
    "ps_fantasy": "ethereal fantasy atmosphere with magical glowing particles and soft iridescent light",
    "ps_fairytale": "dark fairytale mood with mysterious enchanted atmosphere",
    "ps_cyber": "cyberpunk aesthetic with saturated neon glow and futuristic haze",
    "ps_vaporwave": "vaporwave retrowave aesthetic with pink-purple gradients and 80s glow",
    "ps_surreal": "surreal dreamcore atmosphere with an uncanny dreamlike quality",
    # Shot Framing
    "sf_extreme_cu": "extreme close-up of face only",
    "sf_closeup": "close-up portrait shot showing head and shoulders",
    "sf_medium_cu": "medium close-up from chest up",
    "sf_medium": "medium shot from waist up",
    "sf_cowboy": "cowboy shot from mid-thigh up",
    "sf_medium_full": "medium full shot from knees up",
    "sf_full": "full body shot",
    "sf_wide": "wide shot showing full body and surrounding environment",
    # Camera Angle
    "cam_eye": "shot at eye level", "cam_low": "shot from low angle looking up",
    "cam_high": "shot from high angle looking down",
    "cam_3q": "three-quarter view", "cam_profile": "side profile view",
    "cam_selfie": "selfie angle shot from arm's length slightly above eye level",
    "cam_dutch": "dutch angle tilted composition",
    "cam_over_shoulder": "over-the-shoulder shot", "cam_bird": "bird's eye view from directly above",
    "cam_worm": "worm's eye view from ground level looking straight up",
    "cam_ground": "ground level shot with the camera placed close to the floor",
    "cam_pov": "first-person POV shot",
    "cam_back": "shot from directly behind the subject",
    # Depth of Field
    "dof_sharp": "deep focus with everything sharp",
    "dof_portrait": "shallow depth of field at f/1.8 with subject in sharp focus and beautifully blurred bokeh background",
    "dof_shallow": "very shallow depth of field at f/1.2 with heavy creamy bokeh and dreamy atmosphere",
    "dof_tiltshift": "tilt-shift effect creating miniature model appearance",
    "dof_soft": "soft dreamy glow with gentle diffusion",
    "dof_bokeh_lights": "shallow depth of field with glowing round bokeh light orbs in the background",
    "dof_motion": "subject in sharp focus with motion-blurred background conveying movement",
    "dof_fg_blur": "shot through blurred foreground elements creating a dreamy layered frame",
    "dof_clean_bg": "clean minimal seamless background with the subject in crisp focus",
    # Composition
    "comp_center": "",
    "comp_rot_left": "rule of thirds composition with subject positioned on the left third of the frame",
    "comp_rot_right": "rule of thirds composition with subject positioned on the right third of the frame",
    "comp_golden": "golden ratio composition with subject at the golden spiral focal point",
    "comp_leading": "composition with leading lines drawing the eye toward the subject",
    "comp_framed": "subject framed through a natural foreground frame like a doorway or foliage",
    "comp_negative_space": "composed with generous negative space around the subject",
    "comp_symmetry": "symmetrical composition with subject centered along the axis of symmetry",
    "comp_diagonal": "dynamic composition built on strong diagonal lines",
    "comp_fill": "tight composition with the subject filling the entire frame",
    "comp_reflection": "creative reflection composition using a mirror or water surface",
    "comp_depth": "layered composition with distinct foreground, midground and background depth",
    # Pose (sorted A-Z)
    "pose_arms_up": "with arms raised above head",
    "pose_cross_arms": "with arms crossed",
    "pose_back_camera": "facing away from camera showing back",
    "pose_blow_kiss": "blowing a kiss toward the camera",
    "pose_cross_leg": "sitting with legs crossed elegantly",
    "pose_crouch": "crouching down",
    "pose_dynamic": "in a dynamic action pose",
    "pose_hand_hair": "with hand running through hair",
    "pose_hand_chin": "resting chin on hand thoughtfully",
    "pose_hands_back": "standing sweetly with hands clasped behind back",
    "pose_cheek_hands": "with both hands framing the face cutely",
    "pose_hands_pocket": "with hands in pockets casually",
    "pose_heart_hands": "making a heart shape with both hands toward the camera",
    "pose_hug_knees": "sitting hugging knees to chest",
    "pose_jump": "jumping in the air",
    "pose_kneel": "kneeling on the ground",
    "pose_lean": "leaning against a wall",
    "pose_looking_away": "looking away from camera",
    "pose_over_shoulder": "looking back over shoulder",
    "pose_lying": "lying down relaxed",
    "pose_mini_heart": "making a mini heart gesture with thumb and index finger",
    "pose_peace": "flashing a cute peace sign",
    "pose_run": "running in motion",
    "pose_s_curve": "standing in an S-curve pose with weight on one hip",
    "pose_sit": "sitting comfortably",
    "pose_stand": "standing elegantly",
    "pose_hair_tuck": "gently tucking hair behind ear",
    "pose_twirl": "twirling with movement in clothing",
    "pose_w_sit": "sitting in a W-sit position with legs folded to the sides",
    "pose_walk": "walking naturally",
    "pose_wink": "winking playfully at the camera",
    "pose_fix_jacket": "adjusting jacket collar with a confident look",
    "pose_adjust_glasses": "stylishly adjusting sunglasses",
    "pose_finger_heart": "making a cute Korean finger heart gesture",
    "pose_hair_flip": "flipping hair dramatically in motion",
    "pose_arms_behind_head": "with hands clasped behind head, relaxed",
    "pose_railing": "leaning casually on a railing",
    "pose_look_back_walk": "walking away and glancing back over shoulder at the camera",
    "pose_mirror_selfie": "taking a mirror selfie with a smartphone",
    "pose_peek_fingers": "peeking playfully through fingers held near the eyes",
    "pose_reach_camera": "reaching one hand out toward the camera, follow-me style",
    "pose_shield_sun": "raising one hand to shield eyes from the sun",
    "pose_legs_extended": "sitting on the ground with legs extended, leaning back on hands",
    "pose_squat": "posing in a low streetwear squat",
    "pose_hold_hat": "touching the brim of a hat stylishly",
    "pose_walk_away": "walking away from the camera candidly",
    "pose_arms_open": "with arms open wide in a joyful welcoming gesture",
    "pose_candid": "captured candidly in natural unposed movement",
    "pose_chin_up": "with chin tilted up in a confident poised stance",
    "pose_dance": "dancing gracefully with flowing movement",
    "pose_editorial": "striking an avant-garde editorial fashion pose with angular arm placement",
    "pose_elegant": "posing with elegant graceful posture and refined hand gestures",
    "pose_hand_hip": "standing with one hand on hip",
    "pose_head_tilt": "tilting head cutely to one side",
    "pose_high_fashion": "in a high-fashion model stance with strong confident body lines",
    "pose_lean_forward": "leaning toward the camera playfully",
    "pose_look_up": "gazing upward with a dreamy expression",
    "pose_runway": "walking a runway stride with confident model attitude",
    "pose_sit_stairs": "sitting casually on a set of stairs",
    "pose_stretch": "stretching arms overhead in a graceful pose",
    # Model Type
    "model_realistic": "Photorealistic",
    "model_cinematic": "cinematic film still with movie-quality production",
    "model_film": "analog film photograph with natural grain, Kodak Portra 400",
    "model_fashion": "high-fashion editorial photography",
    "model_anime": "Anime illustration style",
    "model_digital_painting": "detailed digital painting artwork",
    "model_watercolor": "soft watercolor painting with delicate brush strokes",
    "model_comic": "comic manga style illustration with clean line art",
    "model_3d": "3D rendered CGI",
    # Quality
    "qt_8k": "8K UHD", "qt_detail": "highly detailed", "qt_sharp": "sharp focus",
    "qt_pro": "professional photography", "qt_award": "award-winning", "qt_magazine": "magazine quality",
    # Aspect Ratio
    "ar_1_1": "--ar 1:1", "ar_16_9": "--ar 16:9", "ar_9_16": "--ar 9:16", "ar_4_5": "--ar 4:5",
    "ar_3_2": "--ar 3:2", "ar_2_3": "--ar 2:3",
    "ar_4_3": "--ar 4:3", "ar_3_4": "--ar 3:4",
    "ar_iphone": "--ar 1179:2556", "ar_android": "--ar 1080:2400",
}


# ═══════════════════════════════════════════════════════════════════════════
#  3. HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def t(key: str) -> str:
    lang = st.session_state.get("lang", "en")
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

def eng(key: str) -> str:
    return ENGLISH_VALUES.get(key, "")

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
AG_KEYS = ["age_20_25", "age_5_9", "age_10_14", "age_15_19",
           "age_26_35", "age_36_45", "age_46_60", "age_60plus"]
ET_KEYS = ["eth_asian", "eth_se_asian", "eth_south_asian", "eth_european",
           "eth_african", "eth_latin", "eth_middle_east", "eth_mixed"]
NS_KEYS = ["ns_solo", "ns_duo", "ns_trio", "ns_group"]
HR_KEYS_WOMEN = [
    "hair_long", "hair_straight", "hair_loose_waves",
    "hair_curly", "hair_wavy", "hair_layered", "hair_wolf_cut",
    "hair_hush_cut", "hair_hime", "hair_bob", "hair_lob", "hair_pixie",
    "hair_ponytail", "hair_high_ponytail", "hair_bun", "hair_messy_bun",
    "hair_space_buns", "hair_braids", "hair_french_braid",
    "hair_twin_braids", "hair_twintails",
    "hair_half_up", "hair_side_swept",
]
HR_KEYS_MEN = [
    "hair_short", "hair_buzz", "hair_crew_cut", "hair_middle_part",
    "hair_textured_crop", "hair_undercut", "hair_fade", "hair_slick_back",
    "hair_man_bun", "hair_bald",
]
# Full list (used for non-binary and as the language-reset superset)
HR_KEYS = HR_KEYS_WOMEN + HR_KEYS_MEN

def hair_keys_for_gender(gd_key: str):
    """Hairstyle option pool filtered by the selected gender."""
    if gd_key == "gender_female":
        return HR_KEYS_WOMEN
    if gd_key == "gender_male":
        return HR_KEYS_MEN
    return HR_KEYS
HC_KEYS = ["hc_black", "hc_blue_black", "hc_dark_brown", "hc_ash_brown",
           "hc_milk_tea", "hc_light_brown", "hc_honey_blonde", "hc_blonde",
           "hc_platinum", "hc_red", "hc_burgundy", "hc_rose_gold",
           "hc_pink", "hc_purple", "hc_blue", "hc_silver", "hc_white",
           "hc_ombre", "hc_highlights"]
BN_KEYS = ["bangs_none", "bangs_straight", "bangs_see_through", "bangs_side",
           "bangs_curtain", "bangs_wispy", "bangs_micro", "bangs_hime"]
EX_KEYS = ["expr_smile", "expr_bright_smile", "expr_laugh", "expr_giggle",
           "expr_soft_gaze", "expr_doe_eyes", "expr_pout", "expr_playful",
           "expr_shy", "expr_confident", "expr_smirk", "expr_dreamy",
           "expr_peaceful", "expr_neutral", "expr_pensive",
           "expr_serious", "expr_surprised", "expr_sad", "expr_sultry"]
BT_KEYS = ["bt_slim", "bt_petite", "bt_lean", "bt_athletic",
           "bt_hourglass", "bt_curvy", "bt_tall", "bt_average"]
AP_KEYS = ["app_beautiful", "app_cpop", "app_charming", "app_chic",
           "app_cool", "app_cute", "app_doll", "app_elegant",
           "app_fierce", "app_girl_next_door", "app_handsome",
           "app_jpop", "app_kpop", "app_natural", "app_sweet", "app_youthful"]
MU_KEYS = ["mu_none", "mu_red_lip", "mu_douyin", "mu_glam", "mu_gradient",
           "mu_dewy", "mu_natural", "mu_no_makeup", "mu_smoky", "mu_soft_matte"]
FS_KEYS = ["fs_athleisure", "fs_barbiecore", "fs_bohemian", "fs_office",
           "fs_casual", "fs_clean_girl", "fs_coquette", "fs_cottagecore",
           "fs_cyberpunk", "fs_dark_academia", "fs_egirl", "fs_elegant",
           "fs_gorpcore", "fs_gothic", "fs_grunge", "fs_japanese",
           "fs_korean", "fs_light_academia", "fs_minimalist", "fs_mob_wife",
           "fs_old_money", "fs_parisian", "fs_preppy", "fs_resort",
           "fs_rockstar", "fs_skater", "fs_streetwear", "fs_thai",
           "fs_vintage", "fs_western", "fs_y2k"]
FB_KEYS = ["fab_none", "fab_chiffon", "fab_cotton", "fab_denim", "fab_lace",
           "fab_leather", "fab_linen", "fab_satin", "fab_sheer",
           "fab_silk", "fab_tweed", "fab_velvet", "fab_wool"]
CP_KEYS = ["col_none", "col_black", "col_baby_blue", "col_beige", "col_blue",
           "col_brown", "col_burgundy", "col_colorblock", "col_cool",
           "col_coral", "col_earthy", "col_gold", "col_green", "col_hot_pink",
           "col_khaki", "col_lilac", "col_mint", "col_mono", "col_navy",
           "col_orange", "col_pastel", "col_peach", "col_pink", "col_purple",
           "col_red", "col_sage", "col_silver", "col_teal", "col_vibrant",
           "col_warm", "col_white", "col_yellow"]
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
LO_KEYS = ["loc_studio", "loc_airport", "loc_amusement", "loc_aquarium",
           "loc_art_gallery", "loc_beach", "loc_bridge", "loc_castle",
           "loc_cafe", "loc_desert", "loc_old_town", "loc_flower_field",
           "loc_forest", "loc_garden", "loc_stairs", "loc_gym", "loc_room",
           "loc_lake", "loc_library", "loc_hotel_lobby", "loc_mountain",
           "loc_neon_alley", "loc_night_market", "loc_pool", "loc_rice_field",
           "loc_rooftop", "loc_shopping", "loc_snow", "loc_subway",
           "loc_temple", "loc_train", "loc_university", "loc_street",
           "loc_waterfall"]
TD_KEYS = ["tod_golden", "tod_blue", "tod_noon", "tod_night", "tod_overcast", "tod_sunrise"]
LT_KEYS = ["lit_natural", "lit_window", "lit_studio", "lit_rim",
           "lit_neon", "lit_fairy", "lit_candle", "lit_dramatic", "lit_flash",
           "lit_backlit", "lit_dappled", "lit_blinds", "lit_gel",
           "lit_spotlight", "lit_moonlight", "lit_bonfire", "lit_godrays"]
SN_KEYS = ["season_none", "season_spring", "season_summer",
           "season_autumn", "season_winter", "season_rainy"]
PS_KEYS = ["ps_none", "ps_dreamy", "ps_soft", "ps_vivid", "ps_bw",
           "ps_vintage", "ps_cinematic", "ps_moody", "ps_pastel",
           "ps_hdr", "ps_matte", "ps_commercial", "ps_editorial",
           "ps_documentary", "ps_polaroid", "ps_digicam", "ps_fantasy",
           "ps_fairytale", "ps_cyber", "ps_vaporwave", "ps_surreal"]
SF_KEYS = ["sf_extreme_cu", "sf_closeup", "sf_medium_cu", "sf_medium",
           "sf_cowboy", "sf_medium_full", "sf_full", "sf_wide"]
CA_KEYS = ["cam_eye", "cam_low", "cam_worm", "cam_ground", "cam_high",
           "cam_3q", "cam_profile", "cam_selfie", "cam_dutch",
           "cam_over_shoulder", "cam_back", "cam_pov", "cam_bird"]
DOF_KEYS = ["dof_sharp", "dof_portrait", "dof_shallow", "dof_bokeh_lights",
            "dof_motion", "dof_fg_blur", "dof_clean_bg",
            "dof_tiltshift", "dof_soft"]
CMP_KEYS = ["comp_center", "comp_rot_left", "comp_rot_right",
            "comp_golden", "comp_leading", "comp_framed",
            "comp_negative_space", "comp_symmetry", "comp_diagonal",
            "comp_fill", "comp_reflection", "comp_depth"]
PO_KEYS = ["pose_fix_jacket", "pose_adjust_glasses", "pose_arms_up",
           "pose_cross_arms", "pose_arms_open", "pose_back_camera",
           "pose_blow_kiss", "pose_candid", "pose_chin_up",
           "pose_cross_leg", "pose_crouch", "pose_dance",
           "pose_dynamic", "pose_editorial", "pose_elegant",
           "pose_finger_heart", "pose_hair_flip", "pose_hand_hair",
           "pose_hand_chin", "pose_hand_hip", "pose_hands_back",
           "pose_arms_behind_head", "pose_cheek_hands",
           "pose_hands_pocket", "pose_head_tilt", "pose_heart_hands",
           "pose_high_fashion", "pose_hug_knees", "pose_jump",
           "pose_kneel", "pose_lean", "pose_railing", "pose_lean_forward",
           "pose_looking_away", "pose_look_back_walk",
           "pose_over_shoulder", "pose_look_up", "pose_lying",
           "pose_mini_heart", "pose_mirror_selfie", "pose_peace",
           "pose_peek_fingers", "pose_reach_camera", "pose_run",
           "pose_runway", "pose_s_curve", "pose_shield_sun", "pose_sit",
           "pose_sit_stairs", "pose_legs_extended", "pose_stand",
           "pose_squat", "pose_stretch", "pose_hold_hat",
           "pose_hair_tuck", "pose_twirl", "pose_w_sit",
           "pose_walk", "pose_walk_away", "pose_wink"]

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
    "w_angle": CA_KEYS, "w_dof": DOF_KEYS, "w_comp": CMP_KEYS, "w_pose": PO_KEYS,
}

# Scene/camera subset for the "Random Scene" button — keeps the subject,
# outfit and pose untouched (useful for consistent-character variations).
SCENE_RANDOM_WIDGETS = {
    "w_location": LO_KEYS, "w_tod": TD_KEYS, "w_lighting": LT_KEYS,
    "w_season": SN_KEYS, "w_pstyle": PS_KEYS, "w_framing": SF_KEYS,
    "w_angle": CA_KEYS, "w_dof": DOF_KEYS, "w_comp": CMP_KEYS,
}

# Widgets whose stored value is a translated label — must be reset when the
# UI language changes, otherwise the stale label is no longer a valid option.
LANG_DEPENDENT_WIDGETS = list(RANDOM_WIDGETS) + [
    "fashion_multi", "w_gender", "w_age", "w_eth", "w_hair",
    "w_top", "top_fabric_sel", "top_color_sel",
    "w_bottom", "bot_fabric_sel", "bot_color_sel", "w_shoes",
    "w_hair_p2", "w_hair_color_p2", "w_expr_p2",
    "w_hair_p3", "w_hair_color_p3", "w_expr_p3",
]

# Per-person hairstyle widgets — all depend on the gender's hair pool
HAIR_WIDGET_KEYS = ("w_hair", "w_hair_p2", "w_hair_p3")

# Widget key → option key list, for saving/loading a look as JSON.
# Presets store option KEYS (language-independent), not translated labels.
PRESET_WIDGETS = {
    "w_gender": GD_KEYS, "w_age": AG_KEYS, "w_eth": ET_KEYS,
    "w_hair": HR_KEYS, "w_hair_color": HC_KEYS, "w_bangs": BN_KEYS,
    "w_expr": EX_KEYS, "w_body": BT_KEYS, "w_appearance": AP_KEYS,
    "w_makeup": MU_KEYS,
    "w_top": TOP_KEYS, "top_fabric_sel": FB_KEYS, "top_color_sel": CP_KEYS,
    "w_bottom": BOT_KEYS, "bot_fabric_sel": FB_KEYS, "bot_color_sel": CP_KEYS,
    "w_shoes": SH_KEYS,
    "w_hair_p2": HR_KEYS, "w_hair_color_p2": HC_KEYS, "w_expr_p2": EX_KEYS,
    "w_hair_p3": HR_KEYS, "w_hair_color_p3": HC_KEYS, "w_expr_p3": EX_KEYS,
    "w_location": LO_KEYS, "w_tod": TD_KEYS, "w_lighting": LT_KEYS,
    "w_season": SN_KEYS, "w_pstyle": PS_KEYS, "w_framing": SF_KEYS,
    "w_angle": CA_KEYS, "w_dof": DOF_KEYS, "w_comp": CMP_KEYS, "w_pose": PO_KEYS,
}


def reset_hair_on_gender_change():
    """The hairstyle option lists depend on gender — drop stale selections."""
    for wk in HAIR_WIDGET_KEYS:
        st.session_state.pop(wk, None)


def randomize_look():
    """Pick a random label for every style widget, then auto-generate."""
    for widget_key, option_keys in RANDOM_WIDGETS.items():
        st.session_state[widget_key] = t(random.choice(option_keys))
    # Hair: pick from the pool matching the currently selected gender
    gd_label = st.session_state.get("w_gender", t("gender_female"))
    if gd_label == t("gender_male"):
        hair_pool = HR_KEYS_MEN
    elif gd_label == t("gender_nb"):
        hair_pool = HR_KEYS
    else:
        hair_pool = HR_KEYS_WOMEN
    st.session_state["w_hair"] = t(random.choice(hair_pool))
    # Extra persons (only visible for duo/trio) get distinct random looks too
    for suffix in ("_p2", "_p3"):
        st.session_state[f"w_hair{suffix}"] = t(random.choice(hair_pool))
        st.session_state[f"w_hair_color{suffix}"] = t(random.choice(HC_KEYS))
        st.session_state[f"w_expr{suffix}"] = t(random.choice(EX_KEYS))
    # Outfit: either a fashion style OR explicit garments, never both
    if random.random() < 0.5:
        st.session_state["fashion_multi"] = [t(k) for k in random.sample(FS_KEYS, random.randint(1, 2))]
        st.session_state["w_top"] = t("top_none")
        st.session_state["w_bottom"] = t("bot_none")
        st.session_state["top_fabric_sel"] = t("fab_none")
        st.session_state["bot_fabric_sel"] = t("fab_none")
        st.session_state["top_color_sel"] = t("col_none")
        st.session_state["bot_color_sel"] = t("col_none")
        st.session_state["w_shoes"] = t("sh_none")
    else:
        st.session_state["fashion_multi"] = []
        st.session_state["w_top"] = t(random.choice(TOP_KEYS[1:]))
        st.session_state["w_bottom"] = t(random.choice(BOT_KEYS[1:]))
        st.session_state["top_fabric_sel"] = t(random.choice(FB_KEYS[1:]))
        st.session_state["bot_fabric_sel"] = t(random.choice(FB_KEYS[1:]))
        st.session_state["top_color_sel"] = t(random.choice(CP_KEYS[1:]))
        st.session_state["bot_color_sel"] = t(random.choice(CP_KEYS[1:]))
        st.session_state["w_shoes"] = t(random.choice(SH_KEYS[1:]))
    st.session_state["force_generate"] = True


def randomize_scene():
    """Randomize only scene/camera widgets, keeping subject/outfit/pose fixed."""
    for widget_key, option_keys in SCENE_RANDOM_WIDGETS.items():
        st.session_state[widget_key] = t(random.choice(option_keys))
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
    # Gender first — the hairstyle pool depends on it
    gd = data.get("w_gender")
    if gd in GD_KEYS:
        st.session_state["w_gender"] = t(gd)
    else:
        gd = None
    for widget_key, option_keys in PRESET_WIDGETS.items():
        val = data.get(widget_key)
        if not isinstance(val, str) or val not in option_keys:
            continue
        # Hairstyles must exist in the pool of the (possibly new) gender
        if widget_key in HAIR_WIDGET_KEYS:
            gd_label = st.session_state.get("w_gender", t("gender_female"))
            pool = HR_KEYS_MEN if gd_label == t("gender_male") else (
                HR_KEYS if gd_label == t("gender_nb") else HR_KEYS_WOMEN)
            if val not in pool:
                st.session_state.pop(widget_key, None)
                continue
        st.session_state[widget_key] = t(val)
    fs = data.get("fashion_multi", [])
    if isinstance(fs, list):
        st.session_state["fashion_multi"] = [t(k) for k in fs if k in FS_KEYS]
    st.session_state["preset_status"] = "ok"
    st.session_state["force_generate"] = True


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

        # Midjourney-only knobs, appended to the --ar parameter block
        mj_stylize = 100
        mj_seed = ""
        if pf_selected_key == "platform_midjourney":
            mj_stylize = st.number_input(t("mj_stylize"), min_value=0,
                                         max_value=1000, value=100, step=50)
            mj_seed = st.text_input(t("mj_seed"), value="")

        st.divider()
        st.caption("v5.4 — AI Prompt Generator")

    # ── Header ───────────────────────────────────────────────────────────
    st.markdown(
        f'<div class="app-header"><h1>🎨 {t("app_title")}</h1>'
        f'<p>{t("app_subtitle")}</p></div>',
        unsafe_allow_html=True,
    )

    # ══════════════════════════════════════════════════════════════════════
    #  EXPANDER 1 — Subject
    # ══════════════════════════════════════════════════════════════════════
    with st.expander(f"👤  {t('exp_subject')}", expanded=True):
        # Reference photo checkbox (no file uploader — just a toggle)
        attach_subject = st.checkbox(t("attach_subject_photo"), key="attach_subject")
        if attach_subject:
            st.markdown(f'<div class="ref-attached">📎 {t("attach_subject_note")}</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            gd_labels, _ = make_option(GD_KEYS)
            gd_sel = st.selectbox(t("gender"), gd_labels, key="w_gender",
                                  on_change=reset_hair_on_gender_change)
            gd_key = GD_KEYS[gd_labels.index(gd_sel)]
        with col2:
            ag_labels, _ = make_option(AG_KEYS)
            ag_sel = st.selectbox(t("age_group"), ag_labels, key="w_age")
            ag_key = AG_KEYS[ag_labels.index(ag_sel)]
        with col3:
            et_labels, _ = make_option(ET_KEYS)
            et_sel = st.selectbox(t("ethnicity"), et_labels, key="w_eth")
            et_key = ET_KEYS[et_labels.index(et_sel)]

        col4, col5 = st.columns(2)
        with col4:
            hr_options = hair_keys_for_gender(gd_key)
            hr_labels, _ = make_option(hr_options)
            hr_sel = st.selectbox(t("hair_style"), hr_labels, key="w_hair")
            hr_key = hr_options[hr_labels.index(hr_sel)]
        with col5:
            hc_labels, _ = make_option(HC_KEYS)
            hc_sel = st.selectbox(t("hair_color"), hc_labels, key="w_hair_color")
            hc_key = HC_KEYS[hc_labels.index(hc_sel)]

        col_bn, col_ex = st.columns(2)
        with col_bn:
            bn_labels, _ = make_option(BN_KEYS)
            bn_sel = st.selectbox(t("bangs"), bn_labels, key="w_bangs")
            bn_key = BN_KEYS[bn_labels.index(bn_sel)]
        with col_ex:
            ex_labels, _ = make_option(EX_KEYS)
            ex_sel = st.selectbox(t("expression"), ex_labels, key="w_expr")
            ex_key = EX_KEYS[ex_labels.index(ex_sel)]

        col_mu, col_ns = st.columns(2)
        with col_mu:
            mu_labels, _ = make_option(MU_KEYS)
            mu_sel = st.selectbox(t("makeup"), mu_labels, key="w_makeup")
            mu_key = MU_KEYS[mu_labels.index(mu_sel)]
        with col_ns:
            ns_labels, _ = make_option(NS_KEYS)
            ns_sel = st.selectbox(t("num_subjects"), ns_labels)
            ns_key = NS_KEYS[ns_labels.index(ns_sel)]

        # Per-person looks so a duo/trio doesn't come out as identical clones.
        # Person 1 uses the main selectors above; each extra person gets their
        # own hair / hair color / expression (different defaults on purpose).
        extra_person_keys = []
        if ns_key in ("ns_duo", "ns_trio"):
            st.caption(t("multi_person_hint"))
            for pi in range(2, 3 if ns_key == "ns_duo" else 4):
                st.markdown(f"**{t(f'person_{pi}')}**")
                pc1, pc2, pc3 = st.columns(3)
                with pc1:
                    p_hr_labels, _ = make_option(hr_options)
                    p_hr_sel = st.selectbox(
                        t("hair_style"), p_hr_labels,
                        index=min(3 * (pi - 1), len(hr_options) - 1),
                        key=f"w_hair_p{pi}")
                    p_hr_key = hr_options[p_hr_labels.index(p_hr_sel)]
                with pc2:
                    p_hc_labels, _ = make_option(HC_KEYS)
                    p_hc_sel = st.selectbox(
                        t("hair_color"), p_hc_labels,
                        index=min(6 * (pi - 1), len(HC_KEYS) - 1),
                        key=f"w_hair_color_p{pi}")
                    p_hc_key = HC_KEYS[p_hc_labels.index(p_hc_sel)]
                with pc3:
                    p_ex_labels, _ = make_option(EX_KEYS)
                    p_ex_sel = st.selectbox(
                        t("expression"), p_ex_labels,
                        index=min(1 + 9 * (pi - 2), len(EX_KEYS) - 1),
                        key=f"w_expr_p{pi}")
                    p_ex_key = EX_KEYS[p_ex_labels.index(p_ex_sel)]
                extra_person_keys.append((p_hr_key, p_hc_key, p_ex_key))
        elif ns_key == "ns_group":
            st.caption(t("group_hint"))

        col7, _ = st.columns(2)
        with col7:
            skin_check = st.checkbox(t("skin_detail"))

        col_bt, col_ap = st.columns(2)
        with col_bt:
            bt_labels, _ = make_option(BT_KEYS)
            bt_sel = st.selectbox(t("body_type"), bt_labels, key="w_body")
            bt_key = BT_KEYS[bt_labels.index(bt_sel)]
        with col_ap:
            ap_labels, _ = make_option(AP_KEYS)
            ap_sel = st.selectbox(t("appearance"), ap_labels, key="w_appearance")
            ap_key = AP_KEYS[ap_labels.index(ap_sel)]

    # ══════════════════════════════════════════════════════════════════════
    #  EXPANDER 2 — Outfit & Style
    # ══════════════════════════════════════════════════════════════════════
    with st.expander(f"👗  {t('exp_outfit')}", expanded=True):
        # Fashion presets (A-Z)
        fs_labels = [t(k) for k in FS_KEYS]
        fs_selected_labels = st.multiselect(t("fashion_presets"), fs_labels, default=[],
                                             help=t("fashion_presets_help"), key="fashion_multi")
        fs_selected_keys = [FS_KEYS[fs_labels.index(lbl)] for lbl in fs_selected_labels]

        st.markdown("---")

        # ── Top: garment + fabric + color ──
        # Garments default to "None" so a fashion preset alone fully defines
        # the outfit; fabric/color pickers only appear once a garment is chosen.
        col_top, col_bot = st.columns(2)
        with col_top:
            top_labels, _ = make_option(TOP_KEYS)
            top_sel = st.selectbox(t("top_garment"), top_labels, key="w_top")
            top_key = TOP_KEYS[top_labels.index(top_sel)]
            top_fb_key, top_cp_key = "fab_none", "col_none"
            if top_key != "top_none":
                top_fb_labels, _ = make_option(FB_KEYS)
                top_fb_sel = st.selectbox(t("top_fabric"), top_fb_labels, key="top_fabric_sel")
                top_fb_key = FB_KEYS[top_fb_labels.index(top_fb_sel)]
                top_cp_labels, _ = make_option(CP_KEYS)
                top_cp_sel = st.selectbox(t("top_color"), top_cp_labels, key="top_color_sel")
                top_cp_key = CP_KEYS[top_cp_labels.index(top_cp_sel)]
        # ── Bottom: garment + fabric + color ──
        with col_bot:
            bot_labels, _ = make_option(BOT_KEYS)
            bot_sel = st.selectbox(t("bottom_garment"), bot_labels, key="w_bottom")
            bot_key = BOT_KEYS[bot_labels.index(bot_sel)]
            bot_fb_key, bot_cp_key = "fab_none", "col_none"
            if bot_key != "bot_none":
                bot_fb_labels, _ = make_option(FB_KEYS)
                bot_fb_sel = st.selectbox(t("bot_fabric"), bot_fb_labels, key="bot_fabric_sel")
                bot_fb_key = FB_KEYS[bot_fb_labels.index(bot_fb_sel)]
                bot_cp_labels, _ = make_option(CP_KEYS)
                bot_cp_sel = st.selectbox(t("bot_color"), bot_cp_labels, key="bot_color_sel")
                bot_cp_key = CP_KEYS[bot_cp_labels.index(bot_cp_sel)]

        # Gentle warning when a preset style and explicit garments are mixed
        if fs_selected_keys and (top_key != "top_none" or bot_key != "bot_none"):
            st.caption(t("outfit_clash_hint"))

        col_sh, _ = st.columns(2)
        with col_sh:
            sh_labels, _ = make_option(SH_KEYS)
            sh_sel = st.selectbox(t("footwear"), sh_labels, key="w_shoes")
            sh_key = SH_KEYS[sh_labels.index(sh_sel)]

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
                         "acc_glasses", "acc_hair_clip", "acc_ribbon", "acc_hat",
                         "acc_headband", "acc_scrunchie", "acc_sunglasses", "acc_tiara"]
        acc_body_keys = ["acc_anklet", "acc_belt", "acc_bowtie", "acc_bracelet",
                         "acc_choker", "acc_earrings", "acc_necklace", "acc_necktie",
                         "acc_ring", "acc_scarf", "acc_watch"]
        acc_carried_keys = ["acc_backpack", "acc_book", "acc_camera", "acc_clutch",
                            "acc_crossbody", "acc_bouquet", "acc_bag", "acc_coffee",
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
    #  EXPANDER 3 — Scene & Lighting
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
            lo_labels, _ = make_option(LO_KEYS)
            lo_sel = st.selectbox(t("location"), lo_labels, key="w_location")
            lo_key = LO_KEYS[lo_labels.index(lo_sel)]
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
        col10, col11, col_season, col_ps = st.columns(4)
        with col10:
            td_labels, _ = make_option(TD_KEYS)
            td_sel = st.selectbox(t("time_of_day"), td_labels, key="w_tod")
            td_key = TD_KEYS[td_labels.index(td_sel)]
        with col11:
            lt_labels, _ = make_option(LT_KEYS)
            lt_sel = st.selectbox(t("lighting"), lt_labels, key="w_lighting")
            lt_key = LT_KEYS[lt_labels.index(lt_sel)]
        with col_season:
            sn_labels, _ = make_option(SN_KEYS)
            sn_sel = st.selectbox(t("season"), sn_labels, key="w_season")
            sn_key = SN_KEYS[sn_labels.index(sn_sel)]
            weather_rain = st.checkbox(t("weather_rain"), key="weather_rain_cb")
            weather_snow = st.checkbox(t("weather_snow"), key="weather_snow_cb")
            weather_leaves = st.checkbox(t("weather_leaves"), key="weather_leaves_cb")
        with col_ps:
            ps_labels, _ = make_option(PS_KEYS)
            ps_sel = st.selectbox(t("picture_style"), ps_labels, key="w_pstyle")
            ps_key = PS_KEYS[ps_labels.index(ps_sel)]

        st.markdown("---")

        # ── Shot Framing + Camera Angle + DOF ──
        col12, col13 = st.columns(2)
        with col12:
            sf_labels, _ = make_option(SF_KEYS)
            sf_sel = st.selectbox(t("shot_framing"), sf_labels, index=1, key="w_framing")
            sf_key = SF_KEYS[sf_labels.index(sf_sel)]
        with col13:
            ca_labels, _ = make_option(CA_KEYS)
            ca_sel = st.selectbox(t("camera_angle"), ca_labels, key="w_angle")
            ca_key = CA_KEYS[ca_labels.index(ca_sel)]

        col14, col15, col16 = st.columns(3)
        with col14:
            dof_labels, _ = make_option(DOF_KEYS)
            dof_sel = st.selectbox(t("dof"), dof_labels, index=1, key="w_dof")
            dof_key = DOF_KEYS[dof_labels.index(dof_sel)]
        with col15:
            cmp_labels, _ = make_option(CMP_KEYS)
            cmp_sel = st.selectbox(t("composition"), cmp_labels, key="w_comp")
            cmp_key = CMP_KEYS[cmp_labels.index(cmp_sel)]
        with col16:
            po_labels, _ = make_option(PO_KEYS)
            po_sel = st.selectbox(t("pose"), po_labels, key="w_pose")
            po_key = PO_KEYS[po_labels.index(po_sel)]
        look_at_camera = st.checkbox(t("look_camera"))

    # ══════════════════════════════════════════════════════════════════════
    #  EXPANDER 4 — Advanced
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
            "w_location": lo_key, "w_tod": td_key, "w_lighting": lt_key,
            "w_season": sn_key, "w_pstyle": ps_key, "w_framing": sf_key,
            "w_angle": ca_key, "w_dof": dof_key, "w_comp": cmp_key, "w_pose": po_key,
        }
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
    gen_col, rand_col, scene_col = st.columns([1, 1, 1])
    with gen_col:
        generate_clicked = st.button(f"🚀  {t('generate_btn')}", type="primary", use_container_width=True)
    with rand_col:
        st.button(f"🎲  {t('random_btn')}", on_click=randomize_look, use_container_width=True)
    with scene_col:
        st.button(f"🎬  {t('random_scene_btn')}", on_click=randomize_scene, use_container_width=True)
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
        for qk in qt_selected:
            specs.append(eng(qk))
        technical = ", ".join(specs)

        # Subject (with body type + appearance)
        bangs_text = eng(bn_key)
        bangs_part = f", {bangs_text}" if bangs_text else ""
        makeup_part = f", {eng(mu_key)}" if eng(mu_key) else ""
        if attach_subject:
            subject = (f"a photo of the exact same person as in the attached reference photo, "
                       f"preserving their facial identity and features precisely, "
                       f"{eng(bt_key)}, {eng(ap_key)}, "
                       f"with {eng(hr_key)}, {eng(hc_key)}{bangs_part}, "
                       f"and {eng(ex_key)}{makeup_part}")
        elif ns_key == "ns_solo":
            subject = (f"a {eng(ag_key)} {eng(et_key)} {eng(gd_key)}, "
                       f"{eng(bt_key)}, {eng(ap_key)}, "
                       f"with {eng(hr_key)}, {eng(hc_key)}{bangs_part}, "
                       f"and {eng(ex_key)}{makeup_part}")
        elif ns_key in ("ns_duo", "ns_trio"):
            # Distinct per-person descriptions so the AI can tell them apart
            ordinals = ["second", "third"]
            person_descs = [f"the first with {eng(hr_key)}, {eng(hc_key)}{bangs_part}, "
                            f"and {eng(ex_key)}{makeup_part}"]
            for i, (p_hr, p_hc, p_ex) in enumerate(extra_person_keys):
                person_descs.append(f"the {ordinals[i]} with {eng(p_hr)}, "
                                    f"{eng(p_hc)}, and {eng(p_ex)}")
            subject = (f"{eng(ns_key)} {eng(ag_key)} {eng(et_key)} {eng(gd_key)}s, "
                       f"{eng(bt_key)}, {eng(ap_key)}, "
                       + "; ".join(person_descs))
        else:  # group — detail the central person, vary the rest
            subject = (f"{eng(ns_key)} {eng(ag_key)} {eng(et_key)} {eng(gd_key)}s, "
                       f"{eng(bt_key)}, {eng(ap_key)}, "
                       f"each person with a clearly distinct hairstyle, outfit variation and expression, "
                       f"the central person with {eng(hr_key)}, {eng(hc_key)}{bangs_part}, "
                       f"and {eng(ex_key)}{makeup_part}")
        if skin_check:
            subject += ", with ultra-realistic skin texture showing pores and fine details"

        # Outfit (top & bottom each with their own fabric + color).
        # Garments set to "None" are omitted so fashion presets don't clash.
        outfit_parts = []
        for fk in fs_selected_keys:
            v = eng(fk)
            if v:
                outfit_parts.append(v)
        for g_key, fb_key, cp_key in ((top_key, top_fb_key, top_cp_key),
                                      (bot_key, bot_fb_key, bot_cp_key)):
            garment = eng(g_key)
            if not garment:
                continue
            if eng(fb_key):
                garment += f" made of {eng(fb_key)}"
            if eng(cp_key):
                garment += f" in {eng(cp_key)}"
            outfit_parts.append(garment)
        if eng(sh_key):
            outfit_parts.append(eng(sh_key))
        if outfit_text.strip():
            outfit_parts.append(f"wearing {translate_to_english(outfit_text)}")
        if attach_outfit:
            outfit_parts.append("wearing the exact outfit shown in the attached outfit reference image, matching its design, colors and details")
        for ak in acc_selected:
            v = eng(ak)
            if v:
                outfit_parts.append(v)
        outfit = ", ".join(outfit_parts)

        # Pose
        pose = eng(po_key)
        if look_at_camera:
            pose += ", looking directly at the camera with engaging eye contact"

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
        weather_parts = []
        if weather_rain:
            weather_parts.append("with rain falling from the sky")
        if weather_snow:
            weather_parts.append("with snow gently falling")
        if weather_leaves:
            weather_parts.append("with red and golden autumn leaves falling through the air")
        weather_text = ", ".join(weather_parts)
        env_time = eng(td_key)
        env_parts = [env_loc, env_time]
        if season_text:
            env_parts.append(season_text)
        if weather_text:
            env_parts.append(weather_text)
        environment = ", ".join(env_parts)

        # Camera & Lighting + Picture Style + Composition
        camera_parts = [eng(lt_key), eng(sf_key), eng(ca_key), eng(dof_key)]
        cmp_text = eng(cmp_key)
        if cmp_text:
            camera_parts.append(cmp_text)
        ps_text = eng(ps_key)
        if ps_text:
            camera_parts.append(ps_text)
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

    # ── Prompt history ────────────────────────────────────────────────────
    history = st.session_state.get("prompt_history", [])
    if history:
        st.markdown("---")
        with st.expander(f"🕘 {t('history_header')}", expanded=False):
            for item in history:
                st.code(item, language=None)


if __name__ == "__main__":
    main()
