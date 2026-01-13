import requests
import json
import os

from dotenv import load_dotenv

# Load .env file
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "xiaomi/mimo-v2-flash:free"


def call_llm_recommendation(analytics_context, user_question):
    """
    Calls OpenRouter LLM using aggregated analytics context
    """

    system_prompt = """
You are an AI assistant that provides retail business recommendations.
You MUST:
- Use only the provided analytics context
- Do NOT assume missing data
- Do NOT perform numerical analysis
- Respond in clear, professional language
"""

    user_prompt = f"""
Analytics Summary:
{json.dumps(analytics_context, indent=2)}

User Question:
{user_question}

Provide a concise, actionable recommendation.
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "reasoning": {"enabled": True}
    }

    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        data=json.dumps(payload),
        timeout=30
    )

    response.raise_for_status()
    result = response.json()

    return result["choices"][0]["message"]["content"]
