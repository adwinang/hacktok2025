from fastapi import APIRouter, HTTPException
from model.audit_report import AuditReportCreateRequest

audit_report_router = APIRouter(prefix="/audit-report", tags=["audit-report"])


@audit_report_router.post("/")
async def create_audit_report(request: AuditReportCreateRequest):
    """
    Create an audit report.
    """
    try:
        audit_report_service = audit_report_router.audit_report_service
        audit_report_id = await audit_report_service.create_audit_report_async(request)
        return {"success": True, "audit_report_id": audit_report_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@audit_report_router.get("/{audit_report_id}")
async def get_audit_report(audit_report_id: str):
    """
    Get all audit reports.
    """
    try:
        audit_report_service = audit_report_router.audit_report_service
        audit_report = await audit_report_service.get_audit_report_async(audit_report_id)
        return {"success": True, "audit_report": audit_report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@audit_report_router.post("/{audit_report_id}/action")
async def execute_audit_report_action(audit_report_id: str):
    """
    Execute an audit report action.
    """
    try:
        compliance_action_service = audit_report_router.compliance_action_service
        await compliance_action_service.execute_audit_report_action_async(audit_report_id)
        return {"success": True, "message": "Audit report action executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@audit_report_router.post("/{audit_report_id}/dismiss")
async def dismiss_audit_report(audit_report_id: str):
    """
    Dismiss an audit report.
    """
    try:
        compliance_action_service = audit_report_router.compliance_action_service
        await compliance_action_service.dismiss_audit_report_async(audit_report_id)
        return {"success": True, "message": "Audit report dismissed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
