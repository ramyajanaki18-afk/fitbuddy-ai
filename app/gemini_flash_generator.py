import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_nutrition_tip_with_flash(goal: str) -> str:
    # Updated to gemini-3.8-flash
    model = genai.GenerativeModel("models/gemini-3.8-flash")
    prompt = f"Provide a concise, practical nutrition or recovery tip tailored for someone whose fitness goal is '{goal}'. Keep it short and actionable."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Nutrition tip unavailable: {str(e)}"
    