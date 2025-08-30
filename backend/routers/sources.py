from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from model.source import Source, SourceCreateRequest, SourceIdsRequest
from model.source_content import SourceContentCreateRequest


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


@source_router.post("/ids")
async def get_sources_via_ids(source_ids_request: SourceIdsRequest):
    """
    Retrieve sources by IDs.
    """
    try:
        source_service = source_router.source_service
        sources = await source_service.get_sources_via_ids_async(
            source_ids_request.source_ids
        )
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


@source_router.get("/count")
async def get_source_count():
    """
    Retrieve the count of sources.
    """
    try:
        source_service = source_router.source_service
        count = await source_service.get_source_count_async()
        return {"success": True, "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@source_router.get("/contents")
async def get_source_contents():
    """
    Retrieve all source contents.
    """
    try:
        source_content_service = source_router.source_content_service
        source_contents = await source_content_service.get_source_contents_async()
        return {"success": True, "source_contents": source_contents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@source_router.get("/content")
async def get_source_content(url: str):
    """
    Retrieve source content by source URL.
    """
    try:
        source_content_service = source_router.source_content_service
        source_contents = (
            await source_content_service.get_source_content_by_source_url_async(url)
        )
        return {"success": True, "url": url, "source_contents": source_contents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@source_router.post("/content")
async def create_source_content(source_content_request: SourceContentCreateRequest):
    """
    Create a new source content.
    """
    try:
        source_content_service = source_router.source_content_service
        source_content_id = await source_content_service.create_source_content_async(
            source_content_request
        )
        return {"success": True, "source_content_id": source_content_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@source_router.post("/refresh-all")
async def refresh_all_sources():
    """
    Refresh all sources.
    """
    try:
        knowledge_base_service = source_router.knowledge_base_service
        source_contents_updates = (
            await knowledge_base_service.refresh_all_sources_content_async()
        )
        return {"success": True, "source_contents_updates": source_contents_updates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@source_router.post("/refresh")
async def refresh_given_sources(sources: List[Source]):
    """
    Refresh given sources.
    """
    try:
        knowledge_base_service = source_router.knowledge_base_service
        source_contents_updates = (
            await knowledge_base_service.refresh_given_sources_content_async(sources)
        )
        return {"success": True, "source_contents_updates": source_contents_updates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@source_router.get("/stream")
async def stream_sources():
    """
    Stream sources in real-time using Server-Sent Events (SSE).

    Sends initial list of sources followed by live updates on insert/update/replace.
    """
    try:
        source_service = source_router.source_service

        async def generate_sse_stream():
            async for sse_message in source_service.stream_sources_async():
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
            status_code=500, detail=f"Failed to stream sources: {str(e)}"
        )
