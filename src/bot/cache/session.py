from cache.client import get_redis

TTL = 60 * 60 * 24  # 24 hours

async def get_state(user_id: int) -> str | None:
  r = await get_redis()
  return await r.get(f"state:{user_id}")

async def set_state(user_id: int, state: str) -> None:
  r = await get_redis()
  await r.set(f"state:{user_id}", state, ex=TTL)

async def clear_state(user_id: int) -> None:
  r = await get_redis()
  await r.delete(f"state:{user_id}")
