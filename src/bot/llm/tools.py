from agents import ImageGenerationTool
from core.config import settings

IMAGE_GEN_TOOL = ImageGenerationTool(
  tool_config={
    "type": "image_generation",
    "partial_images": 0,
    "output_format": "png",
    "quality": "low",
    "size": "1536x1024",
    "model": settings.image_model,
  }
)

def save_image_locally(b64_data: str, filename: str = "output.png") -> str:
  import base64
  with open(filename, "wb") as f:
    f.write(base64.b64decode(b64_data))
  return f"Image saved as {filename}"
