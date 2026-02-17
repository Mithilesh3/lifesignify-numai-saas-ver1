from openai import OpenAI
from app.core.llm_config import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ai_narrative(flat_data: dict, scores: dict) -> dict:

    prompt = f"""
You are an elite behavioral intelligence system.

User Behavioral Scores:
{scores}

User Profile Data:
{flat_data}

Generate:

1. Executive Summary (professional tone)
2. Psychological Pattern Analysis
3. Strategic Advice
4. 30-Day Action Plan
5. 90-Day Growth Plan

Be precise. Avoid fluff. Keep it structured.
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": "You are a strategic behavioral intelligence analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=LLM_TEMPERATURE,
        max_tokens=LLM_MAX_TOKENS,
    )

    text = response.choices[0].message.content

    return {
        "ai_full_narrative": text
    }
