from flask import Flask, render_template, request
from config import ML_SERVICE_ADDRESS, logger
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_video', methods=['POST'])
def process_video():
    video_link = request.form['videoLink']

    # код для обработки ссылки и скачивания видео
    data = {"youtube_url": video_link}
    response = requests.request("get", ML_SERVICE_ADDRESS, data=data)
    return_data = response.json()
    logger.info(return_data)
    # видос
    return 'static/video.mp4'


if __name__ == '__main__':
    app.run(debug=True)
