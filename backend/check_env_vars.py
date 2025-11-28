import os
from dotenv import load_dotenv

load_dotenv(".env.local")

keys = ["LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET", "DEEPGRAM_API_KEY", "GOOGLE_API_KEY"]

print("--- ENV CHECK ---")
for key in keys:
    value = os.getenv(key)
    if value:
        masked = value[:4] + "..." + value[-4:] if len(value) > 8 else "****"
        print(f"{key}: {masked}")
    else:
        print(f"{key}: MISSING")
print("-----------------")
