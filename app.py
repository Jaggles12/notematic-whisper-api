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
