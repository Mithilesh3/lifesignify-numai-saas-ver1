from typing import Dict, Any, Optional


# =====================================================
# MANTRA LIBRARY
# =====================================================

NUMBER_MANTRAS = {
    1: {
        "deity": "Surya (Sun)",
        "mantra_sanskrit": "Om Ghrini Suryaya Namaha",
        "mantra_english": "Om Ghrini Suryaya Namaha",
        "donation": "Donate wheat or jaggery on Sunday",
    },
    2: {
        "deity": "Chandra (Moon)",
        "mantra_sanskrit": "Om Som Somaya Namaha",
        "mantra_english": "Om Som Somaya Namaha",
        "donation": "Donate rice or milk on Monday",
    },
    3: {
        "deity": "Guru (Jupiter)",
        "mantra_sanskrit": "Om Brihaspataye Namaha",
        "mantra_english": "Om Brihaspataye Namaha",
        "donation": "Donate yellow sweets or turmeric",
    },
    4: {
        "deity": "Rahu",
        "mantra_sanskrit": "Om Rahave Namaha",
        "mantra_english": "Om Rahave Namaha",
        "donation": "Donate black sesame or blankets",
    },
    5: {
        "deity": "Budh (Mercury)",
        "mantra_sanskrit": "Om Bum Budhaya Namaha",
        "mantra_english": "Om Bum Budhaya Namaha",
        "donation": "Donate green vegetables",
    },
    6: {
        "deity": "Shukra (Venus)",
        "mantra_sanskrit": "Om Shukraya Namaha",
        "mantra_english": "Om Shukraya Namaha",
        "donation": "Donate white clothes or rice",
    },
    7: {
        "deity": "Ketu",
        "mantra_sanskrit": "Om Ketave Namaha",
        "mantra_english": "Om Ketave Namaha",
        "donation": "Feed stray dogs",
    },
    8: {
        "deity": "Shani",
        "mantra_sanskrit": "Om Sham Shanicharaya Namaha",
        "mantra_english": "Om Sham Shanicharaya Namaha",
        "donation": "Donate black clothes or mustard oil",
    },
    9: {
        "deity": "Mangal (Mars)",
        "mantra_sanskrit": "Om Kraam Kreem Kraum Sah Bhaumaya Namaha",
        "mantra_english": "Om Kraam Kreem Kraum Sah Bhaumaya Namaha",
        "donation": "Donate red lentils",
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
        "mobile_wallpaper": "Use a calm geometric ya sacred-symbol wallpaper jo distraction kam kare.",
        "charging_direction": "Phone ko East ya North facing position me charge karna zyada grounding feel kara sakta hai.",
        "whatsapp_dp": "DP simple, clear aur confident rakhein taki digital identity clutter-free rahe.",
        "mobile_usage_timing": "Heavy decisions raat me avoid karein; important calls aur planning ko morning ya early evening me shift karein.",
        "number_energy_hint": f"Supportive ending energies: {supportive_text}. Real phone numbers generate nahi kiye gaye hain.",
    }


# =====================================================
# LIFESTYLE REMEDIES
# =====================================================


def generate_lifestyle_remedies(number: int, weakest_metric: str) -> Dict[str, Any]:
    color = NUMBER_COLORS.get(number, "balancing colors")
    focus_area = _focus_message(weakest_metric)

    return {
        "bracelet_suggestion": f"Color anchor ke liye number {number} aligned shades ({color}) ka subtle bracelet ya accessory use kar sakte hain.",
        "daily_routine": f"Aapke liye sabse important habit hai {focus_area}.",
        "meditation": "Roz 10 minute focused breathing ya mantra-based stillness practice rakhein.",
        "color_alignment": f"Workspace aur clothing me {color} tones use karna aapki energy ko more aligned feel kara sakta hai.",
        "habit_recommendation": f"Next 21 days ke liye ek repeatable ritual banayein jo {focus_area} par directly kaam kare.",
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
        "practice_guideline": "108 repetitions daily for 21 days, preferably same time every morning.",
        "purpose": f"Is remedy ka purpose hai {focus_area} aur inner alignment ko support karna.",
        "planetary_alignment": f"Number {number} ki planetary energy ko disciplined routine ke saath harmonize karna is remedy ka main focus hai.",
    }


# =====================================================
# DAILY ENERGY ALIGNMENT
# =====================================================


def generate_daily_energy_alignment(number: int, weakest_metric: str) -> Dict[str, Any]:
    focus_area = _focus_message(weakest_metric)

    return {
        "morning": "Subah 10-15 minutes sunlight exposure ke saath din start karein.",
        "breathing": "5 minutes deep nasal breathing ya box breathing se nervous system ko steady karein.",
        "focus_routine": f"First work block se pehle ek clear intention likhein. Aaj ka main alignment focus: {focus_area}.",
        "evening_reset": "Raat me screen slowdown aur short reflection note ke saath mental clutter release karein.",
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
