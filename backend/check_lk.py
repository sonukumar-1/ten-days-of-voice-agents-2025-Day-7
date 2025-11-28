import os
import asyncio
from livekit import api
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env.local"
load_dotenv(dotenv_path=env_path)

async def main():
    url = os.getenv("LIVEKIT_URL")
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")

    print(f"URL: {url}")
    print(f"API Key: {api_key}")
    print(f"API Secret: {api_secret[:5]}..." if api_secret else "None")

    if not url or not api_key or not api_secret:
        print("Missing credentials!")
        return

    lkapi = api.LiveKitAPI(url, api_key, api_secret)
    try:
        rooms = await lkapi.room.list_rooms()
        print(f"Successfully connected! Found {len(rooms.rooms)} rooms.")
    except Exception as e:
        print(f"Failed to connect: {e}")
    finally:
        await lkapi.aclose()

if __name__ == "__main__":
    asyncio.run(main())
