import os
from pathlib import Path
from dotenv import load_dotenv
import asyncio

# Load environment variables
env_path = Path(__file__).parent / "backend" / ".env.local"
load_dotenv(dotenv_path=env_path)

async def test_gemini():
    print("Testing Gemini API...")
    try:
        from livekit.plugins import google
        llm = google.LLM(model="gemini-2.5-flash")
        
        # Test simple completion
        stream = llm.chat(
            chat_ctx=google.llm.ChatContext(
                messages=[
                    google.llm.ChatMessage(
                        role="user",
                        content="Say 'Hello from Gemini' in exactly those words."
                    )
                ]
            )
        )
        
        response_text = ""
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                response_text += chunk.choices[0].delta.content
                
        print(f"✅ Gemini Response: {response_text}")
        return True
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_murf():
    print("\nTesting Murf TTS API...")
    try:
        from livekit.plugins import murf
        tts = murf.TTS(model="en-US-falcon")
        
        # Test simple TTS
        stream = tts.synthesize("Hello from Murf TTS")
        
        audio_data = b""
       async for chunk in stream:
            audio_data += chunk.data
            
        print(f"✅ Murf Response: Generated {len(audio_data)} bytes of audio")
        return True
    except Exception as e:
        print(f"❌ Murf Error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    gemini_ok = await test_gemini()
    murf_ok = await test_murf()
    
    print("\n" + "="*50)
    print("Test Results:")
    print(f"Gemini LLM: {'✅ Working' if gemini_ok else '❌ Failed'}")
    print(f"Murf TTS: {'✅ Working' if murf_ok else '❌ Failed'}")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main())
