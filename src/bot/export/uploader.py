import httpx
from export.client import LINKEDIN_API

def _headers(token: str) -> dict:
  return {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0",
  }

async def register_image_upload(token: str, person_urn: str) -> tuple[str, str]:
  """Returns (upload_url, asset_urn)"""
  async with httpx.AsyncClient() as client:
    r = await client.post(
      f"{LINKEDIN_API}/assets?action=registerUpload",
      headers=_headers(token),
      json={
        "registerUploadRequest": {
          "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
          "owner": person_urn,
          "serviceRelationships": [
            {
              "relationshipType": "OWNER",
              "identifier": "urn:li:userGeneratedContent",
            }
          ],
        }
      },
    )
    r.raise_for_status()
    data = r.json()
    upload_url = data["value"]["uploadMechanism"][
      "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
    ]["uploadUrl"]
    asset_urn = data["value"]["asset"]
    return upload_url, asset_urn

async def upload_image(upload_url: str, token: str, image_path: str) -> None:
  with open(image_path, "rb") as f:
    image_bytes = f.read()
  async with httpx.AsyncClient() as client:
    r = await client.post(
      upload_url,
      headers={"Authorization": f"Bearer {token}"},
      content=image_bytes,
    )
    r.raise_for_status()
