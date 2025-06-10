from PIL import Image
from io import BytesIO

def convert_to_webp(image_bytes: bytes, quality: int = 85) -> bytes:
    """Convert image bytes to WEBP format."""
    with Image.open(BytesIO(image_bytes)) as img:
        output = BytesIO()
        img.save(output, format="WEBP", quality=quality)
        return output.getvalue()

def resize_image(image_bytes: bytes, max_size: tuple[int, int] = (512, 512)) -> bytes:
    """Resize image while maintaining aspect ratio."""
    with Image.open(BytesIO(image_bytes)) as img:
        img.thumbnail(max_size)
        output = BytesIO()
        img.save(output, format="PNG")
        return output.getvalue()
