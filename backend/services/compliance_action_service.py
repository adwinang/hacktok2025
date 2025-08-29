from services.feature_service import FeatureService
from services.audit_report_service import AuditReportService
from model.feature import FeatureUpdateRequest
from model.audit_report import AuditReportUpdateRequest, AuditReportStatus


class ComplianceActionService:
    def __init__(self, feature_service: FeatureService, audit_report_service: AuditReportService):
        self.feature_service = feature_service
        self.audit_report_service = audit_report_service

    async def execute_audit_report_action_async(self, audit_report_id: str):
        try:
            # Verify the audit report is valid
            audit_report = await self.audit_report_service.get_audit_report_async(audit_report_id)

            # If the audit report has a change in status, update the feature status
            if audit_report["needs_action"]:
                # update the feature status
                feature_update_request = FeatureUpdateRequest(
                    status=audit_report["status_change_to"]
                )
                await self.feature_service.update_feature_async(audit_report["feature_id"], feature_update_request)
        except Exception as e:
            print("error", e)
            raise e

    async def dismiss_audit_report_async(self, audit_report_id: str):
        try:
            # Verify the audit report is valid
            audit_report = await self.audit_report_service.get_audit_report_async(audit_report_id)

            # Dismiss the audit report
            audit_report["status"] = AuditReportStatus.DISMISSED
            audit_report_update_request = AuditReportUpdateRequest(
                status=AuditReportStatus.DISMISSED
            )
            await self.audit_report_service.update_audit_report_async(audit_report_id, audit_report_update_request)

            # Update the feature status
            feature_update_request = FeatureUpdateRequest(
                status=audit_report["original_status"]
            )
            await self.feature_service.update_feature_async(audit_report["feature_id"], feature_update_request)
        except Exception as e:
            raise e

    async def verify_audit_report_async(self, audit_report_id: str):
        try:
            # Verify the audit report is valid
            audit_report = await self.audit_report_service.get_audit_report_async(audit_report_id)

            # Verify the audit report
            audit_report["status"] = AuditReportStatus.VERIFIED
            audit_report_update_request = AuditReportUpdateRequest(
                status=AuditReportStatus.VERIFIED
            )
            await self.audit_report_service.update_audit_report_async(audit_report_id, audit_report_update_request)

            # Update the feature status
            feature_update_request = FeatureUpdateRequest(
                status=audit_report["status_change_to"]
            )
            await self.feature_service.update_feature_async(audit_report["feature_id"], feature_update_request)
        except Exception as e:
            raise e
