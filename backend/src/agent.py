import logging
from pathlib import Path
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from typing import Annotated, Dict, Any, Optional, List

# Load env vars
env_path = Path(__file__).parent.parent / ".env.local"
load_dotenv(dotenv_path=env_path)

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
from livekit.plugins import silero, google, deepgram, noise_cancellation, murf
from livekit.plugins.turn_detector.multilingual import MultilingualModel

try:
    from src.cart import Cart
    from src.order_manager import OrderManager
except ImportError:
    from cart import Cart
    from order_manager import OrderManager

logger = logging.getLogger("grocery-agent")

# Load Catalog
CATALOG_PATH = Path(__file__).parent.parent.parent / "shared-data" / "burgerking_content.json"
try:
    with open(CATALOG_PATH, "r") as f:
        CATALOG = json.load(f)
    logger.info(f"Loaded catalog with {len(CATALOG)} items")
except Exception as e:
    logger.error(f"Failed to load catalog: {e}")
    CATALOG = []

class GroceryAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=self._get_instructions(),
        )
        self.cart = Cart()
        self.order_manager = OrderManager(orders_dir=str(Path(__file__).parent.parent / "orders"))
        self.catalog_lookup = {item["name"].lower(): item for item in CATALOG}

    def _get_instructions(self) -> str:
        return """
        You are a **Burger King Ordering Assistant**.
        
        **YOUR GOAL:**
        Help users order flame-grilled burgers, fries, and beverages.
        
        **CAPABILITIES:**
        1.  **Add Items:** Add specific items to the cart (e.g., "I want a Whopper").
        2.  **Recommend Combos:** If a user asks for a burger, suggest adding fries and a drink to make it a meal.
        3.  **Manage Cart:** Remove items, update quantities, or clear the cart.
        4.  **Check Cart:** List what's in the cart.
        5.  **Checkout:** Confirm the order and save it.

        **CATALOG:**
        You have access to the Burger King menu, including these **SPECIAL DEALS**:
        - **Whopper Meal Deal** (₹299): Whopper + Fries + Pepsi.
        - **Family Feast** (₹599): 2 Whoppers + 2 Fries + 2 Pepsis + Onion Rings.
        - **Snack Box** (₹199): Crispy Veg + Small Fries + Pepsi.

        If a user asks for something not in the menu (like Big Mac), politely say you serve the best flame-grilled burgers, not that other stuff.

        **TONE:**
        - Bold, confident, and fun ("Have it your way!").
        - Confirm actions clearly.
        - Always upsell politely (e.g., "Want to make that a meal with fries and a Pepsi?").
        - When the user says "that's all" or "place order", summarize the cart and ask for confirmation.

        **TOOLS:**
        - `add_to_cart`: Add items.
        - `remove_from_cart`: Remove items.
        - `view_cart`: Get current cart state.
        - `place_order`: Finalize the order.
        - `recommend_meal_upgrade`: Suggest items to complete a meal.
        """

    @function_tool
    async def add_to_cart(
        self,
        ctx: RunContext,
        item_name: Annotated[str, "The name of the item to add"],
        quantity: Annotated[int, "The quantity to add"] = 1,
        notes: Annotated[str, "Any special notes (e.g., 'no onions')"] = "",
    ):
        """Add an item to the cart. Tries to match item_name to catalog."""
        logger.info(f"Tool add_to_cart called: {item_name} x{quantity}")
        
        # Simple fuzzy match or direct lookup
        item_key = item_name.lower()
        matched_item = None
        
        # Exact match
        if item_key in self.catalog_lookup:
            matched_item = self.catalog_lookup[item_key]
        else:
            # Partial match
            for name, item in self.catalog_lookup.items():
                if item_key in name or name in item_key:
                    matched_item = item
                    break
        
        if not matched_item:
            return f"I couldn't find '{item_name}' in our menu. We have favorites like the Whopper, Chicken Royale, and more."

        added_item = self.cart.add_item(
            item_id=matched_item["id"],
            name=matched_item["name"],
            price=matched_item["price"],
            quantity=quantity,
            notes=notes
        )
        
        return f"Added {quantity}x {matched_item['name']} to cart. Total: ₹{self.cart.get_total():.2f}"

    @function_tool
    async def remove_from_cart(
        self,
        ctx: RunContext,
        item_name: Annotated[str, "The name of the item to remove"],
    ):
        """Remove an item from the cart."""
        # Find item in cart by name
        item_id_to_remove = None
        for item in self.cart.items.values():
            if item_name.lower() in item.name.lower():
                item_id_to_remove = item.id
                break
        
        if item_id_to_remove:
            removed = self.cart.remove_item(item_id_to_remove)
            return f"Removed {removed.name} from your cart."
        else:
            return f"I couldn't find '{item_name}' in your cart."

    @function_tool
    async def view_cart(self, ctx: RunContext):
        """Get the current status of the cart."""
        return str(self.cart)

    @function_tool
    async def recommend_meal_upgrade(
        self,
        ctx: RunContext,
        base_item: Annotated[str, "The item the user just ordered (e.g., 'burger')"],
    ):
        """Suggests adding fries and a drink to make it a meal."""
        logger.info(f"Tool recommend_meal_upgrade called for: {base_item}")
        
        suggestions = []
        if "fries" not in str(self.cart).lower():
             suggestions.append("Fries (Medium)")
        if "pepsi" not in str(self.cart).lower():
             suggestions.append("Pepsi (Medium)")

        if suggestions:
            # We don't auto-add, just return text for the LLM to say
            return f"Would you like to make that a meal by adding {', '.join(suggestions)}?"
        else:
            return "You've got a great meal there! Anything else?"

    @function_tool
    async def place_order(self, ctx: RunContext):
        """Finalize the order and save it."""
        if not self.cart.items:
            return "Your cart is empty. I can't place an empty order."
        
        try:
            order_id = self.order_manager.place_order(self.cart)
            total = self.cart.get_total()
            self.cart.clear() # Clear cart after order
            return f"Order placed successfully! Order ID is {order_id}. Total amount: ₹{total:.2f}. Thank you for choosing Burger King!"
        except Exception as e:
            logger.error(f"Failed to place order: {e}")
            return "I'm sorry, there was an issue placing your order. Please try again."

