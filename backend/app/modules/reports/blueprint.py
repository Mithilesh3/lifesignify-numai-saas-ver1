from typing import Dict, List


SECTION_TITLES: Dict[str, str] = {
    "cover": "Cover",
    "primary_insight": "Primary Insight",
    "intelligence_metrics": "Intelligence Metrics",
    "numerology_architecture": "Numerology Architecture",
    "archetype_intelligence": "Archetype Intelligence",
    "loshu_diagnostic": "Lo Shu Diagnostic",
    "planetary_mapping": "Planetary Mapping",
    "structural_deficit_model": "Structural Deficit Model",
    "circadian_alignment": "Circadian Alignment",
    "environment_alignment": "Environment Alignment",
    "vedic_remedy_protocol": "Vedic Remedy Protocol",
    "execution_plan": "21-Day Execution Plan",
}


BASE_SECTION_KEYS: List[str] = [
    "cover",
    "primary_insight",
    "intelligence_metrics",
    "numerology_architecture",
    "archetype_intelligence",
    "loshu_diagnostic",
    "planetary_mapping",
    "structural_deficit_model",
    "circadian_alignment",
    "environment_alignment",
    "vedic_remedy_protocol",
    "execution_plan",
]


TIER_SECTION_KEYS: Dict[str, List[str]] = {
    "basic": BASE_SECTION_KEYS,
    "pro": BASE_SECTION_KEYS,
    "premium": BASE_SECTION_KEYS,
    "enterprise": BASE_SECTION_KEYS,
}


def get_tier_section_blueprint(plan_name: str) -> Dict[str, object]:
    tier = (plan_name or "basic").strip().lower()
    section_keys = TIER_SECTION_KEYS.get(tier, TIER_SECTION_KEYS["basic"])

    return {
        "plan_tier": tier,
        "section_count": len(section_keys),
        "sections": [
            {
                "order": index,
                "key": key,
                "title": SECTION_TITLES[key],
            }
            for index, key in enumerate(section_keys, start=1)
        ],
    }


def get_all_tier_section_blueprints() -> Dict[str, Dict[str, object]]:
    return {
        tier: get_tier_section_blueprint(tier)
        for tier in ("basic", "pro", "premium", "enterprise")
    }
