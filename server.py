import os
import base64
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder=".")
CORS(app)

API_KEY = os.getenv("GOOGLE_API_KEY")

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if not API_KEY:
        return jsonify({"response": "Gemini APIキーが未設定です"})

    text = None

    if "audio" in request.files:
        audio = request.files["audio"]
        audio_base64 = base64.b64encode(audio.read()).decode("utf-8")
        text = "音声入力されました。"  # Whisperが無い前提の仮テキスト
    elif request.is_json:
        json_data = request.get_json()
        text = json_data.get("text", "")
    else:
        return jsonify({"response": "無効な入力です"}), 400

    payload = {
        "contents": [{"parts": [{"text": text}]}]
    }

    try:
        res = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            },
            params={"key": API_KEY},
            json=payload
        )
        result = res.json()
        message = result["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"response": message})
    except Exception as e:
        return jsonify({"response": "エラーが発生しました"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))