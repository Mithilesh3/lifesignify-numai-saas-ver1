from typing import Dict, Any, Optional


# =====================================================
# MANTRA LIBRARY
# =====================================================

NUMBER_MANTRAS = {
    1: {
        "deity": "Surya (Sun)",
        "mantra_sanskrit": "ॐ घृणि सूर्याय नमः",
        "mantra_english": "Om Ghrini Suryaya Namaha",
        "donation": "रविवार को गेहूं या गुड़ दान करें",
    },
    2: {
        "deity": "Chandra (Moon)",
        "mantra_sanskrit": "ॐ सोम सोमाय नमः",
        "mantra_english": "Om Som Somaya Namaha",
        "donation": "सोमवार को चावल या दूध दान करें",
    },
    3: {
        "deity": "Guru (Jupiter)",
        "mantra_sanskrit": "ॐ बृहस्पतये नमः",
        "mantra_english": "Om Brihaspataye Namaha",
        "donation": "पीली मिठाई या हल्दी दान करें",
    },
    4: {
        "deity": "Rahu",
        "mantra_sanskrit": "ॐ राहवे नमः",
        "mantra_english": "Om Rahave Namaha",
        "donation": "काला तिल या कंबल दान करें",
    },
    5: {
        "deity": "Budh (Mercury)",
        "mantra_sanskrit": "ॐ बुं बुधाय नमः",
        "mantra_english": "Om Bum Budhaya Namaha",
        "donation": "हरी सब्जियां दान करें",
    },
    6: {
        "deity": "Shukra (Venus)",
        "mantra_sanskrit": "ॐ शुक्राय नमः",
        "mantra_english": "Om Shukraya Namaha",
        "donation": "सफेद कपड़े या चावल दान करें",
    },
    7: {
        "deity": "Ketu",
        "mantra_sanskrit": "ॐ केतवे नमः",
        "mantra_english": "Om Ketave Namaha",
        "donation": "आवारा कुत्तों को भोजन कराएं",
    },
    8: {
        "deity": "Shani",
        "mantra_sanskrit": "ॐ शं शनैश्चराय नमः",
        "mantra_english": "Om Sham Shanicharaya Namaha",
        "donation": "काले कपड़े या सरसों का तेल दान करें",
    },
    9: {
        "deity": "Mangal (Mars)",
        "mantra_sanskrit": "ॐ क्रां क्रीं क्रौं सः भौमाय नमः",
        "mantra_english": "Om Kraam Kreem Kraum Sah Bhaumaya Namaha",
        "donation": "लाल मसूर दान करें",
    },
}

NUMBER_COLORS = {
    1: "Gold / Orange",
    2: "White / Silver",
    3: "Yellow",
    4: "Electric Blue",
    5: "Green",
    6: "Light Blue / Pink",
    7: "Grey / Smoky White",
    8: "Dark Blue / Black",
    9: "Red",
}

HABIT_FOCUS = {
    "life_stability_index": "daily routine aur sleep-wake consistency ko stable banana",
    "financial_discipline_index": "money review aur spending boundaries ko strong banana",
    "emotional_regulation_index": "breathwork aur calm-response practice ko deepen karna",
    "dharma_alignment_score": "daily priorities ko long-term purpose ke saath align karna",
    "confidence_score": "decision journal aur clarity ritual ko improve karna",
}


# =====================================================
# INTERNAL HELPERS
# =====================================================


def _weakest_metric(scores: Optional[Dict[str, Any]]) -> str:
    if not scores:
        return "life_stability_index"

    candidates = [
        "life_stability_index",
        "financial_discipline_index",
        "emotional_regulation_index",
        "dharma_alignment_score",
        "confidence_score",
    ]

    resolved = []
    for key in candidates:
        try:
            resolved.append((key, int(scores.get(key, 50))))
        except (TypeError, ValueError):
            resolved.append((key, 50))

    return min(resolved, key=lambda item: item[1])[0]


def _focus_message(metric_key: str) -> str:
    return HABIT_FOCUS.get(metric_key, HABIT_FOCUS["life_stability_index"])


# =====================================================
# MOBILE REMEDIES
# =====================================================


