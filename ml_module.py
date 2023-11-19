import numpy as np

from config import logger, DEBUG, DEVICE, supported_languages, AUDIO_CHUNK_SIZE, ASR_MODEL, whisper_languages
from utils import download_video, extract_audio_signal_and_sampling_rate, merge_new_audio

from transformers import pipeline
from transformers import VitsModel, AutoTokenizer
import torch
import soundfile as sf


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
        with torch.no_grad():
            output = self.models[language](**inputs).waveform.float().numpy()[0]

        return output


class VideoTranslator:
    def __init__(self):
        self.stt_pipeline = pipeline("automatic-speech-recognition", model=ASR_MODEL, device=DEVICE)
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
            audio_array = audio_array[:30 * sampling_rate]

        audio_parts = []
        for i in range(0, (len(audio_array) // sampling_rate + AUDIO_CHUNK_SIZE - 1) // AUDIO_CHUNK_SIZE):
            start = i * AUDIO_CHUNK_SIZE * sampling_rate
            end = start + AUDIO_CHUNK_SIZE * sampling_rate
            audio_parts.append(audio_array[start:end])

        texts = []
        for audio_part in audio_parts:
            text = self.apply_stt(audio_part, sampling_rate, language)
            texts.append(text)
            logger.info(f"Processed audio part {len(texts)} / {len(audio_parts)}")

        output_audio_path = video_path.replace("video_", "translated_").replace(".mp4", ".wav")

        synthesized_audios = []
        for i, (text, audio_part) in enumerate(zip(texts, audio_parts)):
            synthesized_audio = self.audio_synthesizer.synthesize(text, language)
            synthesized_audios.append(synthesized_audio)
            logger.info(f"Synthesized audio {len(synthesized_audios)} / {len(texts)}")

        output_sampling_rate = self.audio_synthesizer.models[language].config.sampling_rate
        audio = np.concatenate(synthesized_audios)
        sf.write(output_audio_path, audio, output_sampling_rate)
        new_video_path, success = merge_new_audio(video_path, output_audio_path)
        logger.info("Finished processing video")
        return new_video_path, success

    def apply_stt(self, audio_array, sampling_rate, language):
        audio = {"array": audio_array, "sampling_rate": sampling_rate}
        outputs = self.stt_pipeline(audio,
                                    max_new_tokens=256,
                                    generate_kwargs={"task": "transcribe", "language": whisper_languages[language]})
        return outputs["text"]

