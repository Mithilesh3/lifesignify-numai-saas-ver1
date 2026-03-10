from __future__ import annotations

from typing import Any, Dict, List, Tuple


METRIC_GUIDE: Dict[str, Dict[str, str]] = {
    "life_stability_index": {
        "label": "जीवन स्थिरता | Life Stability",
        "meaning": "यह संकेतक बताता है कि आपका routine, pressure handling और long-term consistency कितनी स्थिर है।",
        "risk": "जब यह score नीचे जाता है, तब execution टूट-टूट कर चलता है और अच्छे अवसर भी fragmented effort में बदल सकते हैं।",
        "improvement": "Sleep rhythm, debt control, emotional recovery और weekly planning को एक साथ improve करने से यह score मजबूत होता है।",
    },
    "confidence_score": {
        "label": "निर्णय स्पष्टता | Decision Clarity",
        "meaning": "यह score दो चीजें दिखाता है: behavioral input कितना पूरा है और आपकी decision visibility कितनी साफ है।",
        "risk": "Low confidence का मतलब यह नहीं कि क्षमता कम है; इसका अर्थ अक्सर यह होता है कि data sparse है या clarity filters अभी weak हैं।",
        "improvement": "Decision journal, written criteria और complete intake signals इस score को जल्दी बेहतर बनाते हैं।",
    },
    "dharma_alignment_score": {
        "label": "धर्म संतुलन | Dharma Alignment",
        "meaning": "यह बताता है कि आपका effort, role choice और inner purpose एक-दूसरे के साथ कितने aligned हैं।",
        "risk": "Low dharma alignment से मेहनत बहुत लगती है लेकिन compounding कम होता है, क्योंकि energy scattered directions में चली जाती है।",
        "improvement": "Role clarity, focus discipline और meaningful work selection इस score के लिए सबसे बड़ा lever है।",
    },
    "emotional_regulation_index": {
        "label": "भावनात्मक संतुलन | Emotional Regulation",
        "meaning": "यह score pressure के दौरान nervous system stability, response quality और recovery speed को reflect करता है।",
        "risk": "यह क्षेत्र कमजोर हो तो अच्छे decisions भी stress phase में reactive बन सकते हैं।",
        "improvement": "Breathwork, lower-noise routines, sleep recovery और decision delay rules इसे मजबूत बनाते हैं।",
    },
    "financial_discipline_index": {
        "label": "वित्तीय अनुशासन | Financial Discipline",
        "meaning": "यह संकेतक savings, debt, impulse control और risk attitude के संयुक्त pattern को पढ़ता है।",
        "risk": "Weak financial discipline अक्सर income problem नहीं बल्कि structure problem को show करता है।",
        "improvement": "Budget checkpoints, auto-saving और delayed spending protocol सबसे direct remedy हैं।",
    },
    "karma_pressure_index": {
        "label": "कर्म दबाव | Karma Pressure",
        "meaning": "यह score anxiety, setbacks और unresolved load के pressure signal को capture करता है।",
        "risk": "High karma pressure phases में छोटी समस्याएं भी disproportionately heavy महसूस हो सकती हैं।",
        "improvement": "Priority reduction, debt cleanup और recovery rituals इस pressure को soften करते हैं।",
    },
}

NUMBER_TRAITS: Dict[int, Dict[str, str]] = {
    1: {"gift": "initiative और leadership", "shadow": "ego-driven solo execution", "growth": "collaboration के साथ clear leadership"},
    2: {"gift": "sensitivity और partnership intelligence", "shadow": "indecision और emotional dependency", "growth": "boundaries के साथ supportive influence"},
    3: {"gift": "communication और creative expression", "shadow": "scatter और unfinished execution", "growth": "structured communication with disciplined follow-through"},
    4: {"gift": "structure, process और reliability", "shadow": "rigidity और slow adaptation", "growth": "system thinking के साथ flexible execution"},
    5: {"gift": "adaptability, learning और mobility", "shadow": "restlessness और inconsistency", "growth": "freedom के भीतर disciplined rhythm"},
    6: {"gift": "care, responsibility और relationship anchoring", "shadow": "over-responsibility और guilt load", "growth": "healthy care with boundaries"},
    7: {"gift": "analysis, insight और research depth", "shadow": "withdrawal और overthinking", "growth": "deep thinking को practical expression देना"},
    8: {"gift": "power, material strategy और governance", "shadow": "control stress और harsh pressure", "growth": "ethical authority with stable systems"},
    9: {"gift": "vision, compassion और larger purpose", "shadow": "energy leakage और emotional exhaustion", "growth": "purpose को grounded structure देना"},
}

