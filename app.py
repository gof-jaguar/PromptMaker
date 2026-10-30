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
        "num_subjects": "Number of People",
        "ns_solo": "Solo (1 person)",
        "ns_duo": "Duo (2 people)",
        "ns_trio": "Trio (3 people)",
        "ns_group": "Group (5 people)",
        "person_2": "Person 2 — distinct look",
        "person_3": "Person 3 — distinct look",
        "multi_person_hint": "💡 Give each person their own gender, hairstyle, hair color and expression below so the AI can tell them apart.",
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
        "attach_outfit_note": "Prompt will instruct AI to recreate the attached outfit (mannequin or flat-lay images work too)",
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
        "loc_brick_ruin": "Old Brick House with Ivy",
        "loc_overgrown": "Overgrown Garden",
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
        "ps_nostalgic": "Warm Nostalgic Film",
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

        # ── v5.5 — "Not specified" options ──
        "age_none": "— Not specified —",
        "eth_none": "— Not specified —",
        "hair_none": "— Not specified —",
        "hc_none": "— Not specified —",
        "expr_none": "— Not specified —",
        "bt_none": "— Not specified —",
        "app_none": "— Not specified —",
        "pose_none": "— None —",
        "tod_none": "— Not specified —",
        "lit_none": "— Not specified —",
        "loc_none": "— Not specified —",
        "sf_none": "— Not specified —",
        "dof_none": "— Not specified —",
        # ── v5.5 — Per-person gender / group mix ──
        "group_mix": "Group Genders",
        "gg_same": "Same as main gender",
        "gg_mixed": "Mixed (men & women)",
        # ── v5.5 — Makeup ──
        "mu_editorial": "Editorial / Avant-garde",
        "mu_freckles": "Faux Freckles",
        "mu_goth": "Goth / Dark",
        "mu_igari": "Igari Blush (Japanese)",
        "mu_bronzed": "Sun-kissed Bronzed",
        "mu_glitter": "Y2K Glitter",
        # ── v5.5 — Expressions ──
        "expr_wink": "Winking",
        "expr_tongue": "Tongue Out (Playful)",
        "expr_mischief": "Mischievous Grin",
        "expr_fierce": "Fierce Gaze",
        "expr_eyes_closed": "Eyes Closed (Serene)",
        "expr_bored": "Bored / Nonchalant",
        "expr_angry": "Angry / Glaring",
        "expr_tearful": "Tearful / Teary Eyes",
        # ── v5.5 — Fashion styles ──
        "fs_basketball": "Basketball / Jersey",
        "fs_beach_cover": "Beachwear / Cover-up",
        "fs_bikini": "Bikini Swimwear",
        "fs_cheer": "Cheerleader",
        "fs_golf": "Golf Wear",
        "fs_one_piece": "One-piece Swimsuit",
        "fs_rashguard": "Rash Guard / Surf",
        "fs_school": "School Uniform",
        "fs_ski": "Ski / Snowboard Wear",
        "fs_teen": "Teen / High-School Style",
        "fs_tennis": "Tennis / Court Style",
        "fs_yoga": "Yoga / Activewear",
        # ── v5.5 — Locations ──
        "loc_arcade": "Arcade / Game Center",
        "loc_ballroom": "Ballroom / Grand Hall",
        "loc_basketball": "Basketball Court",
        "loc_cherry": "Cherry Blossom Park",
        "loc_cliff": "Cliff / Ocean View",
        "loc_convenience": "Convenience Store",
        "loc_greenhouse": "Greenhouse / Botanical",
        "loc_harbor": "Harbor / Marina",
        "loc_ice_rink": "Ice Skating Rink",
        "loc_skatepark": "Skate Park",
        "loc_stadium": "Sports Stadium",
        "loc_supermarket": "Supermarket Aisle",
        "loc_vineyard": "Vineyard",
        "loc_yacht": "Yacht Deck",
        # ── v5.5 — Camera angles ──
        # ── v5.5 — Lighting ──
        "lit_silhouette": "Sunset Silhouette",
        "lit_lowkey": "Low-key (dark & moody)",
        "lit_highkey": "High-key (bright & airy)",
        "lit_lantern": "Paper Lanterns",
        "lit_fireworks": "Fireworks Glow",
        "lit_screen": "Screen / TV Glow",
        "lit_projector": "Projector Patterns",
        "lit_disco": "Disco Ball Sparkle",
        # ── v5.5 — Poses ──
        "pose_boxing": "Boxing Stance",
        "pose_cartwheel": "Cartwheel",
        "pose_dribble": "Dribbling Basketball",
        "pose_finger_frame": "Finger Frame",
        "pose_meditate": "Meditating (Lotus)",
        "pose_ok_sign": "OK Sign",
        "pose_point_camera": "Pointing at Camera",
        "pose_salute": "Playful Salute",
        "pose_selfie": "Selfie (arm extended)",
        "pose_shush": "Shush (finger to lips)",
        "pose_skip": "Skipping",
        "pose_thumbs_up": "Thumbs Up",
        "pose_tiptoe": "Tiptoe Reach",
        "pose_wave": "Waving Hello",
        "pose_yoga": "Yoga Pose",
        "pose_carefree_walk": "Carefree Walk, Arms Swinging",
        "pose_touch_plants": "Crouching, Touching Plants",
        "pose_hold_camera": "Holding a Film Camera",
        "pose_grass_stalk": "Holding a Grass Stalk",
        "pose_ear_wall": "Listening Against a Wall",
        "pose_peek_tree": "Peeking from Behind a Tree",
        "pose_pick_flower": "Picking a Flower",
        "pose_smell_flower": "Smelling a Flower, Eyes Closed",

        # ── Companion / Animal ──
        "companion": "Companion / Animal",
        "pet_none": "— None —",
        "pet_bird": "Bird on Finger",
        "pet_butterflies": "Butterflies Around",
        "pet_cat": "Cat",
        "pet_dog": "Dog",
        "pet_kitten": "Kitten",
        "pet_puppy": "Puppy",
        "pet_rabbit": "Rabbit",

        # ── Quick Themes ──
        "themes_header": "Quick Themes",
        "theme_select": "Theme",
        "apply_theme_btn": "Apply Theme",
        "theme_hint": "Sets a curated look & scene, then generates — your gender, age and identity stay as chosen.",
        "theme_golden_garden": "🌾 Golden Hour Garden",
        "theme_neon_night": "🌃 Neon City Night",
        "theme_cafe_film": "☕ Cozy Café Film",
        "theme_beach": "🏖️ Summer Beach",
        "theme_studio": "🎬 Studio Editorial",
        "theme_cherry": "🌸 Cherry Blossom Spring",

        # ── Photo Set ──
        "photo_set_btn": "Photo Set",
        "photo_set_header": "Photo Set — same look, 6 shots",
        "photo_set_hint": "Same subject, outfit and scene in every shot — only the pose, framing and camera angle change. Generate them all for a matching album.",
        "photo_set_shot": "Shot",
        "photo_set_download": "Download all shots",
        # v5.7 — pose builder + outfit layers
        "exp_pose": "Pose & Body Language",
        "attach_pose_photo": "I will attach a pose reference image (e.g. a mannequin pose sheet)",
        "attach_pose_note": "Prompt will instruct AI to copy only the body pose from the attached image — not its face, body or clothing. The pose pickers below are disabled.",
        "ref_note_pose": "Attach: Pose reference image (mannequin / pose sheet)",
        "pose_category": "Pose Category",
        "pose_detail_header": "Fine-tune the pose",
        "pose_detail_hint": "💡 Optional details layered on top of the pose — leave on “None” if they would contradict it (e.g. hands in pockets + heart hands).",
        "body_dir": "Body Orientation",
        "head_pos": "Head Position",
        "gaze": "Gaze / Eye Direction",
        "hands_pos": "Arms & Hands",
        "legs_pos": "Legs & Stance",
        "pose_energy": "Pose Mood / Energy",
        "pose_text": "Describe the pose in your own words (optional)",
        "pose_text_placeholder": "e.g. sitting on a swing, holding the ropes, legs stretched forward",
        "outfit_mode": "Outfit Type",
        "dress_garment": "Dress / One-piece",
        "dress_fabric": "Dress Fabric",
        "dress_color": "Dress Color",
        "outfit_set": "Outfit Set",
        "outfit_set_hint": "Each set is a complete, coordinated look (layers, legwear, shoes, bag, jewelry). Accessories below are added on top.",
        "outer_layer": "Outer Layer",
        "outer_color": "Outer Layer Color",
        "fit": "Fit / Silhouette",
        "legwear": "Socks & Legwear",
        "details": "Design Details & Prints",
        "details_help": "Pick a few — e.g. ruffles + ribbon bows + lace trim",
        "om_separates": "Top + Bottom",
        "om_dress": "Dress / One-piece",
        "om_set": "Ready-made Outfit Set",
        "pc_all": "All Poses",
        "pc_standing": "Standing",
        "pc_walking": "Walking & Motion",
        "pc_sitting": "Sitting",
        "pc_kneeling": "Kneeling",
        "pc_lying": "Lying Down",
        "pc_crouching": "Crouching & Bending",
        "pc_cute": "Cute Hand Gestures",
        "pc_social": "Social Media & Fashion",
        "pc_props": "Nature & Props",
        "pc_sport": "Sports & Action",
        "pose_contrapposto": "Contrapposto, Weight on One Leg",
        "pose_hands_hips": "Both Hands on Hips",
        "pose_hands_nape": "Hands on Nape of Neck",
        "pose_hand_collar": "Hand at Collarbone",
        "pose_foot_kick": "One Foot Kicked Up Behind",
        "pose_hair_both": "Both Hands Lifting Hair",
        "pose_walk_toward": "Walking Toward Camera",
        "pose_bag_strap": "Walking, Holding Bag Strap",
        "pose_sit_side": "Side-Saddle Sitting",
        "pose_sit_knee_up": "Sitting, One Knee Up",
        "pose_sit_cheek_knee": "Sitting, Cheek on Knees",
        "pose_sit_chair_back": "Sitting Backwards on a Chair",
        "pose_sit_ledge": "Sitting on a Ledge, Legs Dangling",
        "pose_sit_floor_cross": "Sitting Cross-legged on the Floor",
        "pose_sit_hold_ankle": "Sitting, Holding Ankle",
        "pose_wariza_hands": "Wariza, Hands on Floor in Front",
        "pose_seiza": "Seiza (Sitting on Heels)",
        "pose_kneel_upright": "Kneeling Upright, Hands on Thighs",
        "pose_one_knee": "On One Knee",
        "pose_kneel_look_up": "Kneeling, Looking Up",
        "pose_kneel_hair": "Kneeling, Hand in Hair",
        "pose_lie_stomach": "Lying on Stomach, Feet Up",
        "pose_lie_side": "Lying on Side, Head on Hand",
        "pose_lie_back_hair": "Lying on Back, Hair Spread Out",
        "pose_lie_back_knee": "Lying on Back, One Knee Up",
        "pose_lie_arm_pillow": "Lying on Stomach, Head on Arms",
        "pose_crouch_chin": "Crouching, Chin in Hand",
        "pose_crouch_look_back": "Crouching, Looking Back",
        "pose_bend_knees": "Bending Forward, Hands on Knees",
        "pose_bend_shoe": "Bending Down to Fix a Shoe",
        "pose_double_peace": "Double Peace Under Chin",
        "pose_gyaru_peace": "Gyaru Peace (Back of Hand)",
        "pose_fist_cheeks": "Fists on Cheeks (Burikko)",
        "pose_bunny_ears": "Bunny Ears Hands",
        "pose_cat_paw": "Cat Paw Gesture",
        "pose_rawr": "Rawr! Claw Pose",
        "pose_poke_cheek": "Poking Own Cheek",
        "pose_flower_chin": "Flower Pose (Chin on Palms)",
        "pose_sweater_paws": "Sweater Paws Over Mouth",
        "pose_please": "Pleading 'Please' Hands",
        "pose_self_hug": "Shy Self-Hug",
        "pose_big_heart": "Big Heart Above Head",
        "pose_yawn": "Yawning Stretch",
        "pose_coat_lapels": "Holding Coat Lapels",
        "pose_phone_check": "Checking Phone Candidly",
        "pose_skirt_hem": "Holding the Skirt Hem",
        "pose_curtsy": "Curtsy",
        "pose_umbrella": "Holding an Umbrella",
        "pose_bouquet": "Holding a Bouquet",
        "pose_read_book": "Reading a Book",
        "pose_coffee": "Holding a Coffee Cup",
        "pose_bicycle": "Standing with a Bicycle",
        "pose_balloons": "Holding Balloons",
        "pose_ballet": "Ballet Arabesque",
        "pose_tennis_swing": "Tennis Swing",
        "pose_skateboard": "Riding a Skateboard",
        "pose_lunge": "Stretching Lunge",
        "dir_none": "— None —",
        "dir_back": "Back View",
        "dir_back_look": "Back Turned, Looking Back",
        "dir_front": "Facing the Camera",
        "dir_side": "Side Profile",
        "dir_slight": "Slightly Angled",
        "dir_3q": "Three-Quarter Turn",
        "head_none": "— None —",
        "head_chin_down": "Chin Lowered",
        "head_chin_up": "Chin Raised",
        "head_shoulder": "Cheek Toward Shoulder",
        "head_rest_hand": "Resting on Hand",
        "head_back": "Tilted Back",
        "head_tilt": "Tilted to One Side",
        "head_turned": "Turned to the Side",
        "gaze_none": "— None —",
        "gaze_closed": "Eyes Closed",
        "gaze_camera": "Looking at Camera",
        "gaze_down": "Looking Down",
        "gaze_away": "Looking Into the Distance",
        "gaze_upward_glance": "Looking Up at Camera (Upward Glance)",
        "gaze_up": "Looking Upward",
        "gaze_side_glance": "Side Glance at Camera",
        "hands_none": "— None —",
        "hands_crossed": "Arms Crossed",
        "hands_overhead": "Arms Raised Overhead",
        "hands_relaxed": "Arms Relaxed at Sides",
        "hands_both_hips": "Both Hands on Hips",
        "hands_lips": "Finger to Lips",
        "hands_hair": "Hand in Hair",
        "hands_hip": "Hand on Hip",
        "hands_neck": "Hand on Neck / Collarbone",
        "hands_face": "Hand Touching Face",
        "hands_behind": "Hands Clasped Behind Back",
        "hands_clasped": "Hands Clasped in Front",
        "hands_pockets": "Hands in Pockets",
        "hands_strap": "Holding Bag Strap",
        "hands_sleeve": "Tugging a Sleeve",
        "legs_none": "— None —",
        "legs_ankles_crossed": "Ankles Crossed",
        "legs_kick_back": "Foot Kicked Up Behind",
        "legs_knees_in": "Knees Together, Toes In",
        "legs_crossed_knee": "Legs Crossed at the Knee",
        "legs_cross_stand": "Legs Crossed While Standing",
        "legs_extended": "Legs Stretched Out",
        "legs_together": "Legs Together",
        "legs_mid_stride": "Mid-Stride",
        "legs_tiptoe": "On Tiptoe",
        "legs_knee_bent": "One Knee Slightly Bent",
        "legs_wide": "Wide Power Stance",
        "pe_none": "— None —",
        "pe_candid": "Candid, Unposed",
        "pe_confident": "Confident Power Pose",
        "pe_cool": "Cool & Nonchalant",
        "pe_dynamic": "Dynamic, Mid-Motion",
        "pe_elegant": "Elegant & Graceful",
        "pe_playful": "Playful & Energetic",
        "pe_relaxed": "Relaxed & Natural",
        "pe_shy": "Shy & Soft",
        "dress_none": "— None —",
        "dress_babydoll": "Babydoll Dress",
        "dress_ballgown": "Ball Gown",
        "dress_bodycon": "Bodycon Dress",
        "dress_corset": "Corset Dress",
        "dress_jumpsuit": "Jumpsuit",
        "dress_knit": "Knit Dress",
        "dress_maxi": "Maxi Dress",
        "dress_midi": "Midi Dress",
        "dress_mini": "Mini Dress",
        "dress_off_shoulder": "Off-Shoulder Dress",
        "dress_pinafore": "Pinafore Dress",
        "dress_qipao": "Qipao / Cheongsam",
        "dress_romper": "Romper / Playsuit",
        "dress_shirt": "Shirt Dress",
        "dress_slip": "Slip Dress",
        "dress_sundress": "Sundress",
        "dress_tea": "Tea Dress (Vintage)",
        "dress_tiered": "Tiered Ruffle Dress",
        "dress_wrap": "Wrap Dress",
        "out_none": "— None —",
        "out_blazer": "Blazer",
        "out_bolero": "Bolero / Shrug",
        "out_cape": "Cape",
        "out_cardigan": "Cardigan",
        "out_cropped_cardigan": "Cropped Cardigan",
        "out_denim_jacket": "Denim Jacket",
        "out_faux_fur": "Faux Fur Coat",
        "out_kimono": "Kimono-style Cardigan",
        "out_leather": "Leather Jacket",
        "out_wool_coat": "Long Wool Coat",
        "out_open_shirt": "Open Button-up Shirt",
        "out_puffer": "Puffer Jacket",
        "out_shawl": "Shawl over Shoulders",
        "out_trench": "Trench Coat",
        "out_tweed": "Tweed Jacket",
        "out_varsity": "Varsity Jacket",
        "out_zip_hoodie": "Zip-up Hoodie",
        "fit_none": "— Not specified —",
        "fit_aline": "A-Line",
        "fit_body": "Body-Hugging",
        "fit_cropped": "Cropped & High-Waisted",
        "fit_fitted": "Fitted",
        "fit_flowy": "Flowy & Airy",
        "fit_layered": "Layered",
        "fit_oversized": "Oversized",
        "fit_relaxed": "Relaxed Fit",
        "fit_tailored": "Tailored",
        "leg_none": "— None —",
        "leg_ankle": "Ankle Socks",
        "leg_crew": "Crew Socks",
        "leg_fishnet": "Fishnet Tights",
        "leg_frilly": "Frilly Lace-trim Socks",
        "leg_knee": "Knee-high Socks",
        "leg_warmers": "Leg Warmers",
        "leg_loose": "Loose Socks (Japanese)",
        "leg_opaque": "Opaque Black Tights",
        "leg_patterned": "Patterned Tights",
        "leg_sheer_black": "Sheer Black Tights",
        "leg_nude": "Sheer Nude Stockings",
        "leg_thigh": "Thigh-high Socks",
        "leg_white_tights": "White Tights",
        "det_corset": "Corset Lacing",
        "det_embroidery": "Embroidery",
        "det_floral": "Floral Print",
        "det_gingham": "Gingham",
        "det_lace_trim": "Lace Trim",
        "det_off_shoulder": "Off-Shoulder Neckline",
        "det_buttons": "Pearl Buttons",
        "det_collar": "Peter Pan Collar",
        "det_checks": "Plaid / Check Pattern",
        "det_pleats": "Pleats",
        "det_polka": "Polka Dots",
        "det_puff": "Puff Sleeves",
        "det_bows": "Ribbon Bows",
        "det_frills": "Ruffles / Frills",
        "det_sailor": "Sailor Collar",
        "det_sequins": "Sequins / Sparkle",
        "det_sheer_sleeves": "Sheer Sleeves",
        "det_slit": "Side Slit",
        "det_square_neck": "Square Neckline",
        "det_stripes": "Stripes",
        "det_tiered": "Tiered Layers",
        "det_v_neck": "V-Neckline",
        "os_none": "— None —",
        "os_spr_frill_knit": "🌸 Spring · Frill Knit + Denim Mini + Coat",
        "os_spr_floral_cami": "🌸 Spring · Floral Cami + Cardigan + Pleated Skirt",
        "os_spr_floral_midi": "🌸 Spring · Floral Midi Dress + Denim Jacket",
        "os_spr_ribbon_blouse": "🌸 Spring · Ribbon Blouse + Mint Midi Skirt",
        "os_spr_shirt_dress": "🌸 Spring · Ribbon Shirt Dress + Tights",
        "os_spr_lace_cami": "🌸 Spring · Lace Cami + Cardigan + Wide Pants",
        "os_sum_linen": "☀️ Summer · Linen Shirt + Shorts",
        "os_sum_sundress": "☀️ Summer · Eyelet Sundress + Straw Hat",
        "os_sum_crop_denim": "☀️ Summer · Baby Tee + Denim Shorts",
        "os_sum_halter_maxi": "☀️ Summer · Halter Maxi Dress",
        "os_sum_gingham": "☀️ Summer · Gingham Puff Top + White Skirt",
        "os_sum_resort": "☀️ Summer · Resort Shirt + Linen Trousers",
        "os_aut_trench": "🍂 Autumn · Trench + Turtleneck + Jeans",
        "os_aut_corduroy": "🍂 Autumn · Corduroy Pinafore + Knit + Beret",
        "os_aut_plaid": "🍂 Autumn · Plaid Skirt + Chunky Cardigan",
        "os_aut_leather": "🍂 Autumn · Leather Jacket + Satin Slip Skirt",
        "os_aut_knit_dress": "🍂 Autumn · Knit Dress + Suede Boots",
        "os_aut_blazer": "🍂 Autumn · Oversized Blazer + Wide Trousers",
        "os_win_wool_coat": "❄️ Winter · Long Wool Coat + Chunky Scarf",
        "os_win_puffer": "❄️ Winter · Puffer + Hoodie + Beanie",
        "os_win_fur": "❄️ Winter · Faux Fur Coat + Black Knit Dress",
        "os_win_tweed": "❄️ Winter · Tweed Jacket & Skirt Set + Pearls",
        "os_win_overcoat": "❄️ Winter · Turtleneck + Overcoat",
        "os_win_cozy": "❄️ Winter · Cozy Knit + Leg Warmers",
        "os_par_sequin": "✨ Party · Sequin Mini Dress",
        "os_par_satin_gown": "✨ Party · Satin Slip Gown",
        "os_par_tulle": "✨ Party · Tulle Princess Dress",
        "os_par_velvet_suit": "✨ Party · Velvet Suit",
        "os_par_lbd": "✨ Party · Little Black Dress",
        "fab_corduroy": "Corduroy",
        "fab_crochet": "Crochet",
        "fab_jersey": "Jersey",
        "fab_knit": "Fine Knit",
        "fab_organza": "Organza",
        "fab_sequin": "Sequin",
        "fab_tulle": "Tulle",
        "col_butter": "Butter Yellow",
        "col_grey": "Grey",
        "col_ivory": "Ivory",
        # v5.8 — subject details, character lock, camera & scene
        "sub_identity": "Identity",
        "sub_face": "Face Details",
        "sub_hair": "Hair",
        "sub_expression": "Expression, Makeup & Nails",
        "sub_people": "People & Companion",
        "skin_tone": "Skin Tone",
        "face_shape": "Face Shape",
        "eye_shape": "Eye Shape",
        "eye_color": "Eye Color",
        "brows": "Eyebrows",
        "lips": "Lips",
        "face_marks": "Facial Features & Charm Points",
        "face_marks_help": "Pick a few — e.g. mole under eye + aegyo-sal + dimples",
        "facial_hair": "Facial Hair",
        "skin_finish": "Skin Finish",
        "hair_finish": "Hair Finish & Styling",
        "nails": "Nails",
        "char_lock_header": "Character Lock",
        "char_lock_hint": "Lock identity, face, body & hair so every prompt describes the same person — Random Look, themes and presets then only change styling, pose and scene.",
        "char_name": "Character name (optional)",
        "char_name_placeholder": "e.g. Mali",
        "char_lock_btn": "Lock character",
        "char_unlock_btn": "Unlock",
        "char_locked_msg": "is locked — identity, face, body and hair stay fixed.",
        "char_unnamed": "Character",
        "char_download": "Download character (JSON)",
        "char_library": "Saved characters (this session)",
        "char_load_btn": "Load & lock",
        "char_json_hint": "To reuse later, download the JSON and paste it into Advanced → Apply Look.",
        "location_category": "Location Category",
        "atmosphere": "Weather & Atmosphere",
        "atmosphere_help": "Pick any — e.g. after-rain reflections + fog",
        "bg_people": "Background People",
        "sub_lighting": "Lighting",
        "light_dir": "Light Direction",
        "light_color": "Light Color",
        "light_quality": "Light Quality",
        "sub_camera": "Camera",
        "cam_height": "Camera Height",
        "cam_dir": "Camera Position (around subject)",
        "cam_special": "Special Shot / Perspective",
        "cam_hint": "💡 Height = how high the camera is · Position = where it stands around the subject (Body Orientation in the Pose section = where the subject faces) · Framing = how much of the body is shown.",
        "cam_preview": "Camera in prompt:",
        "camera_film": "Camera / Film Stock",
        "lens_fx": "Lens & Film Effects",
        "lens_fx_help": "Pick any — e.g. film grain + light leak",
        "lcat_all": "All Locations",
        "lcat_indoor": "Studio & Indoor",
        "lcat_home": "Home & Bedroom",
        "lcat_city": "City & Street",
        "lcat_shops": "Cafés & Shops",
        "lcat_nature": "Nature & Parks",
        "lcat_water": "Beach & Water",
        "lcat_luxury": "Luxury & Elegant",
        "lcat_travel": "Landmarks & Travel",
        "lcat_thai": "Thailand",
        "lcat_asia": "Japan & Korea",
        "lcat_leisure": "Sports & Leisure",
        "st_none": "— Not specified —",
        "st_porcelain": "Porcelain / Very Fair",
        "st_fair": "Fair",
        "st_light_warm": "Light, Warm Undertone",
        "st_medium": "Medium / Wheatish",
        "st_olive": "Olive",
        "st_tan": "Tan / Sun-kissed",
        "st_brown": "Brown",
        "st_deep": "Deep",
        "fsh_none": "— Not specified —",
        "fsh_heart": "Heart-shaped",
        "fsh_sharp": "High Cheekbones",
        "fsh_oval": "Oval",
        "fsh_round": "Round, Soft Cheeks",
        "fsh_small": "Small Delicate Face",
        "fsh_v": "V-line (Slim Jaw)",
        "eye_none": "— Not specified —",
        "eye_almond": "Almond-shaped",
        "eye_big": "Big Round Eyes",
        "eye_doe": "Doe Eyes",
        "eye_double": "Double Eyelids",
        "eye_monolid": "Monolid",
        "eye_droopy": "Soft Droopy Puppy Eyes",
        "eye_cat": "Upturned Cat Eyes",
        "ec_none": "— Not specified —",
        "ec_amber": "Amber",
        "ec_black": "Black",
        "ec_blue": "Blue",
        "ec_dark_brown": "Dark Brown",
        "ec_green": "Green",
        "ec_grey": "Grey",
        "ec_hazel": "Hazel / Light Brown",
        "brow_none": "— Not specified —",
        "brow_feathery": "Fluffy Feathered",
        "brow_arched": "Softly Arched",
        "brow_straight": "Straight K-Brows",
        "brow_thick": "Thick Natural",
        "brow_thin": "Thin & Defined",
        "lip_none": "— Not specified —",
        "lip_cat": "Cat Lips (Upturned Corners)",
        "lip_full": "Full Lips",
        "lip_heart": "Heart-shaped (Cupid's Bow)",
        "lip_plump": "Plump & Glossy",
        "lip_small": "Small Rosebud Lips",
        "lip_thin": "Thin, Defined Lips",
        "fm_aegyo": "Aegyo-sal (Puffy Under-eyes)",
        "fm_mole_lip": "Beauty Mark Near Lips",
        "fm_dimples": "Dimples",
        "fm_high_nose": "High Nose Bridge",
        "fm_lashes": "Long Natural Lashes",
        "fm_mole_eye": "Mole Under Eye",
        "fm_freckles": "Natural Freckles",
        "fm_rosy": "Naturally Rosy Cheeks",
        "fm_button_nose": "Small Button Nose",
        "fm_snaggle": "Snaggletooth (Yaeba)",
        "fh_none": "— Not specified —",
        "fh_clean": "Clean-shaven",
        "fh_full_beard": "Full Beard",
        "fh_goatee": "Goatee",
        "fh_stubble": "Light Stubble",
        "fh_mustache": "Mustache",
        "fh_short_beard": "Short Beard",
        "skf_none": "— Not specified —",
        "skf_dewy": "Dewy Glow",
        "skf_porcelain": "Flawless Porcelain",
        "skf_glass": "Glass Skin",
        "skf_natural": "Natural, Lightly Textured",
        "skf_matte": "Soft Matte",
        "skf_sunkissed": "Sun-kissed Glow",
        "skf_real": "Ultra-realistic Texture (Pores)",
        "hf_none": "— Not specified —",
        "hf_messy": "Effortlessly Messy",
        "hf_strands": "Face-framing Strands",
        "hf_glossy": "Glossy & Silky",
        "hf_sleek": "Sleek & Polished",
        "hf_tucked": "Tucked Behind Ears",
        "hf_voluminous": "Voluminous",
        "hf_wet": "Wet Look",
        "hf_windswept": "Wind-swept",
        "nl_none": "— Not specified —",
        "nl_black": "Black Nails",
        "nl_chrome": "Chrome / Glazed Donut",
        "nl_red": "Classic Red",
        "nl_natural": "Clean Natural Manicure",
        "nl_french": "French Manicure",
        "nl_glitter": "Glitter",
        "nl_long": "Long Almond, Decorated",
        "nl_nude": "Nude Gel",
        "nl_pastel": "Pastel",
        "ld_none": "— Not specified —",
        "ld_back": "Backlight",
        "ld_butterfly": "Butterfly / Paramount",
        "ld_clamshell": "Clamshell (Beauty)",
        "ld_front": "Front Light",
        "ld_loop": "Loop Light",
        "ld_rembrandt": "Rembrandt (45°)",
        "ld_side": "Side Light",
        "ld_split": "Split Light (Half Face)",
        "ld_top": "Top Light",
        "ld_under": "Under Light (Eerie)",
        "lc_none": "— Not specified —",
        "lc_amber": "Candlelit Amber",
        "lc_cool": "Cool Blue",
        "lc_green": "Green Fluorescent Tint",
        "lc_red": "Moody Red",
        "lc_neutral": "Neutral Daylight",
        "lc_pink_blue": "Pink & Blue Mixed",
        "lc_purple": "Purple & Magenta",
        "lc_teal_orange": "Teal & Orange (Cinematic)",
        "lc_warm": "Warm Golden",
        "lq_none": "— Not specified —",
        "lq_hard": "Hard, Crisp Shadows",
        "lq_high_contrast": "High Contrast",
        "lq_low_contrast": "Low Contrast, Airy",
        "lq_soft": "Soft & Diffused",
        "ch_none": "— Not specified —",
        "ch_aerial": "Aerial / Drone (Very High)",
        "ch_top": "Top-Down (Directly Overhead)",
        "ch_high": "High Angle (Looking Down)",
        "ch_slight_high": "Slightly Above Eye Level (Flattering)",
        "ch_eye": "Eye Level",
        "ch_chest": "Chest Level",
        "ch_waist": "Waist Level",
        "ch_slight_low": "Slightly Below Eye Level",
        "ch_low": "Low Angle (Looking Up)",
        "ch_ground": "Ground Level",
        "ch_worm": "Worm's Eye (Straight Up)",
        "cd_none": "— Not specified —",
        "cd_front": "Front (Straight-on)",
        "cd_front_3q": "Front Three-Quarter (45°)",
        "cd_side": "Side (90° Profile)",
        "cd_back_3q": "Rear Three-Quarter",
        "cd_back": "Directly Behind",
        "cd_over_shoulder": "Over the Shoulder",
        "cs_none": "— None —",
        "cs_telephoto": "Candid Telephoto (Paparazzi)",
        "cs_cctv": "CCTV / Security Camera",
        "cs_dutch": "Dutch Tilt",
        "cs_pov": "First-person POV",
        "cs_fisheye": "Fisheye Lens",
        "cs_mirror": "Mirror Reflection",
        "cs_selfie": "Selfie (Arm's Length)",
        "cs_through": "Shot Through Foreground",
        "cs_window": "Through a Window",
        "cf_none": "— Not specified —",
        "cf_digicam": "2000s Compact Digicam",
        "cf_arri": "ARRI Alexa (Cinema)",
        "cf_canon": "Canon EOS R5 (Clean Digital)",
        "cf_cinestill": "CineStill 800T (Night Film)",
        "cf_disposable": "Disposable Film Camera",
        "cf_superia": "Fujifilm Superia 400 Film",
        "cf_fuji": "Fujifilm X-T5 (Classic Chrome)",
        "cf_hasselblad": "Hasselblad Medium Format",
        "cf_ilford": "Ilford HP5 (B&W Film)",
        "cf_instax": "Instax Mini (Instant)",
        "cf_iphone": "iPhone (Smartphone)",
        "cf_gold": "Kodak Gold 200 Film",
        "cf_portra": "Kodak Portra 400 Film",
        "cf_leica": "Leica M (Rangefinder)",
        "cf_polaroid": "Polaroid Instant Film",
        "cf_sony": "Sony A7R V (Sharp Digital)",
        "atm_puddles": "After-Rain Reflections",
        "atm_leaves": "Autumn Leaves Falling",
        "atm_petals": "Cherry Petals Falling",
        "atm_confetti": "Confetti",
        "atm_dust": "Dust Particles in Light",
        "atm_fireflies": "Fireflies",
        "atm_fog": "Fog / Mist",
        "atm_wind": "Gentle Breeze (Hair Blowing)",
        "atm_sparkles": "Magical Sparkles",
        "atm_rain": "Rain",
        "atm_smoke": "Smoke / Haze",
        "atm_snow": "Snow",
        "atm_bubbles": "Soap Bubbles",
        "atm_steam": "Steam",
        "bgp_none": "— Not specified —",
        "bgp_few": "A Few Passersby",
        "bgp_crowd": "Blurred Bustling Crowd",
        "bgp_empty": "No One Else (Empty)",
        "lfx_chromatic": "Chromatic Aberration",
        "lfx_double": "Double Exposure",
        "lfx_date": "Film Date Stamp",
        "lfx_grain": "Film Grain",
        "lfx_halation": "Halation Glow",
        "lfx_flare": "Lens Flare",
        "lfx_leak": "Light Leak",
        "lfx_motion": "Motion Blur",
        "lfx_prism": "Prism Rainbow",
        "lfx_bloom": "Soft Bloom",
        "lfx_vignette": "Vignette",
        "loc_dance_studio": "Dance Studio",
        "loc_classroom": "Sunlit Classroom",
        "loc_museum": "Museum Hall",
        "loc_bedroom": "Cozy Bedroom",
        "loc_kitchen": "Homey Kitchen",
        "loc_living": "Living Room Sofa",
        "loc_balcony": "Balcony with Plants",
        "loc_window_seat": "Window Seat",
        "loc_vanity": "Vanity Mirror",
        "loc_crosswalk": "City Crosswalk",
        "loc_railway": "Old Railway Tracks",
        "loc_bus_stop": "Bus Stop",
        "loc_flower_shop": "Flower Shop",
        "loc_bookstore": "Bookstore",
        "loc_bakery": "Pastel Bakery",
        "loc_boutique": "Fashion Boutique",
        "loc_record_store": "Vintage Record Store",
        "loc_laundromat": "Retro Laundromat",
        "loc_sunflower": "Sunflower Field",
        "loc_lavender": "Lavender Field",
        "loc_autumn_park": "Autumn Park",
        "loc_meadow": "Wildflower Meadow",
        "loc_lighthouse": "Seaside Lighthouse",
        "loc_mansion": "Classic Mansion Interior",
        "loc_fine_dining": "Fine Dining Restaurant",
        "loc_santorini": "Santorini-style White Village",
        "loc_venice": "Venice-style Canal",
        "loc_th_wat": "Golden Thai Temple",
        "loc_th_floating": "Floating Market",
        "loc_th_chiangmai": "Chiang Mai Old Town Lane",
        "loc_th_shophouse": "Old Shophouse Street",
        "loc_th_island": "Thai Island Beach",
        "loc_th_rooftop": "Bangkok Rooftop Bar",
        "loc_th_tea": "Tea Plantation Hills",
        "loc_th_tuktuk": "Tuk-tuk Street",
        "loc_jp_torii": "Shrine with Torii Gates",
        "loc_jp_street": "Tokyo Side Street",
        "loc_jp_ryokan": "Ryokan Tatami Room",
        "loc_bamboo": "Bamboo Forest",
        "loc_kr_hanok": "Hanok Village",
        "loc_kr_street": "Seoul Neighborhood Street",
        "loc_photo_booth": "Photo Booth",
        "loc_bowling": "Retro Bowling Alley",
        "loc_carousel": "Vintage Carousel",
        "loc_cinema": "Movie Theater",
        "loc_karaoke": "Karaoke Room",
        "loc_tennis": "Tennis Court",
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
        "num_subjects": "จำนวนคน",
        "ns_solo": "เดี่ยว (1 คน)",
        "ns_duo": "คู่ (2 คน)",
        "ns_trio": "3 คน",
        "ns_group": "กลุ่ม (5 คน)",
        "person_2": "คนที่ 2 — ลุคเฉพาะตัว",
        "person_3": "คนที่ 3 — ลุคเฉพาะตัว",
        "multi_person_hint": "💡 เลือกเพศ ทรงผม สีผม และสีหน้าให้แต่ละคนต่างกันด้านล่าง เพื่อให้ AI แยกแต่ละคนออกจากกันได้",
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
        "attach_outfit_note": "พรอมต์จะสั่งให้ AI สร้างชุดตามรูปที่แนบ (ใช้ภาพหุ่นใส่ชุดหรือภาพวางชุดได้)",
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
        "loc_brick_ruin": "บ้านอิฐเก่าเลื้อยไม้เถา",
        "loc_overgrown": "สวนรกครึ้มธรรมชาติ",
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
        "ps_nostalgic": "ฟิล์มโทนอุ่นชวนคิดถึง",
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

        # ── v5.5 — ตัวเลือก "ไม่ระบุ" ──
        "age_none": "— ไม่ระบุ —",
        "eth_none": "— ไม่ระบุ —",
        "hair_none": "— ไม่ระบุ —",
        "hc_none": "— ไม่ระบุ —",
        "expr_none": "— ไม่ระบุ —",
        "bt_none": "— ไม่ระบุ —",
        "app_none": "— ไม่ระบุ —",
        "pose_none": "— ไม่ระบุ —",
        "tod_none": "— ไม่ระบุ —",
        "lit_none": "— ไม่ระบุ —",
        "loc_none": "— ไม่ระบุ —",
        "sf_none": "— ไม่ระบุ —",
        "dof_none": "— ไม่ระบุ —",
        # ── v5.5 — เพศรายคน / กลุ่ม ──
        "group_mix": "เพศของคนในกลุ่ม",
        "gg_same": "เพศเดียวกับที่เลือกด้านบน",
        "gg_mixed": "คละกัน (ชาย-หญิง)",
        # ── v5.5 — เมคอัพ ──
        "mu_editorial": "เมคอัพแฟชั่น / อาว็อง-การ์ด",
        "mu_freckles": "แต้มกระน่ารัก",
        "mu_goth": "โกธิค / สายดาร์ก",
        "mu_igari": "บลัชอิการิ (ญี่ปุ่น)",
        "mu_bronzed": "ผิวแทนโกลว์แดดสวย",
        "mu_glitter": "กลิตเตอร์ Y2K",
        # ── v5.5 — สีหน้า ──
        "expr_wink": "ขยิบตา",
        "expr_tongue": "แลบลิ้นขี้เล่น",
        "expr_mischief": "ยิ้มมีเลศนัย",
        "expr_fierce": "สายตาดุดัน",
        "expr_eyes_closed": "หลับตาสงบ",
        "expr_bored": "เบื่อๆ เฉยชา",
        "expr_angry": "โกรธ / ถลึงตา",
        "expr_tearful": "น้ำตาคลอ",
        # ── v5.5 — สไตล์แฟชั่น ──
        "fs_basketball": "บาสเกตบอล / เสื้อเจอร์ซีย์",
        "fs_beach_cover": "ชุดชายหาด / ผ้าคลุม",
        "fs_bikini": "ชุดว่ายน้ำบิกินี่",
        "fs_cheer": "ชุดเชียร์ลีดเดอร์",
        "fs_golf": "ชุดกอล์ฟ",
        "fs_one_piece": "ชุดว่ายน้ำวันพีซ",
        "fs_rashguard": "แรชการ์ด / ชุดเซิร์ฟ",
        "fs_school": "ชุดนักเรียน",
        "fs_ski": "ชุดสกี / สโนว์บอร์ด",
        "fs_teen": "แฟชั่นวัยรุ่น / วัยเรียน",
        "fs_tennis": "ชุดเทนนิส",
        "fs_yoga": "ชุดโยคะ / ออกกำลังกาย",
        # ── v5.5 — สถานที่ ──
        "loc_arcade": "ร้านเกมอาร์เคด",
        "loc_ballroom": "ห้องบอลรูมหรูหรา",
        "loc_basketball": "สนามบาสเกตบอล",
        "loc_cherry": "สวนซากุระบานสะพรั่ง",
        "loc_cliff": "หน้าผาริมทะเล",
        "loc_convenience": "ร้านสะดวกซื้อ",
        "loc_greenhouse": "เรือนกระจก / สวนพฤกษศาสตร์",
        "loc_harbor": "ท่าเรือ / มารีน่า",
        "loc_ice_rink": "ลานสเก็ตน้ำแข็ง",
        "loc_skatepark": "ลานสเก็ตบอร์ด",
        "loc_stadium": "สนามกีฬาสเตเดียม",
        "loc_supermarket": "ซูเปอร์มาร์เก็ต",
        "loc_vineyard": "ไร่องุ่น",
        "loc_yacht": "ดาดฟ้าเรือยอชท์",
        # ── v5.5 — มุมกล้อง ──
        # ── v5.5 — สไตล์แสง ──
        "lit_silhouette": "เงาดำย้อนแสงอาทิตย์ตก",
        "lit_lowkey": "โลว์คีย์ (มืดขรึม)",
        "lit_highkey": "ไฮคีย์ (สว่างโปร่ง)",
        "lit_lantern": "แสงโคมกระดาษ",
        "lit_fireworks": "แสงพลุ / ดอกไม้ไฟ",
        "lit_screen": "แสงจากหน้าจอ / ทีวี",
        "lit_projector": "แสงโปรเจกเตอร์",
        "lit_disco": "แสงดิสโก้บอล",
        # ── v5.5 — ท่าโพส ──
        "pose_boxing": "ท่าชกมวย",
        "pose_cartwheel": "ตีลังกาล้อเกวียน",
        "pose_dribble": "เลี้ยงลูกบาส",
        "pose_finger_frame": "ทำกรอบรูปด้วยนิ้ว",
        "pose_meditate": "นั่งสมาธิ",
        "pose_ok_sign": "ทำมือโอเค",
        "pose_point_camera": "ชี้มาที่กล้อง",
        "pose_salute": "วันทยหัตถ์เล่นๆ",
        "pose_selfie": "เซลฟี่ (ยื่นแขนถ่าย)",
        "pose_shush": "ทำท่าจุ๊ๆ (นิ้วแตะปาก)",
        "pose_skip": "ก้าวกระโดดร่าเริง",
        "pose_thumbs_up": "ยกนิ้วโป้ง",
        "pose_tiptoe": "เขย่งเท้าเอื้อมมือ",
        "pose_wave": "โบกมือทักทาย",
        "pose_yoga": "ท่าโยคะ",
        "pose_carefree_walk": "เดินชิลแกว่งแขนสบายๆ",
        "pose_touch_plants": "นั่งยองแตะใบไม้ใบหญ้า",
        "pose_hold_camera": "ถือกล้องฟิล์มมองไปไกลๆ",
        "pose_grass_stalk": "ถือดอกหญ้าข้างแก้ม",
        "pose_ear_wall": "แนบหูฟังกำแพงเก่า",
        "pose_peek_tree": "แอบมองจากหลังต้นไม้",
        "pose_pick_flower": "เอื้อมเด็ดดอกไม้เล็กๆ",
        "pose_smell_flower": "ดมดอกไม้หลับตายิ้ม",

        # ── Companion / Animal ──
        "companion": "เพื่อนร่วมเฟรม (สัตว์)",
        "pet_none": "— ไม่มี —",
        "pet_bird": "นกเกาะบนนิ้ว",
        "pet_butterflies": "ผีเสื้อบินรอบตัว",
        "pet_cat": "แมว",
        "pet_dog": "สุนัข",
        "pet_kitten": "ลูกแมว",
        "pet_puppy": "ลูกสุนัข",
        "pet_rabbit": "กระต่าย",

        # ── Quick Themes ──
        "themes_header": "ธีมสำเร็จรูป",
        "theme_select": "เลือกธีม",
        "apply_theme_btn": "ใช้ธีมนี้",
        "theme_hint": "ตั้งค่าลุคและฉากที่จัดชุดไว้ให้ แล้วสร้างพรอมต์ทันที — เพศ อายุ และตัวตนที่เลือกไว้ไม่เปลี่ยน",
        "theme_golden_garden": "🌾 สวนแดดทองยามเย็น",
        "theme_neon_night": "🌃 เมืองนีออนยามค่ำคืน",
        "theme_cafe_film": "☕ คาเฟ่อบอุ่นโทนฟิล์ม",
        "theme_beach": "🏖️ ชายหาดหน้าร้อน",
        "theme_studio": "🎬 สตูดิโอแฟชั่น",
        "theme_cherry": "🌸 ซากุระฤดูใบไม้ผลิ",

        # ── Photo Set ──
        "photo_set_btn": "ชุดภาพถ่าย",
        "photo_set_header": "ชุดภาพถ่าย — ลุคเดิม 6 ช็อต",
        "photo_set_hint": "ตัวแบบ ชุด และฉากเหมือนกันทุกช็อต — เปลี่ยนเฉพาะท่าโพส ระยะภาพ และมุมกล้อง นำไปสร้างภาพเป็นอัลบั้มชุดเดียวกันได้เลย",
        "photo_set_shot": "ช็อตที่",
        "photo_set_download": "ดาวน์โหลดทุกช็อต",
        # v5.7 — pose builder + outfit layers
        "exp_pose": "ท่าโพสและภาษากาย",
        "attach_pose_photo": "จะแนบรูปท่าโพสอ้างอิง (เช่น ภาพหุ่นท่าโพส)",
        "attach_pose_note": "พรอมต์จะสั่งให้ AI เลียนแบบเฉพาะท่าทางจากรูปที่แนบ ไม่เอาหน้าตา รูปร่าง หรือเสื้อผ้า (ตัวเลือกท่าด้านล่างจะถูกปิดไว้)",
        "ref_note_pose": "แนบ: รูปท่าโพสอ้างอิง (หุ่น / ภาพท่าโพส)",
        "pose_category": "หมวดท่าโพส",
        "pose_detail_header": "ปรับรายละเอียดท่า",
        "pose_detail_hint": "💡 รายละเอียดเสริมที่ต่อท้ายท่าหลัก ปล่อยเป็น “ไม่ระบุ” ถ้าขัดกับท่าที่เลือก (เช่น มือล้วงกระเป๋า + ทำมือหัวใจ)",
        "body_dir": "ทิศทางลำตัว",
        "head_pos": "ตำแหน่งศีรษะ",
        "gaze": "ทิศทางสายตา",
        "hands_pos": "แขนและมือ",
        "legs_pos": "ขาและการยืน",
        "pose_energy": "อารมณ์ของท่าทาง",
        "pose_text": "อธิบายท่าโพสเอง (ไม่บังคับ)",
        "pose_text_placeholder": "เช่น นั่งชิงช้า มือจับเชือก เหยียดขาไปข้างหน้า",
        "outfit_mode": "รูปแบบชุด",
        "dress_garment": "เดรส / ชุดชิ้นเดียว",
        "dress_fabric": "เนื้อผ้าเดรส",
        "dress_color": "สีเดรส",
        "outfit_set": "ชุดสำเร็จรูป",
        "outfit_set_hint": "แต่ละชุดจัดมาครบแล้ว (เสื้อซ้อน ถุงเท้า รองเท้า กระเป๋า เครื่องประดับ) เครื่องประดับที่ติ๊กด้านล่างจะถูกเพิ่มเข้าไปอีก",
        "outer_layer": "เสื้อคลุมชั้นนอก",
        "outer_color": "สีเสื้อคลุม",
        "fit": "ทรงชุด",
        "legwear": "ถุงเท้าและถุงน่อง",
        "details": "ดีเทลและลวดลาย",
        "details_help": "เลือกได้หลายอย่าง เช่น ระบาย + โบว์ + ขอบลูกไม้",
        "om_separates": "เสื้อ + ท่อนล่าง",
        "om_dress": "เดรส / ชุดชิ้นเดียว",
        "om_set": "ชุดสำเร็จรูปตามฤดู",
        "pc_all": "ทุกท่า",
        "pc_standing": "ยืน",
        "pc_walking": "เดินและเคลื่อนไหว",
        "pc_sitting": "นั่ง",
        "pc_kneeling": "คุกเข่า",
        "pc_lying": "นอน",
        "pc_crouching": "นั่งยองและก้มตัว",
        "pc_cute": "ท่ามือน่ารัก",
        "pc_social": "โซเชียลและแฟชั่น",
        "pc_props": "ธรรมชาติและพร็อพ",
        "pc_sport": "กีฬาและแอคชั่น",
        "pose_contrapposto": "ยืนลงน้ำหนักขาเดียว",
        "pose_hands_hips": "เท้าเอวสองข้าง",
        "pose_hands_nape": "มือแตะต้นคอสองข้าง",
        "pose_hand_collar": "มือแตะไหปลาร้า",
        "pose_foot_kick": "ยกเท้าไปด้านหลังข้างเดียว",
        "pose_hair_both": "ยกผมขึ้นด้วยสองมือ",
        "pose_walk_toward": "เดินเข้าหากล้อง",
        "pose_bag_strap": "เดินจับสายกระเป๋า",
        "pose_sit_side": "นั่งพับเพียบ",
        "pose_sit_knee_up": "นั่งชันเข่าข้างเดียว",
        "pose_sit_cheek_knee": "นั่งชันเข่าเอาแก้มพิง",
        "pose_sit_chair_back": "นั่งคร่อมเก้าอี้กลับด้าน",
        "pose_sit_ledge": "นั่งบนขอบ ห้อยขา",
        "pose_sit_floor_cross": "นั่งขัดสมาธิสบายๆ",
        "pose_sit_hold_ankle": "นั่งเอามือจับข้อเท้า",
        "pose_wariza_hands": "นั่งพับขาแบบญี่ปุ่น มือวางด้านหน้า",
        "pose_seiza": "นั่งคุกเข่าทับส้นเท้า (เซซะ)",
        "pose_kneel_upright": "คุกเข่าตัวตรง มือวางบนต้นขา",
        "pose_one_knee": "คุกเข่าข้างเดียว",
        "pose_kneel_look_up": "คุกเข่าแหงนมอง",
        "pose_kneel_hair": "คุกเข่า มือแตะผม",
        "pose_lie_stomach": "นอนคว่ำ ยกเท้าขึ้น",
        "pose_lie_side": "นอนตะแคง มือยันศีรษะ",
        "pose_lie_back_hair": "นอนหงาย ผมสยาย",
        "pose_lie_back_knee": "นอนหงายชันเข่า",
        "pose_lie_arm_pillow": "นอนคว่ำหนุนแขน",
        "pose_crouch_chin": "นั่งยองเท้าคาง",
        "pose_crouch_look_back": "นั่งยองหันกลับมามอง",
        "pose_bend_knees": "โน้มตัว มือวางบนเข่า",
        "pose_bend_shoe": "ก้มลงจัดรองเท้า",
        "pose_double_peace": "ชูสองนิ้วสองมือใต้คาง",
        "pose_gyaru_peace": "ชูสองนิ้วกลับด้านแบบกยารุ",
        "pose_fist_cheeks": "กำมือแนบแก้ม (บุริกโกะ)",
        "pose_bunny_ears": "ทำมือหูกระต่าย",
        "pose_cat_paw": "ทำมือแมวกวัก",
        "pose_rawr": "ท่าเสือคำราม (กาโอ้)",
        "pose_poke_cheek": "จิ้มแก้มตัวเอง",
        "pose_flower_chin": "เท้าคางด้วยสองฝ่ามือ (ท่าดอกไม้)",
        "pose_sweater_paws": "แขนเสื้อยาวปิดปาก",
        "pose_please": "พนมมือขอร้องน่ารัก",
        "pose_self_hug": "กอดตัวเองเขินๆ",
        "pose_big_heart": "ทำหัวใจใหญ่เหนือหัว",
        "pose_yawn": "หาวพร้อมบิดขี้เกียจ",
        "pose_coat_lapels": "จับปกเสื้อโค้ทสองข้าง",
        "pose_phone_check": "ก้มดูมือถือแบบแคนดิด",
        "pose_skirt_hem": "จับชายกระโปรง",
        "pose_curtsy": "ถอนสายบัว",
        "pose_umbrella": "ถือร่ม",
        "pose_bouquet": "ถือช่อดอกไม้",
        "pose_read_book": "อ่านหนังสือ",
        "pose_coffee": "ถือแก้วกาแฟสองมือ",
        "pose_bicycle": "ยืนจูงจักรยาน",
        "pose_balloons": "ถือลูกโป่ง",
        "pose_ballet": "ท่าบัลเล่ต์อาราเบสก์",
        "pose_tennis_swing": "ตีเทนนิส",
        "pose_skateboard": "เล่นสเก็ตบอร์ด",
        "pose_lunge": "ยืดเหยียดท่าลันจ์",
        "dir_none": "— ไม่ระบุ —",
        "dir_back": "หันหลังทั้งตัว",
        "dir_back_look": "หันหลังแล้วเหลียวมอง",
        "dir_front": "หันหน้าเข้ากล้อง",
        "dir_side": "หันข้าง",
        "dir_slight": "เฉียงเล็กน้อย",
        "dir_3q": "หันเฉียง 3/4",
        "head_none": "— ไม่ระบุ —",
        "head_chin_down": "ก้มคางเล็กน้อย",
        "head_chin_up": "เชิดคาง",
        "head_shoulder": "ซบแก้มเข้าหาไหล่",
        "head_rest_hand": "ศีรษะพิงมือ",
        "head_back": "เงยศีรษะไปด้านหลัง",
        "head_tilt": "เอียงศีรษะ",
        "head_turned": "หันศีรษะไปด้านข้าง",
        "gaze_none": "— ไม่ระบุ —",
        "gaze_closed": "หลับตา",
        "gaze_camera": "มองกล้อง",
        "gaze_down": "มองลงต่ำ",
        "gaze_away": "มองไปไกลๆ",
        "gaze_upward_glance": "ช้อนตามองกล้อง",
        "gaze_up": "มองขึ้นด้านบน",
        "gaze_side_glance": "ชำเลืองมองกล้อง",
        "hands_none": "— ไม่ระบุ —",
        "hands_crossed": "กอดอก",
        "hands_overhead": "ยกแขนเหนือศีรษะ",
        "hands_relaxed": "ปล่อยแขนสบายๆ",
        "hands_both_hips": "เท้าเอวสองข้าง",
        "hands_lips": "นิ้วแตะริมฝีปาก",
        "hands_hair": "มือแตะผม",
        "hands_hip": "มือเท้าเอว",
        "hands_neck": "มือแตะคอ / ไหปลาร้า",
        "hands_face": "มือแตะใบหน้า",
        "hands_behind": "ไขว้มือไว้ด้านหลัง",
        "hands_clasped": "ประสานมือด้านหน้า",
        "hands_pockets": "มือล้วงกระเป๋า",
        "hands_strap": "จับสายกระเป๋า",
        "hands_sleeve": "ดึงแขนเสื้อ",
        "legs_none": "— ไม่ระบุ —",
        "legs_ankles_crossed": "ไขว้ข้อเท้า",
        "legs_kick_back": "ยกเท้าไปด้านหลัง",
        "legs_knees_in": "เข่าชิด ปลายเท้าเข้า",
        "legs_crossed_knee": "ไขว่ห้าง",
        "legs_cross_stand": "ยืนไขว้ขา",
        "legs_extended": "เหยียดขาออก",
        "legs_together": "ขาชิด",
        "legs_mid_stride": "กำลังก้าวเดิน",
        "legs_tiptoe": "เขย่งปลายเท้า",
        "legs_knee_bent": "งอเข่าข้างเดียวเล็กน้อย",
        "legs_wide": "ยืนกางขามั่นใจ",
        "pe_none": "— ไม่ระบุ —",
        "pe_candid": "แคนดิด ไม่จัดท่า",
        "pe_confident": "มั่นใจ ทรงพลัง",
        "pe_cool": "เท่ นิ่งๆ",
        "pe_dynamic": "ไดนามิก กำลังเคลื่อนไหว",
        "pe_elegant": "สง่างาม อ่อนช้อย",
        "pe_playful": "ขี้เล่น สดใส",
        "pe_relaxed": "ผ่อนคลาย เป็นธรรมชาติ",
        "pe_shy": "เขินอาย อ่อนโยน",
        "dress_none": "— ไม่ระบุ —",
        "dress_babydoll": "เดรสเบบี้ดอลล์",
        "dress_ballgown": "ชุดราตรีบอลกาวน์",
        "dress_bodycon": "เดรสรัดรูป",
        "dress_corset": "เดรสคอร์เซ็ต",
        "dress_jumpsuit": "จัมพ์สูท",
        "dress_knit": "เดรสไหมพรม",
        "dress_maxi": "เดรสยาว (แม็กซี่)",
        "dress_midi": "เดรสยาวคลุมเข่า (มิดี้)",
        "dress_mini": "มินิเดรส",
        "dress_off_shoulder": "เดรสเปิดไหล่",
        "dress_pinafore": "เดรสเอี๊ยม",
        "dress_qipao": "กี่เพ้า",
        "dress_romper": "รอมเปอร์ / จั๊มสูทขาสั้น",
        "dress_shirt": "เชิ้ตเดรส",
        "dress_slip": "สลิปเดรส",
        "dress_sundress": "เดรสฤดูร้อน (ซันเดรส)",
        "dress_tea": "เดรสวินเทจ (ทีเดรส)",
        "dress_tiered": "เดรสระบายชั้น",
        "dress_wrap": "เดรสป้าย",
        "out_none": "— ไม่ระบุ —",
        "out_blazer": "เบลเซอร์",
        "out_bolero": "โบเลโร่ (เสื้อคลุมสั้น)",
        "out_cape": "เสื้อคลุมเคป",
        "out_cardigan": "คาร์ดิแกน",
        "out_cropped_cardigan": "คาร์ดิแกนครอป",
        "out_denim_jacket": "แจ็คเก็ตยีนส์",
        "out_faux_fur": "โค้ทขนเฟอร์เทียม",
        "out_kimono": "เสื้อคลุมทรงกิโมโน",
        "out_leather": "แจ็คเก็ตหนัง",
        "out_wool_coat": "โค้ทขนสัตว์ตัวยาว",
        "out_open_shirt": "เชิ้ตปลดกระดุมคลุม",
        "out_puffer": "แจ็คเก็ตบุนวม",
        "out_shawl": "ผ้าคลุมไหล่",
        "out_trench": "เทรนช์โค้ท",
        "out_tweed": "แจ็คเก็ตผ้าทวีด",
        "out_varsity": "แจ็คเก็ตวาร์ซิตี้",
        "out_zip_hoodie": "ฮู้ดดี้ซิป",
        "fit_none": "— ไม่ระบุ —",
        "fit_aline": "ทรงเอ",
        "fit_body": "รัดรูป",
        "fit_cropped": "ครอปเอวสูง",
        "fit_fitted": "พอดีตัว",
        "fit_flowy": "พลิ้วไหว",
        "fit_layered": "เลเยอร์ซ้อนชั้น",
        "fit_oversized": "โอเวอร์ไซซ์",
        "fit_relaxed": "ทรงหลวมสบาย",
        "fit_tailored": "ทรงตัดเย็บเข้ารูป",
        "leg_none": "— ไม่ระบุ —",
        "leg_ankle": "ถุงเท้าข้อสั้น",
        "leg_crew": "ถุงเท้าข้อกลาง",
        "leg_fishnet": "ถุงน่องตาข่าย",
        "leg_frilly": "ถุงเท้าระบายลูกไม้",
        "leg_knee": "ถุงเท้ายาวถึงเข่า",
        "leg_warmers": "ปลอกขาไหมพรม",
        "leg_loose": "ถุงเท้าย้วย (สไตล์ญี่ปุ่น)",
        "leg_opaque": "ถุงน่องดำทึบ",
        "leg_patterned": "ถุงน่องลวดลาย",
        "leg_sheer_black": "ถุงน่องดำแบบบาง",
        "leg_nude": "ถุงน่องสีเนื้อ",
        "leg_thigh": "ถุงเท้ายาวเหนือเข่า",
        "leg_white_tights": "ถุงน่องสีขาว",
        "det_corset": "เชือกผูกแบบคอร์เซ็ต",
        "det_embroidery": "งานปัก",
        "det_floral": "ลายดอกไม้",
        "det_gingham": "ลายตารางกิงแฮม",
        "det_lace_trim": "ขอบลูกไม้",
        "det_off_shoulder": "คอปาดเปิดไหล่",
        "det_buttons": "กระดุมมุก",
        "det_collar": "ปกบัว",
        "det_checks": "ลายสก็อต",
        "det_pleats": "จีบพลีท",
        "det_polka": "ลายจุด",
        "det_puff": "แขนตุ๊กตา",
        "det_bows": "โบว์ริบบิ้น",
        "det_frills": "ระบาย",
        "det_sailor": "ปกกะลาสี",
        "det_sequins": "เลื่อม / วิบวับ",
        "det_sheer_sleeves": "แขนผ้าโปร่ง",
        "det_slit": "ผ่าข้าง",
        "det_square_neck": "คอเหลี่ยม",
        "det_stripes": "ลายทาง",
        "det_tiered": "ระบายเป็นชั้น",
        "det_v_neck": "คอวี",
        "os_none": "— ไม่ระบุ —",
        "os_spr_frill_knit": "🌸 ใบไม้ผลิ · ไหมพรมระบาย + มินิสเกิร์ตยีนส์ + โค้ท",
        "os_spr_floral_cami": "🌸 ใบไม้ผลิ · สายเดี่ยวลายดอก + คาร์ดิแกน + กระโปรงพลีท",
        "os_spr_floral_midi": "🌸 ใบไม้ผลิ · เดรสมิดี้ลายดอก + แจ็คเก็ตยีนส์",
        "os_spr_ribbon_blouse": "🌸 ใบไม้ผลิ · เบลาส์ผูกโบว์ + กระโปรงมิดี้สีมิ้นต์",
        "os_spr_shirt_dress": "🌸 ใบไม้ผลิ · เชิ้ตเดรสผูกโบว์ + ถุงน่อง",
        "os_spr_lace_cami": "🌸 ใบไม้ผลิ · สายเดี่ยวลูกไม้ + คาร์ดิแกน + กางเกงขากว้าง",
        "os_sum_linen": "☀️ ฤดูร้อน · เชิ้ตลินิน + กางเกงขาสั้น",
        "os_sum_sundress": "☀️ ฤดูร้อน · เดรสผ้าฉลุ + หมวกสาน",
        "os_sum_crop_denim": "☀️ ฤดูร้อน · เสื้อครอปเบบี้ที + ยีนส์ขาสั้น",
        "os_sum_halter_maxi": "☀️ ฤดูร้อน · เดรสยาวคล้องคอ",
        "os_sum_gingham": "☀️ ฤดูร้อน · เสื้อแขนตุ๊กตาลายกิงแฮม + กระโปรงขาว",
        "os_sum_resort": "☀️ ฤดูร้อน · เชิ้ตรีสอร์ท + กางเกงลินิน",
        "os_aut_trench": "🍂 ใบไม้ร่วง · เทรนช์โค้ท + คอเต่า + ยีนส์",
        "os_aut_corduroy": "🍂 ใบไม้ร่วง · เอี๊ยมลูกฟูก + ไหมพรม + หมวกเบเร่ต์",
        "os_aut_plaid": "🍂 ใบไม้ร่วง · กระโปรงลายสก็อต + คาร์ดิแกนหนา",
        "os_aut_leather": "🍂 ใบไม้ร่วง · แจ็คเก็ตหนัง + กระโปรงซาติน",
        "os_aut_knit_dress": "🍂 ใบไม้ร่วง · เดรสไหมพรม + บู๊ตหนังกลับ",
        "os_aut_blazer": "🍂 ใบไม้ร่วง · เบลเซอร์โอเวอร์ไซซ์ + กางเกงขากว้าง",
        "os_win_wool_coat": "❄️ ฤดูหนาว · โค้ทยาว + ผ้าพันคอหนา",
        "os_win_puffer": "❄️ ฤดูหนาว · แจ็คเก็ตบุนวม + ฮู้ดดี้ + หมวกไหมพรม",
        "os_win_fur": "❄️ ฤดูหนาว · โค้ทเฟอร์ + เดรสไหมพรมดำ",
        "os_win_tweed": "❄️ ฤดูหนาว · เซ็ตทวีด + สร้อยมุก",
        "os_win_overcoat": "❄️ ฤดูหนาว · คอเต่า + โอเวอร์โค้ท",
        "os_win_cozy": "❄️ ฤดูหนาว · ไหมพรมอุ่นๆ + ปลอกขา",
        "os_par_sequin": "✨ ปาร์ตี้ · มินิเดรสเลื่อม",
        "os_par_satin_gown": "✨ ปาร์ตี้ · ชุดราตรีซาตินทรงสลิป",
        "os_par_tulle": "✨ ปาร์ตี้ · เดรสเจ้าหญิงผ้าทูล",
        "os_par_velvet_suit": "✨ ปาร์ตี้ · สูทกำมะหยี่",
        "os_par_lbd": "✨ ปาร์ตี้ · เดรสดำตัวเล็ก (LBD)",
        "fab_corduroy": "ผ้าลูกฟูก",
        "fab_crochet": "ผ้าถักโครเชต์",
        "fab_jersey": "ผ้ายืดเจอร์ซีย์",
        "fab_knit": "ผ้าไหมพรมเนื้อละเอียด",
        "fab_organza": "ผ้าแก้ว (ออร์แกนซ่า)",
        "fab_sequin": "ผ้าเลื่อม",
        "fab_tulle": "ผ้าทูล",
        "col_butter": "เหลืองบัตเตอร์",
        "col_grey": "เทา",
        "col_ivory": "สีงาช้าง",
        # v5.8 — subject details, character lock, camera & scene
        "sub_identity": "ตัวตน",
        "sub_face": "รายละเอียดใบหน้า",
        "sub_hair": "ผม",
        "sub_expression": "สีหน้า เมคอัพ และเล็บ",
        "sub_people": "จำนวนคนและสัตว์เลี้ยง",
        "skin_tone": "โทนสีผิว",
        "face_shape": "รูปหน้า",
        "eye_shape": "รูปตา",
        "eye_color": "สีตา",
        "brows": "คิ้ว",
        "lips": "ริมฝีปาก",
        "face_marks": "จุดเด่นบนใบหน้า",
        "face_marks_help": "เลือกได้หลายอย่าง เช่น ไฝใต้ตา + ถุงใต้ตาน่ารัก + ลักยิ้ม",
        "facial_hair": "หนวดเครา",
        "skin_finish": "ลักษณะผิว",
        "hair_finish": "ลักษณะเส้นผม",
        "nails": "เล็บ",
        "char_lock_header": "ล็อกตัวละคร",
        "char_lock_hint": "ล็อกตัวตน ใบหน้า รูปร่าง และผม ให้ทุกพรอมต์เป็นคนเดิม ปุ่มสุ่มลุค ธีม และพรีเซ็ตจะเปลี่ยนแค่การแต่งตัว ท่าโพส และฉาก",
        "char_name": "ชื่อตัวละคร (ไม่บังคับ)",
        "char_name_placeholder": "เช่น มะลิ",
        "char_lock_btn": "ล็อกตัวละคร",
        "char_unlock_btn": "ปลดล็อก",
        "char_locked_msg": "ถูกล็อกแล้ว ตัวตน ใบหน้า รูปร่าง และผมจะคงเดิม",
        "char_unnamed": "ตัวละคร",
        "char_download": "ดาวน์โหลดตัวละคร (JSON)",
        "char_library": "ตัวละครที่บันทึกไว้ (เซสชันนี้)",
        "char_load_btn": "โหลดและล็อก",
        "char_json_hint": "ถ้าจะใช้ภายหลัง ให้ดาวน์โหลด JSON แล้ววางในส่วนขั้นสูง → ใช้ลุคนี้",
        "location_category": "หมวดสถานที่",
        "atmosphere": "สภาพอากาศและบรรยากาศ",
        "atmosphere_help": "เลือกได้หลายอย่าง เช่น แอ่งน้ำหลังฝน + หมอก",
        "bg_people": "ผู้คนในฉากหลัง",
        "sub_lighting": "แสง",
        "light_dir": "ทิศทางแสง",
        "light_color": "สีของแสง",
        "light_quality": "คุณภาพแสง",
        "sub_camera": "กล้อง",
        "cam_height": "ระดับความสูงกล้อง",
        "cam_dir": "ตำแหน่งกล้อง (รอบตัวแบบ)",
        "cam_special": "มุมพิเศษ / เปอร์สเปกทีฟ",
        "cam_hint": "💡 ความสูง = กล้องอยู่สูงหรือต่ำ · ตำแหน่ง = กล้องยืนตรงไหนรอบตัวแบบ (ส่วน “ทิศทางลำตัว” ในท่าโพส = แบบหันไปทางไหน) · ระยะภาพ = เห็นตัวแบบมากแค่ไหน",
        "cam_preview": "กล้องในพรอมต์:",
        "camera_film": "กล้อง / ฟิล์ม",
        "lens_fx": "เอฟเฟกต์เลนส์และฟิล์ม",
        "lens_fx_help": "เลือกได้หลายอย่าง เช่น เกรนฟิล์ม + แสงรั่ว",
        "lcat_all": "ทุกสถานที่",
        "lcat_indoor": "สตูดิโอและในอาคาร",
        "lcat_home": "ในบ้านและห้องนอน",
        "lcat_city": "เมืองและถนน",
        "lcat_shops": "คาเฟ่และร้านค้า",
        "lcat_nature": "ธรรมชาติและสวน",
        "lcat_water": "ทะเลและแหล่งน้ำ",
        "lcat_luxury": "หรูหราและสง่างาม",
        "lcat_travel": "สถานที่ท่องเที่ยว",
        "lcat_thai": "ประเทศไทย",
        "lcat_asia": "ญี่ปุ่นและเกาหลี",
        "lcat_leisure": "กีฬาและสันทนาการ",
        "st_none": "— ไม่ระบุ —",
        "st_porcelain": "ขาวมาก (พอร์ซเลน)",
        "st_fair": "ผิวขาว",
        "st_light_warm": "ขาวเหลือง",
        "st_medium": "ผิวสองสี",
        "st_olive": "ผิวมะกอก (โอลีฟ)",
        "st_tan": "ผิวแทน",
        "st_brown": "ผิวน้ำตาล",
        "st_deep": "ผิวเข้ม",
        "fsh_none": "— ไม่ระบุ —",
        "fsh_heart": "หน้ารูปหัวใจ",
        "fsh_sharp": "โหนกแก้มสูง",
        "fsh_oval": "หน้ารูปไข่",
        "fsh_round": "หน้ากลม แก้มนุ่ม",
        "fsh_small": "หน้าเล็ก",
        "fsh_v": "หน้าวีเชฟ (คางเรียว)",
        "eye_none": "— ไม่ระบุ —",
        "eye_almond": "ตาอัลมอนด์",
        "eye_big": "ตาโตกลม",
        "eye_doe": "ตากวาง (ตาหวานโต)",
        "eye_double": "ตาสองชั้น",
        "eye_monolid": "ตาชั้นเดียว",
        "eye_droopy": "ตาตก (ตาลูกหมา)",
        "eye_cat": "ตาแมว (หางตาชี้ขึ้น)",
        "ec_none": "— ไม่ระบุ —",
        "ec_amber": "สีอำพัน",
        "ec_black": "สีดำ",
        "ec_blue": "สีฟ้า",
        "ec_dark_brown": "น้ำตาลเข้ม",
        "ec_green": "สีเขียว",
        "ec_grey": "สีเทา",
        "ec_hazel": "น้ำตาลอ่อน (เฮเซล)",
        "brow_none": "— ไม่ระบุ —",
        "brow_feathery": "คิ้วฟูขนนก",
        "brow_arched": "คิ้วโก่งนิดๆ",
        "brow_straight": "คิ้วตรงแบบเกาหลี",
        "brow_thick": "คิ้วหนาธรรมชาติ",
        "brow_thin": "คิ้วบางคม",
        "lip_none": "— ไม่ระบุ —",
        "lip_cat": "ปากแมว (มุมปากยกขึ้น)",
        "lip_full": "ปากอิ่ม",
        "lip_heart": "ปากรูปหัวใจ (กระจับชัด)",
        "lip_plump": "ปากอวบฉ่ำ",
        "lip_small": "ปากเล็กกุหลาบตูม",
        "lip_thin": "ปากบางได้รูป",
        "fm_aegyo": "ถุงใต้ตาน่ารัก (แอกโยซัล)",
        "fm_mole_lip": "ไฝเสน่ห์ใกล้ริมฝีปาก",
        "fm_dimples": "ลักยิ้ม",
        "fm_high_nose": "สันจมูกโด่ง",
        "fm_lashes": "ขนตายาวธรรมชาติ",
        "fm_mole_eye": "ไฝใต้ตา",
        "fm_freckles": "กระธรรมชาติ",
        "fm_rosy": "แก้มแดงระเรื่อ",
        "fm_button_nose": "จมูกเล็กน่ารัก",
        "fm_snaggle": "ฟันเขี้ยวน่ารัก (ยาเอบะ)",
        "fh_none": "— ไม่ระบุ —",
        "fh_clean": "โกนเกลี้ยง",
        "fh_full_beard": "เคราเต็มหน้า",
        "fh_goatee": "เคราแพะ",
        "fh_stubble": "หนวดเคราเขียวๆ",
        "fh_mustache": "หนวด",
        "fh_short_beard": "เคราสั้น",
        "skf_none": "— ไม่ระบุ —",
        "skf_dewy": "ผิวฉ่ำโกลว์",
        "skf_porcelain": "ผิวเนียนกริบไร้ที่ติ",
        "skf_glass": "ผิวกระจก (Glass Skin)",
        "skf_natural": "ผิวธรรมชาติ มีเท็กซ์เจอร์นิดๆ",
        "skf_matte": "ผิวแมตต์นุ่ม",
        "skf_sunkissed": "ผิวโกลว์รับแดด",
        "skf_real": "ผิวสมจริงสุดๆ (เห็นรูขุมขน)",
        "hf_none": "— ไม่ระบุ —",
        "hf_messy": "ยุ่งนิดๆ แบบตั้งใจ",
        "hf_strands": "ปอยผมกรอบหน้า",
        "hf_glossy": "เงาสลวย",
        "hf_sleek": "เรียบแปล้",
        "hf_tucked": "ทัดหู",
        "hf_voluminous": "ผมพองมีวอลลุ่ม",
        "hf_wet": "ผมเปียก",
        "hf_windswept": "ผมปลิวลม",
        "nl_none": "— ไม่ระบุ —",
        "nl_black": "เล็บดำ",
        "nl_chrome": "เล็บโครม (เกลซโดนัท)",
        "nl_red": "เล็บแดงคลาสสิก",
        "nl_natural": "เล็บธรรมชาติสะอาด",
        "nl_french": "เล็บเฟรนช์",
        "nl_glitter": "เล็บกากเพชร",
        "nl_long": "เล็บยาวทรงอัลมอนด์แต่งลาย",
        "nl_nude": "เล็บเจลสีนู้ด",
        "nl_pastel": "เล็บพาสเทล",
        "ld_none": "— ไม่ระบุ —",
        "ld_back": "แสงย้อน",
        "ld_butterfly": "แสงผีเสื้อ (บนหน้าตรง)",
        "ld_clamshell": "แสงหอยลาย (บิวตี้)",
        "ld_front": "แสงหน้าตรง",
        "ld_loop": "แสงลูป",
        "ld_rembrandt": "แสงเรมบรันต์ (45°)",
        "ld_side": "แสงข้าง",
        "ld_split": "แสงครึ่งหน้า",
        "ld_top": "แสงจากด้านบน",
        "ld_under": "แสงจากด้านล่าง (ลึกลับ)",
        "lc_none": "— ไม่ระบุ —",
        "lc_amber": "อำพันแสงเทียน",
        "lc_cool": "โทนเย็นอมฟ้า",
        "lc_green": "อมเขียวแสงฟลูออเรสเซนต์",
        "lc_red": "แดงมีมูด",
        "lc_neutral": "แสงกลางวันเป็นกลาง",
        "lc_pink_blue": "ชมพูผสมฟ้า",
        "lc_purple": "ม่วงและบานเย็น",
        "lc_teal_orange": "ทีลและส้ม (ภาพยนตร์)",
        "lc_warm": "โทนอุ่นสีทอง",
        "lq_none": "— ไม่ระบุ —",
        "lq_hard": "แสงแข็ง เงาคม",
        "lq_high_contrast": "คอนทราสต์สูง",
        "lq_low_contrast": "คอนทราสต์ต่ำ โปร่งสบาย",
        "lq_soft": "แสงนุ่ม กระจายตัว",
        "ch_none": "— ไม่ระบุ —",
        "ch_aerial": "มุมสูงมาก (โดรน)",
        "ch_top": "มุมบนลงล่างตรงๆ",
        "ch_high": "มุมสูง (กดลง)",
        "ch_slight_high": "สูงกว่าระดับตาเล็กน้อย (ถ่ายแล้วสวย)",
        "ch_eye": "ระดับสายตา",
        "ch_chest": "ระดับอก",
        "ch_waist": "ระดับเอว",
        "ch_slight_low": "ต่ำกว่าระดับตาเล็กน้อย",
        "ch_low": "มุมต่ำ (เงยขึ้น)",
        "ch_ground": "ระดับพื้น",
        "ch_worm": "มุมหนอน (เงยตั้งฉาก)",
        "cd_none": "— ไม่ระบุ —",
        "cd_front": "ด้านหน้าตรง",
        "cd_front_3q": "เฉียงด้านหน้า 45°",
        "cd_side": "ด้านข้าง 90°",
        "cd_back_3q": "เฉียงด้านหลัง",
        "cd_back": "ด้านหลังตรง",
        "cd_over_shoulder": "ข้ามไหล่",
        "cs_none": "— ไม่ระบุ —",
        "cs_telephoto": "เทเลโฟโต้แอบถ่าย (ปาปารัสซี่)",
        "cs_cctv": "กล้องวงจรปิด",
        "cs_dutch": "เอียงกล้อง (Dutch Angle)",
        "cs_pov": "มุมมองบุคคลที่หนึ่ง (POV)",
        "cs_fisheye": "เลนส์ฟิชอาย",
        "cs_mirror": "ภาพสะท้อนในกระจก",
        "cs_selfie": "เซลฟี่ (ยื่นแขน)",
        "cs_through": "ถ่ายลอดฉากหน้า",
        "cs_window": "ถ่ายผ่านกระจกหน้าต่าง",
        "cf_none": "— ไม่ระบุ —",
        "cf_digicam": "กล้องดิจิทัลคอมแพคยุค 2000",
        "cf_arri": "ARRI Alexa (กล้องภาพยนตร์)",
        "cf_canon": "Canon EOS R5 (ดิจิทัลคมชัด)",
        "cf_cinestill": "CineStill 800T (ฟิล์มกลางคืน)",
        "cf_disposable": "กล้องฟิล์มใช้แล้วทิ้ง",
        "cf_superia": "ฟิล์ม Fujifilm Superia 400",
        "cf_fuji": "Fujifilm X-T5 (Classic Chrome)",
        "cf_hasselblad": "Hasselblad มีเดียมฟอร์แมต",
        "cf_ilford": "ฟิล์มขาวดำ Ilford HP5",
        "cf_instax": "Instax Mini (ฟิล์มโพลารอยด์เล็ก)",
        "cf_iphone": "iPhone (มือถือ)",
        "cf_gold": "ฟิล์ม Kodak Gold 200",
        "cf_portra": "ฟิล์ม Kodak Portra 400",
        "cf_leica": "Leica M (เรนจ์ไฟน์เดอร์)",
        "cf_polaroid": "ฟิล์มโพลารอยด์",
        "cf_sony": "Sony A7R V (ดิจิทัลคมชัด)",
        "atm_puddles": "พื้นเปียกสะท้อนแสงหลังฝน",
        "atm_leaves": "ใบไม้ร่วงปลิว",
        "atm_petals": "กลีบซากุระร่วง",
        "atm_confetti": "กระดาษสีโปรยปราย",
        "atm_dust": "ฝุ่นละอองในลำแสง",
        "atm_fireflies": "หิ่งห้อย",
        "atm_fog": "หมอก",
        "atm_wind": "ลมพัดเบาๆ (ผมปลิว)",
        "atm_sparkles": "ประกายวิบวับ",
        "atm_rain": "ฝนตก",
        "atm_smoke": "ควัน / หมอกควัน",
        "atm_snow": "หิมะตก",
        "atm_bubbles": "ฟองสบู่",
        "atm_steam": "ไอน้ำ",
        "bgp_none": "— ไม่ระบุ —",
        "bgp_few": "มีคนเดินผ่านเล็กน้อย",
        "bgp_crowd": "ฝูงชนพลุกพล่าน (เบลอ)",
        "bgp_empty": "ไม่มีคนอื่นในฉาก",
        "lfx_chromatic": "ขอบสีเหลื่อม",
        "lfx_double": "ภาพซ้อน (Double Exposure)",
        "lfx_date": "ตัวเลขวันที่แบบกล้องฟิล์ม",
        "lfx_grain": "เกรนฟิล์ม",
        "lfx_halation": "แสงฟุ้งรอบไฟ (Halation)",
        "lfx_flare": "แสงแฟลร์",
        "lfx_leak": "แสงรั่ว (Light Leak)",
        "lfx_motion": "ภาพเบลอจากการเคลื่อนไหว",
        "lfx_prism": "ปริซึมสายรุ้ง",
        "lfx_bloom": "ฟุ้งนุ่ม (Bloom)",
        "lfx_vignette": "ขอบภาพมืด (Vignette)",
        "loc_dance_studio": "สตูดิโอเต้น",
        "loc_classroom": "ห้องเรียนแสงแดดส่อง",
        "loc_museum": "ห้องโถงพิพิธภัณฑ์",
        "loc_bedroom": "ห้องนอนอบอุ่น",
        "loc_kitchen": "ห้องครัวในบ้าน",
        "loc_living": "โซฟาห้องนั่งเล่น",
        "loc_balcony": "ระเบียงต้นไม้",
        "loc_window_seat": "มุมนั่งริมหน้าต่าง",
        "loc_vanity": "โต๊ะเครื่องแป้ง",
        "loc_crosswalk": "ทางม้าลายกลางเมือง",
        "loc_railway": "รางรถไฟเก่า",
        "loc_bus_stop": "ป้ายรถเมล์",
        "loc_flower_shop": "ร้านดอกไม้",
        "loc_bookstore": "ร้านหนังสือ",
        "loc_bakery": "ร้านเบเกอรี่โทนพาสเทล",
        "loc_boutique": "ร้านเสื้อผ้าบูติก",
        "loc_record_store": "ร้านแผ่นเสียงวินเทจ",
        "loc_laundromat": "ร้านซักผ้าเรโทร",
        "loc_sunflower": "ทุ่งทานตะวัน",
        "loc_lavender": "ทุ่งลาเวนเดอร์",
        "loc_autumn_park": "สวนสาธารณะฤดูใบไม้ร่วง",
        "loc_meadow": "ทุ่งดอกไม้ป่า",
        "loc_lighthouse": "ประภาคารริมทะเล",
        "loc_mansion": "คฤหาสน์คลาสสิก",
        "loc_fine_dining": "ร้านอาหารหรู",
        "loc_santorini": "หมู่บ้านสีขาวสไตล์ซานโตรินี",
        "loc_venice": "คลองสไตล์เวนิส",
        "loc_th_wat": "วัดไทยสีทอง",
        "loc_th_floating": "ตลาดน้ำ",
        "loc_th_chiangmai": "ซอยเมืองเก่าเชียงใหม่",
        "loc_th_shophouse": "ย่านตึกแถวชิโนโปรตุกีส",
        "loc_th_island": "ชายหาดเกาะไทย",
        "loc_th_rooftop": "รูฟท็อปบาร์กรุงเทพ",
        "loc_th_tea": "ไร่ชาบนเขา",
        "loc_th_tuktuk": "ถนนกับรถตุ๊กตุ๊ก",
        "loc_jp_torii": "ศาลเจ้าซุ้มโทริอิ",
        "loc_jp_street": "ซอยในโตเกียว",
        "loc_jp_ryokan": "ห้องเรียวกังเสื่อทาทามิ",
        "loc_bamboo": "ป่าไผ่",
        "loc_kr_hanok": "หมู่บ้านฮันอก",
        "loc_kr_street": "ย่านเก๋ในโซล",
        "loc_photo_booth": "ตู้ถ่ายรูป",
        "loc_bowling": "โบว์ลิ่งเรโทร",
        "loc_carousel": "ม้าหมุนวินเทจ",
        "loc_cinema": "โรงภาพยนตร์",
        "loc_karaoke": "ห้องคาราโอเกะ",
        "loc_tennis": "สนามเทนนิส",
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
    "loc_brick_ruin": "beside an old abandoned red-brick building overgrown with ivy, surrounded by tall wild grass and lush trees",
    "loc_overgrown": "in a lush overgrown garden with tall wild grass, ferns and dappled greenery",
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
    "ps_nostalgic": "warm nostalgic film tone with golden sunlit hues, soft grain, muted greens and a gentle hazy glow, evoking fond summer memories",
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
    # v5.5 — "Not specified" options (emit nothing in the prompt)
    "age_none": "", "eth_none": "", "hair_none": "", "hc_none": "",
    "expr_none": "", "bt_none": "", "app_none": "", "pose_none": "",
    "tod_none": "", "lit_none": "", "loc_none": "", "sf_none": "",
    "dof_none": "",
    # v5.5 — Makeup
    "mu_editorial": "avant-garde editorial makeup with bold graphic artistic accents",
    "mu_freckles": "fresh natural makeup with cute faux freckles scattered across the nose and cheeks",
    "mu_goth": "gothic dark makeup with deep dark lips and dramatic black eyeliner",
    "mu_igari": "Japanese igari-style makeup with soft flushed blush swept across the cheeks",
    "mu_bronzed": "sun-kissed bronzed makeup with a golden glow and highlighted cheekbones",
    "mu_glitter": "playful Y2K glitter makeup with sparkly eyeshadow and glossy lips",
    # v5.5 — Expressions
    "expr_wink": "winking playfully with one eye closed",
    "expr_tongue": "sticking tongue out playfully",
    "expr_mischief": "mischievous impish grin",
    "expr_fierce": "fierce intense piercing gaze",
    "expr_eyes_closed": "eyes gently closed with a serene blissful face",
    "expr_bored": "bored nonchalant expression",
    "expr_angry": "angry intense glare",
    "expr_tearful": "tearful glistening eyes with an emotional expression",
    # v5.5 — Fashion styles
    "fs_basketball": "sporty basketball style with an oversized jersey and athletic shorts",
    "fs_beach_cover": "breezy beachwear with a flowing sarong cover-up over a swimsuit",
    "fs_bikini": "stylish two-piece bikini swimwear",
    "fs_cheer": "cheerleader uniform with a pleated skirt and pom-poms",
    "fs_golf": "modern golf wear with a polo shirt and pleated golf skirt",
    "fs_one_piece": "elegant one-piece swimsuit",
    "fs_rashguard": "sporty long-sleeve rash guard surf wear",
    "fs_school": "neat school uniform with a pleated skirt and ribbon tie",
    "fs_ski": "stylish ski wear with an insulated jacket and snow goggles",
    "fs_teen": "trendy teen fashion with a playful youthful mix of casual pieces",
    "fs_tennis": "sporty tennis outfit with a pleated tennis skirt and fitted polo top",
    "fs_yoga": "form-fitting yoga activewear set with leggings and a sports top",
    # v5.5 — Locations
    "loc_arcade": "inside a retro arcade glowing with colorful game machines",
    "loc_ballroom": "in an opulent grand ballroom with crystal chandeliers and gilded details",
    "loc_basketball": "on an outdoor basketball court with painted lines and a chain-link fence",
    "loc_cherry": "in a park full of blooming cherry blossom trees with petals drifting in the air",
    "loc_cliff": "on a dramatic coastal cliff overlooking the open ocean",
    "loc_convenience": "outside a brightly lit convenience storefront",
    "loc_greenhouse": "inside a lush botanical greenhouse filled with tropical plants",
    "loc_harbor": "at a scenic harbor marina with yachts and sailboats",
    "loc_ice_rink": "at an ice skating rink with a glossy reflective surface",
    "loc_skatepark": "at a concrete skate park with ramps and street art",
    "loc_stadium": "in a large sports stadium with floodlights and sweeping stands",
    "loc_supermarket": "in a colorful supermarket aisle with neatly stocked shelves",
    "loc_vineyard": "in a sun-drenched vineyard with rolling rows of grapevines",
    "loc_yacht": "on the deck of a luxury yacht surrounded by sparkling blue water",
    # v5.5 — Camera angles
    # v5.5 — Lighting
    "lit_silhouette": "dramatic silhouette backlighting against a glowing sunset sky",
    "lit_lowkey": "low-key lighting with deep shadows and a single soft key light",
    "lit_highkey": "bright high-key lighting with soft even illumination and minimal shadows",
    "lit_lantern": "warm glow of traditional paper lanterns",
    "lit_fireworks": "colorful fireworks bursting in the night sky lighting the scene",
    "lit_screen": "cool blue screen glow illuminating the face in a dark room",
    "lit_projector": "projector light casting colorful patterns across the subject",
    "lit_disco": "sparkling disco ball reflections scattering spots of light",
    # v5.5 — Poses
    "pose_boxing": "in a playful boxing stance with fists raised",
    "pose_cartwheel": "captured mid-cartwheel in dynamic motion",
    "pose_dribble": "dribbling a basketball in mid-move",
    "pose_finger_frame": "framing the shot with a finger-frame gesture toward the camera",
    "pose_meditate": "sitting cross-legged in a peaceful lotus meditation pose",
    "pose_ok_sign": "making a cute OK hand sign",
    "pose_point_camera": "pointing playfully straight at the camera",
    "pose_salute": "giving a cheeky two-finger salute",
    "pose_selfie": "taking a selfie with one arm outstretched",
    "pose_shush": "holding one finger to the lips in a playful shush gesture",
    "pose_skip": "skipping forward with a light joyful bounce",
    "pose_thumbs_up": "giving a cheerful thumbs up",
    "pose_tiptoe": "standing on tiptoes reaching upward",
    "pose_wave": "waving hello at the camera cheerfully",
    "pose_yoga": "balancing gracefully in a yoga tree pose",
    "pose_carefree_walk": "walking carefree with arms swinging loosely out to the sides, looking down at the ground with a soft smile",
    "pose_touch_plants": "crouching down and gently touching small plants and leaves on the ground",
    "pose_hold_camera": "holding a vintage film camera at chest level while gazing up and away thoughtfully",
    "pose_grass_stalk": "playfully holding a stalk of wild grass up beside their face",
    "pose_ear_wall": "leaning close to an old wall with a hand cupped behind the ear, as if listening to it",
    "pose_peek_tree": "peeking out playfully from behind a tree trunk with a bright smile",
    "pose_pick_flower": "reaching down to pick a small flower from the grass",
    "pose_smell_flower": "holding a small wildflower up to their nose with both hands, eyes closed with a soft blissful smile",
    "pet_none": "",
    "pet_bird": "with a small bird perched on their outstretched finger",
    "pet_butterflies": "with colorful butterflies fluttering around them",
    "pet_cat": "gently reaching out to a cute cat, about to touch its nose",
    "pet_dog": "accompanied by a friendly dog, petting it affectionately",
    "pet_kitten": "cradling a tiny kitten in their hands",
    "pet_puppy": "playing with an adorable puppy",
    "pet_rabbit": "holding a fluffy white rabbit",
    # v5.7 — pose builder + outfit layers
    "pose_contrapposto": "standing in a relaxed contrapposto stance with weight shifted onto one leg and one hand resting on the hip",
    "pose_hands_hips": "standing confidently with both hands on the hips",
    "pose_hands_nape": "standing with both hands lifted to the nape of the neck, elbows raised and chest open",
    "pose_hand_collar": "standing with one hand lightly touching the collarbone and the other resting on the thigh",
    "pose_foot_kick": "standing on one leg with the other foot playfully kicked up behind",
    "pose_hair_both": "lifting their hair up with both hands, elbows raised",
    "pose_walk_toward": "walking confidently toward the camera",
    "pose_bag_strap": "walking with one hand holding the strap of a shoulder bag",
    "pose_sit_side": "sitting side-saddle on the floor with legs folded to one side and one hand resting on the ground",
    "pose_sit_knee_up": "sitting on the ground with one knee drawn up and an arm resting casually across it",
    "pose_sit_cheek_knee": "sitting with knees drawn up and one cheek resting softly on the knees",
    "pose_sit_chair_back": "sitting backwards on a chair with arms folded over the backrest",
    "pose_sit_ledge": "sitting on a low ledge with legs dangling and hands resting beside them",
    "pose_sit_floor_cross": "sitting cross-legged on the floor with hands resting on the knees",
    "pose_sit_hold_ankle": "sitting with legs bent to one side and one hand gently holding the ankle",
    "pose_wariza_hands": "sitting in a cute wariza with knees together and both hands placed on the floor in front",
    "pose_seiza": "kneeling in seiza, sitting back on the heels with hands resting in the lap",
    "pose_kneel_upright": "kneeling upright with hands resting on the thighs",
    "pose_one_knee": "kneeling on one knee with a forearm resting on the raised knee",
    "pose_kneel_look_up": "kneeling on one knee and looking up toward the sky",
    "pose_kneel_hair": "kneeling upright with one hand in the hair and the other on the hip",
    "pose_lie_stomach": "lying on the stomach propped on the elbows, chin in the hands, feet kicked up playfully behind",
    "pose_lie_side": "lying on one side with the head propped up on one hand",
    "pose_lie_back_hair": "lying on the back with arms resting above the head and hair spread out around them",
    "pose_lie_back_knee": "lying on the back, relaxed, with one knee raised",
    "pose_lie_arm_pillow": "lying on the stomach with the head resting on folded arms",
    "pose_crouch_chin": "crouching down with elbows on the knees and chin resting in one hand",
    "pose_crouch_look_back": "crouching low and glancing back over the shoulder",
    "pose_bend_knees": "bending forward slightly with hands on the knees, looking up at the camera",
    "pose_bend_shoe": "bending down to adjust a shoe strap",
    "pose_double_peace": "making double peace signs under the chin",
    "pose_gyaru_peace": "making a gyaru peace sign with the back of the hand facing out beside the face",
    "pose_fist_cheeks": "pressing small fists cutely against both cheeks",
    "pose_bunny_ears": "holding both hands above the head like bunny ears",
    "pose_cat_paw": "making a playful cat-paw gesture with loosely curled hands near the face",
    "pose_rawr": "doing a playful 'rawr' pose with hands curled like little claws",
    "pose_poke_cheek": "poking their own cheek with an index finger and a cute smile",
    "pose_flower_chin": "resting the chin on both open palms like a blooming flower",
    "pose_sweater_paws": "covering the mouth shyly with long sweater-paw sleeves",
    "pose_please": "pressing palms together in a cute pleading 'please' gesture",
    "pose_self_hug": "shyly hugging themselves with both arms",
    "pose_big_heart": "making a big heart shape with both arms above the head",
    "pose_yawn": "yawning cutely with one hand over the mouth while stretching",
    "pose_coat_lapels": "holding the lapels of their coat with both hands",
    "pose_phone_check": "looking down at a smartphone candidly",
    "pose_skirt_hem": "lightly holding the hem of the skirt with both hands",
    "pose_curtsy": "dipping into a graceful curtsy",
    "pose_umbrella": "holding an open umbrella resting over one shoulder",
    "pose_bouquet": "holding a bouquet of flowers close to the chest",
    "pose_read_book": "reading an open book, absorbed in it",
    "pose_coffee": "holding a coffee cup close with both hands",
    "pose_bicycle": "standing beside a bicycle with one hand on the handlebar",
    "pose_balloons": "holding a bunch of balloons",
    "pose_ballet": "balancing in a graceful ballet arabesque",
    "pose_tennis_swing": "swinging a tennis racket mid-stroke",
    "pose_skateboard": "riding a skateboard mid-glide",
    "pose_lunge": "stretching in a deep lunge",
    "dir_none": "",
    "dir_back": "seen from behind with the back to the camera",
    "dir_back_look": "back turned to the camera, looking back over the shoulder",
    "dir_front": "body facing the camera squarely",
    "dir_side": "body turned sideways in full profile",
    "dir_slight": "body angled slightly away from the camera",
    "dir_3q": "body turned three-quarters to the camera",
    "head_none": "",
    "head_chin_down": "chin lowered slightly",
    "head_chin_up": "chin raised slightly",
    "head_shoulder": "cheek tipped toward the shoulder",
    "head_rest_hand": "head resting against one hand",
    "head_back": "head tilted back",
    "head_tilt": "head tilted gently to one side",
    "head_turned": "head turned to the side",
    "gaze_none": "",
    "gaze_closed": "eyes gently closed",
    "gaze_camera": "looking directly at the camera with engaging eye contact",
    "gaze_down": "eyes cast downward",
    "gaze_away": "gazing off into the distance",
    "gaze_upward_glance": "glancing up at the camera through the lashes",
    "gaze_up": "eyes looking upward",
    "gaze_side_glance": "giving the camera a sideways glance",
    "hands_none": "",
    "hands_crossed": "arms crossed",
    "hands_overhead": "arms raised overhead",
    "hands_relaxed": "arms relaxed naturally at the sides",
    "hands_both_hips": "both hands on the hips",
    "hands_lips": "a fingertip resting lightly on the lips",
    "hands_hair": "one hand running through the hair",
    "hands_hip": "one hand on the hip",
    "hands_neck": "one hand resting at the neck and collarbone",
    "hands_face": "one hand softly touching the face",
    "hands_behind": "hands clasped behind the back",
    "hands_clasped": "hands clasped loosely in front",
    "hands_pockets": "hands tucked casually into the pockets",
    "hands_strap": "one hand holding a bag strap",
    "hands_sleeve": "fingers tugging lightly at a sleeve",
    "legs_none": "",
    "legs_ankles_crossed": "ankles crossed",
    "legs_kick_back": "one foot kicked up behind",
    "legs_knees_in": "knees together with toes turned slightly inward",
    "legs_crossed_knee": "legs crossed at the knee",
    "legs_cross_stand": "legs crossed while standing",
    "legs_extended": "legs stretched out long",
    "legs_together": "legs held neatly together",
    "legs_mid_stride": "caught mid-stride",
    "legs_tiptoe": "up on tiptoe",
    "legs_knee_bent": "one knee slightly bent",
    "legs_wide": "feet planted in a wide power stance",
    "pe_none": "",
    "pe_candid": "with candid, unposed body language",
    "pe_confident": "with strong, confident body language",
    "pe_cool": "with cool, nonchalant body language",
    "pe_dynamic": "captured mid-motion with dynamic energy",
    "pe_elegant": "with graceful, elegant posture",
    "pe_playful": "with playful, energetic body language",
    "pe_relaxed": "with relaxed, natural body language",
    "pe_shy": "with shy, soft body language",
    "dress_none": "",
    "dress_babydoll": "wearing a babydoll dress",
    "dress_ballgown": "wearing a ball gown",
    "dress_bodycon": "wearing a bodycon dress",
    "dress_corset": "wearing a corset dress",
    "dress_jumpsuit": "wearing a jumpsuit",
    "dress_knit": "wearing a knit dress",
    "dress_maxi": "wearing a flowing maxi dress",
    "dress_midi": "wearing a midi dress",
    "dress_mini": "wearing a mini dress",
    "dress_off_shoulder": "wearing an off-shoulder dress",
    "dress_pinafore": "wearing a pinafore dress over a simple top",
    "dress_qipao": "wearing a qipao cheongsam dress",
    "dress_romper": "wearing a romper playsuit",
    "dress_shirt": "wearing a shirt dress",
    "dress_slip": "wearing a slip dress",
    "dress_sundress": "wearing a sundress",
    "dress_tea": "wearing a vintage tea dress",
    "dress_tiered": "wearing a tiered ruffle dress",
    "dress_wrap": "wearing a wrap dress",
    "out_none": "",
    "out_blazer": "a tailored blazer",
    "out_bolero": "a cropped bolero shrug",
    "out_cape": "a cape",
    "out_cardigan": "a soft knit cardigan",
    "out_cropped_cardigan": "a cropped knit cardigan",
    "out_denim_jacket": "a denim jacket",
    "out_faux_fur": "a fluffy faux-fur coat",
    "out_kimono": "a flowing kimono-style cardigan",
    "out_leather": "a leather jacket",
    "out_wool_coat": "a long wool coat",
    "out_open_shirt": "an unbuttoned shirt worn open",
    "out_puffer": "a puffer jacket",
    "out_shawl": "a soft shawl draped over the shoulders",
    "out_trench": "a trench coat",
    "out_tweed": "a tweed jacket",
    "out_varsity": "a varsity jacket",
    "out_zip_hoodie": "an open zip-up hoodie",
    "fit_none": "",
    "fit_aline": "an A-line silhouette",
    "fit_body": "a body-hugging silhouette",
    "fit_cropped": "a cropped, high-waisted silhouette",
    "fit_fitted": "a neatly fitted silhouette",
    "fit_flowy": "a flowy, airy silhouette",
    "fit_layered": "a layered silhouette",
    "fit_oversized": "an oversized, relaxed silhouette",
    "fit_relaxed": "a relaxed-fit silhouette",
    "fit_tailored": "a sharply tailored silhouette",
    "leg_none": "",
    "leg_ankle": "white ankle socks",
    "leg_crew": "crew socks",
    "leg_fishnet": "fishnet tights",
    "leg_frilly": "frilly lace-trimmed socks",
    "leg_knee": "knee-high socks",
    "leg_warmers": "knit leg warmers",
    "leg_loose": "slouchy Japanese loose socks",
    "leg_opaque": "opaque black tights",
    "leg_patterned": "patterned tights",
    "leg_sheer_black": "sheer black tights",
    "leg_nude": "sheer nude stockings",
    "leg_thigh": "thigh-high socks",
    "leg_white_tights": "white tights",
    "det_corset": "a corset-style lace-up bodice",
    "det_embroidery": "delicate embroidery",
    "det_floral": "a floral print",
    "det_gingham": "a gingham pattern",
    "det_lace_trim": "lace trim",
    "det_off_shoulder": "an off-shoulder neckline",
    "det_buttons": "pearl buttons",
    "det_collar": "a rounded Peter Pan collar",
    "det_checks": "a plaid check pattern",
    "det_pleats": "crisp pleats",
    "det_polka": "a polka-dot pattern",
    "det_puff": "puff sleeves",
    "det_bows": "ribbon bow accents",
    "det_frills": "ruffled frill trims",
    "det_sailor": "a sailor collar",
    "det_sequins": "sparkling sequins",
    "det_sheer_sleeves": "sheer sleeves",
    "det_slit": "a side slit",
    "det_square_neck": "a square neckline",
    "det_stripes": "stripes",
    "det_tiered": "tiered layers",
    "det_v_neck": "a V-neckline",
    "os_none": "",
    "os_spr_frill_knit": "wearing an ivory frill-trimmed knit top, a denim mini skirt and a light beige spring coat, with white crew socks and white sneakers",
    "os_spr_floral_cami": "wearing a yellow floral camisole under a soft pink cardigan and a pink pleated mini skirt, with ivory socks, mary jane shoes and a small ribbon-trimmed shoulder bag",
    "os_spr_floral_midi": "wearing a pink floral midi dress with a cropped denim jacket, white ankle socks, strappy sandals and a mini bag",
    "os_spr_ribbon_blouse": "wearing a cream ribbon-tie blouse and a mint green pleated midi skirt, with beige pumps, a small handbag and a delicate gold necklace",
    "os_spr_shirt_dress": "wearing a sage green shirt dress with a ribbon tie at the collar, sheer beige tights, low sandals and a mini bag on a gold chain",
    "os_spr_lace_cami": "wearing a blue lace-trimmed camisole layered under a cropped knit cardigan and cream wide-leg pants, with pointed pumps and a pearl necklace",
    "os_sum_linen": "wearing an oversized white linen shirt with rolled sleeves and beige linen shorts, with leather slide sandals, a straw tote bag and thin gold hoop earrings",
    "os_sum_sundress": "wearing a white cotton eyelet sundress and a wide-brim straw hat, with flat strappy sandals and a woven basket bag",
    "os_sum_crop_denim": "wearing a fitted baby-tee crop top and high-waisted light-wash denim shorts, with white ankle socks, chunky sneakers and a mini shoulder bag",
    "os_sum_halter_maxi": "wearing a flowing printed halter-neck maxi dress, with flat sandals, layered gold anklets and oversized sunglasses",
    "os_sum_gingham": "wearing a red gingham puff-sleeve top and a white tiered mini skirt, with white canvas sneakers and a cherry hair clip",
    "os_sum_resort": "wearing a short-sleeve printed resort shirt and relaxed cream linen trousers, with leather loafers and round sunglasses",
    "os_aut_trench": "wearing a classic beige trench coat over a fine-knit cream turtleneck and straight-leg blue jeans, with brown leather loafers and a structured shoulder bag",
    "os_aut_corduroy": "wearing a brown corduroy pinafore dress over a cream ribbed knit top, with opaque black tights, mary jane shoes and a wool beret",
    "os_aut_plaid": "wearing a burgundy plaid pleated skirt and a white collared shirt under a chunky cream cardigan, with knee-high socks and chunky penny loafers",
    "os_aut_leather": "wearing a black leather biker jacket over a grey ribbed tank and a champagne satin slip midi skirt, with black ankle boots",
    "os_aut_knit_dress": "wearing a camel ribbed knit midi dress with a thin belt, knee-high brown suede boots and a small gold pendant necklace",
    "os_aut_blazer": "wearing an oversized grey wool blazer over a white t-shirt and pleated wide-leg trousers, with white leather sneakers and a black tote bag",
    "os_win_wool_coat": "wearing a long camel wool coat over a cream cable-knit sweater and a knit mini skirt, with a chunky knit scarf, black tights and knee-high leather boots",
    "os_win_puffer": "wearing a cropped white puffer jacket over a grey hoodie and relaxed sweatpants, with a soft knit beanie and chunky winter sneakers",
    "os_win_fur": "wearing a fluffy faux-fur coat over a fitted black knit dress, with sheer black tights, heeled ankle boots and pearl earrings",
    "os_win_tweed": "wearing a matching cream tweed jacket and mini skirt set with gold buttons, a pearl necklace, white tights and black ballet flats",
    "os_win_overcoat": "wearing a charcoal wool overcoat over a black turtleneck sweater and tailored grey trousers, with leather chelsea boots and a cashmere scarf",
    "os_win_cozy": "wearing an oversized fluffy knit sweater and a pleated mini skirt, with cream knit leg warmers, fuzzy earmuffs and suede boots",
    "os_par_sequin": "wearing a sparkling silver sequin mini dress, with strappy heeled sandals, a small metallic clutch and statement drop earrings",
    "os_par_satin_gown": "wearing a floor-length champagne satin slip gown with a cowl neckline, delicate strappy heels and a thin diamond necklace",
    "os_par_tulle": "wearing a pastel pink tulle princess dress with a fitted bodice and layered full skirt, satin ribbon details, pearl hair accessories and ballet flats",
    "os_par_velvet_suit": "wearing a tailored deep green velvet suit with a black silk shirt, polished oxford shoes and a slim watch",
    "os_par_lbd": "wearing a classic little black dress with a square neckline, sheer black tights, black pointed pumps and pearl stud earrings",
    "fab_corduroy": "corduroy fabric",
    "fab_crochet": "crochet knit",
    "fab_jersey": "soft jersey fabric",
    "fab_knit": "fine-gauge knit",
    "fab_organza": "organza fabric",
    "fab_sequin": "sequin fabric",
    "fab_tulle": "tulle fabric",
    "col_butter": "soft butter yellow color tones",
    "col_grey": "grey color tones",
    "col_ivory": "soft ivory color tones",
    # v5.8 — subject details, camera & scene
    "st_none": "",
    "st_porcelain": "porcelain fair skin",
    "st_fair": "fair skin",
    "st_light_warm": "light warm-toned skin",
    "st_medium": "medium wheat-toned skin",
    "st_olive": "olive skin",
    "st_tan": "sun-kissed tan skin",
    "st_brown": "warm brown skin",
    "st_deep": "deep rich dark skin",
    "fsh_none": "",
    "fsh_heart": "a heart-shaped face",
    "fsh_sharp": "high sculpted cheekbones",
    "fsh_oval": "an oval face",
    "fsh_round": "a soft round face with full cheeks",
    "fsh_small": "a small delicate face",
    "fsh_v": "a slim V-line jaw",
    "eye_none": "",
    "eye_almond": "almond-shaped",
    "eye_big": "big round",
    "eye_doe": "large doe",
    "eye_double": "double-lidded",
    "eye_monolid": "monolid",
    "eye_droopy": "soft droopy puppy-like",
    "eye_cat": "upturned cat-like",
    "ec_none": "",
    "ec_amber": "amber",
    "ec_black": "deep black",
    "ec_blue": "blue",
    "ec_dark_brown": "dark brown",
    "ec_green": "green",
    "ec_grey": "grey",
    "ec_hazel": "warm hazel",
    "brow_none": "",
    "brow_feathery": "fluffy feathered brows",
    "brow_arched": "softly arched brows",
    "brow_straight": "soft straight brows",
    "brow_thick": "thick natural brows",
    "brow_thin": "thin defined brows",
    "lip_none": "",
    "lip_cat": "cat-like lips with naturally upturned corners",
    "lip_full": "full lips",
    "lip_heart": "heart-shaped lips with a defined cupid's bow",
    "lip_plump": "plump glossy lips",
    "lip_small": "small rosebud lips",
    "lip_thin": "thin, well-defined lips",
    "fm_aegyo": "puffy aegyo-sal under the eyes",
    "fm_mole_lip": "a beauty mark near the lips",
    "fm_dimples": "cute dimples",
    "fm_high_nose": "a high nose bridge",
    "fm_lashes": "long natural lashes",
    "fm_mole_eye": "a small beauty mark under one eye",
    "fm_freckles": "light natural freckles across the nose",
    "fm_rosy": "naturally rosy cheeks",
    "fm_button_nose": "a small button nose",
    "fm_snaggle": "a cute snaggletooth",
    "fh_none": "",
    "fh_clean": "clean-shaven",
    "fh_full_beard": "a full well-groomed beard",
    "fh_goatee": "a goatee",
    "fh_stubble": "light stubble",
    "fh_mustache": "a mustache",
    "fh_short_beard": "a short trimmed beard",
    "skf_none": "",
    "skf_dewy": "with dewy glowing skin",
    "skf_porcelain": "with flawless porcelain-smooth skin",
    "skf_glass": "with luminous glass skin",
    "skf_natural": "with natural, lightly textured skin",
    "skf_matte": "with smooth soft-matte skin",
    "skf_sunkissed": "with sun-kissed glowing skin",
    "skf_real": "with ultra-realistic skin texture showing pores and fine details",
    "hf_none": "",
    "hf_messy": "effortlessly messy hair",
    "hf_strands": "loose face-framing strands",
    "hf_glossy": "glossy silky hair",
    "hf_sleek": "sleek polished hair",
    "hf_tucked": "hair tucked behind the ears",
    "hf_voluminous": "voluminous hair",
    "hf_wet": "wet-look hair",
    "hf_windswept": "wind-swept hair",
    "nl_none": "",
    "nl_black": "with glossy black nails",
    "nl_chrome": "with glazed chrome nails",
    "nl_red": "with classic red nails",
    "nl_natural": "with clean natural manicured nails",
    "nl_french": "with a French manicure",
    "nl_glitter": "with sparkly glitter nails",
    "nl_long": "with long almond-shaped decorated nails",
    "nl_nude": "with nude gel nails",
    "nl_pastel": "with pastel nails",
    "ld_none": "",
    "ld_back": "backlighting from behind the subject",
    "ld_butterfly": "butterfly lighting from above and in front, flattering the cheekbones",
    "ld_clamshell": "clamshell beauty lighting with a soft fill from below and minimal shadows",
    "ld_front": "soft front lighting",
    "ld_loop": "loop lighting casting a soft small nose shadow",
    "ld_rembrandt": "Rembrandt lighting with a small triangle of light on the shadowed cheek",
    "ld_side": "directional side lighting sculpting the face",
    "ld_split": "split lighting with half the face in shadow",
    "ld_top": "overhead top light",
    "ld_under": "dramatic underlighting from below",
    "lc_none": "",
    "lc_amber": "deep amber candlelit tones",
    "lc_cool": "cool bluish color temperature",
    "lc_green": "a greenish fluorescent tint",
    "lc_red": "moody red light",
    "lc_neutral": "neutral daylight color balance",
    "lc_pink_blue": "mixed pink and blue lighting",
    "lc_purple": "purple and magenta toned light",
    "lc_teal_orange": "cinematic teal and orange color contrast",
    "lc_warm": "warm golden color temperature",
    "lq_none": "",
    "lq_hard": "hard light with crisp defined shadows",
    "lq_high_contrast": "high-contrast lighting",
    "lq_low_contrast": "low-contrast airy lighting",
    "lq_soft": "soft diffused light",
    "ch_none": "",
    "ch_aerial": "aerial drone view from high above the scene",
    "ch_top": "top-down shot from directly overhead",
    "ch_high": "high-angle shot with the camera well above the subject looking down",
    "ch_slight_high": "camera slightly above eye level angled gently down, a flattering portrait angle",
    "ch_eye": "camera at eye level, looking straight at the subject",
    "ch_chest": "camera held at chest level",
    "ch_waist": "camera held at waist level, looking slightly up",
    "ch_slight_low": "camera slightly below eye level angled gently upward",
    "ch_low": "low-angle shot with the camera below the subject looking up, making them look tall and powerful",
    "ch_ground": "camera placed at ground level, close to the floor",
    "ch_worm": "worm's eye view from the ground looking straight up",
    "cd_none": "",
    "cd_front": "camera directly in front of the subject",
    "cd_front_3q": "camera at a 45-degree angle to the front of the subject",
    "cd_side": "camera to the side of the subject for a profile view",
    "cd_back_3q": "camera behind and to one side of the subject, showing the back and a partial profile",
    "cd_back": "camera directly behind the subject",
    "cd_over_shoulder": "over-the-shoulder framing",
    "cs_none": "",
    "cs_telephoto": "candid telephoto shot from a distance, as if unnoticed",
    "cs_cctv": "elevated security-camera viewpoint from a high corner",
    "cs_dutch": "dutch angle tilted composition",
    "cs_pov": "first-person POV shot",
    "cs_fisheye": "shot up close with playful fisheye lens distortion",
    "cs_mirror": "captured as a reflection in a mirror",
    "cs_selfie": "selfie angle shot from arm's length slightly above eye level",
    "cs_through": "shot through foreground elements such as leaves or a doorway framing the subject",
    "cs_window": "shot through a window pane with soft reflections",
    "cf_none": "",
    "cf_digicam": "shot on an early-2000s compact digital camera",
    "cf_arri": "shot on an ARRI Alexa cinema camera",
    "cf_canon": "shot on a Canon EOS R5",
    "cf_cinestill": "shot on CineStill 800T film with red halation around lights",
    "cf_disposable": "shot on a disposable film camera with on-camera flash",
    "cf_superia": "shot on Fujifilm Superia 400 film with cool green tones",
    "cf_fuji": "shot on a Fujifilm X-T5 with Classic Chrome film simulation",
    "cf_hasselblad": "shot on a Hasselblad medium format camera",
    "cf_ilford": "shot on Ilford HP5 black and white film",
    "cf_instax": "shot on Fujifilm Instax Mini instant film",
    "cf_iphone": "shot on an iPhone with a natural smartphone photo look",
    "cf_gold": "shot on Kodak Gold 200 film with warm nostalgic colors",
    "cf_portra": "shot on Kodak Portra 400 film with soft natural skin tones",
    "cf_leica": "shot on a Leica M rangefinder",
    "cf_polaroid": "shot on Polaroid instant film",
    "cf_sony": "shot on a Sony A7R V",
    "atm_puddles": "with wet ground and puddles reflecting the lights after rain",
    "atm_leaves": "with red and golden autumn leaves falling through the air",
    "atm_petals": "with pink cherry blossom petals drifting through the air",
    "atm_confetti": "with colorful confetti falling",
    "atm_dust": "with dust particles glittering in the light beams",
    "atm_fireflies": "with glowing fireflies floating around",
    "atm_fog": "with soft fog and mist hanging in the air",
    "atm_wind": "with a gentle breeze blowing, hair and clothes fluttering softly in the wind",
    "atm_sparkles": "with tiny magical sparkles in the air",
    "atm_rain": "with rain falling from the sky",
    "atm_smoke": "with drifting smoke and haze",
    "atm_snow": "with snow gently falling",
    "atm_bubbles": "with iridescent soap bubbles floating in the air",
    "atm_steam": "with soft rising steam",
    "bgp_none": "",
    "bgp_few": "with a few passersby in the background",
    "bgp_crowd": "with a bustling crowd blurred in the background",
    "bgp_empty": "with no other people in the scene",
    "lfx_chromatic": "slight chromatic aberration",
    "lfx_double": "a double exposure effect",
    "lfx_date": "an orange date stamp in the corner like an old film camera",
    "lfx_grain": "fine film grain",
    "lfx_halation": "soft halation glow around highlights",
    "lfx_flare": "subtle lens flare",
    "lfx_leak": "warm light leaks",
    "lfx_motion": "motion blur conveying movement",
    "lfx_prism": "prism rainbow light refractions",
    "lfx_bloom": "dreamy soft bloom",
    "lfx_vignette": "a gentle vignette",
    "loc_dance_studio": "in a dance studio with wall mirrors and a wooden floor",
    "loc_classroom": "in a sunlit classroom with wooden desks",
    "loc_museum": "in a grand museum hall with high ceilings",
    "loc_bedroom": "in a cozy bedroom with soft bedding and warm decor",
    "loc_kitchen": "in a bright homey kitchen",
    "loc_living": "on a sofa in a stylish living room",
    "loc_balcony": "on a sunny apartment balcony filled with potted plants",
    "loc_window_seat": "on a cushioned window seat bathed in soft daylight",
    "loc_vanity": "at a vanity table with a lit mirror",
    "loc_crosswalk": "on a busy city crosswalk",
    "loc_railway": "along old railway tracks stretching into the distance",
    "loc_bus_stop": "at a city bus stop",
    "loc_flower_shop": "in a charming flower shop overflowing with blooms",
    "loc_bookstore": "in a cozy independent bookstore",
    "loc_bakery": "in a sweet pastel bakery with display cases of pastries",
    "loc_boutique": "in a chic fashion boutique with clothing racks",
    "loc_record_store": "in a vintage record store",
    "loc_laundromat": "in a retro laundromat with rows of washing machines",
    "loc_sunflower": "in a vast sunflower field",
    "loc_lavender": "in a purple lavender field",
    "loc_autumn_park": "in a park with golden autumn trees and fallen leaves",
    "loc_meadow": "in a wildflower meadow at the edge of the woods",
    "loc_lighthouse": "by a white lighthouse on the seashore",
    "loc_mansion": "inside a classic mansion with tall windows and ornate moldings",
    "loc_fine_dining": "in an upscale fine dining restaurant with candlelit tables",
    "loc_santorini": "in a Santorini-style village with white walls and blue domes",
    "loc_venice": "beside a Venice-style canal with gondolas",
    "loc_th_wat": "at a golden Thai Buddhist temple with ornate tiered roofs",
    "loc_th_floating": "at a bustling Thai floating market with wooden boats full of fruit and flowers",
    "loc_th_chiangmai": "on a quiet lane in Chiang Mai old town with old wooden houses and bougainvillea",
    "loc_th_shophouse": "on a street of old Sino-Portuguese shophouses with colorful facades",
    "loc_th_island": "on a white-sand Thai island beach with longtail boats and limestone cliffs",
    "loc_th_rooftop": "at a rooftop bar overlooking the glittering Bangkok skyline at night",
    "loc_th_tea": "on rolling terraced green tea plantation hills",
    "loc_th_tuktuk": "on a lively Bangkok street beside a colorful tuk-tuk",
    "loc_jp_torii": "under rows of vermilion torii gates at a Japanese shrine",
    "loc_jp_street": "on a narrow Tokyo side street with vending machines and hanging signs",
    "loc_jp_ryokan": "in a traditional Japanese ryokan room with tatami mats and shoji screens",
    "loc_bamboo": "in a towering bamboo forest",
    "loc_kr_hanok": "in a traditional Korean hanok village with curved tiled roofs",
    "loc_kr_street": "on a trendy Seoul neighborhood street lined with cafés",
    "loc_photo_booth": "inside a photo booth with a colorful curtain",
    "loc_bowling": "at a retro bowling alley",
    "loc_carousel": "beside a glowing vintage carousel",
    "loc_cinema": "in a movie theater with red velvet seats",
    "loc_karaoke": "in a karaoke room glowing with colorful LED lights",
    "loc_tennis": "on a tennis court",
}


