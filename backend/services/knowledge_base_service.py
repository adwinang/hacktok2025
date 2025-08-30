from typing import List
from model.source_content import SourceContentCreateRequest, SourceContentUpdate
from model.source import Source, SourceUpdateRequest

import requests
from readability import Document

from services.source_content_service import SourceContentService
from services.source_service import SourceService
from agents.source_tagging_agent import SourceTaggingAgent


class KnowledgeBaseService:
    def __init__(self, source_service: SourceService, source_content_service: SourceContentService, source_tagging_agent: SourceTaggingAgent):
        self.source_service = source_service
        self.source_content_service = source_content_service
        self.source_tagging_agent = source_tagging_agent
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
            headers = {
                "User-Agent": "Mozilla/5.0 (compatible; KnowledgeBaseBot/1.0; +https://aegir.co/bot)"
            }
            req = requests.get(source.source_url, headers=headers)
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
                # TODO: Extra, implement levenshtein distance to check if the two are similar
                # Proceed if the two do not have 97% similarity
                if actual_title == current_title and actual_content == current_content:
                    continue

            # Create a new source content
            await self.source_content_service.create_source_content_async(
                SourceContentCreateRequest(
                    source_url=source.source_url,
                    title=actual_title,
                    content=actual_content,
                )
            )

            created_source_content = await self.source_content_service.get_source_content_by_source_url_async(
                source.source_url
            )

            # Generate source tags using the source tagging agent
            source_tags = await self.source_tagging_agent.generate_source_tags(source, created_source_content)

            # Update source tags
            await self.source_service.update_source_async(source.id, SourceUpdateRequest(tags=source_tags.tags))

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
