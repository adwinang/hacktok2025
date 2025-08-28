from fastapi import APIRouter, HTTPException
from model.source import SourceCreateRequest


source_router = APIRouter(prefix="/sources", tags=["source"])


@source_router.get("/")
async def get_sources():
    """
    Retrieve all sources from the database.
    """
    try:
        source_service = source_router.source_service
        sources = await source_service.get_sources_async()
        return {"success": True, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@source_router.post("/")
async def create_source(source_request: SourceCreateRequest):
    """
    Create a new source.
    """
    try:
        source_service = source_router.source_service
        source_id = await source_service.create_source_async(source_request)
        return {"success": True, "source_id": source_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@source_router.delete("/{source_id}")
async def delete_source(source_id: str):
    """
    Delete a source.
    """
    try:
        source_service = source_router.source_service
        await source_service.delete_source_async(source_id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