# ═══════════════════════════════════════════════════════════════════════════
#  3. HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def t(key: str) -> str:
    lang = st.session_state.get("lang", "en")
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

def eng(key: str) -> str:
    return ENGLISH_VALUES.get(key, "")

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
HR_KEYS_WOMEN = [
    "hair_none",
    "hair_long", "hair_straight", "hair_loose_waves",
    "hair_curly", "hair_wavy", "hair_layered", "hair_wolf_cut",
    "hair_hush_cut", "hair_hime", "hair_bob", "hair_lob", "hair_pixie",
    "hair_ponytail", "hair_high_ponytail", "hair_bun", "hair_messy_bun",
    "hair_space_buns", "hair_braids", "hair_french_braid",
    "hair_twin_braids", "hair_twintails",
    "hair_half_up", "hair_side_swept",
]
HR_KEYS_MEN = [
    "hair_none",
    "hair_short", "hair_buzz", "hair_crew_cut", "hair_middle_part",
    "hair_textured_crop", "hair_undercut", "hair_fade", "hair_slick_back",
    "hair_man_bun", "hair_bald",
]
# Full list (used for non-binary and as the language-reset superset)
HR_KEYS = HR_KEYS_WOMEN + HR_KEYS_MEN[1:]  # skip duplicate hair_none

