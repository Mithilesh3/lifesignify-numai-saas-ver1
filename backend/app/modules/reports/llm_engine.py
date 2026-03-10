from typing import Dict, Any, Optional
from app.core.llm_config import azure_client, DEPLOYMENT_NAME
import json
import logging

logger = logging.getLogger(__name__)

# =====================================================
# TOKEN LIMIT PER PLAN
# =====================================================

PLAN_TOKEN_BASE = {
    "basic": 1600,
    "pro": 2200,
    "premium": 3000,
    "enterprise": 3800,
}


# =====================================================
# SAFE JSON PARSER
# =====================================================


def _safe_json_parse(raw_text: str) -> Dict[str, Any]:

    if not raw_text:
        return {}

    try:
        return json.loads(raw_text)

    except Exception:

        try:

            start = raw_text.index("{")
            end = raw_text.rindex("}") + 1

            return json.loads(raw_text[start:end])

        except Exception:

            logger.error("AI JSON parsing failed")

            return {}


# =====================================================
# MAIN AI REPORT GENERATOR
# =====================================================


def generate_ai_narrative(
    numerology_core: Dict[str, Any],
    scores: Dict[str, Any],
    current_problem: str,
    plan_name: str,
    token_multiplier: float = 1.0,
    intake_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:

    plan_name = (plan_name or "basic").lower()
    intake_context = intake_context or {}
    preferences = intake_context.get("preferences") or {}
    language_preference = str(preferences.get("language_preference") or "hindi").lower()

    base_tokens = PLAN_TOKEN_BASE.get(plan_name, 1600)
    max_tokens = int(base_tokens * token_multiplier)
    business_signals = numerology_core.get("business_analysis", {})

    prompt = f"""
You are an elite numerology strategist and behavioral intelligence advisor.

Do NOT calculate numerology numbers.
All numerology calculations are already provided.
Your task is to interpret them and generate a strategic life intelligence report.

Writing style requirements:
- The report must be written in Hindi-major language using Devanagari script.
- Keep the language ratio around 80-90% Hindi and 10-20% English.
- English words may be used for modern terms such as career, business, strategy, growth, leadership, execution.
- Never use Roman Hindi.
- Sound psychologically insightful, practical, and premium.
- Avoid generic astrology statements and avoid mystical exaggeration.
- Make the report feel clearly different for each user by grounding every section in the user's name, numerology values, strongest or weakest scores, and stated life focus.
- If data is missing, acknowledge the gap instead of inventing facts.
- If confidence_score is low or behavioral inputs are sparse, explicitly say that some intelligence metrics are based on limited inputs.

--------------------------------------------------

USER CURRENT PROBLEM
{current_problem}

--------------------------------------------------

USER PROFILE INPUT
{intake_context}

--------------------------------------------------

NUMEROLOGY CORE DATA
{numerology_core}

--------------------------------------------------

BUSINESS NUMEROLOGY SIGNALS
{business_signals}

--------------------------------------------------

BEHAVIORAL INTELLIGENCE SCORES
{scores}

--------------------------------------------------

PLAN TIER
{plan_name.upper()}

LEGACY LANGUAGE PREFERENCE
{language_preference}

Depth of analysis should increase with plan tier.
The wording should read like a premium North Indian life-intelligence report.
Even if a legacy preference says "hinglish", the final narration must still be Hindi-major in Devanagari script.

--------------------------------------------------

STRICT OUTPUT RULES

Return VALID JSON ONLY.
Do NOT include markdown.
Do NOT include explanations outside JSON.
Keep responses structured and professional.
- Keep each field concise but specific.

--------------------------------------------------

REQUIRED JSON STRUCTURE

{{
 "executive_brief": {{
   "summary": "",
   "key_strength": "",
   "key_risk": "",
   "strategic_focus": ""
 }},

 "analysis_sections": {{
   "career_analysis": "",
   "decision_profile": "",
   "emotional_analysis": "",
   "financial_analysis": ""
 }},

 "strategic_guidance": {{
   "short_term": "",
   "mid_term": "",
   "long_term": ""
 }},

 "growth_blueprint": {{
   "phase_1": "",
   "phase_2": "",
   "phase_3": ""
 }},

 "business_block": {{
   "business_strength": "",
   "risk_factor": "",
   "compatible_industries": []
 }},

 "compatibility_block": {{
   "compatible_numbers": [],
   "challenging_numbers": [],
   "relationship_guidance": ""
 }}
}}
"""

    try:

        response = azure_client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "system",
                    "content": """
You are an elite numerology strategist and behavioral intelligence advisor.
Do NOT calculate numerology numbers.
All numerology calculations are already provided.
Interpret them into a premium life intelligence report.
Write the report in Hindi-major language using Devanagari script.
Target a mix of roughly 80-90% Hindi and 10-20% English.
English words may be used for modern concepts such as career, business, strategy, growth, leadership, and execution.
Never write Roman Hindi.
Avoid generic astrology statements.
Make the output meaningfully different when user profile inputs differ.
If inputs are sparse, acknowledge that some intelligence scores are based on limited data.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=max_tokens,
        )

        raw_text = response.choices[0].message.content.strip()
        structured_output = _safe_json_parse(raw_text)

        summary = (
            structured_output.get("executive_brief", {}).get("summary")
            if isinstance(structured_output, dict)
            else ""
        )
        if not structured_output or not str(summary).strip():
            raise ValueError("Invalid JSON from AI")

        return structured_output

    except Exception as e:

        logger.error(f"AI generation failed: {str(e)}")

        return {}

