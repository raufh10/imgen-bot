from cache.client import get_redis
from cache.models import SessionCache

_KEY = "session:current"

async def get_session() -> SessionCache | None:
  r = await get_redis()
  data = await r.get(_KEY)
  return SessionCache.model_validate_json(data) if data else None

async def set_session(session: SessionCache) -> None:
  r = await get_redis()
  await r.set(_KEY, session.model_dump_json())

async def clear_session() -> None:
  r = await get_redis()
  await r.delete(_KEY)