def hair_keys_for_gender(gd_key: str):
    """Hairstyle option pool filtered by the selected gender."""
    if gd_key == "gender_female":
        return HR_KEYS_WOMEN
    if gd_key == "gender_male":
        return HR_KEYS_MEN
    return HR_KEYS
HC_KEYS = ["hc_none", "hc_black", "hc_blue_black", "hc_dark_brown", "hc_ash_brown",
           "hc_milk_tea", "hc_light_brown", "hc_honey_blonde", "hc_blonde",
           "hc_platinum", "hc_red", "hc_burgundy", "hc_rose_gold",
           "hc_pink", "hc_purple", "hc_blue", "hc_silver", "hc_white",
           "hc_ombre", "hc_highlights"]
BN_KEYS = ["bangs_none", "bangs_straight", "bangs_see_through", "bangs_side",
           "bangs_curtain", "bangs_wispy", "bangs_micro", "bangs_hime"]
EX_KEYS = ["expr_none", "expr_smile", "expr_bright_smile", "expr_laugh",
           "expr_giggle", "expr_wink", "expr_tongue",
           "expr_soft_gaze", "expr_doe_eyes", "expr_pout", "expr_playful",
           "expr_mischief", "expr_shy", "expr_confident", "expr_smirk",
           "expr_fierce", "expr_dreamy",
           "expr_peaceful", "expr_eyes_closed", "expr_neutral", "expr_bored",
           "expr_pensive", "expr_serious", "expr_surprised",
           "expr_angry", "expr_sad", "expr_tearful", "expr_sultry"]
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
FS_KEYS = ["fs_athleisure", "fs_barbiecore", "fs_basketball", "fs_beach_cover",
           "fs_bikini", "fs_bohemian", "fs_office",
           "fs_casual", "fs_cheer", "fs_clean_girl", "fs_coquette", "fs_cottagecore",
           "fs_cyberpunk", "fs_dark_academia", "fs_egirl", "fs_elegant",
           "fs_golf", "fs_gorpcore", "fs_gothic", "fs_grunge", "fs_japanese",
           "fs_korean", "fs_light_academia", "fs_minimalist", "fs_mob_wife",
           "fs_old_money", "fs_one_piece", "fs_parisian", "fs_preppy",
           "fs_rashguard", "fs_resort",
           "fs_rockstar", "fs_school", "fs_skater", "fs_ski", "fs_streetwear",
           "fs_teen", "fs_tennis", "fs_thai",
           "fs_vintage", "fs_western", "fs_y2k", "fs_yoga"]
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
# one category; LO_KEYS is derived: None, Studio (default), then A-Z.
LCAT_KEYS = ["lcat_all", "lcat_indoor", "lcat_home", "lcat_city", "lcat_shops",
            "lcat_nature", "lcat_water", "lcat_luxury", "lcat_travel", "lcat_thai",
            "lcat_asia", "lcat_leisure"]
