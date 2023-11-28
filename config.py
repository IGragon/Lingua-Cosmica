import os
import torch
from loguru import logger
import nltk
nltk.download('punkt')

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {DEVICE}")

ASR_MODEL = "medium"
if ASR_MODEL == "large":
    DEVICE = "cpu"

DEBUG = False

VIDEO_STORAGE_PATH = "./data/videos"
os.makedirs(VIDEO_STORAGE_PATH, exist_ok=True)

MAX_RESOLUTION = 720

supported_languages = ["eng", "spa", "rus"]
full_languages = {
    "eng": "english",
    "spa": "spanish",
    "rus": "russian",
}


USE_WANDB = False

if USE_WANDB:
    try:
        import wandb
        from dotenv import load_dotenv
        load_dotenv()
        WANDB_KEY = os.getenv("WANDB_KEY")
        wandb.login(key=WANDB_KEY)
        wandb.init(
            # set the wandb project where this run will be logged
            project="LinguaCosmica",
            config={
                "whisper_model": ASR_MODEL,
                "device": DEVICE,
            }
        )
        logger.info("W&B monitoring successfully initialized")
    except BaseException as e:
        USE_WANDB = False
        logger.warning(f"Could not initialize W&B: {str(e)}")

logger.info("Config loaded")
