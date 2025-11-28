# Day 6: Fraud Alert Voice Agent

This directory contains the implementation for the Fraud Alert Voice Agent.

## Setup

1.  **Database**: The SQLite database `fraud_cases.db` is automatically created and seeded by `src/database.py`.
    To reset/seed the database:
    ```bash
    uv run src/database.py
    ```

2.  **Agent**: The agent code is in `src/agent.py`.
    To run the agent:
    ```bash
    uv run src/agent.py start
    ```
    Or in dev mode:
    ```bash
    uv run src/agent.py dev
    ```

## Features

- **Database Integration**: Loads fraud cases from SQLite.
- **Identity Verification**: Asks a security question based on the user's file.
- **Transaction Review**: Reads out suspicious transaction details.
- **Outcome Tracking**: Updates the database with the result (Safe/Fraud) and a note.

## Telephony (Advanced Goal)

To use this agent with a real phone number via LiveKit Telephony, please refer to [SIP_GUIDE.md](SIP_GUIDE.md).

## Testing

1.  Start the agent.
2.  Connect to the room (using Playground or SIP).
3.  Say "Hello".
4.  The agent will ask for your username.
5.  Provide "john_doe" or "jane_smith".
6.  Answer the security question (John: "Smith", Jane: "Fluffy").
7.  Confirm or deny the transaction.