def prewarm(proc: JobProcess):
    try:
        logger.info("Starting prewarm...")
        proc.userdata["vad"] = silero.VAD.load()
        proc.userdata["stt"] = deepgram.STT(model="nova-3")
        # proc.userdata["turn_detection"] = MultilingualModel()
        
        if not os.getenv("DEEPGRAM_API_KEY"):
            logger.error("DEEPGRAM_API_KEY is missing")
        if not os.getenv("GOOGLE_API_KEY"):
            logger.error("GOOGLE_API_KEY is missing")
            
        logger.info("Prewarm completed")
    except Exception as e:
        logger.error(f"Prewarm failed: {e}", exc_info=True)
        raise e

async def entrypoint(ctx: JobContext):
    try:
        logger.info("Entrypoint started")
        ctx.log_context_fields = {"room": ctx.room.name}
        
        agent = GroceryAgent()
        
        session = AgentSession(
            stt=ctx.proc.userdata.get("stt") or deepgram.STT(model="nova-3"),
            llm=google.LLM(model="gemini-2.5-flash"),
            tts=deepgram.TTS(model="aura-helios-en"), 
            turn_detection=ctx.proc.userdata.get("turn_detection") or MultilingualModel(),
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

        logger.info("Starting session...")
        await session.start(
            agent=agent,
            room=ctx.room,
            room_input_options=RoomInputOptions(
                noise_cancellation=noise_cancellation.BVC(),
            ),
        )
        
        logger.info("Connecting to room...")
        await ctx.connect()
        logger.info("Connected to room")
        
        # Initial greeting
        await session.say("Welcome to Burger King! Home of the Whopper. What can I get for you today?", add_to_chat_ctx=True)
        logger.info("Initial greeting sent")

    except Exception as e:
        logger.error(f"Error in entrypoint: {e}")
        raise e

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint, 
            prewarm_fnc=prewarm,
            agent_name="freshmarket-agent",
            ws_url=os.getenv("LIVEKIT_URL"),
            api_key=os.getenv("LIVEKIT_API_KEY"),
            api_secret=os.getenv("LIVEKIT_API_SECRET"),
        )
    )

