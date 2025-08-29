from datetime import datetime
from model.audit_report import AuditReport, AuditReportCreateRequest, AuditReportStatus, AuditReportUpdateRequest
from repository.audit_report_repository import AuditReportRepositoryAsync


class AuditReportService:
    def __init__(self, audit_report_repository: AuditReportRepositoryAsync):
        self.audit_report_repository = audit_report_repository

    async def create_audit_report_async(self, audit_report: AuditReportCreateRequest):
        try:
            audit_report = AuditReport(
                feature_id=audit_report.feature_id,
                source_ids=audit_report.source_ids,
                needs_action=audit_report.needs_action,
                original_status=audit_report.original_status,
                status_change_to=audit_report.status_change_to,
                reason=audit_report.reason,
                confidence=audit_report.confidence,
                created_at=datetime.utcnow(),
                updated_at=None,
                status=AuditReportStatus.PENDING
            )
            audit_report_id = await self.audit_report_repository.create_audit_report_async(audit_report.model_dump())
            return audit_report_id
        except Exception as e:
            raise e

    async def get_audit_report_async(self, audit_report_id: str):
        try:
            audit_report = await self.audit_report_repository.get_audit_report_async(audit_report_id)
            return audit_report
        except Exception as e:
            raise e

    async def update_audit_report_async(self, audit_report_id: str, audit_report_update_request: AuditReportUpdateRequest):
        try:
            await self.audit_report_repository.update_audit_report_async(audit_report_id, audit_report_update_request)
        except Exception as e:
            raise e
