from flask import Flask, render_template, request, send_file, jsonify
from ml_module import VideoTranslator
from config import logger

video_translator = VideoTranslator()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_video', methods=['POST'])
def process_video():
    video_link = request.form['videoLink']
    
    from_language = request.form["fromLanguageSelect"]
    to_language = request.form["toLanguageSelect"]

    # код для обработки ссылки и скачивания видео
    return_link, success = video_translator.process(video_link, to_language)
    if success:
        return jsonify({'video_path': return_link, 'video_url': '/download?video_path=' + return_link})
    else:
        logger.info(f"Failed to process video: {video_link}")
        return ...  # render_template('error.html')


@app.route('/download')
def download():
    video_path = request.args.get('video_path', '')
    return send_file(video_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