PLANET_MAP: Dict[int, str] = {
    1: "सूर्य | Surya",
    2: "चंद्र | Chandra",
    3: "गुरु | Guru",
    4: "राहु | Rahu",
    5: "बुध | Budh",
    6: "शुक्र | Shukra",
    7: "केतु | Ketu",
    8: "शनि | Shani",
    9: "मंगल | Mangal",
    11: "चंद्र-गुरु मिश्र ऊर्जा | Moon-Jupiter Blend",
    22: "राहु-शनि संरचना | Rahu-Saturn Build Force",
}

LOSHU_MEANINGS: Dict[int, str] = {
    1: "स्वतंत्र निर्णय और personal will",
    2: "sensitivity, relationship awareness और diplomacy",
    3: "communication, creative expression और social ease",
    4: "discipline, order और practical systems",
    5: "adaptability, center balance और response flexibility",
    6: "family duty, commitment और responsibility",
    7: "introspection, research और inner truth seeking",
    8: "power handling, endurance और material governance",
    9: "vision, courage और larger humanitarian direction",
}

FOCUS_LABELS = {
    "finance_debt": "financial stability और debt control",
    "career_growth": "career growth और role positioning",
    "relationship": "relationship clarity और emotional balance",
    "health_stability": "health stability और energy rhythm",
    "emotional_confusion": "emotional clarity और inner steadiness",
    "business_decision": "business direction और strategic execution",
    "general_alignment": "overall life alignment",
}


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _clean_text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    text = " ".join(str(value).split())
    return text or default


def _first_name(identity: Dict[str, Any]) -> str:
    full_name = _clean_text(identity.get("full_name"), "उपयोगकर्ता")
    return full_name.split()[0] if full_name else "उपयोगकर्ता"


def _focus_label(focus_key: str) -> str:
    return FOCUS_LABELS.get(focus_key or "general_alignment", FOCUS_LABELS["general_alignment"])


def _life_numbers(numerology_core: Dict[str, Any]) -> Tuple[int, int, int, int]:
    pyth = numerology_core.get("pythagorean") or {}
    chaldean = numerology_core.get("chaldean") or {}
    return (
        _safe_int(pyth.get("life_path_number"), 0),
        _safe_int(pyth.get("destiny_number"), 0),
        _safe_int(pyth.get("expression_number"), 0),
        _safe_int(chaldean.get("name_number"), 0),
    )


def _metric_pairs(scores: Dict[str, Any]) -> List[Tuple[str, int]]:
    ordered = []
    for key in (
        "life_stability_index",
        "confidence_score",
        "dharma_alignment_score",
        "emotional_regulation_index",
        "financial_discipline_index",
        "karma_pressure_index",
    ):
        ordered.append((key, _safe_int(scores.get(key), 50)))
    return ordered


def _strongest_metric(scores: Dict[str, Any]) -> Tuple[str, int]:
    return max(_metric_pairs(scores), key=lambda item: item[1])


def _weakest_metric(scores: Dict[str, Any]) -> Tuple[str, int]:
    return min(_metric_pairs(scores), key=lambda item: item[1])


def _score_tone(score: int) -> str:
    if score >= 75:
        return "मजबूत"
    if score >= 55:
        return "मध्यम लेकिन workable"
    return "संवेदनशील"


def _dominant_planet(life_path: int, destiny: int, name_number: int) -> str:
    primary = life_path or destiny or name_number or 5
    return PLANET_MAP.get(primary, "बुध | Budh")


def _missing_numbers(numerology_core: Dict[str, Any]) -> List[int]:
    loshu = numerology_core.get("loshu_grid") or {}
    missing = loshu.get("missing_numbers") or []
    return sorted(_safe_int(number, 0) for number in missing if _safe_int(number, 0))


def _present_numbers(numerology_core: Dict[str, Any]) -> List[int]:
    loshu = numerology_core.get("loshu_grid") or {}
    grid = loshu.get("grid_counts") or {}
    present: List[int] = []
    for number in range(1, 10):
        if _safe_int(grid.get(str(number), grid.get(number)), 0) > 0:
            present.append(number)
    return present


