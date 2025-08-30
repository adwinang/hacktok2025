from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from model.audit_report import AuditReportCreateRequest

audit_report_router = APIRouter(prefix="/audit-report", tags=["audit-report"])


@audit_report_router.get("/")
async def get_audit_reports():
    """
    Get all audit reports.
    """
    try:
        audit_report_service = audit_report_router.audit_report_service
        audit_reports = await audit_report_service.get_audit_reports_async()
        return {"success": True, "audit_reports": audit_reports}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@audit_report_router.get("/stream")
async def stream_audit_reports():
    """
    Stream audit reports in real-time using Server-Sent Events (SSE).

    This endpoint:
    1. First sends all existing audit reports as initial data
    2. Then streams real-time updates as new audit reports are added

    The response format follows SSE standards with proper headers.
    """
    try:
        audit_report_service = audit_report_router.audit_report_service

        async def generate_sse_stream():
            async for sse_message in audit_report_service.stream_audit_reports_async():
                yield sse_message

        return StreamingResponse(
            generate_sse_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS, HEAD",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Max-Age": "3600",
            },
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to stream audit reports: {str(e)}"
        )


@audit_report_router.get("/feature/{feature_id}/pending")
async def get_pending_audit_report_for_feature(feature_id: str):
    """
    Get pending audit report for a feature.
    """
    try:
        audit_report_service = audit_report_router.audit_report_service
        audit_report = (
            await audit_report_service.get_pending_audit_report_for_feature_async(
                feature_id
            )
        )
        return {"success": True, "audit_report": audit_report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@audit_report_router.get("/source/{source_id}")
async def get_audit_reports_by_source(source_id: str):
    """
    Get all audit reports associated with a specific source.

    Matches audit reports where the given source_id exists in the source_ids array.
    """
    try:
        audit_report_service = audit_report_router.audit_report_service
        audit_reports = await audit_report_service.get_audit_reports_by_source_async(
            source_id
        )
        return {"success": True, "audit_reports": audit_reports}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@audit_report_router.get("/{audit_report_id}")
async def get_audit_report(audit_report_id: str):
    """
    Get all audit reports.
    """
    try:
        audit_report_service = audit_report_router.audit_report_service
        audit_report = await audit_report_service.get_audit_report_async(
            audit_report_id
        )
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
        await compliance_action_service.execute_audit_report_action_async(
            audit_report_id
        )
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


@audit_report_router.post("/{audit_report_id}/verify")
async def verify_audit_report(audit_report_id: str):
    """
    Verify an audit report.
    """
    try:
        compliance_action_service = audit_report_router.compliance_action_service
        await compliance_action_service.verify_audit_report_async(audit_report_id)
        return {"success": True, "message": "Audit report verified successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
