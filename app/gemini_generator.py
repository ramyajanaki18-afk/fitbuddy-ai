import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def generate_workout_gemini(name: str, age: int, weight: float, goal: str, intensity: str, feedback: str = None):
    # Updated to gemini-3.8-flash
    model = genai.GenerativeModel('models/gemini-3.8-flash')
    
    prompt = f"""
    Create a personalized 7-day workout plan for a user with the following details:
    - Name: {name}
    - Age: {age}
    - Weight: {weight} kg
    - Fitness Goal: {goal}
    - Workout Intensity: {intensity}
    """
    
    if feedback:
        prompt += f"\n- Additional User Feedback for adjustment: {feedback}"
        
    prompt += "\nPlease format the output clearly with days, exercises, sets, and reps."

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating workout plan: {str(e)}"