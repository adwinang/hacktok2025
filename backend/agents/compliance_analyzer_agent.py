import os
from pathlib import Path
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from model.feature import Feature, FeatureStatus
from model.source_content import SourceContent
import dotenv
from pydantic import BaseModel
from typing import List

dotenv.load_dotenv()

llm = ChatAnthropic(
    model=os.getenv("ANTHROPIC_MODEL"),
    temperature=0.2,
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


class ComplianceAnalyzerAgentResponse(BaseModel):
    needs_action: bool
    original_status: FeatureStatus
    status_change_to: FeatureStatus
    reason: str
    confidence: float


class ComplianceAnalyzerAgent:
    def __init__(self):
        self.structured_llm = llm.with_structured_output(
            ComplianceAnalyzerAgentResponse)

    def _format_feature_for_prompt(self, feature: Feature) -> str:
        """Format feature information for prompt injection"""
        return f"Name: {feature.name}\nDescription: {feature.description}\nCurrent Status: {feature.status}"

    def _format_source_contents_for_prompt(self, source_contents: List[SourceContent]) -> str:
        """Format source contents for prompt injection"""
        formatted_sources = []
        for i, source_content in enumerate(source_contents, 1):
            formatted_sources.append(
                f"Source {i}:\n"
                f"Title: {source_content.title}\n"
                f"URL: {source_content.source_url}\n"
                f"Content: {source_content.content}"
            )
        return "\n\n".join(formatted_sources)

    async def analyze_compliance(self, source_contents: List[SourceContent], feature: Feature) -> ComplianceAnalyzerAgentResponse:
        """Analyze feature compliance against regulatory source requirements"""
        try:
            # Load system prompt template
            current_dir = Path(__file__).parent
            template_path = current_dir / "templates" / "compliance_analyzer.md"
            system_template_content = template_path.read_text(encoding='utf-8')

            # Format inputs for prompt
            formatted_feature = self._format_feature_for_prompt(feature)
            formatted_sources = self._format_source_contents_for_prompt(
                source_contents)

            # Create the chat prompt with separate system and human messages
            chat_prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=system_template_content),
                HumanMessage(content="Feature to Analyze:\n{feature_details}"),
                HumanMessage(
                    content="Regulatory Source Content:\n{source_content}")
            ])

            # Create chain and invoke
            chain = chat_prompt | self.structured_llm
            response = await chain.ainvoke({
                "feature_details": formatted_feature,
                "source_content": formatted_sources
            })

            return response

        except FileNotFoundError as e:
            raise FileNotFoundError(f"Template file not found: {e}")
        except Exception as e:
            raise RuntimeError(f"Error analyzing compliance: {e}")
