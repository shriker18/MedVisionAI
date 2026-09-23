from PIL import Image
import torch


image = Image.open("/Users/sagarvarma/Downloads/WhatsApp Image 2025-11-06 at 14.42.47.jpeg")

print("Image format:", image.format)
print("Image mode:", image.mode)
print("Image size:", image.size)

image = image.convert("RGB")

image_tensor = torch.tensor(
    list(image.getdata()),
    dtype=torch.float32
)

image_tensor = image_tensor.reshape(
    image.height,
    image.width,
    3
)

print("Tensor shape:", image_tensor.shape)
print("Tensor dtype:", image_tensor.dtype)