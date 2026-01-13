import requests
import json
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    print("❌ OPENROUTER_API_KEY not found")
    exit(1)

url = "https://openrouter.ai/api/v1/chat/completions"

payload = {
    "model": "xiaomi/mimo-v2-flash:free",
    "messages": [
        {
            "role": "user",
            "content": "Give one simple retail staffing recommendation."
        }
    ],
    "reasoning": {"enabled": True}
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

try:
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload),
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Raw Response:", response.text)

    response.raise_for_status()

    result = response.json()
    print("\n✅ LLM RESPONSE:")
    print(result["choices"][0]["message"]["content"])

except requests.exceptions.HTTPError as e:
    print("\n❌ HTTP ERROR")
    print(e)
except requests.exceptions.RequestException as e:
    print("\n❌ REQUEST ERROR")
    print(e)
except Exception as e:
    print("\n❌ GENERAL ERROR")
    print(e)
