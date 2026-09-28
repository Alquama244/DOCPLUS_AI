import re

# Predefined responses for standard hospital inquiries
RULES = [
    (r"\b(hello|hi|hey|greetings)\b", "Hello! Welcome to DOCPLUS Hospital. How can I assist you today?"),
    (r"\b(visiting hours|visit time|visiting time)\b", "Visiting hours are from 10:00 AM to 12:00 PM and 4:00 PM to 7:00 PM daily."),
    (r"\b(emergency|ambulance|urgent)\b", "For emergencies, please call our 24/7 helpline at 1800-123-4567 or visit Emergency Ward Gate 2."),
    (r"\b(location|address|where are you)\b", "DOCPLUS Hospital is located at Main Road, Bistupur, Jamshedpur, Jharkhand."),
    (r"\b(billing|cost|fee|payment)\b", "For billing queries, visit the reception counter on the ground floor."),
    (r"\b(bye|goodbye|exit)\b", "Thank you for contacting DOCPLUS Hospital. Have a healthy day!")
]

def get_rule_response(user_input: str) -> str:
    text = user_input.lower().strip()
    for pattern, response in RULES:
        if re.search(pattern, text):
            return response
    return "I am a simple rule-based assistant. I can answer queries regarding visiting hours, emergency contact, location, and billing."