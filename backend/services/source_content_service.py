from typing import List
from datetime import datetime
from repository.source_content_repository import SourceContentRepositoryAsync
from model.source_content import SourceContent, SourceContentCreateRequest


class SourceContentService:
    def __init__(self, source_content_repository: SourceContentRepositoryAsync):
        self.source_content_repository = source_content_repository

    async def get_source_contents_async(self) -> List[SourceContent]:
        try:
            source_contents_data = await self.source_content_repository.get_source_contents_async()
            source_contents = []
            for source_content_data in source_contents_data:
                source_content = SourceContent(**source_content_data)
                source_contents.append(source_content)
            return source_contents
        except Exception as e:
            raise e

    async def get_source_content_by_source_url_async(self, source_url: str) -> List[dict]:
        try:
            source_contents_data = await self.source_content_repository.get_source_content_by_source_url_async(source_url)
            source_contents = []
            for source_content_data in source_contents_data:
                source_content = SourceContent(**source_content_data)
                source_contents.append(source_content)
            return source_contents
        except Exception as e:
            raise e

    async def get_source_content_by_source_urls_async(self, source_urls: List[str]) -> List[SourceContent]:
        try:
            source_contents_data = await self.source_content_repository.get_source_content_by_source_urls_async(source_urls)
            source_contents = []
            for source_content_data in source_contents_data:
                source_content = SourceContent(**source_content_data)
                source_contents.append(source_content)
            return source_contents
        except Exception as e:
            raise e

    async def create_source_content_async(self, source_content: SourceContentCreateRequest) -> str:
        try:
            source_content_obj = SourceContent(
                source_url=str(source_content.source_url),
                title=str(source_content.title),
                content=str(source_content.content),
                created_at=datetime.utcnow(),
                updated_at=None
            )
            source_content_id = await self.source_content_repository.add_source_content_async(source_content_obj.model_dump())
            return source_content_id
        except Exception as e:
            raise e
