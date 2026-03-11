import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

models_to_try = [
    "models/gemini-1.5-flash",
    "models/gemini-1.5-flash-latest",
    "models/gemini-pro",
    "models/gemini-1.0-pro",
    "models/gemini-2.0-flash-exp"
]

for model_name in models_to_try:
    print(f"Trying {model_name}...")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hi")
        print(f"Success with {model_name}!")
        exit(0)
    except Exception as e:
        print(f"Failed {model_name}: {e}")

print("All popular models failed. Checking list_models again...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Found available model: {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
