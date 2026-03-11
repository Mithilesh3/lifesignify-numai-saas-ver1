from __future__ import annotations

from datetime import datetime
import re
from typing import Any, Dict, List, Sequence, Tuple

from app.modules.reports.blueprint import SECTION_TITLES, get_tier_section_blueprint

PLANET_BY_NUMBER: Dict[int, str] = {
    1: "Surya",
    2: "Chandra",
    3: "Guru",
    4: "Rahu",
    5: "Budh",
    6: "Shukra",
    7: "Ketu",
    8: "Shani",
    9: "Mangal",
    11: "Moon-Jupiter",
    22: "Rahu-Saturn",
}

NUMBER_TRAITS: Dict[int, Dict[str, str]] = {
    1: {"strength": "initiative and leadership", "risk": "over-control", "protocol": "lead with review loops"},
    2: {"strength": "diplomacy and empathy", "risk": "indecision", "protocol": "enforce decision windows"},
    3: {"strength": "communication and creativity", "risk": "scattered execution", "protocol": "convert ideas into weekly outputs"},
    4: {"strength": "discipline and structure", "risk": "rigidity", "protocol": "blend process with flexibility"},
    5: {"strength": "adaptability and speed", "risk": "restless switching", "protocol": "protect freedom inside routine"},
    6: {"strength": "responsibility and trust", "risk": "over-burdening", "protocol": "set role boundaries"},
    7: {"strength": "analysis and insight", "risk": "overthinking", "protocol": "convert insight to checkpoints"},
    8: {"strength": "authority and material strategy", "risk": "pressure intensity", "protocol": "scale with governance"},
    9: {"strength": "vision and influence", "risk": "energy leakage", "protocol": "prioritize and close loops"},
}

COMPOUND_MEANINGS: Dict[int, str] = {
    13: "karmic discipline debt",
    14: "karmic freedom debt",
    16: "karmic ego correction",
    19: "karmic independence debt",
    22: "master builder field",
    33: "master service field",
}

SECTION_META: Dict[str, Dict[str, Any]] = {
    "default": {
        "purpose": "यह सेक्शन निर्धारक diagnosis और correction protocol देता है।",
        "key_inputs": ["numerology_core", "core_metrics", "intake_context"],
        "output_fields": ["cards", "bullets", "narrative"],
        "interpretation_logic": "Structural signals को behavior impact और protocol में map किया जाता है।",
        "tone_guidance": "Executive, premium, और consultation-grade tone बनाए रखें।",
    },
    "intelligence_metrics": {
        "purpose": "Strength, deficit, और intervention focus को measurable format में quantify करें।",
        "key_inputs": ["core_metrics", "loshu_grid", "behavioral_intake"],
        "output_fields": ["primary_strength", "primary_deficit", "structural_cause", "intervention_focus", "risk_band"],
        "interpretation_logic": "Metric stack rank करके उसे structural signals से जोड़ा जाता है।",
        "tone_guidance": "Diagnostic, concise, और high-authority guidance दें।",
    },
}


def _safe_text(value: Any, default: str = "") -> str:
    text = " ".join(str(value or "").split())
    return text or default


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_list(value: Any) -> List[Any]:
    if isinstance(value, list):
        return [item for item in value if item not in (None, "", [], {})]
    if value in (None, "", [], {}):
        return []
    return [value]


def _reduce_number(value: int) -> int:
    while value > 9 and value not in {11, 22, 33}:
        value = sum(int(char) for char in str(value))
    return value


def _alpha_sum(value: str) -> int:
    cleaned = "".join(char for char in value.lower() if char.isalpha())
    return sum(ord(char) - 96 for char in cleaned)


def _vibration_from_text(value: str) -> int:
    total = _alpha_sum(value)
    return _reduce_number(total) if total > 0 else 0


def _vibration_from_digits(value: str) -> int:
    digits = [int(char) for char in str(value or "") if char.isdigit()]
    return _reduce_number(sum(digits)) if digits else 0


def _metric_labels() -> Dict[str, str]:
    return {
        "life_stability_index": "Life Stability",
        "confidence_score": "Decision Clarity",
        "dharma_alignment_score": "Dharma Alignment",
        "emotional_regulation_index": "Emotional Regulation",
        "financial_discipline_index": "Financial Discipline",
        "karma_pressure_index": "Karma Pressure",
    }


def _metric_order(scores: Dict[str, Any]) -> List[Tuple[str, int]]:
    keys = [
        "life_stability_index",
        "confidence_score",
        "dharma_alignment_score",
        "emotional_regulation_index",
        "financial_discipline_index",
        "karma_pressure_index",
    ]
    return [(key, _safe_int(scores.get(key), 50)) for key in keys]


def _metric_status(score: int) -> str:
    if score >= 75:
        return "Strong"
    if score >= 55:
        return "Moderate"
    return "Sensitive"


def _risk_band(scores: Dict[str, Any]) -> str:
    confidence = _safe_int(scores.get("confidence_score"), 50)
    stability = _safe_int(scores.get("life_stability_index"), 50)
    emotional = _safe_int(scores.get("emotional_regulation_index"), 50)
    finance = _safe_int(scores.get("financial_discipline_index"), 50)
    karma = _safe_int(scores.get("karma_pressure_index"), 50)
    weakest = min(confidence, stability, emotional, finance)
    if karma >= 75 or weakest <= 35:
        return "High Risk | Structural Intervention Required"
    if karma >= 60 or weakest <= 49:
        return "Watch Zone | Guided Stabilization Required"
    if weakest >= 70 and karma <= 45:
        return "Strategic Growth Zone | Scale with Governance"
    return "Correctable Zone | Protocol-Driven Improvement"


def _dominant_planet(life_path: int, destiny: int, name_number: int) -> str:
    primary = life_path or destiny or name_number or 5
    return PLANET_BY_NUMBER.get(primary, "Budh")


def _parse_date(value: str) -> Tuple[int, int, int]:
    text = _safe_text(value)
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            dt = datetime.strptime(text, fmt)
            return (dt.day, dt.month, dt.year)
        except ValueError:
            continue
    return (1, 1, 2000)


def _personal_year(day: int, month: int) -> int:
    total = sum(int(char) for char in f"{day:02d}{month:02d}{datetime.utcnow().year}")
    return _reduce_number(total)


def _lucky_dates(day: int, month: int, life_path: int, destiny: int) -> List[int]:
    anchors = {life_path, destiny, _reduce_number(day), _reduce_number(month)}
    anchors.discard(0)
    dates = sorted(value for value in anchors if value <= 31)
    return dates[:5] or [3, 5, 9]


def _karmic_numbers(day: int, name_compound: int, business_compound: int) -> List[int]:
    values = [day, name_compound, business_compound]
    return sorted(set(value for value in values if value in {13, 14, 16, 19}))


def _hidden_passion(loshu_grid: Dict[str, Any], full_name: str) -> Tuple[int, str]:
    counts = loshu_grid.get("grid_counts") if isinstance(loshu_grid, dict) else {}
    if isinstance(counts, dict) and counts:
        best_number = max(range(1, 10), key=lambda number: _safe_int(counts.get(str(number), counts.get(number, 0)), 0))
        return best_number, NUMBER_TRAITS.get(best_number, NUMBER_TRAITS[5])["strength"]
    vibration = _vibration_from_text(full_name) or 5
    return vibration, NUMBER_TRAITS.get(vibration, NUMBER_TRAITS[5])["strength"]


def _pinnacle_challenge(day: int, month: int, year: int) -> Dict[str, List[int]]:
    year_sum = _reduce_number(sum(int(char) for char in str(year)))
    day_root = _reduce_number(day)
    month_root = _reduce_number(month)
    p1 = _reduce_number(day_root + month_root)
    p2 = _reduce_number(day_root + year_sum)
    p3 = _reduce_number(p1 + p2)
    c1 = abs(day_root - month_root)
    c2 = abs(day_root - year_sum)
    c3 = abs(c1 - c2)
    return {"pinnacles": [p1, p2, p3], "challenges": [c1, c2, c3]}

def _name_options(full_name: str, target_numbers: Sequence[int]) -> List[Dict[str, Any]]:
    base = _safe_text(full_name)
    if not base:
        return []
    variants = [base, f"{base}a", f"{base}h", f"{base}aa", f"{base}y", f"{base}i"]
    options: List[Dict[str, Any]] = []
    seen = set()
    for variant in variants:
        key = variant.lower()
        if key in seen:
            continue
        seen.add(key)
        number = _vibration_from_text(variant)
        if number <= 0:
            continue
        if target_numbers and number not in target_numbers:
            continue
        options.append({"option": variant, "number": number, "logic": "aligns with target vibration"})
    return options[:3]


def _handle_patterns(base: str, target_numbers: Sequence[int]) -> List[str]:
    cleaned = "".join(char for char in base.lower() if char.isalnum()) or "strategicprofile"
    patterns: List[str] = []
    for number in target_numbers[:3] or [1, 3, 5]:
        patterns.append(f"{cleaned}.{number}")
        patterns.append(f"{cleaned}_{number}x")
    deduped: List[str] = []
    for item in patterns:
        if item not in deduped:
            deduped.append(item)
    return deduped[:4]


def _compound_meaning(value: int) -> str:
    return COMPOUND_MEANINGS.get(value, "composite growth-pressure cycle")


