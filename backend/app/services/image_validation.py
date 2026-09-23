from io import BytesIO

from PIL import Image


def validate_image(
    image_bytes: bytes,
    max_file_size_mb: int,
) -> dict:

    max_size_bytes = max_file_size_mb * 1024 * 1024

    if len(image_bytes) > max_size_bytes:
        raise ValueError(
            f"Image exceeds {max_file_size_mb} MB limit."
        )

    try:
        image = Image.open(BytesIO(image_bytes))
        image.verify()

        image = Image.open(BytesIO(image_bytes))

    except Exception:
        raise ValueError(
            "Invalid or corrupted image file."
        )

    return {
        "format": image.format,
        "mode": image.mode,
        "width": image.width,
        "height": image.height,
        "size_bytes": len(image_bytes),
    }