LOC_CATEGORIES = {
    "lcat_indoor": ["loc_art_gallery", "loc_dance_studio", "loc_library", "loc_museum",
            "loc_studio", "loc_classroom"],
    "lcat_home": ["loc_balcony", "loc_bedroom", "loc_kitchen", "loc_room", "loc_living",
            "loc_vanity", "loc_window_seat"],
    "lcat_city": ["loc_bridge", "loc_bus_stop", "loc_crosswalk", "loc_neon_alley",
            "loc_night_market", "loc_railway", "loc_rooftop", "loc_shopping",
            "loc_subway", "loc_train", "loc_university", "loc_street"],
    "lcat_shops": ["loc_bookstore", "loc_cafe", "loc_convenience", "loc_boutique",
            "loc_flower_shop", "loc_bakery", "loc_laundromat", "loc_supermarket",
            "loc_record_store"],
    "lcat_nature": ["loc_autumn_park", "loc_cherry", "loc_desert", "loc_flower_field",
            "loc_forest", "loc_garden", "loc_greenhouse", "loc_lavender",
            "loc_mountain", "loc_brick_ruin", "loc_overgrown", "loc_rice_field",
            "loc_snow", "loc_sunflower", "loc_vineyard", "loc_meadow"],
    "lcat_water": ["loc_beach", "loc_cliff", "loc_harbor", "loc_lake", "loc_pool",
            "loc_lighthouse", "loc_waterfall"],
    "lcat_luxury": ["loc_ballroom", "loc_mansion", "loc_fine_dining", "loc_stairs",
            "loc_hotel_lobby", "loc_yacht"],
    "lcat_travel": ["loc_airport", "loc_castle", "loc_old_town", "loc_santorini", "loc_temple",
            "loc_venice"],
    "lcat_thai": ["loc_th_rooftop", "loc_th_chiangmai", "loc_th_floating", "loc_th_wat",
            "loc_th_shophouse", "loc_th_tea", "loc_th_island", "loc_th_tuktuk"],
    "lcat_asia": ["loc_bamboo", "loc_kr_hanok", "loc_jp_ryokan", "loc_kr_street", "loc_jp_torii",
            "loc_jp_street"],
    "lcat_leisure": ["loc_amusement", "loc_aquarium", "loc_arcade", "loc_basketball", "loc_gym",
            "loc_ice_rink", "loc_karaoke", "loc_cinema", "loc_photo_booth",
            "loc_bowling", "loc_skatepark", "loc_stadium", "loc_tennis", "loc_carousel"],
}
LO_KEYS = ["loc_none", "loc_studio"] + sorted(
    (k for keys in LOC_CATEGORIES.values() for k in keys if k != "loc_studio"),
    key=lambda k: TRANSLATIONS["en"][k].lower())


