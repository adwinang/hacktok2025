from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from model.feature import FeatureCreateRequest, FeatureUpdateRequest


feature_router = APIRouter(prefix="/features", tags=["feature"])


@feature_router.get("/")
async def get_features():
    """
    Retrieve all features from the database.

    Returns a list of feature objects, each containing the following attributes (see /models/feature.py for details):
    - id: Unique identifier for the feature
    - name: Name of the feature
    - description: Detailed description of the feature
    - status: Current status of the feature (e.g., "pending", "pass", "warning", "critical")
    - created_at: Timestamp when the feature was created (UTC)
    - updated_at: Timestamp when the feature was last updated (UTC), or null if never updated

    Example response:
    {
        "success": true,
        "features": [
            {
                "id": "abc123",
                "name": "New Feature",
                "description": "Description of the feature",
                "status": "pending",
                "created_at": "2024-06-01T12:00:00Z",
                "updated_at": null
            },
            ...
        ]
    }
    """

    try:
        feature_service = feature_router.feature_service

        features = await feature_service.get_features_async()

        return {"success": True, "features": features}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve features: {str(e)}")


@feature_router.post("/")
async def create_feature(feature_request: FeatureCreateRequest):
    """
    Create a new feature with automatic field population.
    Only requires name and description in the request body.

    - created_at: Set to current database time (UTC)
    - updated_at: Set to null/empty
    - status: Automatically set to "pending"
    """

    try:
        feature_service = feature_router.feature_service

        feature_id = await feature_service.create_feature_async(feature_request)

        return {
            "success": True,
            "message": "Feature created successfully",
            "feature_id": feature_id
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create feature: {str(e)}")


@feature_router.put("/{feature_id}")
async def update_feature(feature_id: str, update_request: FeatureUpdateRequest):
    """
    Update a feature by ID.

    This endpoint allows updating any combination of:
    - name: Feature name
    - description: Feature description  
    - status: Feature status (pending, pass, warning, critical)

    Only provided fields will be updated. The updated_at timestamp is automatically set.
    """
    try:
        feature_service = feature_router.feature_service

        # Check if at least one field is provided for update
        if not any([
            update_request.name is not None,
            update_request.description is not None,
            update_request.status is not None
        ]):
            raise HTTPException(
                status_code=400,
                detail="At least one field (name, description, or status) must be provided for update"
            )

        success = await feature_service.update_feature_async(feature_id, update_request)

        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Feature with ID {feature_id} not found or could not be updated"
            )

        return {
            "success": True,
            "message": "Feature updated successfully",
            "feature_id": feature_id
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to update feature: {str(e)}")


@feature_router.get("/stream")
async def stream_features():
    """
    Stream features in real-time using Server-Sent Events (SSE).

    This endpoint:
    1. First sends all existing features as initial data
    2. Then streams real-time updates as features are created/updated

    The response format follows SSE standards with proper headers.
    """
    try:
        feature_service = feature_router.feature_service

        async def generate_sse_stream():
            async for sse_message in feature_service.stream_features_async():
                yield sse_message

        return StreamingResponse(
            generate_sse_stream(),
            media_type="text/event-stream",
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS, HEAD',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Max-Age': '3600'
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to stream features: {str(e)}")
