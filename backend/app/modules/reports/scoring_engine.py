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
# CONFIDENCE SCORE (DATA COMPLETENESS)
# ==========================================================

def compute_confidence_score(data: Dict[str, Any]) -> int:

    required_fields = [
        "anxiety",
        "debt_ratio",
        "savings_ratio",
        "stress_level",
        "decision_clarity",
        "years_experience",
    ]

    filled = sum(1 for field in required_fields if data.get(field) is not None)

    return int((filled / len(required_fields)) * 100)


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

def generate_score_summary(data: Dict[str, Any]) -> Dict[str, Any]:

    emotional = emotional_regulation_index(data)
    financial = financial_discipline_index(data)
    stability = life_stability_index(data)
    dharma = dharma_alignment_score(data, emotional)
    karma = karma_pressure_index(data)
    confidence = compute_confidence_score(data)

    return {
        "life_stability_index": stability,
        "emotional_regulation_index": emotional,
        "financial_discipline_index": financial,
        "dharma_alignment_score": dharma,
        "karma_pressure_index": karma,
        "confidence_score": confidence,
        "risk_band": risk_band(stability),
    }


