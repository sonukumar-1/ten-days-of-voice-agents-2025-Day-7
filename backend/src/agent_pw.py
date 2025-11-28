import logging
from pathlib import Path
from dotenv import load_dotenv
import os

# Load env vars BEFORE importing livekit to ensure they are picked up
env_path = Path(__file__).parent.parent / ".env.local"
load_dotenv(dotenv_path=env_path)

import json
import traceback
from datetime import datetime
from typing import Annotated, Dict, Any

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    function_tool,
    RunContext,
    llm,
)
from livekit.plugins import openai, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("pw-sdr-agent")


class PhysicsWallahSDRAgent(Agent):
    def __init__(self) -> None:
        # Load content
        self.content = self._load_content()
        self.leads_path = Path(__file__).resolve().parent.parent.parent / "shared-data" / "leads.json"
        
        super().__init__(
            instructions=self._get_instructions(),
        )

    def _load_content(self) -> Dict[str, Any]:
        try:
            content_path = Path(__file__).resolve().parent.parent.parent / "shared-data" / "pw_content.json"
            with open(content_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading content: {e}")
            return {}

    def _get_instructions(self) -> str:
        company_info = self.content.get("company_info", {})
        verticals = self.content.get("verticals", [])
        faqs = self.content.get("faqs", [])
        
        verticals_str = "\n".join([f"- {v['name']}: {v['description']}" for v in verticals])
        faqs_str = "\n".join([f"Q: {f['question']}\nA: {f['answer']}" for f in faqs])
        
        return f"""
        You are a friendly and energetic Sales Development Representative (SDR) for **{company_info.get('name', 'Physics Wallah')}**.
        
        **COMPANY OVERVIEW:**
        {company_info.get('description')}
        Mission: {company_info.get('mission')}
        
        **KEY OFFERINGS:**
        {verticals_str}
        
        **FAQ KNOWLEDGE BASE:**
        {faqs_str}
        
        **YOUR GOAL:**
        1.  **Qualify the Lead:** Warmly engage with the student or parent. Find out who they are (Student/Parent), their Class/Grade, and what Exam they are targeting (JEE, NEET, Boards, etc.).
        2.  **Answer Questions:** Use the FAQ and Offerings info to answer questions about courses, pricing (mention affordability), and faculties.
        3.  **Close:** Once you have their details and have answered their questions, summarize their interest and end the call with high energy ("Padhai Karte Raho!", "All the best!").
        
        **YOUR PERSONA:**
        - **Tone:** Professional, Warm, Efficient, and Encouraging. You are an expert Admission Counselor.
        - **Greeting:** "Hello! Welcome to Physics Wallah's Admission Cell. I am your AI Counselor. I can help you find the perfect course and batch for your goals. To get started, may I know your name?"
        - **Behavior:**
          - Be concise and professional.
          - Focus on gathering requirements (Class, Exam, Goals) to suggest the best batch.
          - Provide clear, accurate information about fee structures and scholarships.
          - Guide the user towards enrollment.
        
        **LEAD CAPTURE:**
        You must collect: Name, Role (Student/Parent), Class/Grade, Target Exam, Email, Timeline (When they want to join).
        When the user indicates they are done (e.g., "That's all", "Thanks"), or after you have collected all info:
        1.  Verbally summarize what you have recorded (e.g., "Thank you [Name]. I have noted your interest in [Exam] for Class [Class]...").
        2.  Call the `save_lead` tool.
        """

    @function_tool
    async def save_lead(
        self,
        ctx: RunContext,
        name: Annotated[str, "Full Name"],
        role: Annotated[str, "Role (Student or Parent)"],
        grade: Annotated[str, "Class or Grade (e.g., 11th, 12th, Dropper)"],
        target_exam: Annotated[str, "Target Exam (e.g., JEE, NEET, UPSC)"],
        email: Annotated[str, "Email Address"],
        timeline: Annotated[str, "When they plan to join (e.g., Immediately, Next Year)"] = "Not specified",
        use_case: Annotated[str, "Specific goal or use case"] = "Exam Preparation",
        team_size: Annotated[str, "Study group size or 'Individual'"] = "Individual",
        company: Annotated[str, "School or College Name"] = "Not specified",
    ):
        """Save the lead's information to the database. Call this at the end of the conversation."""
        try:
            lead_data = {
                "timestamp": datetime.now().isoformat(),
                "name": name,
                "role": role,
                "grade": grade,
                "target_exam": target_exam,
                "email": email,
                "timeline": timeline,
                "use_case": use_case,
                "team_size": team_size,
                "company": company # Mapping School/College to company field for consistency with prompt requirements
            }
            
            # Load existing leads
            leads = []
            if self.leads_path.exists():
                with open(self.leads_path, "r") as f:
                    try:
                        leads = json.load(f)
                    except json.JSONDecodeError:
                        leads = []
            
            leads.append(lead_data)
            
            # Save back
            with open(self.leads_path, "w") as f:
                json.dump(leads, f, indent=2)
                
            logger.info(f"Lead saved: {name}, {target_exam}")
            return "Lead saved successfully. All the best for your preparation!"
            
        except Exception as e:
            logger.error(f"Error saving lead: {e}")
            return "There was an error saving your details, but I have noted them down."

def prewarm(proc: JobProcess):
    """Preload models to minimize first-call latency"""
    # Preload VAD model
    proc.userdata["vad"] = silero.VAD.load()
    
    # Preload STT model to reduce initialization time
    proc.userdata["stt"] = deepgram.STT(model="nova-3")


async def entrypoint(ctx: JobContext):
    try:
        ctx.log_context_fields = {
            "room": ctx.room.name,
        }

        # Initialize the agent
        agent = PhysicsWallahSDRAgent()

        session = AgentSession(
            stt=ctx.proc.userdata.get("stt") or deepgram.STT(model="nova-3"),
            llm=google.LLM(
                model="gemini-2.5-flash",
            ),
            # Use Deepgram Aura TTS (reliable fallback)
            tts=deepgram.TTS(
                model="aura-helios-en",  # Professional male voice
            ), 
            turn_detection=MultilingualModel(),
            vad=ctx.proc.userdata["vad"],
            preemptive_generation=True,
        )
        
        usage_collector = metrics.UsageCollector()

        @session.on("metrics_collected")
        def _on_metrics_collected(ev: MetricsCollectedEvent):
            metrics.log_metrics(ev.metrics)
            usage_collector.collect(ev.metrics)

        async def log_usage():
            summary = usage_collector.get_summary()
            logger.info(f"Usage: {summary}")

        ctx.add_shutdown_callback(log_usage)

        await session.start(
            agent=agent,
            room=ctx.room,
            room_input_options=RoomInputOptions(
                noise_cancellation=noise_cancellation.BVC(),
            ),
        )

        await ctx.connect()
    
    except Exception as e:
        logger.error(f"Error in entrypoint: {e}")
        logger.error(traceback.format_exc())
        raise e


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint, 
            prewarm_fnc=prewarm,
            ws_url=os.getenv("LIVEKIT_URL"),
            api_key=os.getenv("LIVEKIT_API_KEY"),
            api_secret=os.getenv("LIVEKIT_API_SECRET"),
        )
    )
