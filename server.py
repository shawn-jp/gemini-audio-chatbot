import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64

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
        return jsonify({"response": "Gemini APIキーが設定されていません"}), 400

    audio = request.files.get("audio")
    if not audio:
        return jsonify({"response": "音声ファイルがありません"}), 400

    # ここにGemini APIを使った応答生成処理を追加する（省略）
    return jsonify({"response": "（ダミー応答）こんにちは！"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))