def loc_keys_for_category(lcat_key: str):
    """Location option pool for the selected category (None stays first)."""
    if lcat_key in LOC_CATEGORIES:
        return ["loc_none"] + [k for k in LO_KEYS if k in LOC_CATEGORIES[lcat_key]]
    return LO_KEYS

TD_KEYS = ["tod_none", "tod_golden", "tod_blue", "tod_noon", "tod_night",
           "tod_overcast", "tod_sunrise"]
LT_KEYS = ["lit_none", "lit_natural", "lit_window", "lit_studio",
           "lit_highkey", "lit_lowkey", "lit_rim", "lit_silhouette",
           "lit_neon", "lit_fairy", "lit_lantern", "lit_candle",
           "lit_dramatic", "lit_flash",
           "lit_backlit", "lit_dappled", "lit_blinds", "lit_gel",
           "lit_spotlight", "lit_moonlight", "lit_bonfire", "lit_fireworks",
           "lit_screen", "lit_projector", "lit_disco", "lit_godrays"]
SN_KEYS = ["season_none", "season_spring", "season_summer",
           "season_autumn", "season_winter", "season_rainy"]
PS_KEYS = ["ps_none", "ps_dreamy", "ps_soft", "ps_vivid", "ps_bw",
           "ps_vintage", "ps_nostalgic", "ps_cinematic", "ps_moody", "ps_pastel",
           "ps_hdr", "ps_matte", "ps_commercial", "ps_editorial",
           "ps_documentary", "ps_polaroid", "ps_digicam", "ps_fantasy",
           "ps_fairytale", "ps_cyber", "ps_vaporwave", "ps_surreal"]
