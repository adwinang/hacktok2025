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
        # operation to change status from pass to critical -> will atuomatically update the frontend
        # output:
        # 1. sources it cross checked on
        # 2. status change to
        # 3. reason
        # 4. confidence

        # ComplianceAnalyzerAgent(features, sources + source content) -> AuditReoprt

        # wrapped via audit report service -> compliance action
        # compliance_action_service.execute(compliance_action)
        # compliance_action_service.dismiss(audit_report_id)

        # audit_report_action

        # once we have the audit report, add it via compliance_action_service

        # audit_report_id = await audit_report_service.create_audit_report_async(audit_report)
        # compliace_action_service.execute_audit_report_action_async(audit_report_id)

        pass

    # Priority 2
    async def analyze_feature_impact_async(self, feature_id: str):
        # TODO: Implement
        pass
