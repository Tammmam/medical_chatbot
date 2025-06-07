from flask import Flask, request, jsonify
from flask_cors import CORS
from mistral_runner import generate_response
from db import save_chat, get_chat_history

app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("prompt", "")
    username = data.get("username", "default_user")  # Optional username support

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Generate response from the model
    response = generate_response(prompt)

    # Save to MongoDB
    save_chat(username, prompt, response)

    return jsonify({"response": response})


@app.route("/api/history", methods=["POST"])
def history():
    data = request.get_json()
    username = data.get("username", "")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    history = get_chat_history(username)

    # Format history (hide _id and clean output)
    formatted = [
        {
            "prompt": chat.get("prompt"),
            "response": chat.get("response"),
            "timestamp": chat.get("timestamp")
        }
        for chat in history
    ]

    return jsonify({"history": formatted})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