SF_KEYS = ["sf_none", "sf_extreme_cu", "sf_closeup", "sf_medium_cu", "sf_medium",
           "sf_cowboy", "sf_medium_full", "sf_full", "sf_wide"]
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
# category; PO_KEYS is derived from this map, sorted A-Z by English label.
PC_KEYS = ["pc_all", "pc_standing", "pc_walking", "pc_sitting", "pc_kneeling",
          "pc_lying", "pc_crouching", "pc_cute", "pc_social", "pc_props",
          "pc_sport"]
POSE_CATEGORIES = {
    "pc_standing": ["pose_arms_up", "pose_cross_arms", "pose_arms_open", "pose_back_camera",
            "pose_hair_both", "pose_hands_hips", "pose_chin_up", "pose_contrapposto",
            "pose_elegant", "pose_hand_collar", "pose_hand_hair", "pose_hand_hip",
            "pose_hands_back", "pose_arms_behind_head", "pose_hands_pocket",
            "pose_hands_nape", "pose_lean", "pose_railing", "pose_looking_away",
            "pose_over_shoulder", "pose_look_up", "pose_foot_kick", "pose_s_curve",
            "pose_stand", "pose_stretch", "pose_tiptoe"],
    "pc_walking": ["pose_candid", "pose_carefree_walk", "pose_dance", "pose_hair_flip",
            "pose_jump", "pose_look_back_walk", "pose_run", "pose_runway", "pose_skip",
            "pose_twirl", "pose_walk", "pose_walk_away", "pose_walk_toward",
            "pose_bag_strap"],
    "pc_sitting": ["pose_cross_leg", "pose_hug_knees", "pose_meditate", "pose_sit_side",
            "pose_sit", "pose_sit_chair_back", "pose_sit_floor_cross", "pose_sit_ledge",
            "pose_sit_stairs", "pose_sit_cheek_knee", "pose_sit_hold_ankle",
            "pose_legs_extended", "pose_sit_knee_up", "pose_w_sit", "pose_wariza_hands"],
    "pc_kneeling": ["pose_kneel", "pose_kneel_upright", "pose_kneel_hair", "pose_kneel_look_up",
            "pose_one_knee", "pose_seiza"],
    "pc_lying": ["pose_lying", "pose_lie_back_hair", "pose_lie_back_knee", "pose_lie_side",
            "pose_lie_stomach", "pose_lie_arm_pillow"],
    "pc_crouching": ["pose_bend_shoe", "pose_bend_knees", "pose_crouch", "pose_crouch_chin",
            "pose_crouch_look_back", "pose_lean_forward", "pose_squat"],
    "pc_cute": ["pose_big_heart", "pose_blow_kiss", "pose_bunny_ears", "pose_cat_paw",
            "pose_double_peace", "pose_finger_frame", "pose_finger_heart",
            "pose_fist_cheeks", "pose_flower_chin", "pose_gyaru_peace",
            "pose_hand_chin", "pose_cheek_hands", "pose_head_tilt", "pose_heart_hands",
            "pose_mini_heart", "pose_ok_sign", "pose_peace", "pose_peek_fingers",
            "pose_salute", "pose_please", "pose_point_camera", "pose_poke_cheek",
            "pose_rawr", "pose_shush", "pose_self_hug", "pose_sweater_paws",
            "pose_thumbs_up", "pose_hair_tuck", "pose_wave", "pose_wink", "pose_yawn"],
    "pc_social": ["pose_fix_jacket", "pose_adjust_glasses", "pose_phone_check", "pose_curtsy",
            "pose_editorial", "pose_high_fashion", "pose_coat_lapels", "pose_skirt_hem",
            "pose_mirror_selfie", "pose_reach_camera", "pose_selfie", "pose_shield_sun",
            "pose_hold_hat"],
    "pc_props": ["pose_touch_plants", "pose_bouquet", "pose_coffee", "pose_hold_camera",
            "pose_grass_stalk", "pose_umbrella", "pose_balloons", "pose_ear_wall",
            "pose_peek_tree", "pose_pick_flower", "pose_read_book", "pose_smell_flower",
            "pose_bicycle"],
    "pc_sport": ["pose_ballet", "pose_boxing", "pose_cartwheel", "pose_dribble", "pose_dynamic",
            "pose_skateboard", "pose_lunge", "pose_tennis_swing", "pose_yoga"],
}
PO_KEYS = ["pose_none"] + sorted(
    (k for keys in POSE_CATEGORIES.values() for k in keys),
    key=lambda k: TRANSLATIONS["en"][k].lower())


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
OSET_KEYS = ["os_none", "os_spr_frill_knit", "os_spr_floral_cami",
             "os_spr_floral_midi", "os_spr_ribbon_blouse", "os_spr_shirt_dress",
             "os_spr_lace_cami", "os_sum_linen", "os_sum_sundress",
             "os_sum_crop_denim", "os_sum_halter_maxi", "os_sum_gingham",
             "os_sum_resort", "os_aut_trench", "os_aut_corduroy", "os_aut_plaid",
             "os_aut_leather", "os_aut_knit_dress", "os_aut_blazer",
             "os_win_wool_coat", "os_win_puffer", "os_win_fur", "os_win_tweed",
             "os_win_overcoat", "os_win_cozy", "os_par_sequin", "os_par_satin_gown",
             "os_par_tulle", "os_par_velvet_suit", "os_par_lbd"]
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
                           "pose_selfie", "pose_phone_check"}
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
LANG_DEPENDENT_WIDGETS = list(PRESET_WIDGETS) + list(MULTI_WIDGETS) + ["w_theme"]

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


