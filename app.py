from flask import Flask, request, jsonify
from flask_cors import CORS
import whisper
import tempfile

app = Flask(__name__)
CORS(app)

# Load the Whisper model (use "tiny" for faster startup)
model = whisper.load_model("tiny")

@app.route("/asr", methods=["GET", "POST"])
def transcribe():
    if request.method == "GET":
        return '''
            <h1>Upload an Audio File</h1>
            <form method="POST" enctype="multipart/form-data">
              <input type="file" name="audio_file">
              <input type="submit" value="Transcribe">
            </form>
        '''

    if 'audio_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['audio_file']

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp_file:
        file.save(temp_file.name)
        result = model.transcribe(temp_file.name)
        return jsonify({"text": result["text"]})

@app.route('/')
def home():
    return "Whisper Transcriber is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
