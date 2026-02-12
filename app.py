"""
=============================================================================
 Advanced AI Image Prompt Generator — Bilingual (Thai / English)
 Responsive design: iPhone · Android · iPad · Mac · PC
 v4.0 — Body Type, Appearance/Vibe, Editable Prompt Sections
=============================================================================
 Run    : streamlit run app.py
=============================================================================
"""

import html as html_mod
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
        "model_anime": "Anime / Illustration",
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
        "hair_style": "Hair Style",
        # Women's hairstyles
        "hair_long": "Long Flowing",
        "hair_straight": "Straight Long",
        "hair_loose_waves": "Loose Waves",
        "hair_curly": "Curly",
        "hair_wavy": "Wavy",
        "hair_bob": "Bob Cut",
        "hair_lob": "Long Bob / Lob",
        "hair_pixie": "Pixie Cut",
        "hair_ponytail": "Ponytail",
        "hair_high_ponytail": "High Ponytail",
        "hair_bun": "Bun",
        "hair_messy_bun": "Messy Bun",
        "hair_braids": "Braids",
        "hair_loose_braid": "Loose Braid",
        "hair_twin_braids": "Twin Braids",
        "hair_twintails": "Twin Tails",
        "hair_half_up": "Half Up Half Down",
        "hair_side_swept": "Side Swept",
        # Men's hairstyles
        "hair_short": "Short",
        "hair_undercut": "Undercut",
        "hair_slick_back": "Slicked Back",
        "hair_crew_cut": "Crew Cut",
        "hair_pompadour": "Pompadour",
        "hair_man_bun": "Man Bun",
        "hair_fade": "Fade",
        "hair_bald": "Bald / Shaved",
        "hair_color": "Hair Color",
        "hc_black": "Black",
        "hc_dark_brown": "Dark Brown",
        "hc_light_brown": "Light Brown",
        "hc_blonde": "Blonde",
        "hc_platinum": "Platinum Blonde",
        "hc_red": "Red / Auburn",
        "hc_ginger": "Ginger",
        "hc_silver": "Silver / Gray",
        "hc_white": "White",
        "hc_blue": "Blue",
        "hc_pink": "Pink",
        "hc_purple": "Purple / Lavender",
        "hc_green": "Green",
        "hc_ombre": "Ombre (dark to light)",
        "hc_highlights": "Highlights / Streaks",
        "bangs": "Bangs",
        "bangs_none": "None",
        "bangs_straight": "Straight Bangs",
        "bangs_side": "Side Bangs",
        "bangs_curtain": "Curtain Bangs",
        "bangs_wispy": "Wispy Bangs",
        "bangs_micro": "Micro Bangs",
        "expression": "Facial Expression",
        "expr_smile": "Gentle Smile",
        "expr_laugh": "Laughing",
        "expr_confident": "Confident",
        "expr_serious": "Serious / Stoic",
        "expr_neutral": "Neutral",
        "expr_pensive": "Pensive / Thoughtful",
        "expr_shy": "Shy / Bashful",
        "expr_surprised": "Surprised",
        "expr_sad": "Sad / Melancholic",
        "expr_angry": "Angry / Fierce",
        "expr_dreamy": "Dreamy",
        "expr_playful": "Playful",
        "expr_sultry": "Sultry",
        "expr_peaceful": "Peaceful / Serene",

        # ── Body Type ──
        "body_type": "Body Type",
        "bt_slim": "Slim / Slender",
        "bt_athletic": "Athletic / Fit",
        "bt_curvy": "Curvy",
        "bt_petite": "Petite",
        "bt_tall": "Tall / Model-like",
        "bt_average": "Average",

        # ── Appearance / Vibe ──
        "appearance": "Appearance / Vibe",
        "app_cute": "Cute / Adorable",
        "app_beautiful": "Beautiful / Gorgeous",
        "app_handsome": "Handsome / Charming",
        "app_cool": "Cool / Edgy",
        "app_elegant": "Elegant / Sophisticated",
        "app_sweet": "Sweet / Innocent",
        "app_fierce": "Fierce / Bold",
        "app_natural": "Natural / Fresh-faced",

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
        "fs_streetwear": "Streetwear / Urban",
        "fs_korean": "Korean Fashion (K-Style)",
        "fs_japanese": "Japanese Harajuku",
        "fs_minimalist": "Minimalist / Clean",
        "fs_bohemian": "Bohemian / Boho",
        "fs_vintage": "Vintage / Retro",
        "fs_gothic": "Gothic / Dark",
        "fs_preppy": "Preppy / Academic",
        "fs_athleisure": "Athleisure / Sporty",
        "fs_elegant": "Elegant / Formal",
        "fs_cottagecore": "Cottagecore / Pastoral",
        "fs_cyberpunk": "Cyberpunk / Techwear",
        "fs_y2k": "Y2K / 2000s Revival",
        "fs_old_money": "Old Money / Quiet Luxury",
        "fs_grunge": "Grunge / 90s",
        "top_garment": "Top",
        "top_tshirt": "T-Shirt",
        "top_crop": "Crop Top",
        "top_blouse": "Blouse",
        "top_button_shirt": "Button-up Shirt",
        "top_tank": "Tank Top",
        "top_sweater": "Sweater",
        "top_hoodie": "Hoodie",
        "top_polo": "Polo Shirt",
        "top_turtleneck": "Turtleneck",
        "top_off_shoulder": "Off-shoulder Top",
        "top_camisole": "Camisole",
        "top_cardigan": "Cardigan",
        "bottom_garment": "Bottom",
        "bot_jeans": "Jeans",
        "bot_mini_skirt": "Mini Skirt",
        "bot_maxi_skirt": "Maxi Skirt",
        "bot_pleated_skirt": "Pleated Skirt",
        "bot_shorts": "Shorts",
        "bot_wide_leg": "Wide-leg Pants",
        "bot_cargo": "Cargo Pants",
        "bot_leggings": "Leggings",
        "bot_pencil_skirt": "Pencil Skirt",
        "bot_a_line": "A-line Skirt",
        "bot_sweatpants": "Sweatpants",
        "bot_trousers": "Tailored Trousers",
        "attach_outfit_photo": "I will attach outfit reference photo",
        "attach_outfit_note": "Prompt will instruct AI to recreate the attached outfit",
        "fabric": "Fabric / Material",
        "fab_cotton": "Cotton",
        "fab_silk": "Silk",
        "fab_denim": "Denim",
        "fab_leather": "Leather",
        "fab_lace": "Lace",
        "fab_satin": "Satin",
        "fab_wool": "Wool Knit",
        "fab_sheer": "Sheer / Translucent",
        "color_palette": "Color Palette",
        "col_red": "Red",
        "col_pink": "Pink",
        "col_orange": "Orange",
        "col_yellow": "Yellow & Gold",
        "col_green": "Green",
        "col_blue": "Blue",
        "col_purple": "Purple & Lavender",
        "col_white": "White & Cream",
        "col_black": "All Black",
        "col_beige": "Beige & Nude",
        "col_pastel": "Pastel",
        "col_mono": "Monochrome",
        "col_earthy": "Earthy & Brown",
        "col_warm": "Warm Tones (red, orange, gold)",
        "col_cool": "Cool Tones (blue, teal, silver)",
        "col_vibrant": "Vibrant & Neon",

        # ── Accessories (checkboxes) ──
        "accessories": "Accessories (select all that apply)",
        "acc_group_head": "Head Accessories",
        "acc_group_body": "Body / Jewelry",
        "acc_group_carried": "Carried Items",
        "acc_beanie": "Beanie",
        "acc_beret": "Beret",
        "acc_cap": "Cap",
        "acc_glasses": "Prescription Glasses",
        "acc_hair_clip": "Hair Clip",
        "acc_hat": "Hat",
        "acc_headband": "Headband",
        "acc_sunglasses": "Sunglasses",
        "acc_tiara": "Tiara / Crown",
        "acc_bangle": "Bangle",
        "acc_belt": "Belt",
        "acc_bowtie": "Bow Tie",
        "acc_bracelet": "Bracelet",
        "acc_brooch": "Brooch",
        "acc_choker": "Choker",
        "acc_earrings": "Earrings",
        "acc_necktie": "Necktie",
        "acc_necklace": "Necklace",
        "acc_pendant": "Pendant",
        "acc_ring": "Ring",
        "acc_scarf": "Scarf",
        "acc_shawl": "Shawl",
        "acc_suspenders": "Suspenders",
        "acc_watch": "Watch",
        "acc_backpack": "Backpack",
        "acc_bag": "Handbag",
        "acc_bouquet": "Flower Bouquet",
        "acc_clutch": "Clutch Bag",
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
        "loc_street": "Urban Street",
        "loc_cafe": "Coffee Shop / Café",
        "loc_beach": "Beach / Seaside",
        "loc_forest": "Forest / Nature",
        "loc_rooftop": "Rooftop / Cityscape",
        "loc_room": "Indoor Room / Bedroom",
        "loc_temple": "Temple / Historic",
        "loc_garden": "Garden / Park",
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
        "lit_studio": "Studio Softbox",
        "lit_rim": "Rim / Backlit",
        "lit_neon": "Neon / Cyberpunk",
        "lit_candle": "Candlelight / Warm",
        "lit_dramatic": "Dramatic Chiaroscuro",
        "lit_flat": "Flat / Even",

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

        # ── Shot Framing (NEW) ──
        "shot_framing": "Shot Framing",
        "sf_extreme_cu": "Extreme Close-up (face only)",
        "sf_closeup": "Close-up (head & shoulders)",
        "sf_medium_cu": "Medium Close-up (chest up)",
        "sf_medium": "Medium Shot (waist up)",
        "sf_medium_full": "Medium Full (knees up)",
        "sf_full": "Full Body",
        "sf_wide": "Wide Shot (full body + environment)",

        # ── Camera Angle ──
        "camera_angle": "Camera Angle",
        "cam_eye": "Eye Level",
        "cam_low": "Low Angle (heroic)",
        "cam_high": "High Angle (overhead)",
        "cam_3q": "3/4 View",
        "cam_dutch": "Dutch Angle (tilted)",
        "cam_over_shoulder": "Over the Shoulder",
        "cam_bird": "Bird's Eye View",

        # ── Depth of Field (NEW) ──
        "dof": "Depth of Field / Background",
        "dof_sharp": "Everything Sharp (deep focus)",
        "dof_portrait": "Portrait Bokeh (f/1.8, subject sharp, background blurred)",
        "dof_shallow": "Shallow DOF (f/1.2, heavy bokeh, dreamy)",
        "dof_tiltshift": "Tilt-shift (miniature effect)",
        "dof_soft": "Soft / Dreamy Glow",

        # ── Pose ──
        "pose": "Action / Pose",
        "pose_stand": "Standing",
        "pose_sit": "Sitting",
        "pose_walk": "Walking",
        "pose_lean": "Leaning Against Wall",
        "pose_cross_arms": "Arms Crossed",
        "pose_hand_hair": "Hand in Hair",
        "pose_looking_away": "Looking Away",
        "pose_dynamic": "Dynamic / Action Pose",
        "pose_crouch": "Crouching",
        "pose_twirl": "Twirling",
        "pose_over_shoulder": "Looking Over Shoulder",
        "pose_run": "Running",
        "pose_jump": "Jumping",
        "pose_lying": "Lying Down",
        "pose_hand_chin": "Hand on Chin",
        "pose_hands_pocket": "Hands in Pockets",
        "pose_arms_up": "Arms Above Head",
        "pose_back_camera": "Back to Camera",

        # ── Advanced ──
        "exp_advanced": "Advanced & Technical",
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
        "model_anime": "อนิเมะ / ภาพวาด",
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
        "hair_style": "ทรงผม",
        # ทรงผมผู้หญิง
        "hair_long": "ยาวสลวย",
        "hair_straight": "ยาวตรง",
        "hair_loose_waves": "ลอนหลวม",
        "hair_curly": "หยิก",
        "hair_wavy": "หยักศก",
        "hair_bob": "บ็อบ",
        "hair_lob": "ลองบ็อบ",
        "hair_pixie": "พิกซี่",
        "hair_ponytail": "หางม้า",
        "hair_high_ponytail": "หางม้าสูง",
        "hair_bun": "มวยผม",
        "hair_messy_bun": "มวยผมหลวม",
        "hair_braids": "ถักเปีย",
        "hair_loose_braid": "ถักเปียหลวม",
        "hair_twin_braids": "ถักเปียสองข้าง",
        "hair_twintails": "มัดสองข้าง",
        "hair_half_up": "มัดครึ่ง",
        "hair_side_swept": "ปัดข้าง",
        # ทรงผมผู้ชาย
        "hair_short": "สั้น",
        "hair_undercut": "อันเดอร์คัท",
        "hair_slick_back": "เสยไปด้านหลัง",
        "hair_crew_cut": "ทรงนักเรียน",
        "hair_pompadour": "พอมปาดัวร์",
        "hair_man_bun": "มัดจุก",
        "hair_fade": "เฟด",
        "hair_bald": "โล้น / โกนผม",
        "hair_color": "สีผม",
        "hc_black": "ดำ",
        "hc_dark_brown": "น้ำตาลเข้ม",
        "hc_light_brown": "น้ำตาลอ่อน",
        "hc_blonde": "บลอนด์",
        "hc_platinum": "บลอนด์แพลตินั่ม",
        "hc_red": "แดง / ออเบิร์น",
        "hc_ginger": "จินเจอร์",
        "hc_silver": "เงิน / เทา",
        "hc_white": "ขาว",
        "hc_blue": "น้ำเงิน",
        "hc_pink": "ชมพู",
        "hc_purple": "ม่วง / ลาเวนเดอร์",
        "hc_green": "เขียว",
        "hc_ombre": "ออมเบร (เข้มไล่อ่อน)",
        "hc_highlights": "ไฮไลท์ / ทำเส้น",
        "bangs": "หน้าม้า",
        "bangs_none": "ไม่มี",
        "bangs_straight": "หน้าม้าตรง",
        "bangs_side": "หน้าม้าปัดข้าง",
        "bangs_curtain": "หน้าม้าม่าน",
        "bangs_wispy": "หน้าม้าบาง",
        "bangs_micro": "หน้าม้าสั้น",
        "expression": "สีหน้า / อารมณ์",
        "expr_smile": "ยิ้มอ่อน",
        "expr_laugh": "หัวเราะ",
        "expr_confident": "มั่นใจ",
        "expr_serious": "จริงจัง / เข้มขรึม",
        "expr_neutral": "เฉยๆ / ปกติ",
        "expr_pensive": "ครุ่นคิด",
        "expr_shy": "เขินอาย",
        "expr_surprised": "ตกใจ / ประหลาดใจ",
        "expr_sad": "เศร้า",
        "expr_angry": "โกรธ / ดุ",
        "expr_dreamy": "เหม่อฝัน",
        "expr_playful": "ขี้เล่น / ซุกซน",
        "expr_sultry": "เย้ายวน",
        "expr_peaceful": "สงบ / เยือกเย็น",

        # ── Body Type ──
        "body_type": "รูปร่าง",
        "bt_slim": "ผอมเพรียว",
        "bt_athletic": "กล้ามเนื้อ / ฟิต",
        "bt_curvy": "หุ่นโค้งเว้า",
        "bt_petite": "ตัวเล็กกะทัดรัด",
        "bt_tall": "สูง / หุ่นนางแบบ",
        "bt_average": "ปกติทั่วไป",

        # ── Appearance / Vibe ──
        "appearance": "ลุค / ไวบ์ภาพรวม",
        "app_cute": "น่ารัก / คิ้วท์",
        "app_beautiful": "สวยงาม / สวยหรู",
        "app_handsome": "หล่อ / มีเสน่ห์",
        "app_cool": "เท่ / คูล",
        "app_elegant": "สง่างาม / ดูแพง",
        "app_sweet": "หวาน / ใสซื่อ",
        "app_fierce": "ดุดัน / เข้มขรึม",
        "app_natural": "ธรรมชาติ / สดใส",

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
        "fs_streetwear": "สตรีทแวร์ / อเบอร์แบน",
        "fs_korean": "แฟชั่นเกาหลี (K-Style)",
        "fs_japanese": "ฮาราจูกุ ญี่ปุ่น",
        "fs_minimalist": "มินิมอล / สะอาดตา",
        "fs_bohemian": "โบฮีเมียน / โบโฮ",
        "fs_vintage": "วินเทจ / เรโทร",
        "fs_gothic": "โกธิค / ดาร์ค",
        "fs_preppy": "เพรปปี้ / นักเรียนอินเตอร์",
        "fs_athleisure": "แอธเลเชอร์ / สปอร์ต",
        "fs_elegant": "เอเลแกนท์ / ทางการ",
        "fs_cottagecore": "คอตเทจคอร์ / ชนบท",
        "fs_cyberpunk": "ไซเบอร์พังก์ / เทคแวร์",
        "fs_y2k": "Y2K / ยุค 2000",
        "fs_old_money": "Old Money / หรูเงียบๆ",
        "fs_grunge": "กรันจ์ / ยุค 90",
        "top_garment": "เสื้อ",
        "top_tshirt": "เสื้อยืด",
        "top_crop": "ครอปท็อป",
        "top_blouse": "เสื้อเบลาส์",
        "top_button_shirt": "เสื้อเชิ้ต",
        "top_tank": "เสื้อกล้าม",
        "top_sweater": "เสื้อสเวตเตอร์",
        "top_hoodie": "เสื้อฮู้ด",
        "top_polo": "เสื้อโปโล",
        "top_turtleneck": "เสื้อคอเต่า",
        "top_off_shoulder": "เสื้อเปิดไหล่",
        "top_camisole": "เสื้อสายเดี่ยว",
        "top_cardigan": "เสื้อคาร์ดิแกน",
        "bottom_garment": "ท่อนล่าง",
        "bot_jeans": "กางเกงยีนส์",
        "bot_mini_skirt": "กระโปรงสั้น",
        "bot_maxi_skirt": "กระโปรงยาว",
        "bot_pleated_skirt": "กระโปรงพลีท",
        "bot_shorts": "กางเกงขาสั้น",
        "bot_wide_leg": "กางเกงขาบาน",
        "bot_cargo": "กางเกงคาร์โก้",
        "bot_leggings": "เลกกิ้ง",
        "bot_pencil_skirt": "กระโปรงทรงดินสอ",
        "bot_a_line": "กระโปรงทรงเอ",
        "bot_sweatpants": "กางเกงวอร์ม",
        "bot_trousers": "กางเกงสแล็ค",
        "attach_outfit_photo": "จะแนบรูปชุดอ้างอิง",
        "attach_outfit_note": "พรอมต์จะสั่งให้ AI สร้างชุดตามรูปที่แนบ",
        "fabric": "ผ้า / วัสดุ",
        "fab_cotton": "ผ้าฝ้าย",
        "fab_silk": "ผ้าไหม",
        "fab_denim": "ผ้ายีนส์",
        "fab_leather": "หนัง",
        "fab_lace": "ลูกไม้",
        "fab_satin": "ผ้าซาติน",
        "fab_wool": "ผ้าขนสัตว์ถัก",
        "fab_sheer": "ผ้าบาง / โปร่ง",
        "color_palette": "โทนสี",
        "col_red": "แดง",
        "col_pink": "ชมพู",
        "col_orange": "ส้ม",
        "col_yellow": "เหลืองและทอง",
        "col_green": "เขียว",
        "col_blue": "น้ำเงิน",
        "col_purple": "ม่วงและลาเวนเดอร์",
        "col_white": "ขาวและครีม",
        "col_black": "ดำล้วน",
        "col_beige": "เบจและนู้ด",
        "col_pastel": "พาสเทล",
        "col_mono": "โมโนโครม",
        "col_earthy": "โทนดินและน้ำตาล",
        "col_warm": "โทนอุ่น (แดง, ส้ม, ทอง)",
        "col_cool": "โทนเย็น (น้ำเงิน, เขียวอมฟ้า, เงิน)",
        "col_vibrant": "สดใสและนีออน",

        # ── Accessories ──
        "accessories": "เครื่องประดับ (เลือกได้หลายอย่าง)",
        "acc_group_head": "เครื่องประดับศีรษะ",
        "acc_group_body": "เครื่องประดับร่างกาย / เครื่องเพชร",
        "acc_group_carried": "ของที่ถือ",
        "acc_beanie": "หมวกบีนนี่",
        "acc_beret": "หมวกเบเร่ต์",
        "acc_cap": "แก๊ป",
        "acc_glasses": "แว่นสายตา",
        "acc_hair_clip": "กิ๊บติดผม",
        "acc_hat": "หมวก",
        "acc_headband": "ที่คาดผม",
        "acc_sunglasses": "แว่นกันแดด",
        "acc_tiara": "มงกุฎ / เทียร่า",
        "acc_bangle": "กำไล",
        "acc_belt": "เข็มขัด",
        "acc_bowtie": "โบว์ไท",
        "acc_bracelet": "สร้อยข้อมือ",
        "acc_brooch": "เข็มกลัด",
        "acc_choker": "โชคเกอร์",
        "acc_earrings": "ต่างหู",
        "acc_necktie": "เนคไท",
        "acc_necklace": "สร้อยคอ",
        "acc_pendant": "จี้",
        "acc_ring": "แหวน",
        "acc_scarf": "ผ้าพันคอ",
        "acc_shawl": "ผ้าคลุมไหล่",
        "acc_suspenders": "สายเอี๊ยม",
        "acc_watch": "นาฬิกา",
        "acc_backpack": "เป้สะพายหลัง",
        "acc_bag": "กระเป๋าถือ",
        "acc_bouquet": "ช่อดอกไม้",
        "acc_clutch": "กระเป๋าคลัตช์",
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
        "loc_street": "ถนนในเมือง",
        "loc_cafe": "ร้านกาแฟ / คาเฟ่",
        "loc_beach": "ชายหาด / ทะเล",
        "loc_forest": "ป่า / ธรรมชาติ",
        "loc_rooftop": "ดาดฟ้า / วิวเมือง",
        "loc_room": "ห้อง / ห้องนอน",
        "loc_temple": "วัด / สถานที่ประวัติศาสตร์",
        "loc_garden": "สวน / สวนสาธารณะ",
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
        "lit_studio": "ซอฟต์บ็อกซ์สตูดิโอ",
        "lit_rim": "แสงขอบ / แบ็คไลท์",
        "lit_neon": "นีออน / ไซเบอร์พังก์",
        "lit_candle": "แสงเทียน / อบอุ่น",
        "lit_dramatic": "ดราม่า เคียโรสกูโร",
        "lit_flat": "แสงเรียบ / สม่ำเสมอ",

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

        # ── Shot Framing ──
        "shot_framing": "ระยะภาพ / เฟรมมิ่ง",
        "sf_extreme_cu": "โคลสอัพมาก (ใบหน้าอย่างเดียว)",
        "sf_closeup": "โคลสอัพ (ศีรษะและไหล่)",
        "sf_medium_cu": "มีเดียมโคลสอัพ (หน้าอกขึ้นไป)",
        "sf_medium": "ภาพครึ่งตัว (เอวขึ้นไป)",
        "sf_medium_full": "ภาพเกือบเต็มตัว (เข่าขึ้นไป)",
        "sf_full": "ภาพเต็มตัว",
        "sf_wide": "ภาพกว้าง (เต็มตัว + สิ่งแวดล้อม)",

        # ── Camera Angle ──
        "camera_angle": "มุมกล้อง",
        "cam_eye": "ระดับสายตา",
        "cam_low": "มุมต่ำ (ดูยิ่งใหญ่)",
        "cam_high": "มุมสูง (มองลง)",
        "cam_3q": "มุม 3/4",
        "cam_dutch": "มุมเอียง (Dutch Angle)",
        "cam_over_shoulder": "มองข้ามไหล่",
        "cam_bird": "มุมมองจากบน (Bird's Eye)",

        # ── Depth of Field ──
        "dof": "ความชัดลึก / พื้นหลัง",
        "dof_sharp": "ชัดทั้งภาพ (Deep Focus)",
        "dof_portrait": "หน้าชัดหลังเบลอ (Portrait f/1.8)",
        "dof_shallow": "เบลอหนักมาก (f/1.2, โบเก้ฝัน)",
        "dof_tiltshift": "Tilt-shift (เหมือนโมเดลจิ๋ว)",
        "dof_soft": "นุ่มนวล / เรืองแสง (Dreamy)",

        # ── Pose ──
        "pose": "ท่าโพส / แอคชั่น",
        "pose_stand": "ยืน",
        "pose_sit": "นั่ง",
        "pose_walk": "เดิน",
        "pose_lean": "พิงกำแพง",
        "pose_cross_arms": "กอดอก",
        "pose_hand_hair": "มือจับผม",
        "pose_looking_away": "มองไปทางอื่น",
        "pose_dynamic": "ท่าไดนามิก / แอคชั่น",
        "pose_crouch": "นั่งยอง",
        "pose_twirl": "หมุนตัว",
        "pose_over_shoulder": "เหลียวมองข้ามไหล่",
        "pose_run": "วิ่ง",
        "pose_jump": "กระโดด",
        "pose_lying": "นอน",
        "pose_hand_chin": "มือจับคาง",
        "pose_hands_pocket": "มือในกระเป๋า",
        "pose_arms_up": "ยกแขนเหนือศีรษะ",
        "pose_back_camera": "หันหลังให้กล้อง",

        # ── Advanced ──
        "exp_advanced": "ขั้นสูงและเทคนิค",
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
    "hair_wavy": "wavy hair", "hair_bob": "bob cut",
    "hair_lob": "long bob lob hairstyle", "hair_pixie": "pixie cut",
    "hair_ponytail": "ponytail", "hair_high_ponytail": "high ponytail",
    "hair_bun": "hair bun", "hair_messy_bun": "messy bun",
    "hair_braids": "braids", "hair_loose_braid": "loose braid",
    "hair_twin_braids": "twin braids", "hair_twintails": "twin tails",
    "hair_half_up": "half up half down hairstyle", "hair_side_swept": "side swept hair",
    # Hair Style — Men's
    "hair_short": "short hair", "hair_undercut": "undercut hairstyle",
    "hair_slick_back": "slicked back hair", "hair_crew_cut": "crew cut",
    "hair_pompadour": "pompadour hairstyle", "hair_man_bun": "man bun",
    "hair_fade": "fade haircut", "hair_bald": "bald head",
    # Hair Color
    "hc_black": "black hair", "hc_dark_brown": "dark brown hair",
    "hc_light_brown": "light brown hair", "hc_blonde": "blonde hair",
    "hc_platinum": "platinum blonde hair", "hc_red": "red auburn hair",
    "hc_ginger": "ginger hair", "hc_silver": "silver gray hair",
    "hc_white": "white hair", "hc_blue": "blue hair",
    "hc_pink": "pink hair", "hc_purple": "purple lavender hair",
    "hc_green": "green hair", "hc_ombre": "ombre hair transitioning dark to light",
    "hc_highlights": "hair with highlights and streaks",
    # Bangs
    "bangs_none": "", "bangs_straight": "with straight bangs",
    "bangs_side": "with side-swept bangs", "bangs_curtain": "with curtain bangs",
    "bangs_wispy": "with wispy bangs", "bangs_micro": "with micro bangs",
    # Expression
    "expr_smile": "gentle smile", "expr_laugh": "laughing joyfully",
    "expr_confident": "confident expression", "expr_serious": "serious stoic expression",
    "expr_neutral": "neutral expression", "expr_pensive": "pensive thoughtful expression",
    "expr_shy": "shy bashful expression", "expr_surprised": "surprised expression",
    "expr_sad": "sad melancholic expression", "expr_angry": "angry fierce expression",
    "expr_dreamy": "dreamy wistful expression", "expr_playful": "playful mischievous expression",
    "expr_sultry": "sultry seductive expression", "expr_peaceful": "peaceful serene expression",
    # Body Type
    "bt_slim": "slim slender body", "bt_athletic": "athletic fit toned body",
    "bt_curvy": "curvy body with feminine proportions", "bt_petite": "petite small body frame",
    "bt_tall": "tall model-like body proportions", "bt_average": "average body build",
    # Appearance / Vibe
    "app_cute": "cute adorable baby-faced features",
    "app_beautiful": "beautiful gorgeous striking features",
    "app_handsome": "handsome chiseled jawline and sharp features",
    "app_cool": "cool edgy sharp features with confident attitude",
    "app_elegant": "elegant sophisticated refined features",
    "app_sweet": "sweet innocent youthful features",
    "app_fierce": "fierce bold intense striking features",
    "app_natural": "natural fresh-faced dewy skin look",
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
    # Fabric
    "fab_cotton": "cotton fabric", "fab_silk": "silk fabric",
    "fab_denim": "denim", "fab_leather": "leather",
    "fab_lace": "lace fabric", "fab_satin": "satin fabric",
    "fab_wool": "wool knit", "fab_sheer": "sheer translucent fabric",
    # Top Garment
    "top_tshirt": "wearing a t-shirt", "top_crop": "wearing a crop top",
    "top_blouse": "wearing a blouse", "top_button_shirt": "wearing a button-up shirt",
    "top_tank": "wearing a tank top", "top_sweater": "wearing a sweater",
    "top_hoodie": "wearing a hoodie", "top_polo": "wearing a polo shirt",
    "top_turtleneck": "wearing a turtleneck", "top_off_shoulder": "wearing an off-shoulder top",
    "top_camisole": "wearing a camisole", "top_cardigan": "wearing a cardigan",
    # Bottom Garment
    "bot_jeans": "wearing jeans", "bot_mini_skirt": "wearing a mini skirt",
    "bot_maxi_skirt": "wearing a maxi skirt", "bot_pleated_skirt": "wearing a pleated skirt",
    "bot_shorts": "wearing shorts", "bot_wide_leg": "wearing wide-leg pants",
    "bot_cargo": "wearing cargo pants", "bot_leggings": "wearing leggings",
    "bot_pencil_skirt": "wearing a pencil skirt", "bot_a_line": "wearing an A-line skirt",
    "bot_sweatpants": "wearing sweatpants", "bot_trousers": "wearing tailored trousers",
    # Color Palette
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
    # Accessories — Head
    "acc_beanie": "wearing a beanie",
    "acc_beret": "wearing a beret",
    "acc_cap": "wearing a cap",
    "acc_glasses": "wearing prescription glasses",
    "acc_hair_clip": "wearing a hair clip",
    "acc_hat": "wearing a hat",
    "acc_headband": "wearing a headband",
    "acc_sunglasses": "wearing stylish sunglasses",
    "acc_tiara": "wearing a tiara",
    # Accessories — Body / Jewelry
    "acc_bangle": "wearing a bangle",
    "acc_belt": "wearing a belt",
    "acc_bowtie": "wearing a bow tie",
    "acc_bracelet": "wearing a bracelet",
    "acc_brooch": "wearing a brooch",
    "acc_choker": "wearing a choker",
    "acc_earrings": "wearing earrings",
    "acc_necktie": "wearing a necktie",
    "acc_necklace": "wearing a necklace",
    "acc_pendant": "wearing a pendant",
    "acc_ring": "wearing a ring",
    "acc_scarf": "wearing a scarf",
    "acc_shawl": "wearing a shawl",
    "acc_suspenders": "wearing suspenders",
    "acc_watch": "wearing a wristwatch",
    # Accessories — Carried Items
    "acc_backpack": "carrying a backpack",
    "acc_bag": "carrying a handbag",
    "acc_bouquet": "holding a flower bouquet",
    "acc_clutch": "carrying a clutch bag",
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
    "lit_rim": "dramatic rim lighting from behind",
    "lit_neon": "colorful neon lights with cyberpunk atmosphere",
    "lit_candle": "warm candlelight illumination",
    "lit_dramatic": "dramatic chiaroscuro lighting with deep shadows",
    "lit_flat": "flat even lighting",
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
    # Shot Framing
    "sf_extreme_cu": "extreme close-up of face only",
    "sf_closeup": "close-up portrait shot showing head and shoulders",
    "sf_medium_cu": "medium close-up from chest up",
    "sf_medium": "medium shot from waist up",
    "sf_medium_full": "medium full shot from knees up",
    "sf_full": "full body shot",
    "sf_wide": "wide shot showing full body and surrounding environment",
    # Camera Angle
    "cam_eye": "shot at eye level", "cam_low": "shot from low angle looking up",
    "cam_high": "shot from high angle looking down",
    "cam_3q": "three-quarter view", "cam_dutch": "dutch angle tilted composition",
    "cam_over_shoulder": "over-the-shoulder shot", "cam_bird": "bird's eye view from directly above",
    # Depth of Field
    "dof_sharp": "deep focus with everything sharp",
    "dof_portrait": "shallow depth of field at f/1.8 with subject in sharp focus and beautifully blurred bokeh background",
    "dof_shallow": "very shallow depth of field at f/1.2 with heavy creamy bokeh and dreamy atmosphere",
    "dof_tiltshift": "tilt-shift effect creating miniature model appearance",
    "dof_soft": "soft dreamy glow with gentle diffusion",
    # Pose
    "pose_stand": "standing elegantly", "pose_sit": "sitting comfortably",
    "pose_walk": "walking naturally", "pose_lean": "leaning against a wall",
    "pose_cross_arms": "with arms crossed", "pose_hand_hair": "with hand running through hair",
    "pose_looking_away": "looking away from camera", "pose_dynamic": "in a dynamic action pose",
    "pose_crouch": "crouching down", "pose_twirl": "twirling with movement in clothing",
    "pose_over_shoulder": "looking back over shoulder", "pose_run": "running in motion",
    "pose_jump": "jumping in the air", "pose_lying": "lying down relaxed",
    "pose_hand_chin": "resting chin on hand thoughtfully",
    "pose_hands_pocket": "with hands in pockets casually",
    "pose_arms_up": "with arms raised above head",
    "pose_back_camera": "facing away from camera showing back",
    # Model Type
    "model_realistic": "Photorealistic", "model_anime": "Anime illustration style",
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
}
@media (min-width: 1400px) {
    .block-container { max-width: 1200px !important; margin: 0 auto !important; }
}
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
    border-left: 4px solid #00897b; padding: 10px 14px; border-radius: 8px; margin: 8px 0; font-size: 0.9rem; }
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
        st.divider()

        ar_keys = ["ar_1_1", "ar_16_9", "ar_9_16", "ar_4_5",
                   "ar_3_2", "ar_2_3", "ar_4_3", "ar_3_4",
                   "ar_iphone", "ar_android"]
        ar_labels, _ = make_option(ar_keys)
        ar_idx = st.selectbox(t("aspect_ratio"), ar_labels, index=0)
        ar_selected_key = ar_keys[ar_labels.index(ar_idx)]

        mt_keys = ["model_realistic", "model_anime", "model_3d"]
        mt_labels, _ = make_option(mt_keys)
        mt_idx = st.selectbox(t("model_type"), mt_labels, index=0)
        mt_selected_key = mt_keys[mt_labels.index(mt_idx)]

        st.divider()
        st.caption("v4.0 — AI Prompt Generator")

    # ── Header ───────────────────────────────────────────────────────────
    st.markdown(f"## {t('app_title')}")
    st.caption(t("app_subtitle"))

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
            gd_keys = ["gender_female", "gender_male", "gender_nb"]
            gd_labels, _ = make_option(gd_keys)
            gd_sel = st.selectbox(t("gender"), gd_labels)
            gd_key = gd_keys[gd_labels.index(gd_sel)]
        with col2:
            ag_keys = ["age_20_25", "age_5_9", "age_10_14", "age_15_19",
                        "age_26_35", "age_36_45", "age_46_60", "age_60plus"]
            ag_labels, _ = make_option(ag_keys)
            ag_sel = st.selectbox(t("age_group"), ag_labels)
            ag_key = ag_keys[ag_labels.index(ag_sel)]
        with col3:
            et_keys = ["eth_asian", "eth_se_asian", "eth_south_asian", "eth_european",
                        "eth_african", "eth_latin", "eth_middle_east", "eth_mixed"]
            et_labels, _ = make_option(et_keys)
            et_sel = st.selectbox(t("ethnicity"), et_labels)
            et_key = et_keys[et_labels.index(et_sel)]

        col4, col5 = st.columns(2)
        with col4:
            hr_keys = [
                # Women's hairstyles
                "hair_long", "hair_straight", "hair_loose_waves",
                "hair_curly", "hair_wavy", "hair_bob", "hair_lob", "hair_pixie",
                "hair_ponytail", "hair_high_ponytail", "hair_bun", "hair_messy_bun",
                "hair_braids", "hair_loose_braid", "hair_twin_braids", "hair_twintails",
                "hair_half_up", "hair_side_swept",
                # Men's hairstyles
                "hair_short", "hair_undercut", "hair_slick_back", "hair_crew_cut",
                "hair_pompadour", "hair_man_bun", "hair_fade", "hair_bald",
            ]
            hr_labels, _ = make_option(hr_keys)
            hr_sel = st.selectbox(t("hair_style"), hr_labels)
            hr_key = hr_keys[hr_labels.index(hr_sel)]
        with col5:
            hc_keys = ["hc_black", "hc_dark_brown", "hc_light_brown", "hc_blonde",
                        "hc_platinum", "hc_red", "hc_ginger", "hc_silver", "hc_white",
                        "hc_blue", "hc_pink", "hc_purple", "hc_green",
                        "hc_ombre", "hc_highlights"]
            hc_labels, _ = make_option(hc_keys)
            hc_sel = st.selectbox(t("hair_color"), hc_labels)
            hc_key = hc_keys[hc_labels.index(hc_sel)]

        col_bn, col_ex = st.columns(2)
        with col_bn:
            bn_keys = ["bangs_none", "bangs_straight", "bangs_side",
                        "bangs_curtain", "bangs_wispy", "bangs_micro"]
            bn_labels, _ = make_option(bn_keys)
            bn_sel = st.selectbox(t("bangs"), bn_labels)
            bn_key = bn_keys[bn_labels.index(bn_sel)]
        with col_ex:
            ex_keys = ["expr_smile", "expr_laugh", "expr_confident",
                        "expr_serious", "expr_neutral", "expr_pensive",
                        "expr_shy", "expr_surprised", "expr_sad", "expr_angry",
                        "expr_dreamy", "expr_playful", "expr_sultry", "expr_peaceful"]
            ex_labels, _ = make_option(ex_keys)
            ex_sel = st.selectbox(t("expression"), ex_labels)
            ex_key = ex_keys[ex_labels.index(ex_sel)]

        col7, _ = st.columns(2)
        with col7:
            skin_check = st.checkbox(t("skin_detail"))

        col_bt, col_ap = st.columns(2)
        with col_bt:
            bt_keys = ["bt_slim", "bt_athletic", "bt_curvy", "bt_petite",
                        "bt_tall", "bt_average"]
            bt_labels, _ = make_option(bt_keys)
            bt_sel = st.selectbox(t("body_type"), bt_labels)
            bt_key = bt_keys[bt_labels.index(bt_sel)]
        with col_ap:
            ap_keys = ["app_cute", "app_beautiful", "app_handsome", "app_cool",
                        "app_elegant", "app_sweet", "app_fierce", "app_natural"]
            ap_labels, _ = make_option(ap_keys)
            ap_sel = st.selectbox(t("appearance"), ap_labels)
            ap_key = ap_keys[ap_labels.index(ap_sel)]

    # ══════════════════════════════════════════════════════════════════════
    #  EXPANDER 2 — Outfit & Style
    # ══════════════════════════════════════════════════════════════════════
    with st.expander(f"👗  {t('exp_outfit')}", expanded=True):
        # Fashion presets
        fs_keys = ["fs_streetwear", "fs_korean", "fs_japanese", "fs_minimalist",
                    "fs_bohemian", "fs_vintage", "fs_gothic", "fs_preppy",
                    "fs_athleisure", "fs_elegant", "fs_cottagecore", "fs_cyberpunk",
                    "fs_y2k", "fs_old_money", "fs_grunge"]
        fs_labels = [t(k) for k in fs_keys]
        fs_selected_labels = st.multiselect(t("fashion_presets"), fs_labels, default=[],
                                             help=t("fashion_presets_help"), key="fashion_multi")
        fs_selected_keys = [fs_keys[fs_labels.index(lbl)] for lbl in fs_selected_labels]

        st.markdown("---")

        # ── Top & Bottom garment selectors ──
        col_top, col_bot = st.columns(2)
        with col_top:
            top_keys = ["top_tshirt", "top_crop", "top_blouse", "top_button_shirt",
                         "top_tank", "top_sweater", "top_hoodie", "top_polo",
                         "top_turtleneck", "top_off_shoulder", "top_camisole", "top_cardigan"]
            top_labels, _ = make_option(top_keys)
            top_sel = st.selectbox(t("top_garment"), top_labels)
            top_key = top_keys[top_labels.index(top_sel)]
        with col_bot:
            bot_keys = ["bot_jeans", "bot_mini_skirt", "bot_maxi_skirt", "bot_pleated_skirt",
                         "bot_shorts", "bot_wide_leg", "bot_cargo", "bot_leggings",
                         "bot_pencil_skirt", "bot_a_line", "bot_sweatpants", "bot_trousers"]
            bot_labels, _ = make_option(bot_keys)
            bot_sel = st.selectbox(t("bottom_garment"), bot_labels)
            bot_key = bot_keys[bot_labels.index(bot_sel)]

        st.markdown("---")
        outfit_text = st.text_input(t("outfit_input"), placeholder=t("outfit_placeholder"))

        # Outfit reference checkbox
        attach_outfit = st.checkbox(t("attach_outfit_photo"), key="attach_outfit")
        if attach_outfit:
            st.markdown(f'<div class="ref-attached">📎 {t("attach_outfit_note")}</div>', unsafe_allow_html=True)

        st.markdown("---")
        col8, col9 = st.columns(2)
        with col8:
            fb_keys = ["fab_cotton", "fab_silk", "fab_denim", "fab_leather",
                        "fab_lace", "fab_satin", "fab_wool", "fab_sheer"]
            fb_labels, _ = make_option(fb_keys)
            fb_sel = st.selectbox(t("fabric"), fb_labels)
            fb_key = fb_keys[fb_labels.index(fb_sel)]
        with col9:
            cp_keys = ["col_red", "col_pink", "col_orange", "col_yellow",
                        "col_green", "col_blue", "col_purple", "col_white",
                        "col_black", "col_beige", "col_pastel", "col_mono",
                        "col_earthy", "col_warm", "col_cool", "col_vibrant"]
            cp_labels, _ = make_option(cp_keys)
            cp_sel = st.selectbox(t("color_palette"), cp_labels)
            cp_key = cp_keys[cp_labels.index(cp_sel)]

        # ── Accessories: grouped checkboxes ──
        st.markdown(f"**{t('accessories')}**")
        acc_selected = []

        acc_head_keys = ["acc_beanie", "acc_beret", "acc_cap", "acc_glasses",
                         "acc_hair_clip", "acc_hat", "acc_headband",
                         "acc_sunglasses", "acc_tiara"]
        acc_body_keys = ["acc_bangle", "acc_belt", "acc_bowtie", "acc_bracelet",
                         "acc_brooch", "acc_choker", "acc_earrings", "acc_necktie",
                         "acc_necklace", "acc_pendant", "acc_ring", "acc_scarf",
                         "acc_shawl", "acc_suspenders", "acc_watch"]
        acc_carried_keys = ["acc_backpack", "acc_bag", "acc_bouquet",
                            "acc_clutch", "acc_umbrella"]

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
            lo_keys = ["loc_studio", "loc_street", "loc_cafe", "loc_beach",
                        "loc_forest", "loc_rooftop", "loc_room", "loc_temple", "loc_garden"]
            lo_labels, _ = make_option(lo_keys)
            lo_sel = st.selectbox(t("location"), lo_labels)
            lo_key = lo_keys[lo_labels.index(lo_sel)]
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
            td_keys = ["tod_golden", "tod_blue", "tod_noon", "tod_night", "tod_overcast", "tod_sunrise"]
            td_labels, _ = make_option(td_keys)
            td_sel = st.selectbox(t("time_of_day"), td_labels)
            td_key = td_keys[td_labels.index(td_sel)]
        with col11:
            lt_keys = ["lit_natural", "lit_studio", "lit_rim", "lit_neon",
                        "lit_candle", "lit_dramatic", "lit_flat"]
            lt_labels, _ = make_option(lt_keys)
            lt_sel = st.selectbox(t("lighting"), lt_labels)
            lt_key = lt_keys[lt_labels.index(lt_sel)]
        with col_season:
            sn_keys = ["season_none", "season_spring", "season_summer",
                        "season_autumn", "season_winter", "season_rainy"]
            sn_labels, _ = make_option(sn_keys)
            sn_sel = st.selectbox(t("season"), sn_labels)
            sn_key = sn_keys[sn_labels.index(sn_sel)]
            weather_rain = st.checkbox(t("weather_rain"), key="weather_rain_cb")
            weather_snow = st.checkbox(t("weather_snow"), key="weather_snow_cb")
            weather_leaves = st.checkbox(t("weather_leaves"), key="weather_leaves_cb")
        with col_ps:
            ps_keys = ["ps_none", "ps_dreamy", "ps_soft", "ps_vivid", "ps_bw",
                        "ps_vintage", "ps_cinematic", "ps_moody", "ps_pastel",
                        "ps_hdr", "ps_matte"]
            ps_labels, _ = make_option(ps_keys)
            ps_sel = st.selectbox(t("picture_style"), ps_labels)
            ps_key = ps_keys[ps_labels.index(ps_sel)]

        st.markdown("---")

        # ── Shot Framing + Camera Angle + DOF ──
        col12, col13 = st.columns(2)
        with col12:
            sf_keys = ["sf_extreme_cu", "sf_closeup", "sf_medium_cu", "sf_medium",
                        "sf_medium_full", "sf_full", "sf_wide"]
            sf_labels, _ = make_option(sf_keys)
            sf_sel = st.selectbox(t("shot_framing"), sf_labels, index=1)
            sf_key = sf_keys[sf_labels.index(sf_sel)]
        with col13:
            ca_keys = ["cam_eye", "cam_low", "cam_high", "cam_3q",
                        "cam_dutch", "cam_over_shoulder", "cam_bird"]
            ca_labels, _ = make_option(ca_keys)
            ca_sel = st.selectbox(t("camera_angle"), ca_labels)
            ca_key = ca_keys[ca_labels.index(ca_sel)]

        col14, col15 = st.columns(2)
        with col14:
            dof_keys = ["dof_sharp", "dof_portrait", "dof_shallow", "dof_tiltshift", "dof_soft"]
            dof_labels, _ = make_option(dof_keys)
            dof_sel = st.selectbox(t("dof"), dof_labels, index=1)
            dof_key = dof_keys[dof_labels.index(dof_sel)]
        with col15:
            po_keys = ["pose_stand", "pose_sit", "pose_walk", "pose_lean",
                        "pose_cross_arms", "pose_hand_hair", "pose_looking_away", "pose_dynamic",
                        "pose_crouch", "pose_twirl", "pose_over_shoulder", "pose_run",
                        "pose_jump", "pose_lying", "pose_hand_chin", "pose_hands_pocket",
                        "pose_arms_up", "pose_back_camera"]
            po_labels, _ = make_option(po_keys)
            po_sel = st.selectbox(t("pose"), po_labels)
            po_key = po_keys[po_labels.index(po_sel)]

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

    # ══════════════════════════════════════════════════════════════════════
    #  6. GENERATE
    # ══════════════════════════════════════════════════════════════════════
    st.markdown("")
    gen_col, _ = st.columns([1, 2])
    with gen_col:
        generate_clicked = st.button(f"🚀  {t('generate_btn')}", type="primary", use_container_width=True)

    st.markdown("---")
    st.markdown(f"### {t('result_header')}")

    if generate_clicked:
        # ── Build each section ──
        # Technical
        specs = [eng(mt_selected_key), "shot on 35mm lens"]
        for qk in qt_selected:
            specs.append(eng(qk))
        technical = ", ".join(specs)

        # Subject (with body type + appearance)
        bangs_text = eng(bn_key)
        bangs_part = f", {bangs_text}" if bangs_text else ""
        if attach_subject:
            subject = (f"a photo of the uploaded person, {eng(bt_key)}, {eng(ap_key)}, "
                       f"with {eng(hr_key)}, {eng(hc_key)}{bangs_part}, "
                       f"and {eng(ex_key)}")
        else:
            subject = (f"a {eng(ag_key)} {eng(et_key)} {eng(gd_key)}, "
                       f"{eng(bt_key)}, {eng(ap_key)}, "
                       f"with {eng(hr_key)}, {eng(hc_key)}{bangs_part}, "
                       f"and {eng(ex_key)}")
        if skin_check:
            subject += ", with ultra-realistic skin texture showing pores and fine details"

        # Outfit
        outfit_parts = []
        for fk in fs_selected_keys:
            v = eng(fk)
            if v:
                outfit_parts.append(v)
        outfit_parts.append(eng(top_key))
        outfit_parts.append(eng(bot_key))
        if outfit_text.strip():
            outfit_parts.append(f"wearing {translate_to_english(outfit_text)}")
        if attach_outfit:
            outfit_parts.append("wearing the outfit shown in the attached outfit reference image")
        outfit_parts.append(f"made of {eng(fb_key)}")
        outfit_parts.append(f"in {eng(cp_key)}")
        for ak in acc_selected:
            v = eng(ak)
            if v:
                outfit_parts.append(v)
        outfit = ", ".join(outfit_parts)

        # Pose
        pose = eng(po_key)

        # Environment
        if attach_scene:
            env_loc = "in the location shown in the attached scene reference image"
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

        # Camera & Lighting + Picture Style
        camera_parts = [eng(lt_key), eng(sf_key), eng(ca_key), eng(dof_key)]
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

        # ── Store each section in session_state (using widget keys) ──
        st.session_state["ta_technical"] = technical
        st.session_state["ta_subject"] = subject
        st.session_state["ta_outfit"] = outfit
        st.session_state["ta_pose"] = pose
        st.session_state["ta_environment"] = environment
        st.session_state["ta_camera"] = camera_section
        st.session_state["ta_custom"] = custom_eng
        st.session_state["ed_negative"] = negative_eng
        st.session_state["sec_ar"] = eng(ar_selected_key)
        st.session_state["ref_notes"] = ref_notes
        st.session_state["prompt_generated"] = True

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
        all_parts = [ed_tech, ed_subj, ed_outfit, ed_pose, ed_env, ed_cam]
        if ed_custom.strip():
            all_parts.append(ed_custom)
        if ar_val:
            all_parts.append(ar_val)
        combined_prompt = ", ".join(s.strip() for s in all_parts if s.strip())

        st.markdown("---")
        st.markdown(f"### 📋 {t('section_final')}")
        st.code(combined_prompt, language=None)

        # Copy button — use components.html so JS actually executes
        safe_prompt = html_mod.escape(combined_prompt).replace("`", "\\`").replace("${", "\\${")
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
            const text = `{safe_prompt}`;
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
        components.html(copy_html, height=60)

        # Negative prompt
        ed_neg = st.session_state.get("ed_negative", "")
        if ed_neg:
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


if __name__ == "__main__":
    main()
