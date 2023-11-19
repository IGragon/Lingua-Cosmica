from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

from config import logger, VIDEO_STORAGE_PATH, AUDIO_STORAGE_PATH
from pytube import YouTube

from moviepy.editor import VideoFileClip
import numpy as np
import hashlib
import time


def encode_string(string: str):
    return hashlib.sha1(string.encode('utf-8')).hexdigest()


def download_video(youtube_video_url):
    # Create a YouTube object for the given video URL
    yt = YouTube(youtube_video_url)
    filename = encode_string(youtube_video_url + str(time.time())) + ".mp4"

    # Get the stream with 720p resolution (video and audio combined)
    stream = yt.streams.filter(res="720p").first()
    if stream is None:
        stream = yt.streams.get_highest_resolution()

    # Download the 720p video and audio to the specified output path
    video_file = stream.download(VIDEO_STORAGE_PATH, filename=filename, filename_prefix="video_")
    return video_file


def convert_audio_to_mono(audio_array):
    return audio_array.mean(axis=1)


def extract_audio_signal_and_sampling_rate(file_path):
    # Load the video file
    video_clip = VideoFileClip(file_path)

    # Extract the audio as a NumPy array
    audio_array = video_clip.audio.to_soundarray()
    if audio_array.shape[1] > 1:
        audio_array = convert_audio_to_mono(audio_array)

    # Get the sampling rate
    sampling_rate = audio_array.shape[0] / video_clip.duration

    return audio_array, int(sampling_rate)


def merge_new_audio(video_path, audio_path):
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        new_audioclip = CompositeAudioClip([audio_clip])

        video_clip.audio = new_audioclip
        new_video_path = video_path.replace(".mp4", "_translated.mp4")
        video_clip.write_videofile(new_video_path)
        return new_video_path, True
    except Exception as e:
        logger.error(f"Error merging new audio to {video_path=}: {e}")
        return None, False
