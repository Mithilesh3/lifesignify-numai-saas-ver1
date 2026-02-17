import os
from typing import Dict, Any
from openai import AzureOpenAI


# =====================================================
# AZURE OPENAI CLIENT INITIALIZATION
# =====================================================
azure_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1-mini")


# =====================================================
# PROMPT BUILDER
# =====================================================
def build_prompt(flat_data: Dict[str, Any], scores: Dict[str, Any]) -> str:

    return f"""
You are an advanced behavioral intelligence system inspired by Sanatana Dharma principles.

User Profile:
- Monthly Income: {flat_data.get("monthly_income")}
- Savings Ratio: {flat_data.get("savings_ratio")}
- Debt Ratio: {flat_data.get("debt_ratio")}
- Industry: {flat_data.get("industry")}
- Experience: {flat_data.get("years_experience")} years
- Stress Level: {flat_data.get("stress_level")}
- Anxiety: {flat_data.get("anxiety")}
- Major Setbacks: {flat_data.get("major_setbacks")}

System Scores:
{scores}

Generate a structured premium-level life analysis report including:

1. Executive Summary
2. Behavioral Pattern Insights
3. Financial Discipline Commentary
4. Emotional Regulation Commentary
5. Strategic Growth Direction
6. Risk Interpretation
7. Clear Actionable Guidance

Tone:
- Deep
- Strategic
- Insightful
- Investor-grade
- Non-mystical but wisdom-inspired

Do not mention being an AI.
Do not provide deterministic predictions.
Limit to 800-1200 words.
"""


# =====================================================
# MAIN AI NARRATIVE GENERATOR
# =====================================================
def generate_ai_narrative(
    flat_data: Dict[str, Any],
    scores: Dict[str, Any]
) -> Dict[str, Any]:

    prompt = build_prompt(flat_data, scores)

    try:
        response = azure_client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a high-level behavioral intelligence strategist."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1500,
        )

        content = response.choices[0].message.content

        return {
            "ai_full_narrative": content
        }

    except Exception as e:
        return {
            "ai_full_narrative": "AI narrative generation temporarily unavailable.",
            "error": str(e)
        }
