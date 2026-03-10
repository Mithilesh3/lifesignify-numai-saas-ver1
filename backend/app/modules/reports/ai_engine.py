from typing import Dict, Any
from datetime import datetime
import traceback

from app.modules.reports.scoring_engine import generate_score_summary
from app.modules.reports.llm_engine import generate_ai_narrative
from app.modules.numerology.core_engine import generate_numerology_profile

from app.modules.reports.remedy_engine import generate_remedy_protocol
from app.modules.reports.archetype_engine import generate_numerology_archetype

from app.modules.numerology.business_engine import analyze_business_name

from app.core.config import settings


# =====================================================
# PLAN CONFIGURATION
# =====================================================

PLAN_FEATURES = {
    "basic": {"token_multiplier": 0.7},
    "pro": {"token_multiplier": 0.9},
    "premium": {"token_multiplier": 1.1},
    "enterprise": {"token_multiplier": 1.3},
}

FOCUS_LABELS = {
    "finance_debt": "financial pressure and debt management",
    "career_growth": "career growth and positioning",
    "relationship": "relationship patterns and compatibility",
    "health_stability": "health stability and sustainable routines",
    "emotional_confusion": "emotional clarity and inner stability",
    "business_decision": "business direction and strategic decisions",
    "general_alignment": "overall life alignment",
}

FOCUS_ACTIONS = {
    "finance_debt": "stabilize cash flow, tighten debt discipline, and build a repeatable savings habit",
    "career_growth": "choose roles and projects that compound credibility instead of scattering energy",
    "relationship": "bring more clarity, boundaries, and communication into close relationships",
    "health_stability": "protect energy through sleep, routine, and lower-stress decision cycles",
    "emotional_confusion": "reduce internal noise before making major choices and build steadier routines",
    "business_decision": "prioritize disciplined execution over reactive expansion",
    "general_alignment": "simplify priorities and align daily action with long-term direction",
}

METRIC_LABELS = {
    "life_stability_index": "Life Stability",
    "financial_discipline_index": "Financial Discipline",
    "emotional_regulation_index": "Emotional Regulation",
    "dharma_alignment_score": "Dharma Alignment",
    "confidence_score": "Decision Confidence",
}

METRIC_STRENGTHS = {
    "life_stability_index": "a reliable ability to create structure when priorities are clear",
    "financial_discipline_index": "an instinct for measured decisions around money and risk",
    "emotional_regulation_index": "the capacity to stay composed and recover after pressure",
    "dharma_alignment_score": "strong alignment between effort, timing, and purpose",
    "confidence_score": "enough self-awareness to make grounded decisions with momentum",
}

METRIC_RISKS = {
    "life_stability_index": "inconsistency in routines can weaken execution at important moments",
    "financial_discipline_index": "money decisions can drift without stronger budgeting structure",
    "emotional_regulation_index": "stress can distort judgment if recovery habits are not protected",
    "dharma_alignment_score": "energy may be spent on paths that do not compound into long-term progress",
    "confidence_score": "unclear inputs are reducing precision, so major decisions need more validation",
}


# =====================================================
# INTERNAL HELPERS
# =====================================================


def _clean_mapping(values: Dict[str, Any]) -> Dict[str, Any]:
    return {
        key: value
        for key, value in (values or {}).items()
        if value not in (None, "", [], {})
    }


def _prepare_identity(identity: Dict[str, Any], birth_details: Dict[str, Any]) -> Dict[str, Any]:
    prepared = _clean_mapping(identity)
    date_of_birth = (birth_details or {}).get("date_of_birth")
    if date_of_birth and not prepared.get("date_of_birth"):
        prepared["date_of_birth"] = date_of_birth
    return prepared


def _build_intake_context(request_data: Dict[str, Any]) -> Dict[str, Any]:
    request_data = request_data or {}
    birth_details = request_data.get("birth_details") or {}
    contact = request_data.get("contact") or {}
    preferences = request_data.get("preferences") or {}
    identity = _prepare_identity(request_data.get("identity") or {}, birth_details)

    mobile_number = contact.get("mobile_number")
    if mobile_number and not identity.get("mobile_number"):
        identity["mobile_number"] = mobile_number

    return {
        "identity": identity,
        "birth_details": _clean_mapping(birth_details),
        "focus": _clean_mapping(request_data.get("focus") or {}),
        "financial": _clean_mapping(request_data.get("financial") or {}),
        "career": _clean_mapping(request_data.get("career") or {}),
        "emotional": _clean_mapping(request_data.get("emotional") or {}),
        "life_events": _clean_mapping(request_data.get("life_events") or {}),
        "calibration": _clean_mapping(request_data.get("calibration") or {}),
        "contact": _clean_mapping(contact),
        "preferences": _clean_mapping(preferences),
        "current_problem": (request_data.get("current_problem") or "").strip(),
    }


