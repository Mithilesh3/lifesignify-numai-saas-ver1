"""
LIFE SIGNIFY NUMAI
Weighted Intelligence Scoring Engine
Enterprise / Investor Grade
"""

from typing import Dict, Any, List


# ==========================================================
# CORE UTILITIES
# ==========================================================

def normalize(value, min_val, max_val):
    if value is None:
        return 0.5  # neutral fallback

    value = max(min_val, min(value, max_val))
    return (value - min_val) / (max_val - min_val)


def _present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    return True


def _normalized_or_none(value, min_val, max_val, invert: bool = False):
    if value is None:
        return None
    normalized = normalize(value, min_val, max_val)
    return (1 - normalized) if invert else normalized



def weighted_score(components: List[Dict[str, float]]) -> int:
    """
    components example:
    [
        {"value": 0.7, "weight": 0.4},
        {"value": 0.5, "weight": 0.6},
    ]
    """
    valid = [c for c in components if c["value"] is not None]
    if not valid:
        return 50  # neutral fallback

    total_weight = sum(c["weight"] for c in valid)
    score = sum(c["value"] * c["weight"] for c in valid)

    return int((score / total_weight) * 100)


# ==========================================================
# LIFE STABILITY INDEX
# ==========================================================

def life_stability_index(data: Dict[str, Any]) -> int:

    emotional = normalize(data.get("emotional_stability"), 1, 10)
    debt = 1 - normalize(data.get("debt_ratio"), 0, 100)
    stress = 1 - normalize(data.get("stress_level"), 1, 10)
    savings = normalize(data.get("savings_ratio"), 0, 100)
    setbacks = 1 - normalize(data.get("major_setbacks"), 0, 5)

    return weighted_score([
        {"value": emotional, "weight": 0.30},
        {"value": debt, "weight": 0.25},
        {"value": stress, "weight": 0.20},
        {"value": savings, "weight": 0.15},
        {"value": setbacks, "weight": 0.10},
    ])


# ==========================================================
# EMOTIONAL REGULATION INDEX
# ==========================================================

def emotional_regulation_index(data: Dict[str, Any]) -> int:

    anxiety = 1 - normalize(data.get("anxiety"), 1, 10)
    impulse = normalize(data.get("impulse_control"), 1, 10)
    confusion = 1 - normalize(data.get("decision_confusion"), 1, 10)
    stability = normalize(data.get("emotional_stability"), 1, 10)

    return weighted_score([
        {"value": anxiety, "weight": 0.30},
        {"value": impulse, "weight": 0.25},
        {"value": confusion, "weight": 0.20},
        {"value": stability, "weight": 0.25},
    ])


# ==========================================================
# FINANCIAL DISCIPLINE INDEX
# ==========================================================

def financial_discipline_index(data: Dict[str, Any]) -> int:

    savings = normalize(data.get("savings_ratio"), 0, 100)
    debt = 1 - normalize(data.get("debt_ratio"), 0, 100)
    impulse = 1 - normalize(data.get("impulse_spending"), 1, 10)

    risk_map = {
        "low": 0.8,
        "moderate": 0.6,
        "high": 0.3,
    }

    raw_risk_tolerance = data.get("risk_tolerance")
    risk_key = str(raw_risk_tolerance).strip().lower() if raw_risk_tolerance is not None else ""
    risk = risk_map.get(risk_key, 0.5)

    return weighted_score([
        {"value": savings, "weight": 0.30},
        {"value": debt, "weight": 0.25},
        {"value": risk, "weight": 0.20},
        {"value": impulse, "weight": 0.25},
    ])


# ==========================================================
# DHARMA ALIGNMENT SCORE
# ==========================================================

def dharma_alignment_score(data: Dict[str, Any], emotional_score: int) -> int:

    stress = 1 - normalize(data.get("stress_level"), 1, 10)
    experience = normalize(data.get("years_experience"), 0, 30)
    clarity = normalize(data.get("decision_clarity"), 1, 10)

    focus_bonus = 0.7 if data.get("life_focus") else 0.4
    emotional = emotional_score / 100

    return weighted_score([
        {"value": stress, "weight": 0.25},
        {"value": experience, "weight": 0.20},
        {"value": clarity, "weight": 0.20},
        {"value": focus_bonus, "weight": 0.20},
        {"value": emotional, "weight": 0.15},
    ])


