# Burger King Voice Agent - Day 7 Challenge 🍔�

Welcome to the **Burger King Voice Agent**! This project is a flame-grilled, premium voice assistant designed to bring the "Have it your way" experience to life through an interactive voice interface.

## About the Project

This agent acts as a **Burger King Ordering Assistant**. It helps users order Whoppers, fries, and deals with a seamless voice-first experience.

**Key Features:**
- **Burger King Persona**: Bold, confident, and fun ("Have it your way!").
- **Smart Cart**: Add items, remove items, and view your cart using natural language.
- **Deals & Combos**: Recognizes special deals like "Whopper Meal Deal" and "Family Feast".
- **Premium UI**: A "Flame Grilled" frontend with dynamic animations, rotating deals carousel, and a custom "Flame Button".

## Tech Stack

- **Backend**: Python, LiveKit Agents, Deepgram (Nova-3 STT, Aura TTS), Google Gemini 2.5 Flash (LLM).
- **Frontend**: Next.js 15 (Turbopack), Tailwind CSS, Framer Motion, LiveKit Components.
- **Design**: Custom Burger King theme (Red `#D62300`, Orange `#E55F25`, Brown `#502314`, Cream `#F5EBDC`).

## Quick Start

### Prerequisites

- Python 3.9+ with `uv`
- Node.js 18+ with `pnpm`
- LiveKit Server (local or cloud)

### 1. Backend Setup

```bash
cd backend
uv sync
cp .env.example .env.local
# Configure LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET, DEEPGRAM_API_KEY, GOOGLE_API_KEY
./restart_backend_debug.sh
```

### 2. Frontend Setup

```bash
cd frontend
pnpm install
cp .env.example .env.local
# Configure LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET
./restart_frontend.sh
```

### 3. Run

Open `http://localhost:3000` (or the port shown in your terminal) to start ordering!

## License

MIT
