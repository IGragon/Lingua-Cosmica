import numpy as np

from config import logger, DEBUG, DEVICE, supported_languages, ASR_MODEL, full_languages, USE_WANDB
from utils import download_video, extract_audio_signal_and_sampling_rate, merge_new_audio

from transformers import VitsModel, AutoTokenizer
import whisper
import torch
import soundfile as sf
import librosa
from audiostretchy import stretch
from nltk import sent_tokenize

import time

if USE_WANDB:
    from config import wandb

class VoiceSynthesizer:
    def __init__(self):
        self.tokenizers = {
            lang: AutoTokenizer.from_pretrained(f"facebook/mms-tts-{lang}") for lang in supported_languages
        }

        self.models = {
            lang: VitsModel.from_pretrained(f"facebook/mms-tts-{lang}") for lang in supported_languages
        }

    def synthesize(self, text, language):
        inputs = self.tokenizers[language](text, return_tensors="pt")
        if inputs["input_ids"].shape[1] == 0:
            return None

        with torch.no_grad():
            output = self.models[language](**inputs).waveform.float().numpy()[0]

        return output


class VideoTranslator:
    def __init__(self):
        self.stt_model = whisper.load_model(ASR_MODEL, device=DEVICE)
        self.audio_synthesizer = VoiceSynthesizer()

    def process(self, youtube_video_url, language) -> (str, bool):
        try:
            video_path = download_video(youtube_video_url)
            logger.info("Downloaded video")
        except Exception as e:
            logger.error(f"Error downloading video: {type(e).__name__} {e}")
            return "", False

        try:
            audio_array, sampling_rate = extract_audio_signal_and_sampling_rate(video_path)
            logger.info("Extracted audio signal and sampling rate")
        except Exception as e:
            logger.error(f"Error extracting audio signal and sampling rate: {type(e).__name__} {e}")
            return "", False

        if DEBUG:
            audio_array = audio_array[:120 * sampling_rate]

        stt_start = time.time()
        texts = self.apply_stt(audio_array, sampling_rate, language)
        stt_end = time.time()
        stt_time = stt_end - stt_start

        output_audio_path = video_path.replace("video_", "translated_").replace(".mp4", ".wav")

        tts_start = time.time()
        synthesized_audios = []
        for i, text in enumerate(texts):
            synthesized_audio = self.audio_synthesizer.synthesize(text, language)
            synthesized_audios.append(synthesized_audio)
            logger.info(f"Synthesized audio {len(synthesized_audios)} / {len(texts)}")
        tts_end = time.time()
        tts_time = tts_end - tts_start

        failed_synth = len([audio for audio in synthesized_audios if audio is None])
        if failed_synth > 0:
            logger.warning(f"Failed to synthesize {failed_synth} audio part(s)")
            average_synth_len = sum(len(audio) for audio in synthesized_audios if audio is not None) / len([audio for audio in synthesized_audios if audio is not None])
            for i in range(len(synthesized_audios)):
                if synthesized_audios[i] is None:
                    synthesized_audios[i] = np.zeros((int(average_synth_len), ))

        output_sampling_rate = self.audio_synthesizer.models[language].config.sampling_rate
        audio = np.concatenate(synthesized_audios)
        sf.write(output_audio_path, audio, output_sampling_rate)

        with open(output_audio_path, "rb") as f:
            output_duration_seconds = sf.info(f).duration

        original_duration_seconds = len(audio_array) / sampling_rate
        stretch_ratio = original_duration_seconds / output_duration_seconds
        logger.info(f"Stretch ratio: {stretch_ratio}")
        stretch.stretch_audio(output_audio_path, output_audio_path,
                              ratio=stretch_ratio,
                              double_range=True)

        data, samplerate = sf.read(output_audio_path)
        data = data[: round(samplerate * original_duration_seconds)]
        sf.write(output_audio_path, data, samplerate)

        new_video_path, success = merge_new_audio(video_path, output_audio_path)
        if USE_WANDB:
            wandb.log({
                "stt_time": stt_time,
                "tts_time": tts_time,
                "failed_synth": failed_synth,
                "translated_texts": len(texts),
                "stretch_ratio": stretch_ratio
            })

        logger.info("Finished processing video")
        return new_video_path, success

    def apply_stt(self, audio_array: np.array, sampling_rate: int, language: str):
        resampled_audio = librosa.resample(audio_array, orig_sr=sampling_rate, target_sr=whisper.audio.SAMPLE_RATE)
        outputs = self.stt_model.transcribe(resampled_audio.astype(np.float32), language=full_languages[language])
        output_text = outputs["text"]
        sentence_tokens = sent_tokenize(output_text, language=full_languages[language])
        return sentence_tokens
