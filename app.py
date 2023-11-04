from flask import Flask, render_template, request
from pytube import YouTube

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_video', methods=['POST'])
def process_video():
    video_link = request.form['videoLink']

    # код для обработки ссылки и скачивания видео
    # Затычка
    yt = YouTube(video_link)
    yt.streams.filter(progressive=True, file_extension='mp4').first().download()

    # видос
    return 'static/video.mp4'


if __name__ == '__main__':
    app.run(debug=True)
