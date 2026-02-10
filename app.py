from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests

# Load env
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    user_text = data.get("text", "").strip()

    if not user_text:
        return jsonify({"prompt": "Please write something"}), 400

    prompt_instruction = f"""
You are an expert prompt engineer.

Convert the following ordinary text into a perfect AI prompt.

User text:
{user_text}

The final prompt must include:
- Role
- Task
- Context
- Output format
"""

    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openai/gpt-3.5-turbo",  # You can swap to other free models
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_instruction}
            ]
        }

        response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
        result = response.json()

        # Extract text safely
        output_text = result["choices"][0]["message"]["content"]

        return jsonify({"prompt": output_text})

    except Exception as e:
        return jsonify({"prompt": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port, debug=True)