def _metric_extremes(scores: Dict[str, Any]) -> tuple[tuple[str, int], tuple[str, int]]:
    metric_pairs = []
    for key in METRIC_LABELS:
        raw_value = scores.get(key, 50)
        try:
            value = int(raw_value)
        except (TypeError, ValueError):
            value = 50
        metric_pairs.append((key, value))

    strongest = max(metric_pairs, key=lambda item: item[1])
    weakest = min(metric_pairs, key=lambda item: item[1])
    return strongest, weakest


def _build_personalized_fallback(
    intake_context: Dict[str, Any],
    numerology_core: Dict[str, Any],
    scores: Dict[str, Any],
    current_problem: str,
) -> Dict[str, Any]:
    identity = intake_context.get("identity") or {}
    birth_details = intake_context.get("birth_details") or {}
    focus = intake_context.get("focus") or {}
    financial = intake_context.get("financial") or {}
    career = intake_context.get("career") or {}
    emotional = intake_context.get("emotional") or {}

    full_name = identity.get("full_name") or "User"
    first_name = full_name.split()[0] if full_name else "User"
    focus_key = focus.get("life_focus") or "general_alignment"
    focus_label = FOCUS_LABELS.get(focus_key, FOCUS_LABELS["general_alignment"])
    focus_action = FOCUS_ACTIONS.get(focus_key, FOCUS_ACTIONS["general_alignment"])

    pythagorean = numerology_core.get("pythagorean") or {}
    life_path = pythagorean.get("life_path_number")
    destiny_number = pythagorean.get("destiny_number")

    strongest, weakest = _metric_extremes(scores)
    strongest_label = METRIC_LABELS[strongest[0]]
    weakest_label = METRIC_LABELS[weakest[0]]
    strongest_message = METRIC_STRENGTHS[strongest[0]]
    weakest_message = METRIC_RISKS[weakest[0]]

    confidence = scores.get("confidence_score", 50)
    risk_band = scores.get("risk_band", "Correctable")
    monthly_income = financial.get("monthly_income")
    risk_tolerance = financial.get("risk_tolerance")
    industry = career.get("industry")
    role = career.get("role") or "professional"
    anxiety_level = emotional.get("anxiety_level")
    decision_confusion = emotional.get("decision_confusion")
    date_of_birth = birth_details.get("date_of_birth") or identity.get("date_of_birth")

    problem_statement = current_problem or "general direction aur long-term stability"
    role_phrase = role.replace("_", " ")
    industry_phrase = f" in {industry}" if industry else ""
    income_phrase = f" Current monthly income around {monthly_income} indicate karti hai." if monthly_income else ""
    risk_phrase = f" Risk tolerance abhi {str(risk_tolerance).lower()} side par hai." if risk_tolerance else ""
    anxiety_phrase = f" Reported anxiety level {anxiety_level}/10 hai." if anxiety_level is not None else ""
    confusion_phrase = (
        f" Decision confusion {decision_confusion}/10 hai, isliye bade choices me extra validation helpful rahega."
        if decision_confusion is not None
        else ""
    )
    date_phrase = f" Date of birth input {date_of_birth} se numerology core derive hua hai." if date_of_birth else ""

    business_signals = numerology_core.get("business_analysis") or {}
    business_strength = business_signals.get(
        "business_strength",
        f"{first_name}'s profile supports strategic work that rewards clarity, reputation, and disciplined follow-through.",
    )
    business_risk = business_signals.get(
        "risk_factor",
        f"The main business risk is that {weakest_label.lower()} may slow execution when pressure rises.",
    )
    compatible_industries = business_signals.get("compatible_industries") or []

    compatibility = numerology_core.get("compatibility") or {}
    compatibility_guidance = (
        f"Current compatibility signal is {compatibility.get('compatibility_level', 'Moderate')} "
        f"with score {compatibility.get('compatibility_score', 0)}/100."
        if compatibility
        else f"{first_name} benefits most from relationships that reinforce {strongest_label.lower()} and reduce pressure on {weakest_label.lower()}."
    )

    compatible_numbers = [number for number in [life_path, destiny_number] if isinstance(number, int)]
    challenging_numbers = []

    return {
        "_fallback_used": True,
        "executive_brief": {
            "summary": (
                f"{full_name}'s report is centered on {focus_label}. "
                f"Life Path {life_path or 'N/A'} and Destiny {destiny_number or 'N/A'} suggest a profile with "
                f"{strongest_message}, while the current pressure point is {weakest_message}. "
                f"The immediate concern is {problem_statement}.{date_phrase}"
            ),
            "key_strength": f"Aapka strongest signal {strongest_label} hai. Iska matlab hai {strongest_message}.",
            "key_risk": f"Lowest signal {weakest_label} hai, jo yeh batata hai ki {weakest_message}.",
            "strategic_focus": (
                f"Priority now is to {focus_action}. Decisions should be filtered through stronger {weakest_label.lower()} routines."
            ),
        },
        "analysis_sections": {
            "career_analysis": (
                f"As a {role_phrase}{industry_phrase}, {first_name} is more likely to progress through roles that reward "
                f"{strongest_label.lower()} instead of constant reactive change. Dharma alignment is {scores.get('dharma_alignment_score', 50)}/100, "
                f"so work choices should stay close to the stated goal of {focus_label}."
            ),
            "decision_profile": (
                f"Current decision confidence is {confidence}/100 and the overall risk band is {risk_band}. "
                f"{confusion_phrase if confusion_phrase else 'Major choices will improve when decisions are slowed down enough to validate assumptions.'}"
            ),
            "emotional_analysis": (
                f"Emotional regulation is {scores.get('emotional_regulation_index', 50)}/100. {anxiety_phrase}"
                f"This suggests that recovery routines and lower-noise environments will directly improve judgment quality."
            ),
            "financial_analysis": (
                f"Financial discipline is {scores.get('financial_discipline_index', 50)}/100{income_phrase}."
                f"{risk_phrase} The most useful shift now is to make money decisions more structured and less reactive."
            ),
        },
        "strategic_guidance": {
            "short_term": f"Short term me pehle {weakest_label.lower()} ko stabilize karein aur focus ko {focus_label} par centered rakhein.",
            "mid_term": f"Mid term me {strongest_label.lower()} ko repeatable weekly system me convert karein, especially work aur finance decisions me.",
            "long_term": f"Use Life Path {life_path or 'N/A'} as a guide for bigger moves and only scale once {weakest_label.lower()} is no longer a recurring bottleneck.",
        },
        "growth_blueprint": {
            "phase_1": f"Noise kam karke {problem_statement} ke around stable base create karein.",
            "phase_2": f"{strongest_label.lower()} ko visible advantage banayein through consistency, better filters, aur cleaner routines.",
            "phase_3": f"Expand into bigger opportunities once {focus_label} is supported by stronger execution discipline.",
        },
        "business_block": {
            "business_strength": business_strength,
            "risk_factor": business_risk,
            "compatible_industries": compatible_industries,
        },
        "compatibility_block": {
            "compatible_numbers": compatible_numbers,
            "challenging_numbers": challenging_numbers,
            "relationship_guidance": compatibility_guidance,
        },
    }


