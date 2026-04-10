import logging
from openai import AsyncOpenAI
from bot.core.config import settings
from bot.openai.prompts import SYSTEM_PROMPT, PROMPT_CACHE_KEY

logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=settings.openai_api_key)

IMAGE_TOOL = {
  "type": "image_generation",
  "partial_images": 0,
  "output_format": "base64",
  "quality": "auto",
  "size": "auto",
}

async def get_response(user_message: str) -> dict:
  logger.debug("Sending message to OpenAI: %s", user_message)

  response = await client.responses.create(
    model=settings.openai_model,
    service_tier="flex",
    instructions=SYSTEM_PROMPT,
    input=user_message,
    tools=[IMAGE_TOOL],
    store=True,
    metadata={
      "prompt_cache_key": PROMPT_CACHE_KEY,
      "prompt_cache_retention": "24h",
    },
  )

  result = {"text": None, "image_b64": None}

  for item in response.output:
    if item.type == "message":
      for block in item.content:
        if block.type == "output_text":
          result["text"] = block.text

    elif item.type == "image_generation_call":
      result["image_b64"] = item.result

  logger.debug("OpenAI response parsed: text=%s image=%s",
    bool(result["text"]),
    bool(result["image_b64"]),
  )

  return result