def _zone_balance(numerology_core: Dict[str, Any]) -> Tuple[str, str]:
    loshu = numerology_core.get("loshu_grid") or {}
    grid = loshu.get("grid_counts") or {}
    zones = {
        "mental plane": sum(_safe_int(grid.get(str(number), 0), 0) for number in (4, 9, 2)),
        "emotional plane": sum(_safe_int(grid.get(str(number), 0), 0) for number in (3, 5, 7)),
        "practical plane": sum(_safe_int(grid.get(str(number), 0), 0) for number in (8, 1, 6)),
    }
    weakest = min(zones.items(), key=lambda item: item[1])[0]
    strongest = max(zones.items(), key=lambda item: item[1])[0]
    return strongest, weakest


def _metric_driver(metric_key: str, scores: Dict[str, Any], intake_context: Dict[str, Any]) -> str:
    financial = intake_context.get("financial") or {}
    emotional = intake_context.get("emotional") or {}
    career = intake_context.get("career") or {}
    life_events = intake_context.get("life_events") or {}

    if metric_key == "confidence_score":
        missing = []
        if financial.get("savings_ratio") is None:
            missing.append("savings ratio")
        if financial.get("debt_ratio") is None:
            missing.append("debt ratio")
        if career.get("stress_level") is None:
            missing.append("stress level")
        if emotional.get("anxiety_level") is None:
            missing.append("anxiety signal")
        if career.get("years_experience") is None:
            missing.append("experience depth")
        if missing:
            return "यह score नीचे है क्योंकि behavioral intake में " + ", ".join(missing[:4]) + " जैसे signals अधूरे हैं।"
        return "Confidence low नहीं है; इसका आधार decision clarity और input completeness दोनों हैं।"

    if metric_key == "financial_discipline_index":
        savings = financial.get("savings_ratio")
        debt = financial.get("debt_ratio")
        return (
            f"Savings ratio {savings if savings is not None else 'उपलब्ध नहीं'} और debt ratio {debt if debt is not None else 'उपलब्ध नहीं'} "
            "इस metric को सबसे अधिक influence कर रहे हैं।"
        )

    if metric_key == "emotional_regulation_index":
        anxiety = emotional.get("anxiety_level")
        stability = emotional.get("emotional_stability")
        return (
            f"Anxiety level {anxiety if anxiety is not None else 'उपलब्ध नहीं'} और emotional stability "
            f"{stability if stability is not None else 'उपलब्ध नहीं'} इस score की दिशा तय कर रहे हैं।"
        )

    if metric_key == "life_stability_index":
        setbacks = len(life_events.get("setback_events_years") or [])
        stress = career.get("stress_level")
        return (
            f"Stress level {stress if stress is not None else 'उपलब्ध नहीं'} और setback count {setbacks} "
            "जीवन स्थिरता की practical quality को shape कर रहे हैं।"
        )

    if metric_key == "dharma_alignment_score":
        years = career.get("years_experience")
        focus_key = (intake_context.get("focus") or {}).get("life_focus")
        return (
            f"Current focus {_focus_label(focus_key)} और experience depth {years if years is not None else 'उपलब्ध नहीं'} "
            "इस alignment score के प्रमुख drivers हैं।"
        )

    if metric_key == "karma_pressure_index":
        setbacks = len(life_events.get("setback_events_years") or [])
        anxiety = emotional.get("anxiety_level")
        return (
            f"Anxiety signal {anxiety if anxiety is not None else 'उपलब्ध नहीं'} और पिछले setbacks {setbacks} "
            "कर्म दबाव की intensity को influence कर रहे हैं।"
        )

    return "यह संकेतक उपलब्ध numerology और behavioral inputs के संयुक्त pattern से निकला है।"


