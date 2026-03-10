from typing import Dict, List

SECTION_TITLES: Dict[str, str] = {
    "executive_summary": "Executive Strategic Intelligence Summary",
    "core_numerology_numbers": "Core Numerology Numbers",
    "name_number_analysis": "Name Number Analysis",
    "birth_date_numerology": "Birth Date Numerology",
    "loshu_grid_intelligence": "Lo Shu Grid Intelligence",
    "karmic_pattern_intelligence": "Karmic Pattern Intelligence",
    "hidden_talent_intelligence": "Hidden Talent Intelligence",
    "personal_year_forecast": "Personal Year Forecast",
    "lucky_numbers_favorable_dates": "Lucky Numbers & Favorable Dates",
    "basic_remedies": "Basic Remedy Protocol",
    "lifestyle_alignment": "Lifestyle Alignment",
    "closing_synthesis": "Closing Strategic Synthesis",
    "intelligence_metrics": "Numerology Intelligence Metrics",
    "archetype_intelligence": "Archetype Intelligence",
    "career_intelligence": "Career Intelligence",
    "financial_intelligence": "Financial Intelligence",
    "numerology_architecture": "Numerology Architecture Blueprint",
    "planetary_influence": "Planetary Influence Intelligence",
    "compatibility_intelligence": "Compatibility Intelligence",
    "life_cycle_timeline": "Life Cycle Timeline",
    "pinnacle_challenge_cycle_intelligence": "Pinnacle & Challenge Cycle Intelligence",
    "strategic_guidance": "Strategic Guidance",
    "name_vibration_optimization": "Name Vibration Optimization",
    "mobile_number_intelligence": "Mobile Number Intelligence",
    "email_identity_intelligence": "Email Identity Intelligence",
    "digital_discipline": "Digital Discipline",
    "vedic_remedy": "Vedic Remedy Intelligence",
    "correction_protocol_summary": "Correction Protocol Summary",
    "leadership_intelligence": "Leadership Intelligence",
    "business_intelligence": "Business Intelligence",
    "wealth_energy_blueprint": "Wealth Energy Blueprint",
    "decision_intelligence": "Decision Intelligence",
    "emotional_intelligence": "Emotional Intelligence",
    "strategic_timing_intelligence": "Strategic Timing Intelligence",
    "growth_blueprint": "Growth Blueprint",
    "signature_intelligence": "Signature Intelligence",
    "business_name_intelligence": "Business Name Intelligence",
    "brand_handle_optimization": "Brand Handle Optimization",
    "residence_energy_intelligence": "Residence Energy Intelligence",
    "vehicle_number_intelligence": "Vehicle Number Intelligence",
    "strategic_execution_roadmap": "Strategic Execution Roadmap",
}

BASIC_SECTION_KEYS: List[str] = [
    "executive_summary",
    "core_numerology_numbers",
    "name_number_analysis",
    "birth_date_numerology",
    "loshu_grid_intelligence",
    "karmic_pattern_intelligence",
    "hidden_talent_intelligence",
    "personal_year_forecast",
    "lucky_numbers_favorable_dates",
    "basic_remedies",
    "lifestyle_alignment",
    "closing_synthesis",
]

PREMIUM_SECTION_KEYS: List[str] = [
    "executive_summary",
    "intelligence_metrics",
    "archetype_intelligence",
    "career_intelligence",
    "financial_intelligence",
    "numerology_architecture",
    "loshu_grid_intelligence",
    "planetary_influence",
    "compatibility_intelligence",
    "life_cycle_timeline",
    "pinnacle_challenge_cycle_intelligence",
    "personal_year_forecast",
    "strategic_guidance",
    "name_vibration_optimization",
    "mobile_number_intelligence",
    "email_identity_intelligence",
    "lifestyle_alignment",
    "digital_discipline",
    "vedic_remedy",
    "correction_protocol_summary",
    "closing_synthesis",
]

ENTERPRISE_SECTION_KEYS: List[str] = [
    "executive_summary",
    "intelligence_metrics",
    "archetype_intelligence",
    "leadership_intelligence",
    "career_intelligence",
    "business_intelligence",
    "wealth_energy_blueprint",
    "decision_intelligence",
    "emotional_intelligence",
    "numerology_architecture",
    "planetary_influence",
    "loshu_grid_intelligence",
    "karmic_pattern_intelligence",
    "hidden_talent_intelligence",
    "life_cycle_timeline",
    "pinnacle_challenge_cycle_intelligence",
    "strategic_timing_intelligence",
    "compatibility_intelligence",
    "personal_year_forecast",
    "strategic_guidance",
    "growth_blueprint",
    "name_vibration_optimization",
    "mobile_number_intelligence",
    "email_identity_intelligence",
    "signature_intelligence",
    "business_name_intelligence",
    "brand_handle_optimization",
    "residence_energy_intelligence",
    "vehicle_number_intelligence",
    "lifestyle_alignment",
    "digital_discipline",
    "vedic_remedy",
    "correction_protocol_summary",
    "strategic_execution_roadmap",
    "closing_synthesis",
]

TIER_SECTION_KEYS: Dict[str, List[str]] = {
    "basic": BASIC_SECTION_KEYS,
    "pro": PREMIUM_SECTION_KEYS,
    "premium": PREMIUM_SECTION_KEYS,
    "enterprise": ENTERPRISE_SECTION_KEYS,
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
