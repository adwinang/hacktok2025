"""
Compliance analysis routes.

This module contains routes for compliance analysis.
"""

from fastapi import APIRouter, HTTPException
from model.analysis_requests import AnalyzeSourcesRequest, AnalyzeFeatureRequest

# Create router for health-related routes
compliance_router = APIRouter(prefix="/compliance", tags=["compliance"])


@compliance_router.post("/analyze-sources")
async def analyze_sources(request: AnalyzeSourcesRequest):
    """
    Basic compliance analysis endpoint.
    """
    try:
        compliance_analysis_service = compliance_router.compliance_analysis_service
        await compliance_analysis_service.analyze_sources_impact_async(
            request.source_ids)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@compliance_router.post("/analyze-feature")
async def analyze_feature(request: AnalyzeFeatureRequest):
    """
    Basic compliance analysis endpoint.
    """
    try:
        compliance_analysis_service = compliance_router.compliance_analysis_service
        await compliance_analysis_service.analyze_feature_impact_async(
            request.feature_id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
