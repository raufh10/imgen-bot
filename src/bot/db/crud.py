from uuid import UUID

from db.client import get_pool
from db.models import NewsPost

async def get_unposted() -> list[NewsPost]:
  pool = await get_pool()
  rows = await pool.fetch(
    """
    SELECT id, subreddit, title, content, url, ups, upvote_ratio, posted_at
    FROM news_posts
    WHERE is_posted = FALSE
    ORDER BY created_at ASC
    """
  )
  return [NewsPost(**dict(row)) for row in rows]

async def mark_as_posted(post_id: UUID) -> NewsPost | None:
  pool = await get_pool()
  row = await pool.fetchrow(
    """
    UPDATE news_posts
    SET is_posted = TRUE, posted_at = NOW()
    WHERE id = $1
    RETURNING *
    """,
    post_id,
  )
  return NewsPost(**dict(row)) if row else None
