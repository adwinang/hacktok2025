from typing import List
from agents.compliance_analyzer_agent import ComplianceAnalyzerAgent
from services.source_service import SourceService
from services.source_content_service import SourceContentService
from services.feature_service import FeatureService


class ComplianceAnalysisService:
    def __init__(self, source_service: SourceService, source_content_service: SourceContentService, feature_service: FeatureService, compliance_analyzer_agent: ComplianceAnalyzerAgent):
        self.source_service = source_service
        self.source_content_service = source_content_service
        self.feature_service = feature_service
        self.compliance_analyzer_agent = compliance_analyzer_agent

    # Priority 1
    async def analyze_sources_impact_async(self, source_ids: List[str]):
        # TODO: Implement
        pass

    # Priority 2
    async def analyze_feature_impact_async(self, feature_id: str):
        # TODO: Implement
        pass
