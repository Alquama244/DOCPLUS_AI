from flask import Flask, render_template, request, jsonify
from ai_engine import ask_docplus

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"reply": "Please type a question."})
    reply = ask_docplus(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
