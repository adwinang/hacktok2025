from typing import List
from model.source_content import SourceContent, SourceContentCreateRequest, SourceContentUpdate
from model.source import Source

import requests
from readability import Document

from services.source_content_service import SourceContentService
from services.source_service import SourceService


class KnowledgeBaseService:
    def __init__(self, source_service: SourceService, source_content_service: SourceContentService):
        self.source_service = source_service
        self.source_content_service = source_content_service
        pass

    async def refresh_all_sources_content_async(self) -> List[SourceContentUpdate]:
        # Get all sources from the database
        sources = await self.source_service.get_sources_async()

        # Refresh the content for each source
        return await self.refresh_given_sources_content_async(sources)

    async def refresh_given_sources_content_async(self, sources: List[Source]) -> List[SourceContentUpdate]:
        # Get the source contents from the database for each source url
        current_source_contents = await self.source_content_service.get_source_content_by_source_urls_async(
            [source.source_url for source in sources]
        )

        # Create a dictionary source_url -> source_content (if multiple source_contents, take the latest one)
        source_contents_dict = {}
        for source_content in current_source_contents:
            existing = source_contents_dict.get(source_content.source_url)
            # Keep the latest one based on created_at timestamp
            if existing is None or source_content.created_at > existing.created_at:
                source_contents_dict[source_content.source_url] = source_content

        source_contents_update = []

        for source in sources:
            # Scrape the latest source content for each source url
            req = requests.get(source.source_url)
            doc = Document(req.text)
            actual_title = doc.title()
            actual_content = doc.summary()

            # Get the current source content from the database for each source url
            existing_source_content = source_contents_dict.get(
                source.source_url)

            # If there's existing content, check if it's the same
            if existing_source_content is not None:
                current_title = existing_source_content.title
                current_content = existing_source_content.content

                # If the two are the same, then skip
                if actual_title == current_title and actual_content == current_content:
                    print("called here")
                    continue

            print("called here 2")
            # Create a new source content
            await self.source_content_service.create_source_content_async(
                SourceContentCreateRequest(
                    source_url=source.source_url,
                    title=actual_title,
                    content=actual_content,
                )
            )

            # Add the source content update to the list
            source_contents_update.append(
                SourceContentUpdate(
                    source_id=source.id,
                    source_url=source.source_url,
                    title=actual_title,
                    content=actual_content,
                )
            )

        return source_contents_update
