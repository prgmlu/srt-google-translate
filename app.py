from flask import Flask, request, send_file
import os
import subprocess
from google_translate import get_translated_srt
import pysrt

app = Flask(__name__)

# Path to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to process the MP4 file
def process_file(video_file_path, srt_file_path, language_code):
    # Translate the subtitles
    translated_srt = get_translated_srt(srt_file_path, language_code)
    translated_srt_path = os.path.join(UPLOAD_FOLDER, "translated_" + os.path.basename(srt_file_path))
    
    # Save translated subtitles to a new SRT file
    translated_srt.save(translated_srt_path, encoding='utf-8')
    
    # Use absolute paths
    abs_video_path = os.path.abspath(video_file_path)
    abs_translated_srt_path = os.path.abspath(translated_srt_path)
    
    # Create the output video with subtitles
    output_path = os.path.join(UPLOAD_FOLDER, "output_" + os.path.basename(video_file_path))
    command = [
        "ffmpeg", 
        "-i", abs_video_path, 
        "-vf", f"subtitles='{abs_translated_srt_path}'",  # Enclosing the path in quotes
        '-y',
        output_path
    ]
    subprocess.run(command)
    
    return output_path

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    srt_file = request.files.get('srt', None)
    language_code = request.form.get('language_code', 'en')  # Default to English
    
    if file.filename == '':
        return 'No selected file', 400
    if srt_file and srt_file.filename == '':
        return 'No selected SRT file', 400

    if file and (srt_file or not srt_file):
        video_file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(video_file_path)
        
        srt_file_path = None
        if srt_file:
            srt_file_path = os.path.join(UPLOAD_FOLDER, srt_file.filename)
            srt_file.save(srt_file_path)
        
        output_path = process_file(video_file_path, srt_file_path, language_code)
        return send_file(output_path, as_attachment=True, download_name="output_" + file.filename)

if __name__ == '__main__':
    app.run(debug=True)
