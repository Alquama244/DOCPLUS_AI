import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tasks import get_doctor_schedule, get_current_time, calculate

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

system_prompt = """
You are DOCPLUS AI, an intelligent AI assistant and hospital receptionist capable of
answering general and medical questions and performing basic tasks.

You have access to these tools:
1. get_doctor_schedule - search doctor schedules or department availability.
2. get_current_time - get the current date and time.
3. calculate - perform a math calculation.

Use a tool whenever the question matches what it does. For medical questions,
give clear, useful information, then remind the user that a doctor should
confirm any diagnosis or treatment. Keep answers well organised and not too long.
"""

# models to try, in order. all confirmed available for this key
MODELS = [
    "gemini-3.5-flash-lite",
    # "gemini-3.1-flash-lite",
    # "gemini-3.8-flash",
    # "gemini-3.7-flash",
]

TOOLS = [get_doctor_schedule, get_current_time, calculate]


def ask_ai_assistant(user_question: str) -> str:
    """
    Sends the question to Gemini, with tool calling enabled, and returns the reply.
    Tries each model in order until one succeeds.
    """
    if not client:
        return "AI Assistant is not configured. Please add GEMINI_API_KEY to the .env file."

    last_error = None

    for model_name in MODELS:
        try:
            chat = client.chats.create(
                model=model_name,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=TOOLS,
                ),
            )
            response = chat.send_message(user_question)
            if response and response.text:
                return response.text
        except Exception as e:
            last_error = e
            print(model_name, "failed:", str(e)[:150])
            continue

    return ("The AI service is busy right now, please try again in a few seconds. "
            f"(Details: {last_error})")


if __name__ == "__main__":
    q = input("Ask DOCPLUS: ")
    print(ask_ai_assistant(q))