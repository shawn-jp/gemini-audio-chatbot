
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
import requests

app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if not GOOGLE_API_KEY:
        return jsonify({"error": "Gemini APIキーが設定されていません。"}), 500

    audio_data = request.files["audio_data"].read()
    audio_base64 = base64.b64encode(audio_data).decode("utf-8")

    body = {
        "contents": [{
            "role": "user",
            "parts": [{
                "inline_data": {
                    "mime_type": "audio/webm",
                    "data": audio_base64
                }
            }]
        }]
    }

    headers = {"Content-Type": "application/json"}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GOOGLE_API_KEY}"
    res = requests.post(url, headers=headers, json=body)

    if res.ok:
        try:
            text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"text": text})
        except Exception as e:
            return jsonify({"error": "Geminiの応答の解析に失敗しました。"}), 500
    else:
        return jsonify({"error": "Gemini APIの呼び出しに失敗しました。"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
