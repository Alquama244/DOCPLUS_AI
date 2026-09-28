import streamlit as st
from rule_based import get_rule_response
from ai_engine import ask_ai_assistant

st.set_page_config(page_title="DOCPLUS Assistant System", layout="centered")

st.title("DOCPLUS Assistant System")

# Navigation mode selection in sidebar
st.sidebar.title("Select Mode")
mode = st.sidebar.radio(
    "Choose Mode:",
    ("Task 1: Rule-Based Chatbot", "Task 2: Smart AI Assistant")
)

st.write(f"Current System Mode: **{mode}**")

# Session state initialization for message history
if "rule_messages" not in st.session_state:
    st.session_state.rule_messages = [
        {"role": "assistant", "content": "Welcome to Rule-Based Mode. Ask about visiting hours, emergency, location, or billing."}
    ]

if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = [
        {"role": "assistant", "content": "Welcome to Smart AI Assistant Mode. I can answer questions and perform basic tasks (calculations, schedule search, date/time)."}
    ]

# Render selected mode
if mode == "Task 1: Rule-Based Chatbot":
    for msg in st.session_state.rule_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Enter a query for the Rule-Based Bot..."):
        st.session_state.rule_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        reply = get_rule_response(prompt)
        with st.chat_message("assistant"):
            st.write(reply)
        st.session_state.rule_messages.append({"role": "assistant", "content": reply})

else:
    for msg in st.session_state.ai_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask AI Assistant anything or request a task..."):
        st.session_state.ai_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Processing request..."):
                reply = ask_ai_assistant(prompt)
                st.write(reply)
        st.session_state.ai_messages.append({"role": "assistant", "content": reply})