def generate_mobile_remedies(number: int, mobile_analysis: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    color = NUMBER_COLORS.get(number, "Neutral")
    supportive = (mobile_analysis or {}).get("supportive_number_energies") or []
    supportive_text = ", ".join(str(value) for value in supportive[:3]) if supportive else "1, 3, 5"

    return {
        "mobile_cover_color": color,
        "mobile_wallpaper": "ऐसा calm geometric या sacred-symbol wallpaper रखें जो distraction कम करे।",
        "charging_direction": "फोन को East या North facing दिशा में charge करना ज्यादा grounding दे सकता है।",
        "whatsapp_dp": "DP simple, clear और confident रखें ताकि digital identity clutter-free रहे।",
        "mobile_usage_timing": "Heavy decisions रात में avoid करें; important calls और planning को morning या early evening में रखें।",
        "number_energy_hint": f"Supportive ending energies: {supportive_text}. यहां real phone numbers generate नहीं किए गए हैं।",
    }


# =====================================================
# LIFESTYLE REMEDIES
# =====================================================


def generate_lifestyle_remedies(number: int, weakest_metric: str) -> Dict[str, Any]:
    color = NUMBER_COLORS.get(number, "balancing colors")
    focus_area = _focus_message(weakest_metric)

    return {
        "bracelet_suggestion": f"Color anchor के लिए number {number} aligned shades ({color}) का subtle bracelet या accessory use कर सकते हैं।",
        "daily_routine": f"आपके लिए सबसे important habit है {focus_area}।",
        "meditation": "रोज 10 minute focused breathing या mantra-based stillness practice रखें।",
        "color_alignment": f"Workspace और clothing में {color} tones use करना आपकी energy को more aligned महसूस करा सकता है।",
        "habit_recommendation": f"अगले 21 दिनों के लिए ऐसा repeatable ritual बनाएं जो {focus_area} पर directly काम करे।",
    }


# =====================================================
# VEDIC REMEDIES
# =====================================================


def generate_vedic_remedies(number: int, weakest_metric: str) -> Dict[str, Any]:
    mantra_data = NUMBER_MANTRAS.get(number)

    if not mantra_data:
        return {}

    focus_area = _focus_message(weakest_metric)

    return {
        "deity": mantra_data["deity"],
        "mantra_sanskrit": mantra_data["mantra_sanskrit"],
        "mantra_pronunciation": mantra_data["mantra_english"],
        "recommended_donation": mantra_data["donation"],
        "practice_guideline": "21 दिनों तक रोज 108 repetitions करें, बेहतर होगा कि हर सुबह same time पर करें।",
        "purpose": f"इस remedy का purpose है {focus_area} और inner alignment को support करना।",
        "planetary_alignment": f"Number {number} की planetary energy को disciplined routine के साथ harmonize करना इस remedy का main focus है।",
    }


# =====================================================
# DAILY ENERGY ALIGNMENT
# =====================================================


def generate_daily_energy_alignment(number: int, weakest_metric: str) -> Dict[str, Any]:
    focus_area = _focus_message(weakest_metric)

    return {
        "morning": "सुबह 10-15 minutes sunlight exposure के साथ दिन शुरू करें।",
        "breathing": "5 minutes deep nasal breathing या box breathing से nervous system को steady करें।",
        "focus_routine": f"First work block से पहले एक clear intention लिखें। आज का main alignment focus: {focus_area}।",
        "evening_reset": "रात में screen slowdown और short reflection note के साथ mental clutter release करें।",
    }


# =====================================================
# MASTER REMEDY GENERATOR
# =====================================================


def generate_remedy_protocol(
    numerology_core: Dict[str, Any],
    scores: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    pythagorean = numerology_core.get("pythagorean", {})
    mobile_analysis = numerology_core.get("mobile_analysis", {})

    primary_number = pythagorean.get("life_path_number") or pythagorean.get("destiny_number") or 0
    if not primary_number:
        return {}

    weakest_metric = _weakest_metric(scores)

    return {
        "lifestyle_remedies": generate_lifestyle_remedies(primary_number, weakest_metric),
        "mobile_remedies": generate_mobile_remedies(primary_number, mobile_analysis=mobile_analysis),
        "vedic_remedies": generate_vedic_remedies(primary_number, weakest_metric),
        "daily_energy_alignment": generate_daily_energy_alignment(primary_number, weakest_metric),
    }