def _metric_explanations(scores: Dict[str, Any], intake_context: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    explanations: Dict[str, Dict[str, Any]] = {}
    for key, score in _metric_pairs(scores):
        guide = METRIC_GUIDE[key]
        explanations[key] = {
            "label": guide["label"],
            "score": score,
            "status": _score_tone(score),
            "meaning": guide["meaning"],
            "driver": _metric_driver(key, scores, intake_context),
            "risk": guide["risk"],
            "improvement": guide["improvement"],
        }
    return explanations


def _deficit_model(
    scores: Dict[str, Any],
    numerology_core: Dict[str, Any],
    remedies: Dict[str, Any],
    intake_context: Dict[str, Any],
) -> Dict[str, str]:
    missing = _missing_numbers(numerology_core)
    weakest_metric_key, weakest_score = _weakest_metric(scores)
    weakest_metric = METRIC_GUIDE[weakest_metric_key]["label"]

    if 5 in missing:
        deficit = "केंद्र 5 की कमी | Missing center 5"
        symptom = "Decision instability, context switching और emotional anchoring की कमी एक साथ दिखाई दे सकती है।"
        patch = "हर बड़े निर्णय के लिए 24-hour pause rule, written priorities और same-time daily reset install करें।"
    elif missing:
        primary_missing = missing[0]
        deficit = f"लो शु कमी {primary_missing} | Missing {primary_missing}"
        symptom = (
            f"यह कमी {LOSHU_MEANINGS.get(primary_missing, 'core expression')} से जुड़े व्यवहार में gap दिखाती है, "
            "जिससे consistency या communication में friction बढ़ सकता है।"
        )
        patch = (
            f"ऐसी routine बनाएं जो {LOSHU_MEANINGS.get(primary_missing, 'इस ऊर्जा')} को daily action में convert करे। "
            "Small repeated practices यहां सबसे effective रहेंगी।"
        )
    else:
        deficit = f"स्कोर अंतर | Weakest metric: {weakest_metric}"
        symptom = METRIC_GUIDE[weakest_metric_key]["risk"]
        patch = METRIC_GUIDE[weakest_metric_key]["improvement"]

    focus_key = (intake_context.get("focus") or {}).get("life_focus")
    routine = ((remedies.get("daily_energy_alignment") or {}).get("focus_routine")) or "सुबह स्पष्ट intention लिखें।"
    rationale = (
        f"Current focus {_focus_label(focus_key)} है और weakest pressure point का score {weakest_score} है। "
        f"इसलिए engineered patch केवल advice नहीं बल्कि daily operating system होना चाहिए. Anchor line: {routine}"
    )

    return {
        "structural_deficit": deficit,
        "behavioral_symptom": symptom,
        "engineered_patch": patch,
        "rationale": rationale,
    }


def build_interpretation_report(
    intake_context: Dict[str, Any],
    numerology_core: Dict[str, Any],
    scores: Dict[str, Any],
    archetype: Dict[str, Any],
    remedies: Dict[str, Any],
) -> Dict[str, Any]:
    identity = intake_context.get("identity") or {}
    birth_details = intake_context.get("birth_details") or {}
    preferences = intake_context.get("preferences") or {}
    focus = intake_context.get("focus") or {}
    financial = intake_context.get("financial") or {}
    career = intake_context.get("career") or {}
    current_problem = _clean_text(intake_context.get("current_problem"), "overall life alignment")

    name = _clean_text(identity.get("full_name"), "उपयोगकर्ता")
    first_name = _first_name(identity)
    city = _clean_text(birth_details.get("birthplace_city"), "जन्म-स्थान उपलब्ध नहीं")
    language = _clean_text(preferences.get("language_preference"), "hindi")
    focus_key = _clean_text(focus.get("life_focus"), "general_alignment")
    focus_label = _focus_label(focus_key)

    life_path, destiny, expression, name_number = _life_numbers(numerology_core)
    dominant_planet = _dominant_planet(life_path, destiny, name_number)
    strongest_metric_key, strongest_metric_score = _strongest_metric(scores)
    weakest_metric_key, weakest_metric_score = _weakest_metric(scores)
    strongest_metric = METRIC_GUIDE[strongest_metric_key]["label"]
    weakest_metric = METRIC_GUIDE[weakest_metric_key]["label"]
    metric_explanations = _metric_explanations(scores, intake_context)

    archetype_name = _clean_text(archetype.get("archetype_name"), "Strategic Pattern")
    core_archetype = _clean_text(archetype.get("core_archetype"), "Adaptive Archetype")
    behavior_style = _clean_text(archetype.get("behavior_style"), "Adaptive Thinker")
    archetype_description = _clean_text(archetype.get("description"))

    traits = NUMBER_TRAITS.get(life_path or destiny or 5, NUMBER_TRAITS[5])
    missing_numbers = _missing_numbers(numerology_core)
    present_numbers = _present_numbers(numerology_core)
    strongest_zone, weakest_zone = _zone_balance(numerology_core)
    risk_band = _clean_text(scores.get("risk_band"), "Correctable")
    confidence = _safe_int(scores.get("confidence_score"), 50)
    mobile_analysis = numerology_core.get("mobile_analysis") or {}
    business_analysis = numerology_core.get("business_analysis") or {}
    compatibility = numerology_core.get("compatibility") or {}
    life_remedies = remedies.get("lifestyle_remedies") or {}
    mobile_remedies = remedies.get("mobile_remedies") or {}
    vedic = remedies.get("vedic_remedies") or {}
    daily = remedies.get("daily_energy_alignment") or {}

    savings = financial.get("savings_ratio")
    debt = financial.get("debt_ratio")
    stress_level = career.get("stress_level")
    years = career.get("years_experience")
    industry = _clean_text(career.get("industry"), _clean_text(preferences.get("profession"), "general professional domain"))

    primary_insight = {
        "core_archetype": archetype_name,
        "strength": (
            f"{strongest_metric} इस report का सबसे मजबूत संकेतक है। इसका अर्थ है कि {first_name} के पास "
            f"{METRIC_GUIDE[strongest_metric_key]['meaning'].replace('यह ', '').replace('यह score ', '')}"
        ),
        "critical_deficit": (
            f"सबसे बड़ा deficit {weakest_metric} में दिख रहा है। वर्तमान score {weakest_metric_score} इस बात का संकेत देता है कि "
            f"{METRIC_GUIDE[weakest_metric_key]['risk']}"
        ),
        "stability_risk": (
            f"Risk band {risk_band} है। इसका अर्थ यह है कि structure मौजूद है, लेकिन अगर {weakest_metric.lower()} पर काम नहीं किया गया "
            "तो growth pressure phases में instability जल्दी बढ़ सकती है।"
        ),
        "phase_1_diagnostic": (
            f"Phase 1 Diagnostic: {first_name} की current challenge '{current_problem}' है। Life Path {life_path}, Destiny {destiny} "
            f"और weakest signal {weakest_metric.lower()} यह दिखाते हैं कि समस्या केवल बाहरी नहीं बल्कि operating rhythm की भी है।"
        ),
        "phase_2_blueprint": (
            f"Phase 2 Structural Blueprint: Foundation number {life_path}, execution number {destiny}, expression {expression} "
            f"और public facade {name_number} को एक single strategic lane में align करना होगा ताकि {focus_label} compounding mode में जा सके।"
        ),
        "phase_3_intervention_protocol": (
            f"Phase 3 Intervention Protocol: सुबह के anchor, decision filters, mobile-energy hygiene और remedy discipline को 21-day protocol में चलाकर "
            f"{weakest_metric.lower()} को stabilize करना इस report की मुख्य recommendation है।"
        ),
        "narrative": (
            f"{name} की Strategic Life Audit यह दिखाती है कि core archetype '{archetype_name}' है, जिसका central theme {traits['gift']} है। "
            f"Life Path {life_path}, Destiny {destiny} और Name Number {name_number} मिलकर एक ऐसा pattern बना रहे हैं जिसमें potential मौजूद है, "
            f"लेकिन उसका compounding weakest metric {weakest_metric.lower()} के कारण रुक सकता है। Current focus {focus_label} है, "
            f"और confidence score {confidence} बताता है कि clarity का स्तर {'मध्यम' if confidence >= 50 else 'सीमित'} है। "
            f"इसलिए report का intent prediction देना नहीं बल्कि operating system redesign करना है, ताकि {first_name} reactive cycle से निकलकर deliberate growth mode में जा सके।"
        ),
    }

    numerology_architecture = {
        "foundation": {
            "label": "Foundation → Life Path",
            "value": life_path,
            "meaning": f"Life Path {life_path} आपकी natural journey, recurring lessons और default direction को govern करता है।",
        },
        "left_pillar": {
            "label": "Left Pillar → Destiny",
            "value": destiny,
            "meaning": f"Destiny {destiny} outer-world execution, achievement style और visible contribution की शैली को shape करता है।",
        },
        "right_pillar": {
            "label": "Right Pillar → Expression",
            "value": expression,
            "meaning": f"Expression {expression} communication tone, talent expression और public articulation की ताकत दिखाता है।",
        },
        "facade": {
            "label": "Facade → Name Number",
            "value": name_number,
            "meaning": f"Name Number {name_number} social vibration, first impression और public trust architecture को influence करता है।",
        },
        "interaction_summary": (
            f"जब Foundation {life_path} movement create करता है, Left Pillar {destiny} उसे execution में बदलता है, Right Pillar {expression} "
            f"उसकी communication quality तय करता है और Facade {name_number} दुनिया तक उसकी branding पहुंचाता है। "
            f"{first_name} के case में यह architecture research, structured movement और identity signal को combine करता है, इसलिए random multitasking के बजाय "
            "clear lanes बनाना ज्यादा powerful रहेगा।"
        ),
    }

    leadership_traits = [
        f"{traits['gift']} इस profile की natural leadership strength है।",
        f"Behavior Style '{behavior_style}' यह दिखाता है कि {first_name} uncertainty के बीच pattern पढ़ सकता है।",
        f"{industry} जैसे domain में यह profile ownership, analysis और credibility-driven roles में अधिक चमक सकती है।",
    ]
    if business_analysis.get("compatible_industries"):
        leadership_traits.append(
            "Business vibration विशेष रूप से इन sectors को support करती है: "
            + ", ".join(str(item) for item in business_analysis.get("compatible_industries", [])[:3])
            + "."
        )

    archetype_intelligence = {
        "signature": (
            f"{core_archetype} signature का मतलब यह है कि {first_name} का mind surface-level patterns से जल्दी संतुष्ट नहीं होता। "
            f"यह profile {archetype_description or traits['gift']} को practical strategy में बदलने की क्षमता रखती है।"
        ),
        "leadership_traits": leadership_traits,
        "shadow_traits": (
            f"इस archetype का shadow side {traits['shadow']} है। Weakest metric {weakest_metric.lower()} होने के कारण "
            f"यह shadow pressure phases में और visible हो सकता है, खासकर जब stress level {stress_level if stress_level is not None else 'उपलब्ध नहीं'} हो।"
        ),
        "growth_path": (
            f"Growth path यह है कि {traits['growth']}। इसका practical मतलब है कि freedom और depth दोनों को repeatable systems के भीतर operate करना होगा।"
        ),
    }

    missing_meanings = [
        f"Missing {number}: {LOSHU_MEANINGS[number]} वाले क्षेत्र पर conscious training की जरूरत है।"
        for number in missing_numbers
        if number in LOSHU_MEANINGS
    ]
    center_presence = 5 in present_numbers
    loshu_diagnostic = {
        "present_numbers": present_numbers,
        "missing_numbers": missing_numbers,
        "center_presence": center_presence,
        "energy_imbalance": f"Strongest zone {strongest_zone} है, जबकि weakest zone {weakest_zone} दिख रहा है।",
        "missing_number_meanings": missing_meanings,
        "narrative": (
            f"Lo Shu grid {first_name} के behavioral architecture का silent map है। Present numbers {', '.join(map(str, present_numbers)) or 'none'} "
            f"उन energies को दिखाते हैं जो naturally accessible हैं, जबकि missing numbers {', '.join(map(str, missing_numbers)) or 'none'} "
            "बताते हैं कि किन qualities को consciously build करना होगा। "
            f"Center 5 {'present' if center_presence else 'missing'} होने के कारण adaptability और internal balance "
            f"{'accessible' if center_presence else 'एक major training theme'} बनते हैं। यह grid विशेष रूप से {focus_label} के context में महत्वपूर्ण है।"
        ),
    }

    calibration_cluster = []
    calibration = intake_context.get("calibration") or {}
    for key in ("stress_response", "money_decision_style", "biggest_weakness", "decision_style"):
        value = _clean_text(calibration.get(key))
        if value:
            calibration_cluster.append(value.replace("_", " "))
    if not calibration_cluster:
        calibration_cluster = ["structured clarity", "measured response", "deliberate execution"]

    planetary_mapping = {
        "background_forces": (
            f"Life Path {life_path}, Destiny {destiny} और Name Number {name_number} मिलकर {dominant_planet} की background force को amplify कर रहे हैं। "
            "यह force बताती है कि learning, discipline, speed या introspection में से कौन-सी energy report में सबसे central है।"
        ),
        "primary_intervention_planet": dominant_planet,
        "calibration_cluster": ", ".join(calibration_cluster[:3]),
        "narrative": (
            f"Planetary mapping को यहां prediction की तरह नहीं बल्कि calibration map की तरह पढ़ा जाना चाहिए। {dominant_planet} इस समय primary intervention planet है, "
            f"क्योंकि current deficit {weakest_metric.lower()} के around दिखाई दे रहा है। इसका अर्थ यह है कि remedies, routines और behavioral rules "
            f"उसी energy को stabilize करें जो {first_name} के numbers में सबसे loud या सबसे stressed रूप में उभर रही है।"
        ),
    }

    deficit_model = _deficit_model(scores, numerology_core, remedies, intake_context)

    circadian_alignment = {
        "morning_routine": _clean_text(
            daily.get("morning"),
            "सुबह 10-15 मिनट sunlight, breath reset और दिन का एक primary intention लिखें।",
        ),
        "work_alignment": _clean_text(
            daily.get("focus_routine"),
            f"पहले work block से पहले {focus_label} से जुड़ा एक measurable outcome define करें।",
        ),
        "evening_shutdown": _clean_text(
            daily.get("evening_reset"),
            "रात में screen slowdown, spending stop-line और short reflection note के साथ दिन बंद करें।",
        ),
        "narrative": (
            f"{first_name} की report यह साफ दिखाती है कि circadian rhythm केवल health tool नहीं बल्कि decision quality tool है। "
            f"जब morning anchor clear होता है, तब {weakest_metric.lower()} का noise कम होता है। "
            f"इसीलिए इस report का समय-संबंधी protocol सीधे productivity नहीं बल्कि judgment stability को target करता है।"
        ),
    }

    supportive_energies = mobile_analysis.get("supportive_number_energies") or []
    environment_alignment = {
        "physical_space": (
            f"Workspace को clean zones में divide करें: deep work, admin work और recovery. {city} जैसी high-noise environment contexts में visual clutter कम रखना खास जरूरी है।"
        ),
        "color_alignment": _clean_text(
            life_remedies.get("color_alignment"),
            "Color environment को overstimulating नहीं बल्कि grounding बनाएं।",
        ),
        "mobile_number_analysis": (
            _clean_text(mobile_analysis.get("compatibility_summary"))
            + (" " if mobile_analysis.get("compatibility_summary") else "")
            + _clean_text(
                mobile_analysis.get("correction_suggestion"),
                f"Supportive ending energies: {', '.join(map(str, supportive_energies[:3])) or '1, 3, 5'}",
            )
        ).strip(),
        "digital_behavior": " ".join(
            part
            for part in [
                _clean_text(mobile_remedies.get("mobile_usage_timing")),
                _clean_text(mobile_remedies.get("whatsapp_dp")),
                _clean_text(mobile_remedies.get("charging_direction")),
            ]
            if part
        ),
        "narrative": (
            f"Environment alignment का मतलब केवल color suggestion नहीं बल्कि external friction कम करना है। "
            f"अगर mobile vibration {mobile_analysis.get('mobile_vibration', 'N/A')} है और supportive energies {', '.join(map(str, supportive_energies[:3])) or '1, 3, 5'} हैं, "
            "तो digital behavior, notification load और device symbolism भी day-to-day response quality को influence करेंगे।"
        ),
    }

    vedic_protocol = {
        "focus": f"Primary focus: {weakest_metric}",
        "code": _clean_text(vedic.get("mantra_sanskrit"), "ॐ बुधाय नमः"),
        "parameter": _clean_text(vedic.get("practice_guideline"), "21 दिनों तक रोज 108 बार जप करें।"),
        "output": _clean_text(vedic.get("recommended_donation"), "हरित दान या grounded सेवा करें।"),
        "purpose": _clean_text(
            vedic.get("purpose"),
            f"इस remedy का उद्देश्य {weakest_metric.lower()} को stabilize करना और {dominant_planet} की energy को disciplined direction देना है।",
        ),
        "planetary_alignment": _clean_text(
            vedic.get("planetary_alignment"),
            f"{dominant_planet} इस समय intervention planet के रूप में काम कर रहा है।",
        ),
        "pronunciation": _clean_text(vedic.get("mantra_pronunciation")),
    }

    execution_plan = {
        "install_rhythm": "दिन 1-7: Morning anchor, spending visibility, sleep boundary और one-page daily intention को install करें।",
        "deploy_anchor": "दिन 8-14: Weakest metric के लिए एक measurable control जोड़ें, जैसे debt check, recovery block या decision rule.",
        "run_protocol": "दिन 15-21: Remedy discipline, work-lane clarity और review cadence को बिना break maintain करें ताकि नया pattern body level पर settle हो।",
        "checkpoints": [
            "सप्ताह 1 checkpoint: confidence score driver inputs पूरे करें।",
            f"सप्ताह 2 checkpoint: {weakest_metric.lower()} को track करने वाला एक visible metric रखें।",
            "सप्ताह 3 checkpoint: जो routine काम कर रहा है उसे अगले 60 दिनों की plan sheet में lock करें।",
        ],
        "summary": (
            f"21-day plan का उद्देश्य transformation का illusion देना नहीं बल्कि operating discipline की शुरुआत करना है। "
            f"यदि {first_name} इस protocol को consistency से follow करता है, तो {focus_label} से जुड़ा वर्तमान pressure measurable clarity में बदल सकता है।"
        ),
    }

    compatible_numbers = compatibility.get("compatible_numbers")
    challenging_numbers = compatibility.get("challenging_numbers")
    if compatible_numbers is None:
        compatible_numbers = mobile_analysis.get("supportive_number_energies") or [life_path or 1, name_number or 3]
    if challenging_numbers is None:
        challenging_numbers = missing_numbers[:2]

    executive_brief = {
        "summary": primary_insight["narrative"],
        "key_strength": primary_insight["strength"],
        "key_risk": primary_insight["critical_deficit"],
        "strategic_focus": primary_insight["phase_3_intervention_protocol"],
    }

    analysis_sections = {
        "career_analysis": (
            f"{industry} domain में {first_name} को ऐसे roles ज़्यादा suit करते हैं जहां ownership, depth और credibility visible हो। "
            f"Years of experience {years if years is not None else 'उपलब्ध नहीं'} होने के बावजूद growth तभी compound करेगी जब {weakest_metric.lower()} पर control बढ़ेगा।"
        ),
        "decision_profile": (
            f"Decision profile अभी {confidence}/100 confidence और {risk_band} risk band पर खड़ा है। "
            "इसका अर्थ है कि choices में क्षमता मौजूद है, लेकिन better filters, written decision rules और noise reduction की जरूरत है।"
        ),
        "emotional_analysis": (
            f"Emotional regulation score {_safe_int(scores.get('emotional_regulation_index'), 50)} है। "
            "इसका behavioral अर्थ है कि recovery system को luxury नहीं बल्कि strategy समझना होगा।"
        ),
        "financial_analysis": (
            f"Financial discipline score {_safe_int(scores.get('financial_discipline_index'), 50)} है। "
            f"Savings {savings if savings is not None else 'उपलब्ध नहीं'} और debt {debt if debt is not None else 'उपलब्ध नहीं'} के आधार पर यह स्पष्ट है कि money structure growth engine बनेगा या pressure engine, यह routine तय करेगी।"
        ),
    }

    strategic_guidance = {
        "short_term": primary_insight["phase_1_diagnostic"],
        "mid_term": primary_insight["phase_2_blueprint"],
        "long_term": primary_insight["phase_3_intervention_protocol"],
    }

    growth_blueprint = {
        "phase_1": execution_plan["install_rhythm"],
        "phase_2": execution_plan["deploy_anchor"],
        "phase_3": execution_plan["run_protocol"],
    }

    business_block = {
        "business_strength": _clean_text(
            business_analysis.get("business_strength"),
            f"{first_name} की profile strategy, clarity और trust-based positioning को support करती है।",
        ),
        "risk_factor": _clean_text(
            business_analysis.get("risk_factor"),
            f"Main business risk यह है कि {weakest_metric.lower()} growth opportunities को fragmented execution में बदल सकता है।",
        ),
        "compatible_industries": business_analysis.get("compatible_industries") or [industry],
    }

    compatibility_block = {
        "compatible_numbers": compatible_numbers,
        "challenging_numbers": challenging_numbers,
        "relationship_guidance": (
            f"ऐसे लोग या environments {first_name} को ज्यादा support करेंगे जो {strongest_metric.lower()} को reinforce करें और "
            f"{weakest_metric.lower()} पर unnecessary pressure न बढ़ाएं।"
        ),
    }

    return {
        "primary_insight": primary_insight,
        "metric_explanations": metric_explanations,
        "numerology_architecture": numerology_architecture,
        "archetype_intelligence": archetype_intelligence,
        "loshu_diagnostic": loshu_diagnostic,
        "planetary_mapping": planetary_mapping,
        "structural_deficit_model": deficit_model,
        "circadian_alignment": circadian_alignment,
        "environment_alignment": environment_alignment,
        "vedic_remedy_protocol": vedic_protocol,
        "execution_plan": execution_plan,
        "executive_brief": executive_brief,
        "analysis_sections": analysis_sections,
        "strategic_guidance": strategic_guidance,
        "growth_blueprint": growth_blueprint,
        "business_block": business_block,
        "compatibility_block": compatibility_block,
        "meta_notes": {
            "language_preference": language,
            "dominant_planet": dominant_planet,
            "focus_label": focus_label,
            "strongest_metric": strongest_metric,
            "strongest_metric_score": strongest_metric_score,
            "weakest_metric": weakest_metric,
            "weakest_metric_score": weakest_metric_score,
        },
    }
