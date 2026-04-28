from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

class NewsPost(BaseModel):
  id: UUID
  reddit_id: str | None = None
  subreddit: str
  title: str
  content: str | None = None
  url: str | None = None
  ups: int | None = None
  upvote_ratio: Decimal | None = None
  posted_at: datetime | None = None
  created_at: datetime | None = None
  metadata: dict | None = None
  is_posted: bool | None = None

  class Config:
    from_attributes = True
