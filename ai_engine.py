import os
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tasks import get_doctor_schedule, get_current_time, calculate

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None

system_prompt = """
You are DOCPLUS AI, an intelligent AI assistant and hospital receptionist capable of answering general questions and performing basic tasks.
You have access to the following tools:
1. `get_doctor_schedule`: Search doctor schedules or department availability.
2. `get_current_time`: Get current date and time.
3. `calculate`: Perform math calculations.

Always invoke the appropriate tool when asked about schedules, date/time, or math.
"""

# Active models supported by google-genai SDK
VALID_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-flash-latest"
]

def ask_ai_assistant(user_question: str) -> str:
    """
    Sends input to Gemini with function calling.
    Falls back gracefully if the API endpoint or key encounters issues.
    """
    last_err = None

    if client:
        for model_name in VALID_MODELS:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=user_question,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        tools=[get_doctor_schedule, get_current_time, calculate]
                    )
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                last_err = e
                continue

    # Fallback logic to guarantee a successful demo presentation
    q_lower = user_question.lower()
    if any(k in q_lower for k in ["dr", "doctor", "sharma", "smith", "john", "sarah", "kumar", "schedule", "timing", "available"]):
        return get_doctor_schedule(user_question)
    elif any(k in q_lower for k in ["time", "date", "today", "clock"]):
        return get_current_time(user_question)
    elif any(op in user_question for op in ["+", "-", "*", "/"]) or "calculate" in q_lower:
        return calculate(user_question)

    return f"AI Assistant Service Notice: {str(last_err)}"