# =====================================================
# INPUT FLATTENER
# =====================================================


def flatten_input(data: Dict[str, Any]) -> Dict[str, Any]:

    data = data or {}

    financial = data.get("financial") or {}
    career = data.get("career") or {}
    emotional = data.get("emotional") or {}
    focus = data.get("focus") or {}
    life_events = data.get("life_events") or {}
    calibration = data.get("calibration") or {}

    decision_confusion = emotional.get("decision_confusion")
    impulse_control = emotional.get("impulse_control")

    decision_clarity = None
    if decision_confusion is not None:
        decision_clarity = max(1, min(10, 11 - int(decision_confusion)))

    impulse_spending = None
    if impulse_control is not None:
        impulse_spending = max(1, min(10, 11 - int(impulse_control)))

    return {

        "monthly_income": financial.get("monthly_income"),
        "savings_ratio": financial.get("savings_ratio"),
        "debt_ratio": financial.get("debt_ratio"),
        "risk_tolerance": financial.get("risk_tolerance"),
        "impulse_spending": impulse_spending,

        "industry": career.get("industry"),
        "role": career.get("role"),
        "years_experience": career.get("years_experience"),
        "stress_level": career.get("stress_level"),

        "anxiety": emotional.get("anxiety_level"),
        "decision_confusion": decision_confusion,
        "decision_clarity": decision_clarity,
        "impulse_control": impulse_control,
        "emotional_stability": emotional.get("emotional_stability"),

        "life_focus": focus.get("life_focus"),
        "major_setbacks": len(life_events.get("setback_events_years") or []),

        "stress_response": calibration.get("stress_response"),
        "money_decision_style": calibration.get("money_decision_style"),
        "biggest_weakness": calibration.get("biggest_weakness"),
        "life_preference": calibration.get("life_preference"),
        "decision_style": calibration.get("decision_style"),
    }


# =====================================================
# SAFE AI WRAPPER
# Guarantees structure even if LLM fails
# =====================================================


