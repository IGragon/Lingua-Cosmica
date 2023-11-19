from flask import Flask, render_template, request, send_file, jsonify
from pytube import YouTube

app = Flask(__name__)

# youtube_video_url = 'https://www.youtube.com/watch?v=aQ0w2I0Eb9I'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    video_link = request.form['videoLink']
    
    from_language = request.form["fromLanguageSelect"]
    to_language = request.form["toLanguageSelect"]

    print (from_language)

    # download
    yt = YouTube(video_link)
    video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first().download(output_path='static/', filename=f'video_{from_language}_to_{to_language}.mp4')
    video_path = f'static/video_{from_language}_to_{to_language}.mp4'

    # Return JSON response with video_path and video_url
    return jsonify({'video_path': video_path, 'video_url': '/download?video_path=' + video_path})


@app.route('/download')
def download():
    video_path = request.args.get('video_path', '')
    return send_file(video_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
