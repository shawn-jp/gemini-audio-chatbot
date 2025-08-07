from flask import Flask, request, jsonify
import os
import base64
import tempfile
import requests

app = Flask(__name__)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    audio = request.files["audio"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
        audio.save(temp_audio.name)

        with open(temp_audio.name, "rb") as f:
            audio_data = f.read()

        audio_base64 = base64.b64encode(audio_data).decode("utf-8")

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"inline_data": {
            "mime_type": "audio/webm",
            "data": audio_base64
        }}]}],
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
    res = requests.post(url, json=payload, headers=headers)

    if res.status_code == 200:
        reply = res.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        reply = f"エラー: {res.status_code}"

    return jsonify({"reply": reply})