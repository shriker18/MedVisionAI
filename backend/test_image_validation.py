from app.services.image_validation import validate_image


with open("/Users/sagarvarma/Downloads/WhatsApp Image 2025-11-06 at 14.42.47.jpeg", "rb") as file:
    image_bytes = file.read()


result = validate_image(image_bytes)

print(result)