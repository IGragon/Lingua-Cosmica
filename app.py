from flask import Flask, render_template, request, send_file
from pytube import YouTube

app = Flask(__name__)

# youtube_video_url = 'https://www.youtube.com/watch?v=aQ0w2I0Eb9I'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    video_link = request.form['videoLink']
    
    # код для обработки ссылки и скачивания видео

    # download video
    yt = YouTube(video_link)
    video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first().download(output_path = 'static/', filename = "video.mp4")

    return send_file('static/video.mp4', as_attachment=True)

@app.route('/download')
def download():
    return send_file('static/video.mp4', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
