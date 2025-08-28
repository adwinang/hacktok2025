from typing import Optional
from pydantic import BaseModel, HttpUrl
from datetime import datetime


class Source(BaseModel):
    id: Optional[str] = None
    source_url: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class SourceCreateRequest(BaseModel):
    source_url: HttpUrl
