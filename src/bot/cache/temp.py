import json
from uuid import UUID

from cache.client import get_redis
from cache.models import SessionCache

async def get_session(session_id: UUID) -> SessionCache | None:
  r = await get_redis()
  data = await r.get(f"session:{session_id}")
  return SessionCache.model_validate_json(data) if data else None

async def set_session(session: SessionCache) -> None:
  r = await get_redis()
  await r.set(f"session:{session.id}", session.model_dump_json())

async def clear_session(session_id: UUID) -> None:
  r = await get_redis()
  await r.delete(f"session:{session_id}")
