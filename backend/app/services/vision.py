from io import BytesIO
from typing import Optional

import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForImageTextToText

from app.config import MODEL_ID, DEVICE


class VisionService:

    def __init__(self):
        self.processor = None
        self.model = None
        self.device = self._select_device()

    def _select_device(self):
        if DEVICE != "auto":
            return torch.device(DEVICE)

        if torch.backends.mps.is_available():
            return torch.device("mps")

        if torch.cuda.is_available():
            return torch.device("cuda")

        return torch.device("cpu")

    def _load(self):
        # Load the model only once
        if self.model is not None:
            return

        print(f"[MedVision] Loading model: {MODEL_ID}")
        print(f"[MedVision] Device: {self.device}")

        self.processor = AutoProcessor.from_pretrained(
            MODEL_ID
        )

        self.model = AutoModelForImageTextToText.from_pretrained(
            MODEL_ID,
            torch_dtype="auto"
        )

        self.model.to(self.device)
        self.model.eval()

        print("[MedVision] Model loaded successfully.")

    def analyze(
        self,
        image_bytes: bytes,
        question: Optional[str] = None,
    ) -> str:

        # Load model when the first analysis request arrives
        self._load()

        image = Image.open(
            BytesIO(image_bytes)
        ).convert("RGB")

        question = question or (
            "Analyze this medical image conservatively. "
            "Describe the visible findings and visual characteristics. "
            "Mention uncertainty where appropriate. "
            "Do not provide a definitive diagnosis."
        )

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": image,
                    },
                    {
                        "type": "text",
                        "text": question,
                    },
                ],
            }
        ]

        inputs = self.processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        )

        inputs = {
            key: value.to(self.device)
            if hasattr(value, "to")
            else value
            for key, value in inputs.items()
        }

        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=False,
            )

        input_length = inputs["input_ids"].shape[-1]

        generated_tokens = outputs[0][input_length:]

        result = self.processor.decode(
            generated_tokens,
            skip_special_tokens=True,
        )

        return result.strip()


# One reusable instance for the application
vision_service = VisionService()