from flask import Flask, render_template, request
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
    return_link, success = video_translator.process(video_link)
    if success:
        return 'static/video.mp4'
    else:
        logger.info("Failed to process video")
        return ...  # render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
