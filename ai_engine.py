from google import genai
from google.genai import types
from search import get_doctor_schedule

# 🔑 Your real Gemini API key goes here
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

#print("Current folder:", os.getcwd())
#print("API_KEY:", API_KEY)

client = genai.Client(api_key=API_KEY)

system_prompt = """
You are DOCPLUS AI, a helpful hospital receptionist. 
Answer questions politely about doctor schedules using the provided tool.
"""

def ask_docplus(user_question):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=user_question,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[get_doctor_schedule]
        )
    )
    return response.text

# --- INTERACTIVE MODE ---
if __name__ == "__main__":
    print("Welcome to DOCPLUS AI. Type 'exit' to quit.\n")
    while True:
        user_question = input("You: ")
        if user_question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        answer = ask_docplus(user_question)
        print("\nDOCPLUS AI:", answer, "\n")