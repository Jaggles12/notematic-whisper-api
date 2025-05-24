from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import tempfile

app = Flask(__name__)
CORS(app)

model = whisper.load_model("tiny")  # Fast to load

@app.route('/')
def home():
    return "Whisper Transcriber is running."

@app.route("/asr", methods=["POST"])
def transcribe():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['audio_file']

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp_file:
        file.save(temp_file.name)
        result = model.transcribe(temp_file.name)
        return jsonify({"text": result["text"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
