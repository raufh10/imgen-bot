from cache.models import SessionCache
from export.client import get_person_urn
from export.uploader import register_image_upload, upload_image
from export.poster import publish_post

async def export_to_linkedin(
  session: SessionCache,
  token: str,
  image_path: str | None = None,
) -> str:
  """
  Main entry point.
  - token: OAuth2 access token obtained via get_oauth_url -> exchange_code_for_token
  - image_path: optional path to image file to attach
  Returns post URN.
  """
  person_urn = await get_person_urn(token)

  asset_urn: str | None = None
  if image_path:
    upload_url, asset_urn = await register_image_upload(token, person_urn)
    await upload_image(upload_url, token, image_path)

  return await publish_post(
    token=token,
    person_urn=person_urn,
    text=session.post_draft,
    asset_urn=asset_urn,
  )
