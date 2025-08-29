import json
from datetime import datetime
from typing import AsyncGenerator
from model.audit_report import AuditReport, AuditReportCreateRequest, AuditReportStatus, AuditReportUpdateRequest
from repository.audit_report_repository import AuditReportRepositoryAsync


class AuditReportService:
    def __init__(self, audit_report_repository: AuditReportRepositoryAsync):
        self.audit_report_repository = audit_report_repository

    async def get_audit_reports_async(self):
        try:
            audit_reports = await self.audit_report_repository.get_audit_reports_async()
            return audit_reports
        except Exception as e:
            raise e

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
            # Convert Pydantic model to dict, excluding None values
            update_data = audit_report_update_request.model_dump(
                exclude_none=True)
            # Add updated_at timestamp
            update_data["updated_at"] = datetime.utcnow()

            await self.audit_report_repository.update_audit_report_async(audit_report_id, update_data)
        except Exception as e:
            raise e

    async def get_pending_audit_report_for_feature_async(self, feature_id: str):
        try:
            audit_report = await self.audit_report_repository.get_audit_report_for_feature_async(feature_id, AuditReportStatus.PENDING)
            return audit_report
        except Exception as e:
            raise e

    async def stream_audit_reports_async(self) -> AsyncGenerator[str, None]:
        try:
            initial_audit_reports = await self.get_audit_reports_async()

            audit_reports_data = []
            for audit_report in initial_audit_reports:
                audit_report_dict = audit_report.copy()

                if "created_at" in audit_report_dict and audit_report_dict["created_at"]:
                    audit_report_dict["created_at"] = audit_report_dict["created_at"].isoformat(
                    )
                if "updated_at" in audit_report_dict and audit_report_dict["updated_at"]:
                    audit_report_dict["updated_at"] = audit_report_dict["updated_at"].isoformat(
                    )

                audit_reports_data.append(audit_report_dict)

            initial_message = {
                "type": "initial_data",
                "data": {
                    "audit_reports": audit_reports_data
                }
            }

            yield f"data: {json.dumps(initial_message)}\n\n"
            yield f": heartbeat\n\n"

            async for change in self.audit_report_repository.stream_audit_reports():
                operation_type = change["operation_type"]

                # Determine event type based on operation
                if operation_type == "insert":
                    event_type = "audit_report_added"
                elif operation_type == "update" or operation_type == "replace":
                    event_type = "audit_report_updated"
                elif operation_type == "delete":
                    event_type = "audit_report_deleted"
                else:
                    event_type = "audit_report_changed"

                # Handle document data
                audit_report_data = None
                if change["updated_document"] is not None:
                    updated_doc = change["updated_document"].copy()

                    if "created_at" in updated_doc and updated_doc["created_at"]:
                        updated_doc["created_at"] = updated_doc["created_at"].isoformat(
                        )
                    if "updated_at" in updated_doc and updated_doc["updated_at"]:
                        updated_doc["updated_at"] = updated_doc["updated_at"].isoformat(
                        )

                    audit_report_data = updated_doc

                change_message = {
                    "type": event_type,
                    "data": {
                        "operation_type": operation_type,
                        "audit_report_id": change["audit_report_id"],
                        "audit_report_data": audit_report_data,
                        "timestamp": change["timestamp"].as_datetime().isoformat()
                    }
                }

                yield f"data: {json.dumps(change_message)}\n\n"

        except Exception as e:
            error_message = {
                "type": "error",
                "data": {
                    "message": f"Streaming error: {str(e)}"
                }
            }
            yield f"data: {json.dumps(error_message)}\n\n"
