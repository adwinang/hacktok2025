from enum import Enum
from pydantic import BaseModel
from model.feature import FeatureStatus
from datetime import datetime
from typing import List, Optional


class AuditReportStatus(str, Enum):
    PENDING = "pending"
    DISMISSED = "dismissed"
    VERIFIED = "verified"


class AuditReport(BaseModel):
    id: Optional[str] = None
    feature_id: str
    source_ids: List[str]
    needs_action: bool
    original_status: FeatureStatus
    status_change_to: FeatureStatus
    reason: str
    confidence: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    status: AuditReportStatus = AuditReportStatus.PENDING


class AuditReportCreateRequest(BaseModel):
    feature_id: str
    source_ids: List[str]
    needs_action: bool
    original_status: FeatureStatus
    status_change_to: FeatureStatus
    reason: str
    confidence: float


class AuditReportUpdateRequest(BaseModel):
    status: Optional[AuditReportStatus] = None
    # reason: Optional[str] = None
    # confidence: Optional[float] = None
