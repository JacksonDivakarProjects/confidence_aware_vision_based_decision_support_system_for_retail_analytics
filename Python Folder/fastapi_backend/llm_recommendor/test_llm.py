import requests
import json
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env explicitly
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("OPENROUTER_API_KEY")
print("API KEY LOADED:", bool(API_KEY))

url = "https://openrouter.ai/api/v1/chat/completions"

payload = {
    "model": "xiaomi/mimo-v2-flash:free",
    "messages": [
        {"role": "user", "content": "Say hello"}
    ]
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    # 🔑 REQUIRED BY OPENROUTER
    "HTTP-Referer": "http://localhost:3000",
    "X-Title": "Retail Footfall Analytics Project"
}

response = requests.post(
    url,
    headers=headers,
    data=json.dumps(payload),
    timeout=30
)

print("Status Code:", response.status_code)
print("Raw Response:", response.text)
