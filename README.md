# DOCPLUS Assistant System

A hybrid healthcare assistant built with Python and Streamlit, featuring a **Rule-Based Chatbot** and a **Smart AI Assistant** with function calling capabilities.

## Features

### Task 1: Rule-Based Chatbot
- Responds to predefined keywords using regular expressions (Regex).
- Provides instant details for visiting hours, location, emergency contacts, and billing.

### Task 2: Smart AI Assistant
- Integrated with Google Gemini API (`google-genai` SDK) with automated fallback execution.
- Executes real-time tasks using Python tool calling:
  - **Doctor Schedule Search:** Queries `hospital.db` (SQLite) for specialist availability.
  - **Arithmetic Calculations:** Evaluates user math expressions safely using Python's `ast` module.
  - **Date & Time Retrieval:** Returns current system timestamps.

---

## Setup & Running

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt