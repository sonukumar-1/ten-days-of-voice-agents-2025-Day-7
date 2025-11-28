# LiveKit Telephony Integration Guide (Day 6)

To run this Fraud Alert Agent with a real phone number using LiveKit Telephony, follow these steps:

## 1. Prerequisites
- A LiveKit Cloud project.
- A SIP Trunk provider (e.g., Twilio, Telnyx) or use LiveKit's built-in telephony if available.

## 2. Configure SIP Trunk
1.  Go to the **LiveKit Cloud Dashboard**.
2.  Navigate to **Settings** > **Telephony** (or **SIP**).
3.  **Create a SIP Trunk**:
    - Enter your SIP provider credentials.
    - Configure the numbers you want to use.

## 3. Create a Dispatch Rule
You need to tell LiveKit where to send incoming calls.
1.  Go to **SIP** > **Dispatch Rules**.
2.  Create a new Rule:
    - **Name**: `Fraud Agent Dispatch`
    - **Rule**: `Direct` (or specific number matching).
    - **Dispatch to**: `Room`
    - **Room Name**: `fraud-alert-room` (or use a dynamic pattern like `call-{caller_id}`).
    - **Agent Name**: Leave blank or specify if using explicit assignment.

## 4. Run the Agent
The agent is configured to connect to rooms. When a call comes in, LiveKit creates a room and the agent joins it.

To ensure the agent picks up the specific room:
- If you used a static room name (e.g., `fraud-alert-room`), run the agent normally. It will listen for any room.
- If you want to test locally, you can use the LiveKit CLI to simulate a SIP call or just connect to the room.

## 5. Testing
1.  Call the phone number configured.
2.  The call should be routed to LiveKit.
3.  The Agent should join the room and say "Hello...".
4.  Speak to the agent as if you are the customer.

## 6. Outbound Calls (Optional)
To make outbound calls, you would use the `livekit-api` to create a SIP participant in a room.
```python
from livekit import api
lkapi = api.LiveKitAPI()
room = await lkapi.room.create_room()
await lkapi.sip.create_sip_participant(
    api.CreateSIPParticipantRequest(
        room_name=room.name,
        sip_trunk_id="<trunk-id>",
        sip_call_to="<phone-number>",
    )
)
```