def reset_pose_on_category_change():
    """Pose category changed — the old pose may not be in the new pool."""
    st.session_state.pop("w_pose", None)


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
    roll = random.random()
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
        st.session_state["w_outfit_set"] = t(random.choice(OSET_KEYS[1:]))
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

        st.divider()
        st.caption("v5.8 — AI Prompt Generator")

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
                lb1, lb2 = st.columns([2, 1])
                with lb1:
                    st.selectbox(t("char_library"), list(library), key="w_char_lib")
                with lb2:
                    st.markdown("<div style='height:1.75rem'></div>", unsafe_allow_html=True)
                    st.button(f"📂 {t('char_load_btn')}", on_click=load_library_character,
                              use_container_width=True)
        st.markdown("---")

        # Reference photo checkbox (no file uploader — just a toggle)
        attach_subject = st.checkbox(t("attach_subject_photo"), key="attach_subject")
        if attach_subject:
            st.markdown(f'<div class="ref-attached">📎 {t("attach_subject_note")}</div>', unsafe_allow_html=True)

        def pick(keys, label_key, widget_key, index=0, **kw):
            """Selectbox over option keys → selected key (locked if part of the character)."""
            labels, _ = make_option(keys)
            sel = st.selectbox(t(label_key), labels, index=index, key=widget_key,
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
                        key=f"w_hair_p{pi}")
                    p_hr_key = p_hr_options[p_hr_labels.index(p_hr_sel)]
                with pc2:
                    p_hc_labels, _ = make_option(HC_KEYS)
                    p_hc_sel = st.selectbox(
                        t("hair_color"), p_hc_labels,
                        index=min(1 + 6 * (pi - 1), len(HC_KEYS) - 1),
                        key=f"w_hair_color_p{pi}")
                    p_hc_key = HC_KEYS[p_hc_labels.index(p_hc_sel)]
                with pc3:
                    p_ex_labels, _ = make_option(EX_KEYS)
                    p_ex_sel = st.selectbox(
                        t("expression"), p_ex_labels,
                        index=min(2 + 9 * (pi - 2), len(EX_KEYS) - 1),
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
        # Fashion presets (A-Z)
        fs_labels = [t(k) for k in FS_KEYS]
        fs_selected_labels = st.multiselect(t("fashion_presets"), fs_labels, default=[],
                                             help=t("fashion_presets_help"), key="fashion_multi")
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
            os_labels, _ = make_option(OSET_KEYS)
            os_sel = st.selectbox(t("outfit_set"), os_labels, index=1, key="w_outfit_set")
            os_key = OSET_KEYS[os_labels.index(os_sel)]
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
                                  on_change=reset_pose_on_category_change,
                                  disabled=attach_pose)
            pc_key = PC_KEYS[pc_labels.index(pc_sel)]
        with col_po:
            po_options = pose_keys_for_category(pc_key)
            po_labels, _ = make_option(po_options)
            if st.session_state.get("w_pose") not in po_labels:
                st.session_state.pop("w_pose", None)
            po_sel = st.selectbox(t("pose"), po_labels, key="w_pose", disabled=attach_pose)
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
                                        on_change=reset_location_on_category_change)
                lcat_key = LCAT_KEYS[lcat_labels.index(lcat_sel)]
            with col_lo:
                lo_options = loc_keys_for_category(lcat_key)
                lo_labels, _ = make_option(lo_options)
                if st.session_state.get("w_location") not in lo_labels:
                    st.session_state.pop("w_location", None)
                lo_sel = st.selectbox(t("location"), lo_labels, index=1, key="w_location")
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
            td_sel = st.selectbox(t("time_of_day"), td_labels, index=1, key="w_tod")
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
            lt_sel = st.selectbox(t("lighting"), lt_labels, index=1, key="w_lighting")
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
            sf_sel = st.selectbox(t("shot_framing"), sf_labels, index=2, key="w_framing")
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
            ps_sel = st.selectbox(t("picture_style"), ps_labels, key="w_pstyle")
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
        technical = ", ".join(specs)

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
            subject += ", the same recurring character with a consistent face and identity in every image"
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


if __name__ == "__main__":
    main()
