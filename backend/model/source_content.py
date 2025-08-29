from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class SourceContent(BaseModel):
    id: Optional[str] = None
    source_url: str
    title: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class SourceContentCreateRequest(BaseModel):
    source_url: str
    title: str
    content: str


class SourceContentUpdate(BaseModel):
    source_id: str
    source_url: str
    title: str
    content: str
