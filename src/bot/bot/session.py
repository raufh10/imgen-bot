from uuid import uuid4

from cache.models import NewsItem, SessionCache
from cache.temp import clear_session, get_session, set_session
from db.crud import get_unposted
from export.client import get_person_urn, get_token

async def init_session() -> SessionCache:
  existing = await get_session()
  if existing:
    return existing

  posts = await get_unposted()
  news = [
    NewsItem(
      id=uuid4(),
      original=post,
      draft="",
    )
    for post in posts
  ]

  session = SessionCache(
    person_urn=get_person_urn(),
    token=get_token(),
    news=news,
  )
  await set_session(session)
  return session

async def save_session(session: SessionCache) -> None:
  await set_session(session)
