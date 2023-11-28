import os
import torch
from loguru import logger
import nltk
nltk.download('punkt')

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {DEVICE}")

ASR_MODEL = "small"

DEBUG = True

VIDEO_STORAGE_PATH = "./data/videos"
# AUDIO_STORAGE_PATH = "./data/audios"
os.makedirs(VIDEO_STORAGE_PATH, exist_ok=True)
# os.makedirs(AUDIO_STORAGE_PATH, exist_ok=True)

MAX_RESOLUTION = 720

supported_languages = ["eng", "spa", "rus"]
full_languages = {
    "eng": "english",
    "spa": "spanish",
    "rus": "russian",
}

AUDIO_CHUNK_SIZE = 10  # in seconds

logger.info("Config loaded")
