
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("TINYFISH_API_KEY")

if not api_key:
    raise ValueError("TinyFish API key not found in .env")

response = requests.get(
    "https://api.search.tinyfish.ai",
    headers={"X-API-Key": api_key},
    params={
        "query": "India Tele MANAS official mental health helpline"
    },
    timeout=30
)

response.raise_for_status()

print("TinyFish connection successful!")
print(response.json())
