from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from enum import Enum
from typing import Optional


class FeatureStatus(str, Enum):
    PENDING = "pending"
    PASS = "pass"
    WARNING = "warning"
    CRITICAL = "critical"


class Feature(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    status: FeatureStatus = FeatureStatus.PENDING
    created_at: datetime
    updated_at: Optional[datetime] = None


class FeatureCreateRequest(BaseModel):
    name: str = Field(..., description="Name of the feature")
    description: str = Field(..., description="Description of the feature")


class FeatureUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, description="Name of the feature")
    description: Optional[str] = Field(
        None, description="Description of the feature")
    status: Optional[FeatureStatus] = Field(
        None, description="Status of the feature")
