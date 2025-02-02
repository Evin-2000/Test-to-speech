##import tempfile
##from gtts import gTTS
##
##def do_tts(text):
##    tts = gTTS(text)
##    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
##        tts.save(temp_file.name)
##        return temp_file.name
##
##text = input("please write the text:")
##file_path = do_tts(text)
##print(f"TTS file saved at: {file_path}")

from flask import Flask, request, jsonify, render_template_string
from gtts import gTTS
import os
import tempfile

app = Flask(__name__)

# Function to generate TTS and save it in memory
def do_tts(text):
    tts = gTTS(text)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name

@app.route('/')
def home():
    return render_template_string(open('C:/Users/Raja/Documents/python/project/projects/intex.html').read())

@app.route('/process-text', methods=['POST'])
def process_text():
    text = request.form.get('text', '')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    try:
        file_path = do_tts(text)
        audio_filename = os.path.basename(file_path)
        audio_url = f"/static/{audio_filename}"

        # Move the file to static folder
        if not os.path.exists('static'):
            os.mkdir('static')
        os.rename(file_path, os.path.join('static', audio_filename))

        return jsonify({"audio_url": audio_url})  # Send the audio URL back to the frontend

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)

