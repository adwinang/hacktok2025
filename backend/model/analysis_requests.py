from pydantic import BaseModel
from typing import List


class AnalyzeSourcesRequest(BaseModel):
    source_ids: List[str]


class AnalyzeFeatureRequest(BaseModel):
    feature_id: str
