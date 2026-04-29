from datetime import date
from cache.client import get_redis
from cache.models import SessionCache

async def get_session(session_date: date) -> SessionCache | None:
  r = await get_redis()
  data = await r.get(f"session:{session_date.isoformat()}")
  return SessionCache.model_validate_json(data) if data else None

async def set_session(session: SessionCache) -> None:
  r = await get_redis()
  await r.set(f"session:{session.date.isoformat()}", session.model_dump_json())

async def clear_session(session_date: date) -> None:
  r = await get_redis()
  await r.delete(f"session:{session_date.isoformat()}")
