from flask import Flask, render_template, request, send_file
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

    # код для обработки ссылки и скачивания видео
    return_link, success = video_translator.process(video_link, "spa")
    if success:
        return send_file(return_link, as_attachment=True)
    else:
        logger.info("Failed to process video")
        return ...  # render_template('error.html')


@app.route('/download')
def download():
    return send_file('static/video.mp4', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