def safe_generate_ai_narrative(
    numerology_core,
    scores,
    current_problem,
    plan_name,
    token_multiplier,
    intake_context,
):

    try:

        ai_sections = generate_ai_narrative(
            numerology_core=numerology_core,
            scores=scores,
            current_problem=current_problem,
            plan_name=plan_name,
            token_multiplier=token_multiplier,
            intake_context=intake_context,
        )

        if isinstance(ai_sections, dict) and ai_sections.get("executive_brief"):
            ai_sections["_fallback_used"] = False
            return ai_sections

        raise ValueError("AI returned invalid structure")

    except Exception:

        traceback.print_exc()

        return _build_personalized_fallback(
            intake_context=intake_context,
            numerology_core=numerology_core,
            scores=scores,
            current_problem=current_problem,
        )


# =====================================================
# MASTER REPORT GENERATOR
# =====================================================


def generate_life_signify_report(
    request_data: Dict[str, Any],
    plan_name: str = "basic",
) -> Dict[str, Any]:

    plan_name = (plan_name or "basic").lower()

    features = PLAN_FEATURES.get(plan_name, PLAN_FEATURES["basic"])

    intake_context = _build_intake_context(request_data)
    identity = intake_context.get("identity") or {}
    birth_details = intake_context.get("birth_details") or {}
    current_problem = intake_context.get("current_problem")

    # -------------------------------------------------
    # NUMEROLOGY CORE ENGINE
    # -------------------------------------------------

    numerology_core = generate_numerology_profile(
        identity=identity,
        birth_details=birth_details,
        plan_name=plan_name,
    ) or {}

    # -------------------------------------------------
    # BUSINESS NUMBER ENGINE
    # -------------------------------------------------

    try:
        business_signals = analyze_business_name(
            identity.get("business_name")
        )
    except Exception:
        traceback.print_exc()
        business_signals = {}

    numerology_core["business_analysis"] = business_signals

    # -------------------------------------------------
    # BEHAVIORAL SCORING ENGINE
    # -------------------------------------------------

    flat_data = flatten_input(request_data)

    scores = generate_score_summary(flat_data) or {}

    # -------------------------------------------------
    # ARCHETYPE ENGINE
    # -------------------------------------------------

    archetype = generate_numerology_archetype(
        numerology_core,
        scores
    )

    # -------------------------------------------------
    # REMEDY ENGINE
    # -------------------------------------------------

    remedies = generate_remedy_protocol(
        numerology_core,
        scores=scores,
    )

    # -------------------------------------------------
    # AI NARRATIVE
    # -------------------------------------------------

    ai_sections = safe_generate_ai_narrative(
        numerology_core=numerology_core,
        scores=scores,
        current_problem=current_problem,
        plan_name=plan_name,
        token_multiplier=features["token_multiplier"],
        intake_context=intake_context,
    )

    # -------------------------------------------------
    # RADAR CHART DATA
    # -------------------------------------------------

    radar_chart_data = {
        "Life Stability": scores.get("life_stability_index", 50),
        "Decision Clarity": scores.get("confidence_score", 50),
        "Dharma Alignment": scores.get("dharma_alignment_score", 50),
        "Emotional Regulation": scores.get("emotional_regulation_index", 50),
        "Financial Discipline": scores.get("financial_discipline_index", 50),
    }

    # -------------------------------------------------
    # FINAL REPORT JSON
    # -------------------------------------------------

    report_output = {

        "meta": {
            "report_version": "5.3",
            "engine_version": settings.ENGINE_VERSION,
            "plan_tier": plan_name,
            "generated_at": datetime.utcnow().isoformat(),
            "used_fallback_narrative": ai_sections.get("_fallback_used", False),
        },

        "identity": identity,

        "birth_details": birth_details,

        "focus": intake_context.get("focus") or {},

        "preferences": intake_context.get("preferences") or {},

        "current_problem": current_problem,

        "core_metrics": scores,

        "numerology_core": numerology_core,

        "executive_brief": ai_sections.get("executive_brief"),

        "analysis_sections": ai_sections.get("analysis_sections"),

        "strategic_guidance": ai_sections.get("strategic_guidance"),

        "growth_blueprint": ai_sections.get("growth_blueprint"),

        "business_block": ai_sections.get("business_block"),

        "compatibility_block": ai_sections.get("compatibility_block"),

        "radar_chart_data": radar_chart_data,

        "lifestyle_remedies": remedies.get("lifestyle_remedies"),

        "mobile_remedies": remedies.get("mobile_remedies"),

        "vedic_remedies": remedies.get("vedic_remedies"),

        "daily_energy_alignment": remedies.get("daily_energy_alignment"),

        "numerology_archetype": archetype,

        "disclaimer": {
            "framework": "Tiered Numerology Intelligence System",
            "confidence_score": 88,
            "note": "Insights are probabilistic and strategic, not deterministic predictions.",
        },
    }

    return report_output




