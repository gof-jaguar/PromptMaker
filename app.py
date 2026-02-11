"""
=============================================================================
 Advanced AI Image Prompt Generator — Bilingual (Thai / English)
 Responsive design: iPhone · Android · iPad · Mac · PC
 v4.0 — Body Type, Appearance/Vibe, Editable Prompt Sections
=============================================================================
 Run    : streamlit run app.py
=============================================================================
"""

import streamlit as st

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
        "age_child": "Child (5-12)",
        "age_teen": "Teenager (13-19)",
        "age_young": "Young Adult (20-30)",
        "age_mid": "Middle-aged (31-50)",
        "age_senior": "Senior (50+)",
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
        "hair_long": "Long Flowing",
        "hair_short": "Short",
        "hair_curly": "Curly",
        "hair_wavy": "Wavy",
        "hair_ponytail": "Ponytail",
        "hair_bun": "Bun",
        "hair_braids": "Braids",
        "hair_twintails": "Twin Tails",
        "hair_bob": "Bob Cut",
        "hair_pixie": "Pixie Cut",
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
        "expression": "Facial Expression",
        "expr_smile": "Gentle Smile",
        "expr_serious": "Serious / Stoic",
        "expr_laugh": "Laughing",
        "expr_pensive": "Pensive / Thoughtful",
        "expr_confident": "Confident",
        "expr_neutral": "Neutral",

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
        "col_warm": "Warm Tones (red, orange, gold)",
        "col_cool": "Cool Tones (blue, teal, silver)",
        "col_pastel": "Pastels",
        "col_mono": "Monochrome / Black & White",
        "col_earthy": "Earthy / Natural",
        "col_vibrant": "Vibrant / Neon",

        # ── Accessories (checkboxes) ──
        "accessories": "Accessories (select all that apply)",
        "acc_glasses": "Prescription Glasses",
        "acc_sunglasses": "Sunglasses",
        "acc_earrings": "Earrings",
        "acc_necklace": "Necklace / Pendant",
        "acc_choker": "Choker",
        "acc_bracelet": "Bracelet / Bangle",
        "acc_watch": "Watch",
        "acc_ring": "Ring(s)",
        "acc_hat": "Hat / Cap",
        "acc_beanie": "Beanie / Knit Cap",
        "acc_headband": "Headband / Hair Clip",
        "acc_scarf": "Scarf / Shawl",
        "acc_tie": "Necktie / Bow Tie",
        "acc_belt": "Belt",
        "acc_bag": "Handbag / Purse",
        "acc_backpack": "Backpack",

        # ── Scene ──
        "exp_scene": "Scene & Lighting",
        "scene_mode": "Location Input",
        "scene_mode_preset": "Choose from List",
        "scene_mode_custom": "Describe / Type",
        "scene_custom_input": "Describe your location",
        "scene_custom_placeholder": "e.g. Tokyo street at night with neon signs and wet pavement",
        "attach_scene_photo": "I will attach scene/background reference photo",
        "attach_scene_note": "Prompt will instruct AI to use the attached background",
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
        "lighting": "Lighting Style",
        "lit_natural": "Natural / Ambient",
        "lit_studio": "Studio Softbox",
        "lit_rim": "Rim / Backlit",
        "lit_neon": "Neon / Cyberpunk",
        "lit_candle": "Candlelight / Warm",
        "lit_dramatic": "Dramatic Chiaroscuro",
        "lit_flat": "Flat / Even",

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
        "age_child": "เด็ก (5-12)",
        "age_teen": "วัยรุ่น (13-19)",
        "age_young": "วัยหนุ่มสาว (20-30)",
        "age_mid": "วัยกลางคน (31-50)",
        "age_senior": "ผู้อาวุโส (50+)",
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
        "hair_long": "ยาวสลวย",
        "hair_short": "สั้น",
        "hair_curly": "หยิก",
        "hair_wavy": "หยักศก",
        "hair_ponytail": "หางม้า",
        "hair_bun": "มวยผม",
        "hair_braids": "ถักเปีย",
        "hair_twintails": "มัดสองข้าง",
        "hair_bob": "บ็อบ",
        "hair_pixie": "พิกซี่",
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
        "expression": "สีหน้า / อารมณ์",
        "expr_smile": "ยิ้มอ่อน",
        "expr_serious": "จริงจัง / เข้มขรึม",
        "expr_laugh": "หัวเราะ",
        "expr_pensive": "ครุ่นคิด",
        "expr_confident": "มั่นใจ",
        "expr_neutral": "เฉยๆ / ปกติ",

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
        "col_warm": "โทนอุ่น (แดง, ส้ม, ทอง)",
        "col_cool": "โทนเย็น (น้ำเงิน, เขียวอมฟ้า, เงิน)",
        "col_pastel": "พาสเทล",
        "col_mono": "ขาวดำ / โมโนโครม",
        "col_earthy": "โทนดิน / ธรรมชาติ",
        "col_vibrant": "สดใส / นีออน",

        # ── Accessories ──
        "accessories": "เครื่องประดับ (เลือกได้หลายอย่าง)",
        "acc_glasses": "แว่นสายตา",
        "acc_sunglasses": "แว่นกันแดด",
        "acc_earrings": "ต่างหู",
        "acc_necklace": "สร้อยคอ / จี้",
        "acc_choker": "โชคเกอร์",
        "acc_bracelet": "กำไล / สร้อยข้อมือ",
        "acc_watch": "นาฬิกา",
        "acc_ring": "แหวน",
        "acc_hat": "หมวก / แก๊ป",
        "acc_beanie": "หมวกบีนนี่ / ไหมพรม",
        "acc_headband": "ที่คาดผม / กิ๊บ",
        "acc_scarf": "ผ้าพันคอ / ผ้าคลุมไหล่",
        "acc_tie": "เนคไท / โบว์ไท",
        "acc_belt": "เข็มขัด",
        "acc_bag": "กระเป๋าถือ",
        "acc_backpack": "เป้สะพายหลัง",

        # ── Scene ──
        "exp_scene": "ฉากและแสง",
        "scene_mode": "ระบุสถานที่",
        "scene_mode_preset": "เลือกจากรายการ",
        "scene_mode_custom": "พิมพ์อธิบายเอง",
        "scene_custom_input": "อธิบายสถานที่ / ฉากหลัง",
        "scene_custom_placeholder": "เช่น ถนนในโตเกียวตอนกลางคืน มีป้ายนีออนและพื้นเปียกฝน",
        "attach_scene_photo": "จะแนบรูปฉาก/แบ็คกราวด์อ้างอิง",
        "attach_scene_note": "พรอมต์จะสั่งให้ AI ใช้ฉากหลังตามรูปที่แนบ",
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
        "lighting": "สไตล์แสง",
        "lit_natural": "แสงธรรมชาติ",
        "lit_studio": "ซอฟต์บ็อกซ์สตูดิโอ",
        "lit_rim": "แสงขอบ / แบ็คไลท์",
        "lit_neon": "นีออน / ไซเบอร์พังก์",
        "lit_candle": "แสงเทียน / อบอุ่น",
        "lit_dramatic": "ดราม่า เคียโรสกูโร",
        "lit_flat": "แสงเรียบ / สม่ำเสมอ",

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
    "age_child": "child (5-12 years old)", "age_teen": "teenager (13-19 years old)",
    "age_young": "young adult (20-30 years old)", "age_mid": "middle-aged adult (31-50 years old)",
    "age_senior": "senior (50+ years old)",
    # Ethnicity
    "eth_asian": "East-Asian", "eth_se_asian": "Southeast-Asian",
    "eth_south_asian": "South-Asian", "eth_european": "European Caucasian",
    "eth_african": "African", "eth_latin": "Latin American",
    "eth_middle_east": "Middle-Eastern", "eth_mixed": "mixed-race",
    # Hair Style
    "hair_long": "long flowing hair", "hair_short": "short hair",
    "hair_curly": "curly hair", "hair_wavy": "wavy hair",
    "hair_ponytail": "ponytail", "hair_bun": "hair bun",
    "hair_braids": "braids", "hair_twintails": "twin tails",
    "hair_bob": "bob cut", "hair_pixie": "pixie cut",
    "hair_bald": "bald head",
    # Hair Color
    "hc_black": "black hair", "hc_dark_brown": "dark brown hair",
    "hc_light_brown": "light brown hair", "hc_blonde": "blonde hair",
    "hc_platinum": "platinum blonde hair", "hc_red": "red auburn hair",
    "hc_ginger": "ginger hair", "hc_silver": "silver gray hair",
    "hc_white": "white hair", "hc_blue": "blue hair",
    "hc_pink": "pink hair", "hc_purple": "purple lavender hair",
    "hc_green": "green hair", "hc_ombre": "ombre hair transitioning dark to light",
    "hc_highlights": "hair with highlights and streaks",
    # Expression
    "expr_smile": "gentle smile", "expr_serious": "serious stoic expression",
    "expr_laugh": "laughing joyfully", "expr_pensive": "pensive thoughtful expression",
    "expr_confident": "confident expression", "expr_neutral": "neutral expression",
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
    # Color Palette
    "col_warm": "warm color tones of red orange and gold",
    "col_cool": "cool color tones of blue teal and silver",
    "col_pastel": "pastel colors", "col_mono": "monochrome black and white",
    "col_earthy": "earthy natural tones", "col_vibrant": "vibrant neon colors",
    # Accessories (each is a standalone phrase)
    "acc_glasses": "wearing prescription glasses",
    "acc_sunglasses": "wearing stylish sunglasses",
    "acc_earrings": "wearing earrings",
    "acc_necklace": "wearing a necklace with pendant",
    "acc_choker": "wearing a choker",
    "acc_bracelet": "wearing bracelets",
    "acc_watch": "wearing a wristwatch",
    "acc_ring": "wearing rings",
    "acc_hat": "wearing a hat",
    "acc_beanie": "wearing a knit beanie",
    "acc_headband": "wearing a headband with hair clips",
    "acc_scarf": "wearing a scarf",
    "acc_tie": "wearing a necktie",
    "acc_belt": "wearing a belt",
    "acc_bag": "carrying a handbag",
    "acc_backpack": "carrying a backpack",
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
    # Lighting
    "lit_natural": "natural ambient lighting", "lit_studio": "professional studio softbox lighting",
    "lit_rim": "dramatic rim lighting from behind",
    "lit_neon": "colorful neon lights with cyberpunk atmosphere",
    "lit_candle": "warm candlelight illumination",
    "lit_dramatic": "dramatic chiaroscuro lighting with deep shadows",
    "lit_flat": "flat even lighting",
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
    # Model Type
    "model_realistic": "Photorealistic", "model_anime": "Anime illustration style",
    "model_3d": "3D rendered CGI",
    # Quality
    "qt_8k": "8K UHD", "qt_detail": "highly detailed", "qt_sharp": "sharp focus",
    "qt_pro": "professional photography", "qt_award": "award-winning", "qt_magazine": "magazine quality",
    # Aspect Ratio
    "ar_1_1": "--ar 1:1", "ar_16_9": "--ar 16:9", "ar_9_16": "--ar 9:16", "ar_4_5": "--ar 4:5",
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

        ar_keys = ["ar_1_1", "ar_16_9", "ar_9_16", "ar_4_5"]
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
            ag_keys = ["age_young", "age_teen", "age_child", "age_mid", "age_senior"]
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
            hr_keys = ["hair_long", "hair_short", "hair_curly", "hair_wavy",
                        "hair_ponytail", "hair_bun", "hair_braids", "hair_twintails",
                        "hair_bob", "hair_pixie", "hair_bald"]
            hr_labels, _ = make_option(hr_keys)
            hr_sel = st.selectbox(t("hair_style"), hr_labels)
            hr_key = hr_keys[hr_labels.index(hr_sel)]
        with col5:
            # ── NEW: Hair Color ──
            hc_keys = ["hc_black", "hc_dark_brown", "hc_light_brown", "hc_blonde",
                        "hc_platinum", "hc_red", "hc_ginger", "hc_silver", "hc_white",
                        "hc_blue", "hc_pink", "hc_purple", "hc_green",
                        "hc_ombre", "hc_highlights"]
            hc_labels, _ = make_option(hc_keys)
            hc_sel = st.selectbox(t("hair_color"), hc_labels)
            hc_key = hc_keys[hc_labels.index(hc_sel)]

        col6, col7 = st.columns(2)
        with col6:
            ex_keys = ["expr_smile", "expr_serious", "expr_laugh",
                        "expr_pensive", "expr_confident", "expr_neutral"]
            ex_labels, _ = make_option(ex_keys)
            ex_sel = st.selectbox(t("expression"), ex_labels)
            ex_key = ex_keys[ex_labels.index(ex_sel)]
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
            cp_keys = ["col_warm", "col_cool", "col_pastel", "col_mono", "col_earthy", "col_vibrant"]
            cp_labels, _ = make_option(cp_keys)
            cp_sel = st.selectbox(t("color_palette"), cp_labels)
            cp_key = cp_keys[cp_labels.index(cp_sel)]

        # ── Accessories: individual checkboxes ──
        st.markdown(f"**{t('accessories')}**")
        acc_keys = ["acc_glasses", "acc_sunglasses", "acc_earrings", "acc_necklace",
                     "acc_choker", "acc_bracelet", "acc_watch", "acc_ring",
                     "acc_hat", "acc_beanie", "acc_headband", "acc_scarf",
                     "acc_tie", "acc_belt", "acc_bag", "acc_backpack"]
        acc_cols = st.columns(4)
        acc_selected = []
        for i, ak in enumerate(acc_keys):
            with acc_cols[i % 4]:
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
        scene_mode_labels = [t("scene_mode_preset"), t("scene_mode_custom")]
        scene_mode = st.radio(t("scene_mode"), scene_mode_labels, index=0, horizontal=True, key="scene_mode_radio")

        lo_key = "loc_studio"
        scene_custom_text = ""

        if scene_mode == scene_mode_labels[0]:
            lo_keys = ["loc_studio", "loc_street", "loc_cafe", "loc_beach",
                        "loc_forest", "loc_rooftop", "loc_room", "loc_temple", "loc_garden"]
            lo_labels, _ = make_option(lo_keys)
            lo_sel = st.selectbox(t("location"), lo_labels)
            lo_key = lo_keys[lo_labels.index(lo_sel)]
        else:
            scene_custom_text = st.text_area(t("scene_custom_input"),
                                              placeholder=t("scene_custom_placeholder"),
                                              height=80, key="scene_custom_ta")

        st.markdown("---")
        col10, col11 = st.columns(2)
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
                        "pose_cross_arms", "pose_hand_hair", "pose_looking_away", "pose_dynamic"]
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
        if attach_subject:
            subject = (f"a person matching the provided reference photo exactly, "
                       f"same face and identity, {eng(bt_key)}, {eng(ap_key)}, "
                       f"with {eng(hr_key)}, {eng(hc_key)}, "
                       f"and {eng(ex_key)}")
        else:
            subject = (f"a {eng(ag_key)} {eng(et_key)} {eng(gd_key)}, "
                       f"{eng(bt_key)}, {eng(ap_key)}, "
                       f"with {eng(hr_key)}, {eng(hc_key)}, "
                       f"and {eng(ex_key)}")
        if skin_check:
            subject += ", with ultra-realistic skin texture showing pores and fine details"

        # Outfit
        outfit_parts = []
        for fk in fs_selected_keys:
            v = eng(fk)
            if v:
                outfit_parts.append(v)
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
        else:
            env_loc = eng(lo_key)
        environment = f"{env_loc}, {eng(td_key)}"

        # Camera & Lighting
        camera_section = f"{eng(lt_key)}, {eng(sf_key)}, {eng(ca_key)}, {eng(dof_key)}"

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

        # Copy button
        copy_js = f"""
        <textarea id="prompt-text" style="position:absolute;left:-9999px">{combined_prompt}</textarea>
        <button onclick="
            var ta=document.getElementById('prompt-text');
            ta.style.position='static'; ta.select(); document.execCommand('copy');
            ta.style.position='absolute'; ta.style.left='-9999px';
            this.innerText='✅ Copied!';
            setTimeout(()=>this.innerText='📋 {t("copy_btn")}',2000);
        " style="background:linear-gradient(135deg,#43e97b 0%,#38f9d7 100%);border:none;
            padding:12px 28px;border-radius:10px;font-size:1rem;font-weight:600;cursor:pointer;
            color:#1a1a2e;min-height:48px;font-family:'Noto Sans Thai',sans-serif;">📋 {t("copy_btn")}</button>
        """
        st.markdown(copy_js, unsafe_allow_html=True)

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
