import os

from dotenv import load_dotenv

load_dotenv()


MODEL_ID = os.getenv(
    "MODEL_ID",
    "google/medgemma-1.5-4b-it"
)

MAX_FILE_SIZE_MB = int(
    os.getenv("MAX_FILE_SIZE_MB", "10")
)

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

DEVICE = os.getenv("DEVICE", "cpu")