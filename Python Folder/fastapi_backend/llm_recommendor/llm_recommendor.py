import requests
import json
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = os.getenv("MODEL_NAME")


def call_llm_recommendation(analytics_context, user_question):
    """
    Calls OpenRouter LLM using analytics context.
    Compatible with Gemma models (NO system/developer role).
    """

    combined_prompt = f"""
You are an AI assistant that provides retail business recommendations.

Rules:
- Use confidence-aware KPIs to suggest actions.
- If coverage is low, explain that decisions are deferred due to insufficient confidence.
- Do NOT assume missing data.
- Do NOT perform numerical analysis.
- Respond in clear, professional language.

Analytics Summary:
{json.dumps(analytics_context, indent=2)}

User Question:
{user_question}

Provide a concise, actionable recommendation.
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": combined_prompt
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "Retail Footfall Analytics Project"
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        print(response.text)

    response.raise_for_status()
    result = response.json()

    return result["choices"][0]["message"]["content"]


if __name__ == "__main__":
    dummy_context = {
        "baseline_kpis": {"footfall": 1000, "conversion_rate": 0.05},
        "confidence_kpis": {"footfall": 800, "conversion_rate": 0.04, "coverage": 0.8},
        "trend": {"slope": -0.02, "interpretation": "Stable demand"}
    }

    question = "Should we increase staffing on weekends?"

    recommendation = call_llm_recommendation(dummy_context, question)
    print("LLM Recommendation:")
    print(recommendation)
