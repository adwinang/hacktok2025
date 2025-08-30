import os
import json
from pathlib import Path
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from model.source import Source
from model.source_content import SourceContent
import dotenv
from pydantic import BaseModel
from typing import List

dotenv.load_dotenv()

llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"),
                    temperature=0.2,
                    api_key=os.getenv("ANTHROPIC_API_KEY"))


class SourceTaggingAgentResponse(BaseModel):
    tags: List[str]


class SourceTaggingAgent:
    def __init__(self):
        self.structured_llm = llm.with_structured_output(
            SourceTaggingAgentResponse)

    def _load_available_tags(self) -> dict:
        """Load and parse the available tags from JSON file"""
        current_dir = Path(__file__).parent
        tags_path = current_dir / "resources" / "list_of_tags.json"

        with open(tags_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _format_tags_for_prompt(self, tags_data: dict) -> str:
        """Format JSON tags for prompt injection"""
        formatted = []
        for tag in tags_data["regulation_tags"]:
            formatted.append(
                f"• **{tag['tag']}** - {tag['name']}\n"
                f"  Description: {tag['description']}\n"
                f"  Examples: {', '.join(tag['examples'])}"
            )
        return "\n\n".join(formatted)

    async def generate_source_tags(self, source: Source, source_content: SourceContent) -> SourceTaggingAgentResponse:
        """Generate tags for a given source and source content"""
        try:
            # Load system prompt template
            current_dir = Path(__file__).parent
            template_path = current_dir / "templates" / "feature_tagging.md"
            system_template_content = template_path.read_text(encoding='utf-8')

            # Load and format available tags
            available_tags = self._load_available_tags()
            formatted_tags = self._format_tags_for_prompt(available_tags)

            # Simple string replacement instead of PromptTemplate to avoid curly brace conflicts
            formatted_system_prompt = system_template_content.replace(
                "{available_tags}", formatted_tags)

            chain_prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=formatted_system_prompt),
                HumanMessage(content=f"Source: {source}"),
                HumanMessage(content=f"Source Content: {source_content}"),
            ])

            chain = chain_prompt | self.structured_llm
            response = await chain.ainvoke({
                "source": source,
                "source_content": source_content,
            })

            return response

        except FileNotFoundError as e:
            raise FileNotFoundError(f"Template or tags file not found: {e}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in tags file: {e}")
        except Exception as e:
            raise RuntimeError(f"Error generating source tags: {e}")
