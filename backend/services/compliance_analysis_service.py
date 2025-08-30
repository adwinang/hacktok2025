from typing import List
from agents.compliance_analyzer_agent import ComplianceAnalyzerAgent
from services.source_service import SourceService
from services.source_content_service import SourceContentService
from services.feature_service import FeatureService
from services.audit_report_service import AuditReportService
from services.compliance_action_service import ComplianceActionService
from model.audit_report import AuditReportCreateRequest


class ComplianceAnalysisService:
    def __init__(self, source_service: SourceService, source_content_service: SourceContentService, feature_service: FeatureService, audit_report_service: AuditReportService, compliance_action_service: ComplianceActionService, compliance_analyzer_agent: ComplianceAnalyzerAgent):
        self.source_service = source_service
        self.source_content_service = source_content_service
        self.feature_service = feature_service
        self.audit_report_service = audit_report_service
        self.compliance_action_service = compliance_action_service
        self.compliance_analyzer_agent = compliance_analyzer_agent

    # Priority 1
    async def analyze_sources_impact_async(self, source_ids: List[str]):
        # Retrieve the source content
        sources = await self.source_service.get_sources_via_ids_async(source_ids)

        source_urls = [source.source_url for source in sources]

        source_contents = await self.source_content_service.get_source_content_by_source_urls_async(source_urls)

        # TODO: Refactor this later
        related_features = await self.feature_service.get_features_by_tags_async(sources[0].tags)

        # Truncate related_features to a maximum of 5
        # NOTE: Truncating to avoid rate limiting error from LLM API
        truncated_features = related_features[:5]
        agent_response = await self.compliance_analyzer_agent.analyze_compliance(source_contents, truncated_features)

        # Create audit reports for each compliance analysis response
        audit_report_ids = []
        for i, response in enumerate(agent_response):
            # Get corresponding feature (assumes responses map to features by index)
            corresponding_feature = related_features[i]

            # Create AuditReportCreateRequest
            audit_report_request = AuditReportCreateRequest(
                feature_id=corresponding_feature.id,
                source_ids=source_ids,
                needs_action=response.needs_action,
                original_status=response.original_status,
                status_change_to=response.status_change_to,
                reason=response.reason,
                confidence=response.confidence
            )

            # Create audit report via service
            audit_report_id = await self.audit_report_service.create_audit_report_async(audit_report_request)
            await self.compliance_action_service.execute_audit_report_action_async(audit_report_id)
            audit_report_ids.append(audit_report_id)

        return audit_report_ids

    # Priority 2
    async def analyze_feature_impact_async(self, feature_id: str):
        # TODO: Implement
        pass
