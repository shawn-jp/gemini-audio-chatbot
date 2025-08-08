from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import tempfile
import os
import base64
import requests

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/")
def index():
    return "Server is up and running!"

@app.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        audio_data = request.files.get("audio")
        if not audio_data:
            raise ValueError("音声データが受信されていません")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_file:
            audio_path = temp_file.name
            audio_data.save(audio_path)

        with open(audio_path, "rb") as f:
            audio_base64 = base64.b64encode(f.read()).decode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GEMINI_API_KEY}",
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": "これは音声です。文字起こししてください。"},
                        {
                            "inlineData": {
                                "mimeType": "audio/webm",
                                "data": audio_base64,
                            }
                        },
                    ]
                }
            ]
        }

        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
            headers=headers,
            json=data,
        )

        result = response.json()
        if "candidates" in result:
            output_text = result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            raise ValueError(result.get("error", {}).get("message", "Gemini APIからの応答が不正です"))

        return jsonify({"text": output_text})

    except Exception as e:
        print("エラーが発生しました:", e)
        return jsonify({"error": str(e)}), 500
