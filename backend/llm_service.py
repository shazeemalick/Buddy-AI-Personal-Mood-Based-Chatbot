import os
from typing import List, Dict
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Get Gemini API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    print(f"Loading API Key (Length: {len(GEMINI_API_KEY)}, Starts with: {GEMINI_API_KEY[:5]})")
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("CRITICAL: No GEMINI_API_KEY found in environment!")

# Mood-based prompt templates
MOOD_PROMPTS = {
    "happy": "You are a very happy, cheerful, and optimistic assistant. Use emojis and be extremely positive.",
    "funny": "You are a hilarious assistant with a great sense of humor. Tell jokes, be sarcastic (in a fun way), and use witty puns.",
    "aggressive": "You are an aggressive, direct, and no-nonsense assistant. You are blunt, fast-paced, and don't mince words. (Stay professional but be firm).",
    "motivational": "You are a world-class life coach and motivational speaker. You are inspiring, encouraging, and focus on growth and grit.",
    "sports": "You are a sports fanatic! Use sports analogies, be high-energy, and talk like a commentator or an athlete.",
    "neutral": "You are a helpful and polite assistant."
}

def generate_mood_response(mood: str, user_input: str, history: List[Dict[str, str]]):
    try:
        system_prompt = MOOD_PROMPTS.get(mood, MOOD_PROMPTS["neutral"])
        formatted_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            formatted_history.append({"role": role, "parts": [msg["content"]]})
        
        model_name = "models/gemini-2.5-flash"
        model = genai.GenerativeModel(model_name=model_name, system_instruction=system_prompt)
        chat = model.start_chat(history=formatted_history)
        
        response = chat.send_message(
            user_input,
            generation_config=genai.types.GenerationConfig(max_output_tokens=500, temperature=0.8)
        )
        return response.text
    except Exception as e:
        print(f"LLM Error: {str(e)}")
        raise e

def analyze_mood(user_input: str) -> str:
    """Detects the mood of the user input and returns one of the supported moods."""
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        prompt = f"Analyze the sentiment of this text: '{user_input}'. Return exactly ONE word from this list: [happy, funny, aggressive, motivational, sports, neutral]. If unsure, return 'neutral'."
        response = model.generate_content(prompt)
        detected = response.text.strip().lower()
        # Clean up in case Gemini adds punctuation
        for mood in MOOD_PROMPTS.keys():
            if mood in detected:
                return mood
        return "neutral"
    except Exception as e:
        print(f"Mood Detection Error: {e}")
        return "neutral"

def generate_summary(history: List[Dict[str, str]]) -> str:
    """Generates a brief summary of the conversation so far."""
    try:
        if not history: return ""
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        last_msgs = [f"{m['role']}: {m['content']}" for m in history[-6:]]
        prompt = f"Summarize the essence of this conversation in one short sentence (max 15 words):\n\n" + "\n".join(last_msgs)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Summary Error: {e}")
        return ""

