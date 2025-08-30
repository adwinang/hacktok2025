from datetime import datetime
from typing import List
from model.source import Source, SourceCreateRequest
from repository.source_repository import SourceRepositoryAsync
from agents.source_tagging_agent import SourceTaggingAgent


class SourceService:
    def __init__(self, source_repository: SourceRepositoryAsync, source_tagging_agent: SourceTaggingAgent):
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
                updated_at=None
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

    async def get_source_count_async(self) -> int:
        try:
            return await self.source_repository.get_source_count()
        except Exception as e:
            raise e