CARD_LABELS_HI: Dict[str, str] = {
    "What is happening": "क्या हो रहा है",
    "Why it is happening": "यह क्यों हो रहा है",
    "What it affects": "इसका प्रभाव",
    "What to do about it": "क्या करना चाहिए",
    "Current Number": "वर्तमान संख्या",
    "Current Name Number": "वर्तमान नाम संख्या",
    "Target Numbers": "लक्ष्य संख्याएं",
    "Strength": "मुख्य ताकत",
    "Risk": "मुख्य जोखिम",
    "Current Mobile": "वर्तमान मोबाइल",
    "Target Vibrations": "लक्ष्य वाइब्रेशन",
    "Ending Logic": "अंतिम अंक लॉजिक",
    "Current Email": "वर्तमान ईमेल",
    "Email Vibration": "ईमेल वाइब्रेशन",
    "Authority Signal": "ऑथोरिटी सिग्नल",
    "Starting Stroke": "शुरुआती स्ट्रोक",
    "Ending Stroke": "अंतिम स्ट्रोक",
    "Authority Alignment": "ऑथोरिटी एलाइनमेंट",
    "Business Name": "बिज़नेस नाम",
    "Industry Fit": "इंडस्ट्री फिट",
    "Social Handle": "सोशल हैंडल",
    "Domain Handle": "डोमेन हैंडल",
    "Current Residence Number": "वर्तमान रेजिडेंस नंबर",
    "Residence Vibration": "रेजिडेंस वाइब्रेशन",
    "Current Vehicle Number": "वर्तमान वाहन नंबर",
    "Vehicle Vibration": "वाहन वाइब्रेशन",
    "Focus": "फोकस",
    "Code": "कोड",
    "Parameter": "पैरामीटर",
    "Output": "आउटपुट",
    "Top Priority": "टॉप प्रायोरिटी",
    "High-Impact Quick Fixes": "हाई-इम्पैक्ट क्विक फिक्स",
    "Medium-Term Adjustments": "मिड-टर्म एडजस्टमेंट",
    "Premium Advisory": "प्रीमियम एडवाइजरी",
    "Current Personal Year": "वर्तमान पर्सनल ईयर",
    "Favorable Dates": "अनुकूल तिथियां",
    "Lucky Numbers": "सपोर्टिव नंबर",
    "Risk Band": "रिस्क बैंड",
    "Dominant Planet": "डॉमिनेंट ग्रह",
}

DEVANAGARI_PATTERN = re.compile(r"[\u0900-\u097F]")
PLACEHOLDER_PATTERN = re.compile(r"\{[^{}]+\}")

PHRASE_REPLACEMENTS: Sequence[Tuple[str, str]] = [
    ("Deterministic structure", "निर्धारित संरचना"),
    ("deterministic structure", "निर्धारित संरचना"),
    ("Deterministic signal", "निर्धारित संकेत"),
    ("deterministic signal", "निर्धारित संकेत"),
    ("generated from deterministic profile synthesis", "निर्धारित प्रोफाइल synthesis से तैयार"),
    ("Not provided", "इनपुट उपलब्ध नहीं"),
    ("Current cycle", "वर्तमान चक्र"),
    ("Current personal year", "वर्तमान पर्सनल ईयर"),
    ("Personal year", "पर्सनल ईयर"),
    ("Risk band", "रिस्क बैंड"),
    ("Primary deficit", "मुख्य कमी"),
    ("Primary strength", "मुख्य ताकत"),
    ("Current ", "वर्तमान "),
    ("Target ", "लक्ष्य "),
    ("Option ", "विकल्प "),
]

WORD_REPLACEMENTS: Sequence[Tuple[str, str]] = [
    (r"\bprofile\b", "प्रोफाइल"),
    (r"\bstrategic\b", "रणनीतिक"),
    (r"\banalysis\b", "विश्लेषण"),
    (r"\bstructure\b", "संरचना"),
    (r"\bindicates\b", "संकेत देता है"),
    (r"\bshows\b", "दिखाता है"),
    (r"\bsupports\b", "सपोर्ट करता है"),
    (r"\bimproves\b", "बेहतर करता है"),
    (r"\bstabilize\b", "स्थिर करें"),
    (r"\bconsistency\b", "कंसिस्टेंसी"),
    (r"\bdiscipline\b", "डिसिप्लिन"),
    (r"\bstrategy\b", "स्ट्रैटेजी"),
    (r"\brisk\b", "जोखिम"),
    (r"\bstrength\b", "ताकत"),
    (r"\bdeficit\b", "कमी"),
    (r"\balignment\b", "एलाइनमेंट"),
    (r"\bgrowth\b", "ग्रोथ"),
]


def _hindi_mix_text(value: Any) -> str:
    text = _safe_text(value)
    if not text:
        return text

    text = PLACEHOLDER_PATTERN.sub("", text)
    text = re.sub(r"(,\s*){2,}", ", ", text)
    text = re.sub(r"\s+[|]\s+", " | ", text)
    text = re.sub(r"\s{2,}", " ", text).strip(" ,;|")

    if not text:
        return "इनपुट उपलब्ध नहीं"

    for source, target in PHRASE_REPLACEMENTS:
        text = text.replace(source, target)

    for pattern, replacement in WORD_REPLACEMENTS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    text = re.sub(r"\s{2,}", " ", text).strip()
    text = re.sub(r"([|,:;])\1+", r"\1", text)
    text = text.replace("रणनीतिक संकेत: रणनीतिक संकेत:", "रणनीतिक संकेत:")
    text = text.replace("..", ".")

    latin_letters = sum(1 for ch in text if ("a" <= ch.lower() <= "z"))
    latin_ratio = latin_letters / max(len(text), 1)
    has_devanagari = bool(DEVANAGARI_PATTERN.search(text))

    if latin_ratio > 0.55 and not has_devanagari:
        text = f"रणनीतिक संकेत: {text}. इसे सुधार प्रोटोकॉल और disciplined execution के साथ लागू करें।"

    return text


def _localize_payloads(payloads: Dict[str, Any]) -> Dict[str, Any]:
    localized: Dict[str, Any] = {}
    for key, payload in (payloads or {}).items():
        if not isinstance(payload, dict):
            localized[key] = payload
            continue

        entry = dict(payload)

        entry["purpose"] = _hindi_mix_text(
            entry.get("purpose") or "यह सेक्शन deterministic diagnosis और correction protocol देता है।"
        ) or "यह सेक्शन deterministic diagnosis और correction protocol देता है।"
        entry["interpretation_logic"] = _hindi_mix_text(entry.get("interpretation_logic")) or "Structural signal से actionable insight निकाली जाती है।"
        entry["tone_guidance"] = _hindi_mix_text(entry.get("tone_guidance")) or "Executive और premium tone रखें।"
        entry["narrative"] = _hindi_mix_text(entry.get("narrative")) or "इनपुट उपलब्ध नहीं"

        cards = []
        for card in entry.get("cards") or []:
            if not isinstance(card, dict):
                continue
            label = _safe_text(card.get("label"))
            cards.append(
                {
                    "label": CARD_LABELS_HI.get(label, _hindi_mix_text(label)),
                    "value": _hindi_mix_text(card.get("value")) or "इनपुट उपलब्ध नहीं",
                }
            )
        entry["cards"] = cards

        entry["bullets"] = [_hindi_mix_text(item) for item in (entry.get("bullets") or []) if _safe_text(item)]

        localized[key] = entry

    return localized


def _section_payload(
    section_key: str,
    narrative: str,
    what_happening: str,
    why_happening: str,
    impact: str,
    action: str,
    extra_cards: Sequence[Dict[str, str]] | None = None,
    bullets: Sequence[str] | None = None,
) -> Dict[str, Any]:
    meta = SECTION_META.get(section_key, SECTION_META["default"])
    cards = [
        {"label": "क्या हो रहा है", "value": what_happening},
        {"label": "यह क्यों हो रहा है", "value": why_happening},
        {"label": "इसका प्रभाव", "value": impact},
        {"label": "क्या करना चाहिए", "value": action},
    ]
    if extra_cards:
        cards.extend(extra_cards)
    clean_bullets = [_safe_text(item) for item in (bullets or []) if _safe_text(item)]
    return {
        "section_key": section_key,
        "title": SECTION_TITLES.get(section_key, section_key.replace("_", " ").title()),
        "purpose": meta["purpose"],
        "key_inputs": meta["key_inputs"],
        "output_fields": meta["output_fields"],
        "interpretation_logic": meta["interpretation_logic"],
        "tone_guidance": meta["tone_guidance"],
        "cards": cards,
        "bullets": clean_bullets,
        "narrative": _safe_text(narrative),
    }


def _ensure_all_payloads(plan_name: str, payloads: Dict[str, Any]) -> Dict[str, Any]:
    for section in get_tier_section_blueprint(plan_name).get("sections", []):
        key = section.get("key")
        if key and key not in payloads:
            payloads[key] = _section_payload(
                key,
                narrative=f"{SECTION_TITLES.get(key, key)} निर्धारित प्रोफाइल synthesis से तैयार किया गया है।",
                what_happening="इस intelligence layer में स्पष्ट निर्धारित संकेत दिख रहा है।",
                why_happening="यह layer numerology core और intake patterns के रिश्ते से निकला है।",
                impact="यह correction-aware निर्णय lens उपलब्ध कराता है।",
                action="इस protocol को integrated execution system में लागू करें।",
            )
    return payloads


