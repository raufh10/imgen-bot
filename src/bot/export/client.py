import httpx

from core.config import settings

LINKEDIN_API = "https://api.linkedin.com/v2"
AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
SCOPES = "w_member_social r_liteprofile"

def get_oauth_url(redirect_uri: str, state: str) -> str:
  return (
    f"{AUTH_URL}"
    f"?response_type=code"
    f"&client_id={settings.LINKEDIN_CLIENT_ID}"
    f"&redirect_uri={redirect_uri}"
    f"&state={state}"
    f"&scope={SCOPES}"
  )

async def exchange_code_for_token(code: str, redirect_uri: str) -> dict:
  async with httpx.AsyncClient() as client:
    r = await client.post(
      TOKEN_URL,
      data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "client_secret": settings.LINKEDIN_CLIENT_SECRET,
      },
    )
    r.raise_for_status()
    return r.json()  # contains access_token, expires_in

async def get_person_urn(token: str) -> str:
  async with httpx.AsyncClient() as client:
    r = await client.get(
      f"{LINKEDIN_API}/me",
      headers={
        "Authorization": f"Bearer {token}",
        "X-Restli-Protocol-Version": "2.0.0",
      },
    )
    r.raise_for_status()
    person_id = r.json()["id"]
    return f"urn:li:person:{person_id}"
