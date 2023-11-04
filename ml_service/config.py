import torch
from loguru import logger

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {DEVICE}")

DEBUG = True

VIDEO_STORAGE_PATH = "./data/videos"
AUDIO_STORAGE_PATH = "./data/audios"

MAX_RESOLUTION = 720

logger.info("Config loaded")
