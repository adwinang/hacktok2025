from typing import List, Optional
from pydantic import BaseModel, HttpUrl
from datetime import datetime


class Source(BaseModel):
    id: Optional[str] = None
    source_url: str
    tags: Optional[List[str]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class SourceCreateRequest(BaseModel):
    source_url: HttpUrl
    tags: Optional[List[str]] = None


class SourceUpdateRequest(BaseModel):
    tags: Optional[List[str]] = None


class SourceIdsRequest(BaseModel):
    source_ids: List[str]
