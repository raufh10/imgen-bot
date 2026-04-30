from datetime import date
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from db.models import NewsPost
from llm.models import Draft

class NewsItem(BaseModel):
  id: UUID = Field(default_factory=uuid4)
  original: NewsPost
  draft: str = ""
  image_path: str | None = None
  image_urn: str | None = None
  drafts: list[Draft] = Field(default_factory=list)

class SessionCache(BaseModel):
  date: date
  person_urn: str
  token: str
  news: list[NewsItem]
