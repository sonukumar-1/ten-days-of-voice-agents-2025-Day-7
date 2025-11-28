import asyncio
import os
import aiohttp
from livekit.plugins import murf
from dotenv import load_dotenv

load_dotenv(".env.local")

async def main():
    async with aiohttp.ClientSession() as session:
        try:
            tts = murf.TTS(
                http_session=session,
                voice="Matthew",
                style="Conversation",
                speed=5,
                pitch=0,
                model="FALCON",
                sample_rate=24000,
            )
            print("Testing Murf TTS with model 'FALCON' and voice 'Matthew'...")
            async for audio in tts.synthesize("Hello, this is a test."):
                print("Received audio chunk")
                break
            print("Synthesis successful!")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
