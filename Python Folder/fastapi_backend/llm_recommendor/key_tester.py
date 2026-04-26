import os
from dotenv import load_dotenv

#
load_dotenv()

print("API KEY LOADED:", os.getenv("OPENROUTER_API_KEY"))
