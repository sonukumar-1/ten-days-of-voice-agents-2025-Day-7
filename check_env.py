from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path("backend/.env.local")
load_dotenv(dotenv_path=env_path)

required_keys = [
    "LIVEKIT_URL",
    "LIVEKIT_API_KEY",
    "LIVEKIT_API_SECRET",
    "OPENAI_API_KEY",
    "DEEPGRAM_API_KEY",
    "GOOGLE_API_KEY"
]

print("Environment Variable Check:")
for key in required_keys:
    value = os.getenv(key)
    status = "Present" if value else "MISSING"
    if key == "LIVEKIT_URL" and value:
        print(f"{key}: {value} ({status})")
    else:
        print(f"{key}: {status}")
