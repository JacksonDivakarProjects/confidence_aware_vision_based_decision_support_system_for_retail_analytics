import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from fastapi_backend root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

print("API KEY LOADED:", os.getenv("OPENROUTER_API_KEY"))
