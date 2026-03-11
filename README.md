# Buddy AI: Personal Mood-Based Chatbot 🤖✨

Buddy AI 2.0 is a cutting-edge, personal chatbot application that adapts its persona, voice, and UI to match your mood. Built with a **FastAPI** backend and a **React (Vite)** frontend, it leverages the power of **Gemini 2.5 Flash** to provide a truly interactive and context-aware experience.

---

## 🚀 Key Features

### 🌈 Mood-Based Personas
Chat with an AI that has a distinct personality! Choose from:
*   **Happy**: Cheerful, optimistic, and emoji-loving.
*   **Funny**: Sarcastic, witty, and full of puns.
*   **Aggressive**: Blunt, no-nonsense, and direct.
*   **Motivational**: Inspiring, grit-focused, and encouraging.
*   **Sports**: Fanatic energy with constant sports analogies.

### 🧠 Innovation Upgrades
*   **AI Mood Detection**: Automatically analyzes your sentiment and suggests switching to the most appropriate persona.
*   **Voice Experience**: 
    *   **Speech-to-Text (STT)**: Use the microphone button to speak your heart out.
    *   **Text-to-Speech (TTS)**: Listen to Buddy AI talk back with mood-specific pitch and speed tuning.
*   **Dynamic Morphing UI**: A premium glassmorphic interface that physically "morphs" and transitions colors based on the chat's intensity and mood.
*   **Smart Conversation Digest**: Automated summaries every 6 messages to keep the conversation's context clear and grounded.

---

## 🛠 Tech Stack

*   **Frontend**: React (Vite), Vanilla CSS (Glassmorphism), Lucide-React.
*   **Backend**: Python (FastAPI), SQLModel (SQLite), Pydantic.
*   **AI**: Google Gemini 2.5 Flash API.
*   **APIs**: Browser Web Speech API (STT/TTS).

---

## 📦 Installation & Setup

### Prerequisites
*   Python 3.10+
*   Node.js (v18+)
*   Gemini API Key ([Get one here](https://aistudio.google.com/))

### 1. Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```
**Configure Environment**:
Create/Edit `.env` in the `backend/` folder:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

**Run Backend**:
```bash
uvicorn main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🎨 UI & Design
The project features a **Premium Glassmorphic Design System** with:
*   Dynamic CSS radial gradients that shift positions (`--x1`, `--y1` etc.).
*   Smooth backdrop blur effects and SVG-inspired transitions.
*   Pulse and morph animations triggered by chat activity.

---

## 📝 License
This project is open-source and free to use for personal experiments. Enjoy chatting with Buddy!
