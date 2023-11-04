from config import logger, DEBUG, DEVICE
from utils import download_video, extract_audio_signal_and_sampling_rate, merge_new_audio

from transformers import pipeline
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import soundfile as sf


class VoiceSynthesizer:
    def __init__(self):
        self.processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        self.model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
        self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

        # load xvector containing speaker's voice characteristics from a dataset
        embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        self.speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

    def synthesize(self, text, output_path):
        input_values = self.processor(text, return_tensors="pt").input_values
        with torch.no_grad():
            audio = self.model.generate_speech(input_values,
                                               speaker_embeddings=self.speaker_embeddings,
                                               vocoder=self.vocoder)
        sf.write(output_path, audio[0].numpy(), self.processor.feature_extractor.sampling_rate)


class VideoTranslator:
    def __init__(self):
        self.stt_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-small", device=DEVICE)
        self.audio_synthesizer = VoiceSynthesizer()

    def process(self, youtube_video_url) -> (str, bool):
        video_path, audio_path = download_video(youtube_video_url)
        if video_path is None or audio_path is None:
            return "", False

        audio_array, sampling_rate = extract_audio_signal_and_sampling_rate(audio_path)
        if DEBUG:
            logger.info("Trim audio to 10 seconds")
            audio_array = audio_array[:sampling_rate * 10]  # 10 seconds

        # TODO: translate audio by portions (maybe)
        translated_text = self.apply_stt(audio_array, sampling_rate)

        output_audio_path = "translated_" + audio_path.replace(".mp4", ".wav")[6:]
        self.audio_synthesizer.synthesize(translated_text, output_audio_path)
        new_video_path, success = merge_new_audio(video_path, output_audio_path)
        return new_video_path, success

    def apply_stt(self, audio_array, sampling_rate, language="es"):
        audio = {"array": audio_array, "sampling_rate": sampling_rate}
        outputs = self.stt_pipeline(audio,
                                    max_new_tokens=256,
                                    generate_kwargs={"task": "transcribe", "language": language})
        return outputs["text"]

