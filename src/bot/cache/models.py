from uuid import UUID

from pydantic import BaseModel

from db.models import NewsPost

class Slide(BaseModel):
  original: NewsPost
  slide_prompt: str
  slide_path: str

class SessionCache(BaseModel):
  id: UUID
  post_draft: str
  slides: list[Slide]