# ==========================================================
# KARMA PRESSURE INDEX
# ==========================================================

def karma_pressure_index(data: Dict[str, Any]) -> int:

    anxiety = normalize(data.get("anxiety"), 1, 10)
    debt = normalize(data.get("debt_ratio"), 0, 100)
    setbacks = normalize(data.get("major_setbacks"), 0, 5)

    return weighted_score([
        {"value": anxiety, "weight": 0.35},
        {"value": debt, "weight": 0.30},
        {"value": setbacks, "weight": 0.20},
        {"value": 0.6, "weight": 0.15},  # baseline pressure factor
    ])


# ==========================================================
# DATA COMPLETENESS SCORE
# ==========================================================

def compute_data_completeness_score(data: Dict[str, Any], plan_name: str = "basic") -> int:

    plan = (plan_name or "basic").strip().lower()

    basic_fields = [
        "life_focus",
        "major_setbacks",
        "decision_style",
        "stress_response",
        "money_decision_style",
        "biggest_weakness",
        "life_preference",
    ]
    pro_fields = basic_fields + [
        "savings_ratio",
        "debt_ratio",
        "stress_level",
        "decision_clarity",
        "years_experience",
        "anxiety",
        "impulse_control",
        "emotional_stability",
    ]
    enterprise_fields = pro_fields + [
        "monthly_income",
        "industry",
        "role",
        "decision_confusion",
        "impulse_spending",
    ]

    required_fields = {
        "basic": basic_fields,
        "pro": pro_fields,
        "premium": pro_fields,
        "enterprise": enterprise_fields,
    }.get(plan, basic_fields)

    filled = sum(1 for field in required_fields if _present(data.get(field)))
    ratio = filled / len(required_fields)
    score = int(ratio * 100)

    # Basic plans intentionally collect lighter intake, so keep a realistic floor.
    if plan == "basic" and score < 35:
        return 35

    return score


# ==========================================================
# DECISION CLARITY SCORE
# ==========================================================

def compute_decision_clarity_score(
    data: Dict[str, Any],
    data_completeness_score: int,
    plan_name: str = "basic",
) -> int:
    plan = (plan_name or "basic").strip().lower()

    direct_clarity = data.get("decision_clarity")
    components = [
        {"value": _normalized_or_none(direct_clarity, 1, 10), "weight": 0.40},
        {"value": _normalized_or_none(data.get("decision_confusion"), 1, 10, invert=True), "weight": 0.25},
        {"value": _normalized_or_none(data.get("stress_level"), 1, 10, invert=True), "weight": 0.15},
        {"value": _normalized_or_none(data.get("impulse_control"), 1, 10), "weight": 0.10},
        {"value": _normalized_or_none(data.get("emotional_stability"), 1, 10), "weight": 0.10},
    ]

    has_signal = any(c["value"] is not None for c in components)
    if not has_signal:
        return 45 if plan == "basic" else 40

    score = weighted_score(components)

    # If behavioral intake is sparse, prevent unrealistic collapse to zero.
    if data_completeness_score < 30:
        score = max(score, 42 if plan == "basic" else 38)

    return score


# ==========================================================
# RISK BAND MAPPING
# ==========================================================

def risk_band(score: int) -> str:
    if score >= 70:
        return "Stable"
    elif score >= 45:
        return "Correctable"
    return "Critical"


# ==========================================================
# MASTER SCORING FUNCTION
# ==========================================================

def generate_score_summary(data: Dict[str, Any], plan_name: str = "basic") -> Dict[str, Any]:

    emotional = emotional_regulation_index(data)
    financial = financial_discipline_index(data)
    stability = life_stability_index(data)
    dharma = dharma_alignment_score(data, emotional)
    karma = karma_pressure_index(data)
    completeness = compute_data_completeness_score(data, plan_name=plan_name)
    decision_clarity = compute_decision_clarity_score(
        data,
        data_completeness_score=completeness,
        plan_name=plan_name,
    )

    return {
        "life_stability_index": stability,
        "emotional_regulation_index": emotional,
        "financial_discipline_index": financial,
        "dharma_alignment_score": dharma,
        "karma_pressure_index": karma,
        # Backward-compatible field used across renderer/UI as Decision Clarity.
        "confidence_score": decision_clarity,
        # Explicit completeness signal for intake-quality warnings.
        "data_completeness_score": completeness,
        "risk_band": risk_band(stability),
    }


