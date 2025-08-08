import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    audio = request.files.get("audio")
    if not audio:
        return jsonify({"error": "No audio file"}), 400

    text = "[音声認識未実装]"

    response = gemini_response(text)
    return jsonify({"text": response})

@app.route("/textquery", methods=["POST"])
def textquery():
    data = request.get_json()
    user_input = data.get("text", "")
    if not user_input:
        return jsonify({"error": "No text provided"}), 400

    response = gemini_response(user_input)
    return jsonify({"text": response})

def gemini_response(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": GEMINI_API_KEY
    }
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        res = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload)
        res.raise_for_status()
        candidates = res.json().get("candidates", [])
        return candidates[0]["content"]["parts"][0]["text"] if candidates else "回答が見つかりませんでした。"
    except Exception as e:
        return f"エラーが発生しました: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)