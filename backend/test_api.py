import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print(f"Testing with API Key: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

if not api_key:
    print("No API Key found!")
    exit(1)

genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content("Hello, respond with 'success'.")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