def build_interpretation_report(
    intake_context: Dict[str, Any],
    numerology_core: Dict[str, Any],
    scores: Dict[str, Any],
    archetype: Dict[str, Any],
    remedies: Dict[str, Any],
    plan_name: str = "basic",
) -> Dict[str, Any]:
    intake_context = intake_context or {}
    numerology_core = numerology_core or {}
    scores = scores or {}
    archetype = archetype or {}
    remedies = remedies or {}

    identity = intake_context.get("identity") or {}
    birth_details = intake_context.get("birth_details") or {}
    focus = intake_context.get("focus") or {}
    career = intake_context.get("career") or {}
    contact = intake_context.get("contact") or {}
    preferences = intake_context.get("preferences") or {}

    full_name = _safe_text(identity.get("full_name"), "Strategic Client")
    first_name = full_name.split()[0]
    date_of_birth = _safe_text(birth_details.get("date_of_birth") or identity.get("date_of_birth"))
    day, month, year = _parse_date(date_of_birth)
    current_problem = _safe_text(intake_context.get("current_problem"), "strategic consistency and calibrated growth")

    city = _safe_text(birth_details.get("birthplace_city") or identity.get("city"), "current city")
    career_industry = _safe_text(career.get("industry") or preferences.get("profession"), "strategy and operations")

    pyth = numerology_core.get("pythagorean") or {}
    chaldean = numerology_core.get("chaldean") or {}
    loshu_grid = numerology_core.get("loshu_grid") or {}
    mobile_analysis = numerology_core.get("mobile_analysis") or {}
    email_analysis = numerology_core.get("email_analysis") or {}
    name_correction = numerology_core.get("name_correction") or {}
    business_analysis = numerology_core.get("business_analysis") or {}
    compatibility = numerology_core.get("compatibility") or {}

    life_path = _safe_int(pyth.get("life_path_number"), 0)
    destiny = _safe_int(pyth.get("destiny_number"), 0)
    expression = _safe_int(pyth.get("expression_number"), 0)
    soul_urge = _safe_int(pyth.get("soul_urge_number"), _reduce_number(_alpha_sum(full_name)))
    personality = _safe_int(pyth.get("personality_number"), expression)
    name_number = _safe_int(chaldean.get("name_number"), _safe_int(name_correction.get("current_number"), 0))

    name_compound = _alpha_sum(full_name)
    name_trait = NUMBER_TRAITS.get(name_number or life_path or 5, NUMBER_TRAITS[5])
    name_strength = name_trait["strength"]
    name_risk = name_trait["risk"]

    dominant_planet = _dominant_planet(life_path, destiny, name_number)

    metric_labels = _metric_labels()
    metric_pairs = _metric_order(scores)
    strongest_key, strongest_score = max(metric_pairs, key=lambda item: item[1])
    weakest_key, weakest_score = min(metric_pairs, key=lambda item: item[1])
    strongest_metric = metric_labels[strongest_key]
    weakest_metric = metric_labels[weakest_key]
    risk_band = _risk_band(scores)

    grid_counts = loshu_grid.get("grid_counts") if isinstance(loshu_grid, dict) else {}
    loshu_present: List[int] = []
    loshu_missing: List[int] = []
    if isinstance(grid_counts, dict) and grid_counts:
        for number in range(1, 10):
            count = _safe_int(grid_counts.get(str(number), grid_counts.get(number, 0)), 0)
            if count > 0:
                loshu_present.append(number)
            else:
                loshu_missing.append(number)
    else:
        loshu_missing = [3, 5, 6]

    override_missing = [_safe_int(value, 0) for value in _safe_list(loshu_grid.get("missing_numbers")) if _safe_int(value, 0)]
    if override_missing:
        loshu_missing = sorted(set(override_missing))
        loshu_present = [number for number in range(1, 10) if number not in loshu_missing]

    primary_missing = loshu_missing[0] if loshu_missing else 0
    structural_cause = (
        f"सबसे कमजोर अक्ष {weakest_metric} पर Lo Shu में digit {primary_missing or 'none'} की कमी और current stress load का संयुक्त प्रभाव है।"
    )
    intervention_focus = (
        f"{weakest_metric.lower()} को rhythm protocol से स्थिर करें, फिर identity corrections को architecture के साथ align करें।"
    )

    metric_cards: List[Dict[str, Any]] = []
    for key, score in metric_pairs:
        label = metric_labels[key]
        metric_cards.append(
            {
                "key": key,
                "label": label,
                "score": score,
                "status": _metric_status(score),
                "meaning": f"{label} का score {score} आपकी deterministic behavior-risk quality को दिखाता है।",
                "risk": "Low score पर pressure के समय execution unstable हो सकता है।",
                "improvement": "Measurable protocol बनाकर weekly review checkpoint जोड़ें।",
            }
        )

    metric_explanations = {
        card["key"]: {
            "label": card["label"],
            "score": card["score"],
            "status": card["status"],
            "meaning": card["meaning"],
            "driver": structural_cause,
            "risk": card["risk"],
            "improvement": card["improvement"],
        }
        for card in metric_cards
    }

    mobile_value = _safe_text(contact.get("mobile_number") or identity.get("mobile_number"))
    mobile_vibration = _safe_int(mobile_analysis.get("mobile_vibration") or mobile_analysis.get("mobile_number_vibration"), _vibration_from_digits(mobile_value))
    mobile_supportive = [_safe_int(value, 0) for value in _safe_list(mobile_analysis.get("supportive_number_energies")) if _safe_int(value, 0)]
    if not mobile_supportive:
        mobile_supportive = [life_path or 1, destiny or 3, 5]
    mobile_compatibility = _safe_text(
        mobile_analysis.get("compatibility_status"),
        "supportive" if mobile_vibration in mobile_supportive else "neutral",
    )
    mobile_summary = _safe_text(
        mobile_analysis.get("compatibility_summary"),
        f"Mobile vibration {mobile_vibration} और profile compatibility {mobile_compatibility} का संयुक्त असर communication tone पर पड़ता है।",
    )

    email_value = _safe_text(identity.get("email"))
    email_vibration = _safe_int(email_analysis.get("email_number"), _vibration_from_text(email_value.split("@")[0] if email_value else ""))

    social_handle = _safe_text(contact.get("social_handle"))
    domain_handle = _safe_text(contact.get("domain_handle"))
    residence_number = _safe_text(contact.get("residence_number"))
    vehicle_number = _safe_text(contact.get("vehicle_number"))
    residence_vibration = _vibration_from_digits(residence_number)
    vehicle_vibration = _vibration_from_digits(vehicle_number)

    business_name = _safe_text(identity.get("business_name"))
    business_number = _safe_int(business_analysis.get("business_number"), _vibration_from_text(business_name))
    business_compound = _safe_int(business_analysis.get("compound_number"), _alpha_sum(business_name))
    business_strength = _safe_text(
        business_analysis.get("business_strength"),
        "Business signal disciplined execution के साथ strategic positioning को support करता है।",
    )
    business_risk = _safe_text(
        business_analysis.get("risk_factor"),
        "Commercial outcome pressure के समय discipline और clarity पर निर्भर करता है।",
    )
    business_industries = [_safe_text(item) for item in _safe_list(business_analysis.get("compatible_industries")) if _safe_text(item)]
    if not business_industries:
        business_industries = [career_industry, "consulting", "digital services"]

    personal_year = _personal_year(day, month)
    lucky_dates = _lucky_dates(day, month, life_path, destiny)
    karmic_numbers = _karmic_numbers(day, name_compound, business_compound)
    hidden_passion_number, hidden_talent_trait = _hidden_passion(loshu_grid, full_name)
    pinnacle = _pinnacle_challenge(day, month, year)

    name_targets = sorted({value for value in [life_path, destiny, expression, 3, 5, 6] if value and value not in {4, 8}})[:4]
    if not name_targets:
        name_targets = [1, 3, 5]
    name_options = _name_options(full_name, name_targets)

    compatibility_summary = _safe_text(
        compatibility.get("relationship_guidance"),
        f"Compatibility उन profiles के साथ strongest होती है जो {strongest_metric.lower()} को reinforce करें और {weakest_metric.lower()} पर pressure कम करें।",
    )

    lifestyle_protocol = "Daily same-time morning anchor, deep-work first block, और evening shutdown checklist follow करें।"
    digital_protocol = "Notification tiering रखें, late-night high-stake decisions avoid करें, और weekly digital detox window रखें।"
    decision_protocol = "High-impact decisions में 24-hour delay rule, written criteria, और weekly assumption audit लागू करें।"
    emotional_protocol = "Key calls से पहले breath reset, fixed sleep window, और post-stress review cadence बनाए रखें।"

    vedic = remedies.get("vedic_remedies") if isinstance(remedies, dict) else {}
    vedic = vedic if isinstance(vedic, dict) else {}
    vedic_code = _safe_text(vedic.get("mantra_pronunciation") or vedic.get("mantra_sanskrit"), "Om Budhaya Namah")
    vedic_parameter = _safe_text(vedic.get("practice_guideline"), "21 days x 108 repetitions fixed time पर")
    vedic_output = _safe_text(vedic.get("recommended_donation"), "Weekly practical donation with clear intention")

    correction_priority_lines = [
        f"{weakest_metric.lower()} को rhythm protocol से स्थिर करें।",
        "Name और mobile vibration alignment optimize करें।",
        "Email और signature authority signal upgrade करें।",
        "अगर high-pressure pattern बना रहे तो residence और vehicle vibration align करें।",
    ]

    payloads: Dict[str, Any] = {}
    payloads["executive_summary"] = _section_payload("executive_summary", f"{full_name} की प्रोफाइल रणनीतिक है, पर correction-sensitive भी है। Risk band {risk_band} दिखाता है कि primary strength {strongest_metric} और primary deficit {weakest_metric} के बीच संतुलन बनाना ज़रूरी है। Core concern: {current_problem}.", f"Strategic potential स्पष्ट है, लेकिन {weakest_metric.lower()} execution में friction ला रहा है।", structural_cause, f"इसका असर {career_industry} में career momentum, financial discipline, और decision quality पर पड़ता है।", intervention_focus, [{"label": "Risk Band", "value": risk_band}, {"label": "Dominant Planet", "value": dominant_planet}])
    payloads["intelligence_metrics"] = {**_section_payload("intelligence_metrics", "Metrics को structural diagnostics की तरह पढ़ना चाहिए।", f"Primary Strength: {strongest_metric}. Primary Deficit: {weakest_metric}.", structural_cause, "Deficit metric volatility बढ़ाता है, जबकि strength metric growth leverage देता है।", intervention_focus, [{"label": "Primary Strength", "value": strongest_metric}, {"label": "Primary Deficit", "value": weakest_metric}, {"label": "Structural Cause", "value": structural_cause}, {"label": "Intervention Focus", "value": intervention_focus}, {"label": "Risk Band", "value": risk_band}]), "metric_cards": metric_cards, "show_chart": True}
    payloads["core_numerology_numbers"] = _section_payload("core_numerology_numbers", f"मूल अंक संरचना: Life Path {life_path}, Destiny {destiny}, Expression {expression}, Soul Urge {soul_urge}, Personality {personality}.", "Core numbers strategic-growth potential दिखाते हैं, लेकिन protocol dependency भी दर्शाते हैं।", "Direction, execution, expression, और projection इस stack से नियंत्रित होते हैं।", "Role-fit, leadership style, और stress response इसी architecture को follow करते हैं।", "Strongest axis leverage करें और weakest behavior loop को patch करें।")
    payloads["name_number_analysis"] = _section_payload("name_number_analysis", f"Current name vibration {name_number}, compound {name_compound} ({_compound_meaning(name_compound)}).", "Name signal is active but partially optimized.", "Name frequency impacts authority and trust perception.", "Mismatch can suppress social clarity and strategic momentum.", "Move toward target-aligned spelling where practical.", [{"label": "Current Name Number", "value": str(name_number)}, {"label": "Strength", "value": name_trait['strength']}, {"label": "Risk", "value": name_trait['risk']}, {"label": "Target Numbers", "value": ', '.join(str(value) for value in name_targets)}], [f"Option {index + 1}: {item['option']} -> {item['number']}" for index, item in enumerate(name_options)])
    payloads["birth_date_numerology"] = _section_payload("birth_date_numerology", f"Birth pattern and personal year {personal_year} define timing quality.", "Birth-date rhythm indicates cycle-based opportunities and caution windows.", "Day, month, and year roots shape recurring behavior cadence.", "Cycle alignment improves clarity and reduces decision friction.", "Schedule major actions in favorable date windows.", [{"label": "Favorable Dates", "value": ', '.join(str(v) for v in lucky_dates)}])
    payloads["loshu_grid_intelligence"] = _section_payload("loshu_grid_intelligence", f"Lo Shu present: {', '.join(str(v) for v in loshu_present) or 'none'} | missing: {', '.join(str(v) for v in loshu_missing) or 'none'}.", "Lo Shu reveals naturally available energies and missing capacities.", "Digit distribution maps communication, discipline, and adaptability.", "Missing center/communication digits can amplify instability.", "Target missing number themes with habit-based correction protocol.")
    payloads["karmic_pattern_intelligence"] = _section_payload("karmic_pattern_intelligence", f"Karmic indicators: {', '.join(str(v) for v in karmic_numbers) if karmic_numbers else 'none explicit'}.", "Karmic numbers indicate recurring lesson loops.", "Date and compound patterns repeat during stress cycles.", "Unresolved loops delay consistency and compounding progress.", "Attach one behavior protocol to each active karmic pattern.")
    payloads["hidden_talent_intelligence"] = _section_payload("hidden_talent_intelligence", f"Hidden Passion number {hidden_passion_number} indicates edge in {hidden_talent_trait}.", "Latent skill axis is visible in number-dominance patterns.", "Core and grid signals create compounding potential.", "When activated, this axis boosts speed and confidence.", "Convert hidden talent into weekly measurable outputs.")
    payloads["personal_year_forecast"] = _section_payload("personal_year_forecast", f"Personal year {personal_year} indicates correction-led growth and consolidation.", f"Current cycle number {personal_year} defines the year theme.", "Personal year derives from birth day/month and current year.", "Cycle awareness improves effort-to-result ratio.", "Use favorable dates for launches and directional decisions.")
    payloads["lucky_numbers_favorable_dates"] = _section_payload("lucky_numbers_favorable_dates", "Lucky logic is scheduling calibration, not superstition.", "Selected numbers and dates show higher profile resonance.", "They align with life-path and destiny rhythm.", "Timing alignment can improve confidence and outcomes.", "Use these windows for high-impact actions.", [{"label": "Lucky Numbers", "value": ', '.join(str(v) for v in name_targets[:4])}, {"label": "Favorable Dates", "value": ', '.join(str(v) for v in lucky_dates)}])
    payloads["basic_remedies"] = _section_payload("basic_remedies", "Basic remedies are behavior anchors designed for consistency.", f"Weakest metric {weakest_metric.lower()} requires stabilization.", "Profile sensitivity increases when routine breaks under stress.", "Instability affects strategic clarity and follow-through.", f"{lifestyle_protocol} | {digital_protocol}", bullets=[f"Mantra code: {vedic_code}", f"Practice: {vedic_parameter}", f"Output: {vedic_output}"])
    payloads["archetype_intelligence"] = _section_payload("archetype_intelligence", f"{first_name} archetype blends {name_strength} with risk of {name_risk}.", "Archetype signature shows strategic upside with discipline dependency.", "Core numbers combine analytical depth and adaptive drive.", "Leadership impact depends on rhythm and message clarity.", name_trait["protocol"])
    payloads["career_intelligence"] = _section_payload("career_intelligence", f"Career alignment {career_industry} में ownership-driven roles के साथ strongest दिखता है।", "Growth curve strategic responsibility और measurable outcomes को favor करता है।", "Life-path और expression alignment depth-based execution को reward करता है।", "Role mismatch होने पर effort तो लगता है, पर compounding नहीं बनती।", "ऐसे roles चुनें जिनमें authority, visibility, और accountability स्पष्ट हो।")
    payloads["financial_intelligence"] = _section_payload("financial_intelligence", f"Financial signal: discipline score {_safe_int(scores.get('financial_discipline_index'), 50)} और protocol-first improvement path।", "Financial behavior correction-ready है, पर structure dependency अधिक है।", "Metric stack stress phase में discipline variance दिखाता है।", "Protocol के बिना growth reactive decisions में leak हो सकती है।", "Budget checkpoints और monthly capital review तुरंत install करें।")
    payloads["numerology_architecture"] = _section_payload("numerology_architecture", f"Architecture: Foundation {life_path}, Left Pillar {destiny}, Right Pillar {expression}, Facade {name_number}.", "Core numbers form a unified structural blueprint.", "Each pillar controls direction, execution, and projection.", "Misalignment appears as confidence drift and inconsistency.", "Align corrections (name/mobile/email) to this architecture.")
    payloads["planetary_influence"] = _section_payload("planetary_influence", f"Primary intervention planet: {dominant_planet}.", "Planetary mapping is calibration lens, not fate prediction.", "Core numbers amplify one intervention channel in current cycle.", "Ignoring it increases friction in decision and emotional domains.", "Anchor routines and remedies to intervention-planet discipline.")
    payloads["compatibility_intelligence"] = _section_payload("compatibility_intelligence", _safe_text(compatibility.get("relationship_guidance"), f"Compatibility strongest with profiles reinforcing {strongest_metric.lower()} and reducing pressure on {weakest_metric.lower()}"), "Compatibility signal highlights support and friction patterns.", "Number resonance influences communication pace and expectation alignment.", "Mismatch can drain energy in personal and business collaborations.", "Prioritize partnerships that reinforce strengths and de-risk deficits.")
    payloads["life_cycle_timeline"] = _section_payload("life_cycle_timeline", "Life cycle timeline maps foundation, expansion, and integration phases.", "Current phase requires correction-led consolidation before aggressive scaling.", "Pinnacle progression and personal-year rhythm indicate sequencing needs.", "Right sequencing improves long-term optionality and stability.", "Plan in three phases: stabilize, optimize, scale.")
    payloads["pinnacle_challenge_cycle_intelligence"] = _section_payload("pinnacle_challenge_cycle_intelligence", f"Pinnacles {pinnacle['pinnacles']} | Challenges {pinnacle['challenges']}.", "Pinnacle cycles define opportunities; challenge cycles define resistance.", "Date-derived reductions map developmental sequence.", "Ignoring challenge signatures repeats avoidable errors.", "Match strategy to active pinnacle and neutralize challenge traits.")
    payloads["strategic_guidance"] = _section_payload("strategic_guidance", "Strategic guidance converts numerology into operating decisions.", "System requires correction-first execution before scale expansion.", f"Risk band {risk_band} and weakest axis {weakest_metric.lower()} require stabilization.", "Correct sequence improves clarity and timing quality.", "Run correction stack: behavior -> identity -> timing -> scale.")
    payloads["name_vibration_optimization"] = _section_payload("name_vibration_optimization", f"Current name number {name_number}, compound {name_compound} ({_compound_meaning(name_compound)}).", "Name vibration is active but partially optimized for strategic goals.", "Name frequency encodes authority and trust signal.", "Suboptimal signal can reduce conversion quality and momentum.", "Adopt target-aligned variants where commercial context justifies.", [{"label": "Current Number", "value": str(name_number)}, {"label": "Target Numbers", "value": ', '.join(str(v) for v in name_targets)}, {"label": "Strength", "value": name_trait['strength']}, {"label": "Risk", "value": name_trait['risk']}], [f"Option {index + 1}: {item['option']} -> {item['number']}" for index, item in enumerate(name_options)])
    payloads["mobile_number_intelligence"] = _section_payload("mobile_number_intelligence", mobile_summary, f"Current mobile vibration {mobile_vibration} with {mobile_compatibility} compatibility.", "Mobile frequency influences communication and response cadence.", "Misalignment may increase noise or decision fatigue.", "Shift to supportive ending patterns when feasible.", [{"label": "Current Mobile", "value": mobile_value or 'Not provided'}, {"label": "Target Vibrations", "value": ', '.join(str(v) for v in mobile_supportive[:4])}, {"label": "Ending Logic", "value": "Prefer final digits matching supportive triad"}])
    payloads["email_identity_intelligence"] = _section_payload("email_identity_intelligence", f"Current email vibration {email_vibration} shapes digital authority signal.", "Digital identity is active but can be optimized for trust and visibility.", "Email local-part vibration affects first-impression coding.", "Weak signal can lower credibility and response quality.", "Use cleaner naming pattern aligned with target profile numbers.", [{"label": "Current Email", "value": email_value or 'Not provided'}, {"label": "Email Vibration", "value": str(email_vibration or 0)}, {"label": "Authority Signal", "value": 'High' if email_vibration in {1, 8, 9, 22} else 'Moderate'}], [f"Suggested pattern: {pattern}" for pattern in _handle_patterns(first_name, name_targets)])
    payloads["signature_intelligence"] = _section_payload("signature_intelligence", "Signature energy should communicate authority with controlled flow and completion.", "Current signature behavior can be optimized for growth alignment.", "Stroke structure encodes confidence and decision intent.", "Weak structure can dilute authority signal.", "Use rising start, stable midline, and forward closure stroke.", [{"label": "Starting Stroke", "value": "Begin upward, avoid backward hooks"}, {"label": "Ending Stroke", "value": "Close forward-right with complete finish"}, {"label": "Authority Alignment", "value": 'High' if name_number in {1, 8, 9, 22} else 'Moderate'}])
    payloads["business_name_intelligence"] = _section_payload("business_name_intelligence", f"Business vibration {business_number or 0}, compound {business_compound or 0}, signal: {business_strength}.", "Business name signal affects commercial trust and positioning.", "Brand vibration influences category fit and conversion texture.", "Misalignment can reduce pricing power and authority velocity.", "Adjust naming pattern toward target commercial numbers when required.", [{"label": "Business Name", "value": business_name or 'Not provided'}, {"label": "Industry Fit", "value": ', '.join(business_industries[:3])}, {"label": "Risk", "value": business_risk}])

    handle_source = domain_handle or social_handle or first_name
    handle_vibration = _vibration_from_text(handle_source)
    payloads["brand_handle_optimization"] = _section_payload("brand_handle_optimization", f"Current handle/domain vibration {handle_vibration or 0} should align with visibility strategy.", "Public handle signal can be optimized for trust and discoverability.", "Handle vibration influences memorability and social proof perception.", "Weak naming logic lowers visibility consistency.", "Unify handle/domain root with target vibration endings.", [{"label": "Social Handle", "value": social_handle or 'Not provided'}, {"label": "Domain Handle", "value": domain_handle or 'Not provided'}, {"label": "Authority Signal", "value": 'High' if handle_vibration in {1, 8, 9, 22} else 'Moderate'}], [f"Improved pattern: {pattern}" for pattern in _handle_patterns(handle_source, name_targets)])
    payloads["residence_energy_intelligence"] = _section_payload("residence_energy_intelligence", f"Residence vibration {residence_vibration or 0} affects baseline stability signal.", "Home number creates recurring environmental energy tone.", "Repeated daily exposure amplifies behavior feedback.", "Misfit vibration can reduce recovery quality and clarity.", "Apply symbolic balancing with plate letters and entrance corrections.", [{"label": "Current Residence Number", "value": residence_number or 'Not provided'}, {"label": "Residence Vibration", "value": str(residence_vibration or 0)}])
    payloads["vehicle_number_intelligence"] = _section_payload("vehicle_number_intelligence", f"Vehicle vibration {vehicle_vibration or 0} influences movement tone and confidence expression.", "Vehicle number creates recurring movement-state signal.", "Travel frequency amplifies vibration feedback into transitions.", "Misalignment may increase urgency bias and reactive behavior.", "Prefer compatible number logic during selection or correction.", [{"label": "Current Vehicle Number", "value": vehicle_number or 'Not provided'}, {"label": "Vehicle Vibration", "value": str(vehicle_vibration or 0)}])
    payloads["lifestyle_alignment"] = _section_payload("lifestyle_alignment", "Lifestyle alignment strategic infrastructure है, सिर्फ wellness filler नहीं।", f"Weakest metric {weakest_metric.lower()} को rhythm-led stabilization चाहिए।", "Routine disruption cognitive noise और volatility बढ़ाता है।", "यह instability clarity, discipline, और execution quality को प्रभावित करती है।", lifestyle_protocol)
    payloads["digital_discipline"] = _section_payload("digital_discipline", "Digital behavior सीधे decision quality और recovery को shape करता है।", "Notification overload एक hidden performance drain है।", "High-frequency context switching deficit metrics को amplify करता है।", "इसके बाद reactive decisions और deep-work quality में गिरावट दिखती है।", digital_protocol)
    payloads["vedic_remedy"] = _section_payload("vedic_remedy", "Vedic protocol is focus-conditioning and discipline anchor.", "Current profile benefits from ritualized consistency loops.", "Weakest metric and dominant planet point to intervention need.", "Improves composure and timing discipline.", f"Code: {vedic_code} | Parameter: {vedic_parameter}", [{"label": "Focus", "value": weakest_metric}, {"label": "Code", "value": vedic_code}, {"label": "Parameter", "value": vedic_parameter}, {"label": "Output", "value": vedic_output}])
    payloads["correction_protocol_summary"] = _section_payload("correction_protocol_summary", "Correction protocol ranks interventions by impact on stability and monetizable outcomes.", "Multiple correction levers exist and must be sequenced.", "Weakest metric and identity-signal gaps define order.", "Correct sequencing improves measurable improvement speed.", "Execute 21-day and 90-day checkpoints with priority order.", [{"label": "Top Priority", "value": correction_priority_lines[0]}, {"label": "High-Impact Quick Fixes", "value": ' | '.join(correction_priority_lines[:2])}, {"label": "Medium-Term Adjustments", "value": "Email identity, signature protocol, environment alignment"}, {"label": "Premium Advisory", "value": "Run full correction audit quarterly"}], correction_priority_lines)
    payloads["business_intelligence"] = _section_payload("business_intelligence", f"Business signal: {business_strength}. Risk gate: {business_risk}.", "Commercial upside exists with correction-led governance discipline.", "Business vibration and metric stack indicate potential with pressure constraints.", "Without structure, growth can convert into volatility.", "Align offer, pricing, and positioning to cycle window.")
    payloads["wealth_energy_blueprint"] = _section_payload("wealth_energy_blueprint", f"Wealth blueprint: financial discipline {_safe_int(scores.get('financial_discipline_index'), 50)} with business vibration {business_number or 'N/A'}.", "Wealth path depends on behavior architecture.", "Financial metric and identity signals define compounding quality.", "Protocol failure causes leak in high-income phases.", "Use monthly capital governance and staged risk model.")
    payloads["decision_intelligence"] = _section_payload("decision_intelligence", "Decision intelligence को filters, delay rules, और review loops से engineer किया जाता है।", "Current profile में capability है, पर stress phase inconsistency भी है।", f"Weakest metric {weakest_metric.lower()} high load में decision noise बढ़ाता है।", "Fast और unfiltered calls opportunity cost बढ़ाती हैं।", decision_protocol)
    payloads["emotional_intelligence"] = _section_payload("emotional_intelligence", "Emotional regulation strategic performance infrastructure का core हिस्सा है।", "Recovery speed एक variable risk factor की तरह काम करती है।", "Metric pattern बताता है कि rhythm टूटने पर reactive windows बढ़ती हैं।", "इसका प्रभाव clarity, relationships, और financial discipline पर पड़ता है।", emotional_protocol)
    payloads["leadership_intelligence"] = _section_payload("leadership_intelligence", "Leadership signal should combine authority with stable execution cadence.", "Leadership potential is high but governance rhythm is mandatory.", "Core numbers indicate strategic strength with overextension risk.", "Inconsistent cadence reduces trust and execution velocity.", "Weekly leadership protocol: priorities, delegation, review, recovery.")
    payloads["strategic_timing_intelligence"] = _section_payload("strategic_timing_intelligence", "Timing intelligence calibrates when to push, pause, and consolidate.", "Decision quality varies by cycle windows and date resonance.", "Personal-year and pinnacle sequences define timing intensity.", "Poor timing increases effort with lower conversion.", "Use favorable dates for launches and negotiations.", [{"label": "Current Personal Year", "value": str(personal_year)}, {"label": "Favorable Dates", "value": ', '.join(str(v) for v in lucky_dates)}])
    payloads["growth_blueprint"] = _section_payload("growth_blueprint", "Growth blueprint sequences stabilize -> optimize -> scale.", "Current phase is correction-led stabilization before aggressive expansion.", f"Risk band {risk_band} requires structural readiness before scale.", "Premature expansion can lock volatility into operations.", "Run staged roadmap with gate checks across 90 days.")
    payloads["strategic_execution_roadmap"] = _section_payload("strategic_execution_roadmap", "Execution roadmap converts intelligence into a 90-day operating system.", "Multiple interventions need coordinated sequencing.", "Correction outcomes compound only in operational order.", "Unsequenced action wastes effort and obscures ROI.", "Days 1-30 stabilize, 31-60 optimize, 61-90 scale tests.", bullets=["Days 1-30: metric deficit stabilization and behavior lock.", "Days 31-60: identity corrections (name/mobile/email/signature).", "Days 61-90: timing alignment and controlled scale tests."])
    payloads["closing_synthesis"] = _section_payload("closing_synthesis", f"Final synthesis: {full_name} में clear leverage potential है, यदि correction priorities को disciplined execution के साथ चलाया जाए।", "Profile calibration-sensitive है, fundamentally blocked नहीं।", "Strength-deficit architecture स्पष्ट है और सही sequence से correct की जा सकती है।", "Protocol-led execution constraints को strategic advantage में बदल सकता है।", "Correction stack, timing control, और quarterly recalibration पर committed रहें।")

    if plan_name == "basic":
        mulank = _reduce_number(day)
        bhagyank = life_path or _reduce_number(day + month + _reduce_number(year))
        interaction_gap = abs((mulank or 0) - (bhagyank or 0))
        interaction_state = "संतुलित" if interaction_gap <= 2 else "विरोधी संकेत"
        repeating_numbers = [
            number
            for number in range(1, 10)
            if _safe_int(grid_counts.get(str(number), grid_counts.get(number, 0)), 0) > 1
        ]
        repeating_text = ", ".join(str(number) for number in repeating_numbers) if repeating_numbers else "कोई प्रमुख पुनरावृत्ति नहीं"
        mobile_classification = "supportive" if mobile_vibration in {mulank, bhagyank, destiny} else "neutral"
        email_available = bool(email_value)
        color_base = (name_number or bhagyank or mulank or 5)
        color_map = {
            1: ("gold, saffron", "dark grey"),
            2: ("white, silver", "muddy brown"),
            3: ("yellow, honey", "dull black"),
            4: ("smoky blue, graphite", "neon red"),
            5: ("green, mint", "overly dark maroon"),
            6: ("cream, rose", "charcoal black"),
            7: ("sea green, turquoise", "rust orange"),
            8: ("navy, steel blue", "faded yellow"),
            9: ("maroon, crimson", "pale grey"),
        }
        favorable_colors, caution_colors = color_map.get(color_base, ("green, blue", "muddy grey"))
        mulank_trait = NUMBER_TRAITS.get(mulank, NUMBER_TRAITS[5])
        bhagyank_trait = NUMBER_TRAITS.get(bhagyank, NUMBER_TRAITS[5])
        focus_key = _safe_text((intake_context.get("focus") or {}).get("life_focus"), "general_alignment")
        focus_text = focus_key.replace("_", " ")
        city_hint = _safe_text(birth_details.get("birthplace_city") or identity.get("city"), "local environment")
        compatibility_level = _safe_text((numerology_core.get("compatibility") or {}).get("compatibility_level"), "Moderate")

        basic_payloads: Dict[str, Any] = {}
        basic_payloads["executive_numerology_summary"] = _section_payload(
            "executive_numerology_summary",
            f"{full_name} की numerology profile का मूल स्वर {mulank}-{bhagyank}-{name_number or '-'} संयोजन पर आधारित है। मुख्य ताकत {strongest_metric} और चुनौती {weakest_metric} है। वर्तमान focus: {focus_text}.",
            "Core number stack से quick nature signal स्पष्ट है।",
            "मूलांक, भाग्यांक और नामांक का संयुक्त प्रभाव baseline behavior तय करता है।",
            f"इसका असर निर्णय, संबंध, दिनचर्या और execution consistency पर पड़ता है, खासकर {city_hint} जैसे environment में।",
            f"पहली correction priority: {weakest_metric.lower()} stabilization और missing number discipline।",
        )
        basic_payloads["core_numbers_analysis"] = _section_payload(
            "core_numbers_analysis",
            f"Mulank {mulank}, Bhagyank {bhagyank}, Destiny {destiny}, Expression {expression}.",
            "ये चार संख्या आपकी आधार संरचना दिखाती हैं।",
            "जन्मतिथि और नाम vibration से ये numbers deterministic तरीके से निकलते हैं।",
            "व्यक्तित्व, अवसर और चुनौतियों का मुख्य pattern यही तय करता है।",
            "हर weekly review में इन numbers के basis पर self-observation करें।",
        )
        basic_payloads["name_number_analysis"] = _section_payload(
            "name_number_analysis",
            f"नामांक {name_number} और compound {name_compound} आपके पहचान संकेत को प्रभावित करते हैं।",
            "नाम संख्या आपके social impression और communication tone को दर्शाती है।",
            "अक्षर-वाइब्रेशन से बना total आपकी पहचान की स्थिरता और trust signal तय करता है।",
            "नाम और मूलांक/भाग्यांक में mismatch होने पर clarity और confidence प्रभावित हो सकते हैं।",
            "नाम उपयोग में consistency रखें और practical होने पर target-friendly spelling अपनाएं।",
            [
                {"label": "Current Name Number", "value": str(name_number)},
                {"label": "Strength", "value": name_trait["strength"]},
                {"label": "Risk", "value": name_trait["risk"]},
            ],
            [f"विकल्प {index + 1}: {item['option']} -> {item['number']}" for index, item in enumerate(name_options)],
        )
        basic_payloads["mulank_description"] = _section_payload(
            "mulank_description",
            f"Mulank {mulank} आपकी instinctive response style और daily behavior tone को दर्शाता है। यह {mulank_trait['strength']} को बढ़ाता है और {mulank_trait['risk']} tendency दिखा सकता है।",
            "मूलांक आपकी natural प्रतिक्रिया और प्राथमिकता pattern दिखाता है।",
            "दिनांक जन्म का root number सीधे personality reflexes से जुड़ता है।",
            "Strengths और blind spots दैनिक फैसलों में बार-बार दिखते हैं।",
            "मूलांक strength को routine में उपयोग करें और weakness पर habit correction लगाएं।",
        )
        basic_payloads["bhagyank_description"] = _section_payload(
            "bhagyank_description",
            f"Bhagyank {bhagyank} life path theme, growth direction और recurring lesson cycle को define करता है। इसका core strength {bhagyank_trait['strength']} है।",
            "भाग्यांक long-term direction और opportunity flow का संकेत देता है।",
            "पूरा जन्मांक योग (life path) से destiny pattern निकलता है।",
            f"गलत timing या discipline gap होने पर growth धीमी हो सकती है और {bhagyank_trait['risk']} बढ़ सकता है।",
            f"व्यक्तिगत वर्ष {personal_year} और भाग्यांक को जोड़कर yearly focus तय करें।",
        )
        basic_payloads["number_interaction_analysis"] = _section_payload(
            "number_interaction_analysis",
            f"Mulank {mulank}, Bhagyank {bhagyank}, Name Number {name_number or '-'} के बीच {interaction_state} pattern दिखाई देता है (gap {interaction_gap}).",
            "Numbers में harmony या conflict execution style बदलता है।",
            "जब root numbers दूर होते हैं तो behavior में friction बढ़ता है।",
            "फोकस, confidence और consistency पर सीधा प्रभाव पड़ता है।",
            "अगर conflict है तो routine, mantra और number-aligned habit से correction करें।",
        )
        basic_payloads["loshu_grid_interpretation"] = _section_payload(
            "loshu_grid_interpretation",
            f"Lo Shu present: {', '.join(str(v) for v in loshu_present) or 'none'} | missing: {', '.join(str(v) for v in loshu_missing) or 'none'}.",
            "Lo Shu grid ऊर्जा layout को practical रूप से दिखाता है।",
            "जन्मांक digit distribution से present और missing energies निकलती हैं।",
            "Present numbers natural strengths और missing numbers correction areas बताते हैं।",
            "Grid reading को weekly behavior tracking से validate करें।",
        )
        basic_payloads["missing_numbers_analysis"] = _section_payload(
            "missing_numbers_analysis",
            f"Missing numbers: {', '.join(str(v) for v in loshu_missing) if loshu_missing else 'none'}.",
            "Missing numbers संभावित behavior gaps को दिखाते हैं।",
            "इन digits की कमी communication, flexibility या discipline gaps में दिख सकती है।",
            "गैप untreated रहे तो repeat friction बनता है।",
            "हर missing digit के लिए एक micro-habit correction निर्धारित करें।",
            [f"Missing {number}: structured correction routine आवश्यक." for number in loshu_missing[:5]],
        )
        basic_payloads["repeating_numbers_impact"] = _section_payload(
            "repeating_numbers_impact",
            f"Repeating numbers pattern: {repeating_text}.",
            "Repeated digits amplified traits दिखाते हैं।",
            "एक ही digit का बार-बार आना excess tendency को मजबूत करता है।",
            "Overuse होने पर rigidity, impulsivity या overthinking उभर सकता है।",
            "Amplified trait को balance करने के लिए opposite habit anchor जोड़ें।",
        )
        basic_payloads["mobile_number_numerology"] = _section_payload(
            "mobile_number_numerology",
            f"Mobile vibration {mobile_vibration} का classification: {mobile_classification}.",
            "मोबाइल vibration daily communication tone को प्रभावित करता है।",
            "Digit sum vibration profile numbers के साथ resonance बनाता या घटाता है।",
            "Conflicting vibration होने पर distraction और clarity drop हो सकती है।",
            "Supportive ending pattern चुनें और usage discipline maintain रखें।",
            [{"label": "Current Mobile", "value": mobile_value or "इनपुट उपलब्ध नहीं"}],
        )
        basic_payloads["mobile_life_number_compatibility"] = _section_payload(
            "mobile_life_number_compatibility",
            f"Mobile vibration {mobile_vibration} बनाम life numbers {mulank}/{bhagyank}: {mobile_classification}.",
            "यह सेक्शन mobile और life-number relationship को simple तरीके से पढ़ता है।",
            "Compatibility resonance जितनी बेहतर होगी, communication clarity उतनी smooth रहती है।",
            "Mismatch होने पर response fatigue या decision delay बढ़ सकता है।",
            "यदि mismatch है तो अगली SIM update में supportive digit logic चुनें।",
        )
        basic_payloads["email_numerology"] = _section_payload(
            "email_numerology",
            f"Email vibration {email_vibration or 0} trust, clarity और digital identity signal को प्रभावित करता है।" if email_available else "ईमेल इनपुट उपलब्ध नहीं है, इसलिए अभी detailed email numerology analysis सीमित है।",
            "Email local-part भी एक numerology identity layer मानी जाती है।",
            "Vibration authority perception और response quality पर प्रभाव डालती है।",
            "Weak pattern होने पर digital signal dilute हो सकता है।",
            "Email उपलब्ध होने पर clean pattern के साथ optimized सुझाव generate करें।",
            [{"label": "Current Email", "value": email_value or "इनपुट उपलब्ध नहीं"}],
        )
        basic_payloads["numerology_personality_profile"] = _section_payload(
            "numerology_personality_profile",
            f"Personality profile में {name_strength} प्रमुख है, जबकि {name_risk} internal blind spot की तरह दिखता है।",
            "Numbers social style, inner nature और reaction pattern को summarize करते हैं।",
            "Mulank + Name Number का मिश्रण interpersonal tone तय करता है।",
            "Blind spots unmanaged रहें तो relationship और confidence दोनों प्रभावित होते हैं।",
            "Strength-driven behavior रखें और blind spot पर conscious pause rule लगाएं।",
        )
        basic_payloads["current_life_phase_insight"] = _section_payload(
            "current_life_phase_insight",
            f"Current life phase theme: personal year {personal_year} और risk band {risk_band}.",
            "यह phase correction-led stabilization और clarity building का संकेत देता है।",
            "Personal year और number interaction इस समय की priority तय करते हैं।",
            "Wrong focus चुनने पर effort high और output low रह सकता है।",
            "इस phase में consistency, timing और disciplined decisions पर फोकस रखें।",
        )
        basic_payloads["career_financial_tendencies"] = _section_payload(
            "career_financial_tendencies",
            f"Career tendency {career_industry} orientation के साथ और financial discipline score {_safe_int(scores.get('financial_discipline_index'), 50)} के आसपास है। यह {focus_text} लक्ष्य के लिए उपयोगी संकेत देता है।",
            "यह section केवल numerology-based tendencies बताता है, consulting strategy नहीं।",
            "Work style, routine discipline और number resonance earning pattern को shape करते हैं।",
            "Reactive style होने पर income consistency प्रभावित हो सकती है।",
            "Skill depth, role-fit और money routine पर steady focus रखें।",
        )
        basic_payloads["relationship_compatibility_patterns"] = _section_payload(
            "relationship_compatibility_patterns",
            f"{compatibility_summary} Current compatibility level: {compatibility_level}.",
            "Relationship pattern में emotional style और number resonance दोनों काम करते हैं।",
            "Compatibility tendency communication pace और expectation alignment से बनती है।",
            "Mismatch होने पर repeated misunderstanding cycle बन सकता है।",
            "Clear boundaries, calm communication और timing awareness रखें।",
        )
        basic_payloads["health_tendencies_from_numbers"] = _section_payload(
            "health_tendencies_from_numbers",
            f"Emotional regulation score {_safe_int(scores.get('emotional_regulation_index'), 50)} और karma pressure {_safe_int(scores.get('karma_pressure_index'), 50)} stress tendency की दिशा दिखाते हैं। सबसे संवेदनशील axis: {weakest_metric}.",
            "यह numerology-based wellness tendency है, medical diagnosis नहीं।",
            "Number imbalance sleep rhythm, stress response और recovery pattern प्रभावित कर सकता है।",
            "अवहेलना करने पर fatigue और decision quality दोनों गिर सकते हैं।",
            "Breath reset, sleep discipline और low-noise routine अपनाएं।",
        )
        basic_payloads["personal_year_forecast"] = _section_payload(
            "personal_year_forecast",
            f"वर्तमान personal year {personal_year} इस वर्ष की गति और प्राथमिकता तय करता है।",
            f"Year {personal_year} में focus theme correction + consistency है।",
            "Personal year जन्म दिन, माह और वर्तमान वर्ष के योग से बनता है।",
            "सही timing चुनने पर effort का परिणाम बेहतर मिलता है।",
            "महत्वपूर्ण decisions और launches को favorable date windows में रखें।",
            [
                {"label": "Current Personal Year", "value": str(personal_year)},
                {"label": "Favorable Dates", "value": ", ".join(str(v) for v in lucky_dates)},
            ],
        )
        basic_payloads["lucky_numbers_favorable_dates"] = _section_payload(
            "lucky_numbers_favorable_dates",
            f"Supportive numbers: {', '.join(str(v) for v in name_targets[:4]) or '3, 5, 9'} | favorable dates: {', '.join(str(v) for v in lucky_dates)}.",
            "यह superstition नहीं, बल्कि numerology timing utility है।",
            "मूलांक, भाग्यांक और नामांक resonance से कुछ तिथियां अधिक supportive रहती हैं।",
            "गलत timing में वही प्रयास धीमा या थकाऊ लग सकता है।",
            "महत्वपूर्ण meeting, outreach और नई शुरुआत supportive dates पर करें।",
            [
                {"label": "Lucky Numbers", "value": ", ".join(str(v) for v in name_targets[:4]) or "3, 5, 9"},
                {"label": "Favorable Dates", "value": ", ".join(str(v) for v in lucky_dates)},
            ],
        )
        basic_payloads["color_alignment"] = _section_payload(
            "color_alignment",
            f"Favorable colors: {favorable_colors}. Caution colors: {caution_colors}.",
            "Color alignment numerology support layer की तरह काम करती है।",
            "Dominant number vibration से aligned tones focus और steadiness बढ़ा सकते हैं।",
            "Mismatched color overuse से energy tone dull हो सकती है।",
            "Primary wardrobe/workspace में favorable tones का controlled use करें।",
        )
        basic_payloads["remedies_lifestyle_adjustments"] = _section_payload(
            "remedies_lifestyle_adjustments",
            f"Basic correction layer = simple mantra + disciplined habit + lifestyle alignment. Dominant planet support: {dominant_planet}.",
            "Remedies को practical routine के साथ जोड़ना सबसे प्रभावी रहता है।",
            "Consistency के बिना remedy signal कमजोर हो जाता है।",
            "Irregular practice से correction outcome धीमा पड़ता है।",
            "Daily short mantra, fixed routine, और weekly review रखें।",
            [
                f"Mantra: {vedic_code}",
                f"Practice: {vedic_parameter}",
                f"Lifestyle: {lifestyle_protocol}",
            ],
        )
        basic_payloads["closing_numerology_guidance"] = _section_payload(
            "closing_numerology_guidance",
            f"Main life theme: {bhagyank} path refinement with {mulank} day-expression and name signal {name_number}. Primary correction: {weakest_metric}.",
            "आपकी numerology profile workable और correctable है।",
            "Core numbers, Lo Shu gaps और daily habits का जोड़ final outcome तय करता है।",
            "Correction priority ignore करने पर repeat cycle बन सकता है।",
            "Next best step: 21-day correction routine + monthly numerology review.",
        )

        payloads.update(basic_payloads)

        # Backward-compatible aliases consumed by current template/context layers.
        payloads["executive_summary"] = basic_payloads["executive_numerology_summary"]
        payloads["core_numerology_numbers"] = basic_payloads["core_numbers_analysis"]
        payloads["birth_date_numerology"] = basic_payloads["current_life_phase_insight"]
        payloads["loshu_grid_intelligence"] = basic_payloads["loshu_grid_interpretation"]
        payloads["mobile_number_intelligence"] = basic_payloads["mobile_number_numerology"]
        payloads["email_identity_intelligence"] = basic_payloads["email_numerology"]
        payloads["archetype_intelligence"] = basic_payloads["numerology_personality_profile"]
        payloads["career_intelligence"] = basic_payloads["career_financial_tendencies"]
        payloads["financial_intelligence"] = basic_payloads["career_financial_tendencies"]
        payloads["decision_intelligence"] = basic_payloads["number_interaction_analysis"]
        payloads["emotional_intelligence"] = basic_payloads["health_tendencies_from_numbers"]
        payloads["compatibility_intelligence"] = basic_payloads["relationship_compatibility_patterns"]
        payloads["lifestyle_alignment"] = basic_payloads["remedies_lifestyle_adjustments"]
        payloads["basic_remedies"] = basic_payloads["remedies_lifestyle_adjustments"]
        payloads["closing_synthesis"] = basic_payloads["closing_numerology_guidance"]

    payloads = _ensure_all_payloads(plan_name, payloads)
    payloads = _localize_payloads(payloads)

    primary_insight = {
        "core_archetype": _safe_text(archetype.get("archetype_name"), "रणनीतिक अनुकूल archetype"),
        "strength": f"Primary strength axis: {strongest_metric}",
        "critical_deficit": f"Primary deficit axis: {weakest_metric}",
        "stability_risk": risk_band,
        "phase_1_diagnostic": "Phase 1: deficit triggers diagnose करके baseline behaviors lock करें।",
        "phase_2_blueprint": "Phase 2: architecture-aligned identity corrections deploy करें।",
        "phase_3_intervention_protocol": "Phase 3: 90-day timing-calibrated execution protocol चलाएं।",
        "narrative": payloads["executive_summary"]["narrative"],
    }

    executive_brief = {
        "summary": payloads["executive_summary"]["narrative"],
        "key_strength": primary_insight["strength"],
        "key_risk": primary_insight["critical_deficit"],
        "strategic_focus": intervention_focus,
    }

    analysis_sections = {
        "career_analysis": payloads["career_intelligence"]["narrative"],
        "decision_profile": payloads["decision_intelligence"]["narrative"],
        "emotional_analysis": payloads["emotional_intelligence"]["narrative"],
        "financial_analysis": payloads["financial_intelligence"]["narrative"],
    }

    strategic_guidance = {
        "short_term": "Short term में weakest metric को low-noise behavior protocol से stabilize करें।",
        "mid_term": "Mid term में identity corrections deploy करके behavior delta measure करें।",
        "long_term": "Long term scale के लिए strategic timing और quarterly recalibration रखें।",
    }

    growth_blueprint = {
        "phase_1": "Days 1-30: deficit behavior stabilize करके baseline lock करें।",
        "phase_2": "Days 31-60: identity और environment पर correction stack deploy करें।",
        "phase_3": "Days 61-90: timing-aligned growth experiments execute करें।",
    }

    if plan_name == "basic":
        primary_insight = {
            "core_archetype": _safe_text(archetype.get("archetype_name"), "मूल अंक व्यक्तित्व"),
            "strength": f"मुख्य ताकत: {strongest_metric}",
            "critical_deficit": f"मुख्य चुनौती: {weakest_metric}",
            "stability_risk": risk_band,
            "phase_1_diagnostic": "चरण 1: मूलांक और भाग्यांक pattern समझें।",
            "phase_2_blueprint": "चरण 2: missing numbers और routine correction लागू करें।",
            "phase_3_intervention_protocol": "चरण 3: 21-day numerology correction discipline चलाएं।",
            "narrative": payloads["executive_numerology_summary"]["narrative"],
        }
        executive_brief = {
            "summary": payloads["executive_numerology_summary"]["narrative"],
            "key_strength": primary_insight["strength"],
            "key_risk": primary_insight["critical_deficit"],
            "strategic_focus": payloads["remedies_lifestyle_adjustments"]["cards"][3]["value"] if payloads["remedies_lifestyle_adjustments"]["cards"] else intervention_focus,
        }
        strategic_guidance = {
            "short_term": "Mulank-Bhagyank understanding के साथ daily correction शुरू करें।",
            "mid_term": "Missing numbers और repeating traits पर structured balancing करें।",
            "long_term": "Personal year timing के साथ numerology-aligned decisions लें।",
        }
        growth_blueprint = {
            "phase_1": "Week 1: core numbers observation + daily log।",
            "phase_2": "Week 2: missing number correction + routine discipline।",
            "phase_3": "Week 3: mobile/email alignment और follow-through review।",
        }

    business_block = {"business_strength": business_strength, "risk_factor": business_risk, "compatible_industries": business_industries}
    compatibility_block = {"compatible_numbers": [value for value in [life_path, destiny, expression] if value], "challenging_numbers": loshu_missing[:3], "relationship_guidance": compatibility_summary}

    return {
        "primary_insight": primary_insight,
        "metric_explanations": metric_explanations,
        "metrics_spine": {"primary_strength": strongest_metric, "primary_deficit": weakest_metric, "structural_cause": structural_cause, "intervention_focus": intervention_focus, "risk_band": risk_band},
        "numerology_architecture": {"foundation": life_path, "left_pillar": destiny, "right_pillar": expression, "facade": name_number, "narrative": payloads["numerology_architecture"]["narrative"]},
        "archetype_intelligence": {"signature": payloads["archetype_intelligence"]["narrative"], "leadership_traits": name_trait["strength"], "shadow_traits": name_trait["risk"], "growth_path": name_trait["protocol"]},
        "loshu_diagnostic": {"present_numbers": loshu_present, "missing_numbers": loshu_missing, "center_presence": 5 in loshu_present, "energy_imbalance": f"Present {len(loshu_present)} बनाम missing {len(loshu_missing)}.", "missing_number_meanings": [f"Missing {number}: conscious correction protocol बनाएं।" for number in loshu_missing], "narrative": payloads["loshu_grid_intelligence"]["narrative"]},
        "planetary_mapping": {"background_forces": f"Life Path {life_path}, Destiny {destiny}, और Name {name_number} मिलकर {dominant_planet} influence channel बनाते हैं।", "primary_intervention_planet": dominant_planet, "calibration_cluster": "discipline, timing, authority", "narrative": payloads["planetary_influence"]["narrative"]},
        "structural_deficit_model": {"deficit": f"Primary deficit: {weakest_metric}", "symptom": "Stress phase में execution inconsistency और identity mismatch दिखता है।", "patch": intervention_focus, "summary": "Deficit -> behavior risk -> protocol patch sequence को strict order में चलाएं।"},
        "circadian_alignment": {"morning_routine": "10-minute sunlight, breath reset, और strategic priority lock करें।", "work_alignment": "Communication noise से पहले first deep-work block पूरा करें।", "evening_shutdown": "Decision freeze window, digital wind-down, और short review रखें।", "narrative": "Rhythm quality सीधे decision quality को drive करती है।"},
        "environment_alignment": {"physical_space": "Focus और recovery के लिए low-clutter workspace zones बनाएं।", "color_alignment": "Workspace और digital surfaces पर grounded color palette रखें।", "mobile_number_analysis": payloads["mobile_number_intelligence"]["narrative"], "digital_behavior": digital_protocol, "narrative": "Environment का काम friction कम करना और clarity protect करना है।"},
        "vedic_remedy_protocol": {"focus": weakest_metric, "code": vedic_code, "parameter": vedic_parameter, "output": vedic_output, "purpose": "Disciplined intention से deficit metric को stabilize करना।", "planetary_alignment": dominant_planet, "pronunciation": vedic_code},
        "execution_plan": {"install_rhythm": growth_blueprint["phase_1"], "deploy_anchor": growth_blueprint["phase_2"], "run_protocol": growth_blueprint["phase_3"], "checkpoints": ["Week 1: rhythm और metric baseline lock करें।", "Week 2: identity corrections deploy करके behavior delta compare करें।", "Week 3: timing windows validate करके decision quality scale करें।"], "summary": "21-day execution पहले stability बनाता है, फिर strategic expansion को support करता है।"},
        "executive_brief": executive_brief,
        "analysis_sections": analysis_sections,
        "strategic_guidance": strategic_guidance,
        "growth_blueprint": growth_blueprint,
        "business_block": business_block,
        "compatibility_block": compatibility_block,
        "personal_year_forecast": {"current_personal_year": personal_year, "theme": "वर्तमान वर्ष में structure consolidation और correction adoption पर फोकस रखें।", "opportunities": "Aligned launches, cleaner partnerships, और stronger authority signal.", "caution_areas": "High-noise windows में reactive decisions से बचें।", "favorable_dates": lucky_dates},
        "executive_numerology_summary": payloads.get("executive_numerology_summary"),
        "core_numbers_analysis": payloads.get("core_numbers_analysis"),
        "mulank_description": payloads.get("mulank_description"),
        "bhagyank_description": payloads.get("bhagyank_description"),
        "number_interaction_analysis": payloads.get("number_interaction_analysis"),
        "loshu_grid_interpretation": payloads.get("loshu_grid_interpretation"),
        "missing_numbers_analysis": payloads.get("missing_numbers_analysis"),
        "repeating_numbers_impact": payloads.get("repeating_numbers_impact"),
        "mobile_number_numerology": payloads.get("mobile_number_numerology"),
        "mobile_life_number_compatibility": payloads.get("mobile_life_number_compatibility"),
        "email_numerology": payloads.get("email_numerology"),
        "numerology_personality_profile": payloads.get("numerology_personality_profile"),
        "current_life_phase_insight": payloads.get("current_life_phase_insight"),
        "career_financial_tendencies": payloads.get("career_financial_tendencies"),
        "relationship_compatibility_patterns": payloads.get("relationship_compatibility_patterns"),
        "health_tendencies_from_numbers": payloads.get("health_tendencies_from_numbers"),
        "color_alignment": payloads.get("color_alignment"),
        "remedies_lifestyle_adjustments": payloads.get("remedies_lifestyle_adjustments"),
        "closing_numerology_guidance": payloads.get("closing_numerology_guidance"),
        "name_vibration_optimization": payloads["name_vibration_optimization"],
        "mobile_number_intelligence": payloads["mobile_number_intelligence"],
        "email_identity_intelligence": payloads["email_identity_intelligence"],
        "signature_intelligence": payloads.get("signature_intelligence"),
        "business_name_intelligence": payloads.get("business_name_intelligence"),
        "brand_handle_optimization": payloads.get("brand_handle_optimization"),
        "residence_energy_intelligence": payloads.get("residence_energy_intelligence"),
        "vehicle_number_intelligence": payloads.get("vehicle_number_intelligence"),
        "correction_protocol_summary": payloads["correction_protocol_summary"],
        "karmic_pattern_intelligence": payloads["karmic_pattern_intelligence"],
        "hidden_talent_intelligence": payloads["hidden_talent_intelligence"],
        "pinnacle_challenge_cycle_intelligence": payloads["pinnacle_challenge_cycle_intelligence"],
        "life_cycle_timeline": payloads["life_cycle_timeline"],
        "strategic_timing_intelligence": payloads.get("strategic_timing_intelligence"),
        "wealth_energy_blueprint": payloads.get("wealth_energy_blueprint"),
        "leadership_intelligence": payloads.get("leadership_intelligence"),
        "decision_intelligence": payloads.get("decision_intelligence"),
        "emotional_intelligence": payloads.get("emotional_intelligence"),
        "digital_discipline": payloads.get("digital_discipline"),
        "lifestyle_alignment": payloads.get("lifestyle_alignment"),
        "vedic_remedy": payloads.get("vedic_remedy"),
        "closing_synthesis": payloads["closing_synthesis"],
        "section_payloads": payloads,
        "meta_notes": {"dominant_planet": dominant_planet, "strongest_metric": strongest_metric, "strongest_metric_score": strongest_score, "weakest_metric": weakest_metric, "weakest_metric_score": weakest_score, "focus": _safe_text(focus.get("life_focus"), "general_alignment"), "city": city, "career_industry": career_industry, "risk_band": risk_band, "social_handle": social_handle, "domain_handle": domain_handle, "residence_number": residence_number, "vehicle_number": vehicle_number},
    }
