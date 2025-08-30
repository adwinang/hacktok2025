import json
from datetime import datetime
from typing import AsyncGenerator, List
from model.source import Source, SourceCreateRequest, SourceUpdateRequest
from repository.source_repository import SourceRepositoryAsync
from agents.source_tagging_agent import SourceTaggingAgent


class SourceService:
    def __init__(
        self,
        source_repository: SourceRepositoryAsync,
        source_tagging_agent: SourceTaggingAgent,
    ):
        self.source_repository = source_repository
        self.source_tagging_agent = source_tagging_agent

    async def get_sources_async(self) -> list[Source]:
        try:
            sources_data = await self.source_repository.get_sources()
            sources = []
            for source_data in sources_data:
                source = Source(**source_data)
                sources.append(source)
            return sources
        except Exception as e:
            raise e

    async def get_sources_via_ids_async(self, source_ids: List[str]) -> list[Source]:
        try:
            sources_data = await self.source_repository.get_sources_via_ids(source_ids)
            sources = []
            for source_data in sources_data:
                source = Source(**source_data)
                sources.append(source)
            return sources
        except Exception as e:
            raise e

    async def create_source_async(self, source_request: SourceCreateRequest) -> str:
        try:
            # TODO: Add a pre-processing layer to add more metadata to the source
            source = Source(
                source_url=str(source_request.source_url),
                created_at=datetime.utcnow(),
                updated_at=None,
            )
            source_id = await self.source_repository.add_source(source.model_dump())
            return source_id
        except Exception as e:
            raise e

    async def delete_source_async(self, source_id: str) -> bool:
        try:
            return await self.source_repository.remove_source(source_id)
        except Exception as e:
            raise e

    async def update_source_async(
        self, source_id: str, source_request: SourceUpdateRequest
    ) -> bool:
        try:
            return await self.source_repository.update_source(
                source_id, source_request.model_dump()
            )
        except Exception as e:
            raise e

    async def get_source_count_async(self) -> int:
        try:
            return await self.source_repository.get_source_count()
        except Exception as e:
            raise e

    async def stream_sources_async(self) -> AsyncGenerator[str, None]:
        try:
            # Initial payload: all sources
            initial_sources = await self.get_sources_async()
            sources_data = []
            for source in initial_sources:
                source_dict = source.model_dump()
                if "created_at" in source_dict and source_dict["created_at"]:
                    source_dict["created_at"] = source_dict["created_at"].isoformat()
                if "updated_at" in source_dict and source_dict["updated_at"]:
                    source_dict["updated_at"] = source_dict["updated_at"].isoformat()
                sources_data.append(source_dict)

            initial_message = {
                "type": "initial_data",
                "data": {"sources": sources_data},
            }
            yield f"data: {json.dumps(initial_message)}\n\n"
            yield f": heartbeat\n\n"

            # Stream updates from MongoDB change stream
            async for change in self.source_repository.stream_sources():
                updated_doc = change["updated_document"].copy()
                if "created_at" in updated_doc and updated_doc["created_at"]:
                    updated_doc["created_at"] = updated_doc["created_at"].isoformat()
                if "updated_at" in updated_doc and updated_doc["updated_at"]:
                    updated_doc["updated_at"] = updated_doc["updated_at"].isoformat()

                change_message = {
                    "type": "source_update",
                    "data": {
                        "operation_type": change["operation_type"],
                        "source_id": change["source_id"],
                        "source_data": updated_doc,
                        "timestamp": change["timestamp"].as_datetime().isoformat(),
                    },
                }

                yield f"data: {json.dumps(change_message)}\n\n"

        except Exception as e:
            error_message = {
                "type": "error",
                "data": {"message": f"Streaming error: {str(e)}"},
            }
            yield f"data: {json.dumps(error_message)}\n